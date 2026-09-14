# Independent review of the continuous projected base box

Status: PASS. The closed four-parameter box in
[the archive](../results/det5_projected_base_box.json) is excluded for actual
forward-order Y[0,3] target bodies, with all admissible remaining parameters
free. This is a continuous inequality argument, not a sampled box test or a
new global flatness bound. Reviewed sources are bound in
[the independent receipt](../results/det5_projected_base_box_independent_review.json).

## Independent necessity of the projected H2 inequality

Put `Delta=B-A`, `H2=tau+(2-a/3)*Delta`, and

    f=1-q+L*E/2+2*Delta.

An elementary decomposition proves the needed implication directly:

    f-H2=(1-q)*(1-tau-aA/3)
          +[L*E*(a/3+1/2)-q*tau].                 (1)

The second bracket is `L*Q/(1-p)`. It is strictly positive because Q>0
and the actual compact domain has L>0 and p<1. The first term is strictly
positive by q<1 and the strict bound `tau<1-aA/3`. Thus H2<f, including
at a=1 or q=0 whenever the stated actual domain applies. No division by
q or by `1-y`, and no replacement of an actual a endpoint, is needed for
this necessity. It agrees with condition (III) of
[the exact H2 subsystem projection](DET5_FORWARD_MIDDLE_GAUGE_EXACT_PROJECTION.md).
The full subsystem sufficiency theorem is not required for this box proof.

The prior [four-base review](DET5_FOUR_BASE_SHAPE_CUTS_INDEPENDENT_REVIEW.md)
justifies that H3 cannot witness the first horizontal gauge jointly with
the second target. Therefore the complete forward gauge conjunction requires
H1>T or H2>T, with `H1=(2-a/3)B` and `T=183/100`.

## Monotonic bounds over the whole closed box

The reviewed parameter intervals, in order `(p,q,C,E)`, are

    [0,1/32] x [31/64,33/64] x [3/64,5/64] x [31/64,33/64].

Expand f as

    1-q+(5/2-2p-pq/2)*E+2(q-1)*C.

Its partial derivatives with respect to p,q,C are strictly negative
throughout this box, and its E derivative is strictly positive. In particular,
`f_q<=-27/32<0` and `f_E>=9951/4096>0`; the other two signs follow
from E>0 and q<1. Thus its exact maximum occurs at
`p=0,q=31/64,C=3/64,E=33/64` and equals

    f<=3597/2048<183/100,
    183/100-3597/2048=3771/51200>0.

This monotonicity proves the upper bound at every real point of the closed
box, including irrational points and all boundary faces. A corner evaluation
without this sign argument would not by itself have been sufficient.
Also `B=qC+E<=2277/4096<183/200`, so
`H1<2B<183/100`. By (1), H2<f<T. Both surviving alternatives fail,
proving the target exclusion uniformly in a,tau,t,h and the corresponding
original r,u. The proof uses necessary target conditions only and asserts
no realization of a body at any parameter point.

## Comparisons with earlier necessary base cuts

Monotonic endpoint bounds give uniformly

    B-A >= 1757/4096 > 83/200,
    L >= 2015/2048 > 49/1500,
    L*E >= 62465/131072 > 6039/16000 >= (183/250)*q.

Hence the earlier forward base disjunction is satisfied by its asymmetric
alternative throughout this box, and the earlier LE and height-separation
cuts are also satisfied. The strict domain C,E>0 and C+E<1 holds throughout;
`S>183/500` and `B>34728093/250000000` hold as well. The earlier necessary
endpoint-separation cut `M0*(1-p)>L` is also uniformly satisfied.
These comparisons concern these explicit base-only necessities; they are
not a claim that all former fiber constraints were simultaneously feasible.

## Heights, previous rectangles, and measure

Both normalized heights are monotone increasing in p and decreasing in q
(with possible zero derivatives at endpoints). Thus their actual ranges
are contained in

    x in [0,33/2017],
    y in [31/64,1056/2017].

Exact separating-coordinate comparisons show that this height enclosure is
disjoint from each of the seven original certified Y[0,3] rectangles,
the enlarged [3/5,1]^2 rectangle, and the later strong anchor rectangle
`[0,1/256] x [31/256,33/256]`. The large lower bound on L also keeps this
box outside the earlier forward separated-height band.

These displayed height intervals are only an enclosure of the heights of
the excluded four-parameter box. They are **not an independently excluded
Y rectangle**: removing the restrictions on C,E would invalidate this
inference. They must not be inserted into a height-only residual queue as
an excluded rectangle without another proof.

The product of the four compact-coordinate side lengths is exactly
`1/1048576`. This is parameter-space volume in `(p,q,C,E)`. It is not a
measure of residual bodies, a physical tetrahedron volume, a count of
realizable shapes, or a newly removed area in the Y-height square.
The archive correctly limits its measure and scope claims.

No correction is required. The root generator's arithmetic agrees with
these independent endpoint calculations. No solver query, prior replay,
or edit to the reviewed generator/archive was needed for this review.
