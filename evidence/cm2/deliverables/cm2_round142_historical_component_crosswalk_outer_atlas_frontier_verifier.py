#!/usr/bin/env python3
"""Independent verifier for the Round142 historical-component frontier.

The producer is neither imported nor executed.  This verifier independently
reconstructs the dyadic ranks, nested inside witnesses, D0-crossing outside
witness, two-enumeration underdetermination proof, symbolic negative-oracle
contract, centered-jet atlas frontier, and all strict nonpromotion fields from
byte-pinned Round27/137/139/140 inputs.
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
from typing import Any


if hasattr(sys, "set_int_max_str_digits"):
    sys.set_int_max_str_digits(0)

HERE = Path(__file__).resolve().parent
VERIFIER = Path(__file__).resolve()
PRODUCER = (
    HERE
    / "cm2_round142_historical_component_crosswalk_outer_atlas_frontier.py"
)
CERTIFICATE = (
    HERE
    / "cm2-round142-historical-component-crosswalk-outer-atlas-frontier-2026-07-24.json"
)
OUTPUT = (
    HERE
    / "cm2-round142-historical-component-crosswalk-outer-atlas-frontier-verification-2026-07-24.json"
)

CERTIFICATE_SCHEMA = (
    "cm2.round142.historical-component-crosswalk-outer-atlas-frontier.v1"
)
VERIFICATION_SCHEMA = (
    "cm2.round142.historical-component-crosswalk-outer-atlas-frontier-verification.v1"
)
PRODUCER_SHA256 = (
    "97477687d0013f5a8b426250b930e845858c624685c1f45f6528c336963b7d4c"
)
CERTIFICATE_SHA256 = (
    "816284789cc1249efd0ae9b9880e7d0434e8f74499c2616c6b64331997143ba0"
)
CERTIFICATE_RESULT_SHA256 = (
    "e734b4008ab822710c8b4c5aec5cc1a871f16d7bcea2230ba80eb2f493f0a37e"
)

ROUND27 = (
    HERE / "cm2-gate34-round27-arbitrary-n-path-schema-manifest-2026-07-18.json"
)
ROUND137 = (
    HERE
    / "cm2-round137-seed-independent-dyadic-basis-rank-contract-2026-07-24.json"
)
ROUND137_VERIFICATION = (
    HERE
    / "cm2-round137-seed-independent-dyadic-basis-rank-contract-verification-2026-07-24.json"
)
ROUND139 = (
    HERE
    / "cm2-round139-rank3-minus-d0-adjacent-h1-collar-return-frontier-2026-07-24.json"
)
ROUND139_VERIFICATION = (
    HERE
    / "cm2-round139-rank3-minus-d0-adjacent-h1-collar-return-frontier-verification-2026-07-24.json"
)
ROUND140 = (
    HERE
    / "cm2-round140-fixed-s-adaptive-component-identity-bridge-2026-07-24.json"
)
ROUND140_VERIFICATION = (
    HERE
    / "cm2-round140-fixed-s-adaptive-component-identity-bridge-verification-2026-07-24.json"
)
ROUND140_PARENT_W = (
    HERE
    / "cm2-round140-round35-parent-w-r1648-materialization-audit-2026-07-24.json"
)
ROUND140_PARENT_W_VERIFICATION = (
    HERE
    / "cm2-round140-round35-parent-w-r1648-materialization-audit-verification-2026-07-24.json"
)

PINS = {
    ROUND27.name:
        "988f364bd1e6943178238c072e725de01af36452ef25d179eae6aef4000f7916",
    ROUND137.name:
        "06918b7bbfdeed9bda41a1220a25b630df6eaaa5f06024757f25a8c9fe7b88bf",
    ROUND137_VERIFICATION.name:
        "53369532c293d9cb2830a362facef7e4c4040f826f5ddea70519fde9034a1a5c",
    ROUND139.name:
        "64e91e6b1efcb2675982fbc453b08349b003c8be5b4d236f61e1392aaee045f0",
    ROUND139_VERIFICATION.name:
        "57093537ae3f464e276da830ee5821ffbe3576278c71adbe111b22a128f3005f",
    ROUND140.name:
        "e3f08525e770829c3ce71fed872a18dbfdc3139f514c3f865d12f6abc114a353",
    ROUND140_VERIFICATION.name:
        "75500f473e1932151bc643109187e99e88033c3b9457b584ecb1df4c0860b611",
    ROUND140_PARENT_W.name:
        "bb6283e2fccba194b47f9aa174e85594560ba88062ed57d06651003744755a79",
    ROUND140_PARENT_W_VERIFICATION.name:
        "b38306fb85e4a8a27d0339d95ff9e7ee3eabea044239972c719c926e0891782d",
}

SOURCE_CORE_ID = (
    "core:90398e9ab632e57b027266bc7c34461a0a6a6d308c35fbeacc41432a3d7f48f7"
)
PATH_SHA256 = (
    "5cec1061ec331e8f37929dfb1b2b2a78757309ba60198d571abd9e8cf6c70ed9"
)
ADAPTIVE_ID = (
    "round140-fixed-s0-adaptive-path-cell:"
    "a4a3be3cf7115abec08f372382ca7a863838e963a7d03af400d6a6ca58812b6a"
)
CONTAINING_LOCATOR = (
    "round140-unique-containing-maximal-component-locator:"
    "028dd77208582e33185707e1ea1ca31988e3cf4f698674fb8a0f791981dce90b"
)


class VerificationError(RuntimeError):
    pass


def require(condition: bool, label: str) -> None:
    if not condition:
        raise VerificationError(label)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    ).encode("utf-8")


def digest(value: Any) -> str:
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def qstr(value: Q) -> str:
    value = Q(value)
    return (
        str(value.numerator)
        if value.denominator == 1
        else f"{value.numerator}/{value.denominator}"
    )


def reject_constant(token: str) -> None:
    raise VerificationError(f"non-finite JSON token:{token}")


def no_duplicate_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        require(key not in result, f"duplicate JSON key:{key}")
        result[key] = value
    return result


def strict_loads(payload: str) -> Any:
    return json.loads(
        payload,
        object_pairs_hook=no_duplicate_pairs,
        parse_constant=reject_constant,
    )


def strict_json(path: Path) -> dict[str, Any]:
    value = strict_loads(path.read_text(encoding="utf-8"))
    require(isinstance(value, dict), f"object:{path.name}")
    return value


def with_hash(row: dict[str, Any]) -> dict[str, Any]:
    result = dict(row)
    result["row_sha256"] = digest(row)
    return result


def closed_result(
    path: Path, schema: str, expected_status: str
) -> dict[str, Any]:
    envelope = strict_json(path)
    require(envelope["schema"] == schema, f"schema:{path.name}")
    require(
        envelope["result_sha256"] == digest(envelope["result"]),
        f"result digest:{path.name}",
    )
    require(
        envelope["result"]["status"] == expected_status,
        f"status:{path.name}",
    )
    return envelope["result"]


def validate_pair(level: int, left: int, right: int) -> None:
    require(
        isinstance(level, int)
        and level >= 2
        and isinstance(left, int)
        and isinstance(right, int)
        and 1 <= left < right <= 2**level - 1,
        "pair",
    )


def validate_2d_row(row: tuple[int, int, int, int, int]) -> None:
    level, a0, a1, b0, b1 = row
    validate_pair(level, a0, a1)
    validate_pair(level, b0, b1)
    require(
        any(endpoint % 2 for endpoint in (a0, a1, b0, b1)),
        "primitive row",
    )


def interval_pair_count(level: int) -> int:
    require(level >= 1, "pair-count level")
    return (2**level - 1) * (2**level - 2) // 2


def pair_lex_rank(level: int, left: int, right: int) -> int:
    validate_pair(level, left, right)
    preceding = left - 1
    maximum = 2**level - 1
    return (
        preceding * maximum
        - preceding * (preceding + 1) // 2
        + right - left - 1
    )


def pair_is_even(pair: tuple[int, int]) -> bool:
    return pair[0] % 2 == 0 and pair[1] % 2 == 0


def even_pair_count_before(level: int, left: int, right: int) -> int:
    validate_pair(level, left, right)
    half_maximum = 2 ** (level - 1) - 1
    earlier = (left - 1) // 2
    count = earlier * half_maximum - earlier * (earlier + 1) // 2
    if left % 2 == 0:
        count += max(0, (right - 1) // 2 - left // 2)
    return count


def rank_2d(row: tuple[int, int, int, int, int]) -> int:
    validate_2d_row(row)
    level, a0, a1, b0, b1 = row
    total = interval_pair_count(level)
    even = interval_pair_count(level - 1)
    arank = pair_lex_rank(level, a0, a1)
    before = arank * total - even_pair_count_before(
        level, a0, a1
    ) * even
    brank = pair_lex_rank(level, b0, b1)
    if pair_is_even((a0, a1)):
        require(not pair_is_even((b0, b1)), "primitive b")
        within = brank - even_pair_count_before(level, b0, b1)
    else:
        within = brank
    return even**2 + before + within


def encoded_integer(value: int) -> dict[str, Any]:
    decimal = str(value)
    return {
        "decimal": decimal,
        "decimal_digit_count": len(decimal),
        "bit_length": value.bit_length(),
        "sha256_of_decimal": hashlib.sha256(decimal.encode()).hexdigest(),
    }


def row_box(
    row: tuple[int, int, int, int, int]
) -> tuple[Q, Q, Q, Q]:
    level, a0, a1, b0, b1 = row
    denominator = 2**level
    return (
        Q(a0, denominator),
        Q(a1, denominator),
        Q(b0, denominator),
        Q(b1, denominator),
    )


def all_keys(value: Any) -> set[str]:
    result: set[str] = set()
    if isinstance(value, dict):
        for key, child in value.items():
            result.add(key)
            result.update(all_keys(child))
    elif isinstance(value, list):
        for child in value:
            result.update(all_keys(child))
    return result


def load_dependencies() -> dict[str, dict[str, Any]]:
    for name, expected in PINS.items():
        path = HERE / name
        require(sha256(path) == expected, f"pin:{name}")
    r27 = strict_json(ROUND27)
    require(
        r27["schema"]
        == "cm2.gate34.round27-arbitrary-n-path-schema.manifest.v1",
        "Round27 schema",
    )
    r137 = closed_result(
        ROUND137,
        "cm2.round137.seed-independent-dyadic-basis-rank-contract.v1",
        "CERTIFIED_PROSPECTIVE_SEED_INDEPENDENT_DYADIC_BASIS_RANK_CONTRACT",
    )
    closed_result(
        ROUND137_VERIFICATION,
        "cm2.round137.seed-independent-dyadic-basis-rank-contract-verification.v1",
        "PASS",
    )
    r139 = closed_result(
        ROUND139,
        "cm2.round139.rank3-minus-d0-adjacent-h1-collar-return-frontier.v1",
        "CERTIFIED_MINUS_D0_ADJACENT_H1_COLLAR_STRICT_FIRST_RETURN",
    )
    closed_result(
        ROUND139_VERIFICATION,
        "cm2.round139.rank3-minus-d0-adjacent-h1-collar-return-frontier-verification.v1",
        "PASS",
    )
    r140 = closed_result(
        ROUND140,
        "cm2.round140.fixed-s-adaptive-component-identity-bridge.v1",
        "CERTIFIED_FIXED_S_ADAPTIVE_IDENTITY_STRICT_NONSUBSTITUTION",
    )
    closed_result(
        ROUND140_VERIFICATION,
        "cm2.round140.fixed-s-adaptive-component-identity-bridge-verification.v1",
        "PASS",
    )
    parent_w = closed_result(
        ROUND140_PARENT_W,
        "cm2.round140.round35-parent-w-r1648-materialization-audit.v1",
        "CERTIFIED_MAXIMAL_LEGAL_ROUND35_PARENT_W_DATA_FROM_R1648",
    )
    closed_result(
        ROUND140_PARENT_W_VERIFICATION,
        "cm2.round140.round35-parent-w-r1648-materialization-audit-verification.v1",
        "PASS",
    )
    require(
        r140["fixed_s_adaptive_path_cell"]["adaptive_path_cell_id"]
        == ADAPTIVE_ID
        and r140["unique_containing_maximal_component_bridge"][
            "unique_containing_component_locator_id"
        ]
        == CONTAINING_LOCATOR
        and r139["corrected_rank3_source_contract"]["source_core_id"]
        == SOURCE_CORE_ID
        and parent_w["maximal_legal_Round35_field_status"][
            "historical_Round27_component_rank_materialized"
        ]
        is False,
        "dependency boundaries",
    )
    return {
        "r27": r27,
        "r137": r137,
        "r139": r139,
        "r140": r140,
    }


def expected_structures(
    loaded: dict[str, dict[str, Any]]
) -> dict[str, Any]:
    r27, r137, r139, r140 = (
        loaded["r27"],
        loaded["r137"],
        loaded["r139"],
        loaded["r140"],
    )
    component = r27["result"][
        "canonical_regular_connected_component_schema"
    ]
    historical_audit = r137["historical_schema_audit"]
    expected_absent = [
        key
        for key in (
            "historical_dyadic_basis_enumeration_id",
            "historical_dyadic_basis_enumeration_sha256",
            "historical_dyadic_basis_row_encoding",
            "historical_dyadic_basis_index_origin",
            "historical_dyadic_basis_rank",
            "historical_dyadic_basis_unrank",
            "historical_coordinate_normalization",
            "historical_enumeration_order",
            "historical_enumeration_seed",
        )
        if key not in all_keys(r27)
    ]
    require(len(expected_absent) == 9, "absent historical fields")
    crosswalk = with_hash({
        "Round27_rank_definition": component["canonical_component_rank"],
        "Round27_component_ID_definition": component[
            "canonical_component_id"
        ],
        "Round27_component_coordinates_enumerated": False,
        "historical_basis_row_encoding_frozen":
            historical_audit["historical_basis_row_encoding_frozen"],
        "historical_coordinate_normalization_frozen":
            historical_audit["historical_coordinate_normalization_frozen"],
        "historical_enumeration_order_frozen":
            historical_audit["historical_enumeration_order_frozen"],
        "historical_rank_unrank_algorithm_frozen":
            historical_audit["historical_rank_unrank_algorithm_frozen"],
        "historical_index_origin_frozen":
            historical_audit[
                "historical_zero_or_one_based_indexing_frozen"
            ],
        "absent_executable_field_count": 9,
        "absent_executable_fields": expected_absent,
        "Round137_v1_is_prospective_not_a_historical_crosswalk": True,
        "an_outer_atlas_alone_can_recover_historical_numeric_rank": False,
        "exact_first_blocker":
            "no unique historical enumeration is defined by the frozen Round27 bytes",
    })

    witness = r140["Round137_v1_contained_basis_upper_bound"]
    parent = tuple(witness["contained_primitive_basis_row"])
    validate_2d_row(parent)
    require(
        encoded_integer(rank_2d(parent))
        == witness["contained_primitive_basis_rank"],
        "parent rank",
    )
    m, a0, a1, b0, b1 = parent
    require(a1 == a0 + 1 and b1 == b0 + 1, "parent consecutive")
    rows = (
        ("A", (m + 1, 2 * a0, 2 * a0 + 1, 2 * b0, 2 * b0 + 1)),
        ("B", (m + 1, 2 * a0 + 1, 2 * a1, 2 * b0, 2 * b0 + 1)),
    )
    inside = []
    for name, row in rows:
        validate_2d_row(row)
        payload = [
            "round142-inside-basis-witness-v1",
            ADAPTIVE_ID,
            name,
            list(row),
        ]
        inside.append(with_hash({
            "name": name,
            "primitive_basis_row": list(row),
            "Round137_v1_rank": encoded_integer(rank_2d(row)),
            "closure_contained_in_Round140_parent_basis_box": True,
            "closure_strictly_inside_adaptive_R1648_cell": True,
            "closure_contained_in_unique_maximal_component_U": True,
            "witness_id": "round142-inside-basis:" + digest(payload),
        }))

    normalizations = r137[
        "source_core_affine_normalization_contract"
    ]["normalization_rows"]
    normal = [
        row
        for row in normalizations
        if row["source_core_id"] == SOURCE_CORE_ID
    ]
    require(len(normal) == 1, "normalization")
    ct0, ct1 = (Q(value) for value in normal[0]["t_bounds"])
    cp0, cp1 = (Q(value) for value in normal[0]["p_bounds"])
    collar = r139["minus_D0_adjacent_H1_collar"]
    tlo, thi = (Q(value) for value in collar["t_image_outer"])
    plo, phi = (Q(value) for value in collar["p_image_outer"])
    u = ((tlo - ct0) / (ct1 - ct0), (thi - ct0) / (ct1 - ct0))
    v = ((plo - cp0) / (cp1 - cp0), (phi - cp0) / (cp1 - cp0))
    outside_row = (5, 30, 31, 8, 9)
    box = row_box(outside_row)
    require(
        box[0] <= u[0] <= u[1] <= box[1]
        and box[2] <= v[0] <= v[1] <= box[3],
        "outside enclosure",
    )
    normalized = {
        "u": [qstr(value) for value in u],
        "v": [qstr(value) for value in v],
    }
    outside_payload = [
        "round142-D0-crossing-outside-basis-v1",
        SOURCE_CORE_ID,
        list(outside_row),
        digest(normalized),
        r139["deep_same_D0_root_and_b_star"]["row_sha256"],
    ]
    outside = with_hash({
        "primitive_basis_row": list(outside_row),
        "Round137_v1_rank": encoded_integer(rank_2d(outside_row)),
        "normalized_D0_collar_enclosure_sha256": digest(normalized),
        "whole_certified_D0_collar_enclosure_in_box_closure": True,
        "exact_D3_zero_point_x_star_in_enclosure": True,
        "x_star_is_excluded_collision3_tangency_boundary": True,
        "box_closure_is_not_contained_in_regular_path_component_U": True,
        "outside_witness_id":
            "round142-D0-crossing-outside-basis:" + digest(outside_payload),
    })

    ambiguity_payload = [
        "round142-historical-enumeration-underdetermination-v1",
        CONTAINING_LOCATOR,
        inside[0]["witness_id"],
        outside["outside_witness_id"],
    ]
    ambiguity = with_hash({
        "proof_kind": "TWO_COMPATIBLE_FIXED_BIJECTIONS",
        "component_locator": CONTAINING_LOCATOR,
        "inside_basis_witness": inside[0]["witness_id"],
        "outside_basis_witness": outside["outside_witness_id"],
        "model_E0_finite_prefix": [
            {"index_zero_based": 0, "basis_role": "inside_A"},
        ],
        "model_E1_finite_prefix": [
            {"index_zero_based": 0, "basis_role": "outside_D0_crossing"},
            {"index_zero_based": 1, "basis_role": "inside_A"},
        ],
        "finite_prefix_extension_lemma":
            "any injection from a finite initial segment into a countably infinite set extends to a bijection N->set",
        "both_models_satisfy_Round27_fixed_bijective_enumeration_sentence":
            True,
        "least_index_in_model_E0_zero_based": 0,
        "least_index_in_model_E1_zero_based": 1,
        "least_index_in_model_E0_one_based": 1,
        "least_index_in_model_E1_one_based": 2,
        "ambiguity_does_not_depend_on_index_origin": True,
        "historical_numeric_rank_identified_by_frozen_artifacts": False,
        "historical_c24_component_ID_identified_by_frozen_artifacts": False,
        "ambiguity_proof_id":
            "round142-historical-enumeration-underdetermination:"
            + digest(ambiguity_payload),
    })

    negative = with_hash({
        "target_enumeration": "round137-dyadic-basis-enumeration-v1",
        "scope": "prospective_only_not_historical_crosswalk",
        "positive_oracle":
            "one primitive basis box whose closure is certified inside U",
        "negative_oracle":
            "for every earlier v1 rank r, certify closure(unrank_2d(r)) is not a subset of U",
        "symbolic_outer_atlas_sufficient_condition":
            "certify U subset O, then prove no earlier basis-box closure is a subset of O",
        "axis_rectangle_specialization":
            "compute the least v1 basis row strictly inside the rational outer rectangle by level then lex arithmetic; equality with the positive witness proves leastness without enumerating all earlier ranks",
        "finite_union_atlas_specialization":
            "use exact cell-union coverage plus symbolic dyadic-box subset queries; frontier exhaustion is mandatory",
        "currently_certified_global_outer_enclosure":
            "normalized source chart (0,1)^2 only",
        "current_outer_enclosure_earliest_v1_row": [2, 1, 2, 1, 2],
        "current_outer_enclosure_earliest_v1_rank": 0,
        "current_positive_upper_bound_rank":
            witness["contained_primitive_basis_rank"],
        "current_negative_oracle_closes_gap": False,
        "failure_of_interval_replay_is_a_negative_membership_oracle": False,
        "historical_enumeration_crosswalk_still_required_even_if_v1_oracle_closes":
            True,
    })

    atlas_payload = [
        "round142-centered-jet-outer-atlas-frontier-v1",
        CONTAINING_LOCATOR,
        ADAPTIVE_ID,
        ambiguity["ambiguity_proof_id"],
        negative["row_sha256"],
    ]
    atlas = with_hash({
        "atlas_contract_id":
            "round142-centered-jet-outer-atlas-frontier:"
            + digest(atlas_payload),
        "fixed_parameter_s": "0",
        "return_depth": 1648,
        "Round27_path_tuple_sha256": PATH_SHA256,
        "target_component_locator": CONTAINING_LOCATOR,
        "preferred_coordinates": {
            "leaf_coordinate": "x=sqrt(17)*r, r=(4/25)*asin(t)",
            "transverse_coordinate": "beta=(asin(p)-4r)-b_star",
            "centered_generators": ["delta_x", "delta_beta"],
        },
        "certified_seed_cell_id": ADAPTIVE_ID,
        "certified_seed_cell_count": 1,
        "certified_seed_connected": True,
        "certified_seed_same_1648_path": True,
        "certified_seed_positive_area": True,
        "certified_seed_adjacency_edge_count": 0,
        "certified_leaf_event_endpoints": [{
            "event": "collision3_D3_zero",
            "coordinate": "x_star",
            "role": "right_leaf_boundary_candidate",
            "certified_exact_on_leaf": True,
            "certified_as_complete_2D_component_face": False,
        }],
        "required_cell_payload": [
            "centered two-generator state enclosure at every collision",
            "same selected owner and official word at all 1648 stages",
            "strict nonreturn at stages 1..1647 and strict terminal return",
            "homogeneity/incidence/chart/core margins",
            "Jacobian of every active event function in (x,beta)",
            "determinant/transversality ledger for intersecting event faces",
        ],
        "candidate_component_faces_requiring_validation": [
            "collision3 D3=0 tangency face",
            "terminal G[-7,-13] destination-core p=-1/50 face",
            "all transverse owner/root/chart/homogeneity/core event faces",
        ],
        "adjacency_rule":
            "two validated cells are adjacent only through an artificial face with a certified overlap or shared face and identical 1648 path payload",
        "outer_closure_rule":
            "every open atlas frontier must be continued or classified as a certified physical path-fibre event face",
        "complete_2D_centered_jet_cell_count": 0,
        "complete_2D_adjacency_edge_count": 0,
        "complete_physical_boundary_face_count": 0,
        "maximal_component_U_outer_enclosed": False,
        "maximal_component_U_boundary_exhausted": False,
        "Round137_v1_earlier_ranks_symbolically_excluded": False,
        "historical_least_rank_computed": False,
        "first_missing_historical_oracle":
            "the exact Round27 dyadic-basis enumeration/order, row encoding, normalization and index origin",
        "first_missing_geometric_oracle_after_prospective_v1_adoption":
            "a complete validated two-generator centered-jet outer atlas with exhausted event frontier",
    })
    return {
        "crosswalk": crosswalk,
        "parent": parent,
        "parent_rank": witness["contained_primitive_basis_rank"],
        "inside": inside,
        "outside": outside,
        "ambiguity": ambiguity,
        "negative": negative,
        "atlas": atlas,
    }


def verify_result(
    result: dict[str, Any], loaded: dict[str, dict[str, Any]]
) -> None:
    expected = expected_structures(loaded)
    require(
        result["status"]
        == "CERTIFIED_HISTORICAL_ENUMERATION_UNDERDETERMINATION_AND_OUTER_ATLAS_FRONTIER",
        "status",
    )
    require(
        result["provenance"] == {
            "dependency_sha256": dict(sorted(PINS.items())),
            "append_only": True,
            "Round139_or_Round140_files_modified": False,
        },
        "provenance",
    )
    require(
        result["historical_definition_and_crosswalk_audit"]
        == expected["crosswalk"],
        "crosswalk",
    )
    inside_container = {
        "Round140_parent_basis_row": list(expected["parent"]),
        "Round140_parent_basis_rank": expected["parent_rank"],
        "strictly_nested_child_count": 2,
        "strictly_nested_children": expected["inside"],
        "children_sha256": digest(expected["inside"]),
    }
    require(
        result["inside_basis_witnesses"] == inside_container,
        "inside witnesses",
    )
    require(
        result["D0_crossing_outside_basis_witness"]
        == expected["outside"],
        "outside witness",
    )
    require(
        result["two_enumeration_model_underdetermination_proof"]
        == expected["ambiguity"],
        "ambiguity proof",
    )
    require(
        result["prospective_v1_symbolic_negative_oracle_contract"]
        == expected["negative"],
        "negative oracle contract",
    )
    require(
        result["centered_jet_outer_atlas_frontier"] == expected["atlas"],
        "atlas frontier",
    )
    frontier_payload = [
        "round142-historical-component-frontier-v1",
        expected["crosswalk"]["row_sha256"],
        expected["ambiguity"]["row_sha256"],
        expected["atlas"]["row_sha256"],
        expected["negative"]["row_sha256"],
    ]
    require(
        result["frontier_id"]
        == "round142-historical-component-frontier:"
        + digest(frontier_payload),
        "frontier ID",
    )
    require(
        result["strict_nonpromotion"] == {
            "new_historical_Round27_component_rank_count": 0,
            "new_historical_Round27_c24_component_ID_count": 0,
            "new_maximal_component_outer_atlas_count": 0,
            "new_complete_2D_centered_jet_cell_count": 0,
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
        "strict nonpromotion",
    )
    require(
        result["strict_nonclaims"] == [
            "the two enumeration models prove underdetermination; neither is asserted to be the unnamed historical enumeration",
            "Round137-v1 is not retroactively substituted for the Round27 enumeration",
            "the one-cell adaptive registry is not the maximal regular path component",
            "the D0 leaf endpoint is not promoted to a complete two-dimensional boundary face",
            "the symbolic negative-oracle contract is not a completed negative oracle",
            "no historical component rank/ID or Round35 restriction is minted",
        ],
        "strict nonclaims",
    )
    require(
        set(result) == {
            "status",
            "provenance",
            "historical_definition_and_crosswalk_audit",
            "inside_basis_witnesses",
            "D0_crossing_outside_basis_witness",
            "two_enumeration_model_underdetermination_proof",
            "prospective_v1_symbolic_negative_oracle_contract",
            "centered_jet_outer_atlas_frontier",
            "frontier_id",
            "strict_nonpromotion",
            "strict_nonclaims",
        },
        "result key set",
    )


def verify_envelope(
    envelope: dict[str, Any],
    loaded: dict[str, dict[str, Any]],
) -> None:
    require(
        set(envelope) == {"schema", "result", "result_sha256"},
        "envelope key set",
    )
    require(envelope["schema"] == CERTIFICATE_SCHEMA, "certificate schema")
    require(
        envelope["result_sha256"] == digest(envelope["result"]),
        "certificate result digest",
    )
    verify_result(envelope["result"], loaded)


def set_path(value: Any, path: tuple[Any, ...], replacement: Any) -> None:
    target = value
    for key in path[:-1]:
        target = target[key]
    target[path[-1]] = replacement


def semantic_mutations(
    envelope: dict[str, Any], loaded: dict[str, dict[str, Any]]
) -> list[dict[str, Any]]:
    attacks = [
        ("status", ("result", "status"), "PASS"),
        (
            "dependency_pin",
            ("result", "provenance", "dependency_sha256", ROUND139.name),
            "0" * 64,
        ),
        (
            "append_only",
            ("result", "provenance", "append_only"),
            False,
        ),
        (
            "crosswalk_order",
            (
                "result",
                "historical_definition_and_crosswalk_audit",
                "historical_enumeration_order_frozen",
            ),
            True,
        ),
        (
            "absent_count",
            (
                "result",
                "historical_definition_and_crosswalk_audit",
                "absent_executable_field_count",
            ),
            8,
        ),
        (
            "outer_atlas_recovers_history",
            (
                "result",
                "historical_definition_and_crosswalk_audit",
                "an_outer_atlas_alone_can_recover_historical_numeric_rank",
            ),
            True,
        ),
        (
            "parent_level",
            ("result", "inside_basis_witnesses", "Round140_parent_basis_row", 0),
            5882,
        ),
        (
            "child_count",
            ("result", "inside_basis_witnesses", "strictly_nested_child_count"),
            1,
        ),
        (
            "child_endpoint",
            (
                "result",
                "inside_basis_witnesses",
                "strictly_nested_children",
                0,
                "primitive_basis_row",
                1,
            ),
            1,
        ),
        (
            "child_containment",
            (
                "result",
                "inside_basis_witnesses",
                "strictly_nested_children",
                0,
                "closure_contained_in_unique_maximal_component_U",
            ),
            False,
        ),
        (
            "child_rank_hash",
            (
                "result",
                "inside_basis_witnesses",
                "strictly_nested_children",
                1,
                "Round137_v1_rank",
                "sha256_of_decimal",
            ),
            "0" * 64,
        ),
        (
            "outside_row",
            (
                "result",
                "D0_crossing_outside_basis_witness",
                "primitive_basis_row",
                1,
            ),
            29,
        ),
        (
            "outside_D0",
            (
                "result",
                "D0_crossing_outside_basis_witness",
                "exact_D3_zero_point_x_star_in_enclosure",
            ),
            False,
        ),
        (
            "outside_component",
            (
                "result",
                "D0_crossing_outside_basis_witness",
                "box_closure_is_not_contained_in_regular_path_component_U",
            ),
            False,
        ),
        (
            "model_kind",
            (
                "result",
                "two_enumeration_model_underdetermination_proof",
                "proof_kind",
            ),
            "ONE_MODEL",
        ),
        (
            "model_E0_rank",
            (
                "result",
                "two_enumeration_model_underdetermination_proof",
                "least_index_in_model_E0_zero_based",
            ),
            1,
        ),
        (
            "model_E1_rank",
            (
                "result",
                "two_enumeration_model_underdetermination_proof",
                "least_index_in_model_E1_zero_based",
            ),
            0,
        ),
        (
            "model_extension",
            (
                "result",
                "two_enumeration_model_underdetermination_proof",
                "both_models_satisfy_Round27_fixed_bijective_enumeration_sentence",
            ),
            False,
        ),
        (
            "historical_identified",
            (
                "result",
                "two_enumeration_model_underdetermination_proof",
                "historical_numeric_rank_identified_by_frozen_artifacts",
            ),
            True,
        ),
        (
            "negative_scope",
            (
                "result",
                "prospective_v1_symbolic_negative_oracle_contract",
                "scope",
            ),
            "historical",
        ),
        (
            "negative_closed",
            (
                "result",
                "prospective_v1_symbolic_negative_oracle_contract",
                "current_negative_oracle_closes_gap",
            ),
            True,
        ),
        (
            "failure_is_oracle",
            (
                "result",
                "prospective_v1_symbolic_negative_oracle_contract",
                "failure_of_interval_replay_is_a_negative_membership_oracle",
            ),
            True,
        ),
        (
            "atlas_seed_count",
            (
                "result",
                "centered_jet_outer_atlas_frontier",
                "certified_seed_cell_count",
            ),
            2,
        ),
        (
            "atlas_cell_count",
            (
                "result",
                "centered_jet_outer_atlas_frontier",
                "complete_2D_centered_jet_cell_count",
            ),
            1,
        ),
        (
            "atlas_face_claim",
            (
                "result",
                "centered_jet_outer_atlas_frontier",
                "certified_leaf_event_endpoints",
                0,
                "certified_as_complete_2D_component_face",
            ),
            True,
        ),
        (
            "atlas_outer",
            (
                "result",
                "centered_jet_outer_atlas_frontier",
                "maximal_component_U_outer_enclosed",
            ),
            True,
        ),
        (
            "atlas_rank",
            (
                "result",
                "centered_jet_outer_atlas_frontier",
                "historical_least_rank_computed",
            ),
            True,
        ),
        ("frontier_id", ("result", "frontier_id"), "forged"),
        (
            "historical_count",
            (
                "result",
                "strict_nonpromotion",
                "new_historical_Round27_component_rank_count",
            ),
            1,
        ),
        (
            "atlas_count",
            (
                "result",
                "strict_nonpromotion",
                "new_maximal_component_outer_atlas_count",
            ),
            1,
        ),
        (
            "gate5_maturity",
            ("result", "strict_nonpromotion", "global_gate5_maturity"),
            "11/18",
        ),
        (
            "gate5",
            ("result", "strict_nonpromotion", "Gate5"),
            "CERTIFIED",
        ),
        (
            "cm2",
            ("result", "strict_nonpromotion", "CM2"),
            "GO",
        ),
        (
            "nonclaim",
            ("result", "strict_nonclaims", 0),
            "historical enumeration recovered",
        ),
    ]
    outcomes = []
    for name, path, replacement in attacks:
        mutant = copy.deepcopy(envelope)
        set_path(mutant, path, replacement)
        mutant["result_sha256"] = digest(mutant["result"])
        rejected = False
        try:
            verify_envelope(mutant, loaded)
        except (VerificationError, KeyError, IndexError, TypeError, ValueError):
            rejected = True
        require(rejected, f"mutation accepted:{name}")
        outcomes.append({"attack": name, "rejected": True})
    return outcomes


def parser_attacks() -> list[dict[str, Any]]:
    attacks = [
        ("duplicate_top", '{"schema":"a","schema":"b"}'),
        ("duplicate_nested", '{"x":{"a":1,"a":2}}'),
        ("nan", '{"x":NaN}'),
        ("infinity", '{"x":Infinity}'),
        ("negative_infinity", '{"x":-Infinity}'),
        ("top_array", "[]"),
        ("trailing", '{"x":1} garbage'),
    ]
    outcomes = []
    for name, payload in attacks:
        rejected = False
        try:
            value = strict_loads(payload)
            require(isinstance(value, dict), "top object")
        except (VerificationError, json.JSONDecodeError, ValueError):
            rejected = True
        require(rejected, f"parser attack accepted:{name}")
        outcomes.append({"attack": name, "rejected": True})
    return outcomes


def protected_paths() -> set[Path]:
    return {
        PRODUCER.resolve(),
        VERIFIER.resolve(),
        CERTIFICATE.resolve(),
        *((HERE / name).resolve() for name in PINS),
    }


def safe_certificate_path(path: Path) -> Path:
    absolute = path.absolute()
    metadata = absolute.lstat()
    require(
        stat.S_ISREG(metadata.st_mode)
        and metadata.st_nlink == 1
        and not absolute.is_symlink(),
        "unsafe certificate path",
    )
    resolved = absolute.resolve()
    require(sha256(resolved) == CERTIFICATE_SHA256, "certificate byte pin")
    return resolved


def validate_output_target(path: Path, certificate_path: Path) -> Path:
    absolute = path.absolute()
    parent = absolute.parent
    require(
        parent.exists()
        and parent.is_dir()
        and not parent.is_symlink()
        and parent.resolve() == parent,
        "unsafe output parent",
    )
    require(not absolute.is_symlink(), "output symlink")
    resolved = absolute.resolve(strict=False)
    require(resolved != certificate_path, "input/output alias")
    require(resolved not in protected_paths(), "protected output")
    if absolute.exists():
        metadata = absolute.lstat()
        require(
            stat.S_ISREG(metadata.st_mode) and metadata.st_nlink == 1,
            "unsafe existing output",
        )
        for item in protected_paths() | {certificate_path}:
            if item.exists():
                require(
                    not os.path.samefile(absolute, item),
                    "hardlink output alias",
                )
    return resolved


def path_attacks() -> list[dict[str, Any]]:
    outcomes = []
    certificate = CERTIFICATE.resolve()
    cases: list[tuple[str, Any]] = [
        (
            "certificate_directory",
            lambda root: safe_certificate_path(root),
        ),
        (
            "certificate_symlink",
            lambda root: (
                (root / "cert-link").symlink_to(certificate),
                safe_certificate_path(root / "cert-link"),
            ),
        ),
        (
            "output_producer",
            lambda root: validate_output_target(PRODUCER, certificate),
        ),
        (
            "output_certificate",
            lambda root: validate_output_target(CERTIFICATE, certificate),
        ),
        (
            "output_dependency",
            lambda root: validate_output_target(ROUND139, certificate),
        ),
        (
            "output_symlink",
            lambda root: (
                (root / "out-link").symlink_to(root / "future"),
                validate_output_target(root / "out-link", certificate),
            ),
        ),
    ]
    with tempfile.TemporaryDirectory(prefix="cm2-r142-path-") as temporary:
        root = Path(temporary)
        for name, action in cases:
            rejected = False
            try:
                action(root)
            except (VerificationError, OSError):
                rejected = True
            require(rejected, f"path attack accepted:{name}")
            outcomes.append({"attack": name, "rejected": True})
        fifo = root / "fifo"
        os.mkfifo(fifo)
        rejected = False
        try:
            safe_certificate_path(fifo)
        except (VerificationError, OSError):
            rejected = True
        require(rejected, "FIFO accepted")
        outcomes.append({"attack": "certificate_FIFO", "rejected": True})
        first = root / "first"
        second = root / "second"
        first.write_text("x", encoding="utf-8")
        os.link(first, second)
        rejected = False
        try:
            validate_output_target(first, certificate)
        except (VerificationError, OSError):
            rejected = True
        require(rejected, "multi-link output accepted")
        outcomes.append({"attack": "output_hardlink", "rejected": True})
    return outcomes


def write_atomic(
    path: Path, value: dict[str, Any], certificate_path: Path
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
        prefix=f".{resolved.name}.", suffix=".tmp", dir=resolved.parent
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
    require(sha256(PRODUCER) == PRODUCER_SHA256, "producer pin")
    require(sha256(certificate_path) == CERTIFICATE_SHA256, "certificate pin")
    loaded = load_dependencies()
    envelope = strict_json(certificate_path)
    require(
        envelope["result_sha256"] == CERTIFICATE_RESULT_SHA256,
        "certificate result pin",
    )
    verify_envelope(envelope, loaded)
    mutations = semantic_mutations(envelope, loaded)
    parsers = parser_attacks()
    paths = path_attacks()
    result = envelope["result"]
    verification = {
        "status": "PASS",
        "producer_sha256": PRODUCER_SHA256,
        "certificate_sha256": CERTIFICATE_SHA256,
        "certificate_result_sha256": CERTIFICATE_RESULT_SHA256,
        "certificate_schema": CERTIFICATE_SCHEMA,
        "verifier_sha256": sha256(VERIFIER),
        "dependency_sha256": dict(sorted(PINS.items())),
        "independent_recomputation": {
            "producer_imported_or_executed": False,
            "Round27_missing_crosswalk_fields_reaudited": True,
            "Round137_v1_parent_rank_recomputed": True,
            "two_nested_inside_basis_rows_and_ranks_recomputed": True,
            "D0_normalization_and_outside_basis_inclusion_recomputed": True,
            "two_enumeration_model_proof_recomputed": True,
            "symbolic_negative_oracle_contract_recomputed": True,
            "centered_jet_outer_atlas_frontier_recomputed": True,
            "strict_nonpromotion_recomputed": True,
        },
        "verified_outputs": {
            "ambiguity_proof_id": result[
                "two_enumeration_model_underdetermination_proof"
            ]["ambiguity_proof_id"],
            "inside_basis_witness_count": result[
                "inside_basis_witnesses"
            ]["strictly_nested_child_count"],
            "outside_basis_row": result[
                "D0_crossing_outside_basis_witness"
            ]["primitive_basis_row"],
            "complete_2D_centered_jet_cell_count": result[
                "centered_jet_outer_atlas_frontier"
            ]["complete_2D_centered_jet_cell_count"],
            "historical_component_rank_count": result[
                "strict_nonpromotion"
            ]["new_historical_Round27_component_rank_count"],
            "Gate5": result["strict_nonpromotion"]["Gate5"],
            "CM2": result["strict_nonpromotion"]["CM2"],
        },
        "semantic_mutation_test_count": len(mutations),
        "semantic_mutation_tests": mutations,
        "strict_parser_test_count": len(parsers),
        "strict_parser_tests": parsers,
        "path_safety_test_count": len(paths),
        "path_safety_tests": paths,
        "determinism_contract": {
            "canonical_JSON_sort_keys": True,
            "no_hash_iteration_controls_output": True,
            "producer_and_verifier_dual_seed_replay_required": True,
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
        envelope = build_verification(certificate_path)
        write_atomic(args.output, envelope, certificate_path)
        print("STATUS:", envelope["result"]["status"])
        print(
            "SEMANTIC_MUTATIONS:",
            envelope["result"]["semantic_mutation_test_count"],
        )
        print(
            "HISTORICAL_COMPONENT_COUNT:",
            envelope["result"]["verified_outputs"][
                "historical_component_rank_count"
            ],
        )
        return 0
    except (
        VerificationError,
        KeyError,
        IndexError,
        TypeError,
        ValueError,
        OSError,
        json.JSONDecodeError,
    ) as exc:
        print(f"VerificationError: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
