# Reconstructing the ACMS local maximum theorem

This note follows Sections 1–4 of Averkov, Codenotti, Macchia and Santos,
*A local maximizer for lattice width of 3-dimensional hollow bodies*,
arXiv:1907.06199v2. The source is [the arXiv paper](https://arxiv.org/abs/1907.06199),
with primary links in [papers/README.md](../papers/README.md).

## Statement and normalization

Let `r = sqrt(2)` and let `Delta = conv(a_1,a_2,a_3,a_4)`, where

$$
\begin{aligned}
a_1&=(2+r,r,2+r),\\
a_2&=(-r,2+r,-2-r),\\
a_3&=(-2-r,-r,2+r),\\
a_4&=(r,-2-r,-2-r).
\end{aligned}\tag{1}
$$

The affine lattice is

$$
\Lambda=\{(a,b,c):a,b,c\in1+2\mathbb Z,\ a+b+c\in1+4\mathbb Z\}.
$$

The four facet contacts are

$$
p_1=(-1,-1,-1),\quad p_2=(1,-1,1),\quad
p_3=(1,1,-1),\quad p_4=(-1,1,1).
$$

The seven displayed dual lattice functionals are

$$
\frac14(1,1,1),\ \frac14(-1,1,1),\ \frac14(1,1,-1),\ \frac14(1,-1,1),
\quad \frac12e_1,\ \frac12e_2,\ \frac12e_3,
\tag{2}
$$

and each has width `2+sqrt(2)` on `Delta`. The four `p_i` form an affine
lattice basis for `Lambda`.

Theorem 1.2 of the paper says that `Delta` is a strict local maximizer among
hollow tetrahedra: every sufficiently small tetrahedral perturbation is either
non-hollow or has lattice width strictly below `2+sqrt(2)`. Corollary 1.3
extends the conclusion to hollow convex bodies contained in a sufficiently
small open neighborhood of `Delta`.

The proof is local and is not a global classification of hollow bodies.

## Perturbing the lattice while fixing `Delta`

Fix the vertex coordinates of `Delta` and vary the affine lattice. Write

$$
\begin{array}{ll}
p_1(t)=(-1,-1,-1)+(t_{11},t_{12},t_{13}),&
p_2(t)=(1,-1,1)+(t_{21},t_{22},t_{23}),\\
p_3(t)=(1,1,-1)+(t_{31},t_{32},t_{33}),&
p_4(t)=(-1,1,1)+(t_{41},t_{42},t_{43}).
\end{array}
$$

Each perturbed contact is constrained to its corresponding facet. The four
coplanarity conditions express the third coordinates as

$$
\begin{aligned}
t_{13}&=-\frac{(2+r)t_{11}+rt_{12}}2,&
t_{23}&=\frac{-rt_{21}+(2+r)t_{22}}2,\\
t_{33}&=\frac{(2+r)t_{31}+rt_{32}}2,&
t_{43}&=\frac{rt_{41}-(2+r)t_{42}}2.
\end{aligned}
$$

The first equation is written with the outer minus sign and parentheses made
explicit. This is the line-broken form used in the paper; distributing the
minus gives the equivalent expression used by the exact replay script.

Thus the local chart has eight variables

$$
t=(t_{11},t_{12},t_{21},t_{22},t_{31},t_{32},t_{41},t_{42}).
$$

With rows

$$
M(t)=\begin{bmatrix}
p_4(t)-p_1(t)\\p_2(t)-p_1(t)\\p_3(t)-p_1(t)
\end{bmatrix},
$$

the perturbed linear lattice is `Z^3 M(t)` and its dual is
`M(t)^(-1) Z^3`. In the lattice basis used by the paper, the seven integer
vectors in (2) become

$$
u_1=(1,1,1),\ u_2=(1,0,0),\ u_3=(0,0,1),\ u_4=(0,1,0),\
u_5=(0,1,1),\ u_6=(1,0,1),\ u_7=(1,1,0).
\tag{3}
$$

At `t=0`, the first six dual functionals have unique maximizing and minimizing
vertices. By continuity, this remains true in a neighborhood. If

$$
\begin{aligned}
v_1&=a_1-a_4,&v_2&=a_3-a_4,&v_3&=a_2-a_3,\\
v_4&=a_1-a_2,&v_5&=a_1-a_3,&v_6&=a_2-a_4,
\end{aligned}
$$

then the six corresponding widths are

$$
f_i(t)=\operatorname{width}(\Delta,M(t)^{-1}u_i)
      =v_iM(t)^{-1}u_i,\qquad 1\le i\le6.
$$

The seventh functional is omitted because at `t=0` it has two maximizing and
two minimizing vertices. This omission is logically safe: lattice width is at
most the width in each one of the six retained lattice directions, so proving
that one retained direction drops below the target proves that lattice width
drops.

Theorem 2.1 is the precise local algebraic target:

> The system `f_i(t) >= 2+sqrt(2)`, `i=1,...,6`, has the isolated solution
> `t=0`.

## Polynomial/KKT argument

Since `det M(0)=16>0`, shrink the neighborhood so that `det M(t)>0`. Define

$$
h_i(t)=\det M(t)\bigl(f_i(t)-(2+\sqrt2)\bigr)
      =v_iM(t)^{\#}u_i-(2+\sqrt2)\det M(t),
$$

where `M# = det(M) M^(-1)` is the adjugate. Each `h_i` is a polynomial of
degree at most three, and locally `f_i >= 2+sqrt(2)` is equivalent to
`h_i >= 0`.

The exact gradients at the origin, in the displayed order of the eight
coordinates, are

$$
\begin{aligned}
\nabla h_1(0)&=4(-1,1,-1,-2,0,0,-2,1)
 +2r(-2,0,1,-1,0,0,-3,1),\\
\nabla h_2(0)&=4(-2,1,0,0,1,2,1,1)
 +2r(-1,-1,0,0,1,3,0,2),\\
\nabla h_3(0)&=4(0,0,2,-1,1,-1,1,2)
 +2r(0,0,3,-1,2,0,-1,1),\\
\nabla h_4(0)&=4(-1,-2,-1,-1,2,-1,0,0)
 +2r(-1,-3,0,-2,1,1,0,0),\\
\nabla h_5(0)&=8(1,0,-1,0,-1,0,1,0)
 +8r(1,0,0,0,-1,0,0,0),\\
\nabla h_6(0)&=8(0,1,0,1,0,-1,0,-1)
 +8r(0,0,0,1,0,0,0,-1).
\end{aligned}\tag{4}
$$

They have rank five and the positive dependence is

$$
\nabla h_1(0)+\nabla h_2(0)+\nabla h_3(0)+\nabla h_4(0)
 +r\bigl(\nabla h_5(0)+\nabla h_6(0)\bigr)=0.
$$

Set `lambda=(1,1,1,1,r,r)` and decompose

$$
\lambda_i h_i(t)=l_i(t)+q_i(t)+r_i(t)
$$

into homogeneous degrees one, two and three. For a constant `c>0`, define

$$
H(t)=\sum_{i=1}^6(c-l_i(t))\lambda_i h_i(t).
$$

The positive dependence gives `H(0)=0` and `grad H(0)=0`. Its degree-two part
is

$$
c\sum_iq_i-\sum_i l_i^2.
$$

At `c=0`, the latter is negative semidefinite, with nullspace

$$
V=\{v\in\mathbb R^8:\nabla h_i(0)\cdot v=0,\ i=1,\ldots,6\}.
$$

The paper's exact Sage computation gives `dim(V)=3` and the parametrization

$$
\begin{aligned}
v(w_1,w_2,w_3)=&\left(1,0,0,0,\frac r2,\frac r2,-\frac r2,\frac{r-2}2\right)w_1\\
&+\left(0,1,0,-r,\frac{2-r}2,\frac{2-r}2,\frac r2,\frac{2-3r}2\right)w_2\\
&+\left(0,0,1,-1,1-r,1,0,-r\right)w_3.
\end{aligned}
$$

In these coordinates the Hessian of `sum_i q_i` restricted to `V` is

$$
Q_V=\begin{bmatrix}
-19r/2-13&-5r/2-4&-r-2\\
-5r/2-4&-39r/2-27&-16r-22\\
-r-2&-16r-22&-19r-26
\end{bmatrix},
$$

which is negative definite. Therefore the Hessian of `H(0)` is negative
definite for every sufficiently small positive `c`: the `-sum l_i^2` term is
strictly negative off `V`, and the `c sum q_i` term is strictly negative on
`V`.

The direct SymPy calculation in
`experiments/replay_local_hessian.py` uses the ordinary Hessian convention
(second derivatives, with no extra `1/2`) and obtains `16 Q_V` for the matrix
of `sum_i lambda_i h_i` restricted to the displayed basis. Thus the paper's
displayed matrix and the direct chart calculation differ by the positive
normalization factor `16`; this leaves the Sylvester sign test unchanged. The
same replay checks the full auxiliary Hessian of `H` at `c=1/100` directly and
through the product-rule formula.

Choose such a `c`. Since `H` has a strict local maximum of zero, `H(t)<0`
for all nonzero sufficiently small `t`. Shrink once more so that every
`c-l_i(t)>0`. If all six `lambda_i h_i(t)` were nonnegative, then every term
of `H(t)` would be nonnegative, contradicting `H(t)<0`. Hence some `h_i(t)<0`
and therefore some `f_i(t)<2+sqrt(2)`. This proves Theorem 2.1 and Theorem
1.2.

The qualitative negative-definiteness step is now replayed exactly in the
SymPy certificate script: it
checks the restricted matrix up to the positive factor `16` and checks the
full auxiliary Hessian at `c=1/100`. The paper does not print a rational `c`
or a radius for Theorem 1.2; the explicit radius calculation belongs to
Section 4 and remains a separate degree-16 coefficient-majorant computation.

## Explicit neighborhood and metric conversion

For an explicit neighborhood, the paper imposes four families of strict
conditions in the `t` chart:

1. `det M(t)>0`;
2. `l_i(t)<c` for all six `i`;
3. `(v_i-v) M(t)# u_i>0` for every `i` and every other vertex `v` of
   `Delta-Delta` (66 quadratic inequalities in total);
4. `grad^2 H(t)` is negative definite.

Condition 3 guarantees that `v_i` remains the active difference-body vertex,
so the formula for `f_i` still gives the actual width in that dual direction.
The other conditions provide the sign and strict-Hessian neighborhoods used in
the preceding argument.

The paper changes to eight symmetric facet coordinates
`s=(s_1^(h),s_1^(v),...,s_4^(h),s_4^(v))`. On the facet containing `p_1`, if
`(b_2,b_3,b_4)` are barycentric coordinates relative to `(a_2,a_3,a_4)`,

$$
s_1^{(v)}=b_3=\frac12+\frac{t_{13}}{4+2r},
\qquad s_1^{(h)}=b_4-b_2. \tag{5}
$$

The other facets are obtained by the fourfold rotary reflection symmetry. A
change of barycentric coordinates by at most `epsilon` changes every `s`
coordinate by at most `2 epsilon`.

The four reported `L_infinity` bounds are:

$$
\begin{array}{c|c}
\text{condition}&\text{reported radius in the s chart}\\
\hline
(i)&(\sqrt2-1)/4\approx0.1036\\
(ii),\ c=9.75&0.02614\\
(iii)&0.04423\\
(iv),\ c=9.75&0.02646
\end{array}
$$

The linear radius in (ii) has the exact expression

$$
\rho_{\rm lin}=\frac{9.75}{192+128\sqrt2}
=0.0261380552144476\ldots,
$$

because the largest coefficient `L_1` norm of the six linear forms is
`192+128 sqrt(2)`. Conditions (iii) and (iv) are certified in the paper by
the coefficient-majorant Proposition 4.7, applied to 66 quadratic polynomials
and one degree-16 determinant polynomial, respectively. The computation was
reported as exact Sage arithmetic and took about 14 hours.

Taking the intersection yields the published statement:

> Theorem 4.3. `width_{Lambda(0)}(Delta) > width_{Lambda(s)}(Delta)` for
> `s != 0` and `||s||_infinity < 0.02614`.

Theorem 1.4 translates this to the published barycentric statement:

> If `dist_Delta(p_i,p_i') <= 0.01307` for all four contacts, then
> `width_{Lambda'}(Delta) <= width_Lambda(Delta)`, with equality only when all
> four contacts are unchanged.

### Decimal-boundary limitation

The displayed local radii are rounded decimal reports, while the proof uses
strict inequalities. In particular, the exact elementary linear radius above
is `0.0261380552...`, which is *below* the printed `0.02614`; likewise
`2*0.01307=0.02614` is slightly above the exact half-radius. A mechanically
rigorous replay should use the exact expression (and the unrounded Sage
bounds for (iii)–(iv)), or a downward-rounded safe radius such as
`||s||_infinity < 0.02613` and `dist_Delta < 0.013065`. The paper's published
`<=0.01307` should be quoted as its theorem statement, but not treated as an
independently certified closed-ball endpoint without recovering the original
unrounded computation.

## Extension from tetrahedra to convex bodies

Corollary 1.3 chooses `U=int((1+epsilon)Delta)` with `epsilon` small. If a
hollow convex body `K subset U` had width at least `2+sqrt(2)`, the two lattice
functionals `x/2` and `y/2` force `K` to contain points close to all four
vertices of `Delta` (each functional has unique extrema at the appropriate two
vertices). The four facet contacts `p_i` then have weakly separating planes
`H_i` from `K`. For small enough `epsilon`, those four inequalities are a
small perturbation of the four facet inequalities of `Delta`, and their
intersection `Delta'` contains `K` and lies in the tetrahedral local chart.

Theorem 1.2 gives `width(Delta') <= 2+sqrt(2)`, with equality only for
`Delta'=Delta`; monotonicity under containment gives the same upper bound for
`K`. If `K` is a strict subset of `Delta`, one of the two functionals `x/2`
or `y/2` has strictly smaller width, so equality is possible only for
`K=Delta`.

The phrases “points close”, “planes close” and “small enough” are continuity
arguments in the paper; no explicit Hausdorff radius is supplied. The extension
also assumes the chosen four contacts and supporting planes stay in the local
combinatorial chart.
