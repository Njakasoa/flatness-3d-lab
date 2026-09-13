# Sixty-three necessary contact-hull types above a sub-candidate threshold

Date: 2026-09-13. Computational theorem with independent certificate replay
and internal adversarial review. External novelty is not established.

Let c=(11/7)(1+2/sqrt(3))=3.38595798888... . All equivalences below are
affine transformations preserving the ambient lattice Z^3. A contact hull
is the convex hull of one lattice point chosen in the relative interior of
each facet of an inclusion-maximal hollow set. This is different from the
entire set of boundary lattice points of that set.

## Statement

Let K be a compact full-dimensional hollow convex body in R^3 with w(K)>c.
It has a bounded inclusion-maximal hollow extension M. For every selection
of one relative-interior lattice point on each facet of M, the resulting
contact hull P is equivalent to one of the following necessary possibilities:

| dimension of P | vertices of P = facets of M | number of types |
|---:|---:|---:|
| 2 | 4 | 1 (unimodular square) |
| 3 | 4 | 10 |
| 3 | 5 | 11 |
| 3 | 6 | 22 |
| 3 | 7 | 10 |
| 3 | 8 | 9 |
| | total | 63 |

The ten tetrahedra are listed in CONTACT_OBSTRUCTION_REDUCTION.md. The
52 other three-dimensional representatives are explicit integer vertex sets
in results/contact_extensions.json. The full difference-body minima for
these 52 representatives are in certificates/contact_hull_obstructions.json.
The same list applies at w(K)>=2+sqrt(2), since c<2+sqrt(2).

This classifies a necessary discrete contact hull, not the surrounding body.
It does not assert that all 63 hulls are realized by bodies with w>c. For each
fixed hull, continuous facet choices and width optimization remain.

## From arbitrary bodies to bounded maximal extensions

Every full-dimensional hollow convex set is contained in a maximal one;
the blocked-facet/recession characterization is standard Lovasz theory.
One proof is Averkov, *A proof of Lovasz's theorem
on maximal lattice-free sets*, Theorem 1 (its Lemma 7 is the parity lemma,
not the existence assertion):
https://arxiv.org/html/1110.1014 .

For completeness, existence can also be obtained from Zorn's lemma. For a
chain of closed full-dimensional hollow sets containing K, the closure of
their union is convex. If a lattice point were interior to that closure,
it would be inside a simplex of points from the union (approximate a small
simplex surrounding it). The finitely many simplex vertices lie in one
member of the chain, a contradiction. Thus the closure is a hollow upper
bound for the chain.

Lovasz's characterization says that the recession cone of a maximal set is
a rational linear space. If nonzero, a lattice basis change writes the set
as a hollow convex body in dimension at most two times a linear space.
Integer directions of finite width descend to the quotient lattice.
The planar flatness bound A=1+2/sqrt(3) (or the one-dimensional bound one)
then gives w(M)<=A<c. This contradicts width monotonicity w(M)>=w(K)>c.
Hence M is bounded, a polytope, and all its facets have lattice blockers.

Choose blockers p_i in distinct relative facet interiors. Every p_i is a
vertex of their hull: its supporting facet form is zero there and strictly
positive on every other blocker. Every nonvertex convex combination of the
p_i uses at least two different blockers, so all facet forms are strictly
positive at that combination. Such a point is interior to M and cannot be
integer. Therefore P is closed-empty and its vertices are exactly the p_i.

There are at most eight such points. Otherwise two would have identical
parity in Z^3; their integer midpoint is a nonvertex point of P, impossible.
There are at least four facets. An empty planar integer polygon has at most
four vertices (planar parity), and a four-vertex empty polygon is a
unimodular parallelogram: triangulate it into two empty triangles and use
Pick's theorem. Hence the only planar possibility is the square. The hull
cannot have dimension one because it has at least four exposed vertices.

## Every larger empty hull contains a unimodular frame

Howe's theorem gives width one for an empty lattice 3-polytope. For five or
more vertices, one of its two integer layers contains at least three
vertices. These are noncollinear, since an empty segment has only its two
endpoints. Their triangle is empty, and therefore unimodular in the planar
layer lattice. Adding a vertex from the other layer makes a unimodular
tetrahedron. A lattice transformation puts this frame at

    F={0,e1,e2,e3}.

For any four affinely independent vertices of P, their convex hull is an
empty lattice tetrahedron T: it is contained in P, and no other vertex of P
can lie in its convex hull because every vertex of P is extreme. Since
T is also contained in M, CONTACT_OBSTRUCTION_REDUCTION.md restricts it to
the ten types, each having normalized determinant at most 13.

For an additional vertex q=(q1,q2,q3) after normalization at F, replacing
one vertex of F at a time gives determinants q1,q2,q3,1-q1-q2-q3 up to sign.
They are either zero or bounded in absolute value by 13. Thus

    |q_i|<=13,  |1-q1-q2-q3|<=13.                         (B)

This proves a uniform finite box for every additional contact. It is not
an empirical coordinate cutoff and does not bound the body's real vertices.

## Exact exhaustive extension algorithm

enumeration/contact_extensions.py enumerates all 13,100 integer points in
(B) outside F, then tests extension of F. The tests leave 424 possibilities.
Starting from F, extend repeatedly to five, six, seven and eight vertices.
At each step require:

1. There is a common primitive integer height placing every vertex in layers
   zero and one. Because F is present, every possible height, after sign,
   has coefficients in {0,1}^3 other than zero: seven tests suffice.
2. Every triangle is primitive in its plane: the gcd of its integer cross
   product components is one. This excludes collinear triples as well.
3. Every nondegenerate four-vertex tetrahedron has one of the ten allowed
   ordered HNFs. The allowed ordered set contains all vertex permutations
   and anchor choices of those ten representatives, giving 47 ordered HNFs.

These tests are necessary by the arguments above. They also ensure the
output hull is empty and all listed points are vertices. By Caratheodory,
any lattice point of the hull lies in a simplex on at most four input points.
The three-dimensional simplices pass the empty-tetrahedron check; triangles
are empty by the primitive cross-product test; edges are primitive as edges
of those triangles. So no extra lattice point can occur. A listed point
could not be nonextreme either: applying the same argument to its convex
representation by other points would contradict these tests.

Canonicalization considers *every ordered unimodular four-frame* in the
point set. It maps that frame to F and takes the lexicographically least
sorted transformed point set. The list of transformed sets is invariant
under affine lattice maps, and equality of canonical keys gives an explicit
lattice map, so this is a complete invariant on the supported domain.
Every canonical output still contains F. Therefore all subsequent extension
steps use the same proved box (B) and seven height tests.

Completeness follows inductively: any admissible target contains F; add its
other vertices in any order. Every intermediate subset remains admissible.
After each canonicalization, the remaining target vertices transform with
it, remain bounded by (B), and appear in the next extension pool. Quotienting
cannot destroy a necessary extension path. The resulting class counts are
11,22,10,9. No floating-point convex hull or guessed search radius is used.

## Full difference-body minima

For a two-layer polytope with layer polygons P0,P1, the zero-height section
of P-P is S=conv(P0-P0,P1-P1). Its planar lattice is identified with Z^2 by
deleting a coordinate whose coefficient in the binary height is one.
At dilation less than one, any integer vector in P-P must have height zero.
An integer edge gives lambda_1(P-P)<=1. Consequently

    lambda_1(P-P)=min(1,lambda_1(S)).

src/width_one_minimum.py builds S with an exact integer monotone-chain hull,
computes rational gauges from all its edge inequalities, and searches its
complete coordinate box up to dilation one. All 52 hulls have lambda_1>4/11
and also lambda_1>1-A/(2+sqrt(2)). So this additional necessary test removes
none of these candidates; its exact witnesses are retained.

## Nine-template compression

There is a compact equivalent way to supply all the necessary configurations.
Every one of the 63 hulls is an affine lattice image of a subset of the
vertices of one of the nine eight-vertex hulls. The exact embedding table is
certificates/contact_templates.json: each row gives the chosen template,
vertex indices, integer matrix U with determinant +/-1, and integer
translation t, such that U times the selected subset plus t equals the
listed canonical contact set. experiments/contact_templates.py constructs
these witnesses.

This proves a further corollary: after normalization, the contact set of M
is a subset of one of nine explicitly listed eight-point templates. It does
not say that the other template vertices lie in M or on its boundary.
Deleting vertices from a template is a description of candidate contact
sets, not an operation on the surrounding hollow body's facets.

All noncoplanar four-subsets of the nine templates have exactly the ten
tetrahedron classes, and the five-to-eight-subsets have counts 11,22,10,9.
Their coplanar four-subsets are unimodular squares. Thus the templates
compress the complete list, without replacing the exhaustive argument that
the list is necessary.

See results/eight_contact_hulls.png for the templates and
results/contact_reduction_counts.png for the class counts. Rendered hulls
are illustrations only; their exact integer coordinates and maps are the
certificates.

## Validation and novelty boundary

The Astra review independently regenerated the 51 tetrahedron classes and
checked all 52 extension hulls for closed emptiness and extremality using
supporting planes and complete integer boxes. It found no mathematical
blocker, but identified missing validation of the main certificate payload.
The repaired verifier rechecks all 51 tetrahedra, all 52 larger hulls,
1,365 four-point subsets and 63 template embeddings, and rejects 21 deliberate
mutations. The reviewer independently confirmed rejection through the actual
script entrypoint and checked all affine maps. The repair is closed in
results/CONTACT_REDUCTION_REVIEW.md. The full eight-stage replay passed;
see results/CONTACT_REDUCTION_VALIDATION.md for coverage and limits.

ACMS already prove finite contact reduction in principle. The proposed
contribution here is the sharper planar obstruction and the explicit
63-type necessary list at a threshold below the Codenotti--Santos width.
The existence of a finite reduction itself is known. Closest-work and
2025--2026 checks are in CONTACT_MINIMA_LITERATURE.md and
CONTACT_HULL_NOVELTY_AUDIT.md. No matching explicit list was found in the
checked primary sources, but priority remains unverified. No new global width
bound is asserted.
