#!/usr/bin/env python3
"""Replay and fail-closed verifier for the Gate-4/5 reflection pair."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
DEFAULT_MANIFEST = HERE / "cm2-gate45-reflection-pair-manifest-2026-07-15.json"
CERTIFICATE = HERE / "cm2_gate45_reflection_pair_cert.py"
REQUIRED_GLOBAL = (
    "complete_event_registry",
    "all_symmetry_orbits_and_non_symmetric_rows",
    "stopped_parent_recovery_both_orientations",
    "global_single_charge_ledger",
    "global_roof_current_row_cancellation",
    "four_term_kac_typing",
    "phase_cm2_norm_lifts",
)
REQUIRED_OUTPUT = (
    "TWO_ROW_COMMON_COAREA_BY_ISOMETRY: CERTIFIED",
    "LOCAL_REFLECTION_SOURCE_TEST_NORM_ISOMETRY: CERTIFIED",
    "TWO_ROW_LOCAL_ROOF_CURRENT_MASS_CANCELLATION: CERTIFIED",
    "GLOBAL_EVENT_REGISTRY: NOT CERTIFIED",
)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def integrity_findings(data: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(data, dict):
        return ["manifest root is not an object"]
    if data.get("schema") != "cm2.gate45.reflection-pair.v1":
        errors.append("schema mismatch")
    provenance = data.get("provenance")
    if not isinstance(provenance, list):
        errors.append("provenance missing")
    else:
        for item in provenance:
            if not isinstance(item, dict):
                errors.append("malformed provenance item")
                continue
            rel = item.get("path")
            expected = item.get("sha256")
            if not isinstance(rel, str) or not isinstance(expected, str):
                errors.append("malformed provenance fields")
                continue
            path = ROOT / rel
            if not path.is_file():
                errors.append(f"missing provenance file: {rel}")
            elif sha256(path) != expected:
                errors.append(f"provenance hash mismatch: {rel}")
    rows = data.get("rows")
    if not isinstance(rows, list) or len(rows) != 2:
        errors.append("exactly two rows are required")
    else:
        polarities = [row.get("polarity") for row in rows if isinstance(row, dict)]
        coareas = [row.get("coarea") for row in rows if isinstance(row, dict)]
        marks = [row.get("kac_mark") for row in rows if isinstance(row, dict)]
        norms = [row.get("source_test_norm") for row in rows if isinstance(row, dict)]
        if polarities != [1, -1] or sum(polarities) != 0:
            errors.append("row polarity cancellation mismatch")
        if coareas != ["m_orbit", "m_orbit"]:
            errors.append("common coarea mismatch")
        if marks != [[1, -1], [1, -1]]:
            errors.append("Kac mark mismatch")
        if norms != ["K_orbit", "K_orbit"]:
            errors.append("reflection source/test norm mismatch")
    try:
        run = subprocess.run(
            [sys.executable, str(CERTIFICATE)],
            check=False,
            capture_output=True,
            text=True,
            timeout=30,
        )
    except (OSError, subprocess.SubprocessError) as exc:
        errors.append(f"certificate replay failed: {exc}")
    else:
        if run.returncode != 0:
            errors.append(f"certificate exit {run.returncode}: {run.stderr}")
        for line in REQUIRED_OUTPUT:
            if line not in run.stdout:
                errors.append(f"certificate output missing: {line}")
    return errors


def completion_findings(data: Any) -> list[str]:
    if not isinstance(data, dict):
        return list(REQUIRED_GLOBAL)
    completion = data.get("global_completion")
    if not isinstance(completion, dict):
        return list(REQUIRED_GLOBAL)
    return [field for field in REQUIRED_GLOBAL if not completion.get(field)]


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
    errors = integrity_findings(data)
    missing = completion_findings(data)
    if args.self_test:
        if errors:
            print("SELF_TEST: FAIL")
            for error in errors:
                print(f"  {error}")
            return 1
        if set(missing) != set(REQUIRED_GLOBAL):
            print(f"SELF_TEST: FAIL unexpected completion set: {missing}")
            return 1
        print("SELF_TEST: PASS")
        print("  two-row symmetry ledger replayed")
        print("  incomplete global layers rejected")
        return 0
    if errors:
        print("GATE45_REFLECTION_PAIR_INTEGRITY: FAIL")
        for error in errors:
            print(f"  {error}")
        return 1
    print("GATE45_REFLECTION_PAIR_LOCAL_LAYER: CERTIFIED")
    if missing:
        print("GATE45_GLOBAL_COMPLETION: NOT_CERTIFIED")
        for field in missing:
            print(f"  missing={field}")
        return 2
    print("GATE45_GLOBAL_COMPLETION: CERTIFIED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
