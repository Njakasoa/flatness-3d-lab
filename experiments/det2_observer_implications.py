"""QF_LRA implication screen for the complete observer guard list.

The observer certificate supplies 1,456 possible interior lattice points on
twelve lines.  Its 972 pair-tautological points can never be interior for a
strict pair row, so this experiment checks the remaining 484 guards against
the reviewed 48-clause antecedent: the 40 retained ``[-2,3]^3`` clauses and
the eight irredundant centralizer-closure clauses.

Only the column-stochastic pair chart is used here.  Every expression is
linear in the eight column parameters; there are no determinant, width, or
NRA atoms.  A SAT result is a missing guard in this finite relaxation and is
reported with exact rational F parameters.  It is not a hollowness or global
width conclusion.
"""

from __future__ import annotations

import json
import time
from collections import Counter
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
CERTIFICATE = HERE / "certificates" / "det2_observer_lines.json"
CLOSURE_RESULT = HERE / "results" / "det2_pair_lattice_closure.json"
JSON_OUT = HERE / "results" / "det2_observer_implications.json"

PER_QUERY_TIMEOUT_MS = 10_000
GLOBAL_WALL_SECONDS = 120.0
EXPECTED_GUARDS = 484
EXPECTED_OLD_CLAUSES = 40
EXPECTED_NEW_CLAUSES = 8


def point_tuple(values: Iterable[int]) -> tuple[int, int, int]:
    point = tuple(int(value) for value in values)
    if len(point) != 3:
        raise AssertionError(f"expected a 3D point, got {point}")
    return point  # type: ignore[return-value]


def scalar_text(model: z3.ModelRef, expression: z3.ArithRef) -> str:
    """Serialize a model value without converting an exact rational to float."""

    return z3.simplify(model.eval(expression, model_completion=True)).sexpr()


def exact_model(
    model: z3.ModelRef,
    c: Sequence[z3.ArithRef],
    d: Sequence[z3.ArithRef],
    matrix: Sequence[Sequence[z3.ArithRef]],
) -> dict[str, Any]:
    return {
        "parameters": {
            "c": [scalar_text(model, value) for value in c],
            "d": [scalar_text(model, value) for value in d],
        },
        "F": [
            [scalar_text(model, value) for value in row]
            for row in matrix
        ],
    }


def clause_for(
    matrix: Sequence[Sequence[z3.ArithRef]],
    point: tuple[int, int, int],
    rows: Sequence[int],
) -> z3.BoolRef:
    """Build the guard clause ``Or(F_i lambda(point) <= 0)``."""

    return closure.clause_for_point(matrix, point, rows)


def validate_and_load() -> tuple[
    dict[str, Any],
    list[tuple[int, int, int]],
    list[tuple[int, int, int]],
    list[tuple[int, int, int]],
    dict[tuple[int, int, int], tuple[int, ...]],
]:
    certificate = json.loads(CERTIFICATE.read_text())
    closure_result = json.loads(CLOSURE_RESULT.read_text())

    if certificate.get("finite_guard_count") != 1456:
        raise AssertionError("observer certificate finite count changed")
    if certificate.get("pair_nontrivial_count") != EXPECTED_GUARDS:
        raise AssertionError("observer certificate pair count changed")
    if certificate.get("pair_tautological_count") != 972:
        raise AssertionError("observer certificate tautological count changed")

    old_points = sorted(
        point_tuple(point)
        for point in closure.BOX_POINTS
        if closure.simplify_clause(point)["classification"] == "retained"
    )
    if len(old_points) != EXPECTED_OLD_CLAUSES:
        raise AssertionError(f"expected 40 old clauses, got {len(old_points)}")

    basis_points = [
        point_tuple(point)
        for point in closure_result["lra_implications"]["irredundant_basis_points"]
    ]
    if len(basis_points) != EXPECTED_NEW_CLAUSES or len(set(basis_points)) != EXPECTED_NEW_CLAUSES:
        raise AssertionError("closure basis is not the reviewed eight-point basis")
    base_points = old_points + basis_points
    if len(set(base_points)) != EXPECTED_OLD_CLAUSES + EXPECTED_NEW_CLAUSES:
        raise AssertionError("old and closure basis clauses overlap unexpectedly")

    guard_rows: dict[tuple[int, int, int], tuple[int, ...]] = {}
    for record in certificate["guards"]:
        point = point_tuple(record["point"])
        if record.get("tautological", False):
            continue
        rows = tuple(int(row) for row in record["possible_blocking_rows"])
        if point in guard_rows or not rows:
            raise AssertionError(f"duplicate or empty observer guard {point}")
        profile = closure.simplify_clause(point)
        if profile["classification"] != "retained":
            raise AssertionError(f"observer guard is not retained under pair profile: {point}")
        if tuple(profile["possible_rows"]) != rows:
            raise AssertionError(f"observer and closure row profiles differ at {point}")
        guard_rows[point] = rows

    certificate_points = {
        point_tuple(point) for point in certificate["pair_nontrivial_points"]
    }
    if certificate_points != set(guard_rows) or len(guard_rows) != EXPECTED_GUARDS:
        raise AssertionError("certificate guard lists disagree")

    # Keep the certificate's order: it is deterministic and makes the greedy
    # pass reproducible.  The sorted list is used only for base provenance.
    ordered_guards = [
        point_tuple(point)
        for point in certificate["pair_nontrivial_points"]
    ]
    if len(ordered_guards) != len(set(ordered_guards)):
        raise AssertionError("observer guard order contains duplicates")
    return certificate, old_points, basis_points, ordered_guards, guard_rows


def query_guard(
    solver: z3.Solver,
    matrix: Sequence[Sequence[z3.ArithRef]],
    point: tuple[int, int, int],
    rows: Sequence[int],
    c: Sequence[z3.ArithRef],
    d: Sequence[z3.ArithRef],
    deadline: float,
) -> dict[str, Any]:
    """Check an implication by asserting the strict negation of its clause."""

    remaining = deadline - time.monotonic()
    if remaining <= 0:
        return {
            "status": "unknown",
            "reason": "global_wallcap",
            "elapsed_seconds": 0.0,
        }
    timeout_ms = max(1, min(PER_QUERY_TIMEOUT_MS, int(remaining * 1000)))
    candidate_negation = [
        closure.z3_slack(matrix, point, row) > 0
        for row in rows
    ]
    solver.set(timeout=timeout_ms)
    solver.push()
    started = time.monotonic()
    solver.add(*candidate_negation)
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
        reason = solver.reason_unknown()
        result["reason"] = reason or (
            "global_wallcap" if deadline - time.monotonic() <= 0 else "solver_unknown"
        )
    solver.pop()
    return result


def status_counts(records: Sequence[dict[str, Any]]) -> dict[str, int]:
    counts = Counter(record["status"] for record in records)
    return {key: counts[key] for key in ("unsat", "sat", "unknown") if counts[key]}


def main() -> None:
    started = time.monotonic()
    certificate, old_points, basis_points, ordered_guards, guard_rows = validate_and_load()

    c, d = column.column_parameters()
    matrix = column.column_matrix(c, d)
    domain = closure.pair_domain_constraints(matrix, c, d)
    profiles = {
        point: closure.simplify_clause(point)
        for point in [*old_points, *basis_points, *ordered_guards]
    }
    base_clauses = [
        clause_for(matrix, point, profiles[point]["possible_rows"])
        for point in [*old_points, *basis_points]
    ]
    solver = z3.Solver()
    solver.add(*domain, *base_clauses)

    deadline = started + GLOBAL_WALL_SECONDS
    phase1_records: list[dict[str, Any]] = []
    for point in ordered_guards:
        record = query_guard(
            solver, matrix, point, guard_rows[point], c, d, deadline
        )
        phase1_records.append({"point": list(point), **record})

    phase1_counts = status_counts(phase1_records)
    sat_phase1 = [
        point
        for point, record in zip(ordered_guards, phase1_records)
        if record["status"] == "sat"
    ]
    unknown_phase1 = [
        point
        for point, record in zip(ordered_guards, phase1_records)
        if record["status"] == "unknown"
    ]

    # Add each genuinely missing guard as soon as it remains SAT.  Guards
    # proved UNSAT in phase one stay implied under additional clauses, so only
    # SAT/UNKNOWN phase-one records need a second check.  This is a greedy
    # reduction of the finite list, not a claim that the selected set is
    # geometrically sufficient.
    greedy_records: list[dict[str, Any]] = []
    selected: list[tuple[int, int, int]] = []
    phase2_skipped = not sat_phase1 and not unknown_phase1
    if not phase2_skipped and deadline - time.monotonic() > 0:
        for point, phase1 in zip(ordered_guards, phase1_records):
            if phase1["status"] == "unsat":
                greedy_records.append(
                    {"point": list(point), "status": "inherited_unsat"}
                )
                continue
            record = query_guard(
                solver, matrix, point, guard_rows[point], c, d, deadline
            )
            greedy_records.append({"point": list(point), **record})
            if record["status"] == "sat":
                selected.append(point)
                solver.add(clause_for(matrix, point, guard_rows[point]))
    else:
        phase2_skipped = True

    phase2_counts = status_counts(
        [record for record in greedy_records if record["status"] != "inherited_unsat"]
    )
    selected_records = [list(point) for point in selected]
    result = {
        "status": "observer_guard_qf_lra_implications",
        "certificate": {
            "path": str(CERTIFICATE.relative_to(HERE)),
            "finite_guard_count": certificate["finite_guard_count"],
            "pair_nontrivial_count": certificate["pair_nontrivial_count"],
            "pair_tautological_count": certificate["pair_tautological_count"],
            "pair_signature_counts": {
                str(rows): count
                for rows, count in Counter(guard_rows.values()).items()
            },
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
        },
        "antecedent": {
            "domain": "strict off-diagonal positivity, pair dominance, column sums one, and D=sum(c)>2",
            "old_clause_count": len(old_points),
            "new_closure_basis_count": len(basis_points),
            "total_clause_count": len(base_clauses),
            "old_points": [list(point) for point in old_points],
            "new_closure_basis_points": [list(point) for point in basis_points],
        },
        "phase1_against_48_clauses": {
            "guard_count": len(phase1_records),
            "status_counts": phase1_counts,
            "exact_implication_count": phase1_counts.get("unsat", 0),
            "missing_guard_count": phase1_counts.get("sat", 0),
            "unknown_count": phase1_counts.get("unknown", 0),
            "records": phase1_records,
        },
        "greedy_phase2": {
            "ran": not phase2_skipped,
            "status_counts": phase2_counts,
            "selected_necessary_guard_count": len(selected),
            "selected_necessary_guards": selected_records,
            "records": greedy_records,
            "scope": "finite QF_LRA reduction only; selected guards do not establish hollowness or a global width bound",
        },
        "scope": {
            "observer_hypotheses": certificate["hypotheses"],
            "finite_guard_screen": "The 484 pair-nontrivial guards are tested under the 48-clause necessary relaxation.",
            "no_hollow_conclusion": True,
            "no_global_bound": True,
            "no_3_4_bound": True,
        },
        "elapsed_seconds": time.monotonic() - started,
    }
    JSON_OUT.write_text(json.dumps(result, indent=2) + "\n")
    print(
        json.dumps(
            {
                "status": result["status"],
                "phase1": phase1_counts,
                "phase2": phase2_counts,
                "selected": len(selected),
                "elapsed_seconds": result["elapsed_seconds"],
            }
        )
    )


if __name__ == "__main__":
    main()
