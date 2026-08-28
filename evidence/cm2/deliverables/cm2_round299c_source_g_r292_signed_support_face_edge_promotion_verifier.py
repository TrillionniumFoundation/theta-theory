#!/usr/bin/env python3
"""Independent cacheless verifier for the Round299-C signed-face edge package.

The verifier never imports, executes, or parses the Round299-C producer.  It
uses the separately pinned Round299 mathematical classifier implementation
only as a library of exact-rational/Arb routines, calls those routines directly
on the pinned Round174/179/274/275/287/292/294/295A/296/297 sources, and does
not read the persisted Round299 probe ledger or result as an expected oracle.

All 43,092 classifications and the three derived formal ledgers are completed
before any Round299-C candidate ledger or result is opened.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import copy
from fractions import Fraction as Q
import gc
import gzip
import hashlib
import io
import json
import os
from pathlib import Path
import stat
import sys
import tempfile
from typing import Any, Callable

from flint import ctx


HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import cm2_round299_source_g_r292_signed_support_face_classifier_independent_probe as math299


PREFIX = "cm2_round299c_source_g_r292_signed_support_face_edge_promotion"
PRODUCER = HERE / f"{PREFIX}.py"
CLASSIFICATION = HERE / f"{PREFIX}_classification_inventory.json.gz"
RAW_EDGES = HERE / f"{PREFIX}_accepted_nonself_raw_edge_witnesses.json.gz"
CANONICAL_EDGES = HERE / f"{PREFIX}_canonical_occurrence_edge_pairs.json.gz"
NO_EDGES = HERE / f"{PREFIX}_self_and_exclusion.json.gz"
PRODUCER_ATTACKS = HERE / f"{PREFIX}_attack_suite.json"
RESULT = HERE / f"{PREFIX}_result.json"
VERIFIER = HERE / f"{PREFIX}_verifier.py"
INDEPENDENT_ATTACKS = HERE / f"{PREFIX}_independent_attack_suite.json"
VERIFICATION = HERE / f"{PREFIX}_verification.json"

SCHEMA = "cm2.round299c.source-g-r292-signed-support-face-edge-promotion.v1"
VERIFY_SCHEMA = SCHEMA + ".verification.v1"
ATTACK_SCHEMA = SCHEMA + ".independent-attack-suite.v1"

MATH_SOURCE = (
    "cm2_round299_source_g_r292_signed_support_face_classifier_"
    "independent_probe.py"
)
PERSISTED_PROBE_LEDGER = (
    "cm2_round299_source_g_r292_signed_support_face_classifier_"
    "independent_probe_ledger.json.gz"
)
PERSISTED_PROBE_RESULT = (
    "cm2_round299_source_g_r292_signed_support_face_classifier_"
    "independent_probe_result.json"
)

MATH_SOURCE_SHA256 = (
    "d6cae0b9ede704b7da57fd9c37b8097919e01592482a8a0eee63fd4a27178b24"
)
PERSISTED_PROBE_LEDGER_SHA256 = (
    "9797d486eaf96ce8352883093c24637b5eb9cb27af60fd79e5ee03a6585d27a9"
)
PERSISTED_PROBE_RESULT_SHA256 = (
    "07427f743ace170d6d7d832c67658d8d27eca2d51092049625c117abfc8efcdb"
)

CANDIDATE_PINS = {
    PRODUCER.name:
        "4c8209f283709649c2a969bbc98b2efe080afb8b760b0d246a0a00501c871920",
    CLASSIFICATION.name:
        "2b7afa578911a701bf72e9d04032cd179bec3b7f86163530561d6fe81c53faa3",
    RAW_EDGES.name:
        "3e05e96d98ef5b72c3cdd4d4fd63047fd9636281354997b3d4a9dfc6480aa150",
    CANONICAL_EDGES.name:
        "e63f164bf9cc559ec8d3a2895e66493933b43b90f1ad3b163dfb41e12bb04df1",
    NO_EDGES.name:
        "cc9583b5a00db9f4c727c95692db7a356b1d37a443074b28610a3e6822168b96",
    PRODUCER_ATTACKS.name:
        "61de25264720cca43a3ca72ae0db241c6f09624c70ce9f34eef83340e802d45e",
    RESULT.name:
        "7954669c0cc421732b28277ae2c03cacd6fbd70d9c5575765a5c087b7c65c5f4",
}

PRODUCER_ATTACK_SELF_SHA256 = (
    "c0a859150234b7af5da01934d3ac0551b0ab85508d57b0bac57703752f94d071"
)
RESULT_SELF_SHA256 = (
    "36a484e614fb0d660062fa1b7529afb0d5f6ca0fd617955bebcf47ce650a4b8c"
)

ACCEPT = (
    "ACCEPT_STRICT_POSITIVE_AREA_FACE_PATCH_AND_TWO_SIDED_CORRIDOR"
)
REJECT = "REJECT_NO_COMMON_POSITIVE_AREA_SIGNED_FACE_PATCH"
ZERO_FIELDS = (
    "formal_occurrence_identity_collapse_credit",
    "formal_DSU_rank_reduction_credit",
    "formal_maximality_credit",
    "formal_fibre_credit",
    "formal_global_disposition_credit",
)


class VerificationError(RuntimeError):
    """Fail-closed verification error."""


def need(condition: bool, label: str) -> None:
    if not condition:
        raise VerificationError(label)


def duplicate_free_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise VerificationError("JSON_DUPLICATE_KEY")
        result[key] = value
    return result


def reject_constant(token: str) -> Any:
    raise VerificationError("JSON_NONFINITE:" + token)


def canonical(value: Any) -> bytes:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
        allow_nan=False,
    ).encode("ascii")


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def file_sha256(path: Path) -> str:
    state = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1 << 20), b""):
            state.update(chunk)
    return state.hexdigest()


def strict_json_bytes(payload: bytes, label: str) -> dict[str, Any]:
    try:
        text = payload.decode("ascii")
        value = json.loads(
            text,
            object_pairs_hook=duplicate_free_object,
            parse_constant=reject_constant,
        )
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise VerificationError(label + ":STRICT_JSON") from error
    need(isinstance(value, dict), label + ":JSON_OBJECT")
    need(payload == canonical(value) + b"\n", label + ":CANONICAL_JSON")
    return value


def deterministic_gzip(value: Any, *, mtime: int = 0) -> bytes:
    target = io.BytesIO()
    with gzip.GzipFile(
        filename="",
        mode="wb",
        fileobj=target,
        compresslevel=9,
        mtime=mtime,
    ) as stream:
        stream.write(canonical(value))
    return target.getvalue()


def strict_gzip_bytes(payload: bytes, label: str) -> dict[str, Any]:
    try:
        with gzip.GzipFile(fileobj=io.BytesIO(payload), mode="rb") as stream:
            decoded = stream.read()
    except (OSError, EOFError) as error:
        raise VerificationError(label + ":STRICT_GZIP") from error
    try:
        value = json.loads(
            decoded.decode("ascii"),
            object_pairs_hook=duplicate_free_object,
            parse_constant=reject_constant,
        )
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise VerificationError(label + ":GZIP_JSON") from error
    need(isinstance(value, dict), label + ":GZIP_OBJECT")
    need(decoded == canonical(value), label + ":GZIP_CANONICAL_PAYLOAD")
    need(payload == deterministic_gzip(value), label + ":DETERMINISTIC_GZIP")
    return value


def require_safe_regular(
    path: Path,
    expected_name: str,
    expected_sha256: str | None = None,
) -> None:
    need(path.name == expected_name, "PATH_BASENAME:" + expected_name)
    need(path.parent == HERE, "PATH_PARENT:" + expected_name)
    need(not path.is_symlink(), "PATH_SYMLINK:" + expected_name)
    try:
        status = os.lstat(path)
    except FileNotFoundError as error:
        raise VerificationError("PATH_MISSING:" + expected_name) from error
    need(stat.S_ISREG(status.st_mode), "PATH_NOT_REGULAR:" + expected_name)
    need(status.st_nlink == 1, "PATH_LINK_COUNT:" + expected_name)
    need(
        path.resolve(strict=True).parent == HERE.resolve(strict=True),
        "PATH_RESOLUTION:" + expected_name,
    )
    if expected_sha256 is not None:
        need(
            file_sha256(path) == expected_sha256,
            "FILE_PIN:" + expected_name,
        )


def close_row(payload: dict[str, Any]) -> dict[str, Any]:
    need("row_sha256" not in payload, "ROW_ALREADY_CLOSED")
    row = dict(payload)
    row["row_sha256"] = digest(payload)
    return row


def verify_closed_row(row: dict[str, Any], label: str) -> None:
    payload = {key: value for key, value in row.items() if key != "row_sha256"}
    need(
        set(row) == set(payload) | {"row_sha256"}
        and row["row_sha256"] == digest(payload),
        label + ":ROW_CLOSURE",
    )


def qbox(value: Any, label: str) -> tuple[Q, ...]:
    need(isinstance(value, list) and len(value) == 6, label + ":QBOX")
    result = tuple(Q(item) for item in value)
    need(
        all(
            result[2 * axis] <= result[2 * axis + 1]
            for axis in range(3)
        ),
        label + ":ORDERED_QBOX",
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
    corridor: dict[str, Any],
    patch: tuple[Q, ...],
    axis: int,
    left: bool,
    label: str,
) -> None:
    need(isinstance(corridor, dict), label + ":OBJECT")
    box = qbox(
        corridor["exact_positive_volume_transformed_corridor"],
        label + ":BOX",
    )
    need(
        Q(corridor["exact_transformed_corridor_volume"]) == volume(box) > 0,
        label + ":POSITIVE_VOLUME",
    )
    for tangent in range(3):
        if tangent != axis:
            need(
                box[2 * tangent] == patch[2 * tangent]
                and box[2 * tangent + 1] == patch[2 * tangent + 1],
                label + ":TANGENTIAL_FOOTPRINT",
            )
    if left:
        need(
            box[2 * axis + 1] == patch[2 * axis]
            and box[2 * axis] < box[2 * axis + 1],
            label + ":LEFT_SIDE",
        )
    else:
        need(
            box[2 * axis] == patch[2 * axis]
            and box[2 * axis] < box[2 * axis + 1],
            label + ":RIGHT_SIDE",
        )
    certificates = corridor["t_boundary_sqrt_enclosure_certificates"]
    need(
        isinstance(certificates, list)
        and corridor["t_boundary_sqrt_enclosures_sha256"]
        == digest(certificates),
        label + ":SQRT_CERTIFICATE_CLOSURE",
    )
    trace = corridor["dyadic_inward_shrink_trace"]
    depth = corridor["corridor_depth"]
    need(
        isinstance(depth, int)
        and depth > 0
        and isinstance(trace, list)
        and len(trace) == depth
        and corridor["dyadic_inward_shrink_trace_sha256"] == digest(trace),
        label + ":SHRINK_TRACE_CLOSURE",
    )
    final = trace[-1]
    need(
        final["corridor_depth"] == depth
        and final["transformed_corridor_sha256"]
        == digest(corridor["exact_positive_volume_transformed_corridor"])
        and final["t_boundary_sqrt_enclosures_sha256"]
        == digest(certificates),
        label + ":FINAL_TRACE_BINDING",
    )
    replay = corridor["signed_support_replay"]
    if replay is None:
        need(
            corridor["support_basis"]
            == "INHERITED_R287_FULL_SIGNED_SUPPORT"
            and depth == 1
            and final["signed_support_state"]
            == "INHERITED_FULL_SIGNED_SUPPORT",
            label + ":INHERITED_FULL_SUPPORT",
        )
    else:
        need(
            isinstance(replay, dict)
            and corridor["support_basis"]
            == "R287_ACTIVE_FACTOR_STRICT_CORRIDOR_REPLAY"
            and replay["signed_support_state"]
            == "FULL_DESIRED_SIDE_SUPPORT"
            and final["signed_support_state"]
            == "FULL_DESIRED_SIDE_SUPPORT",
            label + ":ACTIVE_FACTOR_STRICT_REPLAY",
        )


def raw_edge_row(source: dict[str, Any]) -> dict[str, Any]:
    source_id = source[
        "Round299_independent_signed_face_classification_row_id"
    ]
    payload = {
        "Round299C_signed_face_raw_edge_witness_row_id":
            "round299c-signed-face-raw-edge:" + digest(source_id),
        "source_Round299_classification_row_id": source_id,
        "source_Round299_classification_row_sha256": source["row_sha256"],
        "unordered_formal_occurrence_endpoint_pair":
            source["unordered_nonself_formal_occurrence_endpoint_pair"],
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
    return close_row(payload)


def validate_raw_edge(row: dict[str, Any], label: str) -> None:
    verify_closed_row(row, label)
    pair = row["unordered_formal_occurrence_endpoint_pair"]
    need(
        isinstance(pair, list)
        and len(pair) == 2
        and pair == sorted(pair)
        and pair[0] != pair[1],
        label + ":CANONICAL_NONSELF_PAIR",
    )
    need(
        row["formal_component_edge_witness_credit"] == 1
        and row["formal_component_edge_credit"] == 0
        and all(row[field] == 0 for field in ZERO_FIELDS),
        label + ":WITNESS_ONLY_CREDIT",
    )
    axis = row["common_face_axis"]
    patch = qbox(row["accepted_patch"], label + ":PATCH")
    need(
        area(patch, axis) > 0
        and Q(row["accepted_patch_area"]) == area(patch, axis),
        label + ":PATCH_AREA",
    )
    validate_corridor(
        row["left_strict_positive_volume_corridor"],
        patch,
        axis,
        True,
        label + ":LEFT_CORRIDOR",
    )
    validate_corridor(
        row["right_strict_positive_volume_corridor"],
        patch,
        axis,
        False,
        label + ":RIGHT_CORRIDOR",
    )


def canonical_edge_row(
    pair: tuple[str, str],
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
            "round299c-canonical-signed-face-edge:" + digest(list(pair)),
        "unordered_formal_occurrence_endpoint_pair": list(pair),
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
    return close_row(payload)


def validate_canonical_edge(row: dict[str, Any], label: str) -> None:
    verify_closed_row(row, label)
    pair = row["unordered_formal_occurrence_endpoint_pair"]
    accepted = row["accepted_raw_edge_witness_row_ids"]
    rejected = row["source_reject_face_row_ids_for_same_endpoint_pair"]
    need(
        isinstance(pair, list)
        and len(pair) == 2
        and pair == sorted(pair)
        and pair[0] != pair[1],
        label + ":CANONICAL_PAIR",
    )
    need(
        accepted == sorted(set(accepted))
        and len(accepted) == row["accepted_raw_edge_witness_count"] > 0
        and row["accepted_raw_edge_witness_row_ids_sha256"]
        == digest(accepted),
        label + ":ACCEPTED_WITNESSES",
    )
    source_ids = row["source_accept_classification_row_ids"]
    need(
        source_ids == sorted(set(source_ids))
        and len(source_ids) == len(accepted)
        and row["source_accept_classification_row_ids_sha256"]
        == digest(source_ids),
        label + ":SOURCE_ACCEPTS",
    )
    need(
        rejected == sorted(set(rejected))
        and len(rejected)
        == row["source_reject_face_row_count_for_same_endpoint_pair"]
        and row["source_reject_face_row_ids_for_same_endpoint_pair_sha256"]
        == digest(rejected),
        label + ":COEXISTING_REJECTS",
    )
    need(
        row["pair_acceptance_semantics"]
        == "EXISTS_STRICT_POSITIVE_AREA_PATCH_WITH_TWO_SIDED_CORRIDOR"
        and row[
            "a_rejected_face_does_not_negate_an_accepted_face_for_same_pair"
        ] is True,
        label + ":EXISTS_SEMANTICS",
    )
    need(
        row["formal_component_edge_credit"] == 1
        and all(row[field] == 0 for field in ZERO_FIELDS),
        label + ":EDGE_ONLY_CREDIT",
    )


def no_edge_row(source: dict[str, Any]) -> dict[str, Any]:
    source_id = source[
        "Round299_independent_signed_face_classification_row_id"
    ]
    self_accept = (
        source["decision"] == ACCEPT
        and source["same_formal_occurrence_endpoint"]
    )
    need(self_accept or source["decision"] == REJECT, "NO_EDGE_DISPOSITION")
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
    return close_row(payload)


def validate_no_edge(row: dict[str, Any], label: str) -> None:
    verify_closed_row(row, label)
    self_accept = (
        row["disposition"]
        == "ACCEPTED_POSITIVE_PATCH_BUT_SELF_ENDPOINT_NO_EDGE"
    )
    rejected = (
        row["disposition"]
        == "REJECTED_NO_COMMON_POSITIVE_AREA_PATCH_NO_EDGE"
    )
    need(self_accept ^ rejected, label + ":DISPOSITION")
    if self_accept:
        need(
            row["decision"] == ACCEPT
            and row["left_formal_occurrence_id"]
            == row["right_formal_occurrence_id"]
            and row["unordered_nonself_formal_occurrence_endpoint_pair"]
            is None
            and row["accepted_patch"] is not None
            and row["exclusion_evidence"] is None,
            label + ":SELF_ACCEPT",
        )
    else:
        need(
            row["decision"] == REJECT
            and row["accepted_patch"] is None
            and isinstance(row["exclusion_evidence"], dict),
            label + ":REJECT_EXCLUSION",
        )
    need(
        row["formal_component_edge_witness_credit"] == 0
        and row["formal_component_edge_credit"] == 0
        and all(row[field] == 0 for field in ZERO_FIELDS),
        label + ":ZERO_CREDIT",
    )


def ledger_document(
    suffix: str,
    status: str,
    id_field: str,
    rows: list[dict[str, Any]],
    metadata: dict[str, Any],
) -> dict[str, Any]:
    return {
        "schema": SCHEMA + "." + suffix + ".v1",
        "status": status,
        **metadata,
        "row_count": len(rows),
        "rows_sha256": digest(rows),
        "row_ids_sha256": digest([row[id_field] for row in rows]),
        "row_hashes_sha256": digest([row["row_sha256"] for row in rows]),
        "every_row_closed_by_own_SHA256": True,
        "rows": rows,
    }


def build_expected() -> dict[str, Any]:
    """Complete the mathematical and formal reconstruction before candidates."""
    need(
        file_sha256(HERE / MATH_SOURCE) == MATH_SOURCE_SHA256,
        "MATH_SOURCE_PIN",
    )
    need(math299.PINS == math299.PINS, "MATH_PIN_TABLE")
    ctx.prec = math299.ARB_PRECISION_BITS
    regions = math299.load_regions()
    r287_regions, r287_cells = math299.load_r287()
    refined = math299.load_refined_occurrence_map()
    cells = math299.load_cells(
        regions, r287_regions, r287_cells, refined
    )
    need(len(cells) == 11_852, "CELL_CENSUS")
    classifications = math299.enumerate_and_classify(cells, regions)
    channels = math299.load_existing_channel_pairs()
    source_census = math299.census(classifications, channels)
    need(
        source_census[
            "raw_same_chart_same_physical_t_sign_box_face_contact_count"
        ] == 43_092
        and source_census[
            "accepted_nonself_raw_component_edge_candidate_count"
        ] == 27_856
        and source_census[
            "accepted_distinct_nonself_occurrence_pair_count"
        ] == 25_452
        and source_census[
            "accepted_self_endpoint_physical_patch_count"
        ] == 2_092
        and source_census["rejected_raw_face_contact_count"] == 13_144
        and source_census["unresolved_face_contact_count"] == 0,
        "SOURCE_CENSUS",
    )
    del cells, regions, r287_regions, r287_cells, refined, channels
    gc.collect()

    for index, row in enumerate(classifications):
        math299.verify_closed_row(row, f"classification:{index}")

    raw_rows = [
        raw_edge_row(row)
        for row in classifications
        if row["decision"] == ACCEPT
        and not row["same_formal_occurrence_endpoint"]
    ]
    raw_rows.sort(
        key=lambda row: row[
            "Round299C_signed_face_raw_edge_witness_row_id"
        ]
    )
    need(len(raw_rows) == 27_856, "RAW_EDGE_CENSUS")
    for index, row in enumerate(raw_rows):
        validate_raw_edge(row, f"raw:{index}")

    raw_by_pair: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    for row in raw_rows:
        raw_by_pair[
            tuple(row["unordered_formal_occurrence_endpoint_pair"])
        ].append(row)
    rejected_by_pair: dict[
        tuple[str, str], list[dict[str, Any]]
    ] = defaultdict(list)
    for row in classifications:
        pair = row["unordered_nonself_formal_occurrence_endpoint_pair"]
        if row["decision"] == REJECT and pair is not None:
            rejected_by_pair[tuple(pair)].append(row)

    canonical_rows = [
        canonical_edge_row(
            pair, raw_by_pair[pair], rejected_by_pair.get(pair, [])
        )
        for pair in sorted(raw_by_pair)
    ]
    canonical_rows.sort(
        key=lambda row: row[
            "Round299C_canonical_signed_face_occurrence_edge_row_id"
        ]
    )
    need(len(canonical_rows) == 25_452, "CANONICAL_EDGE_CENSUS")
    need(
        len(set(raw_by_pair) & set(rejected_by_pair)) == 4,
        "FOUR_MIXED_PAIRS",
    )
    for index, row in enumerate(canonical_rows):
        validate_canonical_edge(row, f"canonical:{index}")

    no_edge_rows = [
        no_edge_row(row)
        for row in classifications
        if not (
            row["decision"] == ACCEPT
            and not row["same_formal_occurrence_endpoint"]
        )
    ]
    no_edge_rows.sort(
        key=lambda row: row["Round299C_signed_face_no_edge_row_id"]
    )
    need(len(no_edge_rows) == 15_236, "NO_EDGE_CENSUS")
    for index, row in enumerate(no_edge_rows):
        validate_no_edge(row, f"no-edge:{index}")
    dispositions = Counter(row["disposition"] for row in no_edge_rows)
    need(
        dispositions == {
            "ACCEPTED_POSITIVE_PATCH_BUT_SELF_ENDPOINT_NO_EDGE": 2_092,
            "REJECTED_NO_COMMON_POSITIVE_AREA_PATCH_NO_EDGE": 13_144,
        },
        "NO_EDGE_DISPOSITIONS",
    )

    classification_doc = ledger_document(
        "classification-inventory",
        "PASS_FORMAL_CLASSIFICATION_INVENTORY_FROZEN",
        "Round299_independent_signed_face_classification_row_id",
        classifications,
        {
            "source_probe_filename": MATH_SOURCE,
            "source_probe_sha256": MATH_SOURCE_SHA256,
            "source_zero_credit_ledger_filename": PERSISTED_PROBE_LEDGER,
            "source_zero_credit_ledger_sha256":
                PERSISTED_PROBE_LEDGER_SHA256,
            "classification_is_complete": True,
            "unresolved_face_contact_count": 0,
        },
    )
    raw_doc = ledger_document(
        "accepted-nonself-raw-edge-witnesses",
        "PASS_27856_ACCEPTED_NONSELF_RAW_EDGE_WITNESSES_PROMOTED",
        "Round299C_signed_face_raw_edge_witness_row_id",
        raw_rows,
        {
            "component_edge_witness_credit_per_row": 1,
            "component_edge_credit_per_row": 0,
        },
    )
    canonical_doc = ledger_document(
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
    no_edge_doc = ledger_document(
        "self-and-exclusion",
        "PASS_15236_SELF_OR_EXCLUDED_CONTACTS_FROZEN_WITH_ZERO_EDGE_CREDIT",
        "Round299C_signed_face_no_edge_row_id",
        no_edge_rows,
        {
            "component_edge_witness_credit_per_row": 0,
            "component_edge_credit_per_row": 0,
            "disposition_histogram": dict(sorted(dispositions.items())),
        },
    )

    documents = {
        "classification": classification_doc,
        "raw": raw_doc,
        "canonical": canonical_doc,
        "no_edge": no_edge_doc,
    }
    ledger_metadata = {}
    for name, path in (
        ("classification_inventory", CLASSIFICATION),
        ("accepted_nonself_raw_edge_witnesses", RAW_EDGES),
        ("canonical_occurrence_edge_pairs", CANONICAL_EDGES),
        ("self_and_exclusion", NO_EDGES),
    ):
        key = {
            "classification_inventory": "classification",
            "accepted_nonself_raw_edge_witnesses": "raw",
            "canonical_occurrence_edge_pairs": "canonical",
            "self_and_exclusion": "no_edge",
        }[name]
        document = documents[key]
        encoded = deterministic_gzip(document)
        ledger_metadata[name] = {
            "filename": path.name,
            "file_sha256": hashlib.sha256(encoded).hexdigest(),
            "row_count": document["row_count"],
            "rows_sha256": document["rows_sha256"],
            "row_ids_sha256": document["row_ids_sha256"],
            "row_hashes_sha256": document["row_hashes_sha256"],
        }
        need(
            ledger_metadata[name]["file_sha256"]
            == CANDIDATE_PINS[path.name],
            "RECONSTRUCTED_LEDGER_PIN:" + name,
        )

    result = {
        "schema": SCHEMA,
        "status":
            "PASS_FORMAL_R292_SIGNED_FACE_COMPONENT_EDGE_PACKAGE_SEALED",
        "direct_input_file_pins": {
            MATH_SOURCE: MATH_SOURCE_SHA256,
            PERSISTED_PROBE_LEDGER: PERSISTED_PROBE_LEDGER_SHA256,
            PERSISTED_PROBE_RESULT: PERSISTED_PROBE_RESULT_SHA256,
        },
        "inherited_input_file_pins":
            dict(sorted(math299.PINS.items())),
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
            "filename": PRODUCER_ATTACKS.name,
            "file_sha256": CANDIDATE_PINS[PRODUCER_ATTACKS.name],
            "attack_count": 22,
            "rejected_attack_count": 22,
            "attack_suite_sha256": PRODUCER_ATTACK_SELF_SHA256,
        },
    }
    result["result_sha256"] = digest(result)
    need(result["result_sha256"] == RESULT_SELF_SHA256, "RESULT_SELF_PIN")
    need(
        hashlib.sha256(canonical(result) + b"\n").hexdigest()
        == CANDIDATE_PINS[RESULT.name],
        "RESULT_FILE_PIN",
    )
    return {
        "documents": documents,
        "result": result,
        "source_census": source_census,
        "samples": {
            "classification_accept": next(
                row for row in classifications
                if row["decision"] == ACCEPT
                and not row["same_formal_occurrence_endpoint"]
            ),
            "classification_reject": next(
                row for row in classifications if row["decision"] == REJECT
            ),
            "classification_active": next(
                row for row in classifications
                if row["decision"] == ACCEPT
                and (
                    row["left_active_factor_descriptor"] is not None
                    or row["right_active_factor_descriptor"] is not None
                )
            ),
            "raw": raw_rows[0],
            "canonical": canonical_rows[0],
            "canonical_mixed": next(
                row for row in canonical_rows
                if row[
                    "source_reject_face_row_count_for_same_endpoint_pair"
                ] > 0
            ),
            "no_edge_self": next(
                row for row in no_edge_rows
                if row["disposition"].startswith("ACCEPTED_")
            ),
            "no_edge_reject": next(
                row for row in no_edge_rows
                if row["disposition"].startswith("REJECTED_")
            ),
        },
    }


def open_and_match_candidates(expected: dict[str, Any]) -> dict[str, str]:
    """Only called after build_expected has completed."""
    candidate_pins = {}
    for path in (
        PRODUCER, CLASSIFICATION, RAW_EDGES, CANONICAL_EDGES,
        NO_EDGES, PRODUCER_ATTACKS, RESULT,
    ):
        require_safe_regular(path, path.name, CANDIDATE_PINS[path.name])
        candidate_pins[path.name] = file_sha256(path)

    for key, path in (
        ("classification", CLASSIFICATION),
        ("raw", RAW_EDGES),
        ("canonical", CANONICAL_EDGES),
        ("no_edge", NO_EDGES),
    ):
        raw = path.read_bytes()
        candidate = strict_gzip_bytes(raw, path.name)
        need(candidate == expected["documents"][key], "EXACT_LEDGER:" + key)
        del candidate, raw
        gc.collect()

    result_raw = RESULT.read_bytes()
    candidate_result = strict_json_bytes(result_raw, RESULT.name)
    need(candidate_result == expected["result"], "EXACT_RESULT")
    del candidate_result, result_raw
    gc.collect()

    historical_raw = PRODUCER_ATTACKS.read_bytes()
    historical = strict_json_bytes(
        historical_raw, PRODUCER_ATTACKS.name
    )
    historical_payload = {
        key: value
        for key, value in historical.items()
        if key != "attack_suite_sha256"
    }
    need(
        historical["attack_suite_sha256"] == digest(historical_payload)
        == PRODUCER_ATTACK_SELF_SHA256,
        "PRODUCER_ATTACK_SELF_CLOSURE",
    )
    need(
        historical["attack_count"]
        == historical["rejected_attack_count"] == 22,
        "PRODUCER_ATTACK_CENSUS",
    )
    del historical, historical_raw
    return candidate_pins


def resign_row(row: dict[str, Any]) -> dict[str, Any]:
    payload = copy.deepcopy(row)
    payload.pop("row_sha256", None)
    return close_row(payload)


def resign_result(result: dict[str, Any]) -> dict[str, Any]:
    payload = copy.deepcopy(result)
    payload.pop("result_sha256", None)
    payload["result_sha256"] = digest(payload)
    return payload


def expect_rejected(
    attack_id: str,
    original: dict[str, Any],
    mutate: Callable[[dict[str, Any]], None],
    reclose: Callable[[dict[str, Any]], dict[str, Any]],
    validate: Callable[[dict[str, Any]], None],
    classification: str = "RESIGNED_SEMANTIC_FORGERY",
) -> dict[str, Any]:
    attacked = copy.deepcopy(original)
    mutate(attacked)
    attacked = reclose(attacked)
    rejected = False
    try:
        validate(attacked)
    except Exception:
        rejected = True
    need(rejected, "ATTACK_ACCEPTED:" + attack_id)
    return {
        "attack_id": attack_id,
        "classification": classification,
        "disposition": "REJECTED",
    }


def exact_row_validator(
    expected: dict[str, Any],
    semantic: Callable[[dict[str, Any], str], None] | None = None,
) -> Callable[[dict[str, Any]], None]:
    def validate(row: dict[str, Any]) -> None:
        verify_closed_row(row, "attack")
        if semantic is not None:
            semantic(row, "attack")
        need(row == expected, "RECONSTRUCTED_EXPECTED_ROW")
    return validate


def build_attacks(expected: dict[str, Any]) -> dict[str, Any]:
    samples = expected["samples"]
    attacks: list[dict[str, Any]] = []

    def forge_active_factor_side(row: dict[str, Any]) -> None:
        descriptor = next(
            value
            for value in (
                row["left_active_factor_descriptor"],
                row["right_active_factor_descriptor"],
            )
            if value is not None
        )
        descriptor["desired_side_sign"] = (
            "STRICT_NEGATIVE"
            if descriptor["desired_side_sign"] == "STRICT_POSITIVE"
            else "STRICT_POSITIVE"
        )

    def add_row(
        attack_id: str,
        sample_name: str,
        mutate: Callable[[dict[str, Any]], None],
        semantic: Callable[[dict[str, Any], str], None] | None = None,
    ) -> None:
        attacks.append(expect_rejected(
            attack_id,
            samples[sample_name],
            mutate,
            resign_row,
            exact_row_validator(samples[sample_name], semantic),
        ))

    add_row(
        "C01_CLASSIFICATION_DECISION_FLIP",
        "classification_accept",
        lambda row: row.__setitem__("decision", REJECT),
    )
    add_row(
        "C02_CLASSIFICATION_PATCH_REMOVED",
        "classification_accept",
        lambda row: row.__setitem__("accepted_patch", None),
    )
    add_row(
        "C03_CLASSIFICATION_PATCH_AREA_ZERO",
        "classification_accept",
        lambda row: row.__setitem__("accepted_patch_area", "0"),
    )
    add_row(
        "C04_CLASSIFICATION_LEFT_CORRIDOR_REMOVED",
        "classification_accept",
        lambda row: row.__setitem__("left_corridor", None),
    )
    add_row(
        "C05_CLASSIFICATION_ENDPOINT_PAIR_REVERSED",
        "classification_accept",
        lambda row: row.__setitem__(
            "unordered_nonself_formal_occurrence_endpoint_pair",
            list(reversed(
                row["unordered_nonself_formal_occurrence_endpoint_pair"]
            )),
        ),
    )
    add_row(
        "C06_CLASSIFICATION_SELF_FLAG_FORGED",
        "classification_accept",
        lambda row: row.__setitem__("same_formal_occurrence_endpoint", True),
    )
    add_row(
        "C07_CLASSIFICATION_FACTOR_FORGED",
        "classification_active",
        forge_active_factor_side,
    )
    add_row(
        "C08_CLASSIFICATION_SQRT_DIGEST_FORGED",
        "classification_accept",
        lambda row: row.__setitem__(
            "common_face_t_boundary_sqrt_enclosures_sha256", "0" * 64
        ),
    )
    add_row(
        "C09_CLASSIFICATION_EARLY_EDGE_CREDIT",
        "classification_accept",
        lambda row: row.__setitem__("formal_component_edge_credit", 1),
    )
    add_row(
        "C10_CLASSIFICATION_REJECT_EXCLUSION_REMOVED",
        "classification_reject",
        lambda row: row.__setitem__("exclusion_evidence", None),
    )

    add_row(
        "R01_RAW_WITNESS_CREDIT_REMOVED",
        "raw",
        lambda row: row.__setitem__(
            "formal_component_edge_witness_credit", 0
        ),
        validate_raw_edge,
    )
    add_row(
        "R02_RAW_EARLY_COMPONENT_EDGE_CREDIT",
        "raw",
        lambda row: row.__setitem__("formal_component_edge_credit", 1),
        validate_raw_edge,
    )
    add_row(
        "R03_RAW_SELF_ENDPOINT_COLLAPSE",
        "raw",
        lambda row: row.__setitem__(
            "unordered_formal_occurrence_endpoint_pair",
            [row["left_formal_occurrence_id"]] * 2,
        ),
        validate_raw_edge,
    )
    add_row(
        "R04_RAW_PATCH_AREA_ZERO",
        "raw",
        lambda row: row.__setitem__("accepted_patch_area", "0"),
        validate_raw_edge,
    )
    add_row(
        "R05_RAW_CORRIDOR_VOLUME_ZERO",
        "raw",
        lambda row: row["left_strict_positive_volume_corridor"].__setitem__(
            "exact_transformed_corridor_volume", "0"
        ),
        validate_raw_edge,
    )
    add_row(
        "R06_RAW_CORRIDOR_FOOTPRINT_FORGED",
        "raw",
        lambda row: row["right_strict_positive_volume_corridor"][
            "exact_positive_volume_transformed_corridor"
        ].__setitem__(2, "999"),
        validate_raw_edge,
    )
    add_row(
        "R07_RAW_SOURCE_HASH_FORGED",
        "raw",
        lambda row: row.__setitem__(
            "source_Round299_classification_row_sha256", "0" * 64
        ),
        validate_raw_edge,
    )
    add_row(
        "R08_RAW_DSU_CREDIT_FORGED",
        "raw",
        lambda row: row.__setitem__("formal_DSU_rank_reduction_credit", 1),
        validate_raw_edge,
    )

    add_row(
        "E01_CANONICAL_ACCEPT_LIST_EMPTIED",
        "canonical",
        lambda row: (
            row.__setitem__("accepted_raw_edge_witness_count", 0),
            row.__setitem__("accepted_raw_edge_witness_row_ids", []),
            row.__setitem__(
                "accepted_raw_edge_witness_row_ids_sha256", digest([])
            ),
        ),
        validate_canonical_edge,
    )
    add_row(
        "E02_CANONICAL_PAIR_REVERSED",
        "canonical",
        lambda row: row.__setitem__(
            "unordered_formal_occurrence_endpoint_pair",
            list(reversed(row["unordered_formal_occurrence_endpoint_pair"])),
        ),
        validate_canonical_edge,
    )
    add_row(
        "E03_CANONICAL_UNIVERSAL_QUANTIFIER",
        "canonical",
        lambda row: row.__setitem__(
            "pair_acceptance_semantics",
            "FOR_ALL_FACES_ACCEPTED",
        ),
        validate_canonical_edge,
    )
    add_row(
        "E04_CANONICAL_EDGE_CREDIT_REMOVED",
        "canonical",
        lambda row: row.__setitem__("formal_component_edge_credit", 0),
        validate_canonical_edge,
    )
    add_row(
        "E05_CANONICAL_IDENTITY_CREDIT_FORGED",
        "canonical",
        lambda row: row.__setitem__(
            "formal_occurrence_identity_collapse_credit", 1
        ),
        validate_canonical_edge,
    )
    add_row(
        "E06_CANONICAL_DSU_CREDIT_FORGED",
        "canonical",
        lambda row: row.__setitem__("formal_DSU_rank_reduction_credit", 1),
        validate_canonical_edge,
    )
    add_row(
        "E07_MIXED_PAIR_REJECT_WITNESSES_DROPPED",
        "canonical_mixed",
        lambda row: (
            row.__setitem__(
                "source_reject_face_row_count_for_same_endpoint_pair", 0
            ),
            row.__setitem__(
                "source_reject_face_row_ids_for_same_endpoint_pair", []
            ),
            row.__setitem__(
                "source_reject_face_row_ids_for_same_endpoint_pair_sha256",
                digest([]),
            ),
        ),
        validate_canonical_edge,
    )
    add_row(
        "E08_MIXED_PAIR_REJECT_NEGATES_ACCEPT",
        "canonical_mixed",
        lambda row: row.__setitem__(
            "a_rejected_face_does_not_negate_an_accepted_face_for_same_pair",
            False,
        ),
        validate_canonical_edge,
    )

    add_row(
        "N01_SELF_NOEDGE_WITNESS_CREDIT_FORGED",
        "no_edge_self",
        lambda row: row.__setitem__(
            "formal_component_edge_witness_credit", 1
        ),
        validate_no_edge,
    )
    add_row(
        "N02_SELF_NOEDGE_COMPONENT_CREDIT_FORGED",
        "no_edge_self",
        lambda row: row.__setitem__("formal_component_edge_credit", 1),
        validate_no_edge,
    )
    add_row(
        "N03_REJECT_EXCLUSION_REMOVED",
        "no_edge_reject",
        lambda row: row.__setitem__("exclusion_evidence", None),
        validate_no_edge,
    )
    add_row(
        "N04_REJECT_DECISION_CHANGED_TO_ACCEPT",
        "no_edge_reject",
        lambda row: row.__setitem__("decision", ACCEPT),
        validate_no_edge,
    )
    add_row(
        "N05_REJECT_DISPOSITION_CHANGED_TO_SELF",
        "no_edge_reject",
        lambda row: row.__setitem__(
            "disposition",
            "ACCEPTED_POSITIVE_PATCH_BUT_SELF_ENDPOINT_NO_EDGE",
        ),
        validate_no_edge,
    )
    add_row(
        "N06_REJECT_MAXIMALITY_CREDIT_FORGED",
        "no_edge_reject",
        lambda row: row.__setitem__("formal_maximality_credit", 1),
        validate_no_edge,
    )

    result = expected["result"]
    result_validator = lambda value: need(
        value == result, "RECONSTRUCTED_EXPECTED_RESULT"
    )
    for attack_id, mutate in (
        (
            "S01_RESULT_CLASSIFICATION_COUNT_FORGED",
            lambda row: row["promotion_contract"].__setitem__(
                "classification_inventory_row_count", 43_091
            ),
        ),
        (
            "S02_RESULT_RAW_EDGE_COUNT_FORGED",
            lambda row: row["promotion_contract"].__setitem__(
                "accepted_nonself_raw_edge_witness_count", 27_855
            ),
        ),
        (
            "S03_RESULT_CANONICAL_EDGE_COUNT_FORGED",
            lambda row: row["promotion_contract"].__setitem__(
                "canonical_occurrence_component_edge_count", 25_451
            ),
        ),
        (
            "S04_RESULT_MIXED_PAIR_COUNT_FORGED",
            lambda row: row["promotion_contract"].__setitem__(
                "accepted_and_rejected_face_pair_overlap_count", 0
            ),
        ),
        (
            "S05_RESULT_UNIVERSAL_QUANTIFIER",
            lambda row: row["promotion_contract"].__setitem__(
                "pair_acceptance_quantifier", "FOR_ALL"
            ),
        ),
        (
            "S06_RESULT_DSU_APPLIED_FORGERY",
            lambda row: row["strict_nonclaims"].__setitem__(
                "component_DSU_applied", True
            ),
        ),
        (
            "S07_RESULT_QUOTIENT_COUNT_FORGERY",
            lambda row: row["strict_nonclaims"].__setitem__(
                "current_quotient_component_count", 106_520
            ),
        ),
        (
            "S08_RESULT_MAXIMALITY_FORGERY",
            lambda row: row["strict_nonclaims"].__setitem__(
                "maximality_proved", True
            ),
        ),
        (
            "S09_RESULT_IDENTITY_COLLAPSE_FORGERY",
            lambda row: row["strict_nonclaims"].__setitem__(
                "accepted_face_connectivity_is_occurrence_identity", True
            ),
        ),
        (
            "S10_RESULT_CM2_FORGERY",
            lambda row: row["strict_nonclaims"].__setitem__("CM2", "GO"),
        ),
    ):
        attacks.append(expect_rejected(
            attack_id,
            result,
            mutate,
            resign_result,
            result_validator,
        ))

    for attack_id, key in (
        ("L01_CLASSIFICATION_ROW_OMITTED", "classification"),
        ("L02_RAW_EDGE_ROW_OMITTED", "raw"),
        ("L03_CANONICAL_EDGE_ROW_OMITTED", "canonical"),
        ("L04_NOEDGE_ROW_OMITTED", "no_edge"),
    ):
        document = expected["documents"][key]
        def mutate_doc(row: dict[str, Any]) -> None:
            row["rows"] = row["rows"][1:]
            row["row_count"] -= 1
            row["rows_sha256"] = digest(row["rows"])
            id_field = {
                "classification":
                    "Round299_independent_signed_face_classification_row_id",
                "raw": "Round299C_signed_face_raw_edge_witness_row_id",
                "canonical":
                    "Round299C_canonical_signed_face_occurrence_edge_row_id",
                "no_edge": "Round299C_signed_face_no_edge_row_id",
            }[key]
            row["row_ids_sha256"] = digest(
                [value[id_field] for value in row["rows"]]
            )
            row["row_hashes_sha256"] = digest(
                [value["row_sha256"] for value in row["rows"]]
            )
        attacks.append(expect_rejected(
            attack_id,
            document,
            mutate_doc,
            lambda value: value,
            lambda value, reference=document: need(
                value == reference, "RECONSTRUCTED_EXPECTED_LEDGER"
            ),
        ))

    base_json = canonical(result) + b"\n"
    serialization_cases = {
        "J01_JSON_DUPLICATE_KEY":
            b'{"schema":"x","schema":"y"}\n',
        "J02_JSON_TRAILING_GARBAGE": base_json + b"x",
        "J03_JSON_NONFINITE": b'{"x":NaN}\n',
        "J04_JSON_NUL": base_json[:-1] + b"\x00\n",
    }
    for attack_id, payload in serialization_cases.items():
        rejected = False
        try:
            strict_json_bytes(payload, "attack")
        except Exception:
            rejected = True
        need(rejected, "ATTACK_ACCEPTED:" + attack_id)
        attacks.append({
            "attack_id": attack_id,
            "classification": "STRICT_JSON_OR_ENCODING_ATTACK",
            "disposition": "REJECTED",
        })

    base_gzip = deterministic_gzip(expected["documents"]["canonical"])
    duplicate_gzip_json = deterministic_gzip({"x": 1})
    gzip_cases = {
        "G01_GZIP_TRUNCATED": base_gzip[:-9],
        "G02_GZIP_CONCATENATED": base_gzip + duplicate_gzip_json,
        "G03_GZIP_NONDETERMINISTIC_HEADER":
            deterministic_gzip(expected["documents"]["canonical"], mtime=1),
    }
    for attack_id, payload in gzip_cases.items():
        rejected = False
        try:
            strict_gzip_bytes(payload, "attack")
        except Exception:
            rejected = True
        need(rejected, "ATTACK_ACCEPTED:" + attack_id)
        attacks.append({
            "attack_id": attack_id,
            "classification": "STRICT_GZIP_ATTACK",
            "disposition": "REJECTED",
        })

    with tempfile.TemporaryDirectory(
        prefix=".round299c-verifier-attacks.", dir=HERE
    ) as temporary:
        temp = Path(temporary)
        dummy = temp / "dummy"
        dummy.write_bytes(b"round299c")

        symlink = temp / "symlink"
        symlink.symlink_to(dummy)
        hardlink = temp / "hardlink"
        os.link(dummy, hardlink)
        path_cases = (
            ("P01_SYMLINK_INPUT", symlink, symlink.name),
            ("P02_HARDLINK_INPUT", hardlink, hardlink.name),
            ("P03_PATH_TRAVERSAL_INPUT", HERE / ".." / RESULT.name, RESULT.name),
        )
        for attack_id, path, name in path_cases:
            rejected = False
            try:
                require_safe_regular(path, name)
            except Exception:
                rejected = True
            need(rejected, "ATTACK_ACCEPTED:" + attack_id)
            attacks.append({
                "attack_id": attack_id,
                "classification": "FILESYSTEM_PATH_ATTACK",
                "disposition": "REJECTED",
            })

    need(
        len({row["attack_id"] for row in attacks}) == len(attacks),
        "UNIQUE_ATTACK_IDS",
    )
    suite = {
        "schema": ATTACK_SCHEMA,
        "status": "PASS_ALL_INDEPENDENT_TARGETED_ATTACKS_REJECTED",
        "attack_count": len(attacks),
        "rejected_count": len(attacks),
        "accepted_count": 0,
        "attacks": attacks,
    }
    suite["attack_suite_sha256"] = digest(suite)
    return suite


def atomic(path: Path, payload: bytes) -> None:
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


def build_verification(
    expected: dict[str, Any],
    candidate_pins: dict[str, str],
    attacks: dict[str, Any],
    attack_bytes: bytes,
) -> dict[str, Any]:
    verification = {
        "schema": VERIFY_SCHEMA,
        "status":
            "PASS_INDEPENDENT_CACHELESS_ROUND299C__43092_CLASSIFICATIONS__"
            "27856_RAW_WITNESSES__25452_CANONICAL_EDGES__"
            "2092_SELF__13144_EXCLUSIONS__4_MIXED_EXISTS_PAIRS__"
            f"{attacks['attack_count']}_OF_{attacks['attack_count']}_"
            "ATTACKS_REJECTED__NO_DSU_OR_MAXIMALITY",
        "independence_contract": {
            "Round299C_producer_imported_or_executed": False,
            "Round299C_producer_parsed_as_Python": False,
            "Round299C_producer_bytes_used_only_as_inert_SHA256_pin": True,
            "persisted_Round299_probe_ledger_used_as_expected_oracle": False,
            "persisted_Round299_probe_result_used_as_expected_oracle": False,
            "pinned_independent_math_source_imported_for_exact_routines": True,
            "all_upstream_math_sources_read_cachelessly": True,
            "expected_43092_classifications_completed_before_candidate_open":
                True,
            "all_three_formal_derived_ledgers_rebuilt_before_candidate_open":
                True,
        },
        "source_reconstruction": {
            "Round292_refinement_cell_count": 11_852,
            "classification_row_count": 43_092,
            "accepted_physical_patch_count": 29_948,
            "accepted_nonself_raw_witness_count": 27_856,
            "canonical_occurrence_edge_pair_count": 25_452,
            "accepted_self_no_edge_count": 2_092,
            "rejected_exclusion_no_edge_count": 13_144,
            "self_and_exclusion_row_count": 15_236,
            "unresolved_contact_count": 0,
            "accepted_and_rejected_pair_overlap_count": 4,
            "pair_acceptance_quantifier": "EXISTS",
            "existing_channel_intersections": {
                "R295A_LOWER": 0,
                "R296_TRUE_SEAM": 0,
                "R297_ORDINARY": 0,
            },
            "upstream_input_pins": dict(sorted(math299.PINS.items())),
            "math_source_sha256": MATH_SOURCE_SHA256,
        },
        "candidate_exact_equality": {
            "all_four_candidate_ledgers_exact_reconstructed_objects": True,
            "all_four_candidate_ledgers_exact_deterministic_bytes": True,
            "candidate_result_exact_reconstructed_object_and_bytes": True,
            "candidate_file_pins": dict(sorted(candidate_pins.items())),
            "candidate_result_self_sha256": RESULT_SELF_SHA256,
            "historical_producer_attack_suite_validated": True,
            "historical_producer_attack_suite_file_sha256":
                CANDIDATE_PINS[PRODUCER_ATTACKS.name],
            "historical_producer_attack_suite_self_sha256":
                PRODUCER_ATTACK_SELF_SHA256,
        },
        "independent_attack_audit": {
            "attack_count": attacks["attack_count"],
            "rejected_count": attacks["rejected_count"],
            "accepted_count": 0,
            "independent_attack_suite_file_sha256":
                hashlib.sha256(attack_bytes).hexdigest(),
            "independent_attack_suite_self_sha256":
                attacks["attack_suite_sha256"],
            "semantic_and_inventory_attack_count": sum(
                row["classification"] == "RESIGNED_SEMANTIC_FORGERY"
                for row in attacks["attacks"]
            ),
            "strict_JSON_GZIP_path_attack_count": sum(
                row["classification"] != "RESIGNED_SEMANTIC_FORGERY"
                for row in attacks["attacks"]
            ),
        },
        "replay_contract": {
            "seed_argument_affects_output": False,
            "PYTHONHASHSEED_affects_output": False,
            "dual_seed_no_write_replay_required": True,
        },
        "formal_credit_audit": {
            "raw_component_edge_witness_credit_total": 27_856,
            "canonical_component_edge_credit_total": 25_452,
            "formal_occurrence_identity_collapse_credit": 0,
            "formal_DSU_rank_reduction_credit": 0,
            "formal_maximality_credit": 0,
            "formal_fibre_credit": 0,
            "formal_global_disposition_credit": 0,
            "component_DSU_applied": False,
            "current_quotient_component_count": None,
            "CM2": "NO_GO_PENDING_COMBINED_DSU_AND_MAXIMALITY_GATES",
        },
        "artifact_transition": {
            "candidate_producer_ledgers_result_and_self_attacks_unchanged":
                True,
            "independent_attack_suite_added_separately": True,
            "final_manifest_required_entry_count": 12,
        },
    }
    verification["verification_sha256"] = digest(verification)
    return verification


def run(seed: int, no_write: bool) -> tuple[dict[str, Any], bytes, bytes]:
    del seed
    require_safe_regular(
        HERE / MATH_SOURCE, MATH_SOURCE, MATH_SOURCE_SHA256
    )
    for filename, pin in math299.PINS.items():
        require_safe_regular(HERE / filename, filename, pin)
    expected = build_expected()
    candidate_pins = open_and_match_candidates(expected)
    attacks = build_attacks(expected)
    attack_bytes = canonical(attacks) + b"\n"
    verification = build_verification(
        expected, candidate_pins, attacks, attack_bytes
    )
    verification_bytes = canonical(verification) + b"\n"
    if no_write:
        require_safe_regular(
            INDEPENDENT_ATTACKS, INDEPENDENT_ATTACKS.name
        )
        require_safe_regular(VERIFICATION, VERIFICATION.name)
        need(
            INDEPENDENT_ATTACKS.read_bytes() == attack_bytes,
            "NO_WRITE_ATTACK_BYTES",
        )
        need(
            VERIFICATION.read_bytes() == verification_bytes,
            "NO_WRITE_VERIFICATION_BYTES",
        )
    else:
        atomic(INDEPENDENT_ATTACKS, attack_bytes)
        atomic(VERIFICATION, verification_bytes)
    return verification, attack_bytes, verification_bytes


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, default=299_351)
    parser.add_argument("--no-write", action="store_true")
    arguments = parser.parse_args()
    verification, attack_bytes, verification_bytes = run(
        arguments.seed, arguments.no_write
    )
    print(verification["status"])
    print(
        "independent_attack_file_sha256="
        + hashlib.sha256(attack_bytes).hexdigest()
    )
    print(
        "independent_attack_self_sha256="
        + verification["independent_attack_audit"][
            "independent_attack_suite_self_sha256"
        ]
    )
    print(
        "verification_file_sha256="
        + hashlib.sha256(verification_bytes).hexdigest()
    )
    print(
        "verification_self_sha256="
        + verification["verification_sha256"]
    )


if __name__ == "__main__":
    main()
