# Adversarial independent review of the twelve-line reduction

Verdict: the proposed lemma is valid under the stated hypotheses: K is
compact, convex, full-dimensional, contains the fixed empty tetrahedron
P, and all four vertices of P lie on the boundary of K. No pair-dominance,
simplex, or volume hypothesis is needed for the twelve-line reduction.
No counterexample or exceptional degenerate case was found. No solver
was used in this review.

## Minimality argument

Compactness makes int(K) intersect Z^3 finite. If nonempty, choose z in
that set minimizing vol(conv(P,z)). P has only its four vertices as
lattice points, all on bd(K), so z is outside P and is a vertex of
Q=conv(P,z).

For q in Q intersect Z^3 other than the four contacts and z, emptiness
of P gives q outside P. Express q=t z+(1-t)p with p in P. Necessarily
0<t<1: t=0 would put q in P and t=1 would give q=z. Because z is
interior to K, this implies q is interior to K. Also conv(P,q) is a
proper full-dimensional convex subset of Q: an extreme point z of Q
cannot belong to conv(P,q), since q is distinct from z. Its volume is
therefore strictly smaller, contradicting minimality. The strict volume
claim must use this proper-subset argument; mere non-strict volume
monotonicity alone would not suffice.

Each p_i remains a vertex of Q. Otherwise it is a convex combination of
z and the other p_j. Its coefficient at z must be positive because p_i
is a vertex of P, making p_i interior to K, a contradiction. Hence Q
has exactly five lattice points, all vertices. This also excludes all
collinear-third-point and redundant-contact degeneracies.

## External theorem and its precise applicability

The primary source is [Blanco and Santos, Lattice 3-polytopes with few
lattice points, arXiv:1409.6701v3](https://arxiv.org/pdf/1409.6701),
Theorem 1.2(1), printed page 2. It states width one for size-five
polytopes of signatures (2,2), (2,1), or (3,2). A full-dimensional
five-point configuration consisting entirely of vertices can have only
(2,2) or (3,2): a side of size one in the affine dependence would
express that point as a convex combination of others. Thus the theorem
applies directly. The paper also records Howe's broader empty-polytope
result on printed page 3, but invoking that broader result is unnecessary.

This use is a consequence of an established classification; it should
not be described as a new classification theorem or priority claim.

## Directions, triangles, and exact lines

For an integer normal (a,b,c), its values on P are
(0,2a+b+c,b,c). Width one forces, after reversing sign, all values into
{0,1}. Enumeration of the four choices for (b,c) in {0,1}^2 and the
parity condition on 2a+b+c gives precisely

    (0,1,0), (0,0,1), (1,-1,-1)

modulo sign. Each direction splits the four contacts into two pairs.
Since P is contained in Q and is full-dimensional, any width-one slab
of Q restricts to exactly that same width-one slab of P. An integer z
must lie on one of its two planes.

The three coplanar points consisting of z and that plane's two contacts
are noncollinear, because all five points are vertices. Their triangle
contains no other lattice points. Pick's theorem in the induced plane
lattice makes it unimodular. If v=p_b-p_a and u is the primitive slab
normal, this is equivalent to

    v cross (z-p_a) = +u or -u.

All six contact-pair edge directions are primitive. A nonempty solution
set over Z^3 is therefore one affine integer line z=s+t v, t in Z.
Each of the six pairs contributes two parallel, distinct lines. Distinct
pairs have nonparallel edge directions, so the twelve lines are distinct.
Here is an independently computed set of representatives:

| s | v |
|---|---|
| (-1,0,0) | (0,0,1) |
| (1,0,0) | (0,0,1) |
| (1,1,0) | (-2,0,-1) |
| (-1,1,0) | (-2,0,-1) |
| (1,0,0) | (0,1,0) |
| (-1,0,0) | (0,1,0) |
| (-1,0,1) | (-2,-1,0) |
| (1,0,1) | (-2,-1,0) |
| (1,0,2) | (0,-1,1) |
| (-1,0,0) | (0,-1,1) |
| (-1,0,-1) | (2,1,1) |
| (-1,-1,0) | (2,1,1) |

The union can have intersections; twelve distinct lines does not mean
all their lattice points are distinct. No line contains a contact of P.

Conversely, every integer point z on these lines gives a polytope Q
whose two lattice-level sections are one unimodular triangle and one
primitive segment. There are no intermediate integer levels, so Q has
exactly its five vertices as lattice points. Thus these lines describe
exactly the empty five-vertex extensions of P, not merely a superset.
The necessity for detecting nonhollowness of K still comes from the
minimality argument above; it does not assert that every interior lattice
point of K lies on the lines.

## Complete test and volume truncation

The correct conclusion is

    K is hollow iff int(K) contains no integer point on the twelve lines.

This retains strict interior membership. A boundary lattice point on a
line must not be classified as evidence of nonhollowness. Compactness
alone bounds the relevant integer parameters on each line, although a
uniform precomputed finite list needs an additional quantitative bound.

If vol(K)<21, any interior witness z satisfies

    1 + sum_i max(0,-lambda_i(z)) < 63,

by the visible-pyramid volume identity and conv(P,z) contained in K.
For the fixed coordinates lambda=(1+X/2-Y-Z,X/2,Y-X/2,Z-X/2), this is
sum of negative parts less than 62. The corresponding strict coordinate
bounds give -123<=X<=125 and -61<=Y,Z<=62 for integer points. They supply
a simple finite independent enumeration bound.

A separate standard-library Fraction computation generated the twelve
cross-product lines above and applied this strict filter. It found 123
integer points on each line and 1456 distinct points in their union;
none are contacts of P. Its parameter scan from -1000 through 1000 is
complete because the displayed coordinate bounds and representatives
already force absolute parameter values below 130. Replacing the
strict filter by a weak one changes the list and should not be done
silently. This count is an independent arithmetic check, not a substitute
for the proof of the reduction.

## Saved independent replay and pair-domain profile

`python3 tests/replay_det2_observer_lines_independent.py` independently
reconstructs the fixed normals, empty contact tetrahedron, twelve affine
lines, strict volume intervals, 1456-point union, and pair-domain row
classification. It imports no generator or geometry core. The closed
row-normalized pair domain has three vertices: unit designated weight,
or half designated weight and half one of the other two weights. Direct
evaluation at these weight vectors proves 972 guard clauses tautological
and leaves 484 nontrivial clauses. This calculation is applicable to F
rows by positive row scaling; column constraints need not be used for
this safe tautology removal.

The saved independent replay passes and rejects eight corruptions of
lines, intervals, point lists, masses, classifications, counts, and
normals. The profile's possible-blocking-row test uses a closed domain;
it may conservatively retain a row whose only zero occurs at excluded
zero off-diagonal weights. That conservatism does not remove a necessary
guard or compromise completeness.

The exact line characterization above is explicitly restricted to
five-vertex extensions. General lattice observers may make an old p_i
nonvertex and are not claimed to be described by these lines. The
boundary-contact hypothesis is what excludes those configurations in
the minimal interior-witness application.

## Generalization to every nonunimodular empty contact tetrahedron

Verdict: the proposed generalization is valid. Let P be any empty lattice
3-tetrahedron with normalized volume d>1, contained in a compact convex
full-dimensional K, and require all four vertices of P to lie on bd(K).
The minimal interior-witness proof is unchanged: if K is nonhollow,
it contains an interior lattice point z for which conv(P,z) has exactly
five lattice points, all vertices, and hence width one by the same cited
theorem.

A width-one slab of P cannot split its vertices 3+1. In that case the
three coplanar vertices form an empty lattice triangle, unimodular in its
induced plane lattice. The remaining vertex has lattice height one over
that plane, so the normalized tetrahedron volume is one, contradicting
d>1. A full-dimensional tetrahedron has no 4+0 split. Thus every relevant
slab partitions P into two opposite edges, with two contacts in each
boundary plane.

There are exactly three unordered partitions of four vertices into two
pairs. For each partition the two edge directions are linearly
independent: parallel opposite edges would put all four vertices in a
single plane. Their common perpendicular therefore determines at most
one primitive integer normal modulo sign. Keep this normal only when
the two edge planes are separated by lattice distance one. Consequently
there are at most three relevant slab directions. This argument neither
assumes nor needs the separate classification of empty tetrahedra.

For each retained normal u, each of its two contact pairs (p_a,p_b), and
each sign, use

    (p_b-p_a) cross (z-p_a) = +/-u.

The edge v=p_b-p_a is primitive because P is empty. The integer plane
lattice L={w in Z^3 : u.w=0} is saturated because u is primitive. An
ambient primitive v in L is also primitive in L and extends to a basis
(v,w) of L. The cross product of such a basis is +/-u. Thus each of the
two signs has an integer solution; its full integer solution set is one
affine line with primitive direction v. This addresses the potential
Diophantine-existence gap explicitly.

The same unimodular-triangle argument gives four lines per slab, hence
at most twelve lines in total. Every minimal interior witness lies on
one of them. Conversely any interior lattice point on a listed line is
already an interior lattice point of K. Therefore testing these lines
is equivalent to hollowness under the stated contact assumptions. As
before, this does not say that every interior lattice point of K is on
a line, or that all unrestricted observers preserve the four old vertices.
Each listed line does parameterize empty five-vertex extensions of P.

If additionally vol(K)<V in ordinary Euclidean volume, the visible-pyramid
identity gives, for any relevant interior witness z,

    (d/6) (1 + sum_i max(0,-lambda_i(z))) < V,

and thus the proposed exact truncation

    sum_i max(0,-lambda_i(z)) < 6V/d - 1.

A bound on the total negative barycentric mass also bounds the positive
mass, since the four coordinates sum to one. The resulting barycentric
region is bounded; along each affine line it yields a bounded parameter
interval and finitely many integer guards. Strictness should be retained.
If the volume premise is incompatible with P being contained in K, the
statement is vacuous; it does not license using an arbitrary positive
truncation instead.

The exclusion d=1 is material: unimodular tetrahedra can have 3+1 slabs,
so this particular three-partition/twelve-line proof does not cover them.
No flaw or additional exception was identified for d>1.

## Difference-gauge truncation without a volume hypothesis

Verdict: the proposed convex-combination refinement is correct, including
the strict parameter bounds and the general upper bound of 96 guards at
beta=37/102. Here gamma always means the gauge of K-K, not the gauge of K.
The hypothesis needed for this refinement is gamma_(K-K)(v)>beta for
all six primitive contact-edge vectors (modulo sign).

Fix an observer line q_t=p_a+r+t v, v=p_b-p_a. The vectors (v,r) form
a basis of the slab-plane lattice by the unimodular-triangle equation.
The opposite edge w is in this same vector lattice. Its coefficient
at r has absolute value d, the normalized volume of P: the two contact
planes have lattice separation one, and the edge parallelogram has
normalized lattice area d. Orient w to make that coefficient positive,
so w=a v+d r with integer a.

If q_t lies in K, then r+t v, r+(t-1)v, and -w all lie in K-K, as do
+v and -v. Convexity of K-K gives, with weights d/(d+1) and 1/(d+1),

    ((d t-a)/(d+1)) v in K-K,
    ((d(t-1)-a)/(d+1)) v in K-K.

Symmetry supplies their negatives. Consequently, with

    rho_t=max(1, |d t-a|/(d+1), |d(t-1)-a|/(d+1)),

one has rho_t v in K-K, hence gamma_(K-K)(v)<=1/rho_t. The strict
hypothesis gamma_(K-K)(v)>beta therefore forces rho_t<1/beta.
For positive beta<1 this is precisely the open interval

    a/d + 1 - (d+1)/(d beta) < t < a/d + (d+1)/(d beta).

This derivation applies even when q_t is only in K, so certainly applies
to the minimal interior witness. It uses no volume bound. Values beta>=1
are incompatible with the strict edge-gauge hypothesis, since v is
already in K-K; beta>0 should be stated when using reciprocals.

For d>=2 the interval length is

    2(d+1)/(d beta)-1 <= 3/beta-1.

At beta=37/102 this is at most 269/37<8, so each line contains at most
eight retained integer parameters, and the union has at most 96 guards.
The bound counts integers in an open real interval, not rounded endpoint
inequalities; retain strict comparisons in implementation.

For the fixed determinant-two contacts an independent Fraction-only
calculation using the cross-product equations and opposite-edge
coordinates found seven retained parameters on every line, 64 distinct
points in their union, 44 pair-domain tautologies, and 20 remaining
clauses. The remaining points are

    (-5,-2,1), (-5,1,-2), (-3,-1,1), (-3,1,-1),
    (-1,0,1), (-1,0,2), (-1,0,3),
    (-1,1,0), (-1,2,0), (-1,3,0),
    (1,-2,0), (1,-1,0), (1,0,-2), (1,0,-1), (1,0,0),
    (3,1,1), (5,1,2), (5,2,1), (7,1,3), (7,3,1).

The six required edge directions modulo sign can be chosen as

    (0,1,0), (0,0,1), (2,1,1),
    (2,0,1), (2,1,0), (0,1,-1).

The previously used three coordinate-axis gauge cuts do not supply all
six edge hypotheses. Before replacing the larger guard set by these
20 pair clauses in a relaxation, explicitly include the six edge-gauge
lower bounds or otherwise prove they follow from its asserted conditions.
For a genuinely hollow high-width target the known difference-minimum
bound supplies them, but that fact alone does not allow an arbitrary
partial relaxation assignment to be treated as satisfying those bounds.
With these hypotheses asserted, the 20 exclusions are a complete
hollowness test in the pair domain, rather than another partial-box test.

The gauge refinement now has a durable independent replay:
[replay_det2_gauge_guards_independent.py](../tests/replay_det2_gauge_guards_independent.py),
checking the archived [gauge guard certificate](../certificates/det2_observer_gauge_guards.json)
associated with [the gauge proof](DET2_OBSERVER_GAUGE_GUARDS.md).
Run `python3 tests/replay_det2_gauge_guards_independent.py` from the lab.
It imports neither generators, geometry core, nor other replay scripts.
It reconstructs the line union from separate representatives, solves the
opposite-edge coordinates by two-coordinate Cramer's rule, checks all
archived r,w,a,d data, verifies both convex cancellations as vector
equalities, and checks strict intervals, all 64 points, all 20 retained
pair clauses, and all six contact-edge directions. Ten corruptions are
rejected, including sign changes, missing edge hypotheses, missing guards,
and changed interval bounds. An additional beta=3/5 boundary regression
has open integer endpoints (-1,3), and verifies that only t=0,1,2 survive;
this detects accidental replacement of strict inequalities by weak ones.
The replay passes with standard-library Fraction arithmetic.
