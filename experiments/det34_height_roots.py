"""One-time strong-gauge necessary Y-height root queries for classes 2 and 3.

Retains the generic model's coarse gauges and adds beta=183/500 with the
actual determinant and contact parameter. No determinant-five geometry is
hardcoded. Every archived query is skipped on subsequent invocations.
SAT is an outer-relaxation assignment, UNKNOWN is not infeasibility, and
UNSAT requires independent proof checking before supporting an exclusion.
"""
from fractions import Fraction as Q
from pathlib import Path
import hashlib
import json
import time
import z3
from experiments.det5_height_interval import symmetries
from experiments.height_interval_relaxation import make
from experiments.contact_contraction_trace_probe import ell

ROOT = Path(__file__).resolve().parents[1]
ARCHIVE = ROOT / 'results/det34_height_roots.json'
BETA = Q(183, 500)


def main():
    guard_data = json.loads((ROOT / 'certificates/nonunimodular_observer_guards.json').read_text())
    scans = json.loads((ROOT / 'results/two_vector_class_scan.json').read_text())
    data = json.loads(ARCHIVE.read_text()) if ARCHIVE.exists() else {
        'scope': 'Necessary Y-height root-square relaxations at target17/5 for full relative-interior facet-contact classes2,3. Strong183/500 gauges added to coarse37/102 model. No rank lemma transfer. A class exclusion requires a complete independent proof chain.',
        'target': '17/5', 'strong_beta': str(BETA), 'coarse_beta': '37/102',
        'z3_version': z3.get_version_string(), 'classes': [], 'queries': []}
    for idx in (2, 3):
        C = next(c for c in guard_data['classes'] if c['class_index'] == idx)
        scan = next(c for c in scans['classes'] if c['class_index'] == idx)
        full, group, orbits = symmetries(C['contact_points'])
        assert [p[1] for p in C['contact_points']] == [0, 1, 1, 0]
        vectors = sorted(set(map(tuple, C['primitive_contact_edge_directions'])) |
                         {tuple(r['vector']) for r in scan['eligible_vectors']})
        d, a = C['normalized_volume'], C['contact_points'][1][2]
        if not any(c['class_index'] == idx for c in data['classes']):
            data['classes'].append({'class_index': idx, 'contact_points': C['contact_points'],
                                   'determinant': d, 'parameter': a, 'full_automorphisms': full,
                                   'height_automorphisms': group, 'extrema_orbits': orbits,
                                   'guard_count': len(C['guards']), 'gauge_vectors': vectors})
        for orbit in orbits:
            ext = list(orbit[0])
            if any(r['class_index'] == idx and r['extrema'] == ext for r in data['queries']):
                print('Already archived, skipped: ' + str((idx, ext)), flush=True)
                continue
            box = [[Q(0), Q(1)], [Q(0), Q(1)]]
            solver, F, _, _, _ = make(C, scan, ext, box)
            for v in vectors:
                l = ell(v, d, a)
                values = [sum(F[i][j] * z3.RealVal(str(l[j])) for j in range(4)) for i in range(4)]
                solver.add(z3.Or(*[sum(values[i] for i in range(4) if mask & (1 << i)) > z3.RealVal(str(BETA))
                                   for mask in range(1, 15)]))
            solver.set(timeout=1000)
            path = f'results/det34_height_root_{idx}_{ext[0]}_{ext[1]}.smt2'
            raw = solver.to_smt2().encode()
            (ROOT / path).write_bytes(raw)
            start = time.monotonic()
            status = solver.check()
            row = {'class_index': idx, 'extrema': ext, 'orbit': orbit, 'node': 'r',
                   'box': [['0', '1'], ['0', '1']], 'status': str(status),
                   'elapsed_seconds': time.monotonic() - start, 'timeout_ms': 1000,
                   'path': path, 'input_sha256': hashlib.sha256(raw).hexdigest()}
            if status == z3.unknown:
                row['reason_unknown'] = solver.reason_unknown()
            elif status == z3.sat:
                model = solver.model()
                row['relaxed_assignment'] = {str(v): str(model[v]) for v in model}
            data['queries'].append(row)
            ARCHIVE.write_text(json.dumps(data, indent=2) + '\n')
            print(json.dumps({k: row[k] for k in ('class_index', 'extrema', 'status', 'elapsed_seconds')}), flush=True)
        outcomes = [r['status'] for r in data['queries'] if r['class_index'] == idx]
        print(json.dumps({'class_index': idx, 'root_count': len(outcomes),
                          'all_roots_reported_unsat': len(outcomes) == len(orbits) and all(s == 'unsat' for s in outcomes)}), flush=True)


if __name__ == '__main__':
    main()
