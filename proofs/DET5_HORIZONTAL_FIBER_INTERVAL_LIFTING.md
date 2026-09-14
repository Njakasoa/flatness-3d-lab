# Rigorous interval lifting of the two-variable fibers

Status: proved outer-formulation construction. This note supplies a way to
turn one rational linear refutation into an exclusion of a continuous shape
box. It contains no newly refuted shape box and no claim that finitely many
boxes cover the full shape domain. No solver queries were run for this note.

Use the [ordered chart](DET5_RATIONAL_HEIGHT_CHART_REVIEW.md) and the
[fiber reduction](DET5_HORIZONTAL_FIBER_REVIEW.md). Write

    sigma=(x,y,c,e,r,u), d=y-x,
    D=u*((1-x)c+x e)-r*((1-y)c+y e),
    rho=1/b, T=t/b, H=h/b.

The two height orders are separate charts. In the reverse order, both rows
and columns of F are conjugated as in the chart proof. This does not change
the scalar bounds below. Every claim about hypothetical bodies in this note
assumes the original strict facet contacts, hollowness, and global lattice
width greater than W=17/5.

## Uniform bounds on the projective variables and determinant

Put beta=183/500 and M=6/(5 beta^3)=50000000/2042829.
The [volume argument](DET5_VOLUME_GAP_BOUNDS.md) establishes, for every
hypothetical body under consideration,

    vol(K)<beta^(-3),             width(K,Y)<M.

These are consequences of the full geometric hypothesis and its ACMS
minimum bound. A finite list of ten or eleven gauge inequalities alone is
not a substitute for that hypothesis.

The exact chart domain gives 0<t<1 and 0<h<1, while width(K,Y)=rho.
Consequently

    W<rho<M,             0<T<rho,             0<H<rho.       (1)

All linear variables are therefore nonnegative and uniformly bounded.
The exact volume formula gives another useful necessary condition:

    vol(K)=5 rho/(6 |D|)<beta^(-3)
    ==> |D|>rho/M>W/M=34728093/250000000.                  (2)

In particular, the target geometries stay uniformly away from D=0, even
though the unrestricted chart admits singular matrices. This is a
shape-determinant separation, stronger than merely requiring D!=0.
It does not by itself bound c and e. A complete search still needs to
handle their unbounded chart ranges, or a separately justified compact
change of shape coordinates.

## Polynomial coefficient intervals

Take a finite closed rational box B in the six shape coordinates. We only
seek to exclude admissible chart points lying in B; it is harmless if B
also contains inadmissible points or crosses a chart boundary.

By the fiber proof and its
[coefficient certificate](../certificates/det5_horizontal_fiber_structure.json),
each transformed primitive atom can be written using an expression

    f(sigma,z)=a0(sigma)+aT(sigma)T+aH(sigma)H+arho(sigma)rho,
    z=(T,H,rho),                                          (3)

where every coefficient is a rational polynomial in sigma. Constant
shape conditions are included by setting the other three coefficients to
zero. The affine height identity is handled in this same form.

Evaluate each polynomial with exact rational interval arithmetic over B,
obtaining aj(B) contained in [lj,uj]. For example, interval addition adds
endpoints, and interval multiplication takes the minimum and maximum of
the four endpoint products. Build powers by repeated interval products
and add every signed rational monomial in the certificate. Dependency
overestimation is harmless. Evaluating only the 64 corners is not a
general polynomial enclosure algorithm.

Define rational affine expressions

    f_lo(z)=l0+lT*T+lH*H+lrho*rho,
    f_hi(z)=u0+uT*T+uH*H+urho*rho.

Nonnegativity in (1) proves the pointwise enclosure

    f_lo(z)<=f(sigma,z)<=f_hi(z)       for sigma in B.      (4)

This is an enclosure of coefficients, not an identification of independently
chosen coefficient endpoints with one common shape. Losing those
correlations enlarges the feasible set, as required for an outer model.

If alternative compact coordinates introduce rational coefficients, either
clear denominators with a proved common positive multiplier before using
(3), or use certified rational-function intervals on boxes whose denominator
is separated from zero. A denominator interval containing zero is not
grounds for choosing a sign or silently dividing.

## Sound atom replacements, including strict atoms

Use the following replacements, and preserve the original AND/OR tree:

| Original atom | Necessary outer atom |
| --- | --- |
| f>0 | f_hi>0 |
| f>=0 | f_hi>=0 |
| f<0 | f_lo<0 |
| f<=0 | f_lo<=0 |
| f=0 | f_lo<=0 AND f_hi>=0 |

First put any logical negations into the atoms; independently weakening
an expression below a remaining NOT is unsound. Disequalities can be
expanded as f<0 OR f>0.

For example, an observer guard is an OR of four transformed barycentric
coordinates <=0; replace each coordinate by its lower affine envelope.
A gauge threshold is a finite OR of signed-subset sums minus beta*rho
being >0; use the upper affine envelope for each such sum. The true height
identity H-x*rho-(y-x)*T=1 becomes two enclosing non-strict inequalities.
Off-diagonal positivity and all other domain constraints use the same
table. These replacements retain every actual point in B.

The inherited rectangle exclusions are ORs of strict inequalities. Keep
their strict form and their original Boolean structure. If shape-only
interval reasoning cannot settle such a complement, retaining the
corresponding necessary outer atom or dropping that whole constraint is
sound. Declaring the entire closed cell excluded merely because its
interior misses a rectangle is not sound on a shared face.

## Widths and the two determinant signs

Split the actual domain into s=+1 and s=-1, with sD>0. Equation (2) gives
the stronger linear-in-fiber atom

    sD-rho/M>0.                                         (5)

Its interval outer replacement is

    U_s-rho/M>0,       where sD(B) is contained in [L_s,U_s].

Thus a branch can immediately be discarded if U_s<=W/M; equality also
discards the branch because both lower bounds are strict. A box whose D
interval crosses zero need not be divided merely to define the model:
run both sign branches, retaining (5) in each. It may nevertheless be
profitable to subdivide such a weak cell.

For a directional pair numerator Nhat_ij from the certificate, the exact
width target in sign branch s is the disjunction

    OR over i<j and epsilon in {-1,+1}:
          epsilon*Nhat_ij-W*sD>0.                       (6)

This avoids interval division by D. Apply the coefficient table to each
atom in (6). The fifteen-direction completeness lemma remains the source
of the claimed scope of those directions; an interval construction does
not establish completeness on its own.

## What a checked box refutation proves

Add the rational bounds (1) and all chosen outer atoms to a QF_LRA model
for each determinant sign. For every admissible shape in B, the exact
transformed body supplies a satisfying assignment to at least its true
sign branch, unless the original geometric assumptions themselves fail.
Therefore refuting both outer branches excludes all such actual bodies
in B, including irrational shapes and chart-endpoint ties x=0 or y=1.

A cvc5 proof checked by Ethos against the exact emitted SMT-LIB reference
establishes infeasibility of that particular rational outer formula. A
separate arithmetic audit must bind its intervals to B, its polynomial
coefficients to the reviewed certificate, and its atom directions and
Boolean structure to the original fiber formula. A proof checker alone
does not validate those mathematical encoding implications.

Use closed boxes to make overlapping boundary coverage direct. A finite
union of certified boxes proves only the union actually covered. No
point sample, however numerous, can replace this coverage statement.
The compactness of the three projective variables in (1) does not prove
compactness of the six shape variables.

## When lifting from a point is guaranteed, and when it is not

Infeasibility at one rational shape is insufficient by itself. The strict
system 0<z<a is infeasible at a=0 and feasible for every a>0; the point
refutation has no two-sided neighborhood of validity.

A sufficient robustness condition is infeasibility of the fully closed
fiber formula at the point, with the closed bounds

    W<=rho<=M,             0<=T<=rho,             0<=H<=rho.

Here close every strict primitive inequality while retaining its AND/OR
structure. If this closed formula is infeasible, polynomial interval
enclosures that converge under box contraction eventually give an
infeasible closed outer formula on a neighborhood of that shape.

To prove this, otherwise choose feasible outer assignments on a sequence
of shrinking boxes. Compactness of the displayed z-domain gives a
convergent subsequence. There are only finitely many choices of branches
in the disjunctions, so choose a further subsequence with the same choices.
Every coefficient enclosure converges to the exact point coefficient.
Passing to the limit in the closed affine inequalities produces a
feasible assignment for the closed point formula, a contradiction.

This argument is a local existence result, not a universal termination
theorem for a covering campaign. Closing strict branches may introduce
degenerate feasible points; failure of the robustness condition does not
prove existence of an actual body. Direct checked interval refutation,
when obtained, remains valid without the robustness condition.
