# Enlarged Y corner and improved conditional width bounds

This supplements the immutable [earlier conditional bounds](DET5_CONDITIONAL_WIDTH_BOUNDS.md).
The word "sharp" in this filename identifies the archived threshold probe;
neither optimality of that threshold nor optimality of a geometric bound is
asserted. The conclusions concern specified height subdomains of one contact
class. They do not bound the unrestricted constant Flt(3) or remove an entire
contact class.

## Hypotheses and conclusions

Let K be a full-dimensional hollow real tetrahedron with ordered vertices
v0,...,v3. Assume the lattice contacts

    p0=(0,0,0), p1=(5,1,2), p2=(0,1,0), p3=(0,0,1)

lie in the relative interiors of the facets opposite the corresponding
vertices. No maximality or volume hypothesis is required. Set Y=(0,1,0) and

    q_i = (Y(v_i)-min_j Y(v_j))/w_Y(K),
    A = 1+2/sqrt(3).

Assume v0 attains the minimum and v3 the maximum of Y, so q0=0, q3=1.
The extrema need not be unique. The following are bounds on the full lattice
width w(K); Y need not be a minimizing direction.

| Condition on the actual free heights (q1,q2) | Conclusion |
|---|---|
| [3/5,1]^2 | w(K) <= 17/5 |
| [12/17,1]^2 | w(K) <= (102/65)A, approximately 3.3812223833 |
| [3/4,1]^2 | w(K) <= (23/19)A, approximately 2.6083217044 |

All square boundaries are included. The second conclusion fills the cross
strips missing between the older separately certified squares. The last
conclusion improves the earlier (10/7)A bound on the same upper corner.

## Necessary model for actual tetrahedra

Let F_ij be the barycentric coordinate of p_j at v_i. Then each column sums
to one, F_ii=0, and every off-diagonal entry is strictly positive. Write
b=1/w_Y(K)>0 and a=-min_i Y(v_i)/w_Y(K). Contact containment implies a>=0
and a+b<=1, and exact contact reconstruction gives

    F^T q = a*1+b*(0,1,1,0).

For q=(0,x,y,1), contact column zero is a convex combination of x,y,1,
so a>=min(x,y). Column one gives a+b<=1-F01<1. Consequently

    b < 1-min(x,y).                                      (1)

Thus min(x,y)>=12/17 forces b<5/17, including equality at 12/17;
min(x,y)>=3/4 forces b<1/4 and w_Y(K)>4. In contrast, min(x,y)>=3/5
only forces w_Y(K)>5/2, which does not remove the model's width premise.

The ten integer test vectors are

    V = {(0,0,1),(0,1,-1),(0,1,0),(1,0,0),(1,0,1),
         (2,0,1),(3,0,1),(5,0,2),(5,1,1),(5,1,2)}.

For ell_P(u)=(2u_X/5-u_Y-u_Z,u_X/5,u_Y-u_X/5,u_Z-2u_X/5), their actual
difference-body gauges satisfy gamma_(K-K)(u)=||F ell_P(u)||_1/2.
The checked inputs assert all ten gauges > beta, the necessary non-interior
conditions for twenty fixed integer guards, 0<b<5/17, the stated height
square, and McCormick envelopes for six products q_i F_ij in the contact
equations. They have exactly 22 real variables and no volume assumptions.
An actual hollow tetrahedron meeting the other premises satisfies every
guard condition. This uses only necessity of those conditions; lowering
beta requires no guard-completeness theorem. Its exact products satisfy
all McCormick envelopes, also on the closed box boundaries.

The archived refutations, each already checked by Ethos, are:

| Free-height square | Uniform beta | Existing receipt |
|---|---|---|
| [3/4,1]^2 | 4/23 | [threshold probe](../results/det5_y_corner_gauge_sharp_probe.json) |
| [2/3,1]^2 | 37/102 | [first enlargement](../results/det5_y_corner_enlarged.json) |
| [3/5,1]^2 | 37/102 | [final certified enlargement](../results/det5_y_corner_enlarged_3_5.json) |

Whenever b<5/17 holds, the applicable refutation therefore implies

    min_{u in V} gamma_(K-K)(u) <= beta,
    lambda_1(K-K) <= beta.                              (2)

The conclusion is non-strict because the refuted gauge conditions are strict.

## Converting the certificates into the stated bounds

Use the established ACMS inequality, in the same normalization as the
[earlier proof](DET5_CONDITIONAL_WIDTH_BOUNDS.md),

    lambda_1(K-K) >= 1-A/w(K).

Together with (2), this gives w(K)<=A/(1-beta). By (1), b<5/17 is automatic
on [12/17,1]^2 and on [3/4,1]^2. Apply the final enlargement certificate to
the former and the 4/23 certificate to the latter. The exact coefficients
are 1/(1-37/102)=102/65 and 1/(1-4/23)=23/19, respectively. This proves
the second and third conclusions.

For the first conclusion, argue by contradiction. If w(K)>17/5, then
w_Y(K)>=w(K)>17/5, so b<5/17. Also A<13/6, since 4/3<49/36, and hence

    lambda_1(K-K) >= 1-A/w(K)
                   > 1-5A/17 > 37/102.

Every gauge in V would exceed 37/102, contradicting the checked [3/5,1]^2
refutation. Thus w(K)<=17/5 on the whole enlarged square. Merely applying
A/(1-beta) everywhere on this square would omit a necessary premise;
the stronger (102/65)A assertion is restricted as stated above.

## Independent replay and limits of the SAT probe

Run `python3 tests/replay_det5_y_corner_supplement.py`.
The standard-library-only auditor uses an independent full-matrix builder
and exact rational Gaussian barycentrics to reconstruct every assertion of
all four new inputs. For the three refutations it verifies the input,
compressed CPC, and uncompressed CPC hashes and binds the successful
existing cvc5/Ethos receipts. This is an independent encoding and receipt
audit, not a fresh solver run or a proof-kernel rerun.

The [11/20 probe](../results/det5_y_corner_enlarged_11_20.json) has a saved
rational SAT assignment. Exact substitution verifies all 82 assertions and
all 22 assigned variables. All six lifted products differ from q_i F_ij,
so this assignment does not witness an actual tetrahedron. It neither
disproves a geometric bound on that larger square nor establishes that 3/5
is an optimal domain endpoint. Similarly, no optimality claim follows from
the separate strict optimization experiment.

The [supplement validation receipt](../results/det5_y_corner_supplement_validation.json)
records the four inputs, the three proof bindings, the exact SAT check,
the rational constant checks, and three rejected corruption controls.
Old proof inputs, archives, and conditional-bound receipts remain unchanged.
