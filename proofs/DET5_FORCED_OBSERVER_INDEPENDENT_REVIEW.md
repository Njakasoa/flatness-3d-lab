# Independent review of the forced observer branch

Status: PASS. This is an independent internal analytic review of
[the convex rectangle proof](DET5_FORCED_OBSERVER_BRANCH.md), with sources
bound in [the review receipt](../results/det5_forced_observer_independent_review.json).
It strengthens the earlier positive-determinant result; the earlier proof
and its weaker bounds remain valid. No old archive or proof was modified.

For fixed canonical `x,y,C,E`, retain `A=C+pE>0`, `B=qC+E>0`,
`S=C+E<1`, `V=F(e1-e2)`, and `Z=F(e3-e0)`.
The two observer reductions and their order-specific coefficients are
correct. The first observer implies `ku<=B`, where `k=3` forward and `k=2`
reverse. If the main second-observer alternative `kr<=A` also holds, the
strict-contact pair `(u,r)` lies in the stated closed rectangle.

Independent substitution gives the four values of `kV-Z`:

    -Z,
    ((1-y)A,0,-A,yA),
    (-(1-x)B,B,0,-xB),
    0.

Their half-l1 norms are exactly `S,A,B,0`. Since `0<=x<y<=1`, these
computations remain valid at both tied-extremum endpoints. Affineness of
`kV-Z` in `(u,r)` and convexity of the norm bound the entire rectangle
by `S`; no determinant-sign premise is used. Its corners are only points
of an outer domain, so their possible failure of strict contact positivity
does not affect the argument.

The physical vector in forward order is `(3,0,1)`, with contact-difference
coordinates `(1,3,-3,-1)/5`, giving `(3V-Z)/5`. In reverse order `(2,0,1)`
has the conjugated contact coordinates `(-1,-2,2,1)/5`, giving `(Z-2V)/5`,
up to a norm-preserving row permutation. Thus in both orders the relevant
nonzero lattice gauge is at most `S/5<1/5`.

ACMS Lemma 5.1 therefore gives the strict full-width bound
`w<(5/4)*(1+2/sqrt(3))` on the main second-observer branch. This reasoning
uses exact contact positivity and necessary hollowness guards, without
prior large width, a volume margin, or finite-gauge sufficiency.
At equality in the width threshold, ACMS already gives `lambda1>=1/5`,
which contradicts the strict gauge bound. Consequently `w` at least that
threshold forces `kr>A`. The original observer disjunction then forces
its exceptional `R0` alternative. The inequality of `R0` remains
non-strict because the observer may be on a facet boundary.

Since `ku<=B`, the forced strict inequality gives
`D=uA-rB<=AB/k-rB<0`. Conversely, `D>=0` would force
`r<=uA/B<=A/k`, placing the pair in the excluded main branch.
Thus the same strict width bound applies to actual positive-determinant
bodies in both orders, and the negative determinant sign is necessary
already at the improved threshold. Invertibility excludes `D=0` for an
actual full-dimensional body.

The canonical `R0` formulas have different coefficient orderings, but in
the original physical contact indexing they are the same condition:

    F03 >= 3*F01+2*F02.

Indeed this is exactly the row-0 nonpositivity condition for the original
integer observer `(3,1,1)`, whose affine contact coordinates are
`(1,3,2,-1)/5`. Row 0 stays fixed under the canonical swap, while columns
1 and 2 exchange. It would be incorrect to apply the reversed canonical
weights directly to the unchanged original matrix.

No correction is needed. The result forces one remaining observer branch
and a determinant sign in the stated Y[0,3] chart. It does not exclude
that exceptional branch, the other height charts, or the whole contact
class, and proves no new global flatness bound.
