# Integer programming context

For a convex feasible region K with no interior integer point, a primitive
integer direction u of width w places its interior across at most ceil(w)
integer levels (endpoints may change the closed-set count). Closed K lies on
at most floor(w)+1 integer hyperplanes when its projection endpoints are
appropriately aligned; the exact count is floor(max u.K)-ceil(min u.K)+1.
These slices reduce dimension after a unimodular coordinate change.

The flatness theorem supplies a dimension-dependent width bound used in fixed-
dimension integer programming and geometric branching algorithms. Finding the
direction and processing the slices have costs of their own. Improving 3.972
to 3.9 does not change the worst-case four-level count for closed bodies;
crossing an integer threshold can affect that crude count. The conjectured
2+sqrt2 is still above three. No running-time improvement for a practical solver
is established by this laboratory. The present work changes no known upper bound.

Primary context: Lenstra, Integer programming with a fixed number of variables,
Mathematics of Operations Research 8 (1983), 538–548,
https://doi.org/10.1287/moor.8.4.538; ACMS introduction,
https://arxiv.org/abs/1907.06199.
