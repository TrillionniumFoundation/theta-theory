#!/usr/bin/env python3
"""Independent 640-bit verification of the Round100 interior-gap closure."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import cm2_round100_rank3_immutable_interior_gap_closure as cert
from cm2_round79_tangency_intersection_generator import digest


HERE = Path(__file__).resolve().parent
MANIFEST = HERE / "cm2-round100-rank3-immutable-interior-gap-closure-2026-07-22.json"
PRODUCER_SHA256 = "be5c7d9413f03810210eea8b8d2eb37a9256886f0a339cdcd4ddcf1d32c1e224"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def strict_pairs(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("duplicate JSON key")
        result[key] = value
    return result


def reject_constant(value):
    raise ValueError(f"nonfinite JSON constant: {value}")


def summary(result):
    return (
        result["corrected_locally_physical_port_count"],
        result["surviving_oriented_projective_branch_count"],
        result["surviving_registered_physical_arc_count"],
        result["surviving_registered_source_cap_count"],
        result["ignored_withdrawn_historical_pair_count"],
        result["corrected_unregistered_interior_gap_count"],
        result["certified_immutable_candidate_interior_gap_count"],
        result["remaining_unresolved_interior_gap_count"],
        tuple(sorted(result["gap_method_histogram"].items())),
        result["source_cap_rows_sha256"],
        result["branch_rows_sha256"],
        result["gap_rows_sha256"],
    )


def verify(frozen, higher):
    if set(frozen) != {"schema", "result", "result_sha256"} or frozen["schema"] != cert.SCHEMA:
        raise ValueError("schema")
    if digest(frozen["result"]) != frozen["result_sha256"]:
        raise ValueError("result digest")
    for rows, field in (
        ("source_cap_rows", "source_cap_rows_sha256"),
        ("branch_rows", "branch_rows_sha256"),
        ("gap_rows", "gap_rows_sha256"),
    ):
        if digest(frozen["result"][rows]) != frozen["result"][field]:
            raise ValueError(f"{rows} digest")
    if summary(frozen["result"]) != summary(higher["result"]):
        raise ValueError("higher precision mismatch")
    if summary(frozen["result"])[:8] != (120, 12, 52, 16, 428, 56, 56, 0):
        raise ValueError("summary counts")


def build():
    if sha256(HERE / "cm2_round100_rank3_immutable_interior_gap_closure.py") != PRODUCER_SHA256:
        raise RuntimeError("producer pin mismatch")
    frozen = json.loads(
        MANIFEST.read_text(), object_pairs_hook=strict_pairs, parse_constant=reject_constant
    )
    higher = cert.build(640)
    verify(frozen, higher)
    rejected = 0
    for field, value in (
        ("certified_immutable_candidate_interior_gap_count", 55),
        ("remaining_unresolved_interior_gap_count", 1),
        ("surviving_oriented_projective_branch_count", 11),
    ):
        corrupted = json.loads(json.dumps(frozen))
        corrupted["result"][field] = value
        corrupted["result_sha256"] = digest(corrupted["result"])
        try:
            verify(corrupted, higher)
        except ValueError:
            rejected += 1
    result = {
        "status": "PASS",
        "independent_precision_bits": 640,
        "higher_precision_summary_sha256": digest(summary(higher["result"])),
        "hostile_semantic_mutations_rejected": f"{rejected}/3",
        "strict_json_loader": "duplicate and nonfinite values rejected",
        "producer_sha256": PRODUCER_SHA256,
        "manifest_sha256": sha256(MANIFEST),
    }
    return {
        "schema": "cm2.round100.rank3-immutable-interior-gap-verification.v1",
        "result": result,
        "result_sha256": digest(result),
    }


if __name__ == "__main__":
    print(json.dumps(build(), sort_keys=True, indent=2))
