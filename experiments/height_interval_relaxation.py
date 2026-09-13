"""Exact rational McCormick outer relaxations of complete Y-height charts.

Branch only the two free normalized heights. UNSAT excludes an entire closed
height rectangle. A finite cover would prove a directional bound; a bounded
partial cover does not. Every target below is new; archived queries are not
rerun. Product relaxation uses F entries in [0,1], following stochasticity.
"""
from fractions import Fraction as Q
from pathlib import Path
import json,time
import z3
from experiments.contact_height_charts import height_model,symmetries

ROOT=Path(__file__).resolve().parents[1]


def make(C,S,extrema,box):
    base,F,q,a,b,_=height_model(C,S,extrema)
    solver=z3.SolverFor('QF_LRA');solver.set(timeout=1000)
    # The final four constraints are exactly the four column-height identities.
    solver.add(*list(base.assertions())[:-4])
    products={}
    free=[i for i in range(4) if i not in extrema]
    for i,(low,high) in zip(free,box):
        l,h=z3.RealVal(str(low)),z3.RealVal(str(high))
        solver.add(q[i]>=l,q[i]<=h)
        for j in range(4):
            if j==i:continue
            f=F[i][j];p=z3.Real(f'height_product_{i}_{j}');products[i,j]=p
            solver.add(p>=l*f,p<=h*f,p>=q[i]+h*f-h,p<=q[i]+l*f-l)
    for j in range(4):
        total=sum(products[i,j] if (i,j) in products else q[i]*F[i][j] for i in range(4))
        solver.add(total==a+b*(1 if j in (1,2) else 0))
    return solver,F,q,a,b


def main():
    guards=json.loads((ROOT/'certificates/nonunimodular_observer_guards.json').read_text())
    scans=json.loads((ROOT/'results/two_vector_class_scan.json').read_text())
    records=[];summary=[];budget=31
    for idx in (6,7):
        C=next(c for c in guards['classes'] if c['class_index']==idx)
        S=next(c for c in scans['classes'] if c['class_index']==idx)
        _,orbits=symmetries(C['contact_points'])
        for orbit in orbits:
            extrema=orbit[0];queue=[('r',((Q(0),Q(1)),(Q(0),Q(1))))];closed=[];unknown=[];calls=0
            while queue and calls<budget:
                tag,box=queue.pop(0);solver,F,q,a,b=make(C,S,extrema,box)
                path=f'results/height_interval_{idx}_{extrema[0]}_{extrema[1]}_{tag}.smt2'
                (ROOT/path).write_text(solver.to_smt2())
                start=time.monotonic();status=solver.check();elapsed=time.monotonic()-start;calls+=1
                row={'class_index':idx,'extrema':extrema,'node':tag,'box':[[str(x) for x in r] for r in box],
                     'status':str(status),'elapsed_seconds':elapsed,'timeout_ms':1000,'path':path}
                if status==z3.unsat:closed.append(tag)
                else:
                    if status==z3.unknown:row['reason_unknown']=solver.reason_unknown();unknown.append(tag)
                    axis=max(range(2),key=lambda i:box[i][1]-box[i][0]);l,h=box[axis];m=(l+h)/2
                    for suffix,interval in (('0',(l,m)),('1',(m,h))):
                        child=list(box);child[axis]=interval;queue.append((tag+suffix,tuple(child)))
                records.append(row)
            item={'class_index':idx,'extrema':extrema,'queries':calls,'closed_leaves':closed,
                  'pending_leaves':[{'node':tag,'box':[[str(x) for x in r] for r in box]} for tag,box in queue],
                  'complete_cover':not queue,'unknown_nodes':unknown}
            summary.append(item)
            print(json.dumps({k:item[k] for k in ('class_index','extrema','queries','complete_cover')},ensure_ascii=True),flush=True)
            (ROOT/'results/height_interval_relaxation.json').write_text(json.dumps({
                'scope':'Exact rational outer interval relaxations of Y-width>17/5. UNSAT excludes a rectangle; SAT is only a relaxed solution. Only a complete checked cover could exclude a whole extrema chart.',
                'z3_version':z3.get_version_string(),'max_queries_per_chart':budget,'charts':summary,'queries':records},indent=2)+'\n')


if __name__=='__main__':main()
