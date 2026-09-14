# Two parallel contact sections: exact interpolation and its limits

Status: structural reduction for actual tetrahedra, with no new numerical
flatness bound or certified residual-domain exclusion.

Use the strict contact hypotheses and notation of
[the height-order lemma](DET5_Y_CORNER_ANALYTIC_PROBE.md). In the branch
`x<y`, the normalized vertex heights are `(0,x,y,1)`, the physical plane
`Y=0` has normalized height `a`, and the physical plane `Y=1` has height
`h=a+b`, where `b>0`. Thus `x<a<y` and `a<h<1`.
Write `S_t={(X,Z):(X,t,Z) belongs to K}` for a physical section.
The integer contact segments in these two planar coordinate systems are

    S_0 contains [(0,0),(0,1)],
    S_1 contains [(0,0),(5,2)].

Both segments are primitive lattice segments. Their planar direction
vectors have determinant of absolute value five.

## There is at most one section transition between the contact planes

The plane at normalized height `a` cuts edges `02,03,12,13` and is a
quadrilateral. The two contacts on its adjacent edges are `p0` (facet 0)
and `p3` (facet 3), with common section vertex on edge `12`.

There are three cases at the second contact plane:

* `h<y`: this is another quadrilateral on the same four tetrahedral edges.
  Contacts `p1` and `p2` lie in the relative interiors of the adjacent
  section edges from facets 1 and 2. Their common section vertex lies on
  edge `03`. The two contact pairs therefore occupy complementary pairs
  of adjacent edges.
* `h=y`: the section is a triangle with vertex `v2` and its other two
  vertices on edges `03,13`. Facet 3 contributes only the singleton `v2`;
  its prescribed contact `p3` lies on the other contact plane, so this
  degeneration causes no contradiction.
* `h>y`: the section is a triangle on edges `03,13,23`.

Consequently the only possible transition occurs at physical height

    t_*=(y-a)/b.

It occurs in `(0,1)` exactly when `h>y`, or at the upper endpoint when
`h=y`. For the reverse order `y<x`, exchange vertex labels 1 and 2.

## Exact Minkowski interpolation within each band

Suppose two normalized section heights `s_0<s_1` lie in the same open band
between successive distinct vertex heights. Identify the section planes
by their common `(X,Z)` coordinates, and call the resulting polygons
`Q_0,Q_1`. Then for `0<=t<=1`,

    Q_{(1-t)s_0+t*s_1} = (1-t) Q_0 + t Q_1.                 (1)

Here addition on the right is Minkowski addition. The same identity holds
by continuity when one or both heights reach the endpoints of the band.

Proof. Each section vertex lies on a fixed tetrahedron edge, so its
coordinates are affine functions of the section height. Each section
edge lies in a fixed tetrahedron facet and consequently has a fixed
outward normal in the `(X,Z)` plane. All edges are present throughout the
open band, giving the polygons a common normal fan. For any fixed planar
direction `u`, the same section vertex (or the same edge at a fan boundary)
maximizes `u` throughout that band. Its support value is affine in height.
The support functions on the two sides of (1) therefore agree in every
direction, proving equality of the convex polygons. The endpoint statement
follows by taking limits of these compact sections.

In particular, if `h<=y`, the entire physical slab satisfies

    S_t=(1-t) S_0+t S_1,        0<=t<=1.                    (2)

Every planar directional width is then affine in `t`. If `h>y`, split the
slab once at `t_*`; use (1) on the quadrilateral band below the transition
and the triangular band above it. No further changing shape is hidden
inside either band.

An equivalent exact reduction is that the portion of `K` between any two
section planes in a common band is the convex hull of those two sections.
This statement also follows directly because the slab has no tetrahedron
vertices strictly between its boundary planes.

## What the contact-height equations do not imply

The two equal-contact-height identities and strict facet positivity alone
do not force `h>y`. For example, take

    x=1/5, y=4/5, a=2/5, b=1/5, h=3/5,

and the column-stochastic matrix

    F = [  0     3/10   6/25   1/10
          7/10    0     1/5   8/15
           1/5   1/2     0   11/30
          1/10   1/5   14/25   0   ].

Every off-diagonal entry is positive, `det(F)=-1/100`, and

    F^T (0,1/5,4/5,1)^T = (2/5,3/5,3/5,2/5)^T.

Its reconstructed vertices, in columns, are

    [ -115/3  -10   25   20
          -2   -1    2    3
       61/15 -2/5 11/5 -8/5 ].

This example is deliberately only a contact-geometry counterexample: it
is not hollow. The integer point `(-5,0,0)` has strictly positive barycentric
coordinates `(7/50,17/30,1/30,13/50)` in this matrix. Hollowness could still
imply an additional section-order restriction; this note establishes none.

Likewise, (2) cannot on its own certify lattice freeness of the whole
three-dimensional tetrahedron. Between `Y=0` and `Y=1` there is no interior
integer `Y` level. Hollow sections at the two integer planes do certify
absence of integer interior points in this slab, but say nothing about
integer planes below zero or above one. Nor do they give a common short
integer planar direction: the minimizing lattice directions of `S_0` and
`S_1` may differ. A future planar argument must supply that missing
arithmetic information or control the outer integer sections.
