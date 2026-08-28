#!/usr/bin/env python3
"""Build the Round167 bounded base-R1 exact-attachment deficit registry.

This certificate deliberately does *not* mint Gate5 full keys.  It freezes
the 32 real Round128 component/source-word attachments, aggregates them into
16 source-word rows, and materializes the 16 x 8 open-field deficit grid.
"""

from __future__ import annotations

import argparse
import copy
from fractions import Fraction
import hashlib
import json
import os
from pathlib import Path
import stat
import tempfile
from typing import Any


HERE = Path(__file__).resolve().parent
DEFAULT_OUTPUT = HERE / "cm2_round167_base_r1_exact_key_deficit_registry_certificate.json"

SCHEMA = "cm2.round167.base-r1-exact-key-deficit-registry.v1"
NAMESPACE = "round167-base-r1-exact-key-deficit-registry-v1"
MAX_INPUT_BYTES = 64 * 1024 * 1024

PINS: dict[str, str] = {
    "cm2-round128-base-r1-component-global-word-incidence-2026-07-24.json":
        "7c5f513ba9bac5c5381e5504870b783159ebbb622ca155f649429cb65ad7b10e",
    "cm2-round128-base-r1-component-global-word-incidence-verification-2026-07-24.json":
        "3798cb3e38b7f26de0a5361234d57ef626bd7f990e26d6c787f0abf62647a76d",
    "cm2-round131-global-symbolic-support-deficit-2026-07-24.json":
        "e01ba9eb3cbd6dd4f4bdcafe7e11c7397a493ba4774315b4b440e52d177665a6",
    "cm2-round131-global-symbolic-support-deficit-verification-2026-07-24.json":
        "259c8a1953b62c47db741cd892725ae26463b641c4c290e63a8d4ef91ded3088",
    "cm2-round133-round132-owner-map-realizability-audit-2026-07-24.json":
        "a020ce376c1398384e5f304aff320aa214721f5f8d8bcc1e35bfa31eadd54c91",
    "cm2-round133-round132-owner-map-realizability-audit-verification-2026-07-24.json":
        "f41a45baf3cffab63a3429b66c2f3c9473394024a4ae4c9a234df13e3410794f",
    "cm2-round135-rank3-wide-positive-borel-local-robustness-2026-07-24.json":
        "31b4b017ac7da341b210d28dc2296ba2499d425615f2c3bce750ccec586f67df",
    "cm2-round135-rank3-wide-positive-borel-local-robustness-verification-2026-07-24.json":
        "caaebfdaa85c95d269af32c044de00c313355ddb501570e3bfbe4871231235e7",
    "cm2-round147-gate5-strict-reaudit-upgrade-frontier-2026-07-24.json":
        "db7f1a01f36c56dc537a4873dcd232808c337298a0998608a2c34aeaaa7531ee",
    "cm2-round147-gate5-strict-reaudit-upgrade-frontier-verification-2026-07-24.json":
        "8302642619f66a4a47ec79d8fefb0230378331b578a363f12ad1b64dffebbd3d",
    "cm2-round148-atomic-future-input-admission-2026-07-24.json":
        "7ab3a83998b34811f6af38ea50630a94a3a32a3e43f889b75331e2db716800e3",
    "cm2-round148-atomic-future-input-admission-verification-2026-07-24.json":
        "dacaf48cb0ae968983ce28dd1006f11fc7ebfc1a24c2b2bd2589b72ffd4c6842",
    "cm2_round163_outgoing_chart_pruning_certificate.json":
        "90d3313004be90049efb116a44731aef2554056661ce83b85afafdf3e3738539",
    "cm2_round163_outgoing_chart_pruning_verification.json":
        "28ab965bffb0ab04d4fd839f1f7f895dbbab3a8e5be250a17fa95b7a8cc825d6",
}

CERT_NAMES = {
    "r128": "cm2-round128-base-r1-component-global-word-incidence-2026-07-24.json",
    "r131": "cm2-round131-global-symbolic-support-deficit-2026-07-24.json",
    "r133": "cm2-round133-round132-owner-map-realizability-audit-2026-07-24.json",
    "r135": "cm2-round135-rank3-wide-positive-borel-local-robustness-2026-07-24.json",
    "r147": "cm2-round147-gate5-strict-reaudit-upgrade-frontier-2026-07-24.json",
    "r148": "cm2-round148-atomic-future-input-admission-2026-07-24.json",
    "r163": "cm2_round163_outgoing_chart_pruning_certificate.json",
}

VERIFICATION_NAMES = {
    "r128": "cm2-round128-base-r1-component-global-word-incidence-verification-2026-07-24.json",
    "r131": "cm2-round131-global-symbolic-support-deficit-verification-2026-07-24.json",
    "r133": "cm2-round133-round132-owner-map-realizability-audit-verification-2026-07-24.json",
    "r135": "cm2-round135-rank3-wide-positive-borel-local-robustness-verification-2026-07-24.json",
    "r147": "cm2-round147-gate5-strict-reaudit-upgrade-frontier-verification-2026-07-24.json",
    "r148": "cm2-round148-atomic-future-input-admission-verification-2026-07-24.json",
    "r163": "cm2_round163_outgoing_chart_pruning_verification.json",
}

OPEN_FIELDS = (5, 6, 10, 11, 14, 15, 17, 18)
SATISFIED_FIELDS = (1, 2, 3, 4, 7, 8, 9, 12, 13, 16)


class CertificateError(RuntimeError):
    """Fail-closed certificate construction error."""


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def digest(value: Any) -> str:
    return sha256_bytes(canonical_bytes(value))


def require(condition: bool, label: str) -> None:
    if not condition:
        raise CertificateError(label)


def no_duplicate_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for key, value in pairs:
        if key in out:
            raise CertificateError(f"duplicate JSON key: {key}")
        out[key] = value
    return out


def read_regular_bytes(path: Path, expected_sha256: str) -> bytes:
    st = path.lstat()
    require(stat.S_ISREG(st.st_mode), f"not a regular file: {path.name}")
    require(not path.is_symlink(), f"symlink input rejected: {path.name}")
    require(st.st_nlink == 1, f"multiply linked input rejected: {path.name}")
    require(st.st_size <= MAX_INPUT_BYTES, f"oversized input: {path.name}")
    data = path.read_bytes()
    require(sha256_bytes(data) == expected_sha256, f"pin mismatch: {path.name}")
    return data


def load_pinned_envelope(name: str) -> dict[str, Any]:
    data = read_regular_bytes(HERE / name, PINS[name])
    require(not data.startswith(b"\xef\xbb\xbf"), f"BOM rejected: {name}")
    try:
        text = data.decode("utf-8", "strict")
        doc = json.loads(text, object_pairs_hook=no_duplicate_object)
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise CertificateError(f"invalid JSON input {name}: {exc}") from exc
    require(isinstance(doc, dict), f"non-object envelope: {name}")
    require(set(doc) == {"schema", "result", "result_sha256"}, f"bad envelope keys: {name}")
    require(doc["result_sha256"] == digest(doc["result"]), f"bad result digest: {name}")
    return doc


def close_row(payload: dict[str, Any]) -> dict[str, Any]:
    row = copy.deepcopy(payload)
    row["row_sha256"] = digest(row)
    return row


def row_id(prefix: str, payload: Any) -> str:
    return f"{prefix}:{digest([NAMESPACE, payload])}"


def validate_verification_pass(doc: dict[str, Any], label: str) -> None:
    result = doc["result"]
    require(isinstance(result, dict), f"{label} verification result is not an object")
    require(result.get("status") == "PASS", f"{label} verification is not PASS")


def validate_upstreams(docs: dict[str, dict[str, Any]]) -> None:
    for label, name in VERIFICATION_NAMES.items():
        validate_verification_pass(docs[name], label)

    r128 = docs[CERT_NAMES["r128"]]["result"]
    a128 = r128["A_base_R1_component_to_global_word_incidence"]
    d128 = r128["D_global_safety_and_nonpromotion"]
    require(a128["component_incidence_row_count"] == 32, "Round128 component count")
    require(a128["directed_source_destination_word_edge_count"] == 16, "Round128 edge count")
    require(a128["distinct_source_official_word_count"] == 16, "Round128 source-word count")
    require(a128["components_per_edge"] == 2, "Round128 components per edge")
    require(a128["reciprocal_unordered_word_pair_count"] == 8, "Round128 reciprocal pair count")
    require(a128["numeric_F10_F13_F16_attachment_role"] == "source_official_word", "Round128 attachment role")
    require(d128["gate5_global_maturity"] == "10/18", "Round128 maturity")
    require(d128["global_complete_18_field_block_count"] == 0, "Round128 global block count")
    require(d128["Round67_owner_to_path_crosswalk_row_count"] == 0, "Round128 owner/path count")

    component_rows = a128["component_incidence_rows"]
    require(len(component_rows) == 32, "Round128 component row length")
    require(digest(component_rows) == a128["component_incidence_rows_sha256"], "Round128 component list digest")
    for row in component_rows:
        payload = dict(row)
        stored = payload.pop("row_sha256")
        require(stored == digest(payload), "Round128 component row closure")

    edge_rows = a128["source_destination_word_edge_rows"]
    require(len(edge_rows) == 16, "Round128 edge row length")
    require(digest(edge_rows) == a128["source_destination_word_edge_rows_sha256"], "Round128 edge list digest")
    for row in edge_rows:
        payload = dict(row)
        stored = payload.pop("row_sha256")
        require(stored == digest(payload), "Round128 edge row closure")

    r131 = docs[CERT_NAMES["r131"]]["result"]
    require(r131["status"] == "VERIFIED_EXHAUSTIVE_SYMBOLIC_SUPPORT_DEFICIT_DECOMPOSITION", "Round131 status")
    require(r131["base_R1_incident_word_count"] == 16, "Round131 base-R1 count")
    require(r131["reciprocal_base_R1_unordered_pair_count"] == 8, "Round131 reciprocal count")
    require(r131["priority_frontier"]["next_finite_same_root_target"] == "16 base-R1 incident official words / 8 reciprocal pairs", "Round131 finite target")
    require(r131["safety_state"]["global_gate5_maturity"] == "10/18", "Round131 maturity")
    require(r131["safety_state"]["global_complete_18_field_block_count"] == 0, "Round131 block count")
    require(r131["overlap_contract"]["same_physical_root"] is False, "Round131 overlap root separation")
    require(r131["overlap_contract"]["same_operator_block"] is False, "Round131 overlap operator separation")

    r133 = docs[CERT_NAMES["r133"]]["result"]
    require(r133["status"] == "CERTIFIED_OWNER_MAP_REALIZABILITY_AUDIT__0_MATERIALIZED_OWNED_RECORDS__FIRST_BLOCKER_ACTIVE_REPRESENTATION_CROSSWALK", "Round133 status")
    require(r133["first_missing_object"]["object"] == "Round132-to-Round50 active-representation domain crosswalk", "Round133 first blocker")
    require(r133["first_missing_object"]["observed_64_rows_may_be_treated_as_complete_candidate_fibres"] is False, "Round133 incomplete fibre guard")
    require(r133["count_ledger"]["owner_key_count"] == 0, "Round133 owner count")
    require(r133["count_ledger"]["q_j_recordwise_output_count"] == 0, "Round133 q_j count")
    require(r133["global_safety"]["global_complete_18_field_block_count"] == 0, "Round133 block count")

    r135 = docs[CERT_NAMES["r135"]]["result"]
    require(r135["status"] == "CERTIFIED_WIDE_POSITIVE_BOREL_LOCAL_ROBUSTNESS_ONLY", "Round135 status")
    local135 = r135["wide_local_18_field_transport_contract"]
    require(local135["wide_family_every_exact_fibre_local_field_maturity"] == "18/18", "Round135 local maturity")
    require(local135["field_slot_count_per_exact_lambda"] == 2160, "Round135 local slot count")
    require(r135["global_safety_and_nonpromotion"]["wide_local_level_blocks_do_not_count_as_global_blocks"] is True, "Round135 noncredit guard")
    require(r135["global_safety_and_nonpromotion"]["global_complete_18_field_block_count"] == 0, "Round135 global block count")

    r147 = docs[CERT_NAMES["r147"]]["result"]
    ledger147 = r147["gate5_global_ledger"]
    require(ledger147["global_maturity_after"] == "10/18", "Round147 maturity")
    require(ledger147["global_complete_18_field_block_count_after"] == 0, "Round147 block count")
    require(tuple(ledger147["strictly_blocked_field_indices"]) == OPEN_FIELDS, "Round147 open fields")
    require(tuple(ledger147["strictly_satisfied_field_indices"]) == SATISFIED_FIELDS, "Round147 satisfied fields")

    r148 = docs[CERT_NAMES["r148"]]["result"]
    require(r148["status"] == "CERTIFIED_ATOMIC_FUTURE_INPUT_ADMISSION_AND_PARTIAL_DAG_ADVANCE", "Round148 status")
    ledger148 = r148["gate5_global_ledger"]
    require(ledger148["global_maturity_after"] == "10/18", "Round148 maturity")
    require(ledger148["global_complete_18_field_block_count"] == 0, "Round148 block count")
    require(r148["first_exact_blocker"]["node_id"] == "D02", "Round148 first blocker")
    require(r148["identifier_ledger"]["owner_v1_id"] is None, "Round148 owner must be null")
    require(r148["identifier_ledger"]["q_j_v1_output"] is None, "Round148 q_j must be null")

    r163 = docs[CERT_NAMES["r163"]]["result"]
    require(r163["status"] == "CERTIFIED_FROZEN_PREFIX_OUTGOING_CHART_PRUNING__EXTERIOR_AND_D02_STILL_BLOCKED", "Round163 status")
    require(r163["strict_nonpromotion"]["D02"] == "BLOCKED", "Round163 D02")
    require(r163["strict_nonpromotion"]["global_Gate5_fields"] == "10/18", "Round163 maturity")
    require(r163["strict_nonpromotion"]["global_complete_18_field_blocks"] == 0, "Round163 block count")
    census163 = r163["combined_frozen_prefix_census"]
    require(census163["remaining_leaf_count"] == 39348, "Round163 remaining census")
    require(census163["remaining_outgoing_chart_seam_unresolved"] == 618, "Round163 seam census")
    require(census163["remaining_tangency_graph"] == 32, "Round163 tangency census")
    require(census163["remaining_multi_candidate"] == 38180, "Round163 multi-candidate census")


def build_component_rows(r128: dict[str, Any]) -> list[dict[str, Any]]:
    source = r128["A_base_R1_component_to_global_word_incidence"]["component_incidence_rows"]
    rows: list[dict[str, Any]] = []
    seen_components: set[str] = set()
    seen_attachment_keys: set[str] = set()
    f10_sum = 0
    f13_sum = Fraction(0)
    f16_sum = Fraction(0)

    for upstream in sorted(source, key=lambda r: (r["source_official_word_ordinal"], r["component_id"])):
        require(upstream["component_id"] not in seen_components, "duplicate Round128 component")
        seen_components.add(upstream["component_id"])
        require(upstream["numeric_F10_F13_F16_attachment_role"] == "source_official_word", "non-source numeric attachment")
        require(upstream["source_and_destination_roof_level_j"] == 0, "unexpected roof level")
        require(upstream["source_and_destination_roof_level_count"] == 1, "unexpected roof count")
        require(upstream["time_j"] == 1, "unexpected time")
        require(upstream["base_parameter"] == "s=0", "unexpected base parameter")
        require(upstream["connected_rank"] == 0, "unexpected connected rank")
        require(upstream["source_official_word_key_id"] != upstream["destination_official_word_key_id"], "source/destination role collision")
        require([r["side_label"] for r in upstream["trace_rows"]] == ["inside", "outside"], "trace-side census")

        values = upstream["numeric_local_fields"]
        require(set(values) == {
            "F10_integer_upper",
            "F13_current_variation_strict_upper",
            "F16_Piola_flux_cost_strict_upper",
        }, "numeric field schema")
        f10_sum += values["F10_integer_upper"]
        f13_sum += Fraction(values["F13_current_variation_strict_upper"])
        f16_sum += Fraction(values["F16_Piola_flux_cost_strict_upper"])

        exact_payload = [
            upstream["source_official_word_key_id"],
            upstream["source_core_id"],
            upstream["path_cell_id"],
            upstream["component_id"],
            upstream["destination_face_id"],
            upstream["time_j"],
            upstream["source_and_destination_roof_level_j"],
        ]
        exact_key = row_id("round167-base-r1-component-attachment-key", exact_payload)
        require(exact_key not in seen_attachment_keys, "duplicate Round167 attachment key")
        seen_attachment_keys.add(exact_key)

        attached_fields = []
        field_specs = (
            (10, "coarea_density_regular_bound", "F10_integer_upper"),
            (13, "moving_boundary_DQ_current_and_two_traces", "F13_current_variation_strict_upper"),
            (16, "flux_face_operator_cost", "F16_Piola_flux_cost_strict_upper"),
        )
        for index, name, value_key in field_specs:
            attached_fields.append(close_row({
                "field_index": index,
                "field_name": name,
                "value": values[value_key],
                "value_key_in_Round128": value_key,
                "attachment_role": "source_official_word",
                "source_round72_field_row_sha256": upstream["source_round72_field_row_sha256"],
                "scope": "LOCAL_BASE_R1_PHYSICAL_FACE_COMPONENT_ATTACHMENT",
                "is_Gate5_full_key_slot": False,
                "creates_new_global_field_credit": False,
            }))

        row = close_row({
            "attachment_row_id": row_id("round167-base-r1-component-attachment", exact_payload),
            "attachment_key_id": exact_key,
            "attachment_key_payload": {
                "source_official_word_key_id": upstream["source_official_word_key_id"],
                "source_core_id": upstream["source_core_id"],
                "path_cell_id": upstream["path_cell_id"],
                "component_id": upstream["component_id"],
                "destination_face_id": upstream["destination_face_id"],
                "time_j": upstream["time_j"],
                "roof_level_j": upstream["source_and_destination_roof_level_j"],
            },
            "source_official_word_ordinal": upstream["source_official_word_ordinal"],
            "source_official_word_row": upstream["source_official_word_row"],
            "destination_official_word_key_id": upstream["destination_official_word_key_id"],
            "destination_official_word_ordinal": upstream["destination_official_word_ordinal"],
            "destination_official_word_row": upstream["destination_official_word_row"],
            "candidate_family_id": upstream["candidate_family_id"],
            "component_face_side": upstream["component_face_side"],
            "component_coordinate_germ": upstream["component_coordinate_germ"],
            "trace_rows": upstream["trace_rows"],
            "attached_local_numeric_field_rows": attached_fields,
            "upstream_Round128_incidence_row_id": upstream["incidence_row_id"],
            "upstream_Round128_row_sha256": upstream["row_sha256"],
            "upstream_Round71_component_row_sha256": upstream["source_round71_component_row_sha256"],
            "upstream_Round72_field_row_sha256": upstream["source_round72_field_row_sha256"],
            "numeric_fields_attach_to_source_not_destination": True,
            "homogeneous_subbranch_id": None,
            "owner_v1_id": None,
            "t54_v1_token": None,
            "q_j_v1_output": None,
            "Gate5_full_key_status": "NOT_MATERIALIZED__HOMOGENEOUS_SUBBRANCH_AND_OWNER_ROOT_CHAIN_NULL",
            "is_global_complete_18_field_block": False,
        })
        rows.append(row)

    require(len(rows) == 32, "Round167 component row count")
    require(f10_sum == 480, "Round167 F10 sum")
    require(f13_sum == Fraction(4, 125000000), "Round167 F13 sum")
    require(f16_sum == Fraction(4, 125000000), "Round167 F16 sum")
    return rows


def build_source_word_rows(
    r128: dict[str, Any],
    component_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    a128 = r128["A_base_R1_component_to_global_word_incidence"]
    edges = a128["source_destination_word_edge_rows"]
    components_by_source: dict[str, list[dict[str, Any]]] = {}
    for row in component_rows:
        word = row["attachment_key_payload"]["source_official_word_key_id"]
        components_by_source.setdefault(word, []).append(row)

    rows: list[dict[str, Any]] = []
    for edge in sorted(edges, key=lambda r: r["source_official_word_ordinal"]):
        word = edge["source_official_word_key_id"]
        component_group = sorted(components_by_source.get(word, []), key=lambda r: r["attachment_key_payload"]["component_id"])
        require(len(component_group) == 2, "source-word component multiplicity")
        require({r["attachment_key_payload"]["path_cell_id"] for r in component_group} == {edge["path_cell_id"]}, "source-word path join")
        require({r["destination_official_word_key_id"] for r in component_group} == {edge["destination_official_word_key_id"]}, "source-word destination join")
        require(sorted(r["upstream_Round128_incidence_row_id"] for r in component_group) == sorted(edge["component_incidence_row_ids"]), "source-word incidence join")

        word_payload = [
            word,
            edge["source_core_id"],
            edge["path_cell_id"],
            edge["destination_official_word_key_id"],
            edge["source_and_destination_roof_level_count"],
        ]
        row = close_row({
            "source_word_row_id": row_id("round167-base-r1-source-word-deficit", word_payload),
            "source_official_word_key_id": word,
            "source_official_word_ordinal": edge["source_official_word_ordinal"],
            "source_official_word_row": edge["source_official_word_row"],
            "source_core_id": edge["source_core_id"],
            "path_cell_id": edge["path_cell_id"],
            "destination_official_word_key_id": edge["destination_official_word_key_id"],
            "destination_official_word_ordinal": edge["destination_official_word_ordinal"],
            "destination_official_word_row": edge["destination_official_word_row"],
            "roof_level_j": 0,
            "component_attachment_row_ids": [r["attachment_row_id"] for r in component_group],
            "component_attachment_key_ids": [r["attachment_key_id"] for r in component_group],
            "component_ids": [r["attachment_key_payload"]["component_id"] for r in component_group],
            "component_count": 2,
            "attached_component_field_indices": [10, 13, 16],
            "component_values_are_not_merged_into_one_Gate5_slot": True,
            "numeric_fields_attach_to_source_not_destination": True,
            "homogeneous_subbranch_id": None,
            "owner_v1_id": None,
            "t54_v1_token": None,
            "q_j_v1_output": None,
            "Gate5_base_key_status": "INCOMPLETE__OFFICIAL_WORD_AND_ROOF_REAL__HOMOGENEOUS_SUBBRANCH_NULL",
            "same_root_F1_through_F18_status": "NOT_MATERIALIZED",
            "open_global_field_indices": list(OPEN_FIELDS),
            "global_field_credit_created": False,
            "global_complete_block_created": False,
            "upstream_Round128_edge_row_id": edge["edge_row_id"],
            "upstream_Round128_edge_row_sha256": edge["row_sha256"],
        })
        rows.append(row)

    require(len(rows) == 16, "Round167 source-word row count")
    require(len({r["source_official_word_key_id"] for r in rows}) == 16, "Round167 source-word uniqueness")
    return rows


def build_open_field_rows(
    r135: dict[str, Any],
    r147: dict[str, Any],
) -> list[dict[str, Any]]:
    global_rows = {
        row["field_index"]: row for row in r147["gate5_field_rows"]
    }
    local_rows = {
        row["field_index"]: row for row in r135["wide_field_transport_rows"]
    }
    rows: list[dict[str, Any]] = []
    for field_index in OPEN_FIELDS:
        global_row = global_rows[field_index]
        local_row = local_rows[field_index]
        require(global_row["global_credit_classification"] == "STRICTLY_BLOCKED", "open field classification")
        require(global_row["global_field_credit"] is False, "open field credit")
        require(local_row["global_field_certification_claimed"] is False, "Round135 global nonclaim")
        rows.append(close_row({
            "field_index": field_index,
            "field": global_row["field"],
            "field_name": global_row["field_name"],
            "global_credit_classification": "STRICTLY_BLOCKED",
            "strict_blocker": global_row["strict_blocker"],
            "minimum_closing_evidence": global_row["minimum_closing_evidence"],
            "Round135_local_evidence_status": "PROSPECTIVE_LOCAL_WIDE_COLLAR_ONLY",
            "Round135_local_scope": local_row["scope"],
            "Round135_transport_reason": local_row["transport_reason"],
            "Round135_same_canonical_exact_lambda_key_required": local_row["same_canonical_exact_lambda_key_required"],
            "Round135_is_different_physical_root_and_registry": True,
            "Round135_global_credit": False,
            "base_R1_component_local_attachment_count": 32 if field_index == 10 else 0,
            "base_R1_source_word_count": 16,
            "Gate5_full_key_attachment_count": 0,
            "global_field_credit": False,
        }))
    require(len(rows) == 8, "Round167 open-field row count")
    return rows


def build_deficit_cells(
    source_word_rows: list[dict[str, Any]],
    open_field_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    field_map = {row["field_index"]: row for row in open_field_rows}
    cells: list[dict[str, Any]] = []
    for word in source_word_rows:
        for field_index in OPEN_FIELDS:
            field = field_map[field_index]
            f10_present = field_index == 10
            cell_payload = [word["source_word_row_id"], field_index]
            cells.append(close_row({
                "deficit_cell_id": row_id("round167-base-r1-source-word-open-field-cell", cell_payload),
                "source_word_row_id": word["source_word_row_id"],
                "source_official_word_key_id": word["source_official_word_key_id"],
                "source_official_word_ordinal": word["source_official_word_ordinal"],
                "field_index": field_index,
                "field": field["field"],
                "field_name": field["field_name"],
                "component_local_numeric_attachment_status": (
                    "PRESENT_ON_TWO_REAL_COMPONENT_ROWS__SOURCE_ROLE_ONLY__NOT_GATE5_SLOT"
                    if f10_present else
                    "ABSENT_ON_THIS_BASE_R1_COMPONENT_REGISTRY"
                ),
                "component_local_numeric_attachment_count": 2 if f10_present else 0,
                "homogeneous_subbranch_id": None,
                "owner_v1_id": None,
                "t54_v1_token": None,
                "q_j_v1_output": None,
                "Gate5_full_key_status": "BLOCKED__HOMOGENEOUS_SUBBRANCH_AND_OWNER_ROOT_CHAIN_NULL",
                "Round135_local_wide_collar_status": "DIFFERENT_LOCAL_REGISTRY__NO_CROSS_ROOT_CREDIT",
                "strict_blocker": field["strict_blocker"],
                "minimum_closing_evidence": field["minimum_closing_evidence"],
                "global_credit": False,
                "complete_18_field_block_created": False,
            }))
    require(len(cells) == 128, "Round167 deficit-cell count")
    require(len({cell["deficit_cell_id"] for cell in cells}) == 128, "Round167 deficit-cell uniqueness")
    return cells


def build_result(docs: dict[str, dict[str, Any]]) -> dict[str, Any]:
    validate_upstreams(docs)
    r128 = docs[CERT_NAMES["r128"]]["result"]
    r131 = docs[CERT_NAMES["r131"]]["result"]
    r133 = docs[CERT_NAMES["r133"]]["result"]
    r135 = docs[CERT_NAMES["r135"]]["result"]
    r147 = docs[CERT_NAMES["r147"]]["result"]
    r148 = docs[CERT_NAMES["r148"]]["result"]
    r163 = docs[CERT_NAMES["r163"]]["result"]

    component_rows = build_component_rows(r128)
    source_word_rows = build_source_word_rows(r128, component_rows)
    open_field_rows = build_open_field_rows(r135, r147)
    deficit_cells = build_deficit_cells(source_word_rows, open_field_rows)

    base_word_ids = {r["source_official_word_key_id"] for r in source_word_rows}
    touched_base_ids = {
        row["official_word_key_id"]
        for row in r131["touched_symbolic_word_rows"]
        if row["base_R1_component_incidence"]
    }
    require(base_word_ids == touched_base_ids, "Round131/Round167 base-word set")

    producer_sha256 = sha256_bytes(Path(__file__).read_bytes())
    result = {
        "status": "CERTIFIED_BOUNDED_BASE_R1_EXACT_ATTACHMENTS_AND_OPEN_EIGHT_DEFICIT_GRID__NO_GATE5_PROMOTION",
        "audit_date": "2026-07-26",
        "scope": {
            "object": "32 real base-R1 physical face component attachments grouped under 16 source official words and 8 reciprocal pairs",
            "bounded": True,
            "source_word_count": 16,
            "component_attachment_count": 32,
            "reciprocal_pair_count": 8,
            "open_global_field_count": 8,
            "source_word_by_open_field_deficit_cell_count": 128,
            "global_symbolic_candidate_word_count": 441280,
            "is_complete_global_domain_census": False,
            "is_Gate5_full_key_registry": False,
        },
        "latest_trusted_chain": {
            "Round147_gate5_strict_reaudit": "PASS__10_OF_18__0_GLOBAL_COMPLETE_BLOCKS",
            "Round148_atomic_migration_state": {
                "certified_DAG_nodes": r148["certified_DAG_nodes"],
                "blocked_DAG_nodes": r148["blocked_DAG_nodes"],
                "first_exact_blocker": r148["first_exact_blocker"],
                "identifier_ledger": r148["identifier_ledger"],
            },
            "Round163_latest_accepted_D02_state": {
                "D02": r163["strict_nonpromotion"]["D02"],
                "D03_negative_oracle": r163["strict_nonpromotion"]["D03_negative_oracle"],
                "remaining_leaf_count": r163["combined_frozen_prefix_census"]["remaining_leaf_count"],
                "remaining_outgoing_chart_seam_unresolved": r163["combined_frozen_prefix_census"]["remaining_outgoing_chart_seam_unresolved"],
                "remaining_tangency_graph": r163["combined_frozen_prefix_census"]["remaining_tangency_graph"],
                "remaining_multi_candidate": r163["combined_frozen_prefix_census"]["remaining_multi_candidate"],
            },
            "Round133_owner_chain_state": {
                "first_missing_object": r133["first_missing_object"]["object"],
                "owner_key_count": r133["count_ledger"]["owner_key_count"],
                "q_j_recordwise_output_count": r133["count_ledger"]["q_j_recordwise_output_count"],
                "observed_rows_are_complete_candidate_fibres": False,
            },
            "Round135_local_only_state": {
                "per_exact_lambda_local_maturity": "18/18",
                "per_exact_lambda_field_slot_count": r135["wide_local_18_field_transport_contract"]["field_slot_count_per_exact_lambda"],
                "counts_as_global_complete_block": False,
                "same_physical_root_as_base_R1_rows": False,
            },
        },
        "component_attachment_rows": component_rows,
        "component_attachment_rows_sha256": digest(component_rows),
        "source_word_deficit_rows": source_word_rows,
        "source_word_deficit_rows_sha256": digest(source_word_rows),
        "open_global_field_rows": open_field_rows,
        "open_global_field_rows_sha256": digest(open_field_rows),
        "source_word_open_field_deficit_cells": deficit_cells,
        "source_word_open_field_deficit_cells_sha256": digest(deficit_cells),
        "count_ledger": {
            "component_attachment_rows": 32,
            "source_word_deficit_rows": 16,
            "open_global_field_rows": 8,
            "source_word_open_field_deficit_cells": 128,
            "real_local_F10_component_attachments": 32,
            "real_local_F13_component_attachments": 32,
            "real_local_F16_component_attachments": 32,
            "Gate5_full_key_rows": 0,
            "new_global_field_credits": 0,
            "global_complete_18_field_blocks": 0,
        },
        "global_nonpromotion": {
            "strictly_satisfied_global_field_indices": list(SATISFIED_FIELDS),
            "strictly_blocked_global_field_indices": list(OPEN_FIELDS),
            "global_Gate5_maturity_before": "10/18",
            "global_Gate5_maturity_after": "10/18",
            "global_complete_18_field_blocks_before": 0,
            "global_complete_18_field_blocks_after": 0,
            "Gate5": "NOT_CERTIFIED",
            "CM2": "NO-GO_FOR_CLAIM",
            "D02": "BLOCKED",
            "Round135_local_18_of_18_promoted": False,
            "Round128_local_F10_promoted": False,
        },
        "strict_nonclaims": [
            "a real component/source-word attachment key is not a Gate5 full key because homogeneous_subbranch_id is null",
            "Round128 F10/F13/F16 values attach only to their source official word and component provenance, never to the destination word",
            "two component values under one source word are not merged into one operator slot",
            "Round135 wide-collar local 18/18 is a different physical root and registry and receives no global credit",
            "symbolic word overlap does not identify physical roots, subbranches, owners or operator blocks",
            "no owner, t54 token, Omega_j record or q_j output is inferred from the 32 component rows",
            "no no-incidence word is classified as an empty physical domain",
            "no Gate5 field, complete block, D02 closure, D03 authorization or CM2 theorem is promoted",
        ],
        "provenance": {
            "schema": SCHEMA,
            "namespace": NAMESPACE,
            "producer_sha256": producer_sha256,
            "dependency_sha256": dict(sorted(PINS.items())),
            "append_only": True,
            "Round164_Round165_Round166_dependency_count": 0,
            "older_round_files_modified": False,
        },
    }
    return result


def safe_atomic_write(path: Path, data: bytes, protected_paths: set[Path]) -> None:
    path = Path(os.path.abspath(os.fspath(path)))
    require(path.parent.resolve() == HERE, "output must remain in deliverables")
    if path.exists() or path.is_symlink():
        st = path.lstat()
        require(stat.S_ISREG(st.st_mode), "output target is not a regular file")
        require(not path.is_symlink(), "symlink output rejected")
        require(st.st_nlink == 1, "multiply linked output rejected")
    require(path.resolve(strict=False) not in protected_paths, "output aliases a protected input")
    fd, tmp_name = tempfile.mkstemp(prefix=f".{path.name}.", suffix=".tmp", dir=path.parent)
    tmp = Path(tmp_name)
    try:
        with os.fdopen(fd, "wb") as handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(tmp, path)
        dir_fd = os.open(path.parent, os.O_RDONLY)
        try:
            os.fsync(dir_fd)
        finally:
            os.close(dir_fd)
    finally:
        if tmp.exists():
            tmp.unlink()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()

    docs = {name: load_pinned_envelope(name) for name in PINS}
    result = build_result(docs)
    envelope = {
        "schema": SCHEMA,
        "result": result,
        "result_sha256": digest(result),
    }
    data = canonical_bytes(envelope) + b"\n"
    protected = {(HERE / name).resolve() for name in PINS}
    protected.add(Path(__file__).resolve())
    safe_atomic_write(args.output, data, protected)
    print(f"PASS {args.output}")
    print(f"certificate_sha256={sha256_bytes(data)}")
    print(f"result_sha256={envelope['result_sha256']}")


if __name__ == "__main__":
    main()
