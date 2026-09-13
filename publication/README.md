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
