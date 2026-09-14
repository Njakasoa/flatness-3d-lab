"""Exact continuous four-base box excluded by the projected forward H2 bound.

This is monotonic endpoint arithmetic for explicit polynomial necessities,
not a point sample or a solver label. Other shape and fiber variables are free.
"""
from fractions import Fraction as Q
from pathlib import Path
import hashlib,json
ROOT=Path(__file__).resolve().parents[1]
BOX=[['0','1/32'],['31/64','33/64'],['3/64','5/64'],['31/64','33/64']]


def build():
    (pl,ph),(ql,qh),(cl,ch),(el,eh)=[tuple(map(Q,b))for b in BOX]
    # f=1-q+LE/2+2(B-A): decreases in p,q,C and increases in E.
    # df/dq=-1+2C-pE/2<0; df/dE=5/2-2p-pq/2>0.
    derivative_q_upper=-1+2*ch
    derivative_e_lower=Q(5,2)-2*ph-ph*qh/2
    assert derivative_q_upper<0 and derivative_e_lower>0 and qh<1
    upper=1-ql+(1-pl*ql)*eh/2+2*((ql-1)*cl+(1-pl)*eh)
    assert upper==Q(3597,2048)<Q(183,100)
    B_upper=qh*ch+eh
    difference_lower=(ql-1)*ch+(1-ph)*el
    L_lower=1-ph*qh
    LE_lower=L_lower*el
    assert B_upper<Q(183,200)
    assert difference_lower==Q(1757,4096)>Q(83,200)
    assert LE_lower>Q(183,250)*qh
    assert L_lower>Q(49,1500) and cl+el>Q(183,500) and ch+eh<1
    assert el>Q(34728093,250000000)
    # Exact forward height bounds by monotonicity; x increases in p and
    # decreases in q, while y increases in p and decreases in q.
    xmin=pl*(1-qh)/(1-pl*qh);xmax=ph*(1-ql)/(1-ph*ql)
    ymin=(1-qh)/(1-pl*qh);ymax=(1-ql)/(1-ph*ql)
    assert 0<=xmin<=xmax<Q(1,4) and Q(1,4)<ymin<=ymax<Q(3,4)
    assert ymin>Q(33,256)
    volume=(ph-pl)*(qh-ql)*(ch-cl)*(eh-el)
    assert volume==Q(1,1048576)
    return {'status':'PASS','order':'lt','target_global_width':'17/5','base_parameters':['p','q','C','E'],'closed_box':BOX,
            'parameter_volume':str(volume),'projected_H2_expression':'1-q+(1-p*q)*E/2+2*((q*C+E)-(C+p*E))',
            'projected_H2_upper':str(upper),'required_strict_lower':'183/100','strict_gap':str(Q(183,100)-upper),
            'B_upper':str(B_upper),'B_minus_A_lower':str(difference_lower),'L_lower':str(L_lower),'LE_lower':str(LE_lower),
            'q_LE_comparison_upper':str(Q(183,250)*qh),'derivative_q_upper':str(derivative_q_upper),'derivative_E_lower':str(derivative_e_lower),
            'actual_forward_height_intervals':[[str(xmin),str(xmax)],[str(ymin),str(ymax)]],
            'all_previous_forward_base_cuts_hold_throughout_box':True,'new_base_obstruction_beyond_previous_height_rectangles':True,
            'solver_queries_run':0,'scope':'Analytic four-base closed box exclusion in originalY03 forwardorder. All admissible a,tau,t,h are excluded at the target. No whole class, reverse-order or global flatness exclusion; parameter volume is not residual-body measure.'}


def main():
    out=ROOT/'results/det5_projected_base_box.json';result=build()
    out.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))


if __name__=='__main__':main()
