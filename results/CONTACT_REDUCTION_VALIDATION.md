# Contact-reduction validation receipt

Date: 2026-09-13. Scientific scope: CLAIM-0004, the necessary 63 contact-hull
types above c=(11/7)(1+2/sqrt(3)), with nine-template compression. Internal
verification does not establish external novelty or solve the continuous
optimization of a surviving contact type.

## Reproduction

`.venv/bin/python reproduce_contact_reduction.py` passed all eight stages,
in about 33 seconds on the recorded local environment:

1. Complete determinant-21 HNF enumeration: 6385 ordered matrices, 359 empty
   ordered matrices, 51 affine lattice classes.
2. Exact tetrahedron difference minima and threshold elimination.
3. Exact vertex extension:11/22/10/9 classes with 5/6/7/8 vertices.
4. Exact full difference minima of the 52 extension hulls.
5. Exact lattice embeddings of all 63 configurations into 9 templates.
6. Independent standard-library certificate replay and 21 mutation guards.
7. Exact square-chart and balanced-subfamily controls.
8. Scientific figures derived from the integer data.

The pipeline logs and return codes are in contact_reduction_replay.json.
The new standalone verifier and pipeline reject Python -O/-OO; assertions
must remain enabled. The existing 10 unit tests also pass.

## Independent coverage

tests/replay_contact_minima_independent.py imports none of the root geometry,
exact-arithmetic or enumeration modules. It checks the historical 37-class
minima, the 51 main certificate payloads, all 52 hulls, all 1,365 four-point
subsets, nine templates and 63 affine embeddings. Coverage includes complete
primitive minimizer sets, bounds/counts, rational witnesses, exact quadratic
width bounds and threshold flags, emptiness, extremality, canonical uniqueness,
and determinant+/-1 integer maps. Radical intervals are checked by squaring.

It rejects 21 intentional corruptions including altered minima, missing rows,
missing minimizers, forged HNFs/counts, altered width bounds, duplicate/altered
hulls, invalid template indices and non-unimodular maps. Detailed results
are in contact_reduction_validation.json.

The independent verifier checks every supplied hull; the mathematical
completeness of the list comes from the proved determinant box, exhaustive
generator and canonicalization argument. It is not inferred from checking
52 examples. The Astra reviewer independently regenerated the 51 tetrahedron
classes, checked the 52 larger hulls using supporting planes and full integer
boxes, and reviewed the global maximal-extension/completeness argument.

## Repaired defect and review closure

The initial independent replay never loaded the root's main certificate.
The reviewer demonstrated that altering a minimum and deleting a row passed
that version. The repaired entrypoint rejects both mutations, separately
and together. The reviewer repeated those entrypoint checks and separately
verified all 63 template maps. See CONTACT_REDUCTION_REVIEW.md.

The older 37-class auxiliary certificate uses a sheared unimodular chart for
N=1; its witness coordinates are explicitly interpreted and checked in that
chart. The main 51-class certificate uses the actual source representatives.

Some generated JSON status strings retain their conservative candidate labels;
this receipt and the completed review record the subsequent internal checks.
No external mathematical priority, peer review, global flatness improvement,
or realizability of all 63 types is claimed.
