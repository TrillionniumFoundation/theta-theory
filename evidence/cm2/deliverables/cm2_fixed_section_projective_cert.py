#!/usr/bin/env python3
"""Exact projective benchmark certificate for the fixed-section pilot.

This script certifies only the algebraic two-map benchmark.  It does not
claim that the two maps are return branches based at one billiard Markov
vertex; that connector remains a separate geometric certificate.
"""

from __future__ import annotations

from fractions import Fraction

from cm2_fixed_section_qnl_cert import Qsqrt2


def sign(value: Qsqrt2) -> int:
    """Return the exact sign of r + s*sqrt(2)."""

    r = value.rational
    s = value.radical
    if r == 0 and s == 0:
        return 0
    if r >= 0 and s >= 0:
        return 1
    if r <= 0 and s <= 0:
        return -1
    comparison = r * r - 2 * s * s
    if comparison == 0:
        return 0
    if r > 0 and s < 0:
        return 1 if comparison > 0 else -1
    return -1 if comparison > 0 else 1


def assert_positive(value: Qsqrt2, name: str) -> None:
    if sign(value) <= 0:
        raise AssertionError(f"{name} is not strictly positive: {value}")


def assert_less(left: Qsqrt2, right: Qsqrt2, name: str) -> None:
    assert_positive(right - left, name)


def projective_numerator(
    matrix: tuple[Qsqrt2, Qsqrt2, Qsqrt2], z: Fraction
) -> Qsqrt2:
    a, _, c = matrix
    return c + a * z


def projective_denominator(
    matrix: tuple[Qsqrt2, Qsqrt2, Qsqrt2], z: Fraction
) -> Qsqrt2:
    a, b, _ = matrix
    return a + b * z


def compare_projective(
    matrix: tuple[Qsqrt2, Qsqrt2, Qsqrt2],
    z: Fraction,
    target: Fraction,
    name: str,
) -> int:
    """Compare Phi(z) with target, after certifying a positive denominator."""

    denominator = projective_denominator(matrix, z)
    assert_positive(denominator, f"{name}: denominator")
    difference_numerator = (
        projective_numerator(matrix, z) - target * denominator
    )
    result = sign(difference_numerator)
    if result == 0:
        raise AssertionError(f"{name}: equality is not a strict margin")
    return result


def main() -> None:
    one = Qsqrt2(1)
    a_w = Qsqrt2(Fraction(661, 36), Fraction(-325, 36))
    b_w = Qsqrt2(Fraction(859, 100), Fraction(-11, 2))
    c_w = Qsqrt2(Fraction(15625, 324), Fraction(-625, 81))
    white = (a_w, b_w, c_w)

    a_g = Qsqrt2(Fraction(431, 81))
    b_g = Qsqrt2(Fraction(224, 225))
    c_g = Qsqrt2(Fraction(20000, 729))
    gray = (a_g, b_g, c_g)

    assert a_w * a_w - b_w * c_w == one
    assert a_g * a_g - b_g * c_g == one

    for label, matrix in (("g", gray), ("w", white)):
        denominator_5 = projective_denominator(matrix, Fraction(5))
        denominator_7 = projective_denominator(matrix, Fraction(7))
        assert_less(Qsqrt2(9), denominator_5, f"{label}: denominator > 9")
        assert_less(denominator_7, Qsqrt2(13), f"{label}: denominator < 13")

    assert compare_projective(gray, Fraction(5), Fraction(5), "Phi_g(5)") > 0
    assert (
        compare_projective(gray, Fraction(7), Fraction(11, 2), "Phi_g(7)")
        < 0
    )
    assert (
        compare_projective(white, Fraction(5), Fraction(13, 2), "Phi_w(5)")
        > 0
    )
    assert compare_projective(white, Fraction(7), Fraction(7), "Phi_w(7)") < 0

    gap_numerator = (
        projective_numerator(white, Fraction(5))
        * projective_denominator(gray, Fraction(7))
        - projective_numerator(gray, Fraction(7))
        * projective_denominator(white, Fraction(5))
        - projective_denominator(white, Fraction(5))
        * projective_denominator(gray, Fraction(7))
    )
    assert_positive(gap_numerator, "first-level projective gap > 1")

    twisting_margin = c_w * b_g - c_g * b_w
    assert_less(
        Qsqrt2(Fraction(1040, 81)),
        twisting_margin,
        "eigenslope twisting margin",
    )

    cross_margin = 3969 * c_w - 160000 * b_w
    assert_less(
        Qsqrt2(Fraction(24525, 4)),
        cross_margin,
        "full algebraic twisting margin",
    )

    print("fixed-section Bernoulli projective benchmark: CERTIFIED")
    print("Phi_g([5,7]) is contained in (5,11/2)")
    print("Phi_w([5,7]) is contained in (13/2,7)")
    print("both projective denominators are in (9,13)")
    print("therefore 1/169 < Phi_i' < 1/81")
    print("the first-level image gap is greater than 1")
    print(f"eigenslope_twisting_margin={twisting_margin}")
    print(f"full_algebraic_twisting_margin={cross_margin}")
    print("DYNAMICAL COMMON-VERTEX CONNECTOR: NOT CERTIFIED")


if __name__ == "__main__":
    main()
