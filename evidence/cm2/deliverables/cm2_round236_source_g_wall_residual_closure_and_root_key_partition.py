#!/usr/bin/env python3
"""Close the residual wall boxes and assemble finite key partitions per root."""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import hashlib
import json
import os
from pathlib import Path
import stat
import tempfile
from typing import Any

from flint import arb


H = Path(__file__).resolve().parent
OUT = H / "cm2_round236_source_g_wall_residual_closure_and_root_key_partition_certificate.json"
SCHEMA = "cm2.round236.source-g-wall-residual-closure-and-root-key-partition.v1"
PINS = {
    "cm2_round179_source_g_residual_tube_arrangement_rows.json": "f20b42c1fed781779b537b4d45bf44233eae1ed3ee620b95177a80f0eb2b5e42",
    "cm2_round220_source_g_round179_resolved_child_boundary_atlas_certificate.json": "569a7849b53805ff4deca0eff9a6938a897942d3d682dfef27c27559135ce974",
    "cm2_round234_source_g_wall_endpoint_order_depth6_materialization_certificate.json": "6098032cf429855e816190e9345fa531f70e460eca60d75766e7108fc32c6fac",
    "cm2_round235_source_g_single_endpoint_graph_word_key_partition_certificate.json": "e340fa1a071d85a36b54d10a45ae2fdb9d70b8c90f4c21f054c6fc9505e5e787",
    "cm2_round179_source_g_residual_tube_arrangement.py": "8c568c58d82708a7ab549f126c1fcedfccff563d1d00e3c1f7e6545b4b0d29ab",
}


def need(ok: bool, label: str) -> None:
    if not ok: raise RuntimeError(label)


def can(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False).encode()


def dg(value: Any) -> str:
    return hashlib.sha256(can(value)).hexdigest()


def raw(name: str) -> bytes:
    path = H / name; info = path.lstat(); need(stat.S_ISREG(info.st_mode) and not path.is_symlink() and info.st_nlink == 1, "regular:" + name); data = path.read_bytes(); need(hashlib.sha256(data).hexdigest() == PINS[name], "pin:" + name); return data


def load(name: str) -> dict[str, Any]:
    document = json.loads(raw(name)); need(set(document) == {"schema", "result", "result_sha256"} and dg(document["result"]) == document["result_sha256"], "envelope:" + name); return document["result"]


def unpack(document: dict[str, Any], table: str) -> list[dict[str, Any]]:
    columns = document["row_column_schemas"][table]; return [dict(zip(columns, row, strict=True)) for row in document[table]]


def signature(row: dict[str, Any]) -> dict[str, Any]:
    return {"source_chart": row["chart"], "target_lift": row["owner_target"], "ordered_integer_wall_events": row["ordered_integer_wall_events"], "signed_wall_word": row["signed_wall_word"], "roof": row["roof"], "outgoing_cell": row["outgoing_cell"], "target_chart": row["target_chart"], "official_key_row": row["official_key_row"], "official_key_ordinal": row["official_key_ordinal"], "official_key_id": row["official_key_id"]}


def with_event(base: dict[str, Any], event: list[Any], chart: str, owner: str, registry: dict[str, Any], key_function: Any) -> dict[str, Any]:
    result = dict(base); result["ordered_integer_wall_events"] = [event]; result["signed_wall_word"] = [event[0]]; result["roof"] = 2; key = key_function(chart, owner, (event[0],), registry); result["official_key_row"], result["official_key_ordinal"], result["official_key_id"] = key["row"], key["ordinal"], key["identifier"]; return result


def write(data: bytes) -> None:
    descriptor, name = tempfile.mkstemp(prefix=".round236.", suffix=".tmp", dir=H); temporary = Path(name)
    try:
        with os.fdopen(descriptor, "wb") as handle: handle.write(data); handle.flush(); os.fsync(handle.fileno())
        os.replace(temporary, OUT)
    finally:
        if temporary.exists(): temporary.unlink()


def build() -> dict[str, Any]:
    for name in PINS: raw(name)
    import cm2_round179_source_g_residual_tube_arrangement as r179
    registry = r179.load_inputs()["registry"]
    rows179 = load("cm2_round179_source_g_residual_tube_arrangement_rows.json"); resolved179 = {row["row_id"]: row for row in unpack(rows179, "resolved_3d_child_rows")}
    round220 = load("cm2_round220_source_g_round179_resolved_child_boundary_atlas_certificate.json"); table = round220["coordinate_boundary_atlas"]["tables"]["one_step_split_interface_rows"]; interfaces = {row["split_interface_id"]: row for row in (dict(zip(table["columns"], packed, strict=True)) for packed in table["rows"])}
    round234 = load("cm2_round234_source_g_wall_endpoint_order_depth6_materialization_certificate.json"); round235 = load("cm2_round235_source_g_single_endpoint_graph_word_key_partition_certificate.json")
    double_ids = {row["Round234_frontier_row_id"] for row in round235["double_endpoint_deferred_rows"]}; double_frontier = [row for row in round234["depth6_frontier_rows"] if row["frontier_row_id"] in double_ids]; crossing_frontier = [row for row in round234["depth6_frontier_rows"] if row["reason_labels"][0].startswith("wall_crossing_time_not_strict:")]
    need(len(double_frontier) == 16 and len(crossing_frontier) == 32, "residual universe")
    double_rows, crossing_rows = [], []
    keys_by_interface: dict[str, set[tuple[int, str]]] = defaultdict(set)
    piece_count: Counter[str] = Counter()
    for row in round234["resolved_descendant_rows"]:
        sig = row["local_return_signature"]; keys_by_interface[row["Round220_split_interface_id"]].add((sig["official_key_ordinal"], sig["official_key_id"])); piece_count[row["Round220_split_interface_id"]] += 1
    for row in round235["single_endpoint_graph_partition_rows"]:
        for name in ("event_absent_signature", "event_present_signature"):
            sig = row[name]; keys_by_interface[row["Round220_split_interface_id"]].add((sig["official_key_ordinal"], sig["official_key_id"]))
        piece_count[row["Round220_split_interface_id"]] += 2
    for row in double_frontier:
        reason = row["reason_labels"][0]; _, axis, wall_text = reason.split(":"); wall = int(wall_text); need(wall == 0, "double wall")
        box = r179.box_from(row["box"], row["adaptive_depth"], row["frontier_row_id"]); geometry = r179.interval_geometry(row["chart"], row["owner_target"], box); source_name, target_name = (("source_x", "hit_x") if axis == "X" else ("source_y", "hit_y")); source_dual, target_dual = geometry[source_name], geometry[target_name]
        need(r179.sign(source_dual[0]) == r179.sign(target_dual[0]) == "OVERWRAP", "double factors"); source_derivative, target_derivative = r179.sign(source_dual[1][0]), r179.sign(target_dual[1][0]); need(source_derivative != "OVERWRAP" and target_derivative != "OVERWRAP", "double derivatives")
        interface = interfaces[row["Round220_split_interface_id"]]; sibling_id = interface["lower_child_row_id"] if interface["lower_child_kind"] == "RESOLVED" else interface["upper_child_row_id"]; base = signature(resolved179[sibling_id]); need(base["ordered_integer_wall_events"] == [], "double base word")
        plus = with_event(base, [axis + "+", wall], row["chart"], row["owner_target"], registry, r179.r174.exact_key); minus = with_event(base, [axis + "-", wall], row["chart"], row["owner_target"], registry, r179.r174.exact_key)
        candidates = [base, plus, minus]
        for sig in candidates: keys_by_interface[row["Round220_split_interface_id"]].add((sig["official_key_ordinal"], sig["official_key_id"]))
        piece_count[row["Round220_split_interface_id"]] += 3
        double_rows.append({"double_endpoint_partition_row_id": "round236-double:" + dg(row["frontier_row_id"]), "Round234_frontier_row_id": row["frontier_row_id"], "Round220_split_interface_id": row["Round220_split_interface_id"], "axis": axis, "wall": wall, "source_factor_strict_t_derivative_sign": source_derivative, "target_factor_strict_t_derivative_sign": target_derivative, "same_sign_event_absent_signature": base, "negative_to_positive_signature": plus, "positive_to_negative_signature": minus, "endpoint_graph_union_dimension": 2, "endpoint_graph_union_three_dimensional_volume": 0, "local_finite_exact_key_partition_credit": 1, "whole_root_credit": 0})
    for row in crossing_frontier:
        reason = row["reason_labels"][0]; _, axis, wall_text = reason.split(":"); wall = int(wall_text); box = r179.box_from(row["box"], row["adaptive_depth"], row["frontier_row_id"]); geometry = r179.interval_geometry(row["chart"], row["owner_target"], box); source = geometry["source_x"][0] if axis == "X" else geometry["source_y"][0]; target = geometry["hit_x"][0] if axis == "X" else geometry["hit_y"][0]; source_sign, target_sign = r179.sign(source - arb(wall)), r179.sign(target - arb(wall)); need({source_sign, target_sign} == {"STRICT_NEGATIVE", "STRICT_POSITIVE"}, "opposite endpoints"); token = axis + ("+" if source_sign == "STRICT_NEGATIVE" else "-"); time = (arb(wall) - source) / (target - source)
        interface = interfaces[row["Round220_split_interface_id"]]; sibling_id = interface["lower_child_row_id"] if interface["lower_child_kind"] == "RESOLVED" else interface["upper_child_row_id"]; base = signature(resolved179[sibling_id]); need([token, wall] in base["ordered_integer_wall_events"], "crossing event")
        other_times = []
        for other_token, other_wall in base["ordered_integer_wall_events"]:
            if [other_token, other_wall] == [token, wall]: continue
            other_source = geometry["source_x"][0] if other_token[0] == "X" else geometry["source_y"][0]; other_target = geometry["hit_x"][0] if other_token[0] == "X" else geometry["hit_y"][0]; other_times.append((arb(other_wall) - other_source) / (other_target - other_source))
        need(all(bool(time > other_time) for other_time in other_times), "crossing strict last")
        keys_by_interface[row["Round220_split_interface_id"]].add((base["official_key_ordinal"], base["official_key_id"])); piece_count[row["Round220_split_interface_id"]] += 1
        crossing_rows.append({"crossing_dependency_discharge_row_id": "round236-crossing:" + dg(row["frontier_row_id"]), "Round234_frontier_row_id": row["frontier_row_id"], "Round220_split_interface_id": row["Round220_split_interface_id"], "axis": axis, "wall": wall, "source_endpoint_sign": source_sign, "target_endpoint_sign": target_sign, "transition_event": [token, wall], "exact_endpoint_opposition_proves_time_in_open_unit_interval": True, "event_order_position": "STRICT_LAST", "strictly_preceding_existing_event_count": len(other_times), "local_return_signature": base, "local_exact_key_disposition_credit": 1, "whole_root_credit": 0})
    double_rows.sort(key=lambda row: row["double_endpoint_partition_row_id"]); crossing_rows.sort(key=lambda row: row["crossing_dependency_discharge_row_id"])
    all_interfaces = {row["Round220_split_interface_id"] for row in round234["root_summary_rows"]}; need(len(all_interfaces) == 2_640 and set(keys_by_interface) == all_interfaces, "root coverage")
    root_rows = []
    for interface_id in sorted(all_interfaces):
        keys = sorted(keys_by_interface[interface_id]); root_rows.append({"whole_root_partition_row_id": "round236-root:" + dg(interface_id), "Round220_split_interface_id": interface_id, "finite_partition_piece_count": piece_count[interface_id], "candidate_exact_key_count": len(keys), "candidate_exact_key_ordinals": [item[0] for item in keys], "candidate_exact_key_ids": [item[1] for item in keys], "positive_volume_and_graph_partition_exhaustive": True, "lower_dimensional_graph_volume_credit": 0, "whole_root_local_finite_exact_key_partition_credit": 1, "known_block_incidence_credit": 0, "global_exact_key_fibre_credit": 0})
    histogram = Counter(row["candidate_exact_key_count"] for row in root_rows)
    return {"status": "CERTIFIED_WALL_RESIDUAL_CLOSURE_AND_2640_WHOLE_ROOT_FINITE_KEY_PARTITIONS", "census": {"double_endpoint_box_count": len(double_rows), "crossing_time_box_count": len(crossing_rows), "remaining_unclassified_wall_frontier_count": 0, "whole_root_finite_key_partition_count": len(root_rows), "whole_root_candidate_key_count_histogram": {str(key): value for key, value in sorted(histogram.items())}, "distinct_candidate_exact_key_count": len({ordinal for keys in keys_by_interface.values() for ordinal, _identifier in keys})}, "double_endpoint_partition_rows_sha256": dg(double_rows), "double_endpoint_partition_rows": double_rows, "crossing_dependency_discharge_rows_sha256": dg(crossing_rows), "crossing_dependency_discharge_rows": crossing_rows, "whole_root_finite_key_partition_rows_sha256": dg(root_rows), "whole_root_finite_key_partition_rows": root_rows, "strict_nonpromotion": {"known_block_incidence_credit": 0, "physical_component_credit": 0, "maximal_physical_component_credit": 0, "global_exact_key_fibre_credit": 0, "CM2": "NO-GO_FOR_CLAIM"}, "required_next": "attach the 2640 whole-root finite key partitions to retained common-refinement strata and frozen known blocks"}


def main() -> int:
    parser = argparse.ArgumentParser(); parser.add_argument("--no-write", action="store_true"); arguments = parser.parse_args(); result = build(); document = {"schema": SCHEMA, "result": result, "result_sha256": dg(result)}; data = can(document) + b"\n"
    if not arguments.no_write: write(data)
    print(result["status"]); print(json.dumps(result["census"], sort_keys=True)); print("result_sha256=" + document["result_sha256"]); print("certificate_sha256=" + hashlib.sha256(data).hexdigest()); return 0


if __name__ == "__main__": raise SystemExit(main())
