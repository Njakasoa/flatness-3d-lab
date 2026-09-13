# Determinant-two tetrahedron: the 2+2 blocker branch

This note fixes the determinant-two contact tetrahedron

\[
 P=\operatorname{conv}(0,(2,1,1),e_2,e_3)
\]

and the derangement \(\sigma=(01)(23)\). It records an exact reduction and
a bounded audit. It does **not** claim a uniform width theorem for the full
continuous branch; the finite search found no counterexample but is not an
elimination proof.

## The integer roof chart

For a lattice point \((X,Y,Z)\in\mathbb Z^3\), use

\[
 u=1-Z=x_0+x_2,\qquad v=1-Y=x_0+x_3,
 \qquad w=1+X-Y-Z=x_0+x_1.
\]

The inverse map is

\[
 (X,Y,Z)=(w-u-v+1,\,1-v,\,1-u),
\]

so this is a unimodular affine change of the ambient lattice. The four
contact points become the odd cube corners

\[
 p_0=(1,1,1),\quad p_1=(0,0,1),\quad
 p_2=(1,0,0),\quad p_3=(0,1,0).
\]

The four half-sum points are the even corners. In the 2+2 branch, the two
facets through \(p_0,p_1\) exclude the even corners directly below them and
the two facets through \(p_2,p_3\) exclude the even corners directly above.
After positive normalization their equations have the two-roof form

\[
\begin{aligned}
 L_0(u,v)&=1+a(u-1)+b(v-1),\\
 L_1(u,v)&=1-cu-dv,\\
 U_0(u,v)&=e(1-u)+fv,\\
 U_1(u,v)&=gu+h(1-v),
\end{aligned}
\]

with

\[
 a,b,c,d,e,f,g,h>1,
 \qquad
 K=\{(u,v,w):\max(L_0,L_1)\le w\le\min(U_0,U_1)\}.
\]

The strict inequalities follow from positivity of the three non-designated
entries in each row of the contact matrix. They also make the four assigned
contact points relative-interior points of their facets.

## Four exact necessary hollowness inequalities

At the four projected unit-square corners one endpoint is the integral contact
value (the other roof value is generally real):

\[
\begin{array}{c|c|c}
 (u,v)&\text{contact endpoint}&\text{hollow consequence}\\ \hline
 (0,0)&w=1&\min(e,h)\le2\\
 (1,1)&w=1&\min(f,g)\le2\\
 (1,0)&w=0&\min(b,c)\le2\\
 (0,1)&w=0&\min(a,d)\le2.
\end{array}
\]

For example, at \((0,0)\) the fibre is
\[
 [1,\min(e,h)].
\]
If both \(e,h>2\), the lattice point \((0,0,2)\) is strictly interior.
The other three rows are the same argument after exchanging the two roofs or
reflecting the square. Equality is allowed: a point at the second level can
lie on a facet of a maximal hollow body. Thus these are closed conditions;
replacing them by strict inequalities would incorrectly discard boundary
cases.

These four tests split the finite-slope relaxation into sixteen choices of
the small coefficient. They are necessary only. An asymmetric parameter choice can
satisfy all four and still contain further integer points away from the unit
square; this is why the four half-sum obstructions alone do not certify
hollowness.

The chart also has a deliberate boundary limitation. A designated contact
coefficient \(A_{ij}=1/2\) makes the corresponding facet vertical in the
chosen \(w\)-roof normalization; it is the limit in which one or more of
\(a,b,c,d,e,f,g,h\) tends to infinity. The finite roof formula and the scan
below use strict \(A_{ij}>1/2\), equivalently finite slopes. The equality
cases are part of the original branch and require a separate limiting
argument; they are not silently covered by the numerical scan.

## Exact witness and bounded result

The script [`experiments/det2_pair_branch.py`](../experiments/det2_pair_branch.py)
does one deterministic finite run. Its exact witness sets

\[
 a=b=c=d=e=f=g=h=2.
\]

The four vertices are

\[
 \left(\frac54,-\frac14,-1\right),
 \left(-\frac14,\frac54,-1\right),
 \left(\frac54,\frac54,2\right),
 \left(-\frac14,-\frac14,2\right).
\]

The full integer box is
\([0,1]\times[0,1]\times[-1,2]\); checking all sixteen points with exact
barycentric signs gives no interior lattice point. The exact directional
certificate gives

\[
 w_{\mathbb Z^3}(K)=\frac32,
 \qquad\text{minimized by }(1,0,0),(0,1,0).
\]

This proves the branch is nonempty and supplies a consistency check for the
chart. It is a lower-bound witness for the attainable branch width, not an
upper bound for all choices of the eight parameters.

The same execution performs a fixed-seed log-uniform screen of 768 parameter
choices satisfying the four corner tests. For each bounded sample it scans
the complete integer bounding box, then checks every primitive direction whose
width on the contact tetrahedron is at most three. The contact tetrahedron
gives the finite direction reduction: a direction wider than three on the
contacts cannot minimize a body already known to have width at most three.
The resulting JSON records sample counts and the best hollow sample.

The bounded conclusion is therefore:

* the 2+2 roof reduction and the four corner inequalities are exact;
* the exact symmetric witness is hollow and has width \(3/2\);
* the finite scan produced no hollow width-\(>3\) example;
* no uniform \(\le3\) (or \(\le2\)) proof was obtained from this run.

Promoting the scan to a theorem would be an unsupported generalization. A
complete proof still needs an argument that the remaining integer fibres away
from the unit square force one of the finite direction widths to be at most
three, or an exact elimination over the sixteen coefficient chambers.
