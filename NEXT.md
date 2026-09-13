# Next scientific actions — continuous families

The 63 contact configurations and nine-template compression are internally
verified and published. External novelty is not established, and no global
flatness bound has improved.

1. Probe the determinant-two pair branch using the eight-parameter signed
   adjugate formulation in proofs/DET2_FINITE_ALGEBRAIC_REDUCTION.md. The first
   auxiliary-variable Z3 query timed out after 30 seconds; its positive
   control passed. Change the representation before spending more time on
   the same query.
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
```

Optional SMT: install experiments/requirements-smt.txt and run
`python -m experiments.det2_pair_smt`. This is a bounded experiment, not an
infeasibility certificate. See results/det2_pair_smt.json for the first result.
