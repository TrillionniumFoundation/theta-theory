#!/usr/bin/env python3
"""Independent fail-closed verifier for the round-26 child replay leaf."""

from __future__ import annotations

import argparse
import copy
import hashlib
import importlib.util
import json
import sys
from collections import Counter
from fractions import Fraction
from pathlib import Path
from types import ModuleType
from typing import Any


Q = Fraction
HERE = Path(__file__).resolve().parent
CERTIFICATE = HERE / "cm2_gate34_round26_unresolved_child_replay_cert.py"
ADAPTIVE_CERTIFICATE = HERE / "cm2_gate34_full_core_return_adaptive_frontier_cert.py"
ADAPTIVE_MANIFEST = HERE / "cm2-gate34-full-core-return-adaptive-frontier-manifest-2026-07-18.json"
F789_MANIFEST = HERE / "cm2-gate5-round25-adaptive-face-f789-manifest-2026-07-18.json"
DEFAULT_MANIFEST = HERE / "cm2-gate34-round26-unresolved-child-replay-manifest-2026-07-18.json"

MANIFEST_SCHEMA = "cm2.gate34.round26-unresolved-child-replay.manifest.v1"
RESULT_SCHEMA = "cm2.gate34.round26-unresolved-child-replay.v1"
EXPECTED_CERTIFICATE_SHA256 = (
    "237440eb97921c9c79aec04fbc0d664f0dc7d34accf5d98d27db0323675b04d6"
)
EXPECTED_ADAPTIVE_CERTIFICATE_SHA256 = (
    "d18b234471b192282abf064684fa535cc99c205797399b268f052c0884063a24"
)
EXPECTED_ADAPTIVE_MANIFEST_SHA256 = (
    "f79010c757e687cec2e8d7a8d617f3d94a3814731c58e960195c69107c446ad0"
)
EXPECTED_F789_MANIFEST_SHA256 = (
    "6b9354026a1707a25971925e02acbb5ea7e459ca177190a28ff1b39857283d86"
)
EXPECTED_F789_CERTIFICATE_SHA256 = (
    "d8c4b28ee856927f63bbbb746ea26fd2d7d473b2a3a0009d5c0836fadff3e63a"
)
EXPECTED_DEPENDENCIES = {
    ADAPTIVE_CERTIFICATE.name: EXPECTED_ADAPTIVE_CERTIFICATE_SHA256,
    ADAPTIVE_MANIFEST.name: EXPECTED_ADAPTIVE_MANIFEST_SHA256,
    F789_MANIFEST.name: EXPECTED_F789_MANIFEST_SHA256,
}
EXPECTED_RESULT_DIGEST = (
    "83462d2f185d736d6ac22ba3fe0240e0c5c0ae8c9c967fa32ba397feeed23287"
)
EXPECTED_RAW_CHILD_ROWS_SHA256 = (
    "8b4231dd12755ad51bfcb177ed573a26d0e4144eebf2f0282b5b7949abb58be9"
)
EXPECTED_PARENT_GROUP_ROWS_SHA256 = (
    "1ff91e8ec667380cc4215c35e6b6c8f8a7f047a395111d16daeadef4a95791dc"
)
EXPECTED_SORTED_CHILD_IDS_SHA256 = (
    "0cb99b470605e15b4072782a6005189e99b6601b78f4b9304d275ec6354336fc"
)
EXPECTED_SOURCE_SUMMARY_SHA256 = (
    "89f21605181ea8c9182a3f96cf69e531760d06a392e7aac78dfe00f39557eda5"
)
EXPECTED_CLASS_FRONTIER_SHA256 = {
    "RETURN_AT_1_INNER": (
        "754c57bd537cff1575ded4e524cab1c26739636fc2b7bf2f82d1023a3d3c7a76"
    ),
    "SURVIVE_THROUGH_1_INNER": (
        "95c96a656f164bfa5696a12265baeac42cecc9e1eca11dde532ef9f2e84fea69"
    ),
    "UNRESOLVED_OUTER": (
        "9c2c63341e3bedcb329fdebc9b901a87b36cbf5c12ed70f44f5ed512cdc905ed"
    ),
}

FROZEN_SPLIT_ROWS_SHA256 = (
    "7ab264eef8af4a156c988da008b271d9deb1c89e665d7ba99cbf8f9c63e6767b"
)
PARENT_COUNT = 26876
CHILD_COUNT = 53752
PARENT_MASS = Q(44519, 256000000)
CLASSIFICATIONS = (
    "RETURN_AT_1_INNER",
    "SURVIVE_THROUGH_1_INNER",
    "UNRESOLVED_OUTER",
)
EXPECTED_HISTOGRAM = {
    "RETURN_AT_1_INNER": 4088,
    "SURVIVE_THROUGH_1_INNER": 2048,
    "UNRESOLVED_OUTER": 47616,
}
EXPECTED_MASSES = {
    "RETURN_AT_1_INNER": "5953/1024000000",
    "SURVIVE_THROUGH_1_INNER": "17319/1024000000",
    "UNRESOLVED_OUTER": "38701/256000000",
}
EXPECTED_DEPTH_HISTOGRAM = {
    "13": {
        "RETURN_AT_1_INNER": 0,
        "SURVIVE_THROUGH_1_INNER": 1728,
        "UNRESOLVED_OUTER": 11904,
    },
    "16": {
        "RETURN_AT_1_INNER": 4088,
        "SURVIVE_THROUGH_1_INNER": 320,
        "UNRESOLVED_OUTER": 35712,
    },
}

TOP_KEYS = {
    "schema", "certificate_sha256", "verifier_sha256", "dependencies",
    "result", "verdict",
}
RESULT_KEYS = {
    "schema", "provenance", "frozen_round25_split_plan_replay",
    "child_parent_prefix_ownership_registry", "fresh_child_trichotomy_registry",
    "compact_ledger_contract", "strict_nonpromotion", "internal_replay_digest",
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
        parse_constant=lambda token: (_ for _ in ()).throw(ValueError(token)),
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


def exact_bool(value: Any) -> bool:
    return type(value) is bool


def valid_sha(value: Any) -> bool:
    return (
        isinstance(value, str)
        and len(value) == 64
        and all(character in "0123456789abcdef" for character in value)
    )


def expected_verdict() -> dict[str, Any]:
    return {
        "frozen_round25_split_plan_exact_replay": "CERTIFIED",
        "all_53752_children_fresh_384_bit_whole_box_trichotomy": "CERTIFIED",
        "child_parent_prefix_ownership_and_mass_conservation": "CERTIFIED",
        "one_generation_unresolved_base_mass_ratio_lt_7_over_8": "CERTIFIED",
        "residual_unresolved_outer_cover": "NONEMPTY",
        "complete_step1_R1_Q1_partition": "NOT_CERTIFIED",
        "arbitrary_n_Rn_Qn_partition": "NOT_CERTIFIED",
        "Gate3": "NOT_CERTIFIED",
        "Gate4": "NOT_CERTIFIED",
        "Gate5": "NOT_CERTIFIED",
        "CM2": "NO-GO_FOR_CLAIM",
    }


def expected_nonpromotion() -> dict[str, Any]:
    return {
        "residual_UNRESOLVED_OUTER_children_promoted_to_R1_or_Q1": 0,
        "complete_step1_R1_Q1_partition_without_outer_cover": "NOT_CERTIFIED",
        "finite_depth_exhaustion_of_unresolved_outer_cover": "NOT_CERTIFIED",
        "uniform_multigeneration_boundary_tube_decay": "NOT_CERTIFIED",
        "arbitrary_n_Rn_Qn_physical_partition": "NOT_CERTIFIED",
        "q_weighted_return_tail": "NOT_CERTIFIED",
        "induced_strong_Lasota_Yorke_coefficient": "NOT_CERTIFIED",
        "Gate3": "NOT_CERTIFIED",
        "Gate4": "NOT_CERTIFIED",
        "Gate5": "NOT_CERTIFIED",
        "CM2": "NO-GO_FOR_CLAIM",
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
        errors.append("dependencies")
    if not strict_equal(manifest.get("verdict"), expected_verdict()):
        errors.append("verdict")
    result = manifest.get("result")
    if not isinstance(result, dict):
        return errors + ["result type"]
    if set(result) != RESULT_KEYS:
        errors.append("result keys")
    if result.get("schema") != RESULT_SCHEMA:
        errors.append("result schema")
    if result.get("internal_replay_digest") != result_digest(result):
        errors.append("internal replay digest")
    if result.get("internal_replay_digest") != EXPECTED_RESULT_DIGEST:
        errors.append("frozen result digest")

    provenance = result.get("provenance")
    expected_provenance = {
        "dependency_sha256": EXPECTED_DEPENDENCIES,
        "old_artifacts_modified": False,
        "aggregate_or_recursive_root_modified": False,
        "admission_engine": "python-flint Arb",
        "precision_bits": 384,
        "classification_policy": "fresh_strict_whole_box_trichotomy_fail_closed",
        "clock": "source_core_state_is_time_0_and_next_collision_is_time_1",
    }
    if not strict_equal(provenance, expected_provenance):
        errors.append("provenance")

    plan = result.get("frozen_round25_split_plan_replay")
    if not isinstance(plan, dict):
        errors.append("plan type")
    else:
        expected_plan_subset = {
            "unresolved_parent_count": PARENT_COUNT,
            "scheduled_child_count": CHILD_COUNT,
            "split_axis_histogram": {"t": PARENT_COUNT},
            "parent_base_mass": str(PARENT_MASS),
            "planned_split_record_rows_sha256": FROZEN_SPLIT_ROWS_SHA256,
            "exact_match_to_frozen_F789_plan": True,
        }
        if any(not strict_equal(plan.get(key), value) for key, value in expected_plan_subset.items()):
            errors.append("plan contract")
        representatives = plan.get("representative_split_records")
        if not isinstance(representatives, list) or len(representatives) != 3:
            errors.append("plan representatives")

    ownership = result.get("child_parent_prefix_ownership_registry")
    expected_ownership = {
        "parent_count": PARENT_COUNT,
        "children_per_parent": 2,
        "child_count": CHILD_COUNT,
        "unique_child_atom_id_count": CHILD_COUNT,
        "all_child_paths_are_exact_parent_path_plus_side": True,
        "all_sibling_interiors_disjoint": True,
        "all_sibling_unions_equal_parent_mod_shared_face": True,
        "all_per_parent_child_mass_sums_exact": True,
        "all_child_paths_prefix_free_within_source_core": True,
        "all_next_collision_first_owner_witnesses_inherited_by_subset": True,
        "all_complete_candidate_comparisons_inherited_by_subset": True,
        "parent_group_rows_sha256": EXPECTED_PARENT_GROUP_ROWS_SHA256,
        "sorted_child_atom_ids_sha256": EXPECTED_SORTED_CHILD_IDS_SHA256,
    }
    if not strict_equal(ownership, expected_ownership):
        errors.append("ownership contract")

    registry = result.get("fresh_child_trichotomy_registry")
    if not isinstance(registry, dict):
        errors.append("trichotomy registry type")
    else:
        expected_registry_subset = {
            "fresh_whole_box_Arb_child_count": CHILD_COUNT,
            "classification_histogram": EXPECTED_HISTOGRAM,
            "classification_base_masses": EXPECTED_MASSES,
            "classification_base_mass_sum": str(PARENT_MASS),
            "child_depth_classification_histogram": EXPECTED_DEPTH_HISTOGRAM,
            "residual_unresolved_base_mass_ratio_of_parent": "38701/44519",
            "newly_resolved_base_mass_ratio_of_parent": "5818/44519",
            "residual_unresolved_ratio_strict_upper_benchmark": "7/8",
            "newly_resolved_ratio_strict_lower_benchmark": "1/8",
            "source_core_summary_rows_sha256": EXPECTED_SOURCE_SUMMARY_SHA256,
            "raw_child_rows_sha256": EXPECTED_RAW_CHILD_ROWS_SHA256,
            "class_frontier_rows_sha256": EXPECTED_CLASS_FRONTIER_SHA256,
            "all_three_classes_are_nonempty": True,
            "residual_unresolved_frontier_is_nonempty": True,
        }
        if any(not strict_equal(registry.get(key), value) for key, value in expected_registry_subset.items()):
            errors.append("trichotomy exact contract")
        if not isinstance(registry.get("source_core_summary_rows"), list) or len(registry["source_core_summary_rows"]) != 24:
            errors.append("source summary rows")
        if not isinstance(registry.get("representative_child_rows"), list) or not registry["representative_child_rows"]:
            errors.append("child representatives")
        destination_count = registry.get("return_destination_core_count")
        if type(destination_count) is not int or destination_count != 16:
            errors.append("destination core count")

    expected_compact = {
        "all_53752_child_rows_materialized_during_replay": True,
        "manifest_retains_canonical_digests_and_representative_rows": True,
        "independent_verifier_reconstructs_every_child_and_every_classification": True,
        "deterministic_full_replay_from_frozen_parents_and_split_policy": True,
    }
    if not strict_equal(result.get("compact_ledger_contract"), expected_compact):
        errors.append("compact ledger contract")
    if not strict_equal(result.get("strict_nonpromotion"), expected_nonpromotion()):
        errors.append("strict nonpromotion")
    return errors


def load_adaptive() -> ModuleType:
    if sys.flags.optimize != 0:
        raise RuntimeError("optimized Python is forbidden")
    for path, expected in (
        (CERTIFICATE, EXPECTED_CERTIFICATE_SHA256),
        (ADAPTIVE_CERTIFICATE, EXPECTED_ADAPTIVE_CERTIFICATE_SHA256),
        (ADAPTIVE_MANIFEST, EXPECTED_ADAPTIVE_MANIFEST_SHA256),
        (F789_MANIFEST, EXPECTED_F789_MANIFEST_SHA256),
    ):
        resolved = path.resolve()
        if resolved.parent != HERE or not path.is_file() or path.is_symlink():
            raise RuntimeError(f"unsafe replay path: {path.name}")
        if sha256_path(path) != expected:
            raise RuntimeError(f"replay dependency hash: {path.name}")
    spec = importlib.util.spec_from_file_location(
        "cm2_gate34_round26_independent_adaptive_frozen",
        ADAPTIVE_CERTIFICATE,
    )
    if spec is None or spec.loader is None:
        raise RuntimeError("adaptive import spec")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    if Path(module.__file__).resolve() != ADAPTIVE_CERTIFICATE.resolve():
        raise RuntimeError("adaptive import path")
    if module.ctx.prec != 384:
        raise RuntimeError("adaptive Arb precision")
    module.load_dependencies()
    return module


def qpair(value: Any) -> tuple[Q, Q]:
    if not isinstance(value, list) or len(value) != 2:
        raise RuntimeError("rational pair")
    lower, upper = Q(value[0]), Q(value[1])
    if not lower < upper:
        raise RuntimeError("positive interval")
    return lower, upper


def parent_boxes(rows: list[dict[str, Any]]) -> dict[int, dict[str, tuple[Q, Q]]]:
    result: dict[int, dict[str, tuple[Q, Q]]] = {}
    for index in range(24):
        source = [row for row in rows if row["source_core_index"] == index]
        if not source:
            raise RuntimeError("source cover")
        result[index] = {}
        for coordinate in ("t", "p", "s"):
            pairs = [qpair(row["source_box"][coordinate]) for row in source]
            result[index][coordinate] = (
                min(pair[0] for pair in pairs),
                max(pair[1] for pair in pairs),
            )
    return result


def independent_axis(row: dict[str, Any], core_box: dict[str, tuple[Q, Q]]) -> str:
    scales: dict[str, Q] = {}
    for coordinate in ("t", "p", "s"):
        lower, upper = qpair(row["source_box"][coordinate])
        base_lower, base_upper = core_box[coordinate]
        scales[coordinate] = (upper - lower) / (base_upper - base_lower)
    maximum = max(scales.values())
    return next(coordinate for coordinate in ("t", "p", "s") if scales[coordinate] == maximum)


def independent_boxes(row: dict[str, Any], axis: str) -> list[dict[str, list[str]]]:
    source = {coordinate: list(row["source_box"][coordinate]) for coordinate in ("t", "p", "s")}
    lower, upper = qpair(source[axis])
    middle = (lower + upper) / 2
    result: list[dict[str, list[str]]] = []
    for side in (0, 1):
        child = copy.deepcopy(source)
        child[axis] = [str(lower), str(middle)] if side == 0 else [str(middle), str(upper)]
        result.append(child)
    return result


def independent_split_record(
    row: dict[str, Any], core_box: dict[str, tuple[Q, Q]],
) -> tuple[dict[str, Any], list[dict[str, list[str]]]]:
    axis = independent_axis(row, core_box)
    boxes = independent_boxes(row, axis)
    parent_mass = Q(row["parameter_averaged_unnormalized_base_mass"])
    payload: dict[str, Any] = {
        "parent_atom_id": row["atom_id"],
        "source_core_id": row["source_core_id"],
        "parent_dyadic_path": row["dyadic_path"],
        "parent_depth": row["depth"],
        "split_axis": axis,
        "child_dyadic_paths": [row["dyadic_path"] + "0", row["dyadic_path"] + "1"],
        "child_source_boxes_sha256": digest(boxes),
        "parent_base_mass": str(parent_mass),
        "each_child_base_mass": str(parent_mass / 2),
        "exact_child_mass_sum_equals_parent": True,
        "children_require_fresh_strict_Arb_classification": True,
    }
    payload["split_record_id"] = "split:r1q1:" + digest(payload)
    return payload, boxes


def atom_box(atom: Any) -> dict[str, list[str]]:
    return {
        "t": [str(atom.t0), str(atom.t1)],
        "p": [str(atom.p0), str(atom.p1)],
        "s": [str(atom.s0), str(atom.s1)],
    }


def independent_atom(parent: dict[str, Any], adaptive: ModuleType, cores: tuple[Any, ...]) -> Any:
    box = parent["source_box"]
    index = parent["source_core_index"]
    return adaptive.Atom(
        index, cores[index],
        Q(box["t"][0]), Q(box["t"][1]),
        Q(box["p"][0]), Q(box["p"][1]),
        Q(box["s"][0]), Q(box["s"][1]),
        parent["dyadic_path"],
    )


def independent_child_row(
    parent: dict[str, Any], split: dict[str, Any], child: Any, side: int,
    classification: dict[str, Any], adaptive: ModuleType,
) -> dict[str, Any]:
    source_box = atom_box(child)
    payload = {
        "source_core_id": adaptive.core_id(child.source_core),
        "dyadic_path": child.path,
        "source_box": source_box,
    }
    child_id = "full-core-step1:" + digest(payload)
    raw_mass = adaptive.base_mass(child)
    if child.path != parent["dyadic_path"] + str(side):
        raise RuntimeError("independent child prefix")
    if raw_mass != Q(parent["parameter_averaged_unnormalized_base_mass"]) / 2:
        raise RuntimeError("independent child mass")
    return {
        "child_atom_id": child_id,
        "parent_atom_id": parent["atom_id"],
        "frozen_split_record_id": split["split_record_id"],
        "source_core_index": child.source_core_index,
        "source_core_id": payload["source_core_id"],
        "parent_dyadic_path": parent["dyadic_path"],
        "child_dyadic_path": child.path,
        "parent_depth": parent["depth"],
        "child_depth": child.depth,
        "child_side": side,
        "split_axis": split["split_axis"],
        "source_box": source_box,
        "parent_source_box_sha256": digest(parent["source_box"]),
        "child_source_box_sha256": digest(source_box),
        "child_path_is_exact_parent_prefix_plus_side": True,
        "child_box_is_exact_scheduled_half": True,
        "sibling_interiors_disjoint_and_union_parent_mod_shared_face": True,
        "strict_next_collision_owner_inherited_from_whole_parent_core": True,
        "complete_retained_candidate_comparison_inherited": True,
        "parent_owner_witness_sha256": parent["parent_owner_witness_sha256"],
        "fresh_whole_box_Arb_precision_bits": 384,
        "classification": classification["classification"],
        "destination_core_id": classification["destination_core_id"],
        "classification_witness_rows_sha256": digest(classification["witness_rows"]),
        "output_enclosures": classification["output_enclosures"],
        "parameter_averaged_unnormalized_base_mass": str(raw_mass),
        "parameter_averaged_unnormalized_collision_mass_lower": str(raw_mass),
        "parameter_averaged_unnormalized_collision_mass_upper": str(Q(1401, 1000) * raw_mass),
        "canonical_invariant_area_coordinates": "(r,p=sin(phi))",
        "absolute_inverse_invariant_area_Jacobian": "1",
        "log_invariant_area_Jacobian_distortion": "0",
    }


def independent_replay(manifest: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    adaptive = load_adaptive()
    adaptive_manifest = strict_load(ADAPTIVE_MANIFEST)
    f789 = strict_load(F789_MANIFEST)
    if adaptive_manifest.get("certificate_sha256") != EXPECTED_ADAPTIVE_CERTIFICATE_SHA256:
        return ["independent adaptive certificate field"]
    if f789.get("certificate_sha256") != EXPECTED_F789_CERTIFICATE_SHA256:
        return ["independent F789 certificate field"]
    all_rows = adaptive_manifest["result"]["adaptive_full_core_step1_raw_leaf_rows"]
    if digest(all_rows) != adaptive_manifest["result"]["adaptive_full_core_step1_registry"]["raw_leaf_rows_sha256"]:
        return ["independent adaptive raw rows"]
    unresolved = [row for row in all_rows if row["classification"] == "UNRESOLVED_OUTER"]
    unresolved.sort(key=lambda row: (row["source_core_index"], row["dyadic_path"]))
    if len(unresolved) != PARENT_COUNT:
        return ["independent parent count"]
    core_boxes = parent_boxes(all_rows)
    cores = adaptive.core_cert.physical_cores()
    split_rows: list[dict[str, Any]] = []
    splits: dict[str, tuple[dict[str, Any], list[dict[str, list[str]]]]] = {}
    for parent in unresolved:
        split = independent_split_record(parent, core_boxes[parent["source_core_index"]])
        split_rows.append(split[0])
        splits[parent["atom_id"]] = split
    split_rows.sort(key=lambda row: row["parent_atom_id"])
    if digest(split_rows) != FROZEN_SPLIT_ROWS_SHA256:
        return ["independent split plan digest"]
    frozen_plan = f789["result"]["unresolved_outer_next_generation_split_plan"]
    if frozen_plan["planned_split_record_rows_sha256"] != digest(split_rows):
        return ["independent F789 split binding"]

    rows: list[dict[str, Any]] = []
    parent_groups: list[dict[str, Any]] = []
    for parent in unresolved:
        split, scheduled_boxes = splits[parent["atom_id"]]
        children = adaptive.split_atom(independent_atom(parent, adaptive, cores))
        if [atom_box(child) for child in children] != scheduled_boxes:
            return ["independent scheduled child boxes"]
        group: list[dict[str, Any]] = []
        for side, child in enumerate(children):
            classification = adaptive.classify_atom(child, cores)
            row = independent_child_row(parent, split, child, side, classification, adaptive)
            rows.append(row)
            group.append(row)
        if sum(Q(row["parameter_averaged_unnormalized_base_mass"]) for row in group) != Q(parent["parameter_averaged_unnormalized_base_mass"]):
            return ["independent per-parent mass"]
        parent_groups.append({
            "parent_atom_id": parent["atom_id"],
            "frozen_split_record_id": split["split_record_id"],
            "child_atom_ids": [row["child_atom_id"] for row in group],
            "child_classifications": [row["classification"] for row in group],
            "child_base_masses": [row["parameter_averaged_unnormalized_base_mass"] for row in group],
            "exact_child_mass_sum_equals_parent": True,
        })
    rows.sort(key=lambda row: (row["source_core_index"], row["child_dyadic_path"]))
    parent_groups.sort(key=lambda row: row["parent_atom_id"])
    child_ids = [row["child_atom_id"] for row in rows]
    if len(rows) != CHILD_COUNT or len(set(child_ids)) != CHILD_COUNT:
        return ["independent child cardinality"]
    for index in range(24):
        paths = sorted(row["child_dyadic_path"] for row in rows if row["source_core_index"] == index)
        if len(paths) != len(set(paths)) or any(right.startswith(left) for left, right in zip(paths, paths[1:])):
            return ["independent prefix ownership"]
    histogram = Counter(row["classification"] for row in rows)
    masses = {
        kind: sum(Q(row["parameter_averaged_unnormalized_base_mass"]) for row in rows if row["classification"] == kind)
        for kind in CLASSIFICATIONS
    }
    depth_histogram = {
        str(depth): {
            kind: sum(row["child_depth"] == depth and row["classification"] == kind for row in rows)
            for kind in CLASSIFICATIONS
        }
        for depth in sorted({row["child_depth"] for row in rows})
    }
    source_summary: list[dict[str, Any]] = []
    for index in range(24):
        source_rows = [row for row in rows if row["source_core_index"] == index]
        source_ids = {row["source_core_id"] for row in all_rows if row["source_core_index"] == index}
        if len(source_ids) != 1:
            return ["independent source id"]
        source_summary.append({
            "source_core_index": index,
            "source_core_id": next(iter(source_ids)),
            "child_count": len(source_rows),
            "classification_histogram": {
                kind: sum(row["classification"] == kind for row in source_rows)
                for kind in CLASSIFICATIONS
            },
            "classification_base_masses": {
                kind: str(sum(Q(row["parameter_averaged_unnormalized_base_mass"]) for row in source_rows if row["classification"] == kind))
                for kind in CLASSIFICATIONS
            },
        })
    representative_indices = {0, len(rows) // 4, len(rows) // 2, 3 * len(rows) // 4, len(rows) - 1}
    for kind in CLASSIFICATIONS:
        representative_indices.add(next(index for index, row in enumerate(rows) if row["classification"] == kind))
    representatives = [rows[index] for index in sorted(representative_indices)]
    registry = manifest["result"]["fresh_child_trichotomy_registry"]
    ownership = manifest["result"]["child_parent_prefix_ownership_registry"]
    comparisons = {
        "histogram": (dict(sorted(histogram.items())), registry["classification_histogram"]),
        "masses": ({kind: str(masses[kind]) for kind in CLASSIFICATIONS}, registry["classification_base_masses"]),
        "depth histogram": (depth_histogram, registry["child_depth_classification_histogram"]),
        "raw rows digest": (digest(rows), registry["raw_child_rows_sha256"]),
        "class digests": ({kind: digest([row for row in rows if row["classification"] == kind]) for kind in CLASSIFICATIONS}, registry["class_frontier_rows_sha256"]),
        "source summary": (source_summary, registry["source_core_summary_rows"]),
        "source digest": (digest(source_summary), registry["source_core_summary_rows_sha256"]),
        "representatives": (representatives, registry["representative_child_rows"]),
        "destination count": (len({row["destination_core_id"] for row in rows if row["classification"] == "RETURN_AT_1_INNER"}), registry["return_destination_core_count"]),
        "parent groups": (digest(parent_groups), ownership["parent_group_rows_sha256"]),
        "child ids": (digest(sorted(child_ids)), ownership["sorted_child_atom_ids_sha256"]),
    }
    for label, (observed, frozen) in comparisons.items():
        if not strict_equal(observed, frozen):
            errors.append("independent " + label)
    return errors


def set_path(root: dict[str, Any], path: tuple[Any, ...], value: Any) -> None:
    cursor: Any = root
    for key in path[:-1]:
        cursor = cursor[key]
    cursor[path[-1]] = value


def self_test(manifest: dict[str, Any]) -> tuple[int, int]:
    passed = 0
    total = 0

    def expect_rejected(candidate: dict[str, Any], label: str) -> None:
        nonlocal passed, total
        total += 1
        if check(candidate):
            passed += 1
        else:
            print("HOSTILE TEST FAILED: " + label)

    top_mutations = (
        ("schema", "wrong"),
        ("certificate_sha256", "0" * 64),
        ("verifier_sha256", "0" * 64),
        ("dependencies", {}),
        ("verdict", {**expected_verdict(), "Gate5": "CERTIFIED"}),
    )
    for key, value in top_mutations:
        candidate = copy.deepcopy(manifest)
        candidate[key] = value
        expect_rejected(candidate, "top:" + key)

    mutations: list[tuple[tuple[Any, ...], Any]] = [
        (("schema",), "wrong"),
        (("provenance", "precision_bits"), 383),
        (("provenance", "old_artifacts_modified"), True),
        (("provenance", "aggregate_or_recursive_root_modified"), True),
        (("frozen_round25_split_plan_replay", "unresolved_parent_count"), 26875),
        (("frozen_round25_split_plan_replay", "scheduled_child_count"), 53751),
        (("frozen_round25_split_plan_replay", "split_axis_histogram"), {"p": 26876}),
        (("frozen_round25_split_plan_replay", "parent_base_mass"), "0"),
        (("frozen_round25_split_plan_replay", "planned_split_record_rows_sha256"), "0" * 64),
        (("frozen_round25_split_plan_replay", "exact_match_to_frozen_F789_plan"), False),
        (("child_parent_prefix_ownership_registry", "parent_count"), 1),
        (("child_parent_prefix_ownership_registry", "children_per_parent"), 3),
        (("child_parent_prefix_ownership_registry", "child_count"), 1),
        (("child_parent_prefix_ownership_registry", "unique_child_atom_id_count"), 1),
        (("child_parent_prefix_ownership_registry", "all_child_paths_are_exact_parent_path_plus_side"), False),
        (("child_parent_prefix_ownership_registry", "all_sibling_interiors_disjoint"), False),
        (("child_parent_prefix_ownership_registry", "all_sibling_unions_equal_parent_mod_shared_face"), False),
        (("child_parent_prefix_ownership_registry", "all_per_parent_child_mass_sums_exact"), False),
        (("child_parent_prefix_ownership_registry", "all_child_paths_prefix_free_within_source_core"), False),
        (("child_parent_prefix_ownership_registry", "all_next_collision_first_owner_witnesses_inherited_by_subset"), False),
        (("child_parent_prefix_ownership_registry", "all_complete_candidate_comparisons_inherited_by_subset"), False),
        (("child_parent_prefix_ownership_registry", "parent_group_rows_sha256"), "0" * 64),
        (("child_parent_prefix_ownership_registry", "sorted_child_atom_ids_sha256"), "0" * 64),
        (("fresh_child_trichotomy_registry", "fresh_whole_box_Arb_child_count"), 53751),
        (("fresh_child_trichotomy_registry", "classification_histogram", "RETURN_AT_1_INNER"), 4087),
        (("fresh_child_trichotomy_registry", "classification_histogram", "SURVIVE_THROUGH_1_INNER"), 2047),
        (("fresh_child_trichotomy_registry", "classification_histogram", "UNRESOLVED_OUTER"), 0),
        (("fresh_child_trichotomy_registry", "classification_base_masses", "RETURN_AT_1_INNER"), "0"),
        (("fresh_child_trichotomy_registry", "classification_base_masses", "SURVIVE_THROUGH_1_INNER"), "0"),
        (("fresh_child_trichotomy_registry", "classification_base_masses", "UNRESOLVED_OUTER"), "0"),
        (("fresh_child_trichotomy_registry", "classification_base_mass_sum"), "0"),
        (("fresh_child_trichotomy_registry", "child_depth_classification_histogram", "13", "UNRESOLVED_OUTER"), 0),
        (("fresh_child_trichotomy_registry", "child_depth_classification_histogram", "16", "RETURN_AT_1_INNER"), 0),
        (("fresh_child_trichotomy_registry", "residual_unresolved_base_mass_ratio_of_parent"), "0"),
        (("fresh_child_trichotomy_registry", "newly_resolved_base_mass_ratio_of_parent"), "1"),
        (("fresh_child_trichotomy_registry", "residual_unresolved_ratio_strict_upper_benchmark"), "1"),
        (("fresh_child_trichotomy_registry", "newly_resolved_ratio_strict_lower_benchmark"), "0"),
        (("fresh_child_trichotomy_registry", "raw_child_rows_sha256"), "0" * 64),
        (("fresh_child_trichotomy_registry", "source_core_summary_rows_sha256"), "0" * 64),
        (("fresh_child_trichotomy_registry", "all_three_classes_are_nonempty"), False),
        (("fresh_child_trichotomy_registry", "residual_unresolved_frontier_is_nonempty"), False),
        (("compact_ledger_contract", "all_53752_child_rows_materialized_during_replay"), False),
        (("compact_ledger_contract", "manifest_retains_canonical_digests_and_representative_rows"), False),
        (("compact_ledger_contract", "independent_verifier_reconstructs_every_child_and_every_classification"), False),
        (("compact_ledger_contract", "deterministic_full_replay_from_frozen_parents_and_split_policy"), False),
        (("strict_nonpromotion", "residual_UNRESOLVED_OUTER_children_promoted_to_R1_or_Q1"), 1),
        (("strict_nonpromotion", "complete_step1_R1_Q1_partition_without_outer_cover"), "CERTIFIED"),
        (("strict_nonpromotion", "finite_depth_exhaustion_of_unresolved_outer_cover"), "CERTIFIED"),
        (("strict_nonpromotion", "uniform_multigeneration_boundary_tube_decay"), "CERTIFIED"),
        (("strict_nonpromotion", "arbitrary_n_Rn_Qn_physical_partition"), "CERTIFIED"),
        (("strict_nonpromotion", "q_weighted_return_tail"), "CERTIFIED"),
        (("strict_nonpromotion", "induced_strong_Lasota_Yorke_coefficient"), "CERTIFIED"),
        (("strict_nonpromotion", "Gate3"), "CERTIFIED"),
        (("strict_nonpromotion", "Gate4"), "CERTIFIED"),
        (("strict_nonpromotion", "Gate5"), "CERTIFIED"),
        (("strict_nonpromotion", "CM2"), "GO_FOR_CLAIM"),
    ]
    for index, (path, value) in enumerate(mutations):
        candidate = copy.deepcopy(manifest)
        set_path(candidate["result"], path, value)
        if index % 2 == 0:
            candidate["result"]["internal_replay_digest"] = result_digest(candidate["result"])
        expect_rejected(candidate, "result:" + "/".join(map(str, path)))

    candidate = copy.deepcopy(manifest)
    candidate["result"].pop("compact_ledger_contract")
    candidate["result"]["internal_replay_digest"] = result_digest(candidate["result"])
    expect_rejected(candidate, "missing result key")
    candidate = copy.deepcopy(manifest)
    candidate["extra"] = True
    expect_rejected(candidate, "extra top key")

    parser_probes = (
        ('{"x":1,"x":2}', DuplicateKeyError),
        ('{"x":NaN}', ValueError),
        ('{"x":Infinity}', ValueError),
    )
    for payload, expected_error in parser_probes:
        total += 1
        try:
            json.loads(
                payload,
                object_pairs_hook=reject_duplicate_pairs,
                parse_constant=lambda token: (_ for _ in ()).throw(ValueError(token)),
            )
        except expected_error:
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
        print("LIVE_COMPLETE_STEP1_R1_Q1_PARTITION: NOT_CERTIFIED")
        print("LIVE_GATE5: NOT_CERTIFIED")
        print("use --integrity-only, --replay, or --self-test for frozen audit")
        return 2
    try:
        manifest = strict_load(args.manifest)
        errors = check(manifest)
        if errors:
            print("FAIL: " + "; ".join(errors[:20]))
            return 1
        if args.replay:
            replay_errors = independent_replay(manifest)
            if replay_errors:
                print("FAIL: " + "; ".join(replay_errors[:20]))
                return 1
            if sha256_path(CERTIFICATE) != EXPECTED_CERTIFICATE_SHA256:
                print("FAIL: certificate changed during independent replay")
                return 1
            print("ROUND26_UNRESOLVED_CHILD_INDEPENDENT_REPLAY: PASS")
        elif args.self_test:
            passed, total = self_test(manifest)
            if passed != total:
                print(f"HOSTILE TESTS: {passed}/{total} FAIL")
                return 1
            print(f"HOSTILE TESTS: {passed}/{total} PASS")
        else:
            print("ROUND26_UNRESOLVED_CHILD_INTEGRITY: PASS")
        return 0
    except Exception as error:
        print(f"FAIL: {type(error).__name__}: {error}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
