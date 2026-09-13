# Novelty audit for the necessary contact-hull list

**Audit date:** 2026-09-13.  **Cut-off:** primary preprints and publisher
records available on that date.  **Scope:** the proposed contact-hull
reduction above
\(c=(11/7)(1+2/\sqrt3)=3.38595798888\ldots\), including the exact
tetrahedral \(\lambda _1(P-P)\) screening, the planar diamond inequality,
and the nonsimplicial extension enumeration.  This is a bounded literature
audit, not a priority determination and not permission to publish a novelty
claim.

## Conservative verdict

The closest actual prior result is Averkov--Codenotti--Macchia--Santos
(ACMS), Theorem 5.4.  ACMS already prove the finite contact-hull principle
for a width maximizer: the inscribed empty lattice polytope is either the
unimodular square or a three-dimensional empty lattice polytope of volume at
most \(22/3\), with the tetrahedral branch bounded by volume \(17/6\).
They invoke Howe's theorem, cited through Scarf, that every empty lattice
3-polytope has width one.  They do not give the threshold \(c\), the ten
tetrahedral survivors, the counts

\[
  1,\quad 10,\quad 11,22,10,9,
\]

or a table of fixed-contact difference-body minima.  The finite principle and
its standard maximality ingredients are therefore **known** and must not be
presented as the contribution of this project.

The internal computation is a plausible candidate refinement.  At the stated
threshold it reports one planar square, ten tetrahedra, and
\(11+22+10+9=52\) empty nonsimplicial hulls, for 63 necessary hull types in
total.  The current internal review also finds a stronger organization: all
52 nonsimplicial classes are hulls of vertex subsets of nine eight-vertex
empty templates, and the noncoplanar four-vertex subsets give the ten
tetrahedral classes while coplanar four-vertex subsets give the square branch.
This nine-template/subconfiguration statement is an internal enumeration
observation; the certificate mapping is being finalized separately.  It is
not claimed as a theorem of the cited literature.

No checked primary source explicitly reports the 63 counts, the nine bounded
templates, the ten threshold survivors, or the values of
\(\lambda _1(P-P)\) for this contact-hull problem.  The safe status is
therefore **candidate unreported computational refinement, novelty
unverified**.  The planar inequality
\(N\lambda _1(P-P)^2\leq2\) is an elementary consequence of the known
two-layer structure and planar Minkowski's theorem as written in
[`CONTACT_OBSTRUCTION_REDUCTION.md`](CONTACT_OBSTRUCTION_REDUCTION.md).  No
source was found stating this exact inequality in this contact-hull
application, so it should be called an internal derivation until a wider
priority search is done.  It does not by itself improve the global
three-dimensional flatness bound.

The computation is internally coherent with the reduction notes and the
exact data files, subject to the validation caveats in
[`CONTACT_REDUCTION_REVIEW.md`](../results/CONTACT_REDUCTION_REVIEW.md): it
classifies necessary lattice contact hulls, not all real maximal hollow
bodies and not hulls that are known to be realized above \(c\).  No claim
that \(\operatorname{Flt}(3)=2+\sqrt2\) follows.

## What is established internally

The two reduction notes give the following chain.  A compact hollow body of
width greater than \(c\) can be enlarged to a bounded maximal hollow
extension; blocked facets supply lattice contacts.  A hull of one selected
contact from each facet is empty, has at most eight vertices by the parity
midpoint argument, and is either the planar unimodular square or a full
dimensional empty 3-polytope.  Howe--Scarf width one puts every
full-dimensional empty hull in two lattice layers.  For an empty tetrahedron
with two vertices in each layer, the zero-height section of its difference
body is the diamond \(\operatorname{conv}(\pm u,\pm s)\) of area \(2N\),
where \(N=6\operatorname{vol}(P)\).  Minkowski's first theorem gives

\[
             N\,\lambda _1(P-P)^2\leq 2.                 \tag{A}
\]

Together with the ACMS containment inequality this leaves ten tetrahedral
possibilities at the strict threshold \(w(K)>11A/7\), where
\(A=1+2/\sqrt3\):

| \(N=6\operatorname{vol}(P)\) | White parameter \(a\) | \(\lambda _1(P-P)\) |
|---:|---:|---:|
| 1 | unimodular | 1 |
| 2 | 1 | 1 |
| 3 | 1 | \(2/3\) |
| 4 | 1 | \(1/2\) |
| 5 | 1 | \(2/5\) |
| 5 | 2 | \(3/5\) |
| 7 | 2 | \(3/7\) |
| 8 | 3 | \(1/2\) |
| 10 | 3 | \(2/5\) |
| 13 | 5 | \(5/13\) |

The determinant-11 row \((N,a,\lambda _1)=(11,3,4/11)\) is at equality
and is excluded only for the strict inequality \(w(K)>11A/7\).  The exact
enumeration through determinant 21 and the independent minimum calculation
are recorded in
[`CONTACT_OBSTRUCTION_REDUCTION.md`](CONTACT_OBSTRUCTION_REDUCTION.md),
[`empty_contact_tetrahedra.json`](../results/empty_contact_tetrahedra.json),
and
[`contact_minima_independent.json`](../results/contact_minima_independent.json).

For five or more vertices, the internal argument normalizes a unimodular
frame, uses the ten tetrahedral possibilities to bound every further contact
coordinate, and exhaustively extends from five to eight vertices.  The
reported class counts are 11, 22, 10, and 9.  The files
[`CONTACT_HULL_FINITE_REDUCTION.md`](CONTACT_HULL_FINITE_REDUCTION.md),
[`contact_extensions.json`](../results/contact_extensions.json), and
[`contact_hull_obstructions.json`](../certificates/contact_hull_obstructions.json)
contain the current statement and data.  These are exact integer checks, but
their mathematical priority is a separate question.

The nine-template compression fits the known Cayley picture.  Howe's theorem
is commonly stated as saying that an empty 3-polytope is contained in a
width-one two-layer lattice polytope whose layer sections contain unimodular
parallelograms; equivalently, it admits a two-layer Cayley completion.  After
fixing one layer, the other layer is described by relative
\(\mathrm{SL}_2(\mathbb Z)\) data.  This two-layer/Cayley structure is known;
the bounded nine-template list after the present \(\lambda _1\) screening is
the part for which no matching published count was located.

## Claim-by-claim literature status

| Internal statement | Status after this audit | Reason and closest source |
|---|---|---|
| Maximal hollow extension and relative-interior facet blockers | **Known framework; details must be cited** | Lovász's blocked-facet theorem, recalled as ACMS Proposition 5.3; Averkov's proof is also available at [arXiv:1110.1014](https://arxiv.org/abs/1110.1014). |
| At most eight contact vertices by parity | **Elementary known argument** | Equal residues modulo 2 give an integer midpoint; no novelty should be claimed. |
| Empty planar contact branch is the unimodular square | **Known** | ACMS Theorem 5.4 and the standard empty-polygon argument. |
| Every empty lattice 3-polytope has width one / two-layer Cayley form | **Known** | Howe's theorem as cited by Scarf and ACMS; see [Scarf, *Integral Polyhedra in Three Space*](https://doi.org/10.1287/moor.10.3.403) and [Treutlein, arXiv:0809.1787](https://arxiv.org/abs/0809.1787). |
| ACMS volume and tetrahedral cutoffs | **Known** | [ACMS, arXiv:1907.06199](https://arxiv.org/abs/1907.06199), Theorem 5.4; this is the closest prior result. |
| Planar diamond inequality (A) | **Internally derived; priority unknown** | Follows from the known two-layer form plus planar Minkowski; no checked source states this exact contact-hull refinement. |
| Ten tetrahedral types surviving \(\lambda _1>4/11\) | **Candidate unreported exact refinement** | White gives the infinite empty-tetrahedron normal form; ACMS gives only the coarse determinant bound. No checked source gives this ten-row table. |
| Exact \(\lambda _1(P-P)\) values and 27 exclusions | **Candidate unreported computation** | ACMS uses \(\lambda _1\) symbolically and does not tabulate the 37 determinant-\(\leq17\) classes or their minima. White, Scarf, and Hamm study related lattice tetrahedra but not this table. |
| Nine eight-vertex templates and all 63 subconfiguration counts | **Candidate unreported enumeration; certificate-dependent** | No checked source gives the threshold-restricted template count or the 1/10/11/22/10/9 breakdown. Known Cayley structure means the finite search setup is not itself novel. |
| Fixed-contact continuous optimization for these hulls | **Open in this project and absent from checked sources** | ACMS says fixed full-dimensional cases are decidable in principle by real algebra but too large for direct quantifier elimination; the square branch remains open. |
| Global equality \(\operatorname{Flt}(3)=2+\sqrt2\) | **Still conjectural** | [Codenotti--Santos, arXiv:1812.00916](https://arxiv.org/abs/1812.00916), ACMS, and the later status papers below do not settle it. |

## Primary-source audit

### The finite-reduction and width-one sources

* **ACMS (2019 preprint, 2021 publication).** The paper proves local
  maximality of the Codenotti--Santos tetrahedron, gives the strict upper
  bound below 3.972, and proves Theorem 5.4.  The theorem says square or
  empty 3-polytope of volume at most \(22/3\), and tetrahedron of volume at
  most \(17/6\).  Section 5 says this leaves finitely many fixed-\(P\) cases,
  but it does not enumerate them.  Primary records:
  [arXiv](https://arxiv.org/abs/1907.06199),
  [publisher article](https://doi.org/10.1016/j.dam.2021.04.009), and the
  [ScienceDirect text](https://www.sciencedirect.com/science/article/pii/S0166218X21001529).

* **Scarf (1985), reporting Howe's theorem.** The primary article is
  [*Integral Polyhedra in Three Space*](https://doi.org/10.1287/moor.10.3.403).
  Its abstract identifies the unpublished Howe theorem used for the
  three-dimensional analysis.  ACMS explicitly invokes that theorem for
  empty 3-polytopes.  This establishes the width-one/Cayley ingredient, not
  the bounded nine-template enumeration.

* **White (1964).** [*Lattice Tetrahedra*](https://doi.org/10.4153/CJM-1964-040-2)
  gives the classical classification of empty lattice tetrahedra.  It leaves
  an infinite parameter family, so it is the right source for the normal form
  but not a source for the ten rows selected by the present difference-body
  minimum.

* **Codenotti--Santos (2018 preprint, 2020 publication).** [*Hollow
  Polytopes of Large Width*](https://arxiv.org/abs/1812.00916) supplies the
  (2+\sqrt2) hollow tetrahedron and the global conjecture.  Its symmetric
  family and width certificate do not enumerate integral blocker hulls or
  their fixed-contact minima.

* **Treutlein (2008).** [*3-Dimensional Lattice Polytopes Without Interior
  Lattice Points*](https://arxiv.org/abs/0809.1787) states Howe's Cayley
  formulation for empty 3-polytopes.  It concerns the broad structural
  classification, not the contact-hull threshold or fixed minima.

### Adjacent exact classifications of lattice 3-polytopes

These papers were checked because a six-to-eight-vertex empty contact hull
could be confused with a classification by the total number of lattice
points.  They are relevant nearby results, but their equivalence classes and
invariants are different from the present selected-blocker hulls.

* [Blanco--Santos, *Lattice 3-polytopes with few lattice points*,
  arXiv:1409.6701](https://arxiv.org/abs/1409.6701) classifies the five-lattice-
  point case: nine width-two classes and no larger width, alongside infinite
  width-one families.  It does not state the 63 contact-hull counts.
* [Blanco--Santos, *Lattice 3-polytopes with six lattice points*,
  arXiv:1501.01055](https://arxiv.org/abs/1501.01055) classifies the 76
  width-greater-than-one classes and the width-one six-point classes.  Its
  objects include all lattice points of the polytope; a blocker hull records
  selected facet contacts and can have a different lattice-point census.
* [Blanco--Santos, *Non-spanning lattice 3-polytopes*,
  arXiv:1711.07603](https://arxiv.org/abs/1711.07603) gives a complete
  classification of non-spanning 3-polytopes and the two-layer descriptions
  of their lattice points.  It does not compute the present \(\lambda _1\)
  threshold or contact-hull orbit counts.
* [Alajmi--Soprunova, *Lattice Size of Width One Lattice Polytopes in
  \(\mathbb R^3\)*, arXiv:2207.13124](https://arxiv.org/abs/2207.13124)
  supplies an algorithm for lattice size of empty width-one polytopes.  The
  lattice-size invariant is not \(\lambda _1(P-P)\), and no contact list is
  given.

The AWW/AKW classifications of integral maximal lattice-free polyhedra are
also adjacent but do not subsume this result:
[AWW, arXiv:1010.1077](https://arxiv.org/abs/1010.1077) and
[AKW, arXiv:1509.05200](https://arxiv.org/abs/1509.05200).  Those papers
classify integral polyhedra and their maximality notions.  The present
contact hulls come from real maximal hollow bodies and do not impose integer
facet normals.

### 2024--2026 status check

* [Codenotti--Freyer, *Lattice Reduced and Complete Convex Bodies*,
  arXiv:2307.09429](https://arxiv.org/abs/2307.09429) proves attainment and
  structural reductions, but no contact-hull orbit list or fixed minima.
* [Doolittle--Katthän--Nill--Santos, *Empty simplices of large width*,
  arXiv:2103.14925](https://arxiv.org/abs/2103.14925), published in 2025,
  studies high-dimensional empty simplices and repeats the unresolved
  three-dimensional Codenotti--Santos context.  It does not enumerate the
  determinant-\(\leq17\) contact tetrahedra or the 63 hulls.
* [Hamm, *Classification of Width 1 Lattice Tetrahedra by Their Multi-Width*,
  arXiv:2304.03627](https://arxiv.org/abs/2304.03627), published in 2025,
  classifies integral tetrahedra by multi-width.  That invariant and object
  class do not give the present difference-body-minimum table or the real
  fixed-contact optimization.
* [Averkov--Codenotti--Freyer--Huang, arXiv:2604.27260](https://arxiv.org/abs/2604.27260)
  proves a planar one-interior-point flatness value.  It is a different
  parameterized problem and does not update the classical \(\operatorname{Flt}(3)\)
  question.

No checked 2025--2026 primary source changes the status

\[
  2+\sqrt2\leq \operatorname{Flt}(3)<3.972,
  \qquad \operatorname{Flt}(3)=2+\sqrt2\text{ conjectural}.
\]

## Search log

The web search used the following exact queries on 2026-09-13.  Search-result
pages were used only to find a primary arXiv or publisher record; statements
above were checked against that primary record.

| Query | Primary records opened | Purpose |
|---|---|---|
| `site:arxiv.org 1907.06199 Averkov Codenotti Macchia Santos Theorem 5.4 contact polytope` | [ACMS arXiv:1907.06199](https://arxiv.org/abs/1907.06199), [publisher text](https://www.sciencedirect.com/science/article/pii/S0166218X21001529) | Verify the exact finite-reduction theorem and whether the 63 classes were listed. |
| `site:arxiv.org empty lattice 3-polytope width one Howe Scarf theorem` | [Treutlein arXiv:0809.1787](https://arxiv.org/abs/0809.1787), [Scarf DOI](https://doi.org/10.1287/moor.10.3.403) | Check the width-one/Cayley theorem and its provenance. |
| `site:arxiv.org "contact polytope" hollow lattice width tetrahedron` | [ACMS arXiv:1907.06199](https://arxiv.org/abs/1907.06199) | Search for the contact-hull terminology and fixed-contact lists. |
| `"63" "contact" lattice polytope hollow` | ACMS and adjacent lattice-polytope records | Search for the exact count. No matching primary result was found. |
| `"11/7" "lattice width" hollow` | ACMS and flatness records | Search for the exact threshold. No matching contact-hull publication was found. |
| `"empty lattice polytope" "five" "six" "seven" "eight" vertices dimension 3 classification` | [Blanco--Santos arXiv:1409.6701](https://arxiv.org/abs/1409.6701), [arXiv:1501.01055](https://arxiv.org/abs/1501.01055), [arXiv:1711.07603](https://arxiv.org/abs/1711.07603) | Check nearby enumerations by size, lattice-point census, and spanning type. |
| `"unimodular frame" "empty lattice polytope" three dimensions` | [Treutlein arXiv:0809.1787](https://arxiv.org/abs/0809.1787), Howe/Scarf references | Check whether the frame normalization or two-layer template count was already stated. |
| `Scarf Integral polyhedra in three space Math Operations Research 1985 DOI` | [Scarf publisher page](https://pubsonline.informs.org/doi/10.1287/moor.10.3.403) | Verify the primary Howe/Scarf source. |
| `site:arxiv.org 2025 2026 lattice width empty 3-polytope flatness constant` | [Doolittle et al.](https://arxiv.org/abs/2103.14925), [Hamm](https://arxiv.org/abs/2304.03627), [Averkov et al.](https://arxiv.org/abs/2604.27260), [Codenotti--Freyer](https://arxiv.org/abs/2307.09429) | Check recent work for an update or a matching finite list. |
| `"successive minima" "empty lattice tetrahedra" difference body` | ACMS, White, Hamm, and related arXiv records | Search for a published fixed-\(P\) \(\lambda _1(P-P)\) table. No matching table was found. |

The search did not include a full MathSciNet, zbMATH, thesis, citation-graph,
or unpublished-manuscript crawl. It therefore supplies bounded negative
evidence only. In particular, “not found in this audit” must not be converted
into “new” or “no prior work exists.”

## Safe wording for downstream use

The following wording is supportable after this audit:

> Conditional on the stated maximal-extension and exact-enumeration proofs,
> the project has an internally checked candidate list of 63 necessary
> contact-hull types above \(c=11(1+2/\sqrt3)/7\).  The list appears to be an
> unreported refinement of the finite search principle in ACMS Theorem 5.4;
> its priority and publication-level completeness have not been established.

The following should be avoided until a broader priority check and final
certificate review:

* “This is the first classification of empty lattice 3-polytopes.”
* “The finite contact reduction is new.”
* “The 63 types are all high-width realizers.”
* “The planar diamond inequality is a new theorem.”
* “The three-dimensional flatness conjecture is proved.”

No author contact, publication, or external release is part of this audit.
