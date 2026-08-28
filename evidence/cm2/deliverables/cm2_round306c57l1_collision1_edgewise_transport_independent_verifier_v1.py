#!/usr/bin/env python3
"""Independent fail-closed verifier for the frozen C57-L1 candidate.

The C57-L1 producer is treated as an inert, hash-pinned byte string.  It is
never imported, decoded as Python, compiled, evaluated, or executed.  All
candidate rows are instead checked against the frozen C56/C55B/C35/C36 and
C38->C39->C40->C41 inputs by this separate implementation.
"""

from __future__ import annotations

import ast
import copy
import hashlib
import json
import os
import platform
import re
import stat
import sys
import zlib
from collections import Counter, defaultdict
from fractions import Fraction
from pathlib import Path
from typing import Any, Callable, Iterable


sys.dont_write_bytecode = True
SELF = Path(__file__).absolute()
ROOT = SELF.parent.parent
OUT = SELF.parent
PREFIX = "cm2_round306c57l1_collision1_edgewise_transport"
SCHEMA = "cm2.round306c57l1.collision1-edgewise-transport.v1"
VERIFY_SCHEMA = SCHEMA + ".independent-verification.v1"

PRODUCER = OUT / (PREFIX + "_v1.py")
RESULT = OUT / (PREFIX + "_result_v1.json")
VERIFICATION = OUT / (PREFIX + "_independent_verification_v1.json")
CHAIN = OUT / (PREFIX + "_upstream_task_chains_v1.jsonl.gz")
LOCAL = OUT / (PREFIX + "_local_collision1_cell_status_v1.jsonl.gz")
EDGE = OUT / (PREFIX + "_edge_obligations_v1.jsonl.gz")
CELL = OUT / (PREFIX + "_corridor_cell_transport_v1.jsonl.gz")
HANDOFF = OUT / (PREFIX + "_collision2_ready_handoff_v1.jsonl.gz")

C56_RESULT = OUT / "cm2_round306c56l_large_component_common_refinement_result_v1.json"
C56_VERIFY = OUT / "cm2_round306c56l_large_component_common_refinement_independent_verification_v1.json"
C55B_RESULT = OUT / "cm2_round306c55b_global_component_adjacency_known_sheet_result_v1.json"
C35 = ROOT / ".cm2-runtime/candidates/c35-transition-registry-20260810T145204Z-43f2cb35f9817ae2"
C36 = ROOT / ".cm2-runtime/candidates/c36-template-margin-atlas-20260810T153254Z-f37f908cf93d924c"
C38 = ROOT / ".cm2-runtime/candidates/c38-collision1-2-child-atlas-20260810T180156Z-0d5047fe3a316133"
C39 = ROOT / ".cm2-runtime/candidates/c39-h1-c1-graph-router-20260810T185014Z-e004fadaadcd5559"
C40 = ROOT / ".cm2-runtime/candidates/c40-h1-endpoint-c2-arrangement-20260810T234000Z-c2f144e29bc1172f"
C41 = ROOT / ".cm2-runtime/candidates/c41-lower-strata-depth3-20260811T023804Z-f997365c91559599"
C50A_MANIFEST = OUT / "cm2_round306c50a_global_codimension_owner_oracle_manifest_v1.sha256"
C50A_RESULT = OUT / "cm2_round306c50a_pair1_two_task_global_owner_result_v1.json"
C50A_VERIFY = OUT / "cm2_round306c50a_pair1_two_task_global_owner_independent_verification_v1.json"
C53_HEAD = ROOT / ".cm2-runtime/cm2-global-authority-heads/predecessor-10fb050d30c92b0f2bdcf85a30d28ff670d8efc0b48104b7f04a63c391967b41.seal"
CANONICAL = OUT / "CM2_LATEST_STATUS.md"

HEX64 = re.compile(r"[0-9a-f]{64}\Z")
ALGEBRAIC = {"-1/sqrt(2)", "+1/sqrt(2)"}
SEED_SCOPE = "DUAL_R139_SEED_COLLARS_ONLY"
COLLISION2_PREFIX = "UNRESOLVED_C41_COLLISION2_"

PINS = {
    "producer_file": "a9d25c84a3845c766ccfe33dd090b12b05c5e5ce0aace423ec21e79cc5b31247",
    "result_file": "4126bea2ede296939963a886699cf69a7189ab11015180e9cdf03c25f985325c",
    "result_object": "ca5be921350a34770f5fe12e0734ab55e7fc707c97685c7aa07c2cf53760c6a0",
    "C56_result_file": "99e5fc0019ae21e7bc68d0c2b997ed62e9c47b28fd47d366237b0c06b1d82601",
    "C56_result_object": "0ab2c1ea9086db7f05d9b0c7f96d4348b0b2d8c9f54b47bd8e57aa570133a637",
    "C56_verify_file": "4a3d90843ee1401b32ef02af3eb5eb9ffdee773c4abeb0d096b9bcfe6e3ae6f2",
    "C56_verify_object": "c793495f11962757a1e1ac55539ee7260d59d7e084662eb954a8a973466a70a5",
    "C55B_result_file": "6bf9cae7b4b422c5c2121f95828e1508700fe1a5d1b1128598c8617f65032a93",
    "C55B_result_object": "1ce396e9746d3c0364325e8308e94c9dcd4a3bfbba8c17a9c9961915e807cc56",
    "C35_result_file": "3122c977e47c1b1f685f7c97f3b9d68e9ff79d477916cb8bd4556f4b518c17ad",
    "C35_object": "cb524ae587390a578683c88d933125e041ab2a906f0351370d58f3b0d67aa752",
    "C36_result_file": "7922139708dc486232ec79b29d6339bdca7e00999bddf63d5b9a83b3f4cfbbd1",
    "C36_object": "9251693da7d6cc0ff6011fb965276ac64be2b79be8f245ab8954291a43fb4167",
    "C38_result_file": "094eb7cf3fca64451aaad80bdd970a8a39a58244e492ed3d2c69f63c70ed3501",
    "C38_object": "fba83cdd6eb0eb7d0b71989189ad61ba099e0c440b1f31c3c5aa01b9fbc4f434",
    "C39_result_file": "f9bfacbdaaf5263ba16397e70fe56b4f31149087c2434b7c163ff284b40cfd7e",
    "C39_object": "821c84d3793bcd941e0a574302bf6c5a0835b46f852156a56fde6ec0353d7e02",
    "C40_result_file": "f721b08a4addb7c0369b27ea3af8546c9fad293b1a7808d015bbf783b3aa22d6",
    "C40_object": "397eda962e4bd20429d7cab1ffc53d82cccfdf59bdce8cd03b271a8ded0536ba",
    "C41_result_file": "73fde0eee7eb06bb0f144ea98880c72bfea36e10db696731ae72393cd9b0a50f",
    "C41_object": "b7e47a4ca9d6f4bb1fee10e78877850d5070f6d3c2b06bb0234fbabdaa2b7b24",
    "C50A_manifest_file": "07444544362d8b25d7d5d735e17ad08057dfc459d166ade868a073c2ce4c50f6",
    "C53_head_file": "f62483c87df4b6f4a8a2ad8dcf56febbfce9977200ce94a0ad6ce38e736aeeb3",
    "C53_head_object": "cb90ab914c3b6518384669f42d05df33c21a717596190131c6a0f5683934cbfb",
    "C53_checkpoint": "b58d68a0234b8a7de0e9147f891d37910476d622b840cfa073aed7ff3b4382ab",
    "canonical_file": "922fc5d01918b217556bc3f392c44efcc7c9c6345c881371e6cd34950eb99b57",
}

CANDIDATE_DESCRIPTORS = {
    "upstream_task_chains": {
        "filename": CHAIN.name, "order": "C56L_POST_C53_TASK_ORDER", "row_count": 33319,
        "row_hash_line_sequence_sha256": "2982921dcc3b86010bda8e032a20418daf605688b35fdb8dd2a4fda2c73929d9",
        "sha256": "1b6f852bdd551b27c1b58af431a79942401783c16bb73c47a7275b4a410d688f", "size": 5737544,
    },
    "local_collision1_cell_status": {
        "filename": LOCAL.name, "order": "COMPONENT_INDEX_THEN_CELL_ID", "row_count": 1044,
        "row_hash_line_sequence_sha256": "204090eb121f2a7574c06c22059122cc9633d190d41a6a1917fae617e4798d0f",
        "sha256": "e328bf27a200d52f536b4d019c12c7e37198cb9942bee4dddc32b730c3fcf28d", "size": 234710,
    },
    "edge_obligations": {
        "filename": EDGE.name, "order": "COMPONENT_INDEX_THEN_SOURCE_CELL_ID", "row_count": 1042,
        "row_hash_line_sequence_sha256": "c219895b871c1f6a1adba30d9022470beced9076b21837681c37dd9ade779b28",
        "sha256": "7136dd4585a5ed9de158c0710c6386ece4d8870ab0196db2e373881779c3dbcd", "size": 476907,
    },
    "corridor_cell_transport": {
        "filename": CELL.name, "order": "COMPONENT_INDEX_THEN_CELL_ID", "row_count": 1044,
        "row_hash_line_sequence_sha256": "56f838323b8eb49a01044711d443dbf5f9b41c78e367ccda01d4ec4614b24e8e",
        "sha256": "3f61330c3eafa9101b083b8b6061ee334738bfa3129280874e1a3f7d239e1ac5", "size": 230826,
    },
    "collision2_ready_handoff": {
        "filename": HANDOFF.name, "order": "EMPTY_NO_COLLISION2_READY_HANDOFFS", "row_count": 0,
        "row_hash_line_sequence_sha256": hashlib.sha256(b"").hexdigest(),
        "sha256": "9ceffb7310338057cfe71a4ae1e2c98d2c485d81cdef906532a801f457a38d64", "size": 20,
    },
}

EDGE_REASONS = [
    "C36_OCCURRENCE1_MARGIN_SCOPE_DUAL_R139_SEED_COLLARS_ONLY",
    "C36_NO_C32_FACE_LIPSCHITZ_OR_VARIATION_BOUND",
    "C50A_NO_FROZEN_C57L1_EDGE_OWNER_REQUEST_OR_AUDIT",
    "NO_C41_SPLIT_HISTORY_COMMON_FACE_CROSSWALK",
]


class Rejected(RuntimeError):
    pass


def need(condition: bool, label: str) -> None:
    if type(condition) is not bool or not condition:
        raise Rejected(label)


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False).encode("utf-8")


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def duplicate_guard(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise Rejected("duplicate JSON key:" + key)
        result[key] = value
    return result


def parse_json(raw: bytes, label: str, canonical_line: bool = False) -> Any:
    need(bool(raw) and not raw.startswith(b"\xef\xbb\xbf"), label + ":strict non-BOM bytes")
    try:
        value = json.loads(
            raw.decode("utf-8", "strict"), object_pairs_hook=duplicate_guard,
            parse_constant=lambda token: (_ for _ in ()).throw(Rejected(label + ":" + token)),
        )
    except Rejected:
        raise
    except Exception as exc:
        raise Rejected(label + ":JSON:" + str(exc)) from exc
    if canonical_line:
        need(raw == canonical(value) + b"\n", label + ":canonical line")
    return value


def stat_record(value: os.stat_result) -> dict[str, int]:
    return {
        "device": value.st_dev, "inode": value.st_ino, "mode": value.st_mode,
        "nlink": value.st_nlink, "size": value.st_size,
        "mtime_ns": value.st_mtime_ns, "ctime_ns": value.st_ctime_ns,
    }


def same_stat(left: os.stat_result, right: os.stat_result) -> bool:
    return stat_record(left) == stat_record(right)


def stable_bytes(path: Path, maximum: int = 64 << 20) -> bytes:
    fd = os.open(path, os.O_RDONLY | getattr(os, "O_CLOEXEC", 0) | getattr(os, "O_NOFOLLOW", 0))
    try:
        before = os.fstat(fd)
        need(stat.S_ISREG(before.st_mode) and before.st_nlink == 1, "single-link regular file:" + str(path))
        need(0 < before.st_size <= maximum, "bounded nonempty file:" + str(path))
        pieces: list[bytes] = []
        while block := os.read(fd, 1 << 20):
            pieces.append(block)
        after = os.fstat(fd)
        current = os.stat(path, follow_symlinks=False)
        need(same_stat(before, after) and same_stat(before, current), "stable file:" + str(path))
        return b"".join(pieces)
    finally:
        os.close(fd)


def bytes_sha(path: Path, maximum: int = 64 << 20) -> str:
    return hashlib.sha256(stable_bytes(path, maximum)).hexdigest()


def load_closed(path: Path, file_pin: str, object_pin: str, label: str,
                field: str = "object_sha256") -> dict[str, Any]:
    raw = stable_bytes(path)
    need(hashlib.sha256(raw).hexdigest() == file_pin, label + ":file pin")
    value = parse_json(raw, label, canonical_line=True)
    need(type(value) is dict and value.get(field) == object_pin, label + ":object claim")
    body = copy.deepcopy(value)
    body.pop(field)
    need(digest(body) == object_pin, label + ":object closure")
    return value


def close_dynamic_json(path: Path, file_pin: str, label: str) -> dict[str, Any]:
    raw = stable_bytes(path)
    need(hashlib.sha256(raw).hexdigest() == file_pin, label + ":file pin")
    # These two frozen compact C50a receipts are pretty-printed JSON.  Their
    # exact file bytes are pinned above; semantic closure is canonical below.
    value = parse_json(raw, label, canonical_line=False)
    need(type(value) is dict and type(value.get("object_sha256")) is str, label + ":object claim")
    body = copy.deepcopy(value)
    claim = body.pop("object_sha256")
    need(digest(body) == claim, label + ":object closure")
    return value


def close_row(row: dict[str, Any], label: str) -> None:
    need(type(row) is dict and type(row.get("row_sha256")) is str, label + ":row claim")
    claim = row["row_sha256"]
    need(HEX64.fullmatch(claim) is not None, label + ":row hash shape")
    body = copy.deepcopy(row)
    body.pop("row_sha256")
    need(digest(body) == claim, label + ":row closure")


def scan_ledger(base: Path, descriptor: dict[str, Any], label: str,
                retain: Callable[[dict[str, Any]], bool] | None = None) -> list[dict[str, Any]]:
    required = {"filename", "order", "row_count", "row_hash_line_sequence_sha256", "sha256", "size"}
    need(type(descriptor) is dict and set(descriptor) == required, label + ":descriptor schema")
    path = base / descriptor["filename"]
    fd = os.open(path, os.O_RDONLY | getattr(os, "O_CLOEXEC", 0) | getattr(os, "O_NOFOLLOW", 0))
    try:
        before = os.fstat(fd)
        need(stat.S_ISREG(before.st_mode) and before.st_nlink == 1, label + ":single-link regular ledger")
        need(before.st_size == descriptor["size"] and 0 < before.st_size <= 768 << 20, label + ":ledger size")
        raw_hash = hashlib.sha256()
        while block := os.read(fd, 1 << 20):
            raw_hash.update(block)
        need(raw_hash.hexdigest() == descriptor["sha256"], label + ":ledger file hash")
        os.lseek(fd, 0, os.SEEK_SET)
        decoder = zlib.decompressobj(16 + zlib.MAX_WBITS)
        pending = b""
        sequence = hashlib.sha256()
        count = 0
        answer: list[dict[str, Any]] = []

        def consume(expanded: bytes, final: bool = False) -> None:
            nonlocal pending, count
            pending += expanded
            parts = pending.split(b"\n")
            pending = parts.pop()
            for body in parts:
                line = body + b"\n"
                row = parse_json(line, f"{label}:row:{count}", canonical_line=True)
                need(type(row) is dict, label + ":row object")
                close_row(row, f"{label}:row:{count}")
                sequence.update((row["row_sha256"] + "\n").encode("ascii"))
                count += 1
                if retain is None or retain(row):
                    answer.append(row)
            if final:
                need(pending == b"", label + ":newline-terminated rows")

        while block := os.read(fd, 1 << 20):
            consume(decoder.decompress(block))
            need(not decoder.unused_data and not decoder.unconsumed_tail, label + ":single complete gzip member")
        consume(decoder.flush(), final=True)
        need(decoder.eof and not decoder.unused_data and not decoder.unconsumed_tail, label + ":complete gzip member")
        need(count == descriptor["row_count"], label + ":row count")
        need(sequence.hexdigest() == descriptor["row_hash_line_sequence_sha256"], label + ":row sequence")
        after = os.fstat(fd)
        current = os.stat(path, follow_symlinks=False)
        need(same_stat(before, after) and same_stat(before, current), label + ":stable ledger")
        return answer
    finally:
        os.close(fd)


def semantic(row: dict[str, Any]) -> dict[str, Any]:
    result = copy.deepcopy(row)
    result.pop("row_sha256")
    return result


def sequence_sha(values: Iterable[str]) -> str:
    state = hashlib.sha256()
    for value in values:
        state.update((value + "\n").encode("ascii"))
    return state.hexdigest()


def unique_map(rows: Iterable[dict[str, Any]], key: str, label: str) -> dict[Any, dict[str, Any]]:
    result: dict[Any, dict[str, Any]] = {}
    for row in rows:
        value = row[key]
        need(value not in result, label + ":unique:" + str(value))
        result[value] = row
    return result


class ExactAudit:
    def __init__(self) -> None:
        self.comparisons: Counter[str] = Counter()
        self.tokens: Counter[str] = Counter()

    def token(self, value: Any) -> str:
        token = value.get("value") if isinstance(value, dict) else value
        need(type(token) is str, "exact scalar token")
        if token in ALGEBRAIC:
            if isinstance(value, dict):
                need(value.get("kind") == "ALGEBRAIC" and value.get("minimal_polynomial") == "2*x^2-1",
                     "algebraic metadata")
                expected = ["707/1000", "708/1000"] if token.startswith("+") else ["-708/1000", "-707/1000"]
                need(value.get("isolating_interval") == expected, "algebraic isolating interval")
            self.tokens[token] += 1
            return token
        fraction = Fraction(token)
        need(str(fraction) == token, "canonical rational:" + token)
        if isinstance(value, dict):
            need(value.get("kind") == "RATIONAL", "rational metadata")
        self.tokens["RATIONAL"] += 1
        return token

    def compare(self, left: str, right: str) -> int:
        if left == right:
            self.comparisons["equal"] += 1
            return 0
        left_alg, right_alg = left in ALGEBRAIC, right in ALGEBRAIC
        if not left_alg and not right_alg:
            self.comparisons["rational_vs_rational"] += 1
            return -1 if Fraction(left) < Fraction(right) else 1
        if left_alg and right_alg:
            self.comparisons["negative_vs_positive_algebraic"] += 1
            return -1 if left.startswith("-") else 1
        if left_alg:
            self.comparisons["algebraic_vs_rational"] += 1
            return -self.compare(right, left)
        rational = Fraction(left)
        self.comparisons["rational_vs_positive_algebraic" if right.startswith("+") else "rational_vs_negative_algebraic"] += 1
        if right == "+1/sqrt(2)":
            if rational <= 0:
                return -1
            square = rational * rational
            need(square != Fraction(1, 2), "rational cannot equal positive algebraic boundary")
            return -1 if square < Fraction(1, 2) else 1
        need(right == "-1/sqrt(2)", "known algebraic boundary")
        if rational >= 0:
            return 1
        square = rational * rational
        need(square != Fraction(1, 2), "rational cannot equal negative algebraic boundary")
        return -1 if square > Fraction(1, 2) else 1

    def minimum(self, left: str, right: str) -> str:
        return left if self.compare(left, right) <= 0 else right

    def maximum(self, left: str, right: str) -> str:
        return left if self.compare(left, right) >= 0 else right


def compact_interval(row: dict[str, Any], axis: str, exact: ExactAudit) -> tuple[str, str]:
    values = row["physical_p_interval" if axis == "p" else "physical_t_interval"]
    need(type(values) is list and len(values) == 2, "compact interval shape")
    low, high = exact.token(values[0]), exact.token(values[1])
    need(exact.compare(low, high) < 0, "positive compact interval:" + row["cell_id"])
    return low, high


def check_step_binding(step: dict[str, Any], edge: dict[str, Any]) -> None:
    need({step["from_cell_id"], step["to_cell_id"]} == {edge["left_cell_id"], edge["right_cell_id"]}, "C56/C55B endpoints")
    expected = {
        "C55B_edge_row_sha256": edge["row_sha256"], "upstream_row_sha256": edge["upstream_row_sha256"],
        "face_or_corner_id": edge["face_or_corner_id"], "glue_kind": edge["glue_kind"],
        "gluing_proof_kind": edge["gluing_proof_kind"], "dimension": edge["dimension"],
        "exact_geometry": edge["exact_geometry"],
    }
    need(all(step[key] == value for key, value in expected.items()), "C56/C55B step projection")


def exact_face(step: dict[str, Any], left: dict[str, Any], right: dict[str, Any], exact: ExactAudit) -> dict[str, Any]:
    need({step["from_cell_id"], step["to_cell_id"]} == {left["cell_id"], right["cell_id"]}, "face endpoints")
    geometry = step["exact_geometry"]
    if step["glue_kind"] == "INTRA_CHART_FACE":
        need(left["compact_chart"] == right["compact_chart"] == geometry["compact_chart"], "intra-chart identity")
        axis = geometry["axis"]
        need(axis in {"t", "p"}, "face axis")
        other = "p" if axis == "t" else "t"
        a0, a1 = compact_interval(left, axis, exact)
        b0, b1 = compact_interval(right, axis, exact)
        shared = a1 if a1 == b0 else b1 if b1 == a0 else None
        need(shared is not None, "shared fixed coordinate")
        c0, c1 = compact_interval(left, other, exact)
        d0, d1 = compact_interval(right, other, exact)
        overlap = (exact.maximum(c0, d0), exact.minimum(c1, d1))
        need(exact.compare(overlap[0], overlap[1]) < 0, "positive exact face overlap")
        span = tuple(exact.token(item) for item in geometry["span"])
        need(exact.token(geometry["coordinate"]) == shared and span == overlap, "exact intra-face geometry")
        return {"kind": "EXACT_INTRA_CHART_COMMON_FACE", "axis": axis, "fixed_coordinate": shared,
                "span": list(overlap), "source_geometry_sha256": digest(geometry)}
    need(step["glue_kind"] == "SOURCE_CHART_TRANSITION", "supported corridor glue")
    need(geometry["exact_state_gluing_inherited_from_round162"] is True, "source-seam state glue")
    need({left["compact_chart"], right["compact_chart"]} == {geometry["left_chart"], geometry["right_chart"]}, "source-seam charts")
    a0, a1 = compact_interval(left, "p", exact)
    b0, b1 = compact_interval(right, "p", exact)
    overlap = (exact.maximum(a0, b0), exact.minimum(a1, b1))
    span = tuple(exact.token(item) for item in geometry["physical_p_span"])
    need(exact.compare(overlap[0], overlap[1]) < 0 and span == overlap, "exact source-seam span")
    return {"kind": "EXACT_SOURCE_CHART_SEAM_COMMON_FACE", "seam_id": geometry["seam_id"],
            "physical_p_span": list(overlap), "source_geometry_sha256": digest(geometry)}


def qstr(value: Fraction) -> str:
    return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"


def margin_intervals(margin: dict[str, Any]) -> dict[str, Any]:
    answer: dict[str, Any] = {}
    for collar, vector in sorted(margin["collar_margin_vectors"].items()):
        answer[collar] = {}
        for field, depth in sorted(vector.items()):
            answer[collar][field] = (
                {"applicable": False, "strict_open_lower_bound": None, "upper_bound": None}
                if depth is None else
                {"applicable": True, "dyadic_depth": depth,
                 "strict_open_lower_bound": qstr(Fraction(1, 2 ** depth)), "upper_bound": None}
            )
    return answer


def immutable_snapshot() -> dict[str, Any]:
    answer: dict[str, Any] = {}
    for label, path, pin in (
        ("runtime_C53_authority_head", C53_HEAD, PINS["C53_head_file"]),
        ("canonical_status", CANONICAL, PINS["canonical_file"]),
    ):
        raw = stable_bytes(path)
        state = os.stat(path, follow_symlinks=False)
        value = {"path": str(path.relative_to(ROOT)), "sha256": hashlib.sha256(raw).hexdigest(), "stat": stat_record(state)}
        need(value["sha256"] == pin, label + ":snapshot pin")
        answer[label] = value
    return answer


def independence_audit() -> dict[str, Any]:
    producer_raw = stable_bytes(PRODUCER)
    need(hashlib.sha256(producer_raw).hexdigest() == PINS["producer_file"], "producer inert-byte pin")
    source = stable_bytes(SELF)
    tree = ast.parse(source.decode("utf-8", "strict"), filename=SELF.name)
    imports: list[str] = []
    forbidden_calls: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imports.extend(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            imports.append(node.module or "")
        elif isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id in {"exec", "eval", "compile", "__import__"}:
            forbidden_calls.append(node.func.id)
        elif isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
            if isinstance(node.func.value, ast.Name) and (node.func.value.id, node.func.attr) in {
                ("os", "system"), ("os", "popen"), ("runpy", "run_path"), ("runpy", "run_module"),
                ("subprocess", "run"), ("subprocess", "Popen"), ("subprocess", "call"),
            }:
                forbidden_calls.append(node.func.value.id + "." + node.func.attr)
    forbidden_imports = {"runpy", "subprocess", "importlib", "multiprocessing"}
    need(not any(item.split(".")[0] in forbidden_imports for item in imports), "no producer execution interface imports")
    need(not any(PREFIX in item for item in imports) and not forbidden_calls, "no producer import/dynamic execution")
    need(not any(PREFIX in name for name in sys.modules), "producer absent from sys.modules")
    return {
        "producer_file_sha256": PINS["producer_file"], "producer_treatment": "INERT_HASH_ONLY_BYTES",
        "producer_imported": False, "producer_executed": False, "producer_source_decoded_or_AST_parsed": False,
        "verifier_static_forbidden_imports": [], "verifier_static_forbidden_execution_calls": [],
        "verifier_file_sha256": hashlib.sha256(source).hexdigest(),
    }


def validate_c50a(result: dict[str, Any]) -> list[dict[str, str]]:
    raw = stable_bytes(C50A_MANIFEST)
    need(hashlib.sha256(raw).hexdigest() == PINS["C50A_manifest_file"], "C50a manifest pin")
    text = raw.decode("ascii", "strict")
    need(text.endswith("\n"), "C50a manifest newline")
    members: list[dict[str, str]] = []
    seen: set[str] = set()
    for line in text.splitlines():
        parts = line.split("  ", 1)
        need(len(parts) == 2 and HEX64.fullmatch(parts[0]) is not None, "C50a manifest syntax")
        expected, name = parts
        need(name.startswith("deliverables/cm2_round306c50a_") and name not in seen, "C50a member scope/uniqueness")
        seen.add(name)
        path = ROOT / name
        need(bytes_sha(path, 256 << 20) == expected, "C50a member hash:" + name)
        members.append({"filename": name, "sha256": expected})
    need(len(members) == 8, "C50a member count")
    need(not any("c57l1" in item["filename"].lower() or "edge_obligation" in item["filename"].lower() for item in members),
         "C50a manifest contains no C57L1 edge request/audit")
    need(result["authority_binding"]["C50a_frozen_manifest_members"] == members, "candidate/C50a manifest member binding")
    member_pins = {item["filename"]: item["sha256"] for item in members}
    c50_result = close_dynamic_json(C50A_RESULT, member_pins[str(C50A_RESULT.relative_to(ROOT))], "C50a compact result")
    c50_verify = close_dynamic_json(C50A_VERIFY, member_pins[str(C50A_VERIFY.relative_to(ROOT))], "C50a compact verification")
    need(c50_result["formal_credit"] == c50_result["strict_nonpromotion"]["formal_credit"] ==
         c50_result["strict_nonpromotion"]["D02_gate_credit"] == 0, "C50a result zero credit")
    need(c50_verify["formal_credit"] == c50_verify["strict_nonpromotion"]["formal_credit"] ==
         c50_verify["strict_nonpromotion"]["D02_gate_credit"] == 0, "C50a verification zero credit")
    need(c50_verify["independent_replay"]["C50a_producer_imported_or_executed"] is False, "C50a independent replay")
    return members


def coherent_attacks(baseline_semantic: dict[str, Any]) -> dict[str, Any]:
    baseline = copy.deepcopy(baseline_semantic)
    baseline["object_sha256"] = digest(baseline)

    def validate(value: dict[str, Any]) -> None:
        body = copy.deepcopy(value)
        claim = body.pop("object_sha256", None)
        need(type(claim) is str and digest(body) == claim, "attack object closure")
        need(body == baseline_semantic, "attack exact invariant projection")

    validate(baseline)
    mutations: list[tuple[str, Callable[[dict[str, Any]], None]]] = [
        ("chain_count_33318", lambda x: x["counts"].__setitem__("chains", 33318)),
        ("local_count_1043", lambda x: x["counts"].__setitem__("local_rows", 1043)),
        ("edge_count_1041", lambda x: x["counts"].__setitem__("edge_rows", 1041)),
        ("cell_count_1043", lambda x: x["counts"].__setitem__("cell_rows", 1043)),
        ("handoff_count_one", lambda x: x["counts"].__setitem__("handoff_rows", 1)),
        ("intra_face_count_1025", lambda x: x["counts"].__setitem__("intra_chart_faces", 1025)),
        ("source_seam_count_15", lambda x: x["counts"].__setitem__("source_seams", 15)),
        ("local_beyond_count_351", lambda x: x["counts"].__setitem__("local_beyond_collision1", 351)),
        ("all_nodes_count_90", lambda x: x["counts"].__setitem__("all_nodes_beyond_collision1", 90)),
        ("edge_pass_one", lambda x: x["counts"].__setitem__("edge_transport_pass", 1)),
        ("formal_credit_one", lambda x: x["credits"].__setitem__("formal_credit", 1)),
        ("D02_credit_one", lambda x: x["credits"].__setitem__("D02_gate_credit", 1)),
        ("handoff_credit_one", lambda x: x["credits"].__setitem__("collision2_ready_handoff_credit", 1)),
        ("whole_cell_credit_one", lambda x: x["credits"].__setitem__("whole_cell_CONNECTED_TO_KNOWN_credit", 1)),
        ("geometry_unmaterialized", lambda x: x["proofs"].__setitem__("all_exact_faces_materialized", False)),
        ("lineage_incomplete", lambda x: x["proofs"].__setitem__("all_lineages_exact", False)),
        ("C36_scope_forged_global", lambda x: x["proofs"].__setitem__("C36_scope", "GLOBAL")),
        ("producer_execution_forged", lambda x: x["independence"].__setitem__("producer_executed", True)),
        ("canonical_retarget", lambda x: x["pins"].__setitem__("canonical_file", "0" * 64)),
        ("C53_retarget", lambda x: x["pins"].__setitem__("C53_head_file", "0" * 64)),
    ]
    outcomes: dict[str, str] = {}
    for name, mutation in mutations:
        attacked = copy.deepcopy(baseline_semantic)
        mutation(attacked)
        attacked["object_sha256"] = digest(attacked)
        try:
            validate(attacked)
        except Rejected:
            outcomes[name] = "FAIL_CLOSED"
        else:
            raise Rejected("coherent attack accepted:" + name)
    need(len(outcomes) == len(mutations) == 20, "20 coherent attacks")
    return {"status": "PASS_20_OF_20_COHERENT_RECLOSED_ATTACKS_FAIL_CLOSED", "attack_count": 20,
            "attacks": outcomes, "mutations_reclosed_before_validation": True}


def verify() -> dict[str, Any]:
    snapshot_before = immutable_snapshot()
    independence = independence_audit()

    result = load_closed(RESULT, PINS["result_file"], PINS["result_object"], "C57L1 result")
    need(result["schema"] == SCHEMA + ".result", "candidate result schema")
    need(result["ledgers"] == CANDIDATE_DESCRIPTORS, "candidate exact ledger descriptors")

    c56 = load_closed(C56_RESULT, PINS["C56_result_file"], PINS["C56_result_object"], "C56 result")
    c56_verify = load_closed(C56_VERIFY, PINS["C56_verify_file"], PINS["C56_verify_object"], "C56 verification")
    c55b = load_closed(C55B_RESULT, PINS["C55B_result_file"], PINS["C55B_result_object"], "C55B result")
    c35 = load_closed(C35 / "result.json", PINS["C35_result_file"], PINS["C35_object"], "C35 result")
    c36 = load_closed(C36 / "result.json", PINS["C36_result_file"], PINS["C36_object"], "C36 result")
    c38 = load_closed(C38 / "result.json", PINS["C38_result_file"], PINS["C38_object"], "C38 result")
    c39 = load_closed(C39 / "result.json", PINS["C39_result_file"], PINS["C39_object"], "C39 result")
    c40 = load_closed(C40 / "result.json", PINS["C40_result_file"], PINS["C40_object"], "C40 result")
    c41 = load_closed(C41 / "result.json", PINS["C41_result_file"], PINS["C41_object"], "C41 result")
    c53 = load_closed(C53_HEAD, PINS["C53_head_file"], PINS["C53_head_object"], "C53 authority head",
                      field="authority_seal_object_sha256")
    need(c53["post_seal_effective_checkpoint_object_sha256"] == PINS["C53_checkpoint"], "C53 effective checkpoint")
    need(c56_verify["verified"]["post_C53_unique_logical_tasks"] == 33319 and
         c56_verify["verified"]["topological_corridor_cells"] == 1044 and
         c56_verify["verified"]["D02_gate_credit"] == 0, "C56 independent verification binding")

    expected_authority = {
        "C56L_result_file_sha256": PINS["C56_result_file"], "C56L_result_object_sha256": PINS["C56_result_object"],
        "C56L_independent_verification_file_sha256": PINS["C56_verify_file"],
        "C56L_independent_verification_object_sha256": PINS["C56_verify_object"],
        "C35_object_sha256": PINS["C35_object"], "C36_object_sha256": PINS["C36_object"],
        "C38_object_sha256": PINS["C38_object"], "C39_object_sha256": PINS["C39_object"],
        "C40_object_sha256": PINS["C40_object"], "C41_object_sha256": PINS["C41_object"],
        "C50a_manifest_file_sha256": PINS["C50A_manifest_file"],
        "C50a_producer_file_sha256": "43147808a94e14df20d902db6d7d383f8d230c6685401684bfb9ea697f7e9ed7",
        "C50a_independent_verifier_file_sha256": "2ae76868e0320563cafbc4a472f3ad1bf292817491d97da1fe68ca9d8e8bd3b4",
        "C53_head_file_sha256": PINS["C53_head_file"], "canonical_file_sha256": PINS["canonical_file"],
    }
    for key, value in expected_authority.items():
        need(result["authority_binding"].get(key) == value, "candidate authority binding:" + key)
    c50_members = validate_c50a(result)

    # Close every candidate row and every candidate descriptor before using it.
    chains = scan_ledger(OUT, CANDIDATE_DESCRIPTORS["upstream_task_chains"], "candidate chains")
    locals_ = scan_ledger(OUT, CANDIDATE_DESCRIPTORS["local_collision1_cell_status"], "candidate local")
    edges = scan_ledger(OUT, CANDIDATE_DESCRIPTORS["edge_obligations"], "candidate edges")
    cells = scan_ledger(OUT, CANDIDATE_DESCRIPTORS["corridor_cell_transport"], "candidate cells")
    handoffs = scan_ledger(OUT, CANDIDATE_DESCRIPTORS["collision2_ready_handoff"], "candidate handoff")
    need((len(chains), len(locals_), len(edges), len(cells), len(handoffs)) == (33319, 1044, 1042, 1044, 0),
         "candidate ledger census")

    # Independently close the relevant complete upstream ledgers.
    c56_cells_all = scan_ledger(OUT, c56["ledgers"]["corridor_and_separator_cells"], "C56 cells")
    c56_tasks = scan_ledger(OUT, c56["ledgers"]["post_C53_pending_logical_tasks"], "C56 tasks")
    c56_cells = [row for row in c56_cells_all if row["witness_kind"] == "EXPLICIT_TOPOLOGICAL_CORRIDOR_TO_STRICT_OPEN_ANCHOR"]
    need(len(c56_cells_all) == 1124 and len(c56_cells) == 1044 and len(c56_tasks) == 33319, "C56 scope")
    need([(row["component_index"], row["cell_id"]) for row in c56_cells] ==
         sorted((row["component_index"], row["cell_id"]) for row in c56_cells), "C56 corridor order")

    crosswalk_rows = scan_ledger(OUT, c55b["ledgers"]["cell_component_crosswalk"], "C55B crosswalk")
    c55b_edges = scan_ledger(OUT, c55b["ledgers"]["component_edges_and_glue"], "C55B edges")
    crosswalk = unique_map(crosswalk_rows, "cell_id", "C55B crosswalk")
    c55b_edge_map = unique_map(c55b_edges, "row_sha256", "C55B edges")
    need(len(crosswalk) == 1724 and len(c55b_edge_map) == 5358, "C55B complete ledgers")

    occurrences = scan_ledger(C35, c35["ledgers"]["path_occurrences"], "C35 occurrences")
    margins = scan_ledger(C36, c36["ledgers"]["occurrence_margin_bindings"], "C36 margins")
    need(len(occurrences) == len(margins) == 1648, "C35/C36 occurrence census")
    for index, (occurrence, margin) in enumerate(zip(occurrences, margins, strict=True), start=1):
        need(occurrence["collision_index"] == margin["collision_index"] == index, "C35/C36 ordered alignment")
        for field in ("geometry_template_id", "official_word_variant_id", "incoming_absolute_owner_id",
                      "selected_absolute_owner_id", "incoming_chart", "outgoing_chart", "destination_core_id"):
            need(occurrence[field] == margin[field], "C35/C36 projection:" + field)
    occurrence1, margin1 = occurrences[0], margins[0]
    need(occurrence1["row_sha256"] == "815af4b7fd77b884f70178c9a706de9be94be219b66488c9da48fe7b470b8250", "C35 occurrence1")
    need(margin1["row_sha256"] == "b9238fdb52bf7e3979b7bfdc1beabe5e1d0f2adf10e949f7eeaf13f6a4a7a169", "C36 occurrence1")
    need(c36["map_stage_census"]["scope"] == SEED_SCOPE and margin1["selected_absolute_owner_id"] == "W[1,0]", "C36 scope/owner")
    seed_intervals = margin_intervals(margin1)

    # Select all referenced upstream rows while still closing every row of each upstream ledger.
    wanted38 = {row["C38_row_sha256"] for row in chains}
    wanted39 = {row["C39_row_sha256"] for row in chains}
    wanted40 = {row["C40_row_sha256"] for row in chains}
    wanted41 = {row["C41_row_sha256"] for row in chains}
    c38_rows = scan_ledger(C38, c38["ledgers"]["collision1_2_child_pairs"], "C38 children",
                           retain=lambda row: row["row_sha256"] in wanted38)
    c39_rows = scan_ledger(C39, c39["ledgers"]["routed_child_pairs"], "C39 routed",
                           retain=lambda row: row["row_sha256"] in wanted39)
    c40_rows = scan_ledger(C40, c40["ledgers"]["routed_leaf_cells"], "C40 leaves",
                           retain=lambda row: row["row_sha256"] in wanted40)
    c41_rows = scan_ledger(C41, c41["ledgers"]["routed_ambient_cells"], "C41 ambient",
                           retain=lambda row: row["row_sha256"] in wanted41)
    map38 = unique_map(c38_rows, "row_sha256", "selected C38")
    map39 = unique_map(c39_rows, "row_sha256", "selected C39")
    map40 = unique_map(c40_rows, "row_sha256", "selected C40")
    map41 = unique_map(c41_rows, "row_sha256", "selected C41")
    need(set(map38) == wanted38 and set(map39) == wanted39 and set(map40) == wanted40 and set(map41) == wanted41,
         "selected upstream completeness")

    chain_by_blocker: dict[str, list[dict[str, Any]]] = defaultdict(list)
    chain_census: Counter[str] = Counter()
    for ordinal, (task, actual) in enumerate(zip(c56_tasks, chains, strict=True)):
        c41_row = map41[actual["C41_row_sha256"]]
        c40_row = map40[actual["C40_row_sha256"]]
        c39_row = map39[actual["C39_row_sha256"]]
        c38_row = map38[actual["C38_row_sha256"]]
        need(task["row_sha256"] == actual["C56L_task_row_sha256"] and
             task["C41_routed_ambient_row_sha256"] == c41_row["row_sha256"], "C56/C57/C41 task identity")
        for field in ("pair_index", "path", "source_path", "residual_classification", "split_axis_history",
                      "route_method", "round144_terminal_class", "parent_volume_fraction"):
            task_field = "path" if field == "path" else field
            need(task[task_field] == c41_row[field], "C56/C41 task projection:" + field)
        need(c40_row["row_sha256"] == c41_row["c40_source_row_sha256"], "C40/C41 foreign key")
        need(c39_row["row_sha256"] == c40_row["c39_source_row_sha256"] and
             c38_row["row_sha256"] == c40_row["c38_source_row_sha256"] and
             c38_row["row_sha256"] == c39_row["c38_child_row_sha256"], "C38/C39/C40 foreign keys")
        need(c39_row["path"] == c38_row["path"] and c40_row["source_path"] == c39_row["path"] and
             c41_row["source_path"] == c40_row["path"], "C38-C41 path lineage")
        need(task["pair_index"] == c41_row["pair_index"] == c40_row["pair_index"] ==
             c39_row["pair_index"] == c38_row["pair_index"], "C38-C41 pair lineage")
        past = c41_row["residual_classification"].startswith(COLLISION2_PREFIX)
        expected = {
            "schema": SCHEMA + ".upstream-task-chain-row", "pair_index": task["pair_index"],
            "C55A_blocker_row_sha256": task["C55A_blocker_row_sha256"], "C56L_task_row_sha256": task["row_sha256"],
            "C41_row_sha256": c41_row["row_sha256"], "C41_residual_classification": c41_row["residual_classification"],
            "C41_path": c41_row["path"], "C41_split_axis_history": c41_row["split_axis_history"],
            "C40_row_sha256": c40_row["row_sha256"], "C40_classification": c40_row["classification"], "C40_path": c40_row["path"],
            "C39_row_sha256": c39_row["row_sha256"], "C39_classification": c39_row["classification"],
            "C39_route_method": c39_row["route_method"], "C39_path": c39_row["path"],
            "C38_row_sha256": c38_row["row_sha256"], "C38_classification": c38_row["classification"],
            "C38_first_decision_collision": c38_row["first_decision_collision"], "C38_path": c38_row["path"],
            "within_cell_upstream_lineage_exact": True, "current_pending_task_beyond_collision1": past,
            "cross_C32_face_occurrence1_history_compatibility_proved": False, "formal_credit": 0, "D02_gate_credit": 0,
        }
        need(semantic(actual) == expected, "exact candidate chain reconstruction:" + str(ordinal))
        chain_by_blocker[task["C55A_blocker_row_sha256"]].append(actual)
        chain_census[c41_row["residual_classification"]] += 1

    local_by_cell: dict[str, dict[str, Any]] = {}
    local_class: Counter[tuple[str, bool]] = Counter()
    need([(row["component_index"], row["cell_id"]) for row in locals_] ==
         sorted((row["component_index"], row["cell_id"]) for row in locals_), "candidate local order")
    for index, (source_cell, actual) in enumerate(zip(c56_cells, locals_, strict=True)):
        related = chain_by_blocker[source_cell["C55A_blocker_row_sha256"]]
        need(len(related) == source_cell["post_C53_pending_logical_task_count_for_pair"], "local task count")
        residual = Counter(row["C41_residual_classification"] for row in related)
        past = all(row["current_pending_task_beyond_collision1"] for row in related)
        expected = {
            "schema": SCHEMA + ".local-collision1-cell-status-row", "component_index": source_cell["component_index"],
            "cell_id": source_cell["cell_id"], "pair_index": source_cell["pair_index"],
            "C56L_cell_row_sha256": source_cell["row_sha256"], "C55A_blocker_row_sha256": source_cell["C55A_blocker_row_sha256"],
            "primary_residual_classification": source_cell["primary_residual_classification"],
            "current_pending_task_count": len(related),
            "C57L1_upstream_chain_row_hash_sequence_sha256": sequence_sha(row["row_sha256"] for row in related),
            "C41_residual_classification_census": dict(sorted(residual.items())),
            "all_current_pending_tasks_beyond_collision1": past, "within_cell_C38_C41_lineage_complete": True,
            "occurrence1_common_face_history_crosswalk_present": False,
            "local_status": "LOCAL_PENDING_FRONTIER_ALL_BEYOND_COLLISION1" if past else "LOCAL_PENDING_FRONTIER_RETAINS_COLLISION1_OR_LOWER_STRATA",
            "collision2_ready_edgewise_handoff_credit": 0, "D02_gate_credit": 0,
        }
        need(semantic(actual) == expected, "exact local reconstruction:" + str(index))
        need(source_cell["C55B_crosswalk_row_sha256"] == crosswalk[source_cell["cell_id"]]["row_sha256"], "C56/C55B cell crosswalk")
        local_by_cell[actual["cell_id"]] = actual
        local_class[(source_cell["primary_residual_classification"], past)] += 1
    need(len(local_by_cell) == 1044 and sum(row["all_current_pending_tasks_beyond_collision1"] for row in locals_) == 350,
         "local exact census")

    exact = ExactAudit()
    algebraic_tokens: Counter[str] = Counter()
    for row in crosswalk_rows:
        compact_interval(row, "p", exact)
        compact_interval(row, "t", exact)
        for value in row["physical_t_interval"] + row["physical_p_interval"]:
            token = value.get("value") if isinstance(value, dict) else value
            if token in ALGEBRAIC:
                algebraic_tokens[token] += 1
    need(algebraic_tokens == Counter({"+1/sqrt(2)": 48, "-1/sqrt(2)": 10}), "C55B algebraic boundary census")
    law_cases = {
        "-3/4_lt_negative_boundary": exact.compare("-3/4", "-1/sqrt(2)") < 0,
        "-2/3_gt_negative_boundary": exact.compare("-2/3", "-1/sqrt(2)") > 0,
        "2/3_lt_positive_boundary": exact.compare("2/3", "+1/sqrt(2)") < 0,
        "3/4_gt_positive_boundary": exact.compare("3/4", "+1/sqrt(2)") > 0,
        "negative_lt_positive_boundary": exact.compare("-1/sqrt(2)", "+1/sqrt(2)") < 0,
        "positive_gt_negative_boundary": exact.compare("+1/sqrt(2)", "-1/sqrt(2)") > 0,
    }
    need(all(law_cases.values()), "exact algebraic comparison laws")

    # Validate all 43,884 rooted corridor steps and reconstruct each of the 1,042 candidate edge rows.
    corridor_step_count = 0
    corridor_step_kind: Counter[str] = Counter()
    for source_cell in c56_cells:
        for step in source_cell["corridor_steps"]:
            upstream_edge = c55b_edge_map[step["C55B_edge_row_sha256"]]
            check_step_binding(step, upstream_edge)
            exact_face(step, crosswalk[step["from_cell_id"]], crosswalk[step["to_cell_id"]], exact)
            corridor_step_count += 1
            corridor_step_kind[step["glue_kind"]] += 1
    need(corridor_step_count == 43884, "all rooted corridor-step geometry count")

    edge_by_source: dict[str, dict[str, Any]] = {}
    edge_kind: Counter[str] = Counter()
    endpoint_state: Counter[tuple[bool, bool, str]] = Counter()
    nonanchors = [row for row in c56_cells if row["corridor_step_count"] != 0]
    need(len(nonanchors) == len(edges) == 1042, "nonanchor/edge count")
    for index, (source_cell, actual) in enumerate(zip(nonanchors, edges, strict=True)):
        step = source_cell["corridor_steps"][0]
        need(step["from_cell_id"] == source_cell["cell_id"], "rooted first-step source")
        upstream_edge = c55b_edge_map[step["C55B_edge_row_sha256"]]
        check_step_binding(step, upstream_edge)
        source, target = crosswalk[step["from_cell_id"]], crosswalk[step["to_cell_id"]]
        face = exact_face(step, source, target, exact)
        source_local, target_local = local_by_cell[source["cell_id"]], local_by_cell[target["cell_id"]]
        both = source_local["all_current_pending_tasks_beyond_collision1"] and target_local["all_current_pending_tasks_beyond_collision1"]
        reasons = list(EDGE_REASONS)
        if step["glue_kind"] == "SOURCE_CHART_TRANSITION":
            reasons.append("SOURCE_SEAM_DYNAMIC_OCCURRENCE1_GLUE_NOT_MATERIALIZED")
        if not both:
            reasons.append("EDGE_ENDPOINT_LOCAL_COLLISION1_FRONTIER_NOT_BOTH_COMPLETE")
        expected = {
            "schema": SCHEMA + ".edge-transport-row", "component_index": source_cell["component_index"],
            "source_cell_id": source["cell_id"], "target_cell_id": target["cell_id"],
            "C56L_source_cell_row_sha256": source_cell["row_sha256"], "C55B_edge_row_sha256": step["C55B_edge_row_sha256"],
            "upstream_face_or_seam_row_sha256": step["upstream_row_sha256"], "face_or_corner_id": step["face_or_corner_id"],
            "glue_kind": step["glue_kind"], "exact_common_face_refinement": face,
            "exact_common_face_refinement_materialized": True, "source_local_status_row_sha256": source_local["row_sha256"],
            "target_local_status_row_sha256": target_local["row_sha256"], "both_endpoint_pending_frontiers_beyond_collision1": both,
            "C35_occurrence1_row_sha256": occurrence1["row_sha256"], "C36_occurrence1_margin_row_sha256": margin1["row_sha256"],
            "C36_seed_collar_scope": SEED_SCOPE, "C36_seed_collar_named_strict_margin_intervals": seed_intervals,
            "transported_edge_strict_margin_intervals": None, "C36_C32_face_Lipschitz_or_variation_bound_present": False,
            "C50a_owner_protocol": "CM2_FULL_UNIVERSE_FACE_CORNER_OWNER_V1", "C50a_frozen_edge_request_present": False,
            "C50a_frozen_edge_independent_audit_present": False, "endpoint_occurrence1_owner_compatibility_proved": False,
            "endpoint_occurrence1_owner_compatibility_disproved": False,
            "endpoint_split_history_common_face_compatibility_proved": False,
            "endpoint_split_history_common_face_compatibility_disproved": False, "edge_transport_pass": False,
            "reason_codes": reasons, "collision2_ready_handoff_credit": 0, "D02_gate_credit": 0,
        }
        need(semantic(actual) == expected, "exact edge reconstruction:" + str(index))
        need(actual["source_cell_id"] not in edge_by_source, "unique rooted source edge")
        edge_by_source[actual["source_cell_id"]] = actual
        edge_kind[step["glue_kind"]] += 1
        endpoint_state[(source_local["all_current_pending_tasks_beyond_collision1"],
                        target_local["all_current_pending_tasks_beyond_collision1"], step["glue_kind"])] += 1
    need(edge_kind == Counter({"INTRA_CHART_FACE": 1026, "SOURCE_CHART_TRANSITION": 16}), "candidate edge kind census")

    class_accounting: dict[str, Counter[str]] = defaultdict(Counter)
    all_nodes_count = 0
    need([(row["component_index"], row["cell_id"]) for row in cells] ==
         sorted((row["component_index"], row["cell_id"]) for row in cells), "candidate cell order")
    for index, (source_cell, actual) in enumerate(zip(c56_cells, cells, strict=True)):
        node_ids = [source_cell["cell_id"]] + [step["to_cell_id"] for step in source_cell["corridor_steps"]]
        all_nodes = all(local_by_cell[cell_id]["all_current_pending_tasks_beyond_collision1"] for cell_id in node_ids)
        all_nodes_count += int(all_nodes)
        path_edges = [edge_by_source[step["from_cell_id"]] for step in source_cell["corridor_steps"]]
        need(all(row["C55B_edge_row_sha256"] == step["C55B_edge_row_sha256"]
                 for row, step in zip(path_edges, source_cell["corridor_steps"], strict=True)), "corridor edge chain")
        local = local_by_cell[source_cell["cell_id"]]
        reasons: list[str] = []
        if not local["all_current_pending_tasks_beyond_collision1"]:
            reasons.append("LOCAL_CELL_RETAINS_COLLISION1_OR_LOWER_STRATA_PENDING_TASK")
        if not all_nodes:
            reasons.append("CORRIDOR_CONTAINS_NODE_WITH_INCOMPLETE_LOCAL_COLLISION1_FRONTIER")
        if source_cell["corridor_step_count"] == 0:
            reasons.append("ANCHOR_C36_SEED_COLLAR_NOT_PROMOTED_TO_WHOLE_C32_CELL")
        else:
            reasons.extend(["PATH_EDGE_C36_LIPSCHITZ_OR_VARIATION_TRANSPORT_MISSING",
                            "PATH_EDGE_C50A_OWNER_REQUESTS_AND_AUDITS_MISSING",
                            "PATH_EDGE_SPLIT_HISTORY_COMMON_FACE_COMPATIBILITY_MISSING"])
        expected = {
            "schema": SCHEMA + ".corridor-cell-transport-row", "component_index": source_cell["component_index"],
            "cell_id": source_cell["cell_id"], "pair_index": source_cell["pair_index"],
            "primary_residual_classification": source_cell["primary_residual_classification"],
            "C56L_cell_row_sha256": source_cell["row_sha256"], "local_collision1_status_row_sha256": local["row_sha256"],
            "corridor_step_count": source_cell["corridor_step_count"],
            "corridor_edge_transport_row_hash_sequence_sha256": sequence_sha(row["row_sha256"] for row in path_edges),
            "all_current_cell_pending_tasks_beyond_collision1": local["all_current_pending_tasks_beyond_collision1"],
            "all_corridor_nodes_local_pending_frontiers_beyond_collision1": all_nodes,
            "all_corridor_exact_common_faces_materialized": True, "all_corridor_edge_margin_transports_proved": False,
            "all_corridor_edge_owner_compatibilities_proved": False, "all_corridor_edge_history_compatibilities_proved": False,
            "collision1_edgewise_transport_pass": False, "failure_reason_codes": reasons, "collision2_ready_handoff": False,
            "collision2_ready_handoff_credit": 0, "formal_credit": 0, "D02_gate_credit": 0,
        }
        need(semantic(actual) == expected, "exact corridor-cell reconstruction:" + str(index))
        primary = source_cell["primary_residual_classification"]
        class_accounting[primary]["corridor_cells"] += 1
        class_accounting[primary]["local_beyond_C1_cells"] += int(local["all_current_pending_tasks_beyond_collision1"])
        class_accounting[primary]["all_nodes_beyond_C1_cells"] += int(all_nodes)
    need(all_nodes_count == 89, "all-nodes-beyond-collision1 count")

    scope = {
        "corridor_cell_count": 1044, "unique_rooted_edge_count": 1042, "intra_chart_edge_count": 1026,
        "source_seam_edge_count": 16, "post_C53_task_chain_count": 33319,
        "local_all_pending_beyond_collision1_cell_count": 350,
        "all_nodes_local_beyond_collision1_corridor_cell_count": 89, "edge_transport_pass_count": 0,
        "collision2_ready_handoff_cell_count": 0, "collision2_ready_handoff_row_count": 0,
    }
    need(result["scope"] == scope, "reconstructed result scope")
    need(result["C41_selected_task_residual_classification_census"] == dict(sorted(chain_census.items())), "C41 census")
    endpoint_census = {
        f"source_{str(source).lower()}__target_{str(target).lower()}__{kind}": count
        for (source, target, kind), count in sorted(endpoint_state.items(), key=lambda item: str(item[0]))
    }
    need(result["edge_endpoint_local_status_census"] == endpoint_census, "edge endpoint census")
    class_rows = []
    for primary in sorted(class_accounting):
        counts = class_accounting[primary]
        class_rows.append({
            "primary_residual_classification": primary, "corridor_cell_count": counts["corridor_cells"],
            "local_all_pending_beyond_collision1_cell_count": counts["local_beyond_C1_cells"],
            "all_nodes_local_beyond_collision1_corridor_cell_count": counts["all_nodes_beyond_C1_cells"],
            "edgewise_transport_pass_cell_count": 0, "collision2_ready_handoff_cell_count": 0,
            "remaining_cell_count": counts["corridor_cells"],
        })
    need(result["primary_residual_classification_accounting"] == class_rows, "classification accounting")
    expected_occurrence = {
        "C35_occurrence1_row_sha256": occurrence1["row_sha256"], "C36_occurrence1_margin_row_sha256": margin1["row_sha256"],
        "selected_absolute_owner_id": margin1["selected_absolute_owner_id"], "incoming_chart": margin1["incoming_chart"],
        "outgoing_chart": margin1["outgoing_chart"], "C36_atlas_scope": SEED_SCOPE,
        "seed_collar_named_strict_margin_intervals": seed_intervals, "whole_C32_face_variation_transport_proved": False,
    }
    need(result["occurrence1_binding"] == expected_occurrence, "occurrence1 result binding")
    need(result["formal_effect"] == {
        "collision2_ready_handoff_credit": 0, "whole_cell_CONNECTED_TO_KNOWN_credit": 0, "formal_credit": 0,
        "D02_gate_credit": 0, "installed_four_class_census_unchanged": True, "CM2": "NO-GO_FOR_CLAIM",
    }, "all formal credits locked zero")
    need(result["proof_boundary"] == {
        "exact_C32_common_face_or_source_seam_geometry_materialized": True,
        "within_cell_C38_C41_lineage_materialized": True, "C36_occurrence1_seed_collar_margin_bound": True,
        "C36_edge_Lipschitz_or_variation_transport": False,
        "C50a_frozen_C57L1_edge_owner_requests_and_audits": False,
        "cross_edge_C41_split_history_compatibility": False, "atlas_adjacency_promoted_to_dynamic_transport": False,
    }, "proof boundary")
    need(result["self_test"]["attack_count"] == 10 and result["self_test"]["status"].startswith("PASS_10_OF_10"), "producer receipt self-test binding")

    attack_baseline = {
        "schema": VERIFY_SCHEMA + ".attack-projection", "counts": {
            "chains": 33319, "local_rows": 1044, "edge_rows": 1042, "cell_rows": 1044, "handoff_rows": 0,
            "intra_chart_faces": 1026, "source_seams": 16, "local_beyond_collision1": 350,
            "all_nodes_beyond_collision1": 89, "edge_transport_pass": 0,
        },
        "credits": {"formal_credit": 0, "D02_gate_credit": 0, "collision2_ready_handoff_credit": 0,
                    "whole_cell_CONNECTED_TO_KNOWN_credit": 0},
        "proofs": {"all_exact_faces_materialized": True, "all_lineages_exact": True, "C36_scope": SEED_SCOPE},
        "independence": {"producer_executed": False},
        "pins": {"canonical_file": PINS["canonical_file"], "C53_head_file": PINS["C53_head_file"]},
    }
    attacks = coherent_attacks(attack_baseline)

    snapshot_after = immutable_snapshot()
    need(snapshot_after == snapshot_before, "runtime/canonical stable before/after")
    verification: dict[str, Any] = {
        "schema": VERIFY_SCHEMA, "status": "PASS_INDEPENDENT_C57L1_33319_CHAIN_1044_LOCAL_1042_EDGE_1044_CELL_EMPTY_HANDOFF_AUDIT__ZERO_CREDIT",
        "candidate": {"producer_file_sha256": PINS["producer_file"], "result_file_sha256": PINS["result_file"],
                      "result_object_sha256": PINS["result_object"], "ledgers": CANDIDATE_DESCRIPTORS},
        "upstream_objects": {key: value for key, value in PINS.items() if key.startswith("C") and key.endswith("object")},
        "upstream_ledger_coverage": {
            "C56_corridor_and_separator_rows_closed": 1124, "C56_post_C53_task_rows_closed": 33319,
            "C55B_crosswalk_rows_closed": 1724, "C55B_edge_rows_closed": 5358,
            "C35_occurrence_rows_closed": 1648, "C36_margin_rows_closed": 1648,
            "C38_rows_closed": c38["ledgers"]["collision1_2_child_pairs"]["row_count"],
            "C39_rows_closed": c39["ledgers"]["routed_child_pairs"]["row_count"],
            "C40_rows_closed": c40["ledgers"]["routed_leaf_cells"]["row_count"],
            "C41_rows_closed": c41["ledgers"]["routed_ambient_cells"]["row_count"],
            "selected_C38_rows_rebound": len(map38), "selected_C39_rows_rebound": len(map39),
            "selected_C40_rows_rebound": len(map40), "selected_C41_rows_rebound": len(map41),
            "C50a_manifest_members_hash_bound": len(c50_members),
        },
        "verified": {
            "upstream_task_chains": 33319, "local_collision1_cell_status_rows": 1044,
            "unique_rooted_edge_obligations": 1042, "corridor_cell_transport_rows": 1044,
            "collision2_ready_handoff_rows": 0, "intra_chart_faces": 1026, "source_chart_seams": 16,
            "all_rooted_corridor_step_geometries_checked": corridor_step_count,
            "local_all_pending_beyond_collision1_cells": 350, "all_nodes_beyond_collision1_corridors": 89,
            "edge_transport_passes": 0, "collision2_ready_handoffs": 0,
        },
        "exact_geometry": {
            "implementation": "fractions.Fraction plus sign-and-square comparison against x^2=1/2",
            "algebraic_boundary_token_census": dict(sorted(algebraic_tokens.items())),
            "comparison_operation_census": dict(sorted(exact.comparisons.items())),
            "six_direct_algebraic_order_law_cases": law_cases,
            "all_C56_corridor_steps_bound_to_C55B_exact_geometry": True,
            "candidate_edge_exact_face_payloads_reconstructed": 1042,
        },
        "zero_credit": {"formal_credit": 0, "D02_gate_credit": 0, "collision2_ready_handoff_credit": 0,
                        "whole_cell_CONNECTED_TO_KNOWN_credit": 0, "CM2": "NO-GO_FOR_CLAIM"},
        "classification_accounting": class_rows, "C41_selected_residual_census": dict(sorted(chain_census.items())),
        "attacks": attacks, "independence": independence,
        "runtime_identity": {"python_implementation": platform.python_implementation(),
                             "python_version": platform.python_version(), "executable": sys.executable},
        "runtime_and_canonical_snapshot_before": snapshot_before,
        "runtime_and_canonical_snapshot_after": snapshot_after,
        "runtime_and_canonical_unchanged": True, "files_written": [str(VERIFICATION.relative_to(ROOT))],
        "old_runtime_canonical_files_written": False,
    }
    verification["object_sha256"] = digest(verification)
    VERIFICATION.write_bytes(canonical(verification) + b"\n")
    return verification


def main() -> int:
    need(len(sys.argv) in {1, 2} and (len(sys.argv) == 1 or sys.argv[1] == "--verify"), "usage: verifier [--verify]")
    output = verify()
    print(json.dumps({"status": output["status"], "object_sha256": output["object_sha256"],
                      "verified": output["verified"], "attack_status": output["attacks"]["status"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (Rejected, OSError, ValueError, KeyError, TypeError, IndexError, zlib.error) as exc:
        print(f"FAIL_CLOSED:{type(exc).__name__}:{exc}", file=sys.stderr)
        raise SystemExit(2)
