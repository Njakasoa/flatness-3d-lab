"""Finite empty contact-hull extensions after the ten-tetrahedron reduction.

Candidate output, requiring independent review. Exact integer arithmetic only.
Every empty 3-polytope with >=5 vertices contains a unimodular tetrahedron:
Howe width one puts >=3 vertices in one layer, an empty unimodular triangle,
and a vertex in the other layer completes it. All tetrahedra selected from
its vertices are empty, so the ten-type restriction applies to each of them.
Their determinants <=13 bound every additional point q relative to a fixed
unimodular frame by |q_i|<=13 and |1-sum(q_i)|<=13.
"""
from itertools import combinations,permutations,product
from functools import lru_cache
from math import gcd
from pathlib import Path
import json
from sympy import Matrix
from sympy.matrices.normalforms import hermite_normal_form
from enumeration.empty_tetrahedra import determinant_3x3 as det,adjugate_3x3 as adj

FRAME=((0,0,0),(1,0,0),(0,1,0),(0,0,1))
HEIGHTS=tuple(h for h in product((0,1),repeat=3) if any(h))

def sub(a,b):return tuple(x-y for x,y in zip(a,b))
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def matrix(frame):return tuple(zip(*(sub(p,frame[0]) for p in frame[1:])))

@lru_cache(None)
def triangle_ok(t):
    a,b=sub(t[1],t[0]),sub(t[2],t[0])
    return gcd(a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])==1

def ordered_hnf(frame):
    h=hermite_normal_form(Matrix(matrix(frame)).T).T
    return tuple(int(x) for x in h)

def allowed_ordered_hnfs():
    cases=json.loads(Path('certificates/contact_obstructions.json').read_text())['cases']
    allowed=set()
    for c in cases:
        if c['survives_threshold_11A_over_7']:
            allowed.update(ordered_hnf(f) for f in permutations(c['vertices']))
    return allowed

ALLOWED=None
@lru_cache(None)
def tetra_ok(t):
    n=abs(det(matrix(t)))
    if n==0:return True  # Layer tests and primitive triangles handle the square.
    if n>13:return False
    return ordered_hnf(t) in ALLOWED

@lru_cache(None)
def canonical(points):
    """Complete affine GL3Z invariant for finite sets with a unimodular frame."""
    best=None
    for f in permutations(points,4):
        b=matrix(f);d=det(b)
        if abs(d)!=1:continue
        inv=adj(b)
        key=tuple(sorted(tuple(d*dot(row,sub(p,f[0])) for row in inv) for p in points))
        if best is None or key<best:best=key
    if best is None:raise ValueError('No unimodular frame')
    return best

def extension_ok(p,q):
    # Exact width-one layer certificate. All possible directions on FRAME
    # arise by assigning binary heights, with height(0)=0 up to sign.
    if not any(all(dot(h,v) in (0,1) for v in (*p,q)) for h in HEIGHTS):return False
    if any(not triangle_ok(tuple(sorted((*t,q)))) for t in combinations(p,2)):return False
    if any(not tetra_ok(tuple(sorted((*t,q)))) for t in combinations(p,3)):return False
    return True

def main():
    global ALLOWED
    ALLOWED=allowed_ordered_hnfs()
    raw=[q for q in product(range(-13,14),repeat=3)
         if abs(1-sum(q))<=13 and q not in FRAME]
    pool=[q for q in raw if extension_ok(FRAME,q)]
    levels={4:{canonical(FRAME)}}
    # A canonical form includes FRAME, because each tested change sends a
    # unimodular frame exactly to FRAME. Thus the same finite pool applies.
    for size in range(5,9):
        out=set();accepted=0
        for p in sorted(levels[size-1]):
            assert set(FRAME)<=set(p)
            for q in pool:
                if q in p or not extension_ok(p,q):continue
                accepted+=1;out.add(canonical(tuple(sorted((*p,q)))))
        levels[size]=out
        print(json.dumps({'vertices':size,'classes':len(out),'accepted_extensions_before_quotient':accepted}),flush=True)
    result={'status':'exact_candidate_enumeration_pending_independent_review',
       'threshold':'w(K)>(11/7)*(1+2/sqrt(3))',
       'scope':'Full-dimensional empty lattice contact hulls with five to eight vertices, tetrahedron-wise necessary obstruction only',
       'coordinate_bound':13,'raw_extension_points':len(raw),
       'admissible_extensions_of_standard_frame':len(pool),
       'allowed_ordered_tetrahedron_hnfs':len(ALLOWED),
       'counts':{str(k):len(v) for k,v in levels.items() if k>=5},
       'classes':[{'vertices':[list(p) for p in P],
                   'width_one_direction':list(next(h for h in HEIGHTS if all(dot(h,p) in (0,1) for p in P)))}
                   for n in range(5,9) for P in sorted(levels[n])]}
    Path('results/contact_extensions.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='classes'},indent=2))

if __name__=='__main__':main()
