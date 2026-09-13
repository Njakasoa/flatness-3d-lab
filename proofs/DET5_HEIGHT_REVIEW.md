# Independent review of determinant-five height charts

Date: 2026-09-14. Scope: the two full tetrahedral facet-contact classes
4 and 5, before any new solver result. This review independently recomputes
the affine lattice groups and their action on normalized heights. It does
not certify a new exclusion or a solver cover.

Write

\[
P_a=\operatorname{conv}(p_0,p_1,p_2,p_3),\qquad
(p_0,p_1,p_2,p_3)=(0,(5,1,a),e_2,e_3),\quad a\in\{1,2\}.
\]

The chosen covector is always \(Y=(0,1,0)\), with contact values
\(H=(0,1,1,0)\). The scan certificate chooses Z for class 4, but its
listed gauge vectors and barycentric coordinates remain valid when the
height model uses Y.

## Affine groups and the necessary subgroup restriction

For each of the 24 permutations \(\pi\), the unique affine map is
\(x\mapsto Ux+t\), where

\[
t=p_{\pi(0)},\qquad
U=[p_{\pi(1)}-t\;p_{\pi(2)}-t\;p_{\pi(3)}-t]
  [p_1\;p_2\;p_3]^{-1}.
\]

Exact Fraction Gaussian elimination, independent of the chart generator,
tests that every entry is integral. Since the map permutes a nondegenerate
simplex, its determinant is automatically \(\pm1\). This is an exhaustive
enumeration, not a bounded search over matrix coefficients.

A permutation is written as the tuple of images of 0,1,2,3. For class 4,
the full group consists of

```
0123, 0132, 1023, 1032, 2301, 2310, 3201, 3210.
```

Only four preserve the chosen Y up to sign and integer translation:

| Permutation | Rows of U | Translation t | Height sign |
| --- | --- | --- | --- |
| 0123 | (1,0,0); (0,1,0); (0,0,1) | (0,0,0) | +1 |
| 1032 | (1,-5,-5); (0,-1,0); (0,0,-1) | (5,1,1) | -1 |
| 2301 | (-1,0,5); (0,-1,0); (0,0,1) | (0,1,0) | -1 |
| 3210 | (-1,5,0); (0,1,0); (0,0,-1) | (0,0,1) | +1 |

The other four interchange the Y and Z directions, up to sign. For example,
0132 simply swaps the last two coordinates. They cannot be used as
symmetries of a model which has chosen only Y as its height covector.
The old `symmetries` function assumes all contact automorphisms preserve
the chosen covector and raises on these maps. Its correct generic behavior
for this transfer is to retain the preserving subgroup.

For class 5 the full group already preserves Y and consists of:

| Permutation | Rows of U | Translation t | Height sign |
| --- | --- | --- | --- |
| 0123 | (1,0,0); (0,1,0); (0,0,1) | (0,0,0) | +1 |
| 1302 | (2,-5,-5); (0,-1,0); (1,-2,-2) | (5,1,2) | -1 |
| 2031 | (-2,0,5); (0,-1,0); (-1,1,2) | (0,1,0) | -1 |
| 3210 | (-1,5,0); (0,1,0); (0,1,-1) | (0,0,1) | +1 |

The complete width-one covector sets, up to sign, are \(\{Y,Z\}\) for
class 4 and \(\{Y\}\) for class 5. Completeness follows by assigning
binary heights to the three nonzero vertices and solving the resulting
three equations: after changing sign, the zero vertex has height zero.
No uniqueness of Y is needed once the subgroup is selected explicitly.

## Ordered extrema orbits

If \((l,h)\) are vertex indices attaining the minimum and maximum Y
heights, an affine symmetry with height sign \(\sigma\) acts by

\[
(l,h)\longmapsto
\begin{cases}
(\pi(l),\pi(h)),&\sigma=+1,\\
(\pi(h),\pi(l)),&\sigma=-1.
\end{cases}
\]

Indeed, relabeling contacts also relabels their opposite vertices, while
a negative height sign changes normalized height q into 1-q. Ties are
allowed; any distinct pair of attaining indices belongs to this list.

Class 4 has five orbits:

```
[(0,1),(3,2)]
[(0,2),(3,1)]
[(0,3),(1,2),(2,1),(3,0)]
[(1,0),(2,3)]
[(1,3),(2,0)]
```

Class 5 has three orbits:

```
[(0,1),(0,2),(3,1),(3,2)]
[(0,3),(1,2),(2,1),(3,0)]
[(1,0),(1,3),(2,0),(2,3)]
```

Each list partitions all 12 ordered distinct pairs. Its first pair in
each row is a valid representative chart. Exact direct substitution also
confirms that the existing finite guard sets and the union of primitive
edge directions with listed eligible gauge vectors are invariant under
their respective four-element subgroups (gauge vectors taken up to sign).

## Necessary inequalities and guard coverage

For a hollow full-dimensional tetrahedron with \(w(K)>17/5\), the ACMS
inequality used by the existing lab gives

\[
\lambda_1(K-K)\ge 1-\frac{A}{w(K)}
>1-\frac{13/6}{17/5}=\frac{37}{102}=\beta,
\qquad A=1+2/\sqrt3<13/6.
\]

Thus every nonzero lattice vector used by the model has gauge strictly
greater than beta. This deduction uses full lattice width, not merely
large width in Y. The constant inequality is exact: \(12<7\sqrt3\)
follows from \(144<147\).

The independent stdlib verifier
[`replay_nonunimodular_guards_independent.py`](../tests/replay_nonunimodular_guards_independent.py)
was run through its `verify` function against the current certificate. It
passed the exact emptiness, width-one slab coverage, primitive edge,
plane-basis, strict cutoff and complete integer-interval checks for all
nine classes. In particular:

| Class | Slab directions | Observer lines | Guards | Edge gauges used for truncation |
| --- | --- | --- | --- | --- |
| 4 | Y, Z | 8 | 40 | (0,0,1), (0,1,0), (5,0,1), (5,1,0) |
| 5 | Y | 4 | 20 | (0,0,1), (5,0,2) |

All these edge directions occur in the six primitive contact edges imposed
by the model. The observer theorem and its finite truncation therefore
apply with their existing boundary-contact hypotheses. The exact model
has diagonal entries zero and off-diagonal entries strictly positive,
as required for one contact in the relative interior of each distinct
tetrahedron facet.

## Rank caveat: necessity suffices for the interval exclusion

The d7/d8 three-vector rank lemma must not be transferred automatically.
For its fixed triple \((1,0,0),(3,0,1),(2,0,1)\), the contact gauge masses
are respectively

\[
(2/5,1,1)\quad\text{for class 4},\qquad
(3/5,4/5,3/5)\quad\text{for class 5}.
\]

In both cases their maximum is larger than \(2\beta=37/51\), so the
positive rank margin in that lemma is absent. Class 4's last two vectors
are not among the existing eligible short vectors or the primitive edges,
either. The old optional volume-lift helper, which checks the same rank
margin, is inapplicable. This observation does not prove singular
assignments exist; it means the prior proof of their exclusion supplies
no certificate here.

For the proposed UNSAT campaign, no rank sufficiency theorem is needed.
Given an actual candidate tetrahedron K, its barycentric contact matrix F
is invertible by construction. If \(L=\min Y(K)\), \(U=\max Y(K)\), set

\[
q_i=\frac{Y(v_i)-L}{U-L},\quad
a=-\frac{L}{U-L},\quad b=\frac1{U-L}.
\]

Containment of the contacts implies \(L\le0\), \(U\ge1\), hence
\(0\le a\), \(a+b\le1\). Full width above 17/5 implies
\(0<b<5/17\). The exact identities are \(F^Tq=a\mathbf1+bH\), with
the chosen extrema normalized to zero and one. These facts place every
actual high-width candidate inside one of the eight representative
necessary models, independently of whether those models admit extra
singular assignments.

On a rectangle \(l\le q\le h\), \(0\le f\le1\), the four inequalities

\[
p\ge lf,\quad p\le hf,\quad
p\ge q+hf-h,\quad p\le q+lf-l
\]

hold for the actual product \(p=qf\). Replacing products by these variables
therefore enlarges the feasible set. UNSAT on every leaf of a complete
closed rectangle cover would exclude the associated high-width
tetrahedra. SAT of a rectangle relaxation does not exhibit a tetrahedron,
and incomplete covers do not establish a class exclusion.

## Initial campaign encoding audit

After the geometry review, the initial campaign archive became available.
The independent read-only checker
[`audit_det5_height_independent.py`](../tests/audit_det5_height_independent.py)
passed all 98 archived assertion sets. It independently recomputes the
affine groups and subgroups above, replays the generic guard certificate,
and verifies the exact complete or partial breadth-first dyadic frontier.
It reuses the earlier independent audit's formula reconstruction and exact
linear normalization, importing no discovery generator or geometry engine.

Its report is
[`det5_height_encoding_validation.json`](../results/det5_height_encoding_validation.json).
Class 4 has five complete charts, each with its single full-square root
labeled UNSAT. Class 5 has three partial charts with 72 pending leaves;
these do not constitute an exclusion. All eight deliberately corrupted
inputs were rejected, including a deleted gauge, an extra contradictory
assertion, an incorrect height reversal, an omitted chart orbit and a
false completeness flag on a partial chart.

The review and audit issued no solver query. The audit verifies encodings
and coverage, not the truth of UNSAT labels; independent proof checking
must supply that additional evidence. No additional rank theorem or
global flatness improvement is claimed here.

## Stronger gauge and simultaneous-direction transfer

The later construction
[`det5_joint_height_interval.py`](../experiments/det5_joint_height_interval.py)
was read together with its stronger-gauge Y constructor. This section
reviews the geometric necessity of those models, not any solver outcome.

The rational strengthening \(\beta'=183/500\) is valid for every
hypothetical hollow body of full lattice width above 17/5. Indeed,

\[
\frac{17}{5}(1-\beta')=\frac{5389}{2500}>A,
\]

where the radical comparison reduces to
\(4\cdot2500^2=25000000<3\cdot2889^2=25038963\).
Consequently ACMS yields \(\lambda_1(K-K)>\beta'\). Adding these stronger
gauge inequalities while retaining the old beta inequalities and guards
preserves necessity. The old finite guards remain applicable, since
\(\beta'>37/102\).

For class 5, the exact witness archived in
[`det5_strong_fiber.json`](../results/det5_strong_fiber.json) prevents a
Y-only exclusion under these conditions. Independent Fraction arithmetic
confirmed column stochasticity, the zero-diagonal/positive-off-diagonal
facet-contact pattern, invertibility by Gaussian elimination, and the
normalized Y identities. Reconstructing the vertices as \(P F^{-1}\)
and exhaustively checking their strict coordinate bounding box found no
interior lattice point. The global first minimum is

\[
\lambda_1(K-K)=\frac{14828737}{40315500},
\]

attained at \(\pm(2,0,1)\). This is a global minimum check: using that
attained value \(c\), every vector of gauge at most c lies in the integer
coordinate box \([-2,2]\times[-1,1]\times[-1,1]\), as follows from the
exact coordinate widths of \(c(K-K)\); all nonzero points in that box
were checked. The value exceeds even \(1-A/(17/5)\), by an exact rational
square comparison. Nevertheless the witness has

\[
w_Y(K)=\frac{1290096000}{376157033}>17/5,
\qquad
w_U(K)=\frac{431770127526900}{160704333264053}<17/5,
\quad U=(1,-1,-2).
\]

Thus it disproves the proposed Y-direction conclusion even with the exact
ACMS first-minimum threshold as hypothesis. It supplies no high global
width counterexample, since its U-width is about 2.686736.

The simultaneous model chooses the fixed primitive lattice covector U
alongside Y. Its unshifted contact values are \((0,0,-1,-2)\), hence the
shifted values \(H_U=(2,2,1,0)\) used in the code are correct. If
\(L_U=\min U(K)\), \(R_U=w_U(K)\), define

\[
r_i=\frac{U(v_i)-L_U}{R_U},\qquad
b_U=\frac1{R_U},\qquad
a_U=\frac{-2-L_U}{R_U}.
\]

Containment gives \(a_U\ge0\), \(a_U+2b_U\le1\), while full width above
17/5 gives \(0<b_U<5/17\). The column identities are exactly
\(F^T r=a_U\mathbf1+b_U H_U\). The code includes the factor 2 in the
upper offset bound, uses all 12 ordered U-extrema choices, and applies the
same valid McCormick envelopes to its two remaining free heights. The
four free heights are therefore covered by closed boxes in \([0,1]^4\).

Using only three Y-extrema representatives remains valid for this
**global-width necessity** argument even when the symmetry does not
preserve U. Given any hypothetical high-global-width K, choose a
Y-preserving contact automorphism g that puts its Y-extrema in one of the
three representatives. The transformed body gK remains hollow and has
the same full lattice width, because g is affine unimodular. In
particular the fixed covector U has width above 17/5 on gK, regardless
of the direction to which g sent U on the original body. Its U-extrema
then belong to one of the 12 retained pairs.

This reasoning is not a symmetry equivalence claim for arbitrary bodies
satisfying only the two selected directional inequalities. Such a body
could lose the U inequality after transformation. The reduction is
justified because every lattice direction is wide in the hypothetical
global counterexample. A complete exclusion would require all 36 charts
to have independently audited complete covers and certified UNSAT leaves.
No additional solver calls or complete-cover claims were made in this
review.
