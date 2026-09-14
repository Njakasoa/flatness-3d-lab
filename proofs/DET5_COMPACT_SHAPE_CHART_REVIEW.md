# Bounded shape coordinates and exclusion of the collapsed-height corner

Status: independent algebraic reduction and necessary lower bound on one
shape denominator. This does not cover all shape fibers or exclude the
remaining determinant-five class. No solver queries are used.

## Bijection and exact domain

Start with the ordered branch of the [eight-parameter height
chart](DET5_RATIONAL_HEIGHT_CHART_REVIEW.md), with `0<=x<y<=1`. Define

    p=x/y, q=(1-y)/(1-x), C=(1-x)c, E=y e,
    L=1-pq, S=C+E.

Then `0<=p,q<1` and `L>0`. Conversely, every such pair gives

    y=(1-q)/L, x=p(1-q)/L,
    1-x=(1-p)/L, 1-y=q(1-p)/L,
    d=y-x=(1-p)(1-q)/L.

These formulas are mutually inverse. In particular, `p=0` is precisely
`x=0`, and `q=0` is precisely `y=1`; the tied-extremum cases remain included.
There is no chart point with `p=1` or `q=1`.
The scale variables are recovered by `c=C/(1-x)` and `e=E/y`.
The full positivity conditions are exactly

    C>0, E>0, C<t<1-E,
    r>0, u>0, h>x+d*t,
    h-y*r>0, 1-h-(1-y)*r>0,
    h-x*u>0, 1-h-(1-x)*u>0.

They imply `S<1`, `0<r,u<1`, and `0<h<1`. Thus all six shape
coordinates `(p,q,C,E,r,u)` are bounded. The displayed conditions,
including fiber feasibility, must still be retained: membership in a box
alone is not sufficient.

With columns indexed from zero, the matrix becomes

    col0 = (0, 1-t+q*C, t-C, (1-q)*C),
    col1 = (1-h-(1-y)*r, 0, r, h-y*r),
    col2 = (1-h-(1-x)*u, u, 0, h-x*u),
    col3 = ((1-p)*E, 1-t-E, t+p*E, 0).

Its horizontal determinant factor is

    D=u*(C+p*E)-r*(q*C+E),    det F=(h-x-d*t)*D.

This is a bounded rational chart, not initially a compact domain: its
strict faces are excluded and the corner `p=q=1` makes `L=0`.
Clearing powers of `L` preserves inequality directions whenever `L>0`.

## A quantitative denominator bound for a putative large-width body

Let `b=h-x-d*t>0`. Suppose the guards for the integer observers `(2,1,1)`
and `(3,1,1)` hold. In this height order their exact reductions are

    u <= (q*C+E)/3 OR R3,
    r <= (C+p*E)/3 OR R0,

where

    R3: (1-q)*C >= 2*F31+3*F32,
    R0: (1-p)*E >= 3*F01+2*F02.

The alternative `R3` is in fact impossible on this exact chart. The strict
condition `1-h-(1-x)*u>0` gives

    F32=h-x*u >= (h-x)/(1-x)
               =(d*t+b)/(1-x) > d*C/(1-x)=F30.

For `x=0` the first inequality is equality, but the following strict
inequality still gives `F32>F30`. Thus `F30>=2*F31+3*F32` cannot hold.
In particular, the first observer guard reduces to the single inequality

    3*u <= q*C+E.                                      (1)

Now suppose `gamma(2,0,1)>beta>1/3`. Then

    L > beta-1/3.                                     (2)

No positive lower bound on `b` beyond `b>0` is needed.
First `1-p<=L`, `1-q<=L` and `d<=L`: for the last inequality,
`(1-p)(1-q)<=L^2` because both factors are at most `L`.

By (1), `u<=S/3`.
If the main alternative of the second guard holds, also `r<=S/3`.
Otherwise `R0` gives `F02 <= (1-p)*E/2`. Using

    F02-F01=(1-x)*(r-u)-d*r,
    d/(1-x)=1-q,    (1-p)/(1-x)=L,

and `F01>0`, we obtain

    r-u < (1-q)*r+L*E/2 < 3*L/2.

In both cases `max(r,u)<=S/3+3*L/2`.
To bound the selected gauge, put

    A=(1-x)*(u-r)+d*r,
    B=x*(u-r)-d*r,             A+B=u-r.

These are coordinates 0 and 3 of `F(e1-e2)`. Coordinates 1 and 2 are
`-u,r`. Also

    F(e3-e0)=((1-p)*E, -(q*C+E), C+p*E, -(1-q)*C).

The lattice vector `(2,0,1)` has image
`[2*F(e1-e2)+F(e3-e0)]/5`. Its row 1 is negative and row 2 positive.
For a sum-zero vector the gauge is the sum of its positive coordinates.
The elementary positive-part estimates

    A_+ + B_+ <= (u-r)_+ + d*r,
    (2*A+(1-p)*E)_+ <= 2*A_+ +(1-p)*E,
    (2*B-(1-q)*C)_+ <= 2*B_+

therefore give

    gamma(2,0,1) <= [S+2*max(r,u)+2*d*r]/5
                  < 1/3+L.

Together with `gamma>beta`, this proves (2).
No determinant lower bound is needed in this argument.

For a hollow actual body with global lattice width greater than `17/5`,
the [existing ACMS deduction](DET5_VOLUME_GAP_BOUNDS.md) permits
`beta=183/500`. Consequently the necessary chart condition is

    1-p*q > 49/1500.                                  (3)

If only the weaker ten-gauge threshold `beta=37/102` is assumed, the same
proof gives `1-p*q>1/34`. Both conclusions remove the denominator-zero
corner under the stated finite necessary constraints. The global-width
hypothesis is one established way of obtaining the strong gauge threshold;
the denominator lemma itself needs only the selected gauge and two guards.
Both observer guards are necessary for hollowness, so no sufficiency claim
about a finite observer list is used.

## Reverse height order

The following extension was proposed independently by the fiber-cell reviewer
and checked again here. Conjugate the canonical matrix by the swap of indices
1 and 2, retaining the physical lattice vectors in their original ordering.
The same two integer observer guards become

    u <= (q*C+E)/2 OR F30>=3*F31+2*F32,
    r <= (C+p*E)/2 OR F03>=2*F01+3*F02.

The first alternative involving `F30` remains impossible since `F32>F30`.
Consequently `u<=S/2`. The other exceptional alternative gives
`F02<=F03/3` and hence

    r-u < (1-q)*r+L*E/3 < 4*L/3.

In all cases `max(r,u)<=S/2+4*L/3`. Write the canonical horizontal
vectors as `V=F(e1-e2)` and `Z=F(e3-e0)`. The original lattice vector
`(2,0,1)` now has gauge `gamma((Z-2*V)/5)`; swapping only the shape
labels without changing this sign would be incorrect. Its row 1 is
`2*u-(q*C+E)<=0`. The sum of its positive row-0 and row-3 contributions
is at most `(1-p)*E+2*(r-u)_++2*d*r`. The remaining contribution is
`(C+p*E-2*r)_+`. Finally,

    2*(r-u)_+ +(C+p*E-2*r)_+
        <= max(2*r,C+p*E) <= S+8*L/3.

Therefore the physical lattice gauge satisfies

    gamma(2,0,1) < 1/5+17*L/15.

Under `gamma>beta>1/3` this implies

    L > 15*(beta-1/5)/17.

With `beta=183/500`, the reverse-order cutoff is

    1-p*q > 249/1700.                                 (4)

Thus (3) is a common valid lower bound in both height orders, and (4)
is stronger in the reverse branch. Neither bound needs a volume-derived
positive lower bound on the height gap. The chart hypothesis `b>0` remains
essential in eliminating the first observer alternative.

On the enlarged closed outer shape domain obtained by retaining (3) as
`L>=49/1500` and closing the other bounded intervals, all displayed rational
matrix coefficients have denominators uniformly separated from zero.
Other degenerate faces and `D=0` still require their own treatment; this
result supplies no finite coverage certificate.

Reproduce with `.venv/bin/python tests/replay_det5_compact_shape_chart.py`.
The replay independently checks rational identities and exact fixtures;
the inequalities above supply the universal argument. Its output is
[the validation record](../results/det5_compact_shape_chart_validation.json).
