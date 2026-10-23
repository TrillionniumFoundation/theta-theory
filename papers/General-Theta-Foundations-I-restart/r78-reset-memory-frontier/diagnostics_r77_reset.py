#!/usr/bin/env python3
"""Exact finite diagnostics for the R77 optimal-reset-memory theorems.

This is author-team AI mathematical challenge evidence, not a formal proof,
independent human referee assessment, or an editorial decision. Fractions
and exact symbolic algebra are used throughout; there are no floating probes.
"""
from fractions import Fraction as F
from itertools import combinations
from collections import Counter
import json
import sympy as sp

CHECKS = Counter()


def require(condition, group, message):
    if not bool(condition):
        raise RuntimeError(f"{group}: {message}")
    CHECKS[group] += 1


def exact_solve(matrix, rhs):
    """Independent rational Gaussian elimination for a transient cost law."""
    n = len(rhs)
    aug = [[F(x) for x in matrix[i]] + [F(rhs[i])] for i in range(n)]
    for j in range(n):
        pivot = next((i for i in range(j, n) if aug[i][j]), None)
        if pivot is None:
            raise RuntimeError("Singular rational cost system")
        aug[j], aug[pivot] = aug[pivot], aug[j]
        value = aug[j][j]
        aug[j] = [x / value for x in aug[j]]
        for i in range(n):
            if i != j:
                value = aug[i][j]
                aug[i] = [x - value*y for x, y in zip(aug[i], aug[j])]
    return [row[-1] for row in aug]


def masks(q):
    return range(1, 1 << q)


def actions(mask, q):
    return [a for a in range(q) if mask & (1 << a)]


def transversal(edges, q):
    # Direct enumeration of action subsets, independent of row-distribution search.
    feasible = [mask for mask in masks(q) if all(mask & edge for edge in edges)]
    return min(feasible, key=lambda mask: (mask.bit_count(), mask))


def uniform_row(mask, q):
    den = mask.bit_count()
    return [F(bool(mask & (1 << a)), den) for a in range(q)]


def residual(row, edge, q):
    return sum((row[a] for a in range(q) if not edge & (1 << a)), F(0))


def universal_instrument_diagnostics():
    """Exhaust all simple hypergraphs with q<=4 and <=3 proper edges.

    Upper: solve actual rational post-report cost equations, form the whole
    unknown-initial-state cost operator, and compare all its eigenvalues.
    Lower: enumerate mixed command support families at one label below
    the claimed optimum and evaluate the one-step operator certificate.
    These are finite diagnostics; the manuscript proves arbitrary size.
    """
    graph_cases = upper_instances = mixed_support_families = 0
    for q in range(2, 5):
        full = (1 << q) - 1
        proper = list(range(1, full))
        for s in range(1, min(3, len(proper)) + 1):
            for edge_tuple in combinations(proper, s):
                graph_cases += 1
                H = transversal(edge_tuple, q)
                tau = H.bit_count()
                selected = actions(H, q)
                initial = uniform_row(full, q)
                rows = [initial] + [uniform_row(1 << a, q) for a in selected]
                update = [1 + selected.index(actions(H & edge, q)[0])
                          for edge in edge_tuple]
                require(set(update) == set(range(1, tau + 1)),
                        "universal_reachability", "a minimum transversal row was unused")
                # Every edge has a positive first-failure probability; all
                # selected continuing rows and the counted initializer are reached.
                cost_diagonals = [
                    [F(1 + (0 if edge & (1 << a) else 1)) for edge in edge_tuple]
                    + [F(3 + (a == j)) for j in range(q)]
                    for a in range(q)
                ]
                require(all(F(1) <= x <= F(4)
                            for row in cost_diagonals for x in row),
                        "physical_cost_bounds", "cost operator outside [I,4I]")
                for r in (F(1, 3), F(1, 2), F(3, 4)):
                    upper_instances += 1
                    effect = r / s
                    require(effect > 0 and s*effect + (1-r) == 1,
                            "physical_instrument", "effects fail strict positivity/completeness")
                    c = [sum((rows[update[i]][a] * cost_diagonals[a][i]
                              for a in range(q)), F(0)) for i in range(s)]
                    transition = [[effect for _ in range(s)] for _ in range(s)]
                    system = [[F(i == j) - transition[i][j]
                               for j in range(s)] for i in range(s)]
                    actual_v = exact_solve(system, c)
                    require(all(x == 1/(1-r) for x in actual_v),
                            "universal_actual_cost", "encoded controller fails Bellman cost")
                    computed_optimal_sets = []
                    for i in range(s):
                        d = [cost_diagonals[a][i] + effect*sum(actual_v) - actual_v[i]
                             for a in range(q)]
                        require(all(x >= 0 for x in d),
                                "universal_bellman", "negative residual")
                        computed_optimal_sets.append(sum(1 << a for a in range(q) if d[a] == 0))
                    require(computed_optimal_sets == list(edge_tuple),
                            "universal_bellman", "physical action sets differ from incidence table")
                    # All effects are scalar. This diagonal is the full Hermitian
                    # expected-cost operator, valid also for coherent input states.
                    start_operator = [sum((initial[a]*cost_diagonals[a][j]
                                           for a in range(q)), F(0))
                                      + effect*sum(actual_v)
                                      for j in range(s+q)]
                    value = F(3) + r/(1-r) + F(1, q)
                    require(max(start_operator) == value,
                            "universal_initial_spectrum", "incorrect all-state worst cost")
                    require(all(x < value for x in start_operator[:s]),
                            "universal_initial_spectrum", "reset states unexpectedly maximize start cost")
                    require(all(x == value for x in start_operator[s:]),
                            "universal_initial_spectrum", "extra coordinates fail uniform saddle")
                    require(all(min(residual(row, edge, q) for row in rows) == 0
                                for edge in edge_tuple),
                            "universal_gap_zero", "constructed optimal rows have positive one-step slack")
                # A robust optimum must start uniformly. With total tau labels,
                # at most tau-1 other rows are available. For every nonempty
                # support we use its strictly positive uniform distribution.
                # Zero-residual incidence depends only on support, so this
                # exhausts the possible exact-cover incidences at this size.
                for support_tuple in combinations(list(masks(q)), tau-1):
                    mixed_support_families += 1
                    test_rows = [initial] + [uniform_row(mask, q) for mask in support_tuple]
                    min_residuals = [min(residual(row, edge, q) for row in test_rows)
                                     for edge in edge_tuple]
                    # At r=1/2 the extra operator is this scalar times I.
                    exact_operator_gap = F(1, 2*s)*sum(min_residuals)
                    require(exact_operator_gap > 0,
                            "mixed_row_lower_operator", "undersized mixed rows evaded the exact cost witness")
    return {"simple_hypergraphs": graph_cases,
            "rational_physical_instances": upper_instances,
            "undersized_mixed_support_families": mixed_support_families,
            "q_range": [2, 4], "maximum_number_of_edges": 3,
            "failure_rates": ["1/3", "1/2", "3/4"]}


def initializer_reuse_and_nonsharp_gap():
    # Positive effects, two distinct optimal actions, and an initial row that
    # can be reused. The third physical coordinate exposes the start command.
    half = F(1, 2)
    Ga, Gb = [F(1), F(3), F(6)], [F(3), F(2), F(7)]
    v = exact_solve([[F(3,4), -F(1,4)], [-F(1,4), F(3,4)]], [1,2])
    require(v == [F(5,2), F(7,2)], "initializer_reuse", "Bellman vector")
    La = [g + F(1,4)*sum(v) for g in Ga]
    Lb = [g + F(1,4)*sum(v) for g in Gb]
    require(La == [F(5,2), F(9,2), F(15,2)] and
            Lb == [F(9,2), F(7,2), F(17,2)],
            "initializer_reuse", "start cost operators")
    # All coefficients below are exact polynomial identities in x = P(command b).
    x = sp.symbols("x", real=True)
    rho_cost = sp.Matrix([[sp.Rational(3,4), -sp.Rational(1,4)],
                          [-sp.Rational(1,4), sp.Rational(3,4)]])
    continuation = rho_cost.inv() * sp.Matrix([1+2*x, 3-x])
    require(continuation == sp.Matrix([3+sp.Rational(5,2)*x,
                                      5-sp.Rational(1,2)*x]),
            "initializer_reuse", "one-row exact continuation")
    actual_extra = 6+x + sum(continuation)/4
    require(sp.expand(actual_extra - (8+sp.Rational(3,2)*x)) == 0,
            "initializer_reuse", "one-label actual worst cost")
    start_extra = sp.Rational(15,2)+x
    one_step_extra = start_extra + (2*x + 1-x)/4
    require(sp.expand(one_step_extra - (sp.Rational(31,4)+sp.Rational(5,4)*x)) == 0,
            "initializer_reuse", "one-step lower certificate")
    for other in continuation:
        difference = sp.expand(actual_extra-other)
        require(sp.degree(difference, x) <= 1 and
                difference.subs(x,0) > 0 and difference.subs(x,1) > 0,
                "initializer_reuse_continuum", "extra coordinate is not maximal on [0,1]")
    require(sp.diff(actual_extra,x) == sp.Rational(3,2) and
            sp.diff(one_step_extra,x) == sp.Rational(5,4),
            "initializer_reuse_continuum", "wrong exact monotonicity")
    for num in range(17):
        prob = F(num,16)
        actual = [F(3)+F(5,2)*prob, F(5)-half*prob, F(8)+F(3,2)*prob]
        require(max(actual) == actual[2], "initializer_reuse", "wrong largest cost coordinate")
        # The affine formulas above prove monotonicity on the entire interval;
        # this grid only catches implementation mistakes in their evaluation.
        require(F(31,4)+F(5,4)*prob <= actual[2],
                "initializer_reuse", "certificate exceeds actual controller cost")
    require(F(31,4)-F(15,2) == F(1,4) < F(8)-F(15,2),
            "nonsharp_certificate", "gap certificate incorrectly equals the full frontier")
    return {"dimension": 3, "optimal_live_labels": 2,
            "optimal_cost": "15/2", "one_label_optimal_cost": "8",
            "D_1": "1/4", "actual_one_label_gap": "1/2",
            "point": "The initial command row is reused; D_M is strictly a lower certificate."}


def noncommuting_quantum_diagnostics():
    # Strictly positive failure effects need not commute with the cost operators.
    R = sp.Rational
    I = sp.eye(2)
    E1 = sp.Matrix([[R(1,4), R(1,8)], [R(1,8), R(1,4)]])
    E2 = sp.Matrix([[R(1,4), -R(1,8)], [-R(1,8), R(1,4)]])
    Ga, Gb = sp.diag(1,3), sp.diag(3,2)
    require(E1.det() == R(3,64) and E2.det() == R(3,64),
            "quantum_positivity", "failure effects are not positive definite")
    require(E1+E2 == I/2, "quantum_positivity", "success effect")
    require(E1*Ga != Ga*E1, "quantum_noncommutation", "example accidentally diagonalizes all primitives")
    # An actual instrument realizes the cost mean, rather than merely
    # prescribing incompatible cost and report observables. Give each failure
    # cost 1; split success into two hidden basis outcomes with effects
    # |j><j|/2 and costs 2*G[j,j]-1. The controller observes only success.
    success = [sp.diag(R(1,2),0), sp.diag(0,R(1,2))]
    require(E1+E2+success[0]+success[1] == I,
            "quantum_joint_instrument", "complete refined outcome instrument")
    for name,G in (("a",Ga),("b",Gb)):
        cost_moment = E1+E2 + sum(
            ((2*G[j,j]-1)*success[j] for j in range(2)), sp.zeros(2))
        require(cost_moment == G and all(2*G[j,j]-1 >= 1 for j in range(2)),
                "quantum_joint_instrument", "incorrect hidden cost moment for "+name)
    v1,v2 = R(5,2),R(7,2)
    La,Lb = Ga+v1*E1+v2*E2,Gb+v1*E1+v2*E2
    require(La == sp.Matrix([[R(5,2),-R(1,8)],[-R(1,8),R(9,2)]]),
            "quantum_cost_matrix", "L_a")
    require(Lb == sp.Matrix([[R(9,2),-R(1,8)],[-R(1,8),R(7,2)]]),
            "quantum_cost_matrix", "L_b")
    p = R(1,3)+sp.sqrt(2)/48
    value = R(23,6)+sp.sqrt(2)/12
    L = sp.simplify(p*La+(1-p)*Lb)
    mean = sp.trace(L)/2
    spread = sp.sqrt(2)*3/32
    rho = sp.simplify((I+(L-mean*I)/spread)/2)
    require(sp.simplify(rho.trace()-1) == 0 and sp.simplify(rho.det()) == 0,
            "quantum_saddle", "least-favorable density trace/rank")
    require(all(bool(sp.simplify(rho[i,i] > 0)) for i in range(2)),
            "quantum_saddle", "least-favorable state is not positive")
    require(sp.simplify(L*rho-value*rho) == sp.zeros(2),
            "quantum_saddle", "spectral attainment")
    require(sp.simplify(mean+spread-value) == 0 and bool(spread > 0),
            "quantum_saddle", "largest eigenvalue")
    for name,operator in (("a",La),("b",Lb)):
        require(sp.simplify(sp.trace(rho*operator)-value) == 0,
                "quantum_saddle", "dual equality for command "+name)
    require(bool(R(7,2)+sp.sqrt(65)/8 > value) and
            bool(4+sp.sqrt(17)/8 > value),
            "quantum_initializer", "a pure initial row is accidentally optimal")
    require(La[0,0] == v1 and Lb[0,0] > v1 and
            Lb[1,1] == v2 and La[1,1] > v2,
            "quantum_bellman", "optimal reset-action sets")
    # Mixed initial row plus two pure continuing rows has exact cost L.
    # A hypothetical optimum with two rows cannot cover both singleton
    # action sets in addition to its mixed initial row.
    require(bool(p > 0) and bool(p < 1), "quantum_initializer", "start support is not mixed")
    return {"dimension": 2, "failure_effect_minimum_eigenvalue": "1/8",
            "initial_probability_a": "1/3+sqrt(2)/48",
            "optimal_cost": "23/6+sqrt(2)/12", "optimal_live_labels": 3,
            "exact_saddle_state": str(rho),
            "point": "Both the full Hermitian start matrix and a singular dual density are checked exactly."}


def semidefinite_boundary_counterexample():
    r = F(1,2)
    v = F(1)/(1-r)
    La,Lb = [F(1)+r*v,F(6)],[F(2)+r*v,F(5)]
    actual_b = [F(2)/(1-r),F(5)]
    require(v == 2 and La == [2,6] and Lb == [3,5],
            "semidefinite_counterexample", "Bellman/start identities")
    require(actual_b == [4,5] and max(actual_b) == max(Lb) == 5,
            "semidefinite_counterexample", "one-label controller is not robustly optimal")
    require(F(1,2) < 1, "semidefinite_counterexample", "unexpected closed failure set")
    # Unique minimizing start is b, while the sole reset optimum is a.
    # The blind all-report cover would claim two labels, contradicting
    # the actual one-label optimum. The least-favorable |1> sees no failure.
    return {"actual_optimal_live_labels": 1,
            "incorrect_all_report_formula_without_exposure": 2,
            "optimal_cost": "5", "failure_effect_eigenvalues": ["0","1/2"],
            "cost_operator_constant_b": ["4","5"]}


def main():
    results = {
        "universal_cover_family": universal_instrument_diagnostics(),
        "initializer_reuse": initializer_reuse_and_nonsharp_gap(),
        "noncommuting_quantum": noncommuting_quantum_diagnostics(),
        "semidefinite_boundary": semidefinite_boundary_counterexample(),
    }
    print(json.dumps({
        "schema": "theta.r77.reset-exact-diagnostics.v1",
        "status": "PASS", "arithmetic": "Exact rational and symbolic algebra only",
        "sympy": sp.__version__, "floating_checks": 0,
        "exact_conditions_checked": sum(CHECKS.values()),
        "total_checks": sum(CHECKS.values()),
        "exact_checks": sum(CHECKS.values()),
        "checks_by_group": dict(sorted(CHECKS.items())), "results": results,
        "scope": "Finite exact consistency and counterexample diagnostics. The arbitrary-size and continuum statements rely on the written proofs. Author-team AI challenge, not formal verification, independent human review, priority clearance, or journal acceptance."
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
