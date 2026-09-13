# CLAIM-0007 — determinant-seven/eight contact exclusions by a finite height cover

Date: 2026-09-14. Status: **verified computer-assisted restricted class bounds**.
The complete rational cover and its geometric/encoding soundness passed
independent internal review. All62 independent cvc5 leaf refutations passed
complete internal proof checking and external Ethos checking, with
reference-bound assumptions and rejected corruption controls.
No new global flatness bound or external mathematical priority is claimed.

## Precise target

Let K be a compact full-dimensional hollow real tetrahedron in the standard
integer lattice. Suppose one lattice point in the relative interior of each
of its four facets gives a full contact tetrahedron affine unimodularly
equivalent to either

    P7 = conv(0,(7,1,2),(0,1,0),(0,0,1)),
    P8 = conv(0,(8,1,3),(0,1,0),(0,0,1)).

Then

    w(K) <= 17/5 = 3.4 < 2+sqrt(2).

This requires the four prescribed relative-interior facet contacts. It is
not a bound for arbitrary nonsimplicial bodies containing P7 or P8, nor for
all containing tetrahedra without the facet-contact condition. Sharpness
is not claimed.

Classes 6 and 7 of CLAIM-0004 are
excluded above width17/5. Together with CLAIM-0006, the necessary full
contact list at width at least2+sqrt(2) falls from61 to59: six tetrahedral
classes, 52 spatial hulls with five to eight vertices, and one square.
The original list above c=(11/7)(1+2/sqrt(3)) still has62 classes.
Larger full contact hulls are not excluded merely by containing one of the
four excluded tetrahedral subsets.

## Geometric reduction

Argue by contradiction from w(K)>17/5. ACMS Lemma5.1 gives every nonzero
integer vector a gauge in K-K of at least1-A/w(K), where A=1+2/sqrt(3).
The exact inequality A<13/6 therefore gives every such gauge >37/102.
For each prescribed contact p_j, let F_ij be its barycentric coordinate at
vertex i of K, indexing facet j opposite vertex j. Thus F has zero
diagonal, strictly positive off-diagonal entries, and column sums one.
Its inverse recovers K. The gauge of a difference vector z is

    gamma_(K-K)(z) = ||F ell(z)||_1/2.

The complete observer theorem supplies twenty guards for each of P7,P8
under the six primitive contact-edge gauges. Hollowness implies that at
least one barycentric coordinate is nonpositive at each guard. All cuts
are necessary for the assumed high-width K.

Let Y be the width-one contact covector. Its width on K also exceeds17/5.
Normalize its vertex values to q_i in[0,1], with an ordered minimum/maximum
pair q_L=0,q_H=1. Put b=1/w(K,Y) and offset=-min(Y_i)/w(K,Y). Then

    F^T q = offset*1 + b*(0,1,1,0),
    0<b<5/17,  offset>=0, offset+b<=1.

The contact automorphisms reduce twelve possible ordered extrema to six
orbits for P7 and five for P8. Reflection reverses ordered extrema.
Ties are allowed, so every K lies in at least one of these eleven charts.
The rank theorem in [HEIGHT_RANK_AND_VOLUME](../proofs/HEIGHT_RANK_AND_VOLUME.md)
provides the converse bounded-body interpretation but is not needed to
justify these necessary conditions for an already existing K.

## Continuous-to-finite step

Only the two remaining normalized heights create nonlinear terms.
For each rectangle q_i in[l_i,h_i], replace every product q_i F_ij by a
new variable p_ij and impose the four exact rational inequalities

    l_i F_ij <= p_ij <= h_i F_ij,
    q_i+h_i F_ij-h_i <= p_ij <= q_i+l_i F_ij-l_i.

They hold for all F_ij in[0,1], and hence form an outer relaxation. All
remaining constraints are linear arithmetic with finite disjunctions.
If such a relaxation is UNSAT, the entire rectangle contains no possible
body, not merely its sampled points.

Bisect the longer interval at its rational midpoint after every SAT or
UNKNOWN relaxation. Retain both closed halves, with their common endpoint.
The archived search has113 nodes and62 terminal UNSAT-labelled rectangles,
covering all eleven initial squares[0,1]^2. The two UNKNOWN nodes are
internal nodes with both children completely covered. Neither UNKNOWN nor
SAT is used as a terminal exclusion. No determinant/volume cut is needed.

The [independent audit](../proofs/HEIGHT_RANK_REVIEW.md) reconstructed every
one of the113 formula sets, all dyadic splits, gauge and guard constraints,
and all symmetry orbits. All62 leaf exclusions are now checked by a second SMT engine and an
external proof checker. The [independent cvc5 replay](../tests/replay_height_cover_cvc5.py)
rebuilds the model with twelve free matrix entries rather than eight,
solves each leaf independently, checks complete proofs internally, and
exports CPC proofs for external verification.

## Artifacts and validation

- [Finite cover and original outcomes](../results/height_interval_relaxation.json)
- [Exact interval construction](../experiments/height_interval_relaxation.py)
- [Independent mathematical and encoding review](../proofs/HEIGHT_RANK_REVIEW.md)
- [Independent cvc5 validation receipt](../results/height_cover_cvc5_validation.json)
- [Independent cvc5 encoding and proof export](../tests/replay_height_cover_cvc5.py)
- [External Ethos validation](../results/height_ethos_validation.json) and [portable checker](../tests/check_height_ethos.py)
- [Exact formula/cover audit](../results/height_cover_encoding_validation.json) and [reproduction driver](../reproduce_height_cover.py)
- [Bounded primary-source novelty audit](../proofs/HEIGHT_EXCLUSION_LITERATURE.md)

The finite domain is justified mathematically; the exclusions are claims
about exact rational linear arithmetic. The written geometry uses known
ACMS/observer/classification results. Proof checking does not establish
novelty, external peer review, or a new global bound on Flt(3).

## Completed computational validation

Z3 discovered113 relaxed nodes with62 terminal UNSAT rectangles. Independent
cvc5 1.3.4 rebuilt all62 leaf problems with twelve independent matrix entries,
confirmed UNSAT, checked complete proofs internally, and exported CPC proofs.
No proof node is marked TRUST. Ethos 0.2.3 at its pinned official revision
checked every CPC refutation against its own referenced SMT assumptions.
Its reference adapter is restricted to nullary Real variables; it preserves
all assertions and normalizes only their numeral tokens to Real form.
Proof declarations are checked against that reference and removed only where
they duplicate it. The full proof is streamed after reference loading, so
Ethos retains the reference-binding state. A fresh unrelated assumption and
a changed final conclusion are both rejected by Ethos. Local guards also
reject a missing final false and a non-Real reference declaration.

The exact geometry remains a written proof with internal independent review;
Ethos checks the finite linear refutations, not the entire geometric theorem
inside a proof assistant. Its kernel, compiler/runtime and pinned official
CPC signatures form the stated computational trust base. This is distinct
from external human peer review or priority validation.
