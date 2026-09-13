"""New d5a2 interval campaign with a sharper necessary rational gauge.

For w>17/5, ACMS gives gamma>183/500 since A< (17/5)(1-183/500).
Previously excluded boxes are not being rerun unchanged: every query here
has the stronger gauge constraints. A resumed call visits new children only.
"""
from fractions import Fraction as Q
from pathlib import Path
import argparse,json,time
import z3
from experiments.det5_height_interval import symmetries
from experiments.height_interval_relaxation import make as weak_make
from experiments.contact_contraction_trace_probe import ell

ROOT=Path(__file__).resolve().parents[1]
ARCHIVE=ROOT/'results/det5_strong_height_interval.json'
BETA=Q(183,500)


def make(C,S,ext,box):
    solver,F,q,a,b=weak_make(C,S,ext,box)
    vectors=sorted(set(map(tuple,C['primitive_contact_edge_directions']))|
                   {tuple(v['vector']) for v in S['eligible_vectors']})
    for v in vectors:
        l=ell(v,5,2)
        values=[sum(F[i][j]*z3.RealVal(str(l[j])) for j in range(4)) for i in range(4)]
        solver.add(z3.Or(*[sum(values[i] for i in range(4) if mask&(1<<i))>z3.RealVal(str(BETA)) for mask in range(1,15)]))
    return solver,F,q,a,b


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--max-new-nodes-per-chart',type=int,default=31);args=parser.parse_args()
    if args.max_new_nodes_per_chart<1:raise ValueError('positive budget')
    upperA=Q(17,5)*(1-BETA)
    if upperA<=1 or 3*(upperA-1)**2<=4:raise ValueError('invalid necessary gauge threshold')
    G=json.loads((ROOT/'certificates/nonunimodular_observer_guards.json').read_text())
    scans=json.loads((ROOT/'results/two_vector_class_scan.json').read_text())
    C=next(c for c in G['classes'] if c['class_index']==5);S=next(c for c in scans['classes'] if c['class_index']==5)
    _,group,orbits=symmetries(C['contact_points'])
    data=json.loads(ARCHIVE.read_text()) if ARCHIVE.exists() else {
        'scope':'Necessary Y-width>17/5 interval relaxations for d5a2, strengthened to gauge>183/500. Partial covers and relaxed SAT are not class conclusions.',
        'class_index':5,'target':'17/5','beta':str(BETA),'upper_A':str(upperA),
        'radical_margin':str(3*(upperA-1)**2-4),'height_automorphisms':group,
        'z3_version':z3.get_version_string(),'charts':[],'queries':[]}
    for orbit in orbits:
        ext=list(orbit[0]);chart=next((c for c in data['charts'] if c['extrema']==ext),None)
        if chart is None:
            chart={'class_index':5,'extrema':ext,'queries':0,'closed_leaves':[],
                   'pending_leaves':[{'node':'r','box':[['0','1'],['0','1']]}],'complete_cover':False};data['charts'].append(chart)
        calls=0
        while chart['pending_leaves'] and calls<args.max_new_nodes_per_chart:
            item=chart['pending_leaves'][0];tag=item['node'];box=[[Q(x) for x in pair] for pair in item['box']]
            if any(r['extrema']==ext and r['node']==tag for r in data['queries']):raise ValueError('repeated node')
            solver,*_=make(C,S,ext,box);path=f'results/det5_strong_{ext[0]}_{ext[1]}_{tag}.smt2'
            (ROOT/path).write_text(solver.to_smt2())
            start=time.monotonic();status=solver.check();elapsed=time.monotonic()-start
            record={'class_index':5,'extrema':ext,'node':tag,'box':item['box'],'status':str(status),
                    'elapsed_seconds':elapsed,'timeout_ms':1000,'path':path}
            chart['pending_leaves'].pop(0);chart['queries']+=1;calls+=1
            if status==z3.unsat:chart['closed_leaves'].append(tag)
            else:
                if status==z3.unknown:record['reason_unknown']=solver.reason_unknown()
                axis=max(range(2),key=lambda i:box[i][1]-box[i][0]);l,h=box[axis];mid=(l+h)/2
                for suffix,interval in (('0',(l,mid)),('1',(mid,h))):
                    child=[list(r) for r in box];child[axis]=list(interval)
                    chart['pending_leaves'].append({'node':tag+suffix,'box':[[str(x) for x in r] for r in child]})
            data['queries'].append(record);chart['complete_cover']=not chart['pending_leaves']
            ARCHIVE.write_text(json.dumps(data,indent=2)+'\n')
        print(json.dumps({'extrema':ext,'queries':chart['queries'],'closed_leaves':len(chart['closed_leaves']),
                          'pending':len(chart['pending_leaves']),'complete_cover':chart['complete_cover']}),flush=True)


if __name__=='__main__':main()
