"""Independent polynomial audit of the two archived bilinear class-5 models.

No experiment imports and no satisfiability calls. Exact rational polynomial
normalization checks every assertion, including each of the 15 width clauses.
This does not establish the satisfiability or infeasibility of either model.
"""
from fractions import Fraction as Q
from itertools import product, combinations
from math import gcd
from pathlib import Path
import hashlib, json
import z3

ROOT = Path(__file__).resolve().parents[1]


def need(value, reason):
    if not value:
        raise AssertionError(reason)


def polynomial(e):
    e = z3.simplify(e)
    if z3.is_rational_value(e):
        return {():e.as_fraction()} if e.as_fraction() else {}
    if z3.is_const(e):
        return {(str(e),):Q(1)}
    kind = e.decl().kind()
    if kind in (z3.Z3_OP_ADD,z3.Z3_OP_SUB,z3.Z3_OP_UMINUS):
        out = {}
        for i,c in enumerate(e.children()):
            sign = -1 if kind==z3.Z3_OP_UMINUS or (kind==z3.Z3_OP_SUB and i) else 1
            for monomial,value in polynomial(c).items():
                out[monomial] = out.get(monomial,Q(0))+sign*value
        return {m:v for m,v in out.items() if v}
    if kind==z3.Z3_OP_MUL:
        out = {():Q(1)}
        for c in e.children():
            updated = {}
            for a,x in out.items():
                for b,y in polynomial(c).items():
                    m = tuple(sorted(a+b))
                    updated[m] = updated.get(m,Q(0))+x*y
            out = {m:v for m,v in updated.items() if v}
        return out
    raise AssertionError('Unexpected arithmetic: '+str(e))


def canonical(e, negated=False):
    if z3.is_true(e): return not negated
    if z3.is_false(e): return negated
    if z3.is_not(e): return canonical(e.arg(0),not negated)
    if z3.is_and(e) or z3.is_or(e):
        conjunction = z3.is_and(e)^negated
        op = 'and' if conjunction else 'or'
        values = []
        for c in e.children():
            v = canonical(c,negated)
            if v is conjunction: continue
            if v is (not conjunction): return not conjunction
            if isinstance(v,tuple) and v[0]==op: values.extend(v[1])
            else: values.append(v)
        values = tuple(sorted(set(values),key=repr))
        return conjunction if not values else values[0] if len(values)==1 else (op,values)
    op = {z3.Z3_OP_LE:'<=',z3.Z3_OP_LT:'<',z3.Z3_OP_GE:'>=',z3.Z3_OP_GT:'>',z3.Z3_OP_EQ:'='}[e.decl().kind()]
    coeff = polynomial(e.arg(0)-e.arg(1))
    if negated: op = {'<=':'>','<':'>=','>=':'<','>':'<=','=':'!='}[op]
    if op in ('>','>='):
        op = {'>':'<','>=':'<='}[op]
        coeff = {m:-v for m,v in coeff.items()}
    if not coeff: return op in ('<=','=')
    items = sorted(coeff.items())
    scale = abs(items[0][1])
    if op in ('=','!=') and items[0][1]<0: scale = -scale
    return op,tuple((m,v/scale) for m,v in items)


def forms(assertions):
    return {v for e in assertions if (v:=canonical(z3.simplify(e))) is not True}


def expected(bounded):
    P = [[0,0,0],[5,1,2],[0,1,0],[0,0,1]]
    C = next(c for c in json.loads((ROOT/'certificates/nonunimodular_observer_guards.json').read_text())['classes'] if c['class_index']==5)
    S = next(c for c in json.loads((ROOT/'results/two_vector_class_scan.json').read_text())['classes'] if c['class_index']==5)
    need(C['contact_points']==P and len(C['guards'])==20,'fixed contacts and guards')
    F = [[z3.RealVal(0) for _ in range(4)] for _ in range(4)]
    for j in range(4):
        ids = [i for i in range(4) if i!=j]
        a,b = [z3.Real(f'f{i}{j}') for i in ids[:2]]
        for i,x in zip(ids,(a,b,1-a-b)): F[i][j]=x
    assertions = [F[i][j]>0 for i in range(4) for j in range(4) if i!=j]
    vectors = sorted(set(map(tuple,C['primitive_contact_edge_directions']))|{tuple(v['vector']) for v in S['eligible_vectors']})
    def bary(point,affine=False):
        x,y,z = map(Q,point)
        return [int(affine)+2*x/5-y-z,x/5,y-x/5,z-2*x/5]
    for beta in ('37/102','183/500'):
        for v in vectors:
            l = bary(v)
            values = [sum(F[i][j]*z3.RealVal(str(l[j])) for j in range(4)) for i in range(4)]
            assertions.append(z3.Or(*[sum(values[i] for i in range(4) if mask&(1<<i))>z3.RealVal(beta) for mask in range(1,15)]))
    for v in C['guards']:
        l = bary(v,True)
        assertions.append(z3.Or(*[sum(F[i][j]*z3.RealVal(str(l[j])) for j in range(4))<=0 for i in range(4)]))
    V = [[z3.Real(f'v{i}_{k}') for k in range(3)] for i in range(4)]
    equations = [sum(F[i][j]*V[i][k] for i in range(4))==P[j][k] for j in range(4) for k in range(3)]
    assertions.extend(equations)
    if bounded:
        cap = z3.RealVal('50000000/2042829')
        for x,y,z in V:
            l = [1+2*x/5-y-z,x/5,y-x/5,z-2*x/5]
            assertions += [sum(l[j] for j in range(4) if mask&(1<<j))<cap for mask in range(1,15)]
    # Contact heights bound |y|,|z|<=3 and |5x|<=3+3+6=12.
    directions=[]
    for u in product(range(-2,3),range(-3,4),range(-3,4)):
        if not any(u) or gcd(*u)!=1 or next(x for x in u if x)<0: continue
        h=[sum(u[k]*p[k] for k in range(3)) for p in P]
        if max(h)-min(h)<=3: directions.append(u)
    need(len(directions)==15,'complete fifteen directions')
    widths=[]
    for u in directions:
        h=[sum(u[k]*v[k] for k in range(3)) for v in V]
        widths.append(z3.Or(*[sign*(h[i]-h[j])>z3.RealVal('17/5') for i,j in combinations(range(4),2) for sign in (-1,1)]))
    assertions.extend(widths)
    return assertions,equations,widths,directions


def main():
    archive=json.loads((ROOT/'results/det5_complete_vertex_lift.json').read_text())
    report=[]; mutations=[]
    for name,bounded in [('bilinear',False),('bilinear_volume',True)]:
        row=next(r for r in archive['queries'] if r['model']==name)
        path=ROOT/row['path'];raw=path.read_bytes()
        need(hashlib.sha256(raw).hexdigest()==row['input_sha256'],'archived input hash')
        actual=list(z3.parse_smt2_file(str(path)))
        want,equations,widths,directions=expected(bounded)
        need(row['width_directions']==[list(u) for u in sorted(directions)],'archived complete direction set')
        need(forms(actual)==forms(want),'complete independent polynomial assertion set')
        normalized=forms(actual)
        for label,changed in [
            ('missing width clause',normalized-{canonical(widths[0])}),
            ('wrong affine contact equation',normalized-{canonical(equations[0])}|{canonical(equations[0].arg(0)==1)}),
            ('extraneous contradiction',normalized|{False})]:
            need(changed!=forms(want),'mutation not detected: '+label)
            mutations.append({'model':name,'mutation':label,'rejected':True})
        report.append({'model':name,'assertion_count':len(actual),'width_direction_count':15,
                       'archived_status':row['status'],'input_sha256':row['input_sha256']})
    out={'status':'PASS','models':report,'mutations':mutations,'solver_queries_run':0,
         'scope':'Independent exact polynomial encoding audit only; archived UNKNOWN outcomes do not exclude the class. Cubic target not re-audited here.'}
    (ROOT/'results/det5_vertex_lift_encoding_validation.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out))


if __name__=='__main__': main()
