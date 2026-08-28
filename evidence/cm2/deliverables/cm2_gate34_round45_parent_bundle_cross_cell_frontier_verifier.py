#!/usr/bin/env python3
"""Fail-closed verifier for the Round-45 cross-cell frontier."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import tempfile
from pathlib import Path
from typing import Any

import cm2_gate34_round45_parent_bundle_cross_cell_frontier_cert as cert


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
        scale = result["canonical_crossing_scale_audit"]
        if scale["crossing_arc_Euclidean_length_strict_lower"] != str(
            cert.CROSSING_ARC_LOWER
        ):
            errors.append("crossing length")
        if scale["canonical_natural_cell_Euclidean_length_upper"] != str(
            cert.CELL_LENGTH
        ):
            errors.append("cell length")
        if scale["minimum_distinct_short_cell_IDs_in_one_crossing"] != (
            cert.MINIMUM_CROSSING_CELL_COUNT
        ):
            errors.append("cell count")
        if scale["single_canonical_parent_W_ID_can_be_a_transverse_crossing"] is not False:
            errors.append("single-cell overclaim")
        if scale["round44_long_canonical_parent_W_wording"] != "CORRECTED":
            errors.append("round44 correction")

        counter = result["cross_cell_weight_nonimplication"]
        if "not a counterexample to the physical billiard" not in counter["purpose"]:
            errors.append("countermodel scope")
        if counter["per_cell_density_ratio"] != "1<2000/1999":
            errors.append("countermodel density")
        if counter["family_is_proper"] is not True:
            errors.append("countermodel properness")
        if counter["geometric_extended_parent_crosses_C24"] is not True:
            errors.append("countermodel crossing")
        if counter["C24_hit_mass"] != "0":
            errors.append("countermodel hit")

        interface = result["extended_parent_bundle_minorization_interface"]
        if interface["cellwise_ratio_cannot_be_used_as_R_ext"] is not True:
            errors.append("cross-cell typing")
        hypothetical = interface[
            "hypothetical_only_if_R_ext_equals_2000_over_1999"
        ]
        if hypothetical["one_crossing_pair_hit_fraction_strict_lower"] != (
            "1999/6000000"
        ):
            errors.append("hypothetical pair hit")
        if hypothetical["required_beta_strict_lower"] != "4032/7146425":
            errors.append("beta threshold")
        if hypothetical["safe_reciprocal_beta"] != str(
            cert.HYPOTHETICAL_CROSSING_WEIGHT
        ):
            errors.append("safe beta")
        if hypothetical["next_reciprocal_fails"] != str(
            cert.HYPOTHETICAL_FAILING_WEIGHT
        ):
            errors.append("failing beta")
        for key in ("numeric_R_ext", "numeric_H_cover", "numeric_beta"):
            if interface[key] is not None:
                errors.append(f"interface overclaim: {key}")

        frontier = result["shortest_numeric_frontier"]
        if frontier["post_C24_cut_same_proper_class_return"] != "NOT_CERTIFIED":
            errors.append("post-cut overclaim")
        if frontier["numeric_proper_family_C24_minorization"] != "NOT_CERTIFIED":
            errors.append("minorization frontier")

        scope = result["strict_nonpromotion"]
        expected_scope = {
            "single_canonical_short_cell_covering_route": "DISPROVED_BY_SCALE",
            "extended_parent_bundle_registry": "NOT_CERTIFIED",
            "cross_cell_density_weight_continuation": "NOT_CERTIFIED",
            "numeric_proper_family_C24_minorization": "NOT_CERTIFIED",
            "numeric_collision_time_q": "NOT_CERTIFIED",
            "complete_numeric_C_fw_C_rev": "NOT_CERTIFIED",
            "strong_cemetery": "NOT_CERTIFIED",
            "Gate4": "NOT_CERTIFIED",
            "complete_composite_gates": "0/5",
            "CM2": "NO-GO_FOR_CLAIM",
        }
        if scope != expected_scope:
            errors.append("strict scope")
    except Exception as exc:
        errors.append(f"exception: {exc}")
    return errors


def self_test(path: Path) -> tuple[int, int]:
    source = load(path)
    mutations: list[dict[str, Any]] = []
    edits = [
        ("canonical_crossing_scale_audit", "crossing_arc_Euclidean_length_strict_lower", "0"),
        ("canonical_crossing_scale_audit", "canonical_natural_cell_Euclidean_length_upper", "1"),
        ("canonical_crossing_scale_audit", "minimum_distinct_short_cell_IDs_in_one_crossing", 1),
        ("canonical_crossing_scale_audit", "single_canonical_parent_W_ID_can_be_a_transverse_crossing", True),
        ("canonical_crossing_scale_audit", "round44_long_canonical_parent_W_wording", "UNCHANGED"),
        ("cross_cell_weight_nonimplication", "per_cell_density_ratio", "2"),
        ("cross_cell_weight_nonimplication", "family_is_proper", False),
        ("cross_cell_weight_nonimplication", "geometric_extended_parent_crosses_C24", False),
        ("cross_cell_weight_nonimplication", "C24_hit_mass", "1"),
        ("extended_parent_bundle_minorization_interface", "cellwise_ratio_cannot_be_used_as_R_ext", False),
        ("extended_parent_bundle_minorization_interface", "numeric_R_ext", "2000/1999"),
        ("extended_parent_bundle_minorization_interface", "numeric_H_cover", 1),
        ("extended_parent_bundle_minorization_interface", "numeric_beta", "1/2"),
        ("shortest_numeric_frontier", "post_C24_cut_same_proper_class_return", "CERTIFIED"),
        ("shortest_numeric_frontier", "numeric_proper_family_C24_minorization", "CERTIFIED"),
    ]
    for section, key, value in edits:
        mutation = copy.deepcopy(source)
        mutation["result"][section][key] = value
        mutations.append(mutation)
    for key, value in (
        ("one_crossing_pair_hit_fraction_strict_lower", "1"),
        ("required_beta_strict_lower", "0"),
        ("safe_reciprocal_beta", "1"),
        ("next_reciprocal_fails", "1"),
    ):
        mutation = copy.deepcopy(source)
        mutation["result"]["extended_parent_bundle_minorization_interface"][
            "hypothetical_only_if_R_ext_equals_2000_over_1999"
        ][key] = value
        mutations.append(mutation)
    for key, value in (
        ("single_canonical_short_cell_covering_route", "CERTIFIED"),
        ("extended_parent_bundle_registry", "CERTIFIED"),
        ("cross_cell_density_weight_continuation", "CERTIFIED"),
        ("numeric_proper_family_C24_minorization", "CERTIFIED"),
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
