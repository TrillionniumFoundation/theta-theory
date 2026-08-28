#!/usr/bin/env python3
"""Replay verifier for the complete conservative G:E interval atlas.

One replay rebuilds all 16,580 dyadic leaves with 192-bit Arb, recomputes the
leaf and incidence digests, and checks exact coverage of the rational chart
superset.  It remains fail-closed while multi-candidate collars or global DQ
fields are unresolved.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import runpy
import sys
from fractions import Fraction
from pathlib import Path
from typing import Any


SCHEMA = "cm2.gate3.ge-interval-atlas.v1"
ROOT = Path(__file__).resolve().parent.parent
DELIVERABLES = Path(__file__).resolve().parent
CERTIFICATE = DELIVERABLES / "cm2_gate3_ge_interval_atlas_cert.py"
DEFAULT_MANIFEST = DELIVERABLES / "cm2-gate3-ge-interval-atlas-manifest-2026-07-15.json"
REQUIRED_GLOBAL = (
    "exact_resolution_of_multi_candidate_leaves",
    "physical_normal_forms_for_unresolved_pairs",
    "physical_normal_forms_for_unresolved_triples",
    "remaining_seven_source_cells",
    "global_event_rows",
    "global_dq",
    "global_scalar_matching",
)


def file_digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check_provenance(data: dict[str, Any], errors: list[str]) -> None:
    rows = data.get("provenance")
    if not isinstance(rows, list) or not rows:
        errors.append("provenance missing")
        return
    for index, row in enumerate(rows):
        if not isinstance(row, dict):
            errors.append(f"provenance[{index}] invalid")
            continue
        relative, expected = row.get("path"), row.get("sha256")
        path = ROOT / relative if isinstance(relative, str) else None
        if path is None or not path.is_file():
            errors.append(f"provenance file missing: {relative!r}")
        elif file_digest(path) != expected:
            errors.append(f"provenance hash mismatch: {relative}")


def normalized_counts(summary: dict[str, Any]) -> dict[str, int]:
    return {
        key: summary["classification_counts"].get(key, 0)
        for key in ("unique_first", "tangency_graph", "multi_candidate", "no_future_root")
    }


def normalized_volumes(summary: dict[str, Any]) -> dict[str, str]:
    return {
        key: summary["classification_volumes"].get(key, "0")
        for key in ("unique_first", "tangency_graph", "multi_candidate", "no_future_root")
    }


def compare_manifest_summary(
    data: dict[str, Any], summary: dict[str, Any], errors: list[str]
) -> None:
    coverage = data.get("coverage", {})
    expected_coverage = {
        "domain": summary["domain"],
        "initial_boxes": summary["initial_boxes"],
        "maximum_binary_depth": summary["max_depth"],
        "leaf_count": summary["leaf_count"],
        "coverage_volume": summary["coverage_volume"],
        "full_s_window_leaf_count": summary["full_s_window_leaf_count"],
        "s_split_leaf_count": summary["s_split_leaf_count"],
        "leaf_rows_sha256": summary["leaf_rows_sha256"],
    }
    for field, expected in expected_coverage.items():
        if coverage.get(field) != expected:
            errors.append(f"coverage.{field}: expected {expected!r}, got {coverage.get(field)!r}")

    leaf = data.get("leaf_classification", {})
    if leaf.get("counts") != normalized_counts(summary):
        errors.append("leaf classification counts mismatch")
    if leaf.get("volumes") != normalized_volumes(summary):
        errors.append("leaf classification volumes mismatch")
    if leaf.get("maximum_active_targets_on_one_leaf") != summary["maximum_active_targets"]:
        errors.append("maximum active target count mismatch")
    if leaf.get("depth_counts") != summary["depth_counts"]:
        errors.append("depth counts mismatch")
    if leaf.get("owner_counts") != summary["owner_counts"]:
        errors.append("owner counts mismatch")

    resolved = Fraction(summary["classification_volumes"].get("unique_first", "0")) + Fraction(
        summary["classification_volumes"].get("tangency_graph", "0")
    )
    cover_volume = Fraction(summary["coverage_volume"])
    if Fraction(leaf.get("resolved_volume", "-1")) != resolved:
        errors.append("resolved volume mismatch")
    if Fraction(leaf.get("resolved_volume_fraction_of_cover", "-1")) != resolved / cover_volume:
        errors.append("resolved volume fraction mismatch")

    incidence = data.get("incidence_interface", {})
    pair = incidence.get("pair_rows", {})
    expected_pair = summary["pair_rows"]
    if pair.get("count") != expected_pair["count"]:
        errors.append("pair count mismatch")
    if pair.get("separated_by_interval_atlas") != expected_pair["separated"]:
        errors.append("separated pair count mismatch")
    if pair.get("unresolved_cooccurrence_collar") != expected_pair["unresolved"]:
        errors.append("unresolved pair count mismatch")
    if pair.get("sha256") != expected_pair["sha256"]:
        errors.append("pair digest mismatch")
    triple = incidence.get("triple_rows", {})
    expected_triple = summary["triple_rows"]
    if triple.get("count") != expected_triple["count"]:
        errors.append("triple count mismatch")
    if triple.get("separated_by_interval_atlas") != expected_triple["separated"]:
        errors.append("separated triple count mismatch")
    if triple.get("unresolved_cooccurrence_collar") != expected_triple["unresolved"]:
        errors.append("unresolved triple count mismatch")
    if triple.get("sha256") != expected_triple["sha256"]:
        errors.append("triple digest mismatch")


def replay(data: Any) -> tuple[list[str], dict[str, Any] | None]:
    errors: list[str] = []
    if not isinstance(data, dict):
        return ["top-level manifest is not an object"], None
    if data.get("schema") != SCHEMA:
        errors.append(f"schema mismatch: {data.get('schema')!r}")
    check_provenance(data, errors)
    if str(DELIVERABLES) not in sys.path:
        sys.path.insert(0, str(DELIVERABLES))
    try:
        module = runpy.run_path(str(CERTIFICATE), run_name="cm2_gate3_ge_atlas")
        leaves = module["build_atlas"]()
        summary = module["summarize"](leaves)
    except Exception as exc:
        errors.append(f"Arb atlas replay failed: {exc}")
        return errors, None

    allowed = set(data.get("leaf_classification", {}).get("allowed", []))
    for leaf in leaves:
        if leaf.classification not in allowed:
            errors.append(f"unknown leaf classification: {leaf.classification}")
            break
        if leaf.classification == "unique_first" and (
            leaf.owner_target is None or leaf.active_targets != (leaf.owner_target,)
        ):
            errors.append(f"malformed unique leaf: {leaf.box.path}")
            break
        if leaf.classification == "tangency_graph" and (
            leaf.owner_target is None or len(leaf.tangency_targets) != 1
        ):
            errors.append(f"malformed tangency leaf: {leaf.box.path}")
            break
        if leaf.classification == "multi_candidate" and not leaf.active_targets:
            errors.append(f"empty multi-candidate active set: {leaf.box.path}")
            break
    compare_manifest_summary(data, summary, errors)

    continuation = data.get("parameter_continuation", {})
    if continuation.get("window") != ["-1/400", "1/400"]:
        errors.append("parameter continuation window mismatch")
    if summary["s_split_leaf_count"] != 0:
        errors.append("not every leaf spans the full s-window")
    return errors, summary


def completion_findings(data: dict[str, Any]) -> list[str]:
    registry = data.get("global_completion")
    if not isinstance(registry, dict):
        return ["global_completion"]
    return [field for field in REQUIRED_GLOBAL if not registry.get(field)]


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
    errors, summary = replay(data)
    if errors:
        print("GATE3_GE_ATLAS_INTEGRITY: FAIL")
        for error in errors:
            print(f"  {error}")
        return 1

    missing = completion_findings(data)
    if args.self_test:
        tampered = copy.deepcopy(data)
        tampered["coverage"]["leaf_count"] += 1
        tamper_errors: list[str] = []
        assert summary is not None
        compare_manifest_summary(tampered, summary, tamper_errors)
        if not tamper_errors:
            print("SELF_TEST: FAIL (tampered leaf count accepted)")
            return 1
        if set(missing) != set(REQUIRED_GLOBAL):
            print("SELF_TEST: FAIL (incomplete global snapshot accepted)")
            return 1
        print("SELF_TEST: PASS")
        print("  complete conservative G:E cover replayed")
        print("  leaf-count tamper rejected")
        print("  incomplete exact/global layers rejected")
        return 0

    assert summary is not None
    print("GATE3_GE_CONSERVATIVE_INTERVAL_ATLAS: CERTIFIED")
    print(f"  leaves={summary['leaf_count']}")
    print(f"  unique_first={summary['classification_counts'].get('unique_first', 0)}")
    print(f"  tangency_graph={summary['classification_counts'].get('tangency_graph', 0)}")
    print(f"  multi_candidate={summary['classification_counts'].get('multi_candidate', 0)}")
    print(f"  full_s_window_leaves={summary['full_s_window_leaf_count']}")
    if missing:
        print("GATE3_GE_EXACT_EVENT_PARTITION_AND_GLOBAL_DQ: NOT_CERTIFIED")
        for field in missing:
            print(f"  missing={field}")
        return 2
    print("GATE3_GE_EXACT_EVENT_PARTITION_AND_GLOBAL_DQ: CERTIFIED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
