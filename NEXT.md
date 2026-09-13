# Next scientific actions — 58 candidate contact types remain

CLAIM-0008 proves w<=17/5 for the full relative-interior facet-contact type
P=conv(0,(5,1,1),e2,e3). Five complete height squares have independently
encoded cvc5 refutations checked by Ethos. Combined with CLAIM-0006 and
CLAIM-0007, 58 necessary full hulls remain at width at least 2+sqrt(2):
five tetrahedral classes (indices 0,1,2,3,5), 52 larger spatial hulls and
the square. The list above (11/7)(1+2/sqrt(3)) remains 62.

1. Reuse the twelve independently certified Y rectangles before extending
   the complete-width model. The exact overlay wholly covers one of the
   259 archived joint pending boxes and half of six others; 105 further
   intersections are boundary-only. The archive remains immutable. Removing
   the whole box leaves 258 entries; partial subtraction still needs an
   explicit queue with exact endpoint handling. No new queue is claimed here.
   On the Y:[0,3] upper corner, the independently checked uniform threshold
   3/10 gives the conditional bound (10/7)(1+2/sqrt(3)); this removes neither
   the entire chart nor the contact class. The 69-assumption proof slice
   shows the previous box certificate uses no U conditions or extra widths.
   Its Y square was already an old closed leaf. Use the 17-variable complete
   scaled frame and the direction-coupled envelopes on the residual domain.
   Do not repeat archived solver queries or infer bodies from relaxed SAT.
   See [conditional bounds](proofs/DET5_CONDITIONAL_WIDTH_BOUNDS.md),
   [cylinder correction](proofs/DET5_Y_HIGH_CYLINDER_EXCLUSION.md), and
   [overlay](results/det5_certified_y_overlay.json).
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

The maintainer has authorized publication of this reviewed checkpoint.
The curated public SOURCE_MANIFEST.json records its scientific source revision.
The active scientific objective remains open; these are restricted advances.
