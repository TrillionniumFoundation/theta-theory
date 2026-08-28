#!/usr/bin/env python3
"""Round132: materialize the 64 Round28 occurrence records and 128 traces.

Round28 deterministically constructed, but did not emit, all 64 genuine
moving-first-event grazing occurrence-face rows.  This producer independently
rebuilds them from the pinned maximal-row/current, recovery-carrier and
all-scale-germ sources without importing the Round28 producer.  It emits all
64 canonical occurrence source records and all 128 oriented hit/miss traces.

Nine of the Round68 twelve source-side key fields can now be represented
canonically: restriction, insertion time, collision index, event signature,
primitive key, oriented side label, occurrence word cell, endpoint coordinate
record and root coordinate record.  Return component, owner key and
occurrence-pullback connected rank remain absent.  More importantly, no owner
map q_j and no exact endpoint/root-to-(s,t,p) typed-incidence map is installed.
Consequently no Round67 owned record, no Round67-to-path match and no Gate5
credit is promoted.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import stat
import tempfile
from fractions import Fraction as Q
from pathlib import Path
from typing import Any

from flint import ctx

import cm2_gate34_occurrence_boundary_recovery_carrier_cert as recovery_cert
import cm2_gate34_parameter_dq_all_scale_shell_cert as parameter_cert
import cm2_gate3_depth_one_fixed_gauge_dq_cert as dq_cert


HERE = Path(__file__).resolve().parent
PRODUCER = Path(__file__).resolve()
OUTPUT = (
    HERE
    / "cm2-round132-round28-occurrence-record-materialization-2026-07-24.json"
)
SCHEMA = "cm2.round132.round28-occurrence-record-materialization.v1"
PRECISION_BITS = 512

ROUND28_PRODUCER = (
    HERE / "cm2_gate5_round28_limiting_physical_face_atlas_frontier_cert.py"
)
ROUND28_MANIFEST = (
    HERE
    / "cm2-gate5-round28-limiting-physical-face-atlas-frontier-manifest-2026-07-18.json"
)
DQ_PRODUCER = HERE / "cm2_gate3_depth_one_fixed_gauge_dq_cert.py"
DQ_MANIFEST = (
    HERE / "cm2-gate3-depth-one-fixed-gauge-dq-manifest-2026-07-15.json"
)
RECOVERY_PRODUCER = (
    HERE / "cm2_gate34_occurrence_boundary_recovery_carrier_cert.py"
)
RECOVERY_MANIFEST = (
    HERE
    / "cm2-gate34-occurrence-boundary-recovery-carrier-manifest-2026-07-17.json"
)
PARAMETER_PRODUCER = (
    HERE / "cm2_gate34_parameter_dq_all_scale_shell_cert.py"
)
PARAMETER_MANIFEST = (
    HERE
    / "cm2-gate34-parameter-dq-all-scale-shell-manifest-2026-07-17.json"
)
ROUND67_PRODUCER = (
    HERE
    / "cm2_round67_fixed_j_occurrence_owner_root_time_potential_frontier_cert.py"
)
ROUND67_MANIFEST = (
    HERE
    / "cm2-round67-fixed-j-occurrence-owner-root-time-potential-frontier-manifest-2026-07-21.json"
)
ROUND131_PRODUCER = (
    HERE / "cm2_round131_round67_r1_typed_incidence_crosswalk.py"
)
ROUND131_CERTIFICATE = (
    HERE / "cm2-round131-round67-r1-typed-incidence-crosswalk-2026-07-24.json"
)

INPUTS = (
    ROUND28_PRODUCER,
    ROUND28_MANIFEST,
    DQ_PRODUCER,
    DQ_MANIFEST,
    RECOVERY_PRODUCER,
    RECOVERY_MANIFEST,
    PARAMETER_PRODUCER,
    PARAMETER_MANIFEST,
    ROUND67_PRODUCER,
    ROUND67_MANIFEST,
    ROUND131_PRODUCER,
    ROUND131_CERTIFICATE,
)

BYTE_PINS = {
    ROUND28_PRODUCER.name:
        "b0dda23ec7e8c9dbe82aff861be6b4e1d38ecf281a82165949537b923150ba27",
    ROUND28_MANIFEST.name:
        "ad385983a4152da3bc1d9c58a5a2fba1abb928466ecf9a9f61260b612bddf140",
    DQ_PRODUCER.name:
        "8ce2490ee2b2bdfc251ac1892cb260e40f3eb5d87ce7f232c2076a10c4a9c066",
    DQ_MANIFEST.name:
        "284b25ac30dd86a01bd0faaa7c0a97ee47839670e3cde4309936235badf5fd52",
    RECOVERY_PRODUCER.name:
        "9e69879f921681da4a8eeda9a2af8755c3713151128027784e72cd12896a053a",
    RECOVERY_MANIFEST.name:
        "dd16bd1e3407a6f886ddbf1270ca7ff7289a7d6792e81235f69014cafaf49cb5",
    PARAMETER_PRODUCER.name:
        "ea5b6b7fa265990b1eaa1c106e2c0f82f024b58951bbe65ff55757cbc23df458",
    PARAMETER_MANIFEST.name:
        "2f374298785c74525e0bbb66b39e30be503ad9af05a913fa3175063196d883a8",
    ROUND67_PRODUCER.name:
        "cfb501aff4f321742e3fead9895c596e9105b2a89d064d917646b70c6f91ee8f",
    ROUND67_MANIFEST.name:
        "97cb410b9e960d8331a37ef9203b040c9b1d86c3ed3d1ba6ba66a28c4e4ff400",
    ROUND131_PRODUCER.name:
        "8e7b2bae965be128a288ae38768bf746f5c33c0744449f8edea48014bd22d611",
    ROUND131_CERTIFICATE.name:
        "a8e4b9dabb30396469f28d4df252c9f5de1d9d1620c0a18d252ef23a12f1f3d6",
}

SCHEMA_PINS = {
    ROUND28_MANIFEST.name:
        "cm2.gate5.round28-limiting-physical-face-atlas-frontier.manifest.v3",
    DQ_MANIFEST.name:
        "cm2.gate3.depth-one-fixed-gauge-dq.manifest.v1",
    RECOVERY_MANIFEST.name:
        "cm2.gate34.occurrence-boundary-recovery-carrier.manifest.v1",
    PARAMETER_MANIFEST.name:
        "cm2.gate34.parameter-dq-all-scale-shell.manifest.v1",
    ROUND67_MANIFEST.name:
        "cm2.round67.fixed-j-occurrence-owner-root-time-potential.v1.manifest.v1",
    ROUND131_CERTIFICATE.name:
        "cm2.round131.round67-r1-typed-incidence-crosswalk.v1",
}

RESULT_PINS = {
    ROUND28_MANIFEST.name:
        "282d73b9146a38ff41f78ab6d0fd619c1b955eda32ed3dd5cdae2fd170b340b6",
    DQ_MANIFEST.name:
        "3b05206952610710ffc037b483fd81c77589c08903c722b4e7b56fe2d964c276",
    RECOVERY_MANIFEST.name:
        "a07d8a96949ed18a78b0753546892ddc043b47191bfc75024874e6394ef2f741",
    PARAMETER_MANIFEST.name:
        "8eb47e4bbebc6739b4d7a25a923495b672edffd1bf9456ba37c560174e8a5012",
    ROUND67_MANIFEST.name:
        "c1fd3e486d671b83c6ae6a0c6da8c4d50bd2796842cfe1c8d8d5985001e5a57f",
    ROUND131_CERTIFICATE.name:
        "0fd7f419d5a0afa3fbc20db3757803ee5c2982b4428ba52a97798a6fcc28a0ab",
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

SOURCE_EXACT_FIELDS = [
    "restriction_id",
    "insertion_time",
    "collision_index",
    "event_signature",
    "primitive_key",
    "plaque_side",
    "word_cell",
    "endpoint_coordinate",
    "root_coordinate",
]

SOURCE_MISSING_FIELDS = [
    "return_component",
    "owner_key",
    "rank_zero_component",
]


class VerificationError(RuntimeError):
    """Fail-closed input, reconstruction, semantic or output error."""


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


def qstr(value: Q) -> str:
    return str(value.numerator) if value.denominator == 1 else (
        f"{value.numerator}/{value.denominator}"
    )


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
    except json.JSONDecodeError as exc:
        raise VerificationError(f"strict JSON: {path.name}") from exc
    require(isinstance(value, dict), f"top-level object: {path.name}")
    return value


def with_hash(row: dict[str, Any]) -> dict[str, Any]:
    require("row_sha256" not in row, "row already hashed")
    return {**row, "row_sha256": digest(row)}


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
        require(
            document.get("schema") == SCHEMA_PINS[path.name],
            f"schema pin: {path.name}",
        )
        require(
            isinstance(document.get("result"), dict),
            f"result object: {path.name}",
        )
        require(
            digest(document["result"]) == RESULT_PINS[path.name],
            f"result pin: {path.name}",
        )
    r131 = documents[ROUND131_CERTIFICATE.name]
    require(
        r131.get("result_sha256") == RESULT_PINS[ROUND131_CERTIFICATE.name],
        "Round131 stored result digest",
    )
    require(
        r131["result"]["crosswalk_census"]["typed_incidence_match_row_count"]
        == 0,
        "Round131 no match rows",
    )
    require(
        r131["result"]["source_census"][
            "R1_inner_moving_occurrence_typed_incidence_status"
        ] == "CERTIFIED_EMPTY",
        "Round131 R1 occurrence incidence empty",
    )
    require(
        r131["result"]["global_safety"]["gate5_global_maturity"] == "10/18"
        and r131["result"]["global_safety"]["CM2"] == "NO-GO_FOR_CLAIM",
        "Round131 safety",
    )
    return documents


def reconstruct_round28_occurrences(
    round28: dict[str, Any],
) -> tuple[
    list[dict[str, Any]],
    list[dict[str, Any]],
    list[dict[str, Any]],
    dict[str, Any],
]:
    ctx.prec = PRECISION_BITS
    raw_rows, raw_registry = dq_cert.load_rows()
    typed_rows, typed_registry = dq_cert.corrected_current_rows(raw_rows)
    carrier_rows, carrier_registry = recovery_cert.build_carrier_registry()
    germ_rows = [parameter_cert.certify_germ(row) for row in raw_rows]

    raw = {row["occurrence_id"]: row for row in raw_rows}
    typed = {row["occurrence_id"]: row for row in typed_rows}
    carriers = {row["occurrence_id"]: row for row in carrier_rows}
    germs = {row["occurrence_id"]: row for row in germ_rows}
    require(
        len(raw) == len(typed) == len(carriers) == len(germs) == 64,
        "64-way occurrence reconstruction",
    )
    require(
        set(raw) == set(typed) == set(carriers) == set(germs),
        "occurrence ID join",
    )
    require(
        typed_registry["maximal_row_current_count"] == 64
        and typed_registry[
            "strict_hit_and_miss_trace_attached_to_every_row"
        ] is True,
        "typed-current registry",
    )
    require(
        carrier_registry["oriented_hit_miss_trace_seed_count"] == 128,
        "carrier trace registry",
    )

    round28_face_rows: list[dict[str, Any]] = []
    face_rows: list[dict[str, Any]] = []
    trace_rows: list[dict[str, Any]] = []
    face_ids: set[str] = set()
    trace_ids: set[str] = set()
    germ_ids: set[str] = set()
    restriction_ids: set[str] = set()
    event_ids: set[str] = set()
    word_cell_ids: set[str] = set()

    for occurrence_id in sorted(raw):
        source = raw[occurrence_id]
        current = typed[occurrence_id]
        carrier = carriers[occurrence_id]
        germ = germs[occurrence_id]
        require(
            current["global_physical_label"]
            == carrier["global_physical_label"]
            == source["global_physical_label"],
            "global physical label join",
        )
        require(
            current["base"] == source["base"],
            "maximal occurrence base join",
        )
        require(
            current["left_boundary"] == source["left_boundary"]
            and current["right_boundary"] == source["right_boundary"],
            "boundary descriptor join",
        )
        require(
            germ["face_time_collision_offset"] == 1,
            "occurrence insertion time one",
        )
        require(
            germ["hit_parameter_sign"]
            == current["signed_current"]["polarity"]
            and germ["miss_parameter_sign"]
            == -current["signed_current"]["polarity"],
            "oriented parameter signs",
        )
        require(
            carrier["shared_pulled_back_event_base_restriction"] is True,
            "shared base restriction",
        )

        face_payload = {
            "occurrence_id": occurrence_id,
            "global_physical_label": source["global_physical_label"],
            "source": source["source"],
            "tangent_target": source["target"],
            "epsilon": source["epsilon"],
            "miss_target": source["miss_target"],
        }
        face_id = (
            "physical-moving-occurrence-face-seed:" + digest(face_payload)
        )
        require(face_id not in face_ids, "unique occurrence face ID")
        face_ids.add(face_id)
        germ_ids.add(germ["germ_id"])
        hit_trace_id = carrier["hit_trace_seed_id"]
        miss_trace_id = carrier["miss_trace_seed_id"]
        require(
            hit_trace_id not in trace_ids and miss_trace_id not in trace_ids,
            "unique occurrence trace IDs",
        )
        trace_ids.update((hit_trace_id, miss_trace_id))

        round28_face = {
            "immutable_global_occurrence_face_seed_id": face_id,
            **face_payload,
            "physical_carrier_type":
                "moving_first_event_grazing_occurrence_face",
            "immutable_hit_trace_seed_id": hit_trace_id,
            "immutable_miss_trace_seed_id": miss_trace_id,
            "common_boundary_recovery_carrier_id":
                carrier["common_boundary_recovery_carrier_id"],
            "selected_all_scale_parameter_germ_id": germ["germ_id"],
            "selected_all_scale_germ_exhausts_whole_maximal_row": False,
            "hit_parameter_sign": germ["hit_parameter_sign"],
            "miss_parameter_sign": germ["miss_parameter_sign"],
            "positive_coarea_law": current["positive_coarea_law"],
            "signed_parameter_DQ_current": current["signed_current"],
            "corrected_unnormalized_density_upper_bound_wrt_dtheta": "18/5",
            "artificial_dyadic_face": False,
            "core_preimage_face": False,
        }
        round28_face_rows.append(round28_face)

        restriction_id = (
            "round132-occurrence-restriction:"
            + digest(
                [
                    "round132-occurrence-restriction-v1",
                    occurrence_id,
                    carrier["base_signature"],
                    source["base"],
                    source["left_boundary"],
                    source["right_boundary"],
                ]
            )
        )
        event_signature_id = (
            "round132-occurrence-event-signature:"
            + digest(
                [
                    "round132-occurrence-event-signature-v1",
                    face_id,
                    source["global_physical_label"],
                    source["left_boundary"],
                    source["right_boundary"],
                    source["parameter_coarea_polarity"],
                ]
            )
        )
        occurrence_word_cell_id = (
            "round132-occurrence-word-cell:"
            + digest(
                [
                    "round132-occurrence-word-cell-v1",
                    source["global_physical_label"],
                ]
            )
        )
        require(restriction_id not in restriction_ids, "unique restriction")
        require(event_signature_id not in event_ids, "unique event signature")
        restriction_ids.add(restriction_id)
        event_ids.add(event_signature_id)
        word_cell_ids.add(occurrence_word_cell_id)

        witness_z = Q(source["witness"]["z"])
        half_width = Q(germ["base_half_width"])
        endpoint_coordinate_record = {
            "coordinate_record_version":
                "round132-occurrence-endpoint-coordinate-v1",
            "source_event_chart": germ["source_event_chart"],
            "exact_rational_witness_z": qstr(witness_z),
            "left_boundary_descriptor": source["left_boundary"],
            "right_boundary_descriptor": source["right_boundary"],
            "coordinate_status":
                "EXACT_LOCAL_MAXIMAL_ROW_DESCRIPTOR_AND_RATIONAL_WITNESS",
        }
        root_coordinate_record = {
            "coordinate_record_version":
                "round132-occurrence-root-coordinate-v1",
            "source_event_chart": germ["source_event_chart"],
            "exact_z_interval": [
                qstr(witness_z - half_width),
                qstr(witness_z + half_width),
            ],
            "exact_local_parameter_s_interval": [
                qstr(-half_width),
                qstr(half_width),
            ],
            "maximal_parameter_s_interval": source["base"]["parameter_s"],
            "base_half_width_power": germ["base_half_width_power"],
            "base_event_coordinate_area": germ["base_event_coordinate_area"],
            "parameter_magnitude_interval":
                germ["parameter_magnitude_interval"],
            "germ_geometry_sha256": germ["germ_geometry_sha256"],
            "coordinate_status":
                "EXACT_LOCAL_ALL_SCALE_GERM_BOX__NO_PATH_COORDINATE_MAP",
        }

        canonical_source_fields = {
            "restriction_id": restriction_id,
            "return_component": None,
            "insertion_time": germ["face_time_collision_offset"],
            "collision_index": germ["face_time_collision_offset"],
            "event_signature": event_signature_id,
            "primitive_key": face_id,
            "owner_key": None,
            "rank_zero_component": None,
            "plaque_side": {
                "carrier_kind": "oriented_occurrence_hit_miss",
                "hit_trace_id": hit_trace_id,
                "miss_trace_id": miss_trace_id,
            },
            "word_cell": {
                "occurrence_word_cell_id": occurrence_word_cell_id,
                "global_physical_label": source["global_physical_label"],
                "official_return_path_word_cell_id": None,
            },
            "endpoint_coordinate": endpoint_coordinate_record,
            "root_coordinate": root_coordinate_record,
        }
        require(
            [field for field in REQUIRED_FIELDS
             if canonical_source_fields[field] is None]
            == SOURCE_MISSING_FIELDS,
            "three missing source fields",
        )

        face_rows.append(
            with_hash(
                {
                    "occurrence_record_id":
                        "round132-occurrence-record:"
                        + digest(
                            [
                                "round132-occurrence-record-v1",
                                face_id,
                                restriction_id,
                                event_signature_id,
                                germ["germ_id"],
                            ]
                        ),
                    "immutable_global_occurrence_face_seed_id": face_id,
                    "occurrence_id": occurrence_id,
                    "physical_carrier_type":
                        "moving_first_event_grazing_occurrence_face",
                    "global_physical_label":
                        source["global_physical_label"],
                    "source": source["source"],
                    "tangent_target": source["target"],
                    "epsilon": source["epsilon"],
                    "miss_target": source["miss_target"],
                    "canonical_Round67_source_field_values":
                        canonical_source_fields,
                    "source_side_exact_field_count": 9,
                    "source_side_missing_field_count": 3,
                    "source_side_exact_fields": list(SOURCE_EXACT_FIELDS),
                    "source_side_missing_fields": list(SOURCE_MISSING_FIELDS),
                    "common_boundary_recovery_carrier_id":
                        carrier["common_boundary_recovery_carrier_id"],
                    "selected_all_scale_parameter_germ_id":
                        germ["germ_id"],
                    "hit_trace_seed_id": hit_trace_id,
                    "miss_trace_seed_id": miss_trace_id,
                    "hit_boundary_target_sequence":
                        carrier["hit_boundary_target_sequence"],
                    "miss_boundary_target_sequence":
                        carrier["miss_boundary_target_sequence"],
                    "collision_offset_to_common_carrier":
                        carrier["collision_offset_to_common_carrier"],
                    "positive_coarea_law":
                        current["positive_coarea_law"],
                    "signed_parameter_DQ_current":
                        current["signed_current"],
                    "corrected_unnormalized_density_upper_bound_wrt_dtheta":
                        "18/5",
                    "Round28_rebuilt_face_row": round28_face,
                    "Round28_rebuilt_face_row_sha256":
                        digest(round28_face),
                    "maximal_occurrence_source_row": source,
                    "maximal_occurrence_source_row_sha256": digest(source),
                    "recovery_carrier_row": carrier,
                    "recovery_carrier_row_sha256": digest(carrier),
                    "selected_all_scale_germ_row": germ,
                    "selected_all_scale_germ_row_sha256": digest(germ),
                    "Round67_owner_map_q_j_materialized": False,
                    "Round67_owned_Omega_j_record": False,
                    "occurrence_pullback_component_materialized": False,
                    "exact_endpoint_root_to_s_t_p_map_id": None,
                    "typed_incidence_match_row_id": None,
                }
            )
        )

        for side_label, trace_id, parameter_sign, trace_target in (
            (
                "hit",
                hit_trace_id,
                germ["hit_parameter_sign"],
                source["target"],
            ),
            (
                "miss",
                miss_trace_id,
                germ["miss_parameter_sign"],
                source["miss_target"],
            ),
        ):
            expected_trace_id = (
                "trace:"
                + digest(
                    {
                        "base": carrier["base_signature"],
                        "kind": side_label,
                        "target": trace_target,
                        **(
                            {"epsilon": source["epsilon"]}
                            if side_label == "hit" else {}
                        ),
                    }
                )
            )
            require(trace_id == expected_trace_id, "trace ID reconstruction")
            trace_rows.append(
                with_hash(
                    {
                        "trace_record_id": trace_id,
                        "occurrence_face_seed_id": face_id,
                        "occurrence_id": occurrence_id,
                        "restriction_id": restriction_id,
                        "event_signature_id": event_signature_id,
                        "side_label": side_label,
                        "side_carrier_kind":
                            "oriented_occurrence_hit_miss",
                        "stable_plaque_side_claimed": False,
                        "target": trace_target,
                        "parameter_sign": parameter_sign,
                        "insertion_time": germ["face_time_collision_offset"],
                        "collision_index": germ["face_time_collision_offset"],
                        "collision_offset_to_common_carrier":
                            carrier["collision_offset_to_common_carrier"][
                                side_label
                            ],
                        "common_boundary_recovery_carrier_id":
                            carrier[
                                "common_boundary_recovery_carrier_id"
                            ],
                        "source_event_chart": germ["source_event_chart"],
                        "occurrence_word_cell_id":
                            occurrence_word_cell_id,
                    }
                )
            )

    round28_face_rows.sort(key=canonical)
    face_rows.sort(key=lambda row: row["occurrence_record_id"])
    trace_rows.sort(key=lambda row: row["trace_record_id"])
    require(
        len(round28_face_rows) == len(face_rows) == len(face_ids) == 64,
        "64 occurrence face records",
    )
    require(
        len(trace_rows) == len(trace_ids) == 128,
        "128 occurrence trace records",
    )
    require(len(germ_ids) == 64, "64 germ IDs")
    require(len(restriction_ids) == len(event_ids) == 64, "64 source IDs")
    require(len(word_cell_ids) == 64, "64 occurrence word cells")

    frozen = round28["moving_occurrence_coarea_DQ_face_seed_registry"]
    require(
        digest(round28_face_rows) == frozen["face_rows_sha256"],
        "Round28 full face row digest",
    )
    require(
        digest(sorted(face_ids)) == frozen["face_ids_sha256"],
        "Round28 face ID digest",
    )
    require(
        digest(sorted(trace_ids)) == frozen["trace_seed_ids_sha256"],
        "Round28 trace ID digest",
    )
    require(
        digest(sorted(germ_ids)) == frozen["parameter_germ_ids_sha256"],
        "Round28 germ ID digest",
    )
    require(
        raw_registry["maximal_connected_physical_row_count"] == 64,
        "raw maximal row count",
    )

    replay = {
        "Round28_face_rows_sha256": digest(round28_face_rows),
        "Round28_face_ids_sha256": digest(sorted(face_ids)),
        "Round28_trace_seed_ids_sha256": digest(sorted(trace_ids)),
        "Round28_parameter_germ_ids_sha256": digest(sorted(germ_ids)),
        "Round132_occurrence_record_rows_sha256": digest(face_rows),
        "Round132_trace_record_rows_sha256": digest(trace_rows),
        "restriction_ids_sha256": digest(sorted(restriction_ids)),
        "event_signature_ids_sha256": digest(sorted(event_ids)),
        "occurrence_word_cell_ids_sha256": digest(sorted(word_cell_ids)),
    }
    return round28_face_rows, face_rows, trace_rows, replay


def build() -> dict[str, Any]:
    documents = load_inputs()
    round28 = documents[ROUND28_MANIFEST.name]["result"]
    round67 = documents[ROUND67_MANIFEST.name]["result"]
    round131 = documents[ROUND131_CERTIFICATE.name]["result"]

    fixed = round67["actual_fixed_j_subroot"]
    require(
        fixed["status"] == "CERTIFIED_GRAPH_SUPPORTED_PHYSICAL_SUBROOT",
        "Round67 fixed-j root",
    )
    require(
        fixed["retained_keys"]
        == [
            "restriction-id",
            "time-j",
            "physical-event-signature",
            "primitive-key",
            "connected-rank-0",
            "side-label",
            "word-cell",
            "endpoint/root coordinates",
        ],
        "Round67 retained-key schema",
    )
    require(
        round131["source_census"][
            "Round28_moving_first_event_grazing_occurrence_seed_count"
        ] == 64
        and round131["source_census"][
            "Round28_oriented_hit_miss_occurrence_trace_seed_count"
        ] == 128,
        "Round131 carrier census",
    )

    rebuilt, face_rows, trace_rows, replay = (
        reconstruct_round28_occurrences(round28)
    )
    require(len(rebuilt) == 64, "Round28 rebuilt face count")

    field_rows: list[dict[str, Any]] = []
    for index, field in enumerate(REQUIRED_FIELDS, start=1):
        exact = field in SOURCE_EXACT_FIELDS
        missing = field in SOURCE_MISSING_FIELDS
        require(exact != missing, f"closed field classification: {field}")
        qualifier = {
            "restriction_id":
                "canonical maximal occurrence-row restriction",
            "insertion_time":
                "face_time_collision_offset=1 on all 64 records",
            "collision_index":
                "occurrence face collision offset=1 on all 64 records",
            "event_signature":
                "canonical physical label, boundary and polarity signature",
            "primitive_key":
                "immutable Round28 occurrence-face seed ID",
            "plaque_side":
                "oriented hit/miss side at trace level; not a stable plaque side",
            "word_cell":
                "canonical occurrence word cell; not an official return-path word",
            "endpoint_coordinate":
                "exact local boundary descriptors plus rational witness z",
            "root_coordinate":
                "exact selected local germ box; no path-coordinate map",
            "return_component":
                "no R_n occurrence-pullback component ID",
            "owner_key":
                "Round67 owner map q_j not materialized",
            "rank_zero_component":
                "no occurrence-pullback connected component or canonical rank",
        }[field]
        field_rows.append(
            with_hash(
                {
                    "field_index": index,
                    "required_field": field,
                    "source_side_status":
                        "MATERIALIZED_EXACT_WITH_TYPED_QUALIFIER"
                        if exact else "MISSING",
                    "materialized_record_count": 64 if exact else 0,
                    "qualifier": qualifier,
                    "usable_as_joined_Round67_to_path_key": False,
                }
            )
        )
    require(
        sum(
            row["source_side_status"]
            == "MATERIALIZED_EXACT_WITH_TYPED_QUALIFIER"
            for row in field_rows
        ) == 9,
        "nine exact source fields",
    )

    obstruction_rows = [
        with_hash(
            {
                "obstruction_id": "ROUND67_OWNER_MAP_Q_J_ABSENT",
                "materialized_owner_key_count": 0,
                "effect":
                    "64 source occurrence records are not 64 owned Omega_j records",
            }
        ),
        with_hash(
            {
                "obstruction_id":
                    "OCCURRENCE_PULLBACK_RETURN_COMPONENTS_ABSENT",
                "materialized_return_component_count": 0,
                "materialized_rank_zero_component_count": 0,
                "R1_inner_status": "CERTIFIED_EMPTY",
                "first_unruled_out_depth": "n>=2",
            }
        ),
        with_hash(
            {
                "obstruction_id": "EXACT_ENDPOINT_ROOT_TO_S_T_P_MAP_ABSENT",
                "materialized_exact_map_count": 0,
                "effect":
                    "local exact source coordinates cannot be joined to Round71/72 or an R_n path",
            }
        ),
        with_hash(
            {
                "obstruction_id": "ROUND72_TERMINAL_PREIMAGE_TYPE_MISMATCH",
                "Round72_component_count": 32,
                "Round72_carrier_type":
                    "regular_branch_pullback_of_stationary_destination_core_face",
                "Round132_carrier_type":
                    "moving_first_event_grazing_occurrence_face",
                "direct_typed_match_count": 0,
            }
        ),
    ]

    match_rows: list[dict[str, Any]] = []
    total_rows = len(face_rows) + len(trace_rows) + len(field_rows) + len(
        obstruction_rows
    )
    require(total_rows == 208, "Round132 finite row count")
    all_hashed_rows = face_rows + trace_rows + field_rows + obstruction_rows
    require(
        len({row["row_sha256"] for row in all_hashed_rows}) == total_rows,
        "unique Round132 row hashes",
    )

    return {
        "status":
            "CERTIFIED_64_OCCURRENCE_SOURCE_RECORDS_128_TRACES__OWNER_AND_TYPED_INCIDENCE_OPEN",
        "precision_bits": PRECISION_BITS,
        "provenance": {
            "producer_sha256": sha256_path(PRODUCER),
            "Round28_producer_imported": False,
            "Round28_full_rows_independently_rebuilt_from_three_pinned_sources":
                True,
            "input_byte_pins": {
                name: BYTE_PINS[name] for name in sorted(BYTE_PINS)
            },
            "input_result_pins": {
                name: RESULT_PINS[name] for name in sorted(RESULT_PINS)
            },
            "input_schema_pins": {
                name: SCHEMA_PINS[name] for name in sorted(SCHEMA_PINS)
            },
            "append_only": True,
        },
        "independent_Round28_replay": replay,
        "canonical_record_schema": {
            "version": "round132-occurrence-source-record-v1",
            "restriction_key":
                "(occurrence_id,base_signature,base,left_boundary,right_boundary)",
            "time_and_collision_key":
                "(face_time_collision_offset,collision_index)",
            "event_key":
                "(face_seed_id,global_physical_label,boundaries,polarity)",
            "primitive_key": "immutable Round28 occurrence-face seed ID",
            "side_key":
                "(occurrence_face_seed_id,hit_or_miss,trace_seed_id)",
            "word_key":
                "occurrence global physical label only; not official return path",
            "endpoint_coordinate_key":
                "(source_event_chart,left/right boundary descriptors,rational witness z)",
            "root_coordinate_key":
                "(source_event_chart,exact local z interval,exact local s interval,germ ID)",
            "all_ID_payloads_exclude_Arb_decimal_enclosure_text": True,
        },
        "occurrence_face_record_rows": face_rows,
        "occurrence_face_record_rows_sha256": digest(face_rows),
        "occurrence_trace_record_rows": trace_rows,
        "occurrence_trace_record_rows_sha256": digest(trace_rows),
        "field_materialization_status_rows": field_rows,
        "field_materialization_status_rows_sha256": digest(field_rows),
        "typed_incidence_match_rows": match_rows,
        "typed_incidence_match_rows_sha256": digest(match_rows),
        "obstruction_rows": obstruction_rows,
        "obstruction_rows_sha256": digest(obstruction_rows),
        "count_ledger": {
            "Round28_rebuilt_occurrence_face_count": 64,
            "Round28_rebuilt_oriented_trace_count": 128,
            "canonical_restriction_record_count": 64,
            "canonical_event_signature_count": 64,
            "canonical_occurrence_word_cell_record_count": 64,
            "canonical_endpoint_coordinate_record_count": 64,
            "canonical_root_coordinate_record_count": 64,
            "source_side_exact_required_field_count": 9,
            "source_side_missing_required_field_count": 3,
            "Round67_owned_Omega_j_record_count": 0,
            "occurrence_pullback_return_component_count": 0,
            "occurrence_pullback_rank_zero_component_count": 0,
            "owner_key_count": 0,
            "exact_endpoint_root_to_s_t_p_map_count": 0,
            "typed_incidence_match_row_count": 0,
            "finite_Round132_row_count": 208,
        },
        "Round67_twelve_field_source_materialization": {
            "required_fields": list(REQUIRED_FIELDS),
            "source_side_exact_fields": list(SOURCE_EXACT_FIELDS),
            "source_side_missing_fields": list(SOURCE_MISSING_FIELDS),
            "source_side_status": "9/12",
            "joined_to_owner_or_path_status": "0/12",
            "exact_map_is_an_extra_mandatory_join_object": True,
        },
        "next_required_object": {
            "first_step":
                "materialize q_j owner keys on these occurrence records or an explicitly selected measurable subset",
            "second_step":
                "construct a nonempty n>=2 occurrence-pullback component with canonical connected rank on an R_n path cell",
            "third_step":
                "prove an exact Borel endpoint/root-to-path-coordinate map and oriented side reconciliation",
            "Round71_Round72_terminal_preimage_rows_may_substitute_for_second_step":
                False,
        },
        "global_safety": {
            "Round67_owned_record_count": 0,
            "Round67_to_path_typed_incidence_match_count": 0,
            "Round72_numeric_fields_promoted_to_Round67_root": False,
            "global_complete_18_field_block_count": 0,
            "complete_18_field_block_count": 0,
            "gate5_block_count": 0,
            "gate5_global_maturity": "10/18",
            "gate5_status": "NOT_CERTIFIED",
            "CM2": "NO-GO_FOR_CLAIM",
        },
        "strict_nonclaims": [
            "64 occurrence source records are not 64 Round67 owned Omega_j records",
            "oriented hit/miss sides are not stable plaque sides",
            "occurrence word cells are not official return-path word cells",
            "local endpoint/root coordinate records are not an exact (s,t,p) path map",
            "no R1 occurrence incidence is claimed; strict-inner R1 is certified empty",
            "no n>=2 occurrence-pullback component or connected rank is materialized",
            "Round71/72 terminal-preimage components are not occurrence-pullback components",
            "no F10/F14/F15/F17/F18 common physical block or global Gate5 upgrade",
            "no CM2 claim",
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
