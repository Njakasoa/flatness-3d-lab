"""Thirteen-variable cubic pair-branch SMT probe.

The eight affine pair-chart parameters are augmented by the four positive
inverse column sums ``r`` and the positive determinant ``delta``.  The lift
uses

    A.T*r = 1,       delta = det(A),

and replaces every signed-adjugate quotient by the complementary-minor
quadratic ``Q`` identity

    u.(V_j - V_k) = Q_jk(u)/(delta*r_j*r_k).

The denominator is positive in this model, so each width comparison is a
polynomial inequality of degree at most three.  The finite lattice screen is
the reviewed 40-clause reduction of the 216-point box.  A SAT result is only
a necessary-model candidate and still requires an exact hollow-body check.

Run from ``flatness-3d-lab`` with ``.venv/bin/python``.  This script writes
only ``results/det2_pair_cubic_smt.json`` and
``results/det2_pair_cubic_smt.smt2``.
"""

from __future__ import annotations

import itertools
import json
import re
import time
from fractions import Fraction
from pathlib import Path
from typing import Any, Sequence

import z3

try:
    from experiments import det2_adjugate_smt as base
    from experiments import det2_pair_structured_smt as structured
except ModuleNotFoundError:  # Direct ``python experiments/...py`` invocation.
    import det2_adjugate_smt as base
    import det2_pair_structured_smt as structured


HERE = Path(__file__).resolve().parents[1]
JSON_OUT = HERE / "results" / "det2_pair_cubic_smt.json"
SMT_OUT = HERE / "results" / "det2_pair_cubic_smt.smt2"

SEED = base.SEED
TIMEOUT_MS = base.TIMEOUT_MS
LAMBDA_LO = base.LAMBDA_LO
LAMBDA_HI = base.LAMBDA_HI
CONTACTS = base.CONTACTS
SIGMA = base.SIGMA
REMAINING = base.REMAINING
DIRECTIONS = base.DIRECTIONS
PINNED_PARAMS = base.PINNED_PARAMS

TARGET = Fraction(17, 5)
POSITIVE_TARGET = Fraction(1, 1)


def polynomial(expression: z3.ArithRef) -> z3.ArithRef:
    """Expand an arithmetic expression into a sum of monomials."""

    return z3.simplify(expression, som=True)


def declare_cubic_variables() -> tuple[
    list[z3.ArithRef], list[z3.ArithRef], list[z3.ArithRef], z3.ArithRef
]:
    """Declare exactly 8+4+1 real variables for the cubic formulation."""

    a, b = base.declare_parameters()
    r = [z3.Real(f"r_{i}") for i in range(4)]
    delta = z3.Real("delta")
    return a, b, r, delta


def two_by_two_minor(
    matrix: Sequence[Sequence[z3.ArithRef]],
    rows: Sequence[int],
    columns: Sequence[int],
) -> z3.ArithRef:
    """Return the ordered 2x2 minor used by the complementary-minor identity."""

    if len(rows) != 2 or len(columns) != 2:
        raise ValueError("the pair cubic model only uses 2x2 complementary minors")
    return polynomial(
        matrix[rows[0]][columns[0]] * matrix[rows[1]][columns[1]]
        - matrix[rows[0]][columns[1]] * matrix[rows[1]][columns[0]]
    )


def complementary_width_polynomial(
    matrix: Sequence[Sequence[z3.ArithRef]],
    direction: tuple[int, int, int],
    j: int,
    k: int,
) -> z3.ArithRef:
    """Build Q_jk(u) from ordered complementary row and column minors."""

    if not j < k:
        raise ValueError("complementary width polynomials use j<k")
    values = [sum(u * p for u, p in zip(direction, point)) for point in CONTACTS]
    rows = [index for index in range(4) if index not in (j, k)]
    answer: z3.ArithRef = base.real(0)
    for i, ell in itertools.combinations(range(4), 2):
        columns = [index for index in range(4) if index not in (i, ell)]
        sign = -1 if (i + ell + j + k) % 2 else 1
        answer = answer + sign * (values[i] - values[ell]) * two_by_two_minor(
            matrix, rows, columns
        )
    return polynomial(answer)


def width_constraints(
    matrix: Sequence[Sequence[z3.ArithRef]],
    r: Sequence[z3.ArithRef],
    delta: z3.ArithRef,
    threshold: Fraction,
) -> tuple[list[z3.BoolRef], int]:
    """Encode all 37 widths using six unordered complementary-minor pairs."""

    if threshold <= 0:
        raise ValueError("the width threshold must be positive")
    constraints: list[z3.BoolRef] = []
    q_count = 0
    for direction, _contact_width in DIRECTIONS:
        witnesses: list[z3.BoolRef] = []
        for j, k in itertools.combinations(range(4), 2):
            q = complementary_width_polynomial(matrix, direction, j, k)
            q_count += 1
            # With delta*r_j*r_k>0, |Q|/(delta*r_j*r_k)>p/q is exactly
            # q*|Q| > p*delta*r_j*r_k.  The requested target 17/5 thus has
            # integral coefficients 5Q and 17 delta*r_j*r_k.
            left = threshold.denominator * q
            right = threshold.numerator * delta * r[j] * r[k]
            witnesses.extend((left > right, -left > right))
        constraints.append(z3.Or(*witnesses))
    return constraints, q_count


def cubic_base_constraints(
    a: Sequence[z3.ArithRef],
    b: Sequence[z3.ArithRef],
    r: Sequence[z3.ArithRef],
    delta: z3.ArithRef,
    matrix: Sequence[Sequence[z3.ArithRef]],
    determinant: z3.ArithRef,
    adjugate: Sequence[Sequence[z3.ArithRef]],
) -> list[z3.BoolRef]:
    """Return the pair chart, cubic lift, signs, bounds, and normalization."""

    constraints: list[z3.BoolRef] = []

    # Pair-chart row domain.  The designated entries are closed at 1/2 and
    # the two other off-diagonal entries are strict, as in the reviewed model.
    for i in range(4):
        constraints.append(a[i] >= base.real(1) / 2)
        constraints.append(b[i] > 0)
        constraints.append(base.real(1) - a[i] - b[i] > 0)

    # On this row domain, pair structure gives det(A)>0 iff sum(a_i)>2.
    # Keep the determinant variable and equality explicit in the cubic lift.
    constraints.append(sum(a) > 2)
    constraints.append(delta > 0)
    constraints.append(delta == determinant)

    # The inverse-column-sum lift.  These are the four quadratic equations
    # A^T r=ones, with a separate strict positivity assertion for each r_j.
    constraints.extend(value > 0 for value in r)
    for column in range(4):
        constraints.append(
            sum(matrix[row][column] * r[row] for row in range(4)) == 1
        )

    # The signed-adjugate sign chart is redundant on the exact pair branch,
    # but retaining it records the reviewed branch and helps the NRA search.
    for i in range(4):
        for j in range(4):
            if (i < 2) == (j < 2):
                constraints.append(adjugate[i][j] > 0)
            else:
                constraints.append(adjugate[i][j] < 0)

    # C_j=delta*r_j.  Use this equality only through the cleared bounds so no
    # quotient or auxiliary C variable enters the 13-variable query.
    for j in range(4):
        scale = delta * r[j]
        for i in range(4):
            constraints.append(adjugate[i][j] >= LAMBDA_LO * scale)
            constraints.append(adjugate[i][j] <= LAMBDA_HI * scale)
        # The first ambient coordinate is 2*lambda_1; the other two are
        # lambda_1+lambda_2 and lambda_1+lambda_3.  Retain all Y/Z bounds.
        for subset_sum in (
            adjugate[1][j] + adjugate[2][j],
            adjugate[1][j] + adjugate[3][j],
        ):
            constraints.append(subset_sum >= LAMBDA_LO * scale)
            constraints.append(subset_sum <= LAMBDA_HI * scale)

    # Construction guards document the fixed row-stochastic pair chart.
    for i in range(4):
        if not z3.is_true(z3.simplify(matrix[i][i] == 0)):
            raise AssertionError("pair chart lost a zero diagonal")
        constraints.append(sum(matrix[i][column] for column in range(4)) == 1)

    # Canonical centralizer representative retained from the structured model.
    constraints.extend(
        [
            a[0] >= a[1],
            a[0] >= a[2],
            a[0] >= a[3],
            a[2] >= a[3],
        ]
    )
    return constraints


def finite_hollow_constraints(
    matrix: Sequence[Sequence[z3.ArithRef]],
) -> list[z3.BoolRef]:
    """Reuse the exact 40-clause reduction of the 216-point box."""

    return structured.finite_hollow_constraints(matrix)


def pin_constraints(
    a: Sequence[z3.ArithRef], b: Sequence[z3.ArithRef]
) -> list[z3.BoolRef]:
    """Pin the reviewed positive-control pair matrix."""

    return [
        variable == base.rational_to_z3(PINNED_PARAMS[f"{prefix}_{i}"])
        for prefix, variables in (("a", a), ("b", b))
        for i, variable in enumerate(variables)
    ]


def make_solver(
    *, threshold: Fraction, include_pin: bool
) -> tuple[z3.Solver, dict[str, Any], int, int]:
    """Construct one cubic solver and return its expressions and Q count."""

    a, b, r, delta = declare_cubic_variables()
    matrix = base.affine_matrix(a, b)
    determinant = polynomial(base.determinant4(matrix))
    adjugate = base.signed_adjugate(matrix)
    C, T, N, V = base.reconstruction_expressions(adjugate)

    assertions = cubic_base_constraints(
        a, b, r, delta, matrix, determinant, adjugate
    )
    width, q_count = width_constraints(matrix, r, delta, threshold)
    assertions.extend(width)
    assertions.extend(finite_hollow_constraints(matrix))
    if include_pin:
        assertions.extend(pin_constraints(a, b))

    solver = z3.Solver()
    solver.set(timeout=TIMEOUT_MS)
    solver.set(random_seed=SEED)
    solver.add(*assertions)
    expressions = {
        "a": a,
        "b": b,
        "r": r,
        "delta": delta,
        "A": matrix,
        "det": determinant,
        "S": adjugate,
        "C": C,
        "T": T,
        "N": N,
        "V": V,
        "threshold": threshold,
    }
    return solver, expressions, len(assertions), q_count


def expr_scalar_text(model: z3.ModelRef, expression: z3.ArithRef) -> str:
    return z3.simplify(model.eval(expression, model_completion=True)).sexpr()


def query_result(
    solver: z3.Solver,
    expressions: dict[str, Any],
    assertion_count: int,
) -> dict[str, Any]:
    """Run one solver check and serialize any exact candidate model."""

    started = time.monotonic()
    status = solver.check()
    elapsed = time.monotonic() - started
    result: dict[str, Any] = {
        "status": str(status),
        "elapsed_seconds": elapsed,
        "assertion_count": assertion_count,
        "statistics": base.statistics_json(solver.statistics()),
    }
    if status == z3.sat:
        model = solver.model()
        result["model"] = {
            "parameters": {
                "a": base.expr_vector_text(model, expressions["a"]),
                "b": base.expr_vector_text(model, expressions["b"]),
                "r": base.expr_vector_text(model, expressions["r"]),
                "delta": expr_scalar_text(model, expressions["delta"]),
            },
            "A": base.expr_matrix_text(model, expressions["A"]),
            "determinant": expr_scalar_text(model, expressions["det"]),
            "S": base.expr_matrix_text(model, expressions["S"]),
            "C": base.expr_vector_text(model, expressions["C"]),
            "T": base.expr_matrix_text(model, expressions["T"]),
            "N": base.expr_matrix_text(model, expressions["N"]),
            "V": base.expr_matrix_text(model, expressions["V"]),
        }
        result["exact_parameters_saved"] = True
    elif status == z3.unknown:
        result["reason_unknown"] = solver.reason_unknown()
    return result


def arithmetic_degree(expression: z3.AstRef) -> int:
    """Return the total polynomial degree of an arithmetic AST."""

    if z3.is_int_value(expression) or z3.is_rational_value(expression):
        return 0
    if z3.is_bool(expression):
        return max((arithmetic_degree(child) for child in expression.children()), default=0)
    if z3.is_const(expression) and z3.is_arith_sort(expression.sort()):
        return 1

    kind = expression.decl().kind()
    children = expression.children()
    if kind in (z3.Z3_OP_ADD, z3.Z3_OP_SUB):
        return max((arithmetic_degree(child) for child in children), default=0)
    if kind == z3.Z3_OP_UMINUS:
        return arithmetic_degree(children[0])
    if kind == z3.Z3_OP_MUL:
        return sum(arithmetic_degree(child) for child in children)
    if kind == z3.Z3_OP_DIV:
        denominator_degree = arithmetic_degree(children[1])
        if denominator_degree != 0:
            raise AssertionError("query contains a variable denominator")
        return arithmetic_degree(children[0])
    if kind == z3.Z3_OP_TO_REAL:
        return arithmetic_degree(children[0])
    if kind == z3.Z3_OP_POWER:
        base_degree = arithmetic_degree(children[0])
        exponent = children[1]
        if not z3.is_int_value(exponent) or exponent.as_long() < 0:
            raise AssertionError("query contains a non-polynomial power")
        return base_degree * exponent.as_long()
    raise AssertionError(f"unsupported AST operator in degree check: {expression.decl()}")


def parse_query_metadata(expected_assertions: int) -> dict[str, Any]:
    """Parse the emitted SMT-LIB and verify its variable count and degree."""

    text = SMT_OUT.read_text()
    parsed = list(z3.parse_smt2_file(str(SMT_OUT)))
    declared = re.findall(
        r"\(declare-fun\s+([^\s()]+)\s+\(\)\s+Real\)", text
    )
    expected_names = [
        *(f"a_{i}" for i in range(4)),
        *(f"b_{i}" for i in range(4)),
        *(f"r_{i}" for i in range(4)),
        "delta",
    ]
    actual_degree = max(
        (arithmetic_degree(assertion) for assertion in parsed), default=0
    )
    passed = (
        len(parsed) == expected_assertions
        and len(declared) == 13
        and set(declared) == set(expected_names)
        and actual_degree == 3
    )
    if not passed:
        raise AssertionError(
            "cubic SMT parse guard failed: "
            f"assertions={len(parsed)}/{expected_assertions}, "
            f"declared={declared}, degree={actual_degree}"
        )
    return {
        "passed": passed,
        "assertion_count": len(parsed),
        "declared_real_variable_count": len(declared),
        "declared_real_variables": declared,
        "actual_max_polynomial_degree": actual_degree,
        "logic": "QF_NRA",
    }


def write_smt2(solver: z3.Solver) -> None:
    header = "\n".join(
        [
            "; determinant-two 2+2 PAIR thirteen-variable cubic relaxation",
            "; Generated by experiments/det2_pair_cubic_smt.py; unpinned query only.",
            "; Variables: eight affine parameters, four positive r_j, and positive delta.",
            "; Widths use Q_jk/(delta*r_j*r_k) for all 37 directions and j<k.",
            "; 40 finite-hollowness clauses remain from the reviewed 216-point box.",
            "; SAT is only a necessary-model candidate; UNKNOWN is not an exclusion.",
            f"(set-option :timeout {TIMEOUT_MS})",
            f"(set-option :random-seed {SEED})",
            "(set-logic QF_NRA)",
        ]
    )
    SMT_OUT.write_text(header + "\n" + solver.sexpr() + "\n(check-sat)\n")


def main() -> None:
    started = time.monotonic()
    if len(DIRECTIONS) != 37:
        raise RuntimeError(f"direction enumeration expected 37, got {len(DIRECTIONS)}")
    if len(structured.RETAINED_HOLLOW) != 40 or len(structured.TAUTOLOGICAL_HOLLOW) != 176:
        raise RuntimeError(
            "hollow profile expected 40 retained and 176 tautological clauses, got "
            f"{len(structured.RETAINED_HOLLOW)} and {len(structured.TAUTOLOGICAL_HOLLOW)}"
        )

    # This is the existing Fraction control used by the adjugate and
    # structured probes.  It checks the old A/T/V reconstruction before any
    # solver result is interpreted.
    reconstruction = base.exact_reconstruction_from_params()

    positive_solver, positive_expr, positive_assertions, positive_q_count = make_solver(
        threshold=POSITIVE_TARGET, include_pin=True
    )
    positive = query_result(positive_solver, positive_expr, positive_assertions)
    if positive["status"] != "sat":
        raise RuntimeError(f"positive pinned control expected sat, got {positive['status']}")
    positive["reconstruction_validation"] = base.validate_positive_model(
        positive_expr, positive_solver
    )
    if not positive["reconstruction_validation"]["passed"]:
        raise RuntimeError("positive pinned model failed exact A/T/V reconstruction validation")

    negative_solver, negative_expr, negative_assertions, negative_q_count = make_solver(
        threshold=TARGET, include_pin=True
    )
    negative = query_result(negative_solver, negative_expr, negative_assertions)
    if negative["status"] != "unsat":
        raise RuntimeError(f"negative pinned control expected unsat, got {negative['status']}")

    # This is the only unpinned target query.  Emit it before checking so the
    # exact query survives a timeout.
    main_solver, main_expr, main_assertions, main_q_count = make_solver(
        threshold=TARGET, include_pin=False
    )
    write_smt2(main_solver)
    parse_metadata = parse_query_metadata(main_assertions)
    main_result = query_result(main_solver, main_expr, main_assertions)

    if not (positive_q_count == negative_q_count == main_q_count == 37 * 6):
        raise AssertionError("expected six Q polynomials for each of 37 directions")

    result: dict[str, Any] = {
        "status": "thirteen_variable_cubic_bounded_smt_relaxation_probe",
        "branch": "determinant_2_two_plus_two_sigma_(01)(23)",
        "encoding": "13_variable_cubic_complementary_minor_pair_model",
        "solver": {
            "name": "z3",
            "version": z3.get_version_string(),
            "logic": "QF_NRA",
            "timeout_ms_per_call": TIMEOUT_MS,
            "random_seed": SEED,
            "solver_calls": 3,
        },
        "variable_count": 13,
        "variables": {
            "affine_pair_parameters": [
                *(f"a_{i}" for i in range(4)),
                *(f"b_{i}" for i in range(4)),
            ],
            "inverse_column_sums": [f"r_{i}" for i in range(4)],
            "determinant": "delta",
            "total": 13,
        },
        "contact_vertices_ambient": [list(point) for point in CONTACTS],
        "contact_barycentric_formula": [
            "lambda0=1+X/2-Y-Z",
            "lambda1=X/2",
            "lambda2=Y-X/2",
            "lambda3=Z-X/2",
        ],
        "affine_parameters": {
            "independent": [f"a_{i}" for i in range(4)]
            + [f"b_{i}" for i in range(4)],
            "row_formula": "A_i,sigma(i)=a_i; A_i,first_remaining(i)=b_i; A_i,second_remaining(i)=1-a_i-b_i",
            "sigma": list(SIGMA),
            "remaining_columns": [list(pair) for pair in REMAINING],
        },
        "branch_constraints": {
            "A": "affine 4x4, A_ii=0, each row sums to 1, off-diagonals positive",
            "designated_closed_inequalities": [
                "a_0=A_01>=1/2",
                "a_1=A_10>=1/2",
                "a_2=A_23>=1/2",
                "a_3=A_32>=1/2",
            ],
            "invertibility": "sum_i a_i>2 and delta=det(A)>0",
            "lift": "A^T*r=ones and r_j>0",
            "signed_adjugate": "S=adj(A), with pair-chart within-group positive and cross-group negative signs",
            "denominator_identity": "C_j=delta*r_j; V_j=N_j/C_j",
            "reconstruction": "T_ij=S_ij/C_j; N_j=(2*S_1j,S_1j+S_2j,S_1j+S_3j); V_j=N_j/C_j",
            "domain": "-62*delta*r_j<=S_ij<=63*delta*r_j and the same bounds for Y/Z subset sums",
            "canonical_symmetry": [
                "a_0>=a_1",
                "a_0>=a_2",
                "a_0>=a_3",
                "a_2>=a_3",
            ],
        },
        "directions": [
            {"u": list(direction), "contact_width": width}
            for direction, width in DIRECTIONS
        ],
        "width_encoding": {
            "direction_count": len(DIRECTIONS),
            "unordered_vertex_pair_count": 6,
            "Q_polynomial_count": main_q_count,
            "identity": "u.(V_j-V_k)=Q_jk(u)/(delta*r_j*r_k), j<k",
            "target": "17/5",
            "cleared_target": "5*abs(Q_jk)>17*delta*r_j*r_k",
            "maximum_Q_degree": 2,
        },
        "finite_hollowness_box": {
            "lo": [-2, -2, -2],
            "hi": [3, 3, 3],
            "original_point_count": 216,
            "tautological_clause_count": len(structured.TAUTOLOGICAL_HOLLOW),
            "retained_clause_count": len(structured.RETAINED_HOLLOW),
            "encoding": "exact closed-row-triangle extrema; impossible row atoms omitted",
        },
        "positive_pinned_query": {
            "description": "same dominant 2/3, other 1/6 matrix pinned at control threshold 1; expected SAT",
            **positive,
        },
        "negative_pinned_query": {
            "description": "same pinned matrix at target threshold 17/5; expected UNSAT",
            **negative,
        },
        "main_query": {
            "description": "unconstrained thirteen-variable cubic relaxation at target with only [-2,3]^3 hollow exclusions",
            **main_result,
        },
        "query_parse": parse_metadata,
        "control_reconstruction": reconstruction,
        "smt2_file": str(SMT_OUT.relative_to(HERE)),
        "scope": {
            "interpretation": "SAT supplies a necessary-model candidate only; UNKNOWN is not an exclusion; any SAT candidate needs full exact hollow certification.",
            "finite_box_limit": "The retained 40 clauses come from the [-2,3]^3 necessary relaxation and are not a complete hollowness check.",
            "vertex_bound": "The cleared adjugate bounds encode the proved rational barycentric and ambient bounds [-62,63], including Y/Z subset sums.",
            "run_history": "Exactly three solver checks were run: pinned W=1 SAT, pinned W=17/5 UNSAT, and one unpinned W=17/5 query with a 30 second solver timeout.",
        },
        "elapsed_seconds": time.monotonic() - started,
    }
    JSON_OUT.write_text(json.dumps(result, indent=2) + "\n")
    print(
        json.dumps(
            {
                "status": result["status"],
                "positive": positive["status"],
                "negative": negative["status"],
                "main": main_result["status"],
                "main_reason_unknown": main_result.get("reason_unknown"),
                "directions": len(DIRECTIONS),
                "q_polynomials": main_q_count,
                "variable_count": parse_metadata["declared_real_variable_count"],
                "actual_max_polynomial_degree": parse_metadata["actual_max_polynomial_degree"],
                "control_reconstruction": reconstruction["passed"],
                "json": str(JSON_OUT),
                "smt2": str(SMT_OUT),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
