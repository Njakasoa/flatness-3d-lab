# What remains free in a counterexample search?

A hypothetical counterexample can motivate searching a global width maximizer, but the reduction changes the object being studied. The table concerns a bounded full-dimensional inclusion-maximal width maximizer when invoking ACMS. An arbitrary hollow body above the candidate width need not satisfy the same maximal-facet/contact conclusions. The body-volume window does extend to every hollow K with width at least the candidate value, by the proof inequalities in UPPER_BOUND_SLACK.md.

| Degree of freedom | Bounded? | Known theorem / deduction | Observation in this run | Candidate next lemma | Certification cost |
|---|---|---|---|---|---|
| Facet count of a maximal body | At most 8 in dimension 3 | Lovasz contact criterion and parity bound | 4,5,6 facet families represented | Eliminate a maximal contact type, not arbitrary truncations | Medium to high |
| Contact hull dimension | 2 or 3 | ACMS Thm 5.4 | Unimodular tetrahedral and cube-subset ansatzes | Exclude the coplanar square case | High; unresolved in cited work |
| 3D contact integer volume | <=44 | ACMS Euclidean volume <=22/3 | Not imposed as a universal sample constraint | Efficient inequalities per contact hull | High |
| Tetrahedral contact determinant | <=17 | ACMS Euclidean volume <=17/6 | Complete HNF enumeration is separately bounded | Eliminate determinant classes >=2 | Medium to high |
| Contact positions modulo GL⋉Z | Finite for bounded-volume full-dimensional empty hulls | Standard finite lattice-polytope reduction, made executable for tetrahedra | Canonicalizer checks supported frame domain | Enumerate other 5–8 contact hulls with proof | High |
| Facet orientation at fixed contacts | Continuous; 2 real parameters per facet | Plane through fixed point, modulo nonzero scale | Eight-parameter contact tetra optimization reaches baseline numerically | Certified cover of parameter chambers | Very high |
| Facet normal integrality | False generally | Algebraic Delta normals give a direct obstruction | Engine permits irrational normal ratios | No valid integer-normal restriction known | Must not be assumed |
| Body coordinate range for fixed full-dimensional P | Bounded using volume window | conv(P,x) subset K and barycentric volume formula | Search imposes its own small numerical box | Exploit exact barycentric bounds below | Low to derive, costly to enumerate |
| Potentially minimizing width directions | Finite once a full-dimensional P is fixed | Exact inverse-difference inequality | Complete per-body certificates implemented | Uniform per-contact direction set | Low |
| Symmetry | Not forced by present results | Known Delta is locally optimal | Asymmetric optimization rediscovers its width | Quantitative stability outside imposed ansatz | High |
| Counterexample branch | Open | No global optimality proof | No certified counterexample found | Square case or contact determinants >=2 | High |

## Explicit uniform constraints for a fixed contact simplex

Suppose P=conv(p0,p1,p2,p3) is contained in K and det B=N>0 in absolute value,
where B has columns pi-p0. Put V_P=N/6. For x in K, write affine barycentric
coordinates lambda_i(x) in P. Triangulating conv(P,x) over the visible facets
gives vol(conv(P,x))=V_P (1+sum_i max(0,-lambda_i(x))). Consequently, if
vol(K)<=Vmax, then sum_i max(0,-lambda_i(x))<=Vmax/V_P-1. Each lambda_i lies
in [1-Vmax/V_P, Vmax/V_P]. This is a concrete bounded region in the fixed
contact frame, not an unexplained coordinate cutoff. It is an elementary
consequence of the existing volume theorem, not claimed novel.

For width directions let D=B^T. If w(K,u)<4 then |D u|_infinity<4 because
all contact points are in K. Thus |u_j|<4 sum_i |(D^-1)_ji|; a safe closed
integer box uses ceil(4 sum_i |(D^-1)_ji|)-1. For P=conv(0,e1,e2,e3), every
potentially minimizing direction lies in [-3,3]^3. ACMS supplies w(K)<3.972
for hollow bodies globally through the maximizer bound. This uniform direction
set removes one infinite quantifier in the fixed unimodular contact family.
The exploratory search used [-2,2]^3 and therefore reported only directional
upper estimates; selected exact certificates close that gap per body.

Neither argument bounds the transverse coordinate in the coplanar-square case.
Fixing discrete contacts also does not solve the remaining real parameter
optimization. These are the concrete bottlenecks after the known finite reduction.
