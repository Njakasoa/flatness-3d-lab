"""Independent exact audit of the determinant-13 contraction certificate.

Uses only the standard library; no imports from generators or geometry code.
All checks remain active under python -O.
"""
from copy import deepcopy
from fractions import Fraction as Q
from itertools import product
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
P = ((0, 0, 0), (13, 1, 5), (0, 1, 0), (0, 0, 1))
Z = ((2, 0, 1), (3, 0, 1))


def need(condition, message):
    if not condition:
        raise ValueError(message)


def dot(x, y):
    return sum(a*b for a, b in zip(x, y))


def solve(matrix, rhs):
    """Independent rational Gaussian elimination."""
    rows = [list(map(Q, row))+[Q(value)] for row, value in zip(matrix, rhs)]
    n = len(rows)
    for col in range(n):
        pivot = next(i for i in range(col, n) if rows[i][col])
        rows[col], rows[pivot] = rows[pivot], rows[col]
        scale = rows[col][col]
        rows[col] = [x/scale for x in rows[col]]
        for i in range(n):
            if i != col:
                scale = rows[i][col]
                rows[i] = [x-scale*y for x, y in zip(rows[i], rows[col])]
    return [row[-1] for row in rows]


def derive():
    matrix = [[Q(1)]*4]+[[Q(p[k]) for p in P] for k in range(3)]
    coefficients = [solve(matrix, (0,)+z) for z in Z]
    need(coefficients == [list(map(lambda x: Q(x, 13), row))
                          for row in ((-3, 2, -2, 3), (2, 3, -3, -2))],
         'independent difference-coordinate reconstruction')
    gauges = [sum(map(abs, row))/2 for row in coefficients]
    need(gauges == [Q(5, 13)]*2, 'two initial gauges')
    codes = [tuple(1 if coefficients[r][j] > 0 else -1 for r in range(2))
             for j in range(4)]
    need(len(set(codes)) == 4, 'four distinct column sign codes')
    costs = [[sum(abs(coefficients[r][j]) for r in range(2)
                  if output[r] != codes[j][r])
              for j in range(4)] for output in codes]
    for i, j in product(range(4), repeat=2):
        need(costs[i][j] == 0 if i == j else costs[i][j] >= Q(2, 13),
             'loss cost dominates mismatched mass')
    histogram = {k: 0 for k in range(4)}
    for assignment in product(range(4), repeat=4):
        missing = [j for j in range(4) if j not in assignment]
        histogram[len(missing)] += 1
        # Each missing code costs its whole input column of total mass one.
        for j in missing:
            need(all(codes[i] != codes[j] for i in assignment),
                 'every row mismatches an absent input code')
        if not missing:
            need(sorted(assignment) == list(range(4)), 'bijective matching')
    need(histogram == {0: 24, 1: 144, 2: 84, 3: 4}, '256 assignment coverage')

    # H is a nonnegative linear combination of these twelve elementary
    # transfers. Their coefficients sum to E. Convexity extends cube-vertex
    # checks to arbitrary x of oscillation one; triangle inequality then
    # gives osc(H^T x) <= E osc(x).
    oscillation_checks = 0
    for source, destination in product(range(4), repeat=2):
        if source == destination:
            continue
        for q in product((Q(0), Q(1)), repeat=4):
            image = [Q(0)]*4
            image[source] = q[destination]-q[source]
            need(max(image)-min(image) <= max(q)-min(q),
                 'elementary transfer oscillation bound')
            oscillation_checks += 1
    need(oscillation_checks == 192, 'complete transfer/cube coverage')

    direction = (0, 1, 0)
    contact_values = [dot(direction, p) for p in P]
    need(contact_values == [0, 1, 1, 0], 'explicit width-one covector')
    beta = Q(37, 102)
    loss = Q(5, 13)-beta
    e_bound = Q(13, 2)*(2*loss)
    need(e_bound == Q(29, 102) and 1/(1-e_bound) == Q(102, 73),
         'rational target bounds')
    need(Q(13, 2)*2*Q(5, 13) == 5, 'general E constant')
    need(1-(5-13*Q(4, 13)) == 0, 'strict beta endpoint')

    # Positive rational sqrt(3) enclosure; no floating point in comparisons.
    sqrt_lower = Q(17320508075688772, 10**16)
    sqrt_upper = Q(17320508075688773, 10**16)
    need(sqrt_lower*sqrt_lower < 3 < sqrt_upper*sqrt_upper,
         'radical enclosure')
    a_lower = 1+2/sqrt_upper
    a_upper = 1+2/sqrt_lower
    bound_lower = (1+13*a_lower)/9
    bound_upper = (1+13*a_upper)/9
    c_lower = 11*a_lower/7
    need(bound_upper < c_lower < Q(17, 5), 'bound below reduction threshold')
    need(Q(17, 5)-2 > 0 and (Q(17, 5)-2)**2 < 2,
         'threshold below 2+sqrt(2)')
    need(144 < 147 and a_upper < Q(13, 6), 'coarse ACMS rational bound')
    return {
        'coefficients': coefficients, 'gauges': gauges, 'codes': codes,
        'costs': costs, 'histogram': histogram,
        'oscillation_checks': oscillation_checks,
        'direction': direction, 'contact_values': contact_values,
        'beta': beta, 'loss': loss, 'e_bound': e_bound,
        'width_bound_interval': (bound_lower, bound_upper),
    }


def verify(data):
    result = derive()
    need(data['status'] == 'exact_finite_support_for_analytic_width_bound', 'status scope')
    need(list(map(tuple, data['contacts'])) == list(P), 'contact configuration')
    need(data['normalized_determinant'] == 13, 'determinant')
    need(list(map(tuple, data['lattice_vectors'])) == list(Z), 'lattice vectors')
    need([list(map(Q, row)) for row in data['difference_barycentrics']]
         == result['coefficients'], 'archived difference coordinates')
    need(list(map(Q, data['positive_masses'])) == result['gauges'], 'archived masses')
    need(list(map(tuple, data['column_sign_codes'])) == result['codes'], 'archived sign codes')
    need(Q(data['minimum_absolute_coefficient']) == Q(2, 13), 'minimum coefficient')
    expected_loss = []
    for output in product((-1, 1), repeat=2):
        for j, code in enumerate(result['codes']):
            cost = sum(abs(result['coefficients'][r][j]) for r in range(2)
                       if output[r] != code[r])
            expected_loss.append({'output_code': list(output), 'column': j,
                                  'weight': str(cost), 'mismatch': output != code})
    need(data['loss_majorization'] == expected_loss, 'all sixteen archived loss patterns')
    expected_assignments = []
    for assignment in product(range(4), repeat=4):
        missing = [j for j in range(4) if j not in assignment]
        expected_assignments.append({'row_code_indices': list(assignment),
                                     'missing_input_code_indices': missing,
                                     'is_bijection': not missing})
    need(data['row_code_assignments'] == expected_assignments,
         'all 256 archived row assignments')
    need(data['bijection_count'] == 24 and data['missing_code_assignment_count'] == 232,
         'archived assignment counts')
    need(data['oscillation_elementary_checks'] == result['oscillation_checks'],
         'archived oscillation coverage')
    need(tuple(data['width_one_covector']) == result['direction'], 'width covector')
    need(data['contact_height_values'] == result['contact_values'], 'contact heights')
    need({k: Q(v) for k, v in data['off_permutation_bound'].items()}
         == {'constant': Q(5), 'beta_coefficient': Q(-13)}, 'leakage affine bound')
    need(Q(data['strict_beta_threshold']) == Q(4, 13), 'strict matching threshold')
    need({k: Q(v) for k, v in data['inverse_width_denominator'].items()}
         == {'constant': Q(-4), 'beta_coefficient': Q(13)}, 'inverse denominator')
    bound = data['global_class_bound']
    need(bound['expression'] == '(14+26/sqrt(3))/9', 'exact expression')
    need(Q(bound['rational_part']) == Q(14, 9)
         and Q(bound['sqrt3_coefficient']) == Q(26, 27), 'radical coefficients')
    sl, su = map(Q, data['sqrt3_interval'])
    need(0 < sl < su and sl*sl < 3 < su*su, 'archived radical interval')
    bl, bu = map(Q, bound['verified_interval'])
    need((bl, bu) == (Q(14, 9)+Q(26, 27)*sl, Q(14, 9)+Q(26, 27)*su),
         'archived bound interval computed from radical coefficients')
    need(bl <= result['width_bound_interval'][0]
         < result['width_bound_interval'][1] <= bu, 'independent interval inclusion')
    need(Q(data['rational_upper_bound']) == Q(323, 100) and bu < Q(323, 100),
         'strict rational upper bound')
    need('hollow real tetrahedron' in data['scope']
         and 'Does not apply to arbitrary nonsimplicial' in data['scope']
         and 'not claimed sharp or a global flatness bound' in data['scope'],
         'surrounding-body scope')
    need(data['external_input'] == 'https://arxiv.org/abs/1907.06199, Lemma 5.1',
         'external theorem dependency')
    refinement = data['full_contact_hull_refinement']
    need(refinement == {'previous_necessary_count': 63, 'remaining_necessary_count': 62,
                        'deleted_tetrahedron_class_index': 9, 'larger_hulls_deleted': 0},
         'full-hull-only refinement')
    previous = json.loads((ROOT/'certificates/contact_templates.json').read_text())
    need(previous['configuration_count'] == 63 and len(previous['embeddings']) == 63,
         'actual earlier class count')
    deleted = [row for row in previous['embeddings'] if row['class_index'] == 9]
    need(len(deleted) == 1 and list(map(tuple, deleted[0]['vertices'])) == list(P),
         'deleted class is this full tetrahedron')
    return {'row_code_assignments': 256, 'loss_patterns': 16,
            'oscillation_checks': result['oscillation_checks'],
            'remaining_full_contact_classes': 62}


def main():
    data = json.loads((ROOT/'certificates/det13_contraction.json').read_text())
    report = verify(data)
    mutations = [
        lambda d: d['contacts'][1].__setitem__(0, 12),
        lambda d: d.__setitem__('normalized_determinant', 12),
        lambda d: d['lattice_vectors'][0].__setitem__(0, 1),
        lambda d: d['difference_barycentrics'][0].__setitem__(0, '-2/13'),
        lambda d: d['positive_masses'].__setitem__(0, '4/13'),
        lambda d: d['column_sign_codes'][0].__setitem__(0, 1),
        lambda d: d.__setitem__('minimum_absolute_coefficient', '3/13'),
        lambda d: d['loss_majorization'][0].__setitem__('weight', '1/13'),
        lambda d: d['loss_majorization'].pop(),
        lambda d: d['row_code_assignments'][0].__setitem__('is_bijection', True),
        lambda d: d['row_code_assignments'][0]['missing_input_code_indices'].pop(),
        lambda d: d['row_code_assignments'].pop(),
        lambda d: d.__setitem__('oscillation_elementary_checks', 191),
        lambda d: d['width_one_covector'].__setitem__(0, 1),
        lambda d: d['off_permutation_bound'].__setitem__('constant', '4'),
        lambda d: d.__setitem__('strict_beta_threshold', '3/13'),
        lambda d: d['inverse_width_denominator'].__setitem__('constant', '-3'),
        lambda d: d['global_class_bound'].__setitem__('sqrt3_coefficient', '25/27'),
        lambda d: d['sqrt3_interval'].__setitem__(0, '2'),
        lambda d: d['global_class_bound']['verified_interval'].__setitem__(1, '3'),
        lambda d: d.__setitem__('rational_upper_bound', '16/5'),
        lambda d: d.__setitem__('scope', 'Every containing convex body.'),
        lambda d: d['full_contact_hull_refinement'].__setitem__('larger_hulls_deleted', 1),
        lambda d: d['full_contact_hull_refinement'].__setitem__('deleted_tetrahedron_class_index', 8),
    ]
    for index, mutation in enumerate(mutations):
        altered = deepcopy(data)
        mutation(altered)
        try:
            verify(altered)
        except (ValueError, KeyError, IndexError, TypeError):
            continue
        raise ValueError(f'mutation {index} was not rejected')
    print(json.dumps({'status': 'PASS', **report, 'rejected_mutations': len(mutations)}))


if __name__ == '__main__':
    main()
