# Exact base projection of the forward middle gauge subsystem

Status: necessary-and-sufficient base conditions for one explicitly limited
subsystem. This does not project the full four-gauge problem, reconstruct all
fiber variables, or establish a large-width body. No solver queries are used.

Use the forward [negative-determinant chart](DET5_NEGATIVE_DETERMINANT_GAUGE_NORMAL_FORM.md)
and the strict [projected exceptional observer](DET5_FOUR_BASE_SHAPE_CUTS.md).
Fix base coordinates satisfying

    0<=p,q<1, C,E>0, C+E<1,
    L=1-pq, y=(1-q)/L, x=p*(1-q)/L,
    A=C+pE, B=qC+E, alpha=(1-p)E, Delta=B-A,
    d=y-x>0, w=1-y>=0, T=183/100, beta=T/5.

Then `A,B,alpha>0`, `A,B<1`, and the identity

    alpha-w*Delta=dB                               (1)

holds exactly.

The subsystem considered here asks whether there exist real `a,tau` with

    0<a<1, tau>0,
    tau<1-aA/3,
    Q=alpha*(a/3+1/2)-w*tau>0,
    H2=tau+(2-a/3)*Delta>T.                        (2)

The a endpoint is open as specified in this subsystem. Replacing `a<1` by
`a<=1` would have the same existential answer: a feasible endpoint can be
perturbed slightly downward, since every other inequality is strict and
continuous. This does not identify endpoint parameter values pointwise.

## Exact polynomial answer, including q=0

There exist a,tau satisfying (2) **if and only if** all three following
strict base conditions hold:

    1+2Delta>T,                                    (I)
    L*E+2q*Delta>6beta*q,                           (II)
    1-q+(L*E)/2+2Delta>T.                           (III)

These conditions are polynomial in the four fixed base coordinates
`p,q,C,E` once `Delta=(q-1)C+(1-p)E` is substituted. They use no division by
q, p, `1-q`, or `1-y`, and are consequently suitable for closed interval
boxes that touch q=0. The claimed equivalence still assumes the actual
base domain above; polynomial evaluation outside that domain is not a
geometric sufficiency assertion.

## Interior derivation when w>0

For any fixed `a in (0,1)`, the two strict upper bounds on tau in (2) are

    U_tau1=1-aA/3>0,
    U_tau2=alpha*(a/3+1/2)/w>0.

The strict lower bound is `tau>max(0,T-(2-a/3)Delta)`. Thus such tau exists
exactly when both upper bounds exceed the gauge lower bound. Equivalently,

    U1(a):=1+2Delta-aB/3>T,
    U2(a):=2Delta+alpha/(2w)+a*dB/(3w)>T.            (3)

The second identity uses (1). The first function is strictly decreasing
and the second strictly increasing because `B,d,w>0`. Define

    a_high=3*(1+2Delta-T)/B,
    a_low=3*(w*(T-2Delta)-alpha/2)/(dB).

Then (3), together with `0<a<1`, is exactly the open interval requirement

    max(0,a_low)<a<min(1,a_high).                   (4)

That interval is nonempty precisely when

    a_high>0, a_low<1, a_low<a_high.                (5)

The first condition in (5) is (I). For the second, exact multiplication by
the positive `dB/3` gives

    (1-a_low)*dB/3
      = (5/6)*(alpha+2w*Delta-(6T/5)*w)
      = (5/6)*(1-x)*(L*E+2q*Delta-6beta*q).

Thus it is (II). For the third,

    (a_high-a_low)*dB/3
      = d+alpha/2+(1-x)*(2Delta-T)
      = (1-x)*(1-q+(L*E)/2+2Delta-T).

Since `1-x>0`, this is (III). This proves necessity and sufficiency without
sampling a or tau.

The proof is constructive. When (I)--(III) hold, choose a as the midpoint
of the nonempty interval (4). Choose tau as the midpoint between
`max(0,T-(2-a/3)Delta)` and `min(U_tau1,U_tau2)`. Both midpoints satisfy
all strict inequalities. Rational base coordinates give rational witnesses.
These are witnesses of subsystem (2), not of all original geometry.

## Endpoint q=0

When q=0, `y=1`, `w=0`, `L=1`; the observer expression
`Q=alpha*(a/3+1/2)` is automatically positive. Only `U1(a)>T` remains.
A feasible `a in (0,1)` exists precisely when `U1(0)=1+2Delta>T`, namely
(I). Condition (II) is then simply `E>0`, already true, and (III) follows
from (I) because it adds the strictly positive term `E/2` to its left side.
Hence the same three polynomial conditions are exactly correct at q=0.
A constructive choice is `a=min(1,a_high)/2`, followed by a tau midpoint
using just `U_tau1` and the positive lower bound as above.

All displayed base inequalities are strict. If any required condition
holds only at equality, no point in the open subsystem (2) is supplied by
this projection. In particular, overlapping closed a intervals would not
be a valid substitute for (4).

## Relation to the full problem

The middle gauge H2 is one possible witness for the forward `(1,0,0)`
physical gauge target. These conditions exactly eliminate a,tau only from
(2). The other horizontal gauges, determinant-volume margins, remaining
observers, actual t,h feasibility, inherited exclusions and complete width
requirements still have to be imposed. Thus a base satisfying (I)--(III)
may still be excluded by the full problem. Conversely, a failure rules out
this particular middle-gauge subsystem and is a valid necessary cut on
any full candidate that uses H2.

Run `.venv/bin/python tests/replay_det5_forward_middle_projection.py`.
The [exact replay record](../results/det5_forward_middle_projection_validation.json)
checks the symbolic identities, exact interval equivalence on rational
fixtures, strict boundary examples and constructive rational subsystem
witnesses. The open-interval argument above proves universal equivalence;
these fixtures are not a continuous domain cover.
