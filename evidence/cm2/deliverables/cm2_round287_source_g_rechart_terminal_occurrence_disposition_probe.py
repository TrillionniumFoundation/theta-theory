#!/usr/bin/env python3
"""Round287: terminal, but zero-credit, R275 occurrence disposition audit.

This producer deliberately separates physical support slices from the rational
outer boxes used by Round286.  In particular, every refinement cell belonging
to a Round275 REGULAR_GRAPH_CROSSING row is replayed against the frozen active
factor and the row's strict derivative signs.  A coordinate cell may therefore
be FULL, CLIPPED, or EMPTY for that particular signed region.

No occurrence ID is issued here.  Inclusion aliases remain conditional on
promotion/preservation of their containing Round279 atom, and strictly-new
support unions remain conditional candidates until an independent combined
atom/rechart verifier signs them.
"""
from __future__ import annotations

import argparse
import gzip
import hashlib
import io
import json
import os
import sys
import tempfile
from collections import Counter, defaultdict
from fractions import Fraction as Q
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import cm2_round174_source_g_unique_first_dynamic_occurrence_materialization as r174
import cm2_round179_source_g_residual_tube_arrangement as r179
import cm2_round274_source_g_reverse_rechart_tail_arrangement_probe as r274

PREFIX = "cm2_round287_source_g_rechart_terminal_occurrence_disposition_probe"
OUTPUT = HERE / f"{PREFIX}_result.json"
LEDGER = HERE / f"{PREFIX}_ledger.json.gz"

PINS = {
    "cm2_round174_source_g_unique_first_dynamic_occurrence_materialization.py":
        "3d329525dda6697a3a5d2a8227c94bd9c309ea7ebcc4cdd0c7fbe573c267a218",
    "cm2_round174_source_g_unique_first_dynamic_occurrence_materialization_rows.json":
        "9edeea2e1033b0dd70dee11a53b0f6aeb21fe74030aeefb60b081a7c420cff54",
    "cm2_round179_source_g_residual_tube_arrangement.py":
        "8c568c58d82708a7ab549f126c1fcedfccff563d1d00e3c1f7e6545b4b0d29ab",
    "cm2_round179_source_g_residual_tube_arrangement_rows.json":
        "f20b42c1fed781779b537b4d45bf44233eae1ed3ee620b95177a80f0eb2b5e42",
    "cm2_round274_source_g_reverse_rechart_tail_arrangement_probe.py":
        "677813e132d62732900a26edc3fae5d562049d8d1fac2cea59f7c65d41735292",
    "cm2_round275_source_g_complete_reverse_rechart_materialization_certificate.json":
        "e18935169614fc8b62ead3be7f60b383396ea1d2c52e8151457241f49e770386",
    "cm2_round279_source_g_collar_atom_and_face_edge_freeze_atoms.json.gz":
        "283a10799e0c7d1156695c30cdb2533488602ca646a18804f93211c0a3132dbe",
    "cm2_round280_source_g_expanded_occurrence_identity_contract_audit_result.json":
        "873974c8b343961f9e7c1674a946681749a3c0267bc57a1ccc147ccd21b3bdfc",
    "cm2_round280_source_g_true_seam_and_rechart_region_incidence_probe_region_bindings.json.gz":
        "8354eb042455e6d3ed591ee1620c9fc9def1af916a9bfbc0bf42e473e3e6e58b",
    "cm2_round283_source_g_outgoing_seam_tail_independent_probe_result.json":
        "29a1a48140136f105c2454771afa642794de10c61afc18bfbbefe88f0df70eca",
    "cm2_round283_source_g_outgoing_seam_tail_independent_probe_ledger.json.gz":
        "2643a17cd325a16fabe8508a06b8666811641f837e8c2a2ea8a4a71ab982b786",
    "cm2_round284_source_g_rechart_occurrence_overlap_contract_probe_result.json":
        "e25dd7b494ad2c2ccddc17601d28136c1919a3b16e41f008669bd6c14a513692",
    "cm2_round284_source_g_rechart_occurrence_overlap_contract_probe_ledger.json.gz":
        "39b69e0c5d249454c7ff13da99b260d3a7fabfa03c8ad6866035cbcaa883eb92",
    "cm2_round284_source_g_rechart_occurrence_overlap_contract_probe_verification.json":
        "f1b3c6f3b9ccb8525fdf29379a7369c958a80ce278f3e5afb7232f5bbd842aa6",
    "cm2_round286_source_g_partial_overlap_exact_refinement_probe_result.json":
        "a3b705c489eff9df4e1129bcdf960c6ea9de435e326c1d7e040e01d63352d29e",
    "cm2_round286_source_g_partial_overlap_exact_refinement_probe_ledger.json.gz":
        "bb7e28cbe029e2bb414313ec4a08f6366acbbad88a519926ec2a3a424e679eda",
    "cm2_round286_source_g_partial_overlap_exact_refinement_probe_verification.json":
        "817a212eeac8d855927a617dd07462747c636127e4f4b15ec709f9975a74698e",
}

ENC = json.JSONEncoder(
    sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False
)


def canonical(value: Any) -> bytes:
    return ENC.encode(value).encode()


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def fsha(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def need(condition: bool, label: str) -> None:
    if not condition:
        raise RuntimeError(label)


def qstr(value: Q) -> str:
    return str(value.numerator) if value.denominator == 1 else str(value)


def boxq(values: list[str]) -> tuple[Q, ...]:
    result = tuple(map(Q, values))
    need(len(result) == 6, "box arity")
    need(all(result[2 * i] < result[2 * i + 1] for i in range(3)), "positive box")
    return result


def square_interval(lo: Q, hi: Q) -> tuple[Q, Q]:
    need(lo * hi > 0, "strict signed t interval")
    return (lo * lo, hi * hi) if lo > 0 else (hi * hi, lo * lo)


def physical_t_square_interval(
    coordinate_box: tuple[Q, ...], guard_box: tuple[Q, ...]
) -> tuple[Q, Q]:
    cell = square_interval(coordinate_box[0], coordinate_box[1])
    source = square_interval(guard_box[0], guard_box[1])
    image = (1 - source[1], 1 - source[0])
    result = (max(cell[0], image[0]), min(cell[1], image[1]))
    need(result[0] < result[1], "positive exact physical t interval")
    return result


def signed_t_contains(
    outer: tuple[Q, ...], inner_square: tuple[Q, Q], inner_sign: int
) -> bool:
    if (1 if outer[0] > 0 else -1) != inner_sign:
        return False
    square = square_interval(outer[0], outer[1])
    return square[0] <= inner_square[0] and inner_square[1] <= square[1]


def strict_outer_contains(outer: tuple[Q, ...], inner: tuple[Q, ...]) -> bool:
    return (
        all(outer[2 * i] <= inner[2 * i] and inner[2 * i + 1] <= outer[2 * i + 1]
            for i in range(3))
        and outer != inner
    )


def closed(row: dict[str, Any]) -> dict[str, Any]:
    result = dict(row)
    need("row_sha256" not in result, "row already closed")
    result["row_sha256"] = digest(result)
    return result


def load_json(name: str) -> dict[str, Any]:
    path = HERE / name
    need(fsha(path) == PINS[name], f"pin:{name}")
    return json.loads(path.read_bytes())


def load_gzip(name: str) -> dict[str, Any]:
    path = HERE / name
    need(fsha(path) == PINS[name], f"pin:{name}")
    with gzip.open(path, "rt", encoding="utf-8") as handle:
        return json.load(handle)


def unpack(document: dict[str, Any], table: str) -> list[dict[str, Any]]:
    result = document["result"]
    columns = result["row_column_schemas"][table]
    rows = result[table]
    expected = result["table_census_and_sha256"][table]
    need(len(rows) == expected["row_count"], f"count:{table}")
    need(digest(rows) == expected["rows_sha256"], f"digest:{table}")
    return [dict(zip(columns, row, strict=True)) for row in rows]


def gzip_bytes(value: Any) -> bytes:
    target = io.BytesIO()
    with gzip.GzipFile(filename="", mode="wb", fileobj=target, mtime=0) as handle:
        handle.write(canonical(value))
    return target.getvalue()


def atomic(path: Path, payload: bytes) -> None:
    fd, temporary = tempfile.mkstemp(prefix="." + path.name + ".", dir=path.parent)
    try:
        with os.fdopen(fd, "wb") as handle:
            handle.write(payload)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def atlas_box(values: tuple[Q, ...]) -> Any:
    return r174.atlas.AtlasBox(*values, "round287-probe", None)


def signed_region_cell_state(region: dict[str, Any], values: tuple[Q, ...]) -> tuple[str, list[str]]:
    if region.get("arrangement_classification") != "REGULAR_GRAPH_CROSSING":
        return "FULL_DESIRED_SIDE_SUPPORT", []
    cell = atlas_box(values)
    signs = []
    for want_maximum in (False, True):
        point = r274.extremal_point(
            cell, region["strict_derivative_signs_t_p_s"], want_maximum
        )
        signs.append(
            r179.sign(
                r274.active_dual(
                    r179.interval_geometry(
                        region["adjacent_chart"], region["owner_target"], point
                    ),
                    region["active_reason"],
                )[0]
            )
        )
    need(all(sign in {"STRICT_NEGATIVE", "STRICT_POSITIVE"} for sign in signs),
         "strict cell extrema")
    if signs[0] != signs[1]:
        return "CLIPPED_DESIRED_SIDE_SUPPORT", signs
    if signs[0] == region["active_factor_side_sign"]:
        return "FULL_DESIRED_SIDE_SUPPORT", signs
    return "EMPTY_OPPOSITE_SIDE_COORDINATE_CELL", signs


def common_face(a: tuple[Q, ...], b: tuple[Q, ...]) -> tuple[Q, ...] | None:
    for axis in range(3):
        value = (
            a[2 * axis + 1]
            if a[2 * axis + 1] == b[2 * axis]
            else b[2 * axis + 1]
            if b[2 * axis + 1] == a[2 * axis]
            else None
        )
        if value is None:
            continue
        intervals = []
        for other in range(3):
            if other == axis:
                continue
            intervals.append(
                (
                    max(a[2 * other], b[2 * other]),
                    min(a[2 * other + 1], b[2 * other + 1]),
                )
            )
        if not all(lo < hi for lo, hi in intervals):
            continue
        result = []
        iterator = iter(intervals)
        for other in range(3):
            result.extend((value, value) if other == axis else next(iterator))
        return tuple(result)
    return None


def build() -> tuple[dict[str, Any], dict[str, Any]]:
    for name, expected in PINS.items():
        need(fsha(HERE / name) == expected, f"pin:{name}")

    r174_rows = load_json(
        "cm2_round174_source_g_unique_first_dynamic_occurrence_materialization_rows.json"
    )
    r179_rows = load_json(
        "cm2_round179_source_g_residual_tube_arrangement_rows.json"
    )
    guard_rows = unpack(r174_rows, "chart_guard_rejection_rows")
    guard_rows += unpack(r179_rows, "chart_guard_child_rows")
    need(len(guard_rows) == 880, "guard census")
    guards = {row["row_id"]: row for row in guard_rows}

    r275 = load_json(
        "cm2_round275_source_g_complete_reverse_rechart_materialization_certificate.json"
    )["result"]
    region_list = (
        r275["strict_region_ledger"]["rows"]
        + r275["arrangement_region_ledger"]["rows"]
    )
    need(len(region_list) == 13_788, "R275 region census")
    regions = {row["reverse_rechart_region_row_id"]: row for row in region_list}
    need(len(regions) == 13_788, "unique R275 regions")

    atom_payload = load_gzip(
        "cm2_round279_source_g_collar_atom_and_face_edge_freeze_atoms.json.gz"
    )
    atoms = {row["canonical_atom_id"]: row for row in atom_payload["rows"]}
    need(len(atoms) == 332_016, "R279 atom census")

    identity_contract = load_json(
        "cm2_round280_source_g_expanded_occurrence_identity_contract_audit_result.json"
    )["result"]
    need(
        identity_contract["deterministic_identity_rule"]["identity_alias_rule"].startswith(
            "Collapse identities only under an explicit exact same-positive-open-region"
        ),
        "identity contract",
    )
    bindings_payload = load_gzip(
        "cm2_round280_source_g_true_seam_and_rechart_region_incidence_probe_region_bindings.json.gz"
    )
    bindings = {
        row["Round275_reverse_rechart_region_row_id"]: row
        for row in bindings_payload["rows"]
    }
    need(len(bindings) == 13_788, "R280 binding census")

    r283 = load_json(
        "cm2_round283_source_g_outgoing_seam_tail_independent_probe_result.json"
    )
    r283_ledger = load_gzip(
        "cm2_round283_source_g_outgoing_seam_tail_independent_probe_ledger.json.gz"
    )
    need(r283["census"]["analytic_partition_child_count"] == 64, "R283 child census")
    need(r283_ledger["row_count"] == 40, "R283 endpoint census")
    need(
        r283["strict_nonpromotion"]["expanded_occurrence_credit"] == 0,
        "R283 zero occurrence credit",
    )

    r284 = load_json(
        "cm2_round284_source_g_rechart_occurrence_overlap_contract_probe_result.json"
    )
    r284_payload = load_gzip(
        "cm2_round284_source_g_rechart_occurrence_overlap_contract_probe_ledger.json.gz"
    )
    r284_rows = {row["Round275_region_id"]: row for row in r284_payload["rows"]}
    need(len(r284_rows) == 13_788, "R284 region census")
    need(
        r284["census"]["classification_histogram"]
        == {
            "CONTAINED_ALIAS_CANDIDATE__OCCURRENCE_ID_NOT_YET_ISSUED": 2476,
            "NEW_DISJOINT_CANDIDATE__OCCURRENCE_ID_NOT_YET_ISSUED": 9128,
            "PARTIAL_OVERLAP__EXACT_REFINEMENT_REQUIRED": 2184,
        },
        "R284 classification census",
    )

    r286 = load_json(
        "cm2_round286_source_g_partial_overlap_exact_refinement_probe_result.json"
    )
    r286_payload = load_gzip(
        "cm2_round286_source_g_partial_overlap_exact_refinement_probe_ledger.json.gz"
    )
    need(r286_payload["row_count"] == 7616, "R286 cell census")
    cells_by_region: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in r286_payload["rows"]:
        cells_by_region[row["Round275_region_id"]].append(row)
    need(len(cells_by_region) == 2184, "R286 parent census")

    region_boxes = {
        region_id: boxq(row["adjacent_rational_region_box"])
        for region_id, row in regions.items()
    }
    physical_square = {}
    physical_sign = {}
    for region_id, row in regions.items():
        guard = boxq(guards[row["source_guard_row_id"]]["box"])
        physical_square[region_id] = physical_t_square_interval(
            region_boxes[region_id], guard
        )
        physical_sign[region_id] = 1 if region_boxes[region_id][0] > 0 else -1

    cell_rows = []
    cell_states: dict[str, str] = {}
    cell_boxes: dict[str, tuple[Q, ...]] = {}
    cell_alias_target: dict[str, str | None] = {}
    cell_hist = Counter()
    alias_anchor_hist = Counter()
    corrected_cells_by_region: dict[str, list[dict[str, Any]]] = defaultdict(list)

    for source in r286_payload["rows"]:
        cell_id = source["Round286_refinement_cell_id"]
        region_id = source["Round275_region_id"]
        region = regions[region_id]
        values = boxq(source["cell_exact_box"])
        guard = boxq(guards[region["source_guard_row_id"]]["box"])
        cell_square = physical_t_square_interval(values, guard)
        state, extrema = signed_region_cell_state(region, values)
        occupied = source["atom_occupancy_count"] == 1
        alias_atom_id = source["unique_alias_atom_id"] if occupied else None
        alias_ok = False
        alias_status = None
        if occupied:
            need(alias_atom_id in atoms, "R286 alias atom")
            atom = atoms[alias_atom_id]
            containing = [
                boxq(box)
                for box in atom["frozen_true_support_boxes"]
                if strict_outer_contains(boxq(box), values)
            ]
            need(len(containing) == 1, "unique strict containing atom box")
            need(region["adjacent_chart"] == atom["source_chart"], "alias chart")
            need(
                region["local_return_signature"]
                == atom["complete_10_field_return_signature"],
                "alias complete signature",
            )
            need(region["owner_target"] == atom["owner_target"], "alias owner")
            need(
                signed_t_contains(containing[0], cell_square, physical_sign[region_id]),
                "alias exact physical t inclusion",
            )
            alias_ok = state != "EMPTY_OPPOSITE_SIDE_COORDINATE_CELL"
            anchors = atom["existing_Round208_occurrence_row_ids"]
            need(len(anchors) in {0, 1}, "atom anchor multiplicity")
            alias_status = (
                "PRESERVE_EXISTING_ROUND208_OCCURRENCE_ID"
                if anchors
                else "CONDITIONAL_ON_UNBACKED_ATOM_PROMOTION_OR_LATER_EXACT_ANCHOR"
            )
            alias_anchor_hist[
                ("NONEMPTY" if alias_ok else "EMPTY")
                + ("_R208_ANCHORED" if anchors else "_UNBACKED")
            ] += 1

        if state == "EMPTY_OPPOSITE_SIDE_COORDINATE_CELL":
            disposition = "EMPTY_FOR_THIS_R275_SIGNED_REGION__NO_ALIAS_OR_NEW_SUPPORT"
        elif occupied:
            disposition = (
                "EXACT_INCLUSION_ALIAS_REPRESENTATION_SUBCOVER__"
                "CONDITIONAL_ON_CONTAINING_ATOM_IDENTITY"
            )
        else:
            disposition = (
                "NONEMPTY_UNCOVERED_SLICE__MEMBER_OF_ONE_PARENT_LOCAL_NEW_SUPPORT_UNION"
            )

        row = closed(
            {
                "Round287_refinement_cell_disposition_row_id":
                    "round287-cell-disposition:" + digest(cell_id),
                "Round286_refinement_cell_id": cell_id,
                "Round275_region_id": region_id,
                "source_chart": region["source_chart"],
                "adjacent_chart": region["adjacent_chart"],
                "owner_target": region["owner_target"],
                "complete_10_field_return_signature_sha256":
                    region["complete_10_field_return_signature_sha256"],
                "coordinate_box": source["cell_exact_box"],
                "physical_t_sign": physical_sign[region_id],
                "physical_t_square_open_interval": list(map(qstr, cell_square)),
                "signed_region_cell_state": state,
                "active_factor_extremal_signs": extrema,
                "Round286_coordinate_occupancy_count": source["atom_occupancy_count"],
                "containing_atom_id": alias_atom_id,
                "exact_inclusion_alias_lemma_satisfied": alias_ok,
                "containing_atom_identity_status": alias_status,
                "disposition": disposition,
                "formal_occurrence_credit": 0,
                "formal_component_credit": 0,
                "formal_seam_credit": 0,
                "formal_maximality_credit": 0,
                "Jx_Jy_same_point_glue_credit": 0,
            }
        )
        cell_rows.append(row)
        cell_states[cell_id] = state
        cell_boxes[cell_id] = values
        cell_alias_target[cell_id] = alias_atom_id
        cell_hist[
            ("OCCUPIED" if occupied else "UNCOVERED") + "|" + state
        ] += 1
        corrected_cells_by_region[region_id].append(row)

    need(
        cell_hist
        == {
            "OCCUPIED|FULL_DESIRED_SIDE_SUPPORT": 3484,
            "OCCUPIED|CLIPPED_DESIRED_SIDE_SUPPORT": 2048,
            "OCCUPIED|EMPTY_OPPOSITE_SIDE_COORDINATE_CELL": 168,
            "UNCOVERED|FULL_DESIRED_SIDE_SUPPORT": 1108,
            "UNCOVERED|CLIPPED_DESIRED_SIDE_SUPPORT": 432,
            "UNCOVERED|EMPTY_OPPOSITE_SIDE_COORDINATE_CELL": 376,
        },
        "corrected R286 physical-side census",
    )

    union_rows = []
    union_by_region: dict[str, str] = {}
    internal_face_rows = []
    corrected_partial_hist = Counter()
    for region_id in sorted(cells_by_region):
        region = regions[region_id]
        source_cells = cells_by_region[region_id]
        nonempty_uncovered = [
            cell
            for cell in source_cells
            if cell["atom_occupancy_count"] == 0
            and cell_states[cell["Round286_refinement_cell_id"]]
            != "EMPTY_OPPOSITE_SIDE_COORDINATE_CELL"
        ]
        nonempty_alias = [
            cell
            for cell in source_cells
            if cell["atom_occupancy_count"] == 1
            and cell_states[cell["Round286_refinement_cell_id"]]
            != "EMPTY_OPPOSITE_SIDE_COORDINATE_CELL"
        ]
        empty_cells = [
            cell
            for cell in source_cells
            if cell_states[cell["Round286_refinement_cell_id"]]
            == "EMPTY_OPPOSITE_SIDE_COORDINATE_CELL"
        ]
        corrected_partial_hist[
            (
                "MIXED_WITH_ONE_NEW_SUPPORT"
                if nonempty_uncovered
                else "FULLY_COVERED_NO_NEW_SUPPORT"
            )
        ] += 1
        if not nonempty_uncovered:
            continue

        parent = list(range(len(nonempty_uncovered)))

        def find(index: int) -> int:
            while parent[index] != index:
                parent[index] = parent[parent[index]]
                index = parent[index]
            return index

        face_ids = []
        for left in range(len(nonempty_uncovered)):
            for right in range(left):
                a = nonempty_uncovered[left]
                b = nonempty_uncovered[right]
                face = common_face(
                    cell_boxes[a["Round286_refinement_cell_id"]],
                    cell_boxes[b["Round286_refinement_cell_id"]],
                )
                if face is None:
                    continue
                face_state, signs = signed_region_cell_state(region, face)
                if face_state == "EMPTY_OPPOSITE_SIDE_COORDINATE_CELL":
                    continue
                a_id = a["Round286_refinement_cell_id"]
                b_id = b["Round286_refinement_cell_id"]
                edge = closed(
                    {
                        "Round287_internal_physical_face_row_id":
                            "round287-internal-physical-face:"
                            + digest([region_id, sorted([a_id, b_id])]),
                        "Round275_region_id": region_id,
                        "left_Round286_cell_id": min(a_id, b_id),
                        "right_Round286_cell_id": max(a_id, b_id),
                        "face_box": list(map(qstr, face)),
                        "signed_region_face_state": face_state,
                        "active_factor_extremal_signs": signs,
                        "artificial_refinement_face_only": True,
                        "preserves_one_parent_local_occurrence_identity": True,
                        "formal_component_edge_credit": 0,
                    }
                )
                internal_face_rows.append(edge)
                face_ids.append(edge["Round287_internal_physical_face_row_id"])
                a_root, b_root = find(left), find(right)
                if a_root != b_root:
                    parent[b_root] = a_root

        need(
            len({find(index) for index in range(len(nonempty_uncovered))}) == 1,
            "one connected uncovered union per mixed parent",
        )
        members = sorted(
            cell["Round286_refinement_cell_id"] for cell in nonempty_uncovered
        )
        union_id = "round287-potential-new-support-union:" + digest(
            ["R286_UNCOVERED_PARENT_UNION", region_id, members]
        )
        union_by_region[region_id] = union_id
        union_rows.append(
            closed(
                {
                    "Round287_potential_new_support_union_id": union_id,
                    "source_kind": "R286_NONEMPTY_UNCOVERED_PARENT_UNION",
                    "Round275_region_id": region_id,
                    "source_chart": region["source_chart"],
                    "adjacent_chart": region["adjacent_chart"],
                    "owner_target": region["owner_target"],
                    "complete_10_field_return_signature_sha256":
                        region["complete_10_field_return_signature_sha256"],
                    "nonempty_uncovered_member_cell_count": len(members),
                    "nonempty_uncovered_member_cell_ids": members,
                    "valid_internal_physical_face_count": len(face_ids),
                    "valid_internal_physical_face_ids": sorted(face_ids),
                    "nonempty_alias_slice_count": len(nonempty_alias),
                    "empty_coordinate_cell_count": len(empty_cells),
                    "one_connected_positive_open_support": True,
                    "strictly_disjoint_from_matching_atom_supports": True,
                    "conditional_new_occurrence_count": 1,
                    "formal_occurrence_credit": 0,
                    "formal_component_credit": 0,
                    "formal_seam_credit": 0,
                }
            )
        )

    need(
        corrected_partial_hist
        == {
            "FULLY_COVERED_NO_NEW_SUPPORT": 1292,
            "MIXED_WITH_ONE_NEW_SUPPORT": 892,
        },
        "corrected partial parent census",
    )
    need(len(internal_face_rows) == 648, "valid internal physical face census")
    need(len(union_rows) == 892, "partial new union census")

    region_rows = []
    region_hist = Counter()
    contained_alias_target_atoms = set()
    for region_id in sorted(regions):
        region = regions[region_id]
        audit = r284_rows[region_id]
        classification = audit["classification"]
        alias_atom_id = None
        inclusion_alias = False
        potential_union_id = None
        if classification == "CONTAINED_ALIAS_CANDIDATE__OCCURRENCE_ID_NOT_YET_ISSUED":
            relations = [
                relation
                for relation in audit["relations"]
                if relation["relation"] == "REGION_STRICTLY_CONTAINED_IN_ATOM"
            ]
            need(len(relations) == 1, "unique contained atom")
            alias_atom_id = relations[0]["canonical_atom_id"]
            atom = atoms[alias_atom_id]
            atom_box = boxq(
                atom["frozen_true_support_boxes"][
                    relations[0]["atom_support_box_index"]
                ]
            )
            need(strict_outer_contains(atom_box, region_boxes[region_id]),
                 "strict containing region box")
            need(region["adjacent_chart"] == atom["source_chart"], "contained chart")
            need(
                region["local_return_signature"]
                == atom["complete_10_field_return_signature"],
                "contained complete signature",
            )
            need(region["owner_target"] == atom["owner_target"], "contained owner")
            need(
                signed_t_contains(
                    atom_box, physical_square[region_id], physical_sign[region_id]
                ),
                "contained exact physical t",
            )
            inclusion_alias = True
            contained_alias_target_atoms.add(alias_atom_id)
            disposition = (
                "EXACT_INCLUSION_ALIAS_REPRESENTATION_SUBCOVER__"
                "CONDITIONAL_ON_CONTAINING_ATOM_IDENTITY"
            )
        elif classification == "NEW_DISJOINT_CANDIDATE__OCCURRENCE_ID_NOT_YET_ISSUED":
            need(
                not any(
                    relation["relation"]
                    in {
                        "REGION_STRICTLY_CONTAINED_IN_ATOM",
                        "PARTIAL_POSITIVE_VOLUME_OVERLAP",
                    }
                    for relation in audit["relations"]
                ),
                "disjoint region relation",
            )
            potential_union_id = "round287-potential-new-support-union:" + digest(
                ["WHOLE_R275_REGION", region_id]
            )
            union_by_region[region_id] = potential_union_id
            union_rows.append(
                closed(
                    {
                        "Round287_potential_new_support_union_id": potential_union_id,
                        "source_kind": "WHOLE_R275_DISJOINT_REGION",
                        "Round275_region_id": region_id,
                        "source_chart": region["source_chart"],
                        "adjacent_chart": region["adjacent_chart"],
                        "owner_target": region["owner_target"],
                        "complete_10_field_return_signature_sha256":
                            region["complete_10_field_return_signature_sha256"],
                        "nonempty_uncovered_member_cell_count": 0,
                        "nonempty_uncovered_member_cell_ids": [],
                        "valid_internal_physical_face_count": 0,
                        "valid_internal_physical_face_ids": [],
                        "nonempty_alias_slice_count": 0,
                        "empty_coordinate_cell_count": 0,
                        "one_connected_positive_open_support":
                            region["connected_open_region"],
                        "strictly_disjoint_from_matching_atom_supports": True,
                        "conditional_new_occurrence_count": 1,
                        "formal_occurrence_credit": 0,
                        "formal_component_credit": 0,
                        "formal_seam_credit": 0,
                    }
                )
            )
            disposition = "ONE_STRICTLY_NEW_DISJOINT_SUPPORT_CANDIDATE__ZERO_CREDIT"
        else:
            need(
                classification == "PARTIAL_OVERLAP__EXACT_REFINEMENT_REQUIRED",
                "known R284 classification",
            )
            physical_cells = corrected_cells_by_region[region_id]
            nonempty_new = sum(
                row["Round286_coordinate_occupancy_count"] == 0
                and row["signed_region_cell_state"]
                != "EMPTY_OPPOSITE_SIDE_COORDINATE_CELL"
                for row in physical_cells
            )
            if nonempty_new:
                potential_union_id = union_by_region[region_id]
                disposition = (
                    "EXACT_REFINEMENT_MIXED__ONE_CONNECTED_STRICTLY_NEW_SUPPORT_"
                    "CANDIDATE_PLUS_INCLUSION_ALIAS_SLICES__ZERO_CREDIT"
                )
            else:
                disposition = (
                    "EXACT_REFINEMENT_PHYSICALLY_FULLY_ATOM_COVERED__"
                    "NO_PARENT_ALIAS_AND_NO_NEW_SUPPORT"
                )

        region_hist[disposition] += 1
        region_rows.append(
            closed(
                {
                    "Round287_region_disposition_row_id":
                        "round287-region-disposition:" + digest(region_id),
                    "Round275_region_id": region_id,
                    "source_guard_row_id": region["source_guard_row_id"],
                    "source_chart": region["source_chart"],
                    "adjacent_chart": region["adjacent_chart"],
                    "owner_target": region["owner_target"],
                    "complete_10_field_return_signature_sha256":
                        region["complete_10_field_return_signature_sha256"],
                    "R275_region_kind": region.get(
                        "region_classification",
                        region.get("arrangement_classification"),
                    ),
                    "physical_t_sign": physical_sign[region_id],
                    "physical_t_square_open_interval":
                        list(map(qstr, physical_square[region_id])),
                    "Round284_classification": classification,
                    "exact_inclusion_alias_lemma_satisfied": inclusion_alias,
                    "containing_atom_id": alias_atom_id,
                    "Round286_refinement_cell_count":
                        len(cells_by_region.get(region_id, [])),
                    "Round287_potential_new_support_union_id": potential_union_id,
                    "disposition": disposition,
                    "formal_occurrence_credit": 0,
                    "formal_component_credit": 0,
                    "formal_seam_credit": 0,
                    "formal_maximality_credit": 0,
                    "Jx_Jy_same_point_glue_credit": 0,
                }
            )
        )

    need(
        region_hist
        == {
            "EXACT_INCLUSION_ALIAS_REPRESENTATION_SUBCOVER__"
            "CONDITIONAL_ON_CONTAINING_ATOM_IDENTITY": 2476,
            "ONE_STRICTLY_NEW_DISJOINT_SUPPORT_CANDIDATE__ZERO_CREDIT": 9128,
            "EXACT_REFINEMENT_PHYSICALLY_FULLY_ATOM_COVERED__"
            "NO_PARENT_ALIAS_AND_NO_NEW_SUPPORT": 1292,
            "EXACT_REFINEMENT_MIXED__ONE_CONNECTED_STRICTLY_NEW_SUPPORT_"
            "CANDIDATE_PLUS_INCLUSION_ALIAS_SLICES__ZERO_CREDIT": 892,
        },
        "terminal region disposition census",
    )
    need(len(union_rows) == 10_020, "total conditional new support census")

    # Exhaust every possible positive-volume overlap of R275 rational cover
    # boxes after imposing the exact algebraic t image interval.  The only
    # survivors must be the two mutually exclusive sides of one certified
    # regular graph cell.
    overlap_pairs = []
    by_chart: dict[str, list[tuple[tuple[Q, ...], dict[str, Any]]]] = defaultdict(list)
    for region_id, region in regions.items():
        by_chart[region["adjacent_chart"]].append((region_boxes[region_id], region))
    for chart in sorted(by_chart):
        candidates = sorted(by_chart[chart], key=lambda item: item[0][0])
        for left_index, (a, left) in enumerate(candidates):
            left_id = left["reverse_rechart_region_row_id"]
            for b, right in candidates[left_index + 1 :]:
                if b[0] >= a[1]:
                    break
                right_id = right["reverse_rechart_region_row_id"]
                if not (
                    max(physical_square[left_id][0], physical_square[right_id][0])
                    < min(physical_square[left_id][1], physical_square[right_id][1])
                    and max(a[2], b[2]) < min(a[3], b[3])
                    and max(a[4], b[4]) < min(a[5], b[5])
                ):
                    continue
                need(
                    left.get("arrangement_classification")
                    == right.get("arrangement_classification")
                    == "REGULAR_GRAPH_CROSSING",
                    "only graph-side outer overlap",
                )
                need(left["source_guard_row_id"] == right["source_guard_row_id"],
                     "same graph guard")
                need(a == b, "same graph cell outer box")
                need(left["active_reason"] == right["active_reason"], "same graph reason")
                need(
                    {left["active_factor_side_sign"], right["active_factor_side_sign"]}
                    == {"STRICT_NEGATIVE", "STRICT_POSITIVE"},
                    "opposite graph sides",
                )
                need(
                    left["complete_10_field_return_signature_sha256"]
                    != right["complete_10_field_return_signature_sha256"],
                    "opposite graph signatures",
                )
                overlap_pairs.append(
                    closed(
                        {
                            "Round287_mutually_exclusive_outer_overlap_pair_row_id":
                                "round287-mutually-exclusive-pair:"
                                + digest(sorted([left_id, right_id])),
                            "left_Round275_region_id": min(left_id, right_id),
                            "right_Round275_region_id": max(left_id, right_id),
                            "adjacent_chart": chart,
                            "source_guard_row_id": left["source_guard_row_id"],
                            "active_reason": left["active_reason"],
                            "active_factor_side_signs": sorted(
                                [
                                    left["active_factor_side_sign"],
                                    right["active_factor_side_sign"],
                                ]
                            ),
                            "exact_positive_physical_overlap": False,
                            "reason":
                                "SAME_REGULAR_GRAPH_CELL_OPPOSITE_OPEN_FACTOR_SIDES",
                            "occurrence_identity_collapse_credit": 0,
                            "component_edge_credit": 0,
                        }
                    )
                )
    need(len(overlap_pairs) == 3488, "R275 outer-overlap pair census")

    for rows, id_field in (
        (region_rows, "Round287_region_disposition_row_id"),
        (cell_rows, "Round287_refinement_cell_disposition_row_id"),
        (union_rows, "Round287_potential_new_support_union_id"),
        (internal_face_rows, "Round287_internal_physical_face_row_id"),
        (overlap_pairs, "Round287_mutually_exclusive_outer_overlap_pair_row_id"),
    ):
        rows.sort(key=lambda row: row[id_field])
        ids = [row[id_field] for row in rows]
        need(len(ids) == len(set(ids)), f"unique ids:{id_field}")

    ledger = {
        "schema": "cm2.round287.source-g-rechart-terminal-occurrence-disposition.ledger.v1",
        "region_row_count": len(region_rows),
        "region_rows_sha256": digest(region_rows),
        "region_rows": region_rows,
        "refinement_cell_row_count": len(cell_rows),
        "refinement_cell_rows_sha256": digest(cell_rows),
        "refinement_cell_rows": cell_rows,
        "potential_new_support_union_row_count": len(union_rows),
        "potential_new_support_union_rows_sha256": digest(union_rows),
        "potential_new_support_union_rows": union_rows,
        "valid_internal_physical_face_row_count": len(internal_face_rows),
        "valid_internal_physical_face_rows_sha256": digest(internal_face_rows),
        "valid_internal_physical_face_rows": internal_face_rows,
        "mutually_exclusive_outer_overlap_pair_row_count": len(overlap_pairs),
        "mutually_exclusive_outer_overlap_pair_rows_sha256": digest(overlap_pairs),
        "mutually_exclusive_outer_overlap_pair_rows": overlap_pairs,
    }

    nonempty_alias_count = sum(
        row["exact_inclusion_alias_lemma_satisfied"] for row in cell_rows
    )
    need(nonempty_alias_count == 5532, "nonempty refined alias census")
    empty_count = sum(
        row["signed_region_cell_state"]
        == "EMPTY_OPPOSITE_SIDE_COORDINATE_CELL"
        for row in cell_rows
    )
    need(empty_count == 544, "empty refinement cell census")

    result = {
        "schema": "cm2.round287.source-g-rechart-terminal-occurrence-disposition-probe.v1",
        "status":
            "PASS_ROUND287_PHYSICAL_SIDE_CORRECTED_TERMINAL_DISPOSITION_CONTRACT__"
            "10020_CONDITIONAL_NEW_SUPPORTS__ZERO_CREDIT",
        "pins": PINS,
        "census": {
            "Round275_region_count": len(region_rows),
            "Round286_coordinate_refinement_cell_count": len(cell_rows),
            "Round284_contained_region_inclusion_alias_witness_count": 2476,
            "Round286_nonempty_inclusion_alias_slice_count": nonempty_alias_count,
            "Round286_empty_opposite_side_coordinate_cell_count": empty_count,
            "Round286_nonempty_uncovered_slice_count": 1540,
            "Round286_physically_fully_atom_covered_parent_count": 1292,
            "Round286_mixed_parent_count": 892,
            "valid_internal_artificial_physical_face_count": len(internal_face_rows),
            "connected_new_support_union_from_partial_parents": 892,
            "whole_Round275_disjoint_new_support_candidate_count": 9128,
            "total_conditional_new_Round275_support_count": len(union_rows),
            "R275_pairwise_outer_positive_overlap_pair_count": len(overlap_pairs),
            "R275_pairwise_actual_positive_overlap_pair_count": 0,
            "R283_logical_analytic_child_count_not_occurrence_nodes": 64,
            "cell_state_histogram": dict(sorted(cell_hist.items())),
            "region_disposition_histogram": dict(sorted(region_hist.items())),
            "alias_anchor_histogram": dict(sorted(alias_anchor_hist.items())),
            "contained_alias_target_unique_atom_count":
                len(contained_alias_target_atoms),
        },
        "inclusion_alias_lemma": {
            "name": "EXACT_SAME_POSITIVE_OPEN_REGION_INCLUSION_ALIAS_V1",
            "rule":
                "If a nonempty R275 signed open support or R286 signed support slice "
                "is strictly included in one certified connected positive-open "
                "Round279 atom support under the same physical chart coordinates, "
                "and the complete ten-field signature, exact key, and owner agree, "
                "the smaller row is an exact representation-subcover witness for "
                "that atom occurrence identity and receives no new occurrence ID.",
            "box_containment_alone_is_never_sufficient": True,
            "signature_only_is_never_sufficient": True,
            "face_only_is_never_sufficient": True,
            "partial_overlap_is_never_sufficient": True,
            "does_not_collapse_two_existing_occurrence_ids": True,
            "conditional_on_containing_atom_identity_being_preserved_or_promoted": True,
        },
        "physical_side_correction": {
            "Round286_coordinate_cells_do_not_by_themselves_prove_signed_support": True,
            "active_factor_extrema_replayed_for_every_graph_parent_cell": True,
            "coordinate_empty_rows_removed_from_alias_and_new_support_censuses": 544,
            "old_coordinate_uncovered_count": 1916,
            "corrected_nonempty_uncovered_count": 1540,
            "old_coordinate_mixed_parent_count": 1224,
            "corrected_physical_mixed_parent_count": 892,
            "old_coordinate_internal_face_count": 692,
            "corrected_valid_physical_internal_face_count": 648,
        },
        "pairwise_uniqueness_contract": {
            "all_R275_outer_positive_overlap_pairs_exhausted": True,
            "only_opposite_sides_of_one_regular_graph_cell_survive_outer_test": True,
            "opposite_factor_sides_are_physically_disjoint": True,
            "no_cross_guard_or_return_branch_positive_volume_duplicate_found": True,
            "nonmatching_strict_complete_signatures_exclude_physical_open_overlap": True,
        },
        "Round283_nonoccurrence_guard": {
            "logical_children": 64,
            "materialized_child_identity_ledger_present": False,
            "children_may_overlap_across_return_branches": True,
            "children_are_only_refinement_witnesses_to_be_bound_to_R275_regions": True,
            "occurrence_credit": 0,
        },
        "Round288_dependency": {
            "Round288_artifact_pinned_here": False,
            "reported_additional_R204_exact_atom_alias_count": 640,
            "reported_conditional_new_Round279_atom_count": 295336,
            "reported_combined_conditional_expanded_occurrence_total_if_Round288_freezes":
                431824,
            "arithmetic_is_informational_and_not_credited": True,
        },
        "issuance_blockers": [
            "Freeze and pin the Round288 atom-to-existing-occurrence correction.",
            "Promote or preserve every containing Round279 atom identity, then map all inclusion aliases.",
            "Have an independent verifier reconstruct all 544 empty, 5532 alias, 1540 uncovered, 648 face, 892 union, and 3488 mutually-exclusive-pair rows.",
            "Bind the 64 Round283 logical children only as refinement witnesses; never issue occurrence IDs for them.",
            "Only then issue deterministic IDs for the 10020 strictly-new support unions and rebuild the seam/component DSU.",
        ],
        "strict_nonpromotion": {
            "new_expanded_occurrence_credit": 0,
            "occurrence_identity_collapse_credit": 0,
            "component_edge_credit": 0,
            "seam_edge_credit": 0,
            "maximality_credit": 0,
            "fibre_credit": 0,
            "global_disposition_credit": 0,
            "Jx_Jy_same_point_glue_credit": 0,
            "expanded_occurrences": 126468,
            "quotient": 63224,
            "Gate5": "10/18",
            "D02": "BLOCKED",
            "CM2": "NO-GO_FOR_CLAIM",
        },
        "ledger": {
            "filename": LEDGER.name,
            "region_row_count": len(region_rows),
            "refinement_cell_row_count": len(cell_rows),
            "potential_new_support_union_row_count": len(union_rows),
            "valid_internal_physical_face_row_count": len(internal_face_rows),
            "mutually_exclusive_outer_overlap_pair_row_count": len(overlap_pairs),
            "ledger_object_sha256": digest(ledger),
        },
    }
    return ledger, result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=OUTPUT)
    parser.add_argument("--ledger", type=Path, default=LEDGER)
    parser.add_argument("--seed", type=int, default=287071)
    args = parser.parse_args()
    need(args.seed >= 0, "nonnegative seed")
    ledger, result = build()
    ledger_payload = gzip_bytes(ledger)
    result["ledger"]["file_sha256"] = hashlib.sha256(ledger_payload).hexdigest()
    result["result_sha256"] = digest(result)
    atomic(args.ledger.resolve(), ledger_payload)
    atomic(args.output.resolve(), canonical(result) + b"\n")
    print(
        json.dumps(
            {
                "status": result["status"],
                "result_sha256": result["result_sha256"],
                "conditional_new_supports":
                    result["census"]["total_conditional_new_Round275_support_count"],
                "empty_cells":
                    result["census"]["Round286_empty_opposite_side_coordinate_cell_count"],
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
