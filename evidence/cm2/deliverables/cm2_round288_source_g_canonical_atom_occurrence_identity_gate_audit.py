#!/usr/bin/env python3
"""Round288: cacheless canonical-atom occurrence-identity gate audit.

This producer intentionally grants zero credit.  It reconstructs all 332,020
source signature rows and all 332,016 Round279 canonical atoms from pinned
frozen inputs, compares every atom support envelope against the complete
126,468-row Round266 occurrence geometry, and exhausts positive-volume
same-chart/same-signature overlap among distinct atoms.

The audit is fail-closed about physical promotion: a rectangular *support
envelope* and a rational point witness are not a positive-volume rational
inner-support certificate.
"""
from __future__ import annotations

import argparse
import collections
import gc
import gzip
import hashlib
import io
import json
import os
import stat
import tempfile
from fractions import Fraction as Q
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent
PREFIX = "cm2_round288_source_g_canonical_atom_occurrence_identity_gate_audit"
OUTPUT = HERE / f"{PREFIX}_result.json"
ATOM_DISPOSITIONS = HERE / f"{PREFIX}_atom_dispositions.json.gz"
EXISTING_OVERLAPS = HERE / f"{PREFIX}_existing_overlap_relations.json.gz"
SCHEMA = "cm2.round288.source-g-canonical-atom-occurrence-identity-gate-audit.v1"

PINS = {
    "cm2_round174_source_g_unique_first_dynamic_occurrence_materialization_rows.json":
        "9edeea2e1033b0dd70dee11a53b0f6aeb21fe74030aeefb60b081a7c420cff54",
    "cm2_round179_source_g_residual_tube_arrangement_rows.json":
        "f20b42c1fed781779b537b4d45bf44233eae1ed3ee620b95177a80f0eb2b5e42",
    "cm2_round182_source_g_clipped_graph_and_pair_arrangement_rows.json":
        "ae6e0c38df325e98b01a1d75acfbd8a85a71fda6a118db11d7dff6decf3f847c",
    "cm2_round204_source_g_wall_return_signature_local_replacement_certificate.json":
        "e7e1c49bebcb8c01f0fb4b33af66e4f2a8de560f121cae65f4971b2fec3e1818",
    "cm2_round208_source_g_outgoing_direct_signature_materialization_certificate.json":
        "4d01fb9cee639ec59786c078f7a20b3bbcd5c18ea674fabbfce64e250e765938",
    "cm2_round266_source_g_expanded_curved_face_closure_certificate.json":
        "2d30be104dc522ebb1664129894acf851180b9e5f51dd8471c33137447b599bf",
    "cm2_round269_source_g_closed_collar_direct_signature_materialization_certificate.json":
        "472df3ac65c490b79924beaabb382435f5b74ea8ac6c13d71b1d0ab54ffe01d3",
    "cm2_round270_source_g_outgoing_g_factor_signature_materialization_certificate.json":
        "72a47e53ff601660cb63fe8062403e41a54450fa4a432638faf18a2c76b3efea",
    "cm2_round271_source_g_wall_and_outgoing_tail_signature_materialization_certificate.json":
        "c2a6b66c6fc6ac0b353b36254339a90b91f18c52246c324307ee49569bd7b747",
    "cm2_round272_source_g_boundary_dual_factor_wall_closure_certificate.json":
        "16050c7087deb546d39b2c7922274ccae7cec24a799ecafd9a8304ae1186d8f2",
    "cm2_round279_source_g_collar_atom_and_face_edge_freeze_atoms.json.gz":
        "283a10799e0c7d1156695c30cdb2533488602ca646a18804f93211c0a3132dbe",
    "cm2_round279_source_g_collar_atom_and_face_edge_freeze_edges.json.gz":
        "bc1b976c0609c3271690e3d52c9bae85571f1a7661f404d7bc2e65bb707a2695",
    "cm2_round279_source_g_collar_atom_and_face_edge_freeze_verification.json":
        "a4cd7a96a43a9011e223d230c9f604f567fa56f1b095403cf802261daab5de21",
    "cm2_round280_source_g_expanded_occurrence_identity_contract_audit_result.json":
        "873974c8b343961f9e7c1674a946681749a3c0267bc57a1ccc147ccd21b3bdfc",
    "cm2_round284_source_g_rechart_occurrence_overlap_contract_probe_result.json":
        "e25dd7b494ad2c2ccddc17601d28136c1919a3b16e41f008669bd6c14a513692",
    "cm2_round286_source_g_partial_overlap_exact_refinement_probe_result.json":
        "a3b705c489eff9df4e1129bcdf960c6ea9de435e326c1d7e040e01d63352d29e",
}

SOURCE_SPECS = (
    (
        208,
        "cm2_round208_source_g_outgoing_direct_signature_materialization_certificate.json",
        "formal_local_open_3D_signature_ledger",
        "leaf_row_id",
        "region_row_id",
    ),
    (
        269,
        "cm2_round269_source_g_closed_collar_direct_signature_materialization_certificate.json",
        "formal_direct_side_signature_ledger",
        "Round182_leaf_row_id",
        "signed_region_row_id",
    ),
    (
        270,
        "cm2_round270_source_g_outgoing_g_factor_signature_materialization_certificate.json",
        "formal_direct_side_signature_ledger",
        "Round182_leaf_row_id",
        "signed_region_row_id",
    ),
    (
        271,
        "cm2_round271_source_g_wall_and_outgoing_tail_signature_materialization_certificate.json",
        "formal_side_signature_ledger",
        "Round182_leaf_row_id",
        "signed_region_row_id",
    ),
    (
        272,
        "cm2_round272_source_g_boundary_dual_factor_wall_closure_certificate.json",
        "formal_side_signature_ledger",
        "Round182_leaf_row_id",
        "signed_region_row_id",
    ),
)

FIELDS = {
    "official_key_id",
    "official_key_ordinal",
    "official_key_row",
    "ordered_integer_wall_events",
    "outgoing_cell",
    "roof",
    "signed_wall_word",
    "source_chart",
    "target_chart",
    "target_lift",
}
STRICT_SIGNS = {"STRICT_NEGATIVE", "STRICT_POSITIVE"}


class AuditError(RuntimeError):
    pass


def need(condition: bool, label: str) -> None:
    if not condition:
        raise AuditError(label)


ENCODER = json.JSONEncoder(
    sort_keys=True,
    separators=(",", ":"),
    ensure_ascii=False,
    allow_nan=False,
)


def canonical(value: Any) -> bytes:
    return ENCODER.encode(value).encode()


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def file_sha256(path: Path) -> str:
    result = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            result.update(block)
    return result.hexdigest()


def raw(name: str, maximum: int = 1_200_000_000) -> bytes:
    path = HERE / name
    info = path.lstat()
    need(
        path.parent == HERE
        and stat.S_ISREG(info.st_mode)
        and not path.is_symlink()
        and info.st_nlink == 1
        and 0 < info.st_size <= maximum,
        f"regular pinned input:{name}",
    )
    payload = path.read_bytes()
    need(hashlib.sha256(payload).hexdigest() == PINS[name], f"file pin:{name}")
    return payload


def closed_json(name: str) -> dict[str, Any]:
    value = json.loads(raw(name))
    need(
        isinstance(value, dict)
        and "result" in value
        and value.get("result_sha256") == digest(value["result"]),
        f"closed document:{name}",
    )
    return value["result"]


def unpack(result: dict[str, Any], table: str) -> list[dict[str, Any]]:
    rows = result[table]
    columns = result["row_column_schemas"][table]
    census = result["table_census_and_sha256"][table]
    need(
        len(rows) == census["row_count"] and digest(rows) == census["rows_sha256"],
        f"packed table:{table}",
    )
    return [dict(zip(columns, row, strict=True)) for row in rows]


def qbox(values: list[str] | tuple[str, ...]) -> tuple[Q, ...]:
    result = tuple(Q(value) for value in values)
    need(
        len(result) == 6
        and all(result[2 * axis] < result[2 * axis + 1] for axis in range(3)),
        "positive rational box",
    )
    return result


def box_text(box: tuple[Q, ...]) -> list[str]:
    return [str(value) for value in box]


def box_volume(box: tuple[Q, ...]) -> Q:
    return (
        (box[1] - box[0])
        * (box[3] - box[2])
        * (box[5] - box[4])
    )


def contained(inner: tuple[Q, ...], outer: tuple[Q, ...]) -> bool:
    return all(
        outer[2 * axis] <= inner[2 * axis]
        and inner[2 * axis + 1] <= outer[2 * axis + 1]
        for axis in range(3)
    )


def positive_overlap(left: tuple[Q, ...], right: tuple[Q, ...]) -> bool:
    return all(
        max(left[2 * axis], right[2 * axis])
        < min(left[2 * axis + 1], right[2 * axis + 1])
        for axis in range(3)
    )


def merge_boxes(boxes: list[tuple[Q, ...]]) -> list[tuple[Q, ...]]:
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


def signature_from_geometry(row: dict[str, Any]) -> dict[str, Any]:
    return {
        "official_key_id": row["official_key_id"],
        "official_key_ordinal": row["official_key_ordinal"],
        "official_key_row": row["official_key_row"],
        "ordered_integer_wall_events": row["ordered_integer_wall_events"],
        "outgoing_cell": row["outgoing_cell"],
        "roof": row["roof"],
        "signed_wall_word": row["signed_wall_word"],
        "source_chart": row["chart"],
        "target_chart": row["target_chart"],
        "target_lift": row["owner_target"],
    }


def close(row: dict[str, Any]) -> dict[str, Any]:
    result = dict(row)
    need("row_sha256" not in result, "unclosed row")
    result["row_sha256"] = digest(result)
    return result


def ledger(rows: list[dict[str, Any]], id_field: str, schema: str) -> dict[str, Any]:
    return {
        "schema": schema,
        "row_count": len(rows),
        "rows_sha256": digest(rows),
        "row_ids_sha256": digest([row[id_field] for row in rows]),
        "row_hashes_sha256": digest([row["row_sha256"] for row in rows]),
        "every_row_closed_by_own_SHA256": True,
        "rows": rows,
    }


def gzip_bytes(value: Any) -> bytes:
    buffer = io.BytesIO()
    with gzip.GzipFile(filename="", mode="wb", fileobj=buffer, mtime=0) as handle:
        handle.write(canonical(value) + b"\n")
    return buffer.getvalue()


def atomic(path: Path, payload: bytes) -> None:
    descriptor, temporary = tempfile.mkstemp(prefix="." + path.name + ".", dir=path.parent)
    try:
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(payload)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


class IntervalNode:
    """Exact one-dimensional interval index used only to shortlist 3D boxes."""

    __slots__ = ("center", "cross_lower", "cross_upper", "left", "right")

    def __init__(self, rows: list[tuple[Any, ...]]):
        midpoints = sorted((row[4][0] + row[4][1]) / 2 for row in rows)
        self.center = midpoints[len(midpoints) // 2]
        left: list[tuple[Any, ...]] = []
        right: list[tuple[Any, ...]] = []
        cross: list[tuple[Any, ...]] = []
        for row in rows:
            if row[4][1] <= self.center:
                left.append(row)
            elif row[4][0] >= self.center:
                right.append(row)
            else:
                cross.append(row)
        if not cross:
            ordered = sorted(rows, key=lambda row: (row[4][0], row[4][1], row[0]))
            middle = len(ordered) // 2
            cross = [ordered[middle]]
            left = ordered[:middle]
            right = ordered[middle + 1 :]
            self.center = (cross[0][4][0] + cross[0][4][1]) / 2
        self.cross_lower = sorted(cross, key=lambda row: row[4][0])
        self.cross_upper = sorted(cross, key=lambda row: row[4][1], reverse=True)
        self.left = IntervalNode(left) if left else None
        self.right = IntervalNode(right) if right else None

    def query(self, lower: Q, upper: Q, output: list[tuple[Any, ...]]) -> None:
        if upper <= self.center:
            for row in self.cross_lower:
                if row[4][0] >= upper:
                    break
                output.append(row)
            if self.left is not None:
                self.left.query(lower, upper, output)
        elif lower >= self.center:
            for row in self.cross_upper:
                if row[4][1] <= lower:
                    break
                output.append(row)
            if self.right is not None:
                self.right.query(lower, upper, output)
        else:
            output.extend(self.cross_lower)
            if self.left is not None:
                self.left.query(lower, upper, output)
            if self.right is not None:
                self.right.query(lower, upper, output)


def validate_source_row(
    round_number: int,
    row: dict[str, Any],
    leaf_id: str,
    source_id: str,
) -> str:
    signature = row["local_return_signature"]
    need(set(signature) == FIELDS and digest(signature) == row.get(
        "complete_10_field_return_signature_sha256", digest(signature)
    ), f"complete signature:{source_id}")
    need(
        row.get("expanded_occurrence_credit", 0) == 0
        and row.get("component_edge_credit", row.get("component_credit", 0)) == 0,
        f"source nonpromotion:{source_id}",
    )
    if round_number == 208:
        need(
            row["strict_open_3D_region_exists"] is True
            and row["formal_local_open_3D_signature_credit"] == 1
            and row["adjacency_or_component_propagation_used"] is False
            and row["single_point_evaluation_used"] is False
            and row["parent_signature_guess_used"] is False,
            f"Round208 strict region:{source_id}",
        )
        return "ROUND208_EXISTING_POSITIVE_OPEN_REGION"
    if round_number in {269, 270}:
        need(
            row["direct_whole_leaf_base_certified"] is True
            and row["side_specific_signature_credit"] == 1
            and row["region_factor_sign"] in STRICT_SIGNS
            and row["HPLUS_sign"] in STRICT_SIGNS
            and row["HMINUS_sign"] in STRICT_SIGNS
            and row["candidate_region_id"]
            == leaf_id + ":" + row["region_factor_sign"],
            f"Round{round_number} strict factor side:{source_id}",
        )
        return f"ROUND{round_number}_CONNECTED_FACTOR_SIDE__NO_INNER_BOX_ROW"
    if round_number == 271:
        need(row["side_signature_credit"] == 1, f"Round271 signature credit:{source_id}")
        if row["collar_kind"] == "WALL":
            need(
                row["region_product_sign"] in STRICT_SIGNS
                and row["witness_source_factor_sign"] in STRICT_SIGNS
                and row["witness_target_factor_sign"] in STRICT_SIGNS
                and row["connected_side_extension"] in {
                    "ROUND182_SINGLE_ACTIVE_FACTOR_STRICT_T_MONOTONE_GRAPH_SIDE",
                    "ROUND182_STRICT_NO_GRAPH_CELL",
                },
                f"Round271 wall side:{source_id}",
            )
            return "ROUND271_CONNECTED_WALL_SIDE__POINT_WITNESS_ONLY"
        if source_id.startswith("round271-W-tail-side:"):
            need(
                row["region_product_sign"] in STRICT_SIGNS
                and box_volume(qbox(row["t_child_box"])) > 0,
                f"Round271 W tail:{source_id}",
            )
            return "ROUND271_OUTGOING_W_TAIL_FACTOR_SIDE__ENVELOPE_NOT_INNER_BOX"
        need(
            source_id.startswith("round271-G-tail-side:")
            and row["one_sided_extension"]
            == "EXACT_SOURCE_AXIS_FACTOR_PROPORTIONAL_TO_t_WITH_STRICT_NONZERO_INTERIOR_SIGN",
            f"Round271 G tail:{source_id}",
        )
        return "ROUND271_OUTGOING_G_TAIL__POINT_WITNESS_ONLY"
    need(
        round_number == 272
        and row["side_signature_credit"] == 1
        and row["region_product_sign"] in STRICT_SIGNS
        and row["witness_source_factor_sign"] in STRICT_SIGNS
        and row["witness_target_factor_sign"] in STRICT_SIGNS
        and row["connected_side_extension"]
        == "ONE_SIDED_SOURCE_FACTOR_STRICT_ON_OPEN_INTERIOR__TARGET_FACTOR_IS_THE_ONLY_ACTIVE_GRAPH"
        and row["exact_source_factor_identity"].startswith(
            "source transverse wall factor = (9/25)*t"
        ),
        f"Round272 strict boundary wall side:{source_id}",
    )
    return "ROUND272_CONNECTED_BOUNDARY_WALL_SIDE__POINT_WITNESS_ONLY"


def build(seed: int) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    # Seed is deliberately inert; two externally seeded executions must agree.
    del seed
    for name in PINS:
        need(file_sha256(HERE / name) == PINS[name], f"stream pin:{name}")

    round179 = closed_json(
        "cm2_round179_source_g_residual_tube_arrangement_rows.json"
    )
    retained = {
        row["row_id"]: row
        for row in unpack(round179, "retained_3d_child_rows")
    }
    resolved179 = unpack(round179, "resolved_3d_child_rows")
    need(len(retained) == 106_680 and len(resolved179) == 17_192, "Round179 census")
    del round179

    round182 = closed_json(
        "cm2_round182_source_g_clipped_graph_and_pair_arrangement_rows.json"
    )
    leaves = {
        row["row_id"]: row for row in unpack(round182, "collar_leaf_rows")
    }
    collars = {
        row["Round179_occurrence_row_id"]: row
        for row in unpack(round182, "collar_occurrence_rows")
    }
    need(len(leaves) == 202_840 and len(collars) == 54_220, "Round182 census")
    del round182

    # Every leaf is a positive-volume subset of a retained true-chart owner.
    for leaf in leaves.values():
        child = retained[leaf["retained_child_row_id"]]
        collar = collars[leaf["occurrence_row_id"]]
        leaf_box = qbox(leaf["box"])
        child_box = qbox(child["box"])
        need(
            Q(leaf["coordinate_volume"]) == box_volume(leaf_box) > 0
            and contained(leaf_box, child_box)
            and child["chart"] == collar["chart"]
            and child["origin_row_id"] == collar["origin_row_id"]
            and child["parent_id"] == collar["parent_id"]
            and child["coordinate_volume"] != "0"
            and child["provenance"]
            == "ROUND179_ONE_STEP_POSITIVE_VOLUME_REMAINDER",
            f"true chart retained-child provenance:{leaf['row_id']}",
        )

    source_by_id: dict[str, tuple[int, str, str, str, str]] = {}
    grouped_sources: dict[tuple[str, str], list[tuple[int, str, dict[str, Any]]]] = (
        collections.defaultdict(list)
    )
    source_proof_histogram: collections.Counter[str] = collections.Counter()
    source_round_histogram: collections.Counter[int] = collections.Counter()
    for round_number, name, ledger_name, leaf_field, id_field in SOURCE_SPECS:
        result = closed_json(name)
        rows = result[ledger_name]["rows"]
        need(
            len(rows) == result[ledger_name]["row_count"]
            and digest(rows) == result[ledger_name]["rows_sha256"],
            f"source ledger:{round_number}",
        )
        for row in rows:
            source_id = row[id_field]
            leaf_id = row[leaf_field]
            need(source_id not in source_by_id and leaf_id in leaves, "source identity")
            signature = row["local_return_signature"]
            signature_hash = digest(signature)
            proof = validate_source_row(round_number, row, leaf_id, source_id)
            source_by_id[source_id] = (
                round_number,
                leaf_id,
                signature_hash,
                row["row_sha256"],
                proof,
            )
            grouped_sources[(leaf_id, signature_hash)].append(
                (round_number, source_id, row)
            )
            source_proof_histogram[proof] += 1
            source_round_histogram[round_number] += 1
        del result, rows
        gc.collect()
    need(
        source_round_histogram
        == {208: 36_040, 269: 187_128, 270: 37_712, 271: 70_420, 272: 720}
        and len(source_by_id) == 332_020
        and len(grouped_sources) == 332_016,
        "complete source signature census",
    )

    with gzip.open(
        HERE / "cm2_round279_source_g_collar_atom_and_face_edge_freeze_atoms.json.gz",
        "rt",
    ) as handle:
        atom_document = json.load(handle)
    atoms = atom_document["rows"]
    need(
        len(atoms) == atom_document["row_count"] == 332_016
        and digest(atoms) == atom_document["rows_sha256"],
        "Round279 atom ledger",
    )
    atom_by_id = {row["canonical_atom_id"]: row for row in atoms}
    need(len(atom_by_id) == len(atoms), "unique atom ids")

    # Reconstruct each canonical atom from inert source rows and Round182.
    for atom in atoms:
        stored = dict(atom)
        row_hash = stored.pop("row_sha256")
        need(digest(stored) == row_hash, f"atom row closure:{atom['canonical_atom_id']}")
        leaf_id = atom["Round182_leaf_row_id"]
        leaf = leaves[leaf_id]
        collar = collars[leaf["occurrence_row_id"]]
        signature_hash = atom["complete_10_field_return_signature_sha256"]
        sources = grouped_sources[(leaf_id, signature_hash)]
        need(
            atom["canonical_atom_id"]
            == "round279-collar-atom:" + digest([leaf_id, signature_hash])
            and atom["complete_10_field_return_signature"]
            == sources[0][2]["local_return_signature"]
            and all(
                source[2]["local_return_signature"]
                == atom["complete_10_field_return_signature"]
                for source in sources
            )
            and atom["source_signature_row_ids"]
            == sorted(source[1] for source in sources)
            and atom["source_rounds"] == sorted({source[0] for source in sources})
            and atom["source_alias_multiplicity"] == len(sources)
            and atom["Round182_occurrence_row_id"] == leaf["occurrence_row_id"]
            and atom["origin_row_id"] == collar["origin_row_id"]
            and atom["source_chart"] == collar["chart"]
            == atom["complete_10_field_return_signature"]["source_chart"]
            and atom["owner_target"] == collar["owner_target"]
            == atom["complete_10_field_return_signature"]["target_lift"],
            f"cacheless atom reconstruction:{atom['canonical_atom_id']}",
        )
        expected_boxes = []
        for round_number, _source_id, source_row in sources:
            expected_boxes.append(
                qbox(source_row["t_child_box"])
                if round_number == 271 and "t_child_box" in source_row
                else qbox(leaf["box"])
            )
        normalized = merge_boxes(expected_boxes)
        need(
            [box_text(box) for box in normalized]
            == atom["frozen_true_support_boxes"]
            and all(box_volume(box) > 0 for box in normalized)
            and all(contained(box, qbox(leaf["box"])) for box in normalized),
            f"support envelope reconstruction:{atom['canonical_atom_id']}",
        )

    # Round279 independently verified every edge corridor dynamically.  A
    # corridor is a positive-volume rational box strictly inside one signed
    # atom side, so it is an admissible inner support after its endpoint,
    # signature, chart and owner are rebound here (never from atom incidence
    # alone).
    verification279 = json.loads(
        raw("cm2_round279_source_g_collar_atom_and_face_edge_freeze_verification.json")
    )
    need(
        verification279["status"] == "PASS_INDEPENDENT_ROUND279"
        and verification279["canonical_atom_count"] == 332_016
        and verification279["formal_common_face_edge_witness_count"] == 330_724
        and verification279["formal_inward_corridor_witness_count"] == 661_448
        and verification279["dynamic_verification_histogram"] == {"PASS": 330_724}
        and verification279["attack_tests_rejected"]
        == verification279["attack_tests_total"]
        == 19,
        "Round279 independent dynamic corridor verification",
    )
    with gzip.open(
        HERE / "cm2_round279_source_g_collar_atom_and_face_edge_freeze_edges.json.gz",
        "rt",
    ) as handle:
        edge_document = json.load(handle)
    edges = edge_document["rows"]
    need(
        len(edges) == edge_document["row_count"] == 330_724
        and digest(edges) == edge_document["rows_sha256"],
        "Round279 edge ledger",
    )
    inner_corridors: dict[str, list[dict[str, Any]]] = collections.defaultdict(list)
    corridor_partition_histogram: collections.Counter[str] = collections.Counter()
    for edge in edges:
        stored_edge = dict(edge)
        edge_hash = stored_edge.pop("row_sha256")
        need(digest(stored_edge) == edge_hash, "Round279 edge row closure")
        endpoints = {row["leaf_row_id"]: row for row in edge["endpoint_atoms"]}
        corridors = {
            row["leaf_row_id"]: row for row in edge["two_inward_corridors"]
        }
        need(
            len(endpoints) == len(corridors) == 2
            and set(endpoints) == set(corridors),
            "edge endpoint/corridor bijection",
        )
        for leaf_id, endpoint in endpoints.items():
            atom = atom_by_id[endpoint["canonical_atom_id"]]
            corridor = corridors[leaf_id]
            expected_side = endpoint["geometric_side"] + "_SIDE_INWARD"
            corridor_box = qbox(corridor["exact_corridor_box"])
            atom_envelopes = [
                qbox(values) for values in atom["frozen_true_support_boxes"]
            ]
            need(
                endpoint["leaf_row_id"] == atom["Round182_leaf_row_id"]
                and corridor["geometric_side"] == expected_side
                and edge["complete_10_field_return_signature_sha256"]
                == atom["complete_10_field_return_signature_sha256"]
                and edge["source_chart"] == atom["source_chart"]
                and edge["owner_target"] == atom["owner_target"]
                and box_volume(corridor_box) > 0
                and any(
                    contained(corridor_box, envelope)
                    for envelope in atom_envelopes
                ),
                f"strict corridor atom rebinding:{atom['canonical_atom_id']}",
            )
            inner_corridors[atom["canonical_atom_id"]].append(
                {
                    "formal_face_edge_witness_row_id":
                        edge["formal_face_edge_witness_row_id"],
                    "witness_partition": edge["witness_partition"],
                    "dyadic_normal_depth": corridor["dyadic_normal_depth"],
                    "exact_positive_volume_rational_inner_support_box":
                        corridor["exact_corridor_box"],
                    "exact_inner_support_volume": str(box_volume(corridor_box)),
                    "Round279_independent_dynamic_verification":
                        "PASS_INDEPENDENT_ROUND279",
                }
            )
            corridor_partition_histogram[edge["witness_partition"]] += 1
    need(
        len(inner_corridors) == 310_808
        and sum(len(rows) for rows in inner_corridors.values()) == 661_448,
        "strict inward corridor atom census",
    )
    canonical_inner_corridor = {
        atom_id: min(
            rows,
            key=lambda row: (
                row["formal_face_edge_witness_row_id"],
                row["exact_positive_volume_rational_inner_support_box"],
            ),
        )
        for atom_id, rows in inner_corridors.items()
    }
    del edge_document, edges, inner_corridors
    gc.collect()

    # Complete existing occurrence geometry.  Round266 itself is pinned above;
    # these are its four frozen occurrence sources.
    existing: list[tuple[str, str, str, str, tuple[Q, ...], dict[str, Any]]] = []
    round174 = closed_json(
        "cm2_round174_source_g_unique_first_dynamic_occurrence_materialization_rows.json"
    )
    resolved174 = unpack(round174, "resolved_3d_occurrence_rows")
    for row in resolved174:
        signature = signature_from_geometry(row)
        need(
            row["ambient_dimension"] == 3
            and row["physical_open_subset_positive"] is True
            and Q(row["coordinate_volume"]) == box_volume(qbox(row["box"])) > 0,
            f"Round174 occurrence:{row['row_id']}",
        )
        existing.append(
            (
                row["row_id"],
                "ROUND174_RESOLVED",
                row["chart"],
                digest(signature),
                qbox(row["box"]),
                row,
            )
        )
    del round174, resolved174
    for row in resolved179:
        signature = signature_from_geometry(row)
        need(
            row["ambient_dimension"] == 3
            and row["credit_kind"] == "LOCAL_POSITIVE_3D_OCCURRENCE_ONLY"
            and Q(row["coordinate_volume"]) == box_volume(qbox(row["box"])) > 0,
            f"Round179 occurrence:{row['row_id']}",
        )
        existing.append(
            (
                row["row_id"],
                "ROUND179_RESOLVED",
                row["chart"],
                digest(signature),
                qbox(row["box"]),
                row,
            )
        )
    del resolved179

    round204 = closed_json(
        "cm2_round204_source_g_wall_return_signature_local_replacement_certificate.json"
    )
    rows204 = round204["formal_local_open_3D_region_ledger"]["rows"]
    for row in rows204:
        signature = signature_from_geometry(row)
        need(
            row["ambient_dimension"] == 3
            and row["strict_open_region"] is True
            and row["positive_coordinate_volume"] is True
            and row["formal_local_signature_credit"] == 1,
            f"Round204 occurrence:{row['region_row_id']}",
        )
        existing.append(
            (
                row["region_row_id"],
                "ROUND204_REGION",
                row["chart"],
                digest(signature),
                qbox(row["leaf_exact_box"]),
                row,
            )
        )
    del round204

    round208 = closed_json(
        "cm2_round208_source_g_outgoing_direct_signature_materialization_certificate.json"
    )
    rows208 = round208["formal_local_open_3D_signature_ledger"]["rows"]
    for row in rows208:
        signature = row["local_return_signature"]
        need(
            row["strict_open_3D_region_exists"] is True
            and row["formal_local_open_3D_signature_credit"] == 1,
            f"Round208 occurrence:{row['region_row_id']}",
        )
        existing.append(
            (
                row["region_row_id"],
                "ROUND208_REGION",
                signature["source_chart"],
                digest(signature),
                qbox(row["Round182_leaf_box"]),
                row,
            )
        )
    del round208
    need(
        collections.Counter(row[1] for row in existing)
        == {
            "ROUND174_RESOLVED": 72_500,
            "ROUND179_RESOLVED": 17_192,
            "ROUND204_REGION": 736,
            "ROUND208_REGION": 36_040,
        },
        "Round266 occurrence source census",
    )

    existing_groups: dict[tuple[str, str], list[tuple[Any, ...]]] = (
        collections.defaultdict(list)
    )
    for row in existing:
        existing_groups[(row[2], row[3])].append(row)
    existing_trees = {
        key: IntervalNode(rows) for key, rows in existing_groups.items()
    }

    disposition_rows: list[dict[str, Any]] = []
    overlap_rows: list[dict[str, Any]] = []
    disposition_histogram: collections.Counter[str] = collections.Counter()
    relation_histogram: collections.Counter[tuple[str, str]] = collections.Counter()
    unbacked_round_histogram: collections.Counter[tuple[int, ...]] = collections.Counter()
    promotion_ready_round_histogram: collections.Counter[tuple[int, ...]] = (
        collections.Counter()
    )
    unresolved_round_histogram: collections.Counter[tuple[int, ...]] = (
        collections.Counter()
    )
    overlap_atom_ids: set[str] = set()
    unbacked_overlap_atom_ids: set[str] = set()
    for atom in atoms:
        relations = []
        tree = existing_trees.get(
            (atom["source_chart"], atom["complete_10_field_return_signature_sha256"])
        )
        if tree is not None:
            for box_index, values in enumerate(atom["frozen_true_support_boxes"]):
                box = qbox(values)
                candidates: list[tuple[Any, ...]] = []
                tree.query(box[0], box[1], candidates)
                for existing_row in candidates:
                    if not positive_overlap(box, existing_row[4]):
                        continue
                    if box == existing_row[4]:
                        relation = "EXACT_EQUAL_SUPPORT_ENVELOPE"
                    elif contained(box, existing_row[4]):
                        relation = "ATOM_ENVELOPE_STRICTLY_CONTAINED_IN_EXISTING"
                    elif contained(existing_row[4], box):
                        relation = "EXISTING_ENVELOPE_STRICTLY_CONTAINED_IN_ATOM"
                    else:
                        relation = "PARTIAL_POSITIVE_VOLUME_ENVELOPE_OVERLAP"
                    relations.append((existing_row, box_index, relation))
        relations.sort(key=lambda item: (item[0][1], item[0][0], item[1], item[2]))
        if relations:
            overlap_atom_ids.add(atom["canonical_atom_id"])
            if atom["new_occurrence_region_atom_candidate"]:
                unbacked_overlap_atom_ids.add(atom["canonical_atom_id"])

        if atom["existing_Round208_occurrence_row_ids"]:
            need(
                len(relations) == 1
                and relations[0][0][1] == "ROUND208_REGION"
                and relations[0][2] == "EXACT_EQUAL_SUPPORT_ENVELOPE"
                and atom["existing_Round208_occurrence_row_ids"]
                == [relations[0][0][0]],
                f"Round208 existing alias:{atom['canonical_atom_id']}",
            )
            state = "EXISTING_ROUND208_OCCURRENCE_ID_PRESERVED"
            existing_id = relations[0][0][0]
            existing_source = "ROUND208_REGION"
            inner_status = "INHERITED_FROM_EXISTING_ROUND208_OCCURRENCE"
        elif relations:
            need(
                len(relations) == 1
                and relations[0][0][1] == "ROUND204_REGION"
                and relations[0][2] == "EXACT_EQUAL_SUPPORT_ENVELOPE",
                f"unbacked existing-overlap disposition:{atom['canonical_atom_id']}",
            )
            source_row = grouped_sources[
                (
                    atom["Round182_leaf_row_id"],
                    atom["complete_10_field_return_signature_sha256"],
                )
            ][0][2]
            existing_row = relations[0][0][5]
            need(
                existing_row["leaf_row_id"] == atom["Round182_leaf_row_id"]
                and existing_row["occurrence_row_id"]
                == source_row["occurrence_row_id"]
                and existing_row["origin_row_id"] == atom["origin_row_id"]
                and existing_row["owner_target"] == atom["owner_target"]
                and source_row["witness_source_factor_sign"].endswith(
                    existing_row["source_sign"]
                )
                and source_row["witness_target_factor_sign"].endswith(
                    existing_row["target_factor_sign"]
                ),
                f"Round204 exact physical-region alias:{atom['canonical_atom_id']}",
            )
            state = "EXACT_ALIAS_OF_EXISTING_ROUND204_OCCURRENCE"
            existing_id = relations[0][0][0]
            existing_source = "ROUND204_REGION"
            inner_status = "INHERITED_FROM_EXISTING_ROUND204_OCCURRENCE"
        else:
            existing_id = None
            existing_source = None
            unbacked_round_histogram[tuple(atom["source_rounds"])] += 1
            if atom["canonical_atom_id"] in canonical_inner_corridor:
                state = (
                    "NEW_DISJOINT_PROMOTION_READY_CANDIDATE__"
                    "ROUND279_STRICT_INWARD_CORRIDOR_INNER_SUPPORT__"
                    "PENDING_INDEPENDENT_ROUND288_VERIFIER"
                )
                inner_status = (
                    "PASS_PINNED_ROUND279_DYNAMIC_STRICT_INWARD_CORRIDOR"
                )
                promotion_ready_round_histogram[tuple(atom["source_rounds"])] += 1
            else:
                state = (
                    "NEW_DISJOINT_CANDIDATE__"
                    "POSITIVE_VOLUME_RATIONAL_INNER_SUPPORT_NOT_MATERIALIZED"
                )
                inner_status = (
                    "UNRESOLVED__SOURCE_HAS_ENVELOPE_OR_POINT_NOT_INNER_BOX"
                )
                unresolved_round_histogram[tuple(atom["source_rounds"])] += 1
        disposition_histogram[state] += 1

        reserved_id = (
            "source-g-expanded-occurrence:"
            + digest(
                [
                    "ROUND279_CANONICAL_ATOM_LOCAL_OCCURRENCE_V1",
                    atom["canonical_atom_id"],
                    atom["row_sha256"],
                    atom["Round182_leaf_row_id"],
                    atom["complete_10_field_return_signature_sha256"],
                    atom["source_signature_row_ids"],
                    atom["frozen_true_support_boxes"],
                ]
            )
            if state.startswith("NEW_DISJOINT")
            else None
        )
        proof_classes = sorted(
            {
                source_by_id[source_id][4]
                for source_id in atom["source_signature_row_ids"]
            }
        )
        selected_inner = canonical_inner_corridor.get(atom["canonical_atom_id"])
        disposition_rows.append(
            close(
                {
                    "Round288_atom_disposition_row_id":
                        "round288-atom-disposition:"
                        + digest(atom["canonical_atom_id"]),
                    "canonical_atom_id": atom["canonical_atom_id"],
                    "Round182_leaf_row_id": atom["Round182_leaf_row_id"],
                    "source_signature_row_ids": atom["source_signature_row_ids"],
                    "source_rounds": atom["source_rounds"],
                    "source_proof_classes": proof_classes,
                    "source_chart": atom["source_chart"],
                    "owner_target": atom["owner_target"],
                    "official_key_id":
                        atom["complete_10_field_return_signature"]["official_key_id"],
                    "official_key_ordinal":
                        atom["complete_10_field_return_signature"]["official_key_ordinal"],
                    "complete_10_field_return_signature_sha256":
                        atom["complete_10_field_return_signature_sha256"],
                    "frozen_positive_rational_support_envelopes":
                        atom["frozen_true_support_boxes"],
                    "true_chart_retained_child_owner_verified": True,
                    "positive_volume_existing_overlap_count": len(relations),
                    "occurrence_identity_disposition": state,
                    "existing_local_occurrence_row_id": existing_id,
                    "existing_occurrence_source": existing_source,
                    "reserved_candidate_occurrence_id__not_issued": reserved_id,
                    "positive_volume_rational_inner_support_status": inner_status,
                    "selected_Round279_strict_inner_corridor": selected_inner,
                    "formal_new_occurrence_credit": 0,
                    "formal_component_credit": 0,
                    "formal_maximality_credit": 0,
                    "Jx_Jy_same_point_glue_credit": 0,
                }
            )
        )
        for existing_row, box_index, relation in relations:
            relation_histogram[(existing_row[1], relation)] += 1
            overlap_rows.append(
                close(
                    {
                        "Round288_existing_overlap_relation_row_id":
                            "round288-existing-overlap:"
                            + digest(
                                [
                                    atom["canonical_atom_id"],
                                    existing_row[0],
                                    box_index,
                                ]
                            ),
                        "canonical_atom_id": atom["canonical_atom_id"],
                        "atom_support_box_index": box_index,
                        "existing_local_occurrence_row_id": existing_row[0],
                        "existing_occurrence_source": existing_row[1],
                        "source_chart": atom["source_chart"],
                        "complete_10_field_return_signature_sha256":
                            atom["complete_10_field_return_signature_sha256"],
                        "exact_box": box_text(existing_row[4]),
                        "relation": relation,
                        "physical_alias_credit": 0,
                        "component_credit": 0,
                    }
                )
            )

    disposition_rows.sort(key=lambda row: row["Round288_atom_disposition_row_id"])
    overlap_rows.sort(key=lambda row: row["Round288_existing_overlap_relation_row_id"])
    need(
        disposition_histogram
        == {
            "EXISTING_ROUND208_OCCURRENCE_ID_PRESERVED": 36_040,
            "EXACT_ALIAS_OF_EXISTING_ROUND204_OCCURRENCE": 640,
            (
                "NEW_DISJOINT_PROMOTION_READY_CANDIDATE__"
                "ROUND279_STRICT_INWARD_CORRIDOR_INNER_SUPPORT__"
                "PENDING_INDEPENDENT_ROUND288_VERIFIER"
            ): 274_176,
            (
                "NEW_DISJOINT_CANDIDATE__"
                "POSITIVE_VOLUME_RATIONAL_INNER_SUPPORT_NOT_MATERIALIZED"
            ): 21_160,
        }
        and relation_histogram
        == {
            ("ROUND208_REGION", "EXACT_EQUAL_SUPPORT_ENVELOPE"): 36_040,
            ("ROUND204_REGION", "EXACT_EQUAL_SUPPORT_ENVELOPE"): 640,
        }
        and len(overlap_atom_ids) == 36_680
        and len(unbacked_overlap_atom_ids) == 640,
        "existing overlap terminal disposition census",
    )

    # Same true chart + same complete signature is necessary for local
    # same-positive-open identity.  Physical supports are subsets of these
    # envelopes, so zero envelope overlap proves zero local duplicates.
    atom_items: list[tuple[Any, ...]] = []
    for atom in atoms:
        for box_index, values in enumerate(atom["frozen_true_support_boxes"]):
            atom_items.append(
                (
                    atom["canonical_atom_id"],
                    box_index,
                    atom["source_chart"],
                    atom["complete_10_field_return_signature_sha256"],
                    qbox(values),
                    atom["Round182_leaf_row_id"],
                )
            )
    atom_groups: dict[tuple[str, str], list[tuple[Any, ...]]] = (
        collections.defaultdict(list)
    )
    for item in atom_items:
        atom_groups[(item[2], item[3])].append(item)
    atom_trees = {key: IntervalNode(rows) for key, rows in atom_groups.items()}
    duplicate_pairs: list[tuple[str, int, str, int]] = []
    pair_shortlist_comparisons = 0
    for item in atom_items:
        candidates: list[tuple[Any, ...]] = []
        atom_trees[(item[2], item[3])].query(item[4][0], item[4][1], candidates)
        pair_shortlist_comparisons += len(candidates)
        for other in candidates:
            if (other[0], other[1]) <= (item[0], item[1]):
                continue
            if positive_overlap(item[4], other[4]):
                duplicate_pairs.append((item[0], item[1], other[0], other[1]))
    need(not duplicate_pairs, "distinct atom positive-volume envelope overlap")

    # The four source-row aliases are already contracted inside four canonical
    # atoms; they must not reappear as inter-atom pairs.
    alias_atoms = [
        atom for atom in atoms if atom["source_alias_multiplicity"] == 2
    ]
    need(
        len(alias_atoms) == 4
        and sum(atom["source_alias_multiplicity"] - 1 for atom in atoms) == 4,
        "only four pre-canonical W-tail aliases",
    )

    disposition_ledger = ledger(
        disposition_rows,
        "Round288_atom_disposition_row_id",
        "cm2.round288.canonical-atom-occurrence-disposition-ledger.v1",
    )
    overlap_ledger = ledger(
        overlap_rows,
        "Round288_existing_overlap_relation_row_id",
        "cm2.round288.existing-occurrence-overlap-relation-ledger.v1",
    )
    result = {
        "schema": SCHEMA,
        "status": (
            "PASS_ROUND288_CACHELESS_ATOM_IDENTITY_GATE_AUDIT__"
            "640_PREVIOUSLY_UNBACKED_ROUND204_ALIASES_FOUND__"
            "274176_STRICT_CORRIDOR_INNER_SUPPORTS__"
            "21160_ISOLATED_INNER_SUPPORT_RESIDUALS__ZERO_CREDIT"
        ),
        "input_file_pins": dict(sorted(PINS.items())),
        "census": {
            "source_signature_row_count": 332_020,
            "canonical_atom_count": 332_016,
            "precanonical_Round271_W_tail_alias_contraction_count": 4,
            "existing_Round266_occurrence_count": 126_468,
            "existing_overlap_relation_count": len(overlap_rows),
            "existing_Round208_alias_count": 36_040,
            "newly_discovered_Round204_alias_count": 640,
            "Round204_rows_not_in_Round279_atom_universe": 96,
            "unbacked_atom_count_before_Round288": 295_976,
            "conditionally_distinct_new_atom_candidate_count": 295_336,
            "promotion_ready_new_candidate_count_pending_Round288_independent_verifier":
                274_176,
            "isolated_new_candidate_inner_support_residual_count": 21_160,
            "conditional_occurrence_total_after_only_corridor_backed_candidates":
                400_644,
            "conditional_occurrence_total_if_all_inner_supports_later_pass":
                421_804,
            "Round279_strict_inward_corridor_count": 661_448,
            "Round279_strict_inward_corridor_incident_atom_count": 310_808,
            "Round279_face_isolated_atom_count": 21_208,
            "face_isolated_existing_Round208_atom_count": 48,
            "distinct_same_chart_same_signature_atom_positive_volume_overlap_pair_count":
                0,
            "pairwise_interval_shortlist_comparison_count":
                pair_shortlist_comparisons,
            "source_round_histogram":
                {str(key): value for key, value in sorted(source_round_histogram.items())},
            "source_proof_class_histogram": dict(sorted(source_proof_histogram.items())),
            "new_candidate_source_round_histogram": {
                "|".join(map(str, key)): value
                for key, value in sorted(unbacked_round_histogram.items())
            },
            "promotion_ready_source_round_histogram": {
                "|".join(map(str, key)): value
                for key, value in sorted(promotion_ready_round_histogram.items())
            },
            "unresolved_inner_support_source_round_histogram": {
                "|".join(map(str, key)): value
                for key, value in sorted(unresolved_round_histogram.items())
            },
            "strict_inner_corridor_partition_histogram":
                dict(sorted(corridor_partition_histogram.items())),
            "atom_disposition_histogram": dict(sorted(disposition_histogram.items())),
            "existing_overlap_relation_histogram": {
                "|".join(key): value
                for key, value in sorted(relation_histogram.items())
            },
        },
        "verdict": {
            "claim_that_all_295976_Round279_unbacked_atoms_are_new":
                "REJECTED",
            "reason":
                "640 rows are exact same-leaf, same-chart, same-owner, "
                "same-complete-signature and same-factor-sign aliases of "
                "already frozen Round204 local occurrences.",
            "remaining_295336_are_disjoint_from_complete_Round266_frontier":
                True,
            "remaining_295336_are_pairwise_locally_duplicate_free":
                True,
            "corridor_backed_274176_promotion_ready_after_independent_Round288_verifier":
                True,
            "formal_promotion_now": False,
            "remaining_promotion_blocker":
                "The 21,160 new face-isolated atoms have no Round279 inward "
                "corridor. Their source certificates provide connected "
                "factor-side existence and/or point witnesses, but no "
                "positive-volume rational inner-support box. The 274,176 "
                "corridor-backed candidates remain zero credit until a "
                "standalone Round288 verifier independently rebuilds this "
                "partition.",
        },
        "identity_contract": {
            "ordinary_common_face_never_collapses_occurrence_identity": True,
            "same_signature_never_collapses_occurrence_identity": True,
            "true_seam_never_collapses_occurrence_identity": True,
            "Jx_Jy_never_collapses_occurrence_identity": True,
            "cross_chart_positive_open_identity_requires_explicit_reverse_rechart_alias":
                True,
            "Round284_Round286_rechart_refinement_credit_remains_zero": True,
            "the_640_Round204_aliases_preserve_existing_occurrence_ids": True,
            "reserved_candidate_ids_are_not_formal_ids": True,
        },
        "strict_nonpromotion": {
            "formal_new_expanded_occurrence_credit": 0,
            "formal_occurrence_alias_credit": 0,
            "formal_component_union_credit": 0,
            "formal_DSU_rank_reduction_credit": 0,
            "maximality_credit": 0,
            "fibre_credit": 0,
            "global_disposition_credit": 0,
            "Jx_Jy_same_point_glue_credit": 0,
            "expanded_occurrences": 126_468,
            "quotient_components": 63_224,
            "maximality": "0/63224",
            "exact_key_fibres": "0/116",
            "global_dispositions": "0/224580",
            "Gate5": "10/18",
            "D02": "BLOCKED",
            "CM2": "NO-GO_FOR_CLAIM",
        },
        "required_next": [
            "Preserve the 36,040 Round208 and 640 Round204 occurrence IDs.",
            "Run a standalone cacheless Round288 verifier over all 332,016 dispositions and all 661,448 pinned dynamic corridors.",
            "After verifier PASS, a promoting round may issue 274,176 deterministic new occurrence IDs backed by canonical strict inward corridors.",
            "For each of the remaining 21,160 isolated new atoms, construct and dynamically certify a strict positive-volume rational inner box inside its source factor-side region.",
            "Re-run the complete existing-frontier and pairwise duplicate audit for those isolated inner supports.",
            "Face, true seam and Jx/Jy remain outside occurrence identity.",
        ],
        "atom_disposition_ledger": {
            "filename": ATOM_DISPOSITIONS.name,
            "row_count": disposition_ledger["row_count"],
            "rows_sha256": disposition_ledger["rows_sha256"],
            "row_ids_sha256": disposition_ledger["row_ids_sha256"],
            "row_hashes_sha256": disposition_ledger["row_hashes_sha256"],
        },
        "existing_overlap_relation_ledger": {
            "filename": EXISTING_OVERLAPS.name,
            "row_count": overlap_ledger["row_count"],
            "rows_sha256": overlap_ledger["rows_sha256"],
            "row_ids_sha256": overlap_ledger["row_ids_sha256"],
            "row_hashes_sha256": overlap_ledger["row_hashes_sha256"],
        },
        "provenance": {
            "producer_sha256": file_sha256(Path(__file__).resolve()),
            "cache_or_pickle_input_used": False,
            "source_certificates_treated_as_pinned_inert_documents": True,
            "seed_affects_output": False,
        },
    }
    return disposition_ledger, overlap_ledger, result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, default=288071)
    parser.add_argument("--output", type=Path, default=OUTPUT)
    parser.add_argument("--atom-dispositions", type=Path, default=ATOM_DISPOSITIONS)
    parser.add_argument("--existing-overlaps", type=Path, default=EXISTING_OVERLAPS)
    args = parser.parse_args()
    dispositions, overlaps, result = build(args.seed)
    disposition_payload = gzip_bytes(dispositions)
    overlap_payload = gzip_bytes(overlaps)
    result["atom_disposition_ledger"]["file_sha256"] = hashlib.sha256(
        disposition_payload
    ).hexdigest()
    result["existing_overlap_relation_ledger"]["file_sha256"] = hashlib.sha256(
        overlap_payload
    ).hexdigest()
    result["result_sha256"] = digest(result)
    atomic(args.atom_dispositions, disposition_payload)
    atomic(args.existing_overlaps, overlap_payload)
    atomic(args.output, canonical(result) + b"\n")
    print(result["status"])
    print("result_sha256=" + result["result_sha256"])
    print("atom_dispositions_sha256=" + hashlib.sha256(disposition_payload).hexdigest())
    print("existing_overlaps_sha256=" + hashlib.sha256(overlap_payload).hexdigest())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
