# State of the art: the three-dimensional flatness constant

**Cut-off:** 2026-09-13.  This is a primary-source audit, not a claim of exhaustive novelty.

## Current verdict

For the classical flatness constant

\[
 \operatorname{Flt}(3)=\sup\{w_{\mathbb Z^3}(K):K\subset\mathbb R^3
 \text{ is convex and }\operatorname{int}(K)\cap\mathbb Z^3=\varnothing\},
\]

the established range remains

\[
 \boxed{2+\sqrt2\ \leq\ \operatorname{Flt}(3)\ <\ 3.972}.
\]

The equality \(\operatorname{Flt}(3)=2+\sqrt2\) is still a conjecture.  Codenotti--Santos prove the lower bound with an explicit non-lattice tetrahedron.  Averkov--Codenotti--Macchia--Santos (ACMS) prove strict local maximality of that tetrahedron, give the published universal upper bound \(<3.972\), and reduce a putative global maximizer to finitely many inscribed-contact polytope cases.  They do not finish those cases.  Codenotti--Freyer prove that the supremum is attained, so it is legitimate to speak of a width maximizer when applying the ACMS reduction.

No 2025--2026 primary source located in this audit changes the classical three-dimensional range.  The recent papers checked below concern high-dimensional empty simplices, lattice-tetrahedron enumeration, or the planar one-interior-point variant.

## Definitions and normalization

For a full-dimensional convex body \(K\),

\[
 w_{\mathbb Z^3}(K)=\min_{u\in\mathbb Z^3\setminus\{0\}}
 \left(\max_{x\in K}u\cdot x-\min_{x\in K}u\cdot x\right).
\]

The same definition may be made for an affine lattice \(\Lambda\), using its dual lattice of functionals.  An affine change of coordinates taking \(\Lambda\) to \(\mathbb Z^3\) preserves the numerical width problem.  ACMS and Codenotti--Santos often keep a symmetric affine lattice instead of immediately converting it to \(\mathbb Z^3\).

The existence issue is settled in Codenotti--Freyer, Proposition A.1: for every full-dimensional lattice, some hollow convex body realizes \(\operatorname{Flt}(d)\).  This does not identify the realizer in dimension three.

## The Codenotti--Santos lower-bound tetrahedron

Codenotti--Santos, *Hollow polytopes of large width* (Proc. AMS 148 (2020), 835--850; [arXiv:1812.00916](https://arxiv.org/abs/1812.00916), Theorem 1.1 and Section 5), use

\[
\begin{aligned}
 a_1&=(2+\sqrt2,\sqrt2,2+\sqrt2),\\
 a_2&=(-\sqrt2,2+\sqrt2,-2-\sqrt2),\\
 a_3&=(-2-\sqrt2,-\sqrt2,2+\sqrt2),\\
 a_4&=(\sqrt2,-2-\sqrt2,-2-\sqrt2),
\end{aligned}
\qquad \Delta=\operatorname{conv}(a_1,a_2,a_3,a_4).
\]

The affine lattice is

\[
 \Lambda=\{(a,b,c):a,b,c\in1+2\mathbb Z,\ a+b+c\in1+4\mathbb Z\}.
\]

The four facet contacts are

\[
 p_1=(-1,-1,-1),\quad p_2=(1,-1,1),\quad
 p_3=(1,1,-1),\quad p_4=(-1,1,1),
\]

where \(p_i\) lies in the relative interior of the facet opposite \(a_i\).  They form an affine lattice basis.  A useful explicit lattice isomorphism to standard coordinates is

\[
 (x,y,z)\longmapsto
 \left(\frac{x-y+z+1}{4},\frac{x+y-z+1}{4},
 \frac{-x+y+z+1}{4}\right),
\]

which sends \(p_1\) to \(0\), and \(p_2,p_3,p_4\) to \(e_1,e_2,e_3\).

The width is exactly \(2+\sqrt2\):

* the seven antipodal classes of dual-lattice functionals
  \[
  \tfrac12(1,0,0),\ \tfrac12(0,1,0),\ \tfrac12(0,0,1),
  \quad \tfrac14(\pm1,\pm1,\pm1)
  \]
  (four diagonal classes, with signs identified up to negation) all have width \(2+\sqrt2\);
* hollowness is checked from the finite vertical-lattice-line interval certificate in Codenotti--Santos, Figure 3 and the proof of Theorem 5.1;
* the lower bound for every other dual-lattice functional is certified by their rational-path lemma.  They cover the open octants and the four non-pointed cones cut out by \(a=\pm b\), leaving only three exceptional directions, whose widths are computed directly.

Thus the source has fourteen signed functionals, or seven classes modulo sign.  Calling them “seven signed functionals” is inaccurate.

### Facet normals are not required to be integral

The contact points \(p_i\) are integral in the chosen affine lattice, but the facet planes of \(\Delta\) have algebraic, generally irrational normals.  For example, the facet through \(a_2,a_3,a_4\) and \(p_1\) has, up to a nonzero scalar, normal

\[
 n=(3+2\sqrt2,\ 1+\sqrt2,\ 2+\sqrt2),
 \qquad n\cdot x=-6-4\sqrt2.
\]

The ratios of the coordinates of \(n\) are irrational, so no integer normal represents this plane.  The correct real-maximality condition is that every facet is blocked by a lattice point in its relative interior; it is not a condition that facet normals be integer.  Any enumeration that silently restricts algebraic or real facets to integer normals changes the problem.

Codenotti--Santos conjecture that this tetrahedron is globally extremal:

\[
 \operatorname{Flt}(3)=2+\sqrt2.
\]

Their Theorem 5.1 proves the same value only inside the displayed symmetric two-parameter family \(\Delta(x,y,z)\), subject to its algebraic constraint.

## What ACMS proved

Primary source: Averkov, Codenotti, Macchia, Santos, *A local maximizer for lattice width of 3-dimensional hollow bodies*, Discrete Applied Mathematics 298 (2021), 129--142; [arXiv:1907.06199](https://arxiv.org/abs/1907.06199), [publisher page](https://doi.org/10.1016/j.dam.2021.04.009).

1. **Local theorem.** The Codenotti--Santos tetrahedron is a strict local maximizer among hollow tetrahedra (Theorem 1.2), and consequently among all hollow convex 3-bodies (Corollary 1.3). Their explicit tetrahedral neighborhood uses the facet-contact perturbation metric and gives radius \(0.01307\) in barycentric \(L_\infty\) coordinates (Theorem 1.4). This is a local statement, not a global upper bound.

2. **Published universal upper bound.** Their Theorem 5.2 gives, for a width maximizer \(K\),
   \[
   2+\sqrt2\leq w(K)<3.972,
   \qquad 2.653<\operatorname{vol}(K)<19.919
   \]
   (the paper states the rounded strict volume inequalities
   \(2.653<\operatorname{vol}(K)<19.919\), and rounds the lower width as
   \(3.414\) in the theorem statement).  The strict numerical upper bound
   comes from covering minima, Minkowski, Brunn--Minkowski, Rogers--Shephard
   and the three-dimensional symmetric Mahler inequality; it is not a
   computer-exhaustive search.

3. **Facet contacts.** By the Lovász maximal-lattice-free theorem, recalled as ACMS Proposition 5.3, a maximal hollow body is a polyhedron and every facet has a lattice point in its relative interior.  Picking one such contact from each facet gives an inscribed empty lattice polytope \(P\).

4. **Finite contact reduction (Theorem 5.4).** For a width maximizer \(K\), up to unimodular equivalence, an inscribed empty lattice polytope \(P\) is either
   * the square \(\operatorname{conv}(0,e_1,e_2,e_1+e_2)\), or
   * a full-dimensional empty lattice 3-polytope with ordinary volume \(\operatorname{vol}(P)\leq22/3\).

   If \(P\) is a tetrahedron, \(\operatorname{vol}(P)\leq17/6\).  Since \(6\operatorname{vol}(P)\) is an integer for a lattice 3-polytope, these are determinant bounds \(\leq44\) and, in the tetrahedral case, \(\leq17\).  ACMS explicitly state that this leaves finitely many fixed-\(P\) cases up to unimodular equivalence.  They do **not** enumerate all those cases or solve the resulting optimization.  The square is the only two-dimensional branch and is explicitly left open.

5. **Algebraic formulation.** With a fixed full-dimensional \(P\), the volume bound supplies a bounding region for \(K\).  Hollowness and width can then be expressed in first-order real algebra.  Quantifier elimination gives a theoretical decision procedure, but ACMS state that the resulting formulas are too complex and slow for practical use.  Their explicit local Hessian checks used SageMath exact arithmetic (about 14 hours on an 8 GB machine); that computation proves the local neighborhood, not the global conjecture.

## Real maximality versus integral maximality

Use the notation of Averkov--Krümpelmann--Weltge (AKW), *Notions of maximality for integral lattice-free polyhedra: the case of dimension three* (Math. Oper. Res. 42 (2017), 1035--1062; [arXiv:1509.05200](https://arxiv.org/abs/1509.05200), [DOI](https://doi.org/10.1287/moor.2016.0836)).  For \(X\subseteq\mathbb R^d\), an \(X\)-maximal lattice-free set admits no point \(x\in X\setminus C\) for which \(\operatorname{conv}(C\cup\{x\})\) remains lattice-free.

* \(\mathbb R^d\)-maximal means maximal against all real points.  This is the stronger geometric notion.  For a full-dimensional polyhedron it is equivalent to every facet being **blocked**, i.e. containing an integer point in its relative interior.  It does not require rational or integer facet normals.
* \(\mathbb Z^d\)-maximal is used for integral lattice-free polyhedra and tests only integral extensions.  It is weaker a priori.
* AKW prove that for integral polyhedra in dimension three the two notions coincide.  Combining this with Averkov--Wagner--Weismantel (AWW), *Maximal lattice-free polyhedra: finiteness and an explicit description in dimension three* (Math. Oper. Res. 36 (2011), 721--742; [arXiv:1010.1077](https://arxiv.org/abs/1010.1077), [DOI](https://doi.org/10.1287/moor.1110.0510)), gives exactly twelve bounded and two unbounded \(\mathbb Z^3\)-maximal integral polyhedra up to unimodular equivalence.  The unbounded representatives are \([0,1]\times\mathbb R^2\) and \(\operatorname{conv}(0,2e_1,2e_2)\times\mathbb R\).

This classification is **not** a classification of all real maximal hollow bodies, nor of the Codenotti--Santos algebraic tetrahedron.  The latter is a real maximality/contact problem with integral contacts and real facet normals.  Conflating the AWW/AKW integral list with all real/algebraic facet types is a category error.

## Sourced comparison table

| Dimension / class | Best established bound or value | Exact? | Main method | Classification / computer status | Remaining gap |
|---|---:|---|---|---|---|
| \(d=1\), all hollow convex bodies | \(\operatorname{Flt}(1)=1\) | Yes | Elementary one-dimensional layers | Complete | None |
| \(d=2\), all hollow convex bodies | \(\operatorname{Flt}(2)=1+2/\sqrt3\) | Yes | Hurkens’ exhaustive contact/maximal-body analysis | Unique realizer up to unimodular equivalence; exhaustive low-dimensional search | None for the classical planar constant |
| \(d=3\), all hollow convex bodies | \(2+\sqrt2\leq\operatorname{Flt}(3)<3.972\) | No | C-S explicit width certificate; ACMS geometric inequalities | Finitely many inscribed-contact cases for an attained maximizer, but not enumerated/solved | Prove the global upper bound \(\leq2+\sqrt2\) or find a counterexample |
| \(d=3\), C-S symmetric family \(\Delta(x,y,z)\) | Maximum \(2+\sqrt2\) at the displayed algebraic parameter values | Yes within this family | Two-parameter algebraic optimization plus path certificate | Family analyzed in C-S Theorem 5.1 | Extend beyond the family |
| \(d=3\), hollow tetrahedra near C-S | Strict local maximum at \(2+\sqrt2\); explicit radius \(0.01307\) | Local only | KKT conditions; exact polynomial inequalities; SageMath Hessian check | Local neighborhood certified; no global tetrahedral enumeration | Control all tetrahedra outside the neighborhood |
| \(d=3\), arbitrary hollow maximizer with inscribed empty \(P\) | \(P\) square or \(\operatorname{vol}(P)\leq22/3\); tetrahedral \(P\): \(\leq17/6\) | Reduction only | Lovász contacts, Howe width-one theorem, Minkowski/Rogers--Shephard bounds | Finite fixed-\(P\) reduction stated by ACMS; square branch open | Enumerate and solve every real-algebraic fixed-\(P\) optimization |
| \(d=3\), integral maximal lattice-free polyhedra | 12 bounded + 2 unbounded classes up to unimodular equivalence | Yes for this class | Blocked-facet geometry and finite integral enumeration | AWW list; AKW prove \(\mathbb R^3\)- and \(\mathbb Z^3\)-maximality coincide for integral polyhedra | Does not cover arbitrary real/algebraic facets |
| \(d=3\), lattice reduced bodies | Any lattice-reduced body has at most \(2^{4}-2=14\) vertices; width directions span dimension \(\Omega(\log3)\) | Structural only | Codenotti--Freyer reductions | General theorem; not a C-S global classification | Determine whether every Flt(3) realizer is reduced and exploit contacts |
| \(d\geq4\), empty lattice simplices (recent context) | 2025 constructions include width 11 in dimension 10 and asymptotic \(\geq d/\operatorname{arcsinh}(1)\approx1.1346d\) | Not an exact Flt(3) result | Cyclotomic/circulant constructions plus exhaustive computation in a bounded high-dimensional subfamily | Five width-11 dimension-10 cyclotomic examples found; none larger in the enumerated volume range | No direct implication for the 3D classical constant |

## 2025--2026 updates checked

* Doolittle--Katthän--Nill--Santos, *Empty simplices of large width*, Forum of Mathematics Sigma 13 (2025), e21 ([DOI](https://doi.org/10.1017/fms.2024.131), [arXiv:2103.14925](https://arxiv.org/abs/2103.14925)).  The paper explicitly restates the C-S conjecture and ACMS local result, while its new theorems concern empty simplices in dimensions at least four and asymptotic constructions.
* Hamm, *Classification of Width 1 Lattice Tetrahedra by Their Multi-Width*, Discrete & Computational Geometry 73 (2025), 859--885 ([DOI](https://doi.org/10.1007/s00454-024-00659-5), [arXiv:2304.03627](https://arxiv.org/abs/2304.03627)).  This classifies lattice tetrahedra of multi-width \((1,w_2,w_3)\) and gives a computational route for selected width-2 cases.  The objects are integral lattice tetrahedra, so they do not enumerate the non-lattice C-S candidate or the real-algebraic fixed-contact cases.
* Averkov--Codenotti--Freyer--Huang, *Exact Flatness Constant for One-Point Convex Bodies and the Discrete Isominwidth Problem: The Planar Case*, arXiv:2604.27260 (2026, v2) ([arXiv](https://arxiv.org/abs/2604.27260)).  It proves \(\operatorname{Flt}(2,1)=3\), a different parameterized planar problem.  It does not update classical \(\operatorname{Flt}(3)=\operatorname{Flt}(3,0)\).
* Codenotti--Freyer, *Lattice reduced and complete convex bodies*, JLMS 110 (2024), e12982 ([DOI](https://doi.org/10.1112/jlms.12982), [arXiv](https://arxiv.org/abs/2307.09429)).  This supplies the attainment theorem and general reduced-body structure; it does not determine \(\operatorname{Flt}(3)\).

## Claims to keep out of downstream notes

1. Write “conjectured equality,” never “proved equality,” for \(\operatorname{Flt}(3)=2+\sqrt2\).
2. Treat \(3.972\) as a strict published upper bound, not an attained value and not a numerical search cutoff.
3. State whether a volume is ordinary Euclidean volume with \(\det\mathbb Z^3=1\) or normalized determinant volume; ACMS’ \(22/3\) and \(17/6\) are ordinary volumes, so the corresponding determinant bounds are 44 and 17.
4. Keep the square inscribed-contact branch in any purported complete enumeration; ACMS explicitly leave it unresolved.
5. Do not turn the AWW/AKW list of integral maximal polyhedra into a list of all real/algebraic maximal bodies.
6. A lattice contact point in a facet does not make that facet rational.  The C-S candidate is an explicit counterexample to the shortcut “facet normal = integer vector.”

## Primary references

1. [Codenotti--Santos, *Hollow polytopes of large width*, arXiv:1812.00916](https://arxiv.org/abs/1812.00916).
2. [Averkov--Codenotti--Macchia--Santos, *A local maximizer for lattice width of 3-dimensional hollow bodies*, arXiv:1907.06199](https://arxiv.org/abs/1907.06199).
3. [Averkov--Wagner--Weismantel, *Maximal lattice-free polyhedra...*, arXiv:1010.1077](https://arxiv.org/abs/1010.1077).
4. [Averkov--Krümpelmann--Weltge, *Notions of maximality...*, arXiv:1509.05200](https://arxiv.org/abs/1509.05200).
5. [Codenotti--Freyer, *Lattice Reduced and Complete Convex Bodies*, arXiv:2307.09429](https://arxiv.org/abs/2307.09429).
6. [Doolittle--Katthän--Nill--Santos, *Empty simplices of large width*, arXiv:2103.14925](https://arxiv.org/abs/2103.14925).
7. [Hamm, *Classification of width 1 lattice tetrahedra by their multi-width*, arXiv:2304.03627](https://arxiv.org/abs/2304.03627).
8. [Averkov--Codenotti--Freyer--Huang, arXiv:2604.27260](https://arxiv.org/abs/2604.27260).
