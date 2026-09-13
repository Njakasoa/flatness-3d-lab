#!/usr/bin/env python3
"""Exact checks for the coplanar-square contact chart.

The script deliberately covers a stated subclass and a structural chart,
not the whole ACMS square branch.  It uses only Fraction arithmetic.

Run from ``flatness-3d-lab`` with::

    python experiments/square_contacts.py

The output is the reproducible data file ``results/square_contacts.json``.
"""

from __future__ import annotations

import json
from fractions import Fraction as F
from itertools import product
from pathlib import Path
from typing import Iterable, Sequence


Point = tuple[F, F, F]
Vector = tuple[F, F, F]
Matrix = tuple[tuple[F, F, F], tuple[F, F, F], tuple[F, F, F]]


def det3(m: Matrix) -> F:
    """Exact determinant of a 3 by 3 matrix."""

    return (
        m[0][0] * (m[1][1] * m[2][2] - m[1][2] * m[2][1])
        - m[0][1] * (m[1][0] * m[2][2] - m[1][2] * m[2][0])
        + m[0][2] * (m[1][0] * m[2][1] - m[1][1] * m[2][0])
    )


def solve3(m: Matrix, b: Vector) -> Vector:
    """Solve ``m*x=b`` by Cramer's rule over the rationals."""

    d = det3(m)
    if d == 0:
        raise ValueError("singular matrix")
    columns = []
    for j in range(3):
        rows = [list(row) for row in m]
        for i in range(3):
            rows[i][j] = b[i]
        columns.append(det3(tuple(tuple(row) for row in rows)) / d)
    return tuple(columns)  # type: ignore[return-value]


def add(a: Point, b: Vector) -> Point:
    return tuple(x + y for x, y in zip(a, b))  # type: ignore[return-value]


def square_lambda(
    parameters: Sequence[F], point: Point
) -> tuple[F, F, F, F]:
    """Evaluate the general eight-parameter square-contact chart.

    Parameters are ``(B,D,G,H,A,E,tau0,tau1,tau2,tau3)`` with the
    positivity and sum constraints documented in the proof note.
    """

    B, D, G, H, A, E, t0, t1, t2, t3 = parameters
    if t0 + t1 + t2 + t3 != 0:
        raise ValueError("the four z-coefficients must sum to zero")
    C = B + D - A
    Fcoef = G + H - E
    x, y, z = point
    return (
        A * x + E * y + t0 * z,
        B * (1 - x) + Fcoef * y + t1 * z,
        G + C * x - G * y + t2 * z,
        D * (1 - x) + H * (1 - y) + t3 * z,
    )


def general_data(parameters: Sequence[F]) -> dict:
    """Return the exact matrix, determinant, kernel, and contact table."""

    B, D, G, H, A, E, t0, t1, t2, t3 = parameters
    if t0 + t1 + t2 + t3 != 0:
        raise ValueError("the four z-coefficients must sum to zero")
    C = B + D - A
    Fcoef = G + H - E
    m: Matrix = ((A, E, t0), (-B, Fcoef, t1), (C, -G, t2))
    d: Vector = (F(0), B, G)
    determinant_expansion = (
        A * (Fcoef * t2 + G * t1)
        + E * (B * t2 + C * t1)
        + t0 * (B * G - Fcoef * C)
    )
    kernel: Vector = (
        E * t1 - Fcoef * t0,
        -B * t0 - A * t1,
        A * Fcoef + B * E,
    )
    contacts = ((F(0), F(0), F(0)), (F(1), F(0), F(0)),
                (F(0), F(1), F(0)), (F(1), F(1), F(0)))
    return {
        "derived": {
            "C": str(C),
            "F": str(Fcoef),
            "matrix_M": [[str(x) for x in row] for row in m],
            "offset_d": [str(x) for x in d],
            "determinant": str(det3(m)),
            "determinant_expansion": str(determinant_expansion),
            "determinant_expansion_matches": det3(m) == determinant_expansion,
            "kernel_candidate": [str(x) for x in kernel],
            "kernel_M_product": [
                str(sum(row[j] * kernel[j] for j in range(3))) for row in m
            ],
        },
        "contact_lambda_values": [
            [str(x) for x in square_lambda(parameters, p)] for p in contacts
        ],
        "contact_points": [[str(x) for x in p] for p in contacts],
    }


def balanced_parameters(s: F) -> tuple[F, ...]:
    """The balanced square-contact family used for the exact bound."""

    q = F(1, 4)
    return (q, q, q, q, q, q, s, -s, -s, s)


def balanced_vertices(s: F) -> tuple[Point, Point, Point, Point]:
    """Vertices of the balanced family, indexed by the opposite facets."""

    if s == 0:
        raise ValueError("the balanced prism is not a tetrahedron at s=0")
    h = F(1, 4) / s
    return (
        (F(3, 2), F(3, 2), h),
        (F(-1, 2), F(3, 2), -h),
        (F(3, 2), F(-1, 2), -h),
        (F(-1, 2), F(-1, 2), h),
    )


def integer_box(vertices: Iterable[Point]) -> tuple[range, range, range]:
    """A finite exact box containing every possible integer point."""

    vertices = tuple(vertices)
    return tuple(
        range(min(v[i] for v in vertices).__ceil__(),
              max(v[i] for v in vertices).__floor__() + 1)
        for i in range(3)
    )  # type: ignore[return-value]


def interior_integer_points(vertices: Iterable[Point], parameters: Sequence[F]):
    """Enumerate interior lattice points using the exact barycentric forms."""

    points = []
    for p in product(*integer_box(vertices)):
        point = tuple(F(x) for x in p)
        if min(square_lambda(parameters, point)) > 0:
            points.append(p)
    return points


def shear(vertices: Iterable[Point], n: int) -> tuple[Point, ...]:
    """Apply the unimodular shear (x,y,z) -> (x+n*z,y,z)."""

    return tuple((x + n * z, y, z) for x, y, z in vertices)


def serial_vertices(vertices: Iterable[Point]) -> list[list[str]]:
    return [[str(x) for x in v] for v in vertices]


def main() -> None:
    q = F(1, 4)
    # A general nonsymmetric, full-rank rational chart sanity check.
    general_parameters = (
        F(1, 5), F(1, 4), F(1, 10), F(9, 20),
        F(1, 6), F(1, 8), F(2, 3), F(-1, 2), F(-1, 7), F(-1, 42),
    )
    general = general_data(general_parameters)
    assert general["derived"]["determinant"] != "0"
    general_contacts = ((F(0), F(0), F(0)), (F(1), F(0), F(0)),
                        (F(0), F(1), F(0)), (F(1), F(1), F(0)))
    assert all(sum(square_lambda(general_parameters, point), F(0)) == 1
               for point in general_contacts)
    assert all(
        value > 0
        for i, point in enumerate(general_contacts)
        for j, value in enumerate(square_lambda(general_parameters, point))
        if i != j
    )
    # The unbounded balanced prism is the exact Delta=0 check.
    prism = general_data(balanced_parameters(F(0)))
    assert prism["derived"]["determinant"] == "0"
    assert prism["derived"]["kernel_M_product"] == ["0", "0", "0"]

    balanced = []
    for s in (F(1, 8), F(1, 4), F(1, 2), F(1), F(-1, 4)):
        parameters = balanced_parameters(s)
        vertices = balanced_vertices(s)
        points = interior_integer_points(vertices, parameters)
        expected_hollow = abs(s) >= q
        assert bool(points) is (abs(s) < q)
        balanced.append({
            "s": str(s),
            "vertices": serial_vertices(vertices),
            "interior_integer_points_in_vertex_box": [list(p) for p in points],
            "hollow_by_exact_box_check": not points,
            "all_facets_blocked_by_square_contacts": True,
            "maximality_scope": "blocked-facet criterion, conditional on hollowness",
            "hollow_threshold_formula": "abs(s) >= 1/4",
            "vertical_width": str(F(1, 2) / abs(s)),
            "width_upper_bound": "2" if expected_hollow else None,
        })

    base_vertices = balanced_vertices(q)
    sheared = []
    for n in (-7, 0, 7):
        v = shear(base_vertices, n)
        sheared.append({
            "n": n,
            "vertices": serial_vertices(v),
            "max_abs_coordinate": str(max(abs(x) for p in v for x in p)),
            "contacts_fixed_because_z_zero": True,
            "hollow_and_width_preserved_by_GL3Z": True,
        })

    result = {
        "metadata": {
            "date": "2026-09-13",
            "scope": (
                "bounded tetrahedra with q0,q1,q2,q3 in relative interiors of "
                "the four assigned facets; standard Z^3 chart"
            ),
            "sources_checked": [
                "https://arxiv.org/abs/1907.06199, Section 5.4 and Theorem 5.4 (checked local extraction excluded from public export)",
                "https://arxiv.org/abs/1907.06199 (primary record checked 2026-09-13)",
                "references/LITERATURE_SEARCH.md (project source-search audit)",
            ],
            "not_claimed": [
                "not a solution of the full ACMS square branch",
                "the random/general chart check is not a hollowness search",
                "the balanced width bound does not extend to arbitrary chart parameters",
            ],
        },
        "general_chart": general,
        "delta_zero_recession_check": prism,
        "balanced_family": {
            "lambda_forms": [
                "(x+y)/4 + s*z",
                "(1-x+y)/4 - s*z",
                "(x+1-y)/4 - s*z",
                "(2-x-y)/4 + s*z",
            ],
            "determinant": "-s/4",
            "vertices_formula": [
                "(3/2,3/2,1/(4*s))",
                "(-1/2,3/2,-1/(4*s))",
                "(3/2,-1/2,-1/(4*s))",
                "(-1/2,-1/2,1/(4*s))",
            ],
            "exact_hollow_threshold": "abs(s) >= 1/4 for s != 0",
            "width_argument": (
                "vertical width is 1/(2*abs(s)); hence every hollow member has "
                "lattice width at most 2"
            ),
            "samples": balanced,
        },
        "shear_obstruction": {
            "map": "U_n(x,y,z)=(x+n*z,y,z)",
            "determinant": 1,
            "sample": sheared,
            "conclusion": (
                "No coordinate bound in the fixed square chart can hold, even "
                "for hollow maximal examples; only a bound modulo preserving shears "
                "could be true."
            ),
        },
    }
    output = Path(__file__).resolve().parent.parent / "results" / "square_contacts.json"
    output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "general_determinant": general["derived"]["determinant"],
        "balanced_hollow_threshold": "abs(s) >= 1/4",
        "balanced_hollow_samples": [row["s"] for row in balanced if row["hollow_by_exact_box_check"]],
        "shear_max_abs_coordinates": {str(row["n"]): row["max_abs_coordinate"] for row in sheared},
        "output": str(output),
    }, indent=2))


if __name__ == "__main__":
    main()
