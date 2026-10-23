#!/usr/bin/env python3
"""Finite exact checks of robust memory examples and restart certificates.

These independent calculations do not prove the quantified manuscript
statements. No optimizer, floating-point number, or disabled assert is used.
"""
from collections import Counter
from fractions import Fraction as F
from itertools import product
import json

CHECKS = Counter()


def require(condition, group, message):
    if not condition:
        raise RuntimeError(f"{group}: {message}")
    CHECKS[group] += 1


def solve(matrix, vector):
    n = len(vector)
    rows = [[F(x) for x in matrix[i]] + [F(vector[i])] for i in range(n)]
    for col in range(n):
        pivot = next((i for i in range(col, n) if rows[i][col]), None)
        if pivot is None:
            return None
        rows[col], rows[pivot] = rows[pivot], rows[col]
        scale = rows[col][col]
        rows[col] = [v / scale for v in rows[col]]
        for i in range(n):
            if i != col:
                scale = rows[i][col]
                rows[i] = [x - scale * y for x, y in zip(rows[i], rows[col])]
    return [r[-1] for r in rows]


def reachable_cost(transition, costs, start=0):
    reached = {start}
    while True:
        more = reached | {j for i in reached for j, p in enumerate(transition[i]) if p > 0}
        if more == reached:
            break
        reached = more
    indexes = sorted(reached)
    matrix = [[F(i == j) - transition[i][j] for j in indexes] for i in indexes]
    values = solve(matrix, [costs[i] for i in indexes])
    if values is None or any(v < 0 for v in values):
        return None
    return values[indexes.index(start)]


def transition_for_model(rows, updates, success):
    # updates[k][a] is the distribution of the next label after failure.
    return [[sum(rows[k][a] * (1 - success[a]) * updates[k][a][j]
                 for a in range(2)) for j in range(len(rows))]
            for k in range(len(rows))]


def phi_multiply(x, y):
    # a+b*phi with phi^2=phi+1; formal arithmetic in Q[sqrt(5)].
    a, b = x
    c, d = y
    return a*c+b*d, a*d+b*c+b*d


def exact_golden_ratio_identity():
    group = "exact_golden_ratio_identity"
    phi, r, one = (F(0), F(1)), (F(-1), F(1)), (F(1), F(0))
    require(phi_multiply(r, phi) == one, group, "r*phi is not one")
    require((one[0]+r[0], one[1]+r[1]) == phi, group, "1+r is not phi")
    require(phi_multiply(phi, phi) == (F(1), F(1)), group, "phi polynomial failed")
    # Model 0 reachable value equation: W1=1+(1-r)W1, W2=0 on P2=0.
    one_minus_r = (F(2), F(-1))
    continuation = phi_multiply(one_minus_r, phi)
    require((one[0]+continuation[0], continuation[1]) == phi,
            group, "model-0 supported Bellman equality failed")
    # Model 1: W2=1 and W1=1+r*W2.
    require((F(1)+r[0], r[1]) == phi,
            group, "model-1 Bellman equality failed")
    return {"V1": "2", "V2": "(1+sqrt(5))/2", "V_M_ge_3": "3/2",
            "optimal_initial_a_probability": "(sqrt(5)-1)/2",
            "model_0_reachable_support": [1, 0],
            "model_1_reachable_support": [1, 1]}


def rational_controller_challenge():
    group = "exact_two_label_rational_controllers"
    grid = [F(i, 4) for i in range(5)]
    update_grid = [F(0), F(1, 2), F(1)]
    cases = finite = 0
    minimum = None
    for r, s in product(grid, repeat=2):
        rows = [(r, 1-r), (s, 1-s)]
        for u00, u01, u10, u11 in product(update_grid, repeat=4):
            updates = [[(u00, 1-u00), (u01, 1-u01)],
                       [(u10, 1-u10), (u11, 1-u11)]]
            t0 = transition_for_model(rows, updates, (F(1), F(0)))
            t1 = transition_for_model(rows, updates, (F(0), F(1)))
            c0 = reachable_cost(t0, [F(1), F(1)])
            c1 = reachable_cost(t1, [F(1), F(1)])
            cases += 1
            require(all(sum(row) <= 1 and all(x >= 0 for x in row)
                        for row in t0+t1), group, "invalid failure matrix")
            if c0 is None or c1 is None:
                continue
            finite += 1
            upper_h0, upper_h1 = max(r, s), 1-min(r, s)
            require(upper_h0 > 0 and upper_h1 > 0, group, "finite zero-success controller")
            lower0 = 1+(1-r)/upper_h0
            lower1 = 1+r/upper_h1
            require(c0 >= lower0 and c1 >= lower1, group, "conditional-hazard lower bound failed")
            value = max(c0, c1)
            # A rational v>=1 lies above phi iff v^2-v-1>=0.
            require(value >= 1 and value*value-value-1 >= 0,
                    group, "a rational controller beats phi")
            minimum = value if minimum is None else min(minimum, value)
    require(cases == 2025, group, "unexpected grid size")
    return {"controllers": cases, "finite_robust_controllers": finite,
            "minimum_on_finite_rational_grid": str(minimum),
            "grid_is_not_a_universal_optimality_proof": True}


def pure_start_and_dark_label():
    group = "exact_initialization_and_dark_label"
    # Three labels: mixed initializer, pure a, pure b.
    rows = [(F(1, 2), F(1, 2)), (F(1), F(0)), (F(0), F(1))]
    updates = [[(F(0), F(0), F(1)), (F(0), F(1), F(0))] for _ in rows]
    for success in [(F(1), F(0)), (F(0), F(1))]:
        value = reachable_cost(transition_for_model(rows, updates, success), [F(1)]*3)
        require(value == F(3, 2), group, "three-label value failed")
    # With an uncounted initial mixture, two pure rows have averaged cost 3/2.
    switch = [[F(0), F(0)], [F(1), F(0)]]
    costs = [reachable_cost(switch, [F(1), F(1)], k) for k in range(2)]
    require((costs[0]+costs[1])/2 == F(3, 2), group, "free initializer convention failed")
    # Full-space inverse fails despite finite pure-start cost.
    dark = [[F(1, 2), F(0)], [F(0), F(1)]]
    require(solve([[1-dark[i][j] if i == j else -dark[i][j]
                    for j in range(2)] for i in range(2)], [F(1), F(1)]) is None,
            group, "dark full-space system unexpectedly invertible")
    require(reachable_cost(dark, [F(1), F(1)]) == 2,
            group, "reachable cost discarded with dark label")
    return {"three_counted_label_cost": "3/2",
            "uncounted_random_initialization_two_label_cost": "3/2",
            "full_space_dark_system": "singular",
            "pure_start_reachable_cost": "2"}


def same_palette_counterexample():
    group = "exact_fixed_hidden_model_palette_boundary"
    rows = [(F(1), F(0)), (F(0), F(1))]
    toggle = [[(F(0), F(1))]*2, [(F(1), F(0))]*2]
    models = [(F(1, 2), F(1, 10)), (F(1, 10), F(1, 2))]
    values = [reachable_cost(transition_for_model(rows, toggle, s), [F(1), F(1)])
              for s in models]
    require(values == [F(30, 11), F(38, 11)], group, "toggle costs failed")
    report_only = []
    for chosen in range(2):
        distribution = tuple(F(j == chosen) for j in range(2))
        update = [[distribution]*2 for _ in range(2)]
        costs = [reachable_cost(transition_for_model(rows, update, s), [F(1), F(1)])
                 for s in models]
        report_only.append(max(costs))
    require(report_only == [F(10), F(6)], group, "report-only costs failed")
    require(max(values) < min(report_only), group, "counterexample does not separate")
    return {"toggle_model_costs": [str(x) for x in values],
            "same_palette_report_only_robust_costs": [str(x) for x in report_only],
            "scope": "Known-instrument reset normal form cannot be extended to a hidden fixed model."}


def restart_and_perturbation():
    group = "exact_restart_and_perturbation"
    rows = [(F(1, 2), F(1, 2)), (F(0), F(1))]
    original = [[(F(0), F(1)), (F(1), F(0))],
                [(F(0), F(1)), (F(0), F(1))]]
    source_models = [(F(1), F(0)), (F(0), F(1))]
    count = 0
    for epsilon in [F(1, 10), F(1, 5), F(1, 4)]:
        update = [[tuple((1-epsilon)*q[j]+epsilon*F(j == 0) for j in range(2))
                   for q in row] for row in original]
        b = F(2)
        initial_bound = b/(1-epsilon*b)
        full_bound = 1/epsilon+initial_bound
        for source in source_models:
            ts = transition_for_model(rows, update, source)
            w = solve([[F(i == j)-ts[i][j] for j in range(2)] for i in range(2)], [F(1)]*2)
            require(w is not None and all(v >= 0 for v in w), group, "restart failed full-space properness")
            require(w[0] <= initial_bound and max(w) <= full_bound,
                    group, "restart cost bound failed")
            for eta in [F(1, 100), F(1, 50)]:
                target = tuple(eta if s == 0 else 1-eta for s in source)
                tt = transition_for_model(rows, update, target)
                for zeta in [F(0), F(1, 100)]:
                    delta = zeta+eta*full_bound
                    require(delta < 1, group, "inadmissible perturbation radius")
                    alpha = 1/(1-delta)
                    scaled = [alpha*v for v in w]
                    require(all(scaled[i] >= 1+zeta+sum(tt[i][j]*scaled[j] for j in range(2))
                                for i in range(2)), group, "scaled source supersolution failed")
                    cost = reachable_cost(tt, [1+zeta]*2)
                    require(cost is not None and cost <= alpha*initial_bound,
                            group, "target initial value bound failed")
                    count += 1
    return {"source_target_cost_cases": count,
            "source_uniform_initial_cap": "2", "source_cost_floor": "1",
            "epsilon_values": ["1/10", "1/5", "1/4"],
            "instrument_TV_radii": ["1/100", "1/50"],
            "cost_operator_errors": ["0", "1/100"]}


def main():
    results = {"golden_ratio": exact_golden_ratio_identity(),
               "rational_controller_grid": rational_controller_challenge(),
               "initialization_and_support": pure_start_and_dark_label(),
               "hidden_model_normal_form_boundary": same_palette_counterexample(),
               "restart_perturbation": restart_and_perturbation()}
    total = sum(CHECKS.values())
    print(json.dumps({"schema": "theta.r79.independent-exact-examples.v1",
                      "status": "PASS", "arithmetic": "Exact rational and quadratic-field arithmetic",
                      "exact_checks": total, "floating_checks": 0, "total_checks": total,
                      "exact_conditions_checked": total,
                      "checks_by_group": dict(sorted(CHECKS.items())), "results": results,
                      "scope": "Finite independent author-team diagnostics. No quantified proof, external human review, priority clearance, or editorial decision is asserted."},
                     indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
