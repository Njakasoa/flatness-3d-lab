"""Complete eight-variable cubic pair target with 20 hollow clauses.

Completeness requires the SIX primitive contact-edge gauges, explicitly
asserted below. The 64-point guard theorem is valid without a volume bound.
The stronger volume/axis cuts are retained as necessary target conditions.
"""
import itertools
import json
from fractions import Fraction as Q
from pathlib import Path
import z3
from experiments import det2_pair_column_smt as column
from experiments.det2_observer_gauge_guards import build as guard_build
from experiments.det2_pair_complete_smt import complete_clauses, pin_matrix

ROOT=Path(__file__).resolve().parents[1]
TARGET=Q(17,5)
TIMEOUT_MS=30_000


def edge_gauge_clauses(F,edges,beta):
    clauses=[]
    for x,y,z in edges:
        ell=(Q(x,2)-y-z,Q(x,2),y-Q(x,2),z-Q(x,2))
        theta=[sum(column.base.rational_to_z3(ell[j])*F[i][j] for j in range(4)) for i in range(4)]
        subsets=[sum(theta[i] for i in range(4) if mask&(1<<i))>column.base.rational_to_z3(beta) for mask in range(1,15)]
        clauses.append(z3.Or(*subsets))
    return clauses


def make_solver(threshold,guards):
    c,d=column.column_parameters();F=column.column_matrix(c,d)
    delta=column.polynomial(column.base.determinant4(F));S=column.base.signed_adjugate(F)
    T,V=column.ambient_reconstruction(S,delta)
    assertions=column.column_base_constraints(F,c,d,delta)
    acms,beta=column.acms_constraints(F,c,delta,threshold);assertions.extend(acms)
    widths,num=column.width_constraints(S,delta,threshold);assertions.extend(widths)
    assertions.extend(complete_clauses(F,guards['pair_nontrivial_points']))
    assertions.extend(edge_gauge_clauses(F,guards['edge_directions'],beta))
    solver=z3.Solver();solver.set(timeout=TIMEOUT_MS,random_seed=column.SEED);solver.add(*assertions)
    return solver,{'c':c,'d':d,'F':F,'delta':delta,'S':S,'T':T,'V':V,'beta':beta,'threshold':threshold}


def main():
    guards=guard_build()
    archived=json.loads((ROOT/'certificates/det2_observer_gauge_guards.json').read_text())
    if json.loads(json.dumps(guards))!=archived:raise ValueError('guard certificate changed')
    if len(guards['edge_directions'])!=6 or len(guards['pair_nontrivial_points'])!=20:
        raise ValueError('complete edge/guard coverage changed')
    witness=json.loads((ROOT/'certificates/det2_pair_four_contacts.json').read_text())
    original=[[Q(x) for x in row] for row in witness['exact']['F']]
    p=(2,3,1,0);F=[[original[p[i]][p[j]] for j in range(4)] for i in range(4)]
    controls=[]
    for threshold,expected in ((Q(19,6),'sat'),(TARGET,'unsat')):
        solver,expr=make_solver(threshold,guards);pin_matrix(solver,expr,F)
        result=column.query_result(solver,expr,len(solver.assertions()))
        if result['status']!=expected:raise ValueError('pinned control failed: '+str(result['status']))
        controls.append({'threshold':str(threshold),**result})
    solver,expr=make_solver(TARGET,guards)
    path=ROOT/'results/det2_pair_gauge_complete_smt.smt2'
    path.write_text('; Complete20 hollow clauses plus SIX edge gauges at width17/5\n(set-logic QF_NRA)\n'
                    f'(set-option :timeout {TIMEOUT_MS})\n'+solver.sexpr()+'\n(check-sat)\n')
    result=column.query_result(solver,expr,len(solver.assertions()))
    report={'status':'recorded_gauge_complete_pair_probe','target':str(TARGET),'beta':str(guards['beta']),
            'real_variable_count':8,'maximum_polynomial_degree':3,
            'width_directions':len(column.DIRECTIONS),'complete_hollow_clauses':20,
            'six_contact_edge_gauge_directions':guards['edge_directions'],
            'four_contact_positive_and_negative_controls':controls,'main_query':result,
            'smt2_file':str(path.relative_to(ROOT)),
            'completeness':'At target17/5, the boundary-contact chart, six explicit edge gauges >37/102 and 20 point exclusions are necessary and sufficient for hollowness. Width list is complete. Lower-threshold pinned control is only a control, not a general theorem at that threshold.',
            'scope':'One bounded target query. UNKNOWN is not elimination; UNSAT would require independent infeasibility certificate and encoding review.'}
    (ROOT/'results/det2_pair_gauge_complete_smt.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({'controls':[r['status'] for r in controls],'main':result['status'],'hollow_clauses':20,'edge_gauges':6}))


if __name__=='__main__':main()
