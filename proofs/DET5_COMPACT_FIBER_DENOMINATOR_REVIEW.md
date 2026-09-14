# Endpoint-safe polynomial coefficients for compact shape fibers

Status: independent algebraic derivation and additional necessary shape cuts.
This note neither records a solver refutation nor proves a continuous cover.
It does not modify the stored coefficient certificate or earlier proof files.

Use the [compact shape chart](DET5_COMPACT_SHAPE_CHART_REVIEW.md), with

    L=1-p*q>0, eta=1-q,
    x=p*eta/L, y=eta/L, d=(1-p)*eta/L,
    A=C+p*E, B=q*C+E, S=C+E,
    b=h-x-d*t>0, T=t/b, H=h/b, rho=1/b.

Here `H` is the projective fiber variable. All polynomial matrices below use
another symbol to avoid confusing it with a matrix name. The actual shape
domain has `0<=p,q<1`, `C,E>0`, `C+E<1`, and `0<r,u<1`.
The previously proved target-domain bound `L>49/1500` is common to both
height orders, with a stronger bound in the reverse order.

## One positive multiplier clears the scaled contact matrix

Let `M=F/b`. In canonical low/high ordering, `L*M` has columns

    col0 = L*(0, rho-T+q*C*rho, T-C*rho, eta*C*rho),
    col1 = (L*(rho-H)-q*(1-p)*r*rho,
            0, L*r*rho, L*H-eta*r*rho),
    col2 = (L*(rho-H)-(1-p)*u*rho,
            L*u*rho, 0, L*H-p*eta*u*rho),
    col3 = L*((1-p)*E*rho, rho-T-E*rho, T+p*E*rho, 0).

Each coefficient is a polynomial in the six compact shape parameters, and
each entry is linear in `(T,H,rho)`. No division by `p`, `q`, `1-p`,
`1-q`, `x`, or `y` is needed. In particular the formulas are regular at the
actual tied-extremum endpoints `p=0` and `q=0`.
The height identity has the polynomial form

    L*H-p*eta*rho-(1-p)*eta*T-L=0.                    (1)

The common multiplier `L` is sufficient; a higher common power is valid but
unnecessary. The naturally polynomial columns 0 and 3 need not be multiplied
by `L` for standalone entry positivity conditions. Avoiding a needless
positive factor can reduce interval overestimation. A guard or gauge that
combines several columns may use the displayed common multiplier directly.

## The same multiplier clears every vertex-pair numerator

This conclusion is derived from the matrix geometry independently of any
symbolic cancellation in the stored coefficient file.
Let `J=[e1-e0,e2-e0,e3-e0]`. Column stochasticity gives `F J=J G`, where

    G = [ t-1-q*C,        u+t-1-q*C,       -B      ]
        [ r-t+C,          -t+C,            A      ]
        [ h-y*r-eta*C,    h-x*u-eta*C,      -eta*C ].

Only the third row has coefficients with denominator `L`. Set
`Q=diag(1,1,L)` and `Gbar=Q G`. Its polynomial third row is

    (L*h-eta*r-L*eta*C,
     L*h-p*eta*u-L*eta*C,
     -L*eta*C).

The other rows are unchanged. The adjugate product identity proves

    adj(Gbar)*Q = L*adj(G).                           (2)

Indeed `adj(Gbar)=adj(G)*diag(L,L,1)`; multiplication by `Q` gives (2).
This identity also follows as a polynomial identity, without assuming
invertibility of any individual evaluation used for coefficient extraction.

Both variable parts of `Gbar` have a common right factor:

    Gbar(t,h)=Gbar(0,0)+(t,-t,L*h)^T*(1,1,0).

Thus every two-by-two minor of `Gbar` is jointly affine in `(t,h)`.
The two-update terms vanish because the updated columns are parallel.
Consequently every entry of `adj(Gbar)*Q` is jointly affine in `(t,h)`,
with polynomial shape coefficients.

Let the physical contact columns be
`P=[0,(5,1,2),(0,1,0),(0,0,1)]`. Then

    P J = [ 5,0,0 ]
          [ 1,1,0 ]
          [ 2,0,1 ].

For a vertex-index pair `(i,j)`, write `ei-ej=J*z_ij`; equivalently use
`z_0=0`, `z_1=(1,0,0)`, `z_2=(0,1,0)`, `z_3=(0,0,1)` and
`z_ij=z_i-z_j`. The exact pair numerator is

    N_ij(t,h)=P*adj(F)*(ei-ej)=P*J*adj(G)*z_ij.

Equation (2) gives its denominator-free representation

    n_ij(t,h):=L*N_ij(t,h)
             =P*J*adj(Gbar)*Q*z_ij.                  (3)

All eighteen scalar coordinate-pair numerators therefore need only the
same positive multiplier `L`. Their affine coefficients can be extracted
without derivatives or inadmissible divisions:

    n0=n(0,0), nt=n(1,0)-n0, nh=n(0,1)-n0,
    n(t,h)=n0+nt*t+nh*h.

The three evaluation points need not satisfy the geometric chart domain;
this is extraction of polynomial coefficients, not construction of bodies.
The cleared projective numerator is then

    nhat_ij = n0*rho+nt*T+nh*H = L*N_ij/b.             (4)

This is the quantity to compare with the corresponding stored-certificate
coefficient after substitution and multiplication by `L`. In particular,
substituting `c=C*L/(1-p)` and `e=E*L/(1-q)` into expanded coefficients may
introduce apparent poles at `p=1` or `q=1`. Formula (3) proves that these
poles cancel in every complete coefficient; evaluating uncancelled pieces
separately by interval division is unnecessary and can be invalid on a
box touching those faces.

## Reverse order and complete width atoms

Let `S12` swap indices 1 and 2 and let `sigma` be that permutation. For the
reverse original order `F_actual=S12*F*S12`. One must therefore use

    L*Nactual_ij = P*S12*J*adj(Gbar)*Q*z_sigma(i),sigma(j).

The physical prefactor is now

    P*S12*J = [ 0,5,0 ]
              [ 1,1,0 ]
              [ 0,2,1 ].

This handles both the physical coordinate columns and the vertex-pair
permutation. It preserves the same positive multiplier and affine fiber
structure. Merely swapping the height labels in a physical directional
numerator would not be sufficient.

For a determinant sign `s` and a target width `W`, the exact directional
pair disjunction can be written

    OR over i<j and epsilon in {-1,+1}:
        epsilon*nhat_ij - W*L*s*D > 0,
    D=u*A-r*B,             s*D>0.                      (5)

Here `nhat` is the scalar dot product of (4) with the physical covector.
The factor `L` on the determinant term is essential: omitting it would
change the width target. The original difference is `N_ij/(b*D)`.
The matrix identities do not supply the completeness of the fifteen
covectors; that remains the earlier complete-direction lemma.

Gauge subset atoms can use `subset(L*M*ell)-beta*L*rho>0` and observer
atoms can use a coordinate of `L*M*ell<=0`. Preserve their Boolean trees.
The simple determinant-volume atom `s*D-rho/M0>0` is already polynomial
and need not be multiplied by `L`. Multiplication is optional there;
leaving it unscaled often gives a tighter interval enclosure.

All these polynomial coefficients extend to boxes touching `p=1` or
`q=1`, even if those faces do not represent actual chart points. An outer
model may contain such spurious points. Soundness requires only that the
actual points satisfy the established positive-`L` domain and map into the
outer model. No division on a box whose denominator interval meets zero
is involved in formulas (1)--(5).

## Additional low-degree shape cuts

The following cuts follow directly from the same exact chart and necessary
conditions. They are useful before generating all width disjunctions, but
are not independently sufficient for geometric feasibility.

Write `k=3` in the direct branch and `k=2` in the reverse branch. The first
observer alternative has already been proved impossible, leaving

    k*u <= B.                                         (6)

Since `A,B,r>0`, this yields the unconditional strict bound

    D=u*A-r*B < A*B/k.                                (7)

Under the true global target `w(K)>17/5`, the established volume argument
uses `M0=50000000/2042829` and gives

    |D| > rho/M0 > deltaD,
    deltaD=34728093/250000000.

Thus the positive determinant branch necessarily has

    A*B > k*deltaD,           S^2 > k*deltaD.           (8)

The second follows from `A,B<=S`. In exact rational form, the two right
sides are `104184279/250000000` for the direct branch and
`34728093/125000000` for the reverse branch. These are only positive-sign
cuts; applying them to the negative determinant branch is unjustified.
The gauge of `(0,0,1)` is exactly `S` in both branches, so the full ACMS
necessary minimum bound also gives `S>183/500`.

There is a further endpoint separation from the true global volume bound.
Since `h=x+d*t+b<1` with `d*t>0`, we have `1-x>b>1/M0`. Consequently

    M0*(1-p) > L.                                     (9)

This is another low-degree polynomial shape cut. Combined with the common
positive lower bound on `L`, it separates `p` from 1 uniformly on actual
target geometries. There is no corresponding conclusion about `q=1`
from this argument. Neither (8) nor (9) should be inferred from a finite
list of gauge inequalities alone: their determinant/gap margins use the
true hollow-body global-width hypothesis.

No solver query was made for this derivation. A compiler audit should still
check the emitted coefficients and logical implications against these
identities; the existence of a stable polynomial formula does not certify
an implementation or a resulting cover.
