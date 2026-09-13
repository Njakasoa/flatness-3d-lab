# Coplanar square contacts: an exact chart and a bounded subclass

This note treats the following labelled incidence pattern in the standard
lattice (mathbb Z^3):

\[
 q_0=(0,0,0),\quad q_1=(1,0,0),\quad
 q_2=(0,1,0),\quad q_3=(1,1,0),
\]

where $q_i$ is in the relative interior of the facet $F_i$ of a bounded
hollow tetrahedron $K$. Relabelling the four facets lets us assume this
assignment. The four contacts are deliberately *not* affinely independent:
they lie in $z=0$ and form a unimodular square.

The primary source is [Averkov--Codenotti--Macchia--Santos](https://arxiv.org/abs/1907.06199),
Section 5.4 and Theorem 5.4. ACMS identify this square as
the only two-dimensional inscribed-contact branch and explicitly leave it
unresolved. The statements below are a self-contained exact calculation for
the labelled tetrahedral incidence pattern. They are not a solution of the
full ACMS square branch and are not presented as a literature result.

## Complete affine chart for the labelled incidence pattern

Let $\lambda_0,\ldots,\lambda_3$ be the barycentric affine forms of $K$:

\[
 K=\{x:\lambda_i(x)\geq 0\ (0\leq i\leq3)\},
 \qquad \sum_i\lambda_i=1,
\]

and $F_i=\{\lambda_i=0\}$. Relative-interior incidence means
$\lambda_i(q_i)=0$ and $\lambda_j(q_i)>0$ for $j\ne i$.

Restrict the four forms to $z=0$. The zero at the assigned square corner
and positivity at the other three corners force the signs

\[
\begin{array}{c|cc}
 i&[x]\lambda_i|_{z=0}&[y]\lambda_i|_{z=0}\\ \hline
0&A x&E y\\
1&-B(x-1)&F y\\
2&C x&-G(y-1)\\
3&-D(x-1)&-H(y-1),
\end{array}
\]

with $A,B,C,D,E,F,G,H>0$. The identity $\sum_i\lambda_i=1$ is
equivalent to

\[
 A+C=B+D,\qquad E+F=G+H,\qquad B+D+G+H=1.
\]

Write $C=B+D-A$, $F=G+H-E$, choose

\[
 B,D,G,H>0,\quad B+D+G+H=1,\quad
 0<A<B+D,\quad 0<E<G+H,
\]

and let $\tau_0+\tau_1+\tau_2+\tau_3=0$. Then every such chart is

\[
\begin{aligned}
 \lambda_0&=A x+E y+\tau_0z,\\
 \lambda_1&=B(1-x)+F y+\tau_1z,\\
 \lambda_2&=G+C x-G y+\tau_2z,\\
 \lambda_3&=D(1-x)+H(1-y)+\tau_3z.
\end{aligned}\tag{SC}
\]

Conversely, the inequalities above make the four assigned contacts relative
interior contacts, since the values at $q_0,q_1,q_2,q_3$, in that order,
are

\[
\begin{array}{c|cccc}
q_0&0&B&G&D+H\\
q_1&A&0&C+G&H\\
q_2&E&B+F&0&D\\
q_3&A+E&F&C&0.
\end{array}\tag{1}
\]

Thus (SC) is an exact eight-dimensional affine chart for this labelled
contact incidence: five horizontal parameters and three independent
$\tau_i$'s. It did not use an affine basis made of the contacts.

## Boundedness and recession are one determinant

Put

\[
 M=\begin{pmatrix}
 A&E&\tau_0\\
 -B&F&\tau_1\\
 C&-G&\tau_2
 \end{pmatrix},
 \qquad d=\begin{pmatrix}0\\B\\G\end{pmatrix},
 \qquad \Delta=\det M.
\]

The first three barycentric coordinates satisfy

\[
 (\lambda_0,\lambda_1,\lambda_2)^T=M(x,y,z)^T+d.
\]

The first two columns of $M$ already have rank two, because the determinant
of their first two rows is

\[
 \det\begin{pmatrix}A&E\\-B&F\end{pmatrix}=AF+BE>0.
\]

Therefore:

* If $\Delta\ne0$, $M$ is invertible and $K$ is the inverse affine
  image of the standard barycentric simplex. Its four vertices are
  $M^{-1}(e_1-d),M^{-1}(e_2-d),M^{-1}(e_3-d),M^{-1}(-d)$, with the obvious
  interpretation that $e_i$ specifies $\lambda_i=1$ for $i=0,1,2$.
  In particular, it is a bounded tetrahedron.
* If $\Delta=0$, the vector

  \[
  r=(E\tau_1-F\tau_0,\ -B\tau_0-A\tau_1,\ AF+BE)
  \tag{2}
  \]

  is nonzero and satisfies $Mr=0$. Since $\sum_i\lambda_i=1$, it also
  leaves $\lambda_3$ unchanged. Hence every line $x+\mathbb Rr$ through
  a point of $K$ lies in $K$; the set has a two-sided line recession and
  is not a tetrahedron.

This is the promised boundedness/recession criterion. It also makes the
affine-dependence issue explicit: the contact points can be coplanar while
the barycentric map $M$ is nonsingular. The determinant of the contact
four-frame is zero by construction, whereas the tetrahedron determinant is
controlled by $\Delta\ne0$.

For reference, the determinant expands as

\[
 \Delta=A(F\tau_2+G\tau_1)+E(B\tau_2+C\tau_1)
       +\tau_0(BG-FC).\tag{3}
\]

The exact script and JSON record this calculation, including a $\Delta=0$
balanced prism and a nonsymmetric $\Delta\ne0$ chart:
[`experiments/square_contacts.py`](../experiments/square_contacts.py) and
[`results/square_contacts.json`](../results/square_contacts.json).

## A finite general hollow obstruction

Let $h_{ij}=\lambda_j(q_i)>0$ for $j\ne i$, as listed in (1). At the two
vertical neighbours $q_i\pm e_3$, the assigned form takes values
$\pm\tau_i$. Consequently hollowness imposes the following exact necessary
conditions:

\[
\begin{array}{ll}
\tau_i>0:&\text{some }j\ne i\text{ has }h_{ij}+\tau_j\le0,\\
\tau_i<0:&\text{some }j\ne i\text{ has }h_{ij}-\tau_j\le0.
\end{array}\tag{4}
\]

If $\tau_i=0$, both neighbours remain on $F_i$, so (4) imposes no
condition. This is only a necessary finite test for the full chart; it is not
being promoted to a complete hollowness criterion.

## Exact width bound in a balanced subclass

Impose the balanced parameters

\[
 A=B=C=D=E=F=G=H=\frac14,
 \qquad (\tau_0,\tau_1,\tau_2,\tau_3)=(s,-s,-s,s).
\]

Then (SC) becomes

\[
\begin{aligned}
 \lambda_0&=(x+y)/4+s z,\\
 \lambda_1&=(1-x+y)/4-s z,\\
 \lambda_2&=(x+1-y)/4-s z,\\
 \lambda_3&=(2-x-y)/4+s z.
\end{aligned}\tag{5}
\]

Here $\Delta=-s/4$, so $s\ne0$ is exactly the bounded-tetrahedron
condition. Solving the three facet equations gives

\[
\begin{aligned}
v_0&=(3/2,3/2,1/(4s)),&
v_1&=(-1/2,3/2,-1/(4s)),\\
v_2&=(3/2,-1/2,-1/(4s)),&
v_3&=(-1/2,-1/2,1/(4s)).
\end{aligned}\tag{6}
\]

The hollowness threshold is exact. If a lattice point is interior, then

\[
0<\lambda_0+\lambda_1=(1+2y)/4<1,
\qquad
0<\lambda_0+\lambda_2=(1+2x)/4<1,
\]

so $x,y\in\{0,1\}$. Writing $r=s z$, the four possible horizontal
columns reduce to

\[
\begin{array}{c|c}
(x,y)&\text{interior iff}\\ \hline
(0,0),(1,1)&0<r<1/4\\
(1,0),(0,1)&-1/4<r<0.
\end{array}\tag{7}
\]

For $s\ne0$, a nonzero integer $z$ satisfies (7) exactly when
$\lvert s\rvert<1/4$: if this inequality holds, take
$z=\operatorname{sgn}(s)$; if it fails, every nonzero $z$ has
$\lvert sz\rvert\ge1/4$. Therefore

\[
 K_s\text{ is hollow}\quad\Longleftrightarrow\quad |s|\ge1/4
 \qquad(s\ne0).\tag{8}
\]

The vertical width from (6) is

\[
 \operatorname{width}(K_s,e_3)=\frac1{2|s|}.
\]

Combining this with (8) gives the nontrivial subclass bound

\[
 \boxed{\ |s|\ge1/4\ \Longrightarrow\ w_{\mathbb Z^3}(K_s)\le2\ }.
 \tag{9}
\]

At $s=1/4$ this is sharp within the subclass: the square already gives
width $|a|+|b|$ for a direction $(a,b,c)$, and the only cases with
$|a|+|b|\le1$ are checked directly from (6); every nonzero integer direction
has width at least $2$, while $e_3$ has width $2$. Each $K_s$ has one
relative-interior contact on every facet, so the hollow members are also
inclusion-maximal by the standard blocked-facet criterion.

Equation (9) is a new calculation in this lab for the explicitly stated
balanced subclass. It does **not** imply $w(K)\le2$, or even $w(K)\le3$,
for arbitrary parameters in (SC).

## Why a fixed-chart coordinate bound cannot work

The preserving shear

\[
 U_n(x,y,z)=(x+nz,y,z),\qquad n\in\mathbb Z,
\]

lies in the unimodular group GL(3,Z), fixes all four contacts because their
$z$-coordinate is zero, and preserves hollowness, maximality, and lattice
width. Applying $U_n$ to $K_{1/4}$ replaces the first coordinates in (6)
by $3/2+n,-1/2-n,3/2-n,-1/2+n$. Thus the same hollow maximal width-two
example has arbitrarily large vertex coordinates while the square contacts
remain exactly fixed.

So no coordinate bound can hold in this fixed square chart. A coordinate
bound “after shears” would have to be a statement modulo the subgroup of
unimodular shears preserving $z=0$, and it would need additional control of
the general parameters in (SC). The explicit shear orbit is an obstruction to
silently treating a bounded coordinate search as complete.

## Scope and next mathematical gap

The exact outcome is:

1. (SC)--(3) give a complete labelled affine parametrization and an exact
   bounded/recession criterion without assuming affine independence of the
   contacts.
2. (4) is a finite necessary hollow test in the general chart.
3. The balanced family (5) has the exact hollow threshold (8) and width bound
   (9), with sharp width $2$ at $s=\pm1/4$.
4. Preserving shears disprove any raw coordinate bound in the fixed chart.

The unresolved part is the asymmetric chart: converting (4), plus the other
integer columns, into a width bound such as $3$ for all hollow members. No
such general bound is claimed here. The generated data are an exact replay of
the formulas above, not an exhaustive search or a proof about the remaining
ACMS square branch.
