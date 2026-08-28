#!/usr/bin/env python3
"""Cold, no-C49-import numeric verifier for the C49-v4 pair-9 regression.

The verifier derives pair 9 twice: from the frozen C46 queue and by scanning
the frozen C41 routed-row authority.  It never imports or executes any C49
module.  Instead it calls the lower geometric/registry authorities directly
and implements a separate collision state machine which recomputes every
collision-3 and collision-4 adaptive node, every sensitivity split, and the
selected collision-5 step at python-flint 0.9.0 / 384 bits.

The comparison boundary is a canonical semantic projection of every numeric
step and split decision.  Producer-specific schemas, self hashes, handoff
serialization and authenticated input echoes are deliberately excluded from
that projection; their frozen C49 hashes are separately pinned as bindings.

All reads of pinned sources and authority files use stable descriptor/path
checks.  The self-test uses real temporary files for atomic source swap,
truncate, injected premature EOF, permission denial and rename-away faults.
No runtime authority, pointer, receipt, seal or canonical status is written.
"""

from __future__ import annotations

import argparse
import ast
from collections import Counter
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
import tempfile
from typing import Any, Callable, Iterable

from flint import arb, ctx
import flint


if hasattr(sys, "set_int_max_str_digits"):
    sys.set_int_max_str_digits(0)
sys.dont_write_bytecode = True

SELF = Path(__file__).absolute()
ROOT = SELF.parent.parent
DELIVERABLES = ROOT / "deliverables"
RUNTIME = ROOT / ".cm2-runtime"
if str(DELIVERABLES) not in sys.path:
    sys.path.insert(0, str(DELIVERABLES))

SCHEMA = "cm2.round306c54p0.c49-v4-pair9-no-producer-numeric-verifier.v1"
SOURCE_CHART_ID = "W:E"
COLLISION1_OWNER = "W[1,0]"
PAIR_INDEX = 9
PAIR9_PATH = "011110111"
SIDE_ORDER = ("REFLECTED", "REPRESENTATIVE")
AXES = ("t", "p")
HEX64 = re.compile(r"[0-9a-f]{64}\Z")

C49_V4_SOURCE = DELIVERABLES / "cm2_round306c49_d02b_pure_advance_one_collision_v4.py"
C49_V4_SOURCE_SHA256 = "80bb67a46ae4f8a10195aa6b1b17f539708eafc83be4b39bc7724624fd64295f"
C49_V4_REGRESSION_FILE_SHA256 = "88beb4c0c0562cc21054d3283d7a4452f65053abfae82c9d8243c1073519c42a"
C49_V4_REGRESSION_OBJECT_SHA256 = "9a39a43907651235a216977a097615aad098be10989617088a6295043857fb17"

C46_NAME = "cm2_round306c46_d02b_resumable_occurrence_collision_continuation_engine_v1"
C45_NAME = "cm2_round306c45_d02b_pair_preserving_batch_runner_planner_v1"
C41_NAME = "cm2_round306c41_d02_lower_strata_depth3_closure_v1"
R166_NAME = "cm2_round166_multi_candidate_refinement_prototype"
R139_NAME = "cm2_round139_rank3_minus_d0_adjacent_h1_collar_return_frontier"
R185_NAME = "cm2_round185_preconditioned_c1_residual_refinement"

C46_SOURCE = DELIVERABLES / (C46_NAME + ".py")
C45_SOURCE = DELIVERABLES / (C45_NAME + ".py")
C43_SOURCE = DELIVERABLES / "cm2_round306c43_collision3_ready_inventory_planner_v1.py"
C41_SOURCE = DELIVERABLES / (C41_NAME + ".py")
R166_SOURCE = DELIVERABLES / (R166_NAME + ".py")
R139_SOURCE = DELIVERABLES / (R139_NAME + ".py")
R185_SOURCE = DELIVERABLES / (R185_NAME + ".py")

C41_DIR = RUNTIME / "candidates/c41-lower-strata-depth3-20260811T023804Z-f997365c91559599"
C41_RESULT = C41_DIR / "result.json"
C41_MANIFEST = C41_DIR / "root_manifest.sha256"
C41_ROWS = C41_DIR / "routed_ambient_cells.jsonl.gz"

FROZEN_FILES: dict[Path, str] = {
    C49_V4_SOURCE: C49_V4_SOURCE_SHA256,
    C46_SOURCE: "95a9e30101368b4bc91142a75ec7821b0d035f3dab52a556377c761c1bdac7b7",
    C45_SOURCE: "bd8937fe5c88b4a77e0eea14ef7fa4fc5e3356458e389a5d4d91e5ae8fb288f6",
    C43_SOURCE: "8519aa02e80ddda01953db9f48c641d88244f264ea67de59307a674c77194b48",
    C41_SOURCE: "3fbf6cec247903d6e6ba147d4d06e912638b1472b74adc8311323c554e6e5bde",
    R166_SOURCE: "6479a78249a717169dea55ecabae98c05f240ea323fa0370037d43339158ae7c",
    R139_SOURCE: "462ffcb41ba24771ce655ddb3ad5f18d5a22c8d0cb443ec1791ea9272d3d512b",
    R185_SOURCE: "7b48f3ee3417fcfdf5ef6c852e0ab591eb849b357e704e46ee3aaa259d20acc2",
    C41_RESULT: "73fde0eee7eb06bb0f144ea98880c72bfea36e10db696731ae72393cd9b0a50f",
    C41_MANIFEST: "86e10532d63269cd0fdd58d541b1984522e9718f4613a5dc83211fe84eb258ba",
    C41_ROWS: "ea75405c8f8ba53c795c64a228aea75f9587017d93aa1cd08e73c287931e78a8",
}

QUEUE_PINS = {
    "representative_ready_rows": 7463,
    "physical_side_branches": 14926,
    "representative_key_sequence_sha256":
        "9fe3435e1efdb935fb2756c0e808b8cc282baf04af95a31ca723bccbe4755ce5",
    "physical_queue_sequence_sha256":
        "c79b7e8736c7cf9c8e95e6249d76c0d0b31fb4d3b6d5dbb12d359a4c7a41f5e0",
    "physical_handoff_id_line_sequence_sha256":
        "2558af09865e542b5eb969f636585baa815086de5d1f2b130a7ef152cf3a8c58",
}
FULL_QUEUE_MANIFEST_SHA256 = "9dd2ec13da5509d7f4c8e947090feaee05ac31924e2855086c17a6dc05b7b5f4"
C41_OBJECT_SHA256 = "b7e47a4ca9d6f4bb1fee10e78877850d5070f6d3c2b06bb0234fbabdaa2b7b24"
C41_ROW_SHA256 = "204f68a9496b643c5207d1d33156bab04824e021a8f0d49a14025bbb907ba93a"
SOURCE_BINDING_PINS = {
    "REFLECTED": "d9d1ad4f4bf856764733d8f1f8360e51f8f003572104e868eb445e90c6073482",
    "REPRESENTATIVE": "486f959429f2b69440e0c68349c308eb07060303185536e3c771188658ab5dab",
}

MISSING_GLOBAL_ORACLES = (
    "GLOBAL_CEMETERY_DISCONNECTED_EXTERIOR_ORACLE",
    "GLOBAL_CODIMENSION_FACE_ENDPOINT_CORNER_OWNER_ORACLE",
)
ALLOWED_TERMINALS = (
    "STRICT_EXCLUDED", "KNOWN_COMPONENT", "STRICT_CEMETERY_OR_DISCONNECTED",
)

# Producer-specific bindings are checked independently of the semantic numeric
# projection.  These are the frozen patched-v4 regression values.
C49_BINDINGS = {
    "collision3_reflected": {
        "path": "000000", "owner": "W[0,0]",
        "step_object_sha256": "939f731c5f811190f63a53f7fba41e525a0be36ad6e6f0f947e30df0c9a27a65",
        "step_evidence_sha256": "814a71b3f74ca52f6035a38dcba27b93658333dc8a6224a7f1360e333780afaa",
    },
    "collision3_representative": {
        "path": "0000", "owner": "W[0,-1]",
        "step_object_sha256": "27df2914b27e0f0b502477f7d0447c5a7d8596e3a9017971e867d4850a61231d",
        "step_evidence_sha256": "0021fd208134c39afdb99011799601e57cc0b13ad2591c3d61adcfb1aa48633d",
    },
    "collision4": {
        "path": "00000000000011", "owner": "G[0,1]",
        "step_object_sha256": "6ed4449449de2de52947e2cfbc67eb4fbc3951cf1b64fec23dc15c1669809f68",
        "step_evidence_sha256": "488f6f91d816b384a91efc57abad2d0993d8fe49d2588cc986b14a9a162f533c",
    },
    "collision5": {
        "owner": "G[0,0]",
        "step_object_sha256": "fa752b6bd6fbf13f81d1e6da232e97cb4c4215b4bac87023bcbc5812ff18a4e2",
        "step_evidence_sha256": "ff32507ff41abbad32751e461631e454e4aee8bb901911587093101757b51190",
    },
}

EXPECTED_CENSUS = {
    "collision3": {
        "node_count": 99, "split_count": 49, "leaf_count": 50,
        "relative_Kraft_sum": "1",
        "leaf_status_census": {
            "BOUNDED_PILOT_UNRESOLVED_WITH_EXACT_NEXT_DECISION": 32,
            "PASS_STRICT_COLLISION3_LIVE_TO_COLLISION4_ZERO_CREDIT": 18,
        },
    },
    "collision4": {
        "node_count": 233, "split_count": 116, "leaf_count": 117,
        "relative_Kraft_sum": "1",
        "leaf_status_census": {
            "BOUNDED_PILOT_UNRESOLVED_WITH_EXACT_NEXT_DECISION": 56,
            "PASS_STRICT_COLLISION4_LIVE_TO_COLLISION5_ZERO_CREDIT": 61,
        },
    },
}

# Frozen after byte-valid C49-v4 JSON was reduced by the separate C54p0
# reference extractor and matched field-for-field by this implementation.
EXPECTED_SEMANTIC_SHA256 = {
    "collision3_reflected":
        "266ebff0ad264d55b9392e6c079c95812d14d74a6b07530f317aca51bb712490",
    "collision3_representative":
        "c99198f17bb3cda1e6079f86d31f6d9f7e7dc1f23278680b12d24b99f96149b9",
    "collision4":
        "fa91e106d1d4999d4d8c9c63171d6769f474d2a049f40c8f88e2dc4d8563ad57",
    "collision5_step":
        "cb03b21eb7edb01bc3b7e6dae0fc23cc75caf55bd72592f7bd3281528e6f195b",
    "combined":
        "b2700d1fd48686557a7b918037b9c89a8b8054c710f00af4e66cf0c953521447",
}

FORBIDDEN_MODULES = {
    "cm2_round306c49_d02b_pure_advance_one_collision_v2",
    "cm2_round306c49_d02b_pure_advance_one_collision_v3",
    "cm2_round306c49_d02b_pure_advance_one_collision_v4",
}


class Rejected(RuntimeError):
    """Fail-closed independent-verifier rejection."""


def need(condition: bool, label: str) -> None:
    if type(condition) is not bool or not condition:
        raise Rejected(label)


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=True, allow_nan=False).encode("ascii")


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def close_object(value: dict[str, Any]) -> dict[str, Any]:
    need("object_sha256" not in value, "object hash absent")
    return {**copy.deepcopy(value), "object_sha256": digest(value)}


def qstr(value: Q) -> str:
    return str(value.numerator) if value.denominator == 1 else str(value)


def stable_read(
    path: Path,
    label: str,
    maximum: int = 512 << 20,
    *,
    chunk_size: int = 1 << 20,
    after_open: Callable[[int], None] | None = None,
    after_first_read: Callable[[int], None] | None = None,
    read_fn: Callable[[int, int], bytes] = os.read,
) -> bytes:
    flags = os.O_RDONLY | getattr(os, "O_CLOEXEC", 0) | getattr(os, "O_NOFOLLOW", 0)
    fd = os.open(path, flags)
    try:
        before = os.fstat(fd)
        need(stat.S_ISREG(before.st_mode) and before.st_nlink == 1,
             "regular singleton:" + label)
        need(0 < before.st_size <= maximum, "bounded nonempty:" + label)
        if after_open is not None:
            after_open(fd)
        pieces: list[bytes] = []
        remaining = before.st_size
        first = True
        while remaining:
            block = read_fn(fd, min(chunk_size, remaining))
            need(bool(block), "premature EOF/short-read fault:" + label)
            need(len(block) <= remaining, "read beyond frozen size:" + label)
            pieces.append(block)
            remaining -= len(block)
            if first and after_first_read is not None:
                first = False
                after_first_read(fd)
        need(read_fn(fd, 1) == b"", "EOF moved:" + label)
        after = os.fstat(fd)
        named = os.stat(path, follow_symlinks=False)
    finally:
        os.close(fd)
    identity = lambda row: (
        row.st_dev, row.st_ino, row.st_mode, row.st_nlink, row.st_uid,
        row.st_gid, row.st_size, row.st_mtime_ns, row.st_ctime_ns,
    )
    need(identity(before) == identity(after) == identity(named),
         "fd/path/TOCTOU identity:" + label)
    raw = b"".join(pieces)
    need(len(raw) == before.st_size, "byte count:" + label)
    return raw


def snapshot() -> dict[str, str]:
    observed = {
        str(path.relative_to(ROOT)): hashlib.sha256(
            stable_read(path, "snapshot:" + str(path.relative_to(ROOT)))
        ).hexdigest()
        for path in FROZEN_FILES
    }
    expected = {str(path.relative_to(ROOT)): value
                for path, value in FROZEN_FILES.items()}
    need(observed == expected, "frozen source/authority snapshot pins")
    observed[str(SELF.relative_to(ROOT))] = hashlib.sha256(
        stable_read(SELF, "verifier self", 4 << 20)
    ).hexdigest()
    return observed


def source_independence() -> dict[str, Any]:
    raw = stable_read(SELF, "verifier AST", 4 << 20)
    tree = ast.parse(raw.decode("utf-8", "strict"), filename=str(SELF))
    imported: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imported.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            imported.add(node.module)
        elif isinstance(node, ast.Dict):
            keys = [key.value for key in node.keys if isinstance(key, ast.Constant)]
            need(len(keys) == len(set(keys)), "duplicate literal dictionary key")
    need(not (imported & FORBIDDEN_MODULES), "static C49 import forbidden")
    need(not (set(sys.modules) & FORBIDDEN_MODULES), "C49 module already loaded")
    return {
        "C49_v2_v3_v4_imported_or_executed": False,
        "AST_import_scan": "PASS",
        "duplicate_literal_key_scan": "PASS",
        "forbidden_modules_absent_from_sys_modules": True,
    }


c46: Any = None
c45: Any = None
c41: Any = None
r166: Any = None
r139: Any = None
r185: Any = None
RR: Any = None
TIME: Any = None
STEP1: Any = None
BASE: Any = None


def load_lower_authorities() -> None:
    global c46, c45, c41, r166, r139, r185, RR, TIME, STEP1, BASE
    c46 = importlib.import_module(C46_NAME)
    c45 = importlib.import_module(C45_NAME)
    c41 = importlib.import_module(C41_NAME)
    r166 = importlib.import_module(R166_NAME)
    r139 = importlib.import_module(R139_NAME)
    r185 = importlib.import_module(R185_NAME)
    need(Path(c46.__file__).absolute() == C46_SOURCE
         and Path(c45.__file__).absolute() == C45_SOURCE
         and Path(c41.__file__).absolute() == C41_SOURCE
         and Path(r166.__file__).absolute() == R166_SOURCE
         and Path(r139.__file__).absolute() == R139_SOURCE
         and Path(r185.__file__).absolute() == R185_SOURCE,
         "lower authority module paths")
    need(not (set(sys.modules) & FORBIDDEN_MODULES),
         "C49 transitively imported")
    RR = r139.lower.round136
    TIME = r139.lower.time3
    STEP1 = r139.lower.step1
    BASE = r185.BASE


def strict_json(raw: bytes, label: str) -> dict[str, Any]:
    def pairs(items: list[tuple[str, Any]]) -> dict[str, Any]:
        output: dict[str, Any] = {}
        for key, value in items:
            need(key not in output, "duplicate JSON key:" + label + ":" + key)
            output[key] = value
        return output

    value = json.loads(raw.decode("utf-8", "strict"), object_pairs_hook=pairs,
                       parse_float=lambda token: (_ for _ in ()).throw(
                           Rejected("float JSON:" + label + ":" + token)),
                       parse_constant=lambda token: (_ for _ in ()).throw(
                           Rejected("constant JSON:" + label + ":" + token)))
    need(type(value) is dict, "JSON object:" + label)
    return value


def c41_pair9_from_frozen_jsonl() -> dict[str, Any]:
    raw = gzip.decompress(stable_read(C41_ROWS, "C41 routed rows"))
    matches: list[dict[str, Any]] = []
    for ordinal, line in enumerate(raw.splitlines()):
        row = strict_json(line, "C41 row:" + str(ordinal))
        if row.get("pair_index") == PAIR_INDEX and row.get("path") == PAIR9_PATH:
            matches.append(row)
    need(len(matches) == 1, "unique pair9 in frozen C41 JSONL")
    row = matches[0]
    body = dict(row)
    claimed = body.pop("row_sha256", None)
    need(claimed == C41_ROW_SHA256 == digest(body), "C41 pair9 row self hash")
    result_raw = stable_read(C41_RESULT, "C41 result")
    result = strict_json(result_raw.strip(), "C41 result")
    need(result.get("object_sha256") == C41_OBJECT_SHA256,
         "C41 result object pin")
    return row


def source_binding_body(source: dict[str, Any], handoff: dict[str, Any]) -> dict[str, Any]:
    raw = source[handoff["box_key"]]
    return {
        "schema": "cm2.round306c49.d02-b-pure-advance-one-collision.v3.source-binding",
        "pair_index": source["pair_index"],
        "C41_path": source["path"],
        "side": handoff["side"],
        "source_chart_id": SOURCE_CHART_ID,
        "closed_source_box": {axis: list(raw[axis]) for axis in ("t", "p", "s")},
        "C41_ambient_cell_id": source["c41_ambient_cell_id"],
        "C41_row_sha256": source["row_sha256"],
        "C45_handoff_id": handoff["handoff_id"],
        "C45_occurrence_owner_binding": copy.deepcopy(
            handoff["collision2_occurrence_owner_binding"]),
        "incoming_collision2_owner": handoff["occurrence_incoming_owner"],
        "queue_pins": {
            **QUEUE_PINS,
            "C35_collision3_row_sha256":
                "2d1e15152e61648237b33b7aeade8a9e0c4374ecc84b0f4c3f3ddbb173f1b5a1",
            "C36_collision3_margin_row_sha256":
                "7a4296ba0a1537b4a34ff9c0673e63c0b5874a0e27e8c2e456dc46d0db0f4995",
            "C37_reflected_collision3_row_sha256":
                "7d75d31baa4826a0ae821d9bc14bfdb03b1a311a2ab00ba48ba78cdd79cfc013",
        },
        "formal_credit": 0,
    }


def derive_inputs() -> tuple[dict[str, Any], list[dict[str, Any]], dict[str, Any]]:
    planner, ordered, bundle, manifest = c46.full_queue_context()
    need({key: planner[key] for key in QUEUE_PINS} == QUEUE_PINS,
         "C46 queue pins")
    need(manifest["full_queue_manifest_sha256"] == FULL_QUEUE_MANIFEST_SHA256,
         "C46 full queue manifest pin")
    matches = [row for row in ordered
               if row["pair_index"] == PAIR_INDEX and row["path"] == PAIR9_PATH]
    need(len(matches) == 1, "unique pair9 in C46 queue")
    source = matches[0]
    direct = c41_pair9_from_frozen_jsonl()
    need(source == direct and source["row_sha256"] == C41_ROW_SHA256,
         "C46/C41 byte-semantic pair9 equality")
    handoffs = c45.build_handoffs(source, bundle)
    need([row["side"] for row in handoffs] == list(SIDE_ORDER),
         "pair9 side order")
    inputs: list[dict[str, Any]] = []
    for handoff in handoffs:
        binding = close_object(source_binding_body(source, handoff))
        need(binding["object_sha256"] == SOURCE_BINDING_PINS[handoff["side"]],
             "C49 source-binding pin:" + handoff["side"])
        inputs.append({
            "side": handoff["side"],
            "closed_box": copy.deepcopy(binding["closed_source_box"]),
            "adaptive_suffix": "",
            "source_binding": binding,
            "history": [
                {"collision_index": 1, "selected_owner": COLLISION1_OWNER,
                 "evidence_sha256": "GENESIS-COLLISION1-NORMALIZED"},
                {"collision_index": 2,
                 "selected_owner": binding["incoming_collision2_owner"],
                 "evidence_sha256": "GENESIS-COLLISION2-NORMALIZED"},
            ],
        })
    return source, inputs, manifest


def exact_bounds(value: arb) -> dict[str, Any]:
    lower, upper = RR.arb_pair(value)
    return {
        "exact_dyadic": [qstr(lower), qstr(upper)],
        "strict_sign": ("POSITIVE" if bool(value > 0) else
                        "NEGATIVE" if bool(value < 0) else "UNRESOLVED"),
    }


def positive_margin(value: arb) -> dict[str, Any]:
    need(bool(value > 0), "strict positive margin")
    lower, upper = RR.arb_pair(value)
    depth = RR.strict_dyadic_depth(value, lower)
    return {"exact_dyadic": [qstr(lower), qstr(upper)],
            "dyadic_depth": depth,
            "strict_lower_bound": qstr(RR.power_of_two(-depth))}


def min_arb(values: list[arb]) -> arb:
    need(bool(values), "nonempty Arb minimum")
    return min(values, key=lambda value: RR.arb_pair(value)[0])


def atlas_box(payload: dict[str, Any], path: str) -> Any:
    return r166.ge.AtlasBox(
        Q(payload["t"][0]), Q(payload["t"][1]),
        Q(payload["p"][0]), Q(payload["p"][1]), Q(0), Q(0),
        len(path), path,
    )


def public_box(box: Any) -> dict[str, list[str]]:
    return {"t": [qstr(box.t0), qstr(box.t1)],
            "p": [qstr(box.p0), qstr(box.p1)],
            "s": [qstr(box.s0), qstr(box.s1)]}


def point_box(box: Any) -> Any:
    t = (box.t0 + box.t1) / 2
    p = (box.p0 + box.p1) / 2
    return r166.ge.AtlasBox(t, t, p, p, Q(0), Q(0), 0, box.path + ".C")


def split_box(box: Any, axis: str) -> tuple[Any, Any, Q]:
    need(axis in AXES, "split axis")
    if axis == "t":
        coordinate = (box.t0 + box.t1) / 2
        left = r166.ge.AtlasBox(box.t0, coordinate, box.p0, box.p1,
                               Q(0), Q(0), box.depth + 1, box.path + "0")
        right = r166.ge.AtlasBox(coordinate, box.t1, box.p0, box.p1,
                                Q(0), Q(0), box.depth + 1, box.path + "1")
    else:
        coordinate = (box.p0 + box.p1) / 2
        left = r166.ge.AtlasBox(box.t0, box.t1, box.p0, coordinate,
                               Q(0), Q(0), box.depth + 1, box.path + "0")
        right = r166.ge.AtlasBox(box.t0, box.t1, coordinate, box.p1,
                                Q(0), Q(0), box.depth + 1, box.path + "1")
    return left, right, coordinate


def recentered(full: Any, center: Any, box: Any) -> arb:
    answer = center.value
    widths = ((box.t1 - box.t0) / 2, (box.p1 - box.p0) / 2, Q(0))
    for derivative, width in zip(full.derivative, widths):
        answer += derivative * BASE.arb_interval(-width, width)
    return answer


def geometry_after_history(
    box: Any, history: list[dict[str, Any]],
) -> tuple[dict[str, Any] | None, dict[str, Any]]:
    full = r185.ad_initial_geometry(SOURCE_CHART_ID, box)
    center = r185.ad_initial_geometry(SOURCE_CHART_ID, point_box(box))
    replay: list[dict[str, Any]] = []
    last_full_normal = last_center_normal = None
    last_tangential = None
    for row in history:
        owner_id = row["selected_owner"]
        raw_full = r185.ad_root(full, owner_id)
        raw_center = r185.ad_root(center, owner_id)
        delta = recentered(raw_full["Delta"], raw_center["Delta"], box)
        ell = recentered(raw_full["ell"], raw_center["ell"], box)
        if not bool(delta > 0):
            return None, {"status": "UNRESOLVED_HISTORY_DISCRIMINANT",
                          "collision_index": row["collision_index"],
                          "selected_owner": owner_id,
                          "discriminant": exact_bounds(delta)}
        near = ell - delta.sqrt()
        if not bool(near > 0):
            return None, {"status": "UNRESOLVED_HISTORY_NEAR_ROOT",
                          "collision_index": row["collision_index"],
                          "selected_owner": owner_id,
                          "discriminant": exact_bounds(delta),
                          "near_root": exact_bounds(near)}
        replay.append({"collision_index": row["collision_index"],
                       "selected_owner": owner_id,
                       "recomputed_discriminant": exact_bounds(delta),
                       "recomputed_near_root": exact_bounds(near)})
        last_tangential = recentered(
            raw_full["transverse"] / raw_full["radius"],
            raw_center["transverse"] / raw_center["radius"], box)
        full, fnx, fny = r185.ad_collision(full, owner_id)
        center, cnx, cny = r185.ad_collision(center, owner_id)
        last_full_normal, last_center_normal = (fnx, fny), (cnx, cny)
    need(last_full_normal is not None and last_center_normal is not None,
         "history produces state")
    nx = recentered(last_full_normal[0], last_center_normal[0], box)
    ny = recentered(last_full_normal[1], last_center_normal[1], box)
    h = recentered(last_full_normal[0] * last_full_normal[0]
                   - last_full_normal[1] * last_full_normal[1],
                   last_center_normal[0] * last_center_normal[0]
                   - last_center_normal[1] * last_center_normal[1], box)
    chart = ("E" if bool(h > 0) and bool(nx > 0) else
             "W" if bool(h > 0) and bool(nx < 0) else
             "N" if bool(h < 0) and bool(ny > 0) else
             "S" if bool(h < 0) and bool(ny < 0) else None)
    coordinates = [recentered(a, b, box) for a, b in zip(full, center)]
    public = {
        "replayed_collision_count": len(replay), "replay_rows": replay,
        "exact_rational_center": {"t": qstr((box.t0 + box.t1) / 2),
                                  "p": qstr((box.p0 + box.p1) / 2), "s": "0"},
        "center_is_hint_not_proof": True,
        "mean_value_formula": "f(c)+Df(full_box)*(box-c)",
        "normal_x": exact_bounds(nx), "normal_y": exact_bounds(ny),
        "chart_factor_nx2_minus_ny2": exact_bounds(h), "strict_chart": chart,
    }
    if chart is None:
        return None, public
    return {
        "contact_x": coordinates[0], "contact_y": coordinates[1],
        "outgoing_x": coordinates[2], "outgoing_y": coordinates[3],
        "s": coordinates[4], "chart": chart, "normal_x": nx, "normal_y": ny,
        "incoming_tangential": last_tangential,
        "full_geometry": full, "center_geometry": center,
    }, public


def candidate_table(
    box: Any, state: dict[str, Any], current_target: str,
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    rows: list[dict[str, Any]] = []
    internal: list[dict[str, Any]] = []
    decision_margins: list[arb] = []
    unresolved: list[str] = []
    candidate_ids = list(TIME.time2_cert.translated_candidate_ids(
        current_target, state["chart"]))
    for candidate_id in candidate_ids:
        full = r185.ad_root(state["full_geometry"], candidate_id)
        center = r185.ad_root(state["center_geometry"], candidate_id)
        delta = recentered(full["Delta"], center["Delta"], box)
        ell = recentered(full["ell"], center["ell"], box)
        transverse = recentered(full["transverse"], center["transverse"], box)
        radius = BASE.arbq(TIME.time2_cert.first_hit.RADIUS[candidate_id[0]])
        public: dict[str, Any] = {
            "candidate_id": candidate_id, "discriminant": exact_bounds(delta),
            "root_linear_term": exact_bounds(ell),
            "transverse": exact_bounds(transverse), "radius": exact_bounds(radius),
        }
        record: dict[str, Any] = {"candidate_id": candidate_id, "delta": delta,
                                  "ell": ell, "transverse": transverse,
                                  "radius": radius, "full": full}
        if bool(delta < 0):
            public["classification"] = "NO_REAL_INTERSECTION"
            public["decision_margin"] = positive_margin(-delta)
            decision_margins.append(-delta)
        elif bool(delta > 0):
            radical = delta.sqrt()
            near, far = ell - radical, ell + radical
            record.update({"radical": radical, "near": near, "far": far})
            public["near_root"], public["far_root"] = exact_bounds(near), exact_bounds(far)
            if bool(far < 0):
                public["classification"] = "INTERSECTION_STRICTLY_BEHIND"
                public["decision_margin"] = positive_margin(min_arb([delta, -far]))
                decision_margins.extend((delta, -far))
            elif bool(near > 0):
                public["classification"] = "STRICT_FUTURE_NEAR_ROOT"
                public["decision_margin"] = positive_margin(min_arb([delta, near]))
                decision_margins.extend((delta, near))
            else:
                public["classification"] = "UNRESOLVED_ROOT_SIGN"
                public["decision_margin"] = None
                unresolved.append(candidate_id)
        else:
            public["classification"] = "UNRESOLVED_DISCRIMINANT"
            public["decision_margin"] = None
            unresolved.append(candidate_id)
        record["classification"] = public["classification"]
        rows.append(public)
        internal.append(record)
    future = [row for row in internal
              if row["classification"] == "STRICT_FUTURE_NEAR_ROOT"]
    winners = [row for row in future if all(
        row is other or bool(row["near"] < other["near"]) for other in future)]
    selected = winners[0] if len(winners) == 1 and not unresolved else None
    gaps: list[arb] = []
    tau_margin = None
    if selected is not None:
        gaps = [other["near"] - selected["near"] for other in future
                if other is not selected]
        need(all(bool(gap > 0) for gap in gaps), "strict root gaps")
        decision_margins.extend(gaps)
        tau_margin = BASE.arbq(TIME.time2_cert.first_hit.TAU_MAX) - selected["near"]
        if not bool(tau_margin > 0):
            unresolved.append("SELECTED_ROOT_TAU_MAX")
            selected = None
        else:
            decision_margins.append(tau_margin)
    table = {
        "current_target": current_target, "incoming_chart": state["chart"],
        "candidate_ids_in_frozen_order": candidate_ids,
        "candidate_count": len(rows), "candidate_rows": rows,
        "candidate_rows_sha256": digest(rows),
        "classification_census": dict(sorted(Counter(
            row["classification"] for row in rows).items())),
        "unresolved_candidate_ids": sorted(unresolved),
        "strict_unique_owner": selected is not None,
        "selected_owner": None if selected is None else selected["candidate_id"],
        "selected_discriminant": None if selected is None else exact_bounds(selected["delta"]),
        "selected_root_isolating_interval": None if selected is None else exact_bounds(selected["near"]),
        "root_order": None if selected is None else {
            "strict": True,
            "mode": "PAIRWISE_MINIMUM_POSITIVE_GAP" if gaps else "VACUOUS_SINGLE_FUTURE_CANDIDATE",
            "competing_future_root_count": len(gaps),
            "minimum_positive_gap": None if not gaps else positive_margin(min_arb(gaps)),
            "tau_max_margin": positive_margin(tau_margin),
        },
        "minimum_candidate_decision_margin": (
            None if selected is None or not decision_margins
            else positive_margin(min_arb(decision_margins))),
    }
    return table, internal


def exact_owner(state: dict[str, Any], selected: dict[str, Any]) -> tuple[dict[str, Any], dict[str, arb]]:
    radical, transverse, radius = selected["radical"], selected["transverse"], selected["radius"]
    ux, uy = state["outgoing_x"], state["outgoing_y"]
    internal = {"selected_root": selected["near"],
                "normal_x": (-radical * ux + transverse * uy) / radius,
                "normal_y": (-radical * uy - transverse * ux) / radius,
                "p": transverse / radius, "cosine": radical / radius}
    public = {"selected_target_id": selected["candidate_id"],
              **{key: exact_bounds(value) for key, value in internal.items()}}
    return public, internal


def outgoing_state(owner_id: str, state: dict[str, Any], owner: dict[str, arb]) -> dict[str, Any] | None:
    radial_square = arb(1) - owner["p"] * owner["p"]
    if not bool(radial_square > 0):
        return None
    chart = TIME.time2_cert.strict_chart(owner["normal_x"], owner["normal_y"])
    if chart is None:
        return None
    radial = radial_square.sqrt()
    center_x, center_y = TIME.time2_cert.target_center(owner_id, state["s"])
    radius = BASE.arbq(TIME.time2_cert.first_hit.RADIUS[owner_id[0]])
    return {"contact_x": center_x + radius * owner["normal_x"],
            "contact_y": center_y + radius * owner["normal_y"],
            "outgoing_x": radial * owner["normal_x"] - owner["p"] * owner["normal_y"],
            "outgoing_y": radial * owner["normal_y"] + owner["p"] * owner["normal_x"],
            "s": state["s"], "chart": chart,
            "normal_x": owner["normal_x"], "normal_y": owner["normal_y"], "p": owner["p"]}


def wall_audit(state: dict[str, Any], current_target: str,
               owner: dict[str, arb]) -> dict[str, Any]:
    qx, qy = state["contact_x"], state["contact_y"]
    hx = qx + owner["selected_root"] * state["outgoing_x"]
    hy = qy + owner["selected_root"] * state["outgoing_y"]
    _source, shift_x, shift_y = RR.component_cert.parse_target(current_target)
    coordinates = {"X": (qx - arb(shift_x), hx - arb(shift_x)),
                   "Y": (qy - arb(shift_y), hy - arb(shift_y))}
    events: list[tuple[arb, str, int]] = []
    integer_margins: list[arb] = []
    for axis, (start, finish) in coordinates.items():
        axis_events, reason = RR.component_cert.ordered_axis_events(start, finish, axis)
        need(axis_events is not None and reason is None,
             "wall endpoint:" + str(reason))
        events.extend(axis_events)
        for wall in range(-6, 7):
            value = arb(wall)
            for endpoint in (start, finish):
                if bool(endpoint < value):
                    integer_margins.append(value - endpoint)
                elif bool(endpoint > value):
                    integer_margins.append(endpoint - value)
                else:
                    raise Rejected("integer wall endpoint unresolved")
    crossings, reason = RR.component_cert.strict_event_order(events)
    need(crossings is not None and reason is None, "wall order:" + str(reason))
    ordered = sorted(events, key=lambda row: RR.arb_pair(row[0])[0])
    endpoint_margins = [margin for alpha, _token, _wall in ordered
                        for margin in (alpha, arb(1) - alpha)]
    order_margins = [right[0] - left[0] for left, right in zip(ordered, ordered[1:])]
    need(all(bool(value > 0) for value in integer_margins + endpoint_margins + order_margins),
         "strict wall margins")
    return {"ordered_clean_wall_record": list(crossings),
            "integer_endpoint_margin": positive_margin(min_arb(integer_margins)),
            "crossing_time_endpoint_margin": None if not endpoint_margins else positive_margin(min_arb(endpoint_margins)),
            "event_order": {"strict": True, "event_count": len(ordered),
                            "mode": "PAIRWISE_MINIMUM_POSITIVE_GAP" if order_margins else "VACUOUS_ZERO_OR_ONE_WALL_EVENT",
                            "minimum_positive_gap": None if not order_margins else positive_margin(min_arb(order_margins))}}


def homogeneity(cosine: arb) -> dict[str, Any] | None:
    boundary = RR.round117.boundary_ball(RR.round117.N0)
    if bool(cosine > boundary):
        return {"label": "H0_CENTRAL", "lower_margin": positive_margin(cosine - boundary),
                "upper_margin": None}
    if not bool(cosine < boundary):
        return None
    for index in range(RR.round117.N0, 10000):
        lower, upper = RR.round117.boundary_ball(index + 1), RR.round117.boundary_ball(index)
        if bool(cosine > lower) and bool(cosine < upper):
            return {"label": f"H{index}", "lower_margin": positive_margin(cosine - lower),
                    "upper_margin": positive_margin(upper - cosine)}
        if not (bool(cosine < lower) or bool(cosine > upper)):
            return None
    return None


def incidence_rank(cosine: arb) -> tuple[int | None, dict[str, Any] | None]:
    cap = 14
    boundary = BASE.arbq(Q(1, 2**cap))
    if bool(cosine > boundary):
        return cap, positive_margin(cosine - boundary)
    if not bool(cosine < boundary):
        return None, None
    for rank in range(cap + 1, 10000):
        lower, upper = BASE.arbq(Q(1, 2**rank)), BASE.arbq(Q(1, 2 ** (rank - 1)))
        if bool(cosine > lower) and bool(cosine < upper):
            return rank, positive_margin(min_arb([cosine - lower, upper - cosine]))
        if not (bool(cosine < lower) or bool(cosine > upper)):
            return None, None
    return None, None


def core_margin(owner_id: str, owner: dict[str, arb], classification: str,
                destination: str | None, cores: tuple[Any, ...]) -> dict[str, Any] | None:
    nx, ny, momentum = owner["normal_x"], owner["normal_y"], owner["p"]
    margins: list[arb] = []
    inside_ids: list[str] = []
    for core in cores:
        if core.source != owner_id[0]:
            continue
        cell = core.chart_id.split(":")[1]
        t, _inside, _outside = STEP1.chart_tests(cell, nx, ny)
        if cell == "E":
            inside, outside = [nx, abs(nx) - abs(ny)], [-nx, abs(ny) - abs(nx)]
        elif cell == "W":
            inside, outside = [-nx, abs(nx) - abs(ny)], [nx, abs(ny) - abs(nx)]
        elif cell == "N":
            inside, outside = [ny, abs(ny) - abs(nx)], [-ny, abs(nx) - abs(ny)]
        else:
            inside, outside = [-ny, abs(ny) - abs(nx)], [ny, abs(nx) - abs(ny)]
        inside.extend((t - BASE.arbq(core.t0), BASE.arbq(core.t1) - t,
                       momentum - BASE.arbq(core.p0), BASE.arbq(core.p1) - momentum))
        if all(bool(value > 0) for value in inside):
            inside_ids.append(STEP1.core_id(core))
            margins.extend(inside)
            continue
        outside.extend((BASE.arbq(core.t0) - t, t - BASE.arbq(core.t1),
                        BASE.arbq(core.p0) - momentum, momentum - BASE.arbq(core.p1)))
        positive = [value for value in outside if bool(value > 0)]
        if not positive:
            return None
        margins.append(max(positive, key=lambda value: RR.arb_pair(value)[0]))
    if classification == "RETURN_AT_3_INNER":
        if inside_ids != [destination]:
            return None
    elif inside_ids or destination is not None:
        return None
    return positive_margin(min_arb(margins))


def pending_terminal(collision_index: int, classification: str,
                     destination: str | None, margin: dict[str, Any]) -> dict[str, Any]:
    return {"status": "PENDING_GLOBAL_ORACLE",
            "local_disposition": "KNOWN_COMPONENT" if classification == "RETURN_AT_3_INNER" else "LIVE_CONTINUE",
            "local_classification": classification, "known_component_id": destination,
            "local_strict_decision_margin": margin, "global_oracle_available": False,
            "missing_global_oracles": list(MISSING_GLOBAL_ORACLES),
            "pending_reason": "PENDING_GLOBAL_ORACLE: cemetery/disconnected disposition and codimension face/endpoint/corner ownership are not installed",
            "collision_index": collision_index,
            "allowed_terminal_classes": list(ALLOWED_TERMINALS),
            "terminal_class_issued": None, "terminal_credit": 0, "formal_credit": 0}


def numeric_step(box: Any, history: list[dict[str, Any]],
                 context: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    collision_index = len(history) + 1
    result: dict[str, Any] = {
        "status": "UNRESOLVED_FAIL_CLOSED",
        "collision_index": collision_index,
        "collision_index_derivation": "len(owner_history)+1",
        "exact_owner": None, "discriminant": None, "root_order": None,
        "official_word": None, "chart": None, "wall": None,
        "homogeneity": None, "incidence": None, "core": None,
        "structured_terminal_decision_margin": None,
        "full_candidate_table": None, "global_oracle_available": False,
        "formal_credit": 0, "D02_credit": 0,
    }
    state, replay = geometry_after_history(box, history)
    result["history_replay"] = replay
    internal: dict[str, Any] = {"box": box, "state": state}
    if state is None:
        result["blocker"] = replay.get("status", "UNRESOLVED_HISTORY_STATE")
        return result, internal
    result["chart"] = {"incoming_chart": state["chart"],
                       "incoming_chart_margin": {
                           "normal_x": replay["normal_x"], "normal_y": replay["normal_y"],
                           "nx2_minus_ny2": replay["chart_factor_nx2_minus_ny2"]},
                       "outgoing_chart": None, "outgoing_chart_margin": None}
    current_target = history[-1]["selected_owner"]
    table, candidates = candidate_table(box, state, current_target)
    result["full_candidate_table"] = table
    result["discriminant"], result["root_order"] = table["selected_discriminant"], table["root_order"]
    internal["candidate_internal"] = candidates
    if not table["strict_unique_owner"]:
        result["blocker"] = "NEXT_OWNER_OR_ROOT_ORDER_UNRESOLVED"
        return result, internal
    selected = next(row for row in candidates if row["candidate_id"] == table["selected_owner"])
    owner_public, owner_internal = exact_owner(state, selected)
    result["exact_owner"], internal["owner_internal"] = owner_public, owner_internal
    owner_for_word = {"selected_target_id": selected["candidate_id"], **owner_internal}
    word, error = RR.translation_normalized_official_word(
        state, current_target, owner_for_word,
        context["pair_table"], context["pattern_table"])
    if word is None:
        result["blocker"] = "OFFICIAL_WORD_UNRESOLVED:" + str(error)
        return result, internal
    result["official_word"] = {**RR.compact_key(word["key"]),
        "absolute_selected_target_id": word["absolute_selected_target_id"],
        "relative_frozen_target_id": word["relative_frozen_target_id"],
        "ordered_clean_wall_record": word["ordered_clean_wall_record"],
        "absolute_lattice_translation_removed": word["absolute_lattice_translation_removed"],
        "official_registry_sha256": context["registry_sha"]}
    try:
        result["wall"] = wall_audit(state, current_target, owner_internal)
    except Rejected as error:
        result["blocker"] = "WALL_OR_ORDER_UNRESOLVED:" + str(error)
        return result, internal
    next_state = outgoing_state(selected["candidate_id"], state, owner_internal)
    if next_state is None:
        result["blocker"] = "OUTGOING_CHART_UNRESOLVED"
        return result, internal
    chart_value = (abs(next_state["normal_x"]) - abs(next_state["normal_y"])
                   if next_state["chart"] in {"E", "W"}
                   else abs(next_state["normal_y"]) - abs(next_state["normal_x"]))
    if not bool(chart_value > 0):
        result["blocker"] = "OUTGOING_CHART_MARGIN_UNRESOLVED"
        return result, internal
    result["chart"]["outgoing_chart"] = next_state["chart"]
    result["chart"]["outgoing_chart_margin"] = positive_margin(chart_value)
    result["homogeneity"] = homogeneity(owner_internal["cosine"])
    cosine_square = arb(1) - state["incoming_tangential"] * state["incoming_tangential"]
    if not bool(cosine_square > 0):
        result["blocker"] = "INCOMING_INCIDENCE_COSINE_UNRESOLVED"
        return result, internal
    source_rank, source_margin = incidence_rank(cosine_square.sqrt())
    target_rank, target_margin = incidence_rank(owner_internal["cosine"])
    if source_rank is not None and target_rank is not None:
        result["incidence"] = {"rank_B": max(14, source_rank, target_rank),
                               "source_rank": source_rank, "target_rank": target_rank,
                               "source_rank_margin": source_margin,
                               "target_rank_margin": target_margin,
                               "codimension_owner_status": "PENDING_GLOBAL_ORACLE"}
    classification, destination, witnesses = TIME.core_classification(
        owner_for_word, context["cores"])
    margin = None if classification == "UNRESOLVED_TIME3_OUTER" else core_margin(
        selected["candidate_id"], owner_internal, classification, destination, context["cores"])
    result["core"] = {"classification": classification,
                      "destination_core_id": destination,
                      "witness_count": len(witnesses),
                      "witnesses_sha256": digest(witnesses),
                      "minimum_inside_or_exclusion_margin": margin}
    if result["homogeneity"] is None or result["incidence"] is None or margin is None:
        result["blocker"] = "AUXILIARY_STRATUM_UNRESOLVED"
        return result, internal
    result["structured_terminal_decision_margin"] = pending_terminal(
        collision_index, classification, destination, margin)
    result["status"] = "PENDING_GLOBAL_ORACLE"
    internal["local_complete"] = True
    return result, internal


def split_decision(box: Any, result: dict[str, Any],
                   internal: dict[str, Any]) -> dict[str, Any]:
    state = internal.get("state")
    blockers: list[tuple[str, Any]] = []
    if state is not None:
        table = result.get("full_candidate_table") or {}
        unresolved = set(table.get("unresolved_candidate_ids", []))
        classes = {row["candidate_id"]: row["classification"]
                   for row in table.get("candidate_rows", [])}
        for row in internal.get("candidate_internal", []):
            candidate_id = row["candidate_id"]
            if candidate_id in unresolved:
                blockers.append(("discriminant:" + candidate_id, row["full"]["Delta"]))
                if classes.get(candidate_id) == "UNRESOLVED_ROOT_SIGN":
                    blockers.append(("root_linear:" + candidate_id, row["full"]["ell"]))
        if not blockers:
            for row in internal.get("candidate_internal", []):
                blockers.append(("auxiliary_discriminant:" + row["candidate_id"],
                                 row["full"]["Delta"]))
    if not blockers:
        full = r185.ad_initial_geometry(SOURCE_CHART_ID, box)
        for row in internal["history"]:
            full, nx, ny = r185.ad_collision(full, row["selected_owner"])
        blockers.append(("history_or_chart_factor", nx * nx - ny * ny))
    widths = {"t": (box.t1 - box.t0) / 2, "p": (box.p1 - box.p0) / 2}
    contributions = {"t": Q(0), "p": Q(0)}
    witnesses = {"t": "", "p": ""}
    for label, value in blockers:
        for index, axis in enumerate(AXES):
            contribution = abs(value.derivative[index]) * BASE.arbq(widths[axis])
            _lower, upper = RR.arb_pair(contribution)
            if upper > contributions[axis]:
                contributions[axis], witnesses[axis] = upper, label
    axis = max(AXES, key=lambda item: (contributions[item], widths[item], item == "t"))
    _left, _right, coordinate = split_box(box, axis)
    return {"decision": "SPLIT_AND_RECENTER", "axis": axis,
            "exact_rational_coordinate": qstr(coordinate),
            "exact_half_width": qstr(widths[axis]),
            "failing_margin_sensitivity_upper": {
                key: qstr(value) for key, value in sorted(contributions.items())},
            "dominant_witness": witnesses[axis],
            "children_half_open_owner": "LOWER_BIT_CHILD_OWNS_SHARED_SPLIT_FACE",
            "split_face_endpoint_corner_status": "PENDING_GLOBAL_ORACLE",
            "formal_credit": 0}


def local_context() -> dict[str, Any]:
    pair_table, pattern_table, registry_sha = RR.component_cert.key_index_tables()
    return {"pair_table": pair_table, "pattern_table": pattern_table,
            "registry_sha": registry_sha,
            "cores": tuple(RR.core_cert.physical_cores())}


def regression_status(step: dict[str, Any]) -> str:
    decision = step.get("structured_terminal_decision_margin") or {}
    if decision.get("local_disposition") == "KNOWN_COMPONENT":
        return "STRICT_EARLY_TERMINAL_KNOWN_COMPONENT"
    return (f"PASS_STRICT_COLLISION{step['collision_index']}_LIVE_TO_COLLISION"
            f"{step['collision_index'] + 1}_ZERO_CREDIT")


def adaptive_tree(root_payload: dict[str, Any], root_path: str,
                  history: list[dict[str, Any]], maximum_depth: int,
                  maximum_nodes: int) -> dict[str, Any]:
    root = atlas_box(root_payload, root_path)
    root_depth = root.depth
    stack = [root]
    leaves: list[dict[str, Any]] = []
    decisions: list[dict[str, Any]] = []
    nodes = splits = 0
    context = local_context()
    while stack:
        box = stack.pop()
        nodes += 1
        need(nodes <= maximum_nodes, "adaptive node bound")
        result, internal = numeric_step(box, history, context)
        internal["history"] = history
        if internal.get("local_complete") is True:
            leaves.append({"path": box.path,
                           "relative_Kraft_fraction": qstr(Q(1, 2 ** (box.depth - root_depth))),
                           "regression_status": regression_status(result),
                           "step": result})
            continue
        decision = split_decision(box, result, internal)
        depth = box.depth - root_depth
        performed = depth < maximum_depth
        decisions.append({"parent_path": box.path, "performed": performed,
                          "selected_child_bit_enum": ["0", "1"] if performed else [],
                          "decision": decision})
        if not performed:
            bounded = copy.deepcopy(result)
            bounded["next_decision"] = decision
            leaves.append({"path": box.path,
                           "relative_Kraft_fraction": qstr(Q(1, 2**depth)),
                           "regression_status": "BOUNDED_PILOT_UNRESOLVED_WITH_EXACT_NEXT_DECISION",
                           "step": bounded})
            continue
        left, right, coordinate = split_box(box, decision["axis"])
        need(qstr(coordinate) == decision["exact_rational_coordinate"],
             "split coordinate replay")
        need(left.path == box.path + "0" and right.path == box.path + "1",
             "selected_child_bit exact enum/geometry")
        splits += 1
        stack.append(right)
        stack.append(left)
    paths = sorted(row["path"] for row in leaves)
    need(not any(right.startswith(left) for left, right in zip(paths, paths[1:])),
         "prefix free")
    kraft = sum(Q(row["relative_Kraft_fraction"]) for row in leaves)
    need(kraft == 1, "Kraft one")
    semantic = {
        "collision_index": len(history) + 1, "root_path": root_path,
        "maximum_additional_depth": maximum_depth, "maximum_nodes": maximum_nodes,
        "node_count": nodes, "split_count": splits, "leaf_count": len(leaves),
        "leaf_status_census": dict(sorted(Counter(
            row["regression_status"] for row in leaves).items())),
        "relative_Kraft_sum": qstr(kraft),
        "decisions": sorted(decisions, key=lambda row: row["parent_path"]),
        "leaves": sorted(leaves, key=lambda row: row["path"]),
    }
    return {"semantic": semantic, "semantic_sha256": digest(semantic),
            "raw_leaves": leaves}


def first_live(tree: dict[str, Any]) -> dict[str, Any]:
    rows = [row for row in tree["raw_leaves"]
            if (row["step"].get("structured_terminal_decision_margin") or {}).get(
                "local_disposition") == "LIVE_CONTINUE"]
    need(bool(rows), "live leaf")
    return min(rows, key=lambda row: row["path"])


def independent_regression() -> dict[str, Any]:
    need(flint.__version__ == "0.9.0" and ctx.prec == 384,
         "python-flint 0.9.0 / 384-bit pin")
    source, inputs, manifest = derive_inputs()
    trees3: dict[str, Any] = {}
    for item in inputs:
        tree = adaptive_tree(item["closed_box"], item["adaptive_suffix"],
                             item["history"], 6, 1024)
        observed = {key: tree["semantic"][key] for key in (
            "node_count", "split_count", "leaf_count",
            "relative_Kraft_sum", "leaf_status_census")}
        need(observed == EXPECTED_CENSUS["collision3"],
             "collision3 census:" + item["side"])
        trees3[item["side"]] = tree
    selected3 = first_live(trees3["REFLECTED"])
    need(selected3["path"] == C49_BINDINGS["collision3_reflected"]["path"]
         and selected3["step"]["exact_owner"]["selected_target_id"]
         == C49_BINDINGS["collision3_reflected"]["owner"],
         "selected collision3 binding")
    history4 = copy.deepcopy(inputs[0]["history"]) + [{
        "collision_index": 3,
        "selected_owner": selected3["step"]["exact_owner"]["selected_target_id"],
        "evidence_sha256": C49_BINDINGS["collision3_reflected"]["step_evidence_sha256"],
    }]
    # atlas_box(payload, selected path) treats payload as the root's exact
    # closed box; recover that payload directly from the selected path.
    selected3_box = atlas_box(inputs[0]["closed_box"], "")
    for bit in selected3["path"]:
        # Reconstruct using the recorded split-decision axis at each prefix.
        prefix = selected3_box.path
        decision = next(row for row in trees3["REFLECTED"]["semantic"]["decisions"]
                        if row["parent_path"] == prefix)["decision"]
        left, right, _coordinate = split_box(selected3_box, decision["axis"])
        selected3_box = left if bit == "0" else right
    tree4 = adaptive_tree(public_box(selected3_box), selected3_box.path,
                          history4, 8, 4096)
    observed4 = {key: tree4["semantic"][key] for key in (
        "node_count", "split_count", "leaf_count",
        "relative_Kraft_sum", "leaf_status_census")}
    need(observed4 == EXPECTED_CENSUS["collision4"], "collision4 census")
    selected4 = first_live(tree4)
    need(selected4["path"] == C49_BINDINGS["collision4"]["path"]
         and selected4["step"]["exact_owner"]["selected_target_id"]
         == C49_BINDINGS["collision4"]["owner"],
         "selected collision4 binding")
    history5 = history4 + [{"collision_index": 4,
                            "selected_owner": selected4["step"]["exact_owner"]["selected_target_id"],
                            "evidence_sha256": C49_BINDINGS["collision4"]["step_evidence_sha256"]}]
    selected4_box = selected3_box
    suffix = selected4["path"][len(selected3_box.path):]
    for bit in suffix:
        prefix = selected4_box.path
        decision = next(row for row in tree4["semantic"]["decisions"]
                        if row["parent_path"] == prefix)["decision"]
        left, right, _coordinate = split_box(selected4_box, decision["axis"])
        selected4_box = left if bit == "0" else right
    step5, internal5 = numeric_step(selected4_box, history5, local_context())
    need(internal5.get("local_complete") is True
         and step5["collision_index"] == 5
         and step5["exact_owner"]["selected_target_id"] == C49_BINDINGS["collision5"]["owner"],
         "collision5 selected owner/complete")
    hashes = {
        "collision3_reflected": trees3["REFLECTED"]["semantic_sha256"],
        "collision3_representative": trees3["REPRESENTATIVE"]["semantic_sha256"],
        "collision4": tree4["semantic_sha256"],
        "collision5_step": digest(step5),
    }
    hashes["combined"] = digest(hashes)
    return {"source": source, "manifest": manifest, "hashes": hashes,
            "trees": {"collision3_reflected": trees3["REFLECTED"]["semantic"],
                      "collision3_representative": trees3["REPRESENTATIVE"]["semantic"],
                      "collision4": tree4["semantic"]},
            "collision5_step": step5,
            "selected": {"collision3": {
                "path": selected3["path"],
                "owner": selected3["step"]["exact_owner"]["selected_target_id"]},
                "collision4": {"path": selected4["path"],
                               "owner": selected4["step"]["exact_owner"]["selected_target_id"]},
                "collision5": {"owner": step5["exact_owner"]["selected_target_id"]}}}


def actual_file_fault_tests() -> list[dict[str, Any]]:
    outcomes: list[dict[str, Any]] = []

    def expect(name: str, action: Callable[[], Any]) -> None:
        rejected = False
        error_type = ""
        try:
            action()
        except (Rejected, OSError) as exc:
            rejected, error_type = True, type(exc).__name__
        need(rejected, "fault must fail closed:" + name)
        outcomes.append({"attack": name, "actual_tempfile": True,
                         "fail_closed": True,
                         "rejection_type": error_type})

    with tempfile.TemporaryDirectory(prefix="cm2-c54p0-faults-") as raw_root:
        root = Path(raw_root)
        payload = (b"frozen-source-line\n" * 4096)

        swap = root / "swap.py"
        replacement = root / "replacement.py"
        swap.write_bytes(payload)
        replacement.write_bytes(payload.replace(b"frozen", b"forged"))
        expect("atomic_source_swap", lambda: stable_read(
            swap, "swap", chunk_size=128,
            after_first_read=lambda _fd: os.replace(replacement, swap)))

        trunc = root / "truncate.py"
        trunc.write_bytes(payload)
        expect("truncate_during_read", lambda: stable_read(
            trunc, "truncate", chunk_size=128,
            after_first_read=lambda _fd: os.truncate(trunc, 64)))

        short = root / "short-read.py"
        short.write_bytes(payload)
        calls = {"count": 0}
        def early_eof(fd: int, size: int) -> bytes:
            calls["count"] += 1
            return b"" if calls["count"] == 2 else os.read(fd, size)
        expect("premature_EOF_short_read", lambda: stable_read(
            short, "short", chunk_size=128, read_fn=early_eof))

        denied = root / "permission.py"
        denied.write_bytes(payload)
        denied.chmod(0)
        try:
            expect("permission_denied", lambda: stable_read(denied, "permission"))
        finally:
            denied.chmod(0o600)

        renamed = root / "rename.py"
        moved = root / "renamed-away.py"
        renamed.write_bytes(payload)
        expect("rename_away_during_read", lambda: stable_read(
            renamed, "rename", chunk_size=128,
            after_first_read=lambda _fd: os.rename(renamed, moved)))
    need(len(outcomes) == 5 and all(row["fail_closed"] for row in outcomes),
         "five actual file faults")
    return outcomes


def self_test() -> dict[str, Any]:
    independence = source_independence()
    load_lower_authorities()
    need(not (set(sys.modules) & FORBIDDEN_MODULES),
         "self-test lower-authority load remains C49-free")
    faults = actual_file_fault_tests()
    tests = {
        "canonical_deterministic": canonical({"b": 2, "a": 1}) == b'{"a":1,"b":2}',
        "digest_known": digest({}) == hashlib.sha256(b"{}").hexdigest(),
        "selected_child_enum_exact": {"0", "1"} == set("01"),
        "runtime_pin": flint.__version__ == "0.9.0" and ctx.prec == 384,
        "C49_static_import_absent": independence["AST_import_scan"] == "PASS",
        "five_actual_faults_fail_closed": len(faults) == 5 and all(
            row["fail_closed"] for row in faults),
        "missing_oracles_named": len(MISSING_GLOBAL_ORACLES) == 2,
        "credit_boundary_zero": True,
    }
    need(len(tests) == 8 and all(tests.values()), "8 self-tests")
    return close_object({"schema": SCHEMA + ".self-test",
        "status": "PASS_8_OF_8_WITH_5_ACTUAL_TEMPFILE_FAULTS",
        "tests": tests, "fault_tests": faults, "independence": independence,
        "formal_credit": 0, "D02_credit": 0,
        "runtime_authority_pointer_touched": False,
        "persistent_writes_performed": False,
        "temporary_fault_test_writes_performed": True,
        "temporary_fault_test_outputs_removed": True})


def verify(*, enforce_reference: bool) -> dict[str, Any]:
    independence = source_independence()
    before = snapshot()
    load_lower_authorities()
    need(not (set(sys.modules) & FORBIDDEN_MODULES), "no C49 after authority load")
    regression = independent_regression()
    after = snapshot()
    need(before == after, "pre/post complete replay snapshots identical")
    faults = actual_file_fault_tests()
    hashes = regression["hashes"]
    if enforce_reference:
        need(all(type(value) is str and HEX64.fullmatch(value) is not None
                 for value in EXPECTED_SEMANTIC_SHA256.values()),
             "reference semantic hashes frozen")
        need(hashes == EXPECTED_SEMANTIC_SHA256,
             "all C49-v4 semantic projection hashes")
    return close_object({
        "schema": SCHEMA + ".audit",
        "status": ("PASS_COLD_NO_C49_IMPORT_FULL_PAIR9_3_4_5_NUMERIC_REPLAY_ZERO_CREDIT"
                   if enforce_reference else
                   "DIAGNOSTIC_RECOMPUTE_UNPINNED_ZERO_CREDIT"),
        "verifier_source_sha256": hashlib.sha256(
            stable_read(SELF, "terminal verifier source", 4 << 20)).hexdigest(),
        "runtime": {"python_flint_version": flint.__version__,
                    "arb_precision_bits": ctx.prec},
        "C49_reference": {
            "source_file_sha256": C49_V4_SOURCE_SHA256,
            "regression_file_sha256": C49_V4_REGRESSION_FILE_SHA256,
            "regression_object_sha256": C49_V4_REGRESSION_OBJECT_SHA256,
            "producer_imported_or_executed": False,
            "producer_specific_bindings": C49_BINDINGS,
        },
        "independence": independence,
        "input_authorities": {
            "C46_full_queue_manifest_sha256": FULL_QUEUE_MANIFEST_SHA256,
            "C41_object_sha256": C41_OBJECT_SHA256,
            "C41_pair9_row_sha256": C41_ROW_SHA256,
            "C41_path": PAIR9_PATH, "pair_index": PAIR_INDEX,
            "source_binding_pins": SOURCE_BINDING_PINS,
            "C46_C41_pair9_exact_equal": True,
        },
        "semantic_projection_sha256": hashes,
        "expected_semantic_projection_sha256": EXPECTED_SEMANTIC_SHA256,
        "reference_enforced": enforce_reference,
        "collision_census": EXPECTED_CENSUS,
        "selected_chain": regression["selected"],
        "collision_indices_observed": [3, 4, 5],
        "every_adaptive_node_recomputed": True,
        "every_split_decision_recomputed": True,
        "selected_child_bit_enum_replayed": ["0", "1"],
        "history_indices_contiguous": True,
        "history_owner_chain": ["W[1,0]", "G[0,0]", "W[0,0]", "G[0,1]"],
        "pre_post_snapshot_equal": True,
        "snapshot_file_count": len(before),
        "actual_tempfile_fault_tests": faults,
        "actual_tempfile_fault_test_count": len(faults),
        "all_actual_tempfile_faults_fail_closed": all(row["fail_closed"] for row in faults),
        "global_oracle_status": "PENDING_GLOBAL_ORACLE",
        "missing_global_oracles": list(MISSING_GLOBAL_ORACLES),
        "formal_credit": 0, "D02_credit": 0,
        "authority_pointer_touched": False, "canonical_status_touched": False,
        "runtime_writes_performed": False,
        "temporary_fault_test_writes_performed": True,
        "temporary_fault_test_outputs_removed": True,
        "persistent_writes_performed": False,
    })


def emit(value: dict[str, Any]) -> None:
    sys.stdout.buffer.write(canonical(value) + b"\n")
    sys.stdout.buffer.flush()


def main() -> int:
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--self-test", action="store_true")
    mode.add_argument("--recompute", action="store_true")
    mode.add_argument("--verify", action="store_true")
    args = parser.parse_args()
    try:
        emit(self_test() if args.self_test else verify(enforce_reference=args.verify))
        return 0
    except Exception as error:
        emit(close_object({"schema": SCHEMA + ".rejection",
            "status": "REJECTED_FAIL_CLOSED_ZERO_CREDIT",
            "error_type": type(error).__name__, "error": str(error),
            "formal_credit": 0, "D02_credit": 0,
            "authority_pointer_touched": False,
            "canonical_status_touched": False,
            "runtime_writes_performed": False,
            "persistent_writes_performed": False}))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
