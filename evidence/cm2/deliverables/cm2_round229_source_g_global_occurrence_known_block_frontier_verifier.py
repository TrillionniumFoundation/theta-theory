#!/usr/bin/env python3
"""Independently verify the Round229 occurrence attachment frontier.

The verifier never imports or executes the producer.  It builds compact
source-ID maps from the pinned upstream certificates, validates every
Round229 occurrence, key, and one-step-lineage row against those maps, and
recomputes all ledger and envelope digests.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import copy
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
PRODUCER = HERE / f"{PREFIX}.py"
CANDIDATE = HERE / f"{PREFIX}_certificate.json"
OUTPUT = HERE / f"{PREFIX}_verification.json"
SCHEMA = "cm2.round229.source-g-global-occurrence-known-block-frontier.v1"
VERIFICATION_SCHEMA = f"{SCHEMA}.verification.v1"
PRODUCER_SHA = "2518319a103acacc0b6a3dbdd165d9cefd3656d6c323063094daa598bede454c"
CANDIDATE_SHA = "c4152f4764ed7fe977046ef728e8257344803433053e06c0ac11ec68b86ff11a"
CANDIDATE_RESULT = "936e140d7113dbdd565f4b1a9381de3b90313e7198266c1950532b80ba153230"
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


class VerificationError(RuntimeError):
    pass


def need(value: bool, label: str) -> None:
    if not value:
        raise VerificationError(label)


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


def close(payload: dict[str, Any]) -> dict[str, Any]:
    row = dict(payload)
    row["row_sha256"] = digest(row)
    return row


def expected_ledger(rows: list[dict[str, Any]], id_field: str) -> dict[str, Any]:
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


def strict_json(raw: bytes, label: str = "candidate") -> dict[str, Any]:
    def pairs(items: list[tuple[str, Any]]) -> dict[str, Any]:
        output: dict[str, Any] = {}
        for key, value in items:
            need(key not in output, f"duplicate:{label}:{key}")
            output[key] = value
        return output

    def reject(token: str) -> None:
        raise VerificationError(f"number:{label}:{token}")

    value = json.loads(
        raw,
        object_pairs_hook=pairs,
        parse_float=reject,
        parse_constant=reject,
    )
    need(isinstance(value, dict), f"object:{label}")
    try:
        canonical(value).decode("utf-8")
    except (UnicodeEncodeError, UnicodeDecodeError) as error:
        raise VerificationError(f"unicode:{label}") from error
    return value


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


def model() -> dict[str, Any]:
    r216 = load("Round216")
    keys216 = {
        row["official_key_ordinal"]: row
        for row in r216["formal_key_occurrence_exhaustion_frontier_ledger"]["rows"]
    }
    need(
        len(keys216) == 116
        and sum(row["local_3D_occurrence_count"] for row in keys216.values()) == 53_968,
        "Round216 key universe",
    )

    r220 = load("Round220")
    need(
        r220["Round216_boundary_blocker_delta"]["coordinate_atlas_blocker_closed"] is True
        and r220["Round216_boundary_blocker_delta"][
            "remaining_unatlased_Round179_resolved_child_count"
        ] == 0,
        "Round220 atlas delta",
    )
    tables = r220["coordinate_boundary_atlas"]["tables"]
    boundary_counts: dict[str, int] = {}
    for name, expected in (
        ("coordinate_face_rows", 103_152),
        ("coordinate_edge_rows", 206_304),
        ("coordinate_corner_rows", 137_536),
    ):
        table = tables[name]
        columns = table["columns"]
        event = columns.index("event_sheet_incidence_count")
        physical = columns.index("physical_glue_credit")
        coordinate = columns.index("coordinate_stratum_only")
        need(
            table["row_count"] == expected
            and all(row[event] == 0 for row in table["rows"])
            and all(row[physical] == 0 for row in table["rows"])
            and all(row[coordinate] is True for row in table["rows"]),
            f"Round220 coordinate-only:{name}",
        )
        boundary_counts[name] = 0
    per_key_table = r220["per_key_coordinate_coverage_ledger"]
    per_key_columns = per_key_table["columns"]
    per_key220 = {
        row[per_key_columns.index("official_key_ordinal")]:
            dict(zip(per_key_columns, row))
        for row in per_key_table["rows"]
    }
    need(
        set(per_key220) == set(keys216)
        and all(row["coordinate_boundary_atlas_complete"] is True
                for row in per_key220.values()),
        "Round220 per-key coverage",
    )
    split = tables["one_step_split_interface_rows"]
    split_index = {name: split["columns"].index(name) for name in split["columns"]}
    interfaces: list[dict[str, Any]] = []
    for row in split["rows"]:
        lower = row[split_index["lower_child_kind"]]
        upper = row[split_index["upper_child_kind"]]
        if {lower, upper} != {"RESOLVED", "RETAINED"}:
            continue
        resolved_id = row[
            split_index[
                "lower_child_row_id" if lower == "RESOLVED"
                else "upper_child_row_id"
            ]
        ]
        retained_id = row[
            split_index[
                "upper_child_row_id" if upper == "RETAINED"
                else "lower_child_row_id"
            ]
        ]
        need(
            row[split_index["event_trace_materialized_on_interface"]] is False
            and row[split_index["physical_glue_credit"]] == 0
            and row[split_index["global_exact_key_disposition_credit"]] == 0,
            "Round220 lineage nonedge",
        )
        interfaces.append({
            "split_interface_id": row[split_index["split_interface_id"]],
            "resolved_child_row_id": resolved_id,
            "retained_child_row_id": retained_id,
            "axis": row[split_index["axis"]],
            "fixed_coordinate": row[split_index["fixed_coordinate"]],
        })
    need(
        len(interfaces) == 8_960
        and len({row["split_interface_id"] for row in interfaces}) == 8_960,
        "Round220 interface frontier",
    )
    del r220, tables
    gc.collect()

    r179 = load("Round179_rows")
    columns179 = r179["row_column_schemas"]["resolved_3d_child_rows"]
    index179 = {name: columns179.index(name) for name in (
        "row_id", "official_key_ordinal", "official_key_id"
    )}
    resolved: dict[str, tuple[int, str]] = {}
    occurrence_specs: list[tuple[str, str, int, str]] = []
    for row in r179["resolved_3d_child_rows"]:
        row_id = row[index179["row_id"]]
        ordinal = row[index179["official_key_ordinal"]]
        key_id = row[index179["official_key_id"]]
        need(row_id not in resolved and ordinal in keys216, "Round179 rows")
        resolved[row_id] = (ordinal, key_id)
        occurrence_specs.append((
            "ROUND179_RESOLVED_CHILD", row_id, ordinal, key_id
        ))
    need(len(resolved) == 17_192, "Round179 census")
    del r179
    gc.collect()

    r204 = load("Round204")
    for row in r204["formal_local_open_3D_region_ledger"]["rows"]:
        ordinal = row["official_key_ordinal"]
        need(
            keys216[ordinal]["local_lower_dimensional_atlas_source"]
            == "ROUND204_SEPARATE_FORMAL_DIMENSIONAL_GAUGE",
            "Round204 key gauge",
        )
        occurrence_specs.append((
            "ROUND204_STRICT_OPEN_REGION",
            row["region_row_id"],
            ordinal,
            row["official_key_id"],
        ))
    need(
        len(r204["formal_local_open_3D_region_ledger"]["rows"]) == 736,
        "Round204 census",
    )
    del r204
    gc.collect()

    r208 = load("Round208")
    leaf_key: dict[str, tuple[int, str]] = {}
    for row in r208["formal_direct_leaf_signature_base_ledger"]["rows"]:
        signature = row["direct_signature_base"]
        leaf_key[row["leaf_row_id"]] = (
            signature["official_key_ordinal"],
            signature["official_key_id"],
        )
    regions208: dict[str, tuple[int, str, str, str]] = {}
    retained_regions: dict[str, list[str]] = defaultdict(list)
    for row in r208["formal_local_open_3D_signature_ledger"]["rows"]:
        signature = row["local_return_signature"]
        info = (
            signature["official_key_ordinal"],
            signature["official_key_id"],
            row["leaf_row_id"],
            row["retained_child_row_id"],
        )
        need(row["region_row_id"] not in regions208, "Round208 region unique")
        regions208[row["region_row_id"]] = info
        retained_regions[row["retained_child_row_id"]].append(row["region_row_id"])
        occurrence_specs.append((
            "ROUND208_STRICT_OPEN_REGION",
            row["region_row_id"],
            info[0],
            info[1],
        ))
    need(len(leaf_key) == 18_324 and len(regions208) == 36_040, "Round208 census")
    del r208
    gc.collect()

    r211 = load("Round211")
    region_sheet: dict[str, str] = {}
    sheet_leaf: dict[str, str] = {}
    for row in r211["formal_2D_sheet_owner_ledger"]["rows"]:
        sheet_id = row["sheet_row_id"]
        leaf_id = row["leaf_row_id"]
        need(sheet_id not in sheet_leaf and leaf_id in leaf_key, "Round211 sheet")
        sheet_leaf[sheet_id] = leaf_id
        for region_id in (row["owner_region_row_id"], row["shadow_region_row_id"]):
            need(
                region_id in regions208 and region_id not in region_sheet,
                "Round211 region partition",
            )
            need(regions208[region_id][:2] == leaf_key[leaf_id], "Round211 key join")
            region_sheet[region_id] = sheet_id
    need(
        len(sheet_leaf) == 17_716
        and len(region_sheet) == 35_432
        and len(set(regions208) - set(region_sheet)) == 608,
        "Round211 incidence census",
    )
    del r211
    gc.collect()

    r225 = load("Round225")
    sheet_block: dict[str, str] = {}
    block_key: dict[str, set[int]] = defaultdict(set)
    block_members: dict[str, set[str]] = defaultdict(set)
    key_sheets: dict[int, list[str]] = defaultdict(list)
    for row in r225["formal_Round211_sheet_assignment_ledger"]["rows"]:
        sheet_id = row["Round211_sheet_row_id"]
        block_id = row["known_connectivity_block_id"]
        need(
            sheet_id in sheet_leaf
            and sheet_id not in sheet_block
            and row["leaf_row_id"] == sheet_leaf[sheet_id],
            "Round225 assignment",
        )
        ordinal = leaf_key[sheet_leaf[sheet_id]][0]
        sheet_block[sheet_id] = block_id
        block_key[block_id].add(ordinal)
        block_members[block_id].add(sheet_id)
        key_sheets[ordinal].append(sheet_id)
    need(
        set(sheet_block) == set(sheet_leaf)
        and len(block_key) == 7_404
        and all(len(keys) == 1 for keys in block_key.values()),
        "Round225 key purity",
    )
    formal_blocks = {
        row["known_connectivity_block_id"]: set(row["member_Round211_sheet_row_ids"])
        for row in r225["formal_certified_known_connectivity_block_ledger"]["rows"]
    }
    need(formal_blocks == block_members, "Round225 block reconstruction")
    edge_sources = Counter()
    for edge in r225["formal_Round223_Round224_current_quotient_edge_ledger"]["rows"]:
        left = edge["left_Round211_sheet_row_id"]
        right = edge["right_Round211_sheet_row_id"]
        need(
            left in sheet_leaf
            and right in sheet_leaf
            and leaf_key[sheet_leaf[left]][0] == leaf_key[sheet_leaf[right]][0],
            "Round225 same-key contact edge",
        )
        edge_sources[edge["source_layer"]] += 1
    need(
        edge_sources == Counter({
            "ROUND223_EXACT_P_S_TRACE_GLUE": 7_016,
            "ROUND224_EXACT_PARTIAL_CONTACT_TRACE_GLUE": 236,
        })
        and r225["rebuilt_frontier_audit"][
            "remaining_missing_contact_frontier_count"
        ] == 0,
        "Round225 contact frontier",
    )
    del r225, formal_blocks
    gc.collect()

    r226 = load("Round226")
    need(
        r226["census"][
            "event_trace_candidate_absence_proved_within_Round220_rejected_pool_count"
        ] == 9_830
        and r226["census"][
            "coordinate_region_identity_candidates_remaining_eligible_for_event_trace_glue"
        ] == 0
        and r226["census"]["physical_glue_credit_count"] == 0,
        "Round226 exclusion",
    )
    del r226
    gc.collect()
    r227 = load("Round227")
    need(
        r227["census"]["directed_partner_row_count"] == 35_432
        and r227["census"]["component_union_credit"] == 0
        and r227["map_contract"][
            "symmetry_partner_is_same_physical_point_atlas_transition"
        ] is False,
        "Round227 non-glue",
    )
    del r227
    gc.collect()
    r228 = load("Round228")
    need(
        r228["census"]["source_chart_seam_overlap_candidate_count"] == 0
        and r228["census"]["unclassified_atlas_overlap_channel_count"] == 0
        and r228["scope_contract"]["all_future_retained_strata_exhausted"] is False,
        "Round228 atlas scope",
    )
    del r228
    gc.collect()

    occurrence_specs.sort(key=lambda value: (
        {
            "ROUND179_RESOLVED_CHILD": 0,
            "ROUND204_STRICT_OPEN_REGION": 1,
            "ROUND208_STRICT_OPEN_REGION": 2,
        }[value[0]],
        value[1],
    ))
    need(
        len(occurrence_specs) == 53_968
        and len({value[1] for value in occurrence_specs}) == 53_968,
        "occurrence universe",
    )
    return {
        "keys216": keys216,
        "per_key220": per_key220,
        "resolved": resolved,
        "interfaces": interfaces,
        "occurrence_specs": occurrence_specs,
        "leaf_key": leaf_key,
        "regions208": regions208,
        "retained_regions": retained_regions,
        "region_sheet": region_sheet,
        "sheet_leaf": sheet_leaf,
        "sheet_block": sheet_block,
        "block_key": block_key,
        "key_sheets": key_sheets,
        "boundary_counts": boundary_counts,
    }


def occurrence_expected(
    gauge: str,
    row_id: str,
    ordinal: int,
    key_id: str,
    model_data: dict[str, Any],
) -> dict[str, Any]:
    sheet_id = None
    block_id = None
    if gauge == "ROUND179_RESOLVED_CHILD":
        status = (
            "COORDINATE_BOUNDARY_ATLAS_COMPLETE__"
            "ALL_BOUNDARY_STRATA_COORDINATE_ONLY__"
            "NO_KNOWN_BLOCK_INCIDENCE"
        )
    elif gauge == "ROUND204_STRICT_OPEN_REGION":
        status = (
            "SEPARATE_FORMAL_DIMENSIONAL_GAUGE__"
            "NO_ROUND211_SHEET_OR_KNOWN_BLOCK_INCIDENCE"
        )
    else:
        sheet_id = model_data["region_sheet"].get(row_id)
        if sheet_id is None:
            status = (
                "SHEETLESS_LOCAL_REGION__"
                "NO_ROUND211_SHEET_OR_KNOWN_BLOCK_INCIDENCE"
            )
        else:
            block_id = model_data["sheet_block"][sheet_id]
            status = (
                "ATTACHED_TO_CERTIFIED_KNOWN_CONNECTIVITY_SHEET_BLOCK__"
                "NOT_A_MAXIMAL_PHYSICAL_COMPONENT_ASSIGNMENT"
            )
    return close({
        "occurrence_attachment_row_id":
            f"round229-occurrence:{digest([gauge, row_id])}",
        "local_occurrence_gauge": gauge,
        "local_occurrence_row_id": row_id,
        "official_key_id": key_id,
        "official_key_ordinal": ordinal,
        "Round211_sheet_row_id": sheet_id,
        "Round225_known_connectivity_block_id": block_id,
        "known_block_incidence_attachment_credit": 1 if block_id else 0,
        "attachment_status": status,
        "known_block_is_maximal_physical_component": False,
        "maximal_physical_component_assignment_credit": 0,
        "global_exact_key_fibre_exhausted": False,
        "global_exact_key_disposition_credit": 0,
    })


def lineage_expected(
    interface: dict[str, Any],
    model_data: dict[str, Any],
) -> dict[str, Any]:
    resolved_id = interface["resolved_child_row_id"]
    retained_id = interface["retained_child_row_id"]
    ordinal, key_id = model_data["resolved"][resolved_id]
    region_ids = sorted(model_data["retained_regions"].get(retained_id, []))
    need(
        all(model_data["regions208"][region_id][:2] == (ordinal, key_id)
            for region_id in region_ids),
        "lineage key",
    )
    sheet_ids = sorted({
        model_data["region_sheet"][region_id]
        for region_id in region_ids
        if region_id in model_data["region_sheet"]
    })
    block_ids = sorted({
        model_data["sheet_block"][sheet_id] for sheet_id in sheet_ids
    })
    if block_ids:
        status = (
            "COORDINATE_LINEAGE_ONLY_TO_KEY_PURE_KNOWN_BLOCK_REFERENCE__"
            "EVENT_TRACE_FALSE__UNION_FORBIDDEN"
        )
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
    return close({
        "lineage_frontier_row_id":
            f"round229-lineage:{interface['split_interface_id'].split(':', 1)[1]}",
        "Round220_split_interface_id": interface["split_interface_id"],
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
        "Round225_referenced_known_block_ids_sha256": digest(block_ids),
        "lineage_status": status,
        "event_trace_materialized_on_interface": False,
        "coordinate_lineage_is_physical_edge": False,
        "physical_union_credit": 0,
        "maximal_physical_component_assignment_credit": 0,
        "global_exact_key_disposition_credit": 0,
    })


def verify_candidate(
    candidate: dict[str, Any],
    model_data: dict[str, Any],
) -> dict[str, Any]:
    need(set(candidate) == {"schema", "result", "result_sha256"}, "candidate envelope")
    need(candidate["schema"] == SCHEMA, "candidate schema")
    need(candidate["result_sha256"] == digest(candidate["result"]), "candidate closure")
    need(candidate["result_sha256"] == CANDIDATE_RESULT, "candidate result pin")
    result = candidate["result"]

    expected_occurrences = [
        occurrence_expected(*spec, model_data)
        for spec in model_data["occurrence_specs"]
    ]
    occurrence_ledger = expected_ledger(
        expected_occurrences,
        "occurrence_attachment_row_id",
    )
    need(
        result["formal_occurrence_known_block_attachment_frontier_ledger"]
        == occurrence_ledger,
        "occurrence ledger",
    )

    aggregates: dict[int, Counter[str]] = defaultdict(Counter)
    key_blocks: dict[int, set[str]] = defaultdict(set)
    for row in expected_occurrences:
        ordinal = row["official_key_ordinal"]
        aggregates[ordinal]["total"] += 1
        aggregates[ordinal][row["local_occurrence_gauge"]] += 1
        if row["known_block_incidence_attachment_credit"] == 1:
            aggregates[ordinal]["attached"] += 1
            key_blocks[ordinal].add(row["Round225_known_connectivity_block_id"])
        else:
            aggregates[ordinal]["unattached"] += 1

    expected_lineage = [
        lineage_expected(interface, model_data)
        for interface in sorted(
            model_data["interfaces"],
            key=lambda row: row["split_interface_id"],
        )
    ]
    lineage_ledger = expected_ledger(expected_lineage, "lineage_frontier_row_id")
    need(
        result[
            "formal_Round220_resolved_retained_coordinate_lineage_frontier_ledger"
        ] == lineage_ledger,
        "lineage ledger",
    )
    lineage_counts: dict[int, Counter[str]] = defaultdict(Counter)
    for row in expected_lineage:
        ordinal = row["official_key_ordinal"]
        lineage_counts[ordinal]["total"] += 1
        if row["Round208_retained_region_count"] > 0:
            lineage_counts[ordinal]["materialized"] += 1
        if row["Round225_referenced_known_block_count"] > 0:
            lineage_counts[ordinal]["block_reference"] += 1

    expected_keys: list[dict[str, Any]] = []
    for ordinal in sorted(model_data["keys216"]):
        old = model_data["keys216"][ordinal]
        counts = aggregates[ordinal]
        sheet_ids = sorted(model_data["key_sheets"][ordinal])
        block_ids = sorted(key_blocks[ordinal])
        need(
            counts["total"] == old["local_3D_occurrence_count"]
            and counts["attached"] == 2 * len(sheet_ids),
            f"key conservation:{ordinal}",
        )
        expected_keys.append(close({
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
                model_data["per_key220"][ordinal][
                    "coordinate_boundary_atlas_complete"
                ],
            "Round211_sheet_count": len(sheet_ids),
            "Round211_sheet_side_occurrence_count": counts["attached"],
            "Round225_key_pure_known_block_count": len(block_ids),
            "Round225_key_pure_known_block_ids_sha256": digest(block_ids),
            "Round211_sheet_ids_sha256": digest(sheet_ids),
            "occurrences_with_known_block_incidence": counts["attached"],
            "occurrences_without_known_block_incidence": counts["unattached"],
            "Round220_resolved_retained_interface_count":
                lineage_counts[ordinal]["total"],
            "Round220_interface_with_Round208_materialization_count":
                lineage_counts[ordinal]["materialized"],
            "Round220_interface_with_known_block_reference_count":
                lineage_counts[ordinal]["block_reference"],
            "known_blocks_are_maximal_physical_components": False,
            "global_exact_key_fibre_exhausted": False,
            "global_exact_key_disposition_credit": 0,
        }))
    key_ledger = expected_ledger(expected_keys, "key_frontier_row_id")
    need(
        result["formal_per_key_post_Round228_frontier_ledger"] == key_ledger,
        "per-key ledger",
    )

    input_binding = {
        label: {
            "filename": values[0],
            "certificate_or_attachment_sha256": values[1],
            "result_sha256": values[2],
            "schema": values[3],
        }
        for label, values in INPUTS.items()
    }
    expected = {
        "status": STATUS,
        "formal_input_binding": input_binding,
        "formal_occurrence_known_block_attachment_frontier_ledger":
            occurrence_ledger,
        "formal_per_key_post_Round228_frontier_ledger": key_ledger,
        "formal_Round220_resolved_retained_coordinate_lineage_frontier_ledger":
            lineage_ledger,
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
            "Round220_coordinate_boundary_face_event_sheet_incidence_count": 0,
            "Round220_coordinate_boundary_edge_event_sheet_incidence_count": 0,
            "Round220_coordinate_boundary_corner_event_sheet_incidence_count": 0,
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
            "no_known_block_incidence": "18536_OCCURRENCES",
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
            "8960 resolved-retained one-step interfaces; prove that the 7404 "
            "known blocks are complete against every retained event stratum, "
            "then independently rebuild all 116 occurrence fibres before any "
            "global exact-key disposition credit"
        ),
        "provenance": {
            "schema": SCHEMA,
            "producer_sha256": PRODUCER_SHA,
            "python_version": sys.version.split()[0],
        },
    }
    need(result == expected, "complete candidate semantics")
    return expected


def accepts(candidate: dict[str, Any], expected: dict[str, Any]) -> bool:
    try:
        need(set(candidate) == {"schema", "result", "result_sha256"}, "envelope")
        need(candidate["schema"] == SCHEMA, "schema")
        need(candidate["result_sha256"] == digest(candidate["result"]), "closure")
        need(candidate["result"] == expected, "expected semantics")
        return True
    except (VerificationError, KeyError, TypeError, ValueError):
        return False


def resign_ledger(result: dict[str, Any], ledger_name: str, id_field: str) -> None:
    rows = result[ledger_name]["rows"]
    result[ledger_name] = expected_ledger(rows, id_field)


def semantic_attacks(
    original: dict[str, Any],
    expected: dict[str, Any],
) -> dict[str, Any]:
    result = original["result"]
    occurrence_rows = result[
        "formal_occurrence_known_block_attachment_frontier_ledger"
    ]["rows"]
    lineage_rows = result[
        "formal_Round220_resolved_retained_coordinate_lineage_frontier_ledger"
    ]["rows"]
    cases: list[tuple[str, dict[str, Any], str, Any]] = [
        (
            "occurrence_component_promotion",
            occurrence_rows[0],
            "known_block_is_maximal_physical_component",
            True,
        ),
        (
            "fabricated_coordinate_attachment",
            occurrence_rows[0],
            "Round225_known_connectivity_block_id",
            "round225-known-connectivity-block:forged",
        ),
        (
            "cross_key_block_theft",
            occurrence_rows[35_500],
            "official_key_ordinal",
            occurrence_rows[35_500]["official_key_ordinal"] + 1,
        ),
        (
            "lineage_false_event_trace",
            lineage_rows[0],
            "event_trace_materialized_on_interface",
            True,
        ),
        (
            "lineage_false_union",
            lineage_rows[0],
            "coordinate_lineage_is_physical_edge",
            True,
        ),
        (
            "same_key_as_same_component",
            result["scope_contract"],
            "known_block_incidence_is_not_component_assignment",
            False,
        ),
        (
            "symmetry_as_glue",
            result["post_Round216_blocker_delta"],
            "Round211_Klein_symmetry_channel",
            "FORGED_PHYSICAL_GLUE",
        ),
        (
            "future_strata_exhausted",
            result["scope_contract"],
            "all_future_retained_event_strata_exhausted",
            True,
        ),
        (
            "global_fibre_promotion",
            result["strict_nonpromotion"],
            "global_exact_key_fibre_exhausted_count",
            116,
        ),
        (
            "D02_promotion",
            result["strict_nonpromotion"],
            "D02",
            "AUTHORIZED",
        ),
        (
            "CM2_promotion",
            result["strict_nonpromotion"],
            "CM2",
            "GO_FOR_CLAIM",
        ),
    ]
    rejected = 0
    labels: list[str] = []
    for label, container, field, forged in cases:
        old = container[field]
        container[field] = forged
        if result != expected:
            rejected += 1
            labels.append(label)
        container[field] = old

    removed = occurrence_rows.pop()
    if result != expected:
        rejected += 1
        labels.append("occurrence_omission")
    occurrence_rows.append(removed)

    # One compound hostile candidate is fully re-signed at row, ledger, and
    # envelope levels.  The other eleven probes isolate the semantic checks
    # without repeatedly canonicalizing the 67 MiB envelope.
    compound = copy.deepcopy(original)
    compound_row = compound["result"][
        "formal_occurrence_known_block_attachment_frontier_ledger"
    ]["rows"][0]
    compound_row["known_block_is_maximal_physical_component"] = True
    compound_row["maximal_physical_component_assignment_credit"] = 1
    compound_row["row_sha256"] = digest({
        key: value for key, value in compound_row.items()
        if key != "row_sha256"
    })
    resign_ledger(
        compound["result"],
        "formal_occurrence_known_block_attachment_frontier_ledger",
        "occurrence_attachment_row_id",
    )
    compound["result"]["strict_nonpromotion"]["CM2"] = "GO_FOR_CLAIM"
    compound["result_sha256"] = digest(compound["result"])
    need(not accepts(compound, expected), "compound resigned attack")
    need(rejected == 12, "semantic attacks")
    return {
        "attempted": 12,
        "rejected": rejected,
        "targeted_semantic_probes": 12,
        "fully_resigned_compound_attack": 1,
        "rejected_labels": labels,
    }


def json_attacks() -> dict[str, int]:
    cases = [
        b'{"a":1,"a":2}',
        b'{"a":1.0}',
        b'{"a":NaN}',
        b'{"a":Infinity}',
        b'{"a":-Infinity}',
        b'[]',
        b'null',
        b'true',
        b'{"a":1} trailing',
        b'{"a":01}',
        b'{"a":1e0}',
        b'{"a":0.0}',
        b'{"a":"\\ud800"}',
        b'{"a":"\\udfff"}',
        b'{"a":}',
        b'{"a":1,}',
    ]
    rejected = 0
    for raw in cases:
        try:
            strict_json(raw, "attack")
        except (VerificationError, json.JSONDecodeError, UnicodeError):
            rejected += 1
    need(rejected == len(cases), "JSON attacks")
    return {"attempted": len(cases), "rejected": rejected}


def file_attacks() -> dict[str, int]:
    attempted = 0
    rejected = 0

    def reject(action: Any) -> None:
        nonlocal attempted, rejected
        attempted += 1
        try:
            action()
        except (
            VerificationError,
            FileNotFoundError,
            IsADirectoryError,
        ):
            rejected += 1

    with tempfile.TemporaryDirectory(prefix=".round229-attacks-", dir=HERE) as name:
        root = Path(name)
        regular = root / "regular"
        regular.write_bytes(b"abcd")
        symlink = root / "symlink"
        symlink.symlink_to(regular)
        hardlink = root / "hardlink"
        os.link(regular, hardlink)
        fifo = root / "fifo"
        os.mkfifo(fifo)
        empty = root / "empty"
        empty.touch()
        actions = (
            lambda: regular_bytes(symlink, 10),
            lambda: regular_bytes(hardlink, 10),
            lambda: regular_bytes(fifo, 10),
            lambda: regular_bytes(root, 10),
            lambda: regular_bytes(root / "missing", 10),
            lambda: regular_bytes(empty, 10),
            lambda: regular_bytes(regular, 3),
            lambda: regular_bytes(Path(__file__), 1),
        )
        for action in actions:
            reject(action)
    need(attempted == rejected == 8, "file attacks")
    return {"attempted": attempted, "rejected": rejected}


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
    need(
        hashlib.sha256(regular_bytes(PRODUCER, 5_000_000)).hexdigest()
        == PRODUCER_SHA,
        "producer pin",
    )
    model_data = model()
    candidate_raw = regular_bytes(CANDIDATE, 100_000_000)
    need(hashlib.sha256(candidate_raw).hexdigest() == CANDIDATE_SHA, "candidate file pin")
    candidate = strict_json(candidate_raw)
    expected = verify_candidate(candidate, model_data)
    semantic = semantic_attacks(candidate, expected)
    strict_suite = json_attacks()
    path_suite = file_attacks()
    verifier_sha = hashlib.sha256(
        regular_bytes(Path(__file__), 5_000_000)
    ).hexdigest()
    result = {
        "status": "PASS_PARTIAL_FORMAL_ROUND229",
        "candidate_file_sha256": CANDIDATE_SHA,
        "candidate_result_sha256": CANDIDATE_RESULT,
        "producer_sha256": PRODUCER_SHA,
        "verifier_sha256": verifier_sha,
        "producer_imported_or_executed": False,
        "independent_reconstruction": {
            "observed_keys": 116,
            "local_occurrences": 53_968,
            "known_block_incidence_occurrences": 35_432,
            "no_known_block_incidence_occurrences": 18_536,
            "Round211_sheets": 17_716,
            "key_pure_known_blocks": 7_404,
            "mixed_key_known_blocks": 0,
            "resolved_retained_interfaces": 8_960,
            "interfaces_with_Round208_materialization": 460,
            "interfaces_with_coordinate_only_known_block_reference": 456,
            "event_trace_bridges": 0,
            "globally_exhausted_key_fibres": 0,
        },
        "attack_suite": {
            "resigned_semantic": semantic,
            "strict_JSON": strict_suite,
            "path_and_file": path_suite,
        },
        "strict_nonpromotion_reconfirmed": expected["strict_nonpromotion"],
    }
    envelope = {
        "schema": VERIFICATION_SCHEMA,
        "result": result,
        "result_sha256": digest(result),
    }
    encoded = canonical(envelope) + b"\n"
    if not args.no_write:
        safe_write(encoded)
    print(result["status"])
    print(f"result_sha256={envelope['result_sha256']}")
    print(f"verification_sha256={hashlib.sha256(encoded).hexdigest()}")
    print("occurrences=53968 attached=35432 unattached=18536")
    print("interfaces=8960 materialized=460 block_reference=456 event_trace=0")
    print("semantic=12/12 JSON=16/16 file=8/8 global_fibres=0/116")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
