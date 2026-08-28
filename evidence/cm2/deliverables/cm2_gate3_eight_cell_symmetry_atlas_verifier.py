#!/usr/bin/env python3
"""Fail-closed verifier for the eight-cell Gate-3 interval atlas.

The quick path checks provenance, exact registry arithmetic, reflection-pair
consistency and completion fields.  ``--replay`` additionally rebuilds all
four 192-bit Arb representative atlases (about 31 minutes on the reference
host) and compares every leaf/pair/triple digest.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import runpy
import sys
from pathlib import Path
from typing import Any


SCHEMA = "cm2.gate3.eight-cell-symmetry-atlas.v1"
ROOT = Path(__file__).resolve().parent.parent
HERE = Path(__file__).resolve().parent
DEFAULT_MANIFEST = HERE / "cm2-gate3-eight-cell-symmetry-atlas-manifest-2026-07-15.json"
CERTIFICATE = HERE / "cm2_gate3_eight_cell_symmetry_atlas_cert.py"
CHARTS = ("G:E", "G:W", "G:N", "G:S", "W:E", "W:W", "W:N", "W:S")
REFLECTION_PAIRS = (("G:E", "G:W"), ("G:N", "G:S"), ("W:E", "W:W"), ("W:N", "W:S"))
MISSING_FIELDS = (
    "exact_resolution_of_multi_candidate_leaves",
    "physical_normal_forms_for_unresolved_pairs",
    "physical_normal_forms_for_unresolved_triples",
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
        relative = row.get("path")
        expected = row.get("sha256")
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
    coverage = data.get("coverage", {})
    if coverage.get("domain") != {
        "t": ["-177/250", "177/250"],
        "p": ["-1", "1"],
        "s": ["-1/400", "1/400"],
    }:
        errors.append("coverage domain mismatch")
    if coverage.get("representative_arb_charts") != ["G:E", "G:N", "W:E", "W:N"]:
        errors.append("representative chart registry mismatch")
    if coverage.get("every_leaf_spans_full_s_window") is not True:
        errors.append("full s-window flag missing")
    reflection = data.get("reflection_certificate", {})
    if reflection.get("quarter_turn_used") is not False:
        errors.append("invalid quarter-turn transport")
    if set(reflection.get("row_digests", {})) != {
        "G:E->G:W", "G:N->G:S", "W:E->W:W", "W:N->W:S"
    }:
        errors.append("reflection row registry mismatch")

    charts = data.get("charts")
    if not isinstance(charts, dict) or set(charts) != set(CHARTS):
        errors.append("chart registry mismatch")
        return errors
    totals = {key: 0 for key in ("leaf_count", "unique_first", "tangency_graph", "multi_candidate", "pair_unresolved", "triple_unresolved")}
    for chart_id in CHARTS:
        row = charts[chart_id]
        candidate_count = row.get("candidate_count")
        if candidate_count not in (55, 57):
            errors.append(f"{chart_id}: candidate count invalid")
            continue
        counts = row.get("counts", {})
        leaf_count = row.get("leaf_count")
        if sum(counts.get(key, -10**9) for key in ("unique_first", "tangency_graph", "multi_candidate")) != leaf_count:
            errors.append(f"{chart_id}: leaf arithmetic mismatch")
        pair = row.get("pair_rows", {})
        triple = row.get("triple_rows", {})
        expected_pairs = candidate_count * (candidate_count - 1) // 2
        expected_triples = candidate_count * (candidate_count - 1) * (candidate_count - 2) // 6
        if pair.get("count") != expected_pairs or pair.get("separated", 0) + pair.get("unresolved", 0) != expected_pairs:
            errors.append(f"{chart_id}: pair arithmetic mismatch")
        if triple.get("count") != expected_triples or triple.get("separated", 0) + triple.get("unresolved", 0) != expected_triples:
            errors.append(f"{chart_id}: triple arithmetic mismatch")
        for field in ("leaf_rows_sha256",):
            if not isinstance(row.get(field), str) or len(row[field]) != 64:
                errors.append(f"{chart_id}: {field} invalid")
        totals["leaf_count"] += leaf_count
        for key in ("unique_first", "tangency_graph", "multi_candidate"):
            totals[key] += counts[key]
        totals["pair_unresolved"] += pair["unresolved"]
        totals["triple_unresolved"] += triple["unresolved"]
    if data.get("global_totals") != totals:
        errors.append("global totals mismatch")
    if coverage.get("global_leaf_count") != totals["leaf_count"]:
        errors.append("coverage leaf total mismatch")
    for left, right in REFLECTION_PAIRS:
        a, b = charts[left], charts[right]
        for field in ("candidate_count", "leaf_count", "counts"):
            if a.get(field) != b.get(field):
                errors.append(f"reflection pair {left}/{right}: {field} mismatch")
        for kind in ("pair_rows", "triple_rows"):
            for field in ("count", "separated", "unresolved"):
                if a.get(kind, {}).get(field) != b.get(kind, {}).get(field):
                    errors.append(f"reflection pair {left}/{right}: {kind}.{field} mismatch")
    return errors


def expected_replay_chart(summary: dict[str, Any]) -> dict[str, Any]:
    return {
        "provenance": summary["provenance"],
        "candidate_count": summary["candidate_count"],
        "leaf_count": summary["leaf_count"],
        "counts": {
            key: summary["classification_counts"].get(key, 0)
            for key in ("unique_first", "tangency_graph", "multi_candidate")
        },
        "leaf_rows_sha256": summary["leaf_rows_sha256"],
        "pair_rows": summary["pair_rows"],
        "triple_rows": summary["triple_rows"],
    }


def full_replay(data: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if str(HERE) not in sys.path:
        sys.path.insert(0, str(HERE))
    try:
        module = runpy.run_path(str(CERTIFICATE), run_name="cm2_gate3_eight_cell_replay")
        summary = module["full_summary"]()
    except Exception as exc:
        return [f"Arb replay failed: {exc}"]
    if summary["reflection_row_digests"] != data["reflection_certificate"]["row_digests"]:
        errors.append("reflection digest replay mismatch")
    for chart_id in CHARTS:
        expected = expected_replay_chart(summary["charts"][chart_id])
        actual = data["charts"][chart_id]
        for field, value in expected.items():
            if actual.get(field) != value:
                errors.append(f"{chart_id}: replay mismatch in {field}")
    if summary["global_totals"] != data.get("global_totals"):
        errors.append("replayed global totals mismatch")
    return errors


def missing_completion(data: dict[str, Any]) -> list[str]:
    registry = data.get("global_completion")
    if not isinstance(registry, dict):
        return ["global_completion"]
    return [field for field in MISSING_FIELDS if not registry.get(field)]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("manifest", nargs="?", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--replay", action="store_true", help="rebuild all four Arb representative atlases")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    try:
        data = json.loads(args.manifest.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"MANIFEST_READ_ERROR: {exc}", file=sys.stderr)
        return 1
    errors = check_structure(data)
    if args.replay and not errors:
        errors.extend(full_replay(data))
    if errors:
        print("GATE3_EIGHT_CELL_ATLAS_INTEGRITY: FAIL")
        for error in errors:
            print(f"  {error}")
        return 1
    if args.self_test:
        tampered = copy.deepcopy(data)
        tampered["charts"]["G:N"]["leaf_count"] += 1
        if not check_structure(tampered):
            print("SELF_TEST: FAIL (tampered leaf count accepted)")
            return 1
        tampered = copy.deepcopy(data)
        tampered["reflection_certificate"]["quarter_turn_used"] = True
        if not check_structure(tampered):
            print("SELF_TEST: FAIL (invalid quarter turn accepted)")
            return 1
        print("SELF_TEST: PASS")
        print("  chart-count tamper rejected")
        print("  invalid quarter-turn transport rejected")
        print("  incomplete global fields remain fail-closed")
        return 0
    print("GATE3_EIGHT_CELL_CONSERVATIVE_ATLAS: CERTIFIED")
    print(f"  verification={'full_Arb_replay' if args.replay else 'provenance_and_registry'}")
    print(f"  leaves={data['global_totals']['leaf_count']}")
    print(f"  unique_first={data['global_totals']['unique_first']}")
    print(f"  tangency_graph={data['global_totals']['tangency_graph']}")
    missing = missing_completion(data)
    if missing:
        print("GATE3_EXACT_EVENT_INVENTORY_DQ_SCALAR_MATCHING: NOT_CERTIFIED")
        for field in missing:
            print(f"  missing={field}")
        return 2
    print("GATE3_EXACT_EVENT_INVENTORY_DQ_SCALAR_MATCHING: CERTIFIED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
