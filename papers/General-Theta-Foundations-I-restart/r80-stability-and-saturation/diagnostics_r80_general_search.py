#!/usr/bin/env python3
"""Exact finite probes for the n-location arithmetic saturation theorem.

Independent word sums, product-chain linear systems, finite ordering searches,
and rational powers test particular instances. They are not proofs of the
universal theorem, an exhaustive controller search, or a human referee report.
"""
from collections import Counter
from fractions import Fraction as F
from itertools import combinations, permutations, product
from math import gcd
import json

CHECKS = Counter()


def require(condition, group, message):
    if not condition:
        raise RuntimeError(f"{group}: {message}")
    CHECKS[group] += 1


def ceil_fraction(x):
    return -(-x.numerator // x.denominator)


def solve(matrix, vector):
    n = len(vector)
    rows = [[F(x) for x in matrix[i]]+[F(vector[i])] for i in range(n)]
    for col in range(n):
        pivot = next((i for i in range(col, n) if rows[i][col]), None)
        if pivot is None:
            raise RuntimeError("singular explicit product-chain system")
        rows[col], rows[pivot] = rows[pivot], rows[col]
        scale = rows[col][col]
        rows[col] = [x/scale for x in rows[col]]
        for i in range(n):
            if i != col:
                scale = rows[i][col]
                rows[i] = [x-scale*y for x, y in zip(rows[i], rows[col])]
    return tuple(row[-1] for row in rows)


def word_cost(word, r, c, counts=None):
    n = len(r)
    counts = list(counts or (0,)*n)
    risks = [F(0)]*n
    for a in word:
        for i in range(n):
            risks[i] += c[a]*r[i]**counts[i]
        counts[a] += 1
    return tuple(risks), tuple(r[i]**counts[i] for i in range(n)), tuple(counts)


def greedy(r, c, prior, length, priority=None, remaining=None):
    n = len(r)
    priority = tuple(range(n)) if priority is None else tuple(priority)
    rank = {a: j for j, a in enumerate(priority)}
    scores = [prior[i]*(1-r[i])/c[i] for i in range(n)]
    counts, word = [0]*n, []
    for _ in range(length):
        available = [i for i in range(n) if remaining is None or counts[i] < remaining[i]]
        a = min(available, key=lambda i: (-scores[i], rank[i]))
        word.append(a)
        scores[a] *= r[a]
        counts[a] += 1
    return tuple(word)


def controller_cost(rows, updates, r, c):
    labels, n = len(rows), len(r)
    for row, update in zip(rows, updates):
        require(len(row) == n and sum(row) == 1 and min(row) >= 0,
                "controller_validity", "invalid command row")
        for q in update:
            require(len(q) == labels and sum(q) == 1 and min(q) >= 0,
                    "controller_validity", "invalid counted-label update")
    costs = [sum(row[i]*c[i] for i in range(n)) for row in rows]
    values = []
    for model in range(n):
        transition = [[sum(rows[k][a]*(r[model] if a == model else 1)*updates[k][a][j]
                           for a in range(n)) for j in range(labels)] for k in range(labels)]
        require(all(sum(row) <= 1 and min(row) >= 0 for row in transition),
                "controller_validity", "product transition is not substochastic")
        value = solve([[F(k == j)-transition[k][j] for j in range(labels)]
                       for k in range(labels)], costs)
        require(min(value) >= 0, "controller_validity", "negative resolvent cost")
        values.append(value[0])
    return tuple(values)


def fallback(r, c):
    invq = [1/(1-x) for x in r]
    z = sum(invq)
    row = tuple(x/z for x in invq)
    value = sum(c[i]/(1-r[i]) for i in range(len(r)))
    return row, value


def word_periodic_cost(prefix, cycle, r, c):
    pc, ps, _ = word_cost(prefix, r, c)
    cc, cs, _ = word_cost(cycle, r, c)
    return tuple(None if cs[i] == 1 else pc[i]+ps[i]*cc[i]/(1-cs[i]) for i in range(len(r)))


def chain_periodic_cost(prefix, cycle, r, c):
    word, n = tuple(prefix)+tuple(cycle), len(r)
    labels = len(word)
    rows = [tuple(F(a == j) for j in range(n)) for a in word]
    updates = []
    for k in range(labels):
        nxt = k+1 if k+1 < labels else len(prefix)
        q = tuple(F(j == nxt) for j in range(labels))
        updates.append([q]*n)
    actual = controller_cost(rows, updates, r, c)
    require(actual == word_periodic_cost(prefix, cycle, r, c),
            "periodic_product_chain", "geometric word sum and product resolvent differ")
    return actual


def prefix_mixture(words, weights, r, c):
    n, branches, T = len(r), len(words), len(words[0])
    require(T >= 1 and all(len(w) == T for w in words) and branches <= n,
            "counted_prefix_mixture", "bad prescribed prefix family")
    require(sum(weights) == 1 and min(weights) >= 0,
            "counted_prefix_mixture", "invalid mixture")
    labels = 1+branches*(T-1)+1
    terminal = labels-1
    rows = [None]*labels
    updates = [[None]*n for _ in range(labels)]
    rows[0] = tuple(sum(weights[b] for b in range(branches) if words[b][0] == a) for a in range(n))
    for a in range(n):
        q = [F(0)]*labels
        if rows[0][a] == 0 or T == 1:
            q[terminal] = 1
        else:
            for b in range(branches):
                if words[b][0] == a:
                    q[1+b*(T-1)] = weights[b]/rows[0][a]
        updates[0][a] = tuple(q)
    for b in range(branches):
        for pos in range(1, T):
            label = 1+b*(T-1)+pos-1
            rows[label] = tuple(F(a == words[b][pos]) for a in range(n))
            nxt = label+1 if pos+1 < T else terminal
            q = tuple(F(j == nxt) for j in range(labels))
            updates[label] = [q]*n
    rows[terminal], B = fallback(r, c)
    q = tuple(F(j == terminal) for j in range(labels))
    updates[terminal] = [q]*n
    actual = controller_cost(rows, updates, r, c)
    expected = [F(0)]*n
    for word, weight in zip(words, weights):
        wc, ws, _ = word_cost(word, r, c)
        for i in range(n):
            expected[i] += weight*(wc[i]+B*ws[i])
    require(actual == tuple(expected), "counted_prefix_mixture", "conditional pure-start routing changes risk")
    require(labels == 1+branches*(T-1)+1 and labels <= n*T,
            "counted_prefix_mixture", "label count exceeds nT")
    return actual, labels


def periodic_mixture(prefixes, cycles, weights, r, c):
    """A pure initializer and disjoint full finite tail automata."""
    n, branches = len(r), len(weights)
    words = [tuple(p)+tuple(cy) for p, cy in zip(prefixes, cycles)]
    offsets, labels = [], 1
    for word in words:
        offsets.append(labels)
        labels += len(word)
    rows = [None]*labels
    updates = [[None]*n for _ in range(labels)]
    rows[0] = tuple(sum(weights[b] for b in range(branches) if words[b][0] == a) for a in range(n))
    for a in range(n):
        q = [F(0)]*labels
        if not rows[0][a]:
            q[0] = 1  # An impossible command's update remains a probability row.
        else:
            for b in range(branches):
                if words[b][0] == a:
                    next_pos = 1 if len(words[b]) > 1 else len(prefixes[b])
                    q[offsets[b]+next_pos] = weights[b]/rows[0][a]
        updates[0][a] = tuple(q)
    for b, word in enumerate(words):
        for pos, action in enumerate(word):
            label = offsets[b]+pos
            rows[label] = tuple(F(a == action) for a in range(n))
            next_pos = pos+1 if pos+1 < len(word) else len(prefixes[b])
            q = tuple(F(j == offsets[b]+next_pos) for j in range(labels))
            updates[label] = [q]*n
    actual = controller_cost(rows, updates, r, c)
    components = [word_periodic_cost(p, cy, r, c) for p, cy in zip(prefixes, cycles)]
    expected = tuple(sum(weights[b]*components[b][i] for b in range(branches)) for i in range(n))
    require(actual == expected, "counted_periodic_mixture", "full finite pure-start mixture changes risk")
    require(labels == 1+sum(len(w) for w in words), "counted_periodic_mixture", "uncounted initial or branch memory")
    return actual, labels


def constants(r, c):
    tau = [c[i]/(1-r[i]) for i in range(len(r))]
    B, cmin, cmax, rmin = sum(tau), min(c), max(c), min(r)
    T0 = ceil_fraction(2*B/cmin)
    g = cmin*rmin**T0/2
    T1 = ceil_fraction(2*B*B/(cmin*g))
    K = cmax*T1+B
    delta = g/(2*K)
    C = max(tau)/(delta*min(tau))
    A = C*max(C, 1/rmin)
    require(cmin*T0 >= 2*B and cmin*(T0-1) < 2*B,
            "explicit_constants", "incorrect T0 ceiling")
    require(B*B/(cmin*T1) <= g/2 and B*B/(cmin*(T1-1)) > g/2,
            "explicit_constants", "incorrect T1 truncation bound")
    require(0 < g <= cmin/2 and 0 < delta < F(1, len(r)),
            "explicit_constants", "invalid deletion or prior constant")
    require(A == C*max(C, 1/rmin), "explicit_constants", "rational exponential constant mismatch")
    return {"B": B, "T0": T0, "g": g, "T1": T1, "K": K,
            "delta": delta, "C": C, "A": A}


def finite_phase(t, h, c, prior, priority):
    n, r = len(h), tuple(t**v for v in h)
    scores = tuple(prior[i]*(1-r[i])/c[i] for i in range(n))
    ratios = tuple(scores[i]/scores[-1] for i in range(n-1))+(F(1),)
    rank = {a: j for j, a in enumerate(priority)}
    state = (0,)*(n-1)
    seen, word = {}, []
    while state not in seen:
        if len(word) > 4000:
            raise RuntimeError("commensurate finite-coset probe did not recur")
        seen[state] = len(word)
        values = tuple(ratios[i]*t**(-state[i]) for i in range(n-1))+(F(1),)
        a = min(range(n), key=lambda i: (-values[i], rank[i]))
        word.append(a)
        state = tuple(state[i]+(h[-1] if a == n-1 else -h[i] if a == i else 0) for i in range(n-1))
    start = seen[state]
    return tuple(word[:start]), tuple(word[start:]), len(seen)


def check_exchange_ordering_and_ties():
    cases = 0
    for n in (3, 4):
        r = tuple(F(1, i+2) for i in range(n))
        c = tuple(F(i+2, i+3) for i in range(n))
        prior = tuple(F(i+1, n*(n+1)//2) for i in range(n))
        for counts in product(range(3), repeat=n):
            for i, j in combinations(range(n), 2):
                suffix = tuple(reversed(range(n)))
                ij = word_cost((i, j)+suffix, r, c, counts)[0]
                ji = word_cost((j, i)+suffix, r, c, counts)[0]
                expected = tuple(-c[j]*(1-r[i])*r[i]**counts[i] if k == i else
                                 c[i]*(1-r[j])*r[j]**counts[j] if k == j else F(0) for k in range(n))
                require(tuple(ij[k]-ji[k] for k in range(n)) == expected,
                        "adjacent_exchange", "n-coordinate adjacent exchange failed")
        for length in range(1, 6):
            minima = {}
            for word in product(range(n), repeat=length):
                counts = tuple(word.count(i) for i in range(n))
                risk = word_cost(word, r, c)[0]
                value = sum(prior[i]*risk[i] for i in range(n))
                minima[counts] = min(minima.get(counts, value), value)
                cases += 1
            for counts, value in minima.items():
                word = greedy(r, c, prior, length, remaining=counts)
                risk = word_cost(word, r, c)[0]
                require(sum(prior[i]*risk[i] for i in range(n)) == value,
                        "finite_fixed_count_ordering", "greedy fixed-count order failed")
        # All streams have equal initial index and the same ratio. Each complete
        # level is a tied block. Enumerate TWO independently permuted levels.
        r = (F(2, 3),)*n
        c = tuple(F(i+2, i+3) for i in range(n))
        tau = tuple(x/(1-r[0]) for x in c)
        prior = tuple(x/sum(tau) for x in tau)
        orders = list(permutations(range(n)))
        for lam in [tuple(F(i-n//2) for i in range(n)), tuple(F((-1)**i*(i+1), i+2) for i in range(n))]:
            priority = tuple(sorted(range(n), key=lambda i: -lam[i]/prior[i]))
            chosen = word_cost(priority*2, r, c)[0]
            target = sum(lam[i]*chosen[i] for i in range(n))
            for first, second in product(orders, repeat=2):
                risk = word_cost(first+second, r, c)[0]
                require(sum(lam[i]*risk[i] for i in range(n)) >= target,
                        "consistent_priority_support_function", "independent tied blocks beat global priority")
            for i, j in combinations(range(n), 2):
                risk1 = word_cost((i, j), r, c)[0]
                risk2 = word_cost((j, i), r, c)[0]
                level = prior[i]*(1-r[i])/c[i]
                expected = tuple(c[i]*c[j]*level*(-1/prior[i] if k == i else 1/prior[j] if k == j else 0)
                                 for k in range(n))
                require(tuple(risk1[k]-risk2[k] for k in range(n)) == expected,
                        "tied_exchange_normalization", "prior-normalized tie identity failed")
    return {"finite_words_costed": cases, "locations": [3, 4],
            "scope": "Finite fixed-count ordering and two-level tied-block support-function probes"}


def check_mixtures_and_memoryless():
    cases = 0
    for n in (3, 4):
        for normalized in (True, False):
            r = tuple(F(1, i+2) for i in range(n))
            c = tuple(1-r[i] if normalized else F(i+2, i+3) for i in range(n))
            prior = (F(1, n),)*n
            words_priorities = [tuple((i+j) % n for i in range(n)) for j in range(n)]
            weights_list = [(F(1, n),)*n,
                            tuple(F(2**i, 2**n-1) for i in range(n)),
                            (F(1),)+(F(0),)*(n-1)]
            for T in (1, 2, 3, 5):
                words = [greedy(r, c, prior, T, priority) for priority in words_priorities]
                for weights in weights_list:
                    prefix_mixture(words, weights, r, c)
                    cases += 1
            row, B = fallback(r, c)
            actual = controller_cost([row], [[(F(1),)]*n], r, c)
            require(actual == (B,)*n, "one_label_frontier", "balanced success masses do not attain sum tau")
            for den in (3, 5, 7):
                weights = [F(den+i) for i in range(n)]
                testrow = tuple(x/sum(weights) for x in weights)
                actual = controller_cost([testrow], [[(F(1),)]*n], r, c)
                mean = sum(testrow[i]*c[i] for i in range(n))
                require(actual == tuple(mean/(testrow[i]*(1-r[i])) for i in range(n)),
                        "one_label_frontier", "geometric and product costs differ")
                require(max(actual) >= B, "one_label_frontier", "one-label lower bound failed")
    return {"explicit_prefix_controllers": cases,
            "pure_initial_label_and_fallback_counted": True, "label_formula": "1+b(T-1)+1 <= nT, b<=n, n>=2"}


def check_deletion_and_prior_bounds():
    cases = 0
    for n in (3, 4):
        for rr in (F(1, 3), F(1, 2), F(2, 3)):
            r, c = (rr,)*n, (1-rr,)*n
            d = constants(r, c)
            words = [tuple((i+j) % n for i in range(n)) for j in range(n)]
            risks = [word_periodic_cost((), w, r, c) for w in words]
            average = tuple(sum(row[i] for row in risks)/n for i in range(n))
            V = F(n)-(1-rr)*F(n-1, 2)
            require(average == (V,)*n and V <= d["B"],
                    "attaining_symmetric_instances", "cyclic mixture not an exact equalizer")
            require(d["delta"] <= F(1, n), "prior_lower_bound", "symmetric least-favorable prior violates delta")
            actual, labels = periodic_mixture([()]*n, words, [F(1, n)]*n, r, c)
            require(actual == (V,)*n and labels == 1+n*n,
                    "attaining_symmetric_instances", "counted finite mixture fails to attain exact value")
            for omitted in range(n):
                deleted = [word_periodic_cost((), tuple(a for a in w if a != omitted), r, c) for w in words]
                for model in range(n):
                    if model == omitted:
                        continue
                    other = sum(row[model] for row in deleted)/n
                    require(V-other >= d["g"], "deletion_lower_bound", "finite attaining example violates deletion gap")
                first_mass = sum(F(w.index(omitted) < d["T0"], n) for w in words)
                require(first_mass >= F(1, 2), "deletion_lower_bound", "planned first occurrence is too late")
            cases += 1
        # A proper, general-cost product controller with worst risk exactly B:
        # removing command i yields the conditional i.i.d. row on the others.
        r = tuple(F(1, i+2) for i in range(n))
        for c in [tuple(1-x for x in r), tuple(F(i+2, i+3) for i in range(n))]:
            d = constants(r, c)
            row, B = fallback(r, c)
            for omitted in range(n):
                require((1-row[omitted]*(1-r[omitted]))**d["T0"] <= F(1, 2),
                        "deletion_lower_bound", "success Markov consequence failed")
                require(1-(1-row[omitted])**d["T0"] >= F(1, 2),
                        "deletion_lower_bound", "first omitted call has insufficient planned mass")
                for model in range(n):
                    if model == omitted:
                        continue
                    kept = [j for j in range(n) if j != omitted]
                    mass = 1-row[omitted]
                    mean = sum(row[j]*c[j]/mass for j in kept)
                    deleted_cost = mean/((row[model]/mass)*(1-r[model]))
                    require(B-deleted_cost == c[omitted]/(1-r[omitted]),
                            "deletion_lower_bound", "conditional i.i.d. deletion cost mismatch")
                    require(B-deleted_cost >= d["g"], "deletion_lower_bound", "proper controller deletion gap failed")
            # Exact algebra behind the least-favorable lower bound. A scalar
            # pi<delta cannot satisfy the separator inequality for any V>=cmin.
            for pi in (d["delta"]/4, d["delta"]/2, d["delta"]*F(3, 4)):
                for V in (min(c), B):
                    upper = (1-pi)*(V-d["g"]/2)+pi*d["K"]
                    require(upper < V, "prior_lower_bound", "small prior not excluded by explicit witness")
            cases += 1
    return {"attaining_or_uniformly_proper_families": cases,
            "scope": "Deletion tested on explicit exact attaining symmetric instances and B-cost proper i.i.d. controllers; general proof remains analytic"}


def check_phase_cap_and_powered_tail():
    cases = 0
    for t, h in [(F(1, 2), (1, 2, 3)), (F(2, 3), (1, 1, 2)),
                 (F(1, 2), (1, 1, 2, 3)), (F(2, 3), (1, 2, 2, 3))]:
        n, r = len(h), tuple(t**v for v in h)
        S = sum(F(1, v) for v in h)
        aa, bb = S.numerator, S.denominator
        for normalized in (True, False):
            c = tuple(1-r[i] if normalized else F(i+2, i+3) for i in range(n))
            d = constants(r, c)
            J = 0
            while t**(-J) < d["C"]:
                J += 1
            N0 = max(J, max(h))
            cap = (2*N0+1)**(n-1)
            for prior in [(F(1, n),)*n, tuple(F(i+1, n*(n+1)//2) for i in range(n))]:
                require(min(prior) >= d["delta"], "powered_tail", "test prior outside explicit bounds")
                prefixes, cycles = [], []
                for priority in [tuple(range(n)), tuple(reversed(range(n)))]:
                    prefix, cycle, labels = finite_phase(t, h, c, prior, priority)
                    prefixes.append(prefix)
                    cycles.append(cycle)
                    require(labels <= cap and all(i in cycle for i in range(n)),
                            "finite_coset_cap", "phase exceeds cap or cycle is improper")
                    word = (prefix+cycle*201)[:120]
                    require(word == greedy(r, c, prior, len(word), priority),
                            "finite_coset_cap", "relative lattice state differs from exact score rule")
                    chain_periodic_cost(prefix, cycle, r, c)
                    for T in range(len(word)+1):
                        _, survival, _ = word_cost(word[:T], r, c)
                        right = d["A"]**aa*t**(bb*T)
                        for s in survival:
                            require(s**aa <= right, "powered_tail", "rational powered tail inequality failed")
                    cases += 1
                _, labels = periodic_mixture(prefixes, cycles, (F(2, 5), F(3, 5)), r, c)
                require(labels <= 1+n*cap, "finite_coset_cap", "counted mixture exceeds effective cap")
    return {"commensurate_phase_instances": cases, "finite_horizon": 120,
            "powered_identity": "For sum_i(1/h_i)=a/b, kappa^a=t^b and A=C*max(C,1/r_min), entirely rational",
            "cap": "N <= (2 max(J,h_max)+1)^(n-1); a sufficient cap, not a minimal-memory claim"}


def factor(x):
    out, p = {}, 2
    while p*p <= x:
        while x % p == 0:
            out[p] = out.get(p, 0)+1
            x //= p
        p += 1
    if x > 1:
        out[x] = out.get(x, 0)+1
    return out


def exponent_vector(x):
    out = factor(x.numerator)
    for p, v in factor(x.denominator).items():
        out[p] = out.get(p, 0)-v
    return {p: v for p, v in out.items() if v}


def proportional(x, y):
    primes = set(x)|set(y)
    p = next(p for p in primes if y.get(p, 0))
    scale = F(x.get(p, 0), y[p])
    return scale > 0 and all(F(x.get(q, 0)) == scale*y.get(q, 0) for q in primes)


def common_base(r):
    vectors = [exponent_vector(x) for x in r]
    if not all(proportional(v, vectors[0]) for v in vectors):
        return None
    divisor = 0
    for e in vectors[0].values():
        divisor = gcd(divisor, abs(e))
    primitive = {p: e//divisor for p, e in vectors[0].items()}
    p = next(iter(primitive))
    h = tuple(v[p]//primitive[p] for v in vectors)
    require(all(k > 0 and all(v.get(q, 0) == k*primitive.get(q, 0) for q in set(v)|set(primitive))
                for k, v in zip(h, vectors)), "prime_vector_arithmetic", "primitive exponent ray failed")
    base = F(1)
    for p, e in primitive.items():
        base *= F(p)**e
    return base, h


def check_partial_classes_and_factorization():
    cases = [(F(1, 2), F(1, 4), F(1, 8)),
             (F(4, 9), F(8, 27), F(16, 81)),
             (F(1, 2), F(1, 4), F(1, 3)),
             (F(2, 3), F(4, 9), F(8, 27), F(16, 81)),
             (F(1, 2), F(1, 4), F(1, 3), F(1, 9)),
             (F(2, 3), F(3, 4), F(4, 5))]
    expected = [True, True, False, True, False, False]
    for r, yes in zip(cases, expected):
        result = common_base(r)
        require((result is not None) == yes, "prime_vector_arithmetic", "incorrect commensurability classification")
        if result is not None:
            base, h = result
            require(0 < base < 1 and tuple(base**k for k in h) == r,
                    "prime_vector_arithmetic", "common rational base does not reconstruct data")
    probes = []
    for r, classes in [((F(1, 2), F(1, 4), F(1, 3)), (0, 0, 1)),
                       ((F(1, 2), F(1, 4), F(1, 3), F(1, 9)), (0, 0, 1, 1))]:
        n, c = len(r), tuple(1-x for x in r)
        vectors = [exponent_vector(x) for x in r]
        for i, j in combinations(range(n), 2):
            require(proportional(vectors[i], vectors[j]) == (classes[i] == classes[j]),
                    "partial_commensurability", "incorrect class partition")
        prior = (F(1, n),)*n
        words = [greedy(r, c, prior, 240, priority) for priority in [tuple(range(n)), tuple(reversed(range(n)))]]
        collapsed = [tuple(classes[a] for a in w) for w in words]
        require(collapsed[0][n:] == collapsed[1][n:], "partial_commensurability",
                "class sequence did not coalesce after initial cross-class tie")
        require(words[0][n:] != words[1][n:], "partial_commensurability",
                "probe failed to retain within-class tie freedom")
        for word in words:
            scores = list(prior)
            span_cap = 1/min(r)
            for a in word:
                require(max(scores)/min(scores) <= span_cap,
                        "partial_commensurability", "exact bounded score span failed")
                scores[a] *= r[a]
        probes.append({"n": n, "prefix_length": 240, "class_word_equal_after": n,
                       "command_words_still_differ": True})
    return {"prime_vector_cases": len(cases), "partial_class_probes": probes,
            "scope": "Finite class-word coalescence and exact arithmetic classification; nonperiodicity follows from the written irrational-frequency proof"}


def main():
    results = {"exchange_and_ties": check_exchange_ordering_and_ties(),
               "counted_mixtures": check_mixtures_and_memoryless(),
               "deletion_and_prior": check_deletion_and_prior_bounds(),
               "phase_and_tail": check_phase_cap_and_powered_tail(),
               "arithmetic_classes": check_partial_classes_and_factorization()}
    total = sum(CHECKS.values())
    print(json.dumps({"schema": "theta.r80.general-search-diagnostics.v1", "status": "PASS",
                      "arithmetic": "Exact rational arithmetic; no optimizer or floating comparison",
                      "exact_checks": total, "floating_checks": 0, "total_checks": total,
                      "checks_by_group": dict(sorted(CHECKS.items())), "results": results,
                      "scope": "Finite internal author-team diagnostics. The manuscript supplies universal proofs. No formal proof verification, independent human referee judgment, exhaustive novelty clearance, or editorial acceptance is asserted."},
                     sort_keys=True, indent=2))


if __name__ == "__main__":
    main()
