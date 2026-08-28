#!/usr/bin/env python3
"""Materialize the post-Round228 source-G occurrence attachment frontier.

The output attaches Round208 open-region sides to the frozen Round225
known-connectivity sheet blocks where Round211 supplies an exact incidence.
Round179 resolved children, Round204 regions, and Round208 sheetless regions
remain explicitly unattached.  A known-connectivity block is never promoted
to a maximal physical component.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import gc
import hashlib
import json
import os
from pathlib import Path
import stat
import sys
import tempfile
from typing import Any, Iterable


sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
PREFIX = "cm2_round229_source_g_global_occurrence_known_block_frontier"
OUTPUT = HERE / f"{PREFIX}_certificate.json"
SCHEMA = "cm2.round229.source-g-global-occurrence-known-block-frontier.v1"
STATUS = (
    "CERTIFIED_53968_LOCAL_OCCURRENCE_ATTACHMENT_FRONTIER__"
    "35432_TO_7404_KEY_PURE_KNOWN_BLOCKS__18536_UNATTACHED__"
    "ZERO_GLOBAL_PROMOTION"
)

INPUTS = {
    "Round179_rows": (
        "cm2_round179_source_g_residual_tube_arrangement_rows.json",
        "f20b42c1fed781779b537b4d45bf44233eae1ed3ee620b95177a80f0eb2b5e42",
        "a5468800c1d89cd307a5a26c608550b04db79c64c562fb12bedb22d6cec308cb",
        "cm2.round179.source-g-residual-tube-arrangement-rows.v1",
        180_000_000,
    ),
    "Round204": (
        "cm2_round204_source_g_wall_return_signature_local_replacement_certificate.json",
        "e7e1c49bebcb8c01f0fb4b33af66e4f2a8de560f121cae65f4971b2fec3e1818",
        "ef106d06399094a453eb5e66d73a0022a9bb5343f8c4788b3a3fbc9177d45ccd",
        "cm2.round204.source-g-wall-return-signature-local-replacement.v1",
        20_000_000,
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
    "Round226": (
        "cm2_round226_source_g_chart_transition_contract_census_certificate.json",
        "226e1f350c53fe4d7357ba9a74850e21d5aee5d720c0ea714c460181a6c797e8",
        "8c2a8f0393b4d3d5b4b103e670e2e76b8c1a41f239c0cdc9f35c21ffc90bb088",
        "cm2.round226.source-g-chart-transition-contract-census.v1",
        30_000_000,
    ),
    "Round227": (
        "cm2_round227_source_g_sheet_symmetry_non_glue_audit_certificate.json",
        "fa8d518239d2f2d4eb993ac58c66ffe2b7d222fa8efd4d916689cebd05201461",
        "fe134a35a2bb601f79ed4b712eba0cdb9a01db696bf854a24678a006ab2036ba",
        "cm2.round227.source-g-sheet-symmetry-non-glue-audit.v1",
        50_000_000,
    ),
    "Round228": (
        "cm2_round228_source_g_sheet_atlas_overlap_exhaustion_certificate.json",
        "03bd2bf3d4a6f9c6694062c1f7409058a537a5d4e4742df4e67d485032615cd0",
        "8c220de4122ccdc9673f45a5cd82b5da28c64e47b87af01ee04723f971923550",
        "cm2.round228.source-g-sheet-atlas-overlap-exhaustion.v1",
        30_000_000,
    ),
}


class Round229Error(RuntimeError):
    pass


def need(value: bool, label: str) -> None:
    if not value:
        raise Round229Error(label)


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
        raise Round229Error(f"number:{label}:{token}")

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


def occurrence_row(
    *,
    gauge: str,
    source_row_id: str,
    key_id: str,
    key_ordinal: int,
    status: str,
    sheet_row_id: str | None = None,
    known_block_id: str | None = None,
) -> dict[str, Any]:
    return closed(
        {
            "occurrence_attachment_row_id":
                f"round229-occurrence:{digest([gauge, source_row_id])}",
            "local_occurrence_gauge": gauge,
            "local_occurrence_row_id": source_row_id,
            "official_key_id": key_id,
            "official_key_ordinal": key_ordinal,
            "Round211_sheet_row_id": sheet_row_id,
            "Round225_known_connectivity_block_id": known_block_id,
            "known_block_incidence_attachment_credit":
                1 if known_block_id is not None else 0,
            "attachment_status": status,
            "known_block_is_maximal_physical_component": False,
            "maximal_physical_component_assignment_credit": 0,
            "global_exact_key_fibre_exhausted": False,
            "global_exact_key_disposition_credit": 0,
        }
    )


def build(producer_sha256: str) -> dict[str, Any]:
    r216 = load("Round216")
    frontier216 = r216["formal_key_occurrence_exhaustion_frontier_ledger"]
    need(frontier216["row_count"] == 116, "Round216 key rows")
    key_rows_216 = {
        row["official_key_ordinal"]: row for row in frontier216["rows"]
    }
    need(len(key_rows_216) == 116, "Round216 key uniqueness")
    need(
        r216["local_3D_occurrence_census_without_physical_promotion"][
            "local_3D_occurrence_count"
        ] == 53_968,
        "Round216 local occurrence total",
    )

    r220 = load("Round220")
    delta220 = r220["Round216_boundary_blocker_delta"]
    need(
        delta220["coordinate_atlas_blocker_closed"] is True
        and delta220["Round220_atlased_resolved_child_count"] == 17_192
        and delta220["remaining_unatlased_Round179_resolved_child_count"] == 0,
        "Round220 boundary delta",
    )
    tables220 = r220["coordinate_boundary_atlas"]["tables"]
    boundary_event_counts: dict[str, int] = {}
    for table_name, expected in (
        ("coordinate_face_rows", 103_152),
        ("coordinate_edge_rows", 206_304),
        ("coordinate_corner_rows", 137_536),
    ):
        table = tables220[table_name]
        need(table["row_count"] == expected, f"Round220 count:{table_name}")
        event_index = table["columns"].index("event_sheet_incidence_count")
        coordinate_index = table["columns"].index("coordinate_stratum_only")
        event_total = sum(row[event_index] for row in table["rows"])
        need(event_total == 0, f"Round220 event zero:{table_name}")
        need(
            all(row[coordinate_index] is True for row in table["rows"]),
            f"Round220 coordinate-only:{table_name}",
        )
        boundary_event_counts[table_name] = event_total
    columns220 = r220["per_key_coordinate_coverage_ledger"]["columns"]
    rows220 = r220["per_key_coordinate_coverage_ledger"]["rows"]
    map220 = {
        row[columns220.index("official_key_ordinal")]: dict(zip(columns220, row))
        for row in rows220
    }
    need(
        len(map220) == 116
        and set(map220) == set(key_rows_216)
        and all(row["coordinate_boundary_atlas_complete"] is True for row in map220.values())
        and sum(row["resolved_child_count"] for row in map220.values()) == 17_192,
        "Round220 per-key coverage",
    )
    split_table220 = tables220["one_step_split_interface_rows"]
    split_columns220 = split_table220["columns"]
    split_index220 = {
        name: split_columns220.index(name) for name in split_columns220
    }
    resolved_retained_interfaces: list[dict[str, Any]] = []
    for row in split_table220["rows"]:
        lower_kind = row[split_index220["lower_child_kind"]]
        upper_kind = row[split_index220["upper_child_kind"]]
        if {lower_kind, upper_kind} != {"RESOLVED", "RETAINED"}:
            continue
        if lower_kind == "RESOLVED":
            resolved_id = row[split_index220["lower_child_row_id"]]
            retained_id = row[split_index220["upper_child_row_id"]]
        else:
            resolved_id = row[split_index220["upper_child_row_id"]]
            retained_id = row[split_index220["lower_child_row_id"]]
        need(
            row[split_index220["event_trace_materialized_on_interface"]] is False
            and row[split_index220["physical_glue_credit"]] == 0
            and row[split_index220["whole_origin_credit"]] == 0
            and row[split_index220["global_exact_key_disposition_credit"]] == 0,
            "Round220 resolved-retained nonpromotion",
        )
        resolved_retained_interfaces.append(
            {
                "split_interface_id": row[split_index220["split_interface_id"]],
                "resolved_child_row_id": resolved_id,
                "retained_child_row_id": retained_id,
                "axis": row[split_index220["axis"]],
                "fixed_coordinate": row[split_index220["fixed_coordinate"]],
            }
        )
    need(
        len(resolved_retained_interfaces) == 8_960
        and len({row["split_interface_id"] for row in resolved_retained_interfaces}) == 8_960
        and len({row["resolved_child_row_id"] for row in resolved_retained_interfaces}) == 8_960
        and len({row["retained_child_row_id"] for row in resolved_retained_interfaces}) == 8_960,
        "Round220 resolved-retained frontier",
    )
    del r220, tables220, rows220
    gc.collect()

    r179 = load("Round179_rows")
    schema179 = r179["row_column_schemas"]["resolved_3d_child_rows"]
    resolved179 = r179["resolved_3d_child_rows"]
    need(len(resolved179) == 17_192, "Round179 resolved rows")
    index179 = {name: schema179.index(name) for name in (
        "row_id", "official_key_ordinal", "official_key_id"
    )}
    resolved_key: dict[str, tuple[int, str]] = {}
    occurrence_rows: list[dict[str, Any]] = []
    for source in sorted(resolved179, key=lambda row: row[index179["row_id"]]):
        ordinal = source[index179["official_key_ordinal"]]
        need(ordinal in key_rows_216, "Round179 observed key")
        resolved_key[source[index179["row_id"]]] = (
            ordinal,
            source[index179["official_key_id"]],
        )
        occurrence_rows.append(
            occurrence_row(
                gauge="ROUND179_RESOLVED_CHILD",
                source_row_id=source[index179["row_id"]],
                key_id=source[index179["official_key_id"]],
                key_ordinal=ordinal,
                status=(
                    "COORDINATE_BOUNDARY_ATLAS_COMPLETE__"
                    "ALL_BOUNDARY_STRATA_COORDINATE_ONLY__"
                    "NO_KNOWN_BLOCK_INCIDENCE"
                ),
            )
        )
    del r179, resolved179
    gc.collect()

    r204 = load("Round204")
    regions204 = r204["formal_local_open_3D_region_ledger"]["rows"]
    need(len(regions204) == 736, "Round204 region rows")
    for source in sorted(regions204, key=lambda row: row["region_row_id"]):
        ordinal = source["official_key_ordinal"]
        need(
            key_rows_216[ordinal]["local_lower_dimensional_atlas_source"]
            == "ROUND204_SEPARATE_FORMAL_DIMENSIONAL_GAUGE",
            "Round204 gauge class",
        )
        occurrence_rows.append(
            occurrence_row(
                gauge="ROUND204_STRICT_OPEN_REGION",
                source_row_id=source["region_row_id"],
                key_id=source["official_key_id"],
                key_ordinal=ordinal,
                status=(
                    "SEPARATE_FORMAL_DIMENSIONAL_GAUGE__"
                    "NO_ROUND211_SHEET_OR_KNOWN_BLOCK_INCIDENCE"
                ),
            )
        )
    del r204, regions204
    gc.collect()

    r208 = load("Round208")
    bases208 = r208["formal_direct_leaf_signature_base_ledger"]["rows"]
    regions208 = r208["formal_local_open_3D_signature_ledger"]["rows"]
    need(len(bases208) == 18_324 and len(regions208) == 36_040, "Round208 census")
    leaf_key: dict[str, tuple[int, str]] = {}
    for base in bases208:
        direct = base["direct_signature_base"]
        leaf_key[base["leaf_row_id"]] = (
            direct["official_key_ordinal"],
            direct["official_key_id"],
        )
    compact_regions208: dict[str, tuple[int, str, str]] = {}
    retained_regions208: dict[str, list[str]] = defaultdict(list)
    for region in regions208:
        signature = region["local_return_signature"]
        compact_regions208[region["region_row_id"]] = (
            signature["official_key_ordinal"],
            signature["official_key_id"],
            region["leaf_row_id"],
        )
        retained_regions208[region["retained_child_row_id"]].append(
            region["region_row_id"]
        )
    need(
        len(leaf_key) == 18_324 and len(compact_regions208) == 36_040,
        "Round208 unique IDs",
    )
    del r208, bases208, regions208
    gc.collect()

    r211 = load("Round211")
    sheets211 = r211["formal_2D_sheet_owner_ledger"]["rows"]
    need(len(sheets211) == 17_716, "Round211 sheets")
    region_to_sheet: dict[str, str] = {}
    sheet_to_leaf: dict[str, str] = {}
    for sheet in sheets211:
        sheet_id = sheet["sheet_row_id"]
        leaf_id = sheet["leaf_row_id"]
        need(sheet_id not in sheet_to_leaf and leaf_id in leaf_key, "Round211 IDs")
        sheet_to_leaf[sheet_id] = leaf_id
        for region_id in (
            sheet["owner_region_row_id"],
            sheet["shadow_region_row_id"],
        ):
            need(
                region_id in compact_regions208 and region_id not in region_to_sheet,
                "Round211 region incidence partition",
            )
            need(
                compact_regions208[region_id][:2] == leaf_key[leaf_id],
                "Round211 region key",
            )
            region_to_sheet[region_id] = sheet_id
    need(
        len(region_to_sheet) == 35_432
        and len(set(compact_regions208) - set(region_to_sheet)) == 608,
        "Round211 2*sheet+sheetless identity",
    )
    del r211, sheets211
    gc.collect()

    r225 = load("Round225")
    assignments225 = r225["formal_Round211_sheet_assignment_ledger"]["rows"]
    need(len(assignments225) == 17_716, "Round225 assignments")
    sheet_to_block: dict[str, str] = {}
    block_keys: dict[str, set[int]] = defaultdict(set)
    block_members: dict[str, list[str]] = defaultdict(list)
    key_sheet_ids: dict[int, list[str]] = defaultdict(list)
    for assignment in assignments225:
        sheet_id = assignment["Round211_sheet_row_id"]
        block_id = assignment["known_connectivity_block_id"]
        need(sheet_id in sheet_to_leaf and sheet_id not in sheet_to_block, "Round225 sheet")
        ordinal = leaf_key[sheet_to_leaf[sheet_id]][0]
        sheet_to_block[sheet_id] = block_id
        block_keys[block_id].add(ordinal)
        block_members[block_id].append(sheet_id)
        key_sheet_ids[ordinal].append(sheet_id)
    need(
        set(sheet_to_block) == set(sheet_to_leaf)
        and len(block_keys) == 7_404
        and all(len(keys) == 1 for keys in block_keys.values()),
        "Round225 key-pure blocks",
    )
    delta225 = r225["known_connectivity_delta"]
    audit225 = r225["rebuilt_frontier_audit"]
    need(
        delta225["block_count_after_Round224"] == 7_404
        and delta225["raw_Round211_sheet_row_count"] == 17_716
        and audit225["remaining_missing_contact_frontier_count"] == 0
        and audit225["all_exact_p_s_and_partial_contact_proof_gaps_closed"] is True,
        "Round225 closure",
    )
    del r225, assignments225
    gc.collect()

    for region_id in sorted(compact_regions208):
        ordinal, key_id, _leaf_id = compact_regions208[region_id]
        sheet_id = region_to_sheet.get(region_id)
        if sheet_id is None:
            occurrence_rows.append(
                occurrence_row(
                    gauge="ROUND208_STRICT_OPEN_REGION",
                    source_row_id=region_id,
                    key_id=key_id,
                    key_ordinal=ordinal,
                    status=(
                        "SHEETLESS_LOCAL_REGION__"
                        "NO_ROUND211_SHEET_OR_KNOWN_BLOCK_INCIDENCE"
                    ),
                )
            )
        else:
            occurrence_rows.append(
                occurrence_row(
                    gauge="ROUND208_STRICT_OPEN_REGION",
                    source_row_id=region_id,
                    key_id=key_id,
                    key_ordinal=ordinal,
                    sheet_row_id=sheet_id,
                    known_block_id=sheet_to_block[sheet_id],
                    status=(
                        "ATTACHED_TO_CERTIFIED_KNOWN_CONNECTIVITY_SHEET_BLOCK__"
                        "NOT_A_MAXIMAL_PHYSICAL_COMPONENT_ASSIGNMENT"
                    ),
                )
            )

    lineage_rows: list[dict[str, Any]] = []
    per_key_lineage: dict[int, Counter[str]] = defaultdict(Counter)
    for interface in sorted(
        resolved_retained_interfaces,
        key=lambda row: row["split_interface_id"],
    ):
        resolved_id = interface["resolved_child_row_id"]
        retained_id = interface["retained_child_row_id"]
        need(resolved_id in resolved_key, "Round220 resolved lineage ID")
        ordinal, key_id = resolved_key[resolved_id]
        region_ids = sorted(retained_regions208.get(retained_id, []))
        sheet_ids = sorted({
            region_to_sheet[region_id]
            for region_id in region_ids
            if region_id in region_to_sheet
        })
        block_ids = sorted({sheet_to_block[sheet_id] for sheet_id in sheet_ids})
        if region_ids:
            need(
                all(compact_regions208[region_id][:2] == (ordinal, key_id)
                    for region_id in region_ids),
                "Round220 retained lineage key identity",
            )
            per_key_lineage[ordinal]["with_Round208_materialization"] += 1
        if block_ids:
            status = (
                "COORDINATE_LINEAGE_ONLY_TO_KEY_PURE_KNOWN_BLOCK_REFERENCE__"
                "EVENT_TRACE_FALSE__UNION_FORBIDDEN"
            )
            per_key_lineage[ordinal]["with_known_block_reference"] += 1
        elif region_ids:
            status = (
                "COORDINATE_LINEAGE_ONLY_TO_SHEETLESS_ROUND208_REGIONS__"
                "EVENT_TRACE_FALSE__UNION_FORBIDDEN"
            )
        else:
            status = (
                "RETAINED_SIDE_NOT_MATERIALIZED_IN_ROUND208__"
                "EVENT_TRACE_FALSE__UNION_FORBIDDEN"
            )
        per_key_lineage[ordinal]["total"] += 1
        per_key_lineage[ordinal]["referenced_region_sides"] += len(region_ids)
        per_key_lineage[ordinal]["referenced_sheet_sides"] += sum(
            region_id in region_to_sheet for region_id in region_ids
        )
        lineage_rows.append(
            closed(
                {
                    "lineage_frontier_row_id":
                        f"round229-lineage:{interface['split_interface_id'].split(':', 1)[1]}",
                    "Round220_split_interface_id":
                        interface["split_interface_id"],
                    "resolved_child_row_id": resolved_id,
                    "retained_child_row_id": retained_id,
                    "axis": interface["axis"],
                    "fixed_coordinate": interface["fixed_coordinate"],
                    "official_key_ordinal": ordinal,
                    "official_key_id": key_id,
                    "Round208_retained_region_count": len(region_ids),
                    "Round208_retained_region_ids_sha256": digest(region_ids),
                    "Round211_incident_sheet_count": len(sheet_ids),
                    "Round211_incident_sheet_ids_sha256": digest(sheet_ids),
                    "Round225_referenced_known_block_count": len(block_ids),
                    "Round225_referenced_known_block_ids_sha256":
                        digest(block_ids),
                    "lineage_status": status,
                    "event_trace_materialized_on_interface": False,
                    "coordinate_lineage_is_physical_edge": False,
                    "physical_union_credit": 0,
                    "maximal_physical_component_assignment_credit": 0,
                    "global_exact_key_disposition_credit": 0,
                }
            )
        )
    need(
        len(lineage_rows) == 8_960
        and sum(
            row["Round208_retained_region_count"] > 0
            for row in lineage_rows
        ) == 460
        and sum(
            row["Round225_referenced_known_block_count"] > 0
            for row in lineage_rows
        ) == 456
        and sum(
            row["Round208_retained_region_count"]
            for row in lineage_rows
        ) == 1_536
        and sum(
            row["Round211_incident_sheet_count"]
            for row in lineage_rows
        ) == 740,
        "Round220 lineage frontier census",
    )

    r226 = load("Round226")
    census226 = r226["census"]
    need(
        census226["event_trace_candidate_absence_proved_within_Round220_rejected_pool_count"] == 9_830
        and census226["coordinate_region_identity_candidates_remaining_eligible_for_event_trace_glue"] == 0
        and census226["physical_glue_credit_count"] == 0,
        "Round226 exclusion",
    )
    del r226
    gc.collect()

    r227 = load("Round227")
    census227 = r227["census"]
    need(
        census227["sheet_count"] == 17_716
        and census227["directed_partner_row_count"] == 35_432
        and census227["Klein_orbit_count"] == 4_429
        and census227["Jx_Jy_commutation_failure_count"] == 0
        and census227["cross_orbit_generator_edge_count"] == 0
        and census227["component_union_credit"] == 0
        and r227["map_contract"]["symmetry_partner_is_same_physical_point_atlas_transition"] is False,
        "Round227 non-glue",
    )
    del r227
    gc.collect()

    r228 = load("Round228")
    census228 = r228["census"]
    need(
        census228["Round211_sheet_count"] == 17_716
        and census228["source_chart_seam_overlap_candidate_count"] == 0
        and census228["outgoing_chart_unowned_or_multiply_owned_count"] == 0
        and census228["unclassified_atlas_overlap_channel_count"] == 0
        and census228["new_component_union_credit"] == 0
        and r228["scope_contract"]["all_future_retained_strata_exhausted"] is False,
        "Round228 atlas scope",
    )
    del r228
    gc.collect()

    need(len(occurrence_rows) == 53_968, "Round229 occurrence total")
    need(
        len({row["local_occurrence_row_id"] for row in occurrence_rows}) == 53_968,
        "globally unique occurrence source IDs",
    )
    gauge_counts = Counter(row["local_occurrence_gauge"] for row in occurrence_rows)
    attached = [
        row for row in occurrence_rows
        if row["known_block_incidence_attachment_credit"] == 1
    ]
    need(
        gauge_counts == Counter({
            "ROUND179_RESOLVED_CHILD": 17_192,
            "ROUND204_STRICT_OPEN_REGION": 736,
            "ROUND208_STRICT_OPEN_REGION": 36_040,
        })
        and len(attached) == 35_432
        and len(occurrence_rows) - len(attached) == 18_536,
        "Round229 attachment census",
    )

    aggregates: dict[int, Counter[str]] = defaultdict(Counter)
    key_block_ids: dict[int, set[str]] = defaultdict(set)
    for row in occurrence_rows:
        ordinal = row["official_key_ordinal"]
        aggregates[ordinal]["total"] += 1
        aggregates[ordinal][row["local_occurrence_gauge"]] += 1
        if row["known_block_incidence_attachment_credit"] == 1:
            aggregates[ordinal]["attached"] += 1
            key_block_ids[ordinal].add(row["Round225_known_connectivity_block_id"])
        else:
            aggregates[ordinal]["unattached"] += 1

    per_key_rows: list[dict[str, Any]] = []
    for ordinal in sorted(key_rows_216):
        old = key_rows_216[ordinal]
        counts = aggregates[ordinal]
        block_ids = sorted(key_block_ids[ordinal])
        sheet_ids = sorted(key_sheet_ids[ordinal])
        need(
            counts["total"] == old["local_3D_occurrence_count"],
            f"per-key total:{ordinal}",
        )
        need(
            counts["ROUND179_RESOLVED_CHILD"]
            == old["Round179_resolved_child_occurrence_count"]
            and counts["ROUND204_STRICT_OPEN_REGION"]
            == old["Round204_strict_local_region_occurrence_count"]
            and counts["ROUND208_STRICT_OPEN_REGION"]
            == old["Round208_strict_local_region_occurrence_count"],
            f"per-key gauge totals:{ordinal}",
        )
        need(
            counts["attached"] == 2 * len(sheet_ids),
            f"per-key sheet-side identity:{ordinal}",
        )
        per_key_rows.append(
            closed(
                {
                    "key_frontier_row_id":
                        f"round229-key-frontier:{ordinal:06d}:{digest(old['official_key_id'])}",
                    "official_key_ordinal": ordinal,
                    "official_key_id": old["official_key_id"],
                    "official_key_row": old["official_key_row"],
                    "Round216_classification": old["classification"],
                    "Round216_local_lower_dimensional_atlas_source":
                        old["local_lower_dimensional_atlas_source"],
                    "local_occurrence_count": counts["total"],
                    "Round179_resolved_child_occurrence_count":
                        counts["ROUND179_RESOLVED_CHILD"],
                    "Round204_strict_open_region_count":
                        counts["ROUND204_STRICT_OPEN_REGION"],
                    "Round208_strict_open_region_count":
                        counts["ROUND208_STRICT_OPEN_REGION"],
                    "Round220_coordinate_boundary_atlas_complete":
                        map220[ordinal]["coordinate_boundary_atlas_complete"],
                    "Round211_sheet_count": len(sheet_ids),
                    "Round211_sheet_side_occurrence_count": counts["attached"],
                    "Round225_key_pure_known_block_count": len(block_ids),
                    "Round225_key_pure_known_block_ids_sha256": digest(block_ids),
                    "Round211_sheet_ids_sha256": digest(sheet_ids),
                    "occurrences_with_known_block_incidence": counts["attached"],
                    "occurrences_without_known_block_incidence": counts["unattached"],
                    "Round220_resolved_retained_interface_count":
                        per_key_lineage[ordinal]["total"],
                    "Round220_interface_with_Round208_materialization_count":
                        per_key_lineage[ordinal]["with_Round208_materialization"],
                    "Round220_interface_with_known_block_reference_count":
                        per_key_lineage[ordinal]["with_known_block_reference"],
                    "known_blocks_are_maximal_physical_components": False,
                    "global_exact_key_fibre_exhausted": False,
                    "global_exact_key_disposition_credit": 0,
                }
            )
        )

    need(
        len(per_key_rows) == 116
        and sum(row["local_occurrence_count"] for row in per_key_rows) == 53_968
        and sum(row["Round211_sheet_count"] for row in per_key_rows) == 17_716
        and sum(row["Round225_key_pure_known_block_count"] for row in per_key_rows) == 7_404
        and sum(row["occurrences_with_known_block_incidence"] for row in per_key_rows) == 35_432
        and sum(row["occurrences_without_known_block_incidence"] for row in per_key_rows) == 18_536,
        "per-key conservation",
    )
    sheet_key_count = sum(row["Round211_sheet_count"] > 0 for row in per_key_rows)
    need(sheet_key_count == 24, "Round211 key count")

    input_binding = {
        label: {
            "filename": values[0],
            "certificate_or_attachment_sha256": values[1],
            "result_sha256": values[2],
            "schema": values[3],
        }
        for label, values in INPUTS.items()
    }
    return {
        "status": STATUS,
        "formal_input_binding": input_binding,
        "formal_occurrence_known_block_attachment_frontier_ledger":
            ledger(occurrence_rows, "occurrence_attachment_row_id"),
        "formal_per_key_post_Round228_frontier_ledger":
            ledger(per_key_rows, "key_frontier_row_id"),
        "formal_Round220_resolved_retained_coordinate_lineage_frontier_ledger":
            ledger(lineage_rows, "lineage_frontier_row_id"),
        "census": {
            "observed_official_key_count": 116,
            "local_occurrence_count": 53_968,
            "Round179_resolved_child_occurrence_count": 17_192,
            "Round204_strict_open_region_occurrence_count": 736,
            "Round208_strict_open_region_occurrence_count": 36_040,
            "Round208_leaf_count": 18_324,
            "Round211_sheet_count": 17_716,
            "Round211_sheet_side_occurrence_count": 35_432,
            "Round208_sheetless_occurrence_count": 608,
            "Round208_identity": "36040=2*17716+608",
            "occurrences_with_known_block_incidence": 35_432,
            "occurrences_without_known_block_incidence": 18_536,
            "Round225_key_pure_known_block_count": 7_404,
            "Round225_mixed_key_known_block_count": 0,
            "keys_with_Round211_sheet_and_known_block_incidence": 24,
            "keys_without_Round211_sheet_or_known_block_incidence": 92,
            "Round220_resolved_retained_interface_count": 8_960,
            "Round220_interface_with_Round208_materialization_count": 460,
            "Round220_interface_with_known_block_reference_count": 456,
            "Round220_interface_with_only_sheetless_Round208_regions_count": 4,
            "Round220_interface_without_Round208_materialization_count": 8_500,
            "Round220_lineage_referenced_Round208_region_side_count": 1_536,
            "Round220_lineage_referenced_Round211_sheet_count": 740,
            "Round220_lineage_event_trace_materialized_count": 0,
            "Round220_lineage_physical_union_credit": 0,
            "Round220_coordinate_boundary_face_event_sheet_incidence_count":
                boundary_event_counts["coordinate_face_rows"],
            "Round220_coordinate_boundary_edge_event_sheet_incidence_count":
                boundary_event_counts["coordinate_edge_rows"],
            "Round220_coordinate_boundary_corner_event_sheet_incidence_count":
                boundary_event_counts["coordinate_corner_rows"],
            "maximal_physical_component_assignment_count": 0,
            "globally_exhausted_observed_key_fibre_count": 0,
            "global_exact_key_disposition_credit": 0,
        },
        "post_Round216_blocker_delta": {
            "Round179_resolved_child_coordinate_boundary_atlas":
                "CLOSED_17192_OF_17192_BY_ROUND220",
            "frozen_Round211_exact_contact_frontier":
                "CLOSED_7932_OF_7932_BY_ROUND223",
            "frozen_Round211_partial_contact_frontier":
                "CLOSED_264_OF_264_BY_ROUND224",
            "frozen_Round211_missing_contact_frontier":
                "CLOSED_ZERO_REMAINING_BY_ROUND225",
            "Round220_rejected_coordinate_pool_event_trace_channel":
                "CLOSED_AS_NONEDGE_9830_OF_9830_BY_ROUND226",
            "Round211_Klein_symmetry_channel":
                "CLOSED_AS_NON_GLUE_35432_DIRECTED_PARTNERS_BY_ROUND227",
            "Round211_materialized_sheet_true_atlas_overlap_channel":
                "CLOSED_ZERO_UNCLASSIFIED_BY_ROUND228",
            "global_occurrence_to_maximal_physical_component_assignment":
                "OPEN_53968_OF_53968",
            "known_block_incidence_is_only_a_lower_bound_attachment":
                "35432_OCCURRENCES_TO_7404_KEY_PURE_KNOWN_BLOCKS",
            "no_known_block_incidence":
                "18536_OCCURRENCES",
            "resolved_to_retained_exact_event_trace_bridge":
                "OPEN_8960_OF_8960__456_HAVE_COORDINATE_ONLY_BLOCK_REFERENCES",
        },
        "scope_contract": {
            "all_53968_local_occurrences_are_explicitly_accounted": True,
            "Round208_sheet_side_incidence_partition_is_exact": True,
            "Round225_known_blocks_are_key_pure": True,
            "Round220_coordinate_lineage_reference_is_not_a_physical_edge": True,
            "known_block_incidence_is_not_component_assignment": True,
            "known_connectivity_blocks_are_maximal_physical_components": False,
            "current_materialized_Round211_contact_and_atlas_channels_closed": True,
            "all_future_retained_event_strata_exhausted": False,
            "global_occurrence_fibre_completeness_proved": False,
        },
        "strict_nonpromotion": {
            "known_connectivity_blocks": 7_404,
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
            "materialize maximal-component candidate attachments for the "
            "18536 occurrences with no Round225 known-block incidence, starting "
            "with exact event-trace/common-refinement classification of all "
            "8960 resolved-retained one-step interfaces; prove "
            "that the 7404 known blocks are complete against every retained "
            "event stratum, then independently rebuild all 116 occurrence "
            "fibres before any global exact-key disposition credit"
        ),
        "provenance": {
            "schema": SCHEMA,
            "producer_sha256": producer_sha256,
            "python_version": sys.version.split()[0],
        },
    }


def safe_write(data: bytes) -> None:
    descriptor, name = tempfile.mkstemp(
        prefix=f".{OUTPUT.name}.",
        suffix=".tmp",
        dir=HERE,
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
    parser = argparse.ArgumentParser()
    parser.add_argument("--no-write", action="store_true")
    args = parser.parse_args()
    producer_sha = hashlib.sha256(
        regular_bytes(Path(__file__), 5_000_000)
    ).hexdigest()
    result = build(producer_sha)
    envelope = {
        "schema": SCHEMA,
        "result": result,
        "result_sha256": digest(result),
    }
    encoded = canonical(envelope) + b"\n"
    if not args.no_write:
        safe_write(encoded)
    print(result["status"])
    print(f"producer_sha256={producer_sha}")
    print(f"result_sha256={envelope['result_sha256']}")
    print(f"certificate_sha256={hashlib.sha256(encoded).hexdigest()}")
    print("occurrences=53968 attached_known_block=35432 unattached=18536")
    print("known_blocks=7404 mixed_key_blocks=0 global_fibres=0/116")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
