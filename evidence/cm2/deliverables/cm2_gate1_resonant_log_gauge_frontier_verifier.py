#!/usr/bin/env python3
"""Fail-closed verifier for the Gate-1 resonant logarithmic gauge."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import sys
from pathlib import Path
from typing import Any, Callable


HERE = Path(__file__).resolve().parent
DEFAULT_MANIFEST = (
    HERE / "cm2-gate1-resonant-log-gauge-frontier-manifest-2026-07-16.json"
)
CERTIFICATE = HERE / "cm2_gate1_resonant_log_gauge_frontier_cert.py"
REPORT = HERE / "cm2-gate1-resonant-log-gauge-frontier-assault-2026-07-16.md"
SCHEMA = "cm2.gate1.resonant-log-gauge-frontier.manifest.v1"
RESULT_SCHEMA = "cm2.gate1.resonant-log-gauge-frontier.v1"


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
    if not isinstance(dependencies, dict) or not dependencies:
        errors.append("dependencies missing")
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

    exact(errors, result.get("provenance", {}), {
        "canonical_resonance_manifest": (
            "cm2-gate1-canonical-holonomy-resonance-manifest-2026-07-15.json"
        ),
        "source_model_id": (
            "cm2-centered-fixed-section-pilot-v52-qnl-natural-derivative"
        ),
        "source_resonance": "325/144",
        "canonical_resonance_certificate": (
            "cm2_gate1_canonical_holonomy_resonance_cert.py"
        ),
        "qnl_certificate": "cm2_fixed_section_qnl_cert.py",
    }, "provenance")

    gauge = result.get("exact_resonant_truncated_gauge", {})
    exact(errors, gauge, {
        "exact_input_ratio": "g/mu=-325/144",
        "gauge_coefficient": "k=g/(mu*log(mu))=-325/(144*log(mu))",
        "determinant_B": "1 exactly",
        "homological_equation": "lambda*t(mu*y)-mu*t(y)=g*y^2",
        "log_y_coefficients": ["1", "-1"],
        "log_y_coefficient_sum": "0",
        "constant_coefficient_after_log_shift": "mu*k*log(mu)=g",
        "transformed_truncated_cocycle": (
            "B(mu*y)^(-1)*M_2(y)*B(y)=diag(lambda,mu) exactly"
        ),
        "truncated_QNL_canonical_stable_tail": "CONSTANT_AND_CONVERGENT",
        "two_axis_local_gauge": (
            "B(x,y)=B_u(x)*B_s(y), det(B)=1 exactly"
        ),
    }, "truncated gauge")
    exact(errors, gauge.get("exact_symmetric_cubic_resonances", {}), {
        "F1_xxy_over_lambda": "325/72 exactly",
        "F2_xyy_over_mu": "-325/72 exactly",
        "unstable_resonant_cocycle_ratio": "g_u/lambda=325/144",
        "stable_resonant_cocycle_ratio": "g_s/mu=-325/144",
    }, "symmetric resonances")
    exact(errors, gauge.get("unstable_axis", {}), {
        "exact_input_ratio": "g_u/lambda=325/144",
        "homological_equation": (
            "mu*t(lambda*x)-lambda*t(x)=g_u*x^2"
        ),
        "truncated_QNL_canonical_unstable_tail": (
            "CONSTANT_AND_CONVERGENT_BACKWARD"
        ),
    }, "unstable truncated gauge")

    regularity = result.get("gauge_regularity_and_minimality", {})
    exact(errors, regularity, {
        "regularity": "C^1 and C^{1,alpha} for every 0<alpha<1",
        "not_C2": True,
        "nonzero_k": True,
        "C2_quadratic_gauge_cannot_cancel_g": True,
        "logarithmic_loss_is_the_resonant_escape": True,
    }, "gauge regularity")

    physical = result.get("analytic_physical_QNL_tail", {})
    exact(errors, physical, {
        "stable_base": "S(y)=mu*y+O(y^3)",
        "stable_orbit_asymptotic": (
            "y_n/mu^n -> c(z) != 0 for local nontrivial z"
        ),
        "local_transformed_QNL_stable_canonical_increment_series": (
            "ABSOLUTELY_SUMMABLE"
        ),
        "local_transformed_QNL_stable_canonical_limit": "CONVERGENT",
        "local_transformed_QNL_unstable_canonical_increment_series": (
            "ABSOLUTELY_SUMMABLE_BACKWARD"
        ),
        "local_transformed_QNL_unstable_canonical_limit": "CONVERGENT",
        "natural_gauge_limit_remains_nonconvergent": True,
    }, "physical tail")
    exact(errors, physical.get("conjugated_increment_envelopes", {}), {
        "critical_21": "O(n*mu^n)",
        "diagonal": "O(n*mu^(2*n))",
        "decaying_12": "O(mu^(4*n))",
    }, "increment envelopes")

    limits = result.get("scope_limits", {})
    if limits.get("local_log_gauge_QNL_stable_tail_repaired") is not True:
        errors.append("local logarithmic repair missing")
    if limits.get("local_log_gauge_QNL_unstable_tail_repaired") is not True:
        errors.append("local unstable logarithmic repair missing")
    for key in (
        "natural_gauge_QNL_holonomy_repaired",
        "global_faithful_symbolic_coding_constructed",
        "all_stable_pairs_common_holder_holonomies",
        "unstable_holonomies_constructed",
        "butler_park_class_H_globally_certified",
        "park_piraino_fiber_bunching_restored",
        "physical_full_mass_quotient_constructed",
        "gate1_certified",
        "unconditional_cm2",
    ):
        if limits.get(key) is not False:
            errors.append(f"unsupported completion flag: {key}")

    if result.get("internal_digest") != (
        "4c4591cb3f9a40863ade1715b322b0a1820d034f0993a4244b8edef9d4ed5883"
    ):
        errors.append("internal digest mismatch")
    exact(errors, data.get("verdict", {}), {
        "local_resonant_log_gauge_QNL_stable_tail": "CERTIFIED",
        "global_butler_park_class_H": "NOT_CERTIFIED",
        "park_piraino_on_natural_codings": "NO_GO",
        "gate1": "NOT_CERTIFIED",
        "unconditional_cm2": "NO_GO_FOR_CLAIM",
    }, "verdict")
    return errors


def check_replay(data: dict[str, Any]) -> list[str]:
    if str(HERE) not in sys.path:
        sys.path.insert(0, str(HERE))
    try:
        import cm2_gate1_resonant_log_gauge_frontier_cert as cert
        actual = cert.certify()
    except Exception as exc:  # pragma: no cover - fail-closed path
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
        print("GATE1_RESONANT_LOG_GAUGE_FRONTIER_INTEGRITY: FAIL")
        for error in errors:
            print(f"  {error}")
        return 1

    if args.self_test:
        Mutation = tuple[str, Callable[[dict[str, Any]], None]]
        mutations: list[Mutation] = [
            (
                "resonance",
                lambda d: d["result"]["exact_resonant_truncated_gauge"].__setitem__(
                    "exact_input_ratio", "g/mu=0"
                ),
            ),
            (
                "homological identity",
                lambda d: d["result"]["exact_resonant_truncated_gauge"].__setitem__(
                    "log_y_coefficient_sum", "1"
                ),
            ),
            (
                "regularity",
                lambda d: d["result"]["gauge_regularity_and_minimality"].__setitem__(
                    "not_C2", False
                ),
            ),
            (
                "critical envelope",
                lambda d: d["result"]["analytic_physical_QNL_tail"][
                    "conjugated_increment_envelopes"
                ].__setitem__("critical_21", "O(1)"),
            ),
            (
                "stable orbit asymptotic",
                lambda d: d["result"]["analytic_physical_QNL_tail"].__setitem__(
                    "stable_orbit_asymptotic", "y_n=O(mu^n)"
                ),
            ),
            (
                "local repair",
                lambda d: d["result"]["scope_limits"].__setitem__(
                    "local_log_gauge_QNL_stable_tail_repaired", False
                ),
            ),
            (
                "unstable local repair",
                lambda d: d["result"]["scope_limits"].__setitem__(
                    "local_log_gauge_QNL_unstable_tail_repaired", False
                ),
            ),
            (
                "global class-H overclaim",
                lambda d: d["result"]["scope_limits"].__setitem__(
                    "butler_park_class_H_globally_certified", True
                ),
            ),
            (
                "fiber-bunching overclaim",
                lambda d: d["result"]["scope_limits"].__setitem__(
                    "park_piraino_fiber_bunching_restored", True
                ),
            ),
        ]
        for label, mutate in mutations:
            tampered = copy.deepcopy(data)
            mutate(tampered)
            if not check_structure(tampered):
                print(f"SELF_TEST: FAIL ({label} tamper accepted)")
                return 1
        print("SELF_TEST: PASS")
        for label, _ in mutations:
            print(f"  {label} tamper rejected")
        return 0

    print("GATE1_QNL_RESONANT_LOG_GAUGE_LOCAL_STABLE_UNSTABLE_TAILS: CERTIFIED")
    if args.integrity_only:
        print("GATE1_RESONANT_LOG_GAUGE_FRONTIER_INTEGRITY: PASS")
        return 0
    print("GATE1_GLOBAL_CLASS_H_AND_UNCONDITIONAL_TYPICALITY: NOT_CERTIFIED")
    print("GATE1: NOT_CERTIFIED")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
