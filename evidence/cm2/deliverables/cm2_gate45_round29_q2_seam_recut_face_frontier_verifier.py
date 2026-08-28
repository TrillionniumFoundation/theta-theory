#!/usr/bin/env python3
"""Fail-closed verifier for the round-29 Q2 seam/instance frontier leaf."""

from __future__ import annotations

import argparse
import copy
import hashlib
import importlib.util
import json
import sys
from fractions import Fraction
from pathlib import Path
from types import ModuleType
from typing import Any, Callable


Q = Fraction
HERE = Path(__file__).resolve().parent
DEFAULT_MANIFEST = HERE / "cm2-gate45-round29-q2-seam-recut-face-frontier-manifest-2026-07-18.json"
CERTIFICATE = HERE / "cm2_gate45_round29_q2_seam_recut_face_frontier_cert.py"
VERIFIER = Path(__file__).resolve()
MANIFEST_SCHEMA = "cm2.gate45.round29-q2-seam-recut-face-frontier.manifest.v1"
RESULT_SCHEMA = "cm2.gate45.round29-q2-seam-recut-face-frontier.v1"


class DuplicateKeyError(ValueError):
    pass


def no_duplicate_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise DuplicateKeyError(key)
        result[key] = value
    return result


def parse_json_text(text: str) -> Any:
    return json.loads(
        text,
        object_pairs_hook=no_duplicate_pairs,
        parse_constant=lambda token: (_ for _ in ()).throw(
            ValueError(f"non-finite JSON constant: {token}")
        ),
    )


def load_json(path: Path) -> dict[str, Any]:
    value = parse_json_text(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError("manifest root is not an object")
    return value


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def sha256_path(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def exact_keys(value: Any, expected: set[str]) -> bool:
    return isinstance(value, dict) and set(value) == expected


def is_digest(value: Any) -> bool:
    return (
        isinstance(value, str)
        and len(value) == 64
        and all(char in "0123456789abcdef" for char in value)
    )


def load_certificate() -> ModuleType:
    spec = importlib.util.spec_from_file_location("round29_q2_frontier_cert", CERTIFICATE)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot import certificate")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def validate(data: dict[str, Any], *, integrity: bool) -> list[str]:
    errors: list[str] = []
    try:
        cert = load_certificate()
    except Exception as exc:  # fail closed
        return [f"certificate import: {exc}"]
    top = {"schema", "certificate_sha256", "verifier_sha256", "dependencies", "result", "verdict"}
    if not exact_keys(data, top):
        errors.append("top-level key set")
    if data.get("schema") != MANIFEST_SCHEMA:
        errors.append("manifest schema")
    if data.get("certificate_sha256") != sha256_path(CERTIFICATE):
        errors.append("certificate hash field")
    if data.get("verifier_sha256") != sha256_path(VERIFIER):
        errors.append("verifier hash field")
    if canonical_json(data.get("dependencies")) != canonical_json(cert.DEPENDENCIES):
        errors.append("dependency table")
    if integrity:
        for name, expected in cert.DEPENDENCIES.items():
            path = HERE / name
            if not path.is_file() or path.is_symlink() or path.resolve().parent != HERE:
                errors.append(f"unsafe dependency: {name}")
            elif sha256_path(path) != expected:
                errors.append(f"dependency hash: {name}")

    result = data.get("result")
    expected_result_keys = {
        "schema",
        "provenance",
        "Q2_time2_target_chart_seam_refinement",
        "Q2_actual_parent_W_recut_instance_frontier",
        "Q2_terminal_C24_face_empty_family_ledger",
        "Gate5_frontier",
    }
    if not exact_keys(result, expected_result_keys):
        errors.append("result key set")
        return errors
    assert isinstance(result, dict)
    if result.get("schema") != RESULT_SCHEMA:
        errors.append("result schema")
    provenance = result.get("provenance", {})
    if provenance.get("old_artifacts_modified") is not False:
        errors.append("old artifacts")
    if provenance.get("replay_engine") != "fresh complete 384-bit Arb time-two recursion plus depth-6 fair seam refinement":
        errors.append("replay engine")
    if canonical_json(provenance.get("dependency_sha256")) != canonical_json(cert.DEPENDENCIES):
        errors.append("provenance dependency table")

    seam = result.get("Q2_time2_target_chart_seam_refinement", {})
    for key, expected in {
        "precision_bits": 384,
        "original_strict_Q2_atom_count": 114006,
        "original_strict_single_chart_Q2_atom_count": 108726,
        "original_seam_frontier_parent_count": 5280,
        "maximum_additional_fair_dyadic_depth": 6,
        "mass_identity_resolved_plus_residual_equals_original_seam_mass": True,
        "residual_mass_strictly_less_than_original_seam_mass": True,
        "finite_refinement_claimed_as_complete_chart_atlas": False,
        "representation_seam_claimed_as_physical_cut": False,
    }.items():
        if seam.get(key) != expected or type(seam.get(key)) is not type(expected):
            errors.append(f"seam: {key}")
    histogram = seam.get("refined_classification_histogram", {})
    resolved = seam.get("resolved_strict_single_chart_child_count")
    residual = seam.get("residual_representation_seam_outer_count")
    terminal = seam.get("refined_terminal_cell_count")
    if not all(type(value) is int and value > 0 for value in (resolved, residual, terminal)):
        errors.append("seam positive counts")
    elif histogram != {
        "RESIDUAL_REPRESENTATION_SEAM_OUTER": residual,
        "RESOLVED_STRICT_SINGLE_CHART": resolved,
    } or resolved + residual != terminal:
        errors.append("seam count identity")
    depths = seam.get("refined_additional_depth_histogram", {})
    if not isinstance(depths, dict) or sum(depths.values()) != terminal:
        errors.append("seam depth histogram")
    elif any(not key.isdigit() or int(key) > 6 for key in depths):
        errors.append("seam depth range")
    charts = seam.get("refined_target_chart_histogram", {})
    if not isinstance(charts, dict) or sum(charts.values()) != terminal:
        errors.append("seam chart histogram")
    elif charts.get("UNRESOLVED_REPRESENTATION_SEAM") != residual:
        errors.append("seam unresolved chart count")
    try:
        source_mass = Q(seam.get("original_seam_frontier_base_mass"))
        resolved_mass = Q(seam.get("resolved_base_mass"))
        residual_mass = Q(seam.get("residual_base_mass"))
        if not (0 < residual_mass < source_mass and resolved_mass > 0):
            errors.append("seam mass positivity")
        if resolved_mass + residual_mass != source_mass:
            errors.append("seam mass identity")
    except Exception:
        errors.append("seam mass parse")
    if seam.get("original_plus_refined_strict_single_chart_cell_count") != 108726 + (resolved or 0):
        errors.append("seam strict total")
    for key in ("refined_cell_ids_sha256", "refined_rows_sha256"):
        if not is_digest(seam.get(key)):
            errors.append(f"seam digest: {key}")
    reps = seam.get("representative_rows")
    if not isinstance(reps, list) or len(reps) != 4:
        errors.append("seam representatives")

    recut = result.get("Q2_actual_parent_W_recut_instance_frontier", {})
    for key, expected in {
        "canonical_recut_branch_rule_count": 228012,
        "actual_parent_W_registry_count_in_frozen_dependencies": 0,
        "actual_curve_recut_instance_id_count": 0,
        "branch_rule_retyped_as_actual_curve_instance": False,
        "F7_characteristic_Z_instance_charge_count": 0,
    }.items():
        if recut.get(key) != expected or type(recut.get(key)) is not type(expected):
            errors.append(f"recut: {key}")
    if recut.get("required_instance_key") != "(branch-rule-id,parent-canonical-W-id,natural-index-j)":
        errors.append("recut instance key")

    faces = result.get("Q2_terminal_C24_face_empty_family_ledger", {})
    for key, expected in {
        "strict_Q2_inner_atom_count": 114006,
        "obstacle_compatible_terminal_core_face_family_count_per_atom": 48,
        "atom_terminal_face_family_pair_count": 5472288,
        "nonempty_terminal_core_face_piece_count_on_strict_Q2_inner_atoms": 0,
        "certified_empty_pair_count_is_connected_rank_assignment_count": False,
        "carrier_family_retyped_as_connected_face_piece": False,
        "artificial_dyadic_or_chart_seam_retyped_as_physical_face": False,
        "complete_Q2_physical_face_atlas": "NOT_CERTIFIED",
    }.items():
        if faces.get(key) != expected or type(faces.get(key)) is not type(expected):
            errors.append(f"faces: {key}")

    frontier = result.get("Gate5_frontier", {})
    for key, expected in {
        "F4_strict_single_chart_subledger_enlarged": True,
        "F4_complete_Q2_chart_ledger": "NOT_CERTIFIED",
        "F7_materialized_actual_instance_slot_count": 0,
        "F14_through_F18_materialized_slot_count": 0,
        "numeric_transversality_coarea_one_sided_trace_on_nonempty_connected_faces": "NOT_CERTIFIED",
        "complete_18_field_operator_block_count": 0,
        "global_Gate5_maturity": "4/18_UNCHANGED",
        "CM2": "NO-GO_FOR_CLAIM",
    }.items():
        if frontier.get(key) != expected or type(frontier.get(key)) is not type(expected):
            errors.append(f"frontier: {key}")
    expected_verdict = cert.verdict(result)
    if canonical_json(data.get("verdict")) != canonical_json(expected_verdict):
        errors.append("verdict")
    return errors


def set_path(value: dict[str, Any], path: tuple[str, ...], replacement: Any) -> None:
    cursor: Any = value
    for key in path[:-1]:
        cursor = cursor[key]
    cursor[path[-1]] = replacement


def hostile_cases(data: dict[str, Any]) -> list[tuple[str, dict[str, Any]]]:
    cases: list[tuple[str, dict[str, Any]]] = []
    targeted: list[tuple[tuple[str, ...], Any]] = [
        (("schema",), "bad"),
        (("certificate_sha256",), "0" * 64),
        (("verifier_sha256",), "0" * 64),
        (("result", "schema"), "bad"),
        (("result", "provenance", "old_artifacts_modified"), True),
        (("result", "Q2_time2_target_chart_seam_refinement", "precision_bits"), 53),
        (("result", "Q2_time2_target_chart_seam_refinement", "original_strict_Q2_atom_count"), 114005),
        (("result", "Q2_time2_target_chart_seam_refinement", "original_seam_frontier_parent_count"), 5279),
        (("result", "Q2_time2_target_chart_seam_refinement", "residual_mass_strictly_less_than_original_seam_mass"), False),
        (("result", "Q2_actual_parent_W_recut_instance_frontier", "canonical_recut_branch_rule_count"), 228011),
        (("result", "Q2_actual_parent_W_recut_instance_frontier", "actual_curve_recut_instance_id_count"), 1),
        (("result", "Q2_actual_parent_W_recut_instance_frontier", "branch_rule_retyped_as_actual_curve_instance"), True),
        (("result", "Q2_terminal_C24_face_empty_family_ledger", "atom_terminal_face_family_pair_count"), 5472287),
        (("result", "Q2_terminal_C24_face_empty_family_ledger", "carrier_family_retyped_as_connected_face_piece"), True),
        (("result", "Gate5_frontier", "F14_through_F18_materialized_slot_count"), 1),
        (("result", "Gate5_frontier", "CM2"), "CERTIFIED"),
    ]
    for index, (path, replacement) in enumerate(targeted):
        mutant = copy.deepcopy(data)
        set_path(mutant, path, replacement)
        cases.append((f"targeted-{index}", mutant))
    for index in range(80):
        mutant = copy.deepcopy(data)
        mutant[f"hostile_unknown_{index}"] = index
        cases.append((f"unknown-top-key-{index}", mutant))
    return cases


def self_test(data: dict[str, Any]) -> tuple[int, int]:
    cases = hostile_cases(data)
    rejected = sum(bool(validate(mutant, integrity=False)) for _name, mutant in cases)
    return rejected, len(cases)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("manifest", nargs="?", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--integrity", action="store_true")
    parser.add_argument("--replay", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    try:
        data = load_json(args.manifest)
        errors = validate(data, integrity=args.integrity)
        if errors:
            print("FAIL: " + "; ".join(errors), file=sys.stderr)
            return 1
        if args.replay:
            cert = load_certificate()
            replayed = cert.build_result()
            if canonical_json(replayed) != canonical_json(data["result"]):
                print("FAIL: independent replay mismatch", file=sys.stderr)
                return 1
            print("REPLAY: PASS")
        if args.self_test:
            rejected, total = self_test(data)
            print(f"SELF-TEST: {rejected}/{total} hostile mutations rejected")
            if rejected != total:
                return 1
        print("INTEGRITY: PASS" if args.integrity else "STRUCTURE: PASS")
        if args.integrity or args.replay or args.self_test:
            return 0
        print("CM2: NO-GO_FOR_CLAIM")
        return 2
    except Exception as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
