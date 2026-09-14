"""Replay the fiber certificate using the invariant three-space rank proof.

No discovery imports or solver calls. Checks all stored coefficients against
independent column elimination and the 3x3 restriction, plus the projective
identity and a deliberately corrupted coefficient.
"""
from pathlib import Path
import hashlib
import json
import sympy as s
from audit_det5_quadratic_chart_independent import eliminated

ROOT = Path(__file__).resolve().parents[1]


def need(condition, message):
    if not condition:
        raise ValueError(message)


def main():
    path = ROOT/'certificates/det5_horizontal_fiber_structure.json'
    payload = json.loads(path.read_text())
    def coverage(data):
        need(data['horizontal_variables'] == ['low', 'high', 'c', 'e', 'r', 'u'], 'shape variable order')
        need(data['linear_variables'] == ['alpha=theta/gap', 'eta=h/gap', 'rho=1/gap'], 'scaled variable order')
        need(data['linear_equality'] == 'eta-low*rho-(high-low)*alpha=1', 'normalization metadata')
        need(sorted(row['order'] for row in data['branches']) == ['gt', 'lt'], 'exactly both branches')
        expected_pairs = {(k, i, j) for k in range(3) for i in range(4) for j in range(i)}
        expected_entries = {(i, j) for i in range(4) for j in range(4)}
        for branch in data['branches']:
            pairs = [(r['coordinate'], *r['vertex_pair']) for r in branch['coordinate_pair_numerators']]
            entries = [(r['row'], r['column']) for r in branch['scaled_F_entries']]
            need(len(pairs) == len(set(pairs)) == 18 and set(pairs) == expected_pairs, 'complete unique coordinate pairs')
            need(len(entries) == len(set(entries)) == 16 and set(entries) == expected_entries, 'complete unique matrix entries')
        need(set(data['horizontal_images_lt']) == {'R', 'Z'} and all(len(row) == 4 for row in data['horizontal_images_lt'].values()), 'both horizontal images')
    coverage(payload)
    identity_count = 0
    corruption_control = None
    def zero(expr, message):
        nonlocal identity_count
        need(s.expand(expr) == 0, message)
        identity_count += 1
    B = s.Matrix([[-1, -1, -1], [1, 0, 0], [0, 1, 0], [0, 0, 1]])
    P = s.Matrix([[0, 5, 0, 0], [0, 1, 1, 0], [0, 2, 0, 1]])
    for branch in payload['branches']:
        variables, F, q, a, b = eliminated(branch['order'])
        x, y, t, c, e, r, u, h = variables
        sigma = (x, y, c, e, r, u)
        alpha, eta, rho = s.symbols('alpha eta rho')
        def decode(terms):
            total = 0
            for term in terms:
                need(len(term['powers']) == 6 and all(isinstance(n, int) and n >= 0 for n in term['powers']), 'valid sparse monomial')
                total += s.Rational(term['coefficient'])*s.prod(v**n for v, n in zip(sigma, term['powers']))
            return s.expand(total)
        D = decode(payload['horizontal_determinant'])
        if branch['order'] == 'lt':
            for key, expected in (('R', F[:, 1]-F[:, 2]), ('Z', F[:, 3]-F[:, 0])):
                for terms, value in zip(payload['horizontal_images_lt'][key], expected):
                    zero(decode(terms)-value, 'stored horizontal image')
        G = (F*B)[1:4, :]
        for z in F*B-B*G:
            zero(z, 'invariant zero-sum subspace')
        update = s.Matrix([-t, t, -h]) if branch['order'] == 'lt' else s.Matrix([t, -t, -h])
        for z in G-G.subs({t: 0, h: 0})-update*s.Matrix([[-1, -1, 0]]):
            zero(z, 'single rank-one fiber update')
        zero(s.expand(G.det())-b*D, 'determinant on invariant subspace')
        inverse_numerators = P*B*G.adjugate()
        for row in branch['coordinate_pair_numerators']:
            i, j = row['vertex_pair']
            pair = s.zeros(4, 1); pair[i] = 1; pair[j] = -1
            numerator = (inverse_numerators*pair[1:4, :])[row['coordinate']]
            coefficients = [decode(row[name]) for name in ('alpha', 'eta', 'rho')]
            zero(numerator-(t*coefficients[0]+h*coefficients[1]+coefficients[2]), 'stored coordinate pair')
            if corruption_control is None:
                corruption_control = (numerator, t*coefficients[0]+h*coefficients[1]+coefficients[2]+1)
            zero(s.cancel(rho*numerator.subs({t: alpha/rho, h: eta/rho}))-
                 (alpha*coefficients[0]+eta*coefficients[1]+rho*coefficients[2]), 'projective numerator')
        for row in branch['scaled_F_entries']:
            f = F[row['row'], row['column']]
            coefficients = [decode(row[name]) for name in ('alpha', 'eta', 'rho')]
            zero(f-(t*coefficients[0]+h*coefficients[1]+coefficients[2]), 'stored scaled F')
        # The affine normalization guarantees b=1/rho, so multiplying signs
        # by rho is valid precisely under the explicit rho>0 hypothesis.
        zero(s.cancel(rho*b.subs({t: alpha/rho, h: (1+x*rho+(y-x)*alpha)/rho}))-1,
             'positive-gap normalization')
    # This check must fail independently of any asserted PASS label.
    rejected = False
    try:
        zero(corruption_control[0]-corruption_control[1], 'corrupted stored coordinate pair')
    except ValueError:
        rejected = True
    need(rejected, 'coefficient corruption rejected')
    controls = []
    for mutation in ('missing pair', 'duplicate branch'):
        altered = json.loads(json.dumps(payload))
        if mutation == 'missing pair':
            altered['branches'][0]['coordinate_pair_numerators'].pop()
        else:
            altered['branches'][1] = altered['branches'][0]
        rejected = False
        try:
            coverage(altered)
        except ValueError:
            rejected = True
        need(rejected, mutation+' rejected')
        controls.append(mutation)
    result = {'status': 'PASS', 'scope': 'Independent invariant-subspace and coefficient replay; no shape-domain cover.',
              'certificate_sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
              'symbolic_identities': identity_count, 'branches': 2,
              'coordinate_pairs': 36, 'scaled_entries': 32,
              'coefficient_corruption_rejected': True, 'coverage_mutations_rejected': controls,
              'horizontal_image_expressions': 8, 'solver_queries_run': 0}
    (ROOT/'results/det5_horizontal_fiber_validation.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
