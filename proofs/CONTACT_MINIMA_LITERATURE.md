# Exact successive-minimum audit for the 37 contact tetrahedra

**Cut-off:** 2026-09-13. **Scope:** the 37 closed-empty lattice tetrahedra in
[results/empty_contact_tetrahedra.json](../results/empty_contact_tetrahedra.json),
with normalized determinant \(D\leq17\). This is a fixed-\(P\) calculation in
the tetrahedral branch of ACMS Theorem 5.4. It is not a classification of
maximal hollow bodies and does not address the square or nonsimplicial branches.

## Result

Put
\[
 A=1+\frac2{\sqrt3},\qquad w_0=2+\sqrt2,\qquad
 \alpha=1-\frac{A}{w_0}=0.368902823735\ldots.
\]
ACMS Lemma 5.1 gives
\[
 1\leq \frac{A}{w(K)}+\lambda_1(K-K).
\]
If \(P\subseteq K\), then \(P-P\subseteq K-K\), so monotonicity of successive
minima gives
\[
 \lambda_1(K-K)\leq\lambda_1(P-P)=:\ell(P).
\]
Thus \(w(K)\geq w_0\) forces \(\ell(P)\geq\alpha\). The independent exact
calculation leaves precisely these ten source class ids:
\[
 \boxed{\{0,1,2,3,4,5,8,10,14,23\}}.
\]
The surviving \((D,a,\ell)\) values are
\[
 (1,0,1),(2,1,1),(3,1,\tfrac23),(4,1,\tfrac12),
 (5,1,\tfrac25),(5,2,\tfrac35),(7,2,\tfrac37),
 (8,3,\tfrac12),(10,3,\tfrac25),(13,5,\tfrac5{13}).
\]
The other 27 classes have \(\ell<\alpha\), so no body of width at least
\(2+\sqrt2\) can contain any of them. The comparison is strict for every
rational value in the table; the certified alpha interval used was
\((0.368902823735021962,0.368902823735022342)\).

A useful weaker threshold gives an independent consistency check. If
\[
 w(K)>\frac32A=\frac32+\sqrt3,
\]
then \(\lambda_1(K-K)>1/3\), leaving eleven ids: the above ten plus id 17
(\(D=11,a=3,\ell=4/11\)). If
\(w(K)>\frac{11}{7}A\), then \(\lambda_1(K-K)>4/11\), and the strict
comparison removes id 17 again. These thresholds are below \(w_0\), so they
apply to any putative body with width at least \(w_0\).

Here is the complete value table. The 'a' column is the third coordinate in
the source representative \(P=\operatorname{conv}(0,(D,1,a),e_2,e_3)\).
The value \(\lambda_3=1\) holds for every row.

| id | D | a | ell | lambda2 | alpha test | >1/3 | >4/11 |
|---:|---:|---:|---:|---:|:---:|:---:|:---:|
| 0 | 1 | 0 | 1 | 1 | keep | yes | yes |
| 1 | 2 | 1 | 1 | 1 | keep | yes | yes |
| 2 | 3 | 1 | 2/3 | 1 | keep | yes | yes |
| 3 | 4 | 1 | 1/2 | 1 | keep | yes | yes |
| 4 | 5 | 1 | 2/5 | 1 | keep | yes | yes |
| 5 | 5 | 2 | 3/5 | 3/5 | keep | yes | yes |
| 6 | 6 | 1 | 1/3 | 1 | cut | no | no |
| 7 | 7 | 1 | 2/7 | 1 | cut | no | no |
| 8 | 7 | 2 | 3/7 | 4/7 | keep | yes | yes |
| 9 | 8 | 1 | 1/4 | 1 | cut | no | no |
| 10 | 8 | 3 | 1/2 | 1/2 | keep | yes | yes |
| 11 | 9 | 1 | 2/9 | 1 | cut | no | no |
| 12 | 9 | 2 | 1/3 | 5/9 | cut | no | no |
| 13 | 10 | 1 | 1/5 | 1 | cut | no | no |
| 14 | 10 | 3 | 2/5 | 2/5 | keep | yes | yes |
| 15 | 11 | 1 | 2/11 | 1 | cut | no | no |
| 16 | 11 | 2 | 3/11 | 6/11 | cut | no | no |
| 17 | 11 | 3 | 4/11 | 5/11 | cut | yes | no |
| 18 | 12 | 1 | 1/6 | 1 | cut | no | no |
| 19 | 12 | 5 | 1/3 | 1/2 | cut | no | no |
| 20 | 13 | 1 | 2/13 | 1 | cut | no | no |
| 21 | 13 | 2 | 3/13 | 7/13 | cut | no | no |
| 22 | 13 | 3 | 4/13 | 5/13 | cut | no | no |
| 23 | 13 | 5 | 5/13 | 5/13 | keep | yes | yes |
| 24 | 14 | 1 | 1/7 | 1 | cut | no | no |
| 25 | 14 | 3 | 2/7 | 3/7 | cut | no | no |
| 26 | 15 | 1 | 2/15 | 1 | cut | no | no |
| 27 | 15 | 2 | 1/5 | 8/15 | cut | no | no |
| 28 | 15 | 4 | 1/3 | 1/3 | cut | no | no |
| 29 | 16 | 1 | 1/8 | 1 | cut | no | no |
| 30 | 16 | 3 | 1/4 | 3/8 | cut | no | no |
| 31 | 16 | 7 | 1/4 | 1/2 | cut | no | no |
| 32 | 17 | 1 | 2/17 | 1 | cut | no | no |
| 33 | 17 | 2 | 3/17 | 9/17 | cut | no | no |
| 34 | 17 | 3 | 4/17 | 7/17 | cut | no | no |
| 35 | 17 | 4 | 5/17 | 5/17 | cut | no | no |
| 36 | 17 | 5 | 5/17 | 6/17 | cut | no | no |


The machine-readable witnesses, exact enumeration counts, and the exact
\(\lambda_2\) values are in
[results/contact_minima_independent.json](../results/contact_minima_independent.json).

## Independent exact derivation

Let
\[
 B=\begin{pmatrix}D&0&0\\1&1&0\\a&0&1\end{pmatrix},\qquad
 P=B\Delta_3,\qquad\Delta_3=\operatorname{conv}(0,e_1,e_2,e_3).
\]
For \(q=(q_1,q_2,q_3)\),
\[
 q\in\lambda(\Delta_3-\Delta_3)
 \ \Longleftrightarrow\
 \gamma(q):=\max\left\{\sum_i q_i^+,\sum_i q_i^-\right\}\leq\lambda,
\]
where \(q_i^+=\max(q_i,0)\) and \(q_i^-=\max(-q_i,0)\). Indeed, write
\(q=x-y\) with \(x,y\geq0\): the two simplex slack inequalities are
\(\sum x_i\leq\lambda\) and \(\sum y_i\leq\lambda\), and the positive and
negative parts give the minimum possible sums.

For \(z=(x,y,z_3)\in\mathbb Z^3\),
\[
 B^{-1}z=
 \left(\frac{x}{D},\,\frac{Dy-x}{D},\,\frac{Dz_3-ax}{D}\right).
\]
For \(D>1\), fix \(k=x\bmod D\), \(1\leq k<D\), and allow all integer shifts
of the three displayed barycentric coordinates. The first two residues are
opposite, while the third has residue \(-ak/D\). Choosing the smaller
representative on each pair gives the exact formula
\[
 \ell(P)=\frac1D\min_{1\leq k<D}
 \bigl(d_D(k)+d_D(ak\bmod D)\bigr),\qquad
 d_D(r)=\min(r,D-r).
 \tag{1}
\]
For \(D=1\), the integral coordinate vectors give \(\ell(P)=1\). This is an
exact minimization over the full lattice, not a short-vector numerical
search. As a finite cross-check, if \(\ell=m/D\leq1\), then
\(\gamma(B^{-1}z)\leq\ell\) implies
\[
 |x|\leq m,\quad |Dy-x|\leq m,\quad |Dz_3-ax|\leq m.
\]
Enumerating exactly those integer triples gives the witness and rank counts
recorded in the JSON.

The same rational gauge and exact rank test gives \(\lambda_2(P-P)\) and
\(\lambda_3(P-P)=1\). The latter also follows from the Howe--Scarf width-one
theorem for empty three-dimensional lattice polytopes, as used by ACMS.

## What the exact \lambda_2 calculation does and does not add

For a tetrahedron, Rogers--Shephard equality and Minkowski's second theorem
give
\[
 \frac{D}{6}=\operatorname{vol}(P)
 \leq \frac{2}{5\,\lambda_1(P-P)\lambda_2(P-P)}
 =\frac{2}{5\,\ell(P)\lambda_2(P-P)}.
 \tag{2}
\]
The exact \lambda_2 values are listed above. Substitution into (2) gives
strictly positive slack for all 37 rows; the smallest slack
\[
 \frac{2}{5\ell\lambda_2}-\frac{D}{6}=\frac1{15}
\]
occurs at id 1. It therefore yields no additional type elimination by itself.

Relative-interior blocked contacts do not reverse the containment monotonicity:
for \(P\subset K\),
\(\lambda_i(K-K)\leq\lambda_i(P-P)\). The ACMS contact condition says that
the chosen lattice points lie in relative interiors of facets of \(K\); it does
not supply a lower bound on \(\lambda_2(K-K)\) in terms of
\(\lambda_2(P-P)\). A stricter equality-case argument might use the location of
the minimizing decomposition in the facets of \(P\), but no such universal
strictness statement is used here. Accordingly, the only certified obstruction
from this audit is the exact \lambda_1 threshold.

There is, however, a useful determinant pre-cutoff independent of the table.
For \(D>1\), the numerator in (1) is the \ell_1-length of a nonzero point
in the rank-two congruence lattice
\[
 L_{D,a}=\{(r,s)\in\mathbb Z^2:s\equiv ar\pmod D\},
 \qquad \det L_{D,a}=D.
\]
The planar Minkowski diamond \(\{|r|+|s|\leq R\}\), of area \(2R^2\), gives a
nonzero lattice point with \(|r|+|s|\leq\sqrt{2D}\). Hence
\[
 \ell(P)\leq\sqrt{\frac2D}.
\]
Since \(\sqrt{2/15}<\alpha\), every \(D\geq15\) type is excluded before the
37-row exact check. This sharpens the ACMS coarse determinant cutoff \(D\leq17\)
to \(D\leq14\) for the width-\(w_0\) containment test. It is a statement about
these lattice tetrahedra \(P\), conditional on \(P\subset K\); it is not a
new universal flatness bound.

The same pre-cutoff has an orbit-free geometric proof. White's standard-form
theorem (equivalently the width-one theorem used by Howe--Scarf) puts an empty
three-dimensional lattice tetrahedron in two consecutive lattice layers. If
three vertices were in one layer and one in the other, the three coplanar
vertices would form an empty lattice triangle and hence a unimodular triangle;
the tetrahedron would then have \(D=1\). Thus, for \(D>1\), the layers have
two vertices each. In an affine lattice coordinate system write the four
vertices as
\[
 (0,0,0),\ (u,0),\ (v,1),\ (v+w,1),
 \qquad u,v,w\in\mathbb Z^2.
\]
Then \(D=|\det(u,w)|\), and the zero-layer section of the difference body is
\[
 (P-P)\cap(\mathbb R^2\times\{0\})=\operatorname{conv}(\pm u,\pm w),
 \qquad \operatorname{area}=2D.
\]
The planar Minkowski diamond theorem therefore supplies a nonzero planar
lattice vector in this section at scale at most \(\sqrt{2/D}\), proving the
same \(\ell(P)\leq\sqrt{2/D}\) bound without using the HNF list or the residue
formula. This is a structural check on the determinant pre-cutoff.

## Literature audit

ACMS, [arXiv:1907.06199](https://arxiv.org/abs/1907.06199), Section 5.1,
uses \lambda_1(K-K) in its hollow-body inequality, then uses
\lambda_2\geq\lambda_1 and \lambda_3(P-P)=1 in Theorem 5.4. Its
tetrahedral rounding is the coarse \(D\leq17\) bound. The paper says that
fixing one of finitely many contact polytopes leaves finitely many cases, but
does not enumerate these 37 tetrahedra or calculate their individual
\lambda_1(P-P) values. The exact formula (1), the 27 exclusions, and the
\(D\leq14\) pre-cutoff are therefore a refinement of that finite
calculation, not a claim that ACMS omitted a theorem.

The older primary sources checked for context are Codenotti--Santos,
[arXiv:1812.00916](https://arxiv.org/abs/1812.00916) (the
\(2+\sqrt2\) tetrahedron and conjecture), White's original
[*Lattice tetrahedra*](https://doi.org/10.4153/CJM-1964-040-2), and Scarf's
theorem as cited in ACMS. Neither computes this finite contact-minimum table.

The 2025--2026 primary-source check covered the following:

| Date | Primary source | Relevance to this audit |
|---|---|---|
| 2025 | Doolittle--Katthän--Nill--Santos, [Forum of Mathematics, Sigma](https://doi.org/10.1017/fms.2024.131), [arXiv:2103.14925](https://arxiv.org/abs/2103.14925) | Studies high-dimensional empty simplices and restates the 3D Codenotti--Santos conjectural context. It does not enumerate determinant-\(\leq17\) 3D contact tetrahedra or compute \(\lambda_1(P-P)\). |
| 2025 | Hamm, [Classification of width 1 lattice tetrahedra by their multi-width](https://doi.org/10.1007/s00454-024-00659-5), [arXiv:2304.03627](https://arxiv.org/abs/2304.03627) | Classifies integral tetrahedra by multi-width and gives algorithms for selected widths. Its invariant is not the exact \(P-P\) minimum for this ACMS contact list, and it does not address the real/algebraic fixed-contact optimization. |
| 2026 | Averkov--Codenotti--Freyer--Huang, [arXiv:2604.27260](https://arxiv.org/abs/2604.27260) | Proves the planar one-interior-point value \(\operatorname{Flt}(2,1)=3\), a different parameterized problem; it gives no update to classical \(\operatorname{Flt}(3)\) or this finite contact refinement. |
| 2024 (structural context) | Codenotti--Freyer, [arXiv:2307.09429](https://arxiv.org/abs/2307.09429) | Gives attainment and reduced-body structure, but no per-type \(P-P\) minima. |

The search used primary arXiv/publisher records and exact queries for
“flatness constant”, “lattice width”, “empty simplex”, “lattice tetrahedron”,
“successive minima”, and “difference body”. No checked 2025--2026 primary
source explicitly performs this determinant-\(\leq17\) \(P-P\) minima
refinement. This is bounded negative evidence, not a novelty guarantee.
No claim here upgrades the conjectural status
\(\operatorname{Flt}(3)=2+\sqrt2\).

## Reproducibility and limits

The JSON was generated with independent fractions.Fraction arithmetic and
the residue formula (1), without importing the lab's geometry or
enumeration modules. Every source class is represented; no class is silently
dropped. The result only says that a body containing one of the listed
tetrahedra cannot have width at least \(2+\sqrt2\) when its exact \ell is
below \alpha. The square branch, nonsimplicial branch, maximal-body
optimization, and boundary-strictness questions remain outside this audit.
