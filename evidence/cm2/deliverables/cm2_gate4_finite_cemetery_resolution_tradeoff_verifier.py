#!/usr/bin/env python3
"""Fail-closed verifier for the Gate-4 finite-cemetery tradeoff."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
from fractions import Fraction
from pathlib import Path
from typing import Any

import cm2_gate4_finite_cemetery_resolution_tradeoff_cert as cert


HERE = Path(__file__).resolve().parent
SCHEMA = "cm2.gate4.finite-cemetery-resolution-tradeoff.manifest.v1"
RESULT_SCHEMA = "cm2.gate4.finite-cemetery-resolution-tradeoff.v1"
DEFAULT_MANIFEST = (
    HERE / "cm2-gate4-finite-cemetery-resolution-tradeoff-manifest-2026-07-16.json"
)
CERTIFICATE = HERE / "cm2_gate4_finite_cemetery_resolution_tradeoff_cert.py"


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
    if data.get("verifier_sha256") != sha256_path(Path(__file__)):
        errors.append("verifier hash mismatch")
    dependencies = data.get("dependencies", {})
    expected_dependencies = {
        cert.SOURCE_MANIFEST.name: cert.EXPECTED_SOURCE_MANIFEST_SHA256,
        cert.SOURCE_CERTIFICATE.name: cert.EXPECTED_SOURCE_CERTIFICATE_SHA256,
    }
    if dependencies != expected_dependencies:
        errors.append("dependency ledger mismatch")
    else:
        for name, expected in dependencies.items():
            path = HERE / name
            if not path.is_file() or sha256_path(path) != expected:
                errors.append(f"dependency hash mismatch: {name}")
    try:
        result = cert.certify()
    except Exception as exc:
        return errors + [f"certificate replay failed: {type(exc).__name__}: {exc}"]
    if result.get("schema") != RESULT_SCHEMA:
        errors.append("result schema mismatch")
    if data.get("result_sha256") != cert.digest(result):
        errors.append("result digest mismatch")
    theorem = result.get("finite_cemetery_resolution_theorem", {})
    limits = result.get("scope_limits", {})
    rows = result.get("dyadic_replay_rows", [])
    summary = data.get("replay_summary", {})
    expected_summary = {
        "checked_K": [1, 20],
        "checked_rows": 20,
        "dyadic_lower": "2^K-1",
        "vanishing_cemetery_fine_resolution": (
            "CHARGE_DIVERGES_UNDER_INVERSE_MASS_INTERFACE"
        ),
        "unnormalized_reweighted_escape_refuted": False,
        "numeric_growth_constants_certified": False,
        "gate4_certified": False,
    }
    if summary != expected_summary:
        errors.append("replay summary mismatch")
    expected_theorem = {
        "coordinate_pushforward": (
            "(u_e,s)_*(m_e,s/m_e,s(row_s)) is Lebesgue measure on [0,1]"
        ),
        "mass_per_atom_derivation": (
            "p_a=Lebesgue(A_a)<=diam_u(A_a)<=delta"
        ),
        "count_lower": "N>=ceil((1-epsilon)/delta)",
        "unconditional_charge_identity": "sum_a p_a p_a^-1=N",
        "conditional_on_survival_lower": (
            "with P_ret=sum_a p_a, E[cost | retained]>=N/P_ret>=1/delta"
        ),
        "dyadic_consequence": (
            "delta=2^-K and epsilon<=2^-K imply E[cost]>=2^K-1"
        ),
    }
    for key, expected in expected_theorem.items():
        if theorem.get(key) != expected:
            errors.append(f"theorem mismatch: {key}")
    if len(rows) != 20:
        errors.append("dyadic row count mismatch")
    else:
        for k, row in enumerate(rows, start=1):
            delta = Fraction(1, 1 << k)
            expected_count = (1 << k) - 1
            if row != {
                "K": k,
                "delta": str(delta),
                "epsilon_upper": str(delta),
                "minimum_atom_count": expected_count,
                "unconditional_inverse_mass_charge_lower": expected_count,
                "dyadic_formula": f"2^{k}-1",
            }:
                errors.append(f"dyadic row mismatch: K={k}")
                break
    if result.get("dyadic_replay_rows_sha256") != cert.digest(rows):
        errors.append("row digest mismatch")
    for key in (
        "finite_cemetery_uniform_leafwise_moment_escape",
        "unnormalized_reweighted_family_recovery_refuted",
        "external_random_depth_policy_refuted",
        "numeric_growth_constants_certified",
        "propagated_q_certified",
        "gate4_certified",
        "unconditional_cm2",
    ):
        if limits.get(key) is not False:
            errors.append(f"fail-closed scope mismatch: {key}")
    if limits.get(
        "deterministic_native_vanishing_cemetery_fine_resolution"
    ) != "CHARGE_DIVERGES_UNDER_INVERSE_MASS_INTERFACE":
        errors.append("native divergence scope mismatch")
    if limits.get("uses_only_normalized_cumulative_mass_coordinate") is not True:
        errors.append("mass-coordinate scope guard missing")
    if limits.get("diameter_to_mass_claim_outside_that_coordinate") is not False:
        errors.append("diameter-to-mass scope overclaim")

    # Independent correction guard: conditioning divides by the actual
    # retained mass P_ret, not by its lower bound 1-epsilon.  The desired
    # lower follows instead from N*delta>=P_ret.
    p_ret = Fraction(9, 10)
    delta = Fraction(1, 4)
    n = 4
    if not n * delta >= p_ret or not Fraction(n, 1) / p_ret >= 1 / delta:
        errors.append("conditional-survival arithmetic failed")
    verdict = data.get("verdict", {})
    if verdict != {
        "finite_cemetery_resolution_tradeoff": "CERTIFIED",
        "uniform_native_leafwise_recovery_moment": "NOT_CERTIFIED",
        "unnormalized_reweighted_family_escape": "NOT_REFUTED",
        "complete_numeric_C_fw_C_rev_q": "NOT_CERTIFIED",
        "gate4": "NOT_CERTIFIED",
    }:
        errors.append("verdict mismatch")
    return errors


def mutation_self_test(baseline: dict[str, Any]) -> list[str]:
    cases: list[tuple[str, dict[str, Any]]] = []

    def add(name: str, mutate: Any) -> None:
        candidate = copy.deepcopy(baseline)
        mutate(candidate)
        cases.append((name, candidate))

    add("schema", lambda d: d.__setitem__("schema", "mutated"))
    add("certificate_hash", lambda d: d.__setitem__("certificate_sha256", "0" * 64))
    add("verifier_hash", lambda d: d.__setitem__("verifier_sha256", "0" * 64))
    add(
        "dependency",
        lambda d: d["dependencies"].__setitem__(next(iter(d["dependencies"])), "0" * 64),
    )
    add("result", lambda d: d.__setitem__("result_sha256", "0" * 64))
    add(
        "row_count",
        lambda d: d["replay_summary"].__setitem__("checked_rows", 19),
    )
    add(
        "escape",
        lambda d: d["replay_summary"].__setitem__(
            "unnormalized_reweighted_escape_refuted", True
        ),
    )
    add(
        "numeric",
        lambda d: d["replay_summary"].__setitem__(
            "numeric_growth_constants_certified", True
        ),
    )
    add("verdict", lambda d: d["verdict"].__setitem__("gate4", "CERTIFIED"))
    return [name for name, candidate in cases if not check_structure(candidate)]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--replay", action="store_true")
    parser.add_argument("--integrity-only", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    try:
        data = json.loads(args.manifest.read_text(encoding="utf-8"))
    except Exception as exc:
        print(f"MANIFEST_READ: FAIL ({type(exc).__name__}: {exc})")
        raise SystemExit(1)
    errors = check_structure(data)
    if errors:
        for error in errors:
            print(f"VERIFY: FAIL: {error}")
        raise SystemExit(1)
    if args.self_test:
        failures = mutation_self_test(data)
        if failures:
            print("MUTATION_SELF_TEST: FAIL: " + ", ".join(failures))
            raise SystemExit(1)
        print("MUTATION_SELF_TEST: PASS (9/9 mutations rejected)")
        return
    if args.replay or args.integrity_only:
        print("REPLAY_AND_INTEGRITY: PASS")
        return
    print("GATE4_FINITE_CEMETERY_RESOLUTION_TRADEOFF: CERTIFIED")
    print("GATE4_NATIVE_CHARGED_RECOVERY_AND_PROPAGATED_Q: NOT_CERTIFIED")
    print("GATE4: NOT_CERTIFIED")
    raise SystemExit(2)


if __name__ == "__main__":
    main()
