#!/usr/bin/env python3
"""Fail-closed verifier for the Round-43 N_open effectivity frontier."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import tempfile
from pathlib import Path
from typing import Any

import cm2_gate34_round43_nopen_effectivity_frontier_cert as cert


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
        chain = result["published_projective_N_open_chain"]
        if chain["official_source"] != "arXiv:2104.06947v3":
            errors.append("source")
        if "refrain from making explicit" not in chain["published_effectivity_warning"]:
            errors.append("published warning")
        if chain["explicit_enlarged_cone_relations"]["C24_P0"] != 49:
            errors.append("P0")
        if chain["explicit_enlarged_cone_relations"]["C24_Ct"] != 1493:
            errors.append("Ct")
        if chain["missing_numerical_input_count"] != 9:
            errors.append("missing count")
        if chain["safe_conditional_schedule"] != (
            "N_open=max(N_return,nbar_delta+m_mix)"
        ):
            errors.append("schedule")
        if chain["published_chain_evaluates_to_an_integer_from_frozen_data"] is not False:
            errors.append("effectivity overclaim")
        if chain["effectivity_gap_status"] != (
            "CERTIFIED_MISSING_NUMERICAL_THEOREM_CONSTANTS"
        ):
            errors.append("gap status")

        bypass = result["native_standard_family_bypass_frontier"]
        if bypass["numerical_native_inputs_already_available"][
            "C24_killed_Growth_block"
        ] != 9148:
            errors.append("Growth input")
        if bypass["numeric_native_standard_family_hit_minorization"] != (
            "NOT_CERTIFIED"
        ):
            errors.append("minorization scope")
        if bypass["projective_route_replaced"] is not False:
            errors.append("replacement overclaim")

        scope = result["strict_nonpromotion"]
        if scope["N_open_effectivity_gap"] != "CERTIFIED":
            errors.append("frontier verdict")
        if scope["numeric_N_open"] != "NOT_CERTIFIED":
            errors.append("N_open verdict")
        if scope["final_same_ID_q"] != "NOT_CERTIFIED":
            errors.append("q verdict")
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
        ("published_projective_N_open_chain", "official_source", "wrong"),
        ("published_projective_N_open_chain", "published_effectivity_warning", "explicit"),
        ("published_projective_N_open_chain", "missing_numerical_input_count", 0),
        ("published_projective_N_open_chain", "safe_conditional_schedule", "N_open=1"),
        ("published_projective_N_open_chain", "published_chain_evaluates_to_an_integer_from_frozen_data", True),
        ("published_projective_N_open_chain", "effectivity_gap_status", "NONE"),
        ("native_standard_family_bypass_frontier", "numeric_native_standard_family_hit_minorization", "CERTIFIED"),
        ("native_standard_family_bypass_frontier", "projective_route_replaced", True),
    ]
    for section, key, value in edits:
        mutation = copy.deepcopy(source)
        mutation["result"][section][key] = value
        mutations.append(mutation)
    mutation = copy.deepcopy(source)
    mutation["result"]["published_projective_N_open_chain"][
        "explicit_enlarged_cone_relations"
    ]["C24_P0"] = 1
    mutations.append(mutation)
    mutation = copy.deepcopy(source)
    mutation["result"]["native_standard_family_bypass_frontier"][
        "numerical_native_inputs_already_available"
    ]["C24_killed_Growth_block"] = 1
    mutations.append(mutation)
    for key, value in (
        ("N_open_effectivity_gap", "OPEN"),
        ("numeric_N_open", "CERTIFIED"),
        ("numeric_collision_time_q", "CERTIFIED"),
        ("complete_numeric_C_fw_C_rev", "CERTIFIED"),
        ("final_same_ID_q", "CERTIFIED"),
        ("strong_cemetery", "CERTIFIED"),
        ("Gate4", "CERTIFIED"),
        ("complete_composite_gates", "1/5"),
        ("CM2", "GO"),
    ):
        mutation = copy.deepcopy(source)
        mutation["result"]["strict_nonpromotion"][key] = value
        mutation["verdict"][key] = value
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
