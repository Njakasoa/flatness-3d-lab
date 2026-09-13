# Direction-coupled envelopes for the scaled frame

Status: valid necessary linear cuts and a partial geometric explanation of
the certified rectangle. No new infeasibility, larger excluded rectangle,
contact-class exclusion, or global flatness bound is claimed here.

Use the notation of [the scaled frame](DET5_SCALED_VERTEX_HEIGHT_FRAME.md):
T_i=b(v_i-v_L), b=1/w_Y(K), F is the contact matrix, and the shared lifted
variables W_ij,k represent F_ij T_i,k. Write beta=183/500,
R=6/(5 beta^3), Bmin=1/R and Bmax=5/17.

## What the certified height ordering already forces

In the chart Y-extrema=[0,3], the certified Y box has
q0=0, q3=1 and q1,q2>=3/4. Write F^Tq=a*1+b*(0,1,1,0).
Column stochasticity and the shared height products give

    a >= 3/4+F30/4,
    a+b <= 1-F01,
    a+b <= 1-F02,
    a <= 1-F03.

Consequently

    b+F01+F30/4 <= 1/4,
    b+F02+F30/4 <= 1/4,
    F03+F30/4 <= 1/4.

Because the off-diagonal entries are positive, b<1/4: the actual Y-width
is greater than four throughout this exact normalized box. The minimum-Y
vertex contributes only small barycentric weights to the other contact
columns. This explains a significant geometric restriction of the box, but
is not by itself a contradiction with the five directional lower bounds.
These displayed inequalities are already consequences of the existing
shared Y envelopes and contact equations, so adding them does not strictly
strengthen that linear relaxation.

The five width directions in the verified obstruction are
Y, U=(1,-1,-2), Z, Y-Z, and U-Y=(1,-2,-2). Their lower bounds together with
the full imposed gauge, observer and volume conditions have a checked finite
refutation on the stated box. An elementary analytic contradiction using a
smaller subset of those assumptions has not been established by this note.

## New static directional envelopes need no new variables

Fix a matrix entry f=F_ij, with a valid interval l<=f<=h, and a covector u.
Define the existing linear expressions

    g=u dot T_i,
    z=u dot W_ij.

For an exact frame, z=f*g. Suppose Glo<=g<=Ghi is a valid bound. Add the
four ordinary scalar product envelopes

    z >= l*g+Glo*f-l*Glo,
    z >= h*g+Ghi*f-h*Ghi,
    z <= h*g+Glo*f-h*Glo,
    z <= l*g+Ghi*f-l*Ghi.                                (1)

These inequalities are linear in variables already present in the scaled
frame. They share the same W_ij,k used by every contact equation; a new
independent copy of the directional product would lose the intended
coupling. Validity follows, respectively, from
(f-l)(g-Glo)>=0, (h-f)(Ghi-g)>=0,
(h-f)(g-Glo)>=0 and (f-l)(Ghi-g)>=0.

The actual volume necessity and the containing-simplex lemma give

    |u dot T_i| < R*w(P,u)*b <= R*w(P,u)*Bmax,

because T_L=0. Hence Glo=-R*w(P,u)*Bmax and
Ghi=R*w(P,u)*Bmax are valid closed initial bounds. These depend on the
actual contact width in direction u. In contrast, even retaining the normalized Y bound, summing individual
coordinate bounds gives 5R*Bmax*|u_X|+|u_Y|+2R*Bmax*|u_Z|. For U this is
9R*Bmax+1, while its contact-width bound is 2R*Bmax. The complete
fifteen-direction set therefore provides
useful coupled envelopes, even though its directional span bounds were
already present as separate inequalities on T.

For fixed f and T, the current coordinate envelopes do not in general
imply (1). An exact rational local example is checked by
[the accompanying replay](../tests/replay_det5_direction_envelopes.py).
It satisfies the three coordinate envelopes, including a tightened
Y-interval [3/4,1], but violates a U-direction envelope. This example only
establishes strictness of the local product relaxation; it is not asserted
to satisfy the full contact model or represent a geometric body.

## Bounds from a retained U chart

If the Y reference L is also the selected minimum-U index, then
u=U gives g_i>=0. With selected maximum-U index H_U, write
D=U dot T_HU. The U target and its volume bound imply

    W*Bmin < D < 2R*Bmax,   where W=17/5.

For a normalized U interval r_i in [rlo,rhi], the closed bounds
rlo*W*Bmin <= g_i <= rhi*2R*Bmax are valid. In particular the certified
r1,r2>=1/2 give a positive lower bound for their U products. The extrema
have normalized intervals [0,0] and [1,1].

For an arbitrary retained U chart, let r_L have its known normalized
interval as well. Since T_L=0,

    U dot T_i = D*(r_i-r_L).

Interval multiplication of [rlo_i-rhi_L, rhi_i-rlo_L] with
[W*Bmin, 2R*Bmax] gives a valid scalar interval for g_i. Intersect it with
the general directional bound before applying (1). Correlations discarded
by interval multiplication only weaken the bound and cannot make it unsafe.

Other linear relations can improve directional bounds. In the certified
chart, for example, U-Y equals g_U-q_i. Using g_U>=0 gives
(U-Y) dot T_i >= -qhi_i, much sharper than the symmetric contact-width
bound in that direction. Every such bound must hold over the whole current
box, rather than only at a saved relaxed assignment.

## A perspective variant retains the dependence on b

A further valid formulation adds shared variables tau_ij=b*F_ij. For exact
products, column stochasticity gives sum_i tau_ij=b and tau_jj=0.
There can be eight independent tau variables: express the third
nonzero entry of each column as b minus its first two tau entries.
Apply the usual McCormick bounds to tau=b*f on
f in [l,h], b in [Bmin,Bmax].

If a directional bound has the homogeneous form A*b<=g<=B*b, then the
following additional inequalities are valid:

    z >= l*g+A*tau-l*A*b,
    z >= h*g+B*tau-h*B*b,
    z <= h*g+A*tau-h*A*b,
    z <= l*g+B*tau-l*B*b.                                (2)

To prove this, set x=g/b, which lies in [A,B] because b>0, apply scalar
McCormick to f*x, and multiply by b. Substitution of the exact identities
g=b*x, tau=b*f and z=b*f*x makes each slack b times a product of two
nonnegative interval factors. Choosing A=-R*w(P,u), B=R*w(P,u) retains the
actual volume bound rather than replacing b by its global maximum.

All directions for a given F entry must use the same tau and the same W.
These are necessary outer cuts; McCormick envelopes for tau do not impose
the exact equation tau=b*f. Consequently SAT remains relaxed feasibility,
and no conclusion about an actual body follows without reconstruction.

## Arithmetic verification and limits

Run `python3 tests/replay_det5_direction_envelopes.py`. It verifies the
universal polynomial identities behind all four static and all four
perspective envelopes, checks the contact widths of the fifteen directions,
and certifies the rational local strictness example. It imports neither a
solver nor the geometry engine. The
[receipt](../results/det5_direction_envelope_validation.json) records this
scope. No old solver target was run or changed for this derivation.
