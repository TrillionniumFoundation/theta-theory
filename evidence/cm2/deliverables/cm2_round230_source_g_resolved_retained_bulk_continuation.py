#!/usr/bin/env python3
"""Materialize certified local bulk bridges across the Round220 frontier.

This producer exhausts the 8,960 Round220 one-step resolved/retained
interfaces.  It certifies only strict positive-area local patches: an edge
requires an exact shared box face, equality of all ten immutable local
return-signature fields, and strict equal HPLUS/HMINUS signs on the whole
intersection patch.  No whole-interface claim is made.

The frozen Round211-to-Round225 incidence is used as the only seed.  New
known-block incidence is propagated only through the certified local bulk
bridges.  Known-block incidence is not a membership, component, maximality,
or global exact-key claim.
"""

from __future__ import annotations

import argparse
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
from typing import Any, Iterable


sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
PREFIX = "cm2_round230_source_g_resolved_retained_bulk_continuation"
OUTPUT = HERE / f"{PREFIX}_certificate.json"
SCHEMA = "cm2.round230.source-g-resolved-retained-bulk-continuation.v1"
STATUS = (
    "CERTIFIED_784_NON_EVENT_STRICT_POSITIVE_AREA_LOCAL_BULK_"
    "CONTINUATION_PATCHES__448_INTERFACES__464_NEW_KNOWN_BLOCK_"
    "INCIDENCES__ZERO_MEMBERSHIP_COMPONENT_MAXIMAL_OR_GLOBAL_CREDIT"
)

INPUTS = {
    "Round179_rows": (
        "cm2_round179_source_g_residual_tube_arrangement_rows.json",
        "f20b42c1fed781779b537b4d45bf44233eae1ed3ee620b95177a80f0eb2b5e42",
        "a5468800c1d89cd307a5a26c608550b04db79c64c562fb12bedb22d6cec308cb",
        "cm2.round179.source-g-residual-tube-arrangement-rows.v1",
        180_000_000,
    ),
    "Round182_rows": (
        "cm2_round182_source_g_clipped_graph_and_pair_arrangement_rows.json",
        "ae6e0c38df325e98b01a1d75acfbd8a85a71fda6a118db11d7dff6decf3f847c",
        "9f0f64d93bd0ac2a9dd41965cbfd95531f07582da5eb4c52f14c44da3d0db269",
        "cm2.round182.source-g-clipped-graph-and-pair-arrangement-rows.v1",
        180_000_000,
    ),
    "Round182_certificate": (
        "cm2_round182_source_g_clipped_graph_and_pair_arrangement_certificate.json",
        "27491e3943e88772ec15cee110cd983b14ad82a2a56f8a07d605c3cd8fb49f08",
        "e07da794eed6dbb404de8913f5b871621f9f1b59b355172a37192791ae28911d",
        "cm2.round182.source-g-clipped-graph-and-pair-arrangement.v1",
        1_000_000,
    ),
    "Round208": (
        "cm2_round208_source_g_outgoing_direct_signature_materialization_certificate.json",
        "4d01fb9cee639ec59786c078f7a20b3bbcd5c18ea674fabbfce64e250e765938",
        "d00674fa4061364539ce6f36f6f8de938f50bc54afbf5497266dcfa0e078bca8",
        "cm2.round208.source-g-outgoing-direct-signature-materialization.v1",
        250_000_000,
    ),
    "Round211": (
        "cm2_round211_source_g_outgoing_half_open_owner_materialization_certificate.json",
        "bb03a39a74a237b9f4449214c698795856fce4d6be2195c4f9d7774cd1d4183f",
        "3b831c67669e52f1247ea30c0a1ed7d5c1002931a1c0f621dd934085e87c2d5b",
        "cm2.round211.source-g-outgoing-half-open-owner-materialization.v1",
        180_000_000,
    ),
    "Round216": (
        "cm2_round216_source_g_global_key_occurrence_exhaustion_frontier_certificate.json",
        "fa4cfb3b209518308c61ccdfa95834dd8e6899e6232fc40a569cbab4d6ecbe34",
        "267a4b9aaaab6a576e1c1866cc2fa0b9dc9bf4fc6a3b08a210ed3821e45dd658",
        "cm2.round216.source-g-global-key-occurrence-exhaustion-frontier.v1",
        2_000_000,
    ),
    "Round220": (
        "cm2_round220_source_g_round179_resolved_child_boundary_atlas_certificate.json",
        "569a7849b53805ff4deca0eff9a6938a897942d3d682dfef27c27559135ce974",
        "4d8168cb25bd389f16b332798fcf9b57951deedd8d328bc5a1dac9024508669b",
        "cm2.round220.source-g-round179-resolved-child-boundary-atlas.v1",
        360_000_000,
    ),
    "Round225": (
        "cm2_round225_source_g_certified_connectivity_rebuild_certificate.json",
        "0d040af30906f22f600820e14867c45115e679e33b6ee6f052c51a914cf7d841",
        "0aedfdcc43e45810d97cc0699562a4d1e9faefb0ca3f3e055c84b1ad3ec77512",
        "cm2.round225.source-g-certified-connectivity-rebuild.v1",
        80_000_000,
    ),
    "Round229": (
        "cm2_round229_source_g_global_occurrence_known_block_frontier_certificate.json",
        "c4152f4764ed7fe977046ef728e8257344803433053e06c0ac11ec68b86ff11a",
        "936e140d7113dbdd565f4b1a9381de3b90313e7198266c1950532b80ba153230",
        "cm2.round229.source-g-global-occurrence-known-block-frontier.v1",
        100_000_000,
    ),
}

PROBE_INPUTS = {
    "Round186_probe": (
        "cm2_round186_source_g_factor_face_probe.py",
        "5797b8f4c2ba9c8c5b42b32511f3c97a15469b59bdf00cd8430580c3429c7c64",
        1_000_000,
    ),
    "Round198_probe": (
        "cm2_round198_source_g_outgoing_return_signature_probe.py",
        "59dac5b6e2d79e1612dad51780174f97f71dc1223c01a21b502805d6e9510fbf",
        2_000_000,
    ),
}

RETURN_SIGNATURE_FIELDS = (
    ("chart", "source_chart"),
    ("owner_target", "target_lift"),
    ("ordered_integer_wall_events", "ordered_integer_wall_events"),
    ("signed_wall_word", "signed_wall_word"),
    ("roof", "roof"),
    ("outgoing_cell", "outgoing_cell"),
    ("target_chart", "target_chart"),
    ("official_key_row", "official_key_row"),
    ("official_key_ordinal", "official_key_ordinal"),
    ("official_key_id", "official_key_id"),
)
STRICT_SIGNS = {"STRICT_NEGATIVE", "STRICT_POSITIVE"}

ORACLE_HASHES = {
    "Round220_normal_form_reference_ids_sha256":
        "e72e2c9c7c4b6e55a5e4a6b64d8fd7d98cdd3623e2b19c2e0037f58a33b5b814",
    "Round220_interface_ids_sha256":
        "5f21e8ace887e06af7d039b0d6f6c346a4179ab442b9377b77cfde57382207a1",
    "resolved_child_event_zero_set_ABSENT_ledger_sha256":
        "9e5451b5f808ff80b1bc25dcad1746a78cb8fa7ae3f77483a0fc3e47f2345626",
    "exact_face_candidate_pairs_sha256":
        "e49c1873aeb41d8cd48d4beb5163d7c61954d46e298724e1aff3042e8bf88355",
    "accepted_pairs_sha256":
        "330c0552cd3024980b321cc628f9b2bd5af4aa142acc55d08e9141ec14f41fa7",
    "wrong_side_factor_pairs_sha256":
        "410a6afe4cdbaaecf71c4d402dd5a8d7b3b6d4f30899e6c762a51c7d98b56c6b",
    "remote_full_signature_pairs_sha256":
        "bdb7e2d34b6bc3ef817f9bbbeced8d8d1fb1da27786e3291d247fb759a1cf401",
    "accepted_interface_ids_sha256":
        "ca468ef605c6190d17a8507719a5909ae4da5ef9fe0b07a81e0c2627c72d676c",
    "block_bearing_interface_ids_sha256":
        "59d1c749120af164ea0ee22bc6edc49a0b35efd8bdb35f08bda3c5fa05d61b6e",
    "sheetless_only_interface_ids_sha256":
        "a0db5f6936eb71d195332c92172075c9811386276e101b67ac76e92e63aea43b",
    "reached_known_block_ids_sha256":
        "5f6be28cd44e333c28840a9f25b3eb40181438483233b053390453f4fdd0fc30",
    "mixed_star_sheetless_region_ids_sha256":
        "baedef8374402c872841180b95180ecc55cd56288b16e22926b18b28e827b533",
    "sheetless_only_star_region_ids_sha256":
        "c276a79bbc62623ee6fe839363c3d1cbe3fe75aa22a615503ac49d9bfe1afcf3",
    "derived_resolved_child_ids_sha256":
        "704d3bb48a38a56c73201dfe8cc38bcdd8b285e847b5a94fd0b85671dc1d0a4f",
    "resolved_to_known_block_mapping_sha256":
        "95f70efdb19f36de23d2b520251fcdd37136bad34b9cf68576cfd605d50764a4",
    "sheetless_to_known_block_mapping_sha256":
        "5b7354bd714dbe8879772c7b95718673b91c6457ef097f2a79f237b7b910e1ac",
    "post_Round230_incident_occurrence_ids_sha256":
        "39761020af153c8e05565acfa94950c2934b8689604dc57c2184f7a79d5e88dc",
    "deferred_interface_ids_sha256":
        "840209ba8624cd7b0b0abb2e8291462ee2b88e84bd52a1f98209617e24300ae7",
    "remote_interface_ids_sha256":
        "dd2adc9ddae71f7072c2dc1224cb3b30098d79a3cea088d997e5909c4f41e5ad",
}


class Round230Error(RuntimeError):
    pass


def need(value: bool, label: str) -> None:
    if not value:
        raise Round230Error(label)


ENCODER = json.JSONEncoder(
    sort_keys=True,
    separators=(",", ":"),
    ensure_ascii=False,
    allow_nan=False,
)


def chunks(value: Any) -> Iterable[bytes]:
    for chunk in ENCODER.iterencode(value):
        yield chunk.encode()


def canonical(value: Any) -> bytes:
    return b"".join(chunks(value))


def digest(value: Any) -> str:
    state = hashlib.sha256()
    for chunk in chunks(value):
        state.update(chunk)
    return state.hexdigest()


def closed(value: dict[str, Any]) -> dict[str, Any]:
    row = dict(value)
    row["row_sha256"] = digest(row)
    return row


def ledger(rows: list[dict[str, Any]], id_field: str) -> dict[str, Any]:
    need(len({row[id_field] for row in rows}) == len(rows), f"unique:{id_field}")
    return {
        "row_count": len(rows),
        "rows_sha256": digest(rows),
        "row_ids_sha256": digest([row[id_field] for row in rows]),
        "row_hashes_sha256": digest([row["row_sha256"] for row in rows]),
        "every_row_closed_by_own_SHA256": True,
        "rows": rows,
    }


def zero_credits() -> dict[str, int]:
    return {
        "known_block_membership_assignment_credit": 0,
        "physical_component_credit": 0,
        "maximal_physical_component_credit": 0,
        "global_exact_key_disposition_credit": 0,
    }


def regular_bytes(path: Path, maximum: int) -> bytes:
    before = path.lstat()
    need(
        stat.S_ISREG(before.st_mode)
        and not path.is_symlink()
        and before.st_nlink == 1,
        f"regular:{path.name}",
    )
    need(0 < before.st_size <= maximum, f"bounded:{path.name}")
    descriptor = os.open(
        path,
        os.O_RDONLY
        | getattr(os, "O_NOFOLLOW", 0)
        | getattr(os, "O_CLOEXEC", 0),
    )
    try:
        opened = os.fstat(descriptor)
        need(
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
        pieces: list[bytes] = []
        size = 0
        while True:
            piece = os.read(descriptor, 1024 * 1024)
            if not piece:
                break
            size += len(piece)
            need(size <= maximum, f"bounded-read:{path.name}")
            pieces.append(piece)
        after = os.fstat(descriptor)
        need(
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
        return b"".join(pieces)
    finally:
        os.close(descriptor)


def strict_json(raw: bytes, label: str) -> dict[str, Any]:
    def pairs(items: list[tuple[str, Any]]) -> dict[str, Any]:
        output: dict[str, Any] = {}
        for key, value in items:
            need(key not in output, f"duplicate:{label}:{key}")
            output[key] = value
        return output

    def reject(token: str) -> None:
        raise Round230Error(f"number:{label}:{token}")

    result = json.loads(
        raw,
        object_pairs_hook=pairs,
        parse_float=reject,
        parse_constant=reject,
    )
    need(isinstance(result, dict), f"object:{label}")
    return result


def load(label: str) -> dict[str, Any]:
    name, file_sha, result_sha, schema, maximum = INPUTS[label]
    raw = regular_bytes(HERE / name, maximum)
    need(hashlib.sha256(raw).hexdigest() == file_sha, f"file-pin:{label}")
    envelope = strict_json(raw, label)
    need(set(envelope) == {"result", "result_sha256", "schema"}, f"envelope:{label}")
    need(envelope["schema"] == schema, f"schema:{label}")
    need(envelope["result_sha256"] == result_sha, f"result-pin:{label}")
    need(digest(envelope["result"]) == result_sha, f"result-digest:{label}")
    return envelope["result"]


def pin_probes() -> None:
    for label, (name, expected, maximum) in PROBE_INPUTS.items():
        raw = regular_bytes(HERE / name, maximum)
        need(hashlib.sha256(raw).hexdigest() == expected, f"probe-pin:{label}")


def unpack_table(table: dict[str, Any]) -> list[dict[str, Any]]:
    columns = table["columns"]
    return [dict(zip(columns, row, strict=True)) for row in table["rows"]]


def unpack_attachment(
    document: dict[str, Any],
    table_name: str,
) -> list[dict[str, Any]]:
    columns = document["row_column_schemas"][table_name]
    return [
        dict(zip(columns, row, strict=True))
        for row in document[table_name]
    ]


def exact_positive_area_face(
    resolved_box: list[str],
    retained_leaf_box: list[str],
) -> dict[str, Any] | None:
    need(
        len(resolved_box) == len(retained_leaf_box) == 6,
        "three-dimensional boxes",
    )
    left = [Q(value) for value in resolved_box]
    right = [Q(value) for value in retained_leaf_box]
    touching: list[tuple[int, str, str]] = []
    intersection: list[Q] = []
    for index in range(3):
        left_lo, left_hi = left[2 * index:2 * index + 2]
        right_lo, right_hi = right[2 * index:2 * index + 2]
        overlap_lo = max(left_lo, right_lo)
        overlap_hi = min(left_hi, right_hi)
        if overlap_hi < overlap_lo:
            return None
        if overlap_hi == overlap_lo:
            if left_hi == right_lo:
                touching.append((index, "UPPER", "LOWER"))
            elif right_hi == left_lo:
                touching.append((index, "LOWER", "UPPER"))
            else:
                return None
        intersection.extend((overlap_lo, overlap_hi))
    if len(touching) != 1:
        return None
    axis_index, resolved_side, retained_side = touching[0]
    lengths = [
        intersection[2 * index + 1] - intersection[2 * index]
        for index in range(3)
    ]
    positive = [length for length in lengths if length > 0]
    if len(positive) != 2:
        return None
    return {
        "axis": "tps"[axis_index],
        "resolved_side": resolved_side,
        "retained_side": retained_side,
        "fixed_coordinate": str(intersection[2 * axis_index]),
        "intersection_box": [str(value) for value in intersection],
        "exact_positive_area": str(positive[0] * positive[1]),
    }


def signature_comparison(
    resolved: dict[str, Any],
    signature: dict[str, Any],
) -> tuple[bool, list[str], dict[str, Any]]:
    need(
        set(signature) == {target for _source, target in RETURN_SIGNATURE_FIELDS},
        "exact ten-field local return signature",
    )
    mismatches: list[str] = []
    normalized: dict[str, Any] = {}
    for source, target in RETURN_SIGNATURE_FIELDS:
        normalized[target] = resolved[source]
        if resolved[source] != signature[target]:
            mismatches.append(target)
    return not mismatches, mismatches, normalized


def interface_area(interface: dict[str, Any]) -> Q:
    box = [Q(value) for value in interface["tangential_half_open_box"]]
    need(len(box) == 4 and box[0] < box[1] and box[2] < box[3], "interface area")
    return (box[1] - box[0]) * (box[3] - box[2])


def build(producer_sha256: str) -> dict[str, Any]:
    pin_probes()

    r182_certificate = load("Round182_certificate")
    attachment182 = r182_certificate["row_attachment"]
    need(
        attachment182["file_sha256"] == INPUTS["Round182_rows"][1]
        and attachment182["result_sha256"] == INPUTS["Round182_rows"][2]
        and attachment182["schema"] == INPUTS["Round182_rows"][3]
        and r182_certificate["global_state"]["promotions_issued"] == 0,
        "Round182 certificate/row binding",
    )
    del r182_certificate

    r216 = load("Round216")
    key_frontier216 = r216["formal_key_occurrence_exhaustion_frontier_ledger"]
    need(key_frontier216["row_count"] == 116, "Round216 key count")
    key_rows216 = {
        row["official_key_ordinal"]: row
        for row in key_frontier216["rows"]
    }
    need(
        len(key_rows216) == 116
        and r216["local_3D_occurrence_census_without_physical_promotion"][
            "local_3D_occurrence_count"
        ] == 53_968,
        "Round216 key frontier",
    )
    del r216

    r220 = load("Round220")
    tables220 = r220["coordinate_boundary_atlas"]["tables"]
    for table_name, expected in (
        ("coordinate_face_rows", 103_152),
        ("coordinate_edge_rows", 206_304),
        ("coordinate_corner_rows", 137_536),
    ):
        table = tables220[table_name]
        need(table["row_count"] == expected, f"Round220:{table_name}:count")
        event_index = table["columns"].index("event_sheet_incidence_count")
        need(
            sum(row[event_index] for row in table["rows"]) == 0,
            f"Round220:{table_name}:zero-event",
        )

    interface_rows220 = unpack_table(tables220["one_step_split_interface_rows"])
    interfaces: dict[str, dict[str, Any]] = {}
    for source in interface_rows220:
        if {
            source["lower_child_kind"],
            source["upper_child_kind"],
        } != {"RESOLVED", "RETAINED"}:
            continue
        if source["lower_child_kind"] == "RESOLVED":
            resolved_id = source["lower_child_row_id"]
            retained_id = source["upper_child_row_id"]
            resolved_side = "UPPER"
            retained_side = "LOWER"
        else:
            resolved_id = source["upper_child_row_id"]
            retained_id = source["lower_child_row_id"]
            resolved_side = "LOWER"
            retained_side = "UPPER"
        need(
            source["resolved_incidence_count"] == 1
            and source["retained_incidence_count"] == 1
            and source["event_trace_materialized_on_interface"] is False
            and source["physical_glue_credit"] == 0
            and source["whole_origin_credit"] == 0
            and source["global_exact_key_disposition_credit"] == 0,
            "Round220 one-step nonpromotion",
        )
        interface_id = source["split_interface_id"]
        interfaces[interface_id] = {
            "Round220_split_interface_id": interface_id,
            "origin_row_id": source["origin_row_id"],
            "parent_id": source["parent_id"],
            "chart": source["chart"],
            "axis": source["axis"],
            "fixed_coordinate": source["fixed_coordinate"],
            "tangential_half_open_box": source["tangential_half_open_box"],
            "resolved_child_row_id": resolved_id,
            "retained_child_row_id": retained_id,
            "resolved_side": resolved_side,
            "retained_side": retained_side,
            "half_open_owner_child_kind": source["half_open_owner_child_kind"],
            "half_open_owner_child_row_id": source["half_open_owner_child_row_id"],
        }
    need(
        len(interfaces) == 8_960
        and len({row["resolved_child_row_id"] for row in interfaces.values()})
        == 8_960
        and len({row["retained_child_row_id"] for row in interfaces.values()})
        == 8_960,
        "Round220 resolved-retained interfaces",
    )
    interface_ids = sorted(interfaces)
    need(
        digest(interface_ids)
        == ORACLE_HASHES["Round220_interface_ids_sha256"],
        "Round220 interface ID oracle",
    )

    resolved_atlas220 = {
        row["source_child_row_id"]: row
        for row in unpack_table(tables220["resolved_child_rows"])
        if row["source_child_row_id"]
        in {item["resolved_child_row_id"] for item in interfaces.values()}
    }
    need(len(resolved_atlas220) == 8_960, "Round220 resolved atlas subset")

    normal_account220 = r220[
        "outgoing_wall_and_seam_normal_form_boundary_account"
    ]
    normal_table220 = normal_account220["tables"][
        "relevant_origin_normal_form_rows"
    ]
    normal_by_origin: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in unpack_table(normal_table220):
        normal_by_origin[row["origin_row_id"]].append(row)

    absent_rows: list[dict[str, Any]] = []
    normal_form_reference_ids: list[str] = []
    for interface_id in interface_ids:
        interface = interfaces[interface_id]
        resolved_atlas = resolved_atlas220[interface["resolved_child_row_id"]]
        references = sorted(
            normal_by_origin[interface["origin_row_id"]],
            key=lambda row: row["normal_form_id"],
        )
        need(
            len(references)
            == resolved_atlas["origin_normal_form_reference_count"]
            and resolved_atlas["event_sheet_incidence_count"] == 0,
            "Round220 resolved-child normal-form account",
        )
        for reference in references:
            normal_form_reference_ids.append(reference["normal_form_id"])
            absent_rows.append(
                closed(
                    {
                        "event_zero_set_absence_row_id":
                            "round230-resolved-event-zero-absence:"
                            + digest([
                                interface_id,
                                reference["normal_form_id"],
                            ]),
                        "Round220_split_interface_id": interface_id,
                        "resolved_child_row_id":
                            interface["resolved_child_row_id"],
                        "Round220_normal_form_id":
                            reference["normal_form_id"],
                        "Round179_source_table": reference["source_table"],
                        "Round179_source_row_id": reference["source_row_id"],
                        "normal_form_kind": reference["normal_form_kind"],
                        "equation": reference["equation"],
                        "origin_face_classification":
                            reference["face_classification"],
                        "origin_dimension_account":
                            reference["dimension_account"],
                        "resolved_child_event_zero_set": "ABSENT",
                        "resolved_child_event_sheet_incidence_count": 0,
                        "absence_certification": (
                            "ROUND220_RESOLVED_CHILD_STRICT_DYNAMIC_"
                            "SIGNATURE_RESTRICTION"
                        ),
                        **zero_credits(),
                    }
                )
            )
    normal_form_reference_ids.sort()
    absent_rows.sort(key=lambda row: row["event_zero_set_absence_row_id"])
    reference_count_distribution = Counter(
            resolved_atlas220[row["resolved_child_row_id"]][
                "origin_normal_form_reference_count"
            ]
            for row in interfaces.values()
        )
    normal_reference_digest = digest(normal_form_reference_ids)
    need(
        len(absent_rows) == 8_976
        and reference_count_distribution == Counter({1: 8_952, 3: 8})
        and normal_reference_digest
        == ORACLE_HASHES["Round220_normal_form_reference_ids_sha256"],
        "Round220 8976 normal-form references:"
        f" rows={len(absent_rows)} distribution={reference_count_distribution}"
        f" digest={normal_reference_digest}",
    )
    del (
        r220,
        tables220,
        interface_rows220,
        resolved_atlas220,
        normal_by_origin,
        normal_account220,
    )
    gc.collect()

    resolved_ids = {
        row["resolved_child_row_id"] for row in interfaces.values()
    }
    retained_ids = {
        row["retained_child_row_id"] for row in interfaces.values()
    }
    r179 = load("Round179_rows")
    resolved179: dict[str, dict[str, Any]] = {}
    for row in unpack_attachment(r179, "resolved_3d_child_rows"):
        if row["row_id"] not in resolved_ids:
            continue
        resolved179[row["row_id"]] = {
            key: row[key]
            for key in (
                "row_id",
                "origin_row_id",
                "parent_id",
                "chart",
                "box",
                "owner_target",
                "ordered_integer_wall_events",
                "signed_wall_word",
                "roof",
                "outgoing_cell",
                "target_chart",
                "official_key_row",
                "official_key_ordinal",
                "official_key_id",
            )
        }
    retained179: dict[str, dict[str, Any]] = {}
    for row in unpack_attachment(r179, "retained_3d_child_rows"):
        if row["row_id"] not in retained_ids:
            continue
        retained179[row["row_id"]] = {
            key: row[key]
            for key in (
                "row_id",
                "origin_row_id",
                "parent_id",
                "chart",
                "box",
                "reason_labels",
            )
        }
    need(
        len(resolved179) == len(retained179) == 8_960,
        "Round179 interface child subset",
    )
    for interface in interfaces.values():
        resolved = resolved179[interface["resolved_child_row_id"]]
        retained = retained179[interface["retained_child_row_id"]]
        need(
            resolved["origin_row_id"] == retained["origin_row_id"]
            == interface["origin_row_id"]
            and resolved["parent_id"] == retained["parent_id"]
            == interface["parent_id"]
            and resolved["chart"] == retained["chart"] == interface["chart"],
            "Round179 sibling/interface lineage",
        )
    del r179
    gc.collect()

    interface_by_retained = {
        row["retained_child_row_id"]: row
        for row in interfaces.values()
    }
    r208 = load("Round208")
    source_regions208 = r208["formal_local_open_3D_signature_ledger"]["rows"]
    need(len(source_regions208) == 36_040, "Round208 region census")
    relevant_regions: dict[str, dict[str, Any]] = {}
    regions_by_interface: dict[str, list[str]] = defaultdict(list)
    for source in source_regions208:
        interface = interface_by_retained.get(source["retained_child_row_id"])
        if interface is None:
            continue
        region_id = source["region_row_id"]
        relevant_regions[region_id] = {
            key: source[key]
            for key in (
                "region_row_id",
                "leaf_row_id",
                "origin_row_id",
                "parent_id",
                "occurrence_row_id",
                "retained_child_row_id",
                "Round182_leaf_box",
                "Round182_leaf_coordinate_volume",
                "F_sign",
                "HPLUS_sign",
                "HMINUS_sign",
                "outgoing_cell",
                "local_return_signature",
                "whole_box_factor_C0",
                "inactive_factor",
                "leaf_classification",
            )
        }
        regions_by_interface[
            interface["Round220_split_interface_id"]
        ].append(region_id)
    need(
        len(relevant_regions) == 1_536
        and len(regions_by_interface) == 460
        and Counter(len(rows) for rows in regions_by_interface.values())
        == Counter({2: 400, 4: 32, 3: 20, 128: 4, 9: 4}),
        "Round208 retained-side materialization subset",
    )
    for rows in regions_by_interface.values():
        rows.sort()
    del r208, source_regions208
    gc.collect()

    relevant_leaf_ids = {
        row["leaf_row_id"] for row in relevant_regions.values()
    }
    relevant_occurrence_ids = {
        row["occurrence_row_id"] for row in relevant_regions.values()
    }
    r182_rows = load("Round182_rows")
    leaves182 = {
        row["row_id"]: row
        for row in unpack_attachment(r182_rows, "collar_leaf_rows")
        if row["row_id"] in relevant_leaf_ids
    }
    occurrences182 = {
        row["Round179_occurrence_row_id"]: row
        for row in unpack_attachment(r182_rows, "collar_occurrence_rows")
        if row["Round179_occurrence_row_id"] in relevant_occurrence_ids
    }
    need(
        set(leaves182) == relevant_leaf_ids
        and set(occurrences182) == relevant_occurrence_ids,
        "Round182 relevant leaf/occurrence subset",
    )
    for region in relevant_regions.values():
        leaf = leaves182[region["leaf_row_id"]]
        occurrence = occurrences182[region["occurrence_row_id"]]
        interface = interface_by_retained[region["retained_child_row_id"]]
        resolved = resolved179[interface["resolved_child_row_id"]]
        need(
            leaf["retained_child_row_id"] == region["retained_child_row_id"]
            and leaf["box"] == region["Round182_leaf_box"]
            and leaf["coordinate_volume"]
            == region["Round182_leaf_coordinate_volume"]
            and occurrence["origin_row_id"] == interface["origin_row_id"]
            and occurrence["parent_id"] == interface["parent_id"]
            and occurrence["chart"] == resolved["chart"]
            and occurrence["owner_target"] == resolved["owner_target"],
            "Round182/Round208/interface exact binding",
        )
    relevant_leaf_count = len(leaves182)
    relevant_occurrence_count = len(occurrences182)
    del r182_rows, leaves182, occurrences182
    gc.collect()

    # Round186 is a frozen read-only probe.  It is imported only after its
    # source bytes have been pinned above; no verifier from this or a future
    # round is imported or executed.
    r186 = importlib.import_module("cm2_round186_source_g_factor_face_probe")
    need(
        Path(r186.__file__).resolve()
        == (HERE / PROBE_INPUTS["Round186_probe"][0]).resolve(),
        "Round186 module identity",
    )
    from flint import ctx

    ctx.prec = 256

    candidate_rows_raw: list[dict[str, Any]] = []
    edge_rows_raw: list[dict[str, Any]] = []
    reject_rows_raw: list[dict[str, Any]] = []
    remote_complementary_region_count = 0
    for region_id in sorted(relevant_regions):
        region = relevant_regions[region_id]
        interface = interface_by_retained[region["retained_child_row_id"]]
        interface_id = interface["Round220_split_interface_id"]
        resolved = resolved179[interface["resolved_child_row_id"]]
        exact_signature, mismatch_fields, normalized_signature = (
            signature_comparison(resolved, region["local_return_signature"])
        )
        face = exact_positive_area_face(
            resolved["box"],
            region["Round182_leaf_box"],
        )
        if face is None:
            if exact_signature:
                reject_rows_raw.append(
                    {
                        "reject_row_id":
                            "round230-local-bulk-bridge-reject:"
                            + digest([interface_id, region_id, "REMOTE"]),
                        "Round220_split_interface_id": interface_id,
                        "resolved_child_row_id":
                            interface["resolved_child_row_id"],
                        "retained_child_row_id":
                            interface["retained_child_row_id"],
                        "Round208_region_row_id": region_id,
                        "Round208_leaf_row_id": region["leaf_row_id"],
                        "reject_classification": (
                            "FULL_SIGNATURE_REMOTE_WITHOUT_EXACT_"
                            "POSITIVE_AREA_FACE_OVERLAP"
                        ),
                        "return_signature_exact_field_count": 10,
                        "return_signature_mismatch_fields": [],
                        "exact_positive_area_face_intersection": False,
                        "intersection_patch": None,
                        "known_block_incidence_bridge_credit": 0,
                        **zero_credits(),
                    }
                )
            else:
                need(
                    mismatch_fields == ["outgoing_cell", "target_chart"],
                    "remote complementary signature mismatch",
                )
                remote_complementary_region_count += 1
            continue

        need(
            face["axis"] == interface["axis"]
            and face["resolved_side"] == interface["resolved_side"]
            and face["retained_side"] == interface["retained_side"]
            and face["fixed_coordinate"] == interface["fixed_coordinate"],
            "exact face equals one-step interface patch",
        )
        box = r186.r179.r174.atlas.AtlasBox(
            *(Q(value) for value in face["intersection_box"]),
            0,
            f"round230-face:{digest([interface_id, region_id])}",
        )
        factor_geometry = r186.factor_geometry(
            resolved["chart"],
            resolved["owner_target"],
            box,
        )
        patch_signs = {
            kind: r186.r179.arb_sign(factor_geometry[kind][0])
            for kind in ("HPLUS", "HMINUS")
        }
        need(
            set(patch_signs.values()) <= STRICT_SIGNS
            and len(patch_signs) == 2,
            "Round186 strict whole-patch factor signs",
        )
        factor_signs_equal = (
            patch_signs["HPLUS"] == region["HPLUS_sign"]
            and patch_signs["HMINUS"] == region["HMINUS_sign"]
        )
        accepted = exact_signature and factor_signs_equal
        candidate_id = (
            "round230-exact-face-candidate:"
            + digest([interface_id, region_id, face["intersection_box"]])
        )
        candidate_rows_raw.append(
            {
                "face_candidate_row_id": candidate_id,
                "Round220_split_interface_id": interface_id,
                "resolved_child_row_id":
                    interface["resolved_child_row_id"],
                "retained_child_row_id":
                    interface["retained_child_row_id"],
                "Round208_region_row_id": region_id,
                "Round208_leaf_row_id": region["leaf_row_id"],
                "axis": face["axis"],
                "resolved_side": face["resolved_side"],
                "retained_side": face["retained_side"],
                "fixed_coordinate": face["fixed_coordinate"],
                "exact_intersection_box": face["intersection_box"],
                "exact_positive_area": face["exact_positive_area"],
                "return_signature_field_count": 10,
                "return_signature_exact_equality": exact_signature,
                "return_signature_mismatch_fields": mismatch_fields,
                "Round186_HPLUS_whole_patch_sign":
                    patch_signs["HPLUS"],
                "Round186_HMINUS_whole_patch_sign":
                    patch_signs["HMINUS"],
                "Round208_HPLUS_region_sign":
                    region["HPLUS_sign"],
                "Round208_HMINUS_region_sign":
                    region["HMINUS_sign"],
                "strict_factor_signs_equal_on_whole_patch":
                    factor_signs_equal,
                "candidate_disposition": (
                    "CERTIFIED_LOCAL_BULK_BRIDGE"
                    if accepted
                    else "WRONG_SIDE_FACTOR_INCOMPATIBLE_REJECT"
                ),
                **zero_credits(),
            }
        )
        if accepted:
            edge_rows_raw.append(
                {
                    "certified_local_bulk_bridge_edge_id":
                        "round230-certified-local-bulk-bridge:"
                        + digest([
                            interface_id,
                            region_id,
                            face["intersection_box"],
                        ]),
                    "face_candidate_row_id": candidate_id,
                    "Round220_split_interface_id": interface_id,
                    "resolved_child_row_id":
                        interface["resolved_child_row_id"],
                    "retained_child_row_id":
                        interface["retained_child_row_id"],
                    "Round208_region_row_id": region_id,
                    "Round208_leaf_row_id": region["leaf_row_id"],
                    "axis": face["axis"],
                    "resolved_side": face["resolved_side"],
                    "retained_side": face["retained_side"],
                    "fixed_coordinate": face["fixed_coordinate"],
                    "exact_intersection_box":
                        face["intersection_box"],
                    "exact_positive_area": face["exact_positive_area"],
                    "return_signature_field_names": [
                        target for _source, target in RETURN_SIGNATURE_FIELDS
                    ],
                    "return_signature_field_count": 10,
                    "resolved_return_signature_sha256":
                        digest(normalized_signature),
                    "Round208_return_signature_sha256":
                        digest(region["local_return_signature"]),
                    "all_10_return_signature_fields_exactly_equal": True,
                    "Round186_HPLUS_whole_patch_sign":
                        patch_signs["HPLUS"],
                    "Round186_HMINUS_whole_patch_sign":
                        patch_signs["HMINUS"],
                    "Round208_HPLUS_region_sign":
                        region["HPLUS_sign"],
                    "Round208_HMINUS_region_sign":
                        region["HMINUS_sign"],
                    "both_factor_signs_strict_and_equal_on_whole_patch":
                        True,
                    "resolved_child_event_zero_sets_absent": True,
                    "classification": (
                        "NON_EVENT_STRICT_POSITIVE_AREA_LOCAL_BULK_"
                        "CONTINUATION_PATCH"
                    ),
                    "whole_interface_certified": False,
                    "known_block_incidence_bridge_credit": 1,
                    **zero_credits(),
                }
            )
        else:
            need(
                mismatch_fields == ["outgoing_cell", "target_chart"]
                and not factor_signs_equal,
                "wrong-side/factor reject exact mismatch",
            )
            reject_rows_raw.append(
                {
                    "reject_row_id":
                        "round230-local-bulk-bridge-reject:"
                        + digest([interface_id, region_id, "WRONG_FACTOR"]),
                    "Round220_split_interface_id": interface_id,
                    "resolved_child_row_id":
                        interface["resolved_child_row_id"],
                    "retained_child_row_id":
                        interface["retained_child_row_id"],
                    "Round208_region_row_id": region_id,
                    "Round208_leaf_row_id": region["leaf_row_id"],
                    "reject_classification":
                        "WRONG_SIDE_FACTOR_INCOMPATIBLE",
                    "return_signature_exact_field_count": 8,
                    "return_signature_mismatch_fields":
                        mismatch_fields,
                    "exact_positive_area_face_intersection": True,
                    "intersection_patch": face,
                    "Round186_HPLUS_whole_patch_sign":
                        patch_signs["HPLUS"],
                    "Round186_HMINUS_whole_patch_sign":
                        patch_signs["HMINUS"],
                    "Round208_HPLUS_region_sign":
                        region["HPLUS_sign"],
                    "Round208_HMINUS_region_sign":
                        region["HMINUS_sign"],
                    "known_block_incidence_bridge_credit": 0,
                    **zero_credits(),
                }
            )

    need(
        len(candidate_rows_raw) == 1_512
        and len(edge_rows_raw) == 784
        and Counter(row["axis"] for row in edge_rows_raw)
        == Counter({"t": 400, "p": 384})
        and Counter(
            row["reject_classification"] for row in reject_rows_raw
        ) == Counter({
            "WRONG_SIDE_FACTOR_INCOMPATIBLE": 728,
            "FULL_SIGNATURE_REMOTE_WITHOUT_EXACT_POSITIVE_AREA_FACE_OVERLAP": 12,
        })
        and remote_complementary_region_count == 12,
        "Round230 candidate/edge/reject census",
    )

    r211 = load("Round211")
    sheets211 = r211["formal_2D_sheet_owner_ledger"]["rows"]
    need(len(sheets211) == 17_716, "Round211 sheet count")
    region_to_sheet: dict[str, str] = {}
    sheet_rows211: dict[str, dict[str, Any]] = {}
    for sheet in sheets211:
        sheet_id = sheet["sheet_row_id"]
        need(sheet_id not in sheet_rows211, "Round211 unique sheet ID")
        sheet_rows211[sheet_id] = sheet
        for region_id in (
            sheet["owner_region_row_id"],
            sheet["shadow_region_row_id"],
        ):
            need(region_id not in region_to_sheet, "Round211 region partition")
            region_to_sheet[region_id] = sheet_id
    need(
        len(region_to_sheet) == 35_432,
        "Round211 exact two-sides-per-sheet partition",
    )
    del r211, sheets211
    gc.collect()

    r225 = load("Round225")
    assignments225 = r225["formal_Round211_sheet_assignment_ledger"]["rows"]
    blocks225 = r225["formal_certified_known_connectivity_block_ledger"]["rows"]
    need(
        len(assignments225) == 17_716
        and len(blocks225) == 7_404,
        "Round225 assignment/block census",
    )
    sheet_to_block: dict[str, str] = {}
    for assignment in assignments225:
        sheet_id = assignment["Round211_sheet_row_id"]
        need(
            sheet_id in sheet_rows211 and sheet_id not in sheet_to_block,
            "Round225 sheet assignment partition",
        )
        sheet_to_block[sheet_id] = assignment["known_connectivity_block_id"]
    block_ids225 = {
        row["known_connectivity_block_id"] for row in blocks225
    }
    need(
        set(sheet_to_block) == set(sheet_rows211)
        and set(sheet_to_block.values()) == block_ids225
        and r225["rebuilt_frontier_audit"][
            "remaining_missing_contact_frontier_count"
        ] == 0,
        "Round225 frozen known-block incidence",
    )
    del r225, assignments225, blocks225
    gc.collect()

    for row in candidate_rows_raw:
        sheet_id = region_to_sheet.get(row["Round208_region_row_id"])
        row["Round211_sheet_row_id"] = sheet_id
        row["Round225_known_block_id"] = (
            None if sheet_id is None else sheet_to_block[sheet_id]
        )
    for row in edge_rows_raw:
        sheet_id = region_to_sheet.get(row["Round208_region_row_id"])
        row["Round211_sheet_row_id"] = sheet_id
        row["Round225_known_block_id"] = (
            None if sheet_id is None else sheet_to_block[sheet_id]
        )
        row["retained_region_seed_known_block_incidence"] = (
            sheet_id is not None
        )
    for row in reject_rows_raw:
        sheet_id = region_to_sheet.get(row["Round208_region_row_id"])
        row["Round211_sheet_row_id"] = sheet_id
        row["Round225_known_block_id"] = (
            None if sheet_id is None else sheet_to_block[sheet_id]
        )

    # A bridge star is the complete accepted positive-area patch family on
    # one resolved side.  Direct sheet incidence may seed at most one frozen
    # Round225 block in a star.  That block is propagated only to the resolved
    # child and to sheetless accepted regions in the same certified star.
    edges_by_resolved: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in edge_rows_raw:
        edges_by_resolved[row["resolved_child_row_id"]].append(row)
    need(len(edges_by_resolved) == 448, "Round230 bridge-star count")

    star_rows: list[dict[str, Any]] = []
    incidence_delta_rows: list[dict[str, Any]] = []
    resolved_to_block: dict[str, str] = {}
    sheetless_to_block: dict[str, str] = {}
    coverage_distribution: Counter[tuple[str, str]] = Counter()
    reached_blocks: set[str] = set()
    mixed_sheetless_region_ids: list[str] = []
    sheetless_only_region_ids: list[str] = []
    for resolved_id in sorted(edges_by_resolved):
        edges = sorted(
            edges_by_resolved[resolved_id],
            key=lambda row: row["certified_local_bulk_bridge_edge_id"],
        )
        interface_id = edges[0]["Round220_split_interface_id"]
        interface = interfaces[interface_id]
        need(
            all(row["Round220_split_interface_id"] == interface_id for row in edges),
            "one interface per resolved bridge star",
        )
        block_ids = sorted({
            row["Round225_known_block_id"]
            for row in edges
            if row["Round225_known_block_id"] is not None
        })
        need(len(block_ids) <= 1, "unique known-block seed per star")
        block_id = block_ids[0] if block_ids else None
        accepted_area = sum((Q(row["exact_positive_area"]) for row in edges), Q(0))
        total_area = interface_area(interface)
        need(Q(0) < accepted_area <= total_area, "positive bounded star area")
        ratio = str(accepted_area / total_area)
        coverage_distribution[(interface["axis"], ratio)] += 1
        sheetless_edges = [
            row for row in edges if row["Round211_sheet_row_id"] is None
        ]
        if block_id is not None:
            reached_blocks.add(block_id)
            resolved_to_block[resolved_id] = block_id
            resolved = resolved179[resolved_id]
            incidence_delta_rows.append(
                closed({
                    "incidence_delta_row_id":
                        "round230-known-block-incidence-delta:"
                        + digest([resolved_id, block_id, "RESOLVED"]),
                    "local_occurrence_row_id": resolved_id,
                    "local_occurrence_gauge": "ROUND179_RESOLVED_CHILD",
                    "official_key_ordinal": resolved["official_key_ordinal"],
                    "official_key_id": resolved["official_key_id"],
                    "Round225_known_connectivity_block_id": block_id,
                    "derivation": (
                        "CERTIFIED_LOCAL_BULK_BRIDGE_TO_DIRECT_"
                        "SHEET_INCIDENCE"
                    ),
                    "known_block_incidence_attachment_credit": 1,
                    **zero_credits(),
                })
            )
            for edge in sheetless_edges:
                region_id = edge["Round208_region_row_id"]
                region = relevant_regions[region_id]
                signature = region["local_return_signature"]
                need(
                    region_id not in sheetless_to_block
                    and signature["official_key_ordinal"]
                    == resolved["official_key_ordinal"]
                    and signature["official_key_id"] == resolved["official_key_id"],
                    "sheetless propagation exact key identity",
                )
                sheetless_to_block[region_id] = block_id
                mixed_sheetless_region_ids.append(region_id)
                incidence_delta_rows.append(
                    closed({
                        "incidence_delta_row_id":
                            "round230-known-block-incidence-delta:"
                            + digest([region_id, block_id, "SHEETLESS"]),
                        "local_occurrence_row_id": region_id,
                        "local_occurrence_gauge": "ROUND208_STRICT_OPEN_REGION",
                        "official_key_ordinal": signature["official_key_ordinal"],
                        "official_key_id": signature["official_key_id"],
                        "Round225_known_connectivity_block_id": block_id,
                        "derivation": (
                            "CERTIFIED_LOCAL_BULK_BRIDGE_STAR_PROPAGATION"
                        ),
                        "known_block_incidence_attachment_credit": 1,
                        **zero_credits(),
                    })
                )
        else:
            sheetless_only_region_ids.extend(
                row["Round208_region_row_id"] for row in sheetless_edges
            )

        star_rows.append(
            closed({
                "bridge_star_row_id":
                    "round230-certified-local-bulk-bridge-star:"
                    + digest([resolved_id, interface_id]),
                "Round220_split_interface_id": interface_id,
                "resolved_child_row_id": resolved_id,
                "retained_child_row_id": interface["retained_child_row_id"],
                "axis": interface["axis"],
                "accepted_patch_count": len(edges),
                "accepted_patch_ids_sha256": digest([
                    row["certified_local_bulk_bridge_edge_id"] for row in edges
                ]),
                "direct_sheet_incident_patch_count":
                    len(edges) - len(sheetless_edges),
                "sheetless_patch_count": len(sheetless_edges),
                "accepted_patch_exact_area": str(accepted_area),
                "interface_tangential_exact_area": str(total_area),
                "accepted_patch_coverage_ratio": ratio,
                "Round225_known_connectivity_block_id": block_id,
                "resolved_known_block_incidence_propagated": block_id is not None,
                "sheetless_region_known_block_incidence_propagated_count":
                    len(sheetless_edges) if block_id is not None else 0,
                "whole_interface_certified": accepted_area == total_area,
                **zero_credits(),
            })
        )

    need(
        coverage_distribution == Counter({
            ("t", "1/64"): 276,
            ("t", "1/32"): 44,
            ("t", "9/64"): 4,
            ("p", "1/64"): 112,
            ("p", "1/32"): 8,
            ("p", "1"): 4,
        })
        and len(resolved_to_block) == 444
        and len(sheetless_to_block) == 20
        and len(incidence_delta_rows) == 464
        and len(reached_blocks) == 440,
        "Round230 bridge-star propagation census:"
        f" coverage={coverage_distribution} resolved={len(resolved_to_block)}"
        f" sheetless={len(sheetless_to_block)} delta={len(incidence_delta_rows)}"
        f" reached_blocks={len(reached_blocks)}",
    )

    candidate_rows = [
        closed(row) for row in sorted(
            candidate_rows_raw, key=lambda row: row["face_candidate_row_id"]
        )
    ]
    edge_rows = [
        closed(row) for row in sorted(
            edge_rows_raw,
            key=lambda row: row["certified_local_bulk_bridge_edge_id"],
        )
    ]
    reject_rows = [
        closed(row) for row in sorted(
            reject_rows_raw, key=lambda row: row["reject_row_id"]
        )
    ]
    star_rows.sort(key=lambda row: row["bridge_star_row_id"])
    incidence_delta_rows.sort(key=lambda row: row["incidence_delta_row_id"])

    candidate_pairs = sorted([
        [row["Round220_split_interface_id"], row["Round208_region_row_id"]]
        for row in candidate_rows
    ])
    accepted_pairs = sorted([
        [row["Round220_split_interface_id"], row["Round208_region_row_id"]]
        for row in edge_rows
    ])
    wrong_pairs = sorted([
        [row["Round220_split_interface_id"], row["Round208_region_row_id"]]
        for row in reject_rows
        if row["reject_classification"] == "WRONG_SIDE_FACTOR_INCOMPATIBLE"
    ])
    remote_pairs = sorted([
        [row["Round220_split_interface_id"], row["Round208_region_row_id"]]
        for row in reject_rows
        if row["reject_classification"].startswith("FULL_SIGNATURE_REMOTE")
    ])
    accepted_interface_ids = sorted({
        row["Round220_split_interface_id"] for row in edge_rows
    })
    block_interface_ids = sorted({
        row["Round220_split_interface_id"]
        for row in edge_rows if row["Round225_known_block_id"] is not None
    })
    sheetless_only_interface_ids = sorted(
        set(accepted_interface_ids) - set(block_interface_ids)
    )
    deferred_interface_ids = sorted(set(interface_ids) - set(accepted_interface_ids))
    remote_interface_ids = sorted({pair[0] for pair in remote_pairs})
    oracle_values = {
        "exact_face_candidate_pairs_sha256": digest(candidate_pairs),
        "accepted_pairs_sha256": digest(accepted_pairs),
        "wrong_side_factor_pairs_sha256": digest(wrong_pairs),
        "remote_full_signature_pairs_sha256": digest(remote_pairs),
        "accepted_interface_ids_sha256": digest(accepted_interface_ids),
        "block_bearing_interface_ids_sha256": digest(block_interface_ids),
        "sheetless_only_interface_ids_sha256": digest(sheetless_only_interface_ids),
        "reached_known_block_ids_sha256": digest(sorted(reached_blocks)),
        "mixed_star_sheetless_region_ids_sha256":
            digest(sorted(mixed_sheetless_region_ids)),
        "sheetless_only_star_region_ids_sha256":
            digest(sorted(sheetless_only_region_ids)),
        "derived_resolved_child_ids_sha256": digest(sorted(resolved_to_block)),
        "resolved_to_known_block_mapping_sha256":
            digest(sorted(resolved_to_block.items())),
        "sheetless_to_known_block_mapping_sha256":
            digest(sorted(sheetless_to_block.items())),
        "deferred_interface_ids_sha256": digest(deferred_interface_ids),
        "remote_interface_ids_sha256": digest(remote_interface_ids),
    }
    oracle_mismatches = {
        label: {"expected": ORACLE_HASHES[label], "actual": actual}
        for label, actual in oracle_values.items()
        if actual != ORACLE_HASHES[label]
    }
    need(not oracle_mismatches, f"oracle mismatches:{oracle_mismatches}")
    absent_rows_digest = digest(absent_rows)
    need(
        absent_rows_digest
        == ORACLE_HASHES["resolved_child_event_zero_set_ABSENT_ledger_sha256"],
        "oracle:resolved event-zero absence rows:"
        f"{absent_rows_digest}",
    )

    r229 = load("Round229")
    occurrence_rows229 = r229[
        "formal_occurrence_known_block_attachment_frontier_ledger"
    ]["rows"]
    occurrence229 = {
        row["local_occurrence_row_id"]: row for row in occurrence_rows229
    }
    need(len(occurrence229) == 53_968, "Round229 occurrence partition")
    delta_map = {
        row["local_occurrence_row_id"]:
            row["Round225_known_connectivity_block_id"]
        for row in incidence_delta_rows
    }
    need(len(delta_map) == 464, "unique Round230 incidence delta")
    post_rows: list[dict[str, Any]] = []
    post_incident_ids: list[str] = []
    per_key_post: dict[int, Counter[str]] = defaultdict(Counter)
    for occurrence_id in sorted(occurrence229):
        old = occurrence229[occurrence_id]
        old_block = old["Round225_known_connectivity_block_id"]
        new_block = delta_map.get(occurrence_id)
        need(not (old_block is not None and new_block is not None), "delta is new")
        block_id = old_block if old_block is not None else new_block
        attached = block_id is not None
        if attached:
            post_incident_ids.append(occurrence_id)
        counter = per_key_post[old["official_key_ordinal"]]
        counter["total"] += 1
        counter["attached" if attached else "unattached"] += 1
        counter["new" if new_block is not None else "inherited"] += 1
        post_rows.append(
            closed({
                "post_frontier_row_id":
                    "round230-post-known-block-frontier:"
                    + digest([occurrence_id, block_id]),
                "local_occurrence_row_id": occurrence_id,
                "local_occurrence_gauge": old["local_occurrence_gauge"],
                "official_key_ordinal": old["official_key_ordinal"],
                "official_key_id": old["official_key_id"],
                "Round225_known_connectivity_block_id": block_id,
                "incidence_source": (
                    "ROUND230_CERTIFIED_LOCAL_BULK_BRIDGE"
                    if new_block is not None else
                    "ROUND229_INHERITED_DIRECT_SHEET_INCIDENCE"
                    if old_block is not None else "NONE"
                ),
                "known_block_incidence_attachment_credit": int(attached),
                "known_block_membership_assignment_credit": 0,
                "maximal_physical_component_assignment_credit": 0,
                "global_exact_key_fibre_exhausted": False,
                "global_exact_key_disposition_credit": 0,
            })
        )
    need(
        len(post_incident_ids) == 35_896
        and len(post_rows) - len(post_incident_ids) == 18_072
        and digest(post_incident_ids)
        == ORACLE_HASHES["post_Round230_incident_occurrence_ids_sha256"],
        "post-Round230 occurrence incidence census",
    )

    per_key_rows: list[dict[str, Any]] = []
    for ordinal in sorted(key_rows216):
        old = key_rows216[ordinal]
        counts = per_key_post[ordinal]
        need(counts["total"] == old["local_3D_occurrence_count"], "per-key total")
        per_key_rows.append(
            closed({
                "key_frontier_row_id":
                    f"round230-key-frontier:{ordinal:06d}:{digest(old['official_key_id'])}",
                "official_key_ordinal": ordinal,
                "official_key_id": old["official_key_id"],
                "official_key_row": old["official_key_row"],
                "local_occurrence_count": counts["total"],
                "occurrences_with_known_block_incidence": counts["attached"],
                "occurrences_without_known_block_incidence": counts["unattached"],
                "new_Round230_known_block_incidences": counts["new"],
                "global_exact_key_fibre_exhausted": False,
                "maximal_physical_component_assignment_count": 0,
                "global_exact_key_disposition_credit": 0,
            })
        )
    need(len(per_key_rows) == 116, "Round230 per-key frontier")

    return {
        "status": STATUS,
        "census": {
            "resolved_retained_interface_count": 8_960,
            "interface_event_zero_set_absent_count": 8_960,
            "normal_form_absence_reference_count": 8_976,
            "Round208_retained_side_materialized_interface_count": 460,
            "Round208_relevant_region_count": 1_536,
            "Round182_relevant_leaf_count": relevant_leaf_count,
            "Round182_relevant_occurrence_count": relevant_occurrence_count,
            "exact_face_overlap_region_candidate_count": 1_512,
            "accepted_local_bulk_continuation_edge_count": 784,
            "accepted_t_edge_count": 400,
            "accepted_p_edge_count": 384,
            "rejected_wrong_side_edge_count": 728,
            "remote_exact_signature_region_reference_count": 12,
            "bridge_star_count": 448,
            "block_backed_bridge_star_count": 444,
            "sheetless_only_bridge_star_count": 4,
            "direct_sheet_incident_accepted_edge_count": 728,
            "sheetless_accepted_edge_count": 56,
            "new_resolved_known_block_incidence_count": 444,
            "new_sheetless_region_known_block_incidence_count": 20,
            "derived_occurrence_known_block_incidence_delta_count": 464,
            "post_bridge_occurrences_with_known_block_incidence": 35_896,
            "post_bridge_occurrences_without_known_block_incidence": 18_072,
            "known_connectivity_block_count": 7_404,
            "maximal_physical_component_assignment_count": 0,
            "global_exact_key_fibre_exhausted_count": 0,
        },
        "formal_resolved_child_event_zero_set_absence_ledger":
            ledger(absent_rows, "event_zero_set_absence_row_id"),
        "formal_exact_face_candidate_ledger":
            ledger(candidate_rows, "face_candidate_row_id"),
        "formal_certified_local_bulk_continuation_edge_ledger":
            ledger(edge_rows, "certified_local_bulk_bridge_edge_id"),
        "formal_rejected_local_bulk_candidate_ledger":
            ledger(reject_rows, "reject_row_id"),
        "formal_certified_local_bulk_bridge_star_ledger":
            ledger(star_rows, "bridge_star_row_id"),
        "formal_occurrence_known_block_incidence_delta_ledger":
            ledger(incidence_delta_rows, "incidence_delta_row_id"),
        "formal_post_Round230_occurrence_known_block_frontier_ledger":
            ledger(post_rows, "post_frontier_row_id"),
        "formal_post_Round230_key_frontier_ledger":
            ledger(per_key_rows, "key_frontier_row_id"),
        "coverage_distribution": [
            {"axis": axis, "coverage_ratio": ratio, "bridge_star_count": count}
            for (axis, ratio), count in sorted(coverage_distribution.items())
        ],
        "frozen_oracles": {**ORACLE_HASHES, **oracle_values},
        "scope_contract": {
            "accepted_edges_are_strict_positive_area_local_bulk_patches": True,
            "resolved_child_event_zero_sets_absent": True,
            "whole_interface_certified_only_when_coverage_ratio_is_one": True,
            "known_block_incidence_is_not_membership": True,
            "known_blocks_are_not_claimed_maximal_physical_components": True,
            "all_retained_event_strata_exhausted": False,
            "global_exact_key_fibres_exhausted": False,
        },
        "strict_nonpromotion": {
            "known_block_membership_assignment_credit": 0,
            "maximal_physical_component_credit": 0,
            "global_exact_key_fibre_exhausted_count": 0,
            "global_exact_key_disposition_credit": 0,
            "source_G_global_exact_key_dispositions": "0/224580",
            "D02": "BLOCKED",
            "global_Gate5_fields": "10/18",
            "global_complete_18_field_blocks": 0,
            "CM2": "NO-GO_FOR_CLAIM",
        },
        "required_next": (
            "exhaust the 18072 still-unattached occurrences by materializing "
            "deeper retained event strata and non-coordinate contact channels; "
            "then prove maximal-component completeness and independently rebuild "
            "all 116 exact-key fibres"
        ),
        "provenance": {
            "schema": SCHEMA,
            "producer_sha256": producer_sha256,
            "python_version": sys.version.split()[0],
            "python_flint_version": getattr(r186, "__version__", "dependency-pinned"),
        },
    }


def safe_write(data: bytes) -> None:
    descriptor, name = tempfile.mkstemp(
        prefix=f".{OUTPUT.name}.", suffix=".tmp", dir=HERE
    )
    temporary = Path(name)
    try:
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, OUTPUT)
    finally:
        if temporary.exists():
            temporary.unlink()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--no-write", action="store_true")
    args = parser.parse_args()
    producer_sha = hashlib.sha256(
        regular_bytes(Path(__file__), 5_000_000)
    ).hexdigest()
    result = build(producer_sha)
    envelope = {"schema": SCHEMA, "result": result, "result_sha256": digest(result)}
    encoded = canonical(envelope) + b"\n"
    if not args.no_write:
        safe_write(encoded)
    print(result["status"])
    print(f"producer_sha256={producer_sha}")
    print(f"result_sha256={envelope['result_sha256']}")
    print(f"certificate_sha256={hashlib.sha256(encoded).hexdigest()}")
    print("interfaces=8960 accepted_edges=784 bridge_stars=448")
    print("incidence_delta=464 post_incident=35896 post_unattached=18072")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
