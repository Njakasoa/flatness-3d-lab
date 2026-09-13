# Determinant-five class 5: complete width model and bounded vertices

Independent mathematical review, 2026-09-15. Let
\(P=\operatorname{conv}(p_0,p_1,p_2,p_3)\), with ordered contacts
\((0,(5,1,2),e_2,e_3)\). This review supplies exact model geometry;
it proves no new exclusion of this class.

## Exactly fifteen width directions

For a primitive integer covector \(u=(x,y,z)\), its contact values are
\(0,5x+y+2z,y,z\). If its width on P is at most three, each value
has absolute value at most three. Therefore
\(|y|,|z|\le3\) and \(5|x|\le3+3+6=12\), hence \(|x|\le2\).
Exhaustive enumeration in this finite box, retaining primitive vectors and
identifying opposite signs, gives these fifteen directions:

```
(0,0,1), (0,1,-1), (0,1,0), (0,1,1), (0,2,-1),
(1,-3,-2), (1,-3,-1), (1,-2,-3), (1,-2,-2), (1,-2,-1),
(1,-1,-3), (1,-1,-2), (1,-1,-1), (1,0,-3), (1,0,-2).
```

For every convex body K containing P, requiring width greater than 17/5
in all fifteen directions is equivalent to requiring full lattice width
greater than 17/5. Indeed, any omitted primitive direction has *integer*
width on P at least four, so its width on K is at least four. Nonprimitive
directions are positive integer multiples of primitive ones and cannot
lower the minimum. Since K contains a full-dimensional simplex, its width
function bounds a positive multiple of Euclidean norm; the lattice-width
infimum is attained in a finite set. Thus there is no issue with an
infinite family of strict inequalities tending to the threshold.

The exact affine lattice contact group has four elements, found by testing
all 24 permutations of the affinely independent contacts. Acting by the
transpose of its linear part on covectors gives five orbits:

| Contact width | Orbit, modulo sign |
| --- | --- |
| 1 | (0,1,0) |
| 2 | (0,0,1), (0,1,-1), (1,-2,-2), (1,-1,-2) |
| 3 | (0,1,1), (0,2,-1), (1,-3,-2), (1,0,-2) |
| 3 | (1,-3,-1), (1,-2,-3), (1,-1,-1), (1,0,-3) |
| 3 | (1,-2,-1), (1,-1,-3) |

A body K is not assumed invariant under this group. Consequently one
representative per orbit does not suffice for simultaneous width tests.
A group element changes all directions and the body together.

No direction can be dropped using only general convexity, containment of P,
and triangle inequalities for widths, even when all fourteen other width
conditions are retained. To see this, fix an omitted primitive u and two
linearly independent integer vectors a,b in its kernel. The convex body

\[
K_u=P+[-2,2]a+[-2,2]b
\]

has width \(w_u(P)\le3\) in direction u. Every nonparallel integer
covector v has a nonzero integer scalar product with a or b, so

\[
w_v(K_u)=w_v(P)+4(|v\cdot a|+|v\cdot b|)\ge4.
\]

This construction already satisfies both Y and U width conditions whenever
the omitted direction differs from Y=(0,1,0) and U=(1,-1,-2). These bodies
need not be hollow and need not realize the selected contacts in relative
facet interiors. The argument rules out a generic convexity simplification;
it does not prove irredundancy after imposing those additional hypotheses.

## An exact bilinear model forces its own invertibility

Let F be a real 4 by 4 matrix whose columns sum to one, with zero diagonal
and positive off-diagonal entries. Let V be a 4 by 3 matrix whose rows are
vertices v_i. With P also denoting the 4 by 3 matrix of contact rows,
impose the twelve bilinear equations

\[
V^T F=P^T.
\]

Adjoin a first row of ones to obtain

\[
\begin{bmatrix}\mathbf1^T\\V^T\end{bmatrix}F
=\begin{bmatrix}\mathbf1^T\\P^T\end{bmatrix}.
\]

The right side has determinant 5. Both factors on the left are therefore
invertible. The v_i are affinely independent, and F is exactly their
barycentric contact matrix. No extra determinant inequality is needed to
exclude singular assignments. Positivity and the zero diagonal put each
p_j in the relative interior of the facet opposite v_j.

For a vector t, use the contact linear coordinates

\[
\ell(t)=(2t_x/5-t_y-t_z,\ t_x/5,\ t_y-t_x/5,\ t_z-2t_x/5).
\]

For a point t, add (1,0,0,0) to obtain its affine coordinates lambda(t).
Then F lambda(t) are its barycentric coordinates in K=conv(v_i).
The exact observer guard condition is
\(\bigvee_i(F\lambda(t))_i\le0\) for each of the twenty guards.
Its completeness uses the existing class-5 observer theorem and primitive
contact-edge gauge hypotheses; this review does not independently reprove
that theorem. The existing coarse threshold 37/102 is weaker than the
strong threshold below, so the old guard truncation remains valid.

For each imposed nonzero integer vector t,
\(\gamma_{K-K}(t)=\frac12\|F\ell(t)\|_1\). Since its entries sum to zero,
\(\gamma_{K-K}(t)>\beta\) is exactly the disjunction of the fourteen
nonempty proper subset sums exceeding beta. For each of the fifteen
width directions u, require
\(\bigvee_{i\ne j}u\cdot(v_i-v_j)>17/5\).
All these latter width inequalities are linear in V; only V^T F=P^T
is bilinear. With all six primitive contact-edge gauges and the existing
guard theorem, a satisfying exact real assignment gives a genuine hollow
tetrahedron of lattice width greater than 17/5. Any finite additional
necessary gauge constraints may be imposed without losing such bodies.
A floating-point or unchecked symbolic solver model is not such a certificate.

## Explicit bounded vertices from the volume estimate

Set \(\beta=183/500\). For a hypothetical hollow K with full lattice
width greater than 17/5, the established ACMS inequality yields
\(\lambda_1(K-K)>\beta\). The exact comparison follows from
\(1+2/\sqrt3<5389/2500=(17/5)(1-\beta)\), since
\(3\cdot2889^2-4\cdot2500^2=38963>0\).

Minkowski's convex body theorem and Brunn–Minkowski give
\(\operatorname{vol}(K-K)\le8/\lambda_1(K-K)^3\) and
\(\operatorname{vol}(K-K)\ge8\operatorname{vol}(K)\), respectively.
Thus \(\operatorname{vol}(K)<1/\beta^3\). This volume argument uses the
full first minimum; imposing only finitely many gauge inequalities is
not itself a proof of this volume estimate. The estimate remains a valid
necessary cut because full-width hollow candidates satisfy ACMS.

For any v in K, write its affine contact coordinates lambda_j(v).
The volume of conv(P,v) is

\[
\operatorname{vol}(P)\sum_j\max(\lambda_j(v),0).
\]

Proof: add to P the pyramids over each facet visible from v. The pyramid
over facet j has volume \(-\lambda_j(v)\operatorname{vol}(P)\) if
lambda_j(v)<0. Their interiors are disjoint. Since the lambdas sum to one,
\(1+\sum_j\max(-\lambda_j,0)=\sum_j\max(\lambda_j,0)\).
Consequently every vertex of K satisfies

\[
\sum_j\max(\lambda_j(v),0)<R,
\qquad R=\frac6{5\beta^3}=\frac{50000000}{2042829}.
\]

This cut is linear after replacing the positive-part sum by all fourteen
nonempty proper subset inequalities \(\sum_{j\in S}\lambda_j(v)<R\).
The omitted empty and full subsets have sums zero and one, both below R.
It is stronger than the following coordinate bounds, which are useful for
bounded bilinear relaxations:

| Coordinate | Strict lower bound | Strict upper bound |
| --- | --- | --- |
| x | -239785855/2042829 | 250000000/2042829 |
| y | -47957171/2042829 | 50000000/2042829 |
| z | -95914342/2042829 | 100000000/2042829 |

For a coordinate whose range on P is [0,m], positive affine mass below R
and negative mass below R-1 imply \(-m(R-1)<v_k<mR\).
Equivalently the closed barycentric mass polytope has twelve vertices
\(R e_i-(R-1)e_j\), i unequal to j; taking their images verifies all
coordinate extrema exactly.

## Independent arithmetic receipt

Run `python3 tests/audit_det5_complete_geometry_independent.py` from the
scientific repository. The stdlib-only checker imports no solver or
experiment module. It independently enumerates all directions and contact
permutations, verifies the unimodular group and its five direction orbits,
constructs the fifteen generic convexity counterexamples, and checks the
rational mass and coordinate bounds. Its machine-readable receipt is
[`det5_complete_geometry_validation.json`](../results/det5_complete_geometry_validation.json).
The model-rank and volume implications above are mathematical proofs, not
claims that this arithmetic receipt independently verifies every theorem
used in their derivation.

## Review of the implemented vertex lift

The implementation in
[`det5_complete_vertex_lift.py`](../experiments/det5_complete_vertex_lift.py)
was inspected against these equations, including its imported `build` and
`ell` definitions. No mathematical mismatch was found:

- It removes one off-diagonal variable per column by substitution, leaving
  eight independent F variables; all twelve off-diagonal positivity
  conditions remain. Together with twelve vertex coordinates this gives
  twenty variables and twelve bilinear contact equations.
- The imported model retains all twenty observer guards and the primitive
  contact-edge gauge hypotheses. Added strong 183/500 gauges dominate
  the retained coarse 37/102 inequalities.
- Its contact equations have the correct transpose and index convention.
  The width disjunctions contain both signs for all six unordered vertex
  pairs, equivalent to all twelve ordered differences.
- Its optional cap is exactly 6/(5 beta cubed), and its affine barycentric
  coordinates agree with those above. It includes all fifteen nonempty
  subset inequalities; the full-subset inequality is the harmless true
  statement 1<R. Fourteen nonempty proper subsets would suffice.
- The cubic target additionally imposes the strong determinant-volume
  inequality |det F|>(5/6) beta cubed, which is the same necessary volume
  estimate expressed without vertex variables.

The lower-threshold pinned evaluation is only a regression control of the
formulas. It does not generalize the necessary strong gauge and volume
cuts to every hollow body of width greater than 13/5. The three archived
UNKNOWN outcomes do not prove infeasibility. No solver query was executed
for this independent implementation review.
