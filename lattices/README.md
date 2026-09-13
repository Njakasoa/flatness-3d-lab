# Lattice transformations

Use Polytope.transform(U,t) for integral U with determinant +-1 and integral t.
It rejects dimension errors, nonintegral maps and nonunimodular maps. A lattice
basis change for arbitrary lattices instead requires transforming the lattice
with the body, as explicitly done in src/examples.py.

src/canonical.py gives a complete body invariant when the FULL boundary contact
set contains a unimodular affine frame and has at most eight points. The HNF
contact enumeration handles general empty integer contact tetrahedra separately.
