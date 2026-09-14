# Independent review of the eight-parameter ordered height chart

Status: exact change of coordinates and rank characterization. This reduces
the search formulation; it proves no new width exclusion. The chart formula
was proposed by the root agent and independently checked here.

Let q=(0,x,y,1), H=(0,1,1,0), and suppose F has zero diagonal,
positive off-diagonal entries, column sums one, and
F^T q = a 1 + b H, with b>0. On the branch x<y, the
[height-order lemma](DET5_Y_CORNER_ANALYTIC_PROBE.md) gives x<a<y.
Define

    d=y-x, t=(a-x)/d, h=a+b,
    c=F30/d, e=F03/d, r=F21, u=F12.

The eight parameters are (x,y,t,h,c,e,r,u). Solving the two linear
equations in each column gives exactly

    F = [ 0,                 1-h-(1-y)r,  1-h-(1-x)u,  d e       ]
        [ 1-t+(1-y)c,        0,            u,            1-t-y e   ]
        [ t-(1-x)c,          r,            0,            t+x e     ]
        [ d c,               h-y r,        h-x u,        0         ].

All entries are polynomials of degree at most two. Conversely, the matrix
displayed above has the required column sums and height equations with
a=x+t(y-x) and b=h-a. Recovering the eight parameters by their definitions
shows that this is a bijection, not only an implication between models.

## Exact domain, including tied extrema

The complete domain is

    0 <= x < y <= 1,  0<t<1,  h>x+t(y-x),
    c>0, e>0, (1-x)c<t, y e<1-t,
    r>0, u>0,
    h-y r>0, 1-h-(1-y)r>0,
    h-x u>0, 1-h-(1-x)u>0.

The two omitted off-diagonal positivity conditions are automatic:
1-t+(1-y)c>0 and t+x e>0. The displayed conditions also imply
0<h<1. Both x=0 and y=1 are allowed, separately or simultaneously;
the selected minimum or maximum vertex need not be unique.

The transformation divides only by d>0. The useful auxiliary bounds
c<t/(1-x) and e<(1-t)/y also have strictly positive denominators,
because x<y<=1 and 0<=x<y. They do not give uniform bounds on c,e
over the whole domain: no constant bound such as c,e<=1 may be added.

For the branch in which the original q1>q2, construct the displayed
matrix using the lower height x and upper height y, then conjugate it
by the permutation matrix swapping indices 1 and 2. The original normalized
height vector is then (0,y,x,1). Both rows and columns must be swapped to
preserve the zero diagonal. Gauges and guards are evaluated on the resulting
matrix in the original ordered contact coordinates; the lattice contact
vectors themselves are not silently permuted.

## Determinant and the missing rank condition

Put

    A=(1-x)c+x e,  B=(1-y)c+y e,  D=u A-r B.

Direct determinant expansion gives the polynomial identity

    det(F) = b D.

The Z image is F(e3-e0)=(d e,-B,A,-d c), so its signs and gauge are

    (+,-,+,-),    gamma(Z)=d e+A=y e+(1-x)c.

The domain alone does not force D!=0. For example,

    x=1/4, y=3/4, t=1/2, h=3/5, c=e=r=u=1/5

gives b=1/10, all twelve required entries positive, and D=0. Its four
horizontal gauges at (1,0,0),(2,0,1),(1,0,1),(3,0,1) are respectively
3/50,9/50,6/25,3/25.

If those four gauges are all strictly greater than any beta>3/10, the
[four-vector rank argument](DET5_VOLUME_GAP_BOUNDS.md) forces invertibility.
Its proof is uniform in beta: stochasticity bounds the first two image
norms by 6/5, and the four lower bounds imply
||s-T r0||_1 > 2 beta-3/5 > 0 for every real scalar T.
Here r0=F ell(1,0,0) and s=F ell(2,0,1) span the image of the
horizontal contact-difference plane. Any vector in ker F has coordinate
sum zero, and the exact height identity with b>0 forces its H value
zero. It therefore belongs to that plane, where the map is injective.
Thus the four retained gauge assumptions suffice to infer D!=0; an
independent determinant inequality is not necessary in that formulation.

## Reconstructed geometry

When D!=0, use homogeneous contact columns
Ptilde=[(1,p0),...,(1,p3)], where
p0=0,p1=(5,1,2),p2=e2,p3=e3, and define
Vtilde=Ptilde F^{-1}. Column stochasticity ensures the first row of
Vtilde is all ones. Both factors are invertible, so its columns are the
vertices of a full-dimensional tetrahedron, and Ptilde=Vtilde F places
each contact in the relative interior of its designated opposite facet.

The reconstructed Y-coordinate row is (q^T-a 1^T)/b. Consequently the
chosen extrema really are vertices 0 and 3, and the actual Y width is
1/b. Its volume is 5/(6 b |D|). These claims are exact consequences
of the chart and rank condition. Hollowness and other directional widths
remain additional conditions; a matrix satisfying only the chart domain
is not automatically a hollow or large-width tetrahedron.

Run `.venv/bin/python tests/replay_det5_rational_height_chart_review.py` for
independent symbolic checks of the column and height identities, determinant,
Z formula, the conjugated branch, and the positive singular fixture. The
script issues no solver query. Its receipt records algebraic verification,
not an exclusion result.
