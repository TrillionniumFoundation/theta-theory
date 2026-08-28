#!/usr/bin/env python3
"""Independent 640-bit verification of the Round99 registered-port audit."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import cm2_round99_rank3_registered_port_candidate_audit as cert
from cm2_round79_tangency_intersection_generator import digest


HERE = Path(__file__).resolve().parent
MANIFEST = HERE / "cm2-round99-rank3-registered-port-candidate-audit-2026-07-22.json"
PRODUCER_SHA256 = "bbacd4407aa026850d9a410b61e841bd6e799e67ba16549e4a478a9fcfb7a26f"


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
        result["audited_registered_port_count"],
        result["historical_locally_physical_port_count"],
        result["corrected_locally_physical_port_count"],
        result["corrected_locally_nonphysical_port_count"],
        result["classification_changed_port_count"],
        tuple(sorted(result["corrected_event_classification_histogram"].items())),
        tuple(sorted(result["classification_transition_histogram"].items())),
        tuple(sorted(result["corrected_earliest_winner_histogram_on_changed_ports"].items())),
        result["minimum_historically_consumed_prefix_count"],
        result["maximum_historically_consumed_prefix_count"],
        result["audit_rows_sha256"],
    )


def verify(frozen, higher):
    if set(frozen) != {"schema", "result", "result_sha256"} or frozen["schema"] != cert.SCHEMA:
        raise ValueError("schema")
    if digest(frozen["result"]) != frozen["result_sha256"]:
        raise ValueError("result digest")
    if digest(frozen["result"]["audit_rows"]) != frozen["result"]["audit_rows_sha256"]:
        raise ValueError("row digest")
    if summary(frozen["result"]) != summary(higher["result"]):
        raise ValueError("higher precision mismatch")
    if summary(frozen["result"])[:5] != (3212, 945, 120, 3092, 825):
        raise ValueError("summary counts")


def build():
    if sha256(HERE / "cm2_round99_rank3_registered_port_candidate_audit.py") != PRODUCER_SHA256:
        raise RuntimeError("producer pin mismatch")
    frozen = json.loads(
        MANIFEST.read_text(), object_pairs_hook=strict_pairs, parse_constant=reject_constant
    )
    higher = cert.build(640, 16)
    verify(frozen, higher)
    rejected = 0
    for field, value in (
        ("corrected_locally_physical_port_count", 121),
        ("classification_changed_port_count", 824),
        ("maximum_historically_consumed_prefix_count", 56),
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
        "schema": "cm2.round99.rank3-registered-port-candidate-audit-verification.v1",
        "result": result,
        "result_sha256": digest(result),
    }


if __name__ == "__main__":
    print(json.dumps(build(), sort_keys=True, indent=2))
