#!/usr/bin/env python3
"""Fail-closed verifier for the Gate-2 Markov-route obstruction snapshot."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path
from typing import Any


SCHEMA = "cm2.gate2.markov-route.v1"
ROOT = Path(__file__).resolve().parent.parent
DEFAULT_MANIFEST = Path(__file__).with_name(
    "cm2-gate2-markov-route-manifest-2026-07-15.json"
)
CERTIFICATE = Path(__file__).with_name(
    "cm2_gate2_markov_route_obstruction_cert.py"
)
REQUIRED_CERT_LINES = (
    "DOEBLIN_MINORISATION_BY_LEBESGUE: IMPOSSIBLE",
    "GKM_CONTINUOUS_COMPACT_MIXTURE_FAMILY: EXACT",
    "NO_DETERMINISTIC_IMAGES(all_mixtures): CERTIFIED",
    "ADAPTIVE_ATOMIC_STATIONARY_MASS=(1/2,1/2): CERTIFIED",
    "STATE_DEPENDENT_GKM_2_8_EXTENSION: FALSE",
    "CDKM_UNIFORM_ERGODICITY_FOR_REVERSE_BRANCH_KERNEL: FALSE",
    "PHYSICAL_STOPPED_PARENT_PPE: NOT CERTIFIED",
)
REQUIRED_PHYSICAL_FIELDS = (
    "common_vertex_full_mass_quotient",
    "uniform_weak_topology_operator_gap",
    "stationary_spatial_frostman",
    "stopped_parent_physical_frostman",
    "normalized_amplitude_moment",
    "same_carrier_endpoint_identity",
    "physical_ppe",
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def integrity_findings(data: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(data, dict):
        return ["manifest is not an object"]
    if data.get("schema") != SCHEMA:
        errors.append(f"schema mismatch: {data.get('schema')!r}")

    rows = data.get("provenance")
    if not isinstance(rows, list) or not rows:
        errors.append("provenance missing")
    else:
        for row in rows:
            if not isinstance(row, dict):
                errors.append("invalid provenance row")
                continue
            relative = row.get("path")
            expected = row.get("sha256")
            path = ROOT / relative if isinstance(relative, str) else None
            if path is None or not path.is_file():
                errors.append(f"missing provenance file: {relative!r}")
                continue
            actual = sha256(path)
            if actual != expected:
                errors.append(
                    f"provenance hash mismatch {relative}: {actual} != {expected}"
                )

    exact = data.get("exact_obstructions")
    if not isinstance(exact, dict):
        errors.append("exact_obstructions missing")
    else:
        for field in (
            "reverse_kernel_finite_time_atomic",
            "stationary_density_non_atomic",
            "cdkm_total_variation_uniform_ergodicity_false",
            "physical_density_doeblin_minorisation_false",
            "adaptive_gkm_extension_false",
        ):
            if exact.get(field) is not True:
                errors.append(f"exact_obstructions.{field} is not true")

    cdkm = data.get("cdkm_hypotheses")
    if not isinstance(cdkm, dict):
        errors.append("cdkm_hypotheses missing")
    elif cdkm.get("uniformly_ergodic_in_total_variation") is not False:
        errors.append("CDKM uniform-ergodicity obstruction not recorded")

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
            errors.append(f"certificate exited {run.returncode}: {run.stderr}")
        for line in REQUIRED_CERT_LINES:
            if line not in run.stdout:
                errors.append(f"certificate output missing: {line}")
    return errors


def completion_findings(data: Any) -> list[str]:
    if not isinstance(data, dict):
        return list(REQUIRED_PHYSICAL_FIELDS)
    completion = data.get("physical_completion")
    if not isinstance(completion, dict):
        return list(REQUIRED_PHYSICAL_FIELDS)
    return [field for field in REQUIRED_PHYSICAL_FIELDS if not completion.get(field)]


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
    missing = completion_findings(data)
    if args.self_test:
        if integrity:
            print("SELF_TEST: FAIL")
            for item in integrity:
                print(f"  {item}")
            return 1
        if set(missing) != set(REQUIRED_PHYSICAL_FIELDS):
            print(f"SELF_TEST: FAIL (unexpected completion set: {missing})")
            return 1
        print("SELF_TEST: PASS (valid obstruction snapshot; incompleteness rejected)")
        return 0

    if integrity:
        print("MARKOV_ROUTE_MANIFEST: INVALID")
        for item in integrity:
            print(f"  {item}")
        return 1
    if missing:
        print("PHYSICAL_GATE2: NOT_CERTIFIED")
        for item in missing:
            print(f"  missing: {item}")
        return 2
    print("PHYSICAL_GATE2: CERTIFIED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
