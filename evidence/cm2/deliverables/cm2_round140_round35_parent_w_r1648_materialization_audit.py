#!/usr/bin/env python3
"""Round140: maximal legal Round35 parent-W data from the Round139 R_1648 cell.

The Round139 positive-area fixed-s rectangle has one strict 1648-step return
word.  This append-only audit materializes its exact source-core/path tuple,
the fixed parameter and implicit slope-four leaf descriptor, the complete
incidence-rank path, the B=14 mesh, and prospective Round137-v1 contained
2D/1D basis ranks.

The two numeric ranks are *witness ranks*.  Each is the least Round137-v1
rank whose represented closed box/interval lies in the particular certified
Round139 rectangle/leaf subinterval.  Consequently each is an upper bound on
the corresponding least rank of the larger connected component/leaf
interval.  Earlier basis elements elsewhere in those larger objects are not
excluded.  The unnamed historical Round27/Round35 ranks are not recovered.

The Round35 natural 1e-90 short-cell index is also not minted: the Round139
cell supplies only an interior leaf subinterval, not the oriented endpoint
and arclength origin of the maximal U-intersection leaf interval on which the
historical natural index is based.
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


if hasattr(sys, "set_int_max_str_digits"):
    # Public ranks below have more than 4,300 decimal digits.
    sys.set_int_max_str_digits(0)


HERE = Path(__file__).resolve().parent
OUTPUT = (
    HERE
    / "cm2-round140-round35-parent-w-r1648-materialization-audit-2026-07-24.json"
)
SCHEMA = "cm2.round140.round35-parent-w-r1648-materialization-audit.v1"

ROUND35 = (
    HERE
    / "cm2-gate45-round35-arbitrary-rn-common-carrier-manifest-2026-07-19.json"
)
ROUND27 = (
    HERE
    / "cm2-gate34-round27-arbitrary-n-path-schema-manifest-2026-07-18.json"
)
ROUND137_PRODUCER = (
    HERE / "cm2_round137_seed_independent_dyadic_basis_rank_contract.py"
)
ROUND137 = (
    HERE / "cm2-round137-seed-independent-dyadic-basis-rank-contract-2026-07-24.json"
)
ROUND137_VERIFIER = (
    HERE / "cm2_round137_seed_independent_dyadic_basis_rank_contract_verifier.py"
)
ROUND137_VERIFICATION = (
    HERE
    / "cm2-round137-seed-independent-dyadic-basis-rank-contract-verification-2026-07-24.json"
)
ROUND139 = (
    HERE
    / "cm2-round139-rank3-minus-d0-adjacent-h1-collar-return-frontier-2026-07-24.json"
)
ROUND139_PRODUCER = (
    HERE
    / "cm2_round139_rank3_minus_d0_adjacent_h1_collar_return_frontier.py"
)
ROUND139_VERIFIER = (
    HERE
    / "cm2_round139_rank3_minus_d0_adjacent_h1_collar_return_frontier_verifier.py"
)

PINS = {
    ROUND27.name:
        "988f364bd1e6943178238c072e725de01af36452ef25d179eae6aef4000f7916",
    ROUND35.name:
        "ece7c97beeeb0b527434dc430e247ad0af407dc58b82d634da9e34a2f9e9521c",
    ROUND137_PRODUCER.name:
        "81974ada469f8f24299d7790e16f6380f58b38df151ee67704695aa81c0d08ac",
    ROUND137.name:
        "06918b7bbfdeed9bda41a1220a25b630df6eaaa5f06024757f25a8c9fe7b88bf",
    ROUND137_VERIFIER.name:
        "8d359eb9d397d3c4375d2ae21cc752447f0fb9216d180b59b3517288914fba45",
    ROUND137_VERIFICATION.name:
        "53369532c293d9cb2830a362facef7e4c4040f826f5ddea70519fde9034a1a5c",
    ROUND139_PRODUCER.name:
        "462ffcb41ba24771ce655ddb3ad5f18d5a22c8d0cb443ec1791ea9272d3d512b",
    ROUND139.name:
        "64e91e6b1efcb2675982fbc453b08349b003c8be5b4d236f61e1392aaee045f0",
    ROUND139_VERIFIER.name:
        "cb96e0e1a74abcac4254f20584bab6997edb8de69f0d979f1d65d4c3fdfadd09",
}

RETURN_DEPTH = 1648
SOURCE_CORE_INDEX = 14
SOURCE_CORE_ID = (
    "core:90398e9ab632e57b027266bc7c34461a0a6a6d308c35fbeacc41432a3d7f48f7"
)
SOURCE_T_BOUNDS = (Q(1, 100), Q(1, 50))
SOURCE_P_BOUNDS = (Q(-1, 500), Q(1, 500))
SOURCE_P_STAR = Q(-1587, 1638400)
INCIDENCE_RANK = 14
DELTA_14 = Q(1, 2**23)
EXPECTED_PATH_TUPLE_SHA256 = (
    "5cec1061ec331e8f37929dfb1b2b2a78757309ba60198d571abd9e8cf6c70ed9"
)
EXPECTED_PATH_SEQUENCE_SHA256 = (
    "f504289edce554d47e17a90d7c886586a69f3ec4b64fafd90c718c50ca93221e"
)
EXPECTED_INCIDENCE_PATH_SHA256 = (
    "a2669f5587b2c7c10dc0d18fe1db2516df2b2049a7bf8cd37292636cd9c6fbe7"
)
EXPECTED_2D_LEVEL = 5883
EXPECTED_2D_RANK_DECIMAL_DIGITS = 7084
EXPECTED_2D_RANK_DECIMAL_SHA256 = (
    "81ee4f795045d8478e621dbcaf2cba2437ccb168b34b770f995c012c0060927f"
)
EXPECTED_1D_LEVEL = 5883
EXPECTED_1D_RANK_DECIMAL_DIGITS = 3542
EXPECTED_1D_RANK_DECIMAL_SHA256 = (
    "fe02c53ca61c7ae9a81d189ffbf5d58cbae33ee16cb68e6248c65d5fc708c24d"
)


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


def qstr(value: Q | int) -> str:
    value = Q(value)
    return (
        str(value.numerator)
        if value.denominator == 1
        else f"{value.numerator}/{value.denominator}"
    )


def strict_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        require(type(key) is str and key not in result, "duplicate JSON key")
        result[key] = value
    return result


def strict_json(path: Path) -> dict[str, Any]:
    metadata = path.lstat()
    require(
        stat.S_ISREG(metadata.st_mode)
        and metadata.st_nlink == 1
        and not path.is_symlink()
        and path.resolve().parent == HERE,
        f"unsafe dependency:{path.name}",
    )
    value = json.loads(
        path.read_text(encoding="utf-8"),
        object_pairs_hook=strict_pairs,
        parse_float=lambda token: (_ for _ in ()).throw(
            ValueError(f"floating JSON number forbidden:{token}")
        ),
        parse_constant=lambda token: (_ for _ in ()).throw(
            ValueError(f"invalid JSON constant:{token}")
        ),
    )
    require(type(value) is dict, f"dependency root:{path.name}")
    return value


def closed_result(path: Path, schema: str) -> dict[str, Any]:
    envelope = strict_json(path)
    require(
        set(envelope) == {"schema", "result", "result_sha256"},
        f"closed envelope:{path.name}",
    )
    require(envelope["schema"] == schema, f"schema:{path.name}")
    require(
        type(envelope["result"]) is dict
        and envelope["result_sha256"] == digest(envelope["result"]),
        f"result closure:{path.name}",
    )
    return envelope["result"]


def interval_pair_count(level: int) -> int:
    require(type(level) is int and level >= 0, "nonnegative dyadic level")
    if level < 2:
        return 0
    points = 2**level - 1
    return points * (points - 1) // 2


def validate_pair(level: int, left: int, right: int) -> None:
    require(level >= 2, "dyadic level at least two")
    require(
        1 <= left < right <= 2**level - 1,
        "strict interior ordered pair",
    )


def pair_rank(level: int, left: int, right: int) -> int:
    validate_pair(level, left, right)
    maximum = 2**level - 1
    preceding = left - 1
    return (
        preceding * maximum
        - preceding * (preceding + 1) // 2
        + right - left - 1
    )


def pair_unrank(level: int, ordinal: int) -> tuple[int, int]:
    total = interval_pair_count(level)
    require(0 <= ordinal < total, "pair ordinal range")
    maximum = 2**level - 1
    coefficient = 2 * maximum - 1
    discriminant = coefficient * coefficient - 8 * ordinal
    preceding = (coefficient - math.isqrt(discriminant)) // 2

    def offset(count: int) -> int:
        return count * maximum - count * (count + 1) // 2

    while preceding > 0 and offset(preceding) > ordinal:
        preceding -= 1
    while (
        preceding + 1 <= maximum - 2
        and offset(preceding + 1) <= ordinal
    ):
        preceding += 1
    left = preceding + 1
    right = left + 1 + ordinal - offset(preceding)
    validate_pair(level, left, right)
    return left, right


def even_pairs_before(level: int, left: int, right: int) -> int:
    validate_pair(level, left, right)
    half_maximum = 2 ** (level - 1) - 1
    earlier_even_first = (left - 1) // 2
    count = (
        earlier_even_first * half_maximum
        - earlier_even_first * (earlier_even_first + 1) // 2
    )
    if left % 2 == 0:
        count += max(0, (right - 1) // 2 - left // 2)
    return count


def pair_is_even(pair: tuple[int, int]) -> bool:
    return pair[0] % 2 == 0 and pair[1] % 2 == 0


def primitive_pair_unrank(level: int, ordinal: int) -> tuple[int, int]:
    total = interval_pair_count(level)
    primitive_total = total - interval_pair_count(level - 1)
    require(0 <= ordinal < primitive_total, "primitive pair ordinal range")
    low, high = 0, total - 1
    while low <= high:
        middle = (low + high) // 2
        pair = pair_unrank(level, middle)
        filtered = middle - even_pairs_before(level, *pair)
        if pair_is_even(pair):
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
    raise RuntimeError("primitive pair unrank")


def validate_1d(row: tuple[int, int, int]) -> None:
    level, left, right = row
    validate_pair(level, left, right)
    require(left % 2 or right % 2, "primitive 1D row")


def rank_1d(row: tuple[int, int, int]) -> int:
    validate_1d(row)
    level, left, right = row
    return (
        interval_pair_count(level - 1)
        + pair_rank(level, left, right)
        - even_pairs_before(level, left, right)
    )


def level_for_1d_rank(rank: int) -> int:
    require(type(rank) is int and rank >= 0, "nonnegative 1D rank")
    low, high = 2, max(2, rank.bit_length() + 2)
    while low < high:
        middle = (low + high) // 2
        if interval_pair_count(middle) > rank:
            high = middle
        else:
            low = middle + 1
    return low


def unrank_1d(rank: int) -> tuple[int, int, int]:
    level = level_for_1d_rank(rank)
    local = rank - interval_pair_count(level - 1)
    row = (level, *primitive_pair_unrank(level, local))
    validate_1d(row)
    return row


def validate_2d(row: tuple[int, int, int, int, int]) -> None:
    level, a0, a1, b0, b1 = row
    validate_pair(level, a0, a1)
    validate_pair(level, b0, b1)
    require(
        any(value % 2 for value in (a0, a1, b0, b1)),
        "primitive common denominator",
    )


def rank_2d(row: tuple[int, int, int, int, int]) -> int:
    validate_2d(row)
    level, a0, a1, b0, b1 = row
    total = interval_pair_count(level)
    even = interval_pair_count(level - 1)
    a_rank = pair_rank(level, a0, a1)
    before_a = a_rank * total - even_pairs_before(level, a0, a1) * even
    b_rank = pair_rank(level, b0, b1)
    within_a = (
        b_rank
        if not pair_is_even((a0, a1))
        else b_rank - even_pairs_before(level, b0, b1)
    )
    return even**2 + before_a + within_a


def level_for_2d_rank(rank: int) -> int:
    require(type(rank) is int and rank >= 0, "nonnegative 2D rank")
    low, high = 2, max(2, rank.bit_length() + 2)
    while low < high:
        middle = (low + high) // 2
        if interval_pair_count(middle) ** 2 > rank:
            high = middle
        else:
            low = middle + 1
    return low


def unrank_2d(rank: int) -> tuple[int, int, int, int, int]:
    level = level_for_2d_rank(rank)
    total = interval_pair_count(level)
    even = interval_pair_count(level - 1)
    local = rank - even**2
    low, high = 0, total - 1
    while low <= high:
        middle = (low + high) // 2
        a_pair = pair_unrank(level, middle)
        before_a = middle * total - even_pairs_before(level, *a_pair) * even
        block_size = total - even if pair_is_even(a_pair) else total
        if local < before_a:
            high = middle - 1
        elif local >= before_a + block_size:
            low = middle + 1
        else:
            b_local = local - before_a
            b_pair = (
                primitive_pair_unrank(level, b_local)
                if pair_is_even(a_pair)
                else pair_unrank(level, b_local)
            )
            row = (level, *a_pair, *b_pair)
            validate_2d(row)
            return row
    raise RuntimeError("2D unrank")


def first_two_strict_points(
    lower: Q,
    upper: Q,
    level: int,
) -> tuple[int, int] | None:
    require(Q(0) < lower < upper < Q(1), "normalized open interval")
    denominator = 2**level
    first = (lower.numerator * denominator) // lower.denominator + 1
    second = first + 1
    if (
        1 <= first < second <= denominator - 1
        and lower < Q(first, denominator) < Q(second, denominator) < upper
    ):
        return first, second
    return None


def least_contained_1d(
    lower: Q,
    upper: Q,
) -> tuple[int, int, int]:
    level = 2
    while True:
        pair = first_two_strict_points(lower, upper, level)
        if pair is not None:
            row = (level, *pair)
            validate_1d(row)
            return row
        level += 1


def least_contained_2d(
    u0: Q,
    u1: Q,
    v0: Q,
    v1: Q,
) -> tuple[int, int, int, int, int]:
    level = 2
    while True:
        u_pair = first_two_strict_points(u0, u1, level)
        v_pair = first_two_strict_points(v0, v1, level)
        if u_pair is not None and v_pair is not None:
            row = (level, *u_pair, *v_pair)
            validate_2d(row)
            return row
        level += 1


def encoded_integer(value: int) -> dict[str, Any]:
    require(type(value) is int and value >= 0, "encoded nonnegative integer")
    decimal = str(value)
    return {
        "decimal": decimal,
        "hexadecimal": "0x" + format(value, "x"),
        "bit_length": value.bit_length(),
        "decimal_digit_count": len(decimal),
        "sha256_of_decimal":
            hashlib.sha256(decimal.encode("ascii")).hexdigest(),
    }


def validate_dependencies() -> tuple[
    dict[str, Any],
    dict[str, Any],
    dict[str, Any],
]:
    for name, expected in sorted(PINS.items()):
        path = HERE / name
        require(
            path.is_file()
            and not path.is_symlink()
            and path.resolve().parent == HERE
            and sha256(path) == expected,
            f"dependency byte pin:{name}",
        )

    round27 = strict_json(ROUND27)
    require(
        round27["schema"]
        == "cm2.gate34.round27-arbitrary-n-path-schema.manifest.v1"
        and round27["result"]["C24_full_dimensional_arbitrary_n_candidate_path_join"][
            "candidate_path_id_grammar"
        ]
        == "c24-path:(source_core_id,n,k_1,...,k_n), k_j in frozen K"
        and round27["result"]["canonical_regular_connected_component_schema"][
            "component_coordinates_and_nonempty_ranks_enumerated"
        ] is False,
        "Round27 path/component boundary",
    )

    round35 = strict_json(ROUND35)
    require(
        round35["schema"]
        == "cm2.gate45.round35-arbitrary-rn-common-carrier.v1.manifest.v1",
        "Round35 schema",
    )
    registry = round35["result"]["arbitrary_Rn_parent_W_Borel_registry"]
    require(
        registry["source_interval_rank"]
        == "least rational-dyadic interval basis index with closure inside the interval"
        and registry["source_parent_W_id"]
        == (
            "rn-parent-W:(component-id):(s,b):(source-interval-rank):"
            "(incidence-rank-path):(short-cell-k)"
        )
        and registry["nonempty_component_coordinates_enumerated"] is False,
        "Round35 historical boundary",
    )

    round137 = closed_result(
        ROUND137,
        "cm2.round137.seed-independent-dyadic-basis-rank-contract.v1",
    )
    round137_verification = closed_result(
        ROUND137_VERIFICATION,
        "cm2.round137.seed-independent-dyadic-basis-rank-contract-verification.v1",
    )
    require(
        round137_verification["status"] == "PASS"
        and round137["dyadic_basis_enumeration_v1"]["contract_id"]
        == "round137-dyadic-basis-enumeration-v1"
        and round137["historical_schema_audit"][
            "new_v1_recovers_historical_numeric_labels"
        ] is False,
        "Round137 prospective boundary",
    )

    round139 = closed_result(
        ROUND139,
        "cm2.round139.rank3-minus-d0-adjacent-h1-collar-return-frontier.v1",
    )
    require(
        round139["status"]
        == "CERTIFIED_MINUS_D0_ADJACENT_H1_COLLAR_STRICT_FIRST_RETURN"
        and round139["strict_nonpromotion"][
            "local_positive_area_R1648_return_cylinder_materialized"
        ] is True
        and round139["strict_nonpromotion"][
            "global_Round35_restriction_materialized"
        ] is False,
        "Round139 local/global boundary",
    )
    return round35, round137, round139


def build() -> dict[str, Any]:
    round35, round137, round139 = validate_dependencies()
    source = round139["corrected_rank3_source_contract"]
    cylinder = round139["nested_positive_area_R1648_cylinder"]
    summary = round139["positive_area_first_return_summary"]
    rows = round139["positive_area_collision_rows"]
    root = round139["deep_same_D0_root_and_b_star"]

    require(
        source["source_core_index"] == SOURCE_CORE_INDEX
        and source["source_core_id"] == SOURCE_CORE_ID
        and source["source_chart"] == "W:E"
        and source["source_target"] == "W[1,0]",
        "source core fixture",
    )
    normalization = round137[
        "source_core_affine_normalization_contract"
    ]["normalization_rows"][SOURCE_CORE_INDEX]
    require(
        normalization["source_core_id"] == SOURCE_CORE_ID
        and normalization["t_bounds"]
        == [qstr(value) for value in SOURCE_T_BOUNDS]
        and normalization["p_bounds"]
        == [qstr(value) for value in SOURCE_P_BOUNDS],
        "Round137 source normalization",
    )
    require(
        cylinder["object_kind"]
        == "LOCAL_POSITIVE_AREA_FIXED_S_R1648_CYLINDER"
        and cylinder["s_box"] == ["0", "0"]
        and cylinder["positive_area"] is True
        and summary["object_kind"]
        == "POSITIVE_AREA_FIXED_S_RECTANGLE_CYLINDER"
        and summary["first_return_depth"] == RETURN_DEPTH
        and summary["collision_row_count"] == RETURN_DEPTH
        and summary["strict_first_return_whole_positive_area_rectangle"] is True
        and len(rows) == RETURN_DEPTH
        and digest(rows) == round139["positive_area_collision_rows_sha256"]
        == summary["collision_rows_sha256"],
        "Round139 positive-area R1648 cell",
    )

    path_ids = [
        row["official_word_key"]["official_word_key_id"] for row in rows
    ]
    path_payload = [SOURCE_CORE_ID, RETURN_DEPTH, path_ids]
    incidence_path = [row["incidence_rank_B"] for row in rows]
    require(
        digest(path_ids) == EXPECTED_PATH_SEQUENCE_SHA256
        == summary["official_word_key_sequence_sha256"]
        and digest(path_payload) == EXPECTED_PATH_TUPLE_SHA256
        and len(path_ids) == RETURN_DEPTH
        and all(
            type(identifier) is str and identifier.startswith("gate5-word:")
            for identifier in path_ids
        ),
        "Round27-compatible path tuple",
    )
    require(
        incidence_path == [INCIDENCE_RANK] * RETURN_DEPTH
        and digest(incidence_path) == EXPECTED_INCIDENCE_PATH_SHA256
        and summary["incidence_rank_histogram"]
        == {str(INCIDENCE_RANK): RETURN_DEPTH},
        "incidence path",
    )
    mesh_exponent = math.ceil(3 * (INCIDENCE_RANK + 1) / 2)
    require(mesh_exponent == 23 and DELTA_14 == Q(1, 2**mesh_exponent), "delta14")

    t0, t1 = (Q(value) for value in cylinder["t_box"])
    p0, p1 = (Q(value) for value in cylinder["p_box"])
    require(
        SOURCE_T_BOUNDS[0] < t0 < t1 < SOURCE_T_BOUNDS[1]
        and SOURCE_P_BOUNDS[0] < p0 < p1 < SOURCE_P_BOUNDS[1],
        "cylinder strictly inside source core",
    )
    u0 = (t0 - SOURCE_T_BOUNDS[0]) / (
        SOURCE_T_BOUNDS[1] - SOURCE_T_BOUNDS[0]
    )
    u1 = (t1 - SOURCE_T_BOUNDS[0]) / (
        SOURCE_T_BOUNDS[1] - SOURCE_T_BOUNDS[0]
    )
    v0 = (p0 - SOURCE_P_BOUNDS[0]) / (
        SOURCE_P_BOUNDS[1] - SOURCE_P_BOUNDS[0]
    )
    v1 = (p1 - SOURCE_P_BOUNDS[0]) / (
        SOURCE_P_BOUNDS[1] - SOURCE_P_BOUNDS[0]
    )

    row2 = least_contained_2d(u0, u1, v0, v1)
    rank2 = rank_2d(row2)
    encoded2 = encoded_integer(rank2)
    row1 = least_contained_1d(u0, u1)
    rank1 = rank_1d(row1)
    encoded1 = encoded_integer(rank1)
    require(
        row2[0] == EXPECTED_2D_LEVEL
        and encoded2["decimal_digit_count"]
        == EXPECTED_2D_RANK_DECIMAL_DIGITS
        and encoded2["sha256_of_decimal"]
        == EXPECTED_2D_RANK_DECIMAL_SHA256,
        "2D contained rank fixture",
    )
    require(
        row1[0] == EXPECTED_1D_LEVEL
        and encoded1["decimal_digit_count"]
        == EXPECTED_1D_RANK_DECIMAL_DIGITS
        and encoded1["sha256_of_decimal"]
        == EXPECTED_1D_RANK_DECIMAL_SHA256,
        "1D contained rank fixture",
    )
    require(
        unrank_2d(rank2) == row2 and unrank_1d(rank1) == row1,
        "contained rank/unrank roundtrips",
    )
    denominator2 = 2**row2[0]
    denominator1 = 2**row1[0]
    require(
        u0 < Q(row2[1], denominator2) < Q(row2[2], denominator2) < u1
        and v0 < Q(row2[3], denominator2) < Q(row2[4], denominator2) < v1
        and u0 < Q(row1[1], denominator1) < Q(row1[2], denominator1) < u1,
        "contained rank closures strict",
    )
    require(
        first_two_strict_points(u0, u1, row1[0] - 1) is None
        and (
            first_two_strict_points(u0, u1, row2[0] - 1) is None
            or first_two_strict_points(v0, v1, row2[0] - 1) is None
        ),
        "contained witness levels minimal",
    )

    b_outer = root["b_star_fixed_dyadic_outer"]
    root_bracket = root["deep_D0_root_bracket"]
    require(
        root["same_exact_implicit_b_star"] is True
        and root["same_exact_fixed_p_D0_root"] is True
        and root["deep_D0_unique"] is True
        and root["b_star_fixed_dyadic_outer_bits"] == 16448
        and len(b_outer) == 2
        and Q(b_outer[0]) < Q(b_outer[1])
        and len(root_bracket) == 2
        and Q(root_bracket[0]) < Q(root_bracket[1]),
        "implicit b_star descriptor",
    )

    two_d_locator_payload = {
        "contract": "round137-dyadic-basis-enumeration-v1",
        "source_core_id": SOURCE_CORE_ID,
        "return_depth": RETURN_DEPTH,
        "path_tuple_sha256": digest(path_payload),
        "round139_positive_area_word_cell_id":
            summary["local_D0_adjacent_return_word_cell_id"],
        "contained_basis_row": list(row2),
        "contained_basis_rank_decimal": str(rank2),
    }
    one_d_locator_payload = {
        "contract": "round137-dyadic-basis-enumeration-v1",
        "coordinate": "u=(t-1/100)/(1/100) on the exact b_star leaf",
        "source_core_id": SOURCE_CORE_ID,
        "return_depth": RETURN_DEPTH,
        "path_tuple_sha256": digest(path_payload),
        "contained_basis_row": list(row1),
        "contained_basis_rank_decimal": str(rank1),
    }

    result = {
        "status":
            "CERTIFIED_MAXIMAL_LEGAL_ROUND35_PARENT_W_DATA_FROM_R1648",
        "provenance": {
            "producer_sha256": sha256(Path(__file__).resolve()),
            "dependency_sha256": dict(sorted(PINS.items())),
            "append_only": True,
            "Round139_files_modified": False,
            "historical_identifiers_minted": False,
        },
        "Round35_schema_boundary": {
            "source_parent_W_id_schema":
                round35["result"]["arbitrary_Rn_parent_W_Borel_registry"][
                    "source_parent_W_id"
                ],
            "historical_component_and_interval_enumerations_executable": False,
            "Round137_v1_is_prospective_not_historical": True,
        },
        "materialized_source_core_path_tuple": {
            "Round27_compatible_payload_schema":
                "[source_core_id,return_depth,[official_word_key_id_1,...,official_word_key_id_n]]",
            "payload": path_payload,
            "payload_sha256": digest(path_payload),
            "source_core_index": SOURCE_CORE_INDEX,
            "source_core_id": SOURCE_CORE_ID,
            "return_depth": RETURN_DEPTH,
            "official_word_key_occurrence_count": len(path_ids),
            "official_word_key_sequence_sha256": digest(path_ids),
            "unique_official_word_key_count": len(set(path_ids)),
            "whole_positive_rectangle_has_this_exact_path": True,
        },
        "fixed_parameter_and_exact_implicit_leaf": {
            "s": "0",
            "s_is_exact": True,
            "leaf_equation": "asin(p)-4*r=b_star",
            "contact_coordinate": "r=(4/25)*asin(t)",
            "leaf_equation_in_t": "asin(p)-(16/25)*asin(t)=b_star",
            "fixed_p_star": qstr(SOURCE_P_STAR),
            "t_star_descriptor": (
                "the unique t in deep_D0_root_bracket for which the collision-3 "
                "W[0,0] discriminant D3(t,p_star) is zero"
            ),
            "deep_D0_root_bracket": root_bracket,
            "deep_D0_root_unique": True,
            "exact_b_star_descriptor":
                "b_star=asin(-1587/1638400)-(16/25)*asin(t_star)",
            "b_star_fixed_dyadic_outer_bits":
                root["b_star_fixed_dyadic_outer_bits"],
            "b_star_fixed_dyadic_outer": b_outer,
            "b_star_outer_is_an_enclosure_not_a_rational_replacement": True,
            "same_Round138_local_parent_W_id":
                root["same_Round138_local_parent_W_id"],
        },
        "incidence_rank_and_density_mesh": {
            "incidence_rank_path": incidence_path,
            "incidence_rank_path_run_length_encoding":
                [[INCIDENCE_RANK, RETURN_DEPTH]],
            "incidence_rank_path_sha256": digest(incidence_path),
            "all_source_and_target_capped_cosine_ranks_equal_14":
                all(
                    row["source_capped_reciprocal_cosine_rank"] == INCIDENCE_RANK
                    and row["target_capped_reciprocal_cosine_rank"]
                    == INCIDENCE_RANK
                    for row in rows
                ),
            "Round35_mesh_formula": "delta_B=2^-ceil(3(B+1)/2)",
            "B": INCIDENCE_RANK,
            "ceil_3_times_B_plus_1_over_2": mesh_exponent,
            "delta_14": qstr(DELTA_14),
            "delta_14_power_of_two": "2^-23",
        },
        "Round137_v1_contained_2d_basis_rank": {
            "contract": "round137-dyadic-basis-enumeration-v1",
            "coordinate_normalization": {
                "u": "(t-(1/100))/(1/100)",
                "v": "(p-(-1/500))/(1/250)",
            },
            "physical_positive_R1648_rectangle": {
                "t": cylinder["t_box"],
                "p": cylinder["p_box"],
                "s": cylinder["s_box"],
            },
            "normalized_open_rectangle": {
                "u": [qstr(u0), qstr(u1)],
                "v": [qstr(v0), qstr(v1)],
            },
            "contained_primitive_basis_row": list(row2),
            "contained_primitive_basis_rank": encoded2,
            "rank_unrank_roundtrip_exact": True,
            "basis_closure_strictly_inside_Round139_rectangle": True,
            "least_v1_rank_among_basis_boxes_strictly_contained_in_this_rectangle":
                True,
            "component_witness_locator_id":
                "round140-r1648-component-witness-locator:"
                + digest(two_d_locator_payload),
            "component_witness_locator_payload_sha256":
                digest(two_d_locator_payload),
            "locator_is_noncanonical_and_does_not_deduplicate_components": True,
            "rank_is_upper_bound_for_least_v1_rank_of_containing_component":
                True,
            "least_v1_rank_of_containing_component_computed": False,
            "historical_Round27_canonical_component_rank": None,
            "historical_Round27_c24_component_id": None,
        },
        "Round137_v1_contained_1d_leaf_rank": {
            "contract": "round137-dyadic-basis-enumeration-v1",
            "prospective_leaf_coordinate":
                "u=(t-(1/100))/(1/100), increasing with physical r",
            "exact_leaf":
                "s=0 and b=b_star from the exact implicit descriptor",
            "known_open_leaf_subinterval_normalized_u":
                [qstr(u0), qstr(u1)],
            "contained_primitive_basis_row": list(row1),
            "contained_primitive_basis_rank": encoded1,
            "rank_unrank_roundtrip_exact": True,
            "basis_closure_graph_strictly_inside_positive_R1648_rectangle":
                True,
            "least_v1_rank_among_basis_intervals_strictly_contained_in_this_known_leaf_subinterval":
                True,
            "leaf_witness_locator_id":
                "round140-r1648-leaf-witness-locator:"
                + digest(one_d_locator_payload),
            "leaf_witness_locator_payload_sha256":
                digest(one_d_locator_payload),
            "locator_is_noncanonical": True,
            "rank_is_upper_bound_for_least_v1_rank_of_containing_U_leaf_interval":
                True,
            "least_v1_rank_of_containing_U_leaf_interval_computed": False,
            "historical_Round35_source_interval_rank": None,
            "historical_Round35_r_coordinate_normalization_recovered": False,
        },
        "natural_1e_minus_90_short_cell_audit": {
            "historical_rule":
                "oriented Euclidean arclength intervals [k*1e-90,(k+1)*1e-90] clipped at leaf endpoints",
            "known_exact_leaf_subinterval_H1_length_strict_upper":
                "2^-5888",
            "known_exact_leaf_subinterval_shorter_than_1e-90": (
                10**90 < 2**5888
            ),
            "maximal_U_intersection_leaf_endpoint_materialized": False,
            "historical_oriented_arclength_origin_materialized": False,
            "position_relative_to_endpoint_anchored_1e-90_grid_materialized":
                False,
            "natural_short_cell_index_well_defined_from_available_data": False,
            "natural_short_cell_k": None,
            "reason": (
                "Round139 gives only a tiny interior leaf subinterval; Round35 "
                "does not materialize the maximal U-intersection leaf endpoint "
                "that fixes the oriented arclength origin, so neither k nor a "
                "historical parent-W ID can be selected"
            ),
        },
        "maximal_legal_Round35_field_status": {
            "source_core_path_tuple_materialized": True,
            "s_materialized": True,
            "exact_implicit_b_star_descriptor_materialized": True,
            "b_star_dyadic_outer_materialized": True,
            "incidence_rank_path_materialized": True,
            "delta_14_materialized": True,
            "Round137_v1_contained_2d_rank_materialized": True,
            "Round137_v1_contained_1d_rank_materialized": True,
            "least_Round137_v1_component_rank_materialized": False,
            "least_Round137_v1_leaf_interval_rank_materialized": False,
            "historical_Round27_component_rank_materialized": False,
            "historical_Round35_source_interval_rank_materialized": False,
            "natural_short_cell_k_materialized": False,
            "Round35_source_parent_W_id_materialized": False,
            "Round35_image_recut_rank_materialized": False,
            "Round35_rn_restriction_id_materialized": False,
        },
        "strict_nonpromotion": {
            "containing_witness_rank_is_least_canonical_rank": False,
            "historical_Round27_canonical_component_rank": None,
            "historical_Round27_c24_component_id": None,
            "historical_Round35_source_interval_rank": None,
            "historical_Round35_natural_short_cell_k": None,
            "historical_Round35_source_parent_W_id": None,
            "historical_Round35_image_recut_rank": None,
            "historical_Round35_rn_restriction_id": None,
            "Round50_owner_key_count": 0,
            "Round54_t54_token_count": 0,
            "Round67_q_j_output_count": 0,
            "global_gate5_maturity": "10/18",
            "global_complete_18_field_block_count": 0,
            "Gate5": "NOT_CERTIFIED",
            "CM2": "NO-GO_FOR_CLAIM",
        },
        "count_ledger": {
            "source_core_path_tuple_count": 1,
            "official_word_key_occurrence_count": RETURN_DEPTH,
            "incidence_rank_occurrence_count": RETURN_DEPTH,
            "b_star_exact_implicit_descriptor_count": 1,
            "b_star_dyadic_outer_count": 1,
            "Round137_v1_contained_2d_rank_count": 1,
            "Round137_v1_contained_1d_rank_count": 1,
            "least_canonical_component_rank_count": 0,
            "least_canonical_leaf_interval_rank_count": 0,
            "historical_Round35_parent_W_id_count": 0,
            "historical_Round35_restriction_id_count": 0,
            "global_complete_18_field_block_count": 0,
        },
        "strict_scope": (
            "one positive-area fixed-s R_1648 word cell and one exact implicit "
            "slope-four leaf subgraph inside it"
        ),
        "strict_nonclaims": [
            "the Round137-v1 ranks do not recover the unnamed historical Round27 or Round35 numeric enumerations",
            "the contained 2D rank is not asserted to be the least basis rank anywhere in the larger connected return component",
            "the contained 1D rank is not asserted to be the least basis rank anywhere in the larger U-intersection leaf interval",
            "the b_star dyadic outer is an enclosure of the exact implicitly defined real, not a rational replacement for that real",
            "no natural 1e-90 short-cell k is asserted without the maximal leaf-interval endpoint and oriented arclength origin",
            "no historical c24-component, Round35 parent-W, image recut or rn-restriction identifier is minted",
            "no Gate5 field, complete block or CM2 claim is promoted",
        ],
    }
    require(
        result["strict_nonpromotion"]["global_gate5_maturity"] == "10/18"
        and result["strict_nonpromotion"][
            "global_complete_18_field_block_count"
        ] == 0
        and result["strict_nonpromotion"]["CM2"] == "NO-GO_FOR_CLAIM",
        "global nonpromotion boundary",
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
    print(canonical({
        "status": envelope["result"]["status"],
        "path_tuple_sha256":
            envelope["result"]["materialized_source_core_path_tuple"][
                "payload_sha256"
            ],
        "contained_2d_rank_sha256":
            envelope["result"]["Round137_v1_contained_2d_basis_rank"][
                "contained_primitive_basis_rank"
            ]["sha256_of_decimal"],
        "contained_1d_rank_sha256":
            envelope["result"]["Round137_v1_contained_1d_leaf_rank"][
                "contained_primitive_basis_rank"
            ]["sha256_of_decimal"],
        "natural_short_cell_k": None,
    }))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
