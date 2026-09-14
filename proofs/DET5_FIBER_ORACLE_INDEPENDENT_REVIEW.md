# Independent review of the fixed-shape linear compiler

The compiler implements the algebraic reduction in
[the horizontal-fiber proof](DET5_HORIZONTAL_FIBER_REVIEW.md). The independent
[audit](../tests/audit_det5_fiber_oracle_independent.py) reconstructs its formulas
from the two column-height equations and column stochasticity. It does not use
the compiler or its coefficient certificate to construct expected formulas.
The compiler is imported only as the object under test in additional fixtures.
No discovery solver or proof-kernel calls are made by this audit.

For each ordered fixed shape, the independently eliminated matrix is restricted
to the zero-sum three-space using the basis `B=[e1-e0,e2-e0,e3-e0]`. Computing
`P B adj(G)`, where `F B=B G`, supplies all eighteen coordinate-pair numerators.
The audit then substitutes `theta=alpha/rho`, `h=eta/rho`, multiplies by `rho`,
and checks every sparse stored coefficient against this independent expression.
The normalization is exactly

    eta-low*rho-(high-low)*alpha=1,     rho>0.

Thus the three declared variables have two degrees of freedom. With
`D=u*((1-low)c+low*e)-r*((1-high)c+high*e) != 0`, each actual pair difference
is the transformed numerator divided by `D`. Both signs of `D` are tested.
The compiler correctly uses `17*abs(D)` on the right of the signed inequalities
`5*Nhat>17*abs(D)`, rather than inserting an additional factor of `rho`.

All eleven lattice-vector gauges, all twenty contact observer guards, and all
eight strict complements are independently reconstructed. Each rectangle is
also bound to its existing independently checked full-matrix proof input and
proof hashes. Separate endpoint fixtures test all eight rectangles: a boundary
point remains excluded. A non-strict outside comparison would incorrectly
admit that point and is rejected by the test.

The complete covector list is re-enumerated independently. If the contact
hull has width at most three in an integer direction `(a,b,c)`, then
`|b|,|c|<=3` and `|5a+b+2c|<=3`, whence `|a|<=12/5`. Enumerating this finite
box gives precisely fifteen primitive directions up to sign. Every other
primitive direction has contact width at least four. The Y condition is
`rho>17/5`; each of the remaining fourteen directions contributes its full
signed six-pair disjunction.

When global-target volume cuts are enabled, the upper constant is computed
independently as `R=6/(5*(183/500)^3)=50000000/2042829`. Since
`vol(K)=5*rho/(6*abs(D))`, the volume bound gives `rho<R*abs(D)`.
The supporting width-to-volume lemma gives `rho<R`. The additional
`0<eta<rho` is the transformed condition `0<h<1`. Volume cuts without the
complete-width flag are rejected by the compiler.

The frozen positive control has all 56 original assertions true. Serialization
omits one redundant trailing `true`, leaving 55 true assertions in the file.
The stronger complete-target control has 74 assertions: 69 true and five false
under the same exact rational assignment. The audit verifies every recorded
truth value by exact substitution; it does not infer satisfiability or
unsatisfiability from metadata. Eighteen additional in-memory fixtures exercise
both height orders, both determinant signs, and all three flag combinations.
Singular and unordered shapes, missing normalization, missing gauges, missing
width directions, and incorrect rectangle endpoint handling are rejected.

The fixed-height anchor is a separate six-variable formula, with
`low=0`, `high=1/8`, eleven gauges strictly above `183/500`, twenty guards,
and all eight certified complements. Its complete assertion multiset is
independently reconstructed from column elimination. This verifies the meaning
of its input; its recorded UNSAT status requires the separately bound external
proof check before it supports an exclusion.

The scope distinction matters. A run with `full_width=False` omits fourteen
width constraints from a necessary relaxation of the hollow global target.
In particular, at a lowered gauge threshold such as `3/10`, the inherited
rectangles do not follow merely from Y width greater than `17/5` and those
weaker finite gauges. Exactness is relative to the explicitly restricted
residual domain, or the constraints are used as necessary consequences of the
hollow global target. The positive control already lies outside all eight
rectangles, so this distinction does not affect that control.

Neither finite controls nor fixed-shape linear feasibility cover the continuous
six-dimensional shape domain. This review proves compilation correctness on
the tested inputs and the stated algebraic construction; it supplies no whole
contact-class exclusion and no new global flatness bound.
