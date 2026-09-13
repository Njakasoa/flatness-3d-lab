"""Necessary simultaneous Y and U height charts for d5a2 global width>17/5.

U=(1,-1,-2), shifted contact heights(2,2,1,0). Three Y-extrema reps suffice
for true global-width counterexamples: every lattice direction remains wide
after an affine lattice automorphism. No U-extrema quotient is assumed.
Four free normalized heights are covered by exact rational outer boxes.
"""
from fractions import Fraction as Q
from itertools import permutations
from pathlib import Path
import argparse,json,time
import z3
from experiments.det5_strong_height_interval import make as make_Y
from experiments.det5_height_interval import symmetries

ROOT=Path(__file__).resolve().parents[1]
ARCHIVE=ROOT/'results/det5_joint_height_interval.json'
U=(1,-1,-2)


def make(C,S,Yext,Uext,box):
    solver,F,q,a,b=make_Y(C,S,Yext,box[:2])
    r=[z3.RealVal(0) if i==Uext[0] else z3.RealVal(1) if i==Uext[1] else z3.Real(f'Uq{i}') for i in range(4)]
    offset,gap=z3.Reals('U_offset U_gap')
    heights=[sum(x*y for x,y in zip(U,p)) for p in C['contact_points']]
    heights=[x-min(heights) for x in heights]
    if heights!=[2,2,1,0]:raise ValueError('second contact covector')
    solver.add(offset>=0,offset+2*gap<=1,gap>0,gap<z3.RealVal('5/17'))
    products={};free=[i for i in range(4) if i not in Uext]
    for i,(low,high) in zip(free,box[2:]):
        l,h=z3.RealVal(str(low)),z3.RealVal(str(high));solver.add(r[i]>=l,r[i]<=h)
        for j in range(4):
            if i==j:continue
            p=z3.Real(f'U_product_{i}_{j}');f=F[i][j];products[i,j]=p
            solver.add(p>=l*f,p<=h*f,p>=r[i]+h*f-h,p<=r[i]+l*f-l)
    for j in range(4):
        solver.add(sum(products[i,j] if (i,j) in products else r[i]*F[i][j] for i in range(4))==offset+gap*heights[j])
    return solver,F,q,r,a,b,offset,gap


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--max-new-nodes-per-chart',type=int,default=1);args=parser.parse_args()
    if args.max_new_nodes_per_chart<1:raise ValueError('positive budget')
    G=json.loads((ROOT/'certificates/nonunimodular_observer_guards.json').read_text())
    scans=json.loads((ROOT/'results/two_vector_class_scan.json').read_text())
    C=next(c for c in G['classes'] if c['class_index']==5);S=next(c for c in scans['classes'] if c['class_index']==5)
    _,_,orbits=symmetries(C['contact_points'])
    data=json.loads(ARCHIVE.read_text()) if ARCHIVE.exists() else {
        'scope':'Necessary simultaneous Y/U-width>17/5 outer relaxations for d5a2; beta183/500. Global-width necessity justifies3Yrepresentatives; all12Uextrema retained. Partial covers and relaxed SAT are not exclusions.',
        'class_index':5,'target':'17/5','beta':'183/500','covectors':[[0,1,0],list(U)],
        'z3_version':z3.get_version_string(),'charts':[],'queries':[]}
    for orbit in orbits:
        Yext=list(orbit[0])
        for Uext in map(list,permutations(range(4),2)):
            chart=next((c for c in data['charts'] if c['Y_extrema']==Yext and c['U_extrema']==Uext),None)
            if chart is None:
                chart={'Y_extrema':Yext,'U_extrema':Uext,'queries':0,'closed_leaves':[],
                       'pending_leaves':[{'node':'r','box':[['0','1'] for _ in range(4)]}],'complete_cover':False};data['charts'].append(chart)
            calls=0
            while chart['pending_leaves'] and calls<args.max_new_nodes_per_chart:
                pending=chart['pending_leaves'][0];tag=pending['node'];box=[[Q(x) for x in pair] for pair in pending['box']]
                if any(r['Y_extrema']==Yext and r['U_extrema']==Uext and r['node']==tag for r in data['queries']):raise ValueError('repeated node')
                solver,*_=make(C,S,Yext,Uext,box)
                path=f'results/det5_joint_{Yext[0]}_{Yext[1]}_{Uext[0]}_{Uext[1]}_{tag}.smt2'
                (ROOT/path).write_text(solver.to_smt2())
                start=time.monotonic();status=solver.check();elapsed=time.monotonic()-start
                row={'Y_extrema':Yext,'U_extrema':Uext,'node':tag,'box':pending['box'],'path':path,
                     'status':str(status),'timeout_ms':1000,'elapsed_seconds':elapsed}
                chart['pending_leaves'].pop(0);chart['queries']+=1;calls+=1
                if status==z3.unsat:chart['closed_leaves'].append(tag)
                else:
                    if status==z3.unknown:row['reason_unknown']=solver.reason_unknown()
                    axis=max(range(4),key=lambda i:box[i][1]-box[i][0]);l,h=box[axis];mid=(l+h)/2
                    for suffix,interval in (('0',(l,mid)),('1',(mid,h))):
                        child=[list(r) for r in box];child[axis]=list(interval)
                        chart['pending_leaves'].append({'node':tag+suffix,'box':[[str(x) for x in pair] for pair in child]})
                chart['complete_cover']=not chart['pending_leaves'];data['queries'].append(row)
                ARCHIVE.write_text(json.dumps(data,indent=2)+'\n')
            print(json.dumps({'Y':Yext,'U':Uext,'queries':chart['queries'],'closed':len(chart['closed_leaves']),
                              'pending':len(chart['pending_leaves']),'complete':chart['complete_cover']}),flush=True)


if __name__=='__main__':main()
