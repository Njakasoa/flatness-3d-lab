# Independent internal review of the height-rank and quadratic lift

Date: 2026-09-14. Reviewer: a separate research subagent. Outcome: no
mathematical error found in the stated rank lemma, determinant identity,
or the complete quadratic encoding at the documented target 17/5.
This is an internal mathematical review, not external peer review or a
proof-assistant verification. No class exclusion or novelty claim follows.

## Material and actual checks

I read [the certificate generator](../experiments/height_rank_certificate.py),
[its JSON certificate](../certificates/height_rank_certificate.json),
[the proof](HEIGHT_RANK_AND_VOLUME.md),
[the height chart constructor](../experiments/contact_height_charts.py),
[the complete quadratic lift](../experiments/height_complete_quadratic.py),
the base gauge/guard constructor, and the inherited finite width-direction
enumerator. I did not edit these files or call a solver.

Separate, read-only Python checks used standard-library `Fraction`, an
independently written permutation determinant and Gaussian inverse, and
the archived JSON inputs. They imported no generator, solver, or geometry
engine. These checks verified:

- both classes' difference coordinates by multiplying by the augmented
  contact matrix; the relation z3=z2-z1; all three contact masses; positivity
  and values of the rank margins; every recorded minor and height constant;
- det(C0)=1/d by a direct four-by-four determinant;
- all twelve determinant signs through the row transformation described
  below, at rational normalized heights including endpoint ties;
- presence of all three rank gauges in both archived chart gauge lists;
- all affine contact automorphisms by independently considering the 24
  vertex permutations and solving for their linear maps; their integral
  entries, determinant magnitude one, and height reflection signs;
- equality of the resulting groups and extrema orbit partitions with the
  archives, and invariance of each finite gauge set up to vector sign;
- equality of the ten archived directions with an independent direct
  integer-covector enumeration of contact width at most three.

At this initial stage I did not replay archived SMT assertions, run mutation
tests, or certify the archived counterexample bodies. Subsequent interval
formula and mutation checks are described explicitly below.
The continuous arguments below, rather than finitely many substitutions,
justify the universal mathematical claims.

## Rank and minor bounds

Write A=||r||_1, B=||s||_1, C=||s-r||_1. Nonnegative column stochasticity
and the three strict gauges give 2 beta < A,B,C <= 2M. For
D=||s-tr||_1, the triangle inequalities imply respectively

    B+C-A <= 2D       (0 <= t <= 1),
    A+B-C <= 2D       (t < 0),
    A+C-B <= 2D       (t > 1).

Every left side is greater than 4 beta-2M. Thus D>g=2 beta-M>0 for
every real t. The certificate's closed lower bound D>=g is valid and
slightly weaker. In particular r and s are independent.

If Fx=0, column stochasticity gives 1^T x=0, and the height identity
F^T q=offset*1+bH with b>0 gives H^T x=0. The two-dimensional common
kernel is spanned by ell(z1),ell(z2). Independence of their images forces
x=0. Therefore F is invertible; this argument requires neither a chosen
determinant sign nor initial invertibility.

For r_i nonzero, choose t=s_i/r_i. The distance bound gives

    sum_j |r_i s_j-r_j s_i| > g |r_i|.

For a zero r_i the corresponding weak inequality remains true. Summing
and dividing by two yields total absolute minor sum > beta*g. Since r,s
span the common kernel of the independent covectors 1,q, their minors
are proportional to the complementary minors of [1 q]. With q_L=0 and
q_H=1, the complementary minor magnitude k is the proportionality
magnitude. For normalized heights sorted as 0,u,v,1,

    sum_{i<j}|q_i-q_j| = 3+v-u <= 4.

Consequently k>beta*g/4, so the encoded closed lower bound is safe,
including ties at either height endpoint.

For the upper bound, a two-coordinate projection of a zero-sum vector
with norm at most 2m lies in max(|x|,|y|,|x+y|)<=m. Its six vertices
are the hexagon in the certificate. Absolute determinants of two such
projections are bounded by the maximum over vertex pairs, namely m1*m2.
This proves the upper bound without any assumption on the remaining
normalized heights.

## Determinant and volume normalization

For C0=[ell(z1),ell(z2),ell(eY),e0], direct contact-coordinate calculation
gives det(C0)=1/d. Set M0=F C0=[r s t c]. If i,j complement L,H, the
matrix R with rows e_i^T,e_j^T,q^T,1^T has determinant
-parity(i,j,L,H). The bottom rows of R M0 are (0,0,b,offset) and
(0,0,0,1). Therefore

    det(M0)=-parity(i,j,L,H)*b*(r_i*s_j-r_j*s_i),
    |det F|=d*b*k.

The signs in the certificate agree. Since vol(K)=d/(6|det F|), the
volume condition vol(K)<1/beta^3 is exactly equivalent to
b*k>beta^3/6. Its necessity for the global target uses the previously
established hollow-body gauge/volume bound; large Y-width alone does not
imply that volume condition.

## Complete quadratic lift

Once F is invertible, F^T X=P_X and F^T Z=P_Z uniquely recover the
physical X and Z coordinates of its four vertices. The Y coordinates
are (q_i-offset)/b. Thus, for each covector u and pair i,j,

    u_X*b*(X_i-X_j)+u_Y*(q_i-q_j)+u_Z*b*(Z_i-Z_j)

is exactly b times their physical directional difference. The offset
cancels. Because b>0, comparison with (17/5)b preserves the strict
inequality. The disjunction over both signs of all six pairs is exactly
directional width >17/5; it does not require a preselected maximizing
pair. No accidental cubic term occurs: b*X and b*Z, and the inverse
coordinate constraints F*X and F*Z, have degree two.

Eight independent F entries, two free q entries, offset, b, the positive
minor variable k, and eight physical coordinates give 21 variables.
The disjunction k=minor or k=-minor, together with its positive lower
bound, imposes its absolute value exactly. The product b*k also has
degree two.

The finite direction list is complete at the documented threshold.
Write the contact evaluations of u=(x,y,z) as (0,h,y,z), where
h=d*x+y+a*z. Contact width at most three implies h,y,z lie in [-3,3],
and integrality requires d to divide h-y-a*z. This is exactly the
inherited enumeration, with primitive covectors retained up to sign.
All omitted primitive covectors have integral contact width at least
four; containment P subset K makes their widths strictly greater than
17/5. Independently enumerating x,y,z in [-3,3] is exhaustive here:
|x| <= (6+3a)/d < 2 for both classes whenever contact width is at most
three. It reproduced ten covectors per class.

The exposed `threshold` argument also permits lower-threshold controls,
but the completeness and necessity statements reviewed here concern
17/5. In particular, an arbitrary larger threshold would require revisiting
the finite direction list, and lower thresholds do not automatically
make the fixed ACMS cuts necessary. This is a scope limitation of using
the constructor outside its documented target, not an error in that target.

## Symmetry and branch coverage

Let an affine lattice automorphism T map P_j to P_{p(j)} and satisfy
Y(Tx)=epsilon*Y(x)+t_Y, epsilon in {1,-1}. Relabel the transformed
opposite vertices by V'_{p(i)}=T(V_i). Then

    F'_{p(i),p(j)}=F_{i,j}.

For epsilon=1, q'_{p(i)}=q_i and the extrema become (p(L),p(H)).
For epsilon=-1, q'_{p(i)}=1-q_i and the extrema become (p(H),p(L)).
In the second case offset'=1-offset-b; b is unchanged. This is precisely
the action implemented in `symmetries`. It preserves the allowed offset
interval, normalized endpoint ties, relative-interior contacts, and
column stochasticity.

The independent enumeration obtained group orders two and four and
respectively six and five disjoint orbits covering all twelve ordered
extrema pairs. The finite gauge sets are invariant up to sign under
these groups. Hollow-body observer equivalence ensures that transformed
bodies also satisfy the guard constraints; syntactic invariance of the
particular finite guard list is unnecessary. The full lattice width and
volume conditions are invariant under affine lattice automorphisms.
The auxiliary minor constraints are valid for every transformed body by
the rank proof above. Thus reducing to one representative per orbit loses
no body in the stated target.

The proof's distinction between the twelve-variable Y-only charts and
the complete 21-variable target is correct. This review validates their
geometric interpretation and construction; it does not turn UNKNOWN or
unqueried targets into infeasibility results.

## Interval outer relaxation and branch coverage

I subsequently reviewed
[the interval relaxation](../experiments/height_interval_relaxation.py).
The McCormick inequalities and branch bookkeeping are sound as written.
I also instantiated, without calling `check`, all eleven chart constructors
at the full square and at one proper rational subrectangle. For every
chart I verified that the last four source assertions are precisely the
four intended column-height identities. An arithmetic-expression degree
walk after algebraic simplification found degree at most one in all
22 constructed relaxations. These additional checks use the constructors
and Z3 for expression construction and simplification only; they are
distinct from the earlier standard-library arithmetic checks.

Column stochasticity and nonnegativity imply 0<=f<=1 for each F entry.
For q in [l,h] and the actual product p=f*q, the four envelope slacks are

    p-l*f                 = f*(q-l),
    h*f-p                 = f*(h-q),
    p-(q+h*f-h)           = (1-f)*(h-q),
    (q+l*f-l)-p           = (1-f)*(q-l).

They are all nonnegative. Therefore every actual height-chart solution
in the specified rectangle extends to a feasible relaxed solution by
assigning the six auxiliary products their actual values. This is the
direction needed for sound UNSAT exclusions; a relaxed SAT assignment
need not give an actual body.

The two free q rows have three off-diagonal entries each, so exactly six
genuinely bilinear products require lifting. The residual terms in the
reconstructed identities are constant endpoint heights times F entries,
or free q entries times diagonal zeros. The latter are identically zero;
their unsimplified multiplication syntax introduces no nonlinear content.
Slicing off the final four assertions currently removes exactly the intended
identities. This depends on the present constructor ordering and merits
retaining a structural audit if that constructor changes.

For each chart the initial box is the full closed square [0,1]^2. An UNSAT
node is removed; every SAT or UNKNOWN node is replaced by its two closed
halves along a longest side. Their union equals the parent box, including
the shared boundary. Inductively, excluded node boxes together with the
pending frontier cover the original square. Only nodes excluded by UNSAT
are terminal without children. Thus `complete_cover = not queue` is sound:
it can be true only when excluded boxes cover the entire chart. An UNKNOWN
ancestor is harmless only if all its descendant leaves are eventually
excluded. The query budget stops subdivision while retaining pending
leaves, so reaching that budget does not itself establish a bound.

The exclusion target remains the Y-width chart with its stated gauge and
observer assumptions. A complete independently checked cover of all eleven
symmetry representatives would exclude that target in both classes and
hence exclude the stronger global-width target there. Partial covers,
relaxed SAT models, and UNKNOWN nodes do not yield such an exclusion.
No interval solver outcome was established or independently verified by
this review, and I made no solver queries.

## Audit of the subsequently completed interval campaign

The completed [campaign archive](../results/height_interval_relaxation.json)
was then available. Its SHA-256 at review was
`97cff58c2bc9519a5d1642de725b503369da6764dd36481a552bb06196215021`.
It reports 113 queries across all eleven representatives, with 62 leaves
labelled UNSAT and no pending leaves. Two interior nodes were UNKNOWN;
both were subdivided fully. I independently audited the recorded coverage
and all archived formulas, without issuing any solver queries or importing
the experiment constructors for this audit.

Starting separately from the full square for each chart, I reconstructed
every longest-side split with exact `Fraction` arithmetic and the stated
first-axis tie break. The reconstructed node tags, rational box endpoints,
breadth-first order, child coverage, leaf lists, UNKNOWN lists and query
counts all matched the archive. No queried node was duplicated or omitted.
Every non-UNSAT node had both children, and every terminal node was labelled
UNSAT. The leaves also had total dyadic area one in each chart. Coverage
follows from the checked tree and exact closed-half unions, not merely from
this area sum.

The numbers of leaves by representative, in archived order, are:

| Class | Extrema representatives | UNSAT-labelled leaf counts |
|---|---|---|
| d=7 | (0,1), (0,2), (0,3), (1,0), (1,2), (1,3) | 2, 15, 3, 2, 5, 8 |
| d=8 | (0,1), (0,2), (0,3), (1,0), (1,3) | 6, 6, 3, 6, 6 |

For all 113 archived SMT files I independently reconstructed the expected
F parameterization, strict off-diagonal positivity, all finite gauge
disjunctions, every observer guard, normalized height and offset bounds,
the exact node box, all six product envelopes, and all four lifted height
identities. Parsing the archived formulas used Z3 only as a parser and
algebraic simplifier. A separate rational linear-polynomial normalizer
compared the complete Boolean assertion sets, allowing tautologies,
duplicate constraints and harmless ordering differences. Every archive
matched exactly: no required constraint was missing and no unexpected
constraint was present. In particular, this rules out an accidental extra
constraint as the reason for the reported UNSAT outcomes. It does not
establish that those outcomes are correct.

### Conditional mathematical consequence

Subject to validation of the 62 UNSAT leaves, the combined cover would
prove that every hollow tetrahedron in either of the specified four-facet
relative-interior contact classes has lattice width at most 17/5. To check
the implication, suppose instead that its global lattice width exceeds
17/5. The previously established ACMS bound with A=1+2/sqrt(3)<13/6 gives

    lambda_1(K-K) >= 1-A/w(K)
                    > 1-(13/6)/(17/5) = 37/102.

Hence every finite gauge imposed by these models is necessary. Hollowness
and the contact assumptions supply every observer guard. The Y-width also
exceeds 17/5. Its normalized heights lie in one of the twelve ordered
extrema charts, including endpoint ties, and the reviewed symmetry action
maps that chart to one of the eleven representatives. Its actual products
would satisfy the corresponding outer relaxation in every leaf containing
those heights. Valid UNSAT conclusions for a complete cover would therefore
contradict the existence of this tetrahedron.

This conditional result is a non-strict width bound <=17/5, not an
exclusion of equality. Its scope is these full four-contact tetrahedral
classes. It does not exclude general nonsimplicial hollow bodies containing
the same contact tetrahedra as subsets. With the existing contact reduction,
it would remove the d=7 and d=8 entries from the list at w>=2+sqrt(2),
because 2+sqrt(2)>17/5, reducing that list from 61 to 59. It would leave
unchanged the 62-entry list at the smaller original threshold
c=(11/7)(1+2/sqrt(3))<17/5. It would not prove the global flatness conjecture.

### Remaining validation before treating this as a theorem

The leaf status strings remain unverified by this review. Before promoting
the conditional exclusion, every one of the 62 exact archived leaf formulas
needs an independently validated UNSAT result, ideally a proof checked by
an independent proof checker or explicit rational infeasibility certificates.
A second independent SMT engine on those same formulas can corroborate the
outcomes, with the computational trust and proof availability stated
accurately. The coverage audit, formula audit, symmetry reduction and ACMS
implication must remain attached to that evidence: solver outcomes alone
would not prove the mathematical scope. I endorse the coverage and encoding
checks above, not the currently unverified UNSAT labels.

### Durable audit and independent full-matrix encoder review

The coverage/formula audit is now persisted as
[audit_height_cover_independent.py](../tests/audit_height_cover_independent.py),
with its actual successful output in
[height_cover_encoding_validation.json](../results/height_cover_encoding_validation.json).
It reconstructs contact automorphism representatives, checks every dyadic
tree, compares every archived assertion set, and records all 113 input
file hashes. It imports no experiment or geometry module and never calls
a solver. Its separate rational linear-polynomial normalizer uses Z3 only
for parsing and algebraic simplification.

Running this persisted audit passed all 113 encodings and the 62-leaf cover.
It also rejected five deliberately invalid mutations: a missing covering
leaf, a gap in a dyadic interval, a deleted gauge, an extra contradictory
assertion, and an overrestrictive product envelope. Thus the audit tests
both omissions and accidental strengthening. These tests validate the
audit mechanism; they do not validate the leaf UNSAT conclusions.

I additionally inspected `statement()` in
[replay_height_cover_cvc5.py](../tests/replay_height_cover_cvc5.py) for
accidentally stronger assumptions. None was found. Its twelve independent
off-diagonal F entries with strict positivity and four column sums describe
the same matrix domain as the eight-parameter discovery model. The Gaussian
coordinate systems have augmented right sides (0,v) for differences and
(1,v) for affine guard points. They therefore give the intended gauge and
guard forms without relying on the explicit difference-coordinate formula.
The exact dyadic boxes already imply 0<=q<=1. Its height sums correctly omit
the zero diagonal and low-height contributions, retain the high-height F
contribution, and use offset or offset+gap according to the actual 0/1
contact height. Its four product envelopes agree with the reviewed outer
relaxation. This source review supports equivalence of that independent
encoding; it is not a check of cvc5's UNSAT outputs or exported proofs.
