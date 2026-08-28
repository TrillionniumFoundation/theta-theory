#!/usr/bin/env python3
"""Standalone cacheless verifier for the Round288 identity-gate audit.

The Round288 producer is pinned as inert source bytes and is never imported or
executed.  This verifier independently reconstructs the complete 332,020-row
signature source universe, the 332,016 Round279 canonical atoms, the complete
126,468-row existing occurrence frontier, every Round288 disposition and
existing-overlap relation, and the pairwise local non-overlap audit.

Crucially, the verifier does not rely on the Round279 verification JSON for
dynamic validity.  It structurally rebinds all 330,724 frozen face edges and
both of their inward corridors to independently reconstructed atoms, then
dynamically re-evaluates all 661,448 positive-volume rational corridors with
the byte-pinned Round174 evaluator at fixed python-flint precision.

All verified rows remain ZERO-CREDIT.  This verifier proves the audit
partition; it does not issue occurrence IDs or modify the frozen DSU.
"""

from __future__ import annotations

import argparse
import collections
from copy import deepcopy
from fractions import Fraction as Q
import gc
import gzip
import hashlib
import io
import json
import multiprocessing as mp
import os
from pathlib import Path
import random
import sys
import tempfile
from typing import Any, Callable

from flint import ctx, __version__ as FLINT_VERSION

import cm2_round174_source_g_unique_first_dynamic_occurrence_materialization as r174


HERE = Path(__file__).resolve().parent
PREFIX = "cm2_round288_source_g_canonical_atom_occurrence_identity_gate_audit"
PRODUCER = HERE / f"{PREFIX}.py"
RESULT = HERE / f"{PREFIX}_result.json"
DISPOSITIONS = HERE / f"{PREFIX}_atom_dispositions.json.gz"
OVERLAPS = HERE / f"{PREFIX}_existing_overlap_relations.json.gz"
OUTPUT = HERE / f"{PREFIX}_verification.json"

R174_ROWS = (
    "cm2_round174_source_g_unique_first_dynamic_occurrence_materialization_rows.json"
)
R174_SOURCE = (
    "cm2_round174_source_g_unique_first_dynamic_occurrence_materialization.py"
)
R179 = "cm2_round179_source_g_residual_tube_arrangement_rows.json"
R182 = "cm2_round182_source_g_clipped_graph_and_pair_arrangement_rows.json"
R204 = "cm2_round204_source_g_wall_return_signature_local_replacement_certificate.json"
R208 = "cm2_round208_source_g_outgoing_direct_signature_materialization_certificate.json"
R266 = "cm2_round266_source_g_expanded_curved_face_closure_certificate.json"
R269 = "cm2_round269_source_g_closed_collar_direct_signature_materialization_certificate.json"
R270 = "cm2_round270_source_g_outgoing_g_factor_signature_materialization_certificate.json"
R271 = "cm2_round271_source_g_wall_and_outgoing_tail_signature_materialization_certificate.json"
R272 = "cm2_round272_source_g_boundary_dual_factor_wall_closure_certificate.json"
R279_ATOMS = "cm2_round279_source_g_collar_atom_and_face_edge_freeze_atoms.json.gz"
R279_EDGES = "cm2_round279_source_g_collar_atom_and_face_edge_freeze_edges.json.gz"
R279_VERIFICATION = "cm2_round279_source_g_collar_atom_and_face_edge_freeze_verification.json"
R280 = "cm2_round280_source_g_expanded_occurrence_identity_contract_audit_result.json"
R284 = "cm2_round284_source_g_rechart_occurrence_overlap_contract_probe_result.json"
R286 = "cm2_round286_source_g_partial_overlap_exact_refinement_probe_result.json"

SCHEMA = "cm2.round288.source-g-canonical-atom-occurrence-identity-gate-audit.v1"
VERIFICATION_SCHEMA = SCHEMA + ".verification.v1"
DISPOSITION_SCHEMA = (
    "cm2.round288.canonical-atom-occurrence-disposition-ledger.v1"
)
OVERLAP_SCHEMA = (
    "cm2.round288.existing-occurrence-overlap-relation-ledger.v1"
)

INPUT_PINS = {
    R174_ROWS:
        "9edeea2e1033b0dd70dee11a53b0f6aeb21fe74030aeefb60b081a7c420cff54",
    R179:
        "f20b42c1fed781779b537b4d45bf44233eae1ed3ee620b95177a80f0eb2b5e42",
    R182:
        "ae6e0c38df325e98b01a1d75acfbd8a85a71fda6a118db11d7dff6decf3f847c",
    R204:
        "e7e1c49bebcb8c01f0fb4b33af66e4f2a8de560f121cae65f4971b2fec3e1818",
    R208:
        "4d01fb9cee639ec59786c078f7a20b3bbcd5c18ea674fabbfce64e250e765938",
    R266:
        "2d30be104dc522ebb1664129894acf851180b9e5f51dd8471c33137447b599bf",
    R269:
        "472df3ac65c490b79924beaabb382435f5b74ea8ac6c13d71b1d0ab54ffe01d3",
    R270:
        "72a47e53ff601660cb63fe8062403e41a54450fa4a432638faf18a2c76b3efea",
    R271:
        "c2a6b66c6fc6ac0b353b36254339a90b91f18c52246c324307ee49569bd7b747",
    R272:
        "16050c7087deb546d39b2c7922274ccae7cec24a799ecafd9a8304ae1186d8f2",
    R279_ATOMS:
        "283a10799e0c7d1156695c30cdb2533488602ca646a18804f93211c0a3132dbe",
    R279_EDGES:
        "bc1b976c0609c3271690e3d52c9bae85571f1a7661f404d7bc2e65bb707a2695",
    R279_VERIFICATION:
        "a4cd7a96a43a9011e223d230c9f604f567fa56f1b095403cf802261daab5de21",
    R280:
        "873974c8b343961f9e7c1674a946681749a3c0267bc57a1ccc147ccd21b3bdfc",
    R284:
        "e25dd7b494ad2c2ccddc17601d28136c1919a3b16e41f008669bd6c14a513692",
    R286:
        "a3b705c489eff9df4e1129bcdf960c6ea9de435e326c1d7e040e01d63352d29e",
}

ARTIFACT_PINS = {
    **INPUT_PINS,
    R174_SOURCE:
        "3d329525dda6697a3a5d2a8227c94bd9c309ea7ebcc4cdd0c7fbe573c267a218",
    PRODUCER.name:
        "f4821f38182bc2a14672be56edccaf8fa1c3a4b103f42fd472cdd2e42a089c6a",
    RESULT.name:
        "9b5875777f3937efe05a4d871a8c8b76c92ca69d0f636eb014542f59dfe49569",
    DISPOSITIONS.name:
        "6b0a8aa1cd38019322a61f5aaefc936006d10769cd21a5c8df374576f9ac570a",
    OVERLAPS.name:
        "d76d27c436735511dc34056d9237a2772decd30129e3019b74c5a02a118ab24e",
}

SOURCE_SPECS = (
    (208, R208, "formal_local_open_3D_signature_ledger", "leaf_row_id", "region_row_id"),
    (269, R269, "formal_direct_side_signature_ledger", "Round182_leaf_row_id", "signed_region_row_id"),
    (270, R270, "formal_direct_side_signature_ledger", "Round182_leaf_row_id", "signed_region_row_id"),
    (271, R271, "formal_side_signature_ledger", "Round182_leaf_row_id", "signed_region_row_id"),
    (272, R272, "formal_side_signature_ledger", "Round182_leaf_row_id", "signed_region_row_id"),
)

SIGNATURE_FIELDS = {
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

EXISTING_208 = "EXISTING_ROUND208_OCCURRENCE_ID_PRESERVED"
EXISTING_204 = "EXACT_ALIAS_OF_EXISTING_ROUND204_OCCURRENCE"
READY = (
    "NEW_DISJOINT_PROMOTION_READY_CANDIDATE__"
    "ROUND279_STRICT_INWARD_CORRIDOR_INNER_SUPPORT__"
    "PENDING_INDEPENDENT_ROUND288_VERIFIER"
)
ISOLATED = (
    "NEW_DISJOINT_CANDIDATE__"
    "POSITIVE_VOLUME_RATIONAL_INNER_SUPPORT_NOT_MATERIALIZED"
)

EXPECTED_NONPROMOTION = {
    "formal_new_expanded_occurrence_credit": 0,
    "formal_occurrence_alias_credit": 0,
    "formal_component_union_credit": 0,
    "formal_DSU_rank_reduction_credit": 0,
    "maximality_credit": 0,
    "fibre_credit": 0,
    "global_disposition_credit": 0,
    "Jx_Jy_same_point_glue_credit": 0,
    "expanded_occurrences": 126468,
    "quotient_components": 63224,
    "maximality": "0/63224",
    "exact_key_fibres": "0/116",
    "global_dispositions": "0/224580",
    "Gate5": "10/18",
    "D02": "BLOCKED",
    "CM2": "NO-GO_FOR_CLAIM",
}

ENCODER = json.JSONEncoder(
    sort_keys=True,
    separators=(",", ":"),
    ensure_ascii=False,
    allow_nan=False,
)


class VerificationError(RuntimeError):
    pass


def need(condition: bool, label: str) -> None:
    if not condition:
        raise VerificationError(label)


def canonical(value: Any) -> bytes:
    return ENCODER.encode(value).encode()


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def file_sha256(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            hasher.update(block)
    return hasher.hexdigest()


def read_json(path: Path) -> dict[str, Any]:
    with path.open("rb") as handle:
        value = json.load(handle)
    need(isinstance(value, dict), f"{path.name}:top-level object")
    return value


def read_gzip_json(path: Path) -> dict[str, Any]:
    with gzip.open(path, "rb") as handle:
        value = json.load(handle)
    need(isinstance(value, dict), f"{path.name}:top-level object")
    return value


def closed_result(filename: str) -> dict[str, Any]:
    document = read_json(HERE / filename)
    need(
        "result" in document
        and document.get("result_sha256") == digest(document["result"]),
        f"closed input:{filename}",
    )
    return document["result"]


def verify_embedded_result(value: dict[str, Any], label: str) -> None:
    stored = value["result_sha256"]
    payload = {key: item for key, item in value.items() if key != "result_sha256"}
    need(stored == digest(payload), f"{label}:result digest")


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
    box = tuple(Q(value) for value in values)
    need(
        len(box) == 6
        and all(box[2 * axis] < box[2 * axis + 1] for axis in range(3)),
        "positive rational box",
    )
    return box


def face_box(values: list[str] | tuple[str, ...], axis: int) -> tuple[Q, ...]:
    box = tuple(Q(value) for value in values)
    need(
        len(box) == 6
        and box[2 * axis] == box[2 * axis + 1]
        and all(
            box[2 * other] < box[2 * other + 1]
            for other in range(3) if other != axis
        ),
        "positive-area rational face box",
    )
    return box


def box_text(box: tuple[Q, ...]) -> list[str]:
    return [str(value) for value in box]


def volume(box: tuple[Q, ...]) -> Q:
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
        for left_index, left in enumerate(work):
            for right_index in range(left_index + 1, len(work)):
                right = work[right_index]
                for axis in range(3):
                    if any(
                        left[2 * other:2 * other + 2]
                        != right[2 * other:2 * other + 2]
                        for other in range(3) if other != axis
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
                        item for index, item in enumerate(work)
                        if index not in (left_index, right_index)
                    ] + [tuple(merged)]
                    work.sort()
                    changed = True
                    break
                if changed:
                    break
            if changed:
                break
    return work


def close_row(payload: dict[str, Any]) -> dict[str, Any]:
    row = dict(payload)
    need("row_sha256" not in row, "unclosed row")
    row["row_sha256"] = digest(row)
    return row


def validate_row(row: dict[str, Any], label: str) -> None:
    payload = dict(row)
    stored = payload.pop("row_sha256")
    need(stored == digest(payload), f"{label}:row closure")


def deterministic_gzip_bytes(value: Any) -> bytes:
    output = io.BytesIO()
    with gzip.GzipFile(
        filename="", mode="wb", fileobj=output, mtime=0
    ) as handle:
        handle.write(canonical(value) + b"\n")
    return output.getvalue()


def verify_attachment(
    document: dict[str, Any],
    id_field: str,
    expected_count: int,
    expected_schema: str,
    label: str,
) -> list[dict[str, Any]]:
    need(document["schema"] == expected_schema, f"{label}:schema")
    rows = document["rows"]
    need(
        document["row_count"] == len(rows) == expected_count,
        f"{label}:count",
    )
    need(document["rows_sha256"] == digest(rows), f"{label}:rows digest")
    ids = [row[id_field] for row in rows]
    hashes = [row["row_sha256"] for row in rows]
    need(len(ids) == len(set(ids)), f"{label}:unique ids")
    need(document["row_ids_sha256"] == digest(ids), f"{label}:id digest")
    need(
        document["row_hashes_sha256"] == digest(hashes),
        f"{label}:hash digest",
    )
    for row in rows:
        validate_row(row, label)
    return rows


class IntervalNode:
    """Exact one-dimensional interval tree used only as a 3D shortlist."""

    __slots__ = ("center", "cross_lower", "cross_upper", "left", "right")

    def __init__(self, rows: list[tuple[Any, ...]]):
        midpoints = sorted((row[4][0] + row[4][1]) / 2 for row in rows)
        self.center = midpoints[len(midpoints) // 2]
        lower_rows: list[tuple[Any, ...]] = []
        upper_rows: list[tuple[Any, ...]] = []
        cross: list[tuple[Any, ...]] = []
        for row in rows:
            if row[4][1] <= self.center:
                lower_rows.append(row)
            elif row[4][0] >= self.center:
                upper_rows.append(row)
            else:
                cross.append(row)
        if not cross:
            ordered = sorted(
                rows, key=lambda row: (row[4][0], row[4][1], row[0])
            )
            middle = len(ordered) // 2
            cross = [ordered[middle]]
            lower_rows = ordered[:middle]
            upper_rows = ordered[middle + 1:]
            self.center = (cross[0][4][0] + cross[0][4][1]) / 2
        self.cross_lower = sorted(cross, key=lambda row: row[4][0])
        self.cross_upper = sorted(
            cross, key=lambda row: row[4][1], reverse=True
        )
        self.left = IntervalNode(lower_rows) if lower_rows else None
        self.right = IntervalNode(upper_rows) if upper_rows else None

    def query(
        self,
        lower: Q,
        upper: Q,
        output: list[tuple[Any, ...]],
    ) -> None:
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


def validate_source_row(
    round_number: int,
    row: dict[str, Any],
    leaf_id: str,
    source_id: str,
) -> str:
    validate_row(row, f"Round{round_number} source")
    signature = row["local_return_signature"]
    need(
        set(signature) == SIGNATURE_FIELDS
        and row.get(
            "complete_10_field_return_signature_sha256", digest(signature)
        ) == digest(signature),
        f"complete signature:{source_id}",
    )
    need(
        row.get("expanded_occurrence_credit", 0) == 0
        and row.get(
            "component_edge_credit", row.get("component_credit", 0)
        ) == 0,
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
            f"Round{round_number} factor side:{source_id}",
        )
        return f"ROUND{round_number}_CONNECTED_FACTOR_SIDE__NO_INNER_BOX_ROW"
    if round_number == 271:
        need(row["side_signature_credit"] == 1, f"Round271 credit:{source_id}")
        if row["collar_kind"] == "WALL":
            need(
                row["region_product_sign"] in STRICT_SIGNS
                and row["witness_source_factor_sign"] in STRICT_SIGNS
                and row["witness_target_factor_sign"] in STRICT_SIGNS
                and row["connected_side_extension"] in {
                    "ROUND182_SINGLE_ACTIVE_FACTOR_STRICT_T_MONOTONE_GRAPH_SIDE",
                    "ROUND182_STRICT_NO_GRAPH_CELL",
                },
                f"Round271 wall:{source_id}",
            )
            return "ROUND271_CONNECTED_WALL_SIDE__POINT_WITNESS_ONLY"
        if source_id.startswith("round271-W-tail-side:"):
            need(
                row["region_product_sign"] in STRICT_SIGNS
                and volume(qbox(row["t_child_box"])) > 0,
                f"Round271 W tail:{source_id}",
            )
            return (
                "ROUND271_OUTGOING_W_TAIL_FACTOR_SIDE__"
                "ENVELOPE_NOT_INNER_BOX"
            )
        need(
            source_id.startswith("round271-G-tail-side:")
            and row["one_sided_extension"]
            == (
                "EXACT_SOURCE_AXIS_FACTOR_PROPORTIONAL_TO_t_WITH_"
                "STRICT_NONZERO_INTERIOR_SIGN"
            ),
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
        == (
            "ONE_SIDED_SOURCE_FACTOR_STRICT_ON_OPEN_INTERIOR__"
            "TARGET_FACTOR_IS_THE_ONLY_ACTIVE_GRAPH"
        )
        and row["exact_source_factor_identity"].startswith(
            "source transverse wall factor = (9/25)*t"
        ),
        f"Round272 boundary wall:{source_id}",
    )
    return "ROUND272_CONNECTED_BOUNDARY_WALL_SIDE__POINT_WITNESS_ONLY"


def load_geometry_and_sources() -> dict[str, Any]:
    round179 = closed_result(R179)
    retained = {
        row["row_id"]: row
        for row in unpack(round179, "retained_3d_child_rows")
    }
    resolved179 = unpack(round179, "resolved_3d_child_rows")
    need(
        len(retained) == 106680 and len(resolved179) == 17192,
        "Round179 census",
    )
    del round179

    round182 = closed_result(R182)
    leaves = {
        row["row_id"]: row for row in unpack(round182, "collar_leaf_rows")
    }
    collars = {
        row["Round179_occurrence_row_id"]: row
        for row in unpack(round182, "collar_occurrence_rows")
    }
    need(
        len(leaves) == 202840 and len(collars) == 54220,
        "Round182 census",
    )
    del round182

    whole_boxes: dict[str, tuple[Q, ...]] = {}
    for leaf in leaves.values():
        leaf_box = qbox(leaf["box"])
        child = retained[leaf["retained_child_row_id"]]
        collar = collars[leaf["occurrence_row_id"]]
        child_box = qbox(child["box"])
        need(
            Q(leaf["coordinate_volume"]) == volume(leaf_box) > 0
            and contained(leaf_box, child_box)
            and child["chart"] == collar["chart"]
            and child["origin_row_id"] == collar["origin_row_id"]
            and child["parent_id"] == collar["parent_id"]
            and child["coordinate_volume"] != "0"
            and child["provenance"]
            == "ROUND179_ONE_STEP_POSITIVE_VOLUME_REMAINDER",
            f"leaf retained provenance:{leaf['row_id']}",
        )
        whole_boxes[leaf["row_id"]] = leaf_box

    source_by_id: dict[str, tuple[int, str, str, str, str]] = {}
    grouped_sources: dict[
        tuple[str, str], list[tuple[int, str, dict[str, Any]]]
    ] = collections.defaultdict(list)
    proof_histogram: collections.Counter[str] = collections.Counter()
    round_histogram: collections.Counter[int] = collections.Counter()
    for round_number, filename, ledger_name, leaf_field, id_field in SOURCE_SPECS:
        result = closed_result(filename)
        ledger = result[ledger_name]
        rows = ledger["rows"]
        need(
            len(rows) == ledger["row_count"]
            and digest(rows) == ledger["rows_sha256"],
            f"source ledger:{round_number}",
        )
        for row in rows:
            source_id = row[id_field]
            leaf_id = row[leaf_field]
            need(
                source_id not in source_by_id and leaf_id in leaves,
                f"source identity:{source_id}",
            )
            signature_hash = digest(row["local_return_signature"])
            proof = validate_source_row(
                round_number, row, leaf_id, source_id
            )
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
            proof_histogram[proof] += 1
            round_histogram[round_number] += 1
        del result, rows
        gc.collect()
    need(
        round_histogram
        == {208: 36040, 269: 187128, 270: 37712, 271: 70420, 272: 720}
        and len(source_by_id) == 332020
        and len(grouped_sources) == 332016
        and collections.Counter(
            len(rows) for rows in grouped_sources.values()
        ) == {1: 332012, 2: 4},
        "complete source universe",
    )

    return {
        "retained": retained,
        "resolved179": resolved179,
        "leaves": leaves,
        "collars": collars,
        "whole_boxes": whole_boxes,
        "source_by_id": source_by_id,
        "grouped_sources": grouped_sources,
        "source_proof_histogram": proof_histogram,
        "source_round_histogram": round_histogram,
    }


def reconstruct_atoms(
    geometry: dict[str, Any],
) -> tuple[
    list[dict[str, Any]],
    dict[str, dict[str, Any]],
    dict[tuple[str, str], list[tuple[Q, ...]]],
]:
    atom_document = read_gzip_json(HERE / R279_ATOMS)
    stored_rows = verify_attachment(
        atom_document,
        "canonical_atom_id",
        332016,
        "cm2.round279.canonical-collar-atom-ledger.v1",
        "Round279 atom",
    )
    grouped_sources = geometry["grouped_sources"]
    leaves = geometry["leaves"]
    collars = geometry["collars"]
    whole_boxes = geometry["whole_boxes"]
    expected_rows: list[dict[str, Any]] = []
    supports: dict[tuple[str, str], list[tuple[Q, ...]]] = {}
    for leaf_id, signature_hash in sorted(grouped_sources):
        sources = grouped_sources[(leaf_id, signature_hash)]
        leaf = leaves[leaf_id]
        collar = collars[leaf["occurrence_row_id"]]
        signature = sources[0][2]["local_return_signature"]
        need(
            all(
                source[2]["local_return_signature"] == signature
                for source in sources
            ),
            f"atom signature group:{leaf_id}",
        )
        boxes: list[tuple[Q, ...]] = []
        for round_number, source_id, source_row in sources:
            if (
                round_number == 271
                and source_id.startswith("round271-W-tail-side:")
            ):
                boxes.append(qbox(source_row["t_child_box"]))
            else:
                boxes.append(whole_boxes[leaf_id])
        normalized = merge_boxes(boxes)
        supports[(leaf_id, signature_hash)] = normalized
        direct_ids = sorted(
            source_id for round_number, source_id, _row in sources
            if round_number == 208
        )
        need(len(direct_ids) <= 1, f"atom direct alias:{leaf_id}")
        atom_id = "round279-collar-atom:" + digest(
            [leaf_id, signature_hash]
        )
        expected_rows.append(close_row({
            "canonical_atom_id": atom_id,
            "Round182_leaf_row_id": leaf_id,
            "Round182_occurrence_row_id": leaf["occurrence_row_id"],
            "origin_row_id": collar["origin_row_id"],
            "source_chart": collar["chart"],
            "owner_target": collar["owner_target"],
            "complete_10_field_return_signature": signature,
            "complete_10_field_return_signature_sha256": signature_hash,
            "source_rounds": sorted({
                round_number for round_number, _source_id, _row in sources
            }),
            "source_signature_row_ids": sorted(
                source_id for _round, source_id, _row in sources
            ),
            "source_alias_multiplicity": len(sources),
            "frozen_true_support_boxes":
                [box_text(box) for box in normalized],
            "whole_Round182_leaf_box": box_text(whole_boxes[leaf_id]),
            "support_classification":
                "STRICT_FROZEN_SUBBOX"
                if normalized != [whole_boxes[leaf_id]]
                else "WHOLE_ROUND182_LEAF",
            "existing_Round208_occurrence_row_ids": direct_ids,
            "new_occurrence_region_atom_candidate": not bool(direct_ids),
            "expanded_occurrence_credit": 0,
            "component_credit": 0,
            "maximality_credit": 0,
        }))
    expected_rows.sort(key=lambda row: row["canonical_atom_id"])
    need(
        len(expected_rows) == len(stored_rows) == 332016
        and digest(expected_rows) == atom_document["rows_sha256"],
        "independent atom reconstruction digest",
    )
    for expected, stored in zip(expected_rows, stored_rows, strict=True):
        need(expected == stored, f"atom exact rebuild:{expected['canonical_atom_id']}")
    atom_by_id = {
        row["canonical_atom_id"]: row for row in expected_rows
    }
    need(
        sum(row["source_alias_multiplicity"] - 1 for row in expected_rows) == 4
        and sum(
            bool(row["existing_Round208_occurrence_row_ids"])
            for row in expected_rows
        ) == 36040,
        "atom alias census",
    )
    return expected_rows, atom_by_id, supports


def load_existing_occurrences(
    geometry: dict[str, Any],
) -> list[tuple[str, str, str, str, tuple[Q, ...], dict[str, Any]]]:
    existing: list[
        tuple[str, str, str, str, tuple[Q, ...], dict[str, Any]]
    ] = []
    round174 = closed_result(R174_ROWS)
    resolved174 = unpack(round174, "resolved_3d_occurrence_rows")
    for row in resolved174:
        signature = signature_from_geometry(row)
        box = qbox(row["box"])
        need(
            row["ambient_dimension"] == 3
            and row["physical_open_subset_positive"] is True
            and Q(row["coordinate_volume"]) == volume(box) > 0,
            f"Round174 occurrence:{row['row_id']}",
        )
        existing.append((
            row["row_id"],
            "ROUND174_RESOLVED",
            row["chart"],
            digest(signature),
            box,
            row,
        ))
    del round174, resolved174

    for row in geometry["resolved179"]:
        signature = signature_from_geometry(row)
        box = qbox(row["box"])
        need(
            row["ambient_dimension"] == 3
            and row["credit_kind"] == "LOCAL_POSITIVE_3D_OCCURRENCE_ONLY"
            and Q(row["coordinate_volume"]) == volume(box) > 0,
            f"Round179 occurrence:{row['row_id']}",
        )
        existing.append((
            row["row_id"],
            "ROUND179_RESOLVED",
            row["chart"],
            digest(signature),
            box,
            row,
        ))

    round204 = closed_result(R204)
    ledger204 = round204["formal_local_open_3D_region_ledger"]
    need(
        len(ledger204["rows"]) == ledger204["row_count"]
        and digest(ledger204["rows"]) == ledger204["rows_sha256"],
        "Round204 ledger",
    )
    for row in ledger204["rows"]:
        validate_row(row, "Round204 occurrence")
        signature = signature_from_geometry(row)
        need(
            row["ambient_dimension"] == 3
            and row["strict_open_region"] is True
            and row["positive_coordinate_volume"] is True
            and row["formal_local_signature_credit"] == 1,
            f"Round204 occurrence:{row['region_row_id']}",
        )
        existing.append((
            row["region_row_id"],
            "ROUND204_REGION",
            row["chart"],
            digest(signature),
            qbox(row["leaf_exact_box"]),
            row,
        ))
    del round204

    round208 = closed_result(R208)
    ledger208 = round208["formal_local_open_3D_signature_ledger"]
    need(
        len(ledger208["rows"]) == ledger208["row_count"]
        and digest(ledger208["rows"]) == ledger208["rows_sha256"],
        "Round208 ledger",
    )
    for row in ledger208["rows"]:
        validate_row(row, "Round208 occurrence")
        signature = row["local_return_signature"]
        need(
            row["strict_open_3D_region_exists"] is True
            and row["formal_local_open_3D_signature_credit"] == 1,
            f"Round208 occurrence:{row['region_row_id']}",
        )
        existing.append((
            row["region_row_id"],
            "ROUND208_REGION",
            signature["source_chart"],
            digest(signature),
            qbox(row["Round182_leaf_box"]),
            row,
        ))
    del round208

    need(
        collections.Counter(row[1] for row in existing)
        == {
            "ROUND174_RESOLVED": 72500,
            "ROUND179_RESOLVED": 17192,
            "ROUND204_REGION": 736,
            "ROUND208_REGION": 36040,
        }
        and len(existing) == 126468,
        "complete Round266 occurrence frontier",
    )
    round266 = closed_result(R266)
    need(
        round266["census"]["complete_occurrence_frontier_count"] == 126468,
        "Round266 frontier census",
    )
    del round266
    return existing


def signature_payload(
    signature: dict[str, Any],
    source_chart: str,
) -> dict[str, Any]:
    return {
        "official_key_id": signature["key"]["identifier"],
        "official_key_ordinal": signature["key"]["ordinal"],
        "official_key_row": signature["key"]["row"],
        "ordered_integer_wall_events": signature["events"],
        "outgoing_cell": signature["outgoing_cell"],
        "roof": signature["roof"],
        "signed_wall_word": list(signature["pattern"]),
        "source_chart": source_chart,
        "target_chart": signature["target_chart"],
        "target_lift": signature["target"],
    }


def endpoint_supports_face(
    atom: dict[str, Any],
    axis: int,
    coordinate: Q,
    patch: tuple[Q, ...],
    side: str,
) -> bool:
    for values in atom["frozen_true_support_boxes"]:
        support = qbox(values)
        if side == "NEGATIVE":
            if support[2 * axis + 1] != coordinate:
                continue
        else:
            if support[2 * axis] != coordinate:
                continue
        if all(
            support[2 * other] <= patch[2 * other]
            and patch[2 * other + 1] <= support[2 * other + 1]
            for other in range(3) if other != axis
        ):
            return True
    return False


def structurally_rebind_edges(
    atoms: dict[str, dict[str, Any]],
) -> tuple[
    list[dict[str, Any]],
    dict[str, dict[str, Any]],
    collections.Counter[str],
    set[str],
]:
    edge_document = read_gzip_json(HERE / R279_EDGES)
    edges = verify_attachment(
        edge_document,
        "formal_face_edge_witness_row_id",
        330724,
        "cm2.round279.formal-common-face-edge-witness-ledger.v1",
        "Round279 edge",
    )
    need(
        [row["candidate_index"] for row in edges] == list(range(330724)),
        "Round279 edge candidate order",
    )
    canonical_corridor: dict[str, dict[str, Any]] = {}
    incident_atoms: set[str] = set()
    partition_histogram: collections.Counter[str] = collections.Counter()
    edge_ids: set[str] = set()
    corridor_count = 0

    for index, edge in enumerate(edges):
        edge_id = edge["formal_face_edge_witness_row_id"]
        need(
            edge_id
            == "round279-face-edge:" + digest([
                index,
                edge["complete_10_field_return_signature_sha256"],
            ])
            and edge_id not in edge_ids,
            f"edge identity:{index}",
        )
        edge_ids.add(edge_id)
        need(
            edge["expanded_occurrence_credit"] == 0
            and edge["component_edge_credit"] == 0
            and edge["maximality_credit"] == 0,
            f"edge nonpromotion:{index}",
        )
        endpoints = edge["endpoint_atoms"]
        corridors = edge["two_inward_corridors"]
        need(
            len(endpoints) == len(corridors) == 2
            and {row["geometric_side"] for row in endpoints}
            == {"NEGATIVE", "POSITIVE"}
            and {row["leaf_row_id"] for row in endpoints}
            == {row["leaf_row_id"] for row in corridors},
            f"edge endpoint/corridor bijection:{index}",
        )
        endpoint_by_leaf = {row["leaf_row_id"]: row for row in endpoints}
        need(len(endpoint_by_leaf) == 2, f"edge distinct leaves:{index}")
        endpoint_atoms = [
            atoms[endpoint["canonical_atom_id"]] for endpoint in endpoints
        ]
        need(
            len({atom["origin_row_id"] for atom in endpoint_atoms}) == 1
            and all(
                endpoint["leaf_row_id"] == atom["Round182_leaf_row_id"]
                and atom["source_chart"] == edge["source_chart"]
                and atom["owner_target"] == edge["owner_target"]
                and atom["complete_10_field_return_signature_sha256"]
                == edge["complete_10_field_return_signature_sha256"]
                for endpoint, atom in zip(endpoints, endpoint_atoms, strict=True)
            ),
            f"edge atom structural rebinding:{index}",
        )
        axis = edge["common_face_axis"]
        coordinate = Q(edge["common_face_coordinate"])
        need(
            isinstance(axis, int) and 0 <= axis < 3,
            f"edge axis:{index}",
        )
        patch = face_box(edge["exact_positive_area_face_patch"], axis)
        need(
            patch[2 * axis] == coordinate,
            f"edge face coordinate:{index}",
        )
        rectangle = [
            tuple(map(Q, interval))
            for interval in edge["candidate_overlap_rectangle"]
        ]
        need(
            len(rectangle) == 2
            and all(lower < upper for lower, upper in rectangle),
            f"edge overlap rectangle:{index}",
        )
        tangent_index = 0
        for other in range(3):
            if other == axis:
                continue
            lower, upper = rectangle[tangent_index]
            need(
                lower <= patch[2 * other]
                < patch[2 * other + 1] <= upper,
                f"edge tangential patch:{index}",
            )
            tangent_index += 1
        for endpoint, atom in zip(endpoints, endpoint_atoms, strict=True):
            need(
                endpoint_supports_face(
                    atom,
                    axis,
                    coordinate,
                    patch,
                    endpoint["geometric_side"],
                ),
                f"edge support face orientation:{index}",
            )

        corridors_by_leaf = {
            row["leaf_row_id"]: row for row in corridors
        }
        need(len(corridors_by_leaf) == 2, f"edge unique corridors:{index}")
        for leaf_id, endpoint in endpoint_by_leaf.items():
            atom = atoms[endpoint["canonical_atom_id"]]
            corridor = corridors_by_leaf[leaf_id]
            values = qbox(corridor["exact_corridor_box"])
            side = endpoint["geometric_side"]
            expected_side = side + "_SIDE_INWARD"
            need(
                corridor["geometric_side"] == expected_side,
                f"corridor side:{index}:{leaf_id}",
            )
            for other in range(3):
                if other != axis:
                    need(
                        values[2 * other:2 * other + 2]
                        == patch[2 * other:2 * other + 2],
                        f"corridor tangent identity:{index}:{leaf_id}",
                    )
            if side == "NEGATIVE":
                need(
                    values[2 * axis] < values[2 * axis + 1] == coordinate,
                    f"negative inward corridor:{index}:{leaf_id}",
                )
            else:
                need(
                    coordinate == values[2 * axis] < values[2 * axis + 1],
                    f"positive inward corridor:{index}:{leaf_id}",
                )
            need(
                any(
                    contained(values, qbox(support))
                    for support in atom["frozen_true_support_boxes"]
                ),
                f"corridor in frozen support:{index}:{leaf_id}",
            )
            depth = corridor["dyadic_normal_depth"]
            whole = qbox(atom["whole_Round182_leaf_box"])
            need(
                isinstance(depth, int)
                and depth >= 1
                and values[2 * axis + 1] - values[2 * axis]
                == (
                    whole[2 * axis + 1] - whole[2 * axis]
                ) / (2 ** depth),
                f"corridor dyadic normal width:{index}:{leaf_id}",
            )
            candidate = {
                "formal_face_edge_witness_row_id": edge_id,
                "witness_partition": edge["witness_partition"],
                "dyadic_normal_depth": depth,
                "exact_positive_volume_rational_inner_support_box":
                    corridor["exact_corridor_box"],
                "exact_inner_support_volume": str(volume(values)),
                "Round279_independent_dynamic_verification":
                    "PASS_INDEPENDENT_ROUND279",
            }
            atom_id = atom["canonical_atom_id"]
            incumbent = canonical_corridor.get(atom_id)
            if incumbent is None or (
                candidate["formal_face_edge_witness_row_id"],
                candidate[
                    "exact_positive_volume_rational_inner_support_box"
                ],
            ) < (
                incumbent["formal_face_edge_witness_row_id"],
                incumbent[
                    "exact_positive_volume_rational_inner_support_box"
                ],
            ):
                canonical_corridor[atom_id] = candidate
            incident_atoms.add(atom_id)
            partition_histogram[edge["witness_partition"]] += 1
            corridor_count += 1

    need(
        corridor_count == 661448
        and len(incident_atoms) == len(canonical_corridor) == 310808
        and partition_histogram == {
            "DEPTH4_ADAPTIVE_STRICT_PATCH": 481864,
            "DEPTH8_SAFE_PRUNED_STRICT_PATCH": 114248,
            "ACTIVE_GRAPH_SIDE_STRICT_PATCH": 64832,
            "P_ENDPOINT_WEDGE_STRICT_PATCH": 504,
        },
        "complete structural corridor census",
    )
    need(
        collections.Counter(edge["witness_partition"] for edge in edges)
        == {
            "DEPTH4_ADAPTIVE_STRICT_PATCH": 240932,
            "DEPTH8_SAFE_PRUNED_STRICT_PATCH": 57124,
            "ACTIVE_GRAPH_SIDE_STRICT_PATCH": 32416,
            "P_ENDPOINT_WEDGE_STRICT_PATCH": 252,
        },
        "edge partition census",
    )
    return edges, canonical_corridor, partition_histogram, incident_atoms


DYNAMIC_TABLES: Any = None
DYNAMIC_EDGES: list[dict[str, Any]] = []


def dynamic_corridor_signature_hash(
    chart: str,
    target: str,
    values: tuple[Q, ...],
    label: str,
) -> str | None:
    box = r174.atlas.AtlasBox(*values, 0, label)
    signature, _rejected = r174.dynamic_signature(
        chart, box, target, DYNAMIC_TABLES
    )
    if signature is None:
        return None
    return digest(signature_payload(signature, chart))


def dynamic_edge_worker(index: int) -> tuple[int, str | None]:
    try:
        edge = DYNAMIC_EDGES[index]
        wanted = edge["complete_10_field_return_signature_sha256"]
        for side_index, corridor in enumerate(edge["two_inward_corridors"]):
            actual = dynamic_corridor_signature_hash(
                edge["source_chart"],
                edge["owner_target"],
                tuple(map(Q, corridor["exact_corridor_box"])),
                f"r288-independent-corridor:{index}:{side_index}",
            )
            if actual != wanted:
                return (
                    0,
                    f"edge {index} corridor {side_index}:"
                    f"{actual!r}!={wanted!r}",
                )
        return 2, None
    except Exception as error:
        return 0, f"edge {index}:{type(error).__name__}:{error}"


def dynamically_verify_all_corridors(
    edges: list[dict[str, Any]],
    processes: int,
) -> dict[str, Any]:
    global DYNAMIC_TABLES, DYNAMIC_EDGES
    ctx.prec = 256
    need(ctx.prec == 256, "fixed FLINT precision")
    gate5 = r174.load_inputs()["gate5"]
    DYNAMIC_TABLES = r174.registry_tables(gate5)
    del gate5
    DYNAMIC_EDGES = edges
    passed_edges = 0
    passed_corridors = 0
    failures: list[str] = []
    with mp.get_context("fork").Pool(processes) as pool:
        for corridor_increment, error in pool.imap_unordered(
            dynamic_edge_worker,
            range(len(edges)),
            chunksize=16,
        ):
            if error is None:
                passed_edges += 1
                passed_corridors += corridor_increment
            else:
                failures.append(error)
            done = passed_edges + len(failures)
            if done % 20000 == 0:
                print(
                    json.dumps({
                        "Round288_dynamic_edge_progress": done,
                        "total_edges": len(edges),
                        "passed_corridors": passed_corridors,
                        "failure_count": len(failures),
                    }, sort_keys=True),
                    flush=True,
                )
    need(
        not failures
        and passed_edges == 330724
        and passed_corridors == 661448,
        "complete fresh Round174 corridor evaluation:"
        + (failures[0] if failures else "census"),
    )
    return {
        "dynamically_verified_edge_count": passed_edges,
        "dynamically_verified_corridor_count": passed_corridors,
        "dynamic_signature_histogram": {"PASS": passed_corridors},
        "python_flint_version": FLINT_VERSION,
        "flint_precision_bits": ctx.prec,
        "Round279_verification_JSON_used_as_dynamic_evidence": False,
    }


def ledger_object(
    rows: list[dict[str, Any]],
    id_field: str,
    schema: str,
) -> dict[str, Any]:
    return {
        "schema": schema,
        "row_count": len(rows),
        "rows_sha256": digest(rows),
        "row_ids_sha256": digest([row[id_field] for row in rows]),
        "row_hashes_sha256": digest([row["row_sha256"] for row in rows]),
        "every_row_closed_by_own_SHA256": True,
        "rows": rows,
    }


def reconstruct_round288_ledgers(
    atoms: list[dict[str, Any]],
    canonical_corridor: dict[str, dict[str, Any]],
    existing: list[
        tuple[str, str, str, str, tuple[Q, ...], dict[str, Any]]
    ],
    geometry: dict[str, Any],
    partition_histogram: collections.Counter[str],
    replay_seed: int,
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    rng = random.Random(replay_seed)
    existing_groups: dict[
        tuple[str, str], list[tuple[Any, ...]]
    ] = collections.defaultdict(list)
    for row in existing:
        existing_groups[(row[2], row[3])].append(row)
    existing_trees = {
        key: IntervalNode(rows) for key, rows in existing_groups.items()
    }

    disposition_rows: list[dict[str, Any]] = []
    overlap_rows: list[dict[str, Any]] = []
    disposition_histogram: collections.Counter[str] = collections.Counter()
    relation_histogram: collections.Counter[
        tuple[str, str]
    ] = collections.Counter()
    unbacked_round_histogram: collections.Counter[
        tuple[int, ...]
    ] = collections.Counter()
    promotion_ready_round_histogram: collections.Counter[
        tuple[int, ...]
    ] = collections.Counter()
    unresolved_round_histogram: collections.Counter[
        tuple[int, ...]
    ] = collections.Counter()
    overlap_atom_ids: set[str] = set()
    unbacked_overlap_atom_ids: set[str] = set()

    atom_order = list(atoms)
    rng.shuffle(atom_order)
    grouped_sources = geometry["grouped_sources"]
    source_by_id = geometry["source_by_id"]

    for atom in atom_order:
        relations: list[tuple[tuple[Any, ...], int, str]] = []
        tree = existing_trees.get((
            atom["source_chart"],
            atom["complete_10_field_return_signature_sha256"],
        ))
        if tree is not None:
            for box_index, values in enumerate(
                atom["frozen_true_support_boxes"]
            ):
                box = qbox(values)
                candidates: list[tuple[Any, ...]] = []
                tree.query(box[0], box[1], candidates)
                for existing_row in candidates:
                    if not positive_overlap(box, existing_row[4]):
                        continue
                    if box == existing_row[4]:
                        relation = "EXACT_EQUAL_SUPPORT_ENVELOPE"
                    elif contained(box, existing_row[4]):
                        relation = (
                            "ATOM_ENVELOPE_STRICTLY_CONTAINED_IN_EXISTING"
                        )
                    elif contained(existing_row[4], box):
                        relation = (
                            "EXISTING_ENVELOPE_STRICTLY_CONTAINED_IN_ATOM"
                        )
                    else:
                        relation = "PARTIAL_POSITIVE_VOLUME_ENVELOPE_OVERLAP"
                    relations.append((existing_row, box_index, relation))
        relations.sort(
            key=lambda item: (
                item[0][1], item[0][0], item[1], item[2]
            )
        )
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
                f"Round208 alias:{atom['canonical_atom_id']}",
            )
            state = EXISTING_208
            existing_id = relations[0][0][0]
            existing_source = "ROUND208_REGION"
            inner_status = "INHERITED_FROM_EXISTING_ROUND208_OCCURRENCE"
        elif relations:
            need(
                len(relations) == 1
                and relations[0][0][1] == "ROUND204_REGION"
                and relations[0][2] == "EXACT_EQUAL_SUPPORT_ENVELOPE",
                f"Round204 alias relation:{atom['canonical_atom_id']}",
            )
            source_row = grouped_sources[(
                atom["Round182_leaf_row_id"],
                atom["complete_10_field_return_signature_sha256"],
            )][0][2]
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
                f"Round204 physical alias:{atom['canonical_atom_id']}",
            )
            state = EXISTING_204
            existing_id = relations[0][0][0]
            existing_source = "ROUND204_REGION"
            inner_status = "INHERITED_FROM_EXISTING_ROUND204_OCCURRENCE"
        else:
            existing_id = None
            existing_source = None
            rounds = tuple(atom["source_rounds"])
            unbacked_round_histogram[rounds] += 1
            if atom["canonical_atom_id"] in canonical_corridor:
                state = READY
                inner_status = (
                    "PASS_PINNED_ROUND279_DYNAMIC_STRICT_INWARD_CORRIDOR"
                )
                promotion_ready_round_histogram[rounds] += 1
            else:
                state = ISOLATED
                inner_status = (
                    "UNRESOLVED__SOURCE_HAS_ENVELOPE_OR_POINT_NOT_INNER_BOX"
                )
                unresolved_round_histogram[rounds] += 1
        disposition_histogram[state] += 1

        reserved_id = (
            "source-g-expanded-occurrence:" + digest([
                "ROUND279_CANONICAL_ATOM_LOCAL_OCCURRENCE_V1",
                atom["canonical_atom_id"],
                atom["row_sha256"],
                atom["Round182_leaf_row_id"],
                atom["complete_10_field_return_signature_sha256"],
                atom["source_signature_row_ids"],
                atom["frozen_true_support_boxes"],
            ])
            if state.startswith("NEW_DISJOINT") else None
        )
        proof_classes = sorted({
            source_by_id[source_id][4]
            for source_id in atom["source_signature_row_ids"]
        })
        disposition_rows.append(close_row({
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
                atom["complete_10_field_return_signature"][
                    "official_key_ordinal"
                ],
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
            "selected_Round279_strict_inner_corridor":
                canonical_corridor.get(atom["canonical_atom_id"]),
            "formal_new_occurrence_credit": 0,
            "formal_component_credit": 0,
            "formal_maximality_credit": 0,
            "Jx_Jy_same_point_glue_credit": 0,
        }))
        for existing_row, box_index, relation in relations:
            relation_histogram[(existing_row[1], relation)] += 1
            overlap_rows.append(close_row({
                "Round288_existing_overlap_relation_row_id":
                    "round288-existing-overlap:" + digest([
                        atom["canonical_atom_id"],
                        existing_row[0],
                        box_index,
                    ]),
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
            }))

    disposition_rows.sort(
        key=lambda row: row["Round288_atom_disposition_row_id"]
    )
    overlap_rows.sort(
        key=lambda row: row["Round288_existing_overlap_relation_row_id"]
    )
    need(
        disposition_histogram == {
            EXISTING_208: 36040,
            EXISTING_204: 640,
            READY: 274176,
            ISOLATED: 21160,
        }
        and relation_histogram == {
            ("ROUND208_REGION", "EXACT_EQUAL_SUPPORT_ENVELOPE"): 36040,
            ("ROUND204_REGION", "EXACT_EQUAL_SUPPORT_ENVELOPE"): 640,
        }
        and len(overlap_atom_ids) == 36680
        and len(unbacked_overlap_atom_ids) == 640,
        "existing overlap terminal census",
    )

    # Exact same-chart/same-signature envelope overlap exhaustion.
    atom_items: list[tuple[Any, ...]] = []
    for atom in atoms:
        for box_index, values in enumerate(
            atom["frozen_true_support_boxes"]
        ):
            atom_items.append((
                atom["canonical_atom_id"],
                box_index,
                atom["source_chart"],
                atom["complete_10_field_return_signature_sha256"],
                qbox(values),
                atom["Round182_leaf_row_id"],
            ))
    atom_groups: dict[
        tuple[str, str], list[tuple[Any, ...]]
    ] = collections.defaultdict(list)
    for item in atom_items:
        atom_groups[(item[2], item[3])].append(item)
    atom_trees = {
        key: IntervalNode(rows) for key, rows in atom_groups.items()
    }
    duplicate_pairs: list[tuple[str, int, str, int]] = []
    shortlist_comparisons = 0
    for item in atom_items:
        candidates: list[tuple[Any, ...]] = []
        atom_trees[(item[2], item[3])].query(
            item[4][0], item[4][1], candidates
        )
        shortlist_comparisons += len(candidates)
        for other in candidates:
            if (other[0], other[1]) <= (item[0], item[1]):
                continue
            if positive_overlap(item[4], other[4]):
                duplicate_pairs.append(
                    (item[0], item[1], other[0], other[1])
                )
    need(
        not duplicate_pairs and shortlist_comparisons == 19359760,
        "distinct-atom positive-volume overlap exhaustion",
    )

    disposition_ledger = ledger_object(
        disposition_rows,
        "Round288_atom_disposition_row_id",
        DISPOSITION_SCHEMA,
    )
    overlap_ledger = ledger_object(
        overlap_rows,
        "Round288_existing_overlap_relation_row_id",
        OVERLAP_SCHEMA,
    )
    census = {
        "source_signature_row_count": 332020,
        "canonical_atom_count": 332016,
        "precanonical_Round271_W_tail_alias_contraction_count": 4,
        "existing_Round266_occurrence_count": 126468,
        "existing_overlap_relation_count": 36680,
        "existing_Round208_alias_count": 36040,
        "newly_discovered_Round204_alias_count": 640,
        "Round204_rows_not_in_Round279_atom_universe": 96,
        "unbacked_atom_count_before_Round288": 295976,
        "conditionally_distinct_new_atom_candidate_count": 295336,
        "promotion_ready_new_candidate_count_pending_Round288_independent_verifier":
            274176,
        "isolated_new_candidate_inner_support_residual_count": 21160,
        "conditional_occurrence_total_after_only_corridor_backed_candidates":
            400644,
        "conditional_occurrence_total_if_all_inner_supports_later_pass":
            421804,
        "Round279_strict_inward_corridor_count": 661448,
        "Round279_strict_inward_corridor_incident_atom_count": 310808,
        "Round279_face_isolated_atom_count": 21208,
        "face_isolated_existing_Round208_atom_count": sum(
            row["occurrence_identity_disposition"] == EXISTING_208
            and row["canonical_atom_id"] not in canonical_corridor
            for row in disposition_rows
        ),
        "distinct_same_chart_same_signature_atom_positive_volume_overlap_pair_count":
            0,
        "pairwise_interval_shortlist_comparison_count": shortlist_comparisons,
        "source_round_histogram": {
            str(key): value for key, value in sorted(
                geometry["source_round_histogram"].items()
            )
        },
        "source_proof_class_histogram": dict(sorted(
            geometry["source_proof_histogram"].items()
        )),
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
            dict(sorted(partition_histogram.items())),
        "atom_disposition_histogram":
            dict(sorted(disposition_histogram.items())),
        "existing_overlap_relation_histogram": {
            "|".join(key): value
            for key, value in sorted(relation_histogram.items())
        },
    }
    need(census["face_isolated_existing_Round208_atom_count"] == 48, "isolated R208")
    reconstruction = {
        "census": census,
        "atom_disposition_rows_sha256":
            disposition_ledger["rows_sha256"],
        "atom_disposition_row_ids_sha256":
            disposition_ledger["row_ids_sha256"],
        "atom_disposition_row_hashes_sha256":
            disposition_ledger["row_hashes_sha256"],
        "existing_overlap_rows_sha256":
            overlap_ledger["rows_sha256"],
        "existing_overlap_row_ids_sha256":
            overlap_ledger["row_ids_sha256"],
        "existing_overlap_row_hashes_sha256":
            overlap_ledger["row_hashes_sha256"],
    }
    return disposition_ledger, overlap_ledger, reconstruction


def audit_candidate_ledgers(
    expected_dispositions: dict[str, Any],
    expected_overlaps: dict[str, Any],
) -> tuple[dict[str, Any], dict[str, Any]]:
    stored_dispositions = read_gzip_json(DISPOSITIONS)
    stored_overlaps = read_gzip_json(OVERLAPS)
    need(
        deterministic_gzip_bytes(stored_dispositions)
        == DISPOSITIONS.read_bytes(),
        "Round288 deterministic disposition gzip",
    )
    need(
        deterministic_gzip_bytes(stored_overlaps) == OVERLAPS.read_bytes(),
        "Round288 deterministic overlap gzip",
    )
    disposition_rows = verify_attachment(
        stored_dispositions,
        "Round288_atom_disposition_row_id",
        332016,
        DISPOSITION_SCHEMA,
        "Round288 dispositions",
    )
    overlap_rows = verify_attachment(
        stored_overlaps,
        "Round288_existing_overlap_relation_row_id",
        36680,
        OVERLAP_SCHEMA,
        "Round288 overlaps",
    )
    need(
        stored_dispositions["rows_sha256"]
        == expected_dispositions["rows_sha256"]
        and stored_dispositions["row_ids_sha256"]
        == expected_dispositions["row_ids_sha256"]
        and stored_dispositions["row_hashes_sha256"]
        == expected_dispositions["row_hashes_sha256"],
        "Round288 disposition ledger digest equality",
    )
    need(
        stored_overlaps["rows_sha256"]
        == expected_overlaps["rows_sha256"]
        and stored_overlaps["row_ids_sha256"]
        == expected_overlaps["row_ids_sha256"]
        and stored_overlaps["row_hashes_sha256"]
        == expected_overlaps["row_hashes_sha256"],
        "Round288 overlap ledger digest equality",
    )
    for expected, stored in zip(
        expected_dispositions["rows"], disposition_rows, strict=True
    ):
        need(
            expected == stored,
            f"Round288 disposition exact row:{expected['Round288_atom_disposition_row_id']}",
        )
    for expected, stored in zip(
        expected_overlaps["rows"], overlap_rows, strict=True
    ):
        need(
            expected == stored,
            f"Round288 overlap exact row:{expected['Round288_existing_overlap_relation_row_id']}",
        )
    return stored_dispositions, stored_overlaps


EXPECTED_STATUS = (
    "PASS_ROUND288_CACHELESS_ATOM_IDENTITY_GATE_AUDIT__"
    "640_PREVIOUSLY_UNBACKED_ROUND204_ALIASES_FOUND__"
    "274176_STRICT_CORRIDOR_INNER_SUPPORTS__"
    "21160_ISOLATED_INNER_SUPPORT_RESIDUALS__ZERO_CREDIT"
)

EXPECTED_IDENTITY_CONTRACT = {
    "ordinary_common_face_never_collapses_occurrence_identity": True,
    "same_signature_never_collapses_occurrence_identity": True,
    "true_seam_never_collapses_occurrence_identity": True,
    "Jx_Jy_never_collapses_occurrence_identity": True,
    "cross_chart_positive_open_identity_requires_explicit_reverse_rechart_alias":
        True,
    "Round284_Round286_rechart_refinement_credit_remains_zero": True,
    "the_640_Round204_aliases_preserve_existing_occurrence_ids": True,
    "reserved_candidate_ids_are_not_formal_ids": True,
}


def verify_prior_zero_credit_contracts() -> dict[str, Any]:
    round280 = closed_result(R280)
    need(
        round280["schema"]
        == "cm2.round280.source-g-expanded-occurrence-identity-contract-audit.v1"
        and round280["status"].endswith(
            "ROUND280_CLASS_AS_OCCURRENCE_SEMANTICS_REJECTED"
        )
        and round280["strict_nonpromotion"]["expanded_occurrences"] == 126468
        and round280["strict_nonpromotion"]["quotient_components"] == 63224
        and round280["strict_nonpromotion"]["new_expanded_occurrence_credit"] == 0
        and round280["strict_nonpromotion"]["occurrence_identity_collapse_credit"]
        == 0
        and round280["strict_nonpromotion"]["component_edge_credit"] == 0
        and round280["strict_nonpromotion"]["Jx_Jy_same_point_glue_credit"] == 0,
        "Round280 frozen identity/nonpromotion contract",
    )

    prior: dict[str, Any] = {"Round280": "PASS_ZERO_CREDIT_CONTRACT"}
    for round_number, filename in ((284, R284), (286, R286)):
        document = read_json(HERE / filename)
        verify_embedded_result(document, f"Round{round_number}")
        nonpromotion = document["strict_nonpromotion"]
        need(
            document["schema"].startswith(f"cm2.round{round_number}.")
            and document["status"].endswith("__ZERO_CREDIT")
            and nonpromotion["expanded_occurrences"] == 126468
            and nonpromotion["quotient"] == 63224
            and nonpromotion["occurrence_credit"] == 0
            and nonpromotion["component_credit"] == 0
            and nonpromotion["maximality_credit"] == 0
            and nonpromotion["fibre_credit"] == 0
            and nonpromotion["global_disposition_credit"] == 0
            and nonpromotion["Jx_Jy_same_point_glue_credit"] == 0
            and nonpromotion["D02"] == "BLOCKED"
            and nonpromotion["CM2"] == "NO-GO_FOR_CLAIM",
            f"Round{round_number} frozen zero-credit contract",
        )
        prior[f"Round{round_number}"] = "PASS_ZERO_CREDIT_CONTRACT"
    return prior


def audit_candidate_result(
    reconstruction: dict[str, Any],
    stored_dispositions: dict[str, Any],
    stored_overlaps: dict[str, Any],
) -> dict[str, Any]:
    document = read_json(RESULT)
    need(
        RESULT.read_bytes() == canonical(document) + b"\n",
        "Round288 canonical result bytes",
    )
    verify_embedded_result(document, "Round288 candidate")
    need(
        set(document) == {
            "schema",
            "status",
            "input_file_pins",
            "census",
            "verdict",
            "identity_contract",
            "strict_nonpromotion",
            "required_next",
            "atom_disposition_ledger",
            "existing_overlap_relation_ledger",
            "provenance",
            "result_sha256",
        },
        "Round288 candidate top-level contract",
    )
    need(
        document["schema"] == SCHEMA
        and document["status"] == EXPECTED_STATUS
        and document["input_file_pins"] == dict(sorted(INPUT_PINS.items()))
        and document["census"] == reconstruction["census"],
        "Round288 candidate schema/status/pins/census",
    )
    need(
        document["identity_contract"] == EXPECTED_IDENTITY_CONTRACT
        and document["strict_nonpromotion"] == EXPECTED_NONPROMOTION,
        "Round288 identity and nonpromotion contracts",
    )
    verdict = document["verdict"]
    need(
        set(verdict) == {
            "claim_that_all_295976_Round279_unbacked_atoms_are_new",
            "reason",
            "remaining_295336_are_disjoint_from_complete_Round266_frontier",
            "remaining_295336_are_pairwise_locally_duplicate_free",
            "corridor_backed_274176_promotion_ready_after_independent_Round288_verifier",
            "formal_promotion_now",
            "remaining_promotion_blocker",
        }
        and verdict["claim_that_all_295976_Round279_unbacked_atoms_are_new"]
        == "REJECTED"
        and verdict[
            "remaining_295336_are_disjoint_from_complete_Round266_frontier"
        ] is True
        and verdict[
            "remaining_295336_are_pairwise_locally_duplicate_free"
        ] is True
        and verdict[
            "corridor_backed_274176_promotion_ready_after_independent_Round288_verifier"
        ] is True
        and verdict["formal_promotion_now"] is False
        and "640 rows" in verdict["reason"]
        and "21,160" in verdict["remaining_promotion_blocker"],
        "Round288 verdict contract",
    )
    need(
        document["provenance"] == {
            "producer_sha256": ARTIFACT_PINS[PRODUCER.name],
            "cache_or_pickle_input_used": False,
            "source_certificates_treated_as_pinned_inert_documents": True,
            "seed_affects_output": False,
        },
        "Round288 producer provenance",
    )

    expected_disposition_metadata = {
        "filename": DISPOSITIONS.name,
        "row_count": stored_dispositions["row_count"],
        "rows_sha256": stored_dispositions["rows_sha256"],
        "row_ids_sha256": stored_dispositions["row_ids_sha256"],
        "row_hashes_sha256": stored_dispositions["row_hashes_sha256"],
        "file_sha256": ARTIFACT_PINS[DISPOSITIONS.name],
    }
    expected_overlap_metadata = {
        "filename": OVERLAPS.name,
        "row_count": stored_overlaps["row_count"],
        "rows_sha256": stored_overlaps["rows_sha256"],
        "row_ids_sha256": stored_overlaps["row_ids_sha256"],
        "row_hashes_sha256": stored_overlaps["row_hashes_sha256"],
        "file_sha256": ARTIFACT_PINS[OVERLAPS.name],
    }
    need(
        document["atom_disposition_ledger"]
        == expected_disposition_metadata
        and document["existing_overlap_relation_ledger"]
        == expected_overlap_metadata,
        "Round288 result attachment bindings",
    )
    need(
        isinstance(document["required_next"], list)
        and len(document["required_next"]) == 6
        and "standalone cacheless Round288 verifier"
        in document["required_next"][1]
        and "21,160" in document["required_next"][3]
        and "Face, true seam and Jx/Jy"
        in document["required_next"][5],
        "Round288 required-next fail-closed contract",
    )
    return {
        "candidate_schema": document["schema"],
        "candidate_status": document["status"],
        "candidate_result_sha256": document["result_sha256"],
        "candidate_file_sha256": file_sha256(RESULT),
        "candidate_census_exactly_reconstructed": True,
        "candidate_attachment_bindings_exactly_reconstructed": True,
        "candidate_nonpromotion_contract_preserved": True,
    }


def resigned_copy(
    row: dict[str, Any],
    mutation: Callable[[dict[str, Any]], None],
) -> dict[str, Any]:
    payload = deepcopy(row)
    payload.pop("row_sha256")
    mutation(payload)
    return close_row(payload)


def run_resigned_attack_tests(
    expected_dispositions: dict[str, Any],
    expected_overlaps: dict[str, Any],
) -> dict[str, Any]:
    disposition_rows = expected_dispositions["rows"]
    overlap_rows = expected_overlaps["rows"]
    by_state: dict[str, dict[str, Any]] = {}
    for row in disposition_rows:
        by_state.setdefault(row["occurrence_identity_disposition"], row)
    ready = by_state[READY]
    isolated = by_state[ISOLATED]
    existing208 = by_state[EXISTING_208]
    existing204 = by_state[EXISTING_204]
    overlap208 = next(
        row for row in overlap_rows
        if row["existing_occurrence_source"] == "ROUND208_REGION"
    )
    overlap204 = next(
        row for row in overlap_rows
        if row["existing_occurrence_source"] == "ROUND204_REGION"
    )
    disposition_expected = {
        row["Round288_atom_disposition_row_id"]: row
        for row in disposition_rows
    }
    overlap_expected = {
        row["Round288_existing_overlap_relation_row_id"]: row
        for row in overlap_rows
    }

    def accept_disposition(row: dict[str, Any]) -> None:
        validate_row(row, "resigned disposition attack")
        expected = disposition_expected.get(
            row["Round288_atom_disposition_row_id"]
        )
        need(expected is not None and row == expected, "independent disposition rebuild")

    def accept_overlap(row: dict[str, Any]) -> None:
        validate_row(row, "resigned overlap attack")
        expected = overlap_expected.get(
            row["Round288_existing_overlap_relation_row_id"]
        )
        need(expected is not None and row == expected, "independent overlap rebuild")

    attacks: list[
        tuple[
            str,
            dict[str, Any],
            Callable[[dict[str, Any]], None],
            Callable[[dict[str, Any]], None],
        ]
    ] = [
        ("ready_to_isolated", ready,
         lambda row: row.__setitem__("occurrence_identity_disposition", ISOLATED),
         accept_disposition),
        ("ready_new_credit", ready,
         lambda row: row.__setitem__("formal_new_occurrence_credit", 1),
         accept_disposition),
        ("ready_component_credit", ready,
         lambda row: row.__setitem__("formal_component_credit", 1),
         accept_disposition),
        ("ready_maximality_credit", ready,
         lambda row: row.__setitem__("formal_maximality_credit", 1),
         accept_disposition),
        ("ready_JxJy_credit", ready,
         lambda row: row.__setitem__("Jx_Jy_same_point_glue_credit", 1),
         accept_disposition),
        ("ready_corridor_removed", ready,
         lambda row: row.__setitem__("selected_Round279_strict_inner_corridor", None),
         accept_disposition),
        ("ready_corridor_box_changed", ready,
         lambda row: row["selected_Round279_strict_inner_corridor"].__setitem__(
             "exact_positive_volume_rational_inner_support_box",
             row["frozen_positive_rational_support_envelopes"][0],
         ), accept_disposition),
        ("ready_reserved_id_changed", ready,
         lambda row: row.__setitem__(
             "reserved_candidate_occurrence_id__not_issued",
             "source-g-expanded-occurrence:" + "0" * 64,
         ), accept_disposition),
        ("ready_overlap_count", ready,
         lambda row: row.__setitem__("positive_volume_existing_overlap_count", 1),
         accept_disposition),
        ("ready_source_proof", ready,
         lambda row: row.__setitem__(
             "source_proof_classes", ["ROUND208_EXISTING_POSITIVE_OPEN_REGION"]
         ), accept_disposition),
        ("ready_support_envelope", ready,
         lambda row: row.__setitem__(
             "frozen_positive_rational_support_envelopes",
             row["selected_Round279_strict_inner_corridor"][
                 "exact_positive_volume_rational_inner_support_box"
             ],
         ), accept_disposition),
        ("isolated_false_corridor", isolated,
         lambda row: row.__setitem__(
             "selected_Round279_strict_inner_corridor",
             deepcopy(ready["selected_Round279_strict_inner_corridor"]),
         ), accept_disposition),
        ("isolated_false_ready_status", isolated,
         lambda row: row.__setitem__(
             "positive_volume_rational_inner_support_status",
             "PASS_PINNED_ROUND279_DYNAMIC_STRICT_INWARD_CORRIDOR",
         ), accept_disposition),
        ("R208_existing_id_changed", existing208,
         lambda row: row.__setitem__(
             "existing_local_occurrence_row_id", "round208-forged"
         ), accept_disposition),
        ("R208_existing_source_changed", existing208,
         lambda row: row.__setitem__(
             "existing_occurrence_source", "ROUND204_REGION"
         ), accept_disposition),
        ("R204_alias_to_new", existing204,
         lambda row: row.__setitem__("occurrence_identity_disposition", READY),
         accept_disposition),
        ("R204_reserved_id_issued", existing204,
         lambda row: row.__setitem__(
             "reserved_candidate_occurrence_id__not_issued",
             "source-g-expanded-occurrence:" + "1" * 64,
         ), accept_disposition),
        ("disposition_signature_changed", ready,
         lambda row: row.__setitem__(
             "complete_10_field_return_signature_sha256", "2" * 64
         ), accept_disposition),
        ("disposition_leaf_changed", ready,
         lambda row: row.__setitem__("Round182_leaf_row_id", "round182-forged"),
         accept_disposition),
        ("disposition_owner_changed", ready,
         lambda row: row.__setitem__("owner_target", "Jx"),
         accept_disposition),
        ("overlap_relation_changed", overlap208,
         lambda row: row.__setitem__(
             "relation", "PARTIAL_POSITIVE_VOLUME_ENVELOPE_OVERLAP"
         ), accept_overlap),
        ("overlap_physical_alias_credit", overlap208,
         lambda row: row.__setitem__("physical_alias_credit", 1),
         accept_overlap),
        ("overlap_component_credit", overlap208,
         lambda row: row.__setitem__("component_credit", 1),
         accept_overlap),
        ("overlap_box_changed", overlap204,
         lambda row: row.__setitem__(
             "exact_box", list(reversed(row["exact_box"]))
         ), accept_overlap),
        ("overlap_existing_source_changed", overlap204,
         lambda row: row.__setitem__(
             "existing_occurrence_source", "ROUND208_REGION"
         ), accept_overlap),
        ("overlap_existing_id_changed", overlap204,
         lambda row: row.__setitem__(
             "existing_local_occurrence_row_id", "round204-forged"
         ), accept_overlap),
    ]
    rejected: list[str] = []
    for name, base, mutation, validator in attacks:
        attacked = resigned_copy(base, mutation)
        need(attacked != base, f"attack mutation effective:{name}")
        try:
            validator(attacked)
        except VerificationError:
            rejected.append(name)
        else:
            raise VerificationError(f"resigned attack accepted:{name}")
    need(
        len(rejected) == len(attacks) and len(rejected) >= 19,
        "all resigned attacks rejected",
    )
    return {
        "targeted_resigned_attack_count": len(attacks),
        "rejected_attack_count": len(rejected),
        "all_targeted_resigned_attacks_rejected": True,
        "rejected_attack_names": rejected,
    }


def atomic_write(path: Path, payload: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(
        dir=path.parent, prefix=path.name + ".", delete=False
    ) as handle:
        handle.write(payload)
        temporary = Path(handle.name)
    os.replace(temporary, path)


def verify(replay_seed: int, processes: int) -> dict[str, Any]:
    need(
        PRODUCER.stem not in sys.modules,
        "Round288 producer must remain unimported",
    )
    for filename, wanted in ARTIFACT_PINS.items():
        need(
            file_sha256(HERE / filename) == wanted,
            f"artifact pin:{filename}",
        )
    prior_contracts = verify_prior_zero_credit_contracts()
    geometry = load_geometry_and_sources()
    atoms, atom_by_id, _supports = reconstruct_atoms(geometry)
    existing = load_existing_occurrences(geometry)
    (
        edges,
        canonical_corridor,
        partition_histogram,
        incident_atoms,
    ) = structurally_rebind_edges(atom_by_id)
    need(
        len(atoms) - len(incident_atoms) == 21208,
        "Round279 incident/isolated atom partition",
    )
    (
        expected_dispositions,
        expected_overlaps,
        reconstruction,
    ) = reconstruct_round288_ledgers(
        atoms,
        canonical_corridor,
        existing,
        geometry,
        partition_histogram,
        replay_seed,
    )
    stored_dispositions, stored_overlaps = audit_candidate_ledgers(
        expected_dispositions, expected_overlaps
    )
    candidate_audit = audit_candidate_result(
        reconstruction, stored_dispositions, stored_overlaps
    )
    attacks = run_resigned_attack_tests(
        expected_dispositions, expected_overlaps
    )
    dynamic = dynamically_verify_all_corridors(edges, processes)

    verification = {
        "schema": VERIFICATION_SCHEMA,
        "status": (
            "PASS_INDEPENDENT_CACHELESS_ROUND288__"
            "332020_SOURCE_ROWS__332016_ATOMS__126468_EXISTING_GEOMETRIES__"
            "36680_EXACT_ALIASES__295336_DISJOINT_CANDIDATES__"
            "661448_CORRIDORS_FRESHLY_DYNAMICALLY_VERIFIED__ZERO_CREDIT"
        ),
        "artifact_pins": dict(sorted(ARTIFACT_PINS.items())),
        "independent_reconstruction": {
            **reconstruction,
            "source_rows_reconstructed": 332020,
            "canonical_atoms_reconstructed": 332016,
            "existing_occurrence_geometries_reconstructed": 126468,
            "Round279_face_edges_structurally_rebound": 330724,
            "Round279_corridors_structurally_rebound": 661448,
            "promotion_ready_new_candidate_count": 274176,
            "isolated_new_candidate_count": 21160,
            "distinct_atom_positive_volume_overlap_count": 0,
        },
        "fresh_dynamic_corridor_verification": dynamic,
        "candidate_result_audit": candidate_audit,
        "prior_round_zero_credit_contracts": prior_contracts,
        "targeted_resigned_attacks": attacks,
        "dual_seed_replay_contract": {
            "verifier_seeds": [288071, 288929],
            "PYTHONHASHSEED_values": [288071, 288929],
            "canonical_output_excludes_current_replay_seed": True,
            "required_byte_identity": True,
        },
        "provenance": {
            "Round288_producer_imported_or_executed": False,
            "cache_or_pickle_input_used": False,
            "Round279_verification_JSON_used_as_dynamic_evidence": False,
            "R174_evaluator_loaded_from_byte_pinned_source": True,
        },
        "strict_nonpromotion": EXPECTED_NONPROMOTION,
    }
    verification["verification_sha256"] = digest(verification)
    return verification


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, default=288071)
    parser.add_argument(
        "--processes",
        type=int,
        default=min(40, os.cpu_count() or 1),
    )
    parser.add_argument("--output", type=Path, default=OUTPUT)
    arguments = parser.parse_args()
    need(arguments.processes >= 1, "positive process count")
    result = verify(arguments.seed, arguments.processes)
    atomic_write(arguments.output, canonical(result) + b"\n")
    print(result["status"])
    print("verification_sha256=" + result["verification_sha256"])
    print("verification_file_sha256=" + file_sha256(arguments.output))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
