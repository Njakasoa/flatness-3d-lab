"""Symbolic finite check for the stochastic minor partition lemma.

A coefficient triple represents det(c0,c1), det(c0,c2), det(c1,c2),
where c3=-c0-c1-c2. The proof of continuous interpolation and geometry
is in SIMPLEX_WIDTH_VOLUME_MONOTONICITY.md. No geometry or solver imports.
"""
from itertools import product, combinations
from pathlib import Path
import json

ROOT=Path(__file__).resolve().parents[1]
BASE=((1,0,0),(0,1,0),(0,0,1),(-1,-1,-1))

def wedge(a,b):
    return (a[0]*b[1]-a[1]*b[0],
            a[0]*b[2]-a[2]*b[0],
            a[1]*b[2]-a[2]*b[1])

def negate(v):return tuple(-x for x in v)

def main():
    original={wedge(BASE[i],BASE[j]) for i,j in combinations(range(4),2)}
    allowed=original|{negate(v) for v in original}|{(0,0,0)}
    counts={};checks=0
    for i,j in combinations(range(4),2):
        attained=set()
        for destinations in product(range(4),repeat=4):
            rows=[tuple(sum(BASE[c][k] for c in range(4) if destinations[c]==row) for k in range(3)) for row in range(4)]
            minor=wedge(rows[i],rows[j]);assert minor in allowed
            attained.add(minor);checks+=1
        assert attained==allowed
        counts[f'{i},{j}']=len(attained)
    result={'status':'PASS','symbolic_partition_checks':checks,
            'original_minor_coefficient_vectors':[list(v) for v in sorted(original)],
            'distinct_attained_polynomials_per_row_pair':counts,
            'scope':'Universal symbolic verification of the four-column zero-sum partition lemma; continuous and geometric steps are proved in the note.',
            'solver_queries_run':0}
    (ROOT/'results/simplex_width_volume_partition_validation.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
if __name__=='__main__':main()
