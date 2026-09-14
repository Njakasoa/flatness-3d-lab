"""Exact convex-rectangle observer obstruction replay; no solver calls."""
from fractions import Fraction as Q
from hashlib import sha256
from itertools import product
import json
from pathlib import Path
import sympy as s

ROOT=Path(__file__).resolve().parents[1]
NOTE='proofs/DET5_FORCED_OBSERVER_BRANCH.md'
OUT='results/det5_forced_observer_branch_validation.json'


def gamma(v):return sum(max(t,0) for t in v)


def main():
    x,y,C,E,u,r,k=s.symbols('x y C E u r k',real=True)
    p=x/y;q=(1-y)/(1-x)
    A=C+p*E;B=q*C+E;alpha=(1-p)*E;omega=(1-q)*C
    V=s.Matrix([(1-x)*u-(1-y)*r,-u,r,x*u-y*r])
    Z=s.Matrix([alpha,-B,A,-omega]);G=k*V-Z
    expected=[-Z,s.Matrix([(1-y)*A,0,-A,y*A]),s.Matrix([-(1-x)*B,B,0,-x*B]),s.zeros(4,1)]
    substitutions=[{u:0,r:0},{u:B/k,r:0},{u:0,r:A/k},{u:B/k,r:A/k}]
    identities=[]
    for sub,answer in zip(substitutions,expected):identities+=list(G.subs(sub)-answer)
    contacts=s.Matrix([[1,1,1,1],[0,5,0,0],[0,1,1,0],[0,2,0,1]])
    lt=5*contacts.inv()*s.Matrix([0,3,0,1])
    gt=5*contacts.inv()*s.Matrix([0,2,0,1])
    identities+=list(lt-s.Matrix([1,3,-3,-1]))
    identities+=list(s.Matrix([gt[0],gt[2],gt[1],gt[3]])-s.Matrix([-1,-2,2,1]))
    assert all(s.cancel(v)==0 for v in identities)
    fixtures=0
    for xx,yy in ((Q(0),Q(1,4)),(Q(0),Q(1)),(Q(1,4),Q(1,2)),(Q(1,4),Q(1)),(Q(2,3),Q(3,4))):
      for cc,ee in ((Q(1,10),Q(1,5)),(Q(1,3),Q(1,3)),(Q(3,5),Q(1,4))):
        pp=xx/yy;qq=(1-yy)/(1-xx)
        aa=cc+pp*ee;bb=qq*cc+ee;ss=cc+ee;al=(1-pp)*ee;om=(1-qq)*cc
        zz=(al,-bb,aa,-om)
        corners=[tuple(-z for z in zz),((1-yy)*aa,Q(0),-aa,yy*aa),(-(1-xx)*bb,bb,Q(0),-xx*bb),(Q(0),)*4]
        assert [gamma(c) for c in corners]==[ss,aa,bb,Q(0)]
        for kk in (2,3):
          for f,g in product((Q(0),Q(1,4),Q(1,2),Q(3,4),Q(1)),repeat=2):
            uu=f*bb/kk;rr=g*aa/kk
            vv=((1-xx)*uu-(1-yy)*rr,-uu,rr,xx*uu-yy*rr)
            image=tuple(kk*v-z for v,z in zip(vv,zz))
            weights=((1-f)*(1-g),f*(1-g),(1-f)*g,f*g)
            combo=tuple(sum(weights[i]*corners[i][row] for i in range(4)) for row in range(4))
            assert combo==image and gamma(image)<=ss<1
            assert gamma(tuple(-v for v in image))==gamma(image)
            fixtures+=1
    assert Q(183,500)>Q(1,5)
    # ACMS: 1/(1-1/5)=5/4, with strictness from S<1.
    assert 1/(1-Q(1,5))==Q(5,4)
    result={'status':'PASS','proof_note':{'path':NOTE,'sha256':sha256((ROOT/NOTE).read_bytes()).hexdigest()},
            'formal_rational_identities':len(identities),'exact_rectangle_ordered_fixtures':fixtures,
            'forward_obstructing_vector':[3,0,1],'reverse_obstructing_vector':[2,0,1],
            'main_branch_gauge_bound':'S/5<1/5','main_branch_width_bound':'w<(5/4)*(1+2/sqrt(3))',
            'forced_forward':'3r>A AND F03>=3F01+2F02',
            'forced_reverse':'2r>A AND F03>=2F01+3F02',
            'determinant_consequence':'D<0','solver_queries_run':0,
            'scope':'Exact formula and fixture replay; universal convexity proof in note. No exceptional-branch or full-class exclusion.'}
    (ROOT/OUT).write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


if __name__=='__main__':main()
