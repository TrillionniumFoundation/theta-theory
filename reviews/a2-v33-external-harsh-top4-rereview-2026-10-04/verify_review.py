#!/usr/bin/env python3
"""Independent finite diagnostics for the A2 v33 external referee report.

This program imports no author code.  It checks finite algebra and model
mechanisms appearing in the v33 additions: dyadic control rounding,
prefix-free stopped transcripts, centering-scale separation, and a
one-dimensional physical common-response analogue for separated convex
components.  It is not a continuum proof certificate, a TeX build, a
physical apparatus test, or an editorial decision.
"""
from __future__ import annotations

from collections import Counter
from fractions import Fraction as F
from itertools import combinations, product
import json
import math

COUNTS: Counter[str] = Counter()


def require(condition: bool, group: str, detail: str = "") -> None:
    if not condition:
        raise RuntimeError(f"{group}: {detail}")
    COUNTS[group] += 1


def h2(x: float) -> float:
    if x <= 0.0 or x >= 1.0:
        return 0.0
    return -x * math.log2(x) - (1.0 - x) * math.log2(1.0 - x)


def bit_interval(q: F, body: tuple[F, F], a: F) -> int:
    """Closed-solid convention for a one-dimensional convex component."""
    left, right = body
    if left <= q <= right:
        return 0
    p = q + a
    seg_left, seg_right = min(q, p), max(q, p)
    return int(not (seg_right < left or right < seg_left))


def union_bit(q: F, bodies: tuple[tuple[F, F], ...], a: F) -> int:
    if any(left <= q <= right for left, right in bodies):
        return 0
    p = q + a
    lo, hi = min(q, p), max(q, p)
    return int(any(not (hi < left or right < lo) for left, right in bodies))


def hausdorff_interval(c0: tuple[F, F], c1: tuple[F, F]) -> F:
    return max(abs(c0[0] - c1[0]), abs(c0[1] - c1[1]))


def sweep_interval(c: tuple[F, F], a: F) -> tuple[F, F]:
    return (c[0] + min(-a, F(0)), c[1] + max(-a, F(0)))


def distance_intervals(c0: tuple[F, F], c1: tuple[F, F]) -> F:
    if c0[1] < c1[0]:
        return c1[0] - c0[1]
    if c1[1] < c0[0]:
        return c0[0] - c1[1]
    return F(0)


def find_zero_start(
    q: F,
    bodies: tuple[tuple[F, F], ...],
    a: F,
    radius: F,
    denominator: int = 96,
) -> F | None:
    """Brute-force a rational start within radius whose bit is zero."""
    candidates = {q - radius, q, q + radius}
    for k in range(-denominator, denominator + 1):
        candidates.add(q + radius * F(k, denominator))
    for left, right in bodies:
        mid = (left + right) / 2
        candidates.update((left, right, mid))
        eps = radius / denominator
        candidates.update((left - eps, right + eps))
    feasible = [x for x in candidates if abs(x - q) <= radius and union_bit(x, bodies, a) == 0]
    if not feasible:
        return None
    return min(feasible, key=lambda x: (abs(x - q), x))


def reciprocal_checks() -> None:
    bodies = ((F(-2), F(-1)), (F(2), F(3)))
    for q_num, a_num in product(range(-16, 17), range(-8, 9)):
        q, a = F(q_num, 4), F(a_num, 4)
        forward = union_bit(q, bodies, a)
        reverse = union_bit(q + a, bodies, -a)
        chi_q = int(any(l <= q <= r for l, r in bodies))
        chi_qa = int(any(l <= q + a <= r for l, r in bodies))
        require(forward - reverse == chi_qa - chi_q, "reciprocal_balance_truth_table")


def dyadic_and_rounding_checks() -> None:
    for b in range(3, 15):
        mesh = F(1, 2**b)
        for t_exp in range(1, min(b, 7)):
            t = F(1, 2**t_exp)
            for numerator in range(-9, 10):
                x = numerator * mesh
                for i, j in product(range(-5, 6), repeat=2):
                    y0 = x + i * t
                    y1 = x + j * t
                    require(y0.denominator <= 2**b and y1.denominator <= 2**b,
                            "one_dyadic_stencil")
                    require((y0 - x) == i * t and (y1 - x) == j * t,
                            "dyadic_translation_exact")

    for d_exp in range(5, 12):
        d = F(1, 2**d_exp)
        for w_num in range(3, 18):
            w0 = F(w_num, 2)
            states = {(F(0), w0)}
            for k in range(1, 11):
                nxt: set[tuple[F, F]] = set()
                for lo, hi in states:
                    exact_mid = (lo + hi) / 2
                    for eps in (-d, F(0), d):
                        mid = exact_mid + eps
                        for label in (0, 1):
                            nlo, nhi = (mid, hi) if label else (lo, mid)
                            width = max(F(0), nhi - nlo)
                            require(width <= (hi - lo) / 2 + d,
                                    "rounded_width_recurrence")
                            bound = w0 / (2**k) + 2 * d
                            require(width <= bound, "rounded_geometric_width")
                            nxt.add((nlo, nhi))
                states = set(sorted(nxt)[:80])

    for nu_exp, delta_exp in product(range(4, 33), range(2, 17)):
        nu, delta = 2.0**(-nu_exp), 2.0**(-delta_exp)
        for beta in (0.2, 0.5, 1.0):
            s = 6.0 + beta
            sigma = nu ** (s / (s - 2.0))
            b = math.ceil(3.0 + math.log2(1.0 / sigma))
            B = 1 + math.ceil(math.log2(4.0 / nu)) + math.ceil(math.log2(4.0 / delta))
            require(b <= math.ceil(5.0 + 2.0 * math.log2(1.0 / nu)),
                    "dyadic_precision_logarithmic")
            require(B >= nu_exp + delta_exp, "batch_description_budget")


def centering_and_exponent_checks() -> None:
    for beta in (F(1, 10), F(1, 4), F(1, 2), F(3, 4), F(1)):
        s = 6 + beta
        require(s - 2 == 4 + beta, "smoothness_exponent_identity")
        require(F(1, 1) / (s - 2) == F(1, 4 + beta), "attempt_exponent_identity")
        require(s / (s - 2) == (6 + beta) / (4 + beta), "calibration_exponent_identity")
        for h_den in (8, 16, 32, 64, 128):
            h = F(1, h_den)
            raw = float(h ** (s - 2))
            center = float(h ** s)
            require(center / raw <= float(h * h) * (1.0 + 1e-12),
                    "centering_lower_order")
            r = float(h ** s)
            nu = float(h ** (s - 2))
            reconstructed = nu ** float(s / (s - 2))
            require(abs(math.log(reconstructed / r)) < 1e-10,
                    "calibration_power_duality")

    for amplitude_num in range(1, 101):
        amplitude = F(amplitude_num, 10000)
        z_bound = 2 * amplitude
        require(z_bound <= 2 * amplitude, "steiner_first_harmonic_bound")
        require(3 * z_bound <= 6 * amplitude, "steiner_C2_harmonic_bound")


def prefix_free_checks() -> None:
    code_families = [
        ("0", "10", "110", "111"),
        ("00", "01", "10", "11"),
        ("0", "100", "101", "110", "111"),
        ("000", "001", "01", "10", "11"),
    ]
    probability_sets = [
        [F(1, 4)] * 4,
        [F(1, 2), F(1, 4), F(1, 8), F(1, 8)],
        [F(1, 10), F(2, 10), F(3, 10), F(4, 10)],
    ]
    for words in code_families:
        for x, y in combinations(words, 2):
            require(not x.startswith(y) and not y.startswith(x), "terminal_words_prefix_free")
        kraft = sum(F(1, 2 ** len(w)) for w in words)
        require(kraft <= 1, "prefix_kraft_inequality")
        for probs in probability_sets:
            if len(probs) != len(words):
                continue
            entropy = -sum(float(p) * math.log2(float(p)) for p in probs if p)
            mean_length = sum(float(p) * len(w) for p, w in zip(probs, words))
            require(entropy <= mean_length + 1e-12, "entropy_below_mean_length")

    for m in range(2, 257):
        M = 2**m
        for delta in (0.05, 0.1, 0.2, 0.25, 0.4):
            lower = (1.0 - delta) * math.log2(M) - h2(delta)
            require(lower >= 0.0, "sequential_information_nonnegative")
            if delta <= 0.25 and m >= 4:
                require(lower >= 0.4 * m, "expected_length_linear_in_log_packing")

    for n in range(1, 50):
        words = tuple("0" * k + "1" for k in range(n)) + ("0" * n,)
        kraft = sum(F(1, 2 ** len(w)) for w in words)
        require(kraft == 1, "truncated_prefix_mass_identity")
        probs = [F(1, 2 ** (k + 1)) for k in range(n)] + [F(1, 2**n)]
        require(sum(probs) == 1, "truncated_probability_identity")
        entropy = -sum(float(p) * math.log2(float(p)) for p in probs)
        mean = sum(float(p) * len(w) for p, w in zip(probs, words))
        require(abs(entropy - mean) < 1e-12, "truncated_entropy_length_identity")


def sweep_and_common_response_checks() -> None:
    for shift_num, width_num, e_num, a_num in product(range(-3, 4), range(2, 7), range(-2, 3), range(-5, 6)):
        c0 = (F(shift_num), F(shift_num + width_num))
        e = F(e_num, 20)
        c1 = (c0[0] + e, c0[1] + e)
        a = F(a_num, 10)
        require(hausdorff_interval(sweep_interval(c0, a), sweep_interval(c1, a))
                == hausdorff_interval(c0, c1), "sweep_Hausdorff_contraction")

    for gap_num, a_num in product(range(4, 15), range(-6, 7)):
        c = (F(-2), F(-1))
        d = (F(-1 + gap_num), F(gap_num))
        a = F(a_num, 10)
        before = distance_intervals(c, d)
        after = distance_intervals(sweep_interval(c, a), sweep_interval(d, a))
        require(after >= max(F(0), before - abs(a)), "swept_component_separation")

    disagreement_count = 0
    forced_count = 0
    for e_num in (1, 2, 3):
        e = F(e_num, 40)
        b0 = ((F(-5), F(-4)), (F(2), F(3)))
        b1 = ((F(-5) + e, F(-4) + e), (F(2) - e, F(3) - e))
        for a_num in range(-7, 8):
            a = F(a_num, 4)
            require(abs(a) < 2 or abs(a) >= 2, "command_enumerated")
            if abs(a) >= 2:
                continue
            for q_num in range(-300, 301):
                q = F(q_num, 40)
                z0, z1 = union_bit(q, b0, a), union_bit(q, b1, a)
                target = min(z0, z1)
                if z0 != z1:
                    disagreement_count += 1
                f0 = q if z0 == target else find_zero_start(q, b0, a, 2 * e)
                f1 = q if z1 == target else find_zero_start(q, b1, a, 2 * e)
                require(f0 is not None and f1 is not None, "common_response_start_exists",
                        f"e={e}, a={a}, q={q}, bits={z0,z1}")
                assert f0 is not None and f1 is not None
                require(abs(f0 - q) <= 2 * e and abs(f1 - q) <= 2 * e,
                        "physical_perturbation_budget")
                require(union_bit(f0, b0, a) == target and union_bit(f1, b1, a) == target,
                        "common_physical_response")
                if z0 != z1:
                    forced_count += 1
    require(disagreement_count > 0 and forced_count == disagreement_count,
            "nonvacuous_common_response")

    for depth in range(1, 10):
        history0 = ""
        history1 = ""
        for step in range(depth):
            key = int(history0 or "0", 2)
            q = F((7 * key + 3 * step) % 41 - 20, 5)
            a = F(((5 * key + step) % 9) - 4, 4)
            c0 = ((F(-5), F(-4)), (F(2), F(3)))
            c1 = ((F(-5) + F(1, 20), F(-4) + F(1, 20)),
                  (F(2) - F(1, 20), F(3) - F(1, 20)))
            bit = min(union_bit(q, c0, a), union_bit(q, c1, a))
            history0 += str(bit)
            history1 += str(bit)
            require(history0 == history1, "adaptive_transcript_identity")


def finite_arithmetic_checks() -> None:
    column_sets = [
        [(2, 0), (0, 3), (1, 1)],
        [(3, 0), (0, 5), (1, 2)],
        [(4, 0), (0, 6), (2, 3)],
        [(5, 0), (0, 7), (2, 3), (3, 4)],
    ]
    det = lambda x, y: x[0] * y[1] - x[1] * y[0]
    for cols in column_sets:
        minors = [abs(det(x, y)) for x, y in combinations(cols, 2)]
        gamma_index = math.gcd(*minors)
        require(gamma_index >= 1, "integer_cycle_rank")
        for i, j in combinations(range(len(cols)), 2):
            D = (cols[i], cols[j])
            d = det(*D)
            if d == 0:
                continue
            coords = [(F(det(c, D[1]), d), F(det(D[0], c), d)) for c in cols]
            q = math.lcm(*(v.denominator for pair in coords for v in pair))
            require(abs(d) % q == 0, "common_denominator_divides_pair_index")
            int_cols = [(q, 0), (0, q)] + [(int(q*x), int(q*y)) for x, y in coords]
            hdet = math.gcd(*(abs(det(x, y)) for x, y in combinations(int_cols, 2)))
            require(F(abs(d) * hdet, q*q) == gamma_index, "reference_free_covolume")
            require(1 <= hdet <= q*q, "Hermite_index_bounds")


def main() -> None:
    reciprocal_checks()
    dyadic_and_rounding_checks()
    centering_and_exponent_checks()
    prefix_free_checks()
    sweep_and_common_response_checks()
    finite_arithmetic_checks()
    result = {
        "schema": "a2-v33-independent-review-diagnostics-1",
        "status": "passed",
        "checks": dict(sorted(COUNTS.items())),
        "total_checks": sum(COUNTS.values()),
        "imports_author_code": False,
        "physical_sensor_executed": False,
        "tex_build": False,
        "continuum_proof_certificate": False,
        "scope": "finite algebra and model diagnostics for v33 additions only",
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
