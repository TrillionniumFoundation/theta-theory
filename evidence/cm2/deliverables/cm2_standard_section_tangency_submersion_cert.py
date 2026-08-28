#!/usr/bin/env python3
"""Exact margin certificate for standard-section circle tangencies.

For an oriented ray with transverse target displacement

    w = u_perp dot (a - q),

the target-circle discriminant is ``Delta = R^2 - w^2``.  Since
``partial_phi u_perp = -u``, at a forward tangency

    |partial_phi Delta| = 2 R * ell,
    ell = u dot (a - q) > 0.

This script certifies the strict numerical lower margin for the rational
two-disk pilot.  The displayed differential identity is exact algebra; the
only numerical input is the already frozen no-overlap/free-flight bound.

This is a one-step event-submersion certificate.  It is not a global DQ,
occurrence-matching, PPE, or CM2 certificate.
"""

from fractions import Fraction


R_GRAY = Fraction(9, 25)
R_WHITE = Fraction(4, 25)
EPS = Fraction(1, 200)


def main() -> None:
    # The shortest possible solid-boundary gap is the gray--white diagonal
    # gap.  R_GRAY + R_WHITE + EPS = 21/40.
    assert R_GRAY + R_WHITE + EPS == Fraction(21, 40)

    # Prove 1/sqrt(2) > 0.7071 by squaring positive rational numbers.
    rational_diagonal_lower = Fraction(7071, 10000)
    assert rational_diagonal_lower**2 < Fraction(1, 2)

    # Hence tau_min > 0.7071 - 0.525 = 0.1821.
    tau_lower = rational_diagonal_lower - (R_GRAY + R_WHITE + EPS)
    assert tau_lower == Fraction(1821, 10000)

    # At tangency, |partial_phi Delta| = 2 R ell.  Use the smaller radius.
    submersion_lower = 2 * min(R_GRAY, R_WHITE) * tau_lower
    assert submersion_lower == Fraction(1821, 31250)
    assert submersion_lower == Fraction(58272, 1_000_000)

    print("STANDARD_SECTION_TANGENCY_SUBMERSION: CERTIFIED")
    print("  R_min=4/25")
    print("  tau_min>1821/10000")
    print("  identity=|partial_phi Delta|=2*R*ell")
    print("  |partial_phi Delta|>1821/31250=0.058272")
    print("GLOBAL_EVENT_DQ_AND_MATCHING: NOT CERTIFIED")


if __name__ == "__main__":
    main()
