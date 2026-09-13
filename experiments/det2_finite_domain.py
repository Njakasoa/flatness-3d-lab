"""Exact finite-domain data for the determinant-two algebraic reduction."""
import json
from fractions import Fraction as F
from itertools import permutations, product
from math import gcd
from pathlib import Path


def require(value, message):
    if not value:
        raise ValueError(message)


def det3(a):
    return sum(a[0][i]*(a[1][(i+1)%3]*a[2][(i+2)%3]
                       - a[1][(i+2)%3]*a[2][(i+1)%3]) for i in range(3))


def main():
    p = [(0, 0, 0), (2, 1, 1), (0, 1, 0), (0, 0, 1)]
    B_inv = [[F(1, 2), F(0), F(0)], [-F(1, 2), F(1), F(0)],
             [-F(1, 2), F(0), F(1)]]
    maps = []
    for pi in permutations(range(4)):
        t = p[pi[0]]
        C = [[p[pi[j+1]][i]-t[i] for j in range(3)] for i in range(3)]
        U = [[sum(C[i][k]*B_inv[k][j] for k in range(3))
              for j in range(3)] for i in range(3)]
        require(all(x.denominator == 1 for row in U for x in row), 'noninteger map')
        U = [[int(x) for x in row] for row in U]
        require(abs(det3(U)) == 1, 'non-unimodular map')
        require(all(tuple(sum(U[i][k]*p[j][k] for k in range(3))+t[i]
                          for i in range(3)) == p[pi[j]] for j in range(4)),
                'incorrect contact permutation')
        maps.append({'permutation': list(pi), 'matrix': U, 'translation': list(t)})
    directions = []
    for u in product(range(-4, 5), range(-3, 4), range(-3, 4)):
        if not any(u) or next(v for v in u if v) < 0:
            continue
        if gcd(gcd(abs(u[0]), abs(u[1])), abs(u[2])) != 1:
            continue
        values = [sum(a*b for a, b in zip(u, q)) for q in p]
        if max(values)-min(values) <= 3:
            directions.append(list(u))
    require(len(directions) == 37, 'unexpected direction count')
    threshold = F(17, 5)
    A_upper = F(13, 6)
    require((A_upper-1)**2 > F(4, 3), 'invalid radical upper bound')
    lam = 1-A_upper/threshold
    vol = 1/lam**3
    require(lam == F(37, 102) and vol < 21, 'invalid volume bound')
    record = {
        'status': 'exact_finite_domain_data',
        'scope': 'Data for the written necessary model; not an infeasibility certificate.',
        'threshold': str(threshold), 'contacts': p,
        'planar_flatness_strict_upper': str(A_upper),
        'difference_minimum_strict_lower': str(lam),
        'volume_strict_upper': str(vol), 'gap_to_volume_21': str(21-vol),
        'closed_barycentric_bounds': [-62, 63],
        'additional_ambient_vertex_bounds': {'Y': [-62, 63], 'Z': [-62, 63]},
        'complete_hollow_integer_box': [[-124, 126], [-62, 63], [-62, 63]],
        'complete_hollow_box_count': 251*126*126,
        'direction_enumeration_box': [[-4, 4], [-3, 3], [-3, 3]],
        'contact_width_cutoff': 3, 'direction_count': len(directions),
        'directions_modulo_sign': directions,
        'contact_permutation_maps': maps,
        'blocker_representatives': [[1, 0, 3, 2], [1, 2, 3, 0]],
    }
    path = Path(__file__).resolve().parents[1]/'certificates/det2_finite_domain.json'
    path.write_text(json.dumps(record, indent=2)+'\n')
    print('Exact finite domain: 37 directions, 24 lattice automorphisms, volume < 21.')


if __name__ == '__main__':
    main()
