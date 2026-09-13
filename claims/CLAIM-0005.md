# CLAIM-0005 — complete lattice guards for nonunimodular contact tetrahedra

Status: **internally verified application of known observer/classification
principles**. General statement independently reviewed; determinant-two
arithmetic independently implemented. Mathematical novelty is unconfirmed.
This is not a new global flatness bound or elimination of a contact class.

## Exact statement and class of bodies

Let P be an empty three-dimensional lattice tetrahedron of normalized volume
d>1. Let K be compact, full-dimensional and convex, contain P, and have all
four vertices of P on its boundary. Then there is an explicitly constructible
union of at most twelve lattice lines L(P), depending only on P, such that

    int(K) intersect Z^3 is empty
    iff int(K) intersect L(P) intersect Z^3 is empty.

The lines are the neighboring primitive lattice lines to the two contact
segments in each width-one slab of P. There are at most three such slabs
up to orientation. If vol(K)<V, retain only lattice points z on these lines
with negative contact-barycentric mass less than 6V/d-1; the resulting
finite set remains a necessary and sufficient hollowness test.

For P=conv(0,(2,1,1),e2,e3) and V=21 there are twelve lines, 123 parameters
per line and 1456 distinct guards. In the positive pair-dominant facet chart,
972 exclusions are automatic, leaving 484 explicit lattice clauses.

## Gauge refinement

If the difference-body gauge on each of the six primitive contact edges
exceeds beta=37/102, the required line parameters lie in an explicit
interval of length at most 269/37. Therefore at most 96 points suffice for
any d>1 contact tetrahedron, without a volume cutoff. For the determinant-two
case the exact union contains 64 points and only 20 nontrivial pair clauses.
The six edge-gauge assumptions must be asserted; the three coordinate-axis
cuts alone are insufficient. This is a conditional complete hollowness test,
not an assertion of hollowness from width alone.

The proof uses two explicit convex combinations of vectors in K-K to bound
the allowable line parameter. See
[the gauge refinement](../proofs/DET2_OBSERVER_GAUGE_GUARDS.md),
[exact data](../certificates/det2_observer_gauge_guards.json), and
[independent replay](../tests/replay_det2_gauge_guards_independent.py).

## Normalization, threshold and hypotheses

The lattice is standard Z^3; volume is ordinary Euclidean volume and d is
six times vol(P). The general theorem has no width threshold. Its application
to the current pair target uses W=17/5 and the already derived ACMS volume
cut vol(K)<1061208/50653<21. In the column model that cut is asserted as a
determinant inequality and therefore applies to any feasible assignment.

Boundary contacts are essential to retain all five vertices of a minimal
interior extension. The theorem permits arbitrary compact convex K, not only
a tetrahedron. The empty contact tetrahedron and d>1 assumptions cannot be
dropped from this proof. No corresponding line-only theorem is asserted for
the unimodular contact case.

## Exact certificate and continuous-to-finite reduction

Full proof: [DET2_OBSERVER_LINES.md](../proofs/DET2_OBSERVER_LINES.md).
Certificate: [det2_observer_lines.json](../certificates/det2_observer_lines.json).
Generator: [det2_observer_lines.py](../experiments/det2_observer_lines.py).

The argument selects an interior integer point minimizing the volume of its
extension of P. The extension has exactly five lattice points and all are
vertices. The known width-one theorem forces it into a slab of P; its
three-point section is a unimodular triangle. This gives the lattice-line
equations. The volume cutoff then bounds integer parameters by an exact
piecewise-linear negative-mass inequality. The code does not infer
completeness from the size of a numerical search.

## Independent implementation and adversarial review

[Independent stdlib replay](../tests/replay_det2_observer_lines_independent.py)
imports neither generator nor geometry core. It checks the twelve lines,
all 1456 guards, the pair profile and eight deliberately corrupted artifacts,
including coverage and cutoff data. It passes with and without Python `-O`.
[Independent mathematical review](../proofs/DET2_OBSERVER_REVIEW.md) checks
minimality, boundary assumptions, width-one classification, plane-lattice
normalization, degeneracies and the general d>1 extension.

## Counterexample search and controls

Two exact nonhollow pair bodies with width >7/2 pass the old 216-point screen.
Each contains one hidden point on the new guard list. Both are rejected by
the complete screen; neither is a flatness counterexample. Their newer
ACMS cuts already reject them as well. See
[the witnesses and false-candidate analysis](../proofs/DET2_PAIR_WITNESSES.md).

Exact hollow pair bodies with five and precisely four boundary contacts,
both of width >19/6, provide positive controls. They have independent full
bounding-box and width replays. A bounded implementation is
[det2_pair_complete_smt.py](../experiments/det2_pair_complete_smt.py).
The later 20-clause, six-edge-gauge implementation is
[det2_pair_gauge_complete_smt.py](../experiments/det2_pair_gauge_complete_smt.py).
Both full target queries returned UNKNOWN under bounded runs. Positive and
negative exact four-contact pins passed. Separately, all 484 old guards are
implied by the satisfiable 20-guard/six-gauge QF_LRA antecedent. This is a
computational cross-check of the independently proved geometric implication.
Solver outcomes are recorded separately and are not premises of this theorem.

## Closest prior work and 2025–2026 audit

Blanco–Santos, [arXiv:1409.6701v3](https://arxiv.org/pdf/1409.6701),
Theorem 1.2(1), supplies the five-point width-one theorem; the authors also
attribute the all-vertices case to Howe.

Averkov–Schymura, *Complexity of linear relaxations in integer programming*,
[primary full text](https://d-nb.info/1230965718/34), Definition 4.1,
Proposition 4.3 and especially Lemma 6.4 already develop observer/guard sets
and confine observers to neighboring lattice lines plus a finite set in
relevant width-one cases. The general observer and line principles are
therefore known. Here the boundary-contact hypothesis removes the
non-extreme extensions, and the explicit d>1/twelve-line specialization
makes the current flatness feasibility model practical. This is not enough
to establish a new mathematical contribution.

A targeted web audit on 2026-09-13 included 2025–2026 queries and found these
close antecedents; most narrow keyword results were irrelevant. It is not
an exhaustive priority audit and gives no basis for a first-proof claim.

## Proof level and open objections

Level 5 for the stated determinant-two reduction and its exact enumeration:
written proof, independently implemented arithmetic and internal Astra review.
The arbitrary d>1 statement has a written mathematical argument and independent
review, but no all-class enumeration is claimed. The external classification
is used as a published theorem, not re-proved by the program.

Open work: extract useful exact width bounds from the complete finite model;
extend implementation to other nonunimodular contact tetrahedra; determine
whether the explicit specialization has publishable novelty. The global
flatness conjecture and the unimodular continuous contact class remain open.
