"""Exact actual-body audit of six archived ordered-height SAT matrices.

Only the rational F values define the reconstructed bodies. Saved relaxed
heights, gap and product variables are never treated as actual geometry.
Uses stdlib arithmetic and bounded lattice-box enumeration, no solver calls.
"""
from fractions import Fraction as Q
from itertools import product
from math import ceil,floor
from pathlib import Path
import hashlib
import json
from replay_det5_full_gauge_retained_independent import inverse,multiply,dot,need
from replay_det5_conditional_width_bounds import parse,poly,VECTORS

ROOT=Path(__file__).resolve().parents[1]
P=((0,0,0),(5,1,2),(0,1,0),(0,0,1))
DIRECTIONS=sorted([(0,1,0),(0,0,1),(0,1,-1),(1,-2,-2),(1,-1,-2),
 (0,1,1),(0,2,-1),(1,-3,-2),(1,0,-2),(1,-3,-1),(1,-2,-3),
 (1,-1,-1),(1,0,-3),(1,-2,-1),(1,-1,-3)])


def digest(path):return hashlib.sha256((ROOT/path).read_bytes()).hexdigest()


def scalar(text):
    parsed=parse(text);need(len(parsed)==1,'one saved scalar')
    p=poly(parsed[0]);need(set(p)<={''},'exact rational value')
    return p.get('',Q(0))


def main():
    affine=inverse([[1]*4]+[[p[k] for p in P] for k in range(3)])
    records=[];sources={}
    for suffix in ('','_offset','_difference'):
        path='results/det5_y_ordered_root'+suffix+'.json'
        source=json.loads((ROOT/path).read_text());sources[path]=digest(path)
        need(source['extrema']==[0,3] and source['beta']=='37/102' and source['target']=='17/5','source metadata')
        need(len(source['queries'])==2,'two saved order branches')
        for row in source['queries']:
            need(row['status']=='sat' and digest(row['input_path'])==row['input_sha256'],'saved SAT input binding')
            values={k:scalar(v) for k,v in row['assignment'].items()}
            F=[[Q(0) if i==j else values[f'F_{i}_{j}'] for j in range(4)] for i in range(4)]
            need(all(F[i][j]>0 for i in range(4) for j in range(4) if i!=j),'relative facet interiors')
            need(all(sum(F[i][j] for i in range(4))==1 for j in range(4)),'stochastic columns')
            fi=inverse(F)
            vertices=[[sum(Q(P[i][k])*fi[i][j] for i in range(4)) for k in range(3)] for j in range(4)]
            for j in range(4):
                need([sum(F[i][j]*vertices[i][k] for i in range(4)) for k in range(3)]==list(P[j]),'exact contact reconstruction')
            def coords(v,affine_point=False):
                return multiply(F,multiply(affine,[Q(int(affine_point)),*v]))
            bbox=[[ceil(min(v[k] for v in vertices)),floor(max(v[k] for v in vertices))] for k in range(3)]
            interior=[];boundary=[];count=0
            for z in product(*(range(lo,hi+1) for lo,hi in bbox)):
                c=coords(z,True);count+=1
                if min(c)>0:interior.append(list(z))
                elif min(c)==0:boundary.append(list(z))
            widths=[{'direction':list(u),'width':str(max(dot(u,v) for v in vertices)-min(dot(u,v) for v in vertices))} for u in DIRECTIONS]
            minimum=min(Q(r['width']) for r in widths)
            yh=[v[1] for v in vertices];wy=max(yh)-min(yh);q=[(x-min(yh))/wy for x in yh]
            mins=[i for i,x in enumerate(q) if x==0];maxs=[i for i,x in enumerate(q) if x==1]
            ext=[mins[0],maxs[0]] if len(mins)==len(maxs)==1 else None
            gauges=[{'direction':list(u),'gauge':str(sum(map(abs,coords(u)))/2)} for u in sorted(VECTORS)]
            passes=all(Q(r['gauge'])>Q(37,102) for r in gauges)
            savedq=[Q(0),values['q_1'],values['q_2'],Q(1)]
            record={'source_path':path,'source_order':row['order'],'input_path':row['input_path'],'input_sha256':row['input_sha256'],
                'F':[[str(x) for x in r] for r in F],'vertices':[[str(x) for x in r] for r in vertices],
                'relative_facet_contacts':True,'hollow':not interior,'integer_bbox':bbox,'lattice_points_checked':count,
                'interior_lattice_points':interior,'boundary_lattice_points':boundary,
                'actual_Y_minimizer_indices':mins,'actual_Y_maximizer_indices':maxs,'actual_Y_extrema':ext,
                'actual_Y_heights':list(map(str,yh)),'actual_normalized_Y':list(map(str,q)),
                'actual_Y_width':str(wy),'actual_Y_gap':str(1/wy),'actual_Z_width':next(r['width'] for r in widths if r['direction']==[0,0,1]),
                'actual_Y_width_exceeds_17_5':wy>Q(17,5),'actual_Y_chart_0_3':0 in mins and 3 in maxs,
                'saved_relaxed_normalized_Y':list(map(str,savedq)),'saved_relaxed_gap':str(values['gap']),
                'saved_Y_equals_actual':savedq==q,'saved_gap_equals_actual':values['gap']==1/wy,
                'ten_gauges':gauges,'all_ten_gauges_exceed_37_102':passes,'fifteen_direction_widths':widths,
                'minimum_of_fifteen_widths':str(minimum),'fifteen_minimizing_directions':[r['direction'] for r in widths if Q(r['width'])==minimum],
                'global_width_statement':'The minimum of the fifteen listed widths is an upper bound on full lattice width; no exhaustive dual-lattice minimization is claimed.',
                'qualifies_as_requested_Y_only_counterexample':not interior and 0 in mins and 3 in maxs and wy>Q(17,5) and passes}
            records.append(record)
    need(len(records)==6,'exactly six archived matrices')
    result={'status':'PASS','scope':'Independent exact reconstruction of six saved rational matrices; complete primal lattice-box hollowness checks, actual Y charts and ten gauges, and fifteen directional widths. No relaxed height/product values are promoted to geometry.',
            'source_sha256':sources,'bodies':records,'qualifying_counterexamples':sum(r['qualifies_as_requested_Y_only_counterexample'] for r in records),
            'solver_queries_run':0,'new_models_generated':0}
    out=ROOT/'results/det5_ordered_actual_matrices.json'
    if out.exists():need(json.loads(out.read_text())==result,'existing actual-body receipt unchanged')
    else:out.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps([{'source':r['source_path'],'order':r['source_order'],'hollow':r['hollow'],'Y_extrema':r['actual_Y_extrema'],
                      'Y_width':r['actual_Y_width'],'Z_width':r['actual_Z_width'],'minimum_of_fifteen':r['minimum_of_fifteen_widths'],
                      'ten_gauges_pass':r['all_ten_gauges_exceed_37_102'],'qualifies':r['qualifies_as_requested_Y_only_counterexample']} for r in records],indent=2))


if __name__=='__main__':main()
