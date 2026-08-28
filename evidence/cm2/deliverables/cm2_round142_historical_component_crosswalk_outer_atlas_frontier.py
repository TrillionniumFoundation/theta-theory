#!/usr/bin/env python3
"""Round142: historical-component crosswalk and outer-atlas frontier.

This append-only certificate separates two logically independent problems
that were conflated by the Round140 component frontier:

1. Round27's canonical rank uses an *unnamed* fixed bijection of the dyadic
   basis.  The frozen record contains neither its ordering nor an executable
   rank/unrank crosswalk.  We give an explicit two-model witness showing that
   the same certified R1648 component can receive different least indices
   while satisfying every frozen Round27 sentence.
2. If the prospective Round137-v1 enumeration is adopted, a complete
   centered-jet outer atlas can in principle turn least-rank exclusion into a
   symbolic rectangle/atlas query.  We freeze that exact query contract and
   the currently certified seed, but do not claim the missing outer atlas.

No historical component ID, least rank, Round35 restriction, owner, token,
q_j output, Gate5 block, or CM2 theorem is created.
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
    / "cm2-round142-historical-component-crosswalk-outer-atlas-frontier-2026-07-24.json"
)
SCHEMA = (
    "cm2.round142.historical-component-crosswalk-outer-atlas-frontier.v1"
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


class CertificationError(RuntimeError):
    pass


def require(condition: bool, label: str) -> None:
    if not condition:
        raise CertificationError(label)


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
    raise CertificationError(f"non-finite JSON token:{token}")


def no_duplicate_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        require(key not in result, f"duplicate JSON key:{key}")
        result[key] = value
    return result


def strict_json(path: Path) -> dict[str, Any]:
    metadata = path.lstat()
    require(
        stat.S_ISREG(metadata.st_mode)
        and metadata.st_nlink == 1
        and not path.is_symlink(),
        f"unsafe dependency:{path.name}",
    )
    value = json.loads(
        path.read_text(encoding="utf-8"),
        object_pairs_hook=no_duplicate_pairs,
        parse_constant=reject_constant,
    )
    require(isinstance(value, dict), f"object dependency:{path.name}")
    return value


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


def with_hash(row: dict[str, Any]) -> dict[str, Any]:
    result = dict(row)
    result["row_sha256"] = digest(row)
    return result


def validate_pair(level: int, left: int, right: int) -> None:
    require(
        isinstance(level, int)
        and level >= 2
        and isinstance(left, int)
        and isinstance(right, int)
        and 1 <= left < right <= 2**level - 1,
        "dyadic interval pair",
    )


def validate_2d_row(row: tuple[int, int, int, int, int]) -> None:
    level, a0, a1, b0, b1 = row
    validate_pair(level, a0, a1)
    validate_pair(level, b0, b1)
    require(
        any(endpoint % 2 for endpoint in (a0, a1, b0, b1)),
        "primitive common denominator",
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
        + (right - left - 1)
    )


def pair_is_even(pair: tuple[int, int]) -> bool:
    return pair[0] % 2 == 0 and pair[1] % 2 == 0


def even_pair_count_before(level: int, left: int, right: int) -> int:
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


def rank_2d(row: tuple[int, int, int, int, int]) -> int:
    validate_2d_row(row)
    level, a0, a1, b0, b1 = row
    total = interval_pair_count(level)
    even = interval_pair_count(level - 1)
    a_rank = pair_lex_rank(level, a0, a1)
    before_a = (
        a_rank * total
        - even_pair_count_before(level, a0, a1) * even
    )
    b_rank = pair_lex_rank(level, b0, b1)
    if pair_is_even((a0, a1)):
        require(not pair_is_even((b0, b1)), "primitive b pair")
        within_a = b_rank - even_pair_count_before(level, b0, b1)
    else:
        within_a = b_rank
    return even**2 + before_a + within_a


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
    keys: set[str] = set()
    if isinstance(value, dict):
        for key, child in value.items():
            keys.add(key)
            keys.update(all_keys(child))
    elif isinstance(value, list):
        for child in value:
            keys.update(all_keys(child))
    return keys


def validate_dependencies() -> dict[str, dict[str, Any]]:
    paths = (
        ROUND27,
        ROUND137,
        ROUND137_VERIFICATION,
        ROUND139,
        ROUND139_VERIFICATION,
        ROUND140,
        ROUND140_VERIFICATION,
        ROUND140_PARENT_W,
        ROUND140_PARENT_W_VERIFICATION,
    )
    for path in paths:
        require(sha256(path) == PINS[path.name], f"pin:{path.name}")

    round27 = strict_json(ROUND27)
    require(
        round27["schema"]
        == "cm2.gate34.round27-arbitrary-n-path-schema.manifest.v1",
        "Round27 schema",
    )
    component = round27["result"][
        "canonical_regular_connected_component_schema"
    ]
    require(
        component["canonical_component_rank"]
        == "least natural-number index in a fixed bijective enumeration of rational dyadic basis elements whose closure is contained in the component"
        and component["component_coordinates_and_nonempty_ranks_enumerated"]
        is False,
        "Round27 historical boundary",
    )

    round137 = closed_result(
        ROUND137,
        "cm2.round137.seed-independent-dyadic-basis-rank-contract.v1",
        "CERTIFIED_PROSPECTIVE_SEED_INDEPENDENT_DYADIC_BASIS_RANK_CONTRACT",
    )
    audit = round137["historical_schema_audit"]
    require(
        audit["historical_enumeration_order_frozen"] is False
        and audit["historical_rank_unrank_algorithm_frozen"] is False
        and audit["historical_zero_or_one_based_indexing_frozen"] is False
        and audit["new_v1_recovers_historical_numeric_labels"] is False,
        "Round137 historical audit",
    )
    r137v = closed_result(
        ROUND137_VERIFICATION,
        "cm2.round137.seed-independent-dyadic-basis-rank-contract-verification.v1",
        "PASS",
    )
    require(r137v["status"] == "PASS", "Round137 verification")

    round139 = closed_result(
        ROUND139,
        "cm2.round139.rank3-minus-d0-adjacent-h1-collar-return-frontier.v1",
        "CERTIFIED_MINUS_D0_ADJACENT_H1_COLLAR_STRICT_FIRST_RETURN",
    )
    require(
        round139["deep_same_D0_root_and_b_star"]["deep_D0_unique"] is True
        and round139["collision3_analytic_anchor_exclusion"][
            "exact_D3_zero_only_at_excluded_endpoint_x_star"
        ]
        is True
        and round139["corrected_rank3_source_contract"]["source_core_id"]
        == SOURCE_CORE_ID,
        "Round139 D0 boundary",
    )
    r139v = closed_result(
        ROUND139_VERIFICATION,
        "cm2.round139.rank3-minus-d0-adjacent-h1-collar-return-frontier-verification.v1",
        "PASS",
    )
    require(r139v["status"] == "PASS", "Round139 verification")

    round140 = closed_result(
        ROUND140,
        "cm2.round140.fixed-s-adaptive-component-identity-bridge.v1",
        "CERTIFIED_FIXED_S_ADAPTIVE_IDENTITY_STRICT_NONSUBSTITUTION",
    )
    require(
        round140["Round27_path_instance"][
            "Round27_compatible_candidate_path_tuple_sha256"
        ]
        == PATH_SHA256
        and round140["fixed_s_adaptive_path_cell"]["adaptive_path_cell_id"]
        == ADAPTIVE_ID
        and round140["unique_containing_maximal_component_bridge"][
            "unique_containing_component_locator_id"
        ]
        == CONTAINING_LOCATOR
        and round140["unique_containing_maximal_component_bridge"][
            "historical_Round27_least_basis_rank"
        ]
        is None,
        "Round140 bridge",
    )
    r140v = closed_result(
        ROUND140_VERIFICATION,
        "cm2.round140.fixed-s-adaptive-component-identity-bridge-verification.v1",
        "PASS",
    )
    require(r140v["status"] == "PASS", "Round140 verification")

    parent_w = closed_result(
        ROUND140_PARENT_W,
        "cm2.round140.round35-parent-w-r1648-materialization-audit.v1",
        "CERTIFIED_MAXIMAL_LEGAL_ROUND35_PARENT_W_DATA_FROM_R1648",
    )
    require(
        parent_w["maximal_legal_Round35_field_status"][
            "historical_Round27_component_rank_materialized"
        ]
        is False
        and parent_w["maximal_legal_Round35_field_status"][
            "Round35_source_parent_W_id_materialized"
        ]
        is False,
        "Round140 parent-W boundary",
    )
    pwv = closed_result(
        ROUND140_PARENT_W_VERIFICATION,
        "cm2.round140.round35-parent-w-r1648-materialization-audit-verification.v1",
        "PASS",
    )
    require(pwv["status"] == "PASS", "Round140 parent-W verification")
    return {
        "round27": round27,
        "round137": round137,
        "round139": round139,
        "round140": round140,
        "parent_w": parent_w,
    }


def build() -> dict[str, Any]:
    loaded = validate_dependencies()
    round27 = loaded["round27"]
    round137 = loaded["round137"]
    round139 = loaded["round139"]
    round140 = loaded["round140"]

    historical_component = round27["result"][
        "canonical_regular_connected_component_schema"
    ]
    historical_audit = round137["historical_schema_audit"]
    historical_keys = all_keys(round27)
    absent_executable_fields = [
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
        if key not in historical_keys
    ]
    require(len(absent_executable_fields) == 9, "historical fields absent")

    witness = round140["Round137_v1_contained_basis_upper_bound"]
    parent_row = tuple(witness["contained_primitive_basis_row"])
    require(len(parent_row) == 5, "parent basis row")
    validate_2d_row(parent_row)
    parent_rank = rank_2d(parent_row)
    require(
        encoded_integer(parent_rank)
        == witness["contained_primitive_basis_rank"],
        "parent basis rank",
    )
    level, a0, a1, b0, b1 = parent_row
    require(a1 == a0 + 1 and b1 == b0 + 1, "consecutive parent")

    inside_a = (level + 1, 2 * a0, 2 * a0 + 1, 2 * b0, 2 * b0 + 1)
    inside_b = (
        level + 1,
        2 * a0 + 1,
        2 * a1,
        2 * b0,
        2 * b0 + 1,
    )
    validate_2d_row(inside_a)
    validate_2d_row(inside_b)
    pa = row_box(parent_row)
    ca = row_box(inside_a)
    cb = row_box(inside_b)
    require(
        pa[0] <= ca[0] < ca[1] <= pa[1]
        and pa[2] <= ca[2] < ca[3] <= pa[3]
        and pa[0] <= cb[0] < cb[1] <= pa[1]
        and pa[2] <= cb[2] < cb[3] <= pa[3],
        "children nested in parent",
    )
    inside_rows = []
    for name, row in (("A", inside_a), ("B", inside_b)):
        payload = [
            "round142-inside-basis-witness-v1",
            ADAPTIVE_ID,
            name,
            list(row),
        ]
        inside_rows.append(
            with_hash({
                "name": name,
                "primitive_basis_row": list(row),
                "Round137_v1_rank": encoded_integer(rank_2d(row)),
                "closure_contained_in_Round140_parent_basis_box": True,
                "closure_strictly_inside_adaptive_R1648_cell": True,
                "closure_contained_in_unique_maximal_component_U": True,
                "witness_id":
                    "round142-inside-basis:" + digest(payload),
            })
        )

    normalization_rows = round137[
        "source_core_affine_normalization_contract"
    ]["normalization_rows"]
    normalization = [
        row
        for row in normalization_rows
        if row["source_core_id"] == SOURCE_CORE_ID
    ]
    require(len(normalization) == 1, "source normalization")
    normalization = normalization[0]
    ct0, ct1 = (Q(value) for value in normalization["t_bounds"])
    cp0, cp1 = (Q(value) for value in normalization["p_bounds"])
    collar = round139["minus_D0_adjacent_H1_collar"]
    tlo, thi = (Q(value) for value in collar["t_image_outer"])
    plo, phi = (Q(value) for value in collar["p_image_outer"])
    u = ((tlo - ct0) / (ct1 - ct0), (thi - ct0) / (ct1 - ct0))
    v = ((plo - cp0) / (cp1 - cp0), (phi - cp0) / (cp1 - cp0))
    outside_row = (5, 30, 31, 8, 9)
    validate_2d_row(outside_row)
    outside_box = row_box(outside_row)
    require(
        outside_box[0] <= u[0] <= u[1] <= outside_box[1]
        and outside_box[2] <= v[0] <= v[1] <= outside_box[3],
        "D0 enclosure in outside basis box",
    )
    d0_normalized_enclosure = {
        "u": [qstr(value) for value in u],
        "v": [qstr(value) for value in v],
    }
    outside_payload = [
        "round142-D0-crossing-outside-basis-v1",
        SOURCE_CORE_ID,
        list(outside_row),
        digest(d0_normalized_enclosure),
        round139["deep_same_D0_root_and_b_star"]["row_sha256"],
    ]
    outside_witness = with_hash({
        "primitive_basis_row": list(outside_row),
        "Round137_v1_rank": encoded_integer(rank_2d(outside_row)),
        "normalized_D0_collar_enclosure_sha256":
            digest(d0_normalized_enclosure),
        "whole_certified_D0_collar_enclosure_in_box_closure": True,
        "exact_D3_zero_point_x_star_in_enclosure": True,
        "x_star_is_excluded_collision3_tangency_boundary": True,
        "box_closure_is_not_contained_in_regular_path_component_U": True,
        "outside_witness_id":
            "round142-D0-crossing-outside-basis:" + digest(outside_payload),
    })

    require(
        inside_rows[0]["primitive_basis_row"]
        != outside_witness["primitive_basis_row"],
        "inside/outside rows distinct",
    )
    ambiguity_payload = [
        "round142-historical-enumeration-underdetermination-v1",
        CONTAINING_LOCATOR,
        inside_rows[0]["witness_id"],
        outside_witness["outside_witness_id"],
    ]
    ambiguity = with_hash({
        "proof_kind": "TWO_COMPATIBLE_FIXED_BIJECTIONS",
        "component_locator": CONTAINING_LOCATOR,
        "inside_basis_witness": inside_rows[0]["witness_id"],
        "outside_basis_witness": outside_witness["outside_witness_id"],
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

    negative_oracle_contract = with_hash({
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
        negative_oracle_contract["row_sha256"],
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
            "leaf_coordinate":
                "x=sqrt(17)*r, r=(4/25)*asin(t)",
            "transverse_coordinate":
                "beta=(asin(p)-4r)-b_star",
            "centered_generators": ["delta_x", "delta_beta"],
        },
        "certified_seed_cell_id": ADAPTIVE_ID,
        "certified_seed_cell_count": 1,
        "certified_seed_connected": True,
        "certified_seed_same_1648_path": True,
        "certified_seed_positive_area": True,
        "certified_seed_adjacency_edge_count": 0,
        "certified_leaf_event_endpoints": [
            {
                "event": "collision3_D3_zero",
                "coordinate": "x_star",
                "role": "right_leaf_boundary_candidate",
                "certified_exact_on_leaf": True,
                "certified_as_complete_2D_component_face": False,
            }
        ],
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

    crosswalk_audit = with_hash({
        "Round27_rank_definition":
            historical_component["canonical_component_rank"],
        "Round27_component_ID_definition":
            historical_component["canonical_component_id"],
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
        "absent_executable_field_count": len(absent_executable_fields),
        "absent_executable_fields": absent_executable_fields,
        "Round137_v1_is_prospective_not_a_historical_crosswalk": True,
        "an_outer_atlas_alone_can_recover_historical_numeric_rank": False,
        "exact_first_blocker":
            "no unique historical enumeration is defined by the frozen Round27 bytes",
    })

    frontier_payload = [
        "round142-historical-component-frontier-v1",
        crosswalk_audit["row_sha256"],
        ambiguity["row_sha256"],
        atlas["row_sha256"],
        negative_oracle_contract["row_sha256"],
    ]
    result = {
        "status":
            "CERTIFIED_HISTORICAL_ENUMERATION_UNDERDETERMINATION_AND_OUTER_ATLAS_FRONTIER",
        "provenance": {
            "dependency_sha256": dict(sorted(PINS.items())),
            "append_only": True,
            "Round139_or_Round140_files_modified": False,
        },
        "historical_definition_and_crosswalk_audit": crosswalk_audit,
        "inside_basis_witnesses": {
            "Round140_parent_basis_row": list(parent_row),
            "Round140_parent_basis_rank":
                witness["contained_primitive_basis_rank"],
            "strictly_nested_child_count": len(inside_rows),
            "strictly_nested_children": inside_rows,
            "children_sha256": digest(inside_rows),
        },
        "D0_crossing_outside_basis_witness": outside_witness,
        "two_enumeration_model_underdetermination_proof": ambiguity,
        "prospective_v1_symbolic_negative_oracle_contract":
            negative_oracle_contract,
        "centered_jet_outer_atlas_frontier": atlas,
        "frontier_id":
            "round142-historical-component-frontier:"
            + digest(frontier_payload),
        "strict_nonpromotion": {
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
        "strict_nonclaims": [
            "the two enumeration models prove underdetermination; neither is asserted to be the unnamed historical enumeration",
            "Round137-v1 is not retroactively substituted for the Round27 enumeration",
            "the one-cell adaptive registry is not the maximal regular path component",
            "the D0 leaf endpoint is not promoted to a complete two-dimensional boundary face",
            "the symbolic negative-oracle contract is not a completed negative oracle",
            "no historical component rank/ID or Round35 restriction is minted",
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
        *((HERE / name).resolve() for name in PINS),
    }


def validate_output_target(path: Path) -> Path:
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


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=OUTPUT)
    args = parser.parse_args()
    envelope = build()
    write_atomic(args.output, envelope)
    print("STATUS:", envelope["result"]["status"])
    print(
        "AMBIGUITY_ID:",
        envelope["result"][
            "two_enumeration_model_underdetermination_proof"
        ]["ambiguity_proof_id"],
    )
    print(
        "HISTORICAL_COMPONENT_COUNT:",
        envelope["result"]["strict_nonpromotion"][
            "new_historical_Round27_component_rank_count"
        ],
    )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (CertificationError, KeyError, TypeError, ValueError, OSError) as exc:
        print(f"CertificationError: {exc}", file=sys.stderr)
        raise SystemExit(1)
