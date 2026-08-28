#!/usr/bin/env python3
"""Fail-closed audit for the Gate-2 stationary-to-stopped bridge.

The mathematical bridge is unconditional under its displayed inputs.  This
checker verifies the exponent algebra and refuses to promote the current pilot
unless every physical input is explicitly certified on one model identifier.
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path


HERE = Path(__file__).resolve().parent
DEFAULT_MANIFEST = HERE / "cm2_gate2_stationary_to_stopped_manifest.json"


def exponent_identity(alpha: float, theta: float, tau: float, n: int) -> bool:
    delta = tau ** (n / (alpha + theta))
    left = delta**alpha
    right = tau**n * delta ** (-theta)
    target = tau ** (alpha * n / (alpha + theta))
    scale = max(1.0, abs(left), abs(right), abs(target))
    return max(abs(left - target), abs(right - target)) <= 2e-13 * scale


def audit(data: dict) -> tuple[list[str], dict]:
    failures: list[str] = []
    if data.get("schema_version") != 1:
        failures.append("unsupported schema_version")
    if not data.get("model_id"):
        failures.append("missing model_id")

    bridge = data.get("bridge_theorem", {})
    if bridge.get("stationary_to_stopped_formula_proved") is not True:
        failures.append("bridge theorem is not recorded as proved")
    if bridge.get("normalized_amplitude_holder_bridge_proved") is not True:
        failures.append("normalized-amplitude Holder bridge is missing")

    benchmark = data.get("artificial_iid_benchmark", {})
    benchmark_ok = (
        benchmark.get("two_map_sip_proximal_certificate") is True
        and benchmark.get("gkm_finite_depth_theorem_applicable") is True
    )
    if not benchmark_ok:
        failures.append("artificial iid GKM benchmark is not certified")

    # Exercise the balancing identity away from one hand-picked tuple.
    algebra_ok = all(
        exponent_identity(alpha, theta, tau, n)
        for alpha in (0.11, 0.37, 0.83)
        for theta in (0.19, 0.5, 1.0)
        for tau in (0.23, 0.71, 0.97)
        for n in (1, 7, 31, 127)
    )
    if not algebra_ok:
        failures.append("stationary-to-stopped exponent identity failed")

    physical = data.get("physical_inputs", {})
    required = (
        "full_mass_physical_future_kernel",
        "pointwise_holder_mixing_same_kernel",
        "stationary_spatial_frostman_same_kernel",
        "arbitrary_stopped_parent_restart",
        "same_carrier_endpoint_projective_identity",
        "parentwise_normalized_amplitude_moment",
    )
    for field in required:
        if physical.get(field) is not True:
            failures.append(f"physical input missing: {field}")

    # A sample prescribed-depth calculation is reported only as an arithmetic
    # sanity check; it is not a pilot constant.
    alpha, theta, tau, c_buf, c_cem = 0.37, 0.5, 0.71, 3.0, 0.2
    theta_raw = min(
        alpha,
        c_buf * abs(math.log(tau)) * alpha / (alpha + theta),
        c_buf * c_cem,
    )
    summary = {
        "model_id": data.get("model_id"),
        "bridge_algebra_self_test": algebra_ok,
        "artificial_iid_gkm_benchmark": benchmark_ok,
        "sample_theta_raw": theta_raw,
        "gate2_physical_certified": not failures,
        "failure_count": len(failures),
    }
    return failures, summary


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("manifest", nargs="?", type=Path, default=DEFAULT_MANIFEST)
    args = parser.parse_args()
    data = json.loads(args.manifest.read_text(encoding="utf-8"))
    failures, summary = audit(data)
    print(json.dumps(summary, indent=2, sort_keys=True))
    if failures:
        print("GATE2_PHYSICAL: NOT_CERTIFIED")
        for failure in failures:
            print(f"- {failure}")
        return 2
    print("GATE2_PHYSICAL: CERTIFIED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
