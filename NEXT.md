# Next scientific actions — continuous families

Public checkpoint: source revision 38fbeef. These next steps describe this
reviewed snapshot; ongoing local experiments are outside this release.

The 63 contact configurations and nine-template compression are internally
verified and published. The active objective remains a verified research
breakthrough. External novelty is not established, and no global flatness
bound has improved.

1. Implement the thirteen-variable cubic formulation in
   proofs/PAIR_CUBIC_FORMULATION.md. The eight-variable adjugate query and
   its structure-assisted version both returned UNKNOWN under a 30-second
   limit. Their positive and negative pinned controls passed. Do not repeat
   the same degree-six queries unchanged. The new formulation keeps four
   inverse-column-sum variables and one determinant variable; eighteen exact
   complementary-minor identities reduce all width constraints to degree three.
2. Keep equality A_i,sigma(i)=1/2. Finite two-roof slopes omit these vertical
   facet limits. Preserve the 37 complete width directions and proved
   coordinate bounds. The 216 lattice exclusions are only a necessary
   relaxation. SAT requires exact hollowness checks or additional lattice
   cuts; UNSAT requires review of the encoding and solver evidence.
3. Preserve the exact four-contact index-two witness of width >13/4 and its
   open neighborhood. It disproves early unimodularity assumptions and
   prevents pruning all non-unimodular contacts at that threshold. The
   six-contact witness near 3.28338 has no local or global optimum certificate.
4. For the cube class, use Lassak's necessary mixed width/chord inequalities.
   Do not invoke the conjectured sum of inverse axis widths as a theorem.
   At width >=2+sqrt(2), every axis requires a_i<=1+sqrt(2) and W_i/a_i>=sqrt(2).
5. Continue the priority audit beyond the checked primary sources. Howe's
   eight-point extension principle is already known; the finite list under
   the stated width threshold is the proposed refinement. Extra template
   vertices need not belong to the surrounding body.

Replays:

```sh
python3 reproduce.py
python3 reproduce_contact_reduction.py
python3 -m experiments.certify_det2_cycle
python3 -m experiments.certify_det2_four_contacts
python3 tests/replay_det2_cycle_independent.py
python3 -m experiments.det2_finite_domain
python3 -m experiments.pair_matrix_structure
python3 tests/replay_pair_matrix_independent.py
python3 -m experiments.pair_cubic_width_identities
```

Optional SMT: install experiments/requirements-smt.txt and run
`python -m experiments.det2_pair_smt`. This is a bounded experiment, not an
infeasibility certificate. See results/det2_pair_smt.json for the first result.

The pair matrix identities identify the simultaneous half-coefficient case
as the only singular boundary; all other equality cases remain included.
Inverse column sums must still be positive. Eight centralizer symmetries
allow a0 to be maximal and a2>=a3 for genuine bodies up to affine lattice
equivalence. This does not imply equivalence for arbitrary nonhollow points
in a fixed partial-box relaxation.
