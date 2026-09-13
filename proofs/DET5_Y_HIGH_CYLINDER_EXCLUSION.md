# The checked proof excludes a Y-height cylinder without U restrictions

Date: 2026-09-14. Status: a 69-assumption subset of an existing refutation
has been checked by Ethos, and its geometric hypotheses have been mapped
independently. This upgrades an old Y-only UNSAT label to a checked certificate;
it does not discover a new normalized region or exclude the whole class.

Let K=conv(v0,v1,v2,v3) be a compact full-dimensional hollow real tetrahedron,
with p0=0, p1=(5,1,2), p2=e2, p3=e3 in the relative interiors of its respective
opposite facets. Normalize the vertex heights in Y=(0,1,0) to q_i in [0,1].
There is no such K with **global lattice width greater than 17/5** and

    q0=0, q3=1, q1,q2 in [3/4,1].

There is no restriction on normalized U-heights or U-extrema in this statement.
The global-width hypothesis remains needed to derive the gauge and Y-span
bounds below. The assertion is not obtained from a few directional widths alone.

## What the proof actually uses

The original 589-assertion input declared 485 distinct top-level proof
assumptions. An independent occurrence census and a separate lexical dependency
slice agree: only 69 of these assumptions are referenced, and 416 declarations
are inert. Proof identifiers are reused inside nested scopes, so the slice
resolves references in their active lexical environment rather than by a global
last-definition map. The retained proof has been checked against the actual
[69-assertion subset input](../certificates/det5_scaled_box_used_assumptions.smt2),
not merely against the earlier full reference.

The necessary geometric ingredients are:

- Positivity and stochasticity of the contact matrix F, and their redundant
  coordinate bounds 0<=F_ij<=1.
- Gauges in (1,0,0) and (3,0,1) exceeding 37/102, and gauges in (1,0,1)
  and (2,0,1) exceeding beta=183/500.
- Exclusion from the interior of K of the four lattice points
  (-1,0,0), (1,0,1), (2,1,1), and (3,1,1).
- The three Y contact reconstruction equations and valid product envelopes
  for q1,q2 in [3/4,1].
- The reciprocal Y-span bound b>2042829/50000000, where b=1/width(K,Y).

The full mapping, including individual proof assumption identifiers and exact
expanded formulas, is in
[the independent analysis](../results/det5_width_core_assumption_analysis.json).
Group counts there overlap when an inequality belongs to both an original
product envelope and a tightened transfer group.

No U interval, U-extremum condition, additional directional lower-width
clause, horizontal reconstruction equation, or barycentric volume-mass cut
is referenced. The old explicit bound b<5/17 is likewise unused. The global
volume necessity is still present through the lower bound on b.

## Every retained assumption follows from the stated target

For an actual K let F contain the barycentric coordinates of its four
contacts, and use b=1/width(K,Y). Its columns are stochastic, its diagonal
vanishes, and its other entries are positive. With H=(0,1,1,0), contact
averaging gives

    sum_i (F_ij-F_i0) q_i = b H_j,     j=1,2,3.

Set the Y product variables to F_ij q_i. These satisfy all retained unit-box
and [3/4,1]-box McCormick inequalities exactly. Setting q0=0 and q3=1 yields
precisely the three retained Y reconstruction equations.

For difference coordinates ell(v) relative to P,

    gamma_(K-K)(v)=(1/2)||F ell(v)||_1.

The ACMS global-target inequality gives every nonzero integer gauge greater
than beta, which is also greater than 37/102. Thus the four retained gauge
clauses hold. Hollowness directly gives the four stated point-exclusion
clauses: each of those integer points has some nonpositive body barycentric
coordinate. This necessity uses no sufficiency claim about a truncated guard set.

Put R=6/(5 beta^3). The global-target volume necessity and the nested-tetrahedron
width/volume inequality give width(K,Y)<R, hence b>1/R. The other retained
span atom b>-1/R is automatically satisfied. This is the only substantive
volume consequence needed in the projected geometric argument.

Four retained inequalities still mention two horizontal product variables:

    -M_X F_13 <= w1_3_0 <= M_X F_13,
    -M_Z F_20 <= w2_0_2 <= M_Z F_20,

where M_X=1250000000/34728093 and M_Z=500000000/34728093 are positive.
These variables occur in no other retained assertion. They can both be
assigned zero because F_13,F_20>=0. No horizontal vertex reconstruction or
actual-product interpretation is required for these two auxiliary variables
in the reduced formula. This existential projection is why their presence
does not reintroduce any U or other horizontal restriction.

Consequently every actual target satisfying the displayed Y square would
produce an assignment to all 69 retained assumptions. The externally checked
refutation contradicts that assignment, proving the U-free statement.

## Evidence, history and scope

The subset input has SHA-256

    76eedc308f32b7451afa12ea5b20da37431f482fa1b46e7e71807888d6ed3bfe.

The [external subset-check receipt](../results/det5_sliced_proof_validation.json)
binds it to the sliced CPC proof and records successful pinned Ethos checking,
including rejection of an unrelated assumption. No solver was rerun to obtain
this strengthening. The
[independent assumption analyzer](../tests/analyze_det5_width_core_assumptions.py)
performs source-formula matching and classification, rather than proof-kernel
checking.

This square is exactly the old class-5 Y-extrema [0,3] leaf `r1111`, already
recorded UNSAT in both
[the weak Y-only archive](../results/det5_height_interval.json) and
[the stronger-gauge Y-only archive](../results/det5_strong_height_interval.json).
Those entries previously carried solver labels; the new contribution here is
an externally checked proof and an explicit geometric hypothesis audit for
the same region. Its U-restricted appearance in the later joint frontier
reflected incomplete reuse of the old Y-only exclusions.

This standalone cylinder theorem does not rely on any old UNSAT label.
It also does not complete the [0,3] Y chart or the determinant-five class.
The 58-type candidate count and the global flatness bound remain unchanged.
