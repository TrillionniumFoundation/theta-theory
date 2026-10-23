#!/usr/bin/env python3
"""Finite exact diagnostics for R76 return geometry and rare excursions.

Rational and Q(sqrt(3)) arithmetic only. These calculations test finite
instances and identities; they are not a proof of the quantified theorems,
an infinite-horizon verification, a novelty certification, or human review.
All checks remain active with Python -O.
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass
from fractions import Fraction as F
from itertools import product
import json
from math import comb
from math import isqrt
from pathlib import Path

COUNTS = {}


def check(condition, group, description):
    if not condition:
        raise RuntimeError(f"{group}: {description}")
    COUNTS[group] = COUNTS.get(group, 0) + 1


@dataclass(frozen=True)
class Q3:
    a: F = F(0)
    b: F = F(0)

    def __post_init__(self):
        object.__setattr__(self, "a", F(self.a))
        object.__setattr__(self, "b", F(self.b))

    @staticmethod
    def coerce(x):
        return x if isinstance(x, Q3) else Q3(F(x))

    def __add__(self, other):
        other = Q3.coerce(other)
        return Q3(self.a + other.a, self.b + other.b)

    __radd__ = __add__

    def __neg__(self):
        return Q3(-self.a, -self.b)

    def __sub__(self, other):
        return self + (-Q3.coerce(other))

    def __rsub__(self, other):
        return Q3.coerce(other) + (-self)

    def __mul__(self, other):
        other = Q3.coerce(other)
        return Q3(self.a * other.a + 3 * self.b * other.b,
                  self.a * other.b + self.b * other.a)

    __rmul__ = __mul__

    def __truediv__(self, other):
        other = Q3.coerce(other)
        denominator = other.a * other.a - 3 * other.b * other.b
        if not denominator:
            raise ZeroDivisionError
        return self * Q3(other.a / denominator, -other.b / denominator)

    def nonnegative(self):
        if self.a >= 0 and self.b >= 0:
            return True
        if self.a < 0 and self.b <= 0:
            return False
        if self.a >= 0:
            return self.a * self.a >= 3 * self.b * self.b
        return 3 * self.b * self.b >= self.a * self.a


ZERO, ONE = Q3(), Q3(1)
SEEDS = ((Q3(1), ZERO), (Q3(F(-1, 2)), Q3(0, F(1, 2))),
         (Q3(F(-1, 2)), Q3(0, F(-1, 2))))


def rotate(v, phase):
    c, s = phase
    return (c * v[0] - s * v[1], s * v[0] + c * v[1])


def indices(a, length):
    return tuple(m for m in product(range(length), repeat=a) if sum(m) < length)


def dot(v, w):
    return sum((x * y for x, y in zip(v, w)), ZERO)


def target_step(state, phase, report):
    t, x, y = state
    rx, ry = rotate((x, y), phase)
    z = (t / 8, rx / 8, ry / 8)
    h = t / 8 + x / 16
    if report == 0:
        return z
    if report == 1:
        return (h, h, ZERO)
    return (t - z[0] - h, -z[1] - h, -z[2])


def make_tables(phases, length):
    a = len(phases)
    keys = tuple((j, m) for m in indices(a, length) for j in range(3))
    index = {key: i for i, key in enumerate(keys)}
    zero = (0,) * a
    states = []
    for j, m in keys:
        v = SEEDS[j]
        for phase, exponent in zip(phases, m):
            for _ in range(exponent):
                v = rotate(v, phase)
        states.append(v)
    transitions = {}
    for ai, phase in enumerate(phases):
        for report in range(3):
            rows = []
            for (j, m), v in zip(keys, states):
                row = [ZERO] * len(keys)
                h = Q3(F(1, 8)) + v[0] / 16
                p2 = Q3(F(7, 8)) - h
                rv = rotate(v, phase)
                u2 = (-rv[0] / 8 - h, -rv[1] / 8)
                if report == 0:
                    if sum(m) < length - 1:
                        nxt = list(m)
                        nxt[ai] += 1
                        row[index[j, tuple(nxt)]] = Q3(F(1, 8))
                    else:
                        for seed in range(3):
                            row[index[seed, zero]] = Q3(F(1, 24))
                elif report == 1:
                    row[index[0, zero]] = h
                else:
                    for seed, sv in enumerate(SEEDS):
                        row[index[seed, zero]] = (p2 + 2 * dot(sv, u2)) / 3
                rows.append(tuple(row))
            transitions[ai, report] = tuple(rows)
    initial = tuple(Q3(F(1, 3)) if m == zero else ZERO for j, m in keys)
    return keys, tuple(states), transitions, initial


def vm(v, mat):
    return tuple(sum((v[i] * mat[i][j] for i in range(len(v))), ZERO)
                 for j in range(len(mat[0])))


def represented(row, states):
    return (sum(row, ZERO),
            sum((q * v[0] for q, v in zip(row, states)), ZERO),
            sum((q * v[1] for q, v in zip(row, states)), ZERO))


def potential_checks():
    group = "sharp_excursion_potential"
    for r in (F(1, 8), F(1, 3), F(2, 3), F(7, 8)):
        for length in range(1, 13):
            u = tuple((r ** (-k) - 1) / (1 - r) for k in range(length + 1))
            check(u[0] == 0, group, "zero initial potential")
            for k in range(length):
                check(r * u[k + 1] - u[k] == 1, group, "exact constant-rate drift")
                for p in (F(0), r / 7, r / 2, r):
                    check(p * u[k + 1] - u[k] <= 1, group, "controlled rate upper drift")
            attempt_cost = sum(r ** k for k in range(length))
            check(attempt_cost / r ** length == u[-1], group, "renewal waiting expectation")
            for fraction in (F(0), F(1, 13), F(1, 2), F(1)):
                budget = fraction * u[-1]
                check((1-r) * budget / (r ** (-length) - 1) == fraction,
                      group, "randomized waiting attains budget line")
    r = F(1, 8)
    for length in range(1, 25):
        check((1-r) / (r ** (-length) - 1) == F(7, 8 * (8**length - 1)),
              group, "qubit constant including off-by-one")


def finite_stopping_checks():
    group = "finite_stopping_budget"
    # Exact enumeration of all binary report words, for a family of
    # history-dependent hazards and stop rules; no asymptotic extrapolation.
    for r in (F(1, 8), F(1, 2), F(3, 4)):
        for length in range(1, 5):
            for horizon in (2, 4, 7):
                for mode in range(4):
                    frontier = [((), F(1), 0)]
                    expected_cost, hit = F(0), F(0)
                    for t in range(horizon):
                        nxt = []
                        for word, weight, age in frontier:
                            if mode == 1 and word and word[-1] == 0:
                                continue
                            if mode == 2 and t >= 2 and sum(word) % 2 == 0:
                                continue
                            expected_cost += weight
                            p = r if mode != 3 else r / (1 + (sum(word) % 3))
                            q1 = weight * p
                            if age + 1 == length:
                                hit += q1
                            else:
                                nxt.append((word + (1,), q1, age + 1))
                            nxt.append((word + (0,), weight * (1-p), 0))
                        frontier = nxt
                    check(hit <= (1-r) * expected_cost / (r**(-length) - 1),
                          group, "adaptive finite-horizon run probability")


def geometry_checks():
    group = "exact_triangle_and_return_rows"
    check(tuple(sum((v[k] for v in SEEDS), ZERO) for k in range(2)) == (ZERO, ZERO),
          group, "seed barycenter")
    for j in range(2):
        for k in range(2):
            check(sum((v[j] * v[k] for v in SEEDS), ZERO) ==
                  Q3(F(3, 2) if j == k else F(0)), group, "seed second moment")
    phases = ((F(3, 5), F(4, 5)), (F(5, 13), F(12, 13)))
    for c, s in phases:
        check(c*c+s*s == 1, group, "rational unit-circle phase")
    for a, length in ((1, 1), (1, 2), (1, 4), (2, 1), (2, 2), (2, 3)):
        keys, states, transitions, mu = make_tables(phases[:a], length)
        check(len(keys) == 3 * comb(length+a-1, a), group, "commuting dictionary cardinality")
        check(represented(mu, states) == (ONE, ZERO, ZERO), group, "initial quantum state")
        for v in states:
            check(dot(v, v) == ONE, group, "all dictionary states physical and pure")
        for ai in range(a):
            for i, (j, m) in enumerate(keys):
                all_rows = tuple(transitions[ai, s][i] for s in range(3))
                check(sum((sum(row, ZERO) for row in all_rows), ZERO) == ONE,
                      group, "complete stochastic row")
                for s, row in enumerate(all_rows):
                    check(all(q.nonnegative() for q in row), group, "entrywise algebraic positivity")
                    actual = represented(row, states)
                    target = target_step((ONE,) + states[i], phases[ai], s)
                    check(actual[0] == target[0], group, "every branch probability exact")
                    if s != 0 or sum(m) < length - 1:
                        check(actual == target, group, "nonoverflow subnormalized state identity")
                    if s == 2:
                        for ii, (jj, mm) in enumerate(keys):
                            if sum(mm) == 0:
                                check((row[ii] - F(1, 48)).nonnegative(), group,
                                      "uniform return entry lower bound")
                check(sum(all_rows[0], ZERO) == Q3(F(1, 8)), group, "constant rare probability")


def history_checks():
    group = "complete_history_and_terminal_identity"
    phases = ((F(3, 5), F(4, 5)), (F(5, 13), F(12, 13)))
    # Two controls chosen from the visible record. All three reports are
    # enumerated; a non-axis terminal effect is checked through its state.
    length = 3
    keys, states, transitions, mu = make_tables(phases, length)
    for mode in range(2):
        frontier = [((), mu, (ONE, ZERO, ZERO), 0, False)]
        for n in range(6):
            nxt = []
            for word, row, target, age, hit in frontier:
                represented_state = represented(row, states)
                if not hit:
                    check(represented_state == target, group, "every no-overflow history exact")
                    effect = (represented_state[0] + F(3, 5)*represented_state[1]
                              + F(4, 5)*represented_state[2]) / 2
                    target_effect = (target[0] + F(3, 5)*target[1] + F(4, 5)*target[2]) / 2
                    check(effect == target_effect, group, "nonaxis terminal POVM exact")
                if n == 5:
                    continue
                ai = (sum(word) + len(word)) % 2 if mode else 0
                for report in range(3):
                    new_age = age + 1 if report == 0 else 0
                    nxt.append((word + (report,), vm(row, transitions[ai, report]),
                                target_step(target, phases[ai], report), new_age,
                                hit or new_age >= length))
            frontier = nxt
    # An explicit positive discrepancy confirms this is an approximation,
    # not an accidental assertion of exact finite realization.
    row, target = mu, (ONE, ZERO, ZERO)
    for report in (1, 0, 0, 0):
        row = vm(row, transitions[0, report])
        target = target_step(target, phases[0], report)
    check(represented(row, states) != target, group, "overflow genuinely changes a terminal state")


def physical_dictionary_checks():
    group = "physical_dictionary_packing_and_orbits"
    # Q(sqrt(5)) pairs for the quadratic-irrational witness; signs use
    # integer/rational squares, not floating-point approximations.
    def add(u, v):
        return (u[0] + v[0], u[1] + v[1])

    def neg(u):
        return (-u[0], -u[1])

    def mul(u, v):
        return (u[0]*v[0] + 5*u[1]*v[1], u[0]*v[1] + u[1]*v[0])

    def scale(s, u):
        return (s*u[0], s*u[1])

    def positive(u):
        x, y = u
        if x >= 0 and y >= 0:
            return x > 0 or y > 0
        if x <= 0 and y <= 0:
            return False
        if x >= 0:
            return x*x > 5*y*y
        return 5*y*y > x*x

    omega = (F(-1, 2), F(1, 2))
    conjugate = (omega[0], -omega[1])
    check(mul(omega, conjugate) == (F(-1), F(0)), group, "quadratic norm")
    scale_int = 10**30
    root_floor = isqrt(5*scale_int**2)
    lower = F(root_floor-scale_int, 2*scale_int)
    upper = lower + F(1, 2*scale_int)
    for q in range(1, 65):
        p_lower = (q*lower + F(1, 2)).numerator // (q*lower + F(1, 2)).denominator
        p_upper = (q*upper + F(1, 2)).numerator // (q*upper + F(1, 2)).denominator
        check(p_lower == p_upper, group, "certified finite nearest integer")
        p = p_lower
        error = add(scale(q, omega), (F(-p), F(0)))
        error_conj = add(scale(q, conjugate), (F(-p), F(0)))
        norm = p*p + p*q - q*q
        check(norm != 0 and mul(error, error_conj) == (F(norm), F(0)),
              group, "integer norm excludes zero")
        if not positive(error):
            error = neg(error)
        check(positive(add(error, (F(-1, 3*q), F(0)))), group,
              "finite golden separation certificate")
    angles = ((F(0), F(0)), add(scale(2, omega), (F(-1), F(0))),
              add(scale(4, omega), (F(-2), F(0))), omega,
              add(scale(3, omega), (F(-1), F(0))), (F(1), F(0)))
    for left, right in zip(angles, angles[1:]):
        gap = add(right, neg(left))
        check(positive(gap), group, "golden orbit circular ordering")
        check(positive(add((F(1, 4), F(0)), neg(gap))), group,
              "golden orbit gaps below quarter circle")
    check(F(1, 2) > F(25, 121), group, "golden seed disk margin")
    for budget in (F(1, 100), F(1), F(10)):
        zeta = min(F(1), F(7, 8)*budget)
        for length in (2, 3, 5, 10, 20, 40):
            pmin = zeta / 8**length
            delta = pmin / (1 + 9*length*length)
            infidelity = delta / (pmin - delta)
            check(infidelity == F(1, 9*length*length), group,
                  "joint-event conditioning threshold exact")
            check(F(4, 3*(length-1)) > F(4, 3*length), group,
                  "strict packing separation for distinct prefixes")
            check(F(1, 2)+delta < 1-infidelity, group,
                  "pure initializer cannot cover a pure prefix")
            for n in (0, length-1):
                cost = zeta * (1-F(1, 8)**(n+1)) / (1-F(1, 8))
                check(cost <= budget, group, "early abort policy target cost")
    # The original rational rotation has a seven-point rational seed
    # polygon. Check its ordered edge halfplanes and squared inradii.
    c, s = F(3, 5), F(4, 5)
    orbit = [(F(1), F(0))]
    for _ in range(6):
        x, y = orbit[-1]
        orbit.append((c*x-s*y, s*x+c*y))
    for u, v in zip(orbit, orbit[1:] + orbit[:1]):
        determinant = u[0]*v[1]-u[1]*v[0]
        edge_square = (v[0]-u[0])**2 + (v[1]-u[1])**2
        check(determinant > 0, group, "rational polygon origin strictly inside")
        check(determinant**2 > F(25, 121)*edge_square, group,
              "rational polygon contains return disk")
    check(4*c**3-3*c == F(-117, 125), group, "closing edge triple-angle exact value")
    for seeds in (5, 7):
        for depth in (1, 2, 5, 10, 20):
            exponent_set = {j+n for j in range(seeds) for n in range(depth)}
            check(len(exponent_set) == seeds+depth-1, group,
                  "single-orbit union count removes seed multiplier")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    potential_checks()
    finite_stopping_checks()
    geometry_checks()
    history_checks()
    physical_dictionary_checks()
    count = sum(COUNTS.values())
    report = {"status": "PASS", "total_checks": count, "exact_checks": count,
              "floating_checks": 0, "groups": COUNTS,
              "arithmetic": "fractions.Fraction and exact Q(sqrt(3)), Q(sqrt(5))",
              "scope": "finite diagnostics only; no formal proof or independent expert assessment"}
    text = json.dumps(report, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(text)
    print(text, end="")


if __name__ == "__main__":
    main()
