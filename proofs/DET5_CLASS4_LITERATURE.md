# Bounded literature audit: determinant-5 contact class 4

Date: 2026-09-14. Four focused primary-source queries beyond the preceding
[height-exclusion audit](HEIGHT_EXCLUSION_LITERATURE.md). No solver was queried.

## Statement being compared

The candidate states that a full-dimensional hollow real tetrahedron K has
lattice width at most 17/5 if one can select a lattice point in the relative
interior of each of its four facets whose full four-point hull is affine
unimodularly equivalent to

    P = conv(0, (5,1,1), e2, e3).

This is repository class 4. The other determinant-5 class,
`conv(0,(5,1,2),e2,e3)`, is not excluded by this statement. Neither is an
arbitrary nonsimplicial hollow body containing P. The number 5 is normalized
volume, not the number of lattice points.

The research campaign reports infeasibility of five complete normalized
Y-height branch roots by linear McCormick outer relaxation, with no rectangle
subdivision, plus a separate full-12-entry barycentric encoding in cvc5 and
five checked Ethos proofs. This audit does not independently reproduce those
checks. It assesses whether the resulting geometric claim was already located
in the bounded literature search.

**No equivalent bound for this contact class was located. Priority remains
unconfirmed; absence from these queries is not a novelty proof.**

## The contact type and its symmetry are classical

Blanco and Santos, *Lattice 3-polytopes with few lattice points*,
[arXiv:1409.6701v3](https://arxiv.org/pdf/1409.6701), Theorem 2.4 and Lemma 2.6,
p. 6, recall White's empty-tetrahedron classification and the associated vertex
equivalences. Their normal form is
`T(p,q)=conv(0,(1,0,0),(0,0,1),(p,q,1))`, with equivalence precisely
`p' = ±p^(±1) mod q`. Their main five-lattice-point classification concerns a
different parameter from determinant five and does not state the candidate
bound for real circumscribed tetrahedra.

Here are explicit coordinate comparisons, calculated for this audit:

- `(X,Y,Z) -> (Y,X,Z)` sends class 4 to `T(1,5)`.
- `(X,Y,Z) -> (Z,X,Y)` sends the other determinant-5 class to `T(2,5)`.
- The corresponding White parameter orbits are `{1,4}` and `{2,3}` modulo 5.

Thus the distinction between these contact types is classical, and the proof
must retain it. The existence of symmetries of the inscribed contact hull does
not require every circumscribed K to share those symmetries. Using these maps
to identify equivalent cases is legitimate; restricting K itself to a
symmetric subfamily requires an additional theorem.

Codenotti and Santos, *Hollow polytopes of large width*,
[arXiv:1812.00916](https://arxiv.org/pdf/1812.00916), Section 5 and Theorem 5.1,
pp. 8–9, obtains the value `2+sqrt(2)` within an explicitly symmetric family
circumscribed about a unimodular contact simplex. That theorem does not provide
the present determinant-5 bound or a rule making an arbitrary K inherit the
symmetry of its four contacts.

## The immediate intrinsic gauge argument does not reach 17/5

The following is a direct calculation, included to check an obvious possible
antecedent rather than to claim a new lemma. Write `A=1+2/sqrt(3)`. In the
ordered contact tetrahedron above, the barycentric difference coordinates of
an integer vector `(X,Y,Z)` are

    ell = (X-5Y-5Z, X, 5Y-X, 5Z-X)/5,
    gamma_(P-P)(X,Y,Z) = (|ell_0|+...+|ell_3|)/2.

For `X` not divisible by 5, all four integer numerators are nonzero, since
their residues are `(X,X,-X,-X)`. Therefore the gauge is at least 2/5. For
`X` divisible by 5, ell is an integer zero-sum vector; a nonzero input gives
a nonzero ell, hence gauge at least 1. The vector `(1,0,0)` attains 2/5.
Consequently `lambda_1(P-P)=2/5` exactly.

For every hollow K containing P, monotonicity and
[ACMS Lemma 5.1, equation (14)](https://arxiv.org/pdf/1907.06199) give

    1 - A/w(K) <= lambda_1(K-K) <= lambda_1(P-P) = 2/5,
    w(K) <= 5A/3 = 5/3 + 10/(3*sqrt(3)) ≈ 3.59117 > 17/5.

Thus this direct intrinsic use of the published inequality does not establish
the candidate exclusion. This does not rule out stronger classical arguments
combining other inequalities. ACMS Theorem 5.4 permits contact tetrahedra of
normalized volume up to 17 for a width maximizer and does not by that bound
alone remove determinant five. The fixed-contact algebraic programme and
McCormick antecedents are documented in the
[preceding audit](HEIGHT_EXCLUSION_LITERATURE.md).

## Search limits and safe description

The four additional query strings were:

1. `"lattice width" tetrahedron "5" "contact"`
2. `"hollow tetrahedron" "17/5"`
3. `"tetrahedron" "5,1,1" width`
4. `"empty tetrahedra" "width" "five" flatness`

Most exact-coordinate results were unrelated. Search aggregators were not
used as mathematical authorities. The direct inspections were the primary
papers linked above; the inaccessible thesis and alternate-coordinate search
limitations recorded in the preceding audit remain. There was no exhaustive
search under every White or Reeve normal form, no author contact, and no
complete audit of all possible classical consequences.

Safe description: **an explicit 17/5 contact-class exclusion with finite linear
relaxation certificates, beyond the immediate intrinsic bound 5A/3; no matching
statement located in this bounded audit, with priority unconfirmed.** The fact
that no subdivision is needed is a property of this certificate campaign,
not by itself a new general optimization method or a global flatness theorem.
