# Maximal-hull and inscribed-polytope reduction

This note reconstructs Sections 5.3 and the end of 5.4 of Averkov,
Codenotti, Macchia and Santos, *A local maximizer for lattice width of
3-dimensional hollow bodies*, arXiv:1907.06199v2. See [the primary
paper](https://arxiv.org/abs/1907.06199) and the checked local extraction
the article linked in [papers/README.md](../papers/README.md).

The reduction is a search-space theorem for a global width maximizer. It is
not a classification of all hollow bodies and it does not eliminate the
two-dimensional square case.

## Maximal hollow hulls and facet contacts

A hollow convex set is inclusion-maximal if no strictly larger convex set is
hollow in the same lattice. Proposition 5.3 (the Lovász theorem cited by the
paper) says:

> Every maximal hollow convex set `K` is a polyhedron and has at least one
> lattice point in the relative interior of each facet.

The paper applies this to a lattice-width maximizer, using the standard
maximal-hull reduction: enlarge a maximizing body to an inclusion-maximal
hollow hull; lattice width is monotone under containment, so the hull still
has the maximum width. The source does not spell out the extension argument or
the compactness/Zorn details. Any implementation should state this step as an
assumption or cite a maximal-hollow-set existence theorem.

Choose one relative-interior lattice contact from each facet and let `P` be
their convex hull. The paper says that the contacts can be chosen so that `P`
is an empty lattice polytope (its only lattice points are its vertices). The
supporting-facet argument behind this assertion is that a nonvertex lattice
point of the convex hull of contacts from distinct facet interiors would lie
in the interior of `K`, contradicting hollowness; the paper does not give the
full selection proof. The local tetrahedron uses the special empty inscribed
polytope `conv(p_1,...,p_4)`.

## Theorem 5.4, exactly

Let `K` be a width maximizer among hollow convex 3-bodies and let `P` be an
empty lattice polytope inscribed in `K`, meaning that `P` contains at least one
lattice point from the relative interior of each facet of `K`. Then, up to
unimodular equivalence, `P` is either

$$
\operatorname{conv}(0,e_1,e_2,e_1+e_2),
$$

or a three-dimensional empty lattice polytope with

$$
\operatorname{vol}(P)\le\frac{22}{3}.
$$

If `P` is a tetrahedron, the stronger bound is

$$
\operatorname{vol}(P)\le\frac{17}{6}.
$$

All volumes here are normalized to a fundamental cell of the ambient lattice.

## Proof reconstruction

Since `K` is three-dimensional, it has at least four facets. Contacts from
relative interiors of three distinct facets are not collinear, so `P` has
dimension at least two; the facet-separating supports also make the chosen
contacts vertices of `P`. There are two cases.

### The two-dimensional case

An empty lattice polygon with at least four vertices is, up to affine
unimodular equivalence, the square

$$
\operatorname{conv}(0,e_1,e_2,e_1+e_2).
$$

This is the only two-dimensional inscribed type. The paper explicitly says
that it would be desirable to rule out this square case, but currently does
not know how to do so.

### The three-dimensional case

Howe's theorem (cited as [20], Scarf) says that every empty lattice 3-polytope
has lattice width one. In the notation `C_P=P-P`, this means that `C_P`
meets only three consecutive lattice layers and that every smaller
`lambda C_P`, `0<lambda<1`, meets at most one lattice layer. Hence

$$
\lambda_3(C_P)=1.
$$

Minkowski's second theorem gives

$$
\operatorname{vol}(C_P)
\le\frac{8}{\lambda_1(C_P)\lambda_2(C_P)\lambda_3(C_P)}
=\frac{8}{\lambda_1(C_P)\lambda_2(C_P)}
\le\frac{8}{\lambda_1(C_P)^2}. \tag{M2}
$$

Brunn–Minkowski and the inclusion `P subset K` then give

$$
\operatorname{vol}(P)
\le\frac18\operatorname{vol}(C_P)
\le\frac1{\lambda_1(C_P)^2}
\le\frac1{\lambda_1(K-K)^2}. \tag{A}
$$

For a body of width at least `w_0=2+sqrt(2)`, Lemma 5.1 and (14) in the
paper give

$$
\lambda_1(K-K)\ge
\alpha:=1-\frac{1+2/\sqrt3}{2+\sqrt2}
=0.3689028237\ldots. \tag{16}
$$

Substituting this into (A) gives

$$
\operatorname{vol}(P)\le\alpha^{-2}
=7.3481166321\ldots. \tag{B}
$$

For every lattice 3-polytope, `6 vol(P)` is an integer: triangulate into
lattice tetrahedra, each of normalized Euclidean volume an integer divided by
`6`. Since

$$
6\alpha^{-2}=44.0886997931\ldots<45,
$$

the integer `6 vol(P)` is at most `44`, hence

$$
\operatorname{vol}(P)\le\frac{44}{6}=\frac{22}{3}.
$$

### Tetrahedral improvement

If `P` itself is a tetrahedron, equality holds in the Rogers–Shephard ratio:

$$
\operatorname{vol}(P-P)=20\operatorname{vol}(P).
$$

Using this equality in place of the Brunn–Minkowski factor in (A) gives

$$
\operatorname{vol}(P)
\le\frac1{20}\operatorname{vol}(C_P)
\le\frac{2}{5\lambda_1(C_P)^2}
\le\frac25\alpha^{-2}
=2.9392466528\ldots.
$$

Now `6 vol(P)` is an integer strictly below `18` (the exact replay gives
`6*(2/5)*alpha^(-2)=17.6354799172...`), so `6 vol(P)<=17` and

$$
\operatorname{vol}(P)\le\frac{17}{6}.
$$

## What this reduction does and does not provide

Theorem 5.4 supplies a finite search-space principle: after fixing a
full-dimensional inscribed empty polytope `P` up to unimodular equivalence,
one can search only bodies containing that contact configuration. The paper
does not enumerate all equivalence classes. Finiteness uses the bounded-volume
classification of empty 3-polytopes; it is a separate enumeration task.

For fixed full-dimensional `P`, the global volume upper bound from Theorem 5.2
can be converted into a bounded region `B` (for example, a box depending only
on `P`) containing `K`. The paper does not give an explicit formula for `B`.
Once `B` is available, only finitely many lattice points in `B` can matter for
hollowness, so the condition can be encoded by finitely many polynomial
inequalities. In principle, the statement “every hollow convex body in the bounded search family with this fixed
`P` has width at most `2+sqrt(2)`” is then first-order real algebra and hence
decidable by quantifier elimination. The source warns that the resulting
sentences are far too large for a practical brute-force proof.

The square `P=conv(0,e_1,e_2,e_1+e_2)` remains an explicit unresolved branch.
The reduction also inherits the unproved external inputs: Lovász maximal
hulls, Howe/Scarf width one for empty 3-polytopes, Minkowski's second theorem,
and the global maximizer/existence step.
