# Negative-determinant coordinates and reduced horizontal gauges

Status: exact algebraic reduction on the surviving determinant-sign branch.
No solver query, global exclusion, or finite continuous cover is claimed.

Use the canonical [compact height chart](DET5_COMPACT_SHAPE_CHART_REVIEW.md)
and the [proved necessary sign](DET5_POSITIVE_HORIZONTAL_DETERMINANT.md),
with

    0<=x<y<=1, p=x/y, q=(1-y)/(1-x),
    A=C+pE, B=qC+E, S=C+E,
    alpha=(1-p)E, omega=(1-q)C,
    Z=(alpha,-B,A,-omega),
    V=((1-x)u-(1-y)r,-u,r,xu-yr).

The physical lattice images, multiplied by five, are `V-2Z`, `2V+Z`,
`V+3Z`, and `3V-Z` for directions `(1,0,0)`, `(2,0,1)`, `(1,0,1)`,
and `(3,0,1)` in the original height order `q1<q2`. In the reverse original
order `q1>q2`, replace V by -V while retaining Z. This accounts for the
simultaneous canonical row/column permutation and the original physical
contact indexing.

## Coordinates on D<0

Put `k=3` in the forward order and `k=2` in the reverse order. The simplified
observer necessity is `ku<=B`. Since `A,B,u,r>0`, define

    a=ku/B in (0,1], zeta=-D=rB-uA>0, tau=zeta/B>0.

These have the exact inverse

    u=aB/k, r=aA/k+tau, zeta=tau*B.

Consequently this is a bijective change of the `(u,r)` coordinates on the
negative branch satisfying the simplified observer, with all remaining
original chart constraints retained. The original strict bound `r<1` implies

    0<tau<1-aA/k<1,    0<zeta<B.

For a true hollow-body global target `w(K)>17/5`, the already established
[determinant margin](DET5_COMPACT_FIBER_DENOMINATOR_REVIEW.md) gives

    zeta>deltaD=34728093/250000000.

Thus the new coordinate denominator is uniformly positive on actual target
geometries:

    B>zeta>deltaD,   tau*B>deltaD,
    B*(1-aA/k)>deltaD.

These determinant margins use the true global-width premise; they do not
follow solely from a finite horizontal gauge list. The algebraic coordinate
change itself only needs `B>0` and `D<0`.

Define the sum-zero vector

    W=(-(1-y),0,1,-y).

The identities `(1-x)B-(1-y)A=alpha` and `xB-yA=-omega` prove

    V=(a/k)Z+tau*W.                                  (1)

## Two exact max formulas

For a sum-zero vector let `Gamma(v)=||v||_1/2`, equivalently the sum of its
positive coordinates. For `c,t>=0`, define

    P(c,t)=max(cS+yt, cA+t).                          (2)

For `j,t>=0`, define

    N(j,t)=max(jB, t-j(A-B), jS-yt).                  (3)

Then the following are exact, not upper estimates:

    Gamma(cZ+tW)=P(c,t),
    Gamma(-jZ+tW)=N(j,t).                            (4)

For the first identity, the vector's row 1 is nonpositive, row 2 is
nonnegative and row 3 is nonpositive. Summing positive coordinates gives
`cA+t+max(c*alpha-(1-y)t,0)`, which is (2) since `A+alpha=S`.

For the second identity, row 0 is nonpositive and row 1 is nonnegative.
The remaining variable positive parts are `t-jA` and `j*omega-yt`.
They cannot both be strictly positive: if `t>jA`, then
`yt>j*y*A>=j*omega`, using `omega=yA-xB<=yA`. This remains valid at `x=0`,
`y=1`, `j=0`, and `t=0`. Therefore their sum of positive parts is their
maximum together with zero. Adding the fixed positive part `jB` gives (3),
using `B+omega=S`. This disjointness reduces four potential subset values
to three. The identity also includes equality at every transition surface.

## Four physical gauges in both orders

The following table gives **five times** each gauge. All displayed
arguments of P and N are nonnegative because `0<a<=1` and `tau>0`.

| Physical lattice vector | Forward order `q1<q2`, k=3 | Reverse order `q1>q2`, k=2 |
| --- | --- | --- |
| `(1,0,0)` | `N(2-a/3,tau)` | `P(2+a/2,tau)` |
| `(2,0,1)` | `P(1+2a/3,2tau)` | `N(1-a,2tau)` |
| `(1,0,1)` | `P(3+a/3,tau)` | `N(3-a/2,tau)` |
| `(3,0,1)` | `N(1-a,3tau)` | `P(1+3a/2,3tau)` |

The reverse table uses the evenness `Gamma(v)=Gamma(-v)` after substituting
`V=(a/2)Z+tau*W`; this avoids losing the physical sign change. In particular,
at the allowed endpoint `a=1`, both `N(1-a,2tau)` and `N(1-a,3tau)` reduce
to their second argument. No separate endpoint chart is necessary.

For example, the forward `(2,0,1)` formula is

    5*gamma(2,0,1)
      = max((1+2a/3)S+2y*tau, (1+2a/3)A+2tau).

For fixed `x,y,C,E`, all pieces in the table are affine in `(a,tau)`.
Thus a strict lower gauge target `gamma(v)>beta` is exactly an OR of two
or three strict inequalities, each displayed piece being `>5*beta`.
There are ten alternatives in total across these four gauge disjunctions
in each order, compared with fourteen subset alternatives per unrestricted
sum-zero gauge. This is a representation reduction, not a count of complete
Boolean branches or a proof that these four gauges determine the first
lattice minimum.

If base shape coordinates also vary, terms such as `aA`, `aS` and `y*tau`
remain products. The formulas do not turn the entire continuous shape
problem into a linear program, and all strict chart, determinant, remaining
gauge, observer and width conditions retain their prior scope.

## Target-specific simplifications

Set `beta=183/500`, so `5*beta=183/100>1`. The domain has
`0<a<=1`, `B,S<1`, `tau>0` and `y>0`. Hence for `j=1-a`, both
`jB` and `jS-y*t` are strictly less than 1 whenever `t>=0`.
In the N formula only its middle piece can exceed `183/100`. Consequently,
under the retained domain, the following equivalences are exact:

    forward: gamma(3,0,1)>183/500
          iff 3*tau-(1-a)*(A-B)>183/100,

    reverse: gamma(2,0,1)>183/500
          iff 2*tau-(1-a)*(A-B)>183/100.

These three-piece strict disjunctions therefore become one strict atom each
at this target. Equality in the displayed atom does not satisfy the original
strict gauge target, including at the permitted endpoint `a=1`.

There is a further necessary disjunction for the forward `(1,0,0)` gauge.
Write `j=2-a/3`, so `j<2`. Its first and third N pieces satisfy

    jB<2S,       jS-y*tau<2S.

Its middle piece satisfies, using `tau<1-aA/3`,

    tau-j*(A-B) < 1+2*(B-A)-aB/3.                   (5)

Thus the strict lower gauge target implies

    S>183/200
    OR 1+2*(B-A)-aB/3>183/100.                     (6)

If the first or third piece exceeds `183/100`, then `2S>183/100`.
Otherwise the middle piece must exceed the target, and (5) proves the
second alternative. Since `aB/3>0`, (6) in turn implies the weaker
base-shape-only disjunction

    S>183/200 OR B-A>83/200.                        (7)

All inequalities in (6) and (7) are strict: equality at either threshold
alone does not satisfy that alternative. Unlike the first two equivalences,
(6) and (7) are only necessary consequences, not equivalent gauge formulas.
They can be added as cuts, but must not replace the original `(1,0,0)` gauge
unless only an outer necessary relaxation is intended. No sufficiency for
all gauge, observer, chart or width constraints follows from these cuts.

Run `.venv/bin/python tests/replay_det5_negative_determinant_gauges.py`.
The [replay record](../results/det5_negative_determinant_gauges_validation.json)
checks the coordinate identities symbolically, the physical vector
identification in both orders, and rational fixtures including transition
and endpoint cases. The universal argument is the row-sign proof of (4);
the fixtures are not a sampled continuous cover.
