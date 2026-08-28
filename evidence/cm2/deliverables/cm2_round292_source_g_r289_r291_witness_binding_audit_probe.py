#!/usr/bin/env python3
"""ZERO-CREDIT witness-binding audit for the revised Round292 registry.

This probe deliberately does not issue occurrence IDs and does not build a
component DSU.  It answers two narrower questions:

* after the Round292 R287/base-registry overlap refinement, which terminal
  registry supports meet each Round289 seam-tail incidence at the
  seam-facing t^2 face; and
* which already named (or reserved) atom/region occurrences are incident to
  each Round291 physical lower-stratum witness.

Any missing physical incidence is retained as an explicit unresolved
obligation.  Graph-separated Round289 relations and Round291 absence cells
are proved no-binding rows.  Signature equality, Jx/Jy, and source symmetry
are never used as identity or glue.
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
PREFIX = "cm2_round292_source_g_r289_r291_witness_binding_audit_probe"
RESULT = HERE / f"{PREFIX}_result.json"
LEDGER = HERE / f"{PREFIX}_ledger.json.gz"

FILES = {
    "R182": "cm2_round182_source_g_clipped_graph_and_pair_arrangement_rows.json",
    "R204": "cm2_round204_source_g_wall_return_signature_local_replacement_certificate.json",
    "R275": "cm2_round275_source_g_complete_reverse_rechart_materialization_certificate.json",
    "R279": "cm2_round279_source_g_collar_atom_and_face_edge_freeze_atoms.json.gz",
    "R287": "cm2_round287_source_g_rechart_terminal_occurrence_disposition_probe_ledger.json.gz",
    "R288": "cm2_round288_source_g_canonical_atom_occurrence_identity_gate_audit_atom_dispositions.json.gz",
    "R289": "cm2_round289_source_g_outgoing_seam_tail_child_materialization_ledger.json.gz",
    "R289_RESULT": "cm2_round289_source_g_outgoing_seam_tail_child_materialization_result.json",
    "R291": "cm2_round291_source_g_complete_lower_stratum_local_disposition_freeze_ledger.json.gz",
    "R291_RESULT": "cm2_round291_source_g_complete_lower_stratum_local_disposition_freeze_result.json",
    "R292_OVERLAP": "cm2_round292_source_g_r287_registry_overlap_exhaustion_probe_ledger.json.gz",
    "R292_OVERLAP_RESULT": "cm2_round292_source_g_r287_registry_overlap_exhaustion_probe_result.json",
}

PINS = {
    "R182": "ae6e0c38df325e98b01a1d75acfbd8a85a71fda6a118db11d7dff6decf3f847c",
    "R204": "e7e1c49bebcb8c01f0fb4b33af66e4f2a8de560f121cae65f4971b2fec3e1818",
    "R275": "e18935169614fc8b62ead3be7f60b383396ea1d2c52e8151457241f49e770386",
    "R279": "283a10799e0c7d1156695c30cdb2533488602ca646a18804f93211c0a3132dbe",
    "R287": "29838e3e6b33f03bf623bbce8b87e6ba5c3306e66beb0b6634496503fb9a4f9a",
    "R288": "6b0a8aa1cd38019322a61f5aaefc936006d10769cd21a5c8df374576f9ac570a",
    "R289": "6c5680574c17d50749d39fb25970b7fbcbc677f4f73029aca833f549c0ef5001",
    "R289_RESULT": "9091e06b8aca3d5e883621e0e3f701a6b90ce2f02b84f6813cef7727f45c516c",
    "R291": "412b616b2cf75ef1373d98086cfcb2eb90a8c544e9f6b4d16a673f6cfeeb57ab",
    "R291_RESULT": "f07aae7d12b9d33aea0313737b7dafa51b22c1c8b1e5526ecf87ad53c5a8f705",
    "R292_OVERLAP": "8863126e88ffd30438938d0a8bdb577f5928ae81f3f17f4b506829d59103a8ab",
    "R292_OVERLAP_RESULT": "f3887e75f4ef62459b75d8c77eee4781ec14f57651b4feb09b8d7ca8e372c508",
}

SCHEMA = "cm2.round292.r289-r291-witness-binding-audit-probe.v1"
LEDGER_SCHEMA = SCHEMA + ".ledger.v1"


def canonical(value: Any) -> bytes:
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=True
    ).encode()


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def file_sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def need(condition: bool, label: str) -> None:
    if not condition:
        raise RuntimeError(label)


def read_json(key: str) -> dict[str, Any]:
    with (HERE / FILES[key]).open("rb") as handle:
        return json.load(handle)


def read_gzip(key: str) -> dict[str, Any]:
    with gzip.open(HERE / FILES[key], "rt", encoding="utf-8") as handle:
        return json.load(handle)


def closed(payload: dict[str, Any]) -> dict[str, Any]:
    row = dict(payload)
    row["row_sha256"] = digest(payload)
    return row


def verify_row(row: dict[str, Any], label: str) -> None:
    payload = {key: value for key, value in row.items() if key != "row_sha256"}
    need(row["row_sha256"] == digest(payload), f"{label}: row digest")


def verify_table(
    document: dict[str, Any], rows_key: str, count_key: str, hash_key: str
) -> list[dict[str, Any]]:
    rows = document[rows_key]
    need(len(rows) == document[count_key], f"{rows_key}: count")
    need(digest(rows) == document[hash_key], f"{rows_key}: digest")
    for row in rows:
        verify_row(row, rows_key)
    return rows


def unpack(result: dict[str, Any], table: str) -> list[dict[str, Any]]:
    rows = result[table]
    columns = result["row_column_schemas"][table]
    census = result["table_census_and_sha256"][table]
    need(
        len(rows) == census["row_count"] and digest(rows) == census["rows_sha256"],
        f"packed table: {table}",
    )
    return [dict(zip(columns, row, strict=True)) for row in rows]


def qbox(values: Iterable[str]) -> tuple[Q, ...]:
    result = tuple(map(Q, values))
    need(len(result) == 6, "six-coordinate box")
    return result


def positive_overlap(left: tuple[Q, Q], right: tuple[Q, Q]) -> bool:
    return max(left[0], right[0]) < min(left[1], right[1])


def rect_area(rectangle: tuple[Q, Q, Q, Q]) -> Q:
    return (rectangle[1] - rectangle[0]) * (rectangle[3] - rectangle[2])


def intersect_rect(
    left: tuple[Q, Q, Q, Q], right: tuple[Q, Q, Q, Q]
) -> tuple[Q, Q, Q, Q] | None:
    p0, p1 = max(left[0], right[0]), min(left[1], right[1])
    s0, s1 = max(left[2], right[2]), min(left[3], right[3])
    if p0 < p1 and s0 < s1:
        return p0, p1, s0, s1
    return None


def rectangle_union_area(rectangles: Iterable[tuple[Q, Q, Q, Q]]) -> Q:
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


def atomic(path: Path, payload: bytes) -> None:
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


def gzip_bytes(value: Any) -> bytes:
    output = io.BytesIO()
    with gzip.GzipFile(filename="", mode="wb", fileobj=output, mtime=0) as handle:
        handle.write(canonical(value))
    return output.getvalue()


def load_round275_regions() -> dict[str, dict[str, Any]]:
    wrapper = read_json("R275")
    need(wrapper["result_sha256"] == digest(wrapper["result"]), "R275 result")
    rows: list[dict[str, Any]] = []
    for table in ("strict_region_ledger", "arrangement_region_ledger"):
        ledger = wrapper["result"][table]
        need(
            len(ledger["rows"]) == ledger["row_count"]
            and digest(ledger["rows"]) == ledger["rows_sha256"],
            f"R275 {table}",
        )
        rows.extend(ledger["rows"])
    need(len(rows) == 13_788, "R275 region census")
    result = {row["reverse_rechart_region_row_id"]: row for row in rows}
    need(len(result) == len(rows), "R275 unique region IDs")
    return result


def load_atom_maps() -> tuple[
    dict[str, dict[str, Any]],
    dict[str, list[dict[str, Any]]],
    dict[str, list[dict[str, Any]]],
    dict[tuple[str, str], list[dict[str, Any]]],
    dict[str, dict[str, Any]],
]:
    round182 = read_json("R182")["result"]
    leaf_rows = unpack(round182, "collar_leaf_rows")
    pair_rows = unpack(round182, "pair_intersection_rows")
    leaves = {row["row_id"]: row for row in leaf_rows}
    pairs = {row["row_id"]: row for row in pair_rows}

    round288 = read_gzip("R288")
    need(
        round288["row_count"] == 332_016
        and digest(round288["rows"]) == round288["rows_sha256"],
        "R288 atom ledger",
    )
    dispositions = {
        row["canonical_atom_id"]: row for row in round288["rows"]
    }
    need(len(dispositions) == 332_016, "R288 unique atom IDs")

    round279 = read_gzip("R279")
    need(
        round279["row_count"] == 332_016
        and digest(round279["rows"]) == round279["rows_sha256"],
        "R279 atom ledger",
    )
    by_leaf: dict[str, list[dict[str, Any]]] = defaultdict(list)
    by_signature_row: dict[str, list[dict[str, Any]]] = defaultdict(list)
    by_origin_retained: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    atoms: dict[str, dict[str, Any]] = {}
    for source in round279["rows"]:
        atom_id = source["canonical_atom_id"]
        disposition = dispositions[atom_id]
        final_occurrence_id = (
            disposition["existing_local_occurrence_row_id"]
            or disposition["reserved_candidate_occurrence_id__not_issued"]
        )
        need(final_occurrence_id is not None, "atom final/reserved occurrence ID")
        leaf = leaves[source["Round182_leaf_row_id"]]
        row = {
            **source,
            "final_or_reserved_occurrence_id": final_occurrence_id,
            "retained_child_row_id": leaf["retained_child_row_id"],
            "leaf_box": qbox(leaf["box"]),
        }
        atoms[atom_id] = row
        by_leaf[source["Round182_leaf_row_id"]].append(row)
        for signature_row_id in source["source_signature_row_ids"]:
            by_signature_row[signature_row_id].append(row)
        by_origin_retained[
            (source["origin_row_id"], leaf["retained_child_row_id"])
        ].append(row)
    need(len(atoms) == 332_016, "R279/R288 atom join")
    return atoms, by_leaf, by_signature_row, by_origin_retained, pairs


def r289_terminal_support_cells(
    regions: dict[str, dict[str, Any]],
    atoms: dict[str, dict[str, Any]],
) -> dict[str, list[dict[str, Any]]]:
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
    need(len(region_rows) == 13_788 and len(cell_rows) == 7_616, "R287 census")

    result: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in region_rows:
        region_id = row["Round275_region_id"]
        if not row["disposition"].startswith("EXACT_INCLUSION_ALIAS_"):
            continue
        region = regions[region_id]
        box = qbox(region["adjacent_rational_region_box"])
        atom = atoms[row["containing_atom_id"]]
        result[region_id].append({
            "t2": tuple(map(Q, row["physical_t_square_open_interval"])),
            "ps": (box[2], box[3], box[4], box[5]),
            "target_refs": [atom["final_or_reserved_occurrence_id"]],
            "target_kind": "ROUND287_WHOLE_REPRESENTATION_ALIAS_TO_ATOM",
        })

    for row in cell_rows:
        if not row["disposition"].startswith("EXACT_INCLUSION_ALIAS_"):
            continue
        box = qbox(row["coordinate_box"])
        atom = atoms[row["containing_atom_id"]]
        result[row["Round275_region_id"]].append({
            "t2": tuple(map(Q, row["physical_t_square_open_interval"])),
            "ps": (box[2], box[3], box[4], box[5]),
            "target_refs": [atom["final_or_reserved_occurrence_id"]],
            "target_kind": "ROUND287_SLICE_REPRESENTATION_ALIAS_TO_ATOM",
        })

    overlap = read_gzip("R292_OVERLAP")
    need(
        overlap["row_count"] == len(overlap["rows"]) == 22_820
        and digest(overlap["rows"]) == overlap["rows_sha256"],
        "Round292 overlap ledger",
    )
    refinement_rows = [
        row for row in overlap["rows"] if row.get("disposition") is not None
    ]
    need(len(refinement_rows) == 11_852, "Round292 exact refinement rows")
    for row in refinement_rows:
        verify_row(row, "Round292 overlap refinement")
        box = tuple(map(Q, row["exact_transformed_open_cell"]))
        if row["existing_occurrence_occupancy_count"]:
            target_refs = row["existing_occurrence_ids"]
            target_kind = "ROUND292_EXISTING_REGISTRY_REPRESENTATION_SUBCOVER"
        else:
            need(
                row["Round292_refined_new_support_component_id"] is not None,
                "uncovered refinement component",
            )
            target_refs = [row["Round292_refined_new_support_component_id"]]
            target_kind = "ROUND292_REFINED_NEW_SUPPORT_COMPONENT_REFERENCE"
        result[row["Round275_region_id"]].append({
            "t2": (box[0], box[1]),
            "ps": (box[2], box[3], box[4], box[5]),
            "target_refs": target_refs,
            "target_kind": target_kind,
        })
    return result


def audit_r289(
    regions: dict[str, dict[str, Any]],
    support_cells: dict[str, list[dict[str, Any]]],
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    del regions
    ledger = read_gzip("R289")
    relation_table = ledger["region_cell_relation_ledger"]
    relations = relation_table["rows"]
    need(
        relation_table["row_count"] == len(relations) == 9_528
        and digest(relations) == relation_table["rows_sha256"],
        "R289 relation ledger",
    )
    rows: list[dict[str, Any]] = []
    disposition_histogram: Counter[str] = Counter()
    target_count_histogram: Counter[int] = Counter()
    actual_relation_target_reference_count = 0
    actual_relation_subcell_count = 0
    actual_relation_bound_subcell_count = 0
    actual_relation_uncovered_subcell_count = 0
    actual_relation_area = Q(0)
    actual_bound_area = Q(0)
    actual_uncovered_area = Q(0)
    endpoint_targets: dict[tuple[str, int], set[str]] = defaultdict(set)
    unresolved_endpoint_cells: set[tuple[str, int, str]] = set()
    r287 = read_gzip("R287")
    region_upper_by_id = {
        row["Round275_region_id"]: Q(row["physical_t_square_open_interval"][1])
        for row in r287["region_rows"]
    }
    need(len(region_upper_by_id) == 13_788, "R287 region upper-face map")

    for relation in relations:
        verify_row(relation, "R289 relation")
        relation_id = relation["Round289_region_cell_relation_id"]
        rectangle = tuple(map(Q, relation["exact_positive_ps_overlap"]))
        need(rect_area(rectangle) == Q(relation["exact_positive_ps_overlap_area"]), "R289 area")
        if not relation["actual_seam_incidence"]:
            payload = {
                "Round289_region_cell_relation_id": relation_id,
                "Round268_true_seam_patch_row_id":
                    relation["Round268_true_seam_patch_row_id"],
                "side_index": relation["side_index"],
                "Round275_region_id": relation["Round275_region_id"],
                "actual_seam_incidence": False,
                "binding_disposition":
                    "PROVEN_NO_INCIDENCE__SEPARATED_BY_REGULAR_OUTGOING_GRAPH",
                "terminal_registry_target_reference_count": 0,
                "terminal_registry_target_references": [],
                "exact_binding_subcell_count": 0,
                "exact_uncovered_subcell_count": 0,
                "occurrence_binding_credit": 0,
                "seam_edge_credit": 0,
                "component_union_credit": 0,
                "Jx_Jy_same_point_glue_credit": 0,
            }
            rows.append(closed(payload))
            disposition_histogram[payload["binding_disposition"]] += 1
            continue

        region_id = relation["Round275_region_id"]
        region_upper = region_upper_by_id[region_id]
        seam_cells = [
            cell
            for cell in support_cells.get(region_id, [])
            if cell["t2"][1] == region_upper
            and intersect_rect(rectangle, cell["ps"]) is not None
        ]
        p_cuts = {rectangle[0], rectangle[1]}
        s_cuts = {rectangle[2], rectangle[3]}
        for cell in seam_cells:
            hit = intersect_rect(rectangle, cell["ps"])
            need(hit is not None, "R289 seam-cell overlap")
            p_cuts.update(hit[:2])
            s_cuts.update(hit[2:])
        p_intervals = list(zip(sorted(p_cuts), sorted(p_cuts)[1:]))
        s_intervals = list(zip(sorted(s_cuts), sorted(s_cuts)[1:]))
        target_refs: set[str] = set()
        bound_rectangles: list[tuple[Q, Q, Q, Q]] = []
        uncovered_rectangles: list[tuple[Q, Q, Q, Q]] = []
        unique_target_subcells = 0
        multi_target_subcells = 0
        for p0, p1 in p_intervals:
            for s0, s1 in s_intervals:
                cell_rect = (p0, p1, s0, s1)
                midpoint = ((p0 + p1) / 2, (s0 + s1) / 2)
                occupancy = sorted({
                    target
                    for cell in seam_cells
                    if cell["ps"][0] < midpoint[0] < cell["ps"][1]
                    and cell["ps"][2] < midpoint[1] < cell["ps"][3]
                    for target in cell["target_refs"]
                })
                actual_relation_subcell_count += 1
                if occupancy:
                    bound_rectangles.append(cell_rect)
                    target_refs.update(occupancy)
                    actual_relation_bound_subcell_count += 1
                    if len(occupancy) == 1:
                        unique_target_subcells += 1
                    else:
                        multi_target_subcells += 1
                else:
                    uncovered_rectangles.append(cell_rect)
                    actual_relation_uncovered_subcell_count += 1
                    unresolved_endpoint_cells.add((
                        relation["Round268_true_seam_patch_row_id"],
                        relation["side_index"],
                        relation_id,
                    ))
        area = rect_area(rectangle)
        bound_area = rectangle_union_area(bound_rectangles)
        uncovered_area = rectangle_union_area(uncovered_rectangles)
        need(area == bound_area + uncovered_area, "R289 binding area conservation")
        actual_relation_area += area
        actual_bound_area += bound_area
        actual_uncovered_area += uncovered_area
        disposition = (
            "FULL_EXACT_TERMINAL_REGISTRY_SUBCELL_COVER__"
            "CONDITIONAL_PENDING_ROUND292_REGISTRY_FREEZE"
            if uncovered_area == 0
            else
            "PARTIAL_TERMINAL_REGISTRY_SUBCELL_COVER__"
            "UNRESOLVED_PHYSICAL_INCIDENCE_GAP"
        )
        payload = {
            "Round289_region_cell_relation_id": relation_id,
            "Round268_true_seam_patch_row_id":
                relation["Round268_true_seam_patch_row_id"],
            "side_index": relation["side_index"],
            "Round275_region_id": region_id,
            "actual_seam_incidence": True,
            "binding_disposition": disposition,
            "terminal_registry_target_reference_count": len(target_refs),
            "terminal_registry_target_references": sorted(target_refs),
            "exact_binding_subcell_count":
                unique_target_subcells + multi_target_subcells,
            "exact_unique_target_subcell_count": unique_target_subcells,
            "exact_multi_target_subcell_count": multi_target_subcells,
            "exact_uncovered_subcell_count": len(uncovered_rectangles),
            "exact_relation_ps_area": str(area),
            "exact_bound_ps_area": str(bound_area),
            "exact_uncovered_ps_area": str(uncovered_area),
            "occurrence_binding_credit": 0,
            "seam_edge_credit": 0,
            "component_union_credit": 0,
            "Jx_Jy_same_point_glue_credit": 0,
        }
        rows.append(closed(payload))
        disposition_histogram[disposition] += 1
        target_count_histogram[len(target_refs)] += 1
        actual_relation_target_reference_count += len(target_refs)
        endpoint_targets[
            (
                relation["Round268_true_seam_patch_row_id"],
                relation["side_index"],
            )
        ].update(target_refs)

    rows.sort(key=lambda row: row["Round289_region_cell_relation_id"])
    need(len(rows) == 9_528, "R289 audit row census")
    summary = {
        "input_relation_count": len(rows),
        "actual_relation_count": 9_240,
        "graph_separated_relation_count": 288,
        "binding_disposition_histogram": dict(sorted(disposition_histogram.items())),
        "actual_relation_target_reference_count":
            actual_relation_target_reference_count,
        "actual_relation_distinct_target_count_histogram": {
            str(key): value for key, value in sorted(target_count_histogram.items())
        },
        "actual_relation_exact_subcell_count": actual_relation_subcell_count,
        "actual_relation_bound_subcell_count":
            actual_relation_bound_subcell_count,
        "actual_relation_uncovered_subcell_count":
            actual_relation_uncovered_subcell_count,
        "actual_relation_exact_ps_area": str(actual_relation_area),
        "actual_relation_bound_ps_area": str(actual_bound_area),
        "actual_relation_uncovered_ps_area": str(actual_uncovered_area),
        "tail_directed_endpoint_count": len(endpoint_targets),
        "tail_directed_endpoint_target_count_histogram": dict(sorted(Counter(
            len(targets) for targets in endpoint_targets.values()
        ).items())),
        "tail_directed_endpoint_with_unresolved_relation_count": len({
            (patch_id, side_index)
            for patch_id, side_index, _relation_id in unresolved_endpoint_cells
        }),
        "tail_patch_with_unresolved_relation_count": len({
            patch_id for patch_id, _side_index, _relation_id
            in unresolved_endpoint_cells
        }),
    }
    return rows, summary


def audit_r291(
    atoms: dict[str, dict[str, Any]],
    by_leaf: dict[str, list[dict[str, Any]]],
    by_signature_row: dict[str, list[dict[str, Any]]],
    by_origin_retained: dict[tuple[str, str], list[dict[str, Any]]],
    pairs: dict[str, dict[str, Any]],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], dict[str, Any]]:
    del atoms
    ledger = read_gzip("R291")
    rows291 = verify_table(ledger, "rows", "row_count", "rows_sha256")
    need(len(rows291) == 55_428, "R291 row census")

    round204 = read_json("R204")
    need(
        round204["result_sha256"] == digest(round204["result"]),
        "R204 result digest",
    )
    r204_rows = round204["result"]["formal_local_open_3D_region_ledger"]["rows"]
    r204_by_id = {row["region_row_id"]: row for row in r204_rows}

    positive_t_atoms_by_retained: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for atom_rows in by_leaf.values():
        for atom in atom_rows:
            if atom["leaf_box"][0] == 0:
                positive_t_atoms_by_retained[
                    atom["retained_child_row_id"]
                ].append(atom)

    physical_rows: list[dict[str, Any]] = []
    absence_rows: list[dict[str, Any]] = []
    kind_histogram: Counter[str] = Counter()
    target_count_histogram_by_kind: dict[str, Counter[int]] = defaultdict(Counter)
    binding_histogram: Counter[str] = Counter()
    unresolved_cells = 0
    unique_cells = 0
    multi_cells = 0
    target_reference_count = 0
    t0_exact_cover_count = 0
    t0_uncovered_count = 0

    for disposition in rows291:
        for index, witness in enumerate(disposition["physical_witness_cells"]):
            kind = witness["witness_kind"]
            kind_histogram[kind] += 1
            target_refs: set[str] = set()
            exact_cover = True
            if kind == "ROUND182_GRAPH_SHEET_LEAF":
                candidates = by_leaf[witness["leaf_row_id"]]
                need(len(candidates) == 2, "two atoms incident to graph sheet leaf")
                target_refs.update(
                    row["final_or_reserved_occurrence_id"] for row in candidates
                )
                binding_class = "EXACT_TWO_SIDED_GRAPH_SHEET_ATOM_INCIDENCE"
            elif kind == "ROUND208_DIRECT_GRAPH_SIDE_REGION":
                candidates = by_signature_row[witness["region_row_id"]]
                need(len(candidates) == 1, "one atom for R208 direct side")
                target_refs.add(candidates[0]["final_or_reserved_occurrence_id"])
                binding_class = "EXACT_UNIQUE_R208_SIDE_ATOM_INCIDENCE"
            elif kind == "ROUND182_TRANSVERSE_1D_LINE":
                pair = pairs[witness["pair_row_id"]]
                candidates = by_origin_retained[(
                    pair["origin_row_id"],
                    pair["containing_Round179_retained_child_row_id"],
                )]
                need(len(candidates) == 2, "two atom sectors at transverse line")
                target_refs.update(
                    row["final_or_reserved_occurrence_id"] for row in candidates
                )
                binding_class = "EXACT_TWO_SECTOR_TRANSVERSE_LINE_ATOM_INCIDENCE"
            elif kind == "SOURCE_EXACT_T0_SHEET_CELL":
                region_id = witness["half_open_owner_region_row_id"]
                need(region_id in r204_by_id, "R204 half-open owner region")
                target_refs.add(region_id)
                binding_class = "EXACT_UNIQUE_R204_HALF_OPEN_OWNER_INCIDENCE"
            elif kind in {
                "ROUND179_POSITIVE_T0_RETAINED_OWNER",
                "ROUND179_NEGATIVE_T0_SHADOW_PATCH",
            }:
                bounds = qbox(witness["exact_bounds"])
                witness_rect = (bounds[2], bounds[3], bounds[4], bounds[5])
                candidate_atoms = [
                    atom
                    for atom in positive_t_atoms_by_retained[
                        witness["positive_owner_retained_child_row_id"]
                    ]
                    if atom["source_chart"] == disposition["source_chart"]
                    and atom["owner_target"] == witness["owner_target"]
                    and intersect_rect(
                        witness_rect,
                        (
                            atom["leaf_box"][2],
                            atom["leaf_box"][3],
                            atom["leaf_box"][4],
                            atom["leaf_box"][5],
                        ),
                    ) is not None
                ]
                target_refs.update(
                    row["final_or_reserved_occurrence_id"]
                    for row in candidate_atoms
                )
                leaf_rectangles = {
                    (
                        max(witness_rect[0], row["leaf_box"][2]),
                        min(witness_rect[1], row["leaf_box"][3]),
                        max(witness_rect[2], row["leaf_box"][4]),
                        min(witness_rect[3], row["leaf_box"][5]),
                    )
                    for row in candidate_atoms
                }
                covered_area = rectangle_union_area(leaf_rectangles)
                exact_cover = covered_area == rect_area(witness_rect)
                if exact_cover:
                    t0_exact_cover_count += 1
                    binding_class = (
                        "EXACT_POSITIVE_T_OWNER_ATOM_COVER__"
                        + ("UNIQUE_TARGET" if len(target_refs) == 1 else "MULTI_TARGET")
                    )
                else:
                    need(covered_area == 0 and not target_refs, "t0 all-or-zero cover")
                    t0_uncovered_count += 1
                    binding_class = (
                        "UNRESOLVED_POSITIVE_T_OWNER_RETAINED_VOLUME__"
                        "NO_ISSUED_REGISTRY_OCCURRENCE"
                    )
            else:
                raise RuntimeError(f"unknown physical witness kind: {kind}")

            if not target_refs:
                unresolved_cells += 1
            elif len(target_refs) == 1:
                unique_cells += 1
            else:
                multi_cells += 1
            target_reference_count += len(target_refs)
            target_count_histogram_by_kind[kind][len(target_refs)] += 1
            binding_histogram[binding_class] += 1
            witness_id = "round292-r291-physical-witness-binding:" + digest([
                disposition["complete_lower_stratum_local_disposition_row_id"],
                index,
                witness,
            ])
            physical_rows.append(closed({
                "Round292_R291_physical_witness_binding_row_id": witness_id,
                "Round291_local_disposition_row_id":
                    disposition["complete_lower_stratum_local_disposition_row_id"],
                "physical_witness_cell_index": index,
                "witness_kind": kind,
                "source_chart": disposition["source_chart"],
                "canonical_support_kind": disposition["canonical_support_kind"],
                "local_disposition": disposition["local_disposition"],
                "binding_classification": binding_class,
                "exact_witness_covered_by_named_registry_supports": exact_cover,
                "terminal_registry_target_reference_count": len(target_refs),
                "terminal_registry_target_references": sorted(target_refs),
                "occurrence_binding_credit": 0,
                "expanded_occurrence_credit": 0,
                "component_edge_credit": 0,
                "Jx_Jy_same_point_glue_credit": 0,
            }))

        for index, witness in enumerate(disposition["absence_witness_cells"]):
            witness_id = "round292-r291-absence-no-binding:" + digest([
                disposition["complete_lower_stratum_local_disposition_row_id"],
                index,
                witness,
            ])
            absence_rows.append(closed({
                "Round292_R291_absence_no_binding_row_id": witness_id,
                "Round291_local_disposition_row_id":
                    disposition["complete_lower_stratum_local_disposition_row_id"],
                "absence_witness_cell_index": index,
                "witness_kind": witness["witness_kind"],
                "binding_classification":
                    "PROVEN_LOCAL_ABSENCE__NO_REGISTRY_INCIDENCE_BINDING",
                "terminal_registry_target_reference_count": 0,
                "terminal_registry_target_references": [],
                "occurrence_binding_credit": 0,
                "expanded_occurrence_credit": 0,
                "component_edge_credit": 0,
                "Jx_Jy_same_point_glue_credit": 0,
            }))

    physical_rows.sort(
        key=lambda row: row["Round292_R291_physical_witness_binding_row_id"]
    )
    absence_rows.sort(
        key=lambda row: row["Round292_R291_absence_no_binding_row_id"]
    )
    need(len(physical_rows) == 113_452, "R291 physical witness census")
    need(len(absence_rows) == 28_016, "R291 absence witness census")
    need(
        unresolved_cells + unique_cells + multi_cells == len(physical_rows),
        "R291 binding partition",
    )
    summary = {
        "physical_witness_cell_count": len(physical_rows),
        "absence_witness_cell_count": len(absence_rows),
        "physical_witness_kind_histogram": dict(sorted(kind_histogram.items())),
        "physical_binding_classification_histogram":
            dict(sorted(binding_histogram.items())),
        "physical_target_count_histogram_by_kind": {
            kind: {str(key): value for key, value in sorted(histogram.items())}
            for kind, histogram in sorted(target_count_histogram_by_kind.items())
        },
        "physical_witness_unique_target_count": unique_cells,
        "physical_witness_multi_target_count": multi_cells,
        "physical_witness_unresolved_count": unresolved_cells,
        "physical_witness_target_reference_count": target_reference_count,
        "t0_owner_shadow_exact_atom_cover_witness_count": t0_exact_cover_count,
        "t0_owner_shadow_unresolved_retained_volume_witness_count":
            t0_uncovered_count,
        "absence_witness_no_binding_count": len(absence_rows),
        "shadow_patch_count": kind_histogram["ROUND179_NEGATIVE_T0_SHADOW_PATCH"],
        "partitioned_parent_count": sum(
            row["local_disposition"] == "PARTITIONED_PHYSICAL_AND_ABSENT"
            for row in rows291
        ),
    }
    return physical_rows, absence_rows, summary


def build() -> tuple[dict[str, Any], dict[str, Any]]:
    for key, expected in PINS.items():
        need(file_sha256(HERE / FILES[key]) == expected, f"input pin: {key}")

    overlap_result = read_json("R292_OVERLAP_RESULT")
    need(
        overlap_result["status"]
        == "PASS_ZERO_CREDIT__R287_FULL_REGISTRY_OVERLAP_EXHAUSTED"
        and overlap_result["census"]["conditional_base_atom_registry_count"]
        == 421_804
        and overlap_result["census"][
            "refined_strictly_new_support_component_count"
        ] == 9_404
        and overlap_result["census"][
            "occupied_representation_subcover_cell_count"
        ] == 1_600
        and overlap_result["census"]["remaining_unresolved_overlap_count"] == 0,
        "revised Round292 registry contract",
    )

    result289 = read_json("R289_RESULT")
    result291 = read_json("R291_RESULT")
    need(
        result289["census"]["actual_incident_region_cell_relation_count"] == 9_240
        and result289["census"][
            "graph_separated_region_cell_relation_count"
        ] == 288,
        "R289 result census",
    )
    need(
        result291["census"]["whole_physical_support_count"] == 39_252
        and result291["census"]["whole_absent_support_count"] == 16_168
        and result291["census"][
            "partitioned_physical_and_absent_support_count"
        ] == 8,
        "R291 result census",
    )

    regions = load_round275_regions()
    atoms, by_leaf, by_signature, by_origin_retained, pairs = load_atom_maps()
    support_cells = r289_terminal_support_cells(regions, atoms)
    r289_rows, r289_summary = audit_r289(regions, support_cells)
    r291_physical, r291_absence, r291_summary = audit_r291(
        atoms, by_leaf, by_signature, by_origin_retained, pairs
    )

    ledger = {
        "schema": LEDGER_SCHEMA,
        "status": "PASS_ZERO_CREDIT__WITNESS_BINDING_OBLIGATIONS_EXHAUSTIVELY_AUDITED",
        "Round289_relation_binding_row_count": len(r289_rows),
        "Round289_relation_binding_rows_sha256": digest(r289_rows),
        "Round289_relation_binding_rows": r289_rows,
        "Round291_physical_witness_binding_row_count": len(r291_physical),
        "Round291_physical_witness_binding_rows_sha256": digest(r291_physical),
        "Round291_physical_witness_binding_rows": r291_physical,
        "Round291_absence_no_binding_row_count": len(r291_absence),
        "Round291_absence_no_binding_rows_sha256": digest(r291_absence),
        "Round291_absence_no_binding_rows": r291_absence,
    }
    ledger_payload = gzip_bytes(ledger)
    summary = {
        "schema": SCHEMA,
        "status":
            "PASS_ZERO_CREDIT__R289_R291_BINDING_AUDIT__"
            "UNRESOLVED_OBLIGATIONS_RETAINED_FAIL_CLOSED",
        "revised_registry_contract": {
            "preserved_occurrence_count": 126_468,
            "new_atom_occurrence_count": 295_336,
            "refined_R287_new_occurrence_candidate_count": 9_404,
            "conditional_registry_occurrence_count": 431_208,
            "Round288_existing_representation_binding_count": 36_680,
            "Round287_existing_representation_binding_count": 8_008,
            "Round292_additional_existing_representation_binding_count": 1_600,
            "conditional_representation_binding_count": 46_288,
        },
        "Round289": r289_summary,
        "Round291": r291_summary,
        "safe_order": [
            "FREEZE_REVISED_431208_OCCURRENCE_REGISTRY_AND_46288_REPRESENTATION_BINDINGS",
            "CLOSE_R291_UNRESOLVED_POSITIVE_T_RETAINED_OWNER_OPEN_REGION_IDENTITIES",
            "REFINE_AND_BIND_ONLY_PHYSICAL_R289_SUBCELLS_TO_TERMINAL_REGISTRY_OCCURRENCES",
            "BIND_R291_PHYSICAL_WITNESSES_AND_KEEP_ALL_28016_ABSENCE_CELLS_UNBOUND",
            "PAIR_ALL_152_TRUE_SEAM_PATCH_DIRECTED_ENDPOINT_CELLS",
            "ONLY_THEN_BUILD_CANONICAL_SEAM_AND_ORDINARY_FRONTIER_EDGE_LEDGER",
            "ONLY_AFTER_EDGE_LEDGER_FREEZE_REPLAY_COMPONENT_DSU_MAXIMALITY_FIBRES_AND_GLOBAL_DISPOSITIONS",
        ],
        "input_file_pins": {
            FILES[key]: value for key, value in sorted(PINS.items())
        },
        "ledger": {
            "filename": LEDGER.name,
            "file_sha256": hashlib.sha256(ledger_payload).hexdigest(),
            "Round289_relation_binding_rows_sha256": digest(r289_rows),
            "Round291_physical_witness_binding_rows_sha256": digest(r291_physical),
            "Round291_absence_no_binding_rows_sha256": digest(r291_absence),
        },
        "strict_nonpromotion": {
            "expanded_occurrences": 126_468,
            "quotient_components": 63_224,
            "formal_new_occurrence_credit": 0,
            "representation_alias_binding_credit": 0,
            "occurrence_identity_collapse_credit": 0,
            "component_union_credit": 0,
            "seam_edge_credit": 0,
            "DSU_rank_reduction_credit": 0,
            "maximality_credit": 0,
            "exact_key_fibre_credit": 0,
            "global_disposition_credit": 0,
            "Jx_Jy_same_point_glue_credit": 0,
            "Gate5": "10/18",
            "D02": "BLOCKED",
            "CM2": "NO-GO_FOR_CLAIM",
        },
    }
    summary["result_sha256"] = digest(summary)
    return ledger, summary


def main() -> None:
    ledger, result = build()
    atomic(LEDGER, gzip_bytes(ledger))
    atomic(RESULT, canonical(result) + b"\n")
    print(json.dumps({
        "status": result["status"],
        "Round289": result["Round289"],
        "Round291": result["Round291"],
        "ledger_sha256": result["ledger"]["file_sha256"],
        "result_sha256": result["result_sha256"],
    }, sort_keys=True, indent=2))


if __name__ == "__main__":
    main()
