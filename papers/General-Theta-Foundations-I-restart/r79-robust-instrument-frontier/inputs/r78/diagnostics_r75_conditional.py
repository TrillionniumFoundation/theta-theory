#!/usr/bin/env python3
"""Finite exact checks for the R75 conditional-memory author research.

These check stated rational examples and finite identities. They do not
establish the quantified theorems, infinite-horizon limits, novelty,
independent human approval, or correctness in a proof assistant.
All checks remain active under Python -O.
"""
from __future__ import annotations

import argparse
from fractions import Fraction as F
import hashlib
from itertools import product
import json
from pathlib import Path

COUNTS: dict[str, int] = {}


def check(condition, group, description):
    if not condition:
        raise RuntimeError(f"{group}: {description}")
    COUNTS[group] = COUNTS.get(group, 0) + 1


def mat(rows):
    return tuple(tuple(F(x) for x in row) for row in rows)


def vm(v, m):
    return tuple(sum(v[i] * m[i][j] for i in range(len(v)))
                 for j in range(len(m[0])))


def mm(a, b):
    return tuple(vm(row, b) for row in a)


def add(*ms):
    return tuple(tuple(sum(m[i][j] for m in ms)
                       for j in range(len(ms[0][0])))
                 for i in range(len(ms[0])))


def dot(a, b):
    return sum(x * y for x, y in zip(a, b))


def scalar(s, x):
    return tuple(s * t for t in x)


def vector_add(*xs):
    return tuple(sum(t) for t in zip(*xs))


def words(alphabet, max_length):
    for n in range(max_length + 1):
        yield from product(alphabet, repeat=n)


def matrix_word(initial, transitions, w):
    row = initial
    for a in w:
        row = vm(row, transitions[a])
    return row


def determinant3(m):
    a, b, c = m
    return (a[0] * (b[1] * c[2] - b[2] * c[1])
            - a[1] * (b[0] * c[2] - b[2] * c[0])
            + a[2] * (b[0] * c[1] - b[1] * c[0]))


def initialization_checks():
    group = "controlled_stationary_elimination"
    mu = (F(1, 2), F(1, 2))
    aggregate = mat([[F(3, 4), F(1, 4)], [F(1, 4), F(3, 4)]])
    q00 = mat([[F(3, 8), F(1, 8)], [F(1, 8), F(1, 8)]])
    q10 = mat([[F(1, 8), F(1, 8)], [F(1, 8), F(3, 8)]])
    target = {}
    extended = {}
    for command, q0 in enumerate((q00, q10)):
        q1 = mat([[aggregate[i][j] - q0[i][j] for j in range(2)]
                  for i in range(2)])
        gamma = F(1, 8) if command == 0 else F(1, 16)
        for report, q in enumerate((q0, q1)):
            key = (command, report)
            target[key] = q
            # Label zero is the pure initializer.  Redirect a positive
            # gamma portion from each row into it; its future response
            # is mu times the two original future responses.
            core_rows = tuple((gamma,) + tuple(q[i][j] - gamma * mu[j]
                                              for j in range(2))
                              for i in range(2))
            mixed_row = vm(mu, q)
            initial_row = ((gamma,) + tuple(mixed_row[j] - gamma * mu[j]
                                            for j in range(2)))
            extended[key] = (initial_row,) + core_rows
            check(all(t >= 0 for row in extended[key] for t in row),
                  group, "nonnegative recurrent initializer table")
        tsum = add(extended[(command, 0)], extended[(command, 1)])
        check(all(sum(row) == 1 for row in tsum), group, "row normalization")
        check(vm(mu, aggregate) == mu, group, "stationary target mixture")
    nu = (F(1, 3), F(2, 3))
    average = tuple(tuple(sum(nu[a] * (extended[(a, 0)][i][j]
                                       + extended[(a, 1)][i][j])
                                  for a in range(2))
                          for j in range(3)) for i in range(3))
    check(average[0][0] == F(1, 6), group, "strict positive self return")
    beta = tuple(average[0][j] / (1 - average[0][0]) for j in (1, 2))
    check(beta == mu, group, "predictive stationary elimination weights")
    for key, t in extended.items():
        eliminated = tuple(tuple(t[i][j] + t[i][0] * beta[j - 1]
                                 for j in (1, 2)) for i in (1, 2))
        check(eliminated == target[key], group, "elimination restores core")
    decoder = (F(1, 5), F(4, 5))
    extended_decoder = (dot(mu, decoder),) + decoder
    for w in words(tuple(target), 4):
        row = matrix_word(mu, target, w)
        erow = matrix_word((F(1), F(0), F(0)), extended, w)
        check(sum(row) == sum(erow), group, "all finite joint report laws")
        check(dot(row, decoder) == dot(erow, extended_decoder),
              group, "all finite terminal readout laws")
    p0 = sum(vm(mu, q00))
    p00 = sum(vm(vm(mu, q00), q00))
    check(p00 != p0 * p0, group, "non-memoryless exception is excluded")


def physical_branch(alpha, angle, report, state):
    # (t, x, y) represents X=(t I+x sigma_z+y sigma_x)/2.
    t, x, y = state
    c, s = angle
    p0 = (t / 8, alpha * (c * x - s * y) / 8,
          alpha * (s * x + c * y) / 8)
    h = (2 * t + x) / 16
    p1 = (h, h, F(0))
    if report == 0:
        return p0
    if report == 1:
        return p1
    return (t - p0[0] - h, -p0[1] - h, -p0[2])


def physical_word(alpha, angle, w):
    state = (F(1), F(0), F(0))
    for report in w:
        state = physical_branch(alpha, angle, report, state)
    return state


def zero_damping_checks():
    group = "zero_damping_two_state_endpoint"
    mu = (F(3, 14), F(11, 14))
    dictionary = ((F(1), F(1), F(0)), (F(1), F(-3, 11), F(0)))
    transitions = {
        0: mat([[F(3, 112), F(11, 112)], [F(3, 112), F(11, 112)]]),
        1: mat([[F(3, 16), 0], [F(19, 176), 0]]),
        2: mat([[0, F(11, 16)], [F(7, 88), F(121, 176)]]),
    }
    tsum = add(*transitions.values())
    check(tsum == (mu, mu), group, "rank-one aggregate stochastic matrix")
    check(vm(mu, dictionary) == (1, 0, 0), group, "initial density identity")
    angle = (F(3, 5), F(4, 5))
    for report, t in transitions.items():
        for i, state in enumerate(dictionary):
            check(vm(t[i], dictionary) == physical_branch(F(0), angle, report, state),
                  group, "branch intertwining")
    for w in words((0, 1, 2), 5):
        classical = vm(matrix_word(mu, transitions, w), dictionary)
        check(classical == physical_word(F(0), angle, w),
              group, "finite complete quantum word states")
    cylinder = [physical_word(F(0), angle, (1,) + (0,) * n + (1,))[0]
                for n in range(3)]
    check(cylinder[0] * cylinder[2] - cylinder[1] ** 2 == F(1, 2**19),
          group, "rank-two Hankel minor")


SQUARE = ((F(1), F(1), F(0)), (F(1), F(0), F(1)),
          (F(1), F(-1), F(0)), (F(1), F(0), F(-1)))


def square_weights(state):
    t, x, y = state
    spare = t - abs(x) - abs(y)
    if spare < 0:
        raise RuntimeError("point outside the rational square")
    return (max(x, 0) + spare / 4, max(y, 0) + spare / 4,
            max(-x, 0) + spare / 4, max(-y, 0) + spare / 4)


def polygon_checks():
    group = "complete_noisy_instrument_polygon"
    angles = ((F(3, 5), F(4, 5)), (F(3, 5), F(-4, 5)),
              (F(-5, 13), F(12, 13)))
    for angle in angles:
        check(sum(t * t for t in angle) == 1, group, "rational rotation")
    for alpha, selected in ((F(5, 7), angles[:1]), (F(1, 2), angles)):
        tables = {}
        for command, angle in enumerate(selected):
            for report in range(3):
                rows = tuple(square_weights(physical_branch(alpha, angle, report, state))
                             for state in SQUARE)
                tables[(command, report)] = rows
                for i, state in enumerate(SQUARE):
                    check(vm(rows[i], SQUARE) == physical_branch(alpha, angle, report, state),
                          group, "exact all-branch state intertwining")
                    check(all(t >= 0 for t in rows[i]), group, "branch nonnegativity")
            tsum = add(*(tables[(command, report)] for report in range(3)))
            check(all(sum(row) == 1 for row in tsum), group, "command stochasticity")
        mu = (F(1, 4),) * 4
        for w in words(tuple(tables), 3):
            state = (F(1), F(0), F(0))
            for command, report in w:
                state = physical_branch(alpha, selected[command], report, state)
            row = matrix_word(mu, tables, w)
            check(vm(row, SQUARE) == state, group, "common multi-command word states")
        if alpha == F(5, 7):
            check(alpha * (F(3, 5) + F(4, 5)) == 1,
                  group, "exact four-state sector boundary")
            cycle = mat([[0, 1, 0, 0], [0, 0, 1, 0],
                         [0, 0, 0, 1], [1, 0, 0, 0]])
            expected = mat([[(F(3, 7) * (i == j) + F(4, 7) * cycle[i][j]) / 8
                             for j in range(4)] for i in range(4)])
            check(tables[(0, 0)] == expected, group, "boundary lazy directed cycle")
            cylinder = [physical_word(alpha, angles[0], (1,) + (0,) * n + (1,))[0]
                        for n in range(5)]
            minor = tuple(tuple(cylinder[i + j] for j in range(3)) for i in range(3))
            check(determinant3(minor) != 0, group, "rank-three Hankel minor")


def stopped_tree(alpha, horizon, randomized):
    angles = ((F(3, 5), F(4, 5)), (F(-5, 13), F(12, 13)))
    leaves = {}

    def recurse(word, state):
        if len(word) == horizon or (word and word[-1][1] == 1):
            # Terminal sigma_z POVM, recording its result too.
            leaves[word + (("terminal", 0),)] = (state[0] + state[1]) / 2
            leaves[word + (("terminal", 1),)] = (state[0] - state[1]) / 2
            return
        if randomized:
            choices = ((0, F(1, 3)), (1, F(2, 3)))
        else:
            command = 0 if not word or word[-1][1] == 0 else 1
            choices = ((command, F(1)),)
        for command, probability in choices:
            for report in range(3):
                next_state = physical_branch(alpha, angles[command], report,
                                             scalar(probability, state))
                recurse(word + ((command, report),), next_state)

    recurse((), (F(1), F(0), F(0)))
    return leaves


def approximation_checks():
    group = "stopped_law_perturbation"
    epsilon = F(1, 7)
    angle = (F(3, 5), F(4, 5))
    for state in SQUARE + ((F(1), F(3, 5), F(4, 5)),):
        delta0 = vector_add(physical_branch(1 - epsilon, angle, 0, state),
                            scalar(-1, physical_branch(F(1), angle, 0, state)))
        delta2 = vector_add(physical_branch(1 - epsilon, angle, 2, state),
                            scalar(-1, physical_branch(F(1), angle, 2, state)))
        check(delta0[0] == 0 and delta2 == scalar(-1, delta0),
              group, "opposite trace-zero changed branches")
        check(delta0[1] ** 2 + delta0[2] ** 2 == (epsilon / 8) ** 2,
              group, "sharp pure-qubit one-call trace-distance square")
    for randomized, horizons in ((False, range(1, 6)), (True, range(1, 4))):
        for horizon in horizons:
            target = stopped_tree(F(1), horizon, randomized)
            approximate = stopped_tree(1 - epsilon, horizon, randomized)
            check(set(target) == set(approximate), group, "same finite stopped sample space")
            check(sum(target.values()) == sum(approximate.values()) == 1,
                  group, "complete stopped record probability")
            tv = sum(abs(target[w] - approximate[w]) for w in target) / 2
            cost = sum((len(w) - 1) * p for w, p in target.items())
            check(tv <= epsilon * cost / 8,
                  group, "target-cost total variation with terminal measurement")
            check(cost <= horizon, group, "target capped cost")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    initialization_checks()
    zero_damping_checks()
    polygon_checks()
    approximation_checks()
    report = {
        "status": "passed",
        "arithmetic": "exact fractions; no floating-point probes",
        "checks": sum(COUNTS.values()),
        "total_checks": sum(COUNTS.values()),
        "exact_checks": sum(COUNTS.values()),
        "floating_checks": 0,
        "groups": COUNTS,
        "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "scope": "Finite rational examples and identities only; not a proof assistant, novelty clearance, human referee report, or editorial decision.",
    }
    rendered = json.dumps(report, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(rendered)
    print(rendered, end="")


if __name__ == "__main__":
    main()
