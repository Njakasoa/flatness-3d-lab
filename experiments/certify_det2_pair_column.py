"""Bounded exact rationalization of the best column-chart hollow sample.

The source point is fixed: run 4 of ``det2_column_search.json``.  A small
QF_LRA snap is used only to choose rational parameters near that recorded
point.  The snap has eight variables, rounded 1e-6 centers, radius 1e-4,
positive off-diagonal entries, pair row dominance, ``sum(c)>2``, and an
explicit finite integer-box OR hollowness screen.  Exact certification below
uses only the rational parameters and ``src.geometry``; it does not depend on
Z3.

After the first bounded snap succeeds, its exact rational model is archived in
``ARCHIVED_PARAMETERS``.  Future runs therefore replay the same exact body by
default.  ``--resnap`` reruns the same ten-second QF_LRA choice and records the
comparison, without changing the archived exact certificate.
"""

from __future__ import annotations

import argparse
import itertools
import json
import sys
import time
from fractions import Fraction
from pathlib import Path
from typing import Any, Sequence

# Make direct ``python experiments/...py`` invocation resolve the local exact
# geometry package as well as ``python -m experiments...`` does.
HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE))

from src.exact import Q, determinant, inverse
from src.geometry import Polytope, certify_hollow, certify_width


SOURCE_JSON = HERE / "results" / "det2_column_search.json"
CERTIFICATE_JSON = HERE / "certificates" / "det2_pair_column.json"

SEED = 20260913
SOLVER_TIMEOUT_MS = 10_000
SIGMA = (1, 0, 3, 2)
REMAINING = ((2, 3), (2, 3), (0, 1), (0, 1))
OFFDIAGONAL_FLOOR = Fraction(1, 100_000_000)
SNAP_RADIUS = Fraction(1, 10_000)
WIDTH_THRESHOLD = Fraction(19, 6)

# Filled after the first bounded solver run.  Keeping this exact pin makes the
# exact certificate replay independent of Z3 model-choice details.
ARCHIVED_PARAMETERS: tuple[str, ...] = (
    "169893/200000",
    "1/10000",
    "588557/1000000",
    "268049/1000000",
    "294329/1000000",
    "58855699/300000000",
    "49999999/50000000",
    "1/100000000",
)


def load_source() -> dict[str, Any]:
    data = json.loads(SOURCE_JSON.read_text())
    row = data.get("best_numeric_hollow")
    if not row or row.get("index") != 4:
        raise RuntimeError("source best_numeric_hollow run 4 is missing or changed")
    if row.get("trust_status") != "numeric_hollow":
        raise RuntimeError("source run 4 is not marked numeric_hollow")
    return row


def rounded_centers(source: dict[str, Any]) -> tuple[Fraction, ...]:
    """Read the recorded floats and round each to an exact 1e-6 decimal."""

    centers: list[Fraction] = []
    for value in source["parameters"]:
        centers.append(Fraction(f"{float(value):.6f}"))
    return tuple(centers)


def matrix_from_parameters(parameters: Sequence[Fraction]) -> list[list[Fraction]]:
    matrix = [[Fraction(0) for _ in range(4)] for _ in range(4)]
    for column in range(4):
        c = Fraction(parameters[2 * column])
        d = Fraction(parameters[2 * column + 1])
        matrix[SIGMA[column]][column] = c
        first, second = REMAINING[column]
        matrix[first][column] = d
        matrix[second][column] = 1 - c - d
    return matrix


def lambda_xyz(point: tuple[int, int, int]) -> tuple[Fraction, ...]:
    x, y, z = map(Fraction, point)
    return (1 + x / 2 - y - z, x / 2, y - x / 2, z - x / 2)


def exact_vertices(matrix: Sequence[Sequence[Fraction]]) -> list[tuple[Q, Q, Q]]:
    qmatrix = [[Q(value) for value in row] for row in matrix]
    inverse_matrix = inverse(qmatrix)
    return [
        (
            2 * inverse_matrix[1][column],
            inverse_matrix[1][column] + inverse_matrix[2][column],
            inverse_matrix[1][column] + inverse_matrix[3][column],
        )
        for column in range(4)
    ]


def parameter_strings(parameters: Sequence[Fraction]) -> list[str]:
    return [str(Fraction(value)) for value in parameters]


def qjson(value: Q) -> dict[str, Any]:
    return value.json()


def fmatrix_json(matrix: Sequence[Sequence[Fraction]]) -> list[list[str]]:
    return [[str(Fraction(value)) for value in row] for row in matrix]


def exact_body(parameters: Sequence[Fraction]) -> dict[str, Any]:
    matrix = matrix_from_parameters(parameters)
    vertices = exact_vertices(matrix)
    body = Polytope(vertices)
    hollow = certify_hollow(body)
    width = certify_width(body)
    exact_width = Q.from_json(width["width"])

    qmatrix = [[Q(value) for value in row] for row in matrix]
    dominance = [
        qmatrix[row][SIGMA[row]]
        - sum((qmatrix[row][column] for column in range(4) if column not in (row, SIGMA[row])), Q())
        for row in range(4)
    ]
    determinant_value = determinant(qmatrix)
    contacts = [(0, 0, 0), (2, 1, 1), (0, 1, 0), (0, 0, 1)]
    contact_slacks = [[qmatrix[row][column] for row in range(4)] for column in range(4)]
    contact_relint = [
        contact_slacks[column][column] == 0
        and all(contact_slacks[column][row] > 0 for row in range(4) if row != column)
        for column in range(4)
    ]

    if not hollow["hollow"]:
        raise RuntimeError(f"exact snap is nonhollow: {hollow['interior_points']}")
    if not exact_width > Q(WIDTH_THRESHOLD):
        raise RuntimeError(f"exact width {exact_width} does not exceed {WIDTH_THRESHOLD}")
    if not all(qmatrix[i][j] > 0 for i in range(4) for j in range(4) if i != j):
        raise RuntimeError("exact snap has a nonpositive off-diagonal entry")
    if not all(d >= 0 for d in dominance):
        raise RuntimeError(f"pair dominance failed exactly: {dominance}")
    if not sum(qmatrix[index][SIGMA[index]] for index in range(4)) > 2:
        raise RuntimeError("sum of designated entries is not strictly greater than 2")
    if not all(contact_relint):
        raise RuntimeError("a designated contact is not in the relative interior of its facet")

    return {
        "parameters": parameter_strings(parameters),
        "F": fmatrix_json(matrix),
        "vertices": body.json(),
        "determinant": qjson(determinant_value),
        "volume": qjson(body.volume()),
        "hollow": hollow,
        "width": width,
        "width_threshold": str(WIDTH_THRESHOLD),
        "row_pair_dominance": [qjson(value) for value in dominance],
        "row_pair_dominance_equalities": [index for index, value in enumerate(dominance) if not value],
        "contact_points": [list(point) for point in contacts],
        "designated_contact_relative_interior": contact_relint,
        "boundary_count": len(hollow["boundary_points"]),
        "boundary_points": [list(point) for point in hollow["boundary_points"]],
    }


def expanded_integer_box(source: dict[str, Any]) -> tuple[list[int], list[int]]:
    box = source["integer_box_scan"]["integer_box"]
    lo, hi = box
    return [int(value) - 1 for value in lo], [int(value) + 1 for value in hi]


def solver_snap(
    source: dict[str, Any],
    *,
    radius: Fraction = SNAP_RADIUS,
    strict_dominance: bool = False,
) -> dict[str, Any]:
    """Run one bounded QF_LRA snap; all asserted values are exact rationals."""

    try:
        import z3
    except ImportError as exc:  # pragma: no cover - archived replay needs no Z3.
        raise RuntimeError("--resnap requires the bundled z3 package") from exc

    centers = rounded_centers(source)
    variables = [z3.Real(f"p_{index}") for index in range(8)]
    matrix = [[z3.RealVal(0) for _ in range(4)] for _ in range(4)]
    for column in range(4):
        c, d = variables[2 * column], variables[2 * column + 1]
        matrix[SIGMA[column]][column] = c
        first, second = REMAINING[column]
        matrix[first][column] = d
        matrix[second][column] = 1 - c - d

    solver = z3.Solver()
    solver.set(timeout=SOLVER_TIMEOUT_MS, random_seed=SEED)

    def zreal(value: Fraction | int) -> Any:
        fraction = Fraction(value)
        return z3.RealVal(f"{fraction.numerator}/{fraction.denominator}")

    assertions: list[z3.BoolRef] = []
    for variable, center in zip(variables, centers):
        lo = center - radius
        hi = center + radius
        assertions.extend((variable >= zreal(lo), variable <= zreal(hi)))

    floor = zreal(OFFDIAGONAL_FLOOR)
    for row in range(4):
        for column in range(4):
            if row != column:
                assertions.append(matrix[row][column] >= floor)

    dominance_floor = zreal(OFFDIAGONAL_FLOOR) if strict_dominance else zreal(0)
    for row in range(4):
        designated = matrix[row][SIGMA[row]]
        others = sum((matrix[row][column] for column in range(4) if column not in (row, SIGMA[row])), z3.RealVal(0))
        assertions.append(designated - others >= dominance_floor)
    assertions.append(sum((variables[2 * column] for column in range(4)), z3.RealVal(0)) > zreal(2))

    lo, hi = expanded_integer_box(source)
    points = list(itertools.product(*(range(lo[axis], hi[axis] + 1) for axis in range(3))))
    for point in points:
        lam = lambda_xyz(tuple(int(value) for value in point))
        zlam = [zreal(value) for value in lam]
        slacks = [sum((matrix[row][column] * zlam[column] for column in range(4)), z3.RealVal(0)) for row in range(4)]
        assertions.append(z3.Or(*(slack <= 0 for slack in slacks)))

    solver.add(*assertions)
    started = time.monotonic()
    status = solver.check()
    elapsed = time.monotonic() - started
    result: dict[str, Any] = {
        "status": str(status),
        "elapsed_seconds": elapsed,
        "timeout_ms": SOLVER_TIMEOUT_MS,
        "random_seed": SEED,
        "strict_row_dominance": strict_dominance,
        "center_parameters": parameter_strings(centers),
        "radius": str(radius),
        "expanded_integer_box": [lo, hi],
        "expanded_box_point_count": len(points),
        "assertion_count": len(assertions),
    }
    if status == z3.sat:
        model = solver.model()

        def model_fraction(expression: Any) -> Fraction:
            value = z3.simplify(model.eval(expression, model_completion=True))
            if not z3.is_rational_value(value):
                raise RuntimeError(f"non-rational LRA model value {value}")
            return Fraction(value.numerator_as_long(), value.denominator_as_long())

        parameters = tuple(model_fraction(variable) for variable in variables)
        result["parameters"] = parameter_strings(parameters)
        result["F"] = fmatrix_json(matrix_from_parameters(parameters))
        result["exact_model_parameters"] = parameters
    elif status == z3.unknown:
        result["reason_unknown"] = solver.reason_unknown()
    return result


def json_safe(value: Any) -> Any:
    if isinstance(value, Fraction):
        return str(value)
    if isinstance(value, tuple):
        return [json_safe(item) for item in value]
    if isinstance(value, list):
        return [json_safe(item) for item in value]
    if isinstance(value, dict):
        return {key: json_safe(item) for key, item in value.items()}
    return value


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--resnap", action="store_true", help="rerun the bounded QF_LRA snap")
    args = parser.parse_args()

    source = load_source()
    centers = rounded_centers(source)
    snap_attempts: list[dict[str, Any]] = []
    archived = bool(ARCHIVED_PARAMETERS)

    if args.resnap or not archived:
        # Baseline requested choice.  A second wider choice is permitted only
        # if this first bounded interval is UNSAT/UNKNOWN or fails exact checks.
        first = solver_snap(source, radius=SNAP_RADIUS, strict_dominance=False)
        snap_attempts.append(first)
        selected_parameters: tuple[Fraction, ...] | None = None
        if first.get("status") == "sat":
            selected_parameters = tuple(Fraction(value) for value in first["parameters"])
            try:
                exact_body(selected_parameters)
            except RuntimeError:
                selected_parameters = None
        if selected_parameters is None:
            second = solver_snap(source, radius=Fraction(1, 5_000), strict_dominance=False)
            second["reason_for_second_choice"] = "first 1e-4 interval did not yield an exact hollow body above 19/6"
            snap_attempts.append(second)
            if second.get("status") != "sat":
                raise RuntimeError(f"bounded snap choices failed: {snap_attempts}")
            selected_parameters = tuple(Fraction(value) for value in second["parameters"])
            # Never proceed from a second choice without exact certification.
            exact_body(selected_parameters)
        parameters = selected_parameters
    else:
        parameters = tuple(Fraction(value) for value in ARCHIVED_PARAMETERS)
        snap_attempts.append(
            {
                "status": "archived_exact_pin",
                "center_parameters": parameter_strings(centers),
                "radius": str(SNAP_RADIUS),
                "parameters": parameter_strings(parameters),
                "solver_run": False,
            }
        )

    body = exact_body(parameters)
    if not body["hollow"]["hollow"] or not Q.from_json(body["width"]["width"]) > Q(WIDTH_THRESHOLD):
        raise RuntimeError("final exact replay failed hollow/width requirement")

    output = {
        "status": "exact_rational_pair_column_witness",
        "source": {
            "file": str(SOURCE_JSON.relative_to(HERE)),
            "run_index": source["index"],
            "numeric_width": source["numeric_width"],
            "numeric_trust_status": source["trust_status"],
            "numeric_minimizing_directions": source["minimizing_directions"],
        },
        "snap": {
            "method": "bounded QF_LRA around rounded 1e-6 centers",
            "attempts": json_safe(snap_attempts),
            "archived_exact_pin": archived or bool(ARCHIVED_PARAMETERS),
            "offdiagonal_floor": str(OFFDIAGONAL_FLOOR),
            "row_dominance_baseline": ">=0",
            "strict_row_dominance_choice": "The archived exact witness has every row-dominance slack >=1/2000 > 1e-8; the certificate uses exact slacks, not solver provenance.",
            "sum_designated_strict": ">2",
            "finite_integer_box_OR": "expanded numeric vertex box by one in every coordinate; OR_i F lambda(z)<=0",
        },
        "exact": body,
        "scope": "One exact hollow pair-column witness reconstructed from a bounded numerical sample; no optimum or global claim.",
    }
    destination = HERE / "results" / "det2_pair_rationalization.json" if args.resnap else CERTIFICATE_JSON
    destination.write_text(json.dumps(output, indent=2) + "\n")
    print(
        json.dumps(
            {
                "status": output["status"],
                "width": body["width"]["width"],
                "boundary_count": body["boundary_count"],
                "row_pair_dominance_equalities": body["row_pair_dominance_equalities"],
                "certificate": str(destination.relative_to(HERE)),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
