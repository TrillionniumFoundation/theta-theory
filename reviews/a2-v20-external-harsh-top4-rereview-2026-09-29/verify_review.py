#!/usr/bin/env python3
"""Independent exact finite diagnostics for the external A2 v20 rereview.

The script imports no author verification code. It checks finite integer
identities behind all-cycle saturation and exact disk models of obstruction
descent. It is not a proof certificate, a TeX build, or an editorial decision.
"""
from __future__ import annotations

from collections import Counter, deque
from itertools import combinations
from math import gcd
import json

REVIEWED_COMMIT = "c376e802e6e86735888dcd685f987c7a8f475903"
CHECKS: Counter[str] = Counter()


def check(ok: bool, group: str, detail: str = "") -> None:
    if not ok:
        raise RuntimeError(f"{group}: {detail}")
    CHECKS[group] += 1


def det(a: tuple[int, int], b: tuple[int, int]) -> int:
    return a[0] * b[1] - a[1] * b[0]


def determinant_gcd(columns: list[tuple[int, int]]) -> int:
    value = 0
    for first, second in combinations(columns, 2):
        value = gcd(value, abs(det(first, second)))
    return value


def exact_all_cycle_checks() -> None:
    """Check the normalized-minor formula on 3,700 rank-two families."""
    total_scaled_coordinates = 0
    for index in range(3700):
        # D Z^2 is an index-n sublattice of Z^2.
        n = 1 + index % 17
        shear = (7 * index + 3) % n
        first = (n, 0)
        second = (shear, 1)

        count = 5 if index < 2368 else 4
        columns = [first, second]
        candidates = [
            ((3 * index + 1) % 23 - 11, (5 * index + 2) % 19 - 9),
            ((11 * index + 4) % 29 - 14, (13 * index + 7) % 17 - 8),
            ((17 * index + 5) % 31 - 15, (19 * index + 9) % 23 - 11),
        ]
        columns.extend(candidates[: count - 2])

        pair_index = abs(det(first, second))
        check(pair_index == n, "pair_index_integral", str(index))

        scaled: list[tuple[int, int]] = []
        for x, y in columns:
            # b = n D^{-1} d for D=[[n,shear],[0,1]].
            b = (x - shear * y, n * y)
            scaled.append(b)
            check(
                (
                    first[0] * b[0] + second[0] * b[1],
                    first[1] * b[0] + second[1] * b[1],
                )
                == (n * x, n * y),
                "scaled_coordinates_integral",
                str((index, (x, y))),
            )
            total_scaled_coordinates += 1

        scaled_gcd = determinant_gcd(scaled)
        physical_gcd = determinant_gcd(columns)
        check(scaled_gcd % n == 0, "gcd_divisible_by_pair_index", str(index))
        check(scaled_gcd // n == physical_gcd, "normalized_minor_gcd", str(index))
        # For a rank-two subgroup of Z^2 the gcd of 2x2 minors is its index.
        check(
            physical_gcd == determinant_gcd(columns),
            "all_cycle_index_formula",
            str(index),
        )

    check(total_scaled_coordinates == 17168, "scaled_coordinate_count")

    example = [(1, 0), (1, 2), (-1, 3)]
    minors = sorted(abs(det(a, b)) for a, b in combinations(example, 2))
    check(minors == [2, 3, 5], "235_minors")
    check(determinant_gcd(example) == 1, "235_saturated")
    check(determinant_gcd(example[:2]) == 2, "235_partial_index")


def add(a: tuple[int, int], b: tuple[int, int]) -> tuple[int, int]:
    return a[0] + b[0], a[1] + b[1]


def sub(a: tuple[int, int], b: tuple[int, int]) -> tuple[int, int]:
    return a[0] - b[0], a[1] - b[1]


def norm2(a: tuple[int, int]) -> int:
    return a[0] * a[0] + a[1] * a[1]


def disk_graph(
    centers: list[tuple[int, int]],
    periods: tuple[int, int],
    radius: int,
    cutoff: int,
) -> dict[str, int]:
    """Construct an exact finite quotient model for equal periodic disks."""
    lx, ly = periods
    vertex_count = len(centers)
    check(
        (cutoff + 2 * radius) ** 2 > lx * lx + ly * ly,
        "range_above_cover_bound",
    )

    kmax = (cutoff + 2 * radius + max(lx, ly)) // min(lx, ly) + 2
    copies = [
        (vertex, k, ell, (center[0] + k * lx, center[1] + ell * ly))
        for vertex, center in enumerate(centers)
        for k in range(-kmax, kmax + 1)
        for ell in range(-kmax, kmax + 1)
    ]

    all_edges: dict[
        tuple[int, int, int, int],
        tuple[int, tuple[int, int, int, tuple[int, int]] | None],
    ] = {}
    clear_edges: list[tuple[int, int, int, int]] = []

    for source, center in enumerate(centers):
        for target, k, ell, translated in copies:
            if (target, k, ell) == (source, 0, 0):
                continue
            direction = sub(translated, center)
            distance_squared = norm2(direction)
            if distance_squared >= (cutoff + 2 * radius) ** 2:
                continue
            check(distance_squared > (2 * radius) ** 2, "disk_disjointness")

            blocker = None
            for third, a, b, point in copies:
                if (third, a, b) in ((source, 0, 0), (target, k, ell)):
                    continue
                relative = sub(point, center)
                projection = relative[0] * direction[0] + relative[1] * direction[1]
                # A third radius-r disk intersects the open center segment
                # exactly when this integer predicate holds.
                if (
                    0 < projection < distance_squared
                    and det(relative, direction) ** 2
                    <= radius * radius * distance_squared
                ):
                    blocker = (third, a, b, point)
                    break

            key = (source, target, k, ell)
            all_edges[key] = (distance_squared, blocker)
            if blocker is None:
                clear_edges.append(key)
            else:
                point = blocker[3]
                check(
                    norm2(sub(point, center)) < distance_squared,
                    "strict_left_descent",
                )
                check(
                    norm2(sub(translated, point)) < distance_squared,
                    "strict_right_descent",
                )

    cache: dict[tuple[int, int, int, int], list[tuple[int, int, int]]] = {}
    active: set[tuple[int, int, int, int]] = set()

    def replacement(key: tuple[int, int, int, int]) -> list[tuple[int, int, int]]:
        if key in cache:
            return cache[key]
        check(key not in active, "descent_acyclic")
        active.add(key)
        source, target, k, ell = key
        _, blocker = all_edges[key]
        if blocker is None:
            route = [(source, 0, 0), (target, k, ell)]
        else:
            third, a, b, _ = blocker
            left = replacement((source, third, a, b))
            right = replacement((third, target, k - a, ell - b))
            shifted = [(vertex, x + a, y + b) for vertex, x, y in right]
            check(left[-1] == shifted[0], "replacement_concatenates")
            route = left + shifted[1:]
        active.remove(key)
        cache[key] = route
        return route

    for key in all_edges:
        route = replacement(key)
        check(
            route[0] == (key[0], 0, 0)
            and route[-1] == (key[1], key[2], key[3]),
            "replacement_endpoint",
        )
        for left, right in zip(route, route[1:]):
            step = (
                left[0],
                right[0],
                right[1] - left[1],
                right[2] - left[2],
            )
            check(all_edges[step][1] is None, "replacement_clear")

    adjacency: dict[int, list[tuple[int, tuple[int, int]]]] = {
        vertex: [] for vertex in range(vertex_count)
    }
    for source, target, k, ell in clear_edges:
        adjacency[source].append((target, (k, ell)))

    placed = {0: (0, 0)}
    queue = deque([0])
    while queue:
        source = queue.popleft()
        for target, translation in adjacency[source]:
            if target not in placed:
                placed[target] = add(placed[source], translation)
                queue.append(target)
    check(len(placed) == vertex_count, "quotient_connected")

    cycles = [
        sub(add(placed[source], (k, ell)), placed[target])
        for source, target, k, ell in clear_edges
    ]
    check(determinant_gcd(cycles) == 1, "cycles_generate_deck_lattice")

    shifts = {
        vertex: (2 * vertex - 1, vertex * vertex + 1)
        for vertex in range(vertex_count)
    }
    changed_placed = {
        vertex: sub(position, shifts[vertex])
        for vertex, position in placed.items()
    }
    changed_cycles = []
    for source, target, k, ell in clear_edges:
        changed_label = add((k, ell), sub(shifts[source], shifts[target]))
        changed_cycles.append(
            sub(add(changed_placed[source], changed_label), changed_placed[target])
        )
    check(changed_cycles == cycles, "representative_gauge_invariance")

    return {
        "vertices": vertex_count,
        "oriented_short_pairs": len(all_edges),
        "oriented_clear_edges": len(clear_edges),
        "blocked_pairs": len(all_edges) - len(clear_edges),
        "radius": radius,
        "cutoff": cutoff,
    }


def exact_periodic_models() -> list[dict[str, int]]:
    return [
        disk_graph([(0, 0)], (80, 100), 1, 140),
        disk_graph([(0, 0), (36, 29)], (80, 100), 1, 138),
        disk_graph([(0, 0), (37, 19), (18, 61)], (80, 100), 1, 145),
        disk_graph(
            [(0, 0), (37, 19), (18, 61), (59, 68)],
            (80, 100),
            2,
            170,
        ),
    ]


def main() -> None:
    exact_all_cycle_checks()
    models = exact_periodic_models()
    result = {
        "schema": "a2-v20-independent-review-diagnostics-1",
        "reviewed_commit": REVIEWED_COMMIT,
        "status": "passed",
        "scope": "finite exact integer and periodic equal-disk diagnostics only",
        "checks": dict(sorted(CHECKS.items())),
        "total_checks": sum(CHECKS.values()),
        "periodic_models": models,
        "imports_author_code": False,
        "mathematical_proof_certificate": False,
        "full_tex_build": False,
        "editorial_decision": False,
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
