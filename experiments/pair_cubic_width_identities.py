"""Verify the complementary-minor identities for a cubic pair-branch model."""
import itertools
import json
from pathlib import Path

import sympy as s

ROOT = Path(__file__).resolve().parents[1]
VARIABLES = s.symbols('a0 b0 a1 b1 a2 b2 a3 b3')
SIGMA = (1, 0, 3, 2)


def require(value, message):
    if not value:
        raise ValueError(message)


def polynomial_record(expression):
    poly = s.Poly(s.expand(expression), *VARIABLES)
    return {"degree": int(poly.total_degree()),
            "terms": [{"powers": list(m), "coefficient": int(c)}
                      for m, c in poly.terms()]}


def main():
    A = s.zeros(4)
    for i in range(4):
        others = [j for j in range(4) if j not in (i, SIGMA[i])]
        a, b = VARIABLES[2*i:2*i+2]
        A[i, SIGMA[i]] = a
        A[i, others[0]] = b
        A[i, others[1]] = 1-a-b
    determinant = s.expand(A.det(method='domain-ge'))
    require(s.Poly(determinant, *VARIABLES).total_degree() == 3,
            'row-stochastic determinant degree changed')
    adj = A.adjugate()
    column_sums = [sum(adj[i, j] for i in range(4)) for j in range(4)]
    # Values of each ambient coordinate functional on the four contacts.
    coordinate_values = [(0, 2, 0, 0), (0, 1, 1, 0), (0, 1, 0, 1)]
    identities = []
    for axis, values in enumerate(coordinate_values):
        numerators = [sum(values[i]*adj[i, j] for i in range(4)) for j in range(4)]
        for j, k in itertools.combinations(range(4), 2):
            quotient = s.S.Zero
            for i, ell in itertools.combinations(range(4), 2):
                rows = [q for q in range(4) if q not in (j, k)]
                cols = [q for q in range(4) if q not in (i, ell)]
                minor = A.extract(rows, cols).det()
                quotient += (values[i]-values[ell])*(-1)**(i+ell+j+k)*minor
            quotient = s.expand(quotient)
            difference = numerators[j]*column_sums[k]-numerators[k]*column_sums[j]
            require(s.expand(difference-determinant*quotient) == 0,
                    'complementary minor identity failed')
            require(s.Poly(quotient, *VARIABLES).total_degree() <= 2,
                    'width quotient exceeds degree two')
            identities.append({"axis": axis, "vertex_pair": [j, k],
                               "quotient": polynomial_record(quotient)})
    result = {
        "status": "18_formal_complementary_minor_identities_passed",
        "variables": [str(v) for v in VARIABLES],
        "determinant": polynomial_record(determinant),
        "axis_width_quotients": identities,
        "pair_orientation": "j<k; reversing j,k negates the quotient",
        "vertex_difference_identity": "V_j[axis]-V_k[axis]=Q_axis,jk/(delta*r_j*r_k)",
        "definitions": {"delta": "det(A)>0", "r": "A^T*r=ones; r_j>0"},
        "cubic_model_variables": 13,
        "cubic_model_maximum_degree": 3,
        "scope": "Formal width identities and degree bounds; no feasibility or class-bound conclusion.",
    }
    (ROOT/'certificates/pair_cubic_width_identities.json').write_text(
        json.dumps(result, indent=2)+'\n')
    print('PASS: cubic determinant and 18 complementary-minor width identities; all quotients degree <=2')


if __name__ == '__main__':
    main()
