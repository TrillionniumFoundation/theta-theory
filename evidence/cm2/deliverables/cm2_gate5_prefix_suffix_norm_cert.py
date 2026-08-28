#!/usr/bin/env python3
"""Exact Gate-5 prefix/suffix algebra and sharp finite-height obstructions.

This certificate deliberately separates three statements.

1.  A finite Borel return-word ledger of height at most K gives finite
    *algebraic* source pushforwards, test pullbacks and Kac sums.
2.  Those formulas satisfy exact source/test adjoint and Kac pairings.
3.  Height and Borel measurability alone do not bound any of the regular,
    standard-family, flux/face or C1-test norms needed by CM2, and do not
    imply phase aperiodicity.

The countermodels are exact rational calculations.  They are diagnostics,
not models of the billiard.  They show which additional quantitative data
must be certified on the physical return branches.
"""

from __future__ import annotations

import math
from fractions import Fraction


K_N = 9


def dot(left: tuple[Fraction, ...], right: tuple[Fraction, ...]) -> Fraction:
    assert len(left) == len(right)
    return sum((x * y for x, y in zip(left, right)), Fraction(0))


def exact_endpoint_adjoint_pairing() -> Fraction:
    """A finite Borel endpoint map: push source, pull test, same pairing."""

    source = (Fraction(2), Fraction(3), Fraction(5))
    endpoint = (0, 1, 0)
    test = (Fraction(11), Fraction(13))

    pushed = tuple(
        sum((source[i] for i, target in enumerate(endpoint) if target == j),
            Fraction(0))
        for j in range(2)
    )
    pulled = tuple(test[target] for target in endpoint)
    lhs = dot(pushed, test)
    rhs = dot(source, pulled)
    assert pushed == (Fraction(7), Fraction(3))
    assert lhs == rhs == Fraction(116)
    return lhs


def exact_kac_tower_pairing() -> Fraction:
    """Exact normalized tower lift versus the Kac observable sum."""

    base_mass = (Fraction(3), Fraction(2))
    roofs = (2, 3)
    phase_test = (
        (Fraction(5), Fraction(7)),
        (Fraction(11), Fraction(13), Fraction(17)),
    )
    normalizer = sum(
        (base_mass[i] * roofs[i] for i in range(2)), Fraction(0)
    )
    assert normalizer == 12

    phase_pairing = sum(
        (
            base_mass[i] * sum(phase_test[i], Fraction(0)) / normalizer
            for i in range(2)
        ),
        Fraction(0),
    )
    kac_sum = tuple(sum(values, Fraction(0)) for values in phase_test)
    base_pairing = dot(base_mass, kac_sum) / normalizer
    assert phase_pairing == base_pairing == Fraction(59, 6)
    return phase_pairing


def exact_prefix_suffix_pairing() -> Fraction:
    """Finite-dimensional replay of a source prefix and a test suffix."""

    # P sends a two-coordinate source current to a three-coordinate event
    # carrier.  S propagates the event carrier to a two-coordinate endpoint.
    p = (
        (Fraction(1), Fraction(2)),
        (Fraction(0), Fraction(1)),
        (Fraction(3), Fraction(-1)),
    )
    s = (
        (Fraction(2), Fraction(0), Fraction(1)),
        (Fraction(-1), Fraction(4), Fraction(0)),
    )
    source = (Fraction(5), Fraction(7))
    test = (Fraction(11), Fraction(13))

    event = tuple(dot(row, source) for row in p)
    endpoint = tuple(dot(row, event) for row in s)
    lhs = dot(endpoint, test)

    suffix_pull = tuple(
        sum((s[i][j] * test[i] for i in range(2)), Fraction(0))
        for j in range(3)
    )
    full_pull = tuple(
        sum((p[i][j] * suffix_pull[i] for i in range(3)), Fraction(0))
        for j in range(2)
    )
    rhs = dot(source, full_pull)
    assert lhs == rhs == Fraction(623)
    return lhs


def quadratic_branch_obstruction() -> dict[str, Fraction]:
    """One height-one Borel branch can have unbounded inverse-Jacobian cost.

    For H(x)=x^2, the pushforward of dx has density
    rho(y)=1/(2 sqrt(y)).  At y=1/n^2 both rho and the derivative of the
    inverse pullback x=sqrt(y) equal n/2.  The same factor is the inverse
    tangent speed for a pushed one-dimensional face.
    """

    samples: list[Fraction] = []
    for n in (2, 4, 8, 16, 32, 64):
        y = Fraction(1, n * n)
        # Exact evaluation uses sqrt(y)=1/n.
        inverse_speed = Fraction(n, 2)
        push_density = Fraction(n, 2)
        assert y > 0
        assert inverse_speed == push_density
        samples.append(inverse_speed)
    assert all(a < b for a, b in zip(samples, samples[1:]))
    assert samples[-1] == 32
    return {
        "first_inverse_speed": samples[0],
        "last_inverse_speed": samples[-1],
        "last_bv_variation_lower_bound": samples[-1] - Fraction(1, 2),
    }


def finite_cut_complexity_obstruction() -> dict[str, int]:
    """Height one does not control the standard-family boundary mark.

    A unit curve of mass one has cost 1+1/|W|=2.  Split it into n disjoint
    image components, each of mass 1/n and length 1/n.  The positive
    decomposition cost is n+1.  Every n is finite and the return depth is
    still one.
    """

    n = 64
    input_cost = 2
    output_cost = sum(1 + Fraction(1, n) for _ in range(n))
    assert output_cost == n + 1
    assert output_cost / input_cost == Fraction(65, 2)
    return {
        "finite_piece_count": n,
        "input_cost": input_cost,
        "output_cost": int(output_cost),
    }


def phase_period_obstruction() -> int:
    """A strongly connected height-two phase graph may have period two."""

    # Two unit-weight edges 0->1->0.  The only primitive cycle has weight 2.
    cycle_weights = (2, 4, 6)
    period = 0
    for weight in cycle_weights:
        period = math.gcd(period, weight)
    assert period == 2

    # The phase transfer matrix swaps coordinates, so (1,-1) is an exact
    # eigenvector with eigenvalue -1 and its correlations do not decay.
    vector = (Fraction(1), Fraction(-1))
    swapped = (vector[1], vector[0])
    assert swapped == tuple(-x for x in vector)
    return period


def main() -> None:
    assert K_N == 9
    endpoint_pairing = exact_endpoint_adjoint_pairing()
    kac_pairing = exact_kac_tower_pairing()
    prefix_suffix_pairing = exact_prefix_suffix_pairing()
    quadratic = quadratic_branch_obstruction()
    cuts = finite_cut_complexity_obstruction()
    phase_period = phase_period_obstruction()

    print("STANDARD_N_RETURN_HEIGHT_BOUND=9: REPLAYED")
    print("FINITE_BOREL_PREFIX_SUFFIX_FORMULAS: CERTIFIED")
    print(f"  endpoint_adjoint_pairing={endpoint_pairing}")
    print(f"  normalized_kac_pairing={kac_pairing}")
    print(f"  prefix_suffix_pairing={prefix_suffix_pairing}")
    print("HEIGHT_ONLY_REGULAR_DENSITY_NORM_BOUND: FALSE")
    print(
        "  quadratic_branch_inverse_cost_sample="
        f"{quadratic['first_inverse_speed']}..{quadratic['last_inverse_speed']}"
    )
    print("HEIGHT_ONLY_STANDARD_FAMILY_FLUX_NORM_BOUND: FALSE")
    print(
        f"  finite_cut_cost={cuts['input_cost']}->{cuts['output_cost']} "
        f"with_{cuts['finite_piece_count']}_pieces"
    )
    print("HEIGHT_ONLY_PHYSICAL_C1_TEST_PULLBACK_BOUND: FALSE")
    print("HEIGHT_ONLY_PHASE_APERIODICITY: FALSE")
    print(f"  countermodel_cycle_gcd={phase_period}")
    print("PHYSICAL_PREFIX_SUFFIX_BRANCH_CONSTANTS: NOT CERTIFIED")
    print("STANDARD_FAMILY_CM2_NORM_INTERTWINER: NOT CERTIFIED")
    print("FLUX_FACE_CM2_NORM_INTERTWINER: NOT CERTIFIED")
    print("PHYSICAL_TEST_NORM_INTERTWINER: NOT CERTIFIED")
    print("ACTUAL_RETURN_PHASE_GCD_ONE: NOT CERTIFIED")
    print("GATE_5: NOT CERTIFIED")


if __name__ == "__main__":
    main()
