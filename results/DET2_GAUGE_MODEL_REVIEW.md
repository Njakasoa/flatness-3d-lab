# Review of the gauge-complete pair encoding

Verdict: no critical encoding error found at the intended threshold 17/5.
The model includes the six edge-gauge hypotheses required to make its
20 point exclusions a complete hollowness test in the pair chart.
The recorded main result is UNKNOWN due to timeout, not elimination.
This review did not run main(), Solver.check(), or any NRA solve.

## Exact model checks

Source inspection and construction-only Z3 AST inspection confirm:

- Eight real variables and 89 unpinned assertions.
- Maximum asserted polynomial degree three. The rational vertex
  reconstructions T and V are reporting expressions and are not asserted
  as variable-denominator constraints.
- All six primitive contact-edge directions occur, each with one OR over
  the fourteen nonempty proper subsets of four coefficient rows.
- Each edge expression uses the difference coordinates
  (X/2-Y-Z, X/2, Y-X/2, Z-X/2), with no affine constant one.
  Column sums imply sum(theta)=0 for theta=F ell, making the maximum
  subset sum exactly half its L1 norm. All fourteen comparisons are
  strict lower bounds and are affine in the eight parameters.
- There are exactly 20 guard clauses. Each is an OR of four affine
  inequalities F_i lambda(z)<=0, correctly excluding strict interior
  points while allowing boundary contacts. These point coordinates do
  include the affine constant one.
- beta_for_threshold(17/5)=37/102. The six asserted gauges use this beta,
  consistent with the archived guard construction.

The 37 width directions were independently reconstructed by enumerating
primitive integer normals modulo sign with width(P,u)<=3. Completeness
of the finite enumeration follows from contact values
(0,2a+b+c,b,c): b,c lie in [-3,3] and a in [-4,4]. Directions with contact
width at least four automatically have body width greater than 17/5,
since P is contained in K. The reconstructed set exactly matches the
imported direction set. For every retained direction, six vertex pairs
and both signs correctly encode width greater than the target via the
positive determinant; these polynomial inequalities have degree at most
three.

The column chart retains zero diagonal, positive off-diagonal entries,
column sums one, pair-row dominance, designated sum greater than two,
and positive determinant. The reviewed chart proof gives boundedness,
full dimension, and the four designated relative-interior contacts.
Canonical inequalities use entries of F. The retained ACMS determinant
cut also makes the previously omitted -62,63 domain inequalities
redundant, as proved in the earlier column-model review.

## Pin and controls without a solve

The permutation p=(2,3,1,0) commutes with the pair involution and transforms
both rows and columns of the exact four-contact witness. An exact check
confirms that F01 is maximal among designated entries and F23>=F32.
Substituting its eight exact rational parameters directly into every
assertion and simplifying, without a solver query, gives:

- At 19/6, all assertions are true.
- At 17/5, five assertions are false.

This independently validates the intended positive/negative control
behavior reported by the archived runs. It does not infer anything about
the unpinned model from the negative pinned control.

## Scope and minor maintainability caveat

The guard archive and independently replayed geometry are consistent:
64 total guards, 44 pair-domain tautologies, 20 retained clauses, and
six explicit edge-gauge assumptions. Under those hypotheses the target
model's hollowness test is complete. The broader ACMS/classification inputs
remain the mathematical premises documented in CLAIM-0005 and the proofs.

The helper make_solver accepts arbitrary thresholds but always receives
the fixed guard list constructed for beta=37/102. At a lower threshold,
the recomputed beta is smaller and this same shortened list is not in
general a complete hollowness criterion. The report explicitly limits
that lower-threshold invocation to a pinned control, which is correct.
Future reuse as a general lower-threshold solver must rebuild the guard
list or retain the stronger six edge-gauge assumptions. No change is
needed for the current target run.

The archived main query reports timeout/UNKNOWN after roughly 31.7
seconds for a configured 30-second timeout. This supplies neither
feasibility nor infeasibility. No new solver run was performed for this
review.
