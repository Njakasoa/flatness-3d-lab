# The fourteen-gauge formulation has another actual retained witness

Date: 2026-09-14. Status: independently checked rational witness and complete
intrinsic-gauge enumeration. No new contact-class exclusion follows.

The second `retained_witness`, in
[the enriched campaign](../results/det5_joint_enriched_cover.json), passes
all fourteen imposed gauge inequalities, both directional-width constraints,
and the volume-derived linear gap cuts. Its stochastic contact matrix is
invertible, has zero diagonal and strictly positive off-diagonal entries.
Thus all four prescribed contacts of P=conv(0,(5,1,2),e2,e3) lie in their
facet relative interiors.

The independent reconstruction gives:

| Quantity | Exact value |
|---|---|
| Y-width | 20766044221/4192650405 > 17/5 |
| U-width, U=(1,-1,-2) | 1016875379/279510027 > 17/5 |
| Global lattice width | 10682780276/4192650405 < 17/5 |
| Minimizing covector | (0,0,1) |
| Volume | 2588282117/559020054 < (500/183)^3 |
| Full difference-body minimum | 5671/20595 < 183/500 |
| Minimizing integer vector | (2,1,0) |
| Gauge at (1,1,0) | 1375/4119 < 183/500 |

All 135 integer points in the body bounding box are checked: none is
interior and seven are on the boundary. Complete finite searches check 47
primitive width directions and 307 primitive difference-body vectors modulo
sign. The actual normalized Y-extrema are [0,1] and U-extrema are [0,2]; the
replay verifies their exact bilinear identities. Their free heights lie in
the frozen round-two pending leaf `r00111111`, with box

    [1/4,1/2] x [1/4,1/2] x [3/4,1] x [3/4,1],

and in no excluded leaf of that chart. Therefore sound subdivision cannot
close the current exact fourteen-gauge formulation without additional
necessary conditions.

## The missing orbit completes an explicit intrinsic threshold

Enumerating all 24 affine contact permutations and retaining the four
integer unimodular maps gives the orbit of (2,1,0), modulo sign:

    {(1,1,0), (2,1,0), (3,1,1), (4,1,1)}.

Each has intrinsic P-P gauge exactly one, and none appears among the fourteen
previously imposed vectors. The four global-target inequalities gauge >183/500
are consequently valid additions, invariant under the contact symmetries.

There is also a complete geometric bound for the intrinsic enumeration.
If gamma_(P-P)(v)<=6/5, then v belongs to (6/5)(P-P). The coordinate spans of
P are (5,1,2), so every such integer vector lies in

    [-6,6] x [-1,1] x [-2,2].

Exact enumeration in this entire box finds precisely eighteen primitive
vectors modulo sign with intrinsic gauge at most 6/5. They are exactly the
original ten, the first four-vector orbit of intrinsic gauge 6/5, and the
new four-vector orbit of intrinsic gauge one. Thus eighteen is a complete
list for this stated intrinsic threshold. It is not a complete list of all
vectors whose gauge in an arbitrary containing body can be small; no global
gauge-completeness claim is made.

## Independent replay

Run `python3 tests/replay_det5_second_retained_witness_independent.py`.
The standalone stdlib-only test has its own matrix inversion, exact body
reconstruction, search bounds, symmetry enumeration and intrinsic-gauge
enumeration. It imports no discovery code, geometry core, other validator or
solver. Its [receipt](../results/det5_second_retained_witness_validation.json)
records all fourteen checked gauges, both violated gauges, the complete
intrinsic list, source hashes, and four rejected mutations. The first
witness's pinned test and receipt remain unchanged.
