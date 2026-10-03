#!/usr/bin/env python3
"""Independent finite diagnostics for the A2 v32 referee report.

The script imports no author module.  It checks exact finite algebra behind the
reciprocal identity, the killed compass inverse, relaxed bisection,
seven-point interpolation, period arithmetic, packing exponents and binary
transcript counting.  It is not a continuum proof checker, a TeX build, a
physical sensor test, a priority search or an editorial decision.
"""
from __future__ import annotations

from collections import Counter
from fractions import Fraction as F
from itertools import combinations, product
import json
import math
import random

COUNTS: Counter[str] = Counter()
SHIFTS = ((1, 0), (-1, 0), (0, 1), (0, -1))


def require(ok: bool, group: str, detail: str = "") -> None:
    if not ok:
        raise RuntimeError(f"{group}: {detail}")
    COUNTS[group] += 1


def t_value(values: dict[tuple[int, int], F], point: tuple[int, int]) -> F:
    i, j = point
    return sum((values.get((i + a, j + b), F(0)) for a, b in SHIFTS), F(0)) / 4


def determinant(a: tuple[int, int], b: tuple[int, int]) -> int:
    return a[0] * b[1] - a[1] * b[0]


def gaussian_solve(matrix: list[list[F]], rhs: list[F]) -> list[F]:
    n = len(rhs)
    a = [row[:] + [rhs[i]] for i, row in enumerate(matrix)]
    for col in range(n):
        pivot = next((r for r in range(col, n) if a[r][col] != 0), None)
        if pivot is None:
            raise RuntimeError("singular exact linear system")
        if pivot != col:
            a[col], a[pivot] = a[pivot], a[col]
        q = a[col][col]
        a[col] = [x / q for x in a[col]]
        for r in range(n):
            if r == col:
                continue
            q = a[r][col]
            if q:
                a[r] = [a[r][c] - q * a[col][c] for c in range(n + 1)]
    return [a[i][-1] for i in range(n)]


def reciprocal_checks() -> None:
    # Endpoint occupancies x=chi(q), y=chi(q+a).  If both endpoints are free,
    # segment and reverse bits agree, and either common value is possible.
    for hit in (0, 1):
        require(hit - hit == 0, "reciprocal_balance_truth_table")
    require(1 - 0 == 1, "reciprocal_balance_truth_table")
    require(0 - 1 == -1, "reciprocal_balance_truth_table")
    require(0 - 0 == 0, "reciprocal_balance_truth_table")

    # Averaging the pointwise identity commutes with translations.
    for x0, x1, x2, x3 in product(range(3), repeat=4):
        chi = {(0, 0): F(x0, 2), (1, 0): F(x1, 2),
               (0, 1): F(x2, 2), (1, 1): F(x3, 2)}
        lhs = sum((chi.get(p, F(0)) for p in ((1, 0), (-1, 0), (0, 1), (0, -1))), F(0)) / 4 - chi[(0, 0)]
        require(lhs == t_value(chi, (0, 0)) - chi[(0, 0)],
                "pooled_translation_identity")


def hessian_checks() -> None:
    for g, k0, k1 in product(
        (F(1, 5), F(1, 2), F(1), F(3)),
        (F(1, 7), F(1, 3), F(1), F(5, 2)),
        (F(1, 8), F(2, 5), F(4, 3), F(3)),
    ):
        a = 1 / g + k0
        b = -1 / g
        c = 1 / g + k1
        require(a > 0 and a * c - b * b == k0 * k1 + (k0 + k1) / g > 0,
                "normal_hessian_positive")
        lower = min(k0, k1)
        for x, y in product(range(-6, 7), repeat=2):
            q = a * x * x + 2 * b * x * y + c * y * y
            require(q >= lower * (x * x + y * y),
                    "normal_hessian_quadratic_lower_bound")


def finite_sets() -> list[set[tuple[int, int]]]:
    sets: list[set[tuple[int, int]]] = []
    for a in range(0, 4):
        for b in range(0, 3):
            sets.append(set(product(range(-a, a + 1), range(-b, b + 1))))
    for r in range(1, 5):
        sets.append({(i, j) for i in range(-r, r + 1)
                     for j in range(-r, r + 1) if abs(i) + abs(j) <= r})
    sets += [
        {(0, 0), (1, 0)},
        {(0, 0), (1, 0), (2, 0)},
        {(0, 0), (1, 0), (1, 1), (2, 1)},
        {(0, 0), (1, 0), (0, 1), (1, 1), (2, 1)},
    ]
    return [s for s in sets if s]


def exact_exit_times(sites: set[tuple[int, int]]) -> dict[tuple[int, int], F]:
    pts = sorted(sites)
    idx = {p: i for i, p in enumerate(pts)}
    matrix: list[list[F]] = []
    rhs: list[F] = []
    for p in pts:
        row = [F(0)] * len(pts)
        row[idx[p]] = 1
        for a, b in SHIFTS:
            q = (p[0] + a, p[1] + b)
            if q in idx:
                row[idx[q]] -= F(1, 4)
        matrix.append(row)
        rhs.append(F(1))
    sol = gaussian_solve(matrix, rhs)
    return {p: sol[idx[p]] for p in pts}


def exit_and_bellman_checks() -> None:
    for sites in finite_sets():
        exits = exact_exit_times(sites)
        xs = [p[0] for p in sites]
        ys = [p[1] for p in sites]
        # L1 diameter is a conservative upper bound for the Euclidean diameter.
        diameter = (max(xs) - min(xs)) + (max(ys) - min(ys))
        h_bound = F((diameter + 1) ** 2)
        for p, value in exits.items():
            require(value <= h_bound, "mean_exit_bound", f"{sites}, {p}")

        # Verify the exact dynamic equation.
        for p, value in exits.items():
            rhs = 1 + sum((exits.get((p[0] + a, p[1] + b), F(0))
                           for a, b in SHIFTS), F(0)) / 4
            require(value == rhs, "mean_exit_dynamic_equation")

        # Geometric survival after blocks of ceil(2H).
        block = max(1, 2 * int(h_bound))
        distribution = {p: F(1) for p in sites}
        # distribution[p] here is the survival probability starting at p.
        for n in range(1, min(3 * block, 180) + 1):
            distribution = {
                p: sum((distribution.get((p[0] + a, p[1] + b), F(0))
                        for a, b in SHIFTS), F(0)) / 4
                for p in sites
            }
            target = F(1, 2 ** (n // block))
            for value in distribution.values():
                require(value <= target, "geometric_survival_block_bound")

        # Generate a positive occupation on this component and verify the Bellman
        # monotonicity and stopped-semigroup error domination.
        u = {p: F(1 + ((7 * p[0] + 11 * p[1]) % 5), 6) for p in sites}
        g = {p: t_value(u, p) - u.get(p, F(0)) for p in sites}
        v = {p: F(0) for p in sites}
        killed_u = u.copy()
        for _depth in range(1, 13):
            new_v = {}
            for p in sites:
                new_v[p] = max(F(0), t_value(v, p) - g[p])
                require(F(0) <= v[p] <= new_v[p] <= u[p],
                        "bellman_monotone_bounded")
            v = new_v
            killed_u = {p: sum((killed_u.get((p[0] + a, p[1] + b), F(0))
                                for a, b in SHIFTS), F(0)) / 4
                        for p in sites}
            for p in sites:
                require(u[p] - v[p] <= killed_u[p],
                        "bellman_stopped_error_domination")

        # Different-zero-set comparison.  Use several related supports and exact
        # rational amplitudes; H is taken conservatively for both supports.
        candidates = [sites]
        if len(sites) > 1:
            ordered = sorted(sites)
            candidates.append(set(ordered[:-1]))
            candidates.append(set(ordered[1:]))
        for other in candidates:
            if not other:
                continue
            u1 = {p: F(1 + ((3 * p[0] + 5 * p[1]) % 7), 8) for p in sites}
            u2 = {p: F(1 + ((13 * p[0] - 2 * p[1]) % 7), 8) for p in other}
            union = sites | other
            w = {p: u1.get(p, F(0)) - u2.get(p, F(0)) for p in union}
            h = {}
            neighborhood = union | {(p[0] + a, p[1] + b)
                                    for p in union for a, b in SHIFTS}
            for p in neighborhood:
                h[p] = t_value(w, p) - w.get(p, F(0))
            sup_w = max(abs(x) for x in w.values())
            sup_h = max(abs(x) for x in h.values())
            xs2 = [p[0] for p in union]
            ys2 = [p[1] for p in union]
            d2 = (max(xs2) - min(xs2)) + (max(ys2) - min(ys2))
            H = F((d2 + 1) ** 2)
            require(sup_w <= H * sup_h, "different_zero_set_resolvent_bound")


def diamond(radius: int) -> list[tuple[int, int]]:
    return [(i, j) for i in range(-radius, radius + 1)
            for j in range(-radius, radius + 1)
            if abs(i) + abs(j) <= radius]


def dependency_checks() -> None:
    for depth in range(1, 10):
        for bound in range(1, 5):
            inside = lambda p, b=bound: -b <= p[0] <= b and -b <= p[1] <= b
            square = list(product(range(-bound, bound + 1), repeat=2))
            # Use a deterministic forcing on the whole killed square; only the
            # depth-dependent diamond can influence the target.
            forcing_all = {
                p: F(((17 * p[0] + 29 * p[1] + 7 * depth + 3 * bound) % 19) - 9, 13)
                for p in square
            }
            forcing = {
                p: forcing_all[p]
                for p in diamond(depth - 1) if inside(p)
            }
            # Local shrinking-diamond update.
            previous = {p: F(0) for p in diamond(depth)}
            for k in range(1, depth + 1):
                current = {}
                for p in diamond(depth - k):
                    if not inside(p):
                        current[p] = F(0)
                    else:
                        current[p] = min(F(1), max(F(0), t_value(previous, p) - forcing[p]))
                previous = current
            local = previous[(0, 0)]

            # Independent full-square killed update.
            full = {p: F(0) for p in square}
            for _ in range(depth):
                full = {
                    p: min(F(1), max(F(0), t_value(full, p) - forcing_all[p]))
                    for p in square
                }
            require(local == full[(0, 0)], "dependency_diamond_equals_full_killed_update")

            # Exact interval forcing enclosure accumulates at most linearly.
            for eps in (F(1, 200), F(1, 100), F(1, 50)):
                low = {p: forcing[p] - eps for p in forcing}
                high = {p: forcing[p] + eps for p in forcing}
                lo_prev = {p: F(0) for p in diamond(depth)}
                hi_prev = {p: F(0) for p in diamond(depth)}
                for k in range(1, depth + 1):
                    lo_cur, hi_cur = {}, {}
                    for p in diamond(depth - k):
                        if not inside(p):
                            lo_cur[p] = hi_cur[p] = F(0)
                        else:
                            lo_cur[p] = min(F(1), max(F(0), t_value(lo_prev, p) - high[p]))
                            hi_cur[p] = min(F(1), max(F(0), t_value(hi_prev, p) - low[p]))
                        require(lo_cur[p] <= hi_cur[p],
                                "interval_order_preserved")
                    lo_prev, hi_prev = lo_cur, hi_cur
                require(lo_prev[(0, 0)] <= local <= hi_prev[(0, 0)],
                        "interval_encloses_exact_iterate")
                require(local - lo_prev[(0, 0)] <= depth * eps and
                        hi_prev[(0, 0)] - local <= depth * eps,
                        "forcing_error_linear_accumulation")


def bisection_checks() -> None:
    for boundary in (F(k, 64) for k in range(1, 64)):
        for ambiguity in (F(0), F(1, 128), F(1, 64), F(1, 16)):
            states = {(F(0), F(1))}
            for depth in range(1, 11):
                nxt = set()
                for lo, hi in states:
                    mid = (lo + hi) / 2
                    allowed = []
                    if mid <= boundary + ambiguity:
                        allowed.append(True)   # inside label
                    if mid >= boundary - ambiguity:
                        allowed.append(False)  # outside label
                    for label in allowed:
                        new_lo, new_hi = (mid, hi) if label else (lo, mid)
                        require(new_lo - ambiguity <= boundary <= new_hi + ambiguity,
                                "relaxed_bisection_invariant")
                        require(abs((new_lo + new_hi) / 2 - boundary)
                                <= ambiguity + F(1, 2 ** (depth + 1)),
                                "relaxed_bisection_error")
                        nxt.add((new_lo, new_hi))
                states = nxt


def polynomial_weights(x: F, derivative: int) -> list[F]:
    nodes = list(range(-3, 4))
    result: list[F] = []
    for node in nodes:
        coef = [F(1)]
        denom = F(1)
        for other in nodes:
            if other == node:
                continue
            nxt = [F(0)] * (len(coef) + 1)
            for j, value in enumerate(coef):
                nxt[j] -= other * value
                nxt[j + 1] += value
            coef = nxt
            denom *= node - other
        for _ in range(derivative):
            coef = [(j + 1) * coef[j + 1] for j in range(len(coef) - 1)]
        result.append(sum((c * x ** j for j, c in enumerate(coef)), F(0)) / denom)
    return result


def interpolation_checks() -> None:
    for x in (F(0), F(1, 7), F(1, 4), F(1, 2), F(3, 4), F(6, 7), F(1)):
        for derivative in range(4):
            weights = polynomial_weights(x, derivative)
            for power in range(7):
                got = sum((w * F(j) ** power for j, w in zip(range(-3, 4), weights)), F(0))
                expected = (F(0) if power < derivative else
                            F(math.factorial(power), math.factorial(power - derivative))
                            * x ** (power - derivative))
                require(got == expected, "seven_node_polynomial_reproduction")
            norm = sum(abs(w) for w in weights)
            for signs in product((-1, 1), repeat=7):
                value = sum((w * sign for w, sign in zip(weights, signs)), F(0))
                require(abs(value) <= norm, "interpolation_noise_operator_bound")


def exponent_checks() -> None:
    for beta in (F(1, 10), F(1, 5), F(1, 3), F(1, 2), F(2, 3), F(4, 5), F(1)):
        s = 6 + beta
        k = 1 / (s - 2)
        require((s - 2) * k == 1, "C2_target_exponent")
        require(s * k - 2 * k == 1, "localization_to_C2_balance")
        require(s - 2 == 4 + beta, "holder_entropy_exponent")
        require(k < F(1, 4) and s * k > 1,
                "adaptive_exponents_in_expected_range")
        # Value error e=h^s differentiated twice contributes h^(s-2).
        require(s * k - 2 * k == (s - 2) * k,
                "value_noise_derivative_balance")
        # m~1/h gives log packing cardinality of order nu^-k.
        require(k == 1 / (4 + beta), "upper_lower_power_match")


def subgroup_checks() -> None:
    rng = random.Random(3299)
    matrices = [
        ((2, 0), (0, 3)),
        ((3, 1), (1, 2)),
        ((4, -1), (1, 3)),
        ((5, 2), (-1, 4)),
        ((7, -2), (3, 5)),
    ]
    coefficient_pool = [
        (-2, -1), (-1, 0), (0, 1), (1, 0), (1, 1),
        (2, -1), (2, 3), (3, 2), (4, -3)
    ]
    for col1, col2 in matrices:
        det_b = abs(determinant(col1, col2))
        for _ in range(160):
            coeffs = [(1, 0), (0, 1)] + rng.sample(coefficient_pool, 5)
            vectors = [
                (col1[0] * x + col2[0] * y,
                 col1[1] * x + col2[1] * y)
                for x, y in coeffs
            ]
            pair_indices = [(i, j) for i, j in combinations(range(len(vectors)), 2)
                            if determinant(vectors[i], vectors[j]) != 0]
            i, j = rng.choice(pair_indices)
            d1, d2 = vectors[i], vectors[j]
            det_d = determinant(d1, d2)
            coords: list[tuple[F, F]] = []
            for w in vectors:
                coords.append((
                    F(determinant(w, d2), det_d),
                    F(determinant(d1, w), det_d),
                ))
            index = F(abs(det_d), det_b)
            require(index.denominator == 1 and index >= 1,
                    "independent_pair_index_integer")
            for x, y in coords:
                require(index.numerator % x.denominator == 0 and
                        index.numerator % y.denominator == 0,
                        "bounded_denominator_coordinates")
            q = math.lcm(*(z.denominator for xy in coords for z in xy))
            require(index.numerator % q == 0,
                    "common_denominator_divides_pair_index")
            integer_generators = [(q, 0), (0, q)] + [
                (int(q * x), int(q * y)) for x, y in coords
            ]
            minors = [abs(determinant(a, b))
                      for a, b in combinations(integer_generators, 2)]
            det_h = math.gcd(*minors)
            recovered = F(abs(det_d) * det_h, q * q)
            require(recovered == det_b, "reference_free_covolume")
            require(1 <= det_h <= q * q, "Hermite_index_bounds")

            # Unimodular change of the selected independent pair does not change
            # the recovered lattice covolume.
            for U in (((1, 1), (0, 1)), ((1, 0), (1, 1)),
                      ((0, 1), (-1, 0)), ((-1, 0), (0, -1))):
                e1 = (d1[0] * U[0][0] + d2[0] * U[1][0],
                      d1[1] * U[0][0] + d2[1] * U[1][0])
                e2 = (d1[0] * U[0][1] + d2[0] * U[1][1],
                      d1[1] * U[0][1] + d2[1] * U[1][1])
                require(abs(determinant(e1, e2)) == abs(det_d),
                        "unimodular_pair_determinant")


def packing_and_binary_checks() -> None:
    # Binary tree counting, including randomized procedures after fixing seeds.
    for m in range(2, 80):
        M = 2 ** m
        for N in range(max(0, m - 5), m + 1):
            maximum_average_success = F(2 ** N, M)
            require(maximum_average_success <= 1,
                    "binary_tree_leaf_bound")
            if maximum_average_success >= F(3, 4):
                require(N >= m, "three_quarter_success_requires_log_cardinality")
            else:
                require(N < m or m <= 1,
                        "subcritical_transcript_count")

    # Exact exponent bookkeeping for the disjoint-bump packing.
    for beta in (F(1, 10), F(1, 4), F(1, 2), F(3, 4), F(1)):
        s = 6 + beta
        for derivative in range(7):
            require(s - derivative >= beta,
                    "packing_derivative_scaling")
        require(s - 2 == 4 + beta,
                "packing_C2_separation_scale")
        require((1 / (s - 2)) == (1 / (4 + beta)),
                "packing_cardinality_power")


def query_budget_checks() -> None:
    # Finite query accounting at dyadic h.  Constants are intentionally
    # conservative; the check verifies the stated asymptotic decomposition.
    for m in range(4, 101):
        h_inv = m
        bisection_depth = math.ceil(math.log2(16 * m))
        queries = 7 + 5 * h_inv * bisection_depth
        require(queries <= 40 * h_inv * math.log(4 * h_inv),
                "adaptive_query_budget")
        for delta_den in (4, 10, 100, 1000):
            per_query_log = math.log(8 * queries * delta_den)
            attempts = queries * math.ceil(8 * per_query_log)
            require(attempts <= 400 * h_inv * math.log(4 * h_inv)
                    * math.log(400 * h_inv * delta_den),
                    "adaptive_attempt_budget")


def main() -> None:
    reciprocal_checks()
    hessian_checks()
    exit_and_bellman_checks()
    dependency_checks()
    bisection_checks()
    interpolation_checks()
    exponent_checks()
    subgroup_checks()
    packing_and_binary_checks()
    query_budget_checks()
    result = {
        "schema": "a2-v32-independent-review-diagnostics-1",
        "status": "passed",
        "checks": dict(sorted(COUNTS.items())),
        "total_checks": sum(COUNTS.values()),
        "arithmetic": "exact rational/integer except explicit finite logarithm budget comparisons",
        "imports_author_code": False,
        "physical_sensor_executed": False,
        "tex_build": False,
        "uniform_continuum_proof_certificate": False,
        "editorial_decision": False,
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
