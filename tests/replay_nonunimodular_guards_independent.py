"""Independent stdlib verification of generic observer-guard certificates.

The published classification and written observer theorem remain external
geometric inputs. This checks exact coverage, emptiness, bases and cutoffs.
"""
from copy import deepcopy
from fractions import Fraction as Q
from itertools import product, combinations
from math import gcd, floor, ceil
from pathlib import Path
import json
from replay_det13_contraction_independent import need, solve

ROOT = Path(__file__).resolve().parents[1]


def sub(x,y):
    return tuple(a-b for a,b in zip(x,y))


def dot(x,y):
    return sum(a*b for a,b in zip(x,y))


def cross(x,y):
    return (x[1]*y[2]-x[2]*y[1],x[2]*y[0]-x[0]*y[2],x[0]*y[1]-x[1]*y[0])


def canonical(v):
    return v if next(x for x in v if x) > 0 else tuple(-x for x in v)


def verify(data):
    source = json.loads((ROOT/'certificates/contact_templates.json').read_text())
    need(data['class_count'] == len(data['classes']) == 9, 'nine classes')
    beta = Q(data['beta'])
    need(beta == Q(37,102), 'fixed threshold')
    counts = []
    for C,original in zip(data['classes'],source['embeddings'][1:10]):
        P = list(map(tuple,original['vertices']))
        need(C['class_index'] == original['class_index'], 'source class index')
        need(list(map(tuple,C['contact_points'])) == P, 'source contacts')
        edge_rows = [sub(p,P[0]) for p in P[1:]]
        d = abs(dot(edge_rows[0],cross(edge_rows[1],edge_rows[2])))
        need(C['normalized_volume'] == d and d > 1, 'normalized volume')
        affine = [[1]*4]+[[p[k] for p in P] for k in range(3)]
        box = [range(min(p[k] for p in P),max(p[k] for p in P)+1) for k in range(3)]
        lattice = [z for z in product(*box) if min(solve(affine,[1,*z])) >= 0]
        need(set(lattice) == set(P), 'closed-empty tetrahedron')
        need(list(map(tuple,C['integer_points_in_contact_hull'])) == lattice, 'archived emptiness')
        normals = set()
        for values in product((0,1),repeat=3):
            if not any(values):
                continue
            u = solve(edge_rows,values)
            if all(x.denominator == 1 for x in u):
                normals.add(canonical(tuple(map(int,u))))
        need(1 <= len(normals) <= 3 and set(map(tuple,C['width_one_normals'])) == normals, 'all binary-height slabs')
        edges = {canonical(sub(P[j],P[i])) for i,j in combinations(range(4),2)}
        need(all(gcd(*v) == 1 for v in edges), 'primitive edges')
        need(set(map(tuple,C['primitive_contact_edge_directions'])) == edges, 'all edge hypotheses')
        required = {(u,h,s) for u in normals for h in set(dot(u,p) for p in P) for s in (-1,1)}
        seen, guards, used = set(),set(),set()
        occurrences = 0
        for L in C['lines']:
            u,h,s = tuple(L['normal']),L['level'],L['cross_sign']
            key = (u,h,s)
            need(key in required and key not in seen, 'one line for each required side')
            seen.add(key)
            ids = [i for i,p in enumerate(P) if dot(u,p) == h]
            need(ids == L['contact_indices'] and len(ids) == 2, 'two contacts in each layer')
            pa,pb = (P[i] for i in ids)
            v = sub(pb,pa)
            need(tuple(L['primitive_direction']) == v, 'line direction')
            q0 = tuple(L['base_point']); r = sub(q0,pa)
            need(all(isinstance(x,int) for x in q0), 'integer line representative')
            need(dot(u,q0) == h and cross(v,r) == tuple(s*x for x in u), 'unimodular plane basis')
            need(tuple(L['plane_basis_second_vector']) == r, 'recorded plane basis')
            need(dot(v,L['bezout_vector']) == 1, 'Bezout identity')
            others = [i for i in range(4) if i not in ids]
            w = tuple(L['opposite_edge'])
            w0 = sub(P[others[1]],P[others[0]])
            need(w == w0 or w == tuple(-x for x in w0), 'opposite edge orientation')
            # Recover plane coordinates by solving against any independent
            # two coordinate rows, independently of the generator's choice.
            pair = next((i,j) for i,j in combinations(range(3),2) if v[i]*r[j]-v[j]*r[i])
            a,dd = solve([[v[k],r[k]] for k in pair],[w[k] for k in pair])
            need(dd == d and a.denominator == 1, 'plane coordinates')
            need(w == tuple(a*x+dd*y for x,y in zip(v,r)), 'full plane identity')
            need(list(map(Q,L['opposite_edge_coordinates'])) == [a,dd], 'archived plane coordinates')
            left,right = a/d+1-Q(d+1,d)/beta,a/d+Q(d+1,d)/beta
            need(list(map(Q,L['open_parameter_interval'])) == [left,right], 'strict endpoints')
            params = list(range(floor(left)+1,ceil(right)))
            need(params == L['integer_parameters'] and len(params) <= 8, 'complete integer interval')
            points = [tuple(q+t*x for q,x in zip(q0,v)) for t in params]
            need(list(map(tuple,L['points'])) == points, 'line points')
            guards.update(points); used.add(canonical(v)); occurrences += len(points)
        need(seen == required and C['line_count'] == len(required), 'complete line coverage')
        need(C['point_occurrences'] == occurrences, 'occurrence count')
        need(set(map(tuple,C['gauge_directions_used_by_truncation'])) == used, 'needed edge directions')
        need(list(map(tuple,C['guards'])) == sorted(guards), 'complete guard union')
        need(C['guard_count'] == len(guards) <= 96, 'guard bound')
        counts.append(len(guards))
    need(counts == [64,48,40,40,20,20,20,20,20], 'nine exact counts')
    old = json.loads((ROOT/'certificates/det2_observer_gauge_guards.json').read_text())
    need(set(map(tuple,data['classes'][0]['guards'])) == {tuple(r['point']) for r in old['guards']}, 'det2 independent certificate cross-check')
    return {'class_count':9,'guard_counts':counts,'line_counts':[r['line_count'] for r in data['classes']]}


def main():
    data = json.loads((ROOT/'certificates/nonunimodular_observer_guards.json').read_text())
    result = verify(data)
    mutations = [
        lambda d: d.__setitem__('beta','1/3'),
        lambda d: d['classes'].pop(),
        lambda d: d['classes'][8]['width_one_normals'].pop(),
        lambda d: d['classes'][8]['lines'].pop(),
        lambda d: d['classes'][8]['lines'][0]['base_point'].__setitem__(0,99),
        lambda d: d['classes'][8]['lines'][0]['opposite_edge_coordinates'].__setitem__(1,12),
        lambda d: d['classes'][8]['lines'][0]['open_parameter_interval'].__setitem__(0,'0'),
        lambda d: d['classes'][8]['lines'][0]['integer_parameters'].pop(),
        lambda d: d['classes'][8]['guards'].pop(),
        lambda d: d['classes'][8]['gauge_directions_used_by_truncation'].pop(),
    ]
    for mutate in mutations:
        bad = deepcopy(data); mutate(bad)
        try:
            verify(bad)
        except (ValueError,KeyError,IndexError,TypeError,StopIteration):
            continue
        raise ValueError('corrupted guard certificate was accepted')
    print(json.dumps({'status':'PASS',**result,'rejected_mutations':len(mutations)}))


if __name__ == '__main__':
    main()
