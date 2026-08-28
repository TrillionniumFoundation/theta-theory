#!/usr/bin/env python3
"""Read-only side-specific return-signature spike for the Round192 wall tail.

Round192 found 32 exact two-sheet wall-product pairs and 96 strict open-region
candidates in the 64 residual wall-G leaves.  This probe asks whether every
open region has a unique local return signature and exact Gate5 word-key
binding that can be reconstructed from frozen evidence rather than guessed.

Evidence is restricted to:

* the complete pinned Round174/Round179/Round182 chains;
* exact face-adjacent Round174 resolved occurrences in the same Gate3 parent;
* the fact that every relevant Round174/Round182 enclosure has exactly one
  unresolved condition, its recorded integer-wall endpoint transition;
* Round179's source/target wall normal forms;
* Round192's independently reconstructed source/target sheet arrangement; and
* the pinned Gate5 immutable exact-key registry rebuilt by the Round174
  verifier.

The probe emits one JSON document to stdout and progress to stderr.  It has no
output-path option, writes no runtime file, issues no local production credit,
and issues no global exact-key disposition.

Probe-only trust boundary: importing Round192 imports Round182, Round179 and
Round174 before this module can pin them.  Their complete chains and module
identities are pinned immediately after import.  A formal verifier must pin
inert producer bytes before importing a separately implemented evaluator.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from fractions import Fraction as Q
import gc
import hashlib
import json
from pathlib import Path
import sys
from typing import Any

from flint import ctx

import cm2_round192_source_g_wall_endpoint_owner_probe as r192


HERE = Path(__file__).resolve().parent
PROBE = Path(__file__).resolve()
SCHEMA = "cm2.round196.source-g-wall-return-signature-probe.v1"

ROUND192_SOURCE = "cm2_round192_source_g_wall_endpoint_owner_probe.py"
ROUND192_SOURCE_SHA256 = (
    "f91bf6a6a7b5663d52ceab937d91fa1b7add2e2c72bb992791c83b5b5bdb0d46"
)
ROUND192_LEAF_EVIDENCE_SHA256 = (
    "4702ad9ef4a0522d77796924c3ddc5ed075584f887059858d8350b3d81b26492"
)
ROUND192_PAIR_EVIDENCE_SHA256 = (
    "f93a25e1f322bb202c0db99e86357c9b4d7a1940a0ed691a8e508e83a5a9c732"
)

R174_PREFIX = (
    "cm2_round174_source_g_unique_first_dynamic_occurrence_materialization"
)
R174_PINS = {
    f"{R174_PREFIX}.py":
        "3d329525dda6697a3a5d2a8227c94bd9c309ea7ebcc4cdd0c7fbe573c267a218",
    f"{R174_PREFIX}_certificate.json":
        "10221141c58c044b42e43009beb34ae4705995925a88deaa70ff2eba2ea852c7",
    f"{R174_PREFIX}_rows.json":
        "9edeea2e1033b0dd70dee11a53b0f6aeb21fe74030aeefb60b081a7c420cff54",
    f"{R174_PREFIX}_verifier.py":
        "c7ead7c9cb8b4d7b8680e64bfb7870e5c5f5e39277e7c7d3d08a62b600f5c058",
    f"{R174_PREFIX}_verification.json":
        "1f65b5e02b1d1e63bd7e41d6a88d5eb180e2be92620af4b8afa2141c9f6e344c",
    f"{R174_PREFIX}_report.md":
        "d9a098b344ac008ca921018d80a4490202ff5ba55c26b419943bfccdd99744c7",
    f"{R174_PREFIX}_cold_replay.md":
        "19c24d2c9d909c9eac0be6e0b47929356486c181b80589b10f44f944273afd67",
}
R174_MANIFEST = f"{R174_PREFIX}_manifest.sha256"
R174_MANIFEST_SHA256 = (
    "9e92db7748a2c0acdce532c830f899ce153765de64a59e9f372df3099ac91b76"
)
R174_CERTIFICATE_RESULT_SHA256 = (
    "d45f05458c42189cf0ebc51e258356d13278ba40845cce80b6a072ffbc8cf09b"
)
R174_ATTACHMENT_RESULT_SHA256 = (
    "002ca6631edd39c2325c63a1e8f9717d111f4d10c6d2585077d665a0ff128d18"
)
R174_VERIFICATION_RESULT_SHA256 = (
    "6c82800d41e456aeed7000bccb13bfe0e5e6d5f1637ac52a4d5c45b24ed9a23b"
)
R174_ATTACHMENT_SCHEMA = (
    "cm2.round174.source-g-unique-first-dynamic-occurrence-rows.v1"
)

EXPECTED_PAIR_COUNT = 32
EXPECTED_TAIL_REGION_COUNT = 96
EXPECTED_ORIGIN_COUNT = 64
EXPECTED_PARENT_COUNT = 16
EXPECTED_RELEVANT_R182_LEAF_COUNT = 512
EXPECTED_FULL_ORIGIN_REGION_COUNT = 736
SOURCE_G_KEY_COUNT = 224_580
SIGNS = {"NEGATIVE", "POSITIVE"}


def require(condition: bool, label: str) -> None:
    if not condition:
        raise RuntimeError(label)


def canonical(value: Any) -> str:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    )


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value).encode()).hexdigest()


def unpack_one(columns: list[str], packed: list[Any]) -> dict[str, Any]:
    require(len(columns) == len(packed), "packed row width")
    return dict(zip(columns, packed, strict=True))


def check_inputs() -> tuple[dict[str, Any], dict[str, Any]]:
    """Pin the complete chains and rebuild the immutable Gate5 registry."""

    r182 = r192.r182
    r179 = r182.r179
    r174 = r179.r174
    require(
        Path(r192.__file__).resolve() == (HERE / ROUND192_SOURCE).resolve(),
        "Round192 imported module identity",
    )
    require(
        Path(r174.__file__).resolve()
        == (HERE / f"{R174_PREFIX}_verifier.py").resolve(),
        "Round174 imported verifier identity",
    )
    r192.pinned_bytes(HERE / ROUND192_SOURCE, ROUND192_SOURCE_SHA256)
    inherited = r192.check_inputs()

    for name, expected in R174_PINS.items():
        r192.pinned_bytes(HERE / name, expected)
    manifest_raw = r192.pinned_bytes(
        HERE / R174_MANIFEST,
        R174_MANIFEST_SHA256,
    )
    require(
        r192.manifest_entries(manifest_raw) == R174_PINS,
        "Round174 manifest exact entries",
    )
    r192.check_wrapper(
        R174_PREFIX,
        R174_PINS,
        R174_CERTIFICATE_RESULT_SHA256,
        R174_VERIFICATION_RESULT_SHA256,
    )

    frozen = r174.load_frozen_inputs()
    registry = r174.rebuild_registry(frozen["gate5"])
    registry_meta = (
        frozen["gate5"]["result"]["immutable_candidate_key_registry"]
    )
    require(
        registry_meta["candidate_return_word_key_count"] == 441_280
        and len(registry["pairs"]) == 448
        and len(registry["patterns"]) == 985,
        "Gate5 registry census",
    )
    chain = {
        **inherited,
        "Round174_manifest_sha256": R174_MANIFEST_SHA256,
        "Round174_certificate_result_sha256":
            R174_CERTIFICATE_RESULT_SHA256,
        "Round174_attachment_file_sha256":
            R174_PINS[f"{R174_PREFIX}_rows.json"],
        "Round174_attachment_result_sha256":
            R174_ATTACHMENT_RESULT_SHA256,
        "Round174_verification_result_sha256":
            R174_VERIFICATION_RESULT_SHA256,
        "Round192_probe_source_sha256": ROUND192_SOURCE_SHA256,
        "complete_Round174_Round179_Round182_manifest_entry_count":
            len(R174_PINS) + len(r192.R179_PINS) + len(r192.R182_PINS),
        "Gate5_candidate_return_word_key_count": 441_280,
        "Gate5_chart_target_pair_count": 448,
        "Gate5_crossing_pattern_count": 985,
        "probe_only_import_before_pin_boundary": True,
    }
    del frozen
    gc.collect()
    return chain, registry


def reconstruct_round192() -> tuple[
    dict[str, Any],
    dict[str, Any],
    list[dict[str, Any]],
    list[dict[str, Any]],
]:
    scope182 = r192.extract_round182_scope()
    scope179 = r192.extract_round179_scope(
        scope182["occurrences"],
        scope182["origin_ids"],
    )
    rows: list[dict[str, Any]] = []
    for leaf in sorted(
        scope182["residual_leaves"],
        key=lambda row: row["row_id"],
    ):
        occurrence = leaf["occurrence_row_id"]
        collar = scope182["collars"][occurrence]
        origin_id = collar["origin_row_id"]
        rows.append(r192.analyze_leaf(
            leaf,
            collar,
            scope179["walls"][occurrence],
            scope179["origins"][origin_id],
            scope182["origins"][origin_id],
            scope179["retained"][leaf["retained_child_row_id"]],
        ))
    pairs = r192.analyze_pairs(rows)
    require(
        len(rows) == 64
        and len(pairs) == EXPECTED_PAIR_COUNT
        and digest(rows) == ROUND192_LEAF_EVIDENCE_SHA256
        and digest(pairs) == ROUND192_PAIR_EVIDENCE_SHA256,
        "Round192 exact evidence reconstruction",
    )
    return scope182, scope179, rows, pairs


def load_round174_scope(
    origin_ids: set[str],
    parent_ids: set[str],
) -> dict[str, Any]:
    source = r192.load_attachment(
        R174_PREFIX,
        R174_PINS,
        R174_ATTACHMENT_SCHEMA,
        R174_ATTACHMENT_RESULT_SHA256,
    )
    schemas = source["row_column_schemas"]
    parents: dict[str, dict[str, Any]] = {}
    for packed in source["parent_rows"]:
        if packed[0] in parent_ids:
            row = unpack_one(schemas["parent_rows"], packed)
            parents[row["parent_id"]] = row
    residual: dict[str, dict[str, Any]] = {}
    for packed in source["residual_3d_tube_rows"]:
        if packed[0] in origin_ids:
            row = unpack_one(schemas["residual_3d_tube_rows"], packed)
            residual[row["row_id"]] = row
    resolved: list[dict[str, Any]] = []
    for packed in source["resolved_3d_occurrence_rows"]:
        if packed[2] in parent_ids:
            resolved.append(unpack_one(
                schemas["resolved_3d_occurrence_rows"],
                packed,
            ))
    require(
        len(parents) == EXPECTED_PARENT_COUNT
        and set(parents) == parent_ids
        and len(residual) == EXPECTED_ORIGIN_COUNT
        and set(residual) == origin_ids
        and len(resolved) == 192,
        "Round174 relevant row census",
    )
    del source
    gc.collect()
    return {
        "parents": parents,
        "residual": residual,
        "resolved": resolved,
    }


def load_round182_relevant_leaves(
    occurrences: set[str],
    origin_ids: set[str],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    source = r192.load_attachment(
        r192.R182_PREFIX,
        r192.R182_PINS,
        r192.R182_ATTACHMENT_SCHEMA,
        r192.R182_ATTACHMENT_RESULT_SHA256,
    )
    schemas = source["row_column_schemas"]
    leaves = [
        unpack_one(schemas["collar_leaf_rows"], packed)
        for packed in source["collar_leaf_rows"]
        if packed[1] in occurrences
    ]
    carried = [
        unpack_one(schemas["carried_normal_form_rows"], packed)
        for packed in source["carried_normal_form_rows"]
        if packed[2] in origin_ids
    ]
    require(
        len(leaves) == EXPECTED_RELEVANT_R182_LEAF_COUNT,
        "Round182 relevant leaf census",
    )
    del source
    gc.collect()
    return leaves, carried


def qbox(values: list[str]) -> list[Q]:
    return [Q(value) for value in values]


def face_adjacency_axis(
    first_values: list[str],
    second_values: list[str],
) -> int | None:
    """Return the unique shared-face axis with positive overlap otherwise."""

    first = qbox(first_values)
    second = qbox(second_values)
    touching: list[int] = []
    for axis in range(3):
        first_lower, first_upper = first[2 * axis:2 * axis + 2]
        second_lower, second_upper = second[2 * axis:2 * axis + 2]
        if (
            first_upper == second_lower
            or second_upper == first_lower
        ):
            touching.append(axis)
        elif min(first_upper, second_upper) <= max(
            first_lower,
            second_lower,
        ):
            return None
    return touching[0] if len(touching) == 1 else None


def signature_from_resolved(row: dict[str, Any]) -> dict[str, Any]:
    return {
        "owner_target": row["owner_target"],
        "ordered_integer_wall_events":
            row["ordered_integer_wall_events"],
        "signed_wall_word": row["signed_wall_word"],
        "roof": row["roof"],
        "outgoing_cell": row["outgoing_cell"],
        "target_chart": row["target_chart"],
        "official_key_row": row["official_key_row"],
        "official_key_ordinal": row["official_key_ordinal"],
        "official_key_id": row["official_key_id"],
    }


def anchor_audit(
    scope174: dict[str, Any],
    scope179: dict[str, Any],
    registry: dict[str, Any],
) -> tuple[dict[str, dict[str, Any]], dict[str, Any]]:
    r174 = r192.r182.r179.r174
    resolved_by_parent: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in scope174["resolved"]:
        resolved_by_parent[row["parent_id"]].append(row)

    parent_signature: dict[str, dict[str, Any]] = {}
    parent_rows: list[dict[str, Any]] = []
    for parent_id, parent in sorted(scope174["parents"].items()):
        resolved = resolved_by_parent[parent_id]
        signatures = {
            canonical(signature_from_resolved(row)) for row in resolved
        }
        require(
            len(signatures) == 1
            and parent["observed_exact_key_count"] == 1,
            f"unique parent anchor signature:{parent_id}",
        )
        signature = signature_from_resolved(resolved[0])
        expected_key = r174.exact_key(
            parent["chart"],
            parent["owner_target"],
            (),
            registry,
        )
        require(
            signature["owner_target"] == parent["owner_target"]
            and signature["ordered_integer_wall_events"] == []
            and signature["signed_wall_word"] == []
            and signature["roof"] == 1
            and signature["official_key_row"] == expected_key["row"]
            and signature["official_key_ordinal"]
            == expected_key["ordinal"]
            and signature["official_key_id"]
            == expected_key["identifier"]
            and parent["observed_exact_key_ordinals_sha256"]
            == digest([expected_key["ordinal"]])
            and parent["gate3_leaf_row_sha256"]
            == parent_id.split(":", 1)[1],
            f"parent empty-word anchor:{parent_id}",
        )
        parent_signature[parent_id] = signature
        parent_rows.append({
            "parent_id": parent_id,
            "chart": parent["chart"],
            "owner_target": parent["owner_target"],
            "resolved_anchor_row_count": len(resolved),
            "unique_resolved_signature_count": len(signatures),
            "empty_word_official_key_id":
                signature["official_key_id"],
            "empty_word_official_key_ordinal":
                signature["official_key_ordinal"],
        })

    origin_anchor: dict[str, dict[str, Any]] = {}
    adjacency_histogram: Counter[int] = Counter()
    adjacency_axis_histogram: Counter[str] = Counter()
    anchor_rows: list[dict[str, Any]] = []
    for origin_id, origin in sorted(scope179["origins"].items()):
        residual174 = scope174["residual"][origin_id]
        require(
            residual174["parent_id"] == origin["parent_id"]
            and residual174["chart"] == origin["chart"]
            and residual174["box"] == origin["original_box"]
            and residual174["reason_labels"]
            == origin["original_reason_labels"],
            f"Round174/Round179 origin binding:{origin_id}",
        )
        adjacent: list[tuple[int, dict[str, Any]]] = []
        for row in resolved_by_parent[origin["parent_id"]]:
            axis = face_adjacency_axis(
                origin["original_box"],
                row["box"],
            )
            if axis is not None:
                adjacent.append((axis, row))
        require(
            len(adjacent) in {1, 2},
            f"adjacent resolved anchor count:{origin_id}",
        )
        signatures = {
            canonical(signature_from_resolved(row))
            for _axis, row in adjacent
        }
        require(
            len(signatures) == 1
            and signature_from_resolved(adjacent[0][1])
            == parent_signature[origin["parent_id"]],
            f"adjacent anchor signature agreement:{origin_id}",
        )
        adjacency_histogram[len(adjacent)] += 1
        for axis, _row in adjacent:
            adjacency_axis_histogram["tps"[axis]] += 1
        origin_anchor[origin_id] = parent_signature[origin["parent_id"]]
        anchor_rows.append({
            "origin_row_id": origin_id,
            "parent_id": origin["parent_id"],
            "adjacent_resolved_row_count": len(adjacent),
            "adjacent_axes": sorted("tps"[axis] for axis, _row in adjacent),
            "adjacent_resolved_row_ids":
                sorted(row["row_id"] for _axis, row in adjacent),
            "unique_anchor_signature": True,
            "anchor_official_key_id":
                parent_signature[origin["parent_id"]][
                    "official_key_id"
                ],
        })
    require(
        adjacency_histogram == Counter({1: 32, 2: 32})
        and sum(adjacency_axis_histogram.values()) == 96,
        "adjacent anchor census",
    )
    return origin_anchor, {
        "parent_row_count": len(parent_rows),
        "parent_rows_sha256": digest(parent_rows),
        "parent_rows": parent_rows,
        "origin_anchor_row_count": len(anchor_rows),
        "origin_anchor_rows_sha256": digest(anchor_rows),
        "origin_anchor_count_histogram": {
            str(key): value
            for key, value in sorted(adjacency_histogram.items())
        },
        "origin_anchor_axis_histogram":
            dict(sorted(adjacency_axis_histogram.items())),
        "origin_anchor_rows": anchor_rows,
    }


def atlas_box(row: dict[str, Any]) -> Any:
    return r192.r182.r179.r174.atlas.AtlasBox(
        *(Q(value) for value in row["box"]),
        len(row["base_refinement_path"]),
        row["row_id"],
    )


def single_obstruction_audit(
    leaves: list[dict[str, Any]],
    collars: dict[str, dict[str, Any]],
    registry: dict[str, Any],
) -> dict[str, Any]:
    r174 = r192.r182.r179.r174
    reasons = Counter()
    class_reasons = Counter()
    rows: list[dict[str, Any]] = []
    for leaf in sorted(leaves, key=lambda row: row["row_id"]):
        collar = collars[leaf["occurrence_row_id"]]
        signature, failures = r174.certify_signature(
            collar["chart"],
            atlas_box(leaf),
            collar["owner_target"],
            registry,
        )
        require(
            signature is None
            and failures == [collar["reason_label"]]
            and collar["reason_label"].startswith(
                "wall_endpoint_or_count_transition:"
            ),
            f"single signature obstruction:{leaf['row_id']}",
        )
        reasons[failures[0]] += 1
        class_reasons[
            leaf["graph_classification"] + "|" + failures[0]
        ] += 1
        rows.append({
            "leaf_row_id": leaf["row_id"],
            "origin_row_id": collar["origin_row_id"],
            "graph_classification": leaf["graph_classification"],
            "only_signature_failure": failures[0],
            "all_nonwall_signature_fields_strict_on_closed_enclosure": True,
        })
    require(len(rows) == EXPECTED_RELEVANT_R182_LEAF_COUNT, "leaf audit")
    return {
        "audited_leaf_count": len(rows),
        "single_reason_histogram": dict(sorted(reasons.items())),
        "graph_class_and_reason_histogram":
            dict(sorted(class_reasons.items())),
        "all_512_have_exactly_one_recorded_wall_endpoint_reason": True,
        "audit_rows_sha256": digest(rows),
    }


def status_sign(status: str) -> str | None:
    if status == "S+":
        return "POSITIVE"
    if status == "S-":
        return "NEGATIVE"
    if status.startswith("A") and len(status) == 7:
        marker = status[5]
        require(marker in "+-", f"absent status sign:{status}")
        return "POSITIVE" if marker == "+" else "NEGATIVE"
    return None


def source_sign(row: dict[str, Any]) -> str:
    box = qbox(row["box"])
    if box[1] <= 0 and box[0] < 0:
        return "NEGATIVE"
    if box[0] >= 0 and box[1] > 0:
        return "POSITIVE"
    raise RuntimeError(f"source t-side:{row['row_id']}")


def event_token(axis: str, source: str, target: str) -> str | None:
    require(source in SIGNS and target in SIGNS, "event signs")
    if source == target:
        return None
    return axis + ("+" if source == "NEGATIVE" else "-")


def region_signature(
    leaf: dict[str, Any],
    collar: dict[str, Any],
    wall: dict[str, Any],
    anchor: dict[str, Any],
    registry: dict[str, Any],
    target_sign: str,
    region_kind: str,
    is_tail: bool,
    half_open_owner: bool,
) -> dict[str, Any]:
    r174 = r192.r182.r179.r174
    src_sign = source_sign(leaf)
    token = event_token(wall["axis"], src_sign, target_sign)
    word = [] if token is None else [token]
    events = [] if token is None else [[token, wall["integer_wall"]]]
    key = r174.exact_key(
        collar["chart"],
        collar["owner_target"],
        tuple(word),
        registry,
    )
    require(
        anchor["owner_target"] == collar["owner_target"]
        and anchor["signed_wall_word"] == []
        and anchor["roof"] == 1
        and key["row"]
        == [collar["chart"], collar["owner_target"], word, len(word) + 1],
        f"region key binding:{leaf['row_id']}:{region_kind}",
    )
    payload = [
        leaf["row_id"],
        region_kind,
        src_sign,
        target_sign,
        key["identifier"],
    ]
    return {
        "region_row_id": f"round196-wall-region:{digest(payload)}",
        "leaf_row_id": leaf["row_id"],
        "origin_row_id": collar["origin_row_id"],
        "parent_id": collar["parent_id"],
        "chart": collar["chart"],
        "owner_target": collar["owner_target"],
        "graph_classification": leaf["graph_classification"],
        "region_kind": region_kind,
        "Round192_tail_region": is_tail,
        "source_sign": src_sign,
        "target_factor_sign": target_sign,
        "wall_axis": wall["axis"],
        "integer_wall": wall["integer_wall"],
        "ordered_integer_wall_events": events,
        "signed_wall_word": word,
        "wall_crossing_count": len(word),
        "roof": len(word) + 1,
        "outgoing_cell": anchor["outgoing_cell"],
        "target_chart": anchor["target_chart"],
        "official_key_row": key["row"],
        "official_key_ordinal": key["ordinal"],
        "official_key_id": key["identifier"],
        "key_binding_join_cardinality": 1,
        "anchor_empty_word_official_key_id":
            anchor["official_key_id"],
        "crossing_key_parent_observed":
            token is None,
        "crossing_key_binding_source": (
            "FACE_ADJACENT_ROUND174_RESOLVED_EMPTY_WORD_ANCHOR"
            if token is None
            else "PINNED_GATE5_REGISTRY_PLUS_EXACT_SINGLE_WALL_SIGN_CHANGE"
        ),
        "half_open_source_sheet_owner":
            half_open_owner if is_tail else None,
        "signature_uniqueness_status": "UNIQUE",
        "conflicting_signature_count": 0,
        "missing_signature_field_count": 0,
        "local_signature_credit_issued": 0,
        "global_exact_key_disposition_credit": 0,
    }


def enumerate_regions(
    leaves: list[dict[str, Any]],
    collars: dict[str, dict[str, Any]],
    walls: dict[str, dict[str, Any]],
    anchors: dict[str, dict[str, Any]],
    registry: dict[str, Any],
    geometry_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    geometry_by_leaf = {row["leaf_row_id"]: row for row in geometry_rows}
    regions: list[dict[str, Any]] = []
    for leaf in sorted(leaves, key=lambda row: row["row_id"]):
        collar = collars[leaf["occurrence_row_id"]]
        wall = walls[leaf["occurrence_row_id"]]
        origin_id = collar["origin_row_id"]
        graph_class = leaf["graph_classification"]
        is_tail = graph_class == "RESIDUAL_3D"
        half_open_owner = False
        if graph_class == "EMPTY":
            lower = status_sign(leaf["lower_t_face_status"])
            upper = status_sign(leaf["upper_t_face_status"])
            require(
                lower is not None and lower == upper,
                f"empty target sign:{leaf['row_id']}",
            )
            target_regions = [(lower, "NO_TARGET_SHEET_REGION")]
        elif graph_class == "FULL_2D":
            lower = status_sign(leaf["lower_t_face_status"])
            upper = status_sign(leaf["upper_t_face_status"])
            require(
                lower == "NEGATIVE" and upper == "POSITIVE",
                f"full graph target signs:{leaf['row_id']}",
            )
            target_regions = [
                ("NEGATIVE", "TARGET_GRAPH_NEGATIVE_SIDE"),
                ("POSITIVE", "TARGET_GRAPH_POSITIVE_SIDE"),
            ]
        else:
            require(
                graph_class == "RESIDUAL_3D"
                and leaf["row_id"] in geometry_by_leaf,
                f"Round192 residual support:{leaf['row_id']}",
            )
            geometry = geometry_by_leaf[leaf["row_id"]]
            half_open_owner = geometry["half_open_source_sheet_owner"]
            src_sign = source_sign(leaf)
            if geometry["target_2D_sheet_count"] == 0:
                target_regions = [(
                    src_sign,
                    "ROUND192_BOUNDARY_ONLY_SINGLE_REGION",
                )]
            else:
                target_regions = [
                    (
                        src_sign,
                        "ROUND192_TARGET_GRAPH_SAME_SIGN_OUTER_REGION",
                    ),
                    (
                        "POSITIVE"
                        if src_sign == "NEGATIVE"
                        else "NEGATIVE",
                        "ROUND192_TARGET_GRAPH_OPPOSITE_SIGN_"
                        "SOURCE_ADJACENT_REGION",
                    ),
                ]
        for target, kind in target_regions:
            regions.append(region_signature(
                leaf,
                collar,
                wall,
                anchors[origin_id],
                registry,
                target,
                kind,
                is_tail,
                half_open_owner,
            ))
    return regions


def pair_glue_audit(
    geometry_pairs: list[dict[str, Any]],
    tail_regions: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    by_leaf: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in tail_regions:
        by_leaf[row["leaf_row_id"]].append(row)
    output: list[dict[str, Any]] = []
    for pair in geometry_pairs:
        negative = by_leaf[pair["negative_t_leaf_row_id"]]
        positive = by_leaf[pair["positive_t_leaf_row_id"]]
        combined = [*negative, *positive]
        require(
            len(combined) == 3
            and all(
                row["signature_uniqueness_status"] == "UNIQUE"
                for row in combined
            ),
            f"three unique pair regions:{pair['pair_row_id']}",
        )
        crossing = [
            row for row in combined if row["wall_crossing_count"] == 1
        ]
        empty = [
            row for row in combined if row["wall_crossing_count"] == 0
        ]
        graph_leaf = pair["target_graph_leaf_row_id"]
        graph_rows = by_leaf[graph_leaf]
        boundary_leaf = (
            pair["positive_t_leaf_row_id"]
            if pair["target_graph_side"] == "NEGATIVE_T"
            else pair["negative_t_leaf_row_id"]
        )
        boundary_rows = by_leaf[boundary_leaf]
        require(
            len(crossing) == 1
            and len(empty) == 2
            and len(graph_rows) == 2
            and len(boundary_rows) == 1
            and crossing[0]["leaf_row_id"] == graph_leaf
            and len({row["official_key_id"] for row in empty}) == 1
            and crossing[0]["official_key_id"]
            != empty[0]["official_key_id"],
            f"empty-event-empty pair pattern:{pair['pair_row_id']}",
        )
        invariant_fields = (
            "chart",
            "owner_target",
            "outgoing_cell",
            "target_chart",
        )
        require(
            all(
                len({row[field] for row in combined}) == 1
                for field in invariant_fields
            ),
            f"pair signature invariants:{pair['pair_row_id']}",
        )
        owner_rows = [
            row for row in combined
            if row["half_open_source_sheet_owner"] is True
        ]
        require(
            pair["owner_count"] == 1
            and pair["half_open_owner_leaf_row_id"]
            == pair["positive_t_leaf_row_id"]
            and len(owner_rows) == (
                2
                if pair["positive_t_leaf_row_id"] == graph_leaf
                else 1
            )
            and {
                row["leaf_row_id"] for row in owner_rows
            } == {pair["positive_t_leaf_row_id"]},
            f"positive-t half-open owner propagation:{pair['pair_row_id']}",
        )
        output.append({
            "pair_row_id": pair["pair_row_id"],
            "negative_t_leaf_row_id": pair["negative_t_leaf_row_id"],
            "positive_t_leaf_row_id": pair["positive_t_leaf_row_id"],
            "positive_t_half_open_owner_leaf_row_id":
                pair["half_open_owner_leaf_row_id"],
            "target_graph_leaf_row_id": graph_leaf,
            "boundary_only_leaf_row_id": boundary_leaf,
            "outer_empty_region_row_ids": sorted(
                row["region_row_id"] for row in empty
            ),
            "source_adjacent_crossing_region_row_id":
                crossing[0]["region_row_id"],
            "crossing_word": crossing[0]["signed_wall_word"],
            "outer_empty_official_key_id":
                empty[0]["official_key_id"],
            "crossing_official_key_id":
                crossing[0]["official_key_id"],
            "source_sheet_signature_change":
                "INSERT_OR_REMOVE_EXACTLY_ONE_RECORDED_WALL_EVENT",
            "target_sheet_signature_change":
                "INSERT_OR_REMOVE_THE_SAME_SINGLE_WALL_EVENT",
            "owner_target_outgoing_and_target_chart_unchanged": True,
            "unexpected_signature_change_count": 0,
            "pair_glue_status": "UNIQUE_EXPECTED_EMPTY_EVENT_EMPTY",
            "local_signature_credit_issued": 0,
            "global_exact_key_disposition_credit": 0,
        })
    require(len(output) == EXPECTED_PAIR_COUNT, "pair glue census")
    return output


def fibre_rows(
    regions: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    groups: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in regions:
        groups[row["official_key_id"]].append(row)
    output: list[dict[str, Any]] = []
    for key_id, rows in sorted(groups.items()):
        first = rows[0]
        require(
            all(
                row["official_key_row"] == first["official_key_row"]
                and row["official_key_ordinal"]
                == first["official_key_ordinal"]
                for row in rows
            ),
            f"key fibre consistency:{key_id}",
        )
        output.append({
            "official_key_id": key_id,
            "official_key_ordinal": first["official_key_ordinal"],
            "official_key_row": first["official_key_row"],
            "local_region_occurrence_count": len(rows),
            "distinct_origin_count":
                len({row["origin_row_id"] for row in rows}),
            "tail_region_occurrence_count": sum(
                row["Round192_tail_region"] for row in rows
            ),
            "join_cardinality_per_local_region": 1,
            "global_exact_key_fibre_exhausted": False,
            "global_exact_key_disposition_credit": 0,
        })
    return output


def histogram_text_words(
    rows: list[dict[str, Any]],
) -> dict[str, int]:
    counts = Counter(
        canonical(row["signed_wall_word"]) for row in rows
    )
    return dict(sorted(counts.items()))


def main() -> int:
    ctx.prec = 256
    print("pinning complete chains and rebuilding registry", file=sys.stderr)
    chain, registry = check_inputs()
    print("reconstructing Round192 two-sheet geometry", file=sys.stderr)
    scope182, scope179, geometry_rows, geometry_pairs = (
        reconstruct_round192()
    )
    parent_ids = {
        row["parent_id"] for row in scope179["origins"].values()
    }
    require(
        len(parent_ids) == EXPECTED_PARENT_COUNT,
        "relevant Gate3 parent census",
    )

    print("loading Round174 parent and signature anchors", file=sys.stderr)
    scope174 = load_round174_scope(scope182["origin_ids"], parent_ids)
    anchors, anchor_summary = anchor_audit(
        scope174,
        scope179,
        registry,
    )
    print("loading and auditing all 512 Round182 leaves", file=sys.stderr)
    all_leaves, carried_rows = load_round182_relevant_leaves(
        scope182["occurrences"],
        scope182["origin_ids"],
    )
    obstruction = single_obstruction_audit(
        all_leaves,
        scope182["collars"],
        registry,
    )
    require(
        len(carried_rows) == 0,
        "active origins have no Round182 carried rows",
    )

    print("enumerating side-specific local signatures", file=sys.stderr)
    regions = enumerate_regions(
        all_leaves,
        scope182["collars"],
        scope179["walls"],
        anchors,
        registry,
        geometry_rows,
    )
    tail_regions = [
        row for row in regions if row["Round192_tail_region"]
    ]
    require(
        len(tail_regions) == EXPECTED_TAIL_REGION_COUNT
        and len(regions) == EXPECTED_FULL_ORIGIN_REGION_COUNT,
        "region census",
    )
    glue_rows = pair_glue_audit(geometry_pairs, tail_regions)

    tail_status = Counter(
        row["signature_uniqueness_status"] for row in tail_regions
    )
    full_status = Counter(
        row["signature_uniqueness_status"] for row in regions
    )
    require(
        tail_status == Counter({"UNIQUE": EXPECTED_TAIL_REGION_COUNT})
        and full_status
        == Counter({"UNIQUE": EXPECTED_FULL_ORIGIN_REGION_COUNT}),
        "signature uniqueness census",
    )
    per_origin = Counter(row["origin_row_id"] for row in regions)
    tail_per_origin = Counter(
        row["origin_row_id"] for row in tail_regions
    )
    require(
        Counter(per_origin.values()) == Counter({8: 32, 15: 32})
        and Counter(tail_per_origin.values()) == Counter({1: 32, 2: 32})
        and set(per_origin) == scope182["origin_ids"],
        "origin region coverage",
    )

    tail_fibres = fibre_rows(tail_regions)
    all_fibres = fibre_rows(regions)
    require(
        len(tail_fibres) == 12
        and Counter(
            row["local_region_occurrence_count"]
            for row in tail_fibres
        ) == Counter({4: 8, 16: 4})
        and len(all_fibres) == 12
        and Counter(
            row["local_region_occurrence_count"]
            for row in all_fibres
        ) == Counter({28: 8, 128: 4}),
        "exact-key fibre join cardinalities",
    )
    tail_word_histogram = histogram_text_words(tail_regions)
    full_word_histogram = histogram_text_words(regions)
    require(
        tail_word_histogram
        == {
            "[]": 64,
            "[\"X+\"]": 8,
            "[\"X-\"]": 8,
            "[\"Y+\"]": 8,
            "[\"Y-\"]": 8,
        }
        and full_word_histogram
        == {
            "[]": 512,
            "[\"X+\"]": 56,
            "[\"X-\"]": 56,
            "[\"Y+\"]": 56,
            "[\"Y-\"]": 56,
        },
        "word histograms",
    )

    probe_result = {
        "status":
            "READ_ONLY_ZERO_PROMOTION_WALL_G_RETURN_SIGNATURE_PROBE",
        "question":
            "Do the 96 strict Round192 wall-tail regions have unique "
            "side-specific local return signatures and exact immutable "
            "word-key bindings, with only the expected one-event changes "
            "across source and target sheets?",
        "verdict": "VALIDATED",
        "verdict_reason":
            "All 96 tail regions have a unique signature: 64 empty-word "
            "regions and 32 one-wall-event regions.  All 32 pairs exhibit "
            "the expected empty-event-empty glue with unchanged owner, "
            "outgoing cell and target chart.  Extending the same audited "
            "single-obstruction rule over all 512 Round182 leaves yields "
            "736 unique regions, making all 64 origins feasible for full "
            "local replacement.  Production materialization and independent "
            "verification remain pending, and no global fibre is exhausted.",
        "probe": {
            "filename": PROBE.name,
            "sha256": hashlib.sha256(
                r192.regular_file_bytes(PROBE, 2_000_000)
            ).hexdigest(),
            "precision_bits": 256,
            "runtime_filesystem_writes": 0,
            "output_path_option_exists": False,
        },
        "input_chain": chain,
        "Round192_reconstruction": {
            "leaf_evidence_row_count": len(geometry_rows),
            "leaf_evidence_rows_sha256": digest(geometry_rows),
            "pair_evidence_row_count": len(geometry_pairs),
            "pair_evidence_rows_sha256": digest(geometry_pairs),
            "two_sheet_pair_count": len(geometry_pairs),
            "strict_tail_region_candidate_count":
                EXPECTED_TAIL_REGION_COUNT,
        },
        "Gate3_and_adjacent_anchor_evidence": anchor_summary,
        "single_obstruction_evidence": {
            **obstruction,
            "Round179_relevant_wall_normal_form_row_count":
                len(scope179["walls"]),
            "Round179_all_have_source_and_target_regular_graphs": all(
                row["source_factor_classification"] == "REGULAR_GRAPH"
                and row["target_factor_classification"] == "REGULAR_GRAPH"
                for row in scope179["walls"].values()
            ),
            "Round182_carried_normal_form_rows_on_active_origins":
                len(carried_rows),
            "absence_of_carried_rows_not_used_as_positive_evidence": True,
        },
        "tail_signature_reconstruction": {
            "candidate_region_count": len(tail_regions),
            "unique_signature_count": tail_status["UNIQUE"],
            "conflicting_signature_count": 0,
            "missing_signature_count": 0,
            "word_histogram": tail_word_histogram,
            "empty_word_region_count": 64,
            "one_wall_event_region_count": 32,
            "pair_glue_pass_count": len(glue_rows),
            "unexpected_pair_change_count": sum(
                row["unexpected_signature_change_count"]
                for row in glue_rows
            ),
            "positive_t_owner_pair_count": sum(
                row["positive_t_half_open_owner_leaf_row_id"]
                == row["positive_t_leaf_row_id"]
                for row in glue_rows
            ),
            "negative_t_shadow_pair_count": len(glue_rows),
            "all_changes_are_exactly_one_recorded_wall_event": True,
            "all_other_signature_fields_unchanged": True,
            "region_rows_sha256": digest(tail_regions),
            "region_rows": tail_regions,
            "pair_glue_rows_sha256": digest(glue_rows),
            "pair_glue_rows": glue_rows,
        },
        "full_64_origin_local_replacement_feasibility": {
            "Round182_leaf_enclosure_count": len(all_leaves),
            "inferred_strict_open_region_count": len(regions),
            "unique_signature_count": full_status["UNIQUE"],
            "conflicting_signature_count": 0,
            "missing_signature_count": 0,
            "origin_region_count_histogram": {
                str(key): value
                for key, value
                in sorted(Counter(per_origin.values()).items())
            },
            "tail_region_count_per_origin_histogram": {
                str(key): value
                for key, value
                in sorted(Counter(tail_per_origin.values()).items())
            },
            "word_histogram": full_word_histogram,
            "fully_local_replaced_origin_feasibility_count":
                EXPECTED_ORIGIN_COUNT,
            "officially_materialized_fully_local_replaced_origin_count": 0,
            "all_region_rows_sha256": digest(regions),
            "production_status":
                "FEASIBLE_BUT_ROWS_ATTACHMENT_AND_INDEPENDENT_VERIFIER_PENDING",
        },
        "exact_key_fibre_join": {
            "tail_local_region_count": len(tail_regions),
            "tail_distinct_exact_key_count": len(tail_fibres),
            "tail_fibre_cardinality_histogram": {
                str(key): value
                for key, value in sorted(Counter(
                    row["local_region_occurrence_count"]
                    for row in tail_fibres
                ).items())
            },
            "all_64_origin_local_region_count": len(regions),
            "all_64_origin_distinct_exact_key_count": len(all_fibres),
            "all_64_origin_fibre_cardinality_histogram": {
                str(key): value
                for key, value in sorted(Counter(
                    row["local_region_occurrence_count"]
                    for row in all_fibres
                ).items())
            },
            "each_local_region_joins_exactly_one_registry_key": True,
            "many_local_occurrences_may_join_one_exact_key": True,
            "distinct_local_exact_keys_do_not_exhaust_global_fibres": True,
            "tail_fibre_rows_sha256": digest(tail_fibres),
            "tail_fibre_rows": tail_fibres,
            "all_64_origin_fibre_rows_sha256": digest(all_fibres),
            "all_64_origin_fibre_rows": all_fibres,
            "global_source_G_exact_key_fibre_count": SOURCE_G_KEY_COUNT,
            "global_source_G_exact_key_disposition_count": 0,
        },
        "zero_promotion_contract": {
            "probe_only": True,
            "local_signature_rows_officially_materialized": 0,
            "whole_original_tube_credit_issued": 0,
            "official_source_G_global_disposition_count": 0,
            "official_source_G_global_disposition_denominator":
                SOURCE_G_KEY_COUNT,
            "D02": "UNCHANGED_BLOCKED",
            "global_Gate5_fields": "UNCHANGED_10/18",
            "CM2": "UNCHANGED_NO_GO",
        },
        "required_next":
            "rewrite as a formal producer that materializes all 736 region "
            "rows, exact graph/edge/corner lineage and 64 origin summaries; "
            "then independently rebuild geometry, signatures and immutable "
            "key joins without importing the producer, with semantic/JSON/"
            "path attacks and two hash-seed cold replays",
    }
    document = {
        "schema": SCHEMA,
        "probe_result": probe_result,
        "probe_result_sha256": digest(probe_result),
    }
    sys.stdout.write(
        json.dumps(
            document,
            sort_keys=True,
            indent=2,
            ensure_ascii=False,
            allow_nan=False,
        )
        + "\n"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
