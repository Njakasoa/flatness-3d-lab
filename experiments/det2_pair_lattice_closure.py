"""Exact centralizer closure and LRA clause reduction for the pair chart.

The 216 integer points in [-2,3]^3 are closed under the eight affine lattice
maps induced by the permutations centralizing sigma=(01)(23) on
P=(0,(2,1,1),e2,e3).  This script computes that finite closure with Fraction
arithmetic, simplifies F*lambda(z)<=0 using strict off-diagonal positivity
and pair dominance, and checks clause implications in QF_LRA only.

It does not run an NRA solver, use floating point search, prove a global
bound, or claim sufficiency of any finite hollowness list.
"""

from __future__ import annotations

import hashlib
import itertools
import json
import time
from collections import Counter, defaultdict
from fractions import Fraction
from pathlib import Path
from typing import Any, Iterable, Sequence

import z3

try:
    from experiments import det2_pair_column_smt as column
except ModuleNotFoundError:  # Direct ``python experiments/...py`` invocation.
    import det2_pair_column_smt as column


HERE = Path(__file__).resolve().parents[1]
JSON_OUT = HERE / "results" / "det2_pair_lattice_closure.json"

CONTACTS: tuple[tuple[int, int, int], ...] = (
    (0, 0, 0),
    (2, 1, 1),
    (0, 1, 0),
    (0, 0, 1),
)
SIGMA = (1, 0, 3, 2)
BOX_POINTS = frozenset(itertools.product(range(-2, 4), repeat=3))
LRA_TIMEOUT_MS = 10_000


def determinant(matrix: Sequence[Sequence[Fraction]]) -> Fraction:
    """Exact determinant for any small square matrix."""

    n = len(matrix)
    if n == 1:
        return matrix[0][0]
    return sum(
        (Fraction(1) if j % 2 == 0 else Fraction(-1))
        * matrix[0][j]
        * determinant(
            [
                [matrix[i][k] for k in range(n) if k != j]
                for i in range(1, n)
            ]
        )
        for j in range(n)
    )


def inverse(matrix: Sequence[Sequence[Fraction]]) -> list[list[Fraction]]:
    """Exact Gauss-Jordan inverse."""

    n = len(matrix)
    work = [
        list(row) + [Fraction(int(i == j)) for j in range(n)]
        for i, row in enumerate(matrix)
    ]
    for col in range(n):
        pivot = next((i for i in range(col, n) if work[i][col]), None)
        if pivot is None:
            raise ValueError("singular affine frame")
        work[col], work[pivot] = work[pivot], work[col]
        scale = work[col][col]
        work[col] = [value / scale for value in work[col]]
        for i in range(n):
            if i == col:
                continue
            scale = work[i][col]
            work[i] = [x - scale * y for x, y in zip(work[i], work[col])]
    return [row[n:] for row in work]


def matrix_product(
    left: Sequence[Sequence[Fraction]], right: Sequence[Sequence[Fraction]]
) -> list[list[Fraction]]:
    return [
        [
            sum(left[i][k] * right[k][j] for k in range(len(right)))
            for j in range(len(right[0]))
        ]
        for i in range(len(left))
    ]


def affine_map_for_permutation(
    permutation: tuple[int, int, int, int]
) -> tuple[tuple[tuple[int, int, int], ...], tuple[int, int, int]]:
    """Return the unique affine map sending p_i to p_permutation[i]."""

    source_frame = [
        [
            Fraction(CONTACTS[j][i]) - Fraction(CONTACTS[0][i])
            for j in (1, 2, 3)
        ]
        for i in range(3)
    ]
    target = [CONTACTS[permutation[i]] for i in range(4)]
    target_frame = [
        [
            Fraction(target[j][i]) - Fraction(target[0][i])
            for j in (1, 2, 3)
        ]
        for i in range(3)
    ]
    linear = matrix_product(target_frame, inverse(source_frame))
    translation = tuple(
        Fraction(target[0][i])
        - sum(linear[i][j] * CONTACTS[0][j] for j in range(3))
        for i in range(3)
    )
    if any(value.denominator != 1 for row in linear for value in row):
        raise AssertionError("centralizer contact map was not integral")
    if any(value.denominator != 1 for value in translation):
        raise AssertionError("centralizer contact translation was not integral")
    integer_linear = tuple(
        tuple(int(value) for value in row) for row in linear
    )
    integer_translation = tuple(int(value) for value in translation)
    if abs(int(determinant([[Fraction(x) for x in row] for row in integer_linear]))) != 1:
        raise AssertionError("contact symmetry is not unimodular")
    return integer_linear, integer_translation


def apply_affine(
    linear: Sequence[Sequence[int]],
    translation: Sequence[int],
    point: Sequence[int],
) -> tuple[int, int, int]:
    return tuple(
        sum(linear[i][j] * point[j] for j in range(3)) + translation[i]
        for i in range(3)
    )


def centralizer_maps() -> list[dict[str, Any]]:
    permutations = [
        tuple(permutation)
        for permutation in itertools.permutations(range(4))
        if all(
            permutation[SIGMA[i]] == SIGMA[permutation[i]]
            for i in range(4)
        )
    ]
    if len(permutations) != 8:
        raise AssertionError(f"expected centralizer size 8, got {len(permutations)}")
    maps: list[dict[str, Any]] = []
    for permutation in permutations:
        linear, translation = affine_map_for_permutation(permutation)
        image = frozenset(
            apply_affine(linear, translation, point) for point in BOX_POINTS
        )
        if {apply_affine(linear, translation, point) for point in CONTACTS} != {
            CONTACTS[i] for i in permutation
        }:
            raise AssertionError("affine map does not map the contact set correctly")
        maps.append(
            {
                "permutation": list(permutation),
                "linear_matrix": [list(row) for row in linear],
                "translation": list(translation),
                "determinant": int(
                    determinant([[Fraction(x) for x in row] for row in linear])
                ),
                "image_points": image,
            }
        )
    return maps


def lambda_fraction(point: Sequence[int]) -> tuple[Fraction, ...]:
    x, y, z = (Fraction(value) for value in point)
    return (
        Fraction(1) + x / 2 - y - z,
        x / 2,
        y - x / 2,
        z - x / 2,
    )


def row_triangle_values(
    lambdas: Sequence[Fraction], row: int
) -> tuple[Fraction, Fraction, Fraction]:
    """Evaluate a normalized pair row at the three closed-triangle corners."""

    designated = SIGMA[row]
    first, second = [index for index in range(4) if index not in (row, designated)]
    return (
        lambdas[designated],
        (lambdas[designated] + lambdas[first]) / 2,
        (lambdas[designated] + lambdas[second]) / 2,
    )


def simplify_clause(point: tuple[int, int, int]) -> dict[str, Any]:
    """Classify a clause using strict positivity of the two non-designated entries.

    A positive row scale multiplies every row slack by a positive number, so
    the signs are those of the normalized closed triangle.  A row atom is
    possible in the strict domain when its triangle minimum is negative, or
    when both values on the admissible dominance edge ``a=1/2, b,c>0`` are
    zero.  A zero minimum attained only on an excluded edge is omitted, while
    a row with maximum <=0 makes the whole clause tautological.
    """

    lambdas = lambda_fraction(point)
    possible_rows: list[int] = []
    extrema: list[dict[str, str]] = []
    for row in range(4):
        values = row_triangle_values(lambdas, row)
        minimum, maximum = min(values), max(values)
        extrema.append(
            {
                "min": fraction_text(minimum),
                "max": fraction_text(maximum),
            }
        )
        if maximum <= 0:
            return {
                "point": list(point),
                "lambda": [fraction_text(value) for value in lambdas],
                "classification": "tautological",
                "possible_rows": [],
                "row_extrema": extrema,
            }
        if minimum < 0 or (values[1] == 0 and values[2] == 0):
            possible_rows.append(row)
    if not possible_rows:
        return {
            "point": list(point),
            "lambda": [fraction_text(value) for value in lambdas],
            "classification": "contradictory",
            "possible_rows": [],
            "row_extrema": extrema,
        }
    return {
        "point": list(point),
        "lambda": [fraction_text(value) for value in lambdas],
        "classification": "retained",
        "possible_rows": possible_rows,
        "row_extrema": extrema,
    }


def fraction_text(value: Fraction) -> str:
    return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"


def z3_fraction(value: Fraction) -> z3.ArithRef:
    return z3.RealVal(fraction_text(value))


def z3_slack(
    matrix: Sequence[Sequence[z3.ArithRef]],
    point: tuple[int, int, int],
    row: int,
) -> z3.ArithRef:
    return z3.simplify(
        sum(matrix[row][i] * z3_fraction(value) for i, value in enumerate(lambda_fraction(point))),
        som=True,
    )


def pair_domain_constraints(
    matrix: Sequence[Sequence[z3.ArithRef]],
    c: Sequence[z3.ArithRef],
    d: Sequence[z3.ArithRef],
) -> list[z3.BoolRef]:
    """Exact strict positivity, pair dominance, and nonsingularity domain."""

    constraints: list[z3.BoolRef] = []
    for j in range(4):
        constraints.extend((c[j] > 0, d[j] > 0, 1 - c[j] - d[j] > 0))
    for i in range(4):
        designated = SIGMA[i]
        constraints.append(
            matrix[i][designated]
            >= sum(matrix[i][j] for j in range(4) if j not in (i, designated))
        )
    constraints.append(sum(c) > 2)
    return constraints


def clause_for_point(
    matrix: Sequence[Sequence[z3.ArithRef]],
    point: tuple[int, int, int],
    rows: Sequence[int],
) -> z3.BoolRef:
    return z3.Or(*(z3_slack(matrix, point, row) <= 0 for row in rows))


def model_parameters(
    model: z3.ModelRef,
    c: Sequence[z3.ArithRef],
    d: Sequence[z3.ArithRef],
) -> dict[str, list[str]]:
    return {
        "c": [z3.simplify(model.eval(value, model_completion=True)).sexpr() for value in c],
        "d": [z3.simplify(model.eval(value, model_completion=True)).sexpr() for value in d],
    }


def implication_check(
    domain: Sequence[z3.BoolRef],
    antecedent_clauses: Sequence[z3.BoolRef],
    candidate_clause: z3.BoolRef,
    candidate_rows: Sequence[int],
    matrix: Sequence[Sequence[z3.ArithRef]],
    point: tuple[int, int, int],
    c: Sequence[z3.ArithRef],
    d: Sequence[z3.ArithRef],
) -> dict[str, Any]:
    """Check antecedent => candidate by adding the exact clause negation."""

    solver = z3.Solver()
    solver.set(timeout=LRA_TIMEOUT_MS)
    solver.add(*domain, *antecedent_clauses)
    solver.add(*(z3_slack(matrix, point, row) > 0 for row in candidate_rows))
    status = solver.check()
    result: dict[str, Any] = {"status": str(status)}
    if status == z3.sat:
        result["witness_parameters"] = model_parameters(solver.model(), c, d)
    elif status == z3.unknown:
        result["reason_unknown"] = solver.reason_unknown()
    return result


def point_list(items: Iterable[tuple[int, int, int]]) -> list[list[int]]:
    return [list(point) for point in sorted(items)]


def main() -> None:
    started = time.monotonic()
    maps = centralizer_maps()
    closure = frozenset().union(*(entry["image_points"] for entry in maps))
    if len(BOX_POINTS) != 216 or len(closure) != 432:
        raise AssertionError(f"unexpected box/closure sizes: {len(BOX_POINTS)}, {len(closure)}")
    if any(
        apply_affine(entry["linear_matrix"], entry["translation"], point) not in closure
        for entry in maps
        for point in closure
    ):
        raise AssertionError("one-step centralizer image did not close the union")

    image_groups: dict[frozenset[tuple[int, int, int]], list[int]] = defaultdict(list)
    for index, entry in enumerate(maps):
        image_groups[entry["image_points"]].append(index)

    hidden_points = [(-3, 1, -1), (-3, -1, 1)]
    hidden_membership = {}
    for point in hidden_points:
        preimages = []
        for index, entry in enumerate(maps):
            for source in BOX_POINTS:
                if apply_affine(entry["linear_matrix"], entry["translation"], source) == point:
                    preimages.append({"map_index": index, "source": list(source)})
        hidden_membership[str(list(point))] = {
            "in_closure": point in closure,
            "preimages": preimages,
        }

    profiles = {point: simplify_clause(point) for point in closure}
    contradictory = [
        point for point, profile in profiles.items() if profile["classification"] == "contradictory"
    ]
    if contradictory:
        raise AssertionError(f"unexpected contradictory clauses: {contradictory[:3]}")
    original_retained = sorted(
        point for point in BOX_POINTS if profiles[point]["classification"] == "retained"
    )
    new_points = closure - BOX_POINTS
    new_retained = sorted(
        point for point in new_points if profiles[point]["classification"] == "retained"
    )
    new_tautological = sorted(
        point for point in new_points if profiles[point]["classification"] == "tautological"
    )
    if len(original_retained) != 40 or len(new_retained) != 68 or len(new_tautological) != 148:
        raise AssertionError(
            f"unexpected profiles: {len(original_retained)}, {len(new_retained)}, {len(new_tautological)}"
        )

    # Build exact QF_LRA clauses in the same column chart used by the model.
    c, d = column.column_parameters()
    matrix = column.column_matrix(c, d)
    domain = pair_domain_constraints(matrix, c, d)
    old_clauses = [
        clause_for_point(matrix, point, profiles[point]["possible_rows"])
        for point in original_retained
    ]
    clause_map = {
        point: clause_for_point(matrix, point, profiles[point]["possible_rows"])
        for point in new_retained
    }

    implication_results: dict[str, dict[str, Any]] = {}
    implication_counts = Counter()
    for point in new_retained:
        outcome = implication_check(
            domain,
            old_clauses,
            clause_map[point],
            profiles[point]["possible_rows"],
            matrix,
            point,
            c,
            d,
        )
        implication_results[str(list(point))] = outcome
        implication_counts[outcome["status"]] += 1
    not_implied = [
        point
        for point in new_retained
        if implication_results[str(list(point))]["status"] != "unsat"
    ]
    if implication_counts["unknown"]:
        raise RuntimeError("an original-clause implication check timed out")

    # Determine which of the individually new clauses are redundant once the
    # other individually new clauses are available.  This is still QF_LRA.
    relative_results: dict[str, dict[str, Any]] = {}
    for point in not_implied:
        other_new = [clause_map[other] for other in not_implied if other != point]
        outcome = implication_check(
            domain,
            [*old_clauses, *other_new],
            clause_map[point],
            profiles[point]["possible_rows"],
            matrix,
            point,
            c,
            d,
        )
        relative_results[str(list(point))] = outcome
    irredundant_basis = [
        point
        for point in not_implied
        if relative_results[str(list(point))]["status"] != "unsat"
    ]
    if any(
        relative_results[str(list(point))]["status"] == "unknown"
        for point in not_implied
    ):
        raise RuntimeError("a relative implication check timed out")

    # Verify that the eight-clause basis implies every new retained clause,
    # and that no basis member is implied by the other seven.
    basis_clauses = [clause_map[point] for point in irredundant_basis]
    coverage_results: dict[str, dict[str, Any]] = {}
    for point in new_retained:
        outcome = implication_check(
            domain,
            [*old_clauses, *basis_clauses],
            clause_map[point],
            profiles[point]["possible_rows"],
            matrix,
            point,
            c,
            d,
        )
        coverage_results[str(list(point))] = outcome
    if any(value["status"] != "unsat" for value in coverage_results.values()):
        raise AssertionError("the reported irredundant basis did not cover every new clause")
    basis_minimality: dict[str, dict[str, Any]] = {}
    for point in irredundant_basis:
        other_basis = [clause_map[other] for other in irredundant_basis if other != point]
        outcome = implication_check(
            domain,
            [*old_clauses, *other_basis],
            clause_map[point],
            profiles[point]["possible_rows"],
            matrix,
            point,
            c,
            d,
        )
        basis_minimality[str(list(point))] = outcome
    if any(value["status"] != "sat" for value in basis_minimality.values()):
        raise AssertionError("reported basis is not irredundant")

    image_records = []
    for index, entry in enumerate(maps):
        image = entry["image_points"]
        image_records.append(
            {
                "map_index": index,
                "permutation": entry["permutation"],
                "linear_matrix": entry["linear_matrix"],
                "translation": entry["translation"],
                "determinant": entry["determinant"],
                "image_point_count": len(image),
                "image_bounds": [
                    [min(point[axis] for point in image), max(point[axis] for point in image)]
                    for axis in range(3)
                ],
                "overlap_with_original": len(image & BOX_POINTS),
                "distinct_image_group": next(
                    group_index
                    for group_index, group in enumerate(image_groups.values())
                    if index in group
                ),
            }
        )

    all_points_serialized = [list(point) for point in sorted(closure)]
    closure_hash = hashlib.sha256(
        json.dumps(all_points_serialized, separators=(",", ":")).encode()
    ).hexdigest()
    result: dict[str, Any] = {
        "status": "exact_centralizer_lattice_closure_and_lra_clause_reduction",
        "contacts": [list(point) for point in CONTACTS],
        "sigma": list(SIGMA),
        "centralizer": {
            "permutation_convention": "permutation[i] sends contact p_i to p_permutation[i]",
            "size": len(maps),
            "maps": image_records,
            "distinct_image_count": len(image_groups),
            "group_closure_verified": True,
        },
        "box": {
            "lo": [-2, -2, -2],
            "hi": [3, 3, 3],
            "point_count": len(BOX_POINTS),
        },
        "closure": {
            "point_count": len(closure),
            "new_point_count": len(new_points),
            "coordinate_bounds": [
                [min(point[axis] for point in closure), max(point[axis] for point in closure)]
                for axis in range(3)
            ],
            "sha256_sorted_points": closure_hash,
            "points": all_points_serialized,
        },
        "hidden_points": hidden_membership,
        "clause_simplification": {
            "positive_row_scaling": "F_i lambda(z)=(sum_j F_ij)*(normalized_pair_row_i lambda(z)); row sums are strictly positive",
            "strict_domain": "all off-diagonal F entries >0, pair dominance F_i,sigma(i)>=sum of the other two off-diagonal entries, and D=sum_j c_j>2",
            "triangle_rule": "row atom is possible iff the triangle minimum is negative or both admissible dominance-edge values are zero; maximum <=0 makes the whole clause tautological",
            "original_box": {
                "tautological_count": sum(
                    profiles[point]["classification"] == "tautological" for point in BOX_POINTS
                ),
                "retained_count": len(original_retained),
                "row_signature_counts": {
                    str(rows): count
                    for rows, count in Counter(
                        tuple(profiles[point]["possible_rows"])
                        for point in original_retained
                    ).items()
                },
            },
            "closure": {
                "tautological_count": sum(
                    profiles[point]["classification"] == "tautological" for point in closure
                ),
                "retained_count": len(original_retained) + len(new_retained),
                "new_tautological_count": len(new_tautological),
                "new_retained_count": len(new_retained),
                "row_signature_counts": {
                    str(rows): count
                    for rows, count in Counter(
                        tuple(profiles[point]["possible_rows"])
                        for point in closure
                        if profiles[point]["classification"] == "retained"
                    ).items()
                },
            },
            "new_retained_points": point_list(new_retained),
            "new_tautological_points": point_list(new_tautological),
        },
        "lra_implications": {
            "solver": "z3 QF_LRA",
            "timeout_ms_per_check": LRA_TIMEOUT_MS,
            "antecedent": "strict pair domain plus the 40 retained original-box clauses",
            "new_retained_count": len(new_retained),
            "implied_by_original_count": implication_counts["unsat"],
            "not_implied_by_original_count": len(not_implied),
            "unknown_count": implication_counts["unknown"],
            "not_implied_points": point_list(not_implied),
            "implication_results": implication_results,
            "relative_to_other_new": relative_results,
            "irredundant_basis_count": len(irredundant_basis),
            "irredundant_basis_points": point_list(irredundant_basis),
            "basis_coverage_verified": True,
            "basis_minimality": basis_minimality,
            "coverage_results": coverage_results,
            "interpretation": "56 of 68 added non-tautological clauses follow from the original 40; 12 are individually new, and 8 form an irredundant basis once those 12 are jointly available.",
        },
        "scope": {
            "closure_use": "The 432-point set is an exact finite equivariant enlargement of the [-2,3]^3 screen.",
            "no_global_bound": "No global lattice bound is claimed.",
            "no_sufficiency": "The finite clauses remain a necessary hollowness screen only; no sufficiency claim is made.",
        },
        "elapsed_seconds": time.monotonic() - started,
    }
    JSON_OUT.write_text(json.dumps(result, indent=2) + "\n")
    print(
        json.dumps(
            {
                "status": result["status"],
                "centralizer_maps": len(maps),
                "distinct_images": len(image_groups),
                "box_points": len(BOX_POINTS),
                "closure_points": len(closure),
                "hidden_points_in_closure": all(
                    value["in_closure"] for value in hidden_membership.values()
                ),
                "new_retained": len(new_retained),
                "implied_by_original": implication_counts["unsat"],
                "not_implied": len(not_implied),
                "irredundant_basis": len(irredundant_basis),
                "json": str(JSON_OUT),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
