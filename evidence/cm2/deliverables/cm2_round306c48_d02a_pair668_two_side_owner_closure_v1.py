#!/usr/bin/env python3
"""C48 pair-668 two-side route, strict-margin, and owner-closure candidate.

This successor is deliberately narrow.  It replays the deterministic first
pair-668 OWNER_PREREQUISITE task selected by C46/C47, replaces its C41 root by
the exact prefix-free relative frontier ``0, 10, 11``, and routes both the
representative and reflected physical cells independently.

The codimension owner ledger is not local-sibling evidence.  It scans every
C41 ambient row, materializes both physical occurrences, removes the two
selected predecessor occurrences, inserts the six C48 leaves, atomizes every
target face against the full overlay, and recomputes complete incident sets
and unique lexicographic semantic-path owners.  Corners and T-junctions are
separate rows with four-quadrant germ checks.

Even a closed result is only a producer candidate.  This file has no runtime
write, pointer, receipt, seal, installer, or canonical-status code path, and
formal credit remains zero until an independent C48 verifier passes.

Normal use (canonical JSON on stdout only)::

  .cm2-runtime/python-flint-0.9.0/bin/python -I -B THIS.py --self-test
  .cm2-runtime/python-flint-0.9.0/bin/python -I -B THIS.py --materialize
"""

from __future__ import annotations

import argparse
import copy
from fractions import Fraction as Q
import hashlib
import importlib
import json
from pathlib import Path
import re
import sys
from typing import Any, Iterable


SELF = Path(__file__).absolute()
ROOT = SELF.parent.parent
DELIVERABLES = ROOT / "deliverables"
RUNTIME = ROOT / ".cm2-runtime"

SCHEMA = "cm2.round306c48.d02-a-pair668-two-side-owner-closure.v1"
LEAF_SCHEMA = SCHEMA + ".physical-leaf"
MARGIN_SCHEMA = SCHEMA + ".strict-terminal-margin"
FACE_SCHEMA = SCHEMA + ".shared-face-atom-owner"
CORNER_SCHEMA = SCHEMA + ".shared-corner-owner"

C46_NAME = "cm2_round306c46_d02a_general_adaptive_lower_strata_closure_engine_v1"
C41_NAME = "cm2_round306c41_d02_lower_strata_depth3_closure_v1"
C46_SOURCE = DELIVERABLES / (C46_NAME + ".py")
C41_SOURCE = DELIVERABLES / (C41_NAME + ".py")
C47_SOURCE = DELIVERABLES / (
    "cm2_round306c47_d02a_pair668_exact_route_adaptive_feasibility_spike_v1.py"
)
C47_REPORT = DELIVERABLES / (
    "cm2_round306c47_d02a_pair668_exact_route_adaptive_feasibility_"
    "spike_report_v1.md"
)

C46_SOURCE_SHA256 = "365432e96f2c287ef3c5497b7d15e01a80775f52d8cf5b71810d6f4c0e4442ea"
C46_PLAN_OBJECT_SHA256 = "7d004f59282dee21a28db0cd0b727a9045f4befce207c96be4efb07d1399c9bf"
C41_SOURCE_SHA256 = "3fbf6cec247903d6e6ba147d4d06e912638b1472b74adc8311323c554e6e5bde"
C47_SOURCE_SHA256 = "28c7eb805729f4ab8d5adaf5fac211394616877b5e08c39bd9f288c1f7640a1f"
C47_REPORT_SHA256 = "e389886d6d77e7d3ca70c821a8985bf7204458b08ddd8a1cda957c9def2b6aed"
C47_RESULT_OBJECT_SHA256 = "c57bc2711dbc7dad13178643b26f5722d48db703598d3238bfd98aa254e4f9f4"
C47_CHECKPOINT_OBJECT_SHA256 = "6ed628697caf0feb81a0dc5428e1a27bf472c2ec59496556dcffa60ba5ddba5e"

C41_TOKEN = "c41-lower-strata-depth3-20260811T023804Z-f997365c91559599"
C41_DIR = RUNTIME / "candidates" / C41_TOKEN
C41_OBJECT_SHA256 = "b7e47a4ca9d6f4bb1fee10e78877850d5070f6d3c2b06bb0234fbabdaa2b7b24"
C41_RESULT_FILE_SHA256 = "73fde0eee7eb06bb0f144ea98880c72bfea36e10db696731ae72393cd9b0a50f"
C41_ROOT_MANIFEST_FILE_SHA256 = "86e10532d63269cd0fdd58d541b1984522e9718f4613a5dc83211fe84eb258ba"
C41_AMBIENT_LEDGER_FILE_SHA256 = "ea75405c8f8ba53c795c64a228aea75f9587017d93aa1cd08e73c287931e78a8"
C42_SEAL_OBJECT_SHA256 = "b321552768a6aeae6c1d229e52b61ca0b4420314234e02e98366153d4156d460"

PAIR = 668
PAIR_TASK_COUNT = 43
TASK_BINDING = "64400932860d6f224a90204e56a5614bf982eb3a1b87f37f04b86ba112a3ff9f"
ROOT_PATH = "010111011"
AMBIENT_ID = "c41-ambient:a828b4c95611e3e12ab8b3131f19f801ce8e1f1541106010ea94f34ba981a351"
PRIMARY_ID = "c41-c2-outer:4037ee276cf83fdf894f563b3967beba1dc5889764f951a8b8d2c4441b3258e4"
RELATIVE_LEAVES = ("0", "10", "11")
EXPECTED_C41_AMBIENT_COUNT = 91_879
EXPECTED_BASELINE_PHYSICAL_OCCURRENCE_COUNT = 183_758
EXPECTED_OVERLAY_PHYSICAL_OCCURRENCE_COUNT = 183_762
EXPECTED_EXACT_RATIONAL_BASELINE_OCCURRENCE_COUNT = 183_700
SHARD_INDEX = 2
SHARD_ID = "c46-d02a-shard:538ecddfbdd47c229c2e6ed2c62285bcea0b93a101832eef5ea849656c34dd28"
SHARD_TASK_COUNT = 514
SHARD_BINDING_SEQUENCE_SHA256 = "1f41885b9f01cf9c086e5d547cd4878e3ad7244e8a30437611aaffc5a776b340"
GENESIS_CHECKPOINT_OBJECT_SHA256 = "8c0029650c5dfd460e4ed721ded69e004220522bcf2c51d70859547430e018b7"

HEX64 = re.compile(r"[0-9a-f]{64}\Z")


class Rejected(RuntimeError):
    """Fail-closed predecessor, route, margin, or incidence rejection."""


def need(condition: bool, label: str) -> None:
    if type(condition) is not bool or not condition:
        raise Rejected(label)


def canonical(value: Any) -> bytes:
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=True,
        allow_nan=False,
    ).encode("ascii")


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def sequence_digest(values: Iterable[str]) -> str:
    state = hashlib.sha256()
    for value in values:
        state.update(value.encode("ascii") + b"\n")
    return state.hexdigest()


def file_sha256(path: Path) -> str:
    state = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            state.update(block)
    return state.hexdigest()


def qstr(value: Q) -> str:
    return str(value)


def qpair(values: list[str]) -> tuple[Q, Q]:
    need(type(values) is list and len(values) == 2, "rational interval shape")
    result = (Q(values[0]), Q(values[1]))
    need(result[0] <= result[1], "ordered rational interval")
    return result


def load_modules() -> tuple[Any, Any]:
    pins = {
        C46_SOURCE: C46_SOURCE_SHA256,
        C41_SOURCE: C41_SOURCE_SHA256,
        C47_SOURCE: C47_SOURCE_SHA256,
        C47_REPORT: C47_REPORT_SHA256,
        C41_DIR / "result.json": C41_RESULT_FILE_SHA256,
        C41_DIR / "root_manifest.sha256": C41_ROOT_MANIFEST_FILE_SHA256,
        C41_DIR / "routed_ambient_cells.jsonl.gz": C41_AMBIENT_LEDGER_FILE_SHA256,
    }
    for path, expected in pins.items():
        need(file_sha256(path) == expected, "frozen file SHA-256:" + str(path))
    sys.path.insert(0, str(DELIVERABLES))
    try:
        c46 = importlib.import_module(C46_NAME)
        c41 = importlib.import_module(C41_NAME)
    finally:
        if sys.path and sys.path[0] == str(DELIVERABLES):
            sys.path.pop(0)
    need(Path(c46.__file__).absolute() == C46_SOURCE, "C46 import path")
    need(Path(c41.__file__).absolute() == C41_SOURCE, "C41 import path")
    return c46, c41


def selected_inputs(c46: Any, c41: Any) -> dict[str, Any]:
    plan, tasks, _shards = c46.build_read_only_plan(64)
    need(plan["plan_object_sha256"] == C46_PLAN_OBJECT_SHA256, "C46 plan pin")
    need(
        plan["authority_baseline"]["authority_seal_object_sha256"]
        == C42_SEAL_OBJECT_SHA256,
        "C42 authority baseline",
    )
    group = sorted(
        [row for row in tasks if row["pair_index"] == PAIR
         and row["queue"]["priority_class"] == "OWNER_PREREQUISITE"],
        key=lambda row: (row["descendant_path"], row["primary_outer_id"]),
    )
    need(len(group) == PAIR_TASK_COUNT, "pair-668 task census")
    selected = group[0]
    need(
        selected["task_binding_sha256"] == TASK_BINDING
        and selected["descendant_path"] == ROOT_PATH
        and selected["ambient_cell_id"] == AMBIENT_ID
        and selected["primary_outer_id"] == PRIMARY_ID,
        "deterministic task pins",
    )
    result = c41.strict_json(C41_DIR / "result.json")
    c41.validate_object(result, C41_OBJECT_SHA256, "C41 candidate")
    descriptor = result["ledgers"]["routed_ambient_cells"]
    need(descriptor["row_count"] == EXPECTED_C41_AMBIENT_COUNT,
         "C41 ambient descriptor census")
    ambient = None
    source = None
    source_ordinal = None
    for row in c41.iter_ledger(C41_DIR, descriptor):
        if row["c41_ambient_cell_id"] == AMBIENT_ID:
            need(ambient is None, "selected ambient uniqueness")
            ambient = row
    need(ambient is not None, "selected ambient present")
    need(
        ambient["row_sha256"] == selected["ambient_row_sha256"]
        and ambient["pair_index"] == PAIR and ambient["path"] == ROOT_PATH,
        "selected ambient binding",
    )
    c40_dir = ROOT / result["C40_authority"]["path"]
    c40_audit = ROOT / result["C40_authority"]["independent_audit_path"]
    c40_result = c41.strict_json(c40_dir / "result.json")
    for ordinal, row in enumerate(c41.iter_ledger(
            c40_dir, c40_result["ledgers"]["routed_leaf_cells"])):
        if row["c40_leaf_id"] == ambient["c40_source_leaf_id"]:
            need(source is None, "C40 source uniqueness")
            source, source_ordinal = row, ordinal
    need(source is not None and type(source_ordinal) is int, "C40 source present")
    context = c41.load_context(c40_dir, c40_audit, formal=True)
    config = c41.decode_worker_config(context["config"])
    task = c41.task_for_row(source_ordinal, source, context)
    return {
        "plan": plan, "selected": selected, "group": group,
        "C41_result": result, "ambient": ambient,
        "C40_dir": c40_dir, "C40_result": c40_result,
        "source": source, "source_ordinal": source_ordinal,
        "context": context, "config": config, "task": task,
    }


def payload_box(c41: Any, chart: str, box: Any) -> dict[str, Any]:
    payload = c41.box_payload(box)
    need(payload is not None, "rational physical box")
    return {"compact_chart": chart, **payload}


def compact_chart(cell: dict[str, Any]) -> str:
    value = cell["gate3_chart"]
    need(type(value) is str and value.count(":") == 1,
         "two-part Gate3 chart")
    result = value.split(":")[1]
    need(result in {"E", "W", "N", "S"}, "compact chart enum")
    return result


def mirror_path(c41: Any, frozen: dict[str, Any], path: str) -> str:
    """Map a representative dyadic path by exact child-box reflection."""
    task = frozen["task"]
    rep_cell = task["cell"]
    ref_cell = frozen["context"]["cells"][task["c38_source"]["reflected_cell_id"]]
    rep_chart = compact_chart(rep_cell)
    ref_chart = compact_chart(ref_cell)
    rep_box, _ = c41.c39.reconstruct_box(rep_cell, "")
    ref_box, _ = c41.c39.reconstruct_box(ref_cell, "")
    reflected_root = c41.c40.reflected_payload(rep_chart, rep_box)
    need(
        reflected_root["compact_chart"] == ref_chart
        and {key: reflected_root[key] for key in ("t", "p", "s")}
        == c41.box_payload(ref_box),
        "root physical reflection",
    )
    mapped = ""
    for bit in path:
        rep_axis = c41.c38.round166.longest_axis(rep_box)
        ref_axis = c41.c38.round166.longest_axis(ref_box)
        need(rep_axis == ref_axis, "reflection preserves split axis")
        rep_children = c41.c38.round166.split_axis(rep_box, rep_axis)
        ref_children = c41.c38.round166.split_axis(ref_box, ref_axis)
        rep_box = rep_children[int(bit)]
        expected = c41.c40.reflected_payload(rep_chart, rep_box)
        matches = [
            candidate for candidate in (0, 1)
            if expected["compact_chart"] == ref_chart
            and {key: expected[key] for key in ("t", "p", "s")}
            == c41.box_payload(ref_children[candidate])
        ]
        need(len(matches) == 1, "unique exact reflected split child")
        mapped += str(matches[0])
        ref_box = ref_children[matches[0]]
    reconstructed, _ = c41.c39.reconstruct_box(ref_cell, mapped)
    need(c41.box_payload(reconstructed) == c41.box_payload(ref_box),
         "reflected mapped path reconstruction")
    return mapped


def physical_task(c41: Any, frozen: dict[str, Any], side: str, path: str) \
        -> tuple[dict[str, Any], Any, str, str]:
    base = frozen["task"]["c38_source"]
    if side == "REPRESENTATIVE":
        cell = frozen["task"]["cell"]
        physical_path = path
        pseudo = copy.deepcopy(base)
    else:
        need(side == "REFLECTED", "physical side")
        physical_path = mirror_path(c41, frozen, path)
        pseudo = copy.deepcopy(base)
        pseudo["representative_cell_id"] = base["reflected_cell_id"]
        pseudo["representative_origin_key"] = base["reflected_origin_key"]
        pseudo["reflected_cell_id"] = base["representative_cell_id"]
        pseudo["reflected_origin_key"] = base["representative_origin_key"]
        cell = frozen["context"]["cells"][pseudo["representative_cell_id"]]
    pseudo["path"] = physical_path
    task = {
        "task_id": "c48-route:" + side + ":" + path,
        "kind": "C1", "row": pseudo, "cell": cell,
    }
    return task, cell, pseudo["representative_origin_key"], physical_path


def arb_payload(c41: Any, value: Any | None) -> dict[str, Any] | None:
    return None if value is None else c41.c39.arb_payload(value)


def record_payload(c41: Any, record: Any) -> dict[str, Any]:
    return {
        "target_id": record.target_id,
        "classification": record.classification,
        "ell": arb_payload(c41, record.ell),
        "discriminant": arb_payload(c41, record.discriminant),
        "near": arb_payload(c41, record.near),
        "far": arb_payload(c41, record.far),
        "transverse": arb_payload(c41, record.transverse),
    }


def exact_boundary_separation(c41: Any, left: str, right: str) -> dict[str, Any]:
    r181 = c41.round185.r181
    r178 = c41.round185.r178
    lx, lb, ly = r181.target_affine_center(left)
    rx, rb, ry = r181.target_affine_center(right)
    dx = r181.minimum_abs_affine(lx - rx, lb - rb)
    dy = ly - ry
    distance_squared = dx * dx + dy * dy
    radius_sum = Q(r178.base.RADIUS[left[0]]) + Q(r178.base.RADIUS[right[0]])
    margin = distance_squared - radius_sum * radius_sum
    need(margin > 0, "strict obstacle-boundary separation")
    return {
        "left": left, "right": right,
        "minimum_center_distance_squared": qstr(distance_squared),
        "radius_sum_squared": qstr(radius_sum * radius_sum),
        "strict_squared_margin": qstr(margin),
    }


def terminal_margin(c41: Any, cell: dict[str, Any], origin: str, box: Any,
                    route_result: dict[str, Any], c2_detail: dict[str, Any],
                    expected_owners: list[str]) -> dict[str, Any]:
    # Collision-one: exact whole-box owner and H1 strict-side route.
    _reconstructed, active = c41.c39.reconstruct_box(cell, box.path)
    stage, records = c41.c38.round166.classify_active(
        cell["gate3_chart"], box, active
    )
    c1_rows = [record_payload(c41, row) for row in records]
    c1_unresolved = [row for row in records if row.classification in {
        "unresolved_discriminant", "unresolved_root_sign"
    }]
    h1 = route_result["surface_evidence"]["H1"]
    c1_complete = (
        stage.classification == "unique_first"
        and stage.owner_target == c41.FROZEN_OWNER
        and not c1_unresolved
        and h1 is not None and h1["kind"] == "STRICT_SIDE"
        and h1["chart"] == "W"
        and h1["H1_centered"]["sign"] in {"POSITIVE", "NEGATIVE"}
    )

    # Collision-two: reproduce the exact classifier's topological margin.
    r178 = c41.round185.r178
    r181 = c41.round185.r181
    r183 = c41.round185.r183
    state = r181.collision1_state_direct(origin, box)
    geometry = r183.collision2_geometry(state)
    point_box = r181.center_box(box)
    point_state = r181.collision1_state_direct(origin, point_box)
    point_geometry = r183.collision2_geometry(point_state)
    point_status, point_selected = r178.select_owner(
        point_geometry, r183.CANDIDATES
    )
    need(point_status == "STRICT_UNIQUE_OWNER" and isinstance(point_selected, tuple),
         "strict center collision-two owner")
    point_owner, point_owner_data = point_selected
    full_owner_kind, full_owner_data = r178.root_record(
        *geometry, point_owner
    )
    need(full_owner_kind == "STRICT_FUTURE" and full_owner_data is not None,
         "incumbent strict future over full box")
    point_rows: list[dict[str, Any]] = []
    full_rows: list[dict[str, Any]] = []
    for candidate in r183.CANDIDATES:
        point_kind, point_data = r178.root_record(*point_geometry, candidate)
        point_row: dict[str, Any] = {
            "candidate": candidate, "root_kind": point_kind,
            "strict_gap_after_owner": None,
        }
        if candidate != point_owner and point_kind == "STRICT_FUTURE":
            need(point_data is not None, "point competitor data")
            gap = point_data["near"] - point_owner_data["near"]
            need(bool(gap > 0), "strict point root-order gap")
            point_row["strict_gap_after_owner"] = arb_payload(c41, gap)
        point_rows.append(point_row)

        full_kind, full_data = r178.root_record(*geometry, candidate)
        raw = r181.raw_candidate(geometry, candidate)
        disposition = "FULL_BOX_RESOLVED_ROOT_STATUS"
        strict_screen = None
        if candidate != point_owner and full_kind in {
            "UNRESOLVED_DELTA", "UNRESOLVED_ROOT_SIGN"
        }:
            if bool(raw["ell"] + raw["radius"] < 0):
                margin = -(raw["ell"] + raw["radius"])
                disposition = "STRICT_BEHIND_BY_UNIVERSAL_UPPER_BOUND"
                strict_screen = arb_payload(c41, margin)
            elif bool(full_owner_data["near"] < raw["ell"] - raw["radius"]):
                margin = raw["ell"] - raw["radius"] - full_owner_data["near"]
                disposition = "STRICT_LATER_BY_UNIVERSAL_LOWER_BOUND"
                strict_screen = arb_payload(c41, margin)
            else:
                disposition = "UNSCREENED_ACTIVE_COMPETITOR"
        full_rows.append({
            "candidate": candidate, "root_kind": full_kind,
            "raw_ell": arb_payload(c41, raw["ell"]),
            "raw_discriminant": arb_payload(c41, raw["Delta"]),
            "screening_disposition": disposition,
            "strict_screening_margin": strict_screen,
        })
    unscreened = [row for row in full_rows
                  if row["screening_disposition"] == "UNSCREENED_ACTIVE_COMPETITOR"]
    separations = [
        exact_boundary_separation(c41, point_owner, candidate)
        for candidate in r183.CANDIDATES if candidate != point_owner
    ]
    c2_complete = (
        not unscreened
        and c2_detail["point_owner"] == point_owner
        and c2_detail["absolute_collision2_owner"] == point_owner
        and point_owner not in expected_owners
    )
    body = {
        "schema": MARGIN_SCHEMA,
        "collision1": {
            "whole_box_stage_classification": stage.classification,
            "whole_box_owner": stage.owner_target,
            "record_rows": c1_rows,
            "unresolved_record_count": len(c1_unresolved),
            "H1_strict_side": h1,
            "complete": c1_complete,
        },
        "collision2": {
            "center_point_owner_status": point_status,
            "center_point_owner": point_owner,
            "center_point_root_rows": point_rows,
            "full_box_incumbent_root_kind": full_owner_kind,
            "full_box_candidate_rows": full_rows,
            "unscreened_active_competitor_count": len(unscreened),
            "exact_boundary_separation_rows": separations,
            "continuation_argument": (
                "CONNECTED_RATIONAL_BOX__STRICT_CENTER_ORDER__EVERY_UNRESOLVED_"
                "FULL_BOX_COMPETITOR_STRICTLY_SCREENED__POSITIVE_EXACT_"
                "OBSTACLE_BOUNDARY_SEPARATION_FORBIDS_ROOT_ORDER_CROSSING"
            ),
            "selected_absolute_owner": point_owner,
            "allowed_collision2_continuation_owners": expected_owners,
            "terminal_decision": "STRICT_COLLISION2_OWNER_MISMATCH",
            "complete": c2_complete,
        },
        "all_required_strict_margins_complete": c1_complete and c2_complete,
        "formal_credit": 0,
    }
    return {**body, "margin_certificate_sha256": digest(body)}


def route_leaf(c41: Any, frozen: dict[str, Any], side: str,
               relative: str) -> tuple[dict[str, Any], dict[str, Any]]:
    semantic_path = ROOT_PATH + relative
    task, cell, origin, physical_path = physical_task(
        c41, frozen, side, semantic_path
    )
    result = c41.c39.route_c1_task(task, frozen["config"])
    box, _active = c41.c39.reconstruct_box(cell, physical_path)
    classification = result["classification"]
    witness = result["witness"]
    c2_status = c2_baseline = None
    c2_detail: dict[str, Any] | None = None
    c2_evidence: list[dict[str, Any]] = []
    if c41.c40.collision2_safe(result, classification):
        c2_status, c2_detail, c2_evidence, c2_baseline = (
            c41.round185.resolve_dynamic_box(
                origin, box, frozen["config"]["pair_index"],
                frozen["config"]["pattern_index"],
            )
        )
        if c2_status.startswith("LOCAL_EXACT_KEY"):
            classification, witness = c41.c40.expected_collision2(
                c2_detail, frozen["config"]
            )
        else:
            classification = "UNRESOLVED_C40_COLLISION2_" + c2_status
            witness = c2_baseline
    need(c2_detail is not None, "collision-two detail materialized")
    need(classification == "EXCLUDED_C40_COLLISION2_OWNER_MISMATCH",
         "two-side leaf terminal owner mismatch")
    expected_owners = sorted({
        frozen["config"]["original_path"][1]["selected_absolute_owner_id"],
        frozen["config"]["reflected_path"][1]["selected_absolute_owner_id"],
    })
    margin = terminal_margin(
        c41, cell, origin, box, result, c2_detail, expected_owners
    )
    need(margin["all_required_strict_margins_complete"],
         "strict terminal margin complete")
    chart = compact_chart(cell)
    body = {
        "schema": LEAF_SCHEMA,
        "side": side,
        "pair_index": PAIR,
        "task_binding_sha256": TASK_BINDING,
        "relative_path": relative,
        "semantic_path": semantic_path,
        "physical_route_path": physical_path,
        "physical_cell_id": cell["cell_id"],
        "physical_origin_key": origin,
        "exact_closed_box": payload_box(c41, chart, box),
        "relative_parent_fraction": qstr(Q(1, 2 ** len(relative))),
        "C1_route_result": result,
        "C1_route_result_sha256": digest(result),
        "C2_status": c2_status,
        "C2_baseline": c2_baseline,
        "C2_detail": c2_detail,
        "C2_detail_sha256": digest(c2_detail),
        "C2_evidence": c2_evidence,
        "C2_evidence_sequence_sha256": sequence_digest(
            digest(row) for row in c2_evidence
        ),
        "terminal_classification": classification,
        "terminal_witness": witness,
        "terminal_margin_certificate": margin,
        "terminal_candidate_closed": True,
        "formal_credit": 0,
    }
    leaf = {**body, "physical_leaf_id": "c48-leaf:" + digest(body)}
    internal = {
        "box_object": box, "cell": cell, "chart": chart,
        "semantic_path": semantic_path, "physical_path": physical_path,
    }
    return leaf, internal


def occurrence_body(row: dict[str, Any], side: str, chart: str | None,
                    box: dict[str, Any] | None) -> dict[str, Any]:
    return {
        "source_kind": "C41_BASELINE",
        "side": side,
        "pair_index": row["pair_index"],
        "semantic_path": row["path"],
        "physical_route_path": None,
        "physical_cell_id": row[
            "representative_cell_id" if side == "REPRESENTATIVE"
            else "reflected_cell_id"
        ],
        "compact_chart": chart,
        "exact_closed_box": box,
        "upstream_ambient_cell_id": row["c41_ambient_cell_id"],
        "upstream_ambient_row_sha256": row["row_sha256"],
        "upstream_disposition_family": row["disposition_family"],
        "replacement_leaf_id": None,
    }


def occurrence_from_leaf(leaf: dict[str, Any]) -> dict[str, Any]:
    return {
        "source_kind": "C48_REPLACEMENT",
        "side": leaf["side"], "pair_index": PAIR,
        "semantic_path": leaf["semantic_path"],
        "physical_route_path": leaf["physical_route_path"],
        "physical_cell_id": leaf["physical_cell_id"],
        "compact_chart": leaf["exact_closed_box"]["compact_chart"],
        "exact_closed_box": {
            key: leaf["exact_closed_box"][key] for key in ("t", "p", "s")
        },
        "upstream_ambient_cell_id": AMBIENT_ID,
        "upstream_ambient_row_sha256": None,
        "upstream_disposition_family": None,
        "replacement_leaf_id": leaf["physical_leaf_id"],
    }


def close_occurrence(body: dict[str, Any]) -> dict[str, Any]:
    binding = digest(body)
    result = {
        **body,
        "occurrence_binding_sha256": binding,
        "physical_occurrence_id": "c48-occurrence:" + binding,
    }
    box = body["exact_closed_box"]
    if box is None:
        result["rational"] = False
        return result
    t0, t1 = qpair(box["t"])
    p0, p1 = qpair(box["p"])
    s0, s1 = qpair(box["s"])
    need(t0 < t1 and p0 < p1 and s0 == s1 == 0,
         "positive rational s=0 occurrence")
    result.update({
        "rational": True, "t0": t0, "t1": t1,
        "p0": p0, "p1": p1,
    })
    return result


def build_universe(c41: Any, frozen: dict[str, Any],
                   leaves: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    baseline: list[dict[str, Any]] = []
    removed: list[str] = []
    descriptor = frozen["C41_result"]["ledgers"]["routed_ambient_cells"]
    count = 0
    for row in c41.iter_ledger(C41_DIR, descriptor):
        count += 1
        for side in ("REPRESENTATIVE", "REFLECTED"):
            if side == "REPRESENTATIVE":
                cell_id = row["representative_cell_id"]
                chart = compact_chart(frozen["context"]["cells"][cell_id])
                box = row["closed_representative_box"]
            else:
                box = row["closed_reflected_box"]
                chart = None if box is None else box["compact_chart"]
                box = None if box is None else {
                    key: box[key] for key in ("t", "p", "s")
                }
            occurrence = close_occurrence(occurrence_body(row, side, chart, box))
            baseline.append(occurrence)
            if row["c41_ambient_cell_id"] == AMBIENT_ID:
                removed.append(occurrence["physical_occurrence_id"])
    need(count == EXPECTED_C41_AMBIENT_COUNT, "full C41 universe scanned")
    need(len(baseline) == EXPECTED_BASELINE_PHYSICAL_OCCURRENCE_COUNT,
         "baseline physical occurrence census")
    need(sum(row["rational"] for row in baseline)
         == EXPECTED_EXACT_RATIONAL_BASELINE_OCCURRENCE_COUNT,
         "baseline rational occurrence census")
    need(len(removed) == 2, "two selected predecessor occurrences")
    overlay = [row for row in baseline
               if row["physical_occurrence_id"] not in set(removed)]
    inserted = [close_occurrence(occurrence_from_leaf(row)) for row in leaves]
    overlay.extend(inserted)
    need(len(overlay) == EXPECTED_OVERLAY_PHYSICAL_OCCURRENCE_COUNT,
         "overlay occurrence census")
    roots = {
        "C41_ambient_row_count": count,
        "baseline_physical_occurrence_count": len(baseline),
        "baseline_exact_rational_occurrence_count": sum(
            row["rational"] for row in baseline
        ),
        "baseline_occurrence_binding_sequence_sha256": sequence_digest(sorted(
            row["occurrence_binding_sha256"] for row in baseline
        )),
        "removed_predecessor_occurrence_ids": sorted(removed),
        "inserted_replacement_occurrence_ids": sorted(
            row["physical_occurrence_id"] for row in inserted
        ),
        "overlay_physical_occurrence_count": len(overlay),
        "overlay_occurrence_binding_sequence_sha256": sequence_digest(sorted(
            row["occurrence_binding_sha256"] for row in overlay
        )),
        "full_pinned_active_C41_universe_scanned": True,
    }
    return overlay, roots


def interval_overlap(left0: Q, left1: Q, right0: Q, right1: Q) -> tuple[Q, Q] | None:
    low, high = max(left0, right0), min(left1, right1)
    return (low, high) if low < high else None


def leaf_faces(leaf: dict[str, Any]) -> list[dict[str, Any]]:
    box = leaf["exact_closed_box"]
    t0, t1 = qpair(box["t"])
    p0, p1 = qpair(box["p"])
    return [
        {"face": "t_lower", "axis": "t", "fixed": t0, "low": p0, "high": p1},
        {"face": "t_upper", "axis": "t", "fixed": t1, "low": p0, "high": p1},
        {"face": "p_lower", "axis": "p", "fixed": p0, "low": t0, "high": t1},
        {"face": "p_upper", "axis": "p", "fixed": p1, "low": t0, "high": t1},
    ]


def incident_face(occ: dict[str, Any], chart: str, axis: str, fixed: Q,
                  low: Q, high: Q) -> tuple[str, tuple[Q, Q]] | None:
    if not occ["rational"] or occ["compact_chart"] != chart:
        return None
    if axis == "t":
        overlap = interval_overlap(low, high, occ["p0"], occ["p1"])
        if overlap is None:
            return None
        directions = []
        if occ["t1"] == fixed:
            directions.append("LOWER_COORDINATE_SIDE")
        if occ["t0"] == fixed:
            directions.append("UPPER_COORDINATE_SIDE")
    else:
        overlap = interval_overlap(low, high, occ["t0"], occ["t1"])
        if overlap is None:
            return None
        directions = []
        if occ["p1"] == fixed:
            directions.append("LOWER_COORDINATE_SIDE")
        if occ["p0"] == fixed:
            directions.append("UPPER_COORDINATE_SIDE")
    need(len(directions) <= 1, "positive-width occurrence has one face side")
    return None if not directions else (directions[0], overlap)


def compact_incident(row: dict[str, Any], direction: str | None = None) -> dict[str, Any]:
    result = {
        "physical_occurrence_id": row["physical_occurrence_id"],
        "occurrence_binding_sha256": row["occurrence_binding_sha256"],
        "source_kind": row["source_kind"], "side": row["side"],
        "pair_index": row["pair_index"],
        "semantic_path": row["semantic_path"],
        "physical_route_path": row["physical_route_path"],
        "physical_cell_id": row["physical_cell_id"],
        "replacement_leaf_id": row["replacement_leaf_id"],
    }
    if direction is not None:
        result["geometric_side"] = direction
    return result


def unique_semantic_owner(incidents: list[dict[str, Any]]) -> tuple[dict[str, Any] | None, bool]:
    need(bool(incidents), "nonempty incident set")
    minimum = min(row["semantic_path"] for row in incidents)
    winners = [row for row in incidents if row["semantic_path"] == minimum]
    return (winners[0], True) if len(winners) == 1 else (None, False)


def face_ledger(overlay: list[dict[str, Any]], leaves: list[dict[str, Any]]) \
        -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    target_faces = []
    for leaf in leaves:
        for face in leaf_faces(leaf):
            target_faces.append({
                **face, "chart": leaf["exact_closed_box"]["compact_chart"],
                "side": leaf["side"], "leaf_id": leaf["physical_leaf_id"],
            })
    atom_targets: dict[tuple[str, str, Q, Q, Q], list[dict[str, Any]]] = {}
    leaf_face_occurrences: list[dict[str, Any]] = []
    for target in target_faces:
        breaks = {target["low"], target["high"]}
        for occ in overlay:
            match = incident_face(
                occ, target["chart"], target["axis"], target["fixed"],
                target["low"], target["high"],
            )
            if match is not None:
                breaks.update(match[1])
        ordered = sorted(breaks)
        for low, high in zip(ordered, ordered[1:]):
            if low == high:
                continue
            key = (target["chart"], target["axis"], target["fixed"], low, high)
            ref = {"leaf_id": target["leaf_id"], "face": target["face"]}
            atom_targets.setdefault(key, [])
            if ref not in atom_targets[key]:
                atom_targets[key].append(ref)
            leaf_face_occurrences.append({"key": key, **ref})
    rows = []
    for key in sorted(atom_targets, key=lambda value: tuple(map(str, value))):
        chart, axis, fixed, low, high = key
        incidents = []
        for occ in overlay:
            match = incident_face(occ, chart, axis, fixed, low, high)
            if match is not None and match[1][0] <= low and high <= match[1][1]:
                incidents.append((occ, match[0]))
        incidents.sort(key=lambda item: item[0]["physical_occurrence_id"])
        by_direction = {
            direction: [row for row, observed in incidents if observed == direction]
            for direction in ("LOWER_COORDINATE_SIDE", "UPPER_COORDINATE_SIDE")
        }
        complete = all(len(rows_at_side) == 1 for rows_at_side in by_direction.values())
        incident_rows = [compact_incident(row, direction) for row, direction in incidents]
        owner, unique = unique_semantic_owner(incident_rows)
        geometry = {
            "compact_chart": chart,
            "t": [qstr(fixed), qstr(fixed)] if axis == "t" else [qstr(low), qstr(high)],
            "p": [qstr(low), qstr(high)] if axis == "t" else [qstr(fixed), qstr(fixed)],
            "s": ["0", "0"],
        }
        body = {
            "schema": FACE_SCHEMA,
            "canonical_entity_key": {"compact_chart": chart, "exact_closed_face_box": geometry},
            "axis": axis, "target_leaf_face_references": sorted(
                atom_targets[key], key=lambda row: (row["leaf_id"], row["face"])
            ),
            "positive_length_face_overlap_only": True,
            "incident_occurrence_count": len(incident_rows),
            "incident_occurrences": incident_rows,
            "incident_occurrence_binding_sequence_sha256": sequence_digest(
                row["occurrence_binding_sha256"] for row in incident_rows
            ),
            "geometric_side_counts": {
                name: len(values) for name, values in by_direction.items()
            },
            "incident_set_complete": complete,
            "owner_rule": "UNIQUE_LEXICOGRAPHIC_MINIMUM_C41_SEMANTIC_PATH",
            "owner_unique": unique,
            "owner": owner,
            "formal_credit": 0,
        }
        rows.append({**body, "face_atom_id": "c48-face:" + digest(body)})
    return rows, leaf_face_occurrences


QUADRANTS = (
    ("t-_p-", -1, -1), ("t-_p+", -1, 1),
    ("t+_p-", 1, -1), ("t+_p+", 1, 1),
)


def quadrant_membership(occ: dict[str, Any], t: Q, p: Q) -> list[str]:
    if not occ["rational"]:
        return []
    result = []
    for name, tsign, psign in QUADRANTS:
        t_ok = occ["t0"] < t <= occ["t1"] if tsign < 0 else occ["t0"] <= t < occ["t1"]
        p_ok = occ["p0"] < p <= occ["p1"] if psign < 0 else occ["p0"] <= p < occ["p1"]
        if t_ok and p_ok:
            result.append(name)
    return result


def leaf_corners(leaf: dict[str, Any]) -> list[tuple[Q, Q]]:
    box = leaf["exact_closed_box"]
    t0, t1 = qpair(box["t"])
    p0, p1 = qpair(box["p"])
    return [(t0, p0), (t0, p1), (t1, p0), (t1, p1)]


def corner_ledger(overlay: list[dict[str, Any]], leaves: list[dict[str, Any]],
                  faces: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], int]:
    points: set[tuple[str, Q, Q]] = set()
    for face in faces:
        box = face["canonical_entity_key"]["exact_closed_face_box"]
        chart = box["compact_chart"]
        if face["axis"] == "t":
            t = Q(box["t"][0])
            points.add((chart, t, Q(box["p"][0])))
            points.add((chart, t, Q(box["p"][1])))
        else:
            p = Q(box["p"][0])
            points.add((chart, Q(box["t"][0]), p))
            points.add((chart, Q(box["t"][1]), p))
    leaf_corner_occurrences = 0
    rows = []
    for chart, t, p in sorted(points, key=lambda value: tuple(map(str, value))):
        target_boundary = []
        target_corners = []
        for leaf in leaves:
            if leaf["exact_closed_box"]["compact_chart"] != chart:
                continue
            box = leaf["exact_closed_box"]
            t0, t1 = qpair(box["t"]); p0, p1 = qpair(box["p"])
            if t0 <= t <= t1 and p0 <= p <= p1 and (
                    t in {t0, t1} or p in {p0, p1}):
                target_boundary.append(leaf["physical_leaf_id"])
            if (t, p) in leaf_corners(leaf):
                target_corners.append(leaf["physical_leaf_id"])
                leaf_corner_occurrences += 1
        incidents = []
        quadrant_map: dict[str, list[str]] = {name: [] for name, _t, _p in QUADRANTS}
        for occ in overlay:
            if occ["compact_chart"] != chart:
                continue
            quadrants = quadrant_membership(occ, t, p)
            if quadrants:
                incidents.append((occ, quadrants))
                for quadrant in quadrants:
                    quadrant_map[quadrant].append(occ["physical_occurrence_id"])
        incidents.sort(key=lambda item: item[0]["physical_occurrence_id"])
        compact = []
        for occ, quadrants in incidents:
            item = compact_incident(occ)
            item["occupied_quadrants"] = sorted(quadrants)
            compact.append(item)
        complete = all(len(values) == 1 for values in quadrant_map.values())
        owner, unique = unique_semantic_owner(compact)
        count = len(compact)
        kind = {
            3: "THREE_WAY_T_JUNCTION",
            4: "FOUR_WAY_CROSS_JUNCTION",
            2: "TWO_CELL_FACE_VERTEX",
            1: "SINGLE_CELL_CORNER",
        }.get(count, "OTHER_INCIDENT_CENSUS")
        body = {
            "schema": CORNER_SCHEMA,
            "canonical_entity_key": {
                "compact_chart": chart,
                "exact_closed_corner_box": {
                    "compact_chart": chart, "t": [qstr(t), qstr(t)],
                    "p": [qstr(p), qstr(p)], "s": ["0", "0"],
                },
            },
            "junction_kind": kind,
            "target_leaf_boundary_occurrence_ids": sorted(target_boundary),
            "target_leaf_corner_occurrence_ids": sorted(target_corners),
            "incident_occurrence_count": count,
            "incident_occurrences": compact,
            "incident_occurrence_binding_sequence_sha256": sequence_digest(
                row["occurrence_binding_sha256"] for row in compact
            ),
            "quadrant_incident_occurrence_ids": {
                key: sorted(values) for key, values in sorted(quadrant_map.items())
            },
            "four_quadrant_germ_complete": complete,
            "incident_set_complete": complete,
            "owner_rule": "UNIQUE_LEXICOGRAPHIC_MINIMUM_C41_SEMANTIC_PATH",
            "owner_unique": unique,
            "owner": owner,
            "formal_credit": 0,
        }
        rows.append({**body, "corner_entity_id": "c48-corner:" + digest(body)})
    return rows, leaf_corner_occurrences


def logical_successor_leaves(
    leaves: list[dict[str, Any]], faces: list[dict[str, Any]],
    corners: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """Group the six physical rows into three exact logical exits."""
    result = []
    for relative in RELATIVE_LEAVES:
        sides = []
        side_leaf_ids = set()
        for side in ("REPRESENTATIVE", "REFLECTED"):
            leaf = next(row for row in leaves
                        if row["relative_path"] == relative
                        and row["side"] == side)
            side_leaf_ids.add(leaf["physical_leaf_id"])
            route = {
                "physical_leaf_id": leaf["physical_leaf_id"],
                "side": side,
                "semantic_path": leaf["semantic_path"],
                "physical_route_path": leaf["physical_route_path"],
                "physical_cell_id": leaf["physical_cell_id"],
                "physical_origin_key": leaf["physical_origin_key"],
                "exact_closed_box": leaf["exact_closed_box"],
                "C1_route_result": leaf["C1_route_result"],
                "C1_route_result_sha256": leaf["C1_route_result_sha256"],
                "C2_status": leaf["C2_status"],
                "C2_baseline": leaf["C2_baseline"],
                "C2_detail": leaf["C2_detail"],
                "C2_detail_sha256": leaf["C2_detail_sha256"],
                "terminal_classification": leaf["terminal_classification"],
                "terminal_witness": leaf["terminal_witness"],
            }
            side_body = {
                "side": side,
                "independent_route": route,
                "strict_terminal_margin": leaf[
                    "terminal_margin_certificate"
                ],
                "route_complete": leaf["terminal_candidate_closed"],
                "strict_terminal_margin_complete": leaf[
                    "terminal_margin_certificate"
                ]["all_required_strict_margins_complete"],
                "formal_credit": 0,
            }
            sides.append({
                **side_body,
                "physical_side_certificate_sha256": digest(side_body),
            })
        face_ids = sorted(
            row["face_atom_id"] for row in faces
            if any(ref["leaf_id"] in side_leaf_ids
                   for ref in row["target_leaf_face_references"])
        )
        corner_ids = sorted(
            row["corner_entity_id"] for row in corners
            if any(leaf_id in side_leaf_ids
                   for leaf_id in row["target_leaf_boundary_occurrence_ids"])
        )
        body = {
            "schema": SCHEMA + ".logical-exit-certificate",
            "task_binding_sha256": TASK_BINDING,
            "relative_path": relative,
            "absolute_path": ROOT_PATH + relative,
            "relative_fraction": qstr(Q(1, 2 ** len(relative))),
            "exit_class": "STRICT_EXCLUDED",
            "physical_sides": sides,
            "physical_side_count": 2,
            "shared_face_atom_ids": face_ids,
            "shared_corner_entity_ids": corner_ids,
            "all_referenced_face_incident_sets_complete": all(
                row["incident_set_complete"] and row["owner_unique"]
                for row in faces if row["face_atom_id"] in face_ids
            ),
            "all_referenced_corner_incident_sets_complete": all(
                row["incident_set_complete"] and row["owner_unique"]
                for row in corners if row["corner_entity_id"] in corner_ids
            ),
            "both_physical_sides_independently_routed": True,
            "both_physical_sides_strictly_excluded": True,
            "formal_credit": 0,
        }
        result.append({
            **body,
            "exit_certificate_object_sha256": digest(body),
            "logical_exit_id": "c48-logical-exit:" + digest(body),
        })
    return result


def exact_split_events(c41: Any, frozen: dict[str, Any]) -> list[dict[str, Any]]:
    task = frozen["task"]
    source_path = frozen["source"]["path"]
    events = []
    for relative in ("", "1"):
        absolute = ROOT_PATH + relative
        bits = absolute[len(source_path):]
        box, _active = c41.c39.reconstruct_box(task["cell"], absolute)
        history = c41.exact_axis_history(task, bits)
        adjacency, _children, axis = c41.split_row(
            task, box, bits, len(bits), history
        )
        body = {
            "relative_path": relative,
            "absolute_path": absolute,
            "split_axis": ("t", "p", "s")[axis],
            "split_coordinate": adjacency["exact_split_coordinate"],
            "C41_split_face_adjacency": adjacency,
            "C41_split_face_adjacency_sha256": digest(adjacency),
            "oracle_adapter_source_path": str(SELF.relative_to(ROOT)),
            "oracle_adapter_source_sha256": file_sha256(SELF),
            "formal_credit": 0,
        }
        need(body["split_axis"] in {"t", "p"}, "in-slice C48 split")
        events.append({
            **body, "split_event_object_sha256": digest(body)
        })
    return events


def successor_checkpoint(
    c46: Any, c41: Any, frozen: dict[str, Any],
    logical_leaves: list[dict[str, Any]],
) -> dict[str, Any]:
    shard = next(row for row in frozen["plan"]["sharding"]["shards"]
                 if row["shard_index"] == SHARD_INDEX)
    internal_shard = None
    _plan, _tasks, shards = c46.build_read_only_plan(64)
    for candidate in shards:
        if candidate["shard_index"] == SHARD_INDEX:
            internal_shard = candidate
            break
    need(internal_shard is not None, "C46 internal shard-2")
    need(
        shard["shard_id"] == internal_shard["shard_id"] == SHARD_ID
        and shard["task_count"] == len(internal_shard["_tasks"])
        == SHARD_TASK_COUNT
        and shard["ordered_task_binding_sequence_sha256"]
        == internal_shard["ordered_task_binding_sequence_sha256"]
        == SHARD_BINDING_SEQUENCE_SHA256,
        "C46 shard-2 exact pins",
    )
    tasks = internal_shard["_tasks"]
    need(tasks[0]["task_binding_sha256"] == TASK_BINDING,
         "selected task is shard-2 index zero")
    genesis = c46.make_checkpoint(frozen["plan"], internal_shard)
    need(genesis["checkpoint_object_sha256"]
         == GENESIS_CHECKPOINT_OBJECT_SHA256,
         "C46 genesis checkpoint object pin")
    old_states = genesis["task_states"]
    need(len(old_states) == SHARD_TASK_COUNT, "genesis state vector census")
    split_events = exact_split_events(c41, frozen)
    selected_old_sha = digest(old_states[0])
    selected_body = {
        "schema": SCHEMA + ".successor-task-state",
        "C46_predecessor_task_state_sha256": selected_old_sha,
        "task_id": tasks[0]["task_id"],
        "task_binding_sha256": TASK_BINDING,
        "pair_index": PAIR,
        "source_descendant_path": ROOT_PATH,
        "dependency_closure_sha256": tasks[0]["dependency_closure_sha256"],
        "state": "C48_CANDIDATE_SOURCE_CLOSED_ZERO_CREDIT_PENDING_AUDIT",
        "frontier": [],
        "exits": logical_leaves,
        "split_events": split_events,
        "event_count": 5,
        "deepest_additional_depth": 2,
        "relative_Kraft_sum": "1",
        "prefix_free": True,
        "candidate_closed": True,
        "formal_closed": False,
        "credit_lock": {
            "ambient_credit": 0, "terminal_credit": 0,
            "whole_parent_credit": 0, "D02_gate_credit": 0,
            "formal_credit": 0,
        },
    }
    selected_state = {
        **selected_body,
        "successor_task_state_sha256": digest(selected_body),
    }
    task_states = [selected_state, *copy.deepcopy(old_states[1:])]
    need(
        all(canonical(task_states[index]) == canonical(old_states[index])
            for index in range(1, SHARD_TASK_COUNT)),
        "other 513 genesis states preserved byte-for-byte",
    )
    unchanged_root = sequence_digest(
        digest(state) for state in old_states[1:]
    )
    body = {
        "schema": SCHEMA + ".generation-1-successor-checkpoint",
        "status": (
            "C48_ONE_TASK_CANDIDATE_CLOSED__513_SHARD_TASKS_PENDING__"
            "PENDING_INDEPENDENT_AUDIT__ZERO_FORMAL_CREDIT"
        ),
        "plan_object_sha256": C46_PLAN_OBJECT_SHA256,
        "shard_id": SHARD_ID, "shard_index": SHARD_INDEX,
        "generation": 1,
        "previous_checkpoint_object_sha256": GENESIS_CHECKPOINT_OBJECT_SHA256,
        "task_count": SHARD_TASK_COUNT,
        "selected_task_index": 0,
        "candidate_closed_task_count": 1,
        "formal_closed_task_count": 0,
        "pending_task_count": SHARD_TASK_COUNT - 1,
        "ordered_task_binding_sequence_sha256": SHARD_BINDING_SEQUENCE_SHA256,
        "ordered_task_state_sequence_sha256": sequence_digest(
            digest(state) for state in task_states
        ),
        "unchanged_indices_1_through_513_task_state_sequence_sha256": unchanged_root,
        "unchanged_indices_1_through_513_byte_equal_to_genesis": True,
        "task_states": task_states,
        "global_candidate_progress": {
            "frozen_C41_logical_residual_outer_row_count": 33_642,
            "frozen_C41_two_side_residual_occurrence_count": 67_284,
            "installed_C42_logical_closed_task_count": 1,
            "authoritative_logical_pending_task_count_before_C48": 33_641,
            "C48_additional_logical_candidate_closed_count_pending_audit": 1,
            "logical_pending_task_count_after_C48_candidate": 33_640,
            "two_side_pending_occurrence_count_after_C42_and_C48_candidate": 67_280,
            "coarse_formal_authority_unchanged": {
                "paired_coarse_cells": 574,
                "unresolved_coarse_cells": 1_150,
                "representative_parents_remaining": 575,
            },
        },
        "credit_lock": {
            "ambient_credit": 0, "terminal_credit": 0,
            "whole_parent_credit": 0, "D02_gate_credit": 0,
            "formal_credit": 0,
        },
    }
    return {
        **body,
        "successor_checkpoint_object_sha256": digest(body),
        "genesis_checkpoint": genesis,
    }


def build_result() -> dict[str, Any]:
    c46, c41 = load_modules()
    frozen = selected_inputs(c46, c41)
    leaves: list[dict[str, Any]] = []
    internals: dict[tuple[str, str], dict[str, Any]] = {}
    for side in ("REPRESENTATIVE", "REFLECTED"):
        for relative in RELATIVE_LEAVES:
            leaf, internal = route_leaf(c41, frozen, side, relative)
            leaves.append(leaf)
            internals[(side, relative)] = internal
    leaves.sort(key=lambda row: (row["side"], row["relative_path"]))
    need(sum((Q(row["relative_parent_fraction"]) for row in leaves
              if row["side"] == "REPRESENTATIVE"), Q(0)) == 1,
         "representative exact Kraft")
    need(sum((Q(row["relative_parent_fraction"]) for row in leaves
              if row["side"] == "REFLECTED"), Q(0)) == 1,
         "reflected exact Kraft")
    for relative in RELATIVE_LEAVES:
        rep = next(row for row in leaves if row["side"] == "REPRESENTATIVE"
                   and row["relative_path"] == relative)
        ref = next(row for row in leaves if row["side"] == "REFLECTED"
                   and row["relative_path"] == relative)
        reflected = c41.c40.reflected_payload(
            rep["exact_closed_box"]["compact_chart"],
            internals[("REPRESENTATIVE", relative)]["box_object"],
        )
        need(reflected == ref["exact_closed_box"], "leaf reflection involution")

    overlay, universe = build_universe(c41, frozen, leaves)
    faces, leaf_face_occurrences = face_ledger(overlay, leaves)
    corners, leaf_corner_occurrences = corner_ledger(overlay, leaves, faces)
    # The selected representative/reflected boxes are disjoint E-chart regions;
    # target references, not chart alone, define the side census.
    face_by_side = {
        side: sum(any(ref["leaf_id"] in {
            row["physical_leaf_id"] for row in leaves if row["side"] == side
        } for ref in face["target_leaf_face_references"]) for face in faces)
        for side in ("REPRESENTATIVE", "REFLECTED")
    }
    corner_by_side = {
        side: sum(any(leaf_id in {
            row["physical_leaf_id"] for row in leaves if row["side"] == side
        } for leaf_id in corner["target_leaf_boundary_occurrence_ids"])
                  for corner in corners)
        for side in ("REPRESENTATIVE", "REFLECTED")
    }
    leaf_face_by_side = {
        side: sum(ref["leaf_id"] in {
            row["physical_leaf_id"] for row in leaves if row["side"] == side
        } for ref in leaf_face_occurrences)
        for side in ("REPRESENTATIVE", "REFLECTED")
    }
    need(face_by_side == {"REPRESENTATIVE": 10, "REFLECTED": 10},
         "10 face atoms per side")
    need(leaf_face_by_side == {"REPRESENTATIVE": 13, "REFLECTED": 13},
         "13 leaf-face atom occurrences per side")
    need(corner_by_side == {"REPRESENTATIVE": 8, "REFLECTED": 8},
         "8 corner entities per side")
    need(leaf_corner_occurrences == 24, "12 leaf-corner occurrences per side")
    selected_leaf_ids = {row["physical_leaf_id"] for row in leaves}
    selected_internal_t_junctions = [
        row for row in corners
        if row["junction_kind"] == "THREE_WAY_T_JUNCTION"
        and len(set(row["target_leaf_boundary_occurrence_ids"])
                & selected_leaf_ids) == 3
    ]
    need(len(selected_internal_t_junctions) == 2,
         "one selected-frontier internal T-junction per side")
    all_faces = all(
        row["incident_set_complete"] and row["owner_unique"]
        and row["incident_occurrence_count"] == 2 for row in faces
    )
    all_corners = all(
        row["incident_set_complete"] and row["owner_unique"] for row in corners
    )
    need(all_faces and all_corners, "full-universe codimension owners close")
    all_margins = all(
        row["terminal_margin_certificate"]["all_required_strict_margins_complete"]
        for row in leaves
    )
    all_routes = all(row["terminal_candidate_closed"] for row in leaves)
    candidate_closed = all_routes and all_margins and all_faces and all_corners
    need(candidate_closed, "C48 task candidate closure")
    reflected_paths = {
        row["relative_path"]: row["physical_route_path"]
        for row in leaves if row["side"] == "REFLECTED"
    }
    need(reflected_paths == {
        "0": "1010001001", "10": "10100010001", "11": "10100010000"
    }, "reflected physical path pins")
    logical_leaves = logical_successor_leaves(leaves, faces, corners)
    need(
        len(logical_leaves) == 3
        and sum(Q(row["relative_fraction"]) for row in logical_leaves) == 1
        and all(len(row["physical_sides"]) == 2 for row in logical_leaves),
        "three logical two-side exits exact Kraft one",
    )
    successor = successor_checkpoint(
        c46, c41, frozen, logical_leaves
    )
    body = {
        "schema": SCHEMA,
        "status": (
            "PASS_C48_PAIR668_TWO_SIDE_ROUTE_MARGIN_AND_FULL_UNIVERSE_OWNER_"
            "CANDIDATE_CLOSED__PENDING_INDEPENDENT_AUDIT__ZERO_FORMAL_CREDIT"
        ),
        "source": {"path": str(SELF.relative_to(ROOT)), "sha256": file_sha256(SELF)},
        "frozen_inputs": {
            "C46_A_source_sha256": C46_SOURCE_SHA256,
            "C46_A_plan_object_sha256": C46_PLAN_OBJECT_SHA256,
            "C41_source_sha256": C41_SOURCE_SHA256,
            "C41_candidate_object_sha256": C41_OBJECT_SHA256,
            "C41_result_file_sha256": C41_RESULT_FILE_SHA256,
            "C41_root_manifest_file_sha256": C41_ROOT_MANIFEST_FILE_SHA256,
            "C41_ambient_ledger_file_sha256": C41_AMBIENT_LEDGER_FILE_SHA256,
            "C42_authority_seal_object_sha256": C42_SEAL_OBJECT_SHA256,
            "C47_source_sha256": C47_SOURCE_SHA256,
            "C47_report_sha256": C47_REPORT_SHA256,
        },
        "predecessor": {
            "C47_result_object_sha256": C47_RESULT_OBJECT_SHA256,
            "C47_checkpoint_object_sha256": C47_CHECKPOINT_OBJECT_SHA256,
            "C46_plan_object_sha256": C46_PLAN_OBJECT_SHA256,
            "C46_shard_index": SHARD_INDEX,
            "C46_shard_id": SHARD_ID,
            "C46_shard_task_count": SHARD_TASK_COUNT,
            "C46_shard_ordered_task_binding_sequence_sha256": (
                SHARD_BINDING_SEQUENCE_SHA256
            ),
            "C46_generation_0_checkpoint_object_sha256": (
                GENESIS_CHECKPOINT_OBJECT_SHA256
            ),
            "selected_task_index": 0,
        },
        "selection": {
            "pair_index": PAIR, "pair_owner_prerequisite_task_count": PAIR_TASK_COUNT,
            "task_id": frozen["selected"]["task_id"],
            "task_binding_sha256": TASK_BINDING,
            "ambient_cell_id": AMBIENT_ID, "primary_outer_id": PRIMARY_ID,
            "root_semantic_path": ROOT_PATH,
            "relative_frontier": list(RELATIVE_LEAVES),
            "relative_Kraft_sum_per_side": "1",
            "unblocks_sole_deficit_pairs": frozen["selected"]["queue"][
                "unblocks_sole_deficit_pairs"
            ],
        },
        "two_side_route_materialization": {
            "physical_side_count": 2, "physical_leaf_count": len(leaves),
            "representative_leaf_count": 3, "reflected_leaf_count": 3,
            "reflected_paths_derived_by_exact_child_box_matching": reflected_paths,
            "route_and_margin_rows": leaves,
            "route_row_sequence_sha256": sequence_digest(
                row["physical_leaf_id"] for row in leaves
            ),
            "all_six_routes_strict_terminal_owner_mismatch": all_routes,
            "all_six_terminal_margin_certificates_complete": all_margins,
            "reflection_involution_exact_box_checks_pass": True,
        },
        "shared_codimension_owner_ledger": {
            "universe": universe,
            "face_atom_count": len(faces),
            "face_atom_count_by_side": face_by_side,
            "target_leaf_face_atom_occurrence_count": len(leaf_face_occurrences),
            "target_leaf_face_atom_occurrence_count_by_side": leaf_face_by_side,
            "face_atoms": faces,
            "face_atom_id_sequence_sha256": sequence_digest(
                row["face_atom_id"] for row in faces
            ),
            "all_face_atoms_degree_two": all(
                row["incident_occurrence_count"] == 2 for row in faces
            ),
            "all_face_incident_sets_complete": all_faces,
            "corner_entity_count": len(corners),
            "corner_entity_count_by_side": corner_by_side,
            "target_leaf_corner_occurrence_count": leaf_corner_occurrences,
            "corner_entities": corners,
            "corner_entity_id_sequence_sha256": sequence_digest(
                row["corner_entity_id"] for row in corners
            ),
            "all_full_universe_three_way_T_junction_count": sum(
                row["junction_kind"] == "THREE_WAY_T_JUNCTION" for row in corners
            ),
            "selected_frontier_internal_three_way_T_junction_count": len(
                selected_internal_t_junctions
            ),
            "all_corner_four_quadrant_germs_complete": all_corners,
            "all_codimension_owners_unique": all_faces and all_corners,
            "formal_credit": 0,
        },
        "candidate_disposition": {
            "selected_OWNER_PREREQUISITE_task_candidate_closed": candidate_closed,
            "candidate_terminal_class": "STRICT_EXCLUDED_ON_BOTH_PHYSICAL_SIDES",
            "candidate_closed_task_count": 1,
            "candidate_closed_physical_leaf_count": 6,
            "requires_independent_C48_audit_before_any_formal_credit": True,
            "formal_credit": 0,
        },
        "successor": {
            "logical_leaf_count": len(logical_leaves),
            "leaves": logical_leaves,
            "logical_exit_id_sequence_sha256": sequence_digest(
                row["logical_exit_id"] for row in logical_leaves
            ),
            "generation_1_checkpoint": successor,
        },
        "strict_nonpromotion": {
            "runtime_write_code_path_exists": False,
            "runtime_writes_performed": False,
            "candidate_pointer_receipt_or_seal_created": False,
            "C42_C46_C47_or_canonical_modified": False,
            "D02_A_complete": False, "D02_B_complete": False,
            "D02_C_started": False, "D03_started": False,
            "CM2": "NO-GO_FOR_CLAIM", "formal_credit": 0,
        },
    }
    return {**body, "object_sha256": digest(body)}


def self_test() -> dict[str, Any]:
    tests = []
    need(digest({"b": 1, "a": 2}) == digest({"a": 2, "b": 1}),
         "canonical key order")
    tests.append("canonical JSON key order")
    need(sum((Q(1, 2), Q(1, 4), Q(1, 4)), Q(0)) == 1,
         "relative Kraft")
    tests.append("exact 0/10/11 Kraft")
    need(not any(right.startswith(left) for left in RELATIVE_LEAVES
                 for right in RELATIVE_LEAVES if left != right),
         "prefix free")
    tests.append("0/10/11 prefix free")
    need(interval_overlap(Q(0), Q(1), Q(1), Q(2)) is None,
         "corner-only overlap excluded")
    tests.append("positive-length face overlap excludes corner-only contact")
    need(interval_overlap(Q(0), Q(2), Q(1), Q(3)) == (Q(1), Q(2)),
         "positive overlap")
    tests.append("exact positive overlap")
    need(all(HEX64.fullmatch(value) for value in (
        C46_SOURCE_SHA256, C41_SOURCE_SHA256, C47_SOURCE_SHA256,
        C41_OBJECT_SHA256, C42_SEAL_OBJECT_SHA256,
    )), "pin shapes")
    tests.append("frozen SHA-256 pin shapes")
    need(PAIR == 668 and PAIR_TASK_COUNT == 43 and ROOT_PATH == "010111011",
         "selection constants")
    tests.append("pair-668 deterministic selection constants")
    body = {
        "schema": SCHEMA + ".self-test",
        "status": "PASS_C48_PURE_SELF_TEST__NO_FULL_REPLAY__ZERO_CREDIT",
        "test_count": len(tests), "tests": tests,
        "full_universe_read": False, "numerical_route_replay": False,
        "runtime_writes_performed": False, "formal_credit": 0,
    }
    return {**body, "object_sha256": digest(body)}


def emit(value: dict[str, Any]) -> None:
    sys.stdout.buffer.write(canonical(value) + b"\n")
    sys.stdout.buffer.flush()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    modes = parser.add_mutually_exclusive_group(required=True)
    modes.add_argument("--self-test", action="store_true")
    modes.add_argument("--materialize", action="store_true")
    arguments = parser.parse_args(argv)
    try:
        value = self_test() if arguments.self_test else build_result()
        emit(value)
        return 0
    except (Rejected, OSError, ValueError, KeyError, TypeError, AttributeError) as error:
        body = {
            "schema": SCHEMA + ".fail-closed-error", "status": "REJECTED",
            "error_class": type(error).__name__, "reason": str(error),
            "runtime_writes_performed": False, "formal_credit": 0,
        }
        emit({**body, "error_object_sha256": digest(body)})
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
