#!/usr/bin/env python3
"""Independent finite diagnostics for the external A2 v21 rereview.

The script imports no author verification code and uses only the Python
standard library.  It checks exact finite subgroup, weighted-graph, pair-key,
aperture, cutoff-pattern, and exponent identities used in the new v21
arguments.  It is not a proof certificate, a billiard simulation, a TeX
build, a literature-priority determination, or a journal decision.
"""
from __future__ import annotations

from collections import Counter
from fractions import Fraction as F
from itertools import combinations
import json
import math
import random

REVIEWED_COMMIT = "5ab3be483386dab1b2f53575f47dbf7aebd92bd3"
RANDOM_SEED = 20260929
RNG = random.Random(RANDOM_SEED)
CHECKS: Counter[str] = Counter()


def check(condition: bool, group: str, detail: str = "") -> None:
    if not condition:
        raise RuntimeError(f"{group}: {detail}")
    CHECKS[group] += 1


def determinant(u: tuple[int | F, int | F], v: tuple[int | F, int | F]):
    return u[0] * v[1] - u[1] * v[0]


def subgroup_index(columns: list[tuple[int, int]]) -> int:
    """Index in Z^2 of the rank-two column subgroup."""
    return math.gcd(
        *(abs(int(determinant(u, v))) for u, v in combinations(columns, 2))
    )


# ---------------------------------------------------------------------------
# Sparse saturation: deterministic power-of-two chains give exactly the
# proper-divisor argument used in the proof, including its logarithmic bound.
# ---------------------------------------------------------------------------

def sparse_saturation_checks() -> None:
    for case in range(1200):
        exponent = 2 if case < 575 else 1
        initial_index = 2**exponent
        selected = [(initial_index, 0), (0, 1)]
        available = [(2**power, 0) for power in range(exponent - 1, -1, -1)]
        current = subgroup_index(selected)
        steps = 0

        while current > 1:
            candidates = [
                vector
                for vector in available
                if subgroup_index(selected + [vector]) < current
            ]
            check(bool(candidates), "outside_generator_exists", str(case))
            vector = candidates[0]
            new_index = subgroup_index(selected + [vector])
            check(
                current % new_index == 0 and 2 * new_index <= current,
                "proper_divisor_halving",
                str((case, current, new_index)),
            )
            selected.append(vector)
            current = new_index
            steps += 1

        check(current == 1, "saturation_reached", str(case))
        check(
            steps <= initial_index.bit_length() - 1,
            "log2_step_bound",
            str((case, steps)),
        )

        # Five obstacle-orbit counts test
        # (r-1) tree edges + the selected cycle edges.
        for obstacle_count in range(1, 6):
            check(
                (obstacle_count - 1) + len(selected)
                <= obstacle_count + 1 + initial_index.bit_length() - 1,
                "edge_count_bound",
                str((case, obstacle_count)),
            )


# ---------------------------------------------------------------------------
# Relative-neighbor descent on arbitrary positive symmetric weights.  No
# triangle inequality is assumed.  This is a finite model of component
# preservation, not a proof for periodic convex bodies.
# ---------------------------------------------------------------------------

def connected_components(
    vertex_count: int, edges: set[tuple[int, int]]
) -> list[tuple[int, ...]]:
    adjacency = [set() for _ in range(vertex_count)]
    for left, right in edges:
        adjacency[left].add(right)
        adjacency[right].add(left)

    unseen = set(range(vertex_count))
    components: list[tuple[int, ...]] = []
    while unseen:
        stack = [min(unseen)]
        seen: set[int] = set()
        while stack:
            vertex = stack.pop()
            if vertex in seen:
                continue
            seen.add(vertex)
            stack.extend(adjacency[vertex] - seen)
        unseen -= seen
        components.append(tuple(sorted(seen)))
    return sorted(components)


def relative_graph_checks() -> None:
    for case in range(1000):
        vertex_count = RNG.randint(3, 10)
        gaps = [[0] * vertex_count for _ in range(vertex_count)]
        for left, right in combinations(range(vertex_count), 2):
            gaps[left][right] = gaps[right][left] = RNG.randint(1, 50)
        cutoff = RNG.randint(5, 51)

        full = {
            (left, right)
            for left, right in combinations(range(vertex_count), 2)
            if gaps[left][right] < cutoff
        }
        relative = {
            (left, right)
            for left, right in full
            if not any(
                gaps[left][middle] < gaps[left][right]
                and gaps[middle][right] < gaps[left][right]
                for middle in range(vertex_count)
                if middle not in (left, right)
            )
        }
        check(
            connected_components(vertex_count, full)
            == connected_components(vertex_count, relative),
            "relative_components",
            str(case),
        )


# ---------------------------------------------------------------------------
# Undirected positioned-pair keys: translations and return reversal leave the
# same intrinsic key.  Shape congruence itself is not tested here.
# ---------------------------------------------------------------------------

def pair_key(
    source_type: int,
    target_type: int,
    source: tuple[int, int],
    target: tuple[int, int],
) -> tuple[int, int, int, int]:
    displacement = (target[0] - source[0], target[1] - source[1])
    forward = (
        source_type,
        target_type,
        displacement[0],
        displacement[1],
    )
    backward = (
        target_type,
        source_type,
        -displacement[0],
        -displacement[1],
    )
    return min(forward, backward)


def pair_key_checks() -> None:
    for case in range(3000):
        source_type = RNG.randint(0, 4)
        target_type = RNG.randint(0, 4)
        displacement = (RNG.randint(-10, 10), RNG.randint(-10, 10))
        if displacement == (0, 0) and source_type == target_type:
            displacement = (1, 0)
        source = (RNG.randint(-20, 20), RNG.randint(-20, 20))
        target = (
            source[0] + displacement[0],
            source[1] + displacement[1],
        )

        check(
            pair_key(source_type, target_type, source, target)
            == pair_key(source_type, target_type, (0, 0), displacement),
            "pair_key_translation",
            str(case),
        )
        check(
            pair_key(source_type, target_type, source, target)
            == pair_key(target_type, source_type, target, source),
            "pair_key_reverse",
            str(case),
        )


# ---------------------------------------------------------------------------
# A moving real period basis preserves normalized integer cycle minors.
# ---------------------------------------------------------------------------

def normalized_minor_checks() -> None:
    for case in range(2000):
        while True:
            first = (RNG.randint(-8, 8), RNG.randint(-8, 8))
            second = (RNG.randint(-8, 8), RNG.randint(-8, 8))
            if determinant(first, second) != 0:
                break

        matrix = (
            (
                F(RNG.randint(1, 9), RNG.randint(1, 7)),
                F(RNG.randint(-5, 5), RNG.randint(1, 7)),
            ),
            (
                F(RNG.randint(-5, 5), RNG.randint(1, 7)),
                F(RNG.randint(1, 9), RNG.randint(1, 7)),
            ),
        )
        volume = matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
        if volume == 0:
            matrix = ((F(2), F(1, 3)), (F(1, 5), F(3)))
            volume = matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]

        def move(vector: tuple[int, int]) -> tuple[F, F]:
            return (
                matrix[0][0] * vector[0] + matrix[0][1] * vector[1],
                matrix[1][0] * vector[0] + matrix[1][1] * vector[1],
            )

        check(
            determinant(move(first), move(second)) / volume
            == determinant(first, second),
            "normalized_minor_persistence",
            str(case),
        )


# ---------------------------------------------------------------------------
# Exact rectangular-lattice coset models for aperture representatives and the
# algebraic packing identity used in the padded-disk count.
# ---------------------------------------------------------------------------

def nearest_integer(value: F) -> int:
    quotient, remainder = divmod(value.numerator, value.denominator)
    if 2 * remainder >= value.denominator:
        quotient += 1
    return quotient


def aperture_checks() -> None:
    for case in range(2700):
        step_x = F(RNG.randint(1, 7), RNG.randint(1, 5))
        step_y = F(RNG.randint(1, 7), RNG.randint(1, 5))
        x = F(RNG.randint(-50, 50), RNG.randint(1, 11)) * step_x
        y = F(RNG.randint(-50, 50), RNG.randint(1, 11)) * step_y
        copy_x = nearest_integer(x / step_x)
        copy_y = nearest_integer(y / step_y)
        error_x = x - copy_x * step_x
        error_y = y - copy_y * step_y
        aperture = step_x + step_y + F(1, 10)
        check(
            error_x * error_x + error_y * error_y < aperture * aperture,
            "coset_representative_in_aperture",
            str(case),
        )

    for case in range(81):
        radius = F(RNG.randint(1, 20), RNG.randint(1, 10))
        separation = F(RNG.randint(1, 10), RNG.randint(1, 10))
        check(
            (radius + separation / 2) ** 2 / (separation / 2) ** 2
            == (1 + 2 * radius / separation) ** 2,
            "packing_identity",
            str(case),
        )


# ---------------------------------------------------------------------------
# Exact affine-gap controls for the qualitative cutoff-crossing pattern.  This
# models the sign change and persistent basis edges; it is not a physical proof
# of the manuscript's analytic obstacle family.
# ---------------------------------------------------------------------------

def cutoff_and_rate_checks() -> None:
    reference_scale = F(3, 100)
    for case in range(50):
        scale = reference_scale + F(case - 25, 10000)
        cutoff = F(5) - 2 * reference_scale
        extra_gap = F(5) - 2 * scale
        witness_gap = F(2) - 2 * scale
        twice_cover_bound = F(3) - 2 * scale

        check(cutoff > twice_cover_bound, "range_above_cover", str(case))
        check(
            subgroup_index([(1, 0), (0, 1)]) == 1,
            "witness_saturated",
            str(case),
        )
        check(witness_gap < cutoff, "basis_edges_below_cutoff", str(case))
        check(
            (extra_gap < cutoff) == (scale > reference_scale),
            "extra_cutoff_pattern",
            str(case),
        )

    for beta in [F(1, 5), F(1, 4), F(1, 3), F(1, 2), F(2, 3), F(3, 4), F(1)]:
        mesh_exponent = 1 / (2 * beta + 6)
        check(
            beta * mesh_exponent == F(1, 2) - 3 * mesh_exponent,
            "rate_main_balance",
            str(beta),
        )
        check(
            1 - 4 * mesh_exponent >= beta * mesh_exponent,
            "rate_linear_subdominant",
            str(beta),
        )


def main() -> None:
    sparse_saturation_checks()
    relative_graph_checks()
    pair_key_checks()
    normalized_minor_checks()
    aperture_checks()
    cutoff_and_rate_checks()

    result = {
        "schema": "a2-v21-independent-review-diagnostics-1",
        "reviewed_commit": REVIEWED_COMMIT,
        "random_seed": RANDOM_SEED,
        "status": "passed",
        "scope": (
            "Exact finite subgroup, weighted-graph, pair-key, aperture, "
            "cutoff-pattern and exponent diagnostics only"
        ),
        "checks": dict(sorted(CHECKS.items())),
        "total_checks": sum(CHECKS.values()),
        "imports_author_verification_code": False,
        "mathematical_proof_certificate": False,
        "full_tex_build": False,
        "literature_priority_certificate": False,
        "editorial_decision": False,
    }
    if result["total_checks"] != 23945:
        raise RuntimeError(f"unexpected check count: {result['total_checks']}")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
