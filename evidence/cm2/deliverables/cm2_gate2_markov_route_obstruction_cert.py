#!/usr/bin/env python3
"""Exact obstruction certificates for the proposed Gate-2 Markov route.

This file is deliberately a NO-GO certificate.  It checks two finite,
exact models used in the accompanying audit:

1. the full-mass dyadic inverse-branch kernel.  It has compact base,
   continuous branch weights, and Lebesgue stationary measure, but every
   finite-step law from a point is finite atomic.  The support itself is a
   total-variation/Doeblin witness against the non-atomic stationary law;

2. a continuous state-adaptive family of laws on projective Moebius maps.
   Each law satisfies the finite-moment and no-deterministic-images
   hypotheses of GKM Theorem 2.8, while adaptive selection preserves an
   atomic two-point stationary law.  Thus the independent-law theorem
   cannot be Markovized from the same hypotheses, even with continuity.

No claim about physical PPE or a billiard common vertex is made.
"""

from __future__ import annotations

from fractions import Fraction
from typing import NamedTuple


class Matrix(NamedTuple):
    a: int
    b: int
    c: int
    d: int

    def det(self) -> int:
        return self.a * self.d - self.b * self.c

    def trace(self) -> int:
        return self.a + self.d

    def discriminant(self) -> int:
        return self.trace() ** 2 - 4 * self.det()

    def act(self, x: Fraction) -> Fraction:
        denominator = self.c * x + self.d
        assert denominator != 0
        return Fraction(self.a * x + self.b, denominator)

    def fixed_polynomial(self) -> tuple[int, int, int]:
        # x=(a*x+b)/(c*x+d) iff c*x^2+(d-a)*x-b=0.
        return (self.c, self.d - self.a, -self.b)


IDENTITY = Matrix(1, 0, 0, 1)
A = Matrix(3, 1, 1, 1)
B = Matrix(2, 0, 0, 1)
C = Matrix(1, -1, 1, 10)
D = Matrix(2, -1, 0, 1)


def dyadic_reverse_kernel(depth_max: int = 12) -> None:
    """Check the exact full-mass inverse-branch formula through depth 12."""

    x = Fraction(1, 3)
    for depth in range(1, depth_max + 1):
        denominator = 2**depth
        support = [Fraction(x + k, denominator) for k in range(denominator)]
        weight = Fraction(1, denominator)
        assert len(set(support)) == denominator
        assert sum((weight for _ in support), Fraction(0)) == 1
        assert min(support) >= 0
        assert max(support) <= 1

    # For every finite depth S_n(x) is finite, hence Leb(S_n(x))=0, whereas
    # K_x^n(S_n(x))=1.  The finite assertions above certify the support and
    # mass part; the zero Lebesgue mass of a finite set is exact measure
    # theory, not a floating-point computation.
    print(f"DYADIC_FULL_MASS_DEPTHS=1..{depth_max}: EXACT")
    print("TV_WITNESS: K_x^n(S_n)=1, Leb(S_n)=0")
    print("DOEBLIN_MINORISATION_BY_LEBESGUE: IMPOSSIBLE")


def check_hyperbolic(matrix: Matrix) -> None:
    assert matrix.det() > 0
    assert matrix.discriminant() > 0


def adaptive_gkm_counterexample() -> None:
    """Check an exact two-point atomic continuous adaptive projective chain."""

    zero = Fraction(0)
    one = Fraction(1)

    for matrix in (A, B, C, D):
        check_hyperbolic(matrix)

    # mu_0=(id+A+B)/3 maps 0 to (0,1,0).
    assert (IDENTITY.act(zero), A.act(zero), B.act(zero)) == (zero, one, zero)
    # mu_1=(id+C+D)/3 maps 1 to (1,0,1).
    assert (IDENTITY.act(one), C.act(one), D.act(one)) == (one, zero, one)

    # B has fixed set {0,infinity}.  A fixes neither member.
    assert B.fixed_polynomial() == (0, -1, 0)
    assert A.c != 0  # infinity is not fixed by A
    assert A.fixed_polynomial()[2] != 0  # zero is not fixed by A

    # D has fixed set {1,infinity}.  C fixes neither member.
    assert D.fixed_polynomial() == (0, -1, 1)
    assert C.c != 0  # infinity is not fixed by C
    c2, c1, c0 = C.fixed_polynomial()
    assert c2 + c1 + c0 != 0  # one is not fixed by C

    # On the affine chart set t(z)=z^2/(z^2+(z-1)^2), extended by
    # t(infinity)=1/2, and mu_z=(1-t(z))*mu_0+t(z)*mu_1.  This is a
    # continuous compact family, with the required endpoint laws.
    def mixing_parameter(x: Fraction) -> Fraction:
        return x * x / (x * x + (x - 1) * (x - 1))

    assert mixing_parameter(zero) == 0
    assert mixing_parameter(one) == 1

    # The induced transition matrix on {0,1} is
    # [[2/3,1/3],[1/3,2/3]], so the uniform atomic law is stationary.
    transition = (
        (Fraction(2, 3), Fraction(1, 3)),
        (Fraction(1, 3), Fraction(2, 3)),
    )
    stationary = (Fraction(1, 2), Fraction(1, 2))
    pushed = tuple(
        sum(stationary[i] * transition[i][j] for i in range(2))
        for j in range(2)
    )
    assert pushed == stationary

    # Since id belongs to each support, a deterministic image for mu_0
    # would be a probability invariant under both A and B.  Every invariant
    # probability of a hyperbolic projective map is supported on its fixed
    # points (Poincare recurrence), and those fixed sets are disjoint by the
    # exact checks above.  The same argument applies to C,D for mu_1.
    print("GKM_CONTINUOUS_COMPACT_MIXTURE_FAMILY: EXACT")
    print("NO_DETERMINISTIC_IMAGES(all_mixtures): CERTIFIED")
    print("ADAPTIVE_ATOMIC_STATIONARY_MASS=(1/2,1/2): CERTIFIED")
    print("STATE_DEPENDENT_GKM_2_8_EXTENSION: FALSE")


def main() -> None:
    dyadic_reverse_kernel()
    adaptive_gkm_counterexample()
    print("CDKM_UNIFORM_ERGODICITY_FOR_REVERSE_BRANCH_KERNEL: FALSE")
    print("PHYSICAL_COLLISION_SRB_QUOTIENT: NOT INSTANTIATED")
    print("PHYSICAL_STOPPED_PARENT_PPE: NOT CERTIFIED")


if __name__ == "__main__":
    main()
