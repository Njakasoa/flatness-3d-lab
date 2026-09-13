# CLAIM-0006 — two tetrahedral containment classes excluded

Status: **verified restricted width bounds**. The determinant-13 continuous
proof has an independent internal mathematical review. Its parameterized
extension gives the determinant-10 bound; both input calculations have an
independent implementation. External novelty and external peer review are
not established. The bounds are not claimed sharp.

## Exact statements and normalization

Work in the standard integer lattice, with width minimized over all nonzero
integer covectors. Let A=1+2/sqrt(3), and let K be a compact full-dimensional
hollow real tetrahedron. Then

1. If K contains an affine unimodular image of
   P13=conv(0,(13,1,5),e2,e3), then
   `w(K) <= (1+13A)/9 = (14+26/sqrt(3))/9 < 3.23`.
2. If K contains an affine unimodular image of
   P10=conv(0,(10,1,3),e2,e3), then
   `w(K) <= (1+20A)/13 = (21+40/sqrt(3))/13 < 3.4`.

The determinants 13 and 10 are six times ordinary Euclidean contact-hull
volume. The four contained points need not be boundary points or prescribed
facet contacts. The assumption that the surrounding body is a tetrahedron
is essential to the proof's four-row matching argument.

As a consequence, CLAIM-0004's list of 63 necessary full facet-contact hulls
reduces to **62 above (11/7)A** and to **61 at width at least 2+sqrt(2)**.
Only its full tetrahedral classes 9 and 8 are deleted, at their respective
thresholds. No larger contact hull is removed merely because it contains a
tetrahedral subset of determinant 10 or 13. The square remains unresolved.

## Proof and continuous-to-finite reasoning

[Detailed determinant-13 proof](../proofs/DET13_CONTRACTION_BOUND.md).
[Parameterized theorem and determinant-10 application](../proofs/TWO_VECTOR_CONTRACTION.md).

For the barycentric matrix F of the contained configuration in K, two short
lattice vectors produce four distinct column sign pairs. Their gauge losses
bound the total matrix mass assigned to a different sign pair. If that mass
is less than one, every input pair must occur on an output row. Four rows
then give a permutation, and total off-permutation mass controls the inverse
oscillation in a width-one lattice direction. The ACMS lower bound on every
lattice gauge closes the resulting scalar width inequality.

This is a continuous analytic argument. It does not infer emptiness or a
width bound from a finite numerical search. The proof supplies an explicit
integer covector bounding width from above; it needs no exhaustive width
search for K. Non-strict endpoints and the low-width case split are explicit.

## Certificates, independent checks and adversarial controls

- [Determinant-13 certificate](../certificates/det13_contraction.json) and
  [independent verifier](../tests/replay_det13_contraction_independent.py).
- [Exact two-vector scan](../results/two_vector_class_scan.json) and
  [independent Gaussian replay](../tests/replay_two_vector_scan_independent.py).
- [Independent mathematical review](../proofs/DET13_CONTRACTION_REVIEW.md).

The first verifier reconstructs both difference-coordinate rows, checks all
16 sign-loss coefficient cases, all 256 output-row code assignments and
192 elementary oscillation cases. It rejects 24 mutations, including an
incorrect global scope and deletion of larger hulls. Its class-index check
binds the new exclusion to the existing 63-class certificate.

The second verifier re-enumerates the eligible vectors and all 41 separating
pairs across the ten contact tetrahedra, checks exact radical comparisons,
and rejects ten mutations. It independently certifies the two displayed
input pairs. Searching a broader vector domain could improve the bounds;
no optimum of the general method is asserted.

The original argument used a weaker oscillation factor 2E. The independent
review sharpened it to E by comparing distinct columns; the written proof
includes this step directly. The verifiers run normally and under Python -O.
No bounded SMT query, numerical search or solver timeout is a premise.

## Novelty and proof level

The [bounded primary-source audit](../proofs/DET13_CONTRACTION_LITERATURE.md)
identifies ACMS Lemma 5.1 and the established stochastic/oscillation
contraction literature. Ten targeted queries found no matching index-13
containment bound, which is insufficient to establish priority. The
determinant-10 corollary needs a separate targeted priority audit.

These are written proofs with exact arithmetic and internal independent
checks, not proof-assistant formalizations or external peer review. This is
a restricted class exclusion, not an improved global bound on Flt(3).

## Remaining scientific task

At candidate width the tetrahedral branch now has eight necessary contact
types. The 52 spatial contact hulls with five to eight vertices and the
planar square remain. Seek stronger weighted gauge-loss bounds or additional
facet blockers for those surviving types; do not infer their exclusion from
the present two results. The external novelty audit and the full flatness
conjecture remain open.
