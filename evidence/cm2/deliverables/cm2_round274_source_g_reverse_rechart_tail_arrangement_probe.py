#!/usr/bin/env python3
"""Fail-closed exact arrangement probe for Round273's 56 rechart tails.

This is deliberately a zero-credit probe.  It covers the rational outer image
boxes by the same deterministic depth-9 cover used in Round273, then replaces
each remaining interval-overwrap cell by a coordinate-monotone arrangement
certificate.  A later producer/verifier pair must pin and independently
reconstruct these rows before they may participate in frontier binding.
"""
from __future__ import annotations

import collections
import hashlib
import json
from pathlib import Path

import cm2_round174_source_g_unique_first_dynamic_occurrence_materialization as r174
import cm2_round179_source_g_residual_tube_arrangement as r179
import cm2_round273_source_g_reverse_rechart_probe as r273

HERE = Path(__file__).resolve().parent


def canonical(value: object) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()


def digest(value: object) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def active_dual(geometry: dict, reason: str):
    if reason == "outgoing_chart_seam":
        return geometry["outgoing_equality"]
    _kind, axis, wall = reason.split(":")
    dual = geometry["hit_x" if axis == "X" else "hit_y"]
    return dual[0] - r179.arb(int(wall)), dual[1]


def signature_payload(signature: dict, source_chart: str) -> dict:
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


def extremal_point(box, derivative_signs: list[str | None], want_maximum: bool):
    coordinates = []
    for (lower, upper), sign in zip(
        ((box.t0, box.t1), (box.p0, box.p1), (box.s0, box.s1)),
        derivative_signs,
        strict=True,
    ):
        if sign == "STRICT_POSITIVE":
            coordinates.append(upper if want_maximum else lower)
        elif sign == "STRICT_NEGATIVE":
            coordinates.append(lower if want_maximum else upper)
        else:
            coordinates.append((lower + upper) / 2)
    return r174.atlas.AtlasBox(
        coordinates[0], coordinates[0], coordinates[1], coordinates[1],
        coordinates[2], coordinates[2], box.depth, "round274-extremum",
    )


def main() -> int:
    a174 = r273.load_rows("cm2_round174_source_g_unique_first_dynamic_occurrence_materialization_rows.json")
    a179 = r273.load_rows("cm2_round179_source_g_residual_tube_arrangement_rows.json")
    parents = {row["parent_id"]: row for row in r273.unpack(a174, "parent_rows")}
    guards = [(174, row) for row in r273.unpack(a174, "chart_guard_rejection_rows")]
    guards += [(179, row) for row in r273.unpack(a179, "chart_guard_child_rows")]
    tables = r174.registry_tables(r174.load_inputs()["gate5"])

    rows = []
    tail_guards = set()
    reason_histogram = collections.Counter()
    classification_histogram = collections.Counter()
    derivative_histogram = collections.Counter()
    signature_relation_histogram = collections.Counter()
    signature_difference_histogram = collections.Counter()
    for source_round, guard in guards:
        target = parents[guard["parent_id"]]["owner_target"]
        chart, outer_box, proof = r273.rechart_box(
            guard["chart"], guard["box"], 128, guard["row_id"]
        )
        _resolved, residual = r273.refine_cover(chart, outer_box, target, tables)
        if not residual:
            continue
        tail_guards.add(guard["row_id"])
        for cell, path, reasons in residual:
            assert len(reasons) == 1
            reason = reasons[0]
            assert reason in {
                "outgoing_chart_seam",
                "wall_endpoint_or_count_transition:X:0",
                "wall_endpoint_or_count_transition:Y:0",
            }
            dual = active_dual(r179.interval_geometry(chart, target, cell), reason)
            derivative_signs = [r179.sign(value) if value is not None else None for value in dual[1]]
            assert derivative_signs[0] in {"STRICT_NEGATIVE", "STRICT_POSITIVE"}
            extrema = []
            for want_maximum in (False, True):
                point = extremal_point(cell, derivative_signs, want_maximum)
                point_dual = active_dual(r179.interval_geometry(chart, target, point), reason)
                value_sign = r179.sign(point_dual[0])
                assert value_sign in {"STRICT_NEGATIVE", "STRICT_POSITIVE"}
                signature, rejected = r174.dynamic_signature(chart, point, target, tables)
                assert signature is not None, rejected
                payload = signature_payload(signature, chart)
                extrema.append({
                    "kind": "MAXIMUM" if want_maximum else "MINIMUM",
                    "point": [str(point.t0), str(point.p0), str(point.s0)],
                    "active_factor_sign": value_sign,
                    "local_return_signature": payload,
                    "complete_10_field_return_signature_sha256": digest(payload),
                })
            signs = [item["active_factor_sign"] for item in extrema]
            classification = "REGULAR_GRAPH_CROSSING" if signs == ["STRICT_NEGATIVE", "STRICT_POSITIVE"] else "ZERO_SET_ABSENT"
            if classification == "ZERO_SET_ABSENT":
                assert signs[0] == signs[1]
                assert extrema[0]["complete_10_field_return_signature_sha256"] == extrema[1]["complete_10_field_return_signature_sha256"]
                relation = "IDENTICAL"
            else:
                assert extrema[0]["complete_10_field_return_signature_sha256"] != extrema[1]["complete_10_field_return_signature_sha256"]
                relation = "DISTINCT_ACROSS_ONLY_ACTIVE_REGULAR_GRAPH"
                left = extrema[0]["local_return_signature"]
                right = extrema[1]["local_return_signature"]
                changed_fields = tuple(sorted(key for key in left if left[key] != right[key]))
                assert changed_fields
                signature_difference_histogram[(reason, changed_fields)] += 1
            row = {
                "tail_arrangement_row_id": "round274-tail-arrangement:" + digest([guard["row_id"], path]),
                "source_round": source_round,
                "source_guard_row_id": guard["row_id"],
                "source_chart": guard["chart"],
                "adjacent_chart": chart,
                "parent_id": guard["parent_id"],
                "owner_target": target,
                "adjacent_cover_refinement_path": path,
                "adjacent_rational_cell": r174.box_payload(cell),
                "active_reason": reason,
                "strict_derivative_signs_t_p_s": derivative_signs,
                "strict_t_monotonicity": True,
                "extremal_certificates": extrema,
                "arrangement_classification": classification,
                "connected_open_side_count": 2 if classification == "REGULAR_GRAPH_CROSSING" else 1,
                "signature_relation": relation,
                "exact_coordinate_identity": proof["exact_coordinate_identity"],
                "occurrence_credit": 0,
                "component_credit": 0,
                "maximality_credit": 0,
            }
            row["row_sha256"] = digest(row)
            rows.append(row)
            reason_histogram[reason] += 1
            classification_histogram[classification] += 1
            derivative_histogram[tuple(derivative_signs)] += 1
            signature_relation_histogram[relation] += 1

    assert len(tail_guards) == 56
    assert len(rows) == 5012
    assert classification_histogram == {
        "REGULAR_GRAPH_CROSSING": 3488,
        "ZERO_SET_ABSENT": 1524,
    }
    assert signature_difference_histogram == {
        ("outgoing_chart_seam", ("outgoing_cell", "target_chart")): 2464,
        (
            "wall_endpoint_or_count_transition:X:0",
            ("official_key_id", "official_key_ordinal", "official_key_row", "ordered_integer_wall_events", "roof", "signed_wall_word"),
        ): 512,
        (
            "wall_endpoint_or_count_transition:Y:0",
            ("official_key_id", "official_key_ordinal", "official_key_row", "ordered_integer_wall_events", "roof", "signed_wall_word"),
        ): 512,
    }
    result = {
        "status": "ROUND274_REVERSE_RECHART_TAIL_ARRANGEMENT_PROBE__ZERO_CREDIT",
        "census": {
            "input_tail_guard_count": len(tail_guards),
            "arrangement_cell_count": len(rows),
            "reason_histogram": dict(sorted(reason_histogram.items())),
            "classification_histogram": dict(sorted(classification_histogram.items())),
            "connected_open_region_signature_count": 2 * classification_histogram["REGULAR_GRAPH_CROSSING"] + classification_histogram["ZERO_SET_ABSENT"],
            "extremal_evaluator_success_count": 2 * len(rows),
            "remaining_undecided_cell_count": 0,
        },
        "strict_derivative_histogram": {"|".join("NONE" if x is None else x for x in key): value for key, value in sorted(derivative_histogram.items(), key=lambda item: str(item[0]))},
        "signature_relation_histogram": dict(sorted(signature_relation_histogram.items())),
        "crossing_signature_difference_histogram": {
            reason + "::" + ",".join(fields): count
            for (reason, fields), count in sorted(signature_difference_histogram.items())
        },
        "tail_guard_ids_sha256": digest(sorted(tail_guards)),
        "rows_sha256": digest(rows),
        "row_hashes_sha256": digest([row["row_sha256"] for row in rows]),
        "strict_nonpromotion": {
            "occurrence_credit": 0,
            "component_credit": 0,
            "maximality_credit": 0,
            "Jx_Jy_same_point_glue_credit": 0,
            "CM2": "NO-GO_FOR_CLAIM",
        },
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
