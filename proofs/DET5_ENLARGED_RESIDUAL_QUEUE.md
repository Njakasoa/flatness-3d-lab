# Enlarged certified Y square: exact residual-domain update

The certified closed square `Y_extrema = [0,3]`,
\(S=[3/5,1]^2\), adds exactly \(3/40\) of normalized Y-chart area
outside the twelve previously certified Y rectangles. Its union with the seven
old rectangles in this particular Y chart has area
\(7/16+3/40=41/80\). This is new domain beyond the old high corner;
the earlier proof of the \([3/4,1]^2\) corner only upgraded an already
excluded region.

The new square is certified by
[`det5_y_corner_enlarged_3_5.json`](../results/det5_y_corner_enlarged_3_5.json):
a complete cvc5 UNSAT proof with recorded successful Ethos replay. Its premise
uses the weak necessary gauge bound \(37/102\), the target \(17/5\), and
the labeled Y chart. The geometric interpretation remains conditional on the
actual hollow contact tetrahedron having **global lattice width greater than
\(17/5\)**. The overlay below does not replace the separate audit that these
input constraints follow from that geometric premise. In particular, the
corner normalization alone at \(3/5\) does not imply the input bound
\(b<5/17\). No unconditional width bound is inferred here.

## Exact updated queue

[`det5_enlarged_residual_queue.py`](../experiments/det5_enlarged_residual_queue.py)
reads the frozen
[`258-entry queue`](../results/det5_certified_residual_queue.json), its bound
953-query source, and the old and new certificate receipts. It verifies source,
input, compressed-proof and expanded-proof hashes and recorded external check
success. It neither calls a solver nor reruns a proof kernel.

For each old residual entry \(D\), its new domain is
\[
 D'=D\setminus S
   =D\cap\{q_1<3/5\;\lor\;q_2<3/5\}
\]
in the \([0,3]\) Y chart. Other labeled Y charts remain unchanged. The
unchanged original four-dimensional closed box and every old strict exclusion
clause are retained. The new disjunction is simplified only by removing
literals impossible throughout the original box. All closed certified square
boundaries are therefore removed. No symmetry transport is used.

The exact classification of the **previous residual domains**, rather than
of their enclosing boxes, is:

| Effect of the new square | Entries |
|---|---:|
| Wholly removed | 0 |
| Partially removed with positive area | 3 |
| Newly intersected only on boundaries | 0 |
| No new intersection | 255 |

The queue still has **258 entries**. The three tightened entries are:

| Y extrema | U extrema | Original leaf | Added strict restriction |
|---|---|---|---|
| `[0,3]` | `[0,2]` | `r1111011` | \(q_1<3/5\) |
| `[0,3]` | `[0,3]` | `r111101` | \(q_1<3/5\) |
| `[0,3]` | `[0,3]` | `r111110` | \(q_2<3/5\) |

For each of these entries the previous Y-area was \(1/16\), the newly
excluded area is \(3/80\), and the remaining area is \(1/40\): exactly
\(3/5\) of the previous area is removed. The U intervals are untouched.
All six old half-covered boxes keep their previous strict boundaries and
remaining fraction \(1/2\).

The sum of removed four-dimensional box measures over labeled charts is
\(3/128\), taking the previous sum \(1803/1024\) to \(1779/1024\).
These normalized coordinate measures are neither physical volumes nor a
coverage percentage of all contact tetrahedra.

## Why overlapping certificates and boundaries are handled exactly

The new square overlaps old certified rectangles in their interiors. Summing
all intersection areas independently would overcount those overlaps. The
script instead partitions each coordinate at every relevant old and new
rectangle endpoint. It evaluates every endpoint singleton and one rational
midpoint from every intervening open interval. All membership predicates and
strict comparison clauses are constant on each Cartesian cell.

Checking all **2,658 representative pairs** proves exact equality of the
old residual predicates with the old certified-union complement, and exact
equality of every new predicate with the incremental set difference. Empty
domains are identified by all cell types, including lower-dimensional cells;
positive area is computed separately by summing disjoint open two-dimensional
cells. Thus no boundary can be lost merely because it has zero area.

Within the full unit Y chart, the newly certified set outside the old union
is exactly the disjoint union
\[
 [3/5,3/4)\times(3/4,1]
 \quad\cup\quad
 (3/4,1]\times[3/5,3/4),
\]
whose two components each have area \(3/80\).

Reproduce this exact geometry and hash validation with:

```sh
python3 -m experiments.det5_enlarged_residual_queue
```

The result is
[`det5_enlarged_residual_queue.json`](../results/det5_enlarged_residual_queue.json).
The older queue and all frozen discovery archives are preserved. This updates
only the declared pending domain: inherited joint UNSAT labels still require
their own certification, the entire class is not excluded, and the count of
58 contact types has not changed. The SAT probe on \([11/20,1]^2\) does
not enter this subtraction and supplies no actual hollow counterexample.
