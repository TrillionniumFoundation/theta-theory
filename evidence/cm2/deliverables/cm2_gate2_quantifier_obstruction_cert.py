#!/usr/bin/env python3
"""Exact finite certificates for two Gate-2 quantifier obstructions.

This is deliberately an obstruction/audit certificate, not a physical PPE
certificate.  It verifies with rational arithmetic that

1. a marginal finite-time Frostman bound need not survive disintegration
   over frozen parents; and
2. a raw L^p amplitude bound does not control the normalized amplitude tilt.

It also checks the elementary cylinder-mass part of the stopped-parent
binary-kernel bridge for a history-dependent (non-i.i.d.) kernel.
"""

from __future__ import annotations

from fractions import Fraction


def marginal_disintegration_obstruction(depth: int = 6) -> None:
    """A uniform grid marginal is regular while each parent fibre is atomic."""

    n = 2**depth
    points = [Fraction(2 * j + 1, 2 * n) for j in range(n)]
    endpoints = [Fraction(0), *points, Fraction(1)]

    # Every closed interval with endpoints in the finite registry has
    # marginal mass <= length + 1/n.  Moving an arbitrary interval endpoint
    # to the nearest registered point cannot increase the point count, so
    # this is the exact finite-grid analogue of a Frostman-plus-remainder law.
    for left in endpoints:
        for right in endpoints:
            if left > right:
                continue
            count = sum(left <= x <= right for x in points)
            mass = Fraction(count, n)
            assert mass <= right - left + Fraction(1, n)

    # Conditional on parent j, the child is delta_{x_j}.  At the singleton
    # {x_j} its mass is one, which violates the marginal constant-one bound
    # 0 + 1/n.
    assert Fraction(1) > Fraction(1, n)
    print(f"MARGINAL_FROSTMAN: |I| + 2^-{depth} CERTIFIED")
    print("FROZEN_PARENT_CONDITIONAL: ATOMIC COUNTEREXAMPLE CERTIFIED")


def normalized_amplitude_obstruction(depth: int = 6) -> None:
    """A=1_E has a small raw moment but a singular normalized tilt."""

    n = 2**depth
    event_mass = Fraction(1, n)
    raw_second_moment = event_mass
    z_a = event_mass
    normalized_second_moment = event_mass / (z_a * z_a)
    tilted_event_probability = event_mass / z_a

    assert raw_second_moment <= 1
    assert normalized_second_moment == n
    assert tilted_event_probability == 1
    print(f"RAW_L2={raw_second_moment}")
    print(f"NORMALIZED_L2={normalized_second_moment}")
    print("NORMALIZED_TILT_EVENT_MASS=1")


def history_dependent_binary_mass_bridge(depth: int = 12) -> None:
    """Check max cylinder mass <= q^k for a non-i.i.d. binary kernel."""

    eta = Fraction(1, 5)
    q = 1 - eta
    masses = {"": Fraction(1)}
    for level in range(1, depth + 1):
        children: dict[str, Fraction] = {}
        for word, mass in masses.items():
            # The next weight depends on the complete history, so this is not
            # an i.i.d. Bernoulli law.  Both weights stay in [eta, 1-eta].
            ones = word.count("1")
            p_zero = eta if (len(word) + ones) % 2 == 0 else q
            p_one = 1 - p_zero
            assert eta <= p_zero <= q
            assert eta <= p_one <= q
            children[word + "0"] = mass * p_zero
            children[word + "1"] = mass * p_one
        masses = children
        assert sum(masses.values(), Fraction(0)) == 1
        assert max(masses.values()) <= q**level

    print(f"HISTORY_DEPENDENT_BINARY_MAX_CYLINDER<={q}^{depth}: CERTIFIED")


def main() -> None:
    marginal_disintegration_obstruction()
    normalized_amplitude_obstruction()
    history_dependent_binary_mass_bridge()
    print("PHYSICAL_STOPPED_PARENT_PPE: NOT CERTIFIED")


if __name__ == "__main__":
    main()
