"""Exact hollow tetrahedron with four index-two contacts and width > 13/4.

This is one witness, not an optimum for the determinant-two class.
"""
import json
import sys
from fractions import Fraction as F
from pathlib import Path

from src.exact import Q, inverse
from src.geometry import Polytope, certify_hollow, certify_width


def main():
    if sys.flags.optimize:
        raise SystemExit('Exact assertions required; do not use -O/-OO')
    t = list(map(F, ['5/28', '1/2', '1/1000', '13/23',
                     '1/1000', '3/4', '7/26', '2/3']))
    A = [[Q() for _ in range(4)] for _ in range(4)]
    for i in range(4):
        x, y = t[2*i:2*i+2]
        a = (1+x)/2
        r = 1-a
        A[i][(i+1)%4] = Q(a)
        A[i][(i+2)%4] = Q(r*y)
        A[i][(i+3)%4] = Q(r*(1-y))
    assert all(A[i][i] == 0 and sum(A[i], Q()) == 1
               and all(A[i][j] > 0 for j in range(4) if j != i)
               for i in range(4))
    Ai = inverse(A)
    r = [sum((Ai[i][j] for i in range(4)), Q()) for j in range(4)]
    assert min(r) > 0
    contacts = [[0, 0, 0], [2, 1, 1], [0, 1, 0], [0, 0, 1]]
    vertices = [[sum((contacts[i][k]*Ai[i][j] for i in range(4)), Q())/r[j]
                 for k in range(3)] for j in range(4)]
    K = Polytope(vertices)
    hollow = certify_hollow(K)
    width = certify_width(K)
    assert hollow['hollow']
    assert sorted(map(tuple, hollow['boundary_points'])) == sorted(map(tuple, contacts))
    assert F(width['width']['a']) > F(13, 4) and F(width['width']['b']) == 0
    result = {
        'status': 'exact_rational_reconstruction',
        'source_row': 'fixed_small_rational_four_contact_witness',
        'scope': 'One tetrahedron with exactly four index-two facet contacts; no optimum claim.',
        'parameters': list(map(str, t)),
        'facet_matrix': [[str(x.a) for x in row] for row in A],
        'vertices': K.json(), 'hollow': hollow, 'width': width,
    }
    path = Path(__file__).resolve().parents[1]/'certificates/det2_four_contacts.json'
    path.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({'width': width['width'],
                      'boundary_points': hollow['boundary_points'],
                      'integer_box': hollow['integer_box']}, indent=2))


if __name__ == '__main__':
    main()
