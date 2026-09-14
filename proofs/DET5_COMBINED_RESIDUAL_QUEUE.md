# Combined residual queue with the strong anchor rectangle

Status: exact necessary-domain refinement for actual hollow determinant-five
class-5 tetrahedra with strict facet contacts and **global lattice width
strictly greater than `17/5`**. No complete coverage or whole-class exclusion.

The [new combined queue](../results/det5_combined_residual_queue.json) is
obtained from the [separated-height queue](../results/det5_separated_residual_queue.json)
by excluding the closed rectangle

    Y_extrema=[0,3], q1 in [0,1/256], q2 in [31/256,33/256].

The exclusion is bound to the [anchor archive](../results/det5_strong_anchor_rectangle.json),
its [independent geometry/input audit](../results/det5_strong_anchor_rectangle_validation.json),
and its [Ethos reference-bound proof receipt](../results/det5_strong_anchor_rectangle_ethos_validation.json).
The stronger gauges and volume gap premise are necessities for the stated
true global target. The assertion is not inferred from a large Y width alone.

Every Y[0,3] entry receives one appended strict clause:

    q1<0 OR q1>1/256 OR q2<31/256 OR q2>33/256.

This is precisely the complement of the closed rectangle, including all
boundary points. The first literal is redundant inside the normalized
height square but is retained so that the full complement is explicit.
All prior closed boxes, U bounds, strict clauses and separated-height
polynomial constraints are preserved. There are still 258 entries:
70 receive this clause and the other 188 are unchanged. Redundant clauses
on disjoint boxes are harmless. No classification of amended entries as
empty or nonempty is attempted, and no entries are removed.

All inherited measure and overlap fields retain their earlier meaning;
**they are not measures of the combined domains**. No total remaining area
or volume is computed.

The whole anchor rectangle lies outside the previous eight closed excluded
Y rectangles, as checked by exact separating coordinate intervals. It also
satisfies the earlier separated-height necessity throughout: `q1<q2` and

    q2-q1 >= 15/128 > 539/128000
                    >= (49/1500)*q2*(1-q1).

Thus its area `1/32768` is a new exclusion beyond the separated-height band.
Eight preceding residual entry projections contain the entire anchor
rectangle, with all their old strict clauses uniformly satisfied. Their U
boxes remain unchanged. This does not assert nonemptiness after the new cut.

Reproduce the integration and independent audit from the repository root:

```sh
python3 experiments/det5_combined_residual_queue.py
python3 tests/audit_det5_combined_residual_queue.py
```

The audit imports no generator. It checks the entire predecessor chain's
entry values at this transformation, the strict complement on all 35
sign-invariant endpoint/open cells of the rectangle boundaries, the universal
rational interval bounds above, and exact hashes linking the proof and
geometry receipts to their source artifacts. These rectangle cells do not
constitute a numerical discretization of the quadratic separated-height
band. Three mutation controls reject a nonstrict complement, an altered old
clause, and loss of the separated-height constraint. The
[validation record](../results/det5_combined_residual_queue_validation.json)
is PASS. This integration runs no solver or proof kernel; it binds their
existing evidence and adds an exact queue audit.
