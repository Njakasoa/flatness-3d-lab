# Literature search log: 3D flatness and lattice-free contacts

**Search date:** 2026-09-13 (Indian/Antananarivo).  **Scope:** primary papers and publisher/preprint records relevant to the classical \(\operatorname{Flt}(3)\), the Codenotti--Santos tetrahedron, maximal lattice-free contacts, and 2025--2026 developments.

This is a reproducibility log for the audit in [`STATE_OF_THE_ART.md`](../STATE_OF_THE_ART.md).  It records the searches actually used and the claims checked.  It is not an exhaustive bibliography or a novelty guarantee.

## Search procedure

1. Start from the project brief’s claims \(2+\sqrt2\leq\operatorname{Flt}(3)<3.972\), the Codenotti--Santos name, and the ACMS acronym.
2. Search arXiv and publisher indexes by exact title, author pair, and numerical bound.
3. Open the primary preprint or publisher article, then inspect theorem statements and the relevant proof pages rather than relying on a secondary summary.
4. Search specifically for 2025 and 2026 records containing “flatness constant”, “lattice width”, “hollow”, “empty simplex”, “lattice tetrahedron”, and “maximal lattice-free polyhedron”.
5. Record negative evidence conservatively: “no classical \(\operatorname{Flt}(3)\) update located in this audit” is not “no such paper exists.”

## Query log

| Query / route | Primary source opened | Claim checked |
|---|---|---|
| `Codenotti Santos flatness constant dimension 3 tetrahedron 2+sqrt2 coordinates` | [Codenotti--Santos, arXiv:1812.00916](https://arxiv.org/abs/1812.00916) and [PDF](https://arxiv.org/pdf/1812.00916) | Theorem 1.1 lower bound; Section 5 family and coordinates; affine FCC lattice; path and vertical-line certificates; Conjecture 1.2 |
| `Averkov Codenotti Macchia Santos local maximizer 3.972` | [ACMS, arXiv:1907.06199](https://arxiv.org/abs/1907.06199) and [PDF](https://arxiv.org/pdf/1907.06199) | Theorems 1.2, 1.4, 5.2, 5.4; local result, radius 0.01307, strict upper bound, volume interval, inscribed-contact reduction, algebraic formulation |
| `maximal lattice-free real integral dimension 3 classification` | [Averkov--Krümpelmann--Weltge, arXiv:1509.05200](https://arxiv.org/abs/1509.05200) and [DOI](https://doi.org/10.1287/moor.2016.0836) | Definitions of \(\mathbb R^d\)- and \(\mathbb Z^d\)-maximality; equivalence in dimension 3 for integral polyhedra; twelve bounded + two unbounded classes |
| `maximal lattice-free polyhedra explicit description dimension three` | [Averkov--Wagner--Weismantel, arXiv:1010.1077](https://arxiv.org/abs/1010.1077) and [DOI](https://doi.org/10.1287/moor.1110.0510) | Original complete list of maximal lattice-free integral 3-polyhedra and rational-precision finiteness |
| `lattice reduced complete convex bodies flatness constant` | [Codenotti--Freyer, arXiv:2307.09429](https://arxiv.org/abs/2307.09429), [PDF](https://arxiv.org/pdf/2307.09429), and [DOI](https://doi.org/10.1112/jlms.12982) | Structural reduction; exact statement that all \(d>2\) values remain open; Proposition A.1 attainment of \(\operatorname{Flt}(d)\); reduced-simplex local theorem |
| `empty simplices large width 2025` | [Doolittle--Katthän--Nill--Santos, arXiv:2103.14925](https://arxiv.org/abs/2103.14925), [published PDF](https://www.cambridge.org/core/services/aop-cambridge-core/content/view/08EB9BD3CDF8AE894DF9B9491623CE28/S2050509424001312a.pdf), [DOI](https://doi.org/10.1017/fms.2024.131) | 2025 high-dimensional empty-simplex constructions; explicit restatement that C-S remains a conjecture and ACMS only proves local maximality |
| `classification width 1 lattice tetrahedra multi-width 2025` | [Hamm, arXiv:2304.03627](https://arxiv.org/abs/2304.03627), [Springer article](https://doi.org/10.1007/s00454-024-00659-5) | 2025 classification of integral lattice tetrahedra with multi-width \((1,w_2,w_3)\); algorithmic small width-2 extension; relevance and limits for non-lattice C-S candidate |
| `flatness constant 2026 one interior point` | [Averkov--Codenotti--Freyer--Huang, arXiv:2604.27260](https://arxiv.org/abs/2604.27260) | 2026 exact \(\operatorname{Flt}(2,1)=3\), a planar one-point variant; no claim about classical \(\operatorname{Flt}(3)\) |

## Evidence ledger

### Codenotti--Santos (2018 preprint; 2020 publication)

Primary record: [arXiv abstract](https://arxiv.org/abs/1812.00916).  The PDF gives:

* Theorem 1.1: a hollow non-lattice tetrahedron of width \(2+\sqrt2\).
* Section 5: \(\Lambda=\{(a,b,c):a,b,c\in1+2\mathbb Z,\ a+b+c\in1+4\mathbb Z\}\); the four algebraic vertices; the four facet contacts; the symmetric family \(\Delta(x,y,z)\).
* Theorem 5.1: within that family the width is at most \(2+\sqrt2\), with equality at the C-S parameter and its symmetry mate.
* The width certificate: seven antipodal classes (four diagonal and three coordinate classes), the finite vertical-line interval check for hollowness, and rational paths covering all remaining dual directions.
* Conjecture 1.2: the tetrahedron is the widest hollow 3-body.

The source’s Section 5 uses an affine face-centered-cubic lattice for symmetry.  The affine map recorded in `STATE_OF_THE_ART.md` sends the contact basis to the standard lattice and is a direct check that the normalization is legitimate.

### ACMS (2019 preprint; 2021 publication)

Primary record: [arXiv abstract](https://arxiv.org/abs/1907.06199), [full PDF](https://arxiv.org/pdf/1907.06199).  The abstract and introduction establish the lower-bound context and local theorem.  The checked statements are:

* Theorem 1.2: strict local maximizer among hollow tetrahedra.
* Corollary 1.3: strict local maximizer among hollow convex 3-bodies.
* Theorem 1.4: explicit contact perturbation neighborhood with barycentric distance threshold \(0.01307\).
* Theorem 5.2: for an attained width maximizer, width below \(3.972\) and volume in the reported numerical interval; the bound is an analytic inequality chain.
* Proposition 5.3: maximal hollow bodies have a lattice contact in the relative interior of each facet.
* Theorem 5.4: square or bounded-volume empty inscribed contact polytope; tetrahedral bound \(17/6\).
* The final paragraphs of Section 5: fixing a full-dimensional \(P\) gives a bounding region and a first-order real-algebra decision statement, but practical quantifier elimination is judged too slow/complex; the square branch remains open.

The ACMS volume theorem is stated for a **width maximizer**.  It should not be rewritten as a volume bound for every hollow body or every arbitrary counterexample candidate without an attainment/maximization argument.

### Maximality/classification sources

AKW define \(X\)-maximality by testing all points in \(X\setminus C\).  They prove \(\mathbb R^3\)- and \(\mathbb Z^3\)-maximality coincide for integral lattice-free polyhedra and state the consequence: exactly twelve bounded and two unbounded classes up to unimodular equivalence.  Their proof relies on the blocked-facet characterization of \(\mathbb R^3\)-maximality.  AWW is the earlier integral classification.

The scope distinction is essential:

* `R^3` in AKW means the set of allowed extension points, not “a polyhedron with rational/integer normals”.
* The C-S tetrahedron has algebraic vertices and irrational facet normals, while still having one lattice contact in each facet.
* AWW/AKW classify integral polyhedra.  They do not classify all real maximal hollow bodies or all algebraic contact realizations relevant to \(\operatorname{Flt}(3)\).

### 2024--2026 status checks

Codenotti--Freyer’s July 2024 version states that only dimensions 1 and 2 have known exact classical flatness constants, and its Appendix A proves existence of a realizer.  Doolittle et al. (published 2025) still describe C-S as a conjecture and ACMS as a local result.  Hamm (published online 2024, issue 2025) treats integral lattice tetrahedra and multi-width.  The 2026 Averkov--Codenotti--Freyer--Huang preprint proves a planar one-interior-point constant, not the classical 3D constant.  On this checked record, the safe status line as of the cut-off is still

\[
2+\sqrt2\leq\operatorname{Flt}(3)<3.972,
\qquad \operatorname{Flt}(3)=2+\sqrt2\text{ conjectural}.
\]

## Verification calculations recorded for reproducibility

1. The contact-basis map
   \[
   q_1=(x-y+z+1)/4,\quad q_2=(x+y-z+1)/4,\quad q_3=(-x+y+z+1)/4
   \]
   sends the four stated contacts to \(0,e_1,e_2,e_3\) and maps the affine lattice onto \(\mathbb Z^3\).
2. For the facet through \(a_2,a_3,a_4\), a cross product gives the normal \((3+2\sqrt2,1+\sqrt2,2+\sqrt2)\) and plane value \(-6-4\sqrt2\).  The coordinate ratios are irrational; an integer-normal shortcut is therefore invalid.
3. The seven width classes are counted modulo sign: 3 coordinate classes plus 4 diagonal classes.  If signs are counted separately, there are 14 functionals.

No code or generated data is being presented as a proof of the literature claims.  These are algebraic sanity checks for coordinate normalization and terminology.

## Search limitations and negative-result wording

* The audit used direct primary preprints/publisher records and exact-title queries; it did not crawl every journal index, thesis, or unpublished manuscript.
* “No 2025--2026 classical \(\operatorname{Flt}(3)\) update found” means no such update appeared in the checked search paths.  It does not prove nonexistence.
* Secondary pages were used only as discovery aids; numerical and theorem claims in the lab notes are tied to the primary sources above.
