# CLAIM-0001 — Exact baseline reproduction (KNOWN)

- **Exact statement:** The explicit standard-lattice tetrahedron in
  certificates/codenotti_santos.json is hollow and has lattice width
  2+sqrt(2), exactly the seven antipodal direction classes listed there,
  volume 2+4sqrt(2)/3, and four affine lattice automorphisms.
- **Class of bodies:** One full-dimensional algebraic tetrahedron.
- **Normalization:** Standard Z^3 after the explicit affine lattice bijection.
- **Threshold:** Exact equality 2+sqrt(2).
- **Geometric assumptions:** Convex hull of the four exact vertices; positive determinant.
- **Lattice assumptions:** Boundary contacts permitted; affine automorphisms integral with determinant +-1.
- **Exact certificate:** certificates/codenotti_santos.json.
- **Continuous-to-finite reduction:** Inverse edge-difference box (1,2,1), 21 primitive directions modulo sign; integer point box {-1,0,1}^3; all 24 vertex permutations for automorphisms.
- **Independent implementation:** tests/independent_replay.py, SymPy without src imports; checks exported mathematical data and rejects corrupted fields.
- **Counterexample search:** Deliberate missing direction, altered width, zero witness, bad inverse, bad lower bound, missing facets, wrong status, nonhollow dilation and nonunimodular transformation checks.
- **Closest prior work:** Codenotti–Santos arXiv:1812.00916; ACMS arXiv:1907.06199.
- **2025–2026 novelty audit:** STATE_OF_THE_ART.md and references/LITERATURE_SEARCH.md; result explicitly known.
- **Proof level:** Exact finite computation with mathematical completeness argument and independent implementation; level 5 only together with the completed Astra review in results/ADVERSARIAL_REVIEW.md.
- **Open objections:** No assertion that this is the global optimum. External theorem status and code review are not formal proof-assistant verification.
