#!/usr/bin/env python3
"""Round-26 fresh Arb replay of the frozen unresolved C24 children.

This append-only leaf consumes the round-25 adaptive one-step cover and the
separately frozen 26,876-parent split plan.  It reconstructs both scheduled
children of every unresolved parent, proves exact dyadic prefix ownership and
base-mass conservation, and freshly applies the 384-bit whole-box trichotomy.

The output is intentionally a compact digest ledger.  All 53,752 child rows
are materialized during replay, but the JSON manifest stores their canonical
digest, per-core summaries, class/frontier digests, and representative rows
rather than duplicating tens of megabytes of deterministic enclosure text.

A residual ``UNRESOLVED_OUTER`` child is not promoted to R1 or Q1.  This leaf
does not modify an aggregate or recursive root and does not claim a complete
one-step partition, an arbitrary-n return partition, or a strong operator
bound.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from collections import Counter
from fractions import Fraction
from pathlib import Path
from typing import Any

from flint import ctx

import cm2_gate34_full_core_return_adaptive_frontier_cert as adaptive


Q = Fraction
HERE = Path(__file__).resolve().parent
ctx.prec = 384

RESULT_SCHEMA = "cm2.gate34.round26-unresolved-child-replay.v1"
MANIFEST_SCHEMA = "cm2.gate34.round26-unresolved-child-replay.manifest.v1"
DEFAULT_MANIFEST = (
    HERE / "cm2-gate34-round26-unresolved-child-replay-manifest-2026-07-18.json"
)

DEPENDENCIES = {
    "cm2_gate34_full_core_return_adaptive_frontier_cert.py": (
        "d18b234471b192282abf064684fa535cc99c205797399b268f052c0884063a24"
    ),
    "cm2-gate34-full-core-return-adaptive-frontier-manifest-2026-07-18.json": (
        "f79010c757e687cec2e8d7a8d617f3d94a3814731c58e960195c69107c446ad0"
    ),
    "cm2-gate5-round25-adaptive-face-f789-manifest-2026-07-18.json": (
        "6b9354026a1707a25971925e02acbb5ea7e459ca177190a28ff1b39857283d86"
    ),
}

ADAPTIVE_CERTIFICATE_SHA256 = DEPENDENCIES[
    "cm2_gate34_full_core_return_adaptive_frontier_cert.py"
]
F789_CERTIFICATE_SHA256 = (
    "d8c4b28ee856927f63bbbb746ea26fd2d7d473b2a3a0009d5c0836fadff3e63a"
)
FROZEN_PARENT_COUNT = 26876
FROZEN_CHILD_COUNT = 53752
FROZEN_PARENT_MASS = Q(44519, 256000000)
FROZEN_SPLIT_ROWS_SHA256 = (
    "7ab264eef8af4a156c988da008b271d9deb1c89e665d7ba99cbf8f9c63e6767b"
)
EXPECTED_CLASSIFICATION_HISTOGRAM = {
    "RETURN_AT_1_INNER": 4088,
    "SURVIVE_THROUGH_1_INNER": 2048,
    "UNRESOLVED_OUTER": 47616,
}
EXPECTED_CLASSIFICATION_MASSES = {
    "RETURN_AT_1_INNER": Q(5953, 1024000000),
    "SURVIVE_THROUGH_1_INNER": Q(17319, 1024000000),
    "UNRESOLVED_OUTER": Q(38701, 256000000),
}
CLASSIFICATIONS = tuple(EXPECTED_CLASSIFICATION_HISTOGRAM)


class DuplicateKeyError(ValueError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


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
        parse_constant=lambda token: (_ for _ in ()).throw(
            ValueError(f"non-finite JSON constant: {token}")
        ),
    )


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def canonical_digest(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def sha256_path(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def qpair(value: Any) -> tuple[Q, Q]:
    require(isinstance(value, list) and len(value) == 2, "rational pair")
    lower, upper = Q(value[0]), Q(value[1])
    require(lower < upper, "positive interval")
    return lower, upper


def result_digest(result: dict[str, Any]) -> str:
    payload = dict(result)
    payload.pop("internal_replay_digest", None)
    return canonical_digest(payload)


def load_dependencies() -> tuple[dict[str, Any], dict[str, Any]]:
    for name, expected in DEPENDENCIES.items():
        path = (HERE / name).resolve()
        require(path.parent == HERE, f"unsafe dependency: {name}")
        require(path.is_file() and not path.is_symlink(), f"missing dependency: {name}")
        require(sha256_path(path) == expected, f"dependency hash: {name}")
    require(Path(adaptive.__file__).resolve() == (HERE / next(iter(DEPENDENCIES))).resolve(), "adaptive import path")
    adaptive.load_dependencies()
    require(ctx.prec == 384, "Arb precision")

    adaptive_manifest = strict_load(
        HERE / "cm2-gate34-full-core-return-adaptive-frontier-manifest-2026-07-18.json"
    )
    require(isinstance(adaptive_manifest, dict), "adaptive manifest type")
    require(
        adaptive_manifest.get("certificate_sha256") == ADAPTIVE_CERTIFICATE_SHA256,
        "adaptive certificate binding",
    )
    adaptive_result = adaptive_manifest.get("result")
    require(isinstance(adaptive_result, dict), "adaptive result type")
    adaptive_registry = adaptive_result.get("adaptive_full_core_step1_registry")
    require(isinstance(adaptive_registry, dict), "adaptive registry type")
    require(adaptive_registry.get("precision_bits", 384) == 384, "adaptive precision")
    require(adaptive_registry["adaptive_leaf_count"] == 33960, "adaptive leaf count")
    require(
        adaptive_registry["classification_histogram"]
        == {
            "RETURN_AT_1_INNER": 4216,
            "SURVIVE_THROUGH_1_INNER": 2868,
            "UNRESOLVED_OUTER": 26876,
        },
        "adaptive histogram",
    )
    require(adaptive_registry["strict_Arb_admission_only"] is True, "adaptive strict admission")
    require(
        adaptive_registry["raw_leaf_rows_sha256"]
        == canonical_digest(adaptive_result["adaptive_full_core_step1_raw_leaf_rows"]),
        "adaptive row digest",
    )

    f789_manifest = strict_load(
        HERE / "cm2-gate5-round25-adaptive-face-f789-manifest-2026-07-18.json"
    )
    require(isinstance(f789_manifest, dict), "F789 manifest type")
    require(f789_manifest.get("certificate_sha256") == F789_CERTIFICATE_SHA256, "F789 certificate binding")
    require(
        f789_manifest.get("dependencies", {}).get(
            "cm2-gate34-full-core-return-adaptive-frontier-manifest-2026-07-18.json"
        )
        == DEPENDENCIES[
            "cm2-gate34-full-core-return-adaptive-frontier-manifest-2026-07-18.json"
        ],
        "F789 adaptive dependency binding",
    )
    return adaptive_manifest, f789_manifest


def parent_core_boxes(rows: list[dict[str, Any]]) -> dict[int, dict[str, tuple[Q, Q]]]:
    grouped: dict[int, list[dict[str, Any]]] = {index: [] for index in range(24)}
    for row in rows:
        index = row["source_core_index"]
        require(type(index) is int and index in grouped, "source core index")
        grouped[index].append(row)
    require(all(grouped.values()), "all source cores represented")
    result: dict[int, dict[str, tuple[Q, Q]]] = {}
    for index, source_rows in grouped.items():
        result[index] = {}
        for coordinate in ("t", "p", "s"):
            pairs = [qpair(row["source_box"][coordinate]) for row in source_rows]
            result[index][coordinate] = (
                min(pair[0] for pair in pairs),
                max(pair[1] for pair in pairs),
            )
    return result


def choose_split_axis(
    row: dict[str, Any], parent_core: dict[str, tuple[Q, Q]],
) -> str:
    scales: dict[str, Q] = {}
    for coordinate in ("t", "p", "s"):
        lower, upper = qpair(row["source_box"][coordinate])
        parent_lower, parent_upper = parent_core[coordinate]
        scales[coordinate] = (upper - lower) / (parent_upper - parent_lower)
    if scales["t"] >= scales["p"] and scales["t"] >= scales["s"]:
        return "t"
    if scales["p"] >= scales["s"]:
        return "p"
    return "s"


def split_boxes(row: dict[str, Any], axis: str) -> list[dict[str, list[str]]]:
    source = {
        coordinate: list(row["source_box"][coordinate])
        for coordinate in ("t", "p", "s")
    }
    lower, upper = qpair(source[axis])
    middle = (lower + upper) / 2
    children: list[dict[str, list[str]]] = []
    for side in (0, 1):
        child = {coordinate: list(bounds) for coordinate, bounds in source.items()}
        child[axis] = (
            [str(lower), str(middle)] if side == 0
            else [str(middle), str(upper)]
        )
        children.append(child)
    return children


def frozen_split_record(
    row: dict[str, Any], parent_core: dict[str, tuple[Q, Q]],
) -> tuple[dict[str, Any], list[dict[str, list[str]]]]:
    axis = choose_split_axis(row, parent_core)
    boxes = split_boxes(row, axis)
    parent_mass = Q(row["parameter_averaged_unnormalized_base_mass"])
    payload: dict[str, Any] = {
        "parent_atom_id": row["atom_id"],
        "source_core_id": row["source_core_id"],
        "parent_dyadic_path": row["dyadic_path"],
        "parent_depth": row["depth"],
        "split_axis": axis,
        "child_dyadic_paths": [row["dyadic_path"] + "0", row["dyadic_path"] + "1"],
        "child_source_boxes_sha256": canonical_digest(boxes),
        "parent_base_mass": str(parent_mass),
        "each_child_base_mass": str(parent_mass / 2),
        "exact_child_mass_sum_equals_parent": True,
        "children_require_fresh_strict_Arb_classification": True,
    }
    payload["split_record_id"] = "split:r1q1:" + canonical_digest(payload)
    return payload, boxes


def atom_from_row(row: dict[str, Any], cores: tuple[Any, ...]) -> adaptive.Atom:
    box = row["source_box"]
    index = row["source_core_index"]
    return adaptive.Atom(
        index,
        cores[index],
        Q(box["t"][0]), Q(box["t"][1]),
        Q(box["p"][0]), Q(box["p"][1]),
        Q(box["s"][0]), Q(box["s"][1]),
        row["dyadic_path"],
    )


def atom_box(atom: adaptive.Atom) -> dict[str, list[str]]:
    return {
        "t": [str(atom.t0), str(atom.t1)],
        "p": [str(atom.p0), str(atom.p1)],
        "s": [str(atom.s0), str(atom.s1)],
    }


def child_row(
    parent: dict[str, Any],
    split_record: dict[str, Any],
    child: adaptive.Atom,
    side: int,
    classification: dict[str, Any],
) -> dict[str, Any]:
    inherited = adaptive.atom_row(
        child,
        classification,
        parent["parent_owner_witness_sha256"],
        bool(parent["midpoint_proposal_promoted_parent"]),
    )
    source_box = atom_box(child)
    require(inherited["source_box"] == source_box, "inherited child box")
    require(inherited["dyadic_path"] == parent["dyadic_path"] + str(side), "child path")
    require(
        Q(inherited["parameter_averaged_unnormalized_base_mass"])
        == Q(parent["parameter_averaged_unnormalized_base_mass"]) / 2,
        "child half mass",
    )
    return {
        "child_atom_id": inherited["atom_id"],
        "parent_atom_id": parent["atom_id"],
        "frozen_split_record_id": split_record["split_record_id"],
        "source_core_index": inherited["source_core_index"],
        "source_core_id": inherited["source_core_id"],
        "parent_dyadic_path": parent["dyadic_path"],
        "child_dyadic_path": inherited["dyadic_path"],
        "parent_depth": parent["depth"],
        "child_depth": inherited["depth"],
        "child_side": side,
        "split_axis": split_record["split_axis"],
        "source_box": source_box,
        "parent_source_box_sha256": canonical_digest(parent["source_box"]),
        "child_source_box_sha256": canonical_digest(source_box),
        "child_path_is_exact_parent_prefix_plus_side": True,
        "child_box_is_exact_scheduled_half": True,
        "sibling_interiors_disjoint_and_union_parent_mod_shared_face": True,
        "strict_next_collision_owner_inherited_from_whole_parent_core": inherited[
            "strict_next_collision_owner_inherited_from_whole_parent_core"
        ],
        "complete_retained_candidate_comparison_inherited": inherited[
            "complete_retained_candidate_comparison_inherited"
        ],
        "parent_owner_witness_sha256": inherited["parent_owner_witness_sha256"],
        "fresh_whole_box_Arb_precision_bits": 384,
        "classification": inherited["classification"],
        "destination_core_id": inherited["destination_core_id"],
        "classification_witness_rows_sha256": inherited[
            "classification_witness_rows_sha256"
        ],
        "output_enclosures": inherited["output_enclosures"],
        "parameter_averaged_unnormalized_base_mass": inherited[
            "parameter_averaged_unnormalized_base_mass"
        ],
        "parameter_averaged_unnormalized_collision_mass_lower": inherited[
            "parameter_averaged_unnormalized_collision_mass_lower"
        ],
        "parameter_averaged_unnormalized_collision_mass_upper": inherited[
            "parameter_averaged_unnormalized_collision_mass_upper"
        ],
        "canonical_invariant_area_coordinates": inherited[
            "canonical_invariant_area_coordinates"
        ],
        "absolute_inverse_invariant_area_Jacobian": inherited[
            "absolute_inverse_invariant_area_Jacobian"
        ],
        "log_invariant_area_Jacobian_distortion": inherited[
            "log_invariant_area_Jacobian_distortion"
        ],
    }


def compact_replay() -> dict[str, Any]:
    adaptive_manifest, f789_manifest = load_dependencies()
    adaptive_rows = adaptive_manifest["result"]["adaptive_full_core_step1_raw_leaf_rows"]
    require(isinstance(adaptive_rows, list) and len(adaptive_rows) == 33960, "adaptive rows")
    unresolved = [
        row for row in adaptive_rows
        if row.get("classification") == "UNRESOLVED_OUTER"
    ]
    require(len(unresolved) == FROZEN_PARENT_COUNT, "unresolved parent count")
    unresolved.sort(key=lambda row: (row["source_core_index"], row["dyadic_path"]))
    parent_boxes = parent_core_boxes(adaptive_rows)
    cores = adaptive.core_cert.physical_cores()
    require(len(cores) == 24, "physical core count")

    split_rows: list[dict[str, Any]] = []
    split_boxes_by_parent: dict[str, list[dict[str, list[str]]]] = {}
    split_record_by_parent: dict[str, dict[str, Any]] = {}
    parent_mass = Q(0)
    axis_histogram: Counter[str] = Counter()
    for parent in unresolved:
        require(parent["strict_next_collision_owner_inherited_from_whole_parent_core"] is True, "parent first owner")
        require(parent["complete_retained_candidate_comparison_inherited"] is True, "parent comparison")
        split_record, boxes = frozen_split_record(
            parent, parent_boxes[parent["source_core_index"]]
        )
        split_rows.append(split_record)
        split_record_by_parent[parent["atom_id"]] = split_record
        split_boxes_by_parent[parent["atom_id"]] = boxes
        parent_mass += Q(split_record["parent_base_mass"])
        axis_histogram[split_record["split_axis"]] += 1
    split_rows.sort(key=lambda row: row["parent_atom_id"])
    require(canonical_digest(split_rows) == FROZEN_SPLIT_ROWS_SHA256, "frozen split plan digest")
    require(parent_mass == FROZEN_PARENT_MASS, "frozen parent mass")

    frozen_plan = f789_manifest["result"]["unresolved_outer_next_generation_split_plan"]
    require(frozen_plan["current_unresolved_parent_count"] == FROZEN_PARENT_COUNT, "F789 parent count")
    require(frozen_plan["planned_next_generation_child_count"] == FROZEN_CHILD_COUNT, "F789 child count")
    require(Q(frozen_plan["planned_next_generation_base_mass"]) == FROZEN_PARENT_MASS, "F789 mass")
    require(frozen_plan["planned_split_record_rows_sha256"] == FROZEN_SPLIT_ROWS_SHA256, "F789 split digest")
    require(frozen_plan["next_split_axis_histogram"] == dict(sorted(axis_histogram.items())), "F789 axes")
    require(
        frozen_plan["representative_split_records"]
        == [split_rows[0], split_rows[len(split_rows) // 2], split_rows[-1]],
        "F789 representative split records",
    )

    rows: list[dict[str, Any]] = []
    parent_groups: list[dict[str, Any]] = []
    all_child_ids: set[str] = set()
    for parent in unresolved:
        parent_atom = atom_from_row(parent, cores)
        children = adaptive.split_atom(parent_atom)
        split_record = split_record_by_parent[parent["atom_id"]]
        scheduled_boxes = split_boxes_by_parent[parent["atom_id"]]
        require([atom_box(child) for child in children] == scheduled_boxes, "scheduled child geometry")
        group_child_rows: list[dict[str, Any]] = []
        for side, child in enumerate(children):
            classification = adaptive.classify_atom(child, cores)
            row = child_row(parent, split_record, child, side, classification)
            require(row["child_atom_id"] not in all_child_ids, "duplicate child atom")
            all_child_ids.add(row["child_atom_id"])
            rows.append(row)
            group_child_rows.append(row)
        require(
            sum(Q(row["parameter_averaged_unnormalized_base_mass"]) for row in group_child_rows)
            == Q(parent["parameter_averaged_unnormalized_base_mass"]),
            "per-parent child mass conservation",
        )
        parent_groups.append({
            "parent_atom_id": parent["atom_id"],
            "frozen_split_record_id": split_record["split_record_id"],
            "child_atom_ids": [row["child_atom_id"] for row in group_child_rows],
            "child_classifications": [row["classification"] for row in group_child_rows],
            "child_base_masses": [
                row["parameter_averaged_unnormalized_base_mass"]
                for row in group_child_rows
            ],
            "exact_child_mass_sum_equals_parent": True,
        })

    rows.sort(key=lambda row: (row["source_core_index"], row["child_dyadic_path"]))
    parent_groups.sort(key=lambda row: row["parent_atom_id"])
    require(len(rows) == FROZEN_CHILD_COUNT, "child row count")
    require(len(all_child_ids) == FROZEN_CHILD_COUNT, "unique child ids")
    require(len(parent_groups) == FROZEN_PARENT_COUNT, "parent group count")
    for index in range(24):
        paths = [
            row["child_dyadic_path"] for row in rows
            if row["source_core_index"] == index
        ]
        require(len(paths) == len(set(paths)), "unique child path")
        paths.sort()
        require(
            not any(right.startswith(left) for left, right in zip(paths, paths[1:])),
            "child prefix-free ownership",
        )

    histogram = Counter(row["classification"] for row in rows)
    masses = {
        kind: sum(
            Q(row["parameter_averaged_unnormalized_base_mass"])
            for row in rows if row["classification"] == kind
        )
        for kind in CLASSIFICATIONS
    }
    require(dict(sorted(histogram.items())) == EXPECTED_CLASSIFICATION_HISTOGRAM, "fresh histogram")
    require(masses == EXPECTED_CLASSIFICATION_MASSES, "fresh class masses")
    require(sum(masses.values()) == FROZEN_PARENT_MASS, "global child mass conservation")
    unresolved_ratio = masses["UNRESOLVED_OUTER"] / FROZEN_PARENT_MASS
    resolved_ratio = 1 - unresolved_ratio
    require(unresolved_ratio == Q(38701, 44519), "unresolved ratio")
    require(resolved_ratio == Q(5818, 44519), "resolved ratio")
    require(unresolved_ratio < Q(7, 8), "one-generation unresolved decay benchmark")
    require(resolved_ratio > Q(1, 8), "one-generation resolved benchmark")

    depth_class: Counter[tuple[int, str]] = Counter(
        (row["child_depth"], row["classification"]) for row in rows
    )
    require(sum(depth_class.values()) == FROZEN_CHILD_COUNT, "depth histogram total")
    source_summary: list[dict[str, Any]] = []
    for index in range(24):
        source_rows = [row for row in rows if row["source_core_index"] == index]
        source_core_ids = {
            row["source_core_id"] for row in adaptive_rows
            if row["source_core_index"] == index
        }
        require(len(source_core_ids) == 1, "source core id binding")
        source_summary.append({
            "source_core_index": index,
            "source_core_id": next(iter(source_core_ids)),
            "child_count": len(source_rows),
            "classification_histogram": {
                kind: sum(row["classification"] == kind for row in source_rows)
                for kind in CLASSIFICATIONS
            },
            "classification_base_masses": {
                kind: str(sum(
                    Q(row["parameter_averaged_unnormalized_base_mass"])
                    for row in source_rows if row["classification"] == kind
                ))
                for kind in CLASSIFICATIONS
            },
        })

    destination_ids = {
        row["destination_core_id"] for row in rows
        if row["classification"] == "RETURN_AT_1_INNER"
    }
    representative_indices = {0, len(rows) // 4, len(rows) // 2, 3 * len(rows) // 4, len(rows) - 1}
    for kind in CLASSIFICATIONS:
        representative_indices.add(next(
            index for index, row in enumerate(rows) if row["classification"] == kind
        ))
    representatives = [rows[index] for index in sorted(representative_indices)]

    class_frontier_digests = {
        kind: canonical_digest([
            row for row in rows if row["classification"] == kind
        ])
        for kind in CLASSIFICATIONS
    }
    result: dict[str, Any] = {
        "schema": RESULT_SCHEMA,
        "provenance": {
            "dependency_sha256": dict(DEPENDENCIES),
            "old_artifacts_modified": False,
            "aggregate_or_recursive_root_modified": False,
            "admission_engine": "python-flint Arb",
            "precision_bits": 384,
            "classification_policy": "fresh_strict_whole_box_trichotomy_fail_closed",
            "clock": "source_core_state_is_time_0_and_next_collision_is_time_1",
        },
        "frozen_round25_split_plan_replay": {
            "unresolved_parent_count": FROZEN_PARENT_COUNT,
            "scheduled_child_count": FROZEN_CHILD_COUNT,
            "split_axis_histogram": dict(sorted(axis_histogram.items())),
            "parent_base_mass": str(parent_mass),
            "planned_split_record_rows_sha256": canonical_digest(split_rows),
            "representative_split_records": [
                split_rows[0], split_rows[len(split_rows) // 2], split_rows[-1]
            ],
            "exact_match_to_frozen_F789_plan": True,
        },
        "child_parent_prefix_ownership_registry": {
            "parent_count": FROZEN_PARENT_COUNT,
            "children_per_parent": 2,
            "child_count": FROZEN_CHILD_COUNT,
            "unique_child_atom_id_count": len(all_child_ids),
            "all_child_paths_are_exact_parent_path_plus_side": True,
            "all_sibling_interiors_disjoint": True,
            "all_sibling_unions_equal_parent_mod_shared_face": True,
            "all_per_parent_child_mass_sums_exact": True,
            "all_child_paths_prefix_free_within_source_core": True,
            "all_next_collision_first_owner_witnesses_inherited_by_subset": True,
            "all_complete_candidate_comparisons_inherited_by_subset": True,
            "parent_group_rows_sha256": canonical_digest(parent_groups),
            "sorted_child_atom_ids_sha256": canonical_digest(sorted(all_child_ids)),
        },
        "fresh_child_trichotomy_registry": {
            "fresh_whole_box_Arb_child_count": len(rows),
            "classification_histogram": dict(sorted(histogram.items())),
            "classification_base_masses": {
                kind: str(masses[kind]) for kind in CLASSIFICATIONS
            },
            "classification_base_mass_sum": str(sum(masses.values())),
            "child_depth_classification_histogram": {
                str(depth): {
                    kind: depth_class[(depth, kind)] for kind in CLASSIFICATIONS
                }
                for depth in sorted({depth for depth, _kind in depth_class})
            },
            "residual_unresolved_base_mass_ratio_of_parent": str(unresolved_ratio),
            "newly_resolved_base_mass_ratio_of_parent": str(resolved_ratio),
            "residual_unresolved_ratio_strict_upper_benchmark": "7/8",
            "newly_resolved_ratio_strict_lower_benchmark": "1/8",
            "return_destination_core_count": len(destination_ids),
            "source_core_summary_rows": source_summary,
            "source_core_summary_rows_sha256": canonical_digest(source_summary),
            "raw_child_rows_sha256": canonical_digest(rows),
            "class_frontier_rows_sha256": class_frontier_digests,
            "representative_child_rows": representatives,
            "all_three_classes_are_nonempty": all(histogram[kind] > 0 for kind in CLASSIFICATIONS),
            "residual_unresolved_frontier_is_nonempty": histogram["UNRESOLVED_OUTER"] > 0,
        },
        "compact_ledger_contract": {
            "all_53752_child_rows_materialized_during_replay": True,
            "manifest_retains_canonical_digests_and_representative_rows": True,
            "independent_verifier_reconstructs_every_child_and_every_classification": True,
            "deterministic_full_replay_from_frozen_parents_and_split_policy": True,
        },
        "strict_nonpromotion": {
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
        },
    }
    result["internal_replay_digest"] = result_digest(result)
    return result


def verdict() -> dict[str, Any]:
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


def write_manifest(path: Path, verifier_path: Path) -> None:
    result = compact_replay()
    manifest = {
        "schema": MANIFEST_SCHEMA,
        "certificate_sha256": sha256_path(Path(__file__).resolve()),
        "verifier_sha256": sha256_path(verifier_path.resolve()),
        "dependencies": dict(DEPENDENCIES),
        "result": result,
        "verdict": verdict(),
    }
    path.write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-manifest", type=Path)
    parser.add_argument(
        "--verifier",
        type=Path,
        default=HERE / "cm2_gate34_round26_unresolved_child_replay_verifier.py",
    )
    parser.add_argument("--summary", action="store_true")
    args = parser.parse_args()
    if args.write_manifest is not None:
        write_manifest(args.write_manifest, args.verifier)
        print(f"wrote {args.write_manifest}")
        return 0
    result = compact_replay()
    registry = result["fresh_child_trichotomy_registry"]
    print("ROUND26_FROZEN_SPLIT_PLAN_REPLAY: CERTIFIED")
    print("ROUND26_CHILD_PARENT_PREFIX_OWNERSHIP: CERTIFIED")
    print("ROUND26_FRESH_384_BIT_CHILD_TRICHOTOMY: CERTIFIED")
    print(f"CHILD_COUNT: {registry['fresh_whole_box_Arb_child_count']}")
    print(f"CLASSIFICATION_HISTOGRAM: {registry['classification_histogram']}")
    print(f"CLASSIFICATION_BASE_MASSES: {registry['classification_base_masses']}")
    print(
        "RESIDUAL_UNRESOLVED_RATIO: "
        + registry["residual_unresolved_base_mass_ratio_of_parent"]
        + " < 7/8"
    )
    print("COMPLETE_STEP1_R1_Q1_PARTITION: NOT_CERTIFIED")
    print("GATE5: NOT_CERTIFIED")
    print("CM2: NO-GO_FOR_CLAIM")
    return 0 if args.summary else 2


if __name__ == "__main__":
    sys.exit(main())
