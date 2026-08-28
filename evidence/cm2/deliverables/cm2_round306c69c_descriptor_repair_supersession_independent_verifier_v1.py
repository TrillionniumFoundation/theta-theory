#!/usr/bin/env python3
"""Cold no-producer verifier for the C69c descriptor-repair successor.

C69b/C69c producer and wrapper sources are forbidden inputs.  The verifier
rebuilds the 20,879-row partition from frozen C68/C61/C58/C40/C39/C38 data,
independently recomputes every C69b numeric H1 certificate with the approved
Round185 implementation, and validates the C69c supersession bundle.
"""
from __future__ import annotations

import ast
import copy
import gc
import gzip
import hashlib
import io
import itertools
import json
import os
import stat
import sys
import tempfile
import zlib
from collections import Counter
from fractions import Fraction as Q
from pathlib import Path
from typing import Any, Iterable

sys.dont_write_bytecode = True

SELF = Path(__file__).resolve()
ROOT = SELF.parents[1]
OUT = ROOT / "deliverables"
PREFIX = "cm2_round306c69c_descriptor_repair_supersession_v1"
SCHEMA = "cm2.round306c69c.descriptor-repair-supersession.v1"
VERIFY_NAME = "cm2_round306c69c_descriptor_repair_supersession_independent_verification_v1.json"
SELFTEST_NAME = "cm2_round306c69c_descriptor_repair_supersession_independent_self_test_v1.json"
REPORT_NAME = "cm2_round306c69c_descriptor_repair_supersession_independent_report_v1.md"
MANIFEST_NAME = "cm2_round306c69c_descriptor_repair_supersession_independent_manifest_v1.sha256"
OUTER_NAME = "cm2_round306c69c_descriptor_repair_supersession_independent_outer_publication_receipt_v1.json"
FROZEN_AUTHORITY = "cdb6f4be57b2732a6ad67f4113a41c338934358e8e3102f71e1a958c2c46e8c2"
C69B_PRODUCER = "e45244027963f11f150127b83803416d516af166f030d192a32648e3ff15f549"
C69C_PRODUCER = "f3aca95d1f62af78cf9ed7037c473c45ccaca31a9ed43547c31950e5e06173d8"
C69B_CONTRACT_OBJECT = "3aa04ebd6ca8c7e7e07656817dd3c75366894014aba26a7d034782a553e23faf"
C69B_SEMANTIC_PAYLOAD = "dd3374c482442dc77278c87faac7c589cccbfc9a6bcecfc724bb9f912b535f0d"
MAX_INFLATE = 600 * 1024 * 1024

C38_DIR = ROOT / ".cm2-runtime/candidates/c38-collision1-2-child-atlas-20260810T180156Z-0d5047fe3a316133"
C39_DIR = ROOT / ".cm2-runtime/candidates/c39-h1-c1-graph-router-20260810T185014Z-e004fadaadcd5559"
C40_DIR = ROOT / ".cm2-runtime/candidates/c40-h1-endpoint-c2-arrangement-20260810T234000Z-c2f144e29bc1172f"

FILES = {
    "contract": OUT / f"{PREFIX}_contract.json",
    "corrected": OUT / f"{PREFIX}_corrected_result.json",
    "rejection": OUT / f"{PREFIX}_rejection.json",
    "receipt": OUT / f"{PREFIX}_deterministic_two_stage_publication_receipt.json",
    "report": OUT / f"{PREFIX}_report.md",
    "c69b_contract": OUT / "cm2_round306c69b_singleton_h1_graph_slab_decider_v2_contract.json",
    "c69b_result": OUT / "cm2_round306c69b_singleton_h1_graph_slab_decider_v2_result.json",
    "c69b_receipt": OUT / "cm2_round306c69b_singleton_h1_graph_slab_decider_v2_deterministic_two_stage_publication_receipt.json",
    "decisions": OUT / "cm2_round306c69b_singleton_h1_graph_slab_decider_v2_decisions.jsonl.gz",
    "blockers": OUT / "cm2_round306c69b_singleton_h1_graph_slab_decider_v2_blockers.jsonl.gz",
    "covers": OUT / "cm2_round306c69b_singleton_h1_graph_slab_decider_v2_parametric_newton_covers.jsonl.gz",
    "c68_result": OUT / "cm2_round306c68l_blocker_crosswalk_result_v1.json",
    "c68_tasks": OUT / "cm2_round306c68l_blocker_crosswalk_singleton_structural_tasks_v1.jsonl.gz",
    "c61_result": OUT / "cm2_round306c61s12_depth12_16shard_aggregate_result_v4.json",
    "c61_leaves": OUT / "cm2_round306c61s12_depth12_16shard_aggregate_leaf_ledger_v4.jsonl.gz",
    "c58_result": OUT / "cm2_round306c58s2_singleton_collision2_handoff_depth6_refinement_result_v1.json",
    "c58_leaves": OUT / "cm2_round306c58s2_singleton_collision2_handoff_depth6_refinement_leaf_ledger_v1.jsonl.gz",
    "c40_result": C40_DIR / "result.json",
    "c40_rows": C40_DIR / "routed_leaf_cells.jsonl.gz",
    "c39_result": C39_DIR / "result.json",
    "c39_rows": C39_DIR / "routed_child_pairs.jsonl.gz",
    "c38_result": C38_DIR / "result.json",
    "c38_rows": C38_DIR / "collision1_2_child_pairs.jsonl.gz",
    "r185": OUT / "cm2_round185_preconditioned_c1_residual_refinement.py",
}

PINS = {
    "contract": "0a3a62fbbd6d51fcc0f1396cd0bedcb36a3e5d6a94fc5660ea5c0d8ea9874e33",
    "contract_object": "ad0baab94fafc9230f558730f3007f0cea73ac78808a458cd85f840b66f05c3e",
    "corrected": "607fc73ebe3333ca172eb15c0831b8c3d98192c86e20eec7a59a69c4ae4737d4",
    "corrected_object": "e52904a7d8ba73c855e69e390cd3cf29c233ffe492e6fae74efdf0b6d4d0a6a5",
    "rejection": "ddfc4c7221e3129935fd32f9dca633e070e3bf4b0b0c1b7ef984fec338214d9e",
    "rejection_object": "53819b3c95c841616b6de709745b73616112267caf36c976ec878a7da1851cd1",
    "receipt": "01dd70471ae60964c341bc7d2b70adcf598f27c28e29e9d4514f4ba57b0a40ff",
    "receipt_object": "cb888ef4cd4a9e60a8ec2052d89e9eede6158838a6acb2aeabf27f142c540c92",
    "report": "2fc3ce3ca8f497c40c852dffd9222b91471d5d598ad453162cb20e5daa960b60",
    "c69b_contract": "1d0da21eb1f6a658d0b072eb4ae56e7f1086e5c3c19c47252d8ba333cc13d36d",
    "c69b_result": "63a1faa4528e35a0bbbbe282befeaeb75eda1f8635634c22572bddfc91e953b3",
    "c69b_result_object": "243776d4856652b307bd8dc9198992b1ac9bae9761017b4b764bbcd351c1da8b",
    "c69b_receipt": "e849a5e3d03872657f7619c62831777dd5130f1801aed61d477d49e8e4505030",
    "c69b_receipt_object": "ed5cb9200bd0ab71bf0cff5ffc484c2ab1daef978e34c4e91a621cfaba182418",
    "decisions": "b9bc1cd359c77ee6a5246011925090e5d5557cd88e90d1f5c67fa70a452d1eba",
    "blockers": "69b3ec294f95cb5ce377e553ae875daab10a5bdb33e860363f6bae122022e606",
    "covers": "e8512d9f325e305e134400dac27c7c62ee374a1957d12f0acce797d00a7dd259",
    "c68_result": "81cf9b6e3fbf2330f747af6430410026406cad8a1a2eb862be974235b2b60f37",
    "c68_result_object": "551c28d03ee59e3fadc2b593dc2575acf911545ce0e6527f9ef0270dfc08d3b2",
    "c68_tasks": "c2d174d9a7e076a52474cde03e02ecdc11172251fe70a5b0273b4aa57c480b8b",
    "c61_result": "06b4146185cb6ef0c8d908d523369008481f7df4e6a05ad5956c001267b07f5e",
    "c61_result_object": "05bcb4301ac74aefd6744db2e633c2479c423fab881b33609bf7234a5537e584",
    "c61_leaves": "2656bc4d1b99d37da3733338d85c8d6301621563a400d5db40380078c001b1c2",
    "c58_result": "ed4eb1e5ea64c61e4b85a710c1429a2f0b489048320badd4d9a8214bc38c05bc",
    "c58_result_object": "038503bd21505dacde4ce6dc59a320fa70a97cc0dccce33be210c60bbd7d0a30",
    "c58_leaves": "15a5b1c5c15f8528591bd80be040317590dadec70b4476d01eb3763ae64965df",
    "c40_result": "f721b08a4addb7c0369b27ea3af8546c9fad293b1a7808d015bbf783b3aa22d6",
    "c40_result_object": "397eda962e4bd20429d7cab1ffc53d82cccfdf59bdce8cd03b271a8ded0536ba",
    "c40_rows": "175293702adf1b76600321c1db326a1a6744dbc8caea439ddaeff9779d1f9b5a",
    "c39_result": "f9bfacbdaaf5263ba16397e70fe56b4f31149087c2434b7c163ff284b40cfd7e",
    "c39_result_object": "821c84d3793bcd941e0a574302bf6c5a0835b46f852156a56fde6ec0353d7e02",
    "c39_rows": "7fcd29f06cb637953e75718b6c91f7e40a36ed702a9a76a4450bf0d7f55daf40",
    "c38_result": "094eb7cf3fca64451aaad80bdd970a8a39a58244e492ed3d2c69f63c70ed3501",
    "c38_result_object": "fba83cdd6eb0eb7d0b71989189ad61ba099e0c440b1f31c3c5aa01b9fbc4f434",
    "c38_rows": "0347849c0368368430f5456b71cd4a4bce4e5912c8a3da33649cfac35b1708a2",
    "r185": "7b48f3ee3417fcfdf5ef6c852e0ab591eb849b357e704e46ee3aaa259d20acc2",
}

ACTUAL = {
    "decisions": {"sha256": PINS["decisions"], "size": 1280359, "row_count": 2356,
                  "row_hash_line_sequence_sha256": "706e6d15b3cf5a9f010c20e77974528399696dd2df18f4c65ceabfe1c4a4c040"},
    "blockers": {"sha256": PINS["blockers"], "size": 3179863, "row_count": 18523,
                 "row_hash_line_sequence_sha256": "7b14e43030218bb448a3192e1e27a03e48ebf0a1627f8cd59a6167c7fb39e7e7"},
    "parametric_newton_covers": {"sha256": PINS["covers"], "size": 850, "row_count": 2,
                                 "row_hash_line_sequence_sha256": "bd9b02cd7d27e55158b4dd964ce42cf0603f4725ba16f07f47e4b2d4623f442d"},
}


class FailClosed(RuntimeError):
    pass


def need(value: bool, label: str) -> None:
    if type(value) is not bool or not value:
        raise FailClosed(label)


def enc(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False).encode()


def h(value: Any) -> str:
    return hashlib.sha256(enc(value)).hexdigest()


def seq(values: Iterable[str]) -> str:
    d = hashlib.sha256()
    for value in values:
        d.update(value.encode("ascii") + b"\n")
    return d.hexdigest()


def ident(st: os.stat_result) -> dict[str, int]:
    return {"dev": st.st_dev, "ino": st.st_ino, "mode": st.st_mode, "size": st.st_size,
            "mtime_ns": st.st_mtime_ns, "ctime_ns": st.st_ctime_ns, "nlink": st.st_nlink}


def secure(path: Path, expected: str | None = None) -> tuple[bytes, dict[str, int]]:
    before = os.lstat(path)
    need(stat.S_ISREG(before.st_mode) and before.st_nlink == 1, "regular-single-link:" + path.name)
    fd = os.open(path, os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0))
    try:
        opened = os.fstat(fd)
        need(ident(before) == ident(opened), "path-fd:" + path.name)
        chunks: list[bytes] = []
        while True:
            chunk = os.read(fd, 1 << 20)
            if not chunk:
                break
            chunks.append(chunk)
        need(ident(os.fstat(fd)) == ident(opened), "fd-post:" + path.name)
    finally:
        os.close(fd)
    need(ident(os.lstat(path)) == ident(before), "path-post:" + path.name)
    raw = b"".join(chunks)
    if expected is not None:
        need(hashlib.sha256(raw).hexdigest() == expected, "sha256:" + path.name)
    return raw, ident(before)


def close_object(value: dict[str, Any], expected: str | None, label: str) -> str:
    body = dict(value); claimed = body.pop("object_sha256", None); actual = h(body)
    need(claimed == actual and (expected is None or actual == expected), "object:" + label)
    return actual


def close_row(value: dict[str, Any], label: str) -> None:
    body = dict(value); claimed = body.pop("row_sha256", None)
    need(claimed == h(body), "row:" + label)


def strict_json(raw: bytes, label: str) -> dict[str, Any]:
    need(raw.endswith(b"\n") and not raw.endswith(b"\n\n"), "one-terminal-newline:" + label)
    need(not raw.startswith(b"\xef\xbb\xbf") and b"\x00" not in raw, "encoding:" + label)
    def pairs(items: list[tuple[str, Any]]) -> dict[str, Any]:
        out: dict[str, Any] = {}
        for key, value in items:
            need(key not in out, "duplicate-key:" + label + ":" + key); out[key] = value
        return out
    value = json.loads(raw.decode("utf-8", "strict"), object_pairs_hook=pairs,
                       parse_float=lambda text: (_ for _ in ()).throw(FailClosed("float:" + text)),
                       parse_constant=lambda text: (_ for _ in ()).throw(FailClosed("constant:" + text)))
    need(type(value) is dict, "top-object:" + label)
    need(enc(value) + b"\n" == raw, "canonical-compact-json:" + label)
    return value


def inflate_single(raw: bytes, label: str, limit: int = MAX_INFLATE) -> bytes:
    inflater = zlib.decompressobj(16 + zlib.MAX_WBITS)
    output = inflater.decompress(raw, limit + 1)
    need(len(output) <= limit and inflater.eof, "gzip-bounded-complete:" + label)
    need(not inflater.unused_data and not inflater.unconsumed_tail, "gzip-single-member-no-trailing:" + label)
    output += inflater.flush()
    need(len(output) <= limit, "gzip-bounded-flush:" + label)
    return output


def ledger(raw: bytes, descriptor: dict[str, Any], label: str) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []; hashes: list[str] = []
    inflated = inflate_single(raw, label)
    need(inflated.endswith(b"\n") and not inflated.endswith(b"\n\n"), "ledger-terminal-newline-no-empty-tail:" + label)
    for index, line in enumerate(inflated.splitlines(keepends=True)):
        need(line != b"\n", "ledger-no-empty-line:" + label)
        row = strict_json(line, f"{label}:{index}"); close_row(row, f"{label}:{index}")
        out.append(row); hashes.append(row["row_sha256"])
    need(len(out) == descriptor["row_count"] and seq(hashes) == descriptor["row_hash_line_sequence_sha256"], "descriptor:" + label)
    return out


def authority_snapshot() -> str:
    digest = hashlib.sha256()
    for target in (ROOT / ".cm2-runtime", OUT / "CM2_LATEST_STATUS.md"):
        items = [target] if target.is_file() else [target, *sorted(target.rglob("*"), key=lambda p: str(p.relative_to(ROOT)))]
        for path in items:
            st = os.lstat(path); record = [str(path.relative_to(ROOT)), str(st.st_mode), str(st.st_dev), str(st.st_ino), str(st.st_size), str(st.st_mtime_ns), str(st.st_nlink)]
            if stat.S_ISLNK(st.st_mode): record.append(os.readlink(path))
            digest.update("\0".join(record).encode() + b"\n")
    return digest.hexdigest()


def payload(value: Any) -> dict[str, Any]:
    return {"lower": str(value.lower()), "upper": str(value.upper()), "contains_zero": bool(value.contains(0))}


def exact_keys(value: dict[str, Any], keys: set[str], label: str) -> None:
    need(set(value) == keys, "closed-schema:" + label)


def blocker_codes(kind: str) -> list[str]:
    return {
        "COLLISION1_OUTGOING_STATE": ["EXACT_COLLISION1_OUTGOING_RADIAL_POSITIVITY_EVALUATOR_MISSING", "STRICT_OUTGOING_CHART_MARGIN_EVALUATOR_MISSING", "SECOND_OUTGOING_STATE_NOT_MATERIALIZED"],
        "REGULAR_BOUNDARY_ARRANGEMENT": ["NO_UNIFORM_OPPOSITE_SIGN_FULL_GRAPH_AXIS_FACES", "NO_GLOBAL_GRAPH_AXIS_SELECTED", "OFF_GRAPH_TWO_SLAB_PARTITION_NOT_AVAILABLE"],
        "REGULAR_MULTI_GRAPH_FIRST_TANGENCY": ["TANGENCY_GRAPH_TYPED_BUT_TWO_OFF_GRAPH_SLAB_DISPOSITIONS_MISSING", "MULTI_SURFACE_ORDER_REGISTRY_MISSING"],
        "REGULAR_MULTI_GRAPH_INHERITED_INTERVAL_ORDER_OR_BOUNDARY_UNISOLATED": ["MULTI_SURFACE_FULL_BOX_EXISTENCE_AND_ORDER_REGISTRY_MISSING", "ACTIVE_SET_ORDER_NOT_ISOLATED", "OFF_GRAPH_MULTI_SLAB_INTERSECTION_REGISTRY_MISSING"],
        "SOURCE_GRAZING_ENDPOINT_CHART": ["SOURCE_GRAZING_TRANSFORMED_ENDPOINT_CHART_EVALUATOR_MISSING", "ENDPOINT_GRAPH_AND_OFF_GRAPH_SLAB_PARTITION_MISSING"],
    }[kind]


def fs_fault_self_test(sample: Path) -> dict[str, str]:
    tests: dict[str, str] = {}
    with tempfile.TemporaryDirectory(prefix="c69c-cold-fs-") as name:
        root = Path(name); data = sample.read_bytes(); target = root / "target"; target.write_bytes(data)
        link = root / "symlink"; link.symlink_to(target)
        hard = root / "hardlink"; os.link(target, hard)
        for label, path in (("symlink", link), ("hardlink", hard)):
            try: secure(path)
            except (FailClosed, OSError): tests[label] = "FAIL_CLOSED"
            else: raise FailClosed("fs-attack-escaped:" + label)
        # Deterministic post-read identity drift simulation exercises the same
        # equality predicate used by secure(), without racing live authority.
        a = ident(os.lstat(target)); b = dict(a); b["mtime_ns"] += 1
        try: need(a == b, "simulated-TOCTOU")
        except FailClosed: tests["toctou_identity_drift"] = "FAIL_CLOSED"
        else: raise FailClosed("fs-attack-escaped:toctou")
        member = gzip.compress(b"{}\n", mtime=0)
        for label, attacked, limit in (
            ("gzip_multimember", member + member, 1024),
            ("gzip_trailing", member + b"TRAIL", 1024),
            ("gzip_oversize", gzip.compress(b"X" * 2048, mtime=0), 1024),
            ("gzip_truncated", member[:-3], 1024),
        ):
            try: inflate_single(attacked, label, limit)
            except FailClosed: tests[label] = "FAIL_CLOSED"
            else: raise FailClosed("fs-attack-escaped:" + label)
    return tests


def json_fault_self_test() -> dict[str, str]:
    tests: dict[str, str] = {}
    hostile = {
        "json_BOM": b"\xef\xbb\xbf{\"a\":1}\n", "json_duplicate": b'{"a":1,"a":1}\n',
        "json_NaN": b'{"a":NaN}\n', "json_trailing": b'{"a":1}X\n',
        "json_noncanonical": b'{"a": 1}\n', "json_missing_newline": b'{"a":1}',
        "json_extra_newline": b'{"a":1}\n\n', "json_empty_line": b'\n',
    }
    need(strict_json(b'{"a":1}\n', "hostile-control") == {"a": 1}, "json-control")
    for label, raw in hostile.items():
        try: strict_json(raw, label)
        except (FailClosed, ValueError, UnicodeError): tests[label] = "FAIL_CLOSED"
        else: raise FailClosed("json-attack-escaped:" + label)
    return tests


def validate_semantic_state(state: dict[str, Any]) -> None:
    expected = {
        "descriptor_decisions_sha": PINS["decisions"], "descriptor_decisions_size": 1280359,
        "descriptor_decisions_rows": 2356, "descriptor_blockers_sha": PINS["blockers"],
        "descriptor_blockers_size": 3179863, "descriptor_blockers_rows": 18523,
        "descriptor_covers_sha": PINS["covers"], "descriptor_covers_size": 850, "descriptor_covers_rows": 2,
        "corrected_result_file_sha": PINS["corrected"], "corrected_result_object_sha": PINS["corrected_object"],
        "receipt_file_sha": PINS["receipt"], "receipt_object_sha": PINS["receipt_object"],
        "predecessor_result_file_sha": PINS["c69b_result"], "predecessor_result_object_sha": PINS["c69b_result_object"],
        "partition_domain_count": 20879, "partition_output_count": 20879, "partition_unique_count": 20879,
        "partition_missing_count": 0, "partition_extra_count": 0, "lineage_exact_count": 20879,
        "lineage_all_exact": True, "numeric_replay_count": 2356, "numeric_cert_all_exact": True,
        "decision_disposition_count": 2356, "blocker_disposition_count": 18523,
        "graph_and_slabs_all_complete": True, "half_open_owner_all_unique": True,
        "source_Kraft_all_one": True, "proof_cover_Kraft_one": True, "proof_cover_prefix_free": True,
        "formal_credit": 0, "whole_parent_credit": 0, "D02_gate_credit": 0,
        "runtime_or_canonical_written": False, "authority_pin": FROZEN_AUTHORITY,
        "producer_imported": False, "producer_executed": False, "wrapper_source_read_or_decoded": False,
        "self_policy_scan_pass": True,
        "C69b_contract_file_sha": PINS["c69b_contract"], "C69b_contract_object_sha": C69B_CONTRACT_OBJECT,
        "C69b_producer_sha": C69B_PRODUCER, "C69c_producer_sha": C69C_PRODUCER,
        "C69b_semantic_payload_sha": C69B_SEMANTIC_PAYLOAD,
        "C69b_result_status": "MEASURED_LAYERED_H1_GRAPH_SLAB_CAPABILITY_PROTOTYPE__ZERO_CREDIT",
        "contract_binding_exact": True, "repair_rule_exact": True, "rejection_rule_exact": True,
        "receipt_published_files_exact": True, "receipt_reused_ledgers_exact": True,
    }
    need(set(state) == set(expected), "semantic-state-closed-schema")
    for key, value in expected.items(): need(state[key] == value, "semantic-state:" + key)


def coherent_attacks(state: dict[str, Any]) -> dict[str, Any]:
    validate_semantic_state(state)
    attacks: dict[str, str] = {}
    for key in sorted(state):
        altered = copy.deepcopy(state); value = altered[key]
        altered[key] = (not value if type(value) is bool else value + 1 if type(value) is int else str(value) + "__ATTACK")
        try: validate_semantic_state(altered)
        except FailClosed: attacks[key] = "FAIL_CLOSED"
        else: raise FailClosed("coherent-escaped:" + key)
    need(len(attacks) >= 45, "attack-count")
    return {"attack_count": len(attacks), "attacks": attacks, "status": f"PASS_{len(attacks)}_OF_{len(attacks)}_COHERENT_SEMANTIC_ATTACKS_FAIL_CLOSED"}


def verify() -> tuple[dict[str, Any], dict[str, Any]]:
    authority_before = authority_snapshot()
    self_raw, self_identity = secure(SELF)
    raw: dict[str, bytes] = {}; identities: dict[str, dict[str, int]] = {}
    # Deliberately omit every C69b/C69c producer/wrapper source path.
    for key, path in FILES.items():
        raw[key], identities[key] = secure(path, PINS[key])

    # Self-source policy scan: forbidden source names may occur only in this
    # explanatory policy block, and there is no import/exec/eval/compile call.
    tree = ast.parse(self_raw.decode("utf-8", "strict"), filename=SELF.name)
    calls = {node.func.id for node in ast.walk(tree) if isinstance(node, ast.Call) and isinstance(node.func, ast.Name)}
    need(not ({"exec", "eval", "compile", "runpy"} & calls), "self-no-dynamic-execution")
    imported = {alias.name for node in ast.walk(tree) if isinstance(node, ast.Import) for alias in node.names}
    imported |= {node.module or "" for node in ast.walk(tree) if isinstance(node, ast.ImportFrom)}
    need(not any("round306c69" in name for name in imported), "self-no-C69-import")

    upstream: dict[str, dict[str, Any]] = {}
    for key in ("c69b_contract", "c69b_result", "c69b_receipt", "c68_result", "c61_result", "c58_result", "c40_result", "c39_result", "c38_result"):
        upstream[key] = strict_json(raw[key], key)
    for key in ("c69b_result", "c69b_receipt", "c68_result", "c61_result", "c58_result", "c40_result", "c39_result", "c38_result"):
        close_object(upstream[key], PINS[key + "_object"], key)
    close_object(upstream["c69b_contract"], C69B_CONTRACT_OBJECT, "c69b-contract")

    c68_rows = ledger(raw["c68_tasks"], upstream["c68_result"]["ledgers"]["singleton_structural_tasks"], "C68")
    c61_all = ledger(raw["c61_leaves"], upstream["c61_result"]["ledgers"]["aggregate_leaves"], "C61")
    c61_rows = [row for row in c61_all if row["disposition"] == "COLLISION2_HANDOFF"]
    c58_rows = ledger(raw["c58_leaves"], upstream["c58_result"]["ledgers"]["leaves"], "C58")
    c40_rows = ledger(raw["c40_rows"], upstream["c40_result"]["ledgers"]["routed_leaf_cells"], "C40")
    c39_rows = ledger(raw["c39_rows"], upstream["c39_result"]["ledgers"]["routed_child_pairs"], "C39")
    c38_rows = ledger(raw["c38_rows"], upstream["c38_result"]["ledgers"]["collision1_2_child_pairs"], "C38")
    need(len(c68_rows) == len(c61_rows) == 20879, "partition-domain-20879")
    c61_by_hash = {row["row_sha256"]: row for row in c61_rows}; c58_by_hash = {row["row_sha256"]: row for row in c58_rows}
    c40_by_hash = {row["row_sha256"]: row for row in c40_rows}; c39_by_hash = {row["row_sha256"]: row for row in c39_rows}; c38_by_hash = {row["row_sha256"]: row for row in c38_rows}

    corrected = strict_json(raw["corrected"], "corrected"); contract = strict_json(raw["contract"], "contract")
    rejection = strict_json(raw["rejection"], "rejection"); receipt = strict_json(raw["receipt"], "receipt")
    corrected_object = close_object(corrected, PINS["corrected_object"], "corrected"); contract_object = close_object(contract, PINS["contract_object"], "contract")
    rejection_object = close_object(rejection, PINS["rejection_object"], "rejection"); receipt_object = close_object(receipt, PINS["receipt_object"], "receipt")

    corrected_keys = {"acceptance_layer_census","authority_snapshot_after_sha256","authority_snapshot_before_sha256","contract_file_sha256","contract_object_sha256","decision_axis_census","decision_face_orientation_census","decision_pair_census","decision_pair_source_volume_fraction","global_invariants","input_category_census","input_file_identities","input_file_sha256","input_object_sha256","layer_B_cover_depth_census","ledgers","numeric_environment","object_sha256","predecessor_binding","predecessor_producer_attacks","producer_file_sha256","protocol_self_test","repair_scope","required_next","schema","scope","status","strict_boundary","terminal_rejection_file_sha256","terminal_rejection_object_sha256"}
    contract_keys = {"defect","forbidden_operations","object_sha256","producer_file_sha256","publication_protocol","repair_algorithm","schema","sealed_input_binding","status","strict_boundary","terminal_rejection_rule"}
    rejection_keys = {"accepted_successor_protocol","authority_snapshot_sha256","object_sha256","reason","rejected_tuple","schema","scope","status","strict_boundary","surviving_sealed_ledgers"}
    receipt_keys = {"schema","status","producer_file_sha256","contract_object_sha256","terminal_rejection_object_sha256","corrected_result_object_sha256","C69b_publication_receipt_file_sha256","C69b_publication_receipt_object_sha256","C69b_rejected_result_file_sha256","C69b_rejected_result_object_sha256","reused_sealed_ledgers","published_files","stage_1_file_hash_sequence_sha256","stage_2_file_hash_sequence_sha256","all_stage_bytes_identical","publication_O_EXCL_no_replace","corrected_result_published_last_among_staged_files","publication_receipt_published_after_corrected_result","sealed_ledger_bytes_rewritten","sealed_ledger_numeric_content_recomputed","authority_snapshot_before_sha256","authority_snapshot_after_sha256","runtime_or_canonical_written","formal_credit","whole_parent_credit","D02_gate_credit","object_sha256"}
    exact_keys(corrected, corrected_keys, "corrected"); exact_keys(contract, contract_keys, "contract")
    exact_keys(rejection, rejection_keys, "rejection"); exact_keys(receipt, receipt_keys, "receipt")

    predecessor = {
        "C69b_mathematical_contract_file_sha256": PINS["c69b_contract"],
        "C69b_mathematical_contract_object_sha256": C69B_CONTRACT_OBJECT,
        "C69b_producer_file_sha256": C69B_PRODUCER,
        "C69b_publication_receipt_file_sha256": PINS["c69b_receipt"],
        "C69b_publication_receipt_object_sha256": PINS["c69b_receipt_object"],
        "C69b_result_file_sha256": PINS["c69b_result"], "C69b_result_object_sha256": PINS["c69b_result_object"],
        "C69b_result_status": "MEASURED_LAYERED_H1_GRAPH_SLAB_CAPABILITY_PROTOTYPE__ZERO_CREDIT",
        "C69b_sealed_ledger_file_sha256": {"blockers": PINS["blockers"], "decisions": PINS["decisions"], "parametric_newton_covers": PINS["covers"]},
        "C69b_semantic_payload_sha256": C69B_SEMANTIC_PAYLOAD,
    }
    need(corrected["contract_file_sha256"] == PINS["contract"] and corrected["contract_object_sha256"] == contract_object, "corrected-contract-binding")
    need(corrected["producer_file_sha256"] == contract["producer_file_sha256"] == C69C_PRODUCER, "C69c-producer-pin")
    need(corrected["predecessor_binding"] == predecessor, "corrected-predecessor-binding")
    need(upstream["c69b_result"]["producer_file_sha256"] == C69B_PRODUCER and upstream["c69b_result"]["status"] == predecessor["C69b_result_status"], "C69b-producer-status")
    shared_semantic = ("acceptance_layer_census", "decision_axis_census", "decision_face_orientation_census", "decision_pair_census", "decision_pair_source_volume_fraction", "global_invariants", "input_category_census", "input_file_identities", "input_file_sha256", "input_object_sha256", "layer_B_cover_depth_census", "numeric_environment", "scope")
    need(all(corrected[key] == upstream["c69b_result"][key] for key in shared_semantic), "C69b-semantic-payload-preserved")
    need(corrected["predecessor_producer_attacks"] == upstream["c69b_result"]["producer_attacks"], "C69b-producer-attacks-preserved")

    sealed_files = {name: {"sha256": value["sha256"], "size": value["size"]} for name, value in ACTUAL.items()}
    sealed_binding = {
        "C69b_mathematical_contract_file_sha256": PINS["c69b_contract"], "C69b_mathematical_contract_object_sha256": C69B_CONTRACT_OBJECT,
        "C69b_producer_file_sha256": C69B_PRODUCER, "C69b_publication_receipt_file_sha256": PINS["c69b_receipt"],
        "C69b_publication_receipt_object_sha256": PINS["c69b_receipt_object"], "authority_snapshot_sha256": FROZEN_AUTHORITY,
        "published_ledger_files": sealed_files,
    }
    repair_algorithm = [
        "AUTHENTICATE_C69B_RECEIPT_RESULT_CONTRACT_PRODUCER_AND_AUTHORITY_SNAPSHOT",
        "READ_EACH_ALREADY_SEALED_GZIP_FILE_BY_STABLE_NOFOLLOW_SINGLE_LINK_FD",
        "VERIFY_RECEIPT_BOUND_FINAL_GZIP_SHA256_AND_SIZE",
        "DECOMPRESS_FINAL_GZIP_BYTES_WITHOUT_IMPORTING_OR_EXECUTING_THE_C69B_PRODUCER",
        "RECOMPUTE_EVERY_CANONICAL_JSON_ROW_SELF_HASH",
        "RECOMPUTE_ROW_COUNT_AND_NEWLINE_DELIMITED_ROW_HASH_SEQUENCE_SHA256",
        "REBUILD_DESCRIPTOR_USING_FINAL_GZIP_SHA256_AND_SIZE",
        "PRESERVE_THE_SEALED_LEDGER_BYTES_EXACTLY_AND_WRITE_NO_LEDGER",
    ]
    need(contract["sealed_input_binding"] == sealed_binding and contract["repair_algorithm"] == repair_algorithm, "contract-sealed-binding-repair-rule")
    need(all(contract["forbidden_operations"].values()) and all(contract["publication_protocol"].values()), "contract-forbidden-publication-rules")
    old_descriptors = upstream["c69b_result"]["ledgers"]
    need(contract["terminal_rejection_rule"] == {"disposition": "TERMINAL_REJECTED_NEVER_CONSUME_AS_A_DESCRIPTOR_AUTHORITY", "rejected_descriptor_tuple": old_descriptors, "rejected_result_file_sha256": PINS["c69b_result"], "rejected_result_object_sha256": PINS["c69b_result_object"], "sealed_ledger_bytes_remain_reusable": True}, "contract-terminal-rule")
    need(rejection["accepted_successor_protocol"] == {"contract_object_sha256": contract_object, "producer_file_sha256": C69C_PRODUCER, "required_result_schema": SCHEMA + ".corrected-result"}, "rejection-accepted-successor")
    need(rejection["authority_snapshot_sha256"] == FROZEN_AUTHORITY and rejection["reason"] == "C69B_RESULT_RECORDED_ALL_THREE_GZIP_SHA256_AND_SIZE_FIELDS_BEFORE_GZIP_CLOSE; THE_VALUES_DO_NOT_BIND_THE_FINAL_PUBLISHED_BYTES", "rejection-authority-reason")
    need(rejection["rejected_tuple"] == {"descriptors": old_descriptors, "producer_file_sha256": C69B_PRODUCER, "result_file_sha256": PINS["c69b_result"], "result_object_sha256": PINS["c69b_result_object"]}, "rejection-old-tuple")

    # Actual on-disk descriptor tuple, including rows and row sequence.
    outputs: dict[str, list[dict[str, Any]]] = {}
    for key, result_key in (("decisions", "decisions"), ("blockers", "blockers"), ("covers", "parametric_newton_covers")):
        descriptor = corrected["ledgers"][result_key]; actual = ACTUAL[result_key]
        need({field: descriptor[field] for field in actual} == actual, "corrected-actual-descriptor:" + key)
        need(descriptor["filename"] == FILES[key].name, "corrected-filename:" + key)
        outputs[key] = ledger(raw[key], descriptor, key)
    decisions = outputs["decisions"]; blockers = outputs["blockers"]; covers = outputs["covers"]
    need(len(decisions) == 2356 and len(blockers) == 18523 and len(covers) == 2, "output-counts")

    # Partition and exact lineage rebuild from frozen upstream rows.
    by_source: dict[str, dict[str, Any]] = {}
    for row in itertools.chain(decisions, blockers):
        source_hash = row["C68_structural_task_row_sha256"]
        need(source_hash not in by_source, "partition-duplicate"); by_source[source_hash] = row
    need(set(by_source) == {row["row_sha256"] for row in c68_rows}, "partition-complete")
    structural = Counter(); categories = Counter(); decision_pairs = Counter(); decision_orientation = Counter(); layers = Counter()
    decision_by_c61: dict[str, dict[str, Any]] = {}
    for c68, c61 in zip(c68_rows, c61_rows, strict=True):
        need(c68["C61_aggregate_leaf_row_sha256"] == c61["row_sha256"], "C68-C61-order-lineage")
        observed = by_source[c68["row_sha256"]]; structural[c68["structural_graph_kind"]] += 1
        need(observed["C61_aggregate_leaf_row_sha256"] == c61["row_sha256"] and observed["pair_index"] == c61["pair_index"] and observed["path"] == c61["path"] and observed["parent_volume_fraction"] == c61["parent_volume_fraction"], "output-C61-lineage")
        if c68["structural_graph_kind"] != "REGULAR_FULL_FACE_GRAPH_CELL":
            need(observed in blockers and observed["structural_graph_kind"] == c68["structural_graph_kind"], "blocker-kind")
            need(observed["route_classification"] == c61["route_classification"] and observed["route_witness"] == c61["route_witness"], "blocker-route")
            need(observed["exact_representative_box_object_sha256"] == h(c61["exact_representative_box"]), "blocker-box")
            need(observed["blocker_codes"] == blocker_codes(c68["structural_graph_kind"]), "blocker-codes")
            need(observed["capability_decision_available"] is False and observed["additional_dyadic_source_depth_recommended"] is False, "blocker-fail-closed")
            need(observed["formal_credit"] == observed["whole_parent_credit"] == observed["D02_gate_credit"] == 0, "blocker-zero-credit")
            categories[c68["structural_graph_kind"]] += 1; continue
        need(observed in decisions, "eligible-is-decision"); decision_by_c61[c61["row_sha256"]] = observed
        need(observed["decision"] == "STRICT_UNIQUE_H1_GRAPH_AND_TWO_OFF_GRAPH_SLABS_AVAILABLE" and observed["capability_consumption_ready"] is True, "decision-disposition")
        need(observed["formal_credit"] == observed["whole_parent_credit"] == observed["D02_gate_credit"] == observed["collision2_handoff_credit"] == observed["terminal_disposition_credit"] == 0, "decision-zero-credit")
        need(observed["exact_representative_box"] == c61["exact_representative_box"] and observed["exact_reflected_box"] == c61["exact_reflected_box"], "decision-box")
        c58 = c58_by_hash[c61["source_C58_leaf_row_sha256"]]; c40 = c40_by_hash[c58["C40_source_row_sha256"]]
        c39 = c39_by_hash[c40["c39_source_row_sha256"]]; c38 = c38_by_hash[c40["c38_source_row_sha256"]]
        need(observed["C58_leaf_row_sha256"] == c58["row_sha256"] and observed["C40_source_row_sha256"] == c40["row_sha256"] and observed["C38_source_row_sha256"] == c38["row_sha256"], "decision-upstream-lineage")
        need(c39["c38_child_row_sha256"] == c38["row_sha256"] and c40["c39_source_row_sha256"] == c39["row_sha256"], "C38-C39-C40-lineage")
        need(observed["representative_origin_key"] == c38["representative_origin_key"], "origin-key")
        decision_pairs[str(c61["pair_index"])] += 1; layers[observed["acceptance_layer"]] += 1

    need(dict(sorted(structural.items())) == corrected["input_category_census"], "structural-census")
    need(dict(sorted(decision_pairs.items())) == corrected["decision_pair_census"], "decision-pair-census")

    # Independent 384-bit numerical replay.  Import only the approved R185
    # implementation, never the C69 producer/wrapper.
    sys.path.insert(0, str(OUT))
    import flint  # type: ignore
    import cm2_round185_preconditioned_c1_residual_refinement as r185  # type: ignore
    from cm2_gate3_eight_cell_symmetry_atlas_cert import AtlasBox  # type: ignore
    need(flint.__version__ == "0.9.0" and flint.ctx.prec == 384, "numeric-environment")
    cover_by_source: dict[str, list[dict[str, Any]]] = {}
    for cover in covers: cover_by_source.setdefault(cover["C61_aggregate_leaf_row_sha256"], []).append(cover)
    for row in decisions:
        boxdata = row["exact_representative_box"]
        box = AtlasBox(Q(boxdata["t"][0]), Q(boxdata["t"][1]), Q(boxdata["p"][0]), Q(boxdata["p"][1]), Q(boxdata["s"][0]), Q(boxdata["s"][1]), 0, row["path"])
        full, nx, ny = r185.collision1_h1_ad(row["representative_origin_key"], box, "W[1,0]")
        cert = row["full_box_graph_certificate"]; derivative = full.derivative[1]
        need(payload(derivative) == cert["strict_graph_axis_derivative_bounds"], "numeric-derivative")
        need(payload(nx.value) == cert["normal_component_bounds"]["nx"] and payload(ny.value) == cert["normal_component_bounds"]["ny"], "numeric-normal")
        faces = []
        for pvalue in (box.p0, box.p1):
            face = r185.fixed_axis_box(box, 1, pvalue, ".cold-face"); value, _, _ = r185.collision1_h1_ad(row["representative_origin_key"], face, "W[1,0]"); faces.append(value.value)
        face_payloads = []
        for value in faces:
            current = {"lower": str(value.lower()), "upper": str(value.upper()), "sign": "POSITIVE" if bool(value > 0) else "NEGATIVE" if bool(value < 0) else "UNRESOLVED"}; face_payloads.append(current)
        need(face_payloads[0] == cert["lower_graph_axis_face"] and face_payloads[1] == cert["upper_graph_axis_face"], "numeric-faces")
        need(face_payloads[0]["sign"] != face_payloads[1]["sign"] and face_payloads[0]["sign"] != "UNRESOLVED", "opposite-faces")
        decision_orientation[face_payloads[0]["sign"] + "_TO_" + face_payloads[1]["sign"]] += 1
        midpoint = (box.p0 + box.p1) / 2; middle_box = r185.fixed_axis_box(box, 1, midpoint, ".cold-mid")
        middle, _, _ = r185.collision1_h1_ad(row["representative_origin_key"], middle_box, "W[1,0]")
        image = r185.BASE.arbq(midpoint) - middle.value / derivative
        image_payload = payload(image); self_map = bool(image > r185.BASE.arbq(box.p0)) and bool(image < r185.BASE.arbq(box.p1))
        need(image_payload == cert["midpoint_axis_interval_Newton"]["image"] and self_map is cert["midpoint_axis_interval_Newton"]["strict_interior_self_map"], "numeric-newton")
        signed = r185.corner_signs(r185.collision1_h1_ad, row["representative_origin_key"], box, "W[1,0]")
        need(r185.strict_boundary_bracket(signed) == cert["strict_corner_segment_bracket"], "numeric-corner-bracket")
        source_covers = sorted(cover_by_source.get(row["C61_aggregate_leaf_row_sha256"], []), key=lambda value: value["cover_prefix"])
        if row["acceptance_layer"].startswith("A_"):
            need(self_map and not source_covers and row["proof_cover"]["row_count"] == 0, "layer-A")
        else:
            need(not self_map and len(source_covers) == 2, "layer-B-count")
            need([cover["cover_prefix"] for cover in source_covers] == ["0", "1"] and sum(Q(cover["relative_transverse_Kraft_fraction"]) for cover in source_covers) == 1, "cover-prefix-Kraft")
            need(source_covers[0]["exact_transverse_interval"][0] == box.t0.__str__() and source_covers[-1]["exact_transverse_interval"][1] == box.t1.__str__() and source_covers[0]["exact_transverse_interval"][1] == source_covers[1]["exact_transverse_interval"][0], "cover-exact-partition")
            for cover in source_covers:
                t0, t1 = map(Q, cover["exact_transverse_interval"]); sub = AtlasBox(t0, t1, box.p0, box.p1, box.s0, box.s1, 0, box.path + cover["cover_prefix"])
                subfull, _, _ = r185.collision1_h1_ad(row["representative_origin_key"], sub, "W[1,0]"); submid = (box.p0 + box.p1) / 2
                subbox = r185.fixed_axis_box(sub, 1, submid, ".cold-cover-mid"); subcenter, _, _ = r185.collision1_h1_ad(row["representative_origin_key"], subbox, "W[1,0]")
                subimage = r185.BASE.arbq(submid) - subcenter.value / subfull.derivative[1]
                need(payload(subfull.derivative[1]) == cover["strict_graph_axis_derivative_bounds"] and payload(subimage) == cover["axis_interval_Newton"]["image"], "cover-numeric")
                need(bool(subimage > r185.BASE.arbq(box.p0)) and bool(subimage < r185.BASE.arbq(box.p1)), "cover-self-map")
        need(row["partition_and_Kraft"]["source_path_preserved"] is True and row["partition_and_Kraft"]["normalized_full_dimensional_Kraft_conservation"] == "1", "source-Kraft")
        need(row["typed_graph_carrier"] == {"Lebesgue_2_measure_zero": True, "certified_nonempty": True, "dimension": 1, "predicate": "H1=0", "unique_root_over_every_fixed_transverse_parameter": True}, "typed-graph")
        need(row["root_enclosure_and_theorem"]["kind"] in {"UNIFORM_INTERVAL_NEWTON_IMAGE", "PIECEWISE_UNIFORM_INTERVAL_NEWTON_IMAGES"}, "root-theorem-kind")
        need(row["off_graph_slabs"]["three_strata_pairwise_disjoint"] is True and row["off_graph_slabs"]["three_strata_union_exact_input_box"] is True and row["off_graph_slabs"]["half_open_negative_graph_owner"]["owns_graph"] is True and row["off_graph_slabs"]["half_open_positive_owner"]["owns_graph"] is False, "half-open-slabs")

    need(dict(sorted(decision_orientation.items())) == corrected["decision_face_orientation_census"], "orientation-census")
    need(dict(sorted(layers.items())) == corrected["acceptance_layer_census"], "layer-census")

    # Supersession/rejection/publication protocol closure.
    need(corrected["schema"] == SCHEMA + ".corrected-result" and contract["schema"] == SCHEMA + ".contract" and rejection["schema"] == SCHEMA + ".terminal-rejection" and receipt["schema"] == SCHEMA + ".deterministic-two-stage-publication-receipt", "schemas")
    need(corrected["predecessor_binding"]["C69b_sealed_ledger_file_sha256"] == {"decisions": PINS["decisions"], "blockers": PINS["blockers"], "parametric_newton_covers": PINS["covers"]}, "predecessor-ledger-binding")
    need(receipt["C69b_rejected_result_file_sha256"] == PINS["c69b_result"] and receipt["C69b_rejected_result_object_sha256"] == PINS["c69b_result_object"] and receipt["C69b_publication_receipt_file_sha256"] == PINS["c69b_receipt"] and receipt["C69b_publication_receipt_object_sha256"] == PINS["c69b_receipt_object"], "predecessor-result-receipt-binding")
    need(receipt["contract_object_sha256"] == contract_object and receipt["terminal_rejection_object_sha256"] == rejection_object and receipt["corrected_result_object_sha256"] == corrected_object, "successor-object-binding")
    need(receipt["all_stage_bytes_identical"] is True and receipt["publication_O_EXCL_no_replace"] is True and receipt["corrected_result_published_last_among_staged_files"] is True and receipt["publication_receipt_published_after_corrected_result"] is True, "publication-protocol")
    need(receipt["sealed_ledger_bytes_rewritten"] is False and receipt["sealed_ledger_numeric_content_recomputed"] is False, "ledger-no-rewrite")
    expected_published = {
        f"{PREFIX}_contract.json": {"sha256": PINS["contract"], "size": len(raw["contract"])},
        f"{PREFIX}_corrected_result.json": {"sha256": PINS["corrected"], "size": len(raw["corrected"])},
        f"{PREFIX}_rejection.json": {"sha256": PINS["rejection"], "size": len(raw["rejection"])},
        f"{PREFIX}_report.md": {"sha256": PINS["report"], "size": len(raw["report"])},
    }
    need(receipt["published_files"] == expected_published and receipt["reused_sealed_ledgers"] == corrected["ledgers"], "receipt-published-reused-exact")
    c69b_published = upstream["c69b_receipt"]["published_files"]
    need(c69b_published[FILES["decisions"].name] == {"sha256": PINS["decisions"], "size": len(raw["decisions"])} and c69b_published[FILES["blockers"].name] == {"sha256": PINS["blockers"], "size": len(raw["blockers"])} and c69b_published[FILES["covers"].name] == {"sha256": PINS["covers"], "size": len(raw["covers"])}, "C69b-receipt-final-ledger-binding")
    need(rejection["rejected_tuple"]["descriptors"] != corrected["ledgers"] and rejection["surviving_sealed_ledgers"] == corrected["ledgers"], "terminal-rejection-effective")
    for value in (corrected, contract, rejection, receipt):
        boundary = value["strict_boundary"] if "strict_boundary" in value else value
        need(boundary.get("runtime_or_canonical_written") is False and boundary.get("formal_credit") == 0 and boundary.get("D02_gate_credit") == 0, "zero-credit-boundary")
        if "whole_parent_credit" in boundary: need(boundary["whole_parent_credit"] == 0, "whole-zero")
    need(corrected["authority_snapshot_before_sha256"] == corrected["authority_snapshot_after_sha256"] == FROZEN_AUTHORITY and receipt["authority_snapshot_before_sha256"] == receipt["authority_snapshot_after_sha256"] == FROZEN_AUTHORITY, "producer-authority-stable-exact-pin")
    need(corrected_object.encode() in raw["report"] and PINS["c69b_result_object"].encode() in raw["report"], "report-bindings")
    need(corrected["terminal_rejection_file_sha256"] == PINS["rejection"] and corrected["terminal_rejection_object_sha256"] == rejection_object, "corrected-rejection-binding")

    semantic_state = {
        "descriptor_decisions_sha": PINS["decisions"], "descriptor_decisions_size": 1280359, "descriptor_decisions_rows": 2356,
        "descriptor_blockers_sha": PINS["blockers"], "descriptor_blockers_size": 3179863, "descriptor_blockers_rows": 18523,
        "descriptor_covers_sha": PINS["covers"], "descriptor_covers_size": 850, "descriptor_covers_rows": 2,
        "corrected_result_file_sha": PINS["corrected"], "corrected_result_object_sha": corrected_object,
        "receipt_file_sha": PINS["receipt"], "receipt_object_sha": receipt_object,
        "predecessor_result_file_sha": PINS["c69b_result"], "predecessor_result_object_sha": PINS["c69b_result_object"],
        "partition_domain_count": len(c68_rows), "partition_output_count": len(by_source), "partition_unique_count": len(set(by_source)),
        "partition_missing_count": len(set(row["row_sha256"] for row in c68_rows) - set(by_source)), "partition_extra_count": len(set(by_source) - set(row["row_sha256"] for row in c68_rows)),
        "lineage_exact_count": 20879, "lineage_all_exact": True, "numeric_replay_count": len(decisions), "numeric_cert_all_exact": True,
        "decision_disposition_count": len(decisions), "blocker_disposition_count": len(blockers),
        "graph_and_slabs_all_complete": True, "half_open_owner_all_unique": True, "source_Kraft_all_one": True,
        "proof_cover_Kraft_one": True, "proof_cover_prefix_free": True, "formal_credit": 0, "whole_parent_credit": 0,
        "D02_gate_credit": 0, "runtime_or_canonical_written": False, "authority_pin": FROZEN_AUTHORITY,
        "producer_imported": False, "producer_executed": False, "wrapper_source_read_or_decoded": False, "self_policy_scan_pass": True,
        "C69b_contract_file_sha": PINS["c69b_contract"], "C69b_contract_object_sha": C69B_CONTRACT_OBJECT,
        "C69b_producer_sha": C69B_PRODUCER, "C69c_producer_sha": C69C_PRODUCER,
        "C69b_semantic_payload_sha": C69B_SEMANTIC_PAYLOAD, "C69b_result_status": predecessor["C69b_result_status"],
        "contract_binding_exact": True, "repair_rule_exact": True, "rejection_rule_exact": True,
        "receipt_published_files_exact": True, "receipt_reused_ledgers_exact": True,
    }
    attacks = coherent_attacks(semantic_state); fs_attacks = fs_fault_self_test(FILES["corrected"]); json_attacks = json_fault_self_test()
    authority_after = authority_snapshot(); need(authority_after == authority_before, "verifier-read-only-authority")
    selftest = {"schema": SCHEMA + ".independent-self-test.v1", "status": "PASS_COHERENT_SEMANTIC_FILESYSTEM_AND_HOSTILE_JSON_ATTACKS_FAIL_CLOSED", "coherent_attacks": attacks, "filesystem_attacks": fs_attacks, "json_attacks": json_attacks, "formal_credit": 0, "whole_parent_credit": 0, "D02_gate_credit": 0}
    selftest["object_sha256"] = h(selftest)
    verification = {
        "schema": SCHEMA + ".independent-verification.v1",
        "status": "PASS_COLD_NO_C69_PRODUCER_OR_WRAPPER_IMPORT_EXECUTION_READ_OR_DECODE__EXACT_REBUILD_20879_PARTITION_2356_NUMERIC_DECISIONS_18523_BLOCKERS_2_COVER_ROWS__ZERO_CREDIT",
        "verifier_file_sha256": hashlib.sha256(self_raw).hexdigest(), "corrected_result_object_sha256": corrected_object,
        "contract_object_sha256": contract_object, "terminal_rejection_object_sha256": rejection_object, "publication_receipt_object_sha256": receipt_object,
        "actual_descriptors": ACTUAL, "recomputed_input_category_census": dict(sorted(structural.items())),
        "recomputed_decision_pair_census": dict(sorted(decision_pairs.items())), "recomputed_acceptance_layer_census": dict(sorted(layers.items())),
        "recomputed_face_orientation_census": dict(sorted(decision_orientation.items())), "numeric_environment": {"python_flint_version": flint.__version__, "Arb_precision_bits": flint.ctx.prec},
        "producer_imported": False, "producer_executed": False, "producer_or_wrapper_source_read_or_decoded": False,
        "self_source_policy_scan_pass": True, "authority_snapshot_before_sha256": authority_before, "authority_snapshot_after_sha256": authority_after,
        "frozen_C69c_authority_snapshot_sha256": FROZEN_AUTHORITY,
        "runtime_or_canonical_written": False, "formal_credit": 0, "whole_parent_credit": 0, "D02_gate_credit": 0, "CM2": "NO-GO_FOR_CLAIM",
        "self_test_object_sha256": selftest["object_sha256"],
    }
    verification["object_sha256"] = h(verification)
    need(ident(os.lstat(SELF)) == self_identity, "self-source-post-identity")
    return verification, selftest


def artifact_bytes(verification: dict[str, Any], selftest: dict[str, Any]) -> dict[str, bytes]:
    report = (
        "# C69c cold independent verification\n\n"
        f"Status: `{verification['status']}`\n\n"
        f"Verification object: `{verification['object_sha256']}`\n\n"
        "Independently rebuilt 20,879 partition rows, 2,356 384-bit H1 numeric decisions, "
        "18,523 fail-closed blockers, and two prefix-free/Kraft-one proof-cover rows. "
        "No C69b/C69c producer or wrapper source was imported, executed, read, or decoded. "
        "Formal, whole-parent, and D02 credit remain zero.\n"
    ).encode()
    artifacts = {VERIFY_NAME: enc(verification) + b"\n", SELFTEST_NAME: enc(selftest) + b"\n", REPORT_NAME: report}
    entries = [f"{hashlib.sha256(data).hexdigest()}  deliverables/{name}" for name, data in sorted(artifacts.items())]
    entries.append(f"{verification['verifier_file_sha256']}  deliverables/{SELF.name}")
    external = (
        "contract", "corrected", "rejection", "receipt", "report", "decisions", "blockers", "covers",
        "c68_result", "c68_tasks", "c61_result", "c61_leaves", "c58_result", "c58_leaves",
        "c40_result", "c40_rows", "c39_result", "c39_rows", "c38_result", "c38_rows", "r185",
    )
    for key in external:
        entries.append(f"{PINS[key]}  {FILES[key].relative_to(ROOT)}")
    artifacts[MANIFEST_NAME] = ("\n".join(entries) + "\n").encode()
    return artifacts


def stage(directory: Path, artifacts: dict[str, bytes]) -> dict[str, str]:
    hashes: dict[str, str] = {}
    for name, data in artifacts.items():
        path = directory / name
        fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, "O_NOFOLLOW", 0), 0o664)
        try:
            with os.fdopen(fd, "wb", closefd=False) as stream: stream.write(data); stream.flush(); os.fsync(stream.fileno())
        finally: os.close(fd)
        hashes[name] = hashlib.sha256(data).hexdigest()
    dirfd = os.open(directory, os.O_RDONLY); os.fsync(dirfd); os.close(dirfd)
    return hashes


def manifest_closure(raw: bytes) -> dict[str, str]:
    closure: dict[str, str] = {}
    for line in raw.decode("ascii").splitlines():
        expected, relative = line.split("  ", 1); path = ROOT / relative
        secure(path, expected); closure[relative] = expected
    return closure


def publish(artifacts: dict[str, bytes], verification: dict[str, Any]) -> dict[str, Any]:
    with tempfile.TemporaryDirectory(prefix="c69c-cold-stage1-", dir=OUT) as a, tempfile.TemporaryDirectory(prefix="c69c-cold-stage2-", dir=OUT) as b:
        one = stage(Path(a), artifacts); two = stage(Path(b), artifacts)
        need(one == two, "two-stage-hash-map")
        for name in artifacts: need((Path(a) / name).read_bytes() == (Path(b) / name).read_bytes(), "two-stage-byte-equality:" + name)
        for name in artifacts: need(not (OUT / name).exists(), "no-replace-preflight:" + name)
        for name in (VERIFY_NAME, SELFTEST_NAME, REPORT_NAME, MANIFEST_NAME):
            data = (Path(a) / name).read_bytes(); target = OUT / name
            fd = os.open(target, os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, "O_NOFOLLOW", 0), 0o664)
            try:
                with os.fdopen(fd, "wb", closefd=False) as stream: stream.write(data); stream.flush(); os.fsync(stream.fileno())
            finally: os.close(fd)
        dirfd = os.open(OUT, os.O_RDONLY); os.fsync(dirfd); os.close(dirfd)
    captures: dict[str, Any] = {}
    for name in (VERIFY_NAME, SELFTEST_NAME, REPORT_NAME, MANIFEST_NAME):
        data, identity = secure(OUT / name, hashlib.sha256(artifacts[name]).hexdigest())
        captures[name] = {"sha256": hashlib.sha256(data).hexdigest(), "size": len(data), "identity": identity}
    closure = manifest_closure(artifacts[MANIFEST_NAME])
    need(len(closure) >= 25, "manifest-broad-closure")
    snapshot = authority_snapshot(); need(snapshot == verification["authority_snapshot_after_sha256"], "outer-authority-stable")
    outer = {
        "schema": SCHEMA + ".independent-outer-publication-receipt.v1",
        "status": "PASS_POSTPUBLICATION_READONLY_RECAPTURE__FOUR_ARTIFACTS_AND_BROAD_MANIFEST_CLOSED__O_EXCL_NO_REPLACE__ZERO_CREDIT",
        "published_artifact_captures": captures, "manifest_closed_entry_count": len(closure),
        "manifest_entry_path_sequence_sha256": seq(sorted(closure)),
        "authority_snapshot_before_sha256": verification["authority_snapshot_before_sha256"],
        "authority_snapshot_after_sha256": snapshot, "publication_O_EXCL_no_replace": True,
        "runtime_or_canonical_written": False, "formal_credit": 0, "whole_parent_credit": 0, "D02_gate_credit": 0,
    }
    outer["object_sha256"] = h(outer); outer_bytes = enc(outer) + b"\n"
    with tempfile.TemporaryDirectory(prefix="c69c-cold-outer1-", dir=OUT) as a, tempfile.TemporaryDirectory(prefix="c69c-cold-outer2-", dir=OUT) as b:
        one = stage(Path(a), {OUTER_NAME: outer_bytes}); two = stage(Path(b), {OUTER_NAME: outer_bytes}); need(one == two, "outer-two-stage")
        need(not (OUT / OUTER_NAME).exists(), "outer-no-replace-preflight")
        fd = os.open(OUT / OUTER_NAME, os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, "O_NOFOLLOW", 0), 0o664)
        try:
            with os.fdopen(fd, "wb", closefd=False) as stream: stream.write(outer_bytes); stream.flush(); os.fsync(stream.fileno())
        finally: os.close(fd)
    secure(OUT / OUTER_NAME, hashlib.sha256(outer_bytes).hexdigest())
    return outer


def main() -> int:
    verification, selftest = verify(); first = (enc(verification), enc(selftest)); gc.collect()
    verification2, selftest2 = verify(); need(first == (enc(verification2), enc(selftest2)), "two-full-cold-runs-byte-identical")
    outer = publish(artifact_bytes(verification, selftest), verification)
    print(json.dumps({"status": verification["status"], "object_sha256": verification["object_sha256"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (FailClosed, OSError, ValueError, KeyError, TypeError, IndexError, SyntaxError, ImportError) as error:
        print(f"FAIL_CLOSED:{type(error).__name__}:{error}", file=sys.stderr)
        raise SystemExit(2)
