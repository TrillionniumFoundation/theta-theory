#!/usr/bin/env python3
"""Read-only transitive component probe for outgoing-W local signatures.

Nodes are the 36,040 strict Round195 candidate regions plus strict
Round174/Round179 resolved anchor boxes. Edges are allowed only within one
Gate3 parent and outgoing cell, across an exact positive-two-dimensional
shared box-face patch on which whole-face HPLUS/HMINUS enclosures are both
strict with that cell's signs.

A candidate receives a local signature only when its connected component
contains at least one strict anchor and all anchor signatures in the
component agree. No point sampling, parent-wide cell extrapolation, formal
attachment, or global exact-key disposition occurs.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict, deque
from fractions import Fraction as Q
import gc
import hashlib
import json
from pathlib import Path
import sys
from typing import Any

from flint import ctx

import cm2_round198_source_g_outgoing_return_signature_probe as r198


HERE = Path(__file__).resolve().parent
SCHEMA = "cm2.round203.source-g-outgoing-signature-component-probe.v1"

ROUND198_SOURCE = (
    "cm2_round198_source_g_outgoing_return_signature_probe.py"
)
ROUND198_SOURCE_SHA256 = (
    "59dac5b6e2d79e1612dad51780174f97f71dc1223c01a21b502805d6e9510fbf"
)
ROUND198_REPORT = (
    "cm2_round198_source_g_outgoing_return_signature_spike_report.md"
)
ROUND198_REPORT_SHA256 = (
    "4c7996179638a21fdd4b8b0b15f347ca85b627e5002df20fbce58897223ff358"
)

EXPECTED_CANDIDATES = 36_040
EXPECTED_ANCHORS = 18_332
EXPECTED_LEAVES = 18_324
EXPECTED_ORIGINS = 8_268
EXPECTED_PARENTS = 912
EXPECTED_U2_LEAVES = 88
EXPECTED_U2_CANDIDATES = 176
EXPECTED_DIRECT_ANCHORED_CANDIDATES = 3_264
EXPECTED_R195_LEAF_ROWS_SHA256 = (
    "0370fb57e9d2881a8bc2d0e66351a6c551e147d483558c682f051153924f88b5"
)
EXPECTED_R195_U2_ROWS_SHA256 = (
    "12fbc70f82645ae2ad252b4e88587a7841814a03fda1972a0241cd63c45d6ee0"
)
EXPECTED_CANDIDATE_NODE_ROWS_SHA256 = (
    "4907c49e33454110fb9d53eb728761608cf773b802ddb606115f89dbbb1acd17"
)
EXPECTED_ANCHOR_NODE_ROWS_SHA256 = (
    "81c55aa424486784bc1b7b950210b4d4906fe178a8a81a498a95e3907b11b53d"
)
EXPECTED_COMPATIBLE_EDGE_ROWS_SHA256 = (
    "110be08dd6a95bc0bee306abed35d452c6f17b65897b5c9acd3edaf6bcaadf9e"
)
EXPECTED_REJECTED_FACE_ROWS_SHA256 = (
    "29b5f3dfe8987a08e9a97c6b8f5888513073638392cfd95cc71a2f4eac85b5b0"
)
EXPECTED_COMPONENT_ROWS_SHA256 = (
    "d9fb8825b8689889c35e3028bc8a275c662230b72a9f96eb7853f4fdeb2daeb7"
)
EXPECTED_GROUP_ROWS_SHA256 = (
    "01a490d5fda4caf16b4aa73a68390900722c3bc6ede75509db92684f715aeb1a"
)
EXPECTED_ASSIGNMENT_ROWS_SHA256 = (
    "d0d1fdb87da141b2c7260d266ec86415d958c7f773a1a5ccac224a3125dabc3a"
)
EXPECTED_U2_ASSIGNMENT_ROWS_SHA256 = (
    "4223bcc9a07b15969003cec3fe30ca77679ad1e36f80282aa2007b95ae09259d"
)
EXPECTED_PROBE_RESULT_SHA256 = (
    "8addc49f7e1c2661fa82525f59765627f7a2cbb322a0b3b55d4ca5c6a04341d9"
)
EXPECTED_DOCUMENT_SHA256 = (
    "7c4e34d146adb5f34637bed6eeae19719bdd477c47c235a9e57384f950f63e48"
)

CELL_SIGNS = {
    "E": ("STRICT_POSITIVE", "STRICT_POSITIVE"),
    "W": ("STRICT_NEGATIVE", "STRICT_NEGATIVE"),
    "N": ("STRICT_POSITIVE", "STRICT_NEGATIVE"),
    "S": ("STRICT_NEGATIVE", "STRICT_POSITIVE"),
}


def require(condition: bool, label: str) -> None:
    if not condition:
        raise RuntimeError(label)


def canonical(value: Any) -> str:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    )


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value).encode()).hexdigest()


def check_inputs() -> dict[str, Any]:
    r189 = r198.r195.r191.r189
    require(
        Path(r198.__file__).resolve() == (HERE / ROUND198_SOURCE).resolve(),
        "Round198 module identity",
    )
    r189.pinned_sha256(HERE / ROUND198_SOURCE, ROUND198_SOURCE_SHA256)
    r189.pinned_sha256(HERE / ROUND198_REPORT, ROUND198_REPORT_SHA256)
    require(
        r198.EXPECTED_PROBE_RESULT_SHA256
        == "b6f1660dfe18613ac2b3443c68f56a05f9399d3715c4e7f301fdc0482be459d5"
        and r198.EXPECTED_DOCUMENT_SHA256
        == "5d3ddddd6445bc364f7b4febd5f81adcb311d085bce636f9ec74c7a54d3711ee",
        "Round198 embedded final result pins",
    )
    upstream = r198.check_inputs()
    return {
        **upstream,
        "Round198_probe_source_sha256": ROUND198_SOURCE_SHA256,
        "Round198_probe_report_sha256": ROUND198_REPORT_SHA256,
        "Round198_probe_result_sha256":
            r198.EXPECTED_PROBE_RESULT_SHA256,
        "Round198_probe_document_sha256":
            r198.EXPECTED_DOCUMENT_SHA256,
        "probe_only_import_before_pin_boundary": True,
    }


def local_signature(
    base: dict[str, Any],
    cell: str,
) -> dict[str, Any]:
    return {
        **base,
        "outgoing_cell": cell,
        "target_chart":
            f"{base['target_lift'].split('[', 1)[0]}:{cell}",
    }


def reconstruct_nodes() -> tuple[
    list[dict[str, Any]],
    list[dict[str, Any]],
    dict[str, dict[str, Any]],
    set[str],
    dict[str, Any],
]:
    """Rebuild candidate and anchor nodes without using Round198 assignments."""

    outgoing, collar_by_occurrence, source = (
        r198.r195.r191.r189.load_scope()
    )
    del source
    gc.collect()
    require(len(outgoing) == EXPECTED_LEAVES, "outgoing leaf census")
    relevant_parents = {
        collar_by_occurrence[row["occurrence_row_id"]]["parent_id"]
        for row in outgoing
    }
    relevant_occurrences = {row["occurrence_row_id"] for row in outgoing}
    relevant_origins = {
        collar_by_occurrence[row["occurrence_row_id"]]["origin_row_id"]
        for row in outgoing
    }
    require(
        len(relevant_parents) == EXPECTED_PARENTS
        and len(relevant_origins) == EXPECTED_ORIGINS,
        "parent/origin census",
    )
    (
        bases,
        parent_meta,
        parent_anchor_rows,
        anchor_aux,
    ) = r198.load_anchor_ledger(
        relevant_parents,
        relevant_occurrences,
    )
    require(
        len(bases) == EXPECTED_PARENTS
        and anchor_aux["diagnostics"][
            "parent_base_signature_conflict_count"
        ] == 0
        and anchor_aux["diagnostics"][
            "parent_base_signature_missing_count"
        ] == 0,
        "unique parent base signatures",
    )

    context_by_parent = {
        parent_id: {
            "chart": meta["chart"],
            "owner_target": meta["owner_target"],
        }
        for parent_id, meta in parent_meta.items()
    }
    candidate_nodes: list[dict[str, Any]] = []
    leaf_rows: list[dict[str, Any]] = []
    u2_audit_rows: list[dict[str, Any]] = []
    u2_leaf_ids: set[str] = set()
    r195 = r198.r195
    r186 = r195.r191.r189.r188.r186
    for index, raw in enumerate(outgoing, 1):
        collar = collar_by_occurrence[raw["occurrence_row_id"]]
        parent_id = collar["parent_id"]
        require(
            context_by_parent[parent_id]
            == {
                "chart": collar["chart"],
                "owner_target": collar["owner_target"],
            },
            f"parent geometry context:{parent_id}",
        )
        box = r186.r179.r174.atlas.AtlasBox(
            *(Q(value) for value in raw["box"]),
            0,
            raw["row_id"],
        )
        final_faces: dict[str, dict[str, Any]] = {}
        for side, upper, encoded in (
            ("LOWER", False, raw["lower_t_face_status"]),
            ("UPPER", True, raw["upper_t_face_status"]),
        ):
            if encoded == "U":
                final_faces[side] = r195.final_unresolved_face(
                    raw,
                    collar,
                    box,
                    side,
                    upper,
                )
        lower = (
            r195.side_summary(final_faces["LOWER"])
            if "LOWER" in final_faces
            else r195.decode_round182_face(raw["lower_t_face_status"])
        )
        upper = (
            r195.side_summary(final_faces["UPPER"])
            if "UPPER" in final_faces
            else r195.decode_round182_face(raw["upper_t_face_status"])
        )
        leaf = r195.classify_leaf(raw, collar, box, lower, upper)
        leaf_rows.append(leaf)
        is_u2 = (
            raw["lower_t_face_status"] == "U"
            and raw["upper_t_face_status"] == "U"
        )
        if is_u2:
            u2_leaf_ids.add(raw["row_id"])
            u2_audit_rows.append(r195.audit_u2_leaf(
                leaf,
                raw,
                collar,
                box,
                final_faces["LOWER"],
                final_faces["UPPER"],
            ))

        # Passing no base and no anchors makes the Round198 helper derive
        # only strict region factor signs/cells; it cannot assign a signature.
        region_rows = r198.factor_region_rows(
            leaf,
            raw,
            collar,
            box,
            list(final_faces.values()),
            None,
            set(),
            {},
            None,
        )
        for region in region_rows:
            require(
                region["local_return_signature"] is None
                and region["single_point_evaluation_used"] is False,
                f"unsigned candidate reconstruction:{region['candidate_region_id']}",
            )
            candidate_nodes.append({
                "node_id": "candidate:" + region["candidate_region_id"],
                "node_kind": "CANDIDATE_REGION",
                "candidate_region_id": region["candidate_region_id"],
                "leaf_row_id": region["leaf_row_id"],
                "origin_row_id": region["origin_row_id"],
                "occurrence_row_id": region["occurrence_row_id"],
                "parent_id": parent_id,
                "cell": region["outgoing_cell"],
                "F_sign": region["F_sign"],
                "HPLUS_sign": region["HPLUS_sign"],
                "HMINUS_sign": region["HMINUS_sign"],
                "leaf_classification": region["leaf_classification"],
                "box": raw["box"],
            })
        if index % 2000 == 0 or index == len(outgoing):
            print(
                f"component-nodes {index}/{len(outgoing)}",
                file=sys.stderr,
                flush=True,
            )

    leaf_rows.sort(key=lambda row: row["leaf_row_id"])
    u2_audit_rows.sort(key=lambda row: row["leaf_row_id"])
    candidate_nodes.sort(key=lambda row: row["node_id"])
    require(
        len(candidate_nodes) == EXPECTED_CANDIDATES,
        "candidate node census",
    )
    require(
        digest(candidate_nodes) == EXPECTED_CANDIDATE_NODE_ROWS_SHA256,
        "candidate node row digest pin",
    )
    require(
        digest(leaf_rows) == EXPECTED_R195_LEAF_ROWS_SHA256,
        "Round195 leaf reconstruction pin",
    )
    require(
        len(u2_audit_rows) == EXPECTED_U2_LEAVES
        and digest(u2_audit_rows) == EXPECTED_R195_U2_ROWS_SHA256,
        "Round195 U|U reconstruction pin",
    )

    anchor_nodes: list[dict[str, Any]] = []
    for parent_id in sorted(relevant_parents):
        base = bases[parent_id]
        for cell, rows in sorted(
            anchor_aux["anchor_geometry"].get(parent_id, {}).items()
        ):
            require(cell in CELL_SIGNS, f"anchor cell:{cell}")
            signature = local_signature(base, cell)
            for row in rows:
                anchor_nodes.append({
                    "node_id": "anchor:" + row["row_id"],
                    "node_kind": "STRICT_RESOLVED_ANCHOR",
                    "anchor_source": row["source"],
                    "anchor_row_id": row["row_id"],
                    "parent_id": parent_id,
                    "cell": cell,
                    "HPLUS_sign": CELL_SIGNS[cell][0],
                    "HMINUS_sign": CELL_SIGNS[cell][1],
                    "box": row["box"],
                    "local_return_signature": signature,
                    "local_return_signature_sha256": digest(signature),
                })
    anchor_nodes.sort(key=lambda row: row["node_id"])
    require(
        len(anchor_nodes)
        == anchor_aux["diagnostics"]["strict_anchor_geometry_row_count"]
        == EXPECTED_ANCHORS,
        "anchor node census",
    )
    require(
        digest(anchor_nodes) == EXPECTED_ANCHOR_NODE_ROWS_SHA256,
        "anchor node row digest pin",
    )
    require(
        len({row["node_id"] for row in candidate_nodes + anchor_nodes})
        == EXPECTED_CANDIDATES + EXPECTED_ANCHORS,
        "globally unique node identifiers",
    )
    metadata = {
        "bases": bases,
        "parent_anchor_rows": parent_anchor_rows,
        "anchor_diagnostics": anchor_aux["diagnostics"],
        "carried_form_count": len(anchor_aux["carried_forms"]),
        "leaf_rows_sha256": digest(leaf_rows),
        "u2_audit_rows_sha256": digest(u2_audit_rows),
    }
    return (
        candidate_nodes,
        anchor_nodes,
        context_by_parent,
        u2_leaf_ids,
        metadata,
    )


class UnionFind:
    def __init__(self, size: int) -> None:
        self.parent = list(range(size))
        self.rank = [0] * size

    def find(self, value: int) -> int:
        while self.parent[value] != value:
            self.parent[value] = self.parent[self.parent[value]]
            value = self.parent[value]
        return value

    def union(self, left: int, right: int) -> None:
        left_root = self.find(left)
        right_root = self.find(right)
        if left_root == right_root:
            return
        if self.rank[left_root] < self.rank[right_root]:
            left_root, right_root = right_root, left_root
        self.parent[right_root] = left_root
        if self.rank[left_root] == self.rank[right_root]:
            self.rank[left_root] += 1


def build_graph(
    candidate_nodes: list[dict[str, Any]],
    anchor_nodes: list[dict[str, Any]],
    context_by_parent: dict[str, dict[str, Any]],
) -> tuple[
    list[dict[str, Any]],
    list[dict[str, Any]],
    list[dict[str, Any]],
    dict[str, Any],
]:
    nodes = sorted(
        candidate_nodes + anchor_nodes,
        key=lambda row: row["node_id"],
    )
    index_by_id = {
        node["node_id"]: index
        for index, node in enumerate(nodes)
    }
    require(
        len(index_by_id) == len(nodes),
        "node index uniqueness",
    )

    face_buckets: dict[
        tuple[str, str, int, str],
        dict[str, list[int]],
    ] = defaultdict(lambda: {"LOWER": [], "UPPER": []})
    for index, node in enumerate(nodes):
        box = [Q(value) for value in node["box"]]
        require(
            box[0] < box[1]
            and box[2] < box[3]
            and box[4] < box[5],
            f"positive node box:{node['node_id']}",
        )
        for axis in range(3):
            face_buckets[(
                node["parent_id"],
                node["cell"],
                axis,
                str(box[2 * axis]),
            )]["LOWER"].append(index)
            face_buckets[(
                node["parent_id"],
                node["cell"],
                axis,
                str(box[2 * axis + 1]),
            )]["UPPER"].append(index)

    union_find = UnionFind(len(nodes))
    edge_rows: list[dict[str, Any]] = []
    rejected_face_rows: list[dict[str, Any]] = []
    seen_pairs: set[tuple[str, str]] = set()
    adjacency: list[list[int]] = [[] for _ in nodes]
    direct_candidate_ids: set[str] = set()
    bucket_items = sorted(face_buckets.items())
    for bucket_index, (bucket_key, sides) in enumerate(bucket_items, 1):
        parent_id, cell, axis, coordinate = bucket_key
        for upper_index in sorted(
            sides["UPPER"],
            key=lambda value: nodes[value]["node_id"],
        ):
            for lower_index in sorted(
                sides["LOWER"],
                key=lambda value: nodes[value]["node_id"],
            ):
                if upper_index == lower_index:
                    continue
                left = nodes[upper_index]
                right = nodes[lower_index]
                pair = tuple(sorted((left["node_id"], right["node_id"])))
                if pair in seen_pairs:
                    continue
                face = r198.positive_two_dimensional_face_intersection(
                    left["box"],
                    right["box"],
                )
                if face is None:
                    continue
                require(
                    face["axis"] == ("t", "p", "s")[axis],
                    f"face bucket axis:{pair}",
                )
                seen_pairs.add(pair)
                hplus_sign, hminus_sign = CELL_SIGNS[cell]
                proof = r198.compatible_strict_cell_patch(
                    context_by_parent[parent_id],
                    face,
                    hplus_sign,
                    hminus_sign,
                    "round203-edge:" + digest(pair),
                )
                kind_pair = "|".join(sorted((
                    left["node_kind"],
                    right["node_kind"],
                )))
                row = {
                    "edge_id": "round203-edge:" + digest([
                        parent_id,
                        cell,
                        pair,
                        face,
                    ]),
                    "parent_id": parent_id,
                    "cell": cell,
                    "left_node_id": pair[0],
                    "right_node_id": pair[1],
                    "node_kind_pair": kind_pair,
                    "shared_face_axis": face["axis"],
                    "shared_face_coordinate": coordinate,
                    "shared_face_proof": proof,
                }
                if not proof[
                    "compatible_nonempty_relative_open_cell_patch"
                ]:
                    rejected_face_rows.append({
                        **row,
                        "status":
                            "BOX_FACE_WITHOUT_COMPATIBLE_STRICT_CELL_PATCH",
                    })
                    continue
                edge_rows.append({
                    **row,
                    "status":
                        "EXACT_COMPATIBLE_POSITIVE_2D_SHARED_PATCH_EDGE",
                })
                union_find.union(upper_index, lower_index)
                adjacency[upper_index].append(lower_index)
                adjacency[lower_index].append(upper_index)
                if (
                    left["node_kind"] == "CANDIDATE_REGION"
                    and right["node_kind"] == "STRICT_RESOLVED_ANCHOR"
                ):
                    direct_candidate_ids.add(left["node_id"])
                elif (
                    right["node_kind"] == "CANDIDATE_REGION"
                    and left["node_kind"] == "STRICT_RESOLVED_ANCHOR"
                ):
                    direct_candidate_ids.add(right["node_id"])
        if bucket_index % 5000 == 0 or bucket_index == len(bucket_items):
            print(
                f"component-edges {bucket_index}/{len(bucket_items)}",
                file=sys.stderr,
                flush=True,
            )

    edge_rows.sort(key=lambda row: row["edge_id"])
    rejected_face_rows.sort(key=lambda row: row["edge_id"])
    require(
        len({row["edge_id"] for row in edge_rows})
        == len(edge_rows),
        "edge identifier uniqueness",
    )
    require(
        len(direct_candidate_ids) == EXPECTED_DIRECT_ANCHORED_CANDIDATES,
        "Round198 direct anchored candidate pin",
    )
    require(
        len(edge_rows) == 39_200
        and digest(edge_rows) == EXPECTED_COMPATIBLE_EDGE_ROWS_SHA256
        and len(rejected_face_rows) == 32_576
        and digest(rejected_face_rows)
        == EXPECTED_REJECTED_FACE_ROWS_SHA256,
        "frozen compatible/rejected face ledger",
    )

    member_indices: dict[int, list[int]] = defaultdict(list)
    for index in range(len(nodes)):
        member_indices[union_find.find(index)].append(index)
    edge_count_by_root: Counter[int] = Counter()
    for row in edge_rows:
        root = union_find.find(index_by_id[row["left_node_id"]])
        require(
            root
            == union_find.find(index_by_id[row["right_node_id"]]),
            f"edge component:{row['edge_id']}",
        )
        edge_count_by_root[root] += 1

    component_rows: list[dict[str, Any]] = []
    component_by_node_id: dict[str, dict[str, Any]] = {}
    hop_by_node_id: dict[str, int] = {}
    for root, indices in sorted(
        member_indices.items(),
        key=lambda item: min(nodes[index]["node_id"] for index in item[1]),
    ):
        members = sorted(
            (nodes[index] for index in indices),
            key=lambda row: row["node_id"],
        )
        parents = {row["parent_id"] for row in members}
        cells = {row["cell"] for row in members}
        require(
            len(parents) == len(cells) == 1,
            "component parent/cell isolation",
        )
        parent_id = next(iter(parents))
        cell = next(iter(cells))
        candidates = [
            row for row in members
            if row["node_kind"] == "CANDIDATE_REGION"
        ]
        anchors = [
            row for row in members
            if row["node_kind"] == "STRICT_RESOLVED_ANCHOR"
        ]
        anchor_signature_digests = sorted({
            row["local_return_signature_sha256"]
            for row in anchors
        })
        if not anchors:
            status = "UNANCHORED_TRANSITIVE_COMPONENT_RESIDUAL"
            signature = None
        elif len(anchor_signature_digests) != 1:
            status = "CONFLICTING_ANCHOR_SIGNATURE_COMPONENT_RESIDUAL"
            signature = None
        else:
            status = "UNIQUE_ANCHORED_TRANSITIVE_COMPONENT"
            signature = anchors[0]["local_return_signature"]
            require(
                digest(signature) == anchor_signature_digests[0],
                "component signature digest",
            )
            queue: deque[int] = deque(
                index_by_id[row["node_id"]] for row in anchors
            )
            distances = {
                index_by_id[row["node_id"]]: 0 for row in anchors
            }
            while queue:
                current = queue.popleft()
                for neighbor in adjacency[current]:
                    if neighbor in distances:
                        continue
                    distances[neighbor] = distances[current] + 1
                    queue.append(neighbor)
            require(
                set(distances) == set(indices),
                "anchored component BFS coverage",
            )
            for index, distance in distances.items():
                hop_by_node_id[nodes[index]["node_id"]] = distance

        node_ids = [row["node_id"] for row in members]
        component_id = "round203-component:" + digest([
            parent_id,
            cell,
            node_ids,
        ])
        component = {
            "component_id": component_id,
            "parent_id": parent_id,
            "cell": cell,
            "status": status,
            "node_count": len(members),
            "candidate_region_count": len(candidates),
            "strict_anchor_count": len(anchors),
            "edge_count": edge_count_by_root[root],
            "node_ids_sha256": digest(node_ids),
            "candidate_region_ids_sha256": digest(sorted(
                row["candidate_region_id"] for row in candidates
            )),
            "anchor_row_ids_sha256": digest(sorted(
                row["anchor_row_id"] for row in anchors
            )),
            "anchor_source_count": dict(sorted(Counter(
                row["anchor_source"] for row in anchors
            ).items())),
            "anchor_signature_count":
                len(anchor_signature_digests),
            "anchor_signature_digests_sha256":
                digest(anchor_signature_digests),
            "assigned_local_return_signature": signature,
            "single_point_evaluation_used": False,
            "global_exact_key_disposition_credit": 0,
        }
        component_rows.append(component)
        for row in members:
            component_by_node_id[row["node_id"]] = component

    component_rows.sort(key=lambda row: row["component_id"])
    require(
        len(component_by_node_id) == len(nodes)
        and sum(row["node_count"] for row in component_rows) == len(nodes)
        and sum(
            row["candidate_region_count"] for row in component_rows
        ) == EXPECTED_CANDIDATES
        and sum(row["strict_anchor_count"] for row in component_rows)
        == EXPECTED_ANCHORS
        and sum(row["edge_count"] for row in component_rows)
        == len(edge_rows),
        "component node/edge conservation",
    )
    require(
        len(component_rows) == 34_008
        and digest(component_rows) == EXPECTED_COMPONENT_ROWS_SHA256
        and Counter(row["status"] for row in component_rows)
        == {
            "UNANCHORED_TRANSITIVE_COMPONENT_RESIDUAL": 32_776,
            "UNIQUE_ANCHORED_TRANSITIVE_COMPONENT": 1_232,
        },
        "frozen component ledger",
    )

    assignment_rows: list[dict[str, Any]] = []
    for node in candidate_nodes:
        component = component_by_node_id[node["node_id"]]
        signature = component["assigned_local_return_signature"]
        hop = hop_by_node_id.get(node["node_id"])
        require(
            (signature is None and hop is None)
            or (signature is not None and hop is not None and hop >= 1),
            f"candidate propagation distance:{node['node_id']}",
        )
        assignment_rows.append({
            "candidate_region_id": node["candidate_region_id"],
            "leaf_row_id": node["leaf_row_id"],
            "origin_row_id": node["origin_row_id"],
            "parent_id": node["parent_id"],
            "cell": node["cell"],
            "component_id": component["component_id"],
            "component_status": component["status"],
            "direct_anchor_edge": node["node_id"] in direct_candidate_ids,
            "minimum_compatible_edge_hops_from_anchor": hop,
            "assignment_status": (
                "UNIQUE_TRANSITIVELY_PROPAGATED_LOCAL_SIGNATURE"
                if signature is not None
                else component["status"]
            ),
            "local_return_signature": signature,
            "single_point_evaluation_used": False,
            "formal_signature_row_materialized": False,
            "global_exact_key_disposition_credit": 0,
        })
    assignment_rows.sort(key=lambda row: row["candidate_region_id"])
    require(
        digest(assignment_rows) == EXPECTED_ASSIGNMENT_ROWS_SHA256,
        "candidate assignment row digest pin",
    )
    return (
        edge_rows,
        rejected_face_rows,
        component_rows,
        {
            "nodes": nodes,
            "assignment_rows": assignment_rows,
            "direct_candidate_ids": direct_candidate_ids,
        },
    )


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Read-only Round203 compatible shared-face component probe; "
            "no output path and zero global credit."
        )
    )
    parser.parse_args()
    ctx.prec = 256
    pins = check_inputs()
    (
        candidate_nodes,
        anchor_nodes,
        context_by_parent,
        u2_leaf_ids,
        node_metadata,
    ) = reconstruct_nodes()
    (
        edge_rows,
        rejected_face_rows,
        component_rows,
        graph_aux,
    ) = build_graph(
        candidate_nodes,
        anchor_nodes,
        context_by_parent,
    )
    assignment_rows = graph_aux["assignment_rows"]
    assigned_rows = [
        row for row in assignment_rows
        if row["local_return_signature"] is not None
    ]
    residual_rows = [
        row for row in assignment_rows
        if row["local_return_signature"] is None
    ]
    require(
        len(assigned_rows) + len(residual_rows) == EXPECTED_CANDIDATES,
        "assignment conservation",
    )

    assignment_status_counts = Counter(
        row["assignment_status"] for row in assignment_rows
    )
    component_status_counts = Counter(
        row["status"] for row in component_rows
    )
    hop_counts = Counter(
        row["minimum_compatible_edge_hops_from_anchor"]
        for row in assigned_rows
    )
    direct_count = sum(
        row["direct_anchor_edge"] for row in assignment_rows
    )
    require(
        direct_count == EXPECTED_DIRECT_ANCHORED_CANDIDATES
        and hop_counts[1] == EXPECTED_DIRECT_ANCHORED_CANDIDATES,
        "direct/hop-one Round198 pin",
    )
    edge_kind_counts = Counter(
        row["node_kind_pair"] for row in edge_rows
    )
    edge_axis_counts = Counter(
        row["shared_face_axis"] for row in edge_rows
    )
    involved_origins = {
        row["origin_row_id"] for row in assignment_rows
    }
    assigned_origins = {
        row["origin_row_id"] for row in assigned_rows
    }
    residual_origins = {
        row["origin_row_id"] for row in residual_rows
    }
    assigned_leaves = {row["leaf_row_id"] for row in assigned_rows}
    residual_leaves = {row["leaf_row_id"] for row in residual_rows}
    assigned_parents = {row["parent_id"] for row in assigned_rows}
    residual_parents = {row["parent_id"] for row in residual_rows}
    require(len(involved_origins) == EXPECTED_ORIGINS, "origin coverage")

    assigned_signatures = [
        row["local_return_signature"] for row in assigned_rows
    ]
    assigned_key_ids = sorted({
        signature["official_key_id"]
        for signature in assigned_signatures
    })
    assigned_key_ordinals = sorted({
        signature["official_key_ordinal"]
        for signature in assigned_signatures
    })
    require(
        len(assigned_key_ids) == len(assigned_key_ordinals),
        "assigned key ordinal/id bijection",
    )

    u2_rows = [
        row for row in assignment_rows
        if row["leaf_row_id"] in u2_leaf_ids
    ]
    require(
        len(u2_rows) == EXPECTED_U2_CANDIDATES,
        "U|U candidate census",
    )
    u2_status_counts = Counter(
        row["assignment_status"] for row in u2_rows
    )
    u2_leaf_assignment_counts = Counter(
        row["leaf_row_id"] for row in u2_rows
        if row["local_return_signature"] is not None
    )
    u2_leaf_glue_counts = Counter(
        (
            "BOTH_REGIONS_ASSIGNED"
            if u2_leaf_assignment_counts[leaf_id] == 2
            else "ONE_REGION_ASSIGNED"
            if u2_leaf_assignment_counts[leaf_id] == 1
            else "NO_REGION_ASSIGNED"
        )
        for leaf_id in u2_leaf_ids
    )
    require(
        digest(u2_rows) == EXPECTED_U2_ASSIGNMENT_ROWS_SHA256
        and not u2_leaf_assignment_counts
        and u2_leaf_glue_counts == {"NO_REGION_ASSIGNED": 88},
        "frozen U|U component assignment ledger",
    )

    group_rows: list[dict[str, Any]] = []
    components_by_group: dict[
        tuple[str, str], list[dict[str, Any]]
    ] = defaultdict(list)
    for component in component_rows:
        components_by_group[(
            component["parent_id"],
            component["cell"],
        )].append(component)
    candidates_by_group = Counter(
        (row["parent_id"], row["cell"]) for row in candidate_nodes
    )
    anchors_by_group = Counter(
        (row["parent_id"], row["cell"]) for row in anchor_nodes
    )
    assigned_by_group = Counter(
        (row["parent_id"], row["cell"]) for row in assigned_rows
    )
    residual_by_group = Counter(
        (row["parent_id"], row["cell"]) for row in residual_rows
    )
    for group in sorted(
        set(candidates_by_group) | set(anchors_by_group)
    ):
        parent_id, cell = group
        components = components_by_group[group]
        group_rows.append({
            "parent_id": parent_id,
            "cell": cell,
            "candidate_region_count": candidates_by_group[group],
            "strict_anchor_count": anchors_by_group[group],
            "component_count": len(components),
            "component_ids_sha256": digest(sorted(
                row["component_id"] for row in components
            )),
            "component_status_count": dict(sorted(Counter(
                row["status"] for row in components
            ).items())),
            "assigned_candidate_region_count": assigned_by_group[group],
            "residual_candidate_region_count": residual_by_group[group],
            "candidate_conservation": (
                assigned_by_group[group] + residual_by_group[group]
                == candidates_by_group[group]
            ),
        })
    require(
        all(row["candidate_conservation"] for row in group_rows)
        and sum(row["candidate_region_count"] for row in group_rows)
        == EXPECTED_CANDIDATES
        and sum(row["strict_anchor_count"] for row in group_rows)
        == EXPECTED_ANCHORS,
        "parent/cell group conservation",
    )
    require(
        digest(group_rows) == EXPECTED_GROUP_ROWS_SHA256,
        "parent/cell group row digest pin",
    )
    require(
        len(assigned_rows) == EXPECTED_DIRECT_ANCHORED_CANDIDATES
        and len(residual_rows) == 32_776
        and hop_counts == {1: EXPECTED_DIRECT_ANCHORED_CANDIDATES},
        "zero transitive gain pin",
    )

    verdict = (
        "VALIDATED"
        if (
            len(assigned_rows) == EXPECTED_CANDIDATES
            and not residual_rows
            and component_status_counts.get(
                "CONFLICTING_ANCHOR_SIGNATURE_COMPONENT_RESIDUAL",
                0,
            ) == 0
        )
        else "PARTIAL"
    )
    probe_result = {
        "status":
            "READ_ONLY_ZERO_PROMOTION_SOURCE_G_OUTGOING_SIGNATURE_"
            "TRANSITIVE_COMPONENT_PROBE",
        "question":
            "Do strict compatible positive-2D shared-face components "
            "propagate unique local return signatures from real resolved "
            "anchors to all 36,040 outgoing-W candidate regions?",
        "verdict": verdict,
        "verdict_scope":
            "local outgoing-W component signature feasibility only; no "
            "formal rows and no global exact-key fibre disposition",
        "input_chain": pins,
        "node_ledger": {
            "candidate_region_node_count": len(candidate_nodes),
            "strict_anchor_node_count": len(anchor_nodes),
            "total_node_count":
                len(candidate_nodes) + len(anchor_nodes),
            "candidate_node_rows_sha256": digest(candidate_nodes),
            "anchor_node_rows_sha256": digest(anchor_nodes),
            "Round195_leaf_rows_sha256":
                node_metadata["leaf_rows_sha256"],
            "Round195_U_pipe_U_rows_sha256":
                node_metadata["u2_audit_rows_sha256"],
            "parent_count": len(context_by_parent),
            "origin_count": len(involved_origins),
            "anchor_source_count": dict(sorted(Counter(
                row["anchor_source"] for row in anchor_nodes
            ).items())),
            "single_point_evaluation_used": False,
        },
        "strict_component_graph": {
            "allowed_edge_definition":
                "same parent and outgoing cell; exact positive-2D shared "
                "box-face patch; full-face HPLUS/HMINUS enclosures both "
                "strict with cell signs",
            "compatible_edge_count": len(edge_rows),
            "compatible_edge_rows_sha256": digest(edge_rows),
            "edge_node_kind_pair_count":
                dict(sorted(edge_kind_counts.items())),
            "edge_shared_face_axis_count":
                dict(sorted(edge_axis_counts.items())),
            "box_face_without_compatible_strict_patch_count":
                len(rejected_face_rows),
            "rejected_face_rows_sha256": digest(rejected_face_rows),
            "component_count": len(component_rows),
            "component_status_count":
                dict(sorted(component_status_counts.items())),
            "component_rows_sha256": digest(component_rows),
            "parent_cell_group_count": len(group_rows),
            "parent_cell_group_rows_sha256": digest(group_rows),
            "node_conservation": (
                sum(row["node_count"] for row in component_rows)
                == len(candidate_nodes) + len(anchor_nodes)
            ),
            "candidate_conservation": (
                sum(
                    row["candidate_region_count"]
                    for row in component_rows
                )
                == EXPECTED_CANDIDATES
            ),
            "anchor_conservation": (
                sum(row["strict_anchor_count"] for row in component_rows)
                == EXPECTED_ANCHORS
            ),
            "edge_conservation": (
                sum(row["edge_count"] for row in component_rows)
                == len(edge_rows)
            ),
        },
        "transitive_signature_assignment": {
            "candidate_region_count": len(assignment_rows),
            "assigned_candidate_region_count": len(assigned_rows),
            "residual_candidate_region_count": len(residual_rows),
            "direct_anchor_edge_candidate_count": direct_count,
            "newly_assigned_by_two_or_more_hops_count": sum(
                count for hop, count in hop_counts.items() if hop >= 2
            ),
            "minimum_hop_count":
                dict(sorted(
                    (str(hop), count)
                    for hop, count in hop_counts.items()
                )),
            "maximum_minimum_hop":
                max(hop_counts, default=None),
            "assignment_status_count":
                dict(sorted(assignment_status_counts.items())),
            "assignment_rows_sha256": digest(assignment_rows),
            "assigned_leaf_count": len(assigned_leaves),
            "residual_leaf_count": len(residual_leaves),
            "assigned_origin_count": len(assigned_origins),
            "residual_origin_count": len(residual_origins),
            "assigned_parent_count": len(assigned_parents),
            "residual_parent_count": len(residual_parents),
            "assigned_exact_key_count": len(assigned_key_ids),
            "assigned_exact_key_ids_sha256": digest(assigned_key_ids),
            "assigned_exact_key_ordinals_sha256":
                digest(assigned_key_ordinals),
            "anchor_signature_conflict_count":
                component_status_counts.get(
                    "CONFLICTING_ANCHOR_SIGNATURE_COMPONENT_RESIDUAL",
                    0,
                ),
            "parent_wide_or_single_point_guess_count": 0,
            "formal_signature_rows_materialized": False,
        },
        "U_pipe_U_component_glue": {
            "U_pipe_U_leaf_count": len(u2_leaf_ids),
            "candidate_region_count": len(u2_rows),
            "assignment_status_count":
                dict(sorted(u2_status_counts.items())),
            "leaf_glue_status_count":
                dict(sorted(u2_leaf_glue_counts.items())),
            "assignment_rows_sha256": digest(u2_rows),
            "Round195_cross_t_ordering_rebuilt": True,
            "component_edges_do_not_cross_outgoing_cells": True,
        },
        "remaining_global_fibre_join_gap": {
            "local_outgoing_W_component_signature_feasibility_complete":
                verdict == "VALIDATED",
            "local_signature_residual_candidate_region_count":
                len(residual_rows),
            "separate_wall_G_residual_leaf_count": 64,
            "wall_G_signatures_processed_here": False,
            "formal_signature_attachment_emitted": False,
            "half_open_boundary_ownership_materialized": False,
            "global_source_G_exact_key_fibre_count": 224580,
            "global_fibre_occurrence_join_and_deduplication_performed":
                False,
            "fibre_wide_all_occurrences_covered_or_excluded": False,
            "required_next": (
                "materialize additional strict compatible anchors for every "
                "unanchored component if any remain; then formalize local "
                "signature rows, close the 64 wall-G leaves, and perform "
                "the complete half-open global exact-key fibre join"
            ),
        },
        "zero_promotion_contract": {
            "probe_only": True,
            "runtime_filesystem_writes": 0,
            "output_path_option_exists": False,
            "component_assignment_is_not_global_disposition": True,
            "official_source_G_global_disposition_count": 0,
            "official_source_G_global_disposition_denominator": 224580,
            "D02": "UNCHANGED_BLOCKED",
            "global_Gate5_fields": "UNCHANGED_10/18",
            "CM2": "UNCHANGED_NO_GO",
        },
    }
    probe_result_sha256 = digest(probe_result)
    require(
        probe_result_sha256 == EXPECTED_PROBE_RESULT_SHA256,
        "probe result digest pin",
    )
    document = {
        "schema": SCHEMA,
        "probe_result": probe_result,
        "probe_result_sha256": probe_result_sha256,
    }
    output = (
        json.dumps(
            document,
            sort_keys=True,
            indent=2,
            ensure_ascii=False,
            allow_nan=False,
        )
        + "\n"
    )
    require(
        hashlib.sha256(output.encode()).hexdigest()
        == EXPECTED_DOCUMENT_SHA256,
        "probe JSON byte digest pin",
    )
    sys.stdout.write(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
