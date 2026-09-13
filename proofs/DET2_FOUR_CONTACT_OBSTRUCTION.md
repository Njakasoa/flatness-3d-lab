# Four non-unimodular contacts can persist above width 13/4

This is an exact witness and a scope obstruction, not an optimum theorem or
a claimed new global flatness bound. External novelty is not established.

Let the four designated lattice contacts be

    p0=(0,0,0), p1=(2,1,1), p2=(0,1,0), p3=(0,0,1).

Their normalized tetrahedral volume is two. Write x=sum(lambda_i p_i),
sum(lambda_i)=1, and define K by A lambda >= 0, where

```
A = [ 0          33/56       23/112       23/112
      999/4600   0           1001/2000    12987/46000
      2997/8000  999/8000    0            1001/2000
      33/52      19/78       19/156       0          ].
```

Every row sums to one, its diagonal entry is zero, and its other entries are
strictly positive. Hence p_i belongs to the relative interior of the i-th
facet, once boundedness and nondegeneracy are verified.

Put B=A^{-1} and r_j=sum_i B_ij. All r_j are strictly positive. The change
mu=A lambda identifies K with {mu>=0, sum_j r_j mu_j=1}, so its four vertices
have barycentric coordinates B_.j/r_j. This proves boundedness and that the
four inequalities define genuine facets. The generator computes these
quantities over exact rational numbers.

The exact vertices are contained in a box whose only possible integer points
are

    [-1,2] x [-1,1] x [-1,2] intersect Z^3.

All 48 points are checked by the exact facet inequalities. None is interior;
the only boundary points are p0,p1,p2,p3. Thus K is hollow. The facet blockers
also imply maximal hollowness: an extension beyond any facet makes its
relative-interior lattice blocker interior to the enlarged convex body.

The exact lattice width is

    4009295246418 / 1232189371865 = 3.2537979453188... > 13/4,

with unique primitive minimizing direction (1,-1,-1), modulo sign. For this
specific K the proved width-search coordinate bounds are (2,3,2), containing
73 primitive directions modulo sign. The bound comes from a vertex basis:
if D has rows (v_i-v_0)^T and W is a known directional upper bound, then
q=D u satisfies |q_i|<=W for every potentially minimizing direction, hence
|u_j|<=W sum_i |(D^{-1})_ji|. Directions outside the certified integer box
therefore cannot improve W. This is a finite proof, not an empirical cutoff.

Consequently, a proposed rule that four lattice facet contacts must form a
unimodular tetrahedron once the width exceeds 13/4 is false, even for maximal
hollow tetrahedra with exactly four boundary lattice points. The configuration
is in the four-cycle exclusion branch of the determinant-two chart. This
does not exclude a stronger contact theorem at a threshold closer to 2+sqrt(2).

The witness also persists on a relatively open neighborhood in the eight
contact-preserving parameters. Matrix invertibility, r_j>0 and positive
off-diagonal entries are open conditions. A small neighborhood has the same
finite integer bounding box; each noncontact lattice point is strictly outside
at least one facet, and these finitely many strict exclusions persist. Width
is continuous there: a fixed small ball inside every nearby body gives a
uniform finite bound for all potentially minimizing integer directions.
The strict width margin above 13/4 therefore persists. No numerical size for
this neighborhood is asserted.

Reproduction: `python -m experiments.certify_det2_four_contacts`.
Exact payload: [det2_four_contacts.json](../certificates/det2_four_contacts.json).
Both witnesses have passed the [independent rational replay](../tests/replay_det2_cycle_independent.py)
and the [Astra scope review](../results/DET2_WITNESS_ASTRA_REVIEW.md).
The entrypoint requires both inputs and checks the particular claimed width,
hollowness and contact set, including rejection of a different self-consistent
witness substituted under the four-contact claim name.
The companion six-contact rational reconstruction has width about 3.28338;
neither witness comes with a local or global optimality certificate.
