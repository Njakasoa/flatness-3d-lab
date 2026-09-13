# Independent adversarial review of the determinant-two four-contact witness

Reviewed 2026-09-13. Scope: `proofs/DET2_FOUR_CONTACT_OBSTRUCTION.md`, `certificates/det2_four_contacts.json`, and `tests/replay_det2_cycle_independent.py`. This was a bounded mathematical and validator review, without external novelty research or replay of unrelated pipelines. Only this review file was written.

## Verdict

The supplied exact witness supports the stated obstruction. No mathematical defect was found in its width, hollowness, exact contact set, maximality, or unspecified open-neighborhood claim. It supplies no local/global optimum theorem and no novelty conclusion, consistently with the note.

## Exact evidence

The independent standard-library Fraction validator was loaded using `runpy` and applied directly to the four-contact JSON. Both ordinary and optimized (`python3 -O`) replay passed. The certificate has:

- Width `4009295246418/1232189371865`, with positive margin `18719151427/4928757487460` over `13/4`.
- Unique primitive minimizing direction `(1,-1,-1)` modulo sign.
- Complete width coordinate bounds `(2,3,2)`, with 73 primitive representatives.
- All 48 possible lattice points enumerated; no interior points and boundary set exactly `{(0,0,0),(2,1,1),(0,1,0),(0,0,1)}`.
- Absolute determinant two for the three nonzero designated contact vectors.

The independent replay reconstructs the chart matrix from the parameters, inverts it, checks positive inverse column sums, reconstructs all vertices, checks full dimension, derives supporting facets independently, exhausts the integer bounding box, and recomputes the complete finite width search. Stored facet planes are checked up to positive proportionality, including their full contact and relative-interior contact lists. Thus the serialized width and contact lists are not trusted assertions.

The built-in vertex, width-value, and boundary-deletion mutations were rejected. Additional mutations to a stored inverse entry, a width coordinate bound, a facet offset, a relative-interior contact list, and the minimizer list were all rejected, including under optimized Python.

## Mathematical scope and logic

Positive off-diagonal matrix entries put each designated contact strictly inside the other three facet halfspaces. Invertibility and positive inverse column sums identify the feasible barycentric region with a genuine bounded simplex, so each contact is in the relative interior of its designated facet. The independent plane check agrees.

Maximality holds among full-dimensional convex hollow extensions: any point added outside the tetrahedron violates a facet inequality. A small relative-open patch of that facet around its lattice contact, together with the original inward body and the added outward point, puts that lattice contact in the interior of the convex hull. This contradicts hollowness. The proof does not merely establish maximality inside the tetrahedron chart.

The openness argument is valid. Every coordinate extremum of the exact vertices is nonintegral, so continuity of vertices preserves the same finite set of possible integer points in a sufficiently small neighborhood. Each of the 44 noncontact candidates has a strictly violated facet inequality; finitely many such strict exclusions persist simultaneously. Positive off-diagonal entries keep the four contacts in their facet relative interiors. Invertibility and positive inverse column sums persist as well.

For width continuity, a fixed positive-radius ball inside all nearby bodies bounds directional width below by a constant times the norm of the integer direction. A fixed coordinate direction supplies a uniform upper bound on the minimum. Only finitely many integer directions can consequently minimize nearby; the minimum of their continuous directional widths is continuous. The strictly positive width margin persists. This proves existence of an open neighborhood, without an explicit radius or a claim about all parameter values.

## Validator scope caveat

At review time, `validate()` is a consistency validator for either supplied cycle certificate. It does not independently demand an empty interior list, exactly four boundary contacts, or width greater than `13/4`. A self-consistent certificate outside that particular theorem scope can therefore receive `passed`. This does not compromise the current witness: its replayed exact outputs establish all three properties, and the four-contact generator checks them. If the replay is intended as a regression gate for this specific theorem, add those assertions at the four-contact dispatch site rather than narrowing the shared validator used for the six-contact companion.

The root agent separately owns making the four-contact replay input mandatory and guarding generator assertions against optimized Python. Those changes are not implemented by this review.

## Closure after root integration

The validator scope caveat above is resolved in the current entrypoint. Reviewed `validate_claim(name, data)`: it first performs the full independent geometry replay, then requires no interior lattice points, the recorded exact width, and the exact boundary set appropriate to the named certificate. The four-contact branch additionally checks the strict `13/4` threshold. `main()` requires both certificate files and uses this wrapper. Its self-consistent companion substitution guard rejects a different witness under the four-contact claim name.

Independently executed both named claim wrappers under `python3 -O`; both passed. Substituting the valid six-contact payload under the four-contact name was rejected with `recorded witness width changed`. The generic validator remains reusable, while the entrypoint now enforces the theorem-specific claims. No outstanding material findings remain.
