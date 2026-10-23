#!/usr/bin/env python3
"""Exact finite diagnostics for the R73 reversible-memory normal form.

These checks concern explicitly specified finite models and identities.
They do not constitute a proof assistant, human referee assessment, or an
exhaustive search through arbitrary stochastic realizations.  All checks
execute under both ordinary Python and python -O; no assert is used.
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass
from fractions import Fraction as F
from itertools import permutations, product
from math import factorial, lcm
import json
from pathlib import Path


COUNTS: dict[str, int] = {}
GROUP = "initialization"


def check(condition, message):
    if not condition:
        raise RuntimeError(f"{GROUP}: {message}")
    COUNTS[GROUP] = COUNTS.get(GROUP, 0) + 1


def matrix(rows):
    return tuple(tuple(F(x) for x in row) for row in rows)


def eye(n):
    return matrix([[int(i == j) for j in range(n)] for i in range(n)])


def mm(a, b):
    return tuple(tuple(sum(a[i][k] * b[k][j] for k in range(len(b)))
                       for j in range(len(b[0]))) for i in range(len(a)))


def vm(v, a):
    return tuple(sum(v[k] * a[k][j] for k in range(len(v)))
                 for j in range(len(a[0])))


def dot(v, w):
    return sum(x * y for x, y in zip(v, w))


def scaled_sum(terms):
    return tuple(tuple(sum(s * a[i][j] for s, a in terms)
                       for j in range(len(terms[0][1][0])))
                 for i in range(len(terms[0][1])))


def permutation_matrix(p):
    return matrix([[int(p[i] == j) for j in range(len(p))]
                   for i in range(len(p))])


def compose(p, q):
    """Chronological row action: first p, then q."""
    return tuple(q[p[i]] for i in range(len(p)))


def inverse(p):
    q = [0] * len(p)
    for i, j in enumerate(p):
        q[j] = i
    return tuple(q)


def row_rank(rows):
    if not rows:
        return 0
    a = [list(map(F, row)) for row in rows]
    pivot = 0
    for column in range(len(a[0])):
        selected = next((i for i in range(pivot, len(a))
                         if a[i][column]), None)
        if selected is None:
            continue
        a[pivot], a[selected] = a[selected], a[pivot]
        divisor = a[pivot][column]
        a[pivot] = [x / divisor for x in a[pivot]]
        for i in range(len(a)):
            if i != pivot and a[i][column]:
                factor = a[i][column]
                a[i] = [x - factor * y for x, y in zip(a[i], a[pivot])]
        pivot += 1
        if pivot == len(a):
            break
    return pivot


def independent_rows(rows):
    basis = []
    for row in rows:
        if row_rank(basis + [row]) > len(basis):
            basis.append(row)
    return basis


def blockdiag(a, b):
    return tuple(tuple(row) + (F(0),) * len(b) for row in a) + tuple(
        (F(0),) * len(a) + tuple(row) for row in b)


def is_stochastic(a):
    return all(sum(row) == 1 and all(x >= 0 for x in row) for row in a)


def initializer(perms, lam):
    k = len(lam)
    result = []
    for p in perms:
        pm = permutation_matrix(p)
        result.append(((F(0),) + vm(lam, pm),) + tuple(
            (F(0),) + row for row in pm))
    return tuple(result)


def all_words(alphabet, maximum):
    for length in range(maximum + 1):
        yield from product(range(alphabet), repeat=length)


def exact_equivalence(a, da, b, db):
    """Close the combined reachable row space, then check the output map."""
    matrices = tuple(blockdiag(x, y) for x, y in zip(a, b))
    initial = (F(1),) + (F(0),) * (len(da) - 1) + (F(-1),) + (
        F(0),) * (len(db) - 1)
    output = tuple(da) + tuple(db)
    basis = [initial]
    position = 0
    while position < len(basis):
        row = basis[position]
        check(dot(row, output) == 0, "output vanishes on reachable basis")
        for q in matrices:
            image = vm(row, q)
            if row_rank(basis + [image]) > len(basis):
                basis.append(image)
        position += 1
    for row in basis:
        for q in matrices:
            check(row_rank(basis + [vm(row, q)]) == len(basis),
                  "closed reachable span")
    check(len(basis) <= len(output), "finite closure dimension")
    return len(basis)


def hidden_model():
    global GROUP
    GROUP = "hidden_seven_label_projection"
    s = (1, 0, 2)
    t = (0, 2, 1)
    generators = (s, t)
    lam = (F(1, 2), F(1, 3), F(1, 6))
    dec = (F(0), F(1, 4), F(1))
    a = matrix([[F(1, 3), F(2, 3)], [F(3, 4), F(1, 4)]])
    b = matrix([[F(2, 5), F(3, 5)], [F(1, 7), F(6, 7)]])
    internals = (a, b)
    initial_internal = ((F(2, 7), F(5, 7)), (F(3, 8), F(5, 8)))
    hidden = []
    for p, internal, eta in zip(generators, internals, initial_internal):
        moved = vm(lam, permutation_matrix(p))
        rows = [(F(0),) + tuple(moved[i] * eta[j]
                                for i in range(3) for j in range(2))]
        for i in range(3):
            for j in range(2):
                rows.append((F(0),) + tuple(
                    internal[j][h] if z == p[i] else F(0)
                    for z in range(3) for h in range(2)))
        hidden.append(tuple(rows))
    hidden = tuple(hidden)
    for q in hidden:
        check(is_stochastic(q), "hidden transition is stochastic")
    loops = tuple(mm(q, q) for q in hidden)
    lazy = scaled_sum([(F(1, 3), eye(7))] + [(F(1, 3), q) for q in loops])
    k = scaled_sum([(F(1, 3), eye(2)), (F(1, 3), mm(a, a)),
                    (F(1, 3), mm(b, b))])
    mass0 = k[1][0] / (k[0][1] + k[1][0])
    mu = (mass0, 1 - mass0)
    check(vm(mu, k) == mu, "stationary conditional law")
    e_rows = [(F(0),) + tuple(lam[i] * mu[j]
                             for i in range(3) for j in range(2))]
    for i in range(3):
        for _ in range(2):
            e_rows.append((F(0),) + tuple(mu[h] if z == i else F(0)
                                         for z in range(3) for h in range(2)))
    e = tuple(e_rows)
    check(is_stochastic(e), "projection is stochastic")
    check(mm(e, e) == e, "projection idempotence")
    check(mm(lazy, e) == e and mm(e, lazy) == e, "lazy projection identities")
    check(row_rank(e) == 3, "three independent recurrent vertices")
    for loop in loops:
        check(mm(mm(e, loop), e) == e, "identity-word sandwich")
    check(any(mm(e, loop) != e for loop in loops),
          "negative control: no common unsandwiched stationarity")
    fs = tuple(mm(mm(e, q), e) for q in hidden)
    for f in fs:
        check(mm(f, f) == e, "sandwiched involution inverse")
    check(mm(mm(mm(fs[0], fs[1]), mm(fs[0], fs[1])),
             mm(fs[0], fs[1])) == e, "sandwiched product has order three")
    check(mm(fs[0], fs[1]) != mm(fs[1], fs[0]), "faithful nonabelian action")
    check(any(mm(e, q) != mm(q, e) for q in hidden),
          "negative control: original commands need not commute with E")
    normal = initializer(generators, lam)
    dh = (dot(lam, dec),) + tuple(dec[i] for i in range(3) for _ in range(2))
    dn = (dot(lam, dec),) + dec
    for q in normal:
        check(is_stochastic(q), "normal-form transition is stochastic")
    closure_dimension = exact_equivalence(hidden, dh, normal, dn)
    for word in all_words(2, 7):
        rh = (F(1),) + (F(0),) * 6
        rn = (F(1),) + (F(0),) * 3
        group = tuple(range(3))
        for letter in word:
            rh, rn = vm(rh, hidden[letter]), vm(rn, normal[letter])
            group = compose(group, generators[letter])
        target = dot(vm(lam, permutation_matrix(group)), dec)
        check(dot(rh, dh) == target and dot(rn, dn) == target,
              "all prefixes through length seven")
    check(dot(lam, dec) != dot(vm(lam, permutation_matrix(s)), dec),
          "negative control: forgetting the first command changes its answer")
    return {"original_labels": 7, "recurrent_classes": 3,
            "normal_form_labels": 4,
            "stationary_internal_row": [str(x) for x in mu],
            "combined_equivalence_span_dimension": closure_dimension,
            "explicit_prefixes": 255,
            "equivalence_scope": "all words for these two specified finite machines"}


def symmetric_families():
    global GROUP
    GROUP = "symmetric_group_families"
    result = []
    for k in (3, 4, 5):
        group = tuple(permutations(range(k)))
        lam = tuple(F(i + 1, k * (k + 1) // 2) for i in range(k))
        dec = tuple(F(i, k - 1) for i in range(k))
        rows = [vm(lam, permutation_matrix(g)) for g in group]
        tests = [vm(dec, permutation_matrix(g)) for g in group]
        check(len(set(rows)) == factorial(k), "distinct preparation orbit")
        check(row_rank(rows) == k, "reachable orbit rank")
        check(row_rank(tests) == k, "future decoder orbit rank")
        basis = independent_rows(tests)
        signatures = [tuple(dot(row, test) for test in basis) for row in rows]
        check(len(set(signatures)) == factorial(k), "all residuals distinguished")
        for row in rows:
            value = dot(row, dec)
            check(sum(row) == 1 and 0 <= value <= 1,
                  "probability-valid value for every group element")
        cycle = tuple(range(1, k)) + (0,)
        transposition = (1, 0) + tuple(range(2, k))
        generated = {tuple(range(k))}
        frontier = list(generated)
        for g in frontier:
            for command in (cycle, transposition):
                h = compose(g, command)
                if h not in generated:
                    generated.add(h)
                    frontier.append(h)
        check(len(generated) == factorial(k), "two commands generate full group")
        result.append({"dimension": k, "group_order": factorial(k),
                       "residuals": factorial(k), "probability_core": k,
                       "stochastic_memory_by_proved_formula": k + 1})
    k = 3
    group = tuple(permutations(range(k)))
    lam = (F(1, 2), F(1, 3), F(1, 6))
    dec = (F(0), F(1, 4), F(1))
    values = {dot(vm(lam, permutation_matrix(g)), dec) for g in group}
    expected = {F(1, 4), F(3, 8), F(7, 24), F(13, 24), F(11, 24), F(7, 12)}
    check(values == expected, "six stated rational response values")
    coarse = (F(0), F(0), F(1))
    first = {dot(vm(lam, permutation_matrix(g)), coarse) for g in group}
    signatures = {tuple(dot(vm(vm(lam, permutation_matrix(g)),
                              permutation_matrix(h)), coarse) for h in group)
                  for g in group}
    check(len(first) == 3 and len(signatures) == 6,
          "decoder cardinality differs from residual cardinality")
    for degenerate_lam, degenerate_dec, expected_orbit, expected_rank in (
            ((F(1), F(0), F(0)), dec, 3, 3),
            ((F(1, 2), F(1, 4), F(1, 4)), dec, 3, 3),
            ((F(1, 3),) * 3, dec, 1, 1),
            (lam, (F(1, 2),) * 3, 1, 1)):
        signatures = []
        for g in group:
            row = vm(degenerate_lam, permutation_matrix(g))
            signature = tuple(dot(vm(row, permutation_matrix(h)), degenerate_dec)
                              for h in group)
            signatures.append(signature + tuple(1 - x for x in signature))
        check(len(set(signatures)) == expected_orbit, "degenerate residual count")
        check(row_rank(signatures) == expected_rank, "degenerate response rank")
    return result


@dataclass(frozen=True)
class Quadratic:
    """The exact real quadratic field Q(sqrt(3))."""
    a: F = F(0)
    b: F = F(0)

    @staticmethod
    def coerce(value):
        return value if isinstance(value, Quadratic) else Quadratic(F(value))

    def __add__(self, other):
        other = self.coerce(other)
        return Quadratic(self.a + other.a, self.b + other.b)

    __radd__ = __add__

    def __neg__(self):
        return Quadratic(-self.a, -self.b)

    def __sub__(self, other):
        return self + (-self.coerce(other))

    def __rsub__(self, other):
        return self.coerce(other) - self

    def __mul__(self, other):
        other = self.coerce(other)
        return Quadratic(self.a * other.a + 3 * self.b * other.b,
                         self.a * other.b + self.b * other.a)

    __rmul__ = __mul__


def decoder_obstruction():
    global GROUP
    GROUP = "bounded_decoder_endpoint_certificate"
    group = tuple(permutations(range(3)))
    identity = (0, 1, 2)
    s = (1, 0, 2)
    t = (0, 2, 1)
    r = compose(s, t)
    r2 = compose(r, r)
    u = (F(1), F(-1), F(0))

    def beta(g):
        return F(1, 2) + F(1, 4) * dot(vm(u, permutation_matrix(g)), u)

    check(beta(identity) == 1 and beta(s) == 0, "endpoint values")
    check(beta(r) == F(1, 4) and beta(r2) == F(1, 4), "rotation values")
    transpositions = [g for g in group if g != identity and compose(g, g) == identity]
    check(all(beta(g) == F(3, 4) for g in transpositions if g != s),
          "remaining transposition values")
    signatures = [tuple(beta(compose(g, h)) for h in group) for g in group]
    check(len(set(signatures)) == 6 and row_rank(signatures) == 3,
          "endpoint response rank and residual cardinality")
    # Orbit types on <=5 points are fixed, sign, and one natural orbit.
    # The endpoint reduction is proved in the manuscript.  Here the only
    # surviving symbolic candidate is checked for each moved start point.
    for start in (0, 1):
        visits = (r[start], r2[start])
        check(s[start] in visits, "one even image has forced-zero decoder")
        check(F(0) != F(1, 4), "natural plus fixed orbits cannot fit even values")
        mass_sign = F(1, 4)
        mass_natural = 1 - mass_sign
        natural_decoder = tuple(F(int(i == start)) for i in range(3))
        mismatches = []
        for g in group:
            even = g in (identity, r, r2)
            candidate = mass_natural * natural_decoder[g[start]] + (
                mass_sign if even else 0)
            if candidate != beta(g):
                mismatches.append(g)
        check(any(g in transpositions and g != s for g in mismatches),
              "unique endpoint-compatible natural-plus-sign candidate fails")
    GROUP = "qubit_quadratic_field_realization"
    zero, one = Quadratic(), Quadratic(F(1))
    q0 = ((one, zero), (zero, -one))
    q1 = ((Quadratic(F(1, 2)), Quadratic(F(0), F(1, 2))),
          (Quadratic(F(0), F(1, 2)), Quadratic(F(-1, 2))))
    i2 = ((one, zero), (zero, one))
    check(mm(q0, q0) == i2 and mm(q1, q1) == i2, "two unitary involutions")
    unitary_product = mm(q0, q1)
    check(mm(mm(unitary_product, unitary_product), unitary_product)
          == ((-one, zero), (zero, -one)),
          "negative control: physical phase survives before observable quotient")
    for word in all_words(2, 7):
        physical = i2
        g = identity
        # Density evolution applies U_new on the left of the accumulated U.
        for letter in word:
            physical = mm((q0, q1)[letter], physical)
            g = compose(g, (s, t)[letter])
        amplitude = sum(sum(row) for row in physical) * F(1, 2)
        probability = amplitude * amplitude
        check(probability == Quadratic(beta(g)),
              "Born probability equals S3 response for every tested word")
    return {"group": "S3", "dimension": 3, "residuals": 6,
            "permutation_module_minimum": 3,
            "probability_core_by_endpoint_proof": 6,
            "stochastic_memory_by_proved_formula": 6,
            "endpoint_orbit_budget_excluded": [3, 4, 5],
            "physical_field": "Q(sqrt(3))", "physical_words_checked": 255}


def partitions(items):
    if not items:
        yield ()
        return
    first, rest = items[0], items[1:]
    for part in partitions(rest):
        yield ((first,),) + part
        for i in range(len(part)):
            yield part[:i] + ((first,) + part[i],) + part[i + 1:]


def cyclic_specialization():
    global GROUP
    GROUP = "cyclic_partition_specialization"
    results = []
    for orders, expected_core, expected_memory in (
            ((3, 5), 8, 9), ((3, 4), 7, 8), ((3, 6), 6, 6),
            ((5, 5), 5, 5), ((3, 5, 7), 15, 16), ((4, 6, 10), 20, 21)):
        possibilities = list(partitions(tuple(range(len(orders)))))
        core_costs = [sum(lcm(*(orders[j] for j in block)) for block in part)
                      for part in possibilities]
        old_costs = [cost + int(len(part) >= 2)
                    for cost, part in zip(core_costs, possibilities)]
        core = min(core_costs)
        formula = min(lcm(*orders), 1 + core)
        check(core == expected_core, "stated cyclic core count")
        check(formula == min(old_costs) == expected_memory,
              "normal-form formula equals retained partition-plus-start law")
        results.append({"orders": list(orders), "core": core,
                        "pure_start_memory": formula})
    return results


def run():
    hidden = hidden_model()
    symmetric = symmetric_families()
    obstruction = decoder_obstruction()
    cyclic = cyclic_specialization()
    total = sum(COUNTS.values())
    return {"schema": "general-theta.r73.normal-form-diagnostics.v1",
            "status": "PASS", "arithmetic": ["Q", "Q(sqrt(3))"],
            "exact_checks": total, "floating_checks": 0,
            "total_checks": total, "groups": COUNTS,
            "hidden_projection": hidden, "symmetric_families": symmetric,
            "bounded_decoder_obstruction": obstruction,
            "cyclic_specializations": cyclic,
            "limits": [
                "Finite exact diagnostics of specified identities and models.",
                "The all-word comparison closes a concrete finite linear span.",
                "General normal-form and minimality claims rely on written proofs.",
                "No quantifier elimination over arbitrary realizations was executed.",
                "No proof assistant, human referee approval, or editorial decision."]}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    report = json.dumps(run(), indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(report)
    print(report, end="")


if __name__ == "__main__":
    main()
