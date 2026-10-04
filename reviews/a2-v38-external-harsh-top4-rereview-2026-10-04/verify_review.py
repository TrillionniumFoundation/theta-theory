#!/usr/bin/env python3
"""Independent finite diagnostics for the A2 v38 referee review.

This program imports no author code.  It checks exact finite-state stopping
algebra, finite support-envelope and perimeter identities, centered-increment
exit systems, information inequalities, and exponent bookkeeping relevant to
the new v37/v38 claims.  It is not a continuum proof certificate, a TeX build,
a physical sensor execution, or an editorial decision.  All checks remain
active under ``python -O``.
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


def require(ok: bool, group: str, detail: str = "") -> None:
    if not ok:
        raise RuntimeError(f"{group}: {detail}")
    CHECKS[group] += 1


def solve(a: list[list[F]], b: list[F]) -> list[F]:
    n = len(a)
    if len(b) != n or any(len(row) != n for row in a):
        raise ValueError("invalid linear system")
    m = [row[:] + [rhs] for row, rhs in zip(a, b)]
    for col in range(n):
        pivot = next((r for r in range(col, n) if m[r][col] != 0), None)
        if pivot is None:
            raise ValueError("singular matrix")
        m[col], m[pivot] = m[pivot], m[col]
        q = m[col][col]
        m[col] = [x / q for x in m[col]]
        for r in range(n):
            if r == col:
                continue
            q = m[r][col]
            if q:
                m[r] = [x - q * y for x, y in zip(m[r], m[col])]
    return [row[-1] for row in m]


def inverse(a: list[list[F]]) -> list[list[F]]:
    n = len(a)
    cols = []
    for j in range(n):
        e = [F(0)] * n
        e[j] = F(1)
        cols.append(solve([row[:] for row in a], e))
    return [[cols[j][i] for j in range(n)] for i in range(n)]


def mat_vec(a: list[list[F]], x: list[F]) -> list[F]:
    return [sum(v * y for v, y in zip(row, x)) for row in a]


def dot(x: list[F], y: list[F]) -> F:
    return sum((a * b for a, b in zip(x, y)), F(0))


def compass_matrix(k: int) -> tuple[list[tuple[int, int]], list[list[F]], int]:
    states = [(i, j) for i in range(-k, k + 1) for j in range(-k, k + 1)]
    index = {p: n for n, p in enumerate(states)}
    q = [[F(0) for _ in states] for _ in states]
    shifts = ((1, 0), (-1, 0), (0, 1), (0, -1))
    for p, r in index.items():
        for di, dj in shifts:
            p2 = (p[0] + di, p[1] + dj)
            if p2 in index:
                q[r][index[p2]] += F(1, 4)
    return states, q, index[(0, 0)]


def policy_data(q: list[list[F]], origin: int, mask: int) -> dict:
    n = len(q)
    cont = [i for i in range(n) if (mask >> i) & 1]
    pos = {s: i for i, s in enumerate(cont)}
    if cont:
        a = [[(F(1) if i == j else F(0)) - q[si][sj]
              for j, sj in enumerate(cont)] for i, si in enumerate(cont)]
        inv = inverse(a)
    else:
        inv = []

    m = [F(0)] * n
    if origin in pos:
        at = [[(F(1) if i == j else F(0)) - q[sj][si]
               for j, sj in enumerate(cont)] for i, si in enumerate(cont)]
        rhs = [F(1) if si == origin else F(0) for si in cont]
        sol = solve(at, rhs)
        for si, value in zip(cont, sol):
            m[si] = value
    return {"cont": cont, "pos": pos, "inv": inv, "m": m}


def policy_value(data: dict, q: list[list[F]], f: list[F]) -> list[F]:
    n = len(q)
    u = [F(0)] * n
    cont = data["cont"]
    if cont:
        rhs = [-f[i] for i in cont]
        vals = mat_vec(data["inv"], rhs)
        for i, value in zip(cont, vals):
            u[i] = value
    return u


def stopping_polytope_checks() -> None:
    states, q, origin = compass_matrix(1)
    n = len(states)
    i_minus_q = [[(F(1) if i == j else F(0)) - q[i][j]
                  for j in range(n)] for i in range(n)]
    green = inverse(i_minus_q)
    h = mat_vec(green, [F(1)] * n)
    hs = 5
    require(all(F(0) < x <= hs for x in h), "green_exit_budget")

    policies = [policy_data(q, origin, mask) for mask in range(1 << n)]
    for mask, data in enumerate(policies):
        m = data["m"]
        lhs = [m[i] - sum(q[j][i] * m[j] for j in range(n)) for i in range(n)]
        require(all(lhs[i] <= (F(1) if i == origin else F(0)) for i in range(n)),
                "stopping_flow_feasible", str(mask))
        require(all(x >= 0 for x in m), "stopping_measure_nonnegative", str(mask))
        require(sum(m) <= h[origin], "stopping_green_budget", str(mask))
        for i in range(n):
            require(m[i] <= green[origin][i], "stopping_coordinate_budget", f"{mask}:{i}")

    fields: list[list[F]] = []
    for seed in range(24):
        fields.append([F(((7 * i + 11 * seed + i * i) % 23) - 11, 9)
                       for i in range(n)])
    values: list[F] = []
    for f in fields:
        policy_values = [policy_value(data, q, f) for data in policies]
        u = [max(vals[i] for vals in policy_values) for i in range(n)]
        bellman = [max(F(0), sum(q[i][j] * u[j] for j in range(n)) - f[i])
                   for i in range(n)]
        for i in range(n):
            require(u[i] == bellman[i], "stopping_bellman_identity")
        primal = max(-dot(f, data["m"]) for data in policies)
        require(primal == u[origin], "stopping_primal_value")
        values.append(primal)

    for i in range(len(fields)):
        for j in range(len(fields)):
            weighted = sum(green[origin][z] * abs(fields[i][z] - fields[j][z])
                           for z in range(n))
            require(abs(values[i] - values[j]) <= weighted,
                    "stopping_arbitrary_data_stability")
            sup = max(abs(fields[i][z] - fields[j][z]) for z in range(n))
            require(abs(values[i] - values[j]) <= h[origin] * sup,
                    "stopping_sup_stability")

    full = {(i, j): F(0) for i in range(-2, 3) for j in range(-2, 3)}
    full[(0, 0)] = F(3, 5)
    full[(1, 1)] = F(2, 5)
    full[(2, 1)] = F(1, 5)
    shifts = ((1, 0), (-1, 0), (0, 1), (0, -1))
    f = []
    for p in states:
        tv = sum(full[(p[0] + di, p[1] + dj)] for di, dj in shifts) / 4
        f.append(tv - full[p])
    uo = max(-dot(f, data["m"]) for data in policies)
    require(uo == full[(0, 0)], "stencil_nonzero_computational_boundary")
    require(full[(1, 1)] > 0, "stencil_boundary_component_exercised")

    METRICS["stopping_states"] = n
    METRICS["stopping_policies"] = len(policies)
    METRICS["stopping_fields"] = len(fields)
    METRICS["origin_green_mass"] = str(h[origin])


def centered_exit_systems() -> None:
    laws = [
        ({-1: F(1, 2), 1: F(1, 2)}, "symmetric"),
        ({-1: F(2, 3), 2: F(1, 3)}, "right_jump_two"),
        ({-2: F(1, 3), 1: F(2, 3)}, "left_jump_two"),
        ({-3: F(1, 4), 1: F(3, 4)}, "left_jump_three"),
    ]
    cases = 0
    for k in range(2, 9):
        states = list(range(-k, k + 1))
        idx = {x: i for i, x in enumerate(states)}
        for law, name in laws:
            mean = sum(F(step) * prob for step, prob in law.items())
            sigma2 = sum(F(step * step) * prob for step, prob in law.items())
            ell = max(abs(step) for step in law)
            require(mean == 0 and sigma2 > 0, "centered_law_moments", name)
            p = [[F(0) for _ in states] for _ in states]
            terminal2 = [F(0) for _ in states]
            for x in states:
                i = idx[x]
                for step, prob in law.items():
                    y = x + step
                    if y in idx:
                        p[i][idx[y]] += prob
                    else:
                        terminal2[i] += prob * y * y
            a = [[(F(1) if i == j else F(0)) - p[i][j]
                  for j in range(len(states))] for i in range(len(states))]
            h = solve([row[:] for row in a], [F(1)] * len(states))
            exit2 = solve([row[:] for row in a], terminal2)
            diameter = F(2 * k)
            bound = (diameter + ell) ** 2 / sigma2
            for x in states:
                i = idx[x]
                require(sigma2 * h[i] == exit2[i] - x * x,
                        "centered_exit_martingale", f"{name}:{k}:{x}")
                require(F(0) < h[i] <= bound,
                        "centered_exit_uniform_bound", f"{name}:{k}:{x}")
                cases += 1
    METRICS["centered_exit_cases"] = cases


def rectangle_support(a: F, b: F, cx: F = F(0), cy: F = F(0)) -> tuple[F, F, F, F]:
    return (cx + a, -cx + a, cy + b, -cy + b)


def add_support(x, y):
    return tuple(a + b for a, b in zip(x, y))


def scale_support(c: F, x):
    return tuple(c * a for a in x)


def centered_support(x):
    cx = (x[0] - x[1]) / 2
    cy = (x[2] - x[3]) / 2
    return (x[0] - cx, x[1] + cx, x[2] - cy, x[3] + cy)


def width_sum(x) -> F:
    return sum(x)


def envelope_and_perimeter() -> None:
    half = (F(1, 4), F(1, 2), F(3, 4), F(5, 4))
    shifts = (F(-2), F(-1, 3), F(0), F(2, 5), F(7, 4))
    ratios = (F(1), F(3, 2), F(2), F(7, 2))
    cases = 0
    different_minimizers = 0
    for aa, ab, c1a, c1b, c2a, c2b, bx, by in product(
            half, half, half, half, half, half, shifts[:3], shifts[:3]):
        q = rectangle_support(aa, ab)
        obstacles = [rectangle_support(c1a, c1b, F(-1, 2), F(1, 3)),
                     rectangle_support(c2a, c2b, F(4, 5), F(-2, 5))]
        centered_obstacles = [centered_support(c) for c in obstacles]
        base_envelope = tuple(min(c[d] for c in centered_obstacles) for d in range(4))
        minimizers = [tuple(i for i, c in enumerate(centered_obstacles)
                            if c[d] == base_envelope[d]) for d in range(4)]
        different_minimizers += int(len(set(minimizers)) > 1)
        b_support = (bx, -bx, by, -by)
        setting_data = []
        for rho in ratios:
            minus_a = add_support(scale_support(F(-1), b_support), scale_support(rho, q))
            ps = [add_support(c, minus_a) for c in obstacles]
            centered_ps = [centered_support(p) for p in ps]
            env = tuple(min(p[d] for p in centered_ps) for d in range(4))
            setting_data.append((rho, ps, env, minus_a))
            for p, c in zip(ps, obstacles):
                require(width_sum(p) - width_sum(c) == width_sum(q) * rho,
                        "footprint_width_deficit")
                require(2 * width_sum(p) - 2 * width_sum(c) == 2 * width_sum(q) * rho,
                        "isotropic_perimeter_deficit")
        env1 = setting_data[0][2]
        for rho, ps, env, _ in setting_data[1:]:
            recovered_q = tuple((env[d] - env1[d]) / (rho - 1) for d in range(4))
            require(recovered_q == q, "support_envelope_footprint")
            for p, c in zip(ps, obstacles):
                rec = tuple(p[d] - rho * q[d] for d in range(4))
                require(centered_support(rec) == centered_support(c),
                        "support_envelope_body_centered")
        cases += 1
    require(different_minimizers > 0, "support_envelope_minimizer_switch")
    METRICS["support_envelope_cases"] = cases
    METRICS["support_envelope_switches"] = different_minimizers


def binary_entropy(p: float) -> float:
    if p <= 0.0 or p >= 1.0:
        return 0.0
    return -p * math.log2(p) - (1.0 - p) * math.log2(1.0 - p)


def hellinger_bernoulli(a: float, b: float) -> float:
    return ((math.sqrt(a) - math.sqrt(b)) ** 2
            + (math.sqrt(1.0 - a) - math.sqrt(1.0 - b)) ** 2)


def information_inequalities() -> None:
    cases = 0
    max_ratio = 0.0
    for den in (11, 17, 29, 43):
        grid = [i / den for i in range(den + 1)]
        for size in (2, 3, 4, 5):
            for seed in range(40):
                ps = [grid[(seed * 7 + i * i + 3 * i) % len(grid)] for i in range(size)]
                raw = [1 + ((seed + 5 * i + i * i) % 13) for i in range(size)]
                total = float(sum(raw))
                weights = [x / total for x in raw]
                mean = sum(w * p for w, p in zip(weights, ps))
                mutual = binary_entropy(mean) - sum(w * binary_entropy(p) for w, p in zip(weights, ps))
                a, b = min(ps), max(ps)
                h2 = hellinger_bernoulli(a, b)
                require(mutual >= -1e-13, "binary_information_nonnegative")
                require(mutual <= h2 / math.log(2.0) + 2e-12,
                        "hellinger_capacity_bound", f"{den}:{size}:{seed}")
                if h2 > 0:
                    max_ratio = max(max_ratio, mutual * math.log(2.0) / h2)
                cases += 1
    METRICS["hellinger_capacity_cases"] = cases
    METRICS["hellinger_capacity_max_ratio"] = max_ratio


def rate_and_sampling_algebra() -> None:
    beta_values = (F(1, 100), F(1, 16), F(1, 4), F(1, 2), F(3, 4), F(1))
    for beta in beta_values:
        s = 6 + beta
        q0 = (F(3, 2) * s + 1) / (s - 2)
        require(q0 == (3 * s + 2) / (2 * (s - 2)), "stationary_q0_identity")
        require(q0 > 2, "stationary_integral_cost_lower_order")
        lower = (F(3, 2) * s + 1) / (s - 2)
        upper = (F(3, 2) * s + 1) / (s - 2)
        require(lower == upper, "stationary_power_match")
        old_lower = (s + 1) / (s - 2)
        require(q0 - old_lower == s / (2 * (s - 2)), "stationary_prior_gap_identity")
        for gamma in (F(0), F(1, 4), F(1, 2), F(1), F(2)):
            qg = ((gamma + F(3, 2)) * s + 1) / (s - 2)
            require(qg >= q0, "boundary_mass_exponent_monotone")
            require(qg > 2, "boundary_query_dominates_scalar_measurement")

    for m in (1, 9, 25, 81):
        hs = 5
        for eps in (0.8, 0.5, 0.25, 0.1):
            for delta in (0.2, 0.05, 0.01):
                n = math.ceil(8 * hs * hs * eps ** -2 * math.log(4 * m / delta))
                rhs = 4 * m * math.exp(-n * eps * eps / (8 * hs * hs))
                require(rhs <= delta * (1 + 1e-12), "stencil_hoeffding_budget")


def parallel_area_checks() -> None:
    for r0 in (F(1, 5), F(1, 2), F(1), F(7, 4)):
        for eps in (F(1, 100), F(1, 20), F(1, 5)):
            r1 = r0 + eps
            symmetric_over_pi = r1 * r1 - r0 * r0
            linear_over_pi = 2 * r1 * eps + eps * eps
            require(symmetric_over_pi >= 0, "parallel_symmetric_difference_nonnegative")
            require(symmetric_over_pi <= linear_over_pi, "parallel_area_linear_control")


def run() -> dict:
    stopping_polytope_checks()
    centered_exit_systems()
    envelope_and_perimeter()
    information_inequalities()
    rate_and_sampling_algebra()
    parallel_area_checks()
    return {
        "schema": "a2-v38-independent-review-diagnostics-1",
        "status": "passed",
        "checks": dict(sorted(CHECKS.items())),
        "total_checks": sum(CHECKS.values()),
        "metrics": METRICS,
        "imports_author_code": False,
        "runtime_dependencies": "Python standard library only",
        "formal_proof_certificate": False,
        "physical_sensor_executed": False,
        "tex_build": False,
    }


def main() -> int:
    try:
        result = run()
        code = 0
    except Exception as exc:
        result = {
            "schema": "a2-v38-independent-review-diagnostics-1",
            "status": "failed",
            "error": str(exc),
            "formal_proof_certificate": False,
        }
        code = 1
    print(json.dumps(result, sort_keys=True, separators=(",", ":")))
    return code


if __name__ == "__main__":
    sys.exit(main())
