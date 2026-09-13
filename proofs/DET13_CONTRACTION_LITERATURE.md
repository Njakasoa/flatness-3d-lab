# Literature audit: the index-13 two-vector contraction bound

Date: 2026-09-13. Bounded independent primary-source audit; ten search queries,
followed by direct inspection of the relevant papers. This document assesses
antecedents, not the correctness of the proposed proof.

## Candidate and present status

The candidate statement is that every full-dimensional compact hollow real
tetrahedron containing an affine unimodular image of

\[
P=\operatorname{conv}(0,(13,1,5),e_2,e_3)
\]

has lattice width at most

\[
C_{13}=\frac{1+13A}{9}=\frac{14+26/\sqrt3}{9},
\qquad A=1+2/\sqrt3.
\]

The proposed proof uses the two lattice vectors `(2,0,1)` and `(3,0,1)`,
whose barycentric difference vectors in this ordered tetrahedron are
`(-3,2,-2,3)/13` and `(2,3,-3,-2)/13`. The point being audited is the
explicit combination of their four distinct sign codes, a quantitative
permutation approximation of a nonnegative column-stochastic matrix, and
the resulting width bound. The proposed statement does not require that
the four contained lattice points be facet contacts.

No matching index-13 exclusion or identical bound was located in the sources
inspected below. This is **not evidence sufficient to establish novelty**.
The general ingredients have established antecedents, and the proof needs
independent mathematical verification separately from this audit.

## Closest geometric source

Averkov, Codenotti, Macchia, and Santos, *A local maximizer for lattice width
of 3-dimensional hollow bodies*, [arXiv:1907.06199, PDF](https://arxiv.org/pdf/1907.06199),
published in *Discrete Applied Mathematics* 298 (2021), 129–142,
[publisher record](https://doi.org/10.1016/j.dam.2021.04.009).
Page references here use the 22-page arXiv PDF.

- Lemma 5.1, equation (14), p. 18, gives
  `lambda_1(K-K) >= 1 - A/w(K)` for hollow three-dimensional convex bodies.
  This is the direct antecedent of the lower bound on the two gauges.
- Section 5.1, p. 17, attributes the underlying covering-minima inequalities
  to Kannan–Lovász and the planar constant to Hurkens. This component must
  not be described as newly proved here.
- Section 5.3 and Theorem 5.4, pp. 19–20, establish the method of considering
  inscribed empty lattice polytopes and bound the normalized volume of an
  inscribed tetrahedron in a width maximizer by 17. That bound alone permits
  normalized volume 13.
- The closing discussion, pp. 20–21, proposes finite case analysis for the
  possible inscribed polytopes. It does not enumerate or exclude the specific
  index-13 case by the proposed two-vector contraction argument.

The candidate fits this established case-analysis programme. The potential
contribution is a quantitative elimination of one specified containment class,
not the finite-reduction principle itself.

## Codenotti–Santos construction and subsequent context

Codenotti and Santos, *Hollow polytopes of large width*,
[arXiv:1812.00916, PDF](https://arxiv.org/pdf/1812.00916), published in
*Proceedings of the American Mathematical Society* 148 (2020), 835–850.
Section 5, particularly Theorem 5.1 on p. 9 of the inspected 15-page arXiv
PDF, treats a specific parameterized family and obtains width `2+sqrt(2)`.
Its equality analysis lists seven minimizing directions up to sign. This is
the benchmark construction, not a general theorem about tetrahedra containing
the index-13 polytope. No such containment theorem was located in this paper.
The theorem numbering differs from the citation in the ACMS bibliography;
the page and arXiv version above identify the statement actually inspected.

Codenotti's [author publication list](https://codenotti.github.io/papers.html)
was checked as a discovery source. It lists the ACMS article, the original
construction, and *Lattice reduced and complete convex bodies* (2024).
The latter's [publisher abstract and introductory discussion](https://londmathsoc.onlinelibrary.wiley.com/doi/abs/10.1112/jlms.12982)
still describe the dimension-three global value as open and the ACMS result
as local optimality. These contextual observations neither prove nor disprove
priority for the present specific containment bound.

## Established stochastic-matrix machinery

Gaubert and Qu, *Dobrushin ergodicity coefficient for Markov operators on
cones, and beyond*, [arXiv:1302.5226, PDF](https://arxiv.org/pdf/1302.5226).
Theorem 1.1, on the third PDF page of the inspected 30-page version, identifies
the operator norm for Hopf oscillation. In the stochastic-matrix setting,
the discussion immediately following it gives the familiar half row-distance
formula and its equivalence with the Dobrushin coefficient. The oscillation
seminorm is `max(x_i)-min(x_i)`; transpose conventions must be respected when
applying it to a column-stochastic matrix.

Thus oscillation/total-variation duality and stochastic contraction are
classical tools. A near-identity inverse estimate following from a bound on
the perturbation operator is likewise not an adequate novelty claim by itself.
The particular index-13 sign-code certificate, constants, and lattice-width
consequence were not found in this source. A distinction between a contraction
upper bound and the inverse lower bound required here is essential; merely
citing Dobrushin's coefficient does not verify the proposed proof.

## Search record and limits

The ten query strings were:

1. `"flatness" "tetrahedron" "13"`
2. `"Codenotti" "Santos" "three" "flatness"`
3. `"Averkov" "Codenotti" "Macchia" "Santos" lattice free tetrahedron`
4. `"hollow tetrahedra" "13" width`
5. `"lattice width" "stochastic" tetrahedron`
6. `"Hollow polytopes" "Codenotti" "Santos"`
7. `"lattice" "tetrahedron" "13" "width maximizer"`
8. `"stochastic matrices" "near" "permutation" "norm" contraction`
9. `"Dobrushin" "oscillation" "stochastic" coefficient Gaubert Qu`
10. `"flatness" "13" "tetrahedra" "stochastic"`

Many exact-keyword results were irrelevant; absence from them carries little
weight. Secondary reposts and unrelated matrix papers were not used as
mathematical authorities. A direct attempt to retrieve Codenotti's thesis
from the institutional repository met an anti-bot page, so its complete
contents were not audited. This search is not exhaustive across alternate
unimodular coordinates, unpublished work, theses, or equivalent constants.

Safe current description: **a proposed explicit index-13 containment bound,
derived using the ACMS gauge inequality and standard matrix-norm methods;
no matching result found in this bounded audit; priority unconfirmed.**


## Determinant-10 extension: limited follow-up

The parameterized proof subsequently gave (21+40/sqrt(3))/13 for the
configuration conv(0,(10,1,3),e2,e3). Three additional root queries were
`"lattice width" "tetrahedron" "10" "contact"`,
`"hollow" tetrahedron "21" "40" width`, and
`"flatness" "two" "short vectors" tetrahedra`. They returned mostly
irrelevant results and the institutional Codenotti thesis record already
noted above. This is a limited negative search, not an exhaustive audit of
that corollary or an assertion of priority. The mathematical inputs and
antecedents are the same as in the parameterized proof.
