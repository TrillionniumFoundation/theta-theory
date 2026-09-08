#!/usr/bin/env python3
"""Independent finite diagnostics for A1 v30, dc8c1bd475b870cd222627c0cfd6d784363e1728.

Python standard library only. No removable assertions, network access, or author
scripts. Exact rational arithmetic except display-only decimal conversions.
The continuum proofs and publication judgment are NOT certified by this script.
Run: python independent_checks.py > INDEPENDENT_CHECKS.json
     python -O independent_checks.py > optimized.json
"""
from __future__ import annotations
from collections import Counter
from fractions import Fraction as F
from itertools import combinations, product
import hashlib
import json
from pathlib import Path

COUNTS: Counter[str] = Counter()

def check(category: str, condition: bool, detail: str) -> None:
    COUNTS[category] += 1
    if not condition:
        raise RuntimeError(f"{category}: {detail}")

def solve(a: list[list[F]], b: list[F]) -> list[F] | None:
    """Exact square-system Gaussian elimination; singular systems return None."""
    n = len(b)
    rows = [list(map(F, row)) + [F(y)] for row, y in zip(a, b)]
    if len(rows) != n or any(len(row) != n + 1 for row in rows):
        raise ValueError("a square system is required")
    for c in range(n):
        pivot = next((r for r in range(c, n) if rows[r][c]), None)
        if pivot is None:
            return None
        rows[c], rows[pivot] = rows[pivot], rows[c]
        z = rows[c][c]
        rows[c] = [v / z for v in rows[c]]
        for r in range(n):
            if r != c and rows[r][c]:
                z = rows[r][c]
                rows[r] = [v - z*w for v, w in zip(rows[r], rows[c])]
    return [row[-1] for row in rows]

def primal(matrix: list[list[F]]) -> tuple[F, list[F]]:
    """Enumerate vertices of min_rho max_j sum_r rho_r A[r,j]."""
    r, j = len(matrix), len(matrix[0])
    constraints = []
    for k in range(j):
        constraints.append(([matrix[i][k] for i in range(r)] + [F(-1)], F(0)))
    for i in range(r):
        row = [F(0)] * (r + 1)
        row[i] = F(-1)
        constraints.append((row, F(0)))
    best = None
    for active in combinations(constraints, r):
        a = [[F(1)] * r + [F(0)]] + [c[0] for c in active]
        b = [F(1)] + [c[1] for c in active]
        z = solve(a, b)
        if z is None:
            continue
        if all(sum(v*w for v, w in zip(c, z)) <= y for c, y in constraints):
            if best is None or z[-1] < best[0]:
                best = (z[-1], z[:-1])
    if best is None:
        raise RuntimeError("no primal vertex found")
    return best

def game(matrix: list[list[F]]) -> tuple[F, list[F], list[F]]:
    value, rho = primal(matrix)
    # min_lambda max_r (-A^T lambda) is the negative dual value.
    transposed = [[-matrix[r][j] for r in range(len(matrix))]
                  for j in range(len(matrix[0]))]
    neg_dual, lam = primal(transposed)
    check("exact_games", value == -neg_dual, "primal/dual disagreement")
    check("exact_games", sum(rho) == sum(lam) == 1 and min(rho + lam) >= 0,
          "invalid simplex point")
    check("exact_games", all(sum(lam[j]*row[j] for j in range(len(lam))) >= value
                             for row in matrix), "invalid dual certificate")
    return value, rho, lam

def cube_root_floor(n: int) -> int:
    if n < 0:
        raise ValueError("nonnegative integer required")
    lo, hi = 0, 1 << ((n.bit_length() + 2) // 3)
    while lo + 1 < hi:
        mid = (lo + hi) // 2
        if mid**3 <= n:
            lo = mid
        else:
            hi = mid
    return hi if hi**3 <= n else lo

def density_u(u: F) -> F:
    if F(-8, 7) <= u <= 0:
        return 512 * (27/(8-5*u)**3 - 1/(8+3*u)**3)
    if 0 <= u <= F(8, 9):
        return 512 * (27/(8+3*u)**3 - 1/(8-5*u)**3)
    return F(0)

def integral_enclosure(n: int = 8192, scale: int = 10**12) -> tuple[F, F]:
    """Monotone endpoint sums for integral f(z)^(1/3) dz.

    f increases on [-8/7,0] and decreases on [0,8/9] in u=48(z-1/2).
    Their derivative signs are checked algebraically in the referee report;
    sampling alone is not offered as their proof.
    """
    low = F(0)
    high = F(0)
    for left, right, increasing in [(F(-8,7), F(0), True), (F(0), F(8,9), False)]:
        step = (right-left)/n
        bounds = []
        previous = None
        for i in range(n+1):
            f = density_u(left + i*step)
            check("density_enclosure", f >= 0, "negative endpoint density")
            if previous is not None:
                check("density_enclosure", (f >= previous) if increasing else (f <= previous),
                      "endpoint monotonicity diagnostic")
            previous = f
            radicand = (f.numerator * scale**3) // f.denominator
            b = cube_root_floor(radicand)
            check("density_enclosure", F(b**3, scale**3) <= f < F((b+1)**3, scale**3),
                  "integer cube-root bounds")
            bounds.append((b, b+1))
        lows = bounds[:-1] if increasing else bounds[1:]
        highs = bounds[1:] if increasing else bounds[:-1]
        low += step * sum(x[0] for x in lows) / (48*scale)
        high += step * sum(x[1] for x in highs) / (48*scale)
    return low, high

def partition_losses(labels: tuple[int, ...]) -> tuple[F, F]:
    points = list(product((F(1,4), F(3,4)), repeat=2))
    totals = [F(0), F(0)]
    for label in set(labels):
        cell = [p for p, l in zip(points, labels) if l == label]
        means = [sum(p[j] for p in cell)/len(cell) for j in range(2)]
        for p in cell:
            for j in range(2):
                totals[j] += (p[j]-means[j])**2/4
    return tuple(totals)

def run() -> dict:
    constant = 96*26**2*128
    check("physical_constants", constant == 8306688, "unit capacity cost")
    check("physical_constants", F(1,4)*(F(1,8)**2 + F(-1,8)**2) == F(1,128),
          "query isometry")
    check("physical_constants", F(5,16)+F(3,16)+F(1,2) == 1, "full law mass")
    check("physical_constants", F(8,15)-F(4,9) == F(4,45), "full support diameter")
    check("physical_constants", F(constant,128)*F(4,2025) == F(constant,64800) < 129,
          "all-budget ratio constant")
    for u, expected in [(F(-8,7), F(0)), (F(0), F(26)), (F(8,9), F(0))]:
        check("physical_constants", density_u(u) == expected, "density endpoint")
    # Integrals of the rational density on each monotonicity interval.
    def left_primitive(u: F) -> F:
        return F(512,48)*(F(27,10)/(8-5*u)**2 + F(1,6)/(8+3*u)**2)
    def right_primitive(u: F) -> F:
        return F(512,48)*(-F(9,2)/(8+3*u)**2 - F(1,10)/(8-5*u)**2)
    mass = left_primitive(F(0))-left_primitive(F(-8,7)) + right_primitive(F(8,9))-right_primitive(F(0))
    check("physical_constants", mass == F(1,2), "integrated continuous mass")
    # Let t=y^2; integrate 2*y*(x-1/2-b*y) on 0 <= y <= (x-1/2)/b.
    for b, x in product((F(2), F(7), F(103)), (F(0), F(1,2), F(2,3), F(1))):
        a = max(F(0), x-F(1,2))
        h = a/b
        integral = a*h*h-F(2,3)*b*h**3
        check("atom_costs", integral == a**3/(3*b*b), "cubic integral")

    menu_profiles = [lambda x: max(x,2*x-10), lambda x: F(3,2)*x]
    critical = [F(0), F(10), F(20)]
    regret = [max(p(x)-min(q(x) for q in menu_profiles) for x in critical)
              for p in menu_profiles]
    check("menu_stabilization", regret[1] == 5, "eventually optimal order bounded excess")
    check("menu_stabilization", menu_profiles[1](100) == min(p(100) for p in menu_profiles),
          "eventual exactness")
    check("menu_stabilization", menu_profiles[0](1000)-menu_profiles[1](1000) == 490,
          "prescribed excessive slope negative control")
    for c in (F(1), F(10), F(100)):
        check("menu_stabilization", max(c,F(2)*c-c) - F(1)*c == 0, "branch crossing")
        # max(x,2x-c) vs 1.5x: excess of latter peaks at x=c, value c/2.
        check("menu_stabilization", F(3,2)*c-max(c,2*c-c) == c/2,
              "fixed-calibration finite need not be calibration-uniform")

    games = []
    for j in range(2,6):
        a = [[F(1) if r == k else F(1,j*j) for k in range(j)] for r in range(j)]
        value, rho, lam = game(a)
        expected = F(1,j)+F(1,j*j)-F(1,j**3)
        check("checkpoint_penalty", value == expected, "diagonal gain matrix")
        check("checkpoint_penalty", value/F(1,j*j) == j+1-F(1,j), "consistency ratio")
        games.append({"J": j, "value": str(value), "primal": list(map(str,rho)),
                      "dual": list(map(str,lam)), "separate_value": str(F(1,j*j))})
    for j in range(6,65):
        expected = F(1,j)+F(1,j*j)-F(1,j**3)
        uniform_cost = (1+(j-1)*F(1,j*j))/j
        check("checkpoint_penalty", uniform_cost == expected, "uniform primal/dual exact witness")
        check("checkpoint_penalty", expected/F(1,j*j) == j+1-F(1,j), "exact large-J ratio")
    for seed in range(12):
        r, j = 2+seed%3, 2+(seed//3)%3
        a = [[F(1+((i+1)*(k+2)+seed*(i+k+3))%17, 19)
              for k in range(j)] for i in range(r)]
        value, rho, lam = game(a)
        check("exact_games", min(min(row) for row in a) <= value <= max(max(row) for row in a),
              "range")

    # A three-level branching/recombining network with four paths.
    paths = [("a","c","e"), ("a","d","e"), ("b","c","e"), ("b","d","e")]
    weights = {"a":F(1), "b":F(1,4), "c":F(1,9), "d":F(4,9), "e":F(1,3)}
    matrix = [[weights[w] for w in path] for path in paths]
    value, rho, lam = game(matrix)
    occupations = {w:sum(p for p,path in zip(rho, paths) if w in path) for w in weights}
    for level in (("a","b"),("c","d"),("e",)):
        check("network_flows", sum(occupations[w] for w in level) == 1, "level flow conservation")
    check("network_flows", value == F(1,3), "matching forced-last-level lower bound")
    check("network_flows", min(sum(lam[j]*weights[w] for j,w in enumerate(path)) for path in paths) == value,
          "shortest-path dual")
    # Earlier independent fair observation selects either branch. Future fresh law stays unchanged.
    joint = {(old,new): F(1,4) for old,new in product((0,1), repeat=2)}
    for branch in (0,1):
        prob_branch = sum(p for (old,new),p in joint.items() if old == branch)
        prob_one = sum(p for (old,new),p in joint.items() if old == branch and new == 1)
        check("predictability", prob_one/prob_branch == F(1,2), "fresh conditional law")
    check("predictability", sum(p for (old,new),p in joint.items() if new == 1)/F(1,2) == 1,
          "selecting on the new bit destroys the fresh-law assertion")

    strict = []
    for m, delta in product((1,2,7), (F(1,2),F(1,4),F(1,10))):
        ell = F(1,constant*m*m)
        pre = delta**2*ell  # forced first node; split second level equally, phi(1/2)=0
        pred = ell         # second-level linear cost is ell at every occupation split
        check("strict_predictable_witness", pred/pre == 1/delta**2 > 1, "strict late refinement")
        strict.append({"M":m, "delta":str(delta), "Gamma_pre":str(pre),
                       "Gamma_pred":str(pred), "ratio":str(pred/pre)})
    # Positive gains only rescale the local task; removing that rescaling removes this design gap.
    normalized, _, _ = game([[F(1)]*3 for _ in range(3)])
    check("loss_normalization", normalized == 1, "same normalized scalar task at all nodes")

    losses = [partition_losses(labels) for labels in product((0,1), repeat=4)]
    minimum_sum = min(sum(x) for x in losses)
    check("nonregenerative_scope_witness", minimum_sum == F(1,16), "two-center square quantization")
    axis1 = partition_losses((0,0,1,1))
    axis2 = partition_losses((0,1,0,1))
    mixture = tuple((x+y)/2 for x,y in zip(axis1,axis2))
    check("nonregenerative_scope_witness", mixture == (F(1,32),F(1,32)), "one common public-seed mixture")
    check("nonregenerative_scope_witness", max(mixture) == minimum_sum/2,
          "matching randomized common-controller optimum")
    check("nonregenerative_scope_witness", axis1[0] == axis2[1] == 0,
          "independent stopped checkpoint encoders each have zero loss")

    low, high = integral_enclosure()
    k_low, k_high = low**3/1536, high**3/1536
    ratio_low, ratio_high = constant*k_low, constant*k_high
    check("coefficient_interval", F(405,100) < ratio_low < ratio_high < F(406,100),
          "published open interval (4.05,4.06)")
    return {
        "schema":"A1-v30-independent-finite-checks-1",
        "submission":"dc8c1bd475b870cd222627c0cfd6d784363e1728",
        "script_sha256":hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "status":"passed",
        "arithmetic":"exact Fraction/integer arithmetic; float fields are display-only",
        "total_checks":sum(COUNTS.values()),
        "checks_by_category":dict(sorted(COUNTS.items())),
        "finite_J_game_witnesses":games,
        "regenerative_branching_network":{"paths":paths,"value":str(value),
            "occupations":{k:str(v) for k,v in occupations.items()},"dual":list(map(str,lam))},
        "strict_predictable_witnesses":strict,
        "nonregenerative_scope_witness":{"partition_assignments_enumerated":len(losses),
            "minimum_sum_risk":str(minimum_sum),"common_controller_minimax":str(max(mixture)),
            "separate_checkpoint_optima":["0","0"],
            "qualification":"Not a counterexample to v30: no fresh block at stage two; no score feedback."},
        "density_enclosure":{"intervals_per_side":8192,"root_scale":10**12,
            "integral_lower":str(low),"integral_upper":str(high),
            "kappa_lower":str(k_low),"kappa_upper":str(k_high),
            "ratio_lower":str(ratio_low),"ratio_upper":str(ratio_high),
            "display_ratio_lower":float(ratio_low),"display_ratio_upper":float(ratio_high)},
        "verification_limits":["Finite checks do not prove continuum or uniform theorems.",
            "No author script, native two-volume TeX build, or PDF visual audit was executed.",
            "The large check count is dominated by scalar endpoint arithmetic, not theorem coverage."]}

if __name__ == "__main__":
    print(json.dumps(run(), indent=2, sort_keys=True))
