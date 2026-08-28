#!/usr/bin/env python3
"""Round176 formal whole-parent exclusion for 182 multi-candidate origins.

The producer reconstructs the 2,616 owner-active source-W multi-candidate
parents and their depth-8-to-14 longest-axis trees.  It then applies the
bounded dimension-safe closures first explored in Round170, but promotes only
an original depth-8 parent for which every dyadic descendant and every
necessary analytic stratum is excluded.

Round170 child counts and rational volumes are not integer ledger credit.
The integer delta is exactly the number of completely replaced original
parents.  Two rational atlas parents meet the true source-chart boundary;
only their physical portions are credited and the exterior guard band is
explicitly non-credit.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter, defaultdict
from fractions import Fraction as Q
from pathlib import Path
from typing import Any

from flint import ctx

import cm2_round166_multi_candidate_refinement_prototype as r166
import cm2_round170_bounded_dimension_safe_graph_cells as r170


HERE = Path(__file__).resolve().parent
OUTPUT = (
    HERE
    / "cm2_round176_dimension_safe_multi_origin_parent_exclusion_certificate.json"
)
SCHEMA = "cm2.round176.dimension-safe-multi-origin-parent-exclusion.v1"

# Round170 is used only as producer-side executable geometry.  The Round176
# verifier independently reimplements the tree and every closure from Gate3.
PINS = {
    "cm2_gate3_candidate_first_hit_cert.py":
        "6d224d74cda186a40ef9956d1dd6556d5a7b9f506d47c942427ceb66fd705bd2",
    "cm2_gate3_ge_interval_atlas_cert.py":
        "ab120f85a263f3cb0697d8a40bc9ed2bf12b361aa7c54940c214b6fd85b17e2b",
    "cm2_gate3_eight_cell_symmetry_atlas_cert.py":
        "d867f5cb03691289033d1a0d0e277a03e8395d70aae7e0689446d7aa63eac3da",
    "cm2-gate3-chart-seam-quotient-manifest-2026-07-15.json":
        "1fb40060336f04f28a7cac19a70abdd3692ced272825b2f1f6b6ae005f00518b",
    "cm2_round166_multi_candidate_refinement_prototype.py":
        "6479a78249a717169dea55ecabae98c05f240ea323fa0370037d43339158ae7c",
    "cm2_round170_bounded_dimension_safe_graph_cells.py":
        "952ac26c6729a02e3c5c364c8dda89cdc19b756ac46f7d5da01786fa1b7ca75f",
    "cm2_round172_dimension_safe_tangency_parent_frozen_owner_absence_pruning.py":
        "81f147cf6106d7436df282de106fc47e793e8f97a43282b35719e28182e07980",
    "cm2_round172_dimension_safe_tangency_parent_frozen_owner_absence_pruning_certificate.json":
        "3185188c476a64d3e732674fa724ce9a49afe84c61abab448f746a5a3555b66c",
    "cm2_round172_dimension_safe_tangency_parent_frozen_owner_absence_pruning_verification.json":
        "d095ecdd1b59a6577f96f0317f8a30122e8cd3f6baf73ed550c5d227ed1811c3",
    "cm2_round175_dimension_safe_tangency_arrangement.py":
        "16122dcc7c39b140d45139a01bac6d6f41d7cbb60da2499ecc50fbeac2766355",
    "cm2_round175_dimension_safe_tangency_arrangement_certificate.json":
        "a2a69b3d4559fadb647d8f9ea6a06ef4c1625647965423cdb25f53fa08d2deee",
    "cm2_round175_dimension_safe_tangency_arrangement_verifier.py":
        "2c8a5906806adef423ba5d409cbf294c4988db72a1b9cfdf26a61ee9a7d290e6",
    "cm2_round175_dimension_safe_tangency_arrangement_verification.json":
        "6f1d8e515be0cdc977445e7e0d8633df510c793ff99e0f76cf3b4578d2d2bfca",
    "cm2_round175_dimension_safe_tangency_arrangement_manifest.sha256":
        "0ad7140947512de88f5ff4badd5a925c78b9f605be1f519841485f41b9139dc3",
}
ROUND172_RESULT = (
    "a436b4a82b1e8d5c617fe576e0e4e76b6f6f38ad8ac3eda4ddde544c2769a776"
)
ROUND172_VERIFICATION_RESULT = (
    "aa0fb2c28176cf46b058506658a21070679e0a91a4f94ed65245fb378e088603"
)
ROUND175_RESULT = (
    "827d6f674dd4a5291bf08f5ffd65b31187faa1c9fe977e1b7e7da10cd1166d72"
)
ROUND175_VERIFICATION_RESULT = (
    "ed5fd96874a65b49a1e05d5589e2dd9711f224d08a99123e582bc54bce294f6a"
)


def canonical(value: Any) -> str:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    )


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value).encode()).hexdigest()


def require(condition: bool, label: str) -> None:
    if not condition:
        raise RuntimeError(label)


def strict_load(path: Path) -> dict[str, Any]:
    raw = path.read_bytes()
    require(
        not raw.startswith(b"\xef\xbb\xbf") and b"\x00" not in raw,
        f"encoding:{path.name}",
    )

    def reject(value: str) -> None:
        raise ValueError(value)

    def unique(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in pairs:
            require(key not in result, f"duplicate:{path.name}:{key}")
            result[key] = value
        return result

    value = json.loads(
        raw.decode(),
        object_pairs_hook=unique,
        parse_constant=reject,
        parse_float=reject,
    )
    require(type(value) is dict, f"top:{path.name}")
    return value


def check_chain() -> dict[str, Any]:
    for name, expected in PINS.items():
        actual = hashlib.sha256((HERE / name).read_bytes()).hexdigest()
        require(actual == expected, f"pin:{name}:{actual}")
    certificate = strict_load(
        HERE
        / "cm2_round172_dimension_safe_tangency_parent_frozen_owner_absence_pruning_certificate.json"
    )
    verification = strict_load(
        HERE
        / "cm2_round172_dimension_safe_tangency_parent_frozen_owner_absence_pruning_verification.json"
    )
    require(
        certificate["result_sha256"] == ROUND172_RESULT,
        "Round172 result identity",
    )
    require(
        verification["result_sha256"] == ROUND172_VERIFICATION_RESULT
        and verification["result"]["status"] == "PASS",
        "Round172 verification identity",
    )
    require(
        certificate["result"]["Round168_to_Round172_composition"][
            "combined_whole_record_excluded"
        ] == 73172
        and certificate["result"]["Round168_to_Round172_composition"][
            "Round172_conservative_live"
        ] == 3660,
        "Round172 ledger",
    )
    r175 = strict_load(
        HERE
        / "cm2_round175_dimension_safe_tangency_arrangement_certificate.json"
    )
    r175v = strict_load(
        HERE
        / "cm2_round175_dimension_safe_tangency_arrangement_verification.json"
    )
    require(
        r175["result_sha256"] == ROUND175_RESULT,
        "Round175 result identity",
    )
    require(
        r175v["result_sha256"] == ROUND175_VERIFICATION_RESULT
        and r175v["result"]["status"] == "PASS",
        "Round175 verification identity",
    )
    r175_ledger = r175v["result"]["ledger_reconstruction"]
    require(
        r175_ledger["combined_whole_record_excluded"] == 73178
        and r175_ledger["Round175_conservative_live"] == 3654
        and r175_ledger["Round175_new_whole_parent_excluded"] == 6,
        "Round175 ledger",
    )
    manifest_rows = {}
    for line in (
        HERE
        / "cm2_round175_dimension_safe_tangency_arrangement_manifest.sha256"
    ).read_text().splitlines():
        value, name = line.split("  ", 1)
        require(name not in manifest_rows, f"Round175 manifest duplicate:{name}")
        manifest_rows[name] = value
    expected_manifest_rows = {
        "cm2_round175_dimension_safe_tangency_arrangement.py":
            PINS["cm2_round175_dimension_safe_tangency_arrangement.py"],
        "cm2_round175_dimension_safe_tangency_arrangement_certificate.json":
            PINS[
                "cm2_round175_dimension_safe_tangency_arrangement_certificate.json"
            ],
        "cm2_round175_dimension_safe_tangency_arrangement_verifier.py":
            PINS[
                "cm2_round175_dimension_safe_tangency_arrangement_verifier.py"
            ],
        "cm2_round175_dimension_safe_tangency_arrangement_verification.json":
            PINS[
                "cm2_round175_dimension_safe_tangency_arrangement_verification.json"
            ],
        "cm2_round175_dimension_safe_tangency_arrangement_report.md":
            "bfdb125f9b77a4d2abeb1eaa8229dbd8bff163c5ed642cc317129c6bc9f48ae4",
    }
    require(
        manifest_rows == expected_manifest_rows
        and all(
            hashlib.sha256((HERE / name).read_bytes()).hexdigest() == value
            for name, value in manifest_rows.items()
        ),
        "Round175 manifest replay",
    )
    return {
        "file_sha256": dict(sorted(PINS.items())),
        "Round172_result_sha256": ROUND172_RESULT,
        "Round172_verification_result_sha256":
            ROUND172_VERIFICATION_RESULT,
        "Round175_result_sha256": ROUND175_RESULT,
        "Round175_verification_result_sha256":
            ROUND175_VERIFICATION_RESULT,
        "Round175_manifest_entries_replayed": True,
    }


def coarse(disposition: str) -> str:
    if disposition.startswith("EXCLUDED"):
        return "EXCLUDED"
    if disposition.startswith("LIVE"):
        return "LIVE"
    raise RuntimeError(f"unknown disposition:{disposition}")


def box_row(box: Any) -> dict[str, Any]:
    return {
        "t": [str(box.t0), str(box.t1)],
        "p": [str(box.p0), str(box.p1)],
        "s": [str(box.s0), str(box.s1)],
        "ambient_dimension": 3,
    }


def map_counter(value: Counter[Any]) -> dict[str, int]:
    return {
        str(key): count for key, count in sorted(value.items())
    }


def fraction_map(value: dict[str, Q]) -> dict[str, str]:
    return {
        key: str(item) for key, item in sorted(value.items())
    }


def replay_tree() -> dict[str, Any]:
    r166.install_fast_readonly_replay()
    charts = r166.baseline_fast()
    pending: list[r166.Node] = []
    origins: dict[str, dict[str, Any]] = {}
    for chart_id, leaves in charts.items():
        for leaf in leaves:
            if (
                leaf.classification == "multi_candidate"
                and r166.FROZEN_OWNER in leaf.active_targets
            ):
                key = f"{chart_id}:{leaf.box.path}"
                require(key not in origins, f"duplicate origin:{key}")
                origins[key] = {
                    "chart_id": chart_id,
                    "path": leaf.box.path,
                    "box": leaf.box,
                    "active_targets": tuple(leaf.active_targets),
                }
                pending.append(
                    r166.Node(
                        chart_id,
                        leaf.box,
                        leaf.active_targets,
                        leaf.box.path,
                    )
                )
    require(len(origins) == 2616, f"owner-active:{len(origins)}")

    frontier: list[r170.FrontierRow] = []
    prior: dict[str, list[dict[str, Any]]] = defaultdict(list)
    origin_kinds: dict[str, set[str]] = defaultdict(set)
    evaluated_by_origin: Counter[str] = Counter()
    evaluated_boxes = 0
    evaluated_records = 0
    for relative_depth in range(7):
        next_pending: list[r166.Node] = []
        for node in pending:
            origin = f"{node.chart_id}:{node.origin_path}"
            evaluated_by_origin[origin] += 1
            evaluated_boxes += 1
            evaluated_records += len(node.active_targets)
            leaf, records = r166.classify_active(
                node.chart_id, node.box, node.active_targets
            )
            disposition, margins = r166.terminal_disposition(
                node.chart_id, leaf
            )
            if disposition is not None:
                row = {
                    "leaf_key": f"{node.chart_id}:{node.box.path}",
                    "relative_depth": relative_depth,
                    "dimension": 3,
                    "disposition": disposition,
                    "coverage_numerator_64": 2 ** (6 - relative_depth),
                }
                if margins is not None:
                    row["closed_interval_outgoing_margin_signs"] = {
                        key: (
                            "POSITIVE"
                            if bool(value > 0)
                            else (
                                "NEGATIVE"
                                if bool(value < 0)
                                else "OVERWRAPPED"
                            )
                        )
                        for key, value in sorted(margins.items())
                    }
                prior[origin].append(row)
                origin_kinds[origin].add(coarse(disposition))
                continue
            failure = r166.unresolved_failure(
                node.chart_id, leaf, records, margins
            )
            inherited = (
                (r166.FROZEN_OWNER,)
                if leaf.classification == "unique_first"
                else (
                    node.active_targets
                    if leaf.classification == "tangency_graph"
                    else leaf.active_targets
                )
            )
            if relative_depth == 6:
                frontier.append(
                    r170.FrontierRow(
                        node.chart_id,
                        node.box,
                        inherited,
                        origin,
                        failure,
                    )
                )
            else:
                axis = r166.longest_axis(node.box)
                next_pending.extend(
                    r166.Node(
                        node.chart_id,
                        child,
                        inherited,
                        node.origin_path,
                    )
                    for child in r166.split_axis(node.box, axis)
                )
        pending = next_pending

    require(
        len(frontier) == 56780
        and evaluated_boxes == 167984
        and evaluated_records == 415570,
        "depth14 workload",
    )
    require(
        Counter(row.failure for row in frontier)
        == {
            "OUTGOING_CHART_SEAM_OVERWRAP": 7510,
            "SOURCE_GRAZING_ENDPOINT_COLLAR": 1632,
            "TYPED_FROZEN_OWNER_TANGENCY_GRAPH_COLLAR": 80,
            "TYPED_OWNER_MISMATCH_TANGENCY_GRAPH_COLLAR": 1140,
            "UNTYPED_DISCRIMINANT_COLLAR": 46418,
        },
        "frontier census",
    )
    return {
        "origins": origins,
        "frontier": frontier,
        "prior": prior,
        "origin_kinds": origin_kinds,
        "evaluated_by_origin": evaluated_by_origin,
        "workload": {
            "evaluated_box_count": evaluated_boxes,
            "evaluated_target_record_count": evaluated_records,
        },
    }


def closure(row: r170.FrontierRow) -> tuple[str | None, dict[str, Any]]:
    basic = {
        "leaf_key": row.leaf_key,
        "failure": row.failure,
        "ambient_parent_dimension": 3,
    }
    if row.failure == "OUTGOING_CHART_SEAM_OVERWRAP":
        kind, classes, depths = r170.h_partition(
            row.chart_id, row.box, row.origin_key
        )
        terminal_count = sum(classes.values())
        volume = sum(
            Q(count, 2 ** depth) for depth, count in depths.items()
        )
        require(kind is not None and volume == 1, "H closure")
        return kind, {
            **basic,
            "method": "OUTGOING_H_CLOSED_RECTANGLE_TREE",
            "outcome": kind,
            "terminal_evidence": map_counter(classes),
            "terminal_count_by_extra_depth": map_counter(depths),
            "terminal_closed_3D_cell_count": terminal_count,
            "internal_split_2D_face_count": terminal_count - 1,
            "relative_3D_coverage": str(volume),
        }

    if row.failure in {
        "TYPED_FROZEN_OWNER_TANGENCY_GRAPH_COLLAR",
        "TYPED_OWNER_MISMATCH_TANGENCY_GRAPH_COLLAR",
    }:
        records, unresolved = r170.unique_unresolved_discriminant(row)
        closed, witness = r170.close_typed_tangency(row)
        return (
            "EXCLUDED" if closed else None,
            {
                **basic,
                "method": "TYPED_DELTA_THREE_STRATUM",
                "outcome": "EXCLUDED" if closed else "RESIDUAL",
                "target": (
                    unresolved[0].target_id
                    if len(unresolved) == 1
                    else "NONUNIQUE"
                ),
                "active_target_count": len(records),
                "terminal_evidence": witness,
                "strata": [
                    {"predicate": "Delta<0", "dimension": 3},
                    {"predicate": "Delta=0", "dimension": 2},
                    {"predicate": "Delta>0", "dimension": 3},
                ],
                "graph_boundary": {
                    "one_dimensional_edge_count": 4,
                    "zero_dimensional_corner_count": 4,
                    "p_faces_met": False,
                },
                "relative_3D_coverage": "1",
            },
        )

    if row.failure == "UNTYPED_DISCRIMINANT_COLLAR":
        records, unresolved = r170.unique_unresolved_discriminant(row)
        if len(unresolved) != 1:
            return None, {
                **basic,
                "method": "MULTI_DELTA_RESIDUAL",
                "outcome": "RESIDUAL",
                "unresolved_target_count": len(unresolved),
            }
        candidate = unresolved[0]
        derivative_sign, lower, upper, full = r170.graph_faces(
            row, candidate
        )
        same_sign = (
            derivative_sign != 0
            and r170.sign(lower) != 0
            and r170.sign(lower) == r170.sign(upper)
        )
        if not same_sign:
            return None, {
                **basic,
                "method": (
                    "FULL_P_DELTA_GRAPH_RESIDUAL"
                    if full
                    else "CLIPPED_DELTA_RESIDUAL"
                ),
                "outcome": "RESIDUAL",
                "target": candidate.target_id,
            }
        kind, witness = r170.close_same_sign_discriminant(
            row,
            records,
            candidate,
            derivative_sign,
            lower,
            upper,
        )
        require(kind is not None, "same-sign closure")
        return kind, {
            **basic,
            "method": "SAME_SIGN_MONOTONE_DELTA_RECTANGLE",
            "outcome": kind,
            "target": candidate.target_id,
            "strict_derivative_sign":
                "POSITIVE" if derivative_sign > 0 else "NEGATIVE",
            "strict_common_p_face_sign":
                "POSITIVE" if r170.sign(lower) > 0 else "NEGATIVE",
            "terminal_evidence": witness,
            "delta_zero_graph_present": False,
            "terminal_closed_3D_cell_count": 1,
            "relative_3D_coverage": "1",
        }

    require(
        row.failure == "SOURCE_GRAZING_ENDPOINT_COLLAR",
        f"failure dispatch:{row.failure}",
    )
    profile = r170.profile_grazing(row)
    kind = profile["parent_kind"]
    terminal_count = sum(profile["terminal_counts"].values())
    return kind, {
        **basic,
        "method": "COMPACT_Q_CLOSED_CELL_TREE",
        "outcome": kind if kind is not None else "RESIDUAL",
        "coordinate": {
            "r": "[0,1]",
            "q": "sqrt(1023/262144)*r",
            "p": "sign*sqrt(1-(1023/262144)*r^2)",
        },
        "grazing_face": {
            "predicate": "r=0",
            "dimension": 2,
            "classification": profile["face_classification"],
        },
        "interior_predicate": "r>0",
        "interior_dimension": 3,
        "terminal_evidence": map_counter(profile["terminal_counts"]),
        "terminal_count_by_extra_depth":
            map_counter(profile["terminal_depths"]),
        "terminal_closed_3D_cell_count": terminal_count,
        "internal_split_2D_face_count":
            terminal_count + sum(profile["residual_counts"].values()) - 1,
        "terminal_volume_by_disposition":
            fraction_map(profile["terminal_volume"]),
        "classified_relative_3D_coverage":
            str(profile["classified_volume"]),
        "residual_relative_3D_coverage":
            str(profile["residual_volume"]),
        "relative_3D_coverage": str(
            profile["classified_volume"] + profile["residual_volume"]
        ),
    }


def physical_domain(chart_id: str, box: Any) -> dict[str, Any]:
    minimum_abs = (
        Q(0)
        if box.t0 <= 0 <= box.t1
        else min(abs(box.t0), abs(box.t1))
    )
    maximum_abs = max(abs(box.t0), abs(box.t1))
    if 2 * maximum_abs * maximum_abs < 1:
        classification = "STRICT_PHYSICAL_CHART_INTERIOR"
    elif 2 * minimum_abs * minimum_abs > 1:
        classification = "RATIONAL_GUARD_ONLY"
    else:
        classification = "PHYSICAL_CHART_SEAM_AND_GUARD_COMPOSITE"
    return {
        "classification": classification,
        "physical_interior_predicate": "2*t^2<1",
        "source_seam_predicate": "2*t^2=1",
        "source_seam_dimension": (
            2
            if classification
            == "PHYSICAL_CHART_SEAM_AND_GUARD_COMPOSITE"
            else None
        ),
        "source_seam_half_open_owner": (
            "E"
            if classification
            == "PHYSICAL_CHART_SEAM_AND_GUARD_COMPOSITE"
            else None
        ),
        "guard_predicate": "2*t^2>1",
        "guard_outside_exterior_credit": 0,
        "guard_only_parent": classification == "RATIONAL_GUARD_ONLY",
        "physical_positive_volume_present":
            classification != "RATIONAL_GUARD_ONLY",
    }


def origin_summary(
    key: str,
    meta: dict[str, Any],
    prior: list[dict[str, Any]],
    evidence: list[dict[str, Any]],
    evaluated_count: int,
) -> dict[str, Any]:
    prior_counts = Counter(row["disposition"] for row in prior)
    prior_depths = Counter(row["relative_depth"] for row in prior)
    prior_units = sum(row["coverage_numerator_64"] for row in prior)
    frontier_count = len(evidence)
    require(prior_units + frontier_count == 64, f"coverage:{key}")
    terminal_leaf_count = len(prior) + frontier_count
    require(
        evaluated_count == 2 * terminal_leaf_count - 1,
        f"binary tree:{key}",
    )
    methods = Counter(row["method"] for row in evidence)
    proof_classes: Counter[str] = Counter()
    dimension_counts: Counter[int] = Counter()
    needed: set[str] = set()
    for row in prior:
        dimension_counts[3] += 1
        proof_classes[f"PRIOR:{row['disposition']}"] += 1
    for row in evidence:
        method = row["method"]
        proof_classes[f"{method}:{row['outcome']}"] += 1
        if method == "OUTGOING_H_CLOSED_RECTANGLE_TREE":
            dimension_counts[3] += row["terminal_closed_3D_cell_count"]
            dimension_counts[2] += row["internal_split_2D_face_count"]
            needed.add("closed split faces and their lower-dimensional intersections")
        elif method == "TYPED_DELTA_THREE_STRATUM":
            dimension_counts[3] += 2
            dimension_counts[2] += 1
            dimension_counts[1] += 4
            dimension_counts[0] += 4
            needed.add("Delta=0 graph, graph edges, and graph corners")
        elif method == "SAME_SIGN_MONOTONE_DELTA_RECTANGLE":
            dimension_counts[3] += 1
        elif method == "COMPACT_Q_CLOSED_CELL_TREE":
            dimension_counts[3] += row["terminal_closed_3D_cell_count"]
            dimension_counts[2] += (
                row["internal_split_2D_face_count"] + 1
            )
            needed.add("r=0 grazing face and closed q-tree split faces")
        else:
            raise RuntimeError(f"unexpected credited method:{method}")
    source = physical_domain(meta["chart_id"], meta["box"])
    if source["source_seam_dimension"] == 2:
        dimension_counts[2] += 1
        needed.add(
            "physical source seam and all dimension-at-most-one "
            "intersections with analytic/split strata"
        )
    row = {
        "origin_key": key,
        "chart_id": meta["chart_id"],
        "atlas_path": meta["path"],
        "parent_box": box_row(meta["box"]),
        "source_chart_domain": source,
        "initial_active_target_count": len(meta["active_targets"]),
        "initial_active_targets_sha256":
            digest(list(meta["active_targets"])),
        "dyadic_replacement_tree": {
            "root_relative_depth": 0,
            "frontier_relative_depth": 6,
            "maximum_absolute_atlas_depth": 14,
            "evaluated_node_count": evaluated_count,
            "internal_binary_split_count": terminal_leaf_count - 1,
            "terminal_leaf_count": terminal_leaf_count,
            "prior_terminal_cell_count": len(prior),
            "prior_terminal_count_by_relative_depth":
                map_counter(prior_depths),
            "prior_terminal_count_by_disposition":
                map_counter(prior_counts),
            "depth14_frontier_cell_count": frontier_count,
            "coverage_numerator_64": prior_units + frontier_count,
            "coverage_denominator": 64,
            "coverage_identity":
                f"{prior_units}+{frontier_count}=64",
            "lower_child_owns_each_split_face": True,
            "closed_interval_enclosures_used_for_both_children": True,
        },
        "analytic_replacement": {
            "frontier_closure_count_by_method": map_counter(methods),
            "terminal_or_required_stratum_count_by_dimension": {
                str(dim): count
                for dim, count in sorted(dimension_counts.items())
            },
            "needed_lower_dimensional_strata": sorted(needed),
            "all_3D_descendants_excluded": True,
            "all_needed_2D_graphs_and_faces_excluded": True,
            "all_needed_1D_and_0D_intersections_excluded": True,
            "closed_interval_strict_proofs_inherit_to_owned_faces":
                True,
            "terminal_proof_class_counts":
                map_counter(proof_classes),
        },
        "terminal_evidence_row_count": len(prior) + len(evidence),
        "terminal_evidence_rows_sha256": digest(
            sorted(
                prior + evidence,
                key=lambda item: item["leaf_key"],
            )
        ),
        "whole_origin_disposition": "EXCLUDED",
        "whole_origin_integer_credit": 1,
    }
    row["row_sha256"] = digest(row)
    return row


def build_result() -> dict[str, Any]:
    upstream = check_chain()
    replay = replay_tree()
    frontier: list[r170.FrontierRow] = replay["frontier"]
    origin_kinds: dict[str, set[str]] = replay["origin_kinds"]
    evidence_by_origin: dict[str, list[dict[str, Any]]] = defaultdict(list)
    closed_by_origin: Counter[str] = Counter()
    category_keys: dict[str, list[str]] = defaultdict(list)
    residual_keys: list[str] = []

    for row in frontier:
        kind, evidence = closure(row)
        if kind is None:
            residual_keys.append(row.leaf_key)
            continue
        category_keys[kind].append(row.leaf_key)
        evidence_by_origin[row.origin_key].append(evidence)
        closed_by_origin[row.origin_key] += 1
        origin_kinds[row.origin_key].add(kind)

    for values in category_keys.values():
        values.sort()
    residual_keys.sort()
    require(
        {
            key: len(values)
            for key, values in sorted(category_keys.items())
        } == {"EXCLUDED": 6250, "LIVE": 3590, "MIXED": 2900}
        and len(residual_keys) == 44040,
        "closure census",
    )
    frontier_by_origin = Counter(row.origin_key for row in frontier)
    fully = [
        key for key in sorted(replay["origins"])
        if closed_by_origin[key] == frontier_by_origin[key]
    ]
    by_kind: dict[str, list[str]] = defaultdict(list)
    for key in fully:
        kinds = origin_kinds[key]
        category = (
            "WHOLE_ORIGIN_PARENT_EXCLUDED"
            if kinds == {"EXCLUDED"}
            else (
                "WHOLE_ORIGIN_PARENT_LIVE"
                if kinds == {"LIVE"}
                else "RESOLVED_MIXED_OR_ANALYTIC_PARTITION"
            )
        )
        by_kind[category].append(key)
    require(
        {
            key: len(value)
            for key, value in sorted(by_kind.items())
        } == {
            "RESOLVED_MIXED_OR_ANALYTIC_PARTITION": 36,
            "WHOLE_ORIGIN_PARENT_EXCLUDED": 182,
            "WHOLE_ORIGIN_PARENT_LIVE": 236,
        },
        "origin aggregation",
    )
    credited = by_kind["WHOLE_ORIGIN_PARENT_EXCLUDED"]
    require(
        digest(credited)
        == "bfb29d76ced106a3d69a3d4c1ebb2271c45a1567197a3e7da93e883cae6c91b3",
        "182 key identity",
    )
    summaries = [
        origin_summary(
            key,
            replay["origins"][key],
            replay["prior"].get(key, []),
            evidence_by_origin[key],
            replay["evaluated_by_origin"][key],
        )
        for key in credited
    ]
    prior_only_origin_keys: list[str] = []
    analytic_origin_keys: list[str] = []
    analytic_origin_keys_by_method: dict[str, list[str]] = defaultdict(list)
    analytic_frontier_closure_counts: Counter[str] = Counter()
    for row in summaries:
        methods = row["analytic_replacement"][
            "frontier_closure_count_by_method"
        ]
        if not methods:
            prior_only_origin_keys.append(row["origin_key"])
            continue
        analytic_origin_keys.append(row["origin_key"])
        require(
            len(methods) == 1,
            f"one analytic method per credited origin:{row['origin_key']}",
        )
        method = next(iter(methods))
        analytic_origin_keys_by_method[method].append(row["origin_key"])
        analytic_frontier_closure_counts.update(methods)
    require(
        len(prior_only_origin_keys) == 164
        and len(analytic_origin_keys) == 18
        and {
            key: len(values)
            for key, values in sorted(
                analytic_origin_keys_by_method.items()
            )
        }
        == {
            "OUTGOING_H_CLOSED_RECTANGLE_TREE": 8,
            "SAME_SIGN_MONOTONE_DELTA_RECTANGLE": 8,
            "TYPED_DELTA_THREE_STRATUM": 2,
        }
        and analytic_frontier_closure_counts
        == {
            "OUTGOING_H_CLOSED_RECTANGLE_TREE": 60,
            "SAME_SIGN_MONOTONE_DELTA_RECTANGLE": 14,
            "TYPED_DELTA_THREE_STRATUM": 32,
        },
        "164 prior-only plus 18 analytic origin decomposition",
    )
    guard_counts = Counter(
        row["source_chart_domain"]["classification"]
        for row in summaries
    )
    crossing = [
        row["origin_key"] for row in summaries
        if row["source_chart_domain"]["classification"]
        == "PHYSICAL_CHART_SEAM_AND_GUARD_COMPOSITE"
    ]
    require(
        guard_counts
        == {
            "STRICT_PHYSICAL_CHART_INTERIOR": 180,
            "PHYSICAL_CHART_SEAM_AND_GUARD_COMPOSITE": 2,
        }
        and crossing
        == [
            "W:E:00.15.00000100",
            "W:E:07.00.11111011",
        ],
        "physical source guard census",
    )

    r172 = strict_load(
        HERE
        / "cm2_round172_dimension_safe_tangency_parent_frozen_owner_absence_pruning_certificate.json"
    )
    tangency_keys = sorted(
        r172["result"]["whole_parent_frozen_owner_absence_credit"][
            "exact_excluded_parent_keys"
        ]
    )
    r175 = strict_load(
        HERE
        / "cm2_round175_dimension_safe_tangency_arrangement_certificate.json"
    )
    round175_new_tangency_keys = sorted(
        r175["result"]["new_whole_parent_exclusion_credit"][
            "exact_parent_keys"
        ]
    )
    require(
        len(tangency_keys) == 10
        and len(round175_new_tangency_keys) == 6
        and not (set(tangency_keys) & set(round175_new_tangency_keys)),
        "Round175 cumulative tangency keys",
    )
    cumulative_tangency_keys = sorted(
        set(tangency_keys) | set(round175_new_tangency_keys)
    )
    require(not (set(tangency_keys) & set(credited)), "credit disjointness")
    require(
        not (set(cumulative_tangency_keys) & set(credited)),
        "Round175 versus Round176 credit disjointness",
    )

    all_frontier = sorted(row.leaf_key for row in frontier)
    all_origins = sorted(replay["origins"])
    result = {
        "status": (
            "CERTIFIED_182_WHOLE_MULTI_CANDIDATE_PARENT_EXCLUSIONS__"
            "DIMENSION_SAFE__D02_STILL_BLOCKED"
        ),
        "scope": {
            "source_obstacle": "W",
            "frozen_owner": "W[1,0]",
            "frozen_outgoing_chart": "W",
            "original_parent_dimension": 3,
            "integer_credit_unit": "one completely replaced depth8 parent",
            "child_or_volume_count_used_as_integer_credit": False,
            "guard_rejection_used_as_exterior_credit": False,
            "Round170_candidate_digest_used_as_truth": False,
            "not_D02_closure": True,
        },
        "upstream_verified_chain": upstream,
        "independent_reconstruction_target": {
            **replay["workload"],
            "owner_active_depth8_parent_count": 2616,
            "depth14_frontier_cell_count": 56780,
            "closed_depth14_cell_count_by_disposition": {
                key: len(value)
                for key, value in sorted(category_keys.items())
            },
            "residual_depth14_cell_count": len(residual_keys),
            "fully_replaced_origin_count": len(fully),
            "fully_replaced_origin_count_by_disposition": {
                key: len(value)
                for key, value in sorted(by_kind.items())
            },
        },
        "new_whole_parent_exclusion_credit": {
            "count": 182,
            "exact_origin_keys": credited,
            "exact_origin_keys_sha256": digest(credited),
            "origin_summaries": summaries,
            "origin_summaries_sha256": digest(summaries),
            "every_summary_row_self_digest_valid": all(
                row["row_sha256"]
                == digest({
                    key: value for key, value in row.items()
                    if key != "row_sha256"
                })
                for row in summaries
            ),
            "prior_strict_terminal_only_origin_count":
                len(prior_only_origin_keys),
            "prior_strict_terminal_only_origin_keys_sha256":
                digest(prior_only_origin_keys),
            "analytic_closure_origin_count": len(analytic_origin_keys),
            "analytic_closure_origin_keys": analytic_origin_keys,
            "analytic_closure_origin_keys_sha256":
                digest(analytic_origin_keys),
            "analytic_origin_count_by_method": {
                key: len(values)
                for key, values in sorted(
                    analytic_origin_keys_by_method.items()
                )
            },
            "analytic_origin_keys_by_method": {
                key: values
                for key, values in sorted(
                    analytic_origin_keys_by_method.items()
                )
            },
            "analytic_frontier_closure_count_by_method":
                map_counter(analytic_frontier_closure_counts),
        },
        "physical_source_chart_audit": {
            "count_by_classification": map_counter(guard_counts),
            "guard_only_origin_count": 0,
            "crossing_origin_count": 2,
            "exact_crossing_origin_keys": crossing,
            "exact_crossing_origin_keys_sha256": digest(crossing),
            "source_boundary_dimension": 2,
            "source_boundary_analytic_graph_intersection_dimension_at_most":
                1,
            "source_boundary_multiple_graph_intersection_dimension_at_most":
                0,
            "E_owns_source_diagonal_half_open_seam": True,
            "rational_guard_band_exterior_credit": 0,
        },
        "partition_semantics": {
            "dyadic_closed_overlap_evaluation": True,
            "dyadic_disjoint_ledger_owner":
                "lower child owns each split equality face",
            "multiple_split_face_owner":
                "recursive lexicographic lower-child ownership",
            "strict_closed_box_exclusion_inherits_to_all_owned_faces": True,
            "Delta_partition": [
                {"predicate": "Delta<0", "dimension": 3},
                {"predicate": "Delta=0", "dimension": 2},
                {"predicate": "Delta>0", "dimension": 3},
            ],
            "compact_q_partition": [
                {"predicate": "r>0", "dimension": 3},
                {"predicate": "r=0", "dimension": 2},
            ],
            "graph_edge_dimension": 1,
            "graph_corner_dimension": 0,
            "all_dimensions_must_be_excluded_for_parent_credit": True,
        },
        "disjoint_composition": {
            "Round172_tangency_credit_key_count": len(tangency_keys),
            "Round172_tangency_credit_keys_sha256": digest(tangency_keys),
            "Round175_new_tangency_credit_key_count":
                len(round175_new_tangency_keys),
            "Round175_new_tangency_credit_keys_sha256":
                digest(round175_new_tangency_keys),
            "Round175_cumulative_tangency_credit_key_count":
                len(cumulative_tangency_keys),
            "Round175_cumulative_tangency_credit_keys_sha256":
                digest(cumulative_tangency_keys),
            "Round176_multi_credit_key_count": len(credited),
            "Round176_multi_credit_keys_sha256": digest(credited),
            "exact_key_intersection": [],
            "exact_key_intersection_sha256": digest([]),
            "classification_namespace_reason":
                "Round172/Round175 keys are Gate3 tangency_graph parents; "
                "Round176 keys are owner-active multi_candidate parents",
            "sets_proved_disjoint": True,
        },
        "ledger_composition": {
            "base_round": 175,
            "base_whole_record_excluded": 73178,
            "base_conservative_live": 3654,
            "Round176_new_whole_parent_excluded": 182,
            "combined_whole_record_excluded": 73360,
            "combined_conservative_live": 3472,
            "refined_source_W_record_count": 76832,
            "conservation_identity": "73360+3472=76832",
            "analytic_internal_strata_added_to_integer_record_count": False,
            "guard_outside_added_to_integer_record_count": False,
        },
        "layer_exact_key_digests": {
            "owner_active_depth8_origins_sha256": digest(all_origins),
            "all_depth14_frontier_keys_sha256": digest(all_frontier),
            "closed_EXCLUDED_depth14_keys_sha256":
                digest(category_keys["EXCLUDED"]),
            "closed_LIVE_depth14_keys_sha256":
                digest(category_keys["LIVE"]),
            "closed_MIXED_depth14_keys_sha256":
                digest(category_keys["MIXED"]),
            "residual_depth14_keys_sha256": digest(residual_keys),
            "whole_excluded_origin_keys_sha256": digest(credited),
            "whole_live_origin_keys_sha256":
                digest(by_kind["WHOLE_ORIGIN_PARENT_LIVE"]),
            "whole_mixed_origin_keys_sha256":
                digest(by_kind["RESOLVED_MIXED_OR_ANALYTIC_PARTITION"]),
        },
        "strict_nonpromotion": {
            "D02": "BLOCKED",
            "D03_negative_oracle": "UNAUTHORIZED",
            "global_Gate5_fields": "10/18",
            "global_complete_18_field_blocks": 0,
            "remaining_multi_candidate_original_parents": 2616 - 182,
            "remaining_live_after_composition": 3472,
            "CM2": "NO-GO_FOR_CLAIM",
        },
        "next_core_gate": (
            "close the remaining multi-Delta, full/clipped Delta, "
            "tangency/seam double-graph, and compact-q arrangements"
        ),
        "provenance": {
            "producer": Path(__file__).name,
            "producer_sha256":
                hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            "python_flint_version": "0.9.0",
            "arb_precision_bits": 192,
            "producer_imports_pinned_Round166_and_Round170_geometry": True,
            "verifier_must_not_import_or_execute_Round165_166_170": True,
            "older_round_files_modified": False,
        },
    }
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=OUTPUT)
    args = parser.parse_args()
    ctx.prec = 192
    result = build_result()
    document = {
        "schema": SCHEMA,
        "result": result,
        "result_sha256": digest(result),
    }
    args.output.write_text(
        json.dumps(
            document,
            sort_keys=True,
            indent=2,
            ensure_ascii=False,
            allow_nan=False,
        )
        + "\n"
    )
    print(document["result_sha256"])


if __name__ == "__main__":
    main()
