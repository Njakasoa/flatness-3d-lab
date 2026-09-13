"""Two exact SAT/UNSAT pairs for the independent full-matrix encoding."""
from fractions import Fraction as Q
from pathlib import Path
import json
from replay_height_cover_cvc5 import statement,rat,run
from replay_weighted_trace_independent import inv

ROOT=Path(__file__).resolve().parents[1]


def main():
    G=json.loads((ROOT/'certificates/nonunimodular_observer_guards.json').read_text())
    H=json.loads((ROOT/'results/contact_height_charts.json').read_text())
    A=json.loads((ROOT/'results/nonunimodular_complete_smt.json').read_text())
    rows=[]
    for idx in (6,7):
        C=next(c for c in G['classes'] if c['class_index']==idx)
        vectors=next(c for c in H['classes'] if c['class_index']==idx)['gauge_vectors']
        R=next(c for c in A['results'] if c['class_index']==idx)
        F=[list(map(Q,r)) for r in R['controls']['F']];T=inv(F);P=C['contact_points']
        y=[sum(Q(P[i][1])*T[i][j] for i in range(4)) for j in range(4)]
        span=max(y)-min(y);q=[(v-min(y))/span for v in y]
        ext=(q.index(0),q.index(1));offset=-min(y)/span;gap=1/span;extra=[]
        for i in range(4):
            for j in range(4):
                if i!=j:extra.append(f'(assert (= F_{i}_{j} {rat(F[i][j])}))')
            if i not in ext:
                extra.append(f'(assert (= q_{i} {rat(q[i])}))')
                for j in range(4):
                    if i!=j:extra.append(f'(assert (= product_{i}_{j} {rat(q[i]*F[i][j])}))')
        extra.extend([f'(assert (= offset {rat(offset)}))',f'(assert (= gap {rat(gap)}))'])
        statuses=[]
        for W in (Q(1),Q(17,5)):
            text=statement(C,vectors,ext,((Q(0),Q(1)),(Q(0),Q(1))),W)+'\n'.join(extra)+'\n'
            record,_=run(text);statuses.append(record['status'])
        if statuses!=['sat','unsat']:raise ValueError(statuses)
        rows.append({'class_index':idx,'F':R['controls']['F'],'extrema':ext,'normalized_heights':list(map(str,q)),
                     'offset':str(offset),'gap':str(gap),'threshold_one_control':statuses[0],'threshold_17_5_control':statuses[1]})
    print(json.dumps({'status':'PASS','queries':4,
        'scope':'Exactly pinned nontrivial positive and negative controls for the independent full-matrix encoding. The lower threshold is only a control; its ACMS cuts are not generally necessary.',
        'classes':rows},indent=2))


if __name__=='__main__':main()
