"""Bounded LRA test of whether gauges and blockers force small total leakage.

The extra conclusion tested is max_permutation trace(F)>56/17. It would
give E<12/17 and width<17/5 in a contact width-one direction. Failure of
this stronger sufficient condition is not failure of a width bound.
"""
from fractions import Fraction as Q
from itertools import permutations
from pathlib import Path
import json
import time
import argparse
import z3
from src.exact import Q as Quad, determinant, inverse
from src.geometry import Polytope, certify_hollow, certify_width

ROOT=Path(__file__).resolve().parents[1]
BETA=Q(37,102)
TRACE=Q(56,17)


def ell(z,d,a,affine=False):
    x,y,z=map(Q,z)
    return ((1 if affine else 0)+a*x/d-y-z,x/d,y-x/d,z-a*x/d)


def build(C,scan,strict=False,include_trace=True):
    d=C['normalized_volume'];a=C['contact_points'][1][2]
    F=[[z3.RealVal(0) if i==j else z3.Real(f'f{i}{j}') for j in range(4)] for i in range(4)]
    solver=z3.SolverFor('QF_LRA');solver.set(timeout=10000)
    solver.add(*[F[i][j]>0 for i in range(4) for j in range(4) if i!=j])
    solver.add(*[sum(F[i][j] for i in range(4))==1 for j in range(4)])
    vectors=sorted(set(map(tuple,C['primitive_contact_edge_directions'])) |
                   {tuple(r['vector']) for r in scan['eligible_vectors']})
    for v in vectors:
        l=ell(v,d,a)
        values=[sum(F[i][j]*z3.RealVal(str(l[j])) for j in range(4)) for i in range(4)]
        solver.add(z3.Or(*[sum(values[i] for i in range(4) if mask&(1<<i))>z3.RealVal(str(BETA)) for mask in range(1,15)]))
    for v in C['guards']:
        l=ell(v,d,a,True)
        solver.add(z3.Or(*[sum(F[i][j]*z3.RealVal(str(l[j])) for j in range(4))<=0 for i in range(4)]))
    if include_trace:
        for p in permutations(range(4)):
            value=sum(F[p[j]][j] for j in range(4))
            solver.add(value<z3.RealVal(str(TRACE)) if strict else value<=z3.RealVal(str(TRACE)))
    return solver,F,vectors


def certify(matrix,contacts):
    F=[[Quad(x) for x in row] for row in matrix]
    det=determinant(F)
    if not det:
        return {'invertible':False}
    T=inverse(F)
    vertices=[[sum((Quad(contacts[i][k])*T[i][j] for i in range(4)),Quad()) for k in range(3)] for j in range(4)]
    body=Polytope(vertices)
    hollow=certify_hollow(body)
    width=certify_width(body)
    matching=max(sum(matrix[p[j]][j] for j in range(4)) for p in permutations(range(4)))
    return {'invertible':True,'determinant':str(det.a),'vertices':body.json(),
            'volume':body.volume().json(),'hollow':hollow,'width':width,
            'maximum_permutation_trace':str(matching),'minimum_total_off_permutation_mass':str(4-matching)}


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--strict',action='store_true',help='Test trace strictly below the cutoff, preserving the original non-strict run.')
    args=parser.parse_args()
    suffix='_strict' if args.strict else ''
    guards=json.loads((ROOT/'certificates/nonunimodular_observer_guards.json').read_text())
    scans=json.loads((ROOT/'results/two_vector_class_scan.json').read_text())
    results=[]
    for idx in (6,7):
        C=next(c for c in guards['classes'] if c['class_index']==idx)
        scan=next(c for c in scans['classes'] if c['class_index']==idx)
        solver,F,vectors=build(C,scan,args.strict)
        (ROOT/f'results/contraction_trace_class_{idx}{suffix}.smt2').write_text(solver.to_smt2())
        start=time.monotonic();status=solver.check();elapsed=time.monotonic()-start
        row={'class_index':idx,'determinant':C['normalized_volume'],'beta':str(BETA),
             'trace_upper_bound':str(TRACE),'trace_comparison':'<' if args.strict else '<=',
             'gauge_vectors':vectors,'guard_count':len(C['guards']),
             'status':str(status),'elapsed_seconds':elapsed,'timeout_ms':10000}
        if status==z3.sat:
            model=solver.model()
            matrix=[[model.eval(x).as_fraction() for x in r] for r in F]
            row['F']=[[str(x) for x in r] for r in matrix]
            row['exact_body']=certify(matrix,C['contact_points'])
        elif status==z3.unknown:
            row['reason_unknown']=solver.reason_unknown()
        results.append(row)
        print(json.dumps({k:row[k] for k in ('class_index','status','elapsed_seconds')}),flush=True)
    output={'scope':'Tests a sufficient total-leakage criterion under exact necessary gauge and complete observer constraints. SAT refutes only that criterion; no high-width body is inferred. Exact bodies are independently certified by the existing full geometry engine.',
            'z3_version':z3.get_version_string(),'results':results}
    (ROOT/f'results/contact_contraction_trace_probe{suffix}.json').write_text(json.dumps(output,indent=2)+'\n')


if __name__=='__main__':main()
