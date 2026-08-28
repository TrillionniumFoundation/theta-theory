#!/usr/bin/env python3
"""Exact certificates for the Gate-2 full-mass/tail audit.

This is deliberately a mixed positive/negative certificate.

Positive layer
--------------
It records the exact arithmetic behind a finite-core pair-energy route which
does *not* renormalize after truncation.  The accompanying report proves that
an unnormalised retained subkernel with a uniform pair-energy drift, plus its
true omitted probability, gives a full-law small-ball estimate.

Negative layer
--------------
A four-map rational model has all of the tempting marginal inputs:

* two separated core maps;
* an arbitrarily small (here 1/5) finite tail;
* uniformly positive co-Lipschitz constants and hence every branch-loss
  moment;
* a strict same-label Riesz coefficient at alpha=1/20.

Nevertheless two distinct tail maps have an exact common image at two
different inputs.  Their cross term is r^{-alpha} while the input energy is
fixed, so no uniform pair-energy drift can hold.  Thus a marginal
return/grazing/co-Lipschitz tail is not a substitute for an off-diagonal
projective near-collision estimate.

The script also checks an exact full-branch stopping-overshoot model.  It
shows why the canonical prefix antichain needs a named overshoot cemetery (or
an equivalent physical refinement) before native-scale comparability may be
claimed.

No one-state billiard return quotient, physical endpoint carrier, or PPE
amplitude registry is claimed here.
"""

from __future__ import annotations

from fractions import Fraction


def phi_g(z: Fraction) -> Fraction:
    return z / 4


def phi_w(z: Fraction) -> Fraction:
    return Fraction(3, 4) + z / 4


def phi_t0(z: Fraction) -> Fraction:
    return Fraction(1, 3) + z / 6


def phi_t1(z: Fraction) -> Fraction:
    return Fraction(1, 4) + z / 3


def cross_image_obstruction() -> None:
    """Exact finite-tail obstruction to a marginal-moment argument."""

    maps = (phi_g, phi_w, phi_t0, phi_t1)
    slopes = (Fraction(1, 4), Fraction(1, 4), Fraction(1, 6), Fraction(1, 3))
    weights = (
        Fraction(2, 5),
        Fraction(2, 5),
        Fraction(1, 10),
        Fraction(1, 10),
    )
    assert sum(weights, Fraction(0)) == 1
    assert sum(weights[2:], Fraction(0)) == Fraction(1, 5)

    # Every affine branch maps K=[0,1] into K and is co-Lipschitz by 1/6.
    for branch, slope in zip(maps, slopes):
        assert 0 <= branch(Fraction(0)) <= 1
        assert 0 <= branch(Fraction(1)) <= 1
        assert slope >= Fraction(1, 6)

    # The two declared core images are separated by exactly 1/2.
    assert phi_w(Fraction(0)) - phi_g(Fraction(1)) == Fraction(1, 2)

    # The same-label coefficient at alpha=1/20 is bounded by
    # (sum p_a^2) 6^(1/20).  Its twentieth power is strictly below one.
    square_mass = sum((weight * weight for weight in weights), Fraction(0))
    assert square_mass == Fraction(17, 50)
    assert 6 * 17**20 < 50**20

    # But distinct tail labels collide at distinct inputs.
    u = Fraction(0)
    v = Fraction(1, 4)
    assert u != v
    assert phi_t0(u) == phi_t1(v) == Fraction(1, 3)

    # Use the *same* alpha=1/20.  At r=n^-20 the colliding cross term is
    # p_t0 p_t1 r^-alpha=n/100.  The input energy is 4^(1/20)<2 and is fixed.
    # No numerical root is needed for these exact comparisons.
    for n in (8, 64, 1024, 65536):
        r = Fraction(1, n**20)
        assert r < abs(u - v)
        cross_term_at_alpha_one_twentieth = Fraction(n, 100)
        assert r * n**20 == 1
        assert cross_term_at_alpha_one_twentieth == weights[2] * weights[3] * n
        assert 4 < 2**20

    print("FINITE_TAIL_MASS=1/5: EXACT")
    print("ALL_BRANCH_COLIPSCHITZ>=1/6: EXACT")
    print("CORE_FIRST_IMAGE_GAP=1/2: EXACT")
    print("SAME_LABEL_ALPHA=1/20: 6*17^20<50^20")
    print("DISTINCT_TAIL_CROSS_IMAGE_COLLISION: EXACT")
    print("CROSS_OBSTRUCTION_AT_ALPHA=1/20: EXACT")
    print("MARGINAL_TAIL_MOMENT_IMPLIES_PAIR_DRIFT: FALSE")


def stopping_overshoot_certificate(depth_max: int = 16) -> None:
    """Exact scale-overshoot mass in a full-branch Lebesgue quotient.

    I_n=[2^-n,2^-(n-1)] has length and physical branch weight 2^-n.
    At sigma=2^-m, the first-level children n>2m overshoot below sigma^2.
    Their exact total mass is sigma^2.  Hence a full prefix antichain is
    measurable and mass preserving, but pointwise two-sided scale
    comparability requires a named exceptional refinement.
    """

    for m in range(2, depth_max + 1):
        sigma = Fraction(1, 2**m)
        tail_mass = sum(
            (Fraction(1, 2**n) for n in range(2 * m + 1, 8 * m + 1)),
            Fraction(0),
        )
        omitted_geometric_tail = Fraction(1, 2 ** (8 * m))
        assert tail_mass + omitted_geometric_tail == sigma * sigma

        first_overshoot_length = Fraction(1, 2 ** (2 * m + 1))
        assert first_overshoot_length < sigma * sigma

    print(f"FULL_BRANCH_STOPPING_OVERSHOOT_DEPTHS=2..{depth_max}: EXACT")
    print("OVERSHOOT_MASS_AT_SCALE_sigma=2^-m: sigma^2")
    print("POINTWISE_NATIVE_SCALE_COMPARABILITY_WITHOUT_CEMETERY: FALSE")


def unnormalised_core_arithmetic() -> None:
    """Exact sanity checks for the no-renormalisation transfer formula."""

    # A sample retained drift and exact tail sequence.  These values are not
    # billiard constants; they only exercise the algebra used in the theorem.
    kappa = Fraction(3, 4)
    c0 = Fraction(2)
    epsilon = Fraction(1, 1000)
    n = 20
    energy_bound = kappa**n + c0 * (1 - kappa**n) / (1 - kappa)
    union_tail_bound = n * epsilon
    assert energy_bound <= kappa**n + c0 / (1 - kappa)
    assert union_tail_bound == Fraction(1, 50)
    assert union_tail_bound < 1

    # No factor 1/(1-epsilon) occurs: the retained operator is sub-Markov and
    # the omitted physical probability is added back exactly by a union bound.
    print("UNNORMALISED_FINITE_CORE_TRANSFER_ALGEBRA: EXACT")
    print("TRUNCATION_RENORMALISATION_USED: FALSE")


def main() -> None:
    cross_image_obstruction()
    stopping_overshoot_certificate()
    unnormalised_core_arithmetic()
    print("FULL_MASS_BRANCH_ALPHABET_ON_PILOT: NOT_CERTIFIED")
    print("FULL_COUNTABLE_PROJECTIVE_PAIR_DRIFT: NOT_CERTIFIED")
    print("SAME_CARRIER_PHYSICAL_ENDPOINT_IDENTITY: NOT_CERTIFIED")
    print("ACTUAL_STOPPED_ANTICHAIN_AND_AMPLITUDE_REGISTRY: NOT_CERTIFIED")
    print("PHYSICAL_GATE2: NOT_CERTIFIED")


if __name__ == "__main__":
    main()
