# Positive horizontal determinant is incompatible with the target gauges

Status: analytic elimination of one entire determinant-sign branch in each
ordered Y[0,3] chart. The remaining negative branch is not excluded. No
solver query or continuous shape enumeration is used.

Use the exact [compact shape chart](DET5_COMPACT_SHAPE_CHART_REVIEW.md), with
canonical heights `0<=x<y<=1` and

    p=x/y, q=(1-y)/(1-x),
    A=C+pE, B=qC+E, S=C+E<1,
    alpha=(1-p)E, omega=(1-q)C,
    D=uA-rB.

Here `C,E,r,u>0`, so `A,B>0`; `alpha,omega>0` as well. Write the canonical
horizontal images as

    V=F(e1-e2)=((1-x)u-(1-y)r, -u, r, xu-yr),
    Z=F(e3-e0)=(alpha,-B,A,-omega).

Both vectors sum to zero, and their gauge is
`Gamma(v)=sum_i max(v_i,0)=||v||_1/2`. In particular,
`Gamma(Z)=alpha+A=S`. The physical lattice vector `(2,0,1)` has gauge

    Gamma((2V+Z)/5)  for original order q1<q2,
    Gamma((Z-2V)/5)  for original order q1>q2.

The change of sign in the reverse order is essential. The physical contact
points keep their original indexing while the canonical chart swaps 1 and 2.

## A triangular domain for the two remaining shape variables

The already proved elimination of the exceptional row-3 observer alternative
uses strict chart positivity and `b>0`; it gives

    ku<=B, with k=3 for q1<q2 and k=2 for q1>q2.

Suppose additionally `D>=0`. Then `0<=r<=uA/B` and `0<=u<=B/k`. Thus `(u,r)`
belongs to the closed triangle with vertices

    O=(0,0), U=(B/k,0), W=(B/k,A/k).

This is an outer triangle: its boundary may contain shapes that do not
satisfy the original strict contact domain. Bounding its gauges remains
valid for all actual admissible shapes it contains. Explicit barycentric
weights at `O,U,W`, respectively, are

    1-ku/B,  k*(u/B-r/A),  kr/A.

They are nonnegative, sum to one, and reconstruct `(u,r)` exactly.
For fixed `x,y,C,E`, each physical image is affine in `(u,r)` and Gamma is
convex, so its maximum over this triangle is bounded by its largest vertex
value. No sign-pattern enumeration or limit compactification is needed.

The exact identities

    (1-x)B-(1-y)A=alpha,  xB-yA=-omega

show that `V=Z/k` at W.

## Forward order: gauge at most S/3

At O, `Gamma((2V+Z)/5)=S/5`. At W with `k=3`, it equals `S/3`.
At U, `V=((1-x)B/3,-B/3,0,xB/3)` and `Gamma(V)=B/3`.
The triangle inequality for Gamma gives

    Gamma((2V+Z)/5) <= (2B/3+S)/5 <= S/3,

because `B=qC+E<=S`. Convexity consequently proves, on the entire `D>=0`
outer triangle,

    gamma_K-K(2,0,1) <= S/3 < 1/3.                 (1)

## Reverse order: gauge at most S/5

At O, the gauge is `S/5`. At W with `k=2`, `Z-2V=0`, so it is zero.
At U the unscaled physical image is

    Z-2V=(alpha-(1-x)B, 0, A, -omega-xB).

The last coordinate is negative and the third is positive; hence

    Gamma(Z-2V)=A+max(alpha-(1-x)B,0)
               <= A+alpha=S.

Convexity gives throughout the triangle

    gamma_K-K(2,0,1) <= S/5 < 1/5.                 (2)

In particular, **both orders require `D<0` under the necessary gauge
threshold `183/500`**. This eliminates the whole positive determinant-sign
branch, not merely small height gaps. The argument uses one observer
necessity and one physical gauge. The other horizontal gauges are not
needed for this elimination.

## Consequences and scope

The exact determinant identity is `det(F)=bD`, with `b>0`, in both canonical
orders (simultaneous row/column permutation preserves determinant). Therefore
putative actual bodies with global width greater than `17/5` require
`det(F)<0`. The negative branch remains open; this does not eliminate the
whole determinant-five class.

There is also a target-free width consequence. For an actual hollow body,
ACMS gives `lambda1(K-K)>=1-A0/w(K)`, where `A0=1+2/sqrt(3)`; see the
[existing deduction](DET5_VOLUME_GAP_BOUNDS.md). Since the first minimum is
at most the selected physical lattice gauge, (1) and (2) imply, when `D>=0`,

    w(K) < (3/2)*A0  for q1<q2,
    w(K) < (5/4)*A0  for q1>q2.

The strict inequalities follow from `S<1`. No large-width premise, volume
bound or exhaustive finite gauge list is used for these conditional width
bounds. For actual invertible bodies `D=0` is already impossible; its
inclusion in the outer triangle only strengthens the domain covered by the
gauge argument.

The [exact replay](../tests/replay_det5_positive_horizontal_determinant.py)
checks the coordinate and barycentric identities symbolically and tests
rational boundary/interior fixtures in both orders. These fixtures are
checks of the formulas, not a numerical proof of universal coverage. The
convexity and triangle argument above supplies that universal proof.
