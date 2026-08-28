#!/usr/bin/env python3
"""Certify single-endpoint graph wall-word and exact-key partitions."""

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


HERE = Path(__file__).resolve().parent
OUTPUT = HERE / "cm2_round235_source_g_single_endpoint_graph_word_key_partition_certificate.json"
SCHEMA = "cm2.round235.source-g-single-endpoint-graph-word-key-partition.v1"
PINS = {
    "cm2_round179_source_g_residual_tube_arrangement_rows.json": "f20b42c1fed781779b537b4d45bf44233eae1ed3ee620b95177a80f0eb2b5e42",
    "cm2_round220_source_g_round179_resolved_child_boundary_atlas_certificate.json": "569a7849b53805ff4deca0eff9a6938a897942d3d682dfef27c27559135ce974",
    "cm2_round234_source_g_wall_endpoint_order_depth6_materialization_certificate.json": "6098032cf429855e816190e9345fa531f70e460eca60d75766e7108fc32c6fac",
    "cm2_round179_source_g_residual_tube_arrangement.py": "8c568c58d82708a7ab549f126c1fcedfccff563d1d00e3c1f7e6545b4b0d29ab",
}


def need(ok: bool, label: str) -> None:
    if not ok:
        raise RuntimeError(label)


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False).encode()


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def read_pinned(name: str, maximum: int = 400_000_000) -> bytes:
    path = HERE / name
    info = path.lstat()
    need(stat.S_ISREG(info.st_mode) and not path.is_symlink() and info.st_nlink == 1, f"regular:{name}")
    need(0 < info.st_size <= maximum, f"size:{name}")
    raw = path.read_bytes()
    need(hashlib.sha256(raw).hexdigest() == PINS[name], f"pin:{name}")
    return raw


def load_result(name: str) -> dict[str, Any]:
    document = json.loads(read_pinned(name))
    need(set(document) == {"schema", "result", "result_sha256"}, f"envelope:{name}")
    need(digest(document["result"]) == document["result_sha256"], f"digest:{name}")
    return document["result"]


def unpack(document: dict[str, Any], table: str) -> list[dict[str, Any]]:
    columns = document["row_column_schemas"][table]
    return [dict(zip(columns, row, strict=True)) for row in document[table]]


def signature(row: dict[str, Any]) -> dict[str, Any]:
    return {"source_chart": row["chart"], "target_lift": row["owner_target"], "ordered_integer_wall_events": row["ordered_integer_wall_events"], "signed_wall_word": row["signed_wall_word"], "roof": row["roof"], "outgoing_cell": row["outgoing_cell"], "target_chart": row["target_chart"], "official_key_row": row["official_key_row"], "official_key_ordinal": row["official_key_ordinal"], "official_key_id": row["official_key_id"]}


def with_events(base: dict[str, Any], events: list[list[Any]], chart: str, owner: str, registry: dict[str, Any], exact_key: Any) -> dict[str, Any]:
    result = dict(base)
    result["ordered_integer_wall_events"] = events
    result["signed_wall_word"] = [event[0] for event in events]
    result["roof"] = len(events) + 1
    key = exact_key(chart, owner, tuple(result["signed_wall_word"]), registry)
    result["official_key_row"] = key["row"]
    result["official_key_ordinal"] = key["ordinal"]
    result["official_key_id"] = key["identifier"]
    return result


def safe_write(data: bytes) -> None:
    descriptor, name = tempfile.mkstemp(prefix=f".{OUTPUT.name}.", suffix=".tmp", dir=HERE)
    temporary = Path(name)
    try:
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, OUTPUT)
    finally:
        if temporary.exists():
            temporary.unlink()


def build() -> dict[str, Any]:
    for name in PINS:
        read_pinned(name, 5_000_000 if name.endswith(".py") else 400_000_000)
    import cm2_round179_source_g_residual_tube_arrangement as r179

    registry = r179.load_inputs()["registry"]
    rows179 = load_result("cm2_round179_source_g_residual_tube_arrangement_rows.json")
    resolved = {row["row_id"]: row for row in unpack(rows179, "resolved_3d_child_rows")}
    round220 = load_result("cm2_round220_source_g_round179_resolved_child_boundary_atlas_certificate.json")
    table = round220["coordinate_boundary_atlas"]["tables"]["one_step_split_interface_rows"]
    interfaces = {row["split_interface_id"]: row for row in (dict(zip(table["columns"], packed, strict=True)) for packed in table["rows"])}
    round234 = load_result("cm2_round234_source_g_wall_endpoint_order_depth6_materialization_certificate.json")
    endpoint_rows = [row for row in round234["depth6_frontier_rows"] if row["reason_labels"][0].startswith("wall_endpoint_or_count_transition:")]
    released_by_interface: dict[str, list[dict[str, Any]]] = {}
    for row in round234["resolved_descendant_rows"]:
        released_by_interface.setdefault(row["Round220_split_interface_id"], []).append(row["local_return_signature"])
    certified_rows = []
    double_rows = []
    active_histogram: Counter[str] = Counter()
    token_histogram: Counter[str] = Counter()
    for row in endpoint_rows:
        reason = row["reason_labels"][0]
        _kind, axis, wall_text = reason.split(":")
        wall = int(wall_text)
        box = r179.box_from(row["box"], row["adaptive_depth"], row["frontier_row_id"])
        geometry = r179.interval_geometry(row["chart"], row["owner_target"], box)
        source_name = "source_x" if axis == "X" else "source_y"
        target_name = "hit_x" if axis == "X" else "hit_y"
        source = geometry[source_name][0]
        target = geometry[target_name][0]
        source_sign = r179.sign(source - arb(wall))
        target_sign = r179.sign(target - arb(wall))
        active = []
        if source_sign == "OVERWRAP":
            active.append("source")
        if target_sign == "OVERWRAP":
            active.append("target")
        if len(active) == 2:
            double_rows.append({"deferred_row_id": "round235-double-endpoint:" + digest(row["frontier_row_id"]), "Round234_frontier_row_id": row["frontier_row_id"], "Round220_split_interface_id": row["Round220_split_interface_id"], "reason_label": reason, "active_factors": active, "required_next": "two-factor endpoint arrangement", "exact_key_partition_credit": 0})
            continue
        need(len(active) == 1, f"active factor:{row['frontier_row_id']}")
        active_factor = active[0]
        fixed_sign = target_sign if active_factor == "source" else source_sign
        need(fixed_sign in {"STRICT_NEGATIVE", "STRICT_POSITIVE"}, f"fixed sign:{row['frontier_row_id']}")
        positive_token = (active_factor == "source" and fixed_sign == "STRICT_POSITIVE") or (active_factor == "target" and fixed_sign == "STRICT_NEGATIVE")
        token = axis + ("+" if positive_token else "-")
        candidate_time = (arb(wall) - source) / (target - source)
        interface = interfaces[row["Round220_split_interface_id"]]
        sibling_id = interface["lower_child_row_id"] if interface["lower_child_kind"] == "RESOLVED" else interface["upper_child_row_id"]
        base_signature = signature(resolved[sibling_id])
        event = [token, wall]
        base_events = [list(item) for item in base_signature["ordered_integer_wall_events"]]
        other_times = []
        for other_token, other_wall in base_events:
            if [other_token, other_wall] == event:
                continue
            other_source = geometry["source_x"][0] if other_token[0] == "X" else geometry["source_y"][0]
            other_target = geometry["hit_x"][0] if other_token[0] == "X" else geometry["hit_y"][0]
            other_times.append((arb(other_wall) - other_source) / (other_target - other_source))
        if active_factor == "source":
            need(all(bool(candidate_time < other_time) for other_time in other_times), f"strict first:{row['frontier_row_id']}")
            insertion_position = "STRICT_FIRST"
        else:
            need(all(bool(candidate_time > other_time) for other_time in other_times), f"strict last:{row['frontier_row_id']}")
            insertion_position = "STRICT_LAST"
        if event in base_events:
            present = base_signature
            absent_events = list(base_events)
            absent_events.remove(event)
            absent = with_events(base_signature, absent_events, row["chart"], row["owner_target"], registry, r179.r174.exact_key)
        else:
            absent = base_signature
            present_events = [event, *base_events] if active_factor == "source" else [*base_events, event]
            present = with_events(base_signature, present_events, row["chart"], row["owner_target"], registry, r179.r174.exact_key)
        allowed = {digest(absent), digest(present)}
        need(all(digest(item) in allowed for item in released_by_interface.get(row["Round220_split_interface_id"], [])), f"released pair:{row['frontier_row_id']}")
        active_derivative = geometry[source_name][1][0] if active_factor == "source" else geometry[target_name][1][0]
        derivative_sign = r179.sign(active_derivative)
        need(derivative_sign in {"STRICT_NEGATIVE", "STRICT_POSITIVE"}, f"derivative:{row['frontier_row_id']}")
        active_histogram[active_factor] += 1
        token_histogram[token] += 1
        certified_rows.append({
            "endpoint_graph_partition_row_id": "round235-single-endpoint:" + digest(row["frontier_row_id"]),
            "Round234_frontier_row_id": row["frontier_row_id"],
            "Round220_split_interface_id": row["Round220_split_interface_id"],
            "source_chart": row["chart"],
            "target_lift": row["owner_target"],
            "reason_label": reason,
            "active_endpoint_factor": active_factor,
            "active_factor_strict_t_derivative_sign": derivative_sign,
            "fixed_endpoint_factor_sign": fixed_sign,
            "transition_event": event,
            "transition_event_order_position": insertion_position,
            "candidate_time_strict_against_existing_event_count": len(other_times),
            "event_absent_signature": absent,
            "event_present_signature": present,
            "distinct_side_exact_key_count": len({absent["official_key_id"], present["official_key_id"]}),
            "endpoint_graph_dimension": 2,
            "endpoint_graph_three_dimensional_coordinate_volume": 0,
            "local_finite_exact_key_partition_credit": 1,
            "whole_root_exact_key_disposition_credit": 0,
            "known_block_incidence_credit": 0,
            "global_exact_key_fibre_credit": 0,
        })
    certified_rows.sort(key=lambda item: item["endpoint_graph_partition_row_id"])
    double_rows.sort(key=lambda item: item["deferred_row_id"])
    need(len(certified_rows) == 38_328 and len(double_rows) == 16, "frontier partition")
    census = {
        "Round234_endpoint_frontier_count": len(endpoint_rows),
        "certified_single_endpoint_graph_partition_count": len(certified_rows),
        "deferred_double_endpoint_factor_count": len(double_rows),
        "strict_event_order_count": len(certified_rows),
        "active_factor_histogram": dict(sorted(active_histogram.items())),
        "transition_token_histogram": dict(sorted(token_histogram.items())),
        "distinct_candidate_exact_key_count": len({signature["official_key_ordinal"] for item in certified_rows for signature in (item["event_absent_signature"], item["event_present_signature"])}),
    }
    return {
        "status": "CERTIFIED_38328_SINGLE_ENDPOINT_GRAPH_WORD_KEY_PARTITIONS_16_DOUBLE_FACTORS_DEFERRED",
        "census": census,
        "single_endpoint_graph_partition_rows_sha256": digest(certified_rows),
        "single_endpoint_graph_partition_rows": certified_rows,
        "double_endpoint_deferred_rows_sha256": digest(double_rows),
        "double_endpoint_deferred_rows": double_rows,
        "strict_nonpromotion": {"whole_root_exact_key_disposition_credit": 0, "known_block_incidence_credit": 0, "physical_component_credit": 0, "maximal_physical_component_credit": 0, "global_exact_key_fibre_credit": 0, "CM2": "NO-GO_FOR_CLAIM"},
        "required_next": "close 16 double-endpoint and 32 crossing-time boxes, then union the finite key partitions per original root",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--no-write", action="store_true")
    arguments = parser.parse_args()
    result = build()
    document = {"schema": SCHEMA, "result": result, "result_sha256": digest(result)}
    encoded = canonical(document) + b"\n"
    if not arguments.no_write:
        safe_write(encoded)
    print(result["status"])
    print(json.dumps(result["census"], sort_keys=True))
    print(f"result_sha256={document['result_sha256']}")
    print(f"certificate_sha256={hashlib.sha256(encoded).hexdigest()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
