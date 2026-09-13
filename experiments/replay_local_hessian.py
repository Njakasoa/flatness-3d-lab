#!/usr/bin/env python3
"""Exact SymPy replay of the qualitative local-maximality certificate.

The script reconstructs the eight-variable lattice perturbation chart in
Sections 2–3 of ACMS (arXiv:1907.06199v2).  It checks, over Q(sqrt(2)), the
six cubic polynomials h_i, the rank-five gradient dependence, the
three-dimensional nullspace, the restricted Hessian printed in the paper,
and negative definiteness of the auxiliary Hessian for c=1/100.

This is deliberately the qualitative argument.  It does not reproduce the
paper's 14-hour degree-16 coefficient-majorant calculation for the explicit
0.02614 neighborhood; that computation belongs to Section 4.
"""

from __future__ import annotations

import json
from pathlib import Path

import sympy as sp


R = sp.sqrt(2)
ZERO = sp.Integer(0)


def vec(*entries: object) -> sp.Matrix:
    return sp.Matrix([sp.sympify(x) for x in entries])


def exact_sign(expr: sp.Expr) -> int:
    """Return the algebraic sign, requiring SymPy to decide it exactly."""

    sign = sp.sign(sp.radsimp(sp.factor(expr)))
    if sign not in (-1, 0, 1):
        raise AssertionError(f"undecided algebraic sign: {expr}")
    return int(sign)


def matrix_strings(matrix: sp.Matrix) -> list[list[str]]:
    return [[sp.sstr(sp.radsimp(sp.factor(matrix[i, j]))) for j in range(matrix.cols)] for i in range(matrix.rows)]


def principal_minors(matrix: sp.Matrix) -> list[dict[str, object]]:
    records: list[dict[str, object]] = []
    for size in range(1, matrix.rows + 1):
        determinant = sp.radsimp(sp.factor(matrix[:size, :size].det()))
        sign = exact_sign(determinant)
        alternating = ((-1) ** size) * sign == 1
        records.append(
            {
                "size": size,
                "determinant": sp.sstr(determinant),
                "sign": sign,
                "negative_definite_leading_minor": alternating,
            }
        )
    return records


def main() -> None:
    names = ("t11", "t12", "t21", "t22", "t31", "t32", "t41", "t42")
    t = sp.symbols(" ".join(names), real=True)
    t11, t12, t21, t22, t31, t32, t41, t42 = t

    # The four third-coordinate equations are exactly the facet coplanarities
    # in Section 2 of the paper.  In the source's line-broken display the
    # first equation has an outer minus sign before the fraction; writing that
    # parenthesis explicitly gives -( (2+r)t11 + r*t12 )/2.
    t13 = (-(2 + R) * t11 - R * t12) / 2
    t23 = (-R * t21 + (2 + R) * t22) / 2
    t33 = ((2 + R) * t31 + R * t32) / 2
    t43 = (R * t41 - (2 + R) * t42) / 2

    p1 = vec(-1 + t11, -1 + t12, -1 + t13)
    p2 = vec(1 + t21, -1 + t22, 1 + t23)
    p3 = vec(1 + t31, 1 + t32, -1 + t33)
    p4 = vec(-1 + t41, 1 + t42, 1 + t43)

    a1 = vec(2 + R, R, 2 + R)
    a2 = vec(-R, 2 + R, -2 - R)
    a3 = vec(-2 - R, -R, 2 + R)
    a4 = vec(R, -2 - R, -2 - R)

    M = sp.Matrix.vstack((p4 - p1).T, (p2 - p1).T, (p3 - p1).T)
    determinant = sp.factor(M.det())
    adjugate = M.adjugate()

    us = [
        vec(1, 1, 1),
        vec(1, 0, 0),
        vec(0, 0, 1),
        vec(0, 1, 0),
        vec(0, 1, 1),
        vec(1, 0, 1),
    ]
    vs = [
        a1 - a4,
        a3 - a4,
        a2 - a3,
        a1 - a2,
        a1 - a3,
        a2 - a4,
    ]
    target = 2 + R
    hs = [sp.expand((v.T * adjugate * u)[0] - target * determinant) for v, u in zip(vs, us)]
    gradients = [vec(*(sp.diff(h, variable).subs(dict.fromkeys(t, 0)) for variable in t)) for h in hs]
    gradient_matrix = sp.Matrix.vstack(*(g.T for g in gradients))
    lambdas = [1, 1, 1, 1, R, R]
    weighted_gradients = [sp.simplify(lam * g) for lam, g in zip(lambdas, gradients)]
    dependence = sp.simplify(sum(weighted_gradients, vec(0, 0, 0, 0, 0, 0, 0, 0)))

    expected_gradients = [
        4 * vec(-1, 1, -1, -2, 0, 0, -2, 1) + 2 * R * vec(-2, 0, 1, -1, 0, 0, -3, 1),
        4 * vec(-2, 1, 0, 0, 1, 2, 1, 1) + 2 * R * vec(-1, -1, 0, 0, 1, 3, 0, 2),
        4 * vec(0, 0, 2, -1, 1, -1, 1, 2) + 2 * R * vec(0, 0, 3, -1, 2, 0, -1, 1),
        4 * vec(-1, -2, -1, -1, 2, -1, 0, 0) + 2 * R * vec(-1, -3, 0, -2, 1, 1, 0, 0),
        8 * vec(1, 0, -1, 0, -1, 0, 1, 0) + 8 * R * vec(1, 0, 0, 0, -1, 0, 0, 0),
        8 * vec(0, 1, 0, 1, 0, -1, 0, -1) + 8 * R * vec(0, 0, 0, 1, 0, 0, 0, -1),
    ]

    # This is the exact basis printed in the paper for the common gradient
    # kernel V.  It is used to make the restricted-Hessian comparison directly
    # comparable with the displayed 3x3 matrix.
    paper_basis = sp.Matrix.hstack(
        vec(1, 0, 0, 0, R / 2, R / 2, -R / 2, (R - 2) / 2),
        vec(0, 1, 0, -R, (2 - R) / 2, (2 - R) / 2, R / 2, (2 - 3 * R) / 2),
        vec(0, 0, 1, -1, 1 - R, 1, 0, -R),
    )
    computed_nullspace = gradient_matrix.nullspace()
    computed_basis = sp.Matrix.hstack(*computed_nullspace)

    # Hessian of sum(lambda_i h_i) at zero.  This is the Hessian of the
    # quadratic part sum(q_i), with no extra 1/2 factor.
    origin = dict.fromkeys(t, 0)
    weighted_polynomial = sp.expand(sum(lam * h for lam, h in zip(lambdas, hs)))
    weighted_hessian_at_zero = sp.Matrix(
        [[sp.diff(weighted_polynomial, x, y).subs(origin) for y in t] for x in t]
    )
    restricted_hessian = sp.simplify(paper_basis.T * weighted_hessian_at_zero * paper_basis)
    expected_restricted_hessian = sp.Matrix(
        [
            [-19 * R / 2 - 13, -5 * R / 2 - 4, -R - 2],
            [-5 * R / 2 - 4, -39 * R / 2 - 27, -16 * R - 22],
            [-R - 2, -16 * R - 22, -19 * R - 26],
        ]
    )

    # The auxiliary function H from Section 3, with a concrete small c.  The
    # identity below is also checked explicitly to guard against a Hessian
    # coefficient/1/2 convention error.
    c = sp.Rational(1, 100)
    linear_parts = [lam * (g.dot(vec(*t))) for lam, g in zip(lambdas, gradients)]
    auxiliary = sp.expand(
        sum((c - linear) * lam * h for linear, lam, h in zip(linear_parts, lambdas, hs))
    )
    auxiliary_hessian = sp.Matrix(
        [[sp.diff(auxiliary, x, y).subs(origin) for y in t] for x in t]
    )
    linear_gradient_columns = [lam * g for lam, g in zip(lambdas, gradients)]
    formula_hessian = c * weighted_hessian_at_zero - 2 * sum(
        (g * g.T for g in linear_gradient_columns), sp.zeros(8, 8)
    )

    def matrix_is_zero(matrix: sp.Matrix) -> bool:
        """Return True only when every algebraic entry simplifies to zero."""

        return all(sp.simplify(sp.radsimp(entry)) == 0 for entry in matrix)

    gradient_checks = [matrix_is_zero(a - b) for a, b in zip(gradients, expected_gradients)]
    dependence_zero = matrix_is_zero(dependence)
    paper_basis_kernel = matrix_is_zero(gradient_matrix * paper_basis)
    # The direct chart Hessian is exactly 16 times the matrix displayed in the
    # paper.  This positive normalization factor has no effect on definiteness.
    restricted_hessian_scale = sp.Integer(16)
    restricted_matches = matrix_is_zero(
        restricted_hessian - restricted_hessian_scale * expected_restricted_hessian
    )
    auxiliary_formula_matches = matrix_is_zero(auxiliary_hessian - formula_hessian)
    restricted_minors = principal_minors(restricted_hessian)
    auxiliary_minors = principal_minors(auxiliary_hessian)

    assert sp.simplify(determinant.subs(origin) - 16) == 0
    assert all(sp.simplify(h.subs(origin)) == 0 for h in hs)
    assert all(gradient_checks)
    assert gradient_matrix.rank() == 5
    assert dependence_zero
    assert len(computed_nullspace) == 3
    assert paper_basis_kernel
    assert restricted_matches
    assert auxiliary_formula_matches
    assert all(record["negative_definite_leading_minor"] for record in restricted_minors)
    assert all(record["negative_definite_leading_minor"] for record in auxiliary_minors)

    certificate = {
        "source": {
            "title": "A local maximizer for lattice width of 3-dimensional hollow bodies",
            "arxiv": "1907.06199v2",
            "url": "https://arxiv.org/abs/1907.06199",
        },
        "field": "Q(sqrt(2))",
        "chart": {
            "variables": list(names),
            "det_M_at_zero": sp.sstr(determinant.subs(origin)),
            "h_degrees": [sp.Poly(h, *t).total_degree() for h in hs],
            "h_at_zero": [sp.sstr(h.subs(origin)) for h in hs],
        },
        "checks": {
            "gradients_match_paper_equation_4": all(gradient_checks),
            "gradient_rank": int(gradient_matrix.rank()),
            "positive_dependence_coefficients": [sp.sstr(lam) for lam in lambdas],
            "positive_dependence_vector": [sp.sstr(x) for x in dependence],
            "nullspace_dimension": len(computed_nullspace),
            "computed_nullspace_basis": matrix_strings(computed_basis),
            "paper_basis_is_in_kernel": paper_basis_kernel,
            "quadratic_hessian_convention": "Hessian of sum(lambda_i*h_i) at 0; no extra 1/2 factor",
            "restricted_hessian_matches_paper_up_to_positive_scale": restricted_matches,
            "restricted_hessian_scale_relative_to_paper_display": sp.sstr(restricted_hessian_scale),
            "restricted_hessian_direct": matrix_strings(restricted_hessian),
            "restricted_hessian_paper_display": matrix_strings(expected_restricted_hessian),
            "restricted_hessian_leading_minors": restricted_minors,
            "restricted_hessian_negative_definite": all(
                record["negative_definite_leading_minor"] for record in restricted_minors
            ),
            "auxiliary_c": sp.sstr(c),
            "auxiliary_hessian_formula_matches_direct": auxiliary_formula_matches,
            "auxiliary_hessian_leading_minors": auxiliary_minors,
            "auxiliary_hessian_negative_definite": all(
                record["negative_definite_leading_minor"] for record in auxiliary_minors
            ),
        },
        "limitations": [
            "This proves the qualitative existence of a local neighborhood for c=1/100.",
            "It does not reproduce the paper's explicit degree-16 coefficient-majorant radius computation.",
            "It does not prove the geometric hollow-body reduction or any global upper bound.",
        ],
    }
    output_path = Path(__file__).resolve().parents[1] / "certificates" / "local_hessian.json"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(certificate, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(output_path.relative_to(Path(__file__).resolve().parents[1]))
    print(json.dumps({
        "gradient_rank": certificate["checks"]["gradient_rank"],
        "nullspace_dimension": certificate["checks"]["nullspace_dimension"],
        "restricted_negative_definite": certificate["checks"]["restricted_hessian_negative_definite"],
        "auxiliary_c": str(c),
        "auxiliary_negative_definite": certificate["checks"]["auxiliary_hessian_negative_definite"],
    }, indent=2))


if __name__ == "__main__":
    main()
