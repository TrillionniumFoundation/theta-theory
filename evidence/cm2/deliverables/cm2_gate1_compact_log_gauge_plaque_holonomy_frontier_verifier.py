#!/usr/bin/env python3
"""Fail-closed verifier for the compact QNL logarithmic gauge frontier."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import sys
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent
DEFAULT_MANIFEST = (
    HERE / "cm2-gate1-compact-log-gauge-plaque-holonomy-frontier-manifest-2026-07-16.json"
)
CERTIFICATE = HERE / "cm2_gate1_compact_log_gauge_plaque_holonomy_frontier_cert.py"
REPORT = HERE / "cm2-gate1-compact-log-gauge-plaque-holonomy-assault-2026-07-16.md"
SCHEMA = "cm2.gate1.compact-log-gauge-plaque-holonomy-frontier.manifest.v1"
RESULT_SCHEMA = "cm2.gate1.compact-log-gauge-plaque-holonomy-frontier.v1"
INTERNAL_DIGEST = "4d2780a1ae29a170403576efe8890236199656c33848c7d2736d86e3e5c95251"


def sha256_path(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def exact(
    errors: list[str], section: dict[str, Any], expected: dict[str, Any], label: str
) -> None:
    for key, value in expected.items():
        if section.get(key) != value:
            errors.append(f"{label} mismatch: {key}")


def check_structure(data: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(data, dict):
        return ["manifest is not an object"]
    if data.get("schema") != SCHEMA:
        errors.append("manifest schema mismatch")
    if data.get("certificate_sha256") != sha256_path(CERTIFICATE):
        errors.append("certificate hash mismatch")
    if data.get("verifier_sha256") != sha256_path(Path(__file__)):
        errors.append("verifier hash mismatch")
    if data.get("report_sha256") != sha256_path(REPORT):
        errors.append("report hash mismatch")

    dependencies = data.get("dependencies")
    if not isinstance(dependencies, dict) or len(dependencies) != 2:
        errors.append("dependency ledger mismatch")
    else:
        for name, expected_hash in dependencies.items():
            path = HERE / name
            if not path.is_file():
                errors.append(f"dependency missing: {name}")
            elif sha256_path(path) != expected_hash:
                errors.append(f"dependency hash mismatch: {name}")

    result = data.get("result")
    if not isinstance(result, dict):
        return errors + ["result missing"]
    if result.get("schema") != RESULT_SCHEMA:
        errors.append("result schema mismatch")
    if result.get("internal_digest") != INTERNAL_DIGEST:
        errors.append("internal digest mismatch")

    extension = result.get("compact_supported_section_gauge", {})
    exact(errors, extension, {
        "same_coefficient": "k=-325/(144 log(mu))",
        "regularity": "C^1 and C^{1,alpha} for every 0<alpha<1",
        "determinant": "1 exactly",
        "global_inverse_on_section": True,
        "no_chart_boundary_seam": True,
        "equals_previous_local_gauge_on_core": True,
        "compact_support_changes_only_finite_orbit_prefixes": True,
    }, "compact extension")

    plaques = result.get("local_qnl_plaque_holonomies", {})
    exact(errors, plaques, {
        "finite_n_pair_factorisation": (
            "H^s_{x,y;n}=H^s_{p,y;n}(H^s_{p,x;n})^-1 exactly"
        ),
        "local_cocycle_and_groupoid_identities": True,
        "uniform_holder_modulus_on_global_coding": False,
    }, "plaque holonomies")
    for key in (
        "stable_reference_limits",
        "unstable_reference_limits",
        "stable_all_pairs_local_plaque",
        "unstable_all_pairs_local_plaque",
    ):
        if not isinstance(plaques.get(key), str) or "exists" not in plaques[key]:
            errors.append(f"local plaque limit missing: {key}")

    limits = result.get("scope_limits", {})
    for key in (
        "single_compact_supported_gauge_on_qnl_return_section",
        "stable_all_pairs_on_one_local_qnl_plaque",
        "unstable_all_pairs_on_one_local_qnl_plaque",
    ):
        if limits.get(key) is not True:
            errors.append(f"certified local flag missing: {key}")
    for key in (
        "global_faithful_symbolic_coding",
        "global_all_pairs_holder_holonomies",
        "typed_qnl_homoclinic_loop",
        "butler_park_class_H",
        "park_piraino_fiber_bunching",
        "physical_projective_spectral_gap_or_PPE",
        "gate1_certified",
        "unconditional_cm2",
    ):
        if limits.get(key) is not False:
            errors.append(f"unsupported completion flag: {key}")

    exact(errors, data.get("verdict", {}), {
        "compact_supported_qnl_section_gauge": "CERTIFIED",
        "local_stable_unstable_all_pairs_plaque_holonomies": "CERTIFIED",
        "global_butler_park_class_H": "NOT_CERTIFIED",
        "gate1": "NOT_CERTIFIED",
        "unconditional_cm2": "NO_GO_FOR_CLAIM",
    }, "verdict")
    return errors


def check_replay(data: dict[str, Any]) -> list[str]:
    if str(HERE) not in sys.path:
        sys.path.insert(0, str(HERE))
    try:
        import cm2_gate1_compact_log_gauge_plaque_holonomy_frontier_cert as cert
        actual = cert.certify()
    except Exception as exc:  # pragma: no cover
        return [f"certificate replay failed: {exc}"]
    return [] if data.get("result") == actual else ["certificate replay mismatch"]


def run_self_test(data: dict[str, Any]) -> int:
    mutations: list[tuple[str, dict[str, Any]]] = []

    def add(label: str, mutate) -> None:
        tampered = copy.deepcopy(data)
        mutate(tampered)
        mutations.append((label, tampered))

    add("determinant", lambda d: d["result"]["compact_supported_section_gauge"].__setitem__("determinant", "unknown"))
    add("regularity", lambda d: d["result"]["compact_supported_section_gauge"].__setitem__("regularity", "C0"))
    add("boundary seam", lambda d: d["result"]["compact_supported_section_gauge"].__setitem__("no_chart_boundary_seam", False))
    add("stable pair factor", lambda d: d["result"]["local_qnl_plaque_holonomies"].__setitem__("finite_n_pair_factorisation", "false"))
    add("stable local plaque", lambda d: d["result"]["scope_limits"].__setitem__("stable_all_pairs_on_one_local_qnl_plaque", False))
    add("unstable local plaque", lambda d: d["result"]["scope_limits"].__setitem__("unstable_all_pairs_on_one_local_qnl_plaque", False))
    add("global holonomy overclaim", lambda d: d["result"]["scope_limits"].__setitem__("global_all_pairs_holder_holonomies", True))
    add("class H overclaim", lambda d: d["result"]["scope_limits"].__setitem__("butler_park_class_H", True))
    add("Gate 1 overclaim", lambda d: d["result"]["scope_limits"].__setitem__("gate1_certified", True))

    rejected = 0
    for label, tampered in mutations:
        if check_structure(tampered):
            rejected += 1
        else:
            print(f"SELF_TEST: FAIL ({label} mutation accepted)")
            return 1
    print(f"MUTATION_SELF_TEST: PASS ({rejected}/{len(mutations)} mutations rejected)")
    return 0


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
        print("GATE1_COMPACT_LOG_GAUGE_PLAQUE_HOLONOMY_INTEGRITY: FAIL")
        for error in errors:
            print(f"  {error}")
        return 1
    if args.self_test:
        return run_self_test(data)
    if args.integrity_only:
        print("REPLAY_AND_INTEGRITY: PASS")
        return 0
    print("GATE1_COMPACT_SECTION_GAUGE_AND_LOCAL_PLAQUE_HOLONOMIES: CERTIFIED")
    print("GATE1_GLOBAL_CLASS_H_AND_UNCONDITIONAL_TYPICALITY: NOT_CERTIFIED")
    print("GATE1: NOT_CERTIFIED")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
