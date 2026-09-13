# Body representation

Exact bodies are src.geometry.Polytope instances with full-dimensional vertices
in Q, Q(sqrt2) or Q(sqrt3). JSON coordinates use explicit a,b,d fields for
 a+b sqrt(d). No eval or floating conversion is used to parse certificates.

Numerical observations live in results/near_extremizers.jsonl with status
numeric_body, tolerances and directional upper estimates. Exact rationalization
creates a different, explicitly stored body. Its certificates belong to that
new body only. See experiments/certify_discovery.py.
