#!/usr/bin/env python3
"""Independent fail-closed verifier for the Round140 parent-W audit.

The verifier never imports or executes the Round140 producer.  It reconstructs
the source/path tuple directly from the byte-pinned Round139 collision rows,
checks the Round27 and Round35 schema boundaries, and independently implements
the prospective Round137-v1 dyadic enumeration.  In particular, it proves that
the published ranks are the least v1 ranks whose represented box/interval is
strictly contained in the *specific* Round139 rectangle/leaf subinterval.

Those ranks remain witness locators and only upper bounds for the least rank
somewhere in the larger connected component or maximal U-leaf interval.  The
verifier rejects every promotion to a historical component rank, a Round35
source-interval rank, an endpoint-anchored 1e-90 short-cell index, or a
Round35 parent-W identifier.
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


if hasattr(sys, "set_int_max_str_digits"):
    sys.set_int_max_str_digits(0)


HERE = Path(__file__).resolve().parent
VERIFIER = Path(__file__).resolve()
PRODUCER = (
    HERE / "cm2_round140_round35_parent_w_r1648_materialization_audit.py"
)
CERTIFICATE = (
    HERE
    / "cm2-round140-round35-parent-w-r1648-materialization-audit-2026-07-24.json"
)
OUTPUT = (
    HERE
    / "cm2-round140-round35-parent-w-r1648-materialization-audit-verification-2026-07-24.json"
)

CERTIFICATE_SCHEMA = (
    "cm2.round140.round35-parent-w-r1648-materialization-audit.v1"
)
VERIFICATION_SCHEMA = (
    "cm2.round140.round35-parent-w-r1648-materialization-audit-verification.v1"
)
PRODUCER_SHA256 = (
    "6329e0050f6727f8c0fa7d2a5052028645a375c5d59c51169e2ec81fb2ad7377"
)
CERTIFICATE_SHA256 = (
    "bb6283e2fccba194b47f9aa174e85594560ba88062ed57d06651003744755a79"
)
CERTIFICATE_RESULT_SHA256 = (
    "7988f4c9588894ec964e2c6efec4dd07dd28d5011c0bf004ad73f99414534eed"
)
MAX_CERTIFICATE_BYTES = 600_000
MAX_DEPENDENCY_BYTES = 10_000_000
MAX_JSON_INTEGER_DIGITS = 4096

ROUND27 = "cm2-gate34-round27-arbitrary-n-path-schema-manifest-2026-07-18.json"
ROUND35 = (
    "cm2-gate45-round35-arbitrary-rn-common-carrier-manifest-2026-07-19.json"
)
ROUND137_PRODUCER = "cm2_round137_seed_independent_dyadic_basis_rank_contract.py"
ROUND137 = (
    "cm2-round137-seed-independent-dyadic-basis-rank-contract-2026-07-24.json"
)
ROUND137_VERIFIER = (
    "cm2_round137_seed_independent_dyadic_basis_rank_contract_verifier.py"
)
ROUND137_VERIFICATION = (
    "cm2-round137-seed-independent-dyadic-basis-rank-contract-verification-2026-07-24.json"
)
ROUND139_PRODUCER = (
    "cm2_round139_rank3_minus_d0_adjacent_h1_collar_return_frontier.py"
)
ROUND139 = (
    "cm2-round139-rank3-minus-d0-adjacent-h1-collar-return-frontier-2026-07-24.json"
)
ROUND139_VERIFIER = (
    "cm2_round139_rank3_minus_d0_adjacent_h1_collar_return_frontier_verifier.py"
)

INPUT_PINS = {
    ROUND27:
        "988f364bd1e6943178238c072e725de01af36452ef25d179eae6aef4000f7916",
    ROUND35:
        "ece7c97beeeb0b527434dc430e247ad0af407dc58b82d634da9e34a2f9e9521c",
    ROUND137_PRODUCER:
        "81974ada469f8f24299d7790e16f6380f58b38df151ee67704695aa81c0d08ac",
    ROUND137:
        "06918b7bbfdeed9bda41a1220a25b630df6eaaa5f06024757f25a8c9fe7b88bf",
    ROUND137_VERIFIER:
        "8d359eb9d397d3c4375d2ae21cc752447f0fb9216d180b59b3517288914fba45",
    ROUND137_VERIFICATION:
        "53369532c293d9cb2830a362facef7e4c4040f826f5ddea70519fde9034a1a5c",
    ROUND139_PRODUCER:
        "462ffcb41ba24771ce655ddb3ad5f18d5a22c8d0cb443ec1791ea9272d3d512b",
    ROUND139:
        "64e91e6b1efcb2675982fbc453b08349b003c8be5b4d236f61e1392aaee045f0",
    ROUND139_VERIFIER:
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
PATH_TUPLE_SHA256 = (
    "5cec1061ec331e8f37929dfb1b2b2a78757309ba60198d571abd9e8cf6c70ed9"
)
PATH_SEQUENCE_SHA256 = (
    "f504289edce554d47e17a90d7c886586a69f3ec4b64fafd90c718c50ca93221e"
)
INCIDENCE_PATH_SHA256 = (
    "a2669f5587b2c7c10dc0d18fe1db2516df2b2049a7bf8cd37292636cd9c6fbe7"
)
RANK_2D_LEVEL = 5883
RANK_2D_DECIMAL_DIGITS = 7084
RANK_2D_DECIMAL_SHA256 = (
    "81ee4f795045d8478e621dbcaf2cba2437ccb168b34b770f995c012c0060927f"
)
RANK_1D_LEVEL = 5883
RANK_1D_DECIMAL_DIGITS = 3542
RANK_1D_DECIMAL_SHA256 = (
    "fe02c53ca61c7ae9a81d189ffbf5d58cbae33ee16cb68e6248c65d5fc708c24d"
)


class VerificationError(RuntimeError):
    """Fail-closed file, parsing, reconstruction, or semantic error."""


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


def parse_integer(token: str) -> int:
    digits = token[1:] if token.startswith("-") else token
    require(len(digits) <= MAX_JSON_INTEGER_DIGITS, "oversized JSON integer")
    require(token != "-0", "negative-zero JSON integer")
    return int(token)


def reject_float(token: str) -> None:
    raise VerificationError(f"floating JSON number:{token[:32]}")


def reject_constant(token: str) -> None:
    raise VerificationError(f"non-finite JSON constant:{token}")


def validate_json_tree(value: Any) -> None:
    if value is None or type(value) in {bool, int}:
        return
    if type(value) is str:
        require(
            not any(0xD800 <= ord(character) <= 0xDFFF for character in value),
            "unpaired Unicode surrogate",
        )
        return
    if type(value) is list:
        for child in value:
            validate_json_tree(child)
        return
    require(type(value) is dict, "JSON value type")
    for key, child in value.items():
        validate_json_tree(key)
        validate_json_tree(child)


def strict_json_bytes(raw: bytes, label: str, cap: int) -> dict[str, Any]:
    require(len(raw) <= cap, f"JSON byte cap:{label}")
    require(not raw.startswith(b"\xef\xbb\xbf"), f"UTF-8 BOM:{label}")
    try:
        text = raw.decode("utf-8", errors="strict")
        decoder = json.JSONDecoder(
            object_pairs_hook=strict_pairs,
            parse_int=parse_integer,
            parse_float=reject_float,
            parse_constant=reject_constant,
        )
        value, end = decoder.raw_decode(text)
        require(not text[end:].strip(), f"trailing JSON data:{label}")
    except (UnicodeError, ValueError, json.JSONDecodeError) as exc:
        raise VerificationError(f"strict JSON:{label}") from exc
    require(type(value) is dict, f"top-level JSON object:{label}")
    validate_json_tree(value)
    return value


def regular_single_link(path: Path, label: str, cap: int | None = None) -> None:
    try:
        metadata = path.lstat()
    except OSError as exc:
        raise VerificationError(f"missing input:{label}") from exc
    require(stat.S_ISREG(metadata.st_mode), f"regular input:{label}")
    require(metadata.st_nlink == 1, f"single-link input:{label}")
    require(not path.is_symlink(), f"non-symlink input:{label}")
    if cap is not None:
        require(metadata.st_size <= cap, f"input byte cap:{label}")


def exact_workspace_input(path: Path, expected: Path, cap: int) -> bytes:
    regular_single_link(path, expected.name, cap)
    require(
        path.resolve() == expected.resolve()
        and path.name == expected.name
        and path.resolve().parent == HERE,
        f"exact workspace input:{expected.name}",
    )
    return path.read_bytes()


def strict_dependency(path: Path) -> dict[str, Any]:
    regular_single_link(path, path.name, MAX_DEPENDENCY_BYTES)
    require(
        path.resolve().parent == HERE and path.name in INPUT_PINS,
        f"dependency location:{path.name}",
    )
    return strict_json_bytes(
        path.read_bytes(),
        path.name,
        MAX_DEPENDENCY_BYTES,
    )


def closed_result(
    document: dict[str, Any],
    schema: str,
    label: str,
) -> dict[str, Any]:
    require(
        set(document) == {"schema", "result", "result_sha256"},
        f"closed envelope:{label}",
    )
    require(document["schema"] == schema, f"schema:{label}")
    result = document["result"]
    require(
        type(result) is dict and document["result_sha256"] == digest(result),
        f"result closure:{label}",
    )
    return result


def validate_pins(certificate_path: Path) -> bytes:
    regular_single_link(PRODUCER, PRODUCER.name)
    require(
        PRODUCER.resolve().parent == HERE
        and sha256(PRODUCER) == PRODUCER_SHA256,
        "Round140 producer pin",
    )
    certificate_raw = exact_workspace_input(
        certificate_path,
        CERTIFICATE,
        MAX_CERTIFICATE_BYTES,
    )
    require(
        hashlib.sha256(certificate_raw).hexdigest() == CERTIFICATE_SHA256,
        "Round140 certificate pin",
    )
    for name, expected in sorted(INPUT_PINS.items()):
        path = HERE / name
        regular_single_link(path, name, MAX_DEPENDENCY_BYTES)
        require(
            path.resolve().parent == HERE and sha256(path) == expected,
            f"dependency pin:{name}",
        )
    return certificate_raw


def interval_pair_count(level: int) -> int:
    require(type(level) is int and level >= 0, "nonnegative dyadic level")
    if level < 2:
        return 0
    points = 2**level - 1
    return points * (points - 1) // 2


def validate_pair(level: int, left: int, right: int) -> None:
    require(
        type(level) is int
        and type(left) is int
        and type(right) is int
        and level >= 2
        and 1 <= left < right <= 2**level - 1,
        "valid dyadic pair",
    )


def pair_lex_rank(level: int, left: int, right: int) -> int:
    """Direct count of pairs lexicographically before (left,right)."""
    validate_pair(level, left, right)
    maximum = 2**level - 1
    earlier_left = left - 1
    earlier_blocks = (
        earlier_left * maximum
        - earlier_left * (earlier_left + 1) // 2
    )
    return earlier_blocks + (right - left - 1)


def even_pairs_before(level: int, left: int, right: int) -> int:
    """Direct count of all-even pairs before a given lexicographic pair."""
    validate_pair(level, left, right)
    even_points = 2 ** (level - 1) - 1
    earlier_even_left = (left - 1) // 2
    count = (
        earlier_even_left * even_points
        - earlier_even_left * (earlier_even_left + 1) // 2
    )
    if left % 2 == 0:
        count += max(0, (right - 1) // 2 - left // 2)
    return count


def pair_is_even(left: int, right: int) -> bool:
    return left % 2 == 0 and right % 2 == 0


def rank_1d(row: tuple[int, int, int]) -> int:
    level, left, right = row
    validate_pair(level, left, right)
    require(not pair_is_even(left, right), "primitive 1D row")
    return (
        interval_pair_count(level - 1)
        + pair_lex_rank(level, left, right)
        - even_pairs_before(level, left, right)
    )


def rank_2d(row: tuple[int, int, int, int, int]) -> int:
    level, a0, a1, b0, b1 = row
    validate_pair(level, a0, a1)
    validate_pair(level, b0, b1)
    require(
        any(value % 2 for value in (a0, a1, b0, b1)),
        "primitive common denominator",
    )
    total_pairs = interval_pair_count(level)
    even_pairs = interval_pair_count(level - 1)
    a_ordinal = pair_lex_rank(level, a0, a1)
    before_a = (
        a_ordinal * total_pairs
        - even_pairs_before(level, a0, a1) * even_pairs
    )
    b_ordinal = pair_lex_rank(level, b0, b1)
    within_a = (
        b_ordinal
        if not pair_is_even(a0, a1)
        else b_ordinal - even_pairs_before(level, b0, b1)
    )
    return even_pairs**2 + before_a + within_a


def level_for_rank_1d(rank: int) -> int:
    require(type(rank) is int and rank >= 0, "nonnegative 1D rank")
    low, high = 2, max(2, rank.bit_length() + 2)
    while low < high:
        middle = (low + high) // 2
        if interval_pair_count(middle) > rank:
            high = middle
        else:
            low = middle + 1
    return low


def level_for_rank_2d(rank: int) -> int:
    require(type(rank) is int and rank >= 0, "nonnegative 2D rank")
    low, high = 2, max(2, rank.bit_length() + 2)
    while low < high:
        middle = (low + high) // 2
        if interval_pair_count(middle) ** 2 > rank:
            high = middle
        else:
            low = middle + 1
    return low


def first_two_strict_points(
    lower: Q,
    upper: Q,
    level: int,
) -> tuple[int, int] | None:
    require(Q(0) < lower < upper < Q(1), "normalized open interval")
    denominator = 2**level
    first = lower.numerator * denominator // lower.denominator + 1
    second = first + 1
    if (
        1 <= first < second <= denominator - 1
        and lower < Q(first, denominator) < Q(second, denominator) < upper
    ):
        return first, second
    return None


def least_contained_1d(lower: Q, upper: Q) -> tuple[int, int, int]:
    for level in range(2, 100_000):
        pair = first_two_strict_points(lower, upper, level)
        if pair is not None:
            row = (level, *pair)
            require(
                row[1] % 2 or row[2] % 2,
                "consecutive pair is primitive",
            )
            return row
    raise VerificationError("1D contained row search cap")


def least_contained_2d(
    u0: Q,
    u1: Q,
    v0: Q,
    v1: Q,
) -> tuple[int, int, int, int, int]:
    for level in range(2, 100_000):
        u_pair = first_two_strict_points(u0, u1, level)
        v_pair = first_two_strict_points(v0, v1, level)
        if u_pair is not None and v_pair is not None:
            row = (level, *u_pair, *v_pair)
            require(
                any(value % 2 for value in row[1:]),
                "consecutive 2D row is primitive",
            )
            return row
    raise VerificationError("2D contained row search cap")


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


def row_hash_closed(row: dict[str, Any], label: str) -> None:
    require(type(row) is dict and "row_sha256" in row, f"row hash:{label}")
    body = dict(row)
    claimed = body.pop("row_sha256")
    require(claimed == digest(body), f"row closure:{label}")


def load_inputs() -> dict[str, dict[str, Any]]:
    documents: dict[str, dict[str, Any]] = {}
    for name in (ROUND27, ROUND35, ROUND137, ROUND137_VERIFICATION, ROUND139):
        documents[name] = strict_dependency(HERE / name)
    return documents


def reconstruct_expected() -> tuple[dict[str, Any], dict[str, Any]]:
    documents = load_inputs()
    round27_document = documents[ROUND27]
    round35_document = documents[ROUND35]
    round137 = closed_result(
        documents[ROUND137],
        "cm2.round137.seed-independent-dyadic-basis-rank-contract.v1",
        ROUND137,
    )
    round137_verification = closed_result(
        documents[ROUND137_VERIFICATION],
        "cm2.round137.seed-independent-dyadic-basis-rank-contract-verification.v1",
        ROUND137_VERIFICATION,
    )
    round139 = closed_result(
        documents[ROUND139],
        "cm2.round139.rank3-minus-d0-adjacent-h1-collar-return-frontier.v1",
        ROUND139,
    )

    require(
        round27_document["schema"]
        == "cm2.gate34.round27-arbitrary-n-path-schema.manifest.v1"
        and round27_document["verdict"][
            "C24_arbitrary_n_full_dimensional_candidate_path_coverage"
        ] == "CERTIFIED_MOD_SINGULAR_NULL",
        "Round27 manifest boundary",
    )
    round27 = round27_document["result"]
    path_schema = round27[
        "C24_full_dimensional_arbitrary_n_candidate_path_join"
    ]
    component_schema = round27[
        "canonical_regular_connected_component_schema"
    ]
    require(
        path_schema["candidate_path_id_grammar"]
        == "c24-path:(source_core_id,n,k_1,...,k_n), k_j in frozen K"
        and path_schema["exact_nonempty_candidate_path_keys_enumerated"] is False
        and component_schema["canonical_component_id"]
        == "c24-component:(source_core_id,n,path_key,least_dyadic_basis_index)"
        and component_schema[
            "component_coordinates_and_nonempty_ranks_enumerated"
        ] is False,
        "Round27 path/component schema",
    )

    require(
        round35_document["schema"]
        == "cm2.gate45.round35-arbitrary-rn-common-carrier.v1.manifest.v1"
        and round35_document["verdict"][
            "parameterized_schema_is_finite_component_enumeration"
        ] is False,
        "Round35 manifest boundary",
    )
    round35 = round35_document["result"]
    registry = round35["arbitrary_Rn_parent_W_Borel_registry"]
    require(
        registry["component_id_schema"]
        == "c24-component:(source-core-id,n,path-key,least-dyadic-basis-index)"
        and registry["source_interval_rank"]
        == "least rational-dyadic interval basis index with closure inside the interval"
        and registry["source_parent_W_id"]
        == (
            "rn-parent-W:(component-id):(s,b):(source-interval-rank):"
            "(incidence-rank-path):(short-cell-k)"
        )
        and registry["nonempty_component_coordinates_enumerated"] is False,
        "Round35 historical boundary",
    )

    basis = round137["dyadic_basis_enumeration_v1"]
    history = round137["historical_schema_audit"]
    require(
        round137_verification["status"] == "PASS"
        and basis["contract_id"] == "round137-dyadic-basis-enumeration-v1"
        and basis["index_origin"] == "zero_based"
        and basis["one_dimensional"]["row_schema"] == "(m,a0,a1)"
        and basis["two_dimensional"]["row_schema"]
        == "(m,a0,a1,b0,b1)"
        and basis["two_dimensional"]["per_axis_primitive_condition_required"]
        is False
        and history["new_v1_recovers_historical_numeric_labels"] is False
        and history[
            "new_v1_is_prospective_compatible_with_countability_schema_only"
        ] is True,
        "Round137 prospective enumeration boundary",
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
    source = round139["corrected_rank3_source_contract"]
    cylinder = round139["nested_positive_area_R1648_cylinder"]
    summary = round139["positive_area_first_return_summary"]
    rows = round139["positive_area_collision_rows"]
    root = round139["deep_same_D0_root_and_b_star"]
    row_hash_closed(cylinder, "Round139 positive-area cylinder")
    row_hash_closed(root, "Round139 deep root")

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
    row_hash_closed(normalization, "Round137 normalization")
    require(
        normalization["source_core_index"] == SOURCE_CORE_INDEX
        and normalization["source_core_id"] == SOURCE_CORE_ID
        and normalization["chart_id"] == "W:E"
        and normalization["target_id"] == "W[1,0]"
        and normalization["t_bounds"]
        == [qstr(value) for value in SOURCE_T_BOUNDS]
        and normalization["p_bounds"]
        == [qstr(value) for value in SOURCE_P_BOUNDS],
        "Round137 source normalization",
    )

    require(
        cylinder["object_kind"]
        == "LOCAL_POSITIVE_AREA_FIXED_S_R1648_CYLINDER"
        and cylinder["construction"]
        == "first t-half of the graph-collar rectangle, with a fresh leaf p-hull"
        and cylinder["s_box"] == ["0", "0"]
        and cylinder["positive_area"] is True
        and cylinder["contains_a_positive_width_exact_leaf_subgraph"] is True
        and cylinder["contained_in_graph_collar_rectangle_enclosure"] is True
        and cylinder["strictly_inside_source_core"] is True
        and summary["object_kind"]
        == "POSITIVE_AREA_FIXED_S_RECTANGLE_CYLINDER"
        and summary["first_return_depth"] == RETURN_DEPTH
        and summary["collision_row_count"] == RETURN_DEPTH
        and summary["strict_first_return_whole_positive_area_rectangle"] is True
        and summary["exact_half_open_H1_collar"] is None
        and len(rows) == RETURN_DEPTH
        and digest(rows) == round139["positive_area_collision_rows_sha256"]
        == summary["collision_rows_sha256"],
        "Round139 positive-area R1648 cell",
    )

    path_ids: list[str] = []
    incidence_path: list[int] = []
    for index, row in enumerate(rows, 1):
        row_hash_closed(row, f"Round139 collision {index}")
        word = row["official_word_key"]
        require(
            type(word) is dict
            and word["registry_row_sha256"] == digest(word["registry_row"])
            and word["official_word_key_id"]
            == (
                f"gate5-word:{word['ordinal_zero_based']:06d}:"
                f"{word['registry_row_sha256']}"
            )
            and row["collision_index"] == index
            and row["homogeneity_label"] == "H0_CENTRAL"
            and row["incidence_rank_B"] == INCIDENCE_RANK
            and row["source_capped_reciprocal_cosine_rank"] == INCIDENCE_RANK
            and row["target_capped_reciprocal_cosine_rank"] == INCIDENCE_RANK
            and row["retained_and_full_radius4_selected_owner_equal"] is True
            and row["full_radius4_candidate_count"] == 161,
            f"Round139 collision semantics:{index}",
        )
        path_ids.append(word["official_word_key_id"])
        incidence_path.append(row["incidence_rank_B"])

    path_payload = [SOURCE_CORE_ID, RETURN_DEPTH, path_ids]
    require(
        digest(path_ids) == PATH_SEQUENCE_SHA256
        == summary["official_word_key_sequence_sha256"]
        and digest(path_payload) == PATH_TUPLE_SHA256
        and summary["unique_official_word_key_count"] == len(set(path_ids))
        == 141,
        "source/path tuple reconstruction",
    )
    require(
        incidence_path == [INCIDENCE_RANK] * RETURN_DEPTH
        and digest(incidence_path) == INCIDENCE_PATH_SHA256
        and summary["incidence_rank_histogram"]
        == {str(INCIDENCE_RANK): RETURN_DEPTH},
        "incidence path reconstruction",
    )
    mesh_exponent = math.ceil(3 * (INCIDENCE_RANK + 1) / 2)
    require(
        mesh_exponent == 23
        and DELTA_14 == Q(1, 2**mesh_exponent),
        "Round35 delta14",
    )

    t0, t1 = (Q(value) for value in cylinder["t_box"])
    p0, p1 = (Q(value) for value in cylinder["p_box"])
    require(
        SOURCE_T_BOUNDS[0] < t0 < t1 < SOURCE_T_BOUNDS[1]
        and SOURCE_P_BOUNDS[0] < p0 < p1 < SOURCE_P_BOUNDS[1]
        and Q(cylinder["t_width"]) == t1 - t0
        and Q(cylinder["p_width"]) == p1 - p0
        and Q(cylinder["area"]) == (t1 - t0) * (p1 - p0) > 0,
        "exact Round139 inner rectangle",
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
    require(Q(0) < u0 < u1 < Q(1) and Q(0) < v0 < v1 < Q(1), "normalization")

    row2 = least_contained_2d(u0, u1, v0, v1)
    rank2 = rank_2d(row2)
    encoded2 = encoded_integer(rank2)
    row1 = least_contained_1d(u0, u1)
    rank1 = rank_1d(row1)
    encoded1 = encoded_integer(rank1)
    require(
        row2[0] == RANK_2D_LEVEL
        and encoded2["decimal_digit_count"] == RANK_2D_DECIMAL_DIGITS
        and encoded2["sha256_of_decimal"] == RANK_2D_DECIMAL_SHA256
        and level_for_rank_2d(rank2) == row2[0],
        "independent 2D rank reconstruction",
    )
    require(
        row1[0] == RANK_1D_LEVEL
        and encoded1["decimal_digit_count"] == RANK_1D_DECIMAL_DIGITS
        and encoded1["sha256_of_decimal"] == RANK_1D_DECIMAL_SHA256
        and level_for_rank_1d(rank1) == row1[0],
        "independent 1D rank reconstruction",
    )
    denominator = 2**RANK_2D_LEVEL
    require(
        u0 < Q(row2[1], denominator) < Q(row2[2], denominator) < u1
        and v0 < Q(row2[3], denominator) < Q(row2[4], denominator) < v1
        and u0 < Q(row1[1], denominator) < Q(row1[2], denominator) < u1,
        "strict basis containment",
    )
    require(
        first_two_strict_points(u0, u1, RANK_1D_LEVEL - 1) is None
        and (
            first_two_strict_points(u0, u1, RANK_2D_LEVEL - 1) is None
            or first_two_strict_points(v0, v1, RANK_2D_LEVEL - 1) is None
        ),
        "minimal feasible dyadic level",
    )
    # At the first feasible level, consecutive first/second strict points are
    # lexicographically least.  Together with level ordering, this proves the
    # stored rows and ranks are least among boxes/intervals in this cell.
    require(
        tuple(row2[1:3])
        == first_two_strict_points(u0, u1, RANK_2D_LEVEL)
        and tuple(row2[3:5])
        == first_two_strict_points(v0, v1, RANK_2D_LEVEL)
        and tuple(row1[1:3])
        == first_two_strict_points(u0, u1, RANK_1D_LEVEL),
        "lexicographically least contained rows",
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
        "exact implicit b_star descriptor",
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
            "producer_sha256": PRODUCER_SHA256,
            "dependency_sha256": dict(sorted(INPUT_PINS.items())),
            "append_only": True,
            "Round139_files_modified": False,
            "historical_identifiers_minted": False,
        },
        "Round35_schema_boundary": {
            "source_parent_W_id_schema": registry["source_parent_W_id"],
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
            "all_source_and_target_capped_cosine_ranks_equal_14": True,
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
            "known_exact_leaf_subinterval_shorter_than_1e-90":
                10**90 < 2**5888,
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
    replay = {
        "source_path_tuple_sha256": digest(path_payload),
        "official_word_key_sequence_sha256": digest(path_ids),
        "official_word_key_occurrence_count": len(path_ids),
        "unique_official_word_key_count": len(set(path_ids)),
        "incidence_rank_path_sha256": digest(incidence_path),
        "incidence_rank_run": [INCIDENCE_RANK, RETURN_DEPTH],
        "delta_14": qstr(DELTA_14),
        "normalized_rectangle": {
            "u": [qstr(u0), qstr(u1)],
            "v": [qstr(v0), qstr(v1)],
        },
        "contained_2d_level": row2[0],
        "contained_2d_rank_decimal_digits":
            encoded2["decimal_digit_count"],
        "contained_2d_rank_decimal_sha256":
            encoded2["sha256_of_decimal"],
        "contained_1d_level": row1[0],
        "contained_1d_rank_decimal_digits":
            encoded1["decimal_digit_count"],
        "contained_1d_rank_decimal_sha256":
            encoded1["sha256_of_decimal"],
        "natural_short_cell_k": None,
    }
    return result, replay


def evaluate_document(
    document: dict[str, Any],
    expected: dict[str, Any],
) -> None:
    require(
        set(document) == {"schema", "result", "result_sha256"},
        "closed certificate envelope",
    )
    require(document["schema"] == CERTIFICATE_SCHEMA, "certificate schema")
    result = document["result"]
    require(type(result) is dict, "certificate result object")
    require(document["result_sha256"] == digest(result), "certificate closure")
    require(result == expected, "independent expected result equality")
    require(
        document["result_sha256"] == CERTIFICATE_RESULT_SHA256,
        "frozen certificate result digest",
    )


def resign(document: dict[str, Any]) -> None:
    document["result_sha256"] = digest(document["result"])


def set_path(
    document: dict[str, Any],
    path: tuple[Any, ...],
    value: Any,
) -> None:
    target: Any = document
    for key in path[:-1]:
        target = target[key]
    target[path[-1]] = value
    resign(document)


def semantic_mutations(
    certificate: dict[str, Any],
    expected: dict[str, Any],
) -> list[str]:
    mutations: list[tuple[str, Callable[[dict[str, Any]], None]]] = []

    def simple(
        label: str,
        path: tuple[Any, ...],
        value: Any,
    ) -> None:
        mutations.append((label, lambda d, p=path, v=value: set_path(d, p, v)))

    simple("schema altered", ("schema",), "bad")
    simple(
        "producer pin altered",
        ("result", "provenance", "producer_sha256"),
        "0" * 64,
    )
    simple(
        "Round139 certificate pin altered",
        ("result", "provenance", "dependency_sha256", ROUND139),
        "0" * 64,
    )
    simple(
        "Round139 producer pin altered",
        ("result", "provenance", "dependency_sha256", ROUND139_PRODUCER),
        "0" * 64,
    )
    simple(
        "Round139 verifier pin altered",
        ("result", "provenance", "dependency_sha256", ROUND139_VERIFIER),
        "0" * 64,
    )
    simple(
        "historical identifier minted",
        ("result", "provenance", "historical_identifiers_minted"),
        True,
    )
    simple(
        "path source altered",
        ("result", "materialized_source_core_path_tuple", "payload", 0),
        "core:bad",
    )
    simple(
        "return depth altered",
        ("result", "materialized_source_core_path_tuple", "return_depth"),
        RETURN_DEPTH - 1,
    )
    simple(
        "first official word altered",
        ("result", "materialized_source_core_path_tuple", "payload", 2, 0),
        "gate5-word:bad",
    )
    simple(
        "path tuple digest altered",
        ("result", "materialized_source_core_path_tuple", "payload_sha256"),
        "0" * 64,
    )
    simple(
        "fixed s altered",
        ("result", "fixed_parameter_and_exact_implicit_leaf", "s"),
        "1/1000",
    )
    simple(
        "b_star outer called exact rational",
        (
            "result",
            "fixed_parameter_and_exact_implicit_leaf",
            "b_star_outer_is_an_enclosure_not_a_rational_replacement",
        ),
        False,
    )
    simple(
        "root uniqueness altered",
        (
            "result",
            "fixed_parameter_and_exact_implicit_leaf",
            "deep_D0_root_unique",
        ),
        False,
    )
    simple(
        "first incidence altered",
        ("result", "incidence_rank_and_density_mesh", "incidence_rank_path", 0),
        13,
    )
    simple(
        "incidence RLE altered",
        (
            "result",
            "incidence_rank_and_density_mesh",
            "incidence_rank_path_run_length_encoding",
            0,
            1,
        ),
        RETURN_DEPTH - 1,
    )
    simple(
        "B altered",
        ("result", "incidence_rank_and_density_mesh", "B"),
        15,
    )
    simple(
        "delta altered",
        ("result", "incidence_rank_and_density_mesh", "delta_14"),
        "1/4194304",
    )
    simple(
        "2D level altered",
        (
            "result",
            "Round137_v1_contained_2d_basis_rank",
            "contained_primitive_basis_row",
            0,
        ),
        RANK_2D_LEVEL - 1,
    )
    simple(
        "2D endpoint altered",
        (
            "result",
            "Round137_v1_contained_2d_basis_rank",
            "contained_primitive_basis_row",
            1,
        ),
        1,
    )
    simple(
        "2D rank decimal altered",
        (
            "result",
            "Round137_v1_contained_2d_basis_rank",
            "contained_primitive_basis_rank",
            "decimal",
        ),
        "0",
    )
    simple(
        "2D rank digest altered",
        (
            "result",
            "Round137_v1_contained_2d_basis_rank",
            "contained_primitive_basis_rank",
            "sha256_of_decimal",
        ),
        "0" * 64,
    )
    simple(
        "2D larger-component least promoted",
        (
            "result",
            "Round137_v1_contained_2d_basis_rank",
            "least_v1_rank_of_containing_component_computed",
        ),
        True,
    )
    simple(
        "2D upper-bound caveat removed",
        (
            "result",
            "Round137_v1_contained_2d_basis_rank",
            "rank_is_upper_bound_for_least_v1_rank_of_containing_component",
        ),
        False,
    )
    simple(
        "2D locator made canonical",
        (
            "result",
            "Round137_v1_contained_2d_basis_rank",
            "locator_is_noncanonical_and_does_not_deduplicate_components",
        ),
        False,
    )
    simple(
        "historical Round27 component rank minted",
        (
            "result",
            "Round137_v1_contained_2d_basis_rank",
            "historical_Round27_canonical_component_rank",
        ),
        0,
    )
    simple(
        "1D level altered",
        (
            "result",
            "Round137_v1_contained_1d_leaf_rank",
            "contained_primitive_basis_row",
            0,
        ),
        RANK_1D_LEVEL - 1,
    )
    simple(
        "1D rank decimal altered",
        (
            "result",
            "Round137_v1_contained_1d_leaf_rank",
            "contained_primitive_basis_rank",
            "decimal",
        ),
        "0",
    )
    simple(
        "1D larger-leaf least promoted",
        (
            "result",
            "Round137_v1_contained_1d_leaf_rank",
            "least_v1_rank_of_containing_U_leaf_interval_computed",
        ),
        True,
    )
    simple(
        "historical Round35 interval rank minted",
        (
            "result",
            "Round137_v1_contained_1d_leaf_rank",
            "historical_Round35_source_interval_rank",
        ),
        0,
    )
    simple(
        "maximal leaf endpoint invented",
        (
            "result",
            "natural_1e_minus_90_short_cell_audit",
            "maximal_U_intersection_leaf_endpoint_materialized",
        ),
        True,
    )
    simple(
        "oriented arclength origin invented",
        (
            "result",
            "natural_1e_minus_90_short_cell_audit",
            "historical_oriented_arclength_origin_materialized",
        ),
        True,
    )
    simple(
        "natural short-cell k minted",
        (
            "result",
            "natural_1e_minus_90_short_cell_audit",
            "natural_short_cell_k",
        ),
        0,
    )
    simple(
        "short-cell well-defined promoted",
        (
            "result",
            "natural_1e_minus_90_short_cell_audit",
            "natural_short_cell_index_well_defined_from_available_data",
        ),
        True,
    )
    simple(
        "Round35 parent-W materialized",
        (
            "result",
            "maximal_legal_Round35_field_status",
            "Round35_source_parent_W_id_materialized",
        ),
        True,
    )
    simple(
        "least component materialized",
        (
            "result",
            "maximal_legal_Round35_field_status",
            "least_Round137_v1_component_rank_materialized",
        ),
        True,
    )
    simple(
        "witness called canonical least",
        (
            "result",
            "strict_nonpromotion",
            "containing_witness_rank_is_least_canonical_rank",
        ),
        True,
    )
    simple(
        "owner count promoted",
        ("result", "strict_nonpromotion", "Round50_owner_key_count"),
        1,
    )
    simple(
        "global maturity promoted",
        ("result", "strict_nonpromotion", "global_gate5_maturity"),
        "11/18",
    )
    simple(
        "Gate5 promoted",
        ("result", "strict_nonpromotion", "Gate5"),
        "CERTIFIED",
    )
    simple(
        "CM2 promoted",
        ("result", "strict_nonpromotion", "CM2"),
        "CERTIFIED",
    )
    simple(
        "historical parent count promoted",
        ("result", "count_ledger", "historical_Round35_parent_W_id_count"),
        1,
    )
    simple(
        "scope broadened",
        ("result", "strict_scope"),
        "global Round35 component",
    )

    def add_extra(document: dict[str, Any]) -> None:
        document["result"]["unexpected"] = True
        resign(document)

    def delete_nonclaims(document: dict[str, Any]) -> None:
        del document["result"]["strict_nonclaims"]
        resign(document)

    mutations.extend(
        [
            ("extra result key", add_extra),
            ("strict nonclaims deleted", delete_nonclaims),
        ]
    )

    rejected: list[str] = []
    for label, mutate in mutations:
        candidate = copy.deepcopy(certificate)
        mutate(candidate)
        try:
            evaluate_document(candidate, expected)
        except VerificationError:
            rejected.append(label)
        else:
            raise VerificationError(f"semantic mutation accepted:{label}")
    require(len(rejected) == len(mutations), "all semantic mutations rejected")
    return rejected


def strict_json_attacks(valid_raw: bytes) -> list[str]:
    attacks = [
        ("duplicate key", b'{"x":1,"x":2}'),
        ("finite float", b'{"x":1.25}'),
        ("NaN", b'{"x":NaN}'),
        ("Infinity", b'{"x":Infinity}'),
        ("negative Infinity", b'{"x":-Infinity}'),
        ("negative zero integer", b'{"x":-0}'),
        ("UTF-8 BOM", b"\xef\xbb\xbf{}"),
        ("invalid UTF-8", b'{"x":"\xff"}'),
        ("trailing object", b"{}{}"),
        ("top-level array", b"[]"),
        ("unpaired surrogate", b'{"x":"\\ud800"}'),
        ("leading-zero integer", b'{"x":01}'),
        ("unterminated string", b'{"x":"bad}'),
        ("unescaped control", b'{"x":"\x01"}'),
        (
            "oversized integer",
            b'{"x":' + b"1" * (MAX_JSON_INTEGER_DIGITS + 1) + b"}",
        ),
        (
            "oversized document",
            b"{" + b" " * MAX_CERTIFICATE_BYTES + b"}",
        ),
    ]
    parsed = strict_json_bytes(
        valid_raw,
        "valid certificate",
        MAX_CERTIFICATE_BYTES,
    )
    require(parsed["schema"] == CERTIFICATE_SCHEMA, "valid strict JSON control")
    rejected: list[str] = []
    for label, raw in attacks:
        try:
            strict_json_bytes(raw, label, MAX_CERTIFICATE_BYTES)
        except (VerificationError, json.JSONDecodeError, ValueError):
            rejected.append(label)
        else:
            raise VerificationError(f"strict JSON attack accepted:{label}")
    return rejected


def path_safety_attacks() -> list[str]:
    labels: list[str] = []
    with tempfile.TemporaryDirectory(prefix="cm2-r140-parent-path-") as temporary:
        base = Path(temporary)

        def reject(label: str, operation: Callable[[], None]) -> None:
            try:
                operation()
            except (VerificationError, OSError):
                labels.append(label)
            else:
                raise VerificationError(f"path attack accepted:{label}")

        reject(
            "missing input",
            lambda: regular_single_link(base / "missing", "missing"),
        )
        directory = base / "directory"
        directory.mkdir()
        reject(
            "directory input",
            lambda: regular_single_link(directory, "directory"),
        )
        symlink = base / "symlink"
        symlink.symlink_to(CERTIFICATE)
        reject(
            "symlink input",
            lambda: regular_single_link(symlink, "symlink"),
        )
        ordinary = base / "ordinary"
        ordinary.write_bytes(b"{}")
        hardlink = base / "hardlink"
        os.link(ordinary, hardlink)
        reject(
            "multiply-linked input",
            lambda: regular_single_link(ordinary, "hardlink"),
        )
        fifo = base / "fifo"
        os.mkfifo(fifo)
        reject(
            "FIFO input",
            lambda: regular_single_link(fifo, "fifo"),
        )
        outside_copy = base / CERTIFICATE.name
        outside_copy.write_bytes(CERTIFICATE.read_bytes())
        reject(
            "certificate outside workspace",
            lambda: exact_workspace_input(
                outside_copy,
                CERTIFICATE,
                MAX_CERTIFICATE_BYTES,
            ),
        )
        oversized = base / "oversized"
        oversized.write_bytes(b"x" * (MAX_CERTIFICATE_BYTES + 1))
        reject(
            "oversized input",
            lambda: regular_single_link(
                oversized,
                "oversized",
                MAX_CERTIFICATE_BYTES,
            ),
        )
    require(len(labels) == 7, "path attack census")
    return labels


def build_verification(
    replay: dict[str, Any],
    mutations: list[str],
    strict_attacks: list[str],
    path_attacks: list[str],
) -> dict[str, Any]:
    result = {
        "status": "PASS",
        "provenance": {
            "verifier_sha256": sha256(VERIFIER),
            "producer_sha256": PRODUCER_SHA256,
            "certificate_sha256": CERTIFICATE_SHA256,
            "certificate_result_sha256": CERTIFICATE_RESULT_SHA256,
            "dependency_sha256": dict(sorted(INPUT_PINS.items())),
            "producer_imported_or_executed": False,
        },
        "independent_reconstruction": {
            **replay,
            "Round27_path_schema_checked": True,
            "Round35_historical_boundary_checked": True,
            "Round137_v1_rank_formula_reimplemented": True,
            "Round137_v1_minimal_level_and_lex_order_checked": True,
            "Round139_collision_row_closure_count_checked": RETURN_DEPTH,
            "Round139_exact_leaf_subgraph_containment_flag_checked": True,
            "larger_component_or_leaf_least_rank_computed": False,
            "contained_ranks_are_only_upper_bound_locators": True,
        },
        "adversarial_verification": {
            "semantic_mutation_test_count": len(mutations),
            "semantic_mutation_rejection_labels": mutations,
            "strict_json_attack_count": len(strict_attacks),
            "strict_json_attack_rejection_labels": strict_attacks,
            "path_safety_attack_count": len(path_attacks),
            "path_safety_attack_rejection_labels": path_attacks,
            "all_attacks_rejected": True,
        },
        "cold_replay_contract": {
            "deterministic_under_PYTHONHASHSEED": True,
            "no_network": True,
            "no_temporary_spike_dependency": True,
            "certificate_and_all_inputs_byte_pinned": True,
            "producer_not_imported": True,
        },
        "strict_nonpromotion": {
            "historical_Round27_component_rank": None,
            "historical_Round35_source_interval_rank": None,
            "natural_1e_minus_90_short_cell_k": None,
            "Round35_source_parent_W_id": None,
            "Round35_restriction_id": None,
            "Round50_owner_key_count": 0,
            "Round54_t54_token_count": 0,
            "Round67_q_j_output_count": 0,
            "global_complete_18_field_block_count": 0,
            "Gate5": "NOT_CERTIFIED",
            "CM2": "NO-GO_FOR_CLAIM",
        },
    }
    return {
        "schema": VERIFICATION_SCHEMA,
        "result": result,
        "result_sha256": digest(result),
    }


def write_atomic(path: Path, value: dict[str, Any]) -> None:
    require(not path.is_symlink(), "output symlink")
    resolved = path.resolve()
    protected = {
        VERIFIER,
        PRODUCER.resolve(),
        CERTIFICATE.resolve(),
        *((HERE / name).resolve() for name in INPUT_PINS),
    }
    require(resolved not in protected, "output aliases protected input")
    require(
        resolved.parent.is_dir()
        and not path.parent.is_symlink()
        and resolved.name not in {"", ".", ".."},
        "safe output parent",
    )
    if path.exists():
        regular_single_link(path, path.name)
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
    parser.add_argument("--certificate", type=Path, default=CERTIFICATE)
    parser.add_argument("--output", type=Path, default=OUTPUT)
    args = parser.parse_args()
    try:
        certificate_raw = validate_pins(args.certificate)
        certificate = strict_json_bytes(
            certificate_raw,
            CERTIFICATE.name,
            MAX_CERTIFICATE_BYTES,
        )
        expected, replay = reconstruct_expected()
        evaluate_document(certificate, expected)
        mutations = semantic_mutations(certificate, expected)
        strict_attacks = strict_json_attacks(certificate_raw)
        path_attacks = path_safety_attacks()
        verification = build_verification(
            replay,
            mutations,
            strict_attacks,
            path_attacks,
        )
        write_atomic(args.output, verification)
    except (VerificationError, OSError, ValueError, KeyError) as exc:
        print(
            canonical({"status": "FAIL", "reason": str(exc)}),
            file=sys.stderr,
        )
        return 1
    print(canonical({
        "status": "PASS",
        "semantic_mutations": len(mutations),
        "strict_json_attacks": len(strict_attacks),
        "path_safety_attacks": len(path_attacks),
        "path_tuple_sha256": replay["source_path_tuple_sha256"],
        "contained_2d_rank_sha256":
            replay["contained_2d_rank_decimal_sha256"],
        "contained_1d_rank_sha256":
            replay["contained_1d_rank_decimal_sha256"],
        "natural_short_cell_k": None,
    }))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
