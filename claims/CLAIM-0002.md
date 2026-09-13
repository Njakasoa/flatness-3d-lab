# CLAIM-0002 — Bounded empty contact-tetrahedron enumeration (KNOWN framework)

- **Exact statement:** Empty lattice tetrahedra of determinant at most 17 have 37 affine-unimodular classes in the executed HNF enumeration.
- **Class of bodies:** Integer contact tetrahedra, not the surrounding real hollow bodies.
- **Normalization:** N=6 Euclidean volume in Z^3.
- **Threshold:** Integer N<=17.
- **Geometric assumptions:** Full-dimensional tetrahedron with no other lattice points anywhere in its closed hull.
- **Lattice assumptions:** Equivalence under GL(3,Z), integer translation, arbitrary vertex labeling.
- **Exact certificate:** results/empty_contact_tetrahedra.json; every representative included.
- **Continuous-to-finite reduction:** None needed for integer tetrahedra; complete row-HNF ranges and all 24 vertex orders prove exhaustion of this discrete domain. ACMS Theorem 5.4 supplies relevance only to its global-maximizer contact branch.
- **Independent implementation:** Exact inverse recheck and independent Fraction triangular solve by Astra reviewer on all 3268 candidate point sets.
- **Counterexample search:** All closed lattice points are checked, including boundary; counts and canonical keys replayed.
- **Closest prior work:** ACMS Theorem 5.4; classical HNF and empty-tetrahedron classification.
- **2025–2026 novelty audit:** No novelty asserted for enumeration counts or the known bound. Literature audit records sources and limitations.
- **Proof level:** Exact exhaustive implemented enumeration in the stated domain, independently reviewed. The ACMS input theorem is cited, not reproved from first principles here.
- **Open objections:** Square contact branch, nonsimplicial contact hulls and all continuous facet optimization remain unresolved. This does not imply a new bound on Flt(3).
