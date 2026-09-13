# Three-vector rank margin and quadratic height-volume charts

Date: 2026-09-14. Status: internally independently reviewed analytic lemma,
with a separate rational implementation. This is a formulation result, not
an exclusion of a further contact class or a new global flatness bound.

## Assumptions and the horizontal plane

Use P=conv(0,(d,1,a),e2,e3), for (d,a)=(7,2) or (8,3). Its four contact
Y-values are H=(0,1,1,0). Let F be a nonnegative column-stochastic 4 by 4
matrix; invertibility is not initially assumed. For an integer vector v,
let ell(v) be its affine difference coordinates in P and set

    n(v) = ||F ell(v)||_1 / 2.

Take beta=37/102 and z1=(1,0,0), z2=(3,0,1), z3=z2-z1=(2,0,1).
Assume n(zr)>beta for all three vectors. Their intrinsic contact masses
m_r=||ell(zr)||_1/2 are:

| d | (m1,m2,m3) | M=max m_r | g=2 beta-M |
|---|---|---|---|
| 7 | (3/7,4/7,5/7) | 5/7 | 4/357 |
| 8 | (1/2,1/2,1/2) | 1/2 | 23/102 |

Nonnegative column stochasticity contracts the l1 norm, so n(zr)<=m_r<=M.
The two vectors z1,z2 form a unimodular basis of the horizontal lattice Y=0.
Their difference coordinates span the two-dimensional space

    {x : 1^T x=0, H^T x=0}.

Write r=F ell(z1), s=F ell(z2). Put A=||r||_1, B=||s||_1,
C=||s-r||_1. Each is greater than 2 beta and at most 2M.
For arbitrary real t set D=||s-tr||_1. Triangle inequalities give

- B+C-A <= 2D when 0<=t<=1;
- A+B-C <= 2D when t<0;
- A+C-B <= 2D when t>1.

For example, in the first case B<=tA+D and C<=(1-t)A+D.
In the second, B<=-tA+D and C>=(1-t)A-D; the third follows
from C<=(t-1)A+D and B>=tA-D. Each displayed left side is
strictly greater than 4 beta-2M. Consequently

    ||s-tr||_1 > g > 0 for every real t.

In particular r and s are linearly independent.

## Height identity implies invertibility

Suppose q lies in [0,1]^4, with q_L=0 and q_H=1 for distinct extrema L,H,
and

    F^T q = offset * 1 + b H,   b>0.

If Fx=0, column stochasticity gives 1^T x=0. The height identity then
gives H^T x=0. The preceding horizontal injectivity forces x=0, proving
F invertible. This proves there are no singular solutions hidden in these
height charts. No determinant sign assumption is required.

The vertices of the recovered body are the columns of P F^{-1} (with P
viewed as the 3 by 4 coordinate matrix). Their Y-values are
(q_i-offset)/b, hence their Y-width is exactly 1/b. Nonnegative column
stochasticity means the body contains P. If F has zero diagonal and
strictly positive off-diagonal entries, each P vertex is in the relative
interior of its corresponding facet. Under the six imposed contact-edge
gauges, the [complete observer guards](DET2_OBSERVER_GAUGE_GUARDS.md)
therefore certify hollowness.

## Quantitative complementary minor bounds

For every i with r_i nonzero substitute t=s_i/r_i in the distance inequality:

    sum_j |r_i s_j-r_j s_i| > g |r_i|.

The weak inequality also holds when r_i=0. Summing over i and dividing
by two yields

    sum_{i<j} |r_i s_j-r_j s_i| > beta g.

Both r,s annihilate 1 and q. These are two independent covectors. Thus the
2 by 2 minors of [r s] are proportional, with complementary signs, to the
2 by 2 minors of [1 q]. Let i<j be the complement of L,H and define

    k = |r_i s_j-r_j s_i|.

Since |q_H-q_L|=1, the proportionality factor has absolute value k.
Writing the four q-values in order as 0<=u<=v<=1 gives

    sum_{i<j}|q_i-q_j| = 3+v-u <=4.

Therefore k>beta g/4. We retain the weaker closed bound in the encoding.
For any zero-sum vector r with ||r||_1<=2m1, its projection onto two
coordinates satisfies max(|x|,|y|,|x+y|)<=m1. This is the hexagon with
vertices m1*(1,0),(0,1),(-1,1),(-1,0),(0,-1),(1,-1). The analogous
projection of s has scale m2. A bilinear determinant attains its maximum
absolute value at vertex pairs, whose normalized values are at most one.
It follows that

    beta g/4 <= k <= m1 m2.

All 36 hexagon vertex-pair checks are recorded in the certificate.

## Exact height-determinant relation and volume

Let C0 have columns ell(z1), ell(z2), ell(eY), e0. Direct affine-coordinate
calculation gives det(C0)=1/d. In M0=F C0=[r s t c], column sums are
(0,0,0,1), while their q-products are (0,0,b,offset).
Apply the row matrix R with rows e_i^T,e_j^T,q^T,1^T. Its determinant
is minus the parity of (i,j,L,H). The bottom two rows of R M0 are
(0,0,b,offset) and (0,0,0,1). Hence

    det(M0) = -parity(i,j,L,H) * b * (r_i s_j-r_j s_i),
    |det F| = d b k.

All twelve signs are checked independently. In particular
|det F|/b >=37/5202 for d=7 and >=851/5202 for d=8.
Since vol(K)=d/(6|det F|), the necessary ACMS volume cut for the global
target w(K)>17/5 becomes exactly

    vol(K)<1/beta^3  <=>  b k > beta^3/6.

Introducing one real variable k, imposing k>=beta g/4 and
(k=minor OR k=-minor), leaves every constraint polynomial of degree at
most two. The redundant valid cuts k<=m1 m2 and
b>beta^3/(6m1m2) are also retained. This volume cut is necessary for the
global-width target; it is not implied by large Y-width alone.

## Model scope and completeness

[Height charts](../experiments/contact_height_charts.py) have eight F
parameters, two free normalized q-values, offset and b: twelve variables.
Adding k gives thirteen. All three rank vectors and six contact-edge
vectors are explicitly present in the gauge sets. The exact lattice
contact automorphism groups have orders two and four. Their action on
ordered Y-extrema includes reversal when Y is reflected. They partition
the twelve possible extrema pairs into six and five orbits respectively;
ties are included because other normalized heights may equal zero or one.

The eleven original queries impose Y-width>17/5 and full observer/gauge
constraints, but no volume cut. Each returned UNKNOWN within its recorded
bounded run. The rank lemma upgrades their geometric interpretation;
neither their constraints nor their outcomes have been rerun or changed.

A [complete quadratic lift](../experiments/height_complete_quadratic.py)
adds the four physical X-coordinates and four Z-coordinates of the vertices.
Impose F^T X=P_X and F^T Z=P_Z. For each of the ten complete primitive
covectors u, impose that at least one signed pair difference

    u_X b(X_i-X_j) + u_Y(q_i-q_j) + u_Z b(Z_i-Z_j)

exceeds (17/5)b. These are exactly the actual width comparisons multiplied
by positive b. All omitted primitive directions have contact width at least
four, and thus already exceed the target. The resulting 21-variable model
is entirely quadratic and equivalent to the full target under the stated
necessary cuts; all possible extrema branches are covered. Ordinary inverse
lifting is standard algebra: a reduction in degree is not itself a new
mathematical width bound, and more variables may make computation harder.
The eleven complete lifted encodings are archived without solver queries.

## A direction-sensitive shortcut fails

A separate sufficient criterion uses a row permutation of F giving diagonal
entries g_j. If g_j+g_k>1 for equal-height contact pairs and >=22/17 for
cross-height pairs, then Y-width<=17/5. Indeed, choose maximum and minimum
of the inverse Y-values, at j,k, and let D be their oscillation. The column
averages satisfy

    H_j-H_k >= (g_j+g_k-1)D.

Equal contact heights are impossible by positivity; cross-height extrema
then give 1>=(5/17)D. However the gauges and hollow-contact assumptions do
not force any such permutation. The two archived rational bodies in
[the directional probe](../results/directional_contraction_probe.json)
fail all 24 permutations, yet have independently verified hollowness and
full difference minimum above beta. Their lattice widths are
10195234866/4006504279 and 1250053656/474942521, both below 17/5.
They refute the proposed sufficient-criterion implication only.
Permutations with a fixed point fail an equal-height pair automatically,
so the nine derangements suffice in the search.

## Verification and limitations

[Independent rational replay](../tests/replay_height_rank_independent.py)
imports no generator, solver or main geometry engine. It checks the exact
inputs, signs, constants, complete bodies and seven deliberate mutations.
[Certificate](../certificates/height_rank_certificate.json).
[Internal independent mathematical review](HEIGHT_RANK_REVIEW.md).
The certificate supports this written continuous proof; it is not a formal
proof-assistant certificate. No claim of external mathematical priority or
new class elimination is made.

## Subsequent complete interval cover

The quadratic charts above were then relaxed on exact rational height
rectangles. The resulting finite campaign completely covered both classes:
113 nodes, 62 terminal exclusions, eleven full squares. Independent formula
and coverage audits, a separate full-matrix cvc5 encoding, and external
reference-bound Ethos checks validate all62 refutations. Consequently
[CLAIM-0007](../claims/CLAIM-0007.md) proves the restricted facet-contact
bounds w<=17/5 and reduces the candidate-threshold list to59. The earlier
quadratic UNKNOWN outcomes remain unchanged historical records. The
21-variable full-width lift was not queried and is not a premise of this
interval proof; the volume cut is likewise unnecessary for it.
