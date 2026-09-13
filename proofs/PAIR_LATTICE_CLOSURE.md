# Equivariant closure of the pair-branch lattice screen

This note records an exact finite enlargement of the exploratory
`[-2,3]^3` lattice screen for the contact tetrahedron

\[
P=(p_0,p_1,p_2,p_3)=((0,0,0),(2,1,1),(0,1,0),(0,0,1)).
\]

The blocker permutation is \(\sigma=(01)(23)\).  Every permutation of the
four contacts that centralizes \(\sigma\) induces a unique affine lattice map
of \(\mathbb Z^3\) preserving the contact set.  The exact generator and all
serialized points are in
[`experiments/det2_pair_lattice_closure.py`](../experiments/det2_pair_lattice_closure.py)
and
[`results/det2_pair_lattice_closure.json`](../results/det2_pair_lattice_closure.json).

The eight maps use the convention that permutation `q` sends \(p_i\) to
\(p_{q_i}\).  In map order, their linear part \(U\) and translation \(t\)
are:

| `q` | `U` | `t` |
| --- | --- | --- |
| `(0,1,2,3)` | `[[1,0,0],[0,1,0],[0,0,1]]` | `(0,0,0)` |
| `(0,1,3,2)` | `[[1,0,0],[0,0,1],[0,1,0]]` | `(0,0,0)` |
| `(1,0,2,3)` | `[[1,-2,-2],[0,0,-1],[0,-1,0]]` | `(2,1,1)` |
| `(1,0,3,2)` | `[[1,-2,-2],[0,-1,0],[0,0,-1]]` | `(2,1,1)` |
| `(2,3,0,1)` | `[[-1,0,2],[0,-1,0],[0,0,1]]` | `(0,1,0)` |
| `(2,3,1,0)` | `[[-1,2,0],[0,0,-1],[0,1,0]]` | `(0,1,0)` |
| `(3,2,0,1)` | `[[-1,0,2],[0,0,1],[0,-1,0]]` | `(0,0,1)` |
| `(3,2,1,0)` | `[[-1,2,0],[0,1,0],[0,0,-1]]` | `(0,0,1)` |

All eight determinants are \(\pm1\).  Their images of the 216-point box
form four distinct 216-point sets: the original box, one image with first
coordinate range \([-12,13]\), and two images with first-coordinate range
\([-7,8]\).  Their union is closed under all eight maps and has exactly 432
points, 216 of which are new.  The sorted closure is serialized with a
SHA-256 digest in the JSON artifact; its coordinate bounds are

\[
[-12,13]\times[-2,3]\times[-2,3].
\]

Both hidden points are present:

\[
(-3,1,-1),\qquad(-3,-1,1).
\]

For example, the first is the image of `(-1,2,0)` under map 2 and the image
of `(1,0,-1)` under map 4.  The JSON records all exact preimages found in the
box for both points.

For a lattice point \(z\), write \(\lambda(z)\) for its four contact
barycentric coordinates.  A row of \(F\) has zero diagonal, strictly
positive off-diagonal entries, and designated entry
\(F_{i,\sigma(i)}\) at least the sum of its other two entries.  Dividing a
row by its positive row sum gives the closed pair triangle

\[
a\geq \tfrac12,\quad b,c\geq0,\quad a+b+c=1.
\]

Thus multiplying a row slack by its positive row sum does not change its
sign.  The exact row test evaluates the three triangle corner values.  A row
atom can occur in the strict positive domain when its minimum is negative; it
also occurs when both values on the admissible edge \(a=1/2, b,c>0\) are
zero.  A row maximum at most zero makes the entire lattice clause
tautological.  This recovers the original 176 tautologies and 40 retained
clauses, with no contradictory clause.

Over the 432-point closure there are 324 tautologies and 108 retained
clauses.  Relative to the original box, 148 points are new tautologies and
68 points give new retained clauses.  The row-profile reduction is exact for
the stated positivity and weak dominance conditions; it does not use a
floating approximation.

The remaining implication checks use only Z3 QF_LRA with rational
coefficients, strict positivity, pair dominance, \(D=\sum_j c_j>2\), and
the 40 original retained clauses.  Each check had a 10-second timeout and
all checks returned a definite result:

* 56 of the 68 added retained clauses are implied by the original 40.
* 12 are individually new:
  `(-6,-2,1)`, `(-6,1,-2)`, `(-5,-2,1)`, `(-5,1,-2)`,
  `(-3,-1,1)`, `(-3,1,-1)`, `(5,1,2)`, `(5,2,1)`,
  `(7,1,3)`, `(7,3,1)`, `(8,1,3)`, `(8,3,1)`.
* Four of those 12 are implied after the other individually new clauses are
  added: `(-6,-2,1)`, `(-6,1,-2)`, `(8,1,3)`, and `(8,3,1)`.
* The eight-point list
  `(-5,-2,1)`, `(-5,1,-2)`, `(-3,-1,1)`, `(-3,1,-1)`,
  `(5,1,2)`, `(5,2,1)`, `(7,1,3)`, `(7,3,1)`
  is an irredundant basis relative to the original clauses and implies all
  68 added retained clauses.

The exact rational countermodels for the 12 individual non-implications and
the full status tables are serialized in the JSON artifact.  These results
only strengthen a finite necessary screen by equivariance and elementary
linear implications.  They do not provide a global lattice bound, a
sufficiency theorem for hollowness, or an NRA feasibility conclusion.
