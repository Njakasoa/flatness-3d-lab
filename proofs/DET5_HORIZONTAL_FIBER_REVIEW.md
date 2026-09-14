# Independent review: two linear fiber variables over six shape parameters

Status: proved algebraic and optimization reduction. This is not a finite
cover of the six shape parameters, a hollow-body classification, or a new
numerical flatness bound. No solver queries were run for this review.

Fix rational shape parameters

    sigma=(x,y,c,e,r,u),        0<=x<y<=1,

in the [ordered height chart](DET5_RATIONAL_HEIGHT_CHART_REVIEW.md).
Only `t,h` vary. Put `d=y-x`, `a=x+dt`, `b=h-a`, and

    D=u*((1-x)c+x e)-r*((1-y)c+y e).

We require `D!=0` and `b>0`. The latter is a linear restriction in the two
fiber variables. The earlier determinant identity reads `det F=bD`.
All shape-domain conditions remain necessary; fixing a shape does not
silently discard positivity, the strict bounds on `t`, or certified-domain
complements.

## Why every vertex-pair numerator is affine in the fiber variables

This fact has a short rank proof independent of expanding eighteen large
polynomials. Write the chart matrix as

    F(t,h)=F(0,0)+t p alpha^T+h q beta^T,
    p=(0,-1,1,0)^T,      q=(-1,0,0,1)^T,
    alpha=(1,0,0,1)^T,  beta=(0,1,1,0)^T.

The formulas follow entry by entry from the displayed chart matrix.
Column stochasticity makes the three-dimensional subspace

    U={z in R^4: sum(z_i)=0}

a common invariant subspace of these matrices. Since `alpha+beta=1`, the
restriction to `U` has the form

    F|U = F(0,0)|U + (t p-h q) alpha^T|U.                 (1)

Thus the joint variation in both fiber variables is a **single rank-one
update**, with an affine update vector and a fixed covector.

For complete coordinates, let

    B=[e1-e0, e2-e0, e3-e0],       F B=B G.

Here `G` is a three-by-three matrix. In this basis the varying part of `G`
is the outer product

    (-t,t,-h)^T (-1,-1,0).

Every minor of a matrix `G0+w(t,h)v^T`, with `v` fixed and `w` affine, is
affine jointly in `t,h`: expand the minor multilinearly in its columns.
Every term selecting two or more updated columns vanishes because those
columns are scalar multiples of the same restricted vector `w`. The
remaining terms use at most one updated column and are affine. In
particular, all entries of `adj(G)` and `det(G)` are affine.

The action induced by `F` on the one-dimensional quotient `R^4/U` is the
identity, because columns sum to one. Consequently `det(G)=det(F)`.
For the physical contact matrix

    P=[p0,p1,p2,p3],

and any vertex-index pair `i,j`, write `ei-ej=B z_ij`. Then

    P adj(F)(ei-ej) = P B adj(G) z_ij.                  (2)

For nonsingular `F`, this follows from `F^{-1}B=B G^{-1}` and the equality
of determinants. It also extends as a polynomial identity, although only
the nonsingular case is needed here. The right side of (2) is jointly
affine in `t,h`. This proves the claimed affineness of all eighteen
coordinate-pair numerators, and hence of every directional pair numerator.
Individual vertex numerators need not have this degree property; taking
the difference is essential.

For the reverse height order, conjugate `F` by the permutation interchanging
indices 1 and 2. The subspace `U` is preserved; `p` changes sign while
`q,alpha,beta` are unchanged. The same rank-one restriction and proof apply.
The physical contact matrix `P` stays in the original contact ordering.

## Projective coordinates give an exact rational linear formulation

Introduce

    T=t/b,       H=h/b,       R=1/b.

The exact transformed relation and domain condition are

    H-xR-dT=1,       R>0.                                (3)

Conversely, (3) gives `t=T/R`, `h=H/R`, and
`h-x-dt=1/R>0`. Thus this transformation is bijective on the relevant
fiber domain. It has three variables and one independent affine equation,
so the fiber still has two degrees of freedom.

For any affine expression `L(t,h)=L0+Lt*t+Lh*h`, define

    Lhat(T,H,R)=L0*R+Lt*T+Lh*H=L/b.

The coefficients are rational for fixed rational `sigma`. In particular,
`F/b` is entrywise affine. Positivity of off-diagonal entries is equivalent
to positivity of their transformed entries. The restrictions `0<t<1`
become `0<T<R`; every other affine fiber-domain inequality transforms in
exactly the same way.

If a contact guard has barycentric contact vector `ell`, its condition

    at least one coordinate of F ell is <=0

is equivalent to the same disjunction for `(F/b)ell`. A fixed gauge lower
bound `gamma(F ell)>beta` becomes

    gamma((F/b)ell)>beta R.

Using the finite signed-subset expression for the sum-zero gauge gives a
finite disjunction of rational linear inequalities. This includes any
fixed collection of ten or eleven necessary gauge directions. It does
not establish that a selected collection equals the full first minimum.

Let `N_ij(t,h)` be a directional pair numerator in (2). The actual
corresponding vertex difference is

    N_ij/(bD) = Nhat_ij(T,H,R)/D.                        (4)

Since `D` is fixed and nonzero, the condition that a specified directional
width exceed a rational target is a finite disjunction of rational linear
inequalities. For example, width greater than `17/5` is exactly

    OR over i<j:  5*Nhat_ij>17*abs(D)
                  OR -5*Nhat_ij>17*abs(D).

This transformation involves no relaxed products. It is exact on each
fixed rational shape fiber. The complete fifteen-direction width target
can therefore be combined with the strict chart domain, finite guards,
selected gauge bounds, and the applicable inherited exclusions as a
Boolean combination of rational linear inequalities.

The fifteen-direction claim still needs its independent completeness
argument: the remaining integer directions have contact-hull width at
least four. This review does not infer completeness merely from the
number of inequalities. Likewise, the twenty observer guards are used
with their previously established scope; finite observer constraints
alone must not be renamed full hollowness without that justification.

## What finite linear optimization on one fiber proves

Introduce an objective variable `w` with `0<=w<=4`. For each of the
fifteen directions, impose that one signed pair difference in (4) be at
least `w`. The resulting feasible set is a finite union of rational
polyhedra with some strict faces, because `D` is a constant on this fiber.
The upper cap makes the objective bounded. By the complete-direction
argument, this objective computes the supremum of the actual lattice
width clipped at four on the geometries admitted by the other constraints.
If hollowness has only necessary constraints in the formulation, it is
instead an upper optimization over that outer admissible set.

Strict boundaries require an explicit qualification. First discard a
branch if its original strict system is empty. For a nonempty branch,
choose one point satisfying every strict inequality. Convex combinations
of that point with any point of the fully non-strict relaxation approach
the latter while respecting all original strict inequalities. Therefore
that relaxation is exactly the closure of the nonempty branch. Linear
optimization over the closure gives the correct supremum, but does not
necessarily give an attained maximum in the original branch. Closing
an empty strict branch first would be unsound.

A nonempty rational polyhedron with a bounded linear objective has a
rational optimal value. There are only finitely many disjunctive branches.
Consequently a nonempty fixed rational fiber has a rational clipped
supremum, even when no feasible point attains it. This is an existence and
reduction statement, not a claim that the branch enumeration is small.

Finally, **no finite collection of sampled rational shapes covers the
six-dimensional continuous shape domain**. Both the matrix coefficients
and `D` depend nonlinearly on those shape parameters. Their domain need
not be compact in these coordinates, and approaching `D=0` requires care.
Proving a uniform width bound still needs a rigorous argument over every
admissible shape, including limit regimes; rational optima on individual
fibers do not supply it.
