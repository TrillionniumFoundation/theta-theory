#!/usr/bin/env python3
"""Fail-closed verifier for the Gate-2 weak-metric assault manifest."""

from __future__ import annotations

import argparse
from copy import deepcopy
from fractions import Fraction
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
DEFAULT_MANIFEST = HERE / "cm2-gate2-wasserstein-energy-manifest-2026-07-15.json"


PROVED_FIELDS = (
    "wasserstein_to_stopped_bridge",
    "dyadic_full_mass_w1_without_tv",
    "uniform_pair_energy_drift_theorem",
    "adaptive_two_map_pilot_energy_certificate",
    "scaled_holder_normalized_amplitude_lemma",
)

PHYSICAL_FIELDS = (
    "actual_one_state_full_mass_quotient",
    "actual_reverse_branch_weight_registry",
    "common_vertex_transported_projective_chart",
    "full_countable_pair_energy_drift",
    "joint_pair_energy_tail_moment",
    "actual_stopped_parent_restart",
    "same_carrier_endpoint_projective_identity",
    "exhaustive_amplitude_registry",
    "parentwise_normalized_amplitude_moment",
)


def audit(data: dict) -> tuple[list[str], dict]:
    failures: list[str] = []
    if data.get("schema_version") != 1:
        failures.append("unsupported schema_version")
    if not data.get("model_id"):
        failures.append("missing model_id")

    proved = data.get("proved_layers", {})
    for field in PROVED_FIELDS:
        if proved.get(field) is not True:
            failures.append(f"positive layer missing: {field}")
    if proved.get("uses_tv_doeblin") is not False:
        failures.append("TV-Doeblin shortcut must remain disabled")
    if proved.get("uses_iid_gkm_markovization") is not False:
        failures.append("iid GKM Markovization must remain disabled")

    constants = data.get("pilot_constants", {})
    arithmetic_ok = (
        constants.get("weight_floor") == "1/5"
        and constants.get("colipschitz_floor") == "1/169"
        and constants.get("energy_alpha") == "1/20"
        and constants.get("same_map_pair_coefficient") == "17/25"
        and constants.get("raw_interval_exponent") == "1/40"
        and 169 * 17**20 < 25**20
        and Fraction(17, 25) == Fraction(1, 5) ** 2 + Fraction(4, 5) ** 2
    )
    if not arithmetic_ok:
        failures.append("pilot energy arithmetic mismatch")

    physical = data.get("physical_inputs", {})
    for field in PHYSICAL_FIELDS:
        if physical.get(field) is not True:
            failures.append(f"physical input missing: {field}")

    summary = {
        "model_id": data.get("model_id"),
        "positive_bridge_layers": all(proved.get(field) is True for field in PROVED_FIELDS),
        "pilot_energy_arithmetic": arithmetic_ok,
        "physical_gate2_certified": not failures,
        "failure_count": len(failures),
    }
    return failures, summary


def self_test(data: dict) -> None:
    promoted = deepcopy(data)
    promoted["physical_inputs"] = {field: True for field in PHYSICAL_FIELDS}
    failures, _ = audit(promoted)
    assert not failures

    tampered = deepcopy(promoted)
    tampered["physical_inputs"]["full_countable_pair_energy_drift"] = False
    failures, _ = audit(tampered)
    assert any("full_countable_pair_energy_drift" in failure for failure in failures)

    tampered = deepcopy(promoted)
    tampered["proved_layers"]["uses_tv_doeblin"] = True
    failures, _ = audit(tampered)
    assert any("TV-Doeblin" in failure for failure in failures)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("manifest", nargs="?", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()

    data = json.loads(args.manifest.read_text(encoding="utf-8"))
    if args.self_test:
        self_test(data)
        print("MANIFEST_VERIFIER_SELF_TEST: PASS")
        return 0

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
