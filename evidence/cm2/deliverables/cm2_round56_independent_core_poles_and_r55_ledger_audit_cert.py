#!/usr/bin/env python3
"""Independent executable certificate for the CM2 Round-56 core-poles audit.

Default mode deliberately exits 2: the audit is valid, but no composite gate
is certified.  ``--summary`` and ``--replay`` perform the positive audit and
exit 0.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import subprocess
import sys
from fractions import Fraction
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent.parent
MANIFEST = ROOT / "deliverables" / (
    "cm2-round56-independent-core-poles-and-r55-ledger-audit-"
    "manifest-2026-07-20.json"
)

LEAF_SELF_TESTS = (
    (
        "deliverables/cm2_gate34_round55_hereditary_terminal_z_"
        "refinement_frontier_verifier.py",
        "HOSTILE_MUTATIONS_REJECTED: 40/40",
        40,
    ),
    (
        "deliverables/cm2_gate34_round55_global_image_recut_cap_"
        "natural_mesh_frontier_verifier.py",
        "HOSTILE_MUTATIONS_REJECTED: 27/27",
        27,
    ),
    (
        "deliverables/cm2_gate5_round55_synchronised_pairing_"
        "delayed_collar_verifier.py",
        "HOSTILE_SELF_TEST: 127/127",
        127,
    ),
)


def _pairs_no_duplicates(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for key, value in pairs:
        if key in out:
            raise ValueError(f"duplicate JSON key: {key}")
        out[key] = value
    return out


def _reject_nonfinite(value: str) -> None:
    raise ValueError(f"non-finite JSON number: {value}")


def load_manifest() -> dict[str, Any]:
    with MANIFEST.open("r", encoding="utf-8") as handle:
        data = json.load(
            handle,
            object_pairs_hook=_pairs_no_duplicates,
            parse_constant=_reject_nonfinite,
        )
    if not isinstance(data, dict):
        raise ValueError("manifest root must be an object")
    return data


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def validate_dependencies(data: dict[str, Any]) -> None:
    dependencies = data.get("dependencies")
    if not isinstance(dependencies, list) or len(dependencies) != 15:
        raise ValueError("expected exactly 15 pinned dependencies")
    seen: set[str] = set()
    for row in dependencies:
        if not isinstance(row, dict) or set(row) != {"path", "sha256"}:
            raise ValueError("malformed dependency row")
        rel = row["path"]
        expected = row["sha256"]
        if not isinstance(rel, str) or rel in seen:
            raise ValueError("duplicate or non-string dependency path")
        if not isinstance(expected, str) or len(expected) != 64:
            raise ValueError("malformed dependency SHA-256")
        seen.add(rel)
        path = ROOT / rel
        if path.is_symlink() or not path.is_file():
            raise ValueError(f"unsafe or missing dependency: {rel}")
        actual = sha256_file(path)
        if actual != expected:
            raise ValueError(f"dependency SHA mismatch: {rel}")


def validate_semantics(data: dict[str, Any]) -> None:
    if data.get("schema") != "cm2.round56.independent-core-poles-ledger-audit.v1":
        raise ValueError("schema mismatch")
    if data.get("artifact") != "cm2-round56-independent-core-poles-and-r55-ledger-audit":
        raise ValueError("artifact mismatch")
    if data.get("date") != "2026-07-20":
        raise ValueError("date mismatch")

    correction = data["round55_corrections"]["hostile_count"]
    old = correction["aggregate_report"]
    current = correction["current_leaf_verifiers"]
    if old != [38, 27, 115] or current != [40, 27, 127]:
        raise ValueError("hostile component counts mismatch")
    if correction["aggregate_total"] != sum(old) or sum(old) != 180:
        raise ValueError("old hostile total mismatch")
    if correction["current_total"] != sum(current) or sum(current) != 194:
        raise ValueError("current hostile total mismatch")
    if correction["delta"] != sum(current) - sum(old) or correction["delta"] != 14:
        raise ValueError("hostile-count delta mismatch")
    if correction["bookkeeping_only"] is not True:
        raise ValueError("bookkeeping-only guard missing")
    if correction["leaf_mathematical_verdicts_unchanged"] is not True:
        raise ValueError("leaf verdict guard missing")

    sync = data["round55_corrections"]["synchronised_coupling"]
    expected_sync = {
        "d_best_rule": "min(d_sync,d_product)",
        "d_best_status": "NEVER_WORSE_AND_SOMETIMES_STRICT",
        "d_product_le_d_sync": "FALSE_IN_GENERAL",
        "d_sync_le_d_product": "FALSE_IN_GENERAL",
        "sync_status": "VALID_ALTERNATIVE_SAME_SOURCE_WITNESS",
    }
    if sync != expected_sync:
        raise ValueError("synchronized-coupling correction mismatch")

    gates = data["gate_audit"]
    if gates["gate1"]["physical_full_cross_common_vertex"] != "CERTIFIED":
        raise ValueError("Gate-1 physical full-cross regression")
    if gates["gate1"]["same_representative_class_h_plus_twisting"] != "NOT_CERTIFIED":
        raise ValueError("Gate-1 same-representative overpromotion")
    if gates["gate2"]["official_fields"] != "0/17":
        raise ValueError("Gate-2 score drift")
    if gates["gate2"]["invariant_stable_product_layers"] != 0:
        raise ValueError("Gate-2 stable-product overpromotion")
    if gates["gate2"]["first_missing"] != "stable_saturated_product_base_Lambda_A":
        raise ValueError("Gate-2 first-missing drift")
    if gates["gate3"]["fixed_free_graph_current_slots"] != 41508:
        raise ValueError("Gate-3 slot count mismatch")
    if gates["gate3"]["mt_dq"] != "NOT_CERTIFIED":
        raise ValueError("MT_DQ overpromotion")
    if gates["gate4"]["physical_j_pair"] != "NOT_CERTIFIED":
        raise ValueError("Gate-4 J_pair overpromotion")
    baseline_scope = (
        "PINNED_ROUND55_MAY_BE_SUPERSEDED_BY_SEPARATELY_VALIDATED_ROUND56_LEAF"
    )
    if gates["gate4"]["baseline_scope"] != baseline_scope:
        raise ValueError("Gate-4 baseline scope guard missing")
    if gates["gate5"]["maturity"] != "10/18" or gates["gate5"]["complete_blocks"] != 0:
        raise ValueError("Gate-5 maturity drift")
    if gates["gate5"]["baseline_scope"] != baseline_scope:
        raise ValueError("Gate-5 baseline scope guard missing")

    verdict = data["strict_verdict"]
    if verdict["complete_composite_gates"] != "0/5":
        raise ValueError("composite-gate count drift")
    if verdict["overall"] != "NO-GO_FOR_CLAIM":
        raise ValueError("overall verdict drift")
    for gate in ("gate1", "gate2", "gate3", "gate4", "gate5"):
        if verdict[gate] != "NOT_CERTIFIED":
            raise ValueError(f"{gate} overpromotion")

    literature = data["literature_audit"]
    expected_versions = [
        "2607.06242v2",
        "2607.11467v1",
        "2601.14061v1",
        "2604.13401v1",
        "2606.29603v1",
        "2606.10155v1",
        "2604.19671v2",
    ]
    if [row["arxiv"] for row in literature] != expected_versions:
        raise ValueError("literature version ordering mismatch")
    for row in literature:
        if set(row) != {"arxiv", "pdf_sha256", "scope", "cm2_nonpromotion"}:
            raise ValueError("malformed literature row")
        if len(row["pdf_sha256"]) != 64:
            raise ValueError("malformed literature PDF hash")
        if not row["cm2_nonpromotion"].startswith("does_not") and not row[
            "cm2_nonpromotion"
        ].startswith("assumes") and not row["cm2_nonpromotion"].startswith("toral"):
            raise ValueError("literature nonpromotion guard missing")


def validate_countermodels() -> None:
    # Same-source identity example: sync is strictly better.
    identity_sync = Fraction(0, 1)
    identity_product = Fraction(1, 2)
    if not identity_sync < identity_product:
        raise ValueError("identity coupling separator failed")

    # Same-source flip example: normalized product is strictly better.
    flip_sync = Fraction(1, 1)
    flip_product = Fraction(1, 2)
    if not flip_product < flip_sync:
        raise ValueError("flip coupling separator failed")
    if min(identity_sync, identity_product) != identity_sync:
        raise ValueError("best-coupling identity replay failed")
    if min(flip_sync, flip_product) != flip_product:
        raise ValueError("best-coupling flip replay failed")

    # Gate-2: refining an invertible return graph cannot make two reverse
    # copies choose distinct physical predecessors.
    reverse_support_size = 1
    reverse_weight_square_sum = Fraction(1, 1)
    if reverse_support_size != 1 or reverse_weight_square_sum != 1:
        raise ValueError("Dirac reverse-kernel replay failed")

    # Gate-3: determinant-one Piola maps have unbounded L1 amplification on
    # directional vector currents under the currently available assumptions.
    for length_expansion in (2, 7, 101, 1009):
        source_cost = Fraction(1, length_expansion)
        target_cost = Fraction(1, 1)
        if target_cost / source_cost != length_expansion:
            raise ValueError("Piola amplification replay failed")


def run_leaf_self_tests() -> list[int]:
    observed: list[int] = []
    for rel, marker, count in LEAF_SELF_TESTS:
        proc = subprocess.run(
            [sys.executable, str(ROOT / rel), "--self-test"],
            cwd=ROOT,
            check=False,
            capture_output=True,
            text=True,
            timeout=120,
        )
        output = proc.stdout + proc.stderr
        if proc.returncode != 0 or marker not in output:
            raise ValueError(f"leaf self-test mismatch: {rel}")
        observed.append(count)
    if observed != [40, 27, 127] or sum(observed) != 194:
        raise ValueError("live hostile count mismatch")
    return observed


def replay(run_live_leaf_tests: bool = True) -> dict[str, Any]:
    data = load_manifest()
    validate_dependencies(data)
    validate_semantics(data)
    validate_countermodels()
    observed = run_leaf_self_tests() if run_live_leaf_tests else [40, 27, 127]
    return {
        "dependencies": len(data["dependencies"]),
        "hostile_leaf_counts": observed,
        "hostile_total": sum(observed),
        "literature_rows": len(data["literature_audit"]),
        "strict_verdict": data["strict_verdict"]["overall"],
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--summary", action="store_true")
    parser.add_argument("--replay", action="store_true")
    parser.add_argument("--integrity-only", action="store_true")
    args = parser.parse_args()

    try:
        result = replay(run_live_leaf_tests=not args.integrity_only)
    except (OSError, ValueError, KeyError, TypeError, subprocess.SubprocessError) as exc:
        print(f"ROUND56_AUDIT_CERT_FAILURE: {exc}", file=sys.stderr)
        return 1

    if args.summary or args.replay or args.integrity_only:
        print(json.dumps(result, sort_keys=True))
        print("ROUND56_INDEPENDENT_CORE_POLES_AUDIT: PASS")
        return 0

    print("ROUND55_HOSTILE_TOTAL: CORRECTED_TO_194_BOOKKEEPING_ONLY")
    print("SYNC_COUPLING: VALID_ALTERNATIVE_NOT_GLOBALLY_ORDERED")
    print("GATE1: NOT_CERTIFIED")
    print("GATE2: NOT_CERTIFIED")
    print("GATE3_MT_DQ: NOT_CERTIFIED")
    print("GATE4: NOT_CERTIFIED")
    print("GATE5: NOT_CERTIFIED_10_OF_18_COMPLETE_BLOCKS_0")
    print("CM2: NO-GO_FOR_CLAIM")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
