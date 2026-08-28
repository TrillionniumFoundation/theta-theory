#!/usr/bin/env python3
"""Exact rational certificate for the fixed-section two-disk CM2 pilot."""

from decimal import Decimal, getcontext
from fractions import Fraction


getcontext().prec = 50

R_BAR = Fraction(9, 25)     # 0.36
R_WHITE = Fraction(4, 25)   # 0.16
EPS = Fraction(1, 200)      # 0.005


def dec(x: Fraction) -> Decimal:
    return Decimal(x.numerator) / Decimal(x.denominator)


def main() -> None:
    # Stenlund's four elementary fixed-section geometry inequalities.
    assert max(R_BAR, R_WHITE + EPS) < Fraction(1, 2)
    # x < 1/sqrt(2) iff x^2 < 1/2 for x > 0.
    assert (R_BAR + R_WHITE + EPS) ** 2 < Fraction(1, 2)
    # R_bar >= 1/(2 sqrt(2)) iff R_bar^2 >= 1/8.
    assert R_BAR**2 >= Fraction(1, 8)
    assert R_BAR + R_WHITE - EPS >= Fraction(1, 2)

    # For R_bar=9/25,
    # L(R_bar)=(5 sqrt(7))/32-63/800.  To prove L>33/200,
    # it is enough to prove 25 sqrt(7)>39, hence 625*7>39^2.
    assert 625 * 7 > 39**2
    # The sharper claimed free-zone slack is > 0.16964.  After collecting
    # rational terms this is sqrt(7) > 41339/15625.
    sharper_threshold = Fraction(41339, 15625)
    assert Fraction(7) - sharper_threshold**2 == Fraction(71454, 244140625)
    assert Fraction(7) > sharper_threshold**2

    sqrt2 = Decimal(2).sqrt()
    sqrt7 = Decimal(7).sqrt()
    free_threshold = Decimal(5) * sqrt7 / Decimal(32) - Decimal(63) / Decimal(800)
    margins = {
        "boundary_margin": Decimal("0.5") - max(dec(R_BAR), dec(R_WHITE + EPS)),
        "diagonal_margin": Decimal(1) / sqrt2 - dec(R_BAR + R_WHITE + EPS),
        "finite_horizon_lower_margin": dec(R_BAR) - Decimal(1) / (Decimal(2) * sqrt2),
        "blocking_margin": dec(R_BAR + R_WHITE - EPS) - Decimal("0.5"),
        "free_zone_margin": free_threshold - dec(R_WHITE + EPS),
    }
    print("fixed-section two-disk geometry: CERTIFIED")
    for name, value in margins.items():
        print(f"{name}={value}")


if __name__ == "__main__":
    main()
