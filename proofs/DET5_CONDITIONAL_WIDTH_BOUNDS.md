# Conditional lattice-width bounds from the certified Y rectangles

Status: continuous conditional theorems using independently checked finite
refutations and the established ACMS inequality. They apply to specified
normalized-height subdomains, not to the entire determinant-five contact
class. No new bound on the unrestricted constant Flt(3) is asserted.

Let K be a full-dimensional hollow real tetrahedron with vertices v0,...,v3.
Assume the ordered lattice points

    p0=(0,0,0), p1=(5,1,2), p2=(0,1,0), p3=(0,0,1)

lie in the relative interiors of the facets opposite v0,...,v3 respectively.
No maximality hypothesis is needed. Write F_ij for the barycentric coordinate
of p_j at v_i. Then F is nonnegative and column-stochastic, F_ii=0, and
F_ij>0 for i!=j. Define b=1/w_Y(K)>0, a=-min_i Y(v_i)/w_Y(K), and
q_i=(Y(v_i)-min_j Y(v_j))/w_Y(K). Thus

    F^T q = a*1+b*(0,1,1,0).

The extrema conditions below refer to these actual normalized heights.
Ties at their endpoints are allowed.

## A geometric upper bound on b removes the width premise

For Y-extrema [0,3], let x=q1, y=q2, so q=(0,x,y,1). The contact column
zero gives a>=min(x,y). Column one excludes q1 and has a strictly positive
weight at q0=0, so a+b<=1-F01<1. Hence

    b < 1-min(x,y).                                      (1)

In particular x,y>=3/4 implies b<1/4 and w_Y(K)>4. More generally,
min(x,y)>=12/17 implies b<5/17 and w_Y(K)>17/5, including equality at the
normalized threshold 12/17.

For Y-extrema [0,1], write x=q2, y=q3, so q=(0,1,x,y). Column zero gives
a>=min(x,y). Column one has a strictly positive weight at q0=0 and only
x,y as its other heights. If max(x,y)>0, it gives a+b<max(x,y). If
max(x,y)=0, that column would give a+b=0, impossible because a>=0 and b>0.
Consequently every actual body in this chart satisfies

    b < |x-y|.                                          (2)

Thus |x-y|<=5/17 also implies w_Y(K)>17/5. In particular, points with x=y
cannot arise for an actual body with the stated strict facet contacts.
The strict inequalities in (1) and (2) explain why all the stated closed
subdomain endpoints remain valid.

## From a certified refutation to a small lattice gauge

Let V be the following ten nonzero integer vectors:

    (0,0,1), (0,1,-1), (0,1,0), (1,0,0), (1,0,1),
    (2,0,1), (3,0,1), (5,0,2), (5,1,1), (5,1,2).

For difference-barycentric coordinates ell_P(v), the actual difference-body
gauge is gamma_(K-K)(v)=||F ell_P(v)||_1/2. The independently certified
Y-rectangle inputs require all ten gauges to exceed beta, all listed integer
guards to avoid the interior, the stated normalized-height box, and
0<b<5/17. They impose no volume condition.

For an actual hollow K, every listed guard avoids its interior automatically.
This is only the necessary direction of the guard statement: no completeness
or truncation theorem for the finite guard list is needed here. In
particular, lowering beta below the guard construction's original edge-gauge
threshold causes no logical difficulty.

Suppose the geometry already ensures b<5/17 and all ten actual gauges were
strictly greater than beta. The actual F,q,a,b and exact products q_i F_ij
would satisfy the certified linear outer model, since the McCormick
inequalities are valid for exact products throughout their closed box.
This contradicts its checked refutation. Therefore

    gamma_(K-K)(v)<=beta for at least one v in V,
    lambda_1(K-K)<=beta.                                 (3)

Failure of strict lower bounds yields a non-strict upper bound in (3).
Nothing in this argument assumes that an arbitrary SAT relaxation reconstructs
a body; the substitution begins with an actual tetrahedron.

## Conversion to a global lattice-width bound

Write A=1+2/sqrt(3). The established ACMS inequality for a hollow body gives

    lambda_1(K-K) >= 1-A/w(K).

Combining this with (3), for any beta<1, gives the conditional bound

    w(K) <= A/(1-beta).                                  (4)

The conclusion concerns the full lattice width w(K), even though the
normalization and finite refutation use only the Y direction. The proof
uses no assumption that Y minimizes the width.

For beta=37/102 this becomes

    w(K) <= (102/65)(1+2/sqrt(3))
         = approximately 3.3812223833.                   (5)

This is strictly below the original contact-reduction threshold (11/7)A,
since 11/7-102/65=1/455. It is also strictly below 17/5: the exact inequality
A<13/6 follows by squaring 2/sqrt(3)<7/6, and (102/65)(13/6)=17/5.

## Subdomains supported by the twelve old rectangle proofs

All twelve terminal rectangles in
[the old Y proof receipt](../results/det5_class5_y_cvc5_validation.json)
have independent cvc5 refutations checked by Ethos. Bound (5) holds on their
intersection with the geometric automatic-width regions above.
Three entire certified rectangles qualify, and in fact have w_Y(K)>4:

| Y-extrema | Free heights | Rectangle | Old leaf |
|---|---|---|---|
| [0,1] | (q2,q3) | [0,1/8] x [0,1/4] | r00000 |
| [0,1] | (q2,q3) | [1/4,3/8] x [1/4,1/2] | r00110 |
| [0,3] | (q1,q2) | [3/4,1] x [3/4,1] | r1111 |

There are additional closed subdomains. In chart [0,1], intersect each of
its five certified rectangles with |q2-q3|<=5/17. The two whole rectangles
in the table are included among these five pieces. In chart [0,3], there is
also the square [12/17,3/4]^2 inside the certified leaf r1100, in addition
to r1111. These seven pieces are listed exactly in the arithmetic receipt.
They are not asserted to fill the gaps between them or any whole chart.

Without the automatic-width restriction, the old twelve rectangle proofs
still yield w(K)<=17/5, but the stronger bound (5) does not follow from them
alone. Thus the normalized-height conditions are substantive hypotheses.

## A stronger uniform-gauge proof on the upper corner

The [refined corner-threshold receipt](../results/det5_y_corner_gauge_refinement.json)
contains a checked refutation with all ten thresholds lowered uniformly to
beta=3/10 on q1,q2 in [3/4,1], Y-extrema [0,3]. The independent input audit
confirms the exact uniform threshold and absence of volume premises.
Since (1) makes w_Y(K)>4 automatic, (4) yields the stronger corner theorem

    w(K) <= (10/7)(1+2/sqrt(3))
         = 10/7+(20/21)sqrt(3)
         = approximately 3.0781436263.                   (6)

The earlier [beta=1/3 certificate](../results/det5_y_corner_gauge_threshold.json)
also passes the independent premise audit and gives 3/2+sqrt(3); (6)
strictly improves that value. No smaller gauge threshold is claimed here.
The separate 37/102 bounds on the other certified pieces remain (5).

## Independent arithmetic and premise audit

Run `python3 tests/replay_det5_conditional_width_bounds.py`.
The standard-library-only replay reconstructs all 22 declared variables and
every full-matrix linear assertion from independent rational Gaussian
barycentrics. It checks the twelve old inputs and both uniform corner inputs,
binds their input and CPC hashes to successful existing Ethos receipts, and
checks all rational geometric thresholds and constant comparisons. Four
deliberate corruptions of the gauge threshold, corner endpoint, proof hash
and successful-proof status are rejected.
The [validation record](../results/det5_conditional_width_bounds_validation.json)
distinguishes this audit from a new solver run or proof-kernel replay; neither
is performed. The continuous geometric and ACMS implications are the written
proof above. All assertions are conditional on the precise contact and
height hypotheses, so no complete contact type is removed by this statement.
