"""Exact negative-determinant horizontal-gauge formula replay; no solver calls."""
from fractions import Fraction as Q
from hashlib import sha256
from itertools import product
import json
from pathlib import Path
import sympy as s

ROOT=Path(__file__).resolve().parents[1]
NOTE='proofs/DET5_NEGATIVE_DETERMINANT_GAUGE_NORMAL_FORM.md'
OUT='results/det5_negative_determinant_gauges_validation.json'


def gamma(v):return sum(max(z,0) for z in v)


def main():
    x,y,C,E,a,tau,k,u,r=s.symbols('x y C E a tau k u r',real=True)
    p=x/y;q=(1-y)/(1-x)
    A=C+p*E;B=q*C+E;alpha=(1-p)*E;omega=(1-q)*C
    Z=s.Matrix([alpha,-B,A,-omega]);W=s.Matrix([-(1-y),0,1,-y])
    V=s.Matrix([(1-x)*u-(1-y)*r,-u,r,x*u-y*r])
    sub={u:a*B/k,r:a*A/k+tau}
    identities=list(V.subs(sub)-a*Z/k-tau*W)
    identities += [(r*B-u*A).subs(sub)-tau*B,omega-y*A+x*B,
                   A+alpha-C-E,B+omega-C-E,sum(W)]
    contacts=s.Matrix([[1,1,1,1],[0,5,0,0],[0,1,1,0],[0,2,0,1]])
    vectors=[((1,0,0),1,-2),((2,0,1),2,1),((1,0,1),1,3),((3,0,1),3,-1)]
    for physical,n,m in vectors:
        actual=5*contacts.inv()*s.Matrix([0,*physical])
        identities += list(actual-s.Matrix([-m,n,-n,m]))
        identities += list(s.Matrix([actual[0],actual[2],actual[1],actual[3]])-s.Matrix([-m,-n,n,m]))
    assert all(s.cancel(expr)==0 for expr in identities)
    generic=table=target_checks=0
    target=Q(183,100)
    for xx,yy in ((Q(0),Q(1,4)),(Q(0),Q(1)),(Q(1,4),Q(1,2)),(Q(1,4),Q(1)),(Q(2,3),Q(3,4))):
      for cc,ee in ((Q(1,10),Q(1,5)),(Q(1,3),Q(1,3)),(Q(3,5),Q(1,4))):
        pp=xx/yy;qq=(1-yy)/(1-xx)
        AA=cc+pp*ee;BB=qq*cc+ee;SS=cc+ee;al=(1-pp)*ee;om=(1-qq)*cc
        ZZ=(al,-BB,AA,-om);WW=(-(1-yy),0,Q(1),-yy)
        def P(c,t):return max(c*SS+yy*t,c*AA+t)
        def N(j,t):return max(j*BB,t-j*(AA-BB),j*SS-yy*t)
        for coeff in (Q(0),Q(1,4),Q(1),Q(3)):
          # Explicit transition surfaces and values outside either side.
          ts={Q(0),Q(1,9),Q(1),coeff*AA,coeff*om/yy}
          for tt in ts:
            assert gamma(tuple(coeff*z+tt*w for z,w in zip(ZZ,WW)))==P(coeff,tt)
            assert gamma(tuple(-coeff*z+tt*w for z,w in zip(ZZ,WW)))==N(coeff,tt)
            generic+=2
        for aa,tt in product((Q(1,5),Q(1,2),Q(1)),(Q(1,100),Q(1,7),Q(1,2))):
          for kk,sign in ((3,1),(2,-1)):
            uu=aa*BB/kk;rr=aa*AA/kk+tt
            VV=((1-xx)*uu-(1-yy)*rr,-uu,rr,xx*uu-yy*rr)
            assert uu*AA-rr*BB==-tt*BB
            expected=([N(2-aa/3,tt),P(1+2*aa/3,2*tt),P(3+aa/3,tt),N(1-aa,3*tt)] if kk==3
                     else [P(2+aa/2,tt),N(1-aa,2*tt),N(3-aa/2,tt),P(1+3*aa/2,3*tt)])
            for (_,n,m),value in zip(vectors,expected):
              image=tuple(sign*n*v+m*z for v,z in zip(VV,ZZ))
              assert gamma(image)==value
              table+=1
            selected=expected[3] if kk==3 else expected[1]
            middle=(3 if kk==3 else 2)*tt-(1-aa)*(AA-BB)
            assert (selected>target)==(middle>target)
            assert (1-aa)*BB<1 and (1-aa)*SS-yy*(3 if kk==3 else 2)*tt<1
            if kk==3 and rr<1 and expected[0]>target:
                assert SS>Q(183,200) or 1+2*(BB-AA)-aa*BB/3>target
                assert SS>Q(183,200) or BB-AA>Q(83,200)
            target_checks+=1
    # Nonvacuous examples for both branches of the necessary base-shape OR.
    for AA,BB,SS,yy,aa,tt,which in (
        (Q(1,100),Q(161,200),Q(81,100),Q(1,2),Q(1,10),Q(9,10),'asymmetry'),
        (Q(49,100),Q(49,100),Q(49,50),Q(1),Q(1,10),Q(1,20),'high_S')):
        jj=2-aa/3
        gauge5=max(jj*BB,tt-jj*(AA-BB),jj*SS-yy*tt)
        assert aa*AA/3+tt<1 and gauge5>target
        assert (BB-AA>Q(83,200) if which=='asymmetry' else SS>Q(183,200))
        target_checks+=1
    # Strict-threshold equality does not satisfy the collapsed atom.
    for kk,AA,BB,SS,yy in ((3,Q(1,10),Q(1,10),Q(1,5),Q(1)),(2,Q(1,10),Q(1,10),Q(1,5),Q(1))):
        aa=Q(1);tt=target/kk;jj=1-aa
        val=max(jj*BB,kk*tt-jj*(AA-BB),jj*SS-yy*kk*tt)
        assert aa*AA/kk+tt<1 and val==target and not val>target
        target_checks+=1
    delta=Q(34728093,250000000)
    assert 0<delta<1
    result={'status':'PASS','proof_note':{'path':NOTE,'sha256':sha256((ROOT/NOTE).read_bytes()).hexdigest()},
            'formal_rational_identities':len(identities),'generic_max_formula_checks':generic,
            'physical_gauge_table_checks':table,'target_corollary_checks':target_checks,'orders':2,'physical_directions':4,
            'pieces_per_order':[3,2,2,3],'reverse_pieces':[2,3,3,2],
            'deltaD':str(delta),'solver_queries_run':0,
            'scope':'Exact symbolic identities and rational formula checks. Universal sign argument appears in the note; no continuous coverage or global exclusion.'}
    (ROOT/OUT).write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


if __name__=='__main__':main()
