# A continuous determinant-five box excluded using five lower-width directions

## Subsequent certification and corrected interpretation — 2026-09-14

The scaled box below lies in the old Y-only leaf r1111, already recorded
UNSAT. Its independent proof upgrades that label; it is not a newly discovered
excluded region. A reference-bound Ethos check of a 69-assumption dependency
slice shows that U restrictions and all additional lower-width clauses are
unused. All twelve old Y rectangles now have independently encoded cvc5
proofs checked with Ethos. The exact overlay covers one of the 259 joint
pending boxes completely and six halfway; archives are unchanged and no
clipped replacement queue is claimed.

A separate uniform-gauge refutation at beta=3/10, with no volume premise,
gives w(K)<=(10/7)(1+2/sqrt(3)) on the Y:[0,3] upper corner [3/4,1]^2.
See [conditional theorem](DET5_CONDITIONAL_WIDTH_BOUNDS.md),
[assumption audit](DET5_Y_HIGH_CYLINDER_EXCLUSION.md), and
[overlay](../results/det5_certified_y_overlay.json).
The older account below describes the formula as supplied, not the minimal
hypotheses of its proof. The 58-type count and global bound are unchanged.
The maintainer has authorized this checkpoint's GitHub publication.


Date: 2026-09-14. Status: one independently audited linear outer formula,
refuted by cvc5 and checked by the external Ethos proof checker. The geometric
reduction is a written internally reviewed argument. This result excludes
one continuous normalized-height box under the global-width target; it does
not exclude the determinant-five contact class or improve the global bound.

## Precise excluded configuration

Let K=conv(v0,v1,v2,v3) be a compact full-dimensional hollow real tetrahedron.
Its prescribed contacts are

    p0=0, p1=(5,1,2), p2=e2, p3=e3,

with p_i in the relative interior of the facet opposite v_i. Set Y=(0,1,0)
and U=(1,-1,-2), and normalize the four vertex heights separately in each
direction to lie between zero and one. Denote these heights by q_i and r_i.

There is no such K with **global lattice width w(K)>17/5** satisfying

    q0=r0=0,    q3=r3=1,
    q1,q2 in [3/4,1],
    r1,r2 in [1/2,1].

The intervals are closed. Ties with a designated maximum are included;
this is a continuous four-dimensional box, not a sampled fiber. Since Y and
U are nonzero and K is full-dimensional, both normalizations are defined.

The global-width hypothesis is essential to the necessary gauge and volume
cuts used in this proof. The result is **not** an infeasibility theorem from
five large directional widths alone, nor a claim that five covectors suffice
to compute every body's lattice width.

## Necessary outer formula and five lower-width tests

Assume such a global-target K exists. Its contact barycentric matrix F has
zero diagonal, positive off-diagonal entries, and column sums one. Define

    b=1/width(K,Y),    T_i=b(v_i-v0).

Then T0=0, T3,Y=1, and T_i,Y=q_i. The scaled reconstruction equations and
McCormick product envelopes in
[the scaled-frame proof](DET5_SCALED_VERTEX_HEIGHT_FRAME.md) are satisfied
by the exact products F_ij T_i,k. The specified q intervals tighten the two
free Y envelopes. With h_i=U dot T_i and D=h3-h0>0, the r intervals become

    D>(17/5)b,
    h0<=h_i<=h3,
    (1/2)D<=h_i-h0<=D    for i=1,2.

The independently reviewed
[pending-box transfer](DET5_SCALED_PENDING_TRANSFER_REVIEW.md) also retains
the complete observer guards, necessary lattice gauges, all directional
volume upper spans, and shared-product barycentric volume cuts. In particular,
for beta=183/500 the global-width hypothesis implies every required lattice
gauge exceeds beta and vol(K)<beta^(-3). Those necessary implications remain
premises even after some explicit lower-width clauses are removed.

The independently audited reduction deletes precisely twelve of the original
fifteen explicit lower-width clauses, keeping only

    Z=(0,0,1),    Y-Z=(0,1,-1),    (1,-2,-2).

For each of these three covectors u, the retained clause is

    OR over i<j and epsilon in {-1,+1}:
        epsilon * u dot (T_i-T_j) > (17/5)b.

Two further lower-width conditions remain without their redundant explicit
clauses: b<5/17 forces width(K,Y)>17/5, and the selected U-span inequality
forces width(K,U)>17/5. Thus the five lower-width directions are exactly

    (0,1,0), (0,0,1), (0,1,-1), (1,-2,-2), (1,-1,-2),

the complete covector list of contact width at most two, modulo sign.
Every other assertion is preserved. In particular, the formula still has
volume-derived **upper** span bounds in all fifteen directions; “five
lower-width directions” does not mean that every reference to other
covectors has been removed.

Since only constraints were deleted, every actual global-target body in
this box would satisfy the resulting weaker linear outer formula. A
refutation of that formula therefore proves the stated box exclusion.
Neither symmetry nor any previously recorded UNSAT label is required for
this standalone implication: the extrema and intervals are specified directly.

## Evidence and reproduction

The reduced [589-assertion input](../results/det5_scaled_leaf_contact_width_two.smt2)
has input SHA-256

    6f6c06f9445c9da6c7a857865ae5a9fe4b5e72bea3b636dc490fb44733813694.

cvc5 produced a complete internally checked proof with 10,233 proof nodes,
without a recorded admitted rule. The
[CPC proof](../certificates/det5_scaled_leaf_contact_width_two.cpc.gz) was
checked by pinned Ethos against the bound input assumptions. The
[external-check receipt](../results/det5_scaled_width_core_ethos_validation.json)
records success and rejection of an unreferenced assumption and a missing
refutation. External software checking is not external human peer review.

The new
[independent reduced-formula auditor](../tests/audit_det5_five_direction_box_independent.py)
reconstructs the already reviewed full transfer formula without discovery
imports, derives all fifteen lower-width clauses, and verifies that the
reduced formula is exactly its subset obtained by deleting the specified
twelve clauses. It confirms the preserved Y and U conditions and the exact
box, binds the existing proof receipts and rejects three mutations. The
[audit record](../results/det5_five_direction_box_encoding_validation.json)
distinguishes byte binding from actually rerunning a proof kernel.

Reproduce that audit with

    .venv/bin/python tests/audit_det5_five_direction_box_independent.py

using the existing Z3 dependency for syntax and rational polynomial comparison.
This command makes no solver query or proof-kernel call. The separate
[Ethos wrapper](../tests/check_det5_scaled_width_core_ethos.py) documents the
external-check path and required pinned checker sources; its existing receipt
is an archived completed check. For a fresh kernel replay without changing
the archived receipt, supply the pinned paths from
[the existing setup guide](HEIGHT_ETHOS_REPRODUCTION.md):

```sh
.venv/bin/python tests/check_det5_scaled_width_core_ethos.py \
  --ethos ETHOS/build/src/ethos --ethos-source ETHOS \
  --cvc5-source CVC5 --output /tmp/det5-scaled-box-ethos.json
```

This command runs Ethos and its two negative controls, with no SMT solver
query. The syntax adapters import the existing Z3/cvc5 Python dependencies.

The weaker attempt retaining only Z as an additional explicit width clause
returned UNKNOWN under its archived time limit. That outcome proves neither
feasibility nor impossibility and is not needed by this proof.

The box was selected from an inherited frontier, but its standalone exclusion
does not depend on the historical frontier's solver labels. A whole-class
cover would still require every remaining region and checked proof chains
for previously closed regions. The 58-type candidate count remains unchanged;
no mathematical priority claim is made for this box certificate.
