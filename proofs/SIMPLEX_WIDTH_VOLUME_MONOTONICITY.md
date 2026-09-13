# Width divided by volume decreases under tetrahedron containment

Date: 2026-09-14. Status: elementary mathematical lemma, independently derived
from the stochastic minor argument during the lab review. No mathematical
priority claim is made; its literature provenance has not been established.
This result provides bounds for formulations, not a new flatness bound.

**Lemma.** If P and K are full-dimensional tetrahedra in R^3, P is contained
in K, and u is a nonzero real linear covector, then

    width(K,u)/vol(K) <= width(P,u)/vol(P).

Equivalently, vol(K)/width(K,u) >= vol(P)/width(P,u). The statement here is
restricted to nested tetrahedra. The proof does not require lattice coordinates,
hollowness, designated facet contacts, or any symmetry.

## A stochastic minor inequality

Let c0,c1,c2,c3 be vectors in R^2 with sum zero. If F is a nonnegative
column-stochastic 4 by 4 matrix, put r_i=sum_j F_ij c_j. Then for every pair
of distinct rows i,k,

    |det(r_i,r_k)| <= max_{j<l}|det(c_j,c_l)|.

Indeed, the determinant is affine in each column of F separately: its
same-column quadratic term is zero because det(c_j,c_j)=0. Each column
belongs to a standard simplex, so the determinant is a convex combination
of values when every column of F is a coordinate vector. At such a matrix,
the four c_j are partitioned into at most four row groups.

If either selected group is empty, the determinant is zero. If at most two
groups are nonempty, the selected sums are opposites and it is again zero.
With four nonempty groups each selected sum is a singleton. With three
nonempty groups their sizes are 2,1,1. If the selected groups are the two
singletons, the determinant is an original pair minor. Otherwise, replace
the two-element sum by minus the two remaining singleton vectors, using
sum c_j=0. Its determinant with the other selected singleton is plus or
minus an original pair minor. This proves the inequality.

The bound is exact on the full stochastic domain: any chosen original pair
minor is attained by assigning its two columns to the selected rows and the
other two columns to a third row. The proof is continuous and does not assume
that the entries of F are integers.

## Geometry and the complementary minors

Write P=conv(p0,p1,p2,p3), and let ell(v) be the four difference-barycentric
coordinates of v with respect to P. Thus sum ell(v)=0 and
sum_j ell(v)_j p_j=v. Choose linearly independent v1,v2 in ker(u), and t
with u(t)=1. Let H_j=u(p_j), and form the invertible matrix

    C=[ell(v1), ell(v2), ell(t), e0],   delta=det(C).

Its determinant is nonzero because (v1,v2,t) is a physical basis. Its rows
have first two entries c_j=(ell(v1)_j,ell(v2)_j), with sum c_j=0. Since
H^T ell(v1)=H^T ell(v2)=0 and H^T ell(t)=1, the complementary-minor identity
is

    |det(c_j,c_l)| = |delta| * |H_m-H_n|,

where {m,n} complements {j,l}. One can see this directly, without an
additional theorem: multiply C on the left by the matrix with rows
e_j^T,e_l^T,H^T,1^T. Its determinant has absolute value |H_m-H_n|, while
the determinant of the resulting block matrix has absolute value
|det(c_j,c_l)|. Therefore

    max_{j<l}|det(c_j,c_l)| = |delta| * width(P,u).

Let F contain the barycentric coordinates of the P vertices with respect
to K, one P vertex per column. Containment gives nonnegative stochastic
columns. Because both bodies are full-dimensional, F is invertible and

    vol(P)=|det(F)| vol(K).

Let q be the normalized u-heights of the K vertices, ranging from zero to
one, and write b=1/width(K,u). The height identity is

    F^T q = a*1+b*H.

Choose actual minimum and maximum indices L,H0, so q_L=0 and q_H0=1, and
let i,k be their complementary indices. Set r_j=sum_l F_jl c_l and
kappa=|det(r_i,r_k)|. Multiplying FC on the left by the matrix with rows
e_i^T,e_k^T,q^T,1^T gives

    |det(F)| |delta| = b kappa.

Here the row matrix has determinant of absolute value one, and the last
two rows of its product with FC are (0,0,b,a+b*u(p0)) and (0,0,0,1).
The stochastic minor inequality now yields

    width(K,u)/vol(K)
      = |det(F)|/(b vol(P))
      = kappa/(|delta| vol(P))
      <= width(P,u)/vol(P),

as claimed. Tied extrema are harmless: any distinct minimizing and
maximizing indices give the same absolute determinant argument.

## Consequences for the remaining determinant-five class

For P=conv(0,(5,1,2),e2,e3), vol(P)=5/6. Under the established necessary
global-target volume bound vol(K)<beta^(-3), beta=183/500, the lemma gives

    width(K,u) < (6/5) width(P,u) beta^(-3).

For Y and U=(1,-1,-2), the contact widths are one and two, respectively.
This recovers exactly the two linear gap cuts in
[the determinant-five note](DET5_VOLUME_GAP_BOUNDS.md), without separately
enumerating the minor maxima for those directions.

There is also a useful finite completeness bound for small gauges. If
z is an integer vector with gamma_(K-K)(z)<=beta, then z belongs to
beta(K-K). Since the coordinate widths of P are (5,1,2), the lemma gives

    |z_X| < 6/beta^2,
    |z_Y| < 6/(5 beta^2),
    |z_Z| < 12/(5 beta^2).

Consequently every such vector lies in the explicit integer box

    [-44,44] x [-8,8] x [-17,17].

This is a completeness bound under the actual containment and volume
hypotheses. The eighteen vectors of intrinsic P-P gauge at most 6/5 form a
smaller necessary set; their threshold does not alone establish global
gauge completeness. No solver campaign on the larger box is asserted here.

## Symbolic replay of the partition step

Run `python3 tests/replay_simplex_width_volume_partition.py`.
Treating c0,c1,c2 as formal vectors and c3=-c0-c1-c2, the script represents
every determinant as coefficients of the three formal wedge products.
All 256 column assignments and all six row pairs are checked symbolically,
for 1536 identities. Every result is zero or plus or minus an original pair
minor, and every allowable polynomial is attained. The
[record](../results/simplex_width_volume_partition_validation.json) supports
the finite algebra step; the geometric and continuous arguments are the
written proof above. No old files or solver queries were changed.
