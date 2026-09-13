"""Test a direction-sensitive diagonal-pair sufficient width criterion.

If a row matching has diagonal sums >1 within equal-height contact pairs
and >=22/17 across different heights, then width in that covector is <=17/5.
The query asks for a matrix for which every row matching fails this criterion.
"""
from fractions import Fraction as Q
from itertools import combinations, permutations
from pathlib import Path
import json
import time
import z3
from experiments.contact_contraction_trace_probe import build,certify

ROOT=Path(__file__).resolve().parents[1]
HEIGHTS=(0,1,1,0)
MATCHINGS=[p for p in permutations(range(4)) if all(p[j]!=j for j in range(4))]


def failures(F):
    clauses=[]
    for p in MATCHINGS:
        alternatives=[]
        for j,k in combinations(range(4),2):
            pair=F[p[j]][j]+F[p[k]][k]
            alternatives.append(pair<=1 if HEIGHTS[j]==HEIGHTS[k] else pair<z3.RealVal('22/17'))
        clauses.append(z3.Or(*alternatives))
    return clauses


def matching_data(F):
    result=[]
    for p in MATCHINGS:
        same=[F[p[j]][j]+F[p[k]][k] for j,k in combinations(range(4),2) if HEIGHTS[j]==HEIGHTS[k]]
        cross=[F[p[j]][j]+F[p[k]][k] for j,k in combinations(range(4),2) if HEIGHTS[j]!=HEIGHTS[k]]
        result.append({'permutation':p,'minimum_equal_height_sum':str(min(same)),
                       'minimum_cross_height_sum':str(min(cross)),
                       'criterion_holds':min(same)>1 and min(cross)>=Q(22,17)})
    return result


def main():
    guards=json.loads((ROOT/'certificates/nonunimodular_observer_guards.json').read_text())
    scans=json.loads((ROOT/'results/two_vector_class_scan.json').read_text())
    output=[]
    for idx in (6,7):
        C=next(c for c in guards['classes'] if c['class_index']==idx)
        S=next(c for c in scans['classes'] if c['class_index']==idx)
        solver,F,vectors=build(C,S,include_trace=False)
        solver.add(*failures(F))
        (ROOT/f'results/directional_contraction_class_{idx}.smt2').write_text(solver.to_smt2())
        start=time.monotonic();status=solver.check();elapsed=time.monotonic()-start
        row={'class_index':idx,'determinant':C['normalized_volume'],'status':str(status),
             'elapsed_seconds':elapsed,'timeout_ms':10000,'beta':'37/102',
             'gauge_vectors':vectors,'guard_count':len(C['guards']),
             'height_covector':[0,1,0],'height_values':HEIGHTS,'derangement_count':len(MATCHINGS)}
        if status==z3.sat:
            model=solver.model();matrix=[[model.eval(x).as_fraction() for x in r] for r in F]
            row['F']=[[str(x) for x in r] for r in matrix]
            row['matching_checks']=matching_data(matrix)
            row['exact_body']=certify(matrix,C['contact_points'])
        elif status==z3.unknown:row['reason_unknown']=solver.reason_unknown()
        output.append(row)
        print(json.dumps({k:row[k] for k in ('class_index','status','elapsed_seconds')}),flush=True)
    (ROOT/'results/directional_contraction_probe.json').write_text(json.dumps({
        'scope':'Negates a direction-sensitive sufficient width bound under the stated gauges and complete observer constraints. SAT is an obstruction to this intermediate criterion, not a high-width claim.',
        'z3_version':z3.get_version_string(),'results':output},indent=2)+'\n')


if __name__=='__main__':main()
