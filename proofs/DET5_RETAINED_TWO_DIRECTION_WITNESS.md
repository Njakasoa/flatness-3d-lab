# An actual body in a retained determinant-five height chart

Date: 2026-09-14. Status: independently checked exact rational counterexample
to completing the current two-direction relaxation with its ten imposed
gauges and the volume cuts. This is not a counterexample to the conjectured
global flatness bound, or to a formulation imposing every necessary gauge.

The matrix in the `retained_witness` field of
[the volume-gap archive](../results/det5_joint_volume_gaps.json) is nonnegative,
column-stochastic, invertible, has zero diagonal, and has every off-diagonal
entry positive. Inverting it gives a tetrahedron whose four prescribed facet
contacts are P=conv(0,(5,1,2),e2,e3), all in their facet relative interiors.
The rational independent replay gives:

| Quantity | Exact value |
|---|---|
| Y-width | 160418300/26445567 > 17/5 |
| U-width, U=(1,-1,-2) | 237541900/26445567 > 17/5 |
| Global lattice width | 53676652/26445567 < 17/5 |
| Minimizing covector | (0,0,1) |
| Volume | 412120400/79336701 < (500/183)^3 |
| Full difference-body minimum | 113/505 < 183/500 |
| Minimizing integer vector | (3,1,0) |

The entire integer bounding box has 342 points. None is interior, and exactly
seven lie on the boundary. The complete width check uses an inverse edge
frame to bound every potentially minimizing primitive covector and checks
65 directions modulo sign. The full difference-body minimum is checked on
969 primitive vectors modulo sign in the integer bounding box of K-K;
outside this box every gauge is greater than one, whereas the displayed
minimum is below one. All ten gauges actually imposed in the search exceed
183/500, despite the smaller full minimum in the table.

## The retained normalized chart is genuinely occupied

The actual Y-extrema are [0,1], and the actual U-extrema are [0,2]. Their
normalized vertex heights are respectively

    qY=(0,1,355519/397075,114831/158830),
    qU=(0,116017/117595,1,117012/117595).

The replay verifies the exact equations F^T qY=aY*1+bY*(0,1,1,0) and
F^T qU=aU*1+bU*(2,2,1,0), including both offset ranges and the positive
volume-derived gap bounds. These are equations of the actual body, not
height values copied from a relaxed solver model.

In the frozen 835-query
[round-two frontier](../results/det5_joint_round2.json), the actual four free
heights occupy the pending leaf `r1111101` of chart Y=[0,1], U=[0,2]:

    [3/4,1] x [1/2,3/4] x [3/4,1] x [1/2,1].

They occupy no excluded leaf of that chart. Thus the obstacle is present
inside a retained chart and is independent of questions about the Y-symmetry
quotient. Sound subdivision alone cannot exclude the entire current search
domain, because this body satisfies its exact nonlinear premises as well
as the linear volume cuts.

## A precise missing necessary condition

The missing vector (3,1,0) has gauge 113/505. Adding

    gamma_(K-K)(3,1,0) > 183/500

is a sound necessary cut for a global-width counterexample and excludes this
body. Such an addition is a changed formulation; it must not be described as
a refutation of an unchanged pending query. Alternatively, imposing width
in direction Z excludes this body immediately. This witness does not show
that either strengthened formulation is empty, nor that two directional
width constraints with all necessary gauge constraints must remain feasible.

## Independent replay

Run `python3 tests/replay_det5_retained_witness_independent.py`. The script
uses only the Python standard library, with its own generic inverse,
barycentric reconstruction, finite search bounds, and exact arithmetic.
It imports no discovery code, geometry core, other validator, or solver.
The [validation record](../results/det5_retained_witness_validation.json)
binds the two source archives by SHA-256 and records the exact body, all
finite gauges, normalized offsets and gaps, frontier location, and four
rejected mutations (matrix, width, normalized height, and pending frontier).
No old archive or solver query was changed or rerun.

## Symmetry-compatible gauge enrichment

Enumerating all 24 permutations of the contact vertices, solving each affine
map, and retaining precisely the integer maps of determinant plus or minus
one yields four contact automorphisms. Their full orbit of (3,1,0), modulo
sign, is

    {(1,-1,1), (2,1,1), (3,1,0), (6,1,2)}.

Each has intrinsic gauge 6/5 in P-P, and none occurs among the ten previously
imposed gauge vectors. The independent replay verifies these facts directly
from the contact coordinates. Imposing gauge >183/500 for all four vectors
is necessary for the global target and makes the added set invariant under
the full contact symmetry group. The fact that their intrinsic masses exceed
one does not make their gauges redundant: the containing tetrahedron can
shrink the gauge substantially, as the witness demonstrates. This is a
justified new formulation for further queries, not a completed exclusion.
