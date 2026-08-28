#!/usr/bin/env python3
"""Cold independent numeric verifier for the two C51 pair-1 route tasks.

This verifier never imports or executes either the C51 route-probe producer or
the C48 closure producer.  It selects the two tasks from the frozen C46 plan,
loads the frozen C41/C32 authority chain, derives reflected physical paths by
exact child-box matching, and performs a second numerical replay through the
C40 independent auditor.  It rebuilds the adaptive frontiers, all C1/C2
strict-margin certificates, reflection, split decisions, prefix freedom and
Kraft conservation.  The C50a pair-1 owner candidate is consumed as data and
its embedded request is compared with the independent replay.

The program writes nothing.  Canonical, self-hashed JSON is emitted on stdout.
"""

from __future__ import annotations

import argparse
import ast
import base64
import copy
from fractions import Fraction as Q
import gzip
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

SCHEMA = "cm2.round306c52.d02-a-pair1-no-producer-cold-route-audit.v1"
C51_SCHEMA = "cm2.round306c51.d02-a-pair1-two-task-route-probe.v1"
C48_SCHEMA = "cm2.round306c48.d02-a-pair668-two-side-owner-closure.v1"
C50A_SCHEMA = "cm2.round306c50a.global-codimension-owner-oracle.v1"

C51_SOURCE = DELIVERABLES / "cm2_round306c51_d02a_pair1_two_task_route_probe_v1.py"
C51_REPORT = DELIVERABLES / "cm2_round306c51_d02a_pair1_two_task_route_probe_report_v1.md"
C51_SOURCE_SHA256 = "caf043d2a475f8c25e92785587db971a0d33242b8560dd096f09a1e5c6e72069"
C51_REPORT_SHA256 = "d2330ac69da6cdb0e3fa092c9b697c836a21026ebb52b9b3655f9487a88f6330"
C51_OBJECT_SHA256 = "187344a3c524dce1898151bf64f507c181dde137a3710eb9bc5cd1b895a81f6e"
C48_SOURCE = DELIVERABLES / "cm2_round306c48_d02a_pair668_two_side_owner_closure_v1.py"
C48_SOURCE_SHA256 = "a16d8802288c021d6d153942df15c7e7f0078628f5fb2c29eb927c6e9b94a7b8"

C46_NAME = "cm2_round306c46_d02a_general_adaptive_lower_strata_closure_engine_v1"
C41_NAME = "cm2_round306c41_d02_lower_strata_depth3_closure_v1"
C40I_NAME = "cm2_round306c40_d02_h1_endpoint_collision2_arrangement_independent_auditor_v1"
C46_SOURCE = DELIVERABLES / (C46_NAME + ".py")
C41_SOURCE = DELIVERABLES / (C41_NAME + ".py")
C40I_SOURCE = DELIVERABLES / (C40I_NAME + ".py")
C32_SOURCE = DELIVERABLES / "cm2_round306c32_d02_four_chart_compact_atlas_cell_ledger_v1.py"
C46_SOURCE_SHA256 = "365432e96f2c287ef3c5497b7d15e01a80775f52d8cf5b71810d6f4c0e4442ea"
C41_SOURCE_SHA256 = "3fbf6cec247903d6e6ba147d4d06e912638b1472b74adc8311323c554e6e5bde"
C40I_SOURCE_SHA256 = "1cccec33cf7768b5797ca0b05f74812a300fb4b323859a10e9495f3e73d8a0be"
C32_SOURCE_SHA256 = "fce41ccd6a6d99611e8afe4bb799afbe99f3090d751f0c8e8de929bec7cc8d37"
C46_PLAN_OBJECT_SHA256 = "7d004f59282dee21a28db0cd0b727a9045f4befce207c96be4efb07d1399c9bf"

C32_DIR = RUNTIME / "candidates/c32-four-chart-atlas-20260810T133217Z-3c4d0dff259783c9"
C41_DIR = RUNTIME / "candidates/c41-lower-strata-depth3-20260811T023804Z-f997365c91559599"
C32_OBJECT_SHA256 = "32ff9e0f90a12f17b16f67086eabda0986a0d52d185bea0c5c16e20518ca1474"
C41_OBJECT_SHA256 = "b7e47a4ca9d6f4bb1fee10e78877850d5070f6d3c2b06bb0234fbabdaa2b7b24"
FROZEN_FILES = {
    C32_DIR / "result.json": "c2abba977fa21ea965a9d77478df391db496d0e03f60320b9a4adf9005f1a0a4",
    C32_DIR / "root_manifest.sha256": "4af827cfec996f62443b9ef38ea71cd341873de58b9b04cedfcd8faaca70a8e1",
    C32_DIR / "compact_cells.jsonl.gz": "3e330d63cce3a2c9f43551ee882102bd10f706daab2edc00674432561a62f5d8",
    C41_DIR / "result.json": "73fde0eee7eb06bb0f144ea98880c72bfea36e10db696731ae72393cd9b0a50f",
    C41_DIR / "root_manifest.sha256": "86e10532d63269cd0fdd58d541b1984522e9718f4613a5dc83211fe84eb258ba",
    C41_DIR / "routed_ambient_cells.jsonl.gz": "ea75405c8f8ba53c795c64a228aea75f9587017d93aa1cd08e73c287931e78a8",
}

DEFAULT_CANDIDATE = DELIVERABLES / "cm2_round306c50a_pair1_two_task_global_owner_full_candidate_v1.json.gz.b64"
C50A_CANDIDATE_BUNDLE_SHA256 = "3a747cc92700bccc763d6cbf71ece51ebf5d3f5709b330a768c089099025174a"
C50A_CANDIDATE_FILE_SHA256 = "0c3ffd0a9ff26fd128366a6af22aabeb29f72346303988deb4773b5adcd4131e"
C50A_CANDIDATE_OBJECT_SHA256 = "da4557c64b4ce9675a3f8bff8a250b7ec7b643c48aecd738c03b7abed01d0b82"
C50A_REQUEST_OBJECT_SHA256 = "db6292e002ec3c0b810f74af192524407afb1cfa3566c4898aa7fa7b2a8e3496"
C50A_INDEPENDENT_AUDIT_OBJECT_SHA256 = "c037b3b15d19b839a254e3122bce7b1f882f6f9e198638c50a08909bf71231d6"

PAIR = 1
EXPECTED_SHARD_INDEX = 9
EXPECTED_TASK_INDICES = (0, 1)
EXPECTED_TASKS = (
    {
        "task_binding_sha256": "daada4d9fd48677629cbfa9872b073d5fdf1552b115bf94438e7357f9a5dd95b",
        "root_path": "111111110",
        "ambient_cell_id": "c41-ambient:1610ea6d1bc40ef5eed6614db0e25e77ba374850efaec77964a50520b77c1b09",
        "primary_outer_id": "c41-c2-outer:d3762e8c71c9bbb8bd9863d3d47c2a92b380ba5f3ca776509d7cdb2da820ca54",
        "frontier": ("0", "1"),
    },
    {
        "task_binding_sha256": "e37b527423ad1aabba7485faacd03f7bb95ba9d79caebd614fb63d38ccd8dac6",
        "root_path": "111111111",
        "ambient_cell_id": "c41-ambient:bb566b646775f7e2599e0277e84cdfe1e2222371d9c6ccfc5d50a42ec9c663db",
        "primary_outer_id": "c41-c2-outer:f74b3ca3b825776480ebc1ed9f210bcd710ca29dd59c7e7700590c8092d4aaf7",
        "frontier": ("00", "01", "10", "110", "1110", "11110", "11111"),
    },
)

HEX64 = re.compile(r"[0-9a-f]{64}\Z")
FORBIDDEN_MODULES = {
    C51_SOURCE.stem,
    C48_SOURCE.stem,
}


class Rejected(RuntimeError):
    """Fail-closed independent verification rejection."""


def need(condition: bool, label: str) -> None:
    if type(condition) is not bool or not condition:
        raise Rejected(label)


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=True, allow_nan=False).encode("ascii")


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def sequence_digest(values: Iterable[str]) -> str:
    state = hashlib.sha256()
    for value in values:
        need(type(value) is str, "sequence digest string")
        state.update(value.encode("ascii") + b"\n")
    return state.hexdigest()


def file_sha256(path: Path) -> str:
    state = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            state.update(block)
    return state.hexdigest()


def stable_read(path: Path, label: str, maximum: int = 64 << 20) -> bytes:
    flags = os.O_RDONLY | getattr(os, "O_CLOEXEC", 0) | getattr(os, "O_NOFOLLOW", 0)
    fd = os.open(path, flags)
    try:
        before = os.fstat(fd)
        need(stat.S_ISREG(before.st_mode) and before.st_nlink == 1,
             "regular singleton:" + label)
        need(0 < before.st_size <= maximum, "bounded file:" + label)
        pieces: list[bytes] = []
        remaining = before.st_size
        while remaining:
            piece = os.read(fd, min(2 << 20, remaining))
            need(bool(piece), "short read:" + label)
            pieces.append(piece)
            remaining -= len(piece)
        need(os.read(fd, 1) == b"", "stable EOF:" + label)
        after = os.fstat(fd)
    finally:
        os.close(fd)
    identity = lambda row: (
        row.st_dev, row.st_ino, row.st_mode, row.st_nlink, row.st_uid,
        row.st_gid, row.st_size, row.st_mtime_ns, row.st_ctime_ns,
    )
    need(identity(before) == identity(after), "TOCTOU:" + label)
    return b"".join(pieces)


def strict_json(raw: bytes, label: str, *, canonical_line: bool = True) -> dict[str, Any]:
    need(not raw.startswith(b"\xef\xbb\xbf") and b"\x00" not in raw,
         "JSON byte hygiene:" + label)

    def pairs(items: list[tuple[str, Any]]) -> dict[str, Any]:
        output: dict[str, Any] = {}
        for key, value in items:
            need(key not in output, "duplicate JSON key:" + label + ":" + key)
            output[key] = value
        return output

    def no_number(token: str) -> Any:
        raise Rejected("noninteger JSON number:" + label + ":" + token)

    value = json.loads(raw.decode("utf-8", "strict"), object_pairs_hook=pairs,
                       parse_float=no_number, parse_constant=no_number)
    need(type(value) is dict, "JSON top object:" + label)
    expected = canonical(value) + (b"\n" if canonical_line else b"")
    need(raw == expected, "canonical JSON bytes:" + label)
    return value


def candidate_bytes(path: Path) -> tuple[bytes, dict[str, Any]]:
    """Read either the immutable base64/gzip bundle or raw canonical JSON."""
    stored = stable_read(path.absolute(), "C50a pair1 candidate bundle")
    stored_hash = hashlib.sha256(stored).hexdigest()
    if path.name.endswith(".json.gz.b64"):
        need(stored_hash == C50A_CANDIDATE_BUNDLE_SHA256,
             "C50a immutable candidate bundle pin")
        try:
            need(stored.endswith(b"\n") and b"\n" not in stored[:-1]
                 and b"\r" not in stored, "canonical one-line base64 bundle")
            packed = base64.b64decode(stored[:-1], validate=True)
            raw = gzip.decompress(packed)
        except (ValueError, gzip.BadGzipFile, EOFError) as error:
            raise Rejected("C50a candidate bundle decode:" + str(error)) from error
    else:
        raw = stored
    need(hashlib.sha256(raw).hexdigest() == C50A_CANDIDATE_FILE_SHA256,
         "C50a decompressed canonical candidate file pin")
    return raw, {"stored_path": str(path.absolute().relative_to(ROOT)),
                 "stored_file_sha256": stored_hash,
                 "canonical_json_sha256": hashlib.sha256(raw).hexdigest()}


def closed(value: dict[str, Any], field: str, label: str) -> None:
    body = dict(value)
    claimed = body.pop(field, None)
    need(type(claimed) is str and HEX64.fullmatch(claimed) is not None
         and claimed == digest(body), "self hash:" + label)


def qstr(value: Q) -> str:
    return str(value)


def prefix_free(paths: list[str]) -> bool:
    return len(paths) == len(set(paths)) and not any(
        right.startswith(left) for left in paths for right in paths
        if left != right
    )


def compact_chart(cell: dict[str, Any]) -> str:
    value = cell["gate3_chart"]
    need(type(value) is str and value.count(":") == 1, "Gate3 chart shape")
    chart = value.split(":", 1)[1]
    need(chart in {"E", "W", "N", "S"}, "compact chart enum")
    return chart


def box_payload(c41: Any, chart: str, box: Any) -> dict[str, Any]:
    payload = c41.box_payload(box)
    need(payload is not None, "rational physical box")
    return {"compact_chart": chart, **payload}


def interval(raw: list[str], label: str) -> tuple[Q, Q]:
    need(type(raw) is list and len(raw) == 2, "interval shape:" + label)
    values = Q(raw[0]), Q(raw[1])
    need(values[0] <= values[1], "interval order:" + label)
    return values


def source_independence_check() -> dict[str, Any]:
    source = stable_read(SELF, "C52 verifier source", 4 << 20)
    tree = ast.parse(source.decode("utf-8", "strict"), filename=str(SELF))
    imported: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imported.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            imported.add(node.module)
        elif isinstance(node, ast.Dict):
            literal_keys = [key.value for key in node.keys
                            if isinstance(key, ast.Constant)
                            and isinstance(key.value, (str, int))]
            need(len(literal_keys) == len(set(literal_keys)),
                 "duplicate literal key in verifier source")
    need(not any(name in imported for name in FORBIDDEN_MODULES),
         "forbidden C51/C48 static import")
    need(not (FORBIDDEN_MODULES & set(sys.modules)),
         "forbidden C51/C48 already imported")
    return {
        "C51_producer_imported_or_executed": False,
        "C48_producer_imported_or_executed": False,
        "source_ast_import_scan_pass": True,
        "source_ast_duplicate_literal_key_scan_pass": True,
        "forbidden_modules_absent_from_sys_modules": True,
    }


def frozen_snapshot() -> dict[str, str]:
    pins = {
        C46_SOURCE: C46_SOURCE_SHA256,
        C41_SOURCE: C41_SOURCE_SHA256,
        C40I_SOURCE: C40I_SOURCE_SHA256,
        C32_SOURCE: C32_SOURCE_SHA256,
        C51_SOURCE: C51_SOURCE_SHA256,
        C51_REPORT: C51_REPORT_SHA256,
        C48_SOURCE: C48_SOURCE_SHA256,
        **FROZEN_FILES,
    }
    observed = {
        str(path.relative_to(ROOT)): hashlib.sha256(stable_read(
            path, "frozen snapshot:" + str(path.relative_to(ROOT)))).hexdigest()
        for path in pins
    }
    need(observed == {str(path.relative_to(ROOT)): value
                      for path, value in pins.items()},
         "frozen source/authority byte snapshot")
    for path, expected in ((C32_DIR / "result.json", C32_OBJECT_SHA256),
                           (C41_DIR / "result.json", C41_OBJECT_SHA256)):
        value = strict_json(stable_read(path, "authority result"),
                            "authority result", canonical_line=True)
        closed(value, "object_sha256", "authority result")
        need(value["object_sha256"] == expected, "authority object pin")
    return observed


def require_snapshot_equal(before: dict[str, str], after: dict[str, str],
                           label: str) -> None:
    need(before == after, "pre/post stable snapshot equality:" + label)


def modeled_snapshot_attacks(snapshot: dict[str, str]) -> list[dict[str, Any]]:
    """Coherent in-memory models for source swap and late mutation.

    These tests do not touch an authority file.  They exercise the same exact
    equality guard used around imports and the complete numerical replay.
    """
    output = []
    for name, mutate in (
        ("coherent_source_swap", lambda row: row.__setitem__(
            next(iter(row)), "0" * 64)),
        ("late_authority_mutation", lambda row: row.__setitem__(
            next(reversed(row)), "f" * 64)),
    ):
        attacked = dict(snapshot)
        mutate(attacked)
        rejected = False
        reason = None
        try:
            require_snapshot_equal(snapshot, attacked, name)
        except Rejected as error:
            rejected = True
            reason = str(error)
        need(rejected, "modeled snapshot attack must fail closed:" + name)
        output.append({"attack": name, "fail_closed": True,
                       "rejection_sha256": hashlib.sha256(
                           reason.encode("utf-8")).hexdigest()})
    return output


def load_modules() -> tuple[Any, Any, Any]:
    before = set(sys.modules)
    sys.path.insert(0, str(DELIVERABLES))
    try:
        c46 = importlib.import_module(C46_NAME)
        c41 = importlib.import_module(C41_NAME)
        c40i = importlib.import_module(C40I_NAME)
    finally:
        if sys.path and sys.path[0] == str(DELIVERABLES):
            sys.path.pop(0)
    need(Path(c46.__file__).absolute() == C46_SOURCE
         and Path(c41.__file__).absolute() == C41_SOURCE
         and Path(c40i.__file__).absolute() == C40I_SOURCE,
         "frozen module import paths")
    loaded = set(sys.modules) - before
    need(not (FORBIDDEN_MODULES & (loaded | set(sys.modules))),
         "C51/C48 producer module was not loaded")
    c40i.source_pins()
    return c46, c41, c40i


def load_frozen_tasks(c46: Any, c41: Any) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    plan, tasks, shards = c46.build_read_only_plan(64)
    need(plan["plan_object_sha256"] == C46_PLAN_OBJECT_SHA256,
         "C46 plan object pin")
    selected = sorted(
        [row for row in tasks if row["pair_index"] == PAIR
         and row["queue"]["priority_class"] == "DIRECT_WHOLE_PAIR"],
        key=lambda row: (row["descendant_path"], row["primary_outer_id"]),
    )
    observed = tuple((row["task_binding_sha256"], row["descendant_path"],
                      row["ambient_cell_id"], row["primary_outer_id"])
                     for row in selected)
    expected = tuple((row["task_binding_sha256"], row["root_path"],
                      row["ambient_cell_id"], row["primary_outer_id"])
                     for row in EXPECTED_TASKS)
    need(observed == expected, "exact frozen pair-1 direct two-task selection")
    shard_matches = [row for row in shards if PAIR in row["pair_indices"]]
    need(len(shard_matches) == 1
         and shard_matches[0]["shard_index"] == EXPECTED_SHARD_INDEX,
         "pair-1 exact pair-preserving shard")
    indices = tuple(index for index, row in enumerate(shard_matches[0]["_tasks"])
                    if row["task_binding_sha256"] in {
                        item["task_binding_sha256"] for item in EXPECTED_TASKS})
    need(indices == EXPECTED_TASK_INDICES, "pair-1 exact shard task indices")

    result = c41.strict_json(C41_DIR / "result.json")
    c41.validate_object(result, C41_OBJECT_SHA256, "C41 candidate")
    wanted = {row["ambient_cell_id"] for row in selected}
    ambient_by_id: dict[str, dict[str, Any]] = {}
    for row in c41.iter_ledger(C41_DIR, result["ledgers"]["routed_ambient_cells"]):
        if row["c41_ambient_cell_id"] in wanted:
            need(row["c41_ambient_cell_id"] not in ambient_by_id,
                 "selected ambient uniqueness")
            ambient_by_id[row["c41_ambient_cell_id"]] = row
    need(set(ambient_by_id) == wanted, "both selected C41 ambient rows")

    c40_dir = ROOT / result["C40_authority"]["path"]
    c40_audit = ROOT / result["C40_authority"]["independent_audit_path"]
    c40_result = c41.strict_json(c40_dir / "result.json")
    wanted_sources = {ambient_by_id[row["ambient_cell_id"]]["c40_source_leaf_id"]
                      for row in selected}
    sources: dict[str, tuple[int, dict[str, Any]]] = {}
    for ordinal, row in enumerate(c41.iter_ledger(
            c40_dir, c40_result["ledgers"]["routed_leaf_cells"])):
        if row["c40_leaf_id"] in wanted_sources:
            need(row["c40_leaf_id"] not in sources, "C40 source uniqueness")
            sources[row["c40_leaf_id"]] = ordinal, row
    need(set(sources) == wanted_sources, "both selected C40 source rows")
    context = c41.load_context(c40_dir, c40_audit, formal=True)
    config = c41.decode_worker_config(context["config"])
    frozen: list[dict[str, Any]] = []
    for selected_row in selected:
        ambient = ambient_by_id[selected_row["ambient_cell_id"]]
        need(ambient["row_sha256"] == selected_row["ambient_row_sha256"]
             and ambient["pair_index"] == PAIR
             and ambient["path"] == selected_row["descendant_path"],
             "task/C41 ambient binding")
        ordinal, source = sources[ambient["c40_source_leaf_id"]]
        task = c41.task_for_row(ordinal, source, context)
        frozen.append({
            "selected": selected_row, "ambient": ambient, "source": source,
            "source_ordinal": ordinal, "context": context,
            "config": config, "task": task,
        })
    return plan, frozen


def reflected_payload(chart: str, payload: dict[str, Any]) -> dict[str, Any]:
    t0, t1 = interval(payload["t"], "reflection t")
    p0, p1 = interval(payload["p"], "reflection p")
    s0, s1 = interval(payload["s"], "reflection s")
    if chart in {"E", "W"}:
        reflected_chart = chart
        reflected_t = -t1, -t0
    else:
        reflected_chart = {"N": "S", "S": "N"}[chart]
        reflected_t = t0, t1
    return {
        "compact_chart": reflected_chart,
        "t": [qstr(value) for value in reflected_t],
        "p": [qstr(-p1), qstr(-p0)],
        "s": [qstr(s0), qstr(s1)],
    }


def mirror_path(c41: Any, frozen: dict[str, Any], path: str) -> str:
    task = frozen["task"]
    rep_cell = task["cell"]
    ref_cell = frozen["context"]["cells"][task["c38_source"]["reflected_cell_id"]]
    rep_chart, ref_chart = compact_chart(rep_cell), compact_chart(ref_cell)
    rep_box, _ = c41.c39.reconstruct_box(rep_cell, "")
    ref_box, _ = c41.c39.reconstruct_box(ref_cell, "")
    need(reflected_payload(rep_chart, c41.box_payload(rep_box))
         == box_payload(c41, ref_chart, ref_box), "root exact reflection")
    mapped = ""
    for bit in path:
        rep_axis = c41.c38.round166.longest_axis(rep_box)
        ref_axis = c41.c38.round166.longest_axis(ref_box)
        need(rep_axis == ref_axis, "reflection preserves exact split axis")
        rep_children = c41.c38.round166.split_axis(rep_box, rep_axis)
        ref_children = c41.c38.round166.split_axis(ref_box, ref_axis)
        rep_box = rep_children[int(bit)]
        expected = reflected_payload(rep_chart, c41.box_payload(rep_box))
        matches = [candidate for candidate in (0, 1)
                   if expected == box_payload(c41, ref_chart,
                                              ref_children[candidate])]
        need(len(matches) == 1, "unique reflected exact child")
        mapped += str(matches[0])
        ref_box = ref_children[matches[0]]
    reconstructed, _ = c41.c39.reconstruct_box(ref_cell, mapped)
    need(c41.box_payload(reconstructed) == c41.box_payload(ref_box),
         "reflected mapped path reconstruction")
    return mapped


def physical_spec(c41: Any, frozen: dict[str, Any], side: str,
                  semantic_path: str) -> tuple[dict[str, Any], dict[str, Any],
                                                dict[str, Any], str, str, Any]:
    base = frozen["task"]["c38_source"]
    pseudo = copy.deepcopy(base)
    if side == "REPRESENTATIVE":
        cell = frozen["task"]["cell"]
        physical_path = semantic_path
    else:
        need(side == "REFLECTED", "physical side enum")
        physical_path = mirror_path(c41, frozen, semantic_path)
        pseudo["representative_cell_id"] = base["reflected_cell_id"]
        pseudo["representative_origin_key"] = base["reflected_origin_key"]
        pseudo["reflected_cell_id"] = base["representative_cell_id"]
        pseudo["reflected_origin_key"] = base["representative_origin_key"]
        cell = frozen["context"]["cells"][pseudo["representative_cell_id"]]
    pseudo["path"] = physical_path
    route_task = {
        "task_id": "c48-route:" + side + ":" + semantic_path,
        "kind": "C1", "row": pseudo, "cell": cell,
    }
    box, _ = c41.c39.reconstruct_box(cell, physical_path)
    return route_task, pseudo, cell, pseudo["representative_origin_key"], physical_path, box


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
    need(margin > 0, "strict obstacle-boundary separation")
    return {
        "left": left, "right": right,
        "minimum_center_distance_squared": qstr(distance2),
        "radius_sum_squared": qstr(radius * radius),
        "strict_squared_margin": qstr(margin),
    }


def terminal_margin(c41: Any, cell: dict[str, Any], origin: str, box: Any,
                    route: dict[str, Any], c2_detail: dict[str, Any],
                    expected_owners: list[str]) -> dict[str, Any]:
    _box, active = c41.c39.reconstruct_box(cell, box.path)
    stage, records = c41.c38.round166.classify_active(
        cell["gate3_chart"], box, active)
    c1_rows = [root_record_payload(c41, row) for row in records]
    unresolved = [row for row in records if row.classification in {
        "unresolved_discriminant", "unresolved_root_sign"}]
    h1 = route["surface_evidence"]["H1"]
    c1_complete = (
        stage.classification == "unique_first"
        and stage.owner_target == c41.FROZEN_OWNER and not unresolved
        and h1 is not None and h1["kind"] == "STRICT_SIDE"
        and h1["chart"] == "W"
        and h1["H1_centered"]["sign"] in {"POSITIVE", "NEGATIVE"}
    )

    r178, r181, r183 = c41.round185.r178, c41.round185.r181, c41.round185.r183
    geometry = r183.collision2_geometry(r181.collision1_state_direct(origin, box))
    point_box = r181.center_box(box)
    point_geometry = r183.collision2_geometry(
        r181.collision1_state_direct(origin, point_box))
    point_status, selected = r178.select_owner(point_geometry, r183.CANDIDATES)
    need(point_status == "STRICT_UNIQUE_OWNER" and isinstance(selected, tuple),
         "strict center collision-two owner")
    point_owner, point_owner_data = selected
    incumbent_kind, incumbent_data = r178.root_record(*geometry, point_owner)
    need(incumbent_kind == "STRICT_FUTURE" and incumbent_data is not None,
         "full-box incumbent strict future")
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
        full_kind, _full_data = r178.root_record(*geometry, candidate)
        raw = r181.raw_candidate(geometry, candidate)
        disposition = "FULL_BOX_RESOLVED_ROOT_STATUS"
        screen = None
        if candidate != point_owner and full_kind in {
                "UNRESOLVED_DELTA", "UNRESOLVED_ROOT_SIGN"}:
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
        full_rows.append({
            "candidate": candidate, "root_kind": full_kind,
            "raw_ell": arb_payload(c41, raw["ell"]),
            "raw_discriminant": arb_payload(c41, raw["Delta"]),
            "screening_disposition": disposition,
            "strict_screening_margin": arb_payload(c41, screen),
        })
    unscreened = [row for row in full_rows
                  if row["screening_disposition"] == "UNSCREENED_ACTIVE_COMPETITOR"]
    separations = [exact_boundary_separation(c41, point_owner, candidate)
                   for candidate in r183.CANDIDATES if candidate != point_owner]
    c2_complete = (
        not unscreened
        and c2_detail["point_owner"] == point_owner
        and c2_detail["absolute_collision2_owner"] == point_owner
        and point_owner not in expected_owners
    )
    body = {
        "schema": C48_SCHEMA + ".strict-terminal-margin",
        "collision1": {
            "whole_box_stage_classification": stage.classification,
            "whole_box_owner": stage.owner_target,
            "record_rows": c1_rows,
            "unresolved_record_count": len(unresolved),
            "H1_strict_side": h1,
            "complete": c1_complete,
        },
        "collision2": {
            "center_point_owner_status": point_status,
            "center_point_owner": point_owner,
            "center_point_root_rows": point_rows,
            "full_box_incumbent_root_kind": incumbent_kind,
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
    need(c1_complete and c2_complete, "all strict terminal margins complete")
    return {**body, "margin_certificate_sha256": digest(body)}


def producer_compatible_leaf(c41: Any, c40i: Any, frozen: dict[str, Any],
                             side: str, relative: str) -> tuple[dict[str, Any], dict[str, Any]]:
    selected = frozen["selected"]
    semantic = selected["descendant_path"] + relative
    task, pseudo, cell, origin, physical, box = physical_spec(
        c41, frozen, side, semantic)
    route = c41.c39.route_c1_task(task, frozen["config"])
    upstream_classification = route["classification"]
    expected_owners = sorted({
        frozen["config"]["original_path"][1]["selected_absolute_owner_id"],
        frozen["config"]["reflected_path"][1]["selected_absolute_owner_id"],
    })
    try:
        normal = True
        c2_status = c2_baseline = None
        c2_detail = None
        c2_evidence: list[dict[str, Any]] = []
        classification, witness = route["classification"], route["witness"]
        if c41.c40.collision2_safe(route, classification):
            c2_status, c2_detail, c2_evidence, c2_baseline = (
                c41.round185.resolve_dynamic_box(
                    origin, box, frozen["config"]["pair_index"],
                    frozen["config"]["pattern_index"]))
            if c2_status.startswith("LOCAL_EXACT_KEY"):
                classification, witness = c41.c40.expected_collision2(
                    c2_detail, frozen["config"])
            else:
                classification = "UNRESOLVED_C40_COLLISION2_" + c2_status
                witness = c2_baseline
        need(c2_detail is not None, "collision-two detail materialized")
        need(classification == "EXCLUDED_C40_COLLISION2_OWNER_MISMATCH",
             "two-side leaf terminal owner mismatch")
        margin = terminal_margin(c41, cell, origin, box, route, c2_detail,
                                 expected_owners)
        need(margin["all_required_strict_margins_complete"],
             "strict terminal margin complete")
    except Rejected as original_error:
        # Reproduce C51's presentation wrapper around a rejected C48 attempt.
        # The numerical fallback is still rerun from the frozen physical task.
        normal = False
        task, pseudo, cell, origin, physical, box = physical_spec(
            c41, frozen, side, semantic)
        route = c41.c39.route_c1_task(task, frozen["config"])
        upstream_classification = route["classification"]
        need(upstream_classification
             == "EXCLUDED_C39_C1_ENHANCED_W_SIDE_COLLISION2_OWNER_MISMATCH",
             "fallback is exact C39 W-side collision2 owner mismatch:"
             + str(original_error))
        c2_status, c2_detail, c2_evidence, c2_baseline = (
            c41.round185.resolve_dynamic_box(
                origin, box, frozen["config"]["pair_index"],
                frozen["config"]["pattern_index"]))
        need(c2_status.startswith("LOCAL_EXACT_KEY"),
             "fallback exact C2 local key; observed=" + str(c2_status))
        classification, witness = c41.c40.expected_collision2(
            c2_detail, frozen["config"])
        need(classification == "EXCLUDED_C40_COLLISION2_OWNER_MISMATCH",
             "fallback exact C2 owner mismatch")
        margin = terminal_margin(c41, cell, origin, box, route, c2_detail,
                                 expected_owners)
        need(margin["all_required_strict_margins_complete"],
             "fallback C39/C2 strict terminal margin complete")

    independent_c39, independent_c39_witness, independent_box = (
        c40i.independent_c39_child_classification(
            frozen["source"], pseudo, cell, physical, frozen["config"]))
    independent_c2, independent_c2_witness = (
        c40i.independent_c40_collision2_classification(
            origin, independent_box, frozen["config"]))
    need(c41.box_payload(independent_box) == c41.box_payload(box),
         "independent exact box equality")
    need(independent_c2 == classification
         and independent_c2_witness == witness,
         "independent collision-two terminal result")
    need(independent_c39.startswith(("EXCLUDED_", "UNRESOLVED_")),
         "independent C39 classified")

    common = {
        "side": side, "pair_index": PAIR,
        "task_binding_sha256": selected["task_binding_sha256"],
        "relative_path": relative, "semantic_path": semantic,
        "physical_route_path": physical, "physical_cell_id": cell["cell_id"],
        "physical_origin_key": origin,
        "exact_closed_box": box_payload(c41, compact_chart(cell), box),
        "relative_parent_fraction": qstr(Q(1, 2 ** len(relative))),
        "C1_route_result": route,
        "C1_route_result_sha256": digest(route),
        "C2_status": c2_status, "C2_baseline": c2_baseline,
        "C2_detail": c2_detail, "C2_detail_sha256": digest(c2_detail),
        "C2_evidence": c2_evidence,
    }
    if normal:
        body = {
            "schema": C48_SCHEMA + ".physical-leaf", **common,
            "C2_evidence_sequence_sha256": sequence_digest(
                digest(row) for row in c2_evidence),
            "terminal_classification": classification,
            "terminal_witness": witness,
            "terminal_margin_certificate": margin,
            "terminal_candidate_closed": True, "formal_credit": 0,
        }
        leaf = {**body, "physical_leaf_id": "c48-leaf:" + digest(body)}
    else:
        body = {
            "schema": C51_SCHEMA + ".physical-leaf", **common,
            "terminal_classification": classification,
            "upstream_terminal_classification": upstream_classification,
            "terminal_witness": witness,
            "terminal_margin_certificate": margin,
            "terminal_candidate_closed": True, "formal_credit": 0,
        }
        leaf = {**body, "physical_leaf_id": "c51-leaf:" + digest(body)}
    audit = {
        "side": side, "relative_path": relative,
        "normal_C40_safe_route": normal,
        "upstream_C39_classification": upstream_classification,
        "independent_C39_classification": independent_c39,
        "independent_C39_witness": independent_c39_witness,
        "independent_C40_classification": independent_c2,
        "independent_C40_witness": independent_c2_witness,
        "collision1_complete": margin["collision1"]["complete"],
        "collision1_unresolved_record_count": margin["collision1"]["unresolved_record_count"],
        "collision2_candidate_count": len(margin["collision2"]["center_point_root_rows"]),
        "collision2_unscreened_count": margin["collision2"]["unscreened_active_competitor_count"],
        "collision2_boundary_separation_count": len(
            margin["collision2"]["exact_boundary_separation_rows"]),
        "collision2_owner": margin["collision2"]["selected_absolute_owner"],
        "margin_certificate_sha256": margin["margin_certificate_sha256"],
        "leaf_object_sha256": digest(leaf),
    }
    return leaf, audit


def compact_leaf(leaf: dict[str, Any]) -> dict[str, Any]:
    margin = leaf["terminal_margin_certificate"]
    return {
        "side": leaf["side"], "relative_path": leaf["relative_path"],
        "physical_route_path": leaf["physical_route_path"],
        "physical_cell_id": leaf["physical_cell_id"],
        "exact_closed_box": leaf["exact_closed_box"],
        "terminal_classification": leaf["terminal_classification"],
        "selected_absolute_owner": margin["collision2"]["selected_absolute_owner"],
        "unscreened_active_competitor_count": margin["collision2"]["unscreened_active_competitor_count"],
        "all_required_strict_margins_complete": margin["all_required_strict_margins_complete"],
        "physical_leaf_id": leaf["physical_leaf_id"],
        "leaf_object_sha256": digest(leaf), "formal_credit": 0,
    }


def probe_task(c41: Any, c40i: Any, frozen: dict[str, Any],
               budget: int = 16) -> tuple[dict[str, Any], list[dict[str, Any]],
                                          dict[tuple[str, str], dict[str, Any]]]:
    selected = frozen["selected"]
    root = selected["descendant_path"]
    source_path = frozen["source"]["path"]
    frontier = [""]
    terminal: dict[str, list[dict[str, Any]]] = {}
    full_leaves: dict[tuple[str, str], dict[str, Any]] = {}
    observations: dict[str, dict[str, Any]] = {}
    splits: list[dict[str, Any]] = []
    audits: list[dict[str, Any]] = []
    while len(splits) < budget:
        split_path = None
        split_route = None
        for relative in sorted(frontier):
            if relative in terminal:
                continue
            absolute = root + relative
            route = c41.route_at_path(frozen["task"], absolute, frozen["config"])
            observation = {
                "relative_path": relative, "absolute_path": absolute,
                "classification": route["classification"],
                "disposition_family": c41.disposition_family(route["classification"]),
                "route_method": route["route_method"],
                "C2_status": route["c2_status"],
                "C2_detail_sha256": (digest(route["c2_detail"])
                    if route["c2_detail"] is not None else None),
            }
            try:
                rows = []
                local_audits = []
                for side in ("REPRESENTATIVE", "REFLECTED"):
                    leaf, audit = producer_compatible_leaf(
                        c41, c40i, frozen, side, relative)
                    rows.append(compact_leaf(leaf))
                    local_audits.append(audit)
                    full_leaves[(side, relative)] = leaf
                terminal[relative] = rows
                audits.extend(local_audits)
                observation["dual_side_strict_terminal"] = True
                observation["strict_terminal_failure"] = None
            except Exception as error:
                observation["dual_side_strict_terminal"] = False
                observation["strict_terminal_failure"] = (
                    type(error).__name__ + ":" + str(error))
            observations[relative] = observation
            if relative not in terminal:
                split_path, split_route = relative, route
                break
        if split_path is None:
            break
        absolute = root + split_path
        bits = absolute[len(source_path):]
        history = c41.exact_axis_history(frozen["task"], bits)
        adjacency, children, axis = c41.split_row(
            frozen["task"], split_route["box"], bits, len(bits), history)
        for bit in ("0", "1"):
            child = c41.route_at_path(frozen["task"], absolute + bit,
                                      frozen["config"])
            need(c41.box_payload(child["box"])
                 == c41.box_payload(children[int(bit)]),
                 "fresh child equals exact split child")
        split_body = {
            "relative_path": split_path, "absolute_path": absolute,
            "split_axis": ("t", "p", "s")[axis],
            "C41_split_face_adjacency_sha256": digest(adjacency),
            "formal_credit": 0,
        }
        splits.append({**split_body, "split_object_sha256": digest(split_body)})
        frontier.remove(split_path)
        frontier.extend([split_path + "0", split_path + "1"])
        frontier.sort()

    for relative in sorted(frontier):
        if relative in observations:
            continue
        absolute = root + relative
        route = c41.route_at_path(frozen["task"], absolute, frozen["config"])
        observations[relative] = {
            "relative_path": relative, "absolute_path": absolute,
            "classification": route["classification"],
            "disposition_family": c41.disposition_family(route["classification"]),
            "route_method": route["route_method"], "C2_status": route["c2_status"],
            "C2_detail_sha256": (digest(route["c2_detail"])
                if route["c2_detail"] is not None else None),
            "dual_side_strict_terminal": False,
            "strict_terminal_failure": "NOT_EVALUATED_AFTER_RESOURCE_BUDGET",
        }
    paths = sorted(frontier)
    kraft = sum((Q(1, 2 ** len(path)) for path in paths), Q(0))
    need(prefix_free(paths) and kraft == 1, "prefix-free exact Kraft frontier")
    all_closed = set(paths) == set(terminal)
    body = {
        "schema": C51_SCHEMA + ".task-probe",
        "task_id": selected["task_id"],
        "task_binding_sha256": selected["task_binding_sha256"],
        "pair_index": PAIR, "root_path": root,
        "ambient_cell_id": selected["ambient_cell_id"],
        "primary_outer_id": selected["primary_outer_id"],
        "event_budget": budget, "split_count": len(splits),
        "split_events": splits, "frontier_paths": paths,
        "frontier_leaf_count": len(paths), "relative_Kraft_sum": str(kraft),
        "prefix_free": True,
        "dual_side_strict_terminal_paths": sorted(terminal),
        "dual_side_strict_terminal_count": len(terminal),
        "dual_side_terminal_rows": [
            {"relative_path": path, "physical_sides": terminal[path]}
            for path in sorted(terminal)],
        "observations": [observations[path] for path in sorted(
            observations, key=lambda value: (len(value), value))],
        "all_frontier_leaves_dual_side_strict_terminal": all_closed,
        "candidate_route_closure_only": all_closed,
        "global_codimension_owner_oracle_applied": False,
        "candidate_or_authority_created": False,
        "formal_credit": 0, "D02_gate_credit": 0,
    }
    probe = {**body, "task_probe_object_sha256": digest(body)}
    return probe, audits, full_leaves


def reconstructed_c51(plan: dict[str, Any], probes: list[dict[str, Any]]) -> dict[str, Any]:
    all_closed = all(row["all_frontier_leaves_dual_side_strict_terminal"]
                     for row in probes)
    body = {
        "schema": C51_SCHEMA,
        "status": ("PASS_PAIR1_TWO_TASK_DUAL_SIDE_STRICT_ROUTE_FRONTIERS_ZERO_CREDIT"
                   if all_closed else
                   "PASS_PAIR1_PROBE_INCOMPLETE_FRONTIERS_REMAIN_ZERO_CREDIT"),
        "source_sha256": C51_SOURCE_SHA256,
        "C46_plan_object_sha256": plan["plan_object_sha256"],
        "pair_index": PAIR, "task_count": len(probes), "task_probes": probes,
        "both_tasks_route_closed": all_closed,
        "prefix_free_and_Kraft_one_for_both_tasks": all(
            row["prefix_free"] and row["relative_Kraft_sum"] == "1"
            for row in probes),
        "full_global_codimension_owner_ledger_pending": True,
        "independent_no_producer_import_verifier_pending": True,
        "no_replace_seal_pending": True,
        "coarse_formal_authority_unchanged": {
            "paired_coarse_cells": 574, "unresolved_coarse_cells": 1150,
            "representative_parents_remaining": 575,
        },
        "runtime_writes_performed": False,
        "formal_credit": 0, "D02_gate_credit": 0,
        "CM2": "NO-GO_FOR_CLAIM",
    }
    return {**body, "object_sha256": digest(body)}


def proper_prefixes(frontier: list[str]) -> set[str]:
    return {value[:depth] for value in frontier for depth in range(len(value))}


def split_decision(side: str, parent: str, physical_parent: str, axis: str,
                   coordinate: str, lower_logical: str, lower_physical: str,
                   upper_logical: str, upper_physical: str) -> dict[str, Any]:
    body = {
        "split_protocol_version": "CM2_EXACT_TWO_SIDE_BINARY_SPLIT_DECISION_V1",
        "side": side, "logical_parent_prefix": parent,
        "physical_parent_path": physical_parent, "axis": axis,
        "coordinate": coordinate,
        "lower_coordinate_logical_child_prefix": lower_logical,
        "lower_coordinate_physical_child_path": lower_physical,
        "upper_coordinate_logical_child_prefix": upper_logical,
        "upper_coordinate_physical_child_path": upper_physical,
        "half_open_owner_logical_child_prefix": lower_logical,
    }
    return {**body, "split_decision_sha256": digest(body)}


def expected_split_decisions(c41: Any, frozen: dict[str, Any],
                             frontier: list[str]) -> list[dict[str, Any]]:
    output: list[dict[str, Any]] = []
    root = frozen["selected"]["descendant_path"]
    for side in ("REPRESENTATIVE", "REFLECTED"):
        for parent in sorted(proper_prefixes(frontier), key=lambda value: (len(value), value)):
            specs = {}
            for suffix in (parent, parent + "0", parent + "1"):
                _task, _pseudo, _cell, _origin, physical, box = physical_spec(
                    c41, frozen, side, root + suffix)
                specs[suffix] = physical, box
            physical_parent, parent_box = specs[parent]
            zero_physical, zero_box = specs[parent + "0"]
            one_physical, one_box = specs[parent + "1"]
            axis_index = c41.c38.round166.longest_axis(parent_box)
            axis = ("t", "p", "s")[axis_index]
            need(axis in {"t", "p"}, "pair1 split stays in t/p")
            if axis == "t":
                need((zero_box.p0, zero_box.p1, zero_box.s0, zero_box.s1)
                     == (one_box.p0, one_box.p1, one_box.s0, one_box.s1),
                     "t split transverse equality")
                if zero_box.t1 == one_box.t0:
                    lower = parent + "0", zero_physical, zero_box.t1
                    upper = parent + "1", one_physical
                else:
                    need(one_box.t1 == zero_box.t0, "t child adjacency")
                    lower = parent + "1", one_physical, one_box.t1
                    upper = parent + "0", zero_physical
            else:
                need((zero_box.t0, zero_box.t1, zero_box.s0, zero_box.s1)
                     == (one_box.t0, one_box.t1, one_box.s0, one_box.s1),
                     "p split transverse equality")
                if zero_box.p1 == one_box.p0:
                    lower = parent + "0", zero_physical, zero_box.p1
                    upper = parent + "1", one_physical
                else:
                    need(one_box.p1 == zero_box.p0, "p child adjacency")
                    lower = parent + "1", one_physical, one_box.p1
                    upper = parent + "0", zero_physical
            need({zero_physical, one_physical}
                 == {physical_parent + "0", physical_parent + "1"},
                 "physical binary child paths")
            output.append(split_decision(
                side, parent, physical_parent, axis, qstr(lower[2]),
                lower[0], lower[1], upper[0], upper[1]))
    output.sort(key=lambda row: (row["side"], row["logical_parent_prefix"]))
    return output


def validate_candidate(candidate: dict[str, Any], *, hard_pins: bool) -> None:
    closed(candidate, "object_sha256", "C50a pair1 candidate")
    request = candidate["request"]
    closed(request, "request_object_sha256", "C50a pair1 request")
    need(candidate["request_object_sha256"] == request["request_object_sha256"],
         "candidate/request object binding")
    need(candidate["schema"] == C50A_SCHEMA
         and candidate["status"] == (
             "PASS_C50A_GENERIC_TWO_SIDE_HISTORY_BOUND_FULL_UNIVERSE_"
             "OWNER_ORACLE__ZERO_FORMAL_CREDIT"),
         "C50a schema/status")
    need(candidate["formal_credit"] == 0 and request["formal_credit"] == 0,
         "C50a/request zero credit")
    need(request["request_purpose"]
         == "PAIR1_TWO_TASK_NINE_LOGICAL_EIGHTEEN_PHYSICAL_OWNER_REPLAY__ZERO_CREDIT",
         "pair1 request purpose")
    need(request["target_mode"] == "ALL_ACTIVE_HISTORY_REPLACEMENTS"
         and request["target_transaction_indices"] == []
         and len(request["transactions"]) == 2,
         "pair1 two-transaction full-history target")
    owner = candidate["owner_ledger"]
    need(owner["all_codimension_owners_unique"] is True
         and owner["all_corner_four_quadrant_germs_complete"] is True
         and owner["all_face_atoms_degree_two"] is True
         and owner["all_face_incident_sets_complete"] is True,
         "C50a owner closure flags")
    need((owner["face_atom_count"], owner["corner_entity_count"],
          owner["target_face_atom_occurrence_count"],
          owner["target_corner_occurrence_count"]) == (52, 36, 78, 72),
         "C50a pair1 owner census")
    need(candidate["target_replay"]["target_occurrence_count"] == 18,
         "C50a target occurrence census")
    strict = candidate["strict_nonpromotion"]
    need(strict["formal_credit"] == strict["D02_gate_credit"] == 0
         and strict["runtime_writes_performed"] is False
         and strict["authority_or_pointer_modified"] is False
         and strict["seal_or_receipt_created"] is False,
         "strict nonpromotion")
    if hard_pins:
        need(candidate["object_sha256"] == C50A_CANDIDATE_OBJECT_SHA256
             and request["request_object_sha256"] == C50A_REQUEST_OBJECT_SHA256,
             "C50a pair1 candidate/request hard pins")


def compare_candidate(c41: Any, candidate: dict[str, Any],
                      frozen_rows: list[dict[str, Any]],
                      probes: list[dict[str, Any]],
                      leaves_by_task: list[dict[tuple[str, str], dict[str, Any]]],
                      *, hard_pins: bool) -> dict[str, Any]:
    validate_candidate(candidate, hard_pins=hard_pins)
    transactions = candidate["request"]["transactions"]
    for index, (tx, frozen, probe, leaves, expected_task) in enumerate(zip(
            transactions, frozen_rows, probes, leaves_by_task, EXPECTED_TASKS,
            strict=True)):
        frontier = list(expected_task["frontier"])
        need(tx["transaction_index"] == index
             and tx["task"]["upstream_task_binding_sha256"]
             == expected_task["task_binding_sha256"]
             and tx["task"]["root_semantic_path"] == expected_task["root_path"],
             "candidate transaction task binding")
        need(tx["relative_frontier"] == frontier
             and probe["frontier_paths"] == frontier,
             "candidate/replay exact frontier")
        need(prefix_free(frontier)
             and sum((Q(1, 2 ** len(path)) for path in frontier), Q(0)) == 1,
             "candidate frontier prefix-free Kraft one")
        expected_splits = expected_split_decisions(c41, frozen, frontier)
        need(tx["split_decisions"] == expected_splits,
             "candidate exact two-side split decisions")
        split_sequence = sequence_digest(
            row["split_object_sha256"] for row in probe["split_events"])
        expected_replacements = []
        for side in ("REPRESENTATIVE", "REFLECTED"):
            for relative in frontier:
                leaf = leaves[(side, relative)]
                compact = compact_leaf(leaf)
                evidence = {
                    "source_schema": C51_SCHEMA + ".task-probe",
                    "source_task_probe_object_sha256": probe["task_probe_object_sha256"],
                    "source_split_event_sequence_sha256": split_sequence,
                    "source_physical_leaf_id": leaf["physical_leaf_id"],
                    "source_leaf_object_sha256": digest(leaf),
                    "source_compact_leaf_row_sha256": digest(compact),
                    "terminal_classification": leaf["terminal_classification"],
                    "all_required_strict_margins_complete": leaf[
                        "terminal_margin_certificate"]["all_required_strict_margins_complete"],
                    "formal_credit": 0,
                }
                expected_replacements.append({
                    "side": side, "relative_path": relative,
                    "semantic_path": expected_task["root_path"] + relative,
                    "physical_route_path": leaf["physical_route_path"],
                    "physical_cell_id": leaf["physical_cell_id"],
                    "exact_closed_box": leaf["exact_closed_box"],
                    "relative_parent_fraction": qstr(Q(1, 2 ** len(relative))),
                    "source_evidence": evidence,
                })
        expected_replacements.sort(key=lambda row: (row["side"], row["relative_path"]))
        need(tx["replacements"] == expected_replacements,
             "candidate exact 18-side replacement evidence")
        for relative in frontier:
            rep = leaves[("REPRESENTATIVE", relative)]["exact_closed_box"]
            ref = leaves[("REFLECTED", relative)]["exact_closed_box"]
            need(reflected_payload(rep["compact_chart"], rep) == ref,
                 "exact logical-leaf reflection")
            need(reflected_payload(ref["compact_chart"], ref) == rep,
                 "exact reflection involution")
    return {
        "candidate_object_sha256": candidate["object_sha256"],
        "request_object_sha256": candidate["request_object_sha256"],
        "transaction_count": 2, "replacement_count": 18,
        "split_decision_count": 14,
        "owner_face_atom_count": candidate["owner_ledger"]["face_atom_count"],
        "owner_corner_entity_count": candidate["owner_ledger"]["corner_entity_count"],
        "all_candidate_request_fields_match_independent_replay": True,
    }


def reclose_attack(candidate: dict[str, Any]) -> None:
    request = candidate["request"]
    for tx in request["transactions"]:
        body = dict(tx)
        body.pop("transaction_binding_sha256", None)
        tx["transaction_binding_sha256"] = digest(body)
    body = dict(request)
    body.pop("request_object_sha256", None)
    request["request_object_sha256"] = digest(body)
    candidate["request_object_sha256"] = request["request_object_sha256"]
    body = dict(candidate)
    body.pop("object_sha256", None)
    candidate["object_sha256"] = digest(body)


def coherent_attacks(c41: Any, candidate: dict[str, Any],
                     frozen_rows: list[dict[str, Any]], probes: list[dict[str, Any]],
                     leaves_by_task: list[dict[tuple[str, str], dict[str, Any]]]) -> list[dict[str, Any]]:
    mutations = [
        ("swap_tasks", lambda x: x["request"]["transactions"].reverse()),
        ("drop_frontier_leaf", lambda x: x["request"]["transactions"][1]["relative_frontier"].pop()),
        ("non_prefix_frontier", lambda x: x["request"]["transactions"][1]["relative_frontier"].__setitem__(0, "1")),
        ("flip_replacement_side", lambda x: x["request"]["transactions"][0]["replacements"][0].__setitem__("side", "REPRESENTATIVE")),
        ("mutate_physical_path", lambda x: x["request"]["transactions"][0]["replacements"][0].__setitem__("physical_route_path", "0")),
        ("mutate_physical_cell", lambda x: x["request"]["transactions"][0]["replacements"][0].__setitem__("physical_cell_id", "c32-compact-cell:" + "0" * 64)),
        ("mutate_exact_box", lambda x: x["request"]["transactions"][0]["replacements"][0]["exact_closed_box"]["t"].__setitem__(0, "0")),
        ("mutate_fraction", lambda x: x["request"]["transactions"][1]["replacements"][0].__setitem__("relative_parent_fraction", "1/2")),
        ("mutate_terminal_class", lambda x: x["request"]["transactions"][0]["replacements"][0]["source_evidence"].__setitem__("terminal_classification", "LIVE")),
        ("clear_margin_complete", lambda x: x["request"]["transactions"][0]["replacements"][0]["source_evidence"].__setitem__("all_required_strict_margins_complete", False)),
        ("mutate_leaf_hash", lambda x: x["request"]["transactions"][0]["replacements"][0]["source_evidence"].__setitem__("source_leaf_object_sha256", "0" * 64)),
        ("mutate_task_probe_hash", lambda x: x["request"]["transactions"][0]["replacements"][0]["source_evidence"].__setitem__("source_task_probe_object_sha256", "0" * 64)),
        ("mutate_split_axis", lambda x: x["request"]["transactions"][0]["split_decisions"][0].__setitem__("axis", "p")),
        ("mutate_split_coordinate", lambda x: x["request"]["transactions"][0]["split_decisions"][0].__setitem__("coordinate", "0")),
        ("mutate_reflected_child_map", lambda x: x["request"]["transactions"][0]["split_decisions"][0].__setitem__("lower_coordinate_physical_child_path", "0")),
        ("request_formal_credit", lambda x: x["request"].__setitem__("formal_credit", 1)),
        ("candidate_formal_credit", lambda x: x.__setitem__("formal_credit", 1)),
        ("owner_nonunique", lambda x: x["owner_ledger"].__setitem__("all_codimension_owners_unique", False)),
        ("owner_incomplete_corner", lambda x: x["owner_ledger"].__setitem__("all_corner_four_quadrant_germs_complete", False)),
        ("runtime_write_claim", lambda x: x["strict_nonpromotion"].__setitem__("runtime_writes_performed", True)),
    ]
    output = []
    for name, mutate in mutations:
        attacked = copy.deepcopy(candidate)
        mutate(attacked)
        reclose_attack(attacked)
        rejected = False
        reason = None
        try:
            compare_candidate(c41, attacked, frozen_rows, probes,
                              leaves_by_task, hard_pins=False)
        except (Rejected, KeyError, TypeError, ValueError, IndexError) as error:
            rejected = True
            reason = type(error).__name__ + ":" + str(error)
        need(rejected, "coherent attack must fail closed:" + name)
        output.append({"attack": name, "fail_closed": True,
                       "rejection_sha256": hashlib.sha256(
                           reason.encode("utf-8")).hexdigest()})
    return output


def pure_self_test() -> dict[str, Any]:
    tests = []
    for paths in (["0", "1"], ["00", "01", "10", "110", "1110", "11110", "11111"]):
        need(prefix_free(paths), "self-test prefix free")
        need(sum((Q(1, 2 ** len(path)) for path in paths), Q(0)) == 1,
             "self-test Kraft one")
        tests.append("prefix/Kraft:" + ",".join(paths))
    sample = {"compact_chart": "E", "t": ["-2", "-1"],
              "p": ["3", "4"], "s": ["0", "0"]}
    reflected = reflected_payload("E", sample)
    need(reflected_payload("E", reflected) == sample,
         "self-test reflection involution")
    tests.append("reflection involution")
    raw = canonical({"a": 1}) + b"\n"
    need(strict_json(raw, "self-test") == {"a": 1}, "strict JSON positive")
    tests.append("strict canonical JSON")
    for bad in (b'{"a":1,"a":1}\n', b"\xef\xbb\xbf{}\n", b'{"a":1.0}\n'):
        rejected = False
        try:
            strict_json(bad, "hostile")
        except (Rejected, ValueError, UnicodeError):
            rejected = True
        need(rejected, "hostile JSON rejected")
    tests.extend(["duplicate JSON key rejected", "BOM rejected",
                  "noninteger JSON number rejected"])
    independence = source_independence_check()
    need(independence["source_ast_import_scan_pass"]
         and independence["source_ast_duplicate_literal_key_scan_pass"],
         "source AST policy self-test")
    tests.append("source AST import/duplicate-literal-key policy")
    snapshot_attacks = modeled_snapshot_attacks({"source": "1" * 64,
                                                 "authority": "2" * 64})
    need(len(snapshot_attacks) == 2
         and all(row["fail_closed"] for row in snapshot_attacks),
         "modeled snapshot attacks")
    tests.extend(["coherent source-swap model rejected",
                  "late authority-mutation model rejected"])
    body = {"schema": SCHEMA + ".self-test",
            "status": "PASS_10_OF_10_PURE_SELF_TESTS", "tests": tests,
            "formal_credit": 0, "runtime_writes_performed": False}
    return {**body, "object_sha256": digest(body)}


def verify(candidate_path: Path, *, run_attacks: bool,
           emit_c51_object: bool = False) -> dict[str, Any]:
    independence = source_independence_check()
    frozen_files_pre = frozen_snapshot()
    raw_candidate, candidate_storage = candidate_bytes(candidate_path)
    candidate = strict_json(raw_candidate, "C50a pair1 candidate")
    validate_candidate(candidate, hard_pins=True)
    c46, c41, c40i = load_modules()
    plan, frozen_rows = load_frozen_tasks(c46, c41)
    probes, numeric_rows, leaves_by_task = [], [], []
    for frozen, expected in zip(frozen_rows, EXPECTED_TASKS, strict=True):
        probe, rows, leaves = probe_task(c41, c40i, frozen, 16)
        need(tuple(probe["frontier_paths"]) == expected["frontier"],
             "independently discovered exact frontier")
        probes.append(probe)
        numeric_rows.extend(rows)
        leaves_by_task.append(leaves)
    need(len(numeric_rows) == 18 and len({(row["side"], row["relative_path"],
            row["leaf_object_sha256"]) for row in numeric_rows}) == 18,
         "18 unique physical strict numeric rows")
    need(all(row["collision1_complete"]
             and row["collision1_unresolved_record_count"] == 0
             and row["collision2_candidate_count"] == 55
             and row["collision2_unscreened_count"] == 0
             and row["collision2_boundary_separation_count"] == 54
             for row in numeric_rows), "all C1/C2 strict margins complete")
    c51 = reconstructed_c51(plan, probes)
    need(c51["object_sha256"] == C51_OBJECT_SHA256,
         "byte-exact independently reconstructed C51 object:observed="
         + c51["object_sha256"] + ":task_probes="
         + ",".join(row["task_probe_object_sha256"] for row in probes))
    comparison = compare_candidate(c41, candidate, frozen_rows, probes,
                                   leaves_by_task, hard_pins=True)
    frozen_files_post = frozen_snapshot()
    require_snapshot_equal(frozen_files_pre, frozen_files_post,
                           "imports and complete numerical replay")
    if emit_c51_object:
        return c51
    attacks = (coherent_attacks(c41, candidate, frozen_rows, probes,
                                leaves_by_task)
               + modeled_snapshot_attacks(frozen_files_pre)) if run_attacks else []
    need(not run_attacks or len(attacks) == 22, "22 coherent attacks")
    owner_census: dict[str, int] = {}
    route_census: dict[str, int] = {}
    for row in numeric_rows:
        owner_census[row["collision2_owner"]] = owner_census.get(
            row["collision2_owner"], 0) + 1
        route = row["independent_C39_classification"]
        route_census[route] = route_census.get(route, 0) + 1
    task_rows = []
    for index, (probe, expected) in enumerate(zip(probes, EXPECTED_TASKS, strict=True)):
        task_rows.append({
            "task_index": EXPECTED_TASK_INDICES[index],
            "task_binding_sha256": expected["task_binding_sha256"],
            "root_path": expected["root_path"],
            "frontier": list(expected["frontier"]),
            "logical_leaf_count": len(expected["frontier"]),
            "physical_strict_terminal_count": 2 * len(expected["frontier"]),
            "split_count": probe["split_count"],
            "prefix_free": probe["prefix_free"],
            "relative_Kraft_sum": probe["relative_Kraft_sum"],
            "task_probe_object_sha256": probe["task_probe_object_sha256"],
            "leaf_object_sequence_sha256": sequence_digest(
                digest(leaves_by_task[index][(side, relative)])
                for side in ("REPRESENTATIVE", "REFLECTED")
                for relative in expected["frontier"]),
        })
    body = {
        "schema": SCHEMA,
        "status": (
            "PASS_C52_PAIR1_NO_PRODUCER_IMPORT_COLD_INDEPENDENT_ROUTE_MARGIN_"
            "REFLECTION_KRAFT_AND_CANDIDATE_REQUEST_AUDIT__ZERO_CREDIT"),
        "verifier_source_sha256": hashlib.sha256(stable_read(
            SELF, "C52 verifier source final")).hexdigest(),
        "C51": {
            "source_file_sha256": C51_SOURCE_SHA256,
            "report_file_sha256": C51_REPORT_SHA256,
            "independently_reconstructed_object_sha256": c51["object_sha256"],
            "object_sha256": C51_OBJECT_SHA256,
        },
        "C50a": {
            **comparison,
            "candidate_storage": candidate_storage,
            "independent_owner_audit_object_sha256": C50A_INDEPENDENT_AUDIT_OBJECT_SHA256,
        },
        "frozen_plan": {
            "C46_plan_object_sha256": C46_PLAN_OBJECT_SHA256,
            "pair_index": PAIR, "shard_index": EXPECTED_SHARD_INDEX,
            "task_indices": list(EXPECTED_TASK_INDICES),
        },
        "tasks": task_rows,
        "census": {
            "task_count": 2, "logical_leaf_count": 9,
            "physical_side_strict_terminal_count": 18,
            "collision1_strict_margin_complete_count": 18,
            "collision2_strict_margin_complete_count": 18,
            "collision2_55_candidate_replay_count": 18,
            "collision2_positive_boundary_separation_row_count": 18 * 54,
            "reflection_pair_count": 9,
            "prefix_free_task_count": 2, "Kraft_one_task_count": 2,
            "route_classification_census": dict(sorted(route_census.items())),
            "collision2_owner_census": dict(sorted(owner_census.items())),
        },
        "numeric_row_sequence_sha256": sequence_digest(
            digest(row) for row in numeric_rows),
        "frozen_file_sha256": frozen_files_pre,
        "frozen_file_post_sha256": frozen_files_post,
        "frozen_pre_post_equal": True,
        "independence": {
            **independence,
            "C41_C46_and_C32_frozen_authorities_consumed": True,
            "C40_independent_numeric_implementation_replayed": True,
            "C50a_candidate_consumed_as_data_only": True,
        },
        "coherent_attack_count": len(attacks),
        "coherent_attacks": attacks,
        "all_attacks_fail_closed": all(row["fail_closed"] for row in attacks),
        "formal_credit": 0, "D02_gate_credit": 0,
        "candidate_or_authority_created": False,
        "pointer_seal_or_canonical_modified": False,
        "runtime_writes_performed": False,
        "CM2": "NO-GO_FOR_CLAIM",
    }
    return {**body, "object_sha256": digest(body)}


def emit(value: dict[str, Any]) -> None:
    sys.stdout.buffer.write(canonical(value) + b"\n")
    sys.stdout.buffer.flush()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    modes = parser.add_mutually_exclusive_group(required=True)
    modes.add_argument("--verify", action="store_true")
    modes.add_argument("--self-test", action="store_true")
    modes.add_argument("--emit-c51-object", action="store_true")
    parser.add_argument("--candidate", type=Path, default=DEFAULT_CANDIDATE)
    parser.add_argument("--skip-attacks", action="store_true")
    args = parser.parse_args(argv)
    try:
        result = (pure_self_test() if args.self_test else verify(
            args.candidate, run_attacks=(not args.skip_attacks
                                        and not args.emit_c51_object),
            emit_c51_object=args.emit_c51_object))
        emit(result)
        return 0
    except (Rejected, OSError, ValueError, KeyError, TypeError, RuntimeError,
            AssertionError, ImportError) as error:
        body = {
            "schema": SCHEMA + ".rejection", "status": "REJECTED_FAIL_CLOSED",
            "error_class": type(error).__name__, "reason": str(error),
            "formal_credit": 0, "D02_gate_credit": 0,
            "runtime_writes_performed": False,
        }
        emit({**body, "object_sha256": digest(body)})
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
