# Review of pending-chart transfer to the complete scaled frame

Date: 2026-09-14. Status: independent internal mathematical review of
[the transfer encoder](../experiments/det5_scaled_pending_transfer.py).
The additional constraints are necessary for an actual hollow global-target
tetrahedron in the selected inherited chart. This review does not certify
solver answers or establish a complete exclusion cover.

The base construction is described in
[the scaled frame proof](DET5_SCALED_VERTEX_HEIGHT_FRAME.md). Write
W=17/5, beta=183/500, R=6/(5 beta^3), and

    b=1/width(K,Y),   T_i=b(v_i-v_L),
    T_L=0,   T_H,Y=1,   0<=T_i,Y<=1.

In an actual body the lifted variable w(i,j,k) equals F_ij T_i,k. The
encoder's linear relaxations need only contain this exact lifted assignment;
the reverse implication is not asserted for an arbitrary relaxed solution.

## 1. Transfer of the two free Y intervals

The first two inherited box intervals constrain the free normalized
Y-heights in increasing vertex-index order. Those heights are exactly
T_i,Y, because the same extrema L,H are used in both formulations.
For 0<=f=F_ij<=1, t in [lo,hi], and w=f t, the inequalities

    w>=lo*f,   w<=hi*f,
    w>=t+hi*f-hi,   w<=t+lo*f-lo

are the four valid McCormick inequalities on [0,1] x [lo,hi]. The encoder
uses precisely these signs and endpoints and the existing w(i,j,1) variable.
The diagonal products are skipped because F_ii=0. Free-height indices omit
L and H, so every referenced non-diagonal product is a lifted variable in
the base construction. No second independent copy of a product is created.
Keeping the previous, weaker envelopes alongside the tightened ones is valid.

## 2. Transfer of the two free U intervals

Set h_i=U dot T_i with U=(1,-1,-2), and let A,B be the inherited U minimum
and maximum indices. Then

    D=h_B-h_A=b*width(K,U)>W*b>0.

The encoder imposes this positive span and h_A<=h_i<=h_B for all vertices.
The normalized U-height is exactly (h_i-h_A)/D; the translation by v_L
cancels in this difference. Thus its membership in [lo,hi] is equivalent to

    lo*D <= h_i-h_A <= hi*D.

These are linear because lo and hi are inherited rational constants.
The implementation uses the two complementary U indices in increasing order,
matching the old box convention. It neither divides by a variable of unknown
sign nor confuses the U reciprocal gap with b, the Y reciprocal gap.
Tied extrema are retained because the non-extremal bounds are weak.

## 3. Volume-derived spans for every listed covector

For hollow global-target K, the established volume necessity gives
vol(K)<beta^(-3). Since vol(P)=5/6, the nested-tetrahedron inequality gives

    width(K,u)<R*width(P,u).

Every scaled pair difference therefore satisfies

    |u dot (T_i-T_j)|<R*width(P,u)*b.

The encoder computes width(P,u) from the supplied contact coordinates and
adds both signs for all six vertex pairs and all fifteen listed covectors.
The strict inequality follows from the strict volume bound. This is necessary
even when the selected pair is not extremal. It adds redundant directional
information consistently to the coordinate spans already in the base model.
These linear consequences are not claimed equivalent to the whole volume
inequality.

## 4. Barycentric volume cuts share the reconstruction products

Put C=sum_i F_i0 T_i and D_i=T_i-C. Exact contact reconstruction gives
D_i=b v_i, since p0=0. In the relaxed system the encoder defines C from the
same column-zero lifted products already used by reconstruction. The special
cases are handled identically to the base model: diagonal or row-L products
are zero, and the Y product at row H equals F_Hj.

The displayed four coordinates in the encoder are precisely

    b*lambda_P(v_i) =
    (b+2D_i,X/5-D_i,Y-D_i,Z,
     D_i,X/5,
     D_i,Y-D_i,X/5,
     D_i,Z-2D_i,X/5).

They sum to b. For a simplex P,
vol(conv(P,v_i))/vol(P)=sum_j max(lambda_P(v_i)_j,0).
Containment conv(P,v_i) subset K and the strict volume necessity give a
positive-coordinate sum less than R. Every subset sum is at most this
positive sum. Multiplication by b>0 proves the fifteen imposed nonempty
subset inequalities, each with upper bound R*b. The full subset is redundant
but valid because R>1. Relaxing the shared products can weaken these cuts,
but cannot discard an exact target assignment.

## Symmetry, coverage and inherited status

No additional symmetry quotient is used. A hypothetical global-target K can
first be transformed by a contact automorphism to one of the existing three
Y representatives. Global lattice width, hollowness and the necessary volume
bound are preserved. The transformed body's actual U extrema are among all
twelve ordered pairs; its normalized free heights belong to a box in the
inherited chart decomposition. The transfer retains those specific Y/U
extrema and imposes every one of the fifteen width conditions. It does not
assume that K itself is symmetric or that U is fixed by each automorphism.

The driver starts only from pending leaves of the frozen 953-query archive.
This is a valid way to strengthen the unresolved portion of that campaign,
conditional on its frontier accounting. The omitted closed portions rely on
previous recorded UNSAT labels, which presently have encoding/frontier audits
rather than external proof-kernel certification. New refutations on pending
leaves, even if checked, would not by themselves certify the inherited closed
portions or establish a full class exclusion.

The source path, byte hash and query count are recorded, and an existing
transfer archive rejects a changed source hash. These are provenance checks,
not a substitute for verifying inherited solver answers. SAT solutions of
the outer model must likewise be reconstructed and checked as actual bodies;
the exact scaled-frame rank proof does not apply to arbitrary lifted SAT
assignments whose product identities are relaxed.

No mathematical correction to the added constraints was identified in this
review. No solver query or previous file was rerun or modified for it.

## Independent encoding and saved-assignment audit

The separate
[transfer auditor](../tests/audit_det5_scaled_pending_transfer_independent.py)
reuses the independent base-frame reconstruction, then derives all additional
assertions without importing discovery code. In particular it computes the
contact barycentric coefficients by Gaussian inversion rather than copying
the encoder's explicit coordinate formula. Canonical rational polynomial
comparison matches all 36 archived input formulas, and each input is bound
to its exact inherited pending leaf and byte hash.

The [receipt](../results/det5_scaled_pending_transfer_validation.json) also
checks the 14 full saved rational SAT assignments against every assertion,
including their original shared product variables. Every one has a nonzero
product residual; the independent actual-F reconstruction passes none of
the complete fifteen-direction width targets. Six mutations of source-box
binding, the four additional constraint groups, and a saved SAT gap are
rejected. No solver query is issued.

The recorded status distribution is 21 UNKNOWN, 14 SAT and one UNSAT. The
one UNSAT label is not proved by this encoding audit; the earlier caveats
about inherited and new proof-kernel checking remain unchanged.
