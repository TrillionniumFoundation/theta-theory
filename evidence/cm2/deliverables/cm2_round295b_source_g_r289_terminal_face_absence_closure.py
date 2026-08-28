#!/usr/bin/env python3
"""Close the Round289 terminal-face frontier by exact physical/absence rows.

The 396 formerly partial terminal-face relations are not missing occurrences.
Their uncovered rectangles lie in Round287 cells proved empty for the desired
signed Round275 region.  This producer partitions those rectangles into 468
exact wrong-signed pieces, promotes the already known 11,448 unique-target
physical incidences to formal incidence bindings, and emits explicit
no-binding proofs for both the 468 empty pieces and the 288 graph-separated
relations.  It issues no occurrence ID or representation alias and builds no
seam/component/DSU state.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from fractions import Fraction as Q
import gzip
import hashlib
import io
import json
import os
from pathlib import Path
import tempfile
from typing import Any, Iterable


HERE = Path(__file__).resolve().parent
PREFIX = "cm2_round295b_source_g_r289_terminal_face_absence_closure"
RESULT = HERE / f"{PREFIX}_result.json"
LEDGER = HERE / f"{PREFIX}_ledger.json.gz"

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

PINS = {
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

# Filled only after the complete Round294 package has passed its dual replay
# and final manifest seal.  The producer refuses to run with a stale package.
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

SCHEMA = "cm2.round295b.source-g-r289-terminal-face-absence-closure.v1"
LEDGER_SCHEMA = SCHEMA + ".ledger.v1"
EMPTY = "EMPTY_OPPOSITE_SIDE_COORDINATE_CELL"


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


def need(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def read_json(key: str) -> dict[str, Any]:
    with (HERE / FILES[key]).open("rb") as handle:
        value = json.load(handle)
    need(isinstance(value, dict), f"JSON object:{FILES[key]}")
    return value


def read_gzip(key: str) -> dict[str, Any]:
    with gzip.open(HERE / FILES[key], "rt", encoding="utf-8") as handle:
        value = json.load(handle)
    need(isinstance(value, dict), f"gzip JSON object:{FILES[key]}")
    return value


def verify_result_hash(value: dict[str, Any], label: str) -> None:
    claim = value["result_sha256"]
    payload = {
        key: child for key, child in value.items()
        if key != "result_sha256"
    }
    need(claim == digest(payload), f"{label}:result closure")


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
        isinstance(rows, list)
        and len(rows) == document[count_key]
        and digest(rows) == document[hash_key],
        f"{rows_key}:table closure",
    )
    for row in rows:
        verify_row(row, rows_key)
    return rows


def verify_nested_table(
    table: dict[str, Any], id_key: str, expected_count: int, label: str
) -> list[dict[str, Any]]:
    rows = table["rows"]
    need(
        len(rows) == table["row_count"] == expected_count
        and digest(rows) == table["rows_sha256"],
        f"{label}:table closure",
    )
    ids = [row[id_key] for row in rows]
    need(
        len(ids) == len(set(ids))
        and digest(ids) == table["row_ids_sha256"],
        f"{label}:ID closure",
    )
    hashes = []
    for row in rows:
        verify_row(row, label)
        hashes.append(row["row_sha256"])
    need(digest(hashes) == table["row_hashes_sha256"], f"{label}:hash closure")
    return rows


def unpack(document: dict[str, Any], table: str) -> list[dict[str, Any]]:
    result = document["result"]
    rows = result[table]
    columns = result["row_column_schemas"][table]
    census = result["table_census_and_sha256"][table]
    need(
        len(rows) == census["row_count"]
        and digest(rows) == census["rows_sha256"],
        f"packed table:{table}",
    )
    return [dict(zip(columns, row, strict=True)) for row in rows]


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
    coordinate_box: tuple[Q, ...],
    source_guard_box: tuple[Q, ...],
) -> tuple[Q, Q]:
    coordinate = square_interval(coordinate_box[0], coordinate_box[1])
    source = square_interval(source_guard_box[0], source_guard_box[1])
    image = (1 - source[1], 1 - source[0])
    result = max(coordinate[0], image[0]), min(coordinate[1], image[1])
    need(result[0] < result[1], "positive physical t-square intersection")
    return result


def intersect_rect(
    left: tuple[Q, Q, Q, Q],
    right: tuple[Q, Q, Q, Q],
) -> tuple[Q, Q, Q, Q] | None:
    result = (
        max(left[0], right[0]),
        min(left[1], right[1]),
        max(left[2], right[2]),
        min(left[3], right[3]),
    )
    return (
        result
        if result[0] < result[1] and result[2] < result[3]
        else None
    )


def rect_area(rectangle: tuple[Q, Q, Q, Q]) -> Q:
    return (
        (rectangle[1] - rectangle[0])
        * (rectangle[3] - rectangle[2])
    )


def rectangle_union_area(
    rectangles: Iterable[tuple[Q, Q, Q, Q]]
) -> Q:
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


def table(rows: list[dict[str, Any]], id_key: str) -> dict[str, Any]:
    return {
        "row_count": len(rows),
        "rows_sha256": digest(rows),
        "row_ids_sha256": digest([row[id_key] for row in rows]),
        "row_hashes_sha256": digest([row["row_sha256"] for row in rows]),
        "rows": rows,
    }


def verify_round294_seal() -> dict[str, Any]:
    for filename, expected in ROUND294_PINS.items():
        need(
            expected != "PENDING_ROUND294_FINAL_SEAL"
            and file_sha256(HERE / filename) == expected,
            f"Round294 final package pin:{filename}",
        )
    result_path = HERE / (
        "cm2_round294_source_g_occurrence_registry_atomic_promotion_result.json"
    )
    verification_path = HERE / (
        "cm2_round294_source_g_occurrence_registry_atomic_promotion_"
        "verification.json"
    )
    with result_path.open("rb") as handle:
        result = json.load(handle)
    verify_result_hash(result, "Round294")
    with verification_path.open("rb") as handle:
        verification = json.load(handle)
    verification_claim = verification["verification_sha256"]
    verification_payload = {
        key: value for key, value in verification.items()
        if key != "verification_sha256"
    }
    need(
        verification_claim == digest(verification_payload)
        and verification["status"].startswith(
            "PASS_INDEPENDENT_CACHELESS_ROUND294"
        ),
        "Round294 independent verification seal",
    )
    need(
        result["census"]["formal_occurrence_registry_row_count"] == 431_208
        and result["census"]["formal_representation_binding_count"] == 46_288
        and result["census"]["formal_new_occurrence_count"] == 304_740
        and result["nonpromotion_freeze"][
            "post_Round294_quotient_component_count"
        ] is None
        and result["nonpromotion_freeze"][
            "post_Round294_expanded_registry_component_DSU_status"
        ] == "NOT_REBUILT",
        "Round294 registry/non-DSU contract",
    )
    return result


def load_regions_and_guards() -> tuple[
    dict[str, dict[str, Any]], dict[str, dict[str, Any]]
]:
    r275_wrapper = read_json("R275")
    need(
        r275_wrapper["result_sha256"] == digest(r275_wrapper["result"]),
        "Round275 result closure",
    )
    regions: dict[str, dict[str, Any]] = {}
    for name, expected in (
        ("strict_region_ledger", 5_288),
        ("arrangement_region_ledger", 8_500),
    ):
        ledger = r275_wrapper["result"][name]
        rows = ledger["rows"]
        need(
            len(rows) == ledger["row_count"] == expected
            and digest(rows) == ledger["rows_sha256"],
            f"Round275:{name}",
        )
        for row in rows:
            verify_row(row, f"Round275:{name}")
            regions[row["reverse_rechart_region_row_id"]] = row
    need(len(regions) == 13_788, "Round275 region universe")

    guards: dict[str, dict[str, Any]] = {}
    for key, name in (
        ("R174", "chart_guard_rejection_rows"),
        ("R179", "chart_guard_child_rows"),
    ):
        document = read_json(key)
        for row in unpack(document, name):
            need(row["row_id"] not in guards, "unique source guard")
            guards[row["row_id"]] = row
    need(len(guards) == 880, "source guard universe")
    need(
        all(row["source_guard_row_id"] in guards for row in regions.values()),
        "every Round275 region source guard",
    )
    return regions, guards


def load_terminal_face_inputs(
    regions: dict[str, dict[str, Any]],
    guards: dict[str, dict[str, Any]],
) -> tuple[
    list[dict[str, Any]],
    dict[str, list[dict[str, Any]]],
    dict[str, list[dict[str, Any]]],
    dict[str, Q],
    dict[str, str],
]:
    r286 = read_gzip("R286")
    r286_rows = verify_table(r286, "rows", "row_count", "rows_sha256")
    need(len(r286_rows) == 7_616, "Round286 cell census")
    r286_by_id = {
        row["Round286_refinement_cell_id"]: row for row in r286_rows
    }
    need(len(r286_by_id) == len(r286_rows), "Round286 unique cell IDs")

    r287 = read_gzip("R287")
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

    r288 = read_gzip("R288")
    r288_rows = verify_table(r288, "rows", "row_count", "rows_sha256")
    need(len(r288_rows) == 332_016, "Round288 atom disposition census")
    atom_dispositions = {
        row["canonical_atom_id"]: row for row in r288_rows
    }
    formal_target_kind: dict[str, str] = {}
    for row in r288_rows:
        target = (
            row["existing_local_occurrence_row_id"]
            or row["reserved_candidate_occurrence_id__not_issued"]
        )
        need(target is not None, "Round288 final/reserved ID")
        kind = (
            "ROUND294_PRESERVED_EXISTING_OCCURRENCE"
            if row["existing_local_occurrence_row_id"]
            else "ROUND294_PROMOTED_ROUND288_CANONICAL_ATOM"
        )
        if target in formal_target_kind:
            need(formal_target_kind[target] == kind, "consistent target kind")
        formal_target_kind[target] = kind

    support_by_region: dict[str, list[dict[str, Any]]] = defaultdict(list)
    empty_by_region: dict[str, list[dict[str, Any]]] = defaultdict(list)
    upper_by_region: dict[str, Q] = {}

    for row in region_rows:
        region_id = row["Round275_region_id"]
        region = regions[region_id]
        coordinate_box = qbox(region["adjacent_rational_region_box"])
        recomputed = physical_t_square(
            coordinate_box, qbox(guards[row["source_guard_row_id"]]["box"])
        )
        committed = tuple(map(Q, row["physical_t_square_open_interval"]))
        need(recomputed == committed, "Round287 whole-region physical t-square")
        upper_by_region[region_id] = recomputed[1]
        if row["disposition"].startswith("EXACT_INCLUSION_ALIAS_"):
            atom = atom_dispositions[row["containing_atom_id"]]
            target = (
                atom["existing_local_occurrence_row_id"]
                or atom["reserved_candidate_occurrence_id__not_issued"]
            )
            support_by_region[region_id].append({
                "physical_t_square": recomputed,
                "ps_rectangle": (
                    coordinate_box[2],
                    coordinate_box[3],
                    coordinate_box[4],
                    coordinate_box[5],
                ),
                "target_ids": [target],
                "source_kind":
                    "ROUND287_WHOLE_REGION_INCLUSION_REPRESENTATION",
                "source_row_id":
                    row["Round287_region_disposition_row_id"],
            })

    for row in cell_rows:
        cell_id = row["Round286_refinement_cell_id"]
        source = r286_by_id[cell_id]
        need(
            source["Round275_region_id"] == row["Round275_region_id"]
            and source["cell_exact_box"] == row["coordinate_box"]
            and source["atom_occupancy_count"]
            == row["Round286_coordinate_occupancy_count"],
            "Round286/Round287 cell join",
        )
        region_id = row["Round275_region_id"]
        region = regions[region_id]
        coordinate_box = qbox(source["cell_exact_box"])
        recomputed = physical_t_square(
            coordinate_box,
            qbox(guards[region["source_guard_row_id"]]["box"]),
        )
        committed = tuple(map(Q, row["physical_t_square_open_interval"]))
        need(recomputed == committed, "Round287 cell physical t-square")
        ps = (
            coordinate_box[2],
            coordinate_box[3],
            coordinate_box[4],
            coordinate_box[5],
        )
        if row["signed_region_cell_state"] == EMPTY:
            extrema = row["active_factor_extremal_signs"]
            desired = region["active_factor_side_sign"]
            need(
                len(extrema) == 2
                and extrema[0] == extrema[1]
                and extrema[0] in {"STRICT_NEGATIVE", "STRICT_POSITIVE"}
                and extrema[0] != desired
                and not row["exact_inclusion_alias_lemma_satisfied"],
                "strict wrong-signed empty cell",
            )
            empty_by_region[region_id].append({
                "Round286_refinement_cell_id": cell_id,
                "Round287_refinement_cell_disposition_row_id":
                    row["Round287_refinement_cell_disposition_row_id"],
                "coordinate_box": coordinate_box,
                "physical_t_square": recomputed,
                "ps_rectangle": ps,
                "desired_active_factor_side_sign": desired,
                "active_factor_extremal_signs": extrema,
                "Round286_coordinate_occupancy_count":
                    row["Round286_coordinate_occupancy_count"],
                "containing_atom_id": row["containing_atom_id"],
            })
        elif row["disposition"].startswith("EXACT_INCLUSION_ALIAS_"):
            atom = atom_dispositions[row["containing_atom_id"]]
            target = (
                atom["existing_local_occurrence_row_id"]
                or atom["reserved_candidate_occurrence_id__not_issued"]
            )
            support_by_region[region_id].append({
                "physical_t_square": recomputed,
                "ps_rectangle": ps,
                "target_ids": [target],
                "source_kind":
                    "ROUND287_SIGNED_CELL_INCLUSION_REPRESENTATION",
                "source_row_id":
                    row["Round287_refinement_cell_disposition_row_id"],
            })

    r292 = read_gzip("R292A")
    r292_rows = verify_table(r292, "rows", "row_count", "rows_sha256")
    need(len(r292_rows) == 22_820, "Round292A ledger census")
    refinement_rows = [
        row for row in r292_rows if row.get("disposition") is not None
    ]
    need(len(refinement_rows) == 11_852, "Round292A refinement census")
    for row in refinement_rows:
        box = tuple(map(Q, row["exact_transformed_open_cell"]))
        if row["existing_occurrence_occupancy_count"]:
            targets = row["existing_occurrence_ids"]
            for target in targets:
                formal_target_kind.setdefault(
                    target, "ROUND294_EXISTING_REGISTRY_OCCURRENCE"
                )
            kind = "ROUND292A_EXISTING_REGISTRY_SUBCOVER"
        else:
            target = row["Round292_refined_new_support_component_id"]
            need(target is not None, "Round292A refined support target")
            formal_target_kind[target] = (
                "ROUND294_PROMOTED_ROUND292_REFINED_SUPPORT_COMPONENT"
            )
            targets = [target]
            kind = "ROUND292A_REFINED_NEW_SUPPORT_COMPONENT"
        support_by_region[row["Round275_region_id"]].append({
            "physical_t_square": (box[0], box[1]),
            "ps_rectangle": (box[2], box[3], box[4], box[5]),
            "target_ids": targets,
            "source_kind": kind,
            "source_row_id":
                row["Round292_R287_existing_overlap_refinement_cell_id"],
        })

    r289 = read_gzip("R289")
    relation_rows = verify_nested_table(
        r289["region_cell_relation_ledger"],
        "Round289_region_cell_relation_id",
        9_528,
        "Round289 relation ledger",
    )
    need(
        all(
            target in formal_target_kind
            for cells in support_by_region.values()
            for cell in cells
            for target in cell["target_ids"]
        ),
        "every terminal support target is formal after Round294",
    )
    return (
        relation_rows,
        support_by_region,
        empty_by_region,
        upper_by_region,
        formal_target_kind,
    )


def build() -> tuple[dict[str, Any], dict[str, Any]]:
    for key, expected in PINS.items():
        need(
            file_sha256(HERE / FILES[key]) == expected,
            f"input pin:{FILES[key]}",
        )
    round294 = verify_round294_seal()
    regions, guards = load_regions_and_guards()
    (
        relations,
        support_by_region,
        empty_by_region,
        upper_by_region,
        target_kind,
    ) = load_terminal_face_inputs(regions, guards)

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
            "Round289 relation area",
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
            need(hit is not None, "terminal support overlap")
            p_cuts.update(hit[:2])
            s_cuts.update(hit[2:])

        bound_rectangles: list[tuple[Q, Q, Q, Q]] = []
        gap_rectangles: list[tuple[Q, Q, Q, Q]] = []
        relation_physical_ids: list[str] = []
        relation_targets: set[str] = set()
        for p0, p1 in zip(sorted(p_cuts), sorted(p_cuts)[1:]):
            for s0, s1 in zip(sorted(s_cuts), sorted(s_cuts)[1:]):
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
                need(len(targets) == 1, "unique target physical subcell")
                target = targets[0]
                need(target in target_kind, "formal Round294 target")
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

        physical_area = rectangle_union_area(bound_rectangles)
        gap_area = rectangle_union_area(gap_rectangles)
        need(
            relation_area == physical_area + gap_area,
            "baseline terminal-face partition conservation",
        )
        physical_area_total += physical_area
        empty_area_total += gap_area
        actual_target_reference_count += len(relation_targets)
        if gap_rectangles:
            baseline_histogram["PARTIAL"] += 1
            need(len(gap_rectangles) == 1, "one exact gap per partial relation")
        else:
            baseline_histogram["FULL"] += 1

        piece_keys: list[tuple[str, str, tuple[Q, Q, Q, Q]]] = []
        for gap in gap_rectangles:
            hits: list[tuple[dict[str, Any], tuple[Q, Q, Q, Q]]] = []
            for empty in empty_by_region.get(region_id, []):
                if empty["physical_t_square"][1] != upper:
                    continue
                intersection = intersect_rect(gap, empty["ps_rectangle"])
                if intersection is not None:
                    hits.append((empty, intersection))
            need(hits, "every baseline gap has empty-side cover")
            need(
                rectangle_union_area([hit for _cell, hit in hits])
                == rect_area(gap),
                "per-gap empty-side exact cover",
            )
            for index, (_left_cell, left) in enumerate(hits):
                for _right_cell, right in hits[index + 1:]:
                    need(
                        intersect_rect(left, right) is None,
                        "per-gap empty-piece interiors disjoint",
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

    # Global empty-cell use is computed before rows are closed.  This proves
    # reuse partitions one cell rather than counting its area twice.
    pieces_by_cell: dict[
        str, list[dict[str, Any]]
    ] = defaultdict(list)
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
                    f"reused empty cell double-count:{cell_id}",
                )
        used_area = rectangle_union_area(rectangles)
        full_area = rect_area(pieces[0]["empty_cell"]["ps_rectangle"])
        use_class = (
            "FULL_EMPTY_CELL_FACE_USED"
            if used_area == full_area
            else "HALF_EMPTY_CELL_FACE_USED"
        )
        if used_area != full_area:
            need(2 * used_area == full_area, "exact half-used empty cell")
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
        "unique-cell/global gap area without double count",
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
    for raw in raw_relations:
        physical_area = raw.pop("physical_area")
        empty_area = raw.pop("empty_area")
        graph_area = raw.pop("graph_area")
        piece_keys = raw.pop("absence_piece_keys")
        relation_area = Q(raw["exact_relation_ps_area"])
        need(
            relation_area == physical_area + empty_area + graph_area,
            "corrected relation exact area conservation",
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
        key=lambda row: row[
            "Round295B_physical_incidence_binding_row_id"
        ]
    )
    absence_rows.sort(
        key=lambda row: row[
            "Round295B_wrong_signed_empty_no_binding_row_id"
        ]
    )
    graph_rows.sort(
        key=lambda row: row[
            "Round295B_graph_separated_no_binding_row_id"
        ]
    )
    corrected_rows.sort(
        key=lambda row: row[
            "Round295B_corrected_relation_disposition_row_id"
        ]
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
        "baseline/corrected relation census",
    )
    need(
        len(corrected_rows) == 9_528
        and len(physical_rows) == 11_448
        and len(absence_rows) == 468
        and len(graph_rows) == 288
        and actual_target_reference_count == 10_956,
        "Round295B row/target census",
    )
    need(
        gap_multiplicity == {1: 348, 2: 24, 3: 24}
        and len(pieces_by_cell) == 440
        and use_histogram == {1: 412, 2: 28}
        and reused_cells == 28
        and half_used_cells == 4,
        "empty-cell refinement/reuse census",
    )
    need(
        sign_histogram
        == {
            ("STRICT_NEGATIVE", "STRICT_NEGATIVE"): 236,
            ("STRICT_POSITIVE", "STRICT_POSITIVE"): 232,
        }
        and occupancy_histogram == {0: 316, 1: 152},
        "empty sign/coordinate occupancy census",
    )
    need(
        actual_relation_area == Q(851, 51_200)
        and graph_relation_area == Q(3, 12_800)
        and physical_area_total == Q(6_457, 409_600)
        and empty_area_total == Q(351, 409_600)
        and actual_relation_area == physical_area_total + empty_area_total,
        "global exact area conservation",
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
                for key, value in sorted(PINS.items())
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
                str(key): value for key, value in sorted(gap_multiplicity.items())
            },
            "empty_cell_use_multiplicity_histogram": {
                str(key): value for key, value in sorted(use_histogram.items())
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
                ledger["graph_separated_no_binding_ledger"]["rows_sha256"],
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
    persisted = json.loads(canonical(summary) + b"\n")
    claim = persisted.pop("result_sha256")
    need(claim == digest(persisted), "persisted result closure")
    return ledger, summary


def main() -> None:
    ledger, result = build()
    ledger_bytes = deterministic_gzip_bytes(ledger)
    result_bytes = canonical(result) + b"\n"
    atomic_write(LEDGER, ledger_bytes)
    atomic_write(RESULT, result_bytes)
    print(json.dumps({
        "status": result["status"],
        "corrected_relation_count":
            result["corrected_relation_census"]["relation_count"],
        "physical_incidence_binding_count":
            result["formal_credit_transition"][
                "formal_existing_occurrence_physical_incidence_binding_count"
            ],
        "wrong_signed_empty_piece_count":
            result["empty_side_closure"][
                "exact_wrong_signed_empty_intersection_piece_count"
            ],
        "R289_terminal_face_frontier_count":
            result["corrected_relation_census"][
                "remaining_R289_terminal_face_frontier_count"
            ],
        "ledger_file_sha256": hashlib.sha256(ledger_bytes).hexdigest(),
        "result_sha256": result["result_sha256"],
    }, sort_keys=True))


if __name__ == "__main__":
    main()
