#!/usr/bin/env python3
"""Fail-closed verifier for the global reflection-schema manifest."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
from pathlib import Path

import cm2_gate45_global_reflection_schema_cert as cert


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "deliverables/cm2-gate45-global-reflection-schema-manifest-2026-07-15.json"


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def verify(data: dict[str, object], *, require_global: bool) -> None:
    for item in data["provenance"]:  # type: ignore[index]
        path = ROOT / item["path"]  # type: ignore[index]
        assert path.is_file()
        assert sha256(path) == item["sha256"]  # type: ignore[index]

    fresh = cert.certify()
    ledger = data["exact_ledger"]  # type: ignore[index]
    for key in (
        "candidate_row_count",
        "two_row_orbit_count",
        "fixed_label_orbit_count",
        "row_involution_digest",
        "affine_conjugacy_digest",
    ):
        assert ledger[key] == fresh[key]  # type: ignore[index]

    certified = data["certified"]  # type: ignore[index]
    assert all(certified.values())
    completion = data["global_completion"]  # type: ignore[index]
    current = {
        "immutable_physical_event_registry": fresh["immutable_physical_event_registry"],
        "eventwise_dq_typing": fresh["eventwise_dq_typing"],
        "global_single_charge_recovery": fresh["global_single_charge_recovery"],
        "four_term_kac_typing": fresh["four_term_kac_typing"],
        "phase_cm2_norm_lifts": fresh["phase_cm2_norm_lifts"],
        "gate4_certified": fresh["gate4_certified"],
        "gate5_certified": fresh["gate5_certified"],
    }
    assert completion == current
    if require_global:
        assert all(completion.values())


def self_test(data: dict[str, object]) -> None:
    verify(data, require_global=False)
    bad = copy.deepcopy(data)
    bad["exact_ledger"]["fixed_label_orbit_count"] = 0  # type: ignore[index]
    try:
        verify(bad, require_global=False)
    except AssertionError:
        pass
    else:  # pragma: no cover
        raise AssertionError("fixed-orbit tamper was accepted")
    print("MANIFEST_VERIFIER_SELF_TEST: PASS")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    data = json.loads(MANIFEST.read_text())
    if args.self_test:
        self_test(data)
        return
    try:
        verify(data, require_global=True)
    except AssertionError:
        verify(data, require_global=False)
        print("GATES_4_5_GLOBAL_COMPLETION: NOT_CERTIFIED")
        raise SystemExit(2)
    print("GATES_4_5_GLOBAL_COMPLETION: CERTIFIED")


if __name__ == "__main__":
    main()
