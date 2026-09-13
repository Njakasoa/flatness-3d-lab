# Independent review of the thirteen-variable cubic formulation

Reviewed `proofs/PAIR_CUBIC_FORMULATION.md`, `experiments/pair_cubic_width_identities.py`, and `certificates/pair_cubic_width_identities.json`.

**Outcome: no material mathematical discrepancy found.** The proposed formulation is an algebraic reformulation of the stated necessary model. It is not an implemented solver, infeasibility certificate, class elimination, width upper bound, or priority claim.

## Independent serialized-identity check

Reconstructed the eight-parameter row-stochastic matrix directly in SymPy, without importing the generator, and parsed the serialized determinant and all eighteen quotient polynomials. The serialized determinant equals the direct symbolic determinant and has degree three. Every quotient equals the direct oriented adjugate-product numerator divided formally by the determinant, checked by expanding the difference to zero. All quotients have degree at most two, and coverage is exactly the three coordinate axes times six unordered pairs, with no duplicates. The check printed:

```
PASS independent serialized cubic determinant and all 18 oriented quotients
```

The coordinate-value matrix used independently was `[[0,2,0,0],[0,1,1,0],[0,1,0,1]]`, corresponding to the established four contact points. Linearity extends these identities to every direction.

## Orientation and denominators

Expanding `(d^T S)_j C_k-(d^T S)_k C_j` and collecting an unordered pair of contact indices gives `(d_i-d_ell)(S_ij S_ell,k-S_ik S_ell,j)`. Jacobi's identity uses the complementary rows of the original matrix indexed by the complement of `{j,k}`, and complementary columns indexed by the complement of `{i,ell}`, with sign `(-1)^(i+ell+j+k)`. The proof and generator have this orientation correctly.

Since `C_j=delta*r_j`, dividing the identity by `C_j*C_k` leaves `Q_jk/(delta*r_j*r_k)`. There is exactly one surviving determinant factor in the denominator. Positivity of `delta` and of every `r_j` is explicitly imposed, so clearing this denominator preserves strict inequality. Taking both signs of each unordered pair yields exactly directional width greater than the stated positive target `17/5`.

## Equivalence, boundedness, and degree

The pair-matrix lemma and the retained chart conditions imply invertibility and positive determinant. Hence `A^T r=ones` uniquely specifies `r=A^{-T}ones`, the inverse column sums. Requiring all four components to be positive retains the bounded-simplex condition; it has not been silently dropped. Conversely, an admissible bounded matrix has a unique auxiliary assignment, so the lift introduces no extra projected feasible matrices when the same remaining constraints are included.

The thirteen-variable count is eight facet parameters plus four column sums plus one determinant. The maximum total degree is three: matrix-column-sum equations are quadratic, the determinant equation is cubic, each adjugate entry has degree at most three, domain-bound products `delta*r_j` are quadratic, and width products `delta*r_j*r_k` are cubic. The constant-vector argument for the determinant degree is valid because every row sums to one. Fixed-contact lattice exclusions remain affine in facet parameters.

Equivalence is conditional on retaining the same width-direction list, geometric domain bounds, symmetry normalization, and lattice-exclusion scope. This review does not independently re-establish the earlier completeness theorem for the 37 directions or the earlier geometric bound derivations. The formulation explicitly requires those ingredients to remain. Its caveat that a partial 216-point box only provides a necessary hollowness relaxation is correct; the algebraic reformulation does not strengthen that logical status. No solver run was performed.
