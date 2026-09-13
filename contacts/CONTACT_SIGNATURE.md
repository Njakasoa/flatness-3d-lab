# Contact signatures and exact equivalence

A signature records actual facet inequalities (algebraic normals allowed),
incident lattice boundary points, relative interior contacts, affine determinants
of contact frames, minimizing primitive width directions modulo sign, and the
affine lattice automorphism group when computed. Unknown quantities are null,
not guessed. Numerical signatures retain tolerances and are observational.

The implemented exact canonicalizer enumerates every ordered unimodular frame
chosen from the full boundary lattice set (at most eight points in this version).
For each frame it expresses all extreme vertices in that affine lattice basis
and takes a deterministic least serialization. Redundant V-generators are
removed by the exact rank of incident facet normals. Under GL(d,Z)⋉Z^d the set
of such normalized representations is unchanged. Conversely equal normalized
representations exhibit an affine unimodular equivalence. This is complete on
the domain containing a unimodular contact frame.

If no such frame exists the function explicitly returns unsupported; it does
not assert inequivalence or invent an ambient unimodular basis. General integer
contact tetrahedra are separately canonicalized by Hermite normal form in the
finite contact enumeration. These complementary methods are not a general
canonical graph labeling solution for arbitrary real bodies.

The discovery clustering currently uses facet count, relative interior contact
counts and number of numerical active directions. This coarse key is NOT an
equivalence certificate. The tetrahedral search fixes 0,e1,e2,e3 as contacts;
finding that signature there is a construction constraint, never a discovery.
