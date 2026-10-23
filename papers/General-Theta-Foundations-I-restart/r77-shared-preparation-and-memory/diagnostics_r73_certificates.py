#!/usr/bin/env python3
"""Exact finite diagnostics for R73 finite certificates and background damping.

This script uses Fraction and explicit checks, including under python -O.
It verifies finite algebra and constructed examples, not all quantified
theorems, a quantifier-elimination run, formal proof, or external review.
"""
from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from fractions import Fraction as F
from pathlib import Path


COUNTS: dict[str, int] = {}


def check(condition: bool, group: str, message: str) -> None:
    COUNTS[group] = COUNTS.get(group, 0) + 1
    if not condition:
        raise RuntimeError(f"Exact check failed [{group}]: {message}")


def eye(n: int):
    return tuple(tuple(F(i == j) for j in range(n)) for i in range(n))


def mm(a, b):
    return tuple(tuple(sum((a[i][k] * b[k][j] for k in range(len(b))), F(0))
                       for j in range(len(b[0]))) for i in range(len(a)))


def vm(v, a):
    return tuple(sum((v[k] * a[k][j] for k in range(len(v))), F(0))
                 for j in range(len(a[0])))


def dot(v, d):
    return sum((x * y for x, y in zip(v, d)), F(0))


def blend(a, b, alpha):
    return tuple(tuple(alpha * x + (1 - alpha) * y for x, y in zip(ar, br))
                 for ar, br in zip(a, b))


def is_stochastic(a):
    return all(all(x >= 0 for x in row) and sum(row) == 1 for row in a)


def perm(p):
    return tuple(tuple(F(j == p[i]) for j in range(len(p))) for i in range(len(p)))


def det3(a):
    return (a[0][0] * (a[1][1] * a[2][2] - a[1][2] * a[2][1])
            - a[0][1] * (a[1][0] * a[2][2] - a[1][2] * a[2][0])
            + a[0][2] * (a[1][0] * a[2][1] - a[1][1] * a[2][0]))


def outputs(a, d, n):
    v = tuple(F(i == 0) for i in range(len(a)))
    ans = []
    for _ in range(n):
        ans.append(dot(v, d))
        v = vm(v, a)
    return ans


# Sparse exact polynomial arithmetic in the six off-diagonal entries.
ZERO_MONOMIAL = (0,) * 6


def pconst(x):
    x = F(x)
    return {} if not x else {ZERO_MONOMIAL: x}


def pvar(i):
    m = [0] * 6
    m[i] = 1
    return {tuple(m): F(1)}


def padd(*args):
    out = {}
    for a in args:
        for m, c in a.items():
            out[m] = out.get(m, F(0)) + c
    return {m: c for m, c in out.items() if c}


def pscale(a, c):
    return {m: v * F(c) for m, v in a.items() if v * F(c)}


def pmul(a, b):
    out = {}
    for m, c in a.items():
        for n, d in b.items():
            k = tuple(x + y for x, y in zip(m, n))
            out[k] = out.get(k, F(0)) + c * d
    return {m: c for m, c in out.items() if c}


def psub(a, b):
    return padd(a, pscale(b, -1))


def pdet3(a):
    return padd(pmul(a[0][0], psub(pmul(a[1][1], a[2][2]), pmul(a[1][2], a[2][1]))),
                pscale(pmul(a[0][1], psub(pmul(a[1][0], a[2][2]), pmul(a[1][2], a[2][0]))), -1),
                pmul(a[0][2], psub(pmul(a[1][0], a[2][1]), pmul(a[1][1], a[2][0]))))


def symbolic_certificate():
    x = [pvar(i) for i in range(6)]
    one = pconst(1)
    q = ((psub(one, padd(x[0], x[1])), x[0], x[1]),
         (x[2], psub(one, padd(x[2], x[3])), x[3]),
         (x[4], x[5], psub(one, padd(x[4], x[5]))))
    t = padd(*(q[i][i] for i in range(3)))
    h = pdet3(q)
    s = padd(*(psub(pmul(q[i][i], q[j][j]), pmul(q[i][j], q[j][i]))
               for i in range(3) for j in range(i + 1, 3)))
    a = [psub(one, q[i][i]) for i in range(3)]
    lhs = padd(pmul(t, t), pscale(t, -3), pconst(3), pscale(h, -3))
    rhs = padd(*(pscale(pmul(psub(a[i], a[j]), psub(a[i], a[j])), F(1, 2))
                 for i in range(3) for j in range(i + 1, 3)),
               *(pscale(pmul(q[i][j], q[j][i]), 3)
                 for i in range(3) for j in range(i + 1, 3)))
    check(psub(lhs, rhs) == {}, "symbolic", "six-variable nonnegative certificate")
    check(psub(s, padd(t, h, pconst(-1))) == {}, "symbolic", "characteristic middle coefficient")
    check(padd(one, pscale(t, -1), s, pscale(h, -1)) == {},
          "symbolic", "characteristic polynomial vanishes at one")
    for row in q:
        check(psub(padd(*row), one) == {}, "symbolic", "symbolic row sum")
    eta = F(1, 36)
    endpoint = -2 + 64 * eta + 256 * eta * eta
    check(endpoint == F(-2, 81), "rational_gap", "strict contradiction endpoint")
    check(endpoint < 0, "rational_gap", "endpoint is negative")
    check(F(5, 2) * (1 - F(89, 90)) == eta,
          "rational_gap", "closed damping interval endpoint")
    check(3 + 3 - 1 == 5, "rational_gap", "six finite probes for d=3, M=3")
    return {"symbolic_variables": 6, "certificate_difference_monomials": len(psub(lhs, rhs)),
            "strict_contradiction_at_eta_1_over_36": str(endpoint)}


def recurrence_examples():
    # Enumerate a declared finite rational family, including reducible and
    # periodic matrices. These examples do not establish the universal gap.
    row_choices = ((F(1), F(0), F(0)), (F(0), F(1), F(0)),
                   (F(0), F(0), F(1)), (F(1, 3), F(1, 3), F(1, 3)))
    models = 0
    decoders = ((F(0), F(1, 2), F(1)), (F(1), F(1, 2), F(0)),
                (F(1, 3), F(1, 3), F(1, 3)))
    for q in itertools.product(row_choices, repeat=3):
        check(is_stochastic(q), "recurrence", "enumerated stochastic matrix")
        t = sum(q[i][i] for i in range(3))
        h = det3(q)
        s = t + h - 1
        aa = [1 - q[i][i] for i in range(3)]
        rhs = sum((F(1, 2) * (aa[i] - aa[j]) ** 2 + 3 * q[i][j] * q[j][i]
                   for i in range(3) for j in range(i + 1, 3)), F(0))
        check(t * t - 3 * t + 3 - 3 * h == rhs >= 0,
              "recurrence", "nonnegative identity at an exact rational matrix")
        check(0 <= t <= 3 and abs(h) <= 1 and abs(s) <= 3,
              "recurrence", "coefficient bounds")
        for d in decoders:
            models += 1
            y = outputs(q, d, 7)
            for n in range(4):
                check(y[n + 3] - t * y[n + 2] + s * y[n + 1] - h * y[n] == 0,
                      "recurrence", "Cayley-Hamilton scalar recurrence")
            target = (F(1), F(1, 2), F(0), F(1, 2), F(1))
            eta = max(abs(y[i] - target[i]) for i in range(5))
            check(abs(t - h) <= 16 * eta and abs(2 - t - h) <= 16 * eta,
                  "recurrence", "two perturbed recurrence bounds")
            check(abs(t - 1) <= 16 * eta and abs(h - 1) <= 16 * eta,
                  "recurrence", "coefficient extraction bounds")
            check(eta > F(1, 36), "recurrence", "sampled instance agrees with proved universal obstruction")
    return {"matrices": 64, "matrix_decoder_pairs": models,
            "decoder_initial_row": "e_1", "arithmetic": "Fraction"}


def background_model():
    lam = (F(1, 2), F(1, 3), F(1, 6))
    d = (F(0), F(1, 4), F(1))
    permutations = (perm((1, 0, 2)), perm((0, 2, 1)))
    q = []
    for p in permutations:
        first = (F(0),) + vm(lam, p)
        rows = tuple((F(0),) + row for row in p)
        q.append((first,) + rows)
    q = tuple(q)
    decoder = (dot(lam, d),) + d
    initial = (F(1), F(0), F(0), F(0))
    pi = (F(0), F(1, 3), F(1, 3), F(1, 3))
    j = (pi,) * 4
    bbar = dot(pi, decoder)
    orbit = [dot(vm(lam, perm(p)), d) for p in itertools.permutations(range(3))]
    c = max(abs(v - bbar) for v in orbit)
    check(bbar == sum(orbit) / 6 == F(5, 12), "background", "observable group average")
    check(c == F(1, 6), "background", "exact oscillation constant")
    check(mm(j, j) == j, "background", "rank-one reset is idempotent")
    check(dot(initial, decoder) == dot(lam, d), "background", "pure counted initializer decoder")
    alphas = (F(5, 6), F(7, 8))
    noisy = tuple(blend(q[a], j, alphas[a]) for a in range(2))
    for a in range(2):
        check(is_stochastic(q[a]) and is_stochastic(noisy[a]), "background", "common stochastic dimensions")
        check(vm(pi, q[a]) == pi, "background", "common stationary row")
        check(mm(q[a], j) == j == mm(j, q[a]), "background", "two-sided common reset identity")
    check(mm(q[0], q[1]) != mm(q[1], q[0]), "background", "commands really do not commute")
    words = 0
    for length in range(7):
        for word in itertools.product(range(2), repeat=length):
            words += 1
            ordinary = eye(4)
            damped = eye(4)
            beta = F(1)
            for a in word:
                ordinary = mm(ordinary, q[a])
                damped = mm(damped, noisy[a])
                beta *= alphas[a]
            check(damped == blend(ordinary, j, beta), "background_words", "matrix identity including initialization")
            b = dot(vm(initial, ordinary), decoder)
            bn = dot(vm(initial, damped), decoder)
            check(bn == beta * b + (1 - beta) * bbar,
                  "background_words", "exact terminal probability identity")
            epsilon = max(1 - a for a in alphas)
            check(0 <= 1 - beta <= length * epsilon,
                  "background_words", "wordwise product perturbation bound")
            check(abs(bn - b) <= length * epsilon * c,
                  "background_words", "finite-probe background bound")
    return {"labels": 4, "recurrent_labels": 3, "counted_initializer": 1,
            "command_count": 2, "tested_words": words, "maximum_word_length": 6,
            "command_damping": [str(a) for a in alphas], "background": str(bbar),
            "oscillation_constant": str(c)}


def period_four():
    p = perm((1, 2, 3, 0))
    pi = (F(1, 4),) * 4
    j = (pi,) * 4
    d = (F(1), F(1, 2), F(0), F(1, 2))
    cosines = (F(1), F(0), F(-1), F(0))
    alphas = (F(89, 90), F(99, 100), F(1000, 1001), F(1))
    for alpha in alphas:
        q = blend(p, j, alpha)
        check(is_stochastic(q), "period_four", "damped cycle stochasticity")
        y = outputs(q, d, 13)
        for n, value in enumerate(y):
            target = (1 + alpha ** n * cosines[n % 4]) / 2
            check(value == target, "period_four", "constructed exact response on declared finite probes")
            check(0 <= value <= 1, "period_four", "probability decoder validity")
        max_probe_error = max(abs(y[n] - (1 + cosines[n % 4]) / 2) for n in range(6))
        check(max_probe_error <= F(5, 2) * (1 - alpha) <= F(1, 36),
              "period_four", "certified six-probe perturbation range")
    return {"labels": 4, "checked_damping_parameters": [str(a) for a in alphas],
            "checked_sequence_length": 13, "theorem_interval": "89/90 <= alpha <= 1",
            "sharpness_claim": False}


def rank(rows):
    a = [list(row) for row in rows]
    if not a:
        return 0
    pivot = 0
    for col in range(len(a[0])):
        k = next((i for i in range(pivot, len(a)) if a[i][col]), None)
        if k is None:
            continue
        a[pivot], a[k] = a[k], a[pivot]
        factor = a[pivot][col]
        a[pivot] = [v / factor for v in a[pivot]]
        for i in range(len(a)):
            if i != pivot and a[i][col]:
                factor = a[i][col]
                a[i] = [v - factor * w for v, w in zip(a[i], a[pivot])]
        pivot += 1
        if pivot == len(a):
            break
    return pivot


def finite_span_probe():
    # One exact finite linear-space closure computation, independently of
    # word truncation. It validates a concrete controller's all-word equality.
    # Target is the period-four response in a three-coordinate representation.
    t = ((F(1), F(0), F(0)), (F(0), F(0), F(1)), (F(0), F(-1), F(0)))
    beta = (F(1), F(1), F(0))
    b = (F(1, 2), F(1, 2), F(0))
    q = perm((1, 2, 3, 0))
    dd = (F(1), F(1, 2), F(0), F(1, 2))
    s = tuple(tuple(t[i][j] if i < 3 and j < 3 else
                    q[i - 3][j - 3] if i >= 3 and j >= 3 else F(0)
                    for j in range(7)) for i in range(7))
    u = beta + (F(-1), F(0), F(0), F(0))
    v = b + dd
    basis = [u]
    frontier = [u]
    while frontier:
        row = vm(frontier.pop(), s)
        if rank(basis + [row]) > len(basis):
            basis.append(row)
            frontier.append(row)
    check(len(basis) <= 3 + 4, "finite_span", "combined dimension bound")
    for row in basis:
        check(dot(row, v) == 0, "finite_span", "decoder vanishes on a spanning row")
        check(rank(basis + [vm(row, s)]) == len(basis),
              "finite_span", "reachable span is invariant")
    yy = outputs(q, dd, 7)
    r = beta
    for n in range(7):
        check(dot(r, b) == yy[n], "finite_span", "d+M finite probes")
        r = vm(r, t)
    return {"supplied_dimension": 3, "controller_labels": 4,
            "combined_space_dimension": 7, "computed_reachable_rank": len(basis),
            "finite_test_maximum_length": 6,
            "scope": "exact closure for this explicit finite model only"}


def run():
    detail = {"symbolic_certificate": symbolic_certificate(),
              "recurrence_examples": recurrence_examples(),
              "noncommuting_background_model": background_model(),
              "period_four_realization": period_four(),
              "finite_linear_span": finite_span_probe()}
    return {"schema": "gtf-r73-finite-certificates-v1", "status": "passed",
            "arithmetic": "exact integers and fractions.Fraction",
            "total_checks": sum(COUNTS.values()), "exact_checks": sum(COUNTS.values()),
            "floating_probes": 0, "checks_by_group": dict(sorted(COUNTS.items())),
            "details": detail,
            "diagnostic_source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            "limits": ["Finite diagnostics do not replace the quantified mathematical proofs.",
                       "No general real quantifier-elimination computation was executed.",
                       "No proof-assistant, human-referee, or journal decision is claimed.",
                       "Explicit checks remain active under python -O."]}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    report = run()
    encoded = json.dumps(report, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(encoded, encoding="utf-8")
    print(encoded, end="")
