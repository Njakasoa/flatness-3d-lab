# HNF completeness note for empty contact tetrahedra

**Run date:** 2026-09-13.  **Script:** [empty_tetrahedra.py](empty_tetrahedra.py).
**Output:** [empty_contact_tetrahedra.json](../results/empty_contact_tetrahedra.json).

This computation covers the tetrahedral inscribed-contact branch singled out
by ACMS Theorem 5.4.  It is a classification of empty **lattice tetrahedra**
of normalized determinant at most 17, modulo translation,
\(\mathrm{GL}_3(\mathbb Z)\), and vertex relabeling.  It is not a
classification of maximal lattice-free bodies, does not cover nonsimplicial
contact polytopes, and does not cover the ACMS square branch.

## Normal form and finite search

Translate one vertex to \(0\).  For the ordered remaining vertices, put their
vectors into the columns of \(B\).  The ordered
\(\mathrm{GL}_3(\mathbb Z)\)-orbit representative used by the script is

\[
H=\operatorname{HNF}(B^{\mathsf T})^{\mathsf T}
 =\begin{pmatrix}a&0&0\\ b&d&0\\ c&e&f\end{pmatrix},
\]

with

\[
a,d,f>0,\qquad 0\leq b,c<a,\qquad 0\leq e<d.
\]

This is the transpose of the standard column-HNF convention used by SymPy.
The three nonzero tetrahedron vertices are the columns of \(H\), and

\[
D=|\det H|=a d f=6\,\operatorname{vol}(P).
\]

For \(D\leq17\), the number of ordered HNF matrices is the finite sum

\[
\sum_{\substack{a,d,f\geq1\\adf\leq17}}a^2d=3268.
\]

The script enumerates exactly this sum.  For every HNF matrix it checks the
closed tetrahedron for lattice points.  If \(A=H\), \(D=\det A>0\), and
\(\operatorname{adj}(A)\) is the integer adjugate, then for an integer point
\(q\) the non-anchor barycentric numerators are
\(\operatorname{adj}(A)q\).  Thus

\[
q\in\operatorname{conv}(0,A_{\bullet1},A_{\bullet2},A_{\bullet3})
\Longleftrightarrow
\operatorname{adj}(A)q\geq0\text{ coordinatewise and }
\mathbf1^{\mathsf T}\operatorname{adj}(A)q\leq D.
\]

The bounding box is finite because the generated HNF columns have
nonnegative coordinates.  “Empty” in this computation means that the closed
tetrahedron contains exactly its four vertices as integer points; this is
stronger than checking only the relative interior and catches boundary lattice
points on edges and faces.

Finally, for each empty ordered HNF representative, the script takes the
lexicographic minimum of the same HNF construction over all \(4!=24\) choices
of anchor and order of the other vertices.  This removes vertex relabeling and
gives the reported unlabeled \(\mathrm{GL}_3(\mathbb Z)\)-classes.

## Reproduced result

The JSON output records every class, its HNF, vertices, and closed lattice
points.  The aggregate counts are:

| normalized determinant \(D\) | ordered HNF candidates | ordered empty HNFs | unlabeled classes |
|---:|---:|---:|---:|
| 1 | 1 | 1 | 1 |
| 2 | 7 | 1 | 1 |
| 3 | 13 | 3 | 1 |
| 4 | 35 | 3 | 1 |
| 5 | 31 | 9 | 2 |
| 6 | 91 | 3 | 1 |
| 7 | 57 | 15 | 2 |
| 8 | 155 | 9 | 2 |
| 9 | 130 | 15 | 2 |
| 10 | 217 | 9 | 2 |
| 11 | 133 | 27 | 3 |
| 12 | 455 | 9 | 2 |
| 13 | 183 | 33 | 4 |
| 14 | 399 | 15 | 2 |
| 15 | 403 | 21 | 3 |
| 16 | 651 | 21 | 3 |
| 17 | 307 | 45 | 5 |
| **total** | **3268** | **239** | **37** |

The class counts sum to 37.  In the chosen canonical representatives all 37
classes have diagonal HNF entries \((D,1,1)\); this is an output pattern, not
an assumption in the search.

## Independent sanity checks

The following checks were run after the enumeration.

1. The independent integer sum
   \(\sum_{adf\leq17}a^2d\) gives 3268, matching the generated HNF count.
2. For each of the 239 empty HNFs, lattice-point membership was recomputed
   with SymPy's exact rational matrix inverse rather than the script's integer
   adjugate test.  The two closed-point sets agreed for all 239 cases.
3. Every one of the 239 empty ordered HNFs was canonicalized over all 24
   vertex orders.  The resulting 37 keys were all nonempty-checking and
   idempotent: canonicalizing each representative again returned the same key.
4. Every JSON class has determinant equal to the product of its positive HNF
   diagonal entries and has exactly four listed closed lattice points.
5. The script was rerun from its default output path; it reproduced 3268
   ordered candidates, 239 ordered empty HNFs, and 37 unlabeled classes.

These are implementation checks, not an independent proof of the ACMS
theorem.  The HNF completeness argument applies to the finite tetrahedral
contact subclass only.

## Interpretation and limits

ACMS' determinant-\( \leq17 \) bound is conditional on \(P\) being the empty
tetrahedron selected from the blocked facets of an **attained width maximizer**
after maximal-body reduction.  It is not a determinant cutoff for every
hollow tetrahedron relevant to an arbitrary optimization.  Even a complete
HNF list leaves the fixed-\(P\) body optimization unresolved: facets may have
real or algebraic normals, contacts must lie in relative facet interiors, and
the width minimum ranges over all nonzero dual-lattice directions.  The square
and nonsimplicial branches remain outside this output.

Primary reduction source: [Averkov--Codenotti--Macchia--Santos, arXiv:1907.06199, Theorem 5.4](https://arxiv.org/abs/1907.06199).
