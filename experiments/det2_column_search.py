"""Bounded numerical search in the eight-variable column chart.

This is an exploratory companion to the determinant-two pair-branch SMT
relaxations.  The variables are the eight independent entries of a positive
column-stochastic matrix ``F`` with sigma=(01)(23); the fourth off-diagonal
entry in each column is ``1-c-d``.  The body vertices are the columns of
``F^{-1}``, converted from contact barycentric coordinates to (X,Y,Z).

The optimization is a max-min epigraph problem with nine variables (the
eight F parameters and a width variable).  It uses the exact 37 primitive
directions retained below contact width four and the 40 non-tautological
clauses from the structured hollow profile.  These clauses are only a finite
necessary hollowness screen.  Every reported width is numerical; a value is
marked trusted only after a separate full integer bounding-box scan succeeds
with the explicit 200000-point cap.

Run from ``flatness-3d-lab`` with ``python3 experiments/det2_column_search.py``.
The only output written by this script is ``results/det2_column_search.json``.
"""

from __future__ import annotations

import itertools
import json
import math
import time
from pathlib import Path
from typing import Any

import numpy as np
from scipy.optimize import OptimizeResult, minimize


HERE = Path(__file__).resolve().parents[1]
OUT = HERE / "results" / "det2_column_search.json"

SEED = 20260913
N_STARTS = 16
MAXITER = 400
WALL_CAP_SECONDS = 120.0
BOX_CAP = 200_000

SIGMA = (1, 0, 3, 2)
REMAINING = ((2, 3), (2, 3), (0, 1), (0, 1))
CONTACTS = np.asarray(
    ((0, 0, 0), (2, 1, 1), (0, 1, 0), (0, 0, 1)), dtype=float
)

# The ACMS volume consequence for a genuine hollow body of width >17/5 is
# vol(K)<21, hence det(F)>1/63.  This is a target-specific necessary cut and
# is recorded explicitly in the output.
DETERMINANT_FLOOR = 1.0 / 63.0
LAMBDA_LO = -62.0
LAMBDA_HI = 63.0
POSITIVITY_EPS = 1.0e-7
NUMERIC_TOL = 2.0e-6


def contact_width(direction: tuple[int, int, int]) -> int:
    values = [sum(u * x for u, x in zip(direction, p)) for p in CONTACTS.astype(int)]
    return max(values) - min(values)


def retained_directions() -> list[tuple[tuple[int, int, int], int]]:
    """Enumerate exactly the 37 primitive directions with contact width <=3."""

    directions: list[tuple[tuple[int, int, int], int]] = []
    # The bounds are exact for contact width <=3: |u_x|<=4 and
    # |u_y|,|u_z|<=3.  Modulo sign, retain the first nonzero coordinate >0.
    for direction in itertools.product(range(-4, 5), range(-3, 4), range(-3, 4)):
        if not any(direction) or math.gcd(*direction) != 1:
            continue
        if next(value for value in direction if value) < 0:
            continue
        width = int(contact_width(tuple(int(value) for value in direction)))
        if width <= 3:
            directions.append((tuple(int(value) for value in direction), width))
    return directions


DIRECTIONS = retained_directions()


def lambda_xyz(point: tuple[int, int, int]) -> np.ndarray:
    x, y, z = (float(value) for value in point)
    return np.asarray((1.0 + x / 2.0 - y - z, x / 2.0, y - x / 2.0, z - x / 2.0))


def row_domain_values(point_lambda: np.ndarray, row: int) -> tuple[float, float, float]:
    designated = SIGMA[row]
    first, second = REMAINING[row]
    # The closed row-domain triangle has vertices
    # (a,b,c)=(1,0,0),(1/2,1/2,0),(1/2,0,1/2).
    return (
        float(point_lambda[designated]),
        float((point_lambda[designated] + point_lambda[first]) / 2.0),
        float((point_lambda[designated] + point_lambda[second]) / 2.0),
    )


def hollow_profile() -> tuple[
    list[tuple[tuple[int, int, int], tuple[int, ...]]], list[tuple[int, int, int]]
]:
    """Reproduce the exact 40/176 profile from structured_hollowprofile."""

    retained: list[tuple[tuple[int, int, int], tuple[int, ...]]] = []
    tautological: list[tuple[int, int, int]] = []
    for point in itertools.product(range(-2, 4), repeat=3):
        point_tuple = tuple(int(value) for value in point)
        point_lambda = lambda_xyz(point_tuple)
        possible_rows: list[int] = []
        is_tautology = False
        for row in range(4):
            values = row_domain_values(point_lambda, row)
            row_min, row_max = min(values), max(values)
            if row_max <= 0.0:
                is_tautology = True
                break
            if row_min <= 0.0:
                possible_rows.append(row)
        if is_tautology:
            tautological.append(point_tuple)
        else:
            if not possible_rows:
                raise RuntimeError(f"empty non-tautological hollow clause at {point_tuple}")
            retained.append((point_tuple, tuple(possible_rows)))
    return retained, tautological


RETAINED_HOLLOW, TAUTOLOGICAL_HOLLOW = hollow_profile()


def matrix_from_parameters(parameters: np.ndarray) -> np.ndarray:
    """Build F from eight column parameters, with column sums automatic."""

    matrix = np.zeros((4, 4), dtype=float)
    for column in range(4):
        c, d = float(parameters[2 * column]), float(parameters[2 * column + 1])
        matrix[SIGMA[column], column] = c
        first, second = REMAINING[column]
        matrix[first, column] = d
        matrix[second, column] = 1.0 - c - d
    return matrix


def parameters_from_matrix(matrix: np.ndarray) -> np.ndarray:
    values: list[float] = []
    for column in range(4):
        values.extend((float(matrix[SIGMA[column], column]), float(matrix[REMAINING[column][0], column])))
    return np.asarray(values, dtype=float)


def body_vertices(matrix: np.ndarray) -> tuple[np.ndarray, np.ndarray] | None:
    """Return (vertices in XYZ, inverse columns in lambda coordinates)."""

    try:
        inverse = np.linalg.inv(matrix)
    except np.linalg.LinAlgError:
        return None
    if not np.isfinite(inverse).all():
        return None
    lambdas = inverse  # column j is F^{-1} e_j
    vertices = np.asarray(
        [
            (2.0 * lambdas[1, j], lambdas[1, j] + lambdas[2, j], lambdas[1, j] + lambdas[3, j])
            for j in range(4)
        ],
        dtype=float,
    )
    if not np.isfinite(vertices).all():
        return None
    return vertices, lambdas


def width_values(vertices: np.ndarray) -> np.ndarray:
    return np.asarray(
        [
            float(np.ptp(vertices @ np.asarray(direction, dtype=float)))
            for direction, _ in DIRECTIONS
        ],
        dtype=float,
    )


def row_dominance(matrix: np.ndarray) -> np.ndarray:
    return np.asarray(
        [
            matrix[row, SIGMA[row]]
            - sum(matrix[row, column] for column in range(4) if column not in (row, SIGMA[row]))
            for row in range(4)
        ],
        dtype=float,
    )


def coordinate_bounds(lambdas: np.ndarray) -> np.ndarray:
    """Return all target-domain lambda and ambient subset bound slacks."""

    values: list[float] = []
    for column in range(4):
        column_lambda = lambdas[:, column]
        values.extend((column_lambda - LAMBDA_LO).tolist())
        values.extend((LAMBDA_HI - column_lambda).tolist())
        ambient_12 = column_lambda[1] + column_lambda[2]
        ambient_13 = column_lambda[1] + column_lambda[3]
        values.extend((ambient_12 - LAMBDA_LO, LAMBDA_HI - ambient_12))
        values.extend((ambient_13 - LAMBDA_LO, LAMBDA_HI - ambient_13))
    return np.asarray(values, dtype=float)


def partial_hollow_slacks(matrix: np.ndarray) -> np.ndarray:
    """Return -min_i(F lambda(z)) for the 40 retained points."""

    output: list[float] = []
    for point, _possible_rows in RETAINED_HOLLOW:
        slacks = matrix @ lambda_xyz(point)
        output.append(float(-np.min(slacks)))
    return np.asarray(output, dtype=float)


def offdiagonal_entries(matrix: np.ndarray) -> np.ndarray:
    return np.asarray([matrix[i, j] for i in range(4) for j in range(4) if i != j], dtype=float)


def constraint_vector(candidate: np.ndarray) -> np.ndarray:
    """SLSQP inequalities, all required to be nonnegative."""

    parameters = np.asarray(candidate[:8], dtype=float)
    epigraph = float(candidate[8])
    matrix = matrix_from_parameters(parameters)
    determinant = float(np.linalg.det(matrix))
    geometry = body_vertices(matrix)

    constraints: list[float] = []
    constraints.extend((offdiagonal_entries(matrix) - POSITIVITY_EPS).tolist())
    constraints.extend(row_dominance(matrix).tolist())
    constraints.append(determinant - DETERMINANT_FLOOR)

    if geometry is None:
        # Keep the callback finite if SLSQP probes a singular point.  The
        # determinant constraint above then supplies a direction back in.
        constraints.extend([-1.0e6] * len(DIRECTIONS))
        constraints.extend([-1.0e6] * len(RETAINED_HOLLOW))
        constraints.extend([-1.0e6] * (4 * (4 * 2 + 4)))
        return np.asarray(constraints, dtype=float)

    vertices, lambdas = geometry
    constraints.extend((width_values(vertices) - epigraph).tolist())
    constraints.extend(partial_hollow_slacks(matrix).tolist())
    constraints.extend(coordinate_bounds(lambdas).tolist())
    return np.asarray(constraints, dtype=float)


def make_symmetric_control() -> np.ndarray:
    """The reviewed 3/2-width positive control, represented in F parameters."""

    control = np.asarray(
        (
            (0.0, 2.0 / 3.0, 1.0 / 6.0, 1.0 / 6.0),
            (2.0 / 3.0, 0.0, 1.0 / 6.0, 1.0 / 6.0),
            (1.0 / 6.0, 1.0 / 6.0, 0.0, 2.0 / 3.0),
            (1.0 / 6.0, 1.0 / 6.0, 2.0 / 3.0, 0.0),
        ),
        dtype=float,
    )
    return parameters_from_matrix(control)


def random_row_start(rng: np.random.Generator) -> tuple[np.ndarray, np.ndarray] | None:
    """Construct A row by row, then convert it to F=diag(r)A."""

    matrix_a = np.zeros((4, 4), dtype=float)
    designated = rng.uniform(0.51, 0.95, size=4)
    if float(np.sum(designated)) <= 2.0:
        return None
    for row in range(4):
        matrix_a[row, SIGMA[row]] = designated[row]
        rest = [column for column in range(4) if column not in (row, SIGMA[row])]
        split = rng.dirichlet((1.0, 1.0)) * (1.0 - designated[row])
        matrix_a[row, rest[0]], matrix_a[row, rest[1]] = split
    try:
        inverse_column_sums = np.linalg.solve(matrix_a.T, np.ones(4, dtype=float))
    except np.linalg.LinAlgError:
        return None
    if not np.isfinite(inverse_column_sums).all() or np.min(inverse_column_sums) <= POSITIVITY_EPS:
        return None
    matrix_f = np.diag(inverse_column_sums) @ matrix_a
    if not np.isfinite(matrix_f).all() or np.min(offdiagonal_entries(matrix_f)) <= POSITIVITY_EPS:
        return None
    if float(np.linalg.det(matrix_f)) <= DETERMINANT_FLOOR:
        return None
    return matrix_f, matrix_a


def make_starts() -> tuple[list[np.ndarray], list[dict[str, Any]]]:
    rng = np.random.default_rng(SEED)
    starts: list[np.ndarray] = [make_symmetric_control()]
    metadata: list[dict[str, Any]] = [{"kind": "symmetric_control", "seed": None}]
    attempts = 0
    while len(starts) < N_STARTS and attempts < 100_000:
        attempts += 1
        generated = random_row_start(rng)
        if generated is None:
            continue
        matrix_f, matrix_a = generated
        starts.append(parameters_from_matrix(matrix_f))
        metadata.append(
            {
                "kind": "seeded_row_A",
                "seed": SEED,
                "attempt": attempts,
                "A": matrix_a.tolist(),
                "r": np.linalg.solve(matrix_a.T, np.ones(4, dtype=float)).tolist(),
            }
        )
    if len(starts) != N_STARTS:
        raise RuntimeError(f"could only construct {len(starts)} of {N_STARTS} starts")
    return starts, metadata


def start_epigraph(parameters: np.ndarray) -> float:
    geometry = body_vertices(matrix_from_parameters(parameters))
    if geometry is None:
        return 0.0
    return max(0.0, float(np.min(width_values(geometry[0]))))


class WallCapReached(RuntimeError):
    pass


def optimize_start(
    parameters: np.ndarray,
    deadline: float,
) -> tuple[OptimizeResult | None, bool]:
    epigraph = start_epigraph(parameters)
    x0 = np.concatenate((parameters, np.asarray((epigraph,), dtype=float)))

    def objective(candidate: np.ndarray) -> float:
        return -float(candidate[8])

    def constraints(candidate: np.ndarray) -> np.ndarray:
        if time.monotonic() >= deadline:
            raise WallCapReached()
        return constraint_vector(candidate)

    def callback(_candidate: np.ndarray) -> None:
        if time.monotonic() >= deadline:
            raise WallCapReached()

    # c,d bounds are loose; derived third-column positivity and the full
    # off-diagonal positivity constraints are enforced above.
    bounds = [(POSITIVITY_EPS, 1.0 - POSITIVITY_EPS)] * 8 + [(0.0, 100.0)]
    try:
        result = minimize(
            objective,
            x0,
            method="SLSQP",
            bounds=bounds,
            constraints={"type": "ineq", "fun": constraints},
            callback=callback,
            options={"maxiter": MAXITER, "ftol": 1.0e-9, "disp": False},
        )
        return result, False
    except WallCapReached:
        return None, True


def constraint_violations(candidate: np.ndarray) -> dict[str, float]:
    parameters = np.asarray(candidate[:8], dtype=float)
    matrix = matrix_from_parameters(parameters)
    geometry = body_vertices(matrix)
    values: dict[str, float] = {
        "positive_offdiag_min": float(np.min(offdiagonal_entries(matrix))),
        "row_pair_dominance_min": float(np.min(row_dominance(matrix))),
        "determinant": float(np.linalg.det(matrix)),
        "determinant_floor_slack": float(np.linalg.det(matrix) - DETERMINANT_FLOOR),
    }
    if geometry is None:
        values.update(
            {
                "width_epigraph_min_slack": -math.inf,
                "partial_hollow_min_slack": -math.inf,
                "coordinate_min_slack": -math.inf,
            }
        )
        return values
    vertices, lambdas = geometry
    values["width_epigraph_min_slack"] = float(np.min(width_values(vertices) - candidate[8]))
    values["partial_hollow_min_slack"] = float(np.min(partial_hollow_slacks(matrix)))
    values["coordinate_min_slack"] = float(np.min(coordinate_bounds(lambdas)))
    return values


def classify_validity(violations: dict[str, float]) -> tuple[bool, list[str]]:
    failed: list[str] = []
    if violations["positive_offdiag_min"] <= POSITIVITY_EPS - NUMERIC_TOL:
        failed.append("positive_offdiagonal")
    if violations["row_pair_dominance_min"] < -NUMERIC_TOL:
        failed.append("row_pair_dominance")
    if violations["determinant_floor_slack"] < -NUMERIC_TOL:
        failed.append("determinant_or_volume_cut")
    if violations["width_epigraph_min_slack"] < -NUMERIC_TOL:
        failed.append("width_epigraph")
    if violations["partial_hollow_min_slack"] < -NUMERIC_TOL:
        failed.append("partial_hollow")
    if violations["coordinate_min_slack"] < -NUMERIC_TOL:
        failed.append("coordinate_bounds")
    return not failed, failed


def scan_integer_box(matrix: np.ndarray, vertices: np.ndarray, deadline: float) -> dict[str, Any]:
    """Perform the full numerical integer-box interior scan, capped at 200000."""

    lo = np.ceil(np.min(vertices, axis=0) - 1.0e-9).astype(int)
    hi = np.floor(np.max(vertices, axis=0) + 1.0e-9).astype(int)
    side_lengths = hi - lo + 1
    if np.any(side_lengths <= 0):
        return {
            "status": "numeric_hollow",
            "integer_box": [lo.tolist(), hi.tolist()],
            "box_size": 0,
            "interior_points": [],
            "full_integer_bbox_checked": True,
            "scan_tolerance": 1.0e-8,
        }
    box_size = int(np.prod(side_lengths, dtype=np.int64))
    result: dict[str, Any] = {
        "integer_box": [lo.tolist(), hi.tolist()],
        "box_size": box_size,
        "scan_tolerance": 1.0e-8,
    }
    if box_size > BOX_CAP:
        result.update(
            {
                "status": "box_cap",
                "interior_points": [],
                "full_integer_bbox_checked": False,
            }
        )
        return result

    interior: list[list[int]] = []
    for point in itertools.product(
        *(range(int(lo[axis]), int(hi[axis]) + 1) for axis in range(3))
    ):
        if time.monotonic() >= deadline:
            result.update(
                {
                    "status": "scan_wall_cap",
                    "interior_points": interior,
                    "full_integer_bbox_checked": False,
                }
            )
            return result
        slacks = matrix @ lambda_xyz(tuple(int(value) for value in point))
        if bool(np.all(slacks > 1.0e-8)):
            interior.append([int(value) for value in point])
    result.update(
        {
            "status": "numeric_nonhollow" if interior else "numeric_hollow",
            "interior_points": interior,
            "full_integer_bbox_checked": True,
        }
    )
    return result


def candidate_record(
    index: int,
    metadata: dict[str, Any],
    result: OptimizeResult | None,
    wall_cap: bool,
) -> dict[str, Any]:
    record: dict[str, Any] = {
        "index": index,
        "start": metadata,
        "wall_cap_during_optimization": wall_cap,
    }
    if result is None:
        record.update({"optimizer_status": "wall_cap", "trusted_width": None})
        return record

    candidate = np.asarray(result.x, dtype=float)
    matrix = matrix_from_parameters(candidate[:8])
    geometry = body_vertices(matrix)
    violations = constraint_violations(candidate)
    valid, failed = classify_validity(violations)
    record.update(
        {
            "optimizer_status": str(result.message),
            "optimizer_success": bool(result.success),
            "optimizer_iterations": int(getattr(result, "nit", 0)),
            "optimizer_objective_width": float(candidate[8]),
            "parameters": candidate[:8].tolist(),
            "F": matrix.tolist(),
            "constraint_violations": violations,
            "valid_numeric_constraints": valid,
            "invalid_reasons": failed,
        }
    )
    if geometry is None:
        record.update({"numeric_width": None, "trusted_width": None, "trust_status": "invalid_singular"})
        return record

    vertices, lambdas = geometry
    widths = width_values(vertices)
    minimum = float(np.min(widths))
    minimizers = [
        list(direction)
        for (direction, _contact_width), value in zip(DIRECTIONS, widths)
        if value <= minimum + 1.0e-6
    ]
    record.update(
        {
            "vertices": vertices.tolist(),
            "inverse_columns_lambda": lambdas.tolist(),
            "directional_widths": widths.tolist(),
            "numeric_width": minimum,
            "minimizing_directions": minimizers,
        }
    )
    if not valid:
        record.update({"trusted_width": None, "trust_status": "invalid_constraints"})
    else:
        record.update({"trusted_width": None, "trust_status": "pending_integer_bbox"})
    return record


def main() -> None:
    started = time.monotonic()
    deadline = started + WALL_CAP_SECONDS
    if len(DIRECTIONS) != 37:
        raise RuntimeError(f"expected 37 directions, got {len(DIRECTIONS)}")
    if len(RETAINED_HOLLOW) != 40 or len(TAUTOLOGICAL_HOLLOW) != 176:
        raise RuntimeError(
            f"expected 40 retained and 176 tautologies, got "
            f"{len(RETAINED_HOLLOW)} and {len(TAUTOLOGICAL_HOLLOW)}"
        )

    starts, start_metadata = make_starts()
    records: list[dict[str, Any]] = []
    cap_reached = False
    high_threshold = 2.0 + math.sqrt(2.0)

    for index, (parameters, metadata) in enumerate(zip(starts, start_metadata)):
        if time.monotonic() >= deadline:
            cap_reached = True
            break
        result, wall_cap = optimize_start(parameters, deadline)
        if wall_cap:
            cap_reached = True
        record = candidate_record(index, metadata, result, wall_cap)
        records.append(record)
        if record.get("numeric_width") is not None and record["numeric_width"] > high_threshold:
            print(
                json.dumps(
                    {
                        "event": "high_candidate",
                        "index": index,
                        "numeric_width": record["numeric_width"],
                        "threshold": high_threshold,
                        "trusted": record.get("trusted_width"),
                    }
                ),
                flush=True,
            )
        if wall_cap:
            break

    # Scan optimized geometrically valid candidates from largest numerical
    # width down.  The scan is bounded by the same global deadline.
    scan_order = sorted(
        [
            record
            for record in records
            if record.get("numeric_width") is not None
            and record.get("valid_numeric_constraints")
        ],
        key=lambda record: float(record["numeric_width"]),
        reverse=True,
    )
    for record in scan_order:
        if time.monotonic() >= deadline:
            cap_reached = True
            record["integer_box_scan"] = {"status": "scan_wall_cap", "full_integer_bbox_checked": False}
            continue
        matrix = np.asarray(record["F"], dtype=float)
        vertices = np.asarray(record["vertices"], dtype=float)
        scan = scan_integer_box(matrix, vertices, deadline)
        record["integer_box_scan"] = scan
        if scan.get("status") == "scan_wall_cap":
            cap_reached = True
        if scan.get("status") == "numeric_hollow":
            record["trusted_width"] = float(record["numeric_width"])
            record["trust_status"] = "numeric_hollow"
        elif scan.get("status") == "numeric_nonhollow":
            record["trusted_width"] = None
            record["trust_status"] = "untrusted_nonhollow"
        elif scan.get("status") == "box_cap":
            record["trusted_width"] = None
            record["trust_status"] = "untrusted_box_cap"
        else:
            record["trusted_width"] = None
            record["trust_status"] = "untrusted_scan_incomplete"

    trusted = [record for record in records if record.get("trust_status") == "numeric_hollow"]
    valid = [record for record in records if record.get("valid_numeric_constraints")]
    best_hollow = max(trusted, key=lambda record: float(record["trusted_width"])) if trusted else None
    best_valid = max(valid, key=lambda record: float(record["numeric_width"])) if valid else None

    elapsed = time.monotonic() - started
    output: dict[str, Any] = {
        "status": "bounded_slsqp_exploration",
        "branch": "determinant_2_two_plus_two_sigma_(01)(23)",
        "seed": SEED,
        "elapsed_seconds": elapsed,
        "wall_cap_seconds": WALL_CAP_SECONDS,
        "wall_cap_reached": cap_reached,
        "optimizer": {
            "method": "scipy.optimize.minimize(method='SLSQP')",
            "variables": "eight F column parameters plus one max-min epigraph width",
            "starts_requested": N_STARTS,
            "starts_attempted": len(records),
            "maxiter_per_start": MAXITER,
            "symmetric_control_included": True,
            "volume_cut": "det(F)>=1/63 (equivalent to vol(K)<=21); target-specific necessary cut",
        },
        "chart": {
            "sigma": list(SIGMA),
            "remaining_rows_by_column": [list(rows) for rows in REMAINING],
            "column_parameterization": "F[sigma(j),j]=c_j; F[remaining[0],j]=d_j; F[remaining[1],j]=1-c_j-d_j",
            "contact_vertices_ambient": CONTACTS.astype(int).tolist(),
            "lambda_formula": ["1+X/2-Y-Z", "X/2", "Y-X/2", "Z-X/2"],
        },
        "directions": {
            "count": len(DIRECTIONS),
            "list": [{"u": list(direction), "contact_width": width} for direction, width in DIRECTIONS],
            "scope": "all primitive directions modulo sign with contact width <=3; next contact width is >=4",
        },
        "partial_hollow_profile": {
            "lattice_box": [[-2, 3], [-2, 3], [-2, 3]],
            "total_points": 216,
            "tautological_points": len(TAUTOLOGICAL_HOLLOW),
            "retained_clauses": len(RETAINED_HOLLOW),
            "constraint": "-min_i(F lambda(z)) >= 0 on each retained point",
            "status_scope": "necessary finite screen; not a whole-body hollow certificate",
        },
        "full_scan": {
            "box_cap": BOX_CAP,
            "status_labels": ["numeric_hollow", "numeric_nonhollow", "box_cap", "scan_wall_cap"],
            "exact_certificate": False,
        },
        "runs": records,
        "best_numeric_hollow": best_hollow,
        "best_valid_untrusted_or_hollow": best_valid,
        "high_threshold": high_threshold,
        "does_not_prove": "Any uniform width bound or exact hollowness; all optimization and scans are numerical.",
    }
    OUT.write_text(json.dumps(output, indent=2) + "\n")
    print(
        json.dumps(
            {
                "status": output["status"],
                "output": str(OUT),
                "starts_attempted": len(records),
                "elapsed_seconds": elapsed,
                "best_numeric_hollow": None
                if best_hollow is None
                else best_hollow.get("trusted_width"),
                "best_valid_width": None
                if best_valid is None
                else best_valid.get("numeric_width"),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
