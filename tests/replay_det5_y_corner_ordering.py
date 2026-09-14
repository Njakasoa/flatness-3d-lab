"""Exact identities and rational regressions for the actual-height ordering lemma.

Stdlib only. No solver calls and no imports of discovery generators.
"""
from fractions import Fraction as Q
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]


def add(*ps):
    out = {}
    for p in ps:
        for m, c in p.items():
            out[m] = out.get(m, Q(0)) + c
    return {m: c for m, c in out.items() if c}


def mul(p, q):
    out = {}
    for m, c in p.items():
        for n, d in q.items():
            key = tuple(a+b for a, b in zip(m, n))
            out[key] = out.get(key, Q(0)) + c*d
    return {m: c for m, c in out.items() if c}


def neg(p):
    return {m: -c for m, c in p.items()}


def main():
    one = {(0, 0, 0, 0): Q(1)}
    x, y, r, t = [{tuple(int(i == j) for i in range(4)): Q(1)} for j in range(4)]
    delta = add(y, neg(x))
    # z0=r>0, z3=-t<0; D z1= -y*r-(1-y)*t,
    # D z2=x*r+(1-x)*t. These are formal polynomial identities.
    n1 = neg(add(mul(y, r), mul(add(one, neg(y)), t)))
    n2 = add(mul(x, r), mul(add(one, neg(x)), t))
    assert not add(mul(delta, add(r, neg(t))), n1, n2)
    assert not add(mul(x, n1), mul(y, n2), neg(mul(delta, t)))
    assert not add(mul(delta, r), n2, neg(add(mul(y, r), mul(add(one, neg(x)), t))))
    assert not add(mul(delta, r), n1, add(mul(x, r), mul(add(one, neg(y)), t)))
    count = 0
    guard_comparisons = 0
    for denominator in (4, 7, 11):
        for a in range(denominator+1):
            for b in range(denominator+1):
                if a == b:
                    continue
                q1, q2 = Q(a, denominator), Q(b, denominator)
                low, high = sorted((q1, q2))
                D = high-low
                for s, v in ((Q(1, 20), Q(1, 30)), (Q(1, 17), Q(1, 13))):
                    F03, F30 = s*D, v*D
                    zp = low*s+(1-low)*v
                    zn = -high*s-(1-high)*v
                    F10 = Q(1, 2)
                    F20 = 1-F10-F30
                    z1, z2 = (zn, zp) if q1 < q2 else (zp, zn)
                    F13, F23 = F10+z1, F20+z2
                    offset = q1*F10+q2*F20+F30
                    assert low < offset < high
                    gap = (1-offset)/2
                    H = offset+gap
                    eps = min(H, 1-H)/4
                    F = [[0, 1-eps-(H-q2*eps), 1-eps-(H-q1*eps), F03],
                         [F10, 0, eps, F13],
                         [F20, eps, 0, F23],
                         [F30, H-q2*eps, H-q1*eps, 0]]
                    assert all(F[i][j] > 0 for i in range(4) for j in range(4) if i != j)
                    assert all(sum(F[i][j] for i in range(4)) == 1 for j in range(4))
                    q = [Q(0), q1, q2, Q(1)]
                    assert all(sum(q[i]*F[i][j] for i in range(4)) == offset+(gap if j in (1, 2) else 0) for j in range(4))
                    z = [F[i][3]-F[i][0] for i in range(4)]
                    assert z[0] > 0 and z[3] < 0
                    assert (z[1] < 0 < z[2]) if q1 < q2 else (z[2] < 0 < z[1])
                    gauge = sum(abs(c) for c in z)/2
                    assert gauge == F03+(z2 if q1 < q2 else z1)
                    assert gauge == (high*F03+(1-low)*F30)/D
                    # Exact reduction of guards (2,1,1) and (3,1,1).
                    g2 = [-F[i][0]+2*F[i][1]+3*F[i][2]+F[i][3] for i in range(4)]
                    g3 = [F[i][0]+3*F[i][1]+2*F[i][2]-F[i][3] for i in range(4)]
                    third = F30 >= 2*F[3][1]+3*F[3][2]
                    zeroth = F03 >= 3*F[0][1]+2*F[0][2]
                    if q1 < q2:
                        reduced2 = (-z1 >= 3*F[1][2]) or third
                        reduced3 = zeroth or (z2 >= 3*F[2][1])
                    else:
                        reduced2 = (-z2 >= 2*F[2][1]) or third
                        reduced3 = zeroth or (z1 >= 2*F[1][2])
                    assert any(c <= 0 for c in g2) == reduced2
                    assert any(c <= 0 for c in g3) == reduced3
                    guard_comparisons += 2
                    count += 1
    # At equal heights q1=q2=h, the two linear identities imply
    # h*z0-(1-h)*z3=0. Strict z0>0,z3<0 makes this impossible, also at h=0,1.
    for h in (Q(0), Q(1, 7), Q(3, 4), Q(1)):
        assert h*Q(2, 7)+(1-h)*Q(3, 11) > 0
    result = {'status': 'PASS', 'scope': 'Four formal polynomial identities; exact rational contact matrices over both height order branches, including endpoints; equivalent two-branch reductions of two integer guards. Written positivity proof supplies universal sign conclusions. No solver queries.',
              'formal_polynomial_identities': 4, 'exact_contact_matrix_regressions': count,
              'guard_equivalence_regressions': guard_comparisons,
              'proved_lemmas': ['equal free heights impossible for strict actual contacts',
                               'offset lies strictly between the two free heights',
                               'Z has fixed alternating row signs on each height order branch',
                               'Z gauge is one linear expression in F on each branch',
                               'guards (2,1,1) and (3,1,1) each reduce to two alternatives'],
              'solver_queries_run': 0,
              'limitation': 'No new numerical gauge threshold or complete domain exclusion follows from these lemmas alone.'}
    (ROOT/'results/det5_y_corner_ordering_validation.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
