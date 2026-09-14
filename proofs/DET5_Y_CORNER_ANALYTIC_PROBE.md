# Exact height ordering and two guard reductions in the Y corner

Status: proved structural lemmas for actual contacts. They give additional
necessary cuts for a linear outer model. They do not constitute an analytic
derivation of the numerical threshold 4/23 or a new complete exclusion.

Use the ordered determinant-five contacts and the strict opposite-facet
relative-interior hypotheses of
[the conditional theorem](DET5_Y_CORNER_SHARP_SUPPLEMENT.md). Let F be their
barycentric matrix: columns sum to one, its diagonal is zero, and all
off-diagonal entries are positive. In the Y-extrema chart [0,3], write

    q=(0,x,y,1),     0<=x,y<=1,
    F^T q = a*1+b*(0,1,1,0).

Only equality of the heights of contacts p0 and p3 is used in the first
lemma. Hollowness enters only when applying the guard reductions below.
No width, volume, or gauge threshold hypothesis is needed.

## The order of x and y fixes the Z signs

Set z=F(e3-e0). Its four entries are

    z0=F03>0, z1=F13-F10, z2=F23-F20, z3=-F30<0.

Both column sums and equal contact heights give

    z0+z1+z2+z3=0,        x*z1+y*z2+z3=0.                (1)

If x=y=h, these identities imply h*z0-(1-h)*z3=0.
The left side is strictly positive for every h in [0,1], including both
endpoints. Thus **x=y cannot occur for actual strict contacts**.

For x!=y, solving (1) gives

    (y-x)*z1 = -y*F03-(1-y)*F30,
    (y-x)*z2 =  x*F03+(1-x)*F30.                         (2)

Each unsigned numerator is positive throughout [0,1]. Therefore:

| Actual height order | Signs of (z0,z1,z2,z3) |
|---|---|
| x<y | (+,-,+,-) |
| x>y | (+,+,-,-) |

This applies on the full square, not only when x,y>=3/4. Heights x=0 or
y=1 cause no exception. In particular, strict inequalities are appropriate
in both order branches, and no equality branch must be retained for actual
tetrahedra.

The vector e3-e0 is the difference-barycentric coordinate vector of the
lattice direction Z=(0,0,1). Hence its actual difference-body gauge is
||z||_1/2. Its positive support is now fixed, giving

    x<y: gamma(Z)=F03+F23-F20=1-F13-F20,
    x>y: gamma(Z)=F03+F13-F10=1-F23-F10.                 (3)

Thus the condition gamma(Z)>beta is one strict linear inequality in F on
each order branch. The general fourteen-alternative subset encoding can
be replaced by (3). An equivalent exact identity, with m=min(x,y) and
M=max(x,y), is

    gamma(Z) = [M*F03+(1-m)*F30]/(M-m).                 (4)

Equation (4) is a geometric identity, not an additional linear constraint
when x,y are variables. Equations (2) retain bilinear terms; the sign
consequences and the two formulas (3) are linear in F.

There is also a direct linear ordering constraint on the offset:

    min(x,y) < a < max(x,y).                             (5)

Indeed, column zero expresses a as a convex combination of x,y,1 with
strictly positive weight at 1. Since min(x,y)<1, this gives a>min(x,y).
Column three expresses a as a convex combination of 0,x,y with strictly
positive weight at 0. Since max(x,y)>0, this gives a<max(x,y). Thus each
order branch can also impose x<a<y or y<a<x respectively. This proves
the impossibility of x=y independently of solving equations (1).

## A general section interpretation

The height-order argument does not depend on the determinant-five lattice
coordinates. In any full-dimensional tetrahedron, suppose strict contacts
on the facets opposite the minimum and maximum of a nonconstant linear functional have
the same functional value. Then this common value lies strictly between the
values of the other two vertices. The barycentric proof of (1), (2), and (5)
applies after normalizing the minimum and maximum to zero and one.

For x<y, the section at the common contact height a is a quadrilateral.
Vertices v0,v1 lie strictly below this plane and v2,v3 strictly above it.
The four section vertices lie on edges 02,03,12,13. Contact p0 is in the
relative interior of the section edge joining 12 to 13, while p3 is in the
relative interior of the edge joining 02 to 12. These two section edges are
adjacent, meeting at the intersection with edge 12. For x>y swap indices 1,2.
This identifies a definite planar contact arrangement for a future sectional
argument. No classification or width theorem for these quadrilaterals is
asserted here; the height and sign lemmas remain elementary consequences of
strict opposite-facet contact and affine averaging.

## Two hollow guards have only two possible separating facets

The contact barycentric coordinates of lattice points g2=(2,1,1) and
g3=(3,1,1), multiplied by five, are respectively

    (-1,2,3,1),             (1,3,2,-1).

Hollowness requires at least one coordinate of F times each vector to be
nonpositive. Let

    R3: F30 >= 2*F31+3*F32,
    R0: F03 >= 3*F01+2*F02.

The exact equivalent reduced guard clauses are:

| Order | Guard g2=(2,1,1) | Guard g3=(3,1,1) |
|---|---|---|
| x<y | -z1>=3*F12 OR R3 | R0 OR z2>=3*F21 |
| x>y | -z2>=2*F21 OR R3 | R0 OR z1>=2*F12 |

To verify this directly, the four g2 coordinates, after multiplication by
five, are

    2*F01+3*F02+F03,
    z1+3*F12,
    z2+2*F21,
    -F30+2*F31+3*F32.

Its first coordinate is positive. When x<y its third coordinate is also
positive; when x>y its second coordinate is positive. Precisely the two
listed alternatives remain. The four scaled g3 coordinates are

    3*F01+2*F02-F03,
    -z1+2*F12,
    -z2+3*F21,
    F30+3*F31+2*F32.

Its last coordinate is positive, and the sign table removes one middle
coordinate. The boundary comparisons remain non-strict, since an integer
guard may lie on the boundary of a hollow tetrahedron.

## Consequences for strengthened formulations

An actual body in chart [0,3] belongs to exactly one of the two strict
height-order branches. In each branch, add the two strict sign comparisons
from the table, the offset ordering (5), and substitute (3) for the Z gauge. Optionally replace the
two four-alternative guard clauses by their two-alternative forms. These
are necessary conditions even if the rest of the model uses relaxed
products rather than exact reconstruction.

The cuts cannot be justified by treating a McCormick product variable as
an exact product. Their soundness instead follows from the actual-body
substitution above. Consequently, an old relaxed assignment can be removed
without any geometric contradiction. This is a change of formulation, not
a repetition of an unchanged solver query.

This lemma explains a finite sign structure that was obscured by the old
generic gauge encoding. It does not yet explain the particular rational
number 4/23 through a short chain of analytic inequalities. The separate
[proof slices](DET5_CORNER_PROOF_SLICES.md) establish which gauge and guard
premises are sufficient for the existing numerical certificates.

## Exact verification

Run `python3 tests/replay_det5_y_corner_ordering.py`.
The standard-library script proves four cleared-denominator polynomial
identities by exact coefficient cancellation. It also constructs 416 exact
rational matrices satisfying strict contact positivity, column sums, and
all four height reconstruction equations, including both height orders
and endpoint heights. These fixtures verify the offset order, gauge identities and 832
equivalences between full and reduced guard clauses. They are contact
matrix regressions, not claimed hollow tetrahedron witnesses.

The universal inequality proof is the positivity argument above; the
finite fixtures are supplementary checks. The
[receipt](../results/det5_y_corner_ordering_validation.json) records zero
solver queries and no newly proved numerical exclusion.
