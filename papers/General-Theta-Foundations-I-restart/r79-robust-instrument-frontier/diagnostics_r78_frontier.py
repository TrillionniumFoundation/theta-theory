#!/usr/bin/env python3
"""Independent finite exact challenge of reset-palette normalization.

The general controller is evaluated on its reachable product chain; the
normal form is evaluated independently by finite SSP selector enumeration.
No optimization solver or floating-point arithmetic is used. This tests
finite instances, not the quantified theorems or external priority.
"""
from collections import Counter
from fractions import Fraction as F
from itertools import combinations, product
import json
import random

CHECKS = Counter()


def require(ok, group, message):
    if not ok:
        raise RuntimeError(f"{group}: {message}")
    CHECKS[group] += 1


def solve(A, b):
    n = len(b)
    B = [[F(x) for x in A[i]] + [F(b[i])] for i in range(n)]
    for j in range(n):
        k = next((i for i in range(j, n) if B[i][j]), None)
        if k is None:
            return None
        B[j], B[k] = B[k], B[j]
        z = B[j][j]
        B[j] = [x / z for x in B[j]]
        for i in range(n):
            if i != j:
                z = B[i][j]
                B[i] = [x - z * y for x, y in zip(B[i], B[j])]
    return [row[-1] for row in B]


def compositions(total, parts):
    if parts == 1:
        yield (total,)
    else:
        for first in range(total + 1):
            for rest in compositions(total - first, parts - 1):
                yield (first,) + rest


def simplex(q, den):
    return [tuple(F(x, den) for x in row) for row in compositions(den, q)]


def random_row(rng, n):
    row = [rng.randrange(5) for _ in range(n)]
    if not any(row):
        row[rng.randrange(n)] = 1
    return tuple(F(x, sum(row)) for x in row)


def palette_optimum(Q, c, rows):
    """Q[i][a][j], c[i][a]; independently enumerate all proper selectors."""
    s, m = len(Q), len(rows)
    q = len(rows[0])
    candidates = []
    for selector in product(range(m), repeat=s):
        T = [[sum(rows[selector[i]][a] * Q[i][a][j] for a in range(q))
              for j in range(s)] for i in range(s)]
        g = [sum(rows[selector[i]][a] * c[i][a] for a in range(q))
             for i in range(s)]
        x = solve([[F(i == j) - T[i][j] for j in range(s)]
                   for i in range(s)], g)
        if x is not None and all(v >= 0 for v in x):
            candidates.append((x, selector))
    if not candidates:
        return None
    minimum = [min(x[i] for x, _ in candidates) for i in range(s)]
    common = next(((x, k) for x, k in candidates if x == minimum), None)
    require(common is not None, "palette_bellman", "no simultaneous minimizing selector")
    for i in range(s):
        value = min(sum(rows[k][a] * (c[i][a] + sum(Q[i][a][j] * minimum[j]
                      for j in range(s))) for a in range(q)) for k in range(m))
        require(value == minimum[i], "palette_bellman", "Bellman equality failed")
    return common


def product_values(Q, c, rows, routing, start_exposure):
    """Evaluate arbitrary stochastic command/report/previous-label routing.

    start_exposure[j][k] says that some allowed initial state can produce
    report j followed by label k after the first call. Only reachable
    product pairs need have finite cost; all-start quantification is still
    imposed at the physical level and a prescribed label zero.
    """
    s, m, q = len(Q), len(rows), len(rows[0])
    pairs = list(product(range(s), range(m)))
    T = [[sum(rows[k][a] * Q[i][a][j] * routing[k][a][j][ell]
              for a in range(q)) for j, ell in pairs] for i, k in pairs]
    g = [sum(rows[k][a] * c[i][a] for a in range(q)) for i, k in pairs]
    reached = {i * m + k for i in range(s) for k in range(m)
               if start_exposure[i][k]}
    while True:
        more = reached | {j for i in reached for j in range(s*m) if T[i][j] > 0}
        if more == reached:
            break
        reached = more
    R = sorted(reached)
    A = [[F(i == j) - T[i][j] for j in R] for i in R]
    y = solve(A, [g[i] for i in R])
    if y is None or any(v < 0 for v in y):
        return None
    out = {pairs[i]: y[k] for k, i in enumerate(R)}
    return out, len(R), solve([[F(i == j)-T[i][j] for j in range(s*m)]
                              for i in range(s*m)], g)


def random_diagonal_challenge():
    rng = random.Random(781731)
    count = 0
    strict = 0
    for s, q, m in product((1, 2, 3), (2, 3), (1, 2, 3)):
        d = s + 1
        for rep in range(6):
            # Random commuting positive effects, with zeros and survival <=3/4.
            E = [[[F(0) for _ in range(d)] for _ in range(s)] for _ in range(q)]
            for a in range(q):
                for z in range(d):
                    weights = [rng.randrange(4) for _ in range(s)]
                    den = 4 * max(1, sum(weights))
                    for j in range(s):
                        E[a][j][z] = F(3 * weights[j], den)
            G = [[F(rng.randrange(4, 13), 4) for _ in range(d)] for _ in range(q)]
            Q = [[[E[a][j][i] for j in range(s)] for a in range(q)] for i in range(s)]
            c = [[G[a][i] for a in range(q)] for i in range(s)]
            rows = [random_row(rng, q) for _ in range(m)]
            routing = [[[random_row(rng, m) for j in range(s)]
                        for a in range(q)] for k in range(m)]
            exposure = [[any(sum(rows[0][a]*E[a][j][z]*routing[0][a][j][k]
                               for a in range(q)) > 0 for z in range(d))
                         for k in range(m)] for j in range(s)]
            actual = product_values(Q, c, rows, routing, exposure)
            require(actual is not None, "product_normalization", "uniformly transient product is improper")
            y, _, _ = actual
            result = palette_optimum(Q, c, rows)
            require(result is not None, "product_normalization", "finite palette value missing")
            x, selector = result
            old, new = [], []
            for z in range(d):
                old.append(sum(rows[0][a] * (G[a][z] + sum(E[a][j][z] * sum(
                    routing[0][a][j][k] * y.get((j,k), F(0)) for k in range(m))
                    for j in range(s))) for a in range(q)))
                new.append(sum(rows[0][a] * (G[a][z] + sum(E[a][j][z]*x[j]
                    for j in range(s))) for a in range(q)))
                require(new[-1] <= old[-1], "product_normalization", "not all-state dominating")
            C = max(old)
            for value in x:
                require(value <= C, "potential_cap", "all-initial-state cap failed")
            normalized_routing = [[[tuple(F(k == selector[j]) for k in range(m))
                                    for j in range(s)] for a in range(q)] for _ in range(m)]
            normalized_exposure = [[any(sum(rows[0][a]*E[a][j][z]*normalized_routing[0][a][j][k]
                                for a in range(q)) > 0 for z in range(d))
                                for k in range(m)] for j in range(s)]
            normalized = product_values(Q,c,rows,normalized_routing,normalized_exposure)
            require(normalized is not None,"product_normalization","normalized policy improper")
            for (i,k), value in normalized[0].items():
                require(k == selector[i] and value == x[i], "product_normalization",
                        "routed product evaluation disagrees with SSP")
            strict += int(any(a < b for a,b in zip(new,old)))
            count += 1
    return {"instances": count, "strict_improvements": strict,
            "physical_dimensions": [2,3,4], "memory_sizes": [1,2,3],
            "arithmetic": "rational", "seed": 781731}


def unreachable_improper_pair():
    # Command a always succeeds; b traps in reset 1; label 1 uses a,
    # label 2 uses b but is unreachable from the prescribed initial label.
    Q = [[[F(0),F(0)],[F(0),F(1)]],
         [[F(0),F(0)],[F(0),F(1)]]]
    c = [[F(1),F(1)],[F(1),F(1)]]
    rows = [(F(1),F(0)),(F(0),F(1))]
    routing = [[[tuple(F(ell==k) for ell in range(2)) for j in range(2)]
                for a in range(2)] for k in range(2)]
    result = product_values(Q,c,rows,routing,[[False,False],[False,False]])
    require(result is not None and result[1] == 0, "unreachable_pairs", "empty reached set mishandled")
    require(result[2] is None, "unreachable_pairs", "full product unexpectedly transient")
    normal = palette_optimum(Q,c,rows)
    require(normal is not None and normal[0] == [1,1], "unreachable_pairs", "palette replacement failed")
    return {"initial_cost": "1", "whole_product_system": "singular",
            "reachable_nonterminal_pairs": 0,
            "point": "An unused improper pair does not invalidate an all-state pure-start controller."}


def nonexposed_optimality():
    # R77's PSD boundary example, evaluated without its positive-exposure formula.
    Q = [[[F(1,2)],[F(1,2)]]]
    c = [[F(1),F(2)]]
    one = palette_optimum(Q,c,[(F(0),F(1))])
    two = palette_optimum(Q,c,[(F(0),F(1)),(F(1),F(0))])
    require(one[0] == [4] and two[0] == [2], "nonexposed_optimality", "wrong palette values")
    K1, K2 = [F(2)+one[0][0]/2,F(5)], [F(2)+two[0][0]/2,F(5)]
    require(K1 == [4,5] and K2 == [3,5] and max(K1) == max(K2),
            "nonexposed_optimality", "unexposed continuation should not raise robust optimum")
    return {"one_label_operator": [str(x) for x in K1],
            "two_label_operator": [str(x) for x in K2], "robust_value": "5"}


def fixed_prior_cap_boundary():
    # A single initial state |0> succeeds under a, while sigma=|1> is dark
    # under a. Command b succeeds everywhere, so the primitive has a proper
    # all-state policy, but the one-row palette {a} does not.
    Q = [[[F(1)],[F(0)]]]
    c = [[F(1),F(1)]]
    require(palette_optimum(Q,c,[(F(1),F(0))]) is None,
            "fixed_prior_boundary","dark palette falsely given a finite full-state potential")
    require(palette_optimum(Q,c,[(F(0),F(1))])[0] == [1],
            "fixed_prior_boundary","primitive should admit all-state properness")
    return {"restricted_initial_cost_of_a":"1", "cost_of_a_from_reset_state":"infinite",
            "point":"The full finite-potential cap uses the all-initial-state quantifier; it does not follow from one prior."}


def noncommuting_quantum_challenge():
    # Two nonorthogonal pure reset states |0> and |+>, with noncommuting
    # rational effect and cost operators. All matrix comparisons are exact.
    E = [[[[F(2,8),F(1,8)],[F(1,8),F(2,8)]],
          [[F(1,8),F(0)],[F(0),F(2,8)]]],
         [[[F(2,8),F(-1,8)],[F(-1,8),F(2,8)]],
          [[F(2,8),F(0)],[F(0),F(1,8)]]]]
    G = [[[F(2),F(1,4)],[F(1,4),F(3)]],
         [[F(3),F(-1,3)],[F(-1,3),F(2)]]]
    def mean(A,i):
        return A[0][0] if i == 0 else sum(sum(row) for row in A)/2
    def psd(A):
        return A[0][0]>=0 and A[1][1]>=0 and A[0][0]*A[1][1]>=A[0][1]*A[1][0]
    Q = [[[mean(E[a][j],i) for j in range(2)] for a in range(2)] for i in range(2)]
    c = [[mean(G[a],i) for a in range(2)] for i in range(2)]
    for a in range(2):
        for j in range(2):
            require(psd(E[a][j]),"quantum_palette","nonpositive failure effect")
        success = [[F(i==j)-sum(E[a][k][i][j] for k in range(2))
                    for j in range(2)] for i in range(2)]
        require(psd(success),"quantum_palette","nonpositive success effect")
    commutator = [[sum(E[0][0][i][k]*E[0][1][k][j]-E[0][1][i][k]*E[0][0][k][j]
                      for k in range(2)) for j in range(2)] for i in range(2)]
    require(any(v for row in commutator for v in row),"quantum_palette","effects accidentally commute")
    rng = random.Random(781732)
    cases = strict = 0
    for m in (1,2,3):
        for rep in range(12):
            rows = [random_row(rng,2) for _ in range(m)]
            routing = [[[random_row(rng,m) for j in range(2)] for a in range(2)] for k in range(m)]
            exposure = [[sum(rows[0][a]*routing[0][a][j][k] for a in range(2))>0
                         for k in range(m)] for j in range(2)]
            actual = product_values(Q,c,rows,routing,exposure)
            require(actual is not None,"quantum_palette","positive-success product improper")
            y = actual[0]
            x,_ = palette_optimum(Q,c,rows)
            K = [[sum(rows[0][a]*(G[a][i][ell]+sum(E[a][j][i][ell]*sum(
                    routing[0][a][j][k]*y.get((j,k),F(0)) for k in range(m))
                    for j in range(2))) for a in range(2)) for ell in range(2)] for i in range(2)]
            N = [[sum(rows[0][a]*(G[a][i][ell]+sum(E[a][j][i][ell]*x[j]
                    for j in range(2))) for a in range(2)) for ell in range(2)] for i in range(2)]
            difference = [[K[i][j]-N[i][j] for j in range(2)] for i in range(2)]
            require(psd(difference),"quantum_palette","operator dominance failed")
            for i in range(2):
                require(x[i] <= mean(K,i),"quantum_palette","reset-state cap failed")
            strict += int(sum(difference[i][i] for i in range(2))>0)
            cases += 1
    return {"instances":cases,"strict_operator_improvements":strict,
            "physical_dimension":2,"reset_states":"|0><0| and |+><+|",
            "certificate":"nonnegative diagonal and determinant of exact 2x2 Hermitian difference",
            "seed":781732}


def cover_formula(edges,q,m,r):
    s = len(edges)
    lam = r / (s * (1-r))
    best = None
    best_data = None
    for hsize in range(min(q,m-1)+1):
        for H in combinations(range(q),hsize):
            uncovered = [edge for edge in edges if not any(edge & (1<<a) for a in H)]
            b = [sum(not edge & (1<<a) for edge in uncovered) for a in range(q)]
            order = sorted(range(q),key=lambda a:(b[a],a))
            for k in range(1,q+1):
                p = tuple(F(a in order[:k],k) for a in range(q))
                z = F(3)+r/(1-r)+(F(1)+lam*sum(b[a] for a in order[:k]))/k
                if best is None or z < best:
                    best,best_data = z,(H,p)
    return best,best_data


def cover_grid_challenge():
    cases = palette_cases = 0
    for q in (2,3):
        proper = list(range(1,(1<<q)-1))
        grid = simplex(q,6)
        for s in range(1,min(3,len(proper))+1):
            for edges in combinations(proper,s):
                for r in (F(1,4),F(1,2),F(3,4)):
                    for m in (1,2):
                        formula,(H,p) = cover_formula(edges,q,m,r)
                        # Exhaust finite rational palettes including mixed continuing rows.
                        got = None
                        for rows in product(grid,repeat=m):
                            h = [min(sum(row[a] for a in range(q) if not edge & (1<<a))
                                     for row in rows) for edge in edges]
                            x = [1+hi+r*(1+sum(h)/s)/(1-r) for hi in h]
                            fvals = [3+rows[0][a]+r*sum(x)/s for a in range(q)]
                            evals = [1+sum(rows[0][a] for a in range(q) if not edge & (1<<a))
                                     +r*sum(x)/s for edge in edges]
                            value = max(fvals+evals)
                            require(value >= formula,"cover_grid","grid palette beats exact formula")
                            got = value if got is None else min(got,value)
                            palette_cases += 1
                        require(got == formula,"cover_grid","grid omitted a claimed attaining uniform subset")
                        cases += 1
    return {"hypergraph_resource_instances": cases, "rational_palettes": palette_cases,
            "simplex_denominator": 6, "actions": [2,3], "memory_sizes": [1,2],
            "failure_probabilities": ["1/4","1/2","3/4"]}


def singleton_staircase():
    cases = 0
    for n in range(2,9):
        edges = [1<<a for a in range(n)]
        prev = None
        for m in range(1,n+3):
            value,_ = cover_formula(edges,n,m,F(1,2))
            u = max(n-m+1,0)
            predicted = F(4)+F(1,n)+F(u*(n-1),n*n)
            require(value == predicted,"singleton_staircase","closed staircase mismatch")
            if prev is not None:
                require(value < prev if m <= n+1 else value == prev,
                        "singleton_staircase","strict/saturated boundary mismatch")
            # Independent R77 first-residual certificate for this family.
            D = F(u*(n-1),2*n*n)
            require(value-(F(4)+F(1,n)) == 2*D,"singleton_staircase","one-step certificate factor mismatch")
            prev = value
            cases += 1
    return {"dimensions": "2n, n=2,...,8", "resource_points": cases,
            "formula": "4+1/n+max(n-M+1,0)*(n-1)/n^2",
            "strict_range": "M=1,...,n+1; n>=2"}


def main():
    results = {"stochastic_product_comparison": random_diagonal_challenge(),
               "unreachable_improper_pair": unreachable_improper_pair(),
               "nonexposed_optimality": nonexposed_optimality(),
               "fixed_prior_cap_boundary": fixed_prior_cap_boundary(),
               "noncommuting_quantum": noncommuting_quantum_challenge(),
               "cover_frontier": cover_grid_challenge(),
               "singleton_staircase": singleton_staircase()}
    print(json.dumps({"schema":"theta.r78.palette-independent-diagnostics.v1",
                      "status":"PASS", "arithmetic":"Exact rational arithmetic only",
                      "floating_checks":0,"exact_checks":sum(CHECKS.values()),
                      "total_checks":sum(CHECKS.values()),
                      "exact_conditions_checked":sum(CHECKS.values()),
                      "checks_by_group":dict(sorted(CHECKS.items())),"results":results,
                      "scope":"Finite independent mathematical diagnostics; no quantified theorem proof, external expert review, full priority clearance, or editorial assessment is claimed."},
                     indent=2,sort_keys=True))


if __name__ == "__main__":
    main()
