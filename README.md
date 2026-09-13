# Flatness-3D Lab

A reproducible research companion on the three-dimensional flatness constant,
hollow convex bodies, lattice contacts and exact width certificates,
maintained by [Njakasoa](https://github.com/Njakasoa).

**Status: exact reproductions and bounded computational exploration, internally
reviewed with AI assistance. No new global bound, solution of the flatness
conjecture, external peer review or journal/arXiv submission is claimed.**

## Verified baseline

The lab independently reconstructs the Codenotti–Santos tetrahedron in the
standard integer lattice and certifies:

- Lattice width **2 + √2**.
- Volume **2 + (4/3)√2**.
- Exactly four boundary lattice contacts and no interior lattice points.
- Seven primitive minimizing directions up to sign.
- Four affine lattice automorphisms, found by checking all 24 vertex permutations.

The width search has a proved finite coordinate bound. It is not an empirical
search radius. A separate SymPy implementation, importing none of the main
geometry engine, replays the result and rejects ten deliberate mutations.
The planar control certifies the Hurkens witness of width **1 + 2/√3**.

- [Baseline derivation](proofs/BASELINE_RECONSTRUCTION.md) and [exact certificate](certificates/codenotti_santos.json)
- [Complete width/hollowness algorithm](proofs/WIDTH_CERTIFIER.md) and [normalization](NORMALIZATION.md)
- [Independent replay](tests/independent_replay.py) and [planar reconstruction](proofs/FLATNESS_2D_RECONSTRUCTION.md)
- [Adversarial review](results/ADVERSARIAL_REVIEW.md) and [public validation](PUBLIC_VALIDATION.md)

![Exact baseline and truncation control](results/baseline_contacts.png)

## Known bounds and local optimality

The literature audit found the reference bounds

```text
2 + √2 ≤ Flt(3) ≤ 1 + 2/√3 + 2(3/4)^(1/3) < 3.972.
```

The upper radical expression and its volume consequences are replayed using
exact rational intervals. The local-maximality reconstruction checks the
rank-five gradient system, its three-dimensional kernel and a negative-definite
auxiliary Hessian at the exact parameter c = 1/100. These reproduce known
arguments of Averkov–Codenotti–Macchia–Santos, not new theorems. The published
explicit local-radius computation is not fully replayed.

See the [dated literature audit](STATE_OF_THE_ART.md), [upper-bound proof and
slack](proofs/UPPER_BOUND_SLACK.md), and [local-maximality reconstruction](proofs/LOCAL_MAXIMUM_RECONSTRUCTION.md).
Primary articles are [linked](papers/README.md), not redistributed.

## Finite contact enumeration and exploration

Using the known determinant cutoff for the tetrahedral contact branch, the lab
checks **3,268 ordered HNF candidates**, obtains **239 empty ordered tetrahedra**,
and reduces them to **37 affine-unimodular classes** of determinant at most 17.
The [completeness argument](enumeration/HNF_COMPLETENESS.md) and
[full output](results/empty_contact_tetrahedra.json) concern integer contact
tetrahedra. The surrounding real-body optimization, coplanar-square contacts,
and nonsimplicial contact branches remain unresolved.

A seeded asymmetric search records **25,265 numerical bodies/iterates**, including
425 directional estimates above 3.4. Iterates are correlated and the contact
families are incomplete. Eight selected reconstructions are rationalized while
preserving lattice contacts, then certified exactly; none exceeds 2 + √2.
The certificates refer to the rationalized bodies, not the original floats.

A separate exact truncation control produces a hollow body with five facets
and width above 3.4. Thus near-extremizer classification must distinguish
arbitrary bodies from maximal extensions. No universality is inferred from
contact signatures prescribed by the search model.

- [Discovery summary](results/discovery_summary.json) and [recorded dataset](results/near_extremizers.jsonl)
- [Eight exact reconstructions](results/certified_discovery_summary.json)
- [Truncation argument](proofs/TRUNCATION_OBSTRUCTION.md) and [certificate](certificates/truncated_delta.json)
- [Remaining degrees of freedom](results/DEGREES_OF_FREEDOM.md), [stop/pivot report](STOP_REPORT.md), and [next steps](NEXT.md)

![All minimizing directions and contact incidence](results/active_directions_contacts.png)

## Reproduce

Use Python 3.12 from the repository root. No account, API key, proprietary solver
or downloaded third-party paper is required:

```sh
python3 scripts/check_public_snapshot.py
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.lock
.venv/bin/python reproduce.py
```

The default replay executes 11 stages: environment checks, exact 3D and 2D
controls, upper-bound arithmetic, local Hessian, contact enumeration, truncation,
independent verification, ten tests, eight exact reconstructions and figures.
Run without Python `-O` or `-OO`, because certificates use assertions.

The core exact geometry uses only the standard library. SymPy supports the
independent checks; SciPy supports exploration; Matplotlib produces figures.
See [environment notes](ENVIRONMENT_AUDIT.md) and [locked dependencies](requirements.lock).
To regenerate the optional floating search as well:

```sh
OPENBLAS_NUM_THREADS=1 .venv/bin/python reproduce.py --discovery
```

Floating solver trajectories can vary across versions and platforms. Replays
refresh timings, environment reports and generated graphics, so check the
archived snapshot hashes **before** replaying. Exact scientific payloads are
compared separately in [PUBLIC_VALIDATION.md](PUBLIC_VALIDATION.md).

## Public snapshot, license and citation

This curated snapshot has a new public Git history. Operational settings,
session instructions, private notes, installed runtimes and third-party paper
copies are excluded. [SOURCE_MANIFEST.json](SOURCE_MANIFEST.json) records the
scientific source revision and hashes of all exported files. Historical reviews
remain dated records; GitHub publication is separately authorized and does not
establish mathematical priority or external peer review.

Project code and technical documentation use the [MIT license](LICENSE),
following the companion labs. See [rights and attribution](publication/RIGHTS.md),
[CITATION.cff](CITATION.cff), [publication record](PUBLICATION.md), and
[novelty log](NOVELTY_LOG.md).

Related laboratories: [Ihara A(2)](https://github.com/Njakasoa/ihara-a2-lab),
[Quantum Max-Cut](https://github.com/Njakasoa/quantum-max-cut-lab),
[Self-Avoiding Walk](https://github.com/Njakasoa/self-avoiding-walk-lab), and
[Tight Knots](https://github.com/Njakasoa/tight-knots-ropelength).
