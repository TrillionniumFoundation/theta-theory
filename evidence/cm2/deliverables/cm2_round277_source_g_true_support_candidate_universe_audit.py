#!/usr/bin/env python3
"""Zero-credit audit of Round276/277 face candidates on frozen atom supports.

Round276 used the whole Round182 leaf box for every canonical
``(leaf, complete-signature)`` node.  That is the correct frozen rectangular
support envelope except for the twelve Round271 OUTGOING-W rows, which carry
their own ``t_child_box``.  This audit rebuilds the universe after:

* grouping source rows into canonical nodes;
* taking each node's union of its frozen support boxes;
* merging the two artificial W-tail children for the four proven aliases; and
* enumerating positive common faces with explicit negative/positive side
  orientation (never inferred from the lexical order of endpoint IDs).

The output is an audit census only and grants no occurrence or component
credit.
"""
from __future__ import annotations

import collections
import json
from fractions import Fraction as Q

import cm2_round276_source_g_collar_region_face_binding_probe as P


def qtext(value: Q) -> str:
    return str(value)


def box_tuple(values: list[str] | tuple[str, ...]) -> tuple[Q, ...]:
    box = tuple(Q(value) for value in values)
    assert len(box) == 6
    assert all(box[2 * axis] < box[2 * axis + 1] for axis in range(3))
    return box


def merge_boxes(boxes: list[tuple[Q, ...]]) -> list[tuple[Q, ...]]:
    """Return a deterministic rectangular union normalization.

    Boxes are merged only when they have identical spans in two axes and are
    exactly adjacent in the third.  This is sufficient for the four Round271
    artificial t splits and cannot enlarge the union.
    """

    work = sorted(set(boxes))
    changed = True
    while changed:
        changed = False
        for i, left in enumerate(work):
            for j in range(i + 1, len(work)):
                right = work[j]
                for axis in range(3):
                    if any(
                        left[2 * other : 2 * other + 2]
                        != right[2 * other : 2 * other + 2]
                        for other in range(3)
                        if other != axis
                    ):
                        continue
                    if left[2 * axis + 1] == right[2 * axis]:
                        merged = list(left)
                        merged[2 * axis + 1] = right[2 * axis + 1]
                    elif right[2 * axis + 1] == left[2 * axis]:
                        merged = list(right)
                        merged[2 * axis + 1] = left[2 * axis + 1]
                    else:
                        continue
                    work = [
                        box for k, box in enumerate(work) if k not in (i, j)
                    ] + [tuple(merged)]
                    work.sort()
                    changed = True
                    break
                if changed:
                    break
            if changed:
                break
    return work


def edge_record(
    negative_node: tuple[str, str],
    positive_node: tuple[str, str],
    origin: str,
    chart: str,
    axis: int,
    coordinate: Q,
    overlap: tuple[tuple[Q, Q], tuple[Q, Q]],
) -> tuple:
    """Round276-compatible unordered record.

    ``negative_node`` is geometrically on the negative side of the face and
    ``positive_node`` on the positive side.  Sorting occurs only after this
    orientation has been established.
    """

    low, high = sorted((negative_node, positive_node))
    return (
        low,
        high,
        origin,
        chart,
        axis,
        qtext(coordinate),
        tuple((qtext(a), qtext(b)) for a, b in overlap),
    )


def oriented_record(
    negative_node: tuple[str, str],
    positive_node: tuple[str, str],
    origin: str,
    chart: str,
    axis: int,
    coordinate: Q,
    overlap: tuple[tuple[Q, Q], tuple[Q, Q]],
) -> tuple:
    return (
        negative_node,
        positive_node,
        origin,
        chart,
        axis,
        qtext(coordinate),
        tuple((qtext(a), qtext(b)) for a, b in overlap),
    )


def enumerate_edges(
    node_boxes: dict[tuple[str, str], list[tuple[Q, ...]]],
    node_context: dict[tuple[str, str], tuple[str, str]],
) -> tuple[set[tuple], set[tuple], int, int]:
    """Enumerate positive common-face edges from explicit support boxes."""

    faces: dict[tuple, list[list[tuple]]] = collections.defaultdict(
        lambda: [[], []]
    )
    for node, boxes in node_boxes.items():
        origin, chart = node_context[node]
        leaf, signature_hash = node
        for support_index, box in enumerate(boxes):
            for axis in range(3):
                tangential = tuple(
                    (box[2 * other], box[2 * other + 1])
                    for other in range(3)
                    if other != axis
                )
                for side in (0, 1):
                    key = (
                        origin,
                        chart,
                        signature_hash,
                        axis,
                        box[2 * axis + side],
                    )
                    faces[key][side].append(
                        (node, tangential, support_index, leaf)
                    )

    unordered: set[tuple] = set()
    oriented: set[tuple] = set()
    positive_support_face_pair_count = 0
    exact_full_support_face_pair_count = 0
    for (
        origin,
        chart,
        _signature_hash,
        axis,
        coordinate,
    ), (lower_faces, upper_faces) in faces.items():
        # A box whose upper face is here lies on the negative side.  A box
        # whose lower face is here lies on the positive side.
        for negative_node, negative_tangential, _, _ in upper_faces:
            for positive_node, positive_tangential, _, _ in lower_faces:
                if negative_node == positive_node:
                    continue
                overlap = tuple(
                    (max(left[0], right[0]), min(left[1], right[1]))
                    for left, right in zip(
                        negative_tangential,
                        positive_tangential,
                        strict=True,
                    )
                )
                if not all(a < b for a, b in overlap):
                    continue
                positive_support_face_pair_count += 1
                if negative_tangential == positive_tangential:
                    exact_full_support_face_pair_count += 1
                unordered.add(
                    edge_record(
                        negative_node,
                        positive_node,
                        origin,
                        chart,
                        axis,
                        coordinate,
                        overlap,
                    )
                )
                oriented.add(
                    oriented_record(
                        negative_node,
                        positive_node,
                        origin,
                        chart,
                        axis,
                        coordinate,
                        overlap,
                    )
                )
    return (
        unordered,
        oriented,
        positive_support_face_pair_count,
        exact_full_support_face_pair_count,
    )


def endpoint_key(edge: tuple) -> tuple:
    """Edge identity without its overlap rectangle."""

    return edge[:6]


def main() -> int:
    round182 = P.load(
        "cm2_round182_source_g_clipped_graph_and_pair_arrangement_rows.json"
    )
    leaves = P.unpack(round182, "collar_leaf_rows")
    occurrences = {
        row["Round179_occurrence_row_id"]: row
        for row in P.unpack(round182, "collar_occurrence_rows")
    }
    leaf_by_id = {row["row_id"]: row for row in leaves}
    leaf_boxes = {
        row_id: box_tuple(row["box"]) for row_id, row in leaf_by_id.items()
    }

    node_rows: dict[tuple[str, str], list[tuple[int, dict]]] = (
        collections.defaultdict(list)
    )
    source_row_count = 0
    for round_number, name, ledger, leaf_field, _id_field in P.SOURCES:
        for row in P.load(name)[ledger]["rows"]:
            signature = row["local_return_signature"]
            signature_hash = row.get(
                "complete_10_field_return_signature_sha256",
                P.digest(signature),
            )
            assert signature_hash == P.digest(signature)
            leaf = row[leaf_field]
            node_rows[(leaf, signature_hash)].append((round_number, row))
            source_row_count += 1

    assert source_row_count == 332_020
    assert len(node_rows) == 332_016

    node_context: dict[tuple[str, str], tuple[str, str]] = {}
    whole_leaf_boxes: dict[tuple[str, str], list[tuple[Q, ...]]] = {}
    true_support_boxes: dict[tuple[str, str], list[tuple[Q, ...]]] = {}
    alias_nodes: list[tuple[str, str]] = []
    support_changed_nodes: list[tuple[str, str]] = []
    for node, rows in node_rows.items():
        leaf, _ = node
        occurrence = occurrences[leaf_by_id[leaf]["occurrence_row_id"]]
        node_context[node] = (
            occurrence["origin_row_id"],
            occurrence["chart"],
        )
        whole_leaf_boxes[node] = [leaf_boxes[leaf]]
        supports = []
        for round_number, row in rows:
            if (
                round_number == 271
                and row["signed_region_row_id"].startswith(
                    "round271-W-tail-side:"
                )
            ):
                supports.append(box_tuple(row["t_child_box"]))
            else:
                supports.append(leaf_boxes[leaf])
        normalized = merge_boxes(supports)
        true_support_boxes[node] = normalized
        if len(rows) == 2:
            alias_nodes.append(node)
            assert len(normalized) == 1
            assert normalized[0] == leaf_boxes[leaf]
        if normalized != [leaf_boxes[leaf]]:
            support_changed_nodes.append(node)

    assert len(alias_nodes) == 4
    # The four aliases recover their complete parent box.  Four other W-tail
    # signature atoms occupy only one t child.
    assert len(support_changed_nodes) == 4

    old_edges, old_oriented, old_face_pairs, old_full_face_pairs = (
        enumerate_edges(whole_leaf_boxes, node_context)
    )
    new_edges, new_oriented, new_face_pairs, new_full_face_pairs = (
        enumerate_edges(true_support_boxes, node_context)
    )
    assert len(old_edges) == 330_724
    assert P.digest(sorted(old_edges, key=str)) == (
        "8e6a26f93f954a89b37db293bd46c16ca087762e19758fafb6b0fc95864aebbb"
    )

    removed_records = old_edges - new_edges
    added_records = new_edges - old_edges
    old_by_key = {endpoint_key(edge): edge for edge in old_edges}
    new_by_key = {endpoint_key(edge): edge for edge in new_edges}
    shared_keys = set(old_by_key) & set(new_by_key)
    changed_keys = {
        key for key in shared_keys if old_by_key[key] != new_by_key[key]
    }
    unchanged_keys = {
        key for key in shared_keys if old_by_key[key] == new_by_key[key]
    }
    removed_endpoint_keys = set(old_by_key) - set(new_by_key)
    added_endpoint_keys = set(new_by_key) - set(old_by_key)

    changed_node_set = set(support_changed_nodes)

    def touches_changed(edge: tuple) -> bool:
        return edge[0] in changed_node_set or edge[1] in changed_node_set

    old_degree = collections.Counter(
        node for edge in old_edges for node in edge[:2]
    )
    new_degree = collections.Counter(
        node for edge in new_edges for node in edge[:2]
    )

    alias_payload = []
    for node in sorted(alias_nodes):
        rows = node_rows[node]
        alias_payload.append(
            {
                "node": list(node),
                "source_row_ids": sorted(
                    row[
                        "signed_region_row_id"
                    ]
                    for round_number, row in rows
                    if round_number == 271
                ),
                "child_boxes": sorted(
                    row["t_child_box"]
                    for round_number, row in rows
                    if round_number == 271
                ),
                "normalized_union_box": [
                    qtext(value) for value in true_support_boxes[node][0]
                ],
                "internal_artificial_middle_face_is_not_a_frontier_edge": True,
            }
        )

    changed_support_payload = []
    for node in sorted(support_changed_nodes):
        rows = node_rows[node]
        assert len(rows) == 1 and rows[0][0] == 271
        changed_support_payload.append(
            {
                "node": list(node),
                "source_row_id": rows[0][1]["signed_region_row_id"],
                "t_child": rows[0][1]["t_child"],
                "true_support_box": [
                    qtext(value) for value in true_support_boxes[node][0]
                ],
                "whole_leaf_box_previously_used": [
                    qtext(value) for value in whole_leaf_boxes[node][0]
                ],
                "old_candidate_degree": old_degree[node],
                "new_candidate_degree": new_degree[node],
            }
        )

    result = {
        "status": (
            "ROUND277_TRUE_SUPPORT_CANDIDATE_UNIVERSE_AUDIT__ZERO_CREDIT"
        ),
        "census": {
            "source_signature_row_count": source_row_count,
            "canonical_atom_count": len(node_rows),
            "explicit_artificial_alias_pair_count": len(alias_nodes),
            "alias_contraction_count": source_row_count - len(node_rows),
            "canonical_atoms_whose_support_union_recovers_whole_leaf": (
                len(node_rows) - len(support_changed_nodes)
            ),
            "canonical_atoms_with_strictly_smaller_frozen_rectangular_support": (
                len(support_changed_nodes)
            ),
            "old_same_signature_positive_support_face_pair_count": old_face_pairs,
            "old_same_signature_exact_full_support_face_pair_count": (
                old_full_face_pairs
            ),
            "old_same_signature_candidate_edge_count": len(old_edges),
            "new_same_signature_positive_support_face_pair_count": new_face_pairs,
            "new_same_signature_exact_full_support_face_pair_count": (
                new_full_face_pairs
            ),
            "new_same_signature_candidate_edge_count": len(new_edges),
            "unchanged_candidate_edge_count": len(unchanged_keys),
            "changed_overlap_same_endpoint_edge_count": len(changed_keys),
            "removed_endpoint_edge_count": len(removed_endpoint_keys),
            "added_endpoint_edge_count": len(added_endpoint_keys),
            "old_records_removed_count": len(removed_records),
            "new_records_added_count": len(added_records),
            "removed_records_touching_changed_support_atom_count": sum(
                touches_changed(edge) for edge in removed_records
            ),
            "added_records_touching_changed_support_atom_count": sum(
                touches_changed(edge) for edge in added_records
            ),
            "old_candidate_edges_incident_to_changed_support_atom_count": sum(
                touches_changed(edge) for edge in old_edges
            ),
            "new_candidate_edges_incident_to_changed_support_atom_count": sum(
                touches_changed(edge) for edge in new_edges
            ),
        },
        "digests": {
            "old_round276_compatible_candidate_edges_sha256": P.digest(
                sorted(old_edges, key=str)
            ),
            "new_true_support_candidate_edges_sha256": P.digest(
                sorted(new_edges, key=str)
            ),
            "new_true_support_oriented_candidate_edges_sha256": P.digest(
                sorted(new_oriented, key=str)
            ),
            "old_whole_leaf_oriented_candidate_edges_sha256": P.digest(
                sorted(old_oriented, key=str)
            ),
            "removed_old_records_sha256": P.digest(
                sorted(removed_records, key=str)
            ),
            "added_new_records_sha256": P.digest(
                sorted(added_records, key=str)
            ),
            "changed_endpoint_keys_sha256": P.digest(
                sorted(changed_keys, key=str)
            ),
            "removed_endpoint_keys_sha256": P.digest(
                sorted(removed_endpoint_keys, key=str)
            ),
            "added_endpoint_keys_sha256": P.digest(
                sorted(added_endpoint_keys, key=str)
            ),
        },
        "support_changed_atoms": changed_support_payload,
        "explicit_alias_contractions": alias_payload,
        "orientation_contract": {
            "negative_side_endpoint_source": (
                "support box whose UPPER face equals the shared coordinate"
            ),
            "positive_side_endpoint_source": (
                "support box whose LOWER face equals the shared coordinate"
            ),
            "tuple_endpoint_order_used_for_side_orientation": False,
        },
        "interpretation": {
            "candidate_edges_are_only_rectangular_support_upper_bounds": True,
            "positive_MATCH_patch_and_two_inward_corridors_still_required": True,
            "four_alias_middle_faces_are_alias_witnesses_not_component_edges": True,
        },
        "strict_nonpromotion": {
            "expanded_occurrence_credit": 0,
            "component_edge_credit": 0,
            "maximality_credit": 0,
            "CM2": "NO-GO_FOR_CLAIM",
        },
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
