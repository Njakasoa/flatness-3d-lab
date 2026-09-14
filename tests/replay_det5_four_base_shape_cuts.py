"""Symbolic and exact fixture replay of four-base-shape cuts; no solver calls."""
from fractions import Fraction as Q
from hashlib import sha256
from itertools import product
import json
from pathlib import Path
import sympy as s

ROOT=Path(__file__).resolve().parents[1]
NOTE='proofs/DET5_FOUR_BASE_SHAPE_CUTS.md'
OUT='results/det5_four_base_shape_cuts_validation.json'


def numeric(x,y,C,E,a,tau,k):
    p=x/y;q=(1-y)/(1-x);L=1-p*q
    A=C+p*E;B=q*C+E;S=C+E;alpha=S-A
    slack=alpha*(a/k+Q(1,5-k))-(1-y)*tau
    P=lambda c,t:max(c*S+y*t,c*A+t)
    N=lambda j,t:max(j*B,t-j*(A-B),j*S-y*t)
    vals=([N(2-a/3,tau),P(1+2*a/3,2*tau),P(3+a/3,tau),N(1-a,3*tau)] if k==3 else
          [P(2+a/2,tau),N(1-a,2*tau),N(3-a/2,tau),P(1+3*a/2,3*tau)])
    return A,B,S,alpha,L,q,slack,vals


def main():
    x,y,C,E,a,tau,k=s.symbols('x y C E a tau k',real=True)
    p=x/y;q=(1-y)/(1-x);L=1-p*q
    A=C+p*E;B=q*C+E;S=C+E;alpha=S-A;d=y-x
    slack=alpha*(a/k+1/(5-k))-(1-y)*tau
    M=k*tau-(1-a)*(A-B)
    j=2-a/3;c=1+2*a/3;H3=j*S-y*tau
    G1=c*S+2*y*tau;G2=c*A+2*tau;J=(3+a/3)*S+y*tau
    ids=[alpha+(1-y)*(A-B)-d*B,
         (1-y)*M+k*slack-5*alpha/(5-k)+(1-a)*d*B,
         2*H3+G1-5*S,2*H3+G2-5*S+2*slack.subs(k,3),
         J-tau-s.Rational(5,2)*S-(a/3+s.Rational(1,2))*A-slack.subs(k,3),
         alpha-(1-p)*E,1-y-q*(1-p)/L,
         (2+B-A-a*B)-M.subs(k,2)-2*(1-a*A/2-tau)]
    assert all(s.cancel(v)==0 for v in ids)
    T=Q(183,100);checks=0;feasible=[0,0]
    for xx,yy in ((Q(0),Q(1,4)),(Q(0),Q(3,5)),(Q(0),Q(1)),(Q(1,4),Q(1,2)),(Q(1,4),Q(1)),(Q(2,3),Q(3,4))):
      for cc,ee in ((Q(1,100),Q(4,5)),(Q(1,100),Q(49,50)),(Q(1,3),Q(1,3)),(Q(3,5),Q(1,4))):
        for aa,tt,kk in product((Q(1,10),Q(1,2),Q(1)),(Q(1,10),Q(1,2),Q(9,10),Q(23,25)),(2,3)):
            AA,BB,SS,al,LL,qq,sl,vals=numeric(xx,yy,cc,ee,aa,tt,kk)
            if not tt<1-aa*AA/kk or sl<=0:continue
            full=all(v>T for v in vals)
            middle=kk*tt-(1-aa)*(AA-BB)
            if middle>T:
                assert LL*ee>(5-kk)*Q(183,500)*qq
                if kk==2:assert AA-BB<Q(17,100)
            if kk==3:
                jj=2-aa/3;cv=1+2*aa/3
                H1=jj*BB;H2=tt+jj*(BB-AA);HH3=jj*SS-yy*tt
                GG1=cv*SS+2*yy*tt;GG2=cv*AA+2*tt
                reduced=(H1>T or H2>T) and (GG1>T or GG2>T) and middle>T
                assert full==reduced
                assert not (HH3>T and (GG1>T or GG2>T))
                if full:assert BB>Q(183,200) or BB-AA>Q(83,200)
            if full:feasible[kk-2]+=1
            checks+=1
    # Exact surviving asymmetric full chart fixture, independent matrix entries.
    xx=Q(0);yy=Q(3,5);cc=Q(1,100);ee=Q(4,5);aa=Q(1,10);tt=Q(23,25)
    AA,BB,SS,al,LL,qq,sl,vals=numeric(xx,yy,cc,ee,aa,tt,3)
    uu=aa*BB/3;rr=aa*AA/3+tt;t=Q(1,10);h=Q(31,50);pp=xx/yy;d=yy-xx
    cols=[(0,1-t+qq*cc,t-cc,(1-qq)*cc),
          (1-h-(1-yy)*rr,0,rr,h-yy*rr),
          (1-h-(1-xx)*uu,uu,0,h-xx*uu),
          ((1-pp)*ee,1-t-ee,t+pp*ee,0)]
    F=[[Q(cols[j][i]) for j in range(4)] for i in range(4)]
    assert all(F[i][j]>0 for i in range(4) for j in range(4) if i!=j)
    assert all(sum(col)==1 for col in cols)
    assert cc<t<1-ee and h>xx+d*t and 3*uu<=BB
    assert F[0][3]>=3*F[0][1]+2*F[0][2]
    assert BB<Q(183,200) and BB-AA>Q(83,200) and all(v>T for v in vals)
    assert h-xx-d*t==Q(14,25)
    Z=(al,-BB,AA,-(1-qq)*cc)
    V=((1-xx)*uu-(1-yy)*rr,-uu,rr,xx*uu-yy*rr)
    direct=[]
    for n,m in ((1,-2),(2,1),(1,3),(3,-1)):
        image=[n*v+m*z for v,z in zip(V,Z)]
        assert sum(image)==0
        direct.append(sum(max(v,0) for v in image))
    assert direct==vals
    result={'status':'PASS','proof_note':{'path':NOTE,'sha256':sha256((ROOT/NOTE).read_bytes()).hexdigest()},
            'formal_rational_identities':len(ids),'exact_domain_implication_checks':checks,
            'four_gauge_satisfying_sample_counts':{'gt':feasible[0],'lt':feasible[1]},
            'forward_piece_selections_before':12,'forward_piece_selections_after':4,
            'reverse_piece_selections_retained':12,
            'forward_base_cut':'B>183/200 OR B-A>83/200',
            'both_order_base_cuts':['L*E>183*q/250 (lt)','L*E>549*q/500 (gt)'],
            'reverse_extra_base_cut':'A-B<17/100',
            'asymmetric_surviving_fixture':{'x':str(xx),'y':str(yy),'C':str(cc),'E':str(ee),'a':str(aa),'tau':str(tt),'t':str(t),'h':str(h),
                'A':str(AA),'B':str(BB),'S':str(SS),'u':str(uu),'r':str(rr),'F':[[str(v) for v in row] for row in F],
                'five_times_gauges':list(map(str,vals)),'actual_Y_gap':'14/25','actual_Y_width':'25/14',
                'scope':'Exact strict chart and four selected horizontal gauges with forced observer; not a large-width witness or hollowness assertion.'},
            'solver_queries_run':0,'scope':'Universal analytical branch/cut derivations with exact formula replay; no global exclusion or sampled coverage claim.'}
    (ROOT/OUT).write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='asymmetric_surviving_fixture'},indent=2))


if __name__=='__main__':main()
