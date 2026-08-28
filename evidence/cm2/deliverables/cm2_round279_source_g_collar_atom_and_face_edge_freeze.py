#!/usr/bin/env python3
"""Round279: formal zero-credit freeze of collar atoms and face witnesses."""
from __future__ import annotations

import argparse
import collections
import gzip
import hashlib
import json
import os
import tempfile
from fractions import Fraction as Q
from pathlib import Path

import cm2_round276_source_g_collar_region_face_binding_probe as r276
import cm2_round277_source_g_collar_common_face_match_probe as r277
import cm2_round277_source_g_true_support_candidate_universe_audit as support
import cm2_round278_source_g_round271_w_tail_artificial_split_alias_probe as r278


HERE = Path(__file__).resolve().parent
PREFIX = "cm2_round279_source_g_collar_atom_and_face_edge_freeze"
CERTIFICATE = HERE / f"{PREFIX}_certificate.json"
ATOM_LEDGER = HERE / f"{PREFIX}_atoms.json.gz"
EDGE_LEDGER = HERE / f"{PREFIX}_edges.json.gz"
SCHEMA = "cm2.round279.source-g-collar-atom-and-face-edge-freeze.v1"

DEPTH4 = "cm2_round279_source_g_depth4_face_edge_witnesses_zero_credit.json.gz"
DEPTH8 = "cm2_round277_source_g_depth8_new_match_patches_zero_credit.json.gz"
ACTIVE = (
    "cm2_round277_source_g_depth8_active_graph_face_edge_witnesses_zero_credit.json.gz"
)
R182 = "cm2_round182_source_g_clipped_graph_and_pair_arrangement_rows.json"


def canonical(value):
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode()


def digest(value):
    return hashlib.sha256(canonical(value)).hexdigest()


def close(row):
    result = dict(row)
    assert "row_sha256" not in result
    result["row_sha256"] = digest(result)
    return result


def atomic_write(path, payload):
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary = tempfile.mkstemp(prefix=path.name + ".", dir=path.parent)
    try:
        with os.fdopen(fd, "wb") as handle:
            handle.write(payload)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def gzip_payload(payload):
    raw = (json.dumps(payload, sort_keys=True, separators=(",", ":")) + "\n").encode()
    return gzip.compress(raw, compresslevel=9, mtime=0)


def load_gzip(name):
    return json.loads(gzip.decompress((HERE / name).read_bytes()))


def install_candidates():
    # Reconstruct from the frozen R182/R208/R269/R270/R271/R272 inputs.
    # Never deserialize the historical, unpinned /tmp runtime cache.
    r277.build()
    assert len(r277.CAND) == 330724


def build_atoms():
    round182 = r276.load(R182)
    leaves = r276.unpack(round182, "collar_leaf_rows")
    occurrences = {
        row["Round179_occurrence_row_id"]: row
        for row in r276.unpack(round182, "collar_occurrence_rows")
    }
    leaf_by_id = {row["row_id"]: row for row in leaves}
    leaf_boxes = {
        row_id: support.box_tuple(row["box"])
        for row_id, row in leaf_by_id.items()
    }
    grouped = collections.defaultdict(list)
    source_count = 0
    for round_number, name, ledger, leaf_field, id_field in r276.SOURCES:
        rows = r276.load(name)[ledger]["rows"]
        for row in rows:
            signature = row["local_return_signature"]
            signature_hash = row.get(
                "complete_10_field_return_signature_sha256",
                digest(signature),
            )
            assert signature_hash == digest(signature)
            grouped[(row[leaf_field], signature_hash)].append(
                (round_number, row[id_field], row)
            )
            source_count += 1
    assert source_count == 332020
    assert len(grouped) == 332016
    rows = []
    atom_by_node = {}
    direct_count = 0
    alias_count = 0
    strict_support_count = 0
    for (leaf_id, signature_hash), sources in sorted(grouped.items()):
        leaf = leaf_by_id[leaf_id]
        occurrence = occurrences[leaf["occurrence_row_id"]]
        signature = sources[0][2]["local_return_signature"]
        assert all(source_row["local_return_signature"] == signature for _, _, source_row in sources)
        boxes = []
        for round_number, _source_id, source_row in sources:
            if (
                round_number == 271
                and source_row["signed_region_row_id"].startswith(
                    "round271-W-tail-side:"
                )
            ):
                boxes.append(support.box_tuple(source_row["t_child_box"]))
            else:
                boxes.append(leaf_boxes[leaf_id])
        normalized = support.merge_boxes(boxes)
        direct_ids = sorted(
            source_id
            for round_number, source_id, _row in sources
            if round_number == 208
        )
        assert len(direct_ids) <= 1
        direct_count += bool(direct_ids)
        alias_count += len(sources) == 2
        strict_support = normalized != [leaf_boxes[leaf_id]]
        strict_support_count += strict_support
        atom_id = "round279-collar-atom:" + digest([leaf_id, signature_hash])
        atom_by_node[(leaf_id, signature_hash)] = atom_id
        rows.append(
            close(
                {
                    "canonical_atom_id": atom_id,
                    "Round182_leaf_row_id": leaf_id,
                    "Round182_occurrence_row_id": leaf["occurrence_row_id"],
                    "origin_row_id": occurrence["origin_row_id"],
                    "source_chart": occurrence["chart"],
                    "owner_target": occurrence["owner_target"],
                    "complete_10_field_return_signature": signature,
                    "complete_10_field_return_signature_sha256": signature_hash,
                    "source_rounds": sorted(
                        {round_number for round_number, _id, _row in sources}
                    ),
                    "source_signature_row_ids": sorted(
                        source_id for _round, source_id, _row in sources
                    ),
                    "source_alias_multiplicity": len(sources),
                    "frozen_true_support_boxes": [
                        [str(value) for value in box] for box in normalized
                    ],
                    "whole_Round182_leaf_box": [
                        str(value) for value in leaf_boxes[leaf_id]
                    ],
                    "support_classification": (
                        "STRICT_FROZEN_SUBBOX"
                        if strict_support
                        else "WHOLE_ROUND182_LEAF"
                    ),
                    "existing_Round208_occurrence_row_ids": direct_ids,
                    "new_occurrence_region_atom_candidate": not bool(direct_ids),
                    "expanded_occurrence_credit": 0,
                    "component_credit": 0,
                    "maximality_credit": 0,
                }
            )
        )
    rows.sort(key=lambda row: row["canonical_atom_id"])
    assert direct_count == 36040
    assert alias_count == 4
    assert strict_support_count == 4
    payload = {
        "schema": "cm2.round279.canonical-collar-atom-ledger.v1",
        "status": "ROUND279_CANONICAL_COLLAR_ATOMS_FROZEN__ZERO_CREDIT",
        "row_count": len(rows),
        "source_signature_row_count": source_count,
        "artificial_alias_contraction_count": source_count - len(rows),
        "existing_Round208_occurrence_backed_atom_count": direct_count,
        "new_occurrence_region_atom_candidate_count": len(rows) - direct_count,
        "strict_subbox_atom_count": strict_support_count,
        "rows_sha256": digest(rows),
        "row_ids_sha256": digest([row["canonical_atom_id"] for row in rows]),
        "row_hashes_sha256": digest([row["row_sha256"] for row in rows]),
        "rows": rows,
        "strict_nonpromotion": {
            "expanded_occurrence_credit": 0,
            "component_credit": 0,
            "maximality_credit": 0,
        },
    }
    return payload, atom_by_node


def normalized_edge(candidate_index, partition, patch, corridors, atom_by_node):
    a, b, signature_hash, chart, target, axis, coordinate, overlap = r277.CAND[
        candidate_index
    ]
    endpoint = []
    for leaf_id in (a, b):
        box = r277.BOX[leaf_id]
        negative = box[2 * axis + 1] == coordinate
        positive = box[2 * axis] == coordinate
        assert negative != positive
        endpoint.append(
            {
                "leaf_row_id": leaf_id,
                "canonical_atom_id": atom_by_node[(leaf_id, signature_hash)],
                "geometric_side": "NEGATIVE" if negative else "POSITIVE",
            }
        )
    endpoint.sort(key=lambda row: row["geometric_side"])
    normalized_corridors = []
    for corridor in corridors:
        geometric_side = corridor.get("geometric_side", corridor.get("side"))
        assert geometric_side in {
            "NEGATIVE_SIDE_INWARD",
            "POSITIVE_SIDE_INWARD",
        }
        normalized_corridors.append(
            {
                "leaf_row_id": corridor["leaf_row_id"],
                "geometric_side": geometric_side,
                "dyadic_normal_depth": corridor["dyadic_normal_depth"],
                "exact_corridor_box": corridor["exact_corridor_box"],
            }
        )
    normalized_corridors.sort(key=lambda row: row["geometric_side"])
    return close(
        {
            "formal_face_edge_witness_row_id": (
                "round279-face-edge:" + digest([candidate_index, signature_hash])
            ),
            "candidate_index": candidate_index,
            "witness_partition": partition,
            "endpoint_atoms": endpoint,
            "complete_10_field_return_signature_sha256": signature_hash,
            "source_chart": chart,
            "owner_target": target,
            "common_face_axis": axis,
            "common_face_coordinate": str(coordinate),
            "candidate_overlap_rectangle": [
                [str(lower), str(upper)] for lower, upper in overlap
            ],
            "exact_positive_area_face_patch": patch,
            "two_inward_corridors": normalized_corridors,
            "expanded_occurrence_credit": 0,
            "component_edge_credit": 0,
            "maximality_credit": 0,
        }
    )


def build_edges(atom_by_node):
    depth4 = load_gzip(DEPTH4)
    depth8 = load_gzip(DEPTH8)
    active = load_gzip(ACTIVE)
    rows = []
    partitions = collections.Counter()
    indices_by_partition = collections.defaultdict(list)
    for source in depth4["rows"]:
        i = source["candidate_index"]
        rows.append(
            normalized_edge(
                i,
                "DEPTH4_ADAPTIVE_STRICT_PATCH",
                source["exact_positive_area_face_patch"],
                source["two_inward_corridors"],
                atom_by_node,
            )
        )
        partitions["DEPTH4_ADAPTIVE_STRICT_PATCH"] += 1
        indices_by_partition["DEPTH4_ADAPTIVE_STRICT_PATCH"].append(i)
    for source in depth8["rows"]:
        i = source["candidate_index"]
        rows.append(
            normalized_edge(
                i,
                "DEPTH8_SAFE_PRUNED_STRICT_PATCH",
                source["depth8_match_patch"]["exact_face_patch"],
                source["two_inward_corridors"],
                atom_by_node,
            )
        )
        partitions["DEPTH8_SAFE_PRUNED_STRICT_PATCH"] += 1
        indices_by_partition["DEPTH8_SAFE_PRUNED_STRICT_PATCH"].append(i)
    for source in active["rows"]:
        i = source["candidate_index"]
        rows.append(
            normalized_edge(
                i,
                (
                    "P_ENDPOINT_WEDGE_STRICT_PATCH"
                    if source["witness_classification"]
                    == "PASS_P_ENDPOINT_WEDGE_PATCH_AND_TWO_CORRIDORS"
                    else "ACTIVE_GRAPH_SIDE_STRICT_PATCH"
                ),
                source["exact_positive_area_face_patch"],
                source["two_inward_corridors"],
                atom_by_node,
            )
        )
        partition = rows[-1]["witness_partition"]
        partitions[partition] += 1
        indices_by_partition[partition].append(i)
    rows.sort(key=lambda row: row["candidate_index"])
    indices = [row["candidate_index"] for row in rows]
    assert indices == list(range(330724))
    assert partitions == {
        "DEPTH4_ADAPTIVE_STRICT_PATCH": 240932,
        "DEPTH8_SAFE_PRUNED_STRICT_PATCH": 57124,
        "ACTIVE_GRAPH_SIDE_STRICT_PATCH": 32416,
        "P_ENDPOINT_WEDGE_STRICT_PATCH": 252,
    }
    payload = {
        "schema": "cm2.round279.formal-common-face-edge-witness-ledger.v1",
        "status": "ROUND279_ALL_COMMON_FACE_EDGE_WITNESSES_FROZEN__ZERO_CREDIT",
        "row_count": len(rows),
        "witness_partition_histogram": dict(sorted(partitions.items())),
        "candidate_index_partition_sha256": {
            key: digest(sorted(value))
            for key, value in sorted(indices_by_partition.items())
        },
        "candidate_indices_sha256": digest(indices),
        "rows_sha256": digest(rows),
        "row_ids_sha256": digest(
            [row["formal_face_edge_witness_row_id"] for row in rows]
        ),
        "row_hashes_sha256": digest([row["row_sha256"] for row in rows]),
        "rows": rows,
        "strict_nonpromotion": {
            "expanded_occurrence_credit": 0,
            "component_edge_credit": 0,
            "maximality_credit": 0,
        },
    }
    return payload


def file_pins(names):
    return {
        name: hashlib.sha256((HERE / name).read_bytes()).hexdigest()
        for name in sorted(names)
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, default=279071)
    parser.add_argument("--certificate", type=Path, default=CERTIFICATE)
    parser.add_argument("--atom-ledger", type=Path, default=ATOM_LEDGER)
    parser.add_argument("--edge-ledger", type=Path, default=EDGE_LEDGER)
    args = parser.parse_args()
    assert args.seed >= 0
    install_candidates()
    atoms, atom_by_node = build_atoms()
    edges = build_edges(atom_by_node)
    aliases = r278.build()["result"]["formal_zero_credit_alias_witness_ledger"]
    assert aliases["row_count"] == 4
    atom_bytes = gzip_payload(atoms)
    edge_bytes = gzip_payload(edges)
    atomic_write(args.atom_ledger.resolve(), atom_bytes)
    atomic_write(args.edge_ledger.resolve(), edge_bytes)
    input_names = [
        R182,
        *(entry[1] for entry in r276.SOURCES),
        DEPTH4,
        DEPTH8,
        ACTIVE,
        "cm2_round278_source_g_round271_w_tail_artificial_split_alias_probe.py",
        "cm2_round174_source_g_unique_first_dynamic_occurrence_materialization.py",
    ]
    result = {
        "schema": SCHEMA,
        "status": "PASS_PRODUCER_ROUND279__FORMAL_ZERO_CREDIT_FREEZE",
        "census": {
            "source_signature_row_count": 332020,
            "canonical_atom_count": atoms["row_count"],
            "artificial_alias_contraction_count": 4,
            "alias_witness_row_count": aliases["row_count"],
            "existing_Round208_occurrence_backed_atom_count": 36040,
            "new_occurrence_region_atom_candidate_count": 295976,
            "formal_common_face_edge_witness_count": edges["row_count"],
            "formal_inward_corridor_witness_count": 2 * edges["row_count"],
            "remaining_common_face_candidate_edge_count": 0,
        },
        "canonical_atom_ledger_attachment": {
            "file_sha256": hashlib.sha256(atom_bytes).hexdigest(),
            "row_count": atoms["row_count"],
            "rows_sha256": atoms["rows_sha256"],
            "row_ids_sha256": atoms["row_ids_sha256"],
            "row_hashes_sha256": atoms["row_hashes_sha256"],
        },
        "artificial_alias_witness_ledger": aliases,
        "formal_common_face_edge_witness_ledger_attachment": {
            "file_sha256": hashlib.sha256(edge_bytes).hexdigest(),
            "row_count": edges["row_count"],
            "witness_partition_histogram": edges[
                "witness_partition_histogram"
            ],
            "candidate_index_partition_sha256": edges[
                "candidate_index_partition_sha256"
            ],
            "candidate_indices_sha256": edges["candidate_indices_sha256"],
            "rows_sha256": edges["rows_sha256"],
            "row_ids_sha256": edges["row_ids_sha256"],
            "row_hashes_sha256": edges["row_hashes_sha256"],
        },
        "exact_partition_contract": {
            "canonical_atoms_are_exact_quotient_of_332020_source_rows_by_four_proven_aliases": True,
            "candidate_edge_indices_are_exactly_0_through_330723": True,
            "edge_partitions_are_pairwise_disjoint": True,
            "edge_partitions_cover_the_complete_true_support_candidate_universe": True,
            "each_edge_has_one_positive_area_face_patch": True,
            "each_edge_has_exactly_two_geometrically_oriented_inward_corridors": True,
            "Jx_Jy_same_point_edges_included": False,
            "Round268_true_seam_edges_included": False,
        },
        "provenance": {
            "seed_is_order_irrelevant": True,
            "input_file_sha256": file_pins(input_names),
            "producer_file_sha256": hashlib.sha256(
                Path(__file__).read_bytes()
            ).hexdigest(),
        },
        "strict_nonpromotion": {
            "expanded_occurrence_credit": 0,
            "component_edge_credit": 0,
            "DSU_rank_reduction_credit": 0,
            "maximality_credit": 0,
            "exact_key_fibre_credit": 0,
            "global_disposition_credit": 0,
            "Jx_Jy_same_point_glue_credit": 0,
            "CM2": "NO-GO_FOR_CLAIM",
        },
    }
    document = {"result": result, "result_sha256": digest(result)}
    atomic_write(
        args.certificate.resolve(),
        json.dumps(document, indent=2, sort_keys=True).encode() + b"\n",
    )
    print(
        json.dumps(
            {
                "status": result["status"],
                "result_sha256": document["result_sha256"],
                "atom_ledger_file_sha256": result[
                    "canonical_atom_ledger_attachment"
                ]["file_sha256"],
                "edge_ledger_file_sha256": result[
                    "formal_common_face_edge_witness_ledger_attachment"
                ]["file_sha256"],
                **result["census"],
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
