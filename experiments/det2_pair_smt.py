"""A bounded QF_NRA probe for the determinant-two 2+2 pair branch.

This is an exact polynomial relaxation, rather than a hollow-body proof.  The
contact tetrahedron is

    P = conv(0, (2, 1, 1), e2, e3),

and ``A`` is the row-normalized contact slack matrix.  ``T`` has the contact
barycentric coordinates of the four body vertices as its columns.  The
incidence equations ``A*T = positive diagonal`` describe a bounded tetrahedron
without using a roof chart, so the designated coefficients may equal 1/2.

The script intentionally performs exactly two solver checks: a pinned positive
control query using the known width-3/2 witness at threshold 1, followed by the
unconstrained finite relaxation query at threshold 17/5.  Each check has a 30
second Z3 timeout.  The generated SMT-LIB file contains the unconstrained query
for independent replay.

Run from ``flatness-3d-lab`` with ``.venv/bin/python``.  The script writes only
``results/det2_pair_smt.json`` and ``results/det2_pair_smt.smt2``.
"""

from __future__ import annotations

import itertools
import json
import math
import time
from pathlib import Path
from typing import Any

import z3


HERE = Path(__file__).resolve().parents[1]
JSON_OUT = HERE / "results" / "det2_pair_smt.json"
SMT_OUT = HERE / "results" / "det2_pair_smt.smt2"

SEED = 20260913
TIMEOUT_MS = 30_000
LAMBDA_LO = -62
LAMBDA_HI = 63
TARGET = z3.RealVal(17) / 5

# Contact vertices in the original ambient coordinates.  The affine
# barycentric coordinates are
#   (1 + X/2 - Y - Z, X/2, Y - X/2, Z - X/2).
CONTACTS: tuple[tuple[int, int, int], ...] = (
    (0, 0, 0),
    (2, 1, 1),
    (0, 1, 0),
    (0, 0, 1),
)


def contact_width(direction: tuple[int, int, int]) -> int:
    values = [sum(u * x for u, x in zip(direction, p)) for p in CONTACTS]
    return max(values) - min(values)


def retained_directions() -> list[tuple[tuple[int, int, int], int]]:
    """Return the 37 primitive directions modulo sign with width(P,u) <= 3."""

    answer: list[tuple[tuple[int, int, int], int]] = []
    # The small box is an exact consequence of width(P,u) <= 3, rather than a
    # heuristic search radius: |u_y|,|u_z| <= 3 and |u_x| <= 4.
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


def declare_variables() -> tuple[list[list[z3.ArithRef]], list[list[z3.ArithRef]], list[list[z3.ArithRef]]]:
    A = [[z3.Real(f"A_{i}_{k}") for k in range(4)] for i in range(4)]
    T = [[z3.Real(f"T_{i}_{j}") for j in range(4)] for i in range(4)]
    V = [[z3.Real(f"V_{j}_{axis}") for axis in range(3)] for j in range(4)]
    return A, T, V


def base_constraints(
    A: list[list[z3.ArithRef]],
    T: list[list[z3.ArithRef]],
    V: list[list[z3.ArithRef]],
) -> list[z3.BoolRef]:
    """Build the exact simplex/incidence and coordinate-bound constraints."""

    constraints: list[z3.BoolRef] = []

    # A is a row-stochastic contact slack matrix.  The diagonal is the
    # assigned contact facet; all other entries are strictly positive.
    for i in range(4):
        constraints.append(A[i][i] == 0)
        constraints.append(sum(A[i][k] for k in range(4)) == 1)
        for k in range(4):
            if k != i:
                constraints.append(A[i][k] > 0)

    # The 2+2 derangement branch, including its equality boundary.
    for i, k in ((0, 1), (1, 0), (2, 3), (3, 2)):
        constraints.append(A[i][k] >= real(1) / 2)

    # T's columns are barycentric coordinates of the body vertices, with the
    # conservative rational bound proved for any potential w > 17/5 witness.
    for j in range(4):
        constraints.append(sum(T[i][j] for i in range(4)) == 1)
        for i in range(4):
            constraints.append(T[i][j] >= LAMBDA_LO)
            constraints.append(T[i][j] <= LAMBDA_HI)

        # The affine inverse is X=2*T_1j, Y=T_1j+T_2j,
        # Z=T_1j+T_3j.  Keep the latter two coordinates inside the same
        # proved conservative ambient range as the barycentric entries; this
        # is needed when the finite lattice box is used as the stated
        # necessary domain for a genuine high-width witness.
        constraints.append(T[1][j] + T[2][j] >= LAMBDA_LO)
        constraints.append(T[1][j] + T[2][j] <= LAMBDA_HI)
        constraints.append(T[1][j] + T[3][j] >= LAMBDA_LO)
        constraints.append(T[1][j] + T[3][j] <= LAMBDA_HI)

        point_lambda = lambda_xyz(V[j][0], V[j][1], V[j][2])
        for i in range(4):
            constraints.append(T[i][j] == point_lambda[i])

    # Each body vertex is on all but its opposite facet, and is strictly on
    # the positive side of that opposite facet.  A*T therefore is positive
    # diagonal, which forces both A and T to be invertible.
    for i in range(4):
        for j in range(4):
            product_entry = sum(A[i][k] * T[k][j] for k in range(4))
            if i == j:
                constraints.append(product_entry > 0)
            else:
                constraints.append(product_entry == 0)

    return constraints


def width_constraints(V: list[list[z3.ArithRef]], threshold: z3.ArithRef) -> list[z3.BoolRef]:
    """Encode width(K,u)>threshold for every retained primitive direction."""

    constraints: list[z3.BoolRef] = []
    for direction, _contact_w in DIRECTIONS:
        ux, uy, uz = direction
        witnesses: list[z3.BoolRef] = []
        for j in range(4):
            for k in range(4):
                if j == k:
                    continue
                difference = (
                    ux * (V[j][0] - V[k][0])
                    + uy * (V[j][1] - V[k][1])
                    + uz * (V[j][2] - V[k][2])
                )
                witnesses.append(difference > threshold)
        constraints.append(z3.Or(*witnesses))
    return constraints


def finite_hollow_constraints(A: list[list[z3.ArithRef]]) -> list[z3.BoolRef]:
    """Exclude strict interior lattice points in the exploratory box only."""

    constraints: list[z3.BoolRef] = []
    for point in itertools.product(range(-2, 4), repeat=3):
        point_lambda = lambda_xyz(*point)
        # A_i dot lambda(z) is the normalized slack of z in facet i.  At
        # least one nonpositive slack is necessary for this point not to be
        # strictly interior.  This finite box is deliberately a relaxation.
        slacks = [
            sum(A[i][k] * point_lambda[k] for k in range(4)) for i in range(4)
        ]
        constraints.append(z3.Or(*(slack <= 0 for slack in slacks)))
    return constraints


def fixed_control_constraints(
    A: list[list[z3.ArithRef]], T: list[list[z3.ArithRef]], V: list[list[z3.ArithRef]]
) -> list[z3.BoolRef]:
    """Pin the exact width-3/2 witness for an encoding sanity check."""

    # The roof-chart witness transformed to (X,Y,Z), ordered so A*T is the
    # identity.  Its width is 3/2, so it satisfies the lower control threshold
    # of 1 in every retained direction.
    witness_v = (
        (real("7/2"), real("5/4"), real("5/4")),
        (real("1/2"), real("-1/4"), real("-1/4")),
        (real("-1"), real("-1/4"), real("5/4")),
        (real("-1"), real("5/4"), real("-1/4")),
    )
    witness_a = (
        (real(0), real("2/3"), real("1/6"), real("1/6")),
        (real("2/3"), real(0), real("1/6"), real("1/6")),
        (real("1/6"), real("1/6"), real(0), real("2/3")),
        (real("1/6"), real("1/6"), real("2/3"), real(0)),
    )
    witness_t = (
        (real("1/4"), real("7/4"), real("-1/2"), real("-1/2")),
        (real("7/4"), real("1/4"), real("-1/2"), real("-1/2")),
        (real("-1/2"), real("-1/2"), real("1/4"), real("7/4")),
        (real("-1/2"), real("-1/2"), real("7/4"), real("1/4")),
    )
    constraints: list[z3.BoolRef] = []
    for i in range(4):
        for k in range(4):
            constraints.append(A[i][k] == witness_a[i][k])
            constraints.append(T[i][k] == witness_t[i][k])
    for j in range(4):
        for axis in range(3):
            constraints.append(V[j][axis] == witness_v[j][axis])
    return constraints


def make_solver(
    *,
    include_control_pin: bool,
    width_threshold: z3.ArithRef,
) -> tuple[z3.Solver, dict[str, list[list[z3.ArithRef]]], int]:
    A, T, V = declare_variables()
    solver = z3.Solver()
    solver.set(timeout=TIMEOUT_MS)
    solver.set(random_seed=SEED)
    assertions = base_constraints(A, T, V)
    assertions.extend(width_constraints(V, width_threshold))
    assertions.extend(finite_hollow_constraints(A))
    if include_control_pin:
        assertions.extend(fixed_control_constraints(A, T, V))
    solver.add(*assertions)
    return solver, {"A": A, "T": T, "V": V}, len(assertions)


def statistics_json(statistics: z3.Statistics) -> dict[str, int | float | str]:
    output: dict[str, int | float | str] = {}
    for key in statistics.keys():
        value = statistics.get_key_value(key)
        # Statistics values are normally int/float, but str() keeps this
        # robust across Z3 builds that expose a textual counter.
        output[str(key)] = value if isinstance(value, (int, float)) else str(value)
    return output


def model_json(model: z3.ModelRef, variables: dict[str, list[list[z3.ArithRef]]]) -> dict[str, list[list[str]]]:
    output: dict[str, list[list[str]]] = {}
    for name, matrix in variables.items():
        output[name] = [
            [z3.simplify(model.eval(variable, model_completion=True)).sexpr() for variable in row]
            for row in matrix
        ]
    return output


def solver_result(
    solver: z3.Solver,
    variables: dict[str, list[list[z3.ArithRef]]],
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
        result["model"] = model_json(solver.model(), variables)
    elif status == z3.unknown:
        result["reason_unknown"] = solver.reason_unknown()
    return result


def write_smt2(solver: z3.Solver) -> None:
    """Write the exact unconstrained query in standalone SMT-LIB form."""

    header = "\n".join(
        [
            "; determinant-two 2+2 PAIR branch finite QF_NRA relaxation",
            "; Generated by experiments/det2_pair_smt.py; no control pins included.",
            "; SAT is only a relaxation candidate; UNKNOWN is not an exclusion.",
            f"(set-option :timeout {TIMEOUT_MS})",
            f"(set-option :random-seed {SEED})",
            "(set-logic QF_NRA)",
        ]
    )
    # sexpr() has exact rationals and polynomial assertions, with no implicit
    # floating-point approximation.  Add a single replay check command.
    SMT_OUT.write_text(header + "\n" + solver.sexpr() + "\n(check-sat)\n")


def main() -> None:
    started = time.monotonic()
    if len(DIRECTIONS) != 37:
        raise RuntimeError(f"direction enumeration expected 37, got {len(DIRECTIONS)}")

    # First call: fixed exact low-width witness at a deliberately lower
    # threshold.  Its width is 3/2, so this positive control should be SAT and
    # exercises the same incidence, finite-hollowness, and direction encoding.
    control_solver, control_variables, control_assertions = make_solver(
        include_control_pin=True, width_threshold=real(1)
    )
    control = solver_result(control_solver, control_variables, control_assertions)

    # Second (and final) call: the requested finite necessary relaxation.
    main_solver, main_variables, main_assertions = make_solver(
        include_control_pin=False, width_threshold=TARGET
    )
    main_result = solver_result(main_solver, main_variables, main_assertions)
    write_smt2(main_solver)

    result: dict[str, Any] = {
        "status": "bounded_smt_relaxation_probe",
        "branch": "determinant_2_two_plus_two_sigma_(01)(23)",
        "solver": {
            "name": "z3",
            "version": z3.get_version_string(),
            "logic": "QF_NRA",
            "timeout_ms_per_call": TIMEOUT_MS,
            "random_seed": SEED,
            "solver_calls": 2,
        },
        "contact_vertices_ambient": [list(point) for point in CONTACTS],
        "contact_barycentric_formula": [
            "lambda0=1+X/2-Y-Z",
            "lambda1=X/2",
            "lambda2=Y-X/2",
            "lambda3=Z-X/2",
        ],
        "branch_constraints": {
            "A": "real 4x4, A_ii=0, A_ik>0 for i!=k, each row sums to 1",
            "designated_closed_inequalities": ["A_01>=1/2", "A_10>=1/2", "A_23>=1/2", "A_32>=1/2"],
            "T": "column sums 1; T_ij=lambda_i(V_j); -62<=T_ij<=63 and -62<=T_1j+T_2j,T_1j+T_3j<=63",
            "incidence": "(A*T)_ij=0 for i!=j and (A*T)_ii>0",
        },
        "directions": [
            {"u": list(direction), "contact_width": width} for direction, width in DIRECTIONS
        ],
        "width_threshold": "17/5",
        "control_width_threshold": "1",
        "finite_hollowness_box": {"lo": [-2, -2, -2], "hi": [3, 3, 3], "point_count": 216},
        "control_query": {
            "description": "known exact width-3/2 witness pinned with control threshold 1; expected SAT",
            **control,
        },
        "main_query": {
            "description": "unconstrained polynomial relaxation with only [-2,3]^3 hollow exclusions",
            **main_result,
        },
        "smt2_file": str(SMT_OUT.relative_to(HERE)),
        "scope": {
            "interpretation": "SAT supplies a relaxation candidate only; UNSAT requires independent encoding/replay review; UNKNOWN is not an exclusion.",
            "finite_box_limit": "The 216-point box is a necessary relaxation and is not a complete hollowness check.",
            "vertex_bound": "The closed T bounds [-62,63] are the proved rational bound for a hypothetical hollow width>17/5 witness.",
        },
        "elapsed_seconds": time.monotonic() - started,
    }
    JSON_OUT.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({
        "status": result["status"],
        "control": control["status"],
        "main": main_result["status"],
        "main_reason_unknown": main_result.get("reason_unknown"),
        "directions": len(DIRECTIONS),
        "solver_calls": 2,
        "json": str(JSON_OUT),
        "smt2": str(SMT_OUT),
    }, indent=2))


if __name__ == "__main__":
    main()
