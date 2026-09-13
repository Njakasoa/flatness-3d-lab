"""Stdlib-only d5a2 direction, symmetry, and vertex-bound arithmetic audit.
No experiment, solver, or existing certificate imports. Writes a fresh receipt.
"""
from fractions import Fraction as Q
from itertools import permutations, product
from math import gcd
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
P = ((0, 0, 0), (5, 1, 2), (0, 1, 0), (0, 0, 1))
BETA = Q(183, 500)
TARGET = Q(17, 5)


def dot(a, b):
    return sum(x * y for x, y in zip(a, b))


def canonical(u):
    return tuple(-x for x in u) if next(x for x in u if x) < 0 else tuple(u)


def width(u):
    h = [dot(u, p) for p in P]
    return max(h) - min(h)


def inverse(A):
    n = len(A)
    M = [[Q(x) for x in row] + [Q(i == j) for j in range(n)] for i, row in enumerate(A)]
    for i in range(n):
        k = next(k for k in range(i, n) if M[k][i])
        M[i], M[k] = M[k], M[i]
        divisor = M[i][i]
        M[i] = [x / divisor for x in M[i]]
        for k in range(n):
            if k != i:
                factor = M[k][i]
                M[k] = [x - factor * y for x, y in zip(M[k], M[i])]
    return [row[n:] for row in M]


def det3(A):
    return sum(A[0][j] * (A[1][(j + 1) % 3] * A[2][(j + 2) % 3] - A[1][(j + 2) % 3] * A[2][(j + 1) % 3]) for j in range(3))


def verify():
    # |u2|,|u3|<=3 and |5u1+u2+2u3|<=3 imply |u1|<=2.
    directions = sorted({canonical(u) for u in product(range(-2, 3), range(-3, 4), range(-3, 4))
                         if any(u) and gcd(*u) == 1 and width(u) <= 3})
    assert len(directions) == 15
    base_inverse = inverse([[P[j + 1][i] for j in range(3)] for i in range(3)])
    group = []
    for perm in permutations(range(4)):
        t = P[perm[0]]
        differences = [[P[perm[j + 1]][i] - t[i] for j in range(3)] for i in range(3)]
        A = [[sum(differences[i][k] * base_inverse[k][j] for k in range(3)) for j in range(3)] for i in range(3)]
        if any(x.denominator != 1 for row in A for x in row):
            continue
        A = [[int(x) for x in row] for row in A]
        assert abs(det3(A)) == 1
        assert all(tuple(dot(row, P[j]) + t[i] for i, row in enumerate(A)) == P[perm[j]] for j in range(4))
        group.append({'permutation': perm, 'matrix': A, 'translation': t})
    assert len(group) == 4
    remaining = set(directions)
    orbits = []
    while remaining:
        u = min(remaining)
        orbit = sorted({canonical(tuple(sum(g['matrix'][i][j] * u[i] for i in range(3)) for j in range(3))) for g in group})
        assert set(orbit) <= remaining
        assert all(width(v) == width(u) for v in orbit)
        remaining -= set(orbit)
        orbits.append({'directions': orbit, 'contact_width': width(u)})
    assert sorted(len(o['directions']) for o in orbits) == [1, 2, 4, 4, 4]
    # Generic convex-body counterexamples to dropping any one direction.
    witnesses = []
    for u in directions:
        pivot = next(i for i in range(3) if u[i])
        basis = []
        for j in range(3):
            if j != pivot:
                a = [0, 0, 0]
                a[j], a[pivot] = u[pivot], -u[j]
                basis.append(a)
        assert all(dot(u, a) == 0 for a in basis)
        other_widths = [width(v) + 4 * sum(abs(dot(v, a)) for a in basis) for v in directions if v != u]
        assert min(other_widths) >= 4 > TARGET > width(u)
        witnesses.append({'omitted_direction': u, 'kernel_vectors': basis, 'width_in_omitted_direction': width(u), 'minimum_other_listed_width': min(other_widths)})
    R = 6 / (5 * BETA ** 3)
    assert R == Q(50000000, 2042829)
    bounds = []
    barycentric_corners = []
    for i, j in permutations(range(4), 2):
        lam = [Q(0)] * 4
        lam[i], lam[j] = R, 1 - R
        assert sum(lam) == 1 and sum(max(x, 0) for x in lam) == R
        barycentric_corners.append(tuple(sum(lam[k] * P[k][axis] for k in range(4)) for axis in range(3)))
    for axis, m in enumerate((5, 1, 2)):
        lo, hi = min(v[axis] for v in barycentric_corners), max(v[axis] for v in barycentric_corners)
        assert (lo, hi) == (-m * (R - 1), m * R)
        bounds.append({'coordinate': 'xyz'[axis], 'strict_lower': str(lo), 'strict_upper': str(hi)})
    return {'status': 'PASS', 'scope': 'Exact contact geometry and necessary bounds only; no class exclusion or solver result.',
            'contact_points': P, 'target': str(TARGET), 'beta': str(BETA), 'directions': directions,
            'affine_lattice_group': group, 'direction_orbits': orbits,
            'generic_convexity_nonredundancy_witnesses': witnesses,
            'nonredundancy_scope': 'Bodies contain P but need not be hollow or realize P as relint facet contacts.',
            'positive_barycentric_mass_strict_upper': str(R), 'vertex_coordinate_bounds': bounds}


def main():
    result = verify()
    path = ROOT / 'results/det5_complete_geometry_validation.json'
    path.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({'status': result['status'], 'direction_count': len(result['directions']), 'orbit_count': len(result['direction_orbits'])}))


if __name__ == '__main__':
    main()
