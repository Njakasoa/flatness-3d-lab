# CLAIM-0009 — conditional bounds on a determinant-five height corner

Date: 2026-09-14. Status: exact computer-assisted conditional result, with
independent input/arithmetic review and reference-bound Ethos checks.
Novelty remains unconfirmed. The determinant-five class is still open.

## Exact statement, class and normalization

Let K=conv(v0,v1,v2,v3) be a compact full-dimensional hollow real tetrahedron
in R³ with respect to Z³. Require the ordered points

    p0=(0,0,0), p1=(5,1,2), p2=(0,1,0), p3=(0,0,1)

to lie in the relative interiors of the facets opposite v0,v1,v2,v3,
respectively. In the normalized lattice coordinates above, put Y=(0,1,0),
q_i=(Y(v_i)-min_j Y(v_j))/w(K,Y), and A=1+2/sqrt(3).
Assume q0=0 and q3=1. Then:

| Additional actual-height hypothesis | Full lattice-width bound |
|---|---|
| q1,q2 in [3/5,1] | w(K)<=(102/65)A, approximately 3.3812223833 |
| q1,q2 in [3/4,1] | w(K)<=(23/19)A, approximately 2.6083217044 |

All interval endpoints are included. The bounds concern full lattice width;
Y need not minimize it. The specified contact ordering and height conditions
are substantive. No assertion covers all determinant-five tetrahedra,
arbitrary containing polytopes or other extrema charts. No whole contact
class is removed; the 58-type necessary list at width 2+sqrt(2) is unchanged.

## Continuous-to-finite argument and exact certificate

The [original supplementary proof](../proofs/DET5_Y_CORNER_SHARP_SUPPLEMENT.md)
uses column-stochastic facet barycentrics F, six exact height products and
McCormick outer envelopes over each entire closed rectangle. Hollowness
implies the finite guard necessities, independently of any sufficiency
threshold. The original inputs also contained b=1/w(K,Y)<5/17.

The [checked dependency slices](../proofs/DET5_CORNER_PROOF_SLICES.md)
remove that auxiliary upper bound in all three refutations. Their actual
60-,49-,51-assumption inputs have separate reference-bound Ethos checks.
On [3/5,1]^2, the slice uses only four lattice gauges, at (1,0,0),(1,0,1),
(2,0,1),(3,0,1), all with strict lower bound 37/102. If an actual hollow K
satisfied all four lower bounds, its exact heights and products would satisfy
the checked subset. The contradiction proves lambda1(K-K)<=37/102 without
assuming a large Y-width or global width. ACMS Lemma 5.1 now gives the first
row on the entire square. The old restriction of this stronger conclusion
to [12/17,1]^2 is superseded. The 4/23 slice gives the second row in the same
way, with six retained gauges. No volume premise is used.

All rectangle hypotheses remain substantive: their endpoints occur inside
the retained product envelopes, even where an explicit height bound is unused.
Strict facet positivity and strict refuted gauge bounds justify the closed
height-domain endpoints and the non-strict width conclusions. Since
11/7-102/65=1/455, the first bound is below the initial contact-reduction
threshold (11/7)A. This does not change the target of the other archived
joint-domain exclusions, which remains 17/5.

The quantitative 4/23 threshold was suggested by a strict linear optimization;
its reported optimum is not part of the proof. The independent fixed-threshold
CPC refutation supplies the required upper-bound evidence. No optimality of
4/23 for actual bodies or of these width bounds is claimed.

## Independent implementation and falsification

The [standard-library supplement audit](../tests/replay_det5_y_corner_supplement.py)
reconstructs the complete 22-variable inputs from independent rational
barycentrics and binds the three original UNSAT inputs and proof receipts. The separate
slice extractor verifies their reduced premises and preserves the original
statements and CPC payloads.
It also checks the saved [11/20,1]^2 SAT assignment exactly; all six products
fail their required exact product identities, so it is not a body witness.
The older [1/2,1]^2 outer formula was already SAT and was not rerun.
Neither SAT relaxation proves sharpness or feasibility of an actual body.

The new [3/5,1]^2 square contains genuinely new excluded Y-region area 3/40
outside the twelve old rectangles. This is coordinate area in this one chart,
not an invariant fraction of all tetrahedra. The exact residual-domain queue
preserves strict complements and all original U bounds; historical joint
UNSAT labels are not silently promoted to checked proofs.

## Reproduction and proof level

```sh
python3 tests/replay_det5_y_corner_supplement.py
python3 tests/check_det5_y_corner_supplement_ethos.py \
  --ethos ETHOS/build/src/ethos --ethos-source ETHOS --cvc5-source CVC5
```

The first command checks formulas, rational arithmetic, saved SAT values and
archived evidence bindings without a solver or kernel call. The second runs
the external kernel against the three original stored refutations and rejects an unrelated
assumption, with zero SMT queries. See the pinned
[checker setup and trust boundary](../proofs/HEIGHT_ETHOS_REPRODUCTION.md).
The reduced-assumption proof replay is:

```sh
python3 -m experiments.det5_corner_proof_slice \
  --ethos ETHOS/build/src/ethos --ethos-source ETHOS --cvc5-source CVC5
```

Its [receipt](../results/det5_corner_proof_slice.json) binds all three actual
subset statements and successful kernel checks. The original
[Input audit](../results/det5_y_corner_supplement_validation.json) and
[kernel replay](../results/det5_y_corner_supplement_ethos_validation.json)
record their different scopes. Geometry-to-formula implications are written
arguments with independent internal review, not formalized inside Ethos.
Under the lab protocol this is Level 5 for the stated restricted theorem;
external human review and mathematical priority are unresolved.

## Closest prior work, recency audit and open objections

ACMS's difference-minimum inequality and contact programme, and established
McCormick methods, are the main antecedents. The
[bounded 2025–2026 priority audit](../proofs/DET5_HEIGHT_DOMAIN_LITERATURE.md)
records the primary sources and search limitations. No first-proof or
best-known claim is made. The unresolved issues are global chart coverage,
other contact types, sharpness, independent human review and priority.
The outer coupled fifteen-width models remain UNKNOWN and are not evidence
for a whole-class theorem. The full flatness research goal remains open.
