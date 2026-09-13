"""Structured eight-variable QF_NRA probe for the determinant-two pair branch.

This is a refinement of ``det2_adjugate_smt.py``.  The pair matrix structure
gives the exact replacement ``det(A)>0 <=> sum_i a_i>2`` on the row domain,
and gives strict signs for every entry of the signed adjugate.  The query also
uses the centralizer symmetry normalization

    a_0 >= a_1, a_0 >= a_2, a_0 >= a_3, a_2 >= a_3.

The normalization is necessary up to affine lattice equivalence for genuine
hollow bodies.  A fixed partial lattice box is not invariant under all such
maps, so this structured query is not equivalent to the earlier partial-box
relaxation.  SAT remains a candidate requiring exact certification; UNKNOWN
is not an exclusion.

The finite hollow screen is simplified exactly on the closed row-domain
triangles: 176 of the 216 clauses are tautological, and 40 clauses remain
after impossible row atoms are omitted.  The script performs exactly three
solver checks: a pinned positive control at threshold 1, the same pin at
17/5, and one unpinned threshold-17/5 query.  The generated SMT-LIB contains
the unpinned query only.

Run from ``flatness-3d-lab`` with ``.venv/bin/python``.  This script writes
only ``results/det2_pair_structured_smt.json`` and
``results/det2_pair_structured_smt.smt2``.
"""

from __future__ import annotations

import itertools
import json
import time
from fractions import Fraction
from pathlib import Path
from typing import Any, Sequence

import z3

try:
    from experiments import det2_adjugate_smt as base
except ModuleNotFoundError:  # Direct ``python experiments/...py`` invocation.
    import det2_adjugate_smt as base


HERE = Path(__file__).resolve().parents[1]
JSON_OUT = HERE / "results" / "det2_pair_structured_smt.json"
SMT_OUT = HERE / "results" / "det2_pair_structured_smt.smt2"

SEED = base.SEED
TIMEOUT_MS = base.TIMEOUT_MS
LAMBDA_LO = base.LAMBDA_LO
LAMBDA_HI = base.LAMBDA_HI
TARGET = base.TARGET
CONTACTS = base.CONTACTS
SIGMA = base.SIGMA
REMAINING = base.REMAINING
DIRECTIONS = base.DIRECTIONS
PINNED_PARAMS = base.PINNED_PARAMS


def polynomial(expression: z3.ArithRef) -> z3.ArithRef:
    """Expand/simplify a polynomial in sum-of-monomials form."""

    return z3.simplify(expression, som=True)


def structured_base_constraints(
    a: Sequence[z3.ArithRef],
    b: Sequence[z3.ArithRef],
    A: Sequence[Sequence[z3.ArithRef]],
    S: Sequence[Sequence[z3.ArithRef]],
    C: Sequence[z3.ArithRef],
) -> list[z3.BoolRef]:
    """Build the structured row, sign, boundedness, and symmetry constraints."""

    constraints: list[z3.BoolRef] = []

    # The closed blocker inequalities retain all equality cases.  The two
    # other off-diagonal entries remain strict, as required by the contact
    # reduction.
    for i in range(4):
        constraints.append(a[i] >= base.real(1) / 2)
        constraints.append(b[i] > 0)
        constraints.append(base.real(1) - a[i] - b[i] > 0)

    # Pair structure identity: det(A)>0 is exactly sum_i a_i>2 on this row
    # domain.  This linear form replaces the old determinant assertion.
    constraints.append(sum(a) > 2)

    # Positive inverse column sums are still an independent boundedness
    # condition.  Keep them in the signed-adjugate chart as C_j>0.
    constraints.extend(c > 0 for c in C)

    # The structural adjugate signs are redundant under the preceding row and
    # invertibility constraints, but make the reviewed inverse sign pattern
    # explicit and give the nonlinear solver useful branch information.
    for i in range(4):
        for j in range(4):
            if (i < 2) == (j < 2):
                constraints.append(S[i][j] > 0)
            else:
                constraints.append(S[i][j] < 0)

    # Cleared signed-adjugate coordinate bounds.  C_j>0 makes these exactly
    # the barycentric and ambient bounds from the finite reduction.
    for j in range(4):
        for i in range(4):
            constraints.append(S[i][j] >= LAMBDA_LO * C[j])
            constraints.append(S[i][j] <= LAMBDA_HI * C[j])
        for subset_sum in (S[1][j] + S[2][j], S[1][j] + S[3][j]):
            constraints.append(subset_sum >= LAMBDA_LO * C[j])
            constraints.append(subset_sum <= LAMBDA_HI * C[j])

    # These are identities of the affine chart; retaining the assertions
    # documents the row-stochastic construction in the emitted SMT query.
    for i in range(4):
        if not z3.is_true(z3.simplify(A[i][i] == 0)):
            raise AssertionError("pair chart lost a zero diagonal")
        constraints.append(sum(A[i][k] for k in range(4)) == 1)

    # Canonical centralizer representative.  This is necessary up to affine
    # lattice equivalence for genuine hollow bodies; it is not an equivalence
    # for the fixed partial-box relaxation by itself.
    constraints.extend(
        [
            a[0] >= a[1],
            a[0] >= a[2],
            a[0] >= a[3],
            a[2] >= a[3],
        ]
    )
    return constraints


def width_constraints(
    N: Sequence[Sequence[z3.ArithRef]],
    C: Sequence[z3.ArithRef],
    threshold: z3.ArithRef,
) -> list[z3.BoolRef]:
    """Encode all 37 width inequalities after polynomial simplification."""

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
                # Clear the positive C_j*C_k denominator.  som=True expands
                # the degree-five numerator after the exact cancellations.
                numerator = polynomial(5 * difference - 5 * threshold * C[j] * C[k])
                witnesses.append(numerator > 0)
        constraints.append(z3.Or(*witnesses))
    return constraints


def lambda_fraction(point: tuple[int, int, int]) -> list[Fraction]:
    x, y, z = (Fraction(value) for value in point)
    return [
        Fraction(1) + x / 2 - y - z,
        x / 2,
        y - x / 2,
        z - x / 2,
    ]


def row_domain_values(
    point_lambda: Sequence[Fraction],
    row: int,
) -> tuple[Fraction, Fraction, Fraction]:
    """Evaluate a row slack at the three vertices of its closed parameter triangle."""

    designated = SIGMA[row]
    first, second = REMAINING[row]
    # (a,b,c) is respectively (1,0,0), (1/2,1/2,0), or (1/2,0,1/2).
    return (
        point_lambda[designated],
        (point_lambda[designated] + point_lambda[first]) / 2,
        (point_lambda[designated] + point_lambda[second]) / 2,
    )


def hollow_profile() -> tuple[list[tuple[tuple[int, int, int], tuple[int, ...]]], list[tuple[int, int, int]]]:
    """Classify all 216 clauses using exact row-domain triangle extrema."""

    retained: list[tuple[tuple[int, int, int], tuple[int, ...]]] = []
    tautological: list[tuple[int, int, int]] = []
    for point in itertools.product(range(-2, 4), repeat=3):
        point_tuple = tuple(int(value) for value in point)
        point_lambda = lambda_fraction(point_tuple)
        possible_rows: list[int] = []
        tautology = False
        for row in range(4):
            evaluations = row_domain_values(point_lambda, row)
            row_min = min(evaluations)
            row_max = max(evaluations)
            if row_max <= 0:
                tautology = True
                break
            if row_min <= 0:
                possible_rows.append(row)
        if tautology:
            tautological.append(point_tuple)
        else:
            if not possible_rows:
                raise AssertionError(f"empty non-tautological hollow clause at {point_tuple}")
            retained.append((point_tuple, tuple(possible_rows)))
    return retained, tautological


RETAINED_HOLLOW, TAUTOLOGICAL_HOLLOW = hollow_profile()


def finite_hollow_constraints(
    A: Sequence[Sequence[z3.ArithRef]],
) -> list[z3.BoolRef]:
    """Encode the 40 non-tautological hollow clauses with impossible rows omitted."""

    constraints: list[z3.BoolRef] = []
    for point, rows in RETAINED_HOLLOW:
        point_lambda = base.lambda_xyz(*point)
        slacks = [
            sum(A[i][k] * point_lambda[k] for k in range(4))
            for i in rows
        ]
        constraints.append(z3.Or(*(slack <= 0 for slack in slacks)))
    return constraints


def pin_constraints(a: Sequence[z3.ArithRef], b: Sequence[z3.ArithRef]) -> list[z3.BoolRef]:
    return [
        variable == base.rational_to_z3(PINNED_PARAMS[f"{prefix}_{i}"])
        for prefix, variables in (("a", a), ("b", b))
        for i, variable in enumerate(variables)
    ]


def make_solver(
    *,
    width_threshold: z3.ArithRef,
    include_pin: bool,
) -> tuple[z3.Solver, dict[str, Any], int]:
    a, b = base.declare_parameters()
    A = base.affine_matrix(a, b)
    # Keep det in the expression bundle for exact control reporting.  It is
    # intentionally not asserted: sum(a)>2 is the reviewed equivalent.
    det_a = base.determinant4(A)
    S = base.signed_adjugate(A)
    C, T, N, V = base.reconstruction_expressions(S)

    assertions = structured_base_constraints(a, b, A, S, C)
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
            "; determinant-two 2+2 PAIR structured eight-variable relaxation",
            "; Generated by experiments/det2_pair_structured_smt.py; unpinned query only.",
            "; det(A)>0 is replaced by the exact pair-chart condition sum_i a_i>2.",
            "; 176 hollow clauses are tautological on the row-domain triangles; 40 remain.",
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
    if len(RETAINED_HOLLOW) != 40 or len(TAUTOLOGICAL_HOLLOW) != 176:
        raise RuntimeError(
            f"hollow profile expected 40 retained and 176 tautological, got "
            f"{len(RETAINED_HOLLOW)} and {len(TAUTOLOGICAL_HOLLOW)}"
        )

    reconstruction = base.exact_reconstruction_from_params()

    positive_solver, positive_expr, positive_assertions = make_solver(
        width_threshold=base.real(1), include_pin=True
    )
    positive = base.query_result(
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
    positive["reconstruction_validation"] = base.validate_positive_model(positive_expr, positive_solver)
    if not positive["reconstruction_validation"]["passed"]:
        raise RuntimeError("positive pinned model failed exact A/T/V reconstruction validation")

    negative_solver, negative_expr, negative_assertions = make_solver(
        width_threshold=TARGET, include_pin=True
    )
    negative = base.query_result(
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

    main_solver, main_expr, main_assertions = make_solver(
        width_threshold=TARGET, include_pin=False
    )
    write_smt2(main_solver)
    main_result = base.query_result(
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
        "status": "structured_bounded_smt_relaxation_probe",
        "branch": "determinant_2_two_plus_two_sigma_(01)(23)",
        "encoding": "eight_variable_pair_structure_signed_adjugate",
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
            "invertibility": "sum_i a_i>2, exactly equivalent to det(A)>0 on this row domain",
            "epsilon": 1,
            "signed_adjugate": "S=adj(A)",
            "adjugate_signs": "S_ij>0 within groups {0,1},{2,3}; S_ij<0 across groups",
            "column_sums": "C_j=sum_i S_ij>0",
            "reconstruction": "T_ij=S_ij/C_j; N_j=(2*S_1j,S_1j+S_2j,S_1j+S_3j); V_j=N_j/C_j",
            "domain": "-62*C_j<=S_ij<=63*C_j and -62*C_j<=S_1j+S_2j,S_1j+S_3j<=63*C_j",
            "canonical_symmetry": ["a_0>=a_1", "a_0>=a_2", "a_0>=a_3", "a_2>=a_3"],
        },
        "directions": [
            {"u": list(direction), "contact_width": width} for direction, width in DIRECTIONS
        ],
        "width_threshold": "17/5",
        "positive_control_width_threshold": "1",
        "finite_hollowness_box": {
            "lo": [-2, -2, -2],
            "hi": [3, 3, 3],
            "original_point_count": 216,
            "tautological_clause_count": len(TAUTOLOGICAL_HOLLOW),
            "retained_clause_count": len(RETAINED_HOLLOW),
            "retained_row_atom_count": sum(len(rows) for _point, rows in RETAINED_HOLLOW),
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
            "description": "canonical symmetry-restricted unpinned structured relaxation at 17/5",
            **main_result,
        },
        "query_summary": {
            "positive_status": positive["status"],
            "negative_status": negative["status"],
            "main_status": main_result["status"],
            "main_reason_unknown": main_result.get("reason_unknown"),
            "main_assertion_count": main_assertions,
            "smt_real_declaration_count": 8,
            "retained_hollow_clause_count": len(RETAINED_HOLLOW),
        },
        "control_reconstruction": reconstruction,
        "smt2_file": str(SMT_OUT.relative_to(HERE)),
        "scope": {
            "interpretation": "SAT supplies a structured necessary-model candidate only; UNKNOWN is not an exclusion; any SAT candidate needs full exact certification.",
            "symmetry": "Canonical inequalities are necessary up to affine lattice equivalence for genuine hollow bodies; they are not equivalent for the fixed partial-box relaxation.",
            "finite_box_limit": "The retained 40 clauses come from the [-2,3]^3 necessary relaxation and are not a complete hollowness check.",
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
                "tautological_hollow": len(TAUTOLOGICAL_HOLLOW),
                "retained_hollow": len(RETAINED_HOLLOW),
                "retained_row_atoms": sum(len(rows) for _point, rows in RETAINED_HOLLOW),
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
