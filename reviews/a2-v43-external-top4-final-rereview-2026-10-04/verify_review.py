#!/usr/bin/env python3
"""Independent finite diagnostics for the A2 v43 final referee review.

The program imports no author code.  It checks finite exact models of the
endpoint/prefix inverse, protected stopping, signed shared records, moment
factorization, and the v43 default-vs-retained resource hierarchy.  It is not
a continuum proof certificate, a TeX build, a physical experiment, a human
specialist report, or a journal decision.  Every check remains active under
``python -O``.
"""
from __future__ import annotations

from collections import Counter
from fractions import Fraction as F
from itertools import product
import json
import math
import sys

CHECKS: Counter[str] = Counter()
METRICS: dict[str, object] = {}


def require(condition: bool, group: str, detail: str = "") -> None:
    if not condition:
        raise RuntimeError(f"{group}: {detail}")
    CHECKS[group] += 1


def in_union(x: F, intervals: tuple[tuple[F, F], ...]) -> bool:
    return any(left <= x <= right for left, right in intervals)


def segment_intersects(x: F, y: F, intervals: tuple[tuple[F, F], ...]) -> bool:
    lo, hi = min(x, y), max(x, y)
    return any(max(lo, left) <= min(hi, right) for left, right in intervals)


def collision_bit(start: F, displacement: F,
                  intervals: tuple[tuple[F, F], ...]) -> int:
    if in_union(start, intervals):
        return 0
    return int(segment_intersects(start, start + displacement, intervals))


def endpoint_identity() -> None:
    configurations = (
        ((F(-3), F(-2)), (F(0), F(1))),
        ((F(-5, 2), F(-3, 2)), (F(1, 2), F(5, 2))),
        ((F(-4), F(-7, 2)), (F(-1), F(0)), (F(2), F(5, 2))),
        ((F(-7, 4), F(-5, 4)), (F(1, 4), F(3, 4)), (F(9, 4), F(11, 4))),
    )
    displacements = tuple(F(k, 4) for k in range(-6, 7) if k)
    starts = tuple(F(k, 8) for k in range(-48, 49))
    cases = 0
    boundary_cases = 0
    for intervals, a, y in product(configurations, displacements, starts):
        lhs = collision_bit(y, a, intervals) - collision_bit(y + a, -a, intervals)
        rhs = int(in_union(y + a, intervals)) - int(in_union(y, intervals))
        require(lhs == rhs, "endpoint_bit_identity", f"{intervals},{a},{y}")
        boundary_cases += int(any(y in pair or y + a in pair for pair in intervals))
        cases += 1
    require(boundary_cases > 0, "endpoint_boundary_cases_exercised")
    METRICS["endpoint_identity_cases"] = cases
    METRICS["endpoint_boundary_cases"] = boundary_cases


def prefix_inverse_and_stability() -> None:
    values = (F(0), F(1, 4), F(1, 2), F(3, 4), F(1))
    inverse_cases = 0
    stability_cases = 0
    for length in range(2, 8):
        for seq in product(values, repeat=length):
            if F(0) not in seq:
                continue
            increments = [seq[k + 1] - seq[k] for k in range(length - 1)]
            prefixes = [F(0)]
            total = F(0)
            for r in increments:
                total -= r
                prefixes.append(total)
            require(max(prefixes) == seq[0], "finite_prefix_inverse")
            inverse_cases += 1

            if length <= 6 and inverse_cases % 7 == 0:
                for seed in range(3):
                    error = [F(((5 * k + 3 * seed) % 9) - 4, 500)
                             for k in range(length - 1)]
                    perturbed = [r + e for r, e in zip(increments, error)]
                    p0 = [F(0)]
                    p1 = [F(0)]
                    a0 = a1 = F(0)
                    for r, rp in zip(increments, perturbed):
                        a0 -= r
                        a1 -= rp
                        p0.append(a0)
                        p1.append(a1)
                    max_error = max((abs(e) for e in error), default=F(0))
                    require(abs(max(p0) - max(p1))
                            <= (length - 1) * max_error,
                            "finite_prefix_lipschitz")
                    stability_cases += 1
    METRICS["prefix_inverse_cases"] = inverse_cases
    METRICS["prefix_stability_cases"] = stability_cases


def distance_to_interval(x: F, interval: tuple[F, F]) -> F:
    left, right = interval
    if x < left:
        return left - x
    if x > right:
        return x - right
    return F(0)


def protected_first_exit() -> None:
    cases = 0
    parameters = product(
        (F(1), F(3, 2), F(2)),
        (F(1, 10), F(1, 5), F(1, 4)),
        (F(1, 8), F(1, 5), F(1, 3)),
        (F(1), F(3, 2)),
    )
    for plen, rho, t, gap in parameters:
        if rho + t >= gap:
            continue
        p = (F(0), plen)
        q = (-rho, plen + rho)
        others = ((plen + gap, plen + gap + 1),
                  (-gap - 1, -gap))
        k_bound = math.ceil(float((q[1] - q[0]) / t)) + 1
        for i in range(41):
            x = q[0] + (q[1] - q[0]) * F(i, 40)
            m = 1
            while q[0] <= x + m * t <= q[1]:
                m += 1
            y = x + m * t
            require(1 <= m <= k_bound, "protected_exit_bound")
            require(not (q[0] <= y <= q[1]), "protected_exit_outside_polygon")
            require(distance_to_interval(y, p) <= rho + t,
                    "protected_exit_distance")
            require(distance_to_interval(y, p) < gap,
                    "protected_exit_gap_strict")
            require(not any(left <= y <= right for left, right in others),
                    "protected_exit_other_components")

            def occupation(z: F) -> F:
                if not (p[0] <= z <= p[1]):
                    return F(0)
                return F(1, 5) + F(3, 5) * z * (plen - z) / (plen * plen)

            telescoped = sum(occupation(x + j * t) - occupation(x + (j + 1) * t)
                             for j in range(m))
            require(telescoped == occupation(x), "protected_prefix_telescoping")
            cases += 1
    METRICS["protected_first_exit_cases"] = cases


def signed_record_unbiasedness() -> None:
    cases = 0
    negative_increments = 0
    for k_bound in range(1, 13):
        for m in range(1, k_bound + 1):
            for seed in range(24):
                values = [F((7 * seed + 5 * j + j * j) % 21, 20)
                          for j in range(m)] + [F(0)]
                d = [values[j] - values[j + 1] for j in range(m)]
                negative_increments += sum(int(x < 0) for x in d)
                expected = F(0)
                for ell in range(k_bound):
                    active = ell < m
                    delta = d[ell] if active else F(0)
                    p_plus = F(1, 2) - delta / 2
                    p_minus = F(1, 2) + delta / 2
                    require(F(0) <= p_plus <= 1 and F(0) <= p_minus <= 1,
                            "signed_record_probability_range")
                    table_expectation = F(0)
                    for y_plus, y_minus in product((0, 1), repeat=2):
                        prob = ((p_plus if y_plus else 1 - p_plus)
                                * (p_minus if y_minus else 1 - p_minus))
                        z = k_bound * int(active) * (y_minus - y_plus)
                        table_expectation += prob * z
                    require(table_expectation == k_bound * delta,
                            "signed_two_bit_expectation")
                    expected += table_expectation / k_bound
                require(expected == values[0], "signed_shared_record_unbiased")
                cases += 1
    require(negative_increments > 0, "signed_negative_records_exercised")
    METRICS["signed_record_cases"] = cases
    METRICS["negative_active_increments"] = negative_increments


def multi_indices(max_degree: int):
    for total in range(max_degree + 1):
        for i in range(total + 1):
            yield (i, total - i)


def midpoint_shared_moments() -> None:
    cases = 0
    for q in (2, 4, 8):
        ell = F(2, q)
        coords = tuple(-F(1) + (F(i) + F(1, 2)) * ell for i in range(q))
        nodes = tuple(product(coords, coords))
        area = F(4)
        require(area / len(nodes) == ell * ell, "midpoint_area_scaling")
        for seed in range(12):
            v = {x: F((seed + 3 * ix + 5 * iy + ix * iy) % 17, 16)
                 for ix, x0 in enumerate(coords)
                 for iy, y0 in enumerate(coords)
                 for x in [(x0, y0)]}
            for alpha in multi_indices(8):
                shared_expectation = area * sum(
                    (x[0] ** alpha[0]) * (x[1] ** alpha[1]) * v[x]
                    for x in nodes) / len(nodes)
                midpoint_sum = ell * ell * sum(
                    (x[0] ** alpha[0]) * (x[1] ** alpha[1]) * v[x]
                    for x in nodes)
                require(shared_expectation == midpoint_sum,
                        "shared_moment_record_scaling")
                cases += 1
    METRICS["shared_moment_cases"] = cases


def moment(dist: tuple[tuple[tuple[F, F], F], ...], alpha: tuple[int, int]) -> F:
    return sum(weight * point[0] ** alpha[0] * point[1] ** alpha[1]
               for point, weight in dist)


def difference_distribution(u_dist, z_dist):
    out = []
    for u, wu in u_dist:
        for z, wz in z_dist:
            out.append(((u[0] - z[0], u[1] - z[1]), wu * wz))
    return tuple(out)


def binom(n: int, k: int) -> int:
    return math.comb(n, k)


def moment_factorization() -> None:
    cases = 0
    conditioning_cases = 0
    for seed in range(40):
        u_weights = (F(1, 5), F(3, 10), F(1, 2))
        z_weights = (F(1, 4), F(1, 3), F(5, 12))
        u_points = (
            (F(-2 + seed % 3, 5), F(1, 3)),
            (F(1, 4), F(-1 + seed % 2, 4)),
            (F(2, 5), F(1 + seed % 4, 10)),
        )
        z_points = (
            (F(-1, 3), F(2 - seed % 3, 7)),
            (F(1 + seed % 2, 5), F(-2, 5)),
            (F(3, 7), F(1, 6)),
        )
        u_dist = tuple(zip(u_points, u_weights))
        z_dist = tuple(zip(z_points, z_weights))
        y_dist = difference_distribution(u_dist, z_dist)
        u_mom = {a: moment(u_dist, a) for a in multi_indices(10)}
        y_mom = {a: moment(y_dist, a) for a in multi_indices(10)}
        recovered: dict[tuple[int, int], F] = {(0, 0): F(1)}
        for total in range(1, 11):
            for alpha in multi_indices(total):
                if sum(alpha) != total:
                    continue
                rest = F(0)
                for b0 in range(alpha[0] + 1):
                    for b1 in range(alpha[1] + 1):
                        beta = (b0, b1)
                        if beta == alpha:
                            continue
                        coeff = (binom(alpha[0], b0) * binom(alpha[1], b1)
                                 * (-1) ** (b0 + b1))
                        rest += coeff * u_mom[(alpha[0] - b0, alpha[1] - b1)] * recovered[beta]
                sign = F((-1) ** total)
                recovered[alpha] = (y_mom[alpha] - rest) / sign
                require(recovered[alpha] == moment(z_dist, alpha),
                        "triangular_factor_moment_recovery")
                cases += 1

        a_tol = F(1, 10**8)
        perturbed_u = {a: value + (a_tol if (a[0] + 2 * a[1] + seed) % 2 else -a_tol)
                       for a, value in u_mom.items()}
        perturbed_y = {a: value + (a_tol if (2 * a[0] + a[1] + seed) % 2 else -a_tol)
                       for a, value in y_mom.items()}
        recovered2: dict[tuple[int, int], F] = {(0, 0): F(1)}
        for total in range(1, 9):
            for alpha in multi_indices(total):
                if sum(alpha) != total:
                    continue
                rest = F(0)
                for b0 in range(alpha[0] + 1):
                    for b1 in range(alpha[1] + 1):
                        beta = (b0, b1)
                        if beta == alpha:
                            continue
                        coeff = (binom(alpha[0], b0) * binom(alpha[1], b1)
                                 * (-1) ** (b0 + b1))
                        rest += coeff * perturbed_u[(alpha[0] - b0, alpha[1] - b1)] * recovered2[beta]
                recovered2[alpha] = (perturbed_y[alpha] - rest) / F((-1) ** total)
                discrepancy = abs(recovered2[alpha] - moment(z_dist, alpha))
                require(discrepancy <= 2 * a_tol * 8 ** total * math.factorial(total),
                        "factorial_conditioning_bound")
                conditioning_cases += 1
    METRICS["factor_moment_cases"] = cases
    METRICS["factor_conditioning_cases"] = conditioning_cases


def resource_and_dependency_checks() -> None:
    budget_cases = 0
    exponent_cases = 0
    for m in range(2, 41):
        for power in range(4, 4 * m + 1, max(1, m // 4)):
            a = 2.0 ** (-power)
            for delta in (0.2, 0.05, 0.01):
                c = 8.0
                default = a ** -2 * math.log(c * m / delta)
                alternative = m * m * a ** -4 * math.log(c * m / (a * delta))
                require(default < alternative, "default_budget_smaller_than_all_node")
                budget_cases += 1

        eps = 1.0 / m
        c1 = 4.0
        exponent = math.ceil(c1 * m * math.log2(c1 * m))
        log_default = 2 * exponent * math.log(2.0) + math.log(math.log(16 * m / 0.05))
        scale = eps ** -1 * math.log(16 / eps)
        require(log_default <= 8 * scale, "joint_exponential_scale")
        exponent_cases += 1

    graph = {
        "prefix": (),
        "finite_auxiliaries": (),
        "patch_margin": (),
        "moment_conditioning": (),
        "geometry": ("prefix", "finite_auxiliaries"),
        "default_moments": ("geometry", "prefix"),
        "deterministic_moments": ("geometry", "prefix"),
        "common_positive_factor": ("geometry", "moment_conditioning"),
        "default_joint": ("geometry", "default_moments", "common_positive_factor"),
        "deterministic_joint": ("geometry", "deterministic_moments", "common_positive_factor"),
        "prediction": ("default_joint",),
        "finite_period_decision": ("geometry", "patch_margin"),
    }
    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(node: str) -> None:
        require(node not in visiting, "dependency_graph_acyclic", node)
        if node in visited:
            return
        visiting.add(node)
        for parent in graph[node]:
            require(parent in graph, "dependency_graph_defined", parent)
            visit(parent)
        visiting.remove(node)
        visited.add(node)

    for node in graph:
        visit(node)
    require(len(visited) == len(graph), "dependency_graph_complete")
    METRICS["budget_cases"] = budget_cases
    METRICS["exponent_cases"] = exponent_cases
    METRICS["dependency_nodes"] = len(graph)


def run() -> dict:
    endpoint_identity()
    prefix_inverse_and_stability()
    protected_first_exit()
    signed_record_unbiasedness()
    midpoint_shared_moments()
    moment_factorization()
    resource_and_dependency_checks()
    return {
        "schema": "a2-v43-independent-final-review-diagnostics-1",
        "status": "passed",
        "reviewed_commit": "4557df22f5c72bc80943690ecd6c2e39de3734ab",
        "checks": dict(sorted(CHECKS.items())),
        "total_checks": sum(CHECKS.values()),
        "metrics": dict(sorted(METRICS.items())),
        "scope": (
            "Finite exact algebra and finite models for the endpoint/prefix, "
            "protected signed-record, moment-factor and resource chains. "
            "Not a continuum proof certificate, TeX build, physical sensor test, "
            "human specialist review, or journal decision."
        ),
        "imports_author_code": False,
        "runtime_dependencies": "Python standard library only",
        "formal_proof_certificate": False,
        "human_specialist_review": False,
        "physical_sensor_executed": False,
    }


def main() -> int:
    try:
        result = run()
        code = 0
    except (RuntimeError, ArithmeticError, ValueError) as exc:
        result = {
            "schema": "a2-v43-independent-final-review-diagnostics-1",
            "status": "failed",
            "error": str(exc),
            "formal_proof_certificate": False,
            "human_specialist_review": False,
            "physical_sensor_executed": False,
        }
        code = 1
    print(json.dumps(result, sort_keys=True, separators=(",", ":")))
    return code


if __name__ == "__main__":
    sys.exit(main())
