# Shared row-difference products in the ordered Y chart

The [exact ordering lemma](DET5_Y_CORNER_ANALYTIC_PROBE.md) partitions every
actual tetrahedron in the Y-extrema chart [0,3] into q1<q2 or q1>q2.
It proves min(q1,q2)<a<max(q1,q2), fixes the signs of

    d_i = F_i3-F_i0,       i=1,2,

and gives a single linear expression for the Z gauge in each branch.
All off-diagonal entries of the column-stochastic contact matrix lie in
(0,1). Thus d_i belongs to [-1,0] for the smaller-height row and to [0,1]
for the larger-height row. The closed bounds include all actual strict
contacts and may safely be used in an outer relaxation.

Let w_ij denote the existing lifted variables for q_i F_ij. For an actual
body, the *shared* row difference satisfies the identity

    r_i = w_i3-w_i0 = q_i*(F_i3-F_i0) = q_i*d_i.          (1)

This identity uses the same height q_i in both products. It can yield
necessary linear conditions beyond separate envelopes for w_i3 and w_i0.
With q in [0,1], d in [l,h], the four valid inequalities for r=q*d are

    r >= l*q,
    r >= h*q+d-h,
    r <= l*q+d-l,
    r <= h*q.                                           (2)

Their nonnegative residuals are respectively

    q*(d-l), (1-q)*(h-d), (1-q)*(d-l), q*(h-d).

This proves validity throughout the closed intervals, without an endpoint
exception. Use (l,h)=(-1,0) for the smaller-height row and (0,1) for the
larger-height row. The two rows supply eight additional inequalities in
existing variables; no new independently selectable products are introduced.

## Independent encoding and saved-model audit

`python3 tests/audit_det5_ordered_root_independent.py` reconstructs the six
frozen inputs from an independent 22-variable full-matrix builder:

| Archive | Two order branches include |
|---|---|
| det5_y_ordered_root.json | strict height order, Z signs and linear gauge |
| det5_y_ordered_root_offset.json | those constraints plus strict offset order |
| det5_y_ordered_root_difference.json | those constraints plus the eight cuts (2) |

All inputs also contain the unchanged weak-gauge and finite-guard premises,
the target gap bound, the original product envelopes, contact reconstruction,
and strict complements of eight certified same-chart rectangles: seven old
Y[0,3] leaves and the [3/5,1]^2 enlargement. There are eight complements in
each input, not thirteen; rectangles from the other Y-extrema chart are not
subtracted here. Their original refutation inputs and existing successful
proof receipts are bound by exact reconstruction and hashes.

All six saved assignments satisfy every assertion by exact rational
substitution. Every assignment has at least one nonzero w_ij-q_i F_ij
residual, recorded in the [audit receipt](../results/det5_ordered_root_encoding_validation.json).
They establish outer feasibility only; none is certified as an actual
tetrahedron by these assignments.

The original q1>q2 assignment violates an offset-order inequality. The
original q1<q2 assignment violates one row-difference inequality. Thus the
new necessary conditions do exclude previously feasible relaxed points.
Both saved assignments from the offset variant already satisfy all eight
row-difference cuts; the audit does not claim that those particular points
were excluded by the third variant. Both third-variant branches remain SAT.

The auditor rejects reversed-order, missing-complement, and zero-gap
corruptions. It imports no discovery generator, invokes no solver, and
does not rerun a proof kernel. No chart or further height region is closed
by these six SAT results.
