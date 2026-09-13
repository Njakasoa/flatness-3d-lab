# An intrinsic obstruction for contained empty tetrahedra

Date: 2026-09-13. Status: exact result with independent computational replay
and internal adversarial review; external novelty unverified. This does not settle a surrounding body's
continuous optimization or the three-dimensional flatness conjecture.

Write A=1+2/sqrt(3), w0=2+sqrt(2). Volumes are Euclidean volumes with the
ambient integer fundamental cell of volume one. An empty lattice tetrahedron
contains no lattice points other than its four vertices, including on its
boundary. A hollow convex body has no interior lattice points.

## Containment inequality

For every compact full-dimensional hollow convex body K and every
full-dimensional empty lattice tetrahedron P contained in K, put
ell=lambda_1(P-P). If ell<1, then

    w(K) <= A/(1-ell).                                      (1)

Indeed, ACMS Lemma 5.1 gives 1<=A/w(K)+lambda_1(K-K), and inclusion gives
lambda_1(K-K)<=lambda_1(P-P). Rearranging proves (1). No maximality,
facet-interior contact or attainment of a global supremum is needed.
Thus this can be applied to any four affinely independent lattice vertices
of an empty contact polytope with more than four vertices as well.

## A planar improvement of the determinant bound

Let N=6 vol(P). White's width-one theorem for empty lattice tetrahedra gives
a primitive integer height with all vertices in two consecutive layers.
If three vertices are in one layer, their triangle is empty in that layer's
integer lattice, so Pick's theorem makes its normalized area one. The
remaining vertex is at lattice height one, and N=1.

Otherwise two vertices lie in each layer. After a lattice choice of
coordinates, write

    P=conv((0,0),(u,0),(v,1),(v+s,1)), u,v,s in Z^2.

Here N=|det(u,s)|. At height t, P has section
(1-t)[0,u]+t[v,v+s]. Subtracting two points at the same height and taking
the union over 0<=t<=1 proves the exact identity

    (P-P) intersect {height=0} = conv(+u,-u,+s,-s).

The right side is a centrally symmetric diamond of area 2N in the planar
lattice. Minkowski's first theorem, applied with an arbitrarily small
enlargement and then discreteness, bounds its first minimum by sqrt(2/N).
Every planar integer vector is also an ambient integer vector. Consequently

    N ell^2 <= 2.                                          (2)

The N=1 case follows from ell<=1, witnessed by any primitive integer edge.
The argument actually gives ell=min(1,lambda_1(diamond)): for dilations
strictly less than one, every ambient integer point lies in the zero-height
layer. Equation (2) improves the factor 12/5 obtained by applying the
three-dimensional second theorem of Minkowski to the full difference body.

In particular w(K)>3A/2 implies ell>1/3 and N<18, hence N<=17.
The threshold w(K)>11A/7 implies ell>4/11 and N<121/8, hence N<=15.
Finally w(K)>=w0 implies ell>=alpha=1-A/w0. Independently squared rational
radical intervals give alpha>0.368902823735021 and 15 alpha^2>2, so N<=14.

## Exact first minima and the explicit list

Our complete HNF enumeration through determinant 21 supplies 51 affine
unimodular classes. This larger cutoff is justified without (2): ACMS's
width-one/Minkowski argument gives N<=12/(5 ell^2); when ell>1/3 this gives
N<108/5, hence N<=21. Thus the computation also checks the planar improvement
against an independently obtained larger search space.

The canonical representatives found by complete enumeration are unimodular,
or of the form

    T(N,a)=conv(0,(N,1,a),(0,1,0),(0,0,1)), gcd(a,N)=1.

This form is an output check, not a restriction imposed on the HNF search.
For N>1 their first minima have the independent one-dimensional formula

    ell = min_{1<=k<N} [d_N(k)+d_N(a*k mod N)]/N,
    d_N(r)=min(r,N-r).                                    (3)

To prove (3), affine difference barycentric coordinates of a vector
(x,y,z) are (a*x/N-y-z, x/N, y-x/N, z-a*x/N). Their sum is zero,
and the difference-body gauge is the sum of their positive parts.
For a nonzero residue k=x mod N, their fractional parts are a permutation
of (t,1-t,r,1-r), where t=k/N and r=(a*k mod N)/N. Each choice of integer
parts whose total makes the sum zero is realized by an integer ambient
vector. A minimizing choice subtracts one from two fractional parts, leaving
the two smallest positive. To see that other integer parts cannot improve
it, replace any component outside (-1,1) by shifting one unit toward zero
and compensating on an opposite-sign component; this cannot increase the
sum of positive parts and terminates. Of the four numbers, the two smallest
have sum min(t,1-t)+min(r,1-r). The zero residue has integer barycentric
coordinates and minimum one for nonzero vectors. The nonzero-residue
expression is at most one, proving (3).

The main implementation independently computes the gauge in a complete
ambient integer box: an integer edge witnesses ell<=1, and any vector of
gauge <=1 lies in P-P, hence between the coordinate extrema of P-P.
Nonprimitive vectors can be omitted by homogeneity, and sign by symmetry.
This returns every minimizing primitive direction modulo sign, with exact
affine difference coefficients. Both computations agree for all 51 classes.

For w(K)>3A/2=3/2+sqrt(3), every contained empty tetrahedron belongs to one
of the following eleven classes. For w(K)>11A/7, delete the marked row,
leaving exactly ten *necessary possibilities*. They need not all be realizable
inside a body of that width.

| N | a | ell | threshold exclusion |
|--:|--:|:---:|:---|
| 1 | unimodular | 1 | |
| 2 | 1 | 1 | |
| 3 | 1 | 2/3 | |
| 4 | 1 | 1/2 | |
| 5 | 1 | 2/5 | |
| 5 | 2 | 3/5 | |
| 7 | 2 | 3/7 | |
| 8 | 3 | 1/2 | |
| 10 | 3 | 2/5 | |
| 11 | 3 | 4/11 | excluded when w>11A/7 |
| 13 | 5 | 5/13 | |

The threshold 11A/7 is approximately 3.385958, below w0. At w>=w0,
exact interval comparisons give the same ten possibilities. In particular
the normalized determinant is at most 13 after finite elimination.
Strict and non-strict endpoints are intentional; a type at equality in (1)
cannot be deleted at its own threshold without an additional argument.

## Scope and remaining work

This sharpens the explicitly computed tetrahedron list. It is not a list of
all surrounding hollow bodies. In particular the unimodular type, the
coplanar square branch and continuous facet parameters remain unresolved.
The same necessary condition applies to every tetrahedron selected from a
larger empty contact hull, but compatibility and completeness of any extension
enumeration require a separate proof. Novelty of the planar bound and of
the ten-class corollary is not yet established.

Primary inputs: [ACMS, Lemma 5.1 and Theorem 5.4](https://arxiv.org/abs/1907.06199),
White's empty-tetrahedron theorem, and the first and second theorems of
Minkowski. Computational outputs: `certificates/contact_obstructions.json`,
`results/empty_tetrahedra_through_21.json`. Enumeration details are in
`enumeration/HNF_COMPLETENESS.md`; its final original scope warning is
superseded by the direct containment argument above.
