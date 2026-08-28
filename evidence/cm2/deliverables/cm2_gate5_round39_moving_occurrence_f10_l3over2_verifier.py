#!/usr/bin/env python3
"""Fail-closed verifier for the round-39 moving-occurrence F10 moment."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import tempfile
from fractions import Fraction as Q
from pathlib import Path
from typing import Any

import cm2_gate5_round39_moving_occurrence_f10_l3over2_cert as cert


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
        rank = result["physical_rank_L3over2_derivation"]
        mass = Q(8064, 5)
        tail = Q(9158592, 6875)
        moment = mass * (1 << 21) + Q(7, 128) * tail
        if moment != Q(46506443753721, 13750):
            errors.append("independent rank arithmetic")
        if rank["positive_coarea_total_mass_upper"] != str(mass):
            errors.append("mass")
        if rank["integral_2^(3B/2)_dm_strict_upper"] != str(moment):
            errors.append("rank moment")
        if rank["rank_L3over2_moment_status"] != "CERTIFIED_PHYSICAL_RAW_COAREA":
            errors.append("rank status")

        f10 = result["moving_occurrence_seed_F10_L3over2_installation"]
        if f10["same_occurrence_ID_seed_count"] != 64:
            errors.append("seed count")
        if f10["oriented_trace_count"] != 128:
            errors.append("trace count")
        if f10["Lp_power"] != "p=3/2":
            errors.append("Lp")
        if f10["reverse_integral_raw_F10^(3/2)_strict_upper"] != str(1225 * moment):
            errors.append("reverse moment")
        if f10["forward_integral_raw_F10^(3/2)_strict_upper"] != str(4624 * moment):
            errors.append("forward moment")
        if f10["bidirectional_seed_F10_L3over2_status"] != (
            "CERTIFIED_PHYSICAL_RAW_COAREA"
        ):
            errors.append("F10 status")
        rows = f10["representative_integer_envelopes"]
        if len(rows) != 3:
            errors.append("row count")
        for row, rank_value in zip(rows, (14, 18, 24), strict=True):
            if row["B"] != rank_value:
                errors.append("row rank")
            if row["reverse_integer_envelope"] != 35 * (1 << rank_value):
                errors.append("reverse row")
            if row["forward_integer_envelope"] != 68 * (1 << rank_value):
                errors.append("forward row")

        exponents = result["physical_margin_blowup_exponent_match"]
        if exponents["physical_margin_tail_exponent_alpha"] != (
            "2 on this seed subatlas"
        ):
            errors.append("alpha")
        if exponents["F10_blowup_exponent_r"] != "1 on this seed subatlas":
            errors.append("r")
        if exponents["strict_product"] != "r*p=3/2<2=alpha":
            errors.append("product")
        if exponents["round38_integrability_criterion_met"] is not True:
            errors.append("criterion")
        if exponents["arbitrary_Rn_or_all_face_exponent_claimed"] is not False:
            errors.append("scope")

        scope = result["strict_nonpromotion"]
        if scope["arbitrary_Rn_pullback_F10_field"] != "NOT_CERTIFIED":
            errors.append("Rn promotion")
        if scope["complete_all_face_F10_field"] != "NOT_CERTIFIED":
            errors.append("all-face promotion")
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
        ("physical_rank_L3over2_derivation", "positive_coarea_total_mass_upper", "1"),
        (
            "physical_rank_L3over2_derivation",
            "integral_2^(3B/2)_dm_strict_upper",
            "1",
        ),
        (
            "physical_rank_L3over2_derivation",
            "rank_L3over2_moment_status",
            "NOT_CERTIFIED",
        ),
        (
            "moving_occurrence_seed_F10_L3over2_installation",
            "same_occurrence_ID_seed_count",
            63,
        ),
        (
            "moving_occurrence_seed_F10_L3over2_installation",
            "oriented_trace_count",
            127,
        ),
        ("moving_occurrence_seed_F10_L3over2_installation", "Lp_power", "p=2"),
        (
            "moving_occurrence_seed_F10_L3over2_installation",
            "reverse_integral_raw_F10^(3/2)_strict_upper",
            "1",
        ),
        (
            "moving_occurrence_seed_F10_L3over2_installation",
            "forward_integral_raw_F10^(3/2)_strict_upper",
            "1",
        ),
        (
            "moving_occurrence_seed_F10_L3over2_installation",
            "bidirectional_seed_F10_L3over2_status",
            "NOT_CERTIFIED",
        ),
        (
            "physical_margin_blowup_exponent_match",
            "physical_margin_tail_exponent_alpha",
            "1",
        ),
        ("physical_margin_blowup_exponent_match", "F10_blowup_exponent_r", "2"),
        ("physical_margin_blowup_exponent_match", "strict_product", "false"),
        (
            "physical_margin_blowup_exponent_match",
            "round38_integrability_criterion_met",
            False,
        ),
        (
            "physical_margin_blowup_exponent_match",
            "arbitrary_Rn_or_all_face_exponent_claimed",
            True,
        ),
    ]
    for section, key, value in edits:
        mutation = copy.deepcopy(source)
        mutation["result"][section][key] = value
        mutations.append(mutation)
    mutation = copy.deepcopy(source)
    mutation["result"]["moving_occurrence_seed_F10_L3over2_installation"][
        "representative_integer_envelopes"
    ].pop()
    mutations.append(mutation)
    mutation = copy.deepcopy(source)
    mutation["result"]["moving_occurrence_seed_F10_L3over2_installation"][
        "representative_integer_envelopes"
    ][0]["reverse_integer_envelope"] = 1
    mutations.append(mutation)
    for key in ("arbitrary_Rn_pullback_F10_field", "complete_all_face_F10_field", "Gate5"):
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
