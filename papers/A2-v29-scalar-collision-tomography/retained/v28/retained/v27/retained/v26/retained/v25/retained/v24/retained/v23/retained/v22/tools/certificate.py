#!/usr/bin/env python3
"""Finite arithmetic stage of the A2 v22 conditional completion certificate.

Inputs are already recovered genuine physical cycle vectors and area estimates.
This module does not identify bodies, fit endpoint laws, validate a physical
branch, or supply the deterministic error bounds required by the theorem.
"""
from __future__ import annotations
from dataclasses import dataclass
from fractions import Fraction
from itertools import combinations
from math import ceil, gcd, hypot, isfinite, lcm, sqrt
from typing import Sequence

Vector = tuple[float, float]


def determinant(u: Sequence, v: Sequence):
    return u[0] * v[1] - u[1] * v[0]


def extended_gcd(a: int, b: int) -> tuple[int, int, int]:
    """Return nonnegative g and x,y with xa+yb=g, including zero inputs."""
    old_r, r, old_s, s, old_t, t = a, b, 1, 0, 0, 1
    while r:
        q = old_r // r
        old_r, r = r, old_r - q * r
        old_s, s = s, old_s - q * s
        old_t, t = t, old_t - q * t
    sign = 1 if old_r >= 0 else -1
    return sign * old_r, sign * old_s, sign * old_t


def column_hnf(columns: Sequence[tuple[int, int]]) -> tuple[tuple[int, int], tuple[int, int]]:
    """Return matrix rows of the rank-two column basis [(a,0),(b,c)]."""
    if any(not isinstance(z, int) for v in columns for z in v):
        raise TypeError('Hermite input must be integer columns')
    minor_gcd = 0
    for u, v in combinations(columns, 2):
        minor_gcd = gcd(minor_gcd, abs(determinant(u, v)))
    if not minor_gcd:
        raise ValueError('column group has rank less than two')
    c = x_at_c = 0
    for x, y in columns:
        new_c, alpha, beta = extended_gcd(c, y)
        x_at_c = alpha * x_at_c + beta * x
        c = new_c
    if not c or minor_gcd % c:
        raise ArithmeticError('inconsistent rank-two group')
    a = minor_gcd // c
    b = x_at_c % a
    for x, y in columns:
        if y % c or (x - b * (y // c)) % a:
            raise ArithmeticError('Hermite membership check failed')
    return ((a, b), (0, c))


def bounded_rational(value: float, bound: int, radius: float) -> Fraction:
    """Unique reduced rational within radius; fail rather than guess."""
    if not isfinite(value) or bound < 1 or radius <= 0:
        raise ValueError('invalid rational reconstruction inputs')
    candidates: set[Fraction] = set()
    for denominator in range(1, bound + 1):
        nearest = round(value * denominator)
        for numerator in (nearest - 1, nearest, nearest + 1):
            candidate = Fraction(numerator, denominator)
            if abs(float(candidate) - value) < radius:
                candidates.add(candidate)
    if len(candidates) != 1:
        raise ValueError(f'rational reconstruction has {len(candidates)} candidates')
    return candidates.pop()


@dataclass(frozen=True)
class CycleCertificate:
    rank_two: bool
    covolume: float | None
    covolume_error: float | None
    denominator: int | None
    integer_basis: tuple[tuple[int, int], tuple[int, int]] | None
    period_basis_columns: tuple[Vector, Vector] | None
    selected_pair: tuple[int, int] | None
    rational_coordinates: tuple[tuple[Fraction, Fraction], ...]


def recover_cycles(vectors: Sequence[Vector], *, vector_error: float,
                   true_norm_bound: float, covolume_lower: float) -> CycleCertificate:
    """Decode the integer group under the explicit deterministic priors.

    Each supplied vector must be within vector_error of a true period vector.
    True period lattice covolume is at least covolume_lower. Floating arithmetic
    implements the finite diagnostic stage; it is not interval arithmetic.
    """
    B, V, t = true_norm_bound, covolume_lower, vector_error
    if not all(isfinite(x) for x in (B, V, t)) or B <= 0 or V <= 0 or t < 0:
        raise ValueError('invalid deterministic bounds')
    if any(len(v) != 2 or not all(isfinite(z) for z in v) for v in vectors):
        raise ValueError('finite two-dimensional vectors required')
    if any(hypot(*v) > B + t + 1e-12 for v in vectors):
        raise ValueError('observations violate the supplied norm bound')
    det_error = (2 * B + t) * t
    if det_error >= V / 4:
        raise ValueError('precision is insufficient for rank separation')
    pairs = list(combinations(range(len(vectors)), 2))
    if not pairs:
        return CycleCertificate(False, None, None, None, None, None, None, ())
    i, j = max(pairs, key=lambda ij: abs(determinant(vectors[ij[0]], vectors[ij[1]])))
    u, v = vectors[i], vectors[j]
    det = determinant(u, v)
    if abs(det) <= V / 2:
        return CycleCertificate(False, None, None, None, None, None, None, ())
    Q = max(1, ceil(B * B / V))
    radius = 1 / (4 * Q * Q)
    inverse_bound = sqrt(2) * (B + t) / (V - det_error)
    coordinate_error = inverse_bound * t * (1 + 2 * B * B / V)
    if coordinate_error >= radius:
        raise ValueError('precision is insufficient for bounded-denominator separation')
    coords = []
    for x, y in vectors:
        z0 = (v[1] * x - v[0] * y) / det
        z1 = (-u[1] * x + u[0] * y) / det
        coords.append((bounded_rational(z0, Q, radius), bounded_rational(z1, Q, radius)))
    q = lcm(*(z.denominator for p in coords for z in p))
    if q > Q:
        raise ValueError('decoded denominators violate their common-index bound')
    columns = [(int(q * x), int(q * y)) for x, y in coords]
    H = column_hnf(columns)
    factor = H[0][0] * H[1][1] / q**2
    if factor > 1 + 1e-12:
        raise ArithmeticError('integer group does not contain the selected pair')
    basis = tuple(tuple((u[k] * H[0][ell] + v[k] * H[1][ell]) / q
                        for k in range(2)) for ell in range(2))
    return CycleCertificate(True, abs(det) * factor, det_error * factor,
                            q, H, basis, (i, j), tuple(coords))


def completion_decision(cycles: CycleCertificate, *, free_area: float,
                        visible_area_sum: float, combined_area_error: float,
                        covolume_lower: float, body_area_lower: float) -> dict:
    """Conditional decision. False means not certified, not nonexistent.

    combined_area_error bounds the error in estimated A + visible shape areas.
    Visible shapes must already be correctly clustered, counted once each.
    """
    values = (free_area, visible_area_sum, combined_area_error,
              covolume_lower, body_area_lower)
    if not all(isfinite(x) for x in values):
        raise ValueError('non-finite area input')
    if min(free_area, covolume_lower, body_area_lower) <= 0:
        raise ValueError('positive area margins required')
    if visible_area_sum < 0 or combined_area_error < 0:
        raise ValueError('negative area or error')
    if not cycles.rank_two:
        return {'accepted': False, 'reason': 'rank_less_than_two', 'defect': None}
    gap = min(covolume_lower, body_area_lower)
    error = cycles.covolume_error + combined_area_error
    if error >= gap / 4:
        raise ValueError('precision is insufficient for the completion gap')
    defect = cycles.covolume - free_area - visible_area_sum
    if defect < -error - 1e-10:
        raise ValueError('negative defect contradicts the physical model and error bounds')
    return {'accepted': abs(defect) < gap / 2, 'reason': 'completion_gap_test',
            'defect': defect, 'defect_error': error, 'gap': gap}
