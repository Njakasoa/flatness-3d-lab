# Independent review of the four-base-shape cuts

Status: PASS for the stated necessary cuts and forward Boolean equivalence.
This is an independent internal analytic review, not a finite cover or an
exclusion of the surviving chart. The reviewed source is
[the four-base-shape note](DET5_FOUR_BASE_SHAPE_CUTS.md); the exact source
bytes are bound in [the independent receipt](../results/det5_four_base_shape_cuts_independent_review.json).
No previous file or solver archive was modified or rerun.

## Projected observer and strict endpoints

Set `delta=U-R`, where `R=(1-y)r`, `U=(1-x)u`, and let `g=1-h`.
The three inequalities being projected are

    g>R, g>U, 5g<=alpha+kR+(5-k)U.

They admit some g exactly when the upper endpoint for g is strictly larger
than both R and U. This gives

    -alpha/(5-k)<delta<alpha/k.

The source's normal form has `delta=a*alpha/k-(1-y)*tau`, so the left
inequality is exactly `Q>0`. The right inequality is equivalent to
`(1-a)*alpha/k+(1-y)*tau>0`; it is automatic except when `a=1,y=1`.
That exceptional endpoint is incompatible with the strict original
conditions even though Q alone may still be positive. The source correctly
identifies this limitation and does not call Q a sufficient reconstruction
of the remaining fiber constraints. Equality in R0 remains allowed;
strictness of Q comes from the two contact positivities.

## Forward branch equivalence

With `T=183/100`, the two identities
`2H3+G1=5S` and `2H3+G2=5S-2Q` are exact. Since `Q>0`, `S<1`, and
`3T>5`, H3 cannot exceed T simultaneously with either G piece exceeding T.
Thus it is sound to remove H3 as the witness for the first gauge in the
full conjunction. This is not a statement that H3 is always small on its own.

For the third gauge's first piece J, H1>T implies J>H1 directly from
`S>=B>0` and its larger coefficient. If H2>T, the stated identity
`J=tau+(5/2)S+(a/3+1/2)A+Q` gives J>H2, using `B-A<S` and `j<2`.
So J alone already witnesses the third gauge in every surviving branch.
Its other piece is redundant, not impossible. The final gauge retains its
previously proved exact middle-piece atom. This establishes both directions
of the claimed equivalence and the reduction from twelve complete piece
selections to four, under the declared normal-form domain and Q>0.

The base-only disjunction is correctly weaker. H1>T forces `B>T/2`
since `j<2`. H2>T and `tau<1-aA/3` give

    T < H2 < 1+2(B-A)-aB/3,

hence `B-A>(T-1)/2` because `aB>0`. The result is precisely
`B>183/200 OR B-A>83/200`, with strict thresholds. It must not replace
the original gauge conjunction as an equivalent formula.

## Both-order cuts

The identity

    (1-y)M+kQ=5alpha/(5-k)-(1-a)dB

is exact. If M>T, its left side is strictly larger than `(1-y)T`:
this also holds at y=1 because `kQ>0`. The nonnegative subtracted term
on the right then gives `alpha>(5-k)*beta*(1-y)`. Substitution of
`alpha=(1-p)E` and `1-y=q(1-p)/L` divides only by positive `1-p` and L.
Thus the two polynomial cuts have the correct coefficients, strictness,
and endpoint scope. At q=0 they reduce to the automatic positivity `LE>0`;
there is no division by q or by `1-y`. Their polynomial extension to p=1
in outer boxes is not an assertion that p=1 is an actual chart point.

For reverse order the strict upper bound on tau gives
`M<2+B-A-aB`. Since M>T and aB>0, it follows that
`A-B<2-T=17/100`, as claimed. This is again a necessary cut, not an
additional reverse-order Boolean equivalence.

## Asymmetric fixture and scope

The supplied rational matrix has positive off-diagonal entries, unit column
sums, and the actual height identity for `(0,0,3/5,1)`. Its height gap is
`14/25`, so its actual Y width is `25/14`. Recomputing the four physical
gauges directly from this matrix reproduces all recorded values above
`183/500`; the first observer and exceptional R0 guard also hold.
It therefore prevents discarding the asymmetric forward alternative using
only the listed premises. Since full lattice width is at most Y width,
it cannot satisfy the global target `w>17/5`. No assertion of hollowness
or of other necessary gauges is licensed by this fixture, and the source
correctly makes neither assertion.

No correction is required. All new cuts preserve their necessary-condition
scope, and the stated forward equivalence retains its additional domain
hypotheses. The full twelve-branch projection remains valid independently
of whether a compiler adopts this simplification.
