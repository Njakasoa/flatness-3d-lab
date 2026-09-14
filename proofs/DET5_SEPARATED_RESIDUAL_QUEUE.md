# Exact separated-height refinement of the residual queue

Status: necessary-domain refinement for actual hollow determinant-five
class-5 tetrahedra with strict facet contacts and global lattice width
strictly greater than `17/5`. No complete class exclusion or finite coverage
certificate is claimed. No solver queries are used.

## Exact transported necessity

On the chart `Y_extrema=[0,3]`, write the other normalized Y heights as
`q1,q2` in `[0,1]`. The [exact ordering lemma](DET5_Y_CORNER_ANALYTIC_PROBE.md)
excludes `q1=q2`. In each strict order set `m=min(q1,q2)`,
`M=max(q1,q2)`, so `M>0` and `1-m>0`. The bounded shape coordinates in the
[compact shape proof](DET5_COMPACT_SHAPE_CHART_REVIEW.md) give

    p=m/M, q=(1-M)/(1-m),
    1-p*q=(M-m)/(M*(1-m)).

The branch-specific denominator bounds therefore imply the disjunction

    (q1<q2 AND q2-q1 > (49/1500)*q2*(1-q1))
    OR
    (q1>q2 AND q1-q2 > (249/1700)*q1*(1-q2)).

All inequalities are strict, including at the permissible external
height boundaries. Positive denominator multiplication gives the equivalent
integer polynomials

    q2-q1>0 AND -1500*q1+1451*q2+49*q1*q2>0,
    OR
    q1-q2>0 AND 1451*q1-1700*q2+249*q1*q2>0.

The stronger reverse coefficient is tied to the physical order `q1>q2`;
it is not transported to the other branch.

## Queue semantics and preserved archives

The [new queue](../results/det5_separated_residual_queue.json) copies every
entry from the [preceding queue](../results/det5_enlarged_residual_queue.json)
and appends the displayed disjunction to precisely its 70 entries with
Y extrema `[0,3]`. All 258 entries remain, and the other 188 entries are
unchanged. Every original box, U coordinate, rational string and strict
rectangle-complement clause is preserved exactly as a JSON value. The old
queue file is never modified.

An entry means its old closed box AND all old strict complement clauses AND
its new necessary constraint, if present. The full queue is still the union
of these labeled entry domains. The new constraint uses an OR of two AND
branches; every listed polynomial must be strictly positive. Polynomial terms
`[c,i,j]` denote `c*q1^i*q2^j`.

**Inherited measure and overlap fields describe only the preceding queue.**
They are intentionally preserved, and must not be read as areas or volumes of
the newly refined domains. No classification of empty amended entries, total
area calculation, or new entry removal is asserted. Likewise, no revalidation
of inherited joint solver labels is inferred from this update.

## A continuous region newly excluded

The whole closed rational rectangle

    R=[1/8,63/500] × [127/1000,16/125]

has area `1/1000000` and lies strictly inside the low square `[0,1/4]^2`.
Throughout R, `q1<q2`, and exact interval bounds give

    q2-q1 <= 3/1000
           < 2719451/750000000
           = (49/1500)*(127/1000)*(437/500)
           <= (49/1500)*q2*(1-q1).

The strict margin is `469451/750000000`. Thus the first branch fails at
every point, including the rectangle boundary, and the reverse branch fails
by its height order. R is disjoint from each of the eight previously
excluded closed Y rectangles. The independent audit additionally verifies
that eight preceding residual entry projections contain all of R, with all
their old strict clauses uniformly satisfied there. Those entries retain
their entire original U boxes. This establishes genuine positive-area new
exclusion in the preceding residual domain; it is not a numerical grid or
an assertion about the area of the entire excluded band.

## Reproduction and scope of the audit

Run from the scientific repository:

```sh
python3 experiments/det5_separated_residual_queue.py
python3 tests/audit_det5_separated_residual_queue.py
```

The generator rejects a differing pre-existing output instead of overwriting
it. The [independent audit](../tests/audit_det5_separated_residual_queue.py)
imports no generator, reconstructs the rational separation polynomials,
checks every old entry value, hashes the analytic sources, proves the
rectangle inequalities by rational interval bounds, and verifies disjointness
from all previous Y rectangles. Three negative controls reject a deleted
entry, changed old bound, and changed separation coefficient. Its
[record](../results/det5_separated_residual_queue_validation.json) reports
PASS. It verifies this queue transformation and the displayed universal
rectangle argument; the analytic denominator theorem retains its own proof
and validation scope.
