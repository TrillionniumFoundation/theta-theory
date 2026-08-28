#!/usr/bin/env python3
"""Independently verify the Round235 single-endpoint key partitions."""

from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import json
import os
from pathlib import Path
import stat
import tempfile
from typing import Any

from flint import arb


H = Path(__file__).resolve().parent
OUT = H / "cm2_round235_source_g_single_endpoint_graph_word_key_partition_verification.json"
P = {
    "cm2_round179_source_g_residual_tube_arrangement_rows.json": "f20b42c1fed781779b537b4d45bf44233eae1ed3ee620b95177a80f0eb2b5e42",
    "cm2_round220_source_g_round179_resolved_child_boundary_atlas_certificate.json": "569a7849b53805ff4deca0eff9a6938a897942d3d682dfef27c27559135ce974",
    "cm2_round234_source_g_wall_endpoint_order_depth6_materialization_certificate.json": "6098032cf429855e816190e9345fa531f70e460eca60d75766e7108fc32c6fac",
    "cm2_round179_source_g_residual_tube_arrangement.py": "8c568c58d82708a7ab549f126c1f7e6545b4b0d29ab",
    "cm2_round235_source_g_single_endpoint_graph_word_key_partition.py": "8e5f807dfc43632d59cc9c994fd58907080a52bedc7789f8bb507b002ce8641a",
    "cm2_round235_source_g_single_endpoint_graph_word_key_partition_certificate.json": "e340fa1a071d85a36b54d10a45ae2fdb9d70b8c90f4c21f054c6fc9505e5e787",
}
P["cm2_round179_source_g_residual_tube_arrangement.py"] = "8c568c58d82708a7ab549f126c1fcedfccff563d1d00e3c1f7e6545b4b0d29ab"


def need(value: bool, label: str) -> None:
    if not value:
        raise RuntimeError(label)


def can(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False).encode()


def dg(value: Any) -> str:
    return hashlib.sha256(can(value)).hexdigest()


def raw(name: str) -> bytes:
    path = H / name
    info = path.lstat()
    need(stat.S_ISREG(info.st_mode) and not path.is_symlink() and info.st_nlink == 1, "regular:" + name)
    data = path.read_bytes()
    need(hashlib.sha256(data).hexdigest() == P[name], "pin:" + name)
    return data


def load(name: str) -> dict[str, Any]:
    document = json.loads(raw(name))
    need(set(document) == {"schema", "result", "result_sha256"} and dg(document["result"]) == document["result_sha256"], "envelope:" + name)
    return document["result"]


def unpack(document: dict[str, Any], table: str) -> list[dict[str, Any]]:
    columns = document["row_column_schemas"][table]
    return [dict(zip(columns, row, strict=True)) for row in document[table]]


def sig(row: dict[str, Any]) -> dict[str, Any]:
    return {"source_chart": row["chart"], "target_lift": row["owner_target"], "ordered_integer_wall_events": row["ordered_integer_wall_events"], "signed_wall_word": row["signed_wall_word"], "roof": row["roof"], "outgoing_cell": row["outgoing_cell"], "target_chart": row["target_chart"], "official_key_row": row["official_key_row"], "official_key_ordinal": row["official_key_ordinal"], "official_key_id": row["official_key_id"]}


def changed(base: dict[str, Any], events: list[list[Any]], chart: str, owner: str, registry: dict[str, Any], key_function: Any) -> dict[str, Any]:
    result = dict(base)
    result["ordered_integer_wall_events"] = events
    result["signed_wall_word"] = [event[0] for event in events]
    result["roof"] = len(events) + 1
    key = key_function(chart, owner, tuple(result["signed_wall_word"]), registry)
    result["official_key_row"], result["official_key_ordinal"], result["official_key_id"] = key["row"], key["ordinal"], key["identifier"]
    return result


def write(data: bytes) -> None:
    descriptor, name = tempfile.mkstemp(prefix=".round235.", suffix=".tmp", dir=H)
    temporary = Path(name)
    try:
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(data); handle.flush(); os.fsync(handle.fileno())
        os.replace(temporary, OUT)
    finally:
        if temporary.exists(): temporary.unlink()


def verify() -> dict[str, Any]:
    for name in P: raw(name)
    import cm2_round179_source_g_residual_tube_arrangement as r179
    registry = r179.load_inputs()["registry"]
    rows179 = load("cm2_round179_source_g_residual_tube_arrangement_rows.json")
    resolved = {row["row_id"]: row for row in unpack(rows179, "resolved_3d_child_rows")}
    round220 = load("cm2_round220_source_g_round179_resolved_child_boundary_atlas_certificate.json")
    table = round220["coordinate_boundary_atlas"]["tables"]["one_step_split_interface_rows"]
    interfaces = {row["split_interface_id"]: row for row in (dict(zip(table["columns"], packed, strict=True)) for packed in table["rows"])}
    round234 = load("cm2_round234_source_g_wall_endpoint_order_depth6_materialization_certificate.json")
    candidate = load("cm2_round235_source_g_single_endpoint_graph_word_key_partition_certificate.json")
    got = {row["Round234_frontier_row_id"]: row for row in candidate["single_endpoint_graph_partition_rows"]}
    deferred = {row["Round234_frontier_row_id"]: row for row in candidate["double_endpoint_deferred_rows"]}
    endpoints = [row for row in round234["depth6_frontier_rows"] if row["reason_labels"][0].startswith("wall_endpoint_or_count_transition:")]
    active_hist, token_hist, keys = Counter(), Counter(), set()
    single_count = double_count = 0
    for row in endpoints:
        reason = row["reason_labels"][0]; _, axis, wall_text = reason.split(":"); wall = int(wall_text)
        box = r179.box_from(row["box"], row["adaptive_depth"], row["frontier_row_id"]); geometry = r179.interval_geometry(row["chart"], row["owner_target"], box)
        source_name, target_name = (("source_x", "hit_x") if axis == "X" else ("source_y", "hit_y")); source, target = geometry[source_name][0], geometry[target_name][0]
        source_sign, target_sign = r179.sign(source - arb(wall)), r179.sign(target - arb(wall)); active = (["source"] if source_sign == "OVERWRAP" else []) + (["target"] if target_sign == "OVERWRAP" else [])
        if len(active) == 2:
            double_count += 1; need(row["frontier_row_id"] in deferred and deferred[row["frontier_row_id"]]["exact_key_partition_credit"] == 0, "double"); continue
        need(len(active) == 1, "active"); factor = active[0]; fixed = target_sign if factor == "source" else source_sign
        token = axis + ("+" if (factor == "source" and fixed == "STRICT_POSITIVE") or (factor == "target" and fixed == "STRICT_NEGATIVE") else "-")
        interface = interfaces[row["Round220_split_interface_id"]]; sibling_id = interface["lower_child_row_id"] if interface["lower_child_kind"] == "RESOLVED" else interface["upper_child_row_id"]; base = sig(resolved[sibling_id]); event = [token, wall]; events = [list(item) for item in base["ordered_integer_wall_events"]]
        candidate_time = (arb(wall) - source) / (target - source); other_times = []
        for other_token, other_wall in events:
            if [other_token, other_wall] == event: continue
            other_source = geometry["source_x"][0] if other_token[0] == "X" else geometry["source_y"][0]; other_target = geometry["hit_x"][0] if other_token[0] == "X" else geometry["hit_y"][0]
            other_times.append((arb(other_wall) - other_source) / (other_target - other_source))
        need(all(bool(candidate_time < other) for other in other_times) if factor == "source" else all(bool(candidate_time > other) for other in other_times), "order")
        if event in events:
            present = base; absent_events = list(events); absent_events.remove(event); absent = changed(base, absent_events, row["chart"], row["owner_target"], registry, r179.r174.exact_key)
        else:
            absent = base; present = changed(base, [event, *events] if factor == "source" else [*events, event], row["chart"], row["owner_target"], registry, r179.r174.exact_key)
        derivative = geometry[source_name][1][0] if factor == "source" else geometry[target_name][1][0]; derivative_sign = r179.sign(derivative); need(derivative_sign != "OVERWRAP", "derivative")
        expected = {"endpoint_graph_partition_row_id": "round235-single-endpoint:" + dg(row["frontier_row_id"]), "Round234_frontier_row_id": row["frontier_row_id"], "Round220_split_interface_id": row["Round220_split_interface_id"], "source_chart": row["chart"], "target_lift": row["owner_target"], "reason_label": reason, "active_endpoint_factor": factor, "active_factor_strict_t_derivative_sign": derivative_sign, "fixed_endpoint_factor_sign": fixed, "transition_event": event, "transition_event_order_position": "STRICT_FIRST" if factor == "source" else "STRICT_LAST", "candidate_time_strict_against_existing_event_count": len(other_times), "event_absent_signature": absent, "event_present_signature": present, "distinct_side_exact_key_count": len({absent["official_key_id"], present["official_key_id"]}), "endpoint_graph_dimension": 2, "endpoint_graph_three_dimensional_coordinate_volume": 0, "local_finite_exact_key_partition_credit": 1, "whole_root_exact_key_disposition_credit": 0, "known_block_incidence_credit": 0, "global_exact_key_fibre_credit": 0}
        need(got.get(row["frontier_row_id"]) == expected, "row"); single_count += 1; active_hist[factor] += 1; token_hist[token] += 1; keys.update((absent["official_key_ordinal"], present["official_key_ordinal"]))
    need((single_count, double_count) == (38_328, 16), "counts")
    census = candidate["census"]; need(census["certified_single_endpoint_graph_partition_count"] == single_count and census["deferred_double_endpoint_factor_count"] == double_count and census["active_factor_histogram"] == dict(sorted(active_hist.items())) and census["transition_token_histogram"] == dict(sorted(token_hist.items())) and census["distinct_candidate_exact_key_count"] == len(keys), "census")
    need(candidate["strict_nonpromotion"]["CM2"] == "NO-GO_FOR_CLAIM", "nonpromotion")
    return {"status": "PASS_INDEPENDENT_ROUND235", "candidate_sha256": P["cm2_round235_source_g_single_endpoint_graph_word_key_partition_certificate.json"], "candidate_result_sha256": dg(candidate), "producer_imported_or_executed": False, "independently_recomputed_single_endpoint_count": single_count, "deferred_double_endpoint_count": double_count, "strict_event_order_count": single_count, "distinct_candidate_exact_key_count": len(keys), "strict_nonpromotion_reconfirmed": True}


def main() -> int:
    parser = argparse.ArgumentParser(); parser.add_argument("--no-write", action="store_true"); arguments = parser.parse_args(); result = verify(); document = {"schema": "cm2.round235.source-g-single-endpoint-graph-word-key-partition.verification.v1", "result": result, "result_sha256": dg(result)}; data = can(document) + b"\n"
    if not arguments.no_write: write(data)
    print(result["status"]); print(json.dumps(result, sort_keys=True)); print("verification_result_sha256=" + document["result_sha256"]); return 0


if __name__ == "__main__": raise SystemExit(main())
