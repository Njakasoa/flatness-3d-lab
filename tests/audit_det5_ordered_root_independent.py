"""Independent exact ordered-root encoding/SAT audit. No solver queries."""
from pathlib import Path
from fractions import Fraction as Q
import json
import replay_det5_conditional_width_bounds as base
from replay_det5_y_corner_supplement import evaluate

ROOT = Path(__file__).resolve().parents[1]


def plus(*xs):
    return ['+', *xs]


def reconstruction(C, row, rectangles, offset_order=False, difference_coupling=False):
    variables, expected = base.expected(C, [0, 3], [['0', '1']]*2, Q(37, 102))
    z = [plus(0 if i == 3 else f'F_{i}_3',
              ['-', 0 if i == 0 else f'F_{i}_0']) for i in range(4)]
    old_z = ['or', *[['>', plus(*(z[i] for i in range(4) if mask & (1 << i))), Q(37, 102)]
                     for mask in range(1, 15)]]
    key = base.canon(old_z)
    base.need(sum(base.canon(a) == key for a in expected) == 1, 'one generic Z gauge')
    expected = [a for a in expected if base.canon(a) != key]
    exclusions = []
    for box in rectangles:
        exclusions.append(['or', *[atom for i, (lo, hi) in zip((1, 2), box)
                                   for atom in (['<', f'q_{i}', Q(lo)], ['>', f'q_{i}', Q(hi)])]])
    base.need(row['order'] in ('lt', 'gt'), 'two strict order branches only')
    small, large = (1, 2) if row['order'] == 'lt' else (2, 1)
    order = [['<', f'q_{small}', f'q_{large}'],
             ['<', f'F_{small}_3', f'F_{small}_0'],
             ['>', f'F_{large}_3', f'F_{large}_0'],
             ['>', plus('F_0_3', z[large]), Q(37, 102)]]
    offset = [['<', f'q_{small}', 'offset'], ['<', 'offset', f'q_{large}']]
    difference = []
    for i in (1, 2):
        q = f'q_{i}'
        d = z[i]
        w = plus(f'product_{i}_3', ['-', f'product_{i}_0'])
        lo, hi = (-1, 0) if i == small else (0, 1)
        # McCormick for q in [0,1], d in [lo,hi], shared w=q*d.
        difference += [['>=', w, ['*', lo, q]],
                       ['>=', w, plus(d, ['*', hi, q], -hi)],
                       ['<=', w, plus(d, ['*', lo, q], -lo)],
                       ['<=', w, ['*', hi, q]]]
    expected += exclusions + order
    if offset_order:
        expected += offset
    if difference_coupling:
        expected += difference
    return variables, expected, {'offset': offset, 'difference': difference, 'exclusions': exclusions}


def parse_input(row):
    raw = (ROOT/row['input_path']).read_bytes()
    base.need(base.digest(raw) == row['input_sha256'], 'input hash')
    declared, assertions = set(), []
    for c in base.parse(raw.decode()):
        if c[0] == 'set-logic':
            base.need(c == ['set-logic', 'QF_LRA'], 'linear logic')
        elif c[0] == 'declare-fun':
            base.need(c[2:] == [[], 'Real'], 'real variable declaration')
            declared.add(c[1])
        elif c[0] == 'assert':
            assertions.append(c[1])
        else:
            raise ValueError('unexpected input command')
    return declared, assertions


def assignment_of(row):
    assignment = {}
    for key, value in row['assignment'].items():
        parsed = base.parse(value)
        base.need(len(parsed) == 1, 'one SMT rational value')
        p = base.poly(parsed[0])
        base.need(set(p) <= {''}, 'rational constant value')
        assignment[key] = p.get('', Q(0))
    return assignment


def main():
    C = next(c for c in base.read('certificates/nonunimodular_observer_guards.json')['classes'] if c['class_index'] == 5)
    old_path = 'results/det5_class5_y_cvc5_validation.json'
    new_path = 'results/det5_y_corner_enlarged_3_5.json'
    old, new = base.read(old_path), base.read(new_path)
    base.need(old['status'] == 'PASS', 'old proof receipt')
    leaves = [r for r in old['leaves'] if r['extrema'] == [0, 3]]
    base.need(len(leaves) == 7, 'seven old same-chart rectangles')
    rectangle_proofs = [base.audit_row(C, r, [0, 3], r['box'], Q(37, 102)) for r in leaves+[new]]
    rectangles = [r['box'] for r in leaves+[new]]
    sources, checked, controls = {}, [], []
    campaigns = [('results/det5_y_ordered_root.json', False, False),
                 ('results/det5_y_ordered_root_offset.json', True, False),
                 ('results/det5_y_ordered_root_difference.json', True, True)]
    for path, has_offset, has_difference in campaigns:
        archive = base.read(path)
        sources[path] = base.digest((ROOT/path).read_bytes())
        base.need(archive['extrema'] == [0, 3] and archive['box'] == [['0', '1']]*2
                  and Q(archive['beta']) == Q(37, 102) and Q(archive['target']) == Q(17, 5), 'whole-chart metadata')
        base.need(archive.get('offset_order', False) == has_offset, 'offset variant')
        base.need(archive.get('difference_products', False) == has_difference, 'difference coupling variant')
        base.need(archive['old_Y_proof_receipt_sha256'] == base.digest((ROOT/old_path).read_bytes())
                  and archive['enlarged_proof_receipt_sha256'] == base.digest((ROOT/new_path).read_bytes()), 'proof source hashes')
        base.need(archive['excluded_Y_rectangles'] == rectangles, 'exact eight rectangle complements')
        base.need(len(archive['queries']) == 2 and {r['order'] for r in archive['queries']} == {'lt', 'gt'}, 'two exhaustive order branches')
        for row in archive['queries']:
            variables, expected, groups = reconstruction(C, row, rectangles, has_offset, has_difference)
            declared, assertions = parse_input(row)
            base.need(declared == variables and len(declared) == 22, 'exact 22 variables')
            base.need(base.forms(assertions) == base.forms(expected), 'independently reconstructed complete formula')
            base.need(row['status'] == 'sat', 'frozen SAT status')
            assignment = assignment_of(row)
            base.need(set(assignment) == declared, 'complete rational assignment')
            base.need(all(evaluate(a, assignment) for a in assertions), 'every saved assertion evaluates true')
            residuals = {}
            for i in (1, 2):
                for j in range(4):
                    if i != j:
                        name = f'product_{i}_{j}'
                        residuals[name] = str(assignment[name]-assignment[f'q_{i}']*assignment[f'F_{i}_{j}'])
            difference_residuals = {str(i): str((assignment[f'product_{i}_3']-assignment[f'product_{i}_0'])
                                               -assignment[f'q_{i}']*(assignment[f'F_{i}_3']-assignment[f'F_{i}_0'])) for i in (1, 2)}
            base.need(any(Q(r) != 0 for r in residuals.values()), 'outer witness has inexact products')
            checked.append({'archive_path': path, 'order': row['order'], 'input_path': row['input_path'],
                            'input_sha256': row['input_sha256'], 'assertions_checked': len(assertions),
                            'variables_checked': len(declared), 'all_assertions_true': True,
                            'product_minus_exact_qF': residuals,
                            'difference_product_residuals': difference_residuals,
                            'offset_cuts_failed': sum(not evaluate(a, assignment) for a in groups['offset']),
                            'difference_cuts_failed': sum(not evaluate(a, assignment) for a in groups['difference'])})
            # Corruption controls on one representative exact formula and model.
            if not controls:
                reversed_row = {**row, 'order': 'gt' if row['order'] == 'lt' else 'lt'}
                _, wrong, _ = reconstruction(C, reversed_row, rectangles, has_offset, has_difference)
                base.need(base.forms(assertions) != base.forms(wrong), 'wrong order rejected')
                _, missing, _ = reconstruction(C, row, rectangles[:-1], has_offset, has_difference)
                base.need(base.forms(assertions) != base.forms(missing), 'missing certified complement rejected')
                base.need(not all(evaluate(a, {**assignment, 'gap': Q(0)}) for a in assertions), 'zero-gap mutation rejected')
                controls = ['reversed order branch', 'missing enlarged-square complement', 'zero-gap assignment']
    result = {'status': 'PASS',
              'scope': 'Independent full reconstruction and exact saved SAT substitution for ordered-root variants. Eight same-chart certified rectangle complements. Existing rectangle proof receipts bound; no solver calls or proof-kernel reruns. SAT witnesses are outer feasibility only.',
              'source_archive_sha256': sources, 'rectangle_proof_bindings': rectangle_proofs,
              'inputs_checked': checked, 'rejected_corruption_controls': controls,
              'solver_queries_run': 0, 'proof_kernel_reruns': 0}
    (ROOT/'results/det5_ordered_root_encoding_validation.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({'status': 'PASS', 'inputs': len(checked), 'SAT_assignments': len(checked),
                      'rectangle_proofs_bound': len(rectangle_proofs),
                      'extra_cut_failures': [{k: r[k] for k in ('archive_path', 'order', 'offset_cuts_failed', 'difference_cuts_failed')} for r in checked]}, indent=2))


if __name__ == '__main__':
    main()
