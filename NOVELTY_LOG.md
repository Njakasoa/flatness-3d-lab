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
scientific results alone. The maintainer separately authorized GitHub publication
of the baseline and this internally reviewed structural update; see
[PUBLICATION.md](PUBLICATION.md). External novelty remains unverified, and no
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
