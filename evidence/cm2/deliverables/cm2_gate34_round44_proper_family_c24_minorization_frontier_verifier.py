#!/usr/bin/env python3
"""Fail-closed verifier for the Round-44 proper-family minorization frontier."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import tempfile
from pathlib import Path
from typing import Any

import cm2_gate34_round44_proper_family_c24_minorization_frontier_cert as cert


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
        counter = result["properness_Growth_nonimplication"]
        if counter["Growth_inequality_holds_for_every_n"] is not True:
            errors.append("countermodel Growth")
        if counter["family_is_proper"] is not True:
            errors.append("countermodel properness")
        if counter["target_hit_mass_at_every_time"] != "0":
            errors.append("countermodel hit")
        if "not a counterexample to the physical billiard" not in counter["purpose"]:
            errors.append("countermodel scope")

        bump = result["direct_smooth_bump_mixing_route"]
        if bump["frozen_bump"]["mu_s_g_strict_lower"] != str(cert.BUMP_MASS):
            errors.append("bump mass")
        if bump["frozen_bump"]["C1_norm_strict_upper"] != str(cert.BUMP_C1):
            errors.append("bump C1")
        if bump["epsilon_hit"] != str(cert.HIT_GAP):
            errors.append("hit gap")
        if "2724*C_SF" not in bump["safe_threshold_formula"]:
            errors.append("threshold")
        for key in ("numeric_C_SF", "numeric_theta_SF", "numeric_H_SF"):
            if bump[key] is not None:
                errors.append(f"bump overclaim: {key}")

        magnet = result["C24_contained_coupling_magnet_route"]
        if magnet["official_source"] != (
            "Stenlund--Young--Zhang, arXiv:1210.0011v4"
        ):
            errors.append("SYZ source")
        if magnet["published_constants_are_uniform_but_not_numerical"] is not True:
            errors.append("SYZ effectivity")
        if magnet["C24_rectangle_geometry_is_a_certified_SYZ_magnet"] is not False:
            errors.append("magnet overclaim")
        if magnet["missing_input_count"] != 8:
            errors.append("magnet missing count")
        if magnet["numeric_zeta"] is not None or magnet["numeric_Delta"] is not None:
            errors.append("magnet numeric overclaim")
        if magnet["conditional_collision_rate"] != (
            "q_magnet=(1-zeta/2)^(1/Delta)<1"
        ):
            errors.append("magnet rate")

        frontier = result["shortest_numeric_frontier"]
        if frontier["already_numeric"]["C24_killed_Growth_depth"] != 9148:
            errors.append("Growth input")
        if frontier["numeric_proper_family_C24_minorization"] != "NOT_CERTIFIED":
            errors.append("minorization frontier")
        if frontier["numeric_collision_time_C_fw_C_rev_q"] != "NOT_CERTIFIED":
            errors.append("collision frontier")

        scope = result["strict_nonpromotion"]
        if scope["properness_Growth_alone_implies_C24_hit"] is not False:
            errors.append("Growth inference")
        if scope["numeric_proper_family_C24_minorization"] != "NOT_CERTIFIED":
            errors.append("minorization verdict")
        if scope["Gate4"] != "NOT_CERTIFIED":
            errors.append("Gate4")
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
        ("properness_Growth_nonimplication", "Growth_inequality_holds_for_every_n", False),
        ("properness_Growth_nonimplication", "family_is_proper", False),
        ("properness_Growth_nonimplication", "target_hit_mass_at_every_time", "1"),
        ("direct_smooth_bump_mixing_route", "epsilon_hit", "1"),
        ("direct_smooth_bump_mixing_route", "numeric_C_SF", "1"),
        ("direct_smooth_bump_mixing_route", "numeric_theta_SF", "1/2"),
        ("direct_smooth_bump_mixing_route", "numeric_H_SF", 1),
        ("C24_contained_coupling_magnet_route", "published_constants_are_uniform_but_not_numerical", False),
        ("C24_contained_coupling_magnet_route", "C24_rectangle_geometry_is_a_certified_SYZ_magnet", True),
        ("C24_contained_coupling_magnet_route", "missing_input_count", 0),
        ("C24_contained_coupling_magnet_route", "numeric_zeta", "1/2"),
        ("C24_contained_coupling_magnet_route", "numeric_Delta", 1),
        ("shortest_numeric_frontier", "numeric_proper_family_C24_minorization", "CERTIFIED"),
        ("shortest_numeric_frontier", "numeric_collision_time_C_fw_C_rev_q", "CERTIFIED"),
    ]
    for section, key, value in edits:
        mutation = copy.deepcopy(source)
        mutation["result"][section][key] = value
        mutations.append(mutation)
    mutation = copy.deepcopy(source)
    mutation["result"]["direct_smooth_bump_mixing_route"]["frozen_bump"][
        "mu_s_g_strict_lower"
    ] = "0"
    mutations.append(mutation)
    mutation = copy.deepcopy(source)
    mutation["result"]["shortest_numeric_frontier"]["already_numeric"][
        "C24_killed_Growth_depth"
    ] = 1
    mutations.append(mutation)
    for key, value in (
        ("properness_Growth_alone_implies_C24_hit", True),
        ("numeric_proper_family_C24_minorization", "CERTIFIED"),
        ("numeric_C24_coupling_magnet", "CERTIFIED"),
        ("numeric_collision_time_q", "CERTIFIED"),
        ("complete_numeric_C_fw_C_rev", "CERTIFIED"),
        ("strong_cemetery", "CERTIFIED"),
        ("Gate4", "CERTIFIED"),
        ("complete_composite_gates", "1/5"),
        ("CM2", "GO"),
    ):
        mutation = copy.deepcopy(source)
        mutation["result"]["strict_nonpromotion"][key] = value
        mutation["verdict"][key] = value
        mutations.append(mutation)
    for top, value in (
        ("certificate_sha256", "0" * 64),
        ("verifier_sha256", "0" * 64),
        ("dependencies", {}),
    ):
        mutation = copy.deepcopy(source)
        mutation[top] = value
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
