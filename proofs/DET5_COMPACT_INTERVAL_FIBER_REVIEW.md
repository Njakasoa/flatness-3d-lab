# Independent audit of compact interval fiber models

This note reviews `experiments/det5_compact_interval_fiber.py`. The accompanying
`tests/audit_det5_compact_interval_fiber.py` reconstructs the full polynomial
model, each interval formula, and archived inputs independently. It makes no
solver queries and does not promote an archived status to a geometric proof.

## Cleared coefficients and physical directions

The audit independently eliminates the stochastic column equations and the
contact-height equations in both height orders. With
`J=[e1-e0,e2-e0,e3-e0]`, it constructs `F J=J G` and obtains coordinate-pair
numerators from `P J adj(G)`. The physical contact matrix P remains in its
original order when the canonical matrix is conjugated by the swap of indices
1 and 2. This checks the reverse branch without importing the compiler's
sparse coefficient decoder or its matrix-construction function.

Write `L=1-p*q`, with the compact substitution

    x=p*(1-q)/L,   y=(1-q)/L,
    c=C*L/(1-p),   e=E*L/(1-q).

The independent [denominator proof](DET5_COMPACT_FIBER_DENOMINATOR_REVIEW.md)
shows that multiplying the projective matrix and all coordinate-pair
numerators by L clears their rational shape denominators. The resulting
polynomials are affine in `(alpha,eta,rho)`. The horizontal determinant is
unchanged by substitution:

    D=u*(C+p*E)-r*(q*C+E).

An actual contact body in the chart has `p,q in [0,1)`, so `L>0`.
For a fixed determinant sign `s=+1` or `s=-1`, the exact width inequalities
are therefore the signed pair disjunctions

    +/-5*(L*Nhat) > 17*s*D*L.

The multiplier on the right is essential: the compiler correctly includes
L there. In either sign branch the determinant-margin premise implies
`s*D>0`, so this is the same as multiplying the actual `abs(D)` formula
by positive L. The Y target is `rho>17/5`; the other fourteen covectors
have all six pair differences and both signs. The independently enumerated
fifteen-direction completeness argument remains the one for the fixed
contact hull, whose other primitive directions have width at least four.

The audit checks all eleven physical lattice-vector gauges, all twenty
observer disjunctions, and all nine inherited rectangle complements. In a
compact coordinate, a height numerator n represents height `n/L`, so the
outside comparisons are `lo*L-n>0` or `n-hi*L>0`. They remain strict.
Endpoint controls for each closed excluded rectangle reject its boundary.

## Additional shape constraints and their scope

The compact chart has `C,E,r,u>0`, `C+E<1`, `r,u<1`. Under the hollow global
target `w(K)>17/5`, set `beta=183/500` and
`M=6/(5*beta^3)=50000000/2042829`. The interval model uses the necessary
conditions

    17/5 < rho < M,       s*D > rho/M,
    C+E > beta,
    L > 49/1500 (low/high order), or L > 249/1700 (reverse order).

The determinant condition follows from `vol(K)=5*rho/(6*abs(D))` and
the global volume consequence. It cannot be inferred merely from selected
finite gauge lower bounds. Similarly `M*(1-p)>L` follows from
`gap>1/M`, `h=x+(y-x)*theta+gap<1`, and `theta>0`, which give
`1-x>gap`; here `1-x=(1-p)/L`.

The simplified first observer gives `k*u<=q*C+E`, with k=3 in the first
order and k=2 in the reverse order. Put A=`C+p*E` and B=`q*C+E`.
When D is positive, strict positivity yields

    D=u*A-r*B < A*B/k.

Together with `D>rho/M>(17/5)/M`, this implies the stored strict product
margin `A*B>k*(17/5)/M`. This is a valid additional necessity, not a claim
that any positive-determinant contact body survives the other analytic
constraints. The separate sign theorem can exclude that branch while an
interval relaxation of it still has a spurious SAT assignment.

## Why the interval model is an outer model

On a closed shape box inside `[0,1]^6`, each monomial is monotone in every
coordinate. Its exact range is bounded by the products of lower and upper
endpoints raised to their nonnegative integer powers. For a negative
coefficient the endpoint contributions exchange roles. Summing these term
bounds gives a valid rational enclosure of each polynomial coefficient.
The audit implements this direct monotone-monomial construction independently
of the compiler's iterative interval multiplication.

For an affine fiber polynomial

    f=c0+c1*alpha+c2*eta+c3*rho,

coefficient bounds provide `f_lower<=f<=f_upper` because the model explicitly
requires `alpha,eta,rho>=0`. Thus `f>0` implies `f_upper>0`, `f<=0` implies
`f_lower<=0`, and `f=0` implies **both** `f_lower<=0` and `f_upper>=0`.
Applying these implications inside each disjunction preserves every actual
solution. Closing strict comparisons is an additional weakening and hence
also valid for a refutation; it is not an equivalence of feasible sets.

Nonnegative fiber variables, inequality polarity, and conjunction in the
equality case are tested with adversarial controls. Negative variables would
invalidate coefficient-wise bounds. A lower bound substituted for an upper
bound in a positive inequality could wrongly discard a genuine solution.
An OR instead of the two equality bounds would lose the normalization.
Other controls detect missing width directions, missing width multiplier L,
and the wrong physical reverse-order image.

## The first checked interior box

The archived negative-determinant, low/high-order box is

    p in [1/8,1/4],    q in [3/8,1/2],
    C in [1/4,3/8],    E in [3/8,1/2],
    r in [1/2,3/4],    u in [1/8,1/4].

Its exact six-dimensional parameter volume is `1/131072`. Its interval
statement has a reference-bound Ethos proof. The audit separately binds
that successful receipt to the reconstructed input, exact proof bytes,
normalized reference, pinned checker revisions, and negative assumption
control. This covers only the stated box and hypotheses.

The cause of this refutation is already visible in one shape gauge. With
V=`F(e1-e2)` and Z=`F(e3-e0)`, the physical vector `(1,0,0)` has image
`(V-2*Z)/5`. After multiplying by L, its coefficients have no alpha or eta
terms. Every one of its fourteen subset upper bounds has a rho coefficient
at most `-623/32000`. Since `rho>17/5`, its required strict positive gauge
atom is impossible. Thus this certificate demonstrates continuous shape-box
exclusion, but does not demonstrate a nontrivial interaction of the two
remaining fiber variables. The archived whole-cube interval models are SAT
relaxations; they are neither actual bodies nor counterexamples to the
separate analytic sign theorem.

The two fixed-shape oracle controls use `(p,q,C,E)=(1/3,1/4,1/5,1/4)`
and `(r,u)=(1/10,1/2)` or `(1/2,1/10)`, in both height orders. They
admit strict contact matrices: take `theta=1/2` and respectively `h=3/5`
or `h=7/10`. Exact substitution gives gaps `3/55`, `17/110` and matrix
determinants `67/11000`, `-1241/66000`. These are valid contact-domain
controls of both determinant signs; no hollowness assertion is made.

Finite rational point checks, exact interval fixtures, and this one box do
not cover the remaining continuous shape domain. The audit record reports
its precise coefficient, fixture, formula, endpoint, and archived-input
coverage separately from any geometric exclusion.
