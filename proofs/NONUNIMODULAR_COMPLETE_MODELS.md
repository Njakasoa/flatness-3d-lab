# Complete determinant-seven and determinant-eight feasibility targets

The target is w(K)>17/5 for a bounded hollow tetrahedron whose four
relative-interior facet contacts are
P=conv(0,(d,1,a),e2,e3), with (d,a)=(7,2) or (8,3).
These are eight-variable cubic formulations. Their archived target queries
both returned UNKNOWN; no infeasibility or class exclusion follows.

## Contact chart and necessary cuts

The contact-to-body barycentric matrix F has diagonal zero, off-diagonal
entries positive, and column sums one. Two entries in each column are free;
the third is one minus their sum. If delta=det(F) is nonzero, this chart is
the inverse image of the ordinary simplex, and hence a bounded tetrahedron.
Both signs of delta must be retained. Its contact-coordinate vertices are
the columns of adj(F)/delta, and vol(K)=d/(6|delta|).

As in the earlier column model, the determinant is cubic and differences of
adjugate columns are quadratic. Thus width inequalities, after multiplication
by |delta|, have degree at most three. The bound A<13/6 and ACMS's necessary
lambda1(K-K)>=1-A/w(K) give beta=37/102 as a strict lower bound on every
nonzero lattice gauge at this target. The volume bound vol(K)<1/beta^3
therefore supplies |delta|>d beta^3/6 and rules out singular matrices.

All six contact-edge gauges are imposed as disjunctions of fourteen affine
subset sums. The complete 20-point observer lists for each class then give
necessary and sufficient hollowness tests under these assumptions, by
CLAIM-0005. Additional short-vector gauges strengthen the necessary cuts.
The coarse beta could be improved, but no stronger constant was used in
these archived runs. No total-leakage restriction is imposed in these models.

## Why only ten primitive width directions are needed

Since P is contained in K, w(K,u)>=w(P,u) for every integer covector u.
The contact width is an integer. If it exceeds three, it is already at least
four and cannot violate the target width inequality. All directions that
can matter therefore have contact vertex values

    (0,h,y,z), h,y,z in {-3,...,3},
    max(0,h,y,z)-min(0,h,y,z)<=3.

They correspond to integer covectors exactly when d divides h-y-a*z, in
which case u=((h-y-a*z)/d,y,z). Remove zero, nonprimitive vectors and the
negative representative. Each of the two classes leaves exactly ten
directions. This is an exhaustive proof from containment, not an empirical
search radius. The independent audit reconstructs them by rational Gaussian
elimination on the contact edge matrix instead of the congruence formula.

For each remaining u and vertex pair j,k, set
N_jk=sum_i (u dot p_i)(adj(F)_ij-adj(F)_ik). The exact width test is

    OR_(j<k) [N_jk>(17/5)|delta| OR -N_jk>(17/5)|delta|].

These ten tests and the stated gauge, volume and observer constraints give
the complete target in this contact chart. Positivity keeps the contacts
in relative facet interiors; arbitrary containing tetrahedra with different
boundary incidence are not this model's stated domain.

## Recorded outcomes and audit

Each class passed an exact positive pin at width one and a negative pin at
17/5. Those lower-threshold pins are controls; the target-specific necessary
cuts are justified for the main target. The unpinned queries, each requested
with a ten-second limit, returned UNKNOWN after approximately 11.54 and
10.10 seconds respectively. No SAT body or UNSAT certificate was produced.

`tests/audit_nonunimodular_encoding.py` checks the saved assertions against
the current construction after parsing SMT-LIB (temporary let names do not
affect equality), verifies eight variables and maximum degree three,
independently reconstructs all ten directions, and substitutes both exact
pins without calling a solver. At the lower threshold all constraints are
true; at the main threshold ten width constraints fail for each pin.

```sh
.venv/bin/python tests/audit_nonunimodular_encoding.py
```

This is an encoding and arithmetic audit, not a new independent mathematical
peer review. The written reduction uses the already reviewed column/gauge
identities and observer theorem. The archived UNKNOWN outcomes must remain
separate from mathematical conclusions. Further progress requires an
additional structural bound or certificate method, rather than repetition
of these unchanged queries.
