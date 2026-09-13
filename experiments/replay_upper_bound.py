#!/usr/bin/env python3
"""Replay the numerical part of Averkov--Codenotti--Macchia--Santos.

This is a small, dependency-free certificate for the inequalities in Theorem
5.2 and Theorem 5.4 of arXiv:1907.06199v2.  It does not enumerate bodies or
prove any of the geometric input inequalities.  Instead, it records those
inequalities symbolically and evaluates their radical constants with rational
interval arithmetic.  Every displayed decimal conclusion is therefore checked
against strict rational enclosures, rather than against an unqualified float.

Running this file writes ``results/upper_bound.json`` next to this directory.
"""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal, getcontext
from fractions import Fraction
import json
from pathlib import Path


getcontext().prec = 80


@dataclass(frozen=True)
class Interval:
    """An open rational interval known to contain one real number."""

    lo: Fraction
    hi: Fraction

    def __post_init__(self) -> None:
        if not self.lo < self.hi:
            raise ValueError("interval endpoints must satisfy lo < hi")

    @classmethod
    def point(cls, value: Fraction | int) -> "Interval":
        value = Fraction(value)
        # A point interval is useful for constants; widen it by one ulp so the
        # invariant remains an open interval.
        return cls(value - Fraction(1, 10**30), value + Fraction(1, 10**30))

    def __add__(self, other: "Interval") -> "Interval":
        return Interval(self.lo + other.lo, self.hi + other.hi)

    def __radd__(self, other: "Interval") -> "Interval":
        return self + other

    def __sub__(self, other: "Interval") -> "Interval":
        return Interval(self.lo - other.hi, self.hi - other.lo)

    def __rsub__(self, other: "Interval") -> "Interval":
        return Interval(Fraction(other) - self.hi, Fraction(other) - self.lo)

    def __mul__(self, other: "Interval") -> "Interval":
        values = (
            self.lo * other.lo,
            self.lo * other.hi,
            self.hi * other.lo,
            self.hi * other.hi,
        )
        return Interval(min(values), max(values))

    def __rmul__(self, other: "Interval") -> "Interval":
        return self * Interval.point(other)

    def reciprocal(self) -> "Interval":
        if self.lo <= 0 <= self.hi:
            raise ValueError("reciprocal interval crosses zero")
        return Interval(1 / self.hi, 1 / self.lo) if self.lo > 0 else Interval(1 / self.hi, 1 / self.lo)

    def __truediv__(self, other: "Interval") -> "Interval":
        return self * other.reciprocal()

    def power(self, exponent: int) -> "Interval":
        if exponent < 0:
            return self.power(-exponent).reciprocal()
        result = Interval.point(1)
        for _ in range(exponent):
            result = result * self
        return result

    def as_json(self) -> dict[str, str]:
        return {"lo": str(self.lo), "hi": str(self.hi)}


def decimal_value(value: Fraction, places: int = 18) -> str:
    """Render a rational endpoint without going through binary float."""

    decimal = Decimal(value.numerator) / Decimal(value.denominator)
    return f"{decimal:.{places}f}"


def describe(interval: Interval) -> dict[str, object]:
    return {
        "rational_interval": interval.as_json(),
        "decimal_interval": {
            "lo": decimal_value(interval.lo),
            "hi": decimal_value(interval.hi),
        },
    }


def main() -> None:
    # These are deliberately rational enclosures.  The assertions below prove
    # the defining square/cube inequalities with integer arithmetic.
    sqrt2 = Interval(
        Fraction(1414213562373095, 10**15),
        Fraction(1414213562373096, 10**15),
    )
    sqrt3 = Interval(
        Fraction(1732050807568877, 10**15),
        Fraction(1732050807568878, 10**15),
    )
    cbrt_three_quarters = Interval(
        Fraction(908560296416069, 10**15),
        Fraction(908560296416070, 10**15),
    )
    assert sqrt2.lo**2 < 2 < sqrt2.hi**2
    assert sqrt3.lo**2 < 3 < sqrt3.hi**2
    assert cbrt_three_quarters.lo**3 < Fraction(3, 4) < cbrt_three_quarters.hi**3

    one = Interval.point(1)
    two = Interval.point(2)
    w0 = two + sqrt2                         # 2 + sqrt(2)
    A = one + two / sqrt3                    # 1 + 2/sqrt(3)
    alpha = one - A / w0                     # 1 - A/(2+sqrt(2))
    width_upper = A + two * cbrt_three_quarters
    volume_lower = w0.power(3) / Interval.point(15)
    volume_upper = one / alpha.power(3)
    empty_polytope_upper = one / alpha.power(2)
    tetrahedron_upper = Interval.point(Fraction(2, 5)) / alpha.power(2)

    # Strict decimal roundings claimed in the paper and the integer-volume
    # roundings used in Theorem 5.4.
    assert w0.lo > Fraction(3414, 1000)
    assert width_upper.hi < Fraction(3972, 1000)
    assert volume_lower.lo > Fraction(2653, 1000)
    assert volume_upper.hi < Fraction(19919, 1000)
    six_empty = empty_polytope_upper * Interval.point(6)
    six_tetrahedron = tetrahedron_upper * Interval.point(6)
    assert six_empty.hi < 45       # 6 vol(P) is an integer, hence <= 44.
    assert six_tetrahedron.hi < 18  # 6 vol(P) is an integer, hence <= 17.

    results = {
        "source": {
            "title": "A local maximizer for lattice width of 3-dimensional hollow bodies",
            "authors": "G. Averkov, G. Codenotti, A. Macchia, F. Santos",
            "arxiv": "1907.06199v2",
            "url": "https://arxiv.org/abs/1907.06199",
            "scope": "Theorem 5.2 is stated for a width maximizer; the same algebraic bounds use only w(K) >= 2+sqrt(2) once that hypothesis is available.",
        },
        "radical_certificates": {
            "sqrt2": describe(sqrt2),
            "sqrt3": describe(sqrt3),
            "cuberoot_3_over_4": describe(cbrt_three_quarters),
        },
        "constants": {
            "w0 = 2 + sqrt(2)": describe(w0),
            "A = 1 + 2/sqrt(3)": describe(A),
            "alpha = 1 - A/w0": describe(alpha),
        },
        "theorem_5_2_replay": {
            "input_inequalities": [
                "1 <= (1+2/sqrt(3))*mu_1(K) + lambda_1(K-K)",
                "lambda_1(K-K)^3 * vol(K-K) <= 8",
                "4 <= 3*mu_1(K)^3*vol(K-K)",
                "8*vol(K) <= vol(K-K)",
                "vol(K-K) <= 20*vol(K)",
                "lambda_1(K-K) >= alpha when w(K) >= w0",
            ],
            "width_upper_expression": "1 + 2/sqrt(3) + 2*(3/4)^(1/3)",
            "width_upper": describe(width_upper),
            "width_lower_expression": "2 + sqrt(2)",
            "width_lower": describe(w0),
            "volume_lower_expression": "(2 + sqrt(2))^3 / 15",
            "volume_lower": describe(volume_lower),
            "volume_upper_expression": "(1 - (1+2/sqrt(3))/(2+sqrt(2)))^(-3)",
            "volume_upper": describe(volume_upper),
            "rounded_claim": {
                "width": "3.414 < w(K) < 3.972",
                "volume": "2.653 < vol(K) < 19.919",
            },
        },
        "theorem_5_4_replay": {
            "empty_3d_expression": "alpha^(-2)",
            "empty_3d_bound_before_integer_rounding": describe(empty_polytope_upper),
            "empty_3d_normalized_bound": "22/3",
            "tetrahedron_expression": "(2/5)*alpha^(-2)",
            "tetrahedron_bound_before_integer_rounding": describe(tetrahedron_upper),
            "tetrahedron_normalized_bound": "17/6",
            "integer_rounding_checks": {
                "6*empty_3d_upper": describe(six_empty),
                "6*tetrahedron_upper": describe(six_tetrahedron),
            },
        },
        "slack_against_paper_decimals": {
            "width_lower_rounding_down": decimal_value(w0.lo - Fraction(3414, 1000)),
            "width_upper_rounding_up": decimal_value(Fraction(3972, 1000) - width_upper.hi),
            "volume_lower_rounding_down": decimal_value(volume_lower.lo - Fraction(2653, 1000)),
            "volume_upper_rounding_up": decimal_value(Fraction(19919, 1000) - volume_upper.hi),
        },
        "warning": "This replay certifies only the arithmetic consequences of the cited geometric inequalities. It is not a proof of Mahler, covering-minima, Minkowski, Rogers-Shephard, Brunn-Minkowski, Howe, Lovasz, or existence of a global maximizer.",
    }

    output_path = Path(__file__).resolve().parents[1] / "results" / "upper_bound.json"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(results, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(output_path.relative_to(Path(__file__).resolve().parents[1]))
    print(json.dumps({
        "width_upper": describe(width_upper)["decimal_interval"],
        "volume_lower": describe(volume_lower)["decimal_interval"],
        "volume_upper": describe(volume_upper)["decimal_interval"],
        "empty_3d_bound": describe(empty_polytope_upper)["decimal_interval"],
        "tetrahedron_bound": describe(tetrahedron_upper)["decimal_interval"],
    }, indent=2))


if __name__ == "__main__":
    main()
