"""Exact symbolic certificate for six horizontal parameters and linear fibers.

No solver calls. Coordinate pair numerators are jointly affine in theta,h.
After dividing by the positive height gap, each fixed rational horizontal
shape has a complete linear-arithmetic width feasibility formulation.
"""
from pathlib import Path
import hashlib
import json
import sympy as s
from experiments.det5_quadratic_height_chart import NAMES, matrix

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT/'certificates/det5_horizontal_fiber_structure.json'


def need(condition, message):
    if not condition:
        raise ValueError(message)


def main():
    v = s.symbols(' '.join(NAMES))
    x, y, t, c, e, r, u, h = v
    sigma = (x, y, c, e, r, u)
    alpha, eta, rho = s.symbols('alpha eta rho')
    gap = h-x-t*(y-x)
    D = u*((1-x)*c+x*e)-r*((1-y)*c+y*e)
    P = s.Matrix([[0, 5, 0, 0], [0, 1, 1, 0], [0, 2, 0, 1]])
    def encode(expr):
        return [{'powers': list(p), 'coefficient': str(k)}
                for p, k in s.Poly(s.expand(expr), *sigma).terms()]
    result = {'status': 'PASS', 'scope': 'Symbolic fiber structure, not a finite horizontal-domain cover or a flatness bound.',
              'horizontal_variables': list(map(str, sigma)),
              'linear_variables': ['alpha=theta/gap', 'eta=h/gap', 'rho=1/gap'],
              'linear_equality': 'eta-low*rho-(high-low)*alpha=1',
              'horizontal_determinant': encode(D), 'branches': [],
              'solver_queries_run': 0}
    for order in ('lt', 'gt'):
        F = s.Matrix(matrix(v, order)[0])
        adj = F.adjugate(method='berkowitz')
        need(all(s.expand(z) == 0 for z in F*adj-gap*D*s.eye(4)), 'adjugate determinant identity')
        N = P*adj
        affine_F = []
        for i in range(4):
            for j in range(4):
                coefficients = [s.expand(F[i, j]).coeff(t), s.expand(F[i, j]).coeff(h), F[i, j].subs({t: 0, h: 0})]
                need(s.expand(F[i, j]-coefficients[0]*t-coefficients[1]*h-coefficients[2]) == 0, 'F affine in fiber')
                M = coefficients[0]*alpha+coefficients[1]*eta+coefficients[2]*rho
                need(s.expand(rho*F[i, j].subs({t: alpha/rho, h: eta/rho})-M) == 0, 'scaled F linear')
                affine_F.append({'row': i, 'column': j,
                                 'alpha': encode(coefficients[0]), 'eta': encode(coefficients[1]), 'rho': encode(coefficients[2])})
        coordinate_pairs = []
        for k in range(3):
            for i in range(4):
                for j in range(i):
                    numerator = s.expand(N[k, i]-N[k, j])
                    coefficients = [numerator.coeff(t), numerator.coeff(h), numerator.subs({t: 0, h: 0})]
                    need(s.expand(numerator-coefficients[0]*t-coefficients[1]*h-coefficients[2]) == 0, 'all pair numerators affine')
                    need(s.Poly(numerator, t, h).total_degree() <= 1, 'joint fiber degree')
                    coordinate_pairs.append({'coordinate': k, 'vertex_pair': [i, j],
                                             'alpha': encode(coefficients[0]), 'eta': encode(coefficients[1]), 'rho': encode(coefficients[2])})
        result['branches'].append({'order': order, 'adjugate_identities': 16,
                                   'scaled_F_entries': affine_F, 'coordinate_pair_numerators': coordinate_pairs})
    # In the low/high order these are the images of (5,0,2) and (0,0,1).
    F = s.Matrix(matrix(v, 'lt')[0])
    horizontal_R = F[:, 1]-F[:, 2]
    horizontal_Z = F[:, 3]-F[:, 0]
    need(all(z.free_symbols <= set(sigma) for z in map(s.simplify, list(horizontal_R)+list(horizontal_Z))), 'horizontal images independent of fiber')
    need(s.expand(horizontal_R[1]*horizontal_Z[2]-horizontal_R[2]*horizontal_Z[1]+D) == 0, 'horizontal minor')
    result['horizontal_images_lt'] = {'R': [encode(z) for z in horizontal_R], 'Z': [encode(z) for z in horizontal_Z]}
    result['source_generator_sha256'] = hashlib.sha256((ROOT/'experiments/det5_quadratic_height_chart.py').read_bytes()).hexdigest()
    raw = json.dumps(result, indent=2)+'\n'
    if OUT.exists():
        need(OUT.read_text() == raw, 'immutable symbolic certificate')
    else:
        OUT.write_text(raw)
    print('HORIZONTAL_FIBER_STRUCTURE=PASS: 32 adjugate identities, 32 scaled entries, 36 pair numerators; no solver queries')


if __name__ == '__main__':
    main()
