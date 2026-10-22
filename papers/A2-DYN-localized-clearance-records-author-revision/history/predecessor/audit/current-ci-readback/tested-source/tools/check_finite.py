#!/usr/bin/env python3
"""Exact finite diagnostics; not certification of the continuum theorems."""
from fractions import Fraction as F
from itertools import combinations, product
from math import prod
import json


def require(ok, description):
    if not ok:
        raise RuntimeError(description)


def mm(a, b):
    return [[sum(a[i][k] * b[k][j] for k in range(len(b)))
             for j in range(len(b[0]))] for i in range(len(a))]


def inv(a):
    n = len(a)
    x = [[F(v) for v in row] + [F(i == j) for j in range(n)]
         for i, row in enumerate(a)]
    for j in range(n):
        pivot = next((i for i in range(j, n) if x[i][j]), None)
        require(pivot is not None, 'singular test matrix')
        x[j], x[pivot] = x[pivot], x[j]
        scale = x[j][j]
        x[j] = [v / scale for v in x[j]]
        for i in range(n):
            if i != j:
                scale = x[i][j]
                x[i] = [u - scale * v for u, v in zip(x[i], x[j])]
    return [row[n:] for row in x]


def det(a):
    if not a:
        return F(1)
    x = [[F(v) for v in row] for row in a]
    ans = F(1)
    for j in range(len(x)):
        pivot = next((i for i in range(j, len(x)) if x[i][j]), None)
        if pivot is None:
            return F(0)
        if pivot != j:
            x[j], x[pivot] = x[pivot], x[j]
            ans = -ans
        scale = x[j][j]
        ans *= scale
        for i in range(j + 1, len(x)):
            q = x[i][j] / scale
            for k in range(j + 1, len(x)):
                x[i][k] -= q * x[j][k]
    return ans


def optical(tau, kappa):
    z = [[F(1), tau[0]], [F(0), F(1)]]
    for t, k in zip(tau[1:], kappa):
        z = mm([[1 + t * k, t], [k, 1]], z)
    return z[0][1]


def subsets(n):
    for s in range(n + 1):
        yield from combinations(range(1, n + 1), s)


def polynomial(tau, kappa):
    m = len(tau)
    return sum(prod(kappa[j - 1] for j in S)
               * prod(sum(tau[a:b]) for a, b in zip((0,) + S, S + (m,)))
               for S in subsets(m - 1))


def run():
    optical_cases = marked_cases = source_cases = localization_cases = 0
    rho, rmax, tmin = F(47, 59), F(47, 100), F(3, 50)
    for m in range(1, 8):
        for seed in range(8):
            R = F(45 + seed % 3, 100)
            cs = [F(1, 1 + (i * 3 + seed) % 7) for i in range(m + 1)]
            cs[0], cs[-1] = F(4, 5), F(3, 4)
            tau = [tmin + F((seed + i * 5) % 9, 25) for i in range(m)]
            ks = [2 / (R * c) for c in cs[1:-1]]
            b = optical(tau, ks)
            require(b == polynomial(tau, ks), 'positive subset expansion')
            J = [[F(0) for _ in ks] for _ in ks]
            for i, k in enumerate(ks):
                J[i][i] = k + 1 / tau[i] + 1 / tau[i + 1]
                if i:
                    J[i][i - 1] = J[i - 1][i] = 1 / tau[i]
            require(b == prod(tau) * det(J), 'continuant denominator')
            H = [[F(0) for _ in cs] for _ in cs]
            for i, c in enumerate(cs):
                H[i][i] = R * c * (1 if i in (0, m) else 2)
            for i, t in enumerate(tau):
                for j in (i, i + 1):
                    for k in (i, i + 1):
                        H[j][k] += R * R * cs[j] * cs[k] / t
            g0m = H[0][m]
            if m > 1:
                h_inv = inv([row[1:m] for row in H[1:m]])
                g0m -= sum(H[0][i + 1] * h_inv[i][j] * H[j + 1][m]
                           for i in range(m - 1) for j in range(m - 1))
                ji = inv(J)
                require(ji[0][-1] == (-1) ** m * prod(1 / t for t in tau[1:-1]) / det(J),
                        'corner cofactor')
            require(g0m == (-1) ** (m - 1) * R * R * cs[0] * cs[-1] / b,
                    'signed Schur corner')
            omega = abs(g0m) / R
            for S in subsets(m - 1):
                s = len(S)
                upper = rmax ** (s + 1) / (2 ** s * tmin ** (s + 1)) * rho ** (m - s - 1)
                require(omega / prod(cs[j] for j in S) <= upper, 'marked optical bound')
                marked_cases += 1
            optical_cases += 1

    for vals in product(range(4), repeat=4):
        f = list(map(F, vals))
        c, variation = min(f[0], f[-1]), sum(abs(v - u) for u, v in zip(f, f[1:]))
        for gamma in (F(1), F(2), F(5, 2), F(20)):
            paid, per = min(c, gamma * variation), max(F(0), c - gamma * variation)
            require(paid + per == c, 'positive source identity')
            if per > 0:
                require(all(abs(v - c) <= variation < c / gamma for v in f), 'persistence')
            if 0 in f:
                require(per == 0, 'full payment at a zero')
            for capacity in (F(0), F(1, 3), F(2), F(10)):
                old, new = max(F(0), c - capacity), max(F(0), per - capacity)
                require(0 <= old - new <= paid, 'shortage difference')
                require(paid + min(per, capacity) + new == c, 'three-part identity')
                source_cases += 1

    # Interval localization is a separate abstract diagnostic, not a Lorentz realization.
    for h in (F(1), F(1, 10), F(1, 10000)):
        for a in (F(-2), F(-1, 3), F(0), F(3)):
            for ell in (h / 100, h / 3, h * F(99, 100)):
                b = a + ell
                for s in (F(1, 1000), F(1, 2), F(999, 1000)):
                    t = a + s * ell
                    require(t - h < a < b < t + h, 'whole-segment localization')
                    localization_cases += 1
    require(F(4) - 1 - F(1, 32) == F(95, 32), 'epsilon payment exponent')
    require(F(95, 32) / 12 == F(95, 384), 'B payment exponent')
    require((F(1, 16) - F(1, 32)) / 12 == F(1, 384), 'accepted-capacity exponent')
    return dict(status='passed', arithmetic='exact rational', optical_cases=optical_cases,
                marked_cases=marked_cases, source_cases=source_cases,
                localization_cases=localization_cases, continuum_proof_certified=False,
                raw_pointwise_theorem_certified=False)


if __name__ == '__main__':
    print(json.dumps(run(), indent=2, sort_keys=True))
