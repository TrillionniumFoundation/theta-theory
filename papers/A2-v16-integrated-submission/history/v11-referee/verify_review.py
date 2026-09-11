#!/usr/bin/env python3
"""Independent finite arithmetic checks for the A2 v11 referee report.

Uses only the standard library, imports no manuscript code, and makes no network
requests. These checks are not proofs of the functional-analytic statements.
Checks remain active under python -O. Output is deterministic.
"""
from __future__ import annotations

import argparse
import json
from collections import defaultdict
from fractions import Fraction as F
from math import comb, factorial
from pathlib import Path
from typing import Iterable

REVIEWED_COMMIT = "c8af2cf4201deae5b447b490d44e3cba1aaa8ae0"
COUNTS: dict[str, int] = defaultdict(int)


def check(group: str, name: str, condition: bool) -> None:
    if not condition:
        raise RuntimeError(f"{group}: {name}")
    COUNTS[group] += 1


def rising(a: F, n: int) -> F:
    out = F(1)
    for k in range(n):
        out *= a + k
    return out


def half(n: int) -> F:
    return rising(F(1, 2), n)


def falling(n: int, r: int) -> int:
    return 0 if r > n else factorial(n) // factorial(n - r)


def add(a: list[F], b: list[F]) -> list[F]:
    return [(a[i] if i < len(a) else F(0)) +
            (b[i] if i < len(b) else F(0))
            for i in range(max(len(a), len(b)))]


def scale(a: list[F], c: F) -> list[F]:
    return [c * x for x in a]


def mul(a: list[F], b: list[F]) -> list[F]:
    out = [F(0)] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            out[i + j] += x * y
    return out


def trim(a: Iterable[F]) -> list[F]:
    out = list(a)
    while len(out) > 1 and out[-1] == 0:
        out.pop()
    return out


def flux(v: list[F], w: list[F]) -> list[F]:
    # H(V,W) = d^2 T(V,W), using exact simplex moments.
    out = [F(0)] * (len(v) + len(w) + 1)
    for r, vr in enumerate(v):
        for s, ws in enumerate(w):
            out[r + s + 2] += 2 * half(r) * half(s) * vr * ws / factorial(r + s + 2)
    return trim(out)


def abel_over_pi(h: list[F]) -> list[F]:
    # A(H)/pi on polynomials; includes the H''(0) endpoint term.
    out = [F(0)] * max(1, len(h) - 2)
    for k in range(2, len(h)):
        n = k - 2
        out[n] = h[k] * F(k * (k - 1), 2) * factorial(n) / half(n)
    return trim(out)


def weighted_volterra_over_pi(v: list[F], w: list[F]) -> list[F]:
    u = add(v, scale(w, F(-1)))
    a = add(v, w)
    a[0] -= 2
    out = scale(u, F(2)) + [F(0)] * len(a)
    # R_r/pi = (V+W-2)_r (1/2)_r/r!.
    for r in range(1, len(a)):
        rr = a[r] * half(r) / factorial(r)
        for n, un in enumerate(u):
            beta = F(factorial(r - 1)) / rising(F(n) + F(1, 2), r)
            out[r + n] += r * rr * un * beta
    return trim(out)


def basis(nodes: list[int], k: int) -> list[F]:
    out = [F(1)]
    for q in nodes:
        if q != k:
            out = scale(mul(out, [F(-q), F(1)]), F(1, k - q))
    return out


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    for r in range(8):
        for s in range(8):
            n = r + s
            h = 2 * half(r) * half(s) / factorial(n + 2)
            conv_over_pi = half(r) * half(s) / factorial(n)
            check("integrated_flux_identity", f"r={r},s={s}",
                  h * (n + 2) * (n + 1) == 2 * conv_over_pi)

    for r in range(5):
        for s in range(5):
            for q in range(min(r + s, 4) + 1):
                rhs = sum(comb(q, a) * falling(r, a) * falling(s, q - a)
                          for a in range(q + 1))
                check("differentiation_coefficients", f"r={r},s={s},q={q}",
                      rhs == falling(r + s, q))

    for n in range(33):
        lam = 4 * half(n) / factorial(n + 2)
        check("monomial_abel_inverse", f"binomial n={n}",
              lam == F(4 * comb(2 * n, n), 4 ** n * (n + 1) * (n + 2)))
        h = [F(0)] * (n + 2) + [lam]
        target = [F(0)] * n + [F(2)]
        check("monomial_abel_inverse", f"endpoint-inclusive n={n}",
              abel_over_pi(h) == target)

    profiles = [
        [F(1)],
        [F(1), F(1, 5)],
        [F(1), F(-1, 7), F(1, 11)],
        [F(1), F(1, 13), F(-1, 17), F(1, 19)],
        [F(1), F(-1, 23), F(1, 29), F(-1, 31), F(1, 37)],
    ]
    for i, v in enumerate(profiles):
        for k, w in enumerate(profiles):
            hd = add(flux(v, v), scale(flux(w, w), F(-1)))
            check("nonlinear_weighted_volterra", f"pair {i},{k}",
                  abel_over_pi(hd) == weighted_volterra_over_pi(v, w))

    for q in range(4, 11):
        nodes = list(range(1, q + 1))
        bases = {k: basis(nodes, k) for k in nodes}
        for power in range(q):
            reconstructed = [F(0)]
            for k in nodes:
                reconstructed = add(reconstructed, scale(bases[k], F(k ** power)))
            check("positive_node_reproduction", f"q={q},power={power}",
                  trim(reconstructed) == [F(0)] * power + [F(1)])
        for power in range(q):
            value = sum(F((-1) ** (k - 1) * comb(q, k) * k ** power)
                        for k in nodes)
            check("pilot_extrapolation", f"q={q},power={power}",
                  value == (1 if power == 0 else 0))

    for c in (F(3), F(7, 2), F(101)):
        for p in (F(1, 100), F(1, 7), F(1, 3)):
            h = c * p
            check("bernoulli_variance", f"c={c},p={p}",
                  c * c * p * (1 - p) == c * h * (1 - p))

    for t in (F(2), F(3), F(5, 2), F(7, 3)):
        sh = (t - 1 / t) / 2
        ch = (t + 1 / t) / 2
        sh2 = (t * t - 1 / (t * t)) / 2
        area = F(11, 3)
        c1, c2 = 1 / (2 * area * sh), 1 / (2 * area * sh2)
        check("calibration_algebra", f"ratio t={t}", c1 / (2 * c2) == ch)
        check("calibration_algebra", f"area t={t}", 1 / (2 * c1 * sh) == area)
    for shift in (F(0), F(1, 100), F(1, 7), F(2, 5)):
        check("affine_nullspace", f"quadratic shift={shift}",
              abel_over_pi([shift * shift, 2 * shift]) == [F(0)])

    rho = F(1, 8)
    max_steps = 0
    w = F(1)
    while w > rho:
        max_steps += 1
        w *= F(3, 4)
    pending = [(F(1), F(0), 0)]
    terminals = 0
    while pending:
        w, cost, depth = pending.pop()
        if w <= rho:
            terminals += 1
            check("bisection_all_histories", f"cost terminal={terminals}",
                  cost <= 1 / (rho * rho * (1 - F(3, 4) ** 2)))
            check("bisection_all_histories", f"depth terminal={terminals}",
                  depth <= max_steps)
        else:
            for factor in (F(1, 2), F(3, 4)):
                pending.append((w * factor, cost + 1 / (w * w), depth + 1))

    rates = []
    for m in range(4, 21):
        old_nu, new_nu = F(m) - F(5, 2), F(m) - F(1, 2)
        old, new, pilot = 2 + 6 / old_nu, 2 + 6 / new_nu, 2 + F(2, m)
        check("preparation_powers", f"improvement m={m}", new < old)
        check("preparation_powers", f"pilot absorption m={m}", new > pilot)
        check("preparation_powers", f"two extra derivatives m={m}",
              F(m + 2) - F(5, 2) == new_nu)
        check("preparation_powers", f"noise allocation m={m}",
              1 / new_nu + 2 * (1 + F(5, 2) / new_nu) == new)
        check("preparation_powers", f"Holder balance m={m}",
              new_nu / (m + 2) == 1 - F(5, 2) / (m + 2))
        if m in (4, 5, 6, 8, 12, 20):
            rates.append({"m": m, "v11_power_without_bridge": str(old),
                          "review_power_without_bridge": str(new),
                          "pilot_power": str(pilot),
                          "derived_Holder_exponent": str(new_nu / (m + 2))})
    check("preparation_powers", "m=4 baseline", 2 + 6 / F(3, 2) == 6)
    check("preparation_powers", "m=4 improvement", 2 + 6 / F(7, 2) == F(26, 7))

    result = {
        "schema": "a2-v11-independent-referee-checks/v1",
        "reviewed_commit": REVIEWED_COMMIT,
        "status": "passed",
        "total_checks": sum(COUNTS.values()),
        "groups": dict(sorted(COUNTS.items())),
        "bisection_terminal_histories": terminals,
        "rate_table": rates,
        "scope": "Finite exact rational identities; no manuscript code imported.",
        "limitations": [
            "Not a proof of any function-space estimate or asymptotic claim.",
            "No physical billiard simulation or physical realization test.",
            "No author-suite rerun, manuscript build, remote CI, or formal proof checking.",
            "Check counts overlap and are not independent theorem obligations."
        ]
    }
    text = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text, encoding="utf-8")
    else:
        print(text, end="")


if __name__ == "__main__":
    main()
