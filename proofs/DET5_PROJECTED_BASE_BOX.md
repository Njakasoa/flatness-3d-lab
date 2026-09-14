# A continuous four-base-parameter box excluded by projection

Status: analytic exclusion for actual forward-order Y[0,3] determinant-five
class-5 strict facet-contact bodies with global lattice width greater than
`17/5`. No complete chart, reverse-order domain or further contact type is
excluded. No solver search is used.

The [archived closed box](../results/det5_projected_base_box.json), in compact
coordinates `(p,q,C,E)`, is

    [0,1/32] × [31/64,33/64] × [3/64,5/64] × [31/64,33/64].

All admissible remaining parameters are free. Define

    L=1-pq, A=C+pE, B=qC+E, S=C+E, Delta=B-A,
    f=1-q+L*E/2+2Delta, T=183/100.

The [four-base reduction](DET5_FOUR_BASE_SHAPE_CUTS.md) proves that a forward
candidate must satisfy `H1>T OR H2>T`, where

    H1=(2-a/3)B, H2=tau+(2-a/3)Delta.

It removes the third first-gauge piece using the second gauge and the forced
observer; the other forward horizontal gauge is then redundant. That
reduction's hypotheses, including the projected strict observer Q>0, remain
essential here.

The [exact one-gauge projection](DET5_FORWARD_MIDDLE_GAUGE_EXACT_PROJECTION.md)
proves `H2>T` requires `f>T`. The [independent box review](DET5_PROJECTED_BASE_BOX_INDEPENDENT_REVIEW.md)
also gives the direct positive decomposition

    f-H2=(1-q)*(1-tau-aA/3)
          +[L*E*(a/3+1/2)-q*tau]>0.

The second bracket is `L*Q/(1-p)>0`; the first is positive because q<1 and
r=aA/3+tau<1. This necessity includes q=0 and a=1 whenever the actual domain
applies, without using the limited sufficiency part of the projection.

On the entire displayed closed box,

    B<=2277/4096<183/200.

Consequently `H1<2B<T`. For the other alternative, expand

    f=1-q+(5/2-2p-pq/2)*E+2(q-1)*C.

Its derivatives in p,q,C are negative throughout the box, while its
E derivative is positive:

    f_p=-(2+q/2)E<0,
    f_q=-1-pE/2+2C<=-27/32<0,
    f_C=2(q-1)<0,
    f_E=5/2-2p-pq/2>=9951/4096>0.

Thus the maximum over every real point of the closed box occurs at
`p=0,q=31/64,C=3/64,E=33/64`. Exact evaluation gives

    f<=3597/2048<T,
    T-3597/2048=3771/51200>0.

Hence H2<T as well, and both necessary alternatives fail. The argument
covers irrational parameter points and boundary faces, not merely sampled
corners or the finite rational probe.

The box satisfies the preceding simple forward base cuts, including
`B-A>83/200` and `LE>183q/250`, throughout. Its height enclosure is disjoint
from the previously certified Y rectangles, including the strong anchor.
These comparisons and the interval arithmetic are checked in the
[independent review and receipt](../results/det5_projected_base_box_independent_review.json).
The enclosing Y intervals are **not an excluded height-only rectangle**:
the restrictions on C,E are essential. The 258-entry height queue therefore
is not altered by this box result.

The product of its four coordinate side lengths is `1/1048576`. This is
compact-parameter volume, not physical tetrahedron volume, residual-body
measure or excluded area in the Y square. All 58 necessary contact types
remain, and the global flatness conjecture remains open.

The rational projection controls and
[finite base probe](../experiments/det5_horizontal_projection_probe.py) use
exact arithmetic, with no SMT or optimization solver. They are separate
from the universal box proof: fixed-base feasibility means feasibility of
the specified necessary relaxation, not existence of an actual target body.
