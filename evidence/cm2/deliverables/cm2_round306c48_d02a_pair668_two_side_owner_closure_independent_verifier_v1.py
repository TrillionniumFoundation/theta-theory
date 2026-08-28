#!/usr/bin/env python3
"""Cold, no-C48-import verifier for the C48 pair-668 closure candidate.

The verifier consumes the frozen candidate as data.  It never imports or
executes the C48 producer.  It reconstructs the selected task from C41/C46,
replays all six routes through frozen upstream numerical kernels plus the
older independent C40 implementation, rebuilds the complete two-sided C41
occurrence universe in two traversal orders, and compares exact face/corner
incidence and owner ledgers.  It also reconstructs the 514-state successor
from the immutable C46 genesis checkpoint and runs coherent mutation attacks.

It writes nothing.  Canonical audit JSON is emitted on stdout only.
"""

from __future__ import annotations

import argparse
import copy
from fractions import Fraction as Q
import hashlib
import importlib
import json
import os
from pathlib import Path
import re
import stat
import sys
from typing import Any, Iterable


if hasattr(sys, "set_int_max_str_digits"):
    sys.set_int_max_str_digits(0)
sys.dont_write_bytecode = True

SELF = Path(__file__).absolute()
ROOT = SELF.parent.parent
DELIVERABLES = ROOT / "deliverables"
RUNTIME = ROOT / ".cm2-runtime"

SCHEMA = "cm2.round306c48.d02-a-pair668-two-side-owner-closure.independent-verifier.v1"
CANDIDATE_SCHEMA = "cm2.round306c48.d02-a-pair668-two-side-owner-closure.v1"
PRODUCER = DELIVERABLES / "cm2_round306c48_d02a_pair668_two_side_owner_closure_v1.py"
DEFAULT_CANDIDATE = DELIVERABLES / "cm2_round306c48_d02a_pair668_two_side_owner_closure_result_v1.json"
PRODUCER_SHA256 = "a16d8802288c021d6d153942df15c7e7f0078628f5fb2c29eb927c6e9b94a7b8"
CANDIDATE_FILE_SHA256 = "5f356dd0b1bb9ded56548a8b046f2401ad59bf706c253d44dd151649035d283e"
CANDIDATE_OBJECT_SHA256 = "61de17d0a8122a4a03af34cf832cd717fdb715cd9c4cd2fac4162bdab8ddceab"
SUCCESSOR_OBJECT_SHA256 = "bbd909cad5a5d0b9cc44362be6acb26d527f86edc1b8191c06a246a514c9c984"

C46_NAME = "cm2_round306c46_d02a_general_adaptive_lower_strata_closure_engine_v1"
C41_NAME = "cm2_round306c41_d02_lower_strata_depth3_closure_v1"
C40_AUDIT_NAME = "cm2_round306c40_d02_h1_endpoint_collision2_arrangement_independent_auditor_v1"
C46_SOURCE = DELIVERABLES / (C46_NAME + ".py")
C41_SOURCE = DELIVERABLES / (C41_NAME + ".py")
C40_AUDIT_SOURCE = DELIVERABLES / (C40_AUDIT_NAME + ".py")
C47_SOURCE = DELIVERABLES / "cm2_round306c47_d02a_pair668_exact_route_adaptive_feasibility_spike_v1.py"
C47_REPORT = DELIVERABLES / "cm2_round306c47_d02a_pair668_exact_route_adaptive_feasibility_spike_report_v1.md"

C46_SOURCE_SHA256 = "365432e96f2c287ef3c5497b7d15e01a80775f52d8cf5b71810d6f4c0e4442ea"
C41_SOURCE_SHA256 = "3fbf6cec247903d6e6ba147d4d06e912638b1472b74adc8311323c554e6e5bde"
C40_AUDIT_SOURCE_SHA256 = "1cccec33cf7768b5797ca0b05f74812a300fb4b323859a10e9495f3e73d8a0be"
C47_SOURCE_SHA256 = "28c7eb805729f4ab8d5adaf5fac211394616877b5e08c39bd9f288c1f7640a1f"
C47_REPORT_SHA256 = "e389886d6d77e7d3ca70c821a8985bf7204458b08ddd8a1cda957c9def2b6aed"
C46_PLAN_OBJECT_SHA256 = "7d004f59282dee21a28db0cd0b727a9045f4befce207c96be4efb07d1399c9bf"
C47_RESULT_OBJECT_SHA256 = "c57bc2711dbc7dad13178643b26f5722d48db703598d3238bfd98aa254e4f9f4"
C47_CHECKPOINT_OBJECT_SHA256 = "6ed628697caf0feb81a0dc5428e1a27bf472c2ec59496556dcffa60ba5ddba5e"
C42_SEAL_OBJECT_SHA256 = "b321552768a6aeae6c1d229e52b61ca0b4420314234e02e98366153d4156d460"

C41_TOKEN = "c41-lower-strata-depth3-20260811T023804Z-f997365c91559599"
C41_DIR = RUNTIME / "candidates" / C41_TOKEN
C41_OBJECT_SHA256 = "b7e47a4ca9d6f4bb1fee10e78877850d5070f6d3c2b06bb0234fbabdaa2b7b24"
C41_RESULT_FILE_SHA256 = "73fde0eee7eb06bb0f144ea98880c72bfea36e10db696731ae72393cd9b0a50f"
C41_MANIFEST_SHA256 = "86e10532d63269cd0fdd58d541b1984522e9718f4613a5dc83211fe84eb258ba"
C41_LEDGER_SHA256 = "ea75405c8f8ba53c795c64a228aea75f9587017d93aa1cd08e73c287931e78a8"

PAIR = 668
PAIR_TASK_COUNT = 43
TASK_BINDING = "64400932860d6f224a90204e56a5614bf982eb3a1b87f37f04b86ba112a3ff9f"
ROOT_PATH = "010111011"
AMBIENT_ID = "c41-ambient:a828b4c95611e3e12ab8b3131f19f801ce8e1f1541106010ea94f34ba981a351"
PRIMARY_ID = "c41-c2-outer:4037ee276cf83fdf894f563b3967beba1dc5889764f951a8b8d2c4441b3258e4"
RELATIVE_LEAVES = ("0", "10", "11")
SHARD_INDEX = 2
SHARD_ID = "c46-d02a-shard:538ecddfbdd47c229c2e6ed2c62285bcea0b93a101832eef5ea849656c34dd28"
SHARD_TASK_COUNT = 514
SHARD_SEQUENCE_SHA256 = "1f41885b9f01cf9c086e5d547cd4878e3ad7244e8a30437611aaffc5a776b340"
GENESIS_SHA256 = "8c0029650c5dfd460e4ed721ded69e004220522bcf2c51d70859547430e018b7"

EXPECTED_BOXES = {
    ("REPRESENTATIVE", "0"): {"compact_chart": "E", "t": ["79119/256000", "31683/102400"], "p": ["-827/2048", "-413/1024"], "s": ["0", "0"]},
    ("REPRESENTATIVE", "10"): {"compact_chart": "E", "t": ["31683/102400", "1239/4000"], "p": ["-827/2048", "-1653/4096"], "s": ["0", "0"]},
    ("REPRESENTATIVE", "11"): {"compact_chart": "E", "t": ["31683/102400", "1239/4000"], "p": ["-1653/4096", "-413/1024"], "s": ["0", "0"]},
    ("REFLECTED", "0"): {"compact_chart": "E", "t": ["-31683/102400", "-79119/256000"], "p": ["413/1024", "827/2048"], "s": ["0", "0"]},
    ("REFLECTED", "10"): {"compact_chart": "E", "t": ["-1239/4000", "-31683/102400"], "p": ["1653/4096", "827/2048"], "s": ["0", "0"]},
    ("REFLECTED", "11"): {"compact_chart": "E", "t": ["-1239/4000", "-31683/102400"], "p": ["413/1024", "1653/4096"], "s": ["0", "0"]},
}
EXPECTED_PHYSICAL_PATHS = {
    ("REPRESENTATIVE", "0"): "0101110110",
    ("REPRESENTATIVE", "10"): "01011101110",
    ("REPRESENTATIVE", "11"): "01011101111",
    ("REFLECTED", "0"): "1010001001",
    ("REFLECTED", "10"): "10100010001",
    ("REFLECTED", "11"): "10100010000",
}

HEX64 = re.compile(r"[0-9a-f]{64}\Z")


class Reject(RuntimeError):
    pass


def need(condition: bool, label: str) -> None:
    if type(condition) is not bool or not condition:
        raise Reject(label)


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True, allow_nan=False).encode("ascii")


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def sequence_digest(values: Iterable[str]) -> str:
    state = hashlib.sha256()
    for value in values:
        state.update(value.encode("ascii") + b"\n")
    return state.hexdigest()


def bytes_sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def file_sha256(path: Path) -> str:
    state = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            state.update(block)
    return state.hexdigest()


def stable_read(path: Path, label: str, maximum: int = 256 << 20) -> tuple[bytes, tuple[int, ...]]:
    flags = os.O_RDONLY | getattr(os, "O_CLOEXEC", 0) | getattr(os, "O_NOFOLLOW", 0)
    fd = os.open(path, flags)
    try:
        before = os.fstat(fd)
        need(stat.S_ISREG(before.st_mode) and before.st_nlink == 1 and 0 < before.st_size <= maximum, "stable regular singleton:" + label)
        chunks = []
        remaining = before.st_size
        while remaining:
            block = os.read(fd, min(4 << 20, remaining))
            need(bool(block), "short read:" + label)
            chunks.append(block)
            remaining -= len(block)
        need(os.read(fd, 1) == b"", "stable EOF:" + label)
        after = os.fstat(fd)
    finally:
        os.close(fd)
    identity = lambda row: (row.st_dev, row.st_ino, row.st_mode, row.st_nlink, row.st_uid, row.st_gid, row.st_size, row.st_mtime_ns, row.st_ctime_ns)
    need(identity(before) == identity(after), "TOCTOU:" + label)
    return b"".join(chunks), identity(after)


def strict_json(raw: bytes, label: str) -> dict[str, Any]:
    need(not raw.startswith(b"\xef\xbb\xbf") and b"\x00" not in raw, "JSON byte hygiene:" + label)
    def pairs(items: list[tuple[str, Any]]) -> dict[str, Any]:
        output: dict[str, Any] = {}
        for key, value in items:
            need(key not in output, "duplicate JSON key:" + label + ":" + key)
            output[key] = value
        return output
    def no_number(item: str) -> Any:
        raise Reject("noninteger JSON number:" + label + ":" + item)
    value = json.loads(raw.decode("utf-8", "strict"), object_pairs_hook=pairs, parse_float=no_number, parse_constant=no_number)
    need(type(value) is dict and raw == canonical(value) + b"\n", "canonical JSON:" + label)
    return value


def closed(value: dict[str, Any], field: str, label: str, *, excluded: tuple[str, ...] = ()) -> None:
    body = dict(value)
    claimed = body.pop(field, None)
    for key in excluded:
        body.pop(key, None)
    need(type(claimed) is str and HEX64.fullmatch(claimed) is not None and claimed == digest(body), "self-hash:" + label)


def qstr(value: Q) -> str:
    return str(value)


def qpair(values: list[str]) -> tuple[Q, Q]:
    need(type(values) is list and len(values) == 2, "rational interval shape")
    result = Q(values[0]), Q(values[1])
    need(result[0] <= result[1], "ordered rational interval")
    return result


def compact_chart(cell: dict[str, Any]) -> str:
    chart = cell["gate3_chart"]
    need(type(chart) is str and chart.count(":") == 1, "Gate3 chart shape")
    result = chart.split(":", 1)[1]
    need(result in {"E", "W", "N", "S"}, "compact chart")
    return result


def frozen_snapshot() -> dict[str, str]:
    paths = {
        "producer": PRODUCER,
        "C46": C46_SOURCE,
        "C41": C41_SOURCE,
        "C40_independent": C40_AUDIT_SOURCE,
        "C47_source": C47_SOURCE,
        "C47_report": C47_REPORT,
        "C41_result": C41_DIR / "result.json",
        "C41_manifest": C41_DIR / "root_manifest.sha256",
        "C41_ambient": C41_DIR / "routed_ambient_cells.jsonl.gz",
        "C42_candidate_pointer": RUNTIME / "c42-current-token",
        "C42_audit_pointer": RUNTIME / "c42-current-audit-token",
        "C42_authority_seal": RUNTIME / "c42-current-authority-seal",
    }
    observed = {name: file_sha256(path) for name, path in paths.items()}
    need(observed == {
        "producer": PRODUCER_SHA256,
        "C46": C46_SOURCE_SHA256,
        "C41": C41_SOURCE_SHA256,
        "C40_independent": C40_AUDIT_SOURCE_SHA256,
        "C47_source": C47_SOURCE_SHA256,
        "C47_report": C47_REPORT_SHA256,
        "C41_result": C41_RESULT_FILE_SHA256,
        "C41_manifest": C41_MANIFEST_SHA256,
        "C41_ambient": C41_LEDGER_SHA256,
        "C42_candidate_pointer": "fbc5dd3c55bfdd3098ed34ae09ae633a9526a9c9cc6f40b3d87b5669b2ea7f07",
        "C42_audit_pointer": "59aca53c4c35260801b3c559648c88ee974db01ae950f045a5e5aecd64aa36e5",
        "C42_authority_seal": "0e5a76059b2c9407340d88e07f4fcc356d376f5c24b7173e6b95fd5e06bc312d",
    }, "immutable predecessor/source snapshot")
    return observed


def load_modules() -> tuple[Any, Any, Any]:
    sys.path.insert(0, str(DELIVERABLES))
    try:
        c46 = importlib.import_module(C46_NAME)
        c41 = importlib.import_module(C41_NAME)
        c40a = importlib.import_module(C40_AUDIT_NAME)
    finally:
        if sys.path and sys.path[0] == str(DELIVERABLES):
            sys.path.pop(0)
    need(Path(c46.__file__).absolute() == C46_SOURCE, "C46 import path")
    need(Path(c41.__file__).absolute() == C41_SOURCE, "C41 import path")
    need(Path(c40a.__file__).absolute() == C40_AUDIT_SOURCE, "C40 independent import path")
    return c46, c41, c40a


def load_frozen(c46: Any, c41: Any) -> dict[str, Any]:
    plan, tasks, shards = c46.build_read_only_plan(64)
    need(plan["plan_object_sha256"] == C46_PLAN_OBJECT_SHA256, "C46 plan pin")
    need(plan["authority_baseline"]["authority_seal_object_sha256"] == C42_SEAL_OBJECT_SHA256, "C42 seal binding")
    group = sorted([row for row in tasks if row["pair_index"] == PAIR and row["queue"]["priority_class"] == "OWNER_PREREQUISITE"], key=lambda row: (row["descendant_path"], row["primary_outer_id"]))
    need(len(group) == PAIR_TASK_COUNT, "pair-668 owner prerequisite count")
    selected = group[0]
    need(selected["task_binding_sha256"] == TASK_BINDING and selected["descendant_path"] == ROOT_PATH and selected["ambient_cell_id"] == AMBIENT_ID and selected["primary_outer_id"] == PRIMARY_ID, "selected task binding")
    result = c41.strict_json(C41_DIR / "result.json")
    c41.validate_object(result, C41_OBJECT_SHA256, "C41 candidate")
    ambient_rows = list(c41.iter_ledger(C41_DIR, result["ledgers"]["routed_ambient_cells"]))
    need(len(ambient_rows) == 91_879, "C41 ambient census")
    selected_rows = [row for row in ambient_rows if row["c41_ambient_cell_id"] == AMBIENT_ID]
    need(len(selected_rows) == 1 and selected_rows[0]["row_sha256"] == selected["ambient_row_sha256"], "selected ambient row")
    ambient = selected_rows[0]
    c40_dir = ROOT / result["C40_authority"]["path"]
    c40_audit = ROOT / result["C40_authority"]["independent_audit_path"]
    c40_result = c41.strict_json(c40_dir / "result.json")
    source_rows = list(c41.iter_ledger(c40_dir, c40_result["ledgers"]["routed_leaf_cells"]))
    matches = [(index, row) for index, row in enumerate(source_rows) if row["c40_leaf_id"] == ambient["c40_source_leaf_id"]]
    need(len(matches) == 1, "C40 source uniqueness")
    source_ordinal, source = matches[0]
    context = c41.load_context(c40_dir, c40_audit, formal=True)
    config = c41.decode_worker_config(context["config"])
    task = c41.task_for_row(source_ordinal, source, context)
    shard = next(row for row in shards if row["shard_index"] == SHARD_INDEX)
    need(shard["shard_id"] == SHARD_ID and shard["task_count"] == SHARD_TASK_COUNT and shard["ordered_task_binding_sequence_sha256"] == SHARD_SEQUENCE_SHA256, "shard-2 pin")
    return {"plan": plan, "tasks": tasks, "shards": shards, "selected": selected, "ambient": ambient, "ambient_rows": ambient_rows, "result": result, "source": source, "source_ordinal": source_ordinal, "context": context, "config": config, "task": task}


def box_payload(c41: Any, chart: str, box: Any) -> dict[str, Any]:
    payload = c41.box_payload(box)
    need(payload is not None, "rational physical box")
    return {"compact_chart": chart, **payload}


def physical_spec(c41: Any, frozen: dict[str, Any], side: str, relative: str) -> tuple[dict[str, Any], dict[str, Any], str, str, Any]:
    semantic = ROOT_PATH + relative
    physical = EXPECTED_PHYSICAL_PATHS[(side, relative)]
    base = frozen["task"]["c38_source"]
    pseudo = copy.deepcopy(base)
    if side == "REPRESENTATIVE":
        cell = frozen["task"]["cell"]
    else:
        need(side == "REFLECTED", "physical side")
        pseudo["representative_cell_id"] = base["reflected_cell_id"]
        pseudo["representative_origin_key"] = base["reflected_origin_key"]
        pseudo["reflected_cell_id"] = base["representative_cell_id"]
        pseudo["reflected_origin_key"] = base["representative_origin_key"]
        cell = frozen["context"]["cells"][pseudo["representative_cell_id"]]
    pseudo["path"] = physical
    task = {"task_id": "c48-route:" + side + ":" + semantic, "kind": "C1", "row": pseudo, "cell": cell}
    box, _active = c41.c39.reconstruct_box(cell, physical)
    need(box_payload(c41, compact_chart(cell), box) == EXPECTED_BOXES[(side, relative)], "hard-pinned exact leaf box:" + side + ":" + relative)
    return task, pseudo, pseudo["representative_origin_key"], physical, box


def arb_payload(c41: Any, value: Any | None) -> dict[str, Any] | None:
    return None if value is None else c41.c39.arb_payload(value)


def root_record_payload(c41: Any, record: Any) -> dict[str, Any]:
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
    r181, r178 = c41.round185.r181, c41.round185.r178
    lx, lb, ly = r181.target_affine_center(left)
    rx, rb, ry = r181.target_affine_center(right)
    dx = r181.minimum_abs_affine(lx - rx, lb - rb)
    dy = ly - ry
    distance2 = dx * dx + dy * dy
    radius = Q(r178.base.RADIUS[left[0]]) + Q(r178.base.RADIUS[right[0]])
    margin = distance2 - radius * radius
    need(margin > 0, "positive exact obstacle boundary separation")
    return {"left": left, "right": right, "minimum_center_distance_squared": qstr(distance2), "radius_sum_squared": qstr(radius * radius), "strict_squared_margin": qstr(margin)}


def expected_margin(c41: Any, cell: dict[str, Any], origin: str, box: Any, route: dict[str, Any], c2_detail: dict[str, Any], expected_owners: list[str]) -> dict[str, Any]:
    _box, active = c41.c39.reconstruct_box(cell, box.path)
    stage, records = c41.c38.round166.classify_active(cell["gate3_chart"], box, active)
    c1_rows = [root_record_payload(c41, row) for row in records]
    unresolved = [row for row in records if row.classification in {"unresolved_discriminant", "unresolved_root_sign"}]
    h1 = route["surface_evidence"]["H1"]
    c1_complete = stage.classification == "unique_first" and stage.owner_target == c41.FROZEN_OWNER and not unresolved and h1 is not None and h1["kind"] == "STRICT_SIDE" and h1["chart"] == "W" and h1["H1_centered"]["sign"] in {"POSITIVE", "NEGATIVE"}

    r178, r181, r183 = c41.round185.r178, c41.round185.r181, c41.round185.r183
    geometry = r183.collision2_geometry(r181.collision1_state_direct(origin, box))
    point_box = r181.center_box(box)
    point_geometry = r183.collision2_geometry(r181.collision1_state_direct(origin, point_box))
    point_status, selected = r178.select_owner(point_geometry, r183.CANDIDATES)
    need(point_status == "STRICT_UNIQUE_OWNER" and isinstance(selected, tuple), "strict center C2 owner")
    point_owner, point_owner_data = selected
    incumbent_kind, incumbent_data = r178.root_record(*geometry, point_owner)
    need(incumbent_kind == "STRICT_FUTURE" and incumbent_data is not None, "full-box incumbent strict future")
    point_rows = []
    full_rows = []
    for candidate in r183.CANDIDATES:
        point_kind, point_data = r178.root_record(*point_geometry, candidate)
        point_row = {"candidate": candidate, "root_kind": point_kind, "strict_gap_after_owner": None}
        if candidate != point_owner and point_kind == "STRICT_FUTURE":
            need(point_data is not None, "point competitor data")
            gap = point_data["near"] - point_owner_data["near"]
            need(bool(gap > 0), "strict point root order")
            point_row["strict_gap_after_owner"] = arb_payload(c41, gap)
        point_rows.append(point_row)
        full_kind, _full_data = r178.root_record(*geometry, candidate)
        raw = r181.raw_candidate(geometry, candidate)
        disposition = "FULL_BOX_RESOLVED_ROOT_STATUS"
        screen = None
        if candidate != point_owner and full_kind in {"UNRESOLVED_DELTA", "UNRESOLVED_ROOT_SIGN"}:
            if bool(raw["ell"] + raw["radius"] < 0):
                screen = -(raw["ell"] + raw["radius"])
                disposition = "STRICT_BEHIND_BY_UNIVERSAL_UPPER_BOUND"
            elif bool(incumbent_data["near"] < raw["ell"] - raw["radius"]):
                screen = raw["ell"] - raw["radius"] - incumbent_data["near"]
                disposition = "STRICT_LATER_BY_UNIVERSAL_LOWER_BOUND"
            else:
                disposition = "UNSCREENED_ACTIVE_COMPETITOR"
        if screen is not None:
            need(bool(screen > 0), "strict full-box screening margin")
        full_rows.append({"candidate": candidate, "root_kind": full_kind, "raw_ell": arb_payload(c41, raw["ell"]), "raw_discriminant": arb_payload(c41, raw["Delta"]), "screening_disposition": disposition, "strict_screening_margin": arb_payload(c41, screen)})
    unscreened = [row for row in full_rows if row["screening_disposition"] == "UNSCREENED_ACTIVE_COMPETITOR"]
    separations = [exact_boundary_separation(c41, point_owner, candidate) for candidate in r183.CANDIDATES if candidate != point_owner]
    c2_complete = not unscreened and c2_detail["point_owner"] == point_owner and c2_detail["absolute_collision2_owner"] == point_owner and point_owner not in expected_owners
    body = {
        "schema": CANDIDATE_SCHEMA + ".strict-terminal-margin",
        "collision1": {"whole_box_stage_classification": stage.classification, "whole_box_owner": stage.owner_target, "record_rows": c1_rows, "unresolved_record_count": len(unresolved), "H1_strict_side": h1, "complete": c1_complete},
        "collision2": {"center_point_owner_status": point_status, "center_point_owner": point_owner, "center_point_root_rows": point_rows, "full_box_incumbent_root_kind": incumbent_kind, "full_box_candidate_rows": full_rows, "unscreened_active_competitor_count": len(unscreened), "exact_boundary_separation_rows": separations, "continuation_argument": "CONNECTED_RATIONAL_BOX__STRICT_CENTER_ORDER__EVERY_UNRESOLVED_FULL_BOX_COMPETITOR_STRICTLY_SCREENED__POSITIVE_EXACT_OBSTACLE_BOUNDARY_SEPARATION_FORBIDS_ROOT_ORDER_CROSSING", "selected_absolute_owner": point_owner, "allowed_collision2_continuation_owners": expected_owners, "terminal_decision": "STRICT_COLLISION2_OWNER_MISMATCH", "complete": c2_complete},
        "all_required_strict_margins_complete": c1_complete and c2_complete,
        "formal_credit": 0,
    }
    need(c1_complete and c2_complete, "all strict terminal margins complete")
    return {**body, "margin_certificate_sha256": digest(body)}


def expected_leaves(c41: Any, c40a: Any, frozen: dict[str, Any]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    leaves = []
    independent_rows = []
    expected_owners = sorted({frozen["config"]["original_path"][1]["selected_absolute_owner_id"], frozen["config"]["reflected_path"][1]["selected_absolute_owner_id"]})
    for side in ("REPRESENTATIVE", "REFLECTED"):
        for relative in RELATIVE_LEAVES:
            task, pseudo, origin, physical, box = physical_spec(c41, frozen, side, relative)
            cell = task["cell"]
            route = c41.c39.route_c1_task(task, frozen["config"])
            need(c41.c40.collision2_safe(route, route["classification"]), "C2-safe C1 route")
            c2_status, c2_detail, c2_evidence, c2_baseline = c41.round185.resolve_dynamic_box(origin, box, frozen["config"]["pair_index"], frozen["config"]["pattern_index"])
            independent_c39, independent_c39_witness, independent_box = c40a.independent_c39_child_classification(frozen["source"], pseudo, cell, physical, frozen["config"])
            independent_c2, independent_witness = c40a.independent_c40_collision2_classification(origin, independent_box, frozen["config"])
            need(c41.box_payload(independent_box) == c41.box_payload(box), "independent reconstructed box")
            need(independent_c2 == "EXCLUDED_C40_COLLISION2_OWNER_MISMATCH", "independent terminal C2 class")
            need(independent_witness == c2_detail["absolute_collision2_owner"], "independent terminal owner")
            margin = expected_margin(c41, cell, origin, box, route, c2_detail, expected_owners)
            body = {
                "schema": CANDIDATE_SCHEMA + ".physical-leaf",
                "side": side, "pair_index": PAIR, "task_binding_sha256": TASK_BINDING,
                "relative_path": relative, "semantic_path": ROOT_PATH + relative,
                "physical_route_path": physical, "physical_cell_id": cell["cell_id"],
                "physical_origin_key": origin,
                "exact_closed_box": box_payload(c41, compact_chart(cell), box),
                "relative_parent_fraction": qstr(Q(1, 2 ** len(relative))),
                "C1_route_result": route, "C1_route_result_sha256": digest(route),
                "C2_status": c2_status, "C2_baseline": c2_baseline,
                "C2_detail": c2_detail, "C2_detail_sha256": digest(c2_detail),
                "C2_evidence": c2_evidence,
                "C2_evidence_sequence_sha256": sequence_digest(digest(row) for row in c2_evidence),
                "terminal_classification": independent_c2, "terminal_witness": independent_witness,
                "terminal_margin_certificate": margin, "terminal_candidate_closed": True,
                "formal_credit": 0,
            }
            leaf = {**body, "physical_leaf_id": "c48-leaf:" + digest(body)}
            leaves.append(leaf)
            independent_rows.append({"side": side, "relative_path": relative, "independent_C39_classification": independent_c39, "independent_C39_witness": independent_c39_witness, "independent_C40_terminal_classification": independent_c2, "independent_C40_terminal_witness": independent_witness, "exact_box_sha256": digest(body["exact_closed_box"])})
    leaves.sort(key=lambda row: (row["side"], row["relative_path"]))
    need([row["relative_path"] for row in leaves if row["side"] == "REPRESENTATIVE"] == list(RELATIVE_LEAVES), "representative prefix order")
    need(sum((Q(row["relative_parent_fraction"]) for row in leaves if row["side"] == "REPRESENTATIVE"), Q(0)) == 1, "exact representative Kraft")
    need(not any(right.startswith(left) for left in RELATIVE_LEAVES for right in RELATIVE_LEAVES if left != right), "prefix-free logical frontier")
    for relative in RELATIVE_LEAVES:
        rep = next(row for row in leaves if row["side"] == "REPRESENTATIVE" and row["relative_path"] == relative)
        ref = next(row for row in leaves if row["side"] == "REFLECTED" and row["relative_path"] == relative)
        rt0, rt1 = qpair(rep["exact_closed_box"]["t"]); rp0, rp1 = qpair(rep["exact_closed_box"]["p"])
        need(ref["exact_closed_box"] == {"compact_chart": "E", "t": [qstr(-rt1), qstr(-rt0)], "p": [qstr(-rp1), qstr(-rp0)], "s": ["0", "0"]}, "exact leaf reflection involution")
    return leaves, independent_rows


def occurrence_body(row: dict[str, Any], side: str, chart: str | None, box: dict[str, Any] | None) -> dict[str, Any]:
    return {
        "source_kind": "C41_BASELINE", "side": side, "pair_index": row["pair_index"],
        "semantic_path": row["path"], "physical_route_path": None,
        "physical_cell_id": row["representative_cell_id" if side == "REPRESENTATIVE" else "reflected_cell_id"],
        "compact_chart": chart, "exact_closed_box": box,
        "upstream_ambient_cell_id": row["c41_ambient_cell_id"],
        "upstream_ambient_row_sha256": row["row_sha256"],
        "upstream_disposition_family": row["disposition_family"],
        "replacement_leaf_id": None,
    }


def leaf_occurrence_body(leaf: dict[str, Any]) -> dict[str, Any]:
    return {
        "source_kind": "C48_REPLACEMENT", "side": leaf["side"], "pair_index": PAIR,
        "semantic_path": leaf["semantic_path"], "physical_route_path": leaf["physical_route_path"],
        "physical_cell_id": leaf["physical_cell_id"], "compact_chart": leaf["exact_closed_box"]["compact_chart"],
        "exact_closed_box": {key: leaf["exact_closed_box"][key] for key in ("t", "p", "s")},
        "upstream_ambient_cell_id": AMBIENT_ID, "upstream_ambient_row_sha256": None,
        "upstream_disposition_family": None, "replacement_leaf_id": leaf["physical_leaf_id"],
    }


def close_occurrence(body: dict[str, Any]) -> dict[str, Any]:
    binding = digest(body)
    result = {**body, "occurrence_binding_sha256": binding, "physical_occurrence_id": "c48-occurrence:" + binding}
    box = body["exact_closed_box"]
    if box is None:
        result["rational"] = False
        return result
    t0, t1 = qpair(box["t"]); p0, p1 = qpair(box["p"]); s0, s1 = qpair(box["s"])
    need(t0 < t1 and p0 < p1 and s0 == s1 == 0, "positive rational s=0 occurrence")
    result.update({"rational": True, "t0": t0, "t1": t1, "p0": p0, "p1": p1})
    return result


def build_overlay(frozen: dict[str, Any], leaves: list[dict[str, Any]], rows: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    baseline = []
    removed = []
    for row in rows:
        for side in ("REPRESENTATIVE", "REFLECTED"):
            if side == "REPRESENTATIVE":
                cell_id = row["representative_cell_id"]
                chart = compact_chart(frozen["context"]["cells"][cell_id])
                box = row["closed_representative_box"]
            else:
                original = row["closed_reflected_box"]
                chart = None if original is None else original["compact_chart"]
                box = None if original is None else {key: original[key] for key in ("t", "p", "s")}
            occurrence = close_occurrence(occurrence_body(row, side, chart, box))
            baseline.append(occurrence)
            if row["c41_ambient_cell_id"] == AMBIENT_ID:
                removed.append(occurrence["physical_occurrence_id"])
    need(len(baseline) == 183_758 and sum(row["rational"] for row in baseline) == 183_700, "baseline physical occurrence census")
    need(len(removed) == 2, "two predecessor physical occurrences")
    removed_set = set(removed)
    overlay = [row for row in baseline if row["physical_occurrence_id"] not in removed_set]
    inserted = [close_occurrence(leaf_occurrence_body(row)) for row in leaves]
    overlay.extend(inserted)
    need(len(overlay) == 183_762, "overlay physical occurrence census")
    roots = {
        "C41_ambient_row_count": 91_879,
        "baseline_physical_occurrence_count": len(baseline),
        "baseline_exact_rational_occurrence_count": sum(row["rational"] for row in baseline),
        "baseline_occurrence_binding_sequence_sha256": sequence_digest(sorted(row["occurrence_binding_sha256"] for row in baseline)),
        "removed_predecessor_occurrence_ids": sorted(removed),
        "inserted_replacement_occurrence_ids": sorted(row["physical_occurrence_id"] for row in inserted),
        "overlay_physical_occurrence_count": len(overlay),
        "overlay_occurrence_binding_sequence_sha256": sequence_digest(sorted(row["occurrence_binding_sha256"] for row in overlay)),
        "full_pinned_active_C41_universe_scanned": True,
    }
    return overlay, roots


def overlap(a0: Q, a1: Q, b0: Q, b1: Q) -> tuple[Q, Q] | None:
    low, high = max(a0, b0), min(a1, b1)
    return (low, high) if low < high else None


def leaf_faces(leaf: dict[str, Any]) -> list[dict[str, Any]]:
    box = leaf["exact_closed_box"]
    t0, t1 = qpair(box["t"]); p0, p1 = qpair(box["p"])
    return [
        {"face": "t_lower", "axis": "t", "fixed": t0, "low": p0, "high": p1},
        {"face": "t_upper", "axis": "t", "fixed": t1, "low": p0, "high": p1},
        {"face": "p_lower", "axis": "p", "fixed": p0, "low": t0, "high": t1},
        {"face": "p_upper", "axis": "p", "fixed": p1, "low": t0, "high": t1},
    ]


def face_incidence(occ: dict[str, Any], chart: str, axis: str, fixed: Q, low: Q, high: Q) -> tuple[str, tuple[Q, Q]] | None:
    if not occ["rational"] or occ["compact_chart"] != chart:
        return None
    if axis == "t":
        span = overlap(low, high, occ["p0"], occ["p1"])
        if span is None:
            return None
        directions = (["LOWER_COORDINATE_SIDE"] if occ["t1"] == fixed else []) + (["UPPER_COORDINATE_SIDE"] if occ["t0"] == fixed else [])
    else:
        span = overlap(low, high, occ["t0"], occ["t1"])
        if span is None:
            return None
        directions = (["LOWER_COORDINATE_SIDE"] if occ["p1"] == fixed else []) + (["UPPER_COORDINATE_SIDE"] if occ["p0"] == fixed else [])
    need(len(directions) <= 1, "one face side per positive box")
    return None if not directions else (directions[0], span)


def compact_incident(row: dict[str, Any], direction: str | None = None) -> dict[str, Any]:
    result = {key: row[key] for key in ("physical_occurrence_id", "occurrence_binding_sha256", "source_kind", "side", "pair_index", "semantic_path", "physical_route_path", "physical_cell_id", "replacement_leaf_id")}
    if direction is not None:
        result["geometric_side"] = direction
    return result


def unique_owner(incidents: list[dict[str, Any]]) -> tuple[dict[str, Any] | None, bool]:
    need(bool(incidents), "nonempty incidence")
    minimum = min(row["semantic_path"] for row in incidents)
    winners = [row for row in incidents if row["semantic_path"] == minimum]
    return (winners[0], True) if len(winners) == 1 else (None, False)


def build_faces(overlay: list[dict[str, Any]], leaves: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    targets = []
    for leaf in leaves:
        for face in leaf_faces(leaf):
            targets.append({**face, "chart": leaf["exact_closed_box"]["compact_chart"], "side": leaf["side"], "leaf_id": leaf["physical_leaf_id"]})
    atoms: dict[tuple[str, str, Q, Q, Q], list[dict[str, Any]]] = {}
    occurrences = []
    for target in targets:
        breaks = {target["low"], target["high"]}
        for occ in overlay:
            match = face_incidence(occ, target["chart"], target["axis"], target["fixed"], target["low"], target["high"])
            if match is not None:
                breaks.update(match[1])
        ordered = sorted(breaks)
        for low, high in zip(ordered, ordered[1:]):
            if low == high:
                continue
            key = (target["chart"], target["axis"], target["fixed"], low, high)
            ref = {"leaf_id": target["leaf_id"], "face": target["face"]}
            atoms.setdefault(key, [])
            if ref not in atoms[key]:
                atoms[key].append(ref)
            occurrences.append({"key": key, **ref})
    rows = []
    for key in sorted(atoms, key=lambda value: tuple(map(str, value))):
        chart, axis, fixed, low, high = key
        found = []
        for occ in overlay:
            match = face_incidence(occ, chart, axis, fixed, low, high)
            if match is not None and match[1][0] <= low and high <= match[1][1]:
                found.append((occ, match[0]))
        found.sort(key=lambda item: item[0]["physical_occurrence_id"])
        by_side = {direction: [row for row, observed in found if observed == direction] for direction in ("LOWER_COORDINATE_SIDE", "UPPER_COORDINATE_SIDE")}
        compact = [compact_incident(row, direction) for row, direction in found]
        owner, unique = unique_owner(compact)
        geometry = {"compact_chart": chart, "t": [qstr(fixed), qstr(fixed)] if axis == "t" else [qstr(low), qstr(high)], "p": [qstr(low), qstr(high)] if axis == "t" else [qstr(fixed), qstr(fixed)], "s": ["0", "0"]}
        body = {
            "schema": CANDIDATE_SCHEMA + ".shared-face-atom-owner",
            "canonical_entity_key": {"compact_chart": chart, "exact_closed_face_box": geometry},
            "axis": axis, "target_leaf_face_references": sorted(atoms[key], key=lambda row: (row["leaf_id"], row["face"])),
            "positive_length_face_overlap_only": True, "incident_occurrence_count": len(compact), "incident_occurrences": compact,
            "incident_occurrence_binding_sequence_sha256": sequence_digest(row["occurrence_binding_sha256"] for row in compact),
            "geometric_side_counts": {name: len(values) for name, values in by_side.items()},
            "incident_set_complete": all(len(values) == 1 for values in by_side.values()),
            "owner_rule": "UNIQUE_LEXICOGRAPHIC_MINIMUM_C41_SEMANTIC_PATH", "owner_unique": unique, "owner": owner, "formal_credit": 0,
        }
        rows.append({**body, "face_atom_id": "c48-face:" + digest(body)})
    return rows, occurrences


QUADRANTS = (("t-_p-", -1, -1), ("t-_p+", -1, 1), ("t+_p-", 1, -1), ("t+_p+", 1, 1))


def quadrants(occ: dict[str, Any], t: Q, p: Q) -> list[str]:
    if not occ["rational"]:
        return []
    output = []
    for name, tsign, psign in QUADRANTS:
        t_ok = occ["t0"] < t <= occ["t1"] if tsign < 0 else occ["t0"] <= t < occ["t1"]
        p_ok = occ["p0"] < p <= occ["p1"] if psign < 0 else occ["p0"] <= p < occ["p1"]
        if t_ok and p_ok:
            output.append(name)
    return output


def corners_of(leaf: dict[str, Any]) -> list[tuple[Q, Q]]:
    t0, t1 = qpair(leaf["exact_closed_box"]["t"]); p0, p1 = qpair(leaf["exact_closed_box"]["p"])
    return [(t0, p0), (t0, p1), (t1, p0), (t1, p1)]


def build_corners(overlay: list[dict[str, Any]], leaves: list[dict[str, Any]], faces: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], int]:
    points = set()
    for face in faces:
        box = face["canonical_entity_key"]["exact_closed_face_box"]
        chart = box["compact_chart"]
        if face["axis"] == "t":
            points.update({(chart, Q(box["t"][0]), Q(box["p"][0])), (chart, Q(box["t"][0]), Q(box["p"][1]))})
        else:
            points.update({(chart, Q(box["t"][0]), Q(box["p"][0])), (chart, Q(box["t"][1]), Q(box["p"][0]))})
    leaf_corner_count = 0
    rows = []
    for chart, t, p in sorted(points, key=lambda value: tuple(map(str, value))):
        target_boundary = []
        target_corners = []
        for leaf in leaves:
            if leaf["exact_closed_box"]["compact_chart"] != chart:
                continue
            t0, t1 = qpair(leaf["exact_closed_box"]["t"]); p0, p1 = qpair(leaf["exact_closed_box"]["p"])
            if t0 <= t <= t1 and p0 <= p <= p1 and (t in {t0, t1} or p in {p0, p1}):
                target_boundary.append(leaf["physical_leaf_id"])
            if (t, p) in corners_of(leaf):
                target_corners.append(leaf["physical_leaf_id"])
                leaf_corner_count += 1
        found = []
        qmap = {name: [] for name, _t, _p in QUADRANTS}
        for occ in overlay:
            if occ["compact_chart"] != chart:
                continue
            occupied = quadrants(occ, t, p)
            if occupied:
                found.append((occ, occupied))
                for quadrant in occupied:
                    qmap[quadrant].append(occ["physical_occurrence_id"])
        found.sort(key=lambda item: item[0]["physical_occurrence_id"])
        compact = []
        for occ, occupied in found:
            item = compact_incident(occ)
            item["occupied_quadrants"] = sorted(occupied)
            compact.append(item)
        owner, unique = unique_owner(compact)
        count = len(compact)
        kind = {3: "THREE_WAY_T_JUNCTION", 4: "FOUR_WAY_CROSS_JUNCTION", 2: "TWO_CELL_FACE_VERTEX", 1: "SINGLE_CELL_CORNER"}.get(count, "OTHER_INCIDENT_CENSUS")
        body = {
            "schema": CANDIDATE_SCHEMA + ".shared-corner-owner",
            "canonical_entity_key": {"compact_chart": chart, "exact_closed_corner_box": {"compact_chart": chart, "t": [qstr(t), qstr(t)], "p": [qstr(p), qstr(p)], "s": ["0", "0"]}},
            "junction_kind": kind, "target_leaf_boundary_occurrence_ids": sorted(target_boundary), "target_leaf_corner_occurrence_ids": sorted(target_corners),
            "incident_occurrence_count": count, "incident_occurrences": compact,
            "incident_occurrence_binding_sequence_sha256": sequence_digest(row["occurrence_binding_sha256"] for row in compact),
            "quadrant_incident_occurrence_ids": {key: sorted(values) for key, values in sorted(qmap.items())},
            "four_quadrant_germ_complete": all(len(values) == 1 for values in qmap.values()),
            "incident_set_complete": all(len(values) == 1 for values in qmap.values()),
            "owner_rule": "UNIQUE_LEXICOGRAPHIC_MINIMUM_C41_SEMANTIC_PATH", "owner_unique": unique, "owner": owner, "formal_credit": 0,
        }
        rows.append({**body, "corner_entity_id": "c48-corner:" + digest(body)})
    return rows, leaf_corner_count


def expected_owner_ledger(frozen: dict[str, Any], leaves: list[dict[str, Any]], rows: list[dict[str, Any]]) -> dict[str, Any]:
    overlay, universe = build_overlay(frozen, leaves, rows)
    faces, face_occurrences = build_faces(overlay, leaves)
    corners, leaf_corner_count = build_corners(overlay, leaves, faces)
    leaf_ids = {side: {row["physical_leaf_id"] for row in leaves if row["side"] == side} for side in ("REPRESENTATIVE", "REFLECTED")}
    face_by_side = {side: sum(any(ref["leaf_id"] in leaf_ids[side] for ref in face["target_leaf_face_references"]) for face in faces) for side in leaf_ids}
    corner_by_side = {side: sum(any(item in leaf_ids[side] for item in corner["target_leaf_boundary_occurrence_ids"]) for corner in corners) for side in leaf_ids}
    face_occ_by_side = {side: sum(row["leaf_id"] in leaf_ids[side] for row in face_occurrences) for side in leaf_ids}
    all_faces = all(row["incident_set_complete"] and row["owner_unique"] and row["incident_occurrence_count"] == 2 for row in faces)
    all_corners = all(row["incident_set_complete"] and row["owner_unique"] for row in corners)
    need(len(faces) == 20 and face_by_side == {"REPRESENTATIVE": 10, "REFLECTED": 10} and face_occ_by_side == {"REPRESENTATIVE": 13, "REFLECTED": 13}, "face atom census")
    need(len(corners) == 16 and corner_by_side == {"REPRESENTATIVE": 8, "REFLECTED": 8} and leaf_corner_count == 24, "corner census")
    selected_ids = set().union(*leaf_ids.values())
    selected_internal = [
        row for row in corners
        if row["junction_kind"] == "THREE_WAY_T_JUNCTION"
        and len(set(row["target_leaf_boundary_occurrence_ids"]) & selected_ids) == 3
    ]
    need(len(selected_internal) == 2 and all_faces and all_corners, "complete unique full-global codimension owners")
    return {
        "universe": universe,
        "face_atom_count": len(faces), "face_atom_count_by_side": face_by_side,
        "target_leaf_face_atom_occurrence_count": len(face_occurrences), "target_leaf_face_atom_occurrence_count_by_side": face_occ_by_side,
        "face_atoms": faces, "face_atom_id_sequence_sha256": sequence_digest(row["face_atom_id"] for row in faces),
        "all_face_atoms_degree_two": all(row["incident_occurrence_count"] == 2 for row in faces), "all_face_incident_sets_complete": all_faces,
        "corner_entity_count": len(corners), "corner_entity_count_by_side": corner_by_side,
        "target_leaf_corner_occurrence_count": leaf_corner_count, "corner_entities": corners,
        "corner_entity_id_sequence_sha256": sequence_digest(row["corner_entity_id"] for row in corners),
        "all_full_universe_three_way_T_junction_count": sum(row["junction_kind"] == "THREE_WAY_T_JUNCTION" for row in corners),
        "selected_frontier_internal_three_way_T_junction_count": len(selected_internal),
        "all_corner_four_quadrant_germs_complete": all_corners, "all_codimension_owners_unique": all_faces and all_corners, "formal_credit": 0,
    }


def logical_leaves(leaves: list[dict[str, Any]], ledger: dict[str, Any]) -> list[dict[str, Any]]:
    faces = ledger["face_atoms"]
    corners = ledger["corner_entities"]
    output = []
    for relative in RELATIVE_LEAVES:
        sides = []
        side_ids = set()
        for side in ("REPRESENTATIVE", "REFLECTED"):
            leaf = next(row for row in leaves if row["relative_path"] == relative and row["side"] == side)
            side_ids.add(leaf["physical_leaf_id"])
            route = {key: leaf[key] for key in ("physical_leaf_id", "side", "semantic_path", "physical_route_path", "physical_cell_id", "physical_origin_key", "exact_closed_box", "C1_route_result", "C1_route_result_sha256", "C2_status", "C2_baseline", "C2_detail", "C2_detail_sha256", "terminal_classification", "terminal_witness")}
            body = {"side": side, "independent_route": route, "strict_terminal_margin": leaf["terminal_margin_certificate"], "route_complete": leaf["terminal_candidate_closed"], "strict_terminal_margin_complete": leaf["terminal_margin_certificate"]["all_required_strict_margins_complete"], "formal_credit": 0}
            sides.append({**body, "physical_side_certificate_sha256": digest(body)})
        face_ids = sorted(row["face_atom_id"] for row in faces if any(ref["leaf_id"] in side_ids for ref in row["target_leaf_face_references"]))
        corner_ids = sorted(row["corner_entity_id"] for row in corners if any(leaf_id in side_ids for leaf_id in row["target_leaf_boundary_occurrence_ids"]))
        body = {
            "schema": CANDIDATE_SCHEMA + ".logical-exit-certificate", "task_binding_sha256": TASK_BINDING,
            "relative_path": relative, "absolute_path": ROOT_PATH + relative, "relative_fraction": qstr(Q(1, 2 ** len(relative))),
            "exit_class": "STRICT_EXCLUDED", "physical_sides": sides, "physical_side_count": 2,
            "shared_face_atom_ids": face_ids, "shared_corner_entity_ids": corner_ids,
            "all_referenced_face_incident_sets_complete": all(row["incident_set_complete"] and row["owner_unique"] for row in faces if row["face_atom_id"] in face_ids),
            "all_referenced_corner_incident_sets_complete": all(row["incident_set_complete"] and row["owner_unique"] for row in corners if row["corner_entity_id"] in corner_ids),
            "both_physical_sides_independently_routed": True, "both_physical_sides_strictly_excluded": True, "formal_credit": 0,
        }
        output.append({**body, "exit_certificate_object_sha256": digest(body), "logical_exit_id": "c48-logical-exit:" + digest(body)})
    return output


def split_events(c41: Any, frozen: dict[str, Any]) -> list[dict[str, Any]]:
    task = frozen["task"]
    source_path = frozen["source"]["path"]
    output = []
    for relative in ("", "1"):
        absolute = ROOT_PATH + relative
        bits = absolute[len(source_path):]
        box, _active = c41.c39.reconstruct_box(task["cell"], absolute)
        history = c41.exact_axis_history(task, bits)
        adjacency, _children, axis = c41.split_row(task, box, bits, len(bits), history)
        body = {
            "relative_path": relative, "absolute_path": absolute, "split_axis": ("t", "p", "s")[axis],
            "split_coordinate": adjacency["exact_split_coordinate"], "C41_split_face_adjacency": adjacency,
            "C41_split_face_adjacency_sha256": digest(adjacency),
            "oracle_adapter_source_path": str(PRODUCER.relative_to(ROOT)), "oracle_adapter_source_sha256": PRODUCER_SHA256,
            "formal_credit": 0,
        }
        need(body["split_axis"] in {"t", "p"}, "in-slice split event")
        output.append({**body, "split_event_object_sha256": digest(body)})
    return output


def successor_checkpoint(c46: Any, c41: Any, frozen: dict[str, Any], exits: list[dict[str, Any]]) -> dict[str, Any]:
    shard = next(row for row in frozen["shards"] if row["shard_index"] == SHARD_INDEX)
    need(shard["shard_id"] == SHARD_ID and len(shard["_tasks"]) == SHARD_TASK_COUNT and shard["_tasks"][0]["task_binding_sha256"] == TASK_BINDING, "internal shard selected index zero")
    genesis = c46.make_checkpoint(frozen["plan"], shard)
    need(genesis["checkpoint_object_sha256"] == GENESIS_SHA256 and len(genesis["task_states"]) == SHARD_TASK_COUNT, "genesis checkpoint pin")
    old = genesis["task_states"]
    events = split_events(c41, frozen)
    selected_body = {
        "schema": CANDIDATE_SCHEMA + ".successor-task-state", "C46_predecessor_task_state_sha256": digest(old[0]),
        "task_id": shard["_tasks"][0]["task_id"], "task_binding_sha256": TASK_BINDING, "pair_index": PAIR,
        "source_descendant_path": ROOT_PATH, "dependency_closure_sha256": shard["_tasks"][0]["dependency_closure_sha256"],
        "state": "C48_CANDIDATE_SOURCE_CLOSED_ZERO_CREDIT_PENDING_AUDIT", "frontier": [], "exits": exits,
        "split_events": events, "event_count": 5, "deepest_additional_depth": 2,
        "relative_Kraft_sum": "1", "prefix_free": True, "candidate_closed": True, "formal_closed": False,
        "credit_lock": {"ambient_credit": 0, "terminal_credit": 0, "whole_parent_credit": 0, "D02_gate_credit": 0, "formal_credit": 0},
    }
    selected = {**selected_body, "successor_task_state_sha256": digest(selected_body)}
    states = [selected, *copy.deepcopy(old[1:])]
    need(all(canonical(states[index]) == canonical(old[index]) for index in range(1, SHARD_TASK_COUNT)), "other 513 states byte immutable")
    body = {
        "schema": CANDIDATE_SCHEMA + ".generation-1-successor-checkpoint",
        "status": "C48_ONE_TASK_CANDIDATE_CLOSED__513_SHARD_TASKS_PENDING__PENDING_INDEPENDENT_AUDIT__ZERO_FORMAL_CREDIT",
        "plan_object_sha256": C46_PLAN_OBJECT_SHA256, "shard_id": SHARD_ID, "shard_index": SHARD_INDEX, "generation": 1,
        "previous_checkpoint_object_sha256": GENESIS_SHA256, "task_count": SHARD_TASK_COUNT, "selected_task_index": 0,
        "candidate_closed_task_count": 1, "formal_closed_task_count": 0, "pending_task_count": SHARD_TASK_COUNT - 1,
        "ordered_task_binding_sequence_sha256": SHARD_SEQUENCE_SHA256,
        "ordered_task_state_sequence_sha256": sequence_digest(digest(state) for state in states),
        "unchanged_indices_1_through_513_task_state_sequence_sha256": sequence_digest(digest(state) for state in old[1:]),
        "unchanged_indices_1_through_513_byte_equal_to_genesis": True, "task_states": states,
        "global_candidate_progress": {
            "frozen_C41_logical_residual_outer_row_count": 33_642,
            "frozen_C41_two_side_residual_occurrence_count": 67_284,
            "installed_C42_logical_closed_task_count": 1,
            "authoritative_logical_pending_task_count_before_C48": 33_641,
            "C48_additional_logical_candidate_closed_count_pending_audit": 1,
            "logical_pending_task_count_after_C48_candidate": 33_640,
            "two_side_pending_occurrence_count_after_C42_and_C48_candidate": 67_280,
            "coarse_formal_authority_unchanged": {"paired_coarse_cells": 574, "unresolved_coarse_cells": 1_150, "representative_parents_remaining": 575},
        },
        "credit_lock": {"ambient_credit": 0, "terminal_credit": 0, "whole_parent_credit": 0, "D02_gate_credit": 0, "formal_credit": 0},
    }
    result = {**body, "successor_checkpoint_object_sha256": digest(body), "genesis_checkpoint": genesis}
    need(result["successor_checkpoint_object_sha256"] == SUCCESSOR_OBJECT_SHA256, "successor object hard pin")
    return result


def reflected_geometry(box: dict[str, Any]) -> dict[str, Any]:
    t0, t1 = qpair(box["t"]); p0, p1 = qpair(box["p"])
    chart = box["compact_chart"]
    return {"compact_chart": chart if chart in {"E", "W"} else {"N": "S", "S": "N"}[chart], "t": [qstr(-t1), qstr(-t0)] if chart in {"E", "W"} else [qstr(t0), qstr(t1)], "p": [qstr(-p1), qstr(-p0)], "s": list(box["s"])}


def reflection_audit(ledger: dict[str, Any], leaves: list[dict[str, Any]]) -> dict[str, Any]:
    rep_ids = {row["physical_leaf_id"] for row in leaves if row["side"] == "REPRESENTATIVE"}
    ref_ids = {row["physical_leaf_id"] for row in leaves if row["side"] == "REFLECTED"}
    leaf_map = {next(row["physical_leaf_id"] for row in leaves if row["side"] == "REPRESENTATIVE" and row["relative_path"] == relative): next(row["physical_leaf_id"] for row in leaves if row["side"] == "REFLECTED" and row["relative_path"] == relative) for relative in RELATIVE_LEAVES}
    face_map = {"t_lower": "t_upper", "t_upper": "t_lower", "p_lower": "p_upper", "p_upper": "p_lower"}
    rep_faces = [row for row in ledger["face_atoms"] if any(ref["leaf_id"] in rep_ids for ref in row["target_leaf_face_references"])]
    ref_faces = [row for row in ledger["face_atoms"] if any(ref["leaf_id"] in ref_ids for ref in row["target_leaf_face_references"])]
    for row in rep_faces:
        geometry = row["canonical_entity_key"]["exact_closed_face_box"]
        mirrored = reflected_geometry(geometry)
        need(reflected_geometry(mirrored) == geometry, "face reflection involution")
        matches = [other for other in ref_faces if other["canonical_entity_key"]["exact_closed_face_box"] == mirrored]
        need(len(matches) == 1, "face reflection bijection")
        other = matches[0]
        expected_refs = sorted({(leaf_map[ref["leaf_id"]], face_map[ref["face"]]) for ref in row["target_leaf_face_references"]})
        observed_refs = sorted((ref["leaf_id"], ref["face"]) for ref in other["target_leaf_face_references"])
        need(expected_refs == observed_refs, "reflected face target references")
        need(row["owner"]["semantic_path"] == other["owner"]["semantic_path"], "reflected face owner path")
        need(sorted((item["semantic_path"], item["source_kind"]) for item in row["incident_occurrences"]) == sorted((item["semantic_path"], item["source_kind"]) for item in other["incident_occurrences"]), "reflected face incident roots")
    rep_corners = [row for row in ledger["corner_entities"] if any(item in rep_ids for item in row["target_leaf_boundary_occurrence_ids"])]
    ref_corners = [row for row in ledger["corner_entities"] if any(item in ref_ids for item in row["target_leaf_boundary_occurrence_ids"])]
    for row in rep_corners:
        geometry = row["canonical_entity_key"]["exact_closed_corner_box"]
        mirrored = reflected_geometry(geometry)
        need(reflected_geometry(mirrored) == geometry, "corner reflection involution")
        matches = [other for other in ref_corners if other["canonical_entity_key"]["exact_closed_corner_box"] == mirrored]
        need(len(matches) == 1, "corner reflection bijection")
        other = matches[0]
        need(row["owner"]["semantic_path"] == other["owner"]["semantic_path"], "reflected corner owner path")
        need(sorted((item["semantic_path"], item["source_kind"]) for item in row["incident_occurrences"]) == sorted((item["semantic_path"], item["source_kind"]) for item in other["incident_occurrences"]), "reflected corner incident roots")
    need(len(rep_faces) == len(ref_faces) == 10 and len(rep_corners) == len(ref_corners) == 8, "reflection entity census")
    return {"leaf_pairs": 3, "face_atom_pairs": 10, "corner_entity_pairs": 8, "exact_geometry_bijection": True, "involution": True, "incident_root_and_owner_path_equivariance": True}


def expected_candidate(c46: Any, c41: Any, c40a: Any, frozen: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    leaves, independent_rows = expected_leaves(c41, c40a, frozen)
    forward = expected_owner_ledger(frozen, leaves, frozen["ambient_rows"])
    reverse = expected_owner_ledger(frozen, leaves, list(reversed(frozen["ambient_rows"])))
    need(canonical(forward) == canonical(reverse), "dual-order full-universe owner replay")
    reflection = reflection_audit(forward, leaves)
    exits = logical_leaves(leaves, forward)
    successor = successor_checkpoint(c46, c41, frozen, exits)
    body = {
        "schema": CANDIDATE_SCHEMA,
        "status": "PASS_C48_PAIR668_TWO_SIDE_ROUTE_MARGIN_AND_FULL_UNIVERSE_OWNER_CANDIDATE_CLOSED__PENDING_INDEPENDENT_AUDIT__ZERO_FORMAL_CREDIT",
        "source": {"path": str(PRODUCER.relative_to(ROOT)), "sha256": PRODUCER_SHA256},
        "frozen_inputs": {
            "C46_A_source_sha256": C46_SOURCE_SHA256, "C46_A_plan_object_sha256": C46_PLAN_OBJECT_SHA256,
            "C41_source_sha256": C41_SOURCE_SHA256, "C41_candidate_object_sha256": C41_OBJECT_SHA256,
            "C41_result_file_sha256": C41_RESULT_FILE_SHA256, "C41_root_manifest_file_sha256": C41_MANIFEST_SHA256,
            "C41_ambient_ledger_file_sha256": C41_LEDGER_SHA256, "C42_authority_seal_object_sha256": C42_SEAL_OBJECT_SHA256,
            "C47_source_sha256": C47_SOURCE_SHA256, "C47_report_sha256": C47_REPORT_SHA256,
        },
        "predecessor": {
            "C47_result_object_sha256": C47_RESULT_OBJECT_SHA256, "C47_checkpoint_object_sha256": C47_CHECKPOINT_OBJECT_SHA256,
            "C46_plan_object_sha256": C46_PLAN_OBJECT_SHA256, "C46_shard_index": SHARD_INDEX, "C46_shard_id": SHARD_ID,
            "C46_shard_task_count": SHARD_TASK_COUNT, "C46_shard_ordered_task_binding_sequence_sha256": SHARD_SEQUENCE_SHA256,
            "C46_generation_0_checkpoint_object_sha256": GENESIS_SHA256, "selected_task_index": 0,
        },
        "selection": {
            "pair_index": PAIR, "pair_owner_prerequisite_task_count": PAIR_TASK_COUNT,
            "task_id": frozen["selected"]["task_id"], "task_binding_sha256": TASK_BINDING,
            "ambient_cell_id": AMBIENT_ID, "primary_outer_id": PRIMARY_ID, "root_semantic_path": ROOT_PATH,
            "relative_frontier": list(RELATIVE_LEAVES), "relative_Kraft_sum_per_side": "1",
            "unblocks_sole_deficit_pairs": frozen["selected"]["queue"]["unblocks_sole_deficit_pairs"],
        },
        "two_side_route_materialization": {
            "physical_side_count": 2, "physical_leaf_count": 6, "representative_leaf_count": 3, "reflected_leaf_count": 3,
            "reflected_paths_derived_by_exact_child_box_matching": {relative: EXPECTED_PHYSICAL_PATHS[("REFLECTED", relative)] for relative in RELATIVE_LEAVES},
            "route_and_margin_rows": leaves, "route_row_sequence_sha256": sequence_digest(row["physical_leaf_id"] for row in leaves),
            "all_six_routes_strict_terminal_owner_mismatch": True, "all_six_terminal_margin_certificates_complete": True,
            "reflection_involution_exact_box_checks_pass": True,
        },
        "shared_codimension_owner_ledger": forward,
        "candidate_disposition": {
            "selected_OWNER_PREREQUISITE_task_candidate_closed": True,
            "candidate_terminal_class": "STRICT_EXCLUDED_ON_BOTH_PHYSICAL_SIDES",
            "candidate_closed_task_count": 1, "candidate_closed_physical_leaf_count": 6,
            "requires_independent_C48_audit_before_any_formal_credit": True, "formal_credit": 0,
        },
        "successor": {"logical_leaf_count": 3, "leaves": exits, "logical_exit_id_sequence_sha256": sequence_digest(row["logical_exit_id"] for row in exits), "generation_1_checkpoint": successor},
        "strict_nonpromotion": {
            "runtime_write_code_path_exists": False, "runtime_writes_performed": False,
            "candidate_pointer_receipt_or_seal_created": False, "C42_C46_C47_or_canonical_modified": False,
            "D02_A_complete": False, "D02_B_complete": False, "D02_C_started": False, "D03_started": False,
            "CM2": "NO-GO_FOR_CLAIM", "formal_credit": 0,
        },
    }
    expected = {**body, "object_sha256": digest(body)}
    need(expected["object_sha256"] == CANDIDATE_OBJECT_SHA256, "independent candidate object hard pin")
    details = {"independent_route_rows": independent_rows, "reflection": reflection, "dual_owner_traversal_order_equal": True, "ambient_rows_per_traversal": 91_879, "physical_occurrences_per_baseline_traversal": 183_758, "overlay_occurrences_per_traversal": 183_762}
    return expected, details


def audit_nested_hashes(candidate: dict[str, Any]) -> int:
    checks = 0
    for leaf in candidate["two_side_route_materialization"]["route_and_margin_rows"]:
        need(leaf["C1_route_result_sha256"] == digest(leaf["C1_route_result"]), "C1 route hash")
        need(leaf["C2_detail_sha256"] == digest(leaf["C2_detail"]), "C2 detail hash")
        need(leaf["C2_evidence_sequence_sha256"] == sequence_digest(digest(row) for row in leaf["C2_evidence"]), "C2 evidence sequence")
        closed(leaf["terminal_margin_certificate"], "margin_certificate_sha256", "terminal margin")
        body = dict(leaf); claimed = body.pop("physical_leaf_id")
        need(claimed == "c48-leaf:" + digest(body), "physical leaf ID closure")
        checks += 5
    ledger = candidate["shared_codimension_owner_ledger"]
    for row in ledger["face_atoms"]:
        body = dict(row); claimed = body.pop("face_atom_id")
        need(claimed == "c48-face:" + digest(body), "face atom ID closure")
        checks += 1
    for row in ledger["corner_entities"]:
        body = dict(row); claimed = body.pop("corner_entity_id")
        need(claimed == "c48-corner:" + digest(body), "corner entity ID closure")
        checks += 1
    for row in candidate["successor"]["leaves"]:
        body = dict(row); logical_id = body.pop("logical_exit_id"); claimed = body.pop("exit_certificate_object_sha256")
        need(claimed == digest(body) and logical_id == "c48-logical-exit:" + digest(body), "logical exit closure")
        for side in row["physical_sides"]:
            side_body = dict(side); side_claimed = side_body.pop("physical_side_certificate_sha256")
            need(side_claimed == digest(side_body), "physical side certificate closure")
            checks += 1
        checks += 1
    checkpoint = candidate["successor"]["generation_1_checkpoint"]
    checkpoint_body = dict(checkpoint); checkpoint_body.pop("genesis_checkpoint"); claimed = checkpoint_body.pop("successor_checkpoint_object_sha256")
    need(claimed == digest(checkpoint_body), "successor checkpoint closure")
    genesis = checkpoint["genesis_checkpoint"]
    closed(genesis, "checkpoint_object_sha256", "genesis checkpoint")
    selected = checkpoint["task_states"][0]
    closed(selected, "successor_task_state_sha256", "selected successor state")
    for event in selected["split_events"]:
        closed(event, "split_event_object_sha256", "split event")
        checks += 1
    return checks + 3


def static_guard(candidate: dict[str, Any], expected: dict[str, Any]) -> None:
    closed(candidate, "object_sha256", "candidate top")
    need(canonical(candidate) == canonical(expected), "full independent semantic projection")


def set_path(value: dict[str, Any], path: tuple[Any, ...], replacement: Any) -> None:
    cursor: Any = value
    for key in path[:-1]:
        cursor = cursor[key]
    cursor[path[-1]] = replacement


def run_attacks(candidate: dict[str, Any], expected: dict[str, Any]) -> dict[str, Any]:
    attacks: list[tuple[str, tuple[Any, ...], Any]] = [
        ("schema substitution", ("schema",), CANDIDATE_SCHEMA + ".evil"),
        ("PASS status substitution", ("status",), "PASS_UNBOUND"),
        ("producer source drift", ("source", "sha256"), "0" * 64),
        ("C41 predecessor drift", ("frozen_inputs", "C41_source_sha256"), "1" * 64),
        ("C47 checkpoint drift", ("predecessor", "C47_checkpoint_object_sha256"), "2" * 64),
        ("pair substitution", ("selection", "pair_index"), 669),
        ("root path substitution", ("selection", "root_semantic_path"), ROOT_PATH + "0"),
        ("non-prefix frontier", ("selection", "relative_frontier"), ["0", "01", "1"]),
        ("physical side swap", ("two_side_route_materialization", "route_and_margin_rows", 0, "side"), "REPRESENTATIVE"),
        ("relative path drift", ("two_side_route_materialization", "route_and_margin_rows", 0, "relative_path"), "00"),
        ("reflected route path drift", ("two_side_route_materialization", "route_and_margin_rows", 0, "physical_route_path"), "1010001000"),
        ("exact box endpoint drift", ("two_side_route_materialization", "route_and_margin_rows", 0, "exact_closed_box", "t", 0), "-1"),
        ("C2 owner drift", ("two_side_route_materialization", "route_and_margin_rows", 0, "C2_detail", "absolute_collision2_owner"), "G[0,0]"),
        ("terminal margin deletion", ("two_side_route_materialization", "route_and_margin_rows", 0, "terminal_margin_certificate", "all_required_strict_margins_complete"), False),
        ("face atom census drift", ("shared_codimension_owner_ledger", "face_atom_count"), 19),
        ("face incidence deletion", ("shared_codimension_owner_ledger", "face_atoms", 0, "incident_occurrence_count"), 1),
        ("face owner substitution", ("shared_codimension_owner_ledger", "face_atoms", 0, "owner", "semantic_path"), "9"),
        ("unatomized face geometry", ("shared_codimension_owner_ledger", "face_atoms", 0, "canonical_entity_key", "exact_closed_face_box", "p", 1), "1"),
        ("corner census drift", ("shared_codimension_owner_ledger", "corner_entity_count"), 15),
        ("corner quadrant deletion", ("shared_codimension_owner_ledger", "corner_entities", 0, "four_quadrant_germ_complete"), False),
        ("owner uniqueness forgery", ("shared_codimension_owner_ledger", "all_codimension_owners_unique"), False),
        ("candidate closure forgery", ("candidate_disposition", "selected_OWNER_PREREQUISITE_task_candidate_closed"), False),
        ("logical leaf census drift", ("successor", "logical_leaf_count"), 2),
        ("logical terminal substitution", ("successor", "leaves", 0, "exit_class"), "CONNECTED_TO_KNOWN"),
        ("shard pending off-by-one", ("successor", "generation_1_checkpoint", "pending_task_count"), 514),
        ("global pending off-by-one", ("successor", "generation_1_checkpoint", "global_candidate_progress", "logical_pending_task_count_after_C48_candidate"), 33_641),
        ("unchanged genesis state mutation", ("successor", "generation_1_checkpoint", "task_states", 1, "state"), "CLOSED"),
        ("formal credit escalation", ("successor", "generation_1_checkpoint", "credit_lock", "formal_credit"), 1),
        ("CM2 promotion forgery", ("strict_nonpromotion", "CM2"), "CLAIM_CANDIDATE"),
        ("runtime write forgery", ("strict_nonpromotion", "runtime_writes_performed"), True),
    ]
    passed = []
    for name, path, replacement in attacks:
        mutated = copy.deepcopy(candidate)
        set_path(mutated, path, replacement)
        mutated.pop("object_sha256", None)
        mutated["object_sha256"] = digest(mutated)
        rejected = False
        try:
            static_guard(mutated, expected)
        except Reject:
            rejected = True
        need(rejected, "attack accepted:" + name)
        passed.append(name)
    malformed = canonical(candidate).replace(b'{"candidate_disposition":', b'{"schema":"duplicate","candidate_disposition":', 1) + b"\n"
    try:
        strict_json(malformed, "duplicate-key-attack")
        raise Reject("duplicate-key attack accepted")
    except (Reject, json.JSONDecodeError):
        passed.append("duplicate JSON key")
    noncanonical = json.dumps(candidate, sort_keys=False, ensure_ascii=True).encode("ascii") + b"\n"
    try:
        strict_json(noncanonical, "noncanonical-attack")
        raise Reject("noncanonical JSON attack accepted")
    except Reject:
        passed.append("noncanonical JSON bytes")
    return {"attack_count": len(passed), "all_fail_closed": True, "top_hash_reclosed_mutation_count": len(attacks), "attacks": passed}


def verify(candidate: dict[str, Any], c46: Any, c41: Any, c40a: Any, frozen: dict[str, Any]) -> dict[str, Any]:
    expected, details = expected_candidate(c46, c41, c40a, frozen)
    static_guard(candidate, expected)
    need(candidate["object_sha256"] == CANDIDATE_OBJECT_SHA256, "candidate object pin")
    nested = audit_nested_hashes(candidate)
    attacks = run_attacks(candidate, expected)
    return {"nested_self_hash_check_count": nested, "cold_replay": details, "attacks": attacks}


def self_test() -> dict[str, Any]:
    tests = []
    need(digest({"b": 1, "a": 2}) == digest({"a": 2, "b": 1}), "canonical order")
    tests.append("canonical key order")
    need(sum((Q(1, 2), Q(1, 4), Q(1, 4)), Q(0)) == 1, "Kraft")
    tests.append("exact Kraft")
    need(not any(right.startswith(left) for left in RELATIVE_LEAVES for right in RELATIVE_LEAVES if left != right), "prefix free")
    tests.append("prefix-free frontier")
    need(overlap(Q(0), Q(1), Q(1), Q(2)) is None, "corner-only is not face")
    tests.append("positive-length face semantics")
    for box in EXPECTED_BOXES.values():
        need(reflected_geometry(reflected_geometry(box)) == box, "box reflection involution")
    tests.append("reflection involution")
    need(all(HEX64.fullmatch(value) for value in (PRODUCER_SHA256, CANDIDATE_OBJECT_SHA256, SUCCESSOR_OBJECT_SHA256, C41_LEDGER_SHA256)), "pin shapes")
    tests.append("SHA-256 pin shapes")
    body = {"schema": SCHEMA + ".self-test", "status": "PASS_C48_INDEPENDENT_VERIFIER_PURE_SELF_TEST", "test_count": len(tests), "tests": tests, "runtime_writes_performed": False, "formal_credit": 0}
    return {**body, "object_sha256": digest(body)}


def emit(value: dict[str, Any]) -> None:
    sys.stdout.buffer.write(canonical(value) + b"\n")
    sys.stdout.buffer.flush()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    modes = parser.add_mutually_exclusive_group(required=True)
    modes.add_argument("--self-test", action="store_true")
    modes.add_argument("--verify", action="store_true")
    parser.add_argument("--candidate", type=Path, default=DEFAULT_CANDIDATE)
    args = parser.parse_args(argv)
    try:
        if args.self_test:
            emit(self_test())
            return 0
        before = frozen_snapshot()
        raw, identity_before = stable_read(args.candidate.absolute(), "C48 candidate")
        need(bytes_sha256(raw) == CANDIDATE_FILE_SHA256, "candidate file SHA-256")
        candidate = strict_json(raw, "C48 candidate")
        c46, c41, c40a = load_modules()
        frozen = load_frozen(c46, c41)
        result = verify(candidate, c46, c41, c40a, frozen)
        raw_after, identity_after = stable_read(args.candidate.absolute(), "C48 candidate stable reread")
        need(raw_after == raw and identity_after == identity_before, "candidate terminal-byte/identity replay")
        after = frozen_snapshot()
        need(after == before, "predecessor/source immutability across audit")
        body = {
            "schema": SCHEMA,
            "status": "PASS_INDEPENDENT_C48_PAIR668_TWO_SIDE_ROUTE_MARGIN_FULL_GLOBAL_OWNER_AND_GEN1_SUCCESSOR_AUDIT__ZERO_FORMAL_CREDIT",
            "verifier": {"path": str(SELF.relative_to(ROOT)), "sha256": file_sha256(SELF)},
            "candidate": {"path": str(args.candidate.absolute().relative_to(ROOT)), "file_sha256": CANDIDATE_FILE_SHA256, "object_sha256": CANDIDATE_OBJECT_SHA256, "successor_checkpoint_object_sha256": SUCCESSOR_OBJECT_SHA256},
            "independence_boundary": {"C48_producer_imported_or_executed": False, "C48_producer_decision_function_called": False, "frozen_upstream_C41_C46_kernels_used_for_exact_replay": True, "older_no_C40_producer_import_independent_numeric_implementation_used": True, "full_C41_occurrence_universe_reconstructed_twice": True, "candidate_shape_or_hash_alone_grants_credit": False},
            "route_replay": {"physical_side_count": 2, "physical_leaf_count": 6, "strict_terminal_margin_count": 6, "relative_frontier": list(RELATIVE_LEAVES), "relative_Kraft_sum": "1", "prefix_free": True, "all_terminal_classifications": "EXCLUDED_C40_COLLISION2_OWNER_MISMATCH", "rows": result["cold_replay"]["independent_route_rows"]},
            "owner_replay": {key: value for key, value in result["cold_replay"].items() if key != "independent_route_rows"},
            "nested_self_hash_check_count": result["nested_self_hash_check_count"],
            "successor_replay": {"shard_index": SHARD_INDEX, "task_count": SHARD_TASK_COUNT, "selected_task_index": 0, "unchanged_other_state_count": 513, "candidate_closed_task_count": 1, "formal_closed_task_count": 0, "logical_pending_after_candidate": 33_640, "successor_checkpoint_object_sha256": SUCCESSOR_OBJECT_SHA256},
            "attacks": result["attacks"],
            "immutability": {"pre_and_post_snapshot_equal": True, "frozen_file_count": len(before), "snapshot_sha256": digest(before), "candidate_terminal_byte_replay_equal": True, "candidate_identity_replay_equal": True},
            "strict_nonpromotion": {"candidate_pointer_receipt_or_seal_created": False, "runtime_writes_performed": False, "D02_A_complete": False, "D02_B_complete": False, "D02_C_started": False, "D03_started": False, "CM2": "NO-GO_FOR_CLAIM", "formal_credit": 0},
            "formal_credit": 0,
        }
        emit({**body, "object_sha256": digest(body)})
        return 0
    except (Reject, OSError, ValueError, KeyError, TypeError, AttributeError, ImportError) as error:
        body = {"schema": SCHEMA + ".fail-closed", "status": "REJECTED", "error_class": type(error).__name__, "reason": str(error), "runtime_writes_performed": False, "formal_credit": 0}
        emit({**body, "object_sha256": digest(body)})
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
