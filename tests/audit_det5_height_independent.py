"""Read-only determinant-five geometry, formula and frontier audit.

No discovery/experiment imports and no solver.check calls. The independent
earlier audit supplies exact linear formula reconstruction and normalization.
UNSAT labels are deliberately not verified by this script.
"""
from collections import deque
from copy import deepcopy
from fractions import Fraction as Q
from itertools import permutations
from pathlib import Path
import hashlib
import json

import z3
from audit_height_cover_independent import (
    need, inverse, expected_assertions, compare, canonical, expect_rejection,
)
from replay_nonunimodular_guards_independent import verify as verify_guards

ROOT = Path(__file__).resolve().parents[1]


def geometry(points):
    edges = [[points[j][i] - points[0][i] for j in range(1, 4)]
             for i in range(3)]
    inv = inverse(edges)
    full, preserving = [], []
    for p in permutations(range(4)):
        target = [[points[p[j]][i] - points[p[0]][i] for j in range(1, 4)]
                  for i in range(3)]
        U = [[sum(target[i][k] * inv[k][j] for k in range(3))
              for j in range(3)] for i in range(3)]
        if any(x.denominator != 1 for row in U for x in row):
            continue
        entry = {'permutation': list(p), 'matrix': [[int(x) for x in r] for r in U],
                 'translation': points[p[0]]}
        full.append(entry)
        epsilon = U[1][1]
        if abs(epsilon) == 1 and U[1] == [0, epsilon, 0]:
            preserving.append(dict(entry, height_sign=int(epsilon)))
    orbits = {frozenset((g['permutation'][l], g['permutation'][h])
                        if g['height_sign'] == 1 else
                        (g['permutation'][h], g['permutation'][l])
                        for g in preserving)
              for l, h in permutations(range(4), 2)}
    need(sum(map(len, orbits)) == 12 and set().union(*orbits) ==
         set(permutations(range(4), 2)), 'complete disjoint extrema orbits')
    return full, preserving, [[list(pair) for pair in sorted(orbit)]
                              for orbit in sorted(orbits, key=min)]


def geometry_audit(data, guards, scans):
    need([c['class_index'] for c in data['classes']] == [4, 5], 'two source classes')
    representatives, report = set(), []
    for C in data['classes']:
        idx = C['class_index']
        P = [[0, 0, 0], [5, 1, idx - 3], [0, 1, 0], [0, 0, 1]]
        need(C['contact_points'] == guards[idx]['contact_points'] == P,
             'fixed determinant-five contacts')
        full, preserving, orbits = geometry(P)
        need(C['full_automorphisms'] == full, 'exhaustive affine group')
        need(C['height_automorphisms'] == preserving, 'exact height-preserving subgroup')
        need(C['extrema_orbits'] == orbits, 'exact ordered extrema orbit archive')
        need(C['guard_count'] == len(guards[idx]['guards']) == (40 if idx == 4 else 20),
             'class guard count')
        need(len(full) == (8 if idx == 4 else 4) and len(preserving) == 4,
             'expected group orders')
        vectors = set(map(tuple, guards[idx]['primitive_contact_edge_directions'])) | {
            tuple(v['vector']) for v in scans[idx]['eligible_vectors']}
        points = set(map(tuple, guards[idx]['guards']))
        for g in preserving:
            def apply(v):
                return tuple(sum(x * y for x, y in zip(row, v)) for row in g['matrix'])
            def up_to_sign(v):
                return v if next(x for x in v if x) > 0 else tuple(-x for x in v)
            need({up_to_sign(apply(v)) for v in vectors} == vectors,
                 'gauge-vector subgroup invariance')
            need({tuple(x + y for x, y in zip(apply(v), g['translation']))
                  for v in points} == points, 'finite-guard subgroup invariance')
        representatives.update((idx, tuple(orbit[0])) for orbit in orbits)
        report.append({'class_index': idx, 'full_group_order': len(full),
                       'height_group_order': len(preserving), 'extrema_orbits': orbits,
                       'guard_count': len(points), 'gauge_direction_count': len(vectors),
                       'guards_and_gauges_invariant': True})
    return representatives, report


def coverage(data, expected):
    actual = [(c['class_index'], tuple(c['extrema'])) for c in data['charts']]
    need(len(actual) == len(set(actual)) and set(actual) == expected,
         'all eight distinct representative charts')
    allkeys = [(r['class_index'], tuple(r['extrema']), r['node']) for r in data['queries']]
    need(len(allkeys) == len(set(allkeys)), 'unique query records')
    need(all((idx, ext) in expected for idx, ext, _ in allkeys), 'no unaccounted chart')
    report = []
    for chart in data['charts']:
        idx, ext = chart['class_index'], tuple(chart['extrema'])
        rows = [r for r in data['queries']
                if r['class_index'] == idx and tuple(r['extrema']) == ext]
        queue = deque([('r', ((Q(0), Q(1)), (Q(0), Q(1))))])
        closed, unknown = [], []
        for row in rows:
            need(bool(queue), 'no queries below already closed cover')
            tag, box = queue.popleft()
            need(row['node'] == tag, 'exact breadth-first node order')
            need(tuple(tuple(map(Q, r)) for r in row['box']) == box,
                 'exact closed dyadic rectangle')
            if row['status'] == 'unsat':
                closed.append(tag)
                continue
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
        pending = [{'node': tag, 'box': [[str(x) for x in r] for r in box]}
                   for tag, box in queue]
        need(chart['queries'] == len(rows), 'exact query count')
        need(chart['closed_leaves'] == closed, 'exact closed frontier')
        need(chart['pending_leaves'] == pending, 'exact pending frontier')
        need(chart['complete_cover'] == (not queue), 'honest complete-cover flag')
        area = sum((Q(1, 2 ** (len(t) - 1)) for t in closed), Q(0))
        rest = sum((Q(1, 2 ** (len(t) - 1)) for t, _ in queue), Q(0))
        need(area + rest == 1, 'closed plus pending exact area one')
        report.append({'class_index': idx, 'extrema': ext, 'queries': len(rows),
                       'unsat_labelled_leaves': len(closed), 'covered_area': str(area),
                       'pending_leaves': len(queue), 'pending_area': str(rest),
                       'complete_cover': not queue, 'unknown_nodes': unknown})
    return report


def mutations(data, expected_reps, guards, scans, control):
    expected, actual, gauges, envelopes = control
    tests = []
    missing = deepcopy(data)
    missing['queries'] = [r for r in missing['queries']
                          if not (r['class_index'] == 4 and r['extrema'] == [0, 1])]
    tests.append(expect_rejection('missing class4 root leaf',
                                  lambda: coverage(missing, expected_reps)))
    gap = deepcopy(data)
    gap['queries'][0]['box'][0][1] = '99/100'
    tests.append(expect_rejection('gap in full root rectangle',
                                  lambda: coverage(gap, expected_reps)))
    fake = deepcopy(data)
    fake['charts'][-1]['complete_cover'] = True
    tests.append(expect_rejection('partial class5 mislabeled complete',
                                  lambda: coverage(fake, expected_reps)))
    orbit = deepcopy(data)
    orbit['classes'][0]['extrema_orbits'].pop()
    tests.append(expect_rejection('missing extrema orbit',
                                  lambda: geometry_audit(orbit, guards, scans)))
    subgroup = deepcopy(data)
    subgroup['classes'][0]['height_automorphisms'][1]['height_sign'] = 1
    tests.append(expect_rejection('wrong height-reversal sign',
                                  lambda: geometry_audit(subgroup, guards, scans)))
    key = canonical(z3.simplify(gauges[0]))
    deleted = [e for e in actual if canonical(z3.simplify(e)) != key]
    need(len(deleted) < len(actual), 'mutation removed an actual gauge')
    tests.append(expect_rejection('missing necessary gauge assertion',
                                  lambda: compare(expected, deleted)))
    tests.append(expect_rejection('extra contradictory assertion',
                                  lambda: compare(expected, actual + [z3.BoolVal(False)])))
    key = canonical(z3.simplify(envelopes[0]))
    changed = [e for e in actual if canonical(z3.simplify(e)) != key]
    need(len(changed) < len(actual), 'mutation removed an actual envelope')
    changed.append(envelopes[0].arg(0) >= envelopes[0].arg(1) + z3.RealVal('1/100'))
    tests.append(expect_rejection('overrestrictive product envelope',
                                  lambda: compare(expected, changed)))
    return tests


def main():
    archive = ROOT / 'results/det5_height_interval.json'
    guard_path = ROOT / 'certificates/nonunimodular_observer_guards.json'
    scan_path = ROOT / 'results/two_vector_class_scan.json'
    data = json.loads(archive.read_text())
    guard_data = json.loads(guard_path.read_text())
    guard_validation = verify_guards(guard_data)
    guards = {c['class_index']: c for c in guard_data['classes']}
    scans = {c['class_index']: c for c in json.loads(scan_path.read_text())['classes']}
    expected_reps, groups = geometry_audit(data, guards, scans)
    charts = coverage(data, expected_reps)
    hashes, control = [], None
    for row in data['queries']:
        idx, ext = row['class_index'], tuple(row['extrema'])
        path = f'results/det5_height_{idx}_{ext[0]}_{ext[1]}_{row["node"]}.smt2'
        need(row['path'] == path, 'canonical determinant-five archive path')
        box = tuple(tuple(map(Q, r)) for r in row['box'])
        expected, gauges, envelopes = expected_assertions(guards[idx], scans[idx], ext, box)
        actual = list(z3.parse_smt2_file(str(ROOT / path)))
        compare(expected, actual)
        hashes.append({'path': path, 'sha256': hashlib.sha256((ROOT / path).read_bytes()).hexdigest()})
        if idx == 4 and ext == (0, 1) and row['node'] == 'r':
            control = expected, actual, gauges, envelopes
    need(control is not None, 'class4 root mutation control')
    rejection_results = mutations(data, expected_reps, guards, scans, control)
    report = {'status': 'PASS', 'solver_queries_run': 0, 'unsat_outcomes_verified': False,
              'query_count': len(hashes), 'geometry': groups, 'charts': charts,
              'guard_certificate_validation': guard_validation,
              'mutations': rejection_results, 'archived_files': hashes,
              'source_hashes': {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
                                for p in (archive, guard_path, scan_path)},
              'scope': 'Independent exact affine groups, chosen-height subgroups, extrema '
                       'coverage, guard replay, all assertion sets and complete/partial dyadic '
                       'frontiers. Prior independent formula reconstruction reused; no discovery '
                       'imports or solver queries. UNSAT outcomes require a separate proof check.'}
    (ROOT / 'results/det5_height_encoding_validation.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({'status': 'PASS', 'query_count': len(hashes),
                      'complete_charts': sum(c['complete_cover'] for c in charts),
                      'partial_charts': sum(not c['complete_cover'] for c in charts),
                      'pending_leaves': sum(c['pending_leaves'] for c in charts),
                      'rejected_mutations': len(rejection_results), 'solver_queries_run': 0}))


if __name__ == '__main__':
    main()
