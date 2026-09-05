#!/usr/bin/env python3
"""Exact finite certificates accompanying the Round 47 analytic proofs.

All certificate and enclosure arithmetic uses Fraction. Numerical summaries
are diagnostics, not interval-certified logarithms or an all-depth proof.
The finite search raises ResourceLimit rather than returning a partial answer.
"""
from __future__ import annotations
from dataclasses import dataclass
from fractions import Fraction as F
from itertools import product
from math import factorial, prod
from typing import Sequence

class ResourceLimit(RuntimeError):
    """The declared finite resource budget was exceeded; no certificate issued."""


def rational(value: int | str | F) -> F:
    if isinstance(value, float):
        raise TypeError("Use a rational string, integer, or Fraction, not a float")
    return F(value)


def ceil_fraction(x: F) -> int:
    return -(-x.numerator // x.denominator)


@dataclass(frozen=True)
class Box:
    c_min: F
    c_max: F
    a_min: F
    a_max: F
    b_min: F
    b_max: F
    horizon: F = F(1)

    def __post_init__(self) -> None:
        for name in self.__dataclass_fields__:
            object.__setattr__(self, name, rational(getattr(self, name)))
        if not (0 < self.c_min < self.c_max and
                0 < self.a_min < self.a_max and
                2*self.a_max < self.b_min < self.b_max and self.horizon > 0):
            raise ValueError("Require positive ordered box bounds and b_min > 2 a_max")

    @property
    def lam(self) -> F:
        return 1+self.c_max+max(F(1), self.b_max+2*self.a_max)

    @property
    def Q(self) -> F:
        return 8*max(F(2), self.lam, self.horizon, 1/self.horizon, 1/self.a_min)


@dataclass(frozen=True)
class GridCertificate:
    mode: str
    depth: int
    radius: F
    order: int
    jet_order: int
    spacing: F
    atom_mass: F
    jet_constant: F
    amplification: F
    remainder: F
    separation: F

    def validate(self) -> None:
        if self.order < max(8, self.jet_order) or self.order % 4:
            raise ValueError("Invalid diagnostic-grid index")
        if self.spacing <= 0 or self.spacing > 1 or self.atom_mass <= 0:
            raise ValueError("Invalid spacing or mass")
        if self.jet_constant*self.amplification*self.remainder > self.radius/2:
            raise ValueError("The Taylor remainder has not been absorbed")
        expected = self.atom_mass*self.radius**2/(4*self.jet_constant**2*self.amplification**2)
        if self.separation != expected:
            raise ValueError("Incorrect separation certificate")


def grid_certificate(box: Box, depth: int, delta: int | str | F,
                     mode: str = "long", max_order: int = 4096) -> GridCertificate:
    """Find a lawful grid using an exact sufficient remainder test.

    The compact search uses the rational upper bound 3**ceil(Lambda*T/4)
    for the exponential. Its direct separation is certified; it need not
    select precisely the analytic closed-form N_c printed in the paper.
    The long search uses the proved remainder upper bound 2/32**N.
    """
    if not isinstance(depth, int) or depth < 0:
        raise ValueError("depth must be a nonnegative integer")
    delta = rational(delta)
    if not 0 < delta <= 1 or mode not in ("compact", "long"):
        raise ValueError("Require 0 < delta <= 1 and mode compact or long")
    R = 4*depth+8
    if not isinstance(max_order, int) or max_order < R:
        raise ResourceLimit("Diagnostic order exceeds the declared budget")
    L = box.Q**(25*(depth+1))
    N = R
    tau = box.horizon/4
    if mode == "compact":
        N = 4*ceil_fraction(max(F(N), box.horizon/2)/4)
        exponent = ceil_fraction(box.lam*tau)
        if N > max_order or exponent > 100000:
            raise ResourceLimit("Grid or exponential safety cap exceeded")
        exponential_upper = F(3)**exponent
    while N <= max_order:
        if mode == "compact":
            spacing = tau/N
            A = F(8)**N*spacing**(-R)
            E = 2*exponential_upper*(box.lam*tau)**(N+1)/factorial(N+1)
            mass = F(2)**(-N//4-1)/N
        else:
            spacing = 1/(256*box.lam)
            A = F(8)**N*spacing**(-R)
            E = F(2, 32**N)
            mass = F(2)**(-N//4+1)/N
        if L*A*E <= delta/2:
            result = GridCertificate(mode, depth, delta, N, R, spacing, mass,
                                     L, A, E, mass*delta**2/(4*L**2*A**2))
            result.validate()
            return result
        N += 4
    raise ResourceLimit(f"No certificate returned: order budget {max_order} exceeded")


def jacobi_matrix(a: Sequence[F], b: Sequence[F]) -> list[list[F]]:
    n = len(b)
    if n < 1 or len(a) != n-1:
        raise ValueError("Need n diagonals and n-1 off-diagonals")
    J = [[F(0) for _ in range(n)] for _ in range(n)]
    for i, v in enumerate(b):
        J[i][i] = rational(v)
    for i, v in enumerate(a):
        J[i][i+1] = J[i+1][i] = -rational(v)
    return J


def generator(c: F, a: Sequence[F], b: Sequence[F]) -> list[list[F]]:
    J = jacobi_matrix(a, b)
    n = len(b)
    A = [[F(0) for _ in range(2*n)] for _ in range(2*n)]
    for i in range(n):
        A[i][n+i] = 1
        A[n+i][n+i] = -rational(c)
        for j in range(n):
            A[n+i][j] = -J[i][j]
    return A


def matvec(A: Sequence[Sequence[F]], x: Sequence[F]) -> list[F]:
    if any(len(row) != len(x) for row in A):
        raise ValueError("Matrix/vector dimensions do not match")
    return [sum((a*b for a, b in zip(row, x)), F(0)) for row in A]


def step_polynomial(A: Sequence[Sequence[F]], t: F, order: int) -> F:
    """Exact step-response Taylor polynomial through generator degree order."""
    if not A or len(A) % 2 or any(len(row) != len(A) for row in A):
        raise ValueError("Require a nonempty even-dimensional square generator")
    if not isinstance(order, int) or order < 0:
        raise ValueError("Taylor order must be a nonnegative integer")
    t = rational(t)
    if t < 0:
        raise ValueError("Time must be nonnegative")
    n = len(A)//2
    vec = [F(0)]*len(A)
    vec[n] = F(1)
    total, coefficient = F(0), rational(t)
    for k in range(order+1):
        total += vec[0]*coefficient
        vec = matvec(A, vec)
        coefficient *= t/F(k+2)
    return total


@dataclass(frozen=True)
class OuterResult:
    # The coordinate order is c, a_0, b_0, ..., a_J, b_J.
    boxes: tuple[tuple[tuple[F, F], ...], ...]
    uniform_error: F
    examined_boxes: int
    # complete is always True. A capped search raises instead of returning.
    complete: bool = True


def outer_confidence(box: Box, depth: int,
                     observations: Sequence[tuple[F, F, F]], *,
                     tail_depth: int, mesh_radius: F, taylor_order: int,
                     max_boxes: int = 100000) -> OuterResult:
    """Certified finite outer union from rational (time, lower, upper) bands.

    This implements Proposition 'Correctness and termination'. It does not
    manufacture confidence-band coverage: supplied intervals must themselves
    be valid outward enclosures of the statistical bands.
    """
    if depth < 0 or tail_depth < depth+1 or taylor_order < 0:
        raise ValueError("Require depth >= 0, tail_depth >= depth+1, order >= 0")
    if tail_depth > 64 or taylor_order > 4096:
        raise ResourceLimit("Declared dimension/order safety cap exceeded")
    r = rational(mesh_radius)
    if r <= 0 or max_boxes < 1 or not observations:
        raise ValueError("Need a positive mesh/cap and at least one observation")
    obs = [(rational(t), rational(lo), rational(hi)) for t, lo, hi in observations]
    if any(t <= 0 or lo > hi for t, lo, hi in obs):
        raise ValueError("Times must be positive and bands ordered")
    K, P = tail_depth, taylor_order
    Tc = max(t for t, _, _ in obs)
    exponent = ceil_fraction(box.lam*Tc)
    if exponent > 100000:
        raise ResourceLimit("Exponential enclosure safety cap exceeded")
    exp_upper = F(3)**exponent
    tail = 2*Tc*exp_upper*(box.lam*Tc)**K/factorial(K)
    mesh = 2*r*Tc**2*exp_upper
    numerical = Tc*exp_upper*(box.lam*Tc)**(P+1)/factorial(P+1)
    E = tail+mesh+numerical
    # Internal order: c, b_0...b_K, a_0...a_{K-1}.
    intervals = [(box.c_min, box.c_max)] + [(box.b_min, box.b_max)]*(K+1) + [(box.a_min, box.a_max)]*K
    counts = [max(1, ceil_fraction((hi-lo)/(2*r))) for lo, hi in intervals]
    total = prod(counts)
    if total > max_boxes:
        raise ResourceLimit(f"Box count exceeds cap {max_boxes}; no partial result returned")
    partitions = []
    for (lo, hi), count in zip(intervals, counts):
        width = (hi-lo)/count
        partitions.append([(lo+i*width, lo+(i+1)*width) for i in range(count)])
    kept = []
    for cell in product(*partitions):
        centers = [(lo+hi)/2 for lo, hi in cell]
        c, b, a = centers[0], centers[1:K+2], centers[K+2:]
        A = generator(c, a, b)
        valid = True
        for t, lo, hi in obs:
            H = step_polynomial(A, t, P)
            if H+E < lo or H-E > hi:
                valid = False
                break
        if valid:
            projected = [cell[0]]
            for j in range(depth+1):
                projected.extend([cell[K+2+j], cell[1+j]])
            kept.append(tuple(projected))
    return OuterResult(tuple(kept), E, total)
