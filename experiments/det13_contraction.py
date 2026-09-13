"""Exact finite data for the analytic determinant-13 width bound.

No solver or floating arithmetic is used. The continuous proof and ACMS
input are stated in proofs/DET13_CONTRACTION_BOUND.md.
"""
from fractions import Fraction as Q
from itertools import product
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTACTS = [(0, 0, 0), (13, 1, 5), (0, 1, 0), (0, 0, 1)]
VECTORS = [(2, 0, 1), (3, 0, 1)]


def need(value, message):
    if not value:
        raise ValueError(message)


def coefficients(z):
    x, y, z = map(Q, z)
    return (5*x/13-y-z, x/13, y-x/13, z-5*x/13)


def build():
    rows = [coefficients(z) for z in VECTORS]
    for z, row in zip(VECTORS, rows):
        need(sum(row) == 0, 'difference sum')
        need(tuple(sum(row[j]*CONTACTS[j][k] for j in range(4))
                   for k in range(3)) == z, 'vector reconstruction')
    masses = [sum(max(Q(0), x) for x in row) for row in rows]
    need(masses == [Q(5,13)]*2, 'short-vector masses')
    codes = [tuple(1 if rows[r][j] > 0 else -1 for r in range(2))
             for j in range(4)]
    need(len(set(codes)) == 4, 'distinct column codes')
    m = min(abs(x) for row in rows for x in row)
    need(m == Q(2,13), 'minimum coefficient')
    majorization = []
    for output in product((-1,1), repeat=2):
        for j, code in enumerate(codes):
            weight = sum(abs(rows[r][j]) for r in range(2)
                         if output[r] != code[r])
            mismatch = output != code
            need(weight >= m*mismatch, 'mismatch majorization')
            majorization.append({'output_code': output, 'column': j,
                                 'weight': str(weight), 'mismatch': mismatch})
    assignments = []
    for row_codes in product(range(4), repeat=4):
        missing = sorted(set(range(4))-set(row_codes))
        assignments.append({'row_code_indices': row_codes,
                            'missing_input_code_indices': missing,
                            'is_bijection': not missing})
    need(sum(a['is_bijection'] for a in assignments) == 24, 'bijection count')
    # Oscillation bound on the generators of the nonnegative transfer cone.
    transfer_cases = 0
    for j in range(4):
        for i in range(4):
            if i == j:
                continue
            for q in product((0,1), repeat=4):
                htq = [0]*4
                htq[j] = q[i]-q[j]
                need(max(htq)-min(htq) <= max(q)-min(q), 'transfer bound')
                transfer_cases += 1
    lower3 = Q(1732050807568877, 10**15)
    upper3 = Q(1732050807568878, 10**15)
    need(lower3**2 < 3 < upper3**2, 'sqrt3 bracket')
    bound_lo = Q(14,9) + Q(26,27)*lower3
    bound_hi = Q(14,9) + Q(26,27)*upper3
    a_lo = 1+Q(2,3)*lower3
    c_lo = Q(11,7)*a_lo
    need(bound_hi < Q(323,100) < c_lo, 'sub-threshold class bound')
    need(Q(323,100) < 2+Q(1414213562373095, 10**15), 'candidate comparison')
    need(Q(1414213562373095, 10**15)**2 < 2, 'sqrt2 lower bracket')
    return {
        'status': 'exact_finite_support_for_analytic_width_bound',
        'contacts': CONTACTS, 'normalized_determinant': 13,
        'lattice_vectors': VECTORS,
        'difference_barycentrics': [[str(x) for x in row] for row in rows],
        'positive_masses': list(map(str, masses)), 'column_sign_codes': codes,
        'minimum_absolute_coefficient': str(m),
        'loss_majorization': majorization,
        'row_code_assignments': assignments,
        'bijection_count': 24, 'missing_code_assignment_count': 232,
        'oscillation_elementary_checks': transfer_cases,
        'width_one_covector': [0,1,0], 'contact_height_values': [0,1,1,0],
        'off_permutation_bound': {'constant': '5', 'beta_coefficient': '-13'},
        'strict_beta_threshold': '4/13',
        'inverse_width_denominator': {'constant': '-4', 'beta_coefficient': '13'},
        'global_class_bound': {'expression': '(14+26/sqrt(3))/9',
                               'rational_part': '14/9', 'sqrt3_coefficient': '26/27',
                               'verified_interval': [str(bound_lo), str(bound_hi)]},
        'sqrt3_interval': [str(lower3), str(upper3)],
        'rational_upper_bound': '323/100',
        'scope': 'Every full-dimensional hollow real tetrahedron containing an affine unimodular image of the listed P. No boundary-contact assumption. Does not apply to arbitrary nonsimplicial containing bodies; not claimed sharp or a global flatness bound.',
        'external_input': 'https://arxiv.org/abs/1907.06199, Lemma 5.1',
        'full_contact_hull_refinement': {'previous_necessary_count': 63,
                                        'remaining_necessary_count': 62,
                                        'deleted_tetrahedron_class_index': 9,
                                        'larger_hulls_deleted': 0},
    }


def main():
    data = build()
    (ROOT/'certificates/det13_contraction.json').write_text(json.dumps(data, indent=2)+'\n')
    print(json.dumps({key: data[key] for key in ('status', 'global_class_bound',
                     'bijection_count', 'oscillation_elementary_checks')}))


if __name__ == '__main__':
    main()
