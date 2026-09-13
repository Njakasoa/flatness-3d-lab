# Complete finite direction certificate

Let v0,...,vd be affinely independent vertices of a full-dimensional V-polytope K. Let D have rows (vi-v0)^T. Choose any tested integer direction, giving an exact upper bound W on w(K). For any direction u with w(K,u)<=W, q=Du satisfies |qi|<=W. Therefore |uj|<=W sum_i |(D^-1)ji|. Since uj is integral it suffices to enumerate the coordinate box Bj=floor(W sum_i |(D^-1)ji|).

Every direction outside this box has width>W. Inside it, discard zero, nonprimitive multiples and the negative representative, and compare all support differences exactly. The minimum is an upper certificate witnessed by one direction, and a lower certificate supplied by the full finite minimum plus the proved exclusion. Equality is retained to recover ALL minimizing directions. This is not a fixed empirical radius.

The engine rejects singular bodies, unsupported number fields, floats, and workloads exceeding the explicit cap; hitting a cap never returns a partial certificate. Generic polytopes with redundant V-generators are allowed. Exact volume is presently implemented only for simplices.

Facet enumeration considers all d-generator affine hyperplanes; retain supporting hyperplanes, and deduplicate by their full incident vertex-index sets. Every facet contains d affinely independent generators, so it is found. Lattice points lie in the exact coordinate extrema box. Exact facet tests classify interior/boundary/outside, making the hollowness search complete.

This is an elementary implemented certificate argument; mathematical novelty is not claimed. Independent replay must reconstruct the bounds and facet tests, not trust boolean flags in JSON.
