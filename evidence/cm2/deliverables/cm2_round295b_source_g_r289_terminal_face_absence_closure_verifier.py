#!/usr/bin/env python3
"""Independent cacheless verifier for Round295-B.

Neither the Round295-B producer nor any historical R293 producer/result/ledger
is imported, executed, or used as an oracle.  From frozen Round268/275/280/
282/283 inputs this verifier first reconstructs all 9,528 Round289 relation
rectangles.  It then independently rebuilds the terminal registry cover and
wrong-signed empty cells from Round174/179/286/287/288/292A plus the sealed
Round294 contract, constructs the complete expected four-table Round295-B
object, and only afterward opens the candidate result and ledger.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from copy import deepcopy
from fractions import Fraction as Q
import gzip
import hashlib
import io
import json
import os
from pathlib import Path
import tempfile
from typing import Any, Callable, Iterable


HERE = Path(__file__).resolve().parent
PREFIX = "cm2_round295b_source_g_r289_terminal_face_absence_closure"
PRODUCER = HERE / f"{PREFIX}.py"
RESULT = HERE / f"{PREFIX}_result.json"
LEDGER = HERE / f"{PREFIX}_ledger.json.gz"
OUTPUT = HERE / f"{PREFIX}_verification.json"

FILES = {
    "R174": "cm2_round174_source_g_unique_first_dynamic_occurrence_materialization_rows.json",
    "R179": "cm2_round179_source_g_residual_tube_arrangement_rows.json",
    "R268": "cm2_round268_source_g_true_seam_candidate_geometry_exhaustion_certificate.json",
    "R275": "cm2_round275_source_g_complete_reverse_rechart_materialization_certificate.json",
    "R280": "cm2_round280_source_g_true_seam_and_rechart_region_incidence_probe_patch_channels.json.gz",
    "R282": "cm2_round282_source_g_strict_true_seam_normal_corridor_probe_ledger.json.gz",
    "R282_RESULT": "cm2_round282_source_g_strict_true_seam_normal_corridor_probe_result.json",
    "R283": "cm2_round283_source_g_outgoing_seam_tail_independent_probe_ledger.json.gz",
    "R283_RESULT": "cm2_round283_source_g_outgoing_seam_tail_independent_probe_result.json",
    "R286": "cm2_round286_source_g_partial_overlap_exact_refinement_probe_ledger.json.gz",
    "R286_RESULT": "cm2_round286_source_g_partial_overlap_exact_refinement_probe_result.json",
    "R286_VERIFICATION": "cm2_round286_source_g_partial_overlap_exact_refinement_probe_verification.json",
    "R287": "cm2_round287_source_g_rechart_terminal_occurrence_disposition_probe_ledger.json.gz",
    "R287_RESULT": "cm2_round287_source_g_rechart_terminal_occurrence_disposition_probe_result.json",
    "R287_VERIFICATION": "cm2_round287_source_g_rechart_terminal_occurrence_disposition_probe_verification.json",
    "R288": "cm2_round288_source_g_canonical_atom_occurrence_identity_gate_audit_atom_dispositions.json.gz",
    "R288_RESULT": "cm2_round288_source_g_canonical_atom_occurrence_identity_gate_audit_result.json",
    "R288_VERIFICATION": "cm2_round288_source_g_canonical_atom_occurrence_identity_gate_audit_verification.json",
    "R289": "cm2_round289_source_g_outgoing_seam_tail_child_materialization_ledger.json.gz",
    "R289_RESULT": "cm2_round289_source_g_outgoing_seam_tail_child_materialization_result.json",
    "R289_VERIFICATION": "cm2_round289_source_g_outgoing_seam_tail_child_materialization_verification.json",
    "R292A": "cm2_round292_source_g_r287_registry_overlap_exhaustion_probe_ledger.json.gz",
    "R292A_RESULT": "cm2_round292_source_g_r287_registry_overlap_exhaustion_probe_result.json",
    "R292A_VERIFICATION": "cm2_round292_source_g_r287_registry_overlap_exhaustion_probe_verification.json",
    "R292A_MANIFEST": "cm2_round292_source_g_r287_registry_overlap_exhaustion_probe_manifest.sha256",
}

UPSTREAM_PINS = {
    "R174": "9edeea2e1033b0dd70dee11a53b0f6aeb21fe74030aeefb60b081a7c420cff54",
    "R179": "f20b42c1fed781779b537b4d45bf44233eae1ed3ee620b95177a80f0eb2b5e42",
    "R268": "10d5e42f4353e981e7e8d5aacc002bed119453ee14a13398c524d5cb4ac2f7b9",
    "R275": "e18935169614fc8b62ead3be7f60b383396ea1d2c52e8151457241f49e770386",
    "R280": "074b27dd062844331d2d43a91283f5d467fe957123294719e32237fece05d814",
    "R282": "6d94bce99b3ea57b8a568707705d9f16833cfba28b242a6dabb2de5933f6509e",
    "R282_RESULT": "cd054a7036d9c482357611e9af11d028179e0f34a828dca2fbe91332b178f532",
    "R283": "2643a17cd325a16fabe8508a06b8666811641f837e8c2a2ea8a4a71ab982b786",
    "R283_RESULT": "29a1a48140136f105c2454771afa642794de10c61afc18bfbbefe88f0df70eca",
    "R286": "bb7e28cbe029e2bb414313ec4a08f6366acbbad88a519926ec2a3a424e679eda",
    "R286_RESULT": "a3b705c489eff9df4e1129bcdf960c6ea9de435e326c1d7e040e01d63352d29e",
    "R286_VERIFICATION": "817a212eeac8d855927a617dd07462747c636127e4f4b15ec709f9975a74698e",
    "R287": "29838e3e6b33f03bf623bbce8b87e6ba5c3306e66beb0b6634496503fb9a4f9a",
    "R287_RESULT": "1265475e5d27f99eda35b16f13ba342e0d270ca1bc064df215a018d3ffae89f9",
    "R287_VERIFICATION": "c0ad4d3e229a1e21cb5b4f4144575df7f5eaf88d7fc8a6960967ab4c1db515a3",
    "R288": "6b0a8aa1cd38019322a61f5aaefc936006d10769cd21a5c8df374576f9ac570a",
    "R288_RESULT": "9b5875777f3937efe05a4d871a8c8b76c92ca69d0f636eb014542f59dfe49569",
    "R288_VERIFICATION": "f08749d2f90ea63a696c482a342489c12e2c86436734a59c6a2e2b79d9cf9b23",
    "R289": "6c5680574c17d50749d39fb25970b7fbcbc677f4f73029aca833f549c0ef5001",
    "R289_RESULT": "9091e06b8aca3d5e883621e0e3f701a6b90ce2f02b84f6813cef7727f45c516c",
    "R289_VERIFICATION": "3cd242981e64007e22dccc8deee43418be32a1841bb75de96c4871c89dda691f",
    "R292A": "8863126e88ffd30438938d0a8bdb577f5928ae81f3f17f4b506829d59103a8ab",
    "R292A_RESULT": "f3887e75f4ef62459b75d8c77eee4781ec14f57651b4feb09b8d7ca8e372c508",
    "R292A_VERIFICATION": "7088e4f0927100e3c2b36f164e4f64e7b7aa0db5f81b4201c3967f16ba07ddfd",
    "R292A_MANIFEST": "4ea92e4112cae18aa0c13a6d2308816bafc19e4129c09d8b6be914268cfc4870",
}

ROUND294_PINS = {
    "cm2_round294_source_g_occurrence_registry_atomic_promotion.py":
        "6e0ab06cf6ab7dfb7868b2fe7a4699a914e6a3b0f8b18e4181d138bc2d887a9b",
    "cm2_round294_source_g_occurrence_registry_atomic_promotion_attack_suite.json":
        "aefb50be4969676d752cf8c8cb06f355db508007be4c1ee95f07c305e19a8adb",
    "cm2_round294_source_g_occurrence_registry_atomic_promotion_registry_ledger.json.gz":
        "c6b26f13e90072db99fa98f99fc62c77135ff1cbdb23bbbd5bac3e9f64a834bb",
    "cm2_round294_source_g_occurrence_registry_atomic_promotion_representation_binding_ledger.json.gz":
        "f9fcc986771b1c3551420516cd9f2c5dde662f87d044666d9306404f30bb6833",
    "cm2_round294_source_g_occurrence_registry_atomic_promotion_result.json":
        "dc93ef564ce1aec4aabbc7ff717ac76749b92899e210179a00dba63f2d32d626",
    "cm2_round294_source_g_occurrence_registry_atomic_promotion_verifier.py":
        "154158d7910b1ffa1f71475c4e0505c6ab72ca3ab856a2fa4c27d7e376533aaa",
    "cm2_round294_source_g_occurrence_registry_atomic_promotion_verification.json":
        "13dcb461f269a8e346c220b85cad0e87a0392b5e2682b7dd70132fd8bd7a1245",
    "cm2_round294_source_g_occurrence_registry_atomic_promotion_report.md":
        "37676f39ab54092cd6c57ebd85bc21f9ec1de820ea82a4971998106df5c57114",
    "cm2_round294_source_g_occurrence_registry_atomic_promotion_cold_replay.md":
        "017172cac7075e7b90655ad2883fba2989cd27819c91ab5f04f2358737a7bea9",
    "cm2_round294_source_g_occurrence_registry_atomic_promotion_manifest.sha256":
        "90d5cda0271610bf95a72f94e9bae8e192425580019dd3c823b5a69d20e52131",
}

CANDIDATE_PINS = {
    PRODUCER.name:
        "c970371a5e05a76d22cd41accf98848784413f9ce2c937a3dff47c43b763b86a",
    RESULT.name:
        "b10c5caf9813887b06f2ed49796e02befc8abdc048e6909c2146bfc120e6334a",
    LEDGER.name:
        "1714945c470607a68c9fb5e323319899faabd187ecbccd00d266ea6f9361007c",
}

SCHEMA = "cm2.round295b.source-g-r289-terminal-face-absence-closure.v1"
LEDGER_SCHEMA = SCHEMA + ".ledger.v1"
VERIFICATION_SCHEMA = SCHEMA + ".verification.v1"
EMPTY = "EMPTY_OPPOSITE_SIDE_COORDINATE_CELL"
GRAPH = "REGULAR_P_GRAPH_HALF_OPEN_OWNER"
STRICT_ABSENCE = "STRICT_ZERO_ABSENT"
POSITIVE = "STRICT_POSITIVE"
NEGATIVE = "STRICT_NEGATIVE"


class VerificationError(RuntimeError):
    pass


def need(condition: bool, message: str) -> None:
    if not condition:
        raise VerificationError(message)


def canonical(value: Any) -> bytes:
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=True
    ).encode()


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def file_sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def read_json_key(key: str) -> dict[str, Any]:
    with (HERE / FILES[key]).open("rb") as handle:
        value = json.load(handle)
    need(isinstance(value, dict), f"JSON object:{FILES[key]}")
    return value


def read_gzip_key(key: str) -> dict[str, Any]:
    with gzip.open(HERE / FILES[key], "rt", encoding="utf-8") as handle:
        value = json.load(handle)
    need(isinstance(value, dict), f"gzip JSON object:{FILES[key]}")
    return value


def read_gzip_bytes(payload: bytes) -> dict[str, Any]:
    value = json.loads(gzip.decompress(payload))
    need(isinstance(value, dict), "candidate gzip JSON object")
    return value


def close(payload: dict[str, Any]) -> dict[str, Any]:
    row = dict(payload)
    row["row_sha256"] = digest(payload)
    return row


def verify_row(row: dict[str, Any], label: str) -> None:
    payload = {key: value for key, value in row.items() if key != "row_sha256"}
    need(
        set(row) == set(payload) | {"row_sha256"}
        and row["row_sha256"] == digest(payload),
        f"{label}:row closure",
    )


def verify_table(
    document: dict[str, Any],
    rows_key: str,
    count_key: str,
    hash_key: str,
) -> list[dict[str, Any]]:
    rows = document[rows_key]
    need(
        len(rows) == document[count_key]
        and digest(rows) == document[hash_key],
        f"{rows_key}:table closure",
    )
    for row in rows:
        verify_row(row, rows_key)
    return rows


def verify_nested(
    table: dict[str, Any], id_key: str, count: int, label: str
) -> list[dict[str, Any]]:
    rows = table["rows"]
    need(
        len(rows) == table["row_count"] == count
        and digest(rows) == table["rows_sha256"],
        f"{label}:rows closure",
    )
    ids = [row[id_key] for row in rows]
    hashes = []
    for row in rows:
        verify_row(row, label)
        hashes.append(row["row_sha256"])
    need(
        len(ids) == len(set(ids))
        and digest(ids) == table["row_ids_sha256"]
        and digest(hashes) == table["row_hashes_sha256"],
        f"{label}:ID/hash closure",
    )
    return rows


def verify_result(value: dict[str, Any], field: str, label: str) -> None:
    claim = value[field]
    payload = {key: child for key, child in value.items() if key != field}
    need(claim == digest(payload), f"{label}:{field} closure")


def unpack(document: dict[str, Any], table: str) -> list[dict[str, Any]]:
    result = document["result"]
    rows = result[table]
    census = result["table_census_and_sha256"][table]
    need(
        len(rows) == census["row_count"]
        and digest(rows) == census["rows_sha256"],
        f"packed table:{table}",
    )
    return [
        dict(zip(result["row_column_schemas"][table], row, strict=True))
        for row in rows
    ]


def qbox(values: Iterable[str]) -> tuple[Q, ...]:
    result = tuple(map(Q, values))
    need(
        len(result) == 6
        and all(result[2 * axis] < result[2 * axis + 1] for axis in range(3)),
        "positive rational box",
    )
    return result


def qstr(value: Q) -> str:
    return str(value.numerator) if value.denominator == 1 else str(value)


def square_interval(lo: Q, hi: Q) -> tuple[Q, Q]:
    need(lo * hi > 0, "strict signed t interval")
    return (lo * lo, hi * hi) if lo > 0 else (hi * hi, lo * lo)


def physical_t_square(
    coordinate_box: tuple[Q, ...], guard_box: tuple[Q, ...]
) -> tuple[Q, Q]:
    coordinate = square_interval(coordinate_box[0], coordinate_box[1])
    source = square_interval(guard_box[0], guard_box[1])
    image = (1 - source[1], 1 - source[0])
    result = max(coordinate[0], image[0]), min(coordinate[1], image[1])
    need(result[0] < result[1], "positive exact physical t-square")
    return result


def intersect_rect(
    left: tuple[Q, Q, Q, Q],
    right: tuple[Q, Q, Q, Q],
) -> tuple[Q, Q, Q, Q] | None:
    hit = (
        max(left[0], right[0]),
        min(left[1], right[1]),
        max(left[2], right[2]),
        min(left[3], right[3]),
    )
    return hit if hit[0] < hit[1] and hit[2] < hit[3] else None


def rect_area(rectangle: tuple[Q, Q, Q, Q]) -> Q:
    return (
        (rectangle[1] - rectangle[0])
        * (rectangle[3] - rectangle[2])
    )


def union_area(rectangles: Iterable[tuple[Q, Q, Q, Q]]) -> Q:
    rectangles = sorted(set(rectangles))
    if not rectangles:
        return Q(0)
    cuts = sorted({value for row in rectangles for value in row[:2]})
    total = Q(0)
    for p0, p1 in zip(cuts, cuts[1:]):
        spans = sorted(
            (row[2], row[3])
            for row in rectangles
            if row[0] <= p0 and p1 <= row[1]
        )
        merged: list[list[Q]] = []
        for s0, s1 in spans:
            if not merged or merged[-1][1] < s0:
                merged.append([s0, s1])
            else:
                merged[-1][1] = max(merged[-1][1], s1)
        total += (p1 - p0) * sum(s1 - s0 for s0, s1 in merged)
    return total


def deterministic_gzip_bytes(value: Any) -> bytes:
    output = io.BytesIO()
    with gzip.GzipFile(
        filename="", mode="wb", fileobj=output, mtime=0
    ) as handle:
        handle.write(canonical(value))
    return output.getvalue()


def table(rows: list[dict[str, Any]], id_key: str) -> dict[str, Any]:
    return {
        "row_count": len(rows),
        "rows_sha256": digest(rows),
        "row_ids_sha256": digest([row[id_key] for row in rows]),
        "row_hashes_sha256": digest([row["row_sha256"] for row in rows]),
        "rows": rows,
    }


def atomic_write(path: Path, payload: bytes) -> None:
    descriptor, temporary = tempfile.mkstemp(
        prefix="." + path.name + ".", dir=path.parent
    )
    try:
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(payload)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def load_relation_upstream() -> tuple[
    dict[str, dict[str, Any]],
    list[dict[str, Any]],
    dict[str, dict[str, Any]],
]:
    r268 = read_json_key("R268")
    need(
        r268["result_sha256"] == digest(r268["result"]),
        "Round268 result closure",
    )
    patch_rows = verify_nested(
        r268["result"]["formal_true_source_seam_positive_patch_ledger"],
        "true_seam_patch_row_id",
        152,
        "Round268 patches",
    )
    patch_ids = {row["true_seam_patch_row_id"] for row in patch_rows}

    r275 = read_json_key("R275")
    need(
        r275["result_sha256"] == digest(r275["result"]),
        "Round275 result closure",
    )
    regions: dict[str, dict[str, Any]] = {}
    for name, count in (
        ("strict_region_ledger", 5_288),
        ("arrangement_region_ledger", 8_500),
    ):
        for row in verify_nested(
            r275["result"][name],
            "reverse_rechart_region_row_id",
            count,
            "Round275:" + name,
        ):
            regions[row["reverse_rechart_region_row_id"]] = row
    need(len(regions) == 13_788, "Round275 region universe")

    r280 = read_gzip_key("R280")
    channel_rows = verify_nested(
        r280, "Round268_patch_channel_row_id", 152, "Round280 channels"
    )
    channels = {
        row["Round268_true_seam_patch_row_id"]: row for row in channel_rows
    }
    need(set(channels) == patch_ids, "Round280 patch universe")

    r282_result = read_json_key("R282_RESULT")
    verify_result(r282_result, "result_sha256", "Round282")
    r282 = read_gzip_key("R282")
    corridor_rows = verify_nested(
        r282, "Round282_seam_corridor_row_id", 152, "Round282 corridors"
    )
    corridors = {
        row["Round268_true_seam_patch_row_id"]: row
        for row in corridor_rows
    }
    need(set(corridors) == patch_ids, "Round282 patch universe")
    partial_sides = {
        (row["Round268_true_seam_patch_row_id"], index)
        for row in corridor_rows
        for index, side in enumerate(row["side_corridors"])
        if side["classification"]
        == "PARTIAL_STRICT_COVER__ARRANGEMENT_TAIL_FAIL_CLOSED"
    }
    need(len(partial_sides) == 40, "Round282 partial directed endpoints")

    r283_result = read_json_key("R283_RESULT")
    verify_result(r283_result, "result_sha256", "Round283")
    r283 = read_gzip_key("R283")
    endpoints = verify_nested(
        r283, "Round283_endpoint_row_id", 40, "Round283 endpoints"
    )
    need(
        {
            (row["Round268_true_seam_patch_row_id"], row["side_index"])
            for row in endpoints
        } == partial_sides,
        "Round283/Round282 endpoint universe",
    )
    need(
        sum(row["candidate_guard_channel_count"] for row in endpoints) == 48
        and sum(
            row["Round282_residual_rational_cell_count"]
            for row in endpoints
        ) == 540,
        "Round283 endpoint census",
    )
    for endpoint in endpoints:
        patch_id = endpoint["Round268_true_seam_patch_row_id"]
        side_index = endpoint["side_index"]
        side280 = channels[patch_id]["side_channel_rows"][side_index]
        side282 = corridors[patch_id]["side_corridors"][side_index]
        need(
            endpoint["side"] == side280["side"] == side282["side"]
            and endpoint["source_chart"]
            == side280["source_chart"] == side282["source_chart"]
            and endpoint["adjacent_chart"]
            == side280["adjacent_chart"] == side282["adjacent_chart"],
            "endpoint side-channel identity",
        )
        cells = [
            tuple(map(Q, cell))
            for cell in endpoint["Round282_residual_rational_cells"]
        ]
        need(
            len(cells) == endpoint["Round282_residual_rational_cell_count"]
            and all(rect_area(cell) > 0 for cell in cells),
            "Round283 positive residual cells",
        )
        for index, left in enumerate(cells):
            for right in cells[index + 1:]:
                need(
                    intersect_rect(left, right) is None,
                    "Round283 residual interiors disjoint",
                )
    return regions, endpoints, channels


def derive_children(
    endpoint: dict[str, Any], guard: dict[str, Any]
) -> list[dict[str, Any]]:
    patch = tuple(map(Q, endpoint["patch_ps_rectangle"]))
    common = {
        "source_guard_row_id": guard["source_guard_row_id"],
        "source_round": guard["source_round"],
        "parent_id": guard["parent_id"],
        "owner_target": guard["owner_target"],
        "source_chart": guard["source_chart"],
        "adjacent_chart": guard["adjacent_chart"],
        "algebraic_root_sign": guard["algebraic_root_sign"],
        "normal_gap_outer_box": guard["normal_gap_outer_box"],
        "whole_gap_derivative_signs_t_p_s":
            guard["whole_gap_derivative_signs_t_p_s"],
        "sole_dynamic_gap_reason": guard["sole_dynamic_gap_reason"],
    }
    classification = guard["classification"]
    if classification == "FULL_S_BASE_REGULAR_P_GRAPH":
        need(
            set(guard["seam_p_face_signs"]) == {NEGATIVE, POSITIVE},
            "full graph signs",
        )
        return [{
            **common,
            "_rectangle": patch,
            "child_classification": GRAPH,
            "strict_absence_sign": None,
        }]
    if classification == STRICT_ABSENCE:
        need(
            len(set(guard["seam_p_face_signs"])) == 1,
            "whole absence sign",
        )
        return [{
            **common,
            "_rectangle": patch,
            "child_classification": STRICT_ABSENCE,
            "strict_absence_sign": guard["seam_p_face_signs"][0],
        }]
    need(
        classification == "P_ENDPOINT_REGULAR_GRAPH__EXACT_S0_SPLIT"
        and len(guard["half_open_split_rows"]) == 2,
        "split guard",
    )
    result = []
    for split in guard["half_open_split_rows"]:
        s0, s1 = map(Q, split["half_open_s_interval"])
        is_graph = split["classification"] == GRAPH
        signs = split["p_face_signs_at_witness"]
        need(
            (is_graph and set(signs) == {NEGATIVE, POSITIVE})
            or (
                not is_graph
                and split["classification"] == STRICT_ABSENCE
                and len(set(signs)) == 1
            ),
            "split signs",
        )
        result.append({
            **common,
            "_rectangle": (patch[0], patch[1], s0, s1),
            "child_classification": split["classification"],
            "strict_absence_sign": None if is_graph else signs[0],
        })
    return result


def outgoing_sign(region: dict[str, Any]) -> str:
    outgoing = region["local_return_signature"]["outgoing_cell"]
    sign = POSITIVE if outgoing in {"E", "W"} else NEGATIVE
    if "active_factor_side_sign" in region:
        need(
            region["active_factor_side_sign"] == sign
            and region["active_reason"] == "outgoing_chart_seam",
            "Round275 outgoing sign",
        )
    return sign


def independently_reconstruct_r289_relations(
    regions: dict[str, dict[str, Any]],
    endpoints: list[dict[str, Any]],
    channels: dict[str, dict[str, Any]],
) -> list[dict[str, Any]]:
    children: dict[str, dict[str, Any]] = {}
    by_guard: dict[tuple[str, int, str], list[str]] = defaultdict(list)
    endpoint_children: dict[str, list[str]] = defaultdict(list)
    split_count = 0
    for endpoint in endpoints:
        patch_id = endpoint["Round268_true_seam_patch_row_id"]
        side_index = endpoint["side_index"]
        for guard in endpoint["guard_channel_rows"]:
            templates = derive_children(endpoint, guard)
            split_count += int(len(templates) == 2)
            for template_index, template in enumerate(templates):
                rectangle = template["_rectangle"]
                child_id = "round289-tail-child:" + digest([
                    patch_id,
                    side_index,
                    template["source_guard_row_id"],
                    template_index,
                    [qstr(value) for value in rectangle],
                    template["child_classification"],
                ])
                need(child_id not in children, "unique reconstructed child")
                template["Round289_tail_child_row_id"] = child_id
                children[child_id] = template
                by_guard[
                    (patch_id, side_index, template["source_guard_row_id"])
                ].append(child_id)
                endpoint_children[
                    endpoint["Round283_endpoint_row_id"]
                ].append(child_id)
    need(
        len(children) == 64 and split_count == 16,
        "reconstructed child/split census",
    )

    rows: list[dict[str, Any]] = []
    disposition_histogram: Counter[str] = Counter()
    sign_histogram: Counter[tuple[bool, str]] = Counter()
    for endpoint in endpoints:
        patch_id = endpoint["Round268_true_seam_patch_row_id"]
        side_index = endpoint["side_index"]
        channel = channels[patch_id]["side_channel_rows"][side_index]
        for region_id in channel["candidate_Round275_region_ids"]:
            region = regions[region_id]
            box = qbox(region["adjacent_rational_region_box"])
            footprint = (box[2], box[3], box[4], box[5])
            for residual_index, raw_residual in enumerate(
                endpoint["Round282_residual_rational_cells"]
            ):
                residual = tuple(map(Q, raw_residual))
                overlap = intersect_rect(footprint, residual)
                if overlap is None:
                    continue
                possible = by_guard.get(
                    (patch_id, side_index, region["source_guard_row_id"]),
                    [],
                )
                matching = [
                    child_id for child_id in possible
                    if intersect_rect(
                        children[child_id]["_rectangle"], overlap
                    ) is not None
                ]
                need(len(matching) == 1, "one child per relation")
                child_id = matching[0]
                child = children[child_id]
                sign = outgoing_sign(region)
                actual = (
                    child["child_classification"] == GRAPH
                    or sign == child["strict_absence_sign"]
                )
                disposition = (
                    "ACTUAL_INCIDENT_R275_REGION__SAME_SIGN_CONNECTED_GAP"
                    if actual
                    else
                    "NOT_SEAM_INCIDENT__SEPARATED_BY_REGULAR_OUTGOING_GRAPH"
                )
                relation_id = "round289-region-cell-incidence:" + digest([
                    endpoint["Round283_endpoint_row_id"],
                    child_id,
                    region_id,
                    residual_index,
                ])
                rows.append(close({
                    "Round289_region_cell_relation_id": relation_id,
                    "Round289_tail_child_row_id": child_id,
                    "Round283_endpoint_row_id":
                        endpoint["Round283_endpoint_row_id"],
                    "Round268_true_seam_patch_row_id": patch_id,
                    "side_index": side_index,
                    "source_guard_row_id": region["source_guard_row_id"],
                    "Round275_region_id": region_id,
                    "Round275_region_classification":
                        region.get("region_classification")
                        or region["arrangement_classification"],
                    "Round282_residual_cell_index": residual_index,
                    "exact_positive_ps_overlap":
                        list(map(qstr, overlap)),
                    "exact_positive_ps_overlap_area":
                        qstr(rect_area(overlap)),
                    "active_outgoing_equality_sign": sign,
                    "complete_10_field_return_signature_sha256":
                        region[
                            "complete_10_field_return_signature_sha256"
                        ],
                    "disposition": disposition,
                    "actual_seam_incidence": actual,
                    "occurrence_credit": 0,
                    "component_edge_credit": 0,
                }))
                disposition_histogram[disposition] += 1
                sign_histogram[(actual, sign)] += 1
    rows.sort(key=lambda row: row["Round289_region_cell_relation_id"])
    need(
        len(rows) == 9_528
        and disposition_histogram
        == {
            "ACTUAL_INCIDENT_R275_REGION__SAME_SIGN_CONNECTED_GAP":
                9_240,
            "NOT_SEAM_INCIDENT__SEPARATED_BY_REGULAR_OUTGOING_GRAPH":
                288,
        }
        and sign_histogram
        == {
            (True, NEGATIVE): 4_588,
            (True, POSITIVE): 4_652,
            (False, NEGATIVE): 144,
            (False, POSITIVE): 144,
        },
        "independent Round289 relation census",
    )

    # R289 is an upstream seal, not the current candidate.  It is opened only
    # after every expected relation row has been reconstructed.
    frozen = read_gzip_key("R289")
    frozen_rows = verify_nested(
        frozen["region_cell_relation_ledger"],
        "Round289_region_cell_relation_id",
        9_528,
        "frozen Round289 relations",
    )
    need(
        rows == frozen_rows,
        "frozen Round289 relation table differs from reconstruction",
    )
    return rows


def verify_round294_package() -> dict[str, Any]:
    for filename, expected in ROUND294_PINS.items():
        need(
            expected != "PENDING_ROUND294_FINAL_SEAL"
            and file_sha256(HERE / filename) == expected,
            f"Round294 final package pin:{filename}",
        )
    with (
        HERE
        / "cm2_round294_source_g_occurrence_registry_atomic_promotion_result.json"
    ).open("rb") as handle:
        result = json.load(handle)
    verify_result(result, "result_sha256", "Round294")
    with (
        HERE
        / (
            "cm2_round294_source_g_occurrence_registry_atomic_promotion_"
            "verification.json"
        )
    ).open("rb") as handle:
        verification = json.load(handle)
    verify_result(verification, "verification_sha256", "Round294 verification")
    need(
        verification["status"].startswith(
            "PASS_INDEPENDENT_CACHELESS_ROUND294"
        )
        and result["census"]["formal_occurrence_registry_row_count"]
        == 431_208
        and result["census"]["formal_representation_binding_count"]
        == 46_288
        and result["nonpromotion_freeze"][
            "post_Round294_quotient_component_count"
        ] is None
        and result["nonpromotion_freeze"][
            "post_Round294_expanded_registry_component_DSU_status"
        ] == "NOT_REBUILT",
        "sealed Round294 registry/non-DSU contract",
    )
    return result


def reconstruct_terminal_inputs(
    regions: dict[str, dict[str, Any]],
) -> tuple[
    dict[str, list[dict[str, Any]]],
    dict[str, list[dict[str, Any]]],
    dict[str, Q],
    dict[str, str],
    dict[str, dict[str, Any]],
]:
    guards: dict[str, dict[str, Any]] = {}
    for key, table_name in (
        ("R174", "chart_guard_rejection_rows"),
        ("R179", "chart_guard_child_rows"),
    ):
        for row in unpack(read_json_key(key), table_name):
            need(row["row_id"] not in guards, "unique guard ID")
            guards[row["row_id"]] = row
    need(
        len(guards) == 880
        and all(region["source_guard_row_id"] in guards for region in regions.values()),
        "source guard universe",
    )

    r286 = read_gzip_key("R286")
    r286_rows = verify_table(r286, "rows", "row_count", "rows_sha256")
    need(len(r286_rows) == 7_616, "Round286 cell census")
    r286_by_id = {
        row["Round286_refinement_cell_id"]: row for row in r286_rows
    }

    r287 = read_gzip_key("R287")
    region_rows = verify_table(
        r287, "region_rows", "region_row_count", "region_rows_sha256"
    )
    cell_rows = verify_table(
        r287,
        "refinement_cell_rows",
        "refinement_cell_row_count",
        "refinement_cell_rows_sha256",
    )
    need(
        len(region_rows) == 13_788 and len(cell_rows) == 7_616,
        "Round287 disposition census",
    )

    r288 = read_gzip_key("R288")
    atom_rows = verify_table(r288, "rows", "row_count", "rows_sha256")
    need(len(atom_rows) == 332_016, "Round288 atom census")
    atoms = {row["canonical_atom_id"]: row for row in atom_rows}
    target_kind: dict[str, str] = {}
    for atom in atom_rows:
        target = (
            atom["existing_local_occurrence_row_id"]
            or atom["reserved_candidate_occurrence_id__not_issued"]
        )
        need(target is not None, "Round288 final/reserved target")
        kind = (
            "ROUND294_PRESERVED_EXISTING_OCCURRENCE"
            if atom["existing_local_occurrence_row_id"]
            else "ROUND294_PROMOTED_ROUND288_CANONICAL_ATOM"
        )
        target_kind[target] = kind

    support: dict[str, list[dict[str, Any]]] = defaultdict(list)
    empty: dict[str, list[dict[str, Any]]] = defaultdict(list)
    upper: dict[str, Q] = {}
    for disposition in region_rows:
        region_id = disposition["Round275_region_id"]
        region = regions[region_id]
        coordinate = qbox(region["adjacent_rational_region_box"])
        recomputed = physical_t_square(
            coordinate,
            qbox(guards[region["source_guard_row_id"]]["box"]),
        )
        need(
            recomputed
            == tuple(map(
                Q, disposition["physical_t_square_open_interval"]
            )),
            "whole-region physical t-square reconstruction",
        )
        upper[region_id] = recomputed[1]
        if disposition["disposition"].startswith("EXACT_INCLUSION_ALIAS_"):
            atom = atoms[disposition["containing_atom_id"]]
            target = (
                atom["existing_local_occurrence_row_id"]
                or atom["reserved_candidate_occurrence_id__not_issued"]
            )
            support[region_id].append({
                "physical_t_square": recomputed,
                "ps_rectangle": (
                    coordinate[2],
                    coordinate[3],
                    coordinate[4],
                    coordinate[5],
                ),
                "target_ids": [target],
                "source_kind":
                    "ROUND287_WHOLE_REGION_INCLUSION_REPRESENTATION",
                "source_row_id":
                    disposition["Round287_region_disposition_row_id"],
            })

    for disposition in cell_rows:
        cell_id = disposition["Round286_refinement_cell_id"]
        source = r286_by_id[cell_id]
        need(
            source["Round275_region_id"]
            == disposition["Round275_region_id"]
            and source["cell_exact_box"] == disposition["coordinate_box"]
            and source["atom_occupancy_count"]
            == disposition["Round286_coordinate_occupancy_count"],
            "Round286/Round287 exact cell join",
        )
        region_id = disposition["Round275_region_id"]
        region = regions[region_id]
        coordinate = qbox(source["cell_exact_box"])
        recomputed = physical_t_square(
            coordinate,
            qbox(guards[region["source_guard_row_id"]]["box"]),
        )
        need(
            recomputed
            == tuple(map(
                Q, disposition["physical_t_square_open_interval"]
            )),
            "cell physical t-square reconstruction",
        )
        ps = (
            coordinate[2],
            coordinate[3],
            coordinate[4],
            coordinate[5],
        )
        if disposition["signed_region_cell_state"] == EMPTY:
            extrema = disposition["active_factor_extremal_signs"]
            desired = region["active_factor_side_sign"]
            need(
                extrema[0] == extrema[1]
                and extrema[0] in {NEGATIVE, POSITIVE}
                and extrema[0] != desired
                and not disposition[
                    "exact_inclusion_alias_lemma_satisfied"
                ],
                "strict empty opposite-side cell",
            )
            empty[region_id].append({
                "Round286_refinement_cell_id": cell_id,
                "Round287_refinement_cell_disposition_row_id":
                    disposition[
                        "Round287_refinement_cell_disposition_row_id"
                    ],
                "coordinate_box": coordinate,
                "physical_t_square": recomputed,
                "ps_rectangle": ps,
                "desired_active_factor_side_sign": desired,
                "active_factor_extremal_signs": extrema,
                "Round286_coordinate_occupancy_count":
                    disposition["Round286_coordinate_occupancy_count"],
                "containing_atom_id": disposition["containing_atom_id"],
            })
        elif disposition["disposition"].startswith(
            "EXACT_INCLUSION_ALIAS_"
        ):
            atom = atoms[disposition["containing_atom_id"]]
            target = (
                atom["existing_local_occurrence_row_id"]
                or atom["reserved_candidate_occurrence_id__not_issued"]
            )
            support[region_id].append({
                "physical_t_square": recomputed,
                "ps_rectangle": ps,
                "target_ids": [target],
                "source_kind":
                    "ROUND287_SIGNED_CELL_INCLUSION_REPRESENTATION",
                "source_row_id":
                    disposition[
                        "Round287_refinement_cell_disposition_row_id"
                    ],
            })

    r292 = read_gzip_key("R292A")
    r292_rows = verify_table(r292, "rows", "row_count", "rows_sha256")
    need(len(r292_rows) == 22_820, "Round292A row census")
    refinements = [
        row for row in r292_rows if row.get("disposition") is not None
    ]
    need(len(refinements) == 11_852, "Round292A refinement census")
    for row in refinements:
        box = tuple(map(Q, row["exact_transformed_open_cell"]))
        if row["existing_occurrence_occupancy_count"]:
            targets = row["existing_occurrence_ids"]
            for target in targets:
                target_kind.setdefault(
                    target, "ROUND294_EXISTING_REGISTRY_OCCURRENCE"
                )
            source_kind = "ROUND292A_EXISTING_REGISTRY_SUBCOVER"
        else:
            target = row["Round292_refined_new_support_component_id"]
            need(target is not None, "Round292A component target")
            targets = [target]
            target_kind[target] = (
                "ROUND294_PROMOTED_ROUND292_REFINED_SUPPORT_COMPONENT"
            )
            source_kind = "ROUND292A_REFINED_NEW_SUPPORT_COMPONENT"
        support[row["Round275_region_id"]].append({
            "physical_t_square": (box[0], box[1]),
            "ps_rectangle": (box[2], box[3], box[4], box[5]),
            "target_ids": targets,
            "source_kind": source_kind,
            "source_row_id":
                row["Round292_R287_existing_overlap_refinement_cell_id"],
        })
    need(
        all(
            target in target_kind
            for cells in support.values()
            for cell in cells
            for target in cell["target_ids"]
        ),
        "all terminal targets formal after Round294",
    )
    return support, empty, upper, target_kind, guards


def independently_build_expected(
    relations: list[dict[str, Any]],
    regions: dict[str, dict[str, Any]],
    support_by_region: dict[str, list[dict[str, Any]]],
    empty_by_region: dict[str, list[dict[str, Any]]],
    upper_by_region: dict[str, Q],
    target_kind: dict[str, str],
    guards: dict[str, dict[str, Any]],
    round294: dict[str, Any],
) -> tuple[dict[str, Any], dict[str, Any]]:
    """Build the complete expected candidate without reading the candidate."""
    physical_rows: list[dict[str, Any]] = []
    graph_rows: list[dict[str, Any]] = []
    raw_absence_pieces: list[dict[str, Any]] = []
    raw_relations: list[dict[str, Any]] = []
    baseline_histogram: Counter[str] = Counter()
    corrected_histogram: Counter[str] = Counter()
    gap_multiplicity: Counter[int] = Counter()
    actual_target_reference_count = 0
    actual_relation_area = Q(0)
    graph_relation_area = Q(0)
    physical_area_total = Q(0)
    empty_area_total = Q(0)

    for relation in relations:
        relation_id = relation["Round289_region_cell_relation_id"]
        rectangle = tuple(map(Q, relation["exact_positive_ps_overlap"]))
        relation_area = rect_area(rectangle)
        need(
            relation_area == Q(relation["exact_positive_ps_overlap_area"]),
            "reconstructed relation area",
        )
        common = {
            "Round289_region_cell_relation_id": relation_id,
            "Round268_true_seam_patch_row_id":
                relation["Round268_true_seam_patch_row_id"],
            "side_index": relation["side_index"],
            "Round275_region_id": relation["Round275_region_id"],
            "exact_relation_ps_rectangle": list(map(qstr, rectangle)),
            "exact_relation_ps_area": qstr(relation_area),
        }
        if not relation["actual_seam_incidence"]:
            baseline_histogram["GRAPH_SEPARATED"] += 1
            corrected_histogram["GRAPH_SEPARATED_ABSENCE"] += 1
            graph_relation_area += relation_area
            proof_id = (
                "round295b-r289-graph-separated-no-binding:"
                + digest(relation_id)
            )
            graph_rows.append(close({
                "Round295B_graph_separated_no_binding_row_id": proof_id,
                **common,
                "source_Round289_disposition": relation["disposition"],
                "no_binding_classification":
                    "REGULAR_OUTGOING_GRAPH_SEPARATES_TERMINAL_FACE",
                "terminal_registry_target_reference_count": 0,
                "terminal_registry_target_references": [],
                "formal_existing_physical_incidence_binding_credit": 0,
                "formal_new_occurrence_credit": 0,
                "formal_representation_alias_credit": 0,
                "formal_seam_edge_credit": 0,
                "formal_component_union_credit": 0,
                "formal_DSU_rank_reduction_credit": 0,
                "formal_maximality_credit": 0,
                "formal_fibre_credit": 0,
                "formal_global_disposition_credit": 0,
                "Jx_Jy_same_point_glue_credit": 0,
            }))
            raw_relations.append({
                **common,
                "source_relation_classification": "GRAPH_SEPARATED",
                "corrected_relation_disposition":
                    "GRAPH_SEPARATED_ABSENCE__NO_BINDING",
                "physical_row_ids": [],
                "physical_target_ids": [],
                "absence_piece_keys": [],
                "graph_no_binding_proof_ids": [proof_id],
                "physical_area": Q(0),
                "empty_area": Q(0),
                "graph_area": relation_area,
            })
            continue

        actual_relation_area += relation_area
        region_id = relation["Round275_region_id"]
        upper = upper_by_region[region_id]
        terminal_cells = [
            cell for cell in support_by_region.get(region_id, [])
            if cell["physical_t_square"][1] == upper
            and intersect_rect(rectangle, cell["ps_rectangle"]) is not None
        ]
        p_cuts = {rectangle[0], rectangle[1]}
        s_cuts = {rectangle[2], rectangle[3]}
        for cell in terminal_cells:
            hit = intersect_rect(rectangle, cell["ps_rectangle"])
            need(hit is not None, "expected terminal support overlap")
            p_cuts.update(hit[:2])
            s_cuts.update(hit[2:])

        bound_rectangles: list[tuple[Q, Q, Q, Q]] = []
        gap_rectangles: list[tuple[Q, Q, Q, Q]] = []
        relation_physical_ids: list[str] = []
        relation_targets: set[str] = set()
        sorted_p = sorted(p_cuts)
        sorted_s = sorted(s_cuts)
        for p0, p1 in zip(sorted_p, sorted_p[1:]):
            for s0, s1 in zip(sorted_s, sorted_s[1:]):
                subcell = (p0, p1, s0, s1)
                midpoint = ((p0 + p1) / 2, (s0 + s1) / 2)
                covering = [
                    cell for cell in terminal_cells
                    if cell["ps_rectangle"][0] < midpoint[0]
                    < cell["ps_rectangle"][1]
                    and cell["ps_rectangle"][2] < midpoint[1]
                    < cell["ps_rectangle"][3]
                ]
                targets = sorted({
                    target
                    for cell in covering
                    for target in cell["target_ids"]
                })
                if not targets:
                    gap_rectangles.append(subcell)
                    continue
                need(len(targets) == 1, "expected unique target subcell")
                target = targets[0]
                need(target in target_kind, "expected formal target")
                source_refs = sorted({
                    cell["source_kind"] + ":" + cell["source_row_id"]
                    for cell in covering
                    if target in cell["target_ids"]
                })
                row_id = (
                    "round295b-r289-physical-incidence-binding:"
                    + digest([
                        relation_id,
                        list(map(qstr, subcell)),
                        target,
                    ])
                )
                physical_rows.append(close({
                    "Round295B_physical_incidence_binding_row_id": row_id,
                    **common,
                    "terminal_face_physical_t_square": qstr(upper),
                    "exact_physical_ps_subcell":
                        list(map(qstr, subcell)),
                    "exact_physical_ps_area": qstr(rect_area(subcell)),
                    "formal_Round294_occurrence_id": target,
                    "formal_Round294_occurrence_kind":
                        target_kind[target],
                    "terminal_support_source_references": source_refs,
                    "terminal_registry_target_multiplicity": 1,
                    "binding_classification":
                        "FORMAL_EXISTING_ROUND294_OCCURRENCE_"
                        "PHYSICAL_TERMINAL_FACE_INCIDENCE",
                    "formal_existing_physical_incidence_binding_credit": 1,
                    "formal_new_occurrence_credit": 0,
                    "formal_representation_alias_credit": 0,
                    "formal_seam_edge_credit": 0,
                    "formal_component_union_credit": 0,
                    "formal_DSU_rank_reduction_credit": 0,
                    "formal_maximality_credit": 0,
                    "formal_fibre_credit": 0,
                    "formal_global_disposition_credit": 0,
                    "Jx_Jy_same_point_glue_credit": 0,
                }))
                relation_physical_ids.append(row_id)
                relation_targets.add(target)
                bound_rectangles.append(subcell)

        physical_area = union_area(bound_rectangles)
        gap_area = union_area(gap_rectangles)
        need(
            relation_area == physical_area + gap_area,
            "expected terminal-face partition",
        )
        physical_area_total += physical_area
        empty_area_total += gap_area
        actual_target_reference_count += len(relation_targets)
        if gap_rectangles:
            baseline_histogram["PARTIAL"] += 1
            need(len(gap_rectangles) == 1, "one expected exact gap")
        else:
            baseline_histogram["FULL"] += 1

        piece_keys: list[
            tuple[str, str, tuple[Q, Q, Q, Q]]
        ] = []
        for gap in gap_rectangles:
            hits: list[
                tuple[dict[str, Any], tuple[Q, Q, Q, Q]]
            ] = []
            for empty in empty_by_region.get(region_id, []):
                if empty["physical_t_square"][1] != upper:
                    continue
                intersection = intersect_rect(gap, empty["ps_rectangle"])
                if intersection is not None:
                    hits.append((empty, intersection))
            need(hits, "every expected gap has empty cover")
            need(
                union_area(hit for _cell, hit in hits) == rect_area(gap),
                "expected per-gap exact empty union",
            )
            for index, (_left_cell, left) in enumerate(hits):
                for _right_cell, right in hits[index + 1:]:
                    need(
                        intersect_rect(left, right) is None,
                        "expected empty pieces disjoint",
                    )
            gap_multiplicity[len(hits)] += 1
            for empty, intersection in hits:
                piece_key = (
                    relation_id,
                    empty["Round286_refinement_cell_id"],
                    intersection,
                )
                piece_keys.append(piece_key)
                raw_absence_pieces.append({
                    "piece_key": piece_key,
                    **common,
                    "terminal_face_physical_t_square": upper,
                    "exact_baseline_gap_ps_rectangle": gap,
                    "exact_empty_intersection_ps_rectangle": intersection,
                    "empty_cell": empty,
                })

        if gap_rectangles and relation_physical_ids:
            corrected = (
                "MIXED_PHYSICAL_EXISTING_OCCURRENCE_AND_"
                "WRONG_SIGNED_EMPTY_ABSENCE"
            )
            corrected_histogram["MIXED_PHYSICAL_AND_EMPTY"] += 1
        elif gap_rectangles:
            corrected = "WHOLE_WRONG_SIGNED_EMPTY_ABSENCE__NO_BINDING"
            corrected_histogram["WHOLE_EMPTY_ABSENCE"] += 1
        else:
            corrected = "WHOLE_PHYSICAL_EXISTING_OCCURRENCE_INCIDENCE"
            corrected_histogram["WHOLE_PHYSICAL"] += 1
        raw_relations.append({
            **common,
            "source_relation_classification":
                "PARTIAL" if gap_rectangles else "FULL",
            "corrected_relation_disposition": corrected,
            "physical_row_ids": relation_physical_ids,
            "physical_target_ids": sorted(relation_targets),
            "absence_piece_keys": piece_keys,
            "graph_no_binding_proof_ids": [],
            "physical_area": physical_area,
            "empty_area": gap_area,
            "graph_area": Q(0),
        })

    pieces_by_cell: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for piece in raw_absence_pieces:
        pieces_by_cell[
            piece["empty_cell"]["Round286_refinement_cell_id"]
        ].append(piece)
    unique_cell_area = Q(0)
    half_used_cells = 0
    reused_cells = 0
    for cell_id, pieces in pieces_by_cell.items():
        rectangles = [
            piece["exact_empty_intersection_ps_rectangle"]
            for piece in pieces
        ]
        for index, left in enumerate(rectangles):
            for right in rectangles[index + 1:]:
                need(
                    intersect_rect(left, right) is None,
                    "expected reused cell double-count:" + cell_id,
                )
        used_area = union_area(rectangles)
        full_area = rect_area(pieces[0]["empty_cell"]["ps_rectangle"])
        use_class = (
            "FULL_EMPTY_CELL_FACE_USED"
            if used_area == full_area
            else "HALF_EMPTY_CELL_FACE_USED"
        )
        if used_area != full_area:
            need(2 * used_area == full_area, "expected exact half cell")
            half_used_cells += 1
        reused_cells += int(len(pieces) > 1)
        unique_cell_area += used_area
        for piece in pieces:
            piece["empty_cell_use_multiplicity"] = len(pieces)
            piece["empty_cell_global_used_ps_area"] = used_area
            piece["empty_cell_full_ps_area"] = full_area
            piece["empty_cell_global_use_classification"] = use_class
    need(
        unique_cell_area
        == sum(
            rect_area(piece["exact_empty_intersection_ps_rectangle"])
            for piece in raw_absence_pieces
        )
        == empty_area_total,
        "expected unique-cell exact area",
    )

    absence_rows: list[dict[str, Any]] = []
    absence_id_by_key: dict[
        tuple[str, str, tuple[Q, Q, Q, Q]], str
    ] = {}
    for piece in raw_absence_pieces:
        empty = piece["empty_cell"]
        intersection = piece["exact_empty_intersection_ps_rectangle"]
        row_id = (
            "round295b-r289-wrong-signed-empty-no-binding:"
            + digest([
                piece["Round289_region_cell_relation_id"],
                empty["Round286_refinement_cell_id"],
                list(map(qstr, intersection)),
            ])
        )
        absence_id_by_key[piece["piece_key"]] = row_id
        absence_rows.append(close({
            "Round295B_wrong_signed_empty_no_binding_row_id": row_id,
            **{
                key: piece[key]
                for key in (
                    "Round289_region_cell_relation_id",
                    "Round268_true_seam_patch_row_id",
                    "side_index",
                    "Round275_region_id",
                    "exact_relation_ps_rectangle",
                    "exact_relation_ps_area",
                )
            },
            "Round286_refinement_cell_id":
                empty["Round286_refinement_cell_id"],
            "Round287_refinement_cell_disposition_row_id":
                empty["Round287_refinement_cell_disposition_row_id"],
            "coordinate_t_interval": list(map(
                qstr, empty["coordinate_box"][:2]
            )),
            "source_guard_t_interval": list(map(
                qstr,
                qbox(guards[
                    regions[piece["Round275_region_id"]][
                        "source_guard_row_id"
                    ]
                ]["box"])[:2],
            )),
            "independently_recomputed_physical_t_square_open_interval":
                list(map(qstr, empty["physical_t_square"])),
            "physical_t_square_formula":
                "coordinate_t_square INTERSECT "
                "(1-source_guard_t_square)",
            "raw_t_comparison_used": False,
            "terminal_face_physical_t_square":
                qstr(piece["terminal_face_physical_t_square"]),
            "exact_baseline_gap_ps_rectangle": list(map(
                qstr, piece["exact_baseline_gap_ps_rectangle"]
            )),
            "exact_empty_intersection_ps_rectangle":
                list(map(qstr, intersection)),
            "exact_empty_intersection_ps_area":
                qstr(rect_area(intersection)),
            "empty_cell_global_used_ps_area":
                qstr(piece["empty_cell_global_used_ps_area"]),
            "empty_cell_full_ps_area":
                qstr(piece["empty_cell_full_ps_area"]),
            "empty_cell_global_use_classification":
                piece["empty_cell_global_use_classification"],
            "empty_cell_use_multiplicity":
                piece["empty_cell_use_multiplicity"],
            "empty_cell_reused_without_double_count":
                piece["empty_cell_use_multiplicity"] > 1,
            "signed_region_cell_state": EMPTY,
            "desired_active_factor_side_sign":
                empty["desired_active_factor_side_sign"],
            "active_factor_extremal_signs":
                empty["active_factor_extremal_signs"],
            "strictly_opposite_desired_side": True,
            "Round286_coordinate_occupancy_count":
                empty["Round286_coordinate_occupancy_count"],
            "containing_atom_id_ignored_even_if_coordinate_occupied":
                empty["containing_atom_id"],
            "no_binding_classification":
                "WRONG_SIGNED_EMPTY_OPPOSITE_SIDE__NO_OCCURRENCE_BINDING",
            "terminal_registry_target_reference_count": 0,
            "terminal_registry_target_references": [],
            "formal_existing_physical_incidence_binding_credit": 0,
            "formal_new_occurrence_credit": 0,
            "formal_representation_alias_credit": 0,
            "formal_seam_edge_credit": 0,
            "formal_component_union_credit": 0,
            "formal_DSU_rank_reduction_credit": 0,
            "formal_maximality_credit": 0,
            "formal_fibre_credit": 0,
            "formal_global_disposition_credit": 0,
            "Jx_Jy_same_point_glue_credit": 0,
        }))

    corrected_rows: list[dict[str, Any]] = []
    for raw_source in raw_relations:
        raw = dict(raw_source)
        physical_area = raw.pop("physical_area")
        empty_area = raw.pop("empty_area")
        graph_area = raw.pop("graph_area")
        piece_keys = raw.pop("absence_piece_keys")
        relation_area = Q(raw["exact_relation_ps_area"])
        need(
            relation_area == physical_area + empty_area + graph_area,
            "expected corrected relation conservation",
        )
        corrected_id = (
            "round295b-r289-corrected-relation-disposition:"
            + digest(raw["Round289_region_cell_relation_id"])
        )
        corrected_rows.append(close({
            "Round295B_corrected_relation_disposition_row_id":
                corrected_id,
            **raw,
            "physical_incidence_binding_row_count":
                len(raw["physical_row_ids"]),
            "wrong_signed_empty_no_binding_row_count": len(piece_keys),
            "graph_separated_no_binding_row_count":
                len(raw["graph_no_binding_proof_ids"]),
            "wrong_signed_empty_no_binding_row_ids":
                sorted(absence_id_by_key[key] for key in piece_keys),
            "exact_physical_ps_area": qstr(physical_area),
            "exact_wrong_signed_empty_ps_area": qstr(empty_area),
            "exact_graph_separated_ps_area": qstr(graph_area),
            "exact_terminal_face_area_conserved": True,
            "remaining_terminal_face_frontier_ps_area": "0",
            "remaining_terminal_face_frontier_cell_count": 0,
            "formal_new_occurrence_credit": 0,
            "formal_representation_alias_credit": 0,
            "formal_seam_edge_credit": 0,
            "formal_component_union_credit": 0,
            "formal_DSU_rank_reduction_credit": 0,
            "formal_maximality_credit": 0,
            "formal_fibre_credit": 0,
            "formal_global_disposition_credit": 0,
            "Jx_Jy_same_point_glue_credit": 0,
        }))

    physical_rows.sort(
        key=lambda row:
            row["Round295B_physical_incidence_binding_row_id"]
    )
    absence_rows.sort(
        key=lambda row:
            row["Round295B_wrong_signed_empty_no_binding_row_id"]
    )
    graph_rows.sort(
        key=lambda row:
            row["Round295B_graph_separated_no_binding_row_id"]
    )
    corrected_rows.sort(
        key=lambda row:
            row["Round295B_corrected_relation_disposition_row_id"]
    )
    sign_histogram = Counter(
        tuple(row["active_factor_extremal_signs"]) for row in absence_rows
    )
    occupancy_histogram = Counter(
        row["Round286_coordinate_occupancy_count"] for row in absence_rows
    )
    use_histogram = Counter(len(pieces) for pieces in pieces_by_cell.values())
    need(
        baseline_histogram
        == {"FULL": 8_844, "PARTIAL": 396, "GRAPH_SEPARATED": 288}
        and corrected_histogram
        == {
            "WHOLE_PHYSICAL": 8_844,
            "MIXED_PHYSICAL_AND_EMPTY": 392,
            "WHOLE_EMPTY_ABSENCE": 4,
            "GRAPH_SEPARATED_ABSENCE": 288,
        },
        "expected baseline/corrected census",
    )
    need(
        len(corrected_rows) == 9_528
        and len(physical_rows) == 11_448
        and len(absence_rows) == 468
        and len(graph_rows) == 288
        and actual_target_reference_count == 10_956,
        "expected row/target census",
    )
    need(
        gap_multiplicity == {1: 348, 2: 24, 3: 24}
        and len(pieces_by_cell) == 440
        and use_histogram == {1: 412, 2: 28}
        and reused_cells == 28
        and half_used_cells == 4,
        "expected empty refinement census",
    )
    need(
        sign_histogram
        == {
            (NEGATIVE, NEGATIVE): 236,
            (POSITIVE, POSITIVE): 232,
        }
        and occupancy_histogram == {0: 316, 1: 152},
        "expected empty sign/occupancy census",
    )
    need(
        actual_relation_area == Q(851, 51_200)
        and graph_relation_area == Q(3, 12_800)
        and physical_area_total == Q(6_457, 409_600)
        and empty_area_total == Q(351, 409_600)
        and actual_relation_area == physical_area_total + empty_area_total,
        "expected global exact area",
    )

    ledger = {
        "schema": LEDGER_SCHEMA,
        "status": (
            "PASS_ROUND295B_R289_TERMINAL_FACE_FRONTIER_ZERO__"
            "11448_PHYSICAL_INCIDENCE_BINDINGS__468_WRONG_SIGNED_"
            "EMPTY_PIECES__288_GRAPH_NO_BINDING_PROOFS"
        ),
        "corrected_relation_disposition_ledger": table(
            corrected_rows,
            "Round295B_corrected_relation_disposition_row_id",
        ),
        "physical_incidence_binding_ledger": table(
            physical_rows,
            "Round295B_physical_incidence_binding_row_id",
        ),
        "wrong_signed_empty_no_binding_ledger": table(
            absence_rows,
            "Round295B_wrong_signed_empty_no_binding_row_id",
        ),
        "graph_separated_no_binding_ledger": table(
            graph_rows,
            "Round295B_graph_separated_no_binding_row_id",
        ),
    }
    ledger_bytes = deterministic_gzip_bytes(ledger)
    summary = {
        "schema": SCHEMA,
        "status": (
            "PASS_ROUND295B_R289_TERMINAL_FACE_ABSENCE_CLOSURE__"
            "FRONTIER_ZERO__ZERO_NEW_OCCURRENCE_IDS_OR_ALIASES__"
            "NO_SEAM_COMPONENT_DSU_CREDIT"
        ),
        "input_file_pins": {
            **{
                FILES[key]: value
                for key, value in sorted(UPSTREAM_PINS.items())
            },
            **dict(sorted(ROUND294_PINS.items())),
        },
        "Round294_registry_contract": {
            "formal_occurrence_registry_row_count": 431_208,
            "formal_representation_binding_count": 46_288,
            "Round295B_added_occurrence_ID_count": 0,
            "Round295B_added_representation_alias_count": 0,
            "post_Round295B_registry_row_count": 431_208,
            "Round294_result_sha256": round294["result_sha256"],
        },
        "baseline_relation_reconstruction": {
            "relation_count": 9_528,
            "whole_physical_cover_count": 8_844,
            "partial_terminal_face_gap_count": 396,
            "graph_separated_count": 288,
            "physical_terminal_subcell_count": 11_448,
            "actual_relation_distinct_target_reference_count": 10_956,
            "physical_terminal_subcells_all_unique_target": True,
            "exact_actual_relation_ps_area": qstr(actual_relation_area),
            "exact_physical_ps_area": qstr(physical_area_total),
            "exact_gap_ps_area": qstr(empty_area_total),
        },
        "empty_side_closure": {
            "coarse_gap_count": 396,
            "exact_wrong_signed_empty_intersection_piece_count": 468,
            "distinct_Round286_empty_cell_count": 440,
            "per_gap_piece_multiplicity_histogram": {
                str(key): value
                for key, value in sorted(gap_multiplicity.items())
            },
            "empty_cell_use_multiplicity_histogram": {
                str(key): value
                for key, value in sorted(use_histogram.items())
            },
            "reused_empty_cell_count": 28,
            "reused_empty_cell_extra_reference_count": 28,
            "half_used_empty_cell_count": 4,
            "active_factor_extremal_sign_histogram": {
                "STRICT_NEGATIVE|STRICT_NEGATIVE": 236,
                "STRICT_POSITIVE|STRICT_POSITIVE": 232,
            },
            "Round286_coordinate_occupancy_histogram": {
                "0": 316,
                "1": 152,
            },
            "all_empty_signs_strict_and_opposite_desired_side": True,
            "occupancy_one_empty_cells_create_binding": False,
            "physical_t_square_formula":
                "coordinate_t_square INTERSECT "
                "(1-source_guard_t_square)",
            "raw_t_comparison_used": False,
            "per_gap_exact_union": True,
            "per_relation_exact_union": True,
            "global_exact_union": True,
            "piece_interiors_disjoint": True,
            "reused_cells_double_counted": False,
            "exact_gap_ps_area": qstr(empty_area_total),
        },
        "corrected_relation_census": {
            "relation_count": 9_528,
            "physical_relation_count": 9_236,
            "whole_physical_relation_count": 8_844,
            "mixed_physical_and_empty_relation_count": 392,
            "absent_relation_count": 292,
            "whole_wrong_signed_empty_relation_count": 4,
            "graph_separated_absent_relation_count": 288,
            "remaining_R289_terminal_face_frontier_count": 0,
            "remaining_R289_terminal_face_frontier_ps_area": "0",
        },
        "formal_credit_transition": {
            "formal_existing_occurrence_physical_incidence_binding_count":
                11_448,
            "formal_new_occurrence_ID_count": 0,
            "formal_representation_alias_count": 0,
            "formal_seam_edge_credit": 0,
            "formal_component_union_credit": 0,
            "formal_DSU_rank_reduction_credit": 0,
            "formal_maximality_credit": 0,
            "formal_fibre_credit": 0,
            "formal_global_disposition_credit": 0,
            "Jx_Jy_same_point_glue_credit": 0,
        },
        "ledger": {
            "filename": LEDGER.name,
            "file_sha256": hashlib.sha256(ledger_bytes).hexdigest(),
            "corrected_relation_rows_sha256":
                ledger["corrected_relation_disposition_ledger"][
                    "rows_sha256"
                ],
            "physical_incidence_rows_sha256":
                ledger["physical_incidence_binding_ledger"]["rows_sha256"],
            "wrong_signed_empty_rows_sha256":
                ledger["wrong_signed_empty_no_binding_ledger"][
                    "rows_sha256"
                ],
            "graph_separated_rows_sha256":
                ledger["graph_separated_no_binding_ledger"][
                    "rows_sha256"
                ],
        },
        "strict_nonpromotion": {
            "post_Round294_quotient_component_count": None,
            "post_Round294_expanded_registry_component_DSU_status":
                "NOT_REBUILT",
            "legacy_pre_Round294_quotient_components": 63_224,
            "legacy_63224_is_current_post_Round294_count": False,
            "true_seam_directed_endpoint_cell_count": 152,
            "formal_true_seam_edge_count": 0,
            "Gate5": "10/18",
            "D02": "BLOCKED",
            "CM2": "NO-GO_FOR_CLAIM",
        },
    }
    summary["result_sha256"] = digest(summary)
    return ledger, summary


def json_no_duplicates(payload: bytes) -> Any:
    def hook(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in pairs:
            need(key not in result, "duplicate JSON key:" + key)
            result[key] = value
        return result

    try:
        return json.loads(payload.decode("utf-8"), object_pairs_hook=hook)
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise VerificationError("strict JSON decode") from error


def audit_semantic_objects(
    result: dict[str, Any],
    ledger: dict[str, Any],
    expected_result: dict[str, Any],
    expected_ledger: dict[str, Any],
) -> None:
    need(isinstance(result, dict) and isinstance(ledger, dict), "objects")
    verify_result(result, "result_sha256", "candidate result")
    need(
        result["schema"] == SCHEMA
        and ledger["schema"] == LEDGER_SCHEMA,
        "candidate schemas",
    )
    specifications = (
        (
            "corrected_relation_disposition_ledger",
            "Round295B_corrected_relation_disposition_row_id",
            9_528,
        ),
        (
            "physical_incidence_binding_ledger",
            "Round295B_physical_incidence_binding_row_id",
            11_448,
        ),
        (
            "wrong_signed_empty_no_binding_ledger",
            "Round295B_wrong_signed_empty_no_binding_row_id",
            468,
        ),
        (
            "graph_separated_no_binding_ledger",
            "Round295B_graph_separated_no_binding_row_id",
            288,
        ),
    )
    need(
        Path(result["ledger"]["filename"]).name
        == result["ledger"]["filename"]
        and "/" not in result["ledger"]["filename"]
        and "\\" not in result["ledger"]["filename"],
        "candidate ledger basename confinement",
    )
    need(
        result == expected_result,
        "candidate result differs from full independent reconstruction",
    )
    changed_tables = [
        (name, id_key, count)
        for name, id_key, count in specifications
        if ledger[name]["rows_sha256"]
        != expected_ledger[name]["rows_sha256"]
    ]
    if changed_tables:
        for name, id_key, count in changed_tables:
            verify_nested(
                ledger[name], id_key, count, "candidate changed:" + name
            )
        raise VerificationError(
            "candidate table differs from independent reconstruction"
        )
    for name, id_key, count in specifications:
        verify_nested(ledger[name], id_key, count, "candidate:" + name)
    need(
        ledger == expected_ledger,
        "candidate ledger differs from full independent reconstruction",
    )


def audit_candidate_bytes(
    result_bytes: bytes,
    ledger_bytes: bytes,
    expected_result: dict[str, Any],
    expected_ledger: dict[str, Any],
) -> None:
    result = json_no_duplicates(result_bytes)
    need(isinstance(result, dict), "candidate result object")
    try:
        decompressed = gzip.decompress(ledger_bytes)
    except (EOFError, OSError) as error:
        raise VerificationError("candidate gzip decode") from error
    ledger = json_no_duplicates(decompressed)
    need(isinstance(ledger, dict), "candidate ledger object")
    audit_semantic_objects(
        result, ledger, expected_result, expected_ledger
    )
    need(
        result_bytes == canonical(expected_result) + b"\n",
        "candidate result canonical bytes",
    )
    need(
        ledger_bytes == deterministic_gzip_bytes(expected_ledger),
        "candidate deterministic gzip bytes",
    )
    need(
        result["ledger"]["file_sha256"]
        == hashlib.sha256(ledger_bytes).hexdigest(),
        "candidate result/ledger byte binding",
    )


def reclose_result(mutant: dict[str, Any]) -> dict[str, Any]:
    mutant = deepcopy(mutant)
    mutant.pop("result_sha256", None)
    mutant["result_sha256"] = digest(mutant)
    return mutant


def reclose_ledger_row_mutation(
    source: dict[str, Any],
    table_name: str,
    row_index: int,
    mutation: Callable[[dict[str, Any]], None],
) -> dict[str, Any]:
    mutant = dict(source)
    old_table = source[table_name]
    new_table = dict(old_table)
    rows = list(old_table["rows"])
    payload = {
        key: value
        for key, value in rows[row_index].items()
        if key != "row_sha256"
    }
    mutation(payload)
    rows[row_index] = close(payload)
    new_table["rows"] = rows
    new_table["rows_sha256"] = digest(rows)
    id_keys = {
        "corrected_relation_disposition_ledger":
            "Round295B_corrected_relation_disposition_row_id",
        "physical_incidence_binding_ledger":
            "Round295B_physical_incidence_binding_row_id",
        "wrong_signed_empty_no_binding_ledger":
            "Round295B_wrong_signed_empty_no_binding_row_id",
        "graph_separated_no_binding_ledger":
            "Round295B_graph_separated_no_binding_row_id",
    }
    id_key = id_keys[table_name]
    new_table["row_ids_sha256"] = digest([row[id_key] for row in rows])
    new_table["row_hashes_sha256"] = digest(
        [row["row_sha256"] for row in rows]
    )
    mutant[table_name] = new_table
    return mutant


def run_attack_suite(
    expected_result: dict[str, Any],
    expected_ledger: dict[str, Any],
) -> list[dict[str, str]]:
    attacks: list[dict[str, str]] = []

    def rejected(
        attack_id: str,
        classification: str,
        action: Callable[[], None],
    ) -> None:
        try:
            action()
        except Exception:
            attacks.append({
                "attack_id": attack_id,
                "classification": classification,
                "disposition": "REJECTED",
            })
            return
        raise VerificationError("attack accepted:" + attack_id)

    def result_attack(
        attack_id: str,
        path: tuple[str, ...],
        value: Any,
        classification: str = "RESIGNED_SEMANTIC_FORGERY",
    ) -> None:
        mutant = deepcopy(expected_result)
        cursor: dict[str, Any] = mutant
        for key in path[:-1]:
            cursor = cursor[key]
        cursor[path[-1]] = value
        mutant = reclose_result(mutant)
        rejected(
            attack_id,
            classification,
            lambda: audit_semantic_objects(
                mutant, expected_ledger, expected_result, expected_ledger
            ),
        )

    result_attack(
        "A01_RAW_T_COMPARISON_SUMMARY",
        ("empty_side_closure", "raw_t_comparison_used"),
        True,
    )
    result_attack(
        "A02_RAW_T_FORMULA_SUBSTITUTION",
        ("empty_side_closure", "physical_t_square_formula"),
        "raw_t_interval",
    )
    result_attack(
        "A03_OCCUPANCY_ONE_FALSE_BIND_SUMMARY",
        ("empty_side_closure", "occupancy_one_empty_cells_create_binding"),
        True,
    )
    result_attack(
        "A04_FORGED_GAP_AREA",
        ("empty_side_closure", "exact_gap_ps_area"),
        "352/409600",
    )
    result_attack(
        "A05_OMIT_COARSE_GAP",
        ("empty_side_closure", "coarse_gap_count"),
        395,
    )
    result_attack(
        "A06_OMIT_REFINED_PIECE",
        (
            "empty_side_closure",
            "exact_wrong_signed_empty_intersection_piece_count",
        ),
        467,
    )
    result_attack(
        "A07_FORGE_UNIQUE_EMPTY_CELL_COUNT",
        ("empty_side_closure", "distinct_Round286_empty_cell_count"),
        439,
    )
    result_attack(
        "A08_REUSED_CELL_DOUBLE_COUNT_SUMMARY",
        ("empty_side_closure", "reused_cells_double_counted"),
        True,
    )
    result_attack(
        "A09_HALF_CELL_ERASURE",
        ("empty_side_closure", "half_used_empty_cell_count"),
        0,
    )
    result_attack(
        "A10_MISSING_FOUR_WHOLE_EMPTY",
        (
            "corrected_relation_census",
            "whole_wrong_signed_empty_relation_count",
        ),
        0,
    )
    result_attack(
        "A11_MISSING_GRAPH_SEPARATED_RELATION",
        (
            "corrected_relation_census",
            "graph_separated_absent_relation_count",
        ),
        287,
    )
    result_attack(
        "A12_GAP_TO_NEW_OCCURRENCE",
        ("formal_credit_transition", "formal_new_occurrence_ID_count"),
        1,
    )
    result_attack(
        "A13_GAP_TO_ALIAS",
        ("formal_credit_transition", "formal_representation_alias_count"),
        1,
    )
    result_attack(
        "A14_FORGE_152_SEAM_EDGES",
        ("formal_credit_transition", "formal_seam_edge_credit"),
        152,
    )
    result_attack(
        "A15_NONZERO_COMPONENT_UNION",
        ("formal_credit_transition", "formal_component_union_credit"),
        1,
    )
    result_attack(
        "A16_NONZERO_DSU_REDUCTION",
        ("formal_credit_transition", "formal_DSU_rank_reduction_credit"),
        1,
    )
    result_attack(
        "A17_NONZERO_MAXIMALITY",
        ("formal_credit_transition", "formal_maximality_credit"),
        1,
    )
    result_attack(
        "A18_NONZERO_FIBRE",
        ("formal_credit_transition", "formal_fibre_credit"),
        1,
    )
    result_attack(
        "A19_NONZERO_GLOBAL",
        ("formal_credit_transition", "formal_global_disposition_credit"),
        1,
    )
    result_attack(
        "A20_JX_JY_SIGNATURE_IDENTITY_GLUE",
        ("formal_credit_transition", "Jx_Jy_same_point_glue_credit"),
        1,
    )
    result_attack(
        "A21_LEGACY_63224_AS_CURRENT",
        ("strict_nonpromotion", "post_Round294_quotient_component_count"),
        63_224,
    )
    result_attack(
        "A22_LEGACY_CURRENT_FLAG",
        (
            "strict_nonpromotion",
            "legacy_63224_is_current_post_Round294_count",
        ),
        True,
    )
    result_attack(
        "A23_FALSE_FRONTIER_CELL",
        (
            "corrected_relation_census",
            "remaining_R289_terminal_face_frontier_count",
        ),
        1,
    )
    result_attack(
        "A24_REGISTRY_ROW_INFLATION",
        ("Round294_registry_contract", "post_Round295B_registry_row_count"),
        431_209,
    )
    result_attack(
        "A25_PHYSICAL_BINDING_CENSUS_FORGERY",
        (
            "formal_credit_transition",
            "formal_existing_occurrence_physical_incidence_binding_count",
        ),
        11_449,
    )
    result_attack(
        "A26_TARGET_REFERENCE_CENSUS_FORGERY",
        (
            "baseline_relation_reconstruction",
            "actual_relation_distinct_target_reference_count",
        ),
        10_955,
    )
    result_attack(
        "A27_ABSOLUTE_LEDGER_PATH",
        ("ledger", "filename"),
        "/tmp/" + LEDGER.name,
        "RESIGNED_PATH_SUBSTITUTION",
    )
    result_attack(
        "A28_PARENT_LEDGER_PATH",
        ("ledger", "filename"),
        "../" + LEDGER.name,
        "RESIGNED_PATH_SUBSTITUTION",
    )

    absence_name = "wrong_signed_empty_no_binding_ledger"
    absence_rows = expected_ledger[absence_name]["rows"]
    occ1_index = next(
        index for index, row in enumerate(absence_rows)
        if row["Round286_coordinate_occupancy_count"] == 1
    )
    reused_index = next(
        index for index, row in enumerate(absence_rows)
        if row["empty_cell_use_multiplicity"] == 2
    )
    half_index = next(
        index for index, row in enumerate(absence_rows)
        if row["empty_cell_global_use_classification"]
        == "HALF_EMPTY_CELL_FACE_USED"
    )
    negative_index = next(
        index for index, row in enumerate(absence_rows)
        if row["desired_active_factor_side_sign"] == POSITIVE
    )

    def ledger_attack(
        attack_id: str,
        table_name: str,
        row_index: int,
        mutation: Callable[[dict[str, Any]], None],
    ) -> None:
        mutant = reclose_ledger_row_mutation(
            expected_ledger, table_name, row_index, mutation
        )
        rejected(
            attack_id,
            "RESIGNED_SUBSTANTIVE_LEDGER_FORGERY",
            lambda: audit_semantic_objects(
                expected_result, mutant, expected_result, expected_ledger
            ),
        )

    ledger_attack(
        "A29_ROW_RAW_T_COMPARISON",
        absence_name,
        0,
        lambda row: row.update({
            "raw_t_comparison_used": True,
            "physical_t_square_formula": "raw_t_interval",
        }),
    )
    ledger_attack(
        "A30_OCCUPANCY_ONE_FALSE_BIND_ROW",
        absence_name,
        occ1_index,
        lambda row: row.update({
            "formal_existing_physical_incidence_binding_credit": 1,
            "terminal_registry_target_reference_count": 1,
            "terminal_registry_target_references": [
                row["containing_atom_id_ignored_even_if_coordinate_occupied"]
            ],
        }),
    )
    ledger_attack(
        "A31_SIGN_FLIP_TO_DESIRED_SIDE",
        absence_name,
        negative_index,
        lambda row: row.update({
            "active_factor_extremal_signs": [POSITIVE, POSITIVE],
            "strictly_opposite_desired_side": False,
        }),
    )
    ledger_attack(
        "A32_CLIPPED_AS_EMPTY",
        absence_name,
        0,
        lambda row: row.update({
            "signed_region_cell_state":
                "CLIPPED_OR_UNRESOLVED_COORDINATE_CELL"
        }),
    )
    ledger_attack(
        "A33_GAP_ROW_TO_OCCURRENCE",
        absence_name,
        0,
        lambda row: row.update({"formal_new_occurrence_credit": 1}),
    )
    ledger_attack(
        "A34_REUSED_CELL_DOUBLE_COUNT_ROW",
        absence_name,
        reused_index,
        lambda row: row.update({
            "empty_cell_reused_without_double_count": False,
            "empty_cell_global_used_ps_area":
                row["empty_cell_full_ps_area"],
        }),
    )
    ledger_attack(
        "A35_HALF_USED_CELL_AS_FULL",
        absence_name,
        half_index,
        lambda row: row.update({
            "empty_cell_global_use_classification":
                "FULL_EMPTY_CELL_FACE_USED",
            "empty_cell_global_used_ps_area":
                row["empty_cell_full_ps_area"],
        }),
    )
    ledger_attack(
        "A36_FORGED_PIECE_AREA",
        absence_name,
        0,
        lambda row: row.update({
            "exact_empty_intersection_ps_area": "1"
        }),
    )
    ledger_attack(
        "A37_SIGNATURE_IDENTITY_AS_BINDING",
        absence_name,
        0,
        lambda row: row.update({
            "no_binding_classification":
                "COMPLETE_SIGNATURE_IDENTITY_IMPLIES_BINDING",
            "Jx_Jy_same_point_glue_credit": 1,
        }),
    )
    corrected_name = "corrected_relation_disposition_ledger"
    corrected_rows = expected_ledger[corrected_name]["rows"]
    w2_index = next(
        index for index, row in enumerate(corrected_rows)
        if row["wrong_signed_empty_no_binding_row_count"] == 2
    )
    w3_index = next(
        index for index, row in enumerate(corrected_rows)
        if row["wrong_signed_empty_no_binding_row_count"] == 3
    )
    whole_empty_index = next(
        index for index, row in enumerate(corrected_rows)
        if row["corrected_relation_disposition"]
        == "WHOLE_WRONG_SIGNED_EMPTY_ABSENCE__NO_BINDING"
    )
    graph_index = next(
        index for index, row in enumerate(corrected_rows)
        if row["source_relation_classification"] == "GRAPH_SEPARATED"
    )
    ledger_attack(
        "A38_OMITTED_W2_REFINEMENT",
        corrected_name,
        w2_index,
        lambda row: row.update({
            "wrong_signed_empty_no_binding_row_count": 1,
            "wrong_signed_empty_no_binding_row_ids":
                row["wrong_signed_empty_no_binding_row_ids"][:1],
        }),
    )
    ledger_attack(
        "A39_OMITTED_W3_REFINEMENT",
        corrected_name,
        w3_index,
        lambda row: row.update({
            "wrong_signed_empty_no_binding_row_count": 2,
            "wrong_signed_empty_no_binding_row_ids":
                row["wrong_signed_empty_no_binding_row_ids"][:2],
        }),
    )
    ledger_attack(
        "A40_ERASE_WHOLE_EMPTY_RELATION",
        corrected_name,
        whole_empty_index,
        lambda row: row.update({
            "corrected_relation_disposition":
                "WHOLE_PHYSICAL_EXISTING_OCCURRENCE_INCIDENCE"
        }),
    )
    ledger_attack(
        "A41_ERASE_GRAPH_NO_BINDING_PROOF",
        corrected_name,
        graph_index,
        lambda row: row.update({
            "graph_separated_no_binding_row_count": 0,
            "graph_no_binding_proof_ids": [],
        }),
    )
    physical_name = "physical_incidence_binding_ledger"
    ledger_attack(
        "A42_PHYSICAL_TARGET_MULTIPLICITY_TWO",
        physical_name,
        0,
        lambda row: row.update({
            "terminal_registry_target_multiplicity": 2
        }),
    )
    graph_name = "graph_separated_no_binding_ledger"
    ledger_attack(
        "A43_GRAPH_RELATION_FALSE_BIND",
        graph_name,
        0,
        lambda row: row.update({
            "formal_existing_physical_incidence_binding_credit": 1
        }),
    )

    good_result_bytes = canonical(expected_result) + b"\n"
    good_ledger_bytes = deterministic_gzip_bytes(expected_ledger)

    def byte_attack(
        attack_id: str,
        result_bytes: bytes,
        ledger_bytes: bytes,
        classification: str,
    ) -> None:
        rejected(
            attack_id,
            classification,
            lambda: audit_candidate_bytes(
                result_bytes,
                ledger_bytes,
                expected_result,
                expected_ledger,
            ),
        )

    byte_attack(
        "A44_DUPLICATE_RESULT_JSON_KEY",
        b'{"schema":"x","schema":"y"}',
        good_ledger_bytes,
        "MALFORMED_JSON",
    )
    byte_attack(
        "A45_TRAILING_RESULT_JSON",
        good_result_bytes + b"{}",
        good_ledger_bytes,
        "MALFORMED_JSON",
    )
    byte_attack(
        "A46_NON_UTF8_RESULT",
        b"\xff",
        good_ledger_bytes,
        "MALFORMED_ENCODING",
    )
    byte_attack(
        "A47_TRUNCATED_RESULT",
        good_result_bytes[:100],
        good_ledger_bytes,
        "MALFORMED_JSON",
    )
    byte_attack(
        "A48_TRUNCATED_GZIP",
        good_result_bytes,
        good_ledger_bytes[:-8],
        "MALFORMED_GZIP",
    )
    byte_attack(
        "A49_CONCATENATED_GZIP_MEMBERS",
        good_result_bytes,
        good_ledger_bytes + deterministic_gzip_bytes({}),
        "MALFORMED_GZIP",
    )
    alternate = io.BytesIO()
    with gzip.GzipFile(
        filename="forged.json", mode="wb", fileobj=alternate, mtime=7
    ) as handle:
        handle.write(canonical(expected_ledger))
    byte_attack(
        "A50_ALTERNATE_GZIP_HEADER",
        good_result_bytes,
        alternate.getvalue(),
        "NONDETERMINISTIC_GZIP_SUBSTITUTION",
    )
    byte_attack(
        "A51_TRAILING_GZIP_BYTES",
        good_result_bytes,
        good_ledger_bytes + b"TRAIL",
        "MALFORMED_GZIP",
    )
    byte_attack(
        "A52_DUPLICATE_LEDGER_JSON_KEY",
        good_result_bytes,
        gzip.compress(b'{"schema":"x","schema":"y"}', mtime=0),
        "MALFORMED_JSON",
    )
    byte_attack(
        "A53_WRONG_LEDGER_OBJECT",
        good_result_bytes,
        gzip.compress(b"[]", mtime=0),
        "MALFORMED_LEDGER",
    )
    need(
        len(attacks) == 53
        and all(row["disposition"] == "REJECTED" for row in attacks),
        "complete attack suite",
    )
    return attacks


def verify_all() -> dict[str, Any]:
    # Upstream-only phase.  No current candidate artifact is opened before
    # the 9,528 relations and complete expected four-table object exist.
    for key, expected in UPSTREAM_PINS.items():
        need(
            file_sha256(HERE / FILES[key]) == expected,
            "upstream input pin:" + FILES[key],
        )
    round294 = verify_round294_package()
    regions, endpoints, channels = load_relation_upstream()
    relations = independently_reconstruct_r289_relations(
        regions, endpoints, channels
    )
    (
        support,
        empty,
        upper,
        target_kind,
        guards,
    ) = reconstruct_terminal_inputs(regions)
    expected_ledger, expected_result = independently_build_expected(
        relations,
        regions,
        support,
        empty,
        upper,
        target_kind,
        guards,
        round294,
    )

    # Candidate phase begins only here.
    need(
        all("PENDING_" not in value for value in CANDIDATE_PINS.values()),
        "final candidate pins configured",
    )
    for filename, expected in CANDIDATE_PINS.items():
        need(
            file_sha256(HERE / filename) == expected,
            "candidate byte pin:" + filename,
        )
    result_bytes = RESULT.read_bytes()
    ledger_bytes = LEDGER.read_bytes()
    audit_candidate_bytes(
        result_bytes, ledger_bytes, expected_result, expected_ledger
    )
    attacks = run_attack_suite(expected_result, expected_ledger)

    verification = {
        "schema": VERIFICATION_SCHEMA,
        "status": (
            "PASS_INDEPENDENT_CACHELESS_ROUND295B__9528_RELATIONS_"
            "RECONSTRUCTED_BEFORE_CANDIDATE__11448_PHYSICAL_BINDINGS__"
            "468_WRONG_SIGNED_EMPTY_NO_BINDING__288_GRAPH_NO_BINDING__"
            "53_OF_53_ATTACKS_REJECTED"
        ),
        "methodology": {
            "producer_imported_or_executed": False,
            "historical_Round293_used_as_oracle": False,
            "historical_Round293_artifact_opened": False,
            "cache_used": False,
            "expected_object_built_before_candidate_result_or_ledger_read":
                True,
            "relation_geometry_sources": [
                FILES[key]
                for key in ("R268", "R275", "R280", "R282", "R283")
            ],
            "terminal_registry_cover_sources": [
                FILES[key]
                for key in (
                    "R174", "R179", "R286", "R287", "R288", "R292A"
                )
            ],
            "Round294_full_package_byte_pinned": True,
            "physical_t_square_recomputed_from_coordinate_and_source_guard":
                True,
            "two_seed_replay_supported": True,
        },
        "input_file_pins": {
            **{
                FILES[key]: value
                for key, value in sorted(UPSTREAM_PINS.items())
            },
            **dict(sorted(ROUND294_PINS.items())),
        },
        "candidate_file_pins": dict(sorted(CANDIDATE_PINS.items())),
        "independent_reconstruction": {
            "R289_relation_rectangle_count": 9_528,
            "baseline_whole_count": 8_844,
            "baseline_partial_count": 396,
            "baseline_graph_separated_count": 288,
            "corrected_physical_relation_count": 9_236,
            "corrected_absent_relation_count": 292,
            "physical_incidence_binding_row_count": 11_448,
            "wrong_signed_empty_no_binding_row_count": 468,
            "graph_separated_no_binding_row_count": 288,
            "distinct_empty_cell_count": 440,
            "gap_piece_multiplicity_histogram":
                {"1": 348, "2": 24, "3": 24},
            "empty_sign_histogram": {
                "STRICT_NEGATIVE|STRICT_NEGATIVE": 236,
                "STRICT_POSITIVE|STRICT_POSITIVE": 232,
            },
            "empty_coordinate_occupancy_histogram":
                {"0": 316, "1": 152},
            "reused_empty_cell_count": 28,
            "half_used_empty_cell_count": 4,
            "exact_gap_ps_area": "351/409600",
            "remaining_frontier_count": 0,
            "remaining_frontier_ps_area": "0",
        },
        "nonpromotion": {
            "Round295B_added_occurrence_ID_count": 0,
            "Round295B_added_representation_alias_count": 0,
            "formal_seam_edge_credit": 0,
            "formal_component_union_credit": 0,
            "formal_DSU_rank_reduction_credit": 0,
            "formal_maximality_credit": 0,
            "formal_fibre_credit": 0,
            "formal_global_disposition_credit": 0,
            "Jx_Jy_same_point_glue_credit": 0,
            "post_Round294_quotient_component_count": None,
            "post_Round294_DSU_status": "NOT_REBUILT",
            "legacy_63224_used_as_current_count": False,
        },
        "attack_suite": {
            "attack_count": len(attacks),
            "rejected_count": len(attacks),
            "accepted_count": 0,
            "attacks": attacks,
        },
        "candidate_result_embedded_sha256":
            expected_result["result_sha256"],
        "candidate_result_file_sha256":
            hashlib.sha256(result_bytes).hexdigest(),
        "candidate_ledger_file_sha256":
            hashlib.sha256(ledger_bytes).hexdigest(),
        "expected_ledger_object_sha256": digest(expected_ledger),
    }
    verification["verification_sha256"] = digest(verification)
    return verification


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=OUTPUT)
    arguments = parser.parse_args()
    verification = verify_all()
    atomic_write(arguments.output, canonical(verification) + b"\n")
    print(json.dumps({
        "status": verification["status"],
        "verification_sha256": verification["verification_sha256"],
        "attack_count": verification["attack_suite"]["attack_count"],
        "candidate_ledger_file_sha256":
            verification["candidate_ledger_file_sha256"],
    }, sort_keys=True))


if __name__ == "__main__":
    main()
