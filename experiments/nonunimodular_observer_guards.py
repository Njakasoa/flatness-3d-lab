"""Exact gauge-truncated observer lines for the nine nonunimodular classes.

Only stdlib arithmetic is used. Line representatives come from Bezout
identities, not a bounded search. Geometric completeness is conditional on
the minimal-observer theorem in proofs/DET2_OBSERVER_LINES.md and the
contact-edge gauge hypotheses in proofs/DET2_OBSERVER_GAUGE_GUARDS.md.
"""
import itertools
import json
from fractions import Fraction as Q
from math import ceil, floor, gcd
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BETA = Q(37, 102)


def need(condition, message):
    if not condition:
        raise ValueError(message)


def dot(a, b):
    return sum(x * y for x, y in zip(a, b))


def sub(a, b):
    return tuple(x - y for x, y in zip(a, b))


def cross(a, b):
    return (a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2],
            a[0]*b[1]-a[1]*b[0])


def det(rows):
    return dot(rows[0], cross(rows[1], rows[2]))


def solve(rows, rhs):
    denominator = det(rows)
    need(denominator != 0, 'singular linear system')
    return tuple(Q(det([tuple(rhs[i] if j == column else rows[i][j]
                             for j in range(3)) for i in range(3)]), denominator)
                 for column in range(3))


def extended_gcd(a, b):
    """Return nonnegative g and signed x,y with a*x+b*y=g."""
    old_r, r, old_x, x, old_y, y = abs(a), abs(b), 1, 0, 0, 1
    while r:
        quotient = old_r // r
        old_r, r = r, old_r - quotient*r
        old_x, x = x, old_x - quotient*x
        old_y, y = y, old_y - quotient*y
    return old_r, old_x * (-1 if a < 0 else 1), old_y * (-1 if b < 0 else 1)


def bezout(v):
    g, a, b = extended_gcd(v[0], v[1])
    h, c, d = extended_gcd(g, v[2])
    need(h == 1, 'nonprimitive contact edge')
    s = (c*a, c*b, d)
    need(dot(s, v) == 1, 'Bezout identity')
    return s


def canonical_sign(v):
    return v if next(x for x in v if x) > 0 else tuple(-x for x in v)


def barycentric(points, z):
    columns = [sub(p, points[0]) for p in points[1:]]
    rows = list(zip(*columns))
    tail = solve(rows, sub(z, points[0]))
    return (1-sum(tail),) + tail


def width_one_normals(points):
    # Flip a width-one normal if necessary to put p0 at the lower level.
    # All remaining vertex differences then belong to {0,1}.
    rows = [sub(p, points[0]) for p in points[1:]]
    normals = set()
    for values in itertools.product((0, 1), repeat=3):
        if not any(values):
            continue
        u = solve(rows, values)
        if any(x.denominator != 1 for x in u):
            continue
        u = canonical_sign(tuple(map(int, u)))
        need(gcd(*u) == 1, 'width-one normal is primitive')
        normals.add(u)
    need(1 <= len(normals) <= 3, 'nonunimodular empty tetrahedron slabs')
    return sorted(normals)


def build_class(class_index, vertices):
    points = tuple(map(tuple, vertices))
    volume = abs(det([sub(p, points[0]) for p in points[1:]]))
    need(volume > 1, 'this theorem excludes the unimodular case')
    box = [(min(p[j] for p in points), max(p[j] for p in points))
           for j in range(3)]
    integer_points = [z for z in itertools.product(*(range(lo, hi+1) for lo, hi in box))
                      if min(barycentric(points, z)) >= 0]
    need(set(integer_points) == set(points), 'contact hull is not empty')
    edges = sorted({canonical_sign(sub(points[j], points[i]))
                    for i, j in itertools.combinations(range(4), 2)})
    need(len(edges) == 6 and all(gcd(*v) == 1 for v in edges), 'six primitive edges')
    normals = width_one_normals(points)
    lines, guards = [], set()
    for u in normals:
        levels = sorted({dot(u, p) for p in points})
        need(len(levels) == 2 and levels[1]-levels[0] == 1, 'width-one slab')
        for level in levels:
            ids = [i for i, p in enumerate(points) if dot(u, p) == level]
            opposite = [i for i in range(4) if i not in ids]
            need(len(ids) == 2 and len(opposite) == 2, 'two-plus-two slab')
            pa, pb = (points[i] for i in ids)
            v = sub(pb, pa)
            s = bezout(v)
            for sign in (-1, 1):
                target = tuple(sign*x for x in u)
                r = cross(target, s)
                q0 = tuple(a+b for a, b in zip(pa, r))
                need(cross(v, r) == target and dot(u, r) == 0, 'plane basis identity')
                w = sub(points[opposite[1]], points[opposite[0]])
                component = next(i for i, x in enumerate(target) if x)
                d = Q(cross(v, w)[component], target[component])
                if d < 0:
                    w = tuple(-x for x in w)
                    d = -d
                need(d == volume, 'opposite-edge determinant identity')
                component = next(i for i, x in enumerate(v) if x)
                a = Q(w[component]-volume*r[component], v[component])
                need(a.denominator == 1, 'integral plane coordinate')
                a = int(a)
                need(w == tuple(a*x+volume*y for x, y in zip(v, r)), 'w = a*v+d*r')
                need(gcd(a, volume) == 1, 'primitive opposite edge coordinates')
                lower = Q(a, volume)+1-Q(volume+1, volume)/BETA
                upper = Q(a, volume)+Q(volume+1, volume)/BETA
                parameters = list(range(floor(lower)+1, ceil(upper)))
                need(len(parameters) <= 8, 'general eight-points-per-line bound')
                retained = []
                for t in parameters:
                    rho = max(Q(1), Q(abs(volume*t-a), volume+1),
                              Q(abs(volume*(t-1)-a), volume+1))
                    need(rho < 1/BETA, 'strict gauge interval')
                    z = tuple(q+t*x for q, x in zip(q0, v))
                    need(dot(u, z) == level and cross(v, sub(z, pa)) == target,
                         'retained line point')
                    need(z not in points, 'observer cannot be a contact')
                    retained.append(z)
                    guards.add(z)
                # Explicitly certify the two nearest excluded integer endpoints.
                for t in (parameters[0]-1, parameters[-1]+1):
                    rho = max(Q(1), Q(abs(volume*t-a), volume+1),
                              Q(abs(volume*(t-1)-a), volume+1))
                    need(rho >= 1/BETA, 'excluded parameter endpoint')
                lines.append({'normal': u, 'level': level, 'contact_indices': ids,
                              'cross_sign': sign, 'primitive_direction': v,
                              'bezout_vector': s, 'plane_basis_second_vector': r,
                              'base_point': q0, 'opposite_edge': w,
                              'opposite_edge_coordinates': [a, volume],
                              'open_parameter_interval': [str(lower), str(upper)],
                              'integer_parameters': parameters, 'points': retained})
    need(len(lines) == 4*len(normals), 'four lines per slab')
    need(len(guards) <= 96, 'general finite-guard upper bound')
    used_edges = sorted({canonical_sign(tuple(line['primitive_direction']))
                         for line in lines})
    return {'class_index': class_index, 'contact_points': points,
            'normalized_volume': volume, 'integer_points_in_contact_hull': integer_points,
            'primitive_contact_edge_directions': edges, 'width_one_normals': normals,
            'gauge_directions_used_by_truncation': used_edges,
            'line_count': len(lines), 'lines': lines,
            'point_occurrences': sum(len(line['points']) for line in lines),
            'guard_count': len(guards), 'guards': sorted(guards)}


def build():
    source = json.loads((ROOT/'certificates/contact_templates.json').read_text())
    classes = []
    for entry in source['embeddings']:
        vertices = entry['vertices']
        if len(vertices) != 4:
            continue
        d = abs(det([sub(p, vertices[0]) for p in vertices[1:]]))
        if d > 1:
            classes.append(build_class(entry['class_index'], vertices))
    need(len(classes) == 9, 'nine nonunimodular tetrahedral contact classes')
    return {'status': 'exact_generic_nonunimodular_observer_guard_enumeration',
            'beta': str(BETA), 'class_count': len(classes),
            'hypotheses': ['K is compact, convex, and full dimensional',
                           'P is contained in K and its four vertices lie on the boundary of K',
                           'gamma_(K-K)(v) > 37/102 for every primitive contact-edge direction'],
            'construction': 'Complete binary vertex-value slab enumeration; integer Bezout plane bases; strict rational gauge truncation',
            'theorem_dependencies': ['proofs/DET2_OBSERVER_LINES.md',
                                     'proofs/DET2_OBSERVER_GAUGE_GUARDS.md'],
            'scope': 'Under the hypotheses, K is hollow if and only if its interior excludes the listed guards. No width bound or infeasibility is asserted.',
            'classes': classes}


def main():
    data = build()
    output = ROOT/'certificates/nonunimodular_observer_guards.json'
    output.write_text(json.dumps(data, indent=2)+'\n')
    for entry in data['classes']:
        print(json.dumps({key: entry[key] for key in
                          ('class_index', 'normalized_volume', 'width_one_normals',
                           'line_count', 'point_occurrences', 'guard_count')}))


if __name__ == '__main__':
    main()
