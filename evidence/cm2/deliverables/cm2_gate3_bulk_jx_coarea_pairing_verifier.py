#!/usr/bin/env python3
"""Fail-closed verifier for the refined certified-bulk Jx coarea pairing."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import sys
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent
CERTIFICATE = HERE / "cm2_gate3_bulk_jx_coarea_pairing_cert.py"
DEFAULT_MANIFEST = (
    HERE / "cm2-gate3-bulk-jx-coarea-pairing-manifest-2026-07-15.json"
)
SCHEMA = "cm2.gate3.refined-jx-coarea-pairing.manifest.v2"


def sha256_path(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check_structure(data: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(data, dict):
        return ["manifest is not an object"]
    if data.get("schema") != SCHEMA:
        errors.append("schema mismatch")
    if data.get("certificate_sha256") != sha256_path(CERTIFICATE):
        errors.append("certificate hash mismatch")
    dependencies = data.get("dependencies", {})
    if not isinstance(dependencies, dict) or not dependencies:
        errors.append("dependencies missing")
    else:
        for name, expected in dependencies.items():
            path = HERE / name
            if not path.is_file() or sha256_path(path) != expected:
                errors.append(f"dependency mismatch: {name}")
    result = data.get("result", {})
    for key, expected in {
        "certified_physical_box_count": 11812,
        "exact_Jx_box_pair_count": 5906,
        "exact_Jx_component_label_pair_count": 32,
        "all_box_pairs_equal_area": True,
        "all_box_pairs_opposite_polarity": True,
        "all_positive_coarea_laws_pair_by_Jx_pushforward": True,
        "bulk_physical_scalar_mu_dot_r_from_certified_rows": "0",
    }.items():
        if result.get(key) != expected:
            errors.append(f"result mismatch: {key}")
    limits = result.get("scope_limits", {})
    for key in (
        "all_physical_coarea_laws_including_collars",
        "arbitrary_test_current_cancellation",
        "maximal_global_rows",
        "global_dq",
        "gate3_certified",
        "gate4_certified",
        "gate5_certified",
    ):
        if limits.get(key) is not False:
            errors.append(f"unsupported completion flag: {key}")
    if limits.get("unresolved_collar_fraction") != "5263/196608":
        errors.append("unresolved collar fraction mismatch")
    verdict = data.get("verdict", {})
    if verdict.get("bulk_exact_Jx_coarea_pairing") != "CERTIFIED":
        errors.append("bulk pairing verdict mismatch")
    if verdict.get("bulk_physical_scalar_mu_dot_r") != "CERTIFIED":
        errors.append("bulk scalar verdict mismatch")
    if verdict.get("global_DQ_including_collars") != "NOT_CERTIFIED":
        errors.append("global DQ must fail-close")
    if verdict.get("unconditional_CM2") != "NOT_CERTIFIED":
        errors.append("unconditional CM2 must fail-close")
    return errors


def check_replay(data: dict[str, Any]) -> list[str]:
    if str(HERE) not in sys.path:
        sys.path.insert(0, str(HERE))
    try:
        import cm2_gate3_bulk_jx_coarea_pairing_cert as cert
        actual = cert.certify()
    except Exception as exc:
        return [f"certificate replay failed: {exc}"]
    return [] if data.get("result") == actual else ["certificate replay mismatch"]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("manifest", nargs="?", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--replay", action="store_true")
    parser.add_argument("--integrity-only", action="store_true")
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
        print("GATE3_BULK_JX_COAREA_INTEGRITY: FAIL")
        for error in errors:
            print(f"  {error}")
        return 1
    if args.self_test:
        tampered = copy.deepcopy(data)
        tampered["result"]["exact_Jx_box_pair_count"] -= 1
        if not check_structure(tampered):
            print("SELF_TEST: FAIL (pair-count tamper accepted)")
            return 1
        tampered = copy.deepcopy(data)
        tampered["result"]["scope_limits"]["global_dq"] = True
        if not check_structure(tampered):
            print("SELF_TEST: FAIL (unsupported global DQ accepted)")
            return 1
        print("SELF_TEST: PASS")
        print("  pair-count tamper rejected")
        print("  unsupported global DQ rejected")
        return 0
    print("GATE3_BULK_EXACT_JX_COAREA_PAIRING: CERTIFIED")
    print("GATE45_BULK_PHYSICAL_SCALAR_MU_DOT_R: CERTIFIED")
    if args.integrity_only:
        print("GATE3_BULK_JX_COAREA_INTEGRITY: PASS")
        return 0
    print("GATE3_GLOBAL_DQ_INCLUDING_COLLARS: NOT_CERTIFIED")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
