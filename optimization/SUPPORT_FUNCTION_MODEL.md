# Support-function and facet formulation

For a V-polytope, h_K(u)=max_v u.v and w(K,u)=h_K(u)+h_K(-u).
For fixed contact hull P, the uniform direction enclosure in
results/DEGREES_OF_FREEDOM.md can reduce all relevant primitive directions to
a finite set. Introduce t and inequalities t<=w(K,u) for each direction.

The discovery engine uses this epigraph formulation after Powell exploration;
it does not assert convexity. Variable vertices change active support pairs,
and facet-contact/hollowness constraints are nonlinear and disjunctive.
A fixed support chamber admits more explicit algebraic expressions; a complete
cover of all chambers still needs proof.

A facet through a fixed lattice contact p_i is n_i.(x-p_i)<=0 with a REAL
normal n_i, modulo positive scale. There are two local orientation parameters
per facet in dimension three. Integer normals are an optional strict subclass,
not a consequence of maximal lattice-freeness. An exact dual/Farkas or branch
certificate is required before solver infeasibility can eliminate a type.
