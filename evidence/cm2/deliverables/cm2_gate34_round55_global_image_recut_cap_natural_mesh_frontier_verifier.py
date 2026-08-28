#!/usr/bin/env python3
"""Independent verifier for the Round-55 image-recut-cap frontier leaf."""

from __future__ import annotations

import argparse
import ast
import copy
import hashlib
import json
from fractions import Fraction as Q
from pathlib import Path
from typing import Any

import cm2_gate34_round55_global_image_recut_cap_natural_mesh_frontier_cert as cert


HERE = Path(__file__).resolve().parent
DEFAULT_MANIFEST = cert.DEFAULT_MANIFEST
EXPECTED_SCHEMA = cert.MANIFEST_SCHEMA


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def strict_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate key: {key}")
        result[key] = value
    return result


def reject_constant(token: str) -> None:
    raise ValueError(f"non-finite JSON constant: {token}")


def strict_load_bytes(raw: bytes) -> dict[str, Any]:
    value = json.loads(
        raw.decode("utf-8"),
        object_pairs_hook=strict_object,
        parse_constant=reject_constant,
    )
    if not isinstance(value, dict):
        raise ValueError("manifest root")
    return value


def safe_manifest_path(path: Path) -> Path:
    resolved = path.resolve()
    if not path.is_file() or path.is_symlink() or resolved.parent != HERE:
        raise ValueError("unsafe manifest path")
    return resolved


def q(value: str) -> Q:
    return Q(value)


def get_path(value: dict[str, Any], path: tuple[str, ...]) -> Any:
    current: Any = value
    for key in path:
        if not isinstance(current, dict) or key not in current:
            raise ValueError("missing path: " + "/".join(path))
        current = current[key]
    return current


def independent_arithmetic(result: dict[str, Any]) -> None:
    cap = result["global_connected_image_recut_cap"]
    euclidean = q(cap["Euclidean_length_strict_upper"])
    metric = q(cap["adapted_over_Euclidean_strict_upper"])
    adapted = q(cap["adapted_length_strict_upper"])
    delta = q(cap["deterministic_adapted_recut_scale"])
    count = int(cap["uniform_image_recut_count_upper"])
    if euclidean != 68 or metric != Q(141, 4):
        raise ValueError("length inputs")
    if euclidean * metric != adapted or adapted != 2397:
        raise ValueError("adapted length cap")
    if delta != Q(1, 10**90):
        raise ValueError("recut scale")
    if count != 2397 * 10**90 + 1:
        raise ValueError("recut count")
    if not cap["rank_path_derivative_product_used"] is False:
        raise ValueError("product nonuse")

    lemma = result["density_ratio_refinement_lemma"]
    ratio = q(lemma["registered_density_ratio"])
    multiplier = q(lemma["registered_image_refinement_multiplier"])
    if ratio != Q(2000, 1999):
        raise ValueError("density ratio")
    if multiplier != ratio * count:
        raise ValueError("refinement multiplier")
    if lemma["refinement_inequality"] != "sum_j p_j/ell_j<=R*N*p/ell(W)":
        raise ValueError("refinement statement")
    samples = lemma["sample_rows"]
    expected_counts = [1, 2, 8, 128, count]
    if [int(row["cell_count_N"]) for row in samples] != expected_counts:
        raise ValueError("sample counts")
    for row, n in zip(samples, expected_counts, strict=True):
        if q(row["density_ratio_R"]) != ratio:
            raise ValueError("sample ratio")
        if q(row["refined_over_coarse_Z_multiplier_upper"]) != ratio * n:
            raise ValueError("sample multiplier")
    if cert.digest(samples) != lemma["sample_rows_sha256"]:
        raise ValueError("sample digest")

    frontier = result["natural_delta_B_mesh_frontier"]
    if frontier["exact_parity_bound"] != "delta_B^(-1)<=4*2^(3B/2)":
        raise ValueError("natural parity bound")
    expected_B = [14, 15, 16, 31, 64, 65]
    rows = frontier["sample_rows"]
    if [row["B"] for row in rows] != expected_B:
        raise ValueError("natural rows")
    for row, B in zip(rows, expected_B, strict=True):
        exponent = (3 * (B + 1) + 1) // 2
        inv = 1 << exponent
        square_ratio = Q(inv * inv, 1 << (3 * B))
        if row["mesh_exponent_ceil_3Bplus3_over_2"] != exponent:
            raise ValueError("mesh exponent")
        if q(row["delta_B"]) != Q(1, inv):
            raise ValueError("mesh scale")
        if q(row["delta_B_inverse_squared_over_2_to_3B"]) != square_ratio:
            raise ValueError("mesh square ratio")
        if square_ratio not in {Q(8), Q(16)} or square_ratio > 16:
            raise ValueError("mesh parity arithmetic")
    if cert.digest(rows) != frontier["sample_rows_sha256"]:
        raise ValueError("natural row digest")
    joins = frontier["three_unpinned_physical_joins"]
    if [row["id"] for row in joins] != [
        "path_rank_aggregation",
        "metric_alignment",
        "same_ID_canonical_atom",
    ]:
        raise ValueError("frontier IDs")
    if any(row["status"] != "NOT_CERTIFIED" for row in joins):
        raise ValueError("frontier promotion")
    if q(frontier["available_global_collision_q0_moment_strict_upper"]) != Q(
        134217735, 64
    ):
        raise ValueError("q0 moment")

    separator = result["round36_separator_retyping"]
    if separator["round36_manifest_sha256"] != cert.DEPENDENCIES[
        "cm2-gate45-round36-aggregate-z-route-manifest-2026-07-19.json"
    ]:
        raise ValueError("separator SHA")
    if separator["countermodel_still_valid_for_its_installed_fields"] is not True:
        raise ValueError("separator validity")
    if separator["countermodel_disproves_global_connected_length_cap"] is not False:
        raise ValueError("separator scope")


def nonpromotion_guard(result: dict[str, Any]) -> None:
    strict = result["strict_nonpromotion"]
    required = {
        "global_connected_image_recut_count_cap": "CERTIFIED",
        "image_recut_derivative_product_required": False,
        "density_ratio_refinement_lemma": "CERTIFIED_CONDITIONAL",
        "natural_mesh_path_rank_aggregation": "NOT_CERTIFIED",
        "natural_mesh_metric_alignment": "NOT_CERTIFIED",
        "natural_mesh_same_ID_canonical_atom_join": "NOT_CERTIFIED",
        "coarse_terminal_Z_l1": "NOT_CERTIFIED_BY_THIS_LEAF",
        "terminal_cell_refinement_to_J_pair": "NOT_CERTIFIED",
        "physical_J_pair": "NOT_CERTIFIED",
        "physical_I_D": "NOT_CERTIFIED",
        "complete_numeric_C_fw_C_rev": "NOT_CERTIFIED",
        "final_same_ID_q": "NOT_CERTIFIED",
        "strong_cemetery": "NOT_CERTIFIED",
        "Gate4": "NOT_CERTIFIED",
        "Gate5": "NOT_CERTIFIED",
        "complete_composite_gates": "0/5",
        "CM2": "NO-GO_FOR_CLAIM",
    }
    if strict != required:
        raise ValueError("strict nonpromotion map")
    if result["natural_delta_B_mesh_frontier"]["physical_J_pair"] != "NOT_CERTIFIED":
        raise ValueError("natural frontier J_pair")


def ast_guard() -> None:
    source = Path(cert.__file__).resolve().read_text(encoding="utf-8")
    tree = ast.parse(source)
    strings = {
        node.value
        for node in ast.walk(tree)
        if isinstance(node, ast.Constant) and isinstance(node.value, str)
    }
    required = {
        "terminal_cell_refinement_to_J_pair",
        "natural_mesh_path_rank_aggregation",
        "physical_J_pair",
        "NO-GO_FOR_CLAIM",
        "REPLACED_BY_FIXED_MULTIPLIER_ONLY",
    }
    if not required.issubset(strings):
        raise ValueError("AST literal guard")
    forbidden = {
        "CERTIFIED_PHYSICAL_J_PAIR",
        "CERTIFIED_GATE4",
        "CM2_CERTIFIED",
    }
    if strings.intersection(forbidden):
        raise ValueError("AST forbidden promotion")


def verify_value(value: dict[str, Any], expected: dict[str, Any]) -> None:
    if value.get("schema") != EXPECTED_SCHEMA:
        raise ValueError("schema")
    if value.get("certificate_sha256") != sha(Path(cert.__file__).resolve()):
        raise ValueError("certificate hash")
    if value.get("verifier_sha256") != sha(Path(__file__).resolve()):
        raise ValueError("verifier hash")
    if value.get("dependencies") != cert.DEPENDENCIES:
        raise ValueError("dependency ledger")
    result = value.get("result")
    if not isinstance(result, dict):
        raise ValueError("result")
    independent_arithmetic(result)
    nonpromotion_guard(result)
    digest_copy = copy.deepcopy(result)
    recorded = digest_copy.pop("internal_replay_digest", None)
    digest_copy["internal_replay_digest"] = recorded
    # Rebuild exactly as the certificate does: digest is over the result before
    # the digest key is inserted.
    without_digest = copy.deepcopy(result)
    without_digest.pop("internal_replay_digest", None)
    if recorded != cert.digest(without_digest):
        raise ValueError("internal replay digest")
    if value.get("verdict") != result["strict_nonpromotion"]:
        raise ValueError("verdict/result mismatch")
    if value != expected:
        raise ValueError("deterministic semantic replay")
    ast_guard()


def verify_manifest(path: Path) -> tuple[dict[str, Any], bytes, bytes]:
    resolved = safe_manifest_path(path)
    raw = resolved.read_bytes()
    value = strict_load_bytes(raw)
    expected = cert.build_manifest(Path(__file__).resolve())
    verify_value(value, expected)
    reemitted = json.dumps(expected, indent=2, sort_keys=True).encode("utf-8") + b"\n"
    return value, raw, reemitted


def expect_reject(value: dict[str, Any], expected: dict[str, Any]) -> bool:
    try:
        verify_value(value, expected)
    except Exception:
        return True
    return False


def hostile_self_test(path: Path) -> int:
    baseline, raw, _ = verify_manifest(path)
    expected = cert.build_manifest(Path(__file__).resolve())
    mutations: list[dict[str, Any]] = []

    def mutate(keys: tuple[str, ...], replacement: Any) -> None:
        item = copy.deepcopy(baseline)
        cursor: Any = item
        for key in keys[:-1]:
            cursor = cursor[key]
        cursor[keys[-1]] = replacement
        mutations.append(item)

    mutate(("schema",), "cm2.bad")
    mutate(("certificate_sha256",), "0" * 64)
    mutate(("verifier_sha256",), "0" * 64)
    bad_deps = copy.deepcopy(baseline["dependencies"])
    first_dep = next(iter(bad_deps))
    bad_deps[first_dep] = "0" * 64
    mutate(("dependencies",), bad_deps)
    mutate(("result", "global_connected_image_recut_cap", "Euclidean_length_strict_upper"), "69")
    mutate(("result", "global_connected_image_recut_cap", "adapted_over_Euclidean_strict_upper"), "36")
    mutate(("result", "global_connected_image_recut_cap", "adapted_length_strict_upper"), "2398")
    mutate(("result", "global_connected_image_recut_cap", "uniform_image_recut_count_upper"), str(2397 * 10**90 + 2))
    mutate(("result", "global_connected_image_recut_cap", "rank_path_derivative_product_used"), True)
    mutate(("result", "density_ratio_refinement_lemma", "registered_density_ratio"), "1")
    mutate(("result", "density_ratio_refinement_lemma", "refinement_inequality"), "false")
    mutate(("result", "density_ratio_refinement_lemma", "registered_image_refinement_multiplier"), "1")
    mutate(("result", "natural_delta_B_mesh_frontier", "exact_parity_bound"), "false")
    mutate(("result", "natural_delta_B_mesh_frontier", "physical_J_pair"), "CERTIFIED")
    mutate(("result", "natural_delta_B_mesh_frontier", "three_unpinned_physical_joins"), [])
    mutate(("result", "round36_separator_retyping", "countermodel_still_valid_for_its_installed_fields"), False)
    mutate(("result", "round36_separator_retyping", "countermodel_disproves_global_connected_length_cap"), True)
    mutate(("result", "strict_nonpromotion", "natural_mesh_path_rank_aggregation"), "CERTIFIED")
    mutate(("result", "strict_nonpromotion", "terminal_cell_refinement_to_J_pair"), "CERTIFIED")
    mutate(("result", "strict_nonpromotion", "physical_J_pair"), "CERTIFIED")
    mutate(("result", "strict_nonpromotion", "physical_I_D"), "CERTIFIED")
    mutate(("result", "strict_nonpromotion", "Gate4"), "CERTIFIED")
    mutate(("result", "strict_nonpromotion", "CM2"), "CERTIFIED")
    mutate(("verdict", "physical_J_pair"), "CERTIFIED")
    mutate(("result", "internal_replay_digest"), "0" * 64)

    rejected = sum(expect_reject(item, expected) for item in mutations)
    duplicate_raw = raw.replace(b'{\n  "certificate_sha256"', b'{\n  "schema": "duplicate",\n  "certificate_sha256"', 1)
    nonfinite_raw = raw.replace(b'"Euclidean_length_strict_upper": "68"', b'"Euclidean_length_strict_upper": NaN', 1)
    for bad_raw in [duplicate_raw, nonfinite_raw]:
        try:
            strict_load_bytes(bad_raw)
        except Exception:
            rejected += 1
    total = len(mutations) + 2
    if rejected != total:
        raise ValueError(f"hostile rejection count {rejected}/{total}")
    return total


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("manifest", nargs="?", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--verify", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--reemit", action="store_true")
    args = parser.parse_args()

    if args.self_test:
        total = hostile_self_test(args.manifest)
        print(f"HOSTILE_MUTATIONS_REJECTED: {total}/{total}")
        return 0
    if args.verify or args.reemit:
        _, raw, reemitted = verify_manifest(args.manifest)
        if args.reemit:
            if raw != reemitted:
                raise ValueError("re-emission differs")
            print("REEMIT_BYTE_IDENTICAL: PASS")
        else:
            print("AUDIT_MODE: PASS")
        return 0

    print("GLOBAL_IMAGE_RECUT_CAP: CERTIFIED")
    print("NATURAL_MESH_JOIN: NOT_CERTIFIED")
    print("PHYSICAL_J_PAIR: NOT_CERTIFIED")
    print("CM2: NO-GO_FOR_CLAIM")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
