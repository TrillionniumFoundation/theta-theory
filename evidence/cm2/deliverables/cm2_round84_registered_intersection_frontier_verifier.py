#!/usr/bin/env python3
"""Closed-schema and hostile verifier for the Round-84 intersection closure."""
from __future__ import annotations

import copy
import hashlib
import json
import sys
from pathlib import Path
from typing import Any, Iterator

import cm2_round83_common_tangent_frontier_verifier as legacy_verifier
import cm2_round84_registered_intersection_frontier_cert as certificate
import cm2_round84_reverse_common_tangent_closure_generator as reverse_generator


HERE = Path(__file__).resolve().parent
MANIFEST = HERE / "cm2-round84-registered-intersection-frontier-manifest-2026-07-22.json"
LEGACY_MANIFEST = HERE / "cm2-round83-common-tangent-frontier-manifest-2026-07-22.json"


def canonical(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value).encode()).hexdigest()


def strict_text(text: str) -> Any:
    def pairs(rows: list[tuple[str, Any]]) -> dict[str, Any]:
        result = {}
        for key, value in rows:
            if key in result:
                raise ValueError("duplicate key")
            result[key] = value
        return result
    return json.loads(
        text,
        object_pairs_hook=pairs,
        parse_constant=lambda value: (_ for _ in ()).throw(ValueError(value)),
    )


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def scalar_paths(value: Any, prefix: tuple[Any, ...] = ()) -> Iterator[tuple[tuple[Any, ...], Any]]:
    if isinstance(value, dict):
        for key, child in value.items():
            yield from scalar_paths(child, prefix + (key,))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            yield from scalar_paths(child, prefix + (index,))
    else:
        yield prefix, value


def assign_path(value: Any, path: tuple[Any, ...], replacement: Any) -> None:
    cursor = value
    for key in path[:-1]:
        cursor = cursor[key]
    cursor[path[-1]] = replacement


def mutate_scalar(value: Any) -> Any:
    if isinstance(value, bool):
        return not value
    if isinstance(value, int):
        return value + 1
    if isinstance(value, float):
        return value + 1.0
    if isinstance(value, str):
        return value + "__HOSTILE_MUTATION"
    if value is None:
        return "HOSTILE_NULL_REPLACEMENT"
    raise TypeError(type(value))


def validate(document: dict[str, Any]) -> None:
    require(set(document) == {"schema", "pins", "result", "result_sha256"}, "top-level closed schema")
    require(document["schema"] == "cm2.round84.registered-intersection-frontier.v1", "schema")
    require(document["result_sha256"] == digest(document["result"]), "result digest")
    expected = certificate.build()
    require(document == expected, "exact closed-schema certificate mismatch")


def verify_reverse_precision(precision_bits: int) -> None:
    document = reverse_generator.build(precision_bits)
    result = document["result"]
    require(document["result_sha256"] == digest(result), f"reverse digest {precision_bits}")
    require(result["precision_bits"] == precision_bits, f"precision label {precision_bits}")
    require(result["input_hard_component_pair_count"] == 42, f"hard pairs {precision_bits}")
    require(result["post_centered_live_component_pair_count"] == 40, f"live pairs {precision_bits}")
    require(result["input_hard_box_count"] == 614, f"hard boxes {precision_bits}")
    require(result["oriented_common_tangent_target_count"] == 336, f"targets {precision_bits}")
    require(result["unit_normal_identity_overlap_count"] == 336, f"unit identities {precision_bits}")
    require(result["candidate_signed_distance_identity_overlap_count"] == 672, f"distance identities {precision_bits}")
    require(result["target_status_histogram"] == {
        "INVERSE_STRICTLY_SEPARATED": 42,
        "MISS_FIRST": 114,
        "MISS_SECOND": 176,
        "MISS_SOURCE": 4,
    }, f"target partition {precision_bits}")
    require(result["inverse_enclosure_count"] == 42, f"inverse count {precision_bits}")
    require(result["forward_replay_overlap_count"] == 42, f"forward replay {precision_bits}")
    require(result["uniformly_source_core_separated_inverse_count"] == 42, f"core separation {precision_bits}")
    require(result["uniform_core_coordinate_separation_lower"] == "83/4000", f"core gap {precision_bits}")
    require(result["inverse_hard_box_comparison_count"] == 614, f"box comparisons {precision_bits}")
    require(result["uniformly_separated_box_comparison_count"] == 614, f"box separation {precision_bits}")
    require(result["uniform_coordinate_separation_lower"] == "87/4000", f"box gap {precision_bits}")
    require(result["unresolved_target_count"] == 0, f"unresolved targets {precision_bits}")
    require(result["remaining_hard_box_count"] == 0, f"remaining boxes {precision_bits}")


def main() -> int:
    document = strict_text(MANIFEST.read_text())
    validate(document)

    result_scalar_rows = list(scalar_paths(document["result"]))
    result_mutations_rejected = 0
    for path, value in result_scalar_rows:
        mutation = copy.deepcopy(document)
        assign_path(mutation["result"], path, mutate_scalar(value))
        mutation["result_sha256"] = digest(mutation["result"])
        try:
            validate(mutation)
        except Exception:
            result_mutations_rejected += 1

    structural_mutations = []
    mutation = copy.deepcopy(document)
    mutation["unexpected_top_level_claim"] = "CERTIFIED"
    structural_mutations.append(mutation)
    mutation = copy.deepcopy(document)
    mutation["result"]["unexpected_claim"] = "CERTIFIED"
    mutation["result_sha256"] = digest(mutation["result"])
    structural_mutations.append(mutation)
    mutation = copy.deepcopy(document)
    mutation["result"]["strict_state"]["unexpected_gate"] = "CERTIFIED"
    mutation["result_sha256"] = digest(mutation["result"])
    structural_mutations.append(mutation)
    structural_rejected = 0
    for mutation in structural_mutations:
        try:
            validate(mutation)
        except Exception:
            structural_rejected += 1

    strict_cases = ['{"a":1,"a":2}', '{"a":NaN}', '{"a":Infinity}', '{"a":-Infinity}']
    strict_rejected = 0
    for text in strict_cases:
        try:
            strict_text(text)
        except Exception:
            strict_rejected += 1

    for precision_bits in (384, 768):
        verify_reverse_precision(precision_bits)

    reverse_document = strict_text(certificate.REVERSE.read_text())
    inverse_index = next(
        index for index, row in enumerate(reverse_document["result"]["target_rows"])
        if row["status"] == "INVERSE_STRICTLY_SEPARATED"
    )
    reverse_mutations = []
    mutation = copy.deepcopy(reverse_document)
    mutation["result"]["target_rows"][inverse_index]["inverse_enclosures"][0][0] = "[999 +/- 0]"
    mutation["result_sha256"] = digest(mutation["result"])
    reverse_mutations.append(mutation)
    mutation = copy.deepcopy(reverse_document)
    mutation["result"]["target_rows"][inverse_index]["inverse_enclosures"][0][0] = "[999 +/- 0]"
    mutation["result"]["target_rows_sha256"] = digest(mutation["result"]["target_rows"])
    mutation["result_sha256"] = digest(mutation["result"])
    reverse_mutations.append(mutation)
    mutation = copy.deepcopy(reverse_document)
    mutation["result"]["pair_rows"][0]["input_hard_box_count"] += 1
    mutation["result"]["pair_rows_sha256"] = digest(mutation["result"]["pair_rows"])
    mutation["result_sha256"] = digest(mutation["result"])
    reverse_mutations.append(mutation)
    mutation = copy.deepcopy(reverse_document)
    mutation["result"]["unexpected_reverse_claim"] = "CERTIFIED"
    mutation["result_sha256"] = digest(mutation["result"])
    reverse_mutations.append(mutation)
    reverse_mutations_rejected = 0
    for mutation in reverse_mutations:
        try:
            certificate.validate_reverse_document(mutation)
        except Exception:
            reverse_mutations_rejected += 1

    legacy_document = strict_text(LEGACY_MANIFEST.read_text())
    legacy_scalar_rows = list(scalar_paths(legacy_document["result"]))
    legacy_accepted = legacy_rejected = 0
    for path, value in legacy_scalar_rows:
        mutation = copy.deepcopy(legacy_document)
        assign_path(mutation["result"], path, mutate_scalar(value))
        mutation["result_sha256"] = legacy_verifier.digest(mutation["result"])
        try:
            legacy_verifier.validate(mutation, pins=True)
            legacy_accepted += 1
        except Exception:
            legacy_rejected += 1

    require(result_mutations_rejected == len(result_scalar_rows), "Round-84 scalar mutation coverage")
    require(structural_rejected == len(structural_mutations), "Round-84 structural mutation coverage")
    require(strict_rejected == len(strict_cases), "strict JSON coverage")
    require(reverse_mutations_rejected == len(reverse_mutations), "reverse evidence mutation coverage")
    require(len(legacy_scalar_rows) == 60, "legacy scalar path count")
    require(legacy_accepted == 45 and legacy_rejected == 15, "legacy verifier coverage audit")

    audit_result = {
        "manifest_valid": True,
        "exact_closed_schema_validated": True,
        "all_pins_verified": True,
        "round84_result_scalar_mutation_count": len(result_scalar_rows),
        "round84_result_scalar_mutations_rejected": result_mutations_rejected,
        "round84_structural_mutation_count": len(structural_mutations),
        "round84_structural_mutations_rejected": structural_rejected,
        "strict_json_case_count": len(strict_cases),
        "strict_json_rejections": strict_rejected,
        "independent_reverse_recompute_precisions": [384, 768],
        "independent_reverse_recomputations_passed": 2,
        "reverse_evidence_hostile_mutation_count": len(reverse_mutations),
        "reverse_evidence_hostile_mutations_rejected": reverse_mutations_rejected,
        "legacy_round83_result_scalar_mutation_count": len(legacy_scalar_rows),
        "legacy_round83_mutations_rejected": legacy_rejected,
        "legacy_round83_mutations_accepted": legacy_accepted,
        "legacy_round83_closed_schema_coverage": "INCOMPLETE",
    }
    audit = {
        "schema": "cm2.round84.registered-intersection-frontier-audit.v1",
        "result": audit_result,
        "result_sha256": digest(audit_result),
    }
    json.dump(audit, sys.stdout, sort_keys=True, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
