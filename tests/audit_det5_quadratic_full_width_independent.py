"""Independent degree-five complete-width input audit; no solver queries."""
from collections import Counter
from fractions import Fraction as Q
from itertools import permutations, product
from math import gcd
from pathlib import Path
import hashlib
import json
import re

import sympy as s
import z3
import audit_det5_scaled_frame_independent as arithmetic
from audit_det5_quadratic_chart_independent import (
    NAMES, VECTORS, eliminated, as_z3, forms, read, sha,
)

ROOT=Path(__file__).resolve().parents[1]


def polynomial(expr):
    if z3.is_rational_value(expr):
        return {():expr.as_fraction()}
    if z3.is_const(expr):
        assert expr.sort().kind()==z3.Z3_REAL_SORT
        return {(str(expr),):Q(1)}
    kind=expr.decl().kind()
    kids=expr.children()
    if kind in (z3.Z3_OP_ADD,z3.Z3_OP_SUB,z3.Z3_OP_UMINUS):
        out={}
        for i,k in enumerate(kids):
            sign=-1 if kind==z3.Z3_OP_UMINUS or (kind==z3.Z3_OP_SUB and i) else 1
            for m,c in polynomial(k).items():
                out[m]=out.get(m,Q(0))+sign*c
        return {m:c for m,c in out.items() if c}
    if kind==z3.Z3_OP_POWER:
        assert z3.is_rational_value(kids[1])
        n=kids[1].as_fraction()
        assert n.denominator==1 and 0<=n<=5
        kids=[kids[0]]*int(n)
        kind=z3.Z3_OP_MUL
    if kind==z3.Z3_OP_MUL:
        out={():Q(1)}
        for k in kids:
            new={}
            for m,c in out.items():
                for n,d in polynomial(k).items():
                    key=tuple(sorted(m+n))
                    assert len(key)<=5
                    new[key]=new.get(key,Q(0))+c*d
            out={m:c for m,c in new.items() if c}
        return out
    raise ValueError("Not a polynomial: "+str(expr))


# Reuse only the established Boolean/canonical comparison implementation.
# Its exact coefficient parser is replaced locally by the degree-five parser.
arithmetic.polynomial=polynomial


def determinant3(M):
    out=0
    for p in permutations(range(3)):
        inversions=sum(p[i]>p[j] for i in range(3) for j in range(i+1,3))
        out+=(-1)**inversions*product_expr(M[i,p[i]] for i in range(3))
    return s.expand(out)


def product_expr(values):
    out=1
    for v in values:
        out*=v
    return out


def cofactors(F):
    return s.Matrix(4,4,lambda i,j:(-1)**(i+j)*determinant3(F.minor_submatrix(j,i)))


def normalize_abs(expressions,delta):
    pos=polynomial(delta)
    neg={m:-c for m,c in pos.items()}
    positive=forms([delta>0])
    nonpositive=forms([delta<=0])
    count=0

    def visit(expr):
        nonlocal count
        if z3.is_app(expr) and expr.decl().kind()==z3.Z3_OP_ITE:
            condition,left,right=expr.children()
            cp=forms([condition])
            lp,rp=polynomial(left),polynomial(right)
            assert ((cp==positive and lp==pos and rp==neg)
                    or (cp==nonpositive and lp==neg and rp==pos))
            count+=1
            return z3.Real("__abs_det")
        if not expr.children():
            return expr
        return expr.decl()(*[visit(k) for k in expr.children()])

    normalized=[visit(e) for e in expressions]
    assert count>0
    return normalized,count


def rational_assignment(row):
    values={}
    for name,raw in row["assignment"].items():
        atom=z3.parse_smt2_string("(declare-fun v () Real) (assert (= v "+raw+"))")[0].arg(1)
        atom=z3.simplify(atom)
        assert z3.is_rational_value(atom)
        values[name]=atom
    return [(z3.Real(name),value) for name,value in values.items()]


def main():
    path="results/det5_quadratic_full_width.json"
    archive=read(path)
    assert archive["variables"]==list(NAMES)
    assert archive["beta"]=="183/500" and archive["target"]=="17/5"
    assert archive["extra_gauges"]==[[1,-1,1]]
    assert archive["maximum_polynomial_degree"]==5
    assert len(archive["queries"])==2
    assert {r["order"] for r in archive["queries"]}=={"lt","gt"}
    C=next(c for c in read("certificates/nonunimodular_observer_guards.json")["classes"] if c["class_index"]==5)
    assert C["contact_points"]==[[0,0,0],[5,1,2],[0,1,0],[0,0,1]]
    P=s.Matrix([[1]*4]+[[v[k] for v in C["contact_points"]] for k in range(3)])
    inv=P.inv()
    directions=[]
    for v in product(range(-2,3),range(-3,4),range(-3,4)):
        if not any(v) or gcd(*v)!=1 or next(k for k in v if k)<0:
            continue
        heights=[sum(v[k]*point[k] for k in range(3)) for point in C["contact_points"]]
        if max(heights)-min(heights)<=3:
            directions.append(list(v))
    assert len(directions)==15
    geometry=read("results/det5_complete_geometry_validation.json")
    assert geometry["status"]=="PASS" and geometry["directions"]==directions
    assert read("results/det5_quadratic_chart_encoding_validation.json")["status"]=="PASS"
    old=read("results/det5_class5_y_cvc5_validation.json")
    boxes=[r["box"] for r in old["leaves"] if r["extrema"]==[0,3]]
    boxes.append(read("results/det5_y_corner_enlarged_3_5.json")["box"])
    assert len(boxes)==8
    gauge_vectors=sorted(set(VECTORS)|{(1,-1,1)})
    assert len(gauge_vectors)==11
    weak=next(r for r in read("results/det5_quadratic_height_chart.json")["queries"] if r["status"]=="sat")
    weak_subs=rational_assignment(weak)
    reports=[]
    identities=0
    witness_failures=None
    for row in archive["queries"]:
        symbols,F,q,a,b=eliminated(row["order"])
        x,y,t,c,e,r,u,h=symbols
        adj=cofactors(F)
        determinant=s.expand(b*(u*((1-x)*c+x*e)-r*((1-y)*c+y*e)))
        for entry in F*adj-determinant*s.eye(4):
            assert s.expand(entry)==0
            identities+=1
        numerators=P[1:,:]*adj
        delta=as_z3(determinant)
        assert max(map(len,polynomial(delta)))==5
        X,Y,T,Cc,E,R,U,H=map(as_z3,symbols)
        expected=[X>=0,Y<=1,X<Y,T>0,T<1,Cc>0,E>0,as_z3(b)>0,as_z3(b)<z3.RealVal("5/17")]
        expected += [as_z3(F[i,j])>0 for i in range(4) for j in range(4) if i!=j]
        beta=z3.RealVal("183/500")
        for v in gauge_vectors:
            image=F*inv*s.Matrix([0,*v])
            if v==(0,0,1):
                expected.append(as_z3(y*e+(1-x)*c)>beta)
            else:
                expected.append(z3.Or(*[as_z3(sum(image[i] for i in range(4) if mask&(1<<i)))>beta for mask in range(1,15)]))
        for guard in C["guards"]:
            image=F*inv*s.Matrix([1,*guard])
            expected.append(z3.Or(*[as_z3(v)<=0 for v in image]))
        for box in boxes:
            expected.append(z3.Or(*[cut for i,(lo,hi) in zip((1,2),box)
                                   for cut in (as_z3(q[i])<z3.RealVal(lo),as_z3(q[i])>z3.RealVal(hi))]))
        assert len(expected)==60
        expected.append(delta!=0)
        absdet=z3.Real("__abs_det")
        width_rows=[]
        for direction in directions:
            if direction==[0,1,0]:
                continue
            gaps=[s.expand(sum(direction[k]*(numerators[k,i]-numerators[k,j]) for k in range(3)))
                  for i in range(4) for j in range(i)]
            max_degree=max(s.Poly(g,*symbols).total_degree() for g in gaps)
            assert max_degree<=5
            width_rows.append({"direction":direction,"pairs":6,"maximum_numerator_degree":max_degree})
            expected.append(z3.Or(*[cut for g in gaps for cut in
                                    (as_z3(5*g)>17*absdet,as_z3(-5*g)>17*absdet)]))
        assert len(expected)==75
        assert row["cleared_widths"]==width_rows
        assert row["Y_width_encoded_by_gap"] is True
        assert row["gauge_vectors"]==[list(v) for v in gauge_vectors]
        assert row["excluded_rectangles"]==boxes
        assert sha(row["input_path"])==row["input_sha256"]
        raw=(ROOT/row["input_path"]).read_text()
        declared=re.findall(r"\(declare-fun\s+(\S+)\s+\(\)\s+Real\)",raw)
        assert len(declared)==8 and set(declared)==set(NAMES)
        actual=list(z3.parse_smt2_string(raw))
        assert len(actual)==row["assertions"]==75
        normalized,ite_count=normalize_abs(actual,delta)
        assert forms(normalized)==forms(expected)
        assert forms(normalized)!=forms(expected[:-1])
        assert forms(normalized)!=forms(expected[:60]+expected[61:])
        if row["order"]==weak["order"]:
            flags=[z3.simplify(z3.substitute(expr,*weak_subs)) for expr in actual]
            assert all(z3.is_true(v) or z3.is_false(v) for v in flags)
            failed=[i for i,v in enumerate(flags) if z3.is_false(v)]
            assert failed and any(i>=61 for i in failed)
            assert any(21<=i<32 for i in failed)
            witness_failures={"assertion_indices":failed,
                              "failed_gauge_count":sum(21<=i<32 for i in failed),
                              "failed_width_count":sum(i>=61 for i in failed)}
            witness_failures["failed_width_directions"]=[width_rows[i-61]["direction"] for i in failed if i>=61]
        reports.append({"order":row["order"],"status":row["status"],"input_sha256":row["input_sha256"],
                        "assertions":75,"variables":8,"maximum_polynomial_degree":5,
                        "checked_absolute_determinant_terms":ite_count,"widths":15})
    assert witness_failures
    receipt={"status":"PASS","scope":"Independent complete-width input and cofactor identities; no solver status is a proof.",
             "source_archive_sha256":sha(path),"queries":reports,"adjugate_entry_identities":identities,
             "complete_directions":directions,"complete_geometry_receipt_sha256":sha("results/det5_complete_geometry_validation.json"),
             "prior_chart_encoding_receipt_sha256":sha("results/det5_quadratic_chart_encoding_validation.json"),
             "weak_witness_rejection":witness_failures,"missing_width_control":True,"missing_determinant_control":True,
             "solver_queries_run":0,"proof_kernel_calls_run":0}
    (ROOT/"results/det5_quadratic_full_width_encoding_validation.json").write_text(json.dumps(receipt,indent=2)+"\n")
    print("QUADRATIC_FULL_WIDTH_INDEPENDENT=PASS")


if __name__=="__main__":
    main()
