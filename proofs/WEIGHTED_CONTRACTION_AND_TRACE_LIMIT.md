# Weighted contraction and the limit of a total-leakage criterion

Date: 2026-09-13. Analytic refinement of the reviewed two-vector argument,
with an independent arithmetic implementation. No additional contact class
is excluded. No new external mathematical review or novelty claim is made.

## Positive weights

Use the notation of [TWO_VECTOR_CONTRACTION.md](TWO_VECTOR_CONTRACTION.md).
Let m_r=min_j |l_rj|, a_r=||l_r||_1/2, and choose t in (0,1). Write

    S=t a1+(1-t)a2, m=min(t m1,(1-t)m2)>0.

The weighted sum of the two cancellation losses is at most S-beta when
both lattice gauges are at least beta. Every entry with a mismatched
two-sign code contributes at least m times its matrix mass. Therefore

    E <= (S-beta)/m.

If beta>S-m then E<1, so the same four-row matching and oscillation proof
gives w(K)<=m/(m-S+beta). With beta=1-A/w(K), A=1+2/sqrt(3), the low-width
split and the positive-denominator rearrangement yield

    w(K) <= (m+A)/(m-S+1).                               (1)

The vector domain here has a1,a2<1, so the denominator is positive for
every t. On either side of t=m2/(m1+m2), m and S are affine functions of t.
The right side of (1) is a fractional linear function with positive
denominator. Its derivative has constant sign, or is identically zero.
Thus its best value on this domain is obtained at the balancing weight
or an endpoint. At t=0 or t=1, m=0 and the matching argument is unavailable,
but the limiting bound A/(1-a_r) is independently the established intrinsic
containment bound. These three candidates exhaust this particular estimate
for a fixed pair. They do not exhaust multiple-vector or other matrix bounds.

## Determinant eight

For P=conv(0,(8,1,3),e2,e3), take z1=(1,0,0), z2=(2,0,1), with rows

    l1=(3,1,-1,-3)/8,  l2=(-1,1,-1,1)/4.

Both masses are 1/2. Since m1=1/8 and m2=1/4, choose weights 2/3 and 1/3.
Then S=1/2 and m=1/12, and (1) gives

    w(K) <= (1+12A)/7 = (13+24/sqrt(3))/7
          = 3.8366294943... .

This holds for every hollow real tetrahedron K containing an affine
unimodular image of P, without prescribed facet contacts. It improves the
equal-weight estimate (17+32/sqrt(3))/9 but remains above 2+sqrt(2).
For determinant seven, the best candidate in this calculation is the known
intrinsic bound 7A/4. The previous determinant-ten and thirteen exclusions
are unchanged. The 41 pairs give 123 exact weight candidates.

## An insufficient total-leakage criterion

For a column-stochastic matrix F define

    E_min(F)=4-max_permutation sum_j F_(permutation(j),j).

If E_min(F)<=12/17 then the inverse oscillation argument would bound width
in a contact width-one direction by 17/5. It was tempting to derive this
condition from the exact gauges and lattice blockers alone.

The saved rational models disprove that implication at the probe threshold
beta=37/102, even with full hollowness and the global difference minimum
checked independently. Both have positive off-diagonal entries and zero
diagonal, so each of the four prescribed lattice contacts is in the relative
interior of its own facet.

| contact determinant | exact width | E_min(F) | lambda1(K-K) |
|---:|---|---|---|
| 7 | 2380/1893 | 5041/7140 > 12/17 | 2591/7140 > 37/102 |
| 8 | 579334934324160/305964690282487 | 34613/48960 > 12/17 | 125857/342720 > 37/102 |

For determinant eight the global minimum also exceeds the sharper value
1-A/(17/5). Thus improving only the coarse rational approximation of the
ACMS constant cannot rescue this total-leakage implication for that class.
Neither example has large lattice width. They invalidate this sufficient
intermediate condition, not the desired class width bound.

The original non-strict trace queries produced E_min=12/17, which alone
would not disprove a weak leakage bound. The subsequent strict trace queries
were genuinely different and supply the strict examples above. Both original
records are retained, and no query was repeated for a documentation change.

The independent verifier computes every permutation trace, every lattice
point in the whole body box, all possible minimizing width covectors from
an independent inverse-frame bound, and every potentially minimizing lattice
vector in the whole difference-body box. The last box is complete because
an integer contact edge gives lambda1<=1. This is stronger than checking
only the finite gauge constraints used to find the examples.

## Reproduction

```sh
python3 -m experiments.weighted_two_vector_bounds
python3 -O tests/replay_weighted_trace_independent.py
```

The checker imports no generator, geometry core or solver. It checks all 123
weight candidates and four archived exact bodies (two endpoint controls and
the two strict counterexamples), and rejects four meaningful mutations.
The rational matrices and full body certificates are saved in the two
`results/contact_contraction_trace_probe*.json` files.

Optional search: `experiments.contact_contraction_trace_probe` and its
`--strict` variant require Z3. Replaying the proof inputs does not rerun them.
