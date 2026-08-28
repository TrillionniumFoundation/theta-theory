#!/usr/bin/env python3
"""Independent verifier for the Round-56 ambient full-clock downstream leaf."""

from __future__ import annotations

import argparse
import copy
import hashlib
import importlib.util
import json
import sys
from fractions import Fraction as Q
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent
CERT_PATH = HERE / "cm2_gate34_round56_preproperisation_full_clock_downstream_cert.py"
DEFAULT_MANIFEST = (
    HERE
    / "cm2-gate34-round56-preproperisation-full-clock-downstream-manifest-2026-07-20.json"
)
RESULT_SCHEMA = "cm2.gate34.round56-preproperisation-full-clock-downstream.v1"
MANIFEST_SCHEMA = RESULT_SCHEMA + ".manifest.v1"


class DuplicateKeyError(ValueError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def sha256_path(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def strict_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    value: dict[str, Any] = {}
    for key, item in pairs:
        if key in value:
            raise DuplicateKeyError(key)
        value[key] = item
    return value


def strict_load_bytes(raw: bytes) -> dict[str, Any]:
    value = json.loads(
        raw.decode("utf-8"),
        object_pairs_hook=strict_object,
        parse_constant=lambda token: (_ for _ in ()).throw(
            ValueError(f"non-finite JSON constant: {token}")
        ),
    )
    require(isinstance(value, dict), "manifest root")
    return value


def load_cert() -> Any:
    require(CERT_PATH.is_file() and not CERT_PATH.is_symlink(), "certificate path")
    spec = importlib.util.spec_from_file_location("cm2_r56_downstream_cert", CERT_PATH)
    require(spec is not None and spec.loader is not None, "certificate spec")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


cert = load_cert()


def get_path(root: Any, path: tuple[str | int, ...]) -> Any:
    value = root
    for key in path:
        value = value[key]
    return value


def set_path(root: Any, path: tuple[str | int, ...], value: Any) -> None:
    target = root
    for key in path[:-1]:
        target = target[key]
    target[path[-1]] = value


REQUIRED_FIELDS: list[tuple[tuple[str | int, ...], Any]] = [
    (("schema",), RESULT_SCHEMA),
    (("provenance", "old_artifacts_modified"), False),
    (("provenance", "external_theorem_promoted"), False),
    (
        ("acyclic_dependency_ledger", "recordwise_geometry_requires_global_I_D"),
        False,
    ),
    (
        ("acyclic_dependency_ledger", "round56_J_pair_proof_uses_full_clock_conclusion"),
        False,
    ),
    (
        ("acyclic_dependency_ledger", "exact_preclock_factor"),
        "exp((696*Dbar)/4176)=exp(Dbar/6)",
    ),
    (
        ("acyclic_dependency_ledger", "status"),
        "CERTIFIED_ACYCLIC_DISCHARGE_OF_THE_PREPROPERISATION_MOMENT",
    ),
    (
        ("actual_full_clock_consequence", "actual_integrated_bound"),
        "integral Wtilde_r_star^r dm_star<nu(X)+2*A_Hjoint*I_D<infinity",
    ),
    (
        ("actual_full_clock_consequence", "physical_preproperisation_exp_Dbar_over_6_moment"),
        "CERTIFIED_FINITE",
    ),
    (
        ("actual_full_clock_consequence", "full_ambient_two_view_max_clock_exponential_moment"),
        "CERTIFIED_QUALITATIVELY_FINITE",
    ),
    (
        ("actual_full_clock_consequence", "parent_charged_total_ambient_max_envelope_L6over5"),
        "CERTIFIED_QUALITATIVELY_FINITE",
    ),
    (("actual_full_clock_consequence", "numeric_value_claimed"), False),
    (
        ("ambient_exhaustion_consequence", "status"),
        "CERTIFIED_AMBIENT_AC_BOREL_EXHAUSTION_TAIL_VANISHES",
    ),
    (("ambient_exhaustion_consequence", "weak_mass_cemetery_only"), True),
    (("ambient_exhaustion_consequence", "trace_current_control_inferred"), False),
    (
        ("strict_nonpromotion", "two_proper_view_measure_isomorphism"),
        "CERTIFIED_PINNED_ROUND51",
    ),
    (
        ("strict_nonpromotion", "two_proper_view_common_law_blocks_ambient_preclock"),
        False,
    ),
    (("strict_nonpromotion", "physical_J_pair"), "CERTIFIED_FINITE_PINNED_ROUND56"),
    (("strict_nonpromotion", "physical_defect_moment_I_D"), "CERTIFIED_FINITE_PINNED_ROUND56"),
    (
        ("strict_nonpromotion", "physical_preproperisation_exp_Dbar_over_6_moment"),
        "CERTIFIED_FINITE",
    ),
    (
        ("strict_nonpromotion", "full_ambient_two_view_max_clock_exponential_moment"),
        "CERTIFIED_QUALITATIVELY_FINITE",
    ),
    (
        ("strict_nonpromotion", "parent_charged_total_ambient_max_envelope_L6over5"),
        "CERTIFIED_QUALITATIVELY_FINITE",
    ),
    (("strict_nonpromotion", "ambient_AC_Borel_exhaustion_tail"), "CERTIFIED_VANISHING"),
    (("strict_nonpromotion", "physical_common_refinement_J_cap_total"), "NOT_CERTIFIED"),
    (("strict_nonpromotion", "proper_common_terminal_two_view_carrier"), "NOT_CERTIFIED"),
    (("strict_nonpromotion", "physical_proper_same_ID_first_return_kernel"), "NOT_CERTIFIED"),
    (("strict_nonpromotion", "intermediate_C24_avoidance_after_properisation"), "NOT_CERTIFIED"),
    (("strict_nonpromotion", "later_and_repeated_recovery_clock_moments"), "NOT_CERTIFIED"),
    (("strict_nonpromotion", "physical_collision_time_q_L6over5"), "NOT_CERTIFIED"),
    (("strict_nonpromotion", "strong_singular_current_cemetery"), "NOT_CERTIFIED"),
    (("strict_nonpromotion", "full_numeric_C_fw_C_rev_q"), "NOT_CERTIFIED"),
    (("strict_nonpromotion", "Gate4"), "NOT_CERTIFIED"),
    (("strict_nonpromotion", "complete_composite_gates"), "0/5"),
    (("strict_nonpromotion", "CM2"), "NO-GO_FOR_CLAIM"),
]


def independent_checks(manifest: dict[str, Any]) -> None:
    require(Q(696, 4176) == Q(1, 6), "clock exponent")
    require(cert.PRECLOCK_EXPONENT == Q(1, 6), "certificate exponent")
    require(cert.DEFECT_COEFFICIENT == Q(35, 99 * 2**309), "defect coefficient")
    result = manifest["result"]
    for path, expected in REQUIRED_FIELDS:
        require(get_path(result, path) == expected, f"required field: {path}")
    require(manifest["verdict"] == result["strict_nonpromotion"], "verdict parity")
    logic = result["acyclic_dependency_ledger"]["logical_order"]
    require(isinstance(logic, list) and len(logic) == 5, "dependency order")
    require("substitute" in logic[-1], "substitution is last")
    expanded = result["actual_full_clock_consequence"]["expanded_J_pair_bound"]
    require("35/(99*2^309)" in expanded and expanded.endswith("<infinity"), "expanded bound")


def verify_value(value: dict[str, Any], expected: dict[str, Any]) -> None:
    require(set(value) == set(expected), "top-level keys")
    require(value == expected, "deterministic manifest mismatch")
    require(value["schema"] == MANIFEST_SCHEMA, "manifest schema")
    require(value["certificate_sha256"] == sha256_path(CERT_PATH), "certificate hash")
    require(value["verifier_sha256"] == sha256_path(Path(__file__).resolve()), "verifier hash")
    require(value["dependencies"] == cert.DEPENDENCIES, "dependency ledger")
    require("R56_FINAL_SHA256" not in value["dependencies"].values(), "unfrozen hash")
    require(
        value["result"]["internal_replay_digest"]
        == cert.digest({k: v for k, v in value["result"].items() if k != "internal_replay_digest"}),
        "internal replay digest",
    )
    independent_checks(value)


def verify_manifest(path: Path) -> tuple[dict[str, Any], bytes, bytes]:
    path = path.resolve()
    require(path.is_file() and not path.is_symlink(), "manifest path")
    require(path.parent == HERE, "manifest outside deliverables")
    raw = path.read_bytes()
    value = strict_load_bytes(raw)
    expected = cert.build_manifest(Path(__file__).resolve())
    verify_value(value, expected)
    for name, expected_hash in cert.DEPENDENCIES.items():
        dependency = HERE / name
        require(dependency.is_file() and not dependency.is_symlink(), f"dependency path: {name}")
        require(dependency.resolve().parent == HERE, f"dependency scope: {name}")
        require(sha256_path(dependency) == expected_hash, f"dependency SHA: {name}")
    reemitted = (json.dumps(expected, indent=2, sort_keys=True) + "\n").encode("utf-8")
    return value, raw, reemitted


def hostile_mutations(base: dict[str, Any]) -> list[dict[str, Any]]:
    mutations: list[dict[str, Any]] = []

    def changed(path: tuple[str | int, ...], value: Any) -> None:
        item = copy.deepcopy(base)
        set_path(item, path, value)
        mutations.append(item)

    changed(("schema",), "bad.schema")
    changed(("certificate_sha256",), "0" * 64)
    changed(("verifier_sha256",), "1" * 64)
    changed(("dependencies",), {})
    changed(("result", "provenance", "old_artifacts_modified"), True)
    changed(("result", "provenance", "external_theorem_promoted"), True)
    changed(
        ("result", "acyclic_dependency_ledger", "recordwise_geometry_requires_global_I_D"),
        True,
    )
    changed(
        ("result", "acyclic_dependency_ledger", "round56_J_pair_proof_uses_full_clock_conclusion"),
        True,
    )
    changed(("result", "acyclic_dependency_ledger", "logical_order"), [])
    changed(
        ("result", "actual_full_clock_consequence", "physical_preproperisation_exp_Dbar_over_6_moment"),
        "NOT_CERTIFIED",
    )
    changed(
        ("result", "actual_full_clock_consequence", "full_ambient_two_view_max_clock_exponential_moment"),
        "NOT_CERTIFIED",
    )
    changed(
        ("result", "actual_full_clock_consequence", "parent_charged_total_ambient_max_envelope_L6over5"),
        "NOT_CERTIFIED",
    )
    changed(("result", "actual_full_clock_consequence", "numeric_value_claimed"), True)
    changed(("result", "ambient_exhaustion_consequence", "weak_mass_cemetery_only"), False)
    changed(("result", "ambient_exhaustion_consequence", "trace_current_control_inferred"), True)
    changed(("result", "strict_nonpromotion", "two_proper_view_common_law_blocks_ambient_preclock"), True)
    changed(("result", "strict_nonpromotion", "physical_J_pair"), "NOT_CERTIFIED")
    changed(("result", "strict_nonpromotion", "physical_defect_moment_I_D"), "NOT_CERTIFIED")
    changed(
        ("result", "strict_nonpromotion", "physical_common_refinement_J_cap_total"),
        "CERTIFIED",
    )
    changed(
        ("result", "strict_nonpromotion", "proper_common_terminal_two_view_carrier"),
        "CERTIFIED",
    )
    changed(
        ("result", "strict_nonpromotion", "physical_proper_same_ID_first_return_kernel"),
        "CERTIFIED",
    )
    changed(
        ("result", "strict_nonpromotion", "intermediate_C24_avoidance_after_properisation"),
        "CERTIFIED",
    )
    changed(
        ("result", "strict_nonpromotion", "later_and_repeated_recovery_clock_moments"),
        "CERTIFIED",
    )
    changed(("result", "strict_nonpromotion", "physical_collision_time_q_L6over5"), "CERTIFIED")
    changed(("result", "strict_nonpromotion", "strong_singular_current_cemetery"), "CERTIFIED")
    changed(("result", "strict_nonpromotion", "full_numeric_C_fw_C_rev_q"), "CERTIFIED")
    changed(("result", "strict_nonpromotion", "Gate4"), "CERTIFIED")
    changed(("result", "strict_nonpromotion", "complete_composite_gates"), "1/5")
    changed(("result", "strict_nonpromotion", "CM2"), "GO")
    changed(("result", "internal_replay_digest"), "f" * 64)
    changed(("verdict", "physical_collision_time_q_L6over5"), "CERTIFIED")
    changed(("verdict", "Gate4"), "CERTIFIED")
    item = copy.deepcopy(base)
    item["unexpected"] = True
    mutations.append(item)
    return mutations


def run_self_test(path: Path) -> int:
    base, raw, _ = verify_manifest(path)
    expected = cert.build_manifest(Path(__file__).resolve())
    rejected = 0
    mutations = hostile_mutations(base)
    for index, item in enumerate(mutations):
        try:
            verify_value(item, expected)
        except Exception:
            rejected += 1
        else:
            raise RuntimeError(f"hostile mutation accepted: {index}")
    raw_cases = [b'{"x":1,"x":2}', b'{"x":NaN}', b'{"x":Infinity}']
    duplicate = raw.replace(
        b'{\n  "certificate_sha256"',
        b'{\n  "schema": "duplicate",\n  "certificate_sha256"',
        1,
    )
    raw_cases.append(duplicate)
    for item in raw_cases:
        try:
            strict_load_bytes(item)
        except Exception:
            rejected += 1
        else:
            raise RuntimeError("hostile raw JSON accepted")
    total = len(mutations) + len(raw_cases)
    require(rejected == total, "hostile count")
    print(f"HOSTILE_MUTATIONS_REJECTED: {rejected}/{total}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("manifest", nargs="?", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--audit", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--reemit", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        return run_self_test(args.manifest)
    manifest, raw, reemitted = verify_manifest(args.manifest)
    if args.reemit:
        require(raw == reemitted, "re-emission mismatch")
        print("REEMIT_BYTE_IDENTICAL: PASS")
        return 0
    print("AUDIT_MODE: PASS")
    print(
        "PRECLOCK_I_D:",
        manifest["verdict"]["physical_preproperisation_exp_Dbar_over_6_moment"],
    )
    print(
        "AMBIENT_FULL_CLOCK:",
        manifest["verdict"]["full_ambient_two_view_max_clock_exponential_moment"],
    )
    print("PHYSICAL_Q:", manifest["verdict"]["physical_collision_time_q_L6over5"])
    print("GATE4:", manifest["verdict"]["Gate4"])
    print("CM2:", manifest["verdict"]["CM2"])
    return 0 if args.audit else 2


if __name__ == "__main__":
    raise SystemExit(main())
