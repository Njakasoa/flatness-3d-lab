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
