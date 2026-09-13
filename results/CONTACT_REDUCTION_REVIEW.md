# Adversarial internal review of the contact reduction

Date: 2026-09-13. Scope: mathematical and computational internal review; external priority and novelty are not verified here.

## Verdict

No mathematical blocker found in the containment inequality, the planar determinant bound, the residue formula, or the ten/eleven necessary tetrahedron lists. The result is a finite necessary-condition reduction for contained empty lattice polytopes. It does not classify surrounding hollow bodies, prove realizability of each type, improve the universal flatness constant, or settle the conjecture.

The reviewed version of `tests/replay_contact_minima_independent.py` had an important verification gap: it did not read `certificates/contact_obstructions.json` at all. In a temporary repository copy, changing the first main-certificate minimum to `1/999` and deleting the final row still produced exit status zero. Thus that version could not support a claim of mutation rejection or independent replay of the main certificate. The root was informed and assigned a separate verifier repair. Any later repaired verifier needs its own mutation checks; the observation here concerns the inspected version.

## Mathematical checks

* The local primary-source text of ACMS Lemma 5.1 states its inequality for any hollow convex body in dimension three. Using containment monotonicity in the stated direction gives `1 <= A/w(K) + ell(P)` without maximality or special facet contacts.
* For two vertices in each width-one layer, the height-zero section of the difference body is exactly the union of `(1-t)[-u,u]+t[-s,s]`, hence `conv(±u,±s)`. Its planar lattice area is `2N`. Minkowski's first theorem with a limiting enlargement gives `N ell^2 <= 2`. The three-plus-one layer split is unimodular by Pick's theorem.
* Strict thresholds are handled correctly: `w>3A/2` forces `ell>1/3` and `N<=17`; `w>11A/7` forces `ell>4/11` and `N<=15`. The row `(11,3,4/11)` cannot be removed at equality from this inequality alone. The candidate-width comparison leaves the same ten rows. The tetrahedron determinant is at most 13 only after the finite row elimination.
* The residue proof correctly retains all four affine difference coefficients, whose residues form complementary pairs. Minimizing their positive sum gives the stated circular-distance formula. The zero residue contributes minimum one. The unimodular case is handled separately.
* HNF enumeration ranges match the transpose of column HNF, enumerate every ordered ambient unimodular orbit, and quotient all 24 anchor/order choices. Closed emptiness tests are valid on the nonnegative positive-determinant HNFs actually passed to them. Those helpers should not be interpreted as general signed-matrix emptiness routines.

## Reproduced checks

1. `python3 tests/replay_contact_minima_independent.py` passed the 37-row and 51-row exact replays.
2. An independent standard-library Fraction implementation directly read all 51 main-certificate rows and replayed every primitive vector in their complete difference-coordinate boxes. All first minima, complete primitive minimizer sets, bounds, checked-vector counts, source-row links, and rational-threshold flags agreed.
3. `.venv/bin/python` regeneration with `enumeration.empty_tetrahedra.run(21)` exactly equaled the stored source JSON: 6385 ordered HNF candidates, 359 ordered empty HNFs, and 51 affine unimodular classes.
4. The temporary-copy mutation experiment above demonstrated the old replay gap without changing repository certificates.

The independent full-box check supports the actual stored minima, but is not a substitute for checking every serialized witness and summary field in a durable verifier. Enumeration regeneration uses the implementation being reviewed; its completeness is supported separately by the HNF argument, not by regeneration alone.

## Additional extension review

The inspected `enumeration/contact_extensions.py` and `src/width_one_minimum.py` have consistent mathematical logic:

* Howe's width-one theorem gives a unimodular tetrahedron inside every empty three-dimensional lattice polytope with at least five vertices: three vertices share a layer, form an empty unimodular triangle, and a vertex in the other layer completes the frame.
* Relative to that frame, determinants bound all three extra coordinates and `1-sum(q)` by 13. Every possible width-one direction is among the seven nonzero binary vectors after sign normalization, since the frame contains `0,e1,e2,e3`.
* Canonicalization over all unimodular ordered frames is a complete affine unimodular invariant for these finite sets and always leaves the standard frame present. Successive insertion therefore has an exhaustive path to every admissible set.
* Primitive triangle tests together with allowed nondegenerate tetrahedron tests ensure closed emptiness by Carathéodory's theorem. They also exclude nonextreme supplied points: such a point would be an extra lattice point in the convex hull of at most four others. Every true empty polytope passes these tests.
* The stopping bound of eight vertices requires the usual parity argument: two of nine lattice vertices have equal residue modulo two, giving a nonvertex lattice midpoint. This should be explicit in the final proof.
* The generalized height-zero section is `conv(P0-P0,P1-P1)`. Deleting a coordinate whose height coefficient is one gives a unimodular chart of the planar lattice. At scales below one there are no nonzero-height lattice vectors. The section search and its full lattice minimum are therefore valid; its scope correctly warns that nonplanar minimizers at value one are not listed.

An independent exact supporting-plane and complete integer-box check verified that all 52 stored extension sets are closed-empty and every listed point is extreme. Their counts are 11, 22, 10, 9 for five through eight vertices. This review inspected the exhaustion logic but did not independently regenerate the whole extension search or replay every generalized-minimum payload field.

Adding these 52 possibilities to the ten tetrahedra and the planar square gives 63 necessary contact-hull possibilities, conditional on the applicable contact selection assumptions. This is not a classification of 63 hollow bodies. No external novelty claim is approved by this review. The natural ingredients and finite nature of the calculation make a careful literature comparison necessary before describing the bound or list as new.

## Addendum: global statement and maximal extensions

The subsequently drafted `proofs/CONTACT_HULL_FINITE_REDUCTION.md` and `claims/CLAIM-0004.md` were reviewed as well. No new mathematical blocker was found in extending the necessary list to arbitrary compact full-dimensional hollow K of width greater than c.

The Zorn argument is valid: the closure of a chain union is convex, and an interior lattice point can be enclosed by a sufficiently small simplex whose approximated vertices belong to the union. Finitely many vertices then lie in one chain member, contradicting its hollowness. A maximal member containing full-dimensional K is full-dimensional.

The rational-lineality quotient argument correctly excludes unbounded maximal extensions at this width. A lattice splitting identifies such an extension with a lower-dimensional hollow quotient times its lineality space. Finite integer width directions are exactly quotient directions. Its width is therefore bounded by the planar flatness constant A (or by one in quotient dimension one), contradicting width monotonicity. This uses the full recession-space conclusion of Lovasz's theorem, not merely the existence of an unbounded ray.

For any blocker choice in distinct relative facet interiors, the facet inequalities expose each chosen blocker uniquely. Every convex combination using at least two blockers satisfies every facet inequality strictly. Thus the chosen hull is closed-empty, has exactly one vertex per facet, and its size satisfies the parity bound. This reasoning supports the stated universal quantifier over blocker choices, not merely existence of a favorable choice.

The planar square conclusion is also correct. For an explicit short justification beyond Pick's theorem: choose a diagonal and normalize one adjacent unimodular triangle. With diagonal endpoints 0 and e1, the other two vertices have coordinates (a,1) and (b,-1). Convexity puts the diagonal crossing at (a+b)/2 strictly between 0 and 1, forcing the integer a+b to equal one. The quadrilateral is a unimodular parallelogram.

One citation issue was reported to the root: in [Averkov, arXiv:1110.1014](https://arxiv.org/html/1110.1014), Theorem 1 supplies polyhedrality, rational linear recession space, and facet blockers. Lemma 7 is the parity lemma; it is not a maximal-extension existence theorem. The draft's attribution should distinguish these facts and use its own Zorn paragraph for existence. This is a citation correction, not a failure of the supplied existence proof.

The proof now explicitly contains the parity stopping argument and Caratheodory justification requested in the initial review. The global 63-type claim remains a necessary contact-hull reduction with continuous optimization and external novelty assessment outstanding. This addendum does not assert a completed independent audit of the repaired certificate verifier.

## Repair closure and nine-template corollary

The repaired `tests/replay_contact_minima_independent.py` now has a live `main()` that explicitly loads the main tetrahedron, extension, full-hull-minimum, and template certificates. It retains the historical replay, then validates the new payloads and runs mutation guards by default. The previous dead-payload validation gap is closed.

I repeated the original adversarial test through the actual script entrypoint in a temporary repository copy. Changing the first main minimum to `1/999` was rejected with `ValidationError: minimum certificate mismatch at 0`. Deleting the last main row was rejected with `ValidationError: main cases list length changed`. Combining both changes was also rejected. All three runs returned nonzero status; repository artifacts were untouched.

Code inspection confirms that the repaired verifier reconstructs the entire main minimum certificate, including minimizing directions, barycentric upper witness, coordinate bounds, and counts; checks exact radical bounds and survivor metadata; reconstructs the full planar section certificates for all supplied hulls; validates closed emptiness and canonical uniqueness; and checks every four-subset. The stored validation report records 51 main cases, 52 hulls, 1365 four-subsets, nine templates, 63 maps, and 21 successful mutation guards. This final bounded review inspected those paths and reran the original failures, rather than repeating the whole costly pipeline. The root retains responsibility for the final pipeline execution.

The repaired report appropriately distinguishes certificate validation from an independent reimplementation of exhaustive generation. The 52-class exhaustion still rests on the reviewed finite-search proof and generator workflow; fixed expected counts and checks of supplied classes alone are not an independent exhaustion proof.

The nine-template corollary is sound in the written scope. I separately checked that the nine template vertex sets are exactly the stored eight-vertex hulls and replayed all 63 integer affine maps directly. Every matrix had determinant plus or minus one, and every selected subset mapped exactly onto its required target from the ten tetrahedra, 52 larger hulls, and explicit square. Inverting these maps places any necessary contact set into one of the nine templates. It does not place unselected template vertices inside the surrounding maximal hollow body. The written proof explicitly preserves this distinction.

No additional mathematical blocker was found. This closes the original main-payload replay objection while preserving the separate limits concerning exhaustive-search independence, external novelty, and continuous optimization.

Final integration evidence reported by the root: `reproduce_contact_reduction.py` completed all eight stages successfully, including all 21 mutation guards; the pipeline report is `results/contact_reduction_replay.json`. A subsequent guard rejects Python `-O`/`-OO` so historical assertions cannot silently disappear; the root tested that rejection. The historical determinant-one coordinate convention is now explicit and checked, with unchanged minima. With this integration evidence, the original repair objection is closed. External novelty and the surviving continuous problems remain open.
