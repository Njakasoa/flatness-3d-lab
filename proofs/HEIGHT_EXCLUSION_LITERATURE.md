# Literature audit: the determinant-7 and determinant-8 contact exclusions

Date: 2026-09-14. Eight focused search queries, followed by direct primary-source
inspection. This bounded audit concerns antecedents and priority; it does not
verify the mathematical encoding or the solver certificates.

## Candidate and scope

The proposed statement is: if a full-dimensional hollow real tetrahedron K has
one lattice point in the relative interior of each of its four facets, and the
convex hull of these four selected contacts is affine unimodularly equivalent to
either

    P7 = conv(0, (7,1,2), e2, e3),
    P8 = conv(0, (8,1,3), e2, e3),

then its lattice width is at most 17/5. Determinants 7 and 8 are normalized
volumes, not ordinary Euclidean volumes. The candidate imposes the four facet
contact conditions. It makes no assertion about arbitrary nonsimplicial bodies
containing P7 or P8, nor about the optimal width within either class.

The proposed computational argument uses the ACMS gauge inequality, finite
observer constraints, normalized heights with two free coordinates, and
McCormick linear outer relaxations on rational rectangles. The supplied campaign
description reports eleven symmetry branches covered by 62 rectangles, each
UNSAT in Z3; a separate cvc5 encoding was still being checked when this audit was
assigned. These are campaign reports, not results independently established by
this literature search. No solver was queried during the audit.

**No equivalent P7/P8 contact-class bound, or matching 17/5 theorem, was located
in the inspected sources. Priority remains unconfirmed.** Coordinate-specific
negative search results are especially weak because the same contact tetrahedron
can appear in other unimodular coordinates or notation.

## Closest geometric antecedents

Averkov, Codenotti, Macchia, and Santos, *A local maximizer for lattice width of
3-dimensional hollow bodies*, [arXiv:1907.06199](https://arxiv.org/pdf/1907.06199),
Discrete Applied Mathematics 298 (2021), 129–142, is the direct antecedent.
Lemma 5.1, equation (14), p. 18 of the 22-page PDF, yields
`lambda_1(K-K) >= 1 - (1+2/sqrt(3))/w(K)`. Section 5.3 and Theorem 5.4,
pp. 19–20, reduce the contact analysis of a width maximizer to finitely many
inscribed empty lattice polytopes. Its tetrahedral determinant bound is 17 and
therefore does not itself eliminate determinants 7 or 8. The discussion on
pp. 20–21 proposes solving fixed-contact real-algebraic cases with computers,
while explaining the practical difficulty of direct quantifier elimination.
No P7/P8 exclusion by normalized-height rectangles was located there. Thus the
finite fixed-contact programme and gauge input are established antecedents;
the possible contribution here is solving two specified cases with explicit
certificates. This is an inference from the inspected sections, not a claim
that no equivalent consequence can be derived elsewhere in the literature.

Codenotti and Santos, *Hollow polytopes of large width*,
[arXiv:1812.00916](https://arxiv.org/pdf/1812.00916), Proc. AMS 148 (2020),
835–850, Section 5 and Theorem 5.1, studies an explicitly symmetric family
circumscribed about a unimodular contact simplex. Its value `2+sqrt(2)` and
vertical-line hollowness verification are relevant benchmarks. They do not
constitute the stated determinant-7 or determinant-8 contact theorem. In
particular, this source already provides an example of certifying hollowness
through exact intervals on finitely many lattice lines.

Codenotti and Freyer, *Lattice Reduced and Complete Convex Bodies*,
[arXiv:2307.09429v2](https://arxiv.org/abs/2307.09429v2), gives structural results
about reduced bodies; its abstract states that a simplex realizing the flatness
constant must be lattice reduced. The abstract and repository record checked
in this audit do not state the proposed contact-class exclusions. This limited
inspection is not a full-paper exclusion of an equivalent result.

## Established computational ingredients

Garth P. McCormick, *Computability of global solutions to factorable nonconvex
programs: Part I — Convex underestimating problems*, Mathematical Programming
10 (1976), 147–175, [publisher record and abstract](https://link.springer.com/article/10.1007/BF01580665),
explicitly develops convex underestimation to discard regions that cannot
contain a global minimizer. The publisher exposes only a subscription preview;
the full 1976 article was not inspected. Convex outer relaxation and exclusion
of parameter regions must therefore not be presented as a new general method.

Tsoukalas and Mitsos, *Multivariate McCormick relaxations*, Journal of Global
Optimization 59 (2014), 633–662,
[open-access article](https://link.springer.com/article/10.1007/s10898-014-0176-0),
Sections 1–2, discusses factorable functions, auxiliary variables, product
relaxations and relaxed linear programs. It also discusses interval enclosures.
These are established ingredients of the proposed height-product formulation.
The publisher links an erratum; this audit uses the article only for these
general antecedents, not a specialized theorem affected by that correction.

The elementary four bilinear inequalities can be justified directly: for
`l <= x <= u`, `L <= y <= U`, and `z=xy`, expanding the four nonnegative products
of distances to interval endpoints gives

    z >= l*y + L*x - l*L,
    z >= u*y + U*x - u*U,
    z <= u*y + L*x - u*L,
    z <= l*y + U*x - l*U.

Consequently, rational rectangle subdivision and exact infeasibility checks
could certify the proposed geometric exclusions, provided the geometric
implication, symmetry coverage, rectangle coverage, relaxation direction, and
every infeasibility certificate are independently justified. A SAT relaxation
or an UNKNOWN solver result would not settle an original nonlinear case.
This logical observation and the displayed elementary derivation are not
priority claims. The application-specific contacts, finite guards and complete
certificate collection are the potential contribution.

## Search record and limitations

The eight query strings were:

1. `"hollow tetrahedra" "7" "8" width`
2. `"lattice width" tetrahedron "17/5"`
3. `"flatness" "contact" "tetrahedra" Codenotti`
4. `McCormick 1976 computability global solutions factorable nonconvex programs underestimating problems`
5. `"Codenotti" thesis "flatness" tetrahedra`
6. `"hollow" "tetrahedra" "contact" "width" 2026`
7. `"lattice width" "7,1,2"`
8. `"lattice width" "interval" proof tetrahedra`

Queries returned many unrelated items. Secondary aggregators were used only
for discovery and are not mathematical authorities here. Codenotti's thesis
*Covering properties of lattice polytopes* was located through its
[institutional record](https://refubium.fu-berlin.de/handle/fub188/26773), but
direct retrieval failed; its full contents remain unaudited. The search did
not exhaust theses, unpublished calculations, alternate contact coordinates,
or all papers on interval verification. No author was contacted.

Safe description: **proposed explicit 17/5 bounds for two specified real
tetrahedral contact classes, following the ACMS finite-case programme and using
standard bilinear relaxations; no equivalent result found in this bounded
audit, with priority and proof validation treated as separate questions.**
No first, best, optimal, or global-flatness breakthrough claim follows from
this literature audit.
