#!/usr/bin/env python3
"""Independent row-wise verifier for the Round275 reverse-rechart certificate."""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
from pathlib import Path

import cm2_round174_source_g_unique_first_dynamic_occurrence_materialization as r174
import cm2_round179_source_g_residual_tube_arrangement as r179
import cm2_round273_source_g_reverse_rechart_probe as r273
import cm2_round274_source_g_reverse_rechart_tail_arrangement_probe as r274

HERE = Path(__file__).resolve().parent
CERTIFICATE = HERE / "cm2_round275_source_g_complete_reverse_rechart_materialization_certificate.json"


class VerificationError(RuntimeError):
    pass


def need(condition: bool, label: str) -> None:
    if not condition:
        raise VerificationError(label)


def canonical(value: object) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()


def digest(value: object) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def validate_ledger(ledger: dict, id_field: str) -> list[dict]:
    rows = ledger["rows"]
    need(ledger["row_count"] == len(rows), "ledger count")
    need(ledger["rows_sha256"] == digest(rows), "ledger rows digest")
    need(ledger["row_ids_sha256"] == digest([row[id_field] for row in rows]), "ledger ids digest")
    need(ledger["row_hashes_sha256"] == digest([row["row_sha256"] for row in rows]), "ledger hashes digest")
    need(len({row[id_field] for row in rows}) == len(rows), "unique row ids")
    for row in rows:
        body = {key: value for key, value in row.items() if key != "row_sha256"}
        need(row["row_sha256"] == digest(body), "row self hash")
    return rows


def structure(result: dict) -> tuple[list[dict], list[dict], list[dict]]:
    need(result["schema"] == "cm2.round275.source-g-complete-reverse-rechart-materialization.v1", "schema")
    strict = validate_ledger(result["strict_region_ledger"], "reverse_rechart_region_row_id")
    arranged = validate_ledger(result["arrangement_region_ledger"], "reverse_rechart_region_row_id")
    closures = validate_ledger(result["guard_closure_ledger"], "reverse_rechart_guard_closure_row_id")
    census = result["census"]
    need(census == {
        "input_guard_count": 880,
        "strict_cover_region_count": 5288,
        "arrangement_region_count": 8500,
        "total_materialized_connected_region_count": 13788,
        "regular_graph_crossing_cell_count": 3488,
        "zero_set_absence_cell_count": 1524,
        "remaining_failclosed_guard_count": 0,
        "remaining_failclosed_cell_count": 0,
    }, "census")
    need(len(strict) == 5288 and len(arranged) == 8500 and len(closures) == 880, "ledger census")
    nonpromotion = result["strict_nonpromotion"]
    need(all(nonpromotion[key] == 0 for key in (
        "expanded_occurrence_credit", "component_edge_credit", "maximality_credit",
        "fibre_credit", "global_disposition_credit", "Jx_Jy_same_point_glue_credit",
    )), "nonpromotion")
    need(nonpromotion["CM2"] == "NO-GO_FOR_CLAIM", "CM2 no-go")
    return strict, arranged, closures


def local_signature(signature: dict, chart: str) -> dict:
    return r274.signature_payload(signature, chart)


def full_recompute(result: dict) -> None:
    strict, arranged, closures = structure(result)
    strict_by_id = {row["reverse_rechart_region_row_id"]: row for row in strict}
    arranged_by_id = {row["reverse_rechart_region_row_id"]: row for row in arranged}
    closure_by_guard = {row["source_guard_row_id"]: row for row in closures}
    seen_strict = set()
    seen_arranged = set()

    a174 = r273.load_rows("cm2_round174_source_g_unique_first_dynamic_occurrence_materialization_rows.json")
    a179 = r273.load_rows("cm2_round179_source_g_residual_tube_arrangement_rows.json")
    parents = {row["parent_id"]: row for row in r273.unpack(a174, "parent_rows")}
    guards = [(174, row) for row in r273.unpack(a174, "chart_guard_rejection_rows")]
    guards += [(179, row) for row in r273.unpack(a179, "chart_guard_child_rows")]
    tables = r174.registry_tables(r174.load_inputs()["gate5"])
    need(len(guards) == 880, "input guard census")

    for source_round, guard in guards:
        target = parents[guard["parent_id"]]["owner_target"]
        accepted = None
        chart = None
        outer = None
        proof = None
        for bits in (32, 48, 64, 80, 96, 128):
            chart, outer, proof = r273.rechart_box(guard["chart"], guard["box"], bits, guard["row_id"])
            signature, _why = r174.dynamic_signature(chart, outer, target, tables)
            if signature is not None:
                accepted = (bits, outer, signature)
                break
        expected_strict = 0
        expected_arranged = 0
        crossing_cells = 0
        absence_cells = 0
        if accepted is not None:
            bits, cell, signature = accepted
            candidates = [(cell, [], signature, bits)]
            residual = []
        else:
            chart, outer, proof = r273.rechart_box(guard["chart"], guard["box"], 128, guard["row_id"])
            resolved, residual = r273.refine_cover(chart, outer, target, tables)
            candidates = [(cell, path, signature, 128) for cell, path, signature in resolved]
        for cell, path, signature, bits in candidates:
            row_id = "round275-strict-region:" + digest([guard["row_id"], path])
            need(row_id in strict_by_id, "missing strict region")
            row = strict_by_id[row_id]
            expected = local_signature(signature, chart)
            need(row["source_round"] == source_round and row["parent_id"] == guard["parent_id"], "strict provenance")
            need(row["adjacent_rational_region_box"] == r174.box_payload(cell), "strict box")
            need(row["dyadic_sqrt_enclosure_bits"] == bits, "strict precision")
            need(row["local_return_signature"] == expected and row["complete_10_field_return_signature_sha256"] == digest(expected), "strict signature")
            need(row["connected_open_region"] and row["occurrence_credit"] == row["component_credit"] == row["maximality_credit"] == 0, "strict credit")
            seen_strict.add(row_id)
            expected_strict += 1
        for cell, path, reasons in residual:
            need(len(reasons) == 1, "one active tail reason")
            reason = reasons[0]
            dual = r274.active_dual(r179.interval_geometry(chart, target, cell), reason)
            derivatives = [r179.sign(value) if value is not None else None for value in dual[1]]
            need(derivatives[0] in {"STRICT_NEGATIVE", "STRICT_POSITIVE"}, "strict t derivative")
            extrema = []
            for want_maximum in (False, True):
                point = r274.extremal_point(cell, derivatives, want_maximum)
                sign = r179.sign(r274.active_dual(r179.interval_geometry(chart, target, point), reason)[0])
                signature, rejected = r174.dynamic_signature(chart, point, target, tables)
                need(signature is not None, "extremal evaluator:" + str(rejected))
                extrema.append((sign, point, local_signature(signature, chart)))
            crossing = [item[0] for item in extrema] == ["STRICT_NEGATIVE", "STRICT_POSITIVE"]
            need(crossing or extrema[0][0] == extrema[1][0], "extremal classification")
            selected = extrema if crossing else extrema[:1]
            crossing_cells += int(crossing)
            absence_cells += int(not crossing)
            if crossing:
                changed = tuple(sorted(key for key in extrema[0][2] if extrema[0][2][key] != extrema[1][2][key]))
                expected_changed = ("outgoing_cell", "target_chart") if reason == "outgoing_chart_seam" else ("official_key_id", "official_key_ordinal", "official_key_row", "ordered_integer_wall_events", "roof", "signed_wall_word")
                need(changed == expected_changed, "active-only signature transition")
            else:
                need(extrema[0][2] == extrema[1][2], "absence signature identity")
            for sign, point, signature in selected:
                row_id = "round275-arrangement-region:" + digest([guard["row_id"], path, sign])
                need(row_id in arranged_by_id, "missing arrangement region")
                row = arranged_by_id[row_id]
                need(row["adjacent_rational_region_box"] == r174.box_payload(cell), "arrangement box")
                need(row["active_reason"] == reason and row["strict_derivative_signs_t_p_s"] == derivatives, "arrangement geometry")
                need(row["active_factor_side_sign"] == sign and row["local_return_signature"] == signature, "arrangement signature")
                need(row["extremal_witness_point"] == [str(point.t0), str(point.p0), str(point.s0)], "arrangement witness")
                need(row["connected_open_region"] and row["occurrence_credit"] == row["component_credit"] == row["maximality_credit"] == 0, "arrangement credit")
                seen_arranged.add(row_id)
                expected_arranged += 1
        closure = closure_by_guard.get(guard["row_id"])
        need(closure is not None and closure["fully_closed"] and closure["remaining_failclosed_cell_count"] == 0, "guard closure")
        need(closure["strict_cover_region_count"] == expected_strict and closure["arrangement_region_count"] == expected_arranged, "guard region conservation")
        need(closure["regular_graph_crossing_cell_count"] == crossing_cells and closure["zero_set_absence_cell_count"] == absence_cells, "guard arrangement conservation")
    need(seen_strict == set(strict_by_id), "strict universe exact")
    need(seen_arranged == set(arranged_by_id), "arrangement universe exact")


def attacks(result: dict) -> tuple[int, int]:
    mutations = []
    a = copy.deepcopy(result); a["census"]["arrangement_region_count"] += 1; mutations.append(a)
    a = copy.deepcopy(result); a["strict_region_ledger"]["rows"][0]["row_sha256"] = "0" * 64; mutations.append(a)
    a = copy.deepcopy(result); a["arrangement_region_ledger"]["rows"][0]["local_return_signature"]["roof"] = "FORGED"; mutations.append(a)
    a = copy.deepcopy(result); a["guard_closure_ledger"]["rows"].pop(); mutations.append(a)
    a = copy.deepcopy(result); a["strict_nonpromotion"]["Jx_Jy_same_point_glue_credit"] = 1; mutations.append(a)
    rejected = 0
    for mutation in mutations:
        try:
            structure(mutation)
        except Exception:
            rejected += 1
    return rejected, len(mutations)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("certificate", nargs="?", type=Path, default=CERTIFICATE)
    args = parser.parse_args()
    document = json.loads(args.certificate.read_bytes())
    result = document["result"]
    need(document["result_sha256"] == digest(result), "certificate result digest")
    full_recompute(result)
    rejected, total = attacks(result)
    need(rejected == total, "attack rejection")
    print(json.dumps({
        "status": "PASS_INDEPENDENT_ROUND275",
        "certificate_result_sha256": document["result_sha256"],
        "attack_tests_rejected": rejected,
        "attack_tests_total": total,
        "input_guard_count": 880,
        "materialized_connected_region_count": 13788,
        "remaining_failclosed_cell_count": 0,
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
