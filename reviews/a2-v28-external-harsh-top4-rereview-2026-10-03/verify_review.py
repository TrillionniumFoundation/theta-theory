#!/usr/bin/env python3
"""Independent finite diagnostics for the A2 v28 referee report.

The script imports no author module.  It checks finite periodic motifs,
two-sided patch recognition, noisy comparison constants, bounded-denominator
lattice arithmetic, the repeated-disk symmetry jump, cutoff inequalities,
and the displayed smoothing exponents.  It is not a proof certificate,
a TeX build, or a physical sensor execution.
"""
from __future__ import annotations

from collections import Counter
from fractions import Fraction as F
from itertools import combinations, product
from math import gcd, lcm, sqrt
import json
import random

COUNTS: Counter[str] = Counter()


def check(group: str, condition: bool, detail: str = "") -> None:
    if not condition:
        raise RuntimeError(f"{group}: {detail}")
    COUNTS[group] += 1


def det(u: tuple[int, int], v: tuple[int, int]) -> int:
    return u[0] * v[1] - u[1] * v[0]


def periodic_patch(
    motif: frozenset[tuple[int, int, int]], a: int, b: int, radius: int = 3
) -> frozenset[tuple[int, int, int]]:
    return frozenset(
        (x + a * i, y + b * j, colour)
        for x, y, colour in motif
        for i in range(-radius, radius + 1)
        for j in range(-radius, radius + 1)
    )


def global_period(
    motif: frozenset[tuple[int, int, int]],
    a: int,
    b: int,
    shift: tuple[int, int],
) -> bool:
    u, v = shift
    shifted = frozenset(((x + u) % a, (y + v) % b, c) for x, y, c in motif)
    return shifted == motif


def local_two_sided_period(
    motif: frozenset[tuple[int, int, int]],
    patch: frozenset[tuple[int, int, int]],
    shift: tuple[int, int],
) -> bool:
    u, v = shift
    return all(
        (x + sign * u, y + sign * v, c) in patch
        for x, y, c in motif
        for sign in (-1, 1)
    )


def gcd_of_minors(vectors: list[tuple[int, int]]) -> int:
    value = 0
    for u, v in combinations(vectors, 2):
        value = gcd(value, abs(det(u, v)))
    return value


def orbit_count(
    motif: frozenset[tuple[int, int, int]],
    a: int,
    b: int,
    periods: list[tuple[int, int]],
) -> int:
    unseen = set(motif)
    count = 0
    while unseen:
        x, y, colour = min(unseen)
        orbit = {((x + u) % a, (y + v) % b, colour) for u, v in periods}
        check("period_action_preserves_motif", orbit <= set(motif))
        unseen -= orbit
        count += 1
    return count


def check_motif(
    motif: frozenset[tuple[int, int, int]], a: int, b: int, prefix: str
) -> None:
    patch = periodic_patch(motif, a, b)
    root = min(motif)
    candidates = {(x - root[0], y - root[1]) for x, y, _ in motif}
    candidates.update({(a, 0), (-a, 0), (0, b), (0, -b)})
    accepted: list[tuple[int, int]] = []
    for shift in candidates:
        local = local_two_sided_period(motif, patch, shift)
        global_ = global_period(motif, a, b, shift)
        check(prefix + "_local_equals_global", local == global_)
        if local:
            accepted.append(shift)

    residue_periods = [
        shift for shift in product(range(a), range(b))
        if global_period(motif, a, b, shift)
    ]
    covolume = gcd_of_minors(accepted)
    check(
        prefix + "_accepted_list_generates_full_group",
        covolume * len(residue_periods) == a * b,
    )
    check(
        prefix + "_free_action_divisibility",
        len(motif) % len(residue_periods) == 0,
    )
    orbits = orbit_count(motif, a, b, residue_periods)
    check(
        prefix + "_primitive_orbit_count",
        orbits * len(residue_periods) == len(motif),
    )


def exhaustive_motifs() -> None:
    sites = list(product(range(3), range(3)))
    for mask in range(1, 1 << len(sites)):
        motif = frozenset(
            (x, y, 1)
            for index, (x, y) in enumerate(sites)
            if mask & (1 << index)
        )
        check_motif(motif, 3, 3, "uncoloured_3x3")

    sites = list(product(range(4), range(2)))
    for colours in product(range(3), repeat=len(sites)):
        if not any(colours):
            continue
        motif = frozenset(
            (x, y, colour)
            for (x, y), colour in zip(sites, colours)
            if colour
        )
        check_motif(motif, 4, 2, "two_colour_4x2")

    motif = frozenset({(0, 0, 1), (1, 0, 1)})
    patch = periodic_patch(motif, 4, 3)
    one_sided = (1, 0, 1) in patch
    check(
        "one_sided_pair_match_is_not_a_period",
        one_sided and not global_period(motif, 4, 3, (1, 0)),
    )
    check(
        "two_sided_patch_rejects_false_period",
        not local_two_sided_period(motif, patch, (1, 0)),
    )


Body = tuple[F, F, tuple[F, ...]]


def body_metric(C: Body, D: Body, shift: tuple[F, F] = (F(0), F(0))) -> F:
    cx, cy, cs = C
    dx, dy, ds = D
    centre = max(abs(cx + shift[0] - dx), abs(cy + shift[1] - dy))
    support = max(abs(a - b) for a, b in zip(cs, ds))
    return centre + support


def patch_defect(
    sources: list[Body] | tuple[Body, ...],
    targets: list[Body] | tuple[Body, ...],
    shift: tuple[F, F],
) -> F:
    return max(
        min(
            body_metric(C, D, (sign * shift[0], sign * shift[1]))
            for D in targets
        )
        for C in sources
        for sign in (-1, 1)
    )


def noisy_patch_checks() -> None:
    rng = random.Random(20261003)
    fixtures: list[tuple[Body, ...]] = [
        (
            (F(0), F(0), (F(1, 4), F(1, 9))),
            (F(2), F(0), (F(1, 4), F(1, 9))),
            (F(1), F(2), (F(1, 5), F(1, 7))),
        ),
        (
            (F(0), F(0), (F(1, 3), F(1, 8))),
            (F(1), F(1), (F(1, 3), F(1, 8))),
            (F(3), F(2), (F(1, 6), F(2, 9))),
        ),
    ]
    for motif in fixtures:
        a, b = 4, 5
        targets = tuple(
            (x + a * i, y + b * j, support)
            for x, y, support in motif
            for i in range(-3, 4)
            for j in range(-3, 4)
        )
        shifts = [(F(a), F(0)), (F(0), F(b))]
        shifts.extend(
            (x - motif[0][0], y - motif[0][1]) for x, y, _ in motif
        )
        exact = [patch_defect(motif, targets, shift) for shift in shifts]
        positives = [value for value in exact if value > 0]
        eta = min(positives) if positives else F(1)
        e = min(F(1, 100_000), eta / 1000)

        for _ in range(20):
            jitter: dict[Body, Body] = {}
            for C in targets:
                x, y, support = C
                jx = e * F(rng.randint(-20, 20), 10)
                jy = e * F(rng.randint(-20, 20), 10)
                js = tuple(e * F(rng.randint(-30, 30), 10) for _ in support)
                jitter[C] = (
                    x + jx,
                    y + jy,
                    tuple(s + t for s, t in zip(support, js)),
                )
            measured_sources = [jitter[C] for C in motif]
            measured_targets = list(jitter.values())
            for shift, exact_defect in zip(shifts, exact):
                target_x = motif[0][0] + shift[0]
                target_y = motif[0][1] + shift[1]
                endpoint = next(
                    C for C in targets if C[0] == target_x and C[1] == target_y
                )
                measured_root = jitter[motif[0]]
                measured_endpoint = jitter[endpoint]
                measured_shift = (
                    measured_endpoint[0] - measured_root[0],
                    measured_endpoint[1] - measured_root[1],
                )
                estimated = patch_defect(
                    measured_sources, measured_targets, measured_shift
                )
                check(
                    "fourteen_e_defect_lipschitz_bound",
                    abs(estimated - exact_defect) <= 14 * e,
                )
                if exact_defect == 0:
                    check("noisy_true_period_accepted", estimated < eta / 2)
                else:
                    check("noisy_nonperiod_rejected", estimated > eta / 2)


def lattice_arithmetic() -> None:
    rng = random.Random(2803)
    for _ in range(1200):
        vectors = [(1, 0), (0, 1)]
        vectors.extend(
            (rng.randint(-8, 8), rng.randint(-8, 8))
            for _ in range(rng.randint(2, 7))
        )
        independent = [
            (u, v) for u, v in combinations(vectors, 2) if det(u, v)
        ]
        D1, D2 = rng.choice(independent)
        pair_index = abs(det(D1, D2))
        coordinates = [
            (
                F(det(w, D2), det(D1, D2)),
                F(det(D1, w), det(D1, D2)),
            )
            for w in vectors
        ]
        for x, y in coordinates:
            check(
                "coordinate_denominators_divide_pair_index",
                pair_index % x.denominator == 0
                and pair_index % y.denominator == 0,
            )
        q = 1
        for x, y in coordinates:
            q = lcm(q, x.denominator, y.denominator)
        check("common_denominator_divides_pair_index", pair_index % q == 0)
        integer_group = [(q, 0), (0, q)]
        integer_group.extend((int(q * x), int(q * y)) for x, y in coordinates)
        hermite_index = gcd_of_minors(integer_group)
        check(
            "hermite_covolume_formula",
            F(pair_index * hermite_index, q * q) == 1,
        )
        check("hermite_index_bounds", 1 <= hermite_index <= q * q)

    for Q in range(1, 25):
        values = sorted(
            {F(n, d) for d in range(1, Q + 1)
             for n in range(-3 * d, 3 * d + 1)}
        )
        check(
            "bounded_denominator_separation",
            all(b - a >= F(1, Q * Q) for a, b in zip(values, values[1:])),
        )
        step = max(1, len(values) // 40)
        for value in values[::step]:
            noisy = value + F(1, 4 * Q * Q)
            nearest = min(values, key=lambda candidate: abs(candidate - noisy))
            check("unique_rational_lock", nearest == value)


def symmetry_jump_and_geometry() -> None:
    for denominator in range(9, 151):
        t = F(1, denominator)
        motif: tuple[Body, ...] = (
            (F(0), F(0), (F(1, 4),)),
            (F(2) + t, F(0), (F(1, 4),)),
        )
        targets = tuple(
            (x + 4 * i, y + 4 * j, support)
            for x, y, support in motif
            for i in range(-3, 4)
            for j in range(-2, 3)
        )
        false_shift = (F(2) + t, F(0))
        check(
            "repeated_disk_false_shift_defect",
            patch_defect(motif, targets, false_shift) == 2 * t,
        )
        check("repeated_disk_false_shift_is_not_period", (4 + 2 * t) % 4 != 0)
    check("symmetry_point_primitive_covolume", F(2 * 4) == 8)

    for L0 in [F(1), F(3, 2), F(3), F(11), F(50)]:
        B = 1 + L0
        for D0 in [F(1, 4), F(2), F(9)]:
            R = 12 * B + 2 * D0 + 3
            for e in [B / 1000, B / 100, B / 20]:
                check("central_representative_selected", B + 2 * e < 2 * B)
                check("protected_generators_retained", 3 * B + 4 * e < 4 * B)
                check("period_partners_available", 8 * B + 8 * e < 10 * B)
                check("partial_hull_selection_safe", 10 * B + e < 11 * B)
                check(
                    "boundary_collar_inside_launch_square",
                    11 * B + D0 + 1 + F(1, 2) < R,
                )

    check("first_hit_flux_constant", sqrt(3) >= 1)
    check("hull_localization_exponent", 2 * F(3, 4) == F(3, 2))
    check("smoothing_noise_exponent", F(3, 2) - 2 * F(1, 4) == 1)
    check("fourth_order_smoothing_bias", 4 * F(1, 4) == 1)

    for gap in [F(1, 3), F(1, 17), F(1, 101)]:
        found = False
        for j in range(1, 100):
            e = F(1, 2 ** (2 * j))
            threshold = F(1, 2**j)
            if 20 * e < threshold < gap - 20 * e:
                found = True
                break
        check("pointwise_threshold_eventually_separates", found)


def main() -> None:
    exhaustive_motifs()
    noisy_patch_checks()
    lattice_arithmetic()
    symmetry_jump_and_geometry()
    result = {
        "schema": "a2-v28-independent-review-diagnostics-1",
        "status": "passed",
        "checks": dict(sorted(COUNTS.items())),
        "total_checks": sum(COUNTS.values()),
        "imports_author_code": False,
        "arithmetic": "exact integer/rational except one elementary sqrt comparison",
        "tex_build": False,
        "physical_sensor_executed": False,
        "uniform_smooth_table_proof_certificate": False,
        "editorial_decision": False,
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
