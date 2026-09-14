"""Exact algebra and constructive interval replay for one-gauge projection."""
from fractions import Fraction as Q
from hashlib import sha256
from itertools import product
import json
from pathlib import Path
import sympy as s

ROOT=Path(__file__).resolve().parents[1]
NOTE='proofs/DET5_FORWARD_MIDDLE_GAUGE_EXACT_PROJECTION.md'
OUT='results/det5_forward_middle_projection_validation.json'
T=Q(183,100)


def check(base):
    p,q,C,E=base;L=1-p*q;y=(1-q)/L;x=p*y
    A=C+p*E;B=q*C+E;alpha=(1-p)*E;Delta=B-A;d=y-x;w=1-y
    assert 0<=p<1 and 0<=q<1 and C>0 and E>0 and C+E<1
    cuts=(1+2*Delta-T,L*E+2*q*Delta-Q(6,5)*T*q,1-q+L*E/2+2*Delta-T)
    positive=all(c>0 for c in cuts)
    a_high=3*(1+2*Delta-T)/B
    if w:
        a_low=3*(w*(T-2*Delta)-alpha/2)/(d*B)
        left=max(Q(0),a_low);right=min(Q(1),a_high)
        feasible=left<right
    else:
        assert q==0 and y==1 and cuts[1]>0
        left=Q(0);right=min(Q(1),a_high);feasible=left<right
    assert feasible==positive
    witness=None
    if feasible:
        a=(left+right)/2
        lo=max(Q(0),T-(2-a/3)*Delta)
        hi=1-a*A/3
        if w:hi=min(hi,alpha*(a/3+Q(1,2))/w)
        assert lo<hi
        tau=(lo+hi)/2
        assert 0<a<1 and tau>0 and tau<1-a*A/3
        assert alpha*(a/3+Q(1,2))-w*tau>0
        assert tau+(2-a/3)*Delta>T
        witness={'base':list(map(str,base)),'a':str(a),'tau':str(tau),'base_cut_margins':list(map(str,cuts))}
    return positive,w==0,witness,cuts


def main():
    p,q,C,E,a=s.symbols('p q C E a',real=True)
    L=1-p*q;y=(1-q)/L;x=p*y;A=C+p*E;B=q*C+E
    alpha=(1-p)*E;Delta=B-A;d=y-x;w=1-y;target=s.Rational(183,100)
    low=3*(w*(target-2*Delta)-alpha/2)/(d*B)
    high=3*(1+2*Delta-target)/B
    cut2=L*E+2*q*Delta-s.Rational(6,5)*target*q
    cut3=1-q+L*E/2+2*Delta-target
    identities=[alpha-w*Delta-d*B,
                (1-a*A/3)+(2-a/3)*Delta-(1+2*Delta-a*B/3),
                alpha*(a/3+s.Rational(1,2))/w+(2-a/3)*Delta-(2*Delta+alpha/(2*w)+a*d*B/(3*w)),
                (1-low)*d*B/3-s.Rational(5,6)*(1-x)*cut2,
                (high-low)*d*B/3-(1-x)*cut3,
                alpha/(1-x)-L*E,d/(1-x)-(1-q)]
    assert all(s.cancel(v)==0 for v in identities)
    counts={'fixtures':0,'feasible':0,'infeasible':0,'q_zero':0}
    witnesses=[]
    for pp,qq,cc,ee in product((Q(0),Q(1,5),Q(1,2),Q(4,5)),(Q(0),Q(1,10),Q(1,3),Q(2,3),Q(9,10)),
                               (Q(1,100),Q(1,10),Q(1,3),Q(3,5)),(Q(1,10),Q(1,3),Q(3,5),Q(4,5))):
        if cc+ee>=1:continue
        ok,endpoint,witness,_=check((pp,qq,cc,ee))
        counts['fixtures']+=1;counts['feasible' if ok else 'infeasible']+=1;counts['q_zero']+=endpoint
        if witness and (len(witnesses)<5 or endpoint and not any(w['base'][1]=='0' for w in witnesses)):witnesses.append(witness)
    # Exact equality at each individual polynomial boundary, in the actual base domain.
    boundaries=[('I',(Q(0),Q(0),Q(1,10),Q(103,200))),
                ('II',(Q(0),Q(1,2),Q(1,10),Q(287,500))),
                ('III',(Q(0),Q(2,5),Q(1,10),Q(27,50)))]
    equality=[]
    for name,base in boundaries:
        ok,endpoint,witness,cuts=check(base)
        index={'I':0,'II':1,'III':2}[name]
        assert cuts[index]==0 and not ok and witness is None
        assert all(v>0 for i,v in enumerate(cuts) if i!=index)
        equality.append({'condition':name,'base':list(map(str,base)),'margins':list(map(str,cuts))})
    result={'status':'PASS','proof_note':{'path':NOTE,'sha256':sha256((ROOT/NOTE).read_bytes()).hexdigest()},
            'formal_rational_identities':len(identities),'exact_interval_fixture_counts':counts,
            'constructive_subsystem_witnesses':witnesses,'strict_equality_cases':equality,
            'base_conditions':['1+2*(B-A)>183/100','L*E+2*q*(B-A)>549*q/250','1-q+L*E/2+2*(B-A)>183/100'],
            'solver_queries_run':0,
            'scope':'Exact IFF for the specified single-middle-gauge subsystem only. No full four-gauge, geometry, width or volume sufficiency.'}
    (ROOT/OUT).write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='constructive_subsystem_witnesses'},indent=2))


if __name__=='__main__':main()
