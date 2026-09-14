> Publication note (2026-09-14): this snapshot includes the subsequent corner
> bounds, exact residual queue and ordering results below. Historical references
> to local-only work describe earlier checkpoints; see ../PUBLICATION.md.

# Determinant-five research status — 2026-09-14

## Current local refinement: exact ordering and reduced proof premises

The actual-subset checks in [the slice analysis](DET5_CORNER_PROOF_SLICES.md)
remove gap<5/17 from all three corner proofs. Thus CLAIM-0009 now gives
(102/65)A on the entire [3/5,1]^2 square, not only [12/17,1]^2. Its region
area and the residual queue are unchanged. The sharper inner bound remains
(23/19)A, with neither a volume premise nor an initial large-width premise.

The [exact contact-order lemma](DET5_Y_CORNER_ANALYTIC_PROBE.md) proves
q1≠q2, strict offset interlacing, a fixed Z-gauge sign pattern, and two
simplified guard clauses throughout Y[0,3]. Six new linear models with
successive order, offset and shared row-difference cuts are all SAT; all six
assignments fail their six exact product identities. Independent body
reconstruction finds hollow bodies with actual extrema [1,3] or [3,0], every
Y-width below 17/5. They are not actual counterexamples in the retained chart.
Two new nonlinear formulations restore all six products and remain UNKNOWN.
Their exact polynomial inputs have independent source/encoding audits.
No complete chart or further contact type is excluded by these models.


## Current local advance after public 175896f

[CLAIM-0009](../claims/CLAIM-0009.md) proves w<=17/5 on the actual Y:[0,3]
height square [3/5,1]^2, and stronger nested bounds (102/65)A on
[12/17,1]^2 and (23/19)A on [3/4,1]^2. Three new independent cvc5 refutations
have successful reference-bound Ethos checks. The broader 11/20 square has a
saved exact relaxed SAT assignment whose six product identities all fail.

The union-aware [new queue](../results/det5_enlarged_residual_queue.json)
has258 entries, including strict removal of all certified boundaries. The
new square adds 3/40 of Y-chart area and trims three entries by 3/5 of their
previous residual measure, without eliminating any whole additional box.
The old 953-query archive and all earlier proof receipts remain unchanged.

All14saved SAT assignments of the prior scaled transfer violate the new
static directional product envelopes. Nevertheless9 coupled targets and12
exhaustive Z-extrema branches are UNKNOWN under their archived time limits.
These are strictly stronger models with audited formulas, not new exclusions.
The 58-type count and unrestricted flatness bound are unchanged. See the
[supplementary proof](DET5_Y_CORNER_SHARP_SUPPLEMENT.md) and
[coupled formulation review](DET5_COUPLED_FRAME_REVIEW.md).


## Subsequent certification and corrected interpretation — 2026-09-14

The scaled box below lies in the old Y-only leaf r1111, already recorded
UNSAT. Its independent proof upgrades that label; it is not a newly discovered
excluded region. A reference-bound Ethos check of a 69-assumption dependency
slice shows that U restrictions and all additional lower-width clauses are
unused. All twelve old Y rectangles now have independently encoded cvc5
proofs checked with Ethos. The exact overlay covers one of the 259 joint
pending boxes completely and six halfway; archives are unchanged and no
clipped replacement queue is claimed.

A separate uniform-gauge refutation at beta=3/10, with no volume premise,
gives w(K)<=(10/7)(1+2/sqrt(3)) on the Y:[0,3] upper corner [3/4,1]^2.
See [conditional theorem](DET5_CONDITIONAL_WIDTH_BOUNDS.md),
[assumption audit](DET5_Y_HIGH_CYLINDER_EXCLUSION.md), and
[overlay](../results/det5_certified_y_overlay.json).
The older account below describes the formula as supplied, not the minimal
hypotheses of its proof. The 58-type count and global bound are unchanged.
The maintainer has authorized this checkpoint's GitHub publication.


The two determinant-five lattice classes are distinct. CLAIM-0008 excludes
only class 4, represented by P=conv(0,(5,1,1),e2,e3), for full relative-interior
facet-contact tetrahedra of width greater than 17/5. Class 5,
P=conv(0,(5,1,2),e2,e3), remains open.

## Exact failure of the one-direction approach

The rational witness in [det5_strong_fiber.json](../results/det5_strong_fiber.json)
is hollow and has four prescribed relative-interior facet contacts. Its Y-width
is 1290096000/376157033, approximately 3.42967, but its full lattice width is
431770127526900/160704333264053, approximately 2.68674. A minimizing direction
is U=(1,-1,-2). Its full first difference-body minimum is 14828737/40315500,
approximately 0.367817, and exceeds even the exact ACMS necessary threshold
1-(1+2/sqrt(3))/(17/5). Thus a Y-only upper-bound implication from these
hollowness/contact/gauge assumptions is false. This is not a counterexample
to the flatness conjecture.

The [independent rational checker](../tests/replay_det5_height_witness_independent.py)
reconstructs the body, enumerates a proved complete lattice-point box,
and checks every potentially minimizing width direction and difference-body
lattice vector. It also checks the earlier weaker-gauge witness and rejects
three mutations. [Validation](../results/det5_height_witness_validation.json).

## Partial interval campaigns

The initial [archive](../results/det5_height_interval.json) has 98 queries:
five whole-square exclusions for class 4, and 93 class-5 queries with 12
closed leaves and 72 pending boxes. The stronger-gauge class-5 campaign
has another 93 nodes and the same partial counts. Neither excludes class 5.
The stronger rational gauge 183/500 is necessary for a global width above
17/5, but the exact witness already passes it, so further Y-only subdivision
cannot yield the intended theorem.

The [joint Y/U archive](../results/det5_joint_height_interval.json) imposes
width greater than 17/5 in both integer directions. The shifted U-contact
heights are (2,2,1,0), so its offset constraint is offset+2*gap<=1.
Three Y representatives and all twelve U extrema pairs give 36 charts.
There are 217 recorded nodes, 13 complete charts and 131 pending boxes.
The use of the three Y representatives is necessary for the global-width
target because affine lattice symmetries preserve global lattice width;
U itself need not be invariant under that symmetry.

A further [16 exact midpoint fibers](../results/det5_joint_fibers.json)
were all UNSAT, with no old node re-queried. These exclude only isolated
parameter points, not neighborhoods or a continuous class. Their read-only
provenance and encoding audit is stored with the results. Some tested Y
heights coincide, so even an empirical general trend is not established.
None of these partial campaigns contributes to the count of 58.

## Replay

```sh
python3 tests/replay_det5_height_witness_independent.py
```

With the optional pinned Z3 package, the geometric and initial 98-node
encoding audit can be run without a satisfiability query:

```sh
python3 tests/audit_det5_height_independent.py
```

The proof/input and external-kernel replays for the completed class-4
exclusion are documented in [CLAIM-0008](../claims/CLAIM-0008.md).

## Follow-up after the public checkpoint

The four affine contact symmetries of the strong Y-wide witness produce
U-widths approximately 2.686736, 3.243847, 5.601748 and 3.066930. The third
image is a rigorously hollow body with both Y and U widths greater than
17/5. Its Y extrema, however, are [2,0], outside the retained representatives
[0,1], [0,3], [1,0]. It falsifies unrestricted two-direction sufficiency but
does **not** prove any retained chart feasible. The earlier global-target
symmetry reduction remains valid. Its exact matrix, full widths and gauge
minimum are checked in [the independent replay](../tests/replay_det5_joint_symmetry_independent.py)
and [receipt](../results/det5_joint_symmetry_validation.json).

Twelve numerical searches on the original witness's fixed guard/sign branch
reached U-width at most about 3.215542. This is an observed value, not an
upper bound. Another 24 distinct exact fibers, fixing Y extrema [1,0] and
free Y heights [5/16,1/8], were UNSAT. These point exclusions neither prove
a neighborhood empty nor settle any continuous chart. Original archives
were preserved; [query records](../results/det5_retained_joint_probe.json)
and [numerical guidance](../results/det5_retained_joint_probe_numeric.json)
are separate.

A continuation of the published joint-cover seed visits only new children.
The [new archive](../results/det5_joint_continuation.json) has 514 total
queries, including the 217 immutable seed records: 297 genuinely new
queries. Twenty of 36 charts now have recorded complete covers, leaving
142 pending boxes. These partial cover results are not class exclusions.
The independent [encoding/frontier audit](../tests/audit_det5_joint_cover_independent.py)
checks exact boxes and mathematical formulas, not the truth of UNSAT labels.

## Complete fifteen-direction formulations

The [independent geometric review](DET5_COMPLETE_GEOMETRY_REVIEW.md) proves
that exactly fifteen primitive directions up to sign need testing at target
17/5. Every other direction has integer width at least four on the contact
tetrahedron itself. These fifteen directions form five symmetry orbits;
one cannot quotient the width requirements by assuming the surrounding
body is symmetric. The review gives general convexity counterexamples to
such a reduction, without claiming irredundancy under hollowness.

A bilinear model introduces the four unknown body vertices V. The contact
equations V^T F=P^T and column stochasticity imply the augmented identity
[1;V^T] F=[1;P^T]. Its right side has determinant of absolute value five,
so F and the body frame are invertible automatically. All fifteen width
clauses are linear in V. A strengthened version bounds the positive mass
of each vertex's affine contact coordinates by 50000000/2042829, using
the necessary volume bound. These are linear cuts.

Both bilinear targets (20 variables, maximum degree two) and a strengthened
eight-variable cubic target reached UNKNOWN under distinct 20-second
solver limits. No prior query was rerun. Their lower-width and target
pinned controls are evaluated exactly without a solver; the lower-width
pin is a formula regression only.

- [Implementation](../experiments/det5_complete_vertex_lift.py) and [archived outcomes](../results/det5_complete_vertex_lift.json)
- [Independent bilinear polynomial audit](../tests/audit_det5_vertex_lift_independent.py) and [receipt](../results/det5_vertex_lift_encoding_validation.json)

The complete model is available for further decomposition. The global
flatness bound and the list of 58 candidate contact configurations are
unchanged. These follow-up files are included in the newly authorized GitHub update.

## Bounded determinant-three/four control campaign

A separate generic-height root test covers five Y-extrema representatives
for each of the determinant-three and determinant-four contact classes.
All ten outer root relaxations have exact rational SAT assignments, with
the same necessary strong gauge threshold 183/500. They therefore do not
provide immediate root-square exclusions; this says nothing about the
existence of actual high-width hollow tetrahedra in those classes.

[Root queries](../results/det34_height_roots.json) and
[the combined independent probe audit](../tests/audit_det34_and_joint_probes.py)
retain their encodings and exactly check the relaxed SAT assignments.
The audit also verifies the 24 retained joint fibers' distinctness and
source provenance, without checking their UNSAT labels with a proof kernel.

## Retained witnesses force a pivot

The next immutable archive contains 835 queries: 27/36 recorded complete
charts, with 243 pending boxes. Two linear gap cuts derived from volume
produce a genuine retained Y/U witness immediately. Four added gauges exclude
it, but a second witness remains after 14 new queries. Four more gauges give
the complete 18 primitive vectors of intrinsic contact gauge at most 6/5.
After 104 further queries, a third retained witness survives even every
integer gauge at the exact ACMS target threshold. The final mixed archive
has 953 queries, 27 recorded complete charts and 259 pending boxes.

| Witness | Finite gauge system | Full first minimum of K-K | Full lattice width |
|---|---|---|---|
| First retained | 10 vectors | 113/505 | 53676652/26445567 |
| Second retained | 14 vectors | 5671/20595 | 10682780276/4192650405 |
| Third retained | 18 vectors, plus independently checked full minimum | 211637/541875 | 96007799530165500/39202828222912103 |

All three are exactly hollow, have the prescribed relative-interior contacts
and actual retained Y-extrema, and have Y/U widths greater than 17/5. The
first two expose missing gauges. The third exposes the insufficiency of the
two-direction model even with every target gauge and the stated volume
necessities. Further gauge-only refinement cannot close this system.
Their complete widths are small; none challenges the flatness conjecture.

- [First witness](DET5_RETAINED_TWO_DIRECTION_WITNESS.md)
- [Second witness](DET5_SECOND_RETAINED_WITNESS.md)
- [Third witness and independent exact certificate](DET5_FULL_GAUGE_RETAINED_WITNESS.md)
- [Four-vector rank lemma and volume-gap cuts](DET5_VOLUME_GAP_BOUNDS.md)
- [General tetrahedron containment inequality](SIMPLEX_WIDTH_VOLUME_MONOTONICITY.md)

The general inequality width(K,u)/vol(K) <= width(P,u)/vol(P), for nested
full-dimensional tetrahedra, has a written elementary proof and an exact
symbolic check of all 1536 stochastic partition identities. It yields the
linear gap cuts and a complete finite box for small gauges under the actual
volume hypothesis. No priority or global flatness improvement is claimed.

Encoding/frontier audits reconstruct the new formulas and bind inherited
inputs to frozen earlier archives. They do not prove the archived UNSAT
labels. All selected witness properties are checked by independent rational
arithmetic without importing solver or discovery code. The next experiment
must add width directions from the complete fifteen-direction formulation.

## Scaled complete-width frame and a first certified box

The [new frame](DET5_SCALED_VERTEX_HEIGHT_FRAME.md) writes
T_i=b(v_i-v_L), b=1/width(K,Y), and forces T_L=0 and normalized Y-extrema.
Its 17 variables satisfy bilinear reconstruction; all fifteen width tests
are linear. Reconstruction forces invertibility. With fixed rational free
Y-heights, affine elimination gives a twelve-variable quadratic formulation;
this is a slice representation, not a proof over a height box.

Three complete exact targets timed out. A 27-query outer campaign has
19 rational SAT assignments and eight recorded UNSAT leaves, with fourteen
pending matrix boxes across three charts. The independent audit reconstructs
all thirty formulas and frontiers. It supplies rational product completions
for all nineteen saved assignments, each of which fails exact reconstruction.
The pinned retained body passes every non-width exact assertion and fails
exactly the Z and (1,-2,-2) lower-width clauses.

A second formulation transfers frozen Y/U boxes linearly into the scaled
frame, tightens Y products, and adds all-direction volume spans and shared
barycentric-volume cuts. Thirty-six new queries give fourteen SAT, twenty-one
UNKNOWN, and one UNSAT. Every full saved rational SAT assignment satisfies
the corresponding outer formula, but none supplies a body at the target.
All 36 encodings have independent exact audits and six corruption controls.

The one new UNSAT box is Y:[0,3], U:[0,3], with free heights
[3/4,1]^2 x [1/2,1]^2. The full formula did not replay within the cvc5 time
limit. Removing twelve width disjunctions, while retaining Y and U through their
direct span conditions, yields a simpler five-direction core: Y, U, Z, (0,1,-1), (1,-2,-2). That weaker formula is refuted by cvc5
and its CPC proof is verified by Ethos, with referenced assumptions and
final false conclusion bound to its input. The global-width hypothesis is
still needed to derive the gauge and volume necessities. The
[box exclusion](DET5_FIVE_DIRECTION_BOX_EXCLUSION.md) is standalone and does
not depend on the old frontier's unverified UNSAT labels.

Three strictly larger boxes were tried once: [1/2,1]^4 is relaxed SAT;
[3/4,1]^2 x [0,1]^2 is UNKNOWN; [0,1]^2 x [1/2,1]^2 is relaxed SAT.
No larger domain, full chart or additional contact class is excluded.
The original 953-query archive is unchanged, including its 259 pending
boxes; one of those boxes now has an independent continuous refutation.

The exact known-witness analysis computes 300 widths across twenty labeled
symmetry images (sixteen distinct bodies). Z rejects all known retained-chart
Y/U witnesses. Some unnormalized images survive Y/U/Z, but all such images
are outside the retained charts. No global sufficiency of three or five
directions is inferred from this finite table. Twelve restricted numerical
starts testing all fifteen directions observed a best width about 3.071883;
this is neither an upper bound nor an independently certified new witness.

- [Known-witness table and scope](DET5_KNOWN_WIDTH_OBSTRUCTIONS.md)
- [Base encoding and rational-completion audit](../results/det5_scaled_frame_encoding_validation.json)
- [Transfer audit](../results/det5_scaled_pending_transfer_validation.json)
- [Five-direction core and proof producer](../results/det5_scaled_leaf_width_core.json)
- [External proof-kernel receipt](../results/det5_scaled_width_core_ethos_validation.json)
- [Larger-box outcomes](../results/det5_scaled_box_enlargement.json)

This follow-up is included in the newly authorized public checkpoint. The global
bound and 58-type list remain unchanged; no mathematical priority is claimed.
