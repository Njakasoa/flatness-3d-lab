# CLAIM-0011 — a necessary determinant sign at large width

Date: 2026-09-14. Status: analytic restricted result, supported by independent
internal review and exact symbolic replay. Mathematical priority is unconfirmed.
This excludes one sign branch of a continuous contact chart; it does not
exclude the whole contact class or improve the global flatness bound.

## Statement

Let K=conv(v0,v1,v2,v3) be a compact full-dimensional hollow real tetrahedron
in the standard lattice. Require each ordered point

    p0=0, p1=(5,1,2), p2=(0,1,0), p3=(0,0,1)

to lie in the relative interior of the facet opposite the corresponding v_i.
Define the contact matrix by p_j=sum_i F_ij v_i and sum_i F_ij=1.
It has zero diagonal and strictly positive off-diagonal entries.
Normalize actual heights in Y=(0,1,0) to

    q_i=(Y(v_i)-min_j Y(v_j))/width(K,Y).

Assume q0=0 and q3=1; tied extrema are allowed. The existing ordering lemma
implies q1!=q2. Put A0=1+2/sqrt(3). If det(F)>0, then in **both** height
orders,

    w(K)<(5/4)A0=(5/4)(1+2/sqrt(3)).

Consequently, every such body with w(K)>=(5/4)A0, and in particular
with w(K)>17/5 or w(K)>=2+sqrt(2), must have **det(F)<0**.
At the same threshold it also necessarily satisfies

    F03 >= 3*F01 + 2*F02.

This is the nonpositive barycentric coordinate of the integer observer
(3,1,1) relative to the original facet0: that point must lie on its supporting
plane or on its exterior side. It need not lie in the facet itself.

The determinant and displayed entries refer to the stated original
contact/vertex correspondence. Simultaneously relabeling both preserves the
determinant sign. The result is restricted to the specified Y-extrema chart;
no sign or forced-facet statement for other charts is inferred.

## Proof

Use the [exact compact chart](../proofs/DET5_COMPACT_SHAPE_CHART_REVIEW.md),
with x=min(q1,q2), y=max(q1,q2), and canonical low/high labeling. Set

    p=x/y, q=(1-y)/(1-x), A=C+pE, B=qC+E, S=C+E<1,
    D=uA-rB, b=1/width(K,Y)>0.

The chart identities give det(F)=bD in both orders. Let
V=F(e1-e2), Z=F(e3-e0) in the canonical chart, and
Gamma(z)=||z||_1/2 on the sum-zero coordinate space. Then Gamma(Z)=S.

Hollowness excludes the integer observer (2,1,1) from the interior.
Strict contact positivity rules out its exceptional row-3 alternative.
Thus ku<=B, with k=3 in forward order and k=2 in reverse. If additionally
kr<=A, the pair (u,r) lies in the closed rectangle

    [0,B/k] x [0,A/k].

At its four corners, the gauges of kV-Z are respectively S,A,B,0.
Each is at most S. Convexity of Gamma therefore gives Gamma(kV-Z)<=S<1
on the entire rectangle. The physical vector is (3,0,1) in forward order
and (2,0,1) in reverse, with a harmless overall sign in the reverse case.
Its actual lattice gauge is consequently at most S/5<1/5.
The [rectangle supplement](../proofs/DET5_FORCED_OBSERVER_BRANCH.md) gives
the exact corner images and checks the two physical orders.

Apply ACMS Lemma 5.1,

    1-A0/w(K)<=lambda1(K-K)<=gamma_(K-K)(selected vector)<1/5.

Whenever kr<=A this proves w(K)<(5/4)A0, with no large-width or volume
premise. Conversely, at w(K)>=(5/4)A0 we must have kr>A. The other
necessary observer (3,1,1) now forces its remaining row-0 alternative.
In the original physical indexing that is F03>=3F01+2F02 in either order.
Finally uA<=AB/k<rB, so D<0 and det(F)<0.

If det(F)>0, then D>0 forces r<uA/B<=A/k, giving the same strict width
bound. An actual contact matrix is invertible since both labeled tetrahedra
are full-dimensional. Its determinant cannot vanish. The threshold equality
is therefore included in the necessary negative-sign conclusion.

The earlier [triangle proof](../proofs/DET5_POSITIVE_HORIZONTAL_DETERMINANT.md)
remains valid; its forward estimate is weaker because it selects a different
physical vector. The rectangle argument gives the strengthened common bound
and the forced observer clause. Boundary points of these outer parameter
polygons need not themselves be valid strict-contact bodies; convexity still
bounds all actual shapes they contain.

## Evidence and limits

```sh
.venv/bin/python tests/replay_det5_positive_horizontal_determinant.py
.venv/bin/python tests/replay_det5_forced_observer_branch.py
```

The original replay checks 20 exact identities and 450 rational triangle
fixtures. The stronger rectangle replay checks 24 identities and 750 fixtures.
These support the algebra; the written convexity argument proves the universal
result. Both arguments received independent internal review. See the
[rectangle review](../proofs/DET5_FORCED_OBSERVER_INDEPENDENT_REVIEW.md).

The established gauge-to-width implication comes from
[Averkov–Codenotti–Macchia–Santos](https://arxiv.org/abs/1907.06199).
The explicit sign obstruction is a result of this laboratory; priority and
sharpness are not established. The negative determinant branch and the other
height charts remain open. The list of 58 necessary contact types is unchanged.
