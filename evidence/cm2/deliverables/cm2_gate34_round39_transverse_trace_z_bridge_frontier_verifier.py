#!/usr/bin/env python3
"""Fail-closed verifier for the round-39 transverse-trace frontier."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import tempfile
from fractions import Fraction as Q
from pathlib import Path
from typing import Any

import cm2_gate34_round39_transverse_trace_z_bridge_frontier_cert as cert


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
        audit = result["canonical_parent_W_trace_type_audit"]
        if audit["parent_W_slope"] != "4":
            errors.append("parent slope")
        if audit["operator_present_in_current_dependency_chain"] is not False:
            errors.append("trace interface scope")
        if audit["typed_interface_status"] != "MISSING_EXACTLY_LOCATED":
            errors.append("interface status")

        model = result["stable_test_to_transverse_trace_countermodel"]
        if model["stable_short_leaf_exponent"] != "q=1/4":
            errors.append("short leaf exponent")
        if model["stable_controls_tend_to_zero_while_trace_stays_one"] is not True:
            errors.append("model conclusion")
        if model["augmented_trace_theorem_ruled_out"] is not False:
            errors.append("augmentation scope")
        if model["physical_CM2_impossibility_claimed"] is not False:
            errors.append("CM2 scope")
        rows = model["representative_exact_dyadic_rows"]
        if len(rows) != 5:
            errors.append("model row count")
        for row, exponent in zip(rows, (5, 9, 13, 17, 21), strict=True):
            epsilon = Q(1, 1 << exponent)
            block = (exponent - 1) // 4
            if row["epsilon"] != str(epsilon):
                errors.append("epsilon row")
            if row["total_two_dimensional_mass"] != str(2 * epsilon):
                errors.append("mass row")
            if row["stable_leaf_full_integral"] != str(epsilon):
                errors.append("leaf row")
            if row["stable_short_leaf_q14_upper"] != str(Q(1, 1 << (3 * block))):
                errors.append("stable bound row")
            if row["transverse_trace_on_x_equals_zero"] != "1":
                errors.append("trace row")

        budget = result["same_ID_Z_bridge_rate_budget"]
        rate = Q(111718729, 111718750)
        weight = Q(223437479, 223437458)
        weighted = weight * rate
        if budget["projective_rate_r"] != str(rate):
            errors.append("rate")
        if budget["weighted_projective_rate_wr"] != str(weighted):
            errors.append("weighted rate")
        if budget["unweighted_gamma_strict_upper"] != str(1 / rate):
            errors.append("unweighted threshold")
        if budget["weighted_gamma_strict_upper"] != str(1 / weighted):
            errors.append("weighted threshold")
        if budget["unweighted_allowed_excess_above_one"] != str(Q(21, 111718729)):
            errors.append("unweighted margin")
        if budget["weighted_allowed_excess_above_one"] != str(Q(21, 223437479)):
            errors.append("weighted margin")
        if not 2 * rate > 1 or not 2 * weighted > 1:
            errors.append("doubling arithmetic")
        if budget["doubling_bridge_loss_is_safe"] is not False:
            errors.append("doubling scope")

        scope = result["strict_nonpromotion"]
        if scope["bounded_canonical_transverse_trace_operator"] != "NOT_CERTIFIED":
            errors.append("trace promotion")
        if scope["canonical_standard_family_Z_tail"] != "NOT_CERTIFIED":
            errors.append("Z promotion")
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
        ("canonical_parent_W_trace_type_audit", "parent_W_slope", "3"),
        (
            "canonical_parent_W_trace_type_audit",
            "operator_present_in_current_dependency_chain",
            True,
        ),
        (
            "canonical_parent_W_trace_type_audit",
            "typed_interface_status",
            "CERTIFIED",
        ),
        (
            "stable_test_to_transverse_trace_countermodel",
            "stable_short_leaf_exponent",
            "q=1/2",
        ),
        (
            "stable_test_to_transverse_trace_countermodel",
            "stable_controls_tend_to_zero_while_trace_stays_one",
            False,
        ),
        (
            "stable_test_to_transverse_trace_countermodel",
            "augmented_trace_theorem_ruled_out",
            True,
        ),
        (
            "stable_test_to_transverse_trace_countermodel",
            "physical_CM2_impossibility_claimed",
            True,
        ),
        ("same_ID_Z_bridge_rate_budget", "projective_rate_r", "1"),
        ("same_ID_Z_bridge_rate_budget", "weighted_projective_rate_wr", "1"),
        ("same_ID_Z_bridge_rate_budget", "unweighted_gamma_strict_upper", "2"),
        ("same_ID_Z_bridge_rate_budget", "weighted_gamma_strict_upper", "2"),
        ("same_ID_Z_bridge_rate_budget", "doubling_bridge_loss_is_safe", True),
    ]
    for section, key, value in edits:
        mutation = copy.deepcopy(source)
        mutation["result"][section][key] = value
        mutations.append(mutation)
    mutation = copy.deepcopy(source)
    mutation["result"]["stable_test_to_transverse_trace_countermodel"][
        "representative_exact_dyadic_rows"
    ].pop()
    mutations.append(mutation)
    mutation = copy.deepcopy(source)
    mutation["result"]["stable_test_to_transverse_trace_countermodel"][
        "representative_exact_dyadic_rows"
    ][0]["transverse_trace_on_x_equals_zero"] = "0"
    mutations.append(mutation)
    for key in (
        "bounded_canonical_transverse_trace_operator",
        "canonical_standard_family_Z_tail",
        "Gate4",
    ):
        mutation = copy.deepcopy(source)
        mutation["result"]["strict_nonpromotion"][key] = "CERTIFIED"
        mutation["verdict"][key] = "CERTIFIED"
        mutations.append(mutation)
    mutation = copy.deepcopy(source)
    mutation["result"]["strict_nonpromotion"]["CM2"] = "GO"
    mutation["verdict"]["CM2"] = "GO"
    mutations.append(mutation)
    mutation = copy.deepcopy(source)
    mutation["certificate_sha256"] = "0" * 64
    mutations.append(mutation)
    mutation = copy.deepcopy(source)
    mutation["verifier_sha256"] = "0" * 64
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
