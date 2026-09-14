"""Independently eliminate column equations and audit archived quadratic inputs."""
from collections import Counter
from fractions import Fraction
from pathlib import Path
import hashlib
import json
import re

import sympy as s
import z3
from audit_det5_scaled_frame_independent import canonical
import replay_det5_conditional_width_bounds as oldproof

ROOT=Path(__file__).resolve().parents[1]
NAMES=("low","high","theta","c","e","r","u","h")
VECTORS=[(0,0,1),(0,1,-1),(0,1,0),(1,0,0),(1,0,1),
         (2,0,1),(3,0,1),(5,0,2),(5,1,1),(5,1,2)]
BETA=s.Rational(37,102)


def sha(path):
    return hashlib.sha256((ROOT/path).read_bytes()).hexdigest()


def read(path):
    return json.loads((ROOT/path).read_text())


def eliminated(order):
    x,y,t,c,e,r,u,h=s.symbols(" ".join(NAMES))
    a=x+t*(y-x)
    perm=[0,1,2,3] if order=="lt" else [0,2,1,3]
    q=s.Matrix([0,0,0,1])
    q[perm[1]],q[perm[2]]=x,y
    F=s.zeros(4)
    # Assign exactly one independent entry per column; derive the other two
    # from stochasticity and the contact-height equation.
    free={perm[0]:(perm[3],(y-x)*c),
          perm[1]:(perm[2],r),
          perm[2]:(perm[1],u),
          perm[3]:(perm[0],(y-x)*e)}
    for j,(k,v) in free.items():
        F[k,j]=v
        i,l=[i for i in range(4) if i not in (j,k)]
        target=a if j in (0,3) else h
        F[i,j]=s.cancel((target-q[k]*v-q[l]*(1-v))/(q[i]-q[l]))
        F[l,j]=s.expand(1-v-F[i,j])
    return (x,y,t,c,e,r,u,h),F,q,a,h-a


def as_z3(expr):
    expr=s.sympify(expr)
    if expr.is_Rational:
        return z3.RealVal(str(expr))
    if expr.is_Symbol:
        return z3.Real(str(expr))
    if expr.is_Add:
        return sum(as_z3(v) for v in expr.args)
    if expr.is_Mul:
        out=z3.RealVal(1)
        for v in expr.args:
            out=out*as_z3(v)
        return out
    if expr.is_Pow and expr.args[1].is_Integer and expr.args[1]>=0:
        out=z3.RealVal(1)
        for _ in range(int(expr.args[1])):
            out=out*as_z3(expr.args[0])
        return out
    raise ValueError("Unexpected expression "+str(expr))


def forms(expressions):
    def unfold(e):
        if z3.is_eq(e) and z3.is_bool(e.arg(0)):
            a,b=map(unfold,e.children())
            return z3.Or(z3.And(a,b),z3.And(z3.Not(a),z3.Not(b)))
        if z3.is_not(e):
            return z3.Not(unfold(e.arg(0)))
        if z3.is_or(e):
            return z3.Or(*map(unfold,e.children()))
        if z3.is_and(e):
            return z3.And(*map(unfold,e.children()))
        return e
    return Counter(canonical(unfold(z3.simplify(e))) for e in expressions)


def main():
    path="results/det5_quadratic_height_chart.json"
    archive=read(path)
    assert archive["variables"]==list(NAMES)
    assert archive["maximum_polynomial_degree"]==2
    assert archive["lifted_product_variables"]==0
    assert archive["beta"]=="37/102" and archive["target"]=="17/5"
    assert len(archive["queries"])==2
    assert {r["order"] for r in archive["queries"]}=={"lt","gt"}
    C=next(c for c in read("certificates/nonunimodular_observer_guards.json")["classes"] if c["class_index"]==5)
    assert len(C["guards"])==20
    P=s.Matrix([[1]*4]+[[s.Rational(v[k]) for v in C["contact_points"]] for k in range(3)])
    assert abs(P.det())==5
    inv=P.inv()
    oldpath="results/det5_class5_y_cvc5_validation.json"
    newpath="results/det5_y_corner_enlarged_3_5.json"
    old,new=read(oldpath),read(newpath)
    assert old["status"]=="PASS"
    leaves=[r for r in old["leaves"] if r["extrema"]==[0,3]]+[new]
    assert len(leaves)==8
    proofbindings=[oldproof.audit_row(C,r,[0,3],r["box"],Fraction(37,102)) for r in leaves]
    boxes=[r["box"] for r in leaves]
    rows=[]
    fixture_count=0
    for row in archive["queries"]:
        symbols,F,q,a,b=eliminated(row["order"])
        x,y,t,c,e,r,u,h=symbols
        assert all(s.expand(v)==0 for v in F.T*s.ones(4,1)-s.ones(4,1))
        assert all(s.expand(v)==0 for v in F.T*q-a*s.ones(4,1)-b*s.Matrix([0,1,1,0]))
        for v in F:
            assert s.Poly(v,*symbols).total_degree()<=2
        A=(1-x)*c+x*e
        B=(1-y)*c+y*e
        assert s.expand(s.cancel(F.det())-b*(u*A-r*B))==0
        X,Y,T,Cc,E,R,U,H=map(as_z3,symbols)
        expected=[X>=0,Y<=1,X<Y,T>0,T<1,Cc>0,E>0,as_z3(b)>0,as_z3(b)<z3.RealVal("5/17")]
        expected += [as_z3(F[i,j])>0 for i in range(4) for j in range(4) if i!=j]
        gauge_expressions=[]
        for v in VECTORS:
            co=inv*s.Matrix([0,*v])
            image=F*co
            if v==(0,0,1):
                positive=[i for i in range(4) if i in (0,(2 if row["order"]=="lt" else 1))]
                gauge=sum(image[i] for i in positive)
                assert s.expand(gauge-(y*e+(1-x)*c))==0
                constraint=as_z3(gauge)>as_z3(BETA)
            else:
                constraint=z3.Or(*[as_z3(sum(image[i] for i in range(4) if mask&(1<<i)))>as_z3(BETA) for mask in range(1,15)])
            expected.append(constraint)
            gauge_expressions.append(constraint)
        for guard in C["guards"]:
            image=F*inv*s.Matrix([1,*guard])
            expected.append(z3.Or(*[as_z3(v)<=0 for v in image]))
        for box in boxes:
            expected.append(z3.Or(*[cut for i,(lo,hi) in zip((1,2),box)
                                   for cut in (as_z3(q[i])<z3.RealVal(lo),as_z3(q[i])>z3.RealVal(hi))]))
        assert len(expected)==59
        assert row["gauge_vectors"]==[list(v) for v in VECTORS]
        assert row["excluded_rectangles"]==boxes
        assert sha(row["input_path"])==row["input_sha256"]
        raw=(ROOT/row["input_path"]).read_text()
        declarations=re.findall(r"\(declare-fun\s+(\S+)\s+\(\)\s+Real\)",raw)
        assert len(declarations)==8 and set(declarations)==set(NAMES)
        actual=list(z3.parse_smt2_string(raw))
        assert len(actual)==row["assertions"]==59
        # Canonical comparison also independently rejects any polynomial degree >2.
        assert forms(actual)==forms(expected)
        assert forms(actual)!=forms(expected[:-1])
        assert forms(actual)!=forms(expected[:8]+expected[9:])
        assert forms(actual)!=forms(expected[:21]+expected[22:])
        sat_checks=0
        if row["status"]=="sat":
            assert row["rational_assignment"] and row["all_assertions_true"]
            assert set(row["assignment"])==set(NAMES)
            substitutions=[]
            for name,value in row["assignment"].items():
                eq=z3.parse_smt2_string("(declare-fun value () Real) (assert (= value "+value+"))")[0]
                val=z3.simplify(eq.arg(1))
                assert z3.is_rational_value(val)
                substitutions.append((z3.Real(name),val))
            for expr in actual:
                assert z3.is_true(z3.simplify(z3.substitute(expr,*substitutions)))
                sat_checks+=1
        for xv,yv in [(0,s.Rational(3,4)),(s.Rational(1,4),1),(0,1)]:
            tv=s.Rational(1,2)
            av=xv+tv*(yv-xv)
            values={x:xv,y:yv,t:tv,c:s.Rational(1,10),e:s.Rational(1,5),
                    r:s.Rational(1,10),u:s.Rational(3,20),h:(av+1)/2}
            M=F.subs(values)
            assert all(M[i,j]>0 for i in range(4) for j in range(4) if i!=j)
            assert M.det()!=0
            V=P*M.inv()
            heights=list(V[2,:])
            assert min(heights)==heights[0] and max(heights)==heights[3]
            assert max(heights)-min(heights)==1/b.subs(values)
            assert all(s.cancel(q[i].subs(values)-b.subs(values)*heights[i]-a.subs(values))==0 for i in range(4))
            fixture_count+=1
        rows.append({"order":row["order"],"status":row["status"],
                     "input_sha256":row["input_sha256"],"assertions":59,
                     "variables":8,"maximum_polynomial_degree":2,
                     "exact_saved_sat_assertions":sat_checks})
    receipt={"status":"PASS","scope":"Independent elimination, formula and exact saved-SAT audit; no exclusion follows from UNKNOWN.",
             "source_archive_sha256":sha(path),"queries":rows,
             "rectangle_proof_bindings":proofbindings,"endpoint_body_fixtures":fixture_count,
             "missing_rectangle_control":True,"missing_gap_target_control":True,
             "missing_gauge_control":True,"solver_queries_run":0,"proof_kernel_calls_run":0}
    (ROOT/"results/det5_quadratic_chart_encoding_validation.json").write_text(json.dumps(receipt,indent=2)+"\n")
    print("QUADRATIC_CHART_INDEPENDENT=PASS")


if __name__=="__main__":
    main()
