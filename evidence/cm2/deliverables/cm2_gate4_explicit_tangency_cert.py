#!/usr/bin/env python3
"""Exact Q(sqrt(610)) certificate for the Gate-4 tangency witness.

The script verifies the explicit gray-to-white physical tangency used in
``cm2-gate4-reversibility-bridge-2026-07-15.md``.  It is deliberately only a
geometry/coarea certificate.  It does not certify an eventwise reverse
identity, a same-occurrence q, or bidirectional recovery.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from math import sqrt


@dataclass(frozen=True)
class Q610:
    """The exact number a+b*sqrt(610), with rational a,b."""

    a: Fraction
    b: Fraction = Fraction(0)

    @staticmethod
    def coerce(value: Q610 | Fraction | int) -> Q610:
        return value if isinstance(value, Q610) else Q610(Fraction(value))

    def __add__(self, other: Q610 | Fraction | int) -> Q610:
        other = self.coerce(other)
        return Q610(self.a + other.a, self.b + other.b)

    __radd__ = __add__

    def __neg__(self) -> Q610:
        return Q610(-self.a, -self.b)

    def __sub__(self, other: Q610 | Fraction | int) -> Q610:
        return self + (-self.coerce(other))

    def __rsub__(self, other: Q610 | Fraction | int) -> Q610:
        return self.coerce(other) - self

    def __mul__(self, other: Q610 | Fraction | int) -> Q610:
        other = self.coerce(other)
        return Q610(
            self.a * other.a + 610 * self.b * other.b,
            self.a * other.b + self.b * other.a,
        )

    __rmul__ = __mul__

    def __truediv__(self, other: Fraction | int) -> Q610:
        other = Fraction(other)
        return Q610(self.a / other, self.b / other)

    def sign(self) -> int:
        """Return the exact sign using one rational square comparison."""

        if self.b == 0:
            return (self.a > 0) - (self.a < 0)
        if self.a == 0:
            return (self.b > 0) - (self.b < 0)
        if self.a > 0 and self.b > 0:
            return 1
        if self.a < 0 and self.b < 0:
            return -1
        radical_square = 610 * self.b * self.b
        rational_square = self.a * self.a
        if radical_square == rational_square:
            return 0
        radical_dominates = radical_square > rational_square
        if self.b > 0:
            return 1 if radical_dominates else -1
        return -1 if radical_dominates else 1

    def __lt__(self, other: Q610 | Fraction | int) -> bool:
        return (self - other).sign() < 0

    def __gt__(self, other: Q610 | Fraction | int) -> bool:
        return (self - other).sign() > 0

    def decimal(self) -> float:
        return float(self.a) + float(self.b) * sqrt(610)


def main() -> None:
    radical = Q610(Fraction(0), Fraction(1))
    radius_gray = Fraction(9, 25)
    radius_white = Fraction(4, 25)
    qx = radius_gray
    dx, dy = Fraction(7, 50), Fraction(1, 2)
    ell = radical / 50
    ux = (200 + 7 * radical) / 674
    uy = (25 * radical - 56) / 674

    assert ux * ux + uy * uy == Q610(Fraction(1))
    assert ux * dx + uy * dy == ell
    assert (-uy) * dx + ux * dy == Q610(radius_white)
    assert ux > 0 and uy > 0 and ell > 0

    # The only nearby competing gray lift is (1,0).  Its perpendicular
    # distance to the line is (16/25)u_y and its projection lies inside the
    # segment.  The strict distance is larger than the gray radius.
    projection_g10 = Fraction(16, 25) * ux
    distance_g10 = Fraction(16, 25) * uy
    assert projection_g10 > 0 and ell - projection_g10 > 0
    assert distance_g10 > radius_gray

    # Exact endpoint box.  Its coordinate gaps exclude all other gray/white
    # lifts; the source gray disk is not re-entered because u_x>0 at its
    # rightmost point.
    x_contact = Q610(qx) + ell * ux
    y_contact = ell * uy
    assert Q610(Fraction(9, 25)) < x_contact < Fraction(317, 500)
    assert Q610(0) < y_contact < Fraction(103, 250)
    assert 1 - y_contact > radius_gray
    assert Fraction(1, 2) > radius_white
    assert Fraction(3, 2) - x_contact > radius_white

    partial_s = 2 * radius_white * uy
    partial_phi = 2 * radius_white * ell
    expected_partial_s = 4 * (25 * radical - 56) / 8425
    expected_partial_phi = 4 * radical / 625
    assert partial_s == expected_partial_s and partial_s > 0
    assert partial_phi == expected_partial_phi and partial_phi > 0

    print("GATE4_EXPLICIT_GRAY_WHITE_TANGENCY: CERTIFIED")
    print(f"  u=({ux.decimal():.15f},{uy.decimal():.15f})")
    print(f"  flight_to_contact={ell.decimal():.15f}")
    print(f"  gray_G10_line_clearance={distance_g10.decimal():.15f}>9/25")
    print(f"  partial_s_H={partial_s.decimal():.15f}>0")
    print(f"  partial_phi_H={partial_phi.decimal():.15f}>0")
    print("EVENTWISE_SAME_OCCURRENCE_IDENTITY: NOT CERTIFIED")
    print("SINGLE_CHARGE_q_MAX: NOT CERTIFIED")
    print("BIDIRECTIONAL_RECOVERY_MOMENTS: NOT CERTIFIED")


if __name__ == "__main__":
    main()
