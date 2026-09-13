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

The historical Astra review remains internal AI-assisted review. No external
peer review or new global flatness theorem is implied. The explicit published
local-radius computation, square contact branch, nonsimplicial branches and
continuous optimization of all contact types remain unresolved.
