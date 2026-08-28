#!/usr/bin/env python3
"""Exact positive certificates for the Gate-2 weak-metric route.

This script certifies three model-independent arithmetic ingredients used in
the accompanying Gate-2 report.

1. The full-mass dyadic reverse kernel is maximally far from Lebesgue in
   total variation at every finite time, but contracts W_1 exactly by 2^-n.
   Thus the previous TV obstruction does not obstruct a Wasserstein route.

2. The two certified pilot projective maps have separated images and a
   common co-Lipschitz constant 1/169 on K=[5,7].  For arbitrary adaptive
   weights in [1/5,4/5], the two-copy truncated Riesz energy has contraction

       kappa = (17/25) * 169^(1/20) < 1.

   The strict inequality is checked using integer arithmetic after raising
   to the twentieth power.  The resulting finite-depth small-ball benchmark
   is place/history dependent, not i.i.d.

3. A scale-normalized Holder-to-sup bound gives a parentwise normalized
   amplitude moment.  A rational example checks the constants.

The actual collision-SRB quotient, its full countable branch-pair drift,
and the endpoint carrier typing are deliberately NOT claimed here.
"""

from __future__ import annotations

from fractions import Fraction
import math

from cm2_fixed_section_projective_cert import (
    assert_less,
    assert_positive,
    compare_projective,
    projective_denominator,
    projective_numerator,
)
from cm2_fixed_section_qnl_cert import Qsqrt2


def dyadic_wasserstein_certificate(depth_max: int = 16) -> None:
    """Exact same-label coupling for the full-mass dyadic reverse kernel."""

    x = Fraction(1, 7)
    y = Fraction(5, 11)
    distance = abs(x - y)
    for depth in range(depth_max + 1):
        denominator = 2**depth
        support_x = [Fraction(x + k, denominator) for k in range(denominator)]
        support_y = [Fraction(y + k, denominator) for k in range(denominator)]
        coupling_cost = sum(
            (abs(left - right) for left, right in zip(support_x, support_y)),
            Fraction(0),
        ) / denominator
        assert coupling_cost == distance / denominator
        assert len(set(support_x)) == denominator

    print(f"DYADIC_W1_DEPTHS=0..{depth_max}: EXACT_CONTRACTION_2^-n")
    print("DYADIC_TV_AT_FINITE_DEPTH: MAXIMAL (finite support vs Lebesgue)")


def pilot_projective_energy_certificate() -> None:
    """Recheck the pilot maps and the strict adaptive energy coefficient."""

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
    assert compare_projective(gray, Fraction(7), Fraction(11, 2), "Phi_g(7)") < 0
    assert compare_projective(white, Fraction(5), Fraction(13, 2), "Phi_w(5)") > 0
    assert compare_projective(white, Fraction(7), Fraction(7), "Phi_w(7)") < 0

    gap_numerator = (
        projective_numerator(white, Fraction(5))
        * projective_denominator(gray, Fraction(7))
        - projective_numerator(gray, Fraction(7))
        * projective_denominator(white, Fraction(5))
        - projective_denominator(white, Fraction(5))
        * projective_denominator(gray, Fraction(7))
    )
    assert_positive(gap_numerator, "pilot first-level gap > 1")

    # If p,q are both in [eta,1-eta], the probability coefficient of the
    # same-map pairs is pq+(1-p)(1-q).  A bilinear function reaches its
    # maximum at a corner of the rectangle.
    eta = Fraction(1, 5)
    corners = (
        p * q + (1 - p) * (1 - q)
        for p in (eta, 1 - eta)
        for q in (eta, 1 - eta)
    )
    same_map_coefficient = max(corners)
    assert same_map_coefficient == Fraction(17, 25)

    # alpha=1/20 and ell=1/169.  Since all quantities are positive,
    # kappa<1 iff kappa^20<1.
    assert 169 * 17**20 < 25**20
    kappa = float(same_map_coefficient) * 169.0 ** (1.0 / 20.0)
    assert kappa < 1.0

    print("PILOT_PROJECTIVE_IMAGES: SEPARATED_BY_MORE_THAN_1")
    print("PILOT_PROJECTIVE_COLIPSCHITZ: >1/169")
    print("ADAPTIVE_WEIGHT_WINDOW=[1/5,4/5]")
    print("ENERGY_ALPHA=1/20")
    print("KAPPA^20=169*(17/25)^20<1: EXACT")
    print(f"KAPPA_APPROX={kappa:.15f}")
    print(f"FINITE_DEPTH_REMAINDER_BASE=sqrt(kappa)={math.sqrt(kappa):.15f}")
    print("RAW_INTERVAL_EXPONENT=1/40")


def normalized_amplitude_constant_check() -> None:
    """Check one exact instance of the Holder normalization lemma."""

    # On [0,1] with uniform density take A(x)=x.  Here M=1, theta=1,
    # L=1 and delta=min(1,(2L)^-1)=1/2.  The theorem gives
    # A/E[A] <= 2/(m*delta)=4, while the exact supremum is 2.
    mean = Fraction(1, 2)
    exact_normalized_sup = Fraction(1) / mean
    theorem_bound = Fraction(4)
    assert exact_normalized_sup == 2
    assert exact_normalized_sup <= theorem_bound
    print("SCALED_HOLDER_AMPLITUDE_NORMALIZATION_EXAMPLE: EXACT")
    print("A(x)=x: exact_sup(A/E[A])=2 <= theorem_bound=4")


def main() -> None:
    dyadic_wasserstein_certificate()
    pilot_projective_energy_certificate()
    normalized_amplitude_constant_check()
    print("WEAK_METRIC_AND_ENERGY_BRIDGES: POSITIVE_CERTIFICATE")
    print("PHYSICAL_FULL_MASS_PROJECTIVE_KERNEL: NOT_CERTIFIED")
    print("PHYSICAL_STOPPED_PARENT_PPE: NOT_CERTIFIED")


if __name__ == "__main__":
    main()
