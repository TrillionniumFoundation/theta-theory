#!/usr/bin/env python3
"""Depth-6 t-adaptive materialization of the deferred outgoing-chart seam."""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from fractions import Fraction as Q
import hashlib
import json
import os
from pathlib import Path
import stat
import sys
import tempfile
from typing import Any

HERE = Path(__file__).resolve().parent
SCHEMA = "cm2.round231.source-g-outgoing-seam-depth6-materialization.v1"
OUTPUT = HERE / "cm2_round231_source_g_outgoing_seam_depth6_materialization_certificate.json"
PINS = {
    "cm2_round179_source_g_residual_tube_arrangement_rows.json":
        "f20b42c1fed781779b537b4d45bf44233eae1ed3ee620b95177a80f0eb2b5e42",
    "cm2_round220_source_g_round179_resolved_child_boundary_atlas_certificate.json":
        "569a7849b53805ff4deca0eff9a6938a897942d3d682dfef27c27559135ce974",
    "cm2_round230_source_g_resolved_retained_bulk_continuation_certificate.json":
        "88d9d826bd985635d42820c7b66389603ab56a48717531ace525ee2eaf6d3a73",
    "cm2_round179_source_g_residual_tube_arrangement.py":
        "8c568c58d82708a7ab549f126c1fcedfccff563d1d00e3c1f7e6545b4b0d29ab",
    "cm2_round174_source_g_unique_first_dynamic_occurrence_materialization_verifier.py":
        "c7ead7c9cb8b4d7b8680e64bfb7870e5c5f5e39277e7c7d3d08a62b600f5c058",
}


def need(ok: bool, label: str) -> None:
    if not ok:
        raise RuntimeError(label)


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=False, allow_nan=False).encode()


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def qstr(value: Q) -> str:
    return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"


def read_pinned(name: str, maximum: int = 400_000_000) -> bytes:
    path = HERE / name
    info = path.lstat()
    need(stat.S_ISREG(info.st_mode) and not path.is_symlink() and info.st_nlink == 1,
         f"regular:{name}")
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


def volume(box: Any) -> Q:
    return (box.t1 - box.t0) * (box.p1 - box.p0) * (box.s1 - box.s0)


def safe_write(data: bytes) -> None:
    fd, name = tempfile.mkstemp(prefix=f".{OUTPUT.name}.", suffix=".tmp", dir=HERE)
    temporary = Path(name)
    try:
        with os.fdopen(fd, "wb") as handle:
            handle.write(data); handle.flush(); os.fsync(handle.fileno())
        os.replace(temporary, OUTPUT)
    finally:
        if temporary.exists(): temporary.unlink()


def build(depth_limit: int) -> dict[str, Any]:
    need(depth_limit == 6, "frozen depth is six")
    for name in PINS:
        read_pinned(name, 5_000_000 if name.endswith(".py") else 400_000_000)
    import cm2_round179_source_g_residual_tube_arrangement as r179
    need(Path(r179.__file__).resolve() == (HERE / "cm2_round179_source_g_residual_tube_arrangement.py").resolve(),
         "Round179 module")
    r174 = r179.r174
    inputs = r179.load_inputs()
    registry = inputs["registry"]

    rows179 = load_result("cm2_round179_source_g_residual_tube_arrangement_rows.json")
    origins = {row["origin_row_id"]: row for row in unpack(rows179, "origin_tube_rows")}
    retained = {row["row_id"]: row for row in unpack(rows179, "retained_3d_child_rows")}
    r220 = load_result("cm2_round220_source_g_round179_resolved_child_boundary_atlas_certificate.json")
    table = r220["coordinate_boundary_atlas"]["tables"]["one_step_split_interface_rows"]
    interfaces = []
    for packed in table["rows"]:
        row = dict(zip(table["columns"], packed, strict=True))
        if {row["lower_child_kind"], row["upper_child_kind"]} != {"RESOLVED", "RETAINED"}:
            continue
        retained_id = row["upper_child_row_id"] if row["upper_child_kind"] == "RETAINED" else row["lower_child_row_id"]
        interfaces.append((row["split_interface_id"], retained_id))
    need(len(interfaces) == 8_960, "interface census")
    r230 = load_result("cm2_round230_source_g_resolved_retained_bulk_continuation_certificate.json")
    accepted_interfaces = {row["Round220_split_interface_id"] for row in r230["formal_certified_local_bulk_bridge_star_ledger"]["rows"]}
    roots = [(interface_id, retained[retained_id]) for interface_id, retained_id in interfaces
             if interface_id not in accepted_interfaces and retained[retained_id]["reason_labels"] == ["outgoing_chart_seam"]]
    roots.sort(key=lambda item: item[0])
    need(len(roots) == 5_368, "outgoing seam root census")

    resolved_rows: list[dict[str, Any]] = []
    guard_rows: list[dict[str, Any]] = []
    frontier_rows: list[dict[str, Any]] = []
    depth_census: dict[int, Counter[str]] = defaultdict(Counter)
    depth_volume: dict[int, Counter[str]] = defaultdict(Counter)
    root_summaries = []
    for interface_id, root in roots:
        owner = origins[root["origin_row_id"]]["owner_target"]
        initial = r179.box_from(root["box"], len(root["refinement_path"]), root["row_id"])
        nodes = [(initial, [])]
        root_resolved = root_guard = 0
        released_volume = Q(0)
        for depth in range(1, depth_limit + 1):
            next_nodes = []
            for box, path in nodes:
                children = r174.bisect(box, 0)
                for child_index, child in enumerate(children):
                    child_path = [*path, child_index]
                    kind, data = r174.classify_child(root["chart"], child, owner, registry)
                    child_volume = volume(child)
                    depth_census[depth][kind] += 1
                    depth_volume[depth][kind] += child_volume
                    base = {
                        "Round220_split_interface_id": interface_id,
                        "Round179_retained_child_row_id": root["row_id"],
                        "origin_row_id": root["origin_row_id"],
                        "parent_id": root["parent_id"], "chart": root["chart"],
                        "owner_target": owner, "adaptive_depth": depth,
                        "binary_t_path": child_path, "box": r174.box_values(child),
                        "coordinate_volume": qstr(child_volume),
                    }
                    if kind == "resolved":
                        root_resolved += 1; released_volume += child_volume
                        signature = data
                        resolved_rows.append({
                            "materialized_row_id": "round231-resolved:" + digest([interface_id, child_path, base["box"], signature]),
                            **base, "local_return_signature": {
                                "source_chart": root["chart"], "target_lift": owner,
                                "ordered_integer_wall_events": signature["events"],
                                "signed_wall_word": list(signature["pattern"]),
                                "roof": signature["roof"], "outgoing_cell": signature["outgoing"],
                                "target_chart": signature["target_chart"],
                                "official_key_row": signature["key"]["row"],
                                "official_key_ordinal": signature["key"]["ordinal"],
                                "official_key_id": signature["key"]["identifier"],
                            }, "credit_kind": "LOCAL_POSITIVE_3D_OCCURRENCE_ONLY",
                            "known_block_incidence_credit": 0, "physical_component_credit": 0,
                            "global_exact_key_disposition_credit": 0,
                        })
                    elif kind == "guard":
                        root_guard += 1; released_volume += child_volume
                        guard_rows.append({
                            "guard_row_id": "round231-guard:" + digest([interface_id, child_path, base["box"]]),
                            **base, "exact_rejection_predicate": "min|t| gives 2*t^2-1>0",
                            "physical_component_credit": 0, "global_exact_key_disposition_credit": 0,
                        })
                    else:
                        need(data == ["outgoing_chart_seam"], "pure outgoing retained reason")
                        next_nodes.append((child, child_path))
            nodes = next_nodes
        retained_volume = sum((volume(box) for box, _path in nodes), Q(0))
        need(released_volume + retained_volume == Q(root["coordinate_volume"]), "root volume conservation")
        for box, path in nodes:
            frontier_rows.append({
                "frontier_row_id": "round231-depth6-frontier:" + digest([interface_id, path, r174.box_values(box)]),
                "Round220_split_interface_id": interface_id,
                "Round179_retained_child_row_id": root["row_id"],
                "origin_row_id": root["origin_row_id"], "parent_id": root["parent_id"],
                "chart": root["chart"], "owner_target": owner,
                "adaptive_depth": depth_limit, "binary_t_path": path,
                "box": r174.box_values(box), "coordinate_volume": qstr(volume(box)),
                "reason_labels": ["outgoing_chart_seam"],
                "physical_component_credit": 0, "global_exact_key_disposition_credit": 0,
            })
        root_summaries.append({
            "root_summary_id": "round231-root:" + digest(interface_id),
            "Round220_split_interface_id": interface_id,
            "Round179_retained_child_row_id": root["row_id"],
            "resolved_descendant_count": root_resolved, "guard_descendant_count": root_guard,
            "depth6_retained_frontier_count": len(nodes),
            "released_coordinate_volume": qstr(released_volume),
            "retained_coordinate_volume": qstr(retained_volume),
        })

    for rows in (resolved_rows, guard_rows, frontier_rows, root_summaries):
        rows.sort(key=lambda row: next(value for key, value in row.items() if key.endswith("_id")))
    census = {
        "outgoing_seam_root_count": len(roots), "adaptive_depth": depth_limit,
        "materialized_resolved_descendant_count": len(resolved_rows),
        "materialized_guard_descendant_count": len(guard_rows),
        "depth6_retained_frontier_count": len(frontier_rows),
        "roots_fully_resolved_or_guarded_count": sum(row["depth6_retained_frontier_count"] == 0 for row in root_summaries),
        "distinct_released_exact_key_count": len({row["local_return_signature"]["official_key_ordinal"] for row in resolved_rows}),
    }
    return {
        "status": "DEPTH6_OUTGOING_SEAM_ADAPTIVE_MATERIALIZATION_COMPLETE_ZERO_GLOBAL_PROMOTION",
        "census": census,
        "depth_census": {str(d): dict(sorted(c.items())) for d, c in sorted(depth_census.items())},
        "depth_coordinate_volume": {str(d): {k: qstr(v) for k, v in sorted(c.items())} for d, c in sorted(depth_volume.items())},
        "resolved_descendant_rows_sha256": digest(resolved_rows),
        "guard_descendant_rows_sha256": digest(guard_rows),
        "depth6_frontier_rows_sha256": digest(frontier_rows),
        "root_summary_rows_sha256": digest(root_summaries),
        "resolved_descendant_rows": resolved_rows, "guard_descendant_rows": guard_rows,
        "depth6_frontier_rows": frontier_rows, "root_summary_rows": root_summaries,
        "strict_nonpromotion": {"known_block_incidence_credit": 0, "physical_component_credit": 0,
                                "maximal_physical_component_credit": 0,
                                "global_exact_key_disposition_credit": 0, "CM2": "NO-GO_FOR_CLAIM"},
        "required_next": "attach only exact positive-area/event-trace descendants to frozen known blocks with an independent verifier",
    }


def main() -> int:
    parser = argparse.ArgumentParser(); parser.add_argument("--depth", type=int, default=6); parser.add_argument("--no-write", action="store_true")
    args = parser.parse_args(); result = build(args.depth)
    document = {"schema": SCHEMA, "result": result, "result_sha256": digest(result)}
    encoded = canonical(document) + b"\n"
    if not args.no_write: safe_write(encoded)
    print(result["status"]); print(json.dumps(result["census"], sort_keys=True))
    print(f"result_sha256={document['result_sha256']}"); print(f"certificate_sha256={hashlib.sha256(encoded).hexdigest()}")
    return 0


if __name__ == "__main__": raise SystemExit(main())
