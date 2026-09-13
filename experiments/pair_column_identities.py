"""Formal identities for the column-normalized pair chart (SymPy)."""
import itertools
import json
from pathlib import Path
import sympy as s

ROOT = Path(__file__).resolve().parents[1]
VARS = s.symbols('c0 d0 c1 d1 c2 d2 c3 d3')
SIGMA = (1, 0, 3, 2)


def require(condition, message):
    if not condition:
        raise ValueError(message)


def record(expr):
    poly = s.Poly(s.expand(expr), *VARS)
    return {'degree': int(poly.total_degree()),
            'terms': [{'powers': list(m), 'coefficient': str(c)} for m, c in poly.terms()]}


def main():
    F = s.zeros(4)
    for j in range(4):
        rest = [i for i in range(4) if i not in (j, SIGMA[j])]
        c, d = VARS[2*j:2*j+2]
        F[SIGMA[j], j], F[rest[0], j], F[rest[1], j] = c, d, 1-c-d
    delta = s.expand(F.det(method='domain-ge'))
    S = F.adjugate()
    require(s.Poly(delta, *VARS).total_degree() == 3, 'determinant degree changed')
    for i in range(4):
        for j, k in itertools.combinations(range(4), 2):
            require(s.Poly(s.expand(S[i, j]-S[i, k]), *VARS).total_degree() <= 2,
                    'column difference not quadratic')
    axis_contacts = [(0, 2, 0, 0), (0, 1, 1, 0), (0, 1, 0, 1)]
    widths = []
    for axis, values in enumerate(axis_contacts):
        for j, k in itertools.combinations(range(4), 2):
            expr = s.expand(sum(values[i]*(S[i, j]-S[i, k]) for i in range(4)))
            widths.append({'axis': axis, 'vertex_pair': [j, k], 'numerator': record(expr)})
    ell = [s.Matrix([s.Rational(1, 2), s.Rational(1, 2), -s.Rational(1, 2), -s.Rational(1, 2)]),
           s.Matrix([-1, 0, 1, 0]), s.Matrix([-1, 0, 0, 1])]
    positive_rows = [(0, 1), (0, 3), (0, 2)]
    D = sum(F[i, SIGMA[i]] for i in range(4))
    expected = [D/2-1, F[0, 2]+F[3, 2]-F[3, 0], F[0, 3]+F[2, 3]-F[2, 0]]
    for vector, rows, formula in zip(ell, positive_rows, expected):
        theta = F*vector
        require(s.expand(sum(theta)) == 0, 'difference coordinates not zero sum')
        require(s.expand(sum(theta[i] for i in rows)-formula) == 0, 'gauge identity failed')
    sample = s.Matrix([[0, s.Rational(9,10), s.Rational(1,20), s.Rational(1,20)],
                       [s.Rational(9,10), 0, s.Rational(1,20), s.Rational(17,20)],
                       [s.Rational(1,20), s.Rational(1,20), 0, s.Rational(1,10)],
                       [s.Rational(1,20), s.Rational(1,20), s.Rational(9,10), 0]])
    require(all(sum(sample[:, j]) == 1 for j in range(4)), 'sample column sum')
    require(all(sample[i, j] > 0 for i in range(4) for j in range(4) if i != j), 'sample positivity')
    require(all(2*sample[i, SIGMA[i]] >= sum(sample[i, :]) for i in range(4)), 'sample dominance')
    require(sample.det() == s.Rational(9, 250), 'sample determinant')
    gamma = [sum(abs(t) for t in sample*v)/2 for v in ell]
    require(gamma[0] == s.Rational(2, 5) and gamma[2] == s.Rational(1, 10), 'sample gauges')
    data = {'status': 'column_chart_formal_identities_passed',
            'variables': [str(v) for v in VARS],
            'determinant': record(delta), 'axis_width_numerators': widths,
            'coordinate_gauges': [record(t) for t in expected],
            'target_width': '17/5', 'gauge_strict_lower': '37/102',
            'determinant_strict_lower': '50653/3183624',
            'sample': {'facet_matrix': [[str(t) for t in sample.row(i)] for i in range(4)],
                       'determinant': '9/250', 'coordinate_gauges': [str(g) for g in gamma]},
            'scope': 'Formal chart identities and necessary cuts, not infeasibility or a width theorem.'}
    (ROOT/'certificates/pair_column_identities.json').write_text(json.dumps(data, indent=2)+'\n')
    print('PASS: eight-variable column chart; cubic determinant; 24 quadratic column differences; 18 width numerators; three gauge identities')


if __name__ == '__main__':
    main()
