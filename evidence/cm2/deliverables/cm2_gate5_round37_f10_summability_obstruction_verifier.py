#!/usr/bin/env python3
"""Fail-closed verifier for the round-37 F10 summability obstruction."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import tempfile
from pathlib import Path
from typing import Any

import cm2_gate5_round37_f10_summability_obstruction_cert as cert


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
        model = result["countable_analytic_affine_germ_countermodel"]
        if model["total_mass"] != "sum_(k>=1)m_k=1":
            errors.append("total mass")
        if model["canonical_strict_F10_integer"] != "N_k=2^k":
            errors.append("F10 integer")
        if model["partial_weighted_sum"] != "sum_(k=1)^K m_k*N_k=K":
            errors.append("partial sum")
        if model["global_weighted_F10_sum"] != "infinity":
            errors.append("divergence")
        if model["pointwise_finite_plus_total_mass_implies_weighted_F10_L1"] is not False:
            errors.append("nonimplication")
        if model["physical_CM2_impossibility_claimed"] is not False:
            errors.append("scope")
        rows = model["representative_first_eight_rows"]
        if len(rows) != 8:
            errors.append("row count")
        for expected_k, row in enumerate(rows, 1):
            if row["k"] != expected_k:
                errors.append("row index")
            if row["canonical_F10_integer"] != 1 << expected_k:
                errors.append("row integer")
            if row["weighted_F10_contribution"] != "1":
                errors.append("row contribution")

        interface = result["required_physical_quantitative_interface"]
        if interface["current_D1_rank_sum_controls_N_F10"] is not False:
            errors.append("D1 scope")
        if interface["arbitrary_Rn_materialized_F10_rows"] != 0:
            errors.append("materialized rows")
        if interface["weighted_F10_L1_or_Lp_bound"] != "NOT_CERTIFIED":
            errors.append("weighted bound")
        downstream = result["downstream_same_ID_current_frontier"]
        if downstream["complete_operator_block_count"] != 0:
            errors.append("operator blocks")
        if len(downstream["promotion_order"]) != 4:
            errors.append("promotion order")

        scope = result["strict_nonpromotion"]
        if scope["complete_global_F10_field"] != "NOT_CERTIFIED":
            errors.append("F10 nonpromotion")
        if scope["moving_current_F13"] != "NOT_CERTIFIED":
            errors.append("F13 nonpromotion")
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
        ("countable_analytic_affine_germ_countermodel", "total_mass", "infinity"),
        ("countable_analytic_affine_germ_countermodel", "canonical_strict_F10_integer", "N_k=1"),
        ("countable_analytic_affine_germ_countermodel", "partial_weighted_sum", "bounded"),
        ("countable_analytic_affine_germ_countermodel", "global_weighted_F10_sum", "1"),
        ("countable_analytic_affine_germ_countermodel", "pointwise_finite_plus_total_mass_implies_weighted_F10_L1", True),
        ("countable_analytic_affine_germ_countermodel", "physical_CM2_impossibility_claimed", True),
        ("required_physical_quantitative_interface", "current_D1_rank_sum_controls_N_F10", True),
        ("required_physical_quantitative_interface", "arbitrary_Rn_materialized_F10_rows", 1),
        ("downstream_same_ID_current_frontier", "complete_operator_block_count", 1),
    ]
    for section, key, value in edits:
        mutation = copy.deepcopy(source)
        mutation["result"][section][key] = value
        mutations.append(mutation)
    mutation = copy.deepcopy(source)
    mutation["result"]["countable_analytic_affine_germ_countermodel"][
        "representative_first_eight_rows"
    ].pop()
    mutations.append(mutation)
    mutation = copy.deepcopy(source)
    mutation["result"]["countable_analytic_affine_germ_countermodel"][
        "representative_first_eight_rows"
    ][0]["weighted_F10_contribution"] = "0"
    mutations.append(mutation)
    mutation = copy.deepcopy(source)
    mutation["result"]["downstream_same_ID_current_frontier"]["promotion_order"].pop()
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
