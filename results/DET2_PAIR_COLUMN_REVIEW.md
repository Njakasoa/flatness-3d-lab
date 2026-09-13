# Independent exact witness review

The archived certificate passes an independent standard-library Fraction
replay. It describes a hollow tetrahedron in the determinant-two pair
branch with all four row-dominance inequalities strict and exact width

    3731889842479498000000 / 1172185068224586160791 > 19/6.

This is one certified example. No optimum, upper bound, infeasibility,
new-theorem priority, or claim at width 17/5 follows. No solver was run in
this review. The replay does not import the generator, its geometry core,
SymPy, or Z3.

## Reproduction and checks

Run from the lab directory:

    python3 tests/replay_det2_pair_column_independent.py

The verifier independently reconstructs the eight-parameter F, checks its
zero diagonal, all twelve strictly positive off-diagonal entries, four
column sums, every strictly positive pair-row surplus, and designated sum
above two. It computes det(F) by permutation expansion and F inverse by
rational Gauss-Jordan elimination. The reconstructed vertices exactly
match the certificate and satisfy F lambda(V_j)=e_j.

The physical volume, independently computed from three vertex edges, is

    5000000000000000000000 / 1172185068224586160791
      = 1/(3 det(F)).

The smallest integer bounding box containing every integer point of the
body is [-4,4] x [0,4] x [-1,1]. Evaluation of all four exact facet slacks
at all 135 integer points finds no interior points and exactly these five
boundary points:

    (-1,1,0), (0,0,0), (0,0,1), (0,1,0), (2,1,1).

The four designated contacts (0,0,0), (2,1,1), (0,1,0), (0,0,1) each have
exactly their designated zero slack and three positive slacks. The
additional point (-1,1,0) is also in the relative interior of the facet
through (0,0,0). Every supplied facet equation, vertex incidence, lattice
contact list, and relative-interior contact list is checked independently.

For width completeness, take D with rows V_i-V_0, i=1,2,3, and let W be
the least of the three exact coordinate widths. Every possible minimizing
integer direction u has width at most W. Therefore q=D u has |q_i|<=W,
so |u_j|<=W sum_i |(D inverse)_ji|. Taking exact integer floors yields
bounds (1,1,6). Enumerating all primitive directions modulo sign in that
box checks 53 directions; nonprimitive directions cannot improve width.
The unique minimizer modulo sign is (0,1,1). The exact minimum and all
supplied upper/lower/search-bound certificate fields agree.

Twelve independent corruptions are rejected: changed F entry, zero
off-diagonal entry, changed vertex, volume, determinant, width, direction
bound, integer bounding box, removed boundary point, changed contact,
changed facet offset, and false dominance slack. Checks use explicit
exceptions and remain active under Python optimization.

## Omitted S/T domain inequalities in the column SMT

The current `make_solver` does not explicitly append the advertised
-62,63 coordinate and subset-sum bounds. At the main threshold 17/5,
this omission is mathematically harmless: the inequalities are implied
by the asserted determinant cut and chart constraints, even before
assuming hollowness of a feasible assignment.

Indeed beta=1-(13/6)/(17/5)=37/102 and the asserted inequality is

    delta > beta^3/3 = 50653/3183624.

Hence vol(K)=1/(3 delta)<1061208/50653<21. The column chart has all
four contacts in K, so their tetrahedron P is contained in K and has
volume 1/3. For any vertex v of K, write lambda_i for its affine
coordinates relative to P. The visible-facet pyramids have disjoint
interiors and volumes (-lambda_i) vol(P) for lambda_i<0. Thus

    vol(conv(P,v)) = (1 + sum_i max(0,-lambda_i))/3 <= vol(K)<21.

Consequently the total negative barycentric mass is less than 62, and
the total positive mass is less than 63. Every sum over a subset of the
four coordinates therefore lies strictly between -62 and 63. This covers
each T_ij and the Y/Z subset sums T_1j+T_2j and T_1j+T_3j. Multiplication
by delta>0 gives the advertised weak S inequalities (indeed stronger
strict ones). No missing-domain bug affects the threshold-17/5 model.

This redundancy argument is specific to a determinant cut strong enough
to imply volume below 21. It must be recomputed for other thresholds or
if that cut is disabled. The solver metadata's domain description would
be clearer if marked “implied by the determinant cut at 17/5” rather than
read as a list of explicitly emitted assertions.

## Generator observations

No critical error affecting this witness was found. The generator's
standalone positivity expression filters zero entries, so that expression
alone would not reject an off-diagonal zero. Its subsequent four contact
relative-interior checks do reject every such zero, and the independent
replay directly checks all twelve off-diagonal positions. This is a minor
clarity/robustness issue, not a certification failure for the saved body.

The numerical search and archived snap provenance are not mathematical
premises of the replay. In particular, its result does not rely on the
certificate's textual account of a previous strict QF_LRA SAT check.

## Exact perturbation to precisely four boundary lattice points

The independent replay now requires both the original certificate and
`certificates/det2_pair_four_contacts.json`. The latter changes only
parameter p[2]=c1 by +1/1000000; the verifier checks that exact relation.
The new certified width is

    932976210619799500000 / 293047542170915539223 > 19/6.

The second replay independently repeats every matrix, volume, integer-box,
facet, contact, and complete-width check. It requires precisely four
boundary lattice points, equal to the four designated contacts, and all
pair-dominance surpluses strictly positive, with minimum 501/1000000.
The former fifth boundary point q=(-1,1,0) now satisfies

    (F lambda(q))_0 = -1/2000000 < 0,

so lies strictly outside. This is an example in the strict pair branch
with precisely four boundary lattice points, rather than merely a choice
of four determinant-two contacts among five. It is still only an example,
not an optimum or a global bound.

Boundary cardinality is an explicit required argument to the replay, not
inferred from the certificate's claim. Both archived widths are checked,
and replacing either complete valid body with the other is rejected.
The twelve field mutations are applied separately to each certificate,
with two additional whole-witness substitution tests.

Both full replays pass under ordinary Python and `python3 -O`: 135 integer
points and 53 complete primitive directions per body, 24 field mutations
rejected in total, and both whole-witness substitutions rejected.

The contact-index distinction is substantive. In the first body, replacing
p0 by q=(-1,1,0) yields contact edge determinant of absolute value one;
the verifier checks this unimodular alternative exactly. In the second
body, the only four boundary lattice points are the designated contacts,
whose edge determinant has absolute value two (also independently checked).
Thus every choice of one relative-interior lattice contact per facet in
the second body forces this index-two contact tetrahedron, up to ordering.
