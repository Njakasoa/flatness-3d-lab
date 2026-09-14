# Exact residual queue after certified Y exclusions

Date: 2026-09-14. Status: an exact replacement for the declared pending
normalized-height domain, with no new solver query or class exclusion.
The [generator](../experiments/det5_certified_residual_queue.py) uses only the
standard library and creates
[the immutable residual queue](../results/det5_certified_residual_queue.json).
It changes no earlier archive or proof payload.

## Sources and resulting queue

The input domain consists of the 259 pending closed four-dimensional boxes
in the frozen 953-query
[joint Y/U archive](../results/det5_joint_short_gauges.json). The subtracted
regions are the twelve closed Y rectangles whose independent cvc5 proofs
were checked by Ethos in
[the certification receipt](../results/det5_class5_y_cvc5_validation.json).
Their exact overlap with the pending boxes is recorded by
[the independent overlay](../results/det5_certified_y_overlay.json).

The residual queue has 258 entries:

- One whole box is removed: Y-extrema [0,3], U-extrema [0,3], node r111111.
- Six entries lose exactly half of their normalized four-dimensional measure.
- Another 105 entries lose certified boundary points but no positive measure.
- The remaining 147 entries are unchanged.

The 111 changed entries retain 203 explicit strict complement clauses in
total. These counts concern a labeled parameter domain, not counts of actual
bodies or contact classes. The new queue has now been implemented; the old
archive continues to record its historical 259 pending boxes unchanged.

## Exact complement of a closed certified rectangle

Let B be an original closed four-box, and let x,y denote its first two
coordinates, the free normalized Y-heights. For a certified closed rectangle

    R=[a,b] x [c,d],

the exact condition for lying outside R is

    x<a OR x>b OR y<c OR y>d.                         (1)

Every comparison in (1) is strict. Changing any of them to a weak inequality
would reintroduce a certified boundary. The residual entry is the intersection
of B with (1) for every certified rectangle in its Y chart.

A rectangle disjoint from B's Y projection imposes no extra condition, since
B already lies outside it. For an intersecting rectangle, the implementation
removes only individual literals that are impossible throughout B. For example,
if B has x>=a, then the literal x<a is false throughout B and may be deleted.
It does not weaken any retained strict comparison. The remaining clause is
stored explicitly, even when the rectangle meets B only on an edge or corner.

For each entry, the original four closed box bounds remain active. The
outside clauses are joined by AND; the literals inside each clause are joined
by OR. This represents the exact subtraction without introducing new closed
boxes on boundaries that should have been deleted.

The six half-covered boxes all occur in Y-extrema [0,1], whose free heights
are (q2,q3). Their Y projection is [1/4,1/2]^2. The old certified rectangle
r00110 removes its left half [1/4,3/8] x [1/4,1/2]; another certified
rectangle removes the upper boundary. The resulting Y region is precisely

    q2 in (3/8,1/2],   q3 in [1/4,1/2).

Their original U bounds remain unchanged. Thus merely replacing the first
Y interval by the closed interval [3/8,1/2] would be incorrect.

## Full containment and continuous verification

The certified Y rectangles in each chart have disjoint interiors. Exact
rational intersection areas therefore add without double-counting positive
area. A pending nondegenerate closed rectangle is wholly covered when the
sum equals its area. This also certifies its boundary coverage: a finite
union of closed rectangles is closed, so a nonempty relative complement in
the pending rectangle would contain a relatively open neighborhood with
positive area. Exactly one pending box is wholly covered.

The implementation additionally checks subtraction by an endpoint partition.
On each distinct pending Y projection, collect all certified rectangle
endpoints lying inside it, together with its own endpoints. These divide each
coordinate interval into endpoint singletons and open intervals. Every
rectangle-membership predicate and strict clause literal is constant on each
Cartesian product of these cells. Testing the endpoints and one rational
midpoint of every open interval therefore proves the identity on the entire
continuous projection, including every edge and corner.

There are 45 distinct Y projections, verified with 417 exact representative
pairs. Original closed-rectangle membership is compared with the generated
Boolean complement on every pair. Four additional endpoint controls check
the removed threshold 3/8, a surviving point strictly beyond it, the removed
upper boundary 1/2, and preservation of the original outer box bound. The U
coordinates do not occur in the subtraction, so their original bounds can
be carried over unchanged.

## Consumer format

Use `entries` from the JSON. Each entry preserves `Y_extrema`, `U_extrema`,
`node`, and the original `box`, with two free Y coordinates followed by two
free U coordinates, each in increasing vertex-index order outside its extrema.

For each item in `outside_Y_clauses`, impose the OR of its `literals`.
A literal records `free_coordinate`, `vertex_index`, `relation`, and the exact
rational string `threshold`. In the scaled frame T_i=b(v_i-v_L), normalized
Y-height q_i equals T_i,Y, so substitute `T[vertex_index][1]` directly.
Do not use the free-coordinate index as a vertex index. The JSON also records
the certified rectangle and proof input supporting each clause.

The queue is frozen output: rerunning the generator checks equality with an
existing queue rather than overwriting a changed state. Reproduce with

    python3 -m experiments.det5_certified_residual_queue

No solver or proof checker is called. The generator binds the original Y and
joint snapshots, the certification receipt, original and reconstructed proof
inputs, and compressed and expanded CPC payload hashes. It also binds the
previous independent overlay, whose geometric statement reconstruction and
reference-input checks have already passed. Existing external-check receipts
are evidence here, not fresh kernel executions.

## Scope

Each certified Y rectangle excludes actual hollow determinant-five contact
tetrahedra at global target width greater than 17/5. This remains true for
all U values, so its cylinder may be removed from each matching joint chart.
The queue is exactly the original declared pending domain minus those
certified cylinders.

It does not certify the remaining historical joint UNSAT labels or prove that
this pending domain by itself covers every possible global-target body.
A complete class exclusion still requires the remaining domain and the
inherited closed regions to have valid complete proof chains. No conditional
width bound has been extended to the whole contact class, and the 58-type
candidate count remains unchanged.
