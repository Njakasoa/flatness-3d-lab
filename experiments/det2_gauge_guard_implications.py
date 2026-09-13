"""QF_LRA cross-check of the six contact-edge gauge observer cuts.

The gauge certificate truncates the twelve observer lines to 64 points under
the six strict edge-gauge hypotheses gamma(v)>37/102.  Pair dominance makes
44 of those guards tautological, leaving 20 linear lattice exclusions.  This
experiment adds those 20 exclusions and the six exact gauge disjunctions to
the strict eight-variable column chart, then checks all 484 non-tautological
guards from the earlier volume-bounded observer certificate.

Every assertion is linear in F.  SAT records exact rational F parameters and
the missing observer point; UNKNOWN is never treated as an implication.
This is a finite necessary-relaxation check and makes no hollowness or width
bound claim.
"""

from __future__ import annotations

import itertools
import json
import time
from collections import Counter
from fractions import Fraction
from pathlib import Path
from typing import Any, Iterable, Sequence

import z3

try:
    from experiments import det2_pair_column_smt as column
    from experiments import det2_pair_lattice_closure as closure
except ModuleNotFoundError:  # Direct ``python experiments/...py`` invocation.
    import det2_pair_column_smt as column
    import det2_pair_lattice_closure as closure


HERE = Path(__file__).resolve().parents[1]
GAUGE_CERTIFICATE = HERE / "certificates" / "det2_observer_gauge_guards.json"
OBSERVER_CERTIFICATE = HERE / "certificates" / "det2_observer_lines.json"
JSON_OUT = HERE / "results" / "det2_gauge_guard_implications.json"

BETA = Fraction(37, 102)
PER_QUERY_TIMEOUT_MS = 10_000
GLOBAL_WALL_SECONDS = 120.0
EXPECTED_GAUGE_POINTS = 64
EXPECTED_GAUGE_GUARDS = 20
EXPECTED_OBSERVER_GUARDS = 484
SIGMA = (1, 0, 3, 2)


def point_tuple(values: Iterable[int]) -> tuple[int, int, int]:
    point = tuple(int(value) for value in values)
    if len(point) != 3:
        raise AssertionError(f"expected a 3D point, got {point}")
    return point  # type: ignore[return-value]


def fraction_text(value: Fraction) -> str:
    return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"


def z3_fraction(value: Fraction) -> z3.ArithRef:
    return z3.RealVal(fraction_text(value))


def ell(vector: Sequence[int]) -> tuple[Fraction, Fraction, Fraction, Fraction]:
    """Linear (sum-zero) contact barycentrics of a spatial vector."""

    x, y, z = (Fraction(value) for value in vector)
    answer = (x / 2 - y - z, x / 2, y - x / 2, z - x / 2)
    if sum(answer) != 0:
        raise AssertionError(f"edge difference coordinates do not sum to zero: {vector}")
    return answer


def exact_scalar(model: z3.ModelRef, expression: z3.ArithRef) -> str:
    return z3.simplify(model.eval(expression, model_completion=True)).sexpr()


def exact_model(
    model: z3.ModelRef,
    c: Sequence[z3.ArithRef],
    d: Sequence[z3.ArithRef],
    matrix: Sequence[Sequence[z3.ArithRef]],
) -> dict[str, Any]:
    return {
        "parameters": {
            "c": [exact_scalar(model, value) for value in c],
            "d": [exact_scalar(model, value) for value in d],
        },
        "F": [
            [exact_scalar(model, value) for value in row]
            for row in matrix
        ],
    }


def guard_clause(
    matrix: Sequence[Sequence[z3.ArithRef]],
    point: tuple[int, int, int],
    rows: Sequence[int],
) -> z3.BoolRef:
    return closure.clause_for_point(matrix, point, rows)


def gauge_clause(
    matrix: Sequence[Sequence[z3.ArithRef]],
    edge: Sequence[int],
) -> z3.BoolRef:
    """Encode gamma(edge)>beta as the 14 proper subset-sum disjunction."""

    coordinates = ell(edge)
    transformed = [
        z3.simplify(
            sum(matrix[row][j] * z3_fraction(coordinates[j]) for j in range(4)),
            som=True,
        )
        for row in range(4)
    ]
    # Column sums and sum(ell)=0 make this identity exact.  Checking it here
    # guards against accidentally encoding an affine, rather than difference,
    # barycentric vector.
    if not z3.is_true(z3.simplify(sum(transformed) == 0)):
        raise AssertionError(f"F ell({tuple(edge)}) is not symbolically zero-sum")
    subset_sums = [
        sum(transformed[index] for index in range(4) if mask & (1 << index))
        for mask in range(1, 15)
    ]
    return z3.Or(*(value > z3_fraction(BETA) for value in subset_sums))


def load_certificates() -> tuple[
    dict[str, Any],
    dict[str, Any],
    list[tuple[int, int, int]],
    dict[tuple[int, int, int], tuple[int, ...]],
    list[tuple[int, int, int]],
    dict[tuple[int, int, int], tuple[int, ...]],
    list[tuple[int, int, int]],
]:
    gauge_certificate = json.loads(GAUGE_CERTIFICATE.read_text())
    observer_certificate = json.loads(OBSERVER_CERTIFICATE.read_text())
    if gauge_certificate.get("guard_count") != EXPECTED_GAUGE_POINTS:
        raise AssertionError("gauge certificate point count changed")
    if gauge_certificate.get("pair_nontrivial_count") != EXPECTED_GAUGE_GUARDS:
        raise AssertionError("gauge certificate nontrivial count changed")
    if gauge_certificate.get("pair_tautological_count") != 44:
        raise AssertionError("gauge certificate tautological count changed")
    if observer_certificate.get("pair_nontrivial_count") != EXPECTED_OBSERVER_GUARDS:
        raise AssertionError("observer certificate candidate count changed")

    def records_by_point(
        records: Sequence[dict[str, Any]],
    ) -> tuple[list[tuple[int, int, int]], dict[tuple[int, int, int], tuple[int, ...]]]:
        points: list[tuple[int, int, int]] = []
        rows: dict[tuple[int, int, int], tuple[int, ...]] = {}
        for record in records:
            if record.get("tautological", False):
                continue
            point = point_tuple(record["point"])
            possible = tuple(int(row) for row in record["possible_blocking_rows"])
            if point in rows or not possible:
                raise AssertionError(f"duplicate or empty pair guard {point}")
            profile = closure.simplify_clause(point)
            if profile["classification"] != "retained":
                raise AssertionError(f"pair guard is not retained: {point}")
            if tuple(profile["possible_rows"]) != possible:
                raise AssertionError(f"pair profile changed at {point}")
            points.append(point)
            rows[point] = possible
        return points, rows

    gauge_points, gauge_rows = records_by_point(gauge_certificate["guards"])
    observer_points, observer_rows = records_by_point(observer_certificate["guards"])
    if len(gauge_points) != EXPECTED_GAUGE_GUARDS:
        raise AssertionError("gauge guard records do not match count")
    if len(observer_points) != EXPECTED_OBSERVER_GUARDS:
        raise AssertionError("observer guard records do not match count")
    listed_gauge = {
        point_tuple(point) for point in gauge_certificate["pair_nontrivial_points"]
    }
    listed_observer = {
        point_tuple(point) for point in observer_certificate["pair_nontrivial_points"]
    }
    if listed_gauge != set(gauge_points) or listed_observer != set(observer_points):
        raise AssertionError("certificate point lists disagree with guard records")
    if not set(gauge_points).issubset(set(observer_points)):
        raise AssertionError("gauge guards must be among the 484 observer candidates")

    edge_directions = [point_tuple(edge) for edge in gauge_certificate["edge_directions"]]
    if len(edge_directions) != 6 or len(set(edge_directions)) != 6:
        raise AssertionError("expected six distinct edge directions")
    if gauge_certificate.get("beta") != fraction_text(BETA):
        raise AssertionError("gauge certificate beta changed")
    return (
        gauge_certificate,
        observer_certificate,
        gauge_points,
        gauge_rows,
        observer_points,
        observer_rows,
        edge_directions,
    )


def query_guard(
    solver: z3.Solver,
    matrix: Sequence[Sequence[z3.ArithRef]],
    point: tuple[int, int, int],
    rows: Sequence[int],
    c: Sequence[z3.ArithRef],
    d: Sequence[z3.ArithRef],
    deadline: float,
) -> dict[str, Any]:
    """Test antecedent => guard by asserting every possible blocker is >0."""

    remaining = deadline - time.monotonic()
    if remaining <= 0:
        return {"status": "unknown", "reason": "global_wallcap", "elapsed_seconds": 0.0}
    timeout_ms = max(1, min(PER_QUERY_TIMEOUT_MS, int(remaining * 1000)))
    solver.set(timeout=timeout_ms)
    solver.push()
    started = time.monotonic()
    solver.add(*(
        closure.z3_slack(matrix, point, row) > 0
        for row in rows
    ))
    status = solver.check()
    elapsed = time.monotonic() - started
    result: dict[str, Any] = {
        "status": str(status),
        "elapsed_seconds": elapsed,
        "timeout_ms": timeout_ms,
    }
    if status == z3.sat:
        result["exact_F_parameters"] = exact_model(solver.model(), c, d, matrix)
    elif status == z3.unknown:
        result["reason"] = solver.reason_unknown() or (
            "global_wallcap" if deadline - time.monotonic() <= 0 else "solver_unknown"
        )
    solver.pop()
    return result


def status_counts(records: Sequence[dict[str, Any]]) -> dict[str, int]:
    counts = Counter(record["status"] for record in records)
    return {key: counts[key] for key in ("unsat", "sat", "unknown") if counts[key]}


def main() -> None:
    started = time.monotonic()
    (
        gauge_certificate,
        observer_certificate,
        gauge_points,
        gauge_rows,
        observer_points,
        observer_rows,
        edge_directions,
    ) = load_certificates()

    c, d = column.column_parameters()
    matrix = column.column_matrix(c, d)
    domain = closure.pair_domain_constraints(matrix, c, d)
    gamma_clauses = [gauge_clause(matrix, edge) for edge in edge_directions]
    gauge_guard_clauses = [
        guard_clause(matrix, point, gauge_rows[point])
        for point in gauge_points
    ]

    solver = z3.Solver()
    solver.add(*domain, *gamma_clauses, *gauge_guard_clauses)
    base_started = time.monotonic()
    base_status = solver.check()
    base_elapsed = time.monotonic() - base_started
    if base_status != z3.sat:
        raise AssertionError(
            "the gauge antecedent must be SAT before implication checks: "
            f"status={base_status}, reason={solver.reason_unknown()}"
        )
    deadline = started + GLOBAL_WALL_SECONDS
    records: list[dict[str, Any]] = []
    for point in observer_points:
        outcome = query_guard(
            solver, matrix, point, observer_rows[point], c, d, deadline
        )
        records.append({"point": list(point), **outcome})

    counts = status_counts(records)
    result = {
        "status": "observer_gauge_qf_lra_implications",
        "certificates": {
            "gauge_path": str(GAUGE_CERTIFICATE.relative_to(HERE)),
            "observer_path": str(OBSERVER_CERTIFICATE.relative_to(HERE)),
            "gauge_point_count": gauge_certificate["guard_count"],
            "gauge_pair_nontrivial_count": gauge_certificate["pair_nontrivial_count"],
            "gauge_pair_tautological_count": gauge_certificate["pair_tautological_count"],
            "observer_pair_nontrivial_count": observer_certificate["pair_nontrivial_count"],
            "observer_pair_tautological_count": observer_certificate["pair_tautological_count"],
            "gauge_pair_signature_counts": {
                str(rows): count
                for rows, count in Counter(gauge_rows.values()).items()
            },
        },
        "gauge_encoding": {
            "beta": fraction_text(BETA),
            "edge_directions": [list(edge) for edge in edge_directions],
            "ell_definition": "ell(X,Y,Z)=(X/2-Y-Z,X/2,Y-X/2,Z-X/2)",
            "proper_subset_disjunct_count_per_edge": 14,
            "strict_cut": "Or(sum_{i in I}(F*ell(v))_i > 37/102) over all nonempty proper I",
            "gauge_clause_count": len(gamma_clauses),
            "pair_guard_clause_count": len(gauge_guard_clauses),
        },
        "solver": {
            "logic": "QF_LRA",
            "name": "z3",
            "variables": [*(f"c_{i}" for i in range(4)), *(f"d_{i}" for i in range(4))],
            "variable_count": 8,
            "per_query_timeout_ms": PER_QUERY_TIMEOUT_MS,
            "global_wall_cap_seconds": GLOBAL_WALL_SECONDS,
            "push_pop_negation": True,
            "nra_atoms": False,
            "antecedent_assertion_count": len(domain) + len(gamma_clauses) + len(gauge_guard_clauses),
            "domain": "strict off-diagonal positivity, pair dominance, column sums one, and D=sum(c)>2",
            "antecedent_satisfiability": {
                "status": str(base_status),
                "elapsed_seconds": base_elapsed,
            },
        },
        "candidate_implications": {
            "candidate_count": len(records),
            "status_counts": counts,
            "exact_implication_count": counts.get("unsat", 0),
            "sat_missing_guard_count": counts.get("sat", 0),
            "unknown_count": counts.get("unknown", 0),
            "records": records,
        },
        "scope": {
            "finite_crosscheck_only": True,
            "no_hollow_conclusion": True,
            "no_global_width_bound": True,
            "no_3_4_bound": True,
            "sat_witnesses_are_missing_guards": True,
        },
        "elapsed_seconds": time.monotonic() - started,
    }
    JSON_OUT.write_text(json.dumps(result, indent=2) + "\n")
    print(
        json.dumps(
            {
                "status": result["status"],
                "status_counts": counts,
                "elapsed_seconds": result["elapsed_seconds"],
            }
        )
    )


if __name__ == "__main__":
    main()
