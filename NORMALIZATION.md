# Normalization

The computational body is the convex hull of finitely many exact vertices in R^d, d=2 or 3, with nonempty interior. Coordinates lie in Q, Q(sqrt(2)), or Q(sqrt(3)); mixed fields and floating input are rejected. Arbitrary unbounded sets and lower-dimensional bodies are outside the engine contract. The theoretical flatness supremum can be formulated with compact full-dimensional convex bodies.

Hollow means int(K) intersects Z^d trivially. Boundary lattice points are allowed. Width in u is max_v u.v-min_v u.v. Lattice width minimizes over nonzero integral u; nonprimitive multiples cannot improve width, and u and -u have the same value. Direction lists contain the representative whose first nonzero entry is positive.

Under x -> Ux+t with U integral det(U)=+-1 and t integral, hollowness and width are invariant. Directions transform by U^(-T). Width alone is translation invariant for any real t; hollowness is not. An arbitrary invertible affine map is valid only if the lattice is transformed too.

Volumes use the standard Z^d fundamental parallelepiped as unit. Thus normalized integer volume of a lattice simplex is d! times its Euclidean volume. These two normalizations must never be conflated.

ACMS display Delta in the affine lattice Lambda={odd a,b,c: a+b+c=1 mod 4}. Set p0=(-1,-1,-1), B with columns (2,0,2),(2,2,0),(0,2,2). The map z -> p0+Bz bijects Z^3 onto Lambda and |det B|=16. The code applies B^-1(x-p0); the four facet contacts become 0,e1,e2,e3. Raw displayed coordinates must never be checked against Z^3.

FACET NORMAL CORRECTION: width directions are integral, but facet normals of real/algebraic hollow polytopes need not admit any nonzero integer rescaling. No integer-normal restriction is used by the exact engine. Integer-normal exploration is a strict subclass unless an independent reduction proves otherwise.

Maximal lattice-free means inclusion maximal among all lattice-free convex sets, not just among lattice polytopes. Integral maximality is a different property. A theorem about width maximizers, or their contact hulls, is not automatically a theorem about every high-width body.

Statuses: numeric_body (exploration only); exact_body (explicit exact vertices); certified_hollow (full finite point search justified by vertex bounds); certified_lattice_width (complete direction search justified below). Passing one certificate does not imply the other.

Scope refinement after replay: although ACMS Theorem 5.2 is stated for maximizers, its volume inequalities use only hollowness and w(K)>=2+sqrt2. The body-volume window therefore extends to all such K. Contact-hull claims still require their inscribed/maximal contact hypotheses. See proofs/UPPER_BOUND_SLACK.md.
