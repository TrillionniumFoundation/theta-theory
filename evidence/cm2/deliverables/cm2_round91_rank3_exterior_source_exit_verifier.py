#!/usr/bin/env python3
"""768-bit audit of the Round91 exterior source-exit frontier."""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

from cm2_round79_tangency_intersection_generator import digest
import cm2_round91_rank3_exterior_source_exit_cert as cert

HERE = Path(__file__).resolve().parent
MANIFEST = HERE / "cm2-round91-rank3-exterior-source-exit-2026-07-22.json"
PRODUCER_SHA = "d75eb3a9a6aeca2c45b5b9eaa487c32481d4a9cf7e3da04c5d45d6f9a79414da"


def hook(pairs):
    out = {}
    for key, value in pairs:
        if key in out:
            raise ValueError("duplicate JSON key")
        out[key] = value
    return out


def bad(value):
    raise ValueError(f"nonfinite JSON number: {value}")


def load():
    return json.loads(
        MANIFEST.read_text(), object_pairs_hook=hook, parse_constant=bad
    )


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def summary(result):
    return (
        result["input_exterior_projective_ray_count"],
        result["certified_source_exit_ray_count"],
        result["remaining_untyped_exterior_ray_count"],
        len(result["ray_rows"]),
        len(result["unresolved_ray_rows"]),
        result["complete_rank3_projective_branch_continuation_within_frozen_source_cores"],
    )


def verify(frozen, higher):
    if set(frozen) != {"schema", "result", "result_sha256"}:
        raise ValueError("closed top-level schema")
    if frozen["schema"] != cert.SCHEMA:
        raise ValueError("schema")
    result = frozen["result"]
    if digest(result) != frozen["result_sha256"]:
        raise ValueError("result digest")
    if summary(result) != (65, 61, 4, 61, 4, False):
        raise ValueError("frozen frontier summary")
    if len({row["exterior_port_id"] for row in result["ray_rows"]}) != 61:
        raise ValueError("duplicate certified ray")
    if len({row["exterior_port_id"] for row in result["unresolved_ray_rows"]}) != 4:
        raise ValueError("duplicate residual ray")
    if {row["exterior_port_id"] for row in result["ray_rows"]} & {
        row["exterior_port_id"] for row in result["unresolved_ray_rows"]
    }:
        raise ValueError("certified/residual overlap")
    if digest(result["ray_rows"]) != result["ray_rows_sha256"]:
        raise ValueError("ray row digest")
    if digest(result["unresolved_ray_rows"]) != result["unresolved_ray_rows_sha256"]:
        raise ValueError("residual row digest")
    if result["unresolved_reason_histogram"] != {
        "RUNTIME:unresolved competitor event equation: unresolved_discriminant": 4
    }:
        raise ValueError("residual reason ledger")
    if summary(result) != summary(higher["result"]):
        raise ValueError("768-bit summary mismatch")
    frozen_certified = {
        (row["exterior_port_id"], row["projective_end"], row["source_exit_boundary_type"])
        for row in result["ray_rows"]
    }
    higher_certified = {
        (row["exterior_port_id"], row["projective_end"], row["source_exit_boundary_type"])
        for row in higher["result"]["ray_rows"]
    }
    if frozen_certified != higher_certified:
        raise ValueError("768-bit certified identity/type mismatch")
    frozen_residual = {
        (row["exterior_port_id"], tuple(row["branch_key"]), row["projective_end"])
        for row in result["unresolved_ray_rows"]
    }
    higher_residual = {
        (row["exterior_port_id"], tuple(row["branch_key"]), row["projective_end"])
        for row in higher["result"]["unresolved_ray_rows"]
    }
    if frozen_residual != higher_residual:
        raise ValueError("768-bit residual identity mismatch")


def build():
    if sha(HERE / "cm2_round91_rank3_exterior_source_exit_cert.py") != PRODUCER_SHA:
        raise RuntimeError("producer pin")
    frozen = load()
    higher = cert.build(768)
    verify(frozen, higher)
    rejected = 0
    mutations = (
        ("certified_source_exit_ray_count", 65),
        ("remaining_untyped_exterior_ray_count", 0),
        ("complete_rank3_projective_branch_continuation_within_frozen_source_cores", True),
        ("input_exterior_projective_ray_count", 64),
    )
    for field, value in mutations:
        changed = json.loads(json.dumps(frozen))
        changed["result"][field] = value
        changed["result_sha256"] = digest(changed["result"])
        try:
            verify(changed, higher)
        except ValueError:
            rejected += 1
    if rejected != len(mutations):
        raise RuntimeError("hostile mutation rejection")
    result = {
        "status": "PASS",
        "independent_precision_bits": 768,
        "higher_precision_summary": summary(higher["result"]),
        "certified_ray_rows_sha256": frozen["result"]["ray_rows_sha256"],
        "residual_ray_rows_sha256": frozen["result"]["unresolved_ray_rows_sha256"],
        "hostile_semantic_mutations_rejected": "4/4",
        "strict_json_loader": "duplicate and nonfinite rejected",
        "producer_sha256": PRODUCER_SHA,
        "manifest_sha256": sha(MANIFEST),
    }
    return {
        "schema": "cm2.round91.rank3-exterior-source-exit.audit.v1",
        "result": result,
        "result_sha256": digest(result),
    }


def main():
    json.dump(build(), sys.stdout, sort_keys=True, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
