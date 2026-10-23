#!/usr/bin/env python3
"""Finite rational challenges of the R76 convex-specification normal form.

These are independently specified finite models, not a proof of the general
normal form, a formal certificate, or a general quantifier-elimination run.
All comparisons below use exact fractions; no assert disappears under -O.
"""
from __future__ import annotations

from collections import Counter
from fractions import Fraction as F
from itertools import product
import json

COUNTS = Counter()


def check(ok, group):
    if not ok:
        raise RuntimeError("Failed exact diagnostic: " + group)
    COUNTS[group] += 1


def eye(n):
    return [[F(i == j) for j in range(n)] for i in range(n)]


def mm(a, b):
    return [[sum((a[i][k] * b[k][j] for k in range(len(b))), F(0))
             for j in range(len(b[0]))] for i in range(len(a))]


def scale(a, q):
    return [[q * x for x in row] for row in a]


def add(*args):
    return [[sum((a[i][j] for a in args), F(0))
             for j in range(len(args[0][0]))] for i in range(len(args[0]))]


def power(a, k):
    r = eye(len(a))
    while k:
        if k % 2:
            r = mm(r, a)
        a = mm(a, a)
        k //= 2
    return r


def kron(a, b):
    return [[a[i][j] * b[k][l]
             for j in range(len(a[0])) for l in range(len(b[0]))]
            for i in range(len(a)) for k in range(len(b))]


def stochastic(a, group):
    check(all(x >= 0 for row in a for x in row), group)
    check(all(sum(row) == 1 for row in a), group)


def row(i, n):
    return [F(i == j) for j in range(n)]


def transpose(a):
    return list(map(list, zip(*a)))


def mean(matrices):
    return scale(add(*matrices), F(1, len(matrices)))


def solve(a, b):
    """Exact Gauss--Jordan elimination, square nonsingular coefficient matrix."""
    n = len(a)
    aug = [list(a[i]) + [b[i]] for i in range(n)]
    for j in range(n):
        pivot = next((i for i in range(j, n) if aug[i][j]), None)
        if pivot is None:
            raise RuntimeError("Singular diagnostic linear system")
        aug[j], aug[pivot] = aug[pivot], aug[j]
        q = aug[j][j]
        aug[j] = [x / q for x in aug[j]]
        for i in range(n):
            if i != j:
                q = aug[i][j]
                aug[i] = [x - q * y for x, y in zip(aug[i], aug[j])]
    return [aug[i][-1] for i in range(n)]


def projection(t):
    """Compute the closed-class projection independently from finite-chain equations."""
    n = len(t)
    reach = [[bool(t[i][j]) or i == j for j in range(n)] for i in range(n)]
    for k in range(n):
        for i in range(n):
            for j in range(n):
                reach[i][j] = reach[i][j] or (reach[i][k] and reach[k][j])
    classes, used = [], set()
    for i in range(n):
        if i in used:
            continue
        cl = [j for j in range(n) if reach[i][j] and reach[j][i]]
        used.update(cl)
        if not any(t[x][y] for x in cl for y in range(n) if y not in cl):
            classes.append(cl)
    mus = []
    for cl in classes:
        k = len(cl)
        a = [[t[cl[j]][cl[i]] - F(i == j) for j in range(k)]
             for i in range(k)]
        a[-1] = [F(1)] * k
        pi = solve(a, [F(0)] * (k - 1) + [F(1)])
        mu = [F(0)] * n
        for x, val in zip(cl, pi):
            mu[x] = val
        mus.append(mu)
    closed = set(x for cl in classes for x in cl)
    transient = [x for x in range(n) if x not in closed]
    h = [[F(0)] * len(classes) for _ in range(n)]
    for k, cl in enumerate(classes):
        for x in cl:
            h[x][k] = F(1)
        if transient:
            a = [[F(i == j) - t[x][y] for j, y in enumerate(transient)]
                 for i, x in enumerate(transient)]
            b = [sum(t[x][y] for y in cl) for x in transient]
            sol = solve(a, b)
            for x, val in zip(transient, sol):
                h[x][k] = val
    return mm(h, mus), mus, classes, h


def deterministic_semigroup_tests():
    """All pairs of deterministic maps on 2 and 3 labels, with C2 images."""
    for n in (2, 3):
        maps = list(product(range(n), repeat=n))
        identity = tuple(range(n))
        for a in maps:
            for b in maps:
                known = {(identity, 0)}
                pending = [(identity, 0)]
                while pending:
                    f, g = pending.pop()
                    for q in (a, b):
                        new = (tuple(q[x] for x in f), 1 - g)
                        if new not in known:
                            known.add(new)
                            pending.append(new)
                by_g = {0: [], 1: []}
                for f, g in sorted(known):
                    by_g[g].append([[F(f[i] == j) for j in range(n)]
                                    for i in range(n)])
                t = mean(by_g[0])  # contains I; all identity-word support edges
                e, mus, classes, h = projection(t)
                stochastic(e, "exhaustive_deterministic_projection")
                check(mm(e, e) == e, "exhaustive_deterministic_projection")
                check(mm(t, e) == e and mm(e, t) == e,
                      "exhaustive_deterministic_projection")
                fs = {}
                for g, matrices in by_g.items():
                    fs[g] = mm(mm(e, matrices[0]), e)
                    for q in matrices:
                        check(mm(mm(e, q), e) == fs[g],
                              "exhaustive_fiber_collapse")
                check(fs[0] == e, "exhaustive_group_action")
                check(mm(fs[1], fs[1]) == e, "exhaustive_group_action")
                for i in range(n):
                    mixed = sum(v > 0 for v in h[i]) > 1
                    check(len(classes) + int(mixed) <= n,
                          "exhaustive_initializer_charge")
                # Convex ranges are independently computed on the full finite
                # semigroup, so the inequalities test every word of this model.
                d = [[F(i, n - 1), 1 - F(i, n - 1)] for i in range(n)]
                for i in range(n):
                    for g, matrices in by_g.items():
                        vals = [mm([row(i, n)], mm(q, d))[0][0] for q in matrices]
                        projected = mm([row(i, n)], mm(fs[g], d))[0][0]
                        check(min(vals) <= projected <= max(vals),
                              "exhaustive_convex_specification")


def noncommuting_hidden_tests():
    r0 = [[F(2, 3), F(1, 3)], [F(1, 4), F(3, 4)]]
    r1 = [[F(4, 5), F(1, 5)], [F(2, 7), F(5, 7)]]
    flip = [[F(0), F(1)], [F(1), F(0)]]
    qa, qb = kron(flip, r0), kron(flip, r1)
    check(mm(qa, qb) != mm(qb, qa), "noncommuting_hidden_dynamics")
    identity_words = [eye(4), mm(qa, qa), mm(qa, qb), mm(qb, qa), mm(qb, qb)]
    t = mean(identity_words)
    e, mus, classes, h = projection(t)
    check(len(classes) == 2 and all(len(x) == 2 for x in classes),
          "noncommuting_hidden_dynamics")
    check(mm(e, mm(qa, qa)) != e, "noncommuting_hidden_dynamics")
    check(mm(mm(e, mm(qa, qa)), e) == e, "noncommuting_hidden_dynamics")
    f = mm(mm(e, qa), e)
    check(mm(mm(e, qb), e) == f and mm(f, f) == e,
          "noncommuting_hidden_dynamics")
    d = [[F(0)], [F(1, 3)], [F(2, 3)], [F(1)]]
    for length in range(9):
        for w in product((qa, qb), repeat=length):
            q = eye(4)
            for letter in w:
                q = mm(q, letter)
            value = mm([row(0, 4)], mm(q, d))[0][0]
            lo, hi = (F(0), F(1, 3)) if length % 2 == 0 else (F(2, 3), F(1))
            check(lo <= value <= hi, "noncommuting_word_intervals")
            check(mm(mm(e, q), e) == (e if length % 2 == 0 else f),
                  "noncommuting_word_projection")
    check(mm(power(t, 25), e) == e, "noncommuting_lazy_projection")


def transient_mixed_start_test():
    p = [[F((i + 1) % 3 == j) for j in range(3)] for i in range(3)]
    r = [[F(2, 3), F(1, 3)], [F(1, 4), F(3, 4)]]
    qcore = kron(p, r)
    lam = [F(1, 2), F(1, 3), F(1, 6)]
    first = kron(mm([lam], p), [[F(1), F(0)]])[0]
    q = [[F(0)] + first] + [[F(0)] + a for a in qcore]
    stochastic(q, "transient_initializer")
    e, mus, classes, h = projection(mean([eye(7), power(q, 3)]))
    check(len(classes) == 3 and h[0] == lam, "transient_initializer")
    check(mm(mm(e, q), e) != e, "transient_initializer")
    check(power(mm(mm(e, q), e), 3) == e, "transient_initializer")
    check(sum(v > 0 for v in h[0]) == 3 and len(classes) + 1 <= 7,
          "transient_initializer")
    for k in range(1, 10):
        check(mm(mm(e, power(q, 3 * k)), e) == e, "transient_identity_words")


def finite_word_trap():
    eps = F(1, 1000)
    q = [[eps, 1 - eps], [1 - eps, eps]]
    d = [[F(0)], [F(1)]]
    check(mm([row(0, 2)], mm(q, d))[0][0] == 1 - eps,
          "representatives_are_insufficient")
    even_value = mm([row(0, 2)], mm(power(q, 1000), d))[0][0]
    check(even_value > F(1, 4), "representatives_are_insufficient")
    e, mus, classes, h = projection(mean([eye(2), power(q, 2)]))
    check(e == [[F(1, 2), F(1, 2)]] * 2,
          "representatives_are_insufficient")
    check(mm(mm(e, q), e) == e, "representatives_are_insufficient")


def robust_scalar_tests():
    # Exact checks of the zero-sum l2 estimate, with arbitrary signs and
    # multiple outputs; no sampled singular value is substituted for proof.
    for values in product(range(-3, 4), repeat=3):
        z = [F(x, 12) for x in values]
        z.append(-sum(z))
        delta = sum(abs(x) for x in z) / 2
        check(sum(x * x for x in z) <= 2 * delta * delta,
              "zero_sum_fourier_error_bound")
    for p in (2, 3, 5, 7, 11, 13, 17, 19):
        beta = [F((j * j + 3 * j + 1) % (p + 1), p) for j in range(p)]
        lo, hi = min(beta), max(beta)
        radius, center = (hi - lo) / 2, (lo + hi) / 2
        check(max(abs(x - center) for x in beta) == radius,
              "prime_orbit_chebyshev_upper")
        for den in range(1, 12):
            for num in range(den + 1):
                q = F(num, den)
                check(max(abs(x - q) for x in beta) >= radius,
                      "prime_orbit_chebyshev_lower")
        for k in range(1, p):
            check(p % k != 0 or k == 1, "prime_orbit_degrees")


def main():
    deterministic_semigroup_tests()
    noncommuting_hidden_tests()
    transient_mixed_start_test()
    finite_word_trap()
    robust_scalar_tests()
    total = sum(COUNTS.values())
    print(json.dumps({
        "schema": "theta.r76.robust-finite-diagnostics.v1", "status": "PASS",
        "total_checks": total, "exact_checks": total, "floating_checks": 0,
        "groups": dict(sorted(COUNTS.items())),
        "coverage": [
            "All ordered pairs of deterministic maps on 2 and 3 labels, C2 word images, complete finite semigroup closure",
            "Exact closed-class projection from independently solved stationary/absorption equations",
            "Noncommuting rational hidden dynamics with only a sandwiched group action",
            "A transient pure start that projects to a mixed three-orbit preparation",
            "A representative-word approximation trap with eventual order-one error",
            "Finite zero-sum Fourier norm and prime-orbit Chebyshev certificates"
        ],
        "limitations": [
            "Finite diagnostics do not prove the continuum specification/minimax theorems.",
            "No general real quantifier elimination, formal proof, human review or priority certification is performed."
        ]}, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
