# A convex rectangle forces the exceptional observer branch

Status: universal gauge obstruction to the main second-observer branch.
This strengthens the [earlier determinant-sign bound](DET5_POSITIVE_HORIZONTAL_DETERMINANT.md)
without changing that archived proof. The exceptional branch remains open.
No solver query or finite continuous coverage assertion is used.

Use the [compact chart](DET5_COMPACT_SHAPE_CHART_REVIEW.md), in canonical
height order `0<=x<y<=1`. Put

    A=C+pE, B=qC+E, S=C+E<1,
    alpha=(1-p)E, omega=(1-q)C,
    V=((1-x)u-(1-y)r,-u,r,xu-yr),
    Z=(alpha,-B,A,-omega), D=uA-rB.

Here `A,B>0`, `A,B<=S`, and all vectors displayed are in the sum-zero
subspace. For such vectors write `Gamma(v)=||v||_1/2`, the sum of their
positive coordinates. The scalar Gamma is a norm on this subspace and is
convex. The exact identities are

    (1-x)B-(1-y)A=alpha,  xB-yA=-omega,
    alpha+A=B+omega=S.

Let `k=3` in the original forward order `q1<q2`, and `k=2` in the original
reverse order `q1>q2`. The first observer's exceptional row-3 alternative
has already been excluded using strict chart positivity and `b>0`; hence
`ku<=B`. The second observer still gives the disjunction

    forward: 3r<=A OR F03>=3F01+2F02,
    reverse: 2r<=A OR F03>=2F01+3F02.                (1)

The F entries in (1) are canonical chart entries. The reverse coefficients
come from keeping the original physical observer points while conjugating
the contact matrix by the swap of indices 1 and 2.

## Universal rectangle obstruction, independent of determinant sign

Temporarily assume the main alternative `kr<=A`. Then `(u,r)` lies in the
closed rectangle

    0<=u<=B/k,   0<=r<=A/k.

Fix `x,y,C,E` and consider the affine sum-zero image `G=kV-Z`. At the four
corners its exact values and gauges are:

| Corner `(u,r)` | `G=kV-Z` | `Gamma(G)` |
| --- | --- | --- |
| `(0,0)` | `-Z` | `S` |
| `(B/k,0)` | `((1-y)A,0,-A,yA)` | `A` |
| `(0,A/k)` | `(-(1-x)B,B,0,-xB)` | `B` |
| `(B/k,A/k)` | `0` | `0` |

The identities above prove every entry of this table. All gauge evaluations
remain valid when `x=0` or `y=1`, including vanishing corner coordinates.
Every point of the rectangle is a convex combination of its four corners;
thus convexity and `A,B<=S` give

    Gamma(kV-Z)<=S<1.                              (2)

The actual strict contact domain may occupy only part of this outer
rectangle. Its inclusion in the rectangle suffices; the corner matrices
need not themselves represent actual bodies.

In the original forward order the physical lattice vector `(3,0,1)` has
image `(3V-Z)/5`. In the original reverse order `(2,0,1)` has image
`(Z-2V)/5`. These are `G/5` and `-G/5`, respectively. Evenness of Gamma
and (2) therefore imply

    forward main branch: gamma_K-K(3,0,1)<=S/5<1/5,
    reverse main branch: gamma_K-K(2,0,1)<=S/5<1/5.  (3)

No assumption on D was used in this rectangle argument.

## Forced observer clauses and determinant sign

Whenever the corresponding selected physical gauge is at least `1/5`,
(3) rules out the main alternative. Hence **`kr>A`**, and the original
necessary observer disjunction (1) forces its exceptional clause:

    forward: 3r>A AND F03>=3F01+2F02,
    reverse: 2r>A AND F03>=2F01+3F02.                (4)

The `>=` in each exceptional observer clause must be retained: boundary
lattice points may make the guard an equality. The strict `kr>A` follows
because the ruled-out rectangle includes its boundary `kr=A`.
Together with `ku<=B`, (4) immediately gives

    D=uA-rB <= AB/k-rB <0.                         (5)

Thus the determinant sign follows from the stronger observer-branch result,
without invoking the earlier triangular proof. In particular the target
minimum threshold `183/500` implies all of (4)--(5).

## Target-free width consequence

For an actual hollow strict-contact body in this chart, the first observer
is necessary and its reduction applies independently of any assumed large
width. ACMS gives

    lambda1(K-K)>=1-A0/w(K),  A0=1+2/sqrt(3).

If the main second-observer branch `kr<=A` holds, then the first lattice
minimum is at most the selected gauge in (3), and hence

    w(K) < (5/4)*A0                                (6)

in **both** original height orders. The strict inequality follows from
`S<1`, not from a numerical approximation.

Consequently every actual body in the chart with
`w(K)>=(5/4)*A0` requires the exceptional clauses (4) and `D<0`.
This includes equality at the displayed width threshold: ACMS then gives
`lambda1>=1/5`, already incompatible with (3). Also, `D>=0` and `ku<=B`
would imply `r<=uA/B<=A/k`; therefore every actual `D>=0` body satisfies
the same strict bound (6). This improves the previous forward-order
conditional width bound by choosing `(3,0,1)` as the obstructing vector.
It does not bound bodies in the remaining exceptional negative branch.

Run `.venv/bin/python tests/replay_det5_forced_observer_branch.py`.
The [replay receipt](../results/det5_forced_observer_branch_validation.json)
checks symbolic corner and physical-vector identities and rational convex
combination fixtures. Those fixtures check formulas; the universal proof
is the convex rectangle argument above.
