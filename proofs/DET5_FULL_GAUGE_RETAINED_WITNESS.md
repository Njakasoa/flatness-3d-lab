# A retained Y/U witness survives every target gauge

Date: 2026-09-14. Status: exact counterexample to the proposed infeasibility
of a restricted necessary-condition system. This is not a high lattice-width
body and does not exclude a contact class or improve the flatness bound.

Let P=conv(0,(5,1,2),e2,e3). Consider the following column-stochastic matrix
of contact barycentric coordinates:

    F = (1/867000) [      0  140322  677661  179113 ]
                    [   2113       0  174000  350113 ]
                    [   2113  724565       0  337774 ]
                    [ 862774    2113   15339       0 ].

All off-diagonal entries are positive. Define K by the four columns of
P F^(-1), regarding P as the 3-by-4 vertex matrix. Exact Gaussian elimination
shows F is invertible. Thus the four selected contacts lie in relative
interiors of the corresponding facets. There are seven boundary lattice
points in total; the statement concerns the selected four-point hull.

The new stdlib-only [independent replay](../tests/replay_det5_full_gauge_retained_independent.py)
reconstructs K without importing discovery code, the geometry core, solvers,
or another validator. It binds its computations to
[the archived witness](../results/det5_joint_short_gauges.json) and writes
[the exact validation record](../results/det5_full_gauge_retained_validation.json).
It establishes:

| Quantity | Exact value |
|---|---|
| Width in Y=(0,1,0) | 134535942732777000 / 39202828222912103 |
| Width in U=(1,-1,-2) | 194521890431773500 / 39202828222912103 |
| Full lattice width | 96007799530165500 / 39202828222912103 |
| Minimizing covector, modulo sign | (0,0,1) |
| Full first minimum of K-K | 211637 / 541875 |
| Minimizing vector, modulo sign | (2,1,0) |
| Volume | 135773825625000000 / 39202828222912103 |

The first two widths exceed 17/5. The full lattice width is approximately
2.449, whereas the first minimum is approximately 0.390564. In particular,
this example cannot contradict the flatness conjecture.

## Completeness of the arithmetic checks

The coordinates of every point of K lie between coordinate extrema of its
vertices. Exhausting the integer box [-6,5] x [-1,1] x [0,2] therefore checks
all possible interior lattice points: all 108 fail the strict barycentric
interior test. Exactly seven have nonnegative coordinates with a zero entry.

For width, put the three vertex differences from vertex 0 in the rows of D.
A covector with width at most the least coordinate span W has |D u|<=W
coordinatewise. Consequently |u_j|<=W sum_i |(D^-1)_(ji)|. The integer bounds
are [1,2,4]; all 59 primitive directions modulo sign in this box are checked.
Every direction outside has width greater than W. The stated minimizing
covector is unique modulo sign.

For the gauge, independently compute the inverse affine barycentric map B
of P. For every vector v,

    gamma_(K-K)(v) = (1/2) ||F B(0,v)||_1.

Indeed, the difference body of a simplex in barycentric coordinates is the
sum-zero subspace intersected with the l1-ball of radius two. Any lattice
vector of gauge at most one lies in K-K, whose coordinate spans give the
integer bounds [11,3,2]. All 341 primitive vectors modulo sign are checked.
The found minimum is less than one, so the enumeration is complete; a
nonprimitive vector has larger gauge than its primitive divisor.

The same calculation for P-P enumerates the complete 18 primitive vectors
of intrinsic gauge at most 6/5 in the bounds [6,1,2]. Every one exceeds
beta=183/500 in K-K. This includes all eight newly added vectors, but the
full minimum calculation is stronger than any finite-gauge assertion.

## Exact target and volume comparison

Write m=211637/541875, t=(17/5)(1-m)-1. Exact rational arithmetic gives

    4/3 - t^2 = 4673022731/25400390625 > 0.

Thus m > 1-(1+2/sqrt(3))/(17/5). Every nonzero lattice vector satisfies
even the exact ACMS gauge necessity at target width 17/5, rather than merely
the weakened rational necessity beta. Also

    vol(K) m^3 = 606673135440118592/2940212116718407725 < 1.

Hence K satisfies the volume upper bound with its actual first minimum,
and therefore also with beta or the exact target gauge threshold. Its
reciprocal Y and U widths exceed respectively 2042829/50000000 and
2042829/100000000, the previously derived linear volume-gap bounds.

## Location in the retained system

The actual unique normalized extrema are Y:[1,0] and U:[1,3]. Their four
free normalized heights, in chart order, are

    116492766731/155174097731,
    77535689231/155174097731,
    893676904699/897448168082,
    895555839237/897448168082.

They lie in the pending leaf r101111 with box
[3/4,1] x [1/4,1/2] x [1/2,1] x [1/2,1] in the 953-query archive.
They lie in no recorded closed leaf of that chart. The replay verifies the
full bilinear height identities, including the shifted U-contact values
(2,2,1,0), so this is a genuine body in the retained system rather than only
a feasible point of its outer linear relaxation.

Consequently continued subdivision of this Y/U system cannot yield a full
infeasibility proof, even if every lattice gauge receives the exact ACMS
lower bound and these volume necessities are imposed. Further progress
requires additional necessary information, for example additional width
directions. This conclusion does not claim that every conceivable volume
inequality or geometric consequence has already been imposed.

Reproduction: `python3 tests/replay_det5_full_gauge_retained_independent.py`.
Six mutations of the matrix, archived width, normalized heights, pending
frontier, boundary list, and volume are rejected. No solver query is run,
and no previous archive is modified.
