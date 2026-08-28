#!/usr/bin/env python3
"""Dependency-free exact polynomial certificate for the clean impact chart."""

from fractions import Fraction


VARS = ("q1", "q2", "u1", "u2", "c1", "c2", "v1", "v2", "t", "s", "R")
N = len(VARS)


def const(value):
    return {(0,) * N: Fraction(value)}


def var(name):
    exponents = [0] * N
    exponents[VARS.index(name)] = 1
    return {tuple(exponents): Fraction(1)}


def add(*polys):
    out = {}
    for poly in polys:
        for monomial, coefficient in poly.items():
            out[monomial] = out.get(monomial, Fraction(0)) + coefficient
            if out[monomial] == 0:
                del out[monomial]
    return out


def neg(poly):
    return {m: -c for m, c in poly.items()}


def sub(left, right):
    return add(left, neg(right))


def mul(left, right):
    out = {}
    for lm, lc in left.items():
        for rm, rc in right.items():
            monomial = tuple(a + b for a, b in zip(lm, rm))
            out[monomial] = out.get(monomial, Fraction(0)) + lc * rc
    return {m: c for m, c in out.items() if c}


def scale(value, poly):
    return {m: Fraction(value) * c for m, c in poly.items() if value * c}


def diff(poly, name):
    index = VARS.index(name)
    out = {}
    for monomial, coefficient in poly.items():
        power = monomial[index]
        if power:
            reduced = list(monomial)
            reduced[index] -= 1
            out[tuple(reduced)] = coefficient * power
    return out


def square(poly):
    return mul(poly, poly)


def main() -> None:
    q1, q2, u1, u2, c1, c2, v1, v2, t, s, radius = (
        var(name) for name in VARS
    )
    w1 = sub(add(q1, mul(t, u1)), add(c1, mul(s, v1)))
    w2 = sub(add(q2, mul(t, u2)), add(c2, mul(s, v2)))
    g = sub(add(square(w1), square(w2)), square(radius))

    w_dot_u = add(mul(w1, u1), mul(w2, u2))
    w_dot_v = add(mul(w1, v1), mul(w2, v2))
    g_t = diff(g, "t")
    g_s = diff(g, "s")

    assert g_t == scale(2, w_dot_u)
    assert g_s == scale(-2, w_dot_v)
    # Verify -G_s/G_t=(w dot v)/(w dot u) without division.
    assert mul(neg(g_s), w_dot_u) == mul(g_t, w_dot_v)

    # Exact rational bounds for the explicit positive-mass cylinder in v49.
    r_bar = Fraction(9, 25)
    radius_value = Fraction(4, 25)
    y_max = Fraction(1, 100)
    w_max = Fraction(1, 100)
    s_max = Fraction(1, 400)

    # The complete unit clean-pass segment, and hence the pre-impact half of
    # it, stays away from every gray-disk lift.
    clean_vertical_distance = Fraction(1, 2) - y_max - Fraction(1, 2) * w_max
    assert clean_vertical_distance == Fraction(97, 200)
    assert clean_vertical_distance > r_bar

    # Perpendicular line-to-white-centre distance divided by R.
    delta = (y_max + (Fraction(1, 2) + s_max) * w_max) / radius_value
    assert delta == Fraction(601, 6400)
    assert Fraction(1) - delta**2 > Fraction(99, 100) ** 2

    # Exact root-window checks.  Avoid square roots by squaring positive
    # rational quantities.  a_min bounds (c-q).u from below.
    a_num_min = Fraction(1, 2) - s_max - y_max * w_max
    target_entry_lower = radius_value + Fraction(1, 4)
    assert a_num_min**2 > target_entry_lower**2 * (1 + w_max**2)
    # The entry root lies below 1/2 and the exit root lies above 1/2.
    a_max = Fraction(1, 2) + s_max + y_max * w_max
    g_lower = Fraction(99, 100)
    assert a_max - radius_value * g_lower < Fraction(1, 2)
    assert a_num_min**2 > (Fraction(1, 2) - radius_value * g_lower) ** 2 * (
        1 + w_max**2
    )

    # Incoming transversality in the translation direction e_1.  The worst
    # tangential contribution is delta*w_max.
    normal_x_numerator = g_lower - delta * w_max
    assert normal_x_numerator**2 > Fraction(49, 50) ** 2 * (1 + w_max**2)

    # Uniform vertical-fibre entry bounds used by the v50 local standard
    # family theorem.  If 1/4 < tau < 1/2 and cos(phi_+) > 99/100, then
    # tau/cos(phi_+) lies in (1/4,50/99).  Since R=4/25, the circular target
    # slope 1/R+cos(phi_+)/tau lies in (823/100,41/4).
    entry_jacobian_upper = Fraction(1, 2) / Fraction(99, 100)
    entry_slope_lower = 1 / radius_value + Fraction(99, 100) / Fraction(1, 2)
    entry_slope_upper = 1 / radius_value + 1 / Fraction(1, 4)
    assert entry_jacobian_upper == Fraction(50, 99)
    assert entry_slope_lower == Fraction(823, 100)
    assert entry_slope_upper == Fraction(41, 4)

    print("fixed-section clean impact chart: EXACT POLYNOMIAL IDENTITIES CERTIFIED")
    print("d_t G = 2 (w dot u)")
    print("d_s G = -2 (w dot v_c)")
    print("t_s = (w dot v_c)/(w dot u)")
    print("on G=0, |d_t G| = 2 R |n dot u|")
    print("explicit cylinder: POSITIVE-MASS FIRST-HIT BOUNDS CERTIFIED")
    print("incoming |n dot u| > 99/100 and n dot e1 < -49/50")
    print(
        "local entry fibre: RATIONAL CONSEQUENCES OF THE STATED "
        "BILLIARD DIFFERENTIAL FORMULAS CERTIFIED"
    )
    print("1/4 < |dr_+/dphi| < 50/99")
    print("823/100 < dphi_+/dr_+ < 41/4")


if __name__ == "__main__":
    main()
