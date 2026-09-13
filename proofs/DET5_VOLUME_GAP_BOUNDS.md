# Determinant-five rank margin and linear volume cuts

Date: 2026-09-14. Status: mathematical formulation result, with exact finite
arithmetic replay. The four-vector rank argument was proposed by the root
research agent and independently checked by the reviewing agent. This note
neither excludes the remaining determinant-five class nor improves Flt(3).

Let P=conv(0,(5,1,2),e2,e3), and let F be its column-stochastic matrix of
barycentric coordinates in a containing tetrahedron K. Thus F is nonnegative,
and is invertible for an actual full-dimensional K. Zero diagonal and positive
off-diagonal entries are the additional facet-contact assumptions used by the
search; the volume bounds below do not need those additional assumptions.
For v=(x,y,z), define

    ell(v)=(2x/5-y-z, x/5, y-x/5, z-2x/5).

Write beta=183/500. For hollow K with the global target w(K)>17/5, the established ACMS
necessary conditions used in the lab give gamma_(K-K)(v)>beta for every
nonzero integer v and vol(K)<beta^(-3). The rational beta is valid since
A=1+2/sqrt(3)<(17/5)(1-beta)=5389/2500; squaring its positive radical part
reduces this to 25000000<25038963.

## A four-vector rank argument

Set r=F ell(1,0,0), s=F ell(2,0,1), and let
A0=||r||_1, B0=||s||_1, Cminus=||s-r||_1, Cplus=||s+r||_1.
The first two contact masses are both M=3/5. Stochasticity gives
A0,B0<=2M, while the four gauge conditions give
A0,B0,Cminus,Cplus>2 beta. All four vectors occur in the archived eligible
vector set: (1,0,0), (2,0,1), (1,0,1), and (3,0,1).
No upper bound on Cminus or Cplus is required.

For D=||s-tr||_1, triangle inequalities give

- if 0<=t<=1, B0+Cminus-A0<=2D;
- if t>=1, A0+Cminus-B0<=2D.

For the second inequality, A0<=t A0 and
Cminus<=(t-1)A0+D, while B0>=t A0-D. For t<0, apply the same two cases
to -r with parameter -t, using Cplus in place of Cminus. Consequently

    ||s-tr||_1 > g := 2 beta-M = 33/250 > 0

for every real t. Thus the two horizontal images are independent. In an exact
Y-height chart F^T q=a 1+b H_Y with b>0, any vector in ker(F) also lies in
the horizontal difference space, which these two vectors span. Therefore
F is invertible even if invertibility was not imposed separately.
This conclusion concerns the exact bilinear chart, not a McCormick relaxation.

The complementary-minor argument in
[the existing rank proof](HEIGHT_RANK_AND_VOLUME.md) now applies without
change. For any Y-extrema L,H and complementary indices i,j, let
k_Y=|r_i s_j-r_j s_i|. Substitution t=s_i/r_i, summing the resulting minor
inequalities, and the identity sum_{i<j}|q_i-q_j|<=4 yield

    k_Y > beta*g/4 = 6039/500000.

This removes the earlier apparent rank obstruction for this class. The old
three-vector lemma remains inapplicable with its original hypotheses; the
four-vector argument is a distinct valid replacement.

## A uniform upper bound on each complementary minor

For either covector below, choose a unimodular basis v1,v2 of its integer
kernel and an integer transversal t with h(t)=1:

| h | v1 | v2 | t | bound M_h on every absolute minor |
|---|---|---|---|---|
| Y=(0,1,0) | (1,0,0) | (2,0,1) | (0,1,0) | 1/5 |
| U=(1,-1,-2) | (1,1,0) | (2,0,1) | (1,0,0) | 2/5 |

For fixed i,j the expression

    (F ell(v1))_i (F ell(v2))_j
      - (F ell(v1))_j (F ell(v2))_i

is affine in each column of F separately. Indeed, the quadratic term using
the same column cancels. Since each column belongs to a standard simplex,
every value is a convex combination of values at matrices whose four columns
are coordinate vectors. Absolute value is bounded by the maximum absolute
vertex value. Exhaustively checking all 4^4=256 such matrices for each of
six row pairs gives exactly the tabled maxima. Thus these bounds hold on the
whole continuous stochastic domain, with no integrality restriction on F.
The checked script records attaining matrices as well as the maxima.

## Positive height gaps from the volume bound

Let q be the normalized heights in direction h, with selected minimum and
maximum equal to zero and one, and let b=1/width_h(K)>0. The height identity
is F^T q=a 1+b H_h, with H_h allowed any constant shift. Let i,j complement
the selected extrema and put

    k_h=|(F ell(v1))_i (F ell(v2))_j
          -(F ell(v1))_j (F ell(v2))_i|.

The matrix with columns ell(v1),ell(v2),ell(t),e0 has determinant of absolute
value 1/5. Multiplying F by this matrix, and then using rows e_i^T,e_j^T,q^T,
1^T, leaves a block determinant with factors k_h and b. The row change has
determinant of absolute value one, because the omitted q-values are zero and
one. Hence

    |det F| = 5 b k_h,
    vol(K) = 5/(6|det F|) = 1/(6 b k_h).

No choice of orientation is needed because all determinants are absolute.
The established volume cut therefore gives b k_h>beta^3/6. Combining it
with the exact stochastic minor maxima yields the linear necessary cuts

    Y_gap > 5 beta^3/6  = 2042829/50000000,
    U_gap > 5 beta^3/12 = 2042829/100000000.

Equivalently, width_Y(K)<50000000/2042829 (about 24.476) and
width_U(K)<100000000/2042829 (about 48.951). These bounds are modest, but
remove the zero-gap limit and can be added directly to the existing linear
outer relaxations. They require the global-width-derived volume hypothesis;
large Y-width or large Y/U-width alone is insufficient justification.

## Reproduction and scope

Run `python3 tests/replay_det5_volume_gap_bounds.py` from the scientific
repository. The stdlib-only replay checks all 3072 minor vertex values,
the two unimodular frames, their barycentric determinants, all rank masses,
archived gauge inclusion, and the rational constants. The output is
[the validation record](../results/det5_volume_gap_bounds_validation.json).
The finite arithmetic supports the explicit continuous arguments above; it
is not a proof-assistant formalization and does not refute any solver chart.
No old solver query or archive was changed or rerun for this derivation.
