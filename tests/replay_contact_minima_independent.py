#!/usr/bin/env python3
"""Independent exact replay of the contact-reduction certificates.

This file deliberately uses only the standard library.  It does not import
the lab geometry, enumeration, or exact-arithmetic modules.  The default run
checks the historical 37-class certificate, all 51 tetrahedron certificates,
all 52 nonsimplicial hulls, and all 63 embeddings into nine templates. It also
rejects deliberate certificate mutations. Exhaustive enumeration completeness
is supplied separately by the generator proof and adversarial review.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import itertools
import math
import sys
from fractions import Fraction
from pathlib import Path


ALPHA_LO = Fraction("0.368902823735021962")
ALPHA_HI = Fraction("0.368902823735022342")


def ceil_div(a: int, b: int) -> int:
    return -((-a) // b)


def gauge(q: tuple[Fraction, Fraction, Fraction]) -> Fraction:
    positive = sum((x for x in q if x > 0), Fraction(0))
    negative = sum((-x for x in q if x < 0), Fraction(0))
    return max(positive, negative)


def rank(vectors: list[tuple[Fraction, Fraction, Fraction]]) -> int:
    """Exact row rank over Q, for the successive-minimum replay."""

    rows = [list(v) for v in vectors]
    result = 0
    for column in range(3):
        pivot = next(
            (i for i in range(result, len(rows)) if rows[i][column]), None
        )
        if pivot is None:
            continue
        rows[result], rows[pivot] = rows[pivot], rows[result]
        scale = rows[result][column]
        rows[result] = [x / scale for x in rows[result]]
        for i in range(len(rows)):
            if i == result or not rows[i][column]:
                continue
            factor = rows[i][column]
            rows[i] = [rows[i][j] - factor * rows[result][j] for j in range(3)]
        result += 1
    return result


def residue_minimum(n: int, a: int) -> tuple[Fraction, list[int]]:
    if n == 1:
        return Fraction(1), []
    values = []
    for k in range(1, n):
        ak = (a * k) % n
        values.append((min(k, n - k) + min(ak, n - ak), k))
    numerator = min(value for value, _ in values)
    return Fraction(numerator, n), [k for value, k in values if value == numerator]


def bounded_vectors(
    n: int, a: int, m: int
) -> list[tuple[Fraction, tuple[int, int, int]]]:
    """List all nonzero q=B^-1 z with gamma(q)<=m/n.

    The integer inequalities are the certificate's box, so no floating point
    cutoff or guessed coordinate range is used.
    """

    result = []
    for x in range(-m, m + 1):
        y_lo = ceil_div(x - m, n)
        y_hi = (x + m) // n
        z_lo = ceil_div(a * x - m, n)
        z_hi = (a * x + m) // n
        for y in range(y_lo, y_hi + 1):
            for z in range(z_lo, z_hi + 1):
                q = (
                    Fraction(x, n),
                    Fraction(n * y - x, n),
                    Fraction(n * z - a * x, n),
                )
                if any(q) and gauge(q) <= Fraction(m, n):
                    result.append((q, (x, y, z)))
    return result


def all_vectors_at_most_one(n: int, a: int):
    # The m=n box is complete because gamma(q)<=1 implies |q_i|<=1.
    return bounded_vectors(n, a, n)


def class_parameters(item: dict) -> tuple[int, int]:
    vertices = item["vertices"]
    n = int(vertices[1][0])
    if n == 1:
        return n, 0
    assert vertices[1][1] == 1
    assert vertices[2] == [0, 1, 0]
    assert vertices[3] == [0, 0, 1]
    return n, int(vertices[1][2])


def replay_certificate(repo: Path) -> None:
    source_path = repo / "results" / "empty_contact_tetrahedra.json"
    result_path = repo / "results" / "contact_minima_independent.json"
    source = json.loads(source_path.read_text())
    result = json.loads(result_path.read_text())
    assert len(source["classes"]) == 37
    assert len(result["classes"]) == 37

    for source_item, certificate in zip(source["classes"], result["classes"]):
        n, a = class_parameters(source_item)
        assert certificate["D"] == n
        assert certificate["a"] == a
        ell, k_minimizers = residue_minimum(n, a)
        assert certificate["ell"] == str(ell)
        assert certificate["k_minimizers"] == k_minimizers

        if n == 1:
            m = 1
        else:
            m = ell.numerator * n // ell.denominator
        at_ell = bounded_vectors(n, a, m)
        assert len(at_ell) == certificate["certificate"]["vectors_with_gamma_le_ell"]
        assert min(gauge(q) for q, _ in at_ell) == ell
        assert rank([q for q, _ in at_ell]) == certificate["certificate"]["rank_at_ell"]

        # The N=1 White representative in this historical certificate uses
        # the normalized shear B=[[N,0,0],[1,1,0],[a,0,1]], even though its
        # stored HNF representative is the identity simplex.  Check every
        # stored z/q witness through that same B, rather than silently
        # accepting a witness whose coordinate convention is ambiguous.
        by_z_at_ell = {z: q for q, z in at_ell}
        witness_z = tuple(certificate["witness_z"])
        assert witness_z in by_z_at_ell
        assert [fraction_string(x) for x in by_z_at_ell[witness_z]] == certificate["witness_q"]
        assert gauge(by_z_at_ell[witness_z]) == ell

        at_one = all_vectors_at_most_one(n, a)
        values = sorted({gauge(q) for q, _ in at_one})
        lambda2 = next(
            value for value in values if rank([q for q, _ in at_one if gauge(q) <= value]) >= 2
        )
        lambda3 = next(
            value for value in values if rank([q for q, _ in at_one if gauge(q) <= value]) >= 3
        )
        assert certificate["lambda2"] == str(lambda2)
        assert certificate["lambda3"] == str(lambda3)
        by_z_at_one = {z: q for q, z in at_one}
        lambda2_z = tuple(certificate["lambda2_witness_z"])
        assert lambda2_z in by_z_at_one
        assert gauge(by_z_at_one[lambda2_z]) == lambda2

        if ell < ALPHA_LO:
            assert certificate["alpha_relation"] == "<"
        elif ell > ALPHA_HI:
            assert certificate["alpha_relation"] == ">"
        else:
            raise AssertionError(f"alpha interval overlaps class {certificate['id']}")
        assert certificate["gt_one_third"] is (ell > Fraction(1, 3))
        assert certificate["gt_four_eleventh"] is (ell > Fraction(4, 11))

        if n > 1:
            # m/n <= sqrt(2/n) is equivalent to m^2 <= 2n.
            assert m * m <= 2 * n

    assert result["summary"]["alpha_survivor_ids"] == [0, 1, 2, 3, 4, 5, 8, 10, 14, 23]
    assert result["summary"]["one_third_survivor_ids"] == [0, 1, 2, 3, 4, 5, 8, 10, 14, 17, 23]
    assert result["summary"]["four_eleventh_survivor_ids"] == [0, 1, 2, 3, 4, 5, 8, 10, 14, 23]


def replay_source21(repo: Path, path: Path) -> None:
    source = json.loads(path.read_text())
    assert len(source["classes"]) == 51
    assert source["counts"]["unlabeled_gl3z_classes"] == 51

    alpha_survivors = []
    one_third_survivors = []
    four_eleventh_survivors = []
    for index, item in enumerate(source["classes"]):
        n, a = class_parameters(item)
        ell, _ = residue_minimum(n, a)
        # The exact box replay also checks the full lattice minimization for
        # all determinant-21 classes, including those beyond the certificate.
        m = 1 if n == 1 else ell.numerator * n // ell.denominator
        at_ell = bounded_vectors(n, a, m)
        assert min(gauge(q) for q, _ in at_ell) == ell
        if ell < ALPHA_LO:
            pass
        elif ell > ALPHA_HI:
            alpha_survivors.append(index)
        else:
            raise AssertionError(f"alpha interval overlaps source21 class {index}")
        if ell > Fraction(1, 3):
            one_third_survivors.append(index)
        if ell > Fraction(4, 11):
            four_eleventh_survivors.append(index)
        if n > 1:
            assert m * m <= 2 * n

    assert alpha_survivors == [0, 1, 2, 3, 4, 5, 8, 10, 14, 23]
    assert one_third_survivors == [0, 1, 2, 3, 4, 5, 8, 10, 14, 17, 23]
    assert four_eleventh_survivors == [0, 1, 2, 3, 4, 5, 8, 10, 14, 23]
    print(f"source21 exact replay: {len(source['classes'])} classes; formula and box checks passed")


def replay_minima_main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--source21",
        type=Path,
        default=None,
        help="optional determinant-21 enumeration; defaults to results/empty_tetrahedra_through_21.json",
    )
    args = parser.parse_args()
    repo = Path(__file__).resolve().parents[1]
    replay_certificate(repo)
    print("source17 certificate replay: 37 classes; formula, box, rank, and threshold checks passed")
    source21 = args.source21 or (repo / "results" / "empty_tetrahedra_through_21.json")
    if source21.exists():
        replay_source21(repo, source21)


class ValidationError(AssertionError):
    """Raised when a generated certificate is incomplete or inconsistent."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValidationError(message)


def fraction_string(value: Fraction) -> str:
    return str(value.numerator) if value.denominator == 1 else str(value)


def det3(matrix: tuple[tuple[int, int, int], ...]) -> int:
    return (
        matrix[0][0] * (matrix[1][1] * matrix[2][2] - matrix[1][2] * matrix[2][1])
        - matrix[0][1] * (matrix[1][0] * matrix[2][2] - matrix[1][2] * matrix[2][0])
        + matrix[0][2] * (matrix[1][0] * matrix[2][1] - matrix[1][1] * matrix[2][0])
    )


def adj3(matrix: tuple[tuple[int, int, int], ...]) -> tuple[tuple[int, int, int], ...]:
    a = matrix
    return (
        (
            a[1][1] * a[2][2] - a[1][2] * a[2][1],
            a[0][2] * a[2][1] - a[0][1] * a[2][2],
            a[0][1] * a[1][2] - a[0][2] * a[1][1],
        ),
        (
            a[1][2] * a[2][0] - a[1][0] * a[2][2],
            a[0][0] * a[2][2] - a[0][2] * a[2][0],
            a[0][2] * a[1][0] - a[0][0] * a[1][2],
        ),
        (
            a[1][0] * a[2][1] - a[1][1] * a[2][0],
            a[0][1] * a[2][0] - a[0][0] * a[2][1],
            a[0][0] * a[1][1] - a[0][1] * a[1][0],
        ),
    )


def dot3(a: tuple[int, int, int], b: tuple[int, int, int]) -> int:
    return sum(x * y for x, y in zip(a, b))


def sub3(a: tuple[int, int, int], b: tuple[int, int, int]) -> tuple[int, int, int]:
    return tuple(x - y for x, y in zip(a, b))


def matrix_from_frame(frame: tuple[tuple[int, int, int], ...]) -> tuple[tuple[int, int, int], ...]:
    anchor = frame[0]
    columns = [sub3(p, anchor) for p in frame[1:]]
    return tuple(tuple(columns[j][i] for j in range(3)) for i in range(3))


SEARCH_REASON = (
    "An integer edge gives lambda1<=1. Any vector with gauge<=1 lies in P-P and hence "
    "this coordinate box. Gauge=sum positive affine difference barycentrics. "
    "Nonprimitive vectors cannot improve the minimum."
)


def primitive_vector(z: tuple[int, int, int]) -> bool:
    if not any(z) or next(x for x in z if x) < 0:
        return False
    return math.gcd(*z) == 1


def simplex_minimum_certificate(vertices: list[list[int]]) -> dict:
    """Recompute the full 3D P-P minimum with exact integer/rational arithmetic."""

    points = [tuple(int(x) for x in p) for p in vertices]
    require(len(points) == 4 and len(set(points)) == 4, "tetrahedron vertex set invalid")
    base = points[0]
    matrix = matrix_from_frame(tuple(points))
    determinant = det3(matrix)
    require(determinant != 0, "degenerate tetrahedron")
    absolute_determinant = abs(determinant)
    inverse_numerator = adj3(matrix)
    bounds = [
        max(p[j] for p in points) - min(p[j] for p in points) for j in range(3)
    ]
    minimum = Fraction(1)
    active: list[tuple[tuple[int, int, int], tuple[Fraction, ...]]] = []
    checked = 0
    for z in itertools.product(*(range(-b, b + 1) for b in bounds)):
        vector = tuple(int(x) for x in z)
        if not primitive_vector(vector):
            continue
        checked += 1
        q = tuple(
            Fraction(sum(inverse_numerator[i][j] * vector[j] for j in range(3)), determinant)
            for i in range(3)
        )
        barycentric = (-sum(q, Fraction(0)), *q)
        value = sum((x for x in barycentric if x > 0), Fraction(0))
        if value < minimum:
            minimum = value
            active = [(vector, barycentric)]
        elif value == minimum:
            active.append((vector, barycentric))
    require(active and 0 < minimum <= 1, "minimum search produced no witness")
    first_vector, first_barycentric = active[0]
    return {
        "normalized_determinant": absolute_determinant,
        "lambda1": fraction_string(minimum),
        "primitive_minimizers_mod_sign": [list(z) for z, _ in active],
        "upper_witness": {
            "lattice_vector": list(first_vector),
            "difference_barycentrics": [fraction_string(x) for x in first_barycentric],
            "positive_sum": fraction_string(minimum),
        },
        "complete_search": {
            "difference_coordinate_bounds": bounds,
            "primitive_vectors_checked": checked,
            "reason": SEARCH_REASON,
        },
    }


def expected_hnf(vertices: list[list[int]]) -> list[list[int]]:
    points = [tuple(p) for p in vertices]
    determinant = abs(det3(matrix_from_frame(tuple(points))))
    if determinant == 1:
        return [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
    require(points[0] == (0, 0, 0), "nonstandard source anchor")
    require(points[2] == (0, 1, 0) and points[3] == (0, 0, 1), "nonstandard HNF columns")
    require(points[1][1] == 1, "nonstandard White representative")
    return [[determinant, 0, 0], [1, 1, 0], [points[1][2], 0, 1]]


def radical_bound(ell: Fraction) -> dict | None:
    if ell == 1:
        return None
    denominator = 1 - ell
    return {
        "a": fraction_string(Fraction(1, 1) / denominator),
        "b": fraction_string(Fraction(2, 3) / denominator),
        "d": 3,
    }


def radical_value(bound: dict) -> float:
    return float(Fraction(bound["a"])) + float(Fraction(bound["b"])) * math.sqrt(3.0)


def below_candidate_bound(bound: dict | None) -> bool:
    if bound is None:
        return False
    lo2 = Fraction(1414213562373095, 10**15)
    hi2 = Fraction(1414213562373096, 10**15)
    lo3 = Fraction(1732050807568877, 10**15)
    hi3 = Fraction(1732050807568878, 10**15)
    require(lo2 * lo2 < 2 < hi2 * hi2, "sqrt(2) interval constants are invalid")
    require(lo3 * lo3 < 3 < hi3 * hi3, "sqrt(3) interval constants are invalid")
    a = Fraction(bound["a"])
    b = Fraction(bound["b"])
    upper_hi = a + b * hi3
    lower_target = 2 + lo2
    if upper_hi < lower_target:
        return True
    if a + b * lo3 > 2 + hi2:
        return False
    raise ValidationError("radical comparison interval is not separated")


def main_certificate_expected_summary(certificate: dict, source: dict) -> dict:
    expected_keys = {
        "status",
        "source",
        "threshold",
        "finite_reduction",
        "classes_checked",
        "survivors_lower_threshold",
        "survivors_candidate_threshold",
        "intermediate_threshold",
        "survivors_intermediate_threshold",
        "sharper_determinant_bound",
        "surviving_lower_hnfs",
        "surviving_candidate_hnfs",
        "cases",
    }
    require(set(certificate) == expected_keys, "main certificate metadata keys changed")
    require(certificate["status"] == "exact_computational_reduction_pending_novelty_review", "main status changed")
    require(
        certificate["source"]
        == "ACMS Lemma5.1 and Minkowski2 + empty tetrahedron width1 + exact HNF enumeration",
        "main source description changed",
    )
    require(certificate["threshold"] == {"a": "3/2", "b": "1", "d": 3}, "main threshold changed")
    require(
        certificate["intermediate_threshold"] == {"a": "11/7", "b": "22/21", "d": 3},
        "intermediate threshold changed",
    )
    require(
        certificate["finite_reduction"]
        == "w>3A/2 implies lambda1(K-K)>1/3; for empty P subset K: N=6vol(P)<=12/(5 lambda1(P-P)^2)<108/5, hence N<=21.",
        "finite reduction text changed",
    )
    require(
        certificate["sharper_determinant_bound"]
        == "The width-one section diamond has area 2N. Planar Minkowski gives N*lambda1(P-P)^2<=2. Thus w>3A/2 implies N<=17; w>11A/7 implies N<=15; w>=2+sqrt2 implies N<=14.",
        "sharper determinant text changed",
    )
    require(certificate["classes_checked"] == 51, "main class count changed")
    require(len(source["classes"]) == 51, "source21 class count changed")
    cases = certificate["cases"]
    require(len(cases) == 51, "main cases list length changed")
    require([c.get("index") for c in cases] == list(range(51)), "main case indices are not complete")

    lower_ids = []
    intermediate_ids = []
    candidate_ids = []
    lower_hnfs = []
    candidate_hnfs = []
    for index, (source_item, case) in enumerate(zip(source["classes"], cases)):
        require(case["index"] == index, f"case index mismatch at {index}")
        source_vertices = source_item["vertices"]
        require(case["vertices"] == source_vertices, f"case vertices mismatch at {index}")
        require(case["hnf"] == source_item["hnf"], f"case HNF mismatch at {index}")
        require(case["hnf"] == expected_hnf(source_vertices), f"forged HNF at {index}")

        n, a = class_parameters(source_item)
        ell, _ = residue_minimum(n, a)
        expected_minimum = simplex_minimum_certificate(source_vertices)
        require(case["minimum_certificate"] == expected_minimum, f"minimum certificate mismatch at {index}")
        require(case["minimum_certificate"]["lambda1"] == str(ell), f"lambda1 formula mismatch at {index}")

        bound = radical_bound(ell)
        require(case["width_upper"] == bound, f"Q(sqrt(3)) width bound mismatch at {index}")
        expected_decimal = None if bound is None else radical_value(bound)
        if expected_decimal is None:
            require(case["width_upper_decimal_display"] is None, f"unexpected decimal width at {index}")
        else:
            require(case["width_upper_decimal_display"] == expected_decimal, f"decimal width mismatch at {index}")

        lower = ell > Fraction(1, 3)
        intermediate = ell > Fraction(4, 11)
        candidate = bound is None or not below_candidate_bound(bound)
        require(case["survives_threshold_3A_over_2"] is lower, f"lower threshold flag mismatch at {index}")
        require(case["survives_threshold_11A_over_7"] is intermediate, f"intermediate flag mismatch at {index}")
        require(case["survives_candidate_threshold"] is candidate, f"candidate flag mismatch at {index}")
        if lower:
            lower_ids.append(index)
            lower_hnfs.append(case["hnf"])
        if intermediate:
            intermediate_ids.append(index)
        if candidate:
            candidate_ids.append(index)
            candidate_hnfs.append(case["hnf"])

    require(lower_ids == [0, 1, 2, 3, 4, 5, 8, 10, 14, 17, 23], "lower survivor set changed")
    require(intermediate_ids == [0, 1, 2, 3, 4, 5, 8, 10, 14, 23], "intermediate survivor set changed")
    require(candidate_ids == [0, 1, 2, 3, 4, 5, 8, 10, 14, 23], "candidate survivor set changed")
    require(certificate["survivors_lower_threshold"] == len(lower_ids), "lower survivor count changed")
    require(certificate["survivors_intermediate_threshold"] == len(intermediate_ids), "intermediate survivor count changed")
    require(certificate["survivors_candidate_threshold"] == len(candidate_ids), "candidate survivor count changed")
    require(certificate["surviving_lower_hnfs"] == lower_hnfs, "lower HNF survivor list changed")
    require(certificate["surviving_candidate_hnfs"] == candidate_hnfs, "candidate HNF survivor list changed")

    return {
        "classes_checked": len(cases),
        "survivor_ids": {
            "lower_threshold": lower_ids,
            "intermediate_threshold": intermediate_ids,
            "candidate_threshold": candidate_ids,
        },
        "metadata_checked": True,
        "all_hnfs_checked": True,
        "all_minimum_certificates_checked": True,
        "all_radical_width_bounds_checked": True,
    }


def cross2(o: tuple[int, int], a: tuple[int, int], b: tuple[int, int]) -> int:
    return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])


def convex_hull2(points: list[tuple[int, int]]) -> list[tuple[int, int]]:
    ordered = sorted(set(points))
    # A width-one 3-polytope may have a two-point segment in one layer.  Keep
    # that segment as its exact one-dimensional hull; the bounding-box scan in
    # validate_empty_hull still tests every lattice point on it.
    require(len(ordered) >= 2, "layer section is zero-dimensional")
    if len(ordered) == 2:
        return ordered
    lower: list[tuple[int, int]] = []
    for point in ordered:
        while len(lower) >= 2 and cross2(lower[-2], lower[-1], point) <= 0:
            lower.pop()
        lower.append(point)
    upper: list[tuple[int, int]] = []
    for point in reversed(ordered):
        while len(upper) >= 2 and cross2(upper[-2], upper[-1], point) <= 0:
            upper.pop()
        upper.append(point)
    hull = lower[:-1] + upper[:-1]
    require(len(hull) >= 3, "degenerate layer section")
    return hull


def point_in_convex_polygon(point: tuple[int, int], polygon: list[tuple[int, int]]) -> bool:
    signs = [cross2(polygon[i], polygon[(i + 1) % len(polygon)], point) for i in range(len(polygon))]
    return min(signs) >= 0 or max(signs) <= 0


def layer_data(
    vertices: list[list[int]], height: list[int]
) -> tuple[list[tuple[int, int]], list[tuple[int, int]], int, list[int]]:
    points = [tuple(int(x) for x in p) for p in vertices]
    h = tuple(int(x) for x in height)
    require(len(h) == 3 and sum(abs(x) for x in h) == 1, "height direction is not primitive unit")
    pivot = h.index(1) if 1 in h else None
    require(pivot is not None, "height direction must be nonnegative unit")
    keep = [j for j in range(3) if j != pivot]
    values = [dot3(h, p) for p in points]
    require(set(values) == {0, 1}, "vertices do not occupy exactly two unit layers")
    layers = [
        [(p[keep[0]], p[keep[1]]) for p, value in zip(points, values) if value == level]
        for level in (0, 1)
    ]
    require(all(len(layer) >= 2 for layer in layers), "a layer has too few vertices")
    return layers[0], layers[1], pivot, keep


def validate_empty_hull(vertices: list[list[int]], height: list[int]) -> dict:
    points = [tuple(int(x) for x in p) for p in vertices]
    require(len(points) == len(set(points)), "duplicate hull vertex")
    layer0, layer1, pivot, keep = layer_data(vertices, height)
    layer_hulls = [convex_hull2(layer0), convex_hull2(layer1)]
    require(set(layer_hulls[0]) == set(layer0), "non-extreme lattice point in layer zero")
    require(set(layer_hulls[1]) == set(layer1), "non-extreme lattice point in layer one")
    checked_points: list[tuple[int, int, int]] = []
    for layer, polygon, level in zip((layer0, layer1), layer_hulls, (0, 1)):
        bounds = [
            (min(point[j] for point in layer), max(point[j] for point in layer))
            for j in range(2)
        ]
        for first in range(bounds[0][0], bounds[0][1] + 1):
            for second in range(bounds[1][0], bounds[1][1] + 1):
                projected = (first, second)
                if not point_in_convex_polygon(projected, polygon):
                    continue
                point = [0, 0, 0]
                point[pivot] = level
                point[keep[0]], point[keep[1]] = projected
                checked_points.append(tuple(point))
        require(set(checked_points) >= set(tuple(p) for p in points if dot3(tuple(height), tuple(p)) == level), "missing hull vertex")
    require(set(checked_points) == set(points), "hull contains an additional lattice point")
    return {
        "vertex_count": len(points),
        "layer_sizes": [len(layer0), len(layer1)],
        "lattice_points_checked": len(checked_points),
        "empty": True,
        "width_one": True,
    }


def canonical_key(points: list[list[int]]) -> tuple[tuple[int, int, int], ...]:
    """Independent affine GL(3,Z) invariant using every unimodular frame."""

    tuples = tuple(tuple(int(x) for x in p) for p in points)
    best = None
    for frame in itertools.permutations(tuples, 4):
        matrix = matrix_from_frame(frame)
        determinant = det3(matrix)
        if abs(determinant) != 1:
            continue
        adjugate = adj3(matrix)
        anchor = frame[0]
        coordinates = tuple(
            sorted(
                tuple(
                    determinant
                    * sum(adjugate[i][j] * (point[j] - anchor[j]) for j in range(3))
                    for i in range(3)
                )
                for point in tuples
            )
        )
        if best is None or coordinates < best:
            best = coordinates
    require(best is not None, "hull has no unimodular frame")
    return best


def key_digest(key: tuple[tuple[int, int, int], ...]) -> str:
    return hashlib.sha256(repr(key).encode("ascii")).hexdigest()


def tetrahedron_lattice_points(vertices: list[tuple[int, int, int]]) -> set[tuple[int, int, int]]:
    matrix = matrix_from_frame(tuple(vertices))
    determinant = det3(matrix)
    require(determinant != 0, "quartet is degenerate")
    adjugate = adj3(matrix)
    bounds = [
        (min(p[j] for p in vertices), max(p[j] for p in vertices)) for j in range(3)
    ]
    points: set[tuple[int, int, int]] = set()
    for x in range(bounds[0][0], bounds[0][1] + 1):
        for y in range(bounds[1][0], bounds[1][1] + 1):
            for z in range(bounds[2][0], bounds[2][1] + 1):
                point = (x, y, z)
                difference = sub3(point, vertices[0])
                numerators = [sum(adjugate[i][j] * difference[j] for j in range(3)) for i in range(3)]
                barycentric = [Fraction(value, determinant) for value in numerators]
                anchor = 1 - sum(barycentric, Fraction(0))
                if min(anchor, *barycentric) >= 0:
                    points.add(point)
    return points


def section_minimum_certificate(vertices: list[list[int]], height: list[int]) -> dict:
    points = [tuple(int(x) for x in p) for p in vertices]
    h = tuple(int(x) for x in height)
    layer0, layer1, pivot, keep = layer_data(vertices, height)
    differences = [
        (a[0] - b[0], a[1] - b[1])
        for layer in (layer0, layer1)
        for a in layer
        for b in layer
    ]
    polygon = convex_hull2(differences)
    facets = []
    for first, second in zip(polygon, polygon[1:] + polygon[:1]):
        normal = (second[1] - first[1], first[0] - second[0])
        offset = normal[0] * first[0] + normal[1] * first[1]
        require(offset > 0 and all(normal[0] * p[0] + normal[1] * p[1] <= offset for p in differences), "invalid section facet")
        facets.append({"normal": list(normal), "offset": offset})
    bounds = [max(abs(point[j]) for point in polygon) for j in range(2)]
    minimum = Fraction(1)
    active: list[tuple[int, int]] = []
    checked = 0
    for vector in itertools.product(*(range(-bound, bound + 1) for bound in bounds)):
        z = tuple(int(x) for x in vector)
        if not primitive_vector(z):
            continue
        checked += 1
        value = max(Fraction(n[0] * z[0] + n[1] * z[1], f["offset"]) for n, f in [(tuple(f["normal"]), f) for f in facets])
        if value < minimum:
            minimum = value
            active = [z]
        elif value == minimum:
            active.append(z)

    def lift(vector: tuple[int, int]) -> list[int]:
        lifted = [0, 0, 0]
        lifted[keep[0]], lifted[keep[1]] = vector
        lifted[pivot] = -dot3(h, tuple(lifted))
        return lifted

    certificate = {
        "lambda1": fraction_string(minimum),
        "height_direction": list(h),
        "deleted_coordinate": pivot,
        "section_vertices": [list(point) for point in polygon],
        "section_facets": facets,
        "section_search_bounds": bounds,
        "primitive_section_vectors_checked": checked,
        "section_minimizers_mod_sign": [lift(vector) for vector in active],
        "scope": "Section minimizers listed; at lambda1=1 nonplanar minimizers may also exist.",
    }
    return certificate


def validate_main_certificate(repo: Path, certificate: dict | None = None) -> dict:
    source = json.loads((repo / "results" / "empty_tetrahedra_through_21.json").read_text())
    if certificate is None:
        certificate = json.loads((repo / "certificates" / "contact_obstructions.json").read_text())
    return main_certificate_expected_summary(certificate, source)


def validate_extensions(repo: Path, extension_data: dict | None = None) -> tuple[dict, dict]:
    if extension_data is None:
        extension_data = json.loads((repo / "results" / "contact_extensions.json").read_text())
    expected_keys = {
        "status",
        "threshold",
        "scope",
        "coordinate_bound",
        "raw_extension_points",
        "admissible_extensions_of_standard_frame",
        "allowed_ordered_tetrahedron_hnfs",
        "counts",
        "classes",
    }
    require(set(extension_data) == expected_keys, "extension metadata keys changed")
    require(extension_data["status"] == "exact_candidate_enumeration_pending_independent_review", "extension status changed")
    require(extension_data["threshold"] == "w(K)>(11/7)*(1+2/sqrt(3))", "extension threshold changed")
    require(
        extension_data["scope"]
        == "Full-dimensional empty lattice contact hulls with five to eight vertices, tetrahedron-wise necessary obstruction only",
        "extension scope changed",
    )
    require(extension_data["coordinate_bound"] == 13, "extension coordinate bound changed")
    require(extension_data["raw_extension_points"] == 13100, "extension raw-point count changed")
    require(extension_data["admissible_extensions_of_standard_frame"] == 424, "extension admissible count changed")
    require(extension_data["allowed_ordered_tetrahedron_hnfs"] == 47, "extension ordered-HNF count changed")
    require(extension_data["counts"] == {"5": 11, "6": 22, "7": 10, "8": 9}, "extension class counts changed")
    classes = extension_data["classes"]
    require(len(classes) == 52, "extension class count changed")

    keys: list[tuple[tuple[int, int, int], ...]] = []
    records = []
    for index, item in enumerate(classes):
        vertices = item["vertices"]
        height = item["width_one_direction"]
        require(len(vertices) in (5, 6, 7, 8), f"extension vertex count invalid at {index}")
        require(len(set(tuple(p) for p in vertices)) == len(vertices), f"duplicate extension vertex at {index}")
        require(sum(abs(int(x)) for x in height) == 1, f"extension height is not primitive at {index}")
        # The independent layer and lattice-point test is the emptiness check.
        empty_record = validate_empty_hull(vertices, height)
        require(empty_record["vertex_count"] == len(vertices), f"empty-hull vertex count mismatch at {index}")
        key = canonical_key(vertices)
        keys.append(key)
        records.append(
            {
                "index": index,
                "vertices": vertices,
                "vertex_count": len(vertices),
                "height_direction": height,
                "layer_sizes": empty_record["layer_sizes"],
                "lattice_points_checked": empty_record["lattice_points_checked"],
                "empty": True,
                "width_one": True,
                "canonical_key_sha256": key_digest(key),
            }
        )

    require(len(set(keys)) == 52, "extension canonical keys are not unique")
    counts = {str(n): sum(len(c["vertices"]) == n for c in classes) for n in range(5, 9)}
    require(counts == {"5": 11, "6": 22, "7": 10, "8": 9}, "extension vertex histogram changed")
    return (
        {
            "classes_checked": len(classes),
            "counts": counts,
            "empty_hulls_checked": len(classes),
            "width_one_certificates_checked": len(classes),
            "canonical_keys_checked": len(keys),
            "canonical_keys_unique": True,
        },
        {"keys": keys, "records": records},
    )


def affine_image(
    matrix: list[list[int]], translation: list[int], point: list[int]
) -> tuple[int, int, int]:
    """Apply an explicitly certified integral affine map."""

    return tuple(
        sum(int(matrix[row][column]) * int(point[column]) for column in range(3))
        + int(translation[row])
        for row in range(3)
    )


def validate_templates(
    repo: Path,
    template_data: dict | None = None,
    main_certificate: dict | None = None,
    extension_data: dict | None = None,
) -> tuple[dict, dict]:
    """Check all nine templates and all 63 integral affine embeddings.

    The expected target list is reconstructed from the independently checked
    determinant-21 tetrahedron certificate (the ten intermediate survivors),
    the independently checked 52 hull extensions, and the explicit planar
    square.  Thus a row cannot pass merely by reproducing its own target
    vertices: its class index and target representative are checked against
    the preceding certificates as well.
    """

    if template_data is None:
        template_data = json.loads((repo / "certificates" / "contact_templates.json").read_text())
    if main_certificate is None:
        main_certificate = json.loads((repo / "certificates" / "contact_obstructions.json").read_text())
    if extension_data is None:
        extension_data = json.loads((repo / "results" / "contact_extensions.json").read_text())

    expected_keys = {
        "status",
        "scope",
        "templates",
        "template_count",
        "configuration_count",
        "embeddings",
    }
    require(set(template_data) == expected_keys, "template metadata keys changed")
    require(
        template_data["status"] == "exact_template_embeddings_pending_independent_replay",
        "template status changed",
    )
    require(
        template_data["scope"]
        == "Each necessary contact hull is a subset of a template up to affine lattice equivalence. The template need not lie in the surrounding hollow body.",
        "template scope changed",
    )
    templates = template_data["templates"]
    require(template_data["template_count"] == 9, "template count changed")
    require(len(templates) == 9, "template list length changed")
    template_keys: list[tuple[tuple[int, int, int], ...]] = []
    template_records = []
    for index, template in enumerate(templates):
        require(len(template) == 8, f"template {index} does not have eight vertices")
        require(len(set(tuple(p) for p in template)) == 8, f"template {index} has duplicate vertices")
        require(all(len(p) == 3 and all(isinstance(x, int) and not isinstance(x, bool) for x in p) for p in template), f"template {index} is not integral")
        # Every template is full dimensional, so its affine-lattice key is a
        # useful independent guard against a duplicated or malformed row.
        key = canonical_key(template)
        template_keys.append(key)
        template_records.append(
            {
                "index": index,
                "vertex_count": len(template),
                "canonical_key_sha256": key_digest(key),
            }
        )
    require(len(set(template_keys)) == 9, "template canonical keys are not unique")

    embeddings = template_data["embeddings"]
    require(template_data["configuration_count"] == 63, "template configuration count changed")
    require(len(embeddings) == 63, "template embedding count changed")

    # Ten determinant-21 tetrahedra survive the intermediate 11/7 threshold;
    # they precede the 52 nonsimplicial hulls, with the square last.
    tetra_targets = [
        case["vertices"]
        for case in main_certificate["cases"]
        if case["survives_threshold_11A_over_7"]
    ]
    require(len(tetra_targets) == 10, "template tetrahedron target count changed")
    hull_targets = [item["vertices"] for item in extension_data["classes"]]
    require(len(hull_targets) == 52, "template hull target count changed")
    square_target = [[0, 0, 0], [0, 1, 0], [1, 0, 0], [1, 1, 0]]
    target_vertices = tetra_targets + hull_targets + [square_target]
    require(len(target_vertices) == 63, "template target count changed")
    target_keys = [tuple(sorted(tuple(p) for p in target)) for target in target_vertices]
    require(len(set(target_keys)) == 63, "template target classes are duplicated")

    records = []
    for index, embedding in enumerate(embeddings):
        expected_embedding_keys = {
            "class_index",
            "vertices",
            "template_index",
            "subset_indices",
            "map_subset_to_class",
        }
        require(set(embedding) == expected_embedding_keys, f"template embedding keys changed at {index}")
        require(embedding["class_index"] == index, f"template class index mismatch at {index}")
        target = embedding["vertices"]
        require(
            tuple(sorted(tuple(p) for p in target)) == target_keys[index],
            f"template target representative mismatch at {index}",
        )
        template_index = embedding["template_index"]
        require(isinstance(template_index, int) and not isinstance(template_index, bool), f"template index is not integral at {index}")
        require(0 <= template_index < len(templates), f"template index out of range at {index}")
        subset_indices = embedding["subset_indices"]
        require(len(subset_indices) == len(target), f"template subset size mismatch at {index}")
        require(all(isinstance(i, int) and not isinstance(i, bool) for i in subset_indices), f"template subset index is not integral at {index}")
        require(len(set(subset_indices)) == len(subset_indices), f"template subset indices are not unique at {index}")
        require(all(0 <= i < 8 for i in subset_indices), f"template subset index out of range at {index}")

        affine = embedding["map_subset_to_class"]
        require(set(affine) == {"matrix", "translation"}, f"template affine-map keys changed at {index}")
        matrix = affine["matrix"]
        translation = affine["translation"]
        require(
            len(matrix) == 3 and all(len(row) == 3 for row in matrix),
            f"template affine matrix shape changed at {index}",
        )
        require(len(translation) == 3, f"template affine translation shape changed at {index}")
        require(
            all(isinstance(x, int) and not isinstance(x, bool) for row in matrix for x in row)
            and all(isinstance(x, int) and not isinstance(x, bool) for x in translation),
            f"template affine map is not integral at {index}",
        )
        determinant = det3(tuple(tuple(row) for row in matrix))
        require(abs(determinant) == 1, f"template affine matrix is not unimodular at {index}")
        image = [
            affine_image(matrix, translation, templates[template_index][subset_index])
            for subset_index in subset_indices
        ]
        require(set(image) == set(tuple(p) for p in target), f"template affine image mismatch at {index}")
        records.append(
            {
                "class_index": index,
                "template_index": template_index,
                "vertex_count": len(target),
                "subset_indices": list(subset_indices),
                "affine_determinant": determinant,
                "integral_unimodular_map_checked": True,
                "target_vertices_checked": True,
            }
        )

    require([row["class_index"] for row in records] == list(range(63)), "template class references are incomplete")
    return (
        {
            "templates_checked": len(templates),
            "template_vertex_count": 8,
            "template_canonical_keys_unique": True,
            "embeddings_checked": len(embeddings),
            "target_class_indices_exact": True,
            "integral_unimodular_maps_checked": len(embeddings),
            "subset_indices_checked": len(embeddings),
        },
        {"template_records": template_records, "embedding_records": records},
    )


def validate_tetrahedron_quartets(vertices: list[list[int]]) -> dict:
    points = [tuple(int(x) for x in p) for p in vertices]
    values: list[str] = []
    determinant_histogram: dict[str, int] = {}
    quartets = 0
    degenerate_quartets = 0
    full_dimensional_quartets = 0
    for quartet in itertools.combinations(points, 4):
        quartets += 1
        determinant = abs(det3(matrix_from_frame(tuple(quartet))))
        # A nonsimplicial contact hull can contain coplanar four-subsets.  The
        # tetrahedral P-P certificate applies to full-dimensional quartets;
        # those are all checked below, while degenerate subsets are counted
        # explicitly rather than being mistaken for tetrahedra.
        if determinant == 0:
            degenerate_quartets += 1
            continue
        full_dimensional_quartets += 1
        require(tetrahedron_lattice_points(list(quartet)) == set(quartet), "extension quartet is not empty")
        cert = simplex_minimum_certificate([list(p) for p in quartet])
        ell = Fraction(cert["lambda1"])
        require(ell > Fraction(4, 11), "extension quartet falls below the contact threshold")
        require(determinant <= 13, "extension quartet determinant exceeds the ten-type bound")
        values.append(cert["lambda1"])
        determinant_histogram[str(determinant)] = determinant_histogram.get(str(determinant), 0) + 1
    minimum = min((Fraction(value) for value in values), default=Fraction(0))
    return {
        "quartets_checked": quartets,
        "full_dimensional_quartets": full_dimensional_quartets,
        "degenerate_quartets": degenerate_quartets,
        "empty_quartets": full_dimensional_quartets,
        "all_lambda1_gt_4_11": True,
        "minimum_quartet_lambda1": fraction_string(minimum),
        "quartet_lambda1_histogram": {
            value: values.count(value) for value in sorted(set(values), key=Fraction)
        },
        "quartet_determinant_histogram": dict(sorted(determinant_histogram.items(), key=lambda pair: int(pair[0]))),
    }


def validate_hull_certificates(
    repo: Path,
    extension_keys: dict[tuple[tuple[int, int, int], ...], int],
    extension_records: list[dict],
    hull_data: dict | None = None,
) -> tuple[dict, list[dict]]:
    if hull_data is None:
        hull_data = json.loads((repo / "certificates" / "contact_hull_obstructions.json").read_text())
    expected_keys = {
        "status",
        "classes_checked",
        "counts_before",
        "counts_after_intermediate",
        "counts_after_candidate",
        "classes",
    }
    require(set(hull_data) == expected_keys, "hull certificate metadata keys changed")
    require(hull_data["status"] == "exact_candidate_reduction_pending_independent_review", "hull status changed")
    require(hull_data["classes_checked"] == 52, "hull class count changed")
    expected_counts = {"5": 11, "6": 22, "7": 10, "8": 9}
    require(hull_data["counts_before"] == expected_counts, "hull before-counts changed")
    require(hull_data["counts_after_intermediate"] == expected_counts, "hull intermediate-counts changed")
    require(hull_data["counts_after_candidate"] == expected_counts, "hull candidate-counts changed")
    classes = hull_data["classes"]
    require(len(classes) == 52, "hull class list length changed")
    hull_keys: dict[tuple[tuple[int, int, int], ...], int] = {}
    records = []
    total_quartets = 0
    global_lambda_histogram: dict[str, int] = {}
    for index, item in enumerate(classes):
        vertices = item["vertices"]
        height = item["width_one_direction"]
        key = canonical_key(vertices)
        require(key in extension_keys, f"hull class {index} has no extension counterpart")
        require(key not in hull_keys, f"duplicate hull canonical key at {index}")
        hull_keys[key] = index
        require(
            set(tuple(p) for p in vertices)
            == set(tuple(p) for p in extension_records[extension_keys[key]]["vertices"]),
            f"hull and extension vertices differ at {index}",
        )
        empty_record = validate_empty_hull(vertices, height)
        section = section_minimum_certificate(vertices, height)
        require(item["minimum_certificate"] == section, f"hull section certificate mismatch at {index}")
        ell = Fraction(section["lambda1"])
        bound = radical_bound(ell)
        require(item["width_upper"] == bound, f"hull width bound mismatch at {index}")
        expected_intermediate = ell > Fraction(4, 11)
        expected_candidate = bound is None or not below_candidate_bound(bound)
        require(item["survives_intermediate_threshold"] is expected_intermediate, f"hull intermediate flag mismatch at {index}")
        require(item["survives_candidate_threshold"] is expected_candidate, f"hull candidate flag mismatch at {index}")
        require(expected_intermediate and expected_candidate, f"hull candidate {index} unexpectedly excluded")
        quartets = validate_tetrahedron_quartets(vertices)
        total_quartets += quartets["quartets_checked"]
        for value, count in quartets["quartet_lambda1_histogram"].items():
            global_lambda_histogram[value] = global_lambda_histogram.get(value, 0) + count
        records.append(
            {
                "index": index,
                "vertex_count": len(vertices),
                "lambda1": section["lambda1"],
                "section_minimum_certificate_checked": True,
                "full_minimum_proof_checked": True,
                "quartets": quartets,
                "canonical_key_sha256": key_digest(key),
                "empty": empty_record["empty"],
                "width_one": empty_record["width_one"],
            }
        )
    require(set(hull_keys) == set(extension_keys), "extension and hull class sets differ")
    require(len(hull_keys) == 52, "hull canonical keys are not unique")
    return (
        {
            "classes_checked": len(classes),
            "full_minimum_certificates_checked": len(classes),
            "all_hull_certificates_exact": True,
            "all_hulls_empty": True,
            "all_hulls_width_one": True,
            "canonical_keys_unique": True,
            "quartets_checked": total_quartets,
            "all_quartets_empty": True,
            "all_quartets_lambda1_gt_4_11": True,
            "quartet_lambda1_histogram": dict(sorted(global_lambda_histogram.items(), key=lambda pair: Fraction(pair[0]))),
        },
        records,
    )


def expect_rejection(label: str, validator, mutated) -> str:
    try:
        validator(mutated)
    except (AssertionError, KeyError, IndexError, TypeError, ValueError):
        return label
    raise ValidationError(f"mutation guard failed to reject {label}")


def run_mutation_guards(
    repo: Path,
    main_certificate: dict,
    extension_data: dict,
    hull_data: dict,
    template_data: dict,
) -> list[str]:
    labels: list[str] = []

    def main_validator(value):
        validate_main_certificate(repo, value)

    def extension_validator(value):
        validate_extensions(repo, value)

    extension_summary, extension_payload = validate_extensions(repo, extension_data)
    extension_keys = {key: index for index, key in enumerate(extension_payload["keys"])}
    extension_records = extension_payload["records"]

    def hull_validator(value):
        validate_hull_certificates(repo, extension_keys, extension_records, value)

    def template_validator(value):
        validate_templates(repo, value, main_certificate, extension_data)

    mutation = copy.deepcopy(main_certificate)
    mutation["cases"][0]["minimum_certificate"]["lambda1"] = "1/999"
    labels.append(expect_rejection("main_changed_lambda", main_validator, mutation))

    mutation = copy.deepcopy(main_certificate)
    mutation["cases"].pop()
    labels.append(expect_rejection("main_missing_class", main_validator, mutation))

    mutation = copy.deepcopy(main_certificate)
    mutation["cases"][0]["minimum_certificate"]["primitive_minimizers_mod_sign"].pop()
    labels.append(expect_rejection("main_missing_minimizer", main_validator, mutation))

    mutation = copy.deepcopy(main_certificate)
    mutation["cases"][0]["minimum_certificate"]["complete_search"]["primitive_vectors_checked"] += 1
    labels.append(expect_rejection("main_forged_count", main_validator, mutation))

    mutation = copy.deepcopy(main_certificate)
    mutation["cases"][0]["hnf"][0][0] += 1
    labels.append(expect_rejection("main_forged_hnf", main_validator, mutation))

    mutation = copy.deepcopy(main_certificate)
    mutation["survivors_candidate_threshold"] += 1
    labels.append(expect_rejection("main_forged_survivor_count", main_validator, mutation))

    mutation = copy.deepcopy(main_certificate)
    mutation["cases"][2]["width_upper"]["b"] = "200/3"
    labels.append(expect_rejection("main_changed_radical_width", main_validator, mutation))

    mutation = copy.deepcopy(main_certificate)
    mutation["cases"][2]["width_upper_decimal_display"] += 0.01
    labels.append(expect_rejection("main_forged_decimal_width", main_validator, mutation))

    mutation = copy.deepcopy(extension_data)
    mutation["classes"].pop()
    labels.append(expect_rejection("extension_missing_class", extension_validator, mutation))

    mutation = copy.deepcopy(extension_data)
    mutation["classes"][0]["vertices"][0] = [0, 0]
    labels.append(expect_rejection("extension_forged_vertex", extension_validator, mutation))

    mutation = copy.deepcopy(extension_data)
    mutation["classes"][-1]["vertices"] = copy.deepcopy(mutation["classes"][0]["vertices"])
    labels.append(expect_rejection("extension_duplicate_class", extension_validator, mutation))

    mutation = copy.deepcopy(extension_data)
    mutation["counts"]["5"] += 1
    labels.append(expect_rejection("extension_forged_count", extension_validator, mutation))

    mutation = copy.deepcopy(hull_data)
    mutation["classes"][0]["minimum_certificate"]["lambda1"] = "1/999"
    labels.append(expect_rejection("hull_changed_lambda", hull_validator, mutation))

    mutation = copy.deepcopy(hull_data)
    mutation["classes"].pop()
    labels.append(expect_rejection("hull_missing_class", hull_validator, mutation))

    mutation = copy.deepcopy(hull_data)
    mutation["classes"][0]["minimum_certificate"]["section_minimizers_mod_sign"].pop()
    labels.append(expect_rejection("hull_missing_minimizer", hull_validator, mutation))

    mutation = copy.deepcopy(hull_data)
    mutation["classes"][0]["minimum_certificate"]["primitive_section_vectors_checked"] += 1
    labels.append(expect_rejection("hull_forged_count", hull_validator, mutation))

    mutation = copy.deepcopy(hull_data)
    mutation["counts_after_candidate"]["5"] += 1
    labels.append(expect_rejection("hull_forged_count_metadata", hull_validator, mutation))

    mutation = copy.deepcopy(template_data)
    mutation["embeddings"][0]["map_subset_to_class"]["matrix"][0][0] += 1
    labels.append(expect_rejection("template_changed_unimodular_map", template_validator, mutation))

    mutation = copy.deepcopy(template_data)
    mutation["embeddings"][0]["subset_indices"][0] = 8
    labels.append(expect_rejection("template_invalid_subset_index", template_validator, mutation))

    mutation = copy.deepcopy(template_data)
    mutation["embeddings"].pop()
    labels.append(expect_rejection("template_missing_class", template_validator, mutation))

    mutation = copy.deepcopy(template_data)
    mutation["configuration_count"] += 1
    labels.append(expect_rejection("template_forged_count", template_validator, mutation))
    return labels


def main() -> None:
    if sys.flags.optimize:
        raise SystemExit('Assertions required: do not run with -O or -OO')
    parser = argparse.ArgumentParser(description="independent contact-reduction certificate verifier")
    parser.add_argument("--skip-mutation-guards", action="store_true")
    args = parser.parse_args()
    repo = Path(__file__).resolve().parents[1]
    main_certificate = json.loads((repo / "certificates" / "contact_obstructions.json").read_text())
    extension_data = json.loads((repo / "results" / "contact_extensions.json").read_text())
    hull_data = json.loads((repo / "certificates" / "contact_hull_obstructions.json").read_text())
    template_data = json.loads((repo / "certificates" / "contact_templates.json").read_text())

    # Preserve the original 37-class replay as a live check.  The newer
    # certificate checks below cover all 51 determinant-21 cases, but should
    # not make the historical contact-minima artifact silently dead code.
    replay_certificate(repo)
    source21_path = repo / "results" / "empty_tetrahedra_through_21.json"
    if source21_path.exists():
        replay_source21(repo, source21_path)

    main_summary = validate_main_certificate(repo, main_certificate)
    extension_summary, extension_payload = validate_extensions(repo, extension_data)
    extension_keys = {key: index for index, key in enumerate(extension_payload["keys"])}
    hull_summary, hull_records = validate_hull_certificates(
        repo, extension_keys, extension_payload["records"], hull_data
    )
    template_summary, template_payload = validate_templates(
        repo, template_data, main_certificate, extension_data
    )
    mutation_labels = [] if args.skip_mutation_guards else run_mutation_guards(
        repo, main_certificate, extension_data, hull_data, template_data
    )

    result = {
        "status": "independent_validation_passed",
        "method": "stdlib-only exact integer/Fraction replay; root generators are not imported",
        "scope": {
            "main_certificate_cases": 51,
            "historical_contact_minima_classes": 37,
            "extension_hulls": 52,
            "hull_vertex_sizes": {"5": 11, "6": 22, "7": 10, "8": 9},
            "quartet_completeness": "all four-vertex subsets of every 52-hull checked",
            "completeness_claim": "The 52-class enumeration itself is supplied by the root/Astra workflow; this verifier checks every supplied class and its certificate.",
        },
        "main_certificate": main_summary,
        "extension_validation": extension_summary,
        "hull_validation": hull_summary,
        "template_validation": template_summary,
        "mutation_guards": {
            "enabled": not args.skip_mutation_guards,
            "passed": len(mutation_labels),
            "labels": mutation_labels,
        },
        "extension_records": extension_payload["records"],
        "hull_records": hull_records,
        "template_records": template_payload,
    }
    output = repo / "results" / "contact_reduction_validation.json"
    output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({
        "status": result["status"],
        "main_cases": main_summary["classes_checked"],
        "hulls": extension_summary["classes_checked"],
        "quartets": hull_summary["quartets_checked"],
        "mutation_guards": len(mutation_labels),
        "templates": template_summary["templates_checked"],
        "embeddings": template_summary["embeddings_checked"],
    }, indent=2))


if __name__ == "__main__":
    main()
