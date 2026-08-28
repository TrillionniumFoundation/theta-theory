#!/usr/bin/env python3
"""Verifier for the Round-46 Piola F16 certificate."""

from __future__ import annotations

import argparse
import copy
import json
import tempfile
from pathlib import Path
from typing import Any

import cm2_gate5_round46_piola_f16_frontier_cert as cert


def strict_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate key: {key}")
        result[key] = value
    return result


def read(path: Path) -> dict[str, Any]:
    value = json.loads(
        path.read_text(encoding="utf-8"), object_pairs_hook=strict_object
    )
    if not isinstance(value, dict):
        raise ValueError("manifest root")
    return value


def verify(path: Path) -> list[str]:
    errors: list[str] = []
    try:
        if not path.is_file() or path.is_symlink():
            return ["unsafe manifest"]
        source = read(path)
        if source.get("schema") != cert.MANIFEST_SCHEMA:
            errors.append("manifest schema")
        if source.get("certificate_sha256") != cert.sha(Path(cert.__file__).resolve()):
            errors.append("certificate hash")
        if source.get("verifier_sha256") != cert.sha(Path(__file__).resolve()):
            errors.append("verifier hash")
        if source.get("dependencies") != cert.DEPENDENCIES:
            errors.append("dependencies")
        replay = cert.build_result()
        if source.get("result") != replay:
            errors.append("result replay")
        if source.get("verdict") != replay["strict_nonpromotion"]:
            errors.append("verdict replay")

        result = source.get("result", {})
        piola = result.get("area_preserving_Piola_flux_identity", {})
        if piola.get("matrix_identity") != "DS^T cof(DS)=det(DS) I=I":
            errors.append("Piola matrix identity")
        if piola.get("suffix_derivative_multiplier") != "1":
            errors.append("suffix multiplier")
        if piola.get("status") != "CERTIFIED_EXACT_PIOLA_CANCELLATION":
            errors.append("Piola status")
        rows = piola.get("sample_rows", [])
        if len(rows) != 10:
            errors.append("Piola samples")
        if piola.get("sample_rows_sha256") != cert.digest(rows):
            errors.append("Piola sample digest")

        f16 = result.get("all_face_arbitrary_suffix_F16", {})
        if f16.get("all_five_physical_face_grammars_covered") is not True:
            errors.append("five-face F16")
        if f16.get("nonempty_suffix_derivative_product_used") is not False:
            errors.append("derivative product")
        if f16.get("flux_face_operator_cost") != "CERTIFIED":
            errors.append("F16 operator cost")
        if f16.get("status") != "CERTIFIED_ALL_FACE_ARBITRARY_SUFFIX_F16":
            errors.append("F16 status")
        frontier = result.get("corrected_strong_frontier", {})
        if frontier.get("cemetery_compatible_F16") != "NOT_CERTIFIED":
            errors.append("cemetery F16 overclaim")
        maturity = result.get("Gate5_maturity_update", {})
        if maturity.get("current_global_maturity") != "10/18":
            errors.append("maturity")
        if maturity.get("complete_18_field_operator_block_count") != 0:
            errors.append("complete block overclaim")
        strict = result.get("strict_nonpromotion", {})
        expected = {
            "all_five_face_arbitrary_suffix_F16": "CERTIFIED",
            "complete_strong_F13_intertwiner": "NOT_CERTIFIED",
            "cemetery_compatible_F16": "NOT_CERTIFIED",
            "complete_all_face_F10": "NOT_CERTIFIED",
            "F14_F15_F17_F18": "NOT_CERTIFIED",
            "dynamic_MT_DQ": "NOT_CERTIFIED",
            "strong_cemetery": "NOT_CERTIFIED",
            "Gate3": "NOT_CERTIFIED",
            "Gate5_maturity": "10/18",
            "complete_18_field_operator_block_count": 0,
            "Gate5": "NOT_CERTIFIED",
            "complete_composite_gates": "0/5",
            "CM2": "NO-GO_FOR_CLAIM",
        }
        if strict != expected:
            errors.append("strict nonpromotion")
    except Exception as exc:
        errors.append(f"exception: {exc}")
    return errors


def set_path(value: dict[str, Any], path: tuple[str, ...], replacement: Any) -> None:
    cursor: Any = value
    for key in path[:-1]:
        cursor = cursor[key]
    cursor[path[-1]] = replacement


def self_test(path: Path) -> tuple[int, int]:
    source = read(path)
    changes: list[tuple[tuple[str, ...], Any]] = [
        (("result", "schema"), "bad"),
        (("result", "internal_replay_digest"), "0" * 64),
        (("result", "provenance", "path_scope"), "empty suffix"),
        (("result", "area_preserving_Piola_flux_identity", "regular_suffix_branch"), "singular"),
        (("result", "area_preserving_Piola_flux_identity", "area_Jacobian"), "det(DS)=2"),
        (("result", "area_preserving_Piola_flux_identity", "current_pushforward"), "J_prime=J"),
        (("result", "area_preserving_Piola_flux_identity", "normal_measure_pushforward"), "n_prime=n"),
        (("result", "area_preserving_Piola_flux_identity", "matrix_identity"), "DS cof(DS)=I"),
        (("result", "area_preserving_Piola_flux_identity", "pointwise_flux_identity"), "false"),
        (("result", "area_preserving_Piola_flux_identity", "weighted_pairing_identity"), "false"),
        (("result", "area_preserving_Piola_flux_identity", "test_bound"), "needs D_suffix"),
        (("result", "area_preserving_Piola_flux_identity", "suffix_derivative_multiplier"), "2"),
        (("result", "area_preserving_Piola_flux_identity", "artificial_cut_policy"), "absolute first"),
        (("result", "area_preserving_Piola_flux_identity", "sample_rows_sha256"), "0" * 64),
        (("result", "area_preserving_Piola_flux_identity", "status"), "NOT_CERTIFIED"),
        (("result", "all_face_arbitrary_suffix_F16", "path_scope"), "depth one"),
        (("result", "all_face_arbitrary_suffix_F16", "all_five_physical_face_grammars_covered"), False),
        (("result", "all_face_arbitrary_suffix_F16", "same_ID_slot_token"), "bad"),
        (("result", "all_face_arbitrary_suffix_F16", "source_flux_input"), "none"),
        (("result", "all_face_arbitrary_suffix_F16", "suffix_transport"), "raw derivative"),
        (("result", "all_face_arbitrary_suffix_F16", "nonempty_suffix_derivative_product_used"), True),
        (("result", "all_face_arbitrary_suffix_F16", "pointwise_charge_bounds"), ["c_F16=infinity"]),
        (("result", "all_face_arbitrary_suffix_F16", "physical_L6over5_moment"), "NOT_CERTIFIED"),
        (("result", "all_face_arbitrary_suffix_F16", "physical_weighted_tail", "inherited_block_exponent"), "0"),
        (("result", "all_face_arbitrary_suffix_F16", "physical_weighted_tail", "collision_time_rate_numeric"), True),
        (("result", "all_face_arbitrary_suffix_F16", "physical_weighted_tail", "status"), "NOT_CERTIFIED"),
        (("result", "all_face_arbitrary_suffix_F16", "flux_face_operator_cost"), "NOT_CERTIFIED"),
        (("result", "all_face_arbitrary_suffix_F16", "status"), "NOT_CERTIFIED"),
        (("result", "corrected_strong_frontier", "round45_naive_majorant"), "sharp"),
        (("result", "corrected_strong_frontier", "round45_moment_countermodel_status"), "false"),
        (("result", "corrected_strong_frontier", "newly_removed_obstruction"), "none"),
        (("result", "corrected_strong_frontier", "complete_strong_F13_intertwiner"), "CERTIFIED"),
        (("result", "corrected_strong_frontier", "cemetery_compatible_F16"), "CERTIFIED"),
        (("result", "corrected_strong_frontier", "full_all_face_F10"), "CERTIFIED"),
        (("result", "Gate5_maturity_update", "newly_completed_parameterized_field"), "F15"),
        (("result", "Gate5_maturity_update", "current_global_maturity"), "18/18"),
        (("result", "Gate5_maturity_update", "complete_18_field_operator_block_count"), 1),
        (("result", "strict_nonpromotion", "cemetery_compatible_F16"), "CERTIFIED"),
        (("result", "strict_nonpromotion", "Gate5"), "CERTIFIED"),
        (("result", "strict_nonpromotion", "CM2"), "GO"),
        (("verdict", "dynamic_MT_DQ"), "CERTIFIED"),
    ]
    mutations: list[dict[str, Any]] = []
    for path_keys, replacement in changes:
        mutation = copy.deepcopy(source)
        set_path(mutation, path_keys, replacement)
        mutations.append(mutation)

    row_mutation = copy.deepcopy(source)
    row_mutation["result"]["area_preserving_Piola_flux_identity"]["sample_rows"][0][
        "pushed_flux"
    ] = "999"
    mutations.append(row_mutation)

    for key, replacement in (
        ("certificate_sha256", "0" * 64),
        ("verifier_sha256", "0" * 64),
        ("dependencies", {}),
    ):
        mutation = copy.deepcopy(source)
        mutation[key] = replacement
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

