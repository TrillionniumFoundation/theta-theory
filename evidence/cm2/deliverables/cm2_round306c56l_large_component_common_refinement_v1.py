#!/usr/bin/env python3
"""C56-L: exact large-component corridor/refinement obligation ledger.

This is a fail-closed producer.  It consumes frozen C35/C36/C41/C55-A/C55-B
bytes, reconstructs the two 850-cell component subproblems, and materializes:

* one explicit face/seam corridor or separator-island witness for every one of
  the 1,124 currently unresolved cells in those components;
* all 33,319 post-C53 logical C41 rows attached to those cells; and
* the exact 1,124 x 1,648 cell/occurrence product required by C36.

An atlas-graph corridor is not silently promoted to a dynamic known-sheet
continuation.  Unless margin, owner, and history transport cover every
refined stratum, all formal credit remains zero.
"""

from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import sys
from collections import Counter, defaultdict, deque
from pathlib import Path
from typing import Any, Iterable


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "deliverables"
PREFIX = "cm2_round306c56l_large_component_common_refinement"

PRODUCER_SCHEMA = "cm2.round306c56l.large-component-common-refinement.v1"
CELL_SCHEMA = PRODUCER_SCHEMA + ".corridor-or-separator-cell-row"
ISLAND_SCHEMA = PRODUCER_SCHEMA + ".separator-island-row"
TASK_SCHEMA = PRODUCER_SCHEMA + ".post-c53-c41-logical-task-row"
REFINEMENT_SCHEMA = PRODUCER_SCHEMA + ".cell-occurrence-refined-stratum-row"
COMPONENT_SCHEMA = PRODUCER_SCHEMA + ".component-summary-row"

CELL_FILE = PREFIX + "_corridor_and_separator_cells_v1.jsonl.gz"
ISLAND_FILE = PREFIX + "_separator_islands_v1.jsonl.gz"
TASK_FILE = PREFIX + "_post_c53_pending_logical_tasks_v1.jsonl.gz"
REFINEMENT_FILE = PREFIX + "_cell_occurrence_common_refinement_v1.jsonl.gz"
COMPONENT_FILE = PREFIX + "_component_summary_v1.jsonl.gz"
RESULT_FILE = PREFIX + "_result_v1.json"

C55A_RESULT = OUT / "cm2_round306c55a_four_chart_fundamental_domain_bnb_result_v1.json"
C55A_LEAF = OUT / "cm2_round306c55a_four_chart_fundamental_domain_bnb_leaf_ledger_v1.json"
C55B_RESULT = OUT / "cm2_round306c55b_global_component_adjacency_known_sheet_result_v1.json"
C55B_CELL = OUT / "cm2_round306c55b_global_component_adjacency_known_sheet_cell_component_crosswalk_v1.jsonl.gz"
C55B_EDGE = OUT / "cm2_round306c55b_global_component_adjacency_known_sheet_component_edges_and_glue_v1.jsonl.gz"
C55B_COMPONENT = OUT / "cm2_round306c55b_global_component_adjacency_known_sheet_ordinary_components_v1.jsonl.gz"

C35 = ROOT / ".cm2-runtime/candidates/c35-transition-registry-20260810T145204Z-43f2cb35f9817ae2"
C36 = ROOT / ".cm2-runtime/candidates/c36-template-margin-atlas-20260810T153254Z-f37f908cf93d924c"
C41 = ROOT / ".cm2-runtime/candidates/c41-lower-strata-depth3-20260811T023804Z-f997365c91559599"
C53_HEAD = ROOT / ".cm2-runtime/cm2-global-authority-heads/predecessor-10fb050d30c92b0f2bdcf85a30d28ff670d8efc0b48104b7f04a63c391967b41.seal"

EXPECTED = {
    "C55A_RESULT_FILE": "d38f39792fc944b72e70100f9f96f312b5e30e034d5104ce5f848d24378ae5af",
    "C55A_RESULT_OBJECT": "93b732cd65be4453e7b29379d7f70d8c849057d5bcba5489e1f6c4dd705972e3",
    "C55A_LEAF_FILE": "e80c012e3260e8f9e68d5858ba5d9dafd94611e2a1c1200d787a20e3842d8db6",
    "C55A_LEAF_OBJECT": "7dd4c19cfb2b9f8cd30a4a9a23e30f11734e856cc6cc5a04e9a169c051059d90",
    "C55B_RESULT_FILE": "6bf9cae7b4b422c5c2121f95828e1508700fe1a5d1b1128598c8617f65032a93",
    "C55B_RESULT_OBJECT": "1ce396e9746d3c0364325e8308e94c9dcd4a3bfbba8c17a9c9961915e807cc56",
    "C35_OBJECT": "cb524ae587390a578683c88d933125e041ab2a906f0351370d58f3b0d67aa752",
    "C36_OBJECT": "9251693da7d6cc0ff6011fb965276ac64be2b79be8f245ab8954291a43fb4167",
    "C41_OBJECT": "b7e47a4ca9d6f4bb1fee10e78877850d5070f6d3c2b06bb0234fbabdaa2b7b24",
    "C53_HEAD_FILE": "f62483c87df4b6f4a8a2ad8dcf56febbfce9977200ce94a0ad6ce38e736aeeb3",
    "C53_HEAD_OBJECT": "cb90ab914c3b6518384669f42d05df33c21a717596190131c6a0f5683934cbfb",
    "C53_CHECKPOINT": "b58d68a0234b8a7de0e9147f891d37910476d622b840cfa073aed7ff3b4382ab",
}

ATLAS_SCOPE = "DUAL_R139_SEED_COLLARS_ONLY"
ANCHOR_BLOCKER = "C36_SEED_COLLAR_MARGIN_PRESENT__WHOLE_CELL_COVERAGE_MISSING"
CORRIDOR_BLOCKER = "TOPOLOGICAL_CORRIDOR_ONLY__EDGEWISE_MARGIN_OWNER_HISTORY_TRANSPORT_MISSING"
ISLAND_BLOCKER = "FORMAL_EXCLUSION_CUT__EVENT_EXTERIOR_DECIDER_MISSING"


class FailClosed(RuntimeError):
    pass


def require(condition: bool, label: str) -> None:
    if not condition:
        raise FailClosed(label)


def canonical(value: Any) -> bytes:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    ).encode("utf-8")


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def file_sha(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def strict_json(path: Path) -> dict[str, Any]:
    def hook(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        out: dict[str, Any] = {}
        for key, value in pairs:
            require(key not in out, f"duplicate JSON key:{path}:{key}")
            out[key] = value
        return out

    with path.open("r", encoding="utf-8") as stream:
        value = json.load(stream, object_pairs_hook=hook)
    require(type(value) is dict, f"top-level object:{path}")
    return value


def validate_object(value: dict[str, Any], expected: str, label: str) -> None:
    semantic = dict(value)
    claimed = semantic.pop("object_sha256", None)
    require(claimed == expected == digest(semantic), f"object closure:{label}")


def validate_named_object(
    value: dict[str, Any], field: str, expected: str, label: str,
) -> None:
    semantic = dict(value)
    claimed = semantic.pop(field, None)
    require(claimed == expected == digest(semantic), f"object closure:{label}")


def validate_row(row: dict[str, Any], label: str) -> None:
    semantic = dict(row)
    claimed = semantic.pop("row_sha256", None)
    require(type(claimed) is str and digest(semantic) == claimed, f"row closure:{label}")


def read_ledger(path: Path, descriptor: dict[str, Any]) -> list[dict[str, Any]]:
    require(path.name == descriptor["filename"], f"ledger name:{path}")
    require(path.stat().st_size == descriptor["size"], f"ledger size:{path}")
    require(file_sha(path) == descriptor["sha256"], f"ledger file hash:{path}")
    rows: list[dict[str, Any]] = []
    sequence = hashlib.sha256()
    with gzip.open(path, "rt", encoding="utf-8") as stream:
        for index, line in enumerate(stream):
            row = json.loads(line)
            require(type(row) is dict, f"ledger row object:{path}:{index}")
            validate_row(row, f"{path}:{index}")
            sequence.update((row["row_sha256"] + "\n").encode("ascii"))
            rows.append(row)
    require(len(rows) == descriptor["row_count"], f"ledger row count:{path}")
    require(
        sequence.hexdigest() == descriptor["row_hash_line_sequence_sha256"],
        f"ledger row sequence:{path}",
    )
    return rows


class LedgerWriter:
    def __init__(self, path: Path, order: str) -> None:
        self.path = path
        self.order = order
        self.count = 0
        self.sequence = hashlib.sha256()
        self.raw: Any = None
        self.gz: Any = None

    def __enter__(self) -> "LedgerWriter":
        self.raw = self.path.open("wb")
        self.gz = gzip.GzipFile(filename="", mode="wb", fileobj=self.raw, mtime=0)
        return self

    def write(self, semantic: dict[str, Any]) -> dict[str, Any]:
        require("row_sha256" not in semantic, "writer requires open row")
        row_hash = digest(semantic)
        row = {**semantic, "row_sha256": row_hash}
        self.gz.write(canonical(row) + b"\n")
        self.sequence.update((row_hash + "\n").encode("ascii"))
        self.count += 1
        return row

    def __exit__(self, *_args: Any) -> None:
        self.gz.close()
        self.raw.close()

    def descriptor(self) -> dict[str, Any]:
        return {
            "filename": self.path.name,
            "order": self.order,
            "row_count": self.count,
            "row_hash_line_sequence_sha256": self.sequence.hexdigest(),
            "sha256": file_sha(self.path),
            "size": self.path.stat().st_size,
        }


def sequence_sha(values: Iterable[str]) -> str:
    h = hashlib.sha256()
    for value in values:
        h.update((value + "\n").encode("ascii"))
    return h.hexdigest()


def edge_step(edge: dict[str, Any], source: str, target: str) -> dict[str, Any]:
    require({source, target} == {edge["left_cell_id"], edge["right_cell_id"]}, "edge step endpoints")
    return {
        "from_cell_id": source,
        "to_cell_id": target,
        "C55B_edge_row_sha256": edge["row_sha256"],
        "upstream_row_sha256": edge["upstream_row_sha256"],
        "face_or_corner_id": edge["face_or_corner_id"],
        "glue_kind": edge["glue_kind"],
        "gluing_proof_kind": edge["gluing_proof_kind"],
        "dimension": edge["dimension"],
        "exact_geometry": edge["exact_geometry"],
    }


def attack_self_test(summary: dict[str, Any]) -> dict[str, Any]:
    """Small producer-local guard; the independent verifier is authoritative."""
    required = {
        "large_component_count": 2,
        "current_unresolved_cell_count": 1124,
        "topological_corridor_cell_count": 1044,
        "separator_island_cell_count": 80,
        "separator_island_count": 22,
        "post_C53_pending_logical_task_count": 33319,
        "C35_C36_occurrence_count": 1648,
        "cell_occurrence_refined_stratum_count": 1852352,
        "formal_closed_cell_count": 0,
    }

    def guard(candidate: dict[str, Any]) -> None:
        for key, expected in required.items():
            require(candidate.get(key) == expected, f"self-test projection:{key}")
        require(
            candidate["topological_corridor_cell_count"]
            + candidate["separator_island_cell_count"]
            == candidate["current_unresolved_cell_count"],
            "self-test cell partition",
        )
        require(
            candidate["cell_occurrence_refined_stratum_count"]
            == candidate["current_unresolved_cell_count"] * candidate["C35_C36_occurrence_count"],
            "self-test product",
        )

    guard(summary)
    attacks: dict[str, str] = {}
    for name, key, bad in (
        ("drop_component", "large_component_count", 1),
        ("drop_cell", "current_unresolved_cell_count", 1123),
        ("forge_corridor", "topological_corridor_cell_count", 1045),
        ("drop_island_cell", "separator_island_cell_count", 79),
        ("drop_island", "separator_island_count", 21),
        ("drop_task", "post_C53_pending_logical_task_count", 33318),
        ("truncate_occurrence", "C35_C36_occurrence_count", 1647),
        ("truncate_product", "cell_occurrence_refined_stratum_count", 1852351),
        ("forge_formal_credit", "formal_closed_cell_count", 1),
    ):
        altered = dict(summary)
        altered[key] = bad
        try:
            guard(altered)
        except FailClosed:
            attacks[name] = "FAIL_CLOSED"
        else:
            raise FailClosed(f"self-test attack accepted:{name}")
    return {
        "status": "PASS_9_OF_9_PRODUCER_PROJECTION_ATTACKS_FAIL_CLOSED",
        "attack_count": 9,
        "attacks": attacks,
        "projection_object_sha256": digest(summary),
    }


def build() -> dict[str, Any]:
    # Freeze and validate all authority/result bytes before producing output.
    require(file_sha(C55A_RESULT) == EXPECTED["C55A_RESULT_FILE"], "C55-A result file pin")
    c55a_result = strict_json(C55A_RESULT)
    validate_object(c55a_result, EXPECTED["C55A_RESULT_OBJECT"], "C55-A result")
    require(file_sha(C55A_LEAF) == EXPECTED["C55A_LEAF_FILE"], "C55-A leaf file pin")
    require(
        c55a_result["bnb"]["leaf_ledger_object_sha256"] == EXPECTED["C55A_LEAF_OBJECT"],
        "C55-A leaf object binding",
    )
    require(file_sha(C55B_RESULT) == EXPECTED["C55B_RESULT_FILE"], "C55-B result file pin")
    c55b_result = strict_json(C55B_RESULT)
    validate_object(c55b_result, EXPECTED["C55B_RESULT_OBJECT"], "C55-B result")

    c35_result = strict_json(C35 / "result.json")
    c36_result = strict_json(C36 / "result.json")
    c41_result = strict_json(C41 / "result.json")
    validate_object(c35_result, EXPECTED["C35_OBJECT"], "C35")
    validate_object(c36_result, EXPECTED["C36_OBJECT"], "C36")
    validate_object(c41_result, EXPECTED["C41_OBJECT"], "C41")
    require(c36_result["map_stage_census"]["scope"] == ATLAS_SCOPE, "C36 atlas scope")
    require(file_sha(C53_HEAD) == EXPECTED["C53_HEAD_FILE"], "C53 head file pin")
    c53_head = strict_json(C53_HEAD)
    validate_named_object(
        c53_head,
        "authority_seal_object_sha256",
        EXPECTED["C53_HEAD_OBJECT"],
        "C53 head",
    )
    require(
        c53_head["post_seal_effective_checkpoint_object_sha256"]
        == EXPECTED["C53_CHECKPOINT"],
        "C53 effective checkpoint",
    )

    cells = read_ledger(C55B_CELL, c55b_result["ledgers"]["cell_component_crosswalk"])
    edges = read_ledger(C55B_EDGE, c55b_result["ledgers"]["component_edges_and_glue"])
    components = read_ledger(C55B_COMPONENT, c55b_result["ledgers"]["ordinary_components"])
    crosswalk = {row["cell_id"]: row for row in cells}
    component_map = {row["component_index"]: row for row in components}
    require(len(crosswalk) == 1724 and set(component_map) == set(range(26)), "C55-B atlas cardinality")

    # C55-A is a monolithic exact-byte ledger.  Only its 574 blocker rows are
    # retained in memory here; the 76,832 leaf rows are not duplicated.
    c55a_leaf = strict_json(C55A_LEAF)
    require(c55a_leaf.get("object_sha256") == EXPECTED["C55A_LEAF_OBJECT"], "C55-A leaf embedded object")
    blockers = c55a_leaf["blocker_rows"]
    require(len(blockers) == 574, "C55-A blocker count")
    for index, row in enumerate(blockers):
        validate_row(row, f"C55-A blocker:{index}")
    del c55a_leaf

    blocker_by_cell: dict[str, tuple[dict[str, Any], str]] = {}
    large_blockers: list[dict[str, Any]] = []
    for blocker in blockers:
        rep = blocker["representative_cell_id"]
        ref = blocker["reflected_cell_id"]
        require(rep in crosswalk and ref in crosswalk, "blocker cell crosswalk")
        if crosswalk[rep]["component_index"] in (0, 1):
            require(crosswalk[ref]["component_index"] in (0, 1), "large reflection placement")
            large_blockers.append(blocker)
            require(rep not in blocker_by_cell and ref not in blocker_by_cell, "unique blocker cell")
            blocker_by_cell[rep] = (blocker, "REPRESENTATIVE")
            blocker_by_cell[ref] = (blocker, "REFLECTED")
    unresolved = set(blocker_by_cell)
    require(len(large_blockers) == 562 and len(unresolved) == 1124, "large unresolved census")
    require(
        Counter(crosswalk[cell]["component_index"] for cell in unresolved) == Counter({0: 562, 1: 562}),
        "large component unresolved split",
    )

    # Read and bind the full C35/C36 occurrence rows.
    c35_occurrences = read_ledger(C35 / c35_result["ledgers"]["path_occurrences"]["filename"], c35_result["ledgers"]["path_occurrences"])
    c36_bindings = read_ledger(C36 / c36_result["ledgers"]["occurrence_margin_bindings"]["filename"], c36_result["ledgers"]["occurrence_margin_bindings"])
    require(len(c35_occurrences) == len(c36_bindings) == 1648, "R1648 occurrence census")
    for index, (occurrence, margin) in enumerate(zip(c35_occurrences, c36_bindings, strict=True), start=1):
        require(occurrence["collision_index"] == margin["collision_index"] == index, "occurrence index alignment")
        for field in (
            "geometry_template_id",
            "official_word_variant_id",
            "incoming_absolute_owner_id",
            "selected_absolute_owner_id",
            "incoming_chart",
            "outgoing_chart",
            "destination_core_id",
        ):
            require(occurrence[field] == margin[field], f"C35/C36 occurrence projection:{index}:{field}")
        require(
            margin["owner_discriminant_root_order_word_chart_core_map_status"]
            == "MATERIALIZED_ON_DUAL_R139_SEED_COLLARS",
            f"C36 collar-only status:{index}",
        )

    # Verify every referenced post-C53 logical task against the frozen C41
    # routed-ambient ledger and retain only compact fields needed below.
    wanted_task_hashes: set[str] = set()
    task_to_blocker: dict[str, dict[str, Any]] = {}
    for blocker in large_blockers:
        for task_hash in blocker["residual_source_row_sha256s"]:
            require(task_hash not in wanted_task_hashes, "duplicate pending logical task")
            wanted_task_hashes.add(task_hash)
            task_to_blocker[task_hash] = blocker
    require(len(wanted_task_hashes) == 33319, "post-C53 large-component logical task census")

    routed_desc = c41_result["ledgers"]["routed_ambient_cells"]
    routed_path = C41 / routed_desc["filename"]
    require(file_sha(routed_path) == routed_desc["sha256"], "C41 routed ledger file pin")
    c41_selected: dict[str, dict[str, Any]] = {}
    c41_sequence = hashlib.sha256()
    routed_count = 0
    with gzip.open(routed_path, "rt", encoding="utf-8") as stream:
        for routed_count, line in enumerate(stream, start=1):
            row = json.loads(line)
            validate_row(row, f"C41 routed:{routed_count}")
            row_hash = row["row_sha256"]
            c41_sequence.update((row_hash + "\n").encode("ascii"))
            if row_hash in wanted_task_hashes:
                blocker = task_to_blocker[row_hash]
                require(row["pair_index"] == blocker["pair_index"], "C41/blocker pair")
                require(row["representative_cell_id"] == blocker["representative_cell_id"], "C41/blocker representative")
                require(row["reflected_cell_id"] == blocker["reflected_cell_id"], "C41/blocker reflected")
                c41_selected[row_hash] = {
                    "residual_classification": row["residual_classification"],
                    "path": row["path"],
                    "source_path": row["source_path"],
                    "descendant_bits": row["descendant_bits"],
                    "parent_volume_fraction": row["parent_volume_fraction"],
                    "split_axis_history": row["split_axis_history"],
                    "route_method": row["route_method"],
                    "round144_terminal_class": row["round144_terminal_class"],
                }
    require(routed_count == routed_desc["row_count"], "C41 routed row count")
    require(c41_sequence.hexdigest() == routed_desc["row_hash_line_sequence_sha256"], "C41 routed row sequence")
    require(set(c41_selected) == wanted_task_hashes, "all pending task hashes found in C41")

    # Reconstruct the current-unresolved induced graph.  Multiple exact faces
    # between a pair are allowed; the lexicographically smallest row hash is
    # the deterministic corridor edge.
    adjacency: dict[str, list[tuple[str, dict[str, Any]]]] = defaultdict(list)
    incident: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for edge in edges:
        left = edge.get("left_cell_id")
        right = edge.get("right_cell_id")
        if left is not None:
            incident[left].append(edge)
        if right is not None:
            incident[right].append(edge)
        if (
            edge["scope"] == "ORDINARY_INTERNAL"
            and left in unresolved
            and right in unresolved
        ):
            adjacency[left].append((right, edge))
            adjacency[right].append((left, edge))
    for cell_id in adjacency:
        adjacency[cell_id].sort(key=lambda item: (item[0], item[1]["row_sha256"]))

    parent: dict[str, tuple[str, dict[str, Any]] | None] = {}
    distance: dict[str, int] = {}
    anchors: dict[int, str] = {}
    for component_index in (0, 1):
        component = component_map[component_index]
        anchor = component["known_sheet_anchor"]["anchor_cell_id"]
        require(anchor in unresolved, f"anchor current unresolved:{component_index}")
        anchors[component_index] = anchor
        parent[anchor] = None
        distance[anchor] = 0
        queue: deque[str] = deque([anchor])
        while queue:
            cell_id = queue.popleft()
            for neighbor, edge in adjacency.get(cell_id, []):
                if crosswalk[neighbor]["component_index"] != component_index or neighbor in parent:
                    continue
                parent[neighbor] = (cell_id, edge)
                distance[neighbor] = distance[cell_id] + 1
                queue.append(neighbor)
    reachable = set(parent)
    require(len(reachable) == 1044, "topological corridor census")
    require(Counter(crosswalk[cell]["component_index"] for cell in reachable) == Counter({0: 522, 1: 522}), "corridor component split")
    unreachable = unresolved - reachable
    require(len(unreachable) == 80, "separator-cell census")

    # Exact connected components of the unresolved cells cut off from the
    # anchors.  Their boundary rows are retained verbatim by hash plus compact
    # exact-geometry commitments.
    island_by_cell: dict[str, str] = {}
    island_rows_semantic: list[dict[str, Any]] = []
    for component_index in (0, 1):
        remaining = {cell for cell in unreachable if crosswalk[cell]["component_index"] == component_index}
        local_islands: list[list[str]] = []
        while remaining:
            seed = min(remaining)
            found = {seed}
            queue = deque([seed])
            while queue:
                cell_id = queue.popleft()
                for neighbor, _edge in adjacency.get(cell_id, []):
                    if neighbor in remaining and neighbor not in found:
                        found.add(neighbor)
                        queue.append(neighbor)
            remaining -= found
            local_islands.append(sorted(found))
        local_islands.sort(key=lambda values: (values[0], len(values)))
        for local_index, members in enumerate(local_islands):
            island_id = "c56l-separator-island:" + digest(
                {"component_index": component_index, "member_cell_ids": members}
            )
            member_set = set(members)
            for cell_id in members:
                require(cell_id not in island_by_cell, "unique island cell")
                island_by_cell[cell_id] = island_id
            boundary: dict[str, dict[str, Any]] = {}
            for cell_id in members:
                for edge in incident.get(cell_id, []):
                    left = edge.get("left_cell_id")
                    right = edge.get("right_cell_id")
                    other = right if left == cell_id else left
                    if other in member_set:
                        continue
                    boundary[edge["row_sha256"]] = {
                        "C55B_edge_row_sha256": edge["row_sha256"],
                        "upstream_row_sha256": edge["upstream_row_sha256"],
                        "face_or_corner_id": edge["face_or_corner_id"],
                        "glue_kind": edge["glue_kind"],
                        "scope": edge["scope"],
                        "dimension": edge["dimension"],
                        "left_cell_id": left,
                        "right_cell_id": right,
                        "left_disposition": edge["left_disposition"],
                        "right_disposition": edge["right_disposition"],
                        "exact_geometry_sha256": digest(edge["exact_geometry"]),
                    }
            boundary_rows = [boundary[key] for key in sorted(boundary)]
            require(boundary_rows, f"island boundary nonempty:{island_id}")
            boundary_scope = Counter(row["scope"] for row in boundary_rows)
            boundary_dispositions = Counter(
                value
                for row in boundary_rows
                for value in (row["left_disposition"], row["right_disposition"])
                if value is not None and value != "UNRESOLVED_R1648_CONTINUATION"
            )
            require(boundary_dispositions, f"island has an exact non-unresolved cut:{island_id}")
            if boundary_dispositions.get("TYPED_EVENT_GRAPH", 0):
                separator_kind = "EXACT_TYPED_EVENT_BOUNDARY__DYNAMIC_OWNER_GLUE_MISSING"
            elif any("GRAZING" in key for key in boundary_scope):
                separator_kind = "EXACT_GRAZING_BOUNDARY__POSITIVE_TERMINAL_DECIDER_MISSING"
            else:
                separator_kind = "FORMAL_EXCLUSION_CUT__DYNAMIC_EXTERIOR_DECIDER_MISSING"
            island_rows_semantic.append(
                {
                    "schema": ISLAND_SCHEMA,
                    "island_id": island_id,
                    "component_index": component_index,
                    "component_local_island_index": local_index,
                    "member_cell_count": len(members),
                    "member_cell_ids": members,
                    "member_cell_ids_sha256": digest(members),
                    "separator_kind": separator_kind,
                    "boundary_row_count": len(boundary_rows),
                    "boundary_rows": boundary_rows,
                    "boundary_scope_census": dict(sorted(boundary_scope.items())),
                    "boundary_nonunresolved_disposition_census": dict(sorted(boundary_dispositions.items())),
                    "event_or_exterior_terminal_decider_present": False,
                    "whole_cell_terminal_credit": 0,
                    "D02_gate_credit": 0,
                }
            )
    island_rows_semantic.sort(key=lambda row: (row["component_index"], row["member_cell_ids"][0]))
    require(len(island_rows_semantic) == 22 and set(island_by_cell) == unreachable, "separator island partition")

    with LedgerWriter(OUT / ISLAND_FILE, "COMPONENT_INDEX_THEN_MINIMUM_MEMBER_CELL_ID") as island_writer:
        island_rows = [island_writer.write(row) for row in island_rows_semantic]
    island_desc = island_writer.descriptor()
    island_row_hash = {row["island_id"]: row["row_sha256"] for row in island_rows}

    # One explicit corridor or separator witness per physical cell.
    cell_rows: list[dict[str, Any]] = []
    cell_primary = Counter()
    corridor_primary = Counter()
    separator_primary = Counter()
    distance_census = Counter()
    with LedgerWriter(OUT / CELL_FILE, "COMPONENT_INDEX_THEN_CELL_ID") as cell_writer:
        for cell_id in sorted(unresolved, key=lambda value: (crosswalk[value]["component_index"], value)):
            cross = crosswalk[cell_id]
            blocker, role = blocker_by_cell[cell_id]
            component = component_map[cross["component_index"]]
            primary = blocker["primary_residual_classification"]
            cell_primary[primary] += 1
            task_hashes = blocker["residual_source_row_sha256s"]
            semantic: dict[str, Any] = {
                "schema": CELL_SCHEMA,
                "cell_id": cell_id,
                "component_index": cross["component_index"],
                "component_id": cross["component_id"],
                "reflection_role": role,
                "reflection_partner_cell_id": cross["reflection_partner_cell_id"],
                "pair_index": blocker["pair_index"],
                "C55B_crosswalk_row_sha256": cross["row_sha256"],
                "C55A_blocker_row_sha256": blocker["row_sha256"],
                "primary_residual_classification": primary,
                "post_C53_pending_logical_task_count_for_pair": len(task_hashes),
                "post_C53_pending_logical_task_row_hash_sequence_sha256": sequence_sha(task_hashes),
                "anchor_cell_id": anchors[cross["component_index"]],
                "anchor_binding": component["known_sheet_anchor"],
                "C36_atlas_scope": ATLAS_SCOPE,
                "all_1648_occurrences_bound": True,
                "edgewise_margin_transport_complete": False,
                "edgewise_owner_transport_complete": False,
                "edgewise_history_transport_complete": False,
                "whole_cell_connected_to_known_proved": False,
                "whole_cell_terminal_credit": 0,
                "D02_gate_credit": 0,
            }
            if cell_id in reachable:
                chain: list[dict[str, Any]] = []
                cursor = cell_id
                while parent[cursor] is not None:
                    next_cell, edge = parent[cursor]  # type: ignore[misc]
                    chain.append(edge_step(edge, cursor, next_cell))
                    cursor = next_cell
                require(cursor == anchors[cross["component_index"]], "corridor terminates at anchor")
                semantic.update(
                    {
                        "witness_kind": "EXPLICIT_TOPOLOGICAL_CORRIDOR_TO_STRICT_OPEN_ANCHOR",
                        "refinement_blocker_class": ANCHOR_BLOCKER if cell_id == cursor else CORRIDOR_BLOCKER,
                        "corridor_step_count": len(chain),
                        "corridor_steps": chain,
                        "corridor_step_row_hash_sequence_sha256": sequence_sha(
                            step["C55B_edge_row_sha256"] for step in chain
                        ),
                        "separator_island_id": None,
                        "separator_island_row_sha256": None,
                    }
                )
                corridor_primary[primary] += 1
                distance_census[len(chain)] += 1
            else:
                island_id = island_by_cell[cell_id]
                semantic.update(
                    {
                        "witness_kind": "EXACT_SEPARATOR_ISLAND_BLOCKER",
                        "refinement_blocker_class": ISLAND_BLOCKER,
                        "corridor_step_count": None,
                        "corridor_steps": None,
                        "corridor_step_row_hash_sequence_sha256": None,
                        "separator_island_id": island_id,
                        "separator_island_row_sha256": island_row_hash[island_id],
                    }
                )
                separator_primary[primary] += 1
            cell_rows.append(cell_writer.write(semantic))
    cell_desc = cell_writer.descriptor()
    cell_row_by_id = {row["cell_id"]: row for row in cell_rows}
    require(len(cell_row_by_id) == 1124, "cell witness ledger cardinality")

    # Materialize all post-C53 logical C41 tasks in stable pair/hash order.
    logical_primary = Counter()
    logical_residual = Counter()
    with LedgerWriter(OUT / TASK_FILE, "PAIR_INDEX_THEN_C41_ROW_SHA256") as task_writer:
        for blocker in sorted(large_blockers, key=lambda row: row["pair_index"]):
            task_hashes = blocker["residual_source_row_sha256s"]
            require(task_hashes == sorted(task_hashes), "C55-A task hash order")
            for ordinal, task_hash in enumerate(task_hashes):
                selected = c41_selected[task_hash]
                logical_primary[blocker["primary_residual_classification"]] += 1
                logical_residual[selected["residual_classification"]] += 1
                task_writer.write(
                    {
                        "schema": TASK_SCHEMA,
                        "pair_index": blocker["pair_index"],
                        "pair_task_ordinal": ordinal,
                        "C55A_blocker_row_sha256": blocker["row_sha256"],
                        "C41_routed_ambient_row_sha256": task_hash,
                        "representative_cell_id": blocker["representative_cell_id"],
                        "reflected_cell_id": blocker["reflected_cell_id"],
                        "primary_residual_classification": blocker["primary_residual_classification"],
                        **selected,
                        "post_C53_effective_checkpoint_object_sha256": EXPECTED["C53_CHECKPOINT"],
                        "current_pending_logical_task": True,
                        "formal_credit": 0,
                        "D02_gate_credit": 0,
                    }
                )
    task_desc = task_writer.descriptor()
    require(task_desc["row_count"] == 33319, "task output count")

    # Exact common-refinement product.  It is deliberately compact: every row
    # binds a physical cell witness to the exact C35 occurrence and C36 margin
    # row.  Long geometry/margin payloads stay in their already hash-closed
    # upstream ledgers.
    with LedgerWriter(OUT / REFINEMENT_FILE, "COMPONENT_INDEX_THEN_CELL_ID_THEN_COLLISION_INDEX") as refinement_writer:
        for cell_ordinal, cell in enumerate(cell_rows, start=1):
            blocker_class = cell["refinement_blocker_class"]
            for occurrence, margin in zip(c35_occurrences, c36_bindings, strict=True):
                refinement_writer.write(
                    {
                        "schema": REFINEMENT_SCHEMA,
                        "component_index": cell["component_index"],
                        "cell_id": cell["cell_id"],
                        "C56L_cell_witness_row_sha256": cell["row_sha256"],
                        "primary_residual_classification": cell["primary_residual_classification"],
                        "collision_index": occurrence["collision_index"],
                        "C35_occurrence_row_sha256": occurrence["row_sha256"],
                        "C36_occurrence_margin_row_sha256": margin["row_sha256"],
                        "C36_collar_margin_vectors_sha256": margin["collar_margin_vectors_sha256"],
                        "C36_atlas_scope": ATLAS_SCOPE,
                        "factorized_refinement_key_exact": True,
                        "geometric_cell_occurrence_refinement_proved": False,
                        "refinement_blocker_class": blocker_class,
                        "margin_transport_proved": False,
                        "owner_transport_proved": False,
                        "history_transport_proved": False,
                        "strict_terminal_class": None,
                        "whole_cell_terminal_credit": 0,
                        "D02_gate_credit": 0,
                    }
                )
            if cell_ordinal % 100 == 0:
                print(f"common-refinement cells {cell_ordinal}/1124", flush=True)
    refinement_desc = refinement_writer.descriptor()
    require(refinement_desc["row_count"] == 1124 * 1648, "refinement product count")

    # Exact per-component and per-primary-class accounting.
    class_rows: list[dict[str, Any]] = []
    all_primary = sorted(cell_primary)
    for primary in all_primary:
        class_rows.append(
            {
                "primary_residual_classification": primary,
                "physical_cell_count": cell_primary[primary],
                "topological_corridor_cell_count": corridor_primary[primary],
                "separator_island_cell_count": separator_primary[primary],
                "post_C53_pending_logical_task_count": logical_primary[primary],
                "cell_occurrence_refined_stratum_count": cell_primary[primary] * 1648,
                "formal_closed_cell_count": 0,
                "formal_remaining_cell_count": cell_primary[primary],
                "D02_gate_credit": 0,
            }
        )

    component_rows: list[dict[str, Any]] = []
    with LedgerWriter(OUT / COMPONENT_FILE, "COMPONENT_INDEX_ASCENDING") as component_writer:
        for component_index in (0, 1):
            member_cells = sorted(cell for cell in unresolved if crosswalk[cell]["component_index"] == component_index)
            member_pairs = {blocker_by_cell[cell][0]["row_sha256"] for cell in member_cells}
            component_task_hashes = {
                task_hash
                for blocker in large_blockers
                if blocker["row_sha256"] in member_pairs
                for task_hash in blocker["residual_source_row_sha256s"]
            }
            local_islands = [row for row in island_rows if row["component_index"] == component_index]
            semantic = {
                "schema": COMPONENT_SCHEMA,
                "component_index": component_index,
                "component_id": component_map[component_index]["component_id"],
                "C55B_component_row_sha256": component_map[component_index]["row_sha256"],
                "anchor_binding": component_map[component_index]["known_sheet_anchor"],
                "current_unresolved_cell_count": len(member_cells),
                "topological_corridor_cell_count": sum(cell in reachable for cell in member_cells),
                "separator_island_cell_count": sum(cell in unreachable for cell in member_cells),
                "separator_island_count": len(local_islands),
                "maximum_corridor_step_count": max(distance[cell] for cell in member_cells if cell in reachable),
                "post_C53_pending_logical_task_count": len(component_task_hashes),
                "C35_C36_occurrence_count": 1648,
                "cell_occurrence_refined_stratum_count": len(member_cells) * 1648,
                "all_refinements_covered": True,
                "refinements_pairwise_key_distinct": True,
                "edgewise_margin_owner_history_transport_complete": False,
                "formal_closed_cell_count": 0,
                "formal_remaining_cell_count": len(member_cells),
                "whole_component_connected_to_known_credit": 0,
                "D02_gate_credit": 0,
            }
            component_rows.append(component_writer.write(semantic))
    component_desc = component_writer.descriptor()

    summary = {
        "large_component_count": 2,
        "current_unresolved_cell_count": 1124,
        "topological_corridor_cell_count": len(reachable),
        "separator_island_cell_count": len(unreachable),
        "separator_island_count": len(island_rows),
        "post_C53_pending_logical_task_count": len(wanted_task_hashes),
        "C35_C36_occurrence_count": len(c35_occurrences),
        "cell_occurrence_refined_stratum_count": refinement_desc["row_count"],
        "formal_closed_cell_count": 0,
        "formal_remaining_cell_count": 1124,
        "D02_gate_credit": 0,
    }
    self_test = attack_self_test(summary)

    result: dict[str, Any] = {
        "schema": PRODUCER_SCHEMA + ".result",
        "status": (
            "PASS_EXACT_1124_CELL_CORRIDOR_SEPARATOR_AND_1852352_KEY_REFINEMENT_LEDGER__"
            "FAIL_CLOSED_ZERO_WHOLE_CELL_CREDIT__EDGEWISE_MARGIN_OWNER_HISTORY_TRANSPORT_MISSING"
        ),
        "authority_binding": {
            "C55A_result_file_sha256": EXPECTED["C55A_RESULT_FILE"],
            "C55A_result_object_sha256": EXPECTED["C55A_RESULT_OBJECT"],
            "C55A_leaf_file_sha256": EXPECTED["C55A_LEAF_FILE"],
            "C55A_leaf_object_sha256": EXPECTED["C55A_LEAF_OBJECT"],
            "C55B_result_file_sha256": EXPECTED["C55B_RESULT_FILE"],
            "C55B_result_object_sha256": EXPECTED["C55B_RESULT_OBJECT"],
            "C35_object_sha256": EXPECTED["C35_OBJECT"],
            "C36_object_sha256": EXPECTED["C36_OBJECT"],
            "C41_object_sha256": EXPECTED["C41_OBJECT"],
            "C53_head_file_sha256": EXPECTED["C53_HEAD_FILE"],
            "C53_head_object_sha256": EXPECTED["C53_HEAD_OBJECT"],
            "C53_effective_checkpoint_object_sha256": EXPECTED["C53_CHECKPOINT"],
        },
        "scope": summary,
        "topology": {
            "anchor_cell_ids": {str(key): value for key, value in anchors.items()},
            "corridor_distance_census": {str(key): value for key, value in sorted(distance_census.items())},
            "maximum_corridor_step_count": max(distance.values()),
            "corridor_kind": "CURRENT_UNRESOLVED_INDUCED_EXACT_FACE_OR_SOURCE_SEAM_GRAPH",
            "corridor_is_dynamic_known_sheet_proof": False,
            "separator_islands_are_exact_unresolved_induced_components": True,
        },
        "common_refinement": {
            "factorized_key": ["C55B_PHYSICAL_CELL", "C35_R1648_OCCURRENCE", "C36_MARGIN_BINDING"],
            "factorized_refinement_key_exact": True,
            "all_1124_x_1648_keys_materialized": True,
            "C36_atlas_scope": ATLAS_SCOPE,
            "geometric_cell_occurrence_refinement_proved": False,
            "missing_global_bridge": [
                "EDGEWISE_MARGIN_TRANSPORT",
                "EDGEWISE_OWNER_TRANSPORT",
                "EDGEWISE_HISTORY_TRANSPORT",
                "EVENT_OR_EXTERIOR_STRICT_DECIDER_FOR_SEPARATOR_ISLANDS",
            ],
        },
        "primary_residual_classification_accounting": class_rows,
        "actual_C41_residual_classification_logical_task_census": dict(sorted(logical_residual.items())),
        "formal_effect": {
            "whole_cell_CONNECTED_TO_KNOWN_credit": 0,
            "whole_component_CONNECTED_TO_KNOWN_credit": 0,
            "D02_gate_credit": 0,
            "formal_credit": 0,
            "current_four_class_census_unchanged": {
                "EARLIEST_PREFIX_EXCLUDED": 75388,
                "TYPED_EVENT_GRAPH": 296,
                "CONNECTED_TO_KNOWN": 0,
                "SOURCE_GRAZING_OR_CEMETERY": 0,
                "UNRESOLVED_R1648_CONTINUATION": 1148,
                "total": 76832,
            },
            "CM2": "NO-GO_FOR_CLAIM",
        },
        "self_test": self_test,
        "ledgers": {
            "corridor_and_separator_cells": cell_desc,
            "separator_islands": island_desc,
            "post_C53_pending_logical_tasks": task_desc,
            "cell_occurrence_common_refinement": refinement_desc,
            "component_summary": component_desc,
        },
        "required_next": (
            "construct an independent global edgewise margin/owner/history transport atlas on all "
            "1,852,352 cell-occurrence keys and an exact event/exterior strict decider for the 22 "
            "separator islands; only then re-evaluate whole-cell CONNECTED_TO_KNOWN credit"
        ),
    }
    result["object_sha256"] = digest(result)
    (OUT / RESULT_FILE).write_bytes(canonical(result) + b"\n")
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--build", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if not args.build and not args.self_test:
        args.build = True
    if args.build:
        result = build()
        print(json.dumps({
            "status": result["status"],
            "object_sha256": result["object_sha256"],
            "scope": result["scope"],
        }, sort_keys=True))
    elif args.self_test:
        result = strict_json(OUT / RESULT_FILE)
        validate_object(result, result["object_sha256"], "existing C56-L result")
        print(json.dumps(attack_self_test(result["scope"]), sort_keys=True))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (FailClosed, OSError, ValueError, KeyError, TypeError) as exc:
        print(f"FAIL_CLOSED:{type(exc).__name__}:{exc}", file=sys.stderr)
        raise SystemExit(2)
