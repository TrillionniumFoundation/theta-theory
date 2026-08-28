#!/usr/bin/env python3
"""Independent fail-closed verifier for the Round140 identity bridge.

The producer is neither imported nor executed.  From byte-pinned historical
inputs and the Round139 positive-area cylinder, this verifier independently
rebuilds the exact Round27 path tuple, the versioned fixed-s adaptive-cell ID,
the contained Round137-v1 dyadic basis row/rank, and every strict
non-substitution statement in the Round140 result.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
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
    HERE / "cm2_round140_fixed_s_adaptive_component_identity_bridge.py"
)
CERTIFICATE = (
    HERE
    / "cm2-round140-fixed-s-adaptive-component-identity-bridge-2026-07-24.json"
)
OUTPUT = (
    HERE
    / "cm2-round140-fixed-s-adaptive-component-identity-bridge-verification-2026-07-24.json"
)

ROUND27 = (
    HERE / "cm2-gate34-round27-arbitrary-n-path-schema-manifest-2026-07-18.json"
)
ROUND35 = (
    HERE
    / "cm2-gate45-round35-arbitrary-rn-common-carrier-manifest-2026-07-19.json"
)
ROUND133 = (
    HERE
    / "cm2-round133-round132-owner-map-realizability-audit-2026-07-24.json"
)
ROUND137 = (
    HERE
    / "cm2-round137-seed-independent-dyadic-basis-rank-contract-2026-07-24.json"
)
ROUND139 = (
    HERE
    / "cm2-round139-rank3-minus-d0-adjacent-h1-collar-return-frontier-2026-07-24.json"
)
ROUND139_SOURCE = (
    HERE
    / "cm2_round139_rank3_minus_d0_adjacent_h1_collar_return_frontier.py"
)

CERTIFICATE_SCHEMA = (
    "cm2.round140.fixed-s-adaptive-component-identity-bridge.v1"
)
VERIFICATION_SCHEMA = (
    "cm2.round140.fixed-s-adaptive-component-identity-bridge-verification.v1"
)

# Development pins are replaced after the final Round139 reseal.
PRODUCER_SHA256 = (
    "838d5ffbedd88856df561f5b6343d63466d03cab89189b3bc4eb4838f65ad4e2"
)
CERTIFICATE_SHA256 = (
    "e3f08525e770829c3ce71fed872a18dbfdc3139f514c3f865d12f6abc114a353"
)
CERTIFICATE_RESULT_SHA256 = (
    "60a364ec21cc1bedf83f7287a7e8f4e9a90a2be431d04cec8fed3f9c0102496b"
)
ROUND139_SOURCE_SHA256 = (
    "462ffcb41ba24771ce655ddb3ad5f18d5a22c8d0cb443ec1791ea9272d3d512b"
)
PINS = {
    ROUND27.name:
        "988f364bd1e6943178238c072e725de01af36452ef25d179eae6aef4000f7916",
    ROUND35.name:
        "ece7c97beeeb0b527434dc430e247ad0af407dc58b82d634da9e34a2f9e9521c",
    ROUND133.name:
        "a020ce376c1398384e5f304aff320aa214721f5f8d8bcc1e35bfa31eadd54c91",
    ROUND137.name:
        "06918b7bbfdeed9bda41a1220a25b630df6eaaa5f06024757f25a8c9fe7b88bf",
    ROUND139.name:
        "64e91e6b1efcb2675982fbc453b08349b003c8be5b4d236f61e1392aaee045f0",
}

SOURCE_CORE_ID = (
    "core:90398e9ab632e57b027266bc7c34461a0a6a6d308c35fbeacc41432a3d7f48f7"
)
RETURN_DEPTH = 1648
EXPECTED_WORD_SEQUENCE_SHA256 = (
    "f504289edce554d47e17a90d7c886586a69f3ec4b64fafd90c718c50ca93221e"
)
EXPECTED_PATH_TUPLE_SHA256 = (
    "5cec1061ec331e8f37929dfb1b2b2a78757309ba60198d571abd9e8cf6c70ed9"
)
MAX_DOCUMENT_BYTES = 12_000_000
MAX_INTEGER_DIGITS = 10_000


class VerificationError(RuntimeError):
    pass


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


def with_hash(row: dict[str, Any]) -> dict[str, Any]:
    require("row_sha256" not in row, "row already closed")
    return {**row, "row_sha256": digest(row)}


def verify_row(row: dict[str, Any], label: str) -> None:
    require(type(row) is dict, f"row object:{label}")
    body = dict(row)
    recorded = body.pop("row_sha256", None)
    require(recorded == digest(body), f"row closure:{label}")


def encoded_integer(value: int) -> dict[str, Any]:
    require(type(value) is int and value >= 0, "encoded integer")
    decimal = str(value)
    return {
        "decimal": decimal,
        "bit_length": value.bit_length(),
        "decimal_digit_count": len(decimal),
        "sha256_of_decimal":
            hashlib.sha256(decimal.encode("ascii")).hexdigest(),
    }


def strict_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        require(type(key) is str and key not in result, "duplicate JSON key")
        result[key] = value
    return result


def strict_integer(token: str) -> int:
    require(token != "-0", "negative zero integer")
    require(len(token.lstrip("-")) <= MAX_INTEGER_DIGITS, "oversized integer")
    return int(token)


def reject_float(token: str) -> float:
    raise VerificationError(f"floating JSON number forbidden:{token}")


def reject_constant(token: str) -> None:
    raise VerificationError(f"non-finite JSON constant:{token}")


def validate_strings(value: Any) -> None:
    if isinstance(value, str):
        require(
            all(not (0xD800 <= ord(character) <= 0xDFFF) for character in value),
            "unpaired surrogate",
        )
    elif isinstance(value, list):
        for child in value:
            validate_strings(child)
    elif isinstance(value, dict):
        for key, child in value.items():
            validate_strings(key)
            validate_strings(child)


def strict_json_bytes(raw: bytes, label: str) -> dict[str, Any]:
    require(len(raw) <= MAX_DOCUMENT_BYTES, f"document size:{label}")
    require(not raw.startswith(b"\xef\xbb\xbf"), f"UTF-8 BOM:{label}")
    try:
        value = json.loads(
            raw.decode("utf-8"),
            object_pairs_hook=strict_pairs,
            parse_int=strict_integer,
            parse_float=reject_float,
            parse_constant=reject_constant,
        )
    except (UnicodeError, json.JSONDecodeError, ValueError) as exc:
        raise VerificationError(f"strict JSON:{label}") from exc
    require(type(value) is dict, f"top-level JSON object:{label}")
    validate_strings(value)
    return value


def strict_json(path: Path) -> dict[str, Any]:
    require(path.exists(), f"missing input:{path.name}")
    metadata = path.lstat()
    require(
        stat.S_ISREG(metadata.st_mode)
        and metadata.st_nlink == 1
        and not path.is_symlink()
        and path.resolve().parent == HERE,
        f"unsafe input:{path.name}",
    )
    return strict_json_bytes(path.read_bytes(), path.name)


def safe_certificate_path(path: Path) -> Path:
    expanded = path.expanduser()
    require(not expanded.is_symlink(), "certificate symlink")
    try:
        metadata = expanded.lstat()
    except FileNotFoundError as exc:
        raise VerificationError("missing certificate") from exc
    require(stat.S_ISREG(metadata.st_mode), "certificate regular file")
    require(metadata.st_nlink == 1, "certificate single hardlink")
    require(metadata.st_size <= MAX_DOCUMENT_BYTES, "certificate byte cap")
    resolved = expanded.resolve()
    require(sha256(resolved) == CERTIFICATE_SHA256, "certificate byte pin")
    return resolved


def closed_result(document: dict[str, Any], schema: str, label: str) -> dict[str, Any]:
    require(
        set(document) == {"schema", "result", "result_sha256"},
        f"closed envelope:{label}",
    )
    require(document["schema"] == schema, f"schema:{label}")
    require(
        type(document["result"]) is dict
        and document["result_sha256"] == digest(document["result"]),
        f"result closure:{label}",
    )
    return document["result"]


def load_inputs() -> dict[str, dict[str, Any]]:
    for path, label in (
        (PRODUCER, "producer"),
        (ROUND139_SOURCE, "Round139 source"),
    ):
        metadata = path.lstat()
        require(
            stat.S_ISREG(metadata.st_mode)
            and metadata.st_nlink == 1
            and not path.is_symlink()
            and path.resolve().parent == HERE,
            f"safe {label}",
        )
    require(sha256(PRODUCER) == PRODUCER_SHA256, "producer byte pin")
    require(sha256(CERTIFICATE) == CERTIFICATE_SHA256, "certificate byte pin")
    require(
        sha256(ROUND139_SOURCE) == ROUND139_SOURCE_SHA256,
        "Round139 source byte pin",
    )
    loaded: dict[str, dict[str, Any]] = {}
    for path in (ROUND27, ROUND35, ROUND133, ROUND137, ROUND139):
        require(sha256(path) == PINS[path.name], f"dependency byte pin:{path.name}")
        loaded[path.name] = strict_json(path)
    return loaded


def first_consecutive_pair(lower: Q, upper: Q, level: int) -> tuple[int, int] | None:
    require(Q(0) < lower < upper < Q(1), "normalized open interval")
    scale = 1 << level
    first = lower.numerator * scale // lower.denominator + 1
    second = first + 1
    if (
        1 <= first < second <= scale - 1
        and lower < Q(first, scale) < Q(second, scale) < upper
    ):
        return first, second
    return None


def necessary_width_level(width: Q) -> int:
    """First level where width*2^level>1, independently of grid alignment."""
    require(Q(0) < width < Q(1), "normalized width")
    level = max(2, width.denominator.bit_length() - width.numerator.bit_length())
    while width * (1 << level) <= 1:
        level += 1
    while level > 2 and width * (1 << (level - 1)) > 1:
        level -= 1
    return level


def independently_locate_box(
    u0: Q,
    u1: Q,
    v0: Q,
    v1: Q,
) -> tuple[int, int, int, int, int]:
    level = max(
        necessary_width_level(u1 - u0),
        necessary_width_level(v1 - v0),
    )
    while True:
        u_pair = first_consecutive_pair(u0, u1, level)
        v_pair = first_consecutive_pair(v0, v1, level)
        if u_pair is not None and v_pair is not None:
            break
        level += 1
    require(
        level == 2
        or first_consecutive_pair(u0, u1, level - 1) is None
        or first_consecutive_pair(v0, v1, level - 1) is None,
        "minimal simultaneous contained level",
    )
    return (level, *u_pair, *v_pair)


def pair_count(level: int) -> int:
    if level < 2:
        return 0
    point_count = (1 << level) - 1
    return point_count * (point_count - 1) // 2


def pair_position(level: int, left: int, right: int) -> int:
    maximum = (1 << level) - 1
    require(1 <= left < right <= maximum, "pair range")
    # Sum_{i=1}^{left-1} (maximum-i), then offset within the left block.
    earlier = left - 1
    return (
        earlier * maximum
        - earlier * (earlier + 1) // 2
        + right - left - 1
    )


def even_pairs_preceding(level: int, left: int, right: int) -> int:
    require(1 <= left < right <= (1 << level) - 1, "even pair range")
    reduced_maximum = (1 << (level - 1)) - 1
    earlier_even_left = (left - 1) // 2
    count = (
        earlier_even_left * reduced_maximum
        - earlier_even_left * (earlier_even_left + 1) // 2
    )
    if left % 2 == 0:
        count += max(0, (right - 1) // 2 - left // 2)
    return count


def independently_rank_box(row: tuple[int, int, int, int, int]) -> int:
    level, a0, a1, b0, b1 = row
    require(any(item % 2 for item in (a0, a1, b0, b1)), "primitive box")
    total = pair_count(level)
    reduced = pair_count(level - 1)
    a_position = pair_position(level, a0, a1)
    a_even = a0 % 2 == 0 and a1 % 2 == 0
    before_a = (
        a_position * total
        - even_pairs_preceding(level, a0, a1) * reduced
    )
    b_position = pair_position(level, b0, b1)
    if a_even:
        require(b0 % 2 or b1 % 2, "primitive second pair")
        within_a = b_position - even_pairs_preceding(level, b0, b1)
    else:
        within_a = b_position
    return reduced * reduced + before_a + within_a


def validate_historical_inputs(loaded: dict[str, dict[str, Any]]) -> None:
    r27 = loaded[ROUND27.name]
    require(
        r27["schema"] == "cm2.gate34.round27-arbitrary-n-path-schema.manifest.v1"
        and r27["verdict"][
            "C24_arbitrary_n_full_dimensional_candidate_path_coverage"
        ] == "CERTIFIED_MOD_SINGULAR_NULL"
        and r27["verdict"][
            "arbitrary_n_regular_connected_component_existence_schema"
        ] == "CERTIFIED_NONCONSTRUCTIVE"
        and r27["verdict"][
            "nonempty_component_enumeration_and_numeric_payload"
        ] == "NOT_CERTIFIED",
        "Round27 manifest",
    )
    component = r27["result"]["canonical_regular_connected_component_schema"]
    require(
        component["canonical_component_id"]
        == "c24-component:(source_core_id,n,path_key,least_dyadic_basis_index)"
        and component["component_coordinates_and_nonempty_ranks_enumerated"] is False,
        "Round27 component boundary",
    )
    r35 = loaded[ROUND35.name]
    require(
        r35["schema"]
        == "cm2.gate45.round35-arbitrary-rn-common-carrier.v1.manifest.v1"
        and r35["verdict"][
            "parameterized_schema_is_finite_component_enumeration"
        ] is False
        and r35["verdict"]["complete_18_field_operator_block_count"] == 0,
        "Round35 manifest",
    )
    parent = r35["result"]["arbitrary_Rn_parent_W_Borel_registry"]
    carrier = r35["result"]["common_forward_reverse_carrier_pair"]
    require(
        parent["component_id_schema"]
        == "c24-component:(source-core-id,n,path-key,least-dyadic-basis-index)"
        and parent["nonempty_component_coordinates_enumerated"] is False
        and carrier["common_physical_restriction_id"]
        == "rn-restriction:(component-id):(source-parent-W-id):(image-recut-rank)",
        "Round35 identity boundary",
    )
    r133 = closed_result(
        loaded[ROUND133.name],
        "cm2.round133.round132-owner-map-realizability-audit.v1",
        "Round133",
    )
    require(
        r133["count_ledger"]["minimum_replacement_contract_field_count"] == 17,
        "Round133 replacement contract",
    )
    r137 = closed_result(
        loaded[ROUND137.name],
        "cm2.round137.seed-independent-dyadic-basis-rank-contract.v1",
        "Round137",
    )
    require(
        r137["strict_nonpromotion"][
            "historical_Round27_canonical_component_rank"
        ] is None
        and r137["strict_nonpromotion"]["historical_Round27_c24_component_id"]
        is None,
        "Round137 nonpromotion boundary",
    )


def rebuild_expected(loaded: dict[str, dict[str, Any]]) -> dict[str, Any]:
    validate_historical_inputs(loaded)
    r139 = closed_result(
        loaded[ROUND139.name],
        "cm2.round139.rank3-minus-d0-adjacent-h1-collar-return-frontier.v1",
        "Round139",
    )
    require(
        r139["provenance"]["producer_sha256"] == ROUND139_SOURCE_SHA256,
        "Round139 envelope producer provenance",
    )
    cylinder = r139["nested_positive_area_R1648_cylinder"]
    verify_row(cylinder, "Round139 positive cylinder")
    summary = r139["positive_area_first_return_summary"]
    rows = r139["positive_area_collision_rows"]
    require(
        type(rows) is list
        and len(rows) == RETURN_DEPTH
        and r139["positive_area_collision_rows_sha256"] == digest(rows),
        "Round139 positive rows closure",
    )
    for index, row in enumerate(rows, start=1):
        verify_row(row, f"Round139 positive collision {index}")
        require(
            row["collision_index"] == index
            and row["incidence_rank_B"] == 14
            and row["homogeneity_label"] == "H0_CENTRAL",
            f"Round139 collision type:{index}",
        )
    require(
        r139["corrected_rank3_source_contract"]["source_core_id"]
        == SOURCE_CORE_ID
        and cylinder["object_kind"]
        == "LOCAL_POSITIVE_AREA_FIXED_S_R1648_CYLINDER"
        and cylinder["s_box"] == ["0", "0"]
        and cylinder["positive_area"] is True
        and cylinder["whole_box_D3_anchor_discriminant_strictly_negative"] is True
        and summary["object_kind"] == "POSITIVE_AREA_FIXED_S_RECTANGLE_CYLINDER"
        and summary["ordinary_positive_area_rectangle"] is True
        and summary["first_return_depth"] == RETURN_DEPTH
        and summary["strict_first_return_whole_positive_area_rectangle"] is True
        and summary["all_official_words_whole_collar_strict"] is True
        and summary["all_other_owner_decisions_whole_collar_strict"] is True
        and summary["all_homogeneity_and_incidence_decisions_whole_collar_strict"]
        is True
        and summary["collision3_analytic_anchor_exclusion_used"] is False,
        "Round139 ordinary positive-area first return",
    )

    official_ids = [
        row["official_word_key"]["official_word_key_id"] for row in rows
    ]
    official_sha = digest(official_ids)
    path_sha = digest([SOURCE_CORE_ID, RETURN_DEPTH, official_ids])
    require(
        official_sha == EXPECTED_WORD_SEQUENCE_SHA256
        and path_sha == EXPECTED_PATH_TUPLE_SHA256
        and summary["official_word_key_sequence_sha256"] == official_sha,
        "exact Round27 path tuple",
    )
    path_row = with_hash({
        "schema": "round140-round27-path-instance-v1",
        "source_core_id": SOURCE_CORE_ID,
        "return_depth_n": RETURN_DEPTH,
        "official_word_key_occurrence_count": RETURN_DEPTH,
        "official_word_key_sequence_sha256": official_sha,
        "Round27_compatible_candidate_path_tuple_sha256": path_sha,
        "candidate_path_key_grammar":
            "c24-path:(source_core_id,n,k_1,...,k_n)",
        "candidate_path_key_id": "round140-c24-path-instance:" + path_sha,
        "positive_area_nonempty_path_fibre_witness": True,
    })

    t0, t1 = (Q(value) for value in cylinder["t_box"])
    p0, p1 = (Q(value) for value in cylinder["p_box"])
    area = (t1 - t0) * (p1 - p0)
    require(
        Q(1, 100) < t0 < t1 < Q(1, 50)
        and Q(-1, 500) < p0 < p1 < Q(1, 500)
        and area > 0
        and Q(cylinder["area"]) == area,
        "positive rectangle geometry",
    )
    endpoint_policy = {
        "component_support": "open rectangle (t0,t1) x (p0,p1) at s=0",
        "artificial_face_policy":
            "all four rational rectangle faces excluded from this adaptive component",
        "global_endpoint_owner_partition_claimed": False,
        "historical_Q2_s_endpoint_owner_inherited": False,
        "reason":
            "the bridge names one open adaptive cell and does not retrofit ownership to frozen Q2 endpoint faces",
    }
    identity_payload = [
        "round140-fixed-s0-adaptive-path-cell-v1",
        SOURCE_CORE_ID,
        RETURN_DEPTH,
        path_sha,
        [qstr(t0), qstr(t1)],
        [qstr(p0), qstr(p1)],
        cylinder["row_sha256"],
        r139["positive_area_collision_rows_sha256"],
        endpoint_policy,
    ]
    adaptive_id = (
        "round140-fixed-s0-adaptive-path-cell:" + digest(identity_payload)
    )
    adaptive_row = with_hash({
        "adaptive_path_cell_id": adaptive_id,
        "identity_payload_sha256": digest(identity_payload),
        "fixed_parameter_s": "0",
        "source_core_id": SOURCE_CORE_ID,
        "return_depth_n": RETURN_DEPTH,
        "Round27_path_tuple_sha256": path_sha,
        "t_open_interval": [qstr(t0), qstr(t1)],
        "p_open_interval": [qstr(p0), qstr(p1)],
        "positive_collision_area": qstr(area),
        "closure_strictly_inside_source_core": True,
        "closure_has_one_strict_ordinary_owner_path": True,
        "closure_first_return_is_exactly_R1648": True,
        "open_support_connected": True,
        "adaptive_registry_connected_rank": 0,
        "endpoint_policy": endpoint_policy,
        "component_type":
            "CONNECTED_COMPONENT_OF_THIS_ONE_CELL_FINITE_ADAPTIVE_REGISTRY",
    })

    r137 = loaded[ROUND137.name]["result"]
    normalization_rows = r137[
        "source_core_affine_normalization_contract"
    ]["normalization_rows"]
    matching = [
        row for row in normalization_rows
        if row["source_core_id"] == SOURCE_CORE_ID
    ]
    require(len(matching) == 1, "unique source normalization")
    normalization = matching[0]
    verify_row(normalization, "source normalization")
    ct0, ct1 = (Q(value) for value in normalization["t_bounds"])
    cp0, cp1 = (Q(value) for value in normalization["p_bounds"])
    u0, u1 = (t0 - ct0) / (ct1 - ct0), (t1 - ct0) / (ct1 - ct0)
    v0, v1 = (p0 - cp0) / (cp1 - cp0), (p1 - cp0) / (cp1 - cp0)
    basis_row = independently_locate_box(u0, u1, v0, v1)
    level, a0, a1, b0, b1 = basis_row
    scale = 1 << level
    require(
        u0 < Q(a0, scale) < Q(a1, scale) < u1
        and v0 < Q(b0, scale) < Q(b1, scale) < v1,
        "basis closure inside adaptive cell",
    )
    basis_rank = independently_rank_box(basis_row)
    locator_payload = [
        "round140-containing-component-upper-bound-locator-v1",
        adaptive_id,
        "round137-dyadic-basis-enumeration-v1",
        list(basis_row),
        str(basis_rank),
    ]
    locator_id = (
        "round140-containing-component-upper-bound-locator:"
        + digest(locator_payload)
    )
    basis_witness = {
        "contract": "round137-dyadic-basis-enumeration-v1",
        "normalized_source_box": {
            "u": [qstr(u0), qstr(u1)],
            "v": [qstr(v0), qstr(v1)],
        },
        "contained_primitive_basis_row": list(basis_row),
        "contained_primitive_basis_denominator_power": level,
        "contained_primitive_basis_rank": encoded_integer(basis_rank),
        "basis_closure_strictly_inside_adaptive_path_cell": True,
        "minimal_level_with_two_strict_consecutive_grid_points_in_each_coordinate":
            True,
        "lex_first_consecutive_pairs_at_that_level": True,
        "containing_component_rank_upper_bound": encoded_integer(basis_rank),
        "upper_bound_locator_id": locator_id,
        "upper_bound_locator_payload_sha256": digest(locator_payload),
        "least_rank_of_maximal_component_computed": False,
    }

    component_payload = [
        "round140-unique-containing-maximal-component-locator-v1",
        SOURCE_CORE_ID,
        RETURN_DEPTH,
        path_sha,
        adaptive_id,
    ]
    component_locator = (
        "round140-unique-containing-maximal-component-locator:"
        + digest(component_payload)
    )
    component_bridge = {
        "regular_path_fibre":
            "R_1648 intersect fibre(Round27 candidate path) at fixed s=0",
        "adaptive_open_cell_is_subset_of_regular_path_fibre": True,
        "adaptive_open_cell_is_connected": True,
        "unique_containing_maximal_connected_component_exists": True,
        "unique_containing_component_locator_id": component_locator,
        "unique_containing_component_locator_payload_sha256":
            digest(component_payload),
        "locator_is_set_theoretic_not_historical_canonical_ID": True,
        "adaptive_cell_equals_maximal_path_component": False,
        "nonmaximality_reason":
            "the four adaptive rectangle faces are artificial while all physical path predicates remain strict on the closed rectangle; continuity extends the same path across each face locally",
        "historical_Round27_least_basis_rank": None,
        "historical_Round27_c24_component_id": None,
        "Round137_v1_least_rank_of_containing_component": None,
        "Round137_v1_upper_bound_locator": locator_id,
    }
    substitution = {
        "adaptive_path_cell_ID_is_deterministic": True,
        "adaptive_path_cell_ID_may_replace_Round27_canonical_component_ID": False,
        "adaptive_registry_connected_rank_0_may_replace_Round27_least_basis_rank":
            False,
        "incidence_rank_14_may_replace_Round27_component_rank": False,
        "Round137_contained_basis_upper_bound_may_be_called_least": False,
        "unique_containing_component_locator_may_replace_component_ID": False,
        "Round35_parent_W_ID_materialized": False,
        "Round35_short_cell_k_materialized": False,
        "Round35_image_recut_rank_materialized": False,
        "Round35_restriction_ID_materialized": False,
        "minimal_historical_route_blocker": (
            "certify the maximal connected component U of the complete regular "
            "R_1648 path fibre, adopt an executable dyadic basis enumeration for "
            "the historical Round27 schema, and prove the least closure-contained "
            "basis rank by both positive membership and exclusion of every earlier rank"
        ),
        "available_positive_membership_oracle":
            "ordinary interval replay certifies closure(box) lies in the fixed R_1648 path; overlapping certified boxes give a connected same-component corridor",
        "missing_negative_oracle":
            "failure of interval replay is inconclusive and there is no complete outer boundary atlas for excluding an earlier basis box from U",
        "legal_versioned_alternative": (
            "prove a new countable Borel adaptive-refinement invariance theorem "
            "for Round35/50 and version their component/restriction token schemas; "
            "without that theorem this bridge is not a Round35 component"
        ),
    }
    field_rows = [
        {"field_index": 3, "field": "Round50_restriction_id", "status": "MISSING"},
        {"field_index": 6, "field": "arbitrary_Rn_path_key", "status": "MATERIALIZED"},
        {"field_index": 7, "field": "canonical_component_id", "status": "MISSING"},
        {
            "field_index": 11,
            "field": "connected_rank_zero_component_id",
            "status": "LOCAL_ADAPTIVE_ONLY",
        },
        {
            "field_index": 13,
            "field": "active_E_i_and_regular_R_i_witness",
            "status": "LOCAL_REGULAR_PATH_WITNESS_ONLY",
        },
    ]
    field_rows = [with_hash(row) for row in field_rows]
    result = {
        "status": "CERTIFIED_FIXED_S_ADAPTIVE_IDENTITY_STRICT_NONSUBSTITUTION",
        "provenance": {
            "dependency_sha256": dict(sorted(PINS.items())),
            "Round139_source_sha256": ROUND139_SOURCE_SHA256,
            "Round139_certificate_result_sha256":
                loaded[ROUND139.name]["result_sha256"],
            "Round139_result_read_from_certificate": True,
            "Round139_source_imported_or_executed": False,
            "append_only": True,
            "Round139_modified": False,
        },
        "Round27_path_instance": path_row,
        "fixed_s_adaptive_path_cell": adaptive_row,
        "Round137_v1_contained_basis_upper_bound": basis_witness,
        "unique_containing_maximal_component_bridge": component_bridge,
        "Round35_substitution_audit": substitution,
        "Round133_replacement_field_delta_rows": field_rows,
        "Round133_replacement_field_delta_rows_sha256": digest(field_rows),
        "strict_nonpromotion": {
            "new_Round27_nonempty_path_instance_count": 1,
            "new_fixed_s_adaptive_path_cell_count": 1,
            "new_noncanonical_containing_component_locator_count": 1,
            "new_Round137_v1_component_upper_bound_locator_count": 1,
            "new_historical_Round27_canonical_component_count": 0,
            "new_Round35_restriction_count": 0,
            "new_Round50_owner_key_count": 0,
            "new_Round54_t54_token_count": 0,
            "new_Round67_Omega_j_record_count": 0,
            "new_Round67_q_j_output_count": 0,
            "global_complete_18_field_block_count": 0,
            "global_gate5_maturity": "10/18",
            "Gate5": "NOT_CERTIFIED",
            "CM2": "NO-GO_FOR_CLAIM",
        },
        "strict_nonclaims": [
            "the adaptive rectangle is not the maximal Round27 path component",
            "adaptive connected rank zero is not the Round27 least dyadic basis rank",
            "the contained basis rank is only an upper bound for the unique containing component",
            "the set-theoretic containing-component locator is not a canonical component ID",
            "no historical Q2 s-endpoint ownership is retrofitted",
            "no Round35 restriction, Round50 owner, Round54 token or Round67 q_j row is created",
        ],
    }
    return json.loads(json.dumps(result, sort_keys=True))


def verify_document(
    document: dict[str, Any],
    loaded: dict[str, dict[str, Any]],
    *,
    enforce_frozen_result_digest: bool = True,
    expected_result: dict[str, Any] | None = None,
) -> dict[str, Any]:
    result = closed_result(document, CERTIFICATE_SCHEMA, "Round140")
    if enforce_frozen_result_digest:
        require(
            document["result_sha256"] == CERTIFICATE_RESULT_SHA256,
            "pinned Round140 result digest",
        )
    expected = (
        rebuild_expected(loaded)
        if expected_result is None
        else expected_result
    )
    require(result == expected, "independently rebuilt exact Round140 result")
    return result


def reclose(document: dict[str, Any]) -> dict[str, Any]:
    document["result_sha256"] = digest(document["result"])
    return document


def mutation_rejected(
    pristine: dict[str, Any],
    loaded: dict[str, dict[str, Any]],
    expected: dict[str, Any],
    mutate: Callable[[dict[str, Any]], None],
) -> bool:
    candidate = copy.deepcopy(pristine)
    mutate(candidate)
    reclose(candidate)
    try:
        verify_document(
            candidate,
            loaded,
            enforce_frozen_result_digest=False,
            expected_result=expected,
        )
    except (VerificationError, KeyError, TypeError, ValueError, IndexError):
        return True
    return False


def run_mutation_tests(
    pristine: dict[str, Any],
    loaded: dict[str, dict[str, Any]],
) -> dict[str, bool]:
    def assign(
        path: tuple[str | int, ...],
        replacement: Any,
    ) -> Callable[[dict[str, Any]], None]:
        def mutate(value: dict[str, Any]) -> None:
            cursor: Any = value
            for key in path[:-1]:
                cursor = cursor[key]
            cursor[path[-1]] = replacement
        return mutate

    tests: dict[str, Callable[[dict[str, Any]], None]] = {
        "certificate schema altered": assign(
            ("schema",), "cm2.round140.invalid"
        ),
        "closed envelope extra key": assign(("extra",), True),
        "closed result extra key": assign(("result", "extra"), True),
        "status promoted": assign(("result", "status"), "PASS"),
        "Round139 source pin altered": assign(
            ("result", "provenance", "Round139_source_sha256"), "0" * 64
        ),
        "Round139 certificate result pin altered": assign(
            (
                "result",
                "provenance",
                "Round139_certificate_result_sha256",
            ),
            "0" * 64,
        ),
        "Round139 certificate-read flag erased": assign(
            (
                "result",
                "provenance",
                "Round139_result_read_from_certificate",
            ),
            False,
        ),
        "Round139 source execution invented": assign(
            (
                "result",
                "provenance",
                "Round139_source_imported_or_executed",
            ),
            True,
        ),
        "Round139 certificate dependency altered": assign(
            (
                "result",
                "provenance",
                "dependency_sha256",
                ROUND139.name,
            ),
            "0" * 64,
        ),
        "path source core altered": assign(
            ("result", "Round27_path_instance", "source_core_id"),
            "core:" + "0" * 64,
        ),
        "path return depth altered": assign(
            ("result", "Round27_path_instance", "return_depth_n"), 1647
        ),
        "path occurrence count altered": assign(
            (
                "result",
                "Round27_path_instance",
                "official_word_key_occurrence_count",
            ),
            1647,
        ),
        "official word sequence digest altered": assign(
            (
                "result",
                "Round27_path_instance",
                "official_word_key_sequence_sha256",
            ),
            "0" * 64,
        ),
        "Round27 tuple digest altered": assign(
            (
                "result",
                "Round27_path_instance",
                "Round27_compatible_candidate_path_tuple_sha256",
            ),
            "0" * 64,
        ),
        "candidate path ID altered": assign(
            ("result", "Round27_path_instance", "candidate_path_key_id"),
            "round140-c24-path-instance:" + "0" * 64,
        ),
        "nonempty path witness erased": assign(
            (
                "result",
                "Round27_path_instance",
                "positive_area_nonempty_path_fibre_witness",
            ),
            False,
        ),
        "adaptive ID altered": assign(
            (
                "result",
                "fixed_s_adaptive_path_cell",
                "adaptive_path_cell_id",
            ),
            "round140-fixed-s0-adaptive-path-cell:" + "0" * 64,
        ),
        "fixed s altered": assign(
            ("result", "fixed_s_adaptive_path_cell", "fixed_parameter_s"),
            "1/1000",
        ),
        "adaptive t interval altered": assign(
            ("result", "fixed_s_adaptive_path_cell", "t_open_interval"),
            ["0", "1"],
        ),
        "adaptive p interval altered": assign(
            ("result", "fixed_s_adaptive_path_cell", "p_open_interval"),
            ["0", "1"],
        ),
        "adaptive area altered": assign(
            (
                "result",
                "fixed_s_adaptive_path_cell",
                "positive_collision_area",
            ),
            "0",
        ),
        "adaptive connectedness erased": assign(
            ("result", "fixed_s_adaptive_path_cell", "open_support_connected"),
            False,
        ),
        "adaptive rank changed": assign(
            (
                "result",
                "fixed_s_adaptive_path_cell",
                "adaptive_registry_connected_rank",
            ),
            1,
        ),
        "historical endpoint ownership retrofitted": assign(
            (
                "result",
                "fixed_s_adaptive_path_cell",
                "endpoint_policy",
                "historical_Q2_s_endpoint_owner_inherited",
            ),
            True,
        ),
        "global endpoint partition invented": assign(
            (
                "result",
                "fixed_s_adaptive_path_cell",
                "endpoint_policy",
                "global_endpoint_owner_partition_claimed",
            ),
            True,
        ),
        "adaptive component type promoted": assign(
            ("result", "fixed_s_adaptive_path_cell", "component_type"),
            "HISTORICAL_ROUND27_MAXIMAL_COMPONENT",
        ),
        "basis contract altered": assign(
            (
                "result",
                "Round137_v1_contained_basis_upper_bound",
                "contract",
            ),
            "historical-Round27-enumeration",
        ),
        "basis row altered": assign(
            (
                "result",
                "Round137_v1_contained_basis_upper_bound",
                "contained_primitive_basis_row",
            ),
            [2, 1, 2, 1, 2],
        ),
        "basis level altered": assign(
            (
                "result",
                "Round137_v1_contained_basis_upper_bound",
                "contained_primitive_basis_denominator_power",
            ),
            2,
        ),
        "basis rank altered": assign(
            (
                "result",
                "Round137_v1_contained_basis_upper_bound",
                "contained_primitive_basis_rank",
                "decimal",
            ),
            "0",
        ),
        "basis containment erased": assign(
            (
                "result",
                "Round137_v1_contained_basis_upper_bound",
                "basis_closure_strictly_inside_adaptive_path_cell",
            ),
            False,
        ),
        "minimal contained level erased": assign(
            (
                "result",
                "Round137_v1_contained_basis_upper_bound",
                "minimal_level_with_two_strict_consecutive_grid_points_in_each_coordinate",
            ),
            False,
        ),
        "lex-first basis pairs erased": assign(
            (
                "result",
                "Round137_v1_contained_basis_upper_bound",
                "lex_first_consecutive_pairs_at_that_level",
            ),
            False,
        ),
        "least maximal-component rank invented": assign(
            (
                "result",
                "Round137_v1_contained_basis_upper_bound",
                "least_rank_of_maximal_component_computed",
            ),
            True,
        ),
        "basis upper-bound locator altered": assign(
            (
                "result",
                "Round137_v1_contained_basis_upper_bound",
                "upper_bound_locator_id",
            ),
            "round140-containing-component-upper-bound-locator:" + "0" * 64,
        ),
        "adaptive cell promoted to maximal component": assign(
            (
                "result",
                "unique_containing_maximal_component_bridge",
                "adaptive_cell_equals_maximal_path_component",
            ),
            True,
        ),
        "set-theoretic locator promoted to canonical": assign(
            (
                "result",
                "unique_containing_maximal_component_bridge",
                "locator_is_set_theoretic_not_historical_canonical_ID",
            ),
            False,
        ),
        "historical least rank invented": assign(
            (
                "result",
                "unique_containing_maximal_component_bridge",
                "historical_Round27_least_basis_rank",
            ),
            0,
        ),
        "historical component ID invented": assign(
            (
                "result",
                "unique_containing_maximal_component_bridge",
                "historical_Round27_c24_component_id",
            ),
            "c24-component:invented",
        ),
        "Round137 least rank invented": assign(
            (
                "result",
                "unique_containing_maximal_component_bridge",
                "Round137_v1_least_rank_of_containing_component",
            ),
            0,
        ),
        "containing-component locator altered": assign(
            (
                "result",
                "unique_containing_maximal_component_bridge",
                "unique_containing_component_locator_id",
            ),
            "round140-unique-containing-maximal-component-locator:" + "0" * 64,
        ),
        "adaptive ID substituted for Round27 component": assign(
            (
                "result",
                "Round35_substitution_audit",
                "adaptive_path_cell_ID_may_replace_Round27_canonical_component_ID",
            ),
            True,
        ),
        "adaptive rank substituted for least rank": assign(
            (
                "result",
                "Round35_substitution_audit",
                "adaptive_registry_connected_rank_0_may_replace_Round27_least_basis_rank",
            ),
            True,
        ),
        "incidence rank substituted for component rank": assign(
            (
                "result",
                "Round35_substitution_audit",
                "incidence_rank_14_may_replace_Round27_component_rank",
            ),
            True,
        ),
        "upper bound renamed least": assign(
            (
                "result",
                "Round35_substitution_audit",
                "Round137_contained_basis_upper_bound_may_be_called_least",
            ),
            True,
        ),
        "component locator substituted for ID": assign(
            (
                "result",
                "Round35_substitution_audit",
                "unique_containing_component_locator_may_replace_component_ID",
            ),
            True,
        ),
        "Round35 parent W invented": assign(
            (
                "result",
                "Round35_substitution_audit",
                "Round35_parent_W_ID_materialized",
            ),
            True,
        ),
        "Round35 short cell invented": assign(
            (
                "result",
                "Round35_substitution_audit",
                "Round35_short_cell_k_materialized",
            ),
            True,
        ),
        "Round35 image recut invented": assign(
            (
                "result",
                "Round35_substitution_audit",
                "Round35_image_recut_rank_materialized",
            ),
            True,
        ),
        "Round35 restriction invented": assign(
            (
                "result",
                "Round35_substitution_audit",
                "Round35_restriction_ID_materialized",
            ),
            True,
        ),
        "canonical component field promoted": assign(
            (
                "result",
                "Round133_replacement_field_delta_rows",
                2,
                "status",
            ),
            "MATERIALIZED",
        ),
        "historical component count promoted": assign(
            (
                "result",
                "strict_nonpromotion",
                "new_historical_Round27_canonical_component_count",
            ),
            1,
        ),
        "Round35 restriction count promoted": assign(
            (
                "result",
                "strict_nonpromotion",
                "new_Round35_restriction_count",
            ),
            1,
        ),
        "Round50 owner count promoted": assign(
            ("result", "strict_nonpromotion", "new_Round50_owner_key_count"),
            1,
        ),
        "Round54 token count promoted": assign(
            ("result", "strict_nonpromotion", "new_Round54_t54_token_count"),
            1,
        ),
        "Round67 Omega count promoted": assign(
            (
                "result",
                "strict_nonpromotion",
                "new_Round67_Omega_j_record_count",
            ),
            1,
        ),
        "Round67 q_j count promoted": assign(
            ("result", "strict_nonpromotion", "new_Round67_q_j_output_count"),
            1,
        ),
        "complete block invented": assign(
            (
                "result",
                "strict_nonpromotion",
                "global_complete_18_field_block_count",
            ),
            1,
        ),
        "global maturity promoted": assign(
            ("result", "strict_nonpromotion", "global_gate5_maturity"),
            "11/18",
        ),
        "Gate5 promoted": assign(
            ("result", "strict_nonpromotion", "Gate5"), "CERTIFIED"
        ),
        "CM2 promoted": assign(
            ("result", "strict_nonpromotion", "CM2"), "GO_FOR_CLAIM"
        ),
        "strict nonclaim deleted": lambda value: value["result"][
            "strict_nonclaims"
        ].pop(),
    }
    expected = rebuild_expected(loaded)
    outcomes = {
        name: mutation_rejected(pristine, loaded, expected, mutation)
        for name, mutation in tests.items()
    }
    require(
        len(outcomes) == 62 and all(outcomes.values()),
        "62 semantic mutations rejected",
    )
    return outcomes


def run_parser_tests() -> dict[str, bool]:
    invalid = {
        "duplicate top-level key": b'{"x":1,"x":2}',
        "duplicate nested key": b'{"x":{"y":1,"y":2}}',
        "floating number": b'{"x":1.0}',
        "exponential number": b'{"x":1e3}',
        "NaN constant": b'{"x":NaN}',
        "positive Infinity": b'{"x":Infinity}',
        "negative Infinity": b'{"x":-Infinity}',
        "UTF-8 BOM": b'\xef\xbb\xbf{"x":1}',
        "invalid UTF-8": b'{"x":"\xff"}',
        "top-level array": b'[]',
        "top-level null": b'null',
        "trailing document": b'{"x":1}{"y":2}',
        "oversized integer": (
            b'{"x":' + b"1" * (MAX_INTEGER_DIGITS + 1) + b"}"
        ),
        "negative zero": b'{"x":-0}',
        "leading-zero integer": b'{"x":01}',
        "unpaired surrogate": b'{"x":"\\ud800"}',
        "empty document": b"",
        "unescaped control": b'{"x":"\x01"}',
    }
    outcomes: dict[str, bool] = {}
    for name, payload in invalid.items():
        try:
            strict_json_bytes(payload, name)
        except (VerificationError, UnicodeError, ValueError):
            outcomes[name] = True
        else:
            outcomes[name] = False
    require(
        len(outcomes) == 18 and all(outcomes.values()),
        "18 strict parser attacks rejected",
    )
    return outcomes


def protected_paths(certificate_path: Path) -> set[Path]:
    return {
        VERIFIER.resolve(),
        PRODUCER.resolve(),
        CERTIFICATE.resolve(),
        certificate_path.resolve(),
        ROUND139_SOURCE.resolve(),
        *((HERE / name).resolve() for name in PINS),
    }


def validate_output_target(path: Path, certificate_path: Path) -> Path:
    absolute = path.expanduser().absolute()
    parent = absolute.parent
    require(
        parent.exists()
        and parent.is_dir()
        and not parent.is_symlink()
        and parent.resolve() == parent,
        "safe output parent",
    )
    require(not absolute.is_symlink(), "output symlink")
    resolved = absolute.resolve(strict=False)
    protected = protected_paths(certificate_path)
    require(resolved not in protected, "output aliases protected input")
    if absolute.exists():
        metadata = absolute.lstat()
        require(
            stat.S_ISREG(metadata.st_mode) and metadata.st_nlink == 1,
            "safe existing output",
        )
        for item in protected:
            require(
                not item.exists() or not os.path.samefile(absolute, item),
                "output hardlink aliases protected input",
            )
    return resolved


def run_path_safety_tests(certificate_path: Path) -> dict[str, bool]:
    outcomes: dict[str, bool] = {}
    originals = {
        path: sha256(path)
        for path in protected_paths(certificate_path)
        if path.is_file()
    }

    def reject(label: str, action: Callable[[], Any]) -> None:
        try:
            action()
        except (VerificationError, OSError):
            outcomes[label] = True
        else:
            outcomes[label] = False

    with tempfile.TemporaryDirectory(prefix="cm2-r140-bridge-path-") as name:
        root = Path(name)
        copied = root / "certificate.json"
        copied.write_bytes(certificate_path.read_bytes())
        require(
            safe_certificate_path(copied) == copied.resolve(),
            "copied certificate accepted",
        )
        reject(
            "missing certificate",
            lambda: safe_certificate_path(root / "missing.json"),
        )

        input_symlink = root / "input-symlink.json"
        input_symlink.symlink_to(copied)
        reject(
            "certificate symlink",
            lambda: safe_certificate_path(input_symlink),
        )

        input_hardlink = root / "input-hardlink.json"
        os.link(copied, input_hardlink)
        reject(
            "certificate hardlink",
            lambda: safe_certificate_path(copied),
        )
        input_hardlink.unlink()

        input_fifo = root / "input-fifo"
        os.mkfifo(input_fifo)
        reject(
            "certificate FIFO",
            lambda: safe_certificate_path(input_fifo),
        )

        tampered = root / "tampered.json"
        tampered.write_bytes(certificate_path.read_bytes() + b" ")
        reject(
            "tampered certificate byte pin",
            lambda: safe_certificate_path(tampered),
        )

        reject(
            "output aliases selected certificate",
            lambda: validate_output_target(copied, copied),
        )
        reject(
            "output aliases formal certificate",
            lambda: validate_output_target(CERTIFICATE, copied),
        )
        reject(
            "output aliases producer",
            lambda: validate_output_target(PRODUCER, copied),
        )
        reject(
            "output aliases verifier",
            lambda: validate_output_target(VERIFIER, copied),
        )
        reject(
            "output aliases Round139 source",
            lambda: validate_output_target(ROUND139_SOURCE, copied),
        )
        for dependency_name in sorted(PINS):
            reject(
                f"output aliases dependency:{dependency_name}",
                lambda selected=dependency_name: validate_output_target(
                    HERE / selected,
                    copied,
                ),
            )

        output_symlink = root / "output-symlink.json"
        output_symlink.symlink_to(copied)
        reject(
            "output symlink",
            lambda: validate_output_target(output_symlink, copied),
        )

        output_hardlink = root / "output-hardlink.json"
        os.link(copied, output_hardlink)
        reject(
            "output hardlink",
            lambda: validate_output_target(output_hardlink, copied),
        )
        output_hardlink.unlink()

        output_fifo = root / "output-fifo"
        os.mkfifo(output_fifo)
        reject(
            "output FIFO",
            lambda: validate_output_target(output_fifo, copied),
        )

        output_directory = root / "output-directory"
        output_directory.mkdir()
        reject(
            "output directory",
            lambda: validate_output_target(output_directory, copied),
        )

        real_parent = root / "real-parent"
        real_parent.mkdir()
        linked_parent = root / "linked-parent"
        linked_parent.symlink_to(real_parent, target_is_directory=True)
        reject(
            "output parent symlink",
            lambda: validate_output_target(linked_parent / "out.json", copied),
        )

        fresh = root / "fresh.json"
        require(
            validate_output_target(fresh, copied) == fresh.resolve(),
            "fresh output accepted",
        )

    require(
        originals == {path: sha256(path) for path in originals},
        "protected inputs unchanged by path tests",
    )
    require(
        len(outcomes) == 20 and all(outcomes.values()),
        "20 path-safety attacks rejected",
    )
    return outcomes


def write_atomic(
    path: Path,
    value: dict[str, Any],
    certificate_path: Path,
) -> None:
    resolved = validate_output_target(path, certificate_path)
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
        with os.fdopen(
            descriptor, "w", encoding="utf-8", newline="\n"
        ) as handle:
            handle.write(payload)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary_path, resolved)
    finally:
        if temporary_path.exists():
            temporary_path.unlink()


def build_verification(certificate_path: Path) -> dict[str, Any]:
    loaded = load_inputs()
    document = strict_json_bytes(
        certificate_path.read_bytes(),
        certificate_path.name,
    )
    result = verify_document(document, loaded)
    mutation_tests = run_mutation_tests(document, loaded)
    parser_tests = run_parser_tests()
    path_tests = run_path_safety_tests(certificate_path)
    verification = {
        "status": "PASS",
        "producer_sha256": PRODUCER_SHA256,
        "certificate_sha256": CERTIFICATE_SHA256,
        "certificate_result_sha256": CERTIFICATE_RESULT_SHA256,
        "certificate_schema": CERTIFICATE_SCHEMA,
        "verifier_sha256": sha256(VERIFIER),
        "Round139_source_sha256": ROUND139_SOURCE_SHA256,
        "Round139_certificate_sha256": PINS[ROUND139.name],
        "Round139_certificate_result_sha256":
            loaded[ROUND139.name]["result_sha256"],
        "dependency_sha256": dict(sorted(PINS.items())),
        "independent_recomputation": {
            "Round139_source_imported_or_executed": False,
            "Round139_result_read_from_pinned_certificate": True,
            "Round27_path_tuple_rebuilt_from_1648_rows": True,
            "adaptive_identity_payload_and_ID_rebuilt": True,
            "positive_open_rectangle_geometry_rebuilt": True,
            "Round137_normalization_rebuilt": True,
            "minimal_contained_dyadic_basis_row_rebuilt": True,
            "global_primitive_2D_basis_rank_rebuilt": True,
            "unique_containing_component_locator_rebuilt": True,
            "strict_Round27_Round35_nonsubstitution_rebuilt": True,
            "historical_Q2_endpoint_nonretrofit_rebuilt": True,
        },
        "verified_outputs": {
            "adaptive_path_cell_id": result[
                "fixed_s_adaptive_path_cell"
            ]["adaptive_path_cell_id"],
            "Round27_path_tuple_sha256": result[
                "Round27_path_instance"
            ]["Round27_compatible_candidate_path_tuple_sha256"],
            "contained_basis_level": result[
                "Round137_v1_contained_basis_upper_bound"
            ]["contained_primitive_basis_denominator_power"],
            "contained_basis_rank_decimal_sha256": result[
                "Round137_v1_contained_basis_upper_bound"
            ]["contained_primitive_basis_rank"]["sha256_of_decimal"],
            "contained_basis_upper_bound_locator_id": result[
                "Round137_v1_contained_basis_upper_bound"
            ]["upper_bound_locator_id"],
            "historical_Round27_least_basis_rank": result[
                "unique_containing_maximal_component_bridge"
            ]["historical_Round27_least_basis_rank"],
            "historical_Round27_c24_component_id": result[
                "unique_containing_maximal_component_bridge"
            ]["historical_Round27_c24_component_id"],
            "Round35_restriction_count": result[
                "strict_nonpromotion"
            ]["new_Round35_restriction_count"],
            "global_gate5_maturity": result[
                "strict_nonpromotion"
            ]["global_gate5_maturity"],
            "CM2": result["strict_nonpromotion"]["CM2"],
        },
        "semantic_mutation_test_count": len(mutation_tests),
        "mutation_tests": mutation_tests,
        "strict_parser_test_count": len(parser_tests),
        "strict_parser_tests": parser_tests,
        "path_safety_test_count": len(path_tests),
        "path_safety_tests": path_tests,
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
            "producer_verifier_certificate_Round139_source_and_dependencies_protected":
                True,
            "input_output_alias_rejected": True,
            "symlink_hardlink_FIFO_attacks_rejected": True,
            "atomic_replace_after_fsync": True,
        },
        "strict_nonpromotion": dict(result["strict_nonpromotion"]),
    }
    verification = json.loads(json.dumps(verification, sort_keys=True))
    return {
        "schema": VERIFICATION_SCHEMA,
        "result": verification,
        "result_sha256": digest(verification),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certificate", type=Path, default=CERTIFICATE)
    parser.add_argument("--output", type=Path, default=OUTPUT)
    args = parser.parse_args()
    try:
        certificate_path = safe_certificate_path(args.certificate)
        validate_output_target(args.output, certificate_path)
        envelope = build_verification(certificate_path)
        write_atomic(args.output, envelope, certificate_path)
        print("STATUS:", envelope["result"]["status"])
        print(
            "ADAPTIVE_ID:",
            envelope["result"]["verified_outputs"]["adaptive_path_cell_id"],
        )
        print(
            "ROUND35_RESTRICTION_COUNT:",
            envelope["result"]["verified_outputs"]["Round35_restriction_count"],
        )
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
