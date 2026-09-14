# Next scientific actions — 58 candidate contact types remain

CLAIM-0008 proves w<=17/5 for the full relative-interior facet-contact type
P=conv(0,(5,1,1),e2,e3). Five complete height squares have independently
encoded cvc5 refutations checked by Ethos. Combined with CLAIM-0006 and
CLAIM-0007, 58 necessary full hulls remain at width at least 2+sqrt(2):
five tetrahedral classes (indices 0,1,2,3,5), 52 larger spatial hulls and
the square. The list above (11/7)(1+2/sqrt(3)) remains 62.

1. Keep results/det5_enlarged_residual_queue.json as the exact pending
   domain: 258 entries, with strict boundaries and all prior cuts preserved.
   The new proof slices strengthen CLAIM-0009 to (102/65)A on the entire
   [3/5,1]^2 corner, below the original contact-reduction threshold (11/7)A.
   The remaining queue still targets 17/5; do not lower all inherited cuts.

   Use the exact geometric reduction on the whole Y[0,3] chart: q1≠q2,
   min(q1,q2)<offset<max(q1,q2), and a fixed linear Z-gauge formula per
   order branch. The common contact section is a quadrilateral with two
   adjacent contact edges. This is a possible entry to a planar section
   argument or a smaller exact parameterization.

   Six ordered linear models are SAT. Their reconstructed bodies are hollow
   and pass the ten gauges, but all have different actual Y extrema and
   Y-width<17/5. They do not refute the remaining chart target. Two nonlinear
   models restoring all six products are UNKNOWN after 15 seconds. Preserve
   these archives and derive a smaller exact system before more solver calls.
   The eight row-difference envelopes already hold at both offset-model
   witnesses, so repeating that particular strengthening is not useful.
   See [proof slices](proofs/DET5_CORNER_PROOF_SLICES.md),
   [ordering lemma](proofs/DET5_Y_CORNER_ANALYTIC_PROBE.md), and
   [actual matrix audit](results/det5_ordered_actual_matrices.json).
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

The new height-domain theorem, residual queue and coupled experiments are
included in this public snapshot; SOURCE_MANIFEST.json identifies the source.
The active scientific objective remains open.
