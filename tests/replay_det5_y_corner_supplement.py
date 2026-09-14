"""Independent stdlib input, archived-proof, and rational SAT supplement audit.

No discovery-generator imports, solver calls, or proof-kernel reruns.
"""
from fractions import Fraction as Q
import json
import replay_det5_conditional_width_bounds as base

ROOT = base.ROOT


def input_only(C, row, ext, box, beta):
    raw = (ROOT / row['input_path']).read_bytes()
    base.need(base.digest(raw) == row['input_sha256'], 'input hash')
    declared, assertions = set(), []
    for command in base.parse(raw.decode()):
        if command[0] == 'set-logic':
            base.need(command == ['set-logic', 'QF_LRA'], 'linear logic')
        elif command[0] == 'declare-fun':
            base.need(command[2:] == [[], 'Real'], 'nullary real variable')
            declared.add(command[1])
        elif command[0] == 'assert':
            assertions.append(command[1])
        else:
            raise ValueError('unexpected SMT command')
    variables, wanted = base.expected(C, ext, box, beta)
    base.need(declared == variables and len(declared) == 22, '22-variable domain')
    base.need(base.forms(assertions) == base.forms(wanted), 'complete independent formula')
    return declared, assertions


def evaluate(e, assignment):
    if e == 'true':
        return True
    if e == 'false':
        return False
    op, *args = e
    if op in ('or', 'and'):
        return (any if op == 'or' else all)(evaluate(a, assignment) for a in args)
    p = base.poly(['-', *args])
    value = sum(c * (1 if n == '' else assignment[n]) for n, c in p.items())
    return {'<': value < 0, '<=': value <= 0, '>': value > 0,
            '>=': value >= 0, '=': value == 0}[op]


def main():
    C = next(c for c in base.read('certificates/nonunimodular_observer_guards.json')['classes'] if c['class_index'] == 5)
    inputs, sources = [], {}
    sharp_path = 'results/det5_y_corner_gauge_sharp_probe.json'
    sharp = base.read(sharp_path)
    base.need(sharp['extrema'] == [0, 3] and sharp['box'] == [['3/4', '1']] * 2,
              'sharp corner metadata')
    base.need(set(map(tuple, sharp['gauge_vectors'])) == base.VECTORS, 'ten gauges')
    sharp_row = next(r for r in sharp['queries'] if Q(r['beta']) == Q(4, 23))
    inputs.append(base.audit_row(C, sharp_row, [0, 3], sharp['box'], Q(4, 23)))
    sources[sharp_path] = base.digest((ROOT / sharp_path).read_bytes())
    for path, lower in [('results/det5_y_corner_enlarged.json', '2/3'),
                        ('results/det5_y_corner_enlarged_3_5.json', '3/5')]:
        row = base.read(path)
        base.need(row['extrema'] == [0, 3] and row['box'] == [[lower, '1']] * 2,
                  'enlarged square metadata')
        base.need(Q(row['beta']) == Q(37, 102) and Q(row['target']) == Q(17, 5), 'enlarged thresholds')
        base.need(set(map(tuple, row['gauge_vectors'])) == base.VECTORS, 'enlarged ten gauges')
        inputs.append(base.audit_row(C, row, [0, 3], row['box'], Q(37, 102)))
        sources[path] = base.digest((ROOT / path).read_bytes())
    sat_path = 'results/det5_y_corner_enlarged_11_20.json'
    sat = base.read(sat_path)
    base.need(sat['status'] == 'sat' and sat['extrema'] == [0, 3]
              and sat['box'] == [['11/20', '1']] * 2, 'SAT metadata')
    base.need(Q(sat['beta']) == Q(37, 102) and Q(sat['target']) == Q(17, 5)
              and set(map(tuple, sat['gauge_vectors'])) == base.VECTORS, 'SAT thresholds and gauges')
    declared, assertions = input_only(C, sat, [0, 3], sat['box'], Q(37, 102))
    assignment = {}
    for name, text in sat['assignment'].items():
        expression = base.parse(text)
        base.need(len(expression) == 1, 'one rational value')
        p = base.poly(expression[0])
        base.need(set(p) <= {''}, 'constant rational assignment')
        assignment[name] = p.get('', Q(0))
    base.need(set(assignment) == declared, 'complete 22-variable assignment')
    base.need(all(evaluate(a, assignment) for a in assertions), 'all saved assertions true')
    # Lifted products need not be actual products: explicitly record the distinction.
    mismatches = [f'product_{i}_{j}' for i in (1, 2) for j in range(4) if i != j
                  and assignment[f'product_{i}_{j}'] != assignment[f'q_{i}'] * assignment[f'F_{i}_{j}']]
    base.need(mismatches, 'saved outer witness has a genuine product relaxation gap')
    sources[sat_path] = base.digest((ROOT / sat_path).read_bytes())
    failures = []
    for name, action in [
        ('wrong gauge threshold', lambda: input_only(C, sharp_row, [0, 3], sharp['box'], Q(3, 10))),
        ('wrong enlarged endpoint', lambda: input_only(C, sat, [0, 3], [['3/5', '1']] * 2, Q(37, 102))),
        ('altered SAT assignment', lambda: base.need(all(evaluate(a, {**assignment, 'gap': Q(0)}) for a in assertions), 'mutation')),
    ]:
        try:
            action()
        except ValueError:
            failures.append(name)
        else:
            raise ValueError('accepted corruption control: ' + name)
    sharp_coefficient = 1 / (1 - Q(4, 23))
    weak_coefficient = 1 / (1 - Q(37, 102))
    base.need(sharp_coefficient == Q(23, 19) and weak_coefficient == Q(102, 65), 'ACMS coefficients')
    base.need(1 - Q(3, 4) == Q(1, 4) < Q(5, 17), 'automatic corner width premise')
    base.need(1 - Q(12, 17) == Q(5, 17), 'inclusive stronger subcorner endpoint')
    base.need(Q(3, 5) < Q(2, 3) < Q(12, 17) < Q(3, 4), 'nested certified domains')
    base.need(1 - Q(3, 5) > Q(5, 17), 'whole enlarged domain does not force width premise')
    # A < 13/6 follows by squaring the positive inequality 2/sqrt(3) < 7/6.
    base.need(Q(4, 3) < Q(7, 6) ** 2 and weak_coefficient * Q(13, 6) == Q(17, 5), 'strict weak bound below target')
    result = {
        'status': 'PASS',
        'scope': 'Four independently reconstructed 22-variable inputs; three existing cvc5/Ethos proof receipts and proof hashes bound; one saved rational SAT assignment checked exactly. No solver or proof-kernel reruns. Conditional height subdomains only.',
        'source_receipt_sha256': sources,
        'verified_unsat_inputs': inputs,
        'sat_input': {'input_path': sat['input_path'], 'input_sha256': sat['input_sha256'],
                      'variables_checked': len(assignment), 'assertions_checked': len(assertions),
                      'all_assertions_true': True, 'inexact_lifted_products': mismatches,
                      'interpretation': 'Outer feasibility only; this assignment violates exact product identities and is not an actual tetrahedron witness.'},
        'conditional_bounds': [
            {'extrema': [0, 3], 'box': [['3/5', '1']] * 2, 'global_width_upper_bound': '17/5'},
            {'extrema': [0, 3], 'box': [['12/17', '1']] * 2, 'global_width_upper_bound': '(102/65)*(1+2/sqrt(3))'},
            {'extrema': [0, 3], 'box': [['3/4', '1']] * 2, 'global_width_upper_bound': '(23/19)*(1+2/sqrt(3))'},
        ],
        'rejected_corruption_controls': failures,
        'solver_queries_run': 0, 'proof_kernel_reruns': 0,
    }
    (ROOT / 'results/det5_y_corner_supplement_validation.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({'status': result['status'], 'unsat_inputs': len(inputs), 'SAT_assertions': len(assertions),
                      'inexact_lifted_products': len(mismatches), 'conditional_bounds': result['conditional_bounds']}, indent=2))


if __name__ == '__main__':
    main()
