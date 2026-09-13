"""Resumable necessary Y-height interval campaign for the two d=5 classes.

No rank or unique-width-one-direction claim is imported from d=7/8. Only
height-preserving contact automorphisms reduce the extrema cases. Existing
nodes are never requeried: a resumed call visits only pending child boxes.
"""
from fractions import Fraction as Q
from itertools import permutations
from pathlib import Path
import argparse,json,time
import z3
from experiments.nonunimodular_observer_guards import solve
from experiments.height_interval_relaxation import make

ROOT=Path(__file__).resolve().parents[1]
ARCHIVE=ROOT/'results/det5_height_interval.json'


def symmetries(P):
    H=[p[1] for p in P]
    E=[[p[k]-P[0][k] for k in range(3)] for p in P[1:]]
    full=[];group=[]
    for p in permutations(range(4)):
        U=[solve(E,[P[p[j]][k]-P[p[0]][k] for j in range(1,4)]) for k in range(3)]
        if any(x.denominator!=1 for row in U for x in row):continue
        g={'permutation':list(p),'matrix':[[int(x) for x in row] for row in U],'translation':P[p[0]]}
        full.append(g);sign=1-2*H[p[0]]
        if any(H[p[j]]!=H[p[0]]+sign*H[j] for j in range(4)):continue
        group.append({**g,'height_sign':sign})
    todo=set(permutations(range(4),2));orbits=[]
    while todo:
        i,j=min(todo)
        orbit={(g['permutation'][i],g['permutation'][j]) if g['height_sign']==1
               else (g['permutation'][j],g['permutation'][i]) for g in group}
        if not orbit<=todo:raise ValueError('orbit partition')
        todo-=orbit;orbits.append(sorted(orbit))
    return full,group,orbits


def save(data):ARCHIVE.write_text(json.dumps(data,indent=2)+'\n')


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--max-new-nodes-per-chart',type=int,default=31)
    args=parser.parse_args()
    if args.max_new_nodes_per_chart<1:raise ValueError('positive node budget')
    G=json.loads((ROOT/'certificates/nonunimodular_observer_guards.json').read_text())
    scans=json.loads((ROOT/'results/two_vector_class_scan.json').read_text())
    data=json.loads(ARCHIVE.read_text()) if ARCHIVE.exists() else {
        'scope':'Necessary outer Y-width>17/5 relaxations for full relative-interior facet-contact classes4,5. No d7/d8 rank or unique-height assumption. UNSAT excludes only its exact rectangle; a whole-class conclusion requires a full audited cover and independently checked leaf proofs.',
        'z3_version':z3.get_version_string(),'classes':[],'charts':[],'queries':[]}
    for idx in (4,5):
        C=next(c for c in G['classes'] if c['class_index']==idx)
        S=next(c for c in scans['classes'] if c['class_index']==idx)
        full,group,orbits=symmetries(C['contact_points'])
        if not any(c['class_index']==idx for c in data['classes']):
            data['classes'].append({'class_index':idx,'contact_points':C['contact_points'],'full_automorphisms':full,
                                   'height_automorphisms':group,'extrema_orbits':orbits,'guard_count':len(C['guards'])})
        for orbit in orbits:
            ext=list(orbit[0])
            chart=next((c for c in data['charts'] if c['class_index']==idx and c['extrema']==ext),None)
            if chart is None:
                chart={'class_index':idx,'extrema':ext,'queries':0,'closed_leaves':[],
                       'pending_leaves':[{'node':'r','box':[['0','1'],['0','1']]}],'complete_cover':False}
                data['charts'].append(chart)
            calls=0
            while chart['pending_leaves'] and calls<args.max_new_nodes_per_chart:
                pending=chart['pending_leaves'][0];tag=pending['node'];box=[[Q(x) for x in pair] for pair in pending['box']]
                if any(r['class_index']==idx and r['extrema']==ext and r['node']==tag for r in data['queries']):
                    raise ValueError('refuse repeated node')
                solver,*_=make(C,S,ext,box)
                path=f'results/det5_height_{idx}_{ext[0]}_{ext[1]}_{tag}.smt2'
                (ROOT/path).write_text(solver.to_smt2())
                start=time.monotonic();status=solver.check();elapsed=time.monotonic()-start
                row={'class_index':idx,'extrema':ext,'node':tag,'box':pending['box'],'status':str(status),
                     'elapsed_seconds':elapsed,'timeout_ms':1000,'path':path}
                chart['pending_leaves'].pop(0);chart['queries']+=1;calls+=1
                if status==z3.unsat:chart['closed_leaves'].append(tag)
                else:
                    if status==z3.unknown:row['reason_unknown']=solver.reason_unknown()
                    axis=max(range(2),key=lambda i:box[i][1]-box[i][0]);low,high=box[axis];mid=(low+high)/2
                    for suffix,interval in (('0',(low,mid)),('1',(mid,high))):
                        child=[list(r) for r in box];child[axis]=list(interval)
                        chart['pending_leaves'].append({'node':tag+suffix,'box':[[str(x) for x in r] for r in child]})
                data['queries'].append(row);chart['complete_cover']=not chart['pending_leaves'];save(data)
            print(json.dumps({'class_index':idx,'extrema':ext,'new_queries':calls,'total_queries':chart['queries'],
                              'closed_leaves':len(chart['closed_leaves']),'pending':len(chart['pending_leaves']),
                              'complete_cover':chart['complete_cover']}),flush=True)


if __name__=='__main__':main()
