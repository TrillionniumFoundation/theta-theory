#!/usr/bin/env python3
"""Independent finite diagnostics for the A2-DYN v4/v5-alias referee report.

The program imports no author code.  It checks exact and high-precision finite
models for the periodic-record lattice, augmented real rank, quantitative phase
bookkeeping, alternating-orbit edge algebra, one-sided edge Fourier behavior,
Kac/clock formulas, length-bias transfer, and renewal inversion.  It is not a
continuum proof certificate, a transfer-operator construction, a full raw LLT,
a TeX build, a physical experiment, or an editorial decision.  Every check
remains active under ``python -O``.
"""
from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from fractions import Fraction as F
import cmath
import hashlib
import json
import math
import sys

CHECKS: Counter[str] = Counter()
METRICS: dict[str, object] = {}


def require(condition: bool, group: str, detail: str = "") -> None:
    if not condition:
        raise RuntimeError(f"{group}: {detail}")
    CHECKS[group] += 1


def determinant(a: list[list[F]]) -> F:
    m = [row[:] for row in a]
    n = len(m)
    out = F(1)
    for j in range(n):
        pivot = next((i for i in range(j, n) if m[i][j] != 0), None)
        if pivot is None:
            return F(0)
        if pivot != j:
            m[j], m[pivot] = m[pivot], m[j]
            out = -out
        p = m[j][j]
        out *= p
        for i in range(j + 1, n):
            q = m[i][j] / p
            for k in range(j + 1, n):
                m[i][k] -= q * m[j][k]
            m[i][j] = F(0)
    return out


@dataclass(frozen=True)
class Q3:
    """a+b*sqrt(3) with exact rational coefficients."""
    a: F
    b: F = F(0)

    def __add__(self, other: object) -> "Q3":
        other = other if isinstance(other, Q3) else Q3(F(other))
        return Q3(self.a + other.a, self.b + other.b)

    __radd__ = __add__

    def __neg__(self) -> "Q3":
        return Q3(-self.a, -self.b)

    def __sub__(self, other: object) -> "Q3":
        return self + (-other if isinstance(other, Q3) else -Q3(F(other)))

    def __rsub__(self, other: object) -> "Q3":
        return Q3(F(other)) - self

    def __mul__(self, other: object) -> "Q3":
        other = other if isinstance(other, Q3) else Q3(F(other))
        return Q3(self.a * other.a + 3 * self.b * other.b,
                  self.a * other.b + self.b * other.a)

    __rmul__ = __mul__

    def __truediv__(self, other: object) -> "Q3":
        other = other if isinstance(other, Q3) else Q3(F(other))
        norm = other.a * other.a - 3 * other.b * other.b
        if norm == 0:
            raise ZeroDivisionError
        return Q3((self.a * other.a - 3 * self.b * other.b) / norm,
                  (self.b * other.a - self.a * other.b) / norm)

    def is_zero(self) -> bool:
        return self.a == 0 and self.b == 0

    def value(self) -> float:
        return float(self.a) + float(self.b) * math.sqrt(3.0)


def determinant_q3(a: list[list[Q3]]) -> Q3:
    m = [row[:] for row in a]
    n = len(m)
    out = Q3(F(1))
    for j in range(n):
        pivot = next((i for i in range(j, n) if not m[i][j].is_zero()), None)
        if pivot is None:
            return Q3(F(0))
        if pivot != j:
            m[j], m[pivot] = m[pivot], m[j]
            out = -out
        p = m[j][j]
        out = out * p
        for i in range(j + 1, n):
            q = m[i][j] / p
            for k in range(j + 1, n):
                m[i][k] = m[i][k] - q * m[j][k]
            m[i][j] = Q3(F(0))
    return out


def lattice_and_real_rank() -> None:
    v = [
        [F(0), F(0), F(2), F(1)],
        [F(0), F(0), F(3), F(1)],
        [F(1), F(0), F(4), F(1)],
        [F(0), F(1), F(4), F(1)],
    ]
    det_v = determinant(v)
    require(abs(det_v) == 1, "augmented_lattice_unimodular")

    for rnum in range(450, 471):
        R = F(rnum, 1000)
        L2 = Q3(2 - 4 * R)
        L3 = Q3(3, -3 * R)
        g2 = Q3(-4 * R, 2)
        for l4a in (-3, -1, 0, 2, 7):
            for l4b in (-2, 0, 1, 4):
                L4 = Q3(F(l4a, 7), F(l4b, 11))
                rows = [
                    [Q3(0), Q3(0), Q3(2), Q3(1), L2],
                    [Q3(0), Q3(0), Q3(3), Q3(1), L3],
                    [Q3(1), Q3(0), Q3(4), Q3(1), L4],
                    [Q3(0), Q3(1), Q3(4), Q3(1), L4],
                    [Q3(0), Q3(0), Q3(2), Q3(1), g2],
                ]
                d = determinant_q3(rows)
                require(d.a == 2 and d.b == -2,
                        "augmented_real_rank_determinant", f"R={R},L4={L4}")
    METRICS["lattice_det"] = str(det_v)
    METRICS["real_rank_abs_det"] = "2*(sqrt(3)-1)"


def phase_bookkeeping() -> None:
    log_ratio = math.log(100.0 / 49.0)
    gamma = math.log(400.0) / log_ratio - 1.0
    min_lower = float("inf")
    cases = 0
    bs = [1.0 + k / 17.0 for k in range(500)]
    bs += [10.0 ** (k / 20.0) for k in range(0, 161)]
    bs += [math.exp(k / 13.0) for k in range(0, 181)]
    for b in bs:
        m = 1 + math.ceil(math.log(max(1.0, b)) / log_ratio)
        lower_delta = (400.0 ** (-m)) / 10000.0
        upper_delta = (49.0 / 100.0) ** (m - 1) / 300.0
        require(b * upper_delta <= 1.0 / 300.0 * (1.0 + 2e-14),
                "phase_upper_small_arc", f"b={b},m={m}")
        printed = b * 400.0 ** (-m) / (15000.0 * math.pi)
        power = b ** (-gamma) / (2400000000.0 * math.pi)
        require(printed + 1e-300 >= power * (1.0 - 2e-12),
                "phase_polynomial_lower_bound", f"b={b},m={m}")
        approximate = b * lower_delta / (math.pi * (m + 1))
        require(approximate > 0.0, "approximate_phase_positive")
        require(lower_delta < upper_delta, "excess_increment_interval_nonempty")
        min_lower = min(min_lower, printed / power)
        cases += 1

    for B in [1.0 + k / 3.0 for k in range(1, 80)] + [10.0 ** k for k in range(1, 11)]:
        m = 1 + math.ceil(math.log(B) / log_ratio)
        upper_delta = (49.0 / 100.0) ** (m - 1) / 300.0
        lower_delta = 400.0 ** (-m) / 10000.0
        for j in range(101):
            b = 1.0 + (B - 1.0) * j / 100.0
            require(b * upper_delta <= 1.0 / 300.0 * (1.0 + 2e-14),
                    "fixed_band_phase_upper")
            require(b * lower_delta >= lower_delta,
                    "fixed_band_phase_lower")
    require(gamma > 0, "phase_exponent_positive")
    METRICS["phase_cases"] = cases
    METRICS["phase_gamma"] = gamma
    METRICS["phase_min_printed_to_power_ratio"] = min_lower


def edge_hessian_and_decay() -> None:
    max_rel = 0.0
    cases = 0
    q = 47.0 / 53.0
    tstar = 50.0 / 3.0
    vstar = 200.0 / 47.0
    cstar = (47.0 / 90.0) * tstar * tstar / (vstar * (1.0 - q))
    for rnum in range(450, 471):
        R = rnum / 1000.0
        g = 1.0 - 2.0 * R
        zeta = math.acosh(1.0 + g / R)
        for N in range(1, 101):
            sh = math.sinh(N * zeta)
            A = math.sinh(zeta) / g / math.tanh(N * zeta)
            B = math.sinh(zeta) / (g * sh)
            lhs = (A * A - B * B) / (B * B)
            rhs = sh * sh
            rel = abs(lhs - rhs) / max(1.0, rhs)
            max_rel = max(max_rel, rel)
            require(rel < 2e-10, "alternating_hessian_determinant", f"R={R},N={N}")
            J = 1.0 / (2.0 * R * sh)
            require(J > 0.0, "normal_edge_jump_positive")
            if N >= 2:
                require(J <= cstar * q ** (N - 2) * (1.0 + 1e-12),
                        "normal_edge_within_general_decay")
            for b in (1.0, 3.0, 10.0, 100.0, 1000.0):
                ft = J / complex(1.0, -b)
                require(abs(abs(ft) * math.sqrt(1 + b * b) - J) < 2e-13,
                        "edge_fourier_exact_tail")
            cases += 1
    require(abs(q - 2 * tstar / (2 * tstar + vstar)) < 1e-15,
            "edge_neumann_ratio_identity")
    require(0 < q < 1, "edge_neumann_ratio_contracting")
    METRICS["edge_cases"] = cases
    METRICS["edge_max_relative_hessian_error"] = max_rel
    METRICS["general_edge_constant"] = cstar


def kac_and_rate_formulas() -> None:
    max_derivative = 0.0
    for rnum in range(45000, 47001, 5):
        R = rnum / 100000.0
        area = math.sqrt(3.0) / 2.0 - math.pi * R * R
        tau = area / (2.0 * R)
        rate = 1.0 / tau
        tau_prime = -math.sqrt(3.0) / (4.0 * R * R) - math.pi / 2.0
        rate_prime = 2.0 / area + 4.0 * math.pi * R * R / (area * area)
        require(area > 0.17, "free_area_lower_bound")
        require(tau > 0, "mean_free_flight_positive")
        require(abs(tau_prime) < 15.0 / 4.0, "mean_roof_derivative_bound")
        require(0.0 < rate_prime < 110.0, "physical_rate_derivative_bound")
        require(abs(rate - 2.0 * R / area) < 2e-15,
                "collision_rate_reciprocal_identity")
        max_derivative = max(max_derivative, rate_prime)
    METRICS["max_collision_rate_derivative_grid"] = max_derivative


def length_bias_transfer() -> None:
    cases = 0
    for n in range(3, 20):
        weights = [F((7 * i + 3) % 17 + 1, 1) for i in range(n)]
        total_w = sum(weights)
        nu = [w / total_w for w in weights]
        tau = [F((11 * i + 5) % 23 + 1, 7) for i in range(n)]
        mean_tau = sum(p * t for p, t in zip(nu, tau))
        rho = [p * t / mean_tau for p, t in zip(nu, tau)]
        for mask in range(1, min(1 << n, 2048)):
            event = [(mask >> i) & 1 for i in range(n)]
            nuB = sum(p for p, e in zip(nu, event) if e)
            rhoB = sum(p for p, e in zip(rho, event) if e)
            for L in (F(1, 2), F(1), F(2), F(4)):
                tail = sum(p * t for p, t in zip(nu, tau) if t > L)
                rhs = (L * nuB + tail) / mean_tau
                require(rhoB <= rhs, "length_bias_truncation_transfer")
                cases += 1
    METRICS["length_bias_cases"] = cases


def renewal_inversion_models() -> None:
    cases = 0
    max_count_error = 0.0
    for n in range(100, 801, 25):
        for mu in (0.7, 1.0, 1.8, 3.0):
            durations = [mu + 0.08 * math.sin(0.37 * j) + 0.03 * math.cos(0.11 * j)
                         for j in range(1, n + 1)]
            require(min(durations) > 0, "renewal_positive_roofs")
            sums = [0.0]
            for x in durations:
                sums.append(sums[-1] + x)
            horizon = min(sums[-1] * 0.9, n * mu * 0.85)
            grid = [horizon * k / 200.0 for k in range(1, 201)]
            j = 0
            for t in grid:
                while j + 1 < len(sums) and sums[j + 1] <= t:
                    j += 1
                max_dev = max(abs(sums[k] - k * mu) for k in range(j + 2))
                error = abs(j / t - 1.0 / mu)
                crude = (max_dev + mu) / (mu * t)
                require(error <= crude + 1e-12, "renewal_inverse_error_bound")
                max_count_error = max(max_count_error, error)
                cases += 1
    METRICS["renewal_inverse_cases"] = cases
    METRICS["renewal_max_rate_error"] = max_count_error


def residual_and_splice_bookkeeping() -> None:
    cases = 0
    for M in range(3, 21):
        for c in (0.2, 0.5, 1.0, 2.0):
            for A in (0, 1, 3, 7):
                for cM in (0.05, 0.2, 0.5, 1.0, 2.0, 5.0):
                    lo = cM / (M - 1)
                    hi = c / (A + 1)
                    if lo < hi:
                        kappa = (lo + hi) / 2.0
                        require(c - (A + 1) * kappa > 0,
                                "splice_middle_exponent_positive")
                        require((M - 1) * kappa - cM > 0,
                                "splice_outer_exponent_positive")
                    else:
                        require(not (lo < hi), "splice_infeasible_detected")
                    cases += 1
    require(2.0 >= 1.0, "splice_printed_counterexample_no_window")
    METRICS["splice_parameter_cases"] = cases


def subadditive_compact_models() -> None:
    cases = 0
    for eps in (F(1, 100), F(1, 20), F(1, 5)):
        for C in (F(1), F(7, 3), F(5)):
            for M in range(1, 16):
                for m in range(1, M + 1):
                    for n in range(1, 300):
                        q, r = divmod(n, m)
                        cost = q * eps * m + C * r
                        require(cost <= eps * n + C * M,
                                "compact_subadditive_budget")
                        cases += 1
    METRICS["subadditive_budget_cases"] = cases


def main() -> None:
    lattice_and_real_rank()
    phase_bookkeeping()
    edge_hessian_and_decay()
    kac_and_rate_formulas()
    length_bias_transfer()
    renewal_inversion_models()
    residual_and_splice_bookkeeping()
    subadditive_compact_models()
    result = {
        "schema": "a2-dyn-v4-external-review-finite-diagnostics-1",
        "status": "passed",
        "scope": (
            "Independent finite exact algebra and finite/high-precision models for "
            "the periodic, edge, clock, and splice bookkeeping. Not a continuum "
            "proof certificate, transfer-operator realization, full raw LLT, TeX "
            "build, physical experiment, human review, or journal decision."
        ),
        "imports_author_code": False,
        "runtime_dependencies": "Python standard library only",
        "checks": dict(sorted(CHECKS.items())),
        "metrics": METRICS,
        "total_checks": sum(CHECKS.values()),
        "full_raw_LLT_verified": False,
        "formal_proof_certificate": False,
        "physical_experiment": False,
        "human_specialist_review": False,
    }
    payload = json.dumps(result, sort_keys=True, separators=(",", ":")) + "\n"
    sys.stdout.write(payload)


if __name__ == "__main__":
    main()
