#!/usr/bin/env python3
"""Independent verifier for the Round230 resolved/retained bulk bridges.

This verifier never imports or executes the Round230 producer.  Its semantic
model is rebuilt from the frozen Round179, Round208, Round211, Round220,
Round225, and Round229 data, with the Round186 interval factor kernel used
only for whole-face HPLUS/HMINUS evaluation.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import copy
import gc
from fractions import Fraction as Q
import hashlib
import importlib
import json
import os
from pathlib import Path
import stat
import sys
import tempfile
from typing import Any


HERE = Path(__file__).resolve().parent
SCHEMA = "cm2.round230.source-g-resolved-retained-bulk-continuation.v1"
CANDIDATE_NAME = (
    "cm2_round230_source_g_resolved_retained_bulk_continuation_certificate.json"
)
OUTPUT_NAME = (
    "cm2_round230_source_g_resolved_retained_bulk_continuation_verification.json"
)
MAX_JSON_BYTES = 384 * 1024 * 1024
STRICT_SIGNS = {"STRICT_NEGATIVE", "STRICT_POSITIVE"}

INPUTS = {
    "Round179_rows": (
        "cm2_round179_source_g_residual_tube_arrangement_rows.json",
        "f20b42c1fed781779b537b4d45bf44233eae1ed3ee620b95177a80f0eb2b5e42",
        "cm2.round179.source-g-residual-tube-arrangement-rows.v1",
        "a5468800c1d89cd307a5a26c608550b04db79c64c562fb12bedb22d6cec308cb",
    ),
    "Round208": (
        "cm2_round208_source_g_outgoing_direct_signature_materialization_certificate.json",
        "4d01fb9cee639ec59786c078f7a20b3bbcd5c18ea674fabbfce64e250e765938",
        "cm2.round208.source-g-outgoing-direct-signature-materialization.v1",
        "d00674fa4061364539ce6f36f6f8de938f50bc54afbf5497266dcfa0e078bca8",
    ),
    "Round211": (
        "cm2_round211_source_g_outgoing_half_open_owner_materialization_certificate.json",
        "bb03a39a74a237b9f4449214c698795856fce4d6be2195c4f9d7774cd1d4183f",
        "cm2.round211.source-g-outgoing-half-open-owner-materialization.v1",
        "3b831c67669e52f1247ea30c0a1ed7d5c1002931a1c0f621dd934085e87c2d5b",
    ),
    "Round220": (
        "cm2_round220_source_g_round179_resolved_child_boundary_atlas_certificate.json",
        "569a7849b53805ff4deca0eff9a6938a897942d3d682dfef27c27559135ce974",
        "cm2.round220.source-g-round179-resolved-child-boundary-atlas.v1",
        "4d8168cb25bd389f16b332798fcf9b57951deedd8d328bc5a1dac9024508669b",
    ),
    "Round225": (
        "cm2_round225_source_g_certified_connectivity_rebuild_certificate.json",
        "0d040af30906f22f600820e14867c45115e679e33b6ee6f052c51a914cf7d841",
        "cm2.round225.source-g-certified-connectivity-rebuild.v1",
        "0aedfdcc43e45810d97cc0699562a4d1e9faefb0ca3f3e055c84b1ad3ec77512",
    ),
    "Round229": (
        "cm2_round229_source_g_global_occurrence_known_block_frontier_certificate.json",
        "c4152f4764ed7fe977046ef728e8257344803433053e06c0ac11ec68b86ff11a",
        "cm2.round229.source-g-global-occurrence-known-block-frontier.v1",
        "936e140d7113dbdd565f4b1a9381de3b90313e7198266c1950532b80ba153230",
    ),
}

ROUND186_SOURCE = "cm2_round186_source_g_factor_face_probe.py"
ROUND186_SOURCE_SHA256 = (
    "5797b8f4c2ba9c8c5b42b32511f3c97a15469b59bdf00cd8430580c3429c7c64"
)
FACTOR_DEPENDENCY_PINS = {
    "cm2_round182_source_g_clipped_graph_and_pair_arrangement.py":
        "8638f2722e68bd5c6e0eb5932dc76780728998f21a47b1d8c02c28449e984d56",
    "cm2_round179_source_g_residual_tube_arrangement_verifier.py":
        "292719cedfb4d5b802bf87a48314b5237f7b4438e4615d124d716f497044e679",
    "cm2_round174_source_g_unique_first_dynamic_occurrence_materialization_verifier.py":
        "c7ead7c9cb8b4d7b8680e64bfb7870e5c5f5e39277e7c7d3d08a62b600f5c058",
    "cm2_gate3_candidate_first_hit_cert.py":
        "6d224d74cda186a40ef9956d1dd6556d5a7b9f506d47c942427ceb66fd705bd2",
    "cm2_gate3_eight_cell_symmetry_atlas_cert.py":
        "d867f5cb03691289033d1a0d0e277a03e8395d70aae7e0689446d7aa63eac3da",
}


class VerificationError(RuntimeError):
    """Fail-closed verification exception."""


def need(condition: bool, label: str) -> None:
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


def regular_bytes(path: Path, maximum: int) -> bytes:
    """Read one stable regular file without following links."""

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


def check_plain_file(path: Path, expected_name: str, max_bytes: int) -> bytes:
    need(path.parent.resolve() == HERE, f"parent:{expected_name}")
    need(path.name == expected_name, f"name:{expected_name}")
    return regular_bytes(path, max_bytes)


def reject_duplicate(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise VerificationError(f"duplicate JSON key:{key}")
        result[key] = value
    return result


def validate_json_tree(value: Any) -> None:
    if value is None or isinstance(value, (bool, int)):
        return
    if isinstance(value, float):
        raise VerificationError("JSON float forbidden")
    if isinstance(value, str):
        if any(0xD800 <= ord(char) <= 0xDFFF for char in value):
            raise VerificationError("JSON surrogate forbidden")
        return
    if isinstance(value, list):
        for item in value:
            validate_json_tree(item)
        return
    if isinstance(value, dict):
        for key, item in value.items():
            need(isinstance(key, str), "JSON object key")
            validate_json_tree(item)
        return
    raise VerificationError("unsupported JSON value")


def strict_json_bytes(raw: bytes, label: str) -> dict[str, Any]:
    need(raw.endswith(b"\n"), f"final newline:{label}")
    need(not raw.startswith(b"\xef\xbb\xbf"), f"BOM:{label}")
    need(b"\x00" not in raw, f"NUL:{label}")
    try:
        text = raw.decode("utf-8", errors="strict")
        value = json.loads(
            text,
            object_pairs_hook=reject_duplicate,
            parse_float=lambda _text: (_ for _ in ()).throw(
                VerificationError("JSON float forbidden")
            ),
            parse_constant=lambda _text: (_ for _ in ()).throw(
                VerificationError("JSON nonfinite forbidden")
            ),
        )
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise VerificationError(f"strict JSON:{label}") from error
    need(isinstance(value, dict), f"top-level object:{label}")
    validate_json_tree(value)
    return value


def load_pinned(
    name: str,
    expected_sha256: str,
    schema: str,
    result_sha256: str,
) -> dict[str, Any]:
    path = HERE / name
    raw = check_plain_file(path, name, MAX_JSON_BYTES)
    need(hashlib.sha256(raw).hexdigest() == expected_sha256, f"pin:{name}")
    document = strict_json_bytes(raw, name)
    need(set(document) == {"schema", "result", "result_sha256"}, f"envelope:{name}")
    need(document["schema"] == schema, f"schema:{name}")
    need(document["result_sha256"] == result_sha256, f"result pin:{name}")
    need(digest(document["result"]) == result_sha256, f"result digest:{name}")
    return document["result"]


def unpack_table(document: dict[str, Any], name: str) -> list[dict[str, Any]]:
    columns = document["row_column_schemas"][name]
    need(len(columns) == len(set(columns)), f"columns:{name}")
    return [
        dict(zip(columns, row, strict=True))
        for row in document[name]
    ]


def exact_positive_face(
    resolved_box: list[str],
    retained_leaf_box: list[str],
) -> dict[str, Any] | None:
    need(len(resolved_box) == len(retained_leaf_box) == 6, "3D boxes")
    left = [Q(value) for value in resolved_box]
    right = [Q(value) for value in retained_leaf_box]
    touching: list[tuple[int, str, str]] = []
    intersection: list[Q] = []
    for axis in range(3):
        left_lo, left_hi = left[2 * axis:2 * axis + 2]
        right_lo, right_hi = right[2 * axis:2 * axis + 2]
        lo = max(left_lo, right_lo)
        hi = min(left_hi, right_hi)
        if hi < lo:
            return None
        if hi == lo:
            if left_hi == right_lo:
                touching.append((axis, "UPPER", "LOWER"))
            elif right_hi == left_lo:
                touching.append((axis, "LOWER", "UPPER"))
            else:
                return None
        intersection.extend((lo, hi))
    if len(touching) != 1:
        return None
    axis, resolved_side, retained_side = touching[0]
    nonzero = [
        intersection[2 * index + 1] - intersection[2 * index]
        for index in range(3)
        if index != axis
    ]
    need(len(nonzero) == 2 and all(value > 0 for value in nonzero), "positive face")
    return {
        "axis": "tps"[axis],
        "resolved_side": resolved_side,
        "retained_side": retained_side,
        "box": [str(value) for value in intersection],
        "area": str(nonzero[0] * nonzero[1]),
    }


def resolved_signature(row: dict[str, Any]) -> dict[str, Any]:
    return {
        "official_key_ordinal": row["official_key_ordinal"],
        "official_key_id": row["official_key_id"],
        "official_key_row": row["official_key_row"],
        "ordered_integer_wall_events": row["ordered_integer_wall_events"],
        "signed_wall_word": row["signed_wall_word"],
        "roof": row["roof"],
        "outgoing_cell": row["outgoing_cell"],
        "source_chart": row["chart"],
        "target_chart": row["target_chart"],
        "target_lift": row["owner_target"],
    }


def load_factor_kernel() -> Any:
    pins = {ROUND186_SOURCE: ROUND186_SOURCE_SHA256, **FACTOR_DEPENDENCY_PINS}
    for name, expected in pins.items():
        raw = check_plain_file(HERE / name, name, 16 * 1024 * 1024)
        need(hashlib.sha256(raw).hexdigest() == expected, f"factor pin:{name}")
    if str(HERE) not in sys.path:
        sys.path.insert(0, str(HERE))
    try:
        module = importlib.import_module(
            "cm2_round186_source_g_factor_face_probe"
        )
    except (ImportError, ModuleNotFoundError) as error:
        raise VerificationError("Round186 factor kernel unavailable") from error
    module.ctx.prec = 256
    need(module.ctx.prec == 256, "factor precision")
    need(
        isinstance(module.r179.FLINT_VERSION, str)
        and module.r179.FLINT_VERSION != "",
        "FLINT version",
    )
    return module


def whole_face_profiles(
    kernel: Any,
    chart: str,
    target: str,
    face_box: list[str],
    path: str,
) -> dict[str, dict[str, str]]:
    box = kernel.r179.r174.atlas.AtlasBox(
        *(Q(value) for value in face_box),
        0,
        path,
    )
    geometry = kernel.factor_geometry(chart, target, box)
    result: dict[str, dict[str, str]] = {}
    for factor in ("HPLUS", "HMINUS"):
        direct = kernel.r179.arb_sign(geometry[factor][0])
        centered = kernel.r179.arb_sign(
            kernel.centered_value(chart, target, box, factor)
        )
        selected = direct if direct in STRICT_SIGNS else centered
        result[factor] = {
            "direct_sign": direct,
            "centered_sign": centered,
            "selected_sign": selected,
        }
    return result


def build_model() -> dict[str, Any]:
    upstream = {
        label: load_pinned(*spec)
        for label, spec in INPUTS.items()
    }
    kernel = load_factor_kernel()

    resolved_rows = unpack_table(upstream["Round179_rows"], "resolved_3d_child_rows")
    retained_rows = unpack_table(upstream["Round179_rows"], "retained_3d_child_rows")
    resolved = {row["row_id"]: row for row in resolved_rows}
    retained = {row["row_id"]: row for row in retained_rows}
    need(len(resolved) == 17_192, "Round179 resolved census")
    need(len(retained) == 106_680, "Round179 retained census")

    table220 = upstream["Round220"]["coordinate_boundary_atlas"]["tables"][
        "one_step_split_interface_rows"
    ]
    columns220 = table220["columns"]
    interfaces: list[dict[str, Any]] = []
    for packed in table220["rows"]:
        row = dict(zip(columns220, packed, strict=True))
        if {row["lower_child_kind"], row["upper_child_kind"]} != {
            "RESOLVED", "RETAINED"
        }:
            continue
        if row["lower_child_kind"] == "RESOLVED":
            resolved_id = row["lower_child_row_id"]
            retained_id = row["upper_child_row_id"]
        else:
            resolved_id = row["upper_child_row_id"]
            retained_id = row["lower_child_row_id"]
        need(resolved_id in resolved and retained_id in retained, "interface child IDs")
        need(
            row["event_trace_materialized_on_interface"] is False
            and row["physical_glue_credit"] == 0
            and row["whole_origin_credit"] == 0
            and row["global_exact_key_disposition_credit"] == 0,
            "Round220 nonpromotion",
        )
        need(
            row["half_open_owner_child_kind"] == row["upper_child_kind"]
            and row["half_open_owner_child_row_id"] == row["upper_child_row_id"],
            "Round220 half-open owner",
        )
        interfaces.append({
            **row,
            "resolved_child_row_id": resolved_id,
            "retained_child_row_id": retained_id,
        })
    need(
        len(interfaces) == 8_960
        and len({row["split_interface_id"] for row in interfaces}) == 8_960
        and len({row["resolved_child_row_id"] for row in interfaces}) == 8_960
        and len({row["retained_child_row_id"] for row in interfaces}) == 8_960,
        "interface universe",
    )
    interface_resolved_ids = {
        row["resolved_child_row_id"] for row in interfaces
    }
    normal_account = upstream["Round220"][
        "outgoing_wall_and_seam_normal_form_boundary_account"
    ]
    reference_table = normal_account["tables"][
        "resolved_child_normal_form_reference_rows"
    ]
    reference_columns = reference_table["columns"]
    normal_references = [
        dict(zip(reference_columns, packed, strict=True))
        for packed in reference_table["rows"]
        if packed[reference_columns.index("source_child_row_id")]
        in interface_resolved_ids
    ]
    reference_multiplicity = Counter(
        row["source_child_row_id"] for row in normal_references
    )
    need(
        len(normal_references) == 8_976
        and set(reference_multiplicity) == interface_resolved_ids
        and Counter(reference_multiplicity.values()) == {1: 8_952, 3: 8}
        and Counter(row["source_table"] for row in normal_references) == {
            "outgoing_normal_form_rows": 5_816,
            "wall_normal_form_rows": 2_888,
            "source_chart_seam_rows": 264,
            "pair_arrangement_candidate_rows": 8,
        }
        and all(
            row["resolved_child_closed_enclosure_status"]
            == "STRICT_DYNAMIC_SIGNATURE__EVENT_ZERO_SET_ABSENT"
            and row["event_sheet_incidence_count"] == 0
            and row["event_trace_glue_count"] == 0
            and row["physical_component_credit"] == 0
            and row["global_exact_key_disposition_credit"] == 0
            for row in normal_references
        ),
        "resolved interface normal-form reference closure",
    )
    need(
        digest(sorted(row["reference_id"] for row in normal_references))
        == "48e129ccad348ffc522799c78547cb904ebbd700bbd6ebb256a04798b32d4bd0",
        "normal reference ID digest",
    )
    need(
        digest(sorted(
            row["split_interface_id"] for row in interfaces
        ))
        == "5f21e8ace887e06af7d039b0d6f6c346a4179ab442b9377b77cfde57382207a1",
        "interface ID digest",
    )

    regions208 = upstream["Round208"]["formal_local_open_3D_signature_ledger"]["rows"]
    regions_by_retained: dict[str, list[dict[str, Any]]] = defaultdict(list)
    region208: dict[str, dict[str, Any]] = {}
    for row in regions208:
        region_id = row["region_row_id"]
        need(region_id not in region208, "Round208 region uniqueness")
        region208[region_id] = row
        regions_by_retained[row["retained_child_row_id"]].append(row)
    need(len(region208) == 36_040, "Round208 region census")

    region_to_sheet: dict[str, str] = {}
    sheet_to_key: dict[str, tuple[int, str]] = {}
    for row in upstream["Round211"]["formal_2D_sheet_owner_ledger"]["rows"]:
        owner_signature = region208[row["owner_region_row_id"]][
            "local_return_signature"
        ]
        shadow_signature = region208[row["shadow_region_row_id"]][
            "local_return_signature"
        ]
        need(
            (
                owner_signature["official_key_ordinal"],
                owner_signature["official_key_id"],
            )
            == (
                shadow_signature["official_key_ordinal"],
                shadow_signature["official_key_id"],
            ),
            "Round211 sheet key purity",
        )
        sheet_to_key[row["sheet_row_id"]] = (
            owner_signature["official_key_ordinal"],
            owner_signature["official_key_id"],
        )
        for field in ("owner_region_row_id", "shadow_region_row_id"):
            region_id = row[field]
            need(region_id in region208 and region_id not in region_to_sheet,
                 "Round211 region incidence")
            region_to_sheet[region_id] = row["sheet_row_id"]
    need(len(region_to_sheet) == 35_432, "Round211 region incidence census")

    sheet_to_block: dict[str, str] = {}
    block_to_keys: dict[str, set[tuple[int, str]]] = defaultdict(set)
    for row in upstream["Round225"]["formal_Round211_sheet_assignment_ledger"]["rows"]:
        sheet_id = row["Round211_sheet_row_id"]
        need(sheet_id not in sheet_to_block, "Round225 assignment uniqueness")
        sheet_to_block[sheet_id] = row["known_connectivity_block_id"]
        block_to_keys[row["known_connectivity_block_id"]].add(
            sheet_to_key[sheet_id]
        )
    need(len(sheet_to_block) == 17_716, "Round225 assignment census")
    need(
        len(block_to_keys) == 7_404
        and all(len(keys) == 1 for keys in block_to_keys.values()),
        "Round225 block key purity",
    )

    accepted: list[dict[str, Any]] = []
    rejected: list[dict[str, Any]] = []
    interface_model: list[dict[str, Any]] = []
    counters: Counter[str] = Counter()
    accepted_by_resolved: dict[str, list[dict[str, Any]]] = defaultdict(list)

    for interface in sorted(interfaces, key=lambda row: row["split_interface_id"]):
        resolved_row = resolved[interface["resolved_child_row_id"]]
        retained_row = retained[interface["retained_child_row_id"]]
        need(
            resolved_row["origin_row_id"] == retained_row["origin_row_id"]
            == interface["origin_row_id"]
            and resolved_row["parent_id"] == retained_row["parent_id"]
            == interface["parent_id"]
            and resolved_row["chart"] == retained_row["chart"]
            == interface["chart"],
            "exact sibling identity",
        )
        expected_signature = resolved_signature(resolved_row)
        signature_sha = digest(expected_signature)
        accepted_here: list[dict[str, Any]] = []
        rejected_here: list[dict[str, Any]] = []
        ignored_remote_wrong_signature = 0
        for region in sorted(
            regions_by_retained.get(interface["retained_child_row_id"], []),
            key=lambda row: row["region_row_id"],
        ):
            signature_exact = region["local_return_signature"] == expected_signature
            face = exact_positive_face(resolved_row["box"], region["Round182_leaf_box"])
            if face is None:
                if signature_exact:
                    item = {
                        "interface": interface,
                        "resolved": resolved_row,
                        "retained": retained_row,
                        "region": region,
                        "signature_sha256": signature_sha,
                        "region_signature_sha256":
                            digest(region["local_return_signature"]),
                        "signature_exact": True,
                        "face": None,
                        "profiles": None,
                        "classification":
                            "REMOTE_FULL_SIGNATURE_REGION__NO_EXACT_FACE_OVERLAP",
                    }
                    rejected.append(item)
                    rejected_here.append(item)
                    counters["remote_exact_signature"] += 1
                else:
                    ignored_remote_wrong_signature += 1
                continue
            need(
                face["axis"] == interface["axis"],
                "face/interface axis",
            )
            axis_index = "tps".index(face["axis"])
            face_q = [Q(value) for value in face["box"]]
            need(
                face_q[2 * axis_index]
                == face_q[2 * axis_index + 1]
                == Q(interface["fixed_coordinate"]),
                "face/interface plane",
            )
            face_tangential: list[Q] = []
            for index in range(3):
                if index != axis_index:
                    face_tangential.extend(
                        face_q[2 * index:2 * index + 2]
                    )
            interface_tangential = [
                Q(value) for value in interface["tangential_half_open_box"]
            ]
            need(
                interface_tangential[0] <= face_tangential[0]
                < face_tangential[1] <= interface_tangential[1]
                and interface_tangential[2] <= face_tangential[2]
                < face_tangential[3] <= interface_tangential[3],
                "face exact tangential overlap",
            )
            expected_resolved_side = (
                "UPPER"
                if interface["lower_child_kind"] == "RESOLVED"
                else "LOWER"
            )
            need(
                face["resolved_side"] == expected_resolved_side
                and face["retained_side"]
                == ("LOWER" if expected_resolved_side == "UPPER" else "UPPER"),
                "face side orientation",
            )
            profiles = whole_face_profiles(
                kernel,
                resolved_row["chart"],
                resolved_row["owner_target"],
                face["box"],
                (
                    f"round230-verifier:{interface['split_interface_id']}:"
                    f"{region['region_row_id']}"
                ),
            )
            factor_compatible = (
                profiles["HPLUS"]["selected_sign"] == region["HPLUS_sign"]
                and profiles["HMINUS"]["selected_sign"] == region["HMINUS_sign"]
                and profiles["HPLUS"]["selected_sign"] in STRICT_SIGNS
                and profiles["HMINUS"]["selected_sign"] in STRICT_SIGNS
            )
            item = {
                "interface": interface,
                "resolved": resolved_row,
                "retained": retained_row,
                "region": region,
                "signature_sha256": signature_sha,
                "region_signature_sha256": digest(region["local_return_signature"]),
                "signature_exact": signature_exact,
                "face": face,
                "profiles": profiles,
                "factor_compatible": factor_compatible,
            }
            counters["face_candidates"] += 1
            counters[f"face_candidates_{face['axis']}"] += 1
            if signature_exact and factor_compatible:
                sheet_id = region_to_sheet.get(region["region_row_id"])
                block_id = None if sheet_id is None else sheet_to_block[sheet_id]
                if block_id is not None:
                    need(
                        block_to_keys[block_id] == {
                            (
                                resolved_row["official_key_ordinal"],
                                resolved_row["official_key_id"],
                            )
                        },
                        "bridge block/resolved key identity",
                    )
                item["sheet_row_id"] = sheet_id
                item["known_block_id"] = block_id
                item["classification"] = (
                    "CERTIFIED_EXACT_POSITIVE_AREA_LOCAL_BULK_"
                    "CONTINUATION_PATCH"
                )
                accepted.append(item)
                accepted_here.append(item)
                accepted_by_resolved[resolved_row["row_id"]].append(item)
                counters["accepted"] += 1
                counters[f"accepted_{face['axis']}"] += 1
                counters[
                    "accepted_sheet_backed" if sheet_id is not None
                    else "accepted_sheetless"
                ] += 1
            else:
                item["classification"] = (
                    "REJECTED_WRONG_SIDE_OR_INCOMPATIBLE_FULL_FACE_REGION"
                )
                rejected.append(item)
                rejected_here.append(item)
                counters["rejected_incompatible"] += 1
        block_ids = sorted({
            item["known_block_id"]
            for item in accepted_here
            if item["known_block_id"] is not None
        })
        need(len(block_ids) <= 1, "unique block seed per bridge star")
        tangential = [
            Q(value) for value in interface["tangential_half_open_box"]
        ]
        interface_area = (
            (tangential[1] - tangential[0])
            * (tangential[3] - tangential[2])
        )
        accepted_area = sum(
            (Q(item["face"]["area"]) for item in accepted_here),
            Q(0),
        )
        coverage_ratio = (
            str(accepted_area / interface_area)
            if accepted_here else "0"
        )
        interface_model.append({
            "interface": interface,
            "accepted": accepted_here,
            "rejected": rejected_here,
            "ignored_remote_wrong_signature": ignored_remote_wrong_signature,
            "known_block_ids": block_ids,
            "accepted_patch_area": str(accepted_area),
            "interface_tangential_area": str(interface_area),
            "accepted_patch_coverage_ratio": coverage_ratio,
        })

    need(
        counters["face_candidates"] == 1_512
        and counters["face_candidates_t"] == 744
        and counters["face_candidates_p"] == 768
        and counters["accepted"] == 784
        and counters["accepted_t"] == 400
        and counters["accepted_p"] == 384
        and counters["accepted_sheet_backed"] == 728
        and counters["accepted_sheetless"] == 56
        and counters["rejected_incompatible"] == 728
        and counters["remote_exact_signature"] == 12
        and len(rejected) == 740,
        "Round230 bridge census",
    )
    coverage = Counter(
        (
            row["interface"]["axis"],
            row["accepted_patch_coverage_ratio"],
        )
        for row in interface_model
        if row["accepted"]
    )
    need(
        coverage == {
            ("t", "1/64"): 276,
            ("t", "1/32"): 44,
            ("t", "9/64"): 4,
            ("p", "1/64"): 112,
            ("p", "1/32"): 8,
            ("p", "1"): 4,
        },
        "positive-area patch coverage distribution",
    )

    stars_with_block = {
        row["resolved"]["row_id"]: row
        for row in accepted
        if row["known_block_id"] is not None
    }
    resolved_to_blocks: dict[str, set[str]] = defaultdict(set)
    for row in accepted:
        if row["known_block_id"] is not None:
            resolved_to_blocks[row["resolved"]["row_id"]].add(row["known_block_id"])
    need(
        len(resolved_to_blocks) == 444
        and all(len(values) == 1 for values in resolved_to_blocks.values()),
        "block-backed bridge stars",
    )
    bridge_star_count = len(accepted_by_resolved)
    need(bridge_star_count == 448, "bridge star count")

    incidence_delta: list[dict[str, Any]] = []
    for resolved_id in sorted(resolved_to_blocks):
        block_id = next(iter(resolved_to_blocks[resolved_id]))
        row = resolved[resolved_id]
        incidence_delta.append({
            "occurrence_row_id": resolved_id,
            "occurrence_gauge": "ROUND179_RESOLVED_CHILD",
            "official_key_ordinal": row["official_key_ordinal"],
            "official_key_id": row["official_key_id"],
            "known_block_id": block_id,
            "derivation":
                "CERTIFIED_LOCAL_BULK_BRIDGE_TO_DIRECT_SHEET_INCIDENCE",
        })
    propagated_sheetless = 0
    for resolved_id, edges in sorted(accepted_by_resolved.items()):
        blocks = sorted({
            edge["known_block_id"]
            for edge in edges
            if edge["known_block_id"] is not None
        })
        if not blocks:
            continue
        need(len(blocks) == 1, "bridge propagation unique block")
        for edge in edges:
            if edge["known_block_id"] is not None:
                continue
            region = edge["region"]
            incidence_delta.append({
                "occurrence_row_id": region["region_row_id"],
                "occurrence_gauge": "ROUND208_STRICT_OPEN_REGION",
                "official_key_ordinal":
                    region["local_return_signature"]["official_key_ordinal"],
                "official_key_id":
                    region["local_return_signature"]["official_key_id"],
                "known_block_id": blocks[0],
                "derivation":
                    "CERTIFIED_LOCAL_BULK_BRIDGE_STAR_PROPAGATION",
            })
            propagated_sheetless += 1
    need(
        len(incidence_delta) == 464
        and propagated_sheetless == 20,
        "incidence delta",
    )

    r229_occurrences = upstream["Round229"][
        "formal_occurrence_known_block_attachment_frontier_ledger"
    ]["rows"]
    occurrence229 = {
        row["local_occurrence_row_id"]: row for row in r229_occurrences
    }
    need(len(occurrence229) == 53_968, "Round229 occurrence ID uniqueness")
    direct_incidence = {
        occurrence_id: row["Round225_known_connectivity_block_id"]
        for occurrence_id, row in occurrence229.items()
        if row["Round225_known_connectivity_block_id"] is not None
    }
    need(
        len(r229_occurrences) == 53_968
        and len(direct_incidence) == 35_432,
        "Round229 occurrence frontier",
    )
    delta_map: dict[str, str] = {}
    for row in incidence_delta:
        occurrence_id = row["occurrence_row_id"]
        need(
            occurrence_id in occurrence229
            and occurrence_id not in direct_incidence
            and occurrence_id not in delta_map,
            "delta occurrence exact new join",
        )
        old = occurrence229[occurrence_id]
        need(
            (
                old["official_key_ordinal"],
                old["official_key_id"],
            )
            == (
                row["official_key_ordinal"],
                row["official_key_id"],
            )
            and block_to_keys[row["known_block_id"]] == {
                (row["official_key_ordinal"], row["official_key_id"])
            },
            "delta occurrence/block key identity",
        )
        delta_map[occurrence_id] = row["known_block_id"]
    post_incidence = {**direct_incidence, **delta_map}
    need(
        len(post_incidence) == 35_896
        and set(direct_incidence).isdisjoint(delta_map),
        "post-bridge incidence set",
    )

    return {
        "upstream": upstream,
        "normal_references": sorted(
            normal_references, key=lambda row: row["reference_id"]
        ),
        "interfaces": interface_model,
        "accepted": accepted,
        "rejected": rejected,
        "incidence_delta": sorted(
            incidence_delta,
            key=lambda row: (row["occurrence_gauge"], row["occurrence_row_id"]),
        ),
        "post_incidence": dict(sorted(post_incidence.items())),
        "counters": counters,
        "resolved_to_blocks": resolved_to_blocks,
        "accepted_by_resolved": accepted_by_resolved,
        "expected_census": {
            "resolved_retained_interface_count": 8_960,
            "interface_event_zero_set_absent_count": 8_960,
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
            "local_occurrence_count": 53_968,
            "known_connectivity_block_count": 7_404,
            "maximal_physical_component_assignment_count": 0,
            "global_exact_key_fibre_exhausted_count": 0,
        },
    }


def verify_closed_ledger(
    value: Any,
    id_field: str,
    expected_count: int,
    label: str,
) -> list[dict[str, Any]]:
    need(isinstance(value, dict), f"ledger object:{label}")
    need(
        set(value) == {
            "row_count", "rows_sha256", "row_ids_sha256",
            "row_hashes_sha256", "every_row_closed_by_own_SHA256", "rows",
        },
        f"ledger fields:{label}",
    )
    rows = value["rows"]
    need(isinstance(rows, list) and len(rows) == expected_count, f"rows:{label}")
    need(value["row_count"] == expected_count, f"row count:{label}")
    need(value["every_row_closed_by_own_SHA256"] is True, f"closure flag:{label}")
    ids: list[str] = []
    hashes: list[str] = []
    for row in rows:
        need(isinstance(row, dict) and id_field in row, f"row shape:{label}")
        need(isinstance(row[id_field], str), f"row ID type:{label}")
        claimed = row.get("row_sha256")
        need(isinstance(claimed, str) and len(claimed) == 64, f"row hash:{label}")
        payload = dict(row)
        del payload["row_sha256"]
        need(digest(payload) == claimed, f"row closure:{label}:{row[id_field]}")
        ids.append(row[id_field])
        hashes.append(claimed)
    need(len(ids) == len(set(ids)), f"unique IDs:{label}")
    need(digest(rows) == value["rows_sha256"], f"rows digest:{label}")
    need(digest(ids) == value["row_ids_sha256"], f"ID digest:{label}")
    need(digest(hashes) == value["row_hashes_sha256"], f"hash digest:{label}")
    return rows


def prepare_expected(model: dict[str, Any]) -> dict[str, Any]:
    expected_census = dict(model["expected_census"])
    expected_census.pop("local_occurrence_count")
    accepted: dict[tuple[str, str], dict[str, Any]] = {}
    candidates: dict[tuple[str, str], dict[str, Any]] = {}
    rejected: dict[tuple[str, str], dict[str, Any]] = {}
    for item in model["accepted"]:
        key = (
            item["interface"]["split_interface_id"],
            item["region"]["region_row_id"],
        )
        expected = {
            "axis": item["face"]["axis"],
            "box": item["face"]["box"],
            "area": item["face"]["area"],
            "sheet": item["sheet_row_id"],
            "block": item["known_block_id"],
            "HPLUS": item["profiles"]["HPLUS"]["selected_sign"],
            "HMINUS": item["profiles"]["HMINUS"]["selected_sign"],
        }
        need(key not in accepted, "expected accepted uniqueness")
        accepted[key] = expected
        candidates[key] = {**expected, "accepted": True}
    for item in model["rejected"]:
        key = (
            item["interface"]["split_interface_id"],
            item["region"]["region_row_id"],
        )
        remote = item["face"] is None
        expected = {
            "remote": remote,
            "axis": None if remote else item["face"]["axis"],
            "box": None if remote else item["face"]["box"],
            "area": None if remote else item["face"]["area"],
        }
        rejected[key] = expected
        if not remote:
            candidates[key] = {**expected, "accepted": False}

    stars: dict[str, dict[str, Any]] = {}
    for item in model["interfaces"]:
        if not item["accepted"]:
            continue
        interface_id = item["interface"]["split_interface_id"]
        blocks = item["known_block_ids"]
        stars[interface_id] = {
            "resolved": item["interface"]["resolved_child_row_id"],
            "count": len(item["accepted"]),
            "ratio": item["accepted_patch_coverage_ratio"],
            "block": blocks[0] if blocks else None,
            "sheetless": sum(
                edge.get("sheet_row_id") is None for edge in item["accepted"]
            ),
        }

    delta = {
        (row["occurrence_gauge"], row["occurrence_row_id"]): {
            "ordinal": row["official_key_ordinal"],
            "key": row["official_key_id"],
            "block": row["known_block_id"],
            "derivation": row["derivation"],
        }
        for row in model["incidence_delta"]
    }
    occurrence_rows = model["upstream"]["Round229"][
        "formal_occurrence_known_block_attachment_frontier_ledger"
    ]["rows"]
    occurrences = {
        row["local_occurrence_row_id"]: {
            "gauge": row["local_occurrence_gauge"],
            "ordinal": row["official_key_ordinal"],
            "key": row["official_key_id"],
        }
        for row in occurrence_rows
    }
    coverage = Counter(
        (item["interface"]["axis"], item["accepted_patch_coverage_ratio"])
        for item in model["interfaces"] if item["accepted"]
    )
    return {
        "census": {
            **expected_census,
            "normal_form_absence_reference_count": 8_976,
            "Round208_retained_side_materialized_interface_count": 460,
            "Round208_relevant_region_count": 1_536,
            "Round182_relevant_leaf_count": 796,
            "Round182_relevant_occurrence_count": 460,
        },
        "accepted": accepted,
        "candidates": candidates,
        "rejected": rejected,
        "stars": stars,
        "delta": delta,
        "post_incidence": model["post_incidence"],
        "occurrences": occurrences,
        "normal_reference_count": len(model["normal_references"]),
        "coverage": [
            {"axis": axis, "coverage_ratio": ratio, "bridge_star_count": count}
            for (axis, ratio), count in sorted(coverage.items())
        ],
    }


def verify_result(result: dict[str, Any], expected: dict[str, Any]) -> dict[str, Any]:
    need(
        set(result) == {
            "status", "census", "formal_resolved_child_event_zero_set_absence_ledger",
            "formal_exact_face_candidate_ledger",
            "formal_certified_local_bulk_continuation_edge_ledger",
            "formal_rejected_local_bulk_candidate_ledger",
            "formal_certified_local_bulk_bridge_star_ledger",
            "formal_occurrence_known_block_incidence_delta_ledger",
            "formal_post_Round230_occurrence_known_block_frontier_ledger",
            "formal_post_Round230_key_frontier_ledger", "coverage_distribution",
            "frozen_oracles", "scope_contract", "strict_nonpromotion",
            "required_next", "provenance",
        },
        "candidate top-level fields",
    )
    need(
        result["status"] == (
            "CERTIFIED_784_NON_EVENT_STRICT_POSITIVE_AREA_LOCAL_BULK_"
            "CONTINUATION_PATCHES__448_INTERFACES__464_NEW_KNOWN_BLOCK_"
            "INCIDENCES__ZERO_MEMBERSHIP_COMPONENT_MAXIMAL_OR_GLOBAL_CREDIT"
        ),
        "status",
    )
    need(result["census"] == expected["census"], "exact census")
    need(result["coverage_distribution"] == expected["coverage"], "coverage")
    scope = result["scope_contract"]
    need(
        scope == {
            "accepted_edges_are_strict_positive_area_local_bulk_patches": True,
            "resolved_child_event_zero_sets_absent": True,
            "whole_interface_certified_only_when_coverage_ratio_is_one": True,
            "known_block_incidence_is_not_membership": True,
            "known_blocks_are_not_claimed_maximal_physical_components": True,
            "all_retained_event_strata_exhausted": False,
            "global_exact_key_fibres_exhausted": False,
        },
        "scope contract",
    )
    need(
        result["strict_nonpromotion"] == {
            "known_block_membership_assignment_credit": 0,
            "maximal_physical_component_credit": 0,
            "global_exact_key_fibre_exhausted_count": 0,
            "global_exact_key_disposition_credit": 0,
            "source_G_global_exact_key_dispositions": "0/224580",
            "D02": "BLOCKED", "global_Gate5_fields": "10/18",
            "global_complete_18_field_blocks": 0, "CM2": "NO-GO_FOR_CLAIM",
        },
        "strict nonpromotion",
    )
    need(isinstance(result["required_next"], str) and result["required_next"], "next")
    producer_path = HERE / "cm2_round230_source_g_resolved_retained_bulk_continuation.py"
    producer_sha = hashlib.sha256(check_plain_file(
        producer_path, producer_path.name, 5_000_000
    )).hexdigest()
    need(
        result["provenance"]["schema"] == SCHEMA
        and result["provenance"]["producer_sha256"] == producer_sha,
        "producer provenance",
    )

    absence = verify_closed_ledger(
        result["formal_resolved_child_event_zero_set_absence_ledger"],
        "event_zero_set_absence_row_id", 8_976, "absence",
    )
    need(
        all(
            row["resolved_child_event_zero_set"] == "ABSENT"
            and row["resolved_child_event_sheet_incidence_count"] == 0
            and row["physical_component_credit"] == 0
            and row["global_exact_key_disposition_credit"] == 0
            for row in absence
        ),
        "absence semantics",
    )
    candidates = verify_closed_ledger(
        result["formal_exact_face_candidate_ledger"],
        "face_candidate_row_id", 1_512, "candidates",
    )
    edges = verify_closed_ledger(
        result["formal_certified_local_bulk_continuation_edge_ledger"],
        "certified_local_bulk_bridge_edge_id", 784, "edges",
    )
    rejects = verify_closed_ledger(
        result["formal_rejected_local_bulk_candidate_ledger"],
        "reject_row_id", 740, "rejects",
    )
    stars = verify_closed_ledger(
        result["formal_certified_local_bulk_bridge_star_ledger"],
        "bridge_star_row_id", 448, "stars",
    )
    delta = verify_closed_ledger(
        result["formal_occurrence_known_block_incidence_delta_ledger"],
        "incidence_delta_row_id", 464, "delta",
    )
    post = verify_closed_ledger(
        result["formal_post_Round230_occurrence_known_block_frontier_ledger"],
        "post_frontier_row_id", 53_968, "post frontier",
    )
    keys = verify_closed_ledger(
        result["formal_post_Round230_key_frontier_ledger"],
        "key_frontier_row_id", 116, "key frontier",
    )

    actual_candidates: dict[tuple[str, str], dict[str, Any]] = {}
    for row in candidates:
        pair = (row["Round220_split_interface_id"], row["Round208_region_row_id"])
        actual_candidates[pair] = row
        need(
            row["physical_component_credit"] == 0
            and row["global_exact_key_disposition_credit"] == 0,
            "candidate nonpromotion",
        )
    need(set(actual_candidates) == set(expected["candidates"]), "candidate universe")
    for pair, exp in expected["candidates"].items():
        row = actual_candidates[pair]
        need(
            row["axis"] == exp["axis"]
            and row["exact_intersection_box"] == exp["box"]
            and row["exact_positive_area"] == exp["area"]
            and row["return_signature_exact_equality"] is exp["accepted"]
            and row["strict_factor_signs_equal_on_whole_patch"] is exp["accepted"],
            f"candidate semantics:{pair}",
        )

    actual_edges: dict[tuple[str, str], dict[str, Any]] = {}
    for row in edges:
        pair = (row["Round220_split_interface_id"], row["Round208_region_row_id"])
        actual_edges[pair] = row
        exp = expected["accepted"].get(pair)
        need(exp is not None, f"unexpected edge:{pair}")
        need(
            row["axis"] == exp["axis"]
            and row["exact_intersection_box"] == exp["box"]
            and row["exact_positive_area"] == exp["area"]
            and row["Round211_sheet_row_id"] == exp["sheet"]
            and row["Round225_known_block_id"] == exp["block"]
            and row["Round186_HPLUS_whole_patch_sign"] == exp["HPLUS"]
            and row["Round186_HMINUS_whole_patch_sign"] == exp["HMINUS"]
            and row["all_10_return_signature_fields_exactly_equal"] is True
            and row["both_factor_signs_strict_and_equal_on_whole_patch"] is True
            and row["whole_interface_certified"] is False
            and row["known_block_membership_assignment_credit"] == 0
            and row["maximal_physical_component_credit"] == 0,
            f"edge semantics:{pair}",
        )
    need(set(actual_edges) == set(expected["accepted"]), "accepted edge universe")

    actual_rejects = {
        (row["Round220_split_interface_id"], row["Round208_region_row_id"]): row
        for row in rejects
    }
    need(set(actual_rejects) == set(expected["rejected"]), "reject universe")
    for pair, exp in expected["rejected"].items():
        row = actual_rejects[pair]
        need(
            row["known_block_incidence_bridge_credit"] == 0
            and row["physical_component_credit"] == 0
            and (row["intersection_patch"] is None) is exp["remote"],
            f"reject semantics:{pair}",
        )

    actual_stars = {row["Round220_split_interface_id"]: row for row in stars}
    need(set(actual_stars) == set(expected["stars"]), "star universe")
    for interface_id, exp in expected["stars"].items():
        row = actual_stars[interface_id]
        need(
            row["resolved_child_row_id"] == exp["resolved"]
            and row["accepted_patch_count"] == exp["count"]
            and row["accepted_patch_coverage_ratio"] == exp["ratio"]
            and row["Round225_known_connectivity_block_id"] == exp["block"]
            and row["sheetless_patch_count"] == exp["sheetless"]
            and row["whole_interface_certified"] is (exp["ratio"] == "1")
            and row["global_exact_key_disposition_credit"] == 0,
            f"star semantics:{interface_id}",
        )

    actual_delta = {}
    for row in delta:
        key = (row["local_occurrence_gauge"], row["local_occurrence_row_id"])
        actual_delta[key] = {
            "ordinal": row["official_key_ordinal"], "key": row["official_key_id"],
            "block": row["Round225_known_connectivity_block_id"],
            "derivation": row["derivation"],
        }
        need(
            row["known_block_incidence_attachment_credit"] == 1
            and row["known_block_membership_assignment_credit"] == 0
            and row["global_exact_key_disposition_credit"] == 0,
            "delta nonpromotion",
        )
    need(actual_delta == expected["delta"], "incidence delta semantics")

    actual_post: dict[str, str] = {}
    seen_occurrences: set[str] = set()
    per_key = defaultdict(Counter)
    for row in post:
        occurrence_id = row["local_occurrence_row_id"]
        need(occurrence_id not in seen_occurrences, "post occurrence uniqueness")
        seen_occurrences.add(occurrence_id)
        exp = expected["occurrences"].get(occurrence_id)
        need(
            exp is not None and row["local_occurrence_gauge"] == exp["gauge"]
            and row["official_key_ordinal"] == exp["ordinal"]
            and row["official_key_id"] == exp["key"],
            f"post occurrence identity:{occurrence_id}",
        )
        block = row["Round225_known_connectivity_block_id"]
        if block is not None:
            actual_post[occurrence_id] = block
        attached = block is not None
        need(
            row["known_block_incidence_attachment_credit"] == int(attached)
            and row["known_block_membership_assignment_credit"] == 0
            and row["maximal_physical_component_assignment_credit"] == 0
            and row["global_exact_key_fibre_exhausted"] is False
            and row["global_exact_key_disposition_credit"] == 0,
            f"post nonpromotion:{occurrence_id}",
        )
        per_key[exp["ordinal"]]["total"] += 1
        per_key[exp["ordinal"]]["attached" if attached else "unattached"] += 1
        if row["incidence_source"] == "ROUND230_CERTIFIED_LOCAL_BULK_BRIDGE":
            per_key[exp["ordinal"]]["new"] += 1
    need(seen_occurrences == set(expected["occurrences"]), "post occurrence universe")
    need(actual_post == expected["post_incidence"], "post incidence mapping")

    need(len({row["official_key_ordinal"] for row in keys}) == 116, "key ordinals")
    for row in keys:
        counts = per_key[row["official_key_ordinal"]]
        need(
            row["local_occurrence_count"] == counts["total"]
            and row["occurrences_with_known_block_incidence"] == counts["attached"]
            and row["occurrences_without_known_block_incidence"] == counts["unattached"]
            and row["new_Round230_known_block_incidences"] == counts["new"]
            and row["global_exact_key_fibre_exhausted"] is False
            and row["maximal_physical_component_assignment_count"] == 0
            and row["global_exact_key_disposition_credit"] == 0,
            f"key frontier:{row['official_key_ordinal']}",
        )
    return {
        "candidate_semantically_valid": True,
        "interfaces": 8_960, "accepted_edges": 784, "rejected": 740,
        "bridge_stars": 448, "incidence_delta": 464,
        "post_incident": 35_896, "post_unattached": 18_072,
    }


def safe_write(path: Path, data: bytes) -> None:
    descriptor, name = tempfile.mkstemp(prefix=f".{path.name}.", suffix=".tmp", dir=path.parent)
    temporary = Path(name)
    try:
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
    finally:
        if temporary.exists():
            temporary.unlink()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--candidate", type=Path, default=HERE / CANDIDATE_NAME)
    parser.add_argument("--output", type=Path, default=HERE / OUTPUT_NAME)
    parser.add_argument("--no-write", action="store_true")
    args = parser.parse_args()

    model = build_model()
    expected = prepare_expected(model)
    del model
    gc.collect()
    raw = check_plain_file(args.candidate, CANDIDATE_NAME, MAX_JSON_BYTES)
    document = strict_json_bytes(raw, CANDIDATE_NAME)
    need(set(document) == {"schema", "result", "result_sha256"}, "candidate envelope")
    need(document["schema"] == SCHEMA, "candidate schema")
    need(digest(document["result"]) == document["result_sha256"], "candidate result digest")
    summary = verify_result(document["result"], expected)
    verification = {
        "status": "PASS_INDEPENDENT_ROUND230",
        **summary,
        "candidate_sha256": hashlib.sha256(raw).hexdigest(),
        "candidate_result_sha256": document["result_sha256"],
        "verifier_sha256": hashlib.sha256(check_plain_file(
            Path(__file__), Path(__file__).name, 5_000_000
        )).hexdigest(),
        "strict_json_checks": "PASS",
        "path_and_regular_file_checks": "PASS",
        "semantic_nonpromotion_checks": "PASS",
    }
    output_document = {
        "schema": "cm2.round230.source-g-resolved-retained-bulk-continuation-verification.v1",
        "result": verification,
        "result_sha256": digest(verification),
    }
    encoded = (canonical(output_document) + "\n").encode("utf-8")
    if not args.no_write:
        safe_write(args.output, encoded)
    print("PASS_INDEPENDENT_ROUND230")
    print(f"candidate_sha256={verification['candidate_sha256']}")
    print(f"verification_result_sha256={output_document['result_sha256']}")
    print("interfaces=8960 accepted=784 rejected=740 delta=464")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
