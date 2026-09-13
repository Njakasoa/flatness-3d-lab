# CLAIM-0008 — determinant-five contact class 4 exclusion

Date: 2026-09-14. Status: **verified computer-assisted restricted class bound**.
The exact geometry and encoding passed independent internal audit. Five
independently encoded cvc5 refutations passed complete internal proof checking
and external Ethos checking against their referenced assumptions. This is
software verification, not external human peer review; novelty is unconfirmed.

## Statement and scope

Let K be a compact, full-dimensional hollow real tetrahedron in Z³. Suppose
one lattice point in the relative interior of each of its four facets gives
a full contact tetrahedron affine unimodularly equivalent to

    P = conv((0,0,0), (5,1,1), (0,1,0), (0,0,1)).

Then `w(K) <= 17/5 = 3.4 < 2+sqrt(2)`.

The prescribed relative-interior facet contacts are essential. This statement
does not cover arbitrary containing tetrahedra or nonsimplicial bodies.
It excludes class 4 of [CLAIM-0004](CLAIM-0004.md). The other determinant-five
class, class 5 with contact vertex `(5,1,2)`, remains unresolved.

Together with [CLAIM-0006](CLAIM-0006.md) and [CLAIM-0007](CLAIM-0007.md), this
leaves **58 necessary full contact classes** at width at least `2+sqrt(2)`:
five tetrahedral classes (indices 0, 1, 2, 3, 5), 52 spatial hulls with five
to eight vertices, and one square. Larger full hulls are not removed merely
because they contain excluded tetrahedral subsets. The count above the
original lower threshold `c=(11/7)(1+2/sqrt(3))` remains 62. The global
flatness bound is unchanged.

## Geometric implication and finite certificate

Suppose `w(K)>17/5`. Put `A=1+2/sqrt(3)`. ACMS Lemma 5.1 and `A<13/6`
imply `gamma_(K-K)(v)>37/102` for every nonzero integer vector v. Let F have
as column j the barycentric coordinates of contact point j in K, with
facet j opposite vertex j. F has zero diagonal, positive off-diagonal
entries, and column sums one. For the linear barycentric difference map ell,
`gamma_(K-K)(v)=||F ell(v)||_1/2`.

The independently verified observer certificate gives 40 guards on eight
lattice lines. Each guard has at least one nonpositive barycentric coordinate
because K is hollow. The seven imposed gauge directions are the six
primitive contact-edge directions together with `(1,0,0)`. All constraints
are necessary consequences of the assumed K.

Normalize the four vertex values of Y to heights q in `[0,1]`, with an
ordered minimum/maximum pair `(L,H)`. With `b=1/w(K,Y)` and the corresponding
offset, the exact contact relations are

    F^T q = offset*1 + b*(0,1,1,0),
    0 < b < 5/17,  offset >= 0,  offset+b <= 1.

Only the subgroup of four contact automorphisms preserving Y up to sign and
translation is used. The full contact group has order eight and cannot all
be used for this chosen-height reduction. The subgroup covers all twelve
ordered extrema through five representatives:
`(0,1)`, `(0,2)`, `(0,3)`, `(1,0)`, `(1,3)`.

For each representative, the other two q coordinates range over the whole
closed square `[0,1]^2`. Replace each product `q_i F_ij` by p and impose the
four McCormick inequalities for that square. These give an outer relaxation:
every actual K satisfies them. Each of the five root relaxations is UNSAT;
no subdivision, sampling argument, rank converse, or volume cut is needed.
Consequently the complete continuous family is excluded.

The independent cvc5 encoder uses twelve free matrix entries, rather than
the eight-parameter discovery encoding. Its five refutations have 29,237
proof nodes in total. All complete internal proof checks passed without
TRUST or SORRY rules. Ethos 0.2.3 checked all five exported CPC proofs against
their independent SMT inputs. Four corruption controls were rejected.
The geometric reduction remains a written argument with independent internal
review; it is not formalized in Ethos. The Ethos kernel, runtime, official
CPC signatures, and validated reference adapter form the computational trust
boundary.

## Evidence and reproduction

- [Independent geometry and encoding review](../proofs/DET5_HEIGHT_REVIEW.md)
- [Five-root certification details](../proofs/DET5_CLASS4_CERTIFICATION.md)
- [Independent encoding audit receipt](../results/det5_height_encoding_validation.json)
- [cvc5 proof receipt](../results/det5_class4_cvc5_validation.json)
- [Ethos proof receipt](../results/det5_class4_ethos_validation.json)
- [Count and evidence manifest](../certificates/det5_class4_contact_exclusion.json)
- [Bounded primary-source novelty audit](../proofs/DET5_CLASS4_LITERATURE.md)

Run `python3 reproduce_det5_class4.py` for standard-library guard/count checks
and archived input, proof, and reference binding. This default mode hashes
and frames proofs; it does not run a proof kernel or reconstruct all formulas.
Add `--audit-python .venv/bin/python` to run the independent Z3-based
geometry and formula audit, with zero solver queries. To recheck the proof
kernel, use the dedicated Ethos command in the certification details and
[build guide](../proofs/HEIGHT_ETHOS_REPRODUCTION.md). Solver regeneration is
separate and is unnecessary for verifying already archived proofs.
