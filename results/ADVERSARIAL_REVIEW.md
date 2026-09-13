# Adversarial scientific and code review

Review date: 2026-09-13. This is a bounded review of the checked-in research lab, not an endorsement of novelty or a proof of the global three-dimensional flatness conjecture. No network publication was performed.

## Verified mathematical core

- The affine lattice conversion is correct: the three contact differences form a determinant-16 basis of the stated odd-coordinate congruence lattice. Applying its inverse gives the standard integer lattice. Width and volume are then evaluated in the correct lattice; Euclidean volume and normalized determinant are distinguished.
- The complete-width exclusion is valid for full-dimensional supported V-polytopes: with rows of D equal to independent vertex differences, width at most W implies |Du| componentwise at most W, hence |u_j| <= W sum_i |(D^-1)_ji|. Exact floors and enumeration including equality recover all minimizing directions modulo sign. The cap raises rather than returning a partial result.
- Exact facet enumeration and the integer coordinate-extrema box give a complete hollowness test on the stated domain. Boundary contacts are allowed; relative-interior facet contacts are tested separately. Irrational facet normals are supported. The exact engine is limited to Q, Q(sqrt(2)), Q(sqrt(3)), dimensions 2 and 3, and practical work caps; volume supports simplices only.
- Independent SymPy baseline replay passed: width 2+sqrt(2), 21 primitive direction representatives in bounds [1,2,1], seven minima, all 27 integer candidates checked, no interior points, four boundary contacts, and exactly four integral unimodular affine automorphisms among all 24 vertex permutations. This independently supports the symmetry order four, without treating every visual symmetry as a lattice symmetry.
- The HNF search was rerun into /tmp/reviewer-empty.json: 3268 ordered candidates, 239 empty candidates, 37 unlabeled classes through determinant 17. As an additional independent test, closed lattice-point sets for ALL 3268 candidates agreed with a separate triangular solve using Python Fraction arithmetic, including rejected candidates. Transpose-column HNF is the correct left-GL convention; the 24 anchor/order minimum supplies the unordered orbit key.
- The radical upper-bound replay passed. Its rational interval arithmetic supports the printed numerical consequences of the cited geometric inequalities. The width upper bound applies universally under those inputs; the stated volume window requires width at least 2+sqrt(2). The external covering-minima, Mahler, Minkowski, and other geometric theorems are inputs, not established by the script.
- The original nine pytest tests passed; all ten tests in the strengthened suite passed after review fixes. All eight discovery certificates were recomputed from their exact stored vertices using the project engine; width and hollow payloads matched. This last check is same-engine reproducibility, not an independent arithmetic implementation.

## Findings and limits

### Repaired: incomplete certificate-field verification

An adversarial in-memory mutation was initially accepted by tests/independent_replay.py: simultaneously set the upper witness direction to [0,0,0], D_inverse to [], initial_upper to zero, lower checked_minimum to 999, and hollow facets to []. The root repaired the verifier to reconstruct and validate upper/lower witnesses, inverse, initial bound, basis, statuses, facet equations, and relative-interior contact metadata, and added six mutation cases. The review's combined forged payload is now rejected. The mathematical baseline conclusions were already independently recomputed before this fix. The replay remains baseline-specific, not a general-purpose verifier for all discovery or classification certificates, and Python assertions require running without -O.

### Repaired: optional canonicalization contacts were trusted input

The default canonicalize(K) computes the complete boundary-contact set and its contact-frame invariant is sound on the supported domain. Initially, the optional contacts argument checked only integrality, dimension and count. Supplying an arbitrary standard contact frame to a translated/sheared equivalent body broke invariance while returning complete status. The root repaired this by requiring supplied contacts to equal the entire recomputed boundary lattice-point set. The review's forged contact example now raises ValueError. Non-unimodular contact configurations remain explicitly unsupported by this canonicalizer; their HNF contact-tetrahedron classification is a separate computation.

### Numerical discovery is not a global argument

The floating search uses finitely many directions, an interior tolerance, bounded coordinates, restricted contact families, and correlated optimization iterates. Reported numerical widths are upper estimates. The rationalization stage changes the body: it reconstructs exact contact barycentrics or rational supporting planes and then certifies the resulting V-polytope. It does not transfer a theorem to the original floating body or prove an error bound between bodies. No certified counterexample is found among the eight selected exact reconstructions; this says nothing about unsearched bodies or even every recorded numerical row.

### Scope of classification and truncation

The determinant-17 list covers empty lattice tetrahedra, not maximal real lattice-free bodies. Square and nonsimplicial contact branches and optimization for each fixed contact configuration remain unresolved. Maximality in the real convex-set sense cannot be replaced by integral maximality. The truncation argument is valid: arbitrarily small cuts of the known tetrahedron produce nonmaximal nontetrahedral hollow bodies with width arbitrarily near 2+sqrt(2). Therefore a subextremal width threshold cannot force every hollow body to be a tetrahedron. This does not refute a claim about maximal extensions or global maximizers.

### Textual issues reported for integration

The maximal-reduction note initially described the quantifier-elimination target as every body having width *at least* the conjectured value; an upper-bound argument needs *at most* and the hollow-body qualification. The local Hessian chart initially differed between proof and code in the t12 sign of t13, and its printed-paper comparison assertions were still being revised during review. These were reported to the owning agents. Enumeration notes initially contained malformed TeX escapes. The maximal-reduction target and enumeration TeX were checked corrected in the final integrated files. Local Hessian status is recorded below.

## Local Hessian review

The corrected experiments/replay_local_hessian.py was run successfully by this reviewer. It reconstructs the six cubic polynomials, rank-five gradients, their positive dependence, the three-dimensional common kernel, and a negative-definite full auxiliary Hessian at c=1/100. It verifies both direct differentiation and the product-rule Hessian formula. Exact Sylvester signs supply the definiteness test; no floating eigenvalue threshold is used. All six stored h_i(0) values are zero.

The t13 outer minus was independently checked from the raw facet cross product: t13=-(2+sqrt(2))*t11/2-sqrt(2)*t12/2. The corrected proof and script agree. The printed kernel comparison now simplifies algebraic entries before testing zero. The direct restricted Hessian equals 16 times the paper's displayed matrix, and this positive scale is explicitly recorded rather than silently claiming equality. It leaves definiteness unchanged. The final assertions check the gradient, kernel and scaled-Hessian comparisons.

This supplies the qualitative local algebraic isolation step, conditional on the geometric chart/reduction explained in the proof note. It does not reproduce the degree-16 coefficient-majorant calculation for the published numerical radius, provide a certified Hausdorff neighborhood, or establish a global theorem. The stale sentence calling the Hessian step missing was corrected by the owner after review; the final script also asserts all h_i(0)=0.

## Verdict

The baseline exact witness, complete width/hollow algorithm on its stated domain, finite empty-tetrahedron list, and upper-bound arithmetic have passed the checks above. They do not settle Flt(3), classify all high-width maximal bodies, or establish a new global theorem. The two concrete API/certificate defects found during review were repaired and adversarially retested; the remaining scientific scope limits still apply.
