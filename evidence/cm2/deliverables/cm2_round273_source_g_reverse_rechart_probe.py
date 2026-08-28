#!/usr/bin/env python3
"""Exact-enclosure probe for all 880 deferred Source-G chart guards.

The probe proves the adjacent-chart coordinate image is strictly inside its
true chart and asks the pinned Round174 evaluator to certify one complete
return signature on a rational outward enclosure of that algebraic image.
It is intentionally non-promoting; a formal producer/verifier pair must pin
and reproduce its eventual rows before any occurrence or component credit.
"""
from __future__ import annotations

import collections
import hashlib
import json
import math
import sys
from fractions import Fraction as Q
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import cm2_round174_source_g_unique_first_dynamic_occurrence_materialization as r174


def canonical(value: object) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()


def digest(value: object) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def load_rows(name: str) -> dict:
    doc = json.loads((HERE / name).read_bytes())
    result = doc["result"]
    assert doc["result_sha256"] == digest(result)
    return result


def unpack(data: dict, table: str) -> list[dict]:
    rows = data[table]
    columns = data["row_column_schemas"][table]
    expected = data["table_census_and_sha256"][table]
    assert len(rows) == expected["row_count"] and digest(rows) == expected["rows_sha256"]
    return [dict(zip(columns, row, strict=True)) for row in rows]


def sqrt_dyadic_bounds(value: Q, bits: int) -> tuple[Q, Q]:
    assert 0 <= value <= 1
    scale = 1 << bits
    scaled_square_numerator = value.numerator * scale * scale
    quotient = scaled_square_numerator // value.denominator
    k = math.isqrt(quotient)
    while (k + 1) * (k + 1) * value.denominator <= scaled_square_numerator:
        k += 1
    while k * k * value.denominator > scaled_square_numerator:
        k -= 1
    lower = Q(k, scale)
    exact = k * k * value.denominator == scaled_square_numerator
    upper = lower if exact else Q(k + 1, scale)
    assert lower * lower <= value <= upper * upper
    return lower, upper


def adjacent_chart(cell: str, positive_t: bool) -> tuple[str, int]:
    destination = {
        ("E", True): "N", ("E", False): "S",
        ("N", True): "E", ("N", False): "W",
        ("W", True): "N", ("W", False): "S",
        ("S", True): "E", ("S", False): "W",
    }[(cell, positive_t)]
    destination_t_sign = 1 if cell in {"E", "N"} else -1
    return destination, destination_t_sign


def rechart_box(chart: str, values: list[str], bits: int, path: str):
    t0, t1, p0, p1, s0, s1 = map(Q, values)
    assert t0 < t1 and (0 < t0 or t1 < 0)
    assert min(2 * t0 * t0, 2 * t1 * t1) > 1
    positive_t = t0 > 0
    # u=sqrt(1-t^2) is decreasing on t>0 and increasing on t<0.
    if positive_t:
        ulo = sqrt_dyadic_bounds(1 - t1 * t1, bits)[0]
        uhi = sqrt_dyadic_bounds(1 - t0 * t0, bits)[1]
    else:
        ulo = sqrt_dyadic_bounds(1 - t0 * t0, bits)[0]
        uhi = sqrt_dyadic_bounds(1 - t1 * t1, bits)[1]
    cell = chart.split(":", 1)[1]
    destination, sign = adjacent_chart(cell, positive_t)
    if sign < 0:
        ulo, uhi = -uhi, -ulo
    assert ulo < uhi and max(2 * ulo * ulo, 2 * uhi * uhi) < 1
    return (
        f"G:{destination}",
        r174.atlas.AtlasBox(ulo, uhi, p0, p1, s0, s1, 0, path),
        {
            "source_t_interval": [str(t0), str(t1)],
            "image_t_rational_outer_interval": [str(ulo), str(uhi)],
            "image_t_sign": "POSITIVE" if sign > 0 else "NEGATIVE",
            "exact_coordinate_identity": "image_t^2=1-source_t^2; p'=p; s'=s",
        },
    )


def refine_cover(chart, box, target, tables, max_depth=9):
    """Cover a rational adjacent-chart enclosure by strict signature cells."""
    pending = [(box, 0, [])]
    resolved = []
    residual = []
    while pending:
        current, depth, history = pending.pop()
        signature, reasons = r174.dynamic_signature(chart, current, target, tables)
        if signature is not None:
            resolved.append((current, history, signature))
            continue
        if depth >= max_depth:
            residual.append((current, history, reasons))
            continue
        options = []
        for axis in range(3):
            children = r174.split_box(current, axis)
            child_results = [r174.dynamic_signature(chart, child, target, tables) for child in children]
            released = sum(sig is not None for sig, _why in child_results)
            unresolved_reason_count = sum(len(why) for sig, why in child_results if sig is None)
            options.append((
                -released,
                unresolved_reason_count,
                axis != depth % 3,
                axis,
                children,
            ))
        _neg_released, _reason_count, _cycle_penalty, axis, children = min(options)
        pending.extend(
            (child, depth + 1, [*history, f"{('t','p','s')[axis]}{index}"])
            for index, child in enumerate(children)
        )
    return resolved, residual


def main() -> int:
    a174 = load_rows("cm2_round174_source_g_unique_first_dynamic_occurrence_materialization_rows.json")
    a179 = load_rows("cm2_round179_source_g_residual_tube_arrangement_rows.json")
    parents = {row["parent_id"]: row for row in unpack(a174, "parent_rows")}
    guards = []
    for row in unpack(a174, "chart_guard_rejection_rows"):
        guards.append((174, row))
    for row in unpack(a179, "chart_guard_child_rows"):
        guards.append((179, row))
    assert len(guards) == 880

    inputs = r174.load_inputs()
    tables = r174.registry_tables(inputs["gate5"])
    rows = []
    failures = []
    precision_histogram = collections.Counter()
    transition_histogram = collections.Counter()
    key_histogram = collections.Counter()
    for source_round, row in guards:
        parent = parents[row["parent_id"]]
        target = parent["owner_target"]
        accepted = None
        last_reasons = []
        for bits in (32, 48, 64, 80, 96, 128):
            image_chart, image_box, proof = rechart_box(
                row["chart"], row["box"], bits, row["row_id"]
            )
            signature, reasons = r174.dynamic_signature(image_chart, image_box, target, tables)
            if signature is not None:
                accepted = (bits, image_chart, image_box, proof, signature)
                break
            last_reasons = reasons
        cover = []
        cover_residual = []
        if accepted is None:
            image_chart, image_box, proof = rechart_box(
                row["chart"], row["box"], 128, row["row_id"]
            )
            refined, cover_residual = refine_cover(
                image_chart, image_box, target, tables
            )
            cover = [(128, image_chart, cell, proof, sig, path) for cell, path, sig in refined]
        else:
            bits, image_chart, image_box, proof, signature = accepted
            cover = [(bits, image_chart, image_box, proof, signature, [])]
        if cover_residual:
            failures.append({
                "guard_row_id": row["row_id"],
                "initial_reasons": last_reasons,
                "resolved_cover_cell_count": len(cover),
                "remaining_cover_cell_count": len(cover_residual),
                "remaining_reason_histogram": dict(collections.Counter(
                    reason for _cell, _path, reasons in cover_residual for reason in reasons
                )),
            })
        for bits, image_chart, image_box, proof, signature, refinement_path in cover:
            precision_histogram[bits] += 1
            transition_histogram[f"{row['chart']}->{image_chart}"] += 1
            key_histogram[signature["key"]["identifier"]] += 1
            record = {
            "guard_reverse_rechart_row_id": "round273-reverse-rechart:" + digest([row["row_id"]]),
            "source_round": source_round,
            "source_guard_row_id": row["row_id"],
            "source_chart": row["chart"],
            "adjacent_chart": image_chart,
            "parent_id": row["parent_id"],
            "owner_target": target,
            "source_exact_box": row["box"],
            "adjacent_rational_outer_box": r174.box_payload(image_box),
            "dyadic_sqrt_enclosure_bits": bits,
            "adjacent_cover_refinement_path": refinement_path,
            **proof,
            "adjacent_chart_strictly_inside_true_domain": True,
            "forward_reverse_state_identity": True,
            "local_return_signature": {
                "official_key_id": signature["key"]["identifier"],
                "official_key_ordinal": signature["key"]["ordinal"],
                "official_key_row": signature["key"]["row"],
                "ordered_integer_wall_events": signature["events"],
                "outgoing_cell": signature["outgoing_cell"],
                "roof": signature["roof"],
                "signed_wall_word": list(signature["pattern"]),
                "source_chart": image_chart,
                "target_chart": signature["target_chart"],
                "target_lift": signature["target"],
            },
            "occurrence_credit": 0,
            "component_credit": 0,
            }
            if refinement_path:
                record["guard_reverse_rechart_row_id"] = "round273-reverse-rechart-cell:" + digest([
                    row["row_id"], refinement_path
                ])
            record["complete_10_field_return_signature_sha256"] = digest(record["local_return_signature"])
            rows.append(record)

    output = {
        "status": "ROUND273_REVERSE_RECHART_PROBE__ZERO_CREDIT",
        "census": {
            "input_guard_count": len(guards),
            "resolved_signature_cover_cell_count": len(rows),
            "fully_resolved_guard_count": len(guards) - len(failures),
            "failclosed_guard_count": len(failures),
            "precision_histogram": dict(sorted(precision_histogram.items())),
            "transition_histogram": dict(sorted(transition_histogram.items())),
            "observed_adjacent_exact_key_count": len(key_histogram),
        },
        "failures": failures,
        "rows_sha256": digest(rows),
        "rows": rows,
        "strict_nonpromotion": {
            "occurrence_credit": 0,
            "component_credit": 0,
            "maximality_credit": 0,
            "CM2": "NO-GO_FOR_CLAIM",
        },
    }
    print(json.dumps(output, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
