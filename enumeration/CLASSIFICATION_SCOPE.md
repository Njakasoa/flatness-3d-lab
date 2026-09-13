# Classification scope for the three-dimensional contact reduction

**Cut-off:** 2026-09-13.  **Status:** a theorem-backed scope for computation, not a
completed classification and not a claim that the listed branches exhaust all
ways to attack the flatness conjecture.

## What the ACMS reduction actually gives

Let \(K\) be a convex body that attains the three-dimensional flatness
constant.  Codenotti--Freyer, Proposition A.1, supplies such an attained
maximizer.  Replace \(K\) by a maximal lattice-free representative.  The
Lovász blocked-facet theorem, used as Proposition 5.3 in Averkov--Codenotti--
Macchia--Santos (ACMS), gives a lattice point in the relative interior of every
facet.  Choosing one blocked point per facet produces an inscribed empty lattice
polytope \(P\).

ACMS Theorem 5.4 says that, up to \(\mathrm{GL}_3(\mathbb Z)\) and translation,
one may take either

* the two-dimensional square \(\operatorname{conv}(0,e_1,e_2,e_1+e_2)\), or
* a full-dimensional empty lattice 3-polytope with ordinary Euclidean volume
  \(\operatorname{vol}(P)\leq 22/3\).

When \(P\) is a tetrahedron, ACMS sharpen this to
\(\operatorname{vol}(P)\leq17/6\).  For a lattice tetrahedron \(P\),
\(6\operatorname{vol}(P)=|\det(v_1-v_0,v_2-v_0,v_3-v_0)|\), so the corresponding
normalized determinant bounds are \(44\) for the general full-dimensional
branch and \(17\) for the tetrahedral branch.  ACMS state that fixing one of
the finitely many possible \(P\)'s leaves finitely many cases up to unimodular
equivalence, but they do not enumerate or solve those cases.  Their square
branch remains open.

The source of the reduction is [ACMS, arXiv:1907.06199, Theorem 5.4](https://arxiv.org/abs/1907.06199).
The attainment input is [Codenotti--Freyer, arXiv:2307.09429, Proposition A.1](https://arxiv.org/abs/2307.09429).

### Maximizer-only qualification

The volume and determinant bounds above apply to an **attained width maximizer
after the maximal-body/contact reduction**.  They are not a bound on every
hollow body, every arbitrary counterexample candidate, or every near-maximizer
before this reduction.  Likewise, a finite enumeration of \(P\)'s does not by
itself prove the global flatness conjecture: each fixed \(P\) still requires a
real/algebraic optimization and a proof that all relevant lattice directions
are controlled.

## Computational branches

| Branch | Objects to enumerate or optimize | Theorem-backed scope | Status at cut-off | What would still be needed |
|---|---|---|---|---|
| A. Tetrahedral contact branch | Empty lattice tetrahedra \(P\subset\mathbb R^3\), up to translation and \(\mathrm{GL}_3(\mathbb Z)\), with \(D=6\operatorname{vol}(P)\leq17\) | ACMS Theorem 5.4, conditional on \(P\) being the contact polytope of a width maximizer | Finite HNF/empty-simplex computation is an appropriate next step; no complete output is asserted here | Prove completeness of the HNF orbit list, verify emptiness exactly, then solve the fixed-\(P\) real/algebraic contact problem |
| B. Non-simplicial full-dimensional branch | Empty lattice 3-polytopes \(P\) with normalized volume \(D=6\operatorname{vol}(P)\leq44\) | ACMS Theorem 5.4 | Finite in principle up to unimodular equivalence, but no enumeration is supplied by ACMS or this scope note | Include all combinatorial types, not only tetrahedra; certify duplicate removal and solve every fixed-\(P\) contact problem |
| C. Square branch | \(P=\operatorname{conv}(0,e_1,e_2,e_1+e_2)\) in an affine plane | Explicit alternative in ACMS Theorem 5.4 | Open in ACMS; must remain in any “complete” computation | Treat the lower-dimensional contact geometry separately and prove how the surrounding 3D body is constrained |
| D. Fixed-\(P\) body optimization | Maximal hollow real convex bodies \(K\) with selected blocked contacts realizing a fixed \(P\) | ACMS Proposition 5.3 and the final discussion of Section 5 | First-order real algebra gives a theoretical decision procedure; ACMS report practical quantifier elimination as too slow/complex | Handle algebraic facet coefficients, all facets and relative-interior contacts, hollowness, and the lattice-width minimum exactly |
| E. Integral maximality context | Integral lattice-free polyhedra, modulo unimodular equivalence | AWW classification; AKW equivalence of \(\mathbb R^3\)- and \(\mathbb Z^3\)-maximality for integral polyhedra | Exactly 12 bounded and 2 unbounded classes in that integral class | Do not substitute this list for Branches A--D; it excludes general real/algebraic facet positions |

## Branch A: exact enumeration contract

The tetrahedral computation may normalize one vertex to \(0\) and write

\[
 P=\operatorname{conv}(0,v_1,v_2,v_3),\qquad
 D=|\det(v_1,v_2,v_3)|\leq17.
\]

An HNF representative is useful for a finite search, but an HNF list is not
yet a classification.  A completed branch-A result must document all of the
following:

1. **Orbit coverage.** The chosen row/column HNF convention, bounds, and the
   argument that every \(\mathrm{GL}_3(\mathbb Z)\)-orbit has a representative
   in the searched list.
2. **Exact emptiness.** Check that no lattice point lies in the relative
   interior of \(P\), including points on proper faces when “empty” is used in
   the lattice-polytope sense.  Record the convention explicitly.
3. **Duplicate removal.** Identify tetrahedra equivalent under translations,
   unimodular maps, and vertex permutations; determinant alone is not an orbit
   invariant strong enough to remove duplicates.
4. **Contact geometry.** For every fixed \(P\), distinguish a selected contact
   point in the relative interior of a facet from a point merely on the facet
   boundary.  The ACMS reduction uses relative-interior blocked contacts.
5. **Real/algebraic facets.** Allow facet planes of \(K\) to have real or
   algebraic coefficients.  Integral contact points do not imply integer facet
   normals: the Codenotti--Santos tetrahedron has irrational facet normals.
   Restricting normals to \(\mathbb Z^3\) would solve a different problem.
6. **Width certificate.** Verify the minimum over all nonzero dual-lattice
   directions, either by an exact support-function argument or by a finite
   path/cone certificate with a proof covering the complement.  A sample of
   short integer directions is not a width proof.
7. **Hollowness and exact inequalities.** Use exact rational/algebraic
   predicates (or certified intervals), rather than floating-point tests that
   can misclassify a boundary contact.
8. **Maximizer logic.** State where attainment, maximality, and the ACMS
   volume theorem enter.  The determinant cutoff is conditional on the
   contact-reduction hypotheses and must not be presented as a cutoff for all
   hollow tetrahedra.

The branch-A computation can therefore provide a finite list of candidate
contact polytopes.  It cannot, by itself, establish
\(\operatorname{Flt}(3)=2+\sqrt2\), prove that a listed \(P\) is realizable as
the contact polytope of a maximizer, or eliminate Branches B and C.

## Contact points versus facet normals

The Codenotti--Santos lower-bound tetrahedron is the required test case for
this distinction.  Its contacts in the affine lattice are

\[
(-1,-1,-1),\ (1,-1,1),\ (1,1,-1),\ (-1,1,1),
\]

but the facet through the last three vertices has normal, up to scale,

\[
(3+2\sqrt2,\ 1+\sqrt2,\ 2+\sqrt2),
\]

which is not proportional to an integer vector.  Any code or theorem using
blocked lattice contacts must retain real/algebraic facet normals and test
relative-interior incidence directly.

## What this scope does not claim

* Enumerating determinant-\(\leq17\) tetrahedra is not an exhaustive
  classification of all empty lattice 3-polytopes, nor of all maximal hollow
  bodies.
* The determinant-\(\leq44\) statement concerns an inscribed contact polytope
  attached to an attained maximizer, not an arbitrary lattice-free body.
* The 12 bounded plus 2 unbounded AWW/AKW classes are integral-polyhedron
  classes.  They are not all real maximal lattice-free bodies and do not
  classify the algebraic Codenotti--Santos candidate.
* The Codenotti--Santos \(2+\sqrt2\) theorem is exact only in their restricted
  symmetric family; ACMS local maximality and \(3.972\) universal upper bound
  leave the global equality open.
* A search through the 2026 cut-off found no primary source changing the
  classical 3D range, but this is a bounded literature audit rather than an
  exhaustive novelty claim.

## Primary references for the scope

* [Averkov--Codenotti--Macchia--Santos, arXiv:1907.06199](https://arxiv.org/abs/1907.06199), especially Theorem 5.4 and the final paragraphs of Section 5.
* [Codenotti--Freyer, arXiv:2307.09429](https://arxiv.org/abs/2307.09429), Proposition A.1 (attainment).
* [Codenotti--Santos, arXiv:1812.00916](https://arxiv.org/abs/1812.00916), Section 5 (algebraic candidate and contacts).
* [Averkov--Wagner--Weismantel, arXiv:1010.1077](https://arxiv.org/abs/1010.1077) and [Averkov--Krümpelmann--Weltge, arXiv:1509.05200](https://arxiv.org/abs/1509.05200), integral maximality classification.

**Proof-scope refinement.** ACMS states the volume/contact theorem for attained maximizers. Replaying its body-volume inequalities proves the same body-volume window for every hollow K with w(K)>=2+sqrt2, regardless of maximality. Applying a determinant cutoff to a chosen contact tetrahedron additionally requires that it be an empty inscribed contact hull as in the theorem; arbitrary hollow tetrahedra need not have four blocked facets.
