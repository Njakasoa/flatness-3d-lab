# Exact matrix structure in the determinant-two pair branch

This is a simplification of the pair-branch feasibility model, not an
elimination of the branch or a width bound. It specializes elementary
diagonal-dominance and nonnegative-inverse arguments to this contact chart;
no mathematical novelty is claimed for those matrix arguments.

Let A be the four-by-four facet matrix, with diagonal zero, strictly positive
off-diagonal entries, row sums one, and designated entries

    a_0=A_01, a_1=A_10, a_2=A_23, a_3=A_32 >= 1/2.

Then:

1. A is nonsingular exactly when sum_i a_i > 2. In this case det(A)>0.
2. Every entry of A^{-1} is strictly positive within the two diagonal
   two-by-two blocks and strictly negative in the two off-diagonal blocks.
3. Thus a bounded simplex in this chart has the same sign pattern in its
   vertex contact coordinates T_ij. Positivity of the inverse column sums
   is still required separately for boundedness.

In particular, equality of some designated entries to 1/2 is retained.
Only their simultaneous equality is singular.

## Proof by a nonnegative polynomial identity

Permute the columns of A by sigma=(01)(23), obtaining B with diagonal a_i.
Its only off-diagonal entries join the groups {0,1} and {2,3}. Put

    J=diag(1,1,-1,-1),    M=JBJ.

The diagonal of M is a_i and its eight cross-group entries are negative.
Write their positive magnitudes as e_ij. Since their row sum is 1-a_i,

    M_ii = k_i + sum_j e_ij,    k_i=2a_i-1 >= 0,
    M_ij = -e_ij.

All eight e_ij are strictly positive. Treating the four k_i and eight e_ij
as independent formal variables, the determinant of this matrix is the
sum of the 45 directed rooted-forest monomials on the complete bipartite
graph with these two parts. Each vertex either contributes its root
variable k_i or an edge to its parent; cycles are excluded. All coefficients
are positive, every term has a root, and for each possible single root
there are four spanning-tree terms. Therefore det(M)=0 if all k_i=0, and
det(M)>0 if any k_i>0.

The coefficient identity is verified by expanding the determinant directly
with the Leibniz formula and, separately, enumerating all parent assignments
and discarding directed cycles. This finite formal identity holds for every
real specialization, without approximation or a sampled parameter domain.

Each of the sixteen entries of adj(M) also expands with positive coefficients
and contains a term involving only the positive edge variables. Consequently
every adjugate entry is strictly positive, including when some k_i vanish.
If any k_i>0, M^{-1}=adj(M)/det(M) is entrywise strictly positive.
The polynomial check also verifies M adj(M)=det(M) I in all sixteen entries.

Conjugating back gives B^{-1}=J M^{-1} J with the asserted block signs.
The column permutation has positive determinant and preserves each group;
undoing it permutes rows of the inverse within those groups. Hence det(A)>0
and A^{-1} has exactly the same block sign pattern. Finally, since a_i>=1/2,
some k_i>0 is equivalent to sum_i a_i>2. This proves all assertions.

For a bounded simplex the column sums r_j of A^{-1} are positive and
T_ij=(A^{-1})_ij/r_j, so the same signs apply to T. This step does not infer
boundedness from invertibility alone.

## Reproduction and use

Run `python3 -m experiments.pair_matrix_structure`. The standard-library
generator writes [the formal certificate](../certificates/pair_matrix_structure.json),
including all determinant and adjugate monomials. It uses explicit checks
that remain active under optimized Python.

In the pair-branch SMT model, the polynomial constraint det(A)>0 may be
replaced exactly by the linear constraint sum_i a_i>2. The known signs of
the signed adjugate may also be included as redundant inequalities. The
positive-column-sum conditions, all domain bounds, width comparisons, and
lattice exclusions remain necessary. This simplification does not apply
unchanged to the four-cycle branch, whose permuted off-diagonal graph has
a different structure.

## Symmetry normalization for a necessary feasibility model

All 24 permutations of the four determinant-two contacts induce affine
unimodular maps, as established in the finite algebraic reduction and its
exact permutation certificates. The eight permutations commuting with
sigma=(01)(23) preserve this particular blocker branch. They act transitively
on the four indices: swap the two pairs and swap within either pair.

Choose one largest designated entry and move it to index zero. The remaining
swap of indices two and three fixes zero, so it can arrange a_2>=a_3. Thus
every genuine pair-branch body is affine lattice equivalent to one satisfying

    a_0>=a_1, a_0>=a_2, a_0>=a_3, and a_2>=a_3.

All inequalities are weak and keep tied coefficients. The generator lists
the eight centralizing permutations and checks the normalization on all
24 strict order types; weak order types follow by breaking ties arbitrarily.

The polynomial domain bounds apply to every genuine hollow body above the
target width, including its normalized image. A fixed partial lattice box
need not be invariant under these affine maps. Consequently adding these
canonical inequalities is justified as a necessary model for a genuine
high-width hollow body up to equivalence. It is not asserted to preserve
every feasible nonhollow point of the earlier partial-box relaxation.
