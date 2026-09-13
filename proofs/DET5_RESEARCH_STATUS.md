# Determinant-five research status — 2026-09-14

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
