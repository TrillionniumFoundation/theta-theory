#!/usr/bin/env python3
"""Promote the exhaustive Round292 signed-face classification to edge evidence.

Round299 established an exact, zero-credit classification of all 43,092
same-chart, same-physical-t-sign coordinate face contacts between the 11,852
Round292 refinement cells.  This producer byte-pins that classification and
promotes precisely the accepted nonself witnesses to canonical occurrence
component edges.

The promotion is deliberately narrow.  It does not collapse occurrence
identities, apply a DSU, claim a quotient, prove maximality, or issue fibre or
global-disposition credit.
"""

from __future__ import annotations

from collections import Counter, defaultdict
import argparse
import copy
from fractions import Fraction as Q
import gzip
import hashlib
import io
import json
import os
from pathlib import Path
import stat
import tempfile
from typing import Any, Callable


HERE = Path(__file__).resolve().parent
PREFIX = "cm2_round299c_source_g_r292_signed_support_face_edge_promotion"

CLASSIFICATION_LEDGER = HERE / f"{PREFIX}_classification_inventory.json.gz"
RAW_EDGE_LEDGER = HERE / f"{PREFIX}_accepted_nonself_raw_edge_witnesses.json.gz"
CANONICAL_EDGE_LEDGER = HERE / f"{PREFIX}_canonical_occurrence_edge_pairs.json.gz"
NO_EDGE_LEDGER = HERE / f"{PREFIX}_self_and_exclusion.json.gz"
ATTACK_SUITE = HERE / f"{PREFIX}_attack_suite.json"
RESULT = HERE / f"{PREFIX}_result.json"

SCHEMA = "cm2.round299c.source-g-r292-signed-support-face-edge-promotion.v1"

SOURCE_PROBE = (
    "cm2_round299_source_g_r292_signed_support_face_classifier_"
    "independent_probe.py"
)
SOURCE_LEDGER = (
    "cm2_round299_source_g_r292_signed_support_face_classifier_"
    "independent_probe_ledger.json.gz"
)
SOURCE_RESULT = (
    "cm2_round299_source_g_r292_signed_support_face_classifier_"
    "independent_probe_result.json"
)

DIRECT_INPUT_PINS = {
    SOURCE_PROBE:
        "d6cae0b9ede704b7da57fd9c37b8097919e01592482a8a0eee63fd4a27178b24",
    SOURCE_LEDGER:
        "9797d486eaf96ce8352883093c24637b5eb9cb27af60fd79e5ee03a6585d27a9",
    SOURCE_RESULT:
        "07427f743ace170d6d7d832c67658d8d27eca2d51092049625c117abfc8efcdb",
}

EXPECTED_INHERITED_PINS = {
    "cm2_round174_source_g_unique_first_dynamic_occurrence_materialization.py":
        "3d329525dda6697a3a5d2a8227c94bd9c309ea7ebcc4cdd0c7fbe573c267a218",
    "cm2_round179_source_g_residual_tube_arrangement.py":
        "8c568c58d82708a7ab549f126c1fcedfccff563d1d00e3c1f7e6545b4b0d29ab",
    "cm2_round274_source_g_reverse_rechart_tail_arrangement_probe.py":
        "677813e132d62732900a26edc3fae5d562049d8d1fac2cea59f7c65d41735292",
    "cm2_round275_source_g_complete_reverse_rechart_materialization_certificate.json":
        "e18935169614fc8b62ead3be7f60b383396ea1d2c52e8151457241f49e770386",
    "cm2_round287_source_g_rechart_terminal_occurrence_disposition_probe.py":
        "b39849e3aee21688ccf3eb5443984e9e0e8d7a88ed2d61e059ed3485d84c780d",
    "cm2_round287_source_g_rechart_terminal_occurrence_disposition_probe_ledger.json.gz":
        "29838e3e6b33f03bf623bbce8b87e6ba5c3306e66beb0b6634496503fb9a4f9a",
    "cm2_round292_source_g_r287_registry_overlap_exhaustion_probe_ledger.json.gz":
        "8863126e88ffd30438938d0a8bdb577f5928ae81f3f17f4b506829d59103a8ab",
    "cm2_round294_source_g_occurrence_registry_atomic_promotion_registry_ledger.json.gz":
        "c6b26f13e90072db99fa98f99fc62c77135ff1cbdb23bbbd5bac3e9f64a834bb",
    "cm2_round295a_source_g_r291_positive_t_retained_continuation_closure_physical_witness_incidence_binding_ledger.json.gz":
        "2d9addfc9fca55366a58b29a7084c063674c3f556dd5398b038ae7d51fe97dcf",
    "cm2_round296_source_g_true_seam_occurrence_edge_ledger_closure_edge_ledger.json.gz":
        "1b57b10fac9317e1609fb8858972011165bd95e5b1b687604edd6c8ad7139ef7",
    "cm2_round297_source_g_ordinary_face_occurrence_edge_promotion_edge_ledger.json.gz":
        "18a20b4679a8a3e94ccaf1b511694220cad1bc92e1590ded4585ae3735547371",
}

ACCEPT = (
    "ACCEPT_STRICT_POSITIVE_AREA_FACE_PATCH_AND_TWO_SIDED_CORRIDOR"
)
REJECT = "REJECT_NO_COMMON_POSITIVE_AREA_SIGNED_FACE_PATCH"
SOURCE_STATUS = "PASS_ZERO_CREDIT__ALL_43092_SIGNED_FACE_CONTACTS_CLASSIFIED"

FORMAL_ZERO_FIELDS = (
    "formal_occurrence_identity_collapse_credit",
    "formal_DSU_rank_reduction_credit",
    "formal_maximality_credit",
    "formal_fibre_credit",
    "formal_global_disposition_credit",
)


class BuildError(RuntimeError):
    pass


def need(condition: bool, message: str) -> None:
    if not condition:
        raise BuildError(message)


def canonical(value: Any) -> bytes:
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=True
    ).encode()


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def file_sha256(path: Path) -> str:
    result = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1 << 20), b""):
            result.update(chunk)
    return result.hexdigest()


def close(payload: dict[str, Any]) -> dict[str, Any]:
    row = dict(payload)
    row["row_sha256"] = digest(payload)
    return row


def verify_closed(row: dict[str, Any], label: str) -> None:
    payload = {key: value for key, value in row.items() if key != "row_sha256"}
    need(
        set(row) == set(payload) | {"row_sha256"}
        and row["row_sha256"] == digest(payload),
        label + ":row closure",
    )


def reject_duplicate_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise BuildError("duplicate JSON key:" + key)
        result[key] = value
    return result


def guarded_input(filename: str, expected_sha256: str) -> Path:
    path = HERE / filename
    need(
        path.name == filename
        and path.parent == HERE
        and not path.is_symlink(),
        "confined non-symlink input:" + filename,
    )
    try:
        status = os.lstat(path)
    except FileNotFoundError as error:
        raise BuildError("missing input:" + filename) from error
    need(
        stat.S_ISREG(status.st_mode)
        and status.st_nlink == 1
        and path.resolve(strict=True).parent == HERE.resolve(strict=True),
        "regular single-link input:" + filename,
    )
    need(file_sha256(path) == expected_sha256, "byte pin:" + filename)
    return path


def read_json_bytes(path: Path) -> tuple[dict[str, Any], bytes]:
    raw = path.read_bytes()
    value = json.loads(
        raw.decode("ascii"), object_pairs_hook=reject_duplicate_pairs
    )
    need(isinstance(value, dict), path.name + ":JSON object")
    need(raw == canonical(value) + b"\n", path.name + ":canonical JSON")
    return value, raw


def read_gzip_json_bytes(path: Path) -> tuple[dict[str, Any], bytes]:
    raw = path.read_bytes()
    with gzip.GzipFile(fileobj=io.BytesIO(raw), mode="rb") as stream:
        decoded = stream.read()
    value = json.loads(
        decoded.decode("ascii"), object_pairs_hook=reject_duplicate_pairs
    )
    need(isinstance(value, dict), path.name + ":gzip JSON object")
    need(decoded == canonical(value), path.name + ":canonical payload")
    need(
        raw == deterministic_gzip_bytes(value),
        path.name + ":deterministic single-member gzip",
    )
    return value, raw


def deterministic_gzip_bytes(value: Any) -> bytes:
    target = io.BytesIO()
    with gzip.GzipFile(
        filename="",
        mode="wb",
        fileobj=target,
        compresslevel=9,
        mtime=0,
    ) as stream:
        stream.write(canonical(value))
    return target.getvalue()


def atomic(path: Path, payload: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary = tempfile.mkstemp(
        prefix="." + path.name + ".", dir=path.parent
    )
    try:
        with os.fdopen(descriptor, "wb") as stream:
            stream.write(payload)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def qbox(value: Any, label: str) -> tuple[Q, ...]:
    need(isinstance(value, list) and len(value) == 6, label + ":six bounds")
    result = tuple(Q(item) for item in value)
    for axis in range(3):
        need(
            result[2 * axis] <= result[2 * axis + 1],
            label + ":ordered bounds",
        )
    return result


def area(box: tuple[Q, ...], axis: int) -> Q:
    result = Q(1)
    for child_axis in range(3):
        if child_axis != axis:
            result *= box[2 * child_axis + 1] - box[2 * child_axis]
    return result


def volume(box: tuple[Q, ...]) -> Q:
    result = Q(1)
    for axis in range(3):
        result *= box[2 * axis + 1] - box[2 * axis]
    return result


def validate_corridor(
    corridor: Any,
    patch: tuple[Q, ...],
    axis: int,
    left: bool,
    label: str,
) -> None:
    need(isinstance(corridor, dict), label + ":corridor object")
    box = qbox(
        corridor["exact_positive_volume_transformed_corridor"],
        label + ":box",
    )
    for tangent in range(3):
        if tangent != axis:
            need(
                box[2 * tangent:2 * tangent + 2]
                == patch[2 * tangent:2 * tangent + 2],
                label + ":exact patch tangential footprint",
            )
    coordinate = patch[2 * axis]
    if left:
        need(
            box[2 * axis] < box[2 * axis + 1] == coordinate,
            label + ":strict left inward interval",
        )
    else:
        need(
            coordinate == box[2 * axis] < box[2 * axis + 1],
            label + ":strict right inward interval",
        )
    need(
        volume(box) > 0
        and Q(corridor["exact_transformed_corridor_volume"]) == volume(box),
        label + ":exact positive volume",
    )
    certificates = corridor["t_boundary_sqrt_enclosure_certificates"]
    need(
        corridor["t_boundary_sqrt_enclosures_sha256"]
        == digest(certificates),
        label + ":sqrt-certificate digest",
    )
    trace = corridor["dyadic_inward_shrink_trace"]
    need(
        trace
        and corridor["dyadic_inward_shrink_trace_sha256"] == digest(trace),
        label + ":nonempty closed shrink trace",
    )
    replay = corridor["signed_support_replay"]
    if replay is None:
        need(
            corridor["support_basis"]
            == "INHERITED_R287_FULL_SIGNED_SUPPORT",
            label + ":FULL support basis",
        )
    else:
        need(
            corridor["support_basis"]
            == "R287_ACTIVE_FACTOR_STRICT_CORRIDOR_REPLAY"
            and replay["signed_support_state"]
            == "FULL_DESIRED_SIDE_SUPPORT",
            label + ":strict active-factor corridor replay",
        )


def validate_classification_row(row: dict[str, Any], label: str) -> None:
    axis = row["common_face_axis"]
    need(axis in (0, 1, 2), label + ":face axis")
    face = qbox(
        row["exact_positive_area_transformed_coordinate_face"],
        label + ":face",
    )
    need(
        face[2 * axis] == face[2 * axis + 1]
        and area(face, axis) > 0
        and Q(row["exact_transformed_coordinate_face_area"])
        == area(face, axis),
        label + ":exact positive-area coordinate face",
    )
    need(
        row["common_face_t_boundary_sqrt_enclosures_sha256"]
        == digest(row["common_face_t_boundary_sqrt_enclosure_certificates"]),
        label + ":face sqrt-certificate digest",
    )
    left_id = row["left_formal_occurrence_id"]
    right_id = row["right_formal_occurrence_id"]
    same = left_id == right_id
    pair = row["unordered_nonself_formal_occurrence_endpoint_pair"]
    need(
        row["same_formal_occurrence_endpoint"] is same,
        label + ":self endpoint flag",
    )
    if same:
        need(pair is None, label + ":self has no endpoint pair")
    else:
        need(
            pair == sorted([left_id, right_id])
            and pair[0] != pair[1],
            label + ":canonical nonself endpoint pair",
        )
    accepted = row["decision"] == ACCEPT
    rejected = row["decision"] == REJECT
    need(accepted ^ rejected, label + ":closed binary classification")
    need(
        row["diagnostic_nonself_component_edge_candidate"]
        == int(accepted and not same),
        label + ":diagnostic candidate flag",
    )
    need(
        row["formal_component_edge_credit"] == 0
        and all(row[field] == 0 for field in FORMAL_ZERO_FIELDS),
        label + ":source classification is zero credit",
    )

    left_factor = row["left_active_factor_descriptor"]
    right_factor = row["right_active_factor_descriptor"]
    contact_class = row["contact_class"]
    if contact_class == "FULL_FULL":
        need(
            left_factor is None and right_factor is None,
            label + ":FULL/FULL descriptors",
        )
    elif contact_class == "SINGLE_GRAPH":
        need(
            (left_factor is None) ^ (right_factor is None),
            label + ":single graph descriptor",
        )
    elif contact_class.startswith("DOUBLE_GRAPH_SAME_FACTOR_"):
        need(
            isinstance(left_factor, dict)
            and isinstance(right_factor, dict)
            and left_factor["active_function_id"]
            == right_factor["active_function_id"],
            label + ":same mathematical active factor",
        )
        same_side = (
            left_factor["desired_side_sign"]
            == right_factor["desired_side_sign"]
        )
        need(
            same_side
            == contact_class.endswith("SAME_SIDE"),
            label + ":factor side relation",
        )
    else:
        raise BuildError(label + ":unexpected contact class")

    if accepted:
        patch = qbox(row["accepted_patch"], label + ":accepted patch")
        need(
            patch[2 * axis] == patch[2 * axis + 1]
            == face[2 * axis],
            label + ":patch lies on face plane",
        )
        for tangent in range(3):
            if tangent != axis:
                need(
                    face[2 * tangent] <= patch[2 * tangent]
                    < patch[2 * tangent + 1] <= face[2 * tangent + 1],
                    label + ":strict positive tangential patch",
                )
        need(
            area(patch, axis) > 0
            and Q(row["accepted_patch_area"]) == area(patch, axis),
            label + ":exact positive patch area",
        )
        need(
            row["exclusion_evidence"] is None,
            label + ":accepted row has no exclusion",
        )
        validate_corridor(
            row["left_corridor"], patch, axis, True, label + ":left"
        )
        validate_corridor(
            row["right_corridor"], patch, axis, False, label + ":right"
        )
    else:
        need(
            row["accepted_patch"] is None
            and row["left_corridor"] is None
            and row["right_corridor"] is None,
            label + ":rejected row has no accepted geometry",
        )
        exclusion = row["exclusion_evidence"]
        need(
            isinstance(exclusion, dict)
            and exclusion["positive_area_common_strict_trace_possible"]
            is False,
            label + ":exact exclusion evidence",
        )


def validate_source(
    ledger: dict[str, Any],
    result: dict[str, Any],
) -> list[dict[str, Any]]:
    need(ledger["status"] == SOURCE_STATUS, "source ledger pass status")
    need(result["status"] == SOURCE_STATUS, "source result pass status")
    result_payload = {
        key: value for key, value in result.items() if key != "result_sha256"
    }
    need(
        result["result_sha256"] == digest(result_payload),
        "source result self digest",
    )
    need(
        result["input_file_pins"] == EXPECTED_INHERITED_PINS,
        "complete inherited input pins",
    )
    need(
        result["ledger"]["file_sha256"] == DIRECT_INPUT_PINS[SOURCE_LEDGER],
        "source ledger result pin",
    )
    rows = ledger["rows"]
    need(
        ledger["row_count"] == len(rows) == 43_092
        and ledger["rows_sha256"] == digest(rows),
        "source row count and digest",
    )
    ids = [
        row["Round299_independent_signed_face_classification_row_id"]
        for row in rows
    ]
    need(
        ids == sorted(ids)
        and len(ids) == len(set(ids))
        and ledger["row_ids_sha256"] == digest(ids),
        "source ordered unique row IDs",
    )
    need(
        ledger["row_hashes_sha256"]
        == digest([row["row_sha256"] for row in rows]),
        "source row-hash digest",
    )
    for index, row in enumerate(rows):
        label = f"source row {index}"
        verify_closed(row, label)
        validate_classification_row(row, label)

    decisions = Counter(row["decision"] for row in rows)
    classes = Counter(row["contact_class"] for row in rows)
    class_decisions = Counter(
        row["contact_class"] + "|" + row["decision"] for row in rows
    )
    need(
        decisions == {ACCEPT: 29_948, REJECT: 13_144},
        "source decision census",
    )
    need(
        classes == {
            "FULL_FULL": 16_828,
            "SINGLE_GRAPH": 9_576,
            "DOUBLE_GRAPH_SAME_FACTOR_SAME_SIDE": 8_344,
            "DOUBLE_GRAPH_SAME_FACTOR_OPPOSITE_SIDE": 8_344,
        },
        "source contact-class census",
    )
    need(
        class_decisions == {
            "FULL_FULL|" + ACCEPT: 16_828,
            "SINGLE_GRAPH|" + ACCEPT: 4_788,
            "SINGLE_GRAPH|" + REJECT: 4_788,
            "DOUBLE_GRAPH_SAME_FACTOR_SAME_SIDE|" + ACCEPT: 8_332,
            "DOUBLE_GRAPH_SAME_FACTOR_SAME_SIDE|" + REJECT: 12,
            "DOUBLE_GRAPH_SAME_FACTOR_OPPOSITE_SIDE|" + REJECT: 8_344,
        },
        "source class/decision census",
    )
    census = result["census"]
    need(
        census["unresolved_face_contact_count"] == 0
        and census["accepted_nonself_raw_component_edge_candidate_count"]
        == 27_856
        and census["accepted_distinct_nonself_occurrence_pair_count"]
        == 25_452
        and census["accepted_self_endpoint_physical_patch_count"] == 2_092
        and census["rejected_raw_face_contact_count"] == 13_144
        and census["accepted_pair_existing_channel_intersection_count"]
        == {"R295A_LOWER": 0, "R296_TRUE_SEAM": 0, "R297_ORDINARY": 0},
        "source promotion census",
    )
    return rows


def raw_edge_row(source: dict[str, Any]) -> dict[str, Any]:
    source_id = source[
        "Round299_independent_signed_face_classification_row_id"
    ]
    endpoint_pair = source[
        "unordered_nonself_formal_occurrence_endpoint_pair"
    ]
    payload = {
        "Round299C_signed_face_raw_edge_witness_row_id":
            "round299c-signed-face-raw-edge:" + digest(source_id),
        "source_Round299_classification_row_id": source_id,
        "source_Round299_classification_row_sha256": source["row_sha256"],
        "unordered_formal_occurrence_endpoint_pair": endpoint_pair,
        "left_formal_occurrence_id": source["left_formal_occurrence_id"],
        "right_formal_occurrence_id": source["right_formal_occurrence_id"],
        "endpoint_pair_kind": source["endpoint_pair_kind"],
        "source_chart": source["source_chart"],
        "physical_t_sign": source["physical_t_sign"],
        "common_face_axis": source["common_face_axis"],
        "contact_class": source["contact_class"],
        "decision_reason": source["decision_reason"],
        "exact_positive_area_transformed_coordinate_face":
            source["exact_positive_area_transformed_coordinate_face"],
        "accepted_patch": source["accepted_patch"],
        "accepted_patch_area": source["accepted_patch_area"],
        "accepted_patch_t_boundary_sqrt_enclosure_certificates":
            source["accepted_patch_t_boundary_sqrt_enclosure_certificates"],
        "left_strict_positive_volume_corridor": source["left_corridor"],
        "right_strict_positive_volume_corridor": source["right_corridor"],
        "left_active_factor_descriptor":
            source["left_active_factor_descriptor"],
        "right_active_factor_descriptor":
            source["right_active_factor_descriptor"],
        "formal_component_edge_witness_credit": 1,
        "formal_component_edge_credit": 0,
        "formal_occurrence_identity_collapse_credit": 0,
        "formal_DSU_rank_reduction_credit": 0,
        "formal_maximality_credit": 0,
        "formal_fibre_credit": 0,
        "formal_global_disposition_credit": 0,
    }
    return close(payload)


def validate_raw_edge(row: dict[str, Any], label: str) -> None:
    pair = row["unordered_formal_occurrence_endpoint_pair"]
    need(
        isinstance(pair, list)
        and len(pair) == 2
        and pair == sorted(pair)
        and pair[0] != pair[1],
        label + ":canonical nonself pair",
    )
    need(
        row["formal_component_edge_witness_credit"] == 1
        and row["formal_component_edge_credit"] == 0
        and all(row[field] == 0 for field in FORMAL_ZERO_FIELDS),
        label + ":raw witness-only credit",
    )
    axis = row["common_face_axis"]
    patch = qbox(row["accepted_patch"], label + ":patch")
    need(
        area(patch, axis) > 0
        and Q(row["accepted_patch_area"]) == area(patch, axis),
        label + ":positive-area patch",
    )
    validate_corridor(
        row["left_strict_positive_volume_corridor"],
        patch,
        axis,
        True,
        label + ":left",
    )
    validate_corridor(
        row["right_strict_positive_volume_corridor"],
        patch,
        axis,
        False,
        label + ":right",
    )


def canonical_edge_row(
    endpoint_pair: tuple[str, str],
    witnesses: list[dict[str, Any]],
    rejected_sources: list[dict[str, Any]],
) -> dict[str, Any]:
    raw_ids = sorted(
        row["Round299C_signed_face_raw_edge_witness_row_id"]
        for row in witnesses
    )
    source_ids = sorted(
        row["source_Round299_classification_row_id"] for row in witnesses
    )
    rejected_ids = sorted(
        row["Round299_independent_signed_face_classification_row_id"]
        for row in rejected_sources
    )
    payload = {
        "Round299C_canonical_signed_face_occurrence_edge_row_id":
            "round299c-canonical-signed-face-edge:"
            + digest(list(endpoint_pair)),
        "unordered_formal_occurrence_endpoint_pair": list(endpoint_pair),
        "accepted_raw_edge_witness_count": len(witnesses),
        "accepted_raw_edge_witness_row_ids": raw_ids,
        "accepted_raw_edge_witness_row_ids_sha256": digest(raw_ids),
        "source_accept_classification_row_ids": source_ids,
        "source_accept_classification_row_ids_sha256": digest(source_ids),
        "source_reject_face_row_count_for_same_endpoint_pair":
            len(rejected_ids),
        "source_reject_face_row_ids_for_same_endpoint_pair": rejected_ids,
        "source_reject_face_row_ids_for_same_endpoint_pair_sha256":
            digest(rejected_ids),
        "pair_acceptance_semantics":
            "EXISTS_STRICT_POSITIVE_AREA_PATCH_WITH_TWO_SIDED_CORRIDOR",
        "a_rejected_face_does_not_negate_an_accepted_face_for_same_pair":
            True,
        "formal_component_edge_credit": 1,
        "formal_occurrence_identity_collapse_credit": 0,
        "formal_DSU_rank_reduction_credit": 0,
        "formal_maximality_credit": 0,
        "formal_fibre_credit": 0,
        "formal_global_disposition_credit": 0,
    }
    return close(payload)


def validate_canonical_edge(row: dict[str, Any], label: str) -> None:
    pair = row["unordered_formal_occurrence_endpoint_pair"]
    accepted = row["accepted_raw_edge_witness_row_ids"]
    rejected = row["source_reject_face_row_ids_for_same_endpoint_pair"]
    need(
        pair == sorted(pair) and len(pair) == 2 and pair[0] != pair[1],
        label + ":canonical nonself endpoint pair",
    )
    need(
        accepted == sorted(set(accepted))
        and len(accepted) == row["accepted_raw_edge_witness_count"] > 0
        and row["accepted_raw_edge_witness_row_ids_sha256"]
        == digest(accepted),
        label + ":accepted witness inventory",
    )
    source_ids = row["source_accept_classification_row_ids"]
    need(
        source_ids == sorted(set(source_ids))
        and len(source_ids) == len(accepted)
        and row["source_accept_classification_row_ids_sha256"]
        == digest(source_ids),
        label + ":source accept inventory",
    )
    need(
        rejected == sorted(set(rejected))
        and len(rejected)
        == row["source_reject_face_row_count_for_same_endpoint_pair"]
        and row["source_reject_face_row_ids_for_same_endpoint_pair_sha256"]
        == digest(rejected),
        label + ":coexisting reject-face inventory",
    )
    need(
        row["pair_acceptance_semantics"]
        == "EXISTS_STRICT_POSITIVE_AREA_PATCH_WITH_TWO_SIDED_CORRIDOR"
        and row[
            "a_rejected_face_does_not_negate_an_accepted_face_for_same_pair"
        ] is True,
        label + ":EXISTS acceptance semantics",
    )
    need(
        row["formal_component_edge_credit"] == 1
        and all(row[field] == 0 for field in FORMAL_ZERO_FIELDS),
        label + ":canonical edge-only credit",
    )


def no_edge_row(source: dict[str, Any]) -> dict[str, Any]:
    source_id = source[
        "Round299_independent_signed_face_classification_row_id"
    ]
    self_accept = (
        source["decision"] == ACCEPT
        and source["same_formal_occurrence_endpoint"]
    )
    need(self_accept or source["decision"] == REJECT, "no-edge disposition")
    payload = {
        "Round299C_signed_face_no_edge_row_id":
            "round299c-signed-face-no-edge:" + digest(source_id),
        "source_Round299_classification_row_id": source_id,
        "source_Round299_classification_row_sha256": source["row_sha256"],
        "disposition": (
            "ACCEPTED_POSITIVE_PATCH_BUT_SELF_ENDPOINT_NO_EDGE"
            if self_accept
            else "REJECTED_NO_COMMON_POSITIVE_AREA_PATCH_NO_EDGE"
        ),
        "left_formal_occurrence_id": source["left_formal_occurrence_id"],
        "right_formal_occurrence_id": source["right_formal_occurrence_id"],
        "unordered_nonself_formal_occurrence_endpoint_pair":
            source["unordered_nonself_formal_occurrence_endpoint_pair"],
        "contact_class": source["contact_class"],
        "decision": source["decision"],
        "decision_reason": source["decision_reason"],
        "accepted_patch": source["accepted_patch"],
        "accepted_patch_area": source.get("accepted_patch_area"),
        "left_corridor": source["left_corridor"],
        "right_corridor": source["right_corridor"],
        "exclusion_evidence": source["exclusion_evidence"],
        "formal_component_edge_witness_credit": 0,
        "formal_component_edge_credit": 0,
        "formal_occurrence_identity_collapse_credit": 0,
        "formal_DSU_rank_reduction_credit": 0,
        "formal_maximality_credit": 0,
        "formal_fibre_credit": 0,
        "formal_global_disposition_credit": 0,
    }
    return close(payload)


def validate_no_edge(row: dict[str, Any], label: str) -> None:
    self_accept = (
        row["disposition"]
        == "ACCEPTED_POSITIVE_PATCH_BUT_SELF_ENDPOINT_NO_EDGE"
    )
    rejected = (
        row["disposition"]
        == "REJECTED_NO_COMMON_POSITIVE_AREA_PATCH_NO_EDGE"
    )
    need(self_accept ^ rejected, label + ":closed no-edge disposition")
    if self_accept:
        need(
            row["decision"] == ACCEPT
            and row["left_formal_occurrence_id"]
            == row["right_formal_occurrence_id"]
            and row["unordered_nonself_formal_occurrence_endpoint_pair"]
            is None
            and row["accepted_patch"] is not None
            and row["exclusion_evidence"] is None,
            label + ":accepted self semantics",
        )
    else:
        need(
            row["decision"] == REJECT
            and row["accepted_patch"] is None
            and isinstance(row["exclusion_evidence"], dict),
            label + ":rejected exclusion semantics",
        )
    need(
        row["formal_component_edge_witness_credit"] == 0
        and row["formal_component_edge_credit"] == 0
        and all(row[field] == 0 for field in FORMAL_ZERO_FIELDS),
        label + ":all no-edge credits zero",
    )


def expect_rejected(
    name: str,
    candidate: dict[str, Any],
    validator: Callable[[dict[str, Any], str], None],
    mutate: Callable[[dict[str, Any]], None],
) -> dict[str, Any]:
    attacked = copy.deepcopy(candidate)
    mutate(attacked)
    rejected = False
    reason = ""
    try:
        validator(attacked, "attack:" + name)
    except (BuildError, KeyError, ValueError, ZeroDivisionError) as error:
        rejected = True
        reason = type(error).__name__
    need(rejected, "attack survived:" + name)
    return {"attack": name, "rejected": True, "exception_class": reason}


def run_attacks(
    classification_rows: list[dict[str, Any]],
    raw_rows: list[dict[str, Any]],
    canonical_rows: list[dict[str, Any]],
    no_edge_rows: list[dict[str, Any]],
) -> dict[str, Any]:
    accepted = next(row for row in classification_rows if row["decision"] == ACCEPT)
    rejected = next(row for row in classification_rows if row["decision"] == REJECT)
    self_accept = next(
        row for row in classification_rows
        if row["decision"] == ACCEPT and row["same_formal_occurrence_endpoint"]
    )
    opposite = next(
        row for row in classification_rows
        if row["contact_class"]
        == "DOUBLE_GRAPH_SAME_FACTOR_OPPOSITE_SIDE"
    )
    active_corridor = next(
        row for row in classification_rows
        if row["decision"] == ACCEPT
        and row["left_corridor"]["signed_support_replay"] is not None
    )

    attacks: list[dict[str, Any]] = []

    def classification_attack(
        name: str,
        candidate: dict[str, Any],
        mutate: Callable[[dict[str, Any]], None],
    ) -> None:
        attacks.append(
            expect_rejected(name, candidate, validate_classification_row, mutate)
        )

    classification_attack(
        "unresolved-decision",
        accepted,
        lambda row: row.__setitem__("decision", "UNRESOLVED_FAIL_CLOSED"),
    )
    classification_attack(
        "patch-area-zero-claim",
        accepted,
        lambda row: row.__setitem__("accepted_patch_area", "0"),
    )
    classification_attack(
        "patch-escapes-face",
        accepted,
        lambda row: row["accepted_patch"].__setitem__(
            2 * ((row["common_face_axis"] + 1) % 3),
            "-999999999",
        ),
    )
    classification_attack(
        "left-corridor-zero-volume",
        accepted,
        lambda row: row["left_corridor"].__setitem__(
            "exact_transformed_corridor_volume", "0"
        ),
    )
    classification_attack(
        "right-corridor-tangent-mismatch",
        accepted,
        lambda row: row["right_corridor"][
            "exact_positive_volume_transformed_corridor"
        ].__setitem__(2 * ((row["common_face_axis"] + 1) % 3), "-999999999"),
    )
    classification_attack(
        "accepted-missing-left-corridor",
        accepted,
        lambda row: row.__setitem__("left_corridor", None),
    )
    classification_attack(
        "rejected-missing-exclusion",
        rejected,
        lambda row: row.__setitem__("exclusion_evidence", None),
    )
    classification_attack(
        "rejected-exclusion-allows-positive-trace",
        rejected,
        lambda row: row["exclusion_evidence"].__setitem__(
            "positive_area_common_strict_trace_possible", True
        ),
    )
    classification_attack(
        "source-formal-edge-credit-forgery",
        accepted,
        lambda row: row.__setitem__("formal_component_edge_credit", 1),
    )
    classification_attack(
        "nonself-pair-reordered",
        accepted,
        lambda row: row.__setitem__(
            "unordered_nonself_formal_occurrence_endpoint_pair",
            list(reversed(row["unordered_nonself_formal_occurrence_endpoint_pair"])),
        ),
    )
    classification_attack(
        "self-promoted-as-nonself",
        self_accept,
        lambda row: row.__setitem__(
            "unordered_nonself_formal_occurrence_endpoint_pair",
            [row["left_formal_occurrence_id"], row["left_formal_occurrence_id"]],
        ),
    )
    classification_attack(
        "opposite-factor-side-made-equal",
        opposite,
        lambda row: row["right_active_factor_descriptor"].__setitem__(
            "desired_side_sign",
            row["left_active_factor_descriptor"]["desired_side_sign"],
        ),
    )
    classification_attack(
        "active-corridor-replay-overwrap",
        active_corridor,
        lambda row: row["left_corridor"]["signed_support_replay"].__setitem__(
            "signed_support_state", "OVERWRAP"
        ),
    )

    def raw_attack(name: str, mutate: Callable[[dict[str, Any]], None]) -> None:
        attacks.append(
            expect_rejected(name, raw_rows[0], validate_raw_edge, mutate)
        )

    raw_attack(
        "raw-witness-credit-removed",
        lambda row: row.__setitem__("formal_component_edge_witness_credit", 0),
    )
    raw_attack(
        "raw-early-component-edge-credit",
        lambda row: row.__setitem__("formal_component_edge_credit", 1),
    )
    raw_attack(
        "raw-endpoint-self-collapse",
        lambda row: row.__setitem__(
            "unordered_formal_occurrence_endpoint_pair",
            [row["unordered_formal_occurrence_endpoint_pair"][0]] * 2,
        ),
    )

    def canonical_attack(
        name: str, mutate: Callable[[dict[str, Any]], None]
    ) -> None:
        attacks.append(
            expect_rejected(
                name, canonical_rows[0], validate_canonical_edge, mutate
            )
        )

    canonical_attack(
        "canonical-edge-credit-removed",
        lambda row: row.__setitem__("formal_component_edge_credit", 0),
    )
    canonical_attack(
        "canonical-empty-accepted-witness-list",
        lambda row: (
            row.__setitem__("accepted_raw_edge_witness_row_ids", []),
            row.__setitem__("accepted_raw_edge_witness_count", 0),
            row.__setitem__(
                "accepted_raw_edge_witness_row_ids_sha256", digest([])
            ),
        ),
    )
    canonical_attack(
        "canonical-pair-reordered",
        lambda row: row.__setitem__(
            "unordered_formal_occurrence_endpoint_pair",
            list(reversed(row["unordered_formal_occurrence_endpoint_pair"])),
        ),
    )
    canonical_attack(
        "canonical-universal-instead-of-exists-semantics",
        lambda row: row.__setitem__(
            "pair_acceptance_semantics",
            "ALL_FACES_MUST_ACCEPT",
        ),
    )

    def no_edge_attack(
        name: str, mutate: Callable[[dict[str, Any]], None]
    ) -> None:
        attacks.append(
            expect_rejected(name, no_edge_rows[0], validate_no_edge, mutate)
        )

    no_edge_attack(
        "no-edge-component-credit-forgery",
        lambda row: row.__setitem__("formal_component_edge_credit", 1),
    )
    no_edge_attack(
        "no-edge-witness-credit-forgery",
        lambda row: row.__setitem__(
            "formal_component_edge_witness_credit", 1
        ),
    )

    need(all(row["rejected"] for row in attacks), "all self attacks rejected")
    payload = {
        "schema": SCHEMA + ".attack-suite.v1",
        "status": "PASS_ALL_TARGETED_SELF_ATTACKS_REJECTED",
        "attack_count": len(attacks),
        "rejected_attack_count": len(attacks),
        "attacks": attacks,
    }
    payload["attack_suite_sha256"] = digest(payload)
    return payload


def ledger_document(
    schema_suffix: str,
    status: str,
    id_field: str,
    rows: list[dict[str, Any]],
    metadata: dict[str, Any],
) -> dict[str, Any]:
    return {
        "schema": SCHEMA + "." + schema_suffix + ".v1",
        "status": status,
        **metadata,
        "row_count": len(rows),
        "rows_sha256": digest(rows),
        "row_ids_sha256": digest([row[id_field] for row in rows]),
        "row_hashes_sha256": digest([row["row_sha256"] for row in rows]),
        "every_row_closed_by_own_SHA256": True,
        "rows": rows,
    }


def emit_gzip(path: Path, document: dict[str, Any]) -> dict[str, Any]:
    payload = deterministic_gzip_bytes(document)
    atomic(path, payload)
    return {
        "filename": path.name,
        "file_sha256": hashlib.sha256(payload).hexdigest(),
        "row_count": document["row_count"],
        "rows_sha256": document["rows_sha256"],
        "row_ids_sha256": document["row_ids_sha256"],
        "row_hashes_sha256": document["row_hashes_sha256"],
    }


def build(
    classification_path: Path,
    raw_path: Path,
    canonical_path: Path,
    no_edge_path: Path,
    attack_path: Path,
    result_path: Path,
) -> dict[str, Any]:
    for filename, pin in sorted(DIRECT_INPUT_PINS.items()):
        guarded_input(filename, pin)
    for filename, pin in sorted(EXPECTED_INHERITED_PINS.items()):
        guarded_input(filename, pin)

    source_ledger, _ = read_gzip_json_bytes(HERE / SOURCE_LEDGER)
    source_result, _ = read_json_bytes(HERE / SOURCE_RESULT)
    classification_rows = validate_source(source_ledger, source_result)

    raw_rows = [
        raw_edge_row(row)
        for row in classification_rows
        if row["decision"] == ACCEPT
        and not row["same_formal_occurrence_endpoint"]
    ]
    raw_rows.sort(
        key=lambda row: row["Round299C_signed_face_raw_edge_witness_row_id"]
    )
    need(len(raw_rows) == 27_856, "accepted nonself raw edge census")
    for index, row in enumerate(raw_rows):
        verify_closed(row, f"raw edge {index}")
        validate_raw_edge(row, f"raw edge {index}")

    raw_by_pair: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    raw_by_source_id = {}
    for row in raw_rows:
        raw_by_pair[
            tuple(row["unordered_formal_occurrence_endpoint_pair"])
        ].append(row)
        raw_by_source_id[row["source_Round299_classification_row_id"]] = row

    rejected_by_pair: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    for source in classification_rows:
        endpoint_pair = source[
            "unordered_nonself_formal_occurrence_endpoint_pair"
        ]
        if source["decision"] == REJECT and endpoint_pair is not None:
            rejected_by_pair[tuple(endpoint_pair)].append(source)

    canonical_rows = [
        canonical_edge_row(
            endpoint_pair,
            raw_by_pair[endpoint_pair],
            rejected_by_pair.get(endpoint_pair, []),
        )
        for endpoint_pair in sorted(raw_by_pair)
    ]
    canonical_rows.sort(
        key=lambda row:
            row["Round299C_canonical_signed_face_occurrence_edge_row_id"]
    )
    need(len(canonical_rows) == 25_452, "canonical edge-pair census")
    for index, row in enumerate(canonical_rows):
        verify_closed(row, f"canonical edge {index}")
        validate_canonical_edge(row, f"canonical edge {index}")

    accepted_pairs = set(raw_by_pair)
    rejected_pairs = set(rejected_by_pair)
    need(
        len(accepted_pairs & rejected_pairs) == 4,
        "four endpoint pairs have both accepted and rejected source faces",
    )

    no_edge_rows = [
        no_edge_row(row)
        for row in classification_rows
        if not (
            row["decision"] == ACCEPT
            and not row["same_formal_occurrence_endpoint"]
        )
    ]
    no_edge_rows.sort(
        key=lambda row: row["Round299C_signed_face_no_edge_row_id"]
    )
    need(len(no_edge_rows) == 15_236, "self/exclusion census")
    for index, row in enumerate(no_edge_rows):
        verify_closed(row, f"no-edge row {index}")
        validate_no_edge(row, f"no-edge row {index}")
    no_edge_dispositions = Counter(row["disposition"] for row in no_edge_rows)
    need(
        no_edge_dispositions == {
            "ACCEPTED_POSITIVE_PATCH_BUT_SELF_ENDPOINT_NO_EDGE": 2_092,
            "REJECTED_NO_COMMON_POSITIVE_AREA_PATCH_NO_EDGE": 13_144,
        },
        "self/exclusion disposition census",
    )

    attacks = run_attacks(
        classification_rows, raw_rows, canonical_rows, no_edge_rows
    )

    classification_document = ledger_document(
        "classification-inventory",
        "PASS_FORMAL_CLASSIFICATION_INVENTORY_FROZEN",
        "Round299_independent_signed_face_classification_row_id",
        classification_rows,
        {
            "source_probe_filename": SOURCE_PROBE,
            "source_probe_sha256": DIRECT_INPUT_PINS[SOURCE_PROBE],
            "source_zero_credit_ledger_filename": SOURCE_LEDGER,
            "source_zero_credit_ledger_sha256": DIRECT_INPUT_PINS[SOURCE_LEDGER],
            "classification_is_complete": True,
            "unresolved_face_contact_count": 0,
        },
    )
    raw_document = ledger_document(
        "accepted-nonself-raw-edge-witnesses",
        "PASS_27856_ACCEPTED_NONSELF_RAW_EDGE_WITNESSES_PROMOTED",
        "Round299C_signed_face_raw_edge_witness_row_id",
        raw_rows,
        {
            "component_edge_witness_credit_per_row": 1,
            "component_edge_credit_per_row": 0,
        },
    )
    canonical_document = ledger_document(
        "canonical-occurrence-edge-pairs",
        "PASS_25452_CANONICAL_OCCURRENCE_COMPONENT_EDGES_PROMOTED",
        "Round299C_canonical_signed_face_occurrence_edge_row_id",
        canonical_rows,
        {
            "component_edge_credit_per_row": 1,
            "pair_acceptance_quantifier": "EXISTS",
            "accepted_and_rejected_face_pair_overlap_count": 4,
        },
    )
    no_edge_document = ledger_document(
        "self-and-exclusion",
        "PASS_15236_SELF_OR_EXCLUDED_CONTACTS_FROZEN_WITH_ZERO_EDGE_CREDIT",
        "Round299C_signed_face_no_edge_row_id",
        no_edge_rows,
        {
            "component_edge_witness_credit_per_row": 0,
            "component_edge_credit_per_row": 0,
            "disposition_histogram": dict(sorted(no_edge_dispositions.items())),
        },
    )

    ledger_metadata = {
        "classification_inventory": emit_gzip(
            classification_path, classification_document
        ),
        "accepted_nonself_raw_edge_witnesses": emit_gzip(
            raw_path, raw_document
        ),
        "canonical_occurrence_edge_pairs": emit_gzip(
            canonical_path, canonical_document
        ),
        "self_and_exclusion": emit_gzip(no_edge_path, no_edge_document),
    }
    attack_bytes = canonical(attacks) + b"\n"
    atomic(attack_path, attack_bytes)

    result = {
        "schema": SCHEMA,
        "status":
            "PASS_FORMAL_R292_SIGNED_FACE_COMPONENT_EDGE_PACKAGE_SEALED",
        "direct_input_file_pins": dict(sorted(DIRECT_INPUT_PINS.items())),
        "inherited_input_file_pins":
            dict(sorted(EXPECTED_INHERITED_PINS.items())),
        "promotion_contract": {
            "input_Round292_refinement_cell_count": 11_852,
            "all_same_chart_same_physical_t_sign_face_contacts_classified":
                True,
            "classification_inventory_row_count": 43_092,
            "unresolved_face_contact_count": 0,
            "accepted_nonself_raw_edge_witness_count": 27_856,
            "canonical_occurrence_component_edge_count": 25_452,
            "accepted_self_endpoint_no_edge_count": 2_092,
            "rejected_exclusion_no_edge_count": 13_144,
            "self_and_exclusion_row_count": 15_236,
            "every_accepted_witness_has_exact_positive_area_patch": True,
            "every_accepted_witness_has_two_exact_positive_volume_corridors":
                True,
            "every_rejected_face_has_exact_exclusion_evidence": True,
            "accepted_and_rejected_face_pair_overlap_count": 4,
            "pair_acceptance_quantifier": "EXISTS",
            "accepted_pair_existing_channel_intersection_count": {
                "R295A_LOWER": 0,
                "R296_TRUE_SEAM": 0,
                "R297_ORDINARY": 0,
            },
        },
        "formal_credit_contract": {
            "raw_component_edge_witness_credit_total": 27_856,
            "canonical_component_edge_credit_total": 25_452,
            "formal_occurrence_identity_collapse_credit": 0,
            "formal_DSU_rank_reduction_credit": 0,
            "formal_maximality_credit": 0,
            "formal_fibre_credit": 0,
            "formal_global_disposition_credit": 0,
        },
        "strict_nonclaims": {
            "coordinate_face_contact_alone_is_an_edge": False,
            "accepted_face_connectivity_is_occurrence_identity": False,
            "component_DSU_applied": False,
            "current_quotient_component_count": None,
            "maximality_proved": False,
            "CM2":
                "NO_GO_UNTIL_INDEPENDENT_VERIFICATION_AND_COMBINED_DSU_GATES",
        },
        "ledgers": ledger_metadata,
        "attack_suite": {
            "filename": attack_path.name,
            "file_sha256": hashlib.sha256(attack_bytes).hexdigest(),
            "attack_count": attacks["attack_count"],
            "rejected_attack_count": attacks["rejected_attack_count"],
            "attack_suite_sha256": attacks["attack_suite_sha256"],
        },
    }
    result["result_sha256"] = digest(result)
    atomic(result_path, canonical(result) + b"\n")
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, default=299_301)
    parser.add_argument(
        "--classification-ledger", type=Path, default=CLASSIFICATION_LEDGER
    )
    parser.add_argument("--raw-edge-ledger", type=Path, default=RAW_EDGE_LEDGER)
    parser.add_argument(
        "--canonical-edge-ledger", type=Path, default=CANONICAL_EDGE_LEDGER
    )
    parser.add_argument("--no-edge-ledger", type=Path, default=NO_EDGE_LEDGER)
    parser.add_argument("--attack-suite", type=Path, default=ATTACK_SUITE)
    parser.add_argument("--result", type=Path, default=RESULT)
    arguments = parser.parse_args()
    result = build(
        arguments.classification_ledger,
        arguments.raw_edge_ledger,
        arguments.canonical_edge_ledger,
        arguments.no_edge_ledger,
        arguments.attack_suite,
        arguments.result,
    )
    print(result["status"])
    print(json.dumps(result["promotion_contract"], sort_keys=True))
    print("result_sha256=" + result["result_sha256"])
    for name, metadata in sorted(result["ledgers"].items()):
        print(name + "_file_sha256=" + metadata["file_sha256"])


if __name__ == "__main__":
    main()
