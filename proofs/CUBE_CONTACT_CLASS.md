# The eight-facet cube-contact class: exact reduction and the remaining gap

Date: 2026-09-13.  This note records an exact reduction for the continuous
class requested in the cube-contact campaign.  It does not claim a proof of
the conjectural width-≤3 bound.  The numerical file
[`experiments/cube_contact_class.py`](../experiments/cube_contact_class.py)
is an exploratory audit only.

## Model and automatic hollowness

Work first in the uncentered lattice — the cube is

\[
 C=[0,1]^3\subset\mathbb R^3.
\]

For a corner \(c\in\{0,1\}^3\), let
\(\varepsilon_i=2c_i-1\).  A facet through \(c\) with the prescribed
strict orthant sign has, after positive scaling, the inequality

\[
 \sum_{i=1}^3 \varepsilon_i a_{c,i}(x_i-c_i)\leq 0,
 \qquad a_{c,i}>0,
 \qquad \sum_i a_{c,i}=1. \tag{1}
\]

Equivalently, after translating by \((-1/2,-1/2,-1/2)\), its outward normal
is

\[
 n_s=(s_1a_{s,1},s_2a_{s,2},s_3a_{s,3}),
 \quad a_{s,i}>0,
 \quad \|n_s\|_1=1,
\]

and the support value is \(1/2\).  The ambient lattice in centered
coordinates is \((\mathbb Z+1/2)^3\); width functionals remain the integer
vectors \(u\in\mathbb Z^3\).

The intersection of the eight halfspaces (1) contains \(C\).  It is
automatically hollow.  Indeed, for an integer point \(z\), choose the cube
corner \(c\) coordinatewise by \(c_i=0\) when \(z_i\leq0\) and \(c_i=1\)
when \(z_i\geq1\).  Each term
\(\varepsilon_i(z_i-c_i)\) is nonnegative, and if \(z\) is not a cube
corner at least one is positive.  The left side of (1) is then strictly
positive, so \(z\) is outside that facet halfspace.  A cube corner itself
lies on its assigned facet and is allowed on the boundary.

The body is bounded for every strictly positive choice of the weights.  If a
nonzero recession vector \(v\) existed, choose the sign corner
\(s_i=\operatorname{sign}(v_i)\), with an arbitrary sign when \(v_i=0\).
Then \(n_s\cdot v=\sum_i a_{s,i}|v_i|>0\), contradicting all eight
recession inequalities.  The assigned corner is strictly below the other
seven facet planes, so each of the eight planes is a genuine facet.

## Complete finite direction set below width four

For every integer direction \(u\), containment of the unit cube gives

\[
 \operatorname{width}(K,u)\geq
 \operatorname{width}(C,u)=|u_1|+|u_2|+|u_3|. \tag{2}
\]

Lattice width only needs primitive directions, and \(u\) and \(-u\) give
the same width.  Therefore, if \(w_{\mathbb Z^3}(K)<4\), every minimizing
direction belongs, modulo sign, to the following 25-element set:

\[
\begin{array}{c|c}
\|u\|_1 & \text{primitive representatives modulo sign}\\ \hline
1 & (1,0,0)\text{ and permutations}\\
2 & (1,\pm1,0)\text{ and permutations}\\
3 & (1,\pm1,\pm1),\quad (2,\pm1,0)\text{ and permutations}.
\end{array} \tag{3}
\]

The counts are \(3+6+4+12=25\).  This is a complete direction list under
the explicit width-\(<4\) hypothesis; it is not an empirical cutoff.  In
particular, any global width bound below four can be checked against (3),
but checking (3) numerically for selected weights does not prove a uniform
bound.

## The cube-cover obstruction

The same clamping argument gives a geometric cover that is useful but does
not currently close the problem.  In centered coordinates put

\[
 P_i=\{x:-1/2\leq x_i\leq1/2\},
 \qquad i=1,2,3.
\]

Every point outside all three planks has all three coordinates outside the
centered unit interval.  The facet indexed by its coordinate-sign corner
then has strictly positive left side, so

\[
 K\subseteq P_1\cup P_2\cup P_3. \tag{4}
\]

Let \(m_i=\min_Kx_i\), \(M_i=\max_Kx_i\), and
\(W_i=M_i-m_i=\operatorname{width}(K,e_i)\).  The diagonal map

\[
 T(x)_i=\frac{x_i-m_i}{W_i}
\]

maps \(K\) to a convex set \(S\subseteq[0,1]^3\) touching all six facets
of the unit cube.  The three planks in (4) become coordinate planks in
\([0,1]^3\) of widths \(1/W_1,1/W_2,1/W_3\), and they cover \(S\).  Thus

\[
 \frac1{W_1}+\frac1{W_2}+\frac1{W_3}\geq1 
 \quad\Longrightarrow\quad \min_i W_i\leq3. \tag{5}
\]

The implication in (5) is exactly the desired axis-direction conclusion.
However, the displayed inequality is the three-plank form of Bang's
affine/relative plank conjecture for a packed convex set in a cube.  That
conjecture is open for nonsymmetric three-dimensional bodies.  Ball's plank
theorem proves it when the covered body is centrally symmetric, but the
independent weights \(a_{s,i}\) do not make the present intersection
centrally symmetric.  Consequently (4) cannot be upgraded to (5) by citing
the general relative plank theorem.

This is a genuine scope obstruction to the shortest proposed proof.  The
extra information in this class is that the eight cube corners are exposed
by strict-sign facets.  It may be enough to settle this special packed-set
subclass, but that implication is not supplied by the currently known plank
results.  A proof that only invokes (4) and a general relative-plank claim
would therefore be circular or would silently assume an open conjecture.

## Exact local derivative structure for a future elimination

For numerical guidance, let \(N_s=n_s^T\) and write a vertex formed by the
three active facets \(I=\{s,t,r\}\) as

\[
 v_I=\frac12N_I^{-1}{\bf1}. \tag{6}
\]

On a fixed feasible-combinatorial chamber, a support value in direction \(u
\) is \(u\cdot v_I\).  For a perturbation \(\dot N_I\) of the active rows,

\[
 \dot v_I=-N_I^{-1}\dot N_Iv_I,
 \qquad
 \frac{d}{dt}(u\cdot v_I)
 =-u^TN_I^{-1}\dot N_Iv_I. \tag{7}
\]

The derivative of a width is the difference of (7) at its active maximizer
and minimizer.  At a tie, the correct object is the convex hull of these
one-sided derivatives.  A convenient unconstrained parameter is a rowwise
softmax \(a_{s,i}=e^{y_{s,i}}/\sum_j e^{y_{s,j}}\); then

\[
 \dot a_{s,i}=a_{s,i}\left(\dot y_{s,i}
 -\sum_j a_{s,j}\dot y_{s,j}\right),
\]

and \(\dot N_{s,i}=s_i\dot a_{s,i}\).  These formulas give an exact
piecewise-rational route for a chamber-by-chamber proof or for an interval
certificate.  They also show why an optimizer based on one fixed active
vertex pattern cannot certify the full class: active triples and minimizing
directions change on chamber walls.

At the symmetric point \(a_{s,i}=1/3\),

\[
 K=\{x:\|x\|_1\leq3/2\},
 \qquad
 \operatorname{width}(K,u)=3\|u\|_\infty. 
\]

Hence the minimum over (3) is exactly three, witnessed by every primitive
direction with \(\|u\|_\infty=1\).  The bounded numerical search found no
sample with a value above three; this is evidence around the symmetric
equality point only, not a proof.  Its output and all limitations are in
[`results/cube_contact_class.json`](../results/cube_contact_class.json).

## Bounded conclusion

The class is exactly parameterized by 24 positive weight entries subject to
eight row-sum equations (hence 16 free parameters), is always bounded and
hollow, and has the complete 25-direction test (3) whenever its lattice
width is below four.  The natural axis-width
argument reduces to an open three-plank relative-width problem, so no
unconditional width-\(\leq3\) theorem was obtained here and no numerical
search is promoted to one.  The derivative formula (7), the strict-sign
cover (4), and the symmetric equality model are the concrete inputs for a
future special-case proof.

## A sharper necessary condition from inscribed-parallelotope theory

The axis-width inequality is also Conjecture 1 of
[Lassak (2001), *Relationships between widths of a convex body and of an
inscribed parallelotope*](https://doi.org/10.1017/S0004972700019195).
His Theorem 1 proves the weaker, unconditional inequality

    1/W_j + 1/W_k + 1/a_i >= 1,   {i,j,k}={1,2,3},

where a_i is the longest segment in K parallel to e_i. The cube-contact
class satisfies the inscribed-parallelotope hypothesis. This is a known
theorem, not a new bound proved by the lab.

Combining it with W_j,W_k >= w=w_Z3(K)>2 yields the necessary conditions

    a_i <= w/(w-2),       W_i/a_i >= w-2,   for every i.

In particular, a putative cube-contact body with w>=2+sqrt(2) must satisfy

    a_i <= 1+sqrt(2),     W_i/a_i >= sqrt(2),   for all three axes.

Thus its projection widths would exceed its longest parallel chords by a
substantial factor along every axis. This supplies a concrete filter for
future chamber analysis. It does not eliminate the class: neither existence
nor impossibility of such bodies is inferred from these necessary conditions.
The 2026 general plank status alone does not establish the current separate
status of Lassak's more specialized conjecture.

## References for the obstruction

The packed-convex-set formulation and its status are stated in Aharoni,
Holzman, Krivelevich and Meshulam, *Fractional Planks*, Discrete &
Computational Geometry 27 (2002), 585–602,
[doi:10.1007/s00454-001-0088-x](https://doi.org/10.1007/s00454-001-0088-x).
Their introduction defines a packed convex set in the unit cube and records
the plank conjecture, with the centrally symmetric case as the relevant
known special case.  The current general status and the best unconditional
bound (2/(1+\sqrt d)) are summarized by Bakaev–Yehudayoff, *A note on the
affine plank conjecture*, [arXiv:2602.20290](https://arxiv.org/abs/2602.20290).
