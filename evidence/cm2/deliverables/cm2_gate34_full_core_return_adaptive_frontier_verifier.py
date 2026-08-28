#!/usr/bin/env python3
"""Fail-closed verifier for the full-core adaptive return frontier."""

from __future__ import annotations

import argparse
import copy
import hashlib
import importlib.util
import json
import math
import sys
from collections import Counter
from fractions import Fraction
from pathlib import Path
from types import ModuleType
from typing import Any


Q = Fraction
HERE = Path(__file__).resolve().parent
CERTIFICATE = HERE / "cm2_gate34_full_core_return_adaptive_frontier_cert.py"
DEFAULT_MANIFEST = (
    HERE / "cm2-gate34-full-core-return-adaptive-frontier-manifest-2026-07-18.json"
)
MANIFEST_SCHEMA = "cm2.gate34.full-core-return-adaptive-frontier.manifest.v1"
RESULT_SCHEMA = "cm2.gate34.full-core-return-adaptive-frontier.v1"
EXPECTED_CERTIFICATE_SHA256 = (
    "d18b234471b192282abf064684fa535cc99c205797399b268f052c0884063a24"
)
EXPECTED_DEPENDENCIES = {
    "cm2_gate25_physical_return_core_registry_cert.py": (
        "2da58e5fb5fe030023d6fade7252ec67d0e494708b32d1e32b3ce545e2052fdb"
    ),
    "cm2-gate25-physical-return-core-registry-manifest-2026-07-16.json": (
        "144f5516ada8b83ca07459582c8cdb07ba09db11ac18a90cff32c6396c6e5a42"
    ),
    "cm2_gate3_candidate_first_hit_cert.py": (
        "6d224d74cda186a40ef9956d1dd6556d5a7b9f506d47c942427ceb66fd705bd2"
    ),
    "cm2-gate3-first-hit-atlas-manifest-2026-07-15.json": (
        "0c820a5e3481b2c18fabb14d8d0fab7ce454f9a9e68b856bb2a7bf139404f7f4"
    ),
}

EXPECTED_ROWS_SHA256 = (
    "1cfd4d6f7fdd57034655fd002e370c5c1c80b2da53bff06e4ff3b7c0f8c71209"
)
EXPECTED_SLAB_ROWS_SHA256 = (
    "32f186b0973c5da26dc8a541c29d5df51e0be95d88b1f7267b073123e30109ba"
)
EXPECTED_PARENT_OWNER_SHA256 = (
    "c3042515b4a244b064f1aaef97ee236c5d3f6078a53fe3fb9e865a1976853b2f"
)
EXPECTED_PROMOTED_SHA256 = (
    "3722baee5c967664786447dd9166187ed429aa715948b46133eb6c848510cf4f"
)
EXPECTED_HISTOGRAM = {
    "RETURN_AT_1_INNER": 4216,
    "SURVIVE_THROUGH_1_INNER": 2868,
    "UNRESOLVED_OUTER": 26876,
}
EXPECTED_DEPTH_HISTOGRAM = {
    "0": 8,
    "2": 24,
    "3": 8,
    "4": 32,
    "5": 52,
    "6": 28,
    "7": 44,
    "8": 180,
    "9": 84,
    "10": 320,
    "11": 1608,
    "12": 7296,
    "13": 304,
    "14": 2588,
    "15": 21384,
}


class DuplicateKeyError(ValueError):
    pass


def reject_duplicate_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise DuplicateKeyError(key)
        result[key] = value
    return result


def strict_load(path: Path) -> Any:
    return json.loads(
        path.read_text(encoding="utf-8"),
        object_pairs_hook=reject_duplicate_pairs,
        parse_constant=lambda value: (_ for _ in ()).throw(ValueError(value)),
    )


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def digest(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def sha256_path(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def strict_equal(left: Any, right: Any) -> bool:
    return canonical_json(left) == canonical_json(right)


def result_digest(result: dict[str, Any]) -> str:
    payload = dict(result)
    payload.pop("internal_replay_digest", None)
    return digest(payload)


def load_certificate() -> ModuleType:
    if sys.flags.optimize != 0:
        raise RuntimeError("optimized Python is forbidden")
    if sha256_path(CERTIFICATE) != EXPECTED_CERTIFICATE_SHA256:
        raise RuntimeError("certificate hash mismatch before import")
    for name, expected in EXPECTED_DEPENDENCIES.items():
        path = (HERE / name).resolve()
        if path.parent != HERE or not path.is_file() or path.is_symlink():
            raise RuntimeError(f"unsafe dependency path: {name}")
        if sha256_path(path) != expected:
            raise RuntimeError(f"dependency hash mismatch: {name}")
    spec = importlib.util.spec_from_file_location(
        "cm2_gate34_full_core_return_adaptive_frontier_cert_frozen",
        CERTIFICATE,
    )
    if spec is None or spec.loader is None:
        raise RuntimeError("certificate import spec failure")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    if Path(module.__file__).resolve() != CERTIFICATE.resolve():
        raise RuntimeError("certificate resolved path mismatch")
    if sha256_path(CERTIFICATE) != EXPECTED_CERTIFICATE_SHA256:
        raise RuntimeError("certificate changed during import")
    return module


TOP_KEYS = {
    "schema", "certificate_sha256", "verifier_sha256", "dependencies",
    "result", "verdict",
}
RESULT_KEYS = {
    "schema", "provenance", "adaptive_full_core_step1_registry",
    "adaptive_full_core_step1_raw_leaf_rows",
    "adaptive_full_core_step1_open_parameter_slab_rows",
    "collision_mass_inner_outer_frontier", "strict_nonpromotion",
    "internal_replay_digest",
}
ROW_KEYS = {
    "atom_id", "source_core_id", "dyadic_path", "source_box",
    "source_core_index", "depth",
    "positive_two_dimensional_source_rectangle_at_each_s",
    "positive_parameter_interval", "midpoint_proposal_promoted_parent",
    "strict_next_collision_owner_inherited_from_whole_parent_core",
    "complete_retained_candidate_comparison_inherited",
    "parent_owner_witness_sha256", "classification", "destination_core_id",
    "classification_witness_rows_sha256", "output_enclosures",
    "parameter_averaged_unnormalized_base_mass",
    "parameter_averaged_unnormalized_collision_mass_lower",
    "parameter_averaged_unnormalized_collision_mass_upper",
    "canonical_invariant_area_coordinates",
    "absolute_inverse_invariant_area_Jacobian",
    "log_invariant_area_Jacobian_distortion",
}
SOURCE_BOX_KEYS = {"t", "p", "s"}
ENCLOSURE_KEYS = {"normal_x", "normal_y", "p_target"}
SLAB_KEYS = {
    "slab_index", "open_s_interval", "active_leaf_count",
    "classification_histogram", "return_inner_fixed_s_base_mass",
    "survivor_inner_fixed_s_base_mass", "unresolved_outer_fixed_s_base_mass",
    "full_C24_fixed_s_base_mass",
}


def exact_bool(value: Any) -> bool:
    return type(value) is bool


def valid_sha(value: Any) -> bool:
    return (
        isinstance(value, str)
        and len(value) == 64
        and all(character in "0123456789abcdef" for character in value)
    )


def check_rows(rows: Any) -> list[str]:
    if not isinstance(rows, list) or len(rows) != 33960:
        return ["raw leaf count"]
    errors: list[str] = []
    if digest(rows) != EXPECTED_ROWS_SHA256:
        errors.append("raw leaf digest")
    histogram: Counter[str] = Counter()
    depth_histogram: Counter[int] = Counter()
    ids: set[str] = set()
    by_source: dict[int, list[dict[str, Any]]] = {index: [] for index in range(24)}
    source_core_ids: dict[int, str] = {}
    for row in rows:
        if not isinstance(row, dict) or set(row) != ROW_KEYS:
            errors.append("raw leaf keys")
            return errors
        if type(row["source_core_index"]) is not int or not 0 <= row["source_core_index"] < 24:
            errors.append("source core index")
            return errors
        if type(row["depth"]) is not int or row["depth"] != len(row["dyadic_path"]):
            errors.append("depth/path")
            return errors
        if any(character not in "01" for character in row["dyadic_path"]):
            errors.append("dyadic path alphabet")
            return errors
        if row["depth"] > 15:
            errors.append("depth bound")
            return errors
        if not isinstance(row["source_box"], dict) or set(row["source_box"]) != SOURCE_BOX_KEYS:
            errors.append("source box keys")
            return errors
        try:
            for coordinate in ("t", "p", "s"):
                bounds = row["source_box"][coordinate]
                if not isinstance(bounds, list) or len(bounds) != 2:
                    raise ValueError(coordinate)
                if not Q(bounds[0]) < Q(bounds[1]):
                    raise ValueError(coordinate)
            raw_base = Q(row["parameter_averaged_unnormalized_base_mass"])
            raw_lower = Q(row[
                "parameter_averaged_unnormalized_collision_mass_lower"
            ])
            raw_upper = Q(row[
                "parameter_averaged_unnormalized_collision_mass_upper"
            ])
        except (ValueError, ZeroDivisionError):
            errors.append("rational row payload")
            return errors
        if not (raw_base > 0 and raw_lower == raw_base and raw_upper == Q(1401, 1000) * raw_base):
            errors.append("mass bracket")
            return errors
        for field in (
            "positive_two_dimensional_source_rectangle_at_each_s",
            "positive_parameter_interval",
            "strict_next_collision_owner_inherited_from_whole_parent_core",
            "complete_retained_candidate_comparison_inherited",
        ):
            if row[field] is not True:
                errors.append("strict inherited guard")
                return errors
        if not exact_bool(row["midpoint_proposal_promoted_parent"]):
            errors.append("proposal flag type")
            return errors
        if row["classification"] not in EXPECTED_HISTOGRAM:
            errors.append("classification enum")
            return errors
        if row["classification"] == "RETURN_AT_1_INNER":
            if not isinstance(row["destination_core_id"], str):
                errors.append("return destination")
                return errors
        elif row["destination_core_id"] is not None:
            errors.append("nonreturn destination")
            return errors
        if not valid_sha(row["classification_witness_rows_sha256"]):
            errors.append("witness digest")
            return errors
        if row["parent_owner_witness_sha256"] != EXPECTED_PARENT_OWNER_SHA256 and not valid_sha(row["parent_owner_witness_sha256"]):
            errors.append("parent witness digest")
            return errors
        if row["output_enclosures"] is not None:
            if not isinstance(row["output_enclosures"], dict) or set(row["output_enclosures"]) != ENCLOSURE_KEYS:
                errors.append("output enclosure keys")
                return errors
        if row["canonical_invariant_area_coordinates"] != "(r,p=sin(phi))":
            errors.append("area coordinates")
            return errors
        if row["absolute_inverse_invariant_area_Jacobian"] != "1" or row["log_invariant_area_Jacobian_distortion"] != "0":
            errors.append("area Jacobian seed")
            return errors
        payload = {
            "source_core_id": row["source_core_id"],
            "dyadic_path": row["dyadic_path"],
            "source_box": row["source_box"],
        }
        if row["atom_id"] != "full-core-step1:" + digest(payload):
            errors.append("atom id")
            return errors
        if row["atom_id"] in ids:
            errors.append("duplicate atom id")
            return errors
        ids.add(row["atom_id"])
        index = row["source_core_index"]
        if index in source_core_ids and source_core_ids[index] != row["source_core_id"]:
            errors.append("source core id binding")
            return errors
        source_core_ids[index] = row["source_core_id"]
        by_source[index].append(row)
        histogram[row["classification"]] += 1
        depth_histogram[row["depth"]] += 1
    if dict(sorted(histogram.items())) != EXPECTED_HISTOGRAM:
        errors.append("classification histogram")
    if {str(key): value for key, value in sorted(depth_histogram.items())} != EXPECTED_DEPTH_HISTOGRAM:
        errors.append("depth histogram")
    if len(source_core_ids) != 24:
        errors.append("source core coverage")
    for index, source_rows in by_source.items():
        paths = sorted(row["dyadic_path"] for row in source_rows)
        if any(right.startswith(left) for left, right in zip(paths, paths[1:])):
            errors.append(f"prefix overlap source {index}")
            break
    return errors


def check_slabs(rows: Any) -> list[str]:
    if not isinstance(rows, list) or len(rows) != 32:
        return ["parameter slab count"]
    errors: list[str] = []
    if digest(rows) != EXPECTED_SLAB_ROWS_SHA256:
        errors.append("parameter slab digest")
    for index, row in enumerate(rows):
        if not isinstance(row, dict) or set(row) != SLAB_KEYS:
            errors.append("parameter slab keys")
            return errors
        if type(row["slab_index"]) is not int or row["slab_index"] != index:
            errors.append("parameter slab index")
            return errors
        try:
            s0, s1 = map(Q, row["open_s_interval"])
            masses = [
                Q(row["return_inner_fixed_s_base_mass"]),
                Q(row["survivor_inner_fixed_s_base_mass"]),
                Q(row["unresolved_outer_fixed_s_base_mass"]),
            ]
        except (ValueError, TypeError):
            errors.append("parameter slab rational payload")
            return errors
        if s0 >= s1 or sum(masses) != Q(273, 156250):
            errors.append("parameter slab mass cover")
            return errors
        if row["full_C24_fixed_s_base_mass"] != "273/156250":
            errors.append("parameter slab total")
            return errors
        if type(row["active_leaf_count"]) is not int or row["active_leaf_count"] <= 0:
            errors.append("active leaf count")
            return errors
        histogram = row["classification_histogram"]
        if not isinstance(histogram, dict) or sum(histogram.values()) != row["active_leaf_count"]:
            errors.append("slab histogram")
            return errors
    return errors


def check_registry(registry: Any) -> list[str]:
    if not isinstance(registry, dict):
        return ["registry type"]
    expected = {
        "source_core_count": 24,
        "source_phase_dimension_at_fixed_parameter": 2,
        "parameter_dimension": 1,
        "parameter_window": ["-1/400", "1/400"],
        "base_max_binary_depth": 12,
        "promoted_max_binary_depth": 15,
        "midpoint_search_role": "proposal_only_for_refinement",
        "strict_Arb_admission_only": True,
        "adaptive_leaf_count": 33960,
        "classification_histogram": EXPECTED_HISTOGRAM,
        "depth_histogram": EXPECTED_DEPTH_HISTOGRAM,
        "promoted_depth12_parent_count": 3472,
        "source_core_count_with_positive_return_inner_atom": 16,
        "destination_core_count_hit_by_return_inner_atoms": 16,
        "all_24_parent_branches_have_complete_strict_first_owner_replay": True,
        "all_leaf_source_domains_positive_2D_at_each_parameter": True,
        "all_leaf_parameter_intervals_positive": True,
        "leaf_interiors_pairwise_disjoint": True,
        "leaf_union_covers_C24_times_parameter_modulo_shared_null_faces": True,
        "step1_collision_singular_atom_count": 0,
        "unresolved_atoms_are_only_core_membership_or_chart_boundary_outer_boxes": True,
        "canonical_invariant_area_Jacobian_on_every_regular_leaf": "1",
        "global_dtheta_dt_strict_upper_on_abs_t_le_7_over_10": "1401/1000",
        "parent_owner_rows_sha256": EXPECTED_PARENT_OWNER_SHA256,
        "promoted_parent_ids_sha256": EXPECTED_PROMOTED_SHA256,
        "raw_leaf_rows_sha256": EXPECTED_ROWS_SHA256,
        "finest_open_parameter_slab_count": 32,
        "all_open_parameter_slabs_cover_full_C24": True,
        "all_open_parameter_slabs_have_positive_return_inner": True,
        "parameter_slab_rows_sha256": EXPECTED_SLAB_ROWS_SHA256,
    }
    return [] if strict_equal(registry, expected) else ["registry exact contract"]


def check_mass(mass: Any) -> list[str]:
    expected = {
        "parameter_average_measure": "uniform_ds_on_[-1/400,1/400]",
        "source_collision_density": "R_source/sqrt(1-t^2) dt dp",
        "full_C24_parameter_averaged_unnormalized_base_mass": "273/156250",
        "return_inner_base_mass": "6473/256000000",
        "survivor_inner_base_mass": "123841/80000000",
        "unresolved_outer_base_mass": "44519/256000000",
        "return_inner_normalized_collision_SRB_mass_strict_lower": (
            "45311/11714560000"
        ),
        "unresolved_outer_normalized_collision_SRB_mass_strict_upper": (
            "20790373/532480000000"
        ),
        "return_inner_base_fraction_of_C24": "32365/2236416",
        "survivor_inner_base_fraction_of_C24": "123841/139776",
        "unresolved_outer_base_fraction_of_C24": "222595/2236416",
        "return_inner_base_fraction_strict_lower": "1/70",
        "unresolved_outer_base_fraction_strict_upper": "1/10",
        "return_inner_normalized_mass_strict_lower_benchmark": "1/300000",
        "uniform_all_s_return_inner_base_mass_lower": "711/32000000",
        "uniform_all_s_return_inner_base_fraction_strict_lower": "1/80",
        "uniform_all_s_return_inner_normalized_collision_SRB_mass_lower": (
            "4977/1464320000"
        ),
        "uniform_all_s_return_inner_normalized_mass_strict_lower_benchmark": (
            "1/400000"
        ),
        "dyadic_s_boundary_policy": (
            "choose_either_adjacent_closed_leaf_partition; strict box admission "
            "includes the shared parameter endpoint"
        ),
        "C24_normalized_collision_SRB_mass_strict_upper": "29021/75000000",
        "C24_normalized_mass_strict_upper_benchmark": "1/2500",
        "uniform_all_s_muC_first_return_at_1_probability_strict_lower": (
            "9331875/1062400768"
        ),
        "uniform_all_s_muC_first_return_at_1_probability_benchmark": "1/160",
        "immediate_return_probability_is_unconditional_at_time_0_not_survivor_conditioned": True,
        "base_mass_identity_return_plus_survivor_plus_unresolved": True,
        "true_R1_is_contained_in_return_inner_union_unresolved_outer_mod_null": True,
        "true_Q1_is_contained_in_survivor_inner_union_unresolved_outer_mod_null": True,
    }
    return [] if strict_equal(mass, expected) else ["mass frontier exact contract"]


def expected_scope() -> dict[str, Any]:
    return {
        "one_step_return_inner_operator_R1_nonzero": "CERTIFIED",
        "one_step_survivor_inner_operator_Q1_nonzero": "CERTIFIED",
        "full_step1_R1_Q1_partition_without_unresolved_cover": "NOT_CERTIFIED",
        "finite_or_infinite_full_return_partition": "NOT_CERTIFIED",
        "unweighted_exponential_return_tail": "NOT_CERTIFIED",
        "q_weighted_strong_return_tail": "NOT_CERTIFIED",
        "induced_strong_Lasota_Yorke_coefficient": "NOT_CERTIFIED",
        "common_forward_reverse_restriction": "NOT_CERTIFIED",
        "Gate3": "NOT_CERTIFIED",
        "Gate4": "NOT_CERTIFIED",
        "Gate5": "NOT_CERTIFIED",
    }


def expected_verdict() -> dict[str, Any]:
    return {
        "full_24_core_times_parameter_adaptive_cover": "CERTIFIED_MOD_NULL_FACES",
        "positive_full_dimensional_R1_inner_branches": "CERTIFIED",
        "strict_full_dimensional_Q1_survivor_inner_branches": "CERTIFIED",
        "uniform_all_s_muC_first_return_at_1_probability_gt_1_over_160": (
            "CERTIFIED"
        ),
        "step1_collision_singular_cemetery": "EMPTY_ON_FROZEN_PARENT_BRANCHES",
        "unresolved_step1_outer_cover": "NONEMPTY",
        "complete_Rn_Qn_first_return_partition": "NOT_CERTIFIED",
        "physical_exponential_return_tail": "NOT_CERTIFIED",
        "induced_strong_operator": "NOT_CERTIFIED",
        "Gate3": "NOT_CERTIFIED",
        "Gate4": "NOT_CERTIFIED",
        "Gate5": "NOT_CERTIFIED",
    }


def check(manifest: Any) -> list[str]:
    if not isinstance(manifest, dict):
        return ["manifest type"]
    errors: list[str] = []
    if set(manifest) != TOP_KEYS:
        errors.append("manifest keys")
    if manifest.get("schema") != MANIFEST_SCHEMA:
        errors.append("manifest schema")
    if manifest.get("certificate_sha256") != EXPECTED_CERTIFICATE_SHA256:
        errors.append("certificate hash field")
    if sha256_path(CERTIFICATE) != EXPECTED_CERTIFICATE_SHA256:
        errors.append("certificate hash on disk")
    if manifest.get("verifier_sha256") != sha256_path(Path(__file__).resolve()):
        errors.append("verifier hash")
    if not strict_equal(manifest.get("dependencies"), EXPECTED_DEPENDENCIES):
        errors.append("dependency table")
    result = manifest.get("result")
    if not isinstance(result, dict):
        return errors + ["result type"]
    if set(result) != RESULT_KEYS:
        errors.append("result keys")
    if result.get("schema") != RESULT_SCHEMA:
        errors.append("result schema")
    if result.get("internal_replay_digest") != result_digest(result):
        errors.append("internal replay digest")
    provenance = result.get("provenance")
    expected_provenance = {
        "dependency_sha256": EXPECTED_DEPENDENCIES,
        "old_artifacts_modified": False,
        "admission_engine": "python-flint Arb",
        "precision_bits": 384,
        "classification_policy": "strict_trichotomy_fail_closed",
        "clock": "source_core_state_is_time_0_and_next_collision_is_time_1",
    }
    if not strict_equal(provenance, expected_provenance):
        errors.append("provenance")
    errors.extend(check_registry(result.get("adaptive_full_core_step1_registry")))
    errors.extend(check_rows(result.get("adaptive_full_core_step1_raw_leaf_rows")))
    errors.extend(check_slabs(result.get("adaptive_full_core_step1_open_parameter_slab_rows")))
    errors.extend(check_mass(result.get("collision_mass_inner_outer_frontier")))
    if not strict_equal(result.get("strict_nonpromotion"), expected_scope()):
        errors.append("strict nonpromotion")
    if not strict_equal(manifest.get("verdict"), expected_verdict()):
        errors.append("verdict")
    return errors


def self_test(manifest: dict[str, Any]) -> tuple[int, int]:
    passed = 0
    total = 0

    def expect_errors(candidate: dict[str, Any], label: str) -> None:
        nonlocal passed, total
        total += 1
        if check(candidate):
            passed += 1
        else:
            print(f"HOSTILE TEST FAILED: {label}")

    top_mutations = [
        ("schema", "wrong"),
        ("certificate_sha256", "0" * 64),
        ("verifier_sha256", "0" * 64),
        ("dependencies", {}),
        ("verdict", {**manifest["verdict"], "Gate3": "CERTIFIED"}),
    ]
    for field, value in top_mutations:
        candidate = dict(manifest)
        candidate[field] = value
        expect_errors(candidate, f"top:{field}")

    result_mutations = [
        ("schema", "wrong"),
        ("provenance", {}),
        ("strict_nonpromotion", {**expected_scope(), "Gate5": "CERTIFIED"}),
        ("collision_mass_inner_outer_frontier", {
            **manifest["result"]["collision_mass_inner_outer_frontier"],
            "unresolved_outer_base_fraction_of_C24": "0",
        }),
        ("adaptive_full_core_step1_registry", {
            **manifest["result"]["adaptive_full_core_step1_registry"],
            "adaptive_leaf_count": 33959,
        }),
    ]
    for field, value in result_mutations:
        candidate = dict(manifest)
        candidate_result = dict(manifest["result"])
        candidate_result[field] = value
        candidate["result"] = candidate_result
        expect_errors(candidate, f"result:{field}")

    rows = manifest["result"]["adaptive_full_core_step1_raw_leaf_rows"]
    row_mutations = [
        ("classification", "UNRESOLVED_OUTER"),
        ("destination_core_id", None),
        ("depth", 99),
        ("dyadic_path", "2"),
        ("atom_id", "full-core-step1:" + "0" * 64),
        ("positive_two_dimensional_source_rectangle_at_each_s", 1),
        ("strict_next_collision_owner_inherited_from_whole_parent_core", False),
        ("parameter_averaged_unnormalized_collision_mass_upper", "0"),
        ("absolute_inverse_invariant_area_Jacobian", "2"),
        ("classification_witness_rows_sha256", "z" * 64),
    ]
    for field, value in row_mutations:
        candidate_rows = list(rows)
        source_row = rows[0]
        if field == "destination_core_id":
            source_row = next(
                row for row in rows
                if row["classification"] == "RETURN_AT_1_INNER"
            )
            source_index = rows.index(source_row)
        else:
            source_index = 0
        candidate_row = dict(source_row)
        candidate_row[field] = value
        candidate_rows[source_index] = candidate_row
        total += 1
        if check_rows(candidate_rows):
            passed += 1
        else:
            print(f"HOSTILE TEST FAILED: row:{field}")

    candidate_rows = list(rows)
    candidate_rows[1] = rows[0]
    total += 1
    if check_rows(candidate_rows):
        passed += 1

    candidate_rows = list(rows)
    candidate_row = dict(rows[0])
    candidate_box = dict(candidate_row["source_box"])
    candidate_box["t"] = list(reversed(candidate_box["t"]))
    candidate_row["source_box"] = candidate_box
    candidate_rows[0] = candidate_row
    total += 1
    if check_rows(candidate_rows):
        passed += 1

    slabs = manifest["result"]["adaptive_full_core_step1_open_parameter_slab_rows"]
    slab_mutations = [
        ("slab_index", 7),
        ("active_leaf_count", 0),
        ("full_C24_fixed_s_base_mass", "0"),
        ("return_inner_fixed_s_base_mass", "999"),
        ("open_s_interval", ["1", "0"]),
    ]
    for field, value in slab_mutations:
        candidate_slabs = list(slabs)
        candidate_slab = dict(slabs[0])
        candidate_slab[field] = value
        candidate_slabs[0] = candidate_slab
        total += 1
        if check_slabs(candidate_slabs):
            passed += 1
        else:
            print(f"HOSTILE TEST FAILED: slab:{field}")

    parser_probes = [
        ('{"x":1,"x":2}', DuplicateKeyError),
        ('{"x":NaN}', ValueError),
        ('{"x":Infinity}', ValueError),
    ]
    for payload, expected_error in parser_probes:
        total += 1
        try:
            json.loads(
                payload,
                object_pairs_hook=reject_duplicate_pairs,
                parse_constant=lambda value: (_ for _ in ()).throw(ValueError(value)),
            )
        except expected_error:
            passed += 1

    total += 1
    candidate_registry = dict(manifest["result"]["adaptive_full_core_step1_registry"])
    candidate_registry["strict_Arb_admission_only"] = 1
    if check_registry(candidate_registry):
        passed += 1

    total += 1
    candidate_mass = dict(manifest["result"]["collision_mass_inner_outer_frontier"])
    candidate_mass["return_inner_base_fraction_strict_lower"] = "1/2"
    if check_mass(candidate_mass):
        passed += 1

    return passed, total


def main() -> int:
    parser = argparse.ArgumentParser()
    modes = parser.add_mutually_exclusive_group()
    modes.add_argument("--integrity-only", action="store_true")
    modes.add_argument("--replay", action="store_true")
    modes.add_argument("--self-test", action="store_true")
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    args = parser.parse_args()
    if not (args.integrity_only or args.replay or args.self_test):
        print("LIVE_FULL_RN_QN_PARTITION: NOT_CERTIFIED")
        print("use --integrity-only, --replay, or --self-test for frozen audit")
        return 2
    try:
        manifest = strict_load(args.manifest)
        errors = check(manifest)
        if errors:
            print("FAIL: " + "; ".join(errors[:20]))
            return 1
        if args.replay:
            certificate = load_certificate()
            replay = certificate.build_result()
            if not strict_equal(replay, manifest["result"]):
                print("FAIL: independent replay differs from frozen result")
                return 1
            if sha256_path(CERTIFICATE) != EXPECTED_CERTIFICATE_SHA256:
                print("FAIL: certificate changed during replay")
                return 1
            print("FULL_CORE_RETURN_ADAPTIVE_FRONTIER_REPLAY: PASS")
        elif args.self_test:
            passed, total = self_test(manifest)
            if passed != total:
                print(f"HOSTILE TESTS: {passed}/{total} FAIL")
                return 1
            print(f"HOSTILE TESTS: {passed}/{total} PASS")
        else:
            print("FULL_CORE_RETURN_ADAPTIVE_FRONTIER_INTEGRITY: PASS")
        return 0
    except Exception as error:
        print(f"FAIL: {type(error).__name__}: {error}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
