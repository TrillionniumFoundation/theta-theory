#!/usr/bin/env python3
"""Round 140 fixed-s adaptive-component identity bridge.

This append-only layer gives the positive-area fixed-s=0 R_1648 rectangle
from Round 139 a deterministic *adaptive path-cell* identity.  It also
materialises the exact Round27 path tuple and a Round137-v1 dyadic basis box
whose closure is contained in the cell.

The bridge is deliberately a strict non-substitution result.  A connected
adaptive rectangle cut out by artificial rational faces is not the maximal
connected component of the complete regular Round27 path fibre.  Its
deterministic ID therefore cannot be used as the historical Round27
``c24-component`` ID or as a Round35 restriction component.  The contained
dyadic rank is an upper-bound witness for the unique containing maximal
component; it is not its least rank.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import stat
import sys
import tempfile
from fractions import Fraction as Q
from pathlib import Path
from typing import Any


if hasattr(sys, "set_int_max_str_digits"):
    sys.set_int_max_str_digits(0)

HERE = Path(__file__).resolve().parent
OUTPUT = (
    HERE
    / "cm2-round140-fixed-s-adaptive-component-identity-bridge-2026-07-24.json"
)
SCHEMA = "cm2.round140.fixed-s-adaptive-component-identity-bridge.v1"

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


class CertError(RuntimeError):
    pass


class DuplicateKeyError(ValueError):
    pass


def require(condition: bool, label: str) -> None:
    if not condition:
        raise CertError(label)


def strict_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise DuplicateKeyError(key)
        result[key] = value
    return result


def reject_constant(token: str) -> Any:
    raise ValueError(f"non-finite JSON constant:{token}")


def strict_json(path: Path) -> dict[str, Any]:
    require(path.is_file() and not path.is_symlink(), f"dependency file:{path.name}")
    require(path.resolve().parent == HERE.resolve(), f"dependency parent:{path.name}")
    value = json.loads(
        path.read_text(encoding="utf-8"),
        object_pairs_hook=strict_pairs,
        parse_constant=reject_constant,
    )
    require(isinstance(value, dict), f"dependency root:{path.name}")
    return value


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


def qstr(value: Q) -> str:
    return (
        str(value.numerator)
        if value.denominator == 1
        else f"{value.numerator}/{value.denominator}"
    )


def with_hash(row: dict[str, Any]) -> dict[str, Any]:
    require("row_sha256" not in row, "row already closed")
    return {**row, "row_sha256": digest(row)}


def verify_closed_row(row: dict[str, Any], label: str) -> None:
    copy = dict(row)
    recorded = copy.pop("row_sha256", None)
    require(recorded == digest(copy), f"row closure:{label}")


def interval_pair_count(level: int) -> int:
    require(level >= 0, "nonnegative dyadic level")
    if level < 2:
        return 0
    count = 2**level - 1
    return count * (count - 1) // 2


def validate_pair(level: int, left: int, right: int) -> None:
    require(level >= 2, "dyadic level")
    require(1 <= left < right <= 2**level - 1, "dyadic pair")


def pair_lex_rank(level: int, left: int, right: int) -> int:
    validate_pair(level, left, right)
    maximum = 2**level - 1
    preceding = left - 1
    return (
        preceding * maximum
        - preceding * (preceding + 1) // 2
        + right - left - 1
    )


def even_pair_count_before(level: int, left: int, right: int) -> int:
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


def pair_is_even(pair: tuple[int, int]) -> bool:
    return pair[0] % 2 == 0 and pair[1] % 2 == 0


def rank_2d(row: tuple[int, int, int, int, int]) -> int:
    level, a0, a1, b0, b1 = row
    validate_pair(level, a0, a1)
    validate_pair(level, b0, b1)
    require(any(value % 2 for value in (a0, a1, b0, b1)), "primitive 2D row")
    total_pairs = interval_pair_count(level)
    even_pairs = interval_pair_count(level - 1)
    a_rank = pair_lex_rank(level, a0, a1)
    before_a = (
        a_rank * total_pairs
        - even_pair_count_before(level, a0, a1) * even_pairs
    )
    b_rank = pair_lex_rank(level, b0, b1)
    if pair_is_even((a0, a1)):
        require(not pair_is_even((b0, b1)), "primitive b pair")
        within_a = b_rank - even_pair_count_before(level, b0, b1)
    else:
        within_a = b_rank
    return even_pairs**2 + before_a + within_a


def first_two_strict_grid_points(
    lower: Q,
    upper: Q,
    level: int,
) -> tuple[int, int] | None:
    require(Q(0) < lower < upper < Q(1), "normalized interval")
    denominator = 2**level
    first = lower.numerator * denominator // lower.denominator + 1
    second = first + 1
    if (
        first >= 1
        and second <= denominator - 1
        and Q(first, denominator) > lower
        and Q(second, denominator) < upper
    ):
        return first, second
    return None


def level_has_box(
    u0: Q,
    u1: Q,
    v0: Q,
    v1: Q,
    level: int,
) -> bool:
    return (
        first_two_strict_grid_points(u0, u1, level) is not None
        and first_two_strict_grid_points(v0, v1, level) is not None
    )


def contained_witness_row(
    u0: Q,
    u1: Q,
    v0: Q,
    v1: Q,
) -> tuple[int, int, int, int, int]:
    low = 2
    high = 2
    while not level_has_box(u0, u1, v0, v1, high):
        low = high + 1
        high *= 2
    left = 2
    right = high
    while left < right:
        middle = (left + right) // 2
        if level_has_box(u0, u1, v0, v1, middle):
            right = middle
        else:
            left = middle + 1
    level = left
    require(
        level_has_box(u0, u1, v0, v1, level)
        and (level == 2 or not level_has_box(u0, u1, v0, v1, level - 1)),
        "minimal contained witness level",
    )
    u_pair = first_two_strict_grid_points(u0, u1, level)
    v_pair = first_two_strict_grid_points(v0, v1, level)
    require(u_pair is not None and v_pair is not None, "contained pairs")
    return (level, *u_pair, *v_pair)


def encoded_integer(value: int) -> dict[str, Any]:
    require(value >= 0, "nonnegative integer")
    decimal = str(value)
    return {
        "decimal": decimal,
        "bit_length": value.bit_length(),
        "decimal_digit_count": len(decimal),
        "sha256_of_decimal":
            hashlib.sha256(decimal.encode("ascii")).hexdigest(),
    }


def load_inputs() -> dict[str, dict[str, Any]]:
    require(
        sha256(ROUND139_SOURCE) == ROUND139_SOURCE_SHA256,
        "Round139 source hash",
    )
    loaded: dict[str, dict[str, Any]] = {}
    for path in (ROUND27, ROUND35, ROUND133, ROUND137, ROUND139):
        require(sha256(path) == PINS[path.name], f"dependency hash:{path.name}")
        loaded[path.name] = strict_json(path)
    return loaded


def validate_historical_contracts(loaded: dict[str, dict[str, Any]]) -> None:
    r27 = loaded[ROUND27.name]
    require(
        r27["schema"]
        == "cm2.gate34.round27-arbitrary-n-path-schema.manifest.v1",
        "Round27 schema",
    )
    require(
        r27["verdict"][
            "C24_arbitrary_n_full_dimensional_candidate_path_coverage"
        ] == "CERTIFIED_MOD_SINGULAR_NULL"
        and r27["verdict"][
            "arbitrary_n_regular_connected_component_existence_schema"
        ] == "CERTIFIED_NONCONSTRUCTIVE"
        and r27["verdict"][
            "nonempty_component_enumeration_and_numeric_payload"
        ] == "NOT_CERTIFIED",
        "Round27 verdict boundary",
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
        "Round35 verdict boundary",
    )
    parent = r35["result"]["arbitrary_Rn_parent_W_Borel_registry"]
    carrier = r35["result"]["common_forward_reverse_carrier_pair"]
    require(
        parent["component_id_schema"]
        == "c24-component:(source-core-id,n,path-key,least-dyadic-basis-index)"
        and parent["nonempty_component_coordinates_enumerated"] is False,
        "Round35 parent component",
    )
    require(
        carrier["common_physical_restriction_id"]
        == "rn-restriction:(component-id):(source-parent-W-id):(image-recut-rank)",
        "Round35 restriction grammar",
    )
    r133 = loaded[ROUND133.name]
    require(
        r133["schema"]
        == "cm2.round133.round132-owner-map-realizability-audit.v1"
        and r133["result"]["count_ledger"][
            "minimum_replacement_contract_field_count"
        ] == 17,
        "Round133 replacement contract",
    )
    r137 = loaded[ROUND137.name]
    require(
        r137["schema"]
        == "cm2.round137.seed-independent-dyadic-basis-rank-contract.v1"
        and r137["result"]["strict_nonpromotion"][
            "historical_Round27_canonical_component_rank"
        ] is None
        and r137["result"]["strict_nonpromotion"][
            "historical_Round27_c24_component_id"
        ] is None,
        "Round137 prospective boundary",
    )


def build() -> dict[str, Any]:
    loaded = load_inputs()
    validate_historical_contracts(loaded)
    r139_envelope = loaded[ROUND139.name]
    require(
        r139_envelope["schema"]
        == "cm2.round139.rank3-minus-d0-adjacent-h1-collar-return-frontier.v1",
        "Round139 schema",
    )
    r139 = r139_envelope["result"]
    require(r139_envelope["result_sha256"] == digest(r139), "Round139 result closure")
    require(
        r139["provenance"]["producer_sha256"] == ROUND139_SOURCE_SHA256,
        "Round139 envelope producer provenance",
    )

    cylinder = r139["nested_positive_area_R1648_cylinder"]
    verify_closed_row(cylinder, "Round139 cylinder")
    summary = r139["positive_area_first_return_summary"]
    rows = r139["positive_area_collision_rows"]
    require(
        isinstance(rows, list)
        and len(rows) == RETURN_DEPTH
        and r139["positive_area_collision_rows_sha256"] == digest(rows),
        "Round139 cylinder rows",
    )
    for index, row in enumerate(rows, start=1):
        verify_closed_row(row, f"Round139 collision {index}")
        require(
            row["collision_index"] == index
            and row["incidence_rank_B"] == 14
            and row["homogeneity_label"] == "H0_CENTRAL",
            f"Round139 collision typing:{index}",
        )
    require(
        cylinder["object_kind"] == "LOCAL_POSITIVE_AREA_FIXED_S_R1648_CYLINDER"
        and cylinder["s_box"] == ["0", "0"]
        and cylinder["positive_area"] is True
        and cylinder["whole_box_D3_anchor_discriminant_strictly_negative"] is True,
        "Round139 positive-area cylinder",
    )
    require(
        summary["ordinary_positive_area_rectangle"] is True
        and summary["collision3_analytic_anchor_exclusion_used"] is False
        and summary["first_return_depth"] == RETURN_DEPTH
        and summary["official_word_key_sequence_sha256"]
        == EXPECTED_WORD_SEQUENCE_SHA256
        and summary["strict_first_return_whole_positive_area_rectangle"] is True,
        "Round139 ordinary-owner return",
    )
    require(
        r139["corrected_rank3_source_contract"]["source_core_id"]
        == SOURCE_CORE_ID,
        "source core identity",
    )

    official_ids = [
        row["official_word_key"]["official_word_key_id"] for row in rows
    ]
    path_payload = [SOURCE_CORE_ID, RETURN_DEPTH, official_ids]
    path_tuple_sha = digest(path_payload)
    require(
        path_tuple_sha == EXPECTED_PATH_TUPLE_SHA256
        and digest(official_ids) == EXPECTED_WORD_SEQUENCE_SHA256,
        "Round27 path tuple",
    )
    path_row = with_hash({
        "schema": "round140-round27-path-instance-v1",
        "source_core_id": SOURCE_CORE_ID,
        "return_depth_n": RETURN_DEPTH,
        "official_word_key_occurrence_count": len(official_ids),
        "official_word_key_sequence_sha256": digest(official_ids),
        "Round27_compatible_candidate_path_tuple_sha256": path_tuple_sha,
        "candidate_path_key_grammar":
            "c24-path:(source_core_id,n,k_1,...,k_n)",
        "candidate_path_key_id":
            "round140-c24-path-instance:" + path_tuple_sha,
        "positive_area_nonempty_path_fibre_witness": True,
    })

    t0, t1 = (Q(value) for value in cylinder["t_box"])
    p0, p1 = (Q(value) for value in cylinder["p_box"])
    require(
        Q(1, 100) < t0 < t1 < Q(1, 50)
        and Q(-1, 500) < p0 < p1 < Q(1, 500),
        "cylinder strictly inside source core",
    )
    require(
        Q(cylinder["area"]) == (t1 - t0) * (p1 - p0) > 0,
        "cylinder area",
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
        path_tuple_sha,
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
        "Round27_path_tuple_sha256": path_tuple_sha,
        "t_open_interval": [qstr(t0), qstr(t1)],
        "p_open_interval": [qstr(p0), qstr(p1)],
        "positive_collision_area": qstr((t1 - t0) * (p1 - p0)),
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
    normalizations = r137[
        "source_core_affine_normalization_contract"
    ]["normalization_rows"]
    core_rows = [
        row for row in normalizations if row["source_core_id"] == SOURCE_CORE_ID
    ]
    require(len(core_rows) == 1, "unique Round137 normalization")
    core_row = core_rows[0]
    verify_closed_row(core_row, "Round137 normalization")
    ct0, ct1 = (Q(value) for value in core_row["t_bounds"])
    cp0, cp1 = (Q(value) for value in core_row["p_bounds"])
    u0, u1 = (t0 - ct0) / (ct1 - ct0), (t1 - ct0) / (ct1 - ct0)
    v0, v1 = (p0 - cp0) / (cp1 - cp0), (p1 - cp0) / (cp1 - cp0)
    basis_row = contained_witness_row(u0, u1, v0, v1)
    level, a0, a1, b0, b1 = basis_row
    denominator = 2**level
    require(
        u0 < Q(a0, denominator) < Q(a1, denominator) < u1
        and v0 < Q(b0, denominator) < Q(b1, denominator) < v1,
        "basis closure in adaptive cell",
    )
    basis_rank = rank_2d(basis_row)
    basis_locator_payload = [
        "round140-containing-component-upper-bound-locator-v1",
        adaptive_id,
        "round137-dyadic-basis-enumeration-v1",
        list(basis_row),
        str(basis_rank),
    ]
    basis_locator_id = (
        "round140-containing-component-upper-bound-locator:"
        + digest(basis_locator_payload)
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
        "upper_bound_locator_id": basis_locator_id,
        "upper_bound_locator_payload_sha256": digest(basis_locator_payload),
        "least_rank_of_maximal_component_computed": False,
    }

    containing_locator_payload = [
        "round140-unique-containing-maximal-component-locator-v1",
        SOURCE_CORE_ID,
        RETURN_DEPTH,
        path_tuple_sha,
        adaptive_id,
    ]
    containing_locator_id = (
        "round140-unique-containing-maximal-component-locator:"
        + digest(containing_locator_payload)
    )
    component_bridge = {
        "regular_path_fibre":
            "R_1648 intersect fibre(Round27 candidate path) at fixed s=0",
        "adaptive_open_cell_is_subset_of_regular_path_fibre": True,
        "adaptive_open_cell_is_connected": True,
        "unique_containing_maximal_connected_component_exists": True,
        "unique_containing_component_locator_id": containing_locator_id,
        "unique_containing_component_locator_payload_sha256":
            digest(containing_locator_payload),
        "locator_is_set_theoretic_not_historical_canonical_ID": True,
        "adaptive_cell_equals_maximal_path_component": False,
        "nonmaximality_reason":
            "the four adaptive rectangle faces are artificial while all physical path predicates remain strict on the closed rectangle; continuity extends the same path across each face locally",
        "historical_Round27_least_basis_rank": None,
        "historical_Round27_c24_component_id": None,
        "Round137_v1_least_rank_of_containing_component": None,
        "Round137_v1_upper_bound_locator": basis_locator_id,
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
                r139_envelope["result_sha256"],
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
    result = json.loads(json.dumps(result, sort_keys=True))
    return {
        "schema": SCHEMA,
        "result": result,
        "result_sha256": digest(result),
    }


def protected_paths() -> set[Path]:
    return {
        Path(__file__).resolve(),
        ROUND139_SOURCE.resolve(),
        *((HERE / name).resolve() for name in PINS),
    }


def validate_output_target(path: Path) -> Path:
    require(isinstance(path, Path), "output path type")
    absolute = path.absolute()
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
    protected = protected_paths()
    require(resolved not in protected, "output aliases protected path")
    if absolute.exists():
        metadata = absolute.lstat()
        require(
            stat.S_ISREG(metadata.st_mode) and metadata.st_nlink == 1,
            "safe existing output",
        )
        for item in protected:
            if item.exists():
                require(
                    not os.path.samefile(absolute, item),
                    "output hardlink aliases protected input",
                )
    return resolved


def write_atomic(path: Path, value: dict[str, Any]) -> None:
    resolved = validate_output_target(path)
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


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=OUTPUT)
    args = parser.parse_args()
    validate_output_target(args.output)
    envelope = build()
    write_atomic(args.output, envelope)
    print("STATUS:", envelope["result"]["status"])
    print(
        "ADAPTIVE_ID:",
        envelope["result"]["fixed_s_adaptive_path_cell"][
            "adaptive_path_cell_id"
        ],
    )
    print(
        "ROUND35_RESTRICTION_COUNT:",
        envelope["result"]["strict_nonpromotion"][
            "new_Round35_restriction_count"
        ],
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
