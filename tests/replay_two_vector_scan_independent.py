"""Independent Gaussian/stdlib replay of all two-vector scan payloads.

Imports no generator or main geometry code. The continuous argument is a
written theorem; this verifier binds its exact inputs and finite search.
"""
from copy import deepcopy
from fractions import Fraction as Q
from itertools import product, combinations
from math import gcd
from pathlib import Path
import json
from replay_det13_contraction_independent import solve, need

ROOT = Path(__file__).resolve().parents[1]


def radical_sign(a, b):
    if not b:
        return (a > 0)-(a < 0)
    if not a:
        return (b > 0)-(b < 0)
    if (a > 0) == (b > 0):
        return 1 if a > 0 else -1
    comparison = (a*a > 3*b*b)-(a*a < 3*b*b)
    return comparison if a > 0 else -comparison


def read_bound(data):
    need(data['d'] == 3, 'radical field')
    return Q(data['a']), Q(data['b'])


def verify(data):
    source = json.loads((ROOT/'certificates/contact_templates.json').read_text())
    entries = source['embeddings'][:10]
    need(len(data['classes']) == data['class_count'] == 10, 'ten classes')
    counts = []
    below_c, below_candidate = [], []
    total_pairs = 0
    for record, original in zip(data['classes'], entries):
        P = original['vertices']
        need(record['class_index'] == original['class_index'], 'class index')
        need(record['contact_points'] == P, 'contact coordinates')
        matrix = [[1]*4]+[[p[k] for p in P] for k in range(3)]
        widths = [max(p[k] for p in P)-min(p[k] for p in P) for k in range(3)]
        need(record['coordinate_search_box'] == [[-w,w] for w in widths], 'complete box')
        normals = record['width_one_covector']
        need(all(isinstance(x,int) for x in normals) and gcd(*normals) == 1, 'integer covector')
        heights = [sum(x*y for x,y in zip(normals,p)) for p in P]
        need(max(heights)-min(heights) == 1, 'contact width one')
        eligible, primitive_count = [], 0
        for z in product(*(range(-w,w+1) for w in widths)):
            if not any(z) or next(x for x in z if x) < 0 or gcd(*z) != 1:
                continue
            primitive_count += 1
            row = solve(matrix, [0,*z])
            mass = sum(map(abs,row))/2
            if mass < 1 and all(row):
                eligible.append({'vector': list(z), 'positive_mass': str(mass),
                                 'difference_barycentrics': list(map(str,row))})
        need(record['primitive_vectors_up_to_sign_in_box'] == primitive_count, 'primitive count')
        need(record['eligible_vectors'] == eligible and record['eligible_vector_count'] == len(eligible), 'complete vector set')
        expected = {}
        for left,right in combinations(eligible,2):
            rows = [list(map(Q,e['difference_barycentrics'])) for e in (left,right)]
            codes = [[1 if rows[r][j] > 0 else -1 for r in range(2)] for j in range(4)]
            if len(set(map(tuple,codes))) != 4:
                continue
            m = min(abs(x) for row in rows for x in row)
            S = sum(Q(e['positive_mass']) for e in (left,right))
            D = m-S+2
            need(D > 0, 'positive bound denominator')
            expected[tuple(map(tuple,[left['vector'],right['vector']]))] = (rows,codes,m,S,D)
        pairs = record['all_eligible_pairs']
        need(record['distinct_code_pair_count'] == len(pairs) == len(expected), 'pair count')
        seen = set()
        previous_bound = None
        for pair in pairs:
            key = tuple(map(tuple,pair['vectors']))
            need(key in expected and key not in seen, 'pair coverage')
            seen.add(key)
            rows,codes,m,S,D = expected[key]
            need([list(map(Q,r)) for r in pair['difference_barycentrics']] == rows, 'pair coordinates')
            need(pair['column_sign_codes'] == codes, 'distinct sign codes')
            need(list(map(Q,pair['positive_masses'])) == [sum(map(abs,r))/2 for r in rows], 'pair masses')
            need(Q(pair['minimum_absolute_coefficient']) == m and Q(pair['mass_sum']) == S, 'loss constants')
            need(Q(pair['positive_bound_denominator']) == D, 'denominator')
            a,b = read_bound(pair['global_class_bound'])
            need((a,b) == ((m+2)/D,Q(4,3)/D), 'class bound formula')
            need(read_bound(pair['low_width_split']) == (2/D,Q(4,3)/D), 'low width split')
            c_test = radical_sign(a-Q(11,7), b-Q(22,21)) < 0
            candidate_test = radical_sign(a-2,b) <= 0 or radical_sign((a-2)**2+3*b*b-2,2*(a-2)*b) < 0
            need(pair['strictly_below_contact_threshold_11A_over_7'] == c_test, 'c comparison')
            need(pair['strictly_below_candidate_2_plus_sqrt2'] == candidate_test, 'candidate comparison')
            if previous_bound:
                need(radical_sign(a-previous_bound[0],b-previous_bound[1]) >= 0, 'exact pair ordering')
            previous_bound = (a,b)
        need(record['best_pair'] == (pairs[0] if pairs else None), 'selected minimum')
        if pairs:
            if pairs[0]['strictly_below_contact_threshold_11A_over_7']:
                below_c.append(record['class_index'])
            if pairs[0]['strictly_below_candidate_2_plus_sqrt2']:
                below_candidate.append(record['class_index'])
        counts.append(len(eligible))
        total_pairs += len(pairs)
    need(below_c == [9] and below_candidate == [8,9], 'specific exclusions')
    tenth = data['classes'][8]['best_pair']
    a,b = read_bound(tenth['global_class_bound'])
    need(radical_sign(a-Q(17,5),b) < 0, 'determinant ten below 17/5')
    need(data['floating_point_decisions'] is False, 'exact comparison scope')
    return {'eligible_vector_counts': counts, 'verified_pairs': total_pairs,
            'excluded_above_c': below_c, 'excluded_at_candidate': below_candidate}


def main():
    data = json.loads((ROOT/'results/two_vector_class_scan.json').read_text())
    result = verify(data)
    mutations = [
        lambda d: d['classes'].pop(),
        lambda d: d['classes'][8]['eligible_vectors'].pop(),
        lambda d: d['classes'][8]['all_eligible_pairs'].pop(),
        lambda d: d['classes'][8]['all_eligible_pairs'][0]['global_class_bound'].__setitem__('a','20/13'),
        lambda d: d['classes'][8]['all_eligible_pairs'][0]['difference_barycentrics'][0].__setitem__(0,'2/10'),
        lambda d: d['classes'][8]['all_eligible_pairs'][0].__setitem__('minimum_absolute_coefficient','2/10'),
        lambda d: d['classes'][8]['all_eligible_pairs'][0].__setitem__('strictly_below_contact_threshold_11A_over_7',True),
        lambda d: d['classes'][9]['all_eligible_pairs'][0]['column_sign_codes'][0].__setitem__(0,1),
        lambda d: d['classes'][9].__setitem__('best_pair',None),
        lambda d: d['classes'][8]['width_one_covector'].__setitem__(0,1),
    ]
    for mutate in mutations:
        damaged = deepcopy(data)
        mutate(damaged)
        try:
            verify(damaged)
        except (ValueError,KeyError,IndexError,TypeError):
            continue
        raise ValueError('corrupted scan was accepted')
    print(json.dumps({'status':'PASS', **result,'rejected_mutations':len(mutations)}))


if __name__ == '__main__':
    main()
