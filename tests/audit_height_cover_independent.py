"""Independent read-only coverage/formula audit; no solver queries.

No experiment or geometry imports. Z3 only parses and simplifies expressions.
Exact rational normalization compares the complete archived assertion sets.
This checks encodings and coverage, never the truth of UNSAT status labels.
"""
from collections import deque
from copy import deepcopy
from fractions import Fraction as Q
from itertools import permutations
from pathlib import Path
import hashlib
import json

import z3

ROOT = Path(__file__).resolve().parents[1]


def need(condition, message):
    if not condition:
        raise AssertionError(message)


def inverse(matrix):
    n = len(matrix)
    rows = [[Q(x) for x in row] + [Q(i == j) for j in range(n)]
            for i, row in enumerate(matrix)]
    for j in range(n):
        pivot = next(i for i in range(j, n) if rows[i][j])
        rows[j], rows[pivot] = rows[pivot], rows[j]
        scale = rows[j][j]
        rows[j] = [x / scale for x in rows[j]]
        for i in range(n):
            if i != j:
                scale = rows[i][j]
                rows[i] = [x - scale * y for x, y in zip(rows[i], rows[j])]
    return [row[n:] for row in rows]


def representatives(points):
    """Independently enumerate all integral affine vertex automorphisms."""
    edge = [[points[j][i] - points[0][i] for j in range(1, 4)]
            for i in range(3)]
    inv = inverse(edge)
    group = []
    for p in permutations(range(4)):
        target = [[points[p[j]][i] - points[p[0]][i] for j in range(1, 4)]
                  for i in range(3)]
        U = [[sum(target[i][k] * inv[k][j] for k in range(3))
              for j in range(3)] for i in range(3)]
        if any(x.denominator != 1 for row in U for x in row):
            continue
        epsilon = U[1][1]
        need(abs(epsilon) == 1 and U[1] == [0, epsilon, 0], 'height action')
        group.append((p, epsilon))
    orbits = {frozenset((p[l], p[h]) if epsilon == 1 else (p[h], p[l])
                        for p, epsilon in group)
              for l, h in permutations(range(4), 2)}
    need(set().union(*orbits) == set(permutations(range(4), 2)), 'orbit coverage')
    need(sum(map(len, orbits)) == 12, 'disjoint extrema orbits')
    return {min(orbit) for orbit in orbits}


def coverage(data, guards):
    expected = {(idx, ext) for idx in (6, 7)
                for ext in representatives(guards[idx]['contact_points'])}
    actual = [(c['class_index'], tuple(c['extrema'])) for c in data['charts']]
    need(len(actual) == len(set(actual)) and set(actual) == expected,
         'all eleven distinct symmetry representatives')
    allkeys = [(r['class_index'], tuple(r['extrema']), r['node']) for r in data['queries']]
    need(len(allkeys) == len(set(allkeys)), 'unique query records')
    need(all((idx, ext) in expected for idx, ext, _ in allkeys), 'no unaccounted chart')
    output = []
    for chart in data['charts']:
        idx, ext = chart['class_index'], tuple(chart['extrema'])
        rows = [r for r in data['queries']
                if r['class_index'] == idx and tuple(r['extrema']) == ext]
        by_tag = {r['node']: r for r in rows}
        queue = deque([('r', ((Q(0), Q(1)), (Q(0), Q(1))))])
        seen, closed, unknown = [], [], []
        while queue:
            tag, box = queue.popleft()
            need(tag in by_tag, 'missing covering node: ' + tag)
            row = by_tag[tag]
            seen.append(tag)
            need(tuple(tuple(map(Q, pair)) for pair in row['box']) == box,
                 'exact closed dyadic box: ' + tag)
            if row['status'] == 'unsat':
                closed.append(tag)
            else:
                need(row['status'] in ('sat', 'unknown'), 'recognized node status')
                if row['status'] == 'unknown':
                    unknown.append(tag)
                axis = max(range(2), key=lambda i: box[i][1] - box[i][0])
                lo, hi = box[axis]
                middle = (lo + hi) / 2
                for suffix, interval in (('0', (lo, middle)), ('1', (middle, hi))):
                    child = list(box)
                    child[axis] = interval
                    queue.append((tag + suffix, tuple(child)))
        need(seen == [r['node'] for r in rows], 'exact breadth-first query order')
        need(len(seen) == len(by_tag) == chart['queries'], 'all queries accounted')
        need(closed == chart['closed_leaves'], 'exact terminal leaves')
        need(unknown == chart['unknown_nodes'], 'exact UNKNOWN ancestors')
        need(chart['complete_cover'] and not chart['pending_leaves'], 'no pending frontier')
        need(sum(Q(1, 2 ** (len(t) - 1)) for t in closed) == 1, 'dyadic area one')
        output.append({'class_index': idx, 'extrema': ext, 'queries': len(seen),
                       'covered_area': '1', 'unsat_labelled_leaves': len(closed),
                       'fully_subdivided_unknown_ancestors': len(unknown)})
    return output


def polynomial(expression):
    if z3.is_rational_value(expression):
        return {'': expression.as_fraction()}
    if z3.is_const(expression):
        need(expression.sort().kind() == z3.Z3_REAL_SORT, 'real arithmetic variable')
        return {str(expression): Q(1)}
    kind, children = expression.decl().kind(), expression.children()
    if kind in (z3.Z3_OP_ADD, z3.Z3_OP_SUB, z3.Z3_OP_UMINUS):
        result = {}
        for i, child in enumerate(children):
            sign = -1 if kind == z3.Z3_OP_UMINUS or (kind == z3.Z3_OP_SUB and i) else 1
            for name, coefficient in polynomial(child).items():
                result[name] = result.get(name, Q(0)) + sign * coefficient
        return {name: c for name, c in result.items() if c}
    if kind == z3.Z3_OP_MUL:
        result = {'': Q(1)}
        for child in children:
            factor, product = polynomial(child), {}
            for name, coefficient in result.items():
                for other, value in factor.items():
                    need(not (name and other), 'no nonlinear variable products')
                    key = name or other
                    product[key] = product.get(key, Q(0)) + coefficient * value
            result = {name: c for name, c in product.items() if c}
        return result
    raise AssertionError('unsupported arithmetic: ' + str(expression))


def canonical(expression, negated=False):
    if z3.is_true(expression):
        return not negated
    if z3.is_false(expression):
        return negated
    if z3.is_not(expression):
        return canonical(expression.arg(0), not negated)
    if z3.is_and(expression) or z3.is_or(expression):
        conjunction = z3.is_and(expression) ^ negated
        operator = 'and' if conjunction else 'or'
        values = []
        for child in expression.children():
            value = canonical(child, negated)
            if value is conjunction:
                continue
            if value is (not conjunction):
                return not conjunction
            if isinstance(value, tuple) and value[0] == operator:
                values.extend(value[1])
            else:
                values.append(value)
        values = tuple(sorted(set(values), key=repr))
        if not values:
            return conjunction
        return values[0] if len(values) == 1 else (operator, values)
    comparisons = {z3.Z3_OP_LE: '<=', z3.Z3_OP_LT: '<', z3.Z3_OP_GE: '>=',
                   z3.Z3_OP_GT: '>', z3.Z3_OP_EQ: '='}
    need(expression.decl().kind() in comparisons, 'supported Boolean atom')
    comparison = comparisons[expression.decl().kind()]
    coefficients = polynomial(expression.arg(0) - expression.arg(1))
    if negated:
        comparison = {'<=': '>', '<': '>=', '>=': '<', '>': '<=', '=': '!='}[comparison]
    if comparison in ('>', '>='):
        comparison = {'>': '<', '>=': '<='}[comparison]
        coefficients = {name: -c for name, c in coefficients.items()}
    if not coefficients:
        return comparison in ('<=', '=')
    items = sorted(coefficients.items())
    scale = abs(items[0][1])
    if comparison in ('=', '!=') and items[0][1] < 0:
        scale = -scale
    return comparison, tuple((name, c / scale) for name, c in items)


def forms(expressions):
    output = set()
    for expression in expressions:
        value = canonical(z3.simplify(expression))
        if value is not True:
            output.add(value)
    return output


def expected_assertions(contact, scan, extrema, box):
    """Construct the stated mathematics without importing discovery code."""
    d, residue = contact['normalized_volume'], contact['contact_points'][1][2]
    F = [[z3.RealVal(0) for _ in range(4)] for _ in range(4)]
    for j in range(4):
        ids = [i for i in range(4) if i != j]
        x, y = [z3.Real(f'f{i}{j}') for i in ids[:2]]
        for i, value in zip(ids, (x, y, 1 - x - y)):
            F[i][j] = value
    assertions = [F[i][j] > 0 for i in range(4) for j in range(4) if i != j]

    def barycentrics(vector, affine=False):
        x, y, z = map(Q, vector)
        return [int(affine) + residue * x / d - y - z, x / d,
                y - x / d, z - residue * x / d]

    vectors = sorted(set(map(tuple, contact['primitive_contact_edge_directions'])) |
                     {tuple(row['vector']) for row in scan['eligible_vectors']})
    gauges = []
    for vector in vectors:
        coords = barycentrics(vector)
        values = [sum(F[i][j] * z3.RealVal(str(coords[j])) for j in range(4))
                  for i in range(4)]
        gauge = z3.Or(*[sum(values[i] for i in range(4) if mask & (1 << i)) >
                         z3.RealVal('37/102') for mask in range(1, 15)])
        assertions.append(gauge)
        gauges.append(gauge)
    for vector in contact['guards']:
        coords = barycentrics(vector, True)
        assertions.append(z3.Or(*[sum(F[i][j] * z3.RealVal(str(coords[j]))
                                     for j in range(4)) <= 0 for i in range(4)]))
    q = [z3.RealVal(0) if i == extrema[0] else z3.RealVal(1) if i == extrema[1]
         else z3.Real(f'q{i}') for i in range(4)]
    offset, gap = z3.Reals('height_offset height_gap')
    assertions += [v >= 0 for v in q] + [v <= 1 for v in q]
    assertions += [offset >= 0, offset + gap <= 1, gap > 0, gap < z3.RealVal('5/17')]
    products, envelopes = {}, []
    for i, (lo, hi) in zip([i for i in range(4) if i not in extrema], box):
        low, high = z3.RealVal(str(lo)), z3.RealVal(str(hi))
        assertions += [q[i] >= low, q[i] <= high]
        for j in range(4):
            if i == j:
                continue
            product = z3.Real(f'height_product_{i}_{j}')
            products[i, j] = product
            f = F[i][j]
            inequalities = [product >= low * f, product <= high * f,
                            product >= q[i] + high * f - high,
                            product <= q[i] + low * f - low]
            envelopes.extend(inequalities)
            assertions.extend(inequalities)
    for j in range(4):
        total = sum(products.get((i, j), q[i] * F[i][j]) for i in range(4))
        assertions.append(total == offset + gap * int(j in (1, 2)))
    return assertions, gauges, envelopes


def compare(expected, actual):
    wanted, observed = forms(expected), forms(actual)
    need(wanted == observed,
         f'assertion-set mismatch: missing={len(wanted-observed)}, extra={len(observed-wanted)}')


def expect_rejection(name, action):
    try:
        action()
    except AssertionError as error:
        return {'mutation': name, 'rejected': True, 'reason': str(error)}
    raise AssertionError('undetected mutation: ' + name)


def mutations(data, guards, expected, actual, gauges, envelopes):
    results = []
    missing = deepcopy(data)
    missing['queries'] = [r for r in missing['queries']
                          if not (r['class_index'] == 6 and r['extrema'] == [0, 1]
                                  and r['node'] == 'r0')]
    results.append(expect_rejection('missing covering leaf', lambda: coverage(missing, guards)))
    gap = deepcopy(data)
    row = next(r for r in gap['queries'] if r['class_index'] == 6
               and r['extrema'] == [0, 1] and r['node'] == 'r0')
    row['box'][0][1] = '49/100'
    results.append(expect_rejection('gap in closed interval cover', lambda: coverage(gap, guards)))
    gauge_key = canonical(z3.simplify(gauges[0]))
    deleted = [e for e in actual if canonical(z3.simplify(e)) != gauge_key]
    need(len(deleted) < len(actual), 'mutation removed an actual gauge')
    results.append(expect_rejection('deleted gauge', lambda: compare(expected, deleted)))
    results.append(expect_rejection('extra contradictory assertion',
                                    lambda: compare(expected, actual + [z3.BoolVal(False)])))
    envelope_key = canonical(z3.simplify(envelopes[0]))
    altered = [e for e in actual if canonical(z3.simplify(e)) != envelope_key]
    need(len(altered) < len(actual), 'mutation removed an actual envelope')
    altered.append(envelopes[0].arg(0) >= envelopes[0].arg(1) + z3.RealVal('1/100'))
    results.append(expect_rejection('overrestrictive product envelope',
                                    lambda: compare(expected, altered)))
    return results


def main():
    archive = ROOT / 'results/height_interval_relaxation.json'
    data = json.loads(archive.read_text())
    guards = {c['class_index']: c for c in json.loads(
        (ROOT / 'certificates/nonunimodular_observer_guards.json').read_text())['classes']}
    scans = {c['class_index']: c for c in json.loads(
        (ROOT / 'results/two_vector_class_scan.json').read_text())['classes']}
    chart_results = coverage(data, guards)
    file_hashes, control = [], None
    for row in data['queries']:
        idx, ext = row['class_index'], tuple(row['extrema'])
        expected_path = f'results/height_interval_{idx}_{ext[0]}_{ext[1]}_{row["node"]}.smt2'
        need(row['path'] == expected_path, 'canonical node archive path')
        path = ROOT / expected_path
        box = tuple(tuple(map(Q, pair)) for pair in row['box'])
        expected, gauges, envelopes = expected_assertions(guards[idx], scans[idx], ext, box)
        actual = list(z3.parse_smt2_file(str(path)))
        compare(expected, actual)
        file_hashes.append({'path': expected_path, 'sha256': hashlib.sha256(path.read_bytes()).hexdigest()})
        if idx == 6 and ext == (0, 1) and row['node'] == 'r0':
            control = expected, actual, gauges, envelopes
    need(control is not None, 'mutation control leaf exists')
    mutation_results = mutations(data, guards, *control)
    report = {'status': 'PASS', 'archive_sha256': hashlib.sha256(archive.read_bytes()).hexdigest(),
              'solver_queries_run': 0, 'unsat_outcomes_verified': False,
              'query_count': len(data['queries']),
              'unsat_labelled_leaf_count': sum(c['unsat_labelled_leaves'] for c in chart_results),
              'charts': chart_results, 'mutations': mutation_results, 'archived_files': file_hashes,
              'scope': 'Independent complete assertion-set and exact dyadic-cover audit. '
                       'No experiment imports or solver queries. UNSAT status labels are not verified.'}
    destination = ROOT / 'results/height_cover_encoding_validation.json'
    destination.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({key: report[key] for key in ('status', 'query_count',
                     'unsat_labelled_leaf_count', 'solver_queries_run', 'unsat_outcomes_verified')}))
    print('Rejected all five coverage/formula mutations.')


if __name__ == '__main__':
    main()
