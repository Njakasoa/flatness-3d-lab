# Two separating short vectors bound a containing hollow tetrahedron

Let P be a full-dimensional lattice tetrahedron with a primitive integer
covector of width one. Let z1,z2 be nonzero integer vectors whose difference
barycentric coordinate rows l1,l2 in P have no zero entries. Suppose the
four column sign pairs are distinct. Put

    a_r = ||l_r||_1/2, S=a_1+a_2,
    m=min_(r,j) |l_rj| > 0, D=m-S+2.

If D>0, every full-dimensional hollow real tetrahedron K containing P obeys

    w(K) <= (m+2A)/D,       A=1+2/sqrt(3).                (1)

The conclusion is preserved by affine unimodular transformations. It needs
no facet-contact hypothesis and does not apply to arbitrary nonsimplicial K.

## Proof

Use the nonnegative column-stochastic barycentric matrix F of P in K.
As in the fully detailed determinant-13 proof, if both gauges are at least
beta, the sum of the two weighted sign-cancellation losses is at most
S-2 beta. Every entry with a mismatched sign pair has weight at least m,
so its total mass E is at most (S-2 beta)/m. If beta>(S-m)/2, then E<1.
Every input sign pair must occur in an output row; with four rows this is
a bijection. After permuting rows, E is the total off-diagonal mass of F.

The oscillation inequality proved in
[DET13_CONTRACTION_BOUND.md](DET13_CONTRACTION_BOUND.md) gives

    w(K) <= 1/(1-E) <= m/(m-S+2 beta).                    (2)

Write w=w(K). If w<=2A/D, then (1) holds since m>0. Otherwise ACMS gives
beta=1-A/w>(S-m)/2. The denominator in (2) is positive, and (2) becomes

    w <= m/(D-2A/w), hence D w <= m+2A.

This proves (1), including its non-strict endpoint. The finite vector scan
is not part of the continuous proof.

## Two explicit exclusions

The proof applies with the following exact input data, in vertex order
P=conv(0,(d,1,a),e2,e3).

| d,a | integer vectors | l1 | l2 | S | m | bound |
|---|---|---|---|---|---|---|
| 10,3 | (1,0,0), (3,0,1) | (3,1,-1,-3)/10 | (-1,3,-3,1)/10 | 4/5 | 1/10 | (1+20A)/13 |
| 13,5 | (2,0,1), (3,0,1) | (-3,2,-2,3)/13 | (2,3,-3,-2)/13 | 10/13 | 2/13 | (1+13A)/9 |

For both rows u=(0,1,0) supplies width one. Their exact bounds are

    B10 = (21+40/sqrt(3))/13 = 3.391... < 17/5 < 2+sqrt(2),
    B13 = (14+26/sqrt(3))/9 = 3.2234563332... < (11/7)A.

The rational interval check in the independent replay establishes these
comparisons without floating-point decisions. B10 is above (11/7)A; it does
not exclude the determinant-10 type at that lower threshold.

Consequently the previous 63 necessary full contact hulls become **62 above
(11/7)A**, and **61 at width at least 2+sqrt(2)** (also above B10). Only
full tetrahedral contact hulls are removed. Larger hulls containing one of
these tetrahedra remain possible and retain their earlier classification.
Neither new bound is asserted sharp, and the global flatness bound is unchanged.

## Finite scan and scope

`experiments/two_vector_class_scan.py` examines the ten previous tetrahedral
classes. It checks every primitive vector up to sign with gauge in P-P
strictly below one and no zero difference coefficient. Such a vector lies
in P-P, whose coordinate extrema prove the finite search box. All eligible
pairs with distinct column sign codes are compared in Q(sqrt(3)).

Only the determinant-10 and determinant-13 best pairs in that domain give
bounds below 2+sqrt(2). This is not optimality among other vector domains,
weighted sign-loss arguments or different structural bounds. The two
explicit pairs above suffice for the claimed exclusions, irrespective of
whether the search is exhaustive.

The determinant-13 continuous argument was independently reviewed before
this parameterized restatement. The independent arithmetic replay also
checks the determinant-10 data. No separate external peer review is claimed.
The [bounded novelty audit](DET13_CONTRACTION_LITERATURE.md) concerns the
determinant-13 specialization and standard antecedents; priority for either
explicit class bound remains unconfirmed.
