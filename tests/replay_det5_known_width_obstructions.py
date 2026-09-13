"""Exact width tables and finite set covers for five archived d5a2 witnesses.

Uses stdlib only, reconstructs from F, and issues no solver queries. Set-cover
claims concern this finite witness collection and its four contact symmetries.
"""
from fractions import Fraction as Q
from itertools import product, permutations, combinations
from pathlib import Path
from math import gcd
import hashlib
import json

ROOT = Path(__file__).resolve().parents[1]
P = ((0, 0, 0), (5, 1, 2), (0, 1, 0), (0, 0, 1))
TARGET = Q(17, 5)
Y, U, Z = (0, 1, 0), (1, -1, -2), (0, 0, 1)


def need(c, message):
    if not c:
        raise ValueError(message)


def dot(a, b):
    return sum(x*y for x, y in zip(a, b))


def inverse(matrix):
    n = len(matrix)
    a = [[Q(x) for x in row]+[Q(i == j) for j in range(n)] for i, row in enumerate(matrix)]
    for j in range(n):
        pivot = next((i for i in range(j, n) if a[i][j]), None)
        need(pivot is not None, 'invertibility')
        a[j], a[pivot] = a[pivot], a[j]
        t = a[j][j]
        a[j] = [x/t for x in a[j]]
        for i in range(n):
            if i != j:
                t = a[i][j]
                a[i] = [x-t*y for x, y in zip(a[i], a[j])]
    return [r[n:] for r in a]


def rank(matrix):
    a = [[Q(x) for x in r] for r in matrix]
    r = 0
    for j in range(3):
        p = next((i for i in range(r, len(a)) if a[i][j]), None)
        if p is None:
            continue
        a[r], a[p] = a[p], a[r]
        t = a[r][j]
        a[r] = [x/t for x in a[r]]
        for i in range(len(a)):
            if i != r:
                t = a[i][j]
                a[i] = [x-t*y for x, y in zip(a[i], a[r])]
        r += 1
    return r


def det3(a):
    return sum(a[0][j]*(a[1][(j+1)%3]*a[2][(j+2)%3]-a[1][(j+2)%3]*a[2][(j+1)%3]) for j in range(3))


def canonical(u):
    return tuple(-x for x in u) if next(x for x in u if x) < 0 else tuple(u)


def width(vertices, u):
    h = [dot(v, u) for v in vertices]
    return max(h)-min(h)


def direction_key(u):
    return ','.join(map(str, u))


def geometry():
    # width(P,u)<=3 bounds |uY|,|uZ|<=3 and |5uX+uY+2uZ|<=3.
    # Consequently |uX|<=12/5, hence <=2 for integer covectors.
    directions = sorted({canonical(u) for u in product(range(-2,3), range(-3,4), range(-3,4))
                         if any(u) and gcd(*u)==1 and width(P,u)<=3})
    need(len(directions)==15, 'complete fifteen directions')
    B = inverse([[P[j+1][i] for j in range(3)] for i in range(3)])
    group = []
    for perm in permutations(range(4)):
        t = P[perm[0]]
        E = [[P[perm[j+1]][i]-t[i] for j in range(3)] for i in range(3)]
        A = [[sum(E[i][k]*B[k][j] for k in range(3)) for j in range(3)] for i in range(3)]
        if any(x.denominator!=1 for row in A for x in row):
            continue
        A = [[int(x) for x in row] for row in A]
        need(abs(det3(A))==1, 'unimodular contact automorphism')
        need(all(tuple(dot(row,p)+t[i] for i,row in enumerate(A))==P[perm[j]] for j,p in enumerate(P)), 'contact action')
        group.append({'permutation':perm, 'matrix':A, 'translation':t})
    need(len(group)==4, 'full contact group')
    remaining = set(directions)
    orbits = []
    while remaining:
        u = min(remaining)
        orbit = sorted({canonical(tuple(sum(g['matrix'][i][j]*u[i] for i in range(3)) for j in range(3))) for g in group})
        need(set(orbit)<=remaining, 'direction orbit partition')
        remaining -= set(orbit)
        orbits.append({'directions':orbit, 'contact_width':width(P,u), 'rank':rank(orbit)})
    return directions, group, orbits


def smallest_covers(samples, candidates):
    """All minimum-cardinality additional direction sets for the given samples."""
    alive = [s for s in samples if s['passes_Y_U']]
    sets = [{tuple(u) for u in s['directions_at_most_target']} for s in alive]
    for n in range(len(candidates)+1):
        covers = [c for c in combinations(candidates,n) if all(set(c)&bad for bad in sets)]
        if covers:
            return {'sample_ids':[s['id'] for s in alive], 'minimum_additional_count':n, 'all_minimum_sets':covers}
    raise ValueError('finite cover missing')


def main():
    directions, group, orbits = geometry()
    sources = [
        ('strong_fiber', 'results/det5_strong_fiber.json', None),
        ('symmetry', 'results/det5_joint_symmetry_witness.json', None),
        ('retained10', 'results/det5_joint_volume_gaps.json', 'retained_witness'),
        ('retained14', 'results/det5_joint_enriched_cover.json', 'retained_witness'),
        ('retained18', 'results/det5_joint_short_gauges.json', 'retained_witness'),
    ]
    bindings, samples, original, unique = [], [], [], set()
    for name, path, key in sources:
        raw = (ROOT/path).read_bytes()
        data = json.loads(raw)
        data = data[key] if key else data
        F = [list(map(Q,row)) for row in data['F']]
        need(len(F)==4 and all(len(r)==4 for r in F), 'F dimensions')
        need(all(F[i][i]==0 for i in range(4)), 'facet diagonal')
        need(all(F[i][j]>0 for i in range(4) for j in range(4) if i!=j), 'relative interior contacts')
        need(all(sum(F[i][j] for i in range(4))==1 for j in range(4)), 'contact stochasticity')
        Fi = inverse(F)
        V = [[sum(Q(P[i][k])*Fi[i][j] for i in range(4)) for k in range(3)] for j in range(4)]
        need(all(sum(V[i][k]*F[i][j] for i in range(4))==P[j][k] for j in range(4) for k in range(3)), 'reconstructed contacts')
        bindings.append({'name':name, 'path':path, 'key':key, 'sha256':hashlib.sha256(raw).hexdigest()})
        for g in group:
            transformed = [[dot(row,v)+g['translation'][i] for i,row in enumerate(g['matrix'])] for v in V]
            unique.add(tuple(sorted(tuple(v) for v in transformed)))
            # Restore the contact/facet labeling: g(p_i)=p_perm(i), so
            # g(v_i) receives label perm(i). Widths themselves do not change.
            relabeled = [None]*4
            for i, j in enumerate(g['permutation']):
                relabeled[j] = transformed[i]
            hY = [dot(v,Y) for v in relabeled]
            Y_extrema = [(i,j) for i in range(4) for j in range(4)
                         if hY[i]==min(hY) and hY[j]==max(hY)]
            retained_Y = bool(set(Y_extrema)&{(0,1),(0,3),(1,0)})
            widths = {u:width(transformed,u) for u in directions}
            # Independently check each table entry against the pullback action.
            for u in directions:
                pullback = tuple(sum(g['matrix'][i][j]*u[i] for i in range(3)) for j in range(3))
                need(widths[u]==width(V,pullback), 'covector pullback width identity')
            bad = [u for u in directions if widths[u]<=TARGET]
            need(bad, 'known sample has a small listed width')
            s = {'id':name+':'+''.join(map(str,g['permutation'])), 'witness':name,
                 'contact_permutation':g['permutation'], 'actual_relabeled_Y_extrema':Y_extrema, 'lies_in_retained_Y_chart':retained_Y,
                 'widths':{direction_key(u):str(widths[u]) for u in directions},
                 'directions_at_most_target':bad,
                 'full_lattice_width':str(min(widths.values())),
                 'minimizing_directions':[u for u in directions if widths[u]==min(widths.values())],
                 'passes_Y_U':all(widths[u]>TARGET for u in (Y,U)),
                 'passes_Y_U_Z':all(widths[u]>TARGET for u in (Y,U,Z))}
            samples.append(s)
            if g['permutation']==(0,1,2,3):
                original.append(s)
    candidates = [u for u in directions if u not in (Y,U)]
    original_cover = smallest_covers(original,candidates)
    orbit_cover = smallest_covers(samples,candidates)
    retained_cover = smallest_covers([s for s in samples if s['lies_in_retained_Y_chart']],candidates)
    selected = sorted([Z,(0,1,-1),(1,-2,-2)])
    need(original_cover['minimum_additional_count']==1 and original_cover['all_minimum_sets']==[(Z,)], 'unique original-orientation singleton Z')
    need(orbit_cover['minimum_additional_count']==3 and orbit_cover['all_minimum_sets']==[tuple(selected)], 'unique orbit-complete three-direction addition')
    need(any(s['passes_Y_U_Z'] for s in samples), 'rank-three YUZ is insufficient for known images')
    need(retained_cover['minimum_additional_count']==1 and retained_cover['all_minimum_sets']==[(Z,)], 'known retained images need only Z')
    need(all(not s['lies_in_retained_Y_chart'] for s in samples if s['passes_Y_U_Z']), 'known YUZ survivors are outside retained charts')
    low_width = [u for u in directions if width(P,u)<=2]
    need(set(low_width)=={Y,U,*selected}, 'five contact-width-at-most-two directions')
    minimality_forcing = [s['id'] for s in samples if s['passes_Y_U'] and len(s['directions_at_most_target'])==1]
    result = {'status':'PASS', 'scope':'Finite known-witness width tables and set covers only; no universal sufficiency, class exclusion, or new flatness bound.',
              'target':str(TARGET), 'solver_queries':0, 'source_bindings':bindings,
              'directions':directions, 'contact_group':group, 'direction_orbits':orbits,
              'samples':samples, 'sample_count_with_duplicates':len(samples), 'distinct_geometric_samples':len(unique),
              'original_orientation_cover':original_cover, 'contact_symmetry_cover':orbit_cover, 'retained_chart_symmetry_cover':retained_cover,
              'forcing_singleton_samples':minimality_forcing,
              'survives_Y_U_Z':[s['id'] for s in samples if s['passes_Y_U_Z']],
              'direction_set_ranks':{'Y_U':rank([Y,U]), 'Y_U_Z':rank([Y,U,Z]), 'all_five_contact_width_at_most_two':rank(low_width), 'all_fifteen':rank(directions)},
              'Y_U_Z_determinant':det3([Y,U,Z]), 'five_contact_width_at_most_two':low_width}
    (ROOT/'results/det5_known_width_obstructions.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:result[k] for k in ('status','sample_count_with_duplicates','distinct_geometric_samples','original_orientation_cover','contact_symmetry_cover','retained_chart_symmetry_cover','survives_Y_U_Z','direction_set_ranks')},indent=2))


if __name__=='__main__':
    main()
