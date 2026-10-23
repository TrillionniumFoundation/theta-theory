#!/usr/bin/env python3
"""Exact finite diagnostic for the R74 adaptive instrument construction.

Two state-dependent qubit instruments have noncommuting unconditioned
channels. Their branchwise depolarization is eta=3/4. Six physical Pauli
states form an octahedral core and a known distinct pure preparation is
the seventh, counted initial label. Exact Bloch coordinates encode full
Hermitian operators, including imaginary off-diagonal entries.

Checks cover finite operator identities and two bounded adaptive policies.
They do not replace the universal proof or constitute a proof assistant.
All checks remain active with python -O.
"""
from __future__ import annotations

import argparse
from fractions import Fraction as F
import hashlib
from itertools import combinations, permutations, product
import json
from pathlib import Path

COUNTS = {}
ETA = F(3, 4)
AXES = ((F(0), F(0), F(1)), (F(3, 5), F(0), F(4, 5)))
CORE = ((F(1), F(0), F(0)), (F(-1), F(0), F(0)),
        (F(0), F(1), F(0)), (F(0), F(-1), F(0)),
        (F(0), F(0), F(1)), (F(0), F(0), F(-1)))
INITIAL = (F(0), F(3, 5), F(4, 5))
STATES = tuple((F(1),) + r for r in CORE + (INITIAL,))


def check(ok, group, message):
    if not ok:
        raise RuntimeError(f"{group}: {message}")
    COUNTS[group] = COUNTS.get(group, 0) + 1


def matrix(rows):
    return tuple(tuple(F(x) for x in row) for row in rows)


def eye(n):
    return matrix([[int(i == j) for j in range(n)] for i in range(n)])


def dot(a, b):
    return sum(x * y for x, y in zip(a, b))


def mm(a, b):
    return tuple(tuple(sum(a[i][k] * b[k][j] for k in range(len(b)))
                       for j in range(len(b[0]))) for i in range(len(a)))


def mv(a, x):
    return tuple(dot(row, x) for row in a)


def vm(x, a):
    return tuple(sum(x[i] * a[i][j] for i in range(len(x)))
                 for j in range(len(a[0])))


def transpose(a):
    return tuple(zip(*a))


def scale(t, x):
    return tuple(t * v for v in x)


def combine(terms):
    return tuple(tuple(sum(t * a[i][j] for t, a in terms)
                       for j in range(len(terms[0][1][0])))
                 for i in range(len(terms[0][1])))


def tensor(a, b):
    return tuple(tuple(a[i // len(b)][j // len(b[0])] * b[i % len(b)][j % len(b[0])]
                       for j in range(len(a[0]) * len(b[0])))
                 for i in range(len(a) * len(b)))


def det(a):
    n = len(a)
    total = F(0)
    for p in permutations(range(n)):
        inversions = sum(p[i] > p[j] for i in range(n) for j in range(i + 1, n))
        value = F((-1) ** inversions)
        for i in range(n):
            value *= a[i][p[i]]
        total += value
    return total


def psd_principal_minors(a, group):
    check(a == transpose(a), group, "Hermitian matrix")
    for k in range(1, len(a) + 1):
        for idx in combinations(range(len(a)), k):
            minor = tuple(tuple(a[i][j] for j in idx) for i in idx)
            check(det(minor) >= 0, group, f"nonnegative principal minor {idx}")


def real_density(r):
    if r[1] != 0:
        raise RuntimeError("This helper is for real-plane Choi factors only")
    x, _, z = r
    return matrix([[(1 + z) / 2, x / 2], [x / 2, (1 - z) / 2]])


def branch_linear(a, y):
    sign = F(1 if y == 0 else -1)
    n = AXES[a]
    effect = (F(1, 2),) + tuple(sign * x / 2 for x in n)
    posterior = (F(1),) + tuple((1 - ETA) * sign * x for x in n)
    return matrix([[x * e for e in effect] for x in posterior])


def octahedral_weights(r):
    # An exact constructive convex decomposition for ||r||_1<=1.
    remainder = 1 - sum(abs(x) for x in r)
    if remainder < 0:
        raise RuntimeError("Target outside the octahedron")
    weights = [remainder / 6] * 6
    for j, x in enumerate(r):
        weights[2 * j + int(x < 0)] += abs(x)
    return tuple(weights)


def construct_and_check():
    for r in CORE + (INITIAL,):
        check(dot(r, r) == 1, "physical_dictionary", "every retained state is pure")
    check(INITIAL not in CORE, "physical_dictionary", "initializer is a distinct counted label")
    check(3 * (1 - ETA) ** 2 <= 1, "physical_dictionary",
          "Cauchy-Schwarz puts the entire posterior ball in the octahedron")
    maps = [[branch_linear(a, y) for y in range(2)] for a in range(2)]
    channels = [combine([(1, m) for m in row]) for row in maps]
    check(mm(channels[0], channels[1]) != mm(channels[1], channels[0]),
          "physical_instruments", "unconditioned channels do not commute")
    check(mm(maps[0][0], maps[1][0]) != mm(maps[1][0], maps[0][0]),
          "physical_instruments", "observed branch maps do not commute")
    for a in range(2):
        total_choi = []
        for y in range(2):
            sign = F(1 if y == 0 else -1)
            projector = real_density(tuple(sign * x for x in AXES[a]))
            posterior = real_density(tuple((1 - ETA) * sign * x for x in AXES[a]))
            check(mm(projector, projector) == projector, "physical_instruments",
                  "input branch is a genuine rank-one projective measurement")
            choi = tensor(transpose(projector), posterior)
            psd_principal_minors(choi, "physical_instruments")
            residual = combine([(1, choi), (-ETA / 2, tensor(transpose(projector), eye(2)))])
            check(residual == combine([(1 - ETA, tensor(transpose(projector), projector))]),
                  "physical_instruments", "exact CP branchwise posterior-noise certificate")
            psd_principal_minors(residual, "physical_instruments")
            total_choi.append(choi)
        total_choi = combine([(1, j) for j in total_choi])
        partial = matrix([[sum(total_choi[2 * i + k][2 * j + k] for k in range(2))
                           for j in range(2)] for i in range(2)])
        check(partial == eye(2), "physical_instruments", "instrument sum is trace preserving")

    tables = []
    zero_rows = 0
    for a in range(2):
        pair = []
        for y in range(2):
            rows = []
            for state in STATES:
                target = mv(maps[a][y], state)
                probability = target[0]
                if probability == 0:
                    row = (F(0),) * 7
                    zero_rows += 1
                    check(target == (F(0),) * 4, "operator_intertwining",
                          "zero-probability branch has zero positive operator")
                else:
                    posterior = tuple(v / probability for v in target[1:])
                    weights = octahedral_weights(posterior)
                    row = scale(probability, weights) + (F(0),)
                check(min(row) >= 0, "operator_intertwining", "nonnegative outcome row")
                check(vm(row, STATES) == target, "operator_intertwining",
                      "all four operator coordinates intertwine exactly")
                check(row[6] == 0, "operator_intertwining", "no return to counted initializer")
                rows.append(row)
            pair.append(matrix(rows))
        for i in range(7):
            check(sum(sum(t[i]) for t in pair) == 1, "operator_intertwining",
                  "outcomes and retained labels have total probability one")
        probabilities = [sum(pair[0][i]) for i in range(7)]
        check(len(set(probabilities)) > 1, "operator_intertwining",
              "outcome law genuinely depends on input state")
        tables.append(pair)
    check(zero_rows > 0, "operator_intertwining", "zero-probability branch handling was exercised")

    initial_row = tuple(F(i == 6) for i in range(7))
    for depth in range(5):
        for word in product(tuple(product(range(2), repeat=2)), repeat=depth):
            quantum, classical = STATES[6], initial_row
            for a, y in word:
                quantum = mv(maps[a][y], quantum)
                classical = vm(classical, tables[a][y])
            check(vm(classical, STATES) == quantum, "finite_history_operators",
                  "full subnormalized state on each bounded command-outcome history")
    return maps, tables, {"hilbert_dimension": 2, "commands": 2, "outcomes_per_command": 2,
                         "eta": "3/4", "core_labels": 6, "counted_pure_initializer": 1,
                         "total_live_labels": 7, "zero_outcome_rows": zero_rows,
                         "maximum_checked_history_length": 4,
                         "unconditioned_channels_noncommuting": True}


def terminal_axis(history):
    return ((F(0), F(1), F(0)), AXES[0], AXES[1])[len(history) % 3]


def terminal_probability(vector, history, c):
    sign = F(1 if c == 0 else -1)
    return (vector[0] + sign * dot(terminal_axis(history), vector[1:])) / 2


def policy(mode, history):
    n = len(history)
    if mode == "deterministic_feedback":
        stop = F(n == 4 or (n > 0 and history[-1][1] == 1))
        next_command = 0 if n == 0 or history[-1][1] == 1 else 1
        commands = (F(next_command == 0), F(next_command == 1))
        return stop, commands
    if mode == "randomized_feedback":
        stop = F(1) if n == 3 else F(1, 5) if n == 0 else F(1, 2) if history[-1][1] else F(1, 4)
        p1 = F(1, 3) if sum(y for _, y in history) % 2 == 0 else F(2, 3)
        return stop, (1 - p1, p1)
    raise RuntimeError("Unknown finite policy")


def adaptive_checks(maps, tables):
    results = []
    for mode in ("deterministic_feedback", "randomized_feedback"):
        totals = {"quantum_mass": F(0), "classical_mass": F(0),
                  "quantum_score": F(0), "classical_score": F(0),
                  "quantum_cost": F(0), "classical_cost": F(0)}
        leaves = 0
        stopped_histories = 0
        initial = tuple(F(i == 6) for i in range(7))

        def visit(history, quantum, classical):
            nonlocal leaves, stopped_histories
            stop, commands = policy(mode, history)
            check(0 <= stop <= 1 and min(commands) >= 0 and sum(commands) == 1,
                  "adaptive_policy", "visible-history policy probabilities are legal")
            if stop:
                stopped_histories += 1
                cost = F(sum(1 + a for a, _ in history))
                base_score = F(3 * len(history) + sum((i + 1) * (a + 2 * y)
                                                     for i, (a, y) in enumerate(history)))
                for c in range(2):
                    qmass = stop * terminal_probability(quantum, history, c)
                    decoder = tuple(terminal_probability(v, history, c) for v in STATES)
                    cmass = stop * dot(classical, decoder)
                    check(qmass == cmass and qmass >= 0, "adaptive_stopped_law",
                          "stopped cylinder and history-selected terminal POVM agree")
                    score = base_score + F(2 * c - 1, 7)
                    totals["quantum_mass"] += qmass
                    totals["classical_mass"] += cmass
                    totals["quantum_score"] += qmass * score
                    totals["classical_score"] += cmass * score
                    totals["quantum_cost"] += qmass * cost
                    totals["classical_cost"] += cmass * cost
                    leaves += 1
            if stop == 1:
                return
            for a, pcommand in enumerate(commands):
                if pcommand == 0:
                    continue
                weight = (1 - stop) * pcommand
                for y in range(2):
                    visit(history + ((a, y),), scale(weight, mv(maps[a][y], quantum)),
                          scale(weight, vm(classical, tables[a][y])))

        visit((), STATES[6], initial)
        check(totals["quantum_mass"] == totals["classical_mass"] == 1,
              "adaptive_totals", "bounded stopped law has total mass one")
        check(totals["quantum_score"] == totals["classical_score"],
              "adaptive_totals", "bounded terminal/history score expectation agrees")
        check(totals["quantum_cost"] == totals["classical_cost"],
              "adaptive_totals", "nonnegative call-cost expectation agrees")
        results.append({"policy": mode, "stopped_histories": stopped_histories,
                        "terminal_leaves": leaves,
                        "exact_expected_score": str(totals["quantum_score"]),
                        "exact_expected_cost": str(totals["quantum_cost"]),
                        "scope": "one specified bounded visible-history policy; not a test of all policies"})
    return results


def run():
    maps, tables, construction = construct_and_check()
    policies = adaptive_checks(maps, tables)
    total = sum(COUNTS.values())
    return {"schema": "gtf-r74-instrument-diagnostics-v1", "status": "passed",
            "arithmetic": "exact integers and fractions.Fraction in full Hermitian Bloch coordinates",
            "total_checks": total, "exact_checks": total, "floating_probes": 0,
            "checks_by_group": dict(sorted(COUNTS.items())),
            "details": {"construction": construction, "adaptive_policies": policies},
            "diagnostic_source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            "limits": ["Finite operator and policy identities do not replace the universal theorem proofs.",
                       "This does not prove minimality of the seven-label example or an unrestricted noise lower bound.",
                       "No proof-assistant verification, human referee approval, or editorial judgment is claimed.",
                       "All checks remain active under python -O."]}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    encoded = json.dumps(run(), indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(encoded, encoding="utf-8")
    print(encoded, end="")
