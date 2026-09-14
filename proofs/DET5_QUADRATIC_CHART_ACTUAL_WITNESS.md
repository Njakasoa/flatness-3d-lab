# Exact actual body from the quadratic Y chart

The `lt` SAT assignment in
[`det5_quadratic_height_chart.json`](../results/det5_quadratic_height_chart.json)
is an actual hollow tetrahedron with the required facet contacts. The independent
stdlib replay
[`replay_det5_quadratic_witness_independent.py`](../tests/replay_det5_quadratic_witness_independent.py)
reconstructs its matrix and vertices without importing the discovery generator or
calling a solver. Full rational data and exhaustive checks are in
[`det5_quadratic_witness_validation.json`](../results/det5_quadratic_witness_validation.json).

Its column-stochastic contact matrix is

```
F = [ 0          3/64       1259/3264   15/16  ]
    [ 1013/1024  0          259/816     1/256  ]
    [ 1/256      3/4        0           15/256 ]
    [ 7/1024     13/64      19/64       0      ].
```

All off-diagonal entries are strictly positive, and exact Gaussian elimination
certifies invertibility. The vertices of K are obtained from P F^{-1}, where
P has columns 0, (5,1,2), e2, e3. Re-multiplication proves that each contact
lies in the relative interior of its designated facet.

The actual normalized Y heights are (0,0,1/8,1), with offset 15/2048 and gap
593/2048. Thus

\[
 w(K,Y)=2048/593>17/5.
\]

The minimum is **tied between vertices 0 and 1**; vertex 3 uniquely maximizes
Y. This is a valid Y[0,3] chart when extrema are allowed to tie, as in the
closed normalized height boxes. It does not certify a chart with unique
minimum at vertex 0. All eight strict complements of the certified Y rectangles
hold, and the replay binds those rectangles to their source archives.

The integer bounding box is [0,6] × [0,3] × [−1,2]. Exact barycentric
classification of all 112 integer points finds no interior point and exactly
the four designated lattice contacts on the boundary. This proves hollowness
without relying on a finite observer-guard sufficiency claim.

## What the body diagnoses

All ten archived gauge constraints exceed 37/102. However,

\[
 \gamma_{K-K}(2,0,1)=2369/6528<183/500,
\]

so the body already fails the stronger threshold at a tested vector. Moreover,
full enumeration gives

\[
 \lambda_1(K-K)=\gamma_{K-K}(1,-1,1)=801/2560<37/102.
\]

The vector (1,−1,1) is missing from the ten-vector model. To certify the full
minimum, every vector of gauge at most one belongs to K−K, whose coordinate
spans give the integer bounds (6,3,4). The replay checks all 335 primitive
vectors up to sign in that box; the minimum is below one, completing the
argument. Nonprimitive vectors cannot improve the minimum because the gauge
is positively homogeneous. This minimum also fails the exact necessary
ACMS threshold for a hypothetical global width above 17/5.

The global lattice width is

\[
 w(K)=218301984/89395343\approx2.4420,
\]

uniquely minimized up to sign by (1,−1,−2). The replay independently enumerates
all fifteen primitive covectors, up to sign, of contact-hull width at most
three. For a direction (a,b,c) in that set, |b|, |c| ≤ 3 and
|5a+b+2c| ≤ 3 imply |a| ≤ 12/5, giving a complete finite enumeration.
Every other primitive direction has integral P-width at least four and hence
K-width at least four. The displayed minimum is below four, so the fifteen
widths determine the full global width.

Consequently this is a genuine geometric witness against infeasibility of the
**weak ten-gauge Y-only chart**, not a counterexample to the conjectured
flatness bound. It supplies two concrete changes for future formulations:
strengthen the gauge threshold and include the newly exposed short vector.
The present evidence does not show that either change alone is sufficient.
