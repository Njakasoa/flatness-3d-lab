# Strict pair witnesses above width 19/6 and a failed finite screen

There exists a maximal hollow tetrahedron with precisely four lattice
contacts of normalized determinant two, strict pair dominance, and width

    932976210619799500000 / 293047542170915539223 > 19/6 > 3.

This excludes a proposed universal width-at-most-three pruning rule for
the pair branch, even when there are exactly four contacts and all pair
inequalities are strict. Such a rule was never established in this lab.
The witness is below the known global lower bound 2+sqrt(2), and no class
optimum, new global flatness bound or mathematical novelty is asserted.

## Exact construction

Use the column chart in PAIR_COLUMN_FORMULATION.md. In the parameter order
(c0,d0,c1,d1,c2,d2,c3,d3), start with

    (169893/200000, 1/10000, 588557/1000000, 268049/1000000,
     294329/1000000, 58855699/300000000, 49999999/50000000, 1/100000000).

The matrix is

    F = [[0,c1,d2,d3],
         [c0,0,1-c2-d2,1-c3-d3],
         [d0,d1,0,c3],
         [1-c0-d0,1-c1-d1,c2,0]].

This first body has width
3731889842479498000000/1172185068224586160791 >19/6 and five boundary
lattice points: the four designated contacts and q=(-1,1,0).
Now increase c1 by 1/1000000, leaving the other seven parameters unchanged.
Columns still sum to one, every off-diagonal entry stays positive, and all
four pair row-surpluses remain strictly positive. The smallest is
501/1000000. Since lambda(q)=(-1/2,-1/2,3/2,1/2), its row-zero facet slack
changes from zero to -1/2000000. Thus q is now strictly outside.

The proof does not assume that moving q out preserves hollowness. The
whole exact integer bounding box is checked again, and the complete width
search is derived again from an inverse edge matrix. It finds precisely

    (0,0,0), (0,0,1), (0,1,0), (2,1,1)

on the boundary and no integer point in the interior. Each contact has one
zero facet slack and three positive slacks, so each facet has a relative
interior lattice point. The standard maximal lattice-free criterion then
makes the tetrahedron maximal. The four contacts have determinant two;
there is no alternative boundary contact from which to select a different
contact hull. In contrast, the original five-contact body also permits a
unimodular contact selection by replacing (0,0,0) with q; its contact
configuration alone would not exclude that possibility.

Generators and certificates:

- experiments/certify_det2_pair_column.py and certificates/det2_pair_column.json
- experiments/certify_det2_pair_four_contacts.py and certificates/det2_pair_four_contacts.json
- tests/replay_det2_pair_column_independent.py and results/DET2_PAIR_COLUMN_REVIEW.md

The independent replay uses only Fraction arithmetic and imports neither
generator nor the geometry engine. Review and mutation counts are recorded
in the linked review. The original numerical sample is discovery provenance,
not a mathematical premise of either exact certificate.

## Two exact false high-width candidates

The generator experiments/det2_partial_box_counterexamples.py reconstructs
two other rational tetrahedra from recorded numerical runs 7 and 14. Both
have positive column matrices and valid weak pair dominance. Their widths
are respectively

    8252695464092000000 / 2290488401370002229 > 7/2,
    789949112854225000 / 220706204534322573 > 7/2.

Neither has a strict interior lattice point among the 216 points of
[-2,3]^3. Nevertheless, full exact enumeration finds respectively
(-3,1,-1) and (-3,-1,1) strictly inside. The certificate records all four
positive slacks at each hidden point. Their positivity persists in an
explicit small parameter neighborhood, so this is not a floating-point
rounding ambiguity.

These are counterexamples to sufficiency of the small-box screen, not
counterexamples to the flatness conjecture. Both have gamma(eX)<37/102 and
are already excluded by the necessary ACMS cuts of the newer threshold-17/5
column model. Adding their point exclusions does not by itself demonstrate
additional strength over that newer model. The full finite lattice box
remains mathematically justified; no small-box sufficiency is asserted.
