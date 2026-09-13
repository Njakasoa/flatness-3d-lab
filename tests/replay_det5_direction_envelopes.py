"""Universal polynomial checks and local strictness of directional envelopes."""
from fractions import Fraction as Q
from itertools import combinations,product
from math import gcd
from pathlib import Path
import json

ROOT=Path(__file__).resolve().parents[1]

def add(*terms):
    out={}
    for p in terms:
        for m,v in p.items():out[m]=out.get(m,Q(0))+v
    return {m:v for m,v in out.items() if v}
def neg(p):return {m:-v for m,v in p.items()}
def sub(p,q):return add(p,neg(q))
def mul(*terms):
    out={():Q(1)}
    for p in terms:
        nxt={}
        for m,v in out.items():
            for n,w in p.items():
                t=tuple(sorted(m+n));nxt[t]=nxt.get(t,Q(0))+v*w
        out={m:v for m,v in nxt.items() if v}
    return out
def symbol(n):return {(n,):Q(1)}

def main():
    f,g,l,h,A,B,b,x=map(symbol,('f','g','l','h','A','B','b','x'))
    z=mul(f,g)
    slacks=[sub(z,add(mul(l,g),mul(A,f),neg(mul(l,A)))),
            sub(z,add(mul(h,g),mul(B,f),neg(mul(h,B)))),
            sub(add(mul(h,g),mul(A,f),neg(mul(h,A))),z),
            sub(add(mul(l,g),mul(B,f),neg(mul(l,B))),z)]
    factors=[mul(sub(f,l),sub(g,A)),mul(sub(h,f),sub(B,g)),
             mul(sub(h,f),sub(g,A)),mul(sub(f,l),sub(B,g))]
    assert slacks==factors
    g=mul(b,x);tau=mul(b,f);z=mul(b,f,x)
    pslacks=[sub(z,add(mul(l,g),mul(A,tau),neg(mul(l,A,b)))),
             sub(z,add(mul(h,g),mul(B,tau),neg(mul(h,B,b)))),
             sub(add(mul(h,g),mul(A,tau),neg(mul(h,A,b))),z),
             sub(add(mul(l,g),mul(B,tau),neg(mul(l,B,b))),z)]
    pfactors=[mul(b,sub(f,l),sub(x,A)),mul(b,sub(h,f),sub(B,x)),
              mul(b,sub(h,f),sub(x,A)),mul(b,sub(f,l),sub(B,x))]
    assert pslacks==pfactors
    beta=Q(183,500);R=Q(6,5)/beta**3;target=Q(17,5);alpha=R/target
    fv=Q(1,2);T=(Q(5,4),Q(3,4),Q(0));W=(5*alpha/2,Q(3,8),-alpha)
    def allowed(f,t,lo,hi):return max(lo*f,t+hi*f-hi),min(t+lo*f-lo,hi*f)
    for t,w,(lo,hi) in zip(T,W,[(-5*alpha,5*alpha),(Q(3,4),Q(1)),(-2*alpha,2*alpha)]):
        low,high=allowed(fv,t,lo,hi);assert low<=w<=high
    U=(1,-1,-2);gval=sum(u*t for u,t in zip(U,T));zval=sum(u*w for u,w in zip(U,W))
    low,high=allowed(fv,gval,-2*alpha,2*alpha)
    assert gval==Q(1,2) and zval>high
    P=((0,0,0),(5,1,2),(0,1,0),(0,0,1));directions=[]
    for u in product(range(-2,3),range(-3,4),range(-3,4)):
        if not any(u) or next(t for t in u if t)<0 or gcd(*u)!=1:continue
        heights=[sum(x*y for x,y in zip(u,p)) for p in P];width=max(heights)-min(heights)
        if width<=3:directions.append({'direction':list(u),'contact_width':width})
    assert len(directions)==15
    assert next(v['contact_width'] for v in directions if v['direction']==list(U))==2
    result={'status':'PASS','universal_polynomial_identities_checked':8,'solver_queries_run':0,
            'scope':'Algebraic validity of static/perspective envelopes and strictness of a local coordinate-product relaxation. No full-model feasibility or geometric body is claimed.',
            'complete_direction_contact_widths':directions,
            'local_example':{'f':str(fv),'T':list(map(str,T)),'W':list(map(str,W)),
                             'all_coordinate_envelopes_pass':True,'direction':list(U),'directional_value':str(zval),
                             'directional_upper_envelope':str(high),'positive_violation':str(zval-high)}}
    (ROOT/'results/det5_direction_envelope_validation.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
if __name__=='__main__':main()
