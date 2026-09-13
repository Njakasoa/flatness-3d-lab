# A complete hollowness test on twelve lattice lines

Let

    P=conv(p0,p1,p2,p3),
    (p0,p1,p2,p3)=(0,(2,1,1),(0,1,0),(0,0,1)).

Let K be a compact, full-dimensional convex set containing P, with every
p_i on the boundary of K. No pair or cycle assumption is needed for the
first statement.

**Twelve-line criterion.** K is hollow if and only if its interior contains
no lattice point on the twelve lines specified below. These lines are
independent of K. If additionally vol(K)<21, it suffices to test **1456
explicit lattice points**. In the pair facet chart, **972** of those tests
hold automatically by row dominance, leaving **484** explicit clauses.

This is a complete test under its hypotheses, not an empirical search
radius. It is an application of a known five-point classification and a
minimal-extension argument. No new width bound or priority claim is made.

## 1. Find a minimal interior extension

The contact tetrahedron is empty: its only integer points are its four
vertices. This follows directly from its barycentric inequalities or from
the twelve-point bounding-box check in the accompanying certificate.

Suppose K is nonhollow. Among the finitely many z in int(K) intersect Z^3,
choose one minimizing vol(conv(P,z)), and put Q=conv(P,z). The point z is
outside P since its four lattice points lie on the boundary of K.

If q is another integer point of Q outside P and different from z, write

    q = alpha*z + (1-alpha)*p,   p in P,  0<alpha<1.

Such a representation follows from Q=conv(P union {z}); alpha cannot be
zero since q is outside P, and cannot equal one since q differs from z.
Because z is interior to K and p is in K, q is interior to K. Moreover,
conv(P,q) is a proper, full-dimensional subset of Q and has strictly smaller
volume: z is an exposed vertex of Q, and replacing it by q removes it from
the convex hull. This contradicts minimality. Thus Q has exactly five
lattice points, P's vertices and z.

All five points are vertices of Q. The new point z is a vertex since it is
outside P. If some p_i ceased to be a vertex, expressing it as a convex
combination of the other four points would have a positive coefficient of
z (the four p_i are affinely independent). That would put p_i in int(K),
contrary to its boundary status.

This use of boundary contacts is essential. The statement does not assert
that every observer of the finite point set P has all five points extreme.

## 2. A known classification confines that extension to width one

Blanco–Santos, *Lattice 3-polytopes with few lattice points*,
[arXiv:1409.6701v3](https://arxiv.org/pdf/1409.6701), Theorem 1.2(1),
states that five-point three-dimensional lattice polytopes of signatures
(2,2), (2,1), or (3,2) have width one. A configuration of five vertices
has signature (2,2) or (3,2). Therefore Q has lattice width one. This
special case is also attributed there to Howe's theorem for polytopes
whose lattice points are all vertices. We use the stated classification
as an external theorem; we do not claim a new proof of it.

Any width-one integer functional on Q has width one on P. Up to sign the
only possibilities for P are

    u=(0,0,1), (0,1,0), (1,-1,-1).

To check completeness, choose the sign so the values on P are in {0,1}.
The value at p0 is zero. The other values are (2a+b+c,b,c) for an integer
normal (a,b,c). Choosing three binary values and imposing that
(2a+b+c)-b-c is even gives exactly the three normals above, up to sign.
Every such direction separates the contacts into two pairs on consecutive
integer planes.

## 3. Describe the twelve lines

For each of the three normals u and each of its two levels h on P, let
p_a,p_b be the two contacts on that level and v=p_b-p_a. For each sign
s in {-1,1}, take the lattice line defined by

    u dot z = h,
    v cross (z-p_a) = s*u.

The segment direction v is primitive. Each system has an integer solution
q0, and all its integer solutions are exactly q0+t*v, t in Z. Representatives
and parameter intervals are stored in certificates/det2_observer_lines.json.
The three normals, two levels and two signs give twelve distinct lines.

The minimal z from the previous section lies on one of them. It lies on
one of Q's two integer slab levels. That level contains two contacts and
z, forming a lattice triangle with no other lattice points. Pick's theorem
in the plane lattice makes that triangle unimodular. Its oriented cross
product is therefore +u or -u, exactly the displayed equation.

Conversely, every integer z on any displayed line gives an empty five-vertex
extension conv(P,z): one of its two integer slab sections is a unimodular
triangle and the other is a primitive segment. These exhaust its lattice
points, and all five are vertices. This proves that the lines describe
exactly the empty five-vertex extensions of P, not merely a covering list.

If K has no interior lattice point on the lines, a minimal z cannot exist.
This proves the infinite twelve-line criterion. The reverse implication is
immediate from hollowness.

## 4. A finite list under the volume cutoff

For a point z=(X,Y,Z), its contact barycentric coordinates are

    lambda(z)=(1+X/2-Y-Z, X/2, Y-X/2, Z-X/2).

The visible-facet pyramids of P give

    vol(conv(P,z))=(1+sum_i max(0,-lambda_i(z)))/3.

If z is in K and vol(K)<21, its negative barycentric mass is strictly
less than 62. Its positive mass is then less than 63. Every subset sum
lies between -62 and 63, implying in particular the enclosing integer box

    [-124,126] x [-62,63] x [-62,63].

For each line, intersect its integer parameter with this safe box, then
retain exactly those points whose negative barycentric mass is below 62.
This leaves 123 integer parameters on each of the twelve lines and 1456
distinct points after overlaps. The enumeration is entirely rational.
The box supplies completeness of the parameter cutoff, not a heuristic.

For each retained point q, impose that q is not strictly interior to K.
These 1456 exclusions are necessary and sufficient for hollowness under
all stated boundary-contact and volume hypotheses.

## 5. Pair-chart simplification and consequences for the solver

In the positive pair chart, each normalized row belongs to the triangle
with coefficients (a,b,c)=(1,0,0),(1/2,1/2,0),(1/2,0,1/2), interpreted by
closure; actual off-diagonal entries remain strictly positive. For a fixed
q, the three values of its row slack on this triangle bound every possible
row slack. If one row has maximum <=0, q is excluded for every pair matrix.
This removes 972 guards. All remaining 484 exclusions are linear
disjunctions in F. Rows whose minimum is positive cannot exclude q and
may be omitted from the disjunction.

The column model already asserts det(F)>50653/3183624, implying
vol(K)<1061208/50653<21 even for a nonhollow assignment. It also guarantees
all four contacts lie on their facets. Replacing the partial 216-point
screen by the full guard list therefore closes the hollowness gap of that
model at threshold17/5. Together with the established complete 37 width
directions, this gives an exact finite feasibility formulation, subject to
correct implementation. No solver infeasibility or class elimination is
inferred from the written reduction.

Reproduction: `python3 -m experiments.det2_observer_lines`.
Independent review: proofs/DET2_OBSERVER_REVIEW.md.

## 6. Generalization to every nonunimodular empty contact tetrahedron

The twelve-line principle is not peculiar to determinant two. Let P be any
empty lattice tetrahedron of normalized volume d>1. If P is contained in a
compact full-dimensional convex K and its four vertices are on bd(K), then
K is hollow if and only if its interior avoids the lattice points of at
most twelve explicitly constructible lines.

The minimal-extension argument and the five-point width-one theorem apply
unchanged. A width-one slab of P cannot split its vertices as three plus
one. Indeed its three-point face is an empty lattice triangle, hence
unimodular in its plane lattice; the fourth vertex is at primitive lattice
height one. The tetrahedron would have normalized volume one, contrary to
d>1. Therefore every width-one slab splits P into two pairs. There are only
three partitions of four vertices into two unordered pairs. Each partition
admits at most one normal up to sign: it must be perpendicular to the two
opposite edge vectors, which are linearly independent in a full-dimensional
tetrahedron. Retain the primitive normal only when the two levels differ
by one.

For each retained normal and each of its two levels, use the primitive
contact segment v and the equations

    u dot z = h,  v cross (z-p_a) = +/-u.

These again give two lattice lines. Existence of integer representatives
follows because v, primitive in Z^3, is primitive in the rank-two plane
lattice and extends to a basis of that lattice. The same unimodular-triangle
argument proves both inclusion directions. There are at most 3*2*2=12 lines.

A volume cutoff vol(K)<V further restricts every required interior witness
by the exact inequality

    sum_i max(0,-lambda_i(z)) < 6V/d - 1.

Along each line, lambda(z) is affine in its integer parameter. The inequality
therefore gives a bounded open interval of parameters, whose exact integer
points form a complete finite guard set. Boundedness also follows from the
bounded simplex-coordinate negative-mass region. No guessed search radius
or classification of the real surrounding bodies is needed.

The d>1 hypothesis is essential to this particular line reduction. A
unimodular tetrahedron admits three-plus-one slabs, so this argument does
not confine all its empty five-vertex extensions to lines. The unimodular
contact class, including the known Codenotti–Santos contact tetrahedron,
remains outside the generalized statement.

## Prior observer-line methods

The line principle has close established antecedents. Averkov–Schymura,
[Complexity of linear relaxations in integer programming](https://d-nb.info/1230965718/34),
Lemma6.4 and its proof already describe observers on neighboring lattice
lines, together with a finite exceptional set. Their observer/guard-set
framework also precedes the minimal-extension use here. The boundary-contact
hypothesis specializes that framework by preventing contact points from
becoming non-extreme, and the calculation above supplies the explicit
nonunimodular/twelve-line instance needed by this lab. Novelty is unconfirmed;
no first theorem or general invention of observer-line methods is claimed.
