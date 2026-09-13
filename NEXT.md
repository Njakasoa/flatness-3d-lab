# Next scientific actions — 58 candidate contact types remain

CLAIM-0008 proves w<=17/5 for the full relative-interior facet-contact type
P=conv(0,(5,1,1),e2,e3). Five complete height squares have independently
encoded cvc5 refutations checked by Ethos. Combined with CLAIM-0006 and
CLAIM-0007, 58 necessary full hulls remain at width at least 2+sqrt(2):
five tetrahedral classes (indices 0,1,2,3,5), 52 larger spatial hulls and
the square. The list above (11/7)(1+2/sqrt(3)) remains 62.

1. Continue the second determinant-five class using several width directions.
   An exact hollow Y-wide witness passes the exact global gauge threshold;
   the Y-only approach is disproved. The joint Y/U campaign remains partial:
   13 of 36 charts complete, 131 pending boxes after 217 nodes. Sixteen
   additional point fibers are UNSAT; they give no class exclusion. See
   [the research status](proofs/DET5_RESEARCH_STATUS.md).
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

The user authorized publication of this checkpoint on GitHub on 2026-09-14.
The active scientific objective remains open; this is a restricted advance.
