"""Eight-variable complete fifteen-width target, with exact adjugate formulas.

The chart is quadratic; cleared-denominator width inequalities have degree
at most five. All fifteen directions are necessary and sufficient for width
>17/5 under contact containment. No solver status is itself a certificate.
"""
from pathlib import Path
import argparse
import hashlib
import json
import time
import sympy as sp
import z3
from experiments.det5_quadratic_height_chart import NAMES, matrix, problem, rational

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT/'results/det5_quadratic_full_width.json'
EXTRA = [(1, -1, 1)]


def polynomial(expr, symbols, values):
    out = z3.RealVal(0)
    for powers, coefficient in sp.Poly(sp.expand(expr), *symbols).terms():
        term = rational(str(coefficient))
        for v, degree in zip(values, powers):
            if degree:
                term *= v**degree
        out += term
    return z3.simplify(out)


def complete_problem(order):
    values, _, _, _, _, constraints, gauges, boxes = problem(order, '183/500', EXTRA)
    symbols = sp.symbols(' '.join(NAMES))
    F = sp.Matrix(matrix(symbols, order)[0])
    x, y, t, c, e, r, u, h = symbols
    b = h-x-t*(y-x)
    D = u*((1-x)*c+x*e)-r*((1-y)*c+y*e)
    determinant = sp.expand(b*D)
    # Conjugating rows and columns leaves this determinant unchanged.
    adj = F.adjugate(method='berkowitz')
    P = sp.Matrix([[0, 5, 0, 0], [0, 1, 1, 0], [0, 2, 0, 1]])
    numerators = P*adj
    delta = polynomial(determinant, symbols, values)
    constraints.append(delta != 0)
    absolute_det = z3.If(delta > 0, delta, -delta)
    directions = json.loads((ROOT/'results/det5_complete_geometry_validation.json').read_text())['directions']
    rows = []
    for direction in directions:
        if direction == [0, 1, 0]:
            # Already imposed exactly as 0<b<5/17.
            continue
        gaps = [sp.expand(sum(direction[k]*(numerators[k, i]-numerators[k, j]) for k in range(3)))
                for i in range(4) for j in range(i)]
        cleared = [polynomial(g, symbols, values) for g in gaps]
        constraints.append(z3.Or(*[cut for g in cleared
                                  for cut in (5*g > 17*absolute_det, -5*g > 17*absolute_det)]))
        rows.append({'direction': direction, 'pairs': 6,
                     'maximum_numerator_degree': max(sp.Poly(g, *symbols).total_degree() for g in gaps)})
    return values, constraints, gauges, boxes, rows


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--timeout-ms', type=int, default=20000)
    args = ap.parse_args()
    if OUT.exists():
        print('Complete eight-variable archive exists; unchanged queries skipped')
        return
    result = {'scope': 'Complete fifteen-width >17/5 target in two ordered Y[0,3] charts. Degree-five cleared widths, strong necessary gauges, exact facet/height reconstruction. Status alone proves no class exclusion.',
              'beta': '183/500', 'target': '17/5', 'variables': list(NAMES),
              'extra_gauges': EXTRA, 'maximum_polynomial_degree': 5, 'queries': []}
    for order in ('lt', 'gt'):
        values, constraints, gauges, boxes, widths = complete_problem(order)
        solver = z3.SolverFor('QF_NRA')
        solver.add(*[z3.simplify(c) for c in constraints])
        solver.set(timeout=args.timeout_ms)
        path = ROOT/f'results/det5_quadratic_full_width_{order}.smt2'
        raw = solver.to_smt2(); path.write_text(raw)
        start = time.monotonic(); status = solver.check()
        row = {'order': order, 'input_path': str(path.relative_to(ROOT)),
               'input_sha256': hashlib.sha256(raw.encode()).hexdigest(),
               'status': str(status), 'elapsed_seconds': time.monotonic()-start,
               'timeout_ms': args.timeout_ms, 'z3_version': z3.get_version_string(),
               'assertions': len(constraints), 'gauge_vectors': gauges,
               'excluded_rectangles': boxes, 'cleared_widths': widths,
               'Y_width_encoded_by_gap': True}
        if status == z3.unknown:
            row['reason_unknown'] = solver.reason_unknown()
        if status == z3.sat:
            model = solver.model()
            row['assignment'] = {str(v): model.eval(v, model_completion=True).sexpr() for v in values}
            row['rational_assignment'] = all(z3.is_rational_value(model.eval(v)) for v in values)
            row['all_assertions_true'] = all(z3.is_true(z3.simplify(model.eval(c, model_completion=True))) for c in solver.assertions())
        result['queries'].append(row)
        OUT.write_text(json.dumps(result, indent=2)+'\n')
        print(json.dumps({k: row[k] for k in ('order', 'status', 'elapsed_seconds')}), flush=True)


if __name__ == '__main__':
    main()
