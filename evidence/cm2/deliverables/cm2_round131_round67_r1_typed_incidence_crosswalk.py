#!/usr/bin/env python3
"""Round131: fail-closed Round67-to-base-R1 typed-incidence crosswalk.

This producer does not invent a Round67 occurrence/owner record or identify a
Round71/72 terminal-preimage face with an interior return point.  It pins and
replays the certified Round67, Round71, Round72 and Round128 inputs, materializes
all 32 currently unmatched positive base-R1 components, and records the exact
twelve-field and coordinate-map obstruction.

Round69 certifies that strict-inner R1 incidence of the Round67 underlying
moving-occurrence carrier is empty; a Round71/72 stationary-terminal-preimage
component is not an occurrence pullback.  The first admissible future match is
therefore a deterministic Borel typed-incidence row in
Omega_j x occurrence_pullback_face x R_n_path_cell, with n>=2 the first depth
not already ruled out.  Until such a row carries all twelve recordwise
coordinates and an exact coordinate map, the match registry is empty, Round72
F10/F13/F16 remain component-local, global Gate5 remains 10/18 with zero
complete blocks, and CM2 remains NO-GO.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import stat
import tempfile
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent
PRODUCER = Path(__file__).resolve()
OUTPUT = (
    HERE
    / "cm2-round131-round67-r1-typed-incidence-crosswalk-2026-07-24.json"
)
SCHEMA = "cm2.round131.round67-r1-typed-incidence-crosswalk.v1"

ROUND67_PRODUCER = (
    HERE
    / "cm2_round67_fixed_j_occurrence_owner_root_time_potential_frontier_cert.py"
)
ROUND67_MANIFEST = (
    HERE
    / "cm2-round67-fixed-j-occurrence-owner-root-time-potential-frontier-manifest-2026-07-21.json"
)
ROUND28_PRODUCER = (
    HERE / "cm2_gate5_round28_limiting_physical_face_atlas_frontier_cert.py"
)
ROUND28_MANIFEST = (
    HERE
    / "cm2-gate5-round28-limiting-physical-face-atlas-frontier-manifest-2026-07-18.json"
)
ROUND69_MANIFEST = (
    HERE
    / "cm2-round69-base-s-return-incidence-all-gate-manifest-2026-07-21.json"
)
ROUND71_PRODUCER = HERE / "cm2_round71_r1_nonempty_face_germs_cert.py"
ROUND71_WITNESSES = (
    HERE / "cm2-round71-r1-nonempty-face-witnesses-2026-07-21.json"
)
ROUND71_MANIFEST = (
    HERE / "cm2-round71-r1-nonempty-face-germs-manifest-2026-07-21.json"
)
ROUND72_PRODUCER = HERE / "cm2_round72_r1_full_atlas_f10_f13_f16_cert.py"
ROUND72_PROOF = (
    HERE / "cm2-round72-r1-component-f10-f13-f16-proof-2026-07-21.json"
)
ROUND72_MANIFEST = (
    HERE
    / "cm2-round72-r1-full-atlas-f10-f13-f16-manifest-2026-07-21.json"
)
ROUND128_PRODUCER = (
    HERE / "cm2_round128_base_r1_component_global_word_incidence.py"
)
ROUND128_CERTIFICATE = (
    HERE / "cm2-round128-base-r1-component-global-word-incidence-2026-07-24.json"
)
ROUND128_VERIFIER = (
    HERE / "cm2_round128_base_r1_component_global_word_incidence_verifier.py"
)
ROUND128_VERIFICATION = (
    HERE
    / "cm2-round128-base-r1-component-global-word-incidence-verification-2026-07-24.json"
)

INPUTS = (
    ROUND67_PRODUCER,
    ROUND67_MANIFEST,
    ROUND28_PRODUCER,
    ROUND28_MANIFEST,
    ROUND69_MANIFEST,
    ROUND71_PRODUCER,
    ROUND71_WITNESSES,
    ROUND71_MANIFEST,
    ROUND72_PRODUCER,
    ROUND72_PROOF,
    ROUND72_MANIFEST,
    ROUND128_PRODUCER,
    ROUND128_CERTIFICATE,
    ROUND128_VERIFIER,
    ROUND128_VERIFICATION,
)

BYTE_PINS = {
    ROUND67_PRODUCER.name:
        "cfb501aff4f321742e3fead9895c596e9105b2a89d064d917646b70c6f91ee8f",
    ROUND67_MANIFEST.name:
        "97cb410b9e960d8331a37ef9203b040c9b1d86c3ed3d1ba6ba66a28c4e4ff400",
    ROUND28_PRODUCER.name:
        "b0dda23ec7e8c9dbe82aff861be6b4e1d38ecf281a82165949537b923150ba27",
    ROUND28_MANIFEST.name:
        "ad385983a4152da3bc1d9c58a5a2fba1abb928466ecf9a9f61260b612bddf140",
    ROUND69_MANIFEST.name:
        "08d996d52d6aa8ea3b716a46b51d6ae8f0a6b4b9e24c9fab402afe88059bc838",
    ROUND71_PRODUCER.name:
        "ec5b229a7a624ca37f93884d938e26a5e946ff4254edf24cd9a7e7d98d8c6c72",
    ROUND71_WITNESSES.name:
        "3226044b8d0718a0d565c7ff9dd6c4736d2b1d28fa784c46443da92e85b61cc6",
    ROUND71_MANIFEST.name:
        "fb7fd4233d14834ca6a3efc488c2e8f1fcdf97bdeb410a1b93eda8d9b59d50f9",
    ROUND72_PRODUCER.name:
        "bf0a9ced0b66174b100dfe195666312215ce9a873558c48787669e0f77da04f9",
    ROUND72_PROOF.name:
        "12c1f1db87030cf63552621a24ac0ebb1adb39933dc420497b425fb3c1f8e8a9",
    ROUND72_MANIFEST.name:
        "4bb012ae54db337cbdaa8cdc02aee55025dd522ccc566a7fb343b57010d4f6f9",
    ROUND128_PRODUCER.name:
        "d218d92a6aa7a929e734c86110e67ec8ebea75b3c57bf74e5a7d3b3e33d32e35",
    ROUND128_CERTIFICATE.name:
        "7c5f513ba9bac5c5381e5504870b783159ebbb622ca155f649429cb65ad7b10e",
    ROUND128_VERIFIER.name:
        "2745ccccdab9869c4754bab37f13ece70f32c7b59063bf0aed4f59cdd81af544",
    ROUND128_VERIFICATION.name:
        "3798cb3e38b7f26de0a5361234d57ef626bd7f990e26d6c787f0abf62647a76d",
}

SCHEMA_PINS = {
    ROUND67_MANIFEST.name:
        "cm2.round67.fixed-j-occurrence-owner-root-time-potential.v1.manifest.v1",
    ROUND28_MANIFEST.name:
        "cm2.gate5.round28-limiting-physical-face-atlas-frontier.manifest.v3",
    ROUND69_MANIFEST.name:
        "cm2.round69.base-s-return-incidence-all-gate.v1.manifest.v1",
    ROUND71_WITNESSES.name:
        "cm2.round71.r1-nonempty-face-witnesses.v1",
    ROUND71_MANIFEST.name:
        "cm2.round71.r1-nonempty-face-germs.v1.manifest.v1",
    ROUND72_PROOF.name:
        "cm2.round72.r1-component-f10-f13-f16.v1",
    ROUND72_MANIFEST.name:
        "cm2.round72.r1-full-atlas-f10-f13-f16.v1.manifest.v1",
    ROUND128_CERTIFICATE.name:
        "cm2.round128.base-r1-component-global-word-incidence.v1",
    ROUND128_VERIFICATION.name:
        "cm2.round128.base-r1-component-global-word-incidence-verification.v1",
}

CANONICAL_DOCUMENT_PINS = {
    ROUND67_MANIFEST.name:
        ("result", "c1fd3e486d671b83c6ae6a0c6da8c4d50bd2796842cfe1c8d8d5985001e5a57f"),
    ROUND28_MANIFEST.name:
        ("result", "282d73b9146a38ff41f78ab6d0fd619c1b955eda32ed3dd5cdae2fd170b340b6"),
    ROUND69_MANIFEST.name:
        ("result", "8cac8aead2506fddd6c8e9ee0941d3f46a06d390c7913cc3deca42812810e5c7"),
    ROUND71_WITNESSES.name:
        ("document", "519e22b33df9aab7e8ea39b1aff45c3c03eb1d06223259dec0774ec87d70b849"),
    ROUND71_MANIFEST.name:
        ("result", "59a66d6206619d8195b6bc2ccd60d85f90b9a9a581764f7160902eeec3b95107"),
    ROUND72_PROOF.name:
        ("result", "d48f78a39d51ebafe17e0288d7d2ba9f3d8127bab09b45749dc62e1c1bde94ad"),
    ROUND72_MANIFEST.name:
        ("result", "055725862200741853145ed70c2176e807dba675a7f1a2f17e827765e07e740b"),
    ROUND128_CERTIFICATE.name:
        ("result", "46601ee43c7ca8051dac51fd608605a814abfb755092ea8225fd3f0f2c755815"),
    ROUND128_VERIFICATION.name:
        ("result", "2037fb4ad60901824b9a107e51b6092f761dcb9b2d47da1c2f76e2cb06926b45"),
}

REQUIRED_FIELDS = [
    "restriction_id",
    "return_component",
    "insertion_time",
    "collision_index",
    "event_signature",
    "primitive_key",
    "owner_key",
    "rank_zero_component",
    "plaque_side",
    "word_cell",
    "endpoint_coordinate",
    "root_coordinate",
]

ROUND72_EVIDENCE_BY_REQUIRED_FIELD = {
    "restriction_id": [],
    "return_component": ["component_id", "path_cell_id"],
    "insertion_time": ["time_j=1"],
    "collision_index": [],
    "event_signature": [],
    "primitive_key": ["candidate_family_id"],
    "owner_key": ["source_core_id", "destination_core_id"],
    "rank_zero_component": ["component_id", "connected_rank=0"],
    "plaque_side": ["component_face_side", "inside/outside trace IDs"],
    "word_cell": [
        "path_cell_id",
        "source_official_word_key_id",
        "destination_official_word_key_id",
    ],
    "endpoint_coordinate": ["component_coordinate_germ"],
    "root_coordinate": ["component_coordinate_germ"],
}

ROUND67_DECLARED_TOKEN_BY_REQUIRED_FIELD = {
    "restriction_id": "restriction-id",
    "return_component": None,
    "insertion_time": "time-j",
    "collision_index": None,
    "event_signature": "physical-event-signature",
    "primitive_key": "primitive-key",
    "owner_key": "owner view q_j, but no retained recordwise owner-key token",
    "rank_zero_component": "connected-rank-0",
    "plaque_side": "side-label",
    "word_cell": "word-cell",
    "endpoint_coordinate": "endpoint/root coordinates",
    "root_coordinate": "endpoint/root coordinates",
}


class VerificationError(RuntimeError):
    """Fail-closed input, semantic or output error."""


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


def sha256_path(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def strict_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        require(key not in result, f"duplicate JSON key: {key}")
        result[key] = value
    return result


def reject_constant(token: str) -> None:
    raise VerificationError(f"non-finite JSON constant: {token}")


def strict_json_path(path: Path) -> dict[str, Any]:
    raw = path.read_bytes()
    require(not raw.startswith(b"\xef\xbb\xbf"), f"UTF-8 BOM: {path.name}")
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise VerificationError(f"invalid UTF-8: {path.name}") from exc
    try:
        value = json.loads(
            text,
            object_pairs_hook=strict_object,
            parse_constant=reject_constant,
        )
    except (json.JSONDecodeError, UnicodeDecodeError) as exc:
        raise VerificationError(f"strict JSON: {path.name}") from exc
    require(isinstance(value, dict), f"top-level object: {path.name}")
    return value


def with_hash(row: dict[str, Any]) -> dict[str, Any]:
    require("row_sha256" not in row, "row already hashed")
    return {**row, "row_sha256": digest(row)}


def identifier_strings(value: Any) -> list[str]:
    pattern = re.compile(
        r"^(?:restriction:|rn-restriction:|core:|"
        r"physical-r1-face-component:|base-r1-edge-cell:|path-cell:|gate5-word:)"
    )
    found: list[str] = []

    def visit(node: Any) -> None:
        if isinstance(node, dict):
            for child in node.values():
                visit(child)
        elif isinstance(node, list):
            for child in node:
                visit(child)
        elif isinstance(node, str) and pattern.match(node):
            found.append(node)

    visit(value)
    return found


def load_inputs() -> dict[str, dict[str, Any]]:
    for path in INPUTS:
        require(path.is_file(), f"missing input: {path.name}")
        require(
            sha256_path(path) == BYTE_PINS[path.name],
            f"byte pin: {path.name}",
        )

    documents: dict[str, dict[str, Any]] = {}
    for path in INPUTS:
        if path.suffix != ".json":
            continue
        document = strict_json_path(path)
        documents[path.name] = document
        if path.name in SCHEMA_PINS:
            require(
                document.get("schema") == SCHEMA_PINS[path.name],
                f"schema pin: {path.name}",
            )
        if path.name in CANONICAL_DOCUMENT_PINS:
            scope, expected = CANONICAL_DOCUMENT_PINS[path.name]
            value = document if scope == "document" else document.get("result")
            require(value is not None, f"canonical pin scope: {path.name}")
            require(digest(value) == expected, f"canonical pin: {path.name}")

    r128 = documents[ROUND128_CERTIFICATE.name]
    v128 = documents[ROUND128_VERIFICATION.name]
    require(
        r128.get("result_sha256")
        == CANONICAL_DOCUMENT_PINS[ROUND128_CERTIFICATE.name][1],
        "Round128 stored result digest",
    )
    require(
        v128.get("result_sha256")
        == CANONICAL_DOCUMENT_PINS[ROUND128_VERIFICATION.name][1],
        "Round128 verification stored result digest",
    )
    require(v128["result"]["status"] == "PASS", "Round128 verification PASS")
    require(
        v128["result"]["certificate_sha256"]
        == BYTE_PINS[ROUND128_CERTIFICATE.name],
        "Round128 verified certificate pin",
    )
    require(
        v128["result"]["certificate_result_sha256"]
        == r128["result_sha256"],
        "Round128 verified result pin",
    )
    return documents


def build() -> dict[str, Any]:
    documents = load_inputs()
    r67 = documents[ROUND67_MANIFEST.name]["result"]
    r28 = documents[ROUND28_MANIFEST.name]["result"]
    r69 = documents[ROUND69_MANIFEST.name]["result"]
    r71_witnesses = documents[ROUND71_WITNESSES.name]
    r71 = documents[ROUND71_MANIFEST.name]["result"]
    r72_proof = documents[ROUND72_PROOF.name]["result"]
    r72 = documents[ROUND72_MANIFEST.name]["result"]
    r128 = documents[ROUND128_CERTIFICATE.name]["result"]
    v128 = documents[ROUND128_VERIFICATION.name]["result"]

    fixed = r67["actual_fixed_j_subroot"]
    require(
        fixed["status"] == "CERTIFIED_GRAPH_SUPPORTED_PHYSICAL_SUBROOT",
        "Round67 fixed-j root status",
    )
    require(
        fixed["root"]
        == "Omega_j={(a,x):x in E_(j,a)^owner intersect R_(j,a)^reg}",
        "Round67 root formula",
    )
    require(
        fixed["base_law"]
        == "finite standard-Borel endpoint-coarea occurrence law m_occ",
        "Round67 base law",
    )
    require(
        identifier_strings(r67) == [],
        "Round67 has no materialized recordwise identifiers",
    )

    occurrence_registry = r28[
        "moving_occurrence_coarea_DQ_face_seed_registry"
    ]
    require(
        occurrence_registry[
            "materialized_physical_moving_occurrence_face_seed_count"
        ] == 64,
        "Round28 occurrence seed count",
    )
    require(
        occurrence_registry[
            "materialized_oriented_hit_miss_trace_seed_count"
        ] == 128,
        "Round28 occurrence trace count",
    )
    require(
        occurrence_registry["moving_occurrence_faces_are_internal_R1_boundary_faces"]
        is False,
        "Round28 occurrence faces are not internal R1 faces",
    )
    require(
        all(
            row["physical_carrier_type"]
            == "moving_first_event_grazing_occurrence_face"
            for row in occurrence_registry["representative_face_rows"]
        ),
        "Round28 occurrence carrier type",
    )

    obstruction = r69["direct_equality_obstruction"]
    correction = r69["typed_incidence_correction"]
    require(
        obstruction["selected_base_root_occurrence_pair_count"] == 11264,
        "Round69 selected pair audit",
    )
    require(
        obstruction["selected_base_root_occurrence_intersection_count"] == 0,
        "Round69 selected equality intersection",
    )
    require(
        obstruction["recordwise_source_point_equality_is_correct_join"] is False,
        "Round69 equality is not typed join",
    )
    require(
        correction["edge_semantics"]
        == "FACE_IS_BOUNDARY_OR_PULLBACK_CARRIER_INCIDENT_TO_PATH_CELL__NOT_EQUAL_TO_INTERIOR_POINT",
        "Round69 typed edge semantics",
    )
    require(
        correction["R1_inner_moving_occurrence_incidence"]
        == "CERTIFIED_EMPTY",
        "Round69 R1 occurrence incidence is empty",
    )
    require(
        correction[
            "arbitrary_Rn_occurrence_pullback_component_ids_materialized"
        ] == 0
        and correction["arbitrary_Rn_connected_ranks_materialized"] == 0,
        "Round69 no arbitrary-Rn occurrence pullback components",
    )

    fail_closed = r128["B_Round67_occurrence_owner_crosswalk_fail_closed"]
    require(
        fail_closed["required_recordwise_composite_key_fields"]
        == REQUIRED_FIELDS,
        "Round128 twelve-field order",
    )
    require(
        fail_closed["round67_materialized_recordwise_identifier_count"] == 0,
        "Round128 Round67 record count",
    )
    require(
        fail_closed["round67_to_round72_component_crosswalk_row_count"] == 0,
        "Round128 crosswalk count",
    )
    require(
        fail_closed["direct_source_point_equality_pair_audit_count"] == 11264
        and fail_closed["direct_source_point_equality_intersection_count"] == 0,
        "Round128 direct equality obstruction",
    )
    require(v128["replay_audit"]["Round67_joined_fields"] == "0/12", "verified 0/12")

    atlas = r72["complete_base_fibre_terminal_preimage_family_atlas"]
    components = r72["complete_positive_component_registry"]
    numeric = r72["numeric_local_field_registry"]
    require(
        atlas["candidate_family_count"] == 1152
        and atlas["positive_family_count"] == 32
        and atlas["certified_empty_family_count"] == 1120
        and atlas["unresolved_family_count"] == 0,
        "Round72 exhaustive base-R1 census",
    )
    require(
        components["component_count"] == 32
        and components["connected_rank"] == 0
        and components["one_sided_trace_count"] == 64,
        "Round72 component census",
    )
    require(
        numeric["F10_numeric_rows"] == 32
        and numeric["F13_numeric_rows"] == 32
        and numeric["F16_numeric_rows"] == 32,
        "Round72 numeric field census",
    )
    require(
        r72_proof["component_count"] == 32
        and len(r72_proof["rows"]) == 32,
        "Round72 proof rows",
    )
    require(
        r72_proof["F10_integer_sum"] == 480,
        "Round72 F10 sum",
    )
    require(
        len(r71_witnesses["rows"]) == 32,
        "Round71 witness row count",
    )
    r71_components = r71[
        "base_fibre_nonempty_face_witness_registry"
    ]["component_rows"]
    require(len(r71_components) == 32, "Round71 component row count")

    incidence = r128["A_base_R1_component_to_global_word_incidence"]
    incidence_rows = incidence["component_incidence_rows"]
    require(
        incidence["component_incidence_row_count"] == 32
        and len(incidence_rows) == 32,
        "Round128 component incidence count",
    )
    require(
        incidence["directed_source_destination_word_edge_count"] == 16
        and incidence["distinct_path_cell_count"] == 16,
        "Round128 path/word census",
    )

    r71_by_hash = {digest(row): row for row in r71_components}
    r72_by_hash = {digest(row): row for row in r72_proof["rows"]}
    require(len(r71_by_hash) == len(r72_by_hash) == 32, "unique source rows")

    unmatched_rows: list[dict[str, Any]] = []
    component_ids: set[str] = set()
    for source in sorted(incidence_rows, key=lambda row: row["component_id"]):
        require(
            source["source_round71_component_row_sha256"] in r71_by_hash,
            "Round128 to Round71 row hash",
        )
        require(
            source["source_round72_field_row_sha256"] in r72_by_hash,
            "Round128 to Round72 row hash",
        )
        row71 = r71_by_hash[source["source_round71_component_row_sha256"]]
        row72 = r72_by_hash[source["source_round72_field_row_sha256"]]
        for key in (
            "component_id",
            "candidate_family_id",
            "source_core_id",
            "destination_core_id",
            "path_cell_id",
        ):
            require(source[key] == row71[key], f"Round71 identity: {key}")
        for key in ("component_id", "candidate_family_id"):
            require(source[key] == row72[key], f"Round72 identity: {key}")
        require(
            source["numeric_local_fields"]["F10_integer_upper"]
            == row72["F10_integer_upper"],
            "Round72 F10 attachment",
        )
        require(
            source["numeric_local_fields"]["F13_current_variation_strict_upper"]
            == row72["F13_current_variation_strict_upper"],
            "Round72 F13 attachment",
        )
        require(
            source["numeric_local_fields"]["F16_Piola_flux_cost_strict_upper"]
            == row72["F16_Piola_flux_cost_strict_upper"],
            "Round72 F16 attachment",
        )
        require(source["trace_rows"] == row71["trace_rows"], "Round71 traces")
        require(source["base_parameter"] == "s=0", "base parameter s=0")
        require(source["time_j"] == row71["time_j"] == 1, "time j=1")
        require(source["connected_rank"] == row71["connected_rank"] == 0, "rank zero")
        require(
            source["source_and_destination_roof_level_count"] == 1
            and source["source_and_destination_roof_level_j"] == 0,
            "base-R1 roof level",
        )
        require(source["component_id"] not in component_ids, "unique component ID")
        component_ids.add(source["component_id"])

        unmatched_id = (
            "round131-unmatched-round72-component:"
            + digest(
                [
                    "round131-unmatched-round72-component-v1",
                    source["component_id"],
                    source["path_cell_id"],
                    source["source_official_word_key_id"],
                    source["destination_official_word_key_id"],
                ]
            )
        )
        unmatched_rows.append(
            with_hash(
                {
                    "unmatched_row_id": unmatched_id,
                    "join_status":
                        "UNMATCHED__ROUND67_RECORD_AND_EXACT_COORDINATE_MAP_ABSENT",
                    "round67_occurrence_record_id": None,
                    "typed_incidence_id": None,
                    "all_twelve_round67_recordwise_values": {
                        field: None for field in REQUIRED_FIELDS
                    },
                    "missing_round67_required_fields": list(REQUIRED_FIELDS),
                    "missing_round67_required_field_count": 12,
                    "component_id": source["component_id"],
                    "candidate_family_id": source["candidate_family_id"],
                    "Round71_Round72_physical_carrier_type":
                        "regular_branch_pullback_of_stationary_destination_core_face",
                    "eligible_as_Round67_occurrence_pullback_face": False,
                    "component_coordinate_germ":
                        source["component_coordinate_germ"],
                    "component_face_side": source["component_face_side"],
                    "base_parameter": source["base_parameter"],
                    "connected_rank": source["connected_rank"],
                    "time_j": source["time_j"],
                    "return_depth": source["time_j"],
                    "roof_level_j":
                        source["source_and_destination_roof_level_j"],
                    "source_core_id": source["source_core_id"],
                    "destination_core_id": source["destination_core_id"],
                    "destination_face_id": source["destination_face_id"],
                    "path_cell_id": source["path_cell_id"],
                    "source_official_word_key_id":
                        source["source_official_word_key_id"],
                    "destination_official_word_key_id":
                        source["destination_official_word_key_id"],
                    "source_official_word_row":
                        source["source_official_word_row"],
                    "destination_official_word_row":
                        source["destination_official_word_row"],
                    "trace_rows": source["trace_rows"],
                    "numeric_local_fields": source["numeric_local_fields"],
                    "source_round71_component_row_sha256":
                        source["source_round71_component_row_sha256"],
                    "source_round72_field_row_sha256":
                        source["source_round72_field_row_sha256"],
                    "source_round128_incidence_row_id":
                        source["incidence_row_id"],
                    "source_round128_incidence_row_sha256":
                        source["row_sha256"],
                    "candidate_family_id_is_not_Round67_primitive_key": True,
                    "source_or_destination_core_id_is_not_Round67_owner_key":
                        True,
                    "coordinate_face_side_is_not_Round67_plaque_side": True,
                    "word_membership_is_not_same_physical_root": True,
                    "endpoint_root_to_s_t_p_coordinate_map_id": None,
                    "Round72_F10_F13_F16_attached_to_Round67_root": False,
                }
            )
        )
    require(len(unmatched_rows) == len(component_ids) == 32, "32 unmatched rows")

    field_rows = [
        with_hash(
            {
                "field_index": index,
                "required_field": field,
                "Round67_declared_token_or_semantic_source":
                    ROUND67_DECLARED_TOKEN_BY_REQUIRED_FIELD[field],
                "Round67_recordwise_value_materialized": False,
                "Round71_Round72_Round128_evidence_tokens":
                    ROUND72_EVIDENCE_BY_REQUIRED_FIELD[field],
                "same_semantic_key_join_proven": False,
                "field_status": "UNMATCHED",
            }
        )
        for index, field in enumerate(REQUIRED_FIELDS, start=1)
    ]

    root_rows = [
        with_hash(
            {
                "root_schema_row_id":
                    "round131-round67-unmaterialized-root-schema:"
                    + digest(
                        [
                            "round131-round67-unmaterialized-root-schema-v1",
                            fixed["root"],
                            fixed["base_law"],
                            fixed["retained_keys"],
                        ]
                    ),
                "Round67_root": fixed["root"],
                "Round67_root_measure": fixed["root_measure"],
                "Round67_base_law": fixed["base_law"],
                "Round67_owner_law": fixed["owner_law"],
                "Round67_retained_key_schema": fixed["retained_keys"],
                "Round67_materialized_recordwise_identifier_count": 0,
                "Round67_materialized_twelve_field_record_count": 0,
                "status":
                    "ABSTRACT_PHYSICAL_SUBROOT_CERTIFIED__RECORDWISE_ROWS_ABSENT",
            }
        )
    ]

    carrier_type_rows = [
        with_hash(
            {
                "carrier_type_row_id": "ROUND67_UNDERLYING_OCCURRENCE_SEEDS",
                "carrier_type": "moving_first_event_grazing_occurrence_face",
                "materialized_seed_count_in_Round28": 64,
                "materialized_oriented_hit_miss_trace_seed_count_in_Round28":
                    128,
                "internal_R1_boundary_face": False,
                "R1_inner_typed_incidence_status": "CERTIFIED_EMPTY",
                "arbitrary_Rn_occurrence_pullback_component_count": 0,
                "role":
                    "source carrier seeds for a future occurrence-pullback family",
            }
        ),
        with_hash(
            {
                "carrier_type_row_id":
                    "ROUND71_ROUND72_TERMINAL_CORE_PREIMAGE_COMPONENTS",
                "carrier_type":
                    "regular_branch_pullback_of_stationary_destination_core_face",
                "materialized_component_count": 32,
                "materialized_one_sided_trace_count": 64,
                "R1_path_cell_count": 16,
                "eligible_as_Round67_occurrence_pullback_face": False,
                "role":
                    "numeric terminal-preimage F10/F13/F16 components only",
            }
        ),
    ]

    obstruction_rows = [
        with_hash(
            {
                "obstruction_id": "ROUND67_RECORDS_NOT_MATERIALIZED",
                "evidence": {
                    "Round67_materialized_recordwise_identifier_count": 0,
                    "required_field_count": 12,
                    "joined_field_count": 0,
                },
                "blocks": "any typed-incidence match row",
            }
        ),
        with_hash(
            {
                "obstruction_id": "DIRECT_SOURCE_POINT_EQUALITY_IS_EMPTY",
                "evidence": {
                    "pair_audit_count": 11264,
                    "intersection_count": 0,
                    "occurrence_carrier_type":
                        obstruction["raw_occurrence_carrier_type"],
                    "return_carrier_type":
                        obstruction["return_carrier_type"],
                },
                "blocks": "recordwise point-equality join",
            }
        ),
        with_hash(
            {
                "obstruction_id": "TYPED_INCIDENCE_NOT_POINT_EQUALITY",
                "evidence": {
                    "node_sorts": correction["node_sorts"],
                    "edge_semantics": correction["edge_semantics"],
                },
                "blocks": "reusing equality as incidence",
            }
        ),
        with_hash(
            {
                "obstruction_id":
                    "R1_MOVING_OCCURRENCE_TYPED_INCIDENCE_CERTIFIED_EMPTY",
                "evidence": {
                    "Round28_occurrence_seed_count": 64,
                    "Round28_occurrence_carrier_type":
                        "moving_first_event_grazing_occurrence_face",
                    "Round69_R1_inner_moving_occurrence_incidence":
                        "CERTIFIED_EMPTY",
                    "Round71_Round72_terminal_component_count": 32,
                    "terminal_component_carrier_type":
                        "regular_branch_pullback_of_stationary_destination_core_face",
                    "carrier_type_compatible_direct_match_row_count": 0,
                },
                "blocks":
                    "using a Round71/72 terminal-preimage component as a Round67 occurrence-pullback face",
            }
        ),
        with_hash(
            {
                "obstruction_id": "EXACT_COORDINATE_MAP_ABSENT",
                "evidence": {
                    "required_domain": "Round67 endpoint/root coordinates",
                    "required_codomain": "Round72 component germ (s,t,p)",
                    "materialized_map_count": 0,
                },
                "blocks": "Gamma subset Omega_1 x physical_face x path_cell",
            }
        ),
        with_hash(
            {
                "obstruction_id": "SURROGATE_IDENTIFIERS_FORBIDDEN",
                "evidence": {
                    "candidate_family_id_is_not_primitive_key": True,
                    "core_id_is_not_owner_key": True,
                    "coordinate_face_side_is_not_plaque_side": True,
                    "equal_time_rank_or_word_is_not_same_root": True,
                },
                "blocks": "field-name or identifier-shape join",
            }
        ),
    ]

    typed_incidence_match_rows: list[dict[str, Any]] = []
    all_rows = (
        root_rows
        + field_rows
        + carrier_type_rows
        + unmatched_rows
        + obstruction_rows
    )
    require(len(all_rows) == 53, "finite Round131 row census")
    require(
        len({row["row_sha256"] for row in all_rows}) == len(all_rows),
        "unique row hashes",
    )

    return {
        "status":
            "CERTIFIED_FAIL_CLOSED_TYPED_INCIDENCE_CROSSWALK_0_MATCHES_32_UNMATCHED",
        "provenance": {
            "producer_sha256": sha256_path(PRODUCER),
            "input_byte_pins": {
                name: BYTE_PINS[name] for name in sorted(BYTE_PINS)
            },
            "input_canonical_document_pins": {
                name: {
                    "scope": CANONICAL_DOCUMENT_PINS[name][0],
                    "sha256": CANONICAL_DOCUMENT_PINS[name][1],
                }
                for name in sorted(CANONICAL_DOCUMENT_PINS)
            },
            "input_schema_pins": {
                name: SCHEMA_PINS[name] for name in sorted(SCHEMA_PINS)
            },
            "Round128_independent_verification_status": v128["status"],
            "append_only": True,
        },
        "source_census": {
            "Round67_fixed_j_physical_subroot_status": fixed["status"],
            "Round67_materialized_recordwise_identifier_count": 0,
            "Round67_materialized_twelve_field_record_count": 0,
            "Round28_moving_first_event_grazing_occurrence_seed_count": 64,
            "Round28_oriented_hit_miss_occurrence_trace_seed_count": 128,
            "Round71_nonempty_component_count": 32,
            "Round72_candidate_family_count": 1152,
            "Round72_certified_empty_family_count": 1120,
            "Round72_positive_component_count": 32,
            "Round72_one_sided_trace_count": 64,
            "Round72_F10_F13_F16_numeric_row_count_each": 32,
            "Round128_path_cell_count": 16,
            "Round128_source_official_word_count": 16,
            "direct_source_point_equality_pair_audit_count": 11264,
            "direct_source_point_equality_intersection_count": 0,
            "R1_inner_moving_occurrence_typed_incidence_status":
                "CERTIFIED_EMPTY",
            "carrier_type_compatible_direct_match_row_count": 0,
        },
        "round67_unmaterialized_root_schema_rows": root_rows,
        "round67_unmaterialized_root_schema_rows_sha256": digest(root_rows),
        "required_field_status_rows": field_rows,
        "required_field_status_rows_sha256": digest(field_rows),
        "carrier_type_status_rows": carrier_type_rows,
        "carrier_type_status_rows_sha256": digest(carrier_type_rows),
        "typed_incidence_match_rows": typed_incidence_match_rows,
        "typed_incidence_match_rows_sha256": digest(typed_incidence_match_rows),
        "unmatched_round72_component_rows": unmatched_rows,
        "unmatched_round72_component_rows_sha256": digest(unmatched_rows),
        "obstruction_witness_rows": obstruction_rows,
        "obstruction_witness_rows_sha256": digest(obstruction_rows),
        "crosswalk_census": {
            "required_recordwise_field_count": 12,
            "required_recordwise_fields": list(REQUIRED_FIELDS),
            "currently_joined_required_fields": "0/12",
            "typed_incidence_match_row_count": 0,
            "carrier_type_status_row_count": 2,
            "carrier_type_compatible_direct_match_row_count": 0,
            "unmatched_round72_component_row_count": 32,
            "unmatched_round67_record_row_count": None,
            "unmatched_round67_record_row_count_is_null_because_records_are_not_materialized":
                True,
            "obstruction_witness_row_count": 6,
            "finite_Round131_row_count": 53,
        },
        "minimum_nonempty_typed_incidence_row_contract": {
            "graph_symbol": "Gamma",
            "ambient_product":
                "Omega_j x occurrence_pullback_face x R_n_path_cell",
            "required_face_carrier_type":
                "pullback of a Round28 moving_first_event_grazing_occurrence_face seed",
            "R1_inner_occurrence_pullback_target_certified_empty": True,
            "first_return_depth_not_ruled_out_by_the_R1_empty_theorem":
                "n>=2",
            "Round71_Round72_terminal_preimage_components_are_direct_match_candidates":
                False,
            "row_identity_payload": [
                "round67_occurrence_record_id",
                "occurrence_pullback_component_id",
                "path_cell_id",
                "exact_coordinate_map_id",
            ],
            "required_Round67_recordwise_fields": list(REQUIRED_FIELDS),
            "required_occurrence_pullback_path_word_fields": [
                "occurrence_face_seed_id",
                "occurrence_pullback_family_id",
                "occurrence_pullback_component_id",
                "base_parameter",
                "source_core_id",
                "destination_core_id",
                "path_cell_id",
                "source_official_word_key_id",
                "destination_official_word_key_id",
                "inside_trace_id",
                "outside_trace_id",
                "time_j",
                "return_depth",
                "connected_rank",
            ],
            "required_exact_coordinate_map_fields": [
                "coordinate_map_id",
                "domain_chart_and_restriction",
                "endpoint_coordinate_formula",
                "root_coordinate_formula",
                "s_t_p_formula",
                "inverse_or_fibre_formula",
                "Jacobian_or_transversality_nonzero_proof",
                "orientation_and_side_reconciliation",
                "Borel_graph_proof",
            ],
            "required_nonempty_evidence": [
                "one exact matched row",
                "physical incidence proof not point equality",
                "nonempty occurrence-pullback component germ or positive conditional mass witness",
            ],
            "fail_closed_rule":
                "if any required value or exact coordinate map is absent, emit an unmatched row and no match row",
            "future_match_row_count_required_for_nonempty_crosswalk": 1,
            "separate_later_quotient_needed_to_attach_Round72_numeric_fields":
                True,
        },
        "same_root_anti_splice_contract": {
            "candidate_family_id_may_replace_primitive_key": False,
            "source_or_destination_core_id_may_replace_owner_key": False,
            "component_coordinate_face_side_may_replace_plaque_side": False,
            "official_word_membership_may_replace_same_physical_root": False,
            "time_j_and_connected_rank_may_replace_twelve_field_key": False,
            "direct_source_point_equality_may_replace_typed_incidence": False,
            "Round72_component_germ_may_replace_exact_endpoint_root_map": False,
            "Round71_Round72_terminal_preimage_may_replace_occurrence_pullback_face":
                False,
            "Round72_numeric_fields_attached_to_Round67_owner_root": False,
        },
        "field_impact": {
            "F10": (
                "32 nonempty base-R1 numeric rows exist but remain Round72 "
                "component-local and are not attached to the Round67 owner root"
            ),
            "F14": "NOT_INSTALLED_ON_A_JOINED_NONEMPTY_PHYSICAL_ROOT",
            "F15": (
                "NOT_INSTALLED_ON_A_JOINED_NONEMPTY_PHYSICAL_ROOT; no positive "
                "pre-regularization or all-time cemetery payment"
            ),
            "F17": "NOT_INSTALLED_ON_A_JOINED_NONEMPTY_PHYSICAL_ROOT",
            "F18": "NO_COMMON_PHYSICAL_BLOCK_EXISTS",
        },
        "global_safety": {
            "Round67_to_Round72_crosswalk_row_count": 0,
            "global_complete_18_field_block_count": 0,
            "complete_18_field_block_count": 0,
            "gate5_block_count": 0,
            "gate5_global_maturity": "10/18",
            "gate5_status": "NOT_CERTIFIED",
            "CM2": "NO-GO_FOR_CLAIM",
            "arbitrary_return_depth_certified": False,
            "all_time_positive_potential_certified": False,
        },
        "strict_nonclaims": [
            "no Round67 recordwise occurrence or owner row is materialized",
            "no Round67 row is joined to a Round71 or Round72 component",
            "the 32 unmatched rows are not match rows or global coverage rows",
            "Round71/72 terminal-core preimages are not Round67 occurrence-pullback faces",
            "strict inner R1 moving-occurrence typed incidence is certified empty",
            "terminal-preimage face incidence is not interior point equality",
            "equal time, connected rank, word or similarly shaped IDs do not prove a same-root join",
            "Round72 F10/F13/F16 rows are not promoted to the Round67 owner root",
            "no F14/F15/F17/F18 common nonempty physical block is installed",
            "no arbitrary-depth, all-time positive-potential, Gate5 or CM2 claim",
        ],
    }


def safe_output_path(path: Path) -> Path:
    expanded = path.expanduser()
    protected = {PRODUCER, *(item.resolve() for item in INPUTS)}
    require(not expanded.is_symlink(), "output path must not be a symlink")
    if expanded.exists():
        metadata = expanded.lstat()
        require(
            stat.S_ISREG(metadata.st_mode),
            "existing output must be a regular file",
        )
        require(
            metadata.st_nlink == 1,
            "existing output must not have multiple hardlinks",
        )
        for protected_path in protected:
            try:
                require(
                    not os.path.samefile(expanded, protected_path),
                    "output hardlinks a protected input",
                )
            except FileNotFoundError:
                pass
    resolved = expanded.resolve()
    require(resolved not in protected, "output must not overwrite an input")
    require(resolved.parent.is_dir(), "output parent directory")
    return resolved


def write_certificate(path: Path, result: dict[str, Any]) -> None:
    document = {
        "schema": SCHEMA,
        "result": result,
        "result_sha256": digest(result),
    }
    text = json.dumps(
        document,
        sort_keys=True,
        indent=2,
        ensure_ascii=False,
        allow_nan=False,
    ) + "\n"
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=f".{path.name}.tmp-",
        dir=path.parent,
        text=True,
    )
    temporary = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as stream:
            stream.write(text)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
    except BaseException:
        try:
            temporary.unlink()
        except FileNotFoundError:
            pass
        raise


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=OUTPUT)
    args = parser.parse_args()
    output = safe_output_path(args.output)
    result = build()
    write_certificate(output, result)
    print(
        canonical(
            {
                "output": str(output),
                "result_sha256": digest(result),
                "status": result["status"],
            }
        )
    )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except VerificationError as exc:
        print(f"VerificationError: {exc}", file=os.sys.stderr)
        raise SystemExit(1)
