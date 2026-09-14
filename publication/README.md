# Public research companion

The baseline and internally verified contact reduction are published on
[GitHub](https://github.com/Njakasoa/flatness-3d-lab) with the maintainer's
explicit authorization. The public snapshot includes complete written proofs,
exact certificates, independent checkers, figures and bounded exploration.

The structural result gives 63 necessary contact configurations above
(11/7)(1+2/sqrt(3)), compressed into nine templates. It does not improve the
global flatness bound or optimize every surviving continuous family.
External mathematical priority remains unverified.

- [Main result and scope](../claims/CLAIM-0004.md)
- [Complete proof](../proofs/CONTACT_HULL_FINITE_REDUCTION.md)
- [Validation and review](../results/CONTACT_REDUCTION_VALIDATION.md)
- [Public-copy validation](../PUBLIC_VALIDATION.md)
- [Publication record](../PUBLICATION.md) and [rights](RIGHTS.md)

From the repository root, install the pinned dependencies and run:

```sh
python scripts/check_public_snapshot.py
python reproduce.py
python reproduce_contact_reduction.py
```

No journal/arXiv submission or external peer review is claimed.

The subsequent CLAIM-0005 supplies a reviewed boundary-contact observer-line
criterion and conditional finite guard sets. The public companion includes
proofs, exact data, figures and independent replay. Run
`python reproduce_observer_guards.py` from the repository root with the
baseline dependencies. No manuscript submission or novelty claim is implied.

## Tetrahedral containment bounds

[CLAIM-0006](../claims/CLAIM-0006.md) and its linked proofs now exclude two
full tetrahedral contact classes at width at least 2+sqrt(2), leaving 61
necessary full contact hulls. At the lower original threshold, 62 remain.
These bounds assume a tetrahedral surrounding body; the global conjecture
and optimization of the surviving types remain open.

Run `python reproduce_contraction.py`, followed by
`python -m experiments.weighted_two_vector_bounds` and
`python -O tests/replay_weighted_trace_independent.py`. The optional Z3
encoding audit `python tests/audit_nonunimodular_encoding.py` runs no solver.
The written proofs and exact artifacts are the publication deliverable for
this update; no separate manuscript or external review is claimed.

## Current result: 58 necessary candidate contact configurations

[CLAIM-0007](../claims/CLAIM-0007.md) and
[CLAIM-0008](../claims/CLAIM-0008.md) add three facet-contact exclusions.
Their hypotheses are narrower than the preceding containment bounds.
The public snapshot includes 67 CPC refutations, independent encoders,
complete covers and fresh external Ethos receipts. See the
[latest validation](../PUBLIC_VALIDATION.md) and
[checker setup](../proofs/HEIGHT_ETHOS_REPRODUCTION.md).

```sh
python reproduce_height_cover.py
python reproduce_det5_class4.py
python tests/replay_det5_height_witness_independent.py
```

The first command needs the optional pinned Z3 and cvc5 Python packages.
These default replays audit archived data and proof bindings. Actual proof
kernel replay requires Ethos and the pinned signatures.

## Height-region bounds and exact ordering

[CLAIM-0009](../claims/CLAIM-0009.md) now proves the bound (102/65)(1+2/√3)
on the specified [3/5,1]² actual-height region and (23/19)(1+2/√3) on its
[3/4,1]² subregion, with no preliminary large-width hypothesis. It includes
six new proof payloads (three originals and three reduced statements), the
[ordering lemma](../proofs/DET5_Y_CORNER_ANALYTIC_PROBE.md), and the exact
258-entry residual queue. All chart/contact hypotheses remain essential.

```sh
python3 reproduce_det5_corner.py
.venv/bin/python reproduce_det5_corner.py --encodings
```

The default performs ten standard-library checks; `--encodings` adds three
Z3-based input audits without invoking an SMT search. Add the three pinned
external-checker path flags described in the main README to freshly check
all six proofs. The wrapper preserves archived inputs, certificates and
original receipts. See [public validation](../PUBLIC_VALIDATION.md).
