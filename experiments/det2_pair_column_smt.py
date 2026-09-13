"""Eight-variable column-stochastic cubic probe for the determinant-two pair branch.

Columns of ``F=diag(r)A`` are normalized to sum one.  The pair inequalities
are linear in the eight column parameters and make the associated simplex
bounded automatically.  With ``S=adj(F)`` and ``delta=det(F)``, every width
comparison uses the quadratic numerator

    N_jk(u) = sum_i (u.p_i) (S_ij-S_ik),

so ``|N_jk|/delta > W`` has degree at most three.  The finite lattice screen
is the reviewed 40-clause reduction of the 216-point box and remains only a
necessary hollowness relaxation.

This script writes only ``results/det2_pair_column_smt.json`` and
``results/det2_pair_column_smt.smt2``.
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
JSON_OUT = HERE / "results" / "det2_pair_column_smt.json"
SMT_OUT = HERE / "results" / "det2_pair_column_smt.smt2"

SEED = base.SEED
TIMEOUT_MS = base.TIMEOUT_MS
LAMBDA_LO = base.LAMBDA_LO
LAMBDA_HI = base.LAMBDA_HI
CONTACTS = base.CONTACTS
SIGMA = base.SIGMA
REMAINING = base.REMAINING
DIRECTIONS = base.DIRECTIONS
TARGET = Fraction(17, 5)
POSITIVE_TARGET = Fraction(1)

PINNED_PARAMS = {
    **{f"c_{i}": Fraction(2, 3) for i in range(4)},
    **{f"d_{i}": Fraction(1, 6) for i in range(4)},
}


def polynomial(expression: z3.ArithRef) -> z3.ArithRef:
    return z3.simplify(expression, som=True)


def column_parameters() -> tuple[list[z3.ArithRef], list[z3.ArithRef]]:
    return (
        [z3.Real(f"c_{i}") for i in range(4)],
        [z3.Real(f"d_{i}") for i in range(4)],
    )


def column_matrix(
    c: Sequence[z3.ArithRef], d: Sequence[z3.ArithRef]
) -> list[list[z3.ArithRef]]:
    """Build F with designated entry c_j and ascending remaining entries."""

    matrix = [[z3.RealVal(0) for _ in range(4)] for _ in range(4)]
    for j in range(4):
        designated = SIGMA[j]
        first, second = [i for i in range(4) if i not in (j, designated)]
        matrix[designated][j] = c[j]
        matrix[first][j] = d[j]
        matrix[second][j] = 1 - c[j] - d[j]
    return matrix


def ambient_reconstruction(
    adjugate: Sequence[Sequence[z3.ArithRef]], delta: z3.ArithRef
) -> tuple[list[list[z3.ArithRef]], list[list[z3.ArithRef]]]:
    """Return T=F^-1 and ambient vertices from its contact coordinates."""

    T = [[polynomial(adjugate[i][j] / delta) for j in range(4)] for i in range(4)]
    N = [
        [
            polynomial(2 * adjugate[1][j]),
            polynomial(adjugate[1][j] + adjugate[2][j]),
            polynomial(adjugate[1][j] + adjugate[3][j]),
        ]
        for j in range(4)
    ]
    V = [[polynomial(N[j][axis] / delta) for axis in range(3)] for j in range(4)]
    return T, V


def width_constraints(
    adjugate: Sequence[Sequence[z3.ArithRef]],
    delta: z3.ArithRef,
    threshold: Fraction,
    directions: Sequence[tuple[tuple[int, int, int], int]] | None = None,
) -> tuple[list[z3.BoolRef], int]:
    """Encode all 37 directions and six unordered vertex pairs."""

    active_directions = DIRECTIONS if directions is None else directions
    constraints: list[z3.BoolRef] = []
    numerator_count = 0
    for direction, _contact_width in active_directions:
        values = [sum(u * p for u, p in zip(direction, point)) for point in CONTACTS]
        witnesses: list[z3.BoolRef] = []
        for j, k in itertools.combinations(range(4), 2):
            numerator = polynomial(
                sum(values[i] * (adjugate[i][j] - adjugate[i][k]) for i in range(4))
            )
            numerator_count += 1
            left = threshold.denominator * numerator
            right = threshold.numerator * delta
            witnesses.extend((left > right, -left > right))
        constraints.append(z3.Or(*witnesses))
    return constraints, numerator_count


def beta_for_threshold(threshold: Fraction) -> Fraction:
    return max(Fraction(0), Fraction(1) - Fraction(13, 6) / threshold)


def acms_constraints(
    matrix: Sequence[Sequence[z3.ArithRef]],
    c: Sequence[z3.ArithRef],
    delta: z3.ArithRef,
    threshold: Fraction,
) -> tuple[list[z3.BoolRef], Fraction]:
    """Add the target-specific volume and difference-gauge cuts."""

    beta = beta_for_threshold(threshold)
    beta3_over_3 = beta**3 / 3
    D = sum(c)
    constraints = [
        delta > base.rational_to_z3(beta3_over_3),
        D / 2 - 1 > base.rational_to_z3(beta),
        matrix[0][2] + matrix[3][2] - matrix[3][0]
        > base.rational_to_z3(beta),
        matrix[0][3] + matrix[2][3] - matrix[2][0]
        > base.rational_to_z3(beta),
    ]
    return constraints, beta


def column_base_constraints(
    matrix: Sequence[Sequence[z3.ArithRef]],
    c: Sequence[z3.ArithRef],
    d: Sequence[z3.ArithRef],
    delta: z3.ArithRef,
) -> list[z3.BoolRef]:
    """Build positivity, pair dominance, determinant, and symmetry cuts."""

    constraints: list[z3.BoolRef] = []
    for j in range(4):
        constraints.extend(
            [c[j] > 0, d[j] > 0, 1 - c[j] - d[j] > 0]
        )
        if not z3.is_true(z3.simplify(sum(matrix[i][j] for i in range(4)) == 1)):
            raise AssertionError("column chart lost a column-normalization identity")

    # F_i,sigma(i) >= the sum of the other two off-diagonal entries.
    for i in range(4):
        designated_column = SIGMA[i]
        constraints.append(
            matrix[i][designated_column]
            >= sum(matrix[i][j] for j in range(4) if j not in (i, designated_column))
        )

    D = sum(c)
    constraints.append(D > 2)
    constraints.append(delta > 0)

    # F_01 is the largest designated entry; F_23 >= F_32.  These are cuts
    # on F entries, not on the old row-normalized A parameters.
    constraints.extend(
        [
            matrix[0][1] >= matrix[1][0],
            matrix[0][1] >= matrix[2][3],
            matrix[0][1] >= matrix[3][2],
            matrix[2][3] >= matrix[3][2],
        ]
    )
    return constraints


def finite_hollow_constraints(
    matrix: Sequence[Sequence[z3.ArithRef]],
) -> list[z3.BoolRef]:
    """Reuse the reviewed 40-clause row-triangle profile on F lambda."""

    return structured.finite_hollow_constraints(matrix)


def pin_constraints(
    c: Sequence[z3.ArithRef], d: Sequence[z3.ArithRef]
) -> list[z3.BoolRef]:
    return [
        variable == base.rational_to_z3(PINNED_PARAMS[f"{prefix}_{i}"])
        for prefix, variables in (("c", c), ("d", d))
        for i, variable in enumerate(variables)
    ]


def make_solver(
    *,
    threshold: Fraction,
    include_pin: bool,
    directions: Sequence[tuple[tuple[int, int, int], int]] | None = None,
) -> tuple[z3.Solver, dict[str, Any], int, int, Fraction]:
    c, d = column_parameters()
    matrix = column_matrix(c, d)
    delta = polynomial(base.determinant4(matrix))
    adjugate = base.signed_adjugate(matrix)
    T, V = ambient_reconstruction(adjugate, delta)

    assertions = column_base_constraints(matrix, c, d, delta)
    acms, beta = acms_constraints(matrix, c, delta, threshold)
    assertions.extend(acms)
    width, numerator_count = width_constraints(
        adjugate, delta, threshold, directions=directions
    )
    assertions.extend(width)
    assertions.extend(finite_hollow_constraints(matrix))
    if include_pin:
        assertions.extend(pin_constraints(c, d))

    solver = z3.Solver()
    solver.set(timeout=TIMEOUT_MS)
    solver.set(random_seed=SEED)
    solver.add(*assertions)
    expressions = {
        "c": c,
        "d": d,
        "F": matrix,
        "delta": delta,
        "S": adjugate,
        "T": T,
        "V": V,
        "beta": beta,
        "threshold": threshold,
    }
    return solver, expressions, len(assertions), numerator_count, beta


def scalar_text(model: z3.ModelRef, expression: z3.ArithRef) -> str:
    return z3.simplify(model.eval(expression, model_completion=True)).sexpr()


def query_result(
    solver: z3.Solver, expressions: dict[str, Any], assertion_count: int
) -> dict[str, Any]:
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
                "c": base.expr_vector_text(model, expressions["c"]),
                "d": base.expr_vector_text(model, expressions["d"]),
            },
            "F": base.expr_matrix_text(model, expressions["F"]),
            "delta": scalar_text(model, expressions["delta"]),
            "S": base.expr_matrix_text(model, expressions["S"]),
            "T": base.expr_matrix_text(model, expressions["T"]),
            "V": base.expr_matrix_text(model, expressions["V"]),
        }
        result["exact_parameters_saved"] = True
    elif status == z3.unknown:
        result["reason_unknown"] = solver.reason_unknown()
    return result


def arithmetic_degree(expression: z3.AstRef) -> int:
    """Return total polynomial degree, rejecting variable denominators."""

    if z3.is_int_value(expression) or z3.is_rational_value(expression):
        return 0
    if z3.is_bool(expression):
        return max((arithmetic_degree(x) for x in expression.children()), default=0)
    if z3.is_const(expression) and z3.is_arith_sort(expression.sort()):
        return 1
    kind = expression.decl().kind()
    children = expression.children()
    if kind in (z3.Z3_OP_ADD, z3.Z3_OP_SUB):
        return max((arithmetic_degree(x) for x in children), default=0)
    if kind == z3.Z3_OP_UMINUS:
        return arithmetic_degree(children[0])
    if kind == z3.Z3_OP_MUL:
        return sum(arithmetic_degree(x) for x in children)
    if kind == z3.Z3_OP_DIV:
        if arithmetic_degree(children[1]) != 0:
            raise AssertionError("column query contains a variable denominator")
        return arithmetic_degree(children[0])
    if kind == z3.Z3_OP_TO_REAL:
        return arithmetic_degree(children[0])
    raise AssertionError(f"unsupported AST operator: {expression.decl()}")


def parse_query_metadata(expected_assertions: int) -> dict[str, Any]:
    text = SMT_OUT.read_text()
    parsed = list(z3.parse_smt2_file(str(SMT_OUT)))
    declared = re.findall(
        r"\(declare-fun\s+([^\s()]+)\s+\(\)\s+Real\)", text
    )
    expected_names = [*(f"c_{i}" for i in range(4)), *(f"d_{i}" for i in range(4))]
    actual_degree = max(
        (arithmetic_degree(assertion) for assertion in parsed), default=0
    )
    passed = (
        len(parsed) == expected_assertions
        and len(declared) == 8
        and set(declared) == set(expected_names)
        and actual_degree == 3
    )
    if not passed:
        raise AssertionError(
            "column SMT parse guard failed: "
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
            "; determinant-two 2+2 PAIR eight-variable column-stochastic cubic relaxation",
            "; Generated by experiments/det2_pair_column_smt.py; unpinned query only.",
            "; Columns of F are normalized; pair dominance supplies boundedness.",
            "; Widths use N_jk(u)/det(F) for all 37 directions and j<k.",
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
        raise RuntimeError("expected 40 retained and 176 tautological hollow clauses")

    reconstruction = base.exact_reconstruction_from_params()

    positive_solver, positive_expr, positive_assertions, positive_count, positive_beta = make_solver(
        threshold=POSITIVE_TARGET, include_pin=True
    )
    positive = query_result(positive_solver, positive_expr, positive_assertions)
    if positive["status"] != "sat":
        raise RuntimeError(f"positive pinned control expected sat, got {positive['status']}")
    positive["reconstruction_validation"] = base.validate_positive_model(
        {"A": positive_expr["F"], "T": positive_expr["T"], "V": positive_expr["V"]},
        positive_solver,
    )
    if not positive["reconstruction_validation"]["passed"]:
        raise RuntimeError("positive pinned column model failed exact F/T/V reconstruction")

    negative_solver, negative_expr, negative_assertions, negative_count, negative_beta = make_solver(
        threshold=TARGET, include_pin=True
    )
    negative = query_result(negative_solver, negative_expr, negative_assertions)
    if negative["status"] != "unsat":
        raise RuntimeError(f"negative pinned control expected unsat, got {negative['status']}")

    # Emit and run exactly one unpinned target query.
    main_solver, main_expr, main_assertions, main_count, main_beta = make_solver(
        threshold=TARGET, include_pin=False
    )
    write_smt2(main_solver)
    parse_metadata = parse_query_metadata(main_assertions)
    main_result = query_result(main_solver, main_expr, main_assertions)

    if not (positive_count == negative_count == main_count == 37 * 6):
        raise AssertionError("expected six width numerators for each of 37 directions")

    result: dict[str, Any] = {
        "status": "eight_variable_column_cubic_bounded_smt_relaxation_probe",
        "branch": "determinant_2_two_plus_two_sigma_(01)(23)",
        "encoding": "8_variable_column_stochastic_pair_model",
        "solver": {
            "name": "z3",
            "version": z3.get_version_string(),
            "logic": "QF_NRA",
            "timeout_ms_per_call": TIMEOUT_MS,
            "random_seed": SEED,
            "solver_calls": 3,
        },
        "variable_count": 8,
        "variables": {
            "column_parameters": [
                *(f"c_{i}" for i in range(4)),
                *(f"d_{i}" for i in range(4)),
            ],
            "total": 8,
        },
        "contact_vertices_ambient": [list(point) for point in CONTACTS],
        "contact_barycentric_formula": [
            "lambda0=1+X/2-Y-Z",
            "lambda1=X/2",
            "lambda2=Y-X/2",
            "lambda3=Z-X/2",
        ],
        "column_parameters": {
            "independent": [f"c_{i}" for i in range(4)]
            + [f"d_{i}" for i in range(4)],
            "column_formula": "F_sigma(j),j=c_j; F_first_remaining(j),j=d_j; F_second_remaining(j),j=1-c_j-d_j",
            "sigma": list(SIGMA),
            "remaining_rows": [list(REMAINING[j]) for j in range(4)],
        },
        "branch_constraints": {
            "F": "zero diagonal, positive off-diagonal, every column sums to 1",
            "pair_dominance": "F_i,sigma(i)>=sum_{j!=i,sigma(i)}F_i,j",
            "invertibility": "D=sum_j c_j>2 and delta=det(F)>0",
            "boundedness": "automatic from column normalization and pair dominance",
            "signed_adjugate": "S=adj(F)",
            "reconstruction": "T_ij=S_ij/delta; V_j=(2*S_1j,S_1j+S_2j,S_1j+S_3j)/delta",
            "domain": "At target 17/5, -62*delta<=S_ij<=63*delta and Y/Z subset bounds are implied by the determinant cut and P inclusion; not separately asserted",
            "canonical_symmetry": [
                "F_01>=F_10,F_23,F_32",
                "F_23>=F_32",
            ],
        },
        "acms_cuts": {
            "positive_control_beta": str(positive_beta),
            "target_beta": str(main_beta),
            "target_beta_exact": f"{main_beta.numerator}/{main_beta.denominator}",
            "cuts": [
                "delta>beta^3/3",
                "D/2-1>beta",
                "F_02+F_32-F_30>beta",
                "F_03+F_23-F_20>beta",
            ],
            "target_delta_lower_bound": str(main_beta**3 / 3),
        },
        "directions": [
            {"u": list(direction), "contact_width": width}
            for direction, width in DIRECTIONS
        ],
        "width_encoding": {
            "direction_count": len(DIRECTIONS),
            "unordered_vertex_pair_count": 6,
            "quadratic_numerator_count": main_count,
            "identity": "u.(V_j-V_k)=N_jk(u)/delta, j<k",
            "target": "17/5",
            "cleared_target": "5*abs(N_jk)>17*delta",
            "maximum_numerator_degree": 2,
        },
        "finite_hollowness_box": {
            "lo": [-2, -2, -2],
            "hi": [3, 3, 3],
            "original_point_count": 216,
            "tautological_clause_count": len(structured.TAUTOLOGICAL_HOLLOW),
            "retained_clause_count": len(structured.RETAINED_HOLLOW),
            "encoding": "same reviewed row-triangle profile evaluated on F lambda",
        },
        "positive_pinned_query": {
            "description": "F=A symmetric 2/3,1/6 control at threshold 1; expected SAT",
            **positive,
        },
        "negative_pinned_query": {
            "description": "same pinned F at target threshold 17/5; expected UNSAT",
            **negative,
        },
        "main_query": {
            "description": "unconstrained eight-variable column-stochastic cubic relaxation at target",
            **main_result,
        },
        "query_parse": parse_metadata,
        "control_reconstruction": reconstruction,
        "smt2_file": str(SMT_OUT.relative_to(HERE)),
        "scope": {
            "interpretation": "SAT supplies a necessary-model candidate only; UNKNOWN is not an exclusion; any SAT candidate needs full exact hollow certification.",
            "finite_box_limit": "The retained 40 clauses come from the [-2,3]^3 necessary relaxation and are not a complete hollowness check.",
            "acms_cut_scope": "The beta cuts are necessary for genuinely hollow target bodies and can remove nonhollow relaxation points.",
            "run_history": "Exactly three solver checks: pinned W=1 SAT, pinned W=17/5 UNSAT, and one unpinned W=17/5 query with a 30 second solver timeout.",
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
                "quadratic_numerators": main_count,
                "variable_count": parse_metadata["declared_real_variable_count"],
                "actual_max_polynomial_degree": parse_metadata["actual_max_polynomial_degree"],
                "control_reconstruction": positive["reconstruction_validation"]["passed"],
                "json": str(JSON_OUT),
                "smt2": str(SMT_OUT),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
