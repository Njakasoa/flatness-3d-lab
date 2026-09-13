"""Truncate observer lines using six necessary difference-body gauges.

The exact convex-combination bound is proved in DET2_OBSERVER_GAUGE_GUARDS.md.
At beta=37/102 there are 64 guards, 20 nontrivial for pair dominance.
No volume cutoff, floating arithmetic, or solver is used by this generator.
"""
import json
from fractions import Fraction as Q
from math import ceil, floor
from pathlib import Path
from experiments.det2_observer_lines import CONTACTS, build as line_build, cross, sub, pair_profile

ROOT=Path(__file__).resolve().parents[1]
BETA=Q(37,102)


def need(value,message):
    if not value:raise ValueError(message)


def build():
    lines=line_build()['lines'];records=[];points=set();edges=set()
    for L in lines:
        ids=L['contact_indices'];others=[i for i in range(4) if i not in ids]
        pa=CONTACTS[ids[0]];v=tuple(L['primitive_direction']);r=sub(L['base_point'],pa)
        w=sub(CONTACTS[others[1]],CONTACTS[others[0]])
        cr=cross(v,r);cw=cross(v,w);idx=next(i for i,x in enumerate(cr) if x)
        d=Q(cw[idx],cr[idx])
        if d<0:w=tuple(-x for x in w);d=-d
        k=next(k for k,x in enumerate(v) if x)
        a=(Q(w[k])-d*r[k])/v[k]
        need(d==2 and a.denominator==1,'opposite-edge plane coordinates')
        need(tuple(a*x+d*y for x,y in zip(v,r))==w,'opposite-edge identity')
        radius=(d+1)/(d*BETA)
        left=a/d+1-radius;right=a/d+radius
        lo,hi=floor(left)+1,ceil(right)-1
        linepoints=[]
        for t in range(lo,hi+1):
            rho=max(Q(1),abs(d*t-a)/(d+1),abs(d*(t-1)-a)/(d+1))
            need(rho<1/BETA,'strict gauge parameter cutoff')
            z=tuple(q+t*x for q,x in zip(L['base_point'],v))
            points.add(z);linepoints.append(z)
        need(len(linepoints)==7,'determinant-two line count')
        canonical=v if next(x for x in v if x)>0 else tuple(-x for x in v)
        edges.add(canonical)
        records.append({'base_point':L['base_point'],'primitive_direction':v,
                        'contact_indices':ids,'r':r,'opposite_edge_oriented':w,
                        'opposite_edge_basis_coefficients':[str(a),str(d)],
                        'open_parameter_interval':[str(left),str(right)],
                        'integer_parameter_interval':[lo,hi],'points':linepoints})
    rows=[{'point':z,**pair_profile(z)} for z in sorted(points)]
    nontrivial=[r['point'] for r in rows if not r['tautological']]
    need(len(points)==64 and len(nontrivial)==20,'guard count')
    need(len(edges)==6,'six primitive contact-edge directions')
    return {'status':'exact_gauge_truncated_observer_guards','beta':str(BETA),
            'hypotheses':['K compact full dimensional convex contains P','all four contacts lie on boundary of K','gamma_(K-K)(v)>beta for all six primitive contact-edge directions'],
            'volume_cutoff_required':False,'edge_directions':sorted(edges),
            'lines':records,'guard_count':len(points),'guards':rows,
            'pair_nontrivial_count':len(nontrivial),'pair_nontrivial_points':nontrivial,
            'pair_tautological_count':len(points)-len(nontrivial),
            'general_d_greater_than_one_maximum_guards':96,
            'scope':'Complete hollowness criterion under explicit edge-gauge and boundary-contact hypotheses, conditional on the five-point width-one theorem. Not a width bound.'}


def main():
    result=build()
    (ROOT/'certificates/det2_observer_gauge_guards.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:result[k] for k in ('status','guard_count','pair_nontrivial_count','pair_tautological_count','edge_directions')}))


if __name__=='__main__':main()
