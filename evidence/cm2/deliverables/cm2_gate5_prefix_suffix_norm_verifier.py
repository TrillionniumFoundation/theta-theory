#!/usr/bin/env python3
"""Replay and fail-closed verifier for the Gate-5 norm/phase frontier."""

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
DEFAULT_MANIFEST = HERE / "cm2-gate5-prefix-suffix-norm-manifest-2026-07-15.json"
CERTIFICATE = HERE / "cm2_gate5_prefix_suffix_norm_cert.py"

REQUIRED_CERTIFIED_OUTPUT = (
    "STANDARD_N_RETURN_HEIGHT_BOUND=9: REPLAYED",
    "FINITE_BOREL_PREFIX_SUFFIX_FORMULAS: CERTIFIED",
    "HEIGHT_ONLY_REGULAR_DENSITY_NORM_BOUND: FALSE",
    "HEIGHT_ONLY_STANDARD_FAMILY_FLUX_NORM_BOUND: FALSE",
    "HEIGHT_ONLY_PHYSICAL_C1_TEST_PULLBACK_BOUND: FALSE",
    "HEIGHT_ONLY_PHASE_APERIODICITY: FALSE",
    "GATE_5: NOT CERTIFIED",
)

REQUIRED_PHYSICAL = (
    "immutable_complete_return_word_registry",
    "all_homogeneity_subbranches_registered",
    "regular_density_prefix_suffix_bound",
    "inverse_jacobian_and_distortion_sum",
    "standard_family_cut_growth_bound",
    "flux_face_transversality_and_atlas_bound",
    "physical_test_dynamic_holder_c1_pullback_bound",
    "standard_family_cm2_norm_intertwiner",
    "flux_face_cm2_norm_intertwiner",
    "physical_test_norm_intertwiner",
    "actual_weighted_phase_graph",
    "actual_phase_cycle_gcd_one",
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
    if data.get("schema") != "cm2.gate5.prefix-suffix-norm.v1":
        errors.append("schema mismatch")

    provenance = data.get("provenance")
    if not isinstance(provenance, list) or not provenance:
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

    finite = data.get("finite_measurable_layer")
    expected_finite = {
        "uniform_return_depth_bound": 9,
        "finite_borel_return_word_universe": True,
        "finite_prefix_suffix_sums": True,
        "exact_endpoint_source_test_adjoint_pairing": True,
        "exact_normalized_kac_tower_pairing": True,
        "exact_current_prefix_suffix_pairing": True,
    }
    if not isinstance(finite, dict):
        errors.append("finite measurable layer missing")
    else:
        for key, expected in expected_finite.items():
            if finite.get(key) != expected:
                errors.append(f"finite measurable field mismatch: {key}")

    local = data.get("local_physical_layer")
    if not isinstance(local, dict):
        errors.append("local physical layer missing")
    else:
        if local.get("grouped_incidence_positive_width") is not True:
            errors.append("grouped incidence provenance not recorded")
        if local.get("reflection_pair_source_test_isometry") is not True:
            errors.append("reflection isometry provenance not recorded")
        if local.get("covers_every_return_word_and_homogeneity_subbranch") is not False:
            errors.append("local orbit must not be promoted to global coverage")

    obstructions = data.get("logical_obstructions")
    if not isinstance(obstructions, dict):
        errors.append("logical obstruction layer missing")
    else:
        for field in (
            "height_implies_regular_density_norm_bound",
            "height_implies_standard_family_flux_norm_bound",
            "height_implies_physical_c1_test_pullback_bound",
            "height_implies_phase_aperiodicity",
        ):
            if obstructions.get(field) is not False:
                errors.append(f"invalid height-only implication: {field}")
        for field in (
            "quadratic_height_one_countermodel_certified",
            "finite_cut_growth_countermodel_certified",
            "period_two_phase_countermodel_certified",
        ):
            if obstructions.get(field) is not True:
                errors.append(f"missing countermodel: {field}")

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
        for line in REQUIRED_CERTIFIED_OUTPUT:
            if line not in run.stdout:
                errors.append(f"certificate output missing: {line}")
    return errors


def completion_findings(data: Any) -> list[str]:
    if not isinstance(data, dict):
        return list(REQUIRED_PHYSICAL)
    completion = data.get("physical_quantitative_completion")
    if not isinstance(completion, dict):
        return list(REQUIRED_PHYSICAL)
    return [field for field in REQUIRED_PHYSICAL if completion.get(field) is not True]


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
        if set(missing) != set(REQUIRED_PHYSICAL):
            print(f"SELF_TEST: FAIL unexpected completion set: {missing}")
            return 1
        print("SELF_TEST: PASS")
        print("  finite prefix/suffix and Kac algebra replayed")
        print("  height-only norm and phase promotions rejected")
        print("  incomplete physical branch ledger rejected")
        return 0

    if errors:
        print("GATE5_PREFIX_SUFFIX_NORM_INTEGRITY: FAIL")
        for error in errors:
            print(f"  {error}")
        return 1
    print("GATE5_FINITE_PREFIX_SUFFIX_ALGEBRA: CERTIFIED")
    if missing:
        print("GATE5_GLOBAL_NORM_PHASE_TRANSFER: NOT_CERTIFIED")
        for field in missing:
            print(f"  missing={field}")
        return 2
    print("GATE5_GLOBAL_NORM_PHASE_TRANSFER: CERTIFIED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
