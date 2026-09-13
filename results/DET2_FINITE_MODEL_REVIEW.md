# Bounded review of the determinant-two finite algebraic reduction

Reviewed 2026-09-13. Scope: written mathematics in `proofs/DET2_FINITE_ALGEBRAIC_REDUCTION.md`, the local ACMS reconstruction, and relevant lines in the local paper text. No solver calls or SMT encoding review were performed.

## Finding

The necessary-relaxation argument is sound. One correction is needed before calling the full finite lattice-exclusion formulation equivalent to hollowness: the listed individual bounds `-62 <= T_ij <= 63` do not themselves imply the ambient bounds `-62 <= T_1j+T_2j <= 63` and `-62 <= T_1j+T_3j <= 63`. The tighter subset-sum bounds were derived using hollowness and the volume theorem, so cannot be assumed for arbitrary algebraic candidates when proving the converse. Add these ambient vertex bounds explicitly (or all subset-sum bounds), or enlarge the exclusion box to one implied by the individual bounds. This affects the claimed full-model sufficiency, not necessity or the validity of an UNSAT-based relaxation argument. No UNSAT result is claimed in the note.

## Verified components

- ACMS supplies the lower bound `lambda1 >= 1-(1+2/sqrt(3))/w`; Minkowski and Brunn–Minkowski give `vol(K) <= lambda1^(-3)`. These do not require a maximizing body once hollowness and the stated width hypothesis are supplied. At `w > 17/5`, replacing `1+2/sqrt(3)` by `13/6` gives `lambda1 > 37/102`. The volume bound is strictly below 21, with exact gap `2505/50653`.
- Since `vol(P)=1/3`, the visible-facet pyramid identity gives total negative barycentric mass below 62. Total positive mass is therefore below 63. Every individual coordinate and every subset sum lies in `(-62,63)`. The proposed smaller ambient box is valid for every genuine hollow candidate, and its inclusive integer cardinality is exactly `251*126*126 = 3,984,876`.
- For the four half-integral blockers, the facet value is `1/2-A_ij`. Thus `A_ij >= 1/2` correctly includes boundary equality. Strict positivity of the other off-diagonal entries permits at most one such entry per row. Covering all four columns forces a permutation with no fixed point, hence precisely cycle types `2+2` and `4`.
- All 24 contact permutations induce affine unimodular maps of the ambient lattice. In the barycentric hyperplane the lattice is exactly the union of all-integral and all-half-integral coordinate vectors; permutation and inverse permutation preserve it. The induced map is affine, rather than necessarily linear, when the origin contact is moved.
- `AT` positive diagonal and the column-sum constraints force both matrices invertible and force positive column sums of `A^(-1)`. They therefore give exactly the bounded simplex in the stated halfspaces. Conversely a bounded full-dimensional tetrahedron with the designated relative-interior contacts supplies this representation. No strict strengthening of `A_i,sigma(i) >= 1/2` is needed.
- Independent standard-library integer enumeration confirms 37 primitive directions modulo sign with contact width at most 3. The search bounds `|u_y|,|u_z| <= 3`, `|u_x| <= 4` are complete. All omitted directions have integral contact width at least 4, proving the threshold equivalence for `17/5` whenever `K` contains `P`. The disjunction over ordered vertex pairs correctly represents directional width strictly greater than the target.

Subject to the explicit ambient-bound correction above, the written finite reduction is mathematically sound. This review does not verify solver syntax, solver evidence, external novelty, or elimination of either branch.

## Closure

Reviewed the revised proof, which now explicitly imposes `-62 <= T_1j+T_2j <= 63` and `-62 <= T_1j+T_3j <= 63` for every vertex column. Together with the individual barycentric bounds, these force every algebraic candidate simplex inside the stated ambient box independently of hollowness. The full-box lattice exclusions are consequently sufficient as well as necessary for hollowness within this model. The finding is resolved in the written mathematics; no outstanding mathematical findings remain. Corresponding SMT implementation changes were outside this review.

## Auxiliary-variable elimination review

Reviewed the added final section. The determinant-sign homotopy is valid: after moving the designated entries to the diagonal, the row-stochastic matrix has diagonal at least one half; `(1-t)I+tB` has diagonal strictly larger than its off-diagonal row sum for every `t<1`. Its determinant is continuous, nonzero, and initially positive. At `t=1`, nonsingularity makes the limiting determinant positive, including designated-entry equality cases. The column permutation supplies precisely the blocker permutation sign.

Writing `delta = epsilon det(A) > 0`, one has `A^(-1) = S/delta`, so its column sums are `C_j/delta`. Thus positive `C_j` are exactly the bounded-simplex column-sum condition in this admissible nonsingular chart, and `T_ij=S_ij/C_j` follows. Clearing the two positive column denominators in a width comparison gives exactly `5 u dot (N_j C_k-N_k C_j) > 17 C_j C_k`; no inequality reversal or extra solution is introduced. The barycentric and ambient bounds transform correctly by the same positive denominators.

The row parameterization has eight independent real variables and keeps A affine; adjugate entries and column sums have degree at most three, determinant degree at most four, and the displayed width polynomials degree at most six. Lattice exclusions remain linear disjunctions. The claimed equivalence and degree bounds are sound. No solver result was checked or inferred, and no outstanding mathematical findings were introduced.
