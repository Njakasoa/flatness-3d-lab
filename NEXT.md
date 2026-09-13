# Next scientific actions — complete observer models

CLAIM-0005 now provides a complete hollowness test for nonunimodular empty
contact tetrahedra whose vertices remain boundary contacts. The known
observer/classification principles have been specialized and independently
verified. This changes the model's scope; it does not yet improve Flt(3).

1. Apply the general construction to the nine nonunimodular tetrahedra in
   CLAIM-0004, beginning with the determinant-13 contact tetrahedron
   conv(0,(13,1,5),e2,e3). Its small difference-minimum margin above the
   necessary threshold may constrain its column matrix strongly. Enumerate
   its at-most-three width-one slabs, at-most-twelve observer lines and the
   gauge-truncated guards exactly, with an independent implementation.
   Do not assume the determinant-two pair/cycle blocker classification
   applies to other contact tetrahedra.
2. Use the short lattice vectors of that contact hull to study how much a
   containing tetrahedron can expand while preserving the necessary
   difference gauges. Seek a quantitative matrix-contraction or directional
   width bound, or a small exact decomposition into linear blocker cells.
   This is the next proof task, not a request for a longer unchanged NRA run.
3. The determinant-two pair model is now complete at target 17/5: eight
   variables, cubic constraints, 37 complete width directions, 20 hollow
   exclusions and SIX explicit contact-edge gauge cuts. Its bounded target
   query returned UNKNOWN, with nontrivial exact four-contact SAT/UNSAT
   controls. Preserve this result; no family has been eliminated.
4. The six-edge gauge assumptions are mandatory for the 64/20 guard list.
   With only volume<21, use the full 1456/484 list. Without either assumption,
   the complete theorem uses twelve infinite lattice lines. The original 216
   and symmetry-closed 432 point screens alone are insufficient. In particular,
   do not infer full hollowness from an old partial-screen SAT model.
5. Preserve the strict pair witness with precisely four index-two contacts
   and width>19/6. A universal pair width<=3 pruning rule is false. The earlier
   cycle witness above 13/4 remains valid; neither witness is an optimum.
6. Continue the novelty audit: Averkov–Schymura Lemma 6.4 already contains
   observer-line methods, and Blanco–Santos/Howe supplies the width-one input.
   Priority of the boundary-contact specialization and gauge truncation is
   unconfirmed. The unimodular contact class and non-tetrahedral contact
   hulls remain outside CLAIM-0005's d>1 tetrahedral statement.

Exact incremental replays, without solvers:

```sh
python3 -m experiments.certify_det2_pair_column
python3 -m experiments.certify_det2_pair_four_contacts
python3 tests/replay_det2_pair_column_independent.py
python3 -m experiments.det2_partial_box_counterexamples
python3 -m experiments.det2_observer_lines
python3 tests/replay_det2_observer_lines_independent.py
python3 -m experiments.det2_observer_gauge_guards
python3 tests/replay_det2_gauge_guards_independent.py
```

The column polynomial certificate additionally needs SymPy:
`.venv/bin/python -m experiments.pair_column_identities`.
The optional target module is `experiments.det2_pair_gauge_complete_smt`;
its archived UNKNOWN result is not an infeasibility certificate. The general
constructor's lower-threshold pin is only a control; the 64-guard theorem
in that module is justified at the main threshold 17/5.

This public snapshot includes the complete observer-guard checkpoint.
The next research task is the determinant-13 class above. An internally
reviewed specialization does not establish a new global bound or priority.
