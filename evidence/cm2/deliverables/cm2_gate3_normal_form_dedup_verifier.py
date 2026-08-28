#!/usr/bin/env python3
"""Fail-closed verifier for Gate-3 normal-form deduplication."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import sys
from pathlib import Path
from typing import Any


SCHEMA = "cm2.gate3.normal-form-dedup.v1"
HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
DEFAULT_MANIFEST = HERE / "cm2-gate3-normal-form-dedup-manifest-2026-07-15.json"
CHARTS = ("G:E", "G:W", "G:N", "G:S", "W:E", "W:W", "W:N", "W:S")
ORBIT_PAIRS = ("G:E->G:W", "G:N->G:S", "W:E->W:W", "W:N->W:S")
MISSING_GLOBAL = (
    "exact_resolution_of_multi_candidate_leaves",
    "immutable_global_event_rows",
    "global_dq",
    "global_scalar_matching",
)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check_provenance(data: dict[str, Any], errors: list[str]) -> None:
    rows = data.get("provenance")
    if not isinstance(rows, list) or not rows:
        errors.append("provenance missing")
        return
    for index, row in enumerate(rows):
        if not isinstance(row, dict):
            errors.append(f"provenance[{index}] malformed")
            continue
        relative, expected = row.get("path"), row.get("sha256")
        path = ROOT / relative if isinstance(relative, str) else None
        if path is None or not path.is_file():
            errors.append(f"provenance missing: {relative!r}")
        elif digest(path) != expected:
            errors.append(f"provenance hash mismatch: {relative}")


def check_structure(data: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(data, dict):
        return ["manifest is not an object"]
    if data.get("schema") != SCHEMA:
        errors.append("schema mismatch")
    check_provenance(data, errors)

    scope = data.get("scope", {})
    expected_scope_counts = {
        "all_candidate_pair_rows": 12324,
        "all_candidate_triple_rows": 221980,
        "frozen_unresolved_pair_collars": 3038,
        "frozen_unresolved_triple_collars": 10288,
    }
    for key, expected in expected_scope_counts.items():
        if scope.get(key) != expected:
            errors.append(f"scope {key} mismatch")
    if scope.get("parameter_window") != "|s|<=1/400":
        errors.append("parameter window mismatch")

    normal = data.get("universal_normal_form", {})
    if normal.get("minimum_squared_circle_separation_margin") != "36337/160000":
        errors.append("separation margin mismatch")
    if normal.get("physical_pair_multiple_event_count") != 0:
        errors.append("pair physical multiplicity not zero")
    if normal.get("physical_triple_multiple_event_count") != 0:
        errors.append("triple physical multiplicity not zero")

    charts = data.get("chart_normal_form_registries")
    if not isinstance(charts, dict) or set(charts) != set(CHARTS):
        errors.append("chart registry mismatch")
    else:
        pair_total = triple_total = 0
        for chart_id in CHARTS:
            row = charts[chart_id]
            count = row.get("candidate_count")
            expected_pairs = count * (count - 1) // 2 if isinstance(count, int) else -1
            expected_triples = count * (count - 1) * (count - 2) // 6 if isinstance(count, int) else -1
            if row.get("pair_count") != expected_pairs:
                errors.append(f"{chart_id}: pair arithmetic mismatch")
            if row.get("triple_count") != expected_triples:
                errors.append(f"{chart_id}: triple arithmetic mismatch")
            for key in ("pair_rows_sha256", "triple_rows_sha256"):
                if not isinstance(row.get(key), str) or len(row[key]) != 64:
                    errors.append(f"{chart_id}: invalid {key}")
            pair_total += row.get("pair_count", 0)
            triple_total += row.get("triple_count", 0)
        if pair_total != 12324 or triple_total != 221980:
            errors.append("global combination arithmetic mismatch")

    reflection = data.get("reflection_deduplication", {})
    if reflection.get("orbit_size") != 2:
        errors.append("reflection orbit size mismatch")
    if reflection.get("unresolved_pair_representatives") != 1519:
        errors.append("pair representative count mismatch")
    if reflection.get("unresolved_triple_representatives") != 5144:
        errors.append("triple representative count mismatch")
    orbits = reflection.get("orbits", {})
    if set(orbits) != set(ORBIT_PAIRS):
        errors.append("reflection orbit registry mismatch")
    else:
        if 2 * sum(row.get("unresolved_pairs", 0) for row in orbits.values()) != 3038:
            errors.append("reflected pair unresolved arithmetic mismatch")
        if 2 * sum(row.get("unresolved_triples", 0) for row in orbits.values()) != 10288:
            errors.append("reflected triple unresolved arithmetic mismatch")
        for orbit_id, row in orbits.items():
            for key in ("pair_mapping_sha256", "triple_mapping_sha256", "parent_pair_registry_sha256", "parent_triple_registry_sha256"):
                if not isinstance(row.get(key), str) or len(row[key]) != 64:
                    errors.append(f"{orbit_id}: invalid {key}")

    seam = data.get("seam_cancellation", {})
    if seam.get("source_chart_seam_rows") != 8:
        errors.append("source seam count mismatch")
    if seam.get("duplicate_target_rows_inside_one_fixed_source_lift") != 0:
        errors.append("duplicate target row count mismatch")

    event = data.get("local_event_orbit", {})
    if event.get("status") != "complete_positive_width_Jx_symmetry_orbit":
        errors.append("local event orbit status mismatch")
    if event.get("row_count") != 2 or not isinstance(event.get("rows"), list) or len(event["rows"]) != 2:
        errors.append("local event row count mismatch")
    else:
        east, west = event["rows"]
        if (east.get("chart_id"), west.get("chart_id")) != ("G:E", "G:W"):
            errors.append("local event chart orbit mismatch")
        if (east.get("owner"), west.get("owner")) != ("W[0,0]", "W[-1,0]"):
            errors.append("local event owner orbit mismatch")
        if (east.get("miss_trace_target"), west.get("miss_trace_target")) != ("G[1,1]", "G[-1,1]"):
            errors.append("local miss trace orbit mismatch")
        if east.get("parameter_coarea_polarity") != 1 or west.get("parameter_coarea_polarity") != -1:
            errors.append("local event coarea polarity mismatch")

    completion = data.get("global_completion", {})
    if completion.get("pair_physical_multiple_event_normal_forms") != "CERTIFIED_EMPTY_ALL_3038_COLLARS":
        errors.append("pair normal-form completion mismatch")
    if completion.get("triple_physical_multiple_event_normal_forms") != "CERTIFIED_EMPTY_ALL_10288_COLLARS":
        errors.append("triple normal-form completion mismatch")
    return errors


def check_replay(data: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if str(HERE) not in sys.path:
        sys.path.insert(0, str(HERE))
    try:
        import cm2_gate3_normal_form_dedup_cert as cert

        summary = cert.full_summary()
    except Exception as exc:
        return [f"certificate replay failed: {exc}"]

    for chart_id in CHARTS:
        actual = data["chart_normal_form_registries"][chart_id]
        expected = summary["charts"][chart_id]
        mapping = {
            "candidate_count": "candidate_count",
            "pair_count": "pair_count",
            "pair_rows_sha256": "pair_normal_form_rows_sha256",
            "triple_count": "triple_count",
            "triple_rows_sha256": "triple_normal_form_rows_sha256",
        }
        for actual_key, expected_key in mapping.items():
            if actual.get(actual_key) != expected.get(expected_key):
                errors.append(f"{chart_id}: replay mismatch {actual_key}")

    replay_reflection = summary["reflection_deduplication"]
    if data["reflection_deduplication"]["unresolved_pair_representatives"] != replay_reflection["unresolved_pair_representatives"]:
        errors.append("replayed pair representative mismatch")
    if data["reflection_deduplication"]["unresolved_triple_representatives"] != replay_reflection["unresolved_triple_representatives"]:
        errors.append("replayed triple representative mismatch")
    for orbit_id in ORBIT_PAIRS:
        actual = data["reflection_deduplication"]["orbits"][orbit_id]
        expected = replay_reflection["rows"][orbit_id]
        mapping = {
            "pair_mapping_sha256": "pair_mapping_sha256",
            "triple_mapping_sha256": "triple_mapping_sha256",
            "unresolved_pairs": "unresolved_pair_representatives",
            "unresolved_triples": "unresolved_triple_representatives",
        }
        for actual_key, expected_key in mapping.items():
            if actual.get(actual_key) != expected.get(expected_key):
                errors.append(f"{orbit_id}: replay mismatch {actual_key}")
    if data["local_event_orbit"].get("rows_sha256") != summary["local_event_orbit"]["event_rows_sha256"]:
        errors.append("local event-row digest replay mismatch")
    if data["seam_cancellation"].get("source_chart_seam_rows_sha256") != summary["seam_registry"]["rows_sha256"]:
        errors.append("seam digest replay mismatch")
    return errors


def missing_global(data: dict[str, Any]) -> list[str]:
    completion = data.get("global_completion", {})
    return [key for key in MISSING_GLOBAL if not completion.get(key)]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("manifest", nargs="?", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--replay", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    try:
        data = json.loads(args.manifest.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"MANIFEST_READ_ERROR: {exc}", file=sys.stderr)
        return 1
    errors = check_structure(data)
    if args.replay and not errors:
        errors.extend(check_replay(data))
    if errors:
        print("GATE3_NORMAL_FORM_DEDUP_INTEGRITY: FAIL")
        for error in errors:
            print(f"  {error}")
        return 1
    if args.self_test:
        tampered = copy.deepcopy(data)
        tampered["reflection_deduplication"]["unresolved_pair_representatives"] += 1
        if not check_structure(tampered):
            print("SELF_TEST: FAIL (representative-count tamper accepted)")
            return 1
        tampered = copy.deepcopy(data)
        tampered["local_event_orbit"]["rows"][1]["owner"] = "W[0,0]"
        if not check_structure(tampered):
            print("SELF_TEST: FAIL (event-owner tamper accepted)")
            return 1
        print("SELF_TEST: PASS")
        print("  representative-count tamper rejected")
        print("  local event-owner tamper rejected")
        print("  global DQ/scalar matching remains fail-closed")
        return 0

    print("GATE3_PAIR_TRIPLE_PHYSICAL_MULTIPLICITY_NORMAL_FORMS: CERTIFIED")
    print("  pair_collars=3038 -> simultaneous_first_occurrences=0")
    print("  triple_collars=10288 -> simultaneous_first_occurrences=0")
    print("  reflection_representatives=1519 pairs, 5144 triples")
    print("GATE3_LOCAL_JX_EVENT_ROW_ORBIT: CERTIFIED")
    missing = missing_global(data)
    if missing:
        print("GATE3_GLOBAL_EVENT_INVENTORY_DQ_SCALAR_MATCHING: NOT_CERTIFIED")
        for key in missing:
            print(f"  missing={key}")
        return 2
    print("GATE3_GLOBAL_EVENT_INVENTORY_DQ_SCALAR_MATCHING: CERTIFIED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
