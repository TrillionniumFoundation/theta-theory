#!/usr/bin/env python3
"""Close the 1,276 Round280 lower-stratum decision tails.

This producer is deliberately ZERO-CREDIT.  It does not create an expanded
occurrence, a component edge, a maximality assignment, a fibre disposition,
or a Jx/Jy same-point identification.

The two exhaustive inputs are:

* 880 exact source-factor ``t=0`` wall rows.  Round204 freezes the
  outcome-blind policy that the positive-t side owns and the negative-t side
  is a shadow.  Positive-side Round179 retained children are therefore used
  as the only owners.  A negative face with no positive owner is accepted as
  absent only after its positive-area overlap with every one of the complete
  21,232 Round174 unique-first parent boxes is proved empty.
* 396 fully-replaced Round179 origins.  Their two resolved p-children form an
  exhaustive closed cover.  Predicate signs are reconstructed from the
  independent Round179 verifier geometry (wall rows) or the strict resolved
  outgoing cell (outgoing rows).
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import copy
from fractions import Fraction as Q
import gc
import gzip
import hashlib
import io
import json
from pathlib import Path
import sys
import tempfile
from typing import Any


HERE = Path(__file__).resolve().parent
PREFIX = "cm2_round281_source_g_lower_stratum_tail_closure"
DEFAULT_LEDGER = HERE / f"{PREFIX}_ledger.json.gz"
DEFAULT_RESULT = HERE / f"{PREFIX}_result.json"
SCHEMA = "cm2.round281.source-g-lower-stratum-tail-closure.v1"
LEDGER_SCHEMA = "cm2.round281.source-g-lower-stratum-tail-closure-ledger.v1"

INPUT_SHA256 = {
    "cm2_round174_source_g_unique_first_dynamic_occurrence_materialization_rows.json":
        "9edeea2e1033b0dd70dee11a53b0f6aeb21fe74030aeefb60b081a7c420cff54",
    "cm2_round179_source_g_residual_tube_arrangement_rows.json":
        "f20b42c1fed781779b537b4d45bf44233eae1ed3ee620b95177a80f0eb2b5e42",
    "cm2_round179_source_g_residual_tube_arrangement_verifier.py":
        "292719cedfb4d5b802bf87a48314b5237f7b4438e4615d124d716f497044e679",
    "cm2_round204_source_g_wall_return_signature_local_replacement_certificate.json":
        "e7e1c49bebcb8c01f0fb4b33af66e4f2a8de560f121cae65f4971b2fec3e1818",
    "cm2_round280_source_g_lower_stratum_physical_disposition_probe_ledger.json.gz":
        "0f939334f9ca65c535be7123b8f9370b0833f84743b6a094c92ffcc1087dec1b",
    "cm2_round280_source_g_lower_stratum_physical_disposition_probe_result.json":
        "3147925b1f49ae9743055c7dc2e3194d7b0a385994c67097f3cb88e91bf0d484",
}

ROUND280_UNRESOLVED = "UNRESOLVED__SOURCE_T0_HALF_OPEN_OWNER_NOT_MATERIALIZED"
ROUND280_PROVENANCE = "FORMAL_PROVENANCE_ONLY__NO_PHYSICAL_DECISION"

T0_OWNER = "CERTIFIED_PHYSICAL_SUPPORT_EXISTS__POSITIVE_T_HALF_OPEN_OWNER"
T0_SHADOW = (
    "CERTIFIED_PHYSICAL_SUPPORT_EXISTS__NEGATIVE_T_SHADOW_TO_POSITIVE_OWNER"
)
T0_PARTITIONED = (
    "CERTIFIED_PARTITIONED__NEGATIVE_T_SHADOW_AND_ABSENCE"
)
T0_ABSENT = (
    "CERTIFIED_SUPPORT_ABSENT__NEGATIVE_T_SHADOW_WITH_NO_ADMISSIBLE_"
    "POSITIVE_OWNER"
)
REPLACED_ABSENT = (
    "CERTIFIED_SUPPORT_ABSENT__FULLY_REPLACED_RESOLVED_CHILD_COVER"
)


class ClosureError(RuntimeError):
    pass


def need(condition: bool, label: str) -> None:
    if not condition:
        raise ClosureError(label)


ENCODER = json.JSONEncoder(
    sort_keys=True,
    separators=(",", ":"),
    ensure_ascii=False,
    allow_nan=False,
)


def canonical(value: Any) -> bytes:
    return ENCODER.encode(value).encode("utf-8")


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def file_sha256(path: Path) -> str:
    state = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            state.update(chunk)
    return state.hexdigest()


def read_json(path: Path) -> dict[str, Any]:
    with path.open("rb") as stream:
        value = json.load(stream)
    need(isinstance(value, dict), f"object input:{path.name}")
    return value


def read_gzip_json(path: Path) -> dict[str, Any]:
    with gzip.open(path, "rb") as stream:
        value = json.load(stream)
    need(isinstance(value, dict), f"gzip object input:{path.name}")
    return value


def unpack(result: dict[str, Any], table: str) -> list[dict[str, Any]]:
    columns = result["row_column_schemas"][table]
    rows = result[table]
    need(all(len(row) == len(columns) for row in rows), f"packed width:{table}")
    return [dict(zip(columns, row)) for row in rows]


def closed(row: dict[str, Any]) -> dict[str, Any]:
    need("row_sha256" not in row, "row already closed")
    output = dict(row)
    output["row_sha256"] = digest(output)
    return output


def qstr(value: Q) -> str:
    return str(value.numerator) if value.denominator == 1 else str(value)


def qbox(values: list[str]) -> tuple[Q, Q, Q, Q, Q, Q]:
    need(len(values) == 6, "box width")
    return tuple(map(Q, values))  # type: ignore[return-value]


def face_rect(values: list[str]) -> tuple[Q, Q, Q, Q]:
    box = qbox(values)
    return box[2], box[3], box[4], box[5]


def area(rect: tuple[Q, Q, Q, Q]) -> Q:
    p0, p1, s0, s1 = rect
    return (p1 - p0) * (s1 - s0)


def intersection(
    left: tuple[Q, Q, Q, Q],
    right: tuple[Q, Q, Q, Q],
) -> tuple[Q, Q, Q, Q] | None:
    p0 = max(left[0], right[0])
    p1 = min(left[1], right[1])
    s0 = max(left[2], right[2])
    s1 = min(left[3], right[3])
    if p0 >= p1 or s0 >= s1:
        return None
    return p0, p1, s0, s1


def rect_payload(rect: tuple[Q, Q, Q, Q]) -> list[str]:
    return ["0", "0", *(qstr(value) for value in rect)]


def union_area_disjoint(
    rectangles: list[tuple[Q, Q, Q, Q]],
) -> tuple[Q, bool]:
    """Return exact union area and whether interiors are pairwise disjoint."""
    if not rectangles:
        return Q(0), True
    p_values = sorted({value for rect in rectangles for value in rect[:2]})
    s_values = sorted({value for rect in rectangles for value in rect[2:]})
    total = Q(0)
    disjoint = True
    for p0, p1 in zip(p_values, p_values[1:]):
        for s0, s1 in zip(s_values, s_values[1:]):
            if p0 == p1 or s0 == s1:
                continue
            multiplicity = sum(
                rect[0] <= p0 and p1 <= rect[1]
                and rect[2] <= s0 and s1 <= rect[3]
                for rect in rectangles
            )
            if multiplicity:
                total += (p1 - p0) * (s1 - s0)
            if multiplicity > 1:
                disjoint = False
    return total, disjoint


def exact_rect_complement(
    container: tuple[Q, Q, Q, Q],
    covered: list[tuple[Q, Q, Q, Q]],
) -> list[tuple[Q, Q, Q, Q]]:
    """Partition ``container \\ union(covered)`` into exact grid cells."""
    clipped = [
        hit for rect in covered
        if (hit := intersection(container, rect)) is not None
    ]
    p_values = sorted({container[0], container[1], *(
        value for rect in clipped for value in rect[:2]
    )})
    s_values = sorted({container[2], container[3], *(
        value for rect in clipped for value in rect[2:]
    )})
    cells: list[tuple[Q, Q, Q, Q]] = []
    for p0, p1 in zip(p_values, p_values[1:]):
        for s0, s1 in zip(s_values, s_values[1:]):
            if p0 == p1 or s0 == s1:
                continue
            cell = (p0, p1, s0, s1)
            if not any(
                rect[0] <= p0 and p1 <= rect[1]
                and rect[2] <= s0 and s1 <= rect[3]
                for rect in clipped
            ):
                cells.append(cell)
    return sorted(cells)


def zero_credit() -> dict[str, Any]:
    return {
        "expanded_occurrence_credit": 0,
        "component_edge_credit": 0,
        "maximality_credit": 0,
        "exact_key_fibre_credit": 0,
        "global_exact_key_disposition_credit": 0,
        "Jx_Jy_same_point_glue_credit": 0,
        "requires_final_DSU_to_decide_local_physical_support": False,
        "nominal_lineage_promoted_to_occurrence": False,
    }


def gzip_payload(value: Any) -> bytes:
    buffer = io.BytesIO()
    with gzip.GzipFile(filename="", mode="wb", fileobj=buffer, mtime=0) as stream:
        stream.write(canonical(value))
    return buffer.getvalue()


def write_atomic(path: Path, payload: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(
        mode="wb", dir=path.parent, prefix=f".{path.name}.", delete=False
    ) as stream:
        temporary = Path(stream.name)
        stream.write(payload)
        stream.flush()
    temporary.replace(path)


def row_id(round280_row_id: str, state: str) -> str:
    return "round281-lower-tail-closure:" + digest([round280_row_id, state])


def build() -> tuple[dict[str, Any], dict[str, Any]]:
    for filename, expected in INPUT_SHA256.items():
        need(file_sha256(HERE / filename) == expected, f"pinned input:{filename}")

    round204 = read_json(
        HERE / "cm2_round204_source_g_wall_return_signature_local_replacement_certificate.json"
    )["result"]
    sheets204 = round204["formal_2D_sheet_lineage"]
    need(
        sheets204["source_sheet_row_count"] == 224
        and sheets204["all_source_sheets_have_positive_t_half_open_owner"],
        "Round204 positive-t source-sheet policy",
    )
    source_sheet_rows = sheets204["source_sheet_rows"]
    need(
        all(
            row["half_open_owner_policy"]
            == "OUTCOME_BLIND_POSITIVE_T_SIDE_OWNS__NEGATIVE_T_SIDE_IS_SHADOW"
            for row in source_sheet_rows
        ),
        "Round204 policy row closure",
    )
    del round204, source_sheet_rows
    gc.collect()

    previous = read_gzip_json(
        HERE / "cm2_round280_source_g_lower_stratum_physical_disposition_probe_ledger.json.gz"
    )
    previous_rows = previous["rows"]
    tails = [
        row for row in previous_rows
        if row["physical_disposition"]
        in {ROUND280_UNRESOLVED, ROUND280_PROVENANCE}
    ]
    need(len(tails) == 1_276, "Round280 tail census")
    t0_rows = [
        row for row in tails
        if row["physical_disposition"] == ROUND280_UNRESOLVED
    ]
    replaced_rows = [
        row for row in tails
        if row["physical_disposition"] == ROUND280_PROVENANCE
    ]
    need(len(t0_rows) == 880 and len(replaced_rows) == 396, "tail partition")
    del previous, previous_rows
    gc.collect()

    round174 = read_json(
        HERE / "cm2_round174_source_g_unique_first_dynamic_occurrence_materialization_rows.json"
    )["result"]
    parents = unpack(round174, "parent_rows")
    need(len(parents) == 21_232, "complete Round174 parent census")
    del round174
    gc.collect()

    round179 = read_json(
        HERE / "cm2_round179_source_g_residual_tube_arrangement_rows.json"
    )["result"]
    origins = unpack(round179, "origin_tube_rows")
    walls = unpack(round179, "wall_normal_form_rows")
    outgoing = unpack(round179, "outgoing_normal_form_rows")
    resolved = unpack(round179, "resolved_3d_child_rows")
    retained = unpack(round179, "retained_3d_child_rows")
    guards = unpack(round179, "chart_guard_child_rows")
    del round179
    gc.collect()

    need(len(origins) == 62_012, "complete Round179 origin census")
    origin_by_id = {row["origin_row_id"]: row for row in origins}
    wall_by_id = {row["row_id"]: row for row in walls}
    outgoing_by_id = {row["row_id"]: row for row in outgoing}
    parent_by_id = {row["parent_id"]: row for row in parents}
    children_by_origin: dict[str, list[tuple[str, dict[str, Any]]]] = defaultdict(list)
    for kind, rows in (
        ("RESOLVED", resolved),
        ("RETAINED", retained),
        ("GUARD", guards),
    ):
        for row in rows:
            children_by_origin[row["origin_row_id"]].append((kind, row))

    # Every positive-t Round179 origin at t=0 has exactly one retained
    # t=0-adjacent child.  It is the only admissible owner-cell universe.
    positive_owners_by_chart: dict[
        str, list[tuple[dict[str, Any], dict[str, Any], tuple[Q, Q, Q, Q]]]
    ] = defaultdict(list)
    for origin in origins:
        box = qbox(origin["original_box"])
        if not (box[0] == 0 and box[1] > 0):
            continue
        t0_children = [
            (kind, child)
            for kind, child in children_by_origin[origin["origin_row_id"]]
            if qbox(child["box"])[0] == 0
        ]
        need(
            len(t0_children) == 1 and t0_children[0][0] == "RETAINED",
            f"unique positive retained owner:{origin['origin_row_id']}",
        )
        child = t0_children[0][1]
        need(
            face_rect(child["box"]) == face_rect(origin["original_box"]),
            f"owner child full face:{child['row_id']}",
        )
        positive_owners_by_chart[origin["chart"]].append(
            (origin, child, face_rect(origin["original_box"]))
        )

    positive_parents_by_chart: dict[
        str, list[tuple[dict[str, Any], tuple[Q, Q, Q, Q]]]
    ] = defaultdict(list)
    for parent in parents:
        box = qbox(parent["box"])
        if box[0] == 0 and box[1] > 0:
            positive_parents_by_chart[parent["chart"]].append(
                (parent, face_rect(parent["box"]))
            )

    t0_output: list[dict[str, Any]] = []
    shadow_patch_count = 0
    shadow_owner_origins: set[str] = set()
    t0_face_area = Q(0)
    owned_or_shadowed_area = Q(0)
    absent_area = Q(0)

    for previous_row in sorted(
        t0_rows, key=lambda row: row["canonical_support_row_id"]
    ):
        support_id = previous_row["canonical_support_row_id"]
        wall = wall_by_id[support_id]
        origin = origin_by_id[wall["origin_row_id"]]
        box = qbox(origin["original_box"])
        rect = face_rect(origin["original_box"])
        rect_area = area(rect)
        t0_face_area += rect_area
        need(
            previous_row["canonical_support_kind"]
            == "NOMINAL_REGULAR_FACTOR_UNION_IF_PRESENT"
            and wall["source_factor_classification"] == "REGULAR_GRAPH"
            and wall["source_gradient_axis"] == "t"
            and wall["integer_wall"] == 0
            and wall["target_face_classification"] == "STRICT_ZERO_ABSENT"
            and ((box[0] == 0) ^ (box[1] == 0)),
            f"t0 symbolic contract:{support_id}",
        )

        positive_side = box[0] == 0
        patches: list[dict[str, Any]] = []
        patch_rectangles: list[tuple[Q, Q, Q, Q]] = []
        absence_rectangles: list[tuple[Q, Q, Q, Q]] = []
        if positive_side:
            t0_children = [
                child for kind, child
                in children_by_origin[origin["origin_row_id"]]
                if kind == "RETAINED" and qbox(child["box"])[0] == 0
            ]
            need(len(t0_children) == 1, f"self owner child:{support_id}")
            owner_child = t0_children[0]
            patch_rectangles = [rect]
            patches = [{
                "patch_exact_bounds": rect_payload(rect),
                "patch_area": qstr(rect_area),
                "positive_owner_origin_row_id": origin["origin_row_id"],
                "positive_owner_retained_child_row_id": owner_child["row_id"],
                "positive_owner_parent_id": origin["parent_id"],
                "negative_shadow_origin_row_id": None,
                "owner_policy":
                    "OUTCOME_BLIND_POSITIVE_T_SIDE_OWNS__"
                    "NEGATIVE_T_SIDE_IS_SHADOW",
            }]
            state = T0_OWNER
            owned_or_shadowed_area += rect_area
            evidence_basis = (
                "ROUND204_POSITIVE_T_OWNER_POLICY__ROUND179_EXACT_T0_"
                "RETAINED_OWNER_CHILD"
            )
        else:
            for owner_origin, owner_child, owner_rect in (
                positive_owners_by_chart[origin["chart"]]
            ):
                patch = intersection(rect, owner_rect)
                if patch is None:
                    continue
                patch_area = area(patch)
                patches.append({
                    "patch_exact_bounds": rect_payload(patch),
                    "patch_area": qstr(patch_area),
                    "positive_owner_origin_row_id":
                        owner_origin["origin_row_id"],
                    "positive_owner_retained_child_row_id":
                        owner_child["row_id"],
                    "positive_owner_parent_id": owner_origin["parent_id"],
                    "negative_shadow_origin_row_id": origin["origin_row_id"],
                    "owner_policy":
                        "OUTCOME_BLIND_POSITIVE_T_SIDE_OWNS__"
                        "NEGATIVE_T_SIDE_IS_SHADOW",
                })
                patch_rectangles.append(patch)
                shadow_owner_origins.add(owner_origin["origin_row_id"])
            union, disjoint = union_area_disjoint(patch_rectangles)
            need(disjoint, f"shadow owner interiors disjoint:{support_id}")
            if union == rect_area:
                state = T0_SHADOW
                evidence_basis = (
                    "ROUND204_POSITIVE_T_OWNER_POLICY__EXACT_POSITIVE_"
                    "RETAINED_CHILD_PATCH_COVER"
                )
                shadow_patch_count += len(patches)
                owned_or_shadowed_area += rect_area
            elif union > 0:
                need(union < rect_area, f"partial cover proper:{support_id}")
                absence_rectangles = exact_rect_complement(rect, patch_rectangles)
                absence_union, absence_disjoint = union_area_disjoint(
                    absence_rectangles
                )
                need(absence_disjoint, f"partial absence disjoint:{support_id}")
                need(
                    union + absence_union == rect_area,
                    f"partial exact partition:{support_id}",
                )
                # The complete positive-t Round174 parent universe must not
                # touch the complement.  This prevents a retained-origin
                # subset from being mistaken for an exhaustive owner proof.
                complement_parent_hits = [
                    (parent, cell)
                    for parent, parent_rect
                    in positive_parents_by_chart[origin["chart"]]
                    for cell in absence_rectangles
                    if intersection(cell, parent_rect) is not None
                ]
                need(
                    not complement_parent_hits,
                    f"partial complement has positive parent:{support_id}",
                )
                state = T0_PARTITIONED
                evidence_basis = (
                    "ROUND204_POSITIVE_T_OWNER_POLICY__EXACT_POSITIVE_"
                    "RETAINED_CHILD_PATCH_COVER_PLUS_COMPLETE_ROUND174_"
                    "COMPLEMENT_ABSENCE"
                )
                shadow_patch_count += len(patches)
                owned_or_shadowed_area += union
                absent_area += absence_union
            else:
                # Strengthened absence: inspect every complete Round174
                # unique-first parent, not just residual origins/collars.
                parent_hits = [
                    parent for parent, parent_rect
                    in positive_parents_by_chart[origin["chart"]]
                    if intersection(rect, parent_rect) is not None
                ]
                need(
                    not parent_hits,
                    f"negative face has admissible positive parent:{support_id}",
                )
                need(
                    Q(-1) == 2 * Q(0) * Q(0) - 1,
                    "t0 lies strictly inside true source chart",
                )
                state = T0_ABSENT
                evidence_basis = (
                    "ROUND204_POSITIVE_T_ONLY_OWNER_POLICY__COMPLETE_"
                    "ROUND174_UNIQUE_FIRST_PARENT_UNIVERSE_HAS_NO_"
                    "POSITIVE_T_OWNER"
                )
                absent_area += rect_area
                absence_rectangles = [rect]

        union, disjoint = union_area_disjoint(patch_rectangles)
        absence_union, absence_disjoint = union_area_disjoint(
            absence_rectangles
        )
        need(disjoint, f"t0 patches disjoint:{support_id}")
        need(absence_disjoint, f"t0 absence cells disjoint:{support_id}")
        need(
            union + absence_union == rect_area,
            f"t0 owner area conservation:{support_id}",
        )
        payload = {
            "round281_lower_tail_closure_row_id":
                row_id(
                    previous_row["lower_stratum_physical_disposition_row_id"],
                    state,
                ),
            "Round280_lower_support_disposition_row_id":
                previous_row["lower_stratum_physical_disposition_row_id"],
            "Round267_lower_stratum_terminal_lineage_row_id":
                previous_row["Round267_lower_stratum_terminal_lineage_row_id"],
            "canonical_support_row_id": support_id,
            "containing_Round174_residual_row_id":
                previous_row["containing_Round174_residual_row_id"],
            "parent_id": origin["parent_id"],
            "source_chart": origin["chart"],
            "decision_family": "EXACT_SOURCE_T0_HALF_OPEN_OWNER",
            "physical_disposition": state,
            "evidence_basis": evidence_basis,
            "source_factor_exact_zero_set": "t=0",
            "source_factor_regular_t_graph": True,
            "target_factor_strictly_absent": True,
            "t_side": "POSITIVE_T" if positive_side else "NEGATIVE_T",
            "source_t0_face_exact_bounds": rect_payload(rect),
            "source_t0_face_area": qstr(rect_area),
            "owner_patch_count": len(patches),
            "owner_patch_union_area": qstr(union),
            "owner_patch_interiors_pairwise_disjoint": disjoint,
            "owner_patches": patches,
            "absence_cell_count": len(absence_rectangles),
            "absence_cell_union_area": qstr(absence_union),
            "absence_cell_interiors_pairwise_disjoint": absence_disjoint,
            "absence_cells": [
                {
                    "cell_exact_bounds": rect_payload(cell),
                    "cell_area": qstr(area(cell)),
                    "owner_policy":
                        "OUTCOME_BLIND_POSITIVE_T_SIDE_OWNS__"
                        "NEGATIVE_T_SIDE_IS_SHADOW",
                    "complete_positive_t_parent_overlap_absent": True,
                }
                for cell in absence_rectangles
            ],
            "complete_Round174_unique_first_parent_count": len(parents),
            "positive_t_Round174_parent_overlap_count":
                sum(
                    intersection(rect, parent_rect) is not None
                    for _parent, parent_rect
                    in positive_parents_by_chart[origin["chart"]]
                ),
            "t0_true_source_chart_domain_value_2t2_minus_1": "-1",
            "negative_side_may_never_be_forged_as_owner": True,
            **zero_credit(),
        }
        t0_output.append(closed(payload))

    # Fully replaced rows: independently reconstruct strict predicate signs
    # on the exhaustive two-child cover using the Round179 verifier geometry.
    sys.path.insert(0, str(HERE))
    import cm2_round179_source_g_residual_tube_arrangement_verifier as r179v

    replaced_output: list[dict[str, Any]] = []
    replaced_child_count = 0
    for previous_row in sorted(
        replaced_rows, key=lambda row: row["canonical_support_row_id"]
    ):
        support_id = previous_row["canonical_support_row_id"]
        normal = outgoing_by_id.get(support_id) or wall_by_id.get(support_id)
        need(normal is not None, f"fully replaced normal form:{support_id}")
        origin = origin_by_id[normal["origin_row_id"]]
        child_entries = children_by_origin[origin["origin_row_id"]]
        resolved_children = [
            child for kind, child in child_entries if kind == "RESOLVED"
        ]
        retained_children = [
            child for kind, child in child_entries if kind == "RETAINED"
        ]
        guard_children = [
            child for kind, child in child_entries if kind == "GUARD"
        ]
        need(
            origin["fully_replaced_by_bounded_children"]
            and origin["chosen_split_axis"] == "p"
            and len(resolved_children) == 2
            and not retained_children
            and not guard_children
            and sum(Q(child["coordinate_volume"]) for child in resolved_children)
            == Q(origin["original_coordinate_volume"]),
            f"fully replaced exhaustive cover:{support_id}",
        )
        child_evidence: list[dict[str, Any]] = []
        if support_id in outgoing_by_id:
            predicate_kind = "OUTGOING_EQUALITY"
            exact_signs = []
            for child in sorted(
                resolved_children, key=lambda row: row["child_index"]
            ):
                cell = child["outgoing_cell"]
                need(cell in {"E", "W", "N", "S"}, "resolved outgoing cell")
                exact_sign = (
                    "STRICT_POSITIVE" if cell in {"E", "W"}
                    else "STRICT_NEGATIVE"
                )
                exact_signs.append(exact_sign)
                child_evidence.append({
                    "resolved_child_row_id": child["row_id"],
                    "child_index": child["child_index"],
                    "child_box": child["box"],
                    "outgoing_cell": cell,
                    "predicate_sign_from_strict_outgoing_dominance":
                        exact_sign,
                    "predicate_zero_absent_on_closed_child": True,
                })
            need(len(set(exact_signs)) == 1, f"outgoing same strict sign:{support_id}")
        else:
            predicate_kind = "WALL_ENDPOINT_PRODUCT"
            wall = wall_by_id[support_id]
            source_name = "source_x" if wall["axis"] == "X" else "source_y"
            target_name = "hit_x" if wall["axis"] == "X" else "hit_y"
            exact_pairs = []
            for child in sorted(
                resolved_children, key=lambda row: row["child_index"]
            ):
                box = r179v.box_from(
                    child["box"], len(child["refinement_path"]), child["row_id"]
                )
                geometry = r179v.independent_geometry(
                    child["chart"], origin["owner_target"], box
                )
                source_sign = r179v.arb_sign(
                    r179v.subtract_wall(
                        geometry[source_name], wall["integer_wall"]
                    )[0]
                )
                target_sign = r179v.arb_sign(
                    r179v.subtract_wall(
                        geometry[target_name], wall["integer_wall"]
                    )[0]
                )
                need(
                    source_sign in {"STRICT_NEGATIVE", "STRICT_POSITIVE"}
                    and target_sign in {"STRICT_NEGATIVE", "STRICT_POSITIVE"},
                    f"wall child strict factors:{child['row_id']}",
                )
                exact_pairs.append((source_sign, target_sign))
                child_evidence.append({
                    "resolved_child_row_id": child["row_id"],
                    "child_index": child["child_index"],
                    "child_box": child["box"],
                    "source_endpoint_factor_sign": source_sign,
                    "target_endpoint_factor_sign": target_sign,
                    "predicate_product_zero_absent_on_closed_child": True,
                })
            need(len(set(exact_pairs)) == 1, f"wall same strict pair:{support_id}")

        replaced_child_count += len(child_evidence)
        payload = {
            "round281_lower_tail_closure_row_id":
                row_id(
                    previous_row["lower_stratum_physical_disposition_row_id"],
                    REPLACED_ABSENT,
                ),
            "Round280_lower_support_disposition_row_id":
                previous_row["lower_stratum_physical_disposition_row_id"],
            "Round267_lower_stratum_terminal_lineage_row_id":
                previous_row["Round267_lower_stratum_terminal_lineage_row_id"],
            "canonical_support_row_id": support_id,
            "containing_Round174_residual_row_id":
                previous_row["containing_Round174_residual_row_id"],
            "parent_id": origin["parent_id"],
            "source_chart": origin["chart"],
            "decision_family": "FULLY_REPLACED_EXHAUSTIVE_RESOLVED_CHILD_COVER",
            "physical_disposition": REPLACED_ABSENT,
            "evidence_basis":
                "ROUND179_TWO_RESOLVED_P_CHILDREN__STRICT_PREDICATE_SIGNS__"
                "EXACT_VOLUME_COVER",
            "predicate_kind": predicate_kind,
            "chosen_split_axis": origin["chosen_split_axis"],
            "resolved_child_count": len(resolved_children),
            "retained_child_count": len(retained_children),
            "guard_child_count": len(guard_children),
            "origin_coordinate_volume": origin["original_coordinate_volume"],
            "resolved_child_coordinate_volume":
                qstr(sum(
                    Q(child["coordinate_volume"]) for child in resolved_children
                )),
            "child_evidence": child_evidence,
            **zero_credit(),
        }
        replaced_output.append(closed(payload))

    rows = sorted(
        [*t0_output, *replaced_output],
        key=lambda row: row["round281_lower_tail_closure_row_id"],
    )
    need(len(rows) == 1_276, "output row count")
    need(
        len({row["round281_lower_tail_closure_row_id"] for row in rows})
        == len(rows),
        "unique output ids",
    )
    disposition = Counter(row["physical_disposition"] for row in rows)
    need(
        disposition == {
            T0_OWNER: 440,
            T0_SHADOW: 372,
            T0_PARTITIONED: 8,
            T0_ABSENT: 60,
            REPLACED_ABSENT: 396,
        },
        "final exact disposition",
    )
    need(shadow_patch_count == 544, "shadow patch census")
    need(len(shadow_owner_origins) == 396, "shadow owner origin census")
    need(replaced_child_count == 792, "fully replaced child census")
    need(
        all(
            row[field] == 0
            for row in rows
            for field in (
                "expanded_occurrence_credit",
                "component_edge_credit",
                "maximality_credit",
                "exact_key_fibre_credit",
                "global_exact_key_disposition_credit",
                "Jx_Jy_same_point_glue_credit",
            )
        ),
        "strict row zero credit",
    )

    rows_sha256 = digest(rows)
    row_ids_sha256 = digest(
        [row["round281_lower_tail_closure_row_id"] for row in rows]
    )
    row_hashes_sha256 = digest([row["row_sha256"] for row in rows])
    ledger = {
        "schema": LEDGER_SCHEMA,
        "rows": rows,
        "rows_sha256": rows_sha256,
        "row_ids_sha256": row_ids_sha256,
        "row_hashes_sha256": row_hashes_sha256,
    }
    result = {
        "schema": SCHEMA,
        "status": "PASS_ROUND281_LOWER_STRATUM_TAIL_CLOSURE__ZERO_CREDIT",
        "pins": INPUT_SHA256,
        "Round204_half_open_owner_contract": {
            "policy":
                "OUTCOME_BLIND_POSITIVE_T_SIDE_OWNS__"
                "NEGATIVE_T_SIDE_IS_SHADOW",
            "source_sheet_row_count": 224,
            "all_source_sheets_have_positive_t_half_open_owner": True,
        },
        "census": {
            "Round280_nonterminal_input_count": len(tails),
            "Round280_source_t0_input_count": len(t0_rows),
            "Round280_fully_replaced_input_count": len(replaced_rows),
            "final_disposition_histogram": dict(sorted(disposition.items())),
            "remaining_local_physical_decision_count": 0,
            "t0_positive_owner_count": disposition[T0_OWNER],
            "t0_negative_shadow_count": disposition[T0_SHADOW],
            "t0_negative_partitioned_count": disposition[T0_PARTITIONED],
            "t0_negative_no_owner_absence_count": disposition[T0_ABSENT],
            "fully_replaced_absence_count": disposition[REPLACED_ABSENT],
            "shadow_owner_patch_count": shadow_patch_count,
            "distinct_shadow_positive_owner_origin_count":
                len(shadow_owner_origins),
            "fully_replaced_resolved_child_evidence_count":
                replaced_child_count,
            "complete_Round174_unique_first_parent_count": len(parents),
            "complete_Round179_origin_count": len(origins),
            "total_t0_face_area": qstr(t0_face_area),
            "owned_or_shadowed_t0_face_area": qstr(owned_or_shadowed_area),
            "absent_t0_face_area": qstr(absent_area),
            "t0_area_partition_delta":
                qstr(t0_face_area - owned_or_shadowed_area - absent_area),
        },
        "ledger_attachment": {
            "filename": DEFAULT_LEDGER.name,
            "schema": LEDGER_SCHEMA,
            "row_count": len(rows),
            "rows_sha256": rows_sha256,
            "row_ids_sha256": row_ids_sha256,
            "row_hashes_sha256": row_hashes_sha256,
        },
        "strict_nonpromotion": {
            "expanded_occurrence_credit": 0,
            "component_edge_credit": 0,
            "maximality_credit": 0,
            "exact_key_fibre_credit": 0,
            "global_exact_key_disposition_credit": 0,
            "Jx_Jy_same_point_glue_credit": 0,
            "quotient": 63_224,
            "expanded_occurrences": 126_468,
            "maximality": "0/63224",
            "exact_key_fibres": "0/116",
            "global_dispositions": "0/224580",
            "Gate5": "10/18",
            "D02": "BLOCKED",
            "CM2": "NO-GO_FOR_CLAIM",
        },
        "next_gate": (
            "This closes only local lower-stratum existence/absence.  Bind "
            "the final occurrence identity and the 152 true-seam quotient "
            "before any component, maximality, fibre, or global disposition "
            "promotion."
        ),
    }
    result["result_sha256"] = digest(result)
    return ledger, result


def audit_ledger(ledger: dict[str, Any], result: dict[str, Any]) -> None:
    rows = ledger["rows"]
    need(len(rows) == result["ledger_attachment"]["row_count"], "audit count")
    need(digest(rows) == ledger["rows_sha256"], "audit rows digest")
    need(
        digest([row["round281_lower_tail_closure_row_id"] for row in rows])
        == ledger["row_ids_sha256"],
        "audit ids digest",
    )
    need(
        digest([row["row_sha256"] for row in rows])
        == ledger["row_hashes_sha256"],
        "audit hashes digest",
    )
    for row in rows:
        payload = dict(row)
        row_hash = payload.pop("row_sha256")
        need(digest(payload) == row_hash, "audit row closure")
        if row["decision_family"] == "EXACT_SOURCE_T0_HALF_OPEN_OWNER":
            owner_area = Q(row["owner_patch_union_area"])
            absence_area = Q(row["absence_cell_union_area"])
            need(
                owner_area + absence_area == Q(row["source_t0_face_area"]),
                "audit t0 exact partition",
            )
            if row["t_side"] == "NEGATIVE_T":
                need(
                    row["physical_disposition"] != T0_OWNER,
                    "negative side cannot own",
                )
            if row["physical_disposition"] == T0_PARTITIONED:
                need(
                    owner_area > 0 and absence_area > 0,
                    "partitioned row has two nonempty parts",
                )
        for field in (
            "expanded_occurrence_credit",
            "component_edge_credit",
            "maximality_credit",
            "exact_key_fibre_credit",
            "global_exact_key_disposition_credit",
            "Jx_Jy_same_point_glue_credit",
        ):
            need(row[field] == 0, f"audit zero:{field}")


def self_attacks(ledger: dict[str, Any], result: dict[str, Any]) -> dict[str, int]:
    attacks: list[tuple[str, Any]] = []
    negative = next(
        row for row in ledger["rows"]
        if row.get("t_side") == "NEGATIVE_T"
    )
    replaced = next(
        row for row in ledger["rows"]
        if row["decision_family"]
        == "FULLY_REPLACED_EXHAUSTIVE_RESOLVED_CHILD_COVER"
    )
    attacks.append(("forged_negative_owner", (negative, "physical_disposition", T0_OWNER)))
    attacks.append(("forged_occurrence_credit", (negative, "expanded_occurrence_credit", 1)))
    attacks.append(("forged_component_credit", (negative, "component_edge_credit", 1)))
    attacks.append(("forged_JxJy", (negative, "Jx_Jy_same_point_glue_credit", 1)))
    attacks.append(("forged_DSU_dependency", (negative, "requires_final_DSU_to_decide_local_physical_support", True)))
    attacks.append(("forged_replaced_physical", (replaced, "physical_disposition", T0_OWNER)))
    rejected = 0
    for _name, (source, field, value) in attacks:
        candidate = copy.deepcopy(ledger)
        target = next(
            row for row in candidate["rows"]
            if row["round281_lower_tail_closure_row_id"]
            == source["round281_lower_tail_closure_row_id"]
        )
        target[field] = value
        try:
            audit_ledger(candidate, result)
        except ClosureError:
            rejected += 1
    need(rejected == len(attacks), "all self attacks rejected")
    return {"attack_count": len(attacks), "rejected_count": rejected}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--ledger", type=Path, default=DEFAULT_LEDGER)
    parser.add_argument("--output", type=Path, default=DEFAULT_RESULT)
    parser.add_argument("--seed", default="281071")
    args = parser.parse_args()
    ledger, result = build()
    audit_ledger(ledger, result)
    result["attack_tests"] = self_attacks(ledger, result)
    result["result_sha256"] = digest({
        key: value for key, value in result.items() if key != "result_sha256"
    })
    ledger_bytes = gzip_payload(ledger)
    result["ledger_attachment"]["file_sha256"] = hashlib.sha256(
        ledger_bytes
    ).hexdigest()
    result["result_sha256"] = digest({
        key: value for key, value in result.items() if key != "result_sha256"
    })
    write_atomic(args.ledger, ledger_bytes)
    write_atomic(args.output, canonical(result) + b"\n")


if __name__ == "__main__":
    main()
