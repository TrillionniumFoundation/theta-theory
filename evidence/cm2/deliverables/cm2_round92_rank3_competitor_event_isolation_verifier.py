#!/usr/bin/env python3
"""768-bit audit of the Round92 centered-Taylor exterior-ray closure."""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

from cm2_round79_tangency_intersection_generator import digest
import cm2_round92_rank3_competitor_event_isolation_cert as cert

HERE = Path(__file__).resolve().parent
MANIFEST = HERE / "cm2-round92-rank3-competitor-event-isolation-2026-07-22.json"
PRODUCER_SHA = "90527519cc66c1a5fa3a2c8336f97c29994ed893c4508ad370247fd542ccdd50"


def hook(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("duplicate JSON key")
        result[key] = value
    return result


def bad(value):
    raise ValueError(f"nonfinite JSON number: {value}")


def load():
    return json.loads(MANIFEST.read_text(), object_pairs_hook=hook, parse_constant=bad)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def summary(result):
    return (
        result["input_round91_residual_ray_count"],
        result["strict_discriminant_transition_count"],
        result["no_point_discriminant_sign_transition_count"],
        result["centered_taylor_closed_residual_ray_count"],
        result["combined_round91_round92_source_exit_ray_count"],
        result["remaining_exterior_ray_within_frozen_source_cores_count"],
    )


def closure_signature(result):
    return sorted(
        (
            row["exterior_port_id"],
            tuple(row["branch_key"]),
            row["projective_end"],
            row["centered_chain_strip_count"],
            row["centered_discriminant_repair_count"],
            row["whole_open_ray_status"],
        )
        for row in result["closure_rows"]
    )


def diagnostic_signature(result):
    return sorted(
        (
            row["exterior_port_id"],
            tuple(row["branch_key"]),
            row["projective_end"],
            row["probe_status"],
            row["closest_competitor_candidate_id"],
            row["closest_discriminant_sign"],
        )
        for row in result["diagnostic_rows"]
    )


def verify(frozen, higher):
    if set(frozen) != {"schema", "result", "result_sha256"}:
        raise ValueError("closed top-level schema")
    if frozen["schema"] != cert.SCHEMA:
        raise ValueError("schema")
    result = frozen["result"]
    if digest(result) != frozen["result_sha256"]:
        raise ValueError("result digest")
    if summary(result) != (4, 0, 4, 4, 65, 0):
        raise ValueError("frozen summary")
    if digest(result["closure_rows"]) != result["closure_rows_sha256"]:
        raise ValueError("closure rows digest")
    if digest(result["diagnostic_rows"]) != result["diagnostic_rows_sha256"]:
        raise ValueError("diagnostic rows digest")
    if len({row["exterior_port_id"] for row in result["closure_rows"]}) != 4:
        raise ValueError("closure identity uniqueness")
    if summary(result) != summary(higher["result"]):
        raise ValueError("768-bit summary mismatch")
    if closure_signature(result) != closure_signature(higher["result"]):
        raise ValueError("768-bit closure signature mismatch")
    if diagnostic_signature(result) != diagnostic_signature(higher["result"]):
        raise ValueError("768-bit diagnostic signature mismatch")


def build():
    if sha(HERE / "cm2_round92_rank3_competitor_event_isolation_cert.py") != PRODUCER_SHA:
        raise RuntimeError("producer pin")
    frozen = load()
    higher = cert.build(768)
    verify(frozen, higher)
    rejected = 0
    for field, value in (
        ("centered_taylor_closed_residual_ray_count", 3),
        ("combined_round91_round92_source_exit_ray_count", 64),
        ("remaining_exterior_ray_within_frozen_source_cores_count", 1),
        ("strict_discriminant_transition_count", 4),
    ):
        changed = json.loads(json.dumps(frozen))
        changed["result"][field] = value
        changed["result_sha256"] = digest(changed["result"])
        try:
            verify(changed, higher)
        except ValueError:
            rejected += 1
    if rejected != 4:
        raise RuntimeError("hostile mutation rejection")
    result = {
        "status": "PASS",
        "independent_precision_bits": 768,
        "higher_precision_summary": summary(higher["result"]),
        "higher_precision_closure_signature": closure_signature(higher["result"]),
        "hostile_semantic_mutations_rejected": "4/4",
        "strict_json_loader": "duplicate and nonfinite rejected",
        "producer_sha256": PRODUCER_SHA,
        "manifest_sha256": sha(MANIFEST),
    }
    return {
        "schema": "cm2.round92.rank3-competitor-event-isolation.audit.v1",
        "result": result,
        "result_sha256": digest(result),
    }


def main():
    json.dump(build(), sys.stdout, sort_keys=True, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
