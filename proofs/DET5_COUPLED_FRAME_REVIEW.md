# Independent interval and shared-product review of the coupled frame

Status: sound necessary outer inequalities. The interval arguments below
hold continuously, including all closed box endpoints and either sign of a
relative U-height. They do not certify a solver result or exclude a new
contact class. The model is
[the coupled scaled frame](../experiments/det5_coupled_scaled_frame.py).

Use P=conv(0,(5,1,2),e2,e3), W=17/5, beta=183/500,
R=6/(5 beta^3), Bmin=1/R and Bmax=1/W. In the exact scaled frame,

    T_i=b(v_i-v_L),    Bmin<b<Bmax,
    Y dot T_i=q_i,    T_L=0.

The actual volume necessity gives every directional span bound
w_u(K)<R*w_u(P). Thus |u dot T_i|<R*w_u(P)*b for every vertex i.
The endpoints Bmin and Bmax may safely be included when constructing outer
intervals, even though the exact frame imposes strict inequalities.

## Arbitrary U-extrema and the Y reference index

Let U=(1,-1,-2), let its actual extrema be A,B, and write r_i for its
normalized heights. The known intervals for these heights are [0,0] at A,
[1,1] at B, and the current box intervals at the two other indices. Define

    D=b*w_U(K)>0.

Then, because the reference vertex for T is L rather than necessarily A,

    U dot T_i = D*(r_i-r_L).                             (1)

This subtraction is essential. If L=B, for example, all these relative
heights are nonpositive; treating them as nonnegative would be unsound.
The U target and volume bound give

    W*b < D < 2R*b,
    W*Bmin < D < 2R*Bmax.

For r_i in [li,hi] and r_L in [lL,hL], the difference belongs to
[li-hL,hi-lL]. Multiply this interval by the positive D interval, taking the
minimum and maximum of all four endpoint products. This handles positive,
negative and sign-crossing differences uniformly. Dependence between r_i
and r_L cannot invalidate the outer bound; discarding dependence enlarges
the possible set. At i=L the exact interval is [0,0], which the implemented
model correctly uses instead of the weaker independent subtraction bound.

The implementation intersects the resulting U interval with
[-2R*Bmax,2R*Bmax]. For Y it uses the direct normalized interval q_i.
For U-Y=(1,-2,-2), subtracting q_i yields the valid interval
[Ulo-qhi,Uhi-qlo], again intersected with its contact-width bound. The
mathematical implementation matches these rules for all possible extrema.

## Stronger per-vertex bounds available from the same hypotheses

Dividing (1) by positive b gives a homogeneous bound without first replacing
b by its largest possible value:

    (U dot T_i)/b in [li-hL,hi-lL] * [W,2R].

Likewise (Y dot T_i)/b belongs to [qlo/Bmax,qhi/Bmin]. Z has the generic
homogeneous interval [-2R,2R]. Every covector u=(ux,uy,uz) decomposes as

    u = ux*U + (ux+uy)*Y + (2ux+uz)*Z.                    (2)

Signed interval addition using (2), followed by intersection with
[-R*w_u(P),R*w_u(P)], gives another valid homogeneous bound. The analogous
operation on the static U,Y,Z intervals gives a static bound. Each interval
may also be intersected with the consequence of the other:

    static <- static intersect ([Bmin,Bmax]*homogeneous),
    homogeneous <- homogeneous intersect (static*[1/Bmax,1/Bmin]).

These operations need not find the best possible interval. Each preserves
every exact solution, which is the required property. Correlated intervals
are never assumed independent for an equality; only their containing product
or sum intervals are used. If a derived intersection is empty, that would
mean the underlying exact hypotheses have no solution on the current box,
not permission to swap endpoints or silently weaken a bound.

The helper in the independent replay implements these additional bounds.
They extend the implemented special cases to U-2Y and U+Y and to other
linear combinations. The current coupled model uses its documented static
special cases and the generic symmetric homogeneous caps; the existence of
these further valid intervals is not a claim that they were already encoded.

## Shared tau variables and envelope signs

For each contact entry f=F_ij in [0,1], set tau_ij=b*f in an exact frame.
Column stochasticity implies sum_i tau_ij=b and tau_jj=0. The implemented
model uses eight independent tau variables and defines each column's third
off-diagonal entry as b minus its other two tau entries. It then imposes all
four McCormick inequalities for every off-diagonal entry:

    tau >= Bmin*f,          tau <= Bmax*f,
    tau >= b+Bmax*f-Bmax,   tau <= b+Bmin*f-Bmin.

Thus the dependent entries are bounded too; their column identity does not
replace their individual envelopes. These inequalities are exact necessities
of tau=b*f on the closed containing domain.

For g=u dot T_i and z=u dot W_ij, where W_ij,k is the same shared product
used by the contact equations, static bounds lo<=g<=hi give

    z>=lo*f,   z>=g+hi*f-hi,
    z<=g+lo*f-lo,   z<=hi*f.

The homogeneous symmetric bound -cap*b<=g<=cap*b gives

    z>=-cap*tau,   z>=g+cap*tau-cap*b,
    z<=g-cap*tau+cap*b,   z<=cap*tau.

All signs in the model agree with these formulas. Their universal algebraic
proof is recorded in
[the direction-coupled envelope note](DET5_DIRECTION_COUPLED_ENVELOPES.md).
The same eight tau parameters and the same 24 W scalars are reused across
all fifteen directions. Giving each direction unrelated copies would be a
different, weaker relaxation.

## Removing already certified closed rectangles

The old twelve Y rectangles were certified with threshold 37/102 and
Y-width greater than W. Every exact target in the coupled model has Y-width
above W and all eighteen imposed gauges above 183/500>37/102, and an actual
hollow body satisfies every old integer guard. Therefore no exact target
can lie in those certified rectangles. The complement of a closed rectangle
is correctly encoded with strict inequalities:

    q1<lo1 OR q1>hi1 OR q2<lo2 OR q2>hi2.

The rectangle endpoints belong to the certified exclusion and must not be
reintroduced using non-strict complement inequalities. These complements
are justified on the exact global-target domain, not by interpreting an
old relaxed SAT point as a body.

## Independent checks

Run `python3 tests/replay_det5_coupled_intervals.py` for the standard-library
interval replay. It checks 18,432 endpoint/reference/sign cases for (1),
including L at either U-extremum, and representative per-vertex directional
bounds. These finite checks support the implementation; the continuous
validity is the interval proof above. The
[receipt](../results/det5_coupled_interval_validation.json) states this scope.

The separate
[encoding audit](../tests/audit_det5_coupled_scaled_independent.py) imports
only independent reconstruction helpers. It rebuilds the full new assertion
sets, binds source inputs and certified rectangles, and evaluates old saved
rational SAT assignments against the new tau-free static cuts. It makes no
solver calls. Rejection of an old assignment demonstrates an actual tightening
of the relaxation, but does not itself prove infeasibility of a whole box.

The first coupled campaign's independent audit passes all nine new encodings.
All nine recorded solver outcomes remain UNKNOWN. Separately, every one of
the fourteen old rational SAT assignments violates the new static directional
product envelopes, with 19 to 81 violations per assignment. None is rejected
merely by the scalar directional bounds or the certified-rectangle complements.
Thus the coupling itself strictly removes these saved relaxation points.
Four corrupted-formula controls are rejected. The
[encoding receipt](../results/det5_coupled_scaled_encoding_validation.json)
records the exact evaluations and preserves the lack of any new exclusion.
