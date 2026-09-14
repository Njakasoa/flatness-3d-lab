"""Eight exact parameters for each ordered Y[0,3] chart; no lifted products.

All target constraints are quadratic. Two bounded new formulations, not
retries of the archived 22-variable nonlinear inputs. SAT needs exact body
reconstruction; recorded UNSAT/UNKNOWN alone is no geometric certificate.
"""
from pathlib import Path
from fractions import Fraction
import argparse
import hashlib
import json
import time
import z3

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT/'results/det5_quadratic_height_chart.json'
NAMES = ('low', 'high', 'theta', 'c', 'e', 'r', 'u', 'h')


def matrix(values, order):
    x, y, t, c, e, r, u, h = values
    d = y-x
    core = [[0, 1-h-(1-y)*r, 1-h-(1-x)*u, d*e],
            [1-t+(1-y)*c, 0, u, 1-t-y*e],
            [t-(1-x)*c, r, 0, t+x*e],
            [d*c, h-y*r, h-x*u, 0]]
    perm = [0, 1, 2, 3] if order == 'lt' else [0, 2, 1, 3]
    F = [[0]*4 for _ in range(4)]
    for i in range(4):
        for j in range(4):
            F[perm[i]][perm[j]] = core[i][j]
    q = [0]*4
    for i, v in enumerate((0, x, y, 1)):
        q[perm[i]] = v
    return F, q, x+t*d, h-x-t*d


def rational(v):
    v = Fraction(v)
    return z3.RealVal(f'{v.numerator}/{v.denominator}')


def linear_coords(v, point=False):
    x, y, z = map(Fraction, v)
    return [int(point)+2*x/5-y-z, x/5, y-x/5, z-2*x/5]


def problem(order, beta='37/102', extra_vectors=()):
    values = z3.Reals(' '.join(NAMES))
    x, y, t, c, e, r, u, h = values
    F, q, offset, gap = matrix(values, order)
    C = next(c for c in json.loads((ROOT/'certificates/nonunimodular_observer_guards.json').read_text())['classes'] if c['class_index'] == 5)
    S = next(c for c in json.loads((ROOT/'results/two_vector_class_scan.json').read_text())['classes'] if c['class_index'] == 5)
    vectors = sorted(set(map(tuple, C['primitive_contact_edge_directions'])) |
                     {tuple(r['vector']) for r in S['eligible_vectors']} |
                     set(map(tuple, extra_vectors)))
    constraints = [x >= 0, y <= 1, x < y, t > 0, t < 1,
                   c > 0, e > 0, gap > 0, gap < rational('5/17')]
    constraints += [F[i][j] > 0 for i in range(4) for j in range(4) if i != j]
    for v in vectors:
        co = linear_coords(v)
        image = [sum(F[i][j]*rational(co[j]) for j in range(4)) for i in range(4)]
        if v == (0, 0, 1):
            constraints.append(y*e+(1-x)*c > rational(beta))
        else:
            constraints.append(z3.Or(*[
                sum(image[i] for i in range(4) if mask & (1 << i)) > rational(beta)
                for mask in range(1, 15)]))
    for guard in C['guards']:
        co = linear_coords(guard, True)
        constraints.append(z3.Or(*[
            sum(F[i][j]*rational(co[j]) for j in range(4)) <= 0 for i in range(4)]))
    oldpath = ROOT/'results/det5_class5_y_cvc5_validation.json'
    newpath = ROOT/'results/det5_y_corner_enlarged_3_5.json'
    old, new = (json.loads(p.read_text()) for p in (oldpath, newpath))
    boxes = [r['box'] for r in old['leaves'] if r['extrema'] == [0, 3]] + [new['box']]
    for box in boxes:
        constraints.append(z3.Or(*[cut for i, (lo, hi) in zip((1, 2), box)
                                  for cut in (q[i] < rational(lo), q[i] > rational(hi))]))
    return values, F, q, offset, gap, constraints, vectors, boxes


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--timeout-ms', type=int, default=20000)
    args = ap.parse_args()
    if OUT.exists():
        print('Quadratic chart archive exists; unchanged queries skipped')
        return
    result = {'scope': 'Eight-parameter exact Y[0,3] charts with necessary gauges and strict complements of certified regions. No full-width exclusion from a solver status.',
              'beta': '37/102', 'target': '17/5', 'variables': list(NAMES),
              'maximum_polynomial_degree': 2, 'lifted_product_variables': 0,
              'queries': []}
    for order in ('lt', 'gt'):
        values, F, q, offset, gap, constraints, vectors, boxes = problem(order)
        solver = z3.SolverFor('QF_NRA')
        solver.add(*[z3.simplify(c) for c in constraints])
        solver.set(timeout=args.timeout_ms)
        p = ROOT/f'results/det5_quadratic_height_chart_{order}.smt2'
        raw = solver.to_smt2(); p.write_text(raw)
        start = time.monotonic(); status = solver.check()
        row = {'order': order, 'input_path': str(p.relative_to(ROOT)),
               'input_sha256': hashlib.sha256(raw.encode()).hexdigest(),
               'assertions': len(constraints), 'status': str(status),
               'elapsed_seconds': time.monotonic()-start,
               'timeout_ms': args.timeout_ms, 'z3_version': z3.get_version_string(),
               'gauge_vectors': vectors, 'excluded_rectangles': boxes}
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
