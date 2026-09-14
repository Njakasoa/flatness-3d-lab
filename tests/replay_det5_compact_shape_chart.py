"""Independent compact shape chart replay; no solver calls."""
from fractions import Fraction as Q
from pathlib import Path
import json
import sympy as s

ROOT = Path(__file__).resolve().parents[1]


def main():
    p,q,C,E,r,u,t,h = s.symbols('p q C E r u t h')
    L=1-p*q
    y=(1-q)/L
    x=p*y
    d=y-x
    c=C/(1-x)
    e=E/y
    F=s.Matrix([[0,1-h-(1-y)*r,1-h-(1-x)*u,(1-p)*E],
                [1-t+q*C,0,u,1-t-E],
                [t-C,r,0,t+p*E],
                [(1-q)*C,h-y*r,h-x*u,0]])
    old=s.Matrix([[0,1-h-(1-y)*r,1-h-(1-x)*u,d*e],
                  [1-t+(1-y)*c,0,u,1-t-y*e],
                  [t-(1-x)*c,r,0,t+x*e],
                  [d*c,h-y*r,h-x*u,0]])
    equations=[x/y-p,(1-y)/(1-x)-q,
               (1-x)-(1-p)/L,(1-y)-q*(1-p)/L,
               d-(1-p)*(1-q)/L,d/(1-x)-(1-q),
               (1-p)/(1-x)-L]
    equations+=list(F-old)
    equations+=list(F.T*s.Matrix([0,x,y,1])-s.Matrix([x+d*t,h,h,x+d*t]))
    equations+=[sum(F[i,j] for i in range(4))-1 for j in range(4)]
    z=F[:,3]-F[:,0]
    equations+=list(z-s.Matrix([(1-p)*E,-q*C-E,C+p*E,-(1-q)*C]))
    A=(1-x)*(u-r)+d*r
    B=x*(u-r)-d*r
    equations+=[F[0,1]-F[0,2]-A,F[3,1]-F[3,2]-B,A+B-u+r,
                F[0,2]-F[0,1]-(1-x)*(r-u)+d*r]
    equations+=[F.det()-(h-x-d*t)*(u*(C+p*E)-r*(q*C+E))]
    for eq in equations:
        assert s.cancel(eq)==0
    X,Y=s.symbols('X Y')
    pp=X/Y
    qq=(1-Y)/(1-X)
    for eq in [(1-qq)/(1-pp*qq)-Y,pp*(1-qq)/(1-pp*qq)-X]:
        assert s.cancel(eq)==0
    count=guards=branch_R0=bound_checks=gt_bound_checks=0
    pos=lambda v:max(v,Q(0))
    # Include both tied-extremum edges and shapes close to the collapsed corner.
    grid=[Q(0),Q(1,4),Q(2,3),Q(9,10),Q(99,100)]
    for pp in grid:
      for qq in grid:
        LL=1-pp*qq
        yy=(1-qq)/LL
        xx=pp*yy
        dd=yy-xx
        assert 0<=xx<yy<=1 and xx/yy==pp and (1-yy)/(1-xx)==qq
        assert 0<dd<=LL and 1-pp<=LL and 1-qq<=LL
        for CC,EE in [(Q(1,5),Q(1,4)),(Q(2,5),Q(2,5))]:
          tt=(CC+1-EE)/2
          aa=xx+dd*tt
          for hh in [(1+aa)/2,(3*aa+1)/4,(99*aa+1)/100]:
            capr=min(hh/yy,(1-hh)/(1-yy) if yy<1 else Q(2))
            capu=min(hh/xx if xx>0 else Q(2),(1-hh)/(1-xx))
            for rr in [capr/8,capr/3,3*capr/4,99*capr/100]:
              for uu in [capu/8,capu/3,3*capu/4,99*capu/100]:
                ff=[[Q(0),1-hh-(1-yy)*rr,1-hh-(1-xx)*uu,(1-pp)*EE],
                    [1-tt+qq*CC,Q(0),uu,1-tt-EE],
                    [tt-CC,rr,Q(0),tt+pp*EE],
                    [(1-qq)*CC,hh-yy*rr,hh-xx*uu,Q(0)]]
                assert all(ff[i][j]>0 for i in range(4) for j in range(4) if i!=j)
                assert 0<rr<1 and 0<uu<1
                bb=hh-aa
                assert ff[3][1]>bb-dd and ff[3][2]>bb-dd
                assert ff[3][2]>ff[3][0]
                AA=ff[0][1]-ff[0][2]
                BB=ff[3][1]-ff[3][2]
                assert pos(AA)+pos(BB)<=pos(uu-rr)+dd*rr
                zz=[ff[i][3]-ff[i][0] for i in range(4)]
                im=[(2*(ff[i][1]-ff[i][2])+zz[i])/5 for i in range(4)]
                gg=sum(abs(v) for v in im)/2
                assert gg<=(CC+EE+2*max(rr,uu)+2*dd*rr)/5
                R3=(1-qq)*CC>=2*ff[3][1]+3*ff[3][2]
                R0=(1-pp)*EE>=3*ff[0][1]+2*ff[0][2]
                g2=uu<=(qq*CC+EE)/3 or R3
                g3=rr<=(CC+pp*EE)/3 or R0
                exact2=any(-ff[i][0]+2*ff[i][1]+3*ff[i][2]+ff[i][3]<=0 for i in range(4))
                exact3=any(ff[i][0]+3*ff[i][1]+2*ff[i][2]-ff[i][3]<=0 for i in range(4))
                assert (g2,g3)==(exact2,exact3)
                guards+=2
                assert not R3
                if R0:
                    branch_R0+=1
                    assert rr-uu<(1-qq)*rr+LL*EE/2<3*LL/2
                if g2 and g3 and not R3:
                    bound_checks+=1
                    assert gg<Q(1,3)+LL
                R3gt=(1-qq)*CC>=3*ff[3][1]+2*ff[3][2]
                R0gt=(1-pp)*EE>=2*ff[0][1]+3*ff[0][2]
                assert not R3gt
                g2gt=uu<=(qq*CC+EE)/2 or R3gt
                g3gt=rr<=(CC+pp*EE)/2 or R0gt
                exact2gt=any(-ff[i][0]+3*ff[i][1]+2*ff[i][2]+ff[i][3]<=0 for i in range(4))
                exact3gt=any(ff[i][0]+2*ff[i][1]+3*ff[i][2]-ff[i][3]<=0 for i in range(4))
                assert (g2gt,g3gt)==(exact2gt,exact3gt)
                guards+=2
                if R0gt:
                    assert rr-uu<(1-qq)*rr+LL*EE/3<4*LL/3
                if g2gt and g3gt:
                    gt_bound_checks+=1
                    assert uu<=(CC+EE)/2
                    imgt=[(-2*(ff[i][1]-ff[i][2])+zz[i])/5 for i in range(4)]
                    ggt=sum(abs(v) for v in imgt)/2
                    assert 2*pos(rr-uu)+pos(CC+pp*EE-2*rr)<=max(2*rr,CC+pp*EE)
                    assert ggt<Q(1,5)+Q(17,15)*LL
                count+=1
    beta=Q(183,500)
    assert beta-Q(1,3)==Q(49,1500)
    assert Q(37,102)-Q(1,3)==Q(1,34)
    assert 15*(beta-Q(1,5))/17==Q(249,1700)>Q(49,1500)
    result={'status':'PASS','formal_rational_identities':len(equations)+2,
            'exact_matrix_fixtures':count,'guard_equivalence_checks':guards,
            'R0_fixtures':branch_R0,'R3_impossibility_fixtures':count,
            'combined_gauge_bound_fixtures':bound_checks,
            'reverse_order_gauge_bound_fixtures':gt_bound_checks,
            'uniform_denominator_lower_bound':'49/1500',
            'reverse_order_stronger_lower_bound':'249/1700',
            'hypotheses':'Both Y[0,3] height orders, exact chart, original two observer guards, gamma(2,0,1)>183/500. Global width >17/5 for hollow bodies implies these conditions.',
            'solver_queries_run':0,
            'limitation':'No global shape coverage or determinant-five exclusion.'}
    assert branch_R0 and bound_checks and gt_bound_checks
    out=ROOT/'results/det5_compact_shape_chart_validation.json'
    out.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))

if __name__=='__main__':
    main()
