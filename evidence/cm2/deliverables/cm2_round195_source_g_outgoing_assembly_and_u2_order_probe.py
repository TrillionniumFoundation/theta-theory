#!/usr/bin/env python3
"""Read-only final-face assembly probe for the source-G outgoing-W tail.

This spike assembles the mutually exclusive Round186, Round188, and Round191
face normal forms for all 18,412 unresolved t-face incidences in the 18,324
Round182 outgoing-W residual leaves.  It then rebuilds a per-leaf
EMPTY/FULL/CLIPPED dimensional ledger.

The 88 U|U leaves receive an additional whole-3D-box audit: both t-face
normal forms must use one compatible active factor/graph atlas, and that
factor must have strict t and p derivatives on the entire leaf box.  For
two-curve leaves, the sign of -dt/dp gives a strict cross-t p ordering and
excludes curve intersection.

The result is a feasibility probe only.  It writes no certificate or
attachment, exposes no output-path option, materializes no return signature,
and issues no local-as-global exact-key credit.

Probe-only trust boundary: imported Round191/188/186 modules execute before
this module can pin their bytes.  All sources, reports, and the complete
Round182 verified package are pinned immediately afterwards.  A formal
verifier must pin inert producer bytes before loading an independent
evaluator.
"""

from __future__ import annotations

import argparse
from collections import Counter
from fractions import Fraction as Q
import hashlib
import json
from pathlib import Path
import sys
from typing import Any

from flint import ctx

import cm2_round191_source_g_stereographic_endpoint_chart_probe as r191


HERE = Path(__file__).resolve().parent
SCHEMA = "cm2.round195.source-g-outgoing-assembly-and-u2-order-probe.v1"

ROUND186_SOURCE = "cm2_round186_source_g_factor_face_probe.py"
ROUND186_SOURCE_SHA256 = (
    "5797b8f4c2ba9c8c5b42b32511f3c97a15469b59bdf00cd8430580c3429c7c64"
)
ROUND186_REPORT = "cm2_round186_source_g_factor_face_spike_report.md"
ROUND186_REPORT_SHA256 = (
    "43112bf127a717b1e0ed4403d5c4a3290847a9e575208195354f2aff03562bcf"
)
ROUND188_SOURCE = (
    "cm2_round188_source_g_factor_face_boundary_arrangement_probe.py"
)
ROUND188_SOURCE_SHA256 = (
    "11e033c726a51bab875f42c371682814a84f46871f1a45797d5c68aa3b3149de"
)
ROUND188_REPORT = (
    "cm2_round188_source_g_factor_face_boundary_arrangement_spike_report.md"
)
ROUND188_REPORT_SHA256 = (
    "7b3cf3cd5faaf2e987266fe4ac11740dc2e0c2be0a9a0faf00d2849830a161f6"
)
ROUND191_SOURCE = (
    "cm2_round191_source_g_stereographic_endpoint_chart_probe.py"
)
ROUND191_SOURCE_SHA256 = (
    "b37c0a06a392107d7d859c65ab323cf04c7f06cdd4f51cba59c2049c53f70b9f"
)
ROUND191_REPORT = (
    "cm2_round191_source_g_stereographic_endpoint_chart_spike_report.md"
)
ROUND191_REPORT_SHA256 = (
    "a0b1bfd51b7fcfb23f6f8b77ab20f5f4769bbe2228ff2ca2c20b539f9082aa2d"
)

EXPECTED_OUTGOING_LEAVES = 18_324
EXPECTED_OUTGOING_ORIGINS = 8_268
EXPECTED_RETAINED_CHILDREN = 11_960
EXPECTED_OUTGOING_VOLUME = Q(861459, 419430400000)
EXPECTED_UNRESOLVED_FACES = 18_412
EXPECTED_SINGLE_U_LEAVES = 18_236
EXPECTED_U2_LEAVES = 88
EXPECTED_U2_ORIGINS = 76
EXPECTED_WALL_G_RESIDUAL_LEAVES = 64

EXPECTED_FINAL_FACE_METHODS = {
    "ROUND186_BOTH_FACTORS_STRICT_ZERO_ABSENT": 4,
    "ROUND186_ONE_ACTIVE_FACTOR_STRICT_ZERO_ABSENT": 1_172,
    "ROUND186_ONE_ACTIVE_FACTOR_FULL_GRAPH": 1_104,
    "ROUND188_UNIQUE_TWO_ENDPOINT_FACTOR_CURVE": 15_844,
    "ROUND191_UNIQUE_TWO_ENDPOINT_STEREOGRAPHIC_FACTOR_CURVE": 256,
    "ROUND191_STRICT_MONOTONE_ACTIVE_FACTOR_ABSENT": 32,
}
EXPECTED_FINAL_FACE_AREA = Q(31351, 26214400)
EXPECTED_FINAL_FACE_INCIDENT_VOLUME = Q(1726989, 838860800000)
EXPECTED_FINAL_FACE_ROWS_SHA256 = (
    "0efb78285bc7836c84860f157ab4ec45593029aa523a95fd62171d307d7a5396"
)
EXPECTED_LEAF_CLASSES = {
    "CLIPPED_2D_BOUNDARY_1D": 17_308,
    "EMPTY": 608,
    "FULL_2D": 408,
}
EXPECTED_LEAF_CLASS_VOLUMES = {
    "CLIPPED_2D_BOUNDARY_1D": Q(824643, 419430400000),
    "EMPTY": Q(47259, 838860800000),
    "FULL_2D": Q(26373, 838860800000),
}
EXPECTED_DIMENSION_TOTALS = {
    "0D_boundary_endpoint_incidences": 40_912,
    "1D_clipping_curve_segments": 20_456,
    "2D_graph_sheets": 17_716,
    "side_specific_signature_candidate_regions": 36_040,
}
EXPECTED_CANDIDATE_REGION_SIGNS = {
    "STRICT_NEGATIVE": 18_024,
    "STRICT_POSITIVE": 18_016,
}
EXPECTED_LEAF_ROWS_SHA256 = (
    "0370fb57e9d2881a8bc2d0e66351a6c551e147d483558c682f051153924f88b5"
)
EXPECTED_ORIGIN_ROWS_SHA256 = (
    "57cdf91214dbc632ee39cb657a79e83344d34600376e85e12faec7de8ddaaa80"
)
EXPECTED_U2_VOLUME = Q(4071, 838860800000)
EXPECTED_U2_DIMENSIONS = {
    "0D_boundary_endpoint_incidences": 328,
    "1D_clipping_curve_segments": 164,
    "2D_graph_sheets": 88,
    "side_specific_signature_candidate_regions": 176,
}
EXPECTED_U2_ROWS_SHA256 = (
    "12fbc70f82645ae2ad252b4e88587a7841814a03fda1972a0241cd63c45d6ee0"
)

STRICT_SIGNS = {"STRICT_NEGATIVE", "STRICT_POSITIVE"}
NO_BRACKET = "ONE_ACTIVE_FACTOR_STRICT_DERIVATIVE_NO_BRACKET"
ROUND188_CURVE = "UNIQUE_TWO_ENDPOINT_FACTOR_CURVE"
ROUND188_ENDPOINT_RESIDUAL = "BOUNDARY_ENDPOINT_COUNT_RESIDUAL"
ROUND191_CURVE = "UNIQUE_TWO_ENDPOINT_STEREOGRAPHIC_FACTOR_CURVE"
ROUND191_ABSENT = "STRICT_MONOTONE_ACTIVE_FACTOR_ABSENT"


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


def multiply_signs(left: str, right: str) -> str:
    require(left in STRICT_SIGNS and right in STRICT_SIGNS, "strict factors")
    return (
        "STRICT_POSITIVE"
        if left == right
        else "STRICT_NEGATIVE"
    )


def implicit_order_sign(dt_sign: str, dp_sign: str) -> str:
    """Sign of dp_zero/dt = -partial_t(h)/partial_p(h)."""

    require(dt_sign in STRICT_SIGNS, "strict factor dt")
    require(dp_sign in STRICT_SIGNS, "strict factor dp")
    return (
        "STRICT_NEGATIVE"
        if dt_sign == dp_sign
        else "STRICT_POSITIVE"
    )


def full_axis_rows(
    profile: dict[str, Any],
    active: str,
    classification: str,
) -> list[tuple[Any, ...]]:
    return sorted(
        (
            tuple(row)
            for row in profile[active][1]
            if row[-1] == classification
        ),
        key=lambda row: row[0],
    )


def active_and_inactive(
    profile: dict[str, Any],
) -> tuple[str, str]:
    active = [
        kind
        for kind in ("HPLUS", "HMINUS")
        if profile[kind][0] == "OVERWRAP"
    ]
    inactive = [
        kind
        for kind in ("HPLUS", "HMINUS")
        if profile[kind][0] in STRICT_SIGNS
    ]
    require(
        len(active) == len(inactive) == 1,
        "one active and one inactive factor",
    )
    return active[0], inactive[0]


def curve_edge_pair_for_full_axis(axis: str) -> str:
    if axis == "p":
        return "N|S"
    if axis == "s":
        return "E|W"
    raise RuntimeError(f"unsupported full graph axis:{axis}")


def final_unresolved_face(
    row: dict[str, Any],
    collar: dict[str, Any],
    box: Any,
    side: str,
    upper: bool,
) -> dict[str, Any]:
    """Assemble exactly one U face into one final mutually exclusive form."""

    r188 = r191.r189.r188
    r186 = r188.r186
    profile, normal_excluded = r186.face_profile(
        collar["chart"],
        collar["owner_target"],
        box,
        upper,
    )
    require(normal_excluded, f"normal exclusion:{row['row_id']}:{side}")
    baseline = r186.resolution(profile)
    method: str
    zero_set_kind: str
    active_factor: str | None
    inactive_factor: str | None
    inactive_factor_sign: str | None
    active_factor_sign: str | None
    outgoing_factorized_sign: str | None
    graph_axis: str | None
    edge_pair: str
    endpoint_count: int
    evidence_sha256: str

    if baseline == "BOTH_FACTORS_STRICT":
        signs = {
            kind: profile[kind][0]
            for kind in ("HPLUS", "HMINUS")
        }
        require(
            all(value in STRICT_SIGNS for value in signs.values()),
            "both factor signs strict",
        )
        method = "ROUND186_BOTH_FACTORS_STRICT_ZERO_ABSENT"
        zero_set_kind = "ABSENT"
        active_factor = None
        inactive_factor = None
        inactive_factor_sign = None
        active_factor_sign = None
        outgoing_factorized_sign = multiply_signs(
            signs["HPLUS"], signs["HMINUS"]
        )
        graph_axis = None
        edge_pair = ""
        endpoint_count = 0
        evidence_sha256 = digest(profile)
    elif baseline == "ONE_ACTIVE_FACTOR_ABSENT":
        active_factor, inactive_factor = active_and_inactive(profile)
        inactive_factor_sign = profile[inactive_factor][0]
        axes = full_axis_rows(
            profile,
            active_factor,
            "STRICT_ZERO_ABSENT",
        )
        require(axes, "Round186 active-factor absence axis")
        active_signs = {
            row_axis[2]
            for row_axis in axes
            if row_axis[2] == row_axis[3]
            and row_axis[2] in STRICT_SIGNS
        }
        require(
            len(active_signs) == 1,
            "Round186 absence sign consistency",
        )
        active_factor_sign = next(iter(active_signs))
        outgoing_factorized_sign = multiply_signs(
            active_factor_sign,
            inactive_factor_sign,
        )
        method = "ROUND186_ONE_ACTIVE_FACTOR_STRICT_ZERO_ABSENT"
        zero_set_kind = "ABSENT"
        graph_axis = axes[0][0]
        edge_pair = ""
        endpoint_count = 0
        evidence_sha256 = digest(profile)
    elif baseline == "ONE_ACTIVE_FACTOR_FULL_GRAPH":
        active_factor, inactive_factor = active_and_inactive(profile)
        inactive_factor_sign = profile[inactive_factor][0]
        axes = full_axis_rows(
            profile,
            active_factor,
            "FULL_BASE_UNIQUE_GRAPH",
        )
        require(axes, "Round186 active-factor full graph axis")
        graph_axis = axes[0][0]
        require(
            all(axis[0] == graph_axis for axis in axes),
            "Round186 selected graph atlas",
        )
        method = "ROUND186_ONE_ACTIVE_FACTOR_FULL_GRAPH"
        zero_set_kind = "CURVE"
        active_factor_sign = None
        outgoing_factorized_sign = None
        edge_pair = curve_edge_pair_for_full_axis(graph_axis)
        endpoint_count = 2
        evidence_sha256 = digest(profile)
    elif baseline == NO_BRACKET:
        active_factor, inactive_factor = active_and_inactive(profile)
        inactive_factor_sign = profile[inactive_factor][0]
        arrangement = r188.boundary_arrangement(
            collar,
            box,
            upper,
            profile,
        )
        require(
            arrangement["active_factor"] == active_factor
            and arrangement["inactive_factor"] == inactive_factor,
            "Round188 factor identity",
        )
        if arrangement["status"] == ROUND188_CURVE:
            method = "ROUND188_UNIQUE_TWO_ENDPOINT_FACTOR_CURVE"
            zero_set_kind = "CURVE"
            active_factor_sign = None
            outgoing_factorized_sign = None
            graph_axis = arrangement["graph_axis"]
            edge_pair = arrangement["edge_pair"]
            endpoint_count = 2
            evidence_sha256 = digest(arrangement)
        else:
            require(
                arrangement["status"] == ROUND188_ENDPOINT_RESIDUAL,
                f"unexpected Round188 residual:{arrangement['status']}",
            )
            touches_negative = box.p0 == Q(-1)
            touches_positive = box.p1 == Q(1)
            require(
                touches_negative != touches_positive,
                "Round188 endpoint face touches exactly one p endpoint",
            )
            endpoint = "p=-1" if touches_negative else "p=+1"
            item = {
                "leaf_row": row,
                "collar": collar,
                "box": box,
                "side": side,
                "upper": upper,
                "initial_arrangement": arrangement,
                "endpoint": endpoint,
                "two_sided_U_leaf":
                    row["lower_t_face_status"] == "U"
                    and row["upper_t_face_status"] == "U",
            }
            transformed = r191.transformed_arrangement(item)
            require(
                transformed["face_level_resolved"],
                "Round191 endpoint face final resolution",
            )
            active_factor = transformed["active_factor"]
            inactive_factor = transformed["inactive_factor"]
            inactive_factor_sign = transformed[
                "inactive_factor_C0"
            ]["selected_sign"]
            graph_axis = transformed["graph_axis"]
            edge_pair = transformed["edge_pair"]
            endpoint_count = transformed[
                "boundary_unique_endpoint_count"
            ]
            evidence_sha256 = digest(transformed)
            if transformed["status"] == ROUND191_CURVE:
                method = (
                    "ROUND191_UNIQUE_TWO_ENDPOINT_STEREOGRAPHIC_FACTOR_CURVE"
                )
                zero_set_kind = "CURVE"
                active_factor_sign = None
                outgoing_factorized_sign = None
                require(endpoint_count == 2, "Round191 curve endpoints")
            else:
                require(
                    transformed["status"] == ROUND191_ABSENT,
                    f"unexpected Round191 status:{transformed['status']}",
                )
                method = (
                    "ROUND191_STRICT_MONOTONE_ACTIVE_FACTOR_ABSENT"
                )
                zero_set_kind = "ABSENT"
                signs = transformed["graph_axis_endpoint_C0_signs"]
                require(
                    len(signs) == 2
                    and signs[0] == signs[1]
                    and signs[0] in STRICT_SIGNS,
                    "Round191 active absence sign",
                )
                active_factor_sign = signs[0]
                outgoing_factorized_sign = multiply_signs(
                    active_factor_sign,
                    inactive_factor_sign,
                )
                require(endpoint_count == 0, "Round191 absent endpoints")
    else:
        raise RuntimeError(f"unhandled Round186 class:{baseline}")

    require(
        method in EXPECTED_FINAL_FACE_METHODS,
        "known mutually exclusive final face method",
    )
    face_area = (box.p1 - box.p0) * (box.s1 - box.s0)
    require(face_area > 0, "strict t-face coordinate area")
    return {
        "face_row_id": row["row_id"] + ":" + side,
        "leaf_row_id": row["row_id"],
        "occurrence_row_id": row["occurrence_row_id"],
        "origin_row_id": collar["origin_row_id"],
        "side": side,
        "t_coordinate": str(box.t1 if upper else box.t0),
        "face_coordinate_area": str(face_area),
        "incident_leaf_coordinate_volume": row["coordinate_volume"],
        "baseline_Round186_class": baseline,
        "final_method": method,
        "zero_set_kind": zero_set_kind,
        "active_factor": active_factor,
        "inactive_factor": inactive_factor,
        "inactive_factor_sign": inactive_factor_sign,
        "active_factor_absence_sign": active_factor_sign,
        "outgoing_factorized_sign": outgoing_factorized_sign,
        "graph_axis": graph_axis,
        "boundary_edge_pair": edge_pair,
        "boundary_endpoint_incidence_count": endpoint_count,
        "target_normal_zero_excluded": True,
        "evidence_sha256": evidence_sha256,
        "whole_leaf_credit": 0,
        "global_exact_key_disposition_credit": 0,
    }


def decode_round182_face(encoded: str) -> dict[str, Any]:
    sign = {"+": "STRICT_POSITIVE", "-": "STRICT_NEGATIVE"}
    require(encoded != "U", "U face must use final assembly")
    if encoded.startswith("S"):
        require(len(encoded) == 2 and encoded[1] in sign, "strict face code")
        return {
            "provenance": "ROUND182_STRICT_FACE",
            "zero_set_kind": "ABSENT",
            "resolved_sign": sign[encoded[1]],
            "graph_axis": None,
            "boundary_edge_pair": "",
            "boundary_endpoint_incidence_count": 0,
            "active_factor": None,
        }
    require(
        len(encoded) == 7
        and encoded[0] in {"A", "C"}
        and encoded[1] in {"p", "s"},
        f"Round182 encoded face:{encoded}",
    )
    if encoded[0] == "A":
        require(encoded[5] in sign, f"Round182 absence sign:{encoded}")
        return {
            "provenance": "ROUND182_AXIS_ZERO_ABSENT_FACE",
            "zero_set_kind": "ABSENT",
            "resolved_sign": sign[encoded[5]],
            "graph_axis": encoded[1],
            "boundary_edge_pair": "",
            "boundary_endpoint_incidence_count": 0,
            "active_factor": None,
        }
    require(encoded[5] == "_", f"Round182 curve unresolved sign:{encoded}")
    return {
        "provenance": "ROUND182_FULL_BASE_UNIQUE_GRAPH_FACE",
        "zero_set_kind": "CURVE",
        "resolved_sign": None,
        "graph_axis": encoded[1],
        "boundary_edge_pair":
            curve_edge_pair_for_full_axis(encoded[1]),
        "boundary_endpoint_incidence_count": 2,
        "active_factor": None,
    }


def side_summary(face: dict[str, Any]) -> dict[str, Any]:
    return {
        "provenance": face["final_method"],
        "zero_set_kind": face["zero_set_kind"],
        "resolved_sign": face["outgoing_factorized_sign"],
        "graph_axis": face["graph_axis"],
        "boundary_edge_pair": face["boundary_edge_pair"],
        "boundary_endpoint_incidence_count":
            face["boundary_endpoint_incidence_count"],
        "active_factor": face["active_factor"],
    }


def classify_leaf(
    row: dict[str, Any],
    collar: dict[str, Any],
    box: Any,
    lower: dict[str, Any],
    upper: dict[str, Any],
) -> dict[str, Any]:
    r186 = r191.r189.r188.r186
    faces = [lower, upper]
    require(
        all(face["zero_set_kind"] in {"ABSENT", "CURVE"} for face in faces),
        "both t faces locally resolved",
    )
    curve_count = sum(
        face["zero_set_kind"] == "CURVE" for face in faces
    )
    geometry = r186.factor_geometry(
        collar["chart"],
        collar["owner_target"],
        box,
    )
    outgoing = r186.r179.dmul(
        geometry["HPLUS"],
        geometry["HMINUS"],
    )
    t_derivative_sign = r186.r179.arb_sign(outgoing[1][0])
    require(
        t_derivative_sign in STRICT_SIGNS,
        f"strict whole-leaf outgoing t derivative:{row['row_id']}",
    )
    require(
        t_derivative_sign == collar["strict_t_derivative_sign"],
        f"Round182 collar t derivative agreement:{row['row_id']}",
    )

    if curve_count:
        classification = "CLIPPED_2D_BOUNDARY_1D"
        sheet_count = 1
        resolved_sign = None
    else:
        signs = [face["resolved_sign"] for face in faces]
        require(
            all(sign in STRICT_SIGNS for sign in signs),
            f"strict absent face signs:{row['row_id']}",
        )
        if signs[0] == signs[1]:
            classification = "EMPTY"
            sheet_count = 0
            resolved_sign = signs[0]
        else:
            classification = "FULL_2D"
            sheet_count = 1
            resolved_sign = None

    region_count = 1 if classification == "EMPTY" else 2
    candidate_signs = (
        [resolved_sign]
        if classification == "EMPTY"
        else ["STRICT_NEGATIVE", "STRICT_POSITIVE"]
    )
    volume = Q(row["coordinate_volume"])
    require(volume > 0, "strict outgoing leaf volume")
    return {
        "leaf_row_id": row["row_id"],
        "occurrence_row_id": row["occurrence_row_id"],
        "origin_row_id": collar["origin_row_id"],
        "retained_child_row_id": row["retained_child_row_id"],
        "box": row["box"],
        "coordinate_volume": str(volume),
        "base_coordinate_area": row["base_coordinate_area"],
        "lower_t_face": lower,
        "upper_t_face": upper,
        "final_graph_classification": classification,
        "two_dimensional_graph_sheet_count": sheet_count,
        "one_dimensional_clipping_curve_segment_count": curve_count,
        "zero_dimensional_boundary_endpoint_incidence_count":
            2 * curve_count,
        "whole_leaf_outgoing_t_derivative_sign": t_derivative_sign,
        "side_specific_signature_candidate_region_count": region_count,
        "candidate_region_signs": candidate_signs,
        "side_specific_return_signatures_materialized": False,
        "local_geometric_residual": False,
        "whole_leaf_credit": 0,
        "global_exact_key_disposition_credit": 0,
    }


def audit_u2_leaf(
    leaf: dict[str, Any],
    raw_row: dict[str, Any],
    collar: dict[str, Any],
    box: Any,
    lower_face_row: dict[str, Any],
    upper_face_row: dict[str, Any],
) -> dict[str, Any]:
    r186 = r191.r189.r188.r186
    require(box.t0 < box.t1, "U|U strict t interval")
    faces = [lower_face_row, upper_face_row]
    require(
        all(face is not None for face in faces),
        "U|U has two final face rows",
    )
    active = {
        face["active_factor"]
        for face in faces
        if face["active_factor"] is not None
    }
    require(len(active) == 1, f"U|U active factor agreement:{leaf['leaf_row_id']}")
    active_factor = next(iter(active))
    require(
        all(
            face["active_factor"] == active_factor
            for face in faces
        ),
        f"U|U both faces use same active factor:{leaf['leaf_row_id']}",
    )
    atlas_axes = {
        face["graph_axis"]
        for face in faces
        if face["graph_axis"] is not None
    }
    require(
        atlas_axes == {"p"},
        f"U|U compatible p atlas:{leaf['leaf_row_id']}",
    )

    factor = r186.factor_geometry(
        collar["chart"],
        collar["owner_target"],
        box,
    )[active_factor]
    dt_sign = r186.r179.arb_sign(factor[1][0])
    dp_sign = r186.r179.arb_sign(factor[1][1])
    ds_sign = r186.r179.arb_sign(factor[1][2])
    require(
        dt_sign in STRICT_SIGNS
        and dp_sign in STRICT_SIGNS
        and ds_sign in STRICT_SIGNS,
        f"U|U full-box strict active derivatives:{leaf['leaf_row_id']}",
    )
    curve_faces = [
        face for face in faces if face["zero_set_kind"] == "CURVE"
    ]
    require(
        len(curve_faces) in {1, 2},
        f"U|U curve-face count:{leaf['leaf_row_id']}",
    )
    if len(curve_faces) == 2:
        order_sign = implicit_order_sign(dt_sign, dp_sign)
        ordering = (
            "UPPER_CURVE_STRICTLY_GREATER_P_THAN_LOWER_CURVE"
            if order_sign == "STRICT_POSITIVE"
            else "UPPER_CURVE_STRICTLY_LESS_P_THAN_LOWER_CURVE"
        )
        curve_pair_nonintersection = True
        cross_t_status = "TWO_CURVES_STRICTLY_ORDERED_AND_DISJOINT"
    else:
        order_sign = None
        ordering = None
        curve_pair_nonintersection = True
        cross_t_status = "ONE_CURVE_OTHER_T_FACE_STRICTLY_ZERO_ABSENT"

    return {
        "leaf_row_id": leaf["leaf_row_id"],
        "origin_row_id": collar["origin_row_id"],
        "occurrence_row_id": leaf["occurrence_row_id"],
        "coordinate_volume": leaf["coordinate_volume"],
        "active_factor": active_factor,
        "lower_final_method": lower_face_row["final_method"],
        "upper_final_method": upper_face_row["final_method"],
        "lower_graph_axis": lower_face_row["graph_axis"],
        "upper_graph_axis": upper_face_row["graph_axis"],
        "lower_boundary_edge_pair":
            lower_face_row["boundary_edge_pair"],
        "upper_boundary_edge_pair":
            upper_face_row["boundary_edge_pair"],
        "curve_t_face_count": len(curve_faces),
        "whole_3D_box_active_factor_dt_sign": dt_sign,
        "whole_3D_box_active_factor_dp_sign": dp_sign,
        "whole_3D_box_active_factor_ds_sign": ds_sign,
        "implicit_curve_p_order_derivative_sign": order_sign,
        "strict_curve_ordering": ordering,
        "curve_pair_nonintersection": curve_pair_nonintersection,
        "cross_t_status": cross_t_status,
        "two_dimensional_graph_sheet_count":
            leaf["two_dimensional_graph_sheet_count"],
        "one_dimensional_clipping_curve_segment_count":
            leaf["one_dimensional_clipping_curve_segment_count"],
        "zero_dimensional_boundary_endpoint_incidence_count":
            leaf["zero_dimensional_boundary_endpoint_incidence_count"],
        "side_specific_signature_candidate_region_count":
            leaf["side_specific_signature_candidate_region_count"],
        "local_geometric_residual": False,
        "global_exact_key_disposition_credit": 0,
    }


def check_inputs() -> dict[str, Any]:
    r189 = r191.r189
    require(
        Path(r191.__file__).resolve() == (HERE / ROUND191_SOURCE).resolve(),
        "Round191 module identity",
    )
    r189.pinned_sha256(HERE / ROUND191_SOURCE, ROUND191_SOURCE_SHA256)
    r189.pinned_sha256(HERE / ROUND191_REPORT, ROUND191_REPORT_SHA256)
    r189.pinned_sha256(HERE / ROUND188_SOURCE, ROUND188_SOURCE_SHA256)
    r189.pinned_sha256(HERE / ROUND188_REPORT, ROUND188_REPORT_SHA256)
    r189.pinned_sha256(HERE / ROUND186_SOURCE, ROUND186_SOURCE_SHA256)
    r189.pinned_sha256(HERE / ROUND186_REPORT, ROUND186_REPORT_SHA256)
    upstream = r191.check_inputs()
    require(
        upstream["Round188_probe_source_sha256"] == ROUND188_SOURCE_SHA256
        and upstream["Round186_probe_source_sha256"] == ROUND186_SOURCE_SHA256,
        "Round186/188 transitive source pins",
    )
    return {
        **upstream,
        "Round186_probe_report_sha256": ROUND186_REPORT_SHA256,
        "Round188_probe_report_sha256": ROUND188_REPORT_SHA256,
        "Round191_probe_source_sha256": ROUND191_SOURCE_SHA256,
        "Round191_probe_report_sha256": ROUND191_REPORT_SHA256,
        "probe_only_import_before_pin_boundary": True,
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Read-only Round195 outgoing-W final-face assembly and U|U "
            "cross-t ordering probe; zero promotion."
        )
    )
    parser.parse_args()
    ctx.prec = 256

    pins = check_inputs()
    outgoing, collar_by_occurrence, _source = r191.r189.load_scope()
    require(len(outgoing) == EXPECTED_OUTGOING_LEAVES, "outgoing leaf census")
    require(
        len({
            collar_by_occurrence[row["occurrence_row_id"]]["origin_row_id"]
            for row in outgoing
        })
        == EXPECTED_OUTGOING_ORIGINS,
        "outgoing origin census",
    )
    require(
        len({row["retained_child_row_id"] for row in outgoing})
        == EXPECTED_RETAINED_CHILDREN,
        "outgoing retained-child census",
    )
    require(
        sum(
            (Q(row["coordinate_volume"]) for row in outgoing),
            Q(0),
        )
        == EXPECTED_OUTGOING_VOLUME,
        "outgoing exact volume",
    )

    r186 = r191.r189.r188.r186
    final_face_rows: list[dict[str, Any]] = []
    final_face_by_key: dict[tuple[str, str], dict[str, Any]] = {}
    leaf_rows: list[dict[str, Any]] = []
    u2_rows: list[dict[str, Any]] = []
    method_counts: Counter[str] = Counter()
    baseline_counts: Counter[str] = Counter()
    face_zero_set_counts: Counter[str] = Counter()
    face_active_factor_counts: Counter[str] = Counter()
    face_graph_axis_counts: Counter[str] = Counter()
    face_side_counts: Counter[str] = Counter()
    raw_face_count = 0
    raw_face_area = Q(0)
    raw_face_incident_volume = Q(0)
    single_u_count = 0
    u2_count = 0
    endpoint_face_count = 0
    endpoint_origins: set[str] = set()

    for index, row in enumerate(outgoing, 1):
        collar = collar_by_occurrence[row["occurrence_row_id"]]
        require(
            collar["kind"] == "OUTGOING"
            and collar["target_obstacle"] == "W",
            "outgoing-W collar identity",
        )
        box = r186.r179.r174.atlas.AtlasBox(
            *(Q(value) for value in row["box"]),
            0,
            row["row_id"],
        )
        raw_statuses = {
            "LOWER": row["lower_t_face_status"],
            "UPPER": row["upper_t_face_status"],
        }
        unresolved_sides = [
            side for side, value in raw_statuses.items() if value == "U"
        ]
        require(
            len(unresolved_sides) in {1, 2},
            f"outgoing unresolved side count:{row['row_id']}",
        )
        if len(unresolved_sides) == 1:
            single_u_count += 1
        else:
            u2_count += 1

        face_area = Q(row["base_coordinate_area"])
        raw_face_count += len(unresolved_sides)
        raw_face_area += len(unresolved_sides) * face_area
        raw_face_incident_volume += (
            len(unresolved_sides) * Q(row["coordinate_volume"])
        )
        for side, upper in (("LOWER", False), ("UPPER", True)):
            if raw_statuses[side] != "U":
                continue
            face_row = final_unresolved_face(
                row,
                collar,
                box,
                side,
                upper,
            )
            key = (row["row_id"], side)
            require(key not in final_face_by_key, "unique final face key")
            final_face_by_key[key] = face_row
            final_face_rows.append(face_row)
            method_counts[face_row["final_method"]] += 1
            baseline_counts[face_row["baseline_Round186_class"]] += 1
            face_zero_set_counts[face_row["zero_set_kind"]] += 1
            face_active_factor_counts[
                str(face_row["active_factor"])
            ] += 1
            face_graph_axis_counts[str(face_row["graph_axis"])] += 1
            face_side_counts[side] += 1
            if face_row["final_method"].startswith("ROUND191_"):
                endpoint_face_count += 1
                endpoint_origins.add(collar["origin_row_id"])

        lower = (
            side_summary(final_face_by_key[(row["row_id"], "LOWER")])
            if raw_statuses["LOWER"] == "U"
            else decode_round182_face(raw_statuses["LOWER"])
        )
        upper = (
            side_summary(final_face_by_key[(row["row_id"], "UPPER")])
            if raw_statuses["UPPER"] == "U"
            else decode_round182_face(raw_statuses["UPPER"])
        )
        leaf = classify_leaf(row, collar, box, lower, upper)
        leaf_rows.append(leaf)
        if len(unresolved_sides) == 2:
            u2_rows.append(audit_u2_leaf(
                leaf,
                row,
                collar,
                box,
                final_face_by_key[(row["row_id"], "LOWER")],
                final_face_by_key[(row["row_id"], "UPPER")],
            ))
        if index % 2000 == 0 or index == len(outgoing):
            print(
                f"outgoing-assembly {index}/{len(outgoing)}",
                file=sys.stderr,
                flush=True,
            )

    final_face_rows.sort(key=lambda row: row["face_row_id"])
    leaf_rows.sort(key=lambda row: row["leaf_row_id"])
    u2_rows.sort(key=lambda row: row["leaf_row_id"])
    require(
        raw_face_count == len(final_face_rows) == EXPECTED_UNRESOLVED_FACES,
        "final unresolved-face conservation",
    )
    require(
        single_u_count == EXPECTED_SINGLE_U_LEAVES
        and u2_count == EXPECTED_U2_LEAVES
        and single_u_count + u2_count == EXPECTED_OUTGOING_LEAVES,
        "single-U/U|U leaf conservation",
    )
    require(
        dict(sorted(method_counts.items()))
        == EXPECTED_FINAL_FACE_METHODS,
        "exact mutually exclusive final face method census",
    )
    require(
        sum(
            (Q(row["face_coordinate_area"]) for row in final_face_rows),
            Q(0),
        )
        == raw_face_area,
        "final face exact area conservation",
    )
    require(
        sum(
            (
                Q(row["incident_leaf_coordinate_volume"])
                for row in final_face_rows
            ),
            Q(0),
        )
        == raw_face_incident_volume,
        "final face-incidence exact volume conservation",
    )
    require(
        raw_face_area == EXPECTED_FINAL_FACE_AREA
        and raw_face_incident_volume
        == EXPECTED_FINAL_FACE_INCIDENT_VOLUME,
        "final face exact area/incident-volume pins",
    )
    require(
        endpoint_face_count == 288
        and len(endpoint_origins) == 8,
        "Round191 endpoint cohort reconstruction",
    )

    leaf_classes: Counter[str] = Counter()
    leaf_class_volumes: dict[str, Q] = {
        "EMPTY": Q(0),
        "FULL_2D": Q(0),
        "CLIPPED_2D_BOUNDARY_1D": Q(0),
    }
    dimension_totals: Counter[str] = Counter()
    candidate_region_signs: Counter[str] = Counter()
    for row in leaf_rows:
        classification = row["final_graph_classification"]
        leaf_classes[classification] += 1
        leaf_class_volumes[classification] += Q(row["coordinate_volume"])
        dimension_totals["2D_graph_sheets"] += (
            row["two_dimensional_graph_sheet_count"]
        )
        dimension_totals["1D_clipping_curve_segments"] += (
            row["one_dimensional_clipping_curve_segment_count"]
        )
        dimension_totals["0D_boundary_endpoint_incidences"] += (
            row["zero_dimensional_boundary_endpoint_incidence_count"]
        )
        dimension_totals["side_specific_signature_candidate_regions"] += (
            row["side_specific_signature_candidate_region_count"]
        )
        candidate_region_signs.update(row["candidate_region_signs"])
    require(
        sum(leaf_classes.values()) == EXPECTED_OUTGOING_LEAVES,
        "leaf classification census",
    )
    require(
        dict(sorted(leaf_classes.items())) == EXPECTED_LEAF_CLASSES,
        "final leaf classification pin",
    )
    require(
        leaf_class_volumes == EXPECTED_LEAF_CLASS_VOLUMES,
        "final leaf class exact-volume pins",
    )
    require(
        sum(leaf_class_volumes.values(), Q(0)) == EXPECTED_OUTGOING_VOLUME,
        "leaf class exact volume conservation",
    )
    require(
        all(not row["local_geometric_residual"] for row in leaf_rows),
        "zero outgoing leaf local geometric residual",
    )
    require(
        dict(sorted(dimension_totals.items()))
        == EXPECTED_DIMENSION_TOTALS,
        "final dimensional-ledger pins",
    )
    require(
        dict(sorted(candidate_region_signs.items()))
        == EXPECTED_CANDIDATE_REGION_SIGNS,
        "candidate signature-region sign pins",
    )
    require(
        dimension_totals["2D_graph_sheets"]
        == leaf_classes["FULL_2D"]
        + leaf_classes["CLIPPED_2D_BOUNDARY_1D"],
        "one 2D sheet per nonempty leaf",
    )
    require(
        dimension_totals["0D_boundary_endpoint_incidences"]
        == 2 * dimension_totals["1D_clipping_curve_segments"],
        "two endpoint incidences per clipping curve segment",
    )
    require(
        dimension_totals["side_specific_signature_candidate_regions"]
        == leaf_classes["EMPTY"]
        + 2 * dimension_totals["2D_graph_sheets"],
        "one empty or two sheet-side candidate regions per leaf",
    )

    origins: dict[str, dict[str, Any]] = {}
    for row in leaf_rows:
        origin_id = row["origin_row_id"]
        if origin_id not in origins:
            origins[origin_id] = {
                "origin_row_id": origin_id,
                "leaf_count": 0,
                "coordinate_volume": Q(0),
                "classification_count": Counter(),
                "two_dimensional_graph_sheet_count": 0,
                "one_dimensional_clipping_curve_segment_count": 0,
                "zero_dimensional_boundary_endpoint_incidence_count": 0,
                "side_specific_signature_candidate_region_count": 0,
                "local_geometric_residual_leaf_count": 0,
                "global_exact_key_disposition_credit": 0,
            }
        summary = origins[origin_id]
        summary["leaf_count"] += 1
        summary["coordinate_volume"] += Q(row["coordinate_volume"])
        summary["classification_count"][
            row["final_graph_classification"]
        ] += 1
        summary["two_dimensional_graph_sheet_count"] += (
            row["two_dimensional_graph_sheet_count"]
        )
        summary["one_dimensional_clipping_curve_segment_count"] += (
            row["one_dimensional_clipping_curve_segment_count"]
        )
        summary["zero_dimensional_boundary_endpoint_incidence_count"] += (
            row["zero_dimensional_boundary_endpoint_incidence_count"]
        )
        summary["side_specific_signature_candidate_region_count"] += (
            row["side_specific_signature_candidate_region_count"]
        )
        summary["local_geometric_residual_leaf_count"] += int(
            row["local_geometric_residual"]
        )
    origin_rows = []
    for origin_id in sorted(origins):
        row = origins[origin_id]
        origin_rows.append({
            **row,
            "coordinate_volume": str(row["coordinate_volume"]),
            "classification_count":
                dict(sorted(row["classification_count"].items())),
            "local_geometric_residual": (
                row["local_geometric_residual_leaf_count"] != 0
            ),
        })
    require(
        len(origin_rows) == EXPECTED_OUTGOING_ORIGINS,
        "assembled origin census",
    )
    require(
        all(not row["local_geometric_residual"] for row in origin_rows),
        "zero outgoing origin local geometric residual",
    )

    u2_classes: Counter[str] = Counter()
    u2_active_factors: Counter[str] = Counter()
    u2_derivatives: Counter[str] = Counter()
    u2_ordering: Counter[str] = Counter()
    u2_curve_counts: Counter[str] = Counter()
    u2_edge_pairs: Counter[str] = Counter()
    u2_volume = Q(0)
    u2_origins: set[str] = set()
    u2_dimensions: Counter[str] = Counter()
    for row in u2_rows:
        u2_classes[row["cross_t_status"]] += 1
        u2_active_factors[row["active_factor"]] += 1
        u2_derivatives[
            row["whole_3D_box_active_factor_dt_sign"]
            + "|"
            + row["whole_3D_box_active_factor_dp_sign"]
            + "|"
            + row["whole_3D_box_active_factor_ds_sign"]
        ] += 1
        u2_ordering[str(row["strict_curve_ordering"])] += 1
        u2_curve_counts[str(row["curve_t_face_count"])] += 1
        u2_edge_pairs[
            row["lower_boundary_edge_pair"]
            + "||"
            + row["upper_boundary_edge_pair"]
        ] += 1
        u2_volume += Q(row["coordinate_volume"])
        u2_origins.add(row["origin_row_id"])
        u2_dimensions["2D_graph_sheets"] += (
            row["two_dimensional_graph_sheet_count"]
        )
        u2_dimensions["1D_clipping_curve_segments"] += (
            row["one_dimensional_clipping_curve_segment_count"]
        )
        u2_dimensions["0D_boundary_endpoint_incidences"] += (
            row["zero_dimensional_boundary_endpoint_incidence_count"]
        )
        u2_dimensions["side_specific_signature_candidate_regions"] += (
            row["side_specific_signature_candidate_region_count"]
        )
    require(
        len(u2_rows) == EXPECTED_U2_LEAVES
        and len(u2_origins) == EXPECTED_U2_ORIGINS,
        "U|U leaf/origin census",
    )
    require(
        all(row["curve_pair_nonintersection"] for row in u2_rows),
        "all U|U curve pairs nonintersecting",
    )
    require(
        u2_classes == {
            "TWO_CURVES_STRICTLY_ORDERED_AND_DISJOINT": 76,
            "ONE_CURVE_OTHER_T_FACE_STRICTLY_ZERO_ABSENT": 12,
        },
        "U|U cross-t class census",
    )
    require(u2_volume == EXPECTED_U2_VOLUME, "U|U exact volume pin")
    require(
        dict(sorted(u2_dimensions.items())) == EXPECTED_U2_DIMENSIONS,
        "U|U dimensional-ledger pins",
    )
    require(
        u2_ordering == {
            "None": 12,
            "UPPER_CURVE_STRICTLY_GREATER_P_THAN_LOWER_CURVE": 38,
            "UPPER_CURVE_STRICTLY_LESS_P_THAN_LOWER_CURVE": 38,
        },
        "U|U strict ordering direction pins",
    )

    final_face_rows_sha256 = digest(final_face_rows)
    leaf_rows_sha256 = digest(leaf_rows)
    origin_rows_sha256 = digest(origin_rows)
    u2_rows_sha256 = digest(u2_rows)
    require(
        final_face_rows_sha256 == EXPECTED_FINAL_FACE_ROWS_SHA256,
        "final face-row digest pin",
    )
    require(
        leaf_rows_sha256 == EXPECTED_LEAF_ROWS_SHA256,
        "final leaf-row digest pin",
    )
    require(
        origin_rows_sha256 == EXPECTED_ORIGIN_ROWS_SHA256,
        "final origin-row digest pin",
    )
    require(
        u2_rows_sha256 == EXPECTED_U2_ROWS_SHA256,
        "final U|U audit-row digest pin",
    )

    probe_result = {
        "status":
            "READ_ONLY_ZERO_PROMOTION_SOURCE_G_OUTGOING_FINAL_ASSEMBLY_PROBE",
        "question":
            "Do the final Round186/188/191 face normal forms eliminate "
            "every local geometric residual in the 18,324 outgoing-W "
            "leaves, including strict cross-t ordering for all 88 U|U "
            "leaves?",
        "verdict": "VALIDATED",
        "verdict_scope":
            "source-G outgoing-W local geometric assembly only; not a "
            "global exact-key disposition or return-signature certificate",
        "input_chain": pins,
        "scope": {
            "source_obstacle": "G",
            "target_obstacle": "W",
            "outgoing_residual_leaf_count": EXPECTED_OUTGOING_LEAVES,
            "outgoing_origin_count": EXPECTED_OUTGOING_ORIGINS,
            "retained_child_count": EXPECTED_RETAINED_CHILDREN,
            "exact_coordinate_volume": str(EXPECTED_OUTGOING_VOLUME),
            "single_U_leaf_count": single_u_count,
            "U_pipe_U_leaf_count": u2_count,
            "unresolved_t_face_incidence_count": raw_face_count,
        },
        "final_face_assembly": {
            "final_face_row_count": len(final_face_rows),
            "final_face_rows_sha256": final_face_rows_sha256,
            "final_method_count": dict(sorted(method_counts.items())),
            "Round186_baseline_class_count":
                dict(sorted(baseline_counts.items())),
            "zero_set_kind_count":
                dict(sorted(face_zero_set_counts.items())),
            "active_factor_count":
                dict(sorted(face_active_factor_counts.items())),
            "graph_axis_count":
                dict(sorted(face_graph_axis_counts.items())),
            "face_side_count": dict(sorted(face_side_counts.items())),
            "exact_face_coordinate_area": str(raw_face_area),
            "exact_face_incident_leaf_volume":
                str(raw_face_incident_volume),
            "face_count_area_and_incident_volume_conserved": True,
            "Round191_endpoint_face_count": endpoint_face_count,
            "Round191_endpoint_origin_count": len(endpoint_origins),
            "all_face_normal_forms_mutually_exclusive": True,
            "all_target_normal_zeros_excluded": True,
            "local_face_residual_count": 0,
        },
        "per_leaf_dimensional_ledger": {
            "leaf_row_count": len(leaf_rows),
            "leaf_rows_sha256": leaf_rows_sha256,
            "classification_count": dict(sorted(leaf_classes.items())),
            "classification_exact_coordinate_volume": {
                key: str(value)
                for key, value in sorted(leaf_class_volumes.items())
            },
            "exact_coordinate_volume_conserved": True,
            "dimension_count":
                dict(sorted(dimension_totals.items())),
            "candidate_region_sign_count":
                dict(sorted(candidate_region_signs.items())),
            "side_specific_signature_candidate_region_count":
                dimension_totals[
                    "side_specific_signature_candidate_regions"
                ],
            "side_specific_return_signatures_materialized": False,
            "local_geometric_residual_leaf_count": 0,
        },
        "per_origin_assembly": {
            "origin_row_count": len(origin_rows),
            "origin_rows_sha256": origin_rows_sha256,
            "local_geometric_residual_origin_count": 0,
            "all_8268_outgoing_origins_locally_assembled": True,
        },
        "U_pipe_U_cross_t_audit": {
            "leaf_row_count": len(u2_rows),
            "distinct_origin_count": len(u2_origins),
            "exact_coordinate_volume": str(u2_volume),
            "audit_rows_sha256": u2_rows_sha256,
            "cross_t_status_count": dict(sorted(u2_classes.items())),
            "active_factor_count":
                dict(sorted(u2_active_factors.items())),
            "whole_box_dt_dp_ds_sign_count":
                dict(sorted(u2_derivatives.items())),
            "strict_curve_ordering_count":
                dict(sorted(u2_ordering.items())),
            "curve_t_face_count":
                dict(sorted(u2_curve_counts.items())),
            "lower_upper_boundary_edge_pair_count":
                dict(sorted(u2_edge_pairs.items())),
            "dimension_count":
                dict(sorted(u2_dimensions.items())),
            "same_active_factor_on_both_t_faces": True,
            "compatible_p_graph_atlas_on_both_t_faces": True,
            "whole_3D_box_active_factor_dt_and_dp_strict": True,
            "two_curve_leaf_count": 76,
            "two_curve_pairs_strictly_ordered_and_disjoint": 76,
            "one_curve_other_face_absent_leaf_count": 12,
            "curve_pair_intersection_count": 0,
            "local_geometric_residual_count": 0,
        },
        "uncovered_tail": {
            "wall_G_residual_leaf_count":
                EXPECTED_WALL_G_RESIDUAL_LEAVES,
            "wall_G_processed_here": False,
            "formal_face_evidence_attachment_emitted": False,
            "formal_half_open_edge_ownership_materialized": False,
            "side_specific_return_signatures_materialized": False,
            "global_exact_key_fibre_deduplication_performed": False,
            "independent_verifier_built": False,
        },
        "zero_promotion_contract": {
            "probe_only": True,
            "runtime_filesystem_writes": 0,
            "output_path_option_exists": False,
            "whole_leaf_credit_issued": 0,
            "whole_origin_credit_issued": 0,
            "official_source_G_global_disposition_count": 0,
            "official_source_G_global_disposition_denominator": 224580,
            "D02": "UNCHANGED_BLOCKED",
            "global_Gate5_fields": "UNCHANGED_10/18",
            "CM2": "UNCHANGED_NO_GO",
            "required_next":
                "formal producer with complete face/leaf/origin rows, "
                "side-specific return signatures, half-open ownership, "
                "the separate wall-G tail, global exact-key fibre "
                "deduplication, and an independent verifier",
        },
    }
    document = {
        "schema": SCHEMA,
        "probe_result": probe_result,
        "probe_result_sha256": digest(probe_result),
    }
    sys.stdout.write(
        json.dumps(
            document,
            sort_keys=True,
            indent=2,
            ensure_ascii=False,
            allow_nan=False,
        )
        + "\n"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
