# Next scientific actions — 58 candidate contact types remain

Public snapshot: this authorized GitHub update includes the determinant-sign
theorem and four-base projection/box results from source d92d08d. Historical
statements below about local-only work describe earlier research checkpoints.
The global conjecture remains open.

CLAIM-0008 proves w<=17/5 for the full relative-interior facet-contact type
P=conv(0,(5,1,1),e2,e3). Five complete height squares have independently
encoded cvc5 refutations checked by Ethos. Combined with CLAIM-0006 and
CLAIM-0007, 58 necessary full hulls remain at width at least 2+sqrt(2):
five tetrahedral classes (indices 0,1,2,3,5), 52 larger spatial hulls and
the square. The list above (11/7)(1+2/sqrt(3)) remains 62.

1. Use the unchanged 258-entry combined height queue together with the new
   necessary sign det(F)<0 throughout Y[0,3]. CLAIM-0011 removes the entire
   opposite sign in both orders already at width>=(5/4)(1+2/sqrt(3)),
   and forces the original physical row clause F03>=3F01+2F02. Do not rerun
   positive-sign searches or mistake their SAT outer relaxations for bodies.

   The exact compact interval compiler is implemented; independent auditing
   and one reference-bound CPC replay check the first continuous six-shape
   box. That box is a simple horizontal-gauge exclusion. Whole-cube negative
   root remains SAT as an outer relaxation; no cover or actual body follows.
   Preserve the three interval-query archives. Two additional forced-observer
   matrix relaxations are SAT with actual extrema outside Y[0,3]; retain those
   controls too. A stronger target must restore the actual-height conditions.

   The surviving negative-determinant horizontal subsystem now has an exact
   strict projection over (p,q,C,E). Its stored implementation retains twelve
   piece selections per order; an independent analytic reduction shows that
   four suffice in the forward order. Exact rational witnesses establish only
   feasibility of this necessary subsystem, not actual body existence.
   Carry the remaining t,h chart conditions, full widths and other observers
   into the next structural step; do not repeat the archived fixed-base probe.

   Use the new forward cuts B>183/200 OR B-A>83/200 and LE>183q/250;
   the reverse cuts are LE>549q/500 and A-B<17/100. For the forward H2
   alternative, its one-gauge subsystem is feasible exactly when
   1+2(B-A)>183/100, LE+2q(B-A)>549q/250, and
   1-q+LE/2+2(B-A)>183/100. This limited sufficiency does not extend to
   the full four-gauge, volume, observer or complete-width problem.

   The closed four-base box [0,1/32] x [31/64,33/64] x [3/64,5/64] x
   [31/64,33/64] is now continuously excluded in the forward order by
   the last expression's upper bound 3597/2048. Its independent analytic
   review covers every remaining admissible a,tau,t,h. Retain restrictions
   on C,E: its height enclosure cannot be inserted as an excluded Y rectangle.
   The 258-entry height queue stays unchanged. See
   [box proof](proofs/DET5_PROJECTED_BASE_BOX.md),
   [exact H2 projection](proofs/DET5_FORWARD_MIDDLE_GAUGE_EXACT_PROJECTION.md),
   [base cuts](proofs/DET5_FOUR_BASE_SHAPE_CUTS.md), and
   [projection audit](results/det5_horizontal_projection_validation.json).

   The single multiplier L=1-pq clears all original fiber coefficients.
   On the true target both L and B have positive margins. Use these proven
   bounds for interval arithmetic and eliminate empty strict branches before
   closing optimization domains. See [normal form](proofs/DET5_NEGATIVE_DETERMINANT_GAUGE_NORMAL_FORM.md),
   [denominator proof](proofs/DET5_COMPACT_FIBER_DENOMINATOR_REVIEW.md), and
   [interval compiler](proofs/DET5_COMPACT_INTERVAL_FIBER_REVIEW.md).

   Keep the exact weak-model hollow witness, its complete gauge minimum and
   all prior UNKNOWN records. Its failure at strong gauges remains a useful
   control; it is not a counterexample to global flatness or the new sign.
2. Keep the contact hypothesis precise. The P5/P7/P8 bounds require one
   prescribed relative-interior point per facet of a tetrahedron. They do
   not exclude larger contact hulls by containment. The P10/P13 analytic
   bounds have the broader tetrahedral containment hypothesis.
3. Extract shorter analytic proofs from the successful linear refutations.
   Preserve the existing checked certificates; do not rerun unchanged
   solver nodes or mistake a sampled fiber list for a continuous cover.
4. Investigate the remaining tetrahedral types and nonsimplicial branches.
   Neither global optimality nor realization of all remaining contact
   configurations has been established.
5. Mathematical priority remains unconfirmed. The primary-source audits
   identify the established ACMS contact programme and McCormick relaxations.
   Any novelty claim needs a fuller literature and human mathematical review.

Reproduce the completed exclusions with `reproduce_height_cover.py` and
`reproduce_det5_class4.py`. Their default modes check archived evidence;
actual external proof-kernel checking uses the pinned sources documented in
[HEIGHT_ETHOS_REPRODUCTION.md](proofs/HEIGHT_ETHOS_REPRODUCTION.md).

The latest four-base projection and analytic box exclusion are prepared for
the GitHub publication now authorized by the user; this source update does
not itself establish that export has completed. The active scientific
objective remains open.
