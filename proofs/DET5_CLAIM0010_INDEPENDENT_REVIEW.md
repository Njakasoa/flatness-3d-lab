# Independent adversarial review of CLAIM-0010

Status: PASS for the mathematical statement and its stated scope. This is an
internal independent agent review, not external human peer review or a
proof-assistant certificate. The reviewed claim and source bytes are identified
in [the review receipt](../results/det5_claim0010_review_validation.json).

I checked [CLAIM-0010](../claims/CLAIM-0010.md) against the full
[compact-chart argument](DET5_COMPACT_SHAPE_CHART_REVIEW.md), its exact replay,
the residual-queue audit, and the locally archived primary ACMS text,
Lemma 5.1, equation (14), on PDF page 18. The primary lemma concerns every
three-dimensional hollow convex body; the maximizing-body hypothesis starts
in the following subsection and is not a premise of equation (14).

The claim correctly applies that lemma to full lattice width, with
`mu1(K)=1/w(K)`, and uses `lambda1(K-K)<=gamma_(K-K)(2,0,1)` because
`(2,0,1)` is a nonzero integer vector. The argument requires no lower bound
on any gauge: the compact proof's two strict gauge upper estimates follow
from exact contact positivity and two necessary observer guards alone.
Consequently the ACMS corollaries do not circularly assume large width.

For each branch write its strict gauge upper bound as `G(L)`. The deduction
is `1-A/w <= lambda1 <= gamma < G(L)`. When `1-G(L)>0`, this is equivalent
to `w<A/(1-G(L))`. The claim's two domains are exactly the positivity domains
`L<2/3` and `L<12/17`. At the stated rational band endpoints both expressions
for `G` equal `183/500`; hence both strict width bounds are
`w<(500/317)A`. The bound is increasing as `L` increases, so substituting
a closed band endpoint is valid. Strictness comes from the positive contact
conditions in the gauge estimates and survives at the band endpoint.
The exact radical comparison with `17/5` is correct. A 60-digit decimal
check gives `3.398581290819008720849...`; the initial displayed
`3.3985812908190085...` was corrected to `3.3985812908190087...`.
This is a decimal-rendering issue; the exact constant and all inequalities
are unchanged.

Endpoint and order checks:

- `0<=x<y<=1` gives `y>0` and `1-x>0`, so the height denominator never
  vanishes in the actual chart. Also `y(1-x)-(y-x)=x(1-y)>=0`, proving `L<=1`.
- Tied endpoint extrema (`x=0` or `y=1`) have `L=1`. They are allowed in
  the hypotheses; neither narrow band claims to include them.
- The proof eliminates `R3` using `F32>F30` also when `x=0`, where the
  first intermediate inequality is non-strict. The next inequality is
  strict because `b>0` and `C<t`.
- Reverse ordering uses the conjugated guards and the physical image
  `(Z-2V)/5`. The claim does not confuse it with `(Z+2V)/5`.
- Multiplication by the positive height denominator gives exactly the
  two strict polynomial inequalities stated in the necessary disjunction.

The residual-queue statement is consistent with its independent audit:
258 entries are preserved, 70 receive the new two-branch condition and
188 other-chart entries are unchanged. The audit establishes a positive-area
rectangle outside the preceding Y exclusions; it does not claim that the
remaining continuous domain is covered. The claim also preserves this limit,
the 58 necessary contact types, and its tetrahedral facet-contact scope.

No substantive mathematical correction is required; the decimal correction
above has been applied in the reviewed version. This review does not establish
priority, sharpness, an additional global flatness bound, or completeness
of the residual search. The accompanying stdlib replay verifies the new
corollary arithmetic and source bindings without modifying the reviewed files
or rerunning any archived solver query.
