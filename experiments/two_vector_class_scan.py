"""Exact two-vector contraction scan of the ten contact tetrahedra.

The finite search is complete for primitive vectors with gamma_P(z)<1 and
nonzero difference barycentrics, up to sign. It asserts no optimality among
pairs outside this sublevel set, or among other contraction arguments.
The resulting width bounds use the separately reviewed contraction lemma
and the ACMS input; enumeration itself is not their geometric proof.
"""
from fractions import Fraction as F
from itertools import combinations, product
import json
from math import gcd
from pathlib import Path

from src.exact import Q

ROOT = Path(__file__).resolve().parents[1]
A = Q(1, F(2, 3), 3)  # 1+2/sqrt(3); Q's second argument is a coefficient.
C = F(11, 7)*A


def need(condition, message):
    if not condition:
        raise ValueError(message)


def sub(a, b):
    return tuple(x-y for x, y in zip(a, b))


def det(rows):
    a, b, c = rows
    return (a[0]*(b[1]*c[2]-b[2]*c[1])
            - a[1]*(b[0]*c[2]-b[2]*c[0])
            + a[2]*(b[0]*c[1]-b[1]*c[0]))


def solve(rows, rhs):
    d = det(rows)
    need(d != 0, 'nondegenerate system')
    return tuple(F(det([tuple(rhs[i] if j == k else rows[i][j]
                             for j in range(3)) for i in range(3)]), d)
                 for k in range(3))


def difference_barycentrics(points, vector):
    edges = [sub(p, points[0]) for p in points[1:]]
    tail = solve(list(zip(*edges)), vector)
    row = (-sum(tail),)+tail
    need(sum(row) == 0, 'zero coefficient sum')
    need(tuple(sum(c*p[j] for c, p in zip(row, points)) for j in range(3))
         == vector, 'exact vector reconstruction')
    return row


def less_than_candidate(bound):
    # Exact cross-field comparison: for positive bound-2, square once.
    shifted = bound-2
    return shifted < 0 or shifted*shifted < 2


def width_one_normal(points):
    rows = [sub(p, points[0]) for p in points[1:]]
    for values in product((0, 1), repeat=3):
        if not any(values):
            continue
        normal = solve(rows, values)
        if all(x.denominator == 1 for x in normal):
            normal = tuple(map(int, normal))
            heights = [sum(x*y for x, y in zip(normal, p)) for p in points]
            need(max(heights)-min(heights) == 1, 'width-one contact hull')
            return normal
    raise ValueError('contact hull has no width-one lattice covector')


def serialize_pair(first, second):
    rows = (first['coefficients'], second['coefficients'])
    codes = [tuple(1 if row[j] > 0 else -1 for row in rows) for j in range(4)]
    if len(set(codes)) != 4:
        return None
    m = min(abs(x) for row in rows for x in row)
    mass_sum = first['mass']+second['mass']
    denominator = m-mass_sum+2
    if denominator <= 0:
        return None
    bound = (m+2*A)/denominator
    split = 2*A/denominator
    need(split < bound, 'low-width split precedes contraction bound')
    return bound, {
        'vectors': [first['vector'], second['vector']],
        'difference_barycentrics': [[str(x) for x in row] for row in rows],
        'positive_masses': [str(first['mass']), str(second['mass'])],
        'column_sign_codes': codes, 'minimum_absolute_coefficient': str(m),
        'mass_sum': str(mass_sum), 'positive_bound_denominator': str(denominator),
        'global_class_bound': bound.json(), 'bound_expression': str(bound),
        'low_width_split': split.json(),
        'strictly_below_contact_threshold_11A_over_7': bound < C,
        'strictly_below_candidate_2_plus_sqrt2': less_than_candidate(bound),
    }


def scan_class(entry):
    points = tuple(map(tuple, entry['vertices']))
    widths = [max(p[j] for p in points)-min(p[j] for p in points) for j in range(3)]
    vectors = []
    primitive_count = 0
    for vector in product(*(range(-w, w+1) for w in widths)):
        if not any(vector) or next(x for x in vector if x) < 0 or gcd(*vector) != 1:
            continue
        primitive_count += 1
        row = difference_barycentrics(points, vector)
        mass = sum(max(F(0), x) for x in row)
        if mass >= 1 or any(x == 0 for x in row):
            continue
        vectors.append({'vector': vector, 'coefficients': row, 'mass': mass})
    pairs = []
    for first, second in combinations(vectors, 2):
        pair = serialize_pair(first, second)
        if pair is not None:
            pairs.append(pair)
    pairs.sort(key=lambda item: (item[0], item[1]['vectors']))
    return {
        'class_index': entry['class_index'], 'contact_points': points,
        'normalized_determinant': abs(det([sub(p, points[0]) for p in points[1:]])),
        'width_one_covector': width_one_normal(points),
        'coordinate_search_box': [[-w, w] for w in widths],
        'primitive_vectors_up_to_sign_in_box': primitive_count,
        'eligible_vector_count': len(vectors),
        'eligible_vectors': [{'vector': v['vector'], 'positive_mass': str(v['mass']),
                              'difference_barycentrics': list(map(str, v['coefficients']))}
                             for v in vectors],
        'distinct_code_pair_count': len(pairs),
        'best_pair': pairs[0][1] if pairs else None,
        'all_eligible_pairs': [pair for _, pair in pairs],
    }


def build():
    source = json.loads((ROOT/'certificates/contact_templates.json').read_text())
    entries = [entry for entry in source['embeddings'] if len(entry['vertices']) == 4
               and det([sub(p, entry['vertices'][0]) for p in entry['vertices'][1:]])]
    need(len(entries) == 10, 'ten full-dimensional tetrahedral classes')
    classes = [scan_class(entry) for entry in entries]
    d13 = next(entry for entry in classes if entry['normalized_determinant'] == 13)
    need(Q.from_json(d13['best_pair']['global_class_bound']) == (1+13*A)/9,
         'known determinant-13 contraction certificate reproduced')
    return {
        'status': 'exact_finite_two_vector_class_scan', 'class_count': len(classes),
        'ACMS_constant_A': A.json(), 'contact_threshold_c': C.json(),
        'candidate_vector_domain': 'Primitive nonzero lattice vectors z with gamma_P(z)<1 and all four difference barycentrics nonzero, identified up to sign',
        'coordinate_bound_proof': 'gamma_P(z) is the sum of positive difference barycentrics, so gamma_P(z)<1 implies z belongs to P-P. Every coordinate of P-P lies between minus and plus the corresponding coordinate range of P. The displayed closed box therefore contains every candidate in this domain.',
        'pair_symmetry': 'Flipping either vector preserves its mass, minimum absolute coefficient, distinctness of sign-code pairs and resulting bound, so one representative of each sign pair suffices.',
        'bound_formula': 'B=(m+2*A)/(m-S+2), S=a1+a2, m=minimum absolute value of all eight coefficients',
        'bound_scope': 'Assuming the reviewed two-vector contraction lemma and ACMS input, each recorded B bounds the lattice width of every full-dimensional hollow real tetrahedron containing an affine unimodular image of its contact hull. No boundary-contact hypothesis is needed. Nonsimplicial containing bodies are outside this statement.',
        'search_scope': 'Best means best among the displayed finite candidate domain only. No optimality is asserted outside gamma_P(z)<1, among nonprimitive vectors, or among other contraction arguments.',
        'floating_point_decisions': False, 'classes': classes,
    }


def main():
    data = build()
    (ROOT/'results/two_vector_class_scan.json').write_text(json.dumps(data, indent=2)+'\n')
    for entry in data['classes']:
        best = entry['best_pair']
        print(json.dumps({'class_index': entry['class_index'],
                          'determinant': entry['normalized_determinant'],
                          'eligible_vectors': entry['eligible_vector_count'],
                          'eligible_pairs': entry['distinct_code_pair_count'],
                          'best_bound': best['bound_expression'] if best else None,
                          'below_c': best['strictly_below_contact_threshold_11A_over_7'] if best else None,
                          'below_candidate': best['strictly_below_candidate_2_plus_sqrt2'] if best else None}))


if __name__ == '__main__':
    main()
