#!/usr/bin/env python3
"""Independent finite diagnostics for the A1 v17 referee report.

Python 3.10+; standard library only; no network, source import or author tests.
Exact checks use Fraction and integer powers, not floating root comparisons.
Floating Laurent checks are reported separately. These diagnostics do not
prove continuum-uniform theorems or certify mathematical originality.
"""
from __future__ import annotations

import argparse
import cmath
import hashlib
import itertools
import json
import math
from pathlib import Path
import platform
from fractions import Fraction as F
from collections import Counter

COUNTS: Counter[str] = Counter()
MAX_RESIDUAL = 0.0
SUBMISSION = "1f3838d89a5820b853d1e4b78194293b23e70bd2"


def check(condition: bool, group: str, message: str) -> None:
    if not condition:
        raise AssertionError(f"{group}: {message}")
    COUNTS[group] += 1


def products(scales: tuple[F, ...]) -> tuple[F, ...]:
    out = [F(1)]
    for s in scales:
        out.append(out[-1] * s)
    return tuple(out)


def ceil_fraction(x: F) -> int:
    return -(-x.numerator // x.denominator)


def envelope_power(volumes: tuple[F, ...], budget: F, power: int) -> F:
    """Return e(budget)**power exactly; power divisible by all indices."""
    return max((volumes[j] / budget) ** (power // j)
               for j in range(1, len(volumes)))


def envelope_checks() -> int:
    pool = (F(0), F(1, 81), F(1, 9), F(1, 3), F(1), F(3, 2))
    cases = 0
    for p in range(1, 6):
        power = math.lcm(*range(1, p + 1))
        for seq in itertools.combinations_with_replacement(pool, p):
            s = tuple(reversed(seq))
            v = products(s)
            rank = sum(x > 0 for x in s)
            cases += 1
            for ell in range(1, p + 1):
                for M in (1, 2, 3, 11, 97):
                    ep = envelope_power(v, F(M), power)
                    check(M ** power * ep ** ell >= v[ell] ** power,
                          "exact_envelope", "lower bound at integer budget")
                if s[ell - 1] > 0:
                    b = v[ell] / s[ell - 1] ** ell
                    check(b >= 1, "exact_envelope", "supporting budget admissible")
                    ep = envelope_power(v, b, power)
                    check(ep == s[ell - 1] ** power,
                          "exact_envelope", "continuous supporting equality")
                    M = ceil_fraction(b)
                    epm = envelope_power(v, F(M), power)
                    check(v[ell] ** power <= M ** power * epm ** ell
                          <= (2 * v[ell]) ** power,
                          "exact_envelope", "integer rounding sandwich")
                    # A curve oscillating between the stated comparison constants.
                    c, C = F(1, 4), F(9, 4)
                    factor = c if M % 2 else C
                    risk_transform_power = (F(M) ** (2 * power)
                                            * factor ** (ell * power)
                                            * epm ** (2 * ell))
                    check(c ** (ell * power) * v[ell] ** (2 * power)
                          <= risk_transform_power
                          <= 2 ** (2 * power) * C ** (ell * power)
                          * v[ell] ** (2 * power),
                          "exact_envelope", "comparison constants propagate")
                elif rank == 0:
                    check(envelope_power(v, F(19), power) == 0,
                          "exact_zero_rank", "all-zero list")
                else:
                    base = ceil_fraction(v[rank] / s[rank - 1] ** rank)
                    last = None
                    for q in range(4):
                        b = F(base * 2 ** q)
                        ep = envelope_power(v, b, power)
                        check(ep == (v[rank] / b) ** (power // rank),
                              "exact_zero_rank", "last positive branch dominates")
                        value = b ** power * ep ** ell
                        if last is not None:
                            check(value == last * F(2) ** (power * (rank - ell) // rank),
                                  "exact_zero_rank", "geometric decay beyond rank")
                        last = value
    return cases


def boundary_checks() -> None:
    # Whole-budget necessity: same exact envelope for every M <= B, different rank.
    for B in (1, 2, 7, 31, 100):
        eps = F(1, 2 * B)
        v, w = products((F(1), eps)), products((F(1), F(0)))
        for M in range(1, B + 1):
            check(envelope_power(v, F(M), 2) == envelope_power(w, F(M), 2),
                  "exact_scope", "finite-budget indistinguishability")
        M = 4 * B
        check(envelope_power(v, F(M), 2) > envelope_power(w, F(M), 2),
              "exact_scope", "tail curves separate")
    # Integer infimum need not equal the real one: s=(1,2/3,2/3), ell=2.
    v = products((F(1), F(2, 3), F(2, 3)))
    candidate_cubed = F(32, 81)
    for M in range(1, 65):
        # (M e(M)^2)^3 = M^3 e(M)^6.
        val = M ** 3 * envelope_power(v, F(M), 6)
        check(val >= candidate_cubed, "exact_scope", "integer rounding witness")
        if M == 2:
            check(val == candidate_cubed, "exact_scope", "minimum at two")
    check(candidate_cubed > v[2] ** 3,
          "exact_scope", "integer equality cannot replace sandwich")
    # Unordered coefficients can hide below an envelope: (A1,A2,A3)=(1,1/4,1).
    a = (F(1), F(1), F(1, 4), F(1))
    for M in (1, 2, 4, 19, 100):
        check(envelope_power(a, F(M), 6) == F(1, M) ** 2,
              "exact_scope", "hidden nonconcave coefficient")
    check(a[2] < 1, "exact_scope", "not an ordered-product counterexample")


def leja(nodes: tuple[F, ...]) -> tuple[F, ...]:
    remaining = list(enumerate(nodes))
    chosen: list[F] = []
    pivots: list[F] = []
    while remaining:
        if not chosen:
            index, x = min(remaining, key=lambda z: (z[1], z[0]))
            pivot = F(1)
        else:
            index, x = max(remaining,
                           key=lambda z: (math.prod(abs(z[1] - y) for y in chosen), -z[0]))
            pivot = math.prod(abs(x - y) for y in chosen)
        remaining.remove((index, x))
        chosen.append(x)
        pivots.append(F(pivot))
    return tuple(pivots)


def leja_checks() -> int:
    sets = [(F(1, 5),) * 5,
            (F(1, 10), F(1, 5), F(1, 5), F(3, 5), F(9, 10))]
    # Formal positive two-fold sums in the paper's intersecting-collision example.
    for u, v in ((0, 0), (F(1, 64), 0), (F(1, 64), F(1, 64)),
                 (F(1, 64), F(1, 32)), (F(1, 64), F(3, 128)),
                 (F(1, 64), F(1, 64) + F(1, 64) ** 3)):
        exponents = (F(0), F(1), F(2) + u, F(3) + v)
        sets.append(tuple((exponents[i] + exponents[j]) / 20
                          for i in range(4) for j in range(i, 4) if i or j))
    for nodes in sets:
        d = leja(nodes)
        check(all(1 >= x >= y >= 0 for x, y in zip(d, d[1:])),
              "exact_leja", "ordered scales at collisions")
        v = products(d)
        for ell in range(1, len(nodes) + 1):
            volume = max(math.prod(abs(x - y) for x, y in itertools.combinations(sub, 2))
                         for sub in itertools.combinations(nodes, ell))
            check(v[ell] <= volume <= math.factorial(ell) * v[ell],
                  "exact_leja", "maximal determinant comparison")
            if d[ell - 1] > 0:
                b = v[ell] / d[ell - 1] ** ell
                check(all(v[j] / b <= d[ell - 1] ** j for j in range(1, len(v))),
                      "exact_leja", "all branches below supporting scale")
    return len(sets)


def paired_checks() -> None:
    for k in range(1, 9):
        exponents = [2 * ((i + 1) // 2) for i in range(1, 2 * k + 1)]
        for j in range(1, k + 1):
            odd, even = sum(exponents[:2*j-1]), sum(exponents[:2*j])
            check(odd == 2*j*j and even == 2*j*(j+1),
                  "exact_pairs", "paired volume orders")
            check(odd - (2*j-1)*2*j == even - (2*j)*2*j == -2*j*(j-1),
                  "exact_pairs", "odd and even share supporting budget")
            if j > 1:
                # The odd branch is the weighted geometric mean of adjacent even branches.
                l, left, right = 2*j-1, 2*j-2, 2*j
                weight = F(j-1, 2*j-1)
                slope = weight * F(-2, left) + (1-weight)*F(-2, right)
                intercept = (weight * F(2*sum(exponents[:left]), left)
                             + (1-weight)*F(2*sum(exponents[:right]), right))
                check(slope == F(-2, l) and intercept == F(2*odd, l),
                      "exact_pairs", "odd branch interpolation")


def multiply(p: dict[int, complex], q: dict[int, complex]) -> dict[int, complex]:
    out: dict[int, complex] = {}
    for i, x in p.items():
        for j, y in q.items():
            out[i+j] = out.get(i+j, 0j) + x*y
    return out


def posterior(zs: list[complex], tau: float) -> dict[int, complex]:
    p = {0: 1+0j}
    for z in zs:
        p = multiply(p, {0: 1+0j, 1: tau*z, -1: tau*z.conjugate()})
    return {j: x / p[0].real for j, x in p.items()}


def near(x: complex | float, y: complex | float, label: str) -> None:
    global MAX_RESIDUAL
    residual = abs(x-y) / max(1.0, abs(x), abs(y))
    MAX_RESIDUAL = max(MAX_RESIDUAL, residual)
    check(residual <= 3e-12, "floating_laurent", label)


def circular_checks() -> None:
    rho = 1/64
    for n in range(1, 5):
        zs = [complex((j+1)/64, (-1)**j/96) for j in range(n)]
        ws = [z * complex(.7, .2) for z in zs]
        znew = complex(1/32, -1/48)
        for tau in (0., 1/1024, 1/16, 1/4):
            p, q = posterior(zs, tau), posterior(ws, tau)
            new = posterior(zs+[znew], tau)
            y = lambda j: tau**abs(j) * p.get(j, 0j)
            den = 1 + znew*y(1).conjugate() + znew.conjugate()*y(1)
            check(den.real >= 1-tau-1e-14, "floating_laurent", "evidence denominator")
            for j in range(1, n+2):
                update = (y(j) + tau*tau*znew*y(j-1) + znew.conjugate()*y(j+1))/den
                near(update, tau**j*new.get(j, 0j), "weighted causal update")
            for m in range(1, 5):
                B = [sum(math.factorial(m)*rho**(j+2*h)*tau**(2*h)
                         /(math.factorial(j+h)*math.factorial(h)*math.factorial(m-j-2*h))
                         for h in range((m-j)//2+1)) for j in range(m+1)]
                differences = []
                for l in range(2*m+1):
                    phi = 2*math.pi*l/(2*m+1)
                    zq = rho*cmath.exp(-1j*phi)
                    probe = {0: 1+0j}
                    for _ in range(m):
                        probe = multiply(probe, {0: .5+0j, 1: .5*tau*zq,
                                                 -1: .5*tau*zq.conjugate()})
                    actual = sum(x * probe.get(-j, 0j) for j, x in p.items())
                    other = sum(x * probe.get(-j, 0j) for j, x in q.items())
                    formula = 2**(-m)*B[0] + 2**(1-m)*sum(
                        B[j]*y(j)*cmath.exp(1j*j*phi) for j in range(1, m+1)).real
                    near(actual, formula, "physical query via Laurent multiplication")
                    differences.append(abs(actual-other)**2)
                physical = sum(differences)/(2*m+1)
                fourier = 2**(1-2*m)*sum(B[j]**2*abs(tau**j*(p.get(j, 0j)-q.get(j, 0j)))**2
                                         for j in range(1, m+1))
                near(physical, fourier, "finite-query Parseval identity")


def tilt_checks() -> None:
    # A two-atom algebraic diagnostic, not an instance of the full-support theorem.
    mu, likelihood, phi = (F(1, 3), F(2, 3)), (F(1, 2), F(3, 4)), (F(0), F(1))
    expectation = lambda p, v: sum(x*y for x, y in zip(p, v))
    nu = tuple(mu[i]*likelihood[i]/expectation(mu, likelihood) for i in range(2))
    f = tuple(x-expectation(nu, phi) for x in phi)
    s = F(1, 8)
    tilted = tuple(mu[i]*(1+s*f[i])/(1+s*expectation(mu, f)) for i in range(2))
    post = tuple(tilted[i]*likelihood[i]/expectation(tilted, likelihood) for i in range(2))
    check(sum(tilted) == 1 and expectation(mu, f) != 0,
          "exact_tilt", "prior normalization is necessary")
    check(post == tuple(nu[i]*(1+s*f[i]) for i in range(2)),
          "exact_tilt", "posterior tilt after normalized prior pullback")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=Path("EXECUTION_REPORT.json"))
    args = parser.parse_args()
    cases = envelope_checks()
    boundary_checks()
    node_sets = leja_checks()
    paired_checks()
    circular_checks()
    tilt_checks()
    source = Path(__file__).read_bytes()
    exact = sum(v for k, v in COUNTS.items() if k.startswith("exact_"))
    receipt = {
        "reviewed_submission": SUBMISSION,
        "python": platform.python_version(),
        "script_sha256": hashlib.sha256(source).hexdigest(),
        "status": "PASS", "scale_lists": cases, "node_multisets": node_sets,
        "checks_by_group": dict(sorted(COUNTS.items())),
        "exact_assertions": exact,
        "floating_assertions": COUNTS["floating_laurent"],
        "total_assertions": sum(COUNTS.values()),
        "largest_scaled_floating_residual": MAX_RESIDUAL,
        "floating_tolerance": 3e-12,
        "author_tests_run": False, "prior_referee_tests_run": False,
        "submission_build_run": False, "submission_manifest_verified": False,
        "limits": "Finite diagnostics only; no continuum proof, priority finding, or journal endorsement."
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(receipt, indent=2))


if __name__ == "__main__":
    main()
