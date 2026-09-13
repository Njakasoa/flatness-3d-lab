"""Exact polynomial identities for the determinant-two pair matrix.

Standard library only. The four diagonal surplus variables and eight positive
cross-edge weights are independent formal variables. No numerical sampling or
solver conclusion is used to establish the coefficient identities.
"""
import itertools
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EDGES = [(i, j) for i in range(4) for j in range(4) if (i < 2) != (j < 2)]
NAMES = [f"k{i}" for i in range(4)] + [f"e{i}{j}" for i, j in EDGES]
ZERO = (0,) * len(NAMES)


def require(condition, message):
    if not condition:
        raise ValueError(message)


def add(*polys):
    result = {}
    for poly in polys:
        for monomial, coefficient in poly.items():
            result[monomial] = result.get(monomial, 0) + coefficient
    return {m: c for m, c in result.items() if c}


def scale(poly, value):
    return {m: c * value for m, c in poly.items() if c * value}


def multiply(a, b):
    result = {}
    for ma, ca in a.items():
        for mb, cb in b.items():
            m = tuple(x + y for x, y in zip(ma, mb))
            result[m] = result.get(m, 0) + ca * cb
    return {m: c for m, c in result.items() if c}


def variable(index):
    m = list(ZERO)
    m[index] = 1
    return {tuple(m): 1}


def determinant(matrix):
    n = len(matrix)
    result = {}
    for p in itertools.permutations(range(n)):
        inversions = sum(p[i] > p[j] for i in range(n) for j in range(i + 1, n))
        term = {ZERO: (-1) ** inversions}
        for i in range(n):
            term = multiply(term, matrix[i][p[i]])
        result = add(result, term)
    return result


def rooted_forests():
    """Independently enumerate directed forests, each arrow pointing to a root."""
    forests = {}
    choices = [[None] + [j for ii, j in EDGES if ii == i] for i in range(4)]
    for parents in itertools.product(*choices):
        acyclic = True
        for start in range(4):
            visited = set()
            current = start
            while current is not None:
                if current in visited:
                    acyclic = False
                    break
                visited.add(current)
                current = parents[current]
        if not acyclic:
            continue
        monomial = list(ZERO)
        for i, parent in enumerate(parents):
            index = i if parent is None else 4 + EDGES.index((i, parent))
            monomial[index] += 1
        key = tuple(monomial)
        forests[key] = forests.get(key, 0) + 1
    return forests


def serialize(poly):
    return [{"powers": list(m), "coefficient": c} for m, c in sorted(poly.items())]


def main():
    matrix = [[{} for _ in range(4)] for _ in range(4)]
    for i in range(4):
        matrix[i][i] = variable(i)
    for index, (i, j) in enumerate(EDGES, 4):
        edge = variable(index)
        matrix[i][i] = add(matrix[i][i], edge)
        matrix[i][j] = scale(edge, -1)
    det = determinant(matrix)
    forest = rooted_forests()
    require(det == forest, "Leibniz determinant disagrees with forest enumeration")
    require(all(c > 0 for c in det.values()), "negative determinant coefficient")
    require(all(sum(m[:4]) >= 1 for m in det), "root-free determinant term")
    one_root = [sum(m[i] == 1 and sum(m[:4]) == 1 for m in det) for i in range(4)]
    require(all(one_root), "a surplus variable lacks a spanning-tree term")
    adj = []
    for i in range(4):
        row = []
        for j in range(4):
            minor = [[matrix[r][c] for c in range(4) if c != i]
                     for r in range(4) if r != j]
            polynomial = scale(determinant(minor), (-1) ** (i + j))
            require(all(c > 0 for c in polynomial.values()), "negative adjugate coefficient")
            require(any(sum(m[:4]) == 0 for m in polynomial), "no strictly positive edge-only term")
            row.append(polynomial)
        adj.append(row)
    for i in range(4):
        for j in range(4):
            product_entry = add(*(multiply(matrix[i][k], adj[k][j]) for k in range(4)))
            require(product_entry == (det if i == j else {}), "adjugate identity failed")
    sigma = (1, 0, 3, 2)
    centralizer = [p for p in itertools.permutations(range(4))
                   if all(p[sigma[i]] == sigma[p[i]] for i in range(4))]
    require(len(centralizer) == 8, "unexpected pair centralizer")
    # Test every strict order type. Weak orders follow by choosing any total
    # ordering consistent with the ties; the normalized inequalities are weak.
    for ranks in itertools.permutations(range(4)):
        require(any(ranks[p[0]] == max(ranks) and ranks[p[2]] >= ranks[p[3]]
                    for p in centralizer), "missing normalized order type")
    result = {
        "status": "exact_polynomial_identity_passed",
        "variables": NAMES,
        "matrix_definition": "M_ii=k_i+sum_j e_ij; M_ij=-e_ij on cross edges; otherwise zero",
        "cross_edges": EDGES,
        "domain": "k_i>=0; all eight e_ij>0",
        "determinant_equals_rooted_forest_sum": True,
        "determinant_terms": serialize(det),
        "one_root_spanning_tree_counts": one_root,
        "adjugate_terms": [[serialize(p) for p in row] for row in adj],
        "all_adjugate_entries_strictly_positive": True,
        "pair_specialization": {
            "column_permutation": [1, 0, 3, 2],
            "signature_diagonal": [1, 1, -1, -1],
            "surplus": "k_i=2*a_i-1",
            "invertibility_equivalent_to": "sum_i a_i > 2",
            "inverse_signs": [[1 if (i < 2) == (j < 2) else -1 for j in range(4)] for i in range(4)],
        },
        "contact_permutation_centralizer": centralizer,
        "canonical_inequalities": ["a0>=a1", "a0>=a2", "a0>=a3", "a2>=a3"],
        "canonical_order_types_checked": 24,
        "scope": "Matrix-structure identity; not an upper bound or an elimination of the pair branch.",
    }
    path = ROOT / "certificates/pair_matrix_structure.json"
    path.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"status": result["status"], "forest_terms": len(det),
                      "one_root_counts": one_root,
                      "adjugate_term_counts": [[len(p) for p in row] for row in adj]}))


if __name__ == "__main__":
    main()
