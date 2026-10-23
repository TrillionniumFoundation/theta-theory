#!/usr/bin/env python3
"""Exact finite diagnostics for R74 terminal-contrast memory theorems.

These checks test the displayed quotient controllers, explicit payoff witnesses,
the nonabelian coefficient-spanning calculation, and the counted initializer.
They do not search arbitrary stochastic realizations or prove continuum claims.
Every check runs unchanged under Python -O; no assert gates are used.
"""
from __future__ import annotations

import argparse
from collections import Counter
from fractions import Fraction as F
from itertools import permutations
import json
from pathlib import Path


COUNTS: dict[str, int] = {}
GROUP = "initialization"
CHARACTERS = (1, 2, 4, 8, 15)


def check(condition, message):
    if not condition:
        raise RuntimeError(f"{GROUP}: {message}")
    COUNTS[GROUP] = COUNTS.get(GROUP, 0) + 1


def chi(mask, g):
    return 1 if (mask & g).bit_count() % 2 == 0 else -1


def beta(t, g):
    return F(3, 8) + t * sum(chi(c, g) for c in CHARACTERS) / 8


def dot(a, b):
    return sum(x * y for x, y in zip(a, b))


def span(vectors):
    result = {0}
    for v in vectors:
        result |= {x ^ v for x in result}
    return frozenset(result)


def rank(rows):
    a = [list(map(F, r)) for r in rows]
    p = 0
    for col in range(len(a[0])):
        candidate = next((i for i in range(p, len(a)) if a[i][col]), None)
        if candidate is None:
            continue
        a[p], a[candidate] = a[candidate], a[p]
        pivot = a[p][col]
        a[p] = [v / pivot for v in a[p]]
        for i in range(len(a)):
            if i != p and a[i][col]:
                s = a[i][col]
                a[i] = [x - s * y for x, y in zip(a[i], a[p])]
        p += 1
        if p == len(a):
            break
    return p


def partitions(items):
    """All partitions into singleton and pair blocks, with no ordering copies."""
    if not items:
        yield ()
        return
    first, *rest = items
    for tail in partitions(rest):
        yield ((first,),) + tail
    for j, partner in enumerate(rest):
        remaining = rest[:j] + rest[j + 1:]
        for tail in partitions(remaining):
            yield ((first, partner),) + tail


def quotient_cosets(characters):
    h = {g for g in range(16) if all(chi(c, g) == 1 for c in characters)}
    remaining = set(range(16))
    cosets = []
    while remaining:
        g = min(remaining)
        q = frozenset(g ^ h0 for h0 in h)
        cosets.append(q)
        remaining -= q
    return h, cosets


def circuit_and_modes():
    global GROUP
    GROUP = "circuit_observability_and_fourier"
    for excluded in CHARACTERS:
        check(len(span(c for c in CHARACTERS if c != excluded)) == 16,
              "every four circuit characters are independent")
    check(span(CHARACTERS) == frozenset(range(16)), "faithful character span")
    check(Counter(beta(F(1), g) for g in range(16)) ==
          Counter({F(1): 1, F(1, 2): 10, F(0): 5}), "endpoint value multiplicities")
    rows = [[beta(F(1), g ^ h) for h in range(16)] for g in range(16)]
    check(rank(rows) == 6, "exact cyclic response rank")
    check(len({tuple(row) for row in rows}) == 16, "all residuals distinct")
    for t in (F(0), F(1, 5), F(3, 5), F(61, 100), F(4, 5), F(1)):
        values = [beta(t, g) for g in range(16)]
        check(all(0 <= value <= 1 for value in values), "probability validity")
        for mask in range(16):
            coefficient = sum(values[g] * chi(mask, g) for g in range(16)) / 16
            expected = F(3, 8) if mask == 0 else t / 8 if mask in CHARACTERS else F(0)
            check(coefficient == expected, "exact character coefficient")
    return {"group_order": 16, "dimension_for_positive_contrast": 6,
            "residual_count_for_positive_contrast": 16, "module_cover": 10}


def payoff_witnesses():
    global GROUP
    GROUP = "explicit_farkas_witnesses"
    ps = list(partitions(list(CHARACTERS)))
    check(len(ps) == 26, "all singleton/pair partitions")
    norms = {}
    expected_norm = {0: F(3, 2), 1: F(17, 8), 2: F(9, 4)}
    expected_multisets = {
        0: Counter({-4: 1, 0: 10, 4: 5}),
        1: Counter({-3: 1, -1: 6, 1: 4, 3: 2, 5: 3}),
        2: Counter({-2: 5, 0: 4, 2: 2, 4: 4, 6: 1}),
    }
    extra_mode_table = [beta(F(4, 5), g) + F(1, 36) * chi(3, g) for g in range(16)]
    check(all(0 <= v <= 1 for v in extra_mode_table), "extra-mode perturbation is a probability table")
    check(F(1, 36) < (5 * F(4, 5) - 3) / 18, "strict robust radius in displayed perturbation")
    for partition in ps:
        pairs = [block for block in partition if len(block) == 2]
        z = [1 - sum(chi(c, g) for c in CHARACTERS) +
             sum(chi(a ^ b, g) for a, b in pairs) for g in range(16)]
        check(Counter(z) == expected_multisets[len(pairs)], "displayed witness multiset")
        norm = F(sum(abs(v) for v in z), 16)
        check(norm == expected_norm[len(pairs)], "displayed exact witness norm")
        norms[len(pairs)] = str(norm)
        family_support = []
        for block in partition:
            h, cosets = quotient_cosets(block)
            for g in range(16):
                averaged = sum(F(z[g ^ h0]) for h0 in h) / len(h)
                expected = 1 - chi(block[0], g)
                if len(block) == 2:
                    expected *= 1 - chi(block[1], g)
                check(averaged == expected and averaged >= 0,
                      "coset-average Farkas coefficient is exactly nonnegative")
            # First-outcome payoff is -z/16; the other outcome payoff is zero.
            support = sum(max(-F(sum(z[g] for g in q), 16), F(0)) for q in cosets)
            check(support == 0, "exact quotient support-function value")
            family_support.append(support)
        check(max(family_support) == 0, "full-family support-function value")
        check(F(sum(z), 16) == 1, "fixed-orbit average remains positive")
        for t in (F(1, 5), F(3, 5), F(61, 100), F(4, 5), F(1)):
            score = -sum(F(z[g], 16) * beta(t, g) for g in range(16))
            check(score == (5 * t - 3) / 8, "exact strict-margin polynomial")
        perturbed_score = -sum(F(z[g], 16) * extra_mode_table[g] for g in range(16))
        check(perturbed_score > 0, "all displayed families excluded after extra-mode perturbation")
    return {"partition_witnesses": len(ps), "average_absolute_norms": norms,
            "exact_threshold": "3/5", "strict_margin": "(5*t-3)/8",
            "robust_sufficient_radius": "(5*t-3)/18",
            "additional_mode_example": {"contrast": "4/5", "coefficient_at_mask_3": "1/36"}}


def build_core(blocks, weights, terminal_rules, t):
    labels = []
    for i, block in enumerate(blocks):
        for bits in range(1 << len(block)):
            labels.append((i, bits))
    index = {label: j for j, label in enumerate(labels)}
    actions = {}
    for g in range(16):
        targets = []
        for i, bits in labels:
            flip = sum((chi(c, g) < 0) << j for j, c in enumerate(blocks[i]))
            targets.append(index[(i, bits ^ flip)])
        actions[g] = tuple(targets)
    lam = tuple(weights[i] if bits == 0 else F(0) for i, bits in labels)
    decoder = tuple(terminal_rules[i](bits, t) for i, bits in labels)
    return labels, actions, lam, decoder


def validate_core(core, t, expected_size):
    labels, action, lam, decoder = core
    k = len(labels)
    check(k == expected_size, "expected core cardinality")
    check(sum(lam) == 1 and all(v >= 0 for v in lam), "core preparation probability")
    check(all(0 <= v <= 1 for v in decoder), "bounded two-outcome decoder")
    for g in range(16):
        actual = sum(lam[i] * decoder[action[g][i]] for i in range(k))
        check(actual == beta(t, g), "all sixteen exact core response values")
    # Construct the fully charged pure-start machine. The first command acts
    # while the initializer leaves; it is not lost or supplied for free.
    for generator in (1, 2, 4, 8):
        first_row = [F(0)] * (k + 1)
        for i in range(k):
            first_row[action[generator][i]] += lam[i]
        check(sum(first_row) == 1 and first_row[-1] == 0,
              "initializer exits into the counted recurrent core")
        for suffix in range(16):
            actual = sum(first_row[i] * decoder[action[suffix][i]] for i in range(k))
            check(actual == beta(t, generator ^ suffix),
                  "first command and every suffix group element are applied")
    check(dot(lam, decoder) == beta(t, 0), "initializer empty-word decoder")


def quotient_controllers():
    global GROUP
    GROUP = "exact_quotient_controllers_and_initializer"
    low_blocks = tuple((c,) for c in CHARACTERS)
    low_rules = tuple((lambda bits, t: F(3, 8) + (5 * t / 8) * (1 if bits == 0 else -1))
                      for _ in CHARACTERS)
    high_blocks = ((1, 2), (4, 8, 15))
    high_rules = (
        lambda bits, t: (1 - t) * F(3, 8) + t * int(bits == 0),
        lambda bits, t: (1 - t) * F(3, 8) + t * int(bits.bit_count() <= 1),
    )
    for blocks, weights, rules, sample in (
        (low_blocks, (F(1, 5),) * 5, low_rules, F(3, 5)),
        (high_blocks, (F(1, 2),) * 2, high_rules, F(1)),
    ):
        _, action, _, _ = build_core(blocks, weights, rules, sample)
        for g in range(16):
            for h in range(16):
                check(tuple(action[h][action[g][i]] for i in range(len(action[0]))) == action[g ^ h],
                      "exact group multiplication in the common core action")
    for t in (F(0), F(1, 5), F(3, 5)):
        validate_core(build_core(low_blocks, (F(1, 5),) * 5, low_rules, t), t, 10)
    for t in (F(0), F(3, 5), F(61, 100), F(4, 5), F(1)):
        validate_core(build_core(high_blocks, (F(1, 2),) * 2, high_rules, t), t, 12)
    outside = build_core(low_blocks, (F(1, 5),) * 5, low_rules, F(61, 100))[3]
    check(min(outside) < 0, "ten-point displayed decoder detects its exact threshold")
    return {"low_core_size": 10, "high_core_size": 12,
            "charged_pure_start_sizes": [11, 13], "same_action_for_all_commands": True}


def row_perm(row, permutation):
    out = [F(0)] * len(row)
    for i, j in enumerate(permutation):
        out[j] = row[i]
    return tuple(out)


def permutation_sign(p):
    inversions = sum(p[i] > p[j] for i in range(len(p)) for j in range(i + 1, len(p)))
    return 1 if inversions % 2 == 0 else -1


def s3_coefficient_and_controllers():
    global GROUP
    GROUP = "s3_coefficient_injectivity_and_threshold"
    ps = list(permutations(range(3)))
    u, v = (F(1), F(-1), F(0)), (F(1), F(1), F(-2))
    selected = [(0, 1, 2), (1, 0, 2), (0, 2, 1), (1, 2, 0)]
    expected = [((F(1), F(0)), (F(0), F(1))),
                ((F(-1), F(0)), (F(0), F(1))),
                ((F(1, 2), F(1, 2)), (F(3, 2), F(-1, 2))),
                ((F(-1, 2), F(1, 2)), (F(-3, 2), F(-1, 2)))]
    actual_matrices = []
    for p, expected_matrix in zip(selected, expected):
        matrix = []
        for vector in (u, v):
            changed = row_perm(vector, p)
            # coordinates in the orthogonal (but unnormalized) row basis u,v
            coordinates = (dot(changed, u) / dot(u, u), dot(changed, v) / dot(v, v))
            check(tuple(coordinates[0] * u[i] + coordinates[1] * v[i] for i in range(3)) == changed,
                  "standard-plane coordinate reconstruction")
            matrix.append(coordinates)
        matrix = tuple(matrix)
        check(matrix == expected_matrix, "four explicitly displayed standard matrices")
        actual_matrices.append(tuple(x for row in matrix for x in row))
    check(rank(actual_matrices) == 4, "standard matrices span every two-by-two endomorphism")
    for i in range(3):
        for j in range(3):
            check(sum(permutation_sign(p) * int(p[i] == j) for p in ps) == 0,
                  "natural representation has no sign matrix coefficient")
    lam = (F(2, 3), F(0), F(1, 3))
    for t in (F(0), F(1, 5), F(1, 2), F(2, 3)):
        decoder = tuple(F(1, 2) + 3 * t * value / 4 for value in u)
        check(all(0 <= x <= 1 for x in decoder), "three-state decoder valid through two-thirds")
        for p in ps:
            actual = dot(row_perm(lam, p), decoder)
            target = F(1, 2) + t * dot(row_perm(u, p), u) / 4
            check(actual == target, "every exact S3 response under contrast")
    outside = tuple(F(1, 2) + 3 * F(67, 100) * value / 4 for value in u)
    check(min(outside) < 0 and max(outside) > 1, "displayed S3 decoder threshold failure")
    # An actual nonnormal-stabilizer orbit fails the absorption used in the
    # Dedekind theorem, so the condition cannot be silently omitted.
    mixed = (F(1, 2), F(1, 3), F(1, 6))
    decode = (F(0), F(1, 4), F(1))
    h = (1, 0, 2)  # fixes point 2, the selected coset-origin in this orbit
    check(dot(mixed, decode) != dot(row_perm(mixed, h), decode),
          "nonnormal point stabilizer prevents quotient absorption")
    return {"coefficient_span_rank": 4, "exact_threshold": "2/3",
            "positive_core_sizes": [3, 6], "pure_start_sizes": [4, 6],
            "nonnormal_absorption_negative_control": True}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    models = {
        "circuit": circuit_and_modes(),
        "payoff_certificates": payoff_witnesses(),
        "quotient_controllers": quotient_controllers(),
        "s3": s3_coefficient_and_controllers(),
    }
    total = sum(COUNTS.values())
    result = {"schema": "general-theta.r74.contrast-diagnostics.v1", "status": "PASS",
              "arithmetic": ["Q"], "exact_checks": total, "floating_checks": 0,
              "total_checks": total, "groups": COUNTS, "models": models,
              "limits": [
                  "Finite exact identities for the specified group tables, controllers and witnesses.",
                  "Universal lower bounds and contrast intervals rely on the written proofs.",
                  "These checks do not enumerate arbitrary stochastic realizations.",
                  "No general linear-program or quantifier-elimination solve was executed.",
                  "No proof assistant, independent human referee approval or editorial decision."]}
    text = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(text)
    print(text, end="")


if __name__ == "__main__":
    main()
