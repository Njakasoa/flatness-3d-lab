# Independent review: determinant-13 contraction exclusion

## Assessment and scope

The argument is valid, with a stronger oscillation estimate than the initial
proposal. Put A=1+2/sqrt(3). Every hollow, full-dimensional tetrahedron K
containing

    P = conv((0,0,0), (13,1,5), (0,1,0), (0,0,1))

satisfies

    w(K) <= (1+13A)/9 = (14+26/sqrt(3))/9.

No prescribed facet contacts are needed. The conclusion is invariant under
affine unimodular transformations. It excludes the determinant-13 class when
the surrounding body is a tetrahedron; it does not exclude a nonsimplicial
body merely because it contains this P. In particular, it does not justify
removing larger contact hulls containing a determinant-13 subset.

This review establishes the mathematical implication. It does not establish
novelty or a new global flatness upper bound.

## Barycentric identities and sign losses

Order the vertices of P as displayed. Its linear difference coordinates are

    ell(X,Y,Z) = (5X/13-Y-Z, X/13, Y-X/13, Z-5X/13).

Thus z1=(2,0,1) and z2=(3,0,1) have coordinates

    a1 = (-3, 2,-2, 3)/13,
    a2 = ( 2, 3,-3,-2)/13.

Each vector sums to zero and has half its l1 norm equal to 5/13. The four
column sign codes are (-,+), (+,+), (-,-), (+,-), all distinct.

Let v_i be the vertices of K and F_ij the barycentric coordinate of p_j at
v_i. Containment makes F nonnegative and column stochastic; affine
independence makes F invertible. In particular, neither a zero diagonal nor
relative-interior contact assumptions are used. Since simplex difference
coordinates have gauge equal to half their l1 norm,

    gamma_(K-K)(z_r) = ||F a_r||_1/2.

For each output row i choose a sign s_ri of (F a_r)_i, arbitrarily if this
entry is zero. The exact cancellation identity is

    L_r := 5/13 - gamma_(K-K)(z_r)
         = sum_{i,j: s_ri != sign(a_rj)} |a_rj| F_ij.

Indeed, subtracting s_ri(F a_r)_i from the absolute input sum in that row
leaves twice the mismatched absolute input mass. Nonnegativity and column
stochasticity justify summing the identity. Zero output entries cause no
exception: either choice of sign gives the same row loss.

Give output row i its two-sign code (s_1i,s_2i). Define E as the sum of F_ij
over pairs whose output and input codes differ. Every such pair contributes
at least 2/13 to its coefficient in L_1+L_2, whereas matching pairs contribute
zero. Therefore, whenever both gauges are at least beta,

    E <= (13/2)(L_1+L_2) <= 5-13 beta.

If beta>4/13 then E<1. Every input code must then occur among the output
rows: otherwise all of its column, of total mass one, contributes to E.
There are four distinct input codes and four rows, so these occurrences
constitute a bijection. A row permutation consequently transforms F into
G=I+H, where

    e_j := sum_{i != j} G_ij = 1-G_jj,
    E = sum_j e_j,
    sum_i H_ij = 0,
    ||H_column_j||_1 = 2e_j.

## The sharper oscillation estimate

Write osc(x)=max_i x_i-min_i x_i. For two distinct columns j,k, their
difference has zero sum, so centering x at the midpoint of its range gives

    |(H^T x)_j-(H^T x)_k|
      <= ||H_column_j-H_column_k||_1 osc(x)/2
      <= (e_j+e_k) osc(x)
      <= E osc(x).

Taking the largest difference proves

    osc(H^T x) <= E osc(x).

There is no extra factor two. The initial proposal's bound 2E is also
valid, but loses the fact that j and k are distinct and their two leakage
masses are part of the same total E.

For a lattice covector u, put d_j=u dot p_j and q_i=u dot v_i, with v_i
permuted consistently with the row permutation. Then d=G^T q. The triangle
inequality for oscillation gives directly

    osc(d) >= osc(q)-osc(H^T q) >= (1-E) osc(q).

No inverse-series convergence assumption is hidden here. For u=(0,1,0),
d=(0,1,1,0), so osc(d)=1 and

    w(K) <= w(K,u) = osc(q) <= 1/(1-E)
         <= 1/(13 beta-4)                 (beta>4/13).

In the initially proposed target test beta=37/102 with strict gauge lower
bounds, this yields E<29/102 and w(K)<102/73; the weaker proposed bound
w(K)<51/22 is therefore valid as well.

## Hollow-body bound and endpoints

ACMS Lemma 5.1, equation (14), gives

    lambda_1(K-K) >= 1-A/w(K),  A=1+2/sqrt(3).

This is checked in the local primary text
[ACMS, arXiv:1907.06199](https://arxiv.org/abs/1907.06199), and applies to
every hollow three-dimensional convex body. Each nonzero integer vector's
gauge is at least this first minimum. Write w=w(K).

If w<=13A/9, the claimed upper bound (1+13A)/9 already follows. Otherwise
beta=1-A/w>4/13, and the preceding non-strict inequalities give

    w <= 1/(13 beta-4) = 1/(9-13A/w).

The denominator is positive in this case. Multiplication gives

    9w-13A <= 1,

which proves the claimed bound. There is no assertion about unattained
equality: the theorem has a non-strict upper bound, while the case split is
strict only where needed to guarantee E<1.

Finally, (1+13A)/9 < 11A/7 is equivalent to 7<8A, which holds since A>1.
Thus this exclusion applies below the existing contact-reduction threshold.
The complete contact-hull classification and the fact that four facet
contacts correspond to a surrounding tetrahedron remain separate inputs
when updating a global necessary class list.
