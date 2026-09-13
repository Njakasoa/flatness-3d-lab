"""Bounded exact LRA pilot on genuinely new normalized-height fibers.

Fix Y-width=7/2 and two normalized intermediate heights. This asks whether
Y-width alone could prune these classes; it is not a global-width search.
No volume cut is imposed. Stop on the first SAT fiber of each class.
"""
from fractions import Fraction as Q
from pathlib import Path
import json,time
import z3
from experiments.contact_height_charts import height_model,symmetries

ROOT=Path(__file__).resolve().parents[1]
PAIRS=((Q(1,3),Q(2,3)),(Q(2,3),Q(1,3)),(Q(1,2),Q(1,2)),(Q(0),Q(1)),(Q(1),Q(0)))


def main():
    guards=json.loads((ROOT/'certificates/nonunimodular_observer_guards.json').read_text())
    scans=json.loads((ROOT/'results/two_vector_class_scan.json').read_text())
    records=[]
    for idx in (6,7):
        C=next(c for c in guards['classes'] if c['class_index']==idx)
        S=next(c for c in scans['classes'] if c['class_index']==idx)
        _,orbits=symmetries(C['contact_points']);found=False
        for orbit in orbits:
            ext=orbit[0];base,F,q,a,b,_=height_model(C,S,ext)
            i,j=[h for h in range(4) if h not in ext]
            for number,(qi,qj) in enumerate(PAIRS):
                subs=((q[i],z3.RealVal(str(qi))),(q[j],z3.RealVal(str(qj))),(b,z3.RealVal('2/7')))
                solver=z3.SolverFor('QF_LRA');solver.set(timeout=1000)
                solver.add(*[z3.simplify(z3.substitute(e,*subs),som=True) for e in base.assertions()])
                path=f'results/fixed_height_{idx}_{ext[0]}_{ext[1]}_{number}.smt2'
                (ROOT/path).write_text(solver.to_smt2())
                start=time.monotonic();status=solver.check();elapsed=time.monotonic()-start
                r={'class_index':idx,'extrema':ext,'other_heights':[str(qi),str(qj)],'height_gap':'2/7',
                   'status':str(status),'timeout_ms':1000,'elapsed_seconds':elapsed,'path':path}
                if status==z3.sat:
                    model=solver.model();r['F']=[[str(model.eval(e).as_fraction()) for e in row] for row in F]
                    r['offset']=str(model.eval(a).as_fraction());found=True
                elif status==z3.unknown:r['reason_unknown']=solver.reason_unknown()
                records.append(r)
                print(json.dumps({k:r[k] for k in ('class_index','extrema','other_heights','status','elapsed_seconds')}),flush=True)
                (ROOT/'results/fixed_height_fibers.json').write_text(json.dumps({
                    'scope':'Finite fixed-height fibers at Y-width 7/2, with complete observer and gauge constraints. No full lattice-width or volume target. UNSAT applies only to an exact fiber; SAT requires independent whole-body validation.',
                    'z3_version':z3.get_version_string(),'cases':records},indent=2)+'\n')
                if found:break
            if found:break


if __name__=='__main__':main()
