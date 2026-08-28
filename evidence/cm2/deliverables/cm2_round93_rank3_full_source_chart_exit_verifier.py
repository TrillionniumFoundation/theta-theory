#!/usr/bin/env python3
"""Independent 640-bit audit of the Round93 source-chart event isolation."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import cm2_round93_rank3_full_source_chart_exit_cert as cert
from cm2_round79_tangency_intersection_generator import digest


HERE = Path(__file__).resolve().parent
MANIFEST = HERE / "cm2-round93-rank3-full-source-chart-exit-2026-07-22.json"
PRODUCER_SHA = "cec3bc83ae2a9df015441ce72397c2d553a74baf2cab89946a220ee4debb1023"


def hook(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("duplicate JSON key")
        result[key] = value
    return result


def bad(value):
    raise ValueError(f"nonfinite JSON number: {value}")


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def summary(result):
    return (
        result["input_round92_frozen_core_exit_ray_count"],
        result["certified_first_full_source_chart_event_count"],
        tuple(sorted(result["terminal_event_type_histogram"].items())),
        result["remaining_untyped_full_source_chart_ray_count"],
        sum(row["strict_point_probe_count"] for row in result["ray_rows"]),
    )


def signature(result):
    return sorted(
        (
            row["exterior_port_id"],
            tuple(row["branch_key"]),
            row["projective_end"],
            row["terminal_event_type"],
            row["strict_point_probe_count"],
            row["whole_open_ray_status"],
        )
        for row in result["ray_rows"]
    )


def verify(frozen, higher):
    if set(frozen) != {"schema", "result", "result_sha256"}:
        raise ValueError("closed schema")
    if frozen["schema"] != cert.SCHEMA:
        raise ValueError("schema")
    if digest(frozen["result"]) != frozen["result_sha256"]:
        raise ValueError("result digest")
    if digest(frozen["result"]["ray_rows"]) != frozen["result"]["ray_rows_sha256"]:
        raise ValueError("row digest")
    if summary(frozen["result"]) != (65, 65, (("SOURCE_CHART_SEAM", 28), ("SOURCE_GRAZING", 37)), 0, 8320):
        raise ValueError("frozen summary")
    if summary(frozen["result"]) != summary(higher["result"]):
        raise ValueError("higher precision summary")
    if signature(frozen["result"]) != signature(higher["result"]):
        raise ValueError("higher precision signature")


def build():
    if sha(HERE / "cm2_round93_rank3_full_source_chart_exit_cert.py") != PRODUCER_SHA:
        raise RuntimeError("producer pin")
    frozen = json.loads(MANIFEST.read_text(), object_pairs_hook=hook, parse_constant=bad)
    higher = cert.build(640)
    verify(frozen, higher)
    rejected = 0
    for field, value in (
        ("certified_first_full_source_chart_event_count", 64),
        ("remaining_untyped_full_source_chart_ray_count", 1),
        ("input_round92_frozen_core_exit_ray_count", 64),
    ):
        changed = json.loads(json.dumps(frozen))
        changed["result"][field] = value
        changed["result_sha256"] = digest(changed["result"])
        try:
            verify(changed, higher)
        except ValueError:
            rejected += 1
    result = {
        "status": "PASS",
        "independent_precision_bits": 640,
        "higher_precision_summary": summary(higher["result"]),
        "hostile_semantic_mutations_rejected": f"{rejected}/3",
        "strict_json_loader": "duplicate and nonfinite rejected",
        "producer_sha256": PRODUCER_SHA,
        "manifest_sha256": sha(MANIFEST),
    }
    return {"schema": "cm2.round93.rank3-full-source-chart-exit.audit.v1", "result": result, "result_sha256": digest(result)}


if __name__ == "__main__":
    print(json.dumps(build(), sort_keys=True, indent=2))
