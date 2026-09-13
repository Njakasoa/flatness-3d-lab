# Next scientific actions — two tetrahedral classes excluded

CLAIM-0006 proves restricted containment bounds for hollow real tetrahedra:
B13=(14+26/sqrt(3))/9 and B10=(21+40/sqrt(3))/13. The determinant-13
continuous proof was independently reviewed. The parameterized version and
both arithmetic applications have independent exact checks. Novelty remains
unconfirmed; no global flatness improvement is claimed.

1. At width at least 2+sqrt(2), the full tetrahedral contact classes of
   determinants 10 and 13 are excluded. Eight tetrahedral classes remain,
   together with 52 spatial hulls of five to eight contacts and the square:
   61 necessary full hulls. Above c=(11/7)(1+2/sqrt(3)) only determinant 13
   is excluded, leaving 62. Preserve the distinction between these thresholds.
2. Weighting the two-vector estimate is now solved exactly within the stated
   pair domain: 123 endpoint/balancing candidates. The determinant-eight bound
   improves to (1+12A)/7, still above candidate width. No new class is removed.
   Do not repeat this finite weight scan as if it were a new search.
   Next investigate direction-sensitive inverse oscillation or additional
   blocker implications that bound the ten width numerators directly.
3. The four-row matching step is essential. Do not discard a five-to-eight
   contact hull because it contains a determinant-10 or determinant-13
   subset. A nonsimplicial surrounding body is outside the containment bound.
   A rectangular-matrix extension would need a different argument.
4. The generic observer implementation now supplies exact guard sets for all
   nine nonunimodular contact tetrahedra, under boundary-contact and the
   stated edge-gauge assumptions. Determinant 13 has one width-one slab,
   four lines and 20 guards; only two edge directions occur in its truncation.
   These lists are useful even though two full tetrahedral classes are now
   separately excluded at candidate width. They do not imply a width bound.
5. Complete cubic models now exist for determinants seven and eight, each
   with eight variables, ten complete primitive width directions, twenty
   observer guards and the necessary gauge/volume cuts. Both bounded target
   queries returned UNKNOWN. Positive and negative pins and a read-only
   encoding audit pass. The determinant-two target also remains UNKNOWN.
   No unchanged nonlinear target is to be rerun.
   The proposed shortcut E_min(F)<=12/17 from gauges and contacts is false:
   two exactly hollow rational models violate it strictly. Their full global
   difference minima are certified, not inferred from selected vectors.
   The determinant-eight example even passes the sharper exact ACMS gauge
   threshold for width 17/5. Thus merely tightening the coarse beta cannot
   rescue that total-leakage implication. A direction-sensitive argument
   may avoid counting harmless mixing within equal-height columns.
6. Continue priority checks, including equivalent formulations and the
   determinant-10 corollary. ACMS supplies the gauge inequality and standard
   stochastic contraction has prior literature. No first-proof claim is made.

Exact incremental replay, no solver:

```sh
python3 reproduce_contraction.py
```

It checks the two-vector contraction, its finite scan, generic observer
lists and three independent implementations under -O. The earlier geometry
and 63-type certificates are unchanged, valid supersets, and retain their
previous validation. The new exclusion is analytic, not a reinterpretation
of an old timeout.

This public update exports scientific checkpoint 9072ef0. The active research goal remains open while the
remaining types, external novelty and global width optimization are unresolved.

New exact replay (no solver query):

```sh
python3 -m experiments.weighted_two_vector_bounds
python3 -O tests/replay_weighted_trace_independent.py
.venv/bin/python tests/audit_nonunimodular_encoding.py
```

The last audit needs the optional Z3 dependency but never calls Solver.check.
The original non-strict and later strict trace runs are separate archived
models; the latter were needed to disprove the weak leakage implication.
