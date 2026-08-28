#!/usr/bin/env python3
"""Independent cacheless verifier for the Round293 canonical closure.

The Round292 and Round293 producers are pinned only as inert bytes and are
never imported or executed.  Before either Round293 candidate artifact is
opened, this verifier rebuilds the complete 9,528-row Round289 relation
binding table, the 113,452-row Round291 physical-witness table, and the
28,016-row absence/no-binding table directly from the frozen mathematical
inputs.  Mapping keys are normalized before enclosing hashes are computed.
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
PREFIX = "cm2_round293_source_g_r289_r291_witness_binding_canonical_closure"
PRODUCER = HERE / f"{PREFIX}.py"
RESULT = HERE / f"{PREFIX}_result.json"
LEDGER = HERE / f"{PREFIX}_ledger.json.gz"
OUTPUT = HERE / f"{PREFIX}_verification.json"

ROUND292_PREFIX = "cm2_round292_source_g_r289_r291_witness_binding_audit_probe"
ROUND292_PRODUCER = HERE / f"{ROUND292_PREFIX}.py"
ROUND292_RESULT = HERE / f"{ROUND292_PREFIX}_result.json"
ROUND292_LEDGER = HERE / f"{ROUND292_PREFIX}_ledger.json.gz"

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

UPSTREAM_PINS = {
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

BASELINE_PINS = {
    ROUND292_PRODUCER.name:
        "72ff71aa4e74c2d4274afb760879d11d63ffae09dbfe9e6773519ee7a5abc163",
    ROUND292_RESULT.name:
        "07ced5c6e0f5c06b4f22019deda6c770341b264b654fe6ddb9a8f44ec68472ca",
    ROUND292_LEDGER.name:
        "5602f3bd5860ca70277f820e36b602273d7253073c4c4ba6111f6eff2f500570",
}

CANDIDATE_PINS = {
    PRODUCER.name:
        "988282e3ef57c10f882c9796056d7ca68109ee5d294feb2512b554908251ef00",
    RESULT.name:
        "36459f330fdd577031f35d8d8f7e93cf3ebc96bef049a4f687b22c9e39e91613",
    LEDGER.name:
        "0e7395a69844734cc51563882f471987cc566db28a55ccae6e6d15d045f9e53c",
}

ROUND292_IN_MEMORY_RESULT_SHA256 = (
    "919634dc108d9bf06c6b40209b8245f223ae52e2909fb76c71a1e9c25f291db0"
)
ROUND292_PERSISTED_RESULT_RECOMPUTED_SHA256 = (
    "ea99ee814e41fe22ea55ba04682fc44d3a5538aab1e41ccd7a154160a538c670"
)
SCHEMA = "cm2.round293.r289-r291-witness-binding-canonical-closure.v1"
LEDGER_SCHEMA = SCHEMA + ".ledger.v1"
VERIFICATION_SCHEMA = SCHEMA + ".verification.v1"


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
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


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


def read_gzip_bytes(payload: bytes) -> dict[str, Any]:
    value = json.loads(gzip.decompress(payload))
    need(isinstance(value, dict), "candidate gzip JSON object")
    return value


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


def all_mapping_keys_are_strings(value: Any) -> bool:
    if isinstance(value, dict):
        return all(
            isinstance(key, str) and all_mapping_keys_are_strings(child)
            for key, child in value.items()
        )
    if isinstance(value, list):
        return all(map(all_mapping_keys_are_strings, value))
    return True


def closed(payload: dict[str, Any]) -> dict[str, Any]:
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
    document: dict[str, Any], rows_key: str, count_key: str, hash_key: str
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


def unpack(result: dict[str, Any], table: str) -> list[dict[str, Any]]:
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
    need(len(result) == 6, "six-coordinate rational box")
    return result


def rect_area(rectangle: tuple[Q, Q, Q, Q]) -> Q:
    return (rectangle[1] - rectangle[0]) * (rectangle[3] - rectangle[2])


def intersect_rect(
    left: tuple[Q, Q, Q, Q], right: tuple[Q, Q, Q, Q]
) -> tuple[Q, Q, Q, Q] | None:
    p0, p1 = max(left[0], right[0]), min(left[1], right[1])
    s0, s1 = max(left[2], right[2]), min(left[3], right[3])
    return (p0, p1, s0, s1) if p0 < p1 and s0 < s1 else None


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


def load_round275_regions() -> dict[str, dict[str, Any]]:
    wrapper = read_json("R275")
    need(wrapper["result_sha256"] == digest(wrapper["result"]), "R275 result")
    rows: list[dict[str, Any]] = []
    for table in ("strict_region_ledger", "arrangement_region_ledger"):
        ledger = wrapper["result"][table]
        need(
            len(ledger["rows"]) == ledger["row_count"]
            and digest(ledger["rows"]) == ledger["rows_sha256"],
            f"R275:{table}",
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
    by_signature: dict[str, list[dict[str, Any]]] = defaultdict(list)
    by_origin_retained: dict[
        tuple[str, str], list[dict[str, Any]]
    ] = defaultdict(list)
    atoms: dict[str, dict[str, Any]] = {}
    for source in round279["rows"]:
        atom_id = source["canonical_atom_id"]
        disposition = dispositions[atom_id]
        occurrence_id = (
            disposition["existing_local_occurrence_row_id"]
            or disposition["reserved_candidate_occurrence_id__not_issued"]
        )
        need(occurrence_id is not None, "atom final/reserved occurrence ID")
        leaf = leaves[source["Round182_leaf_row_id"]]
        row = {
            **source,
            "final_or_reserved_occurrence_id": occurrence_id,
            "retained_child_row_id": leaf["retained_child_row_id"],
            "leaf_box": qbox(leaf["box"]),
        }
        atoms[atom_id] = row
        by_leaf[source["Round182_leaf_row_id"]].append(row)
        for signature_row_id in source["source_signature_row_ids"]:
            by_signature[signature_row_id].append(row)
        by_origin_retained[
            (source["origin_row_id"], leaf["retained_child_row_id"])
        ].append(row)
    need(len(atoms) == 332_016, "R279/R288 atom join")
    return atoms, by_leaf, by_signature, by_origin_retained, pairs


def reconstruct_terminal_support_cells(
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
        if not row["disposition"].startswith("EXACT_INCLUSION_ALIAS_"):
            continue
        region_id = row["Round275_region_id"]
        box = qbox(regions[region_id]["adjacent_rational_region_box"])
        atom = atoms[row["containing_atom_id"]]
        result[region_id].append({
            "t2": tuple(map(Q, row["physical_t_square_open_interval"])),
            "ps": (box[2], box[3], box[4], box[5]),
            "target_refs": [atom["final_or_reserved_occurrence_id"]],
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
        })

    overlap = read_gzip("R292_OVERLAP")
    need(
        overlap["row_count"] == len(overlap["rows"]) == 22_820
        and digest(overlap["rows"]) == overlap["rows_sha256"],
        "Round292A overlap ledger",
    )
    refinement_rows = [
        row for row in overlap["rows"] if row.get("disposition") is not None
    ]
    need(len(refinement_rows) == 11_852, "Round292A refinement census")
    for row in refinement_rows:
        verify_row(row, "Round292A refinement")
        box = tuple(map(Q, row["exact_transformed_open_cell"]))
        if row["existing_occurrence_occupancy_count"]:
            target_refs = row["existing_occurrence_ids"]
        else:
            need(
                row["Round292_refined_new_support_component_id"] is not None,
                "uncovered refinement component ID",
            )
            target_refs = [row["Round292_refined_new_support_component_id"]]
        result[row["Round275_region_id"]].append({
            "t2": (box[0], box[1]),
            "ps": (box[2], box[3], box[4], box[5]),
            "target_refs": target_refs,
        })
    return result


def reconstruct_r289(
    support_cells: dict[str, list[dict[str, Any]]],
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    ledger = read_gzip("R289")
    table = ledger["region_cell_relation_ledger"]
    relations = table["rows"]
    need(
        table["row_count"] == len(relations) == 9_528
        and digest(relations) == table["rows_sha256"],
        "R289 relation ledger",
    )
    rows: list[dict[str, Any]] = []
    dispositions: Counter[str] = Counter()
    target_histogram: Counter[int] = Counter()
    target_reference_count = 0
    subcell_count = bound_subcell_count = uncovered_subcell_count = 0
    exact_area = bound_area_total = uncovered_area_total = Q(0)
    endpoint_targets: dict[tuple[str, int], set[str]] = defaultdict(set)
    unresolved: set[tuple[str, int, str]] = set()
    r287 = read_gzip("R287")
    upper_by_region = {
        row["Round275_region_id"]: Q(row["physical_t_square_open_interval"][1])
        for row in r287["region_rows"]
    }
    need(len(upper_by_region) == 13_788, "R287 upper-face map")

    for relation in relations:
        verify_row(relation, "R289 relation")
        relation_id = relation["Round289_region_cell_relation_id"]
        rectangle = tuple(map(Q, relation["exact_positive_ps_overlap"]))
        need(
            rect_area(rectangle)
            == Q(relation["exact_positive_ps_overlap_area"]),
            "R289 exact area",
        )
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
            dispositions[payload["binding_disposition"]] += 1
            continue

        region_id = relation["Round275_region_id"]
        seam_cells = [
            cell
            for cell in support_cells.get(region_id, [])
            if cell["t2"][1] == upper_by_region[region_id]
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
        unique_subcells = multi_subcells = 0
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
                subcell_count += 1
                if occupancy:
                    bound_rectangles.append(cell_rect)
                    target_refs.update(occupancy)
                    bound_subcell_count += 1
                    if len(occupancy) == 1:
                        unique_subcells += 1
                    else:
                        multi_subcells += 1
                else:
                    uncovered_rectangles.append(cell_rect)
                    uncovered_subcell_count += 1
                    unresolved.add((
                        relation["Round268_true_seam_patch_row_id"],
                        relation["side_index"],
                        relation_id,
                    ))
        area = rect_area(rectangle)
        bound_area = rectangle_union_area(bound_rectangles)
        uncovered_area = rectangle_union_area(uncovered_rectangles)
        need(area == bound_area + uncovered_area, "R289 area conservation")
        exact_area += area
        bound_area_total += bound_area
        uncovered_area_total += uncovered_area
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
            "exact_binding_subcell_count": unique_subcells + multi_subcells,
            "exact_unique_target_subcell_count": unique_subcells,
            "exact_multi_target_subcell_count": multi_subcells,
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
        dispositions[disposition] += 1
        target_histogram[len(target_refs)] += 1
        target_reference_count += len(target_refs)
        endpoint_targets[
            (
                relation["Round268_true_seam_patch_row_id"],
                relation["side_index"],
            )
        ].update(target_refs)

    rows.sort(key=lambda row: row["Round289_region_cell_relation_id"])
    need(len(rows) == 9_528, "R289 reconstructed row census")
    summary = {
        "input_relation_count": len(rows),
        "actual_relation_count": 9_240,
        "graph_separated_relation_count": 288,
        "binding_disposition_histogram": dict(sorted(dispositions.items())),
        "actual_relation_target_reference_count": target_reference_count,
        "actual_relation_distinct_target_count_histogram": {
            str(key): value for key, value in sorted(target_histogram.items())
        },
        "actual_relation_exact_subcell_count": subcell_count,
        "actual_relation_bound_subcell_count": bound_subcell_count,
        "actual_relation_uncovered_subcell_count": uncovered_subcell_count,
        "actual_relation_exact_ps_area": str(exact_area),
        "actual_relation_bound_ps_area": str(bound_area_total),
        "actual_relation_uncovered_ps_area": str(uncovered_area_total),
        "tail_directed_endpoint_count": len(endpoint_targets),
        "tail_directed_endpoint_target_count_histogram": {
            str(key): value
            for key, value in sorted(Counter(
                len(targets) for targets in endpoint_targets.values()
            ).items())
        },
        "tail_directed_endpoint_with_unresolved_relation_count": len({
            (patch_id, side_index)
            for patch_id, side_index, _relation_id in unresolved
        }),
        "tail_patch_with_unresolved_relation_count": len({
            patch_id for patch_id, _side_index, _relation_id in unresolved
        }),
    }
    return rows, summary


def reconstruct_r291(
    by_leaf: dict[str, list[dict[str, Any]]],
    by_signature: dict[str, list[dict[str, Any]]],
    by_origin_retained: dict[tuple[str, str], list[dict[str, Any]]],
    pairs: dict[str, dict[str, Any]],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], dict[str, Any]]:
    ledger = read_gzip("R291")
    rows291 = verify_table(ledger, "rows", "row_count", "rows_sha256")
    need(len(rows291) == 55_428, "R291 row census")

    round204 = read_json("R204")
    need(
        round204["result_sha256"] == digest(round204["result"]),
        "R204 result closure",
    )
    r204_rows = round204["result"][
        "formal_local_open_3D_region_ledger"
    ]["rows"]
    r204_by_id = {row["region_row_id"]: row for row in r204_rows}

    positive_atoms: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for atom_rows in by_leaf.values():
        for atom in atom_rows:
            if atom["leaf_box"][0] == 0:
                positive_atoms[atom["retained_child_row_id"]].append(atom)

    physical_rows: list[dict[str, Any]] = []
    absence_rows: list[dict[str, Any]] = []
    kind_histogram: Counter[str] = Counter()
    target_histograms: dict[str, Counter[int]] = defaultdict(Counter)
    binding_histogram: Counter[str] = Counter()
    unresolved_cells = unique_cells = multi_cells = 0
    target_reference_count = exact_t0_cover = unresolved_t0 = 0

    for disposition in rows291:
        for index, witness in enumerate(disposition["physical_witness_cells"]):
            kind = witness["witness_kind"]
            kind_histogram[kind] += 1
            target_refs: set[str] = set()
            exact_cover = True
            if kind == "ROUND182_GRAPH_SHEET_LEAF":
                candidates = by_leaf[witness["leaf_row_id"]]
                need(len(candidates) == 2, "graph-sheet two-sided atoms")
                target_refs.update(
                    row["final_or_reserved_occurrence_id"]
                    for row in candidates
                )
                binding_class = (
                    "EXACT_TWO_SIDED_GRAPH_SHEET_ATOM_INCIDENCE"
                )
            elif kind == "ROUND208_DIRECT_GRAPH_SIDE_REGION":
                candidates = by_signature[witness["region_row_id"]]
                need(len(candidates) == 1, "R208 unique side atom")
                target_refs.add(
                    candidates[0]["final_or_reserved_occurrence_id"]
                )
                binding_class = "EXACT_UNIQUE_R208_SIDE_ATOM_INCIDENCE"
            elif kind == "ROUND182_TRANSVERSE_1D_LINE":
                pair = pairs[witness["pair_row_id"]]
                candidates = by_origin_retained[(
                    pair["origin_row_id"],
                    pair["containing_Round179_retained_child_row_id"],
                )]
                need(len(candidates) == 2, "transverse-line two sectors")
                target_refs.update(
                    row["final_or_reserved_occurrence_id"]
                    for row in candidates
                )
                binding_class = (
                    "EXACT_TWO_SECTOR_TRANSVERSE_LINE_ATOM_INCIDENCE"
                )
            elif kind == "SOURCE_EXACT_T0_SHEET_CELL":
                region_id = witness["half_open_owner_region_row_id"]
                need(region_id in r204_by_id, "R204 half-open owner")
                target_refs.add(region_id)
                binding_class = (
                    "EXACT_UNIQUE_R204_HALF_OPEN_OWNER_INCIDENCE"
                )
            elif kind in {
                "ROUND179_POSITIVE_T0_RETAINED_OWNER",
                "ROUND179_NEGATIVE_T0_SHADOW_PATCH",
            }:
                bounds = qbox(witness["exact_bounds"])
                witness_rect = (
                    bounds[2], bounds[3], bounds[4], bounds[5]
                )
                candidates = [
                    atom
                    for atom in positive_atoms[
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
                    for row in candidates
                )
                rectangles = {
                    (
                        max(witness_rect[0], row["leaf_box"][2]),
                        min(witness_rect[1], row["leaf_box"][3]),
                        max(witness_rect[2], row["leaf_box"][4]),
                        min(witness_rect[3], row["leaf_box"][5]),
                    )
                    for row in candidates
                }
                covered_area = rectangle_union_area(rectangles)
                exact_cover = covered_area == rect_area(witness_rect)
                if exact_cover:
                    exact_t0_cover += 1
                    binding_class = (
                        "EXACT_POSITIVE_T_OWNER_ATOM_COVER__"
                        + (
                            "UNIQUE_TARGET"
                            if len(target_refs) == 1
                            else "MULTI_TARGET"
                        )
                    )
                else:
                    need(
                        covered_area == 0 and not target_refs,
                        "t0 all-or-zero cover",
                    )
                    unresolved_t0 += 1
                    binding_class = (
                        "UNRESOLVED_POSITIVE_T_OWNER_RETAINED_VOLUME__"
                        "NO_ISSUED_REGISTRY_OCCURRENCE"
                    )
            else:
                raise VerificationError(
                    f"unknown physical witness kind:{kind}"
                )

            if not target_refs:
                unresolved_cells += 1
            elif len(target_refs) == 1:
                unique_cells += 1
            else:
                multi_cells += 1
            target_reference_count += len(target_refs)
            target_histograms[kind][len(target_refs)] += 1
            binding_histogram[binding_class] += 1
            witness_id = (
                "round292-r291-physical-witness-binding:"
                + digest([
                    disposition[
                        "complete_lower_stratum_local_disposition_row_id"
                    ],
                    index,
                    witness,
                ])
            )
            physical_rows.append(closed({
                "Round292_R291_physical_witness_binding_row_id":
                    witness_id,
                "Round291_local_disposition_row_id":
                    disposition[
                        "complete_lower_stratum_local_disposition_row_id"
                    ],
                "physical_witness_cell_index": index,
                "witness_kind": kind,
                "source_chart": disposition["source_chart"],
                "canonical_support_kind":
                    disposition["canonical_support_kind"],
                "local_disposition": disposition["local_disposition"],
                "binding_classification": binding_class,
                "exact_witness_covered_by_named_registry_supports":
                    exact_cover,
                "terminal_registry_target_reference_count":
                    len(target_refs),
                "terminal_registry_target_references":
                    sorted(target_refs),
                "occurrence_binding_credit": 0,
                "expanded_occurrence_credit": 0,
                "component_edge_credit": 0,
                "Jx_Jy_same_point_glue_credit": 0,
            }))

        for index, witness in enumerate(disposition["absence_witness_cells"]):
            witness_id = (
                "round292-r291-absence-no-binding:"
                + digest([
                    disposition[
                        "complete_lower_stratum_local_disposition_row_id"
                    ],
                    index,
                    witness,
                ])
            )
            absence_rows.append(closed({
                "Round292_R291_absence_no_binding_row_id": witness_id,
                "Round291_local_disposition_row_id":
                    disposition[
                        "complete_lower_stratum_local_disposition_row_id"
                    ],
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
        key=lambda row:
            row["Round292_R291_physical_witness_binding_row_id"]
    )
    absence_rows.sort(
        key=lambda row: row["Round292_R291_absence_no_binding_row_id"]
    )
    need(len(physical_rows) == 113_452, "R291 physical reconstruction")
    need(len(absence_rows) == 28_016, "R291 absence reconstruction")
    need(
        unresolved_cells + unique_cells + multi_cells
        == len(physical_rows),
        "R291 target-count partition",
    )
    summary = {
        "physical_witness_cell_count": len(physical_rows),
        "absence_witness_cell_count": len(absence_rows),
        "physical_witness_kind_histogram":
            dict(sorted(kind_histogram.items())),
        "physical_binding_classification_histogram":
            dict(sorted(binding_histogram.items())),
        "physical_target_count_histogram_by_kind": {
            kind: {
                str(key): value
                for key, value in sorted(histogram.items())
            }
            for kind, histogram in sorted(target_histograms.items())
        },
        "physical_witness_unique_target_count": unique_cells,
        "physical_witness_multi_target_count": multi_cells,
        "physical_witness_unresolved_count": unresolved_cells,
        "physical_witness_target_reference_count": target_reference_count,
        "t0_owner_shadow_exact_atom_cover_witness_count": exact_t0_cover,
        "t0_owner_shadow_unresolved_retained_volume_witness_count":
            unresolved_t0,
        "absence_witness_no_binding_count": len(absence_rows),
        "shadow_patch_count":
            kind_histogram["ROUND179_NEGATIVE_T0_SHADOW_PATCH"],
        "partitioned_parent_count": sum(
            row["local_disposition"]
            == "PARTITIONED_PHYSICAL_AND_ABSENT"
            for row in rows291
        ),
    }
    return physical_rows, absence_rows, summary


EXPECTED_REGISTRY_CONTRACT = {
    "preserved_occurrence_count": 126_468,
    "new_atom_occurrence_count": 295_336,
    "refined_R287_new_occurrence_candidate_count": 9_404,
    "conditional_registry_occurrence_count": 431_208,
    "Round288_existing_representation_binding_count": 36_680,
    "Round287_existing_representation_binding_count": 8_008,
    "Round292_additional_existing_representation_binding_count": 1_600,
    "conditional_representation_binding_count": 46_288,
}

SAFE_ORDER = [
    "FREEZE_REVISED_431208_OCCURRENCE_REGISTRY_AND_46288_REPRESENTATION_BINDINGS",
    "CLOSE_R291_UNRESOLVED_POSITIVE_T_RETAINED_OWNER_OPEN_REGION_IDENTITIES",
    "REFINE_AND_BIND_ONLY_PHYSICAL_R289_SUBCELLS_TO_TERMINAL_REGISTRY_OCCURRENCES",
    "BIND_R291_PHYSICAL_WITNESSES_AND_KEEP_ALL_28016_ABSENCE_CELLS_UNBOUND",
    "PAIR_ALL_152_TRUE_SEAM_PATCH_DIRECTED_ENDPOINT_CELLS",
    "ONLY_THEN_BUILD_CANONICAL_SEAM_AND_ORDINARY_FRONTIER_EDGE_LEDGER",
    "ONLY_AFTER_EDGE_LEDGER_FREEZE_REPLAY_COMPONENT_DSU_MAXIMALITY_FIBRES_AND_GLOBAL_DISPOSITIONS",
]

EXPECTED_NONPROMOTION = {
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
}


def independently_reconstruct_expected() -> tuple[
    dict[str, Any], dict[str, Any], dict[str, Any]
]:
    overlap_result = read_json("R292_OVERLAP_RESULT")
    need(
        overlap_result["status"]
        == "PASS_ZERO_CREDIT__R287_FULL_REGISTRY_OVERLAP_EXHAUSTED"
        and overlap_result["census"][
            "conditional_base_atom_registry_count"
        ] == 421_804
        and overlap_result["census"][
            "refined_strictly_new_support_component_count"
        ] == 9_404
        and overlap_result["census"][
            "occupied_representation_subcover_cell_count"
        ] == 1_600
        and overlap_result["census"][
            "remaining_unresolved_overlap_count"
        ] == 0,
        "Round292A registry contract",
    )
    r289_result = read_json("R289_RESULT")
    r291_result = read_json("R291_RESULT")
    need(
        r289_result["census"][
            "actual_incident_region_cell_relation_count"
        ] == 9_240
        and r289_result["census"][
            "graph_separated_region_cell_relation_count"
        ] == 288,
        "R289 source census",
    )
    need(
        r291_result["census"]["whole_physical_support_count"] == 39_252
        and r291_result["census"]["whole_absent_support_count"] == 16_168
        and r291_result["census"][
            "partitioned_physical_and_absent_support_count"
        ] == 8,
        "R291 source census",
    )

    regions = load_round275_regions()
    atoms, by_leaf, by_signature, by_origin_retained, pairs = (
        load_atom_maps()
    )
    support_cells = reconstruct_terminal_support_cells(regions, atoms)
    r289_rows, r289_summary = reconstruct_r289(support_cells)
    r291_physical, r291_absence, r291_summary = reconstruct_r291(
        by_leaf, by_signature, by_origin_retained, pairs
    )

    ledger = {
        "schema": LEDGER_SCHEMA,
        "status": (
            "PASS_ZERO_CREDIT__ROUND293_CANONICAL_LEDGER_CLOSURE__"
            "ROUND292_ROW_PAYLOADS_PRESERVED"
        ),
        "Round289_relation_binding_row_count": len(r289_rows),
        "Round289_relation_binding_rows_sha256": digest(r289_rows),
        "Round289_relation_binding_rows": r289_rows,
        "Round291_physical_witness_binding_row_count":
            len(r291_physical),
        "Round291_physical_witness_binding_rows_sha256":
            digest(r291_physical),
        "Round291_physical_witness_binding_rows": r291_physical,
        "Round291_absence_no_binding_row_count": len(r291_absence),
        "Round291_absence_no_binding_rows_sha256": digest(r291_absence),
        "Round291_absence_no_binding_rows": r291_absence,
        "canonical_closure": {
            "all_mapping_keys_are_strings": True,
            "row_payloads_and_row_sha256_preserved": True,
            "superseded_ledger_filename": ROUND292_LEDGER.name,
            "superseded_ledger_file_sha256":
                BASELINE_PINS[ROUND292_LEDGER.name],
        },
    }
    need(all_mapping_keys_are_strings(ledger), "expected ledger key types")
    ledger_bytes = deterministic_gzip_bytes(ledger)

    result = {
        "schema": SCHEMA,
        "status": (
            "PASS_ZERO_CREDIT__ROUND293_CANONICAL_JSON_CLOSURE__"
            "R289_R291_AUDIT__UNRESOLVED_OBLIGATIONS_RETAINED_FAIL_CLOSED"
        ),
        "revised_registry_contract": EXPECTED_REGISTRY_CONTRACT,
        "Round289": r289_summary,
        "Round291": r291_summary,
        "safe_order": SAFE_ORDER,
        "input_file_pins": {
            FILES[key]: value
            for key, value in sorted(UPSTREAM_PINS.items())
        },
        "ledger": {
            "filename": LEDGER.name,
            "file_sha256": hashlib.sha256(ledger_bytes).hexdigest(),
            "Round289_relation_binding_rows_sha256": digest(r289_rows),
            "Round291_physical_witness_binding_rows_sha256":
                digest(r291_physical),
            "Round291_absence_no_binding_rows_sha256":
                digest(r291_absence),
        },
        "strict_nonpromotion": EXPECTED_NONPROMOTION,
        "canonical_closure": {
            "all_mapping_keys_normalized_to_strings_before_commitment":
                True,
            "normalized_histogram_paths": [
                "Round289.tail_directed_endpoint_target_count_histogram",
            ],
            "result_sha256_definition":
                "SHA256_CANONICAL_JSON_OF_RESULT_WITHOUT_RESULT_SHA256",
            "round292_in_memory_result_sha256":
                ROUND292_IN_MEMORY_RESULT_SHA256,
            "round292_persisted_result_recomputed_sha256":
                ROUND292_PERSISTED_RESULT_RECOMPUTED_SHA256,
            "round292_result_round_trip_closed": False,
            "round293_result_round_trip_closed": True,
            "superseded_producer_filename": ROUND292_PRODUCER.name,
            "superseded_producer_sha256":
                BASELINE_PINS[ROUND292_PRODUCER.name],
            "superseded_result_filename": ROUND292_RESULT.name,
            "superseded_result_file_sha256":
                BASELINE_PINS[ROUND292_RESULT.name],
        },
    }
    need(
        r289_summary["actual_relation_uncovered_subcell_count"] == 396
        and r291_summary["physical_witness_unresolved_count"] == 576,
        "396/576 unresolved obligations",
    )
    result["result_sha256"] = digest(result)
    round_trip = json.loads(canonical(result) + b"\n")
    claim = round_trip.pop("result_sha256")
    need(claim == digest(round_trip), "expected persisted result closure")
    metadata = {
        "Round289_relation_binding_row_count": len(r289_rows),
        "Round291_physical_witness_binding_row_count":
            len(r291_physical),
        "Round291_absence_no_binding_row_count": len(r291_absence),
        "Round289_unresolved_subcell_count": 396,
        "Round291_unresolved_physical_witness_count": 576,
        "Round289_rows_sha256": digest(r289_rows),
        "Round291_physical_rows_sha256": digest(r291_physical),
        "Round291_absence_rows_sha256": digest(r291_absence),
    }
    return result, ledger, metadata


TABLES = (
    (
        "Round289_relation_binding_rows",
        "Round289_relation_binding_row_count",
        "Round289_relation_binding_rows_sha256",
    ),
    (
        "Round291_physical_witness_binding_rows",
        "Round291_physical_witness_binding_row_count",
        "Round291_physical_witness_binding_rows_sha256",
    ),
    (
        "Round291_absence_no_binding_rows",
        "Round291_absence_no_binding_row_count",
        "Round291_absence_no_binding_rows_sha256",
    ),
)


def verify_complete_ledger(ledger: dict[str, Any], label: str) -> None:
    need(ledger.get("schema") == LEDGER_SCHEMA, f"{label}:schema")
    need(all_mapping_keys_are_strings(ledger), f"{label}:mapping key types")
    for rows_key, count_key, hash_key in TABLES:
        rows = ledger.get(rows_key)
        need(
            isinstance(rows, list)
            and ledger.get(count_key) == len(rows)
            and ledger.get(hash_key) == digest(rows),
            f"{label}:{rows_key} table closure",
        )
        for row in rows:
            verify_row(row, f"{label}:{rows_key}")
            for key, value in row.items():
                if "credit" in key.lower():
                    need(value == 0, f"{label}:nonzero row credit:{key}")


def verify_result_closure(result: dict[str, Any], label: str) -> None:
    need(all_mapping_keys_are_strings(result), f"{label}:mapping key types")
    payload = {
        key: value for key, value in result.items()
        if key != "result_sha256"
    }
    need(
        result.get("result_sha256") == digest(payload),
        f"{label}:result SHA256 closure",
    )
    need(
        result["Round289"]["actual_relation_uncovered_subcell_count"]
        == 396
        and result["Round291"]["physical_witness_unresolved_count"]
        == 576,
        f"{label}:unresolved obligations changed",
    )
    for key, value in result["strict_nonpromotion"].items():
        if "credit" in key.lower():
            need(value == 0, f"{label}:nonzero result credit:{key}")


def audit_candidate_after_expected(
    expected_result: dict[str, Any],
    expected_ledger: dict[str, Any],
) -> tuple[dict[str, Any], dict[str, Any], bytes, bytes]:
    # Deliberately the first open/read/hash of the Round293 result or ledger.
    result_bytes = RESULT.read_bytes()
    ledger_bytes = LEDGER.read_bytes()
    need(
        hashlib.sha256(result_bytes).hexdigest()
        == CANDIDATE_PINS[RESULT.name],
        "candidate result byte pin",
    )
    need(
        hashlib.sha256(ledger_bytes).hexdigest()
        == CANDIDATE_PINS[LEDGER.name],
        "candidate ledger byte pin",
    )
    candidate_result = json.loads(result_bytes)
    candidate_ledger = read_gzip_bytes(ledger_bytes)
    verify_result_closure(candidate_result, "candidate result")
    verify_complete_ledger(candidate_ledger, "candidate ledger")
    need(
        candidate_result == expected_result,
        "candidate result differs from independent reconstruction",
    )
    need(
        candidate_ledger == expected_ledger,
        "candidate ledger differs from independent reconstruction",
    )
    need(
        ledger_bytes == deterministic_gzip_bytes(expected_ledger),
        "candidate ledger is not exact deterministic gzip",
    )
    need(
        result_bytes == canonical(expected_result) + b"\n",
        "candidate result is not exact canonical JSON plus newline",
    )
    return candidate_result, candidate_ledger, result_bytes, ledger_bytes


def audit_round292_defect_after_expected() -> dict[str, Any]:
    # Provenance only.  This object is opened after the expected Round293
    # result/ledger have already been independently reconstructed.
    with ROUND292_RESULT.open("rb") as handle:
        old_result = json.load(handle)
    old_claim = old_result.pop("result_sha256")
    recomputed = digest(old_result)
    need(
        old_claim == ROUND292_IN_MEMORY_RESULT_SHA256
        and recomputed == ROUND292_PERSISTED_RESULT_RECOMPUTED_SHA256
        and old_claim != recomputed,
        "Round292 defect provenance",
    )
    histogram = old_result["Round289"][
        "tail_directed_endpoint_target_count_histogram"
    ]
    need(
        list(sorted(histogram)) == [
            "13", "282", "3", "81", "82", "90", "96"
        ],
        "Round292 persisted lexical histogram keys",
    )
    return {
        "round292_claimed_result_sha256": old_claim,
        "round292_persisted_recomputed_result_sha256": recomputed,
        "round292_round_trip_closed": False,
        "defect":
            "INTEGER_HISTOGRAM_KEYS_NUMERICALLY_SORTED_BEFORE_JSON_ROUND_TRIP",
        "round293_all_mapping_keys_strings_before_commitment": True,
    }


def reclose_result(result: dict[str, Any]) -> None:
    result.pop("result_sha256", None)
    result["result_sha256"] = digest(result)


def reclose_row(row: dict[str, Any]) -> dict[str, Any]:
    payload = {
        key: value for key, value in row.items()
        if key != "row_sha256"
    }
    payload["row_sha256"] = digest(payload)
    return payload


def resigned_row_ledger(
    expected: dict[str, Any],
    table_index: int,
    row_index: int,
    mutate: Callable[[dict[str, Any]], None],
) -> dict[str, Any]:
    rows_key, count_key, hash_key = TABLES[table_index]
    attacked = dict(expected)
    rows = list(expected[rows_key])
    row = deepcopy(rows[row_index])
    mutate(row)
    rows[row_index] = reclose_row(row)
    attacked[rows_key] = rows
    attacked[count_key] = len(rows)
    attacked[hash_key] = digest(rows)
    verify_row(rows[row_index], "resigned attacked row")
    need(
        attacked[hash_key] == digest(rows),
        "resigned attacked table closure",
    )
    return attacked


def run_targeted_attacks(
    expected_result: dict[str, Any],
    expected_ledger: dict[str, Any],
) -> dict[str, Any]:
    rejected: list[str] = []

    def reject_exact(
        attack_id: str,
        attacked: Any,
        expected: Any,
    ) -> None:
        try:
            need(attacked == expected, f"attack accepted:{attack_id}")
        except VerificationError:
            rejected.append(attack_id)
        else:
            raise VerificationError(f"targeted attack accepted:{attack_id}")

    # Closure-valid row re-signing in each independently rebuilt table.
    r289_index = next(
        index
        for index, row in enumerate(
            expected_ledger["Round289_relation_binding_rows"]
        )
        if row["actual_seam_incidence"]
    )
    attacked = resigned_row_ledger(
        expected_ledger,
        0,
        r289_index,
        lambda row: row.__setitem__(
            "terminal_registry_target_references", ["forged-occurrence"]
        ),
    )
    reject_exact(
        "RESIGNED_R289_TARGET_REFERENCE", attacked, expected_ledger
    )

    unresolved_index = next(
        index
        for index, row in enumerate(
            expected_ledger["Round291_physical_witness_binding_rows"]
        )
        if row["terminal_registry_target_reference_count"] == 0
    )
    attacked = resigned_row_ledger(
        expected_ledger,
        1,
        unresolved_index,
        lambda row: row.__setitem__("occurrence_binding_credit", 1),
    )
    reject_exact(
        "RESIGNED_R291_UNRESOLVED_OCCURRENCE_CREDIT",
        attacked,
        expected_ledger,
    )

    attacked = resigned_row_ledger(
        expected_ledger,
        2,
        0,
        lambda row: row.__setitem__(
            "binding_classification", "FORGED_PHYSICAL_BINDING"
        ),
    )
    reject_exact(
        "RESIGNED_R291_ABSENCE_BINDING", attacked, expected_ledger
    )

    # Result-level re-sign attacks: their own result hashes are valid.
    result_attacks: list[
        tuple[str, Callable[[dict[str, Any]], None]]
    ] = [
        (
            "RECLOSED_R289_396_TO_395",
            lambda value: value["Round289"].__setitem__(
                "actual_relation_uncovered_subcell_count", 395
            ),
        ),
        (
            "RECLOSED_R291_576_TO_575",
            lambda value: value["Round291"].__setitem__(
                "physical_witness_unresolved_count", 575
            ),
        ),
        (
            "RECLOSED_REGISTRY_CENSUS",
            lambda value: value["revised_registry_contract"].__setitem__(
                "conditional_registry_occurrence_count", 431_207
            ),
        ),
        (
            "RECLOSED_RESULT_STATUS",
            lambda value: value.__setitem__("status", "PASS_FORGED"),
        ),
        (
            "RECLOSED_FORMAL_OCCURRENCE_CREDIT",
            lambda value: value["strict_nonpromotion"].__setitem__(
                "formal_new_occurrence_credit", 1
            ),
        ),
        (
            "RECLOSED_DSU_RANK_CREDIT",
            lambda value: value["strict_nonpromotion"].__setitem__(
                "DSU_rank_reduction_credit", 1
            ),
        ),
        (
            "RECLOSED_JX_JY_GLUE_CREDIT",
            lambda value: value["strict_nonpromotion"].__setitem__(
                "Jx_Jy_same_point_glue_credit", 1
            ),
        ),
        (
            "RECLOSED_LEDGER_FILE_HASH",
            lambda value: value["ledger"].__setitem__(
                "file_sha256", "0" * 64
            ),
        ),
        (
            "RECLOSED_UPSTREAM_PIN",
            lambda value: value["input_file_pins"].__setitem__(
                FILES["R291"], "0" * 64
            ),
        ),
    ]
    for attack_id, mutate in result_attacks:
        attacked_result = deepcopy(expected_result)
        mutate(attacked_result)
        reclose_result(attacked_result)
        verify_payload = {
            key: value for key, value in attacked_result.items()
            if key != "result_sha256"
        }
        need(
            attacked_result["result_sha256"] == digest(verify_payload),
            f"{attack_id}:effective reclosure",
        )
        reject_exact(attack_id, attacked_result, expected_result)

    # Key-type and duplicate-key ambiguity attacks specifically target the
    # Round292 defect class.  They are rehashed but fail the string-key gate.
    key_attacks: list[
        tuple[str, Callable[[dict[str, Any]], None]]
    ] = [
        (
            "INTEGER_KEY_R289_HISTOGRAM_RECLOSED",
            lambda value: value["Round289"][
                "tail_directed_endpoint_target_count_histogram"
            ].__setitem__(
                13,
                value["Round289"][
                    "tail_directed_endpoint_target_count_histogram"
                ].pop("13"),
            ),
        ),
        (
            "INTEGER_KEY_R291_NESTED_HISTOGRAM_RECLOSED",
            lambda value: value["Round291"][
                "physical_target_count_histogram_by_kind"
            ]["ROUND179_NEGATIVE_T0_SHADOW_PATCH"].__setitem__(
                0,
                value["Round291"][
                    "physical_target_count_histogram_by_kind"
                ]["ROUND179_NEGATIVE_T0_SHADOW_PATCH"].pop("0"),
            ),
        ),
        (
            "DUPLICATE_JSON_KEY_AMBIGUITY_RECLOSED",
            lambda value: value["Round289"][
                "tail_directed_endpoint_target_count_histogram"
            ].__setitem__(3, 999),
        ),
    ]
    for attack_id, mutate in key_attacks:
        attacked_result = deepcopy(expected_result)
        mutate(attacked_result)
        try:
            reclose_result(attacked_result)
        except (TypeError, ValueError):
            # Mixed int/string keys are not even sortable by the canonical
            # encoder.  Rejection therefore occurs before commitment.
            rejected.append(attack_id)
            continue
        try:
            need(
                all_mapping_keys_are_strings(attacked_result),
                f"{attack_id}:non-string key",
            )
        except VerificationError:
            rejected.append(attack_id)
        else:
            raise VerificationError(f"key-type attack accepted:{attack_id}")

    attacked_ledger = dict(expected_ledger)
    attacked_ledger["canonical_closure"] = dict(
        expected_ledger["canonical_closure"]
    )
    attacked_ledger["canonical_closure"][293] = "forged-key"
    try:
        need(
            all_mapping_keys_are_strings(attacked_ledger),
            "INTEGER_KEY_LEDGER_METADATA:non-string key",
        )
    except VerificationError:
        rejected.append("INTEGER_KEY_LEDGER_METADATA")
    else:
        raise VerificationError("integer-key ledger attack accepted")
    del attacked_ledger

    # Stale-hash attacks must fail local closure before exact comparison.
    stale_result = deepcopy(expected_result)
    stale_result["Round289"]["actual_relation_uncovered_subcell_count"] = 0
    try:
        verify_result_closure(stale_result, "stale attacked result")
    except VerificationError:
        rejected.append("STALE_RESULT_SHA256")
    else:
        raise VerificationError("stale result SHA256 attack accepted")

    stale_row = deepcopy(
        expected_ledger["Round289_relation_binding_rows"][r289_index]
    )
    stale_row["occurrence_binding_credit"] = 1
    try:
        verify_row(stale_row, "stale attacked row")
    except VerificationError:
        rejected.append("STALE_ROW_SHA256")
    else:
        raise VerificationError("stale row SHA256 attack accepted")

    stale_table = dict(expected_ledger)
    rows = list(expected_ledger["Round291_absence_no_binding_rows"])
    rows.pop()
    stale_table["Round291_absence_no_binding_rows"] = rows
    try:
        need(
            stale_table["Round291_absence_no_binding_rows_sha256"]
            == digest(rows),
            "stale table SHA256",
        )
    except VerificationError:
        rejected.append("STALE_TABLE_SHA256")
    else:
        raise VerificationError("stale table SHA256 attack accepted")

    # Coordinated row -> table -> gzip -> result re-sign, including credit.
    coordinated_ledger = resigned_row_ledger(
        expected_ledger,
        1,
        unresolved_index,
        lambda row: (
            row.__setitem__("occurrence_binding_credit", 1),
            row.__setitem__("terminal_registry_target_reference_count", 1),
            row.__setitem__(
                "terminal_registry_target_references",
                ["forged-occurrence"],
            ),
        ),
    )
    coordinated_gzip = deterministic_gzip_bytes(coordinated_ledger)
    coordinated_result = deepcopy(expected_result)
    coordinated_result["ledger"][
        "Round291_physical_witness_binding_rows_sha256"
    ] = coordinated_ledger[
        "Round291_physical_witness_binding_rows_sha256"
    ]
    coordinated_result["ledger"]["file_sha256"] = hashlib.sha256(
        coordinated_gzip
    ).hexdigest()
    coordinated_result["strict_nonpromotion"][
        "formal_new_occurrence_credit"
    ] = 1
    reclose_result(coordinated_result)
    try:
        need(
            coordinated_ledger == expected_ledger
            and coordinated_result == expected_result,
            "coordinated resigned chain",
        )
    except VerificationError:
        rejected.append("COORDINATED_ROW_LEDGER_RESULT_CREDIT_RESIGN")
    else:
        raise VerificationError("coordinated full-chain attack accepted")
    del coordinated_ledger, coordinated_gzip, coordinated_result

    # Same decoded object, different gzip header and result formatting.
    buffer = io.BytesIO()
    with gzip.GzipFile(
        filename="forged-ledger.json",
        mode="wb",
        fileobj=buffer,
        compresslevel=9,
        mtime=1,
    ) as handle:
        handle.write(canonical(expected_ledger))
    forged_gzip = buffer.getvalue()
    need(
        read_gzip_bytes(forged_gzip) == expected_ledger
        and forged_gzip != deterministic_gzip_bytes(expected_ledger),
        "effective alternate gzip-header attack",
    )
    rejected.append("ALTERNATE_GZIP_HEADER_SAME_OBJECT")

    pretty_result = json.dumps(
        expected_result, sort_keys=True, indent=2
    ).encode() + b"\n"
    need(
        json.loads(pretty_result) == expected_result
        and pretty_result != canonical(expected_result) + b"\n",
        "effective alternate result-format attack",
    )
    rejected.append("ALTERNATE_JSON_FORMAT_SAME_OBJECT")

    expected_count = (
        3 + len(result_attacks) + len(key_attacks) + 1 + 3 + 1 + 2
    )
    need(
        expected_count == 22
        and len(rejected) == expected_count
        and len(set(rejected)) == expected_count,
        "all 22 targeted attacks rejected",
    )
    return {
        "attack_count": expected_count,
        "rejected_attack_count": len(rejected),
        "all_targeted_attacks_rejected": True,
        "resigned_row_attacks_rejected": 3,
        "reclosed_result_attacks_rejected": len(result_attacks),
        "mapping_key_type_attacks_rejected": len(key_attacks) + 1,
        "stale_hash_attacks_rejected": 3,
        "coordinated_full_chain_credit_resign_rejected": True,
        "alternate_gzip_header_same_object_rejected": True,
        "alternate_json_format_same_object_rejected": True,
        "rejected_attack_ids": rejected,
    }


def verify() -> dict[str, Any]:
    for key, expected_hash in UPSTREAM_PINS.items():
        need(
            file_sha256(HERE / FILES[key]) == expected_hash,
            f"upstream pin:{FILES[key]}",
        )
    for filename, expected_hash in BASELINE_PINS.items():
        need(
            file_sha256(HERE / filename) == expected_hash,
            f"inert superseded artifact pin:{filename}",
        )
    need(
        file_sha256(PRODUCER) == CANDIDATE_PINS[PRODUCER.name],
        "Round293 producer inert byte pin",
    )

    expected_result, expected_ledger, reconstruction = (
        independently_reconstruct_expected()
    )
    expected_gzip = deterministic_gzip_bytes(expected_ledger)
    need(
        hashlib.sha256(expected_gzip).hexdigest()
        == CANDIDATE_PINS[LEDGER.name],
        "independent ledger frozen commitment",
    )
    candidate_result, candidate_ledger, result_bytes, ledger_bytes = (
        audit_candidate_after_expected(expected_result, expected_ledger)
    )
    need(
        candidate_result == expected_result
        and candidate_ledger == expected_ledger,
        "candidate decoded equality before release",
    )
    del candidate_result, candidate_ledger
    defect_audit = audit_round292_defect_after_expected()
    attacks = run_targeted_attacks(expected_result, expected_ledger)
    need(
        result_bytes == canonical(expected_result) + b"\n"
        and ledger_bytes == expected_gzip,
        "final exact candidate equality",
    )

    verification = {
        "schema": VERIFICATION_SCHEMA,
        "status": (
            "PASS_INDEPENDENT_CACHELESS_ROUND293_CANONICAL_CLOSURE__"
            "9528_R289_ROWS__113452_R291_PHYSICAL_ROWS__"
            "28016_R291_ABSENCE_ROWS__396_576_UNRESOLVED_PRESERVED__"
            "ALL_MAPPING_KEYS_STRINGS__ZERO_CREDIT"
        ),
        "artifact_pins": dict(sorted({
            **{
                FILES[key]: value
                for key, value in UPSTREAM_PINS.items()
            },
            **BASELINE_PINS,
            **CANDIDATE_PINS,
        }.items())),
        "independence_contract": {
            "Round292_producer_imported_or_executed": False,
            "Round293_producer_imported_or_executed": False,
            "Round292_result_used_as_expected_oracle": False,
            "Round292_ledger_used_as_expected_oracle": False,
            "Round293_candidate_result_or_ledger_opened_before_complete_expected_reconstruction":
                False,
            "expected_rows_rebuilt_from_frozen_R182_R204_R275_R279_R287_R288_R289_R291_R292A_inputs":
                True,
            "cache_pickle_or_pyc_input_used": False,
            "exact_arithmetic": "fractions.Fraction",
        },
        "independent_reconstruction": reconstruction,
        "canonical_closure_audit": {
            **defect_audit,
            "round293_result_sha256":
                expected_result["result_sha256"],
            "round293_result_file_sha256":
                hashlib.sha256(result_bytes).hexdigest(),
            "round293_result_recomputed_from_persisted_JSON":
                digest({
                    key: value
                    for key, value in json.loads(result_bytes).items()
                    if key != "result_sha256"
                }),
            "round293_round_trip_closed": True,
            "all_candidate_mapping_keys_strings": True,
        },
        "ledger_audit": {
            "Round289_rows_sha256": expected_ledger[
                "Round289_relation_binding_rows_sha256"
            ],
            "Round291_physical_rows_sha256": expected_ledger[
                "Round291_physical_witness_binding_rows_sha256"
            ],
            "Round291_absence_rows_sha256": expected_ledger[
                "Round291_absence_no_binding_rows_sha256"
            ],
            "deterministic_gzip_file_sha256":
                hashlib.sha256(expected_gzip).hexdigest(),
            "candidate_exactly_equals_independent_expected": True,
            "every_row_independently_closed": True,
        },
        "targeted_attacks": attacks,
        "replay_contract": {
            "seed_argument_affects_output": False,
            "external_PYTHONHASHSEED_expected_byte_identical": True,
        },
        "strict_nonpromotion": EXPECTED_NONPROMOTION,
        "verification_sha256": "",
    }
    verification["verification_sha256"] = digest({
        key: value for key, value in verification.items()
        if key != "verification_sha256"
    })
    round_trip = json.loads(canonical(verification) + b"\n")
    claim = round_trip.pop("verification_sha256")
    need(claim == digest(round_trip), "verification persisted closure")
    return verification


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--seed",
        default="293001",
        help="Cold-replay label; deliberately excluded from canonical output.",
    )
    parser.add_argument("--output", type=Path, default=OUTPUT)
    arguments = parser.parse_args()
    del arguments.seed
    verification = verify()
    atomic_write(arguments.output, canonical(verification) + b"\n")
    print(verification["status"])
    print("verification_sha256=" + verification["verification_sha256"])
    print("verification_file_sha256=" + file_sha256(arguments.output))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
