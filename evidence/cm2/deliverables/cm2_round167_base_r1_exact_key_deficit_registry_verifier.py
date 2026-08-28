#!/usr/bin/env python3
"""Independent fail-closed verifier for the Round167 deficit registry.

The verifier imports and executes neither the Round167 producer nor any
Round167 helper.  It independently rebuilds all 32 + 16 + 8 + 128 rows from
byte-pinned upstream certificates and compares the full closed result.
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
PRODUCER = HERE / "cm2_round167_base_r1_exact_key_deficit_registry.py"
DEFAULT_CERTIFICATE = HERE / "cm2_round167_base_r1_exact_key_deficit_registry_certificate.json"
DEFAULT_OUTPUT = HERE / "cm2_round167_base_r1_exact_key_deficit_registry_verification.json"

CERTIFICATE_SCHEMA = "cm2.round167.base-r1-exact-key-deficit-registry.v1"
VERIFICATION_SCHEMA = "cm2.round167.base-r1-exact-key-deficit-registry.verification.v1"
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

VERIFICATION_NAMES = (
    "cm2-round128-base-r1-component-global-word-incidence-verification-2026-07-24.json",
    "cm2-round131-global-symbolic-support-deficit-verification-2026-07-24.json",
    "cm2-round133-round132-owner-map-realizability-audit-verification-2026-07-24.json",
    "cm2-round135-rank3-wide-positive-borel-local-robustness-verification-2026-07-24.json",
    "cm2-round147-gate5-strict-reaudit-upgrade-frontier-verification-2026-07-24.json",
    "cm2-round148-atomic-future-input-admission-verification-2026-07-24.json",
    "cm2_round163_outgoing_chart_pruning_verification.json",
)

OPEN_FIELDS = (5, 6, 10, 11, 14, 15, 17, 18)
SATISFIED_FIELDS = (1, 2, 3, 4, 7, 8, 9, 12, 13, 16)


class VerificationError(RuntimeError):
    """Fail-closed verification error."""


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
        raise VerificationError(label)


def reject_duplicate_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for key, value in pairs:
        if key in out:
            raise VerificationError(f"duplicate JSON key: {key}")
        out[key] = value
    return out


def read_regular(path: Path, expected_sha256: str | None = None) -> bytes:
    st = path.lstat()
    require(stat.S_ISREG(st.st_mode), f"not a regular file: {path.name}")
    require(not path.is_symlink(), f"symlink rejected: {path.name}")
    require(st.st_nlink == 1, f"multiply linked file rejected: {path.name}")
    require(st.st_size <= MAX_INPUT_BYTES, f"oversized file rejected: {path.name}")
    data = path.read_bytes()
    if expected_sha256 is not None:
        require(sha256_bytes(data) == expected_sha256, f"pin mismatch: {path.name}")
    return data


def parse_envelope_bytes(
    data: bytes,
    *,
    label: str,
    require_canonical: bool,
    expected_schema: str | None = None,
) -> dict[str, Any]:
    require(not data.startswith(b"\xef\xbb\xbf"), f"BOM rejected: {label}")
    try:
        text = data.decode("utf-8", "strict")
        doc = json.loads(text, object_pairs_hook=reject_duplicate_keys)
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise VerificationError(f"invalid JSON {label}: {exc}") from exc
    require(isinstance(doc, dict), f"non-object envelope: {label}")
    require(set(doc) == {"schema", "result", "result_sha256"}, f"bad envelope keys: {label}")
    if expected_schema is not None:
        require(doc["schema"] == expected_schema, f"schema mismatch: {label}")
    require(doc["result_sha256"] == digest(doc["result"]), f"bad result digest: {label}")
    if require_canonical:
        require(data == canonical_bytes(doc) + b"\n", f"noncanonical bytes: {label}")
    return doc


def load_pinned(name: str) -> dict[str, Any]:
    return parse_envelope_bytes(
        read_regular(HERE / name, PINS[name]),
        label=name,
        require_canonical=False,
    )


def closed(payload: dict[str, Any]) -> dict[str, Any]:
    row = copy.deepcopy(payload)
    row["row_sha256"] = digest(row)
    return row


def stable_id(prefix: str, payload: Any) -> str:
    return f"{prefix}:{digest([NAMESPACE, payload])}"


def verify_upstream_semantics(docs: dict[str, dict[str, Any]]) -> None:
    for name in VERIFICATION_NAMES:
        require(docs[name]["result"].get("status") == "PASS", f"upstream verification not PASS: {name}")

    r128 = docs[CERT_NAMES["r128"]]["result"]
    a128 = r128["A_base_R1_component_to_global_word_incidence"]
    d128 = r128["D_global_safety_and_nonpromotion"]
    require(
        (
            a128["component_incidence_row_count"],
            a128["directed_source_destination_word_edge_count"],
            a128["distinct_source_official_word_count"],
            a128["components_per_edge"],
            a128["reciprocal_unordered_word_pair_count"],
        ) == (32, 16, 16, 2, 8),
        "Round128 count contract",
    )
    require(a128["numeric_F10_F13_F16_attachment_role"] == "source_official_word", "Round128 source-role contract")
    require(d128["gate5_global_maturity"] == "10/18", "Round128 maturity")
    require(d128["global_complete_18_field_block_count"] == 0, "Round128 block count")
    require(d128["Round67_owner_to_path_crosswalk_row_count"] == 0, "Round128 owner/path guard")
    require(digest(a128["component_incidence_rows"]) == a128["component_incidence_rows_sha256"], "Round128 component closure")
    require(digest(a128["source_destination_word_edge_rows"]) == a128["source_destination_word_edge_rows_sha256"], "Round128 edge closure")
    for group in ("component_incidence_rows", "source_destination_word_edge_rows"):
        for row in a128[group]:
            payload = dict(row)
            stored = payload.pop("row_sha256")
            require(stored == digest(payload), f"Round128 {group} row closure")

    r131 = docs[CERT_NAMES["r131"]]["result"]
    require(r131["status"] == "VERIFIED_EXHAUSTIVE_SYMBOLIC_SUPPORT_DEFICIT_DECOMPOSITION", "Round131 status")
    require(r131["base_R1_incident_word_count"] == 16, "Round131 base count")
    require(r131["reciprocal_base_R1_unordered_pair_count"] == 8, "Round131 pair count")
    require(r131["priority_frontier"]["next_finite_same_root_target"] == "16 base-R1 incident official words / 8 reciprocal pairs", "Round131 target")
    require(r131["overlap_contract"]["same_physical_root"] is False, "Round131 physical separation")
    require(r131["overlap_contract"]["same_physical_subbranch"] is False, "Round131 subbranch separation")
    require(r131["overlap_contract"]["same_operator_block"] is False, "Round131 operator separation")
    require(r131["safety_state"]["global_gate5_maturity"] == "10/18", "Round131 maturity")
    require(r131["safety_state"]["global_complete_18_field_block_count"] == 0, "Round131 block count")

    r133 = docs[CERT_NAMES["r133"]]["result"]
    require(r133["first_missing_object"]["object"] == "Round132-to-Round50 active-representation domain crosswalk", "Round133 first missing object")
    require(r133["first_missing_object"]["observed_64_rows_may_be_treated_as_complete_candidate_fibres"] is False, "Round133 candidate-fibre guard")
    require(r133["count_ledger"]["owner_key_count"] == 0, "Round133 owner count")
    require(r133["count_ledger"]["q_j_recordwise_output_count"] == 0, "Round133 q_j count")
    require(r133["global_safety"]["global_complete_18_field_block_count"] == 0, "Round133 block count")

    r135 = docs[CERT_NAMES["r135"]]["result"]
    require(r135["status"] == "CERTIFIED_WIDE_POSITIVE_BOREL_LOCAL_ROBUSTNESS_ONLY", "Round135 status")
    require(r135["wide_local_18_field_transport_contract"]["wide_family_every_exact_fibre_local_field_maturity"] == "18/18", "Round135 local maturity")
    require(r135["wide_local_18_field_transport_contract"]["field_slot_count_per_exact_lambda"] == 2160, "Round135 slot count")
    require(r135["global_safety_and_nonpromotion"]["wide_local_level_blocks_do_not_count_as_global_blocks"] is True, "Round135 noncredit")

    r147 = docs[CERT_NAMES["r147"]]["result"]
    require(tuple(r147["gate5_global_ledger"]["strictly_blocked_field_indices"]) == OPEN_FIELDS, "Round147 open fields")
    require(tuple(r147["gate5_global_ledger"]["strictly_satisfied_field_indices"]) == SATISFIED_FIELDS, "Round147 satisfied fields")
    require(r147["gate5_global_ledger"]["global_maturity_after"] == "10/18", "Round147 maturity")
    require(r147["gate5_global_ledger"]["global_complete_18_field_block_count_after"] == 0, "Round147 blocks")

    r148 = docs[CERT_NAMES["r148"]]["result"]
    require(r148["first_exact_blocker"]["node_id"] == "D02", "Round148 first blocker")
    require(r148["gate5_global_ledger"]["global_maturity_after"] == "10/18", "Round148 maturity")
    require(r148["gate5_global_ledger"]["global_complete_18_field_block_count"] == 0, "Round148 blocks")
    require(all(r148["identifier_ledger"][key] is None for key in r148["identifier_ledger"]), "Round148 null identifier ledger")

    r163 = docs[CERT_NAMES["r163"]]["result"]
    require(r163["strict_nonpromotion"]["D02"] == "BLOCKED", "Round163 D02")
    require(r163["strict_nonpromotion"]["D03_negative_oracle"] == "UNAUTHORIZED", "Round163 D03")
    require(r163["strict_nonpromotion"]["global_Gate5_fields"] == "10/18", "Round163 maturity")
    require(r163["strict_nonpromotion"]["global_complete_18_field_blocks"] == 0, "Round163 blocks")
    census = r163["combined_frozen_prefix_census"]
    require(
        (
            census["remaining_leaf_count"],
            census["remaining_outgoing_chart_seam_unresolved"],
            census["remaining_tangency_graph"],
            census["remaining_multi_candidate"],
        ) == (39348, 618, 32, 38180),
        "Round163 trusted census",
    )


def reconstruct_component_rows(r128: dict[str, Any]) -> list[dict[str, Any]]:
    raw_rows = r128["A_base_R1_component_to_global_word_incidence"]["component_incidence_rows"]
    out: list[dict[str, Any]] = []
    component_ids: set[str] = set()
    attachment_ids: set[str] = set()
    totals = [0, Fraction(0), Fraction(0)]

    for raw in sorted(raw_rows, key=lambda item: (item["source_official_word_ordinal"], item["component_id"])):
        require(raw["component_id"] not in component_ids, "duplicate component")
        component_ids.add(raw["component_id"])
        require(raw["numeric_F10_F13_F16_attachment_role"] == "source_official_word", "destination attachment forbidden")
        require(raw["source_official_word_key_id"] != raw["destination_official_word_key_id"], "source/destination equality")
        require(raw["source_and_destination_roof_level_j"] == 0, "roof level")
        require(raw["source_and_destination_roof_level_count"] == 1, "roof count")
        require(raw["time_j"] == 1 and raw["base_parameter"] == "s=0" and raw["connected_rank"] == 0, "base-R1 type")
        require([row["side_label"] for row in raw["trace_rows"]] == ["inside", "outside"], "trace sides")

        numeric = raw["numeric_local_fields"]
        totals[0] += numeric["F10_integer_upper"]
        totals[1] += Fraction(numeric["F13_current_variation_strict_upper"])
        totals[2] += Fraction(numeric["F16_Piola_flux_cost_strict_upper"])
        identity = [
            raw["source_official_word_key_id"],
            raw["source_core_id"],
            raw["path_cell_id"],
            raw["component_id"],
            raw["destination_face_id"],
            raw["time_j"],
            raw["source_and_destination_roof_level_j"],
        ]
        attachment_key = stable_id("round167-base-r1-component-attachment-key", identity)
        require(attachment_key not in attachment_ids, "duplicate attachment key")
        attachment_ids.add(attachment_key)

        attached: list[dict[str, Any]] = []
        for index, name, source_name in (
            (10, "coarea_density_regular_bound", "F10_integer_upper"),
            (13, "moving_boundary_DQ_current_and_two_traces", "F13_current_variation_strict_upper"),
            (16, "flux_face_operator_cost", "F16_Piola_flux_cost_strict_upper"),
        ):
            attached.append(closed({
                "field_index": index,
                "field_name": name,
                "value": numeric[source_name],
                "value_key_in_Round128": source_name,
                "attachment_role": "source_official_word",
                "source_round72_field_row_sha256": raw["source_round72_field_row_sha256"],
                "scope": "LOCAL_BASE_R1_PHYSICAL_FACE_COMPONENT_ATTACHMENT",
                "is_Gate5_full_key_slot": False,
                "creates_new_global_field_credit": False,
            }))

        out.append(closed({
            "attachment_row_id": stable_id("round167-base-r1-component-attachment", identity),
            "attachment_key_id": attachment_key,
            "attachment_key_payload": {
                "source_official_word_key_id": raw["source_official_word_key_id"],
                "source_core_id": raw["source_core_id"],
                "path_cell_id": raw["path_cell_id"],
                "component_id": raw["component_id"],
                "destination_face_id": raw["destination_face_id"],
                "time_j": raw["time_j"],
                "roof_level_j": raw["source_and_destination_roof_level_j"],
            },
            "source_official_word_ordinal": raw["source_official_word_ordinal"],
            "source_official_word_row": raw["source_official_word_row"],
            "destination_official_word_key_id": raw["destination_official_word_key_id"],
            "destination_official_word_ordinal": raw["destination_official_word_ordinal"],
            "destination_official_word_row": raw["destination_official_word_row"],
            "candidate_family_id": raw["candidate_family_id"],
            "component_face_side": raw["component_face_side"],
            "component_coordinate_germ": raw["component_coordinate_germ"],
            "trace_rows": raw["trace_rows"],
            "attached_local_numeric_field_rows": attached,
            "upstream_Round128_incidence_row_id": raw["incidence_row_id"],
            "upstream_Round128_row_sha256": raw["row_sha256"],
            "upstream_Round71_component_row_sha256": raw["source_round71_component_row_sha256"],
            "upstream_Round72_field_row_sha256": raw["source_round72_field_row_sha256"],
            "numeric_fields_attach_to_source_not_destination": True,
            "homogeneous_subbranch_id": None,
            "owner_v1_id": None,
            "t54_v1_token": None,
            "q_j_v1_output": None,
            "Gate5_full_key_status": "NOT_MATERIALIZED__HOMOGENEOUS_SUBBRANCH_AND_OWNER_ROOT_CHAIN_NULL",
            "is_global_complete_18_field_block": False,
        }))

    require(len(out) == 32, "component output count")
    require(tuple(totals) == (480, Fraction(4, 125000000), Fraction(4, 125000000)), "numeric totals")
    return out


def reconstruct_word_rows(
    r128: dict[str, Any],
    component_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    grouped: dict[str, list[dict[str, Any]]] = {}
    for component in component_rows:
        grouped.setdefault(component["attachment_key_payload"]["source_official_word_key_id"], []).append(component)

    out: list[dict[str, Any]] = []
    edges = r128["A_base_R1_component_to_global_word_incidence"]["source_destination_word_edge_rows"]
    for edge in sorted(edges, key=lambda item: item["source_official_word_ordinal"]):
        source_word = edge["source_official_word_key_id"]
        components = sorted(grouped.get(source_word, []), key=lambda item: item["attachment_key_payload"]["component_id"])
        require(len(components) == 2, "two components per source word")
        require({item["attachment_key_payload"]["path_cell_id"] for item in components} == {edge["path_cell_id"]}, "edge path join")
        require({item["destination_official_word_key_id"] for item in components} == {edge["destination_official_word_key_id"]}, "edge destination join")
        require(sorted(item["upstream_Round128_incidence_row_id"] for item in components) == sorted(edge["component_incidence_row_ids"]), "edge incidence join")
        identity = [
            source_word,
            edge["source_core_id"],
            edge["path_cell_id"],
            edge["destination_official_word_key_id"],
            edge["source_and_destination_roof_level_count"],
        ]
        out.append(closed({
            "source_word_row_id": stable_id("round167-base-r1-source-word-deficit", identity),
            "source_official_word_key_id": source_word,
            "source_official_word_ordinal": edge["source_official_word_ordinal"],
            "source_official_word_row": edge["source_official_word_row"],
            "source_core_id": edge["source_core_id"],
            "path_cell_id": edge["path_cell_id"],
            "destination_official_word_key_id": edge["destination_official_word_key_id"],
            "destination_official_word_ordinal": edge["destination_official_word_ordinal"],
            "destination_official_word_row": edge["destination_official_word_row"],
            "roof_level_j": 0,
            "component_attachment_row_ids": [item["attachment_row_id"] for item in components],
            "component_attachment_key_ids": [item["attachment_key_id"] for item in components],
            "component_ids": [item["attachment_key_payload"]["component_id"] for item in components],
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
        }))
    require(len(out) == 16 and len({row["source_official_word_key_id"] for row in out}) == 16, "source-word output census")
    return out


def reconstruct_open_rows(r135: dict[str, Any], r147: dict[str, Any]) -> list[dict[str, Any]]:
    global_by_index = {row["field_index"]: row for row in r147["gate5_field_rows"]}
    local_by_index = {row["field_index"]: row for row in r135["wide_field_transport_rows"]}
    out: list[dict[str, Any]] = []
    for field_index in OPEN_FIELDS:
        global_row = global_by_index[field_index]
        local_row = local_by_index[field_index]
        require(global_row["global_credit_classification"] == "STRICTLY_BLOCKED", "global blocked row")
        require(global_row["global_field_credit"] is False, "global credit row")
        require(local_row["global_field_certification_claimed"] is False, "local noncredit row")
        out.append(closed({
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
    return out


def reconstruct_cells(
    word_rows: list[dict[str, Any]],
    open_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    fields = {row["field_index"]: row for row in open_rows}
    out: list[dict[str, Any]] = []
    for word in word_rows:
        for field_index in OPEN_FIELDS:
            field = fields[field_index]
            has_local_f10 = field_index == 10
            identity = [word["source_word_row_id"], field_index]
            out.append(closed({
                "deficit_cell_id": stable_id("round167-base-r1-source-word-open-field-cell", identity),
                "source_word_row_id": word["source_word_row_id"],
                "source_official_word_key_id": word["source_official_word_key_id"],
                "source_official_word_ordinal": word["source_official_word_ordinal"],
                "field_index": field_index,
                "field": field["field"],
                "field_name": field["field_name"],
                "component_local_numeric_attachment_status": (
                    "PRESENT_ON_TWO_REAL_COMPONENT_ROWS__SOURCE_ROLE_ONLY__NOT_GATE5_SLOT"
                    if has_local_f10 else
                    "ABSENT_ON_THIS_BASE_R1_COMPONENT_REGISTRY"
                ),
                "component_local_numeric_attachment_count": 2 if has_local_f10 else 0,
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
    require(len(out) == 128 and len({row["deficit_cell_id"] for row in out}) == 128, "deficit-cell census")
    return out


def reconstruct_result(
    docs: dict[str, dict[str, Any]],
    producer_sha256: str,
) -> dict[str, Any]:
    verify_upstream_semantics(docs)
    r128 = docs[CERT_NAMES["r128"]]["result"]
    r131 = docs[CERT_NAMES["r131"]]["result"]
    r133 = docs[CERT_NAMES["r133"]]["result"]
    r135 = docs[CERT_NAMES["r135"]]["result"]
    r147 = docs[CERT_NAMES["r147"]]["result"]
    r148 = docs[CERT_NAMES["r148"]]["result"]
    r163 = docs[CERT_NAMES["r163"]]["result"]

    component_rows = reconstruct_component_rows(r128)
    word_rows = reconstruct_word_rows(r128, component_rows)
    open_rows = reconstruct_open_rows(r135, r147)
    cells = reconstruct_cells(word_rows, open_rows)

    expected_word_set = {
        row["official_word_key_id"]
        for row in r131["touched_symbolic_word_rows"]
        if row["base_R1_component_incidence"]
    }
    require({row["source_official_word_key_id"] for row in word_rows} == expected_word_set, "Round131 word-set crosscheck")

    return {
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
        "source_word_deficit_rows": word_rows,
        "source_word_deficit_rows_sha256": digest(word_rows),
        "open_global_field_rows": open_rows,
        "open_global_field_rows_sha256": digest(open_rows),
        "source_word_open_field_deficit_cells": cells,
        "source_word_open_field_deficit_cells_sha256": digest(cells),
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
            "schema": CERTIFICATE_SCHEMA,
            "namespace": NAMESPACE,
            "producer_sha256": producer_sha256,
            "dependency_sha256": dict(sorted(PINS.items())),
            "append_only": True,
            "Round164_Round165_Round166_dependency_count": 0,
            "older_round_files_modified": False,
        },
    }


def verify_resigned_mutations(expected: dict[str, Any]) -> list[dict[str, str]]:
    mutations: list[tuple[str, Any]] = [
        ("promote_gate5", lambda r: r["global_nonpromotion"].__setitem__("Gate5", "CERTIFIED")),
        ("promote_maturity", lambda r: r["global_nonpromotion"].__setitem__("global_Gate5_maturity_after", "11/18")),
        ("invent_global_block", lambda r: r["global_nonpromotion"].__setitem__("global_complete_18_field_blocks_after", 1)),
        ("close_D02", lambda r: r["global_nonpromotion"].__setitem__("D02", "CERTIFIED")),
        ("invent_homogeneous_subbranch", lambda r: r["component_attachment_rows"][0].__setitem__("homogeneous_subbranch_id", "forged")),
        ("invent_owner", lambda r: r["component_attachment_rows"][0].__setitem__("owner_v1_id", "forged")),
        ("move_numeric_fields_to_destination", lambda r: r["component_attachment_rows"][0].__setitem__("numeric_fields_attach_to_source_not_destination", False)),
        ("promote_Round135_local", lambda r: r["global_nonpromotion"].__setitem__("Round135_local_18_of_18_promoted", True)),
        ("promote_local_F10", lambda r: r["global_nonpromotion"].__setitem__("Round128_local_F10_promoted", True)),
        ("credit_deficit_cell", lambda r: r["source_word_open_field_deficit_cells"][0].__setitem__("global_credit", True)),
        ("drop_source_word", lambda r: r["source_word_deficit_rows"].pop()),
        ("drop_open_field", lambda r: r["open_global_field_rows"].pop()),
        ("duplicate_component", lambda r: r["component_attachment_rows"].append(copy.deepcopy(r["component_attachment_rows"][0]))),
        ("erase_nonclaim", lambda r: r["strict_nonclaims"].pop()),
    ]
    rows: list[dict[str, str]] = []
    expected_doc = {
        "schema": CERTIFICATE_SCHEMA,
        "result": expected,
        "result_sha256": digest(expected),
    }
    expected_bytes = canonical_bytes(expected_doc) + b"\n"
    for label, mutate in mutations:
        changed = copy.deepcopy(expected)
        mutate(changed)
        candidate = {
            "schema": CERTIFICATE_SCHEMA,
            "result": changed,
            "result_sha256": digest(changed),
        }
        candidate_bytes = canonical_bytes(candidate) + b"\n"
        require(candidate_bytes != expected_bytes, f"mutation did not alter bytes: {label}")
        parsed = parse_envelope_bytes(
            candidate_bytes,
            label=f"mutation:{label}",
            require_canonical=True,
            expected_schema=CERTIFICATE_SCHEMA,
        )
        rejected = parsed["result"] != expected
        require(rejected, f"re-signed mutation accepted: {label}")
        rows.append({"attack": label, "status": "REJECTED"})
    return rows


def safe_atomic_write(path: Path, data: bytes, protected: set[Path]) -> None:
    path = Path(os.path.abspath(os.fspath(path)))
    require(path.parent.resolve() == HERE, "output must remain in deliverables")
    if path.exists() or path.is_symlink():
        st = path.lstat()
        require(stat.S_ISREG(st.st_mode), "output is not regular")
        require(not path.is_symlink(), "symlink output rejected")
        require(st.st_nlink == 1, "multiply linked output rejected")
    require(path.resolve(strict=False) not in protected, "output aliases protected input")
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
    parser.add_argument("--certificate", type=Path, default=DEFAULT_CERTIFICATE)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()

    docs = {name: load_pinned(name) for name in PINS}
    producer_bytes = read_regular(PRODUCER)
    producer_sha256 = sha256_bytes(producer_bytes)
    expected = reconstruct_result(docs, producer_sha256)

    certificate_bytes = read_regular(args.certificate)
    certificate = parse_envelope_bytes(
        certificate_bytes,
        label=args.certificate.name,
        require_canonical=True,
        expected_schema=CERTIFICATE_SCHEMA,
    )
    require(certificate["result"] == expected, "certificate result differs from independent reconstruction")
    require(certificate["result_sha256"] == digest(expected), "certificate result digest differs")

    mutation_rows = verify_resigned_mutations(expected)
    verifier_sha256 = sha256_bytes(Path(__file__).read_bytes())
    verification_result = {
        "status": "PASS",
        "certificate_schema": certificate["schema"],
        "certificate_sha256": sha256_bytes(certificate_bytes),
        "certificate_result_sha256": certificate["result_sha256"],
        "producer_sha256": producer_sha256,
        "verifier_sha256": verifier_sha256,
        "independence_contract": {
            "Round167_producer_imported": False,
            "Round167_producer_executed": False,
            "full_certificate_result_independently_reconstructed": True,
            "all_32_component_attachment_rows_reconstructed": True,
            "all_16_source_word_rows_reconstructed": True,
            "all_8_open_global_field_rows_reconstructed": True,
            "all_128_source_word_field_cells_reconstructed": True,
        },
        "replay_summary": {
            "component_attachment_rows": 32,
            "source_word_deficit_rows": 16,
            "open_global_field_rows": 8,
            "source_word_open_field_deficit_cells": 128,
            "real_local_F10_F13_F16_component_attachments_each": 32,
            "Gate5_full_key_rows": 0,
            "global_Gate5_maturity": "10/18",
            "global_complete_18_field_blocks": 0,
            "D02": "BLOCKED",
            "Round163_remaining_leaf_count": 39348,
        },
        "semantic_mutation_rejection_rows": mutation_rows,
        "semantic_mutation_rejection_count": len(mutation_rows),
        "path_safety_contract": {
            "inputs_must_be_regular_single_link_non_symlink": True,
            "pinned_input_size_limit_bytes": MAX_INPUT_BYTES,
            "certificate_requires_canonical_single_newline_JSON": True,
            "duplicate_JSON_keys_rejected": True,
            "output_alias_to_input_or_source_rejected": True,
            "atomic_replace_after_fsync": True,
        },
        "global_nonpromotion": expected["global_nonpromotion"],
    }
    verification = {
        "schema": VERIFICATION_SCHEMA,
        "result": verification_result,
        "result_sha256": digest(verification_result),
    }
    data = canonical_bytes(verification) + b"\n"
    protected = {(HERE / name).resolve() for name in PINS}
    protected.update({PRODUCER.resolve(), Path(__file__).resolve(), args.certificate.resolve()})
    safe_atomic_write(args.output, data, protected)
    print(f"PASS {args.certificate}")
    print(f"verification_sha256={sha256_bytes(data)}")
    print(f"verification_result_sha256={verification['result_sha256']}")


if __name__ == "__main__":
    main()
