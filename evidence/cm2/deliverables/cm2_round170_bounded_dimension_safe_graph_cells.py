#!/usr/bin/env python3
"""Round170: bounded, dimension-safe graph-cell closure of Round166 frontier.

This producer independently replays the six-level Round166 owner-active tree,
then certifies only four bounded blocks:

* outgoing-chart seam cells, with two 3D open sides and one 2D graph;
* already typed first-tangency collars whose three strata are all excluded;
* single-discriminant boxes whose two p faces have the same strict sign;
* a nonpromotional compact-q profile of source-grazing endpoint collars.

It never turns graph typing into whole-record credit.  Counts of depth-14
records, rational depth-8-parent-equivalent volume, and fully replaced
Round168 parent records are kept in separate ledgers.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter, defaultdict
from dataclasses import dataclass
from fractions import Fraction as Q
from pathlib import Path
from typing import Any

from flint import arb, ctx

import cm2_round165_adaptive_typed_seam_census as r165
import cm2_round166_multi_candidate_refinement_prototype as r166


HERE = Path(__file__).resolve().parent
OUTPUT = HERE / "cm2_round170_bounded_dimension_safe_graph_cells_certificate.json"
SCHEMA = "cm2.round170.bounded-dimension-safe-graph-cells.v1"

PINS = {
    "cm2_round164_tangency_strata_pruning_certificate.json":
        "2f1fcb72224f39c8d4a9d9f666a8579f71d77542e31552aa7c9dbc4b7338f092",
    "cm2_round164_tangency_strata_pruning_verification.json":
        "850bd24ae60979aaaea3f6819dcab665a1f7228d0c104014bfe8cce9e91299b0",
    "cm2_round165_adaptive_typed_seam_census.py":
        "95bdbe3fc8d1d26512d8469a0e9382a3e977d5606375ed2729877c9f1ac8e012",
    "cm2_round165_adaptive_typed_seam_census_certificate.json":
        "2cbd69e8cbde66966d78764c0d5b34518c2ec55891d0238a62f40073ae4876a8",
    "cm2_round165_adaptive_typed_seam_census_verifier.py":
        "1967147d98075792dc6821ff72e46b2f33251ba98950d1660d10280bf0ef298e",
    "cm2_round165_adaptive_typed_seam_census_verification.json":
        "af684b956c40c97e26fdd5f9ddacea85b9c693b0b9a935d387ed1a5142ffa3b5",
    "cm2_round166_multi_candidate_refinement_prototype.py":
        "6479a78249a717169dea55ecabae98c05f240ea323fa0370037d43339158ae7c",
    "cm2_round166_multi_candidate_refinement_prototype_stats.json":
        "ffa028ff9e46219a48b3950a49a7c8f8d111fb54e7c3322aa4387366a2870999",
    "cm2_round166_multi_candidate_refinement_prototype_verifier.py":
        "b069bc640d6bcf7d6eb16570d5844ce88504e00abc587cee958b59a775c68cdf",
    "cm2_round166_multi_candidate_refinement_prototype_verification.json":
        "66f61b657eb72a0db90291d390d1021859c65ab059fdeaedabee95170102d1af",
    "cm2_round168_dimension_safe_source_W_stage_one_ledger_certificate.json":
        "adbdcc3ffbd791126dd759a5699bf65902ebb8529b173db52e4b45e5f299494e",
    "cm2_round168_dimension_safe_source_W_stage_one_ledger_verification.json":
        "994037b25d321e731e4cf4b61c92610fa99fadfccfa2d15ce2a38ccbe20a5cc9",
}

RESULT_IDS = {
    "round164":
        "0f6d7f47ac20734ed294dd04cd7720ccbb9c0a1d4236980f814dd2ea2d5e79d9",
    "round164_verification":
        "bb2e51bdbbd457a5782038efc527000cbf89b73c8645fd6facd126fa453af8c4",
    "round165":
        "93e2899d0a9a79a82e1b193158f3733e891e2c5b4c9ce83f970aff40bf75c270",
    "round165_verification":
        "86356b4b778fc8e2f74ab1edec30c96346027a9c17ade38c6f5aef269d6e5786",
    "round166":
        "6972926f909815e041842fe5582f89898d1589ab69b54a801f5e28fdfa19e548",
    "round166_verification":
        "bf88161e1310db2dc3531e300b0a20af9b7f1c008c0909824b8bfcf64b14097f",
    "round168":
        "1544a7b865df882bab92dbec333e723fea28dd382567945e09ad609e7a811201",
    "round168_verification":
        "07f9bcc6fd42f5439322e1090b281a3f0780c3a706bb19ceeb9f51b666280031",
}

EXCLUSION_H_CLASSES = {
    "STRICT_OUTGOING_CHART_MISMATCH_RECTANGLE",
    "MONOTONE_H_OUTGOING_CHART_MISMATCH_RECTANGLE",
}
LIVE_H_CLASSES = {
    "STRICT_PREFIX_STAGE_ONE_MATCH_RECTANGLE",
    "MONOTONE_H_PREFIX_STAGE_ONE_MATCH_RECTANGLE",
}


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
    documents = {
        "round164": strict_load(
            HERE / "cm2_round164_tangency_strata_pruning_certificate.json"
        ),
        "round164_verification": strict_load(
            HERE / "cm2_round164_tangency_strata_pruning_verification.json"
        ),
        "round165": strict_load(
            HERE / "cm2_round165_adaptive_typed_seam_census_certificate.json"
        ),
        "round165_verification": strict_load(
            HERE / "cm2_round165_adaptive_typed_seam_census_verification.json"
        ),
        "round166": strict_load(
            HERE / "cm2_round166_multi_candidate_refinement_prototype_stats.json"
        ),
        "round166_verification": strict_load(
            HERE / "cm2_round166_multi_candidate_refinement_prototype_verification.json"
        ),
        "round168": strict_load(
            HERE
            / "cm2_round168_dimension_safe_source_W_stage_one_ledger_certificate.json"
        ),
        "round168_verification": strict_load(
            HERE
            / "cm2_round168_dimension_safe_source_W_stage_one_ledger_verification.json"
        ),
    }
    for name, expected in RESULT_IDS.items():
        require(
            documents[name]["result_sha256"] == expected,
            f"result identity:{name}",
        )
    require(
        documents["round164"]["schema"]
        == "cm2.round164.dimension-safe-tangency-graph-typing.v2"
        and documents["round164"]["result"][
            "ambient_frozen_prefix_census"
        ]["remaining_ambient_unresolved_leaf_count"] == 39348
        and documents["round164"]["result"][
            "ambient_frozen_prefix_census"
        ]["new_full_dimensional_ambient_leaf_exclusion_count"] == 0
        and documents["round164_verification"]["result"]["status"] == "PASS",
        "Round164-v2 dimension-safe chain",
    )
    require(
        documents["round165_verification"]["result"]["status"] == "PASS",
        "Round165 verification",
    )
    require(
        documents["round166"]["result"]["refinement"][
            "final_unresolved_failure_types"
        ] == {
            "OUTGOING_CHART_SEAM_OVERWRAP": 7510,
            "SOURCE_GRAZING_ENDPOINT_COLLAR": 1632,
            "TYPED_FROZEN_OWNER_TANGENCY_GRAPH_COLLAR": 80,
            "TYPED_OWNER_MISMATCH_TANGENCY_GRAPH_COLLAR": 1140,
            "UNTYPED_DISCRIMINANT_COLLAR": 46418,
        }
        and documents["round166_verification"]["result"]["status"]
        == "PASS_LIMITED_BASELINE_WITNESS_AND_CONSERVATION_VERIFICATION"
        and not documents["round166_verification"]["result"]["scope"][
            "six_level_refinement_tree_independently_replayed"
        ],
        "Round166 limited chain",
    )
    require(
        documents["round168_verification"]["result"]["status"] == "PASS"
        and documents["round168"]["result"]["conservation"][
            "whole_record_excluded"
        ] == 73162
        and documents["round168"]["result"]["conservation"][
            "conservative_live"
        ] == 3670
        and documents["round168"]["result"]["conservative_live_ledger"][
            "owner_active_multi"
        ] == 2616,
        "Round168 ledger context",
    )
    return {
        "file_sha256": PINS,
        "result_sha256": RESULT_IDS,
        "round166_verifier_scope_was_limited": True,
        "round170_replays_the_six_level_tree_it_claims": True,
    }


@dataclass(frozen=True)
class FrontierRow:
    chart_id: str
    box: r166.ge.AtlasBox
    active_targets: tuple[str, ...]
    origin_key: str
    failure: str

    @property
    def leaf_key(self) -> str:
        return f"{self.chart_id}:{self.box.path}"


def coarse_kind(disposition: str) -> str:
    if disposition.startswith("EXCLUDED"):
        return "EXCLUDED"
    if disposition.startswith("LIVE"):
        return "LIVE"
    raise RuntimeError(f"unknown disposition:{disposition}")


def reconstruct_frontier() -> tuple[
    list[FrontierRow],
    Counter[str],
    dict[str, set[str]],
    set[str],
    dict[str, Q],
    dict[str, int],
]:
    r166.install_fast_readonly_replay()
    charts = r166.baseline_fast()
    pending: list[r166.Node] = []
    all_origins: set[str] = set()
    for chart_id, leaves in charts.items():
        for leaf in leaves:
            if (
                leaf.classification == "multi_candidate"
                and r166.FROZEN_OWNER in leaf.active_targets
            ):
                origin_key = f"{chart_id}:{leaf.box.path}"
                all_origins.add(origin_key)
                pending.append(
                    r166.Node(
                        chart_id,
                        leaf.box,
                        leaf.active_targets,
                        leaf.box.path,
                    )
                )
    require(len(pending) == 2616, "owner-active input")
    frontier: list[FrontierRow] = []
    terminal_counts: Counter[str] = Counter()
    terminal_volume: dict[str, Q] = defaultdict(Q)
    origin_kinds: dict[str, set[str]] = defaultdict(set)
    evaluated_boxes = 0
    evaluated_records = 0
    for relative_depth in range(7):
        next_pending: list[r166.Node] = []
        for node in pending:
            leaf, records = r166.classify_active(
                node.chart_id, node.box, node.active_targets
            )
            evaluated_boxes += 1
            evaluated_records += len(node.active_targets)
            disposition, seam_margins = r166.terminal_disposition(
                node.chart_id, leaf
            )
            origin_key = f"{node.chart_id}:{node.origin_path}"
            if disposition is not None:
                terminal_counts[disposition] += 1
                terminal_volume[disposition] += Q(
                    1, 2 ** relative_depth
                )
                origin_kinds[origin_key].add(coarse_kind(disposition))
                continue
            failure = r166.unresolved_failure(
                node.chart_id, leaf, records, seam_margins
            )
            if leaf.classification == "unique_first":
                inherited = (r166.FROZEN_OWNER,)
            elif leaf.classification == "tangency_graph":
                inherited = node.active_targets
            else:
                inherited = leaf.active_targets
            if relative_depth == 6:
                frontier.append(
                    FrontierRow(
                        node.chart_id,
                        node.box,
                        inherited,
                        origin_key,
                        failure,
                    )
                )
                continue
            axis = r166.longest_axis(node.box)
            for child in r166.split_axis(node.box, axis):
                next_pending.append(
                    r166.Node(
                        node.chart_id,
                        child,
                        inherited,
                        node.origin_path,
                    )
                )
        pending = next_pending
    require(len(frontier) == 56780, "frontier count")
    failure_counts = Counter(row.failure for row in frontier)
    require(
        failure_counts
        == {
            "OUTGOING_CHART_SEAM_OVERWRAP": 7510,
            "SOURCE_GRAZING_ENDPOINT_COLLAR": 1632,
            "TYPED_FROZEN_OWNER_TANGENCY_GRAPH_COLLAR": 80,
            "TYPED_OWNER_MISMATCH_TANGENCY_GRAPH_COLLAR": 1140,
            "UNTYPED_DISCRIMINANT_COLLAR": 46418,
        },
        "frontier type census",
    )
    require(
        terminal_counts
        == {
            "EXCLUDED_OUTGOING_CHART_MISMATCH": 6520,
            "EXCLUDED_UNIQUE_FIRST_OWNER_MISMATCH": 13472,
            "LIVE_FROZEN_STAGE_ONE_OWNER_CHART_MATCH": 8528,
        },
        "prior terminal child census",
    )
    require(
        terminal_volume
        == {
            "EXCLUDED_OUTGOING_CHART_MISMATCH": Q(11437, 32),
            "EXCLUDED_UNIQUE_FIRST_OWNER_MISMATCH": Q(12649, 16),
            "LIVE_FROZEN_STAGE_ONE_OWNER_CHART_MATCH": Q(18587, 32),
        },
        "prior terminal volume",
    )
    require(
        evaluated_boxes == 167984
        and evaluated_records == 415570,
        "Round166 full depth14 replay workload",
    )
    return (
        frontier,
        terminal_counts,
        origin_kinds,
        all_origins,
        dict(terminal_volume),
        {
            "evaluated_box_count": evaluated_boxes,
            "evaluated_target_record_count": evaluated_records,
        },
    )


def sign(value: arb) -> int:
    if bool(value > 0):
        return 1
    if bool(value < 0):
        return -1
    return 0


def h_partition(
    chart_id: str,
    box: r166.ge.AtlasBox,
    origin_key: str,
    max_extra_depth: int = 4,
) -> tuple[str | None, Counter[str], Counter[int]]:
    pending = [(box, 0)]
    terminal_classes: Counter[str] = Counter()
    terminal_depths: Counter[int] = Counter()
    while pending:
        current, depth = pending.pop()
        row, status = r165.terminal_row(
            origin_key, chart_id, current, depth
        )
        if status == "terminal":
            require(row is not None, "H terminal row")
            terminal_classes[row["classification"]] += 1
            terminal_depths[depth] += 1
        elif depth < max_extra_depth:
            pending.extend(
                (child, depth + 1)
                for child in r165.split_box(current)
            )
        else:
            return None, terminal_classes, terminal_depths
    classes = set(terminal_classes)
    if classes <= EXCLUSION_H_CLASSES:
        return "EXCLUDED", terminal_classes, terminal_depths
    if classes <= LIVE_H_CLASSES:
        return "LIVE", terminal_classes, terminal_depths
    return "MIXED", terminal_classes, terminal_depths


def disposition_without_target(
    row: FrontierRow,
    records: list[r166.ge.RootRecord],
    target_id: str,
) -> tuple[str | None, r166.ge.Leaf]:
    remaining = [
        record for record in records
        if record.target_id != target_id
    ]
    leaf = r166.classify_from_records(
        row.chart_id, row.box, remaining
    )
    disposition, _margins = r166.terminal_disposition(
        row.chart_id, leaf
    )
    return disposition, leaf


def target_positive_first(
    candidate: r166.ge.RootRecord,
    records: list[r166.ge.RootRecord],
) -> bool:
    radius = r166.base.arbq(
        r166.base.RADIUS[
            r166._target_cache[candidate.target_id].obstacle
        ]
    )
    if not (
        bool(candidate.ell - radius > 0)
        and bool(candidate.ell < r166.base.arbq(r166.base.TAU_MAX))
    ):
        return False
    for other in records:
        if other.target_id == candidate.target_id:
            continue
        if other.classification in {
            "no_real_intersection",
            "intersection_behind",
        }:
            continue
        lower = r166.ge.earliest_possible_root_lower(other)
        if lower is None or not bool(candidate.ell < lower):
            return False
    return True


def positive_outgoing_chart(
    row: FrontierRow,
    candidate: r166.ge.RootRecord,
) -> str | None:
    qx, qy, ux, uy, _s, _cp = r166.atlas.geometry(
        row.chart_id, row.box
    )
    upper = candidate.discriminant.upper()
    if not bool(upper > 0):
        return None
    h = r166.ge.arb_hull(arb(0), upper.sqrt().upper())
    radius = r166.base.arbq(
        r166.base.RADIUS[
            r166._target_cache[candidate.target_id].obstacle
        ]
    )
    transverse = candidate.transverse
    normal_x = (transverse * uy - h * ux) / radius
    normal_y = (-transverse * ux - h * uy) / radius
    margins = {
        "E": (normal_x - normal_y, normal_x + normal_y),
        "W": (-normal_x - normal_y, -normal_x + normal_y),
        "N": (normal_y - normal_x, normal_y + normal_x),
        "S": (-normal_y - normal_x, -normal_y + normal_x),
    }
    cells = [
        cell for cell, values in margins.items()
        if bool(values[0] > 0) and bool(values[1] > 0)
    ]
    return cells[0] if len(cells) == 1 else None


def unique_unresolved_discriminant(
    row: FrontierRow,
) -> tuple[list[r166.ge.RootRecord], list[r166.ge.RootRecord]]:
    records = r166.records_for(
        row.chart_id, row.box, row.active_targets
    )
    unresolved = [
        record for record in records
        if record.classification == "unresolved_discriminant"
    ]
    return records, unresolved


def graph_faces(
    row: FrontierRow,
    candidate: r166.ge.RootRecord,
) -> tuple[int, arb, arb, bool]:
    *_unused, cp = r166.atlas.geometry(row.chart_id, row.box)
    derivative = (
        2 * candidate.transverse * candidate.ell / cp
        if bool(cp > 0)
        else arb(0)
    )
    derivative_sign = sign(derivative)
    lower = r166.root_at_fixed_p(
        row.chart_id,
        row.box,
        candidate.target_id,
        row.box.p0,
    ).discriminant
    upper = r166.root_at_fixed_p(
        row.chart_id,
        row.box,
        candidate.target_id,
        row.box.p1,
    ).discriminant
    full_graph = (
        derivative_sign > 0
        and bool(lower < 0)
        and bool(upper > 0)
    ) or (
        derivative_sign < 0
        and bool(lower > 0)
        and bool(upper < 0)
    )
    return derivative_sign, lower, upper, full_graph


def close_typed_tangency(
    row: FrontierRow,
) -> tuple[bool, str]:
    records, unresolved = unique_unresolved_discriminant(row)
    if len(unresolved) != 1:
        return False, "NOT_SINGLE_DISCRIMINANT"
    candidate = unresolved[0]
    derivative_sign, _lower, _upper, full_graph = graph_faces(
        row, candidate
    )
    if derivative_sign == 0 or not full_graph:
        return False, "NOT_FULL_MONOTONE_P_GRAPH"
    if not target_positive_first(candidate, records):
        return False, "GRAPH_TARGET_NOT_STRICT_FIRST"
    negative, _negative_leaf = disposition_without_target(
        row, records, candidate.target_id
    )
    if negative is None or not negative.startswith("EXCLUDED"):
        return False, "NEGATIVE_OPEN_SIDE_NOT_WHOLE_EXCLUDED"
    if candidate.target_id != r166.FROZEN_OWNER:
        positive = "EXCLUDED_UNIQUE_FIRST_OWNER_MISMATCH"
        graph = "EXCLUDED_UNIQUE_FIRST_OWNER_MISMATCH"
    else:
        chart = positive_outgoing_chart(row, candidate)
        if chart is None or chart == r166.FROZEN_CHART:
            return False, "POSITIVE_OR_GRAPH_OUTGOING_NOT_MISMATCH"
        positive = "EXCLUDED_OUTGOING_CHART_MISMATCH"
        # The positive-side enclosure includes h=0, so the same strict
        # outgoing chart holds on the two-dimensional tangency graph.
        graph = "EXCLUDED_OUTGOING_CHART_MISMATCH"
    require(
        positive.startswith("EXCLUDED")
        and graph.startswith("EXCLUDED"),
        "typed collar three-stratum exclusion",
    )
    return True, (
        f"NEGATIVE={negative}|GRAPH={graph}|POSITIVE={positive}"
    )


def monotone_face_record(
    candidate: r166.ge.RootRecord,
    lower: arb,
    upper: arb,
    derivative_sign: int,
) -> r166.ge.RootRecord:
    require(derivative_sign != 0, "monotone face derivative")
    if derivative_sign > 0:
        delta = r166.ge.arb_hull(lower.lower(), upper.upper())
    else:
        delta = r166.ge.arb_hull(upper.lower(), lower.upper())
    if bool(delta < 0):
        return r166.ge.RootRecord(
            candidate.target_id,
            "no_real_intersection",
            candidate.ell,
            delta,
            None,
            None,
            candidate.transverse,
        )
    require(bool(delta > 0), "same-sign face delta")
    radical = delta.sqrt()
    near = candidate.ell - radical
    far = candidate.ell + radical
    if bool(far < 0):
        classification = "intersection_behind"
    elif bool(near > 0):
        classification = "strict_future_root"
    else:
        classification = "unresolved_root_sign"
    return r166.ge.RootRecord(
        candidate.target_id,
        classification,
        candidate.ell,
        delta,
        near,
        far,
        candidate.transverse,
    )


def close_same_sign_discriminant(
    row: FrontierRow,
    records: list[r166.ge.RootRecord],
    candidate: r166.ge.RootRecord,
    derivative_sign: int,
    lower: arb,
    upper: arb,
) -> tuple[str | None, str]:
    enhanced = monotone_face_record(
        candidate, lower, upper, derivative_sign
    )
    replaced = [
        enhanced if record.target_id == candidate.target_id else record
        for record in records
    ]
    leaf = r166.classify_from_records(
        row.chart_id, row.box, replaced
    )
    if leaf.classification == "no_future_root":
        return "EXCLUDED", "NO_INHERITED_FUTURE_ROOT"
    if leaf.classification != "unique_first":
        return None, f"ENHANCED_{leaf.classification}"
    if leaf.owner_target != r166.FROZEN_OWNER:
        return "EXCLUDED", "UNIQUE_FIRST_OWNER_MISMATCH"
    if candidate.target_id == r166.FROZEN_OWNER:
        chart = positive_outgoing_chart(row, enhanced)
        if chart is None:
            return None, "ENHANCED_FROZEN_OUTGOING_UNRESOLVED"
        return (
            "LIVE" if chart == r166.FROZEN_CHART else "EXCLUDED"
        ), f"ENHANCED_FROZEN_OUTGOING_{chart}"
    chart, _margins = r166.outgoing_chart(row.chart_id, row.box)
    if chart is not None:
        return (
            "LIVE" if chart == r166.FROZEN_CHART else "EXCLUDED"
        ), f"UNCHANGED_FROZEN_OUTGOING_{chart}"
    h_kind, _classes, _depths = h_partition(
        row.chart_id, row.box, row.origin_key
    )
    return h_kind, "FOLLOWUP_H_PARTITION"


@dataclass(frozen=True)
class QBox:
    t0: Q
    t1: Q
    r0: Q
    r1: Q
    s0: Q
    s1: Q
    depth: int


def q_geometry(
    chart_id: str,
    sign_p: int,
    box: QBox,
) -> tuple[arb, arb, arb, arb, arb, arb]:
    t = r166.base.arb_interval(box.t0, box.t1)
    r = r166.base.arb_interval(box.r0, box.r1)
    s = r166.base.arb_interval(box.s0, box.s1)
    radical_t = r166.ge.sqrt_one_minus_square(box.t0, box.t1)
    _source, cell = chart_id.split(":")
    require(cell in {"N", "S"}, "grazing source chart")
    nx, ny = (t, radical_t if cell == "N" else -radical_t)
    k = Q(1023, 262144)
    compact_q = r166.base.arbq(k).sqrt() * r
    p_lower = r166.base.arbq(
        1 - k * box.r1 * box.r1
    ).sqrt()
    p_upper = r166.base.arbq(
        1 - k * box.r0 * box.r0
    ).sqrt()
    p_abs = r166.ge.arb_hull(
        p_lower.lower(), p_upper.upper()
    )
    p = p_abs if sign_p > 0 else -p_abs
    ux = compact_q * nx - p * ny
    uy = compact_q * ny + p * nx
    cx = r166.base.arbq(Q(1, 2)) + s
    cy = r166.base.arbq(Q(1, 2))
    radius = r166.base.arbq(r166.base.RADIUS["W"])
    return (
        cx + radius * nx,
        cy + radius * ny,
        ux,
        uy,
        s,
        compact_q,
    )


def q_classify(
    chart_id: str,
    sign_p: int,
    box: QBox,
    target_ids: tuple[str, ...],
) -> tuple[str, tuple[str, ...]]:
    geometry = q_geometry(chart_id, sign_p, box)
    records = [
        r166.root_record_from_geometry(geometry, target_id)
        for target_id in target_ids
    ]
    strict = [
        record for record in records
        if record.classification == "strict_future_root"
    ]
    unresolved = [
        record for record in records
        if record.classification in {
            "unresolved_discriminant",
            "unresolved_root_sign",
        }
    ]
    if not strict and not unresolved:
        return "EXCLUDED_NO_INHERITED_FUTURE_ROOT", ()
    for candidate in strict:
        if all(
            other.target_id == candidate.target_id
            or other.classification in {
                "no_real_intersection",
                "intersection_behind",
            }
            or (
                (lower := r166.ge.earliest_possible_root_lower(other))
                is not None
                and bool(candidate.near < lower)
            )
            for other in records
        ):
            if candidate.target_id != r166.FROZEN_OWNER:
                return (
                    "EXCLUDED_UNIQUE_FIRST_OWNER_MISMATCH",
                    (candidate.target_id,),
                )
            qx, qy, ux, uy, s, _compact_q = geometry
            target = r166._target_cache[candidate.target_id]
            center_x, center_y = r166.base.target_center(target, s)
            radius = r166.base.arbq(
                r166.base.RADIUS[target.obstacle]
            )
            normal_x = (
                qx + candidate.near * ux - center_x
            ) / radius
            normal_y = (
                qy + candidate.near * uy - center_y
            ) / radius
            margins = {
                "E": (normal_x - normal_y, normal_x + normal_y),
                "W": (-normal_x - normal_y, -normal_x + normal_y),
                "N": (normal_y - normal_x, normal_y + normal_x),
                "S": (-normal_y - normal_x, -normal_y + normal_x),
            }
            cells = [
                cell for cell, values in margins.items()
                if bool(values[0] > 0) and bool(values[1] > 0)
            ]
            if len(cells) == 1:
                return (
                    "LIVE_FROZEN_STAGE_ONE_OWNER_CHART_MATCH"
                    if cells[0] == r166.FROZEN_CHART
                    else "EXCLUDED_OUTGOING_CHART_MISMATCH"
                ), (candidate.target_id,)
            return "UNRESOLVED_OUTGOING_SEAM", (
                candidate.target_id,
            )
    active: set[str] = set()
    for candidate in strict + unresolved:
        lower = r166.ge.earliest_possible_root_lower(candidate)
        if lower is None or not any(
            other.target_id != candidate.target_id
            and other.near is not None
            and bool(other.near < lower)
            for other in strict
        ):
            active.add(candidate.target_id)
    return "UNRESOLVED_MULTI", tuple(sorted(active))


def q_split(box: QBox) -> tuple[QBox, QBox]:
    widths = (
        (box.t1 - box.t0)
        / (r166.atlas.T_UPPER - r166.atlas.T_LOWER),
        box.r1 - box.r0,
        (box.s1 - box.s0) / (2 * r166.base.EPS),
    )
    axis = max(range(3), key=lambda index: widths[index])
    depth = box.depth + 1
    if axis == 0:
        middle = (box.t0 + box.t1) / 2
        return (
            QBox(
                box.t0, middle, box.r0, box.r1,
                box.s0, box.s1, depth,
            ),
            QBox(
                middle, box.t1, box.r0, box.r1,
                box.s0, box.s1, depth,
            ),
        )
    if axis == 1:
        middle = (box.r0 + box.r1) / 2
        return (
            QBox(
                box.t0, box.t1, box.r0, middle,
                box.s0, box.s1, depth,
            ),
            QBox(
                box.t0, box.t1, middle, box.r1,
                box.s0, box.s1, depth,
            ),
        )
    middle = (box.s0 + box.s1) / 2
    return (
        QBox(
            box.t0, box.t1, box.r0, box.r1,
            box.s0, middle, depth,
        ),
        QBox(
            box.t0, box.t1, box.r0, box.r1,
            middle, box.s1, depth,
        ),
    )


def profile_grazing(
    row: FrontierRow,
    max_depth: int = 8,
) -> dict[str, Any]:
    sign_p = 1 if row.box.p1 == 1 else -1
    require(
        (sign_p > 0 and row.box.p0 == Q(511, 512))
        or (sign_p < 0 and row.box.p1 == Q(-511, 512)),
        "grazing p collar",
    )
    root = QBox(
        row.box.t0,
        row.box.t1,
        Q(0),
        Q(1),
        row.box.s0,
        row.box.s1,
        0,
    )
    face = QBox(
        root.t0, root.t1, Q(0), Q(0),
        root.s0, root.s1, 0,
    )
    face_class, _face_active = q_classify(
        row.chart_id, sign_p, face, row.active_targets
    )
    pending = [(root, row.active_targets)]
    terminal_counts: Counter[str] = Counter()
    terminal_depths: Counter[int] = Counter()
    terminal_volume: dict[str, Q] = defaultdict(Q)
    residual_counts: Counter[str] = Counter()
    residual_volume = Q(0)
    terminal_coarse: list[str] = []
    while pending:
        box, active_targets = pending.pop()
        classification, active = q_classify(
            row.chart_id, sign_p, box, active_targets
        )
        if not classification.startswith("UNRESOLVED"):
            terminal_counts[classification] += 1
            terminal_depths[box.depth] += 1
            terminal_volume[classification] += Q(
                1, 2 ** box.depth
            )
            terminal_coarse.append(coarse_kind(classification))
        elif box.depth < max_depth:
            inherited = active or active_targets
            pending.extend(
                (child, inherited) for child in q_split(box)
            )
        else:
            residual_counts[classification] += 1
            residual_volume += Q(1, 2 ** box.depth)
    classified_volume = sum(terminal_volume.values(), Q(0))
    require(
        classified_volume + residual_volume == 1,
        "grazing parent volume",
    )
    if residual_counts:
        parent_kind = None
    elif set(terminal_coarse) == {"EXCLUDED"}:
        parent_kind = "EXCLUDED"
    elif set(terminal_coarse) == {"LIVE"}:
        parent_kind = "LIVE"
    else:
        parent_kind = "MIXED"
    return {
        "face_classification": face_class,
        "terminal_counts": terminal_counts,
        "terminal_depths": terminal_depths,
        "terminal_volume": terminal_volume,
        "residual_counts": residual_counts,
        "residual_volume": residual_volume,
        "classified_volume": classified_volume,
        "parent_kind": parent_kind,
    }


def fraction_map(values: dict[str, Q]) -> dict[str, str]:
    return {
        key: str(value)
        for key, value in sorted(values.items())
    }


def build_result() -> dict[str, Any]:
    upstream = check_chain()
    (
        frontier,
        prior_terminal_counts,
        origin_kinds,
        all_origins,
        prior_terminal_volume,
        replay_workload,
    ) = reconstruct_frontier()
    frontier_by_origin: Counter[str] = Counter(
        row.origin_key for row in frontier
    )
    category_keys: dict[str, list[str]] = defaultdict(list)
    residual_keys: dict[str, list[str]] = defaultdict(list)
    h_terminal_classes: Counter[str] = Counter()
    h_terminal_depths: Counter[int] = Counter()
    typed_strata: Counter[str] = Counter()
    monotone_witnesses: Counter[str] = Counter()
    grazing_face: Counter[str] = Counter()
    grazing_terminal: Counter[str] = Counter()
    grazing_terminal_depths: Counter[int] = Counter()
    grazing_terminal_volume: dict[str, Q] = defaultdict(Q)
    grazing_residual: Counter[str] = Counter()
    grazing_residual_volume = Q(0)
    grazing_parent_kind: Counter[str] = Counter()

    for row in frontier:
        if row.failure == "OUTGOING_CHART_SEAM_OVERWRAP":
            kind, classes, depths = h_partition(
                row.chart_id, row.box, row.origin_key
            )
            require(kind is not None, "all outgoing seams close")
            category_keys[kind].append(row.leaf_key)
            h_terminal_classes.update(classes)
            h_terminal_depths.update(depths)
            continue
        if row.failure in {
            "TYPED_FROZEN_OWNER_TANGENCY_GRAPH_COLLAR",
            "TYPED_OWNER_MISMATCH_TANGENCY_GRAPH_COLLAR",
        }:
            closed, witness = close_typed_tangency(row)
            if closed:
                category_keys["EXCLUDED"].append(row.leaf_key)
                typed_strata["NEGATIVE_OPEN_SIDE_DIMENSION_3"] += 1
                typed_strata["TANGENCY_GRAPH_DIMENSION_2"] += 1
                typed_strata["POSITIVE_OPEN_SIDE_DIMENSION_3"] += 1
                typed_strata[f"WITNESS:{witness}"] += 1
            else:
                residual_keys[
                    "TYPED_TANGENCY_PLUS_OUTGOING_SEAM_DOUBLE_GRAPH"
                ].append(row.leaf_key)
            continue
        if row.failure == "UNTYPED_DISCRIMINANT_COLLAR":
            records, unresolved = unique_unresolved_discriminant(row)
            if len(unresolved) > 1:
                require(2 <= len(unresolved) <= 5, "multi delta size")
                residual_keys[
                    "MULTI_DISCRIMINANT_2_TO_5_TARGETS"
                ].append(row.leaf_key)
                continue
            require(len(unresolved) == 1, "untyped delta target")
            candidate = unresolved[0]
            derivative_sign, lower, upper, full_graph = graph_faces(
                row, candidate
            )
            same_sign = (
                derivative_sign != 0
                and sign(lower) != 0
                and sign(lower) == sign(upper)
            )
            if same_sign:
                kind, witness = close_same_sign_discriminant(
                    row,
                    records,
                    candidate,
                    derivative_sign,
                    lower,
                    upper,
                )
                require(kind is not None, "same-sign box closes")
                category_keys[kind].append(row.leaf_key)
                monotone_witnesses[witness] += 1
            elif full_graph:
                residual_keys[
                    "FULL_P_DISCRIMINANT_GRAPH_REQUIRES_FIRST_ROOT_EQUALITY"
                ].append(row.leaf_key)
            else:
                residual_keys[
                    "CLIPPED_OR_FACE_OVERWRAP_SINGLE_DISCRIMINANT_GRAPH"
                ].append(row.leaf_key)
            continue
        require(
            row.failure == "SOURCE_GRAZING_ENDPOINT_COLLAR",
            "frontier failure dispatch",
        )
        profile = profile_grazing(row)
        grazing_face[profile["face_classification"]] += 1
        grazing_terminal.update(profile["terminal_counts"])
        grazing_terminal_depths.update(profile["terminal_depths"])
        for key, value in profile["terminal_volume"].items():
            grazing_terminal_volume[key] += value
        grazing_residual.update(profile["residual_counts"])
        grazing_residual_volume += profile["residual_volume"]
        if profile["parent_kind"] is None:
            residual_keys[
                "SOURCE_GRAZING_COMPACT_Q_PARENT_RESIDUAL"
            ].append(row.leaf_key)
            grazing_parent_kind["RESIDUAL"] += 1
        else:
            kind = profile["parent_kind"]
            require(kind in {"EXCLUDED", "LIVE"}, "grazing closed kind")
            category_keys[kind].append(row.leaf_key)
            grazing_parent_kind[kind] += 1

    for values in category_keys.values():
        values.sort()
    for values in residual_keys.values():
        values.sort()
    category_counts = Counter({
        key: len(values) for key, values in category_keys.items()
    })
    residual_counts = Counter({
        key: len(values) for key, values in residual_keys.items()
    })
    require(
        category_counts
        == {"EXCLUDED": 6250, "LIVE": 3590, "MIXED": 2900},
        "closed depth14 category census",
    )
    require(
        residual_counts
        == {
            "CLIPPED_OR_FACE_OVERWRAP_SINGLE_DISCRIMINANT_GRAPH": 26728,
            "FULL_P_DISCRIMINANT_GRAPH_REQUIRES_FIRST_ROOT_EQUALITY": 4812,
            "MULTI_DISCRIMINANT_2_TO_5_TARGETS": 10802,
            "SOURCE_GRAZING_COMPACT_Q_PARENT_RESIDUAL": 1478,
            "TYPED_TANGENCY_PLUS_OUTGOING_SEAM_DOUBLE_GRAPH": 220,
        },
        "residual category census",
    )
    require(
        sum(category_counts.values()) == 12740
        and sum(residual_counts.values()) == 44040,
        "depth14 record conservation",
    )
    require(
        h_terminal_classes
        == {
            "MONOTONE_H_OUTGOING_CHART_MISMATCH_RECTANGLE": 726,
            "MONOTONE_H_PREFIX_STAGE_ONE_MATCH_RECTANGLE": 714,
            "STRICT_OUTGOING_CHART_MISMATCH_RECTANGLE": 1824,
            "STRICT_PREFIX_STAGE_ONE_MATCH_RECTANGLE": 1606,
            "TYPED_SEAM_GRAPH_AND_TWO_OPEN_SIDES": 2792,
        }
        and h_terminal_depths == {0: 7458, 1: 4, 2: 200},
        "outgoing H terminal census",
    )
    require(
        sum(
            value for key, value in typed_strata.items()
            if key == "TANGENCY_GRAPH_DIMENSION_2"
        ) == 1000,
        "typed tangency closure count",
    )
    require(
        sum(monotone_witnesses.values()) == 4076,
        "same-sign monotone census",
    )
    require(
        grazing_parent_kind
        == {"EXCLUDED": 102, "LIVE": 52, "RESIDUAL": 1478},
        "grazing parent census",
    )
    require(
        grazing_face
        == {
            "EXCLUDED_OUTGOING_CHART_MISMATCH": 48,
            "EXCLUDED_UNIQUE_FIRST_OWNER_MISMATCH": 1024,
            "LIVE_FROZEN_STAGE_ONE_OWNER_CHART_MATCH": 424,
            "UNRESOLVED_MULTI": 92,
            "UNRESOLVED_OUTGOING_SEAM": 44,
        },
        "grazing face census",
    )
    require(
        grazing_terminal
        == {
            "EXCLUDED_OUTGOING_CHART_MISMATCH": 5610,
            "EXCLUDED_UNIQUE_FIRST_OWNER_MISMATCH": 25754,
            "LIVE_FROZEN_STAGE_ONE_OWNER_CHART_MATCH": 9834,
        }
        and grazing_residual
        == {
            "UNRESOLVED_MULTI": 39852,
            "UNRESOLVED_OUTGOING_SEAM": 8192,
        },
        "grazing q-cell census",
    )
    require(
        grazing_terminal_volume
        == {
            "EXCLUDED_OUTGOING_CHART_MISMATCH": Q(5747, 128),
            "EXCLUDED_UNIQUE_FIRST_OWNER_MISMATCH": Q(7829, 8),
            "LIVE_FROZEN_STAGE_ONE_OWNER_CHART_MATCH": Q(53863, 128),
        }
        and grazing_residual_volume == Q(12011, 64),
        "grazing volume census",
    )

    # Update origin replacement state, but do not mutate the Round168 ledger.
    closed_by_origin: Counter[str] = Counter()
    for kind, keys in category_keys.items():
        for key in keys:
            chart_id, path = key.split(":", 1)
            # The origin is read from the frontier row registry below.
            _ = chart_id, path
    row_by_key = {row.leaf_key: row for row in frontier}
    for kind, keys in category_keys.items():
        for key in keys:
            origin = row_by_key[key].origin_key
            closed_by_origin[origin] += 1
            origin_kinds[origin].add(kind)
    fully_replaced = {
        origin for origin in all_origins
        if closed_by_origin[origin] == frontier_by_origin[origin]
    }
    origin_categories: dict[str, list[str]] = defaultdict(list)
    for origin in sorted(fully_replaced):
        kinds = origin_kinds[origin]
        if kinds == {"EXCLUDED"}:
            category = "WHOLE_ORIGIN_PARENT_EXCLUDED"
        elif kinds == {"LIVE"}:
            category = "WHOLE_ORIGIN_PARENT_LIVE"
        else:
            category = "RESOLVED_MIXED_OR_ANALYTIC_PARTITION"
        origin_categories[category].append(origin)
    prior_complete = {
        origin for origin in all_origins
        if frontier_by_origin[origin] == 0
    }
    newly_complete = fully_replaced - prior_complete
    require(
        len(all_origins) == 2616
        and len(prior_complete) == 376
        and len(newly_complete) == 78
        and len(fully_replaced) == 454,
        "origin replacement census",
    )

    grazing_excluded = (
        grazing_terminal_volume[
            "EXCLUDED_OUTGOING_CHART_MISMATCH"
        ]
        + grazing_terminal_volume[
            "EXCLUDED_UNIQUE_FIRST_OWNER_MISMATCH"
        ]
    ) / 64
    grazing_live = (
        grazing_terminal_volume[
            "LIVE_FROZEN_STAGE_ONE_OWNER_CHART_MATCH"
        ]
    ) / 64
    grazing_residual_parent_volume = grazing_residual_volume / 64
    non_grazing_excluded = Q(6148, 64)
    non_grazing_live = Q(3538, 64)
    non_grazing_mixed = Q(2900, 64)
    round170_excluded_volume = non_grazing_excluded + grazing_excluded
    round170_live_volume = non_grazing_live + grazing_live
    round170_mixed_volume = non_grazing_mixed
    round170_classified_volume = (
        round170_excluded_volume
        + round170_live_volume
        + round170_mixed_volume
    )
    round170_residual_volume = (
        Q(26728 + 4812 + 10802 + 220, 64)
        + grazing_residual_parent_volume
    )
    require(
        round170_excluded_volume == Q(917955, 8192)
        and round170_live_volume == Q(506727, 8192)
        and round170_mixed_volume == Q(371200, 8192)
        and round170_classified_volume == Q(897941, 4096)
        and round170_residual_volume == Q(2735979, 4096)
        and round170_classified_volume + round170_residual_volume
        == Q(14195, 16),
        "Round170 volume conservation",
    )
    prior_terminal_total = sum(
        prior_terminal_volume.values(), Q(0)
    )
    require(
        prior_terminal_total == Q(27661, 16)
        and prior_terminal_total + Q(14195, 16) == 2616,
        "owner-active depth14 partition",
    )

    all_frontier_keys = sorted(row_by_key)
    closed_keys = sorted(
        key for values in category_keys.values() for key in values
    )
    residual_all_keys = sorted(
        key for values in residual_keys.values() for key in values
    )
    result = {
        "verdict": "PARTIAL",
        "status": (
            "PARTIAL_BOUNDED_GRAPH_CELL_EXPLORATION_ONLY__"
            "NO_FORMAL_CORE_GATE_CREDIT__ROUND168_LEDGER_UNCHANGED"
        ),
        "scope": {
            "source_obstacle": "W",
            "frozen_owner": "W[1,0]",
            "frozen_outgoing_chart": "W",
            "ambient_parameter_dimension": 3,
            "graph_dimension": 2,
            "graph_typing_is_not_whole_record_credit": True,
            "round166_depth14_tree_replayed": True,
            "source_grazing_is_bounded_volume_profile": True,
            "bounded_exploratory_only": True,
            "not_formal_core_gate_credit": True,
            "throwaway_spike_was_rewritten_but_not_promoted": True,
            "not_D02_closure": True,
        },
        "upstream_verified_chain": upstream,
        "round166_full_tree_replay": {
            **replay_workload,
            "owner_active_depth8_parent_count": 2616,
            "prior_terminal_child_record_count":
                sum(prior_terminal_counts.values()),
            "prior_terminal_child_records_by_disposition":
                dict(sorted(prior_terminal_counts.items())),
            "prior_terminal_baseline_parent_equivalent_by_disposition":
                fraction_map(prior_terminal_volume),
            "prior_terminal_baseline_parent_equivalent":
                str(prior_terminal_total),
            "depth14_frontier_child_record_count": len(frontier),
            "depth14_frontier_baseline_parent_equivalent":
                str(Q(len(frontier), 64)),
        },
        "bounded_blocks": {
            "outgoing_H_seams": {
                "input_depth14_parent_record_count": 7510,
                "closed_depth14_parent_record_count": 7510,
                "whole_parent_excluded": 2550,
                "whole_parent_live": 2180,
                "typed_or_mixed_analytic_partition": 2780,
                "input_baseline_parent_equivalent": str(Q(7510, 64)),
                "excluded_baseline_parent_equivalent": str(Q(2550, 64)),
                "live_baseline_parent_equivalent": str(Q(2180, 64)),
                "mixed_baseline_parent_equivalent": str(Q(2780, 64)),
                "terminal_H_cell_count_by_class":
                    dict(sorted(h_terminal_classes.items())),
                "terminal_H_cell_count_by_extra_depth": {
                    str(key): value
                    for key, value in sorted(h_terminal_depths.items())
                },
                "three_stratum_cell_dimensions": [3, 2, 3],
                "half_open_graph_owner": "W",
            },
            "typed_tangency_three_stratum_closure": {
                "input_depth14_parent_record_count": 1220,
                "closed_all_three_strata_excluded": 1000,
                "residual_double_graph_arrangement": 220,
                "closed_baseline_parent_equivalent": str(Q(1000, 64)),
                "residual_baseline_parent_equivalent": str(Q(220, 64)),
                "stratum_witness_counts":
                    dict(sorted(typed_strata.items())),
                "partition": [
                    {"predicate": "Delta<0", "dimension": 3},
                    {"predicate": "Delta=0", "dimension": 2},
                    {"predicate": "Delta>0", "dimension": 3},
                ],
                "whole_child_exclusion_requires_all_three_excluded": True,
            },
            "same_sign_monotone_discriminant": {
                "input_depth14_parent_record_count": 4076,
                "whole_parent_excluded": 2598,
                "whole_parent_live": 1358,
                "typed_or_mixed_H_partition": 120,
                "residual": 0,
                "input_baseline_parent_equivalent": str(Q(4076, 64)),
                "excluded_baseline_parent_equivalent": str(Q(2598, 64)),
                "live_baseline_parent_equivalent": str(Q(1358, 64)),
                "mixed_baseline_parent_equivalent": str(Q(120, 64)),
                "witness_counts":
                    dict(sorted(monotone_witnesses.items())),
                "strict_identity":
                    "dDelta/dp=2*transverse*ell/sqrt(1-p^2)",
                "same_strict_sign_on_both_p_faces_implies_no_Delta_zero_graph":
                    True,
            },
            "source_grazing_compact_q_profile": {
                "input_depth14_parent_record_count": 1632,
                "coordinate": {
                    "r_interval": "[0,1]",
                    "q": "sqrt(1023/262144)*r",
                    "p": "sign*sqrt(1-(1023/262144)*r^2)",
                    "grazing_face": "r=0",
                },
                "grazing_face_dimension": 2,
                "interior_dimension": 3,
                "grazing_face_classification":
                    dict(sorted(grazing_face.items())),
                "max_extra_q_depth": 8,
                "whole_depth14_parent_records": {
                    "excluded": 102,
                    "live": 52,
                    "residual": 1478,
                },
                "q_terminal_cell_count_by_disposition":
                    dict(sorted(grazing_terminal.items())),
                "q_terminal_cell_count_by_extra_depth": {
                    str(key): value
                    for key, value in sorted(
                        grazing_terminal_depths.items()
                    )
                },
                "q_terminal_depth14_parent_equivalent_by_disposition":
                    fraction_map(grazing_terminal_volume),
                "q_residual_cell_count_by_type":
                    dict(sorted(grazing_residual.items())),
                "q_residual_depth14_parent_equivalent":
                    str(grazing_residual_volume),
                "classified_baseline_parent_equivalent":
                    str(
                        sum(grazing_terminal_volume.values(), Q(0)) / 64
                    ),
                "residual_baseline_parent_equivalent":
                    str(grazing_residual_parent_volume),
                "two_dimensional_face_not_counted_as_volume": True,
            },
        },
        "three_noninterchangeable_ledgers": {
            "depth14_terminal_child_records": {
                "input": 56780,
                "whole_excluded": 6250,
                "whole_live": 3590,
                "typed_or_mixed_analytic_partition": 2900,
                "semantically_closed": 12740,
                "residual": 44040,
                "identity": "6250+3590+2900+44040=56780",
            },
            "rational_baseline_parent_equivalent_volume": {
                "Round170_excluded": str(round170_excluded_volume),
                "Round170_live": str(round170_live_volume),
                "Round170_mixed_analytic": str(round170_mixed_volume),
                "Round170_classified": str(round170_classified_volume),
                "Round170_residual": str(round170_residual_volume),
                "Round166_frontier_input": str(Q(14195, 16)),
                "conservation":
                    "897941/4096+2735979/4096=14195/16",
            },
            "Round168_original_depth8_parent_records": {
                "input_owner_active_multi": 2616,
                "fully_replaced_before_Round170_bounded_blocks":
                    len(prior_complete),
                "newly_fully_replaced_by_Round170_bounded_blocks":
                    len(newly_complete),
                "fully_replaced_total_after_verified_depth14_replay":
                    len(fully_replaced),
                "still_not_fully_replaced":
                    2616 - len(fully_replaced),
                "fully_replaced_by_disposition": {
                    key: len(values)
                    for key, values in sorted(origin_categories.items())
                },
                "child_count_never_added_directly_to_original_parent_ledger":
                    True,
                "Round168_integer_ledger_mutated": False,
                "official_Round168_integer_credit_delta": 0,
                "whole_parent_integer_credit_claimed": 0,
            },
        },
        "residual": {
            "depth14_record_count_by_hard_type":
                dict(sorted(residual_counts.items())),
            "depth14_record_baseline_parent_equivalent_by_hard_type": {
                key: str(Q(value, 64))
                for key, value in sorted(residual_counts.items())
            },
            "hard_blocks": [
                "10,802 multi-Delta arrangements",
                "4,812 full-p Delta graphs requiring first-root equality sheets",
                "220 tangency/outgoing-seam double-graph arrangements",
                "1,478 compact-q grazing parents with residual q cells",
                "26,728 clipped or face-overwrapped single-Delta graphs",
            ],
        },
        "key_digests": {
            "all_frontier_leaf_keys_sha256": digest(all_frontier_keys),
            "closed_frontier_leaf_keys_sha256": digest(closed_keys),
            "residual_frontier_leaf_keys_sha256": digest(residual_all_keys),
            "closed_by_category_sha256": {
                key: digest(values)
                for key, values in sorted(category_keys.items())
            },
            "residual_by_category_sha256": {
                key: digest(values)
                for key, values in sorted(residual_keys.items())
            },
            "fully_replaced_origin_by_category_sha256": {
                key: digest(values)
                for key, values in sorted(origin_categories.items())
            },
        },
        "strict_nonpromotion": {
            "Round168_whole_record_excluded": 73162,
            "Round168_conservative_live": 3670,
            "Round168_ledger_unchanged": True,
            "bounded_counts_are_not_official_ledger_credit": True,
            "volume_or_child_record_to_whole_parent_integer_conversion":
                "FORBIDDEN",
            "D02": "BLOCKED",
            "D03_negative_oracle": "UNAUTHORIZED",
            "CM2": "NO-GO_FOR_CLAIM",
        },
        "next_core_gate": (
            "interval-Newton arrangement of multi-Delta, first-root equality, "
            "clipped-Delta, tangency/seam, and residual compact-q graph cells"
        ),
        "provenance": {
            "producer": Path(__file__).name,
            "producer_sha256":
                hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            "python_flint": "0.9.0",
            "arb_precision_bits": 192,
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
