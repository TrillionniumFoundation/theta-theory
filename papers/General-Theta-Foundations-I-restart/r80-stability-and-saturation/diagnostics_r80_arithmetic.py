#!/usr/bin/env python3
"""Independent finite exact diagnostics for the arithmetic memory theorem.

These tests evaluate explicit words and actual controller product chains.
They do not prove nonperiodicity, quantify over every controller, certify
priority, or constitute formal verification or an external referee report.
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
            raise RuntimeError("singular independently constructed controller")
        rows[col], rows[pivot] = rows[pivot], rows[col]
        scale = rows[col][col]
        rows[col] = [x / scale for x in rows[col]]
        for i in range(n):
            if i != col:
                scale = rows[i][col]
                rows[i] = [x-scale*y for x, y in zip(rows[i], rows[col])]
    return [row[-1] for row in rows]


def prefix_cost(word, r, s, ca=None, cb=None, initial_counts=(0, 0)):
    ca = 1-r if ca is None else ca
    cb = 1-s if cb is None else cb
    i, j = initial_counts
    c0 = c1 = F(0)
    for a in word:
        c = ca if a == 0 else cb
        c0 += c*r**i
        c1 += c*s**j
        i += a == 0
        j += a == 1
    return (c0, c1), (r**i, s**j), (i, j)


def greedy(r, s, prior, length, tie=0, ca=None, cb=None, remaining=None):
    ca = 1-r if ca is None else ca
    cb = 1-s if cb is None else cb
    x, y = prior*(1-r)/ca, (1-prior)*(1-s)/cb
    counts = [0, 0]
    word = []
    for _ in range(length):
        if remaining is not None and counts[0] == remaining[0]:
            a = 1
        elif remaining is not None and counts[1] == remaining[1]:
            a = 0
        else:
            a = 0 if x > y else 1 if x < y else tie
        word.append(a)
        counts[a] += 1
        if a == 0:
            x *= r
        else:
            y *= s
    return tuple(word)


def controller_cost(rows, updates, r, s, ca=None, cb=None):
    ca = 1-r if ca is None else ca
    cb = 1-s if cb is None else cb
    n = len(rows)
    g = [p*ca+(1-p)*cb for p in rows]
    out = []
    for fa, fb in [(r, F(1)), (F(1), s)]:
        transition = [[rows[k]*fa*updates[k][0][j] +
                       (1-rows[k])*fb*updates[k][1][j]
                       for j in range(n)] for k in range(n)]
        for q in transition:
            require(all(x >= 0 for x in q) and sum(q) <= 1,
                    "controller_chain_validity", "not substochastic")
        v = solve([[F(i == j)-transition[i][j] for j in range(n)]
                   for i in range(n)], g)
        require(all(x >= 0 for x in v), "controller_chain_validity", "negative cost")
        out.append(v[0])
    return tuple(out)


def deterministic_periodic_cost(prefix, cycle, r, s, ca=None, cb=None):
    word = tuple(prefix)+tuple(cycle)
    n = len(word)
    rows = [F(a == 0) for a in word]
    updates = []
    for i in range(n):
        nxt = i+1 if i+1 < n else len(prefix)
        row = tuple(F(j == nxt) for j in range(n))
        updates.append((row, row))
    actual = controller_cost(rows, updates, r, s, ca, cb)
    pc, ps, _ = prefix_cost(prefix, r, s, ca, cb)
    cc, cs, _ = prefix_cost(cycle, r, s, ca, cb)
    expected = tuple(pc[j]+ps[j]*cc[j]/(1-cs[j]) for j in range(2))
    require(actual == expected, "periodic_chain_vs_word", "resolvent and series disagree")
    return actual


def check_exchange_and_sorting():
    cases = 0
    for r, s in [(F(1, 2), F(1, 3)), (F(2, 3), F(4, 9)), (F(1, 4), F(2, 3))]:
        for ca, cb in [(1-r, 1-s), (F(2, 3), F(5, 4))]:
            for i, j in product(range(7), repeat=2):
                for suffix in [(), (0, 1, 1, 0), (1, 1, 0)]:
                    ab = prefix_cost((0, 1)+suffix, r, s, ca, cb, (i, j))[0]
                    ba = prefix_cost((1, 0)+suffix, r, s, ca, cb, (i, j))[0]
                    require((ab[0]-ba[0], ab[1]-ba[1]) ==
                            (-cb*(1-r)*r**i, ca*(1-s)*s**j),
                            "exchange_identity", "word exchange vector failed")
            for prior in [F(1, 5), F(1, 2), F(4, 5)]:
                for n in range(1, 9):
                    minima = {}
                    for word in product(range(2), repeat=n):
                        c = prefix_cost(word, r, s, ca, cb)[0]
                        val = prior*c[0]+(1-prior)*c[1]
                        i = word.count(0)
                        minima[i] = min(minima.get(i, val), val)
                        cases += 1
                    for i, value in minima.items():
                        w = greedy(r, s, prior, n, ca=ca, cb=cb, remaining=(i, n-i))
                        c = prefix_cost(w, r, s, ca, cb)[0]
                        require(prior*c[0]+(1-prior)*c[1] == value,
                                "exhaustive_fixed_count_ordering", "greedy order not minimal")
    return {"finite_words_independently_costed": cases,
            "scope": "Ordering at fixed finite counts; not a finite-horizon stopping claim."}


def cycle_word(t, h, k, prior, tie, ca=None, cb=None):
    r, s = t**h, t**k
    ca = 1-r if ca is None else ca
    cb = 1-s if cb is None else cb
    ratio = prior*(1-r)*cb/((1-prior)*(1-s)*ca)
    state = 0
    seen, word = {}, []
    while state not in seen:
        if len(word) > 2000:
            raise RuntimeError("finite commensurate phase did not recur in finite probe")
        seen[state] = len(word)
        value = ratio*t**(-state)
        a = 0 if value > 1 else 1 if value < 1 else tie
        word.append(a)
        state += -h if a == 0 else k
    start = seen[state]
    return tuple(word[:start]), tuple(word[start:]), len(seen)


def check_periodic_and_tail():
    cases = 0
    for t in [F(1, 2), F(2, 3)]:
        for h, k in [(1, 1), (1, 2), (2, 1), (2, 3), (3, 2)]:
            r, s = t**h, t**k
            m = min(1-r, 1-s)
            delta = m*m/16
            ratio_cap = (1-delta)/delta
            J = 0
            while t**(-J) < ratio_cap:
                J += 1
            N = max(J, h)+max(J, k)+1
            for prior in [F(1, 3), F(1, 2), F(2, 3)]:
                require(delta <= prior <= 1-delta, "rational_tail_bound", "prior outside bound")
                values = []
                for tie in [0, 1]:
                    prefix, cycle, states = cycle_word(t, h, k, prior, tie)
                    require(0 in cycle and 1 in cycle, "commensurate_phase", "improper cycle")
                    require(states <= N, "commensurate_phase", "explicit cap exceeded")
                    horizon = 100
                    word = (prefix+cycle*(horizon+1))[:horizon]
                    require(word == greedy(r, s, prior, horizon, tie),
                            "commensurate_phase", "phase recursion disagrees with exact indices")
                    values.append(deterministic_periodic_cost(prefix, cycle, r, s))
                    for T in range(horizon+1):
                        surv = prefix_cost(word[:T], r, s)[1]
                        # Raise the manuscript A*kappa^T bound to h+k:
                        # A^(h+k)=t^(-hk)*ratio_cap^max(h,k), entirely rational.
                        right = t**(h*k*(T-1))*ratio_cap**max(h, k)
                        for val in surv:
                            require(val**(h+k) <= right, "rational_tail_bound", "exact tail bound failed")
                    cases += 1
                require(values[0][0] <= values[1][0] and values[0][1] >= values[1][1],
                        "extreme_tie_order", "extreme costs misordered")
                require(prior*values[0][0]+(1-prior)*values[0][1] ==
                        prior*values[1][0]+(1-prior)*values[1][1],
                        "extreme_tie_order", "tie rules changed Bayes value")
            # Test the same arithmetic phase with arbitrary unequal costs.
            for ca, cb in [(F(3, 7), F(5, 2)), (F(7, 3), F(2, 5))]:
                for tie in [0, 1]:
                    prefix, cycle, _ = cycle_word(t, h, k, F(2, 5), tie, ca, cb)
                    word = (prefix+cycle*201)[:200]
                    require(word == greedy(r, s, F(2, 5), 200, tie, ca, cb),
                            "general_cost_phase", "cost-normalized indices failed")
                    deterministic_periodic_cost(prefix, cycle, r, s, ca, cb)
    return {"normalized_periodic_cases": cases, "tail_horizon": 100,
            "tail_arithmetic": "Rational inequalities after the exact positive power h+k"}


def prefix_mixture_controller(words, weight, r, s):
    T = len(words[0])
    if T != len(words[1]) or T < 1:
        raise RuntimeError("bad prefix lengths")
    n = 2*T
    fallback = n-1
    probs = (weight, 1-weight)
    rows = [F(0)]*n
    rows[0] = sum(probs[j] for j in range(2) if words[j][0] == 0)
    rows[fallback] = (1-s)/(2-r-s)
    updates = [[None, None] for _ in range(n)]
    for a in range(2):
        mass = rows[0] if a == 0 else 1-rows[0]
        q = [F(0)]*n
        if mass == 0 or T == 1:
            q[fallback] = 1
        else:
            for j in range(2):
                if words[j][0] == a:
                    q[1+j*(T-1)] = probs[j]/mass
        updates[0][a] = tuple(q)
    for branch in range(2):
        for pos in range(1, T):
            label = 1+branch*(T-1)+(pos-1)
            rows[label] = F(words[branch][pos] == 0)
            nxt = label+1 if pos+1 < T else fallback
            row = tuple(F(j == nxt) for j in range(n))
            updates[label] = [row, row]
    row = tuple(F(j == fallback) for j in range(n))
    updates[fallback] = [row, row]
    for update in updates:
        for q in update:
            require(q is not None and sum(q) == 1 and all(x >= 0 for x in q),
                    "counted_prefix_mixture", "invalid update distribution")
    return rows, updates


def check_pure_start_mixture():
    cases = 0
    for r, s in [(F(1, 2), F(1, 3)), (F(1, 2), F(1, 2)), (F(2, 3), F(4, 9))]:
        for prior in [F(1, 2), F(4, 7)]:
            for T in [1, 2, 3, 5, 8]:
                words = [greedy(r, s, prior, T, tie) for tie in [0, 1]]
                for weight in [F(0), F(1, 3), F(1, 2), F(1)]:
                    rows, updates = prefix_mixture_controller(words, weight, r, s)
                    actual = controller_cost(rows, updates, r, s)
                    expected = [F(0), F(0)]
                    for w, p in zip(words, [weight, 1-weight]):
                        c, survival, _ = prefix_cost(w, r, s)
                        for model in range(2):
                            expected[model] += p*(c[model]+2*survival[model])
                    require(actual == tuple(expected), "counted_prefix_mixture",
                            "product chain disagrees with mixed word and fallback")
                    require(len(rows) == 2*T, "counted_prefix_mixture", "hidden label growth")
                    cases += 1
    # Exact robust symmetric example: two classical extreme cycles and their mixture.
    for r in [F(1, 4), F(1, 2), F(2, 3), F(3, 4)]:
        c_ab = deterministic_periodic_cost((), (0, 1), r, r)
        c_ba = deterministic_periodic_cost((), (1, 0), r, r)
        require(c_ab == (1+r, F(2)) and c_ba == (F(2), 1+r),
                "symmetric_exact_example", "cycle formula failed")
        v = (3+r)/2
        require(tuple((a+b)/2 for a, b in zip(c_ab, c_ba)) == (v, v),
                "symmetric_exact_example", "equal mixture not balanced")
        rows = [F(1, 2), F(1), F(0)]
        updates = [[(F(0), F(0), F(1)), (F(0), F(1), F(0))] for _ in rows]
        require(controller_cost(rows, updates, r, r) == (v, v),
                "symmetric_exact_example", "counted pure-start three-label implementation failed")
    return {"prefix_controller_cases": cases, "labels_for_T_prefix": "2T including pure start and fallback"}


def factor_integer(n):
    out = {}
    p = 2
    while p*p <= n:
        while n % p == 0:
            out[p] = out.get(p, 0)+1
            n //= p
        p += 1
    if n > 1:
        out[n] = out.get(n, 0)+1
    return out


def exponents(x):
    out = factor_integer(x.numerator)
    for p, v in factor_integer(x.denominator).items():
        out[p] = out.get(p, 0)-v
    return {p: v for p, v in out.items() if v}


def commensurate(r, s):
    er, es = exponents(r), exponents(s)
    primes = sorted(set(er)|set(es))
    p = next(p for p in primes if es.get(p, 0))
    ratio = F(er.get(p, 0), es[p])
    if ratio <= 0 or any(F(er.get(q, 0)) != ratio*es.get(q, 0) for q in primes):
        return None
    h, k = ratio.numerator, ratio.denominator
    base = F(1)
    for p, e in er.items():
        if e % h:
            raise RuntimeError("reduced-ratio exponent did not divide")
        base *= F(p)**(e//h)
    return base, h, k


def check_arithmetic_and_nonperiodic_prefixes():
    cases = [(F(1, 2), F(1, 3), False), (F(2, 3), F(4, 9), True),
             (F(4, 9), F(8, 27), True), (F(3, 4), F(9, 16), True),
             (F(2, 5), F(4, 25), True), (F(2, 3), F(3, 4), False)]
    for r, s, expected in cases:
        result = commensurate(r, s)
        require((result is not None) == expected, "rational_arithmetic_test", "wrong classification")
        if result is not None:
            t, h, k = result
            require(t**h == r and t**k == s and 0 < t < 1,
                    "rational_arithmetic_test", "common rational base failed")
    r, s, prior = F(1, 2), F(1, 3), F(4, 7)
    words = [greedy(r, s, prior, 500, tie) for tie in [0, 1]]
    differing = [i for i in range(500) if words[0][i] != words[1][i]]
    require(differing == [3, 4], "irrational_tied_pair_probe", "expected unique adjacent pair changed")
    ratio = prior/(1-prior)
    lower, upper = min(ratio, r), max(ratio, 1/s)
    for word in words:
        i = j = 0
        for a in word:
            value = ratio*r**i/s**j
            require(lower <= value <= upper, "irrational_tied_pair_probe", "exact logarithmic strip failed")
            i += a == 0
            j += a == 1
    return {"rational_factorization_cases": len(cases),
            "irrational_word_prefix_length": 500, "different_positions": differing,
            "scope": "Finite exact strip/coalescence probe; irrationality and no eventual period are proved in the manuscript."}


def check_memoryless_values():
    for qa, qb in [(F(1, 2), F(2, 3)), (F(3, 4), F(1, 5)), (F(2, 5), F(4, 7))]:
        for ca, cb in [(qa, qb), (F(2, 3), F(5, 4))]:
            target = ca/qa+cb/qb
            for p in [F(i, 20) for i in range(1, 20)]+[qb/(qa+qb)]:
                actual = controller_cost([p], [[(F(1),), (F(1),)]], 1-qa, 1-qb, ca, cb)
                g = p*ca+(1-p)*cb
                require(actual == (g/(p*qa), g/((1-p)*qb)),
                        "memoryless_exact_value", "geometric and product costs disagree")
                require(max(actual) >= target, "memoryless_exact_value", "value below stated V1")
                if p == qb/(qa+qb):
                    require(actual == (target, target), "memoryless_exact_value", "attaining row failed")
    return {"scope": "Exact scalar geometric model costs and general positive-cost V1 formula"}


def main():
    results = {"exchange_and_sorting": check_exchange_and_sorting(),
               "periodic_tail": check_periodic_and_tail(),
               "counted_initial_mixture": check_pure_start_mixture(),
               "arithmetic_test": check_arithmetic_and_nonperiodic_prefixes(),
               "memoryless_value": check_memoryless_values()}
    total = sum(CHECKS.values())
    print(json.dumps({"schema": "theta.r80.arithmetic-memory-diagnostics.v1",
                      "status": "PASS", "arithmetic": "Exact rational arithmetic; no optimizer or floating comparison",
                      "exact_checks": total, "floating_checks": 0, "total_checks": total,
                      "exact_conditions_checked": total, "checks_by_group": dict(sorted(CHECKS.items())),
                      "results": results,
                      "scope": "Finite independent author-team diagnostics. Written proofs establish the quantified results; no formal proof verification, independent human review, exhaustive priority clearance or editorial verdict is asserted."},
                     sort_keys=True, indent=2))


if __name__ == "__main__":
    main()
