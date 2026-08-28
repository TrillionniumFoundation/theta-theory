#!/usr/bin/env python3
"""Independent fail-closed verifier for the Round137 dyadic-rank contract.

The Round137 producer is byte pinned but is never imported or executed.  This
verifier independently reconstructs the affine source-core normalizations,
the common-denominator primitive dyadic enumeration, exact one- and
two-dimensional rank/unrank maps, exhaustive small levels, large fixtures,
and the contained Round136 witness.  The historical Round27/35 identifiers,
owner fields, q_j fields, Gate5, and CM2 remain explicitly unpromoted.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import math
import os
import stat
import sys
import tempfile
from fractions import Fraction as Q
from pathlib import Path
from typing import Any, Callable

import cm2_gate25_physical_return_core_registry_cert as core_registry


if hasattr(sys, "set_int_max_str_digits"):
    # The independently reconstructed public upper-bound rank has 4586 digits.
    sys.set_int_max_str_digits(0)


HERE = Path(__file__).resolve().parent
VERIFIER = Path(__file__).resolve()
PRODUCER = (
    HERE / "cm2_round137_seed_independent_dyadic_basis_rank_contract.py"
)
CERTIFICATE = (
    HERE
    / "cm2-round137-seed-independent-dyadic-basis-rank-contract-2026-07-24.json"
)
OUTPUT = (
    HERE
    / "cm2-round137-seed-independent-dyadic-basis-rank-contract-verification-2026-07-24.json"
)

CERTIFICATE_SCHEMA = (
    "cm2.round137.seed-independent-dyadic-basis-rank-contract.v1"
)
VERIFICATION_SCHEMA = (
    "cm2.round137.seed-independent-dyadic-basis-rank-contract-verification.v1"
)
PRODUCER_SHA256 = (
    "81974ada469f8f24299d7790e16f6380f58b38df151ee67704695aa81c0d08ac"
)
CERTIFICATE_SHA256 = (
    "06918b7bbfdeed9bda41a1220a25b630df6eaaa5f06024757f25a8c9fe7b88bf"
)
CERTIFICATE_RESULT_SHA256 = (
    "7517e103dd2c22371892f1b9e560ac886a8bf4a8ad96604cab5d6702d1d8f804"
)
WITNESS_RANK_DECIMAL_SHA256 = (
    "c6f579730386b27b3ccedc3c4159be4a8f42dfbcedceef52004d3a8b0a99fd4b"
)
WITNESS_LEVEL = 3809
WITNESS_RANK_DECIMAL_DIGITS = 4586
MAX_CERTIFICATE_BYTES = 200_000
MAX_DEPENDENCY_BYTES = 4_000_000
MAX_JSON_INTEGER_DIGITS = 2048

CORE_MODULE = HERE / "cm2_gate25_physical_return_core_registry_cert.py"
CORE_MANIFEST = (
    HERE / "cm2-gate25-physical-return-core-registry-manifest-2026-07-16.json"
)
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
    HERE
    / "cm2-round136-rank3-positive-width-r1056-return-frontier-2026-07-24.json"
)

UPSTREAM_PINS = {
    CORE_MODULE.name:
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


class VerificationError(RuntimeError):
    """Fail-closed parsing, reconstruction, semantic, or path error."""


def require(condition: bool, label: str) -> None:
    if not condition:
        raise VerificationError(label)


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


def qstr(value: Q | int) -> str:
    rational = Q(value)
    return (
        str(rational.numerator)
        if rational.denominator == 1
        else f"{rational.numerator}/{rational.denominator}"
    )


def no_duplicate_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise VerificationError(f"duplicate JSON key:{key}")
        result[key] = value
    return result


def parse_json_integer(token: str) -> int:
    digits = token[1:] if token.startswith("-") else token
    if len(digits) > MAX_JSON_INTEGER_DIGITS:
        raise VerificationError("oversized JSON integer")
    if token == "-0":
        raise VerificationError("negative-zero JSON integer")
    return int(token)


def reject_float(token: str) -> float:
    raise VerificationError(f"floating JSON number:{token[:32]}")


def reject_constant(token: str) -> None:
    raise VerificationError(f"non-finite JSON constant:{token}")


def ensure_unicode_scalars(value: Any) -> None:
    if isinstance(value, str):
        require(
            not any(0xD800 <= ord(character) <= 0xDFFF for character in value),
            "unpaired Unicode surrogate",
        )
    elif isinstance(value, list):
        for item in value:
            ensure_unicode_scalars(item)
    elif isinstance(value, dict):
        for key, item in value.items():
            ensure_unicode_scalars(key)
            ensure_unicode_scalars(item)


def strict_json_bytes(raw: bytes, label: str) -> dict[str, Any]:
    require(len(raw) <= MAX_CERTIFICATE_BYTES, f"JSON byte cap:{label}")
    require(not raw.startswith(b"\xef\xbb\xbf"), f"UTF-8 BOM:{label}")
    try:
        text = raw.decode("utf-8", errors="strict")
        decoder = json.JSONDecoder(
            object_pairs_hook=no_duplicate_pairs,
            parse_int=parse_json_integer,
            parse_float=reject_float,
            parse_constant=reject_constant,
        )
        value, end = decoder.raw_decode(text)
        require(not text[end:].strip(), f"trailing JSON data:{label}")
    except (UnicodeError, ValueError, json.JSONDecodeError) as exc:
        raise VerificationError(f"strict JSON:{label}") from exc
    require(type(value) is dict, f"top-level JSON object:{label}")
    ensure_unicode_scalars(value)
    return value


def strict_json(path: Path) -> dict[str, Any]:
    metadata = path.lstat()
    require(stat.S_ISREG(metadata.st_mode), f"regular JSON file:{path.name}")
    require(metadata.st_nlink == 1, f"single-link JSON file:{path.name}")
    require(not path.is_symlink(), f"JSON symlink:{path.name}")
    return strict_json_bytes(path.read_bytes(), path.name)


def strict_dependency_json(path: Path) -> dict[str, Any]:
    """Duplicate-key/constant-safe parser for pinned legacy dependencies.

    Some historical manifests intentionally contain finite JSON floats, so
    the certificate's no-float contract is not projected backwards onto them.
    """

    metadata = path.lstat()
    require(stat.S_ISREG(metadata.st_mode), f"regular dependency:{path.name}")
    require(metadata.st_nlink == 1, f"single-link dependency:{path.name}")
    require(not path.is_symlink(), f"dependency symlink:{path.name}")
    require(metadata.st_size <= MAX_DEPENDENCY_BYTES, f"dependency byte cap:{path.name}")
    try:
        value = json.loads(
            path.read_text(encoding="utf-8"),
            object_pairs_hook=no_duplicate_pairs,
            parse_int=parse_json_integer,
            parse_constant=reject_constant,
        )
    except (UnicodeError, ValueError, json.JSONDecodeError) as exc:
        raise VerificationError(f"dependency JSON:{path.name}") from exc
    require(type(value) is dict, f"dependency object:{path.name}")
    ensure_unicode_scalars(value)
    return value


def validate_pins() -> None:
    require(
        PRODUCER.is_file()
        and not PRODUCER.is_symlink()
        and sha256(PRODUCER) == PRODUCER_SHA256,
        "Round137 producer byte pin",
    )
    for name, expected in UPSTREAM_PINS.items():
        path = HERE / name
        require(
            path.is_file()
            and not path.is_symlink()
            and path.resolve().parent == HERE
            and sha256(path) == expected,
            f"upstream byte pin:{name}",
        )


# ---------------------------------------------------------------------------
# Independent combinatorial implementation
# ---------------------------------------------------------------------------


def pair_count(level: int) -> int:
    require(type(level) is int and level >= 0, "nonnegative level")
    if level < 2:
        return 0
    points = (1 << level) - 1
    return points * (points - 1) // 2


def validate_pair(level: int, left: int, right: int) -> None:
    require(
        all(type(value) is int for value in (level, left, right)),
        "integer pair row",
    )
    require(level >= 2, "pair level at least two")
    last = (1 << level) - 1
    require(1 <= left < right <= last, "interior ordered pair")


def pair_prefix(level: int, left: int) -> int:
    """Number of pairs whose first endpoint is strictly below ``left``."""
    last = (1 << level) - 1
    earlier = left - 1
    return earlier * last - earlier * (earlier + 1) // 2


def pair_rank(level: int, left: int, right: int) -> int:
    validate_pair(level, left, right)
    return pair_prefix(level, left) + right - left - 1


def pair_unrank(level: int, ordinal: int) -> tuple[int, int]:
    total = pair_count(level)
    require(type(ordinal) is int and 0 <= ordinal < total, "pair ordinal")
    last = (1 << level) - 1
    low, high = 1, last - 1
    while low < high:
        middle = (low + high + 1) // 2
        if pair_prefix(level, middle) <= ordinal:
            low = middle
        else:
            high = middle - 1
    left = low
    right = left + 1 + ordinal - pair_prefix(level, left)
    validate_pair(level, left, right)
    return left, right


def all_even(pair: tuple[int, int]) -> bool:
    return pair[0] % 2 == 0 and pair[1] % 2 == 0


def even_pairs_before(level: int, left: int, right: int) -> int:
    """Count even/even pairs before ``(left,right)`` in full lexicographic order."""
    validate_pair(level, left, right)
    reduced_last = (1 << (level - 1)) - 1
    earlier_even_lefts = (left - 1) // 2
    count = (
        earlier_even_lefts * reduced_last
        - earlier_even_lefts * (earlier_even_lefts + 1) // 2
    )
    if left % 2 == 0:
        count += max(0, (right - 1) // 2 - left // 2)
    return count


def primitive_pair_unrank(level: int, ordinal: int) -> tuple[int, int]:
    total = pair_count(level)
    primitive = total - pair_count(level - 1)
    require(0 <= ordinal < primitive, "primitive-pair ordinal")
    low, high = 0, total - 1
    while low <= high:
        middle = (low + high) // 2
        pair = pair_unrank(level, middle)
        filtered = middle - even_pairs_before(level, *pair)
        if all_even(pair):
            if ordinal < filtered:
                high = middle - 1
            else:
                low = middle + 1
        elif ordinal < filtered:
            high = middle - 1
        elif ordinal > filtered:
            low = middle + 1
        else:
            return pair
    raise VerificationError("primitive-pair unrank")


def validate_1d(row: tuple[int, int, int]) -> None:
    require(type(row) is tuple and len(row) == 3, "1D row arity")
    level, left, right = row
    validate_pair(level, left, right)
    require(left % 2 == 1 or right % 2 == 1, "1D primitive denominator")


def rank_1d(row: tuple[int, int, int]) -> int:
    validate_1d(row)
    level, left, right = row
    local = pair_rank(level, left, right) - even_pairs_before(
        level, left, right
    )
    return pair_count(level - 1) + local


def level_of_1d_rank(rank: int) -> int:
    require(type(rank) is int and rank >= 0, "nonnegative 1D rank")
    low, high = 2, max(2, rank.bit_length() + 2)
    while low < high:
        middle = (low + high) // 2
        if pair_count(middle) > rank:
            high = middle
        else:
            low = middle + 1
    return low


def unrank_1d(rank: int) -> tuple[int, int, int]:
    level = level_of_1d_rank(rank)
    local = rank - pair_count(level - 1)
    pair = primitive_pair_unrank(level, local)
    row = (level, *pair)
    validate_1d(row)
    return row


def validate_2d(row: tuple[int, int, int, int, int]) -> None:
    require(type(row) is tuple and len(row) == 5, "2D row arity")
    level, a0, a1, b0, b1 = row
    validate_pair(level, a0, a1)
    validate_pair(level, b0, b1)
    require(
        any(value % 2 == 1 for value in (a0, a1, b0, b1)),
        "common-denominator primitive",
    )


def a_block_start(level: int, a_ordinal: int) -> int:
    total = pair_count(level)
    even = pair_count(level - 1)
    a_pair = pair_unrank(level, a_ordinal)
    return (
        a_ordinal * total
        - even_pairs_before(level, *a_pair) * even
    )


def rank_2d(row: tuple[int, int, int, int, int]) -> int:
    validate_2d(row)
    level, a0, a1, b0, b1 = row
    total = pair_count(level)
    even = pair_count(level - 1)
    a_ordinal = pair_rank(level, a0, a1)
    before_a = a_ordinal * total - even_pairs_before(
        level, a0, a1
    ) * even
    b_ordinal = pair_rank(level, b0, b1)
    within = (
        b_ordinal
        if not all_even((a0, a1))
        else b_ordinal - even_pairs_before(level, b0, b1)
    )
    return even * even + before_a + within


def level_of_2d_rank(rank: int) -> int:
    require(type(rank) is int and rank >= 0, "nonnegative 2D rank")
    low, high = 2, max(2, rank.bit_length() + 2)
    while low < high:
        middle = (low + high) // 2
        if pair_count(middle) ** 2 > rank:
            high = middle
        else:
            low = middle + 1
    return low


def unrank_2d(rank: int) -> tuple[int, int, int, int, int]:
    level = level_of_2d_rank(rank)
    total = pair_count(level)
    even = pair_count(level - 1)
    local = rank - even * even
    low, high = 0, total - 1
    while low <= high:
        middle = (low + high) // 2
        a_pair = pair_unrank(level, middle)
        start = (
            middle * total
            - even_pairs_before(level, *a_pair) * even
        )
        size = total - even if all_even(a_pair) else total
        if local < start:
            high = middle - 1
        elif local >= start + size:
            low = middle + 1
        else:
            b_local = local - start
            b_pair = (
                primitive_pair_unrank(level, b_local)
                if all_even(a_pair)
                else pair_unrank(level, b_local)
            )
            row = (level, *a_pair, *b_pair)
            validate_2d(row)
            return row
    raise VerificationError("2D unrank")


def encode_integer(value: int) -> dict[str, Any]:
    require(type(value) is int and value >= 0, "encoded integer")
    decimal = str(value)
    return {
        "decimal": decimal,
        "hexadecimal": "0x" + format(value, "x"),
        "bit_length": value.bit_length(),
        "decimal_digit_count": len(decimal),
        "sha256_of_decimal": hashlib.sha256(
            decimal.encode("ascii")
        ).hexdigest(),
    }


# ---------------------------------------------------------------------------
# Independent expected-result reconstruction
# ---------------------------------------------------------------------------


def core_payload(core: core_registry.Core) -> dict[str, Any]:
    return {
        "chart_id": core.chart_id,
        "t": [qstr(core.t0), qstr(core.t1)],
        "p": [qstr(core.p0), qstr(core.p1)],
        "target_id": core.target_id,
        "crossings": list(core.crossings),
    }


def core_id(core: core_registry.Core) -> str:
    return "core:" + digest(core_payload(core))


def normalization_rows() -> list[dict[str, Any]]:
    cores = tuple(core_registry.physical_cores())
    require(len(cores) == 24, "24 physical source cores")
    rows: list[dict[str, Any]] = []
    identifiers: set[str] = set()
    for index, core in enumerate(cores):
        identifier = core_id(core)
        require(identifier not in identifiers, "unique physical core IDs")
        identifiers.add(identifier)
        dt, dp = core.t1 - core.t0, core.p1 - core.p0
        require(dt > 0 and dp > 0, "positive core rectangle")
        row = {
            "source_core_index": index,
            "source_core_id": identifier,
            "chart_id": core.chart_id,
            "target_id": core.target_id,
            "family": core.family,
            "t_bounds": [qstr(core.t0), qstr(core.t1)],
            "p_bounds": [qstr(core.p0), qstr(core.p1)],
            "normalization": {
                "u": f"(t-({qstr(core.t0)}))/({qstr(dt)})",
                "v": f"(p-({qstr(core.p0)}))/({qstr(dp)})",
                "inverse_t": f"({qstr(core.t0)})+u*({qstr(dt)})",
                "inverse_p": f"({qstr(core.p0)})+v*({qstr(dp)})",
                "orientation": "increasing_in_each_coordinate",
                "open_core_maps_exactly_to": "(0,1)^2",
            },
        }
        row["row_sha256"] = digest(row)
        rows.append(row)
    return rows


def exhaustive_small() -> dict[str, Any]:
    seen_1d_values: set[tuple[Q, Q]] = set()
    seen_2d_values: set[tuple[Q, Q, Q, Q]] = set()
    seen_1d_ranks: set[int] = set()
    seen_2d_ranks: set[int] = set()
    levels: list[dict[str, Any]] = []
    total_1d = total_2d = 0
    for level in range(2, 5):
        last = (1 << level) - 1
        pairs = [
            (left, right)
            for left in range(1, last)
            for right in range(left + 1, last + 1)
        ]
        current = pair_count(level)
        previous = pair_count(level - 1)
        require(len(pairs) == current, "small pair count")
        count_1d = count_2d = 0
        level_1d_ranks: list[int] = []
        level_2d_ranks: list[int] = []
        for left, right in pairs:
            if all_even((left, right)):
                continue
            row = (level, left, right)
            rank = rank_1d(row)
            require(unrank_1d(rank) == row, "small 1D roundtrip")
            value = (Q(left, 1 << level), Q(right, 1 << level))
            require(
                rank not in seen_1d_ranks and value not in seen_1d_values,
                "small 1D uniqueness",
            )
            seen_1d_ranks.add(rank)
            seen_1d_values.add(value)
            level_1d_ranks.append(rank)
            count_1d += 1
        for a0, a1 in pairs:
            for b0, b1 in pairs:
                row = (level, a0, a1, b0, b1)
                if all(value % 2 == 0 for value in row[1:]):
                    continue
                rank = rank_2d(row)
                require(unrank_2d(rank) == row, "small 2D roundtrip")
                value = (
                    Q(a0, 1 << level),
                    Q(a1, 1 << level),
                    Q(b0, 1 << level),
                    Q(b1, 1 << level),
                )
                require(
                    rank not in seen_2d_ranks and value not in seen_2d_values,
                    "small 2D uniqueness",
                )
                seen_2d_ranks.add(rank)
                seen_2d_values.add(value)
                level_2d_ranks.append(rank)
                count_2d += 1
        require(
            count_1d == current - previous
            and count_2d == current * current - previous * previous,
            "small primitive counts",
        )
        require(
            min(level_1d_ranks) == previous
            and max(level_1d_ranks) == current - 1,
            "small 1D rank interval",
        )
        require(
            min(level_2d_ranks) == previous * previous
            and max(level_2d_ranks) == current * current - 1,
            "small 2D rank interval",
        )
        total_1d += count_1d
        total_2d += count_2d
        levels.append({
            "level_m": level,
            "I_m": current,
            "I_m_minus_1": previous,
            "primitive_2d_row_count": count_2d,
            "primitive_2d_level_offset": previous * previous,
            "primitive_1d_row_count": count_1d,
            "primitive_1d_level_offset": previous,
            "2d_last_rank_inclusive": current * current - 1,
            "1d_last_rank_inclusive": current - 1,
        })
    require(total_1d == 105 and total_2d == 11025, "small telescope")
    return {
        "exhaustive_through_level": 4,
        "level_rows": levels,
        "exhaustive_2d_row_count": total_2d,
        "exhaustive_1d_row_count": total_1d,
        "all_rank_unrank_roundtrips_exact": True,
        "all_global_ranks_unique": True,
        "all_cross_level_rational_boxes_unique": True,
        "level_offsets_exact": True,
        "telescoping_counts_exact": True,
    }


def fixture_1d(row: tuple[int, int, int]) -> dict[str, Any]:
    rank = rank_1d(row)
    require(unrank_1d(rank) == row, "large 1D roundtrip")
    return {"row": list(row), "rank": encode_integer(rank), "roundtrip_exact": True}


def fixture_2d(row: tuple[int, int, int, int, int]) -> dict[str, Any]:
    rank = rank_2d(row)
    require(unrank_2d(rank) == row, "large 2D roundtrip")
    return {"row": list(row), "rank": encode_integer(rank), "roundtrip_exact": True}


def invalid_tests() -> dict[str, Any]:
    invalid_1d = [
        (1, 1, 2),
        (2, 0, 1),
        (2, 1, 1),
        (2, 1, 4),
        (3, 2, 4),
    ]
    invalid_2d = [
        (1, 1, 2, 1, 2),
        (2, 0, 1, 1, 2),
        (2, 1, 1, 1, 2),
        (2, 1, 4, 1, 2),
        (3, 2, 4, 2, 6),
    ]
    rejected_1d = rejected_2d = 0
    for row in invalid_1d:
        try:
            rank_1d(row)
        except VerificationError:
            rejected_1d += 1
    for row in invalid_2d:
        try:
            rank_2d(row)
        except VerificationError:
            rejected_2d += 1
    require(
        rejected_1d == len(invalid_1d)
        and rejected_2d == len(invalid_2d),
        "invalid rows rejected",
    )
    return {
        "invalid_2d_fixture_count": len(invalid_2d),
        "invalid_2d_rejected_count": rejected_2d,
        "invalid_1d_fixture_count": len(invalid_1d),
        "invalid_1d_rejected_count": rejected_1d,
        "boundary_order_and_nonprimitive_cases_fail_closed": True,
    }


def first_two_grid_points(
    lower: Q, upper: Q, level: int
) -> tuple[int, int] | None:
    require(Q(0) < lower < upper < Q(1), "normalized open interval")
    denominator = 1 << level
    first = lower.numerator * denominator // lower.denominator + 1
    second = first + 1
    if (
        1 <= first < second <= denominator - 1
        and Q(first, denominator) > lower
        and Q(second, denominator) < upper
    ):
        return first, second
    return None


def first_contained_row(
    u0: Q, u1: Q, v0: Q, v1: Q
) -> tuple[int, int, int, int, int]:
    for level in range(2, WITNESS_LEVEL + 1):
        u_pair = first_two_grid_points(u0, u1, level)
        v_pair = first_two_grid_points(v0, v1, level)
        if u_pair is not None and v_pair is not None:
            row = (level, *u_pair, *v_pair)
            validate_2d(row)
            return row
    raise VerificationError("contained witness not found through frozen level")


def load_dependencies() -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    validate_pins()
    core_manifest = strict_dependency_json(CORE_MANIFEST)
    round27 = strict_dependency_json(ROUND27)
    round35 = strict_dependency_json(ROUND35)
    round136 = strict_dependency_json(ROUND136)
    require(
        core_manifest.get("schema")
        == "cm2.gate25.physical-return-core-registry.manifest.v1",
        "core manifest schema",
    )
    require(
        round27.get("schema")
        == "cm2.gate34.round27-arbitrary-n-path-schema.manifest.v1",
        "Round27 schema",
    )
    require(
        round35.get("schema")
        == "cm2.gate45.round35-arbitrary-rn-common-carrier.v1.manifest.v1",
        "Round35 schema",
    )
    require(
        set(round136) == {"schema", "result", "result_sha256"}
        and round136["schema"]
        == "cm2.round136.rank3-positive-width-r1056-return-frontier.v1"
        and digest(round136["result"]) == round136["result_sha256"],
        "Round136 closed envelope",
    )
    component = round27["result"]["canonical_regular_connected_component_schema"]
    parent = round35["result"]["arbitrary_Rn_parent_W_Borel_registry"]
    require(
        component["component_coordinates_and_nonempty_ranks_enumerated"] is False
        and "fixed bijective enumeration" in component["canonical_component_rank"],
        "Round27 historical frontier",
    )
    require(
        parent["nonempty_component_coordinates_enumerated"] is False
        and "least rational-dyadic interval basis index"
        in parent["source_interval_rank"],
        "Round35 historical frontier",
    )
    r136 = round136["result"]
    require(
        r136["actual_R1056_return_summary"]["first_return_depth"] == 1056
        and r136["actual_R1056_return_summary"]["source_box_positive_area"] is True
        and r136["strict_nonpromotion"]["c24_component_id"] is None
        and r136["strict_nonpromotion"]["Round35_rn_restriction_id"] is None,
        "Round136 local frontier",
    )
    return round27, round35, round136


def contained_witness(
    round136: dict[str, Any],
    normalizations: list[dict[str, Any]],
) -> dict[str, Any]:
    r136 = round136["result"]
    source_box = r136["rational_source_box_construction"][
        "actual_rational_source_box"
    ]
    source_index = source_box["source_core_index"]
    require(source_index == 14, "Round136 source core index")
    cores = tuple(core_registry.physical_cores())
    core = cores[source_index]
    identifier = core_id(core)
    require(
        identifier
        == normalizations[source_index]["source_core_id"]
        == r136["actual_R1056_return_summary"]["source_core_id"],
        "Round136 normalized core identity",
    )
    t0, t1 = (Q(value) for value in source_box["t"])
    p0, p1 = (Q(value) for value in source_box["p"])
    require(
        core.t0 < t0 < t1 < core.t1
        and core.p0 < p0 < p1 < core.p1,
        "Round136 box inside core",
    )
    u0 = (t0 - core.t0) / (core.t1 - core.t0)
    u1 = (t1 - core.t0) / (core.t1 - core.t0)
    v0 = (p0 - core.p0) / (core.p1 - core.p0)
    v1 = (p1 - core.p0) / (core.p1 - core.p0)
    row = first_contained_row(u0, u1, v0, v1)
    require(row[0] == WITNESS_LEVEL, "minimal contained witness level")
    denominator = 1 << row[0]
    require(
        u0 < Q(row[1], denominator) < Q(row[2], denominator) < u1
        and v0 < Q(row[3], denominator) < Q(row[4], denominator) < v1,
        "contained witness strict closure",
    )
    require(
        first_two_grid_points(u0, u1, row[0] - 1) is None
        or first_two_grid_points(v0, v1, row[0] - 1) is None,
        "previous level lacks a contained consecutive pair",
    )
    rank = rank_2d(row)
    encoded = encode_integer(rank)
    require(
        encoded["decimal_digit_count"] == WITNESS_RANK_DECIMAL_DIGITS
        and encoded["sha256_of_decimal"] == WITNESS_RANK_DECIMAL_SHA256,
        "contained witness upper-bound rank fixture",
    )
    locator_payload = {
        "contract": "round137-dyadic-basis-enumeration-v1",
        "source_core_id": identifier,
        "return_depth": 1056,
        "round136_local_return_cylinder_id":
            r136["actual_R1056_return_summary"]["local_return_cylinder_id"],
        "round136_complete_candidate_path_tuple_sha256":
            r136["actual_R1056_return_summary"][
                "Round27_compatible_complete_candidate_path_tuple_sha256"
            ],
        "contained_basis_row": list(row),
        "contained_basis_rank_decimal": str(rank),
    }
    locator_digest = digest(locator_payload)
    return {
        "source_core_index": source_index,
        "source_core_id": identifier,
        "round136_local_return_cylinder_id":
            r136["actual_R1056_return_summary"]["local_return_cylinder_id"],
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
        "contained_primitive_basis_denominator_power": row[0],
        "contained_primitive_basis_rank": encoded,
        "contained_basis_closure_strictly_inside_round136_box": True,
        "minimal_level_with_two_strict_grid_points_in_each_coordinate": True,
        "lex_first_consecutive_pairs_at_that_level": True,
        "component_witness_locator_id":
            "round137-component-witness-locator:" + locator_digest,
        "component_witness_locator_payload_sha256": locator_digest,
        "locator_is_noncanonical_and_does_not_deduplicate_components": True,
        "round137_v1_component_rank_upper_bound_available": True,
        "round137_v1_component_rank_upper_bound": encoded,
        "upper_bound_reason": (
            "the connected regular R_1056 component containing the strict "
            "Round136 source box also contains this closed dyadic basis box"
        ),
        "round137_v1_least_component_rank_computed": False,
        "historical_Round27_canonical_component_rank": None,
        "historical_Round27_c24_component_id": None,
        "projection_to_Round35_restriction_id": None,
    }


def build_expected() -> dict[str, Any]:
    round27, round35, round136 = load_dependencies()
    normalizations = normalization_rows()
    small = exhaustive_small()
    invalid = invalid_tests()
    fixtures_2d = [
        fixture_2d((16, 1, 2, 3, 4)),
        fixture_2d((64, 2, 4, 2, 3)),
        fixture_2d((257, 2**256 - 2, 2**256 - 1, 1, 2)),
    ]
    fixtures_1d = [
        fixture_1d((16, 1, 2)),
        fixture_1d((64, 2, 3)),
        fixture_1d((257, 2**256 - 2, 2**256 - 1)),
    ]
    witness = contained_witness(round136, normalizations)
    result = {
        "status": "CERTIFIED_PROSPECTIVE_SEED_INDEPENDENT_DYADIC_BASIS_RANK_CONTRACT",
        "provenance": {
            "producer_sha256": PRODUCER_SHA256,
            "dependency_sha256": dict(sorted(UPSTREAM_PINS.items())),
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
            "exact_map":
                "u=(t-t0)/(t1-t0), v=(p-p0)/(p1-p0) for each frozen core",
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
                "endpoint_rule":
                    "1<=a0<a1<=2^m-1 and 1<=b0<b1<=2^m-1",
                "represented_closed_box":
                    "[a0/2^m,a1/2^m] x [b0/2^m,b1/2^m]",
                "primitive_rule": (
                    "at least one of a0,a1,b0,b1 is odd; equivalently the "
                    "common denominator 2^m is minimal"
                ),
                "per_axis_primitive_condition_required": False,
                "lexicographic_order":
                    "(m,a0,a1,b0,b1), skipping all-even rows",
                "I_m": "binom(2^m-1,2)",
                "all_rows_at_level_m": "I_m^2",
                "nonprimitive_rows_at_level_m": "I_(m-1)^2",
                "primitive_rows_at_level_m": "I_m^2-I_(m-1)^2",
                "level_offset": "I_(m-1)^2",
                "level_offset_proof":
                    "sum_{k=2}^{m-1}(I_k^2-I_(k-1)^2)=I_(m-1)^2",
                "global_rank":
                    "I_(m-1)^2 plus lex ordinal among primitive level-m rows",
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
                "level_offset_proof":
                    "sum_{k=2}^{m-1}(I_k-I_(k-1))=I_(m-1)",
                "global_rank":
                    "I_(m-1) plus lex ordinal among primitive level-m rows",
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
            "exhaustive_small_2d_row_count": small["exhaustive_2d_row_count"],
            "exhaustive_small_1d_row_count": small["exhaustive_1d_row_count"],
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
    return json.loads(json.dumps(result, sort_keys=True))


def evaluate_document(document: dict[str, Any], expected: dict[str, Any]) -> None:
    require(
        set(document) == {"schema", "result", "result_sha256"},
        "closed certificate envelope",
    )
    require(document["schema"] == CERTIFICATE_SCHEMA, "certificate schema")
    require(type(document["result"]) is dict, "certificate result object")
    require(
        document["result_sha256"] == digest(document["result"]),
        "certificate result digest",
    )
    require(document["result_sha256"] == CERTIFICATE_RESULT_SHA256, "result pin")
    witness = document["result"]["round136_contained_basis_witness"]
    expected_rank = expected["round136_contained_basis_witness"][
        "contained_primitive_basis_rank"
    ]
    for encoded in (
        witness["contained_primitive_basis_rank"],
        witness["round137_v1_component_rank_upper_bound"],
    ):
        require(
            type(encoded) is dict
            and set(encoded)
            == {
                "decimal",
                "hexadecimal",
                "bit_length",
                "decimal_digit_count",
                "sha256_of_decimal",
            },
            "public upper-bound rank schema",
        )
        decimal = encoded["decimal"]
        hexadecimal = encoded["hexadecimal"]
        require(
            type(decimal) is str
            and len(decimal) == WITNESS_RANK_DECIMAL_DIGITS
            and decimal.isascii()
            and decimal.isdigit()
            and not decimal.startswith("0"),
            "public upper-bound decimal syntax",
        )
        require(
            type(hexadecimal) is str
            and hexadecimal.startswith("0x")
            and len(hexadecimal)
            == 2 + (expected_rank["bit_length"] + 3) // 4
            and all(
                character in "0123456789abcdef"
                for character in hexadecimal[2:]
            )
            and not hexadecimal.startswith("0x0"),
            "public upper-bound hexadecimal syntax",
        )
        require(
            type(encoded["bit_length"]) is int
            and encoded["bit_length"] == expected_rank["bit_length"]
            and type(encoded["decimal_digit_count"]) is int
            and encoded["decimal_digit_count"] == WITNESS_RANK_DECIMAL_DIGITS
            and encoded["sha256_of_decimal"]
            == hashlib.sha256(decimal.encode("ascii")).hexdigest()
            == WITNESS_RANK_DECIMAL_SHA256,
            "public upper-bound rank metadata",
        )
    require(document["result"] == expected, "independent full-result reconstruction")


# ---------------------------------------------------------------------------
# Adversarial tests
# ---------------------------------------------------------------------------


def resign(document: dict[str, Any]) -> None:
    document["result_sha256"] = digest(document["result"])


def set_path(root: dict[str, Any], path: tuple[Any, ...], value: Any) -> None:
    target: Any = root
    for key in path[:-1]:
        target = target[key]
    target[path[-1]] = value


def semantic_mutations(
    certificate: dict[str, Any], expected: dict[str, Any]
) -> list[str]:
    mutations: list[tuple[str, Callable[[dict[str, Any]], None]]] = []

    def simple(label: str, path: tuple[Any, ...], value: Any) -> None:
        def mutate(document: dict[str, Any]) -> None:
            set_path(document, path, value)
            resign(document)
        mutations.append((label, mutate))

    simple("status altered", ("result", "status"), "PASS")
    simple(
        "producer pin altered",
        ("result", "provenance", "producer_sha256"),
        "0" * 64,
    )
    simple(
        "dependency pin altered",
        (
            "result",
            "provenance",
            "dependency_sha256",
            ROUND136.name,
        ),
        "0" * 64,
    )
    simple("seed independence erased", ("result", "provenance", "seed_independent"), False)
    simple("append-only erased", ("result", "provenance", "append_only"), False)
    simple(
        "historical coordinates promoted",
        (
            "result",
            "historical_schema_audit",
            "historical_coordinate_normalization_frozen",
        ),
        True,
    )
    simple(
        "historical order promoted",
        (
            "result",
            "historical_schema_audit",
            "historical_enumeration_order_frozen",
        ),
        True,
    )
    simple(
        "historical labels recovered",
        (
            "result",
            "historical_schema_audit",
            "new_v1_recovers_historical_numeric_labels",
        ),
        True,
    )
    simple(
        "normalization row count altered",
        (
            "result",
            "source_core_affine_normalization_contract",
            "normalization_row_count",
        ),
        23,
    )
    simple(
        "normalization group hash altered",
        (
            "result",
            "source_core_affine_normalization_contract",
            "normalization_rows_sha256",
        ),
        "0" * 64,
    )
    simple(
        "normalization orientation altered",
        (
            "result",
            "source_core_affine_normalization_contract",
            "orientation",
        ),
        "decreasing",
    )
    for index in (0, 14, 23):
        def mutate_normalization(
            document: dict[str, Any], selected: int = index
        ) -> None:
            contract = document["result"][
                "source_core_affine_normalization_contract"
            ]
            row = contract["normalization_rows"][selected]
            row["target_id"] += "-tampered"
            body = {key: value for key, value in row.items() if key != "row_sha256"}
            row["row_sha256"] = digest(body)
            contract["normalization_rows_sha256"] = digest(
                contract["normalization_rows"]
            )
            resign(document)
        mutations.append((f"normalization row altered:{index}", mutate_normalization))
    simple(
        "index origin altered",
        ("result", "dyadic_basis_enumeration_v1", "index_origin"),
        "one_based",
    )
    simple(
        "2D primitive rule altered",
        (
            "result",
            "dyadic_basis_enumeration_v1",
            "two_dimensional",
            "per_axis_primitive_condition_required",
        ),
        True,
    )
    simple(
        "2D offset altered",
        (
            "result",
            "dyadic_basis_enumeration_v1",
            "two_dimensional",
            "level_offset",
        ),
        "I_m^2",
    )
    simple(
        "1D offset altered",
        (
            "result",
            "dyadic_basis_enumeration_v1",
            "one_dimensional",
            "level_offset",
        ),
        "I_m",
    )
    simple(
        "small exhaustive level altered",
        (
            "result",
            "executable_test_ledger",
            "small_level_exhaustive",
            "exhaustive_through_level",
        ),
        3,
    )
    simple(
        "small 2D count altered",
        (
            "result",
            "executable_test_ledger",
            "small_level_exhaustive",
            "exhaustive_2d_row_count",
        ),
        11024,
    )
    simple(
        "small 1D count altered",
        (
            "result",
            "executable_test_ledger",
            "small_level_exhaustive",
            "exhaustive_1d_row_count",
        ),
        104,
    )
    simple(
        "small offset altered",
        (
            "result",
            "executable_test_ledger",
            "small_level_exhaustive",
            "level_rows",
            2,
            "primitive_2d_level_offset",
        ),
        440,
    )
    simple(
        "invalid rejection altered",
        (
            "result",
            "executable_test_ledger",
            "invalid_rows",
            "invalid_2d_rejected_count",
        ),
        4,
    )
    simple(
        "large fixture count altered",
        ("result", "executable_test_ledger", "large_2d_fixture_count"),
        2,
    )
    for dimension, selected in (("1d", 0), ("1d", 2), ("2d", 0), ("2d", 2)):
        key = f"large_{dimension}_rank_unrank_fixtures"
        simple(
            f"large {dimension} fixture rank altered:{selected}",
            ("result", "executable_test_ledger", key, selected, "rank", "decimal"),
            "0",
        )
    witness_root = ("result", "round136_contained_basis_witness")
    simple("witness source index altered", witness_root + ("source_core_index",), 13)
    simple("witness return depth altered", witness_root + ("return_depth",), 1055)
    simple(
        "witness denominator level altered",
        witness_root + ("contained_primitive_basis_denominator_power",),
        3808,
    )
    simple(
        "witness row level altered",
        witness_root + ("contained_primitive_basis_row", 0),
        3808,
    )
    simple(
        "witness row endpoint altered",
        witness_root + ("contained_primitive_basis_row", 1),
        1,
    )
    simple(
        "witness rank decimal altered",
        witness_root + ("contained_primitive_basis_rank", "decimal"),
        "1",
    )
    simple(
        "witness rank hash altered",
        witness_root + ("contained_primitive_basis_rank", "sha256_of_decimal"),
        "0" * 64,
    )
    simple(
        "witness digit count altered",
        witness_root + ("contained_primitive_basis_rank", "decimal_digit_count"),
        4585,
    )
    simple(
        "witness strict containment erased",
        witness_root + ("contained_basis_closure_strictly_inside_round136_box",),
        False,
    )
    simple(
        "witness minimality erased",
        witness_root + ("minimal_level_with_two_strict_grid_points_in_each_coordinate",),
        False,
    )
    simple(
        "witness locator canonicalized",
        witness_root + ("locator_is_noncanonical_and_does_not_deduplicate_components",),
        False,
    )
    simple(
        "least rank invented",
        witness_root + ("round137_v1_least_component_rank_computed",),
        True,
    )
    simple(
        "historical witness rank invented",
        witness_root + ("historical_Round27_canonical_component_rank",),
        0,
    )
    simple(
        "historical witness ID invented",
        witness_root + ("historical_Round27_c24_component_id",),
        "c24-component:invented",
    )
    simple(
        "Round35 witness projection invented",
        witness_root + ("projection_to_Round35_restriction_id",),
        "rn-restriction:invented",
    )
    promotions = [
        ("historical canonical rank", "historical_Round27_canonical_component_rank", 0),
        ("historical component ID", "historical_Round27_c24_component_id", "c24-component:x"),
        ("Round35 source rank", "Round35_source_interval_rank", 0),
        ("Round35 coordinate", "Round35_r_coordinate_normalization", "r"),
        ("Round35 image rank", "Round35_image_recut_rank", 0),
        ("Round35 restriction", "Round35_rn_restriction_id", "rn-restriction:x"),
        ("owner", "Round50_owner_key_count", 1),
        ("t54", "Round54_t54_token_count", 1),
        ("q_j", "Round67_q_j_output_count", 1),
        ("global maturity", "gate5_global_maturity", "18/18"),
        ("global block", "global_complete_18_field_block_count", 1),
        ("complete block", "complete_18_field_block_count", 1),
        ("Gate5", "Gate5", "CERTIFIED"),
        ("CM2", "CM2", "GO_FOR_CLAIM"),
    ]
    for label, key, value in promotions:
        simple(
            f"nonpromotion violated:{label}",
            ("result", "strict_nonpromotion", key),
            value,
        )
    simple(
        "normalization census altered",
        ("result", "count_ledger", "source_core_normalization_row_count"),
        23,
    )
    simple(
        "component census invented",
        ("result", "count_ledger", "historical_Round27_c24_component_id_count"),
        1,
    )
    simple(
        "Round35 census invented",
        ("result", "count_ledger", "Round35_rn_restriction_id_count"),
        1,
    )
    mutations.append(
        (
            "strict nonclaim deleted",
            lambda document: (
                document["result"]["strict_nonclaims"].pop(),
                resign(document),
            ),
        )
    )
    extra = lambda document: (
        document["result"].__setitem__("unknown_semantic_field", True),
        resign(document),
    )
    mutations.append(("unknown result field inserted", extra))

    rejected: list[str] = []
    for label, mutation in mutations:
        candidate = copy.deepcopy(certificate)
        mutation(candidate)
        try:
            evaluate_document(candidate, expected)
        except (
            VerificationError,
            KeyError,
            IndexError,
            TypeError,
            ValueError,
        ):
            rejected.append(label)
        else:
            raise VerificationError(f"semantic mutation accepted:{label}")
    require(len(rejected) == len(mutations), "all semantic mutations rejected")
    return rejected


def strict_json_attacks(
    certificate: dict[str, Any], expected: dict[str, Any]
) -> list[str]:
    raw = (
        json.dumps(
            certificate,
            sort_keys=True,
            indent=2,
            ensure_ascii=False,
            allow_nan=False,
        )
        + "\n"
    ).encode("utf-8")
    attacks: list[tuple[str, bytes]] = []

    def add(label: str, payload: bytes) -> None:
        require(payload != raw, f"strict attack construction:{label}")
        attacks.append((label, payload))

    add(
        "duplicate top-level schema",
        raw.replace(
            b'{\n  "result":',
            b'{\n  "schema": "duplicate",\n  "result":',
            1,
        ),
    )
    add(
        "duplicate nested status",
        raw.replace(
            b'"status": "CERTIFIED_PROSPECTIVE_SEED_INDEPENDENT_DYADIC_BASIS_RANK_CONTRACT"',
            b'"status": "bad", "status": "CERTIFIED_PROSPECTIVE_SEED_INDEPENDENT_DYADIC_BASIS_RANK_CONTRACT"',
            1,
        ),
    )
    add(
        "duplicate witness level",
        raw.replace(
            b'"contained_primitive_basis_denominator_power": 3809',
            b'"contained_primitive_basis_denominator_power": 1, "contained_primitive_basis_denominator_power": 3809',
            1,
        ),
    )
    add(
        "floating count",
        raw.replace(
            b'"source_core_normalization_row_count": 24',
            b'"source_core_normalization_row_count": 24.0',
            1,
        ),
    )
    add(
        "exponent count",
        raw.replace(
            b'"source_core_normalization_row_count": 24',
            b'"source_core_normalization_row_count": 2.4e1',
            1,
        ),
    )
    add(
        "NaN constant",
        raw.replace(
            b'"source_core_normalization_row_count": 24',
            b'"source_core_normalization_row_count": NaN',
            1,
        ),
    )
    add(
        "positive Infinity",
        raw.replace(
            b'"source_core_normalization_row_count": 24',
            b'"source_core_normalization_row_count": Infinity',
            1,
        ),
    )
    add(
        "negative Infinity",
        raw.replace(
            b'"source_core_normalization_row_count": 24',
            b'"source_core_normalization_row_count": -Infinity',
            1,
        ),
    )
    add("UTF-8 BOM", b"\xef\xbb\xbf" + raw)
    add("invalid UTF-8", raw[:16] + b"\xff" + raw[16:])
    add("top-level array", b"[]\n")
    add("top-level null", b"null\n")
    add("trailing second document", raw + b"{}\n")
    add(
        "oversized integer",
        raw.replace(
            b'"source_core_normalization_row_count": 24',
            b'"source_core_normalization_row_count": '
            + b"9" * (MAX_JSON_INTEGER_DIGITS + 1),
            1,
        ),
    )
    add(
        "negative zero",
        raw.replace(
            b'"source_core_normalization_row_count": 24',
            b'"source_core_normalization_row_count": -0',
            1,
        ),
    )
    add(
        "leading zero",
        raw.replace(
            b'"source_core_normalization_row_count": 24',
            b'"source_core_normalization_row_count": 024',
            1,
        ),
    )
    add(
        "unpaired surrogate",
        raw.replace(
            b'"CERTIFIED_PROSPECTIVE_SEED_INDEPENDENT_DYADIC_BASIS_RANK_CONTRACT"',
            b'"\\ud800"',
            1,
        ),
    )
    witness_rank = certificate["result"]["round136_contained_basis_witness"][
        "contained_primitive_basis_rank"
    ]
    decimal_token = json.dumps(witness_rank["decimal"]).encode("ascii")
    hexadecimal_token = json.dumps(witness_rank["hexadecimal"]).encode("ascii")
    add(
        "overlong public decimal string",
        raw.replace(
            decimal_token,
            json.dumps("9" * (WITNESS_RANK_DECIMAL_DIGITS + 1)).encode("ascii"),
            1,
        ),
    )
    add(
        "overlong public hexadecimal string",
        raw.replace(
            hexadecimal_token,
            json.dumps(
                "0x"
                + "f"
                * (
                    (witness_rank["bit_length"] + 3) // 4
                    + 1
                )
            ).encode("ascii"),
            1,
        ),
    )
    extra_envelope = copy.deepcopy(certificate)
    extra_envelope["unknown"] = True
    add(
        "closed envelope extra key",
        (json.dumps(extra_envelope, sort_keys=True) + "\n").encode(),
    )
    extra_result = copy.deepcopy(certificate)
    extra_result["result"]["unknown"] = True
    resign(extra_result)
    add(
        "closed result extra key",
        (json.dumps(extra_result, sort_keys=True) + "\n").encode(),
    )
    stale = copy.deepcopy(certificate)
    stale["result"]["strict_nonpromotion"]["CM2"] = "GO_FOR_CLAIM"
    add(
        "stale result digest",
        (json.dumps(stale, sort_keys=True) + "\n").encode(),
    )

    rejected: list[str] = []
    for label, payload in attacks:
        try:
            document = strict_json_bytes(payload, label)
            evaluate_document(document, expected)
        except (
            VerificationError,
            UnicodeError,
            KeyError,
            IndexError,
            TypeError,
            ValueError,
        ):
            rejected.append(label)
        else:
            raise VerificationError(f"strict JSON attack accepted:{label}")
    require(len(rejected) == len(attacks) == 22, "22 strict attacks rejected")
    return rejected


# ---------------------------------------------------------------------------
# Input/output safety
# ---------------------------------------------------------------------------


def safe_input_path(path: Path) -> Path:
    expanded = path.expanduser()
    require(not expanded.is_symlink(), "certificate symlink")
    try:
        metadata = expanded.lstat()
    except FileNotFoundError as exc:
        raise VerificationError("missing certificate") from exc
    require(stat.S_ISREG(metadata.st_mode), "certificate regular file")
    require(metadata.st_nlink == 1, "certificate single hardlink")
    require(metadata.st_size <= MAX_CERTIFICATE_BYTES, "certificate byte cap")
    resolved = expanded.resolve()
    require(sha256(resolved) == CERTIFICATE_SHA256, "certificate byte pin")
    return resolved


def protected_paths(certificate_path: Path) -> set[Path]:
    return {
        VERIFIER.resolve(),
        PRODUCER.resolve(),
        CERTIFICATE.resolve(),
        certificate_path.resolve(),
        *((HERE / name).resolve() for name in UPSTREAM_PINS),
    }


def safe_output_path(path: Path, certificate_path: Path) -> Path:
    expanded = path.expanduser()
    protected = protected_paths(certificate_path)
    require(not expanded.is_symlink(), "output symlink")
    require(not expanded.parent.is_symlink(), "output parent symlink")
    if expanded.exists():
        metadata = expanded.lstat()
        require(stat.S_ISREG(metadata.st_mode), "output regular file")
        require(metadata.st_nlink == 1, "output single hardlink")
        for protected_path in protected:
            try:
                require(
                    not os.path.samefile(expanded, protected_path),
                    "output hardlink aliases protected input",
                )
            except FileNotFoundError:
                pass
    resolved = expanded.resolve()
    require(resolved not in protected, "output aliases protected input")
    require(resolved.parent.is_dir(), "output parent directory")
    require(not resolved.parent.is_symlink(), "resolved output parent symlink")
    return resolved


def path_safety_tests(certificate_path: Path) -> list[str]:
    labels: list[str] = []
    originals = {
        path: sha256(path)
        for path in protected_paths(certificate_path)
        if path.is_file()
    }

    def reject(label: str, action: Callable[[], Any]) -> None:
        try:
            action()
        except (VerificationError, OSError):
            labels.append(label)
        else:
            raise VerificationError(f"path attack accepted:{label}")

    with tempfile.TemporaryDirectory(prefix="cm2-r137-path-tests-") as name:
        root = Path(name)
        copied = root / "certificate.json"
        copied.write_bytes(certificate_path.read_bytes())
        require(safe_input_path(copied) == copied.resolve(), "copied input accepted")
        reject("missing certificate", lambda: safe_input_path(root / "missing.json"))

        input_symlink = root / "input-symlink.json"
        input_symlink.symlink_to(copied)
        reject("certificate symlink", lambda: safe_input_path(input_symlink))

        input_hardlink = root / "input-hardlink.json"
        os.link(copied, input_hardlink)
        reject("certificate hardlink", lambda: safe_input_path(copied))
        input_hardlink.unlink()

        input_fifo = root / "input-fifo"
        os.mkfifo(input_fifo)
        reject("certificate FIFO", lambda: safe_input_path(input_fifo))

        tampered = root / "tampered.json"
        tampered.write_bytes(certificate_path.read_bytes() + b" ")
        reject("tampered certificate", lambda: safe_input_path(tampered))

        reject(
            "output aliases selected certificate",
            lambda: safe_output_path(copied, copied),
        )
        reject(
            "output aliases formal certificate",
            lambda: safe_output_path(CERTIFICATE, copied),
        )
        reject(
            "output aliases producer",
            lambda: safe_output_path(PRODUCER, copied),
        )
        reject(
            "output aliases verifier",
            lambda: safe_output_path(VERIFIER, copied),
        )
        for name_key in sorted(UPSTREAM_PINS):
            reject(
                f"output aliases upstream:{name_key}",
                lambda selected=name_key: safe_output_path(HERE / selected, copied),
            )

        output_symlink = root / "output-symlink.json"
        output_symlink.symlink_to(copied)
        reject("output symlink", lambda: safe_output_path(output_symlink, copied))

        output_hardlink = root / "output-hardlink.json"
        os.link(copied, output_hardlink)
        reject("output hardlink", lambda: safe_output_path(output_hardlink, copied))
        output_hardlink.unlink()

        output_fifo = root / "output-fifo"
        os.mkfifo(output_fifo)
        reject("output FIFO", lambda: safe_output_path(output_fifo, copied))

        output_directory = root / "output-directory"
        output_directory.mkdir()
        reject(
            "output directory",
            lambda: safe_output_path(output_directory, copied),
        )

        real_parent = root / "real-parent"
        real_parent.mkdir()
        linked_parent = root / "linked-parent"
        linked_parent.symlink_to(real_parent, target_is_directory=True)
        reject(
            "output parent symlink",
            lambda: safe_output_path(linked_parent / "out.json", copied),
        )

        fresh = root / "fresh.json"
        require(
            safe_output_path(fresh, copied) == fresh.resolve(),
            "fresh output accepted",
        )
    require(
        originals
        == {
            path: sha256(path)
            for path in originals
        },
        "protected inputs unchanged by path tests",
    )
    require(len(labels) == 20, "20 path attacks rejected")
    return labels


def build_verification(
    expected: dict[str, Any],
    semantic_labels: list[str],
    strict_labels: list[str],
    path_labels: list[str],
) -> dict[str, Any]:
    witness = expected["round136_contained_basis_witness"]
    normalization = expected["source_core_affine_normalization_contract"]
    tests = expected["executable_test_ledger"]
    return {
        "status": "PASS",
        "verifier_sha256": sha256(VERIFIER),
        "producer_sha256": PRODUCER_SHA256,
        "certificate_sha256": CERTIFICATE_SHA256,
        "certificate_schema": CERTIFICATE_SCHEMA,
        "certificate_result_sha256": CERTIFICATE_RESULT_SHA256,
        "independence_contract": {
            "Round137_producer_imported": False,
            "Round137_producer_executed": False,
            "affine_normalizations_independently_reconstructed": True,
            "common_denominator_primitive_rule_independently_reconstructed": True,
            "I_m_counts_and_offsets_independently_reconstructed": True,
            "rank_1d_and_unrank_1d_independently_reconstructed": True,
            "rank_2d_and_unrank_2d_independently_reconstructed": True,
            "small_levels_independently_exhausted": True,
            "large_fixtures_independently_replayed": True,
            "Round136_contained_witness_independently_reconstructed": True,
            "full_certificate_result_independently_reconstructed": True,
        },
        "reconstruction_audit": {
            "source_core_normalization_row_count":
                normalization["normalization_row_count"],
            "normalization_rows_sha256":
                normalization["normalization_rows_sha256"],
            "exhaustive_small_2d_row_count":
                tests["small_level_exhaustive"]["exhaustive_2d_row_count"],
            "exhaustive_small_1d_row_count":
                tests["small_level_exhaustive"]["exhaustive_1d_row_count"],
            "large_2d_fixture_count": tests["large_2d_fixture_count"],
            "large_1d_fixture_count": tests["large_1d_fixture_count"],
            "witness_source_core_index": witness["source_core_index"],
            "witness_return_depth": witness["return_depth"],
            "witness_minimal_level":
                witness["contained_primitive_basis_denominator_power"],
            "witness_rank_bit_length":
                witness["contained_primitive_basis_rank"]["bit_length"],
            "witness_rank_decimal_digit_count":
                witness["contained_primitive_basis_rank"]["decimal_digit_count"],
            "witness_rank_decimal_sha256":
                witness["contained_primitive_basis_rank"]["sha256_of_decimal"],
            "witness_locator_id": witness["component_witness_locator_id"],
            "historical_Round27_canonical_component_rank":
                witness["historical_Round27_canonical_component_rank"],
            "historical_Round27_c24_component_id":
                witness["historical_Round27_c24_component_id"],
            "projection_to_Round35_restriction_id":
                witness["projection_to_Round35_restriction_id"],
        },
        "semantic_mutation_test_count": len(semantic_labels),
        "semantic_mutation_rejection_labels": semantic_labels,
        "strict_json_attack_count": len(strict_labels),
        "strict_json_attack_rejection_labels": strict_labels,
        "path_safety_self_test_count": len(path_labels),
        "path_safety_rejection_labels": path_labels,
        "determinism_contract": {
            "canonical_JSON_sort_keys": True,
            "no_hash_iteration_controls_output": True,
            "verification_replay_is_PYTHONHASHSEED_independent": True,
            "dual_seed_byte_replay_required_by_freeze_pack": True,
        },
        "path_safety_contract": {
            "certificate_must_match_frozen_byte_pin": True,
            "input_must_be_regular_single_link_non_symlink": True,
            "output_must_be_regular_single_link_or_absent": True,
            "producer_verifier_certificate_and_all_upstreams_protected": True,
            "input_output_alias_rejected": True,
            "symlink_hardlink_FIFO_attacks_rejected": True,
            "atomic_replace_after_fsync": True,
        },
        "safety_and_nonpromotion": dict(expected["strict_nonpromotion"]),
    }


def write_document(path: Path, document: dict[str, Any]) -> None:
    payload = (
        json.dumps(
            document,
            indent=2,
            sort_keys=True,
            ensure_ascii=False,
            allow_nan=False,
        )
        + "\n"
    )
    descriptor, temporary = tempfile.mkstemp(
        prefix=f".{path.name}.",
        suffix=".tmp",
        dir=path.parent,
    )
    temporary_path = Path(temporary)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8", newline="\n") as handle:
            handle.write(payload)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary_path, path)
    finally:
        if temporary_path.exists():
            temporary_path.unlink()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certificate", type=Path, default=CERTIFICATE)
    parser.add_argument("--output", type=Path, default=OUTPUT)
    args = parser.parse_args()
    try:
        certificate_path = safe_input_path(args.certificate)
        certificate = strict_json(certificate_path)
        expected = build_expected()
        evaluate_document(certificate, expected)
        semantic_labels = semantic_mutations(certificate, expected)
        strict_labels = strict_json_attacks(certificate, expected)
        path_labels = path_safety_tests(certificate_path)
        result = build_verification(
            expected, semantic_labels, strict_labels, path_labels
        )
        envelope = {
            "schema": VERIFICATION_SCHEMA,
            "result": result,
            "result_sha256": digest(result),
        }
        output_path = safe_output_path(args.output, certificate_path)
        write_document(output_path, envelope)
        return 0
    except (
        VerificationError,
        KeyError,
        IndexError,
        TypeError,
        ValueError,
        OSError,
    ) as exc:
        print(f"VerificationError: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
