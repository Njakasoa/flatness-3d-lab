# Independent review of the column-normalized pair model

Verdict: no critical mathematical error found in the formulation or identity
certificate. This review validates the chart and conditional necessary cuts;
it does not establish infeasibility, a new width theorem, or priority.
No solver was run.

## Chart and boundaries

The conversion F=diag(r)A, r=A^{-T}1>0 gives column sums one.
Conversely, r=F1 has strictly positive entries, A=diag(r)^{-1}F has row
sums one, and A^T r=1. These constructions are inverse. Row dominance
must be imposed across rows of F; an individual designated entry in a
column need not exceed one half. The column parameterization in the
identity generator has the correct designated locations.

Writing P for the permutation matrix of (01)(23) and J=diag(1,1,-1,-1),
JFPJ has positive diagonal, negative cross-part entries, and row surpluses
k_i>=0. Its graph is connected with strictly positive cross-part edges.
The stated rooted-forest determinant argument applies without requiring
row normalization. Since det(P)=1, det(F)>0 if some k_i>0. If all k_i=0,
the transformed matrix kills 1 and is singular. Column sums imply
sum(k_i)=2D-4, so D>2 is exactly the required strict condition.
Individual equality cases k_i=0 remain valid. Strict off-diagonal
positivity is essential to this argument and to the designated relative
interior contacts; it must not be weakened silently.

Column stochasticity makes F an affine bijection of the sum-one
hyperplane when invertible. Thus F lambda>=0 is a bounded simplex with
vertices F^{-1}e_j. Boundedness needs no extra inverse-column conditions.
The restriction determinant on the zero-sum subspace equals det(F), so
physical volume is 1/(3 det(F)). Adjugate entries have degree at most
three, column differences degree at most two, and dividing width
numerators by the positive determinant preserves inequality orientation.
The stated homogeneous domain bounds consequently have the right signs.

## Gauge signs and cuts

For e_X, F ell(e_X)=(k_0,k_1,-k_2,-k_3)/2. Its positive-part sum is
(k_0+k_1)/2. Column sums give k_0+k_1=k_2+k_3=D-2, proving gamma_X=D/2-1.
Zeros on the dominance boundary cause no problem.

For e_Y, the four entries are
(F_02, F_12-F_10, -F_20, F_32-F_30).
Their signs are respectively positive, negative, negative, positive:
row 1 gives F_10>=F_12+F_13 and row 3 gives F_32>=F_30+F_31.
Thus gamma_Y=F_02+F_32-F_30.

For e_Z, the entries are
(F_03, F_13-F_10, F_23-F_20, -F_30).
Rows 1 and 2 similarly give signs positive, negative, positive, negative,
proving gamma_Z=F_03+F_23-F_20.

The arithmetic converting the stated volume bound into
 det(F)>50653/3183624 and gamma_X>37/102 into D>139/51 is correct.
These conclusions are conditional on the previously established ACMS
implications for genuinely hollow bodies of width greater than 17/5.
This review does not independently reprove that external geometric input.
The text correctly warns that target-specific cuts may reject nonhollow
partial-box assignments or controls at other thresholds.

The symmetry group acts by simultaneous permutation of rows and columns,
so canonical ordering must use F entries, not row-normalized A entries.
Choosing a maximal designated entry first and ordering the remaining
pair gives the claimed weak canonical inequalities, including ties.
As with previous models, this is necessary up to lattice equivalence;
the finite exclusion box itself need not be symmetry invariant.

## Independent computation and coverage limits

A separate inline SymPy calculation using `.venv/bin/python` reconstructed
F explicitly as

    [[0, c1, d2, d3],
     [c0, 0, 1-c2-d2, 1-c3-d3],
     [d0, d1, 0, c3],
     [1-c0-d0, 1-c1-d1, c2, 0]].

It did not import or run the generator. It decoded the saved certificate
and checked the determinant polynomial, cubic determinant degree, all
24 quadratic adjugate column differences, all 18 saved axis-width
numerators, the three coordinate gauge polynomials, the exact sample
determinant and gauges, sample physical volume via vertex differences,
and determinant-cut arithmetic. All checks passed. The default system
Python lacks SymPy; the repository virtual environment provides it.

The generator's gauge checks alone verify the selected positive-row sums,
not their signs throughout the domain. The sign proof above supplies that
missing interpretation. The independent computation covers the identity
certificate, not implementation of all 37 directions, all domain bounds,
176 removed tautologies, or a future solver encoding. Those encodings
still require integration checks before interpreting solver outcomes.
