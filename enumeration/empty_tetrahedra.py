#!/usr/bin/env python3
"""Enumerate empty lattice tetrahedra of determinant at most 17.

This is the finite contact-tetrahedron branch of ACMS Theorem 5.4.  The
enumeration is deliberately narrower than a classification of all maximal
lattice-free bodies: it lists lattice tetrahedra P up to translation,
GL(3,Z), and vertex relabeling, with no lattice point other than the four
vertices (including boundary points).

For an ordered anchored tetrahedron with column matrix B, the ordered orbit
representative is

    H = HNF(B.T).T,

where SymPy's column Hermite normal form gives

    [[a, 0, 0], [b, d, 0], [c, e, f]],

with a,d,f > 0, 0 <= b,c < a and 0 <= e < d.  Every ordered GL(3,Z)
orbit has exactly one such H.  We enumerate all H with a*d*f <= 17, test
emptiness exactly by integer barycentric numerators, and canonicalize over the
24 anchor/vertex orders.

The resulting JSON is an auditable candidate list for the ACMS contact branch;
it is not a proof of the flatness conjecture and says nothing about the square
branch or nonsimplicial contact polytopes.
"""

from __future__ import annotations

import argparse
import itertools
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Iterable, Sequence

from sympy import Matrix
from sympy.matrices.normalforms import hermite_normal_form


MAX_DETERMINANT = 17
VERTEX_PERMUTATIONS = tuple(itertools.permutations(range(4)))


def hnf_from_columns(columns: Sequence[Sequence[int]]) -> tuple[tuple[int, ...], ...]:
    """Return HNF(B.T).T for a 3-column integer matrix B."""

    b = Matrix.hstack(*(Matrix(tuple(int(x) for x in col)) for col in columns))
    h = hermite_normal_form(b.T).T
    return tuple(tuple(int(h[i, j]) for j in range(3)) for i in range(3))


def matrix_columns(h: Sequence[Sequence[int]]) -> tuple[tuple[int, int, int], ...]:
    """Read the three vertex vectors from the columns of H."""

    return tuple(tuple(int(h[i][j]) for i in range(3)) for j in range(3))


def adjugate_3x3(b: Sequence[Sequence[int]]) -> tuple[tuple[int, ...], ...]:
    """Return the integer adjugate of a 3x3 matrix."""

    a = b
    return (
        (
            a[1][1] * a[2][2] - a[1][2] * a[2][1],
            a[0][2] * a[2][1] - a[0][1] * a[2][2],
            a[0][1] * a[1][2] - a[0][2] * a[1][1],
        ),
        (
            a[1][2] * a[2][0] - a[1][0] * a[2][2],
            a[0][0] * a[2][2] - a[0][2] * a[2][0],
            a[0][2] * a[1][0] - a[0][0] * a[1][2],
        ),
        (
            a[1][0] * a[2][1] - a[1][1] * a[2][0],
            a[0][1] * a[2][0] - a[0][0] * a[2][1],
            a[0][0] * a[1][1] - a[0][1] * a[1][0],
        ),
    )


def determinant_3x3(b: Sequence[Sequence[int]]) -> int:
    """Return det(b), using rows as supplied."""

    return (
        b[0][0] * (b[1][1] * b[2][2] - b[1][2] * b[2][1])
        - b[0][1] * (b[1][0] * b[2][2] - b[1][2] * b[2][0])
        + b[0][2] * (b[1][0] * b[2][1] - b[1][1] * b[2][0])
    )


def barycentric_numerators(
    point: Sequence[int], b: Sequence[Sequence[int]], adj: Sequence[Sequence[int]]
) -> tuple[int, int, int]:
    """Return D times the three non-anchor barycentric coordinates."""

    return tuple(sum(adj[i][j] * int(point[j]) for j in range(3)) for i in range(3))


def in_tetrahedron(
    point: Sequence[int],
    b: Sequence[Sequence[int]],
    adj: Sequence[Sequence[int]],
    determinant: int,
) -> bool:
    """Exact closed-tetrahedron membership using integer barycentrics."""

    nums = barycentric_numerators(point, b, adj)
    return min(nums) >= 0 and sum(nums) <= determinant


def lattice_points_in_tetrahedron(
    h: Sequence[Sequence[int]],
) -> tuple[tuple[int, int, int], ...]:
    """Enumerate all integer points in the closed tetrahedron conv(0, cols(H))."""

    columns = matrix_columns(h)
    # Rows of b are coordinate rows; columns are the three non-anchor vertices.
    b = tuple(tuple(int(h[i][j]) for j in range(3)) for i in range(3))
    determinant = abs(determinant_3x3(b))
    if determinant == 0:
        raise ValueError("degenerate tetrahedron")
    if determinant < 0:
        raise AssertionError("absolute determinant unexpectedly negative")
    adj = adjugate_3x3(b)
    maxima = tuple(max((0, *(column[i] for column in columns))) for i in range(3))
    points: list[tuple[int, int, int]] = []
    for x in range(maxima[0] + 1):
        for y in range(maxima[1] + 1):
            for z in range(maxima[2] + 1):
                point = (x, y, z)
                if in_tetrahedron(point, b, adj, determinant):
                    points.append(point)
    return tuple(points)


def is_empty(h: Sequence[Sequence[int]]) -> bool:
    """An empty lattice tetrahedron has exactly its four vertices as points."""

    columns = matrix_columns(h)
    vertices = {(0, 0, 0), *columns}
    return set(lattice_points_in_tetrahedron(h)) == vertices


def canonical_key(h: Sequence[Sequence[int]]) -> tuple[int, ...]:
    """Canonical key over all 24 choices of anchor and vertex order."""

    columns = ((0, 0, 0), *matrix_columns(h))
    representatives = []
    for permutation in VERTEX_PERMUTATIONS:
        anchor = columns[permutation[0]]
        ordered = tuple(
            tuple(columns[index][coordinate] - anchor[coordinate] for coordinate in range(3))
            for index in permutation[1:]
        )
        rep = hnf_from_columns(ordered)
        representatives.append(tuple(rep[row][column] for row in range(3) for column in range(3)))
    return min(representatives)


def key_to_matrix(key: Sequence[int]) -> tuple[tuple[int, ...], ...]:
    return tuple(tuple(int(key[3 * i + j]) for j in range(3)) for i in range(3))


def enumerate_hnf_matrices(max_determinant: int) -> Iterable[tuple[tuple[int, ...], ...]]:
    """Enumerate all lower triangular row-HNF matrices with det <= max."""

    for a in range(1, max_determinant + 1):
        for d in range(1, max_determinant // a + 1):
            for f in range(1, max_determinant // (a * d) + 1):
                determinant = a * d * f
                for b in range(a):
                    for c in range(a):
                        for e in range(d):
                            yield ((a, 0, 0), (b, d, 0), (c, e, f))


def serialize_matrix(h: Sequence[Sequence[int]]) -> list[list[int]]:
    return [list(map(int, row)) for row in h]


def run(max_determinant: int = MAX_DETERMINANT) -> dict:
    all_hnf = list(enumerate_hnf_matrices(max_determinant))
    by_det: Counter[int] = Counter()
    empty_by_det: Counter[int] = Counter()
    empty_hnf: list[tuple[tuple[int, ...], ...]] = []
    for h in all_hnf:
        determinant = h[0][0] * h[1][1] * h[2][2]
        by_det[determinant] += 1
        if is_empty(h):
            empty_by_det[determinant] += 1
            empty_hnf.append(h)

    classes: dict[tuple[int, ...], tuple[tuple[int, ...], ...]] = {}
    for h in empty_hnf:
        key = canonical_key(h)
        classes.setdefault(key, key_to_matrix(key))

    classes_by_det: defaultdict[int, list[tuple[int, ...]]] = defaultdict(list)
    for key in sorted(classes):
        h = classes[key]
        determinant = h[0][0] * h[1][1] * h[2][2]
        classes_by_det[determinant].append(key)

    # Recheck all canonical representatives independently of the first pass.
    for key, h in classes.items():
        if not is_empty(h):
            raise AssertionError(f"canonical representative is not empty: {key}")
        if canonical_key(h) != key:
            raise AssertionError(f"canonical key is not idempotent: {key}")

    return {
        "metadata": {
            "cutoff_date": "2026-09-13",
            "max_normalized_determinant": max_determinant,
            "dimension": 3,
            "objects": "empty lattice tetrahedra, closed-tetrahedron convention",
            "equivalence": "translation + GL(3,Z) + vertex permutations",
            "ordered_hnf": "H = HNF(B.T).T; H rows [[a,0,0],[b,d,0],[c,e,f]], 0<=b,c<a, 0<=e<d",
            "scope": "ACMS Theorem 5.4 tetrahedral inscribed-contact branch only",
            "not_claimed": [
                "not a classification of maximal lattice-free bodies",
                "does not include the ACMS square branch",
                "does not include nonsimplicial contact polytopes",
                "does not prove the global flatness conjecture",
            ],
        },
        "counts": {
            "ordered_hnf_candidates": len(all_hnf),
            "ordered_empty_hnf": len(empty_hnf),
            "unlabeled_gl3z_classes": len(classes),
            "ordered_hnf_by_determinant": {str(k): by_det[k] for k in sorted(by_det)},
            "ordered_empty_hnf_by_determinant": {
                str(k): empty_by_det[k] for k in sorted(empty_by_det)
            },
            "unlabeled_classes_by_determinant": {
                str(k): len(classes_by_det[k]) for k in sorted(classes_by_det)
            },
        },
        "classes": [
            {
                "normalized_determinant": h[0][0] * h[1][1] * h[2][2],
                "hnf": serialize_matrix(h),
                "vertices": [[0, 0, 0], *[list(v) for v in matrix_columns(h)]],
                "closed_lattice_points": [list(p) for p in lattice_points_in_tetrahedron(h)],
            }
            for key, h in sorted(classes.items())
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--max-determinant", type=int, default=MAX_DETERMINANT)
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(__file__).resolve().parent.parent
        / "results"
        / "empty_contact_tetrahedra.json",
    )
    args = parser.parse_args()
    result = run(args.max_determinant)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result["counts"], indent=2))


if __name__ == "__main__":
    main()
