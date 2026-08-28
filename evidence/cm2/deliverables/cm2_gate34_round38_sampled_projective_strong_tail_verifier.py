#!/usr/bin/env python3
"""Fail-closed verifier for the round-38 sampled projective strong tail."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import tempfile
from fractions import Fraction as Q
from pathlib import Path
from typing import Any

import cm2_gate34_round38_sampled_projective_strong_tail_cert as cert


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
        bridge = result["projective_order_norm_bridge"]
        if bridge["bridge_status"] != "CERTIFIED_QUALITATIVE":
            errors.append("order bridge")
        if bridge["numeric_Delta_open"] is not None or bridge["numeric_K_cone"] is not None:
            errors.append("numeric cone scope")
        if bridge["constant_density_one_is_the_projective_reference"] is not True:
            errors.append("order reference")

        tail = result["sampled_C24_killed_strong_tail"]
        epsilon = Q(21, 111718750)
        survival = 1 - epsilon
        weight = Q(survival.denominator + survival.numerator, 2 * survival.numerator)
        weighted = weight * survival
        if tail["explicit_mass_survival_factor_r"] != str(survival):
            errors.append("survival")
        if tail["one_rational_block_weight_w"] != str(weight):
            errors.append("weight")
        if tail["weighted_factor_w_times_r"] != str(weighted):
            errors.append("weighted factor")
        if tail["weighted_factor_margin"] != str(1 - weighted):
            errors.append("weighted margin")
        if not weight > 1 or not weighted < 1:
            errors.append("weight signs")
        if tail["explicit_rational_rate_and_resolvent"] != "CERTIFIED":
            errors.append("resolvent")

        model = result["standard_family_representation_nonuniqueness"]
        if model["same_density_and_same_projective_cone_element_for_every_k"] is not True:
            errors.append("same density")
        if model["representation_dependent_Z_is_unbounded"] is not True:
            errors.append("unbounded Z")
        if model["projective_order_tail_implies_standard_family_Z_tail"] is not False:
            errors.append("Z nonimplication")
        rows = model["representative_rows"]
        if [row["pieces_per_horizontal_leaf"] for row in rows] != [1, 2, 4, 8, 16]:
            errors.append("row pieces")
        for row in rows:
            pieces = row["pieces_per_horizontal_leaf"]
            if row["piece_length"] != str(Q(1, pieces)):
                errors.append("piece length")
            if row["weight_per_piece"] != str(Q(1, pieces)):
                errors.append("piece weight")
            if row["standard_family_Z"] != str(pieces):
                errors.append("row Z")

        frontier = result["physical_installation_frontier"]
        if frontier["scheduled_sparse_C24_projective_strong_skeleton"] != (
            "CERTIFIED_QUALITATIVE"
        ):
            errors.append("sampled skeleton")
        if frontier["full_QN_standard_family_characteristic_C_N"] != "NOT_CERTIFIED":
            errors.append("full QN scope")
        if frontier["silently_replace_frozen_first_return_by_sampled_return"] is not False:
            errors.append("inducing scope")

        scope = result["strict_nonpromotion"]
        if scope["standard_family_Z_or_Growth_tail"] != "NOT_CERTIFIED":
            errors.append("Z scope")
        if scope["Gate4"] != "NOT_CERTIFIED":
            errors.append("Gate4")
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
        ("projective_order_norm_bridge", "bridge_status", "NOT_CERTIFIED"),
        ("projective_order_norm_bridge", "numeric_Delta_open", "1"),
        ("projective_order_norm_bridge", "constant_density_one_is_the_projective_reference", False),
        ("sampled_C24_killed_strong_tail", "explicit_mass_survival_factor_r", "1"),
        ("sampled_C24_killed_strong_tail", "one_rational_block_weight_w", "1"),
        ("sampled_C24_killed_strong_tail", "weighted_factor_margin", "0"),
        ("sampled_C24_killed_strong_tail", "explicit_rational_rate_and_resolvent", "NOT_CERTIFIED"),
        ("standard_family_representation_nonuniqueness", "same_density_and_same_projective_cone_element_for_every_k", False),
        ("standard_family_representation_nonuniqueness", "representation_dependent_Z_is_unbounded", False),
        ("standard_family_representation_nonuniqueness", "projective_order_tail_implies_standard_family_Z_tail", True),
        ("physical_installation_frontier", "full_QN_standard_family_characteristic_C_N", "CERTIFIED"),
        ("physical_installation_frontier", "silently_replace_frozen_first_return_by_sampled_return", True),
    ]
    for section, key, value in edits:
        mutation = copy.deepcopy(source)
        mutation["result"][section][key] = value
        mutations.append(mutation)
    mutation = copy.deepcopy(source)
    mutation["result"]["standard_family_representation_nonuniqueness"][
        "representative_rows"
    ].pop()
    mutations.append(mutation)
    mutation = copy.deepcopy(source)
    mutation["result"]["standard_family_representation_nonuniqueness"][
        "representative_rows"
    ][1]["standard_family_Z"] = "1"
    mutations.append(mutation)
    mutation = copy.deepcopy(source)
    mutation["result"]["strict_nonpromotion"]["standard_family_Z_or_Growth_tail"] = "CERTIFIED"
    mutation["verdict"]["standard_family_Z_or_Growth_tail"] = "CERTIFIED"
    mutations.append(mutation)
    mutation = copy.deepcopy(source)
    mutation["result"]["strict_nonpromotion"]["Gate4"] = "CERTIFIED"
    mutation["verdict"]["Gate4"] = "CERTIFIED"
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
