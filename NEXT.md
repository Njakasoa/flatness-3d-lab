# Next scientific actions — 58 candidate contact types remain

CLAIM-0008 proves w<=17/5 for the full relative-interior facet-contact type
P=conv(0,(5,1,1),e2,e3). Five complete height squares have independently
encoded cvc5 refutations checked by Ethos. Combined with CLAIM-0006 and
CLAIM-0007, 58 necessary full hulls remain at width at least 2+sqrt(2):
five tetrahedral classes (indices 0,1,2,3,5), 52 larger spatial hulls and
the square. The list above (11/7)(1+2/sqrt(3)) remains 62.

1. Keep results/det5_combined_residual_queue.json as the exact pending
   domain: 258 entries, with strict boundaries and all prior cuts preserved.
   The new proof slices strengthen CLAIM-0009 to (102/65)A on the entire
   [3/5,1]^2 corner, below the original contact-reduction threshold (11/7)A.
   The remaining queue still targets 17/5; do not lower all inherited cuts.

   The exact ordered chart now has eight quadratic parameters, with no
   lifted products. Six horizontal parameters sigma=(x,y,c,e,r,u) determine
   D and the whole horizontal gauge norm. Over each fixed rational sigma,
   the remaining theta,h parameters become a rational linear-arithmetic
   fiber after T=theta/b,H=h/b,R=1/b, H-xR-(y-x)T=1. This includes all
   fifteen target widths, finite guards and chosen gauge necessities.

   The exact fiber oracle is implemented and independently audited.
   Implement rigorous interval lifting from the stored coefficient certificate.
   Its purpose is to optimize/eliminate both fiber variables completely,
   then derive conditions covering the six-dimensional shape domain.
   Do not count sampled shapes as a continuous cover. The compact coordinates (p,q,C,E,r,u) are bounded and 1-pq has a
   proved positive margin. The old c,e coordinates have no uniform unit bound;
   D=0 is singular, and empty strict branches
   must be rejected before taking closures for a supremum.

   The weak ten-gauge Y-only chart has an actual hollow counterexample:
   q=(0,0,1/8,1), widthY=2048/593. Thus mere exact height reconstruction
   cannot close that target. Full lambda=801/2560 fails at (1,-1,1), and
   even a previously tested gauge fails strong beta=183/500. Preserve this
   witness; it does not show the missing vector remains decisive after
   strengthening beta. Its global width is only about 2.442 in U.

   The new complete eight-variable model uses strong beta, eleven gauges
   and all fifteen widths. Both order branches are UNKNOWN after 20 seconds.
   Do not repeat those unchanged targets, the old 22-variable UNKNOWN models,
   or the six SAT linear relaxations. See [chart](proofs/DET5_RATIONAL_HEIGHT_CHART_REVIEW.md),
   [linear fiber theorem](proofs/DET5_HORIZONTAL_FIBER_REVIEW.md), and
   [complete model](proofs/DET5_QUADRATIC_FULL_WIDTH_REVIEW.md).
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

The curated GitHub snapshot is being updated under explicit user authorization.
The new band cut refines 70 of 258 residual entries; it preserves 188 other
charts. The combined queue also removes the separately checked continuous rectangle. Neither operation establishes
that every retained entry is nonempty. The scientific objective remains open.
