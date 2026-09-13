"""Standalone Fraction replay; imports neither the generator nor src geometry.

Run python3 tests/replay_det2_pair_column_independent.py. No solver is used.
The direction box is independently derived from an exact edge inverse.
"""
from copy import deepcopy
from fractions import Fraction as Q
from itertools import permutations, product
from math import ceil, floor, gcd
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]


def need(condition, message):
    if not condition:
        raise ValueError(message)


def rational(value):
    if isinstance(value, dict):
        need(Q(value['b']) == 0, 'nonrational field')
        return Q(value['a'])
    return Q(value)


def dot(a, b):
    return sum((x*y for x, y in zip(a, b)), Q())


def determinant(a):
    n = len(a)
    answer = Q()
    for p in permutations(range(n)):
        term = Q((-1)**sum(p[i] > p[j] for i in range(n) for j in range(i+1, n)))
        for i in range(n):
            term *= a[i][p[i]]
        answer += term
    return answer


def inverse(a):
    n = len(a)
    b = [list(row)+[Q(i == j) for j in range(n)] for i, row in enumerate(a)]
    for j in range(n):
        pivot = next((i for i in range(j, n) if b[i][j]), None)
        need(pivot is not None, 'singular matrix')
        b[j], b[pivot] = b[pivot], b[j]
        scale = b[j][j]
        b[j] = [x/scale for x in b[j]]
        for i in range(n):
            if i != j:
                scale = b[i][j]
                b[i] = [x-scale*y for x, y in zip(b[i], b[j])]
    return [row[n:] for row in b]


def lam(point):
    x, y, z = map(Q, point)
    return [1+x/2-y-z, x/2, y-x/2, z-x/2]


def verify(data, *, expected_boundary_count):
    e = data['exact']
    f = [[rational(x) for x in row] for row in e['F']]
    need(len(f) == 4 and all(len(row) == 4 for row in f), 'F shape')
    need(all(f[i][i] == 0 for i in range(4)), 'diagonal')
    need(all(f[i][j] > 0 for i in range(4) for j in range(4) if i != j), 'offdiagonal positivity')
    need(all(sum(f[i][j] for i in range(4)) == 1 for j in range(4)), 'column sums')
    p = list(map(Q, e['parameters']))
    need(len(p) == 8, 'parameter count')
    c0,d0,c1,d1,c2,d2,c3,d3 = p
    need(f == [[0,c1,d2,d3],[c0,0,1-c2-d2,1-c3-d3],
               [d0,d1,0,c3],[1-c0-d0,1-c1-d1,c2,0]], 'parameter reconstruction')
    sig = [1,0,3,2]
    slack = [2*f[i][sig[i]]-sum(f[i]) for i in range(4)]
    need(all(x > 0 for x in slack), 'strict pair dominance')
    need(slack == list(map(rational, e['row_pair_dominance'])), 'dominance claims')
    need(e['row_pair_dominance_equalities'] == [], 'dominance equality claim')
    need(sum(f[i][sig[i]] for i in range(4)) > 2, 'designated sum')
    det = determinant(f)
    need(det > 0 and det == rational(e['determinant']), 'determinant')
    inv = inverse(f)
    vertices = [(2*inv[1][j],inv[1][j]+inv[2][j],inv[1][j]+inv[3][j]) for j in range(4)]
    need(vertices == [tuple(map(rational, v)) for v in e['vertices']], 'vertices')
    for j, v in enumerate(vertices):
        need([dot(row, lam(v)) for row in f] == [Q(i == j) for i in range(4)], 'vertex slacks')
    edges = [[vertices[i][j]-vertices[0][j] for j in range(3)] for i in range(1,4)]
    volume = abs(determinant(edges))/6
    need(volume == 1/(3*det) == rational(e['volume']), 'volume')
    contacts = [(0,0,0),(2,1,1),(0,1,0),(0,0,1)]
    need(contacts == list(map(tuple,e['contact_points'])), 'contacts')
    contact_det = abs(determinant([[Q(contacts[i][j]-contacts[0][j]) for j in range(3)] for i in range(1,4)]))
    need(contact_det == 2, 'designated contact index')
    if expected_boundary_count == 5:
        q = (-1,1,0)
        alternate_det = abs(determinant([[Q(contacts[i][j]-q[j]) for j in range(3)] for i in range(1,4)]))
        need(alternate_det == 1, 'alternate unimodular contacts')
    for j, v in enumerate(contacts):
        values = [dot(row,lam(v)) for row in f]
        need(values[j] == 0 and all(values[i] > 0 for i in range(4) if i != j), 'contact relative interior')
    need(e['designated_contact_relative_interior'] == [True]*4, 'contact claims')
    box = [[ceil(min(v[j] for v in vertices)),floor(max(v[j] for v in vertices))] for j in range(3)]
    boundary, interior = [], []
    count = 0
    for z in product(*(range(a,b+1) for a,b in box)):
        count += 1
        values = [dot(row,lam(z)) for row in f]
        if all(x > 0 for x in values):
            interior.append(z)
        elif all(x >= 0 for x in values):
            boundary.append(z)
    h = e['hollow']
    need(not interior and h['hollow'] is True and h['interior_points'] == [], 'hollowness')
    need(box == h['integer_box'] and count == h['points_checked'], 'complete integer box')
    need(len(boundary) == expected_boundary_count == e['boundary_count'], 'boundary count')
    if expected_boundary_count == 4:
        need(set(boundary) == set(contacts), 'exactly four designated contacts')
        need(dot(f[0],lam((-1,1,0))) == -Q(1,2000000), 'fifth point strictly outside')
        need(min(slack) == Q(501,1000000), 'four-contact minimum surplus')
    need(boundary == list(map(tuple,h['boundary_points'])) == list(map(tuple,e['boundary_points'])), 'boundary points')
    # Check the independent facet data against actual vertices and lattice points.
    need(len(h['facets']) == 4, 'facet count')
    face_ids = set()
    for face in h['facets']:
        n = list(map(rational,face['normal'])); b = rational(face['offset'])
        need(any(n), 'zero facet normal')
        values = [b-dot(n,v) for v in vertices]
        ids = tuple(i for i,x in enumerate(values) if x == 0)
        need(len(ids) == 3 and all(x >= 0 for x in values), 'facet support')
        need(list(ids) == face['vertex_ids'], 'facet vertex ids')
        face_ids.add(ids)
        points = [z for z in boundary if dot(n,z) == b]
        relint = [z for z in points if sum(dot(row,lam(z)) == 0 for row in f) == 1]
        need(points == list(map(tuple,face['lattice_contacts'])), 'facet lattice contacts')
        need(relint == list(map(tuple,face['relative_interior_contacts'])), 'facet relative interior contacts')
    need(len(face_ids) == 4, 'duplicate facets')
    def width(u):
        values = [dot(u,v) for v in vertices]
        return max(values)-min(values)
    # Any minimizer has width <= this exhibited axis upper bound W.
    # With q_i=u.(v_i-v_0), |q_i|<=W and u=edges^{-1}q;
    # hence |u_j|<=W sum_i |edges^{-1}_{ji}|. Integer floors give
    # a complete search box, without relying on supplied search metadata.
    upper = min(width(u) for u in [(1,0,0),(0,1,0),(0,0,1)])
    edge_inv = inverse(edges)
    bounds = [floor(upper*sum(map(abs,row))) for row in edge_inv]
    directions = [u for u in product(*(range(-b,b+1) for b in bounds))
                  if any(u) and next(x for x in u if x) > 0 and gcd(*u) == 1]
    scores = [(width(u),u) for u in directions]
    minimum = min(w for w,u in scores)
    minimizers = sorted(u for w,u in scores if w == minimum)
    w = e['width']; search = w['search_bound']
    need(minimum == rational(w['width']) and minimum > Q(19,6), 'complete width')
    need(e['width_threshold'] == '19/6', 'threshold')
    need(minimizers == sorted(map(tuple,w['minimizing_directions_mod_sign'])), 'minimizers')
    need(len(directions) == w['direction_count'], 'direction count')
    need(upper == rational(search['initial_upper']), 'initial upper')
    need(bounds == search['coordinate_bounds'], 'direction bounds')
    need(search['basis_vertex_ids'] == [0,1,2,3], 'edge basis ids')
    need(edge_inv == [list(map(rational,row)) for row in search['D_inverse']], 'edge inverse')
    upper_claim = w['upper_certificate']
    need(tuple(upper_claim['direction']) in minimizers and rational(upper_claim['value']) == minimum, 'upper certificate')
    need(w['lower_certificate']['all_box_directions_checked'] is True and rational(w['lower_certificate']['checked_minimum']) == minimum, 'lower certificate')
    return {'width':str(minimum),'volume':str(volume),'integer_points':count,
            'primitive_directions_mod_sign':len(directions),'boundary_points':boundary}


def main():
    five = json.loads((ROOT/'certificates/det2_pair_column.json').read_text())
    four = json.loads((ROOT/'certificates/det2_pair_four_contacts.json').read_text())
    p5 = list(map(Q, five['exact']['parameters']))
    p4 = list(map(Q, four['exact']['parameters']))
    expected = list(p5)
    expected[2] += Q(1,1000000)
    need(p4 == expected, 'exact one-parameter perturbation')
    need(rational(five['exact']['width']['width']) == Q(3731889842479498000000,1172185068224586160791), 'five-contact identity')
    need(rational(four['exact']['width']['width']) == Q(932976210619799500000,293047542170915539223), 'four-contact identity')
    # Each mutation must independently be rejected, including geometrically
    # significant fields and evidence defining the complete finite searches.
    mutations = [
        ('entry', lambda e: e['F'][0].__setitem__(1,'1/2')),
        ('zero offdiagonal', lambda e: e['F'][0].__setitem__(3,'0')),
        ('vertex', lambda e: e['vertices'][0][0].__setitem__('a','0')),
        ('volume', lambda e: e['volume'].__setitem__('a','1')),
        ('determinant', lambda e: e['determinant'].__setitem__('a','1')),
        ('width', lambda e: e['width']['width'].__setitem__('a','4')),
        ('direction bound', lambda e: e['width']['search_bound']['coordinate_bounds'].__setitem__(2,5)),
        ('integer box', lambda e: e['hollow']['integer_box'][0].__setitem__(0,-3)),
        ('boundary', lambda e: e['boundary_points'].pop()),
        ('contact', lambda e: e['contact_points'][0].__setitem__(0,1)),
        ('facet', lambda e: e['hollow']['facets'][0]['offset'].__setitem__('a','0')),
        ('dominance', lambda e: e['row_pair_dominance'][3].__setitem__('a','0')),
    ]
    reports = {}
    for label, data, count in [('five_contacts',five,5),('four_contacts',four,4)]:
        report = verify(data, expected_boundary_count=count)
        for name, change in mutations:
            changed = deepcopy(data)
            change(changed['exact'])
            try:
                verify(changed, expected_boundary_count=count)
            except ValueError:
                continue
            raise RuntimeError('mutation accepted: '+label+' '+name)
        report['mutations_rejected'] = len(mutations)
        reports[label] = report
    # Swapping the whole valid exact bodies must not silently change which
    # witness is being certified, even when all their internal fields agree.
    for data, wrong_count in [(five,4),(four,5)]:
        try:
            verify(data, expected_boundary_count=wrong_count)
        except ValueError:
            continue
        raise RuntimeError('whole-witness substitution accepted')
    reports['whole_witness_substitutions_rejected'] = 2
    print(json.dumps(reports,indent=2))


if __name__ == '__main__':
    main()
