#!/usr/bin/env python3
"""Arb certificate for one grouped Gate-4 tangency incidence.

The certified band consists of gray-boundary points

    q(theta) = (9/25) (cos(theta), sin(theta)), |theta| <= 10^-7,

and the clockwise tangent from q(theta) to the central white disk.  The
straight continuation after the tangency is proved to hit G(1,1) first and
transversely.  The source tangency curve is strictly stable-oriented, while
its smooth G(1,1) collision image is strictly unstable-oriented.  This is the
geometry needed to represent the *same grouped incidence* once at each
non-grazing end; it deliberately does not certify the global event registry,
the global recovery theorem, or Gate 4.

The exact tangency and reversal identities used in the companion report are
algebraic consequences of

    u = (L d_x + R d_y, L d_y - R d_x) / |d|^2,
    L^2 = |d|^2 - R^2.

Arb is used for every strict inequality on the whole theta band.

Dependency: python-flint == 0.9.0.
"""

from __future__ import annotations

from fractions import Fraction

from flint import arb, ctx


ctx.prec = 200

THETA_RADIUS = Fraction(1, 10_000_000)
R_GRAY_Q = Fraction(9, 25)
R_WHITE_Q = Fraction(4, 25)


def arbq(value: Fraction | int) -> arb:
    value = Fraction(value)
    return arb(value.numerator) / value.denominator


def symmetric(radius: Fraction) -> arb:
    return arb(0, arbq(radius).upper())


def cross(a: tuple[arb, arb], b: tuple[arb, arb]) -> arb:
    return a[0] * b[1] - a[1] * b[0]


def dot(a: tuple[arb, arb], b: tuple[arb, arb]) -> arb:
    return a[0] * b[0] + a[1] * b[1]


def certify() -> dict[str, arb | int]:
    theta = symmetric(THETA_RADIUS)
    rg = arbq(R_GRAY_Q)
    rw = arbq(R_WHITE_Q)
    half = arbq(Fraction(1, 2))
    one = arb(1)

    cosine = theta.cos()
    sine = theta.sin()
    q = (rg * cosine, rg * sine)
    q_prime = (-rg * sine, rg * cosine)
    normal_g = (cosine, sine)

    # d points from the gray source to the central white centre.  The
    # displayed formula selects the same clockwise tangent as the exact
    # theta=0 witness in cm2_gate4_explicit_tangency_cert.py.
    d = (half - q[0], half - q[1])
    d_prime = (-q_prime[0], -q_prime[1])
    radius_squared = dot(d, d)
    radius_squared_prime = 2 * dot(d, d_prime)
    tangent_time = (radius_squared - rw * rw).sqrt()
    tangent_time_prime = radius_squared_prime / (2 * tangent_time)

    numerator = (
        tangent_time * d[0] + rw * d[1],
        tangent_time * d[1] - rw * d[0],
    )
    numerator_prime = (
        tangent_time_prime * d[0]
        + tangent_time * d_prime[0]
        + rw * d_prime[1],
        tangent_time_prime * d[1]
        + tangent_time * d_prime[1]
        - rw * d_prime[0],
    )
    u = (numerator[0] / radius_squared, numerator[1] / radius_squared)
    u_prime = (
        (numerator_prime[0] * radius_squared - numerator[0] * radius_squared_prime)
        / (radius_squared * radius_squared),
        (numerator_prime[1] * radius_squared - numerator[1] * radius_squared_prime)
        / (radius_squared * radius_squared),
    )

    # Source Birkhoff slope.  The angular derivative of a unit vector is its
    # cross product with its derivative.
    source_angle_prime = cross(u, u_prime)
    source_slope = (source_angle_prime - 1) / rg
    source_cosine = dot(u, normal_g)

    # First intersection with G(1,1).
    displacement_b = (q[0] - one, q[1] - one)
    displacement_b_prime = q_prime
    linear_b = dot(displacement_b, u)
    linear_b_prime = dot(displacement_b_prime, u) + dot(displacement_b, u_prime)
    constant_b = dot(displacement_b, displacement_b) - rg * rg
    constant_b_prime = 2 * dot(displacement_b, displacement_b_prime)
    discriminant_b = linear_b * linear_b - constant_b
    discriminant_b_prime = 2 * linear_b * linear_b_prime - constant_b_prime
    sqrt_discriminant_b = discriminant_b.sqrt()
    sqrt_discriminant_b_prime = discriminant_b_prime / (2 * sqrt_discriminant_b)
    flight_b = -linear_b - sqrt_discriminant_b
    flight_b_prime = -linear_b_prime - sqrt_discriminant_b_prime

    point_b = (q[0] + flight_b * u[0], q[1] + flight_b * u[1])
    point_b_prime = (
        q_prime[0] + flight_b_prime * u[0] + flight_b * u_prime[0],
        q_prime[1] + flight_b_prime * u[1] + flight_b * u_prime[1],
    )
    normal_b = ((point_b[0] - one) / rg, (point_b[1] - one) / rg)
    normal_b_prime = (point_b_prime[0] / rg, point_b_prime[1] / rg)
    normal_angle_prime = cross(normal_b, normal_b_prime)
    incoming_dot = dot(u, normal_b)
    incoming_dot_prime = dot(u_prime, normal_b) + dot(u, normal_b_prime)

    # Reflected outgoing velocity and its derivative at G(1,1).
    velocity_b = (
        u[0] - 2 * incoming_dot * normal_b[0],
        u[1] - 2 * incoming_dot * normal_b[1],
    )
    velocity_b_prime = (
        u_prime[0]
        - 2 * (incoming_dot_prime * normal_b[0] + incoming_dot * normal_b_prime[0]),
        u_prime[1]
        - 2 * (incoming_dot_prime * normal_b[1] + incoming_dot * normal_b_prime[1]),
    )
    outgoing_angle_prime = cross(velocity_b, velocity_b_prime)
    target_slope = (outgoing_angle_prime - normal_angle_prime) / (
        rg * normal_angle_prime
    )
    target_cosine = dot(velocity_b, normal_b)
    target_r_prime = rg * normal_angle_prime

    # The positive coefficient in (theta,phi) coarea coordinates, apart from
    # the table-wide SRB normalization.  Here |H_s|/|H_phi| = u_y/L.
    source_weight = rg * source_cosine * u[1] / tangent_time
    target_weight = source_weight / target_r_prime

    assert tangent_time > arbq(Fraction(49, 100))
    assert tangent_time < arbq(Fraction(1, 2))
    assert u[0] > arbq(Fraction(11, 20))
    assert u[1] > arbq(Fraction(83, 100))
    assert source_cosine > arbq(Fraction(11, 20))
    assert source_slope > arbq(Fraction(-4, 1))
    assert source_slope < arbq(Fraction(-19, 5))

    assert discriminant_b > arbq(Fraction(129, 1000))
    assert flight_b > arbq(Fraction(82, 100))
    assert flight_b < arbq(Fraction(84, 100))
    assert flight_b - tangent_time > arbq(Fraction(33, 100))
    assert -incoming_dot > arbq(Fraction(99, 100))
    assert target_cosine > arbq(Fraction(99, 100))
    assert target_r_prime > arbq(Fraction(13, 100))
    assert target_slope > arbq(Fraction(57, 10))
    assert target_slope < arbq(Fraction(59, 10))

    assert point_b[0] > arbq(Fraction(81, 100))
    assert point_b[0] < arbq(Fraction(83, 100))
    assert point_b[1] > arbq(Fraction(68, 100))
    assert point_b[1] < arbq(Fraction(70, 100))

    assert source_weight > arbq(Fraction(33, 100))
    assert source_weight < arbq(Fraction(34, 100))
    assert target_weight > arbq(Fraction(12, 5))
    assert target_weight < arbq(Fraction(13, 5))

    # Exhaustively rule out every other lift in [-3,3]^2 before G(1,1).
    # A positive discriminant may correspond to an intersection wholly in
    # the past; otherwise its near root must lie after the selected B root.
    checked = 0
    for kind, radius, offset in (
        ("G", rg, (Fraction(0), Fraction(0))),
        ("W", rw, (Fraction(1, 2), Fraction(1, 2))),
    ):
        for i in range(-3, 4):
            for j in range(-3, 4):
                if kind == "G" and (i, j) in {(0, 0), (1, 1)}:
                    continue
                if kind == "W" and (i, j) == (0, 0):
                    # This is the certified tangent contact, not a crossing.
                    continue
                center = (arbq(Fraction(i) + offset[0]), arbq(Fraction(j) + offset[1]))
                delta = (q[0] - center[0], q[1] - center[1])
                linear = dot(delta, u)
                discriminant = linear * linear - (dot(delta, delta) - radius * radius)
                checked += 1
                if discriminant < 0:
                    continue
                assert discriminant > 0
                square_root = discriminant.sqrt()
                near = -linear - square_root
                far = -linear + square_root
                assert far < 0 or near > flight_b

    # The certified segment lies in this compact coordinate box.  Every lift
    # with an index outside [-3,3]^2 is separated in at least one coordinate
    # by much more than the largest radius, so the finite scan is exhaustive.
    assert q[0] > arbq(Fraction(35, 100))
    assert q[1] > arbq(Fraction(-1, 1_000_000))
    assert point_b[0] < arbq(Fraction(83, 100))
    assert point_b[1] < arbq(Fraction(70, 100))

    return {
        "tangent_time": tangent_time,
        "source_cosine": source_cosine,
        "source_slope": source_slope,
        "flight_b": flight_b,
        "target_cosine": target_cosine,
        "target_slope": target_slope,
        "source_weight": source_weight,
        "target_weight": target_weight,
        "checked_competitors": checked,
    }


def main() -> None:
    result = certify()
    print("GATE4_GROUPED_G00_W00_G11_INCIDENCE: CERTIFIED")
    print(f"  theta_band=[-{THETA_RADIUS},+{THETA_RADIUS}]")
    print(f"  tangent_time={result['tangent_time']}")
    print(f"  source_cosine={result['source_cosine']}")
    print(f"  source_dphi_dr={result['source_slope']}")
    print(f"  continuation_flight={result['flight_b']}")
    print(f"  continuation_cosine={result['target_cosine']}")
    print(f"  image_dphi_dr={result['target_slope']}")
    print(f"  source_coarea_weight={result['source_weight']}")
    print(f"  image_coarea_weight={result['target_weight']}")
    print(f"  checked_competitor_lifts={result['checked_competitors']}")
    print("LOCAL_NON_GRAZING_TWO_END_CONTINUATION: CERTIFIED")
    print("GLOBAL_EVENTWISE_REVERSAL_REGISTRY: NOT CERTIFIED")
    print("GLOBAL_SINGLE_CHARGE_q_MAX: NOT CERTIFIED")
    print("GATE_4: NOT CERTIFIED")


if __name__ == "__main__":
    main()
