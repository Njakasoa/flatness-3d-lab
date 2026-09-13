# Public snapshot validation

Date: 2026-09-13. The curated public checkout was tested independently of the
original checkout's files, using the same Python 3.12 dependency environment
recorded in requirements.lock. Installed runtimes are not part of the export.

- Default reproduce.py: all 11 stages passed in the public copy.
- Unit tests: 10 passed.
- Independent SymPy baseline checker: passed, including ten rejected mutations.
- Eight selected exact discovery certificates: replayed; no counterexample.
- Contact enumeration: 3268 candidates, 239 empty ordered forms, 37 classes.
- Qualitative local Hessian and exact upper-bound arithmetic: passed.
- All 13 exact certificate JSON files and five scientific result/data files
  match the original scientific snapshot byte for byte after public replay.
- The recorded numeric search was retained, not regenerated during export.
- Machine-path and credential-pattern scan of public text: no findings.
- Third-party paper copies, session notes, raw mission and operational profiles
  are excluded. Mathematical CONTACT_SIGNATURE.md is retained as algorithm
  documentation, not session memory.

Public-only code adaptations make printed paths repository-relative and
remove machine executable paths from the environment audit. Replay logs
sanitize the checkout prefix. No mathematical algorithm or numerical seed
was changed. Timings, graphics and environment reports are regenerated outputs;
scientific equality was checked separately, as above.

SOURCE_MANIFEST.json covers every public file except itself. Its checker is
run before publication, and an intentionally corrupted expected hash must
be rejected. Check the archived hashes before replaying, because replay
refreshes outputs. The manifest is an integrity record, not a digital signature.

## Structural-update validation

The public copy was replayed again for the update from source da24c58:

- Baseline reproduction: all 11 stages and 10 unit tests passed again.
- Contact-reduction reproduction: all eight stages passed.
- Independent contact verifier: 51 main tetrahedron classes, 52 larger hulls,
  1,365 four-point subsets, nine templates and 63 affine maps passed;
  all 21 deliberate mutations were rejected.
- Nine new scientific JSON/JSONL payloads exactly match committed source bytes
  after replay, including all three new contact certificates. The execution
  timing report is excluded from this equality comparison. The square-control
  payload also matches after excluding its public-only source citation edit.
- All 13 baseline certificate files retain their archived hashes.
- Both recorded numerical campaigns were retained without regeneration.
- Uncommitted ongoing experiments are excluded from this publication.

The historical Astra review remains internal AI-assisted review. No external
peer review or new global flatness theorem is implied. Contact-hull reduction
now includes the square and nonsimplicial branches. Continuous optimization
within those classes and the explicit published local-radius computation
remain unresolved. The 63 types are necessary possibilities; neither their
high-width realizability nor external novelty of the list is established.

## Continuous-family update validation

From source revision 9de72cf, the public copy passed four incremental
commands: both determinant-two witness generators, the independent Fraction
checker, and the finite-domain generator. The two witness certificates,
finite-domain certificate and independent report all reproduced byte for byte.
Each witness check rejects three mutations; substitution of the six-contact
witness under the four-contact claim is also rejected. The report is
[det2_public_validation.json](results/det2_public_validation.json).

The existing geometry engine and the two previously validated reproduction
pipelines are unchanged. Their earlier full replays remain applicable; this
incremental export did not rerun them. Optional floating searches and the
bounded SMT run were retained as recorded experiments, not regenerated.
The SMT timeout supplies no infeasibility certificate. New proof reviews
are internal AI-assisted reviews with their correction closures preserved.

All Markdown links resolve locally, the public text has no private machine
paths or credential-pattern findings, and archived baseline certificates
retain their previous hashes. The complete snapshot manifest was refreshed.

## Pair-model update validation

From committed source 38fbeef, three incremental commands passed in the public
copy: the matrix identity generator, the independent SymPy checker under
Python `-O`, and the complementary-minor identity generator. Both new
certificates reproduce source bytes exactly; all 19 previously published
certificates retain their hashes. The independent checker verifies 45
determinant terms, 16 adjugates, 16 boundary patterns, eight symmetries,
256 weak order tuples and 24 affine lattice maps; two mutations are rejected.
The cubic generator verifies all 18 formal axis/pair identities.

See [the incremental receipt](results/pair_public_validation.json). The
unchanged baseline/contact pipelines were not rerun; the new optional SMT
queries retain their original records and were not repeated for publication.
Neither UNKNOWN outcome is an infeasibility certificate. Public text and
local Markdown links were checked and the complete manifest refreshed.

## Observer-guard update validation

From committed source e84400e, all nine stages of
`reproduce_observer_guards.py` passed in the public copy. The six new exact
certificate files match source bytes after replay; all 21 previously public
certificates retain their archived hashes. Independent checkers reject 44
mutations and whole-witness substitutions, run under Python `-O`, and verify
the strict integer endpoint regression. See the command-by-command receipt
in [observer_validation.json](results/observer_validation.json).

The geometry core and the previously validated baseline/contact pipelines
are unchanged. This publication replay runs no numerical search and no solver
query. Archived nonlinear targets remain UNKNOWN; archived linear implication
checks are distinct evidence and do not establish a width bound.

All public Markdown links resolve. The text scan found no private machine
paths or known credential patterns. The SHA-256 manifest covers all public
files except itself, and a deliberately corrupted expected hash is rejected.
The new figures are explanatory; classification inputs and the six gauge
hypotheses remain explicit in the linked written proofs.
