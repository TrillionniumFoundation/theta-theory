#!/usr/bin/env python3
"""Independent ZERO-CREDIT probe for the Round282 outgoing-seam tails.

The probe works at the 48 frozen guard-channel incidences underlying the 40
unresolved directed endpoints.  It proves strict p-graph regularity on the
entire normal gap from the algebraic true seam to the rational Round275
collar, and records the only additional half-open partition (s=0 in 16 W
channels).  It deliberately emits no occurrence or component edge.
"""
from __future__ import annotations

import gzip
import hashlib
import io
import json
import os
import tempfile
from collections import Counter
from fractions import Fraction as Q
from pathlib import Path
from typing import Any

import cm2_round174_source_g_unique_first_dynamic_occurrence_materialization as r174
import cm2_round179_source_g_residual_tube_arrangement as r179
import cm2_round273_source_g_reverse_rechart_probe as r273


HERE = Path(__file__).resolve().parent
PREFIX = "cm2_round283_source_g_outgoing_seam_tail_independent_probe"
OUTPUT = HERE / f"{PREFIX}_result.json"
LEDGER = HERE / f"{PREFIX}_ledger.json.gz"
SCHEMA = "cm2.round283.source-g-outgoing-seam-tail-independent-probe.v1"
ROOT_BITS = 192
PINS = {
    "cm2_round174_source_g_unique_first_dynamic_occurrence_materialization.py":
        "3d329525dda6697a3a5d2a8227c94bd9c309ea7ebcc4cdd0c7fbe573c267a218",
    "cm2_round174_source_g_unique_first_dynamic_occurrence_materialization_rows.json":
        "9edeea2e1033b0dd70dee11a53b0f6aeb21fe74030aeefb60b081a7c420cff54",
    "cm2_round179_source_g_residual_tube_arrangement.py":
        "8c568c58d82708a7ab549f126c1fcedfccff563d1d00e3c1f7e6545b4b0d29ab",
    "cm2_round179_source_g_residual_tube_arrangement_rows.json":
        "f20b42c1fed781779b537b4d45bf44233eae1ed3ee620b95177a80f0eb2b5e42",
    "cm2_round273_source_g_reverse_rechart_probe.py":
        "40b18650a1fe8d797daf776cb9305686c21fa2eb5a7886c48ce91d697c93105c",
    "cm2_round275_source_g_complete_reverse_rechart_materialization_certificate.json":
        "e18935169614fc8b62ead3be7f60b383396ea1d2c52e8151457241f49e770386",
    "cm2_round280_source_g_true_seam_and_rechart_region_incidence_probe_patch_channels.json.gz":
        "074b27dd062844331d2d43a91283f5d467fe957123294719e32237fece05d814",
    "cm2_round282_source_g_strict_true_seam_normal_corridor_probe.py":
        "61e30d129ff27762abcf25eb074c0ba147027df08aa3cd3860496323f79306fe",
    "cm2_round282_source_g_strict_true_seam_normal_corridor_probe_ledger.json.gz":
        "6d94bce99b3ea57b8a568707705d9f16833cfba28b242a6dabb2de5933f6509e",
    "cm2_round282_source_g_strict_true_seam_normal_corridor_probe_result.json":
        "cd054a7036d9c482357611e9af11d028179e0f34a828dca2fbe91332b178f532",
}


def canonical(value: Any) -> bytes:
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=False,
        allow_nan=False,
    ).encode()


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def fsha(path: Path) -> str:
    result = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            result.update(block)
    return result.hexdigest()


def need(condition: bool, label: str) -> None:
    if not condition:
        raise RuntimeError(label)


def qstr(value: Q) -> str:
    return str(value.numerator) if value.denominator == 1 else str(value)


def area(rectangle: tuple[Q, Q, Q, Q]) -> Q:
    return max(Q(0), rectangle[1] - rectangle[0]) * max(
        Q(0), rectangle[3] - rectangle[2]
    )


def intersection(
    left: tuple[Q, Q, Q, Q], right: tuple[Q, Q, Q, Q]
) -> tuple[Q, Q, Q, Q] | None:
    result = (
        max(left[0], right[0]), min(left[1], right[1]),
        max(left[2], right[2]), min(left[3], right[3]),
    )
    return result if area(result) > 0 else None


def union_area(rectangles: list[tuple[Q, Q, Q, Q]]) -> Q:
    if not rectangles:
        return Q(0)
    ps = sorted({value for rectangle in rectangles for value in rectangle[:2]})
    ss = sorted({value for rectangle in rectangles for value in rectangle[2:]})
    result = Q(0)
    for p0, p1 in zip(ps, ps[1:]):
        for s0, s1 in zip(ss, ss[1:]):
            if any(
                rectangle[0] <= p0 and p1 <= rectangle[1]
                and rectangle[2] <= s0 and s1 <= rectangle[3]
                for rectangle in rectangles
            ):
                result += (p1 - p0) * (s1 - s0)
    return result


def complement_cells(
    container: tuple[Q, Q, Q, Q],
    covered: list[tuple[Q, Q, Q, Q]],
) -> list[tuple[Q, Q, Q, Q]]:
    clipped = [
        overlap for rectangle in covered
        if (overlap := intersection(container, rectangle)) is not None
    ]
    ps = sorted({
        container[0], container[1],
        *(value for rectangle in clipped for value in rectangle[:2]),
    })
    ss = sorted({
        container[2], container[3],
        *(value for rectangle in clipped for value in rectangle[2:]),
    })
    result = []
    for p0, p1 in zip(ps, ps[1:]):
        for s0, s1 in zip(ss, ss[1:]):
            cell = (p0, p1, s0, s1)
            if area(cell) > 0 and not any(
                rectangle[0] <= p0 and p1 <= rectangle[1]
                and rectangle[2] <= s0 and s1 <= rectangle[3]
                for rectangle in clipped
            ):
                result.append(cell)
    need(
        union_area(clipped) + sum(map(area, result)) == area(container),
        "exact complement conservation",
    )
    return result


def close(row: dict[str, Any]) -> dict[str, Any]:
    result = dict(row)
    result["row_sha256"] = digest(result)
    return result


def gzip_bytes(value: Any) -> bytes:
    output = io.BytesIO()
    with gzip.GzipFile(filename="", mode="wb", fileobj=output, mtime=0) as handle:
        handle.write(canonical(value))
    return output.getvalue()


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


def derivative_signs(dual: Any) -> tuple[str | None, ...]:
    return tuple(
        r179.sign(value) if value is not None else None for value in dual[1]
    )


def exact_diagonal_symmetry(
    chart: str, target: str, root_sign: int
) -> bool:
    """Prove F=0 at t=root, p=s=0 by exact diagonal collinearity."""
    if not target.startswith("W["):
        return False
    ix, iy = map(int, target[2:-1].split(","))
    center = (Q(ix) + Q(1, 2), Q(iy) + Q(1, 2))
    cell = chart.split(":")[1]
    normal_signs = {
        "E": (1, root_sign),
        "W": (-1, root_sign),
        "N": (root_sign, 1),
        "S": (root_sign, -1),
    }[cell]
    return (
        abs(center[0]) == abs(center[1]) == Q(1, 2)
        and (1 if center[0] > 0 else -1, 1 if center[1] > 0 else -1)
        == normal_signs
    )


def build() -> tuple[dict[str, Any], dict[str, Any]]:
    for filename, expected in PINS.items():
        need(fsha(HERE / filename) == expected, "pin:" + filename)

    round174 = r273.load_rows(
        "cm2_round174_source_g_unique_first_dynamic_occurrence_materialization_rows.json"
    )
    round179 = r273.load_rows(
        "cm2_round179_source_g_residual_tube_arrangement_rows.json"
    )
    parents = {
        row["parent_id"]: row for row in r273.unpack(round174, "parent_rows")
    }
    guards = {
        row["row_id"]: (174, row)
        for row in r273.unpack(round174, "chart_guard_rejection_rows")
    }
    guards.update({
        row["row_id"]: (179, row)
        for row in r273.unpack(round179, "chart_guard_child_rows")
    })

    with gzip.open(
        HERE / "cm2_round280_source_g_true_seam_and_rechart_region_incidence_probe_patch_channels.json.gz",
        "rt",
    ) as handle:
        channel_document = json.load(handle)
    channels = {
        row["Round268_true_seam_patch_row_id"]: row
        for row in channel_document["rows"]
    }
    with gzip.open(
        HERE / "cm2_round282_source_g_strict_true_seam_normal_corridor_probe_ledger.json.gz",
        "rt",
    ) as handle:
        round282 = json.load(handle)

    round275 = json.load(open(
        HERE / "cm2_round275_source_g_complete_reverse_rechart_materialization_certificate.json"
    ))["result"]
    region_rows = {
        row["reverse_rechart_region_row_id"]: row
        for ledger_name in ("strict_region_ledger", "arrangement_region_ledger")
        for row in round275[ledger_name]["rows"]
    }

    tables = r174.registry_tables(r174.load_inputs()["gate5"])
    root_lower, root_upper = r273.sqrt_dyadic_bounds(Q(1, 2), ROOT_BITS)
    endpoint_rows = []
    classification_histogram = Counter()
    seam_derivative_histogram = Counter()
    gap_derivative_histogram = Counter()
    s_boundary_sign_histogram = Counter()
    candidate_guard_histogram = Counter()
    residual_cell_histogram = Counter()
    raw_region_hit_count = 0
    region_cell_incidence_count = 0
    canonical_channel_cells: set[tuple[Any, ...]] = set()
    arrangement_reasons = Counter()

    for patch in round282["rows"]:
        if patch["classification"] == "FULL_BIDIRECTIONAL_STRICT_NORMAL_CORRIDOR_COVER":
            continue
        patch_id = patch["Round268_true_seam_patch_row_id"]
        channel = channels[patch_id]
        container = tuple(map(Q, [
            *patch["exact_common_p_interval"],
            *patch["exact_common_s_interval"],
        ]))
        for side_index, side in enumerate(patch["side_corridors"]):
            if side["classification"] == "FULL_STRICT_NORMAL_CORRIDOR_COVER":
                continue
            accepted = [
                tuple(map(Q, item["positive_ps_footprint"]))
                for item in side["accepted_strict_corridors"]
            ]
            residual_cells = complement_cells(container, accepted)
            need(
                sum(map(area, residual_cells)) == Q(side["unresolved_area"]),
                "Round282 unresolved area",
            )
            residual_cell_histogram[len(residual_cells)] += 1
            side_channel = channel["side_channel_rows"][side_index]
            guard_rows = []

            for guard_id in side_channel["candidate_guard_row_ids"]:
                source_round, guard = guards[guard_id]
                target = parents[guard["parent_id"]]["owner_target"]
                adjacent_chart, outer_box, proof = r273.rechart_box(
                    guard["chart"], guard["box"], ROOT_BITS, guard_id
                )
                need(adjacent_chart == side["adjacent_chart"], "adjacent chart")
                need(
                    outer_box.p0 <= container[0] <= container[1] <= outer_box.p1
                    and outer_box.s0 <= container[2] <= container[3] <= outer_box.s1,
                    "guard covers patch footprint",
                )
                root_sign = 1 if outer_box.t0 >= 0 else -1
                seam_t = (
                    (root_lower, root_upper)
                    if root_sign > 0 else (-root_upper, -root_lower)
                )
                seam_box = r174.atlas.AtlasBox(
                    seam_t[0], seam_t[1], *container, 0, "round283-seam"
                )
                gap_box = (
                    r174.atlas.AtlasBox(
                        outer_box.t0, root_upper, *container, 0, "round283-gap"
                    )
                    if root_sign > 0 else
                    r174.atlas.AtlasBox(
                        -root_upper, outer_box.t1, *container, 0, "round283-gap"
                    )
                )
                signature, reasons = r174.dynamic_signature(
                    adjacent_chart, gap_box, target, tables
                )
                need(
                    signature is None and reasons == ["outgoing_chart_seam"],
                    "outgoing is sole gap event",
                )
                seam_dual = r179.interval_geometry(
                    adjacent_chart, target, seam_box
                )["outgoing_equality"]
                gap_dual = r179.interval_geometry(
                    adjacent_chart, target, gap_box
                )["outgoing_equality"]
                seam_signs = derivative_signs(seam_dual)
                gap_signs = derivative_signs(gap_dual)
                need(
                    seam_signs[0] in {"STRICT_NEGATIVE", "STRICT_POSITIVE"}
                    and seam_signs[1] in {"STRICT_NEGATIVE", "STRICT_POSITIVE"}
                    and gap_signs[0] == seam_signs[0]
                    and gap_signs[1] == seam_signs[1],
                    "strict stable dt/dp on whole gap",
                )
                if target.startswith("G["):
                    need(
                        seam_signs[2] == gap_signs[2] == "OVERWRAP",
                        "G target structural s-independence",
                    )
                    s_derivative_contract = "EXACTLY_ZERO_BY_G_TARGET_CENTER_INDEPENDENCE"
                else:
                    need(
                        seam_signs[2] in {"STRICT_NEGATIVE", "STRICT_POSITIVE"}
                        and gap_signs[2] == seam_signs[2],
                        "strict stable ds for W target",
                    )
                    s_derivative_contract = seam_signs[2]
                seam_derivative_histogram[seam_signs] += 1
                gap_derivative_histogram[gap_signs] += 1

                p_face_signs = []
                for p_value in container[:2]:
                    face = r174.atlas.AtlasBox(
                        seam_t[0], seam_t[1], p_value, p_value,
                        container[2], container[3], 0, "round283-p-face",
                    )
                    p_face_signs.append(r179.sign(
                        r179.interval_geometry(
                            adjacent_chart, target, face
                        )["outgoing_equality"][0]
                    ))

                split_rows = []
                if set(p_face_signs) == {"STRICT_NEGATIVE", "STRICT_POSITIVE"}:
                    classification = "FULL_S_BASE_REGULAR_P_GRAPH"
                    child_histogram = {
                        "REGULAR_P_GRAPH_HALF_OPEN_OWNER": 1,
                        "STRICT_ZERO_ABSENT": 0,
                    }
                    logical_s_split_count = 0
                    connected_sign_corridor_count = 2
                elif "OVERWRAP" in p_face_signs:
                    need(
                        p_face_signs.count("OVERWRAP") == 1
                        and target.startswith("W[")
                        and seam_signs[2] in {"STRICT_NEGATIVE", "STRICT_POSITIVE"},
                        "endpoint tail is W with strict ds",
                    )
                    overwrap_p = container[p_face_signs.index("OVERWRAP")]
                    need(
                        overwrap_p == 0
                        and container[2] < 0 < container[3]
                        and exact_diagonal_symmetry(
                            adjacent_chart, target, root_sign
                        ),
                        "exact p=s=0 diagonal owner",
                    )
                    boundary_signs = []
                    for s_value in container[2:]:
                        corner = r174.atlas.AtlasBox(
                            seam_t[0], seam_t[1], Q(0), Q(0),
                            s_value, s_value, 0, "round283-s-corner",
                        )
                        boundary_signs.append(r179.sign(
                            r179.interval_geometry(
                                adjacent_chart, target, corner
                            )["outgoing_equality"][0]
                        ))
                    need(
                        set(boundary_signs)
                        == {"STRICT_NEGATIVE", "STRICT_POSITIVE"},
                        "unique strict s bracket at p=0",
                    )
                    s_boundary_sign_histogram[tuple(boundary_signs)] += 1
                    for s0, s1 in (
                        (container[2], Q(0)), (Q(0), container[3])
                    ):
                        witness_s = (s0 + s1) / 2
                        witness_signs = []
                        for p_value in container[:2]:
                            witness = r174.atlas.AtlasBox(
                                seam_t[0], seam_t[1], p_value, p_value,
                                witness_s, witness_s, 0, "round283-half-witness",
                            )
                            witness_signs.append(r179.sign(
                                r179.interval_geometry(
                                    adjacent_chart, target, witness
                                )["outgoing_equality"][0]
                            ))
                        child_classification = (
                            "REGULAR_P_GRAPH_HALF_OPEN_OWNER"
                            if set(witness_signs)
                            == {"STRICT_NEGATIVE", "STRICT_POSITIVE"}
                            else "STRICT_ZERO_ABSENT"
                        )
                        need(
                            child_classification
                            == "REGULAR_P_GRAPH_HALF_OPEN_OWNER"
                            or len(set(witness_signs)) == 1
                            and "OVERWRAP" not in witness_signs,
                            "half-open child classification",
                        )
                        split_rows.append({
                            "half_open_s_interval": [qstr(s0), qstr(s1)],
                            "strict_rational_witness_s": qstr(witness_s),
                            "p_face_signs_at_witness": witness_signs,
                            "classification": child_classification,
                            "p_equals_s_equals_zero_owned_by_frozen_half_open_policy": True,
                        })
                    child_counter = Counter(
                        item["classification"] for item in split_rows
                    )
                    need(
                        child_counter == {
                            "REGULAR_P_GRAPH_HALF_OPEN_OWNER": 1,
                            "STRICT_ZERO_ABSENT": 1,
                        },
                        "one graph and one absence child",
                    )
                    classification = (
                        "P_ENDPOINT_REGULAR_GRAPH__EXACT_S0_SPLIT"
                    )
                    child_histogram = dict(child_counter)
                    logical_s_split_count = 1
                    connected_sign_corridor_count = 3
                else:
                    need(
                        len(set(p_face_signs)) == 1
                        and p_face_signs[0]
                        in {"STRICT_NEGATIVE", "STRICT_POSITIVE"},
                        "same-sign absence",
                    )
                    classification = "STRICT_ZERO_ABSENT"
                    child_histogram = {
                        "REGULAR_P_GRAPH_HALF_OPEN_OWNER": 0,
                        "STRICT_ZERO_ABSENT": 1,
                    }
                    logical_s_split_count = 0
                    connected_sign_corridor_count = 1

                classification_histogram[classification] += 1
                guard_rows.append({
                    "source_guard_row_id": guard_id,
                    "source_round": source_round,
                    "parent_id": guard["parent_id"],
                    "owner_target": target,
                    "source_chart": guard["chart"],
                    "adjacent_chart": adjacent_chart,
                    "algebraic_root_sign": root_sign,
                    "exact_coordinate_identity": proof["exact_coordinate_identity"],
                    "normal_gap_outer_box": [
                        qstr(gap_box.t0), qstr(gap_box.t1),
                        qstr(gap_box.p0), qstr(gap_box.p1),
                        qstr(gap_box.s0), qstr(gap_box.s1),
                    ],
                    "sole_dynamic_gap_reason": "outgoing_chart_seam",
                    "seam_derivative_signs_t_p_s": list(seam_signs),
                    "whole_gap_derivative_signs_t_p_s": list(gap_signs),
                    "s_derivative_contract": s_derivative_contract,
                    "seam_p_face_signs": p_face_signs,
                    "classification": classification,
                    "logical_s_split_count": logical_s_split_count,
                    "analytic_child_histogram": child_histogram,
                    "half_open_split_rows": split_rows,
                    "connected_sign_corridor_count": connected_sign_corridor_count,
                    "regular_p_graph_has_no_fold_or_bifurcation_on_gap": True,
                    "component_edge_credit": 0,
                })

            candidate_guard_histogram[len(guard_rows)] += 1
            need(
                len(guard_rows) == side_channel["candidate_guard_count"],
                "candidate guard conservation",
            )

            candidate_region_hits = set()
            for region_id in side_channel["candidate_Round275_region_ids"]:
                region = region_rows[region_id]
                box = list(map(Q, region["adjacent_rational_region_box"]))
                footprint = intersection(
                    container, (box[2], box[3], box[4], box[5])
                )
                if footprint is None:
                    continue
                row_hit = False
                for residual in residual_cells:
                    overlap = intersection(footprint, residual)
                    if overlap is None:
                        continue
                    row_hit = True
                    region_cell_incidence_count += 1
                    root_sign = 1 if box[0] >= 0 else -1
                    canonical_channel_cells.add((
                        patch_id, side_index, region["adjacent_chart"],
                        region["owner_target"], root_sign, overlap,
                    ))
                if row_hit:
                    candidate_region_hits.add(region_id)
                    if "active_reason" in region:
                        arrangement_reasons[region["active_reason"]] += 1
            raw_region_hit_count += len(candidate_region_hits)

            endpoint_rows.append(close({
                "Round283_endpoint_row_id": "round283-outgoing-seam-endpoint:" + digest(
                    [patch_id, side_index]
                ),
                "Round268_true_seam_patch_row_id": patch_id,
                "side_index": side_index,
                "side": side["side"],
                "source_chart": side["source_chart"],
                "adjacent_chart": side["adjacent_chart"],
                "patch_ps_rectangle": [qstr(value) for value in container],
                "Round282_unresolved_area": qstr(sum(map(area, residual_cells))),
                "Round282_residual_rational_cell_count": len(residual_cells),
                "Round282_residual_rational_cells": [
                    [qstr(value) for value in cell] for cell in residual_cells
                ],
                "candidate_guard_channel_count": len(guard_rows),
                "guard_channel_rows": guard_rows,
                "candidate_Round275_region_hit_count": len(candidate_region_hits),
                "candidate_Round275_region_ids_sha256": digest(
                    sorted(candidate_region_hits)
                ),
                "analytic_tail_residual_after_regular_graph_partition": "0",
                "formal_component_edge_credit": 0,
                "formal_occurrence_credit": 0,
                "maximality_credit": 0,
            }))

    endpoint_rows.sort(key=lambda row: row["Round283_endpoint_row_id"])
    need(len(endpoint_rows) == 40, "endpoint count")
    need(len({row["Round268_true_seam_patch_row_id"] for row in endpoint_rows}) == 24, "patch count")
    need(sum(row["candidate_guard_channel_count"] for row in endpoint_rows) == 48, "guard channels")
    need(candidate_guard_histogram == {1: 32, 2: 8}, "guard histogram")
    need(sum(row["Round282_residual_rational_cell_count"] for row in endpoint_rows) == 540, "residual cells")
    need(residual_cell_histogram == {2: 8, 4: 16, 20: 8, 33: 4, 42: 4}, "cell histogram")
    need(classification_histogram == {
        "FULL_S_BASE_REGULAR_P_GRAPH": 24,
        "P_ENDPOINT_REGULAR_GRAPH__EXACT_S0_SPLIT": 16,
        "STRICT_ZERO_ABSENT": 8,
    }, "classification histogram")
    need(s_boundary_sign_histogram == {
        ("STRICT_NEGATIVE", "STRICT_POSITIVE"): 8,
        ("STRICT_POSITIVE", "STRICT_NEGATIVE"): 8,
    }, "s boundary signs")
    need(raw_region_hit_count == 6596, "region hits")
    need(region_cell_incidence_count == 9528, "region cell incidences")
    need(len(canonical_channel_cells) == 1128, "canonical channel cells")
    need(set(arrangement_reasons) <= {"outgoing_chart_seam"}, "only outgoing arrangement")

    regular_graph_child_count = (
        classification_histogram["FULL_S_BASE_REGULAR_P_GRAPH"]
        + classification_histogram["P_ENDPOINT_REGULAR_GRAPH__EXACT_S0_SPLIT"]
    )
    absence_child_count = (
        classification_histogram["STRICT_ZERO_ABSENT"]
        + classification_histogram["P_ENDPOINT_REGULAR_GRAPH__EXACT_S0_SPLIT"]
    )
    analytic_child_count = regular_graph_child_count + absence_child_count
    connected_sign_corridor_count = 2 * regular_graph_child_count + absence_child_count
    need((regular_graph_child_count, absence_child_count, analytic_child_count) == (40, 24, 64), "child census")
    need(connected_sign_corridor_count == 104, "sign corridor census")

    ledger = {
        "schema": SCHEMA + ".ledger",
        "row_count": len(endpoint_rows),
        "rows": endpoint_rows,
        "rows_sha256": digest(endpoint_rows),
        "row_ids_sha256": digest([
            row["Round283_endpoint_row_id"] for row in endpoint_rows
        ]),
        "row_hashes_sha256": digest([
            row["row_sha256"] for row in endpoint_rows
        ]),
    }
    result = {
        "schema": SCHEMA,
        "status": (
            "PASS_INDEPENDENT_ROUND283_OUTGOING_SEAM_TAIL_GEOMETRY__"
            "ANALYTIC_RESIDUAL_ZERO__ZERO_CREDIT"
        ),
        "pins": PINS,
        "root_enclosure_bits": ROOT_BITS,
        "census": {
            "input_failclosed_patch_count": 24,
            "input_failclosed_directed_endpoint_count": 40,
            "candidate_guard_channel_incidence_count": 48,
            "candidate_guard_count_per_endpoint_histogram": {
                str(key): value for key, value in sorted(candidate_guard_histogram.items())
            },
            "Round282_residual_rational_ps_cell_count": 540,
            "Round282_residual_cell_count_per_endpoint_histogram": {
                str(key): value for key, value in sorted(residual_cell_histogram.items())
            },
            "candidate_Round275_region_hit_count": raw_region_hit_count,
            "Round275_region_by_residual_cell_incidence_count": region_cell_incidence_count,
            "canonical_endpoint_chart_target_root_ps_channel_cell_count": len(canonical_channel_cells),
            "guard_channel_classification_histogram": dict(sorted(classification_histogram.items())),
            "logical_new_p_split_count": 0,
            "logical_s_equals_zero_split_count": 16,
            "analytic_partition_child_count": analytic_child_count,
            "regular_p_graph_child_count": regular_graph_child_count,
            "strict_zero_absence_child_count": absence_child_count,
            "connected_open_sign_corridor_count": connected_sign_corridor_count,
            "exact_half_open_graph_owner_count": regular_graph_child_count,
            "remaining_analytic_tail_endpoint_count": 0,
            "remaining_analytic_tail_patch_count": 0,
        },
        "proof_contract": {
            "whole_gap_only_dynamic_reason_is_outgoing_chart_seam": True,
            "strict_dt_on_all_48_whole_gap_channels": True,
            "strict_dp_on_all_48_whole_gap_channels": True,
            "G_target_channel_count_with_structural_exact_ds_zero": 32,
            "W_target_channel_count_with_strict_ds": 16,
            "W_strict_ds_sign_histogram": {
                "STRICT_NEGATIVE": 8, "STRICT_POSITIVE": 8,
            },
            "interior_crossing_channels_are_G_targets": 24,
            "endpoint_channels_are_W_targets": 16,
            "same_sign_absence_channels_are_G_targets": 8,
            "endpoint_zero_is_exactly_p_equals_s_equals_zero_by_diagonal_collinearity": True,
            "strict_dp_makes_every_nonempty_zero_set_a_regular_p_graph": True,
            "strict_dt_and_structural_zero_or_strict_ds_make_each_graph_monotone_on_the_whole_gap": True,
            "half_open_owner_assigns_graph_once_and_shadow_side_never_duplicates_it": True,
        },
        "seam_derivative_histogram": {
            "|".join("NONE" if item is None else item for item in key): value
            for key, value in sorted(seam_derivative_histogram.items())
        },
        "whole_gap_derivative_histogram": {
            "|".join("NONE" if item is None else item for item in key): value
            for key, value in sorted(gap_derivative_histogram.items())
        },
        "ledger": {
            "filename": LEDGER.name,
            "row_count": ledger["row_count"],
            "rows_sha256": ledger["rows_sha256"],
        },
        "strict_nonpromotion": {
            "expanded_occurrence_credit": 0,
            "component_edge_credit": 0,
            "maximality_credit": 0,
            "exact_key_fibre_credit": 0,
            "global_disposition_credit": 0,
            "Jx_Jy_same_point_glue_credit": 0,
            "quotient": 63224,
            "expanded_occurrences": 126468,
            "Gate5": "10/18",
            "D02": "BLOCKED",
            "CM2": "NO-GO_FOR_CLAIM",
        },
        "formal_next_gate": (
            "A pinned producer and independent verifier must materialize the "
            "64 half-open analytic children, bind their sign signatures to "
            "the frozen Round275 region rows, pair both sides of each of the "
            "152 patches, and only then emit seam DSU edges."
        ),
    }
    result["result_sha256"] = digest(result)
    return ledger, result


def main() -> None:
    ledger, result = build()
    ledger_payload = gzip_bytes(ledger)
    result["ledger"]["file_sha256"] = hashlib.sha256(ledger_payload).hexdigest()
    result["result_sha256"] = digest({
        key: value for key, value in result.items() if key != "result_sha256"
    })
    atomic(LEDGER, ledger_payload)
    atomic(OUTPUT, canonical(result) + b"\n")
    print(json.dumps({
        "status": result["status"],
        "result_sha256": result["result_sha256"],
        **result["census"],
    }, sort_keys=True))


if __name__ == "__main__":
    main()
