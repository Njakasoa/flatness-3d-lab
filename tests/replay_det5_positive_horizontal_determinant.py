"""Symbolic and rational replay of the determinant-sign gauge bound; no solver."""
from fractions import Fraction as Q
from hashlib import sha256
from itertools import product
import json
from pathlib import Path
import sympy as s

ROOT=Path(__file__).resolve().parents[1]
NOTE='proofs/DET5_POSITIVE_HORIZONTAL_DETERMINANT.md'
OUT='results/det5_positive_horizontal_determinant_validation.json'


def gamma(v):return sum(max(z,0) for z in v)


def main():
    x,y,C,E,u,r,k=s.symbols('x y C E u r k', real=True)
    p=x/y;q=(1-y)/(1-x)
    A=C+p*E;B=q*C+E;alpha=(1-p)*E;omega=(1-q)*C
    V=s.Matrix([(1-x)*u-(1-y)*r,-u,r,x*u-y*r])
    Z=s.Matrix([alpha,-B,A,-omega])
    identities=[(1-x)*B-(1-y)*A-alpha,x*B-y*A+omega,
                sum(Z),sum(V),alpha+A-C-E]
    identities.extend(V.subs({u:B/k,r:A/k})-Z/k)
    weights=[1-k*u/B,k*(u/B-r/A),k*r/A]
    identities.extend([sum(weights)-1,(weights[1]+weights[2])*B/k-u,weights[2]*A/k-r])
    # Independent physical contact-coordinate images verify the original signs.
    P=s.Matrix([[1,1,1,1],[0,5,0,0],[0,1,1,0],[0,2,0,1]])
    ell=P.inv()*s.Matrix([0,2,0,1])
    identities.extend(ell-s.Matrix([-s.Rational(1,5),s.Rational(2,5),-s.Rational(2,5),s.Rational(1,5)]))
    swapped=s.Matrix([ell[0],ell[2],ell[1],ell[3]])
    identities.extend(swapped-s.Matrix([-s.Rational(1,5),-s.Rational(2,5),s.Rational(2,5),s.Rational(1,5)]))
    assert all(s.cancel(v)==0 for v in identities)
    count=0
    samples=[Q(0),Q(1,4),Q(1,2),Q(3,4),Q(1)]
    for xx,yy in ((Q(0),Q(1,4)),(Q(0),Q(1)),(Q(1,4),Q(1,2)),(Q(1,4),Q(1)),(Q(2,3),Q(3,4))):
        for cc,ee in ((Q(1,10),Q(1,5)),(Q(1,3),Q(1,3)),(Q(3,5),Q(1,4))):
            pp=xx/yy;qq=(1-yy)/(1-xx)
            aa=cc+pp*ee;bb=qq*cc+ee;al=(1-pp)*ee;om=(1-qq)*cc;ss=cc+ee
            zz=(al,-bb,aa,-om)
            assert gamma(zz)==ss
            for kk,sign in ((3,1),(2,-1)):
                for wU,wW in product(samples,repeat=2):
                    if wU+wW>1:continue
                    wO=1-wU-wW
                    uu=(wU+wW)*bb/kk;rr=wW*aa/kk
                    vv=((1-xx)*uu-(1-yy)*rr,-uu,rr,xx*uu-yy*rr)
                    image=tuple((z+sign*2*v)/5 for z,v in zip(zz,vv))
                    assert uu*aa-rr*bb>=0 and kk*uu<=bb
                    bound=ss/3 if kk==3 else ss/5
                    assert gamma(image)<=bound
                    assert [1-kk*uu/bb,kk*(uu/bb-rr/aa),kk*rr/aa]==[wO,wU,wW]
                    count+=1
    receipt={'status':'PASS','proof_note':{'path':NOTE,'sha256':sha256((ROOT/NOTE).read_bytes()).hexdigest()},
             'formal_rational_identities':len(identities),'exact_rational_ordered_triangle_fixtures':count,
             'forward_gauge_bound':'S/3','reverse_gauge_bound':'S/5','necessary_sign_at_beta_183_500':'D<0',
             'solver_queries_run':0,
             'scope':'Formula replay and exact fixture checks; the universal analytic proof is the convex outer-triangle argument in the note. No negative-branch exclusion or new global flatness bound.'}
    (ROOT/OUT).write_text(json.dumps(receipt,indent=2)+'\n')
    print(json.dumps(receipt,indent=2))


if __name__=='__main__':main()
