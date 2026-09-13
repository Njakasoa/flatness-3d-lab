# Column normalization: eight variables and cubic inequalities

This note gives an equivalent chart for all bounded tetrahedra in the
determinant-two pair branch. It adds necessary ACMS cuts for the target width;
it does not assert that the resulting model is infeasible.

## A normalization which encodes boundedness

For an admissible row-normalized A let r=A^{-T}ones>0 and put

    F=diag(r) A.

Then F has zero diagonal, positive off-diagonal entries, and each column
sums to one. Multiplication of a facet inequality by r_i>0 preserves the
body and its designated relative-interior lattice contact. Pair dominance
becomes the four linear inequalities

    F_i,sigma(i) >= sum_{j!=i,sigma(i)} F_ij,
    sigma=(01)(23).

At least one inequality is strict. Conversely, suppose F has exactly these
properties. Apply the bipartite matrix lemma directly, with diagonal surplus
k_i=F_i,sigma(i)-sum_other F_ij>=0. It gives det(F)>0 whenever some k_i>0.
Since F preserves the affine hyperplane sum(lambda)=1, the invertible map
beta=F lambda identifies {lambda:F lambda>=0,sum(lambda)=1} with the ordinary
standard simplex. Thus this body is bounded and full-dimensional, and its
four contact-coordinate vertices are the columns of F^{-1}.

Normalize the rows of F by their positive row sums r_i to recover A. Then
A^T r=F^T ones=ones; therefore this is exactly the original positive vector
of inverse column sums. The two charts are inverse to each other. In
particular, the column chart does not infer boundedness from invertibility
of an arbitrary row-normalized matrix.

Parameterize each column j by its two first off-diagonal choices, with the
third entry equal to one minus their sum. There are eight real parameters,
all off-diagonal positivity constraints are linear, and pair row dominance
is linear. Individual designated column entries need not be >=1/2.
Writing D=sum_i F_i,sigma(i), simultaneous column normalization gives
sum_i k_i=2D-4. Thus some k_i>0 is equivalent to D>2.

## Direct cubic width comparisons

Let delta=det(F)>0 and S=adj(F). Both have degree at most three in the eight
column parameters. For each contact coordinate i and body-vertex pair j,k,
the polynomial S_ij-S_ik has degree at most two.

For a conceptual degree proof, split the ambient four-dimensional vector
space into the zero-sum subspace and one affine reference vector. In this
basis column-stochasticity gives a block matrix with a constant last row
(0,0,0,1). Its restriction G to the zero-sum subspace is a three-by-three
affine matrix. The inverse image of e_j-e_k lies in that subspace, where
it is adj(G)(e_j-e_k)/det(G). Multiplying by det(F)=det(G) proves the quadratic
numerator statement. This also follows by direct formal expansion.

For d_i=u dot p_i, set N_jk(u)=sum_i d_i(S_ij-S_ik). Then

    u dot (V_j-V_k)=N_jk(u)/delta.

For all 37 retained width directions, impose

    OR_{j<k} (N_jk(u)>W*delta OR -N_jk(u)>W*delta).

These are cubic polynomial inequalities in only eight variables. The
contact-coordinate bounds are -62*delta<=S_ij<=63*delta. The two ambient
subset-sum bounds use S_1j+S_2j and S_1j+S_3j in the same way. They remain
cubic. Hollow lattice-point exclusions F_i lambda(z)<=0 remain linear
disjunctions. The same exact 176 tautologies can be removed from the
216-point partial box: row scaling preserves their sign classification.
The remaining 40 clauses still express only a necessary hollowness test.

In the implemented threshold-17/5 column model these coordinate bounds are
implied, rather than separately asserted. The determinant cut below gives
vol(K)<21 for every feasible F, even a nonhollow assignment. Since P is
contained in K, each vertex v satisfies

    (1+sum_i max(0,-lambda_i(v)))/3 = vol(conv(P,v)) <= vol(K)<21.

The visible-facet pyramids justify the equality. Thus total negative mass is
less than 62 and total positive mass less than 63; every coordinate subset
sum lies in (-62,63). This proves the advertised S/T bounds redundant at
this threshold. The argument must be recomputed if the determinant cut or
width threshold changes. See results/DET2_PAIR_COLUMN_REVIEW.md.

The centralizer symmetries act by simultaneous row and column permutations
of F and preserve column normalization. One may arrange F_01 to be the
largest designated entry and F_23>=F_32. This uses the designated entries
of F, not the differently normalized designated entries of A.

## Necessary determinant and difference-gauge cuts

The contact tetrahedron has volume 1/3. Since its affine vertex map has
determinant det(F^{-1}),

    vol(K)=1/(3*delta).

The established ACMS consequence for a hollow body of width >17/5 is
vol(K)<1061208/50653. Therefore a genuine target body satisfies the cubic cut

    delta > 50653/3183624.

Let ell(z)=(X/2-Y-Z, X/2, Y-X/2, Z-X/2) for a lattice vector z=(X,Y,Z).
These are linear difference coordinates, without the affine constant one.
The unique zero-sum coefficients expressing z in body-vertex coordinates
are theta=F ell(z). A simplex difference body consists exactly of zero-sum
coefficient vectors with sum(theta_i positive)<=1. Thus its gauge is

    gamma_(K-K)(z)=(1/2) sum_i |(F ell(z))_i|.

The previously established bound lambda1(K-K)>37/102 implies this strict
lower bound for every nonzero integer z. For the three coordinate vectors,
pair dominance fixes the relevant signs, giving the linear formulas

    gamma(e_X)=D/2-1,
    gamma(e_Y)=F_02+F_32-F_30,
    gamma(e_Z)=F_03+F_23-F_20.

Consequently the three necessary cuts are

    D>139/51,
    F_02+F_32-F_30>37/102,
    F_03+F_23-F_20>37/102.

They use the ACMS implication for genuinely hollow target bodies; they need
not preserve every nonhollow feasible point of a partial-box relaxation.
If a pinned control is tested at a different width threshold, these
target-specific cuts must be adjusted or disabled for that control.

More generally gamma(z)=max_{nonempty proper I} sum_{i in I}(F ell(z))_i.
Thus a fixed-vector gauge lower bound is a disjunction of fourteen affine
inequalities. It raises neither the polynomial degree nor the number of
real variables. No finite selection of such cuts is claimed sufficient
for hollowness or for the global difference minimum.

## Verification and remaining scope

`python3 -m experiments.pair_column_identities` checks the cubic determinant,
all quadratic adjugate column differences, the eighteen axis/pair width
numerators, and the symbolic gauge formulas. Its certificate records an
exact bounded example with delta=9/250, gamma(e_X)=2/5 and gamma(e_Z)=1/10:
testing only the X direction cannot replace all difference-minimum cuts.
The example even satisfies the stated volume bound; it is not asserted to
be hollow or to have large width.

All identities concern the fixed contact chart. The same complete width
directions, geometric domain bounds and carefully stated lattice-exclusion
scope remain required. A feasible solver assignment still needs exact
whole-body certification, and UNKNOWN supplies no elimination.
