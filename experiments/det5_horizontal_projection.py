"""Exact elimination of two horizontal variables over four compact base parameters.

The formula describes a specified necessary relaxation, not actual bodies.
No SMT, floating optimizer or numerical feasibility test is used. Every
infeasible branch has a small strict-Farkas certificate; every feasible branch
has an exactly checked rational interior witness.
"""
from fractions import Fraction as Q
from itertools import combinations,product
from functools import lru_cache
from pathlib import Path
import hashlib,json
import sympy as s

ROOT=Path(__file__).resolve().parents[1]
BASE=s.symbols('p q C E')
a,tau=s.symbols('a tau')
p,q,C,E=BASE
L=1-p*q
A=C+p*E
B=q*C+E
S=C+E
ALPHA=(1-p)*E
y=(1-q)/L
DELTA=s.Rational(34728093,250000000)
THRESHOLD=s.Rational(183,100)
VECTORS=((1,0,0),(2,0,1),(1,0,1),(3,0,1))


def pieces(order):
    def positive(c,t):return (c*S+y*t,c*A+t)
    def negative(j,t):return (j*B,t-j*(A-B),j*S-y*t)
    if order=='lt':
        return (negative(2-a/3,tau),positive(1+2*a/3,2*tau),positive(3+a/3,tau),(3*tau-(1-a)*(A-B),))
    if order=='gt':
        return (positive(2+a/2,tau),(2*tau-(1-a)*(A-B),),negative(3-a/2,tau),positive(1+3*a/2,3*tau))
    raise ValueError('order')


def branches(order):return tuple(product(*(range(len(v)) for v in pieces(order))))


@lru_cache(None)
def coefficient_rows(order,pattern):
    k=3 if order=='lt' else 2
    pp=pieces(order)
    if tuple(pattern)not in branches(order):raise ValueError('piece pattern')
    rows=[('a positive',a),('a below one',1-a),('tau positive',tau),
          ('r below one',1-a*A/k-tau),('volume determinant margin',B*tau-DELTA),
          ('projected forced observer',L*(ALPHA*(a/k+s.Rational(1,5-k))-(1-y)*tau)),
          ('Z gauge',S-s.Rational(183,500)),
          ('height separation',L-(s.Rational(49,1500)if order=='lt'else s.Rational(249,1700)))]
    rows += [(str(v),L*(terms[i]-THRESHOLD))for v,terms,i in zip(VECTORS,pp,pattern)]
    output=[]
    for label,expr in rows:
        poly=s.Poly(s.cancel(expr),a,tau)
        if poly.total_degree()>1:raise ValueError('not affine')
        co=[s.expand(poly.coeff_monomial(m)) for m in(a,tau,1)]
        for value in co:s.Poly(value,*BASE)
        output.append({'label':label,'coefficients':co})
    return output


def dot(v,w):return sum(x*y for x,y in zip(v,w))
def cross(v,w):return v[0]*w[1]-v[1]*w[0]


def strict_farkas(rows):
    """Return a verified nonnegative circuit of at most three rows, or None."""
    rows=[tuple(map(Q,row)) for row in rows]
    def check(ids,weights):
        if not any(weights) or min(weights)<0:return None
        nn=[sum(weight*rows[i][j] for i,weight in zip(ids,weights))for j in(0,1)]
        constant=sum(weight*rows[i][2]for i,weight in zip(ids,weights))
        if nn!=[0,0]or constant>0:return None
        scale=sum(weights);weights=[w/scale for w in weights]
        return {'support':list(ids),'weights':list(map(str,weights)),'weighted_constant':str(constant/scale)}
    for i,row in enumerate(rows):
        if row[0]==row[1]==0 and row[2]<=0:return check((i,),(Q(1),))
    for i,j in combinations(range(len(rows)),2):
        u,v=rows[i][:2],rows[j][:2];uv=dot(u,v)
        if cross(u,v)==0 and uv<0:
            cert=check((i,j),(-uv,dot(u,u)))
            if cert:return cert
    for i,j,k in combinations(range(len(rows)),3):
        u,v,w=rows[i][:2],rows[j][:2],rows[k][:2]
        weights=[cross(v,w),cross(w,u),cross(u,v)]
        if min(weights)<0 and max(weights)<=0:weights=[-v for v in weights]
        cert=check((i,j,k),weights)
        if cert:return cert
    return None


def interior_witness(rows):
    """Average the vertices of the bounded closed polygon, then verify strictness."""
    rows=[tuple(map(Q,row)) for row in rows]
    vertices=set()
    for f,g in combinations(rows,2):
        d=cross(f[:2],g[:2])
        if not d:continue
        point=((f[1]*g[2]-g[1]*f[2])/d,(g[0]*f[2]-f[0]*g[2])/d)
        if all(dot(row[:2],point)+row[2]>=0 for row in rows):vertices.add(point)
    if not vertices:return None
    point=tuple(sum(v[k]for v in vertices)/len(vertices)for k in(0,1))
    if all(dot(row[:2],point)+row[2]>0 for row in rows):return point
    return None


def evaluate_rows(symbolic,base):
    mapping=dict(zip(BASE,map(Q,base)))
    return [tuple(Q(c.subs(mapping))for c in row['coefficients'])for row in symbolic]


def project(base,order):
    base=tuple(map(Q,base));p0,q0,c0,e0=base
    if not(0<=p0<1 and 0<=q0<1 and c0>0 and e0>0 and c0+e0<1):raise ValueError('compact base domain')
    outcomes=[]
    for pattern in branches(order):
        rows=evaluate_rows(coefficient_rows(order,pattern),base)
        witness=interior_witness(rows)
        if witness is not None:
            outcomes.append({'pattern':list(pattern),'status':'feasible','a':str(witness[0]),'tau':str(witness[1]),'minimum_strict_slack':str(min(dot(row[:2],witness)+row[2]for row in rows))})
        else:
            cert=strict_farkas(rows)
            if cert is None:raise AssertionError('bounded strict alternative incomplete')
            outcomes.append({'pattern':list(pattern),'status':'infeasible','certificate':cert})
    return {'base':list(map(str,base)),'order':order,'status':'feasible'if any(v['status']=='feasible'for v in outcomes)else'infeasible','branches':outcomes}


def sparse(poly):
    return [{'powers':list(powers),'coefficient':str(c)} for powers,c in s.Poly(poly,*BASE).terms()]


def build_certificate():
    paths=['proofs/DET5_NEGATIVE_DETERMINANT_GAUGE_NORMAL_FORM.md','proofs/DET5_FORCED_OBSERVER_BRANCH.md']
    return {'scope':'Quantifier-free projection recipe for the specified strict horizontal relaxation over four compact base parameters; not a sufficient body existence criterion.',
            'base_parameters':list(map(str,BASE)),'eliminated_variables':['a','tau'],
            'base_domain':['0<=p<1','0<=q<1','C>0','E>0','C+E<1'],
            'all_rows_strict_positive':True,'a_equals_one_strictification':'All other atoms are strict and continuous; perturb a=1 slightly downward while keeping tau fixed.',
            'threshold':'183/500','global_width_target':'17/5',
            'coefficient_order':['a','tau','constant'],
            'projection_rule':'OR over piece patterns: no nonnegative normal circuit of support<=3 has weighted constant<=0. Zero-normal, opposite-pair and same-signed cofactor-triple tests are explicit polynomial sign predicates.',
            'sources':{n:hashlib.sha256((ROOT/n).read_bytes()).hexdigest()for n in paths},
            'orders':{order:[{'pattern':list(pattern),'rows':[{'label':row['label'],'coefficients':[sparse(c)for c in row['coefficients']]}for row in coefficient_rows(order,pattern)]}for pattern in branches(order)]for order in('lt','gt')}}


def main():
    path=ROOT/'certificates/det5_horizontal_projection.json'
    cert=build_certificate();payload=json.dumps(cert,indent=2)+'\n'
    if path.exists()and path.read_text()!=payload:raise SystemExit('existing certificate differs; review before replacing')
    path.write_text(payload)
    samples=[('1/4','1/4','1/4','1/4'),('1/8','1/2','1/8','3/4'),('0','1/2','1/10','4/5'),('1/3','1/3','2/5','1/2'),('1/2','1/2','1/4','1/3')]
    out=ROOT/'results/det5_horizontal_projection_controls.json'
    if out.exists():print('Existing controls retained; no repeated computation');return
    rows=[project(base,order)for base in samples for order in('lt','gt')]
    result={'status':'PASS','scope':'Ten exact base controls, not continuous coverage. Each branch has a strict witness or a directly checkable Farkas circuit.',
            'certificate_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'solver_queries_run':0,'controls':rows}
    out.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'status':'PASS','branches_per_order':len(branches('lt')),'control_statuses':[(r['order'],r['status'])for r in rows],'solver_queries_run':0}))


if __name__=='__main__':main()
