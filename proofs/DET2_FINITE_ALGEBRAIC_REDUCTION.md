# An explicit finite algebraic problem for determinant-two contacts

This note gives necessary conditions for a hollow tetrahedron of width
greater than 17/5 with contact hull

    P=conv(p0,p1,p2,p3)=conv(0,(2,1,1),e2,e3).

It does not prove that these conditions are infeasible. A solver query on a
subset of the lattice exclusions is only a relaxation of the hollow-body
problem. In particular, solver timeouts are not class eliminations.

## Two blocker branches, including equality cases

For x=(X,Y,Z), the contact barycentric coordinates are

    lambda0=1+X/2-Y-Z, lambda1=X/2,
    lambda2=Y-X/2,     lambda3=Z-X/2.

The four supporting facet forms, normalized by their sum of values at the
contacts, form a matrix A with diagonal zero, positive off-diagonal entries,
and each row summing to one. The body is {x:A lambda(x)>=0}.

Put q_j=(sum_i p_i)/2-p_j. These are four lattice points with contact
barycentric coordinates 1/2 except for coordinate j, which is -1/2.
Consequently the i-th facet excludes q_j from its strict interior exactly
when A_ij>=1/2. Each column j must have such an entry. Each row can have at
most one: two entries at least 1/2 would leave no room for the third positive
off-diagonal entry. Thus the exclusions determine a derangement, with either
cycle type 2+2 or cycle type 4.

All contact permutations induce lattice automorphisms here. The barycentric
coordinates of a lattice point are either all integers or all half-integers;
this property is invariant under permutations and characterizes the ambient
lattice through the inverse formulas X=2lambda1, Y=lambda1+lambda2,
Z=lambda1+lambda3. Hence it suffices to use representatives (01)(23) and
(0123). Keep A_i,sigma(i)>=1/2 as a closed inequality. Replacing it by >1/2
omits the vertical-facet limits of the two-roof chart.

## A polynomial bounded-simplex representation

Introduce a real matrix T whose j-th column consists of the barycentric
coordinates of the j-th body vertex. Require

    sum_i T_ij=1,
    (A T)_ij=0 for i!=j,
    (A T)_jj>0.

These are polynomial conditions of degree at most two. They imply that A and
T are invertible because AT is a positive diagonal matrix. If d_j=(AT)_jj,
then T=A^{-1}diag(d), and the column-sum conditions give
sum_i(A^{-1})_ij=1/d_j>0. Therefore {lambda:A lambda>=0,sum lambda=1}
is exactly the bounded simplex with columns T. Conversely any bounded
tetrahedron with the specified relative-interior facet contacts has this
representation after labeling its vertices opposite the facets.

Its ambient vertices are V_j=(2T_1j,T_1j+T_2j,T_1j+T_3j).

## A rational uniform coordinate bound

The ACMS containment/volume inequalities, reconstructed in
[UPPER_BOUND_SLACK.md](UPPER_BOUND_SLACK.md), give for hollow K of width w

    lambda1(K-K) >= 1-(1+2/sqrt(3))/w,
    vol(K) <= lambda1(K-K)^(-3).

Since 1+2/sqrt(3)<13/6 (equivalently 48<49), w>17/5 gives

    lambda1(K-K)>37/102,
    vol(K)<(102/37)^3=1061208/50653<21.

The final rational gap is 21-1061208/50653=2505/50653>0.
For any point x in K, the visible-facet volume identity yields

    vol(conv(P,x))=(1/3)(1+sum_i max(0,-lambda_i(x))).

Hence sum_i max(0,-lambda_i(x))<62 and each lambda_i(x) lies in (-62,63).
The closed constraints -62<=T_ij<=63 are therefore safe necessary bounds.
Every sum of a subset of the lambda_i also lies in (-62,63). It follows that
all possible lattice points of K lie in the conservative integer box

    [-124,126] x [-62,63] x [-62,63].

For a candidate in the algebraic model, explicitly impose the additional
linear constraints -62<=T_1j+T_2j<=63 and -62<=T_1j+T_3j<=63 for every j.
Individual barycentric bounds alone do not imply these subset-sum bounds.
With them, every candidate simplex lies in the stated ambient box, whether
or not it ultimately passes the hollowness conditions.

This box contains 3,984,876 points. It is a proved finite domain, not a
recommended brute-force workload.

## Exactly 37 width tests for the target threshold

For primitive integer u, retain it modulo sign precisely when w(P,u)<=3.
Since p0=0, such a direction satisfies |u_y|,|u_z|<=3 and
|2u_x+u_y+u_z|<=3, hence |u_x|<=4. Exhausting that small box and filtering
by primitive content and sign gives 37 directions.

For any K containing P, even without a hollowness hypothesis,

    w(K)>17/5
    iff w(K,u)>17/5 for every one of these 37 directions.

Indeed all omitted primitive directions have integer contact width at least
four, so cannot violate the target. This threshold equivalence does not
need an assumed global upper bound below four. Each retained inequality is
the finite disjunction over ordered distinct body-vertex pairs

    OR_{j!=k} u dot (V_j-V_k)>17/5.

## Exact finite hollow conditions and solver scope

For each integer z in the proved enclosing box, hollowness is equivalent to

    OR_i (A_i dot lambda(z)<=0).

Using every point gives a finite real-polynomial feasibility problem for a
potential high-width hollow tetrahedron in either blocker branch. The volume
bound is used only to prove that all genuine counterexamples occur inside
the chosen domain; it is not imposed as an unjustified sampled coordinate
cutoff.

The exploratory SMT query uses only z in [-2,3]^3, while retaining the
polynomial simplex, width and barycentric bounds. This is a necessary
relaxation. SAT supplies at most a candidate for additional exact lattice
cuts; it does not certify hollowness. UNSAT would need independent review
of the encoding and solver evidence before becoming a class-bound claim.
An unknown result leaves the branch open.

## Eliminating the auxiliary vertex variables

There is an equivalent chart with only eight independent facet parameters.
Let epsilon be the sign of the blocker permutation: +1 for the pair branch
and -1 for the four-cycle branch. For a nonsingular admissible A,

    epsilon det(A)>0.

To see this, permute columns so that the designated entries become diagonal,
obtaining a row-stochastic matrix B with B_ii>=1/2. For 0<=t<1 the matrix
(1-t)I+tB has positive diagonal and is strictly diagonally dominant, hence
nonsingular. Its determinant starts at one and stays positive. At t=1 its
determinant is nonnegative, and is positive if B is nonsingular. Undoing the
column permutation proves the sign assertion, including boundary entries
equal to 1/2.

Define S=epsilon adj(A) and C_j=sum_i S_ij. Boundedness is equivalent to

    epsilon det(A)>0 and C_j>0 for every j.

Indeed the column sums of A^{-1} are C_j/(epsilon det(A)). Under these
conditions the body vertices have contact coordinates T_ij=S_ij/C_j.
Consequently all T and V variables can be eliminated. For example the
barycentric bounds become -62 C_j<=S_ij<=63 C_j. The extra ambient bounds
use S_1j+S_2j and S_1j+S_3j in the same way.

Write N_j=(2S_1j,S_1j+S_2j,S_1j+S_3j). The width disjunction becomes

    OR_{j!=k} 5 u dot (N_j C_k-N_k C_j)>17 C_j C_k.

All denominators multiplied here are strictly positive. Each row of A has
one designated entry a_i>=1/2, a second entry b_i>0, and a final entry
1-a_i-b_i>0. Thus A is affine in eight real variables. Cofactors have degree
at most three, and the displayed width inequalities degree at most six.
The determinant sign condition has degree at most four; lattice exclusions
remain linear disjunctions. This equivalent formulation is a concrete next
probe after the auxiliary-variable model times out, not a proved bound.

The exact domain constants, 37 directions and all 24 contact-permutation
maps are reproduced by `python -m experiments.det2_finite_domain` in
[det2_finite_domain.json](../certificates/det2_finite_domain.json).

## Subsequent implementation checkpoint

The eight-variable formulation and a version using pair-specific matrix
structure have now been implemented. Both pinned controls passed in each
script, but each unpinned target query timed out. The pair matrix structure
and exact boundary normalization are in PAIR_MATRIX_STRUCTURE.md. The next
representation, derived in PAIR_CUBIC_FORMULATION.md, has thirteen variables
and polynomial degree at most three. No branch elimination follows from
any of the recorded timeouts.
