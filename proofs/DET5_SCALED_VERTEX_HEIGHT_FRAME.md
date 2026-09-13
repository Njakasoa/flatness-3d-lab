# A scaled vertex frame with linear complete-width tests

Status: exact formulation and independent mathematical review. This changes
the algebra used by the search; it establishes no new exclusion or flatness
bound. No old solver query is repeated by this note.

Let P have ordered vertices p0=0, p1=(5,1,2), p2=e2, p3=e3. Write
H=(0,1,1,0), W=17/5, beta=183/500 and R=6/(5 beta^3). Use a nonnegative
column-stochastic contact matrix F with zero diagonal and strictly positive
off-diagonal entries. Such matrices have eight free scalar parameters.

## Normalized scaled differences

Select distinct indices L,H0 for a minimum and maximum Y-height of the
unknown tetrahedron K. Set

    b=1/width(K,Y),
    T_i=b(v_i-v_L),
    T_L=0,    T_i,Y=q_i,    q_L=0,    q_H0=1,
    0<=q_i<=1,    0<b<1/W.

There are six unknown horizontal scaled coordinates T_i,X,T_i,Z for i!=L,
two free normalized heights q_i, and b. Together with F this is a model in
seventeen real variables. The Y offset and all three physical translations
have been eliminated.

The complete contact reconstruction uses the nine equations

    sum_i (F_ij-F_i0) T_i = b(p_j-p0),    j=1,2,3.       (1)

Every scalar equation has degree at most two. If q is fixed, the three
Y-coordinate equations are linear. The other six contain only products of
shared F entries with the scaled X/Z coordinates.

## Reconstruction forces invertibility

Let I be the three indices different from L. Let N have columns T_i for
these indices, G have entries G_ij=F_ij-F_i0 for i in I and j=1,2,3, and
B=[p1-p0,p2-p0,p3-p0]. Equation (1) is

    N G = b B.

The right side is invertible because b>0 and |det B|=5. Consequently N and
G are invertible. Column stochasticity, subtracting column zero from the
other columns, and replacing the omitted row by the row sum give
|det F|=|det G|. Thus F is invertible as well. This is an exact algebraic
argument: separate determinant inequalities or gauge-based rank conditions
are not needed to force invertibility in this complete lifted model.

Put C=sum_i F_i0 T_i and define actual vertices

    v_L=-C/b,    v_i=(T_i-C)/b.

Their weighted column-zero contact is zero. Equation (1) then shows
sum_i F_ij v_i=p_j for every contact column. Since N is invertible, the
vertices are affinely independent. F is therefore exactly their barycentric
contact matrix, and its positivity and diagonal conditions put each p_j in
the relative interior of its corresponding facet. Their Y-width is exactly
1/b, with the selected actual extrema L,H0.

Conversely, every actual tetrahedron with these contact and extrema
conditions yields these variables and satisfies (1). The construction is
therefore an equivalence, not just a necessary relaxation.

## All fifteen width tests become linear

For every primitive covector u in the independently established
[complete fifteen-direction list](DET5_COMPLETE_GEOMETRY_REVIEW.md), impose

    OR over i<j and signs epsilon in {-1,+1}:
        epsilon * u dot (T_i-T_j) > W b.                 (2)

These tests are linear in the scaled coordinates and b. Multiplication by
positive b proves their equivalence to the actual directional-width tests.
All other primitive covectors have contact width at least four on P and
hence already exceed W on K. Thus (2) for the fifteen listed directions is
equivalent to global lattice width greater than W. The Y test is redundant
with 0<b<1/W but can be retained for uniformity.

The complete list must be imposed on each body. Selecting only one direction
per symmetry orbit would not be equivalent. The existing three Y-extrema
representatives remain sufficient because an affine lattice contact
symmetry transforms the body and the entire width list together.

## Linear bounds from the actual volume necessity

For a global target body, the established ACMS/Minkowski volume necessity
is vol(K)<beta^(-3). The
[containing-tetrahedron width/volume lemma](SIMPLEX_WIDTH_VOLUME_MONOTONICITY.md)
gives w(K,u)<R w(P,u). In particular all pairs satisfy the necessary linear
bounds

    |T_i,X-T_j,X| < 5 R b,
    |T_i,Z-T_j,Z| < 2 R b.                               (3)

Because T_L=0, these include |T_i,X|<5 R b and |T_i,Z|<2 R b. The pairwise
bounds are stronger than just retaining those individual inequalities.
The normalized Y-span is one, so the corresponding Y bound gives

    b>1/R=2042829/50000000.

Using b<1/W also gives constant initial product bounds
|T_i,X|<5R/W and |T_i,Z|<2R/W. These are suitable finite domains for
McCormick envelopes; keeping (3) preserves the stronger dependence on b.
Neither these linear bounds nor the individual-vertex cuts below are
asserted to be equivalent to the full volume inequality.

One can also retain the existing containing-simplex volume cuts. Let
D_i=T_i-C=b v_i, and define the scaled contact barycentric coordinates

    B_i=(b+2D_i,X/5-D_i,Y-D_i,Z,
         D_i,X/5,
         D_i,Y-D_i,X/5,
         D_i,Z-2D_i,X/5).

Their sum is b. For every nonempty coordinate subset S impose

    sum_{j in S} B_i,j < R b.                            (4)

Indeed, vol(conv(P,v_i))/vol(P)=sum_j max(lambda_P(v_i)_j,0), so the actual
volume necessity implies (4). Once the shared products F_i0 T_i have been
lifted, C and (4) are linear expressions in the lifted variables. Products
already used in (1) can be reused; no separate independently relaxed copy
should be introduced for this same algebraic quantity.

## Fixing q gives a twelve-variable quadratic model

At a fixed rational normalized height vector q, introduce an offset a so
that F^T q=a*1+b*H. In any column j, choose its allowed off-diagonal indices
r,s,t with q_r!=q_s, and set F_tj=theta_j. Then

    F_rj=(a+bH_j-q_s-(q_t-q_s)theta_j)/(q_r-q_s),
    F_sj=1-theta_j-F_rj.

Thus F is affine in six variables: theta_0,...,theta_3,a,b. Positivity is
linear, as are a>=0 and a+b<=1. All Y reconstruction equations already hold.
Adding the six horizontal scaled differences leaves twelve variables and
six quadratic reconstruction equations, with every width test still linear.
No variable denominator is introduced because q is fixed rational data.

If a column's three allowed q-values are identical, do not divide by zero.
Its height equation instead imposes a linear consistency condition. In the
present strict facet-contact setting such a fixed q is infeasible: it has
one exceptional vertex at zero or one. The contact column opposite that
vertex averages the common height, while the other contact column with the
same contact Y-value has a strictly positive contribution from the
exceptional vertex. The two equal contact heights would then have different
normalized averages. There are two contacts of each Y-value, so this applies
regardless of the exceptional index. Checking this linear degeneracy is
therefore a valid special case before using the displayed parametrization.

A fixed q slice does not cover a nontrivial q-box. Conversely, a McCormick
relaxation of (1) on boxes is only an outer approximation; its SAT points do
not inherit the exact reconstruction or rank conclusions automatically.

## The four-gauge rank margin remains available

The independent [four-vector argument](DET5_VOLUME_GAP_BOUNDS.md) applies to
exact normalized Y charts. With r=F ell(1,0,0), s=F ell(2,0,1), the first
two intrinsic masses are 3/5. Gauges at those two vectors and at their sum
and difference exceed beta. For all real t the triangle-inequality argument
gives

    ||s-t r||_1 > 2 beta-3/5 = 33/250.

This proves horizontal injectivity and then invertibility from an exact
Y-height identity alone. It also gives the complementary minor bound
k_Y>6039/500000. These facts remain valid if q is fixed. They are useful
additional necessary inequalities or alternative rank certificates, although
(1) already forces invertibility without them.

The finite observer-guard theorem can be applied after exact reconstruction
when its contact-edge gauge hypotheses are imposed. Combined with all
fifteen widths, it yields the intended complete hollow-tetrahedron target.
The present degree reduction changes neither those hypotheses nor the
meaning of a partial solver result.
