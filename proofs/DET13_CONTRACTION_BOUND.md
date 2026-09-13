# A width bound for tetrahedra containing the determinant-13 configuration

Date: 2026-09-13. Theorem with independent mathematical review and exact arithmetic replay.
The bound concerns real tetrahedra, not all convex bodies containing the
same four lattice points. External novelty is unconfirmed.

Let A=1+2/sqrt(3) and

    P=conv((0,0,0),(13,1,5),(0,1,0),(0,0,1)).

**Theorem.** Every compact full-dimensional hollow tetrahedron K containing
an affine unimodular image of P satisfies

    w(K) <= (1+13A)/9 = (14+26/sqrt(3))/9 < 323/100.

There is no assumption that the points of P lie in distinct facet interiors,
or even on the boundary of K. The bound is not asserted to be sharp.

## Barycentric representation and two short vectors

Lattice equivalence lets us assume P itself lies in K. Let F be the matrix
whose j-th column consists of the barycentric coordinates of p_j in K.
Then F is nonnegative and column stochastic. It is invertible, because the
vertices of P and those of K are affinely independent. No zero-diagonal
condition is needed.

For a vector z let l(z) be its zero-sum difference coordinates in P. The
zero-sum difference coordinates in K are F l(z). For any simplex S the
gauge of S-S is the sum of the positive difference coordinates, equivalently
half their l1 norm. In particular

    gamma_(K-K)(z) = ||F l(z)||_1 / 2.

The two integer vectors z1=(2,0,1) and z2=(3,0,1) have coordinates

    l1=(-3,2,-2,3)/13,
    l2=( 2,3,-3,-2)/13.

Both coordinate sums are zero and both positive sums are 5/13. Their four
column sign pairs are (-,+), (+,+), (-,-), (+,-): all four are distinct.
Every nonzero coordinate has absolute value at least m=2/13.

## A quantitative consequence of preserving the two gauges

Suppose gamma_(K-K)(zr)>=beta for r=1,2. Choose the sign of each entry of
F lr, arbitrarily assigning either sign to zero. This assigns a pair of signs
to each of the four output rows. For one r, exact cancellation gives

    sum_(i,j with differing signs) |lr_j| F_ij
       = (||lr||_1 - ||F lr||_1)/2
       = 5/13 - gamma_(K-K)(zr).

Indeed the mismatched incoming mass in a row is the smaller of its positive
and negative incoming masses. If the output is zero, they are equal and
either sign has the same mismatched mass.

Let M be the sum of F_ij over entries where the row sign pair differs from
the input column's pair. Each such entry contributes at least 2/13 times
F_ij to the sum of the two cancellation losses. Hence

    M <= (13/2)(10/13 - 2 beta) = 5 - 13 beta.             (1)

If beta>4/13, the right side is less than one. Each input sign pair must
occur on an output row: otherwise its entire column, of mass one, would
be mismatched. Four distinct input pairs and exactly four rows imply a
bijection. Reorder the rows accordingly to obtain G=I+H, with G nonnegative
and column stochastic, and

    E = sum_j sum_(i!=j) G_ij = M <= 5-13 beta < 1.         (2)

This bijection step is where the tetrahedron hypothesis is used. It cannot
be applied to a body with an arbitrary number of vertices by adding rows.

## Inverse oscillation bound with total off-diagonal mass

For a real vector q write osc(q)=max(q)-min(q). Set
e_j=sum_(i!=j)G_ij. The column h_j of H has sum zero and l1 norm 2e_j.
For distinct j,k, the vector h_j-h_k has sum zero and l1 norm at most
2(e_j+e_k)<=2E. Centering q between its minimum and maximum gives

    |(h_j-h_k) dot q| <= E osc(q).

Consequently osc(H^T q)<=E osc(q). Since G^T q=q+H^T q, the triangle
inequality for oscillation implies

    osc(G^T q) >= (1-E) osc(q).                           (3)

The lattice covector u=(0,1,0) has values d=(0,1,1,0) on P, so osc(d)=1.
Let q list its values at the vertices of K, reordered with G. Barycentric
interpolation gives G^T q=d. Therefore

    w(K) <= w(K,u) = osc(q) <= 1/(1-E)
         <= 1/(13 beta-4),       whenever beta>4/13.      (4)

The coefficient in (3) is E, not 2E: oscillation compares distinct columns,
so their two off-diagonal masses together are bounded by the total E.
No numerical optimization, solver or inferred sign pattern is used.

## Closing the width inequality

Write w=w(K)>0. ACMS Lemma 5.1 and the planar flatness value imply

    lambda_1(K-K) >= 1-A/w.

Every nonzero lattice vector has gauge at least that minimum. If
w<=13A/9, the claimed bound is immediate. Otherwise put beta=1-A/w>4/13
and apply (4) to z1,z2. Its denominator is positive, and

    w <= 1/(9-13A/w),
    9w-13A <= 1,
    w <= (1+13A)/9.

All statements in this step are non-strict at the final bound. The proof
does not claim an equality case or an optimum.

Primary external input: [Averkov–Codenotti–Macchia–Santos,
Lemma 5.1](https://arxiv.org/abs/1907.06199). The matrix cancellation and
oscillation arguments above are proved here in full.

## Consequence for the existing contact reduction

The bound is below c=(11/7)A and below 2+sqrt(2), as checked by rational
radical intervals in the certificate. A maximal hollow polytope whose
selected relative-interior facet contact hull has exactly four vertices
has exactly four facets, hence is a tetrahedron. Therefore the
determinant-13 **four-contact hull** cannot occur above c. The previous
63 necessary full contact hulls reduce to at most 62 by deleting this row.
The other 52 spatial hulls with five to eight vertices and the planar square
are not deleted. They may still contain a determinant-13 tetrahedral subset;
their surrounding polytope need not be a tetrahedron.

The previous 63-type certificate remains a valid necessary superset. Its
enumeration is not changed retroactively. The new exclusion is a separate
analytic refinement, not a solver infeasibility result or a new global
flatness upper bound. External priority requires a separate literature audit.

## Reproduction

`experiments/det13_contraction.py` records the exact contact vectors,
sign-pair separation, coefficient inequalities, all 256 possible row-code
assignments, and exact radical comparisons. These finite checks support the
written continuous argument; they are not a proof-assistant formalization.
An independent verifier and adversarial review are supplied separately.
