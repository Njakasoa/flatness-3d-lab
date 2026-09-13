"""An eight-variable signed-adjugate QF_NRA probe for the 2+2 branch.

The contact tetrahedron is

    P = conv(0, (2, 1, 1), e2, e3),

and ``A`` is its row-normalized contact slack matrix.  In the pair branch
``sigma=(01)(23)``, each row is affine in two parameters: the designated
entry ``a_i`` and the first of the two remaining off-diagonal entries
``b_i``.  The final entry is ``1-a_i-b_i``.  The body vertices are eliminated
using the exact signed adjugate formula

    S = adj(A), C_j = sum_i S_ij, T_ij = S_ij/C_j.

This is a bounded polynomial relaxation.  SAT supplies a candidate that still
requires exact hollow-body certification; UNKNOWN is not an exclusion.  The
script performs three solver checks: a pinned positive control at threshold 1,
the same pinned matrix at threshold 17/5 (negative control), and one unpinned
threshold-17/5 relaxation query.  The generated SMT-LIB file contains the
last query only.

Run from ``flatness-3d-lab`` with ``.venv/bin/python``.  The only files this
script writes are ``results/det2_adjugate_smt.json`` and
``results/det2_adjugate_smt.smt2``.
"""

from __future__ import annotations

import itertools
import json
import math
import time
from fractions import Fraction
from pathlib import Path
from typing import Any, Sequence

import z3


HERE = Path(__file__).resolve().parents[1]
JSON_OUT = HERE / "results" / "det2_adjugate_smt.json"
SMT_OUT = HERE / "results" / "det2_adjugate_smt.smt2"

SEED = 20260913
TIMEOUT_MS = 30_000
LAMBDA_LO = -62
LAMBDA_HI = 63
TARGET = z3.RealVal(17) / 5
EPSILON = 1

# Contact vertices in the original ambient coordinates.  The affine
# barycentric coordinates are
#   (1 + X/2 - Y - Z, X/2, Y - X/2, Z - X/2).
CONTACTS: tuple[tuple[int, int, int], ...] = (
    (0, 0, 0),
    (2, 1, 1),
    (0, 1, 0),
    (0, 0, 1),
)

# The pair blocker permutation and the fixed ordering of the two nonassigned
# columns in each row.  The latter makes the eight-variable chart explicit.
SIGMA = (1, 0, 3, 2)
REMAINING = ((2, 3), (2, 3), (0, 1), (0, 1))


def contact_width(direction: tuple[int, int, int]) -> int:
    values = [sum(u * x for u, x in zip(direction, p)) for p in CONTACTS]
    return max(values) - min(values)


def retained_directions() -> list[tuple[tuple[int, int, int], int]]:
    """Return the 37 primitive directions modulo sign with width(P,u) <= 3."""

    answer: list[tuple[tuple[int, int, int], int]] = []
    # The small box is an exact consequence of width(P,u) <= 3: |u_y|,
    # |u_z| <= 3 and |u_x| <= 4.
    for direction in itertools.product(range(-4, 5), range(-3, 4), range(-3, 4)):
        if not any(direction):
            continue
        if math.gcd(*direction) != 1:
            continue
        first_nonzero = next(x for x in direction if x)
        if first_nonzero < 0:
            continue
        width = contact_width(direction)
        if width <= 3:
            answer.append((tuple(int(x) for x in direction), width))
    return answer


DIRECTIONS = retained_directions()


def real(value: int | str) -> z3.ArithRef:
    """Construct a rational real constant without introducing floats."""

    return z3.RealVal(value)


def lambda_xyz(x: z3.ArithRef | int, y: z3.ArithRef | int, z: z3.ArithRef | int) -> list[z3.ArithRef]:
    """Contact barycentric coordinates of an ambient point."""

    half = real(1) / 2
    return [
        real(1) + half * x - y - z,
        half * x,
        y - half * x,
        z - half * x,
    ]


def declare_parameters() -> tuple[list[z3.ArithRef], list[z3.ArithRef]]:
    """Declare exactly eight independent affine row parameters."""

    a = [z3.Real(f"a_{i}") for i in range(4)]
    b = [z3.Real(f"b_{i}") for i in range(4)]
    return a, b


def affine_matrix(a: Sequence[z3.ArithRef], b: Sequence[z3.ArithRef]) -> list[list[z3.ArithRef]]:
    """Build A from the eight row parameters in the pair chart."""

    matrix: list[list[z3.ArithRef]] = []
    for i in range(4):
        row = [z3.RealVal(0) for _ in range(4)]
        designated = SIGMA[i]
        first, second = REMAINING[i]
        row[designated] = a[i]
        row[first] = b[i]
        row[second] = real(1) - a[i] - b[i]
        matrix.append(row)
    return matrix


def determinant3(matrix: Sequence[Sequence[z3.ArithRef]]) -> z3.ArithRef:
    """Return the exact 3 by 3 determinant polynomial."""

    return z3.simplify(
        matrix[0][0] * (matrix[1][1] * matrix[2][2] - matrix[1][2] * matrix[2][1])
        - matrix[0][1] * (matrix[1][0] * matrix[2][2] - matrix[1][2] * matrix[2][0])
        + matrix[0][2] * (matrix[1][0] * matrix[2][1] - matrix[1][1] * matrix[2][0])
    )


def determinant4(matrix: Sequence[Sequence[z3.ArithRef]]) -> z3.ArithRef:
    """Return the exact 4 by 4 determinant polynomial."""

    terms: list[z3.ArithRef] = []
    for column in range(4):
        minor = [
            [matrix[row][col] for col in range(4) if col != column]
            for row in range(1, 4)
        ]
        sign = 1 if column % 2 == 0 else -1
        terms.append(sign * matrix[0][column] * determinant3(minor))
    return z3.simplify(sum(terms, real(0)))


def signed_adjugate(matrix: Sequence[Sequence[z3.ArithRef]], epsilon: int = EPSILON) -> list[list[z3.ArithRef]]:
    """Return S=epsilon*adj(A), with the cofactor transpose orientation."""

    answer: list[list[z3.ArithRef]] = [[real(0) for _ in range(4)] for _ in range(4)]
    for i in range(4):
        for j in range(4):
            # adj(A)[i,j] is the (j,i) cofactor.
            minor = [
                [matrix[row][col] for col in range(4) if col != i]
                for row in range(4)
                if row != j
            ]
            sign = -1 if (i + j) % 2 else 1
            answer[i][j] = z3.simplify(epsilon * sign * determinant3(minor))
    return answer


def reconstruction_expressions(
    S: Sequence[Sequence[z3.ArithRef]],
) -> tuple[list[z3.ArithRef], list[list[z3.ArithRef]], list[list[z3.ArithRef]], list[list[z3.ArithRef]]]:
    """Return C, T, N, and V expressions from the signed adjugate."""

    C = [z3.simplify(sum(S[i][j] for i in range(4))) for j in range(4)]
    T = [[z3.simplify(S[i][j] / C[j]) for j in range(4)] for i in range(4)]
    N = [
        [
            z3.simplify(2 * S[1][j]),
            z3.simplify(S[1][j] + S[2][j]),
            z3.simplify(S[1][j] + S[3][j]),
        ]
        for j in range(4)
    ]
    V = [[z3.simplify(N[j][axis] / C[j]) for axis in range(3)] for j in range(4)]
    return C, T, N, V


def base_constraints(
    a: Sequence[z3.ArithRef],
    b: Sequence[z3.ArithRef],
    A: Sequence[Sequence[z3.ArithRef]],
    det_a: z3.ArithRef,
    S: Sequence[Sequence[z3.ArithRef]],
    C: Sequence[z3.ArithRef],
) -> list[z3.BoolRef]:
    """Build row, determinant, signed-adjugate, and domain constraints."""

    constraints: list[z3.BoolRef] = []

    # Each row is affine in a_i,b_i, with the closed blocker inequality.  The
    # final off-diagonal entry is positive, so the row sum is one.
    for i in range(4):
        constraints.append(a[i] >= real(1) / 2)
        constraints.append(b[i] > 0)
        constraints.append(real(1) - a[i] - b[i] > 0)

    # epsilon=+1 for sigma=(01)(23).  This is the bounded-simplex sign chart.
    constraints.append(det_a > 0)
    constraints.extend(c > 0 for c in C)

    # T_ij=S_ij/C_j and N_j=(2S_1j,S_1j+S_2j,S_1j+S_3j).  Since C_j>0,
    # these are exactly the proved closed barycentric and ambient bounds after
    # clearing denominators.
    for j in range(4):
        for i in range(4):
            constraints.append(S[i][j] >= LAMBDA_LO * C[j])
            constraints.append(S[i][j] <= LAMBDA_HI * C[j])
        for subset_sum in (S[1][j] + S[2][j], S[1][j] + S[3][j]):
            constraints.append(subset_sum >= LAMBDA_LO * C[j])
            constraints.append(subset_sum <= LAMBDA_HI * C[j])

    # Keep A as an argument to make the row-stochastic structure explicit in
    # the construction and to guard against accidental unused parameters.
    for i in range(4):
        if z3.is_true(z3.simplify(A[i][i] == 0)) is False:
            raise AssertionError("affine pair chart lost a zero diagonal")
        constraints.append(sum(A[i][k] for k in range(4)) == 1)

    return constraints


def width_constraints(
    N: Sequence[Sequence[z3.ArithRef]],
    C: Sequence[z3.ArithRef],
    threshold: z3.ArithRef,
) -> list[z3.BoolRef]:
    """Encode width(K,u)>threshold using positive C_j C_k denominators."""

    constraints: list[z3.BoolRef] = []
    for direction, _contact_w in DIRECTIONS:
        ux, uy, uz = direction
        witnesses: list[z3.BoolRef] = []
        for j in range(4):
            for k in range(4):
                if j == k:
                    continue
                difference = (
                    ux * (N[j][0] * C[k] - N[k][0] * C[j])
                    + uy * (N[j][1] * C[k] - N[k][1] * C[j])
                    + uz * (N[j][2] * C[k] - N[k][2] * C[j])
                )
                # Clearing the positive denominator C_j*C_k from
                # u.(V_j-V_k)>threshold gives
                # 5*u.(N_j*C_k-N_k*C_j)>5*threshold*C_j*C_k.
                witnesses.append(5 * difference > 5 * threshold * C[j] * C[k])
        constraints.append(z3.Or(*witnesses))
    return constraints


def finite_hollow_constraints(A: Sequence[Sequence[z3.ArithRef]]) -> list[z3.BoolRef]:
    """Exclude strict interior lattice points in the exploratory 216-point box."""

    constraints: list[z3.BoolRef] = []
    for point in itertools.product(range(-2, 4), repeat=3):
        point_lambda = lambda_xyz(*point)
        # Each atom is linear in the eight affine row parameters because the
        # lattice barycentric coordinates are fixed rationals.
        slacks = [
            sum(A[i][k] * point_lambda[k] for k in range(4)) for i in range(4)
        ]
        constraints.append(z3.Or(*(slack <= 0 for slack in slacks)))
    return constraints


PINNED_PARAMS = {
    **{f"a_{i}": Fraction(2, 3) for i in range(4)},
    **{f"b_{i}": Fraction(1, 6) for i in range(4)},
}


def pin_constraints(a: Sequence[z3.ArithRef], b: Sequence[z3.ArithRef]) -> list[z3.BoolRef]:
    """Pin the exact positive-control matrix A_ij in the eight-variable chart."""

    return [
        variable == rational_to_z3(PINNED_PARAMS[f"{prefix}_{i}"])
        for prefix, variables in (("a", a), ("b", b))
        for i, variable in enumerate(variables)
    ]


def rational_to_z3(value: Fraction) -> z3.ArithRef:
    return z3.RealVal(f"{value.numerator}/{value.denominator}")


def exact_det4(matrix: Sequence[Sequence[Fraction]]) -> Fraction:
    if len(matrix) == 1:
        return matrix[0][0]
    return sum(
        (Fraction(1) if column % 2 == 0 else Fraction(-1))
        * matrix[0][column]
        * exact_det4(
            [
                [matrix[row][col] for col in range(len(matrix)) if col != column]
                for row in range(1, len(matrix))
            ]
        )
        for column in range(len(matrix))
    )


def exact_adjugate(matrix: Sequence[Sequence[Fraction]]) -> list[list[Fraction]]:
    answer = [[Fraction(0) for _ in range(4)] for _ in range(4)]
    for i in range(4):
        for j in range(4):
            minor = [
                [matrix[row][col] for col in range(4) if col != i]
                for row in range(4)
                if row != j
            ]
            answer[i][j] = (Fraction(-1) if (i + j) % 2 else Fraction(1)) * exact_det4(minor)
    return answer


def exact_reconstruction_values() -> dict[str, Any]:
    """Return the pinned control reconstruction using exact Fractions."""

    matrix: list[list[Fraction]] = []
    for i in range(4):
        row = [Fraction(0) for _ in range(4)]
        row[SIGMA[i]] = PINNED_PARAMS[f"a_{i}"]
        first, second = REMAINING[i]
        row[first] = PINNED_PARAMS[f"b_{i}"]
        row[second] = 1 - row[SIGMA[i]] - row[first]
        matrix.append(row)

    determinant = exact_det4(matrix)
    adj = exact_adjugate(matrix)
    columns = [sum(adj[i][j] for i in range(4)) for j in range(4)]
    t = [[adj[i][j] / columns[j] for j in range(4)] for i in range(4)]
    n = [
        [2 * adj[1][j], adj[1][j] + adj[2][j], adj[1][j] + adj[3][j]]
        for j in range(4)
    ]
    vertices = [[n[j][axis] / columns[j] for axis in range(3)] for j in range(4)]
    return {
        "A": matrix,
        "determinant": determinant,
        "S": adj,
        "C": columns,
        "T": t,
        "N": n,
        "V": vertices,
    }


def exact_reconstruction_from_params() -> dict[str, Any]:
    """Validate the pinned control against the old exact positive control."""

    values = exact_reconstruction_values()

    expected_a = [
        [Fraction(0), Fraction(2, 3), Fraction(1, 6), Fraction(1, 6)],
        [Fraction(2, 3), Fraction(0), Fraction(1, 6), Fraction(1, 6)],
        [Fraction(1, 6), Fraction(1, 6), Fraction(0), Fraction(2, 3)],
        [Fraction(1, 6), Fraction(1, 6), Fraction(2, 3), Fraction(0)],
    ]
    expected_t = [
        [Fraction(1, 4), Fraction(7, 4), Fraction(-1, 2), Fraction(-1, 2)],
        [Fraction(7, 4), Fraction(1, 4), Fraction(-1, 2), Fraction(-1, 2)],
        [Fraction(-1, 2), Fraction(-1, 2), Fraction(1, 4), Fraction(7, 4)],
        [Fraction(-1, 2), Fraction(-1, 2), Fraction(7, 4), Fraction(1, 4)],
    ]
    expected_v = [
        [Fraction(7, 2), Fraction(5, 4), Fraction(5, 4)],
        [Fraction(1, 2), Fraction(-1, 4), Fraction(-1, 4)],
        [Fraction(-1), Fraction(-1, 4), Fraction(5, 4)],
        [Fraction(-1), Fraction(5, 4), Fraction(-1, 4)],
    ]
    passed = values["A"] == expected_a and values["T"] == expected_t and values["V"] == expected_v
    if not passed:
        raise AssertionError("signed-adjugate control reconstruction does not match old positive control")

    return {
        "passed": passed,
        "determinant": fraction_text(values["determinant"]),
        "A": fraction_matrix_text(values["A"]),
        "C": [fraction_text(value) for value in values["C"]],
        "S": fraction_matrix_text(values["S"]),
        "T": fraction_matrix_text(values["T"]),
        "N": fraction_matrix_text(values["N"]),
        "V": fraction_matrix_text(values["V"]),
        "expected_control_vertices": fraction_matrix_text(expected_v),
    }


def fraction_text(value: Fraction) -> str:
    return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"


def fraction_matrix_text(matrix: Sequence[Sequence[Fraction]]) -> list[list[str]]:
    return [[fraction_text(value) for value in row] for row in matrix]


def expr_matrix_text(model: z3.ModelRef, matrix: Sequence[Sequence[z3.ArithRef]]) -> list[list[str]]:
    return [
        [z3.simplify(model.eval(value, model_completion=True)).sexpr() for value in row]
        for row in matrix
    ]


def expr_vector_text(model: z3.ModelRef, vector: Sequence[z3.ArithRef]) -> list[str]:
    return [z3.simplify(model.eval(value, model_completion=True)).sexpr() for value in vector]


def model_fraction(model: z3.ModelRef, expression: z3.ArithRef) -> Fraction:
    """Read an exact rational expression from a pinned Z3 model."""

    value = z3.simplify(model.eval(expression, model_completion=True))
    if not z3.is_rational_value(value):
        raise AssertionError(f"expected a rational control value, got {value}")
    return Fraction(value.numerator_as_long(), value.denominator_as_long())


def model_fraction_matrix(
    model: z3.ModelRef,
    matrix: Sequence[Sequence[z3.ArithRef]],
) -> list[list[Fraction]]:
    return [[model_fraction(model, value) for value in row] for row in matrix]


def validate_positive_model(expressions: dict[str, Any], solver: z3.Solver) -> dict[str, Any]:
    """Check the solver's pinned adjugate reconstruction, entry by entry."""

    model = solver.model()
    expected = exact_reconstruction_values()
    actual_a = model_fraction_matrix(model, expressions["A"])
    actual_t = model_fraction_matrix(model, expressions["T"])
    actual_v = model_fraction_matrix(model, expressions["V"])
    passed = actual_a == expected["A"] and actual_t == expected["T"] and actual_v == expected["V"]
    return {
        "passed": passed,
        "checked": ["A", "T", "V"],
        "A": fraction_matrix_text(actual_a),
        "T": fraction_matrix_text(actual_t),
        "V": fraction_matrix_text(actual_v),
    }


def statistics_json(statistics: z3.Statistics) -> dict[str, int | float | str]:
    output: dict[str, int | float | str] = {}
    for key in statistics.keys():
        value = statistics.get_key_value(key)
        output[str(key)] = value if isinstance(value, (int, float)) else str(value)
    return output


def query_result(
    solver: z3.Solver,
    a: Sequence[z3.ArithRef],
    b: Sequence[z3.ArithRef],
    A: Sequence[Sequence[z3.ArithRef]],
    det_a: z3.ArithRef,
    S: Sequence[Sequence[z3.ArithRef]],
    C: Sequence[z3.ArithRef],
    T: Sequence[Sequence[z3.ArithRef]],
    N: Sequence[Sequence[z3.ArithRef]],
    V: Sequence[Sequence[z3.ArithRef]],
    assertion_count: int,
) -> dict[str, Any]:
    started = time.monotonic()
    status = solver.check()
    elapsed = time.monotonic() - started
    result: dict[str, Any] = {
        "status": str(status),
        "elapsed_seconds": elapsed,
        "assertion_count": assertion_count,
        "statistics": statistics_json(solver.statistics()),
    }
    if status == z3.sat:
        model = solver.model()
        result["model"] = {
            "parameters": {
                "a": expr_vector_text(model, a),
                "b": expr_vector_text(model, b),
            },
            "A": expr_matrix_text(model, A),
            "determinant": z3.simplify(model.eval(det_a, model_completion=True)).sexpr(),
            "S": expr_matrix_text(model, S),
            "C": expr_vector_text(model, C),
            "T": expr_matrix_text(model, T),
            "N": expr_matrix_text(model, N),
            "V": expr_matrix_text(model, V),
        }
    elif status == z3.unknown:
        result["reason_unknown"] = solver.reason_unknown()
    return result


def make_solver(
    *,
    width_threshold: z3.ArithRef,
    include_pin: bool,
) -> tuple[z3.Solver, dict[str, Any], int]:
    a, b = declare_parameters()
    A = affine_matrix(a, b)
    det_a = determinant4(A)
    S = signed_adjugate(A)
    C, T, N, V = reconstruction_expressions(S)

    assertions = base_constraints(a, b, A, det_a, S, C)
    assertions.extend(width_constraints(N, C, width_threshold))
    assertions.extend(finite_hollow_constraints(A))
    if include_pin:
        assertions.extend(pin_constraints(a, b))

    solver = z3.Solver()
    solver.set(timeout=TIMEOUT_MS)
    solver.set(random_seed=SEED)
    solver.add(*assertions)
    expressions = {
        "a": a,
        "b": b,
        "A": A,
        "det": det_a,
        "S": S,
        "C": C,
        "T": T,
        "N": N,
        "V": V,
    }
    return solver, expressions, len(assertions)


def write_smt2(solver: z3.Solver) -> None:
    header = "\n".join(
        [
            "; determinant-two 2+2 PAIR branch, eight-variable signed-adjugate relaxation",
            "; Generated by experiments/det2_adjugate_smt.py; this is the unpinned query.",
            "; SAT is only a relaxation candidate; UNKNOWN is not an exclusion.",
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

    reconstruction = exact_reconstruction_from_params()

    # Positive exact control: the old width-3/2 witness at threshold 1.
    positive_solver, positive_expr, positive_assertions = make_solver(
        width_threshold=real(1), include_pin=True
    )
    positive = query_result(
        positive_solver,
        positive_expr["a"],
        positive_expr["b"],
        positive_expr["A"],
        positive_expr["det"],
        positive_expr["S"],
        positive_expr["C"],
        positive_expr["T"],
        positive_expr["N"],
        positive_expr["V"],
        positive_assertions,
    )
    if positive["status"] != "sat":
        raise RuntimeError(f"positive pinned control expected sat, got {positive['status']}")
    positive["reconstruction_validation"] = validate_positive_model(positive_expr, positive_solver)
    if not positive["reconstruction_validation"]["passed"]:
        raise RuntimeError("positive pinned model failed exact A/T/V reconstruction validation")

    # Negative exact control: the same pinned witness cannot clear 17/5.
    negative_solver, negative_expr, negative_assertions = make_solver(
        width_threshold=TARGET, include_pin=True
    )
    negative = query_result(
        negative_solver,
        negative_expr["a"],
        negative_expr["b"],
        negative_expr["A"],
        negative_expr["det"],
        negative_expr["S"],
        negative_expr["C"],
        negative_expr["T"],
        negative_expr["N"],
        negative_expr["V"],
        negative_assertions,
    )
    if negative["status"] != "unsat":
        raise RuntimeError(f"negative pinned control expected unsat, got {negative['status']}")

    # Main and only unpinned query at the requested target.  Its SMT-LIB is
    # emitted before the check result so it remains available on timeout.
    main_solver, main_expr, main_assertions = make_solver(
        width_threshold=TARGET, include_pin=False
    )
    write_smt2(main_solver)
    main_result = query_result(
        main_solver,
        main_expr["a"],
        main_expr["b"],
        main_expr["A"],
        main_expr["det"],
        main_expr["S"],
        main_expr["C"],
        main_expr["T"],
        main_expr["N"],
        main_expr["V"],
        main_assertions,
    )

    result: dict[str, Any] = {
        "status": "bounded_smt_relaxation_probe",
        "branch": "determinant_2_two_plus_two_sigma_(01)(23)",
        "encoding": "eight_variable_affine_rows_signed_adjugate",
        "solver": {
            "name": "z3",
            "version": z3.get_version_string(),
            "logic": "QF_NRA",
            "timeout_ms_per_call": TIMEOUT_MS,
            "random_seed": SEED,
            "solver_calls": 3,
        },
        "contact_vertices_ambient": [list(point) for point in CONTACTS],
        "contact_barycentric_formula": [
            "lambda0=1+X/2-Y-Z",
            "lambda1=X/2",
            "lambda2=Y-X/2",
            "lambda3=Z-X/2",
        ],
        "affine_parameters": {
            "independent": [f"a_{i}" for i in range(4)] + [f"b_{i}" for i in range(4)],
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
            "epsilon": EPSILON,
            "determinant": "det(A)>0",
            "signed_adjugate": "S=epsilon*adj(A)=adj(A)",
            "column_sums": "C_j=sum_i S_ij>0",
            "reconstruction": "T_ij=S_ij/C_j; N_j=(2*S_1j,S_1j+S_2j,S_1j+S_3j); V_j=N_j/C_j",
            "domain": "-62*C_j<=S_ij<=63*C_j and -62*C_j<=S_1j+S_2j,S_1j+S_3j<=63*C_j",
        },
        "directions": [
            {"u": list(direction), "contact_width": width} for direction, width in DIRECTIONS
        ],
        "width_threshold": "17/5",
        "positive_control_width_threshold": "1",
        "finite_hollowness_box": {
            "lo": [-2, -2, -2],
            "hi": [3, 3, 3],
            "point_count": 216,
            "encoding": "one linear disjunction per lattice point",
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
            "description": "unconstrained eight-variable polynomial relaxation with only [-2,3]^3 hollow exclusions",
            **main_result,
        },
        "control_reconstruction": reconstruction,
        "smt2_file": str(SMT_OUT.relative_to(HERE)),
        "scope": {
            "interpretation": "SAT supplies a relaxation candidate only; UNKNOWN is not an exclusion; any SAT candidate needs full exact certification.",
            "finite_box_limit": "The 216-point box is a necessary relaxation and is not a complete hollowness check.",
            "vertex_bound": "The cleared S/C bounds encode the proved rational barycentric and ambient bounds [-62,63].",
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
                "solver_calls": 3,
                "control_reconstruction": reconstruction["passed"],
                "json": str(JSON_OUT),
                "smt2": str(SMT_OUT),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
