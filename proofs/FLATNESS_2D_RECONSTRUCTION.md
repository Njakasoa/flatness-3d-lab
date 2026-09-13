# Hurkens’ planar extremal triangle

This note fixes an exact representative of the planar equality case and
separates its machine checked witness proof from the global theorem.  The
target value is

\[
  \operatorname{Flt}(2)=1+\frac{2}{\sqrt 3}
  =1+\frac{2\sqrt3}{3}.
\]

Here “hollow” means \(\operatorname{int}(K)\cap\mathbb Z^2=\varnothing\),
and the lattice width is

\[
 w(K)=\min_{u\in\mathbb Z^2\setminus\{0\}}
 \left(\max_{x\in K}u\cdot x-\min_{x\in K}u\cdot x\right).
\]

## Exact witness

Put \(s=\sqrt3\).  One convenient representative is

\[
\begin{aligned}
q_1&=\left(\frac23,-\frac{1+s}{3}\right),\\
q_2&=\left(-\frac{1+s}{3},\frac{2+s}{3}\right),\\
q_3&=\left(\frac{2+s}{3},\frac23\right),
\end{aligned}
\qquad
T=\operatorname{conv}\{q_1,q_2,q_3\}.
\]

The relative-interior contacts on the cyclic edges \(q_1q_2,q_2q_3,q_3q_1\)
are respectively

\[
c_{12}=(0,0),\qquad c_{23}=(0,1),\qquad c_{31}=(1,0),
\]

and, with \(\lambda=1/s=s/3\),

\[
c_{i,i+1}=\lambda q_i+(1-\lambda)q_{i+1}.
\]

The indexing in Averkov–Wagner’s statement of Hurkens’ theorem is shifted:
take \((Q_0,Q_1,Q_2)=(q_3,q_1,q_2)\).  Then

\[
p_i=\frac1{\sqrt3}Q_{i+1}
    +\left(1-\frac1{\sqrt3}\right)Q_{i+2}
\]

gives \(p_0=(0,0),p_1=(0,1),p_2=(1,0)\), exactly the equality condition in
the cited theorem.

The exact area is

\[
\operatorname{area}(T)=1+\frac{\sqrt3}{2}.
\]

The affine lattice symmetry

\[
U=\begin{pmatrix}0&1\\-1&-1\end{pmatrix},\qquad t=(0,1)
\]

satisfies \(U\in\mathrm{GL}_2(\mathbb Z)\), \(U^3=I\), and
\(Uq_1+t=q_2\), \(Uq_2+t=q_3\), \(Uq_3+t=q_1\).  Thus the three contacts and
the three vertices are cyclically permuted.  This is a lattice symmetry, not
an assertion that all Euclidean-looking permutations are lattice affine
automorphisms; the exact enumeration in the certificate finds three
automorphisms including the identity.

## Independent hollowness proof

Every coordinate of every point of \(T\) lies between the corresponding
coordinate extrema of the vertices.  The exact extrema are

\[
 -\frac{1+s}{3}>-1,
 \qquad
 \frac{2+s}{3}<2.
\]

Therefore an integer point in \(T\) can only have coordinates in
\(\{0,1\}^2\).  The three points \((0,0),(0,1),(1,0)\) are the contacts
displayed above, hence lie on the boundary.  For the remaining candidate,
the barycentric coordinates of \((1,1)\) with respect to \((q_1,q_2,q_3)\)
are

\[
\left(1-\frac{2s}{3},\;-1+\frac{2s}{3},\;1\right).
\]

The first coordinate is negative, so \((1,1)\notin T\).  Consequently
\(\operatorname{int}(T)\cap\mathbb Z^2=\varnothing\), and the boundary
integer points are exactly the three contacts.

`experiments/planar_control.py` repeats this argument with exact
\(\mathbb Q(\sqrt3)\) sign arithmetic and also calls the generic facet
classifier.  The resulting certificate checks the four points in
\([0,1]^2\), reports no interior point, and records one relative-interior
contact on every edge.

## Independent complete-width proof

For \(u=(a,b)\in\mathbb Z^2\), set

\[
B=3+2s,\qquad D=3+s.
\]

Three times the pairwise vertex differences evaluated at \(u\) are

\[
\begin{aligned}
L_{12}&=3(q_2-q_1)\cdot u=-Da+Bb,\\
L_{23}&=3(q_3-q_2)\cdot u=Ba-sb,\\
L_{31}&=3(q_1-q_3)\cdot u=-sa-Db.
\end{aligned}
\]

Since the width of a triangle in a direction is the largest absolute
pairwise vertex difference,

\[
 w(T,u)=\frac13\max\{|L_{12}|,|L_{23}|,|L_{31}|\}.
\]

The direction \(u=(1,0)\) already gives

\[
w(T,(1,0))=\frac{B}{3}=1+\frac{2}{\sqrt3}.
\]

It remains to exclude a smaller value in every other integer direction.  Let
\(W=B/3\) and suppose \(w(T,u)\le W\).  In particular,
\(|L_{23}|,|L_{31}|\le B\).  Solving

\[
\begin{pmatrix}B&-s\\-s&-D\end{pmatrix}
\binom a b=\binom{L_{23}}{L_{31}}
\]

uses the exact determinant magnitude

\[
\Delta=BD+s^2=18+9s=9(2+s).
\]

Hence

\[
 |a|\le\frac{B(D+s)}{\Delta}=\frac{B^2}{\Delta}
      =\frac{2+s}{3}<2,
\qquad
 |b|\le\frac{B(B+s)}{\Delta}=1+\frac{s}{3}<2.
\]

As \(a,b\) are integers, every direction with width at most \(W\) lies in
the finite box \([-1,1]^2\).  Up to sign, its primitive directions are

\[
(0,1),\ (1,-1),\ (1,0),\ (1,1).
\]

Exact evaluation gives

\[
\begin{array}{c|c}
u&w(T,u)\\\hline
(0,1)&1+2/\sqrt3\\
(1,0)&1+2/\sqrt3\\
(1,1)&1+2/\sqrt3\\
(1,-1)&2+\sqrt3
\end{array}
\]

Thus no nonzero lattice direction has width below \(W\), and

\[
\boxed{w(T)=1+\frac{2}{\sqrt3}}.
\]

The finite-radius step is an independent certificate of completeness: it does
not rely on a floating-point search cutoff or on an assumption that only
small directions matter.

## What is, and is not, reconstructed globally

The preceding two sections prove this particular triangle is hollow and has
the claimed complete lattice width.  They do not by themselves prove that
every hollow planar convex body has width at most this value.  The global
upper bound is Hurkens’ theorem, with the following source-backed proof
spine.

1. Every planar lattice-free convex set is contained in an inclusion-maximal
   lattice-free set.  The planar maximal-set classification says that such a
   set is a split, a triangle, or a quadrilateral, and every facet has a
   relative-interior lattice contact.

2. Splits have width one.  Quadrilaterals, type-1 triangles, and type-2
   triangles have width at most two.  In the
   source proof, after a unimodular normalization containing \([0,1]^2\),
   the two opposite vertex heights satisfy
   \(1-(h_1+h_3)(h_2+h_4)\ge0\); choosing
   \(h_1+h_3\le h_2+h_4\) gives a coordinate direction of width at most two.

3. The only remaining case is a type-3 triangle.  Write its edge contacts as
   \(p_i=(1-x_i)q_{i+1}+x_iq_{i+2}\), with \(0<x_i<1\).  The lattice-free
   type-3 condition has one of the two cyclic alternatives
   \(x_i+x_j>1\) for all pairs or \(x_i+x_j<1\) for all pairs.
   The source handles the two alternatives symmetrically; for the displayed
   bound we use its (x_i+x_j>1) branch.  If
   \(f=x_0x_1x_2+(1-x_0)(1-x_1)(1-x_2)\), the exact width formula is
   \(w=\min_i x_i/f\).

4. Sort \(x_0\le x_1\le x_2\).  If \(x_0\le1/2\), the formula gives
   \(w<2\).  If \(x_0>1/2\), the source calculation gives

   \[
   f\ge1-3x_0+3x_0^2,
   \qquad
   \frac1w=\frac f{x_0}
      \ge3x_0-3+\frac1{x_0}
      \ge2\sqrt3-3.
   \]

   Therefore \(w\le(2\sqrt3-3)^{-1}=1+2/\sqrt3\), and equality forces
   \(x_0=x_1=x_2=1/\sqrt3\).  This is exactly the contact relation used
   above.

The reduction/classification and the type-3 optimization are the global
Hurkens argument; the local files here supply an independent exact witness
and width certificate.  We therefore label the certificate as a witness
verification plus a source-backed reconstruction of the global proof spine,
not as a verbatim reproof of every maximal-set classification lemma.

## Sources

* C. A. J. Hurkens, “Blowing up convex sets in the plane,” *Linear Algebra
  and its Applications* **134** (1990), 121–128,
  [doi:10.1016/0024-3795(90)90010-A](https://doi.org/10.1016/0024-3795(90)90010-A).
  This is the primary source of the sharp planar covering/flatness theorem.
* G. Averkov and C. Wagner, “Inequalities for the lattice width of
  lattice-free convex sets in the plane,” arXiv:1003.4365 (2010),
  [paper landing page](https://arxiv.org/abs/1003.4365) and
  [full HTML proof](https://arxiv.org/html/1003.4365).  Theorem 2.1 states
  Hurkens’ bound and equality condition; Proposition 3.2 gives the maximal
  planar classification; Lemma 5.1 gives the type-3 width formula and
  optimization; Lemmas 5.2–5.3 handle the other maximal cases.
