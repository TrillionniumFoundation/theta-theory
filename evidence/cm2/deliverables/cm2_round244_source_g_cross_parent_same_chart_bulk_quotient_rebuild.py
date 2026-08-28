#!/usr/bin/env python3
"""Reconcile the Round220 cross-parent pool and rebuild the source-G quotient.

Round226 correctly closed the 9,830 rows as an *event-sheet* channel.  This
round adds a different proof for exactly 328 rows: both endpoint faces use the
same parent-independent global source chart, the same chart embedding, the
same target lift, an exact positive-area common refinement, and the same
closed ten-field return signature.  The other 9,502 rows remain fail-closed.
"""

from __future__ import annotations

import argparse
import ast
from collections import Counter, defaultdict
from fractions import Fraction as Q
import hashlib
import json
import os
from pathlib import Path
import re
import stat
import tempfile
from typing import Any


HERE = Path(__file__).resolve().parent
OUTPUT = (
    HERE
    / "cm2_round244_source_g_cross_parent_same_chart_bulk_quotient_rebuild_certificate.json"
)
SCHEMA = (
    "cm2.round244.source-g-cross-parent-same-chart-bulk-quotient-rebuild.v1"
)
AXES = ("t", "p", "s")
PINS = {
    "cm2_gate3_eight_cell_symmetry_atlas_cert.py":
        "d867f5cb03691289033d1a0d0e277a03e8395d70aae7e0689446d7aa63eac3da",
    "cm2_round173_source_g_exact_return_signature_transport_certificate.json":
        "5ff82c5822f543109da0d50c0637d0d2f9148a738b1a21b16878c70e5505cf1a",
    "cm2_round174_source_g_unique_first_dynamic_occurrence_materialization_rows.json":
        "9edeea2e1033b0dd70dee11a53b0f6aeb21fe74030aeefb60b081a7c420cff54",
    "cm2_round179_source_g_residual_tube_arrangement_rows.json":
        "f20b42c1fed781779b537b4d45bf44233eae1ed3ee620b95177a80f0eb2b5e42",
    "cm2_round220_source_g_round179_resolved_child_boundary_atlas_certificate.json":
        "569a7849b53805ff4deca0eff9a6938a897942d3d682dfef27c27559135ce974",
    "cm2_round226_source_g_chart_transition_contract_census_certificate.json":
        "226e1f350c53fe4d7357ba9a74850e21d5aee5d720c0ea714c460181a6c797e8",
    "cm2_round243_source_g_exact_event_trace_bulk_quotient_rebuild_certificate.json":
        "8d0ca0f887a0b10f7535cc6d632ddcf4599231c882a87fb5a77875e54380a86d",
}
ACCEPTED_CANDIDATE_IDS_SHA256 = (
    "08bfc67e5519fb4a74bf7effe76b5e87d0c682349f5b01ddf9fdef86b804aaa1"
)
ACCEPTED_CANDIDATE_TRIPLETS_SHA256 = (
    "99c1400f7e0d648916778783fadfdba4fe0a2c4b78f5be2014cf608ab777ea2b"
)


def need(value: bool, label: str) -> None:
    if not value:
        raise RuntimeError(label)


def canonical(value: Any) -> bytes:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    ).encode()


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def qstr(value: Q) -> str:
    return (
        str(value.numerator)
        if value.denominator == 1
        else f"{value.numerator}/{value.denominator}"
    )


def read_pinned(name: str, maximum: int = 400_000_000) -> bytes:
    path = HERE / name
    info = path.lstat()
    need(
        stat.S_ISREG(info.st_mode)
        and not path.is_symlink()
        and info.st_nlink == 1
        and 0 < info.st_size <= maximum,
        f"regular:{name}",
    )
    raw = path.read_bytes()
    need(hashlib.sha256(raw).hexdigest() == PINS[name], f"pin:{name}")
    return raw


def load_result(name: str) -> dict[str, Any]:
    document = json.loads(read_pinned(name))
    need(
        set(document) == {"schema", "result", "result_sha256"}
        and digest(document["result"]) == document["result_sha256"],
        f"envelope:{name}",
    )
    return document["result"]


def unpack(value: dict[str, Any]) -> list[dict[str, Any]]:
    columns = value["columns"]
    rows = [
        dict(zip(columns, packed, strict=True))
        for packed in value["rows"]
    ]
    need(value["row_count"] == len(rows), "packed table count")
    return rows


def unpack_rows(
    document: dict[str, Any],
    table: str,
) -> list[dict[str, Any]]:
    columns = document["row_column_schemas"][table]
    return [
        dict(zip(columns, packed, strict=True))
        for packed in document[table]
    ]


def closed(row: dict[str, Any]) -> dict[str, Any]:
    result = dict(row)
    result["row_sha256"] = digest(result)
    return result


def ledger(rows: list[dict[str, Any]], id_field: str) -> dict[str, Any]:
    need(
        len(rows) == len({row[id_field] for row in rows}),
        f"unique:{id_field}",
    )
    return {
        "row_count": len(rows),
        "rows_sha256": digest(rows),
        "row_ids_sha256": digest([row[id_field] for row in rows]),
        "row_hashes_sha256": digest([row["row_sha256"] for row in rows]),
        "every_row_closed_by_own_SHA256": True,
        "rows": rows,
    }


def return_signature(row: dict[str, Any]) -> dict[str, Any]:
    return {
        "source_chart": row["chart"],
        "target_lift": row["owner_target"],
        "ordered_integer_wall_events":
            row["ordered_integer_wall_events"],
        "signed_wall_word": row["signed_wall_word"],
        "roof": row["roof"],
        "outgoing_cell": row["outgoing_cell"],
        "target_chart": row["target_chart"],
        "official_key_row": row["official_key_row"],
        "official_key_ordinal": row["official_key_ordinal"],
        "official_key_id": row["official_key_id"],
    }


def box_values(box: list[str]) -> tuple[Q, ...]:
    values = tuple(Q(value) for value in box)
    need(
        len(values) == 6
        and values[0] < values[1]
        and values[2] < values[3]
        and values[4] < values[5],
        "positive box",
    )
    return values


def rect_values(rect: list[str]) -> tuple[Q, Q, Q, Q]:
    values = tuple(Q(value) for value in rect)
    need(
        len(values) == 4
        and values[0] < values[1]
        and values[2] < values[3],
        "positive rectangle",
    )
    return values  # type: ignore[return-value]


def face_region(face: dict[str, Any]) -> dict[str, tuple[Q, Q]]:
    fixed = Q(face["fixed_coordinate"])
    result = {face["axis"]: (fixed, fixed)}
    rectangle = rect_values(face["tangential_half_open_box"])
    for index, axis in enumerate(face["tangential_axes"]):
        result[axis] = (
            rectangle[2 * index],
            rectangle[2 * index + 1],
        )
    need(set(result) == set(AXES), "complete face region")
    return result


def rectangle_subset_of_parent_face(
    rectangle: tuple[Q, Q, Q, Q],
    parent_box: tuple[Q, ...],
    axis_index: int,
) -> bool:
    tangential = [index for index in range(3) if index != axis_index]
    return (
        parent_box[2 * tangential[0]] <= rectangle[0]
        < rectangle[1] <= parent_box[2 * tangential[0] + 1]
        and parent_box[2 * tangential[1]] <= rectangle[2]
        < rectangle[3] <= parent_box[2 * tangential[1] + 1]
    )


def negate_interval(value: tuple[Q, Q]) -> tuple[Q, Q]:
    return (-value[1], -value[0])


JX = {"G:E": "G:W", "G:W": "G:E", "G:N": "G:N", "G:S": "G:S"}
JY = {"G:E": "G:E", "G:W": "G:W", "G:N": "G:S", "G:S": "G:N"}


def transition_kind(source: str, destination: str) -> str:
    if source == destination:
        return "IDENTITY"
    if JX[source] == destination:
        return "Jx"
    if JY[source] == destination:
        return "Jy"
    if JX[JY[source]] == destination:
        return "JxJy"
    return "NO_PINNED_KLEIN_GENERATOR"


def transformed_region(
    source: str,
    destination: str,
    face: dict[str, Any],
) -> dict[str, tuple[Q, Q]] | None:
    region = face_region(face)
    kind = transition_kind(source, destination)
    if kind == "IDENTITY":
        return region
    if kind == "Jx":
        region["p"] = negate_interval(region["p"])
        region["s"] = negate_interval(region["s"])
        return region
    if kind == "Jy":
        region["p"] = negate_interval(region["p"])
        return region
    if kind == "JxJy":
        region["s"] = negate_interval(region["s"])
        return region
    return None


class DisjointSet:
    def __init__(self, values: list[str]) -> None:
        self.parent = {value: value for value in values}

    def find(self, value: str) -> str:
        parent = self.parent[value]
        while parent != self.parent[parent]:
            self.parent[parent] = self.parent[self.parent[parent]]
            parent = self.parent[parent]
        while value != parent:
            following = self.parent[value]
            self.parent[value] = parent
            value = following
        return parent

    def union(self, left: str, right: str) -> None:
        left_root = self.find(left)
        right_root = self.find(right)
        if left_root == right_root:
            return
        low, high = sorted([left_root, right_root])
        self.parent[high] = low


def safe_write(raw: bytes) -> None:
    descriptor, name = tempfile.mkstemp(
        prefix=".round244.",
        suffix=".tmp",
        dir=HERE,
    )
    temporary = Path(name)
    try:
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(raw)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, OUTPUT)
    finally:
        if temporary.exists():
            temporary.unlink()


def chart_geometry_contract() -> dict[str, Any]:
    raw = read_pinned(
        "cm2_gate3_eight_cell_symmetry_atlas_cert.py",
        5_000_000,
    )
    tree = ast.parse(raw.decode())
    functions = {
        node.name: node
        for node in tree.body
        if isinstance(node, ast.FunctionDef)
    }
    geometry = functions["geometry"]
    arguments = [argument.arg for argument in geometry.args.args]
    names = {
        node.id for node in ast.walk(geometry)
        if isinstance(node, ast.Name)
    }
    need(
        arguments == ["chart_id", "box"]
        and "parent_id" not in names
        and {"chart_id", "box"} <= names,
        "parent-independent global chart geometry",
    )
    return {
        "pinned_geometry_source_sha256":
            PINS["cm2_gate3_eight_cell_symmetry_atlas_cert.py"],
        "geometry_function_arguments": arguments,
        "parent_id_absent_from_geometry_function": True,
        "same_chart_same_t_p_s_has_identity_physical_embedding": True,
    }


def build() -> dict[str, Any]:
    for name in PINS:
        read_pinned(
            name,
            5_000_000 if name.endswith(".py") else 400_000_000,
        )
    geometry_contract = chart_geometry_contract()

    round173 = load_result(
        "cm2_round173_source_g_exact_return_signature_transport_certificate.json"
    )
    generators = {
        row["generator"]: row
        for row in round173["exact_transport_generators"]
    }
    need(
        generators["Jx"]["physical_reflection"]
        == "(x,y,s,p)->(-x,y,-s,-p)"
        and generators["Jy"]["physical_reflection"]
        == "(x,y,s,p)->(x,-y,s,-p)",
        "Klein maps are physical symmetries",
    )

    round174 = load_result(
        "cm2_round174_source_g_unique_first_dynamic_occurrence_materialization_rows.json"
    )
    parents = {
        row["parent_id"]: row
        for row in unpack_rows(round174, "parent_rows")
    }
    need(len(parents) == 21_232, "Round174 parent count")

    round179 = load_result(
        "cm2_round179_source_g_residual_tube_arrangement_rows.json"
    )
    resolved = {
        row["row_id"]: row
        for row in unpack_rows(round179, "resolved_3d_child_rows")
    }
    need(len(resolved) == 17_192, "Round179 resolved count")

    round220 = load_result(
        "cm2_round220_source_g_round179_resolved_child_boundary_atlas_certificate.json"
    )
    tables = round220["coordinate_boundary_atlas"]["tables"]
    atlas_children = unpack(tables["resolved_child_rows"])
    faces = {
        row["face_id"]: row
        for row in unpack(tables["coordinate_face_rows"])
    }
    candidates = unpack(
        tables["rejected_exact_coordinate_coincidence_rows"]
    )
    need(
        len(atlas_children) == 17_192
        and len(faces) == 103_152
        and len(candidates) == 9_830,
        "Round220 pool census",
    )

    round226 = load_result(
        "cm2_round226_source_g_chart_transition_contract_census_certificate.json"
    )
    need(
        round226["census"]["transformed_face_candidate_count"] == 9_830
        and round226["census"][
            "event_trace_candidate_absence_proved_within_Round220_rejected_pool_count"
        ] == 9_830
        and round226["census"]["physical_glue_credit_count"] == 0,
        "Round226 event-sheet closure binding",
    )

    reconciliation_rows: list[dict[str, Any]] = []
    accepted_edges: list[dict[str, Any]] = []
    accepted_triplets: list[list[str]] = []
    accepted_source_ids: list[str] = []
    accepted_axis_histogram: Counter[str] = Counter()
    accepted_chart_histogram: Counter[str] = Counter()
    accepted_area_histogram: Counter[str] = Counter()
    accepted_key_ordinals: set[int] = set()
    transport_lineage_histogram: Counter[str] = Counter()
    parent_common_refinement_histogram: Counter[str] = Counter()
    rejected_disposition_histogram: Counter[str] = Counter()
    minimum_source_chart_margin: Q | None = None
    minimum_direction_margin: Q | None = None
    minimum_cross_chart_source_margin: Q | None = None

    for candidate in sorted(
        candidates,
        key=lambda row: row["candidate_id"],
    ):
        negative_face = faces[candidate["negative_side_face_id"]]
        positive_face = faces[candidate["positive_side_face_id"]]
        negative_atlas = atlas_children[negative_face["child_ordinal"]]
        positive_atlas = atlas_children[positive_face["child_ordinal"]]
        negative = resolved[negative_atlas["source_child_row_id"]]
        positive = resolved[positive_atlas["source_child_row_id"]]
        negative_parent = parents[candidate["negative_parent_id"]]
        positive_parent = parents[candidate["positive_parent_id"]]
        negative_signature = return_signature(negative)
        positive_signature = return_signature(positive)
        signature_equal = negative_signature == positive_signature
        common_rectangle = rect_values(
            candidate["coincident_half_open_box"]
        )
        area = (
            (common_rectangle[1] - common_rectangle[0])
            * (common_rectangle[3] - common_rectangle[2])
        )
        need(area > 0, f"positive candidate area:{candidate['candidate_id']}")
        need(
            negative_face["event_sheet_incidence_count"] == 0
            and positive_face["event_sheet_incidence_count"] == 0
            and negative_atlas["event_sheet_incidence_count"] == 0
            and positive_atlas["event_sheet_incidence_count"] == 0
            and negative_face["coordinate_stratum_only"] is True
            and positive_face["coordinate_stratum_only"] is True,
            f"Round226 event-sheet absence:{candidate['candidate_id']}",
        )
        common = {
            "Round220_candidate_id": candidate["candidate_id"],
            "negative_side_child_row_id": negative["row_id"],
            "positive_side_child_row_id": positive["row_id"],
            "negative_side_face_id": negative_face["face_id"],
            "positive_side_face_id": positive_face["face_id"],
            "negative_parent_id": candidate["negative_parent_id"],
            "positive_parent_id": candidate["positive_parent_id"],
            "negative_chart": candidate["negative_chart"],
            "positive_chart": candidate["positive_chart"],
            "axis": candidate["axis"],
            "fixed_coordinate": candidate["fixed_coordinate"],
            "common_refinement_half_open_box":
                candidate["coincident_half_open_box"],
            "exact_positive_area": qstr(area),
            "same_chart": candidate["same_chart"],
            "same_official_key": candidate["same_official_key"],
            "raw_exact_10_field_signature_equal": signature_equal,
            "both_endpoint_faces_coordinate_stratum_only": True,
            "both_endpoint_faces_event_sheet_incidence_zero": True,
        }

        if candidate["same_chart"]:
            need(
                candidate["same_official_key"]
                and signature_equal
                and negative["chart"] == positive["chart"]
                == candidate["negative_chart"]
                == candidate["positive_chart"]
                and negative["owner_target"] == positive["owner_target"]
                == negative_parent["owner_target"]
                == positive_parent["owner_target"],
                f"same-chart signature contract:{candidate['candidate_id']}",
            )
            need(
                negative_face["side"] == "UPPER"
                and positive_face["side"] == "LOWER"
                and negative_face["half_open_incidence_status"]
                == "EXCLUDED_UPPER_FIXED_COORDINATE"
                and positive_face["half_open_incidence_status"]
                == "INCLUDED_LOWER_FIXED_COORDINATE"
                and negative_face["fixed_coordinate"]
                == positive_face["fixed_coordinate"]
                == candidate["fixed_coordinate"]
                and negative_face["tangential_half_open_box"]
                == positive_face["tangential_half_open_box"]
                == candidate["coincident_half_open_box"],
                f"exact child face identity:{candidate['candidate_id']}",
            )
            need(
                candidate["negative_parent_id"]
                != candidate["positive_parent_id"]
                and negative_parent["chart"] == positive_parent["chart"]
                == negative["chart"]
                and negative_parent["transport_generator"]
                == positive_parent["transport_generator"],
                f"shared global chart lineage:{candidate['candidate_id']}",
            )
            axis_index = AXES.index(candidate["axis"])
            negative_parent_box = box_values(negative_parent["box"])
            positive_parent_box = box_values(positive_parent["box"])
            fixed = Q(candidate["fixed_coordinate"])
            need(
                negative_parent_box[2 * axis_index + 1] == fixed
                == positive_parent_box[2 * axis_index]
                and rectangle_subset_of_parent_face(
                    common_rectangle,
                    negative_parent_box,
                    axis_index,
                )
                and rectangle_subset_of_parent_face(
                    common_rectangle,
                    positive_parent_box,
                    axis_index,
                ),
                f"parent-face common refinement:{candidate['candidate_id']}",
            )
            tangential = [
                index for index in range(3) if index != axis_index
            ]
            negative_parent_rectangle = (
                negative_parent_box[2 * tangential[0]],
                negative_parent_box[2 * tangential[0] + 1],
                negative_parent_box[2 * tangential[1]],
                negative_parent_box[2 * tangential[1] + 1],
            )
            positive_parent_rectangle = (
                positive_parent_box[2 * tangential[0]],
                positive_parent_box[2 * tangential[0] + 1],
                positive_parent_box[2 * tangential[1]],
                positive_parent_box[2 * tangential[1] + 1],
            )
            parent_relation = (
                "EXACT_PARENT_TANGENTIAL_RECTANGLE"
                if negative_parent_rectangle
                == positive_parent_rectangle
                else
                "POSITIVE_AREA_PARENT_COMMON_REFINEMENT_T_JUNCTION"
            )
            region = face_region(negative_face)
            t_margin = Q(1) - 2 * max(
                region["t"][0] ** 2,
                region["t"][1] ** 2,
            )
            p_margin = Q(1) - max(
                region["p"][0] ** 2,
                region["p"][1] ** 2,
            )
            need(
                t_margin > 0 and p_margin > 0,
                f"physical chart interior:{candidate['candidate_id']}",
            )
            minimum_source_chart_margin = (
                t_margin
                if minimum_source_chart_margin is None
                else min(minimum_source_chart_margin, t_margin)
            )
            minimum_direction_margin = (
                p_margin
                if minimum_direction_margin is None
                else min(minimum_direction_margin, p_margin)
            )
            lineage = (
                negative_parent["transport_generator"] or "DIRECT"
            )
            edge = closed({
                "cross_parent_bulk_edge_row_id":
                    "round244-cross-parent-same-chart-bulk-edge:"
                    + digest(candidate["candidate_id"]),
                **common,
                "full_return_signature": negative_signature,
                "full_return_signature_sha256":
                    digest(negative_signature),
                "negative_parent_transport_generator":
                    negative_parent["transport_generator"],
                "positive_parent_transport_generator":
                    positive_parent["transport_generator"],
                "parent_transport_lineage": lineage,
                "global_chart_embedding":
                    "PHI_SOURCE_CHART(chart,t,p,s)",
                "global_chart_embedding_is_parent_independent": True,
                "explicit_coordinate_transition":
                    "IDENTITY_ON_GLOBAL_SOURCE_CHART",
                "resolved_child_faces_exact_equal": True,
                "positive_area_parent_face_common_refinement": True,
                "parent_common_refinement_relation": parent_relation,
                "strictly_inside_source_chart_seam":
                    t_margin > 0,
                "strictly_inside_direction_grazing_boundary":
                    p_margin > 0,
                "source_chart_interior_margin": qstr(t_margin),
                "direction_interior_margin": qstr(p_margin),
                "half_open_owner_unique": True,
                "accepted_from_box_touch_or_key_equality_alone": False,
                "new_evidence_beyond_Round226":
                    "PARENT_INDEPENDENT_GLOBAL_CHART_EMBEDDING_PLUS_"
                    "EXACT_10_FIELD_CLOSED_FACE_RESTRICTION",
                "current_quotient_lower_bound_edge_credit": 1,
                "known_block_incidence_propagation_credit": 1,
                "known_block_membership_assignment_credit": 0,
                "physical_component_credit": 0,
                "maximal_physical_component_credit": 0,
                "global_exact_key_fibre_credit": 0,
            })
            accepted_edges.append(edge)
            accepted_source_ids.append(candidate["candidate_id"])
            accepted_triplets.append([
                candidate["candidate_id"],
                negative["row_id"],
                positive["row_id"],
            ])
            accepted_axis_histogram[candidate["axis"]] += 1
            accepted_chart_histogram[candidate["negative_chart"]] += 1
            accepted_area_histogram[qstr(area)] += 1
            accepted_key_ordinals.add(negative["official_key_ordinal"])
            transport_lineage_histogram[lineage] += 1
            parent_common_refinement_histogram[parent_relation] += 1
            reconciliation_rows.append(closed({
                "candidate_reconciliation_row_id":
                    "round244-candidate-reconciliation:"
                    + digest(candidate["candidate_id"]),
                **common,
                "coordinate_transition_kind":
                    "GLOBAL_SAME_CHART_IDENTITY",
                "transformed_face_region_equal": True,
                "disposition":
                    "ACCEPTED_CROSS_PARENT_SAME_CHART_BULK_EDGE",
                "cross_parent_bulk_edge_row_id":
                    edge["cross_parent_bulk_edge_row_id"],
                "physical_glue_credit": 1,
                "maximal_physical_component_credit": 0,
            }))
            continue

        need(
            not candidate["same_official_key"]
            and not signature_equal,
            f"cross-chart mismatch:{candidate['candidate_id']}",
        )
        cross_region = face_region(negative_face)
        cross_t_margin = Q(1) - 2 * max(
            cross_region["t"][0] ** 2,
            cross_region["t"][1] ** 2,
        )
        need(
            cross_t_margin > 0,
            f"cross-chart face strictly inside chart:{candidate['candidate_id']}",
        )
        minimum_cross_chart_source_margin = (
            cross_t_margin
            if minimum_cross_chart_source_margin is None
            else min(minimum_cross_chart_source_margin, cross_t_margin)
        )
        kind = transition_kind(
            candidate["negative_chart"],
            candidate["positive_chart"],
        )
        transformed = transformed_region(
            candidate["negative_chart"],
            candidate["positive_chart"],
            negative_face,
        )
        transformed_equal = (
            transformed is not None
            and transformed == face_region(positive_face)
        )
        if transformed_equal:
            need(
                kind in {"Jx", "Jy", "JxJy"},
                f"nonidentity symmetry:{candidate['candidate_id']}",
            )
            disposition = (
                "REJECTED_KLEIN_PHYSICAL_SYMMETRY_IMAGE_"
                "IS_NOT_SAME_POINT_CONNECTIVITY_GLUE"
            )
        elif kind in {"Jx", "Jy", "JxJy"}:
            disposition = (
                "REJECTED_KLEIN_TRANSFORMED_FACE_REGION_MISMATCH"
            )
        else:
            disposition = (
                "REJECTED_NO_SAME_POINT_CROSS_CHART_TRANSITION"
            )
        rejected_disposition_histogram[disposition] += 1
        reconciliation_rows.append(closed({
            "candidate_reconciliation_row_id":
                "round244-candidate-reconciliation:"
                + digest(candidate["candidate_id"]),
            **common,
            "coordinate_transition_kind": kind,
            "transformed_face_region_equal": transformed_equal,
            "disposition": disposition,
            "cross_parent_bulk_edge_row_id": None,
            "physical_glue_credit": 0,
            "maximal_physical_component_credit": 0,
        }))

    reconciliation_rows.sort(
        key=lambda row: row["candidate_reconciliation_row_id"]
    )
    accepted_edges.sort(
        key=lambda row: row["cross_parent_bulk_edge_row_id"]
    )
    accepted_source_ids.sort()
    accepted_triplets.sort()
    candidate_census_diagnostic = {
        "reconciliation_row_count": len(reconciliation_rows),
        "accepted_edge_count": len(accepted_edges),
        "accepted_candidate_ids_sha256": digest(accepted_source_ids),
        "accepted_candidate_triplets_sha256": digest(accepted_triplets),
        "accepted_axis_histogram": dict(accepted_axis_histogram),
        "accepted_chart_histogram": dict(accepted_chart_histogram),
        "transport_lineage_histogram": dict(transport_lineage_histogram),
        "parent_common_refinement_histogram":
            dict(parent_common_refinement_histogram),
        "rejected_disposition_histogram":
            dict(rejected_disposition_histogram),
        "minimum_source_chart_margin": qstr(minimum_source_chart_margin),
        "minimum_direction_margin": qstr(minimum_direction_margin),
        "minimum_cross_chart_source_margin":
            qstr(minimum_cross_chart_source_margin),
    }
    candidate_census_matches = (
        len(reconciliation_rows) == 9_830
        and len(accepted_edges) == 328
        and digest(accepted_source_ids)
        == ACCEPTED_CANDIDATE_IDS_SHA256
        and digest(accepted_triplets)
        == ACCEPTED_CANDIDATE_TRIPLETS_SHA256
        and dict(accepted_axis_histogram) == {"p": 292, "t": 36}
        and dict(accepted_chart_histogram)
        == {"G:E": 86, "G:N": 78, "G:S": 78, "G:W": 86}
        and dict(transport_lineage_histogram)
        == {"DIRECT": 164, "Jx": 86, "Jy": 78}
        and dict(parent_common_refinement_histogram)
        == {
            "EXACT_PARENT_TANGENTIAL_RECTANGLE": 320,
            "POSITIVE_AREA_PARENT_COMMON_REFINEMENT_T_JUNCTION": 8,
        }
        and dict(rejected_disposition_histogram)
        == {
            "REJECTED_KLEIN_PHYSICAL_SYMMETRY_IMAGE_IS_NOT_SAME_POINT_CONNECTIVITY_GLUE": 16,
            "REJECTED_KLEIN_TRANSFORMED_FACE_REGION_MISMATCH": 260,
            "REJECTED_NO_SAME_POINT_CROSS_CHART_TRANSITION": 9_226,
        }
        and minimum_source_chart_margin
        == Q(340_846_631, 2_097_152_000_000)
        and minimum_direction_margin == Q(85_575, 4_194_304)
        and minimum_cross_chart_source_margin
        == Q(340_846_631, 2_097_152_000_000)
    )
    if not candidate_census_matches:
        raise RuntimeError(
            "Round244 candidate census:"
            + json.dumps(candidate_census_diagnostic, sort_keys=True)
        )

    round243 = load_result(
        "cm2_round243_source_g_exact_event_trace_bulk_quotient_rebuild_certificate.json"
    )
    prior_edges = round243[
        "formal_exact_event_trace_bulk_edge_ledger"
    ]["rows"]
    source_frontier = round243[
        "formal_post_Round243_occurrence_known_block_frontier_ledger"
    ]["rows"]
    resolved_frontier = {
        row["local_occurrence_row_id"]: row
        for row in source_frontier
        if row["local_occurrence_gauge"] == "ROUND179_RESOLVED_CHILD"
    }
    need(
        len(prior_edges) == 10_384
        and len(source_frontier) == 53_968
        and len(resolved_frontier) == 17_192
        and set(resolved_frontier) == set(resolved),
        "Round243 quotient binding",
    )

    child_ids = sorted(resolved)
    old_dsu = DisjointSet(child_ids)
    for edge in prior_edges:
        old_dsu.union(
            edge["negative_side_child_row_id"],
            edge["positive_side_child_row_id"],
        )
    old_component_pairs = {
        tuple(sorted([
            old_dsu.find(edge["negative_side_child_row_id"]),
            old_dsu.find(edge["positive_side_child_row_id"]),
        ]))
        for edge in accepted_edges
    }
    need(
        all(left != right for left, right in old_component_pairs)
        and len(old_component_pairs) == 292,
        "292 new Round243 component pairs",
    )

    child_dsu = DisjointSet(child_ids)
    for edge in prior_edges:
        child_dsu.union(
            edge["negative_side_child_row_id"],
            edge["positive_side_child_row_id"],
        )
    for edge in accepted_edges:
        child_dsu.union(
            edge["negative_side_child_row_id"],
            edge["positive_side_child_row_id"],
        )
    child_groups: dict[str, list[str]] = defaultdict(list)
    for child_id in child_ids:
        child_groups[child_dsu.find(child_id)].append(child_id)
    need(len(child_groups) == 8_148, "Round244 resolved component count")

    old_component_by_child: dict[str, str] = {}
    for row in round243["formal_resolved_bulk_component_ledger"]["rows"]:
        for child_id in row["member_Round179_resolved_child_row_ids"]:
            need(
                child_id not in old_component_by_child,
                f"old component partition:{child_id}",
            )
            old_component_by_child[child_id] = (
                row["resolved_bulk_component_row_id"]
            )
    need(
        set(old_component_by_child) == set(child_ids),
        "Round243 component partition",
    )

    prior_edge_count: Counter[str] = Counter()
    new_edge_count: Counter[str] = Counter()
    for edge in prior_edges:
        prior_edge_count[
            child_dsu.find(edge["negative_side_child_row_id"])
        ] += 1
    for edge in accepted_edges:
        new_edge_count[
            child_dsu.find(edge["negative_side_child_row_id"])
        ] += 1

    component_rows: list[dict[str, Any]] = []
    component_id_by_root: dict[str, str] = {}
    seed_blocks_by_root: dict[str, set[str]] = {}
    new_ids_by_root: dict[str, list[str]] = {}
    child_root_by_id: dict[str, str] = {}
    old_component_count_histogram: Counter[int] = Counter()
    size_histogram: Counter[int] = Counter()
    seed_block_histogram: Counter[int] = Counter()
    affected_supergroup_count = 0
    for root, member_ids in sorted(child_groups.items()):
        for child_id in member_ids:
            child_root_by_id[child_id] = root
        old_component_ids = sorted({
            old_component_by_child[child_id]
            for child_id in member_ids
        })
        seed_blocks = {
            resolved_frontier[child_id][
                "Round243_known_connectivity_block_id"
            ]
            for child_id in member_ids
            if resolved_frontier[child_id][
                "known_block_incidence_attachment_credit"
            ] == 1
        }
        need(
            None not in seed_blocks and len(seed_blocks) <= 1,
            f"no Round244 block merge:{root}",
        )
        new_ids = [
            child_id
            for child_id in member_ids
            if resolved_frontier[child_id][
                "known_block_incidence_attachment_credit"
            ] == 0
            and seed_blocks
        ]
        signatures = {
            digest(return_signature(resolved[child_id]))
            for child_id in member_ids
        }
        need(len(signatures) == 1, f"component signature:{root}")
        component_id = (
            "round244-resolved-bulk-component:" + digest(member_ids)
        )
        component_id_by_root[root] = component_id
        seed_blocks_by_root[root] = set(seed_blocks)
        new_ids_by_root[root] = new_ids
        size_histogram[len(member_ids)] += 1
        seed_block_histogram[len(seed_blocks)] += 1
        old_component_count_histogram[len(old_component_ids)] += 1
        affected_supergroup_count += len(old_component_ids) > 1
        component_rows.append(closed({
            "resolved_bulk_component_row_id": component_id,
            "member_Round179_resolved_child_count": len(member_ids),
            "member_Round179_resolved_child_row_ids": member_ids,
            "member_Round179_resolved_child_row_ids_sha256":
                digest(member_ids),
            "inherited_Round243_resolved_bulk_component_count":
                len(old_component_ids),
            "inherited_Round243_resolved_bulk_component_ids":
                old_component_ids,
            "inherited_Round243_resolved_bulk_component_ids_sha256":
                digest(old_component_ids),
            "Round243_same_parent_bulk_edge_count":
                prior_edge_count[root],
            "Round244_cross_parent_same_chart_bulk_edge_count":
                new_edge_count[root],
            "full_return_signature_sha256": next(iter(signatures)),
            "seed_Round243_known_connectivity_block_count":
                len(seed_blocks),
            "seed_Round243_known_connectivity_block_ids":
                sorted(seed_blocks),
            "new_occurrence_known_block_incidence_count": len(new_ids),
            "new_occurrence_row_ids": new_ids,
            "new_occurrence_row_ids_sha256": digest(new_ids),
            "certified_known_connectivity_only": True,
            "maximal_physical_component_claimed": False,
            "global_exact_key_fibre_credit": 0,
        }))
    component_rows.sort(
        key=lambda row: row["resolved_bulk_component_row_id"]
    )
    need(
        affected_supergroup_count == 276
        and {
            count: total
            for count, total in old_component_count_histogram.items()
            if count > 1
        } == {2: 264, 3: 8, 4: 4}
        and sum(len(values) for values in new_ids_by_root.values()) == 20
        and seed_block_histogram == {0: 7_708, 1: 440},
        "Round244 component propagation census",
    )

    block_rows = round243[
        "formal_Round243_known_connectivity_block_ledger"
    ]["rows"]
    block_carry_rows = [
        closed({
            "block_carry_row_id":
                "round244-known-connectivity-block-carry:"
                + digest(row["known_connectivity_block_id"]),
            "Round243_known_connectivity_block_id":
                row["known_connectivity_block_id"],
            "Round243_known_connectivity_block_row_sha256":
                row["row_sha256"],
            "Round244_known_connectivity_block_id":
                row["known_connectivity_block_id"],
            "Round244_block_merge_credit": 0,
            "certified_known_connectivity": True,
            "maximal_physical_component_claimed": False,
            "component_exhaustion_credit": 0,
            "global_exact_key_fibre_credit": 0,
        })
        for row in block_rows
    ]
    block_carry_rows.sort(key=lambda row: row["block_carry_row_id"])
    need(len(block_carry_rows) == 7_388, "Round244 block carry count")

    new_block_by_occurrence: dict[str, str] = {}
    new_component_by_occurrence: dict[str, str] = {}
    for root, occurrence_ids in new_ids_by_root.items():
        if not occurrence_ids:
            continue
        need(
            len(seed_blocks_by_root[root]) == 1,
            f"unique seed block:{root}",
        )
        block_id = next(iter(seed_blocks_by_root[root]))
        for occurrence_id in occurrence_ids:
            new_block_by_occurrence[occurrence_id] = block_id
            new_component_by_occurrence[occurrence_id] = (
                component_id_by_root[root]
            )
    need(len(new_block_by_occurrence) == 20, "20 incidence deltas")

    delta_rows: list[dict[str, Any]] = []
    for occurrence_id in sorted(new_block_by_occurrence):
        source = resolved_frontier[occurrence_id]
        root = child_root_by_id[occurrence_id]
        need(
            source["known_block_incidence_attachment_credit"] == 0
            and source["Round243_known_connectivity_block_id"] is None,
            f"new incidence precondition:{occurrence_id}",
        )
        delta_rows.append(closed({
            "incidence_delta_row_id":
                "round244-known-block-incidence-delta:"
                + digest([
                    occurrence_id,
                    new_block_by_occurrence[occurrence_id],
                ]),
            "local_occurrence_row_id": occurrence_id,
            "local_occurrence_gauge": "ROUND179_RESOLVED_CHILD",
            "official_key_ordinal": source["official_key_ordinal"],
            "official_key_id": source["official_key_id"],
            "resolved_bulk_component_row_id":
                new_component_by_occurrence[occurrence_id],
            "seed_Round243_known_connectivity_block_ids":
                sorted(seed_blocks_by_root[root]),
            "Round244_known_connectivity_block_id":
                new_block_by_occurrence[occurrence_id],
            "derivation":
                "CROSS_PARENT_SAME_CHART_GLOBAL_IDENTITY_PLUS_"
                "EXACT_10_FIELD_CLOSED_FACE_RESTRICTION",
            "known_block_incidence_attachment_credit": 1,
            "known_block_membership_assignment_credit": 0,
            "physical_component_credit": 0,
            "maximal_physical_component_credit": 0,
            "global_exact_key_fibre_credit": 0,
        }))
    delta_rows.sort(key=lambda row: row["incidence_delta_row_id"])

    post_rows: list[dict[str, Any]] = []
    for source in source_frontier:
        occurrence_id = source["local_occurrence_row_id"]
        base = {
            key: value
            for key, value in source.items()
            if key not in {"post_frontier_row_id", "row_sha256"}
        }
        if source["known_block_incidence_attachment_credit"] == 1:
            current_block = source[
                "Round243_known_connectivity_block_id"
            ]
            need(current_block is not None, f"old block:{occurrence_id}")
        elif occurrence_id in new_block_by_occurrence:
            current_block = new_block_by_occurrence[occurrence_id]
            base["known_block_incidence_attachment_credit"] = 1
            base["incidence_source"] = (
                "ROUND244_CROSS_PARENT_SAME_CHART_BULK_PROPAGATION"
            )
        else:
            current_block = None
        base["Round244_known_connectivity_block_id"] = current_block
        post_rows.append(closed({
            "post_frontier_row_id":
                "round244-post-known-block-frontier:"
                + digest([
                    occurrence_id,
                    current_block,
                    base["incidence_source"],
                    base["known_block_incidence_attachment_credit"],
                ]),
            **base,
        }))
    post_rows.sort(key=lambda row: row["post_frontier_row_id"])
    need(
        len(post_rows) == len({
            row["local_occurrence_row_id"] for row in post_rows
        }) == 53_968,
        "Round244 occurrence frontier partition",
    )

    key_metadata = {
        row["official_key_ordinal"]: {
            "official_key_id": row["official_key_id"],
            "official_key_row": row["official_key_row"],
        }
        for row in round243[
            "formal_post_Round243_key_frontier_ledger"
        ]["rows"]
    }
    grouped: dict[int, list[dict[str, Any]]] = defaultdict(list)
    for row in post_rows:
        grouped[row["official_key_ordinal"]].append(row)
    delta_by_key = Counter(
        row["official_key_ordinal"] for row in delta_rows
    )
    key_rows: list[dict[str, Any]] = []
    for ordinal, occurrences in sorted(grouped.items()):
        metadata = key_metadata[ordinal]
        attached = sum(
            row["known_block_incidence_attachment_credit"]
            for row in occurrences
        )
        total = len(occurrences)
        need(
            all(
                row["official_key_id"] == metadata["official_key_id"]
                for row in occurrences
            ),
            f"key identity:{ordinal}",
        )
        key_rows.append(closed({
            "key_frontier_row_id":
                "round244-key-frontier:"
                + digest([
                    ordinal,
                    metadata["official_key_id"],
                    attached,
                    total,
                ]),
            "official_key_ordinal": ordinal,
            "official_key_id": metadata["official_key_id"],
            "official_key_row": metadata["official_key_row"],
            "local_occurrence_count": total,
            "occurrences_with_known_block_incidence": attached,
            "occurrences_without_known_block_incidence":
                total - attached,
            "new_Round244_known_block_incidences":
                delta_by_key[ordinal],
            "cumulative_known_block_incidences": attached,
            "maximal_physical_component_assignment_count": 0,
            "global_exact_key_fibre_exhausted": False,
            "global_exact_key_disposition_credit": 0,
        }))
    key_rows.sort(key=lambda row: row["key_frontier_row_id"])

    attached_count = sum(
        row["known_block_incidence_attachment_credit"]
        for row in post_rows
    )
    need(
        len(key_rows) == 116
        and attached_count == 36_200
        and len(delta_by_key) == 12
        and sum(
            row["occurrences_without_known_block_incidence"]
            for row in key_rows
        ) == 17_768,
        "Round244 global frontier census",
    )

    census = {
        "Round220_different_parent_coordinate_candidate_count": 9_830,
        "accepted_cross_parent_same_chart_bulk_edge_count": 328,
        "accepted_axis_histogram":
            dict(sorted(accepted_axis_histogram.items())),
        "accepted_source_chart_histogram":
            dict(sorted(accepted_chart_histogram.items())),
        "accepted_parent_transport_lineage_histogram":
            dict(sorted(transport_lineage_histogram.items())),
        "accepted_parent_common_refinement_relation_histogram":
            dict(sorted(parent_common_refinement_histogram.items())),
        "accepted_exact_area_histogram":
            dict(sorted(accepted_area_histogram.items())),
        "accepted_exact_area_sum": qstr(sum(
            (
                Q(area) * count
                for area, count in accepted_area_histogram.items()
            ),
            Q(0),
        )),
        "accepted_distinct_exact_key_count":
            len(accepted_key_ordinals),
        "minimum_source_chart_interior_margin":
            qstr(minimum_source_chart_margin),
        "minimum_direction_interior_margin":
            qstr(minimum_direction_margin),
        "minimum_cross_chart_source_interior_margin":
            qstr(minimum_cross_chart_source_margin),
        "rejected_cross_chart_candidate_count": 9_502,
        "rejected_cross_chart_disposition_histogram":
            dict(sorted(rejected_disposition_histogram.items())),
        "new_Round243_component_pair_count": len(old_component_pairs),
        "Round243_resolved_bulk_component_count": 8_440,
        "Round244_resolved_bulk_component_count": len(component_rows),
        "Round244_resolved_bulk_component_reduction": 292,
        "affected_Round244_supercomponent_count":
            affected_supergroup_count,
        "affected_supercomponent_inherited_Round243_component_count_histogram":
            {
                str(count): total
                for count, total
                in sorted(old_component_count_histogram.items())
                if count > 1
            },
        "resolved_bulk_component_size_histogram": {
            str(size): count
            for size, count in sorted(size_histogram.items())
        },
        "resolved_bulk_component_seed_block_count_histogram": {
            str(count): total
            for count, total in sorted(seed_block_histogram.items())
        },
        "Round243_known_connectivity_block_count": 7_388,
        "Round244_known_connectivity_block_count": 7_388,
        "Round244_known_connectivity_block_reduction": 0,
        "Round243_occurrences_with_known_block_incidence": 36_180,
        "Round244_new_occurrence_known_block_incidences":
            len(delta_rows),
        "post_Round244_occurrences_with_known_block_incidence":
            attached_count,
        "post_Round244_occurrences_without_known_block_incidence":
            53_968 - attached_count,
        "keys_touched_by_Round244": len(delta_by_key),
        "observed_exact_key_count": len(key_rows),
        "maximal_physical_component_assignment_count": 0,
        "global_exact_key_fibre_exhausted_count": 0,
    }

    return {
        "status": (
            "CERTIFIED_328_CROSS_PARENT_SAME_CHART_GLOBAL_IDENTITY_"
            "BULK_EDGES__9502_CROSS_CHART_ROWS_FAIL_CLOSED__"
            "8148_RESOLVED_BULK_COMPONENTS__7388_KNOWN_BLOCKS__"
            "36200_OF_53968_OCCURRENCE_INCIDENCES__"
            "ZERO_COMPONENT_OR_GLOBAL_FIBRE_PROMOTION"
        ),
        "census": census,
        "formal_input_binding": {
            name: PINS[name] for name in sorted(PINS)
        },
        "global_chart_geometry_contract": geometry_contract,
        "Round226_reconciliation": {
            "Round226_event_sheet_channel_remains_closed_9830_of_9830":
                True,
            "Round244_accepted_edges_use_new_non_event_bulk_evidence":
                True,
            "Round226_coordinate_or_key_equality_never_reused_as_glue":
                True,
            "Round226_Klein_symmetry_is_not_connectivity_glue": True,
        },
        "formal_different_parent_candidate_reconciliation_ledger":
            ledger(
                reconciliation_rows,
                "candidate_reconciliation_row_id",
            ),
        "formal_cross_parent_same_chart_bulk_edge_ledger":
            ledger(
                accepted_edges,
                "cross_parent_bulk_edge_row_id",
            ),
        "formal_resolved_bulk_component_ledger":
            ledger(component_rows, "resolved_bulk_component_row_id"),
        "formal_Round244_known_connectivity_block_carry_ledger":
            ledger(block_carry_rows, "block_carry_row_id"),
        "formal_occurrence_known_block_incidence_delta_ledger":
            ledger(delta_rows, "incidence_delta_row_id"),
        "formal_post_Round244_occurrence_known_block_frontier_ledger":
            ledger(post_rows, "post_frontier_row_id"),
        "formal_post_Round244_key_frontier_ledger":
            ledger(key_rows, "key_frontier_row_id"),
        "scope_contract": {
            "same_chart_global_embedding_is_parent_independent": True,
            "all_328_edges_have_exact_positive_area_physical_common_refinement":
                True,
            "all_328_edges_have_exact_equal_closed_10_field_signature":
                True,
            "all_328_edges_are_strictly_inside_chart_and_direction_boundaries":
                True,
            "all_9502_cross_chart_candidates_remain_fail_closed": True,
            "physical_Klein_symmetry_is_not_same_point_connectivity":
                True,
            "no_edge_accepted_from_box_touch_or_exact_key_equality_alone":
                True,
            "known_block_incidence_is_not_component_membership": True,
            "known_connectivity_blocks_are_not_claimed_maximal": True,
        },
        "strict_nonpromotion": {
            "known_block_membership_assignment_credit": 0,
            "physical_component_credit": 0,
            "maximal_physical_component_credit": 0,
            "global_exact_key_fibre_credit": 0,
            "global_exact_key_disposition_credit": 0,
            "Gate5_complete_field_block_count": 0,
            "Gate5_filled_field_slot_count": 10,
            "Gate5_total_field_slot_count": 18,
            "CM2": "NO-GO_FOR_CLAIM",
        },
        "required_next": (
            "return to the retained/event-bearing frontier: map the Round242 "
            "264 owner-shadow transition patches and 2872 whole-root "
            "zero-absence continuations, then process the remaining 5364 "
            "Round239 wall, crossing-time, source-seam, and whole-signature "
            "interfaces; the rejected 9502 cross-chart coordinate pool must "
            "not be recycled"
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--no-write", action="store_true")
    arguments = parser.parse_args()
    result = build()
    document = {
        "schema": SCHEMA,
        "result": result,
        "result_sha256": digest(result),
    }
    raw = canonical(document) + b"\n"
    if not arguments.no_write:
        safe_write(raw)
    print(result["status"])
    print(json.dumps(result["census"], sort_keys=True))
    print(f"result_sha256={document['result_sha256']}")
    print(f"certificate_sha256={hashlib.sha256(raw).hexdigest()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
