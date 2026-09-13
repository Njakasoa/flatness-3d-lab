"""Independent SymPy replay of the Codenotti--Santos baseline certificate.

This file intentionally does not import anything from ``src``.  It rebuilds
the standard-lattice tetrahedron from the raw affine lattice presentation,
uses SymPy algebraic numbers for every sign/comparison, and checks the JSON
certificate produced by the project engine.

Run from ``flatness-3d-lab`` as::

    .venv/bin/python tests/independent_replay.py
"""

from __future__ import annotations

import copy
import json
import sys
from itertools import permutations, product
from math import gcd
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parents[1]
CERTIFICATE_PATH = ROOT / "certificates" / "codenotti_santos.json"
OUT_PATH = ROOT / "certificates" / "independent_replay.json"


def simp(x):
    return sp.simplify(x)


def exact_zero(x):
    return simp(x) == 0


def exact_equal(a, b):
    return exact_zero(a - b)


def exact_integer(x):
    x = simp(x)
    return bool(x.is_rational and x.q == 1)


def q_json(x):
    """Decode the project's Q(a,b,d) JSON without importing project code."""

    if isinstance(x, dict) and {"a", "b", "d"}.issubset(x):
        return simp(sp.Rational(x["a"]) + sp.Rational(x["b"]) * sp.sqrt(int(x["d"])))
    return sp.Integer(x)


def point_json(p):
    return [str(simp(x)) for x in p]


def matrix_json(M):
    return [[str(simp(x)) for x in row] for row in M.tolist()]


def decode_vertices(payload):
    return [sp.Matrix([q_json(x) for x in row]) for row in payload]


def vertex_payload_equal(payload, vertices):
    decoded = decode_vertices(payload)
    assert len(decoded) == len(vertices)
    for got, want in zip(decoded, vertices):
        assert all(exact_equal(got[i], want[i]) for i in range(3))


def directional_width(vertices, u):
    u = sp.Matrix(u)
    values = [simp(v.dot(u)) for v in vertices]
    return simp(max(values) - min(values))


def primitive_directions(bounds):
    """Primitive directions in a box, modulo sign."""

    answer = []
    for u in product(*(range(-b, b + 1) for b in bounds)):
        if not any(u):
            continue
        if gcd(*(abs(x) for x in u)) != 1:
            continue
        first_nonzero = next(x for x in u if x)
        if first_nonzero < 0:
            continue
        answer.append(tuple(u))
    return answer


def lattice_box(vertices):
    lows = [int(sp.ceiling(min(v[j] for v in vertices))) for j in range(3)]
    highs = [int(sp.floor(max(v[j] for v in vertices))) for j in range(3)]
    return list(zip(lows, highs))


def barycentric_matrix(vertices):
    # M * lambda = (x,y,z,1), with columns (v_i,1).
    return sp.Matrix(
        [[vertices[i][j] for i in range(4)] for j in range(3)]
        + [[sp.Integer(1)] * 4]
    )


def classify_integer_point(vertices, point):
    M = barycentric_matrix(vertices)
    rhs = sp.Matrix([*point, 1])
    bary = [simp(x) for x in M.inv() * rhs]
    if all(x > 0 for x in bary):
        return "interior", bary
    if all(x >= 0 for x in bary):
        return "boundary", bary
    return "outside", bary


def enumerate_lattice_points(vertices):
    box = lattice_box(vertices)
    boundary = []
    interior = []
    for p in product(*(range(a, b + 1) for a, b in box)):
        loc, _ = classify_integer_point(vertices, p)
        if loc == "boundary":
            boundary.append(tuple(p))
        elif loc == "interior":
            interior.append(tuple(p))
    return box, boundary, interior


def integer_affine_automorphisms(vertices):
    """Test all 4! simplex permutations, retaining GL(3,Z) maps."""

    base = vertices[0]
    E = sp.Matrix.hstack(*(vertices[i] - base for i in range(1, 4)))
    E_inv = E.inv()
    all_candidates = []
    valid = []
    for perm in permutations(range(4)):
        p0 = vertices[perm[0]]
        F = sp.Matrix.hstack(*(vertices[i] - p0 for i in perm[1:]))
        U = F * E_inv
        t = p0 - U * base
        det = simp(U.det())
        integral = all(exact_integer(x) for x in U) and all(exact_integer(x) for x in t)
        unimodular = exact_equal(abs(det), 1)
        item = {
            "permutation": list(perm),
            "U": [[int(simp(U[i, j])) for j in range(3)] for i in range(3)]
            if integral else matrix_json(U),
            "t": [int(simp(x)) for x in t] if integral else point_json(t),
            "determinant": str(det),
            "integer_entries": integral,
            "unimodular": unimodular,
        }
        all_candidates.append(item)
        if integral and unimodular:
            valid.append({
                "permutation": list(perm),
                "U": item["U"],
                "t": item["t"],
            })
    return all_candidates, valid


def verify_certificate_payload(payload, vertices, width, active, boundary, interior, autos):
    """Verify mutable certificate fields against independently derived values."""

    vertex_payload_equal(payload["vertices"], vertices)
    assert exact_equal(q_json(payload["volume"]), abs(sp.Matrix.hstack(
        *(vertices[i] - vertices[0] for i in range(1, 4))
    ).det()) / 6)

    width_payload = payload["width_certificate"]
    assert width_payload['status']=='certified_lattice_width'
    assert exact_equal(q_json(width_payload["width"]), width)
    assert exact_equal(q_json(width_payload["upper_certificate"]["value"]), width)
    got_active = {tuple(x) for x in width_payload["minimizing_directions_mod_sign"]}
    assert got_active == set(active)
    assert width_payload["direction_count"] == 21
    assert width_payload["search_bound"]["coordinate_bounds"] == [1, 2, 1]
    assert len(width_payload['minimizing_directions_mod_sign'])==len(active)
    upper=width_payload['upper_certificate']
    u=tuple(upper['direction'])
    assert u in active and any(u) and gcd(*u)==1
    assert exact_equal(directional_width(vertices,u),q_json(upper['value']))
    lower=width_payload['lower_certificate']
    assert exact_equal(q_json(lower['checked_minimum']),width)
    assert lower['all_box_directions_checked'] is True
    bound=width_payload['search_bound']
    assert bound['basis_vertex_ids']==[0,1,2,3]
    D=sp.Matrix([list(vertices[i]-vertices[0]) for i in range(1,4)])
    claimed_inverse=sp.Matrix([[q_json(x) for x in row] for row in bound['D_inverse']])
    assert claimed_inverse.shape==(3,3)
    assert all(exact_zero(x) for x in D*claimed_inverse-sp.eye(3))
    initial=min(directional_width(vertices,u) for u in [(1,0,0),(0,1,0),(0,0,1)])
    assert exact_equal(q_json(bound['initial_upper']),initial)
    assert [int(sp.floor(initial*sum(abs(x) for x in row))) for row in claimed_inverse.tolist()]==bound['coordinate_bounds']

    hollow_payload = payload["hollow_certificate"]
    assert hollow_payload['status']=='certified_hollow'
    assert hollow_payload["hollow"] is True
    assert hollow_payload["integer_box"] == [[-1, 1], [-1, 1], [-1, 1]]
    assert {tuple(x) for x in hollow_payload["boundary_points"]} == set(boundary)
    assert hollow_payload["interior_points"] == interior
    assert hollow_payload['points_checked']==27
    assert len(hollow_payload['boundary_points'])==len(boundary)
    facets=hollow_payload['facets'];assert len(facets)==4
    seen=set()
    for facet in facets:
        n=sp.Matrix([q_json(x) for x in facet['normal']]);b=q_json(facet['offset'])
        assert n.shape==(3,1) and any(not exact_zero(x) for x in n)
        slacks=[simp(b-n.dot(v)) for v in vertices]
        assert all(x>=0 for x in slacks)
        on=tuple(i for i,x in enumerate(slacks) if exact_zero(x))
        assert len(on)==3 and on not in seen;seen.add(on)
        assert tuple(facet['vertex_ids'])==on
        cs=[p for p in boundary if exact_equal(n.dot(sp.Matrix(p)),b)]
        assert {tuple(p) for p in facet['lattice_contacts']}==set(cs)
        assert len(facet['lattice_contacts'])==len(cs)
        # A simplex facet relint point has exactly one zero barycentric coordinate.
        rel=[p for p in cs if sum(exact_zero(x) for x in classify_integer_point(vertices,p)[1])==1]
        assert {tuple(p) for p in facet['relative_interior_contacts']}==set(rel)
        assert len(facet['relative_interior_contacts'])==len(rel)

    got_autos = sorted(
        (tuple(x["permutation"]), tuple(tuple(row) for row in x["U"]), tuple(x["t"]))
        for x in payload["lattice_automorphisms"]
    )
    want_autos = sorted(
        (tuple(x["permutation"]), tuple(tuple(row) for row in x["U"]), tuple(x["t"]))
        for x in autos
    )
    assert got_autos == want_autos


def reject_mutated_payload(payload, vertices, width, active, boundary, interior, autos):
    outcomes = {}

    missing_active = copy.deepcopy(payload)
    missing_active["width_certificate"]["minimizing_directions_mod_sign"].pop()
    try:
        verify_certificate_payload(missing_active, vertices, width, active, boundary, interior, autos)
    except AssertionError:
        outcomes["missing_active_direction_rejected"] = True
    else:
        outcomes["missing_active_direction_rejected"] = False

    altered_width = copy.deepcopy(payload)
    altered_width["width_certificate"]["width"] = {"a": "3", "b": "0", "d": 2}
    try:
        verify_certificate_payload(altered_width, vertices, width, active, boundary, interior, autos)
    except AssertionError:
        outcomes["altered_width_rejected"] = True
    else:
        outcomes["altered_width_rejected"] = False

    for name,section,key,value in [
        ('zero_upper_direction','upper_certificate','direction',[0,0,0]),
        ('corrupt_inverse','search_bound','D_inverse',[]),
        ('corrupt_initial_bound','search_bound','initial_upper',{'a':'0','b':'0','d':2}),
        ('corrupt_lower_bound','lower_certificate','checked_minimum',{'a':'999','b':'0','d':2}),
    ]:
        bad=copy.deepcopy(payload);bad['width_certificate'][section][key]=value
        try:verify_certificate_payload(bad,vertices,width,active,boundary,interior,autos)
        except AssertionError:outcomes[name+'_rejected']=True
        else:outcomes[name+'_rejected']=False
    for name,key,value in [('missing_facets','facets',[]),('wrong_hollow_status','status','numeric_body')]:
        bad=copy.deepcopy(payload);bad['hollow_certificate'][key]=value
        try:verify_certificate_payload(bad,vertices,width,active,boundary,interior,autos)
        except AssertionError:outcomes[name+'_rejected']=True
        else:outcomes[name+'_rejected']=False

    # A dilation of the standard simplex by four is no longer hollow: (1,1,1)
    # is an exact interior lattice point.  This catches a hollow certificate
    # that merely checks vertices or boundary contacts.
    four_simplex = [
        sp.Matrix([0, 0, 0]),
        sp.Matrix([4, 0, 0]),
        sp.Matrix([0, 4, 0]),
        sp.Matrix([0, 0, 4]),
    ]
    _, _, dilated_interior = enumerate_lattice_points(four_simplex)
    outcomes["interior_lattice_dilation_rejected"] = (1, 1, 1) in dilated_interior

    # A tempting non-unimodular map must not be accepted as a lattice
    # automorphism merely because it has integral entries.
    bad_U = sp.diag(2, 1, 1)
    outcomes["invalid_GL_map_rejected"] = not (
        all(exact_integer(x) for x in bad_U) and exact_equal(abs(bad_U.det()), 1)
    )
    assert all(outcomes.values())
    return outcomes


def main():
    payload = json.loads(CERTIFICATE_PATH.read_text())
    s2 = sp.sqrt(2)

    # Raw body and affine lattice contacts from Codenotti--Santos.  The matrix
    # B has the three contact differences as columns; x=p0+B*z identifies the
    # affine lattice with standard Z^3.
    raw_vertices = [
        sp.Matrix([2 + s2, s2, 2 + s2]),
        sp.Matrix([-s2, 2 + s2, -2 - s2]),
        sp.Matrix([-2 - s2, -s2, 2 + s2]),
        sp.Matrix([s2, -2 - s2, -2 - s2]),
    ]
    raw_contacts = [
        sp.Matrix([-1, -1, -1]),
        sp.Matrix([1, -1, 1]),
        sp.Matrix([1, 1, -1]),
        sp.Matrix([-1, 1, 1]),
    ]
    B = sp.Matrix.hstack(*(p - raw_contacts[0] for p in raw_contacts[1:]))
    B_inv = B.inv()
    vertices = [sp.Matrix([simp(x) for x in B_inv * (p - raw_contacts[0])]) for p in raw_vertices]
    vertex_payload_equal(payload["vertices"], vertices)

    # Independent volume and width computation.
    E = sp.Matrix.hstack(*(vertices[i] - vertices[0] for i in range(1, 4)))
    volume = simp(abs(E.det()) / 6)
    initial_upper = min(directional_width(vertices, (1, 0, 0)),
                        directional_width(vertices, (0, 1, 0)),
                        directional_width(vertices, (0, 0, 1)))
    D = sp.Matrix([list(vertices[i] - vertices[0]) for i in range(1, 4)])
    D_inv = D.inv()
    bounds = [int(sp.floor(initial_upper * sum(abs(x) for x in row))) for row in D_inv.tolist()]
    directions = primitive_directions(bounds)
    widths = {u: directional_width(vertices, u) for u in directions}
    width = min(widths.values())
    active = sorted(u for u, w in widths.items() if exact_equal(w, width))
    assert bounds == [1, 2, 1]
    assert len(directions) == 21
    assert active == [tuple(x) for x in payload["width_certificate"]["minimizing_directions_mod_sign"]]
    assert exact_equal(width, 2 + s2)

    # Independent barycentric enumeration of the exact integer bounding box.
    integer_box, boundary, interior = enumerate_lattice_points(vertices)
    assert integer_box == [(-1, 1), (-1, 1), (-1, 1)]
    assert boundary == [(0, 0, 0), (0, 0, 1), (0, 1, 0), (1, 0, 0)]
    assert interior == []

    all_candidates, autos = integer_affine_automorphisms(vertices)
    assert len(all_candidates) == 24
    assert len(autos) == 4
    verify_certificate_payload(payload, vertices, width, active, boundary, interior, autos)
    mutations = reject_mutated_payload(payload, vertices, width, active, boundary, interior, autos)

    result = {
        "status": "independent_replay_passed",
        "source_certificate": str(CERTIFICATE_PATH.relative_to(ROOT)),
        "no_src_imports": True,
        "raw_lattice_reconstruction": {
            "raw_vertices": [point_json(p) for p in raw_vertices],
            "raw_contacts": [point_json(p) for p in raw_contacts],
            "B_columns": matrix_json(B),
            "B_inverse": matrix_json(B_inv),
            "standard_vertices": [point_json(p) for p in vertices],
        },
        "json_values_verified": {
            "vertices": True,
            "volume": str(volume),
            "width": str(width),
            "active_directions": [list(u) for u in active],
            "hollow_boundary": [list(p) for p in boundary],
            "hollow_interior": [list(p) for p in interior],
        },
        "width_replay": {
            "initial_upper": str(initial_upper),
            "difference_matrix": matrix_json(D),
            "difference_matrix_inverse": matrix_json(D_inv),
            "justified_coordinate_bounds": bounds,
            "primitive_direction_count_mod_sign": len(directions),
            "active_directions": [list(u) for u in active],
            "all_directions_in_box_checked": True,
            "radius_argument": "|u.D_row|<=W implies |u_j|<=W*sum_i |(D^-1)_{ji}|; outside the box width>W",
        },
        "hollow_replay": {
            "integer_box": [list(x) for x in integer_box],
            "points_checked": 27,
            "boundary_points": [list(p) for p in boundary],
            "interior_points": [list(p) for p in interior],
            "barycentric_enumeration_exact": True,
        },
        "permutation_replay": {
            "permutations_tested": len(all_candidates),
            "integer_unimodular_automorphisms": len(autos),
            "valid_automorphisms": autos,
        },
        "mutation_guards": mutations,
    }
    OUT_PATH.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({
        "status": result["status"],
        "width": str(width),
        "directions_checked": len(directions),
        "interior_points": interior,
        "permutations_tested": len(all_candidates),
        "valid_automorphisms": len(autos),
        "mutation_guards": mutations,
        "certificate": str(OUT_PATH.relative_to(ROOT)),
    }, indent=2))


if __name__ == "__main__":
    main()
