#!/usr/bin/env python3
"""Cold independent verifier for the frozen C58s2 depth-six refinement.

The C58s2 producer is captured only as pinned inert bytes and AST.  It is
never imported or executed.  Exact routes are independently replayed through
the already frozen C41 independent-auditor kernel and its pinned lower
authorities.  Boundary atoms, owners, leaf rows, handoff summaries, parent
Kraft sums and every zero-credit lock are then reconstructed from scratch.
"""

from __future__ import annotations

import argparse
import ast
from collections import Counter
import copy
from fractions import Fraction
import hashlib
import json
import os
from pathlib import Path
import re
import stat
import sys
import tempfile
from typing import Any, Callable, Iterable
import zlib


sys.dont_write_bytecode = True
SELF = Path(__file__).absolute()
ROOT = SELF.parent.parent
OUT = SELF.parent
sys.path.insert(0, str(OUT))

# This is a frozen independent auditor, not either C58s2 or C41 producer.
import cm2_round306c41_d02_lower_strata_depth3_closure_independent_auditor_v1 as c41a  # noqa: E402


BASE = "cm2_round306c58s2_singleton_collision2_handoff_depth6_refinement"
SCHEMA = BASE.replace("cm2_round306c58s2_singleton_", "cm2.round306c58s2.singleton-")
SCHEMA = SCHEMA.replace("_", "-") + ".independent-verifier.v1"
CORE_SCHEMA = "cm2.round306c58s2.singleton-collision2-handoff-depth6-refinement.v1"
HEX64 = re.compile(r"[0-9a-f]{64}\Z")
PAIRS = (31, 188, 200, 270, 321, 410, 471, 474, 631, 711, 787, 853)

PRODUCER = OUT / (BASE + "_v1.py")
RESULT = OUT / (BASE + "_result_v1.json")
LEAVES = OUT / (BASE + "_leaf_ledger_v1.jsonl.gz")
OWNERS = OUT / (BASE + "_face_corner_owner_ledger_v1.jsonl.gz")
HANDOFFS = OUT / (BASE + "_handoff_summary_v1.jsonl.gz")
PARENTS = OUT / (BASE + "_parent_summary_v1.jsonl.gz")

C57_BASE = "cm2_round306c57s1_singleton_collision1_common_refinement"
C57_RESULT = OUT / (C57_BASE + "_result_v1.json")
C57_LEAVES = OUT / (C57_BASE + "_leaf_ledger_v1.jsonl.gz")
C57_MANIFEST = OUT / (C57_BASE + "_manifest_v1.sha256")
C57_VERIFY = OUT / (C57_BASE + "_independent_verification_v1.json")
C57A_BASE = "cm2_round306c57a_singleton_collision1_candidate_independent"
C57A_AUDIT = OUT / (C57A_BASE + "_audit_v1.json")
C57A_MANIFEST = OUT / (C57A_BASE + "_manifest_v1.sha256")
C40 = ROOT / ".cm2-runtime/candidates/c40-h1-endpoint-c2-arrangement-20260810T234000Z-c2f144e29bc1172f"

PIN = {
    "producer_file": "b6f399392fb9a042960d7231aeedf49a083198967e6a40d5c703a8a60e20262a",
    "result_file": "ed4eb1e5ea64c61e4b85a710c1429a2f0b489048320badd4d9a8214bc38c05bc",
    "result_object": "038503bd21505dacde4ce6dc59a320fa70a97cc0dccce33be210c60bbd7d0a30",
    "leaf_file": "15a5b1c5c15f8528591bd80be040317590dadec70b4476d01eb3763ae64965df",
    "owner_file": "f3e9e60b2b0be82fbbceb5a41a3b49547b03080cd414f146146722f5d7c3370f",
    "handoff_file": "d7fa7095dfc5c44d699adf30e19971ddc0be722ddddaf096e0ece0d9bc6cec9c",
    "parent_file": "6f3a8fa4501cb872a33d7446a14d804eeb352bb6d049158f3c7ee88893b7872d",
    "C57_result_file": "9881c22ac4a8630b90b8eb16d81c1670bb6f544e5f4666197d0e6047771d8c4c",
    "C57_result_object": "8cda7681bcbe93c065f1f336842e9fffa6bd3ea67268e96d95fcb3d1f8cbbb58",
    "C57_leaf_file": "918899a914ad4fbb05c1095cac9f42f6c46d02f0acdad366538a395021aeaee6",
    "C57_owner_file": "72d4dd688378166bfd8dbf9ded56ef091014803f80777ea21847a831b4c3f884",
    "C57_parent_file": "8817069967798042bd87315f57e7c3cea279c6564c0e50a5ac927ca4f765e510",
    "C57_manifest_file": "4427e1376811454ad3b6ec5478c1687064cea81f5d33ebd0c13284952928ced0",
    "C57_verify_file": "e1c9849aed542eebdb83856446eba0325af35211c8a9ce714f991b0385918d15",
    "C57_verify_object": "cec8d9bbe3345552b7cb1734c84ed3c1026dc02276780cb6fca9f502118953d6",
    "C57a_audit_file": "9fdbb28605e81de75949486416851f4d2bb233c4953650fcbadd024c12dccbdc",
    "C57a_audit_object": "f7984162bdb64c7cbb828e9d3733103637898007c91c89292b64717145b818c0",
    "C57a_manifest_file": "669377fd362a5c66dd36c75d27685c2f76a0e5661c400dd99494455940d15db5",
    "C40_result_file": "f721b08a4addb7c0369b27ea3af8546c9fad293b1a7808d015bbf783b3aa22d6",
    "C40_object": "397eda962e4bd20429d7cab1ffc53d82cccfdf59bdce8cd03b271a8ded0536ba",
    "C41_independent_auditor_file": "537f3dea94c3743235df8984ba4922d37f82999ff3d8abbac59e5171ef38b74c",
}

C57_MANIFEST_MEMBERS = {
    C57_BASE + "_face_corner_owner_ledger_v1.jsonl.gz": PIN["C57_owner_file"],
    C57_BASE + "_independent_self_test_v1.json": "85a7c7783f1333f6ddebc091864a27ced72b0106fbdc5ec4aa2ecc001cf6bda0",
    C57_BASE + "_independent_verification_v1.json": PIN["C57_verify_file"],
    C57_BASE + "_independent_verifier_v1.py": "046445077aabb0bcd58c9a0368ffd1aee5dd2e83970631397e3303d1692cdbc9",
    C57_BASE + "_leaf_ledger_v1.jsonl.gz": PIN["C57_leaf_file"],
    C57_BASE + "_parent_ledger_v1.jsonl.gz": PIN["C57_parent_file"],
    C57_BASE + "_report_v1.md": "01160ee0b1e5c168bcb5accb234fc16b6e30da7c53362c45c0cf4ceb1c13d71a",
    C57_BASE + "_result_v1.json": PIN["C57_result_file"],
    C57_BASE + "_v1.py": "52184b7211176dcd8b3321d77ac33143457e0be912769d0486d822a57eef0b13",
}
C57A_MANIFEST_MEMBERS = {
    C57A_BASE + "_audit_v1.json": PIN["C57a_audit_file"],
    C57A_BASE + "_report_v1.md": "08d7e495393ab07b3aa363d6aa53d6ba0fffc905d5ba7b93c1b811e9d883aa28",
    C57A_BASE + "_self_test_v1.json": "171d67782e0de1822bf7e069a614c2783ccad08d82a0b353d13e4d96b45111fb",
    C57A_BASE + "_verifier_v1.py": "afa648cc29a1ba627b2e41f7cd45f2d62d1135df212d6483c2c5f7da6e203d1e",
}


class Rejected(RuntimeError):
    pass


def need(condition: bool, label: str) -> None:
    if type(condition) is not bool or not condition:
        raise Rejected(label)


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False,
                      allow_nan=False).encode("utf-8")


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def bytes_sha(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def close(value: dict[str, Any], key: str = "object_sha256") -> dict[str, Any]:
    answer = copy.deepcopy(value)
    need(key not in answer, "already closed:" + key)
    answer[key] = digest(answer)
    return answer


def row_close(value: dict[str, Any]) -> dict[str, Any]:
    answer = copy.deepcopy(value)
    need("row_sha256" not in answer, "row already closed")
    answer["row_sha256"] = digest(answer)
    return answer


def duplicate_guard(items: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in items:
        if key in result:
            raise Rejected("duplicate JSON key:" + key)
        result[key] = value
    return result


def parse(raw: bytes, label: str, canonical_required: bool = False) -> Any:
    need(bool(raw) and not raw.startswith(b"\xef\xbb\xbf"), label + " strict bytes")
    try:
        value = json.loads(
            raw.decode("utf-8", "strict"), object_pairs_hook=duplicate_guard,
            parse_constant=lambda token: (_ for _ in ()).throw(Rejected(label + ":" + token)),
        )
    except Rejected:
        raise
    except Exception as exc:
        raise Rejected(label + " JSON:" + str(exc)) from exc
    if canonical_required:
        need(raw == canonical(value) + b"\n", label + " canonical bytes")
    return value


def fingerprint(value: os.stat_result) -> tuple[int, ...]:
    return (value.st_dev, value.st_ino, value.st_mode, value.st_nlink, value.st_size,
            value.st_mtime_ns, value.st_ctime_ns)


def capture(paths: Iterable[Path], maximum: int = 256 << 20,
            hook: Callable[[], None] | None = None) -> dict[Path, bytes]:
    ordered = tuple(paths)
    need(len(ordered) == len(set(ordered)), "duplicate capture path")
    descriptors: dict[Path, int] = {}
    before: dict[Path, os.stat_result] = {}
    try:
        for path in ordered:
            descriptor = os.open(path, os.O_RDONLY | getattr(os, "O_CLOEXEC", 0) |
                                 getattr(os, "O_NOFOLLOW", 0))
            state = os.fstat(descriptor)
            need(stat.S_ISREG(state.st_mode) and state.st_nlink == 1 and
                 0 < state.st_size <= maximum, "single-link frozen input:" + str(path))
            descriptors[path] = descriptor
            before[path] = state
        raw: dict[Path, bytes] = {}
        for path in ordered:
            chunks: list[bytes] = []
            while block := os.read(descriptors[path], 4 << 20):
                chunks.append(block)
            raw[path] = b"".join(chunks)
        if hook is not None:
            hook()
        for path in ordered:
            need(fingerprint(before[path]) == fingerprint(os.fstat(descriptors[path])) ==
                 fingerprint(os.stat(path, follow_symlinks=False)), "TOCTOU:" + str(path))
        return raw
    finally:
        for descriptor in descriptors.values():
            os.close(descriptor)


def closed_result(raw: bytes, file_pin: str, object_pin: str, label: str) -> dict[str, Any]:
    need(bytes_sha(raw) == file_pin, label + " file pin")
    value = parse(raw, label, canonical_required=True)
    need(type(value) is dict and value.get("object_sha256") == object_pin,
         label + " object claim")
    body = copy.deepcopy(value)
    body.pop("object_sha256")
    need(digest(body) == object_pin, label + " object reconstruction")
    return value


def ledger_rows(raw: bytes, descriptor: dict[str, Any], file_pin: str,
                label: str) -> list[dict[str, Any]]:
    need(bytes_sha(raw) == descriptor.get("sha256") == file_pin, label + " file pin")
    decoder = zlib.decompressobj(16 + zlib.MAX_WBITS)
    try:
        expanded = decoder.decompress(raw, 768 << 20) + decoder.flush()
    except zlib.error as exc:
        raise Rejected(label + " gzip:" + str(exc)) from exc
    need(decoder.eof and not decoder.unused_data and not decoder.unconsumed_tail,
         label + " exactly one gzip member")
    lines = expanded.splitlines(keepends=True)
    need(len(lines) == descriptor.get("row_count"), label + " row count")
    sequence = hashlib.sha256()
    rows: list[dict[str, Any]] = []
    for line in lines:
        row = parse(line, label + " row", canonical_required=True)
        need(type(row) is dict and type(row.get("row_sha256")) is str and
             HEX64.fullmatch(row["row_sha256"]) is not None, label + " row claim")
        body = copy.deepcopy(row)
        claim = body.pop("row_sha256")
        need(digest(body) == claim, label + " row closure")
        sequence.update((claim + "\n").encode("ascii"))
        rows.append(row)
    need(sequence.hexdigest() == descriptor.get("row_hash_line_sequence_sha256"),
         label + " row sequence")
    return rows


def manifest(raw: bytes, expected_sha: str, expected: dict[str, str], label: str,
             captured: dict[Path, bytes]) -> None:
    need(bytes_sha(raw) == expected_sha, label + " manifest pin")
    parsed: dict[str, str] = {}
    for line in raw.decode("ascii", "strict").splitlines():
        fields = line.split("  ", 1)
        need(len(fields) == 2 and HEX64.fullmatch(fields[0]) is not None,
             label + " manifest line")
        need(fields[1] not in parsed, label + " manifest duplicate")
        parsed[fields[1]] = fields[0]
    need(parsed == expected, label + " manifest exact membership")
    for name, claim in expected.items():
        path = OUT / name
        need(bytes_sha(captured[path]) == claim, label + " member:" + name)


def q(value: Any) -> Fraction:
    return Fraction(str(value))


def box_key(box: dict[str, Any]) -> tuple[Fraction, Fraction, Fraction, Fraction]:
    return q(box["t"][0]), q(box["t"][1]), q(box["p"][0]), q(box["p"][1])


def prefix_free(paths: list[str]) -> bool:
    ordered = sorted(paths, key=lambda value: (len(value), value))
    return all(not later.startswith(first) for index, first in enumerate(ordered)
               for later in ordered[index + 1:])


def producer_independence(raw: bytes) -> dict[str, Any]:
    need(bytes_sha(raw) == PIN["producer_file"], "C58 producer source pin")
    tree = ast.parse(raw.decode("utf-8", "strict"), filename=PRODUCER.name)
    imported: list[str] = []
    dynamic: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imported.extend(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            imported.append(node.module or "")
        elif isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id in {
            "exec", "eval", "compile", "__import__",
        }:
            dynamic.append(node.func.id)
    need(not dynamic, "C58 producer dynamic execution token")
    need(not any(PRODUCER.stem in name for name in sys.modules), "C58 producer loaded")
    need(not any(PRODUCER.stem == item for item in imported), "verifier imported C58 producer")
    return {
        "C58_producer_imported": False,
        "C58_producer_executed": False,
        "C58_producer_consumed_as_pinned_inert_bytes_and_AST_only": True,
    }


def core_paths() -> tuple[Path, ...]:
    c57_members = tuple(OUT / name for name in C57_MANIFEST_MEMBERS)
    c57a_members = tuple(OUT / name for name in C57A_MANIFEST_MEMBERS)
    return (
        PRODUCER, RESULT, LEAVES, OWNERS, HANDOFFS, PARENTS,
        C57_MANIFEST, C57A_MANIFEST, *c57_members, *c57a_members,
        Path(c41a.__file__).resolve(), C40 / "result.json",
    )


def frozen_bindings(raw: dict[Path, bytes]) -> tuple[
    dict[str, Any], list[dict[str, Any]], dict[str, Any], dict[str, Any]
]:
    manifest(raw[C57_MANIFEST], PIN["C57_manifest_file"], C57_MANIFEST_MEMBERS,
             "C57", raw)
    manifest(raw[C57A_MANIFEST], PIN["C57a_manifest_file"], C57A_MANIFEST_MEMBERS,
             "C57a", raw)
    c57_result = closed_result(raw[C57_RESULT], PIN["C57_result_file"],
                               PIN["C57_result_object"], "C57 result")
    c57_leaves = ledger_rows(raw[C57_LEAVES], c57_result["ledgers"]["leaves"],
                             PIN["C57_leaf_file"], "C57 leaves")
    c57_verify = closed_result(raw[C57_VERIFY], PIN["C57_verify_file"],
                               PIN["C57_verify_object"], "C57 verification")
    c57a = closed_result(raw[C57A_AUDIT], PIN["C57a_audit_file"],
                         PIN["C57a_audit_object"], "C57a audit")
    need(c57_verify["status"].startswith("PASS_SECOND_COLD_NO_PRODUCER_") and
         c57_verify["formal_credit"] == c57_verify["whole_parent_credit"] ==
         c57_verify["D02_gate_credit"] == 0 and
         c57_verify["coverage"]["exact_collision2_handoffs"] == 319,
         "C57 final verification boundary")
    need(c57a["status"].startswith("PASS_INDEPENDENT_C57S1_") and
         c57a["candidate_is_authority"] is False and
         c57a["formal_credit"] == c57a["D02_gate_credit"] == 0,
         "C57a final audit boundary")
    need(len(c57_leaves) == 781 and
         sum(row["leaf_disposition"] == "STRICT_TERMINAL" for row in c57_leaves) == 462 and
         sum(row["leaf_disposition"] == "COLLISION2_HANDOFF" for row in c57_leaves) == 319,
         "C57 final leaf census")
    for row in c57_leaves:
        if row["leaf_disposition"] == "COLLISION2_HANDOFF":
            handoff = copy.deepcopy(row["collision2_handoff"])
            claim = handoff.pop("handoff_object_sha256", None)
            need(claim == digest(handoff) and row["D02_gate_credit"] ==
                 row["whole_parent_credit"] == 0, "C57 handoff closure/credit")
    return c57_result, c57_leaves, c57_verify, c57a


def numeric_context() -> tuple[list[dict[str, Any]], dict[str, dict[str, Any]],
                               dict[str, dict[str, Any]], dict[str, Any]]:
    need(bytes_sha(Path(c41a.__file__).read_bytes()) == PIN["C41_independent_auditor_file"],
         "C41 independent auditor source pin")
    c41a.source_pins()
    need(bytes_sha((C40 / "result.json").read_bytes()) == PIN["C40_result_file"],
         "C40 result file pin")
    c40_result = c41a.c40a.pinned_result(C40, PIN["C40_object"], "C40 result")
    authority = c40_result["C39_authority"]
    c39_path = (ROOT / authority["path"]).resolve()
    c39_audit = (ROOT / authority["independent_audit_path"]).resolve()
    c39_result, _audit, _rows, _parents = c41a.c40a.load_c39_authority(c39_path, c39_audit)
    c38_index, cells, config = c41a.c40a.load_geometry_authority(c39_result)
    config["cores"] = tuple(c41a.round139.lower.core_cert.physical_cores())
    sources = c41a.c40a.pinned_ledger(C40, c40_result, "routed_leaf_cells",
                                      "C40 routed leaves")
    need(len(sources) == 35009 and len({row["row_sha256"] for row in sources}) == 35009,
         "C40 routed source census/uniqueness")
    c41a.install_complete_cache()
    return sources, c38_index, cells, config


def route_reconstruction(selected: list[dict[str, Any]]) -> tuple[
    list[dict[str, Any]], Counter[str], int
]:
    sources, c38_index, cells, config = numeric_context()
    source_index = {row["row_sha256"]: (ordinal, row)
                    for ordinal, row in enumerate(sources)}
    need(len({row["C40_leaf_row_sha256"] for row in selected}) == 97,
         "97 unique C40 source rows")
    expected: list[dict[str, Any]] = []
    raw_census: Counter[str] = Counter()
    route_cache: dict[tuple[str, str], dict[str, Any]] = {}
    for ordinal, source_handoff in enumerate(selected):
        c57_handoff = source_handoff["collision2_handoff"]
        source_ordinal, source = source_index[source_handoff["C40_leaf_row_sha256"]]
        task = c41a.task_for_source(source_ordinal, source, c38_index, cells,
                                    config["source_chart_seams"])
        stack: list[tuple[str, int, Fraction, str | None]] = [(
            source_handoff["path"], 0, q(source_handoff["parent_volume_fraction"]), None
        )]
        final: list[dict[str, Any]] = []
        while stack:
            path, depth, volume, parent_path = stack.pop()
            key = (source["row_sha256"], path)
            route = route_cache.get(key)
            if route is None:
                route = c41a.independent_route_at_path(task, path, config)
                route_cache[key] = route
            family = c41a.disposition_family(route["classification"])
            if family == "RESIDUAL_OUTER" and depth < 6:
                stack.append((path + "1", depth + 1, volume / 2, path))
                stack.append((path + "0", depth + 1, volume / 2, path))
                continue
            box = c41a.box_payload(route["box"])
            reflected = c41a.reflected_box(
                task["c38_source"]["representative_origin_key"], route["box"])
            if family == "TERMINAL_EXCLUDED":
                disposition = "STRICT_TERMINAL"
                strict_class = "EARLIEST_PREFIX_EXCLUDED"
                next_handoff = None
                c3_ready = None
            elif family == "COLLISION3_READY":
                disposition = "COLLISION3_READY"
                strict_class = None
                next_handoff = None
                c3_ready = {
                    "next_collision_index": 3,
                    "route_classification": route["classification"],
                    "route_witness": route["witness"],
                    "exact_representative_box": box,
                    "exact_reflected_box": reflected,
                    "collision3_ready_credit": 0,
                }
                c3_ready["collision3_ready_object_sha256"] = digest(c3_ready)
            else:
                disposition = "COLLISION2_HANDOFF"
                strict_class = None
                c3_ready = None
                next_handoff = {
                    "next_collision_index": 2,
                    "prior_C57_leaf_row_sha256": source_handoff["row_sha256"],
                    "prior_C57_handoff_object_sha256": c57_handoff["handoff_object_sha256"],
                    "collision1_history_row_sha256": c57_handoff["collision1_history_row_sha256"],
                    "collision1_original_owner": c57_handoff["collision1_original_owner"],
                    "collision1_event_order": c57_handoff["collision1_event_order"],
                    "exact_representative_box": box,
                    "exact_reflected_box": reflected,
                    "route_classification": route["classification"],
                    "route_witness": route["witness"],
                    "route_method": route["route_method"],
                    "residual_classification": c41a.residual_classification(route["classification"]),
                    "c2_status": route["c2_status"],
                    "c2_baseline": route["c2_baseline"],
                    "handoff_credit": 0,
                }
                next_handoff["handoff_object_sha256"] = digest(next_handoff)
            raw_census[route["classification"]] += 1
            final.append({
                "schema": CORE_SCHEMA + ".leaf-row",
                "source_handoff_ordinal": ordinal,
                "source_C57_leaf_row_sha256": source_handoff["row_sha256"],
                "source_C57_handoff_object_sha256": c57_handoff["handoff_object_sha256"],
                "pair_index": source_handoff["pair_index"],
                "path": path,
                "additional_depth": depth,
                "parent_path": parent_path,
                "parent_volume_fraction": str(volume),
                "representative_cell_id": source_handoff["representative_cell_id"],
                "reflected_cell_id": source_handoff["reflected_cell_id"],
                "exact_representative_box": box,
                "exact_reflected_box": reflected,
                "C40_source_row_sha256": source["row_sha256"],
                "route_classification": route["classification"],
                "route_witness": route["witness"],
                "route_method": route["route_method"],
                "disposition": disposition,
                "strict_terminal_class": strict_class,
                "collision2_handoff": next_handoff,
                "collision3_ready": c3_ready,
                "face_corner_owner_row_sha256s": [],
                "face_owner_count": 0,
                "corner_owner_count": 0,
                "owner_rows_complete": False,
                "local_terminal_credit": 1 if disposition == "STRICT_TERMINAL" else 0,
                "collision3_ready_credit": 0,
                "whole_parent_credit": 0,
                "D02_gate_credit": 0,
            })
        final.sort(key=lambda row: row["path"])
        need(prefix_free([row["path"] for row in final]) and
             sum(q(row["parent_volume_fraction"]) for row in final) ==
             q(source_handoff["parent_volume_fraction"]),
             "independent per-handoff prefix/Kraft")
        expected.extend(final)
    expected.sort(key=lambda row: (row["source_handoff_ordinal"], row["path"]))
    return expected, raw_census, len(route_cache)


def owner_reconstruction(open_leaves: list[dict[str, Any]],
                         observed: list[dict[str, Any]]) -> list[dict[str, Any]]:
    line_segments: dict[tuple[int, str, Fraction], list[tuple[Fraction, Fraction, str]]] = {}
    corners: dict[tuple[int, Fraction, Fraction], set[str]] = {}
    leaf_id_by_index: dict[int, str] = {}
    path_by_id: dict[str, str] = {}
    for index, row in enumerate(open_leaves):
        leaf_id = "c58s2-leaf:" + digest({
            "source": row["source_C57_leaf_row_sha256"], "path": row["path"]
        })
        need(leaf_id not in path_by_id, "independent leaf id uniqueness")
        leaf_id_by_index[index] = leaf_id
        path_by_id[leaf_id] = row["path"]
        t0, t1, p0, p1 = box_key(row["exact_representative_box"])
        need(t0 < t1 and p0 < p1, "positive exact leaf box")
        for axis, coordinate, low, high in (
            ("t", t0, p0, p1), ("t", t1, p0, p1),
            ("p", p0, t0, t1), ("p", p1, t0, t1),
        ):
            line_segments.setdefault((row["pair_index"], axis, coordinate), []).append(
                (low, high, leaf_id))
        for t in (t0, t1):
            for p in (p0, p1):
                corners.setdefault((row["pair_index"], t, p), set()).add(leaf_id)

    expected_owners: list[dict[str, Any]] = []
    refs: dict[str, list[str]] = {leaf_id: [] for leaf_id in path_by_id}
    face_refs: dict[str, list[str]] = {leaf_id: [] for leaf_id in path_by_id}
    corner_refs: dict[str, list[str]] = {leaf_id: [] for leaf_id in path_by_id}
    for (pair, axis, coordinate), segments in sorted(line_segments.items(), key=str):
        endpoints = sorted({point for low, high, _leaf in segments for point in (low, high)})
        for low, high in zip(endpoints, endpoints[1:]):
            incident = sorted({leaf for start, stop, leaf in segments
                               if start <= low and high <= stop})
            if not incident:
                continue
            owner = min(incident, key=lambda leaf: (path_by_id[leaf], leaf))
            closed = row_close({
                "schema": CORE_SCHEMA + ".owner-row", "pair_index": pair,
                "atom_kind": "FACE", "axis": axis, "coordinate": str(coordinate),
                "span": [str(low), str(high)], "incident_leaf_ids": incident,
                "incident_leaf_count": len(incident),
                "owner_rule": "LEXICOGRAPHIC_MINIMUM_PATH_THEN_LEAF_ID",
                "owner_leaf_id": owner, "owner_unique": True,
                "owner_credit": 0, "D02_gate_credit": 0,
            })
            expected_owners.append(closed)
            for leaf in incident:
                refs[leaf].append(closed["row_sha256"])
                face_refs[leaf].append(closed["row_sha256"])
    for (pair, t, p), incident_set in sorted(corners.items(), key=str):
        incident = sorted(incident_set)
        owner = min(incident, key=lambda leaf: (path_by_id[leaf], leaf))
        closed = row_close({
            "schema": CORE_SCHEMA + ".owner-row", "pair_index": pair,
            "atom_kind": "CORNER", "t": str(t), "p": str(p),
            "incident_leaf_ids": incident, "incident_leaf_count": len(incident),
            "owner_rule": "LEXICOGRAPHIC_MINIMUM_PATH_THEN_LEAF_ID",
            "owner_leaf_id": owner, "owner_unique": True,
            "owner_credit": 0, "D02_gate_credit": 0,
        })
        expected_owners.append(closed)
        for leaf in incident:
            refs[leaf].append(closed["row_sha256"])
            corner_refs[leaf].append(closed["row_sha256"])
    need(len(expected_owners) == 21227 and expected_owners == observed,
         "21,227 exact atomized owner rows/order/incidence/unique owner")

    closed_leaves: list[dict[str, Any]] = []
    for index, row in enumerate(open_leaves):
        leaf_id = leaf_id_by_index[index]
        need(len(face_refs[leaf_id]) >= 4 and len(corner_refs[leaf_id]) == 4,
             "independent owner completeness")
        value = copy.deepcopy(row)
        value["face_corner_owner_row_sha256s"] = sorted(refs[leaf_id])
        value["face_owner_count"] = len(face_refs[leaf_id])
        value["corner_owner_count"] = len(corner_refs[leaf_id])
        value["owner_rows_complete"] = True
        value["leaf_id"] = leaf_id
        closed_leaves.append(row_close(value))
    return closed_leaves


def aggregate_reconstruction(selected: list[dict[str, Any]], carried: list[dict[str, Any]],
                             leaves: list[dict[str, Any]],
                             observed_handoffs: list[dict[str, Any]],
                             observed_parents: list[dict[str, Any]]) -> tuple[int, int]:
    by_source: dict[str, list[dict[str, Any]]] = {}
    for row in leaves:
        by_source.setdefault(row["source_C57_leaf_row_sha256"], []).append(row)
    expected_handoffs: list[dict[str, Any]] = []
    whole_handoffs = 0
    for ordinal, source in enumerate(selected):
        rows = by_source[source["row_sha256"]]
        paths = [row["path"] for row in rows]
        kraft = sum(q(row["parent_volume_fraction"]) for row in rows)
        terminal = sum(row["disposition"] == "STRICT_TERMINAL" for row in rows)
        c3 = sum(row["disposition"] == "COLLISION3_READY" for row in rows)
        residual = len(rows) - terminal - c3
        whole_terminal = terminal == len(rows)
        whole_no_residual = residual == 0
        whole_handoffs += int(whole_terminal)
        need(prefix_free(paths) and kraft == q(source["parent_volume_fraction"]),
             "aggregate per-handoff prefix/Kraft")
        expected_handoffs.append(row_close({
            "schema": CORE_SCHEMA + ".handoff-summary-row",
            "source_handoff_ordinal": ordinal,
            "source_C57_leaf_row_sha256": source["row_sha256"],
            "pair_index": source["pair_index"], "source_path": source["path"],
            "source_parent_volume_fraction": source["parent_volume_fraction"],
            "refined_leaf_count": len(rows), "strict_terminal_leaf_count": terminal,
            "collision3_ready_leaf_count": c3,
            "collision2_handoff_leaf_count": residual,
            "path_prefix_free": True,
            "Kraft_conservation": source["parent_volume_fraction"],
            "whole_source_handoff_terminal": whole_terminal,
            "whole_source_handoff_terminal_or_collision3_ready": whole_no_residual,
            "whole_handoff_credit": 0, "D02_gate_credit": 0,
        }))
    need(expected_handoffs == observed_handoffs and whole_handoffs == 38,
         "319 exact handoff summaries and 38 whole terminal")

    by_pair: dict[int, list[dict[str, Any]]] = {pair: [] for pair in PAIRS}
    for row in carried:
        by_pair[row["pair_index"]].append(row)
    for row in leaves:
        by_pair[row["pair_index"]].append(row)
    expected_parents: list[dict[str, Any]] = []
    whole_pairs = 0
    for pair in PAIRS:
        rows = by_pair[pair]
        paths = [row["path"] for row in rows]
        kraft = sum(q(row["parent_volume_fraction"]) for row in rows)
        residual = sum(row.get("disposition") == "COLLISION2_HANDOFF" for row in rows)
        c3 = sum(row.get("disposition") == "COLLISION3_READY" for row in rows)
        terminal = len(rows) - residual - c3
        whole = residual == 0 and c3 == 0
        whole_pairs += int(whole)
        need(prefix_free(paths) and kraft == 1, "combined parent prefix/Kraft")
        expected_parents.append(row_close({
            "schema": CORE_SCHEMA + ".parent-summary-row", "pair_index": pair,
            "combined_leaf_count": len(rows), "strict_terminal_leaf_count": terminal,
            "collision3_ready_leaf_count": c3,
            "collision2_handoff_leaf_count": residual,
            "path_prefix_free": True, "parent_Kraft_conservation": "1",
            "whole_representative_parent_terminal": whole,
            "whole_reflected_parent_terminal": whole,
            "whole_pair_credit": 0, "D02_gate_credit": 0,
        }))
    need(expected_parents == observed_parents and whole_pairs == 0,
         "12 exact combined parent summaries/prefix/Kraft/nonclosure")
    return whole_handoffs, whole_pairs


def verify() -> dict[str, Any]:
    raw = capture(core_paths(), maximum=32 << 20)
    independence = producer_independence(raw[PRODUCER])
    result = closed_result(raw[RESULT], PIN["result_file"], PIN["result_object"],
                           "C58s2 result")
    need(result["schema"] == CORE_SCHEMA and result["status"] ==
         "PASS_EXACT_DEPTH6_CONTINUATION__319_INPUT_HANDOFFS__5548_LEAVES__2949_TERMINAL__0_C3_READY__2599_EXACT_C2_HANDOFFS__ZERO_WHOLE_SINGLETON_CLOSED",
         "C58s2 schema/status")
    observed_leaves = ledger_rows(raw[LEAVES], result["ledgers"]["leaves"],
                                  PIN["leaf_file"], "C58 leaves")
    observed_owners = ledger_rows(raw[OWNERS], result["ledgers"]["face_corner_owners"],
                                  PIN["owner_file"], "C58 owners")
    observed_handoffs = ledger_rows(raw[HANDOFFS], result["ledgers"]["handoff_summaries"],
                                    PIN["handoff_file"], "C58 handoff summaries")
    observed_parents = ledger_rows(raw[PARENTS], result["ledgers"]["parent_summaries"],
                                   PIN["parent_file"], "C58 parent summaries")
    need((len(observed_leaves), len(observed_owners), len(observed_handoffs),
          len(observed_parents)) == (5548, 21227, 319, 12), "C58 ledger census")
    c57_result, c57_leaves, c57_verify, c57a = frozen_bindings(raw)
    selected = [row for row in c57_leaves if row["leaf_disposition"] == "COLLISION2_HANDOFF"]
    carried = [row for row in c57_leaves if row["leaf_disposition"] == "STRICT_TERMINAL"]
    need(result["frozen_inputs"] == {
        "C57_result_object_sha256": PIN["C57_result_object"],
        "C57_result_file_sha256": PIN["C57_result_file"],
        "C57_leaf_file_sha256": PIN["C57_leaf_file"],
        "C57_owner_file_sha256": PIN["C57_owner_file"],
        "C57_parent_file_sha256": PIN["C57_parent_file"],
        "C57_manifest_sha256": PIN["C57_manifest_file"],
        "C57_independent_verification_object_sha256": PIN["C57_verify_object"],
        "C57a_audit_object_sha256": PIN["C57a_audit_object"],
        "C57a_manifest_sha256": PIN["C57a_manifest_file"],
        "C40_object_sha256": PIN["C40_object"],
    }, "C58 frozen C57/C57a/C40 bindings")

    open_expected, raw_census, route_evaluations = route_reconstruction(selected)
    need(route_evaluations == 10777 and len(open_expected) == 5548,
         "independent route evaluation/leaf census")
    closed_expected = owner_reconstruction(open_expected, observed_owners)
    need(closed_expected == observed_leaves, "5,548 exact independently routed leaf rows")
    whole_handoffs, whole_pairs = aggregate_reconstruction(
        selected, carried, closed_expected, observed_handoffs, observed_parents)

    dispositions = Counter(row["disposition"] for row in closed_expected)
    need(dispositions == Counter({"STRICT_TERMINAL": 2949,
                                  "COLLISION2_HANDOFF": 2599}) and
         all(row["collision3_ready"] is None and row["collision3_ready_credit"] == 0
             for row in closed_expected), "independent 2949/0/2599 disposition census")
    need(result["routing"] == {
        "maximum_additional_dyadic_depth": 6,
        "exact_route_evaluations": 10777,
        "input_C57_handoffs": 319,
        "unique_C40_source_rows": 97,
        "refined_leaf_count": 5548,
        "raw_classification_census": dict(sorted(raw_census.items())),
        "disposition_census": {
            "STRICT_TERMINAL": 2949, "COLLISION3_READY": 0,
            "COLLISION2_HANDOFF": 2599,
        },
        "whole_input_handoffs_terminal": 38,
        "whole_input_handoffs_terminal_or_collision3_ready": 38,
    }, "C58 reconstructed routing census")
    need(result["strict_boundary"] == {
        "C1_equality_carriers_relabelled_C3_ready": False,
        "unrelated_C40_C2_rows_imported": False,
        "whole_pairs_closed": 0, "whole_singletons_closed": 0,
        "whole_singletons_remaining": 24, "formal_credit": 0,
        "whole_parent_credit": 0, "D02_gate_credit": 0,
        "runtime_writes_performed": False, "canonical_writes_performed": False,
    } and whole_handoffs == 38 and whole_pairs == 0,
         "C58 strict zero-credit/nonpromotion boundary")

    return close({
        "schema": SCHEMA + ".verification",
        "status": "PASS_COLD_NO_C58_PRODUCER_EXACT_NUMERIC_REPLAY__319_TO_5548__2949_TERMINAL__0_C3__2599_C2__21227_ATOMIC_OWNERS__12_KRAFT_ONE__ZERO_CREDIT",
        "frozen_core": {
            "producer_file_sha256": PIN["producer_file"],
            "result_file_sha256": PIN["result_file"],
            "result_object_sha256": PIN["result_object"],
            "leaf_ledger_sha256": PIN["leaf_file"],
            "owner_ledger_sha256": PIN["owner_file"],
            "handoff_summary_sha256": PIN["handoff_file"],
            "parent_summary_sha256": PIN["parent_file"],
        },
        "frozen_input_cosigns": {
            "C57_result_object_sha256": c57_result["object_sha256"],
            "C57_verification_object_sha256": c57_verify["object_sha256"],
            "C57_manifest_sha256": PIN["C57_manifest_file"],
            "C57a_audit_object_sha256": c57a["object_sha256"],
            "C57a_manifest_sha256": PIN["C57a_manifest_file"],
            "C40_object_sha256": PIN["C40_object"],
        },
        "coverage": {
            "input_C57_handoffs": 319, "unique_C40_source_rows": 97,
            "independent_numeric_route_evaluations": 10777,
            "refined_leaf_rows": 5548, "strict_terminal_leaves": 2949,
            "collision3_ready_leaves": 0, "exact_collision2_handoffs": 2599,
            "whole_input_handoffs_terminal": 38,
            "atomic_face_corner_owner_rows": 21227,
            "combined_parent_rows": 12, "reflection_pairs": 12,
            "singleton_cells": 24,
        },
        "reconstructed_invariants": {
            "all_numeric_routes_boxes_witnesses_methods_and_dispositions_exact": True,
            "all_2599_collision2_handoff_objects_and_C57_histories_exact": True,
            "all_21227_atomized_geometries_incidence_sets_and_unique_owners_exact": True,
            "all_leaf_owner_reference_sets_complete": True,
            "all_319_source_partitions_prefix_free_and_Kraft_conserved": True,
            "all_12_combined_parent_partitions_prefix_free_and_Kraft_one": True,
            "no_C1_equality_carrier_relabelled_collision3_ready": True,
        },
        "whole_singletons_closed": 0,
        "whole_singletons_remaining": 24,
        "candidate_is_authority": False,
        "formal_credit": 0,
        "whole_parent_credit": 0,
        "D02_gate_credit": 0,
        "runtime_canonical_pointer_or_seal_writes": False,
        "independence": independence,
    })


def synthetic_baseline() -> dict[str, Any]:
    return close({
        "schema": "synthetic.c58s2", "inputs": 319, "C40_sources": 97,
        "route_evaluations": 10777, "maximum_depth": 6, "leaves": 5548,
        "terminal": 2949, "C3": 0, "C2": 2599, "owners": 21227,
        "whole_handoffs": 38, "parents": 12, "next_collision": 2,
        "C57_bound": True, "C57a_bound": True, "numeric_replay": True,
        "exact_boxes": True, "exact_witnesses": True, "owner_geometry": True,
        "owner_incidence": True, "owner_unique": True, "owner_refs": True,
        "prefix_free": True, "Kraft": "1", "whole_pairs": 0,
        "whole_singletons": 0, "formal_credit": 0, "whole_parent_credit": 0,
        "owner_credit": 0, "D02_gate_credit": 0,
    })


def synthetic_validate(value: dict[str, Any]) -> None:
    baseline = synthetic_baseline()
    need(type(value) is dict and set(value) == set(baseline), "synthetic closed schema")
    body = copy.deepcopy(value)
    claim = body.pop("object_sha256")
    need(claim == digest(body) and value == baseline, "synthetic exact invariants")


def self_test() -> dict[str, Any]:
    baseline = synthetic_baseline()
    synthetic_validate(baseline)
    tests: dict[str, bool] = {"baseline_valid": True}
    attacks: list[tuple[str, Any]] = [
        ("inputs", 318), ("C40_sources", 96), ("route_evaluations", 10776),
        ("maximum_depth", 5), ("leaves", 5547), ("terminal", 2950),
        ("C3", 1), ("C2", 2598), ("owners", 21226), ("whole_handoffs", 39),
        ("parents", 11), ("next_collision", 3), ("C57_bound", False),
        ("C57a_bound", False), ("numeric_replay", False), ("exact_boxes", False),
        ("exact_witnesses", False), ("owner_geometry", False),
        ("owner_incidence", False), ("owner_unique", False), ("owner_refs", False),
        ("prefix_free", False), ("Kraft", "2047/2048"), ("whole_pairs", 1),
        ("whole_singletons", 2), ("formal_credit", 1), ("whole_parent_credit", 1),
        ("owner_credit", 1), ("D02_gate_credit", 1),
    ]
    for field, replacement in attacks:
        attacked = copy.deepcopy(baseline)
        attacked.pop("object_sha256")
        attacked[field] = replacement
        attacked = close(attacked)
        try:
            synthetic_validate(attacked)
        except Rejected:
            tests["coherent_" + field + "_rejected"] = True
    malformed = (
        ("duplicate_key", b'{"a":1,"a":2}\n'),
        ("NaN", b'{"a":NaN}\n'),
        ("BOM", b'\xef\xbb\xbf{"a":1}\n'),
        ("trailing_bytes", b'{"a":1}\nX'),
    )
    for name, value in malformed:
        try:
            parse(value, name, canonical_required=True)
        except Rejected:
            tests[name + "_rejected"] = True
    with tempfile.TemporaryDirectory(prefix="cm2-c58s2-cold-") as temporary:
        root = Path(temporary)
        target = root / "target"
        target.write_bytes(canonical(baseline) + b"\n")
        link = root / "link"
        link.symlink_to(target.name)
        try:
            capture((link,))
        except OSError:
            tests["symlink_rejected"] = True
        hard = root / "hard"
        os.link(target, hard)
        try:
            capture((target,))
        except Rejected:
            tests["hardlink_rejected"] = True
        hard.unlink()
        replacement = root / "replacement"
        replacement.write_bytes(canonical(baseline) + b"\n")
        try:
            capture((target,), hook=lambda: os.replace(replacement, target))
        except Rejected:
            tests["TOCTOU_replacement_rejected"] = True
    source = capture((PRODUCER,))[PRODUCER]
    tests["C58_producer_not_imported_or_executed"] = not producer_independence(source)[
        "C58_producer_imported"]
    need(len(tests) == 38 and all(tests.values()), "38/38 hostile tests")
    return close({
        "schema": SCHEMA + ".self-test",
        "status": "PASS_38_OF_38_EXECUTED_COHERENT_HOSTILE_TESTS",
        "tests": tests, "test_count": 38,
        "synthetic_is_authority": False, "formal_credit": 0,
        "whole_parent_credit": 0, "D02_gate_credit": 0,
        "runtime_canonical_pointer_or_seal_writes": False,
    })


def main() -> int:
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--verify", action="store_true")
    group.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    try:
        value = verify() if args.verify else self_test()
        sys.stdout.buffer.write(canonical(value) + b"\n")
        return 0
    except (Rejected, c41a.Reject, OSError, KeyError, ValueError, zlib.error) as exc:
        failure = close({
            "schema": SCHEMA + ".fail-closed", "status": "FAIL_CLOSED_REJECTED",
            "reason": str(exc), "formal_credit": 0, "whole_parent_credit": 0,
            "D02_gate_credit": 0, "runtime_canonical_pointer_or_seal_writes": False,
        })
        sys.stdout.buffer.write(canonical(failure) + b"\n")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
