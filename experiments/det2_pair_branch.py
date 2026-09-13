"""Bounded audit of the determinant-two 2+2 blocker branch.

The script is deliberately a finite exploration.  It records the exact
two-roof chart, the four corner-fibre consequences of hollowness, and an
exact rational symmetric witness.  The random part is only a search for a
counterexample; it is never used as a proof of a uniform width bound.

Run from ``flatness-3d-lab`` with ``.venv/bin/python``.  The only output file
written by this script is ``results/det2_pair_branch.json``.
"""

from __future__ import annotations

import itertools
import json
import math
import time
from fractions import Fraction
from pathlib import Path

import numpy as np


HERE = Path(__file__).resolve().parents[1]
OUT = HERE / "results" / "det2_pair_branch.json"


# The contact points in the unimodular (u,v,w) chart are the odd cube corners.
CONTACTS = np.array(
    [[1.0, 1.0, 1.0], [0.0, 0.0, 1.0], [1.0, 0.0, 0.0], [0.0, 1.0, 0.0]]
)


def roof_planes(t: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Return H,b for H @ (u,v,w) <= b.

    The four rows are respectively the two lower roofs and the two upper
    roofs.  The parameters are ordered ``a,b,c,d,e,f,g,h`` as in the proof
    note.
    """

    a, b, c, d, e, f, g, h = map(float, t)
    H = np.array(
        [[a, b, -1.0], [-c, -d, -1.0], [e, -f, 1.0], [-g, h, 1.0]],
        dtype=float,
    )
    rhs = np.array([-1.0 + a + b, -1.0, e, h], dtype=float)
    return H, rhs


def roof_vertices(t: np.ndarray) -> np.ndarray | None:
    """Enumerate the four feasible triple intersections, if nondegenerate."""

    H, rhs = roof_planes(t)
    vertices: list[np.ndarray] = []
    for ids in itertools.combinations(range(4), 3):
        try:
            vertex = np.linalg.solve(H[list(ids)], rhs[list(ids)])
        except np.linalg.LinAlgError:
            continue
        if np.all(H @ vertex <= rhs + 2.0e-9):
            vertices.append(vertex)
    if len(vertices) != 4:
        return None
    if abs(np.linalg.det(np.c_[np.asarray(vertices[1:]) - vertices[0]])) < 1.0e-10:
        return None
    return np.asarray(vertices)


def primitive_directions() -> list[tuple[int, int, int]]:
    """Finite direction list sufficient whenever the width is below four.

    The contact tetrahedron is contained in K.  Its width in a direction is
    ``ptp(CONTACTS @ u)``.  Any direction with contact width > 3 cannot
    minimize a body whose width is at most 3.  Enumerating the resulting
    bounded set, rather than imposing an arbitrary direction radius, is the
    finite screen used here.
    """

    directions: list[tuple[int, int, int]] = []
    for u in itertools.product(range(-8, 9), repeat=3):
        if not any(u):
            continue
        if math.gcd(*u) != 1:
            continue
        first = next(x for x in u if x)
        if first < 0:
            continue
        if np.ptp(CONTACTS @ np.asarray(u, dtype=float)) <= 3.0 + 1.0e-12:
            directions.append(tuple(int(x) for x in u))
    return directions


DIRECTIONS = primitive_directions()


def directional_minimum(vertices: np.ndarray) -> tuple[float, tuple[int, int, int]]:
    values = [(float(np.ptp(vertices @ np.asarray(u, dtype=float))), u) for u in DIRECTIONS]
    return min(values)


def fraction_inverse(matrix: list[list[Fraction]]) -> list[list[Fraction]]:
    """Small exact Gauss-Jordan inverse used by the witness check."""

    n = len(matrix)
    work = [list(row) + [Fraction(int(i == j)) for j in range(n)] for i, row in enumerate(matrix)]
    for col in range(n):
        pivot = next((row for row in range(col, n) if work[row][col]), None)
        if pivot is None:
            raise ValueError("singular exact matrix")
        work[col], work[pivot] = work[pivot], work[col]
        scale = work[col][col]
        work[col] = [x / scale for x in work[col]]
        for row in range(n):
            if row == col:
                continue
            scale = work[row][col]
            if scale:
                work[row] = [x - scale * y for x, y in zip(work[row], work[col])]
    return [row[n:] for row in work]


def interior_integer_points(vertices: np.ndarray, cap: int = 100_000) -> tuple[str, list[tuple[int, int, int]]]:
    """Scan the full integer bounding box, with an explicit work cap."""

    lo = np.ceil(vertices.min(axis=0) - 1.0e-9).astype(int)
    hi = np.floor(vertices.max(axis=0) + 1.0e-9).astype(int)
    box_size = int(np.prod(hi - lo + 1))
    if box_size > cap:
        return "box_cap", []
    inverse = np.linalg.inv(np.c_[vertices, np.ones(4)].T)
    inside: list[tuple[int, int, int]] = []
    for point in itertools.product(*(range(int(lo[i]), int(hi[i]) + 1) for i in range(3))):
        bary = np.asarray([*point, 1.0]) @ inverse.T
        if np.all(bary > 1.0e-8):
            inside.append(tuple(int(x) for x in point))
    return ("hollow" if not inside else "nonhollow"), inside


def corner_conditions(t: np.ndarray) -> dict[str, bool]:
    """Necessary corner-fibre tests forced by hollowness."""

    a, b, c, d, e, f, g, h = map(float, t)
    return {
        "(0,0): min(e,h)<=2": min(e, h) <= 2.0,
        "(1,1): min(f,g)<=2": min(f, g) <= 2.0,
        "(1,0): min(b,c)<=2": min(b, c) <= 2.0,
        "(0,1): min(a,d)<=2": min(a, d) <= 2.0,
    }


def exact_symmetric_witness() -> dict[str, object]:
    """Exact M=2 witness, reconstructed without floating point decisions."""

    vertices = [
        [Fraction(5, 4), Fraction(-1, 4), Fraction(-1)],
        [Fraction(-1, 4), Fraction(5, 4), Fraction(-1)],
        [Fraction(5, 4), Fraction(5, 4), Fraction(2)],
        [Fraction(-1, 4), Fraction(-1, 4), Fraction(2)],
    ]
    matrix = [
        [vertices[j][i] for j in range(4)] for i in range(3)
    ] + [[Fraction(1) for _ in range(4)]]
    inverse = fraction_inverse(matrix)
    interior: list[list[int]] = []
    for point in itertools.product(range(0, 2), range(0, 2), range(-1, 3)):
        bary = [
            sum(Fraction(point[i]) * inverse[j][i] for i in range(3)) + inverse[j][3]
            for j in range(4)
        ]
        if all(x > 0 for x in bary):
            interior.append(list(point))

    exact_widths: list[tuple[Fraction, tuple[int, int, int]]] = []
    for direction in DIRECTIONS:
        values = [
            sum(Fraction(direction[i]) * vertices[j][i] for i in range(3))
            for j in range(4)
        ]
        exact_widths.append((max(values) - min(values), direction))
    best = min(exact_widths)

    # Recover the row-stochastic contact matrix directly from facet slacks.
    # Row i is the normalized vector of slacks of its facet at the four
    # contact points; its assigned contact has slack zero.
    facet_normals = [
        [Fraction(2), Fraction(2), Fraction(-1)],
        [Fraction(-2), Fraction(-2), Fraction(-1)],
        [Fraction(2), Fraction(-2), Fraction(1)],
        [Fraction(-2), Fraction(2), Fraction(1)],
    ]
    facet_rhs = [Fraction(3), Fraction(-1), Fraction(2), Fraction(2)]
    contact_matrix: list[list[str]] = []
    for normal, rhs in zip(facet_normals, facet_rhs):
        slacks = [
            rhs - sum(normal[i] * Fraction(CONTACTS[j, i]) for i in range(3))
            for j in range(4)
        ]
        total = sum(slacks, Fraction(0))
        contact_matrix.append([str(x / total) for x in slacks])

    return {
        "parameters": {name: "2" for name in "abcdefgh"},
        "vertices": [[str(x) for x in row] for row in vertices],
        "integer_box": [[0, 1], [0, 1], [-1, 2]],
        "interior_points": interior,
        "hollow_certified": not interior,
        "lattice_width": str(best[0]),
        "minimizing_directions": [list(u) for width, u in exact_widths if width == best[0]],
        "contact_matrix": contact_matrix,
        "interpretation": "nonempty exact witness; it does not prove a uniform upper bound",
    }


def exact_roof_vertices(parameters: list[Fraction]) -> list[list[Fraction]] | None:
    """Exact triple-intersection reconstruction for a finite-slope roof."""

    a, b, c, d, e, f, g, h = parameters
    H = [[a, b, Fraction(-1)], [-c, -d, Fraction(-1)], [e, -f, Fraction(1)], [-g, h, Fraction(1)]]
    rhs = [-1 + a + b, Fraction(-1), e, h]
    vertices: list[list[Fraction]] = []
    for ids in itertools.combinations(range(4), 3):
        inverse = fraction_inverse([H[i] for i in ids])
        vertex = [
            sum(inverse[row][col] * rhs[ids[col]] for col in range(3))
            for row in range(3)
        ]
        if all(sum(H[i][j] * vertex[j] for j in range(3)) <= rhs[i] for i in range(4)):
            vertices.append(vertex)
    return vertices if len(vertices) == 4 else None


def exact_roof_scan(parameters: list[Fraction]) -> dict[str, object]:
    """Exact hollow and width check for one rational roof sample."""

    vertices = exact_roof_vertices(parameters)
    if vertices is None:
        return {"status": "degenerate"}
    matrix = [[vertices[j][i] for j in range(4)] for i in range(3)] + [[Fraction(1)] * 4]
    inverse = fraction_inverse(matrix)

    def floor_fraction(x: Fraction) -> int:
        return x.numerator // x.denominator

    def ceil_fraction(x: Fraction) -> int:
        return -((-x).numerator // (-x).denominator)

    lo = [ceil_fraction(min(v[i] for v in vertices)) for i in range(3)]
    hi = [floor_fraction(max(v[i] for v in vertices)) for i in range(3)]
    interior: list[list[int]] = []
    for point in itertools.product(*(range(lo[i], hi[i] + 1) for i in range(3))):
        bary = [
            sum(Fraction(point[i]) * inverse[j][i] for i in range(3)) + inverse[j][3]
            for j in range(4)
        ]
        if all(x > 0 for x in bary):
            interior.append(list(point))

    widths: list[tuple[Fraction, tuple[int, int, int]]] = []
    for direction in DIRECTIONS:
        values = [sum(Fraction(direction[i]) * v[i] for i in range(3)) for v in vertices]
        widths.append((max(values) - min(values), direction))
    best = min(widths)
    return {
        "parameters": [str(x) for x in parameters],
        "vertices": [[str(x) for x in v] for v in vertices],
        "integer_box": [lo, hi],
        "interior_points": interior,
        "hollow_certified": not interior,
        "lattice_width": str(best[0]),
        "lattice_width_decimal": float(best[0]),
        "minimizing_direction": list(best[1]),
    }


def exact_high_width_sample() -> dict[str, object]:
    """A rationalized high-width hollow sample from the bounded search."""

    decimals = [1.03135625, 6.51602411, 1.13787099, 1.05376977, 1.99847345, 1.11572430, 3.41388019, 6.14250577]
    parameters = [Fraction(str(x)).limit_denominator(1000) for x in decimals]
    result = exact_roof_scan(parameters)
    result["source"] = "deterministic exploratory sample; denominator <=1000 rationalization"
    result["interpretation"] = "exact hollow witness below width three, not a uniform upper-bound certificate"
    return result


def numeric_scan() -> dict[str, object]:
    """Run a deterministic, capped exploratory search."""

    rng = np.random.default_rng(20260913)
    attempted = 0
    feasible = 0
    hollow = 0
    nonhollow = 0
    box_cap = 0
    best: dict[str, object] | None = None
    for _ in range(768):
        attempted += 1
        parameters = 1.0 + 10.0 ** rng.uniform(-4.0, 1.1, size=8)
        if not all(corner_conditions(parameters).values()):
            continue
        vertices = roof_vertices(parameters)
        if vertices is None:
            continue
        feasible += 1
        status, interior = interior_integer_points(vertices)
        if status == "box_cap":
            box_cap += 1
            continue
        if status == "hollow":
            hollow += 1
            width, direction = directional_minimum(vertices)
            candidate = {
                "width_upper_screen": width,
                "direction": list(direction),
                "parameters": [float(x) for x in parameters],
                "integer_box_status": status,
            }
            if best is None or width > float(best["width_upper_screen"]):
                best = candidate
        else:
            nonhollow += 1

    return {
        "seed": 20260913,
        "attempted": attempted,
        "feasible_roof_tetrahedra": feasible,
        "numeric_hollow": hollow,
        "numeric_nonhollow": nonhollow,
        "box_cap": box_cap,
        "best_hollow_sample": best,
        "scope": "finite random screen with full integer-box scan when box <=100000",
        "does_not_prove": "a uniform width bound or absence of an asymmetric counterexample",
    }


def main() -> None:
    started = time.monotonic()
    result = {
        "status": "bounded_exploration_inconclusive",
        "branch": "determinant_2_two_plus_two_sigma_(01)(23)",
        "chart": {
            "contact_vertices_uvw": CONTACTS.astype(int).tolist(),
            "integer_change_of_coordinates": {
                "u": "1-Z",
                "v": "1-Y",
                "w": "1+X-Y-Z",
                "inverse": "(X,Y,Z)=(w-u-v+1,1-v,1-u)",
            },
            "inequalities": [
                "w >= 1+a(u-1)+b(v-1)",
                "w >= 1-cu-dv",
                "w <= e(1-u)+fv",
                "w <= gu+h(1-v)",
            ],
            "strict_parameter_domain": "a,b,c,d,e,f,g,h > 1",
            "scope_limit": "finite slopes correspond to designated A_ij>1/2; A_ij=1/2 is a vertical-facet limit omitted from this chart",
        },
        "corner_fibre_necessary_conditions": [
            "min(e,h) <= 2 at (u,v)=(0,0)",
            "min(f,g) <= 2 at (u,v)=(1,1)",
            "min(b,c) <= 2 at (u,v)=(1,0)",
            "min(a,d) <= 2 at (u,v)=(0,1)",
        ],
        "direction_count_below_contact_width_4": len(DIRECTIONS),
        "exact_symmetric_witness": exact_symmetric_witness(),
        "exact_high_width_sample": exact_high_width_sample(),
        "numeric_scan": numeric_scan(),
        "elapsed_seconds": time.monotonic() - started,
    }
    OUT.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"status": result["status"], "output": str(OUT), "directions": len(DIRECTIONS)}, indent=2))


if __name__ == "__main__":
    main()
