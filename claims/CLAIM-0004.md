# CLAIM-0004 — Explicit necessary contact configurations (POSSIBLY NOVEL)

- **Exact statement:** For c=(11/7)(1+2/sqrt(3)), every compact full-dimensional
  hollow K in R^3 of width >c has a bounded maximal hollow extension M.
  Every hull of one relative-interior lattice blocker per facet of M is
  affinely lattice-equivalent to one of 63 explicit necessary configurations:
  one planar square, ten tetrahedra, and 11/22/10/9 empty polytopes with
  5/6/7/8 vertices. The same applies when w(K)>=2+sqrt(2). All63 contact sets
  are affinely lattice-equivalent to vertex subsets of nine eight-point
  templates, with explicit integer embedding certificates.
- **Class of bodies:** All compact full-dimensional hollow convex 3-bodies,
  through bounded inclusion-maximal extensions. Not just integral bodies.
- **Normalization:** Ambient Z^3, Euclidean fundamental volume one, N=6vol(T).
- **Threshold:** Strict >c; the higher Codenotti--Santos threshold is inclusive.
- **Geometric assumptions:** Real facets allowed. Boundary lattice points
  allowed. Choose blockers from distinct relative facet interiors.
- **Lattice assumptions:** Affine GL3(Z) equivalence; closed emptiness of hull.
- **Exact certificate:** certificates/contact_obstructions.json,
  certificates/contact_hull_obstructions.json, results/contact_extensions.json,
  certificates/contact_templates.json.
- **Continuous-to-finite reduction:** ACMS containment inequality; planar
  section N lambda_1(T-T)^2<=2; exact ten-tetrahedron table; larger contact hulls
  contain a unimodular frame; four determinant bounds give coordinate box13;
  exhaustive vertex extension and complete unimodular-frame quotient.
- **Independent implementation:** tests/replay_contact_minima_independent.py;
  results/CONTACT_REDUCTION_REVIEW.md records separate rational checks.
  Validator repairs are complete; all 21 deliberate mutations are rejected.
- **Counterexample search:** Seven non-unimodular tetrahedral contact orbits,
  84 recorded numerical rows, best numeric hollow width about3.05298; bounded
  exploration only. Square chart has an exact balanced subclass of width<=2,
  leaving asymmetric square realizations open.
- **Closest prior work:** ACMS arXiv:1907.06199, Lemma5.1 and Theorem5.4;
  White/Howe empty-polytope width one; Lovasz blocked-facet characterization.
- **2025–2026 novelty audit:** proofs/CONTACT_MINIMA_LITERATURE.md and
  proofs/CONTACT_HULL_NOVELTY_AUDIT.md supply bounded negative evidence for
  the refinement and complete list. External priority remains unverified.
- **Proof level:** Level 5 under this lab's internal protocol: complete written
  argument, exact enumeration, independent implementation and Astra
  adversarial review. This is not formal proof-assistant verification or
  external peer review. Eight-stage reproduction passes in about 33 seconds.
- **Open objections:** External novelty not established; 63 are necessary hull
  possibilities, not realized high-width bodies; continuous optimization of
  every surviving type remains open; no improvement to global Flt(3) asserted.

Proofs: proofs/CONTACT_OBSTRUCTION_REDUCTION.md and
proofs/CONTACT_HULL_FINITE_REDUCTION.md.

## Subsequent analytic refinement

[CLAIM-0006](CLAIM-0006.md) excludes the full determinant-13 tetrahedral
contact hull above the threshold of this claim, reducing the necessary list
to 62. At width at least 2+sqrt(2), the full determinant-10 tetrahedral hull
is also excluded, leaving 61. The original 63-type certificate remains a
valid necessary superset; no larger hull is deleted merely because it
contains one of those tetrahedral subsets.

## Subsequent height-cover exclusions (2026-09-14)

[CLAIM-0007](CLAIM-0007.md) excludes full tetrahedral contact classes6 and7
above width17/5, using a complete rational interval cover with independently
encoded and externally checked linear refutations. Together with CLAIM-0006,
this leaves59 necessary full hulls at width at least2+sqrt(2). The original
63-class list remains a valid superset and its certificate is unchanged.
The list above the original threshold c still has62 members. No larger
hull is removed merely for containing an excluded tetrahedral subset.
