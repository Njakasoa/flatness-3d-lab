# CLAIM-0010 — quantitative interlacing in the determinant-five Y chart

Date: 2026-09-14. Status: analytic restricted result, independently reviewed
and supported by exact symbolic/fixture replays. Mathematical priority is
unconfirmed. No new global flatness bound or full contact-class exclusion.

## Statement and exact hypotheses

Let K=conv(v0,v1,v2,v3) be a compact full-dimensional hollow real tetrahedron
in the standard lattice Z³. The ordered points

    p0=(0,0,0), p1=(5,1,2), p2=(0,1,0), p3=(0,0,1)

must lie in the relative interiors of the facets opposite v0,v1,v2,v3,
respectively. Put Y=(0,1,0), A=1+2/sqrt(3), and normalize the actual
vertex heights by q_i=(Y(v_i)-min_j Y(v_j))/width(K,Y).
Assume q0=0 and q3=1; these extrema need not be unique.

The [ordering lemma](../proofs/DET5_Y_CORNER_ANALYTIC_PROBE.md) gives q1!=q2.
Write x=min(q1,q2), y=max(q1,q2), and

    L=(y-x)/(y*(1-x)),      0<L<=1.

The denominator is positive, including tied endpoint extrema. Then:

| Original height order | Sufficient domain | Full lattice-width bound |
|---|---|---|
| q1<q2 | L<2/3 | w(K)< A/(2/3-L) |
| q1>q2 | L<12/17 | w(K)< A/(4/5-17*L/15) |

In particular, either of the following closed band conditions implies

    w(K)<(500/317)A = 3.3985812908190087... <17/5:

- q1<q2 and L<=49/1500;
- q1>q2 and L<=249/1700.

Thus an actual body in this chart with w(K)>17/5 necessarily satisfies the
strict disjunction

    q1<q2 AND q2-q1 > (49/1500)*q2*(1-q1),
    OR
    q1>q2 AND q1-q2 > (249/1700)*q1*(1-q2).

These are analytic two-dimensional height-band exclusions, with a strict
width conclusion even on their band endpoints. They cover neither all Y
extrema charts nor the entire determinant-five contact class. The necessary
58-type count is unchanged. Larger containing polytopes are not covered by
the tetrahedral facet-contact hypothesis.

## Proof and antecedents

The [independent compact-chart proof](../proofs/DET5_COMPACT_SHAPE_CHART_REVIEW.md)
uses p=x/y, q=(1-y)/(1-x), C=(1-x)c, E=y*e. Here q is a compact
shape coordinate, distinct from the indexed vertex heights q_i. The positive
chart gives C+E<1 and expresses the two horizontal contact differences exactly.

Hollowness makes (2,1,1) and (3,1,1) noninterior. For the first observer,
the separating-facet alternative R3 is impossible because F32>F30 in the
canonical low/high ordering. The remaining guard bounds u. The other
observer bounds r directly or gives an explicit bound on r-u. Positive-part
estimates then prove, without any high-width or volume assumption,

    q1<q2: gamma_(K-K)(2,0,1)<1/3+L,
    q1>q2: gamma_(K-K)(2,0,1)<1/5+17*L/15.

The change of sign of the horizontal vector in the reverse branch is
essential and is checked separately. Only two necessary observer guards
are used; no finite observer sufficiency theorem is needed for this proof.

Apply the established ACMS Lemma 5.1 inequality

    1-A/w(K) <= lambda1(K-K) <= gamma_(K-K)(2,0,1).

The strict gauge estimates and the positive displayed denominators give
the two claimed width bounds. Substituting the rational band endpoints gives
beta=183/500 in both branches and 1-beta=317/500. Finally,
A<(17/5)*(317/500)=5389/2500 is equivalent, after isolating and squaring the
positive radical, to 25000000<25038963. This proves the last strict comparison.

The contact/gauge programme and the last inequality come from
[Averkov–Codenotti–Macchia–Santos](https://arxiv.org/abs/1907.06199).
The new item in this lab is the explicit two-observer height-separation
argument and its bounded-coordinate consequence. No priority or sharpness
claim is made; the broader literature limitations in the
[dated height-domain audit](../proofs/DET5_HEIGHT_DOMAIN_LITERATURE.md) remain.

## Reproduction, independent review and limitations

```sh
.venv/bin/python tests/replay_det5_compact_shape_chart.py
python3 tests/audit_det5_separated_residual_queue.py
```

The first replay checks 42 symbolic identities, 2400 exact rational contact
matrices and 9600 observer equivalences, with separate tests of both gauge
estimates. Finite fixtures do not prove the universal inequalities; the
written analytic estimates do. The reverse-order estimate and endpoint-safe
R3 argument received a separate independent internal review.

The second replay checks the exact emitted polynomial cut and the preservation
of all prior residual constraints. Its [receipt](../results/det5_separated_residual_queue_validation.json)
records the resulting 70 refined entries among 258, with 188 other charts
unchanged. No entry removal or continuous coverage of the remaining domain
is claimed. The new band includes an explicitly certified positive-area
rectangle outside all previous Y exclusions.

The [bounded shape coordinates](../proofs/DET5_COMPACT_SHAPE_CHART_REVIEW.md)
now satisfy 1-pq>49/1500 in either order at target width. This separates their
rational denominator from zero. Singular determinant faces need their own
control; the [volume bound](../proofs/DET5_HORIZONTAL_FIBER_INTERVAL_LIFTING.md)
provides a determinant margin only under the true global-width hypothesis.
Neither this compactification nor exact linear optimization on individual
fibers completes the six-dimensional continuous-domain problem.
