"""Exact, stdlib-only check of the two-direction d5 counterexample.

Reconstructs the body from F and independently exhausts complete lattice boxes.
Neither solver output nor other project checkers are imported.
"""
from fractions import Fraction as Q
from itertools import product
from math import ceil, floor, gcd
from pathlib import Path
from copy import deepcopy
import hashlib
import json

ROOT = Path(__file__).resolve().parents[1]


def need(condition, message):
    if not condition:
        raise ValueError(message)


def inverse(matrix):
    n = len(matrix)
    a = [[Q(x) for x in row] + [Q(i == j) for j in range(n)]
         for i, row in enumerate(matrix)]
    for j in range(n):
        k = next(i for i in range(j, n) if a[i][j])
        a[j], a[k] = a[k], a[j]
        p = a[j][j]
        a[j] = [x / p for x in a[j]]
        for i in range(n):
            if i != j:
                p = a[i][j]
                a[i] = [x - p * y for x, y in zip(a[i], a[j])]
    return [row[n:] for row in a]


def dot(a, b):
    return sum(x * y for x, y in zip(a, b))


def mv(a, x):
    return [dot(row, x) for row in a]


def width(vertices, u):
    h = [dot(v, u) for v in vertices]
    return max(h) - min(h)


def canonical(v):
    return any(v) and next(x for x in v if x) > 0 and gcd(*v) == 1


def replay(data):
    source = ROOT / data['source']
    need(hashlib.sha256(source.read_bytes()).hexdigest() == data['source_sha256'],
         'source byte binding')
    original = json.loads(source.read_text())
    p = [[Q(x) for x in row] for row in data['contact_vertices']]
    need(p == [[0, 0, 0], [5, 1, 2], [0, 1, 0], [0, 0, 1]], 'contact template')
    f = [[Q(x) for x in row] for row in data['F']]
    need(all(f[i][i] == 0 for i in range(4)), 'facet diagonal')
    need(all(f[i][j] > 0 for i in range(4) for j in range(4) if i != j),
         'relative interior facet contacts')
    need(all(sum(f[i][j] for i in range(4)) == 1 for j in range(4)),
         'column stochasticity')
    fi = inverse(f)
    v = [[sum(p[i][k] * fi[i][j] for i in range(4)) for k in range(3)]
         for j in range(4)]
    need(v == [[Q(x) for x in row] for row in data['vertices']], 'body reconstruction')
    ov = [[Q(x['a']) for x in row] for row in original['body']['vertices']]
    permutations = {(0, 1, 2, 3), (1, 3, 0, 2), (2, 0, 3, 1), (3, 2, 1, 0)}
    need({tuple(a['permutation']) for a in data['automorphism_orbit']} == permutations,
         'four affine contact symmetries')
    for a in data['automorphism_orbit']:
        m, t, perm = a['linear'], a['translation'], a['permutation']
        mi = inverse(m)
        need(all(x.denominator == 1 for row in mi for x in row), 'unimodularity')
        need(all([x + y for x, y in zip(mv(m, p[i]), t)] == p[perm[i]]
                 for i in range(4)), 'affine contact action')
        pull = [sum((1, -1, -2)[j] * m[j][k] for j in range(3)) for k in range(3)]
        need(pull == a['pulled_U'] and width(ov, pull) == Q(a['U_width']),
             'exact direction-width orbit')
        ys = [Q(0)] * 4
        for i in range(4):
            ys[perm[i]] = dot(m[1], ov[i]) + t[1]
        need(a['Y_extrema'] == [ys.index(min(ys)), ys.index(max(ys))],
             'orbit Y extrema')
    m, t, perm = data['linear'], data['translation'], data['chosen_permutation']
    need(any(a['linear'] == m and a['translation'] == t and a['permutation'] == perm
             for a in data['automorphism_orbit']), 'selected symmetry')
    need(all(v[perm[i]] == [x + y for x, y in zip(mv(m, ov[i]), t)]
             for i in range(4)), 'transformed body binding')
    a = [[Q(1)] * 4] + [[p[i][k] for i in range(4)] for k in range(3)]
    ai = inverse(a)

    def bary(z, affine=False):
        return mv(f, mv(ai, [Q(int(affine)), *z]))

    bounds = [(ceil(min(x[k] for x in v)), floor(max(x[k] for x in v)))
              for k in range(3)]
    boundary = []
    count = 0
    for z in product(*(range(lo, hi + 1) for lo, hi in bounds)):
        count += 1
        c = bary(z, True)
        need(min(c) <= 0, 'hollowness')
        if min(c) == 0:
            boundary.append(z)
    y, u = width(v, (0, 1, 0)), width(v, (1, -1, -2))
    ys = [x[1] for x in v]
    extrema = [ys.index(min(ys)), ys.index(max(ys))]
    need(extrema == data['Y_extrema'] == [2, 0], 'Y extrema of witness')
    need(data['retained_Y_representatives'] == [[0, 1], [0, 3], [1, 0]],
         'retained Y charts')
    need(extrema not in data['retained_Y_representatives'] and
         data['lies_in_retained_Y_chart'] is False, 'reduced-chart limitation')
    need(y == Q(data['Y_width']) and u == Q(data['U_width']), 'two exact widths')
    need(y > Q(17, 5) and u > Q(17, 5), 'both requested directions wide')
    # For any direction whose width <= upper, |D u| <= upper componentwise.
    # The following finite inverse-frame box therefore includes every minimizer.
    upper = min(width(v, e) for e in [(1, 0, 0), (0, 1, 0), (0, 0, 1)])
    d = [[v[i][k] - v[0][k] for k in range(3)] for i in range(1, 4)]
    di = inverse(d)
    ub = [floor(upper * sum(map(abs, row))) for row in di]
    best = upper
    for z in product(*(range(-b, b + 1) for b in ub)):
        if canonical(z):
            best = min(best, width(v, z))
    need(best == Q(data['lattice_width']) and best < Q(17, 5), 'full lattice width')
    need(width(v, data['minimizing_width_direction']) == best, 'width witness')
    # Every z with gamma_(K-K)(z)<=1 lies in the coordinate difference box.
    # A minimum <1 found in that box is consequently the full lattice minimum.
    gb = [floor(max(x[k] for x in v) - min(x[k] for x in v)) for k in range(3)]
    minimum = Q(1)
    for z in product(*(range(-b, b + 1) for b in gb)):
        if canonical(z):
            minimum = min(minimum, sum(map(abs, bary(z))) / 2)
    need(minimum == Q(data['full_difference_minimum']) < 1, 'full gauge minimum')
    need(sum(map(abs, bary(data['minimizing_gauge_vector']))) / 2 == minimum,
         'gauge witness')
    need(minimum > Q(183, 500), 'strong rational gauge necessity')
    # min > 1-(1+2/sqrt(3))/(17/5): if h>0, h<2/sqrt(3) iff 3h^2<4.
    h = Q(17, 5) * (1 - minimum) - 1
    need(h <= 0 or 3 * h * h < 4, 'exact ACMS gauge necessity')
    return {'Y_width': str(y), 'U_width': str(u), 'lattice_width': str(best),
            'full_difference_minimum': str(minimum), 'integer_points_checked': count,
            'boundary_points': boundary, 'width_search_bounds': ub,
            'gauge_search_bounds': gb, 'Y_extrema': extrema,
            'lies_in_retained_Y_chart': False, 'solver_queries': 0}


def main():
    data = json.loads((ROOT / 'results/det5_joint_symmetry_witness.json').read_text())
    result = replay(data)
    for field in ('F', 'U_width', 'full_difference_minimum'):
        broken = deepcopy(data)
        if field == 'F':
            broken[field][0][1] = '0'
        else:
            broken[field] = '4'
        try:
            replay(broken)
        except (ValueError, StopIteration, ZeroDivisionError):
            continue
        raise ValueError('accepted corruption: ' + field)
    print(json.dumps({'status': 'PASS', **result, 'rejected_mutations': 3}, indent=2))


if __name__ == '__main__':
    main()
