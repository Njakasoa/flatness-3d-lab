# A thirteen-variable cubic formulation of the pair branch

This is an equivalent algebraic representation of the existing necessary
pair-branch model. It supplies no infeasibility result and no width bound.
It trades five auxiliary variables for a lower maximum polynomial degree.

Use the eight affine facet parameters of the signed-adjugate model. Add four
positive variables r_j and one positive variable delta, constrained by

    A^T r = (1,1,1,1)^T,       delta = det(A).

Retain sum_i a_i>2, a_i>=1/2, b_i>0 and 1-a_i-b_i>0. The exact pair matrix
lemma gives det(A)>0, so r is uniquely the vector of inverse column sums.
Its positivity is exactly the additional bounded-simplex condition. Define
S=adj(A), C_j=sum_i S_ij; then C_j=delta*r_j and

    T_ij=S_ij/(delta*r_j).

The determinant is cubic in the eight affine row parameters. One way to
see the degree bound is to change the column basis so that its first vector
is the all-ones vector. Because A fixes this vector, the first transformed
column is constant, and the other three are affine. The determinant therefore
has degree at most three. Its actual expanded polynomial has degree three.

## Width comparisons through complementary minors

Let d_i=u dot p_i be the values of an integer direction on the four contacts.
For j<k define the quadratic polynomial

    Q_jk(u) = sum_{i<ell} (d_i-d_ell) (-1)^(i+ell+j+k)
              det A[complement{j,k}, complement{i,ell}].

The row and column complements in this formula are ordered increasingly.
Set Q_kj=-Q_jk. The two-by-two complementary-minor identity for the adjugate
gives

    (d^T S)_j C_k - (d^T S)_k C_j = det(A) Q_jk(u).

The formula can also be verified by expanding all terms: collect each
coefficient d_i-d_ell, then use the corresponding two-by-two minor of adj(A).
Consequently the exact directional vertex difference is

    u dot (V_j-V_k) = Q_jk(u)/(delta*r_j*r_k).

All three denominator factors are positive. Width greater than a rational
target W in direction u is therefore exactly

    OR_{j<k} (Q_jk(u)>W*delta*r_j*r_k
               OR -Q_jk(u)>W*delta*r_j*r_k).

The left sides are quadratic, and the right sides are cubic in the thirteen
variables. For W=17/5, multiply by five to use integral coefficients.

The existing domain bounds become, for example,

    -62*delta*r_j <= S_ij <= 63*delta*r_j,

and similarly for the two required ambient subset sums. These are also of
degree at most three, because the adjugate entries are cubic and delta*r_j
is quadratic. The four equations A^T r=ones are quadratic, delta=det(A) is
cubic, and lattice exclusions remain disjunctions of affine inequalities.
Thus every polynomial in this representation has degree at most three.

The same 37 complete width directions, proved domain bounds, canonical
symmetries and exact lattice-exclusion scope must be retained. Using the
partial 216-point box still gives only a necessary relaxation of hollowness.
Nothing here licenses interpreting a timeout as elimination.

## Formal checks

`python3 -m experiments.pair_cubic_width_identities` verifies the identity for
all six unordered vertex pairs and all three ambient coordinate functionals.
Linearity in u then verifies it for every direction, not just a sampled list.
The [certificate](../certificates/pair_cubic_width_identities.json) records
the cubic determinant and all eighteen quadratic quotients. Formal expansion
checks the complementary-minor formula against the direct adjugate products.
The intended next experiment is a solver implementation of this formulation;
the polynomial identity certificate itself contains no solver verdict.
