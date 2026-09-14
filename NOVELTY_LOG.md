# Novelty log

Audit date: 2026-09-13. Search coverage is logged in references/LITERATURE_SEARCH.md.
A search finding no newer theorem is not a proof that none exists.

| Item | Status | Rationale |
|---|---|---|
| Width 2+sqrt2 tetrahedron | KNOWN / REDISCOVERED computationally | Codenotti–Santos, 2018 preprint / 2020 publication |
| Strict local maximality | KNOWN; reconstruction | Averkov–Codenotti–Macchia–Santos |
| Global upper bound <3.972 and volume window | KNOWN; exact constant replay | ACMS Theorem 5.2 |
| Finite contact hull reduction, det<=17 tetrahedral case | KNOWN; executable partial enumeration | ACMS Theorem 5.4 |
| Uniform inverse-basis direction box | VERIFIED IMPLEMENTATION of elementary argument | No claim of mathematical priority |
| Barycentric coordinate enclosure from volume | Elementary consequence / not claimed novel | Standard simplex visible-facet volume decomposition |
| High-width non-tetrahedral truncations | Elementary scope obstruction | No claim of novelty; not about maximal bodies |
| Numeric return to known width without symmetry seed | Level 0 observation | Incomplete fixed-contact family and correlated iterates |
| Planar intrinsic bound N lambda1(T-T)^2<=2 | POSSIBLY NOVEL refinement | White two-layer structure + planar Minkowski; no priority guarantee |
| Explicit63necessary contact hulls above11A/7; nine-template compression | POSSIBLY NOVEL, internally verified theorem | Exact enumeration, complete argument, independent replay and adversarial review |
| Improved global Flt(3) bound | NOT ESTABLISHED | Continuous optimization of surviving contacts remains open |

The 2026 one-point planar flatness paper concerns Flt(2,1), not Flt(3,0).
Do not describe it as resolving this project's conjecture. No publication,
priority claim, contact with authors, or external release is authorized by the
scientific results alone. The user separately authorized GitHub publication of
the reproducible baseline and subsequent reviewed checkpoints in the curated
public checkout. The latest export is separately authorized; mathematical
priority remains unconfirmed, and no external peer review or journal/arXiv
submission has occurred.

The new tetrahedral refinement audit is proofs/CONTACT_MINIMA_LITERATURE.md.
The complete-contact-hull audit is proofs/CONTACT_HULL_NOVELTY_AUDIT.md. A mathematical
corollary of known tools can be correct and useful without being novel.

## Subsequent continuous-class probes

The determinant-two witnesses at widths about 3.28338 and 3.25380 are exact
examples and scope controls, not claimed novel extrema. The latter has exactly
four index-two contacts and persists on an open parameter neighborhood.
The cube-contact axis-width proposal encounters Lassak's inscribed-parallelotope
conjecture; his established mixed width/chord inequality supplies a necessary
condition instead. An additional 2008 source credits Howe's eight-point
extension principle. See references/EIGHT_FACET_RESEARCH_SOURCES.md.


## Pair matrix and lower-degree model

The bipartite pair matrix admits an exact rooted-forest determinant expansion
and a strict inverse sign pattern. These specialize established matrix
arguments; no novelty claim is made. Their role here is to preserve all
boundary cases while simplifying the feasibility model. Complementary-minor
identities yield a thirteen-variable cubic encoding. This is an algebraic
reformulation, not a new width theorem, and its solver implementation remains
a next step. The two additional eight-variable queries returned UNKNOWN.


## Complete observer guards and gauge truncation

Date: 2026-09-13. The twelve-line contact criterion is an internally verified
application of known observer methods and the five-point width-one theorem.
Averkov–Schymura, Complexity of linear relaxations in integer programming,
Lemma 6.4, is a close antecedent: observers lie on neighboring lattice lines
plus a finite exceptional set. Blanco–Santos 1409.6701v3 supplies the empty
five-vertex width-one input. Neither underlying principle is new.

The boundary-contact specialization, exact 1456/484 determinant-two list,
and subsequent six-edge-gauge truncation to 64/20 are explicit verified
results of this lab. The general nonunimodular version has at most 96 guards
under the six gauge hypotheses. No priority is established for these
specializations or convex-combination bounds. Narrow and 2025–2026 web
queries did not constitute an exhaustive novelty audit. CLAIM-0005 records
sources and limitations. The continuous width optimization remains open.

Two exact pair witnesses above 19/6, one with exactly 4 contacts, and two
nonhollow false high-width samples are certification/control results;
no optimum or global bound is asserted.

## Analytic containment bounds for determinants 13 and 10

The two-vector sign-loss argument now yields verified restricted bounds
(14+26/sqrt(3))/9 and (21+40/sqrt(3))/13 for hollow real tetrahedra containing
the specified contact configurations. This excludes two full tetrahedral
contact types at candidate width. It does not delete nonsimplicial hulls
containing those configurations or improve the global flatness upper bound.

The independent primary-source audit in DET13_CONTRACTION_LITERATURE.md
identifies the inherited ACMS gauge inequality and standard oscillation
contraction antecedents. No matching index-13 bound was found in ten bounded
queries, which is insufficient to establish novelty. Three additional
queries for determinant 10 returned mostly irrelevant results and the
Codenotti thesis record; no exhaustive determinant-10 priority check is
claimed. Both exact class bounds have unconfirmed external priority.

## Weighted determinant-eight bound

The weighted cancellation argument is a direct refinement of the already
reviewed two-vector proof. It gives (1+12A)/7 for the determinant-eight
containment class, without deleting that class at candidate width. No
separate priority audit establishes novelty of this numerical class bound.
The strict trace examples are exact falsifications of a proposed sufficient
intermediate condition. The complete seven/eight model timeouts are not
mathematical exclusions. No new global flatness bound is asserted.

## Exact height-cover exclusions (2026-09-14)

CLAIM-0007 is a verified computer-assisted restricted result: full P7/P8
relative-interior facet-contact tetrahedra have width<=17/5. The resulting
59-type candidate list uses the earlier P10/P13 exclusions as well. The
62 rational leaf refutations were independently encoded and externally
checked. Those computational checks establish neither priority nor external
human peer review. The eight-query primary-source audit in
proofs/HEIGHT_EXCLUSION_LITERATURE.md found no equivalent statement, but
ACMS already proposes the fixed-contact finite programme and McCormick's
relaxation method is established. Novelty status: POSSIBLY NOVEL, unconfirmed.
The rank/height determinant identity is supporting algebra, not itself
claimed a new geometry-of-numbers theorem. No global bound is improved.

## 2026-09-14 — first determinant-five facet-contact class

The restricted w<=17/5 result has a complete five-square proof chain. A
bounded primary-source audit found no equivalent statement, but priority
remains unconfirmed. The other determinant-five class is inequivalent and
remains open. See proofs/DET5_CLASS4_LITERATURE.md and CLAIM-0008.

## 2026-09-14 — complete d5a2 model and symmetry qualification

The new bilinear formulation and explicit finite direction list are
algorithmic research tools derived from elementary affine algebra and
existing ACMS/Minkowski bounds. No mathematical priority claim is made.
The exact both-wide directional witness is outside retained normalized
charts and does not refute their global-target reduction. No new global
or restricted-class upper bound is claimed in this follow-up.

## 2026-09-14 — retained full-gauge witness and containment lemma

An exact retained-chart witness disproves infeasibility of the two-direction
system even under all exact target gauge inequalities and the stated volume
bounds. This corrects the remaining possibility left open by the earlier
out-of-chart symmetry witness. It is a methodological obstruction, not a
new high-width example or class exclusion. Three witnesses have independent
exhaustive rational checks. The elementary nested-tetrahedron width/volume
lemma supplies formulation bounds; no novelty claim is made. A bounded
six-query literature search found no exact match but is insufficient to
establish priority. No global bound is changed.

## 2026-09-14 — scaled frame and five-direction continuous-box obstruction

Homogeneous vertex differences reduce the contact model to17variables with
linear width tests; fixed rational heights reduce it to12variables. These
are elementary formulation tools, not claimed new geometry-of-numbers
principles. One retained four-dimensional height rectangle is now refuted
with a cvc5 proof checked by Ethos. This is a restricted continuous-box
obstruction, not a new class bound or global flatness bound. No dedicated
priority audit or external human review has been completed for this box;
novelty is unconfirmed. The broader ACMS finite-contact programme remains
credited. Larger-box probes are not promoted to certificates.

## 2026-09-14 — Y-only proof audit and publication checkpoint

The previous turn made progress in complete modeling and certification, but
its certified box was an old Y-only closed region not inherited by the joint
frontier. All twelve old rectangles now have cvc5/Ethos certificates. A lexical
proof slice retains 69 hypotheses and needs no U condition or extra width.
The independently audited uniform beta=3/10 corner refutation yields the
conditional bound (10/7)(1+2/sqrt(3)); it uses no volume premise. This remains
a partial height-domain theorem, with no new class exclusion, global bound
or established mathematical priority. The 953-query archive is unchanged.
The exact overlay identifies one fully and six partly covered pending boxes.
Closed-model optimization returns a degenerate relaxed point at gap zero;
it supplies no additional geometric bound. The user explicitly requested
GitHub publication following the Ihara companion. Export the reviewed
scientific checkpoint and preserve the existing curated public history.

## 2026-09-14 — enlarged conditional corner and exact residual frontier

Previous goal turn: progress; publication 175896f completed and verified.
Current turn: progress. The old Y exclusions now have an exact258-entry
residual queue with strict boundary complements. Three new cvc5/Ethos
refutations prove the nested conditional bounds in CLAIM-0009, enlarging
the Y square to [3/5,1]^2 and strengthening its inner corner to(23/19)A.
The larger11/20 probe is exact relaxed SAT, with all six product identities
failing. A union-aware update removes new Y-area 3/40 and trims three queue
entries by 3/5 of their prior measure. The final queue still has 258 entries.

Independent agents verified the continuous interval/tau reasoning, all nine
coupled inputs, all four newcorner inputs, saved SAT values and exact residual
subtraction. Root verified all twelve Z-extrema branch inputs and ran a
standalone reference-bound replay of the three new proofs. Directional
coupling rejects all 14prior saved SAT assignments; nine strengthened queries
and twelve Z branches remain UNKNOWN. No old solver node was rerun. These
exploratory targets are frozen pending a structural simplification.
A bounded primary-source recency/priority audit found no basis for a novelty
claim. All 58 necessary types and the global bound remain unchanged. Work is
local after 175896f; the broad research objective is still active.

## 2026-09-14 — structural ordering and smaller sufficient proof premises

Previous goal turn: progress, committed as 6ffebe7. Current turn: progress.
Three lexical proof slices passed Ethos against their actual 60/49/51
assumptions; gap<5/17 is absent throughout. This strengthens CLAIM-0009
to (102/65)A on the entire 3/5 square, with the same certified region area.
Four planar lattice gauges suffice for that result. No new global bound
or whole contact-class exclusion follows.

A separate exact lemma forces unequal free heights, offset interlacing and
fixed Z-gauge signs; two guards reduce to two alternatives each. Root added
the general quadrilateral-section interpretation and independently reviewed
the reduced-premise implication. Six structurally strengthened linear
models are SAT, all independently reconstructed and rationally checked.
Their six actual F bodies are hollow and pass ten gauges, but have wrong
Y extrema and Y-width<17/5. Both nonlinear product-restored models remain
UNKNOWN under 15-second limits. Root audited both exact encodings.
The original archives remain unchanged and these new targets are frozen.
The next step should use the geometric section/order structure rather than
repeat the current product-envelope strengthening. Mathematical priority
is unconfirmed; the established ACMS inequality remains the main antecedent.
The work stays local after public 175896f and the broad goal remains active.

## 2026-09-14 — exact quadratic chart and horizontal-fiber reduction

Previous goal turn: progress. Publication c5cbbd2 was verified on GitHub,
with scientific source e42b25d and a repaired JSON-list replay. The research
objective remains open; no new publication is performed in this turn.
Current turn: progress, with four structurally new bounded queries.

Root derived an exact eight-parameter quadratic contact matrix, eliminating the
six lifted products and all eight column/height equations by construction.
Independent column elimination, endpoint fixtures and input audits pass.
One weak-gauge branch is SAT with a rational actual hollow body; the other
is UNKNOWN. Its widthY=2048/593, full width=218301984/89395343 and full
difference minimum=801/2560 are independently certified, including 112 primal
points, 15 complete width directions and 335 primitive gauge vectors. The weak
Y-only target is feasible; the body fails both a stronger old gauge and the
newly exposed vector (1,-1,1). No global counterexample follows.

Root then imposed all fifteen widths, beta 183/500 and the additional gauge in
an eight-variable degree-five formulation. Both 20-second targets are UNKNOWN.
Independent audits reconstruct all 75 assertions per branch and their exact
adjugate geometry. No old solver query was repeated.

A further analytic reduction separates six horizontal shape variables from
two fiber variables. Independent review proves that the restriction of F
to the invariant zero-sum space varies by a single rank-one update, making
all vertex-pair numerators jointly affine in the fiber. Projective scaling
yields exact rational linear constraints for every fixed rational shape.
The symbolic certificate has an independent 158-identity replay. The rational
clipped-supremum statement respects empty strict branches and unattained
limits. It gives no finite continuous shape cover and no new width bound.
A separate review proves exact section interpolation within each band and
identifies its possible one transition between the two contact planes.

The eight-variable parameterization and linear-fiber formulation are recorded
as structural progress. Standard barycentric algebra, rank-one determinant
identities, projective linearization and the established ACMS/observer results
are the antecedents; mathematical priority is unconfirmed. No new CLAIM number,
complete class exclusion or global improvement is asserted. All 58 necessary
types and the 258-entry residual queue remain. The next scientific step is
exact fiber elimination plus a rigorous argument over all six shape variables.

## 2026-09-14 — quantitative height bands, bounded shape coordinates and checked rectangle

CLAIM-0010 gives w(K)<(500/317)(1+2/sqrt(3))<17/5 in two closed
height bands of the prescribed determinant-five Y[0,3] facet-contact chart.
Two necessary observer exclusions prove the gauge estimates analytically;
no prior large-width or volume assumption is used in this claim. Independent
symbolic and exact fixture checks support the written universal argument.
Six compact shape coordinates are bounded, with their rational denominator
separated from zero under the true global target. Exact fixed-shape linear
fibers are implemented and independently audited, with retained weak-model
controls. This does not provide continuous six-dimensional coverage.

Two new linear queries were UNSAT: fixed heights (0,1/8), and the continuous
rectangle [0,1/256] x [31/256,33/256]. Both archived CPC proofs have fresh
reference-bound Ethos checks and independent encoding audits. The rectangle
uses the volume-derived gap bound under true global width>17/5; it cannot
inherit the stronger analytic band bound. Its area outside the old rectangles
and the analytic band is 1/32768. No new contact type or global bound is claimed.
The original nonlinear queries and prior solver archives remain unchanged.
Mathematical priority is unconfirmed. Publication now has explicit user authorization.
