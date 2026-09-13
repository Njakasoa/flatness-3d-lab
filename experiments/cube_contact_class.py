"""Bounded numerical audit of the eight-facet cube-contact class.

The model is written in centered coordinates.  The unit cube is
[-1/2,1/2]^3 and the eight supporting planes are

    (s_1 a_1, s_2 a_2, s_3 a_3) . x <= 1/2,

where s_i in {-1,1}, a_i > 0 and a_1+a_2+a_3=1.  The ambient lattice is
the translated lattice (Z+1/2)^3; lattice-width directions are still the
integer vectors Z^3.

This file is deliberately exploratory.  It enumerates all vertices of the
half-space intersection, checks the complete primitive direction set with
l1 norm at most three, and performs a small Dirichlet/differential-evolution
search.  No floating-point output here is a proof certificate.
"""

from __future__ import annotations

import argparse
import itertools
import json
import math
from pathlib import Path

import numpy as np


SIGNS = np.array(list(itertools.product((-1.0, 1.0), repeat=3)), dtype=float)
TRIPLES = list(itertools.combinations(range(8), 3))


def primitive_directions(max_l1: int = 3) -> np.ndarray:
    """Return primitive integer directions modulo sign and in first-octant order."""

    ans = []
    for u in itertools.product(range(-max_l1, max_l1 + 1), repeat=3):
        if not any(u) or sum(abs(x) for x in u) > max_l1:
            continue
        if math.gcd(*u) != 1:
            continue
        first = next(x for x in u if x)
        if first < 0:
            continue
        ans.append(u)
    return np.asarray(ans, dtype=float)


DIRS = primitive_directions(3)


def softmax_rows(logits: np.ndarray) -> np.ndarray:
    """Convert 8 x 3 unconstrained parameters to positive row sums one."""

    z = np.asarray(logits, dtype=float).reshape(8, 3)
    z = z - z.max(axis=1, keepdims=True)
    e = np.exp(z)
    return e / e.sum(axis=1, keepdims=True)


def vertices(weights: np.ndarray, tolerance: float = 2e-9) -> np.ndarray:
    """Enumerate feasible triple intersections of the eight facet planes."""

    weights = np.asarray(weights, dtype=float).reshape(8, 3)
    normals = SIGNS * weights
    values = np.full(8, 0.5)
    found = []
    for ids in TRIPLES:
        matrix = normals[list(ids)]
        if abs(np.linalg.det(matrix)) <= 1e-11:
            continue
        point = np.linalg.solve(matrix, values[list(ids)])
        if np.all(normals @ point <= values + tolerance):
            found.append(point)
    unique = []
    for point in found:
        if not any(np.linalg.norm(point - other, ord=np.inf) <= 5e-8 for other in unique):
            unique.append(point)
    if not unique:
        raise RuntimeError("bounded positive-orthant model produced no vertices")
    return np.asarray(unique)


def directional_widths(weights: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Return widths for all 25 directions and the vertex array."""

    v = vertices(weights)
    values = v @ DIRS.T
    return np.ptp(values, axis=0), v


def summarize(weights: np.ndarray) -> dict:
    widths, v = directional_widths(weights)
    i = int(np.argmin(widths))
    axis = widths[np.sum(np.abs(DIRS), axis=1) == 1]
    return {
        "weights": np.asarray(weights).tolist(),
        "vertices": v.tolist(),
        "vertex_count": int(len(v)),
        "directional_widths": [
            {"direction": [int(x) for x in u], "width": float(w)}
            for u, w in zip(DIRS, widths)
        ],
        "minimum_width_over_l1_le_3": float(widths[i]),
        "minimizing_direction": [int(x) for x in DIRS[i]],
        "axis_widths": [float(x) for x in axis],
    }


def random_search(rng: np.random.Generator, samples: int) -> dict:
    best = None
    for alpha in (1.0, 0.3, 0.1):
        for _ in range(samples):
            weights = rng.dirichlet(np.full(3, alpha), size=8)
            row = summarize(weights)
            if best is None or row["minimum_width_over_l1_le_3"] > best["minimum_width_over_l1_le_3"]:
                best = row | {"dirichlet_alpha": alpha}
    assert best is not None
    return best


def bounded_global_search(seed: int, generations: int, population: int) -> dict | None:
    """A deliberately small global search; absent SciPy, return no result."""

    try:
        from scipy.optimize import differential_evolution
    except ImportError:
        return None

    def objective(logits: np.ndarray) -> float:
        weights = softmax_rows(logits)
        try:
            widths, _ = directional_widths(weights)
        except (FloatingPointError, np.linalg.LinAlgError, RuntimeError):
            return 1e4
        return -float(np.min(widths))

    result = differential_evolution(
        objective,
        [(-7.0, 7.0)] * 24,
        seed=seed,
        popsize=population,
        maxiter=generations,
        polish=False,
        updating="immediate",
        workers=1,
        tol=1e-5,
    )
    row = summarize(softmax_rows(result.x))
    row.update(
        {
            "seed": seed,
            "generations": generations,
            "population": population,
            "objective_evaluations": int(result.nfev),
            "optimizer_status": str(result.message),
        }
    )
    return row


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--samples", type=int, default=250)
    parser.add_argument("--generations", type=int, default=25)
    parser.add_argument("--population", type=int, default=6)
    parser.add_argument("--seed", type=int, default=20260913)
    parser.add_argument("--output", default="results/cube_contact_class.json")
    args = parser.parse_args()

    rng = np.random.default_rng(args.seed)
    uniform = np.full((8, 3), 1.0 / 3.0)
    uniform_row = summarize(uniform)
    random_row = random_search(rng, args.samples)
    optimized_row = bounded_global_search(args.seed, args.generations, args.population)
    candidates = [uniform_row, random_row]
    if optimized_row is not None:
        candidates.append(optimized_row)
    best = max(candidates, key=lambda x: x["minimum_width_over_l1_le_3"])

    result = {
        "status": "numeric_exploration_only",
        "model": {
            "centered_cube": "[-1/2,1/2]^3",
            "ambient_lattice": "(Z+1/2)^3",
            "facet_normal": "(s1*a1,s2*a2,s3*a3), a_i>0, sum(a_i)=1",
            "facet_support": "1/2",
            "boundedness": "strictly positive weights in all eight orthants",
        },
        "direction_set": {
            "max_l1": 3,
            "count_modulo_sign": int(len(DIRS)),
            "directions": [[int(x) for x in u] for u in DIRS],
            "completeness_reason": "K contains the unit cube, so width(K,u)>=||u||_1; if width(K)<4, a minimizing primitive u has ||u||_1<=3.",
        },
        "uniform_reference": uniform_row,
        "random_search": {
            "seed": args.seed,
            "samples_per_dirichlet_alpha": args.samples,
            "alphas": [1.0, 0.3, 0.1],
            "best": random_row,
        },
        "bounded_global_search": optimized_row,
        "best_observed": best,
        "limits": [
            "All vertices and widths use floating-point arithmetic.",
            "The direction set is complete only under the stated width<4 hypothesis.",
            "Sampling and optimization do not prove a universal width bound.",
            "The axis-width route is the three-plank packed-convex-set conjecture after bounding-box normalization.",
        ],
    }
    path = Path(args.output)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({
        "status": result["status"],
        "direction_count": len(DIRS),
        "uniform_min": uniform_row["minimum_width_over_l1_le_3"],
        "random_best": random_row["minimum_width_over_l1_le_3"],
        "optimizer_best": None if optimized_row is None else optimized_row["minimum_width_over_l1_le_3"],
        "best_observed": best["minimum_width_over_l1_le_3"],
        "best_direction": best["minimizing_direction"],
    }, indent=2))


if __name__ == "__main__":
    main()
