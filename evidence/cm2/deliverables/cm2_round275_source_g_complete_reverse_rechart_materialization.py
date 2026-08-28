#!/usr/bin/env python3
"""Materialize the complete 880-guard reverse-rechart region universe."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import tempfile
from pathlib import Path

import cm2_round174_source_g_unique_first_dynamic_occurrence_materialization as r174
import cm2_round179_source_g_residual_tube_arrangement as r179
import cm2_round273_source_g_reverse_rechart_probe as r273
import cm2_round274_source_g_reverse_rechart_tail_arrangement_probe as r274

HERE = Path(__file__).resolve().parent
PREFIX = "cm2_round275_source_g_complete_reverse_rechart_materialization"
OUTPUT = HERE / f"{PREFIX}_certificate.json"
SCHEMA = "cm2.round275.source-g-complete-reverse-rechart-materialization.v1"


def canonical(value: object) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()


def digest(value: object) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def close(row: dict) -> dict:
    result = dict(row)
    assert "row_sha256" not in result
    result["row_sha256"] = digest(result)
    return result


def signature_payload(signature: dict, chart: str) -> dict:
    return r274.signature_payload(signature, chart)


def ledger(rows: list[dict], id_field: str) -> dict:
    return {
        "row_count": len(rows),
        "rows_sha256": digest(rows),
        "row_ids_sha256": digest([row[id_field] for row in rows]),
        "row_hashes_sha256": digest([row["row_sha256"] for row in rows]),
        "every_row_closed_by_own_SHA256": all(
            row["row_sha256"] == digest({key: value for key, value in row.items() if key != "row_sha256"})
            for row in rows
        ),
        "rows": rows,
    }


def resolved_row(source_round, guard, target, chart, cell, proof, signature, path, bits):
    local = signature_payload(signature, chart)
    return close({
        "reverse_rechart_region_row_id": "round275-strict-region:" + digest([guard["row_id"], path]),
        "source_round": source_round,
        "source_guard_row_id": guard["row_id"],
        "parent_id": guard["parent_id"],
        "owner_target": target,
        "source_chart": guard["chart"],
        "adjacent_chart": chart,
        "adjacent_cover_refinement_path": path,
        "adjacent_rational_region_box": r174.box_payload(cell),
        "dyadic_sqrt_enclosure_bits": bits,
        "exact_coordinate_identity": proof["exact_coordinate_identity"],
        "region_classification": "WHOLE_STRICT_SIGNATURE_CELL",
        "connected_open_region": True,
        "local_return_signature": local,
        "complete_10_field_return_signature_sha256": digest(local),
        "occurrence_credit": 0,
        "component_credit": 0,
        "maximality_credit": 0,
    })


def tail_regions(source_round, guard, target, chart, cell, proof, path, reasons, tables):
    assert len(reasons) == 1
    reason = reasons[0]
    dual = r274.active_dual(r179.interval_geometry(chart, target, cell), reason)
    derivative_signs = [r179.sign(value) if value is not None else None for value in dual[1]]
    assert derivative_signs[0] in {"STRICT_NEGATIVE", "STRICT_POSITIVE"}
    extrema = []
    for want_maximum in (False, True):
        point = r274.extremal_point(cell, derivative_signs, want_maximum)
        value_sign = r179.sign(r274.active_dual(r179.interval_geometry(chart, target, point), reason)[0])
        assert value_sign in {"STRICT_NEGATIVE", "STRICT_POSITIVE"}
        signature, rejected = r174.dynamic_signature(chart, point, target, tables)
        assert signature is not None, rejected
        local = signature_payload(signature, chart)
        extrema.append((value_sign, point, local))
    signs = [item[0] for item in extrema]
    crossing = signs == ["STRICT_NEGATIVE", "STRICT_POSITIVE"]
    assert crossing or signs[0] == signs[1]
    if not crossing:
        assert digest(extrema[0][2]) == digest(extrema[1][2])
    else:
        left, right = extrema[0][2], extrema[1][2]
        changed = tuple(sorted(key for key in left if left[key] != right[key]))
        expected = (
            ("outgoing_cell", "target_chart")
            if reason == "outgoing_chart_seam"
            else ("official_key_id", "official_key_ordinal", "official_key_row", "ordered_integer_wall_events", "roof", "signed_wall_word")
        )
        assert changed == expected
    selected = extrema if crossing else extrema[:1]
    rows = []
    for side_index, (value_sign, point, local) in enumerate(selected):
        rows.append(close({
            "reverse_rechart_region_row_id": "round275-arrangement-region:" + digest([guard["row_id"], path, value_sign]),
            "source_round": source_round,
            "source_guard_row_id": guard["row_id"],
            "parent_id": guard["parent_id"],
            "owner_target": target,
            "source_chart": guard["chart"],
            "adjacent_chart": chart,
            "adjacent_cover_refinement_path": path,
            "adjacent_rational_region_box": r174.box_payload(cell),
            "dyadic_sqrt_enclosure_bits": 128,
            "exact_coordinate_identity": proof["exact_coordinate_identity"],
            "active_reason": reason,
            "strict_derivative_signs_t_p_s": derivative_signs,
            "strict_t_monotonicity": True,
            "arrangement_classification": "REGULAR_GRAPH_CROSSING" if crossing else "ZERO_SET_ABSENT",
            "active_factor_side_sign": value_sign,
            "connected_open_region": True,
            "extremal_witness_point": [str(point.t0), str(point.p0), str(point.s0)],
            "local_return_signature": local,
            "complete_10_field_return_signature_sha256": digest(local),
            "occurrence_credit": 0,
            "component_credit": 0,
            "maximality_credit": 0,
        }))
    return rows, crossing


def build_result() -> dict:
    a174 = r273.load_rows("cm2_round174_source_g_unique_first_dynamic_occurrence_materialization_rows.json")
    a179 = r273.load_rows("cm2_round179_source_g_residual_tube_arrangement_rows.json")
    parents = {row["parent_id"]: row for row in r273.unpack(a174, "parent_rows")}
    guards = [(174, row) for row in r273.unpack(a174, "chart_guard_rejection_rows")]
    guards += [(179, row) for row in r273.unpack(a179, "chart_guard_child_rows")]
    assert len(guards) == 880
    tables = r174.registry_tables(r174.load_inputs()["gate5"])
    strict_rows = []
    arrangement_rows = []
    closure_rows = []
    for source_round, guard in guards:
        target = parents[guard["parent_id"]]["owner_target"]
        accepted = None
        proof = None
        chart = None
        outer_box = None
        for bits in (32, 48, 64, 80, 96, 128):
            chart, outer_box, proof = r273.rechart_box(guard["chart"], guard["box"], bits, guard["row_id"])
            signature, _reasons = r174.dynamic_signature(chart, outer_box, target, tables)
            if signature is not None:
                accepted = (bits, outer_box, signature)
                break
        guard_strict = []
        guard_arrangement = []
        crossing_cells = 0
        absence_cells = 0
        if accepted is not None:
            bits, cell, signature = accepted
            guard_strict.append(resolved_row(source_round, guard, target, chart, cell, proof, signature, [], bits))
        else:
            chart, outer_box, proof = r273.rechart_box(guard["chart"], guard["box"], 128, guard["row_id"])
            resolved, residual = r273.refine_cover(chart, outer_box, target, tables)
            for cell, path, signature in resolved:
                guard_strict.append(resolved_row(source_round, guard, target, chart, cell, proof, signature, path, 128))
            for cell, path, reasons in residual:
                regions, crossing = tail_regions(source_round, guard, target, chart, cell, proof, path, reasons, tables)
                guard_arrangement.extend(regions)
                crossing_cells += int(crossing)
                absence_cells += int(not crossing)
        strict_rows.extend(guard_strict)
        arrangement_rows.extend(guard_arrangement)
        closure_rows.append(close({
            "reverse_rechart_guard_closure_row_id": "round275-guard-closure:" + digest([guard["row_id"]]),
            "source_guard_row_id": guard["row_id"],
            "source_round": source_round,
            "parent_id": guard["parent_id"],
            "source_chart": guard["chart"],
            "adjacent_chart": chart,
            "strict_cover_region_count": len(guard_strict),
            "arrangement_region_count": len(guard_arrangement),
            "regular_graph_crossing_cell_count": crossing_cells,
            "zero_set_absence_cell_count": absence_cells,
            "fully_closed": True,
            "remaining_failclosed_cell_count": 0,
            "occurrence_credit": 0,
            "component_credit": 0,
        }))
    assert len(strict_rows) == 5288
    assert len(arrangement_rows) == 8500
    assert len(closure_rows) == 880
    assert sum(row["regular_graph_crossing_cell_count"] for row in closure_rows) == 3488
    assert sum(row["zero_set_absence_cell_count"] for row in closure_rows) == 1524
    return {
        "schema": SCHEMA,
        "status": "PASS_PRODUCER_ROUND275__ZERO_GLOBAL_CREDIT",
        "census": {
            "input_guard_count": 880,
            "strict_cover_region_count": 5288,
            "arrangement_region_count": 8500,
            "total_materialized_connected_region_count": 13788,
            "regular_graph_crossing_cell_count": 3488,
            "zero_set_absence_cell_count": 1524,
            "remaining_failclosed_guard_count": 0,
            "remaining_failclosed_cell_count": 0,
        },
        "strict_region_ledger": ledger(strict_rows, "reverse_rechart_region_row_id"),
        "arrangement_region_ledger": ledger(arrangement_rows, "reverse_rechart_region_row_id"),
        "guard_closure_ledger": ledger(closure_rows, "reverse_rechart_guard_closure_row_id"),
        "strict_nonpromotion": {
            "expanded_occurrence_credit": 0,
            "component_edge_credit": 0,
            "maximality_credit": 0,
            "fibre_credit": 0,
            "global_disposition_credit": 0,
            "Jx_Jy_same_point_glue_credit": 0,
            "CM2": "NO-GO_FOR_CLAIM",
        },
    }


def atomic_write(path: Path, payload: bytes) -> None:
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


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=OUTPUT)
    parser.add_argument("--seed", type=int, default=275071)
    args = parser.parse_args()
    assert args.seed >= 0
    result = build_result()
    document = {"result": result, "result_sha256": digest(result)}
    atomic_write(args.output.resolve(), json.dumps(document, indent=2, sort_keys=True).encode() + b"\n")
    print(json.dumps({"status": result["status"], "result_sha256": document["result_sha256"], **result["census"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
