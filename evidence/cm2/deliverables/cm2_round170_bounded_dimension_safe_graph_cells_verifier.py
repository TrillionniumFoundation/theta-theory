#!/usr/bin/env python3
"""Verifier for the bounded Round170 PARTIAL exploration.

The verifier does not import the Round170 producer.  It does import the
pinned Round165/Round166 producer modules, fully replays their claimed
depth-14 tree relative to those pins, and separately re-evaluates every
Round170 seam, tangency, same-sign discriminant, and compact-q classification.
It therefore is not algorithmically independent of the upstream tree code.
"""

from __future__ import annotations

import argparse
import copy
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
CERTIFICATE = (
    HERE / "cm2_round170_bounded_dimension_safe_graph_cells_certificate.json"
)
OUTPUT = (
    HERE / "cm2_round170_bounded_dimension_safe_graph_cells_verification.json"
)
SCHEMA = (
    "cm2.round170.bounded-dimension-safe-graph-cells.verification.v1"
)
CERTIFICATE_SCHEMA = "cm2.round170.bounded-dimension-safe-graph-cells.v1"
PRODUCER_SHA256 = (
    "952ac26c6729a02e3c5c364c8dda89cdc19b756ac46f7d5da01786fa1b7ca75f"
)
# Filled after the final producer replay.
EXPECTED_CERTIFICATE_RESULT_SHA256 = (
    "3497231e62539574bb5610df4024f1d06a6a40d787a08e089427c028678c4117"
)
VERIFIER_PINS = {
    "cm2_round164_tangency_strata_pruning_certificate.json":
        "2f1fcb72224f39c8d4a9d9f666a8579f71d77542e31552aa7c9dbc4b7338f092",
    "cm2_round164_tangency_strata_pruning_verification.json":
        "850bd24ae60979aaaea3f6819dcab665a1f7228d0c104014bfe8cce9e91299b0",
    "cm2_round165_adaptive_typed_seam_census.py":
        "95bdbe3fc8d1d26512d8469a0e9382a3e977d5606375ed2729877c9f1ac8e012",
    "cm2_round165_adaptive_typed_seam_census_verification.json":
        "af684b956c40c97e26fdd5f9ddacea85b9c693b0b9a935d387ed1a5142ffa3b5",
    "cm2_round166_multi_candidate_refinement_prototype.py":
        "6479a78249a717169dea55ecabae98c05f240ea323fa0370037d43339158ae7c",
    "cm2_round166_multi_candidate_refinement_prototype_verification.json":
        "66f61b657eb72a0db90291d390d1021859c65ab059fdeaedabee95170102d1af",
    "cm2_round168_dimension_safe_source_W_stage_one_ledger_certificate.json":
        "adbdcc3ffbd791126dd759a5699bf65902ebb8529b173db52e4b45e5f299494e",
    "cm2_round168_dimension_safe_source_W_stage_one_ledger_verification.json":
        "994037b25d321e731e4cf4b61c92610fa99fadfccfa2d15ce2a38ccbe20a5cc9",
}

EXCLUSION_H = {
    "STRICT_OUTGOING_CHART_MISMATCH_RECTANGLE",
    "MONOTONE_H_OUTGOING_CHART_MISMATCH_RECTANGLE",
}
LIVE_H = {
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


def strict_load_bytes(raw: bytes, label: str) -> dict[str, Any]:
    require(
        not raw.startswith(b"\xef\xbb\xbf") and b"\x00" not in raw,
        f"encoding:{label}",
    )

    def reject(value: str) -> None:
        raise ValueError(value)

    def unique(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in pairs:
            require(key not in result, f"duplicate:{label}:{key}")
            result[key] = value
        return result

    value = json.loads(
        raw.decode(),
        object_pairs_hook=unique,
        parse_constant=reject,
        parse_float=reject,
    )

    def strings(item: Any) -> None:
        if type(item) is str:
            require(
                "\x00" not in item
                and not any(
                    0xD800 <= ord(character) <= 0xDFFF
                    for character in item
                ),
                f"decoded-string:{label}",
            )
        elif type(item) is list:
            for child in item:
                strings(child)
        elif type(item) is dict:
            for key, child in item.items():
                strings(key)
                strings(child)

    strings(value)
    require(type(value) is dict, f"top:{label}")
    return value


def strict_load(path: Path) -> dict[str, Any]:
    return strict_load_bytes(path.read_bytes(), path.name)


def check_verifier_chain() -> None:
    for name, expected in VERIFIER_PINS.items():
        require(
            hashlib.sha256((HERE / name).read_bytes()).hexdigest()
            == expected,
            f"verifier pin:{name}",
        )
    r164 = strict_load(
        HERE / "cm2_round164_tangency_strata_pruning_verification.json"
    )
    r165v = strict_load(
        HERE / "cm2_round165_adaptive_typed_seam_census_verification.json"
    )
    r166v = strict_load(
        HERE / "cm2_round166_multi_candidate_refinement_prototype_verification.json"
    )
    r168v = strict_load(
        HERE
        / "cm2_round168_dimension_safe_source_W_stage_one_ledger_verification.json"
    )
    require(
        r164["result"]["status"] == "PASS"
        and r165v["result"]["status"] == "PASS"
        and r166v["result_sha256"]
        == "bf88161e1310db2dc3531e300b0a20af9b7f1c008c0909824b8bfcf64b14097f"
        and r166v["result"]["status"]
        == "PASS_LIMITED_BASELINE_WITNESS_AND_CONSERVATION_VERIFICATION"
        and r168v["result"]["status"] == "PASS",
        "verifier chain identity",
    )


@dataclass(frozen=True)
class ShadowRow:
    chart_id: str
    box: r166.ge.AtlasBox
    active_targets: tuple[str, ...]
    origin_key: str
    failure: str

    @property
    def key(self) -> str:
        return f"{self.chart_id}:{self.box.path}"


def coarse(disposition: str) -> str:
    if disposition.startswith("EXCLUDED"):
        return "EXCLUDED"
    if disposition.startswith("LIVE"):
        return "LIVE"
    raise RuntimeError(disposition)


def replay_tree() -> tuple[
    list[ShadowRow],
    Counter[str],
    dict[str, Q],
    dict[str, set[str]],
    set[str],
    dict[str, int],
]:
    r166.check_pins()
    r166.install_fast_readonly_replay()
    charts = r166.baseline_fast()
    pending: list[r166.Node] = []
    origins: set[str] = set()
    for chart_id, leaves in charts.items():
        for leaf in leaves:
            if (
                leaf.classification == "multi_candidate"
                and r166.FROZEN_OWNER in leaf.active_targets
            ):
                origins.add(f"{chart_id}:{leaf.box.path}")
                pending.append(
                    r166.Node(
                        chart_id,
                        leaf.box,
                        leaf.active_targets,
                        leaf.box.path,
                    )
                )
    require(len(pending) == 2616, "shadow owner active")
    frontier: list[ShadowRow] = []
    terminal_counts: Counter[str] = Counter()
    terminal_volume: dict[str, Q] = defaultdict(Q)
    origin_kinds: dict[str, set[str]] = defaultdict(set)
    boxes = 0
    records_evaluated = 0
    for relative_depth in range(7):
        children: list[r166.Node] = []
        for node in pending:
            leaf, records = r166.classify_active(
                node.chart_id, node.box, node.active_targets
            )
            boxes += 1
            records_evaluated += len(node.active_targets)
            disposition, margins = r166.terminal_disposition(
                node.chart_id, leaf
            )
            origin = f"{node.chart_id}:{node.origin_path}"
            if disposition is not None:
                terminal_counts[disposition] += 1
                terminal_volume[disposition] += Q(
                    1, 2 ** relative_depth
                )
                origin_kinds[origin].add(coarse(disposition))
                continue
            failure = r166.unresolved_failure(
                node.chart_id, leaf, records, margins
            )
            if leaf.classification == "unique_first":
                inherited = (r166.FROZEN_OWNER,)
            elif leaf.classification == "tangency_graph":
                inherited = node.active_targets
            else:
                inherited = leaf.active_targets
            if relative_depth == 6:
                frontier.append(
                    ShadowRow(
                        node.chart_id,
                        node.box,
                        inherited,
                        origin,
                        failure,
                    )
                )
            else:
                axis = r166.longest_axis(node.box)
                children.extend(
                    r166.Node(
                        node.chart_id,
                        child,
                        inherited,
                        node.origin_path,
                    )
                    for child in r166.split_axis(node.box, axis)
                )
        pending = children
    require(
        len(frontier) == 56780
        and boxes == 167984
        and records_evaluated == 415570,
        "shadow tree workload",
    )
    return (
        frontier,
        terminal_counts,
        dict(terminal_volume),
        origin_kinds,
        origins,
        {
            "evaluated_box_count": boxes,
            "evaluated_target_record_count": records_evaluated,
        },
    )


def strict_sign(value: arb) -> int:
    if bool(value > 0):
        return 1
    if bool(value < 0):
        return -1
    return 0


def h_shadow(
    row: ShadowRow,
) -> tuple[str | None, Counter[str], Counter[int]]:
    pending = [(row.box, 0)]
    classes: Counter[str] = Counter()
    depths: Counter[int] = Counter()
    while pending:
        box, depth = pending.pop()
        terminal, state = r165.terminal_row(
            row.origin_key, row.chart_id, box, depth
        )
        if state == "terminal":
            require(terminal is not None, "shadow H row")
            classes[terminal["classification"]] += 1
            depths[depth] += 1
        elif depth < 4:
            pending.extend(
                (child, depth + 1) for child in r165.split_box(box)
            )
        else:
            return None, classes, depths
    keys = set(classes)
    if keys <= EXCLUSION_H:
        return "EXCLUDED", classes, depths
    if keys <= LIVE_H:
        return "LIVE", classes, depths
    return "MIXED", classes, depths


def active_records(
    row: ShadowRow,
) -> tuple[list[r166.ge.RootRecord], list[r166.ge.RootRecord]]:
    records = r166.records_for(
        row.chart_id, row.box, row.active_targets
    )
    unresolved = [
        record for record in records
        if record.classification == "unresolved_discriminant"
    ]
    return records, unresolved


def p_face_data(
    row: ShadowRow,
    candidate: r166.ge.RootRecord,
) -> tuple[int, arb, arb, bool]:
    *_unused, cp = r166.atlas.geometry(row.chart_id, row.box)
    derivative = (
        2 * candidate.transverse * candidate.ell / cp
        if bool(cp > 0)
        else arb(0)
    )
    derivative_sign = strict_sign(derivative)
    low = r166.root_at_fixed_p(
        row.chart_id,
        row.box,
        candidate.target_id,
        row.box.p0,
    ).discriminant
    high = r166.root_at_fixed_p(
        row.chart_id,
        row.box,
        candidate.target_id,
        row.box.p1,
    ).discriminant
    graph = (
        derivative_sign > 0 and bool(low < 0) and bool(high > 0)
    ) or (
        derivative_sign < 0 and bool(low > 0) and bool(high < 0)
    )
    return derivative_sign, low, high, graph


def remove_target_disposition(
    row: ShadowRow,
    records: list[r166.ge.RootRecord],
    target_id: str,
) -> str | None:
    leaf = r166.classify_from_records(
        row.chart_id,
        row.box,
        [
            record for record in records
            if record.target_id != target_id
        ],
    )
    disposition, _margins = r166.terminal_disposition(
        row.chart_id, leaf
    )
    return disposition


def target_first_on_positive(
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


def shadow_positive_chart(
    row: ShadowRow,
    candidate: r166.ge.RootRecord,
) -> str | None:
    _qx, _qy, ux, uy, _s, _cp = r166.atlas.geometry(
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


def typed_shadow(
    row: ShadowRow,
    records: list[r166.ge.RootRecord],
    unresolved: list[r166.ge.RootRecord],
) -> tuple[bool, str]:
    if len(unresolved) != 1:
        return False, ""
    candidate = unresolved[0]
    ds, _low, _high, full_graph = p_face_data(row, candidate)
    if ds == 0 or not full_graph:
        return False, ""
    if not target_first_on_positive(candidate, records):
        return False, ""
    negative = remove_target_disposition(
        row, records, candidate.target_id
    )
    if negative is None or not negative.startswith("EXCLUDED"):
        return False, ""
    if candidate.target_id == r166.FROZEN_OWNER:
        chart = shadow_positive_chart(row, candidate)
        if chart is None or chart == r166.FROZEN_CHART:
            return False, ""
        positive = graph = "EXCLUDED_OUTGOING_CHART_MISMATCH"
    else:
        positive = graph = "EXCLUDED_UNIQUE_FIRST_OWNER_MISMATCH"
    return True, (
        f"NEGATIVE={negative}|GRAPH={graph}|POSITIVE={positive}"
    )


def refined_delta_record(
    candidate: r166.ge.RootRecord,
    low: arb,
    high: arb,
    derivative_sign: int,
) -> r166.ge.RootRecord:
    delta = (
        r166.ge.arb_hull(low.lower(), high.upper())
        if derivative_sign > 0
        else r166.ge.arb_hull(high.lower(), low.upper())
    )
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
    require(bool(delta > 0), "shadow same sign delta")
    radical = delta.sqrt()
    near = candidate.ell - radical
    far = candidate.ell + radical
    classification = (
        "intersection_behind"
        if bool(far < 0)
        else (
            "strict_future_root"
            if bool(near > 0)
            else "unresolved_root_sign"
        )
    )
    return r166.ge.RootRecord(
        candidate.target_id,
        classification,
        candidate.ell,
        delta,
        near,
        far,
        candidate.transverse,
    )


def same_sign_shadow(
    row: ShadowRow,
    records: list[r166.ge.RootRecord],
    candidate: r166.ge.RootRecord,
    derivative_sign: int,
    low: arb,
    high: arb,
) -> tuple[str | None, str]:
    enhanced = refined_delta_record(
        candidate, low, high, derivative_sign
    )
    leaf = r166.classify_from_records(
        row.chart_id,
        row.box,
        [
            enhanced if record.target_id == candidate.target_id else record
            for record in records
        ],
    )
    if leaf.classification == "no_future_root":
        return "EXCLUDED", "NO_INHERITED_FUTURE_ROOT"
    if leaf.classification != "unique_first":
        return None, f"ENHANCED_{leaf.classification}"
    if leaf.owner_target != r166.FROZEN_OWNER:
        return "EXCLUDED", "UNIQUE_FIRST_OWNER_MISMATCH"
    if candidate.target_id == r166.FROZEN_OWNER:
        chart = shadow_positive_chart(row, enhanced)
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
    kind, _classes, _depths = h_shadow(row)
    return kind, "FOLLOWUP_H_PARTITION"


@dataclass(frozen=True)
class CompactBox:
    t0: Q
    t1: Q
    r0: Q
    r1: Q
    s0: Q
    s1: Q
    depth: int


def compact_geometry(
    chart_id: str,
    p_sign: int,
    box: CompactBox,
) -> tuple[arb, arb, arb, arb, arb, arb]:
    t = r166.base.arb_interval(box.t0, box.t1)
    r = r166.base.arb_interval(box.r0, box.r1)
    s = r166.base.arb_interval(box.s0, box.s1)
    rt = r166.ge.sqrt_one_minus_square(box.t0, box.t1)
    cell = chart_id.split(":")[1]
    require(cell in {"N", "S"}, "shadow compact chart")
    nx, ny = t, rt if cell == "N" else -rt
    k = Q(1023, 262144)
    compact_q = r166.base.arbq(k).sqrt() * r
    p_low = r166.base.arbq(1 - k * box.r1 * box.r1).sqrt()
    p_high = r166.base.arbq(1 - k * box.r0 * box.r0).sqrt()
    p_abs = r166.ge.arb_hull(p_low.lower(), p_high.upper())
    p = p_abs if p_sign > 0 else -p_abs
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


def compact_classify(
    chart_id: str,
    p_sign: int,
    box: CompactBox,
    targets: tuple[str, ...],
) -> tuple[str, tuple[str, ...]]:
    geometry = compact_geometry(chart_id, p_sign, box)
    records = [
        r166.root_record_from_geometry(geometry, target_id)
        for target_id in targets
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
            qx, qy, ux, uy, s, _q = geometry
            target = r166._target_cache[candidate.target_id]
            cx, cy = r166.base.target_center(target, s)
            radius = r166.base.arbq(
                r166.base.RADIUS[target.obstacle]
            )
            nx = (qx + candidate.near * ux - cx) / radius
            ny = (qy + candidate.near * uy - cy) / radius
            margins = {
                "E": (nx - ny, nx + ny),
                "W": (-nx - ny, -nx + ny),
                "N": (ny - nx, ny + nx),
                "S": (-ny - nx, -ny + nx),
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


def compact_split(box: CompactBox) -> tuple[CompactBox, CompactBox]:
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
            CompactBox(
                box.t0, middle, box.r0, box.r1,
                box.s0, box.s1, depth,
            ),
            CompactBox(
                middle, box.t1, box.r0, box.r1,
                box.s0, box.s1, depth,
            ),
        )
    if axis == 1:
        middle = (box.r0 + box.r1) / 2
        return (
            CompactBox(
                box.t0, box.t1, box.r0, middle,
                box.s0, box.s1, depth,
            ),
            CompactBox(
                box.t0, box.t1, middle, box.r1,
                box.s0, box.s1, depth,
            ),
        )
    middle = (box.s0 + box.s1) / 2
    return (
        CompactBox(
            box.t0, box.t1, box.r0, box.r1,
            box.s0, middle, depth,
        ),
        CompactBox(
            box.t0, box.t1, box.r0, box.r1,
            middle, box.s1, depth,
        ),
    )


def compact_profile(row: ShadowRow) -> dict[str, Any]:
    p_sign = 1 if row.box.p1 == 1 else -1
    root = CompactBox(
        row.box.t0,
        row.box.t1,
        Q(0),
        Q(1),
        row.box.s0,
        row.box.s1,
        0,
    )
    face = CompactBox(
        root.t0, root.t1, Q(0), Q(0),
        root.s0, root.s1, 0,
    )
    face_class, _active = compact_classify(
        row.chart_id, p_sign, face, row.active_targets
    )
    pending = [(root, row.active_targets)]
    terminal: Counter[str] = Counter()
    depths: Counter[int] = Counter()
    volumes: dict[str, Q] = defaultdict(Q)
    residual: Counter[str] = Counter()
    residual_volume = Q(0)
    coarse_terminal: set[str] = set()
    while pending:
        box, targets = pending.pop()
        classification, active = compact_classify(
            row.chart_id, p_sign, box, targets
        )
        if not classification.startswith("UNRESOLVED"):
            terminal[classification] += 1
            depths[box.depth] += 1
            volumes[classification] += Q(1, 2 ** box.depth)
            coarse_terminal.add(coarse(classification))
        elif box.depth < 8:
            inherited = active or targets
            pending.extend(
                (child, inherited) for child in compact_split(box)
            )
        else:
            residual[classification] += 1
            residual_volume += Q(1, 2 ** box.depth)
    require(
        sum(volumes.values(), Q(0)) + residual_volume == 1,
        "shadow compact mass",
    )
    if residual:
        parent_kind = None
    elif coarse_terminal == {"EXCLUDED"}:
        parent_kind = "EXCLUDED"
    elif coarse_terminal == {"LIVE"}:
        parent_kind = "LIVE"
    else:
        parent_kind = "MIXED"
    return {
        "face": face_class,
        "terminal": terminal,
        "depths": depths,
        "volumes": volumes,
        "residual": residual,
        "residual_volume": residual_volume,
        "parent_kind": parent_kind,
    }


def shadow_audit() -> dict[str, Any]:
    (
        frontier,
        prior_counts,
        prior_volume,
        origin_kinds,
        all_origins,
        workload,
    ) = replay_tree()
    frontier_by_origin: Counter[str] = Counter(
        row.origin_key for row in frontier
    )
    category_keys: dict[str, list[str]] = defaultdict(list)
    residual_keys: dict[str, list[str]] = defaultdict(list)
    h_classes: Counter[str] = Counter()
    h_depths: Counter[int] = Counter()
    tangency_witnesses: Counter[str] = Counter()
    monotone_witnesses: Counter[str] = Counter()
    compact_face: Counter[str] = Counter()
    compact_terminal: Counter[str] = Counter()
    compact_depths: Counter[int] = Counter()
    compact_volumes: dict[str, Q] = defaultdict(Q)
    compact_residual: Counter[str] = Counter()
    compact_residual_volume = Q(0)
    compact_parents: Counter[str] = Counter()

    for row in frontier:
        if row.failure == "OUTGOING_CHART_SEAM_OVERWRAP":
            kind, classes, depths = h_shadow(row)
            require(kind is not None, "shadow seam closure")
            category_keys[kind].append(row.key)
            h_classes.update(classes)
            h_depths.update(depths)
            continue
        if row.failure in {
            "TYPED_FROZEN_OWNER_TANGENCY_GRAPH_COLLAR",
            "TYPED_OWNER_MISMATCH_TANGENCY_GRAPH_COLLAR",
        }:
            records, unresolved = active_records(row)
            closed, witness = typed_shadow(
                row, records, unresolved
            )
            if closed:
                category_keys["EXCLUDED"].append(row.key)
                tangency_witnesses[witness] += 1
            else:
                residual_keys[
                    "TYPED_TANGENCY_PLUS_OUTGOING_SEAM_DOUBLE_GRAPH"
                ].append(row.key)
            continue
        if row.failure == "UNTYPED_DISCRIMINANT_COLLAR":
            records, unresolved = active_records(row)
            if len(unresolved) > 1:
                residual_keys[
                    "MULTI_DISCRIMINANT_2_TO_5_TARGETS"
                ].append(row.key)
                continue
            require(len(unresolved) == 1, "shadow delta count")
            candidate = unresolved[0]
            ds, low, high, full_graph = p_face_data(row, candidate)
            same_sign = (
                ds != 0
                and strict_sign(low) != 0
                and strict_sign(low) == strict_sign(high)
            )
            if same_sign:
                kind, witness = same_sign_shadow(
                    row, records, candidate, ds, low, high
                )
                require(kind is not None, "shadow monotone closure")
                category_keys[kind].append(row.key)
                monotone_witnesses[witness] += 1
            elif full_graph:
                residual_keys[
                    "FULL_P_DISCRIMINANT_GRAPH_REQUIRES_FIRST_ROOT_EQUALITY"
                ].append(row.key)
            else:
                residual_keys[
                    "CLIPPED_OR_FACE_OVERWRAP_SINGLE_DISCRIMINANT_GRAPH"
                ].append(row.key)
            continue
        require(
            row.failure == "SOURCE_GRAZING_ENDPOINT_COLLAR",
            "shadow dispatch",
        )
        profile = compact_profile(row)
        compact_face[profile["face"]] += 1
        compact_terminal.update(profile["terminal"])
        compact_depths.update(profile["depths"])
        for key, value in profile["volumes"].items():
            compact_volumes[key] += value
        compact_residual.update(profile["residual"])
        compact_residual_volume += profile["residual_volume"]
        kind = profile["parent_kind"]
        if kind is None:
            compact_parents["RESIDUAL"] += 1
            residual_keys[
                "SOURCE_GRAZING_COMPACT_Q_PARENT_RESIDUAL"
            ].append(row.key)
        else:
            require(kind in {"EXCLUDED", "LIVE"}, "shadow compact kind")
            compact_parents[kind] += 1
            category_keys[kind].append(row.key)

    for values in category_keys.values():
        values.sort()
    for values in residual_keys.values():
        values.sort()
    row_by_key = {row.key: row for row in frontier}
    closed_by_origin: Counter[str] = Counter()
    for kind, keys in category_keys.items():
        for key in keys:
            origin = row_by_key[key].origin_key
            closed_by_origin[origin] += 1
            origin_kinds[origin].add(kind)
    fully = {
        origin for origin in all_origins
        if closed_by_origin[origin] == frontier_by_origin[origin]
    }
    prior_complete = {
        origin for origin in all_origins
        if frontier_by_origin[origin] == 0
    }
    origin_categories: dict[str, list[str]] = defaultdict(list)
    for origin in sorted(fully):
        kinds = origin_kinds[origin]
        category = (
            "WHOLE_ORIGIN_PARENT_EXCLUDED"
            if kinds == {"EXCLUDED"}
            else (
                "WHOLE_ORIGIN_PARENT_LIVE"
                if kinds == {"LIVE"}
                else "RESOLVED_MIXED_OR_ANALYTIC_PARTITION"
            )
        )
        origin_categories[category].append(origin)

    frontier_keys = sorted(row_by_key)
    closed_keys = sorted(
        key for values in category_keys.values() for key in values
    )
    residual_all = sorted(
        key for values in residual_keys.values() for key in values
    )
    return {
        "workload": workload,
        "frontier_failure": dict(
            sorted(Counter(row.failure for row in frontier).items())
        ),
        "prior_terminal_counts": dict(sorted(prior_counts.items())),
        "prior_terminal_volume": {
            key: str(value)
            for key, value in sorted(prior_volume.items())
        },
        "category_counts": {
            key: len(values)
            for key, values in sorted(category_keys.items())
        },
        "residual_counts": {
            key: len(values)
            for key, values in sorted(residual_keys.items())
        },
        "h_classes": dict(sorted(h_classes.items())),
        "h_depths": {
            str(key): value for key, value in sorted(h_depths.items())
        },
        "tangency_witnesses": dict(sorted(tangency_witnesses.items())),
        "monotone_witnesses": dict(sorted(monotone_witnesses.items())),
        "compact_face": dict(sorted(compact_face.items())),
        "compact_terminal": dict(sorted(compact_terminal.items())),
        "compact_depths": {
            str(key): value
            for key, value in sorted(compact_depths.items())
        },
        "compact_volumes": {
            key: str(value)
            for key, value in sorted(compact_volumes.items())
        },
        "compact_residual": dict(sorted(compact_residual.items())),
        "compact_residual_volume": str(compact_residual_volume),
        "compact_parents": dict(sorted(compact_parents.items())),
        "origin_counts": {
            "prior_complete": len(prior_complete),
            "newly_complete": len(fully - prior_complete),
            "fully_complete": len(fully),
            "still_incomplete": 2616 - len(fully),
            "by_disposition": {
                key: len(values)
                for key, values in sorted(origin_categories.items())
            },
        },
        "key_digests": {
            "all_frontier": digest(frontier_keys),
            "closed": digest(closed_keys),
            "residual": digest(residual_all),
            "closed_by_category": {
                key: digest(values)
                for key, values in sorted(category_keys.items())
            },
            "residual_by_category": {
                key: digest(values)
                for key, values in sorted(residual_keys.items())
            },
            "origin_by_category": {
                key: digest(values)
                for key, values in sorted(origin_categories.items())
            },
        },
    }


def verify_projection(result: dict[str, Any], audit: dict[str, Any]) -> None:
    require(result["verdict"] == "PARTIAL", "verdict")
    require(
        result["status"]
        == (
            "PARTIAL_BOUNDED_GRAPH_CELL_EXPLORATION_ONLY__"
            "NO_FORMAL_CORE_GATE_CREDIT__ROUND168_LEDGER_UNCHANGED"
        ),
        "status",
    )
    scope = result["scope"]
    require(
        scope["ambient_parameter_dimension"] == 3
        and scope["graph_dimension"] == 2
        and scope["graph_typing_is_not_whole_record_credit"]
        and scope["bounded_exploratory_only"]
        and scope["not_formal_core_gate_credit"]
        and scope["not_D02_closure"],
        "scope",
    )
    replay = result["round166_full_tree_replay"]
    require(
        replay["evaluated_box_count"]
        == audit["workload"]["evaluated_box_count"]
        and replay["evaluated_target_record_count"]
        == audit["workload"]["evaluated_target_record_count"]
        and replay["prior_terminal_child_records_by_disposition"]
        == audit["prior_terminal_counts"]
        and replay[
            "prior_terminal_baseline_parent_equivalent_by_disposition"
        ] == audit["prior_terminal_volume"]
        and replay["depth14_frontier_child_record_count"] == 56780,
        "tree replay",
    )
    blocks = result["bounded_blocks"]
    h = blocks["outgoing_H_seams"]
    require(
        h["terminal_H_cell_count_by_class"] == audit["h_classes"]
        and h["terminal_H_cell_count_by_extra_depth"]
        == audit["h_depths"]
        and h["whole_parent_excluded"] == 2550
        and h["whole_parent_live"] == 2180
        and h["typed_or_mixed_analytic_partition"] == 2780,
        "H block",
    )
    tangency = blocks["typed_tangency_three_stratum_closure"]
    require(
        tangency["closed_all_three_strata_excluded"]
        == sum(audit["tangency_witnesses"].values())
        == 1000
        and tangency["residual_double_graph_arrangement"] == 220
        and tangency["whole_child_exclusion_requires_all_three_excluded"],
        "tangency block",
    )
    monotone = blocks["same_sign_monotone_discriminant"]
    require(
        monotone["witness_counts"] == audit["monotone_witnesses"]
        and sum(audit["monotone_witnesses"].values()) == 4076
        and monotone["whole_parent_excluded"] == 2598
        and monotone["whole_parent_live"] == 1358
        and monotone["typed_or_mixed_H_partition"] == 120
        and monotone["residual"] == 0,
        "monotone block",
    )
    grazing = blocks["source_grazing_compact_q_profile"]
    require(
        grazing["grazing_face_classification"]
        == audit["compact_face"]
        and grazing["q_terminal_cell_count_by_disposition"]
        == audit["compact_terminal"]
        and grazing["q_terminal_cell_count_by_extra_depth"]
        == audit["compact_depths"]
        and grazing[
            "q_terminal_depth14_parent_equivalent_by_disposition"
        ] == audit["compact_volumes"]
        and grazing["q_residual_cell_count_by_type"]
        == audit["compact_residual"]
        and grazing["q_residual_depth14_parent_equivalent"]
        == audit["compact_residual_volume"]
        and grazing["whole_depth14_parent_records"]
        == {
            "excluded": audit["compact_parents"]["EXCLUDED"],
            "live": audit["compact_parents"]["LIVE"],
            "residual": audit["compact_parents"]["RESIDUAL"],
        }
        and grazing["grazing_face_dimension"] == 2
        and grazing["interior_dimension"] == 3
        and grazing["two_dimensional_face_not_counted_as_volume"],
        "grazing block",
    )
    ledgers = result["three_noninterchangeable_ledgers"]
    children = ledgers["depth14_terminal_child_records"]
    require(
        children
        == {
            "identity": "6250+3590+2900+44040=56780",
            "input": 56780,
            "residual": 44040,
            "semantically_closed": 12740,
            "typed_or_mixed_analytic_partition": 2900,
            "whole_excluded": 6250,
            "whole_live": 3590,
        },
        "child ledger",
    )
    volume = ledgers["rational_baseline_parent_equivalent_volume"]
    require(
        volume["Round170_excluded"] == "917955/8192"
        and volume["Round170_live"] == "506727/8192"
        and volume["Round170_mixed_analytic"] == "725/16"
        and volume["Round170_classified"] == "897941/4096"
        and volume["Round170_residual"] == "2735979/4096",
        "volume ledger",
    )
    origins = ledgers["Round168_original_depth8_parent_records"]
    expected_origins = audit["origin_counts"]
    require(
        origins["fully_replaced_before_Round170_bounded_blocks"]
        == expected_origins["prior_complete"]
        and origins["newly_fully_replaced_by_Round170_bounded_blocks"]
        == expected_origins["newly_complete"]
        and origins[
            "fully_replaced_total_after_verified_depth14_replay"
        ] == expected_origins["fully_complete"]
        and origins["still_not_fully_replaced"]
        == expected_origins["still_incomplete"]
        and origins["fully_replaced_by_disposition"]
        == expected_origins["by_disposition"]
        and origins["Round168_integer_ledger_mutated"] is False
        and origins["official_Round168_integer_credit_delta"] == 0
        and origins["whole_parent_integer_credit_claimed"] == 0
        and origins[
            "child_count_never_added_directly_to_original_parent_ledger"
        ],
        "origin ledger",
    )
    require(
        result["residual"]["depth14_record_count_by_hard_type"]
        == audit["residual_counts"],
        "residual counts",
    )
    keys = result["key_digests"]
    require(
        keys["all_frontier_leaf_keys_sha256"]
        == audit["key_digests"]["all_frontier"]
        and keys["closed_frontier_leaf_keys_sha256"]
        == audit["key_digests"]["closed"]
        and keys["residual_frontier_leaf_keys_sha256"]
        == audit["key_digests"]["residual"]
        and keys["closed_by_category_sha256"]
        == audit["key_digests"]["closed_by_category"]
        and keys["residual_by_category_sha256"]
        == audit["key_digests"]["residual_by_category"]
        and keys["fully_replaced_origin_by_category_sha256"]
        == audit["key_digests"]["origin_by_category"],
        "key digests",
    )
    nonpromotion = result["strict_nonpromotion"]
    require(
        nonpromotion["Round168_whole_record_excluded"] == 73162
        and nonpromotion["Round168_conservative_live"] == 3670
        and nonpromotion["Round168_ledger_unchanged"]
        and nonpromotion["bounded_counts_are_not_official_ledger_credit"]
        and nonpromotion[
            "volume_or_child_record_to_whole_parent_integer_conversion"
        ] == "FORBIDDEN"
        and nonpromotion["D02"] == "BLOCKED"
        and nonpromotion["CM2"] == "NO-GO_FOR_CLAIM",
        "nonpromotion",
    )
    require(
        result["provenance"]["producer_sha256"] == PRODUCER_SHA256
        and hashlib.sha256(
            (
                HERE
                / "cm2_round170_bounded_dimension_safe_graph_cells.py"
            ).read_bytes()
        ).hexdigest()
        == PRODUCER_SHA256,
        "producer identity",
    )


def verify_document(
    document: dict[str, Any],
    audit: dict[str, Any],
) -> None:
    require(document["schema"] == CERTIFICATE_SCHEMA, "certificate schema")
    require(
        digest(document["result"]) == document["result_sha256"],
        "certificate digest",
    )
    require(
        document["result_sha256"]
        == EXPECTED_CERTIFICATE_RESULT_SHA256,
        "full canonical expected-result equality",
    )
    verify_projection(document["result"], audit)


def resign(document: dict[str, Any]) -> dict[str, Any]:
    document["result_sha256"] = digest(document["result"])
    return document


def semantic_attacks(
    certificate: dict[str, Any],
    audit: dict[str, Any],
) -> tuple[int, int]:
    paths_and_values = [
        (("result", "verdict"), "VALIDATED"),
        (("result", "status"), "CERTIFIED"),
        (("result", "scope", "graph_dimension"), 3),
        (
            (
                "result",
                "scope",
                "graph_typing_is_not_whole_record_credit",
            ),
            False,
        ),
        (
            (
                "result",
                "three_noninterchangeable_ledgers",
                "depth14_terminal_child_records",
                "whole_excluded",
            ),
            6251,
        ),
        (
            (
                "result",
                "three_noninterchangeable_ledgers",
                "rational_baseline_parent_equivalent_volume",
                "Round170_excluded",
            ),
            "918000/8192",
        ),
        (
            (
                "result",
                "three_noninterchangeable_ledgers",
                "Round168_original_depth8_parent_records",
                "official_Round168_integer_credit_delta",
            ),
            6250,
        ),
        (
            (
                "result",
                "three_noninterchangeable_ledgers",
                "Round168_original_depth8_parent_records",
                "whole_parent_integer_credit_claimed",
            ),
            454,
        ),
        (
            (
                "result",
                "bounded_blocks",
                "outgoing_H_seams",
                "whole_parent_excluded",
            ),
            2551,
        ),
        (
            (
                "result",
                "bounded_blocks",
                "typed_tangency_three_stratum_closure",
                "closed_all_three_strata_excluded",
            ),
            1220,
        ),
        (
            (
                "result",
                "bounded_blocks",
                "typed_tangency_three_stratum_closure",
                "whole_child_exclusion_requires_all_three_excluded",
            ),
            False,
        ),
        (
            (
                "result",
                "bounded_blocks",
                "same_sign_monotone_discriminant",
                "residual",
            ),
            1,
        ),
        (
            (
                "result",
                "bounded_blocks",
                "source_grazing_compact_q_profile",
                "grazing_face_dimension",
            ),
            3,
        ),
        (
            (
                "result",
                "bounded_blocks",
                "source_grazing_compact_q_profile",
                "two_dimensional_face_not_counted_as_volume",
            ),
            False,
        ),
        (
            (
                "result",
                "residual",
                "depth14_record_count_by_hard_type",
                "MULTI_DISCRIMINANT_2_TO_5_TARGETS",
            ),
            0,
        ),
        (
            (
                "result",
                "key_digests",
                "closed_frontier_leaf_keys_sha256",
            ),
            "0" * 64,
        ),
        (
            ("result", "strict_nonpromotion", "Round168_ledger_unchanged"),
            False,
        ),
        (
            (
                "result",
                "strict_nonpromotion",
                "volume_or_child_record_to_whole_parent_integer_conversion",
            ),
            "ALLOWED",
        ),
        (("result", "strict_nonpromotion", "D02"), "READY"),
        (("result", "strict_nonpromotion", "CM2"), "GO"),
    ]
    rejected = 0
    for path, value in paths_and_values:
        mutated = copy.deepcopy(certificate)
        cursor: Any = mutated
        for key in path[:-1]:
            cursor = cursor[key]
        cursor[path[-1]] = value
        resign(mutated)
        try:
            verify_document(mutated, audit)
        except Exception:
            rejected += 1
    return rejected, len(paths_and_values)


def json_attacks() -> tuple[int, int]:
    attacks = [
        b'\xef\xbb\xbf{"schema":"x"}',
        b'{"schema":"x","schema":"y"}',
        b'{"x":NaN}',
        b'{"x":Infinity}',
        b'{"x":"\\ud800"}',
        b'{"x":"a\\u0000b"}',
        b'{"x":1}\x00',
    ]
    rejected = 0
    for index, raw in enumerate(attacks):
        try:
            strict_load_bytes(raw, f"attack-{index}")
        except Exception:
            rejected += 1
    return rejected, len(attacks)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certificate", type=Path, default=CERTIFICATE)
    parser.add_argument("--output", type=Path, default=OUTPUT)
    args = parser.parse_args()
    ctx.prec = 192
    check_verifier_chain()
    certificate = strict_load(args.certificate)
    audit = shadow_audit()
    verify_document(certificate, audit)
    semantic_rejected, semantic_total = semantic_attacks(
        certificate, audit
    )
    json_rejected, json_total = json_attacks()
    require(
        semantic_rejected == semantic_total,
        "semantic attacks",
    )
    require(json_rejected == json_total, "JSON attacks")
    result = {
        "status": "PASS_PARTIAL_BOUNDED_EXPLORATION_ONLY",
        "verdict": "PARTIAL",
        "certificate_result_sha256":
            certificate["result_sha256"],
        "certificate_file_sha256":
            hashlib.sha256(args.certificate.read_bytes()).hexdigest(),
        "producer_file_sha256": PRODUCER_SHA256,
        "verification_contract": {
            "imports_Round170_producer": False,
            "imports_pinned_Round165_and_Round166_producer_modules": True,
            "algorithmically_independent_of_Round166_tree_code": False,
            "Round166_depth14_tree_fully_replayed_relative_to_pins": True,
            "Round170_claimed_geometry_recomputed": True,
            "full_canonical_expected_result_equality": True,
            "audit_projection_sha256": digest(audit),
        },
        "attack_suite": {
            "resigned_semantic_attacks_rejected":
                semantic_rejected,
            "resigned_semantic_attacks_total":
                semantic_total,
            "strict_JSON_attacks_rejected": json_rejected,
            "strict_JSON_attacks_total": json_total,
        },
        "nonpromotion_enforced": {
            "Round168_integer_ledger_delta": 0,
            "child_or_volume_to_whole_parent_integer_fold_rejected": True,
            "D02": "BLOCKED",
            "CM2": "NO-GO_FOR_CLAIM",
        },
    }
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
