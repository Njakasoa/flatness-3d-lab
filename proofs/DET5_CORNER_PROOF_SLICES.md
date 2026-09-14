# Checked dependency slices remove the auxiliary gap upper bound

The three archived corner refutations remain valid after deleting the input
assumption `gap < 5/17`. This is established by three fresh Ethos checks of
lexically sliced CPC proofs against their actual reduced input statements.
It is not inferred solely from textual absence or from a solver's UNSAT label.

The consequence is an improved conditional theorem on the full enlarged
height square. Under the ordered hollow-tetrahedron contact hypotheses of
[CLAIM-0009](../claims/CLAIM-0009.md), with Y=(0,1,0), q0=0 and q3=1,

\[
 (q_1,q_2)\in[3/5,1]^2
 \quad\Longrightarrow\quad
 w(K)\le\frac{102}{65}\left(1+\frac2{\sqrt3}\right)
 \approx3.3812223833.
\]

This improves the archived 17/5 conclusion on this entire square. No premise
that global width exceeds 17/5 is needed for this stronger conclusion. On
[3/4,1]^2 the previous bound (23/19)(1+2/sqrt(3)) remains valid, with the gap
upper bound likewise omitted. The earlier statement restricting the
(102/65)(1+2/sqrt(3)) conclusion to [12/17,1]^2 was valid for the full input;
the checked subsets now remove the reason for that restriction.

## What the checked refutations actually use

All three original inputs have 82 assertions. Their retained hypotheses are:

| Hypothesis group | beta=4/23, lower=3/4 | beta=37/102, lower=2/3 | beta=37/102, lower=3/5 |
|---|---:|---:|---:|
| Strict off-diagonal F positivity | 12 | 12 | 12 |
| Column sums equal one | 4 | 4 | 4 |
| gap > 0 | 1 | 1 | 1 |
| gap < 5/17 | 0 | 0 | 0 |
| offset >= 0 | 0 | 0 | 0 |
| offset + gap <= 1 | 0 | 0 | 1 |
| Gauge lower bounds | 6 | 4 | 4 |
| Integer non-interior guards | 12 | 5 | 5 |
| Explicit lower height bounds | 1 | 0 | 1 |
| Explicit upper height bounds | 0 | 0 | 0 |
| McCormick product inequalities | 20 | 19 | 19 |
| Height/contact equations | 4 | 4 | 4 |
| **Total** | **60** | **49** | **51** |

The explicit retained height bounds are q1>=3/4 in the first slice and
q2>=3/5 in the third. These counts do **not** remove the rectangle hypothesis
from the geometric theorem: the retained product inequalities still contain
the corresponding rectangle endpoints. No minimality or necessity of each
retained assertion is claimed; these are dependencies of the particular
archived refutations.

Both enlargement slices use exactly the four gauges at

    (1,0,0), (1,0,1), (2,0,1), (3,0,1).

The 4/23 slice additionally uses (0,0,1) and (5,0,2). In particular neither
enlargement proof uses the Y gauge explicitly. The five guards used at lower
3/5 are

    (-1,0,0), (1,0,1), (2,1,1), (3,1,1), (8,1,3).

At lower 2/3, replace (8,1,3) by (1,0,2). The twelve guards used by the
4/23 slice are

    (-1,0,0), (-1,0,1), (-1,0,2), (-2,1,-1),
    (-3,1,-1), (-7,1,-3), (1,0,1), (1,0,2),
    (2,1,1), (3,1,1), (7,1,3), (8,1,3).

The [analysis receipt](../results/det5_corner_proof_slice.json) lists every
retained and omitted assumption, its original assertion syntax, its group,
and its command position in the source proof.

## Geometric implication after deleting the gap upper bound

Let F be the actual barycentric contact matrix and b=1/w(K,Y)>0. Positive
facet contacts give all twelve strict F inequalities and the four column
sums. The exact normalized heights and products satisfy the retained
McCormick inequalities and height/contact equations on the entire closed
specified square. Contact containment also gives offset+b<=1, the only
retained offset bound in the lower-3/5 slice. Hollowness makes every listed
integer guard a necessary non-interior condition, independently of any
finite-guard sufficiency threshold.

Suppose all four listed enlargement gauges were greater than 37/102.
The actual data would satisfy all 51 hypotheses of the lower-3/5 subset,
contradicting its checked refutation. Hence at least one of those four gauges
is at most 37/102, and therefore lambda_1(K-K)<=37/102. Applying the ACMS
inequality lambda_1(K-K)>=1-A/w(K), with A=1+2/sqrt(3), gives
w(K)<=A/(1-37/102)=(102/65)A. No upper constraint on b enters this argument.
The same argument with six gauges and beta=4/23 gives (23/19)A on the old
upper corner. All endpoints are included because the actual products remain
in the closed-domain envelopes and the refuted gauge conditions are strict.

The strengthened width conclusion applies to the same enlarged square,
so it does not alter the certified-region area: its new area outside the
old Y union remains 3/40. It does not remove a whole contact class, change
the 58-type necessary list, or certify inherited joint-search UNSAT labels.

## Lexical extraction and external validation

[The extraction script](../experiments/det5_corner_proof_slice.py) uses the
existing lexical CPC slicer. Identifier references are resolved in their
active scope before a new binding is installed; push/pop scopes restore the
environment, and needed discharge shells are retained. Dependency closure
starts from the final false step. Inert global assumption declarations are
then deleted. Retained assumptions are independently matched by exact
rational linear normalization to the reconstructed 82-assertion input.
The reduced SMT reference retains the original assertion rendering, avoiding
CPC-versus-SMT rational-numeral syntax differences.

The three proof/input pairs are in
[`certificates/det5_corner_slices`](../certificates/det5_corner_slices).
Their command counts change from 37,477 to 37,440; 25,660 to 25,598; and
29,423 to 29,363, respectively. Small command-count reductions do not detract
from the removal of substantive hypotheses: most retained commands perform
internal propositional and arithmetic inference.

Reproduce the analysis without a solver or proof-kernel call:

```sh
python3 -m experiments.det5_corner_proof_slice
```

Recheck the three subsets against the pinned external kernel and signatures:

```sh
python3 -m experiments.det5_corner_proof_slice \
  --ethos ETHOS/build/src/ethos \
  --ethos-source ETHOS --cvc5-source CVC5
```

The successful receipt pins Ethos revision
`221641668d75eaffd308e0511d63962cea937110` and cvc5 signature revision
`f3b21c4483d3b88dc63cb7cd3e5eb092eee5e341`, all source and reduced proof hashes,
and each exact reference hash. All three outputs were `correct`, exit code
zero, with empty stderr. There were zero new SMT queries. Original files
are unchanged; repeated extraction checks the new artifacts byte for byte.
Geometry-to-encoding implications remain written mathematics, separately
reviewed, rather than a formal geometric development inside Ethos.
