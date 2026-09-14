# Independent strict Farkas review for the horizontal branch projection

This note concerns a finite affine system in the two variables `z=(a,tau)`,
after fixing the four base parameters. It proves the elimination and witness
criterion. It does not by itself verify the geometric derivation of each
projected inequality or establish a uniform exclusion of all base parameters.
No solver calls are used in this review.

Write each retained branch atom as

    f_i(z)=n_i dot z+c_i > 0,       i=1,...,m.             (1)

All normals and constants are real; they can be rational functions of the
base parameters on their stated domain. A positive common denominator may
be cleared before applying the criterion. A denominator of unknown sign
must not be silently cleared.

## Exact infeasibility criterion, including strict boundaries

System (1) is infeasible if and only if there is a nonzero vector
`lambda>=0` such that

    sum_i lambda_i n_i=0,       sum_i lambda_i c_i<=0.    (2)

Moreover, a certificate can always be chosen with at most three positive
coordinates.

For sufficiency, a strict feasible point would give
`sum lambda_i f_i(z)>0` because at least one weight is positive. Its value
would also equal `sum lambda_i c_i<=0`, a contradiction. The non-strict
comparison in the final certificate is essential: two opposite strict
inequalities can be inconsistent with weighted constant exactly zero.

For necessity, consider the affine subspace
`S={Nz+c:z in R²}` in `R^m`. If it does not meet the open positive orthant,
finite-dimensional separation gives a nonzero separating linear functional
lambda. Since S contains both directions of every vector in the image of N,
the functional is constant on S: `N^T lambda=0`. Nonnegativity of its
coefficients is forced by the unbounded positive coordinate directions of
the orthant. The infimum of its values on that open orthant is zero, so
`lambda dot c<=0`. This proves (2). Equivalently, one may maximize a common
slack t subject to `Nz+c>=t*1`; that linear program is always feasible,
and its finite nonpositive optimum has the same dual certificate with
`sum lambda_i=1`.

Normalize a certificate by `sum lambda_i=1`. The feasible weights lie in
the compact polytope

    lambda>=0,   sum lambda_i=1,   sum lambda_i n_i=0.

Minimize `sum lambda_i c_i` there, and among its minimizers choose one
with smallest support. If the support had more than three entries, the
corresponding columns `(1,n_i)` in `R³` would be linearly dependent.
There would be a nonzero perturbation d supported there with
`sum d_i=0` and `sum d_i n_i=0`. Both small signs of that perturbation
preserve nonnegative weights. Minimality forces `sum d_i c_i=0`, since
otherwise one sign would improve the objective. Increase one perturbation
until a supported weight first becomes zero. This yields a minimizer of
smaller support, a contradiction. Thus three weights suffice, including
when the two normal-coordinate equations are dependent.

## Complete quantifier-free enumeration in two dimensions

The following cases exhaust every certificate of support at most three.
The word "constant" below means the affine constant c_i, not the full
value f_i at a trial point.

1. **One normal.** If `n_i=0`, the atom is impossible exactly when
   `c_i<=0`. A zero normal with positive constant is harmless.

2. **Opposite parallel nonzero normals.** For i<j, require
   `cross(n_i,n_j)=0` and `dot(n_i,n_j)<0`. Then

       lambda_i=-dot(n_i,n_j),  lambda_j=||n_i||²

   are both positive and annihilate the normals. This pair certifies
   infeasibility exactly when

       -dot(n_i,n_j)*c_i+||n_i||²*c_j <= 0.

   Parallel normals pointing in the same direction have no positive
   two-term dependence. Cases with a zero normal are already covered by
   the first item.

3. **Rank-two triples.** For i<j<k, form the cofactor vector

       d=(cross(n_j,n_k),cross(n_k,n_i),cross(n_i,n_j)).

   Its weighted normal sum is identically zero. If all three entries are
   positive, this triple certifies infeasibility when `d dot c<=0`.
   If all three entries are negative, first reverse its sign; equivalently
   the certificate test is `d dot c>=0`. Testing `d dot c<=0` without
   reversing a negative cofactor vector would be incorrect.

   A rank-two triple whose cofactor vector has a zero coordinate reduces
   to a support-two dependence, already covered by item 2. Mixed signs
   cannot supply nonnegative weights. A rank-one or rank-zero triple also
   reduces to the earlier cases. Thus it is sufficient to test strictly
   same-signed, nonzero cofactor entries in the triple enumeration, provided
   every single and pair case is also tested.

Infeasibility is the disjunction of these explicitly enumerated cases.
Strict feasibility is its Boolean negation. Because determinants, scalar
products and weighted constants are explicit expressions in the base
parameters, this is genuinely a finite quantifier-free condition; it does
not quantify over a hidden weight vector. It can still be a large polynomial
Boolean formula, so the elimination alone is not a tractability claim or a
continuous-domain coverage proof.

## Exact witness from a bounded closed polygon

Let `P={z:f_i(z)>=0 for all i}` be the closed relaxation. The projected
branch contains the strict bounds

    a>0,  1-a>0,  tau>0,  1-a*A/k-tau>0,

with A>0 and k>0. Their closures imply `0<=a<=1` and `0<=tau<=1`,
so P is compact. Additional affine inequalities cannot destroy boundedness.

Enumerate every pair of nonparallel boundary lines `f_i=f_j=0`, solve it
exactly, and keep its intersection when it satisfies all closed inequalities.
Every retained intersection is a vertex of P, and every vertex is obtained
this way. This remains true when P is a segment or a single point: bounded
vertices have at least two linearly independent active normals. Consequently,
if no intersection is retained, P is empty.

If intersections are retained, take their arithmetic mean v. Exact
deduplication is optional: repetitions merely give some vertices larger
positive weights, while every vertex is still represented. All closed
inequalities hold at v. Now check every original strict inequality at v.
If they all hold, v is an explicit strict feasible witness. If some atom
has value zero, its nonnegative values on all represented vertices must
all be zero. Since P is the convex hull of those vertices, that atom is
zero everywhere on P, so no strict feasible point exists. This proves the
barycenter test for empty, lower-dimensional, and full-dimensional cases.

For rational input coefficients every intersection and the barycenter are
rational, so no numerical tolerance or approximate interior test is needed.

A useful qualification: **P full-dimensional is equivalent to strict
feasibility only after excluding zero-normal atoms with nonpositive
constants.** For example, append the atom `0>0` to the open unit square;
the closed relaxation remains full-dimensional, but the strict system is
infeasible. The singleton certificate catches this case, and the direct
barycenter test catches it as well. Thus the implementation can avoid any
ambiguous dimension shortcut by checking all strict inequalities on the
computed barycenter.

## Replacing the first-observer endpoint a=1 by a<1

Suppose the unprojected first-observer bound gives `0<a<=1`, and every
other retained branch inequality is strict and affine in `(a,tau)`.
A feasible point with a<1 already satisfies the strict version. At a feasible
point `(1,tau0)`, each of the finitely many other strict atoms has a positive
margin. Moving to `(1-epsilon,tau0)` changes each value continuously, so a
sufficiently small epsilon>0 preserves all those margins and keeps a>0.
Explicitly, for each atom whose a coefficient b_i is positive, choose
`epsilon<f_i(1,tau0)/b_i`, and also choose `epsilon<1`. Atoms with
nonpositive a coefficient do not decrease. This proves equivalence of
existence with `a<=1` and existence with `a<1` under the stated hypotheses.

The argument applies to the displayed projected R0 inequality and the
selected strict gauge pieces because they are affine and strict once the
base is fixed. It does not justify discarding an endpoint if another
retained equality or non-strict constraint forces a=1. Any such additional
constraint would have to be reviewed separately. Selecting one strict
piece from a maximum does not require an extra equality or a dominance
constraint when the original condition is simply that the maximum exceed
a threshold.

## Independent audit of the stored horizontal projection

The implementation is now accompanied by
[an independent audit](../tests/audit_det5_horizontal_projection_independent.py).
It reconstructs the four gauge-piece families from the original physical
vectors, rather than importing the implementation's piece formulas. For a
horizontal physical vector `(vx,0,vz)`,

    5*ell(v)=vx*(e1-e2)+(5*vz-2*vx)*(e3-e0).

Canonical reversal changes only the first horizontal vector's sign.
Substituting `V=(a/k)Z+tau*W`, and using evenness where necessary, gives
the P and N positive-part formulas in
[the negative-determinant normal form](DET5_NEGATIVE_DETERMINANT_GAUGE_NORMAL_FORM.md).
The two inactive pieces of `N(1-a,t)` are strictly below one, so only its
middle piece can exceed the actual target `183/100`. This yields precisely
12 piece-selection patterns per order, with 12 strict inequalities each.
The full 12-pattern reference does not rely on any subsequent reduction
of the forward-order pattern list.

The projected observer atom has an independent direct justification.
Write `V0=F01-F02=(a/k)*alpha-(1-y)*tau`. The forced exceptional observer
clause is

    alpha >= k*F01+(5-k)*F02.

Since `F01>0`, its right side is strictly greater than
`(5-k)*(F02-F01)=-(5-k)*V0`. Therefore
`alpha+(5-k)*V0>0`. Dividing by `5-k>0` and multiplying by `L>0` gives
exactly the stored projected observer polynomial. This is a necessary
projection of the exceptional clause with strict facet positivity; the
projection does not claim to restore every discarded height constraint.

The determinant atom is `B*tau>deltaD`, with

    deltaD=(17/5)*(5/6)*(183/500)^3=34728093/250000000.

It follows from the global target and its determinant/volume consequence.
The other base-only atoms retain the Z gauge and the previously proved
height-separation band. The quantifier-free result characterizes the
specified horizontal relaxation, not full hollow-body existence.

All 864 stored polynomial coefficients are compared with this reconstruction,
including every branch label, monomial power vector and strict inequality.
The ten original rational base controls comprise 120 branches. A separate
frozen probe comprises 22 additional forward-order bases, or 264 branches.
Every archived branch is classified independently by **strict Fourier-Motzkin
elimination**: eliminate a by combining each lower and upper bound with
positive weights, then compare the resulting strict lower and upper bounds
on tau. Every saved infeasibility certificate is also checked directly for
nonnegative normalized weights, zero weighted normal and nonpositive weighted
constant. Every saved feasible witness satisfies all 12 inequalities exactly.

The additional probe's four infeasible bases are point obstructions to this
relaxation; the audit does not turn them into neighborhoods or a continuous
cover. It also checks the probe's complete initial filtered-grid prefix,
without rerunning its research search or invoking a solver.

The generic kernel controls include an identically-zero atom on a full
closed square, positive and negative constants, feasible parallel normals,
opposite normals with zero weighted constant, both signs of triple
cofactors, rank-degenerate triples, and closed segments or points with no
strict interior. There are also 160 deterministic rational bounded systems
compared against independent strict elimination. Integer inputs with a
nonterminating rational certificate are included. The implementation now
coerces both kernel inputs to `Fraction`, preventing accidental float
normalization or float line intersections when a caller supplies integers.
A deliberately corrupted weight is rejected by the independent verifier.

The [validation record](../results/det5_horizontal_projection_validation.json)
records all coverage and outcome counts. These are exact arithmetic audits,
not SMT queries or floating optimization, and they establish no coverage of
the remaining four-dimensional continuous base domain.
