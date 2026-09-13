r"""Exact independent control for the Hurkens planar triangle.

Run from ``flatness-3d-lab`` as::

    python experiments/planar_control.py

All proof decisions use ``src.exact.Q`` in :math:`\mathbb Q(\sqrt 3)`.
The width check is deliberately written here rather than delegated to the
generic certificate routine: the inverse of two edge-difference forms gives
an exact finite radius, after which the four primitive direction classes in
``[-1,1]^2`` are enumerated.
"""

from __future__ import annotations

import json
import sys
from fractions import Fraction as F
from math import gcd
from pathlib import Path


# Permit ``python experiments/planar_control.py`` as well as module execution.
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.exact import Q  # noqa: E402
from src.geometry import Polytope, certify_hollow, simplex_automorphisms  # noqa: E402


def R(a=0, b=0):
    """Return ``a + b*sqrt(3)`` as an exact field element."""

    return Q(F(a), F(b), 3)


def vec_add(a, b):
    return tuple(x + y for x, y in zip(a, b))


def vec_scale(c, a):
    return tuple(c * x for x in a)


def point_json(p):
    """Serialize a point, collapsing exact integral Q-elements to integers."""

    answer = []
    for x in p:
        x = Q.coerce(x)
        answer.append(int(x.a) if x.integer() else x.json())
    return answer


def canonical_direction(u):
    """Choose one representative of ``{u,-u}`` with primitive gcd one."""

    a, b = u
    g = gcd(abs(a), abs(b))
    if g != 1:
        raise ValueError(f"non-primitive direction {u}")
    if a < 0 or (a == 0 and b < 0):
        return (-a, -b)
    return (a, b)


def directional_width(vertices, u):
    values = [u[0] * v[0] + u[1] * v[1] for v in vertices]
    return max(values) - min(values)


def qsqrt3_vertices():
    """The type-3 equality triangle for contacts (0,0),(0,1),(1,0).

    The cyclic order here is q1--q2--q3.  In this order the edge contacts
    are c12=(0,0), c23=(0,1), c31=(1,0), and

        c_{i,i+1} = (1/sqrt(3))*q_i
                         + (1-1/sqrt(3))*q_{i+1}.
    """

    return (
        (R(F(2, 3)), R(F(-1, 3), F(-1, 3))),
        (R(F(-1, 3), F(-1, 3)), R(F(2, 3), F(1, 3))),
        (R(F(2, 3), F(1, 3)), R(F(2, 3))),
    )


def main():
    vertices = qsqrt3_vertices()
    K = Polytope(vertices)

    sqrt3 = R(0, 1)
    lam = sqrt3 / 3  # 1/sqrt(3)
    mu = 1 - lam
    target = R(3, 2) / 3  # 1 + 2/sqrt(3)

    # Exact edge contacts and the source theorem's equality parameter.
    contacts = [
        vec_add(vec_scale(lam, vertices[i]), vec_scale(mu, vertices[(i + 1) % 3]))
        for i in range(3)
    ]
    expected_contacts = ((0, 0), (0, 1), (1, 0))
    assert tuple(contacts) == expected_contacts

    # Any integer point of K has each coordinate strictly between -1 and 2.
    # Thus only (0,0),(0,1),(1,0),(1,1) can occur.  The first three are
    # contacts; the barycentric coordinates of (1,1) include a negative entry.
    coordinate_min = [min(v[j] for v in vertices) for j in range(2)]
    coordinate_max = [max(v[j] for v in vertices) for j in range(2)]
    assert all(-1 < x < 2 for x in coordinate_min + coordinate_max)
    barycentric_11 = (1 - 2 * sqrt3 / 3, -1 + 2 * sqrt3 / 3, 1)
    assert barycentric_11[0] < 0
    assert sum(barycentric_11, Q()) == 1
    reconstructed_11 = tuple(
        sum(barycentric_11[i] * vertices[i][j] for i in range(3))
        for j in range(2)
    )
    assert reconstructed_11 == (1, 1)

    hollow = certify_hollow(K)
    assert hollow["hollow"]
    assert set(map(tuple, hollow["boundary_points"])) == set(expected_contacts)
    assert hollow["interior_points"] == []

    # Width formula.  If u=(a,b), three times the three pairwise vertex
    # differences are L12,L23,L31.  Consequently width(u) is the maximum of
    # their absolute values divided by three.
    B = R(3, 2)       # 3+2*sqrt(3) = 3*(1+2/sqrt(3))
    D = R(3, 1)       # 3+sqrt(3)
    S = sqrt3
    delta = R(18, 9)  # B*D+S^2 = 9*(2+sqrt(3))

    def edge_forms(u):
        a, b = u
        return (
            -D * a + B * b,  # 3*(q2-q1).u
            B * a - S * b,   # 3*(q3-q2).u
            -S * a - D * b,  # 3*(q1-q3).u
        )

    for u in ((1, 0), (0, 1), (1, 1), (1, -1), (2, 1), (-1, 2)):
        forms = edge_forms(u)
        assert max(abs(x) for x in forms) / 3 == directional_width(vertices, u)

    # Finite-radius argument.  If width(u) <= target, then |L23|,|L31| <= B.
    # Solving [B,-S; -S,-D]*(a,b)^T=(L23,L31)^T gives
    #   |a| <= B*(D+S)/delta = B^2/delta,
    #   |b| <= B*(B+S)/delta.
    # Both exact bounds are <2, hence an integer u lies in [-1,1]^2.
    bound_a = B * B / delta
    bound_b = B * (B + S) / delta
    assert D + S == B
    assert bound_a < 2
    assert bound_b < 2

    box_directions = []
    for a in range(-1, 2):
        for b in range(-1, 2):
            if (a, b) == (0, 0) or gcd(abs(a), abs(b)) != 1:
                continue
            c = canonical_direction((a, b))
            if c not in box_directions:
                box_directions.append(c)
    box_directions.sort()
    box_widths = {str(u): directional_width(vertices, u) for u in box_directions}
    assert all(w >= target for w in box_widths.values())
    minimizing = [u for u in box_directions if box_widths[str(u)] == target]
    assert minimizing == [(0, 1), (1, 0), (1, 1)]

    # The affine lattice symmetry cycles the three vertices and contacts.
    # U is in GL(2,Z), U^3=I, and U*q_i+t=q_{i+1}.
    U = ((0, 1), (-1, -1))
    t = (0, 1)
    transformed = [
        (U[0][0] * v[0] + U[0][1] * v[1] + t[0],
         U[1][0] * v[0] + U[1][1] * v[1] + t[1])
        for v in vertices
    ]
    assert transformed == [vertices[1], vertices[2], vertices[0]]

    result = {
        "body": "Hurkens planar extremal triangle in Z^2",
        "normalization": {
            "contacts": [list(p) for p in expected_contacts],
            "vertex_order": "q1,q2,q3; contact c_i lies on q_i--q_{i+1}",
            "lambda": "1/sqrt(3)=sqrt(3)/3",
            "mu": "1-1/sqrt(3)",
        },
        "vertices": K.json(),
        "area": K.volume().json(),
        "contact_certificate": {
            "exact_contacts": [point_json(p) for p in contacts],
            "all_three_edges_have_relative_interior_contact": True,
        },
        "hollow_certificate": hollow,
        "width_certificate": {
            "status": "certified_lattice_width",
            "width": target.json(),
            "minimizing_directions_mod_sign": [list(u) for u in minimizing],
            "upper_certificate": {
                "direction": [0, 1],
                "value": target.json(),
            },
            "lower_certificate": {
                "checked_minimum_in_radius_box": target.json(),
                "all_radius_box_directions_checked": True,
                "finite_radius_argument": "width(u)<=W implies |a|<2 and |b|<2, hence u in [-1,1]^2",
            },
            "search_bound": {
                "target_times_three": B.json(),
                "edge_forms_times_three": [
                    "-(3+sqrt(3))*a + (3+2*sqrt(3))*b",
                    "(3+2*sqrt(3))*a - sqrt(3)*b",
                    "-sqrt(3)*a - (3+sqrt(3))*b",
                ],
                "linear_system_determinant_abs": delta.json(),
                "coordinate_bounds_if_width_le_target": {
                    "a_abs_lt": bound_a.json(),
                    "b_abs_lt": bound_b.json(),
                    "integer_box": [[-1, 1], [-1, 1]],
                },
                "enumerated_primitive_directions_mod_sign": [list(u) for u in box_directions],
                "exact_widths_in_box": {k: v.json() for k, v in box_widths.items()},
            },
        },
        "lattice_automorphisms": simplex_automorphisms(K),
        "independent_exact_checks": {
            "coordinate_bounds": {
                "min": [x.json() for x in coordinate_min],
                "max": [x.json() for x in coordinate_max],
            },
            "(1,1)_barycentric": [Q.coerce(x).json() for x in barycentric_11],
            "symmetry_matrix": [list(row) for row in U],
            "symmetry_translation": list(t),
            "symmetry_order_three": True,
        },
    }

    out = ROOT / "certificates" / "planar_control.json"
    out.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({
        "width": str(target),
        "area": str(K.volume()),
        "minimizing_directions_mod_sign": minimizing,
        "hollow_boundary_points": hollow["boundary_points"],
        "hollow_interior_points": hollow["interior_points"],
        "finite_radius_box": [[-1, 1], [-1, 1]],
        "certificate": str(out.relative_to(ROOT)),
    }, indent=2))


if __name__ == "__main__":
    main()
