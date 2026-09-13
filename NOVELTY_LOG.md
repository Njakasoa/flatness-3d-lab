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
the reproducible baseline, completed in the curated public checkout. New
research remains local while proof and novelty reviews are completed; no
external peer review or journal/arXiv submission has occurred.

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
reformulation, not a new width theorem, and its solver implementation was subsequently completed in the observer update. The two additional eight-variable queries returned UNKNOWN.


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
