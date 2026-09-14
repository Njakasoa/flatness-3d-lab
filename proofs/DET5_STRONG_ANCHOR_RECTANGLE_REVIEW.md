# Independent exclusion of a continuous rectangle near the fixed-height anchor

Let `P=conv(0,(5,1,2),e2,e3)` have the prescribed strict relative-interior
facet contacts in a hollow full-dimensional tetrahedron `K`. In the normalized
Y-extrema chart `[0,3]`, write the vertex heights as `(0,q1,q2,1)`.
There is no such `K` with **global lattice width greater than `17/5`** and

    0 <= q1 <= 1/256,       31/256 <= q2 <= 33/256.       (1)

This is a continuous closed rectangle, including all its boundary points.
It is a restricted contact-domain exclusion, not a whole determinant-five
class exclusion and not a new global bound for `Flt(3)`.

## Necessary premises and the independently reconstructed statement

The established ACMS deduction for the global target gives
`gamma_(K-K)(v)>183/500` for every nonzero integer vector `v`. The rational
threshold is valid because

    1+2/sqrt(3) < (17/5)*(1-183/500) = 5389/2500.

The established volume consequence is `vol(K)<(183/500)^(-3)`.
The [width-to-volume monotonicity lemma](SIMPLEX_WIDTH_VOLUME_MONOTONICITY.md)
applied to `P subset K` gives

    width(K,Y)/vol(K) <= width(P,Y)/vol(P) = 6/5.

Consequently, with `gap=1/width(K,Y)`,

    gap > (5/6)*(183/500)^3 = 2042829/50000000.           (2)

The global target also implies `gap<5/17`. These are necessities of the
hollow global-width hypothesis; they do not follow merely from a finite list
of selected gauges and a large Y width.

The audited linear statement has 22 variables and 84 assertions:

| Premises | Count |
|---|---:|
| Positive off-diagonal entries of F | 12 |
| Column stochasticity | 4 |
| Offset and original gap domain | 4 |
| Physical lattice-vector gauge bounds | 11 |
| Contact observer guards | 20 |
| Bounds on the two free heights | 4 |
| McCormick bounds on six lifted products | 24 |
| Four contact-height identities | 4 |
| New lower gap bound (2) | 1 |

The eleven physical gauge vectors are
`(0,0,1), (0,1,-1), (0,1,0), (1,0,0), (1,0,1), (2,0,1), (3,0,1),`
`(5,0,2), (5,1,1), (5,1,2), (1,-1,1)`.
The audit obtains all contact coordinates by independently inverting the
homogeneous contact matrix. It reconstructs every signed-subset gauge
inequality, all twenty observer disjunctions, and all four envelopes for each
product. For an actual body, setting each lifted variable to its true product
satisfies those envelopes. No sufficiency of this relaxation is needed.

The statement was refuted by cvc5, and its archived CPC proof was checked by
Ethos against the complete reference statement. The independent audit binds
both actual input and proof bytes to that successful reference-bound receipt.
It does not infer an exclusion from a solver status alone. Mutations removing
the lower gap premise, lowering the gauge threshold, dropping the eleventh
gauge, or changing a height endpoint are rejected.

The generic reference adapter was also independently reviewed and exercised
on three-, six-, and 22-variable inputs, as well as a synthetic input with
nested Boolean lets, variable shadowing, and an explicit false assertion.
Every assertion survives expansion and numeric typing with the same meaning
and position. The separately recorded proof check also rejects an unrelated
false assumption. This is external software checking, not human peer review.

## Exact additional coverage

Each of the eight earlier certified closed Y rectangles has a coordinate
interval strictly separated from the corresponding interval in (1).
Thus (1) lies wholly outside their union, including at every endpoint.
Its area in the normalized `(q1,q2)` plane is exactly

    (1/256)*(2/256) = 1/32768.

It also lies outside the newer analytic diagonal exclusion. Throughout (1),
`q1<q2` and

    L=(q2-q1)/(q2*(1-q1))
       >= (30/256)/(33/256) = 10/11 > 49/1500.

The rectangle therefore adds coverage beyond both earlier rectangle exclusions
and the `L<=49/1500` analytic band. Its benefit must be represented by the
strict outside clause

    q1<0 OR q1>1/256 OR q2<31/256 OR q2>33/256.

Within the existing nonnegative chart this simplifies to
`q1>1/256 OR q2<31/256 OR q2>33/256`; equality stays excluded.
No area statement here asserts that a physical tetrahedron occupies every
height point, nor that every residual queue entry meets this rectangle.

Reproduce the independent audit with
`.venv/bin/python tests/audit_det5_strong_anchor_rectangle.py`.
The [validation record](../results/det5_strong_anchor_rectangle_validation.json)
contains exact old-union separation witnesses, input and proof hashes,
reference-adapter checks, and mutation controls. That command performs no
new discovery solver or proof-kernel calls.
