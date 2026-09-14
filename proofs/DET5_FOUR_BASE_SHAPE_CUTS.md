# Four-base-shape cuts and forward horizontal branch reduction

Status: analytic simplification of necessary horizontal gauge constraints.
This neither excludes the remaining exceptional chart nor proves a complete
continuous cover. No solver query is used and previous proof files remain
unchanged.

Use the [negative determinant normal form](DET5_NEGATIVE_DETERMINANT_GAUGE_NORMAL_FORM.md),
with `A=C+pE`, `B=qC+E`, `S=C+E<1`, `alpha=S-A`, `d=y-x>0`,
`L=1-pq`, `0<a<=1`, `tau>0`, and `tau<1-aA/k`. Here `k=3` forward
and `k=2` reverse. Put `T=183/100=5*beta`, with `beta=183/500`.
The [forced exceptional observer](DET5_FORCED_OBSERVER_BRANCH.md) is retained.

## A strict consequence of the exceptional observer

Write `g=1-h`, `R=(1-y)r`, `U=(1-x)u`. Strict off-diagonal positivity gives
`F01=g-R>0`, `F02=g-U>0`. The forced observer is

    alpha>=k*F01+(5-k)*F02=5g-kR-(5-k)U.

Using `g>R` yields the strict necessary inequality

    Q:=alpha*(a/k+1/(5-k))-(1-y)*tau>0.              (1)

Indeed `U-R=(a/k)*alpha-(1-y)*tau`, and the observer implies
`alpha>(5-k)*(R-U)`. Equality in the observer itself remains permitted;
the strictness of (1) comes from strict contact positivity.

For clarity, projecting only these two contact positivities and the
observer over g gives both

    -alpha/(5-k)<U-R<alpha/k.

The upper inequality follows from `g>U`. It is automatic under
`0<a<=1`, `tau>0`, `y<=1` except at `a=1,y=1`, where the actual strict
conditions are impossible. Equation (1) alone is a necessary projection,
not a sufficient reconstruction of all h and t constraints. No division by
`1-y` is required, so the cuts below remain valid at `y=1`.

## Forward order: twelve selections reduce to four

Let `j=2-a/3`, `c=1+2a/3`. The three candidate pieces of five times the
`(1,0,0)` gauge are

    H1=jB,  H2=tau+j(B-A),  H3=jS-y*tau.

The two pieces for `(2,0,1)` are

    G1=cS+2y*tau,  G2=cA+2tau.

Because `2j+c=5`, the exact identities are

    2H3+G1=5S,
    2H3+G2=5S-2Q,                                  (2)

where Q is (1) with `k=3`. Thus `H3>T` and either `Gi>T` would require
`5S>3T=549/100>5`, which is impossible. **The third piece H3 can never
witness the `(1,0,0)` target while `(2,0,1)` also meets its target.**
This eliminates four of the initial twelve piece selections universally.

After that elimination, the `(1,0,1)` gauge is automatically satisfied by
its first piece

    J=(3+a/3)S+y*tau.

If `H1>T`, then `J>H1` since `S>=B`, `3+a/3>j` and `y*tau>=0`.
If `H2>T`, the exact identity

    J=tau+(5/2)S+(a/3+1/2)A+Q

gives `J>tau+(5/2)S>H2`, since `B-A<S` and `j<2`.
Thus the second-piece choices for `(1,0,1)` are redundant, rather than
impossible, in the surviving branches.

Under the stated normal-form domain and Q>0, the entire forward conjunction
of the four horizontal strict gauge targets is therefore **equivalent** to

    (H1>T OR H2>T)
    AND (G1>T OR G2>T)
    AND 3tau-(1-a)(A-B)>T.                          (3)

The last atom is the already established exact `(3,0,1)` reduction.
Equation (3) needs only four piece selections instead of twelve. It does
not eliminate either remaining `(1,0,0)` alternative. In particular,

    B>183/200 OR B-A>83/200                          (4)

is a necessary pure-base cut: `H1<T` whenever `B<=T/2` because `j<2`,
and `H2<1+2(B-A)-aB/3` by the strict upper bound on tau. This improves the
previous alternative `S>183/200` to `B>183/200`. The inequalities in (4)
are strict, including at their threshold endpoints.

## Additional pure-base cuts in both orders

The forced middle piece is

    M=k*tau-(1-a)*(A-B)>T.

The exact identity

    (1-y)*M+kQ
      =5*alpha/(5-k)-(1-a)*d*B                     (5)

uses `alpha+(1-y)*(A-B)=dB`. Since Q>0 and `(1-a)dB>=0`, it yields

    alpha>(5-k)*beta*(1-y).

Using `alpha=(1-p)E` and `1-y=q*(1-p)/L`, and multiplying/dividing only
by strictly positive L and `1-p`, this becomes the endpoint-safe polynomial
cut

    forward: L*E>183*q/250,
    reverse: L*E>549*q/500.                         (6)

No division by q or `1-y` is used; q=0 is included. Although the original
compact coordinates have p<1, the displayed polynomials themselves are
regular on closed interval boxes touching p=1.

There is an additional reverse-order cut. With k=2, strict `tau<1-aA/2`
gives

    M<2+B-A-aB.

Thus `M>T` requires `aB<17/100+B-A`. Since aB>0,

    reverse: A-B<17/100.                            (7)

This is strict; equality cannot support the selected gauge target. No
reverse-order branch-count reduction beyond the existing twelve selections
is claimed here.

## The asymmetric forward alternative is not contradicted by these premises

The following rational exact chart fixture satisfies all chart positivity
conditions, the first observer reduction, the exceptional observer and all
four horizontal targets, while `B<183/200` and `B-A>83/200`:

    x=0, y=3/5, C=1/100, E=4/5,
    a=1/10, tau=23/25, t=1/10, h=31/50.

Here `A=1/100`, `B=201/250`, `S=81/100`,
`u=aB/3=67/2500`, and `r=aA/3+tau=2761/3000`.
Its actual height gap is `b=h-x-(y-x)t=14/25`, hence its Y width is only
`25/14`. The fixture proves that the asymmetric alternative cannot be
universally removed using just the premises studied here. It is **not** a
large-width body, and no claim about full hollowness or the other gauges is
made. The exact matrix and all four gauge values are recorded in the replay.

Run `.venv/bin/python tests/replay_det5_four_base_shape_cuts.py`.
The [receipt](../results/det5_four_base_shape_cuts_validation.json) checks
symbolic identities, exact implication fixtures, and the explicit surviving
asymmetric fixture. The analytic arguments (1)--(7), not numerical samples,
prove the universal cuts and Boolean reduction.
