#!/usr/bin/env python3
"""Fail-closed verifier for the round-38 F10 margin exponent frontier."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import tempfile
from fractions import Fraction as Q
from pathlib import Path
from typing import Any

import cm2_gate5_round38_f10_margin_exponent_frontier_cert as cert


def pairs(rows: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in rows:
        if key in result:
            raise ValueError(f"duplicate key: {key}")
        result[key] = value
    return result


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(path: Path) -> dict[str, Any]:
    value = json.loads(
        path.read_text(encoding="utf-8"),
        object_pairs_hook=pairs,
        parse_constant=lambda token: (_ for _ in ()).throw(ValueError(token)),
    )
    if not isinstance(value, dict):
        raise ValueError("manifest root")
    return value


def verify(path: Path) -> list[str]:
    errors: list[str] = []
    try:
        manifest = load(path)
        if set(manifest) != {
            "schema",
            "certificate_sha256",
            "verifier_sha256",
            "dependencies",
            "result",
            "verdict",
        }:
            errors.append("top-level keys")
        if manifest.get("schema") != cert.MANIFEST_SCHEMA:
            errors.append("schema")
        if manifest.get("certificate_sha256") != sha(Path(cert.__file__).resolve()):
            errors.append("certificate hash")
        if manifest.get("verifier_sha256") != sha(Path(__file__).resolve()):
            errors.append("verifier hash")
        if manifest.get("dependencies") != cert.DEPENDENCIES:
            errors.append("dependencies")
        expected = cert.build_result()
        if manifest.get("result") != expected:
            errors.append("result")
        if manifest.get("verdict") != expected["strict_nonpromotion"]:
            errors.append("verdict")

        result = manifest["result"]
        theorem = result["dyadic_margin_integrability_theorem"]
        if theorem["geometric_series_ratio"] != "2^(r*p-alpha)":
            errors.append("series ratio")
        if theorem["sufficient_and_sharp_strict_condition"] != "r*p<alpha":
            errors.append("criterion")
        if theorem["theorem_status"] != "CERTIFIED_EXACT_DYADIC_CRITERION":
            errors.append("theorem status")

        model = result["critical_linear_tube_countermodel"]
        if model["total_mass"] != "1":
            errors.append("total mass")
        if model["linear_margin_tail"] != "mu{eta<=t}<=t for every 0<t<1":
            errors.append("linear tail")
        if model["critical_exponents"] != "alpha=1, r=1, p=1":
            errors.append("critical exponents")
        if model["global_F10_L1_sum"] != "infinity":
            errors.append("divergence")
        if model["linear_tube_tail_alone_implies_inverse_margin_F10_L1"] is not False:
            errors.append("nonimplication")
        if model["physical_CM2_impossibility_claimed"] is not False:
            errors.append("scope")
        rows = model["representative_first_eight_shells"]
        if len(rows) != 8:
            errors.append("row count")
        for expected_k, row in enumerate(rows, 1):
            if row["k"] != expected_k:
                errors.append("row index")
            if row["shell_mass"] != str(Q(1, 1 << (expected_k + 1))):
                errors.append("row mass")
            if row["margin_eta"] != str(Q(1, 1 << expected_k)):
                errors.append("row margin")
            if row["finite_F10_integer"] != 1 << expected_k:
                errors.append("row F10")
            if row["L1_contribution"] != "1/2":
                errors.append("row contribution")

        budget = result["physical_F10_exponent_budget"]
        if budget["physical_margin_exponent_interpretation"] != "alpha=1 in h, not alpha=1/3":
            errors.append("width exponent")
        if budget["one_step_parameter_averaged_scope_only"] is not True:
            errors.append("one-step scope")
        if budget["certified_physical_F10_blowup_exponent_r"] is not None:
            errors.append("r scope")
        if budget["certified_arbitrary_Rn_margin_tail_exponent_alpha"] is not None:
            errors.append("alpha scope")
        if budget["current_D1_rank_tail_closes_path_margin_products"] is not False:
            errors.append("D1 scope")

        scope = result["strict_nonpromotion"]
        if scope["complete_global_F10_field"] != "NOT_CERTIFIED":
            errors.append("F10 scope")
        if scope["Gate5_maturity"] != "7/18_UNCHANGED":
            errors.append("maturity")
        if scope["complete_composite_gates"] != "0/5":
            errors.append("gate count")
        if scope["CM2"] != "NO-GO_FOR_CLAIM":
            errors.append("CM2")
    except Exception as exc:
        errors.append(f"exception: {exc}")
    return errors


def self_test(path: Path) -> tuple[int, int]:
    source = load(path)
    mutations: list[dict[str, Any]] = []
    edits = [
        ("dyadic_margin_integrability_theorem", "geometric_series_ratio", "1"),
        ("dyadic_margin_integrability_theorem", "sufficient_and_sharp_strict_condition", "r*p<=alpha"),
        ("dyadic_margin_integrability_theorem", "theorem_status", "NOT_CERTIFIED"),
        ("critical_linear_tube_countermodel", "total_mass", "infinity"),
        ("critical_linear_tube_countermodel", "linear_margin_tail", "false"),
        ("critical_linear_tube_countermodel", "critical_exponents", "alpha=2"),
        ("critical_linear_tube_countermodel", "global_F10_L1_sum", "1"),
        ("critical_linear_tube_countermodel", "linear_tube_tail_alone_implies_inverse_margin_F10_L1", True),
        ("critical_linear_tube_countermodel", "physical_CM2_impossibility_claimed", True),
        ("physical_F10_exponent_budget", "physical_margin_exponent_interpretation", "alpha=1/3"),
        ("physical_F10_exponent_budget", "one_step_parameter_averaged_scope_only", False),
        ("physical_F10_exponent_budget", "certified_physical_F10_blowup_exponent_r", "1/2"),
        ("physical_F10_exponent_budget", "current_D1_rank_tail_closes_path_margin_products", True),
    ]
    for section, key, value in edits:
        mutation = copy.deepcopy(source)
        mutation["result"][section][key] = value
        mutations.append(mutation)
    mutation = copy.deepcopy(source)
    mutation["result"]["critical_linear_tube_countermodel"][
        "representative_first_eight_shells"
    ].pop()
    mutations.append(mutation)
    mutation = copy.deepcopy(source)
    mutation["result"]["critical_linear_tube_countermodel"][
        "representative_first_eight_shells"
    ][0]["L1_contribution"] = "0"
    mutations.append(mutation)
    mutation = copy.deepcopy(source)
    mutation["result"]["strict_nonpromotion"]["complete_global_F10_field"] = "CERTIFIED"
    mutation["verdict"]["complete_global_F10_field"] = "CERTIFIED"
    mutations.append(mutation)
    mutation = copy.deepcopy(source)
    mutation["result"]["strict_nonpromotion"]["Gate5"] = "CERTIFIED"
    mutation["verdict"]["Gate5"] = "CERTIFIED"
    mutations.append(mutation)
    mutation = copy.deepcopy(source)
    mutation["result"]["strict_nonpromotion"]["CM2"] = "GO"
    mutation["verdict"]["CM2"] = "GO"
    mutations.append(mutation)
    mutation = copy.deepcopy(source)
    mutation["certificate_sha256"] = "0" * 64
    mutations.append(mutation)
    mutation = copy.deepcopy(source)
    mutation["dependencies"] = {}
    mutations.append(mutation)

    rejected = 0
    with tempfile.TemporaryDirectory() as directory:
        for index, mutation in enumerate(mutations):
            target = Path(directory) / f"mutation-{index}.json"
            target.write_text(json.dumps(mutation), encoding="utf-8")
            rejected += bool(verify(target))
    return rejected, len(mutations)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("manifest", nargs="?", type=Path, default=cert.DEFAULT_MANIFEST)
    parser.add_argument("--integrity-only", action="store_true")
    parser.add_argument("--replay", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    errors = verify(args.manifest)
    if errors:
        print("AUDIT_MODE: FAIL")
        for error in errors:
            print(error)
        return 1
    if args.self_test:
        rejected, total = self_test(args.manifest)
        print(f"HOSTILE_MUTATIONS_REJECTED: {rejected}/{total}")
        return 0 if rejected == total else 1
    if args.integrity_only or args.replay:
        print("AUDIT_MODE: PASS")
        return 0
    print("AUDIT_MODE: PASS")
    print("CM2: NO-GO_FOR_CLAIM")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
