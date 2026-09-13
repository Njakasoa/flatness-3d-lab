# Independent review of the pair matrix structure

Reviewed `proofs/PAIR_MATRIX_STRUCTURE.md`, `experiments/pair_matrix_structure.py`, and the serialized `certificates/pair_matrix_structure.json` using the local virtual environment's SymPy. The verification reconstructed the twelve-variable matrix independently, read the JSON directly, and did not import the generator.

**Outcome: no material mathematical or certificate discrepancy found.** This is a matrix-structure result, not a flatness upper bound, branch elimination, or novelty claim.

## Formal certificate checks

- The serialized variable order is exactly four surplus variables followed by the eight directed cross-group edge variables. Monomial exponent vectors are nonnegative integers of length twelve, with no duplicate monomials within a polynomial.
- SymPy's direct determinant equals the serialized determinant as a polynomial in all twelve independent variables. There are exactly 45 terms, each with positive coefficient and at least one surplus variable. Each of the four possible single roots has four spanning-tree terms.
- All sixteen serialized adjugate polynomials equal SymPy's adjugate in their stated positions. In particular, the cofactor transpose is correct. Every coefficient is positive and every entry has an edge-only term.
- Independently expanded `M * adj(M) - det(M) * I` vanishes entrywise. The adjugate monomial counts are `[[21,6,9,9],[6,21,9,9],[9,9,21,6],[9,9,6,21]]`.

These are formal coefficient comparisons, not sampled checks. With all eight edges strictly positive, the edge-only adjugate terms prove strict positivity even on surplus boundaries. The single-root determinant terms prove strict positivity whenever any surplus is positive; all-zero surplus makes every determinant term vanish.

## Orientation and boundaries

Writing `P` for the permutation matrix of `(01)(23)`, the chart gives `B=A P`, `M=J A P J`, and therefore `A^{-1}=P J M^{-1} J`. Both swaps together have determinant positive one. The left multiplication by `P` only exchanges inverse rows within their groups, preserving the claimed block signs. The proof uses the correct permutation and inverse orientation.

As supplementary exact rational checks, all sixteen subsets of rows at designated value `1/2` were tested, taking the remaining designated entries as `3/4` and splitting each row's remaining mass equally. The all-half case has rank three; each other case has positive determinant and the claimed strict inverse signs. The inverse permutation/conjugation formula also holds in each nonsingular case. These checks supplement the formal identity rather than replace it.

Strict positivity of all off-diagonal entries is essential to the strict conclusions and connectivity argument; the statement correctly retains that hypothesis. Simultaneous designated equality is allowed in the domain but is singular, exactly as stated.

## Boundedness caveat

Positive determinant does not imply positive inverse column sums, even under every stated chart condition. For example,

```
A = [[0,   1/2,  1/10, 2/5],
     [1/2, 0,    1/10, 2/5],
     [1/10,2/5,  0,    1/2],
     [1/10,3/20, 3/4,  0  ]]
```

has determinant `1/80`, while its inverse column sums are `[34/5, 16/5, -6, 0]`. Thus column-sum positivity must remain a separate condition. The proof explicitly preserves this requirement and only transfers inverse signs to normalized vertex contacts after assuming positive column sums. There is no boundedness inference from invertibility in the reviewed statement.

## Follow-up: symmetry normalization

The appended symmetry normalization is valid for genuine hollow bodies up to **affine** lattice equivalence. Independently reconstructed all 24 affine maps permuting the four contacts `(0,0,0), (2,1,1), (0,1,0), (0,0,1)`; every linear part has integral entries and determinant `+1` or `-1`. The translation is an integral contact point. Thus the precise group is integral translations together with `GL(3,Z)`, as the proof states, rather than only origin-fixing linear maps.

Independently enumerated the eight permutations commuting with `(01)(23)` and matched the new serialized list exactly. For every one of the 256 tuples in `{0,1,2,3}^4`, a centralizer permutation makes the first designated entry maximal and puts the third at least as large as the fourth. This directly covers all weak order types, including ties, in addition to the generator's 24 strict order types. Simultaneous row/contact relabeling sends each designated entry to the corresponding permuted designated entry because the relabeling commutes with the blocker permutation. Therefore the normalized inequalities preserve a representative of every genuine pair-branch body.

Affine unimodular maps preserve hollowness and lattice width. Universal geometric domain bounds apply again to the transformed genuine body. A fixed partial lattice test box such as `[-2,3]^3` need not be preserved, so this argument does not give an equivalence on all feasible points of a nonhollow partial-box relaxation. The appended proof explicitly makes this distinction correctly. No material issue found in the new normalization section or its serialized symmetry data; the unchanged formal polynomial identity was not repeated for this follow-up.

## Reproducible independent replay

Saved the independent verifier as `tests/replay_pair_matrix_independent.py`. It reads the serialized JSON directly, never imports the generator, and uses explicit exceptions so checks remain active under optimized Python. It also rejects a deliberately corrupted determinant coefficient and a missing adjugate entry.

Executed successfully:

```
.venv/bin/python -O tests/replay_pair_matrix_independent.py
PASS: 45 determinant terms; 16 adjugates; 16 boundary masks; 8 centralizers; 256 weak-rank tuples; 24 affine lattice maps; 2 corruption guards
```
