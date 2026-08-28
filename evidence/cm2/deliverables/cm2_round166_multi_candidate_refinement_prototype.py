#!/usr/bin/env python3
"""Round166 prototype: targeted refinement of the outside-W:W multi leaves.

This is an explicitly nonpromotional profiling prototype.  It leaves the
Round162--164 files untouched and replays their pinned 192-bit source-W
atlases with three semantics-preserving accelerations:

* retained candidate lists and target lookups are cached;
* phase geometry is evaluated once per box, rather than once per target;
* a child's candidate set is inherited from its parent's conservative
  ``active_targets`` set.

The last acceleration is rigorous.  A target removed from a parent active
set has a strict future root which is uniformly earlier on the whole parent.
That same inequality holds on every child.  Following the finite domination
chain ends at a retained active target, so an exact first target among the
inherited active set is also exact among the original retained candidates.

The frozen first prefix is

    first owner W[1,0], outgoing dominant chart W.

For exclusion it is enough to export an exact interval witness that some
strict future root is uniformly earlier than the frozen-owner lower bound.
This is called an ``owner-dominated`` earliest-prefix witness below; it does
not claim which target is globally first when several earlier targets remain.

Dependency: python-flint == 0.9.0.  Run with ``.venv-neurips/bin/python``.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import time
from collections import Counter, defaultdict
from dataclasses import dataclass
from fractions import Fraction as Q
from pathlib import Path
from typing import Any, Iterable

from flint import arb, ctx

import cm2_gate3_candidate_first_hit_cert as base
import cm2_gate3_eight_cell_symmetry_atlas_cert as atlas
import cm2_gate3_ge_interval_atlas_cert as ge


HERE = Path(__file__).resolve().parent
OUTPUT = HERE / "cm2_round166_multi_candidate_refinement_prototype_stats.json"
SCHEMA = "cm2.round166.multi-candidate-refinement-prototype.v1"
FROZEN_OWNER = "W[1,0]"
FROZEN_CHART = "W"
DIRECT_CHARTS = ("W:E", "W:N")
OUTSIDE_CHARTS = ("W:E", "W:N", "W:S")

PINNED_SHA256 = {
    "cm2_gate3_candidate_first_hit_cert.py":
        "6d224d74cda186a40ef9956d1dd6556d5a7b9f506d47c942427ceb66fd705bd2",
    "cm2_gate3_eight_cell_symmetry_atlas_cert.py":
        "d867f5cb03691289033d1a0d0e277a03e8395d70aae7e0689446d7aa63eac3da",
    "cm2_gate3_ge_interval_atlas_cert.py":
        "ab120f85a263f3cb0697d8a40bc9ed2bf12b361aa7c54940c214b6fd85b17e2b",
    "cm2_round164_tangency_strata_pruning_certificate.json":
        "2f1fcb72224f39c8d4a9d9f666a8579f71d77542e31552aa7c9dbc4b7338f092",
    "cm2_round164_tangency_strata_pruning_verification.json":
        "850bd24ae60979aaaea3f6819dcab665a1f7228d0c104014bfe8cce9e91299b0",
}
ROUND164_V2_RESULT_SHA256 = (
    "0f6d7f47ac20734ed294dd04cd7720ccbb9c0a1d4236980f814dd2ea2d5e79d9"
)
ROUND164_V2_VERIFICATION_RESULT_SHA256 = (
    "bb2e51bdbbd457a5782038efc527000cbf89b73c8645fd6facd126fa453af8c4"
)
CANDIDATE_SHA256 = {
    "W:E": "ebeeae12ba192d7808031ebf4be3537fb49e73e17295404adcad371045e7c2e7",
    "W:N": "4719c19ccb8c63288e8815c4b8961f64d9d096dd4377641acafbec59c00769e5",
    "W:S": "89d699755e74a71b2771fb907e3f1bcf0e13d96621a977a4731c563cb928a5f8",
}
BASELINE_LEAF_SHA256 = {
    "W:E": "248c0b77c22594ceb69f475978bcc9d7867530fcfaeefe1518e3538938c268e2",
    "W:N": "728dbce4e414bc859d050b3fa5619febcddd277d3354b2af6c32f3414212ea82",
    "W:S": "e3fbab0ef15d6b9fd06e1b78da40050eb29b8bb724ceb4ad5408926f7eeaa373",
}
BASELINE_COUNTS = {
    "W:E": {"leaf": 18930, "unique_first": 6518, "tangency_graph": 24, "multi_candidate": 12388},
    "W:N": {"leaf": 19484, "unique_first": 6584, "tangency_graph": 4, "multi_candidate": 12896},
    "W:S": {"leaf": 19484, "unique_first": 6584, "tangency_graph": 4, "multi_candidate": 12896},
}


def canonical(value: Any) -> str:
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"),
        ensure_ascii=False, allow_nan=False,
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
            require(key not in result, f"duplicate key:{path.name}")
            result[key] = value
        return result

    value = json.loads(
        raw.decode(),
        object_pairs_hook=unique,
        parse_constant=reject,
        parse_float=reject,
    )

    def check_strings(item: Any) -> None:
        if type(item) is str:
            require(
                "\x00" not in item
                and not any(
                    0xD800 <= ord(character) <= 0xDFFF
                    for character in item
                ),
                f"decoded string encoding:{path.name}",
            )
        elif type(item) is list:
            for child in item:
                check_strings(child)
        elif type(item) is dict:
            for key, child in item.items():
                check_strings(key)
                check_strings(child)

    check_strings(value)
    require(type(value) is dict, f"top object:{path.name}")
    return value


def check_pins() -> dict[str, Any]:
    for name, expected in PINNED_SHA256.items():
        actual = hashlib.sha256((HERE / name).read_bytes()).hexdigest()
        require(actual == expected, f"pin:{name}:{actual}")
    certificate = strict_load(
        HERE / "cm2_round164_tangency_strata_pruning_certificate.json"
    )
    verification = strict_load(
        HERE / "cm2_round164_tangency_strata_pruning_verification.json"
    )
    require(
        certificate["schema"]
        == "cm2.round164.dimension-safe-tangency-graph-typing.v2"
        and certificate["result_sha256"] == ROUND164_V2_RESULT_SHA256,
        "Round164 v2 certificate identity",
    )
    require(
        verification["schema"]
        == "cm2.round164.dimension-safe-tangency-graph-typing.verification.v2"
        and verification["result_sha256"]
        == ROUND164_V2_VERIFICATION_RESULT_SHA256
        and verification["result"]["status"] == "PASS"
        and verification["result"]["certificate_result_sha256"]
        == certificate["result_sha256"],
        "Round164 v2 verification identity",
    )
    result = certificate["result"]
    typing = result["tangency_graph_typing"]
    ambient = result["ambient_frozen_prefix_census"]
    rows = typing["rows"]
    require(
        result["scope"]["typed_graphs_are_terminal_codimension_one_strata"]
        and result["scope"]["typed_graphs_do_not_remove_ambient_parent_leaves"]
        and result["scope"]["off_graph_sides_remain_unresolved"],
        "Round164 v2 scope",
    )
    require(
        typing["ambient_parameter_dimension"] == 3
        and typing["ambient_parent_leaf_count"] == 32
        and typing["new_full_dimensional_parent_leaf_exclusion_count"] == 0
        and typing["remaining_off_graph_ambient_parent_count"] == 32
        and not typing["full_dimensional_parent_replacement_completed"]
        and all(
            row["ambient_parameter_dimension"] == 3
            and row["typed_graph_dimension"] == 2
            and row["credit_scope"] == "CODIMENSION_ONE_GRAPH_ONLY"
            and row["ambient_leaf_bulk_disposition"]
            == "UNRESOLVED_OFF_GRAPH_BULK"
            for row in rows
        ),
        "Round164 v2 dimension assertions",
    )
    require(
        ambient["combined_recordwise_excluded_ambient_leaf_count"] == 37480
        and ambient["remaining_ambient_unresolved_leaf_count"] == 39348
        and ambient["remaining_multi_candidate"] == 38180
        and ambient["remaining_tangency_ambient_leaf_bulk"] == 32
        and ambient["new_full_dimensional_ambient_leaf_exclusion_count"] == 0,
        "Round164 v2 ambient census",
    )
    return {
        "certificate_file_sha256": PINNED_SHA256[
            "cm2_round164_tangency_strata_pruning_certificate.json"
        ],
        "certificate_result_sha256": certificate["result_sha256"],
        "verification_file_sha256": PINNED_SHA256[
            "cm2_round164_tangency_strata_pruning_verification.json"
        ],
        "verification_result_sha256": verification["result_sha256"],
        "ambient_parameter_dimension": 3,
        "typed_graph_dimension": 2,
        "ambient_parent_leaf_count": 32,
        "full_dimensional_leaf_exclusion_count": 0,
        "ambient_recordwise_excluded_leaf_count": 37480,
        "ambient_remaining_leaf_count": 39348,
    }


# Freeze the exact upstream registries before monkey-patching their slow
# linear generators/lookups.  The tuple order is part of the certificate.
_candidate_cache = {
    chart_id: tuple(base.candidate_ids(chart_id))
    for chart_id in OUTSIDE_CHARTS
}
_target_cache = {target.target_id: target for target in base.TARGETS}


def install_fast_readonly_replay() -> None:
    for chart_id, values in _candidate_cache.items():
        require(
            base.canonical_digest(list(values)) == CANDIDATE_SHA256[chart_id],
            f"candidate digest:{chart_id}",
        )

    def candidate_ids(chart_id: str) -> list[str]:
        if chart_id in _candidate_cache:
            return list(_candidate_cache[chart_id])
        # Round166 never builds another chart.  Fail closed instead of silently
        # changing the scope of the prototype.
        raise KeyError(f"uncached chart:{chart_id}")

    def target_by_id(target_id: str) -> base.Target:
        return _target_cache[target_id]

    base.candidate_ids = candidate_ids
    base.target_by_id = target_by_id
    atlas.records = records_full
    atlas.root_record = root_record_fast


def root_record_from_geometry(
    geometry: tuple[arb, arb, arb, arb, arb, arb],
    target_id: str,
) -> ge.RootRecord:
    qx, qy, ux, uy, s, _radical_p = geometry
    target = _target_cache[target_id]
    ax, ay = base.target_center(target, s)
    dx, dy = ax - qx, ay - qy
    ell = ux * dx + uy * dy
    transverse = -uy * dx + ux * dy
    radius = base.arbq(base.RADIUS[target.obstacle])
    discriminant = radius * radius - transverse * transverse
    if bool(discriminant < 0):
        return ge.RootRecord(
            target_id, "no_real_intersection", ell, discriminant,
            None, None, transverse,
        )
    if not bool(discriminant > 0):
        return ge.RootRecord(
            target_id, "unresolved_discriminant", ell, discriminant,
            None, None, transverse,
        )
    radical = discriminant.sqrt()
    near, far = ell - radical, ell + radical
    if bool(far < 0):
        classification = "intersection_behind"
    elif bool(near > 0):
        classification = "strict_future_root"
    else:
        classification = "unresolved_root_sign"
    return ge.RootRecord(
        target_id, classification, ell, discriminant,
        near, far, transverse,
    )


def root_record_fast(
    chart_id: str,
    box: ge.AtlasBox,
    target_id: str,
) -> ge.RootRecord:
    return root_record_from_geometry(atlas.geometry(chart_id, box), target_id)


def records_for(
    chart_id: str,
    box: ge.AtlasBox,
    target_ids: Iterable[str],
) -> list[ge.RootRecord]:
    geometry = atlas.geometry(chart_id, box)
    return [
        root_record_from_geometry(geometry, target_id)
        for target_id in target_ids
    ]


def records_full(chart_id: str, box: ge.AtlasBox) -> list[ge.RootRecord]:
    return records_for(chart_id, box, _candidate_cache[chart_id])


def root_at_fixed_p(
    chart_id: str,
    box: ge.AtlasBox,
    target_id: str,
    p: Q,
) -> ge.RootRecord:
    face = ge.AtlasBox(
        box.t0, box.t1, p, p, box.s0, box.s1,
        box.depth, box.path,
    )
    return root_record_fast(chart_id, face, target_id)


def physical_tangency_graph(
    chart_id: str,
    box: ge.AtlasBox,
    candidate: ge.RootRecord,
    all_records: list[ge.RootRecord],
) -> bool:
    if candidate.classification != "unresolved_discriminant":
        return False
    if box.p0 <= -1 or box.p1 >= 1:
        return False
    *_unused, radical_p = atlas.geometry(chart_id, box)
    if (
        not bool(radical_p > 0)
        or not bool(candidate.ell > 0)
        or not bool(candidate.ell < base.arbq(base.TAU_MAX))
    ):
        return False
    derivative = 2 * candidate.transverse * candidate.ell / radical_p
    if not (bool(derivative > 0) or bool(derivative < 0)):
        return False
    lower = root_at_fixed_p(
        chart_id, box, candidate.target_id, box.p0,
    ).discriminant
    upper = root_at_fixed_p(
        chart_id, box, candidate.target_id, box.p1,
    ).discriminant
    if bool(derivative > 0):
        if not (bool(lower < 0) and bool(upper > 0)):
            return False
    elif not (bool(lower > 0) and bool(upper < 0)):
        return False
    for other in all_records:
        if other.target_id == candidate.target_id:
            continue
        if other.classification in {
            "no_real_intersection", "intersection_behind",
        }:
            continue
        lower_root = ge.earliest_possible_root_lower(other)
        if lower_root is None or not bool(candidate.ell < lower_root):
            return False
    return True


def classify_from_records(
    chart_id: str,
    box: ge.AtlasBox,
    all_records: list[ge.RootRecord],
) -> ge.Leaf:
    strict = [
        row for row in all_records
        if row.classification == "strict_future_root"
    ]
    unresolved = [
        row for row in all_records
        if row.classification in {
            "unresolved_discriminant", "unresolved_root_sign",
        }
    ]
    if not strict and not unresolved:
        return ge.Leaf(
            box, "no_future_root", None, (), (),
            "all inherited roots absent or behind",
        )
    for candidate in strict:
        require(candidate.near is not None, "strict root payload")
        if all(
            other.target_id == candidate.target_id
            or other.classification in {
                "no_real_intersection", "intersection_behind",
            }
            or (
                (lower := ge.earliest_possible_root_lower(other))
                is not None
                and bool(candidate.near < lower)
            )
            for other in all_records
        ):
            return ge.Leaf(
                box, "unique_first", candidate.target_id,
                (candidate.target_id,), (),
                "exact inherited-active-set first root",
            )
    tangencies = tuple(
        row.target_id
        for row in unresolved
        if physical_tangency_graph(chart_id, box, row, all_records)
    )
    if len(tangencies) == 1:
        return ge.Leaf(
            box, "tangency_graph", tangencies[0],
            tangencies, tangencies,
            "unique monotone inherited-active-set first tangency",
        )
    active: set[str] = set()
    for candidate in strict + unresolved:
        lower = ge.earliest_possible_root_lower(candidate)
        if lower is None or not any(
            other.target_id != candidate.target_id
            and other.near is not None
            and bool(other.near < lower)
            for other in strict
        ):
            active.add(candidate.target_id)
    return ge.Leaf(
        box, "multi_candidate", None,
        tuple(sorted(active)), tangencies,
        "inherited interval ordering or boundary type not isolated",
    )


def classify_active(
    chart_id: str,
    box: ge.AtlasBox,
    target_ids: tuple[str, ...],
) -> tuple[ge.Leaf, list[ge.RootRecord]]:
    records = records_for(chart_id, box, target_ids)
    return classify_from_records(chart_id, box, records), records


def outgoing_chart(
    chart_id: str,
    box: ge.AtlasBox,
) -> tuple[str | None, dict[str, arb]]:
    record = root_record_fast(chart_id, box, FROZEN_OWNER)
    require(
        record.classification == "strict_future_root"
        and record.near is not None,
        "frozen owner strict root",
    )
    qx, qy, ux, uy, s, _radical_p = atlas.geometry(chart_id, box)
    target = _target_cache[FROZEN_OWNER]
    center_x, center_y = base.target_center(target, s)
    radius = base.arbq(base.RADIUS[target.obstacle])
    normal_x = (qx + record.near * ux - center_x) / radius
    normal_y = (qy + record.near * uy - center_y) / radius
    margins = {
        "E.first": normal_x - normal_y,
        "E.second": normal_x + normal_y,
        "W.first": -normal_x - normal_y,
        "W.second": -normal_x + normal_y,
        "N.first": normal_y - normal_x,
        "N.second": normal_y + normal_x,
        "S.first": -normal_y - normal_x,
        "S.second": -normal_y + normal_x,
    }
    for cell in ("E", "W", "N", "S"):
        if (
            bool(margins[f"{cell}.first"] > 0)
            and bool(margins[f"{cell}.second"] > 0)
        ):
            return cell, margins
    return None, margins


def baseline_fast() -> dict[str, list[ge.Leaf]]:
    direct_e = atlas.build_atlas("W:E")
    direct_n = atlas.build_atlas("W:N")
    charts = {
        "W:E": direct_e,
        "W:N": direct_n,
        "W:S": [
            atlas.reflect_leaf("W:N", "horizontal", leaf)
            for leaf in direct_n
        ],
    }
    for chart_id, leaves in charts.items():
        counts = Counter(leaf.classification for leaf in leaves)
        expected = BASELINE_COUNTS[chart_id]
        require(len(leaves) == expected["leaf"], f"leaf count:{chart_id}")
        for key in ("unique_first", "tangency_graph", "multi_candidate"):
            require(counts[key] == expected[key], f"{key} count:{chart_id}")
        rows = [
            atlas.leaf_row(chart_id, leaf)
            for leaf in sorted(leaves, key=lambda item: item.box.path)
        ]
        require(
            atlas.canonical_digest(rows) == BASELINE_LEAF_SHA256[chart_id],
            f"leaf digest:{chart_id}",
        )
    return charts


def inherited_owner_witness(
    chart_id: str,
    leaf: ge.Leaf,
) -> dict[str, Any]:
    """Replay why the frozen owner is absent from a parent active set."""

    require(
        leaf.classification == "multi_candidate"
        and FROZEN_OWNER not in leaf.active_targets,
        "owner-absent parent",
    )
    records = records_full(chart_id, leaf.box)
    owner = next(row for row in records if row.target_id == FROZEN_OWNER)
    if owner.classification in {
        "no_real_intersection", "intersection_behind",
    }:
        return {
            "kind": f"owner_{owner.classification}",
            "competitor": None,
        }
    lower = ge.earliest_possible_root_lower(owner)
    require(lower is not None, "inactive owner has lower bound")
    dominators = [
        row for row in records
        if row.target_id != FROZEN_OWNER
        and row.classification == "strict_future_root"
        and row.near is not None
        and bool(row.near < lower)
    ]
    require(bool(dominators), "inactive owner has strict dominator")
    # The order is deterministic and inherited from the pinned registry.
    return {
        "kind": "owner_dominated_by_strict_future_root",
        "competitor": dominators[0].target_id,
    }


@dataclass(frozen=True)
class Node:
    chart_id: str
    box: ge.AtlasBox
    active_targets: tuple[str, ...]
    origin_path: str


def split_axis(box: ge.AtlasBox, axis: int) -> tuple[ge.AtlasBox, ge.AtlasBox]:
    depth = box.depth + 1
    if axis == 0:
        middle = (box.t0 + box.t1) / 2
        return (
            ge.AtlasBox(
                box.t0, middle, box.p0, box.p1, box.s0, box.s1,
                depth, box.path + "0",
            ),
            ge.AtlasBox(
                middle, box.t1, box.p0, box.p1, box.s0, box.s1,
                depth, box.path + "1",
            ),
        )
    if axis == 1:
        middle = (box.p0 + box.p1) / 2
        return (
            ge.AtlasBox(
                box.t0, box.t1, box.p0, middle, box.s0, box.s1,
                depth, box.path + "0",
            ),
            ge.AtlasBox(
                box.t0, box.t1, middle, box.p1, box.s0, box.s1,
                depth, box.path + "1",
            ),
        )
    middle = (box.s0 + box.s1) / 2
    return (
        ge.AtlasBox(
            box.t0, box.t1, box.p0, box.p1, box.s0, middle,
            depth, box.path + "0",
        ),
        ge.AtlasBox(
            box.t0, box.t1, box.p0, box.p1, middle, box.s1,
            depth, box.path + "1",
        ),
    )


def longest_axis(box: ge.AtlasBox) -> int:
    widths = (
        box.t1 - box.t0,
        box.p1 - box.p0,
        box.s1 - box.s0,
    )
    return max(range(3), key=lambda index: widths[index])


def terminal_disposition(
    chart_id: str,
    leaf: ge.Leaf,
) -> tuple[str | None, dict[str, arb] | None]:
    if leaf.classification == "no_future_root":
        return "EXCLUDED_NO_INHERITED_FUTURE_ROOT", None
    # A tangency_graph is a certified codimension-one graph *inside* this
    # full-dimensional box.  It is not a volumetric disposition: the two
    # off-graph sides must still be split.  This is the crucial distinction
    # between a typed stratum and an excluded leaf record.
    if leaf.classification == "tangency_graph":
        return None, None
    if leaf.classification != "unique_first":
        return None, None
    if leaf.owner_target != FROZEN_OWNER:
        return "EXCLUDED_UNIQUE_FIRST_OWNER_MISMATCH", None
    cell, margins = outgoing_chart(chart_id, leaf.box)
    if cell is None:
        return None, margins
    if cell == FROZEN_CHART:
        return "LIVE_FROZEN_STAGE_ONE_OWNER_CHART_MATCH", margins
    return "EXCLUDED_OUTGOING_CHART_MISMATCH", margins


def unresolved_failure(
    chart_id: str,
    leaf: ge.Leaf,
    records: list[ge.RootRecord],
    seam_margins: dict[str, arb] | None,
) -> str:
    if leaf.classification == "tangency_graph":
        if leaf.owner_target == FROZEN_OWNER:
            return "TYPED_FROZEN_OWNER_TANGENCY_GRAPH_COLLAR"
        return "TYPED_OWNER_MISMATCH_TANGENCY_GRAPH_COLLAR"
    if leaf.classification == "unique_first":
        require(leaf.owner_target == FROZEN_OWNER, "only owner seam unresolved")
        require(seam_margins is not None, "seam margins")
        # The eight chart margins contain opposite duplicates.  There are
        # only two independent diagonal seam equations: nx-ny and nx+ny.
        independent = [
            seam_margins["E.first"],
            seam_margins["E.second"],
        ]
        ambiguous = [
            value for value in independent
            if not bool(value > 0) and not bool(value < 0)
        ]
        if len(ambiguous) == 2:
            return "OUTGOING_CHART_CORNER_OVERWRAP"
        return "OUTGOING_CHART_SEAM_OVERWRAP"
    if box_touches_source_grazing(leaf.box):
        return "SOURCE_GRAZING_ENDPOINT_COLLAR"
    if len(leaf.tangency_targets) > 1:
        return "MULTIPLE_FIRST_TANGENCY_GRAPHS"
    classes = Counter(record.classification for record in records)
    if classes["unresolved_root_sign"]:
        return "UNRESOLVED_ROOT_SIGN"
    if classes["unresolved_discriminant"]:
        return "UNTYPED_DISCRIMINANT_COLLAR"
    if classes["strict_future_root"] >= 2:
        return "STRICT_ROOT_ORDER_OVERLAP"
    return "MIXED_INTERVAL_DEPENDENCY"


def box_touches_source_grazing(box: ge.AtlasBox) -> bool:
    return box.p0 == -1 or box.p1 == 1


def profile(
    charts: dict[str, list[ge.Leaf]],
    extra_depth: int,
) -> dict[str, Any]:
    baseline_multi = {
        chart_id: [
            leaf for leaf in leaves
            if leaf.classification == "multi_candidate"
        ]
        for chart_id, leaves in charts.items()
    }
    require(
        all(
            leaf.box.depth == atlas.MAX_DEPTH
            for leaves in baseline_multi.values()
            for leaf in leaves
        ),
        "all baseline multi leaves at pinned maximum depth",
    )
    immediate_counts: Counter[str] = Counter()
    immediate_competitors: Counter[str] = Counter()
    pending: list[Node] = []
    baseline_active_sizes: Counter[int] = Counter()
    chart_baseline: dict[str, Any] = {}
    for chart_id, leaves in baseline_multi.items():
        owner_present = 0
        owner_absent = 0
        for leaf in leaves:
            baseline_active_sizes[len(leaf.active_targets)] += 1
            if FROZEN_OWNER not in leaf.active_targets:
                owner_absent += 1
                witness = inherited_owner_witness(chart_id, leaf)
                immediate_counts[witness["kind"]] += 1
                if witness["competitor"] is not None:
                    immediate_competitors[witness["competitor"]] += 1
            else:
                owner_present += 1
                pending.append(Node(
                    chart_id, leaf.box, leaf.active_targets, leaf.box.path,
                ))
        chart_baseline[chart_id] = {
            "multi_candidate": len(leaves),
            "frozen_owner_in_active": owner_present,
            "frozen_owner_absent_exact_prefix_exclusion": owner_absent,
        }

    snapshots: list[dict[str, Any]] = []
    terminal: Counter[str] = Counter()
    terminal_by_chart: dict[str, Counter[str]] = defaultdict(Counter)
    evaluated_boxes = 0
    evaluated_target_records = 0
    final_failure: Counter[str] = Counter()
    final_active_sizes: Counter[int] = Counter()
    final_depths: Counter[int] = Counter()
    terminal_parent_volume: Counter[str] = Counter()
    typed_stratum_boxes: Counter[str] = Counter()

    # Levels are relative to the pinned depth-8 parent leaves.  A terminal
    # result persists and is not reevaluated at later snapshots.
    for relative_depth in range(extra_depth + 1):
        next_pending: list[Node] = []
        level_failures: Counter[str] = Counter()
        level_active_sizes: Counter[int] = Counter()
        for node in pending:
            leaf, records = classify_active(
                node.chart_id, node.box, node.active_targets,
            )
            evaluated_boxes += 1
            evaluated_target_records += len(node.active_targets)
            disposition, seam_margins = terminal_disposition(
                node.chart_id, leaf,
            )
            if disposition is not None:
                terminal[disposition] += 1
                terminal_by_chart[node.chart_id][disposition] += 1
                terminal_parent_volume[disposition] += Q(
                    1, 2 ** relative_depth,
                )
                continue
            failure = unresolved_failure(
                node.chart_id, leaf, records, seam_margins,
            )
            if leaf.classification == "tangency_graph":
                typed_stratum_boxes[failure] += 1
            level_failures[failure] += 1
            if leaf.classification == "unique_first":
                inherited = (FROZEN_OWNER,)
            elif leaf.classification == "tangency_graph":
                # The tangency target may disappear on one side of its graph,
                # so keep the input active registry for the off-graph bulk.
                inherited = node.active_targets
            else:
                inherited = leaf.active_targets
            level_active_sizes[len(inherited)] += 1
            if relative_depth == extra_depth:
                final_failure[failure] += 1
                final_active_sizes[len(inherited)] += 1
                final_depths[leaf.box.depth] += 1
                continue
            axis = longest_axis(node.box)
            for child in split_axis(node.box, axis):
                next_pending.append(Node(
                    node.chart_id, child, inherited, node.origin_path,
                ))
        snapshots.append({
            "extra_depth": relative_depth,
            "absolute_max_depth": atlas.MAX_DEPTH + relative_depth,
            "new_terminal_subboxes_cumulative": dict(sorted(terminal.items())),
            "unresolved_subbox_count": sum(level_failures.values()),
            "unresolved_parent_box_volume_equivalent": str(Q(
                sum(level_failures.values()), 2 ** relative_depth,
            )),
            "terminal_parent_box_volume_equivalent_cumulative": str(
                sum(terminal_parent_volume.values(), Q(0))
            ),
            "typed_stratum_box_witnesses_cumulative":
                dict(sorted(typed_stratum_boxes.items())),
            "unresolved_failure_types": dict(sorted(level_failures.items())),
            "unresolved_active_size": {
                str(key): value
                for key, value in sorted(level_active_sizes.items())
            },
        })
        pending = next_pending

    immediate_excluded = sum(immediate_counts.values())
    owner_active = sum(
        row["frozen_owner_in_active"]
        for row in chart_baseline.values()
    )
    terminal_volume_total = sum(terminal_parent_volume.values(), Q(0))
    final_unresolved_equivalent = Q(
        sum(final_failure.values()), 2 ** extra_depth,
    )
    require(
        terminal_volume_total + final_unresolved_equivalent == owner_active,
        "targeted parent-volume partition",
    )
    classified_equivalent = Q(immediate_excluded) + terminal_volume_total
    return {
        "baseline": {
            "outside_W_W_multi_candidate_count":
                sum(len(leaves) for leaves in baseline_multi.values()),
            "all_multi_leaves_at_pinned_maximum_depth": atlas.MAX_DEPTH,
            "charts": chart_baseline,
            "active_target_size": {
                str(key): value
                for key, value in sorted(baseline_active_sizes.items())
            },
            "immediate_exact_prefix_exclusion_witness_types":
                dict(sorted(immediate_counts.items())),
            "immediate_dominator_targets":
                dict(immediate_competitors.most_common()),
        },
        "refinement": {
            "split_policy":
                "bisect largest raw (t,p,s) rational width; stable t,p,s tie break",
            "maximum_extra_depth": extra_depth,
            "snapshots": snapshots,
            "terminal_subboxes_by_chart": {
                chart_id: dict(sorted(counts.items()))
                for chart_id, counts in sorted(terminal_by_chart.items())
            },
            "evaluated_box_count": evaluated_boxes,
            "evaluated_target_record_count": evaluated_target_records,
            "terminal_parent_box_volume_by_disposition": {
                key: str(value)
                for key, value in sorted(terminal_parent_volume.items())
            },
            "final_unresolved_failure_types": dict(sorted(final_failure.items())),
            "final_unresolved_active_size": {
                str(key): value
                for key, value in sorted(final_active_sizes.items())
            },
            "final_unresolved_absolute_depth": {
                str(key): value
                for key, value in sorted(final_depths.items())
            },
            "parent_box_equivalent_summary": {
                "immediate_whole_parent_exclusions": str(immediate_excluded),
                "owner_active_input": str(owner_active),
                "terminal_classified_subbox_volume":
                    str(terminal_volume_total),
                "final_unresolved_subbox_volume":
                    str(final_unresolved_equivalent),
                "classified_multi_parent_equivalent":
                    str(classified_equivalent),
                "classified_fraction_of_38180":
                    str(classified_equivalent / Q(38180)),
                "unresolved_fraction_of_38180":
                    str(final_unresolved_equivalent / Q(38180)),
            },
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--extra-depth", type=int, default=3)
    parser.add_argument("--output", type=Path, default=OUTPUT)
    args = parser.parse_args()
    require(0 <= args.extra_depth <= 12, "extra depth range")
    ctx.prec = 192
    round164_v2_chain = check_pins()
    started = time.perf_counter()
    install_fast_readonly_replay()
    replay_started = time.perf_counter()
    charts = baseline_fast()
    replay_finished = time.perf_counter()
    result = profile(charts, args.extra_depth)
    finished = time.perf_counter()
    result.update({
        "status": (
            "NONPROMOTIONAL_PROTOTYPE__"
            "VALID_ROUND163_AMBIENT_BASELINE"
        ),
        "algorithm": {
            "candidate_registry_cached_and_digest_checked": True,
            "target_lookup_O1": True,
            "one_geometry_evaluation_per_box": True,
            "parent_active_set_inherited": True,
            "parent_inactive_target_inequalities_persist_on_children": True,
            "terminal_unique_first_is_exact_over_full_retained_registry": True,
            "owner_dominated_witness_is_exact_prefix_exclusion": True,
        },
        "baseline_replay": {
            "candidate_sha256": CANDIDATE_SHA256,
            "leaf_rows_sha256": BASELINE_LEAF_SHA256,
            "all_pinned_leaf_digests_reproduced": True,
        },
        "round164_v2_dimension_safe_chain": round164_v2_chain,
        "provenance": {
            "round166_producer": Path(__file__).name,
            "round166_producer_sha256":
                hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            "dependency_sha256": PINNED_SHA256,
        },
        "runtime_seconds": {
            "baseline_fast_replay":
                format(replay_finished - replay_started, ".6f"),
            "targeted_refinement":
                format(finished - replay_finished, ".6f"),
            "total": format(finished - started, ".6f"),
        },
        "strict_nonpromotion": {
            "prototype_not_an_independent_verifier": True,
            "round164_tangency_owner_mismatch_is_only_a_codimension_one_stratum": True,
            "round164_tangency_rows_do_not_subtract_full_dimensional_leaf_records": True,
            "valid_round163_combined_excluded_leaf_records": 37480,
            "valid_round163_remaining_leaf_records": 39348,
            "D02": "BLOCKED",
            "D03_negative_oracle": "UNAUTHORIZED",
            "CM2": "NO-GO_FOR_CLAIM",
        },
    })
    document = {
        "schema": SCHEMA,
        "result": result,
        "result_sha256": digest(result),
    }
    args.output.write_text(
        json.dumps(
            document, sort_keys=True, indent=2,
            ensure_ascii=False, allow_nan=False,
        ) + "\n"
    )
    print(document["result_sha256"])
    print(json.dumps(result["runtime_seconds"], sort_keys=True))
    print(json.dumps(result["baseline"], sort_keys=True))
    print(json.dumps(
        result["refinement"]["snapshots"], sort_keys=True,
    ))


if __name__ == "__main__":
    main()
