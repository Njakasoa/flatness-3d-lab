"""Exact finite arithmetic underlying DET5_VOLUME_GAP_BOUNDS.md.

No solver, model generator, or main geometry engine. This replays the
multiaffine vertex maxima; the continuous reduction is proved in the note.
"""
from fractions import Fraction as Q
from itertools import combinations, product
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]


def det(A):
    A = [list(map(Q, row)) for row in A]
    out = Q(1)
    for i in range(len(A)):
        p = next((p for p in range(i, len(A)) if A[p][i]), None)
        if p is None:
            return Q(0)
        if p != i:
            A[p], A[i] = A[i], A[p]
            out = -out
        pivot = A[i][i]
        out *= pivot
        for p in range(i + 1, len(A)):
            ratio = A[p][i] / pivot
            A[p] = [x - ratio*y for x,y in zip(A[p], A[i])]
    return out


def ell(v):
    x, y, z = v
    return [Q(2*x,5)-y-z, Q(x,5), y-Q(x,5), z-Q(2*x,5)]


def check():
    beta = Q(183,500)
    configurations = [
        ('Y', (0,1,0), (1,0,0), (2,0,1), (0,1,0), Q(1,5)),
        ('U', (1,-1,-2), (1,1,0), (2,0,1), (1,0,0), Q(2,5)),
    ]
    records = []
    for name, covector, v1, v2, transversal, expected in configurations:
        dot = lambda a,b: sum(x*y for x,y in zip(a,b))
        assert dot(covector,v1) == dot(covector,v2) == 0
        assert dot(covector,transversal) == 1
        B = list(zip(v1,v2,transversal))
        assert abs(det(B)) == 1
        C = list(zip(ell(v1),ell(v2),ell(transversal),[1,0,0,0]))
        assert abs(det(C)) == Q(1,5)
        a,b = ell(v1),ell(v2)
        maxima = {}
        witnesses = {}
        for i,j in combinations(range(4),2):
            maximum = Q(0)
            for destinations in product(range(4),repeat=4):
                r = [sum(a[c] for c in range(4) if destinations[c] == row) for row in range(4)]
                s = [sum(b[c] for c in range(4) if destinations[c] == row) for row in range(4)]
                value = abs(r[i]*s[j]-r[j]*s[i])
                if value > maximum:
                    maximum = value
                    witnesses[f'{i},{j}'] = list(destinations)
            assert maximum == expected
            maxima[f'{i},{j}'] = str(maximum)
        records.append({'direction':name,'covector':list(covector),
                        'kernel_basis':[list(v1),list(v2)],
                        'transversal':list(transversal),
                        'vertices_checked_per_minor':256,
                        'minor_maxima':maxima,'attaining_destinations':witnesses,
                        'strict_gap_lower_bound':str(beta**3/(6*expected)),
                        'strict_width_upper_bound':str(6*expected/beta**3)})
    scans = json.loads((ROOT/'results/two_vector_class_scan.json').read_text())
    eligible = {tuple(v['vector']) for c in scans['classes'] if c['class_index']==5 for v in c['eligible_vectors']}
    vectors = [(1,0,0),(2,0,1),(1,0,1),(3,0,1)]
    assert set(vectors) <= eligible
    masses = [sum(map(abs,ell(v)))/2 for v in vectors]
    assert masses == [Q(3,5),Q(3,5),Q(4,5),Q(4,5)]
    g = 2*beta-Q(3,5)
    assert g == Q(33,250) and g > 0
    lower_minor = beta*g/4
    assert lower_minor == Q(6039,500000)
    upperA = Q(17,5)*(1-beta)
    assert upperA > 1 and 3*(upperA-1)**2 > 4
    return {'status':'PASS','beta':str(beta),
            'scope':'Exact finite arithmetic; continuous multiaffine and rank arguments are in the accompanying proof. Not a class exclusion or a solver proof.',
            'rank_vectors':[list(v) for v in vectors],
            'intrinsic_masses':list(map(str,masses)),
            'rank_margin':str(g),'strict_Y_minor_lower_bound':str(lower_minor),
            'directions':records}


if __name__ == '__main__':
    result = check()
    (ROOT/'results/det5_volume_gap_bounds_validation.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
