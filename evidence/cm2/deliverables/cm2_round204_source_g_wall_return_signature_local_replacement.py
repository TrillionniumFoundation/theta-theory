#!/usr/bin/env python3
"""Formal local replacement of the 64 Round182 wall-G origins.

This producer starts from the fully pinned and independently verified
Round182 package.  It reconstructs the 64 relevant wall-G origins and all
512 of their Round182 leaves, discharges the sole return-signature
obstruction on every leaf, and materializes 736 strict open 3D local
signature regions.  It also materializes the complete source/target 2D
sheet, 1D boundary/intersection, and 0D endpoint/corner lineage with
deterministic half-open owners.

The Round192 and Round196 probes are design references only.  They are not
read, imported, pinned, or used as formal inputs.

All credit is local.  Whole original-tube credit and global exact-key
disposition credit remain zero.
"""

from __future__ import annotations

import argparse
import copy
from collections import Counter, defaultdict
from fractions import Fraction as Q
import gc
import hashlib
import importlib
import json
import os
from pathlib import Path
import stat
import sys
import tempfile
from typing import Any, Callable

from flint import arb, ctx, __version__ as FLINT_VERSION


HERE = Path(__file__).resolve().parent
OUTPUT = (
    HERE
    / "cm2_round204_source_g_wall_return_signature_local_replacement"
    "_certificate.json"
)
SCHEMA = (
    "cm2.round204.source-g-wall-return-signature-local-replacement.v1"
)
STATUS = (
    "CERTIFIED_LOCAL_SOURCE_G_WALL_RETURN_SIGNATURE_REPLACEMENT__"
    "NO_WHOLE_TUBE_OR_GLOBAL_EXACT_KEY_DISPOSITION"
)
MAX_INPUT_BYTES = 400 * 1024 * 1024

R182_PREFIX = "cm2_round182_source_g_clipped_graph_and_pair_arrangement"
R182_PRODUCER = f"{R182_PREFIX}.py"
R182_CERTIFICATE = f"{R182_PREFIX}_certificate.json"
R182_ATTACHMENT = f"{R182_PREFIX}_rows.json"
R182_VERIFIER = f"{R182_PREFIX}_verifier.py"
R182_VERIFICATION = f"{R182_PREFIX}_verification.json"
R182_REPORT = f"{R182_PREFIX}_report.md"
R182_COLD = f"{R182_PREFIX}_cold_replay.md"
R182_MANIFEST = f"{R182_PREFIX}_manifest.sha256"
R182_PINS = {
    R182_PRODUCER:
        "8638f2722e68bd5c6e0eb5932dc76780728998f21a47b1d8c02c28449e984d56",
    R182_CERTIFICATE:
        "27491e3943e88772ec15cee110cd983b14ad82a2a56f8a07d605c3cd8fb49f08",
    R182_ATTACHMENT:
        "ae6e0c38df325e98b01a1d75acfbd8a85a71fda6a118db11d7dff6decf3f847c",
    R182_VERIFIER:
        "790b17cf6dadebc37b889fff63c6ecde985cccf53c95523cd6c2bc39d12db566",
    R182_VERIFICATION:
        "b008c2208891374696b88506e87957bbb754d95d62677d9406c466405b311f36",
    R182_REPORT:
        "708272e9425bef74f3f4639c76fd17078f509d3acc5d324325c224e743985f0c",
    R182_COLD:
        "c0fd075a0ba56de5380c6cc89620dc82fa640c0466b118565cf1755aedf61f99",
}
R182_MANIFEST_SHA256 = (
    "32dea92dd0de87d3ded6ed69a908b58b01402ddcdef3f0e2b5ffde096a9383c5"
)
R182_CERTIFICATE_SCHEMA = (
    "cm2.round182.source-g-clipped-graph-and-pair-arrangement.v1"
)
R182_ATTACHMENT_SCHEMA = (
    "cm2.round182.source-g-clipped-graph-and-pair-arrangement-rows.v1"
)
R182_VERIFICATION_SCHEMA = (
    "cm2.round182.source-g-clipped-graph-and-pair-arrangement.verification.v1"
)
R182_CERTIFICATE_RESULT_SHA256 = (
    "e07da794eed6dbb404de8913f5b871621f9f1b59b355172a37192791ae28911d"
)
R182_ATTACHMENT_RESULT_SHA256 = (
    "9f0f64d93bd0ac2a9dd41965cbfd95531f07582da5eb4c52f14c44da3d0db269"
)
R182_VERIFICATION_RESULT_SHA256 = (
    "61715ef39e232937d821ba1c634181f905454b758abbe98d889c768ddc809797"
)
R182_STATUS = (
    "CERTIFIED_BOUNDED_PARTIAL_SOURCE_G_CLIPPED_GRAPH_AND_PAIR_ARRANGEMENT__"
    "NO_GLOBAL_EXACT_KEY_DISPOSITION_OR_D02_PROMOTION"
)

EXPECTED_ORIGIN_COUNT = 64
EXPECTED_PARENT_COUNT = 16
EXPECTED_LEAF_COUNT = 512
EXPECTED_EMPTY_LEAF_COUNT = 256
EXPECTED_FULL_GRAPH_LEAF_COUNT = 192
EXPECTED_TAIL_LEAF_COUNT = 64
EXPECTED_OPEN_REGION_COUNT = 736
EXPECTED_TAIL_REGION_COUNT = 96
EXPECTED_TAIL_PAIR_COUNT = 32
EXPECTED_SOURCE_SHEET_CELL_COUNT = 224
EXPECTED_TARGET_SHEET_CELL_COUNT = 224
EXPECTED_EXACT_INTERSECTION_SEGMENT_COUNT = 16
EXPECTED_SOURCE_G_KEY_COUNT = 224_580
EXPECTED_RELEVANT_INPUT_VOLUME = Q(177, 1_600_000)
EXPECTED_ROUND182_CLOSED_VOLUME = Q(22_479, 204_800_000)
EXPECTED_TAIL_VOLUME = Q(177, 204_800_000)
EXPECTED_SINGLE_TAIL_VOLUME = Q(177, 13_107_200_000)
EXPECTED_ORIGIN_VOLUME = Q(177, 102_400_000)
EXPECTED_ORIGIN_CLOSED_VOLUME = Q(22_479, 13_107_200_000)
EXPECTED_KEY_ORDINALS = [
    18715, 18716, 18717,
    70920, 70921, 70922,
    128050, 128059, 128060,
    186165, 186174, 186175,
]
SIGNS = {"NEGATIVE", "POSITIVE"}
STRICT_SIGNS = {"STRICT_NEGATIVE", "STRICT_POSITIVE"}
CHART_CONTRACT = {
    "G:E": ("G[1,0]", "Y", "source_y"),
    "G:W": ("G[-1,0]", "Y", "source_y"),
    "G:N": ("G[0,1]", "X", "source_x"),
    "G:S": ("G[0,-1]", "X", "source_x"),
}


class Round204Error(RuntimeError):
    pass


def require(condition: bool, label: str) -> None:
    if not condition:
        raise Round204Error(label)


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    ).encode()


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def digest(value: Any) -> str:
    return sha256_bytes(canonical_bytes(value))


def closed_row(payload: dict[str, Any]) -> dict[str, Any]:
    row = copy.deepcopy(payload)
    row["row_sha256"] = digest(row)
    return row


def qstr(value: Q) -> str:
    return (
        str(value.numerator)
        if value.denominator == 1
        else f"{value.numerator}/{value.denominator}"
    )


def regular_bytes(
    path: Path,
    maximum: int = MAX_INPUT_BYTES,
) -> bytes:
    before = path.lstat()
    require(stat.S_ISREG(before.st_mode), f"regular:{path.name}")
    require(not path.is_symlink(), f"symlink:{path.name}")
    require(before.st_nlink == 1, f"hardlink:{path.name}")
    require(0 < before.st_size <= maximum, f"size:{path.name}")
    flags = os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0)
    descriptor = os.open(path, flags)
    try:
        opened = os.fstat(descriptor)
        require(
            (
                opened.st_dev,
                opened.st_ino,
                opened.st_size,
                opened.st_mtime_ns,
            )
            == (
                before.st_dev,
                before.st_ino,
                before.st_size,
                before.st_mtime_ns,
            ),
            f"stable-open:{path.name}",
        )
        chunks: list[bytes] = []
        total = 0
        while True:
            chunk = os.read(descriptor, 1024 * 1024)
            if not chunk:
                break
            total += len(chunk)
            require(total <= maximum, f"bounded-read:{path.name}")
            chunks.append(chunk)
        after = os.fstat(descriptor)
        require(
            (
                after.st_dev,
                after.st_ino,
                after.st_size,
                after.st_mtime_ns,
            )
            == (
                opened.st_dev,
                opened.st_ino,
                opened.st_size,
                opened.st_mtime_ns,
            ),
            f"stable-read:{path.name}",
        )
        return b"".join(chunks)
    finally:
        os.close(descriptor)


def pinned_bytes(
    path: Path,
    expected: str,
    maximum: int = MAX_INPUT_BYTES,
) -> bytes:
    raw = regular_bytes(path, maximum)
    require(sha256_bytes(raw) == expected, f"pin:{path.name}")
    return raw


def unique_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        require(key not in result, f"duplicate JSON key:{key}")
        result[key] = value
    return result


def reject_number(token: str) -> None:
    raise Round204Error(f"noninteger JSON number:{token}")


def validate_tree(value: Any, path: str = "$") -> None:
    require(
        type(value) in {dict, list, str, int, bool, type(None)},
        f"JSON type:{path}",
    )
    if type(value) is dict:
        for key, child in value.items():
            require(
                type(key) is str
                and "\x00" not in key
                and not any(0xD800 <= ord(char) <= 0xDFFF for char in key),
                f"JSON key:{path}",
            )
            validate_tree(child, f"{path}.{key}")
    elif type(value) is list:
        for index, child in enumerate(value):
            validate_tree(child, f"{path}[{index}]")
    elif type(value) is str:
        require(
            "\x00" not in value
            and not any(0xD800 <= ord(char) <= 0xDFFF for char in value),
            f"JSON string:{path}",
        )


def strict_json(raw: bytes, label: str) -> dict[str, Any]:
    require(
        raw
        and not raw.startswith(b"\xef\xbb\xbf")
        and b"\x00" not in raw,
        f"JSON encoding:{label}",
    )
    try:
        value = json.loads(
            raw.decode("utf-8", "strict"),
            object_pairs_hook=unique_pairs,
            parse_float=reject_number,
            parse_constant=reject_number,
        )
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise Round204Error(f"JSON parse:{label}:{exc}") from exc
    validate_tree(value)
    require(type(value) is dict, f"JSON top object:{label}")
    require(raw == canonical_bytes(value) + b"\n",
            f"canonical JSON:{label}")
    return value


def manifest_entries(raw: bytes) -> dict[str, str]:
    try:
        text = raw.decode("ascii", "strict")
    except UnicodeDecodeError as exc:
        raise Round204Error("manifest ASCII") from exc
    require(text.endswith("\n"), "manifest newline")
    result: dict[str, str] = {}
    for line in text.splitlines():
        parts = line.split("  ", 1)
        require(len(parts) == 2, "manifest line")
        value, name = parts
        require(
            len(value) == 64
            and all(character in "0123456789abcdef" for character in value),
            f"manifest digest:{name}",
        )
        require(
            name not in result
            and name not in {"", ".", ".."}
            and "/" not in name
            and "\\" not in name,
            f"manifest name:{name}",
        )
        result[name] = value
    return result


def pin_round182() -> None:
    observed = {
        name: sha256_bytes(regular_bytes(HERE / name))
        for name in R182_PINS
    }
    require(observed == R182_PINS, "Round182 package pins")
    manifest_raw = pinned_bytes(
        HERE / R182_MANIFEST,
        R182_MANIFEST_SHA256,
        10_000,
    )
    require(
        manifest_entries(manifest_raw) == R182_PINS,
        "Round182 exact manifest entries",
    )


def unwrap(
    document: dict[str, Any],
    *,
    schema: str,
    result_sha256: str,
    label: str,
) -> dict[str, Any]:
    require(
        set(document) == {"schema", "result", "result_sha256"}
        and document["schema"] == schema
        and document["result_sha256"] == result_sha256
        and digest(document["result"]) == result_sha256,
        f"wrapper:{label}",
    )
    return document["result"]


def load_formal_inputs() -> dict[str, Any]:
    require(FLINT_VERSION == "0.9.0", "python-flint version")
    pin_round182()
    certificate = unwrap(
        strict_json(
            pinned_bytes(
                HERE / R182_CERTIFICATE,
                R182_PINS[R182_CERTIFICATE],
                10_000_000,
            ),
            R182_CERTIFICATE,
        ),
        schema=R182_CERTIFICATE_SCHEMA,
        result_sha256=R182_CERTIFICATE_RESULT_SHA256,
        label="Round182 certificate",
    )
    attachment_document = strict_json(
        pinned_bytes(
            HERE / R182_ATTACHMENT,
            R182_PINS[R182_ATTACHMENT],
            MAX_INPUT_BYTES,
        ),
        R182_ATTACHMENT,
    )
    attachment = unwrap(
        attachment_document,
        schema=R182_ATTACHMENT_SCHEMA,
        result_sha256=R182_ATTACHMENT_RESULT_SHA256,
        label="Round182 attachment",
    )
    verification = unwrap(
        strict_json(
            pinned_bytes(
                HERE / R182_VERIFICATION,
                R182_PINS[R182_VERIFICATION],
                10_000_000,
            ),
            R182_VERIFICATION,
        ),
        schema=R182_VERIFICATION_SCHEMA,
        result_sha256=R182_VERIFICATION_RESULT_SHA256,
        label="Round182 verification",
    )
    require(
        certificate["status"] == R182_STATUS
        and verification["status"] == "PASS"
        and verification["certificate_result_sha256"]
        == R182_CERTIFICATE_RESULT_SHA256
        and verification["attachment_result_sha256"]
        == R182_ATTACHMENT_RESULT_SHA256
        and verification["complete_expected_certificate_rebuilt"] is True
        and verification["full_attachment_byte_for_byte_matched"] is True
        and verification["producer_imported_or_executed"] is False
        and verification["global_state_reconfirmed"]["D02"] == "BLOCKED"
        and verification["global_state_reconfirmed"]["Gate5"] == "10/18"
        and verification["global_state_reconfirmed"]["CM2"] == "NO-GO",
        "Round182 independent acceptance",
    )

    evaluator = importlib.import_module(
        "cm2_round182_source_g_clipped_graph_and_pair_arrangement_verifier"
    )
    require(
        Path(evaluator.__file__).resolve() == (HERE / R182_VERIFIER).resolve()
        and sha256_bytes(regular_bytes(Path(evaluator.__file__)))
        == R182_PINS[R182_VERIFIER],
        "Round182 evaluator identity",
    )
    pin_round182()
    source179, _cert182, rebuilt_attachment, _cert_raw, _attachment_raw = (
        evaluator.load_source_and_documents()
    )
    require(
        rebuilt_attachment["result_sha256"]
        == R182_ATTACHMENT_RESULT_SHA256
        and rebuilt_attachment["result"] == attachment,
        "Round182 evaluator attachment binding",
    )

    r174 = evaluator.r179.r174
    frozen174 = r174.load_frozen_inputs()
    registry = r174.rebuild_registry(frozen174["gate5"])
    registry_meta = frozen174["gate5"]["result"][
        "immutable_candidate_key_registry"
    ]
    require(
        registry_meta["candidate_return_word_key_count"] == 441_280
        and len(registry["pairs"]) == 448
        and len(registry["patterns"]) == 985,
        "immutable Gate5 registry",
    )
    attachment174_document = strict_json(
        pinned_bytes(
            Path(r174.ATTACHMENT),
            r174.EXPECTED_ATTACHMENT_SHA256,
            MAX_INPUT_BYTES,
        ),
        Path(r174.ATTACHMENT).name,
    )
    attachment174 = unwrap(
        attachment174_document,
        schema=r174.ATTACHMENT_SCHEMA,
        result_sha256=r174.EXPECTED_ATTACHMENT_RESULT,
        label="transitive Round174 attachment",
    )
    del frozen174, rebuilt_attachment, attachment_document
    gc.collect()
    pin_round182()
    return {
        "certificate182": certificate,
        "verification182": verification,
        "attachment182": attachment,
        "attachment174": attachment174,
        "source179": source179,
        "registry": registry,
        "evaluator": evaluator,
    }


def unpack(
    columns: list[str],
    packed: list[Any],
) -> dict[str, Any]:
    require(len(columns) == len(packed), "packed row width")
    return dict(zip(columns, packed, strict=True))


def extract_round182_scope(
    attachment: dict[str, Any],
) -> dict[str, Any]:
    schemas = attachment["row_column_schemas"]
    collar_columns = schemas["collar_occurrence_rows"]
    leaf_columns = schemas["collar_leaf_rows"]
    origin_columns = schemas["origin_replacement_rows"]
    carry_columns = schemas["carried_normal_form_rows"]

    collars: dict[str, dict[str, Any]] = {}
    collar_packed_sha256: dict[str, str] = {}
    for packed in attachment["collar_occurrence_rows"]:
        row = unpack(collar_columns, packed)
        occurrence = row["Round179_occurrence_row_id"]
        require(occurrence not in collars, f"collar duplicate:{occurrence}")
        collars[occurrence] = row
        collar_packed_sha256[occurrence] = digest(packed)

    all_leaf_rows: list[tuple[list[Any], dict[str, Any]]] = [
        (packed, unpack(leaf_columns, packed))
        for packed in attachment["collar_leaf_rows"]
    ]
    tail_leaves = [
        row for _packed, row in all_leaf_rows
        if Q(row["residual_3d_collar_volume"]) > 0
        and collars[row["occurrence_row_id"]]["kind"] == "WALL"
    ]
    require(len(tail_leaves) == EXPECTED_TAIL_LEAF_COUNT,
            "wall-G tail leaf census")
    occurrence_ids = {
        row["occurrence_row_id"] for row in tail_leaves
    }
    relevant_collars = {
        occurrence: collars[occurrence]
        for occurrence in occurrence_ids
    }
    origin_ids = {
        row["origin_row_id"] for row in relevant_collars.values()
    }
    require(
        len(occurrence_ids) == EXPECTED_TAIL_LEAF_COUNT
        and len(origin_ids) == EXPECTED_ORIGIN_COUNT
        and all(
            collar["kind"] == "WALL"
            and collar["target_obstacle"] == "G"
            and collar["reason_label"].startswith(
                "wall_endpoint_or_count_transition:"
            )
            for collar in relevant_collars.values()
        ),
        "wall-G occurrence/origin scope",
    )

    leaves = [
        row for _packed, row in all_leaf_rows
        if row["occurrence_row_id"] in occurrence_ids
    ]
    leaf_packed_sha256 = {
        row["row_id"]: digest(packed)
        for packed, row in all_leaf_rows
        if row["occurrence_row_id"] in occurrence_ids
    }
    leaves.sort(key=lambda row: row["row_id"])
    require(
        len(leaves) == EXPECTED_LEAF_COUNT
        and len(leaf_packed_sha256) == EXPECTED_LEAF_COUNT,
        "all relevant Round182 leaves",
    )
    leaves_by_occurrence: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in leaves:
        leaves_by_occurrence[row["occurrence_row_id"]].append(row)
    for occurrence, rows in leaves_by_occurrence.items():
        rows.sort(key=lambda row: row["row_id"])
        packed_rows = [
            [row[column] for column in leaf_columns]
            for row in rows
        ]
        collar = relevant_collars[occurrence]
        require(
            len(rows) == 8
            and sum(
                Q(row["closed_3d_side_union_volume"]) > 0
                for row in rows
            ) == 7
            and sum(
                Q(row["residual_3d_collar_volume"]) > 0
                for row in rows
            ) == 1
            and digest(packed_rows) == collar["leaf_rows_sha256"],
            f"Round182 collar leaf binding:{occurrence}",
        )

    origins: dict[str, dict[str, Any]] = {}
    origin_packed_sha256: dict[str, str] = {}
    for packed in attachment["origin_replacement_rows"]:
        if packed[1] not in origin_ids:
            continue
        row = unpack(origin_columns, packed)
        origin_id = row["Round179_origin_row_id"]
        require(origin_id not in origins, f"origin duplicate:{origin_id}")
        origins[origin_id] = row
        origin_packed_sha256[origin_id] = digest(packed)
    require(set(origins) == origin_ids, "Round182 origin support")

    carried = [
        unpack(carry_columns, packed)
        for packed in attachment["carried_normal_form_rows"]
        if packed[2] in origin_ids
    ]
    require(not carried, "no carried rows on active origins")

    classification = Counter(
        row["graph_classification"] for row in leaves
    )
    require(
        classification == Counter({
            "EMPTY": EXPECTED_EMPTY_LEAF_COUNT,
            "FULL_2D": EXPECTED_FULL_GRAPH_LEAF_COUNT,
            "RESIDUAL_3D": EXPECTED_TAIL_LEAF_COUNT,
        }),
        "relevant leaf classification census",
    )
    tail_patterns = Counter(
        row["lower_t_face_status"] + "|" + row["upper_t_face_status"]
        for row in tail_leaves
    )
    require(
        tail_patterns == Counter({"S-|U": 32, "U|S+": 32}),
        "tail face pattern census",
    )
    input_volume = sum(
        (Q(row["coordinate_volume"]) for row in leaves),
        Q(0),
    )
    closed_volume = sum(
        (Q(row["closed_3d_side_union_volume"]) for row in leaves),
        Q(0),
    )
    tail_volume = sum(
        (Q(row["residual_3d_collar_volume"]) for row in leaves),
        Q(0),
    )
    require(
        input_volume == EXPECTED_RELEVANT_INPUT_VOLUME
        and closed_volume == EXPECTED_ROUND182_CLOSED_VOLUME
        and tail_volume == EXPECTED_TAIL_VOLUME
        and closed_volume + tail_volume == input_volume
        and all(
            Q(row["residual_3d_collar_volume"])
            == EXPECTED_SINGLE_TAIL_VOLUME
            for row in tail_leaves
        ),
        "Round182 relevant exact volume",
    )
    for origin_id, origin in origins.items():
        require(
            origin["collar_occurrence_count"] == 1
            and origin["Round179_retained_child_count"] == 2
            and Q(origin["Round179_retained_coordinate_volume"])
            == EXPECTED_ORIGIN_VOLUME
            and Q(origin["closed_Round182_retained_coordinate_volume"])
            == EXPECTED_ORIGIN_CLOSED_VOLUME
            and Q(origin["residual_Round182_retained_coordinate_volume"])
            == EXPECTED_SINGLE_TAIL_VOLUME
            and origin["fully_geometrically_replaced_original_tube"] is False
            and origin["Round182_released_global_exact_key_count"] == 0
            and origin["global_exact_key_disposition_credit"] == 0,
            f"Round182 origin binding:{origin_id}",
        )
    parent_ids = {
        collar["parent_id"] for collar in relevant_collars.values()
    }
    require(len(parent_ids) == EXPECTED_PARENT_COUNT,
            "relevant parent census")
    return {
        "leaves": leaves,
        "tail_leaves": sorted(
            tail_leaves,
            key=lambda row: row["row_id"],
        ),
        "leaves_by_occurrence": leaves_by_occurrence,
        "collars": relevant_collars,
        "origins": origins,
        "occurrence_ids": occurrence_ids,
        "origin_ids": origin_ids,
        "parent_ids": parent_ids,
        "leaf_packed_sha256": leaf_packed_sha256,
        "collar_packed_sha256": collar_packed_sha256,
        "origin_packed_sha256": origin_packed_sha256,
        "classification": dict(sorted(classification.items())),
        "tail_patterns": dict(sorted(tail_patterns.items())),
        "input_volume": input_volume,
        "closed_volume": closed_volume,
        "tail_volume": tail_volume,
    }


def extract_round179_scope(
    source179: dict[str, Any],
    occurrence_ids: set[str],
    origin_ids: set[str],
) -> dict[str, Any]:
    schemas = source179["row_column_schemas"]
    walls: dict[str, dict[str, Any]] = {}
    wall_packed_sha256: dict[str, str] = {}
    for packed in source179["wall_normal_form_rows"]:
        if packed[0] not in occurrence_ids:
            continue
        row = unpack(schemas["wall_normal_form_rows"], packed)
        walls[row["row_id"]] = row
        wall_packed_sha256[row["row_id"]] = digest(packed)
    origins: dict[str, dict[str, Any]] = {}
    for packed in source179["origin_tube_rows"]:
        if packed[0] not in origin_ids:
            continue
        row = unpack(schemas["origin_tube_rows"], packed)
        origins[row["origin_row_id"]] = row
    retained: dict[str, dict[str, Any]] = {}
    for packed in source179["retained_3d_child_rows"]:
        if packed[1] not in origin_ids:
            continue
        row = unpack(schemas["retained_3d_child_rows"], packed)
        retained[row["row_id"]] = row
    require(
        set(walls) == occurrence_ids
        and set(origins) == origin_ids
        and len(retained) == 2 * EXPECTED_ORIGIN_COUNT
        and Counter(row["origin_row_id"] for row in retained.values())
        == Counter({origin_id: 2 for origin_id in origin_ids}),
        "Round179 exact support",
    )
    return {
        "walls": walls,
        "origins": origins,
        "retained": retained,
        "wall_packed_sha256": wall_packed_sha256,
    }


def extract_round174_scope(
    attachment174: dict[str, Any],
    origin_ids: set[str],
    parent_ids: set[str],
) -> dict[str, Any]:
    schemas = attachment174["row_column_schemas"]
    parents: dict[str, dict[str, Any]] = {}
    for packed in attachment174["parent_rows"]:
        if packed[0] in parent_ids:
            row = unpack(schemas["parent_rows"], packed)
            parents[row["parent_id"]] = row
    residual: dict[str, dict[str, Any]] = {}
    for packed in attachment174["residual_3d_tube_rows"]:
        if packed[0] in origin_ids:
            row = unpack(schemas["residual_3d_tube_rows"], packed)
            residual[row["row_id"]] = row
    resolved: list[dict[str, Any]] = []
    for packed in attachment174["resolved_3d_occurrence_rows"]:
        if packed[2] in parent_ids:
            resolved.append(unpack(
                schemas["resolved_3d_occurrence_rows"],
                packed,
            ))
    require(
        len(parents) == EXPECTED_PARENT_COUNT
        and set(parents) == parent_ids
        and len(residual) == EXPECTED_ORIGIN_COUNT
        and set(residual) == origin_ids
        and len(resolved) == 192,
        "Round174 transitive anchor scope",
    )
    return {
        "parents": parents,
        "residual": residual,
        "resolved": resolved,
    }


def qbox(values: list[str]) -> list[Q]:
    return [Q(value) for value in values]


def face_adjacency_axis(
    first_values: list[str],
    second_values: list[str],
) -> int | None:
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


def compact_resolved_signature(row: dict[str, Any]) -> dict[str, Any]:
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


def build_anchor_evidence(
    scope174: dict[str, Any],
    scope179: dict[str, Any],
    registry: dict[str, Any],
    r174: Any,
) -> tuple[
    dict[str, dict[str, Any]],
    list[dict[str, Any]],
    list[dict[str, Any]],
]:
    resolved_by_parent: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in scope174["resolved"]:
        resolved_by_parent[row["parent_id"]].append(row)

    parent_signatures: dict[str, dict[str, Any]] = {}
    parent_rows: list[dict[str, Any]] = []
    for parent_id, parent in sorted(scope174["parents"].items()):
        resolved = resolved_by_parent[parent_id]
        signatures = {
            canonical_bytes(compact_resolved_signature(row))
            for row in resolved
        }
        require(
            len(signatures) == 1
            and parent["observed_exact_key_count"] == 1,
            f"unique parent signature:{parent_id}",
        )
        signature = compact_resolved_signature(resolved[0])
        exact_key = r174.exact_key(
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
            and signature["official_key_row"] == exact_key["row"]
            and signature["official_key_ordinal"] == exact_key["ordinal"]
            and signature["official_key_id"] == exact_key["identifier"]
            and parent["observed_exact_key_ordinals_sha256"]
            == digest([exact_key["ordinal"]]),
            f"parent empty anchor:{parent_id}",
        )
        parent_signatures[parent_id] = signature
        parent_rows.append(closed_row({
            "parent_id": parent_id,
            "chart": parent["chart"],
            "owner_target": parent["owner_target"],
            "resolved_anchor_row_count": len(resolved),
            "unique_resolved_signature_count": 1,
            "empty_word_official_key_id": exact_key["identifier"],
            "empty_word_official_key_ordinal": exact_key["ordinal"],
            "empty_word_official_key_row": exact_key["row"],
            "formal_anchor_binding": True,
            "whole_original_tube_credit": 0,
            "global_exact_key_disposition_credit": 0,
        }))

    origin_anchors: dict[str, dict[str, Any]] = {}
    origin_rows: list[dict[str, Any]] = []
    adjacency_counts: Counter[int] = Counter()
    adjacency_axes: Counter[str] = Counter()
    for origin_id, origin in sorted(scope179["origins"].items()):
        prior = scope174["residual"][origin_id]
        require(
            prior["parent_id"] == origin["parent_id"]
            and prior["chart"] == origin["chart"]
            and prior["box"] == origin["original_box"]
            and prior["reason_labels"] == origin["original_reason_labels"],
            f"Round174/179 origin binding:{origin_id}",
        )
        adjacent: list[tuple[int, dict[str, Any]]] = []
        for resolved in resolved_by_parent[origin["parent_id"]]:
            axis = face_adjacency_axis(
                origin["original_box"],
                resolved["box"],
            )
            if axis is not None:
                adjacent.append((axis, resolved))
        require(len(adjacent) in {1, 2},
                f"adjacent anchor count:{origin_id}")
        signatures = {
            canonical_bytes(compact_resolved_signature(row))
            for _axis, row in adjacent
        }
        require(
            len(signatures) == 1
            and compact_resolved_signature(adjacent[0][1])
            == parent_signatures[origin["parent_id"]],
            f"origin anchor agreement:{origin_id}",
        )
        adjacency_counts[len(adjacent)] += 1
        for axis, _row in adjacent:
            adjacency_axes["tps"[axis]] += 1
        origin_anchors[origin_id] = parent_signatures[
            origin["parent_id"]
        ]
        origin_rows.append(closed_row({
            "origin_row_id": origin_id,
            "parent_id": origin["parent_id"],
            "adjacent_resolved_row_count": len(adjacent),
            "adjacent_axes": sorted(
                "tps"[axis] for axis, _row in adjacent
            ),
            "adjacent_resolved_row_ids": sorted(
                row["row_id"] for _axis, row in adjacent
            ),
            "unique_empty_word_anchor": True,
            "anchor_official_key_id":
                parent_signatures[origin["parent_id"]][
                    "official_key_id"
                ],
            "whole_original_tube_credit": 0,
            "global_exact_key_disposition_credit": 0,
        }))
    require(
        adjacency_counts == Counter({1: 32, 2: 32})
        and adjacency_axes == Counter({"t": 64, "p": 32}),
        "adjacent anchor census",
    )
    return origin_anchors, parent_rows, origin_rows


def atlas_box(row: dict[str, Any], r174: Any) -> Any:
    return r174.atlas.AtlasBox(
        *(Q(value) for value in row["box"]),
        len(row["base_refinement_path"]),
        row["row_id"],
    )


def fixed_box(
    box: Any,
    r174: Any,
    *,
    t: Q | None = None,
    p: Q | None = None,
) -> Any:
    return r174.atlas.AtlasBox(
        box.t0 if t is None else t,
        box.t1 if t is None else t,
        box.p0 if p is None else p,
        box.p1 if p is None else p,
        box.s0,
        box.s1,
        box.depth,
        box.path,
    )


def qarb(value: Q) -> arb:
    return arb(value.numerator) / value.denominator


def arb_sign(value: arb, r179: Any) -> str:
    return r179.arb_sign(value)


def analyze_tail_leaf(
    leaf: dict[str, Any],
    *,
    collar: dict[str, Any],
    wall: dict[str, Any],
    origin179: dict[str, Any],
    origin182: dict[str, Any],
    retained: dict[str, Any],
    evaluator: Any,
    leaf_packed_sha256: str,
    collar_packed_sha256: str,
    wall_packed_sha256: str,
) -> dict[str, Any]:
    r179 = evaluator.r179
    r174 = r179.r174
    box = atlas_box(leaf, r174)
    contract = CHART_CONTRACT.get(collar["chart"])
    require(contract is not None, f"tail chart:{leaf['row_id']}")
    expected_owner, expected_axis, source_name = contract
    require(
        collar["owner_target"] == expected_owner
        and collar["target_obstacle"] == "G"
        and collar["kind"] == "WALL"
        and wall["origin_row_id"] == collar["origin_row_id"]
        and wall["axis"] == expected_axis
        and wall["integer_wall"] == 0
        and wall["source_factor_classification"] == "REGULAR_GRAPH"
        and wall["source_gradient_axis"] == "t"
        and wall["source_gradient_sign"] == "STRICT_POSITIVE"
        and wall["target_factor_classification"] == "REGULAR_GRAPH"
        and wall["target_gradient_axis"] == "t"
        and wall["target_gradient_sign"] == "STRICT_POSITIVE",
        f"tail wall symbolic contract:{leaf['row_id']}",
    )
    require(
        origin179["origin_row_id"] == collar["origin_row_id"]
        and origin179["chart"] == collar["chart"]
        and origin179["owner_target"] == collar["owner_target"]
        and origin179["original_reason_labels"]
        == [collar["reason_label"]]
        and origin182["Round179_origin_row_id"]
        == collar["origin_row_id"]
        and retained["origin_row_id"] == collar["origin_row_id"]
        and retained["row_id"] == leaf["retained_child_row_id"],
        f"tail origin lineage:{leaf['row_id']}",
    )

    lower_unresolved = leaf["lower_t_face_status"] == "U"
    upper_unresolved = leaf["upper_t_face_status"] == "U"
    require(lower_unresolved != upper_unresolved,
            f"tail one unresolved face:{leaf['row_id']}")
    if lower_unresolved:
        require(
            box.t0 == 0
            and box.t1 > 0
            and leaf["upper_t_face_status"] == "S+",
            f"positive tail:{leaf['row_id']}",
        )
        t_side = "POSITIVE_T"
        outer_t = box.t1
        expected_outer_sign = "STRICT_POSITIVE"
    else:
        require(
            box.t1 == 0
            and box.t0 < 0
            and leaf["lower_t_face_status"] == "S-",
            f"negative tail:{leaf['row_id']}",
        )
        t_side = "NEGATIVE_T"
        outer_t = box.t0
        expected_outer_sign = "STRICT_NEGATIVE"
    require(
        (box.p0 == 0) != (box.p1 == 0),
        f"tail exact p0 boundary:{leaf['row_id']}",
    )
    outer_p = box.p1 if box.p0 == 0 else box.p0

    geometry = r179.independent_geometry(
        collar["chart"],
        collar["owner_target"],
        box,
    )
    source = r179.subtract_wall(geometry[source_name], 0)
    exact_dt = qarb(Q(9, 25))
    expected_source_value = (
        r174.first_hit.arb_interval(box.t0, box.t1) * exact_dt
    )
    require(
        source[0].contains(expected_source_value)
        and expected_source_value.contains(source[0])
        and source[1][0].contains(exact_dt)
        and arb_sign(source[1][0], r179) == "STRICT_POSITIVE"
        and source[1][1].is_zero()
        and source[1][2].is_zero(),
        f"tail source exact identity:{leaf['row_id']}",
    )
    t0_face = fixed_box(box, r174, t=Q(0))
    source_t0 = r179.subtract_wall(
        r179.independent_geometry(
            collar["chart"],
            collar["owner_target"],
            t0_face,
        )[source_name],
        0,
    )
    source_outer = r179.subtract_wall(
        r179.independent_geometry(
            collar["chart"],
            collar["owner_target"],
            fixed_box(box, r174, t=outer_t),
        )[source_name],
        0,
    )
    require(
        source_t0[0].is_zero()
        and arb_sign(source_outer[0], r179) == expected_outer_sign,
        f"tail exact source sheet:{leaf['row_id']}",
    )

    target_name = "hit_x" if wall["axis"] == "X" else "hit_y"

    def target_function(child: Any) -> tuple[Any, tuple[Any, ...]]:
        target_geometry = r179.independent_geometry(
            collar["chart"],
            collar["owner_target"],
            child,
        )
        return r179.subtract_wall(
            target_geometry[target_name],
            wall["integer_wall"],
        )

    target = target_function(box)
    target_t0 = target_function(t0_face)
    target_corner = target_function(
        fixed_box(box, r174, t=Q(0), p=Q(0))
    )
    target_t0_p_outer = target_function(
        fixed_box(box, r174, t=Q(0), p=outer_p)
    )
    target_outer_t = target_function(
        fixed_box(box, r174, t=outer_t)
    )
    dt_sign = arb_sign(target[1][0], r179)
    dp_sign = arb_sign(target[1][1], r179)
    p_outer_sign = arb_sign(target_t0_p_outer[0], r179)
    outer_t_sign = arb_sign(target_outer_t[0], r179)
    require(
        arb_sign(target[0], r179) == "OVERWRAP"
        and arb_sign(target_t0[0], r179) == "OVERWRAP"
        and dt_sign == "STRICT_POSITIVE"
        and dp_sign in STRICT_SIGNS
        and target[1][2].is_zero()
        and target_corner[0].is_zero()
        and p_outer_sign in STRICT_SIGNS
        and outer_t_sign == expected_outer_sign,
        f"tail target boundary evidence:{leaf['row_id']}",
    )
    if p_outer_sign == outer_t_sign:
        target_class = (
            "EXACT_T0_P0_S_EDGE_ONLY__NO_OFF_SOURCE_TARGET_ZERO"
        )
        target_sheet_count = 0
        target_region_count = 1
        newton_interior = None
        newton_image = None
        product_zero_set = "EXACT_SOURCE_T0_SHEET"
    else:
        newton_interior, newton_image = evaluator.v_newton(
            target_function,
            fixed_box(box, r174, p=outer_p),
            "t",
        )
        require(newton_interior is True,
                f"tail interval Newton:{leaf['row_id']}")
        target_class = (
            "UNIQUE_CLIPPED_TARGET_2D_GRAPH__"
            "T_BRACKET_MONOTONICITY_AND_P_OUTER_INTERVAL_NEWTON"
        )
        target_sheet_count = 1
        target_region_count = 2
        product_zero_set = (
            "SOURCE_T0_SHEET_UNION_UNIQUE_TARGET_2D_GRAPH__"
            "INTERSECTION_T0_P0_S_LINE"
        )

    pair_key = [
        collar["chart"],
        collar["owner_target"],
        wall["axis"],
        wall["integer_wall"],
        qstr(box.p0),
        qstr(box.p1),
        qstr(box.s0),
        qstr(box.s1),
    ]
    common_face = [
        "0", "0",
        qstr(box.p0), qstr(box.p1),
        qstr(box.s0), qstr(box.s1),
    ]
    intersection = [
        "0", "0", "0", "0",
        qstr(box.s0), qstr(box.s1),
    ]
    payload = [
        leaf["row_id"],
        collar["origin_row_id"],
        pair_key,
        target_class,
    ]
    return closed_row({
        "tail_geometry_row_id":
            f"round204-wall-tail-geometry:{digest(payload)}",
        "leaf_row_id": leaf["row_id"],
        "Round182_leaf_packed_sha256": leaf_packed_sha256,
        "Round182_collar_packed_sha256": collar_packed_sha256,
        "Round179_wall_packed_sha256": wall_packed_sha256,
        "origin_row_id": collar["origin_row_id"],
        "parent_id": collar["parent_id"],
        "retained_child_row_id": leaf["retained_child_row_id"],
        "chart": collar["chart"],
        "owner_target": collar["owner_target"],
        "wall_axis": wall["axis"],
        "integer_wall": wall["integer_wall"],
        "t_side": t_side,
        "half_open_source_sheet_owner": t_side == "POSITIVE_T",
        "pair_key": pair_key,
        "pair_key_sha256": digest(pair_key),
        "leaf_box": leaf["box"],
        "coordinate_volume": leaf["residual_3d_collar_volume"],
        "common_t0_face_exact_bounds": common_face,
        "common_t0_face_sha256": digest(common_face),
        "source_wall_factor_name": source_name,
        "source_wall_factor_exact": "(9/25)*t",
        "source_wall_factor_exact_zero_set": "t=0",
        "source_wall_strict_outer_t_sign":
            arb_sign(source_outer[0], r179),
        "target_wall_factor_name": target_name,
        "target_wall_full_leaf_sign": arb_sign(target[0], r179),
        "target_wall_t0_face_sign": arb_sign(target_t0[0], r179),
        "target_wall_exact_t0_p0_s_edge_zero": True,
        "target_t_derivative_sign": dt_sign,
        "target_t_derivative_interval": target[1][0].str(40),
        "target_p_derivative_sign": dp_sign,
        "target_p_derivative_interval": target[1][1].str(40),
        "target_s_derivative_exact_zero": True,
        "target_t0_p_outer_sign": p_outer_sign,
        "target_t0_p_outer_interval": target_t0_p_outer[0].str(40),
        "target_outer_t_face_sign": outer_t_sign,
        "target_outer_t_face_interval": target_outer_t[0].str(40),
        "target_zero_classification": target_class,
        "target_2D_sheet_count": target_sheet_count,
        "target_open_3D_region_count": target_region_count,
        "target_p_outer_interval_newton_interior": newton_interior,
        "target_p_outer_interval_newton_image": newton_image,
        "source_target_1D_intersection_exact_bounds": intersection,
        "source_target_1D_intersection_endpoint_incidence_count": 2,
        "wall_product_zero_set": product_zero_set,
        "wall_product_equivalent_to_source_t0_sheet_only":
            target_sheet_count == 0,
        "local_lineage_materialized": True,
        "whole_original_tube_credit": 0,
        "global_exact_key_disposition_credit": 0,
    })


def build_tail_pairs(
    tail_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    groups: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in tail_rows:
        groups[row["pair_key_sha256"]].append(row)
    require(len(groups) == EXPECTED_TAIL_PAIR_COUNT,
            "tail pair census")
    output: list[dict[str, Any]] = []
    for key_sha256, rows in sorted(groups.items()):
        by_side = {row["t_side"]: row for row in rows}
        require(
            len(rows) == 2
            and set(by_side) == {"NEGATIVE_T", "POSITIVE_T"},
            f"tail signed pair:{key_sha256}",
        )
        negative = by_side["NEGATIVE_T"]
        positive = by_side["POSITIVE_T"]
        require(
            negative["pair_key"] == positive["pair_key"]
            and negative["common_t0_face_exact_bounds"]
            == positive["common_t0_face_exact_bounds"]
            and negative["common_t0_face_sha256"]
            == positive["common_t0_face_sha256"],
            f"tail common face:{key_sha256}",
        )
        graph_rows = [
            row for row in rows if row["target_2D_sheet_count"] == 1
        ]
        boundary_rows = [
            row for row in rows if row["target_2D_sheet_count"] == 0
        ]
        require(
            len(graph_rows) == 1
            and len(boundary_rows) == 1
            and positive["half_open_source_sheet_owner"] is True
            and negative["half_open_source_sheet_owner"] is False,
            f"tail pair graph/owner:{key_sha256}",
        )
        payload = [
            negative["pair_key"],
            negative["leaf_row_id"],
            positive["leaf_row_id"],
        ]
        output.append(closed_row({
            "tail_pair_row_id":
                f"round204-wall-tail-pair:{digest(payload)}",
            "pair_key": negative["pair_key"],
            "pair_key_sha256": key_sha256,
            "negative_t_leaf_row_id": negative["leaf_row_id"],
            "negative_t_origin_row_id": negative["origin_row_id"],
            "positive_t_leaf_row_id": positive["leaf_row_id"],
            "positive_t_origin_row_id": positive["origin_row_id"],
            "common_t0_face_exact_bounds":
                negative["common_t0_face_exact_bounds"],
            "common_t0_face_byte_for_byte_equal": True,
            "common_t0_face_sha256":
                negative["common_t0_face_sha256"],
            "half_open_owner_policy":
                "OUTCOME_BLIND_POSITIVE_T_SIDE_OWNS__"
                "NEGATIVE_T_SIDE_IS_SHADOW",
            "half_open_owner_leaf_row_id": positive["leaf_row_id"],
            "half_open_shadow_leaf_row_id": negative["leaf_row_id"],
            "owner_count": 1,
            "target_graph_side": graph_rows[0]["t_side"],
            "target_graph_leaf_row_id": graph_rows[0]["leaf_row_id"],
            "target_boundary_only_side": boundary_rows[0]["t_side"],
            "target_boundary_only_leaf_row_id":
                boundary_rows[0]["leaf_row_id"],
            "source_2D_sheet_cell_count": 1,
            "target_2D_sheet_cell_count": 1,
            "source_target_1D_intersection_segment_count": 1,
            "source_target_0D_endpoint_incidence_count": 2,
            "local_lineage_materialized": True,
            "whole_original_tube_credit": 0,
            "global_exact_key_disposition_credit": 0,
        }))
    return output


def audit_single_obstruction(
    leaves: list[dict[str, Any]],
    collars: dict[str, dict[str, Any]],
    registry: dict[str, Any],
    r174: Any,
    leaf_packed_sha256: dict[str, str],
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    reasons: Counter[str] = Counter()
    classes: Counter[str] = Counter()
    for index, leaf in enumerate(leaves, 1):
        collar = collars[leaf["occurrence_row_id"]]
        signature, failures = r174.certify_signature(
            collar["chart"],
            atlas_box(leaf, r174),
            collar["owner_target"],
            registry,
        )
        require(
            signature is None
            and failures == [collar["reason_label"]]
            and collar["reason_label"].startswith(
                "wall_endpoint_or_count_transition:"
            ),
            f"sole obstruction:{leaf['row_id']}",
        )
        reasons[failures[0]] += 1
        classes[leaf["graph_classification"] + "|" + failures[0]] += 1
        rows.append(closed_row({
            "leaf_row_id": leaf["row_id"],
            "Round182_leaf_packed_sha256":
                leaf_packed_sha256[leaf["row_id"]],
            "origin_row_id": collar["origin_row_id"],
            "graph_classification": leaf["graph_classification"],
            "only_signature_failure": failures[0],
            "only_signature_failure_class":
                "INTEGER_WALL_ENDPOINT_OR_COUNT_TRANSITION",
            "all_nonwall_signature_fields_strict_on_closed_enclosure": True,
            "absence_of_carried_rows_not_used_as_positive_evidence": True,
            "whole_original_tube_credit": 0,
            "global_exact_key_disposition_credit": 0,
        }))
        if index % 64 == 0 or index == len(leaves):
            print(
                f"Round204 signature obstruction audit {index}/{len(leaves)}",
                file=sys.stderr,
                flush=True,
            )
    require(
        len(rows) == EXPECTED_LEAF_COUNT
        and reasons == Counter({
            "wall_endpoint_or_count_transition:X:0": 256,
            "wall_endpoint_or_count_transition:Y:0": 256,
        }),
        "single obstruction census",
    )
    return rows


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


def source_sign(leaf: dict[str, Any]) -> str:
    box = qbox(leaf["box"])
    if box[1] <= 0 and box[0] < 0:
        return "NEGATIVE"
    if box[0] >= 0 and box[1] > 0:
        return "POSITIVE"
    raise Round204Error(f"source t side:{leaf['row_id']}")


def touches_t0(leaf: dict[str, Any]) -> bool:
    box = qbox(leaf["box"])
    return box[0] == 0 or box[1] == 0


def event_token(
    wall_axis: str,
    source: str,
    target: str,
) -> str | None:
    require(source in SIGNS and target in SIGNS, "event signs")
    if source == target:
        return None
    return wall_axis + ("+" if source == "NEGATIVE" else "-")


def build_open_region_payloads(
    *,
    leaves: list[dict[str, Any]],
    collars: dict[str, dict[str, Any]],
    walls: dict[str, dict[str, Any]],
    anchors: dict[str, dict[str, Any]],
    registry: dict[str, Any],
    r174: Any,
    tail_geometry: list[dict[str, Any]],
    leaf_packed_sha256: dict[str, str],
) -> list[dict[str, Any]]:
    geometry_by_leaf = {
        row["leaf_row_id"]: row for row in tail_geometry
    }
    regions: list[dict[str, Any]] = []
    for leaf in leaves:
        collar = collars[leaf["occurrence_row_id"]]
        wall = walls[leaf["occurrence_row_id"]]
        origin_id = collar["origin_row_id"]
        classification = leaf["graph_classification"]
        src_sign = source_sign(leaf)
        if classification == "EMPTY":
            lower = status_sign(leaf["lower_t_face_status"])
            upper = status_sign(leaf["upper_t_face_status"])
            require(
                lower is not None and lower == upper,
                f"empty target sign:{leaf['row_id']}",
            )
            target_regions = [(
                lower,
                "NO_TARGET_SHEET_REGION",
            )]
            target_sheet_exists = False
        elif classification == "FULL_2D":
            lower = status_sign(leaf["lower_t_face_status"])
            upper = status_sign(leaf["upper_t_face_status"])
            require(
                lower == "NEGATIVE" and upper == "POSITIVE",
                f"full target graph bracket:{leaf['row_id']}",
            )
            target_regions = [
                ("NEGATIVE", "TARGET_GRAPH_NEGATIVE_SIDE"),
                ("POSITIVE", "TARGET_GRAPH_POSITIVE_SIDE"),
            ]
            target_sheet_exists = True
        else:
            require(
                classification == "RESIDUAL_3D"
                and leaf["row_id"] in geometry_by_leaf,
                f"tail geometry support:{leaf['row_id']}",
            )
            geometry = geometry_by_leaf[leaf["row_id"]]
            if geometry["target_2D_sheet_count"] == 0:
                target_regions = [(
                    src_sign,
                    "TAIL_BOUNDARY_ONLY_SINGLE_REGION",
                )]
                target_sheet_exists = False
            else:
                target_regions = [
                    (
                        src_sign,
                        "TAIL_TARGET_GRAPH_SAME_SIGN_OUTER_REGION",
                    ),
                    (
                        "POSITIVE"
                        if src_sign == "NEGATIVE"
                        else "NEGATIVE",
                        "TAIL_TARGET_GRAPH_OPPOSITE_SIGN_"
                        "SOURCE_ADJACENT_REGION",
                    ),
                ]
                target_sheet_exists = True
        for target_sign, region_kind in target_regions:
            token = event_token(
                wall["axis"],
                src_sign,
                target_sign,
            )
            word = [] if token is None else [token]
            events = [] if token is None else [
                [token, wall["integer_wall"]]
            ]
            key = r174.exact_key(
                collar["chart"],
                collar["owner_target"],
                tuple(word),
                registry,
            )
            anchor = anchors[origin_id]
            require(
                anchor["owner_target"] == collar["owner_target"]
                and anchor["signed_wall_word"] == []
                and anchor["roof"] == 1
                and key["row"] == [
                    collar["chart"],
                    collar["owner_target"],
                    word,
                    len(word) + 1,
                ],
                f"region exact key:{leaf['row_id']}:{region_kind}",
            )
            payload = [
                leaf["row_id"],
                region_kind,
                src_sign,
                target_sign,
                key["identifier"],
            ]
            regions.append({
                "region_row_id":
                    f"round204-wall-open-region:{digest(payload)}",
                "leaf_row_id": leaf["row_id"],
                "Round182_leaf_packed_sha256":
                    leaf_packed_sha256[leaf["row_id"]],
                "occurrence_row_id": leaf["occurrence_row_id"],
                "origin_row_id": origin_id,
                "parent_id": collar["parent_id"],
                "retained_child_row_id": leaf["retained_child_row_id"],
                "chart": collar["chart"],
                "owner_target": collar["owner_target"],
                "base_refinement_path": leaf["base_refinement_path"],
                "leaf_exact_box": leaf["box"],
                "leaf_exact_coordinate_volume": leaf["coordinate_volume"],
                "ambient_dimension": 3,
                "strict_open_region": True,
                "positive_coordinate_volume": True,
                "individual_curved_region_exact_volume_not_claimed": True,
                "leaf_outer_volume_counted_once_in_exact_conservation": True,
                "graph_classification": classification,
                "region_kind": region_kind,
                "tail_region": classification == "RESIDUAL_3D",
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
                "crossing_key_parent_observed": token is None,
                "crossing_key_binding_source": (
                    "FACE_ADJACENT_ROUND174_RESOLVED_EMPTY_WORD_ANCHOR"
                    if token is None
                    else
                    "PINNED_GATE5_REGISTRY_AND_EXACT_SINGLE_WALL_SIGN_CHANGE"
                ),
                "source_t0_sheet_incident": touches_t0(leaf),
                "half_open_source_sheet_owner": (
                    src_sign == "POSITIVE"
                    if touches_t0(leaf)
                    else None
                ),
                "target_graph_sheet_incident": target_sheet_exists,
                "half_open_target_sheet_owner": (
                    target_sign == "POSITIVE"
                    if target_sheet_exists
                    else None
                ),
                "source_sheet_row_id": None,
                "target_sheet_row_id": None,
                "signature_uniqueness_status": "UNIQUE",
                "conflicting_signature_count": 0,
                "missing_signature_field_count": 0,
                "formal_local_signature_credit": 1,
                "whole_original_tube_credit": 0,
                "global_exact_key_disposition_credit": 0,
            })
    regions.sort(key=lambda row: row["region_row_id"])
    require(
        len(regions) == EXPECTED_OPEN_REGION_COUNT
        and len({
            row["region_row_id"] for row in regions
        }) == EXPECTED_OPEN_REGION_COUNT
        and Counter(row["tail_region"] for row in regions)[True]
        == EXPECTED_TAIL_REGION_COUNT,
        "formal open region census",
    )
    words = Counter(
        canonical_bytes(row["signed_wall_word"]).decode()
        for row in regions
    )
    tail_words = Counter(
        canonical_bytes(row["signed_wall_word"]).decode()
        for row in regions if row["tail_region"]
    )
    require(
        words == Counter({
            "[]": 512,
            "[\"X+\"]": 56,
            "[\"X-\"]": 56,
            "[\"Y+\"]": 56,
            "[\"Y-\"]": 56,
        })
        and tail_words == Counter({
            "[]": 64,
            "[\"X+\"]": 8,
            "[\"X-\"]": 8,
            "[\"Y+\"]": 8,
            "[\"Y-\"]": 8,
        }),
        "formal word histograms",
    )
    return regions


def relative_t0_target_sign(
    leaf: dict[str, Any],
    tail_by_leaf: dict[str, dict[str, Any]],
) -> str:
    box = qbox(leaf["box"])
    require(box[0] == 0 or box[1] == 0,
            f"t0 face required:{leaf['row_id']}")
    status = (
        leaf["lower_t_face_status"]
        if box[0] == 0
        else leaf["upper_t_face_status"]
    )
    value = status_sign(status)
    if value is not None:
        return value
    require(
        status == "U" and leaf["row_id"] in tail_by_leaf,
        f"tail t0 sign evidence:{leaf['row_id']}",
    )
    strict = tail_by_leaf[leaf["row_id"]][
        "target_t0_p_outer_sign"
    ]
    require(strict in STRICT_SIGNS,
            f"strict tail p-relative sign:{leaf['row_id']}")
    return "POSITIVE" if strict == "STRICT_POSITIVE" else "NEGATIVE"


def build_sheet_payloads(
    *,
    leaves: list[dict[str, Any]],
    collars: dict[str, dict[str, Any]],
    walls: dict[str, dict[str, Any]],
    regions: list[dict[str, Any]],
    tail_geometry: list[dict[str, Any]],
) -> tuple[
    list[dict[str, Any]],
    list[dict[str, Any]],
    dict[str, str],
    dict[str, str],
]:
    regions_by_leaf: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in regions:
        regions_by_leaf[row["leaf_row_id"]].append(row)
    leaf_by_id = {row["row_id"]: row for row in leaves}
    tail_by_leaf = {
        row["leaf_row_id"]: row for row in tail_geometry
    }

    source_groups: dict[bytes, list[dict[str, Any]]] = defaultdict(list)
    source_keys: dict[bytes, list[Any]] = {}
    for leaf in leaves:
        if not touches_t0(leaf):
            continue
        collar = collars[leaf["occurrence_row_id"]]
        wall = walls[leaf["occurrence_row_id"]]
        box = leaf["box"]
        key = [
            collar["chart"],
            collar["owner_target"],
            wall["axis"],
            wall["integer_wall"],
            box[2], box[3], box[4], box[5],
        ]
        encoded = canonical_bytes(key)
        source_keys[encoded] = key
        source_groups[encoded].append(leaf)
    require(
        len(source_groups) == EXPECTED_SOURCE_SHEET_CELL_COUNT
        and sum(len(rows) for rows in source_groups.values()) == 448,
        "source t0 sheet pairing scope",
    )
    source_sheets: list[dict[str, Any]] = []
    source_sheet_by_leaf: dict[str, str] = {}
    for encoded, group in sorted(source_groups.items()):
        require(len(group) == 2, "source sheet pair size")
        by_sign = {source_sign(leaf): leaf for leaf in group}
        require(
            set(by_sign) == {"NEGATIVE", "POSITIVE"},
            "source sheet signed sides",
        )
        negative = by_sign["NEGATIVE"]
        positive = by_sign["POSITIVE"]
        incident_parent_ids = {
            collars[leaf["occurrence_row_id"]]["parent_id"]
            for leaf in group
        }
        require(
            len(incident_parent_ids) == 2,
            "source sheet cross-parent local pair",
        )
        signs = {
            relative_t0_target_sign(leaf, tail_by_leaf)
            for leaf in group
        }
        require(len(signs) == 1, "source sheet relative target sign")
        target_sign = next(iter(signs))
        incident_regions = [
            row for leaf in group
            for row in regions_by_leaf[leaf["row_id"]]
            if row["target_factor_sign"] == target_sign
        ]
        require(
            len(incident_regions) == 2
            and {row["source_sign"] for row in incident_regions}
            == {"NEGATIVE", "POSITIVE"},
            "source sheet incident region pair",
        )
        owner_region = next(
            row for row in incident_regions
            if row["source_sign"] == "POSITIVE"
        )
        key = source_keys[encoded]
        sheet_id = (
            f"round204-source-t0-sheet-cell:{digest(key)}"
        )
        payload = {
            "sheet_row_id": sheet_id,
            "sheet_kind": "SOURCE_EXACT_T0_SHEET_CELL",
            "ambient_dimension": 2,
            "incident_parent_ids": sorted(incident_parent_ids),
            "chart": key[0],
            "owner_target": key[1],
            "wall_axis": key[2],
            "integer_wall": key[3],
            "base_p_s_exact_bounds": key[4:],
            "exact_ambient_bounds": [
                "0", "0", *key[4:],
            ],
            "source_wall_factor_exact": "(9/25)*t",
            "source_wall_factor_exact_zero_set": "t=0",
            "relative_interior_target_factor_sign": target_sign,
            "negative_t_leaf_row_id": negative["row_id"],
            "positive_t_leaf_row_id": positive["row_id"],
            "negative_t_origin_row_id":
                collars[negative["occurrence_row_id"]]["origin_row_id"],
            "positive_t_origin_row_id":
                collars[positive["occurrence_row_id"]]["origin_row_id"],
            "incident_open_region_row_ids": sorted(
                row["region_row_id"] for row in incident_regions
            ),
            "half_open_owner_policy":
                "OUTCOME_BLIND_POSITIVE_T_SIDE_OWNS__"
                "NEGATIVE_T_SIDE_IS_SHADOW",
            "half_open_owner_leaf_row_id": positive["row_id"],
            "half_open_shadow_leaf_row_id": negative["row_id"],
            "half_open_owner_region_row_id":
                owner_region["region_row_id"],
            "tail_source_sheet_cell":
                negative["graph_classification"] == "RESIDUAL_3D"
                and positive["graph_classification"] == "RESIDUAL_3D",
            "boundary_1D_row_ids": [],
            "boundary_0D_row_ids": [],
            "source_target_intersection_1D_row_ids": [],
            "local_dimension_lineage_materialized": True,
            "lower_dimensional_credit": 0,
            "whole_original_tube_credit": 0,
            "global_exact_key_disposition_credit": 0,
        }
        source_sheets.append(payload)
        for leaf in group:
            source_sheet_by_leaf[leaf["row_id"]] = sheet_id
    require(
        len(source_sheets) == EXPECTED_SOURCE_SHEET_CELL_COUNT
        and Counter(
            row["tail_source_sheet_cell"] for row in source_sheets
        )[True] == EXPECTED_TAIL_PAIR_COUNT,
        "source sheet census",
    )

    target_sheets: list[dict[str, Any]] = []
    target_sheet_by_leaf: dict[str, str] = {}
    for leaf in leaves:
        tail = tail_by_leaf.get(leaf["row_id"])
        sheet_exists = (
            leaf["graph_classification"] == "FULL_2D"
            or (
                tail is not None
                and tail["target_2D_sheet_count"] == 1
            )
        )
        if not sheet_exists:
            continue
        collar = collars[leaf["occurrence_row_id"]]
        wall = walls[leaf["occurrence_row_id"]]
        leaf_regions = regions_by_leaf[leaf["row_id"]]
        negative = [
            row for row in leaf_regions
            if row["target_factor_sign"] == "NEGATIVE"
        ]
        positive = [
            row for row in leaf_regions
            if row["target_factor_sign"] == "POSITIVE"
        ]
        require(
            len(negative) == len(positive) == 1,
            f"target sheet incident regions:{leaf['row_id']}",
        )
        key = [
            leaf["row_id"],
            collar["chart"],
            collar["owner_target"],
            wall["axis"],
            wall["integer_wall"],
            leaf["box"][2:],
        ]
        sheet_id = f"round204-target-graph-sheet-cell:{digest(key)}"
        target_sheet_by_leaf[leaf["row_id"]] = sheet_id
        target_sheets.append({
            "sheet_row_id": sheet_id,
            "sheet_kind": "TARGET_REGULAR_GRAPH_SHEET_CELL",
            "ambient_dimension": 2,
            "leaf_row_id": leaf["row_id"],
            "origin_row_id": collar["origin_row_id"],
            "parent_id": collar["parent_id"],
            "chart": collar["chart"],
            "owner_target": collar["owner_target"],
            "wall_axis": wall["axis"],
            "integer_wall": wall["integer_wall"],
            "base_p_s_exact_bounds": leaf["box"][2:],
            "leaf_t_exact_bounds": leaf["box"][:2],
            "target_factor_graph_axis": "t",
            "target_t_derivative_sign": (
                tail["target_t_derivative_sign"]
                if tail is not None
                else "STRICT_POSITIVE"
            ),
            "existence_certification": (
                "ROUND204_TAIL_T_BRACKET_MONOTONICITY_AND_"
                "P_OUTER_INTERVAL_NEWTON"
                if tail is not None
                else "PINNED_ROUND182_FULL_2D_ENDPOINT_BRACKET"
            ),
            "negative_side_region_row_id":
                negative[0]["region_row_id"],
            "positive_side_region_row_id":
                positive[0]["region_row_id"],
            "half_open_owner_policy":
                "TARGET_FACTOR_POSITIVE_SIDE_OWNS__"
                "NEGATIVE_SIDE_IS_SHADOW",
            "half_open_owner_region_row_id":
                positive[0]["region_row_id"],
            "half_open_shadow_region_row_id":
                negative[0]["region_row_id"],
            "source_sign_on_leaf": source_sign(leaf),
            "source_t0_sheet_row_id":
                source_sheet_by_leaf.get(leaf["row_id"]),
            "exact_source_target_intersection_on_p0_boundary":
                tail is not None,
            "boundary_1D_row_ids": [],
            "boundary_0D_row_ids": [],
            "source_target_intersection_1D_row_ids": [],
            "local_dimension_lineage_materialized": True,
            "lower_dimensional_credit": 0,
            "whole_original_tube_credit": 0,
            "global_exact_key_disposition_credit": 0,
        })
    require(
        len(target_sheets) == EXPECTED_TARGET_SHEET_CELL_COUNT
        and Counter(
            row["exact_source_target_intersection_on_p0_boundary"]
            for row in target_sheets
        )[True] == EXPECTED_TAIL_PAIR_COUNT,
        "target sheet census",
    )
    for region in regions:
        region["source_sheet_row_id"] = source_sheet_by_leaf.get(
            region["leaf_row_id"]
        )
        region["target_sheet_row_id"] = target_sheet_by_leaf.get(
            region["leaf_row_id"]
        )
        require(
            (region["source_sheet_row_id"] is not None)
            == region["source_t0_sheet_incident"]
            and (region["target_sheet_row_id"] is not None)
            == region["target_graph_sheet_incident"],
            f"region sheet incidence:{region['region_row_id']}",
        )
    return (
        source_sheets,
        target_sheets,
        source_sheet_by_leaf,
        target_sheet_by_leaf,
    )


def build_dimension_boundary_lineage(
    source_sheets: list[dict[str, Any]],
    target_sheets: list[dict[str, Any]],
) -> tuple[
    list[dict[str, Any]],
    list[dict[str, Any]],
    list[dict[str, Any]],
    list[dict[str, Any]],
]:
    edge_incidences: dict[bytes, list[dict[str, Any]]] = defaultdict(list)
    edge_keys: dict[bytes, list[Any]] = {}

    def point_key(
        sheet: dict[str, Any],
        p: str,
        s: str,
        *,
        source: bool,
    ) -> list[Any]:
        prefix = (
            "EXACT_T0_P0_S_POINT"
            if p == "0"
            else (
                "EXACT_SOURCE_T0_P_S_POINT"
                if source
                else "TARGET_GRAPH_P_S_POINT"
            )
        )
        return [
            prefix,
            sheet["chart"],
            sheet["owner_target"],
            sheet["wall_axis"],
            sheet["integer_wall"],
            p,
            s,
        ]

    def add_edge(
        sheet: dict[str, Any],
        key: list[Any],
        boundary: str,
        endpoints: list[list[Any]],
    ) -> None:
        encoded = canonical_bytes(key)
        edge_keys[encoded] = key
        edge_incidences[encoded].append({
            "sheet_row_id": sheet["sheet_row_id"],
            "sheet_kind": sheet["sheet_kind"],
            "sheet_owner_region_row_id":
                sheet["half_open_owner_region_row_id"],
            "boundary_name": boundary,
            "endpoint_keys": endpoints,
        })

    for sheet in source_sheets:
        p0, p1, s0, s1 = sheet["base_p_s_exact_bounds"]
        common = [
            sheet["chart"],
            sheet["owner_target"],
            sheet["wall_axis"],
            sheet["integer_wall"],
        ]
        for boundary, p in (("p-", p0), ("p+", p1)):
            kind = (
                "EXACT_T0_P0_S_SEGMENT"
                if p == "0"
                else "EXACT_SOURCE_T0_P_FIXED_S_SEGMENT"
            )
            add_edge(
                sheet,
                [kind, *common, p, s0, s1],
                boundary,
                [
                    point_key(sheet, p, s0, source=True),
                    point_key(sheet, p, s1, source=True),
                ],
            )
        for boundary, s in (("s-", s0), ("s+", s1)):
            add_edge(
                sheet,
                [
                    "EXACT_SOURCE_T0_S_FIXED_P_SEGMENT",
                    *common,
                    s, p0, p1,
                ],
                boundary,
                [
                    point_key(sheet, p0, s, source=True),
                    point_key(sheet, p1, s, source=True),
                ],
            )

    for sheet in target_sheets:
        p0, p1, s0, s1 = sheet["base_p_s_exact_bounds"]
        common = [
            sheet["chart"],
            sheet["owner_target"],
            sheet["wall_axis"],
            sheet["integer_wall"],
        ]
        for boundary, p in (("p-", p0), ("p+", p1)):
            kind = (
                "EXACT_T0_P0_S_SEGMENT"
                if p == "0"
                else "TARGET_GRAPH_P_FIXED_S_CURVE"
            )
            add_edge(
                sheet,
                [kind, *common, p, s0, s1],
                boundary,
                [
                    point_key(sheet, p, s0, source=False),
                    point_key(sheet, p, s1, source=False),
                ],
            )
        for boundary, s in (("s-", s0), ("s+", s1)):
            add_edge(
                sheet,
                [
                    "TARGET_GRAPH_S_FIXED_P_CURVE",
                    *common,
                    s, p0, p1,
                ],
                boundary,
                [
                    point_key(sheet, p0, s, source=False),
                    point_key(sheet, p1, s, source=False),
                ],
            )

    edge_payloads: list[dict[str, Any]] = []
    sheet_to_edges: dict[str, list[str]] = defaultdict(list)
    point_to_edges: dict[bytes, list[dict[str, Any]]] = defaultdict(list)
    point_keys: dict[bytes, list[Any]] = {}
    for encoded, incidences in sorted(edge_incidences.items()):
        key = edge_keys[encoded]
        edge_id = f"round204-wall-1D-stratum:{digest(key)}"
        source_incident = [
            row for row in incidences
            if row["sheet_kind"] == "SOURCE_EXACT_T0_SHEET_CELL"
        ]
        ordered = sorted(
            incidences,
            key=lambda row: (
                0 if row["sheet_kind"]
                == "SOURCE_EXACT_T0_SHEET_CELL" else 1,
                row["sheet_row_id"],
            ),
        )
        owner = ordered[0]
        endpoint_keys = {
            canonical_bytes(point)
            for incidence in incidences
            for point in incidence["endpoint_keys"]
        }
        require(len(endpoint_keys) == 2,
                f"edge endpoint consistency:{edge_id}")
        endpoint_ids = []
        for point_encoded in sorted(endpoint_keys):
            point = next(
                endpoint
                for incidence in incidences
                for endpoint in incidence["endpoint_keys"]
                if canonical_bytes(endpoint) == point_encoded
            )
            point_keys[point_encoded] = point
            point_id = f"round204-wall-0D-stratum:{digest(point)}"
            endpoint_ids.append(point_id)
            point_to_edges[point_encoded].append({
                "edge_row_id": edge_id,
                "edge_kind": key[0],
                "owner_region_row_id":
                    owner["sheet_owner_region_row_id"],
                "incident_sheet_row_ids": sorted({
                    row["sheet_row_id"] for row in incidences
                }),
            })
        payload = {
            "edge_row_id": edge_id,
            "ambient_dimension": 1,
            "geometry_kind": key[0],
            "geometry_key": key,
            "incident_sheet_row_ids": sorted({
                row["sheet_row_id"] for row in incidences
            }),
            "incident_sheet_kind_counts": dict(sorted(Counter(
                row["sheet_kind"] for row in incidences
            ).items())),
            "raw_sheet_boundary_incidence_count": len(incidences),
            "half_open_owner_policy": (
                "SOURCE_SHEET_PRECEDENCE_THEN_LEXICOGRAPHIC_"
                "EXACT_BASE_CELL_OWNER"
                if source_incident
                else "LEXICOGRAPHIC_TARGET_SHEET_CELL_OWNER"
            ),
            "half_open_owner_sheet_row_id": owner["sheet_row_id"],
            "half_open_owner_region_row_id":
                owner["sheet_owner_region_row_id"],
            "half_open_shadow_sheet_row_ids": sorted(
                row["sheet_row_id"] for row in incidences
                if row["sheet_row_id"] != owner["sheet_row_id"]
            ),
            "exact_source_target_intersection":
                key[0] == "EXACT_T0_P0_S_SEGMENT",
            "endpoint_0D_row_ids": sorted(endpoint_ids),
            "local_dimension_lineage_materialized": True,
            "lower_dimensional_credit": 0,
            "whole_original_tube_credit": 0,
            "global_exact_key_disposition_credit": 0,
        }
        edge_payloads.append(payload)
        for incidence in incidences:
            sheet_to_edges[incidence["sheet_row_id"]].append(edge_id)

    corner_payloads: list[dict[str, Any]] = []
    edge_to_corners: dict[str, list[str]] = defaultdict(list)
    for encoded, incidences in sorted(point_to_edges.items()):
        key = point_keys[encoded]
        point_id = f"round204-wall-0D-stratum:{digest(key)}"
        ordered = sorted(
            incidences,
            key=lambda row: (
                0 if row["edge_kind"] == "EXACT_T0_P0_S_SEGMENT"
                else (
                    1 if row["edge_kind"].startswith("EXACT_SOURCE")
                    else 2
                ),
                row["edge_row_id"],
            ),
        )
        owner = ordered[0]
        incident_edges = sorted({
            row["edge_row_id"] for row in incidences
        })
        incident_sheets = sorted({
            sheet_id
            for row in incidences
            for sheet_id in row["incident_sheet_row_ids"]
        })
        corner_payloads.append({
            "point_row_id": point_id,
            "ambient_dimension": 0,
            "geometry_kind": key[0],
            "geometry_key": key,
            "incident_1D_row_ids": incident_edges,
            "incident_2D_sheet_row_ids": incident_sheets,
            "raw_edge_endpoint_incidence_count": len(incidences),
            "half_open_owner_policy":
                "INTERSECTION_THEN_SOURCE_THEN_TARGET_EDGE_PRECEDENCE__"
                "LEXICOGRAPHIC_OWNER",
            "half_open_owner_1D_row_id": owner["edge_row_id"],
            "half_open_owner_region_row_id":
                owner["owner_region_row_id"],
            "half_open_shadow_1D_row_ids": [
                edge for edge in incident_edges
                if edge != owner["edge_row_id"]
            ],
            "exact_source_target_intersection_endpoint":
                key[0] == "EXACT_T0_P0_S_POINT",
            "local_dimension_lineage_materialized": True,
            "lower_dimensional_credit": 0,
            "whole_original_tube_credit": 0,
            "global_exact_key_disposition_credit": 0,
        })
        for edge_id in incident_edges:
            edge_to_corners[edge_id].append(point_id)

    edge_rows: list[dict[str, Any]] = []
    for payload in edge_payloads:
        require(
            sorted(payload["endpoint_0D_row_ids"])
            == sorted(edge_to_corners[payload["edge_row_id"]]),
            f"edge/corner endpoints:{payload['edge_row_id']}",
        )
        edge_rows.append(closed_row(payload))
    corner_rows = [
        closed_row(payload) for payload in corner_payloads
    ]
    corner_by_edge = {
        edge_id: sorted(point_ids)
        for edge_id, point_ids in edge_to_corners.items()
    }
    intersection_edges = [
        row for row in edge_rows
        if row["exact_source_target_intersection"]
    ]
    require(
        len(intersection_edges)
        == EXPECTED_EXACT_INTERSECTION_SEGMENT_COUNT
        and all(
            row["incident_sheet_kind_counts"]
            == {
                "SOURCE_EXACT_T0_SHEET_CELL": 2,
                "TARGET_REGULAR_GRAPH_SHEET_CELL": 2,
            }
            for row in intersection_edges
        )
        and sum(
            row["incident_sheet_kind_counts"][
                "SOURCE_EXACT_T0_SHEET_CELL"
            ]
            for row in intersection_edges
        ) == EXPECTED_TAIL_PAIR_COUNT
        and sum(
            row["incident_sheet_kind_counts"][
                "TARGET_REGULAR_GRAPH_SHEET_CELL"
            ]
            for row in intersection_edges
        ) == EXPECTED_TAIL_PAIR_COUNT,
        "exact source-target intersection ledger",
    )

    source_closed: list[dict[str, Any]] = []
    target_closed: list[dict[str, Any]] = []
    for sheet in [*source_sheets, *target_sheets]:
        edge_ids = sorted(set(sheet_to_edges[sheet["sheet_row_id"]]))
        require(len(edge_ids) == 4,
                f"sheet four boundary edges:{sheet['sheet_row_id']}")
        corner_ids = sorted({
            point_id
            for edge_id in edge_ids
            for point_id in corner_by_edge[edge_id]
        })
        require(len(corner_ids) == 4,
                f"sheet four corners:{sheet['sheet_row_id']}")
        sheet["boundary_1D_row_ids"] = edge_ids
        sheet["boundary_0D_row_ids"] = corner_ids
        sheet["source_target_intersection_1D_row_ids"] = [
            edge_id for edge_id in edge_ids
            if next(
                row for row in edge_rows
                if row["edge_row_id"] == edge_id
            )["exact_source_target_intersection"]
        ]
        closed = closed_row(sheet)
        if sheet["sheet_kind"] == "SOURCE_EXACT_T0_SHEET_CELL":
            source_closed.append(closed)
        else:
            target_closed.append(closed)
    source_closed.sort(key=lambda row: row["sheet_row_id"])
    target_closed.sort(key=lambda row: row["sheet_row_id"])
    edge_rows.sort(key=lambda row: row["edge_row_id"])
    corner_rows.sort(key=lambda row: row["point_row_id"])
    require(
        len(source_closed) == EXPECTED_SOURCE_SHEET_CELL_COUNT
        and len(target_closed) == EXPECTED_TARGET_SHEET_CELL_COUNT
        and all(len(row["endpoint_0D_row_ids"]) == 2 for row in edge_rows)
        and all(row["half_open_owner_region_row_id"] for row in edge_rows)
        and all(
            row["half_open_owner_region_row_id"] for row in corner_rows
        ),
        "complete dimensional half-open lineage",
    )
    return source_closed, target_closed, edge_rows, corner_rows


def build_tail_signature_glue(
    tail_pairs: list[dict[str, Any]],
    regions: list[dict[str, Any]],
    source_sheet_by_leaf: dict[str, str],
    target_sheet_by_leaf: dict[str, str],
    source_sheets: list[dict[str, Any]],
    target_sheets: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    by_leaf: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in regions:
        if row["tail_region"]:
            by_leaf[row["leaf_row_id"]].append(row)
    source_by_id = {
        row["sheet_row_id"]: row for row in source_sheets
    }
    target_by_id = {
        row["sheet_row_id"]: row for row in target_sheets
    }
    output: list[dict[str, Any]] = []
    for pair in tail_pairs:
        negative = by_leaf[pair["negative_t_leaf_row_id"]]
        positive = by_leaf[pair["positive_t_leaf_row_id"]]
        combined = [*negative, *positive]
        crossing = [
            row for row in combined if row["wall_crossing_count"] == 1
        ]
        empty = [
            row for row in combined if row["wall_crossing_count"] == 0
        ]
        graph_leaf = pair["target_graph_leaf_row_id"]
        boundary_leaf = pair["target_boundary_only_leaf_row_id"]
        require(
            len(combined) == 3
            and len(crossing) == 1
            and len(empty) == 2
            and len(by_leaf[graph_leaf]) == 2
            and len(by_leaf[boundary_leaf]) == 1
            and crossing[0]["leaf_row_id"] == graph_leaf
            and len({row["official_key_id"] for row in empty}) == 1
            and crossing[0]["official_key_id"]
            != empty[0]["official_key_id"],
            f"tail empty-event-empty:{pair['tail_pair_row_id']}",
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
            f"tail signature invariants:{pair['tail_pair_row_id']}",
        )
        source_sheet_id = source_sheet_by_leaf[
            pair["positive_t_leaf_row_id"]
        ]
        require(
            source_sheet_by_leaf[pair["negative_t_leaf_row_id"]]
            == source_sheet_id,
            f"tail source sheet pair:{pair['tail_pair_row_id']}",
        )
        target_sheet_id = target_sheet_by_leaf[graph_leaf]
        source_sheet = source_by_id[source_sheet_id]
        target_sheet = target_by_id[target_sheet_id]
        intersections = sorted(set(
            source_sheet["source_target_intersection_1D_row_ids"]
        ) & set(
            target_sheet["source_target_intersection_1D_row_ids"]
        ))
        require(
            len(intersections) == 1
            and source_sheet["half_open_owner_leaf_row_id"]
            == pair["positive_t_leaf_row_id"]
            and target_sheet["half_open_owner_region_row_id"]
            in {row["region_row_id"] for row in combined},
            f"tail dimensional glue:{pair['tail_pair_row_id']}",
        )
        output.append(closed_row({
            "pair_glue_row_id":
                "round204-wall-signature-pair-glue:"
                f"{digest(pair['tail_pair_row_id'])}",
            "tail_pair_row_id": pair["tail_pair_row_id"],
            "negative_t_leaf_row_id": pair["negative_t_leaf_row_id"],
            "positive_t_leaf_row_id": pair["positive_t_leaf_row_id"],
            "source_sheet_2D_row_id": source_sheet_id,
            "target_sheet_2D_row_id": target_sheet_id,
            "source_target_intersection_1D_row_id": intersections[0],
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
            "materialized_local_open_region_count": 3,
            "whole_original_tube_credit": 0,
            "global_exact_key_disposition_credit": 0,
        }))
    output.sort(key=lambda row: row["pair_glue_row_id"])
    require(len(output) == EXPECTED_TAIL_PAIR_COUNT,
            "tail signature glue census")
    return output


def build_key_fibres(
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
        output.append(closed_row({
            "official_key_id": key_id,
            "official_key_ordinal": first["official_key_ordinal"],
            "official_key_row": first["official_key_row"],
            "local_region_occurrence_count": len(rows),
            "distinct_origin_count":
                len({row["origin_row_id"] for row in rows}),
            "tail_region_occurrence_count": sum(
                row["tail_region"] for row in rows
            ),
            "local_region_row_ids": sorted(
                row["region_row_id"] for row in rows
            ),
            "join_cardinality_per_local_region": 1,
            "formal_local_join_materialized": True,
            "global_exact_key_fibre_exhausted": False,
            "whole_original_tube_credit": 0,
            "global_exact_key_disposition_credit": 0,
        }))
    output.sort(key=lambda row: row["official_key_ordinal"])
    require(
        len(output) == 12
        and [row["official_key_ordinal"] for row in output]
        == EXPECTED_KEY_ORDINALS
        and Counter(
            row["local_region_occurrence_count"] for row in output
        ) == Counter({28: 8, 128: 4})
        and Counter(
            row["tail_region_occurrence_count"] for row in output
        ) == Counter({4: 8, 16: 4}),
        "12 exact-key joins",
    )
    return output


def build_origin_completion_rows(
    *,
    scope182: dict[str, Any],
    regions: list[dict[str, Any]],
    source_sheets: list[dict[str, Any]],
    target_sheets: list[dict[str, Any]],
    edge_rows: list[dict[str, Any]],
    corner_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    regions_by_origin: dict[str, list[dict[str, Any]]] = defaultdict(list)
    leaves_by_origin: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for leaf in scope182["leaves"]:
        origin_id = scope182["collars"][
            leaf["occurrence_row_id"]
        ]["origin_row_id"]
        leaves_by_origin[origin_id].append(leaf)
    for row in regions:
        regions_by_origin[row["origin_row_id"]].append(row)
    source_by_origin: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in source_sheets:
        source_by_origin[row["negative_t_origin_row_id"]].append(row)
        source_by_origin[row["positive_t_origin_row_id"]].append(row)
    target_by_origin: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in target_sheets:
        target_by_origin[row["origin_row_id"]].append(row)
    edge_by_id = {row["edge_row_id"]: row for row in edge_rows}
    corner_by_id = {row["point_row_id"]: row for row in corner_rows}

    output: list[dict[str, Any]] = []
    for origin_id in sorted(scope182["origin_ids"]):
        leaves = leaves_by_origin[origin_id]
        local_regions = regions_by_origin[origin_id]
        source = source_by_origin[origin_id]
        target = target_by_origin[origin_id]
        sheet_ids = {
            row["sheet_row_id"] for row in [*source, *target]
        }
        relevant_edges = sorted({
            edge_id
            for sheet in [*source, *target]
            for edge_id in sheet["boundary_1D_row_ids"]
        })
        relevant_corners = sorted({
            point_id
            for edge_id in relevant_edges
            for point_id in edge_by_id[edge_id]["endpoint_0D_row_ids"]
        })
        require(
            len(leaves) == 8
            and len(local_regions) in {8, 15}
            and len(source) == 7
            and all(edge_id in edge_by_id for edge_id in relevant_edges)
            and all(point_id in corner_by_id for point_id in relevant_corners)
            and sum(
                (Q(leaf["coordinate_volume"]) for leaf in leaves),
                Q(0),
            ) == EXPECTED_ORIGIN_VOLUME,
            f"origin complete local cover:{origin_id}",
        )
        prior = scope182["origins"][origin_id]
        output.append(closed_row({
            "origin_row_id": origin_id,
            "Round182_origin_packed_sha256":
                scope182["origin_packed_sha256"][origin_id],
            "parent_id": next(
                scope182["collars"][leaf["occurrence_row_id"]][
                    "parent_id"
                ]
                for leaf in leaves
            ),
            "Round182_leaf_row_count": len(leaves),
            "Round182_leaf_row_ids": sorted(
                leaf["row_id"] for leaf in leaves
            ),
            "Round182_leaf_classification_counts": dict(sorted(Counter(
                leaf["graph_classification"] for leaf in leaves
            ).items())),
            "exact_input_coordinate_volume": str(EXPECTED_ORIGIN_VOLUME),
            "strict_open_3D_region_count": len(local_regions),
            "strict_open_3D_region_row_ids": sorted(
                row["region_row_id"] for row in local_regions
            ),
            "source_t0_2D_sheet_cell_count": len(source),
            "target_graph_2D_sheet_cell_count": len(target),
            "incident_2D_sheet_row_ids": sorted(sheet_ids),
            "incident_1D_stratum_row_ids": relevant_edges,
            "incident_0D_stratum_row_ids": relevant_corners,
            "distinct_local_exact_key_count": len({
                row["official_key_id"] for row in local_regions
            }),
            "local_exact_key_ids": sorted({
                row["official_key_id"] for row in local_regions
            }),
            "all_8_Round182_leaves_have_unique_local_signatures": True,
            "all_dimensions_have_deterministic_half_open_lineage": True,
            "Round182_fully_geometrically_replaced_original_tube":
                prior["fully_geometrically_replaced_original_tube"],
            "Round204_fully_locally_signature_replaced": True,
            "formal_local_replacement_credit": 1,
            "whole_original_tube_credit": 0,
            "global_exact_key_disposition_credit": 0,
        }))
    require(
        len(output) == EXPECTED_ORIGIN_COUNT
        and Counter(
            row["strict_open_3D_region_count"] for row in output
        ) == Counter({8: 32, 15: 32})
        and sum(
            row["formal_local_replacement_credit"] for row in output
        ) == EXPECTED_ORIGIN_COUNT
        and all(
            row["whole_original_tube_credit"] == 0
            and row["global_exact_key_disposition_credit"] == 0
            for row in output
        ),
        "64 origin local completion rows",
    )
    return output


def histogram_words(rows: list[dict[str, Any]]) -> dict[str, int]:
    return dict(sorted(Counter(
        canonical_bytes(row["signed_wall_word"]).decode()
        for row in rows
    ).items()))


def build_result(producer_sha256: str) -> dict[str, Any]:
    ctx.prec = 256
    print("Round204 pinning and loading Round182", file=sys.stderr, flush=True)
    formal = load_formal_inputs()
    evaluator = formal["evaluator"]
    r174 = evaluator.r179.r174
    scope182 = extract_round182_scope(formal["attachment182"])
    scope179 = extract_round179_scope(
        formal["source179"],
        scope182["occurrence_ids"],
        scope182["origin_ids"],
    )
    scope174 = extract_round174_scope(
        formal["attachment174"],
        scope182["origin_ids"],
        scope182["parent_ids"],
    )
    print("Round204 rebuilding formal empty-word anchors",
          file=sys.stderr, flush=True)
    anchors, anchor_parent_rows, anchor_origin_rows = (
        build_anchor_evidence(
            scope174,
            scope179,
            formal["registry"],
            r174,
        )
    )

    print("Round204 auditing all 512 sole obstructions",
          file=sys.stderr, flush=True)
    obstruction_rows = audit_single_obstruction(
        scope182["leaves"],
        scope182["collars"],
        formal["registry"],
        r174,
        scope182["leaf_packed_sha256"],
    )

    print("Round204 rebuilding 64 tail geometries",
          file=sys.stderr, flush=True)
    tail_geometry: list[dict[str, Any]] = []
    for index, leaf in enumerate(scope182["tail_leaves"], 1):
        occurrence = leaf["occurrence_row_id"]
        collar = scope182["collars"][occurrence]
        origin_id = collar["origin_row_id"]
        tail_geometry.append(analyze_tail_leaf(
            leaf,
            collar=collar,
            wall=scope179["walls"][occurrence],
            origin179=scope179["origins"][origin_id],
            origin182=scope182["origins"][origin_id],
            retained=scope179["retained"][
                leaf["retained_child_row_id"]
            ],
            evaluator=evaluator,
            leaf_packed_sha256=
                scope182["leaf_packed_sha256"][leaf["row_id"]],
            collar_packed_sha256=
                scope182["collar_packed_sha256"][occurrence],
            wall_packed_sha256=
                scope179["wall_packed_sha256"][occurrence],
        ))
        if index % 16 == 0 or index == EXPECTED_TAIL_LEAF_COUNT:
            print(
                f"Round204 tail geometry {index}/"
                f"{EXPECTED_TAIL_LEAF_COUNT}",
                file=sys.stderr,
                flush=True,
            )
    tail_geometry.sort(key=lambda row: row["leaf_row_id"])
    tail_pairs = build_tail_pairs(tail_geometry)
    require(
        len(tail_geometry) == EXPECTED_TAIL_LEAF_COUNT
        and Counter(
            row["target_2D_sheet_count"] for row in tail_geometry
        ) == Counter({0: 32, 1: 32}),
        "tail geometry census",
    )

    print("Round204 materializing 736 strict open regions",
          file=sys.stderr, flush=True)
    region_payloads = build_open_region_payloads(
        leaves=scope182["leaves"],
        collars=scope182["collars"],
        walls=scope179["walls"],
        anchors=anchors,
        registry=formal["registry"],
        r174=r174,
        tail_geometry=tail_geometry,
        leaf_packed_sha256=scope182["leaf_packed_sha256"],
    )
    (
        source_sheet_payloads,
        target_sheet_payloads,
        source_sheet_by_leaf,
        target_sheet_by_leaf,
    ) = build_sheet_payloads(
        leaves=scope182["leaves"],
        collars=scope182["collars"],
        walls=scope179["walls"],
        regions=region_payloads,
        tail_geometry=tail_geometry,
    )

    print("Round204 materializing 2D/1D/0D owner lineage",
          file=sys.stderr, flush=True)
    (
        source_sheet_rows,
        target_sheet_rows,
        edge_rows,
        corner_rows,
    ) = build_dimension_boundary_lineage(
        source_sheet_payloads,
        target_sheet_payloads,
    )
    region_rows = [
        closed_row(payload) for payload in region_payloads
    ]
    region_rows.sort(key=lambda row: row["region_row_id"])
    tail_glue_rows = build_tail_signature_glue(
        tail_pairs,
        region_rows,
        source_sheet_by_leaf,
        target_sheet_by_leaf,
        source_sheet_rows,
        target_sheet_rows,
    )
    fibre_rows = build_key_fibres(region_rows)
    origin_rows = build_origin_completion_rows(
        scope182=scope182,
        regions=region_rows,
        source_sheets=source_sheet_rows,
        target_sheets=target_sheet_rows,
        edge_rows=edge_rows,
        corner_rows=corner_rows,
    )

    tail_regions = [row for row in region_rows if row["tail_region"]]
    exact_intersection_edges = [
        row for row in edge_rows
        if row["exact_source_target_intersection"]
    ]
    exact_intersection_endpoints = [
        row for row in corner_rows
        if row["exact_source_target_intersection_endpoint"]
    ]
    require(
        len(tail_regions) == EXPECTED_TAIL_REGION_COUNT
        and len(exact_intersection_edges)
        == EXPECTED_EXACT_INTERSECTION_SEGMENT_COUNT
        and all(
            row["formal_local_signature_credit"] == 1
            and row["whole_original_tube_credit"] == 0
            and row["global_exact_key_disposition_credit"] == 0
            for row in region_rows
        ),
        "formal local replacement/no-promotion invariant",
    )
    pin_round182()

    relevant_attachment_bindings = {
        "collar_occurrence_rows_sha256": digest(sorted(
            scope182["collar_packed_sha256"].items()
        )),
        "all_512_leaf_packed_sha256": digest(sorted(
            scope182["leaf_packed_sha256"].items()
        )),
        "origin_replacement_rows_sha256": digest(sorted(
            scope182["origin_packed_sha256"].items()
        )),
        "Round179_wall_rows_sha256": digest(sorted(
            scope179["wall_packed_sha256"].items()
        )),
    }
    result = {
        "status": STATUS,
        "Round182_binding": {
            "manifest_sha256": R182_MANIFEST_SHA256,
            "manifest_entry_count": len(R182_PINS),
            "dependency_sha256": dict(sorted(R182_PINS.items())),
            "certificate_result_sha256":
                R182_CERTIFICATE_RESULT_SHA256,
            "attachment_result_sha256":
                R182_ATTACHMENT_RESULT_SHA256,
            "verification_result_sha256":
                R182_VERIFICATION_RESULT_SHA256,
            "verification_status":
                formal["verification182"]["status"],
            "complete_expected_certificate_rebuilt":
                formal["verification182"][
                    "complete_expected_certificate_rebuilt"
                ],
            "full_attachment_byte_for_byte_matched":
                formal["verification182"][
                    "full_attachment_byte_for_byte_matched"
                ],
            "formal_files_modified": False,
            "relevant_attachment_bindings":
                relevant_attachment_bindings,
        },
        "formal_scope_contract": {
            "target_obstacle": "G",
            "predicate_kind": "WALL",
            "Round182_origin_count": EXPECTED_ORIGIN_COUNT,
            "Round182_leaf_count": EXPECTED_LEAF_COUNT,
            "Round182_leaf_classification_counts":
                scope182["classification"],
            "strict_open_3D_region_count": len(region_rows),
            "tail_open_3D_region_count": len(tail_regions),
            "distinct_exact_key_join_count": len(fibre_rows),
            "all_signature_rows_formally_materialized": True,
            "all_64_origins_fully_locally_signature_replaced": True,
            "local_replacement_only": True,
            "whole_original_tube_credit": 0,
            "global_exact_key_disposition_credit": 0,
        },
        "empty_word_anchor_evidence_ledger": {
            "parent_row_count": len(anchor_parent_rows),
            "parent_rows_sha256": digest(anchor_parent_rows),
            "parent_rows": anchor_parent_rows,
            "origin_row_count": len(anchor_origin_rows),
            "origin_rows_sha256": digest(anchor_origin_rows),
            "origin_rows": anchor_origin_rows,
            "origin_adjacent_anchor_count_histogram":
                {"1": 32, "2": 32},
            "origin_adjacent_axis_histogram": {"p": 32, "t": 64},
        },
        "single_obstruction_evidence_ledger": {
            "row_count": len(obstruction_rows),
            "rows_sha256": digest(obstruction_rows),
            "rows": obstruction_rows,
            "only_reason_histogram": {
                "wall_endpoint_or_count_transition:X:0": 256,
                "wall_endpoint_or_count_transition:Y:0": 256,
            },
            "all_512_have_exactly_one_recorded_wall_reason": True,
            "all_nonwall_signature_fields_strict": True,
            "Round182_carried_rows_on_active_origins": 0,
            "absence_of_carried_rows_not_used_as_positive_evidence": True,
        },
        "tail_geometry_evidence_ledger": {
            "leaf_row_count": len(tail_geometry),
            "leaf_rows_sha256": digest(tail_geometry),
            "leaf_rows": tail_geometry,
            "pair_row_count": len(tail_pairs),
            "pair_rows_sha256": digest(tail_pairs),
            "pair_rows": tail_pairs,
            "target_graph_side_count": 32,
            "target_boundary_only_side_count": 32,
            "positive_t_source_sheet_owner_count": 32,
            "negative_t_source_sheet_shadow_count": 32,
        },
        "formal_local_open_3D_region_ledger": {
            "row_count": len(region_rows),
            "rows_sha256": digest(region_rows),
            "rows": region_rows,
            "tail_row_count": len(tail_regions),
            "tail_rows_sha256": digest(tail_regions),
            "leaf_region_count_histogram":
                {"1": 288, "2": 224},
            "origin_region_count_histogram": {"8": 32, "15": 32},
            "word_histogram": histogram_words(region_rows),
            "tail_word_histogram": histogram_words(tail_regions),
            "unique_signature_count": len(region_rows),
            "conflicting_signature_count": 0,
            "missing_signature_count": 0,
            "formal_local_signature_credit": len(region_rows),
            "whole_original_tube_credit": 0,
            "global_exact_key_disposition_credit": 0,
        },
        "formal_2D_sheet_lineage": {
            "source_sheet_row_count": len(source_sheet_rows),
            "source_sheet_rows_sha256": digest(source_sheet_rows),
            "source_sheet_rows": source_sheet_rows,
            "target_sheet_row_count": len(target_sheet_rows),
            "target_sheet_rows_sha256": digest(target_sheet_rows),
            "target_sheet_rows": target_sheet_rows,
            "source_sheet_tail_cell_count": 32,
            "target_sheet_tail_cell_count": 32,
            "all_source_sheets_have_positive_t_half_open_owner": True,
            "all_target_sheets_have_positive_factor_half_open_owner": True,
            "whole_original_tube_credit": 0,
            "global_exact_key_disposition_credit": 0,
        },
        "formal_1D_boundary_and_intersection_lineage": {
            "row_count": len(edge_rows),
            "rows_sha256": digest(edge_rows),
            "rows": edge_rows,
            "exact_source_target_intersection_segment_count":
                len(exact_intersection_edges),
            "exact_source_target_intersection_rows_sha256":
                digest(exact_intersection_edges),
            "exact_source_sheet_boundary_incidence_count": sum(
                row["incident_sheet_kind_counts"][
                    "SOURCE_EXACT_T0_SHEET_CELL"
                ]
                for row in exact_intersection_edges
            ),
            "exact_target_sheet_boundary_incidence_count": sum(
                row["incident_sheet_kind_counts"][
                    "TARGET_REGULAR_GRAPH_SHEET_CELL"
                ]
                for row in exact_intersection_edges
            ),
            "every_1D_stratum_has_exactly_two_0D_endpoints": True,
            "every_1D_stratum_has_one_half_open_owner": True,
            "whole_original_tube_credit": 0,
            "global_exact_key_disposition_credit": 0,
        },
        "formal_0D_endpoint_and_corner_lineage": {
            "row_count": len(corner_rows),
            "rows_sha256": digest(corner_rows),
            "rows": corner_rows,
            "exact_source_target_endpoint_row_count":
                len(exact_intersection_endpoints),
            "exact_source_target_endpoint_rows_sha256":
                digest(exact_intersection_endpoints),
            "every_0D_stratum_has_one_half_open_owner": True,
            "whole_original_tube_credit": 0,
            "global_exact_key_disposition_credit": 0,
        },
        "tail_pair_signature_glue_ledger": {
            "row_count": len(tail_glue_rows),
            "rows_sha256": digest(tail_glue_rows),
            "rows": tail_glue_rows,
            "empty_event_empty_pair_count": len(tail_glue_rows),
            "unexpected_signature_change_count": 0,
            "all_owner_target_outgoing_and_target_chart_unchanged": True,
            "whole_original_tube_credit": 0,
            "global_exact_key_disposition_credit": 0,
        },
        "origin_local_completion_ledger": {
            "row_count": len(origin_rows),
            "rows_sha256": digest(origin_rows),
            "rows": origin_rows,
            "fully_locally_signature_replaced_origin_count":
                len(origin_rows),
            "formal_local_replacement_credit": len(origin_rows),
            "whole_original_tube_credit": 0,
            "global_exact_key_disposition_credit": 0,
        },
        "exact_key_local_join_ledger": {
            "row_count": len(fibre_rows),
            "rows_sha256": digest(fibre_rows),
            "rows": fibre_rows,
            "official_key_ordinals": EXPECTED_KEY_ORDINALS,
            "all_736_regions_join_exactly_one_immutable_key": True,
            "many_local_occurrences_may_join_one_exact_key": True,
            "no_global_exact_key_fibre_exhausted": True,
            "global_source_G_exact_key_fibre_count":
                EXPECTED_SOURCE_G_KEY_COUNT,
            "global_source_G_exact_key_disposition_count": 0,
        },
        "exact_dimension_and_positive_volume_conservation": {
            "Round182_relevant_leaf_count": len(scope182["leaves"]),
            "Round182_relevant_input_coordinate_volume":
                str(scope182["input_volume"]),
            "Round182_closed_leaf_count": 448,
            "Round182_closed_coordinate_volume":
                str(scope182["closed_volume"]),
            "Round182_tail_leaf_count": len(scope182["tail_leaves"]),
            "Round182_tail_coordinate_volume":
                str(scope182["tail_volume"]),
            "Round204_locally_replaced_leaf_count":
                len(scope182["leaves"]),
            "Round204_output_cover_coordinate_volume":
                str(scope182["input_volume"]),
            "strict_positive_open_3D_region_count": len(region_rows),
            "individual_curved_open_region_volumes_not_summed": True,
            "each_leaf_outer_volume_counted_exactly_once": True,
            "all_2D_1D_0D_strata_have_zero_ambient_3D_volume": True,
            "integer_leaf_delta": 0,
            "exact_coordinate_volume_delta": "0",
        },
        "formal_local_replacement_and_strict_nonpromotion": {
            "materialized_local_signature_region_count":
                len(region_rows),
            "materialized_local_origin_completion_count":
                len(origin_rows),
            "whole_original_tube_credit": 0,
            "global_exact_key_disposition_credit": 0,
            "source_G_global_exact_key_dispositions":
                f"0/{EXPECTED_SOURCE_G_KEY_COUNT}",
            "D02": "BLOCKED",
            "global_Gate5_fields": "10/18",
            "global_complete_18_field_blocks": 0,
            "CM2": "NO-GO_FOR_CLAIM",
        },
        "probe_nondependency": {
            "Round192_probe_read_imported_or_pinned": False,
            "Round196_probe_read_imported_or_pinned": False,
            "probe_outputs_used_as_formal_inputs": False,
            "formal_result_rebuilt_from_pinned_Round182_chain": True,
        },
        "next_core_gate":
            "continue the remaining Round182 source-G residual origins; "
            "do not identify these local occurrences with whole global "
            "exact-key fibres",
        "provenance": {
            "schema": SCHEMA,
            "producer_sha256": producer_sha256,
            "python_flint_version": FLINT_VERSION,
            "effective_Arb_precision_bits": ctx.prec,
            "Round182_manifest_sha256": R182_MANIFEST_SHA256,
            "Round182_dependency_sha256":
                dict(sorted(R182_PINS.items())),
            "Round182_evaluator":
                "pinned independent Round182 verifier library",
            "Round182_files_modified": False,
        },
    }
    return result


def validate_output(path: Path) -> Path:
    require(not any(part == ".." for part in path.parts),
            "output parent alias")
    absolute = Path(os.path.abspath(os.fspath(path)))
    require(
        absolute.parent == HERE and absolute.parent.resolve() == HERE,
        "output exact directory",
    )
    allowed = (
        absolute.name == OUTPUT.name
        or (
            absolute.name.startswith(".cm2_round204_")
            and absolute.name.endswith("_certificate.json")
        )
    )
    require(allowed, "output allowlist")
    protected = {
        Path(__file__).resolve(),
        (HERE / R182_MANIFEST).resolve(),
    }
    protected.update((HERE / name).resolve() for name in R182_PINS)
    require(
        absolute.resolve(strict=False) not in protected,
        "protected output",
    )
    if absolute.exists() or absolute.is_symlink():
        metadata = absolute.lstat()
        require(
            stat.S_ISREG(metadata.st_mode)
            and not absolute.is_symlink()
            and metadata.st_nlink == 1,
            "output type",
        )
    return absolute


def safe_write(path: Path, data: bytes) -> None:
    absolute = validate_output(path)
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=f".{absolute.name}.",
        suffix=".tmp",
        dir=absolute.parent,
    )
    temporary = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, absolute)
        directory_descriptor = os.open(
            os.fspath(absolute.parent),
            os.O_RDONLY | getattr(os, "O_DIRECTORY", 0),
        )
        try:
            os.fsync(directory_descriptor)
        finally:
            os.close(directory_descriptor)
    finally:
        if temporary.exists():
            temporary.unlink()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=OUTPUT)
    arguments = parser.parse_args()
    producer_sha256 = sha256_bytes(regular_bytes(Path(__file__), 5_000_000))
    result = build_result(producer_sha256)
    envelope = {
        "schema": SCHEMA,
        "result": result,
        "result_sha256": digest(result),
    }
    safe_write(arguments.output, canonical_bytes(envelope) + b"\n")
    print(envelope["result_sha256"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
