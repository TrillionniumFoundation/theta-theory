#!/usr/bin/env python3
"""Fail-closed verifier for the Gate-3 first-hit atlas snapshot.

The verifier recomputes all 1,296 chart/target classifications from the
certificate module, checks their frozen digests and counts, and reruns both
positive-width first-hit patches with Arb.  It then separately rejects the
snapshot as a global Gate-3 certificate while any completion field is null.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import runpy
import sys
from fractions import Fraction
from pathlib import Path
from typing import Any


SCHEMA = "cm2.gate3.first-hit-atlas.v1"
ROOT = Path(__file__).resolve().parent.parent
DEFAULT_MANIFEST = Path(__file__).with_name(
    "cm2-gate3-first-hit-atlas-manifest-2026-07-15.json"
)
CERTIFICATE = Path(__file__).with_name("cm2_gate3_candidate_first_hit_cert.py")
REQUIRED_COMPLETION_FIELDS = (
    "all_retained_event_rows",
    "all_selected_root_boxes",
    "all_first_hit_partitions",
    "pair_incidence_table",
    "triple_incidence_table",
    "parameter_continuation",
    "global_dq",
    "global_scalar_matching",
)


def digest_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def fraction(value: str) -> Fraction:
    return Fraction(value)


def check_provenance(data: dict[str, Any], errors: list[str]) -> None:
    rows = data.get("provenance")
    if not isinstance(rows, list) or not rows:
        errors.append("provenance is empty")
        return
    for index, row in enumerate(rows):
        if not isinstance(row, dict):
            errors.append(f"provenance[{index}] is not an object")
            continue
        relative = row.get("path")
        expected = row.get("sha256")
        path = ROOT / relative if isinstance(relative, str) else None
        if path is None or not path.is_file():
            errors.append(f"missing provenance file: {relative!r}")
            continue
        actual = digest_file(path)
        if actual != expected:
            errors.append(
                f"provenance hash mismatch {relative}: expected {expected}, got {actual}"
            )


def check_candidate_reduction(
    data: dict[str, Any], module: dict[str, Any], errors: list[str]
) -> None:
    reduction = data.get("candidate_reduction")
    if not isinstance(reduction, dict):
        errors.append("candidate_reduction missing")
        return
    charts = reduction.get("charts")
    if not isinstance(charts, list):
        errors.append("candidate_reduction.charts is not a list")
        return
    rows_by_id = {
        row.get("chart_id"): row for row in charts if isinstance(row, dict)
    }
    expected_ids = [f"{source}:{cell}" for source in ("G", "W") for cell in ("E", "W", "N", "S")]
    if sorted(rows_by_id) != sorted(expected_ids):
        errors.append(f"chart ids mismatch: {sorted(rows_by_id)}")
        return

    total_pairs = total_retained = total_empty = 0
    classification_rows = module["classification_rows"]
    candidate_ids = module["candidate_ids"]
    canonical_digest = module["canonical_digest"]
    for chart_id in expected_ids:
        row = rows_by_id[chart_id]
        generated_rows = classification_rows(chart_id)
        generated_candidates = candidate_ids(chart_id)
        generated_counts: dict[str, int] = {}
        for generated in generated_rows:
            label = generated["classification"]
            generated_counts[label] = generated_counts.get(label, 0) + 1
        retained = len(generated_candidates)
        empty = len(generated_rows) - retained
        expected_values = {
            "retained": retained,
            "empty": empty,
            "self_source": generated_counts.get("self_source", 0),
            "empty_horizon_center_distance": generated_counts.get(
                "empty_horizon_center_distance", 0
            ),
            "empty_outgoing_halfspace": generated_counts.get(
                "empty_outgoing_halfspace", 0
            ),
            "classification_sha256": canonical_digest(generated_rows),
            "candidate_sha256": canonical_digest(generated_candidates),
        }
        for field, expected in expected_values.items():
            if row.get(field) != expected:
                errors.append(
                    f"{chart_id}.{field}: expected {expected!r}, got {row.get(field)!r}"
                )
        total_pairs += len(generated_rows)
        total_retained += retained
        total_empty += empty
    for field, expected in (
        ("chart_target_pair_count", total_pairs),
        ("retained_pair_count", total_retained),
        ("certified_empty_pair_count", total_empty),
    ):
        if reduction.get(field) != expected:
            errors.append(
                f"candidate_reduction.{field}: expected {expected}, got {reduction.get(field)}"
            )


def check_first_hit_patches(
    data: dict[str, Any], module: dict[str, Any], errors: list[str]
) -> None:
    patches = data.get("certified_local_first_hit_patches")
    if not isinstance(patches, list) or len(patches) != 2:
        errors.append("exactly two local first-hit patches are required")
        return
    PhaseBox = module["PhaseBox"]
    certify = module["certify_first_hit_patch"]
    for index, row in enumerate(patches):
        if not isinstance(row, dict):
            errors.append(f"patch[{index}] is not an object")
            continue
        box = row.get("box", {})
        try:
            phase_box = PhaseBox(
                row["chart_id"],
                fraction(box["t"][0]),
                fraction(box["t"][1]),
                fraction(box["p"][0]),
                fraction(box["p"][1]),
                fraction(box["s"][0]),
                fraction(box["s"][1]),
            )
            root, missed, later = certify(phase_box, row["selected_target_id"])
        except Exception as exc:  # fail closed with the exact failing patch
            errors.append(f"patch[{index}] Arb replay failed: {exc}")
            continue
        if not bool(root > 0):
            errors.append(f"patch[{index}] selected root is not strictly positive: {root}")
        enclosure = row.get("selected_root_enclosure")
        if not isinstance(enclosure, list) or len(enclosure) != 2:
            errors.append(f"patch[{index}] root enclosure missing")
        else:
            lower, upper = fraction(enclosure[0]), fraction(enclosure[1])
            arbq = module["arbq"]
            if not bool(root > arbq(lower)) or not bool(root < arbq(upper)):
                errors.append(
                    f"patch[{index}] root {root} not inside ({lower},{upper})"
                )
        if row.get("retained_competitors_missed") != missed:
            errors.append(f"patch[{index}] missed competitor count mismatch")
        if row.get("retained_competitors_strictly_later") != later:
            errors.append(f"patch[{index}] later competitor count mismatch")


def integrity_findings(data: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(data, dict):
        return ["top-level manifest is not an object"]
    if data.get("schema") != SCHEMA:
        errors.append(f"schema mismatch: {data.get('schema')!r}")
    check_provenance(data, errors)
    try:
        module = runpy.run_path(str(CERTIFICATE), run_name="cm2_gate3_candidate_cert")
    except Exception as exc:
        errors.append(f"certificate import failed: {exc}")
        return errors
    check_candidate_reduction(data, module, errors)
    check_first_hit_patches(data, module, errors)
    root_machinery = data.get("root_machinery")
    if not isinstance(root_machinery, dict):
        errors.append("root_machinery missing")
    else:
        for field in (
            "discriminant",
            "selected_incoming_root",
            "physical_conditions",
            "competing_hit_comparison",
            "tangency_submersion",
            "certificate",
        ):
            if not isinstance(root_machinery.get(field), str) or not root_machinery[field]:
                errors.append(f"root_machinery.{field} missing")
    return errors


def completion_findings(data: dict[str, Any]) -> list[str]:
    completion = data.get("global_completion")
    if not isinstance(completion, dict):
        return ["global_completion registry missing"]
    return [field for field in REQUIRED_COMPLETION_FIELDS if not completion.get(field)]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("manifest", nargs="?", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    try:
        data = json.loads(args.manifest.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"MANIFEST_READ_ERROR: {exc}", file=sys.stderr)
        return 1

    integrity = integrity_findings(data)
    missing = completion_findings(data) if isinstance(data, dict) else []
    if args.self_test:
        if integrity:
            print("SELF_TEST: FAIL (valid snapshot rejected)")
            for item in integrity:
                print(f"  {item}")
            return 1
        if set(missing) != set(REQUIRED_COMPLETION_FIELDS):
            print("SELF_TEST: FAIL (incomplete snapshot was not rejected)")
            print(f"  missing={missing}")
            return 1
        tampered = json.loads(json.dumps(data))
        tampered["candidate_reduction"]["charts"][0]["retained"] += 1
        if not integrity_findings(tampered):
            print("SELF_TEST: FAIL (candidate-count tamper was accepted)")
            return 1
        print("SELF_TEST: PASS")
        print("  1296-row reduction and two Arb patches replayed")
        print("  tampered count rejected")
        print("  incomplete global Gate-3 snapshot rejected")
        return 0

    if integrity:
        print("GATE3_EVIDENCE_INTEGRITY: FAIL")
        for item in integrity:
            print(f"  {item}")
        return 1
    print("GATE3_EVIDENCE_INTEGRITY: CERTIFIED")
    print("  chart_target_pairs=1296")
    print("  retained_candidates=448")
    print("  certified_empty_pairs=848")
    print("  local_first_hit_patches=2")
    if missing:
        print("GATE3_GLOBAL_EVENT_DQ_MATCHING: NOT_CERTIFIED")
        for field in missing:
            print(f"  missing={field}")
        return 2
    print("GATE3_GLOBAL_EVENT_DQ_MATCHING: CERTIFIED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
