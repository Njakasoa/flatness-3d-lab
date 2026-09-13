"""At most 16 new exact midpoint fibers of a fixed simultaneous-height archive.

The source cover is read only. A nonsingular SAT witness would concern the
two prescribed directions, never imply a large global lattice width.
"""
from fractions import Fraction as Q
from pathlib import Path
from itertools import product
from math import floor, ceil, gcd, prod
import hashlib
import json
import time
import z3
from experiments.det5_joint_height_interval import make, U
from experiments.det5_height_fiber_witness import inverse
from experiments.contact_contraction_trace_probe import certify, ell

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'results/det5_joint_height_interval.json'
ARCHIVE = ROOT / 'results/det5_joint_fibers.json'


def save(data):
    ARCHIVE.write_text(json.dumps(data, indent=2) + '\n')


def main():
    raw = SOURCE.read_bytes()
    source = json.loads(raw)
    C = next(c for c in json.loads((ROOT/'certificates/nonunimodular_observer_guards.json').read_text())['classes'] if c['class_index'] == 5)
    S = next(c for c in json.loads((ROOT/'results/two_vector_class_scan.json').read_text())['classes'] if c['class_index'] == 5)
    data = json.loads(ARCHIVE.read_text()) if ARCHIVE.exists() else {
        'scope': 'Exact midpoint fibers of pending simultaneous Y/U height boxes. UNSAT excludes only a fiber; SAT needs exact invertibility and body checks and does not imply large global width.',
        'source_sha256': hashlib.sha256(raw).hexdigest(), 'source_query_count': len(source['queries']),
        'class_index': 5, 'beta': '183/500', 'target': '17/5',
        'z3_version': z3.get_version_string(), 'maximum_queries': 16, 'queries': []}
    if data['source_sha256'] != hashlib.sha256(raw).hexdigest():
        raise ValueError('Source cover changed; preserve provenance')
    if any(row.get('invertible') for row in data['queries']):
        print('An invertible witness is already archived; no repeated query')
        return
    # Prioritize the least closed charts; cycle Y charts within each stratum.
    charts = [c for c in source['charts'] if c['pending_leaves']]
    ordered = []
    for count in sorted({len(c['closed_leaves']) for c in charts}):
        queues = {tuple(y): [c for c in charts if c['Y_extrema'] == y and len(c['closed_leaves']) == count]
                  for y in ([0, 1], [0, 3], [1, 0])}
        while any(queues.values()):
            for key in queues:
                if queues[key]:
                    ordered.append(queues[key].pop(0))
    for number, chart in enumerate(ordered[:16]):
        if number < len(data['queries']):
            continue
        leaf = chart['pending_leaves'][0]
        midpoint = [sum(map(Q, pair))/2 for pair in leaf['box']]
        box = [[v, v] for v in midpoint]
        Yext, Uext = chart['Y_extrema'], chart['U_extrema']
        solver, F, q, r, a, b, offset, gap = make(C, S, Yext, Uext, box)
        path = f'results/det5_joint_fiber_{number:02d}.smt2'
        (ROOT/path).write_text(solver.to_smt2())
        start = time.monotonic()
        status = solver.check()
        row = {'Y_extrema': Yext, 'U_extrema': Uext, 'source_node': leaf['node'],
               'source_box': leaf['box'], 'midpoint': list(map(str, midpoint)),
               'path': path, 'status': str(status), 'elapsed_seconds': time.monotonic()-start,
               'timeout_ms': 1000}
        data['queries'].append(row)
        if status == z3.unknown:
            row['reason_unknown'] = solver.reason_unknown()
        if status == z3.sat:
            model = solver.model()
            val = lambda x: model.eval(x, model_completion=True).as_fraction()
            matrix = [[val(x) for x in line] for line in F]
            row.update(F=[[str(x) for x in line] for line in matrix],
                       Y_normalized=list(map(str, map(val, q))), U_normalized=list(map(str, map(val, r))),
                       Y_offset=str(val(a)), Y_gap=str(val(b)), U_offset=str(val(offset)), U_gap=str(val(gap)))
            # Preserve rational SAT assignments before potentially heavy work.
            save(data)
            try:
                T = inverse(matrix)
            except ValueError:
                row['invertible'] = False
            else:
                row['invertible'] = True
                P = C['contact_points']
                V = [[sum(Q(P[i][k])*T[i][j] for i in range(4)) for k in range(3)] for j in range(4)]
                row['rational_vertices'] = [[str(x) for x in v] for v in V]
                directional = [max(sum(Q(u[k])*v[k] for k in range(3)) for v in V)-min(sum(Q(u[k])*v[k] for k in range(3)) for v in V) for u in ((0,1,0), U)]
                assert all(w > Q(17,5) for w in directional)
                assert directional == [1/val(b), 1/val(gap)]
                row['directional_widths'] = list(map(str, directional))
                boxcount = prod(max(0, floor(max(v[k] for v in V))-ceil(min(v[k] for v in V))+1) for k in range(3))
                row['integer_body_box_count'] = boxcount
                save(data)
                if boxcount <= 50000:
                    row['exact_body'] = certify(matrix, P)
                    save(data)
                    bounds = [floor(max(v[k] for v in V)-min(v[k] for v in V)) for k in range(3)]
                    if prod(2*x+1 for x in bounds) <= 100000:
                        minimum, best = Q(1), []
                        for z in product(*(range(-x,x+1) for x in bounds)):
                            if not any(z) or next(x for x in z if x) < 0 or gcd(*z) != 1:
                                continue
                            l = ell(z,5,2)
                            gamma = sum(abs(sum(matrix[i][j]*l[j] for j in range(4))) for i in range(4))/2
                            if gamma < minimum:
                                minimum, best = gamma, [z]
                            elif gamma == minimum:
                                best.append(z)
                        row['full_difference_minimum'] = str(minimum)
                        row['minimizing_vectors'] = best
        save(data)
        print(json.dumps({k: row[k] for k in ('Y_extrema','U_extrema','source_node','status','elapsed_seconds')}), flush=True)
        if row.get('invertible'):
            break
    assert SOURCE.read_bytes() == raw


if __name__ == '__main__':
    main()
