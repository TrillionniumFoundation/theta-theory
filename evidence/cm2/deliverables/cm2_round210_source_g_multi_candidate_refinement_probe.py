#!/usr/bin/env python3
"""Read-only bounded refinement probe for all source-G multi-candidate leaves.

This is a feasibility census, not a formal disposition certificate.  It
inherits only parent-uniformly active targets and records unique-first boxes,
typed tangency boxes, and unresolved multi-candidate boxes separately.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from dataclasses import dataclass
from fractions import Fraction as Q
import hashlib
import json
from pathlib import Path
from typing import Any

from flint import ctx

import cm2_gate3_eight_cell_symmetry_atlas_cert as atlas
import cm2_round166_multi_candidate_refinement_prototype as r166


HERE = Path(__file__).resolve().parent
PINS = {
    "cm2_gate3_candidate_first_hit_cert.py":
        "6d224d74cda186a40ef9956d1dd6556d5a7b9f506d47c942427ceb66fd705bd2",
    "cm2_gate3_ge_interval_atlas_cert.py":
        "ab120f85a263f3cb0697d8a40bc9ed2bf12b361aa7c54940c214b6fd85b17e2b",
    "cm2_gate3_eight_cell_symmetry_atlas_cert.py":
        "d867f5cb03691289033d1a0d0e277a03e8395d70aae7e0689446d7aa63eac3da",
    "cm2_round166_multi_candidate_refinement_prototype.py":
        "6479a78249a717169dea55ecabae98c05f240ea323fa0370037d43339158ae7c",
    "cm2-gate3-eight-cell-symmetry-atlas-manifest-2026-07-15.json":
        "f8fda665edbb7d8b39ce495188f90ecb2b5ec4384c1eb958949627df167c4987",
}
CHARTS = ("G:E", "G:N", "G:W", "G:S")
EXPECTED = {
    "G:E": {
        "leaf": 16_580, "unique_first": 5_276,
        "tangency_graph": 38, "multi_candidate": 11_266,
        "rows": "6d0efa44d3f0eaf31939d25fc3fb1bca65314317a7a973a6c73083ec2799c491",
    },
    "G:N": {
        "leaf": 16_630, "unique_first": 5_340,
        "tangency_graph": 42, "multi_candidate": 11_248,
        "rows": "887de52013a80f36db593c3acc263afa2872ece9635fa875c21dd5c4c5201a8b",
    },
    "G:W": {
        "leaf": 16_580, "unique_first": 5_276,
        "tangency_graph": 38, "multi_candidate": 11_266,
        "rows": "49ca4f4d7ed83bb2ad13cbe1f166c04c2964f04da6d0ce9283be51de81639fda",
    },
    "G:S": {
        "leaf": 16_630, "unique_first": 5_340,
        "tangency_graph": 42, "multi_candidate": 11_248,
        "rows": "6bd373beef4d406afe33c0bff878c4021472bfa6eb399cddd5f2606138e08e4a",
    },
}


def require(condition: bool, label: str) -> None:
    if not condition:
        raise RuntimeError(label)


def canonical(value: Any) -> str:
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"),
        ensure_ascii=False, allow_nan=False,
    )


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value).encode()).hexdigest()


def check_pins() -> None:
    for name, expected in PINS.items():
        require(
            hashlib.sha256((HERE / name).read_bytes()).hexdigest() == expected,
            f"pin:{name}",
        )


def baseline() -> dict[str, list[Any]]:
    ctx.prec = 192
    direct_e = atlas.build_atlas("G:E")
    direct_n = atlas.build_atlas("G:N")
    charts = {
        "G:E": direct_e,
        "G:N": direct_n,
        "G:W": [
            atlas.reflect_leaf("G:E", "vertical", leaf)
            for leaf in direct_e
        ],
        "G:S": [
            atlas.reflect_leaf("G:N", "horizontal", leaf)
            for leaf in direct_n
        ],
    }
    for chart_id in CHARTS:
        leaves = charts[chart_id]
        expected = EXPECTED[chart_id]
        counts = Counter(leaf.classification for leaf in leaves)
        rows = [
            atlas.leaf_row(chart_id, leaf)
            for leaf in sorted(leaves, key=lambda item: item.box.path)
        ]
        require(len(leaves) == expected["leaf"], f"leaf:{chart_id}")
        for label in ("unique_first", "tangency_graph", "multi_candidate"):
            require(counts[label] == expected[label], f"{label}:{chart_id}")
        require(
            atlas.canonical_digest(rows) == expected["rows"],
            f"rows:{chart_id}",
        )
    return charts


@dataclass(frozen=True)
class Node:
    chart_id: str
    box: Any
    active_targets: tuple[str, ...]
    origin_path: str


def residual_label(leaf: Any, records: list[Any]) -> str:
    if leaf.classification == "tangency_graph":
        return "TYPED_TANGENCY_GRAPH__OFF_GRAPH_BULK_UNRESOLVED"
    require(leaf.classification == "multi_candidate", "residual class")
    classes = Counter(row.classification for row in records)
    if len(leaf.tangency_targets) > 1:
        return "MULTIPLE_TANGENCY_TARGETS"
    if leaf.box.p0 == -1 or leaf.box.p1 == 1:
        return "SOURCE_GRAZING_FACE_TOUCH"
    if classes["unresolved_root_sign"]:
        return "ROOT_SIGN_OR_FIRST_ORDER_UNRESOLVED"
    if classes["unresolved_discriminant"]:
        return "DISCRIMINANT_OR_FIRST_ORDER_UNRESOLVED"
    return "STRICT_MULTI_FIRST_ORDER_UNRESOLVED"


def profile(charts: dict[str, list[Any]], extra_depth: int, precision: int) -> dict[str, Any]:
    ctx.prec = precision
    pending = [
        Node(chart_id, leaf.box, leaf.active_targets, leaf.box.path)
        for chart_id in CHARTS
        for leaf in charts[chart_id]
        if leaf.classification == "multi_candidate"
    ]
    require(len(pending) == 45_028, "multi input")
    require(
        all(node.box.depth == atlas.MAX_DEPTH for node in pending),
        "baseline depth",
    )
    baseline_active = Counter(len(node.active_targets) for node in pending)
    terminal_counts: Counter[str] = Counter()
    terminal_by_chart: dict[str, Counter[str]] = defaultdict(Counter)
    terminal_targets: Counter[str] = Counter()
    terminal_parent_equivalent: Counter[str] = Counter()
    snapshots: list[dict[str, Any]] = []
    evaluated_boxes = 0
    evaluated_records = 0
    final_residual: Counter[str] = Counter()
    final_active: Counter[int] = Counter()
    final_tangency_targets: Counter[str] = Counter()

    for relative_depth in range(extra_depth + 1):
        next_pending: list[Node] = []
        level_residual: Counter[str] = Counter()
        level_active: Counter[int] = Counter()
        for node in pending:
            leaf, records = r166.classify_active(
                node.chart_id, node.box, node.active_targets,
            )
            evaluated_boxes += 1
            evaluated_records += len(node.active_targets)
            if leaf.classification in {"unique_first", "no_future_root"}:
                label = leaf.classification.upper()
                terminal_counts[label] += 1
                terminal_by_chart[node.chart_id][label] += 1
                terminal_parent_equivalent[label] += Q(
                    1, 2 ** relative_depth,
                )
                if leaf.owner_target is not None:
                    terminal_targets[leaf.owner_target] += 1
                continue

            label = residual_label(leaf, records)
            inherited = (
                node.active_targets
                if leaf.classification == "tangency_graph"
                else leaf.active_targets
            )
            require(inherited, "nonempty inherited active set")
            level_residual[label] += 1
            level_active[len(inherited)] += 1
            if relative_depth == extra_depth:
                final_residual[label] += 1
                final_active[len(inherited)] += 1
                for target in leaf.tangency_targets:
                    final_tangency_targets[target] += 1
                continue
            axis = r166.longest_axis(node.box)
            for child in r166.split_axis(node.box, axis):
                next_pending.append(Node(
                    node.chart_id, child, inherited, node.origin_path,
                ))
        snapshots.append({
            "extra_depth": relative_depth,
            "absolute_depth": atlas.MAX_DEPTH + relative_depth,
            "terminal_subbox_count_cumulative":
                dict(sorted(terminal_counts.items())),
            "terminal_parent_equivalent_cumulative": {
                key: str(value)
                for key, value in sorted(terminal_parent_equivalent.items())
            },
            "residual_subbox_count": sum(level_residual.values()),
            "residual_parent_equivalent":
                str(Q(sum(level_residual.values()), 2 ** relative_depth)),
            "residual_kind_count": dict(sorted(level_residual.items())),
            "residual_active_target_size": {
                str(key): value for key, value in sorted(level_active.items())
            },
        })
        pending = next_pending

    terminal_equivalent = sum(terminal_parent_equivalent.values(), Q(0))
    residual_equivalent = Q(
        sum(final_residual.values()), 2 ** extra_depth,
    )
    require(
        terminal_equivalent + residual_equivalent == 45_028,
        "parent-equivalent conservation",
    )
    return {
        "scope": {
            "baseline_multi_candidate_leaf_count": 45_028,
            "baseline_tangency_graph_leaf_count_kept_separate": 160,
            "baseline_absolute_depth": atlas.MAX_DEPTH,
            "refinement_precision_bits": precision,
            "maximum_extra_depth": extra_depth,
            "split_policy":
                "largest exact rational t,p,s width with stable axis tie break",
            "probe_only_no_integer_or_global_credit": True,
        },
        "baseline_active_target_size": {
            str(key): value for key, value in sorted(baseline_active.items())
        },
        "refinement": {
            "snapshots": snapshots,
            "evaluated_subbox_count": evaluated_boxes,
            "evaluated_target_record_count": evaluated_records,
            "terminal_subbox_count": dict(sorted(terminal_counts.items())),
            "terminal_subbox_count_by_chart": {
                chart: dict(sorted(counts.items()))
                for chart, counts in sorted(terminal_by_chart.items())
            },
            "terminal_unique_first_target_count":
                dict(terminal_targets.most_common()),
            "terminal_parent_equivalent": {
                key: str(value)
                for key, value in sorted(terminal_parent_equivalent.items())
            },
            "final_residual_subbox_count":
                sum(final_residual.values()),
            "final_residual_kind_count":
                dict(sorted(final_residual.items())),
            "final_residual_active_target_size": {
                str(key): value for key, value in sorted(final_active.items())
            },
            "final_tangency_target_count":
                dict(final_tangency_targets.most_common()),
            "final_residual_parent_equivalent": str(residual_equivalent),
            "terminal_plus_residual_parent_equivalent": "45028",
            "exact_parent_equivalent_conservation": True,
        },
        "promotion_boundary": {
            "typed_tangency_boxes_are_not_whole_box_dispositions": True,
            "unique_first_subboxes_are_local_dynamic_inputs_only": True,
            "whole_original_parent_credit": 0,
            "global_exact_key_disposition_credit": 0,
            "D02": "BLOCKED",
            "Gate5": "10/18",
            "CM2": "NO-GO_FOR_CLAIM",
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--extra-depth", type=int, default=3)
    parser.add_argument("--precision", type=int, default=256)
    args = parser.parse_args()
    require(0 <= args.extra_depth <= 8, "extra depth")
    require(192 <= args.precision <= 768, "precision")
    check_pins()
    result = profile(baseline(), args.extra_depth, args.precision)
    document = {
        "schema": "cm2.round210.source-g-multi-candidate-refinement-probe.v1",
        "result": result,
        "result_sha256": digest(result),
    }
    print(json.dumps(
        document, sort_keys=True, indent=2,
        ensure_ascii=False, allow_nan=False,
    ))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
