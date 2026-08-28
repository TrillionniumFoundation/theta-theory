#!/usr/bin/env python3
"""Independent verifier for the Round132 occurrence-record materialization.

The verifier does not import or execute the Round132 producer.  It rebuilds
the 64 moving-occurrence face records and 128 oriented traces from the three
frozen source constructions, checks the exact 9/12 source-side qualifier
semantics, reconstructs every one of the 208 closed rows, and keeps the
Round67 owner/path join and all global Gate5 credit at zero.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import importlib.util
import json
import os
import stat
import tempfile
from fractions import Fraction as Q
from pathlib import Path
from types import ModuleType
from typing import Any, Callable

from flint import ctx


HERE = Path(__file__).resolve().parent
VERIFIER = Path(__file__).resolve()
PRODUCER = HERE / "cm2_round132_round28_occurrence_record_materialization.py"
CERTIFICATE = (
    HERE
    / "cm2-round132-round28-occurrence-record-materialization-2026-07-24.json"
)
OUTPUT = (
    HERE
    / "cm2-round132-round28-occurrence-record-materialization-verification-2026-07-24.json"
)

CERTIFICATE_SCHEMA = "cm2.round132.round28-occurrence-record-materialization.v1"
VERIFICATION_SCHEMA = (
    "cm2.round132.round28-occurrence-record-materialization-verification.v1"
)
PRODUCER_SHA256 = (
    "88a12779148a49f111380c0560b0cb490a4e87f00d7ba7671878eec858f87d53"
)
CERTIFICATE_SHA256 = (
    "b5d09c7398dae4b77a6f011430286f88539e0f13ca449e50eb84fc3712d67d31"
)
CERTIFICATE_RESULT_SHA256 = (
    "3a5b4450d838ac39e0e7f596344589b520a8060bb0131bd88fb8f2c77af4d624"
)
PRECISION_BITS = 512

R28P = "cm2_gate5_round28_limiting_physical_face_atlas_frontier_cert.py"
R28 = (
    "cm2-gate5-round28-limiting-physical-face-atlas-frontier-"
    "manifest-2026-07-18.json"
)
DQP = "cm2_gate3_depth_one_fixed_gauge_dq_cert.py"
DQ = "cm2-gate3-depth-one-fixed-gauge-dq-manifest-2026-07-15.json"
RECOVERYP = "cm2_gate34_occurrence_boundary_recovery_carrier_cert.py"
RECOVERY = (
    "cm2-gate34-occurrence-boundary-recovery-carrier-"
    "manifest-2026-07-17.json"
)
PARAMETERP = "cm2_gate34_parameter_dq_all_scale_shell_cert.py"
PARAMETER = (
    "cm2-gate34-parameter-dq-all-scale-shell-manifest-2026-07-17.json"
)
R67P = "cm2_round67_fixed_j_occurrence_owner_root_time_potential_frontier_cert.py"
R67 = (
    "cm2-round67-fixed-j-occurrence-owner-root-time-potential-frontier-"
    "manifest-2026-07-21.json"
)
R131P = "cm2_round131_round67_r1_typed_incidence_crosswalk.py"
R131 = "cm2-round131-round67-r1-typed-incidence-crosswalk-2026-07-24.json"

BYTE_PINS = {
    R28P: "b0dda23ec7e8c9dbe82aff861be6b4e1d38ecf281a82165949537b923150ba27",
    R28: "ad385983a4152da3bc1d9c58a5a2fba1abb928466ecf9a9f61260b612bddf140",
    DQP: "8ce2490ee2b2bdfc251ac1892cb260e40f3eb5d87ce7f232c2076a10c4a9c066",
    DQ: "284b25ac30dd86a01bd0faaa7c0a97ee47839670e3cde4309936235badf5fd52",
    RECOVERYP: "9e69879f921681da4a8eeda9a2af8755c3713151128027784e72cd12896a053a",
    RECOVERY: "dd16bd1e3407a6f886ddbf1270ca7ff7289a7d6792e81235f69014cafaf49cb5",
    PARAMETERP: "ea5b6b7fa265990b1eaa1c106e2c0f82f024b58951bbe65ff55757cbc23df458",
    PARAMETER: "2f374298785c74525e0bbb66b39e30be503ad9af05a913fa3175063196d883a8",
    R67P: "cfb501aff4f321742e3fead9895c596e9105b2a89d064d917646b70c6f91ee8f",
    R67: "97cb410b9e960d8331a37ef9203b040c9b1d86c3ed3d1ba6ba66a28c4e4ff400",
    R131P: "8e7b2bae965be128a288ae38768bf746f5c33c0744449f8edea48014bd22d611",
    R131: "a8e4b9dabb30396469f28d4df252c9f5de1d9d1620c0a18d252ef23a12f1f3d6",
}

SCHEMA_PINS = {
    R28: "cm2.gate5.round28-limiting-physical-face-atlas-frontier.manifest.v3",
    DQ: "cm2.gate3.depth-one-fixed-gauge-dq.manifest.v1",
    RECOVERY: "cm2.gate34.occurrence-boundary-recovery-carrier.manifest.v1",
    PARAMETER: "cm2.gate34.parameter-dq-all-scale-shell.manifest.v1",
    R67: "cm2.round67.fixed-j-occurrence-owner-root-time-potential.v1.manifest.v1",
    R131: "cm2.round131.round67-r1-typed-incidence-crosswalk.v1",
}

RESULT_PINS = {
    R28: "282d73b9146a38ff41f78ab6d0fd619c1b955eda32ed3dd5cdae2fd170b340b6",
    DQ: "3b05206952610710ffc037b483fd81c77589c08903c722b4e7b56fe2d964c276",
    RECOVERY: "a07d8a96949ed18a78b0753546892ddc043b47191bfc75024874e6394ef2f741",
    PARAMETER: "8eb47e4bbebc6739b4d7a25a923495b672edffd1bf9456ba37c560174e8a5012",
    R67: "c1fd3e486d671b83c6ae6a0c6da8c4d50bd2796842cfe1c8d8d5985001e5a57f",
    R131: "0fd7f419d5a0afa3fbc20db3757803ee5c2982b4428ba52a97798a6fcc28a0ab",
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
GROUPS = [
    "occurrence_face_record_rows",
    "occurrence_trace_record_rows",
    "field_materialization_status_rows",
    "typed_incidence_match_rows",
    "obstruction_rows",
]


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


def sha256_bytes(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def sha256_path(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def qstr(value: Q) -> str:
    return (
        str(value.numerator)
        if value.denominator == 1
        else f"{value.numerator}/{value.denominator}"
    )


def strict_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        require(key not in result, f"duplicate JSON key:{key}")
        result[key] = value
    return result


def reject_constant(token: str) -> None:
    raise VerificationError(f"non-finite JSON constant:{token}")


def strict_json_bytes(raw: bytes, label: str) -> dict[str, Any]:
    require(len(raw) <= 4_000_000, f"oversized JSON:{label}")
    require(not raw.startswith(b"\xef\xbb\xbf"), f"UTF-8 BOM:{label}")
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise VerificationError(f"invalid UTF-8:{label}") from exc
    try:
        value = json.loads(
            text,
            object_pairs_hook=strict_object,
            parse_constant=reject_constant,
        )
    except (json.JSONDecodeError, UnicodeDecodeError, ValueError) as exc:
        raise VerificationError(f"strict JSON:{label}") from exc
    require(isinstance(value, dict), f"top-level object:{label}")
    return value


def strict_json_path(path: Path) -> dict[str, Any]:
    return strict_json_bytes(path.read_bytes(), path.name)


def closed_row(row: dict[str, Any]) -> dict[str, Any]:
    require("row_sha256" not in row, "row already closed")
    return {**row, "row_sha256": digest(row)}


def load_source_module(name: str) -> ModuleType:
    path = HERE / name
    require(sha256_path(path) == BYTE_PINS[name], f"module pin:{name}")
    specification = importlib.util.spec_from_file_location(
        "round132_verifier_" + name.removesuffix(".py"),
        path,
    )
    require(
        specification is not None and specification.loader is not None,
        f"module specification:{name}",
    )
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


def load_upstreams(check_files: bool = True) -> dict[str, dict[str, Any]]:
    if check_files:
        for name, expected in BYTE_PINS.items():
            path = HERE / name
            require(path.is_file(), f"missing upstream:{name}")
            require(sha256_path(path) == expected, f"upstream byte pin:{name}")
        require(sha256_path(PRODUCER) == PRODUCER_SHA256, "producer byte pin")

    documents: dict[str, dict[str, Any]] = {}
    for name in SCHEMA_PINS:
        document = strict_json_path(HERE / name)
        require(document.get("schema") == SCHEMA_PINS[name], f"schema pin:{name}")
        require(isinstance(document.get("result"), dict), f"result object:{name}")
        require(digest(document["result"]) == RESULT_PINS[name], f"result pin:{name}")
        if name == R131:
            require(
                document.get("result_sha256") == RESULT_PINS[name],
                "Round131 stored result digest",
            )
        documents[name] = document

    r131 = documents[R131]["result"]
    require(
        r131["crosswalk_census"]["typed_incidence_match_row_count"] == 0,
        "Round131 zero typed matches",
    )
    require(
        r131["source_census"]["R1_inner_moving_occurrence_typed_incidence_status"]
        == "CERTIFIED_EMPTY",
        "Round131 R1 occurrence incidence empty",
    )
    require(
        r131["global_safety"]["gate5_global_maturity"] == "10/18"
        and r131["global_safety"]["CM2"] == "NO-GO_FOR_CLAIM",
        "Round131 safety",
    )
    return documents


def reconstruct_occurrence_rows(
    round28: dict[str, Any],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], dict[str, Any]]:
    """Rebuild the rows directly from the frozen lower-level constructors."""

    ctx.prec = PRECISION_BITS
    dq = load_source_module(DQP)
    recovery = load_source_module(RECOVERYP)
    parameter = load_source_module(PARAMETERP)

    raw_rows, raw_registry = dq.load_rows()
    typed_rows, typed_registry = dq.corrected_current_rows(raw_rows)
    carrier_rows, carrier_registry = recovery.build_carrier_registry()
    germ_rows = [parameter.certify_germ(row) for row in raw_rows]

    raw = {row["occurrence_id"]: row for row in raw_rows}
    typed = {row["occurrence_id"]: row for row in typed_rows}
    carriers = {row["occurrence_id"]: row for row in carrier_rows}
    germs = {row["occurrence_id"]: row for row in germ_rows}
    require(
        len(raw) == len(typed) == len(carriers) == len(germs) == 64,
        "64-way occurrence reconstruction",
    )
    require(set(raw) == set(typed) == set(carriers) == set(germs), "occurrence join")
    require(
        typed_registry["maximal_row_current_count"] == 64
        and typed_registry["strict_hit_and_miss_trace_attached_to_every_row"] is True,
        "typed-current registry",
    )
    require(
        carrier_registry["oriented_hit_miss_trace_seed_count"] == 128,
        "carrier trace registry",
    )

    round28_faces: list[dict[str, Any]] = []
    faces: list[dict[str, Any]] = []
    traces: list[dict[str, Any]] = []
    face_ids: set[str] = set()
    trace_ids: set[str] = set()
    germ_ids: set[str] = set()
    restriction_ids: set[str] = set()
    event_ids: set[str] = set()
    word_ids: set[str] = set()

    for occurrence_id in sorted(raw):
        source = raw[occurrence_id]
        current = typed[occurrence_id]
        carrier = carriers[occurrence_id]
        germ = germs[occurrence_id]
        require(
            current["global_physical_label"]
            == carrier["global_physical_label"]
            == source["global_physical_label"],
            "physical-label join",
        )
        require(current["base"] == source["base"], "base join")
        require(
            current["left_boundary"] == source["left_boundary"]
            and current["right_boundary"] == source["right_boundary"],
            "boundary join",
        )
        require(germ["face_time_collision_offset"] == 1, "collision offset one")
        require(
            germ["hit_parameter_sign"] == current["signed_current"]["polarity"]
            and germ["miss_parameter_sign"] == -current["signed_current"]["polarity"],
            "parameter signs",
        )
        require(
            carrier["shared_pulled_back_event_base_restriction"] is True,
            "shared restriction",
        )

        face_payload = {
            "occurrence_id": occurrence_id,
            "global_physical_label": source["global_physical_label"],
            "source": source["source"],
            "tangent_target": source["target"],
            "epsilon": source["epsilon"],
            "miss_target": source["miss_target"],
        }
        face_id = "physical-moving-occurrence-face-seed:" + digest(face_payload)
        require(face_id not in face_ids, "unique face ID")
        face_ids.add(face_id)
        germ_ids.add(germ["germ_id"])
        hit_trace_id = carrier["hit_trace_seed_id"]
        miss_trace_id = carrier["miss_trace_seed_id"]
        require(
            hit_trace_id not in trace_ids and miss_trace_id not in trace_ids,
            "unique trace IDs",
        )
        trace_ids.update((hit_trace_id, miss_trace_id))

        round28_face = {
            "immutable_global_occurrence_face_seed_id": face_id,
            **face_payload,
            "physical_carrier_type": "moving_first_event_grazing_occurrence_face",
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
        round28_faces.append(round28_face)

        restriction_id = "round132-occurrence-restriction:" + digest(
            [
                "round132-occurrence-restriction-v1",
                occurrence_id,
                carrier["base_signature"],
                source["base"],
                source["left_boundary"],
                source["right_boundary"],
            ]
        )
        event_id = "round132-occurrence-event-signature:" + digest(
            [
                "round132-occurrence-event-signature-v1",
                face_id,
                source["global_physical_label"],
                source["left_boundary"],
                source["right_boundary"],
                source["parameter_coarea_polarity"],
            ]
        )
        word_id = "round132-occurrence-word-cell:" + digest(
            ["round132-occurrence-word-cell-v1", source["global_physical_label"]]
        )
        require(restriction_id not in restriction_ids, "unique restriction")
        require(event_id not in event_ids, "unique event")
        restriction_ids.add(restriction_id)
        event_ids.add(event_id)
        word_ids.add(word_id)

        witness_z = Q(source["witness"]["z"])
        half_width = Q(germ["base_half_width"])
        endpoint = {
            "coordinate_record_version": "round132-occurrence-endpoint-coordinate-v1",
            "source_event_chart": germ["source_event_chart"],
            "exact_rational_witness_z": qstr(witness_z),
            "left_boundary_descriptor": source["left_boundary"],
            "right_boundary_descriptor": source["right_boundary"],
            "coordinate_status":
                "EXACT_LOCAL_MAXIMAL_ROW_DESCRIPTOR_AND_RATIONAL_WITNESS",
        }
        root = {
            "coordinate_record_version": "round132-occurrence-root-coordinate-v1",
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
            "parameter_magnitude_interval": germ["parameter_magnitude_interval"],
            "germ_geometry_sha256": germ["germ_geometry_sha256"],
            "coordinate_status":
                "EXACT_LOCAL_ALL_SCALE_GERM_BOX__NO_PATH_COORDINATE_MAP",
        }
        source_fields = {
            "restriction_id": restriction_id,
            "return_component": None,
            "insertion_time": germ["face_time_collision_offset"],
            "collision_index": germ["face_time_collision_offset"],
            "event_signature": event_id,
            "primitive_key": face_id,
            "owner_key": None,
            "rank_zero_component": None,
            "plaque_side": {
                "carrier_kind": "oriented_occurrence_hit_miss",
                "hit_trace_id": hit_trace_id,
                "miss_trace_id": miss_trace_id,
            },
            "word_cell": {
                "occurrence_word_cell_id": word_id,
                "global_physical_label": source["global_physical_label"],
                "official_return_path_word_cell_id": None,
            },
            "endpoint_coordinate": endpoint,
            "root_coordinate": root,
        }
        require(
            [field for field in REQUIRED_FIELDS if source_fields[field] is None]
            == SOURCE_MISSING_FIELDS,
            "exactly three source gaps",
        )

        record_id = "round132-occurrence-record:" + digest(
            [
                "round132-occurrence-record-v1",
                face_id,
                restriction_id,
                event_id,
                germ["germ_id"],
            ]
        )
        faces.append(
            closed_row(
                {
                    "occurrence_record_id": record_id,
                    "immutable_global_occurrence_face_seed_id": face_id,
                    "occurrence_id": occurrence_id,
                    "physical_carrier_type":
                        "moving_first_event_grazing_occurrence_face",
                    "global_physical_label": source["global_physical_label"],
                    "source": source["source"],
                    "tangent_target": source["target"],
                    "epsilon": source["epsilon"],
                    "miss_target": source["miss_target"],
                    "canonical_Round67_source_field_values": source_fields,
                    "source_side_exact_field_count": 9,
                    "source_side_missing_field_count": 3,
                    "source_side_exact_fields": list(SOURCE_EXACT_FIELDS),
                    "source_side_missing_fields": list(SOURCE_MISSING_FIELDS),
                    "common_boundary_recovery_carrier_id":
                        carrier["common_boundary_recovery_carrier_id"],
                    "selected_all_scale_parameter_germ_id": germ["germ_id"],
                    "hit_trace_seed_id": hit_trace_id,
                    "miss_trace_seed_id": miss_trace_id,
                    "hit_boundary_target_sequence":
                        carrier["hit_boundary_target_sequence"],
                    "miss_boundary_target_sequence":
                        carrier["miss_boundary_target_sequence"],
                    "collision_offset_to_common_carrier":
                        carrier["collision_offset_to_common_carrier"],
                    "positive_coarea_law": current["positive_coarea_law"],
                    "signed_parameter_DQ_current": current["signed_current"],
                    "corrected_unnormalized_density_upper_bound_wrt_dtheta": "18/5",
                    "Round28_rebuilt_face_row": round28_face,
                    "Round28_rebuilt_face_row_sha256": digest(round28_face),
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

        for side, trace_id, sign, target in (
            ("hit", hit_trace_id, germ["hit_parameter_sign"], source["target"]),
            ("miss", miss_trace_id, germ["miss_parameter_sign"], source["miss_target"]),
        ):
            expected_trace_id = "trace:" + digest(
                {
                    "base": carrier["base_signature"],
                    "kind": side,
                    "target": target,
                    **({"epsilon": source["epsilon"]} if side == "hit" else {}),
                }
            )
            require(trace_id == expected_trace_id, "trace ID reconstruction")
            traces.append(
                closed_row(
                    {
                        "trace_record_id": trace_id,
                        "occurrence_face_seed_id": face_id,
                        "occurrence_id": occurrence_id,
                        "restriction_id": restriction_id,
                        "event_signature_id": event_id,
                        "side_label": side,
                        "side_carrier_kind": "oriented_occurrence_hit_miss",
                        "stable_plaque_side_claimed": False,
                        "target": target,
                        "parameter_sign": sign,
                        "insertion_time": germ["face_time_collision_offset"],
                        "collision_index": germ["face_time_collision_offset"],
                        "collision_offset_to_common_carrier":
                            carrier["collision_offset_to_common_carrier"][side],
                        "common_boundary_recovery_carrier_id":
                            carrier["common_boundary_recovery_carrier_id"],
                        "source_event_chart": germ["source_event_chart"],
                        "occurrence_word_cell_id": word_id,
                    }
                )
            )

    round28_faces.sort(key=canonical)
    faces.sort(key=lambda row: row["occurrence_record_id"])
    traces.sort(key=lambda row: row["trace_record_id"])
    require(len(round28_faces) == len(faces) == len(face_ids) == 64, "64 faces")
    require(len(traces) == len(trace_ids) == 128, "128 traces")
    require(len(germ_ids) == 64, "64 germs")
    require(len(restriction_ids) == len(event_ids) == len(word_ids) == 64, "64 IDs")

    frozen = round28["moving_occurrence_coarea_DQ_face_seed_registry"]
    require(digest(round28_faces) == frozen["face_rows_sha256"], "Round28 face digest")
    require(digest(sorted(face_ids)) == frozen["face_ids_sha256"], "Round28 ID digest")
    require(
        digest(sorted(trace_ids)) == frozen["trace_seed_ids_sha256"],
        "Round28 trace digest",
    )
    require(
        digest(sorted(germ_ids)) == frozen["parameter_germ_ids_sha256"],
        "Round28 germ digest",
    )
    require(
        raw_registry["maximal_connected_physical_row_count"] == 64,
        "raw maximal row count",
    )

    replay = {
        "Round28_face_rows_sha256": digest(round28_faces),
        "Round28_face_ids_sha256": digest(sorted(face_ids)),
        "Round28_trace_seed_ids_sha256": digest(sorted(trace_ids)),
        "Round28_parameter_germ_ids_sha256": digest(sorted(germ_ids)),
        "Round132_occurrence_record_rows_sha256": digest(faces),
        "Round132_trace_record_rows_sha256": digest(traces),
        "restriction_ids_sha256": digest(sorted(restriction_ids)),
        "event_signature_ids_sha256": digest(sorted(event_ids)),
        "occurrence_word_cell_ids_sha256": digest(sorted(word_ids)),
    }
    return faces, traces, replay


def field_status_rows() -> list[dict[str, Any]]:
    qualifiers = {
        "restriction_id": "canonical maximal occurrence-row restriction",
        "return_component": "no R_n occurrence-pullback component ID",
        "insertion_time": "face_time_collision_offset=1 on all 64 records",
        "collision_index": "occurrence face collision offset=1 on all 64 records",
        "event_signature": "canonical physical label, boundary and polarity signature",
        "primitive_key": "immutable Round28 occurrence-face seed ID",
        "owner_key": "Round67 owner map q_j not materialized",
        "rank_zero_component":
            "no occurrence-pullback connected component or canonical rank",
        "plaque_side":
            "oriented hit/miss side at trace level; not a stable plaque side",
        "word_cell":
            "canonical occurrence word cell; not an official return-path word",
        "endpoint_coordinate":
            "exact local boundary descriptors plus rational witness z",
        "root_coordinate":
            "exact selected local germ box; no path-coordinate map",
    }
    rows: list[dict[str, Any]] = []
    for index, field in enumerate(REQUIRED_FIELDS, start=1):
        exact = field in SOURCE_EXACT_FIELDS
        require(exact != (field in SOURCE_MISSING_FIELDS), f"field partition:{field}")
        rows.append(
            closed_row(
                {
                    "field_index": index,
                    "required_field": field,
                    "source_side_status":
                        "MATERIALIZED_EXACT_WITH_TYPED_QUALIFIER"
                        if exact
                        else "MISSING",
                    "materialized_record_count": 64 if exact else 0,
                    "qualifier": qualifiers[field],
                    "usable_as_joined_Round67_to_path_key": False,
                }
            )
        )
    return rows


def obstruction_rows() -> list[dict[str, Any]]:
    return [
        closed_row(
            {
                "obstruction_id": "ROUND67_OWNER_MAP_Q_J_ABSENT",
                "materialized_owner_key_count": 0,
                "effect":
                    "64 source occurrence records are not 64 owned Omega_j records",
            }
        ),
        closed_row(
            {
                "obstruction_id": "OCCURRENCE_PULLBACK_RETURN_COMPONENTS_ABSENT",
                "materialized_return_component_count": 0,
                "materialized_rank_zero_component_count": 0,
                "R1_inner_status": "CERTIFIED_EMPTY",
                "first_unruled_out_depth": "n>=2",
            }
        ),
        closed_row(
            {
                "obstruction_id": "EXACT_ENDPOINT_ROOT_TO_S_T_P_MAP_ABSENT",
                "materialized_exact_map_count": 0,
                "effect":
                    "local exact source coordinates cannot be joined to Round71/72 or an R_n path",
            }
        ),
        closed_row(
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


def build_expected(check_files: bool = True) -> dict[str, Any]:
    documents = load_upstreams(check_files=check_files)
    round28 = documents[R28]["result"]
    round67 = documents[R67]["result"]
    round131 = documents[R131]["result"]
    fixed = round67["actual_fixed_j_subroot"]
    require(
        fixed["status"] == "CERTIFIED_GRAPH_SUPPORTED_PHYSICAL_SUBROOT",
        "Round67 fixed root",
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
        "Round67 retained schema",
    )
    require(
        round131["source_census"][
            "Round28_moving_first_event_grazing_occurrence_seed_count"
        ]
        == 64
        and round131["source_census"][
            "Round28_oriented_hit_miss_occurrence_trace_seed_count"
        ]
        == 128,
        "Round131 source census",
    )

    faces, traces, replay = reconstruct_occurrence_rows(round28)
    fields = field_status_rows()
    obstructions = obstruction_rows()
    matches: list[dict[str, Any]] = []
    all_rows = faces + traces + fields + obstructions
    require(
        len(all_rows) == len({row["row_sha256"] for row in all_rows}) == 208,
        "208 unique rows",
    )

    result = {
        "status":
            "CERTIFIED_64_OCCURRENCE_SOURCE_RECORDS_128_TRACES__OWNER_AND_TYPED_INCIDENCE_OPEN",
        "precision_bits": PRECISION_BITS,
        "provenance": {
            "producer_sha256": PRODUCER_SHA256,
            "Round28_producer_imported": False,
            "Round28_full_rows_independently_rebuilt_from_three_pinned_sources": True,
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
        "occurrence_face_record_rows": faces,
        "occurrence_face_record_rows_sha256": digest(faces),
        "occurrence_trace_record_rows": traces,
        "occurrence_trace_record_rows_sha256": digest(traces),
        "field_materialization_status_rows": fields,
        "field_materialization_status_rows_sha256": digest(fields),
        "typed_incidence_match_rows": matches,
        "typed_incidence_match_rows_sha256": digest(matches),
        "obstruction_rows": obstructions,
        "obstruction_rows_sha256": digest(obstructions),
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
    require(digest(result) == CERTIFICATE_RESULT_SHA256, "expected result digest")
    return result


def validate_row_closures(result: dict[str, Any]) -> None:
    counts = [64, 128, 12, 0, 4]
    hashes: list[str] = []
    for group, count in zip(GROUPS, counts):
        rows = result.get(group)
        require(isinstance(rows, list) and len(rows) == count, f"group count:{group}")
        require(result.get(group + "_sha256") == digest(rows), f"group digest:{group}")
        for row in rows:
            require(isinstance(row, dict), f"row object:{group}")
            payload = dict(row)
            recorded = payload.pop("row_sha256", None)
            require(recorded == digest(payload), f"row digest:{group}")
            hashes.append(recorded)
    require(len(hashes) == len(set(hashes)) == 208, "208 unique row digests")

    faces = result["occurrence_face_record_rows"]
    traces = result["occurrence_trace_record_rows"]
    face_ids = {
        row["immutable_global_occurrence_face_seed_id"]: row for row in faces
    }
    require(len(face_ids) == 64, "64 unique face IDs")
    trace_ids = {row["trace_record_id"] for row in traces}
    require(len(trace_ids) == 128, "128 unique trace IDs")
    traces_by_face: dict[str, list[dict[str, Any]]] = {
        identifier: [] for identifier in face_ids
    }
    for trace in traces:
        require(
            trace["occurrence_face_seed_id"] in traces_by_face,
            "trace points to known face",
        )
        traces_by_face[trace["occurrence_face_seed_id"]].append(trace)
        require(
            trace["side_carrier_kind"] == "oriented_occurrence_hit_miss"
            and trace["stable_plaque_side_claimed"] is False,
            "trace side is oriented hit/miss, not stable plaque",
        )

    for identifier, face in face_ids.items():
        attached = traces_by_face[identifier]
        require(
            len(attached) == 2
            and {row["side_label"] for row in attached} == {"hit", "miss"},
            "one hit and one miss trace per face",
        )
        values = face["canonical_Round67_source_field_values"]
        require(set(values) == set(REQUIRED_FIELDS), "closed twelve-field source row")
        require(
            [field for field in REQUIRED_FIELDS if values[field] is None]
            == SOURCE_MISSING_FIELDS,
            "only return/owner/rank missing",
        )
        require(
            values["plaque_side"]["carrier_kind"]
            == "oriented_occurrence_hit_miss",
            "plaque-side typed qualifier",
        )
        require(
            values["word_cell"]["official_return_path_word_cell_id"] is None,
            "word cell is not official return-path word",
        )
        require(
            {
                row["trace_record_id"] for row in attached
            }
            == {
                values["plaque_side"]["hit_trace_id"],
                values["plaque_side"]["miss_trace_id"],
            },
            "trace-to-side linkage",
        )
        require(
            all(
                row["occurrence_word_cell_id"]
                == values["word_cell"]["occurrence_word_cell_id"]
                for row in attached
            ),
            "trace-to-occurrence-word linkage",
        )
        for embedded, recorded in (
            ("Round28_rebuilt_face_row", "Round28_rebuilt_face_row_sha256"),
            (
                "maximal_occurrence_source_row",
                "maximal_occurrence_source_row_sha256",
            ),
            ("recovery_carrier_row", "recovery_carrier_row_sha256"),
            (
                "selected_all_scale_germ_row",
                "selected_all_scale_germ_row_sha256",
            ),
        ):
            require(digest(face[embedded]) == face[recorded], f"embedded digest:{embedded}")
        require(
            face["Round67_owner_map_q_j_materialized"] is False
            and face["Round67_owned_Omega_j_record"] is False
            and face["occurrence_pullback_component_materialized"] is False
            and face["exact_endpoint_root_to_s_t_p_map_id"] is None
            and face["typed_incidence_match_row_id"] is None,
            "face remains unowned and unmatched",
        )

    fields = result["field_materialization_status_rows"]
    require(
        [row["required_field"] for row in fields] == REQUIRED_FIELDS,
        "field order",
    )
    require(
        [
            row["required_field"]
            for row in fields
            if row["source_side_status"]
            == "MATERIALIZED_EXACT_WITH_TYPED_QUALIFIER"
        ]
        == SOURCE_EXACT_FIELDS,
        "nine exact-with-qualifier fields",
    )
    require(
        [
            row["required_field"]
            for row in fields
            if row["source_side_status"] == "MISSING"
        ]
        == SOURCE_MISSING_FIELDS,
        "three missing fields",
    )
    require(
        all(
            row["usable_as_joined_Round67_to_path_key"] is False
            for row in fields
        ),
        "no field usable as joined key",
    )
    require(
        fields[8]["qualifier"]
        == "oriented hit/miss side at trace level; not a stable plaque side",
        "plaque-side nonclaim",
    )
    require(
        fields[9]["qualifier"]
        == "canonical occurrence word cell; not an official return-path word",
        "word-cell nonclaim",
    )

    ledger = result["count_ledger"]
    require(ledger["finite_Round132_row_count"] == 208, "finite row ledger")
    require(
        ledger["source_side_exact_required_field_count"] == 9
        and ledger["source_side_missing_required_field_count"] == 3,
        "9/12 source ledger",
    )
    require(
        ledger["Round67_owned_Omega_j_record_count"]
        == ledger["occurrence_pullback_return_component_count"]
        == ledger["occurrence_pullback_rank_zero_component_count"]
        == ledger["owner_key_count"]
        == ledger["exact_endpoint_root_to_s_t_p_map_count"]
        == ledger["typed_incidence_match_row_count"]
        == 0,
        "owner/map/match counts remain zero",
    )
    materialization = result["Round67_twelve_field_source_materialization"]
    require(
        materialization["source_side_status"] == "9/12"
        and materialization["joined_to_owner_or_path_status"] == "0/12",
        "source 9/12 is not joined 9/12",
    )
    safety = result["global_safety"]
    require(
        safety["Round67_owned_record_count"] == 0
        and safety["Round67_to_path_typed_incidence_match_count"] == 0
        and safety["global_complete_18_field_block_count"] == 0
        and safety["complete_18_field_block_count"] == 0
        and safety["gate5_block_count"] == 0
        and safety["gate5_global_maturity"] == "10/18"
        and safety["gate5_status"] == "NOT_CERTIFIED"
        and safety["CM2"] == "NO-GO_FOR_CLAIM",
        "global safety",
    )


def evaluate_document(document: dict[str, Any], expected: dict[str, Any]) -> None:
    require(
        set(document) == {"schema", "result", "result_sha256"},
        "closed certificate envelope",
    )
    require(document["schema"] == CERTIFICATE_SCHEMA, "certificate schema")
    result = document["result"]
    require(isinstance(result, dict), "certificate result object")
    require(document["result_sha256"] == digest(result), "outer result digest")
    validate_row_closures(result)
    require(result == expected, "independent expected result equality")
    require(
        document["result_sha256"] == CERTIFICATE_RESULT_SHA256,
        "frozen result digest",
    )


def close_mutated_row(result: dict[str, Any], group: str, index: int) -> None:
    row = result[group][index]
    row.pop("row_sha256", None)
    row["row_sha256"] = digest(row)
    result[group + "_sha256"] = digest(result[group])


def resign(document: dict[str, Any]) -> None:
    document["result_sha256"] = digest(document["result"])


def semantic_mutations(
    certificate: dict[str, Any],
    expected: dict[str, Any],
) -> list[str]:
    mutations: list[tuple[str, Callable[[dict[str, Any]], None]]] = []

    def simple(path: tuple[Any, ...], value: Any) -> Callable[[dict[str, Any]], None]:
        def mutate(document: dict[str, Any]) -> None:
            target: Any = document
            for key in path[:-1]:
                target = target[key]
            target[path[-1]] = value
            resign(document)

        return mutate

    def mutate_row(
        group: str,
        index: int,
        operation: Callable[[dict[str, Any]], None],
    ) -> Callable[[dict[str, Any]], None]:
        def mutate(document: dict[str, Any]) -> None:
            result = document["result"]
            operation(result[group][index])
            close_mutated_row(result, group, index)
            resign(document)

        return mutate

    def invent_match(document: dict[str, Any]) -> None:
        result = document["result"]
        result["typed_incidence_match_rows"].append(
            closed_row(
                {
                    "typed_incidence_match_id": "round132-match:" + "0" * 64,
                    "occurrence_record_id": result["occurrence_face_record_rows"][0][
                        "occurrence_record_id"
                    ],
                    "owner_key": "owner:" + "0" * 64,
                    "path_cell_id": "path:" + "0" * 64,
                    "exact_map_id": "map:" + "0" * 64,
                }
            )
        )
        result["typed_incidence_match_rows_sha256"] = digest(
            result["typed_incidence_match_rows"]
        )
        result["count_ledger"]["typed_incidence_match_row_count"] = 1
        result["count_ledger"]["finite_Round132_row_count"] = 209
        resign(document)

    def delete_face(document: dict[str, Any]) -> None:
        result = document["result"]
        result["occurrence_face_record_rows"].pop()
        result["occurrence_face_record_rows_sha256"] = digest(
            result["occurrence_face_record_rows"]
        )
        result["count_ledger"]["Round28_rebuilt_occurrence_face_count"] = 63
        result["count_ledger"]["finite_Round132_row_count"] = 207
        resign(document)

    def delete_trace(document: dict[str, Any]) -> None:
        result = document["result"]
        result["occurrence_trace_record_rows"].pop()
        result["occurrence_trace_record_rows_sha256"] = digest(
            result["occurrence_trace_record_rows"]
        )
        result["count_ledger"]["Round28_rebuilt_oriented_trace_count"] = 127
        result["count_ledger"]["finite_Round132_row_count"] = 207
        resign(document)

    def tamper_embedded_source(row: dict[str, Any]) -> None:
        row["maximal_occurrence_source_row"]["epsilon"] = 999
        row["maximal_occurrence_source_row_sha256"] = digest(
            row["maximal_occurrence_source_row"]
        )

    mutations.extend(
        [
            (
                "certificate schema altered",
                lambda document: (
                    document.__setitem__("schema", "bad"),
                    resign(document),
                ),
            ),
            (
                "status altered",
                simple(("result", "status"), "CERTIFIED_OWNER_JOIN"),
            ),
            (
                "precision altered",
                simple(("result", "precision_bits"), 511),
            ),
            (
                "producer pin altered",
                simple(("result", "provenance", "producer_sha256"), "0" * 64),
            ),
            (
                "Round28 source pin altered",
                simple(("result", "provenance", "input_byte_pins", R28P), "0" * 64),
            ),
            (
                "Round131 result pin altered",
                simple(("result", "provenance", "input_result_pins", R131), "0" * 64),
            ),
            (
                "Round28 import claim altered",
                simple(("result", "provenance", "Round28_producer_imported"), True),
            ),
            (
                "append-only claim altered",
                simple(("result", "provenance", "append_only"), False),
            ),
            (
                "replay face digest altered",
                simple(
                    ("result", "independent_Round28_replay", "Round28_face_rows_sha256"),
                    "0" * 64,
                ),
            ),
            (
                "record schema side promoted",
                simple(
                    ("result", "canonical_record_schema", "side_key"),
                    "stable plaque side",
                ),
            ),
            (
                "record schema word promoted",
                simple(
                    ("result", "canonical_record_schema", "word_key"),
                    "official return path",
                ),
            ),
            ("face deleted and ledgers re-signed", delete_face),
            ("trace deleted and ledgers re-signed", delete_trace),
            (
                "face carrier type altered",
                mutate_row(
                    "occurrence_face_record_rows",
                    0,
                    lambda row: row.__setitem__(
                        "physical_carrier_type",
                        "stationary_destination_core_preimage",
                    ),
                ),
            ),
            (
                "face owner map fabricated",
                mutate_row(
                    "occurrence_face_record_rows",
                    0,
                    lambda row: row.__setitem__(
                        "Round67_owner_map_q_j_materialized", True
                    ),
                ),
            ),
            (
                "face owned Omega fabricated",
                mutate_row(
                    "occurrence_face_record_rows",
                    0,
                    lambda row: row.__setitem__("Round67_owned_Omega_j_record", True),
                ),
            ),
            (
                "return component fabricated",
                mutate_row(
                    "occurrence_face_record_rows",
                    0,
                    lambda row: (
                        row["canonical_Round67_source_field_values"].__setitem__(
                            "return_component", "component:" + "0" * 64
                        ),
                        row.__setitem__(
                            "occurrence_pullback_component_materialized", True
                        ),
                    ),
                ),
            ),
            (
                "owner key fabricated",
                mutate_row(
                    "occurrence_face_record_rows",
                    0,
                    lambda row: row[
                        "canonical_Round67_source_field_values"
                    ].__setitem__("owner_key", "owner:" + "0" * 64),
                ),
            ),
            (
                "rank-zero component fabricated",
                mutate_row(
                    "occurrence_face_record_rows",
                    0,
                    lambda row: row[
                        "canonical_Round67_source_field_values"
                    ].__setitem__("rank_zero_component", 0),
                ),
            ),
            (
                "oriented side promoted to stable plaque",
                mutate_row(
                    "occurrence_face_record_rows",
                    0,
                    lambda row: row[
                        "canonical_Round67_source_field_values"
                    ]["plaque_side"].__setitem__("carrier_kind", "stable_plaque"),
                ),
            ),
            (
                "occurrence word promoted to official word",
                mutate_row(
                    "occurrence_face_record_rows",
                    0,
                    lambda row: row[
                        "canonical_Round67_source_field_values"
                    ]["word_cell"].__setitem__(
                        "official_return_path_word_cell_id",
                        "gate5-word:000000:" + "0" * 64,
                    ),
                ),
            ),
            (
                "exact path map fabricated",
                mutate_row(
                    "occurrence_face_record_rows",
                    0,
                    lambda row: row.__setitem__(
                        "exact_endpoint_root_to_s_t_p_map_id", "map:" + "0" * 64
                    ),
                ),
            ),
            (
                "typed incidence row link fabricated",
                mutate_row(
                    "occurrence_face_record_rows",
                    0,
                    lambda row: row.__setitem__(
                        "typed_incidence_match_row_id", "match:" + "0" * 64
                    ),
                ),
            ),
            (
                "embedded source altered with digest reclosed",
                mutate_row("occurrence_face_record_rows", 0, tamper_embedded_source),
            ),
            (
                "face exact-field count promoted",
                mutate_row(
                    "occurrence_face_record_rows",
                    0,
                    lambda row: row.__setitem__("source_side_exact_field_count", 12),
                ),
            ),
            (
                "face missing-field list erased",
                mutate_row(
                    "occurrence_face_record_rows",
                    0,
                    lambda row: row.__setitem__("source_side_missing_fields", []),
                ),
            ),
            (
                "trace stable plaque promoted",
                mutate_row(
                    "occurrence_trace_record_rows",
                    0,
                    lambda row: row.__setitem__("stable_plaque_side_claimed", True),
                ),
            ),
            (
                "trace side carrier promoted",
                mutate_row(
                    "occurrence_trace_record_rows",
                    0,
                    lambda row: row.__setitem__("side_carrier_kind", "stable_plaque"),
                ),
            ),
            (
                "trace side label altered",
                mutate_row(
                    "occurrence_trace_record_rows",
                    0,
                    lambda row: row.__setitem__("side_label", "inside"),
                ),
            ),
            (
                "trace collision time altered",
                mutate_row(
                    "occurrence_trace_record_rows",
                    0,
                    lambda row: row.__setitem__("collision_index", 2),
                ),
            ),
            (
                "plaque field qualifier promoted",
                mutate_row(
                    "field_materialization_status_rows",
                    8,
                    lambda row: row.__setitem__(
                        "qualifier", "canonical stable plaque side"
                    ),
                ),
            ),
            (
                "word field qualifier promoted",
                mutate_row(
                    "field_materialization_status_rows",
                    9,
                    lambda row: row.__setitem__(
                        "qualifier", "official return-path word"
                    ),
                ),
            ),
            (
                "owner field marked exact",
                mutate_row(
                    "field_materialization_status_rows",
                    6,
                    lambda row: (
                        row.__setitem__(
                            "source_side_status",
                            "MATERIALIZED_EXACT_WITH_TYPED_QUALIFIER",
                        ),
                        row.__setitem__("materialized_record_count", 64),
                    ),
                ),
            ),
            (
                "plaque field marked usable for join",
                mutate_row(
                    "field_materialization_status_rows",
                    8,
                    lambda row: row.__setitem__(
                        "usable_as_joined_Round67_to_path_key", True
                    ),
                ),
            ),
            ("typed incidence match invented", invent_match),
            (
                "owner obstruction count altered",
                mutate_row(
                    "obstruction_rows",
                    0,
                    lambda row: row.__setitem__("materialized_owner_key_count", 1),
                ),
            ),
            (
                "first possible depth reduced",
                mutate_row(
                    "obstruction_rows",
                    1,
                    lambda row: row.__setitem__("first_unruled_out_depth", "n>=1"),
                ),
            ),
            (
                "exact-map obstruction erased",
                mutate_row(
                    "obstruction_rows",
                    2,
                    lambda row: row.__setitem__("materialized_exact_map_count", 1),
                ),
            ),
            (
                "terminal-preimage mismatch erased",
                mutate_row(
                    "obstruction_rows",
                    3,
                    lambda row: row.__setitem__("direct_typed_match_count", 1),
                ),
            ),
            (
                "face count ledger altered",
                simple(
                    ("result", "count_ledger", "Round28_rebuilt_occurrence_face_count"),
                    63,
                ),
            ),
            (
                "source exact ledger promoted",
                simple(
                    (
                        "result",
                        "count_ledger",
                        "source_side_exact_required_field_count",
                    ),
                    12,
                ),
            ),
            (
                "owner count promoted",
                simple(("result", "count_ledger", "owner_key_count"), 64),
            ),
            (
                "owned record count promoted",
                simple(
                    (
                        "result",
                        "count_ledger",
                        "Round67_owned_Omega_j_record_count",
                    ),
                    64,
                ),
            ),
            (
                "exact map count promoted",
                simple(
                    (
                        "result",
                        "count_ledger",
                        "exact_endpoint_root_to_s_t_p_map_count",
                    ),
                    64,
                ),
            ),
            (
                "source status promoted",
                simple(
                    (
                        "result",
                        "Round67_twelve_field_source_materialization",
                        "source_side_status",
                    ),
                    "12/12",
                ),
            ),
            (
                "joined status promoted",
                simple(
                    (
                        "result",
                        "Round67_twelve_field_source_materialization",
                        "joined_to_owner_or_path_status",
                    ),
                    "9/12",
                ),
            ),
            (
                "terminal preimages allowed as substitute",
                simple(
                    (
                        "result",
                        "next_required_object",
                        "Round71_Round72_terminal_preimage_rows_may_substitute_for_second_step",
                    ),
                    True,
                ),
            ),
            (
                "Round67 safety owner count promoted",
                simple(("result", "global_safety", "Round67_owned_record_count"), 64),
            ),
            (
                "Round67 path match promoted",
                simple(
                    (
                        "result",
                        "global_safety",
                        "Round67_to_path_typed_incidence_match_count",
                    ),
                    1,
                ),
            ),
            (
                "Round72 fields promoted",
                simple(
                    (
                        "result",
                        "global_safety",
                        "Round72_numeric_fields_promoted_to_Round67_root",
                    ),
                    True,
                ),
            ),
            (
                "global complete block invented",
                simple(
                    ("result", "global_safety", "global_complete_18_field_block_count"),
                    1,
                ),
            ),
            (
                "complete block invented",
                simple(
                    ("result", "global_safety", "complete_18_field_block_count"),
                    1,
                ),
            ),
            (
                "Gate5 block invented",
                simple(("result", "global_safety", "gate5_block_count"), 1),
            ),
            (
                "Gate5 maturity promoted",
                simple(("result", "global_safety", "gate5_global_maturity"), "18/18"),
            ),
            (
                "Gate5 status promoted",
                simple(("result", "global_safety", "gate5_status"), "CERTIFIED"),
            ),
            (
                "CM2 promoted",
                simple(("result", "global_safety", "CM2"), "GO_FOR_CLAIM"),
            ),
            (
                "strict nonclaim deleted",
                lambda document: (
                    document["result"]["strict_nonclaims"].pop(),
                    resign(document),
                ),
            ),
            (
                "unknown result key added",
                lambda document: (
                    document["result"].__setitem__("unknown", True),
                    resign(document),
                ),
            ),
        ]
    )

    rejected: list[str] = []
    for label, mutation in mutations:
        candidate = copy.deepcopy(certificate)
        mutation(candidate)
        try:
            evaluate_document(candidate, expected)
        except (VerificationError, KeyError, IndexError, TypeError, ValueError):
            rejected.append(label)
        else:
            raise VerificationError(f"semantic mutation accepted:{label}")
    return rejected


def strict_json_attacks(
    certificate: dict[str, Any],
    expected: dict[str, Any],
) -> list[str]:
    raw = canonical(certificate).encode("utf-8")
    status = (
        b'"status":"CERTIFIED_64_OCCURRENCE_SOURCE_RECORDS_128_TRACES__'
        b'OWNER_AND_TYPED_INCIDENCE_OPEN"'
    )
    attacks: list[tuple[str, bytes]] = [
        (
            "duplicate top-level schema key",
            raw.replace(b'{"result":', b'{"schema":"duplicate","result":', 1),
        ),
        (
            "duplicate nested status key",
            raw.replace(status, b'"status":"duplicate",' + status, 1),
        ),
        (
            "floating-point count",
            raw.replace(
                b'"finite_Round132_row_count":208',
                b'"finite_Round132_row_count":208.0',
                1,
            ),
        ),
        (
            "NaN constant",
            raw.replace(
                b'"finite_Round132_row_count":208',
                b'"finite_Round132_row_count":NaN',
                1,
            ),
        ),
        (
            "positive Infinity",
            raw.replace(
                b'"finite_Round132_row_count":208',
                b'"finite_Round132_row_count":Infinity',
                1,
            ),
        ),
        (
            "negative Infinity",
            raw.replace(
                b'"finite_Round132_row_count":208',
                b'"finite_Round132_row_count":-Infinity',
                1,
            ),
        ),
        ("UTF-8 BOM", b"\xef\xbb\xbf" + raw),
        ("invalid UTF-8", raw[:-1] + b"\xff}"),
        ("top-level array", b"[]"),
        ("top-level null", b"null"),
        ("trailing second document", raw + b"{}"),
        (
            "oversized integer",
            raw.replace(
                b'"finite_Round132_row_count":208',
                b'"finite_Round132_row_count":' + b"9" * 5000,
                1,
            ),
        ),
        (
            "negative zero",
            raw.replace(
                b'"finite_Round132_row_count":208',
                b'"finite_Round132_row_count":-0',
                1,
            ),
        ),
        (
            "leading-zero integer",
            raw.replace(
                b'"finite_Round132_row_count":208',
                b'"finite_Round132_row_count":0208',
                1,
            ),
        ),
        (
            "unpaired surrogate",
            raw.replace(
                b'"schema":"cm2.round132.round28-occurrence-record-materialization.v1"',
                b'"schema":"\\ud800"',
                1,
            ),
        ),
    ]
    extra_top = copy.deepcopy(certificate)
    extra_top["unknown"] = True
    attacks.append(
        ("closed envelope extra key", canonical(extra_top).encode("utf-8"))
    )
    extra_result = copy.deepcopy(certificate)
    extra_result["result"]["unknown"] = True
    resign(extra_result)
    attacks.append(
        ("closed result extra key", canonical(extra_result).encode("utf-8"))
    )
    stale = copy.deepcopy(certificate)
    stale["result"]["status"] = "tampered"
    attacks.append(
        ("stale outer result digest", canonical(stale).encode("utf-8"))
    )

    rejected: list[str] = []
    for label, attack in attacks:
        try:
            document = strict_json_bytes(attack, label)
            evaluate_document(document, expected)
        except (VerificationError, KeyError, IndexError, TypeError, ValueError):
            rejected.append(label)
        else:
            raise VerificationError(f"strict JSON attack accepted:{label}")
    return rejected


def build_verification(
    certificate: dict[str, Any],
    expected: dict[str, Any],
    mutations: list[str],
    strict_attacks: list[str],
) -> dict[str, Any]:
    result = {
        "status": "PASS",
        "producer_sha256": PRODUCER_SHA256,
        "certificate_sha256": CERTIFICATE_SHA256,
        "certificate_result_sha256": CERTIFICATE_RESULT_SHA256,
        "certificate_schema": CERTIFICATE_SCHEMA,
        "verifier_sha256": sha256_path(VERIFIER),
        "independence_contract": {
            "Round132_producer_imported": False,
            "Round132_producer_executed": False,
            "three_pinned_lower_level_source_constructions_replayed": True,
            "Round28_full_face_registry_digest_independently_recovered": True,
            "all_64_occurrence_face_records_independently_reconstructed": True,
            "all_128_oriented_trace_records_independently_reconstructed": True,
            "all_208_Round132_rows_independently_reconstructed": True,
        },
        "replay_audit": {
            "occurrence_face_record_count": 64,
            "oriented_trace_record_count": 128,
            "hit_trace_count": 64,
            "miss_trace_count": 64,
            "required_field_count": 12,
            "source_side_exact_with_typed_qualifier_count": 9,
            "source_side_missing_count": 3,
            "joined_owner_or_path_field_count": 0,
            "Round67_owner_key_count": 0,
            "Round67_owned_Omega_j_record_count": 0,
            "occurrence_pullback_component_count": 0,
            "exact_endpoint_root_to_s_t_p_map_count": 0,
            "typed_incidence_match_count": 0,
            "obstruction_row_count": 4,
            "finite_row_count": 208,
            "row_group_counts": [64, 128, 12, 0, 4],
            "all_row_group_and_outer_hashes_rebuilt": True,
            "plaque_side_is_only_oriented_hit_miss_qualifier": True,
            "word_cell_is_not_official_return_path_word": True,
            "first_unruled_out_occurrence_pullback_depth": "n>=2",
        },
        "semantic_mutation_test_count": len(mutations),
        "semantic_mutation_rejection_labels": mutations,
        "strict_json_attack_count": len(strict_attacks),
        "strict_json_attack_rejection_labels": strict_attacks,
        "determinism_contract": {
            "canonical_JSON_sort_keys": True,
            "no_hash_iteration_controls_output": True,
            "verification_replay_is_PYTHONHASHSEED_independent": True,
        },
        "safety": {
            "Round67_owned_record_count": 0,
            "Round67_to_path_typed_incidence_match_count": 0,
            "global_complete_18_field_block_count": 0,
            "complete_18_field_block_count": 0,
            "gate5_block_count": 0,
            "gate5_global_maturity": "10/18",
            "Gate5": "NOT_CERTIFIED",
            "CM2": "NO-GO_FOR_CLAIM",
        },
    }
    require(certificate["result"] == expected, "valid certificate equality")
    return {
        "schema": VERIFICATION_SCHEMA,
        "result": result,
        "result_sha256": digest(result),
    }


def safe_input_path(path: Path) -> Path:
    expanded = path.expanduser()
    require(expanded.exists(), "certificate missing")
    require(not expanded.is_symlink(), "certificate must not be a symlink")
    metadata = expanded.lstat()
    require(stat.S_ISREG(metadata.st_mode), "certificate must be regular")
    require(metadata.st_nlink == 1, "certificate must not have hardlinks")
    return expanded.resolve()


def safe_output_path(path: Path, certificate_path: Path) -> Path:
    expanded = path.expanduser()
    protected = {
        VERIFIER,
        PRODUCER.resolve(),
        CERTIFICATE.resolve(),
        certificate_path.resolve(),
        *((HERE / name).resolve() for name in BYTE_PINS),
    }
    require(not expanded.is_symlink(), "output must not be a symlink")
    if expanded.exists():
        metadata = expanded.lstat()
        require(stat.S_ISREG(metadata.st_mode), "existing output must be regular")
        require(metadata.st_nlink == 1, "existing output must not have hardlinks")
        for item in protected:
            try:
                require(
                    not os.path.samefile(expanded, item),
                    "output aliases protected input",
                )
            except FileNotFoundError:
                pass
    resolved = expanded.resolve()
    require(resolved not in protected, "output overwrites protected input")
    require(resolved.parent.is_dir(), "output parent directory")
    return resolved


def write_document(path: Path, document: dict[str, Any]) -> None:
    payload = (
        json.dumps(
            document,
            sort_keys=True,
            indent=2,
            ensure_ascii=False,
            allow_nan=False,
        )
        + "\n"
    )
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=f".{path.name}.tmp-",
        dir=path.parent,
        text=True,
    )
    temporary = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as stream:
            stream.write(payload)
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
    parser.add_argument("--certificate", type=Path, default=CERTIFICATE)
    parser.add_argument("--output", type=Path, default=OUTPUT)
    args = parser.parse_args()
    try:
        certificate_path = safe_input_path(args.certificate)
        raw = certificate_path.read_bytes()
        require(sha256_bytes(raw) == CERTIFICATE_SHA256, "certificate byte pin")
        certificate = strict_json_bytes(raw, certificate_path.name)
        expected = build_expected(check_files=True)
        evaluate_document(certificate, expected)
        mutations = semantic_mutations(certificate, expected)
        attacks = strict_json_attacks(certificate, expected)
        verification = build_verification(certificate, expected, mutations, attacks)
        output = safe_output_path(args.output, certificate_path)
        write_document(output, verification)
        print(
            canonical(
                {
                    "output": str(output),
                    "semantic_mutations": len(mutations),
                    "status": "PASS",
                    "strict_json_attacks": len(attacks),
                }
            )
        )
        return 0
    except (
        VerificationError,
        OSError,
        ValueError,
        KeyError,
        IndexError,
        TypeError,
        ArithmeticError,
    ) as exc:
        print(f"VerificationError: {exc}", file=os.sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
