"""Bounded numerical search in non-unimodular contact-tetrahedron orbits.

This is an exploratory companion to ``experiments/discovery.py``.  It keeps
the four lattice contacts fixed at one of the empty tetrahedra listed in
``results/empty_contact_tetrahedra.json`` and varies all eight real
barycentric degrees of freedom independently.  If ``C`` is the contact
matrix (its j-th column has a zero in row j), then

    P_aug = V_aug C,       V_aug = P_aug C^{-1}.

The optimization and the hollowness checks below are floating point only.
Rows are deliberately labelled ``numeric_*`` and are not certificates.  The
integer box is generated from the actual numerical vertex extrema for every
row that is accepted or retained as a screening candidate; there is no fixed
``[-N,N]^3`` search box.  Potential width directions are obtained from the
exact integer numerator condition

    |<u, p_i-p_0>| < 4,

using the global hollow-body width cap ``w < 4``.  Consequently a direction
omitted from the finite set cannot be a minimizer for a body satisfying that
cap.  This is a screening reduction, not a proof of the cap or of any
reported width.

The default run searches determinant 2--8 after the exact
lambda_1(P-P) pre-screen.  The determinant-17 table remains available for a
later bounded run; this file intentionally does not alter the enumeration or
the exact geometry engine.
"""

from __future__ import annotations

import argparse
import itertools
import json
import math
import time
from collections import Counter
from pathlib import Path
from typing import Any, Iterable

import numpy as np
from scipy.optimize import minimize
from scipy.spatial import ConvexHull


SEED = 20260913
W0 = 2.0 + math.sqrt(2.0)
GLOBAL_WIDTH_CAP = 4.0
INTERIOR_TOLERANCE = 1.0e-8
BOUNDARY_TOLERANCE = 3.0e-7
BOX_MARGIN = 1.0e-8

# The numerical volume/width theorem gives a much smaller meaningful region
# than an arbitrary blind lattice box.  These are evaluation safety caps: a
# row is retained only after its entire actual numerical box is checked.
MAX_VERTEX_COORDINATE = 40.0
MAX_BOX_POINTS = 2_000_000

DEFAULT_STARTS = 6
DEFAULT_SAMPLE_BUDGET = 900


# Exact pre-screen data supplied by the contact-orbit reduction.  The witness
# is a primitive integer vector attaining lambda_1(P-P) in these ten classes.
# The values are represented as strings so the JSON output does not pretend
# that the pre-screen itself was obtained by floating optimization.
PRESCREEN_DATA: dict[int, dict[str, Any]] = {
    1: {"lambda1": "1", "witness": [-2, -1, -1]},
    2: {"lambda1": "2/3", "witness": [-1, 0, 0]},
    3: {"lambda1": "1/2", "witness": [-1, 0, 0]},
    4: {"lambda1": "2/5", "witness": [-1, 0, 0]},
    5: {"lambda1": "3/5", "witness": [-2, 0, -1]},
    6: {"lambda1": "1/3", "witness": [-1, 0, 0]},
    7: {"lambda1": "2/7", "witness": [-1, 0, 0]},
    8: {"lambda1": "3/7", "witness": [-1, 0, 0]},
    9: {"lambda1": "1/4", "witness": [-1, 0, 0]},
    10: {"lambda1": "1/2", "witness": [-3, 0, -1]},
}


def determinant_3x3(matrix: np.ndarray) -> int:
    """Return the exact determinant of an integer 3 by 3 array."""

    a = np.asarray(matrix, dtype=np.int64)
    return int(
        a[0, 0] * (a[1, 1] * a[2, 2] - a[1, 2] * a[2, 1])
        - a[0, 1] * (a[1, 0] * a[2, 2] - a[1, 2] * a[2, 0])
        + a[0, 2] * (a[1, 0] * a[2, 1] - a[1, 1] * a[2, 0])
    )


def adjugate_3x3(matrix: np.ndarray) -> np.ndarray:
    """Return the exact integer adjugate of a 3 by 3 array."""

    a = np.asarray(matrix, dtype=np.int64)
    return np.array(
        [
            [
                a[1, 1] * a[2, 2] - a[1, 2] * a[2, 1],
                a[0, 2] * a[2, 1] - a[0, 1] * a[2, 2],
                a[0, 1] * a[1, 2] - a[0, 2] * a[1, 1],
            ],
            [
                a[1, 2] * a[2, 0] - a[1, 0] * a[2, 2],
                a[0, 0] * a[2, 2] - a[0, 2] * a[2, 0],
                a[0, 2] * a[1, 0] - a[0, 0] * a[1, 2],
            ],
            [
                a[1, 0] * a[2, 1] - a[1, 1] * a[2, 0],
                a[0, 1] * a[2, 0] - a[0, 0] * a[2, 1],
                a[0, 0] * a[1, 1] - a[0, 1] * a[1, 0],
            ],
        ],
        dtype=np.int64,
    )


def primitive_signed(vector: Iterable[int]) -> tuple[int, int, int] | None:
    """Normalize a nonzero integer vector modulo sign and gcd."""

    values = np.asarray(tuple(int(v) for v in vector), dtype=np.int64)
    if not np.any(values):
        return None
    gcd = int(np.gcd.reduce(np.abs(values)))
    if gcd == 0:
        return None
    values //= gcd
    positive = tuple(int(v) for v in values)
    negative = tuple(-int(v) for v in values)
    return min(positive, negative)


def finite_direction_set(
    contacts: np.ndarray, width_cap: int = int(GLOBAL_WIDTH_CAP)
) -> tuple[np.ndarray, dict[str, Any]]:
    """Derive all primitive directions allowed by |B^T u|_infinity < width_cap.

    If B has columns p_i-p_0, every integer direction u with body width less
    than four has q=B^T u with integer coordinates in {-3,...,3}.  Solving
    B^T u=q using the integer adjugate avoids a coordinate cutoff in u.
    """

    p = np.asarray(contacts, dtype=np.int64)
    differences = (p[1:] - p[0]).T
    matrix = differences.T
    determinant = determinant_3x3(matrix)
    if determinant == 0:
        raise ValueError("contact tetrahedron is degenerate")
    adjugate = adjugate_3x3(matrix)
    denominator = abs(determinant)
    directions: set[tuple[int, int, int]] = set()
    numerators: dict[tuple[int, int, int], tuple[int, int, int]] = {}
    for q in itertools.product(range(-width_cap + 1, width_cap), repeat=3):
        if q == (0, 0, 0):
            continue
        numerator = adjugate @ np.asarray(q, dtype=np.int64)
        if determinant < 0:
            numerator = -numerator
        if np.any(numerator % denominator):
            continue
        direction = primitive_signed(numerator // denominator)
        if direction is None:
            continue
        directions.add(direction)
        numerators[direction] = tuple(
            int(x) for x in differences.T @ np.asarray(direction, dtype=np.int64)
        )
    ordered = np.asarray(sorted(directions), dtype=np.int64)
    return ordered, {
        "derivation": "q=B^T u, q in {-3,...,3}^3, integer adjugate solve",
        "width_cap_strict": width_cap,
        "contact_difference_matrix_columns": differences.tolist(),
        "contact_difference_determinant": int(determinant),
        "primitive_mod_sign": True,
        "direction_count": int(len(ordered)),
        "directions": ordered.tolist(),
        "difference_numerators_Bt_u": {
            str([int(v) for v in direction]): list(
                numerators[tuple(int(v) for v in direction)]
            )
            for direction in ordered
        },
    }


def body_from_parameters(
    contacts: np.ndarray, parameters: np.ndarray
) -> tuple[np.ndarray, np.ndarray]:
    """Build V and C from eight unconstrained real logit parameters."""

    values = np.asarray(parameters, dtype=float)
    if values.shape != (8,):
        raise ValueError("the contact chart has exactly eight real parameters")
    contact_matrix = np.zeros((4, 4), dtype=float)
    for column in range(4):
        logits = np.array(
            [values[2 * column], values[2 * column + 1], 0.0], dtype=float
        )
        logits -= np.max(logits)
        weights = np.exp(logits)
        weights /= np.sum(weights)
        rows = [row for row in range(4) if row != column]
        contact_matrix[rows, column] = weights
    p_augmented = np.vstack([np.asarray(contacts, dtype=float).T, np.ones(4)])
    # P_aug = V_aug C.  Solve on the right without forming a matrix inverse.
    v_augmented = np.linalg.solve(contact_matrix.T, p_augmented.T).T
    vertices = v_augmented[:3].T
    if not np.isfinite(vertices).all():
        raise np.linalg.LinAlgError("nonfinite contact-chart vertex")
    return vertices, contact_matrix


def _integer_grid(lower: np.ndarray, upper: np.ndarray) -> np.ndarray:
    """Create the complete integer box requested by a numerical assessment."""

    axes = [np.arange(int(a), int(b) + 1, dtype=np.int64) for a, b in zip(lower, upper)]
    mesh = np.meshgrid(*axes, indexing="ij")
    return np.stack(mesh, axis=-1).reshape(-1, 3)


def assess_body(
    vertices: np.ndarray,
    contacts: np.ndarray,
    directions: np.ndarray,
    *,
    max_vertex_coordinate: float = MAX_VERTEX_COORDINATE,
    max_box_points: int = MAX_BOX_POINTS,
) -> dict[str, Any]:
    """Assess one body, including its complete numerical integer bounding box."""

    result: dict[str, Any] = {"valid_geometric_body": False}
    values = np.asarray(vertices, dtype=float)
    if values.shape != (4, 3) or not np.isfinite(values).all():
        result["rejection"] = "nonfinite_or_wrong_vertex_shape"
        return result
    if float(np.max(np.abs(values))) > max_vertex_coordinate:
        result["rejection"] = "vertex_coordinate_cap"
        result["max_abs_vertex_coordinate"] = float(np.max(np.abs(values)))
        return result
    try:
        hull = ConvexHull(values)
    except Exception as exc:  # scipy raises several Qhull-specific classes
        result["rejection"] = "degenerate_hull"
        result["hull_error"] = str(exc)
        return result

    lower = np.floor(np.min(values, axis=0) - BOX_MARGIN).astype(np.int64)
    upper = np.ceil(np.max(values, axis=0) + BOX_MARGIN).astype(np.int64)
    shape = upper - lower + 1
    box_points = int(np.prod(shape, dtype=np.int64))
    result.update(
        {
            "vertices": values.tolist(),
            "facet_equations": hull.equations.tolist(),
            "facet_count": int(len(hull.equations)),
            "volume_numeric": float(hull.volume),
            "integer_bbox_lower": lower.tolist(),
            "integer_bbox_upper": upper.tolist(),
            "integer_bbox_shape": shape.tolist(),
            "integer_bbox_points": box_points,
        }
    )
    if box_points > max_box_points:
        result["rejection"] = "integer_bbox_cap"
        return result

    points = _integer_grid(lower, upper)
    equations = np.asarray(hull.equations, dtype=float)
    slacks = -(points @ equations[:, :3].T + equations[:, 3])
    minimum_slack = np.min(slacks, axis=1)
    closed = np.all(slacks >= -BOUNDARY_TOLERANCE, axis=1)
    interior = np.all(slacks > INTERIOR_TOLERANCE, axis=1)
    interior_points = points[interior]
    boundary = points[closed & np.any(np.abs(slacks) <= BOUNDARY_TOLERANCE, axis=1)]
    relative_counts: list[int] = []
    for facet in range(len(equations)):
        on_facet = np.abs(slacks[:, facet]) <= BOUNDARY_TOLERANCE
        if len(equations) == 1:
            strict_other = np.ones(len(points), dtype=bool)
        else:
            strict_other = np.all(
                np.delete(slacks, facet, axis=1) > BOUNDARY_TOLERANCE, axis=1
            )
        relative_counts.append(int(np.sum(closed & on_facet & strict_other)))

    if len(directions):
        widths = np.ptp(values @ np.asarray(directions, dtype=float).T, axis=0)
        width = float(np.min(widths))
        active = np.asarray(directions)[widths <= width + 1.0e-6]
    else:
        widths = np.empty(0, dtype=float)
        width = float("nan")
        active = np.empty((0, 3), dtype=np.int64)

    contact_slacks = -(
        np.asarray(contacts, dtype=float) @ equations[:, :3].T + equations[:, 3]
    )
    result.update(
        {
            "valid_geometric_body": True,
            "integer_points_checked": int(len(points)),
            "interior_integer_point_count": int(len(interior_points)),
            "interior_integer_points_sample": interior_points[:16].tolist(),
            "hollow_numeric": bool(len(interior_points) == 0),
            "minimum_integer_slack_max": float(np.maximum(minimum_slack, 0.0).max(initial=0.0)),
            "boundary_lattice_points_numeric": boundary.tolist(),
            "relative_interior_contact_counts": relative_counts,
            "directional_widths": [float(x) for x in widths],
            "width_directional_screened": width,
            "active_directions_numeric": active.tolist(),
            "contact_facet_slacks": contact_slacks.tolist(),
            "full_integer_bbox_checked": True,
            "bbox_margin": BOX_MARGIN,
            "interior_tolerance": INTERIOR_TOLERANCE,
            "boundary_tolerance": BOUNDARY_TOLERANCE,
        }
    )
    return result


def parse_fraction(value: str) -> float:
    """Parse the small rational strings in ``PRESCREEN_DATA`` for comparison."""

    if value == "1":
        return 1.0
    numerator, denominator = value.split("/", 1)
    return float(int(numerator) / int(denominator))


def prescreen_record(class_id: int) -> dict[str, Any] | None:
    """Return the exact necessary pre-screen data when available."""

    data = PRESCREEN_DATA.get(class_id)
    if data is None:
        return None
    ell = parse_fraction(str(data["lambda1"]))
    if ell >= 1.0:
        upper = None
    else:
        upper = (1.0 + 2.0 / math.sqrt(3.0)) / (1.0 - ell)
    survives = bool(upper is None or upper >= W0 - 1.0e-12)
    return {
        "lambda1_difference_body_exact": str(data["lambda1"]),
        "lambda1_witness_integer_direction": list(data["witness"]),
        "necessary_width_upper_bound_decimal": upper,
        "necessary_width_upper_bound": "infinity" if upper is None else upper,
        "survives_w0_pre_screen": survives,
        "inequality": "w(K) <= (1+2/sqrt(3))/(1-lambda1(P-P))",
        "scope": "necessary test for P subset K; no numerical optimization used",
    }


def _json_number(value: Any) -> Any:
    """Convert numpy scalars recursively enough for JSON rows."""

    if isinstance(value, np.generic):
        return value.item()
    if isinstance(value, dict):
        return {str(k): _json_number(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [_json_number(v) for v in value]
    return value


def det2_auxiliary_q_analysis(row: dict[str, Any]) -> dict[str, Any] | None:
    """Inspect the four integral q_j points in the determinant-two orbit.

    For this orbit, q_j=(sum_i p_i)/2-p_j are integral.  A hollow numerical
    body must place every q_j outside (or, at a limiting degeneracy, on) one
    of its four supporting facets.  The facet containing contact p_i is
    identified from the stored contact slacks.  This diagnostic is not used
    in optimization; it records whether the strict exclusions realize a
    4-cycle or a pair of 2-cycles.
    """

    if int(row.get("orbit_class_id", -1)) != 1:
        return None
    try:
        contacts = np.asarray(row["contact_vertices"], dtype=np.int64)
        numerator = np.sum(contacts, axis=0) - 2 * contacts
        if np.any(numerator % 2):
            return {"status": "not_integral", "q_points": []}
        q_points = numerator // 2
        contact_slacks = np.asarray(row["contact_facet_slacks_numeric"], dtype=float)
        equations = np.asarray(row["facet_equations_numeric"], dtype=float)
        if contact_slacks.shape != (4, 4) or equations.shape[0] != 4:
            return {"status": "missing_facet_data", "q_points": q_points.tolist()}
        contact_to_facet = np.argmin(contact_slacks, axis=1)
        facet_to_contact = {
            int(facet): int(contact) for contact, facet in enumerate(contact_to_facet)
        }
        q_slacks = -(q_points @ equations[:, :3].T + equations[:, 3])
        options: list[list[int]] = []
        for slacks in q_slacks:
            options.append(
                sorted(
                    {
                        int(facet_to_contact[int(facet)])
                        for facet in range(4)
                        if slacks[int(facet)] < -BOUNDARY_TOLERANCE
                    }
                )
            )
        permutation_types: list[str] = []
        permutations: list[list[int]] = []
        for permutation in itertools.permutations(range(4)):
            if any(permutation[j] == j for j in range(4)):
                continue
            if not all(permutation[j] in options[j] for j in range(4)):
                continue
            seen: set[int] = set()
            lengths: list[int] = []
            for start in range(4):
                if start in seen:
                    continue
                current = start
                length = 0
                while current not in seen:
                    seen.add(current)
                    length += 1
                    current = int(permutation[current])
                lengths.append(length)
            lengths.sort(reverse=True)
            if lengths == [4]:
                kind = "cycle4"
            elif lengths == [2, 2]:
                kind = "two_plus_two"
            else:
                kind = "other"
            permutation_types.append(kind)
            permutations.append([int(x) for x in permutation])
        return {
            "status": "strict_exclusion_matching" if permutations else "boundary_or_undetermined",
            "q_points": q_points.tolist(),
            "contact_to_facet": [int(x) for x in contact_to_facet],
            "facet_to_contact": {
                str(int(facet)): int(contact) for facet, contact in facet_to_contact.items()
            },
            "q_facet_slacks": q_slacks.tolist(),
            "strict_exclusion_options_by_q": options,
            "permutations": permutations,
            "permutation_types": sorted(set(permutation_types)),
        }
    except (KeyError, ValueError, TypeError):
        return None


def candidate_row(
    *,
    class_id: int,
    contact_class: dict[str, Any],
    contacts: np.ndarray,
    hnf: Any,
    directions: np.ndarray,
    direction_metadata: dict[str, Any],
    parameters: np.ndarray,
    contact_matrix: np.ndarray,
    assessment: dict[str, Any],
    source: str,
    source_index: int,
    optimization: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Build one self-contained, explicitly numerical candidate row."""

    hollow = bool(assessment.get("hollow_numeric", False))
    status = "numeric_hollow_candidate" if hollow else "numeric_nonhollow_screening"
    row = _json_number(
        {
            "status": status,
            "numeric_only": True,
            "exact_certificate": False,
            "orbit_class_id": class_id,
            "normalized_contact_determinant": int(contact_class["normalized_determinant"]),
            "contact_hnf": hnf,
            "contact_vertices": contacts.tolist(),
            "parameter_chart": {
                "free_real_variables": 8,
                "independent_no_symmetry": True,
                "column_j_zero_row_j": True,
                "positive_off_diagonal_softmax": True,
                "formula": "V_aug=P_aug C^{-1}",
            },
            "parameters_logit": [float(x) for x in parameters],
            "contact_matrix_C": contact_matrix.tolist(),
            "body_vertices": assessment.get("vertices"),
            "facet_equations_numeric": assessment.get("facet_equations"),
            "volume_numeric": assessment.get("volume_numeric"),
            "integer_bbox": {
                "lower": assessment.get("integer_bbox_lower"),
                "upper": assessment.get("integer_bbox_upper"),
                "shape": assessment.get("integer_bbox_shape"),
                "points_checked": assessment.get("integer_bbox_points"),
                "full_box_checked": assessment.get("full_integer_bbox_checked", False),
                "margin": assessment.get("bbox_margin"),
            },
            "integer_points_checked": assessment.get("integer_points_checked"),
            "interior_integer_point_count": assessment.get("interior_integer_point_count"),
            "interior_integer_points_sample": assessment.get("interior_integer_points_sample"),
            "hollow_numeric": hollow,
            "lattice_contacts_numeric": assessment.get("boundary_lattice_points_numeric"),
            "relative_interior_contact_counts": assessment.get(
                "relative_interior_contact_counts"
            ),
            "contact_facet_slacks_numeric": assessment.get("contact_facet_slacks"),
            "direction_set": direction_metadata,
            "directional_widths_numeric": assessment.get("directional_widths"),
            "width_directional_screened": assessment.get("width_directional_screened"),
            "active_directions_numeric": assessment.get("active_directions_numeric"),
            "global_width_cap_used": "w(K)<4",
            "rational_reconstruction_hint": {
                "reconstruct_from": ["contact_vertices", "contact_matrix_C", "body_vertices"],
                "suggested_limit_denominator": 10_000_000,
                "recompute_rule": "form P_aug C^{-1}, then exact hollow and width checks",
                "stored_parameters_are_float": True,
            },
            "source": source,
            "source_index": int(source_index),
            "optimization": optimization,
            "screening_tolerances": {
                "interior": INTERIOR_TOLERANCE,
                "boundary": BOUNDARY_TOLERANCE,
            },
        }
    )
    auxiliary = det2_auxiliary_q_analysis(row)
    if auxiliary is not None:
        row["det2_auxiliary_q_analysis"] = auxiliary
    return row


class SearchStopped(Exception):
    """Raised when a numeric hollow body exceeds w0 and needs exact review."""


def search_orbit(
    *,
    class_id: int,
    contact_class: dict[str, Any],
    rng: np.random.Generator,
    requested_starts: int,
    sample_budget: int,
    max_rows: int,
) -> tuple[dict[str, Any], list[dict[str, Any]], bool]:
    """Sample and optimize one fixed contact orbit."""

    contacts = np.asarray(contact_class["vertices"], dtype=np.int64)
    directions, direction_metadata = finite_direction_set(contacts)
    pre = prescreen_record(class_id)
    counts: Counter[str] = Counter()
    evaluations = 0
    valid_samples: list[tuple[float, np.ndarray, np.ndarray, dict[str, Any]]] = []
    hollow_samples: list[tuple[float, np.ndarray, np.ndarray, dict[str, Any]]] = []
    sample_start = time.perf_counter()

    def evaluate(parameters: np.ndarray) -> tuple[np.ndarray, np.ndarray, dict[str, Any]] | None:
        nonlocal evaluations
        evaluations += 1
        try:
            vertices, matrix = body_from_parameters(contacts, parameters)
        except (FloatingPointError, np.linalg.LinAlgError, ValueError):
            counts["chart_failure"] += 1
            return None
        assessment = assess_body(vertices, contacts, directions)
        if not assessment.get("valid_geometric_body", False):
            counts[str(assessment.get("rejection", "invalid"))] += 1
            return vertices, matrix, assessment
        counts["full_bbox_assessments"] += 1
        return vertices, matrix, assessment

    # The bounded pool is intentionally small.  Each accepted pool element
    # has already undergone the complete integer-box test.
    for _ in range(sample_budget):
        parameters = np.asarray(rng.normal(0.0, 1.1, size=8), dtype=float)
        evaluated = evaluate(parameters)
        if evaluated is None:
            continue
        vertices, matrix, assessment = evaluated
        if not assessment.get("valid_geometric_body", False):
            continue
        width = float(assessment["width_directional_screened"])
        item = (width, parameters.copy(), matrix.copy(), assessment)
        valid_samples.append(item)
        if assessment.get("hollow_numeric", False):
            hollow_samples.append(item)

    valid_samples.sort(key=lambda item: item[0], reverse=True)
    hollow_samples.sort(key=lambda item: item[0], reverse=True)
    selected: list[tuple[str, float, np.ndarray, np.ndarray, dict[str, Any]]] = []
    selected_keys: set[tuple[float, ...]] = set()
    for item in hollow_samples[:requested_starts]:
        key = tuple(np.round(item[1], 9))
        selected.append(("random_hollow_start", *item))
        selected_keys.add(key)
    # An orbit may have a very small hollow chart or no hollow sample at all.
    # Fill the bounded multistart budget with geometrically valid starts so
    # SLSQP can seek the hollow chamber; their status is retained explicitly.
    for item in valid_samples:
        if len(selected) >= requested_starts:
            break
        key = tuple(np.round(item[1], 9))
        if key in selected_keys:
            continue
        selected.append(("random_geometric_start", *item))
        selected_keys.add(key)

    rows: list[dict[str, Any]] = []
    best_nonhollow: tuple[float, np.ndarray, np.ndarray, dict[str, Any]] | None = None
    best_hollow: tuple[float, np.ndarray, np.ndarray, dict[str, Any]] | None = None
    stop_triggered = False

    def append_row(
        source: str,
        source_index: int,
        parameters: np.ndarray,
        matrix: np.ndarray,
        assessment: dict[str, Any],
        optimization: dict[str, Any] | None = None,
    ) -> None:
        nonlocal best_nonhollow, best_hollow, stop_triggered
        if not assessment.get("valid_geometric_body", False):
            return
        width = float(assessment["width_directional_screened"])
        item = (width, parameters.copy(), matrix.copy(), assessment)
        if assessment.get("hollow_numeric", False):
            if best_hollow is None or width > best_hollow[0]:
                best_hollow = item
        elif best_nonhollow is None or width > best_nonhollow[0]:
            best_nonhollow = item
        if len(rows) < max_rows:
            rows.append(
                candidate_row(
                    class_id=class_id,
                    contact_class=contact_class,
                    contacts=contacts,
                    hnf=contact_class["hnf"],
                    directions=directions,
                    direction_metadata=direction_metadata,
                    parameters=parameters,
                    contact_matrix=matrix,
                    assessment=assessment,
                    source=source,
                    source_index=source_index,
                    optimization=optimization,
                )
            )
        if assessment.get("hollow_numeric", False) and width > W0 + 1.0e-7:
            stop_triggered = True

    for index, (source, width, parameters, matrix, assessment) in enumerate(selected):
        append_row(source, index, parameters, matrix, assessment)
        if stop_triggered:
            # Keep the triggering row in the returned JSONL payload so the
            # parent process can reconstruct it before any further search.
            break

    # Cache one complete assessment per SLSQP point because objective and
    # constraints are called separately by scipy.
    for run_index, (source, start_width, start_parameters, _, start_assessment) in enumerate(
        selected
    ):
        cache: dict[tuple[float, ...], tuple[np.ndarray, np.ndarray, dict[str, Any]] | None] = {}

        def cached(parameters: np.ndarray):
            key = tuple(np.round(np.asarray(parameters, dtype=float), 12))
            if key not in cache:
                cache[key] = evaluate(np.asarray(parameters, dtype=float))
            return cache[key]

        def objective(y: np.ndarray) -> float:
            evaluated = cached(y[:8])
            if evaluated is None or not evaluated[2].get("valid_geometric_body", False):
                return 100.0 + float(np.linalg.norm(y[:8]))
            assessment = evaluated[2]
            depth = float(assessment.get("minimum_integer_slack_max", 0.0))
            # A large depth means an integer point is numerically interior.
            # This soft penalty keeps the SLSQP trajectory near hollow charts.
            return -float(y[8]) + 300.0 * depth

        def constraints(y: np.ndarray) -> np.ndarray:
            evaluated = cached(y[:8])
            if evaluated is None or not evaluated[2].get("valid_geometric_body", False):
                return np.full(len(directions), -100.0, dtype=float)
            widths = np.asarray(evaluated[2]["directional_widths"], dtype=float)
            return widths - float(y[8])

        initial_t = float(start_assessment["width_directional_screened"])
        initial = np.r_[start_parameters, initial_t]
        try:
            result = minimize(
                objective,
                initial,
                method="SLSQP",
                bounds=[(-3.0, 3.0)] * 8 + [(0.0, GLOBAL_WIDTH_CAP)],
                constraints={"type": "ineq", "fun": constraints},
                options={"maxiter": 120, "ftol": 1.0e-8, "disp": False},
            )
            optimization = {
                "method": "SLSQP_epigraph",
                "success": bool(result.success),
                "message": str(result.message),
                "iterations": int(getattr(result, "nit", -1)),
                "objective": float(result.fun),
                "epigraph_t": float(result.x[8]),
                "start_width": float(start_width),
                "start_source": source,
                "run_index": run_index,
            }
            optimized = cached(result.x[:8])
            if optimized is not None:
                vertices, matrix, assessment = optimized
                append_row(
                    "slsqp_epigraph_final",
                    run_index,
                    result.x[:8],
                    matrix,
                    assessment,
                    optimization,
                )
                if stop_triggered:
                    # Return the triggering candidate and stop the campaign
                    # only after the orbit summary has been assembled.
                    break
        except SearchStopped:
            raise
        except Exception as exc:  # retain the run accounting and continue
            counts["optimizer_exception"] += 1
            if len(rows) < max_rows:
                rows.append(
                    {
                        "status": "numeric_optimizer_exception",
                        "numeric_only": True,
                        "exact_certificate": False,
                        "orbit_class_id": class_id,
                        "source": "slsqp_epigraph_exception",
                        "source_index": run_index,
                        "error": str(exc),
                    }
                )

    elapsed = time.perf_counter() - sample_start
    summary: dict[str, Any] = {
        "orbit_class_id": class_id,
        "normalized_contact_determinant": int(contact_class["normalized_determinant"]),
        "contact_hnf": contact_class["hnf"],
        "contact_vertices": contacts.tolist(),
        "pre_screen": pre,
        "direction_set_count": int(len(directions)),
        "direction_set_derivation": direction_metadata,
        "starts_requested": int(requested_starts),
        "starts_used": int(len(selected)),
        "random_hollow_starts_found": int(len(hollow_samples)),
        "random_geometric_starts_found": int(len(valid_samples)),
        "optimization_runs": int(len(selected)),
        "accepted_numeric_rows": int(len(rows)),
        "full_bbox_assessments": int(counts["full_bbox_assessments"]),
        "assessment_count": int(evaluations),
        "assessment_rejections": dict(counts),
        "best_numeric_hollow_width": None if best_hollow is None else float(best_hollow[0]),
        "best_numeric_nonhollow_width": None
        if best_nonhollow is None
        else float(best_nonhollow[0]),
        "best_numeric_hollow_source": None
        if best_hollow is None
        else "row_orbit_best",
        "stop_rule_triggered": bool(stop_triggered),
        "elapsed_seconds": float(elapsed),
        "limits": [
            "numeric floating-point contact chart; no exact certification",
            "hollow test uses the complete numerical integer bounding box",
            "direction set is complete only under the supplied global width<4 cap",
            "four fixed contacts and four body facets; no square/nonsimplicial branch",
            "multistart points and optimization iterates are correlated",
        ],
    }
    return summary, rows, stop_triggered


def run(
    *,
    input_path: Path,
    summary_path: Path,
    candidates_path: Path,
    det_min: int = 2,
    det_max: int = 8,
    requested_starts: int = DEFAULT_STARTS,
    sample_budget: int = DEFAULT_SAMPLE_BUDGET,
    seed: int = SEED,
) -> dict[str, Any]:
    """Run the bounded campaign and write its JSON/JSONL audit artifacts."""

    source = json.loads(input_path.read_text())
    selected_classes = [
        (index, contact_class)
        for index, contact_class in enumerate(source["classes"])
        if det_min <= int(contact_class["normalized_determinant"]) <= det_max
    ]
    if not selected_classes:
        raise ValueError("no contact classes in requested determinant range")

    # The exact necessary bound is cheap and deliberately applied before any
    # numerical body evaluation.  For determinant > 8 the small hand-audited
    # table is incomplete, so unknown classes remain eligible.
    searched: list[tuple[int, dict[str, Any]]] = []
    screened_out: list[dict[str, Any]] = []
    for class_id, contact_class in selected_classes:
        pre = prescreen_record(class_id)
        if pre is not None and not pre["survives_w0_pre_screen"]:
            screened_out.append(
                {
                    "orbit_class_id": class_id,
                    "normalized_contact_determinant": int(
                        contact_class["normalized_determinant"]
                    ),
                    "contact_vertices": contact_class["vertices"],
                    "pre_screen": pre,
                    "status": "exact_necessary_bound_below_w0",
                }
            )
        else:
            searched.append((class_id, contact_class))

    rng = np.random.default_rng(seed)
    rows: list[dict[str, Any]] = []
    orbit_summaries: list[dict[str, Any]] = []
    stop_reason: str | None = None
    campaign_start = time.perf_counter()
    try:
        for class_id, contact_class in searched:
            summary, orbit_rows, stopped = search_orbit(
                class_id=class_id,
                contact_class=contact_class,
                rng=rng,
                requested_starts=requested_starts,
                sample_budget=sample_budget,
                max_rows=max(2 * requested_starts + 4, 12),
            )
            orbit_summaries.append(summary)
            rows.extend(orbit_rows)
            if stopped:
                stop_reason = (
                    f"class {class_id} yielded a numeric hollow candidate above w0; "
                    "stop for exact falsification"
                )
                break
    except SearchStopped as exc:
        stop_reason = str(exc) + "; stop for exact falsification"

    numeric_hollow = [row for row in rows if row.get("status") == "numeric_hollow_candidate"]
    det2_q_rows = [
        row.get("det2_auxiliary_q_analysis")
        for row in rows
        if row.get("orbit_class_id") == 1 and row.get("det2_auxiliary_q_analysis")
    ]
    det2_q_pattern_counts: Counter[str] = Counter()
    for analysis in det2_q_rows:
        for kind in analysis.get("permutation_types", []):
            det2_q_pattern_counts[str(kind)] += 1
    best_row = max(
        numeric_hollow,
        key=lambda row: float(row.get("width_directional_screened", -math.inf)),
        default=None,
    )
    by_det: Counter[str] = Counter(
        str(int(contact_class["normalized_determinant"]))
        for _, contact_class in selected_classes
    )
    summary = {
        "status": "numeric_exploration_stop_for_exact_review"
        if stop_reason
        else "numeric_exploration_complete",
        "seed": int(seed),
        "dimension": 3,
        "determinant_scope": {
            "requested_min": int(det_min),
            "requested_max": int(det_max),
            "available_table_max": 17,
            "classes_in_requested_range": dict(by_det),
        },
        "contact_class_source": str(input_path),
        "input_metadata": source.get("metadata", {}),
        "w0_decimal": W0,
        "global_width_cap_used": "w(K)<4",
        "pre_screen_formula": "w(K) <= (1+2/sqrt(3))/(1-lambda1(P-P))",
        "pre_screen_scope": "exact necessary test applied before numerical search",
        "searched_orbit_count": int(len(orbit_summaries)),
        "screened_out_orbit_count": int(len(screened_out)),
        "searched_orbits": orbit_summaries,
        "screened_out_orbits": screened_out,
        "numeric_candidate_rows": int(len(rows)),
        "numeric_hollow_candidate_rows": int(len(numeric_hollow)),
        "numeric_nonhollow_rows": int(
            sum(row.get("status") == "numeric_nonhollow_screening" for row in rows)
        ),
        "det2_auxiliary_qj_diagnostic": {
            "orbit_class_id": 1,
            "formula": "q_j=(sum_i p_i)/2-p_j",
            "candidate_rows_with_integral_q": int(len(det2_q_rows)),
            "strict_exclusion_permutation_type_counts": dict(det2_q_pattern_counts),
            "interpretation": "diagnostic only; boundary-limit rows may have no strict matching permutation",
        },
        "global_best_numeric_hollow": None
        if best_row is None
        else {
            "orbit_class_id": best_row["orbit_class_id"],
            "normalized_contact_determinant": best_row["normalized_contact_determinant"],
            "width_directional_screened": best_row["width_directional_screened"],
            "source": best_row["source"],
        },
        "stop_rule": {
            "triggered": bool(stop_reason),
            "reason": stop_reason,
            "action": "exactly reconstruct and falsify any numeric row above w0 before continuing",
        },
        "parameters": {
            "starts_requested_per_searched_orbit": int(requested_starts),
            "random_sample_budget_per_orbit": int(sample_budget),
            "max_rows_per_orbit": int(2 * requested_starts + 4),
            "parameter_bounds": [-3.0, 3.0],
            "epigraph_bounds": [0.0, GLOBAL_WIDTH_CAP],
            "interior_tolerance": INTERIOR_TOLERANCE,
            "boundary_tolerance": BOUNDARY_TOLERANCE,
            "max_vertex_coordinate": MAX_VERTEX_COORDINATE,
            "max_integer_bbox_points": MAX_BOX_POINTS,
        },
        "assumptions_and_limits": [
            "C has a zero diagonal and strictly positive off-diagonal columns, so each prescribed contact is in a numerical relative facet interior",
            "all eight real variables are independent; no symmetry is imposed",
            "the contact tetrahedron is held in the listed integer coordinates",
            "every retained candidate reports a complete numerical integer bounding box",
            "the finite direction set follows from P differences and the external global width<4 cap, not from a fixed direction cutoff",
            "all widths, hollowness, facets, and optimization outcomes are numerical labels only",
            "the exact pre-screen does not certify the body search and the body search does not certify the pre-screen",
            "the search covers only fixed four-facet contact tetrahedra; square, five-to-eight-facet, and nonsimplicial branches are outside scope",
        ],
        "elapsed_seconds": float(time.perf_counter() - campaign_start),
        "output_contract": {
            "candidates_jsonl": str(candidates_path),
            "summary_json": str(summary_path),
            "rational_reconstruction": "contact vertices, C, body vertices and logits are stored in every numerical row",
        },
    }

    candidates_path.parent.mkdir(parents=True, exist_ok=True)
    candidates_path.write_text("".join(json.dumps(_json_number(row), sort_keys=True) + "\n" for row in rows))
    summary_path.parent.mkdir(parents=True, exist_ok=True)
    summary_path.write_text(json.dumps(_json_number(summary), indent=2, sort_keys=True) + "\n")
    print(json.dumps(_json_number(summary), indent=2, sort_keys=True))
    return summary


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--input",
        type=Path,
        default=Path("results/empty_contact_tetrahedra.json"),
    )
    parser.add_argument(
        "--summary",
        type=Path,
        default=Path("results/contact_orbit_search.json"),
    )
    parser.add_argument(
        "--candidates",
        type=Path,
        default=Path("results/contact_orbit_candidates.jsonl"),
    )
    parser.add_argument("--det-min", type=int, default=2)
    parser.add_argument("--det-max", type=int, default=8)
    parser.add_argument("--starts", type=int, default=DEFAULT_STARTS)
    parser.add_argument("--sample-budget", type=int, default=DEFAULT_SAMPLE_BUDGET)
    parser.add_argument("--seed", type=int, default=SEED)
    args = parser.parse_args()
    if not 4 <= args.starts <= 8:
        raise SystemExit("--starts must be between 4 and 8")
    run(
        input_path=args.input,
        summary_path=args.summary,
        candidates_path=args.candidates,
        det_min=args.det_min,
        det_max=args.det_max,
        requested_starts=args.starts,
        sample_budget=args.sample_budget,
        seed=args.seed,
    )


if __name__ == "__main__":
    main()
