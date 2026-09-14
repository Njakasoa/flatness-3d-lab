# Independent review of cleared complete-width inequalities

Status: exact algebraic formulation review, not a width exclusion. The two
eight-parameter ordered charts are reviewed in
[the chart note](DET5_RATIONAL_HEIGHT_CHART_REVIEW.md). The fixed contact
simplex is P=conv(0,(5,1,2),e2,e3).

Write delta=det(F)=bD and N=P_matrix adj(F), where P_matrix is the
three-by-four matrix of contact coordinates. If delta is nonzero, the
actual vertex matrix is N/delta. For an integer covector v and unordered
vertex pair i,j, put

    G_ij = v . (N_i-N_j).

Regardless of the sign of delta, its directional width is exactly

    max_{i<j} |G_ij| / |delta|.

Consequently width_v(K)>17/5 is equivalent to the finite disjunction

    OR_{i<j} (5 G_ij > 17 |delta| OR -5 G_ij > 17 |delta|).

The determinant comparison must be strict. Replacing it with a non-strict
comparison would change the target and permit threshold-equality bodies.
The model explicitly imposes delta!=0, although the four strict horizontal
gauges already imply this through the established rank argument. The extra
comparison makes the cleared-denominator interpretation immediate.

The Y direction is represented exactly by 0<b<5/17, since the reconstructed
normalized vertex heights have minimum zero and maximum one. The other
fourteen directions use the displayed pair disjunctions. The
[fifteen-direction enumeration](DET5_COMPLETE_GEOMETRY_REVIEW.md) is
complete for the target: any omitted primitive integer covector has integer
width at least four on P, and hence width at least four on every K containing
P. The independent audit repeats the bounded enumeration rather than merely
trusting the saved list.

Entries of F are quadratic. Cofactor cancellation gives pair numerators of
degree at most five; delta=bD has degree five. Thus the complete-width
formulation has eight real variables and polynomial inequalities of degree
at most five, with a conditional expression implementing the absolute
determinant. It introduces no free product variable.

The proof of the width equivalence uses contact containment and invertibility.
It does not require hollowness. The strong gauges and observer guards are
additional necessary conditions for the research target. A solver UNKNOWN
gives no exclusion, and a solver SAT would still require exact reconstruction
and the appropriate hollowness verification before being presented as a
geometric counterexample.

Run `.venv/bin/python tests/audit_det5_quadratic_full_width_independent.py`.
The audit derives F independently by solving the two column equations,
computes every cofactor by the six-term determinant formula, checks all
entries of F adj(F)=delta I in both branches, reconstructs the complete input
formulas, and verifies every occurrence of the absolute determinant before
canonical comparison. It also checks that the earlier weak-gauge rational
witness fails both strengthened gauge conditions and actual full-width
conditions. No discovery generator is imported and no solver query is run.
