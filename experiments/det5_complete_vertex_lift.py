"""Complete d5a2 width targets with an exact bilinear vertex lift.

The affine contact equations force invertibility; all 15 primitive covectors
of contact width <=3 are tested. Default bounded queries are archived once.
UNKNOWN never means an exclusion. Prior height archives are read only.
"""
from fractions import Fraction as Q
from itertools import combinations
from pathlib import Path
import argparse, hashlib, json, time
import z3
from experiments.contact_contraction_trace_probe import build, ell
from experiments.nonunimodular_complete_smt import make as cubic_make, width_directions
from experiments.det5_height_fiber_witness import inverse

ROOT = Path(__file__).resolve().parents[1]
BETA = Q(183, 500)
TARGET = Q(17, 5)
ARCHIVE = ROOT / 'results/det5_complete_vertex_lift.json'


def rat(x):
    return z3.RealVal(str(x))


def gauges(solver, F, vectors):
    for v in vectors:
        l = ell(v, 5, 2)
        values = [sum(F[i][j] * rat(l[j]) for j in range(4)) for i in range(4)]
        solver.add(z3.Or(*[sum(values[i] for i in range(4) if mask & (1 << i)) > rat(BETA)
                           for mask in range(1, 15)]))


def make(C, scan, threshold=TARGET, volume_bounds=True):
    base, F, vectors = build(C, scan, include_trace=False)
    replacements = []
    for j in range(4):
        ids = [i for i in range(4) if i != j]
        replacements.append((F[ids[2]][j], 1-F[ids[0]][j]-F[ids[1]][j]))
    F = [[z3.simplify(z3.substitute(v, *replacements)) for v in row] for row in F]
    solver = z3.SolverFor('QF_NRA')
    solver.add(*[z3.simplify(z3.substitute(c, *replacements)) for c in base.assertions()])
    gauges(solver, F, vectors)
    V = [[z3.Real(f'v{i}_{k}') for k in range(3)] for i in range(4)]
    for j in range(4):
        for k in range(3):
            solver.add(sum(V[i][k]*F[i][j] for i in range(4)) == C['contact_points'][j][k])
    if volume_bounds:
        # vol(conv(P,v))/vol(P) = sum_j max(lambda_j(v),0).
        # A global-width target forces vol(K)<beta^-3 by Minkowski/ACMS.
        cap = Q(6, 5)/BETA**3
        for x, y, z in V:
            bary = [1+rat(Q(2,5))*x-y-z, x/5, y-x/5, z-rat(Q(2,5))*x]
            for mask in range(1, 16):
                solver.add(sum(bary[j] for j in range(4) if mask & (1 << j)) < rat(cap))
    directions = width_directions(5, 2)
    for u in directions:
        values = [sum(u[k]*v[k] for k in range(3)) for v in V]
        solver.add(z3.Or(*[sign*(values[i]-values[j]) > rat(threshold)
                           for i, j in combinations(range(4), 2) for sign in (-1, 1)]))
    return solver, F, V, directions, vectors


def pinned_control(solver, F, V, pin):
    replacements = []
    for j in range(4):
        ids = [i for i in range(4) if i != j]
        for i in ids[:2]:
            replacements.append((F[i][j], rat(pin[i][j])))
    if V is not None:
        T = inverse(pin)
        P = [[0,0,0], [5,1,2], [0,1,0], [0,0,1]]
        actual = [[sum(Q(P[i][k])*T[i][j] for i in range(4)) for k in range(3)] for j in range(4)]
        replacements += [(V[i][k], rat(actual[i][k])) for i in range(4) for k in range(3)]
    evaluated = [z3.simplify(z3.substitute(c, *replacements)) for c in solver.assertions()]
    if any(not(z3.is_true(c) or z3.is_false(c)) for c in evaluated):
        raise ValueError('Control substitution left symbolic terms')
    return {'true':sum(z3.is_true(c) for c in evaluated), 'false':sum(z3.is_false(c) for c in evaluated)}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--timeout-ms', type=int, default=20000)
    args = parser.parse_args()
    if args.timeout_ms <= 0:
        raise ValueError('positive timeout')
    C = next(c for c in json.loads((ROOT/'certificates/nonunimodular_observer_guards.json').read_text())['classes'] if c['class_index']==5)
    S = next(c for c in json.loads((ROOT/'results/two_vector_class_scan.json').read_text())['classes'] if c['class_index']==5)
    pin = [[Q(x) for x in row] for row in json.loads((ROOT/'results/det5_strong_fiber.json').read_text())['F']]
    data = json.loads(ARCHIVE.read_text()) if ARCHIVE.exists() else {
        'scope':'Complete class5 global-width targets at17/5; necessary strong gauge and optional volume cuts. SAT needs independent reconstruction; UNKNOWN gives no exclusion.',
        'class_index':5, 'target':str(TARGET), 'beta':str(BETA), 'z3_version':z3.get_version_string(), 'queries':[]}
    for name, bounded in [('bilinear',False), ('bilinear_volume',True), ('cubic_strong',True)]:
        if any(row['model']==name for row in data['queries']):
            print('Already archived, skipped: '+name, flush=True)
            continue
        if name.startswith('bilinear'):
            solver,F,V,directions,vectors = make(C,S,volume_bounds=bounded)
            positive,PF,PV,_,_ = make(C,S,threshold=Q(13,5),volume_bounds=bounded)
        else:
            solver,F,delta,directions,vectors = cubic_make(C,S)
            gauges(solver,F,vectors)
            solver.add(z3.Or(delta>rat(Q(5,6)*BETA**3), -delta>rat(Q(5,6)*BETA**3)))
            V = None
            positive,PF,_,_,_ = cubic_make(C,S,Q(13,5))
            gauges(positive,PF,vectors)
            PV = None
        controls = {'width_13_over_5':pinned_control(positive,PF,PV,pin),
                    'width_17_over_5':pinned_control(solver,F,V,pin)}
        if controls['width_13_over_5']['false'] or not controls['width_17_over_5']['false']:
            raise ValueError('Pinned exact control failure')
        solver.set(timeout=args.timeout_ms)
        path = 'results/det5_complete_'+name+'.smt2'
        raw = solver.to_smt2().encode()
        (ROOT/path).write_bytes(raw)
        start = time.monotonic()
        status = solver.check()
        row = {'model':name,'path':path,'input_sha256':hashlib.sha256(raw).hexdigest(),
               'width_directions':directions,'gauge_vectors':vectors,'guard_count':len(C['guards']),
               'controls':controls,'timeout_ms':args.timeout_ms,'status':str(status),
               'elapsed_seconds':time.monotonic()-start}
        if status==z3.unknown:
            row['reason_unknown']=solver.reason_unknown()
        elif status==z3.sat:
            model=solver.model()
            row['assignment']={str(v):str(model[v]) for v in model}
        data['queries'].append(row)
        ARCHIVE.write_text(json.dumps(data,indent=2)+'\n')
        print(json.dumps({k:row[k] for k in ('model','status','elapsed_seconds')}),flush=True)


if __name__=='__main__':
    main()
