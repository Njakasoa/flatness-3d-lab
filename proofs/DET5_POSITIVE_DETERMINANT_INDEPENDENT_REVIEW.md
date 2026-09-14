# Independent review: exclusion of the positive horizontal determinant

Status: PASS for the entire nonnegative-determinant outer domain of both
ordered Y[0,3] charts. This is an independent internal analytic review, not
external human peer review or a proof-assistant certificate. The remaining
negative determinant domain is not excluded.

Reviewed source: [the determinant-sign argument](DET5_POSITIVE_HORIZONTAL_DETERMINANT.md).
Its exact bytes and the earlier chart proof are bound in
[the independent receipt](../results/det5_positive_determinant_independent_review.json).
No reviewed source or prior archive was changed and no solver query was run.

## Triangle and physical-vector checks

Retain the source notation `A=C+pE`, `B=qC+E`, `S=C+E<1`,
`D=uA-rB`, and `V=F(e1-e2)`, `Z=F(e3-e0)` in canonical order.
All divisions in the triangle argument are by `A,B>0`.
The exact observer condition is `ku<=B`, with `k=3` forward and `k=2`
reverse. Its discarded alternative is impossible on the actual chart
because `F32>F30`, including the endpoint `x=0`.
Thus `D>=0` implies `0<=r<=Au/B`, and the three explicit barycentric
weights in the source are nonnegative and reconstruct `(u,r)`.
This is the full stated triangle, not a sampling approximation.
Its vertices need not correspond to valid strict-contact tetrahedra:
they are used only to bound the convex function of `(u,r)` containing
every valid pair. Consequently there is no hidden assumption of geometric
feasibility at the vertices.

Solving the physical affine contact equations for `(2,0,1)` gives
`ell=(-1,2,-2,1)/5`. Swapping the middle canonical contact indices gives
`(-1,-2,2,1)/5`. The simultaneous row permutation preserves the half-l1
norm. Therefore the forward image is `(Z+2V)/5`, and the reverse image is
`(Z-2V)/5`, exactly as stated. The determinant is unchanged by the two
permutations; both actual orders still satisfy `det(F)=bD`.

## Vertex norms and strictness

At the triangle origin `V=0`, and `Gamma(Z)=S` in both branches.
At `(u,r)=(B/k,A/k)`, the two displayed algebraic identities give
`V=Z/k`. The resulting forward and reverse gauges are respectively
`S/3` and zero.

At the remaining vertex `(B/k,0)`, forward order has `Gamma(V)=B/3`,
because `0<=x<=1`. Hence the triangle inequality gives
`Gamma((2V+Z)/5)<=(2B/3+S)/5<=S/3`.
Reverse order admits an even simpler exact expression than the source
requires:

    Z-2V = (-(1-y)*A, 0, A, -y*A).

Indeed `alpha-(1-x)*B=-(1-y)*A` and `omega+x*B=y*A`.
Its gauge is exactly `A`, so the scaled vertex gauge is `A/5<=S/5`.
This expression is valid when `x=0`, `y=1`, or both; zeros in the displayed
vector cause no sign ambiguity.

For fixed shape coordinates other than `r,u`, the images are affine and
Gamma is convex. Their values throughout the triangle are therefore at
most `S/3` forward and `S/5` reverse. This is a universal convexity proof,
not an inference from finite fixture checks. Since strict contacts imply
`S<1`, the selected physical gauges are strictly less than `1/3` and
`1/5`, even if a triangle boundary or a tied height extremum is included.
No gauge lower bound, volume margin, or large-width assumption entered
this upper-bound argument.

## ACMS consequences and precise scope

The archived primary ACMS Lemma 5.1, equation (14), applies to all hollow
three-dimensional convex bodies and gives `1-A0/w<=lambda1(K-K)` with
`A0=1+2/sqrt(3)`. The selected nonzero lattice vector gives
`lambda1(K-K)<=gamma_(K-K)(2,0,1)`. Combining these with the strict
upper bounds yields exactly

    w < 3*A0/2  in forward order,
    w < 5*A0/4  in reverse order,

under `D>=0`. The denominators `2/3` and `4/5` are positive.
Both constants are strictly below `17/5`, as checked by exact rational
radical comparisons. Therefore every actual target body in this Y[0,3]
chart must have `D<0`, or equivalently `det(F)<0` since `b>0`.
For an actual full-dimensional tetrahedron `D=0` is impossible already;
including it in the outer proof is harmless and strengthens the algebraic
statement. The proof does not apply to other Y-extrema charts without
another argument and does not eliminate the whole contact class.

No correction is required. The independent stdlib replay checks physical
contact-vector reconstruction, exact reverse vertex identities, rational
triangle boundary/interior cases including tied extrema, and the final
constant comparisons. These support the formulas; the reasoning above
is what proves the full continuous-domain conclusion.
