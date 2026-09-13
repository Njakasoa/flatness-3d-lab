"""Pair target model with the complete twelve-line hollowness guards.

One bounded main query at width17/5. This strengthens the previous partial
screen using the independently reviewed 1456-point criterion (484 nontrivial
pair clauses). UNKNOWN is not an elimination; solver UNSAT still needs an
independent infeasibility certificate and encoding review.
"""
import json
from fractions import Fraction as Q
from pathlib import Path
import z3
from experiments import det2_pair_column_smt as column
from experiments.det2_observer_lines import build, lam

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'results/det2_pair_complete_smt.json'
TARGET=Q(17,5)
TIMEOUT_MS=30_000


def complete_clauses(matrix, guards):
    return [z3.Or(*[sum(column.base.rational_to_z3(x)*matrix[i][j]
                       for j,x in enumerate(lam(z)))<=0 for i in range(4)]) for z in guards]


def make_solver(threshold, guards):
    solver,expr,_,num,beta=column.make_solver(threshold=threshold,include_pin=False)
    solver.add(*complete_clauses(expr['F'],guards))
    solver.set(timeout=TIMEOUT_MS)
    return solver,expr


def pin_matrix(solver,expr,F):
    solver.add(*[expr['F'][i][j]==column.base.rational_to_z3(F[i][j]) for i in range(4) for j in range(4)])


def main():
    certificate=build()
    archived=json.loads((ROOT/'certificates/det2_observer_lines.json').read_text())
    if json.loads(json.dumps(certificate))!=archived:
        raise ValueError('complete guard archive differs from exact reconstruction')
    guards=certificate['pair_nontrivial_points']
    witness=json.loads((ROOT/'certificates/det2_pair_four_contacts.json').read_text())
    original=[[Q(x) for x in row] for row in witness['exact']['F']]
    p=(2,3,1,0)  # centralizer relabeling puts F01 maximal and F23>=F32
    F=[[original[p[i]][p[j]] for j in range(4)] for i in range(4)]
    controls=[]
    for threshold,expected in ((Q(19,6),'sat'),(TARGET,'unsat')):
        solver,expr=make_solver(threshold,guards);pin_matrix(solver,expr,F)
        result=column.query_result(solver,expr,len(solver.assertions()))
        if result['status']!=expected:
            raise ValueError(f'complete-guard pinned control expected {expected}: {result["status"]}')
        controls.append({'threshold':str(threshold),'expected':expected,**result})
    # Exact guard evaluations of both false high-width candidates, independently
    # of the ACMS constraints that also happen to reject them.
    rejected=[]
    bad=json.loads((ROOT/'certificates/det2_partial_box_counterexamples.json').read_text())
    for case in bad['cases']:
        f=[[Q(x) for x in row] for row in case['F']]
        inside=[list(z) for z in guards if all(sum(f[i][j]*x for j,x in enumerate(lam(z)))>0 for i in range(4))]
        if inside!=[case['hidden_point']]:raise ValueError('full guard missed false candidate interior')
        rejected.append(inside[0])
    solver,expr=make_solver(TARGET,guards)
    path=ROOT/'results/det2_pair_complete_smt.smt2'
    path.write_text('; Complete observer-guard pair model at width17/5\n(set-logic QF_NRA)\n'
                    f'(set-option :timeout {TIMEOUT_MS})\n'+solver.sexpr()+'\n(check-sat)\n')
    result=column.query_result(solver,expr,len(solver.assertions()))
    report={'status':'recorded_complete_guard_target_probe','threshold':str(TARGET),
            'real_variable_count':8,'maximum_polynomial_degree':3,
            'complete_width_direction_count':len(column.DIRECTIONS),
            'complete_guard_count':certificate['finite_guard_count'],
            'explicit_nontrivial_guard_clauses':len(guards),
            'older_partial_guard_clauses_retained_redundantly':40,
            'hollow_scope':'At target17/5, determinant cut gives volume<21 and the reviewed observer theorem makes guards necessary and sufficient for hollowness.',
            'source_claim':'claims/CLAIM-0005.md',
            'positive_and_negative_controls':controls,
            'exact_nonhollow_controls_rejected_at':rejected,
            'main_query':result,'smt2_file':str(path.relative_to(ROOT)),
            'scope':'Complete finite target formulation, one bounded solver run. UNKNOWN supplies no result; UNSAT needs independent certificate/review before class elimination.'}
    OUT.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({'controls':[r['status'] for r in controls],'main':result['status'],
                      'complete_guard_count':len(guards)}))


if __name__=='__main__':main()
