#!/usr/bin/env python3
"""Independent no-producer verifier for C56-L.

The candidate producer is never imported or executed.  This verifier rebuilds
the unresolved graph, anchor BFS, separator islands, C41 task projection, and
the full 1,124 x 1,648 refinement product directly from frozen inputs.
"""

from __future__ import annotations

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
RESULT = OUT / (PREFIX + "_result_v1.json")
VERIFICATION = OUT / (PREFIX + "_independent_verification_v1.json")

C55A_RESULT = OUT / "cm2_round306c55a_four_chart_fundamental_domain_bnb_result_v1.json"
C55A_LEAF = OUT / "cm2_round306c55a_four_chart_fundamental_domain_bnb_leaf_ledger_v1.json"
C55B_RESULT = OUT / "cm2_round306c55b_global_component_adjacency_known_sheet_result_v1.json"
C35 = ROOT / ".cm2-runtime/candidates/c35-transition-registry-20260810T145204Z-43f2cb35f9817ae2"
C36 = ROOT / ".cm2-runtime/candidates/c36-template-margin-atlas-20260810T153254Z-f37f908cf93d924c"
C41 = ROOT / ".cm2-runtime/candidates/c41-lower-strata-depth3-20260811T023804Z-f997365c91559599"
C53_HEAD = ROOT / ".cm2-runtime/cm2-global-authority-heads/predecessor-10fb050d30c92b0f2bdcf85a30d28ff670d8efc0b48104b7f04a63c391967b41.seal"
CANONICAL = OUT / "CM2_LATEST_STATUS.md"

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
    "CANONICAL_FILE": "922fc5d01918b217556bc3f392c44efcc7c9c6345c881371e6cd34950eb99b57",
}

BASE_SCHEMA = "cm2.round306c56l.large-component-common-refinement.v1"
CELL_SCHEMA = BASE_SCHEMA + ".corridor-or-separator-cell-row"
ISLAND_SCHEMA = BASE_SCHEMA + ".separator-island-row"
TASK_SCHEMA = BASE_SCHEMA + ".post-c53-c41-logical-task-row"
REFINEMENT_SCHEMA = BASE_SCHEMA + ".cell-occurrence-refined-stratum-row"
COMPONENT_SCHEMA = BASE_SCHEMA + ".component-summary-row"
ATLAS_SCOPE = "DUAL_R139_SEED_COLLARS_ONLY"
ANCHOR_BLOCKER = "C36_SEED_COLLAR_MARGIN_PRESENT__WHOLE_CELL_COVERAGE_MISSING"
CORRIDOR_BLOCKER = "TOPOLOGICAL_CORRIDOR_ONLY__EDGEWISE_MARGIN_OWNER_HISTORY_TRANSPORT_MISSING"
ISLAND_BLOCKER = "FORMAL_EXCLUSION_CUT__EVENT_EXTERIOR_DECIDER_MISSING"


class Reject(RuntimeError):
    pass


def demand(value: bool, label: str) -> None:
    if not value:
        raise Reject(label)


def encoded(value: Any) -> bytes:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    ).encode("utf-8")


def object_hash(value: Any) -> str:
    return hashlib.sha256(encoded(value)).hexdigest()


def bytes_hash(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as source:
        while True:
            block = source.read(1024 * 1024)
            if not block:
                return h.hexdigest()
            h.update(block)


def load_object(path: Path) -> dict[str, Any]:
    def no_duplicates(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in pairs:
            demand(key not in result, f"duplicate key:{path}:{key}")
            result[key] = value
        return result

    with path.open("r", encoding="utf-8") as source:
        value = json.load(source, object_pairs_hook=no_duplicates)
    demand(type(value) is dict, f"object required:{path}")
    return value


def close_object(value: dict[str, Any], field: str, expected: str, label: str) -> None:
    semantic = dict(value)
    claim = semantic.pop(field, None)
    demand(claim == expected and object_hash(semantic) == expected, f"closed object:{label}")


def close_row(row: dict[str, Any], label: str) -> None:
    semantic = dict(row)
    claim = semantic.pop("row_sha256", None)
    demand(type(claim) is str and object_hash(semantic) == claim, f"closed row:{label}")


def line_sequence(values: Iterable[str]) -> str:
    h = hashlib.sha256()
    for value in values:
        h.update((value + "\n").encode("ascii"))
    return h.hexdigest()


def read_closed_ledger(base: Path, descriptor: dict[str, Any]) -> list[dict[str, Any]]:
    path = base / descriptor["filename"]
    demand(path.stat().st_size == descriptor["size"], f"size:{path}")
    demand(bytes_hash(path) == descriptor["sha256"], f"file hash:{path}")
    rows: list[dict[str, Any]] = []
    sequence = hashlib.sha256()
    with gzip.open(path, "rt", encoding="utf-8") as source:
        for index, line in enumerate(source):
            row = json.loads(line)
            demand(type(row) is dict, f"row object:{path}:{index}")
            close_row(row, f"{path}:{index}")
            sequence.update((row["row_sha256"] + "\n").encode("ascii"))
            rows.append(row)
    demand(len(rows) == descriptor["row_count"], f"row count:{path}")
    demand(sequence.hexdigest() == descriptor["row_hash_line_sequence_sha256"], f"row sequence:{path}")
    return rows


def exact_step(edge: dict[str, Any], source: str, target: str) -> dict[str, Any]:
    demand({source, target} == {edge["left_cell_id"], edge["right_cell_id"]}, "step endpoints")
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


def snapshot() -> dict[str, Any]:
    return {
        "C53_head_file_sha256": bytes_hash(C53_HEAD),
        "canonical_file_sha256": bytes_hash(CANONICAL),
        "runtime_head_stat": {
            "size": C53_HEAD.stat().st_size,
            "inode": C53_HEAD.stat().st_ino,
            "nlink": C53_HEAD.stat().st_nlink,
        },
    }


def projection_guard(summary: dict[str, Any], result: dict[str, Any]) -> None:
    exact = {
        "large_component_count": 2,
        "current_unresolved_cell_count": 1124,
        "topological_corridor_cell_count": 1044,
        "separator_island_cell_count": 80,
        "separator_island_count": 22,
        "post_C53_pending_logical_task_count": 33319,
        "C35_C36_occurrence_count": 1648,
        "cell_occurrence_refined_stratum_count": 1852352,
        "formal_closed_cell_count": 0,
        "formal_remaining_cell_count": 1124,
        "D02_gate_credit": 0,
    }
    demand(summary == exact, "exact result scope")
    common = result["common_refinement"]
    demand(common["all_1124_x_1648_keys_materialized"] is True, "product materialized")
    demand(common["factorized_refinement_key_exact"] is True, "factorized keys exact")
    demand(common["geometric_cell_occurrence_refinement_proved"] is False, "no geometric overclaim")
    demand(common["C36_atlas_scope"] == ATLAS_SCOPE, "C36 scope preserved")
    formal = result["formal_effect"]
    demand(
        formal["whole_cell_CONNECTED_TO_KNOWN_credit"]
        == formal["whole_component_CONNECTED_TO_KNOWN_credit"]
        == formal["D02_gate_credit"]
        == formal["formal_credit"]
        == 0,
        "all credit locks zero",
    )
    demand(formal["CM2"] == "NO-GO_FOR_CLAIM", "CM2 status")


def adversarial_checks(result: dict[str, Any], cells: list[dict[str, Any]]) -> dict[str, Any]:
    tests: dict[str, str] = {}

    def rejected(name: str, mutation: Any) -> None:
        clone = json.loads(json.dumps(result))
        mutation(clone)
        try:
            projection_guard(clone["scope"], clone)
        except Reject:
            tests[name] = "FAIL_CLOSED"
        else:
            raise Reject(f"attack accepted:{name}")

    rejected("cell_drop", lambda x: x["scope"].__setitem__("current_unresolved_cell_count", 1123))
    rejected("corridor_forge", lambda x: x["scope"].__setitem__("topological_corridor_cell_count", 1045))
    rejected("island_cell_drop", lambda x: x["scope"].__setitem__("separator_island_cell_count", 79))
    rejected("island_drop", lambda x: x["scope"].__setitem__("separator_island_count", 21))
    rejected("task_drop", lambda x: x["scope"].__setitem__("post_C53_pending_logical_task_count", 33318))
    rejected("occurrence_truncation", lambda x: x["scope"].__setitem__("C35_C36_occurrence_count", 1647))
    rejected("refinement_truncation", lambda x: x["scope"].__setitem__("cell_occurrence_refined_stratum_count", 1852351))
    rejected("formal_cell_forge", lambda x: x["scope"].__setitem__("formal_closed_cell_count", 1))
    rejected("D02_credit_forge", lambda x: x["scope"].__setitem__("D02_gate_credit", 1))
    rejected("geometric_proof_forge", lambda x: x["common_refinement"].__setitem__("geometric_cell_occurrence_refinement_proved", True))
    rejected("C36_scope_drift", lambda x: x["common_refinement"].__setitem__("C36_atlas_scope", "GLOBAL"))
    rejected("whole_cell_credit_forge", lambda x: x["formal_effect"].__setitem__("whole_cell_CONNECTED_TO_KNOWN_credit", 1))
    rejected("whole_component_credit_forge", lambda x: x["formal_effect"].__setitem__("whole_component_CONNECTED_TO_KNOWN_credit", 1))
    rejected("CM2_forge", lambda x: x["formal_effect"].__setitem__("CM2", "GO"))

    # Two row-local coherent attacks, checked independently of the result guard.
    sample = json.loads(json.dumps(cells[0]))
    original = sample["row_sha256"]
    sample["edgewise_margin_transport_complete"] = True
    semantic = dict(sample)
    semantic.pop("row_sha256")
    demand(object_hash(semantic) != original, "margin transport row tamper detected")
    tests["cell_margin_transport_byte_tamper"] = "FAIL_CLOSED"
    sample = json.loads(json.dumps(cells[-1]))
    original = sample["row_sha256"]
    sample["C55A_blocker_row_sha256"] = "0" * 64
    semantic = dict(sample)
    semantic.pop("row_sha256")
    demand(object_hash(semantic) != original, "blocker binding row tamper detected")
    tests["cell_blocker_binding_byte_tamper"] = "FAIL_CLOSED"
    demand(len(tests) == 16, "attack count")
    return {
        "status": "PASS_16_OF_16_COHERENT_ATTACKS_FAIL_CLOSED",
        "attack_count": 16,
        "attacks": tests,
    }


def verify() -> dict[str, Any]:
    before = snapshot()
    demand(before["C53_head_file_sha256"] == EXPECTED["C53_HEAD_FILE"], "C53 head snapshot pin")
    demand(before["canonical_file_sha256"] == EXPECTED["CANONICAL_FILE"], "canonical snapshot pin")

    result = load_object(RESULT)
    result_object = result.get("object_sha256")
    demand(type(result_object) is str, "candidate object field")
    close_object(result, "object_sha256", result_object, "C56-L result")
    projection_guard(result["scope"], result)

    # Independent upstream pins.
    demand(bytes_hash(C55A_RESULT) == EXPECTED["C55A_RESULT_FILE"], "C55-A result bytes")
    c55a_result = load_object(C55A_RESULT)
    close_object(c55a_result, "object_sha256", EXPECTED["C55A_RESULT_OBJECT"], "C55-A result")
    demand(bytes_hash(C55A_LEAF) == EXPECTED["C55A_LEAF_FILE"], "C55-A leaf bytes")
    demand(bytes_hash(C55B_RESULT) == EXPECTED["C55B_RESULT_FILE"], "C55-B result bytes")
    c55b = load_object(C55B_RESULT)
    close_object(c55b, "object_sha256", EXPECTED["C55B_RESULT_OBJECT"], "C55-B result")
    c35 = load_object(C35 / "result.json")
    c36 = load_object(C36 / "result.json")
    c41 = load_object(C41 / "result.json")
    close_object(c35, "object_sha256", EXPECTED["C35_OBJECT"], "C35")
    close_object(c36, "object_sha256", EXPECTED["C36_OBJECT"], "C36")
    close_object(c41, "object_sha256", EXPECTED["C41_OBJECT"], "C41")
    demand(c36["map_stage_census"]["scope"] == ATLAS_SCOPE, "C36 collar-only scope")
    head = load_object(C53_HEAD)
    close_object(head, "authority_seal_object_sha256", EXPECTED["C53_HEAD_OBJECT"], "C53 head")
    demand(head["post_seal_effective_checkpoint_object_sha256"] == EXPECTED["C53_CHECKPOINT"], "C53 checkpoint")

    c55b_cells = read_closed_ledger(OUT, c55b["ledgers"]["cell_component_crosswalk"])
    c55b_edges = read_closed_ledger(OUT, c55b["ledgers"]["component_edges_and_glue"])
    c55b_components = read_closed_ledger(OUT, c55b["ledgers"]["ordinary_components"])
    cross = {row["cell_id"]: row for row in c55b_cells}
    component = {row["component_index"]: row for row in c55b_components}
    demand(len(cross) == 1724 and len(component) == 26, "C55-B reconstructed cardinality")

    atlas = load_object(C55A_LEAF)
    demand(atlas["object_sha256"] == EXPECTED["C55A_LEAF_OBJECT"], "C55-A embedded object")
    blockers = atlas["blocker_rows"]
    demand(len(blockers) == 574, "blocker count")
    for index, blocker in enumerate(blockers):
        close_row(blocker, f"C55-A blocker:{index}")
    del atlas

    blocker_by_cell: dict[str, tuple[dict[str, Any], str]] = {}
    large_blockers: list[dict[str, Any]] = []
    for blocker in blockers:
        rep = blocker["representative_cell_id"]
        ref = blocker["reflected_cell_id"]
        if cross[rep]["component_index"] in (0, 1):
            large_blockers.append(blocker)
            demand(rep not in blocker_by_cell and ref not in blocker_by_cell, "unique blocker physical cell")
            blocker_by_cell[rep] = (blocker, "REPRESENTATIVE")
            blocker_by_cell[ref] = (blocker, "REFLECTED")
    unresolved = set(blocker_by_cell)
    demand(len(large_blockers) == 562 and len(unresolved) == 1124, "large blocker cardinality")

    occurrences = read_closed_ledger(C35, c35["ledgers"]["path_occurrences"])
    margins = read_closed_ledger(C36, c36["ledgers"]["occurrence_margin_bindings"])
    demand(len(occurrences) == len(margins) == 1648, "occurrence cardinality")
    for index, (occurrence, margin) in enumerate(zip(occurrences, margins, strict=True), start=1):
        demand(occurrence["collision_index"] == margin["collision_index"] == index, "occurrence alignment")
        for field in ("geometry_template_id", "official_word_variant_id", "incoming_absolute_owner_id", "selected_absolute_owner_id", "incoming_chart", "outgoing_chart", "destination_core_id"):
            demand(occurrence[field] == margin[field], f"occurrence projection:{index}:{field}")

    candidate_cells = read_closed_ledger(OUT, result["ledgers"]["corridor_and_separator_cells"])
    candidate_islands = read_closed_ledger(OUT, result["ledgers"]["separator_islands"])
    candidate_tasks = read_closed_ledger(OUT, result["ledgers"]["post_C53_pending_logical_tasks"])
    candidate_components = read_closed_ledger(OUT, result["ledgers"]["component_summary"])
    demand(len(candidate_cells) == 1124 and len(candidate_islands) == 22 and len(candidate_tasks) == 33319 and len(candidate_components) == 2, "candidate small-ledger census")

    # Rebuild exact induced graph and deterministic anchor BFS.
    adjacency: dict[str, list[tuple[str, dict[str, Any]]]] = defaultdict(list)
    incident: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for edge in c55b_edges:
        left, right = edge.get("left_cell_id"), edge.get("right_cell_id")
        if left is not None:
            incident[left].append(edge)
        if right is not None:
            incident[right].append(edge)
        if edge["scope"] == "ORDINARY_INTERNAL" and left in unresolved and right in unresolved:
            adjacency[left].append((right, edge))
            adjacency[right].append((left, edge))
    for cell_id in adjacency:
        adjacency[cell_id].sort(key=lambda item: (item[0], item[1]["row_sha256"]))

    anchors: dict[int, str] = {}
    parent: dict[str, tuple[str, dict[str, Any]] | None] = {}
    distance: dict[str, int] = {}
    for ci in (0, 1):
        anchor = component[ci]["known_sheet_anchor"]["anchor_cell_id"]
        anchors[ci] = anchor
        parent[anchor] = None
        distance[anchor] = 0
        queue: deque[str] = deque([anchor])
        while queue:
            current = queue.popleft()
            for neighbor, edge in adjacency.get(current, []):
                if cross[neighbor]["component_index"] == ci and neighbor not in parent:
                    parent[neighbor] = (current, edge)
                    distance[neighbor] = distance[current] + 1
                    queue.append(neighbor)
    reachable = set(parent)
    stranded = unresolved - reachable
    demand(len(reachable) == 1044 and len(stranded) == 80 and max(distance.values()) == 118, "independent BFS census")

    # Reconstruct separator components and exact cut payloads.
    expected_islands: list[dict[str, Any]] = []
    island_id_by_cell: dict[str, str] = {}
    for ci in (0, 1):
        pending = {cell for cell in stranded if cross[cell]["component_index"] == ci}
        groups: list[list[str]] = []
        while pending:
            seed = min(pending)
            found = {seed}
            queue = deque([seed])
            while queue:
                current = queue.popleft()
                for neighbor, _edge in adjacency.get(current, []):
                    if neighbor in pending and neighbor not in found:
                        found.add(neighbor)
                        queue.append(neighbor)
            pending -= found
            groups.append(sorted(found))
        groups.sort(key=lambda values: (values[0], len(values)))
        for local_index, members in enumerate(groups):
            island_id = "c56l-separator-island:" + object_hash({"component_index": ci, "member_cell_ids": members})
            member_set = set(members)
            for cell_id in members:
                island_id_by_cell[cell_id] = island_id
            boundary: dict[str, dict[str, Any]] = {}
            for cell_id in members:
                for edge in incident.get(cell_id, []):
                    left, right = edge.get("left_cell_id"), edge.get("right_cell_id")
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
                        "exact_geometry_sha256": object_hash(edge["exact_geometry"]),
                    }
            boundary_rows = [boundary[key] for key in sorted(boundary)]
            scope_census = Counter(row["scope"] for row in boundary_rows)
            disposition_census = Counter(
                value for row in boundary_rows
                for value in (row["left_disposition"], row["right_disposition"])
                if value is not None and value != "UNRESOLVED_R1648_CONTINUATION"
            )
            demand(boundary_rows and disposition_census, "nonempty exact separator cut")
            if disposition_census.get("TYPED_EVENT_GRAPH", 0):
                separator_kind = "EXACT_TYPED_EVENT_BOUNDARY__DYNAMIC_OWNER_GLUE_MISSING"
            elif any("GRAZING" in key for key in scope_census):
                separator_kind = "EXACT_GRAZING_BOUNDARY__POSITIVE_TERMINAL_DECIDER_MISSING"
            else:
                separator_kind = "FORMAL_EXCLUSION_CUT__DYNAMIC_EXTERIOR_DECIDER_MISSING"
            expected_islands.append({
                "schema": ISLAND_SCHEMA,
                "island_id": island_id,
                "component_index": ci,
                "component_local_island_index": local_index,
                "member_cell_count": len(members),
                "member_cell_ids": members,
                "member_cell_ids_sha256": object_hash(members),
                "separator_kind": separator_kind,
                "boundary_row_count": len(boundary_rows),
                "boundary_rows": boundary_rows,
                "boundary_scope_census": dict(sorted(scope_census.items())),
                "boundary_nonunresolved_disposition_census": dict(sorted(disposition_census.items())),
                "event_or_exterior_terminal_decider_present": False,
                "whole_cell_terminal_credit": 0,
                "D02_gate_credit": 0,
            })
    expected_islands.sort(key=lambda row: (row["component_index"], row["member_cell_ids"][0]))
    demand(len(expected_islands) == 22, "independent island count")
    for expected_row, actual in zip(expected_islands, candidate_islands, strict=True):
        semantic = dict(actual)
        claim = semantic.pop("row_sha256")
        demand(semantic == expected_row and object_hash(expected_row) == claim, "island exact reconstruction")
    island_row_hash = {row["island_id"]: row["row_sha256"] for row in candidate_islands}

    # Rebuild every cell corridor row exactly.
    expected_cell_order = sorted(unresolved, key=lambda value: (cross[value]["component_index"], value))
    cell_primary = Counter()
    corridor_primary = Counter()
    island_primary = Counter()
    for cell_id, actual in zip(expected_cell_order, candidate_cells, strict=True):
        blocker, role = blocker_by_cell[cell_id]
        ci = cross[cell_id]["component_index"]
        primary = blocker["primary_residual_classification"]
        cell_primary[primary] += 1
        task_hashes = blocker["residual_source_row_sha256s"]
        expected: dict[str, Any] = {
            "schema": CELL_SCHEMA,
            "cell_id": cell_id,
            "component_index": ci,
            "component_id": cross[cell_id]["component_id"],
            "reflection_role": role,
            "reflection_partner_cell_id": cross[cell_id]["reflection_partner_cell_id"],
            "pair_index": blocker["pair_index"],
            "C55B_crosswalk_row_sha256": cross[cell_id]["row_sha256"],
            "C55A_blocker_row_sha256": blocker["row_sha256"],
            "primary_residual_classification": primary,
            "post_C53_pending_logical_task_count_for_pair": len(task_hashes),
            "post_C53_pending_logical_task_row_hash_sequence_sha256": line_sequence(task_hashes),
            "anchor_cell_id": anchors[ci],
            "anchor_binding": component[ci]["known_sheet_anchor"],
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
            steps: list[dict[str, Any]] = []
            cursor = cell_id
            while parent[cursor] is not None:
                target, edge = parent[cursor]  # type: ignore[misc]
                steps.append(exact_step(edge, cursor, target))
                cursor = target
            expected.update({
                "witness_kind": "EXPLICIT_TOPOLOGICAL_CORRIDOR_TO_STRICT_OPEN_ANCHOR",
                "refinement_blocker_class": ANCHOR_BLOCKER if cell_id == cursor else CORRIDOR_BLOCKER,
                "corridor_step_count": len(steps),
                "corridor_steps": steps,
                "corridor_step_row_hash_sequence_sha256": line_sequence(step["C55B_edge_row_sha256"] for step in steps),
                "separator_island_id": None,
                "separator_island_row_sha256": None,
            })
            corridor_primary[primary] += 1
        else:
            island_id = island_id_by_cell[cell_id]
            expected.update({
                "witness_kind": "EXACT_SEPARATOR_ISLAND_BLOCKER",
                "refinement_blocker_class": ISLAND_BLOCKER,
                "corridor_step_count": None,
                "corridor_steps": None,
                "corridor_step_row_hash_sequence_sha256": None,
                "separator_island_id": island_id,
                "separator_island_row_sha256": island_row_hash[island_id],
            })
            island_primary[primary] += 1
        semantic = dict(actual)
        claim = semantic.pop("row_sha256")
        demand(semantic == expected and object_hash(expected) == claim, f"cell exact reconstruction:{cell_id}")

    # Rebind all 33,319 current logical tasks to the actual C41 ledger.
    wanted: dict[str, dict[str, Any]] = {}
    for blocker in large_blockers:
        for task_hash in blocker["residual_source_row_sha256s"]:
            demand(task_hash not in wanted, "unique pending C41 task")
            wanted[task_hash] = blocker
    demand(len(wanted) == 33319, "unique task count")
    routed_descriptor = c41["ledgers"]["routed_ambient_cells"]
    routed_path = C41 / routed_descriptor["filename"]
    demand(bytes_hash(routed_path) == routed_descriptor["sha256"], "C41 routed bytes")
    selected: dict[str, dict[str, Any]] = {}
    routed_sequence = hashlib.sha256()
    routed_count = 0
    with gzip.open(routed_path, "rt", encoding="utf-8") as source:
        for routed_count, line in enumerate(source, start=1):
            row = json.loads(line)
            close_row(row, f"C41 routed:{routed_count}")
            row_hash = row["row_sha256"]
            routed_sequence.update((row_hash + "\n").encode("ascii"))
            if row_hash in wanted:
                blocker = wanted[row_hash]
                demand(row["pair_index"] == blocker["pair_index"], "C41 pair projection")
                selected[row_hash] = {
                    "residual_classification": row["residual_classification"],
                    "path": row["path"],
                    "source_path": row["source_path"],
                    "descendant_bits": row["descendant_bits"],
                    "parent_volume_fraction": row["parent_volume_fraction"],
                    "split_axis_history": row["split_axis_history"],
                    "route_method": row["route_method"],
                    "round144_terminal_class": row["round144_terminal_class"],
                }
    demand(routed_count == routed_descriptor["row_count"], "C41 full row count")
    demand(routed_sequence.hexdigest() == routed_descriptor["row_hash_line_sequence_sha256"], "C41 full row sequence")
    demand(set(selected) == set(wanted), "all selected C41 tasks found")

    task_index = 0
    logical_primary = Counter()
    logical_residual = Counter()
    for blocker in sorted(large_blockers, key=lambda row: row["pair_index"]):
        task_hashes = blocker["residual_source_row_sha256s"]
        demand(task_hashes == sorted(task_hashes), "task order")
        for ordinal, task_hash in enumerate(task_hashes):
            actual = candidate_tasks[task_index]
            task_index += 1
            compact = selected[task_hash]
            expected = {
                "schema": TASK_SCHEMA,
                "pair_index": blocker["pair_index"],
                "pair_task_ordinal": ordinal,
                "C55A_blocker_row_sha256": blocker["row_sha256"],
                "C41_routed_ambient_row_sha256": task_hash,
                "representative_cell_id": blocker["representative_cell_id"],
                "reflected_cell_id": blocker["reflected_cell_id"],
                "primary_residual_classification": blocker["primary_residual_classification"],
                **compact,
                "post_C53_effective_checkpoint_object_sha256": EXPECTED["C53_CHECKPOINT"],
                "current_pending_logical_task": True,
                "formal_credit": 0,
                "D02_gate_credit": 0,
            }
            semantic = dict(actual)
            claim = semantic.pop("row_sha256")
            demand(semantic == expected and object_hash(expected) == claim, f"task exact reconstruction:{task_hash}")
            logical_primary[blocker["primary_residual_classification"]] += 1
            logical_residual[compact["residual_classification"]] += 1
    demand(task_index == 33319, "task audit cursor")

    # Verify all 1,852,352 refinement rows without loading them into memory.
    refinement_descriptor = result["ledgers"]["cell_occurrence_common_refinement"]
    refinement_path = OUT / refinement_descriptor["filename"]
    demand(refinement_path.stat().st_size == refinement_descriptor["size"], "refinement file size")
    demand(bytes_hash(refinement_path) == refinement_descriptor["sha256"], "refinement file hash")
    refinement_sequence = hashlib.sha256()
    refinement_count = 0
    with gzip.open(refinement_path, "rt", encoding="utf-8") as source:
        for refinement_count, line in enumerate(source, start=1):
            row = json.loads(line)
            close_row(row, f"refinement:{refinement_count}")
            refinement_sequence.update((row["row_sha256"] + "\n").encode("ascii"))
            zero = refinement_count - 1
            cell_index, occurrence_index = divmod(zero, 1648)
            cell = candidate_cells[cell_index]
            occurrence = occurrences[occurrence_index]
            margin = margins[occurrence_index]
            expected = {
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
                "refinement_blocker_class": cell["refinement_blocker_class"],
                "margin_transport_proved": False,
                "owner_transport_proved": False,
                "history_transport_proved": False,
                "strict_terminal_class": None,
                "whole_cell_terminal_credit": 0,
                "D02_gate_credit": 0,
            }
            semantic = dict(row)
            claim = semantic.pop("row_sha256")
            demand(semantic == expected and object_hash(expected) == claim, f"refinement exact row:{refinement_count}")
            if refinement_count % 250000 == 0:
                print(f"independent refinement verify {refinement_count}/1852352", flush=True)
    demand(refinement_count == 1852352, "refinement full count")
    demand(refinement_sequence.hexdigest() == refinement_descriptor["row_hash_line_sequence_sha256"], "refinement row sequence")

    # Per-primary residual accounting must be independently reproduced.
    expected_class_rows = []
    for primary in sorted(cell_primary):
        expected_class_rows.append({
            "primary_residual_classification": primary,
            "physical_cell_count": cell_primary[primary],
            "topological_corridor_cell_count": corridor_primary[primary],
            "separator_island_cell_count": island_primary[primary],
            "post_C53_pending_logical_task_count": logical_primary[primary],
            "cell_occurrence_refined_stratum_count": cell_primary[primary] * 1648,
            "formal_closed_cell_count": 0,
            "formal_remaining_cell_count": cell_primary[primary],
            "D02_gate_credit": 0,
        })
    demand(result["primary_residual_classification_accounting"] == expected_class_rows, "primary classification accounting")
    demand(result["actual_C41_residual_classification_logical_task_census"] == dict(sorted(logical_residual.items())), "actual C41 census")

    # Component summary fields that carry semantic credit and global counts.
    for row in candidate_components:
        demand(row["schema"] == COMPONENT_SCHEMA, "component schema")
        demand(row["current_unresolved_cell_count"] == 562, "component unresolved")
        demand(row["topological_corridor_cell_count"] == 522, "component corridor")
        demand(row["separator_island_cell_count"] == 40, "component separator cells")
        demand(row["separator_island_count"] == 11, "component islands")
        demand(row["maximum_corridor_step_count"] == 118, "component max distance")
        demand(row["post_C53_pending_logical_task_count"] == 33319, "shared logical task count")
        demand(row["cell_occurrence_refined_stratum_count"] == 926176, "component product")
        demand(row["edgewise_margin_owner_history_transport_complete"] is False, "component no transport")
        demand(row["formal_closed_cell_count"] == 0 and row["formal_remaining_cell_count"] == 562, "component credit")
        demand(row["whole_component_connected_to_known_credit"] == row["D02_gate_credit"] == 0, "component gate locks")

    attacks = adversarial_checks(result, candidate_cells)
    after = snapshot()
    demand(before == after, "runtime/canonical stable across audit")
    demand("cm2_round306c56l_large_component_common_refinement_v1" not in sys.modules, "producer not imported")

    verification: dict[str, Any] = {
        "schema": BASE_SCHEMA + ".independent-verification.v1",
        "status": (
            "PASS_INDEPENDENT_NO_PRODUCER_RECONSTRUCTION__1124_CELLS__22_ISLANDS__"
            "33319_TASKS__1852352_REFINEMENT_ROWS__16_OF_16_ATTACKS_FAIL_CLOSED__ZERO_CREDIT"
        ),
        "candidate_result_file_sha256": bytes_hash(RESULT),
        "candidate_result_object_sha256": result_object,
        "producer_imported": False,
        "producer_executed": False,
        "verified": {
            "large_components": 2,
            "current_unresolved_cells": 1124,
            "topological_corridor_cells": 1044,
            "separator_cells": 80,
            "separator_islands": 22,
            "maximum_corridor_steps": 118,
            "post_C53_unique_logical_tasks": 33319,
            "C35_C36_occurrences": 1648,
            "cell_occurrence_refinement_rows": 1852352,
            "formal_closed_cells": 0,
            "formal_remaining_cells": 1124,
            "D02_gate_credit": 0,
        },
        "primary_residual_classification_accounting": expected_class_rows,
        "attacks": attacks,
        "runtime_and_canonical_snapshot_before": before,
        "runtime_and_canonical_snapshot_after": after,
        "runtime_and_canonical_unchanged": True,
    }
    verification["object_sha256"] = object_hash(verification)
    VERIFICATION.write_bytes(encoded(verification) + b"\n")
    return verification


def main() -> int:
    verification = verify()
    print(json.dumps({
        "status": verification["status"],
        "object_sha256": verification["object_sha256"],
        "verified": verification["verified"],
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (Reject, OSError, ValueError, KeyError, TypeError, IndexError) as exc:
        print(f"FAIL_CLOSED:{type(exc).__name__}:{exc}", file=sys.stderr)
        raise SystemExit(2)
