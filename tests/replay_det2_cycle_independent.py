#!/usr/bin/env python3
"""Independent exact replay of the determinant-two cycle certificates.

This module deliberately uses only the Python standard library.  In
particular, it does not import ``src`` or reuse the project's geometry
implementation.  The small amount of linear algebra below is implemented
with :class:`fractions.Fraction`, and all proof decisions are exact.

Both ``certificates/det2_cycle_rational.json`` and
``certificates/det2_four_contacts.json`` are required inputs. Running the file writes
``results/det2_cycle_independent.json``.
"""

from __future__ import annotations

from copy import deepcopy
from fractions import Fraction
from itertools import combinations, product
from math import gcd
import json
from pathlib import Path
from typing import Any, Iterable, Sequence


ROOT = Path(__file__).resolve().parents[1]
PRIMARY_CERTIFICATE = ROOT / "certificates" / "det2_cycle_rational.json"
FOUR_CONTACT_CERTIFICATE = ROOT / "certificates" / "det2_four_contacts.json"
OUTPUT = ROOT / "results" / "det2_cycle_independent.json"

# The four-cycle reconstruction uses the standard integral contact frame
# appearing in the certificate generator: one origin, one (2,1,1) contact,
# and the two coordinate contacts e_2 and e_3.  Their order is the row order
# used when converting the inverse facet matrix back to vertices.
CONTACT_FRAME: tuple[tuple[int, int, int], ...] = (
    (0, 0, 0),
    (2, 1, 1),
    (0, 1, 0),
    (0, 0, 1),
)

DESIGNATED_RELINT = (
    ((0, 0, 0), (1, 2, 3)),
    ((2, 1, 1), (0, 2, 3)),
    ((0, 1, 0), (0, 1, 3)),
    ((0, 0, 1), (0, 1, 2)),
)


class ValidationError(AssertionError):
    """Raised when a serialized field does not match an exact replay."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValidationError(message)


def frac(value: Any) -> Fraction:
    """Parse a rational JSON scalar without accepting binary floats."""

    require(not isinstance(value, float), "floating point value in certificate")
    try:
        return Fraction(value)
    except (TypeError, ValueError, ZeroDivisionError) as exc:
        raise ValidationError(f"invalid rational scalar {value!r}") from exc


def qscalar(value: Any) -> Fraction:
    """Parse the project's rational-only Q JSON representation."""

    require(isinstance(value, dict), f"expected Q object, got {value!r}")
    require(set(value) == {"a", "b", "d"}, "malformed Q object")
    a = frac(value["a"])
    b = frac(value["b"])
    require(b == 0, "independent replay only accepts rational Q entries")
    require(int(value["d"]) == 2, "unexpected quadratic field tag")
    return a


def vector_sub(a: Sequence[Fraction], b: Sequence[Fraction]) -> tuple[Fraction, ...]:
    return tuple(x - y for x, y in zip(a, b))


def dot(a: Sequence[Fraction], b: Sequence[Fraction]) -> Fraction:
    return sum((x * y for x, y in zip(a, b)), Fraction(0))


def cross(a: Sequence[Fraction], b: Sequence[Fraction]) -> tuple[Fraction, Fraction, Fraction]:
    return (
        a[1] * b[2] - a[2] * b[1],
        a[2] * b[0] - a[0] * b[2],
        a[0] * b[1] - a[1] * b[0],
    )


def determinant(matrix: Sequence[Sequence[Fraction]]) -> Fraction:
    """Bareiss-free recursive determinant, sufficient for the 4 by 4 inputs."""

    n = len(matrix)
    if n == 0:
        return Fraction(1)
    if n == 1:
        return matrix[0][0]
    total = Fraction(0)
    for j, entry in enumerate(matrix[0]):
        minor = [list(row[:j]) + list(row[j + 1 :]) for row in matrix[1:]]
        total += (-1 if j % 2 else 1) * entry * determinant(minor)
    return total


def inverse(matrix: Sequence[Sequence[Fraction]]) -> list[list[Fraction]]:
    """Gauss-Jordan inversion over Fraction, independent of project helpers."""

    n = len(matrix)
    require(n and all(len(row) == n for row in matrix), "square matrix required")
    aug = [list(row) + [Fraction(int(i == j)) for j in range(n)] for i, row in enumerate(matrix)]
    for col in range(n):
        pivot = next((row for row in range(col, n) if aug[row][col]), None)
        require(pivot is not None, "singular matrix")
        if pivot != col:
            aug[col], aug[pivot] = aug[pivot], aug[col]
        scale = aug[col][col]
        aug[col] = [x / scale for x in aug[col]]
        for row in range(n):
            if row == col:
                continue
            scale = aug[row][col]
            if scale:
                aug[row] = [x - scale * y for x, y in zip(aug[row], aug[col])]
    return [row[n:] for row in aug]


def parse_point(value: Any) -> tuple[int, int, int]:
    require(isinstance(value, list) and len(value) == 3, f"malformed lattice point {value!r}")
    answer = []
    for x in value:
        require(isinstance(x, int) and not isinstance(x, bool), "lattice point is not integral")
        answer.append(int(x))
    return tuple(answer)  # type: ignore[return-value]


def parse_vertices(value: Any) -> list[tuple[Fraction, Fraction, Fraction]]:
    require(isinstance(value, list) and len(value) == 4, "expected four vertices")
    answer: list[tuple[Fraction, Fraction, Fraction]] = []
    for vertex in value:
        require(isinstance(vertex, list) and len(vertex) == 3, "malformed vertex")
        answer.append(tuple(qscalar(x) for x in vertex))  # type: ignore[arg-type]
    return answer


def parse_matrix(value: Any) -> list[list[Fraction]]:
    require(isinstance(value, list) and len(value) == 4, "expected four by four matrix")
    answer = []
    for row in value:
        require(isinstance(row, list) and len(row) == 4, "malformed four by four matrix")
        answer.append([frac(x) for x in row])
    return answer


def parse_q_vector(value: Any) -> tuple[Fraction, Fraction, Fraction]:
    require(isinstance(value, list) and len(value) == 3, "malformed Q vector")
    return tuple(qscalar(x) for x in value)  # type: ignore[return-value]


def q_matrix_json(matrix: Sequence[Sequence[Fraction]]) -> list[list[dict[str, Any]]]:
    return [[{"a": str(x), "b": "0", "d": 2} for x in row] for row in matrix]


def point_list_json(points: Iterable[Sequence[int]]) -> list[list[int]]:
    return [list(map(int, point)) for point in points]


def rational_text(value: Fraction) -> str:
    return str(value)


def reconstruct_facet_matrix(parameters: Sequence[Fraction]) -> list[list[Fraction]]:
    require(len(parameters) == 8, "expected eight cycle parameters")
    matrix = [[Fraction(0) for _ in range(4)] for _ in range(4)]
    for i in range(4):
        x, y = parameters[2 * i : 2 * i + 2]
        a = (1 + x) / 2
        remainder = 1 - a
        matrix[i][(i + 1) % 4] = a
        matrix[i][(i + 2) % 4] = remainder * y
        matrix[i][(i + 3) % 4] = remainder * (1 - y)
    return matrix


def reconstruct_vertices(matrix: Sequence[Sequence[Fraction]]) -> list[tuple[Fraction, Fraction, Fraction]]:
    inv = inverse(matrix)
    column_sums = [sum((inv[i][j] for i in range(4)), Fraction(0)) for j in range(4)]
    require(all(x > 0 for x in column_sums), "inverse facet matrix has nonpositive column sum")
    vertices = []
    for j in range(4):
        vertices.append(
            tuple(
                sum((CONTACT_FRAME[i][k] * inv[i][j] for i in range(4)), Fraction(0))
                / column_sums[j]
                for k in range(3)
            )
        )
    return vertices


def check_cycle_chart(data: dict[str, Any]) -> tuple[list[tuple[Fraction, Fraction, Fraction]], list[list[Fraction]]]:
    parameters = [frac(x) for x in data.get("parameters", [])]
    matrix = parse_matrix(data.get("facet_matrix"))
    expected_matrix = reconstruct_facet_matrix(parameters)
    require(matrix == expected_matrix, "facet_matrix disagrees with cycle parameters")
    for i, row in enumerate(matrix):
        require(row[i] == 0, f"facet_matrix diagonal entry {i} is nonzero")
        require(sum(row, Fraction(0)) == 1, f"facet_matrix row {i} does not sum to one")
        require(all(row[j] > 0 for j in range(4) if j != i), f"facet_matrix row {i} is not positive off diagonal")

    expected_vertices = reconstruct_vertices(matrix)
    vertices = parse_vertices(data.get("vertices"))
    require(vertices == expected_vertices, "raw vertices disagree with facet_matrix/contact reconstruction")
    require(determinant([list(vector_sub(v, vertices[0])) for v in vertices[1:]]) != 0, "vertices are not full dimensional")
    return vertices, matrix


def independent_facets(vertices: Sequence[Sequence[Fraction]]) -> list[tuple[tuple[int, int, int], tuple[Fraction, Fraction, Fraction], Fraction]]:
    """Return the four outward supporting planes in ascending vertex-id order."""

    answer = []
    for ids in combinations(range(4), 3):
        a, b, c = (vertices[i] for i in ids)
        normal = cross(vector_sub(b, a), vector_sub(c, a))
        offset = dot(normal, a)
        signs = [dot(normal, v) - offset for v in vertices]
        require(all(x <= 0 for x in signs) or all(x >= 0 for x in signs), "facet vertices do not support simplex")
        if any(x > 0 for x in signs):
            normal = tuple(-x for x in normal)  # type: ignore[assignment]
            offset = -offset
        require(all(dot(normal, v) - offset <= 0 for v in vertices), "failed outward facet orientation")
        answer.append((ids, normal, offset))
    return answer


def exact_box(vertices: Sequence[Sequence[Fraction]]) -> list[list[int]]:
    bounds = []
    for coordinate in range(3):
        values = [v[coordinate] for v in vertices]
        lo = min(values)
        hi = max(values)
        bounds.append([(-(-lo.numerator // lo.denominator)), hi.numerator // hi.denominator])
    return bounds


def classify(point: Sequence[int], facets: Sequence[tuple[tuple[int, int, int], Sequence[Fraction], Fraction]]) -> str:
    signs = [dot(normal, point) - offset for _, normal, offset in facets]
    if any(x > 0 for x in signs):
        return "outside"
    if any(x == 0 for x in signs):
        return "boundary"
    return "interior"


def replay_lattice_points(
    data: dict[str, Any],
    vertices: Sequence[Sequence[Fraction]],
    facets: Sequence[tuple[tuple[int, int, int], Sequence[Fraction], Fraction]],
) -> dict[str, Any]:
    hollow = data.get("hollow")
    require(isinstance(hollow, dict), "missing hollow certificate")
    bounds = exact_box(vertices)
    stored_box = hollow.get("integer_box")
    require(stored_box == bounds, f"integer box mismatch: expected {bounds}, got {stored_box}")

    boundary: list[tuple[int, int, int]] = []
    interior: list[tuple[int, int, int]] = []
    count = 0
    for point in product(*(range(lo, hi + 1) for lo, hi in bounds)):
        count += 1
        location = classify(point, facets)
        if location == "boundary":
            boundary.append(point)
        elif location == "interior":
            interior.append(point)
    require(hollow.get("status") == ("certified_hollow" if not interior else "certified_nonhollow"), "hollow status mismatch")
    require(hollow.get("hollow") is (not interior), "hollow boolean mismatch")
    require(hollow.get("points_checked") == count, "exact bounding-box point count mismatch")
    require(hollow.get("interior_points") == point_list_json(interior), "interior lattice-point list mismatch")
    require(hollow.get("boundary_points") == point_list_json(boundary), "boundary lattice-point list mismatch")

    return {
        "status": hollow["status"],
        "integer_box": bounds,
        "points_checked": count,
        "interior_points": point_list_json(interior),
        "boundary_points": point_list_json(boundary),
    }


def parse_stored_facets(data: dict[str, Any], vertices: Sequence[Sequence[Fraction]], boundary: Sequence[Sequence[int]]) -> list[tuple[tuple[int, int, int], tuple[Fraction, Fraction, Fraction], Fraction]]:
    hollow = data["hollow"]
    stored = hollow.get("facets")
    require(isinstance(stored, list) and len(stored) == 4, "expected four stored facets")
    independent = independent_facets(vertices)
    parsed = []
    for index, (item, expected) in enumerate(zip(stored, independent)):
        require(isinstance(item, dict), f"facet {index} is malformed")
        expected_ids, expected_normal, expected_offset = expected
        ids = tuple(int(x) for x in item.get("vertex_ids", []))
        require(ids == expected_ids, f"facet {index} vertex ids mismatch")
        normal_value = parse_q_vector(item.get("normal"))
        offset_value = qscalar(item.get("offset"))
        require(normal_value != (0, 0, 0), f"facet {index} normal is zero")
        require(all(dot(normal_value, vertices[j]) == offset_value for j in ids), f"facet {index} misses a vertex plane")
        require(all(dot(normal_value, vertices[j]) < offset_value for j in set(range(4)) - set(ids)), f"facet {index} is not supporting outward")
        scale_index = next(i for i, x in enumerate(expected_normal) if x)
        scale = normal_value[scale_index] / expected_normal[scale_index]
        require(scale > 0, f"facet {index} orientation is reversed")
        require(all(normal_value[j] == scale * expected_normal[j] for j in range(3)), f"facet {index} normal is not proportional")
        require(offset_value == scale * expected_offset, f"facet {index} offset is inconsistent")

        contacts = [parse_point(point) for point in item.get("lattice_contacts", [])]
        relint = [parse_point(point) for point in item.get("relative_interior_contacts", [])]
        expected_contacts = [tuple(point) for point in boundary if dot(normal_value, point) == offset_value]
        expected_relint = [point for point in expected_contacts if sum(dot(n, point) == b for _, n, b in independent) == 1]
        require(contacts == expected_contacts, f"facet {index} lattice contacts mismatch")
        require(relint == expected_relint, f"facet {index} relative-interior contacts mismatch")
        parsed.append((ids, normal_value, offset_value))
    return parsed


def replay_designated_contacts(data: dict[str, Any], facets: Sequence[tuple[tuple[int, int, int], Sequence[Fraction], Fraction]]) -> list[dict[str, Any]]:
    all_relint = []
    for point, ids in DESIGNATED_RELINT:
        memberships = [facet_ids for facet_ids, normal, offset in facets if dot(normal, point) == offset]
        require(memberships == [ids], f"designated contact {point} is not relative-interior to facet {ids}")
        all_relint.append({"point": list(point), "facet_vertex_ids": list(ids)})
    return all_relint


def primitive_directions(bounds: Sequence[int]) -> list[tuple[int, int, int]]:
    answer = []
    for direction in product(*(range(-b, b + 1) for b in bounds)):
        if direction == (0, 0, 0):
            continue
        first_nonzero = next(x for x in direction if x)
        if first_nonzero <= 0:
            continue
        if gcd(*(abs(x) for x in direction)) != 1:
            continue
        answer.append(tuple(int(x) for x in direction))
    return answer


def directional_width(vertices: Sequence[Sequence[Fraction]], direction: Sequence[int]) -> Fraction:
    values = [dot(vertex, direction) for vertex in vertices]
    return max(values) - min(values)


def replay_width(data: dict[str, Any], vertices: Sequence[Sequence[Fraction]]) -> dict[str, Any]:
    width = data.get("width")
    require(isinstance(width, dict), "missing width certificate")
    expected_facets = independent_facets(vertices)
    del expected_facets  # Keeps this routine visibly independent of stored planes.

    basis_ids = [0, 1, 2, 3]
    differences = [list(vector_sub(vertices[i], vertices[0])) for i in basis_ids[1:]]
    differences_inverse = inverse(differences)
    initial_upper = min(directional_width(vertices, tuple(int(i == j) for i in range(3))) for j in range(3))
    bounds = [
        (initial_upper * sum((abs(x) for x in row), Fraction(0))).numerator
        // (initial_upper * sum((abs(x) for x in row), Fraction(0))).denominator
        for row in differences_inverse
    ]
    # The floor above is written without using any project helper.  Keep the
    # expression explicit so a future change cannot accidentally round up.
    stored_search = width.get("search_bound")
    require(isinstance(stored_search, dict), "missing width search bound")
    require(stored_search.get("basis_vertex_ids") == basis_ids, "width basis vertex ids mismatch")
    require(stored_search.get("initial_upper") == {"a": str(initial_upper), "b": "0", "d": 2}, "initial width upper bound mismatch")
    require(stored_search.get("D_inverse") == q_matrix_json(differences_inverse), "stored difference inverse mismatch")
    require(stored_search.get("coordinate_bounds") == bounds, "width coordinate bounds mismatch")
    require(stored_search.get("proof") == "q_i=<u,v_i-v_0>, |q_i|<=w(K,u)<=W; u=D^-1 q implies |u_j|<=W sum_i |D^-1_ji|. Outside this box width>W.", "width bound proof text mismatch")

    directions = primitive_directions(bounds)
    values = {direction: directional_width(vertices, direction) for direction in directions}
    best = min(values.values())
    minimizers = [list(direction) for direction in directions if values[direction] == best]
    require(width.get("status") == "certified_lattice_width", "width status mismatch")
    require(qscalar(width.get("width")) == best, "claimed width does not match complete direction replay")
    require(width.get("minimizing_directions_mod_sign") == minimizers, "claimed minimizer directions mismatch")
    require(width.get("direction_count") == len(directions), "complete direction count mismatch")
    upper = width.get("upper_certificate")
    lower = width.get("lower_certificate")
    require(isinstance(upper, dict) and isinstance(lower, dict), "incomplete width certificates")
    require(upper.get("direction") == minimizers[0], "upper witness direction mismatch")
    require(qscalar(upper.get("value")) == best, "upper witness value mismatch")
    require(qscalar(lower.get("checked_minimum")) == best, "lower checked minimum mismatch")
    require(lower.get("all_box_directions_checked") is True, "lower box-completeness flag missing")

    return {
        "width": rational_text(best),
        "minimizing_directions_mod_sign": minimizers,
        "direction_count": len(directions),
        "initial_upper": rational_text(initial_upper),
        "basis_vertex_ids": basis_ids,
        "coordinate_bounds": bounds,
        "basis_bound_justification": "For width <= initial_upper, each q_i=<u,v_i-v_0> satisfies |q_i|<=initial_upper. With u=D^-1 q, each integer coordinate u_j lies in the displayed floor bound; all primitive representatives in that finite box were checked.",
    }


def validate(data: dict[str, Any]) -> dict[str, Any]:
    require(data.get("status") == "exact_rational_reconstruction", "certificate status mismatch")
    vertices, _ = check_cycle_chart(data)
    independent = independent_facets(vertices)
    lattice = replay_lattice_points(data, vertices, independent)
    parse_stored_facets(data, vertices, lattice["boundary_points"])
    designated = replay_designated_contacts(data, independent)
    widths = replay_width(data, vertices)
    return {
        "status": "passed",
        "checks": {
            "raw_vertices_rational_facet_matrix_consistent": True,
            "exact_integer_bbox_exhausted": True,
            "stored_supporting_facets_and_contacts_consistent": True,
            "four_designated_relative_interior_contacts": True,
            "complete_width_basis_bound_and_direction_replay": True,
            "claimed_width_minimizers_consistent": True,
        },
        "exact": {
            "vertices": [[[str(x), "0", 2] for x in vertex] for vertex in vertices],
            "integer_box": lattice["integer_box"],
            "points_checked": lattice["points_checked"],
            "interior_points": lattice["interior_points"],
            "boundary_points": lattice["boundary_points"],
            "designated_relative_interior_contacts": designated,
            "width": widths,
        },
    }


def expect_rejection(mutated: dict[str, Any]) -> str:
    try:
        validate(mutated)
    except ValidationError as exc:
        return str(exc)
    raise ValidationError("mutation was accepted")


def mutation_guards(data: dict[str, Any]) -> dict[str, Any]:
    guards: dict[str, Any] = {}

    vertex_mutation = deepcopy(data)
    original_vertex = frac(vertex_mutation["vertices"][0][0]["a"])
    vertex_mutation["vertices"][0][0]["a"] = str(original_vertex + Fraction(1, 1000))
    guards["vertex_mutation"] = {
        "rejected": True,
        "reason": expect_rejection(vertex_mutation),
    }

    width_mutation = deepcopy(data)
    width_mutation["width"]["width"]["a"] = "1"
    guards["width_value_mutation"] = {
        "rejected": True,
        "reason": expect_rejection(width_mutation),
    }

    boundary_mutation = deepcopy(data)
    boundary = boundary_mutation["hollow"]["boundary_points"]
    require(len(boundary) >= 1, "cannot make boundary mutation on empty list")
    boundary_mutation["hollow"]["boundary_points"] = boundary[:-1]
    guards["boundary_list_mutation"] = {
        "rejected": True,
        "reason": expect_rejection(boundary_mutation),
    }
    return guards


def load_json(path: Path) -> dict[str, Any]:
    require(path.exists(), f"missing certificate: {path}")
    with path.open(encoding="utf-8") as handle:
        value = json.load(handle)
    require(isinstance(value, dict), f"certificate root is not an object: {path}")
    return value


def validate_claim(name: str, data: dict[str, Any]) -> dict[str, Any]:
    """Bind a self-consistent geometry payload to the two recorded claims."""
    result = validate(data)
    exact = result['exact']
    require(not exact['interior_points'], 'recorded witness must be hollow')
    expected = {
        'det2_cycle_rational.json': (
            '4320583268114594607881031741630319110755574/1315893928867311218381530956762804285589247',
            sorted([*CONTACT_FRAME, (1, 0, 1), (1, 1, 0)])),
        'det2_four_contacts.json': (
            '4009295246418/1232189371865', sorted(CONTACT_FRAME)),
    }
    require(name in expected, 'unknown recorded witness')
    width, boundary = expected[name]
    require(frac(exact['width']['width']) == frac(width), 'recorded witness width changed')
    require(sorted(map(tuple, exact['boundary_points'])) == boundary,
            'recorded witness contact set changed')
    if name == 'det2_four_contacts.json':
        require(frac(width) > Fraction(13, 4), 'four-contact width threshold failed')
    result['checks']['recorded_hollow_witness_and_contact_scope'] = True
    return result


def main() -> None:
    certificate_results: dict[str, Any] = {}
    paths = [PRIMARY_CERTIFICATE, FOUR_CONTACT_CERTIFICATE]
    for path in paths:
        data = load_json(path)
        result = validate_claim(path.name, data)
        result["mutation_guards"] = mutation_guards(data)
        certificate_results[path.name] = result

    try:
        validate_claim(FOUR_CONTACT_CERTIFICATE.name, load_json(PRIMARY_CERTIFICATE))
    except ValidationError:
        substituted_witness_rejected = True
    else:
        raise ValidationError('different self-consistent witness accepted for four-contact claim')
    report = {
        "status": "passed" if all(item["status"] == "passed" for item in certificate_results.values()) else "failed",
        "validator": "tests/replay_det2_cycle_independent.py",
        "imports_project_src": False,
        "arithmetic": "Python standard-library Fraction only",
        "certificates": certificate_results,
        "four_contact_certificate": "required_and_validated",
        "self_consistent_witness_substitution_rejected": substituted_witness_rejected,
        "limitations": [
            "This is an exact replay for the supplied reconstructed tetrahedron(s), not a search or a proof of global or local optimality.",
            "The finite width argument certifies each supplied body using its exact difference-coordinate basis bound; it does not establish a uniform bound for other bodies.",
            "The certificate chart assumes the four standard integral contacts 0, (2,1,1), e2, e3 in the stated row order.",
        ],
    }
    OUTPUT.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "status": report["status"],
        "certificates": {
            name: {
                "boundary_points": value["exact"]["boundary_points"],
                "width": value["exact"]["width"]["width"],
                "minimizers": value["exact"]["width"]["minimizing_directions_mod_sign"],
                "mutation_guards": list(value["mutation_guards"]),
            }
            for name, value in certificate_results.items()
        },
    }, indent=2))


if __name__ == "__main__":
    main()
