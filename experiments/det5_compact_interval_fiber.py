"""Exact polynomial outer LRA models on continuous compact shape boxes.

The positive multiplier L clears every fiber coefficient. No solver is called
by construction; each named driver query is archived once, including its proof.
A refutation covers only its recorded box, order and determinant sign.
"""
from fractions import Fraction as Q
from functools import lru_cache
from pathlib import Path
import argparse,gzip,hashlib,json,sys
import sympy as s
import z3
from experiments.det5_horizontal_fiber_oracle import coordinates,statement,rational,VECTORS

ROOT=Path(__file__).resolve().parents[1]
P,QVAR,C,E,R,U=s.symbols('p q C E r u')
SHAPE=(P,QVAR,C,E,R,U)
T,H,Z=s.symbols('alpha eta rho')
FIBER=(T,H,Z)
L=1-P*QVAR
BETA=s.Rational(183,500)
W=s.Rational(17,5)
MAX=s.Rational(50000000,2042829)


def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()


def atom(expr,relation):
    expr=s.Poly(s.expand(expr),*FIBER)
    if expr.total_degree()>1:raise ValueError('nonlinear fiber atom')
    coefficients=[expr.coeff_monomial(m) for m in (1,T,H,Z)]
    for c in coefficients:s.Poly(c,*SHAPE)
    return {'relation':relation,'coefficients':coefficients}


def any_of(*nodes):return {'or':list(nodes)}


@lru_cache(None)
def exact_model(order,sign):
    if order not in ('lt','gt') or sign not in (-1,1):raise ValueError('chart/sign')
    certpath=ROOT/'certificates/det5_horizontal_fiber_structure.json'
    cert=json.loads(certpath.read_text())
    branch=next(b for b in cert['branches'] if b['order']==order)
    x,y,c,e,r,u=s.symbols('low high c e r u')
    old=(x,y,c,e,r,u)
    sub={x:P*(1-QVAR)/L,y:(1-QVAR)/L,c:C*L/(1-P),e:E*L/(1-QVAR),r:R,u:U}
    def decode(terms):
        f=sum(s.Rational(t['coefficient'])*s.prod(v**n for v,n in zip(old,t['powers'])) for t in terms)
        return s.Poly(s.cancel(L*f.subs(sub,simultaneous=True)),*SHAPE).as_expr()
    def linear(row):return sum(decode(row[k])*z for k,z in zip(('alpha','eta','rho'),FIBER))
    M=s.zeros(4)
    for row in branch['scaled_F_entries']:M[row['row'],row['column']]=linear(row)
    pairs={(row['coordinate'],*row['vertex_pair']):linear(row) for row in branch['coordinate_pair_numerators']}
    D=U*(C+P*E)-R*(QVAR*C+E)
    rows=[]
    def add(expr,rel,label):rows.append({'label':label,'formula':atom(expr,rel)})
    add(H*L-P*(1-QVAR)*Z-(1-P)*(1-QVAR)*T-L,'=','height normalization')
    for expr in (Z-W,MAX-Z,T,Z-T,H,Z-H):add(expr,'>','projective bounds')
    for a in (P,QVAR):add(a,'>=','compact shape');add(1-a,'>','compact shape')
    for a in (C,E,R,U):add(a,'>','compact shape')
    for a in (1-C-E,1-R,1-U):add(a,'>','compact shape')
    delta=s.Rational(49,1500) if order=='lt' else s.Rational(249,1700)
    add(L-delta,'>','analytic height separation')
    add(sign*D-Z/MAX,'>','global volume determinant margin')
    add(C+E-BETA,'>','horizontal Z gauge')
    add(MAX*(1-P)-L,'>','global gap compact face margin')
    if sign==1:add((C+P*E)*(QVAR*C+E)-(3 if order=='lt' else 2)*W/MAX,'>','positive determinant product margin')
    for i in range(4):
        for j in range(4):
            if i!=j:add(M[i,j],'>','strict facet contact')
    for v in VECTORS:
        image=M*s.Matrix(coordinates(v))
        rows.append({'label':'gauge '+str(v),'formula':any_of(*[atom(sum(image[i] for i in range(4) if mask&(1<<i))-BETA*L*Z,'>') for mask in range(1,15)])})
    guardpath=ROOT/'certificates/nonunimodular_observer_guards.json'
    guards=next(c for c in json.loads(guardpath.read_text())['classes'] if c['class_index']==5)['guards']
    for point in guards:
        image=M*s.Matrix(coordinates(point,True))
        rows.append({'label':'observer '+str(point),'formula':any_of(*[atom(a,'<=') for a in image])})
    # Direct two-observer consequence avoids introducing spurious R3 options.
    add(QVAR*C+E-(3 if order=='lt' else 2)*U,'>=','simplified first observer')
    directionpath=ROOT/'results/det5_complete_geometry_validation.json'
    directions=json.loads(directionpath.read_text())['directions']
    for v in directions:
        if v==[0,1,0]:continue
        gaps=[sum(v[k]*pairs[k,i,j] for k in range(3)) for i in range(4) for j in range(i)]
        rows.append({'label':'width '+str(v),'formula':any_of(*[atom(eps*5*g-17*sign*D*L,'>') for g in gaps for eps in (-1,1)])})
    oldpath=ROOT/'results/det5_class5_y_cvc5_validation.json'
    extrapath=ROOT/'results/det5_y_corner_enlarged_3_5.json'
    anchorpath=ROOT/'results/det5_strong_anchor_rectangle.json'
    boxes=[b['box'] for b in json.loads(oldpath.read_text())['leaves'] if b['extrema']==[0,3]]
    boxes += [json.loads(extrapath.read_text())['box'],json.loads(anchorpath.read_text())['box']]
    hn=[P*(1-QVAR),1-QVAR] if order=='lt' else [1-QVAR,P*(1-QVAR)]
    for box in boxes:
        rows.append({'label':'closed rectangle complement '+str(box),'formula':any_of(*[atom(expr,'>') for h,(lo,hi) in zip(hn,box) for expr in (s.Rational(lo)*L-h,h-s.Rational(hi)*L)])})
    sources=[certpath,guardpath,directionpath,oldpath,extrapath,anchorpath,
             ROOT/'proofs/DET5_COMPACT_SHAPE_CHART_REVIEW.md',ROOT/'proofs/DET5_HORIZONTAL_FIBER_INTERVAL_LIFTING.md']
    return rows,{'order':order,'determinant_sign':sign,'positive_multiplier':'1-p*q','target':'17/5',
                 'sources':{str(p.relative_to(ROOT)):digest(p) for p in sources}}


def times(a,b):
    vals=[x*y for x in a for y in b];return min(vals),max(vals)


def interval(poly,box):
    lo=hi=Q(0)
    for powers,coefficient in s.Poly(poly,*SHAPE).terms():
        term=(Q(coefficient),Q(coefficient))
        for bounds,n in zip(box,powers):
            power=(Q(1),Q(1))
            for _ in range(n):power=times(power,bounds)
            term=times(term,power)
        lo+=term[0];hi+=term[1]
    return lo,hi


def compile_box(box,order,sign,closed=False):
    box=tuple(tuple(map(Q,b)) for b in box)
    if len(box)!=6 or any(len(b)!=2 or not(0<=b[0]<=b[1]<=1) for b in box):raise ValueError('six closed subintervals of [0,1]')
    rows,metadata=exact_model(order,sign)
    z=z3.Reals('alpha eta rho');zz=(z3.RealVal(1),*z)
    envelopes=[]
    def outer(node):
        if 'or' in node:return z3.Or(*[outer(c) for c in node['or']])
        bounds=[interval(c,box) for c in node['coefficients']]
        lower=sum(rational(b[0])*a for b,a in zip(bounds,zz));upper=sum(rational(b[1])*a for b,a in zip(bounds,zz))
        rel=node['relation'];envelopes.append({'relation':rel,'bounds':[[str(v) for v in b] for b in bounds]})
        if closed:rel={'>':'>=','<':'<='}.get(rel,rel)
        if rel=='>':return upper>0
        if rel=='>=':return upper>=0
        if rel=='<':return lower<0
        if rel=='<=':return lower<=0
        if rel=='=':return z3.And(lower<=0,upper>=0)
        raise ValueError('relation')
    assertions=[outer(row['formula']) for row in rows]
    # Explicit nonnegativity is essential to coefficient-wise enclosure.
    assertions += [a>=0 for a in z]
    metadata={**metadata,'box':[[str(v) for v in b] for b in box],
              'closed_strict_atoms':closed,'rows':len(rows),'enclosed_atoms':len(envelopes),
              'envelopes_sha256':hashlib.sha256(json.dumps(envelopes,sort_keys=True).encode()).hexdigest()}
    return z,assertions,metadata


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--box',required=True,help='JSON array of six rational endpoint pairs')
    ap.add_argument('--order',choices=('lt','gt'),required=True)
    ap.add_argument('--sign',type=int,choices=(-1,1),required=True)
    ap.add_argument('--tag',required=True)
    ap.add_argument('--closed',action='store_true')
    a=ap.parse_args()
    if not all(c.isalnum() or c=='_' for c in a.tag):raise ValueError('simple archive tag')
    stem='det5_compact_interval_'+a.tag
    out=ROOT/'results'/f'{stem}.json'
    if out.exists():raise SystemExit('Existing named query retained; no repeat')
    _,rows,metadata=compile_box(json.loads(a.box),a.order,a.sign,a.closed)
    text=statement(rows);path=ROOT/'results'/f'{stem}.smt2';path.write_text(text)
    from experiments.det5_y_corner_gauge_threshold import solve
    result,proof=solve(text)
    result.update(metadata,scope='Continuous compact-shape outer LRA in one order and determinant sign. UNSAT requires input audit and external proof replay before geometric exclusion.',
                  input_path=str(path.relative_to(ROOT)),input_sha256=hashlib.sha256(text.encode()).hexdigest(),solver_queries_run=1)
    if proof:
        raw=proof.encode() if isinstance(proof,str) else proof
        p=ROOT/'certificates'/f'{stem}.cpc.gz';p.write_bytes(gzip.compress(raw,mtime=0))
        result.update(proof_path=str(p.relative_to(ROOT)),proof_sha256=hashlib.sha256(raw).hexdigest())
    out.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:result[k] for k in ('status','elapsed_seconds','rows','enclosed_atoms')},indent=2))


if __name__=='__main__':main()
