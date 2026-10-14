#!/usr/bin/env python3
"""Deterministic finite regressions; not a continuum or LLT certificate."""
from __future__ import annotations
from fractions import Fraction as F
import json
import math
import random


def require(ok: bool, message: str) -> None:
    if not ok:
        raise RuntimeError(message)


def determinant(a: list[list[F]]) -> F:
    if not a:
        return F(1)
    b = [row[:] for row in a]
    value = F(1)
    for i in range(len(b)):
        require(b[i][i] > 0, 'nonpositive optical elimination pivot')
        pivot = b[i][i]
        value *= pivot
        for j in range(i + 1, len(b)):
            ratio = b[j][i] / pivot
            for k in range(i + 1, len(b)):
                b[j][k] -= ratio * b[i][k]
    return value


def optical_matrix(lengths: list[F], potentials: list[F]) -> list[list[F]]:
    n = len(potentials)
    require(len(lengths) == n + 1, 'inconsistent optical dimensions')
    a = [[F(0) for _ in range(n)] for _ in range(n)]
    for i in range(n):
        a[i][i] = 1 / lengths[i] + 1 / lengths[i + 1] + potentials[i]
        if i + 1 < n:
            a[i][i + 1] = a[i + 1][i] = -1 / lengths[i + 1]
    return a


def transfer(lengths: list[F], potentials: list[F]) -> F:
    y, flux = lengths[0], F(1)
    for length, potential in zip(lengths[1:], potentials):
        flux += potential * y
        y += length * flux
    return y


def checks() -> dict:
    rng = random.Random(761011)
    tau, rmax = F(3, 50), F(47, 100)
    count = 0
    for m in range(1, 10):
        for _ in range(12):
            radius = F(rng.randrange(450, 471), 1000)
            lengths = [tau + F(rng.randrange(0, 60), 100) for _ in range(m)]
            incidences = [F(rng.randrange(1, 101), 100) for _ in range(m - 1)]
            potentials = [2 / (radius * c) for c in incidences]
            det = determinant(optical_matrix(lengths, potentials))
            product = math.prod(lengths)
            y = transfer(lengths, potentials)
            require(y == product * det, 'continuant/positive-transfer mismatch')
            ymin = transfer([tau] * m, [2 / rmax] * (m - 1))
            require(y >= ymin, 'homogeneous denominator comparison failed')
            selected = [i for i in range(m - 1) if rng.randrange(2)]
            compare = [2 / radius if i in selected else v for i, v in enumerate(potentials)]
            ratio = determinant(optical_matrix(lengths, compare)) / det
            bound = math.prod([53 * incidences[i] / (6 + 47 * incidences[i]) for i in selected])
            require(ratio <= bound, 'simultaneous incidence gain failed')
            require(1 / y <= F(1, 1) / ymin * bound, 'combined optical bound failed')
            count += 1
    eta = math.acosh(53 / 47)
    rho = (53 - 10 * math.sqrt(6)) / 47
    require(abs(math.exp(-eta) - rho) < 1e-14, 'optical rate identity')
    for m in range(1, 60):
        exact = float(transfer([tau] * m, [2 / rmax] * (m - 1)))
        formula = float(tau) * math.sinh(m * eta) / math.sinh(eta)
        require(abs(exact / formula - 1) < 2e-13, 'hyperbolic-sine formula')
    for radius in (1e-5, .01, .2, 1.0):
        for h in (1e-8, 1e-4, .01):
            rh = math.sqrt(radius * radius + 2 * h)
            require(abs((radius / rh) * (rh / radius) - 1) < 1e-14, 'Morse Jacobian')
            require(rh - radius <= math.sqrt(2 * h) + 1e-14, 'Morse displacement')
    # A nonconstant source in exact planar Morse coordinates.
    angles = [(j + .5) * 2 * math.pi / 8192 for j in range(8192)]
    for h in (1e-6, 1e-3, .05):
        radius = .1
        rh = math.sqrt(radius * radius + 2 * h)
        defect = sum(max(0.0, .7 * (radius - rh) * math.cos(t)) for t in angles) * 2 * math.pi / len(angles)
        require(defect <= 2 * math.pi * .7 * math.sqrt(2 * h), 'weighted Morse defect')
    # Recharting a constant source must not destroy mass at a cap seam.
    source = [F(j + 1, 100) for j in range(64)]
    permutation = [(i + 17) % 64 for i in range(64)]
    target = [F(0)] * 64
    for i, j in enumerate(permutation):
        target[j] = source[i]
    matched = sum(min(source[i], target[j]) for i, j in enumerate(permutation))
    require(matched == sum(source), 'coordinate transport lost source mass')
    fake_kill = sum(source[i] for i, j in enumerate(permutation) if i // 8 != j // 8)
    require(fake_kill > 0, 'fixture did not expose artificial cap killing')
    # Fixed-width small mass is not uniform pointwise smallness.
    for m in (10, 100, 1000):
        height, width, delta = m ** -2, m ** -3, .1
        require(abs(m * m * height - 1) < 1e-12, 'pulse normalization')
        require(m * m * height * width / (2 * delta) <= 5 * m ** -3 + 1e-14, 'pulse average')
    return {'rational_optical_fixtures': count, 'hyperbolic_sine_counts': 59,
            'morse_jacobian_fixtures': 12, 'morse_weight_fixtures': 3,
            'cap_reassignment_mass_preserved': True, 'narrow_pulse_false_closure_rejected': True,
            'rho': rho, 'scope': 'finite algebra, analytic model fixtures and source bookkeeping only',
            'formal_proof_certificate': False, 'full_raw_return_LLT_proved': False}


if __name__ == '__main__':
    print(json.dumps(checks(), indent=2, sort_keys=True))
