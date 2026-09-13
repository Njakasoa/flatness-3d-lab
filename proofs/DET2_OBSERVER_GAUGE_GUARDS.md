# Sixty-four complete guards from contact-edge gauges

For the determinant-two contact tetrahedron P and a compact, full-dimensional
convex K containing P with its four vertices on bd(K), suppose

    gamma_(K-K)(v) > beta=37/102

for each of the six primitive contact-edge directions v. Then hollowness
of K is equivalent to exclusion of **64 explicit lattice points**. In the
positive pair-dominant chart only **20** of these exclusions are nontrivial.
This statement does not require a volume bound. The six edge-gauge
hypotheses are essential to this reduction and must be explicitly retained
in the solver; the previous three coordinate-axis cuts do not replace them.

The already established ACMS implication makes these hypotheses necessary
for a genuinely hollow body of width >17/5. Their role in the feasibility
model is as asserted necessary inequalities, so sufficiency of the reduced
hollowness screen is not inferred circularly from assumed hollowness.

## Convex combinations truncate each observer line

Use the twelve-line theorem in DET2_OBSERVER_LINES.md. For one of its lines,
let p_a,p_b be the two contacts at a slab level and write

    v=p_b-p_a,  q_t=p_a+r+t*v,  t in Z.

The two vectors v,r form a basis of the plane lattice. Orient the opposite
contact edge w so its coordinates in this basis are

    w=a*v+d*r,

where d is the normalized volume of the contact tetrahedron (d=2 here).
The coefficient has magnitude d because the two contact segments lie on
consecutive primitive lattice planes. Primitivity of w implies gcd(a,d)=1.

If q_t belongs to K, then the vectors q_t-p_a, q_t-p_b and -w belong to
K-K. Convexity gives

    d/(d+1)*(q_t-p_a) - 1/(d+1)*w = (d*t-a)/(d+1)*v in K-K,
    d/(d+1)*(q_t-p_b) - 1/(d+1)*w = (d*(t-1)-a)/(d+1)*v in K-K.

Also +/-v belongs to K-K. Symmetry therefore yields

    gamma_(K-K)(v) <= 1/rho_t,
    rho_t=max(1, |d*t-a|/(d+1), |d*(t-1)-a|/(d+1)).

Only this upper bound is used; it need not be the exact gauge. The asserted
strict lower bound gamma_(K-K)(v)>beta implies rho_t<1/beta. Thus any
possible minimal interior lattice witness on this line has

    a/d + 1 - (d+1)/(d*beta) < t < a/d + (d+1)/(d*beta).

This is a proved finite parameter interval, independent of coordinates of
the real body or of its volume. Endpoints remain strict.

For d=2, a is odd. At beta=37/102 the bounds retain exactly seven integer
parameters on each of the twelve lines. Their union has 64 points. The
pair row-domain triangle excludes 44 automatically, leaving these 20:

    (-5,-2,1), (-5,1,-2), (-3,-1,1), (-3,1,-1),
    (-1,0,1), (-1,0,2), (-1,0,3), (-1,1,0), (-1,2,0), (-1,3,0),
    (1,-2,0), (1,-1,0), (1,0,-2), (1,0,-1), (1,0,0),
    (3,1,1), (5,1,2), (5,2,1), (7,1,3), (7,3,1).

The exact generator records all bases, opposite-edge identities, open
intervals, integer parameters, points and tautological exclusions. These
counts supplement the geometric completeness proof; they do not replace it.

## General nonunimodular bound

For any empty contact tetrahedron with normalized volume d>1, the
previous theorem supplies at most twelve lines. Under the six primitive
contact-edge gauge bounds at the same beta, each parameter interval has
length

    2*(d+1)/(d*beta)-1 <= 3/beta-1 = 269/37 < 8.

An open interval of this length contains at most eight integers. Therefore
**at most 96 explicit lattice points suffice** to test hollowness, under
the same boundary-contact and gauge hypotheses. This is an upper count;
it is not a claim that all 96 are distinct or necessary. The unimodular
contact case is outside this theorem.

## Encoding the additional hypotheses

For a column-normalized tetrahedron K={x:F lambda(x)>=0}, the exact gauge
identity is

    gamma_(K-K)(v)=1/2*||F ell(v)||_1,
    ell(v)=(X/2-Y-Z,X/2,Y-X/2,Z-X/2).

Since the four components sum to zero, this is the maximum over fourteen
nonempty proper subset sums. Hence each of the six required bounds is a
disjunction of affine inequalities in F. Together with the 20 exclusions,
the already complete 37 width directions and the eight-variable column
chart, they preserve the cubic degree bound of the feasibility model.

The generic observer-line principles have established antecedents in
Averkov–Schymura; the five-point width-one input is Blanco–Santos/Howe.
This explicit gauge truncation is internally derived and reviewed but its
mathematical priority remains unconfirmed. No new flatness upper bound is
inferred from the existence of the formulation.

Reproduce with `python3 -m experiments.det2_observer_gauge_guards`.
Certificate: certificates/det2_observer_gauge_guards.json.
