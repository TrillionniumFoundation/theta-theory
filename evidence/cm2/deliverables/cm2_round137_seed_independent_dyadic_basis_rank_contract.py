#!/usr/bin/env python3
"""Round137: executable seed-independent dyadic basis/rank contract.

Round27 used a fixed bijective enumeration of rational-dyadic basis boxes to
prove countability of regular return components, and Round35 used an analogous
one-dimensional interval rank on unstable leaves.  Those certificates froze
only existential prose: they did not freeze a coordinate normalization, row
encoding, order, index origin, or executable rank algorithm.  This append-only
producer therefore defines a *new* prospective ``v1`` implementation.  It does
not claim to recover the unnamed historical enumeration and cannot mint an old
``c24-component`` or ``rn-restriction`` identifier.

For every frozen source core, the exact increasing affine map sends its
``(t,p)`` rectangle to ``(0,1)^2``.  At common dyadic denominator ``2^m`` a
two-dimensional basis row is ``(m,a0,a1,b0,b1)`` with strictly interior,
ordered endpoints.  A row is primitive exactly when its four endpoint
numerators are not all even.  This is a *common-denominator* condition, not a
separate primitive condition on each coordinate interval.

Writing ``I_m = binom(2^m-1,2)``, level ``m`` contains
``I_m^2-I_{m-1}^2`` primitive rows.  Hence the zero-based offset of level
``m`` is exactly ``I_{m-1}^2``.  Rows are lexicographic after the level, with
all-even rows skipped.  The one-dimensional analogue has primitive count
``I_m-I_{m-1}`` and offset ``I_{m-1}``.

The producer includes executable rank/unrank algorithms, exhaustive small
level tests, large-index fixtures, and an exact normalized dyadic box whose
closure is strictly inside the Round136 positive-area R_1056 source box.  That
box gives only a rank upper bound for the component containing the witness
under this new v1 enumeration.  The historical Round27 canonical rank, all
Round35 restriction fields, owner data, q_j, Gate5, and CM2 remain unpromoted.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import stat
import sys
import tempfile
from fractions import Fraction as Q
from pathlib import Path
from typing import Any

import cm2_gate25_physical_return_core_registry_cert as core_cert


if hasattr(sys, "set_int_max_str_digits"):
    # The Round136 witness rank has about 4,600 decimal digits.  It is public
    # mathematical data, not attacker-controlled input.
    sys.set_int_max_str_digits(0)


HERE = Path(__file__).resolve().parent
OUTPUT = (
    HERE
    / "cm2-round137-seed-independent-dyadic-basis-rank-contract-2026-07-24.json"
)
SCHEMA = "cm2.round137.seed-independent-dyadic-basis-rank-contract.v1"

ROUND27 = (
    HERE / "cm2-gate34-round27-arbitrary-n-path-schema-manifest-2026-07-18.json"
)
ROUND35 = (
    HERE / "cm2-gate45-round35-arbitrary-rn-common-carrier-manifest-2026-07-19.json"
)
ROUND136_PRODUCER = (
    HERE / "cm2_round136_rank3_positive_width_r1056_return_frontier.py"
)
ROUND136 = (
    HERE / "cm2-round136-rank3-positive-width-r1056-return-frontier-2026-07-24.json"
)
CORE_MANIFEST = (
    HERE / "cm2-gate25-physical-return-core-registry-manifest-2026-07-16.json"
)

PINS = {
    "cm2_gate25_physical_return_core_registry_cert.py":
        "2da58e5fb5fe030023d6fade7252ec67d0e494708b32d1e32b3ce545e2052fdb",
    CORE_MANIFEST.name:
        "144f5516ada8b83ca07459582c8cdb07ba09db11ac18a90cff32c6396c6e5a42",
    ROUND27.name:
        "988f364bd1e6943178238c072e725de01af36452ef25d179eae6aef4000f7916",
    ROUND35.name:
        "ece7c97beeeb0b527434dc430e247ad0af407dc58b82d634da9e34a2f9e9521c",
    ROUND136_PRODUCER.name:
        "4e78309d5275bf367e6df03509c40ebaaac6f344c7948446a25b3b508c8c2bc2",
    ROUND136.name:
        "d9b7b7823dddce2dcbc16412294c8ecef42b304712d4bb968896d2221b8aa7f9",
}


def require(condition: bool, label: str) -> None:
    if not condition:
        raise RuntimeError(label)


def canonical(value: Any) -> str:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    )


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value).encode("utf-8")).hexdigest()


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def reject_constant(value: str) -> None:
    raise ValueError(f"non-finite JSON constant: {value}")


def no_duplicate_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def strict_json(path: Path) -> dict[str, Any]:
    value = json.loads(
        path.read_text(encoding="utf-8"),
        object_pairs_hook=no_duplicate_pairs,
        parse_constant=reject_constant,
    )
    require(isinstance(value, dict), f"{path.name} JSON object")
    return value


def qstr(value: Q) -> str:
    value = Q(value)
    return (
        str(value.numerator)
        if value.denominator == 1
        else f"{value.numerator}/{value.denominator}"
    )


def core_payload(core: core_cert.Core) -> dict[str, Any]:
    return {
        "chart_id": core.chart_id,
        "t": [qstr(core.t0), qstr(core.t1)],
        "p": [qstr(core.p0), qstr(core.p1)],
        "target_id": core.target_id,
        "crossings": list(core.crossings),
    }


def core_id(core: core_cert.Core) -> str:
    return "core:" + digest(core_payload(core))


def interval_pair_count(level: int) -> int:
    """I_m: all strictly interior endpoint pairs at denominator 2^m."""
    require(level >= 0, "nonnegative dyadic level")
    if level < 2:
        return 0
    interior_point_count = 2**level - 1
    return interior_point_count * (interior_point_count - 1) // 2


def validate_pair(level: int, left: int, right: int) -> None:
    require(level >= 2, "dyadic level at least 2")
    maximum = 2**level - 1
    require(1 <= left < right <= maximum, "strict interior ordered endpoints")


def pair_lex_rank(level: int, left: int, right: int) -> int:
    """Zero-based lexicographic rank among all endpoint pairs at one level."""
    validate_pair(level, left, right)
    maximum = 2**level - 1
    preceding_first = left - 1
    return (
        preceding_first * maximum
        - preceding_first * (preceding_first + 1) // 2
        + right - left - 1
    )


def pair_lex_unrank(level: int, rank: int) -> tuple[int, int]:
    """Inverse of pair_lex_rank using exact integer square roots."""
    total = interval_pair_count(level)
    require(0 <= rank < total, "pair rank range")
    maximum = 2**level - 1
    coefficient = 2 * maximum - 1
    discriminant = coefficient * coefficient - 8 * rank
    preceding_first = (coefficient - math.isqrt(discriminant)) // 2

    def offset(k: int) -> int:
        return k * maximum - k * (k + 1) // 2

    while preceding_first > 0 and offset(preceding_first) > rank:
        preceding_first -= 1
    while (
        preceding_first + 1 <= maximum - 2
        and offset(preceding_first + 1) <= rank
    ):
        preceding_first += 1
    left = preceding_first + 1
    right = left + 1 + rank - offset(preceding_first)
    validate_pair(level, left, right)
    return left, right


def pair_is_even(pair: tuple[int, int]) -> bool:
    return pair[0] % 2 == 0 and pair[1] % 2 == 0


def even_pair_count_before(level: int, left: int, right: int) -> int:
    """Number of all-even endpoint pairs lexicographically before a pair."""
    validate_pair(level, left, right)
    half_maximum = 2 ** (level - 1) - 1
    earlier_even_first_count = (left - 1) // 2
    count = (
        earlier_even_first_count * half_maximum
        - earlier_even_first_count * (earlier_even_first_count + 1) // 2
    )
    if left % 2 == 0:
        reduced_left = left // 2
        count += max(0, (right - 1) // 2 - reduced_left)
    return count


def primitive_pair_unrank(level: int, rank: int) -> tuple[int, int]:
    """Select a pair with at least one odd endpoint by filtered lex rank."""
    total = interval_pair_count(level)
    primitive_total = total - interval_pair_count(level - 1)
    require(0 <= rank < primitive_total, "primitive pair rank range")
    low, high = 0, total - 1
    while low <= high:
        middle = (low + high) // 2
        pair = pair_lex_unrank(level, middle)
        filtered_rank = middle - even_pair_count_before(level, *pair)
        if pair_is_even(pair):
            if rank < filtered_rank:
                high = middle - 1
            else:
                low = middle + 1
        elif rank < filtered_rank:
            high = middle - 1
        elif rank > filtered_rank:
            low = middle + 1
        else:
            return pair
    raise RuntimeError("primitive pair unrank")


def validate_2d_row(row: tuple[int, int, int, int, int]) -> None:
    level, a0, a1, b0, b1 = row
    validate_pair(level, a0, a1)
    validate_pair(level, b0, b1)
    require(
        any(endpoint % 2 for endpoint in (a0, a1, b0, b1)),
        "common denominator primitive",
    )


def rank_2d(row: tuple[int, int, int, int, int]) -> int:
    """Global zero-based rank of a primitive 2D dyadic basis box."""
    validate_2d_row(row)
    level, a0, a1, b0, b1 = row
    total_pairs = interval_pair_count(level)
    even_pairs = interval_pair_count(level - 1)
    a_rank = pair_lex_rank(level, a0, a1)
    a_even_before = even_pair_count_before(level, a0, a1)
    before_a = a_rank * total_pairs - a_even_before * even_pairs
    b_rank = pair_lex_rank(level, b0, b1)
    if not pair_is_even((a0, a1)):
        within_a = b_rank
    else:
        require(not pair_is_even((b0, b1)), "primitive b when a all-even")
        within_a = b_rank - even_pair_count_before(level, b0, b1)
    level_offset = interval_pair_count(level - 1) ** 2
    return level_offset + before_a + within_a


def level_for_2d_rank(rank: int) -> int:
    require(rank >= 0, "nonnegative 2D rank")
    low, high = 2, max(2, rank.bit_length() + 2)
    while low < high:
        middle = (low + high) // 2
        if interval_pair_count(middle) ** 2 > rank:
            high = middle
        else:
            low = middle + 1
    return low


def unrank_2d(rank: int) -> tuple[int, int, int, int, int]:
    """Inverse of rank_2d."""
    level = level_for_2d_rank(rank)
    total_pairs = interval_pair_count(level)
    even_pairs = interval_pair_count(level - 1)
    local = rank - even_pairs**2
    low, high = 0, total_pairs - 1
    while low <= high:
        middle = (low + high) // 2
        a_pair = pair_lex_unrank(level, middle)
        before_a = (
            middle * total_pairs
            - even_pair_count_before(level, *a_pair) * even_pairs
        )
        block_size = (
            total_pairs - even_pairs
            if pair_is_even(a_pair)
            else total_pairs
        )
        if local < before_a:
            high = middle - 1
        elif local >= before_a + block_size:
            low = middle + 1
        else:
            b_local = local - before_a
            b_pair = (
                primitive_pair_unrank(level, b_local)
                if pair_is_even(a_pair)
                else pair_lex_unrank(level, b_local)
            )
            row = (level, *a_pair, *b_pair)
            validate_2d_row(row)
            return row
    raise RuntimeError("2D unrank")


def validate_1d_row(row: tuple[int, int, int]) -> None:
    level, left, right = row
    validate_pair(level, left, right)
    require(left % 2 or right % 2, "1D denominator primitive")


def rank_1d(row: tuple[int, int, int]) -> int:
    """Global zero-based rank of a primitive 1D dyadic basis interval."""
    validate_1d_row(row)
    level, left, right = row
    local = (
        pair_lex_rank(level, left, right)
        - even_pair_count_before(level, left, right)
    )
    return interval_pair_count(level - 1) + local


def level_for_1d_rank(rank: int) -> int:
    require(rank >= 0, "nonnegative 1D rank")
    low, high = 2, max(2, rank.bit_length() + 2)
    while low < high:
        middle = (low + high) // 2
        if interval_pair_count(middle) > rank:
            high = middle
        else:
            low = middle + 1
    return low


def unrank_1d(rank: int) -> tuple[int, int, int]:
    """Inverse of rank_1d."""
    level = level_for_1d_rank(rank)
    local = rank - interval_pair_count(level - 1)
    pair = primitive_pair_unrank(level, local)
    row = (level, *pair)
    validate_1d_row(row)
    return row


def encoded_integer(value: int) -> dict[str, Any]:
    require(value >= 0, "encoded nonnegative integer")
    decimal = str(value)
    hexadecimal = format(value, "x")
    return {
        "decimal": decimal,
        "hexadecimal": "0x" + hexadecimal,
        "bit_length": value.bit_length(),
        "decimal_digit_count": len(decimal),
        "sha256_of_decimal": hashlib.sha256(decimal.encode("ascii")).hexdigest(),
    }


def normalization_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    cores = core_cert.physical_cores()
    require(len(cores) == 24, "frozen source core count")
    seen_ids: set[str] = set()
    for index, core in enumerate(cores):
        identifier = core_id(core)
        require(identifier not in seen_ids, "unique source core id")
        seen_ids.add(identifier)
        require(core.t0 < core.t1 and core.p0 < core.p1, "positive core widths")
        row = {
            "source_core_index": index,
            "source_core_id": identifier,
            "chart_id": core.chart_id,
            "target_id": core.target_id,
            "family": core.family,
            "t_bounds": [qstr(core.t0), qstr(core.t1)],
            "p_bounds": [qstr(core.p0), qstr(core.p1)],
            "normalization": {
                "u": f"(t-({qstr(core.t0)}))/({qstr(core.t1-core.t0)})",
                "v": f"(p-({qstr(core.p0)}))/({qstr(core.p1-core.p0)})",
                "inverse_t": (
                    f"({qstr(core.t0)})+u*({qstr(core.t1-core.t0)})"
                ),
                "inverse_p": (
                    f"({qstr(core.p0)})+v*({qstr(core.p1-core.p0)})"
                ),
                "orientation": "increasing_in_each_coordinate",
                "open_core_maps_exactly_to": "(0,1)^2",
            },
        }
        row["row_sha256"] = digest(row)
        rows.append(row)
    return rows


def exhaustive_small_tests(max_level: int = 4) -> dict[str, Any]:
    require(max_level == 4, "frozen exhaustive level")
    seen_rational_boxes: set[tuple[Q, Q, Q, Q]] = set()
    seen_2d_ranks: set[int] = set()
    seen_1d_intervals: set[tuple[Q, Q]] = set()
    seen_1d_ranks: set[int] = set()
    level_rows: list[dict[str, Any]] = []
    total_2d = 0
    total_1d = 0
    for level in range(2, max_level + 1):
        maximum = 2**level - 1
        i_level = interval_pair_count(level)
        i_previous = interval_pair_count(level - 1)
        expected_2d = i_level**2 - i_previous**2
        expected_1d = i_level - i_previous
        actual_2d = 0
        actual_1d = 0
        level_2d_first = i_previous**2
        level_1d_first = i_previous
        pairs = [
            (left, right)
            for left in range(1, maximum)
            for right in range(left + 1, maximum + 1)
        ]
        require(len(pairs) == i_level, "pair count formula")
        for left, right in pairs:
            if not pair_is_even((left, right)):
                row1 = (level, left, right)
                rank1 = rank_1d(row1)
                require(unrank_1d(rank1) == row1, "1D exhaustive roundtrip")
                require(rank1 not in seen_1d_ranks, "1D unique rank")
                interval = (Q(left, 2**level), Q(right, 2**level))
                require(
                    interval not in seen_1d_intervals,
                    "1D cross-level rational uniqueness",
                )
                seen_1d_ranks.add(rank1)
                seen_1d_intervals.add(interval)
                actual_1d += 1
        for a0, a1 in pairs:
            for b0, b1 in pairs:
                row2 = (level, a0, a1, b0, b1)
                if all(value % 2 == 0 for value in row2[1:]):
                    continue
                rank2 = rank_2d(row2)
                require(unrank_2d(rank2) == row2, "2D exhaustive roundtrip")
                require(rank2 not in seen_2d_ranks, "2D unique rank")
                box = (
                    Q(a0, 2**level),
                    Q(a1, 2**level),
                    Q(b0, 2**level),
                    Q(b1, 2**level),
                )
                require(
                    box not in seen_rational_boxes,
                    "2D cross-level rational uniqueness",
                )
                seen_2d_ranks.add(rank2)
                seen_rational_boxes.add(box)
                actual_2d += 1
        require(actual_2d == expected_2d, "2D primitive count")
        require(actual_1d == expected_1d, "1D primitive count")
        require(
            min(
                rank
                for rank in seen_2d_ranks
                if level_for_2d_rank(rank) == level
            )
            == level_2d_first,
            "2D level offset",
        )
        require(
            min(
                rank
                for rank in seen_1d_ranks
                if level_for_1d_rank(rank) == level
            )
            == level_1d_first,
            "1D level offset",
        )
        total_2d += actual_2d
        total_1d += actual_1d
        level_rows.append({
            "level_m": level,
            "I_m": i_level,
            "I_m_minus_1": i_previous,
            "primitive_2d_row_count": actual_2d,
            "primitive_2d_level_offset": level_2d_first,
            "primitive_1d_row_count": actual_1d,
            "primitive_1d_level_offset": level_1d_first,
            "2d_last_rank_inclusive": i_level**2 - 1,
            "1d_last_rank_inclusive": i_level - 1,
        })
    require(total_2d == interval_pair_count(max_level) ** 2, "2D telescope")
    require(total_1d == interval_pair_count(max_level), "1D telescope")
    return {
        "exhaustive_through_level": max_level,
        "level_rows": level_rows,
        "exhaustive_2d_row_count": total_2d,
        "exhaustive_1d_row_count": total_1d,
        "all_rank_unrank_roundtrips_exact": True,
        "all_global_ranks_unique": True,
        "all_cross_level_rational_boxes_unique": True,
        "level_offsets_exact": True,
        "telescoping_counts_exact": True,
    }


def fixture_2d(row: tuple[int, int, int, int, int]) -> dict[str, Any]:
    rank = rank_2d(row)
    require(unrank_2d(rank) == row, "2D fixture roundtrip")
    return {
        "row": list(row),
        "rank": encoded_integer(rank),
        "roundtrip_exact": True,
    }


def fixture_1d(row: tuple[int, int, int]) -> dict[str, Any]:
    rank = rank_1d(row)
    require(unrank_1d(rank) == row, "1D fixture roundtrip")
    return {
        "row": list(row),
        "rank": encoded_integer(rank),
        "roundtrip_exact": True,
    }


def invalid_row_tests() -> dict[str, Any]:
    invalid_2d = [
        (1, 1, 2, 1, 2),
        (2, 0, 1, 1, 2),
        (2, 1, 1, 1, 2),
        (2, 1, 4, 1, 2),
        (3, 2, 4, 2, 6),
    ]
    invalid_1d = [
        (1, 1, 2),
        (2, 0, 1),
        (2, 1, 1),
        (2, 1, 4),
        (3, 2, 4),
    ]
    rejected_2d = 0
    rejected_1d = 0
    for row in invalid_2d:
        try:
            rank_2d(row)
        except RuntimeError:
            rejected_2d += 1
    for row in invalid_1d:
        try:
            rank_1d(row)
        except RuntimeError:
            rejected_1d += 1
    require(rejected_2d == len(invalid_2d), "invalid 2D rows rejected")
    require(rejected_1d == len(invalid_1d), "invalid 1D rows rejected")
    return {
        "invalid_2d_fixture_count": len(invalid_2d),
        "invalid_2d_rejected_count": rejected_2d,
        "invalid_1d_fixture_count": len(invalid_1d),
        "invalid_1d_rejected_count": rejected_1d,
        "boundary_order_and_nonprimitive_cases_fail_closed": True,
    }


def first_two_strict_grid_points(
    lower: Q,
    upper: Q,
    level: int,
) -> tuple[int, int] | None:
    require(Q(0) < lower < upper < Q(1), "normalized witness interval")
    denominator = 2**level
    first = (lower.numerator * denominator) // lower.denominator + 1
    second = first + 1
    if (
        first >= 1
        and second <= denominator - 1
        and Q(first, denominator) > lower
        and Q(second, denominator) < upper
    ):
        return first, second
    return None


def contained_witness_row(
    u0: Q,
    u1: Q,
    v0: Q,
    v1: Q,
) -> tuple[int, int, int, int, int]:
    level = 2
    while True:
        u_pair = first_two_strict_grid_points(u0, u1, level)
        v_pair = first_two_strict_grid_points(v0, v1, level)
        if u_pair is not None and v_pair is not None:
            row = (level, *u_pair, *v_pair)
            validate_2d_row(row)
            return row
        level += 1


def validate_dependencies() -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    for name, expected in PINS.items():
        path = HERE / name
        require(path.is_file(), f"dependency missing: {name}")
        require(sha256(path) == expected, f"dependency hash: {name}")
    round27 = strict_json(ROUND27)
    round35 = strict_json(ROUND35)
    round136 = strict_json(ROUND136)
    require(
        round27["schema"]
        == "cm2.gate34.round27-arbitrary-n-path-schema.manifest.v1",
        "Round27 schema",
    )
    component = round27["result"]["canonical_regular_connected_component_schema"]
    require(
        component["component_coordinates_and_nonempty_ranks_enumerated"] is False
        and "fixed bijective enumeration" in component["canonical_component_rank"],
        "Round27 nonconstructive enumeration boundary",
    )
    require(
        round35["schema"]
        == "cm2.gate45.round35-arbitrary-rn-common-carrier.v1.manifest.v1",
        "Round35 schema",
    )
    parent = round35["result"]["arbitrary_Rn_parent_W_Borel_registry"]
    require(
        parent["nonempty_component_coordinates_enumerated"] is False
        and "least rational-dyadic interval basis index"
        in parent["source_interval_rank"],
        "Round35 nonconstructive interval-rank boundary",
    )
    require(
        round136["schema"]
        == "cm2.round136.rank3-positive-width-r1056-return-frontier.v1",
        "Round136 schema",
    )
    require(
        digest(round136["result"]) == round136["result_sha256"],
        "Round136 result digest",
    )
    r136 = round136["result"]
    require(
        r136["actual_R1056_return_summary"]["first_return_depth"] == 1056
        and r136["actual_R1056_return_summary"]["source_box_positive_area"] is True
        and r136["strict_nonpromotion"]["c24_component_id"] is None
        and r136["strict_nonpromotion"]["Round35_rn_restriction_id"] is None,
        "Round136 frontier semantics",
    )
    return round27, round35, round136


def round136_witness_projection(
    round136: dict[str, Any],
    normalizations: list[dict[str, Any]],
) -> dict[str, Any]:
    result = round136["result"]
    source_box = result["rational_source_box_construction"][
        "actual_rational_source_box"
    ]
    source_index = source_box["source_core_index"]
    require(source_index == 14, "Round136 source index")
    core = core_cert.physical_cores()[source_index]
    identifier = core_id(core)
    require(
        identifier
        == result["actual_R1056_return_summary"]["source_core_id"]
        == normalizations[source_index]["source_core_id"],
        "Round136 source core identity",
    )
    t0, t1 = (Q(value) for value in source_box["t"])
    p0, p1 = (Q(value) for value in source_box["p"])
    require(
        core.t0 < t0 < t1 < core.t1
        and core.p0 < p0 < p1 < core.p1,
        "Round136 box strictly inside source core",
    )
    u0 = (t0 - core.t0) / (core.t1 - core.t0)
    u1 = (t1 - core.t0) / (core.t1 - core.t0)
    v0 = (p0 - core.p0) / (core.p1 - core.p0)
    v1 = (p1 - core.p0) / (core.p1 - core.p0)
    row = contained_witness_row(u0, u1, v0, v1)
    level, a0, a1, b0, b1 = row
    denominator = 2**level
    require(
        u0 < Q(a0, denominator) < Q(a1, denominator) < u1
        and v0 < Q(b0, denominator) < Q(b1, denominator) < v1,
        "dyadic witness closure strictly inside Round136 source box",
    )
    rank = rank_2d(row)
    locator_payload = {
        "contract": "round137-dyadic-basis-enumeration-v1",
        "source_core_id": identifier,
        "return_depth": 1056,
        "round136_local_return_cylinder_id":
            result["actual_R1056_return_summary"]["local_return_cylinder_id"],
        "round136_complete_candidate_path_tuple_sha256":
            result["actual_R1056_return_summary"][
                "Round27_compatible_complete_candidate_path_tuple_sha256"
            ],
        "contained_basis_row": list(row),
        "contained_basis_rank_decimal": str(rank),
    }
    locator_id = "round137-component-witness-locator:" + digest(locator_payload)
    return {
        "source_core_index": source_index,
        "source_core_id": identifier,
        "round136_local_return_cylinder_id":
            result["actual_R1056_return_summary"]["local_return_cylinder_id"],
        "return_depth": 1056,
        "physical_source_box": {
            "t": source_box["t"],
            "p": source_box["p"],
            "s": source_box["s"],
        },
        "normalized_source_box": {
            "u": [qstr(u0), qstr(u1)],
            "v": [qstr(v0), qstr(v1)],
        },
        "contained_primitive_basis_row": list(row),
        "contained_primitive_basis_denominator_power": level,
        "contained_primitive_basis_rank": encoded_integer(rank),
        "contained_basis_closure_strictly_inside_round136_box": True,
        "minimal_level_with_two_strict_grid_points_in_each_coordinate": True,
        "lex_first_consecutive_pairs_at_that_level": True,
        "component_witness_locator_id": locator_id,
        "component_witness_locator_payload_sha256": digest(locator_payload),
        "locator_is_noncanonical_and_does_not_deduplicate_components": True,
        "round137_v1_component_rank_upper_bound_available": True,
        "round137_v1_component_rank_upper_bound": encoded_integer(rank),
        "upper_bound_reason": (
            "the connected regular R_1056 component containing the strict "
            "Round136 source box also contains this closed dyadic basis box"
        ),
        "round137_v1_least_component_rank_computed": False,
        "historical_Round27_canonical_component_rank": None,
        "historical_Round27_c24_component_id": None,
        "projection_to_Round35_restriction_id": None,
    }


def build() -> dict[str, Any]:
    round27, round35, round136 = validate_dependencies()
    normalizations = normalization_rows()
    small = exhaustive_small_tests()
    invalid = invalid_row_tests()
    large_2d_rows = [
        (16, 1, 2, 3, 4),
        (64, 2, 4, 2, 3),
        (257, 2**256 - 2, 2**256 - 1, 1, 2),
    ]
    large_1d_rows = [
        (16, 1, 2),
        (64, 2, 3),
        (257, 2**256 - 2, 2**256 - 1),
    ]
    fixtures_2d = [fixture_2d(row) for row in large_2d_rows]
    fixtures_1d = [fixture_1d(row) for row in large_1d_rows]
    witness = round136_witness_projection(round136, normalizations)

    result = {
        "status": "CERTIFIED_PROSPECTIVE_SEED_INDEPENDENT_DYADIC_BASIS_RANK_CONTRACT",
        "provenance": {
            "producer_sha256": sha256(Path(__file__).resolve()),
            "dependency_sha256": dict(sorted(PINS.items())),
            "append_only": True,
            "old_artifacts_modified": False,
            "seed_independent": True,
        },
        "historical_schema_audit": {
            "Round27_component_rank_text":
                round27["result"]["canonical_regular_connected_component_schema"][
                    "canonical_component_rank"
                ],
            "Round27_component_coordinates_enumerated": False,
            "Round35_source_interval_rank_text":
                round35["result"]["arbitrary_Rn_parent_W_Borel_registry"][
                    "source_interval_rank"
                ],
            "Round35_nonempty_component_coordinates_enumerated": False,
            "historical_coordinate_normalization_frozen": False,
            "historical_basis_row_encoding_frozen": False,
            "historical_enumeration_order_frozen": False,
            "historical_zero_or_one_based_indexing_frozen": False,
            "historical_rank_unrank_algorithm_frozen": False,
            "new_v1_is_prospective_compatible_with_countability_schema_only": True,
            "new_v1_recovers_historical_numeric_labels": False,
        },
        "source_core_affine_normalization_contract": {
            "source_core_count": len(normalizations),
            "coordinate_names": ["u", "v"],
            "exact_map": (
                "u=(t-t0)/(t1-t0), v=(p-p0)/(p1-p0) for each frozen core"
            ),
            "exact_inverse": "t=t0+u*(t1-t0), p=p0+v*(p1-p0)",
            "orientation": "increasing_in_each_coordinate",
            "open_core_image": "(0,1)^2",
            "normalization_row_count": len(normalizations),
            "normalization_rows_sha256": digest(normalizations),
            "normalization_rows": normalizations,
        },
        "dyadic_basis_enumeration_v1": {
            "contract_id": "round137-dyadic-basis-enumeration-v1",
            "index_origin": "zero_based",
            "two_dimensional": {
                "row_schema": "(m,a0,a1,b0,b1)",
                "level_range": "integer m>=2",
                "endpoint_rule": (
                    "1<=a0<a1<=2^m-1 and 1<=b0<b1<=2^m-1"
                ),
                "represented_closed_box": (
                    "[a0/2^m,a1/2^m] x [b0/2^m,b1/2^m]"
                ),
                "primitive_rule": (
                    "at least one of a0,a1,b0,b1 is odd; equivalently the "
                    "common denominator 2^m is minimal"
                ),
                "per_axis_primitive_condition_required": False,
                "lexicographic_order": "(m,a0,a1,b0,b1), skipping all-even rows",
                "I_m": "binom(2^m-1,2)",
                "all_rows_at_level_m": "I_m^2",
                "nonprimitive_rows_at_level_m": "I_(m-1)^2",
                "primitive_rows_at_level_m": "I_m^2-I_(m-1)^2",
                "level_offset": "I_(m-1)^2",
                "level_offset_proof": (
                    "sum_{k=2}^{m-1}(I_k^2-I_(k-1)^2)=I_(m-1)^2"
                ),
                "global_rank": (
                    "I_(m-1)^2 plus lex ordinal among primitive level-m rows"
                ),
                "executable_functions": ["rank_2d", "unrank_2d"],
            },
            "one_dimensional": {
                "row_schema": "(m,a0,a1)",
                "level_range": "integer m>=2",
                "endpoint_rule": "1<=a0<a1<=2^m-1",
                "represented_closed_interval": "[a0/2^m,a1/2^m]",
                "primitive_rule": "at least one of a0,a1 is odd",
                "lexicographic_order": "(m,a0,a1), skipping all-even rows",
                "all_rows_at_level_m": "I_m",
                "nonprimitive_rows_at_level_m": "I_(m-1)",
                "primitive_rows_at_level_m": "I_m-I_(m-1)",
                "level_offset": "I_(m-1)",
                "level_offset_proof": (
                    "sum_{k=2}^{m-1}(I_k-I_(k-1))=I_(m-1)"
                ),
                "global_rank": (
                    "I_(m-1) plus lex ordinal among primitive level-m rows"
                ),
                "executable_functions": ["rank_1d", "unrank_1d"],
                "Round35_leaf_r_coordinate_frozen_by_historical_artifact": False,
                "Round35_source_interval_rank_recovered": False,
            },
            "bijection_scope": (
                "all nonempty closed rational-dyadic boxes compactly contained "
                "in (0,1)^2, and the analogous 1D intervals, each exactly once"
            ),
        },
        "executable_test_ledger": {
            "small_level_exhaustive": small,
            "invalid_rows": invalid,
            "large_2d_rank_unrank_fixtures": fixtures_2d,
            "large_1d_rank_unrank_fixtures": fixtures_1d,
            "large_2d_fixture_count": len(fixtures_2d),
            "large_1d_fixture_count": len(fixtures_1d),
            "all_large_fixture_roundtrips_exact": True,
        },
        "round136_contained_basis_witness": witness,
        "strict_nonpromotion": {
            "historical_Round27_canonical_component_rank": None,
            "historical_Round27_c24_component_id": None,
            "Round35_source_interval_rank": None,
            "Round35_r_coordinate_normalization": None,
            "Round35_image_recut_rank": None,
            "Round35_rn_restriction_id": None,
            "Round50_owner_key_count": 0,
            "Round54_t54_token_count": 0,
            "Round67_q_j_output_count": 0,
            "gate5_global_maturity": "10/18",
            "global_complete_18_field_block_count": 0,
            "complete_18_field_block_count": 0,
            "Gate5": "NOT_CERTIFIED",
            "CM2": "NO-GO_FOR_CLAIM",
        },
        "count_ledger": {
            "source_core_normalization_row_count": len(normalizations),
            "exhaustive_small_2d_row_count":
                small["exhaustive_2d_row_count"],
            "exhaustive_small_1d_row_count":
                small["exhaustive_1d_row_count"],
            "large_2d_fixture_count": len(fixtures_2d),
            "large_1d_fixture_count": len(fixtures_1d),
            "round136_contained_basis_witness_count": 1,
            "historical_Round27_c24_component_id_count": 0,
            "Round35_rn_restriction_id_count": 0,
            "Round50_owner_key_count": 0,
            "Round67_q_j_output_count": 0,
            "global_complete_18_field_block_count": 0,
        },
        "strict_scope": (
            "a new seed-independent exact affine normalization and executable "
            "rational-dyadic basis rank/unrank contract, plus one contained "
            "basis witness inside the Round136 positive-area source box"
        ),
        "strict_nonclaims": [
            "the new enumeration is not claimed equal to the unnamed historical Round27 enumeration",
            "the contained witness rank is only an upper bound under the new v1 contract",
            "no least component rank is computed because earlier basis boxes are not excluded",
            "the noncanonical witness locator does not identify or deduplicate a full component",
            "no historical c24-component identifier is minted",
            "the Round35 leaf r coordinate and interval enumeration remain unfrozen",
            "no Round35 rn-restriction, owner, t54 token, Omega_j or q_j is materialized",
            "no Gate5 field, Gate5 block or CM2 claim is promoted",
        ],
    }
    require(
        result["strict_nonpromotion"]["gate5_global_maturity"] == "10/18"
        and result["strict_nonpromotion"]["global_complete_18_field_block_count"] == 0
        and result["strict_nonpromotion"]["CM2"] == "NO-GO_FOR_CLAIM",
        "global safety boundary",
    )
    result = json.loads(json.dumps(result, sort_keys=True))
    return {"schema": SCHEMA, "result": result, "result_sha256": digest(result)}


def write_atomic(path: Path, value: dict[str, Any]) -> None:
    require(not path.is_symlink(), "output symlink")
    resolved = path.resolve()
    protected = {
        Path(__file__).resolve(),
        *((HERE / name).resolve() for name in PINS),
    }
    require(resolved not in protected, "output aliases protected input")
    require(
        resolved.name not in {"", ".", ".."}
        and resolved.parent.is_dir()
        and not path.parent.is_symlink(),
        "safe output directory",
    )
    if path.exists():
        metadata = path.lstat()
        require(
            stat.S_ISREG(metadata.st_mode)
            and metadata.st_nlink == 1
            and not path.is_symlink(),
            "safe existing output",
        )
        require(
            all(not os.path.samefile(path, item) for item in protected),
            "output hardlink aliases protected input",
        )
    payload = json.dumps(
        value,
        indent=2,
        sort_keys=True,
        ensure_ascii=False,
        allow_nan=False,
    ) + "\n"
    descriptor, temporary = tempfile.mkstemp(
        prefix=f".{resolved.name}.",
        suffix=".tmp",
        dir=resolved.parent,
    )
    temporary_path = Path(temporary)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8", newline="\n") as handle:
            handle.write(payload)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary_path, resolved)
    finally:
        if temporary_path.exists():
            temporary_path.unlink()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=OUTPUT)
    args = parser.parse_args()
    envelope = build()
    write_atomic(args.output, envelope)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
