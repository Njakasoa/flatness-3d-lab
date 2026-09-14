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

## Tetrahedral containment update validation

From committed source 9072ef03ec1c725ebd303449675f27ac028b00ef, all six
stages of `reproduce_contraction.py` passed in the public checkout. The
weighted generator and its independent trace/certificate verifier also passed,
with 123 weight candidates checked. Together these checks reject 48 mutations.
The three new certificate files and two-vector scan reproduce committed source
bytes exactly; all 27 previously public certificates retain their hashes.

The optional Z3 encoding audit passed for both eight-variable cubic models,
including ten complete width directions, twenty guards and exact positive/
negative pinned evaluations. It calls no solver. All archived solver outcomes
are retained unchanged. See [the incremental receipt](results/contraction_public_validation.json)
and [six-stage evidence](results/contraction_validation.json).

The existing geometry engine and classification artifacts are unchanged;
the earlier baseline/contact replays were not repeated for this incremental
export. Public Markdown links resolve, and the text scan found no private
machine paths or known credential patterns. The snapshot manifest is refreshed
and checked, including rejection of an intentionally corrupted expected hash.
The ongoing uncommitted research is excluded from this release.

## Three further contact-class exclusions — 2026-09-14

Public source checkpoint: f0920819acba3521f244d2510a3d9f901e4ea0fa.
The exact theorem statements are CLAIM-0007 and CLAIM-0008. At candidate
width, 58 necessary full contact types remain; the global bound is unchanged.

Fresh public-copy checks passed:

- `reproduce_height_cover.py`: rank arithmetic, normalized-height encodings,
  all 113 archived interval encodings, exact 62-leaf coverage and independent
  input/proof hash binding; zero satisfiability queries.
- `reproduce_det5_class4.py`: all nine exact guard lists, five full-square
  proof/input/reference bindings, and the explicit 58-survivor list.
- `tests/audit_det5_height_independent.py`: 98 archived formulas, five
  complete and three partial charts; eight rejected mutations, zero queries.
- `tests/replay_det5_height_witness_independent.py`: both rational hollow
  witnesses, complete widths and difference minima; three rejected mutations.
- Actual external Ethos kernel checking of all **67 CPC refutations** in
  the public copy, with referenced assumptions and final false conclusions.
  Both campaigns rejected their four negative controls. Fresh receipts:
  [62-proof check](results/public_height_ethos_validation.json) and
  [five-proof check](results/public_det5_ethos_validation.json).

The independent guard checker rejects ten mutations; the height-rank
checker rejects seven and the height-cover audit rejects five.
The archived proof-producer receipts and all 30 previously published
certificate files remain byte-identical. New scientific payloads match the
committed source, apart from two reproduction receipts whose runtime/mode
fields were refreshed. No numerical search or satisfiability query was rerun.
The unchanged baseline and contraction suites retain their earlier validation.

The separate publication review found the theorem scope and counts correct,
all local Markdown link targets present, no credential/private-path leak,
and no redistributed third-party paper. Partial class-5 searches remain
explicitly incomplete and are excluded from the theorem count. The source
manifest is refreshed over all public files; its checker and deliberate
hash-corruption control pass. Code/documentation license and primary-paper
attribution remain unchanged.

Fresh kernel checking establishes the archived linear refutations relative
to the pinned CPC signature. Geometry-to-SMT soundness has written proofs
and independent internal review; no external human review is claimed.

## Retained full-gauge obstruction and complete models — 2026-09-14

Scientific source: 79d0d35e1b3b4beab576f6c1b950ba4fc3b03e53. Eleven fresh public-copy checks passed.
All 837 exported scientific files match the committed source byte for byte.

- Seven standard-library checks cover the complete fifteen-direction geometry,
  the earlier symmetry witness, all three retained witnesses, the four-vector
  rank/volume arithmetic, and 1,536 formal partition identities for the nested
  tetrahedron lemma. The three retained-witness checkers reject fourteen
  mutations in total; the decisive witness exhausts 108 lattice points,
  59 potentially minimizing width directions and 341 gauge vectors.
- Two independent bilinear encodings and the determinant-three/four root and
  retained-fiber records pass their audits. The root checks evaluate actual
  rational relaxed SAT assignments. No nonlinear UNKNOWN is promoted to a proof.
- The continuation audits reconstruct 322 plus 127 new linear encodings,
  bind earlier inputs to reviewed hashes, and check exact inherited prefixes
  and complete recorded frontiers. The last archive has 953 queries,
  27 charts closed according to archived solver labels and 259 pending boxes.
  These audits do not certify those UNSAT labels with a proof kernel.

No solver query was run. All 167 previously public certificate files,
including the 67 CPC proof payloads, remain byte-identical; their previous
public-copy Ethos validation is retained without repeating unchanged proofs.
The baseline and earlier exclusion results are unchanged.

The final internal publication review confirms scope, counts, imports and the
explicit hollow-body hypothesis required by ACMS. Local Markdown links and
Python syntax checks pass. The text scan found no private machine paths or
known credential patterns. The source manifest and its corruption control
are checked before publication. See the [machine-readable receipt](results/det5_pivot_public_validation.json).

## Partial Y certificates and conditional bounds — 2026-09-14

Scientific source: 2ae604dd301d1a572ed84eb3619c324385500f76.
Nine fresh public-copy audits passed. All 157 exported scientific files
match the committed source byte for byte after replay. These checks cover
30 base and 36 transferred scaled formulas, the reduced and enlarged inputs,
300 exact known-witness widths, 14 independently reconstructed full-matrix
inputs, the 69-assumption map, direction envelopes and the exact Y overlay.
The conditional input audit rejects four premise-corruption controls.

All **16 additional CPC proof payloads** were freshly checked with the pinned
Ethos kernel in the public copy: twelve old Y rectangles, two uniform-gauge
corner proofs, the original scaled proof and its slice. Every input/proof/
reference hash matches the original receipt. An unrelated assumption was
rejected as a negative control. The wrapper ran zero SMT solver queries.
These overlapping partial proofs do not exclude another whole class.

All 167 previously published certificate files remain byte-identical; the
previous public validation of 67 full-class proof payloads is retained.
The earlier baseline and complete-class checks were not rerun unchanged.
[The public replay receipt](results/public_det5_partial_validation.json)
distinguishes fresh kernel checks from arithmetic and premise audits.

Independent internal publication review confirmed the conditional theorem,
closed endpoints, 58-type count and old-region correction. Two presentation
findings were fixed: the stale publication footer and the cvc5 dependency of
--encodings. Python syntax, local Markdown links and privacy-pattern checks
pass. Manifest and deliberate hash-corruption checks are performed on the
final snapshot. This is AI-assisted internal review, not external human
peer review or an established mathematical priority claim.

## Stronger corner bounds and exact ordering — 2026-09-14

Export source: e42b25df01d966b7d7200dfff8391b962e35fdff. Public predecessor: 175896f.
The [incremental public-copy replay](results/public_det5_corner_validation.json)
passed all ten standard-library stages, three optional encoding audits and
both external-checker stages. Six CPC refutations were freshly checked:
three original corner proofs and their three actual reduced-assumption
statements. An unrelated assumption was rejected as a negative control.
These checks invoked zero SMT searches. The checker uses pinned Ethos commit
221641668d75eaffd308e0511d63962cea937110 and cvc5 signatures at
f3b21c4483d3b88dc63cb7cd3e5eb092eee5e341.

The exact stages reproduce the strict residual queues, height-ordering
identities, six saved linear assignments and their actual bodies. The
optional audits reconstruct nine coupled inputs, twelve Z branches and two
exact-product inputs; their recorded UNKNOWN outcomes remain unresolved.
All 197 previously published certificate files retain their SHA-256 values.
Of 98 selected source files, 96 match source bytes; NEXT.md and the research
status note have explicit public-snapshot wording. Archived inputs, proof
payloads and original receipts are restored after each replay command.

A fresh replay caught a tuple/list mismatch when comparing a computed
bounding box with its stored JSON. The source checker now builds JSON list
types directly; all six actual-body records reproduce unchanged. No numerical
result or mathematical claim was altered by this correction.

Independent internal publication review found no scope, endpoint, dependency,
link or privacy blocker. All 23 traced local module dependencies are present.
Python syntax, local Markdown links, oversized-file screening and private-path/
credential-pattern checks pass. Snapshot hashes and a deliberate manifest
corruption control pass. No full contact class or global bound is added;
external software checking is not external human peer review.

## Quantitative height separation and exact linear fibers — 2026-09-14

Scientific source: `5e1992205620baedeb150359451234e913fda78b`. All 69 selected scientific files match that
committed source byte for byte. All 206 previously public certificate
files are unchanged. The independent internal publication review found no
mathematical scope error; dependency documentation was corrected to include
Z3 in the default replay and cvc5 for encoding/proof checks.

The fresh public-copy replay passed **13 stages**:

- Seven exact symbolic, complete-witness, arithmetic and queue checks,
  including 158 fiber identities, 42 compact-chart identities, 2400 rational
  fixtures, both height-band constants and all inherited residual constraints.
- Four independent formula audits covering both eight-variable models,
  the implemented linear fiber compiler and all 84 rectangle assertions.
- Two fresh reference-bound Ethos checks of the fixed-height and continuous
  rectangle CPC refutations; unrelated false assumptions were rejected.

No SMT search was run. The wrapper preserves all original scientific inputs,
certificates and archived receipts; it writes its own
[public replay receipt](results/public_det5_fiber_validation.json).
The public CLAIM-0010 replay explicitly skips the unredistributed primary
article text; it verifies the arithmetic and local bindings. The original
primary-source review remains an archived, identified internal review.

The analytic bands prove a restricted strict bound near 3.39858129. The
separate rectangle excludes global width above 17/5 and adds area 1/32768
in the specified Y chart. The combined queue has 258 retained entries,
including 70 refined entries; their nonemptiness and full continuous coverage
are not claimed. The 58 necessary contact types and the global bound are
unchanged. Exact fixed-shape fibers do not settle the continuous shape domain.

Local Markdown links, Python syntax, privacy-pattern and oversized-file checks,
source-byte comparisons and the snapshot corruption control pass; see
[the publication receipt](results/det5_fiber_publication_validation.json).
Private operational history and third-party papers are excluded.
