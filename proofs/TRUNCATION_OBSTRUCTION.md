# No subextremal threshold forces every hollow body to be tetrahedral

This is an elementary scope correction, not a new flatness bound.

Let T be the certified Codenotti–Santos tetrahedron and W=2+sqrt(2).
Write its barycentric coordinates as lambda_0,...,lambda_3. For 0<delta<1,
put T_delta=T intersect {lambda_0<=1-delta}. This body has six vertices
(the three untouched vertices and the three edge cut points) and five facets.
It is hollow because it is a subset of T.

For the barycenter c of T and epsilon=4 delta/3<1, the copy
(1-epsilon)T+epsilon c is contained in T_delta: its maximum lambda_0 is
1-3 epsilon/4=1-delta. Monotonicity and homogeneity of directional widths give
w(T_delta)>=(1-4 delta/3)W. Thus for EVERY c0<W there exists a hollow
non-tetrahedral body of width>c0. In particular, the suggested implication
“w(K)>3.4 implies K is tetrahedral” is false for arbitrary hollow bodies.

The exact executable control uses delta=1/1000 and computes the complete lattice
width independently of this containment bound. See certificates/truncated_delta.json.
The new cut facet has no relative interior lattice contact, so T_delta is NOT
maximal lattice-free. This argument says nothing against a statement about
maximal extensions, containment in a tetrahedron, or global maximizers.

The same idea creates arbitrarily many facets by sufficiently small further
truncations. Therefore facet count of arbitrary near-extremizers is not the
appropriate target for a finite contact classification. Maximalize first and
state explicitly what object is being classified.
