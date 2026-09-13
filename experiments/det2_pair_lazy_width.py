"""Bounded lazy width cuts for the column-normalized pair model.

At most six checks, each with a 15-second requested timeout. SAT models are
reconstructed with exact Fraction arithmetic before selecting the next cut.
The 37-direction list is complete for the 17/5 target, not a guessed radius.
"""
import json
from fractions import Fraction as Q
from pathlib import Path

import z3
from experiments import det2_pair_column_smt as column

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT/'results/det2_pair_lazy_width.json'
TARGET = Q(17, 5)
MAX_CHECKS = 6
TIMEOUT_MS = 15_000


def require(condition, message):
    if not condition:
        raise ValueError(message)


def inverse(matrix):
    a = [[Q(t) for t in row] + [Q(i == j) for j in range(4)]
         for i, row in enumerate(matrix)]
    for j in range(4):
        pivot = next(i for i in range(j, 4) if a[i][j])
        a[j], a[pivot] = a[pivot], a[j]
        scale = a[j][j]
        a[j] = [x/scale for x in a[j]]
        for i in range(4):
            if i != j:
                scale = a[i][j]
                a[i] = [x-scale*y for x, y in zip(a[i], a[j])]
    return [row[4:] for row in a]


def exact_model(model, expressions):
    F = column.base.model_fraction_matrix(model, expressions['F'])
    T = inverse(F)
    require(all(sum(F[i][j] for i in range(4)) == 1 for j in range(4)),
            'exact column normalization failed')
    require(all(sum(T[i][j] for i in range(4)) == 1 for j in range(4)),
            'exact vertex affine normalization failed')
    vertices = [[2*T[1][j], T[1][j]+T[2][j], T[1][j]+T[3][j]] for j in range(4)]
    widths = []
    for direction, _ in column.DIRECTIONS:
        values = [sum(Q(u)*x for u, x in zip(direction, p)) for p in vertices]
        widths.append((max(values)-min(values), direction))
    widths.sort()
    return F, vertices, widths


def main():
    direction_table = dict(column.DIRECTIONS)
    active = [(1, 0, 0)]
    solver, expr, _, _, _ = column.make_solver(
        threshold=TARGET, include_pin=False,
        directions=[(u, direction_table[u]) for u in active])
    solver.set(timeout=TIMEOUT_MS)
    report = {'status': 'running', 'target': str(TARGET),
              'maximum_checks': MAX_CHECKS, 'timeout_ms_per_check': TIMEOUT_MS,
              'scope': 'Partial hollow relaxation; SAT is not a hollow certificate, UNKNOWN is not elimination.',
              'steps': []}
    OUT.write_text(json.dumps(report, indent=2)+'\n')
    for step in range(MAX_CHECKS):
        path = ROOT/f'results/det2_pair_lazy_width_step_{step}.smt2'
        path.write_text(f'; Lazy width stage {step}, active directions {active}\n'
                        f'(set-option :timeout {TIMEOUT_MS})\n(set-logic QF_NRA)\n'
                        + solver.sexpr()+'\n(check-sat)\n')
        result = column.query_result(solver, expr, len(solver.assertions()))
        result['active_width_directions'] = [list(u) for u in active]
        result['smt2_file'] = str(path.relative_to(ROOT))
        report['steps'].append(result)
        if result['status'] != 'sat':
            report['status'] = 'unreviewed_unsat' if result['status'] == 'unsat' else 'unknown'
            OUT.write_text(json.dumps(report, indent=2)+'\n')
            print(f"Stage {step}: {result['status']}", flush=True)
            return
        try:
            F, vertices, widths = exact_model(solver.model(), expr)
        except ValueError as error:
            result['exact_reconstruction_error'] = str(error)
            report['status'] = 'sat_requires_algebraic_review'
            OUT.write_text(json.dumps(report, indent=2)+'\n')
            return
        width_by_direction = {u: w for w, u in widths}
        require(all(width_by_direction[u] > TARGET for u in active), 'model violates encoded width')
        value, direction = widths[0]
        result['exact_F'] = [[str(t) for t in row] for row in F]
        result['exact_vertices'] = [[str(t) for t in row] for row in vertices]
        result['finite_minimum_width'] = str(value)
        result['minimizing_retained_direction'] = list(direction)
        result['exact_active_width_checks_passed'] = True
        result['all_37_target_tests_passed'] = value > TARGET
        print(f'Stage {step}: SAT; exact finite minimum {value} in {direction}', flush=True)
        if value > TARGET:
            report['status'] = 'width_target_passes_needs_full_hollow_check'
            OUT.write_text(json.dumps(report, indent=2)+'\n')
            return
        require(direction not in active, 'violating direction already encoded')
        if step + 1 < MAX_CHECKS:
            active.append(direction)
            constraints, _ = column.width_constraints(expr['S'], expr['delta'], TARGET,
                directions=[(direction, direction_table[direction])])
            solver.add(*constraints)
        report['status'] = 'running' if step + 1 < MAX_CHECKS else 'check_cap_reached'
        OUT.write_text(json.dumps(report, indent=2)+'\n')


if __name__ == '__main__':
    main()
