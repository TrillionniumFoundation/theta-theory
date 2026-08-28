#!/usr/bin/env python3
"""Independent C79g verifier; statically hard-disabled pending C78s final pins.

The verifier does not import, open, read, decode, compile, or execute the C79g
producer (or any upstream producer).  A future complete append-only v2
successor may bind the real C78s 13-member final surface and reconstruct the
1,148-row overlay, all 76,832 successor rows, and all 862 reflection-parent
rows directly from the pinned evidence bytes.  It then performs coherent
in-memory semantic attacks.  At the present static stage the explicit
``UNFILLED_C78S_*`` gate rejects before candidate or input bytes are read and
before the verification output path is inspected or created.  This v1 remains
permanently execution-disabled and must never be pin-filled in place.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import copy
import hashlib
import json
import os
from pathlib import Path
import stat
import sys
from typing import Any, Iterable, Mapping
import zlib


SELF = Path(os.path.abspath(__file__))
ROOT = SELF.parents[1]
OUT = ROOT / "deliverables"
SCHEMA = "cm2.round306c79g.true-global-no-producer-consumer.v1"
BASE = "cm2_round306c79g_true_global_no_producer_consumer_v1"
CONTRACT = OUT / "cm2_round306c79g_true_global_no_producer_consumer_contract_v1.json"
CLOSED_SCHEMA = OUT / "cm2_round306c79g_true_global_no_producer_consumer_schema_v1.json"
CONTRACT_FILE_PIN = "69bcb716b6c85b241d99938ea57d085c1e8ee868ad5f5c95017bb934de007e07"
CONTRACT_OBJECT_PIN = "974f48d607cb573c161eee6aa830cfbc50cf514e2be718b8e5930034e3fa3176"
CLOSED_SCHEMA_FILE_PIN = "5e2fa93785a8bc019118567627ab1c47d120beace56b7d3a0daa2eb91ca79071"
CHECKPOINT_OBJECT_PIN = "b58d68a0234b8a7de0e9147f891d37910476d622b840cfa073aed7ff3b4382ab"

UNIVERSE = 76_832
BASELINE = 75_684
OVERLAY_COUNT = 1_148
LARGE_COUNT = 1_124
SINGLETON_COUNT = 24
PAIR_COUNT = 862
BASELINE_PAIRS = 288
LARGE_PAIRS = 562
SINGLETON_PAIRS = 12
PENDING_D02 = 33_638
TERMINALS = {
    "CONNECTED_TO_KNOWN", "EARLIEST_PREFIX_EXCLUDED",
    "SOURCE_GRAZING_OR_CEMETERY", "TYPED_EVENT_GRAPH",
}
LARGE_MAP = {
    "WHOLE_PUBLIC_CELL_STRICT_EXCLUSION": (
        "EARLIEST_PREFIX_EXCLUDED", "C78L_WHOLE_STRICT_TO_EARLIEST_PREFIX_EXCLUDED"),
    "EXHAUSTIVE_PUBLIC_CELL_TYPED_EVENT_C3_PARTITION": (
        "TYPED_EVENT_GRAPH", "C78L_TYPED_PARTITION_TO_TYPED_EVENT_GRAPH"),
}
SINGLETON_MAP = {
    "STRICT_EXCLUSION_ONLY": (
        "EARLIEST_PREFIX_EXCLUDED", "C78S_STRICT_ONLY_TO_EARLIEST_PREFIX_EXCLUDED"),
    "STRICT_EXCLUSION_PLUS_CEMETERY_TANGENCY": (
        "SOURCE_GRAZING_OR_CEMETERY",
        "C78S_STRICT_PLUS_CEMETERY_TO_SOURCE_GRAZING_OR_CEMETERY"),
}
CLOSURE = {"owner": True, "history": True, "glue": True,
           "two_sides": True, "incidence": True, "prefix_Kraft": True}
ZERO = {"formal_global_closure_credit": 0, "D02_unlock": False,
        "D02_gate_credit": 0, "D02_task_credit": 0,
        "D02_formal_pending_task_count": PENDING_D02, "D02_started": False}
COMPLETED = {"formal_global_closure_credit": 1, "D02_unlock": True,
             "D02_gate_credit": 0, "D02_task_credit": 0,
             "D02_formal_pending_task_count": PENDING_D02, "D02_started": False}

FIXED_PATHS = {
    "C55A_LEAF": OUT / "cm2_round306c55a_four_chart_fundamental_domain_bnb_leaf_ledger_v1.json",
    "C55A_RESULT": OUT / "cm2_round306c55a_four_chart_fundamental_domain_bnb_result_v1.json",
    "C55A_VERIFY": OUT / "cm2_round306c55a_four_chart_fundamental_domain_bnb_independent_verification_v1.json",
    "C55A_MANIFEST": OUT / "cm2_round306c55a_four_chart_fundamental_domain_bnb_manifest_v1.sha256",
    "C55B_CELLS": OUT / "cm2_round306c55b_global_component_adjacency_known_sheet_cell_component_crosswalk_v1.jsonl.gz",
    "C55B_EDGES": OUT / "cm2_round306c55b_global_component_adjacency_known_sheet_component_edges_and_glue_v1.jsonl.gz",
    "C55B_COMPONENTS": OUT / "cm2_round306c55b_global_component_adjacency_known_sheet_ordinary_components_v1.jsonl.gz",
    "C55B_RESULT": OUT / "cm2_round306c55b_global_component_adjacency_known_sheet_result_v1.json",
    "C55B_VERIFY": OUT / "cm2_round306c55b_global_component_adjacency_known_sheet_independent_verification_v1.json",
    "C55B_SELFTEST": OUT / "cm2_round306c55b_global_component_adjacency_known_sheet_independent_self_test_v1.json",
    "C55B_MANIFEST": OUT / "cm2_round306c55b_global_component_adjacency_known_sheet_manifest_v1.sha256",
    "C72G_CONTRACT": OUT / "cm2_round306c72g_no_producer_global_consumer_successor_contract_v1.json",
    "C72G_VERIFY": OUT / "cm2_round306c72g_no_producer_global_consumer_successor_verification_v1.json",
    "C72G_SELFTEST": OUT / "cm2_round306c72g_no_producer_global_consumer_successor_self_test_v1.json",
    "C72G_MANIFEST": OUT / "cm2_round306c72g_no_producer_global_consumer_successor_manifest_v1.sha256",
    "C72G_OUTER": OUT / "cm2_round306c72g_no_producer_global_consumer_successor_outer_receipt_v1.json",
    "C72G_HEAD": ROOT / ".cm2-runtime/cm2-global-authority-heads/predecessor-10fb050d30c92b0f2bdcf85a30d28ff670d8efc0b48104b7f04a63c391967b41.seal",
}
FIXED_PINS = {
    "C55A_LEAF": "e80c012e3260e8f9e68d5858ba5d9dafd94611e2a1c1200d787a20e3842d8db6",
    "C55A_RESULT": "d38f39792fc944b72e70100f9f96f312b5e30e034d5104ce5f848d24378ae5af",
    "C55A_VERIFY": "6e9dfe5c50cfb104cbb8014873f69f79761b22848f50a51033fced651a121772",
    "C55A_MANIFEST": "848c56c5d328cbdf291715d1eaab2611d3af95fb8bf2875beaadcbb9ffca6e0d",
    "C55B_CELLS": "123a742ed553d89fd1026cf65c64879d9a92916492b5b583888c3312551ca2ce",
    "C55B_EDGES": "23ea0b4419f155f62d32b6b73c5a16c6f402884d333c222ff803899a58da29a0",
    "C55B_COMPONENTS": "bebc49f66efb01c0b980ec10258a60d7aead9d4d2006d28bdd169c9a9ae38a04",
    "C55B_RESULT": "6bf9cae7b4b422c5c2121f95828e1508700fe1a5d1b1128598c8617f65032a93",
    "C55B_VERIFY": "42f31f0c158b08651bec97d83d6980f0372353e71cb4f59959f186a329601bae",
    "C55B_SELFTEST": "e2e45f1a26ae73dd5e0aca08d8fa05b5b3f87fc985cf0a55b977c136948c7a15",
    "C55B_MANIFEST": "c5bd6973bd4836c3d72ae6c32961266ea12a281e4821306fbcc69be86acc45be",
    "C72G_CONTRACT": "6de59a039600f75d0b0d5722f9735fb2456f3b25b8a777df3fffef1f27e1749a",
    "C72G_VERIFY": "7e21fcca280d1f860559d9a1a4afdd2f592b717c5844fc4178fabb2e1d8b684f",
    "C72G_SELFTEST": "79935bb45848ff83db595a4b173bd2df12925be09fa4c3be66dabcdd5453b058",
    "C72G_MANIFEST": "fa77aff4fee070710fb9daf3d229182fb9f14f6b3e7a2534bb728ea91f5a51a7",
    "C72G_OUTER": "de70ab6c7c621e768662055f96a552d5cb4aaae123d4dd82b56ceed926fa68ee",
    "C72G_HEAD": "f62483c87df4b6f4a8a2ad8dcf56febbfce9977200ce94a0ad6ce38e736aeeb3",
}
FIXED_OBJECTS = {
    "C55A_LEAF": "7dd4c19cfb2b9f8cd30a4a9a23e30f11734e856cc6cc5a04e9a169c051059d90",
    "C55A_RESULT": "93b732cd65be4453e7b29379d7f70d8c849057d5bcba5489e1f6c4dd705972e3",
    "C55A_VERIFY": "cd6e3915f1dd89d8eef0766b4a806bc8a22244f348162af72fd009b98368d623",
    "C55B_RESULT": "1ce396e9746d3c0364325e8308e94c9dcd4a3bfbba8c17a9c9961915e807cc56",
    "C55B_VERIFY": "350f076a3dcfaa4424bfb27f2730e876d0f6159baa033c7aafbfaded8c870a68",
    "C55B_SELFTEST": "665cb4eea435b367e8c261788c0c6fe30620b2f0f66f6cd618976500ada1ef01",
    "C72G_CONTRACT": "5b2784b7f033ba4dde0a3d7f30af05ba4a71fb64bd6bf9fe34b64c48cc976b51",
    "C72G_VERIFY": "cd259985de0d2c43d5ad030843fc8116204c6f1cbcce1e18eea44137fe62c62d",
    "C72G_SELFTEST": "0ac9d83cc5e08dae3d0aabeddc2bf0fa665af0bc31c382ff20543c31ec64e0c1",
    "C72G_OUTER": "6380e5bf80dc2063bce5632fa73389dd07f4fe175c6c4b54a2661516d712fa92",
    "C72G_HEAD": "cb90ab914c3b6518384669f42d05df33c21a717596190131c6a0f5683934cbfb",
}

C78L_A = ROOT / ".cm2-runtime/c78l-build-a3.9cdedea3"
C78L_B = ROOT / ".cm2-runtime/c78l-build-b3.9cdedea3"
C78L_VERIFY_A = ROOT / ".cm2-runtime/c78l-independent-v1-a3.a384bba4.json"
C78L_VERIFY_B = ROOT / ".cm2-runtime/c78l-independent-v1-b3.a384bba4.json"
C78L_COMPLETION = ROOT / ".cm2-runtime/c78l-completion-a3.a384bba4"
C78L_PREFIX = "cm2_round306c78l_large_component_final_no_producer_consumer_v1"
C78L_NAMES = {
    "lock": "ZERO_CREDIT_STAGED_C78L_FINAL_CONSUMER_ONLY.lock",
    "tasks": C78L_PREFIX + "_task_consumption.jsonl.gz",
    "sides": C78L_PREFIX + "_task_side_occurrences.jsonl.gz",
    "cells": C78L_PREFIX + "_public_cell_rollup.jsonl.gz",
    "pairs": C78L_PREFIX + "_reflection_pair_rollup.jsonl.gz",
    "registry": C78L_PREFIX + "_source_registry.json",
    "result": C78L_PREFIX + "_result.json",
    "report": C78L_PREFIX + "_report.md",
    "manifest": C78L_PREFIX + "_manifest.sha256",
    "outer": C78L_PREFIX + "_outer_receipt.json",
}
C78L_PINS = {
    "lock": "3eaaa094987dce2545148d6e66c7fb241f2e7429b2988547eff064d05b0f8b19",
    "tasks": "e439be9ae8bc56ab00479baab6d23c029bc6274e7fda72d986153e97fed8c6c9",
    "sides": "7b2f7b57e1d7eeab6fbd1075f23e4d837e9521cb3c17a9d5ab6ef82de4dbea52",
    "cells": "a602f62b5c1c54253256887feac37359cdbb408ce2cad6678c853551e4a1c115",
    "pairs": "47b0c22dc66139964b1a93060ecae30b3fe4786ade5d842ca3e193c63becbbfa",
    "registry": "bf7aa990854950430effb0bc8a05c8e77051f25e3eca8b043cef9a91a237a893",
    "result": "0ab8e3dc9c379dbc14a276b05a394ef96e1cbe93392c940edb0cfe4f246cbb1d",
    "report": "42b6041bf25e94faec45dadf5c013d0d83f995a4e1f9c9e39d81e7c74a294be8",
    "manifest": "09c8a466d3906e01ea38d504f4dcb81b812e591ae7d515551674f7232982bd19",
    "outer": "e343c21c4c5ba1273d370e10eca5aba82e34c6b7f05609b7cb3c25878af0d044",
}
C78L_VERIFY_FILE = "22223e2aca6eaa069cfda7ab95da5f31b6adb36773544f9f2034bd01c6d1f0c1"
C78L_VERIFY_OBJECT = "850eba67fb2d343e8b607394469c8d2febf47229b26d86c6894249fd060c1419"
C78L_COMPLETION_NAMES = {
    "receipt": C78L_PREFIX + "_dual_completion_receipt.json",
    "manifest": C78L_PREFIX + "_dual_completion_manifest.sha256",
    "outer": C78L_PREFIX + "_dual_completion_outer_receipt.json",
}
C78L_COMPLETION_PINS = {
    "receipt": "235e876e53f1ee390ce0f89715fe465376de6b82e07ef6258068e26f35b8a3fd",
    "manifest": "c2ff451ad50cbe5f9b226569351e255b441f7ae500b81867c539b12a8656b1ff",
    "outer": "aa6da7b659af57e7eb5f45ea6e88fc67acdb2e6cbc51953e18e01f265a4e70e4",
}
C78L_RESULT_OBJECT = "bfee46ce15d46718326881fce97cbca7ff10df459732a789b314928ca7c62204"
C78L_COMPLETION_OBJECT = "4b627b9e05d4552ce1a5c55c31a2e9dc11e3e5067657691e0b3fdfdf53562cfe"
C78L_COMPLETION_OUTER_OBJECT = "d67abd63ffabefddcb7829cb781dc038a00498686726e54d806db10f3c2fc4a9"

C78S_PREFIX = "cm2_round306c78s_singleton_final_no_producer_consumer_v1"
C78S_NAMES = {
    "lock": "ZERO_CREDIT_CANDIDATE_SINGLETON_FINAL_NO_PRODUCER_CONSUMER_ONLY.lock",
    "children": C78S_PREFIX + "_child_dispositions.jsonl.gz",
    "sources": C78S_PREFIX + "_source_rollups.jsonl.gz",
    "pairs": C78S_PREFIX + "_reflection_pair_rollups.jsonl.gz",
    "cells": C78S_PREFIX + "_singleton_cell_rollups.jsonl.gz",
    "projection": C78S_PREFIX + "_global_enum_projection.jsonl.gz",
    "result": C78S_PREFIX + "_result.json",
    "report": C78S_PREFIX + "_report.md",
    "manifest": C78S_PREFIX + "_manifest.sha256",
    "outer": C78S_PREFIX + "_outer_receipt.json",
}
C78S_FINAL = {
    "build_A_directory": "UNFILLED_C78S_BUILD_A_DIRECTORY",
    "build_B_directory": "UNFILLED_C78S_BUILD_B_DIRECTORY",
    "pins": {key: "UNFILLED_C78S_" + key.upper() + "_FILE_SHA256" for key in C78S_NAMES},
    "result_object_sha256": "UNFILLED_C78S_RESULT_OBJECT_SHA256",
    "verification_A_path": "UNFILLED_C78S_VERIFICATION_A_PATH",
    "verification_A_file_sha256": "UNFILLED_C78S_VERIFICATION_A_FILE_SHA256",
    "verification_A_object_sha256": "UNFILLED_C78S_VERIFICATION_A_OBJECT_SHA256",
    "verification_B_path": "UNFILLED_C78S_VERIFICATION_B_PATH",
    "verification_B_file_sha256": "UNFILLED_C78S_VERIFICATION_B_FILE_SHA256",
    "verification_B_object_sha256": "UNFILLED_C78S_VERIFICATION_B_OBJECT_SHA256",
    "verifier_source_file_sha256": "UNFILLED_C78S_VERIFIER_SOURCE_FILE_SHA256",
    "final_manifest_A_path": "UNFILLED_C78S_FINAL_MANIFEST_A_PATH",
    "final_manifest_B_path": "UNFILLED_C78S_FINAL_MANIFEST_B_PATH",
    "final_manifest_file_sha256": "UNFILLED_C78S_FINAL_MANIFEST_FILE_SHA256",
    "final_outer_A_path": "UNFILLED_C78S_FINAL_OUTER_A_PATH",
    "final_outer_B_path": "UNFILLED_C78S_FINAL_OUTER_B_PATH",
    "final_outer_file_sha256": "UNFILLED_C78S_FINAL_OUTER_FILE_SHA256",
    "final_outer_object_sha256": "UNFILLED_C78S_FINAL_OUTER_OBJECT_SHA256",
}

LOCK = "ZERO_CREDIT_CANDIDATE_C79G_TRUE_GLOBAL_CONSUMER_ONLY.lock"
OVERLAY = BASE + "_overlay_1148.jsonl.gz"
SUCCESSOR = BASE + "_full_successor_76832.jsonl.gz"
PARENTS = BASE + "_reflection_parent_closure_862.jsonl.gz"
REGISTRY = BASE + "_source_registry.json"
RESULT = BASE + "_result.json"
REPORT = BASE + "_report.md"
MANIFEST = BASE + "_candidate_manifest.sha256"
OUTER_RECEIPT = BASE + "_candidate_outer_receipt.json"
MEMBERS = (LOCK, OVERLAY, SUCCESSOR, PARENTS, REGISTRY, RESULT, REPORT, MANIFEST, OUTER_RECEIPT)


class Reject(RuntimeError):
    pass


def need(value: bool, label: str) -> None:
    if type(value) is not bool or not value:
        raise Reject(label)


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=True, allow_nan=False).encode("ascii")


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def digest(value: Any) -> str:
    return sha(canonical(value))


def close_row(body: dict[str, Any]) -> dict[str, Any]:
    need("row_sha256" not in body, "close row")
    return {**body, "row_sha256": digest(body)}


def close_object(body: dict[str, Any]) -> dict[str, Any]:
    need("object_sha256" not in body, "close object")
    return {**body, "object_sha256": digest(body)}


def verify_row(row: Mapping[str, Any], label: str) -> None:
    body = copy.deepcopy(dict(row)); claim = body.pop("row_sha256", None)
    need(isinstance(claim, str) and claim == digest(body), label + ":row closure")


def verify_object(value: Mapping[str, Any], label: str, pin: str | None = None) -> None:
    body = copy.deepcopy(dict(value)); claim = body.pop("object_sha256", None)
    need(isinstance(claim, str) and claim == digest(body), label + ":object closure")
    if pin is not None:
        need(claim == pin, label + ":object pin")


def strict_json(raw: bytes, label: str) -> Any:
    def pairs(items: list[tuple[str, Any]]) -> dict[str, Any]:
        out: dict[str, Any] = {}
        for key, value in items:
            need(key not in out, label + ":duplicate:" + key)
            out[key] = value
        return out
    try:
        return json.loads(raw, object_pairs_hook=pairs,
                          parse_constant=lambda x: (_ for _ in ()).throw(Reject(label + ":" + x)))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise Reject(label + ":strict JSON") from exc


def sentinels(value: Any) -> list[str]:
    if isinstance(value, str):
        return [value] if "UNFILLED_C78S" in value else []
    if isinstance(value, Mapping):
        return [x for child in value.values() for x in sentinels(child)]
    if isinstance(value, (list, tuple)):
        return [x for child in value for x in sentinels(child)]
    return []


def ensure_c78s_filled() -> None:
    missing = sentinels(C78S_FINAL)
    need(not missing, "C79g verifier disabled: UNFILLED_C78S slots=" + str(len(missing)))


def secure_snapshot(path: Path, required_mode: int | None = None) -> tuple[bytes, tuple[int, int]]:
    try:
        before_path = path.lstat()
    except FileNotFoundError as exc:
        raise Reject("missing input:" + str(path)) from exc
    need(stat.S_ISREG(before_path.st_mode) and not path.is_symlink(), "regular input:" + str(path))
    descriptor = os.open(path, os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0))
    try:
        before = os.fstat(descriptor)
        need(stat.S_ISREG(before.st_mode) and before.st_nlink == 1 and
             (before.st_dev, before.st_ino) == (before_path.st_dev, before_path.st_ino),
             "descriptor identity:" + str(path))
        if required_mode is not None:
            need(stat.S_IMODE(before.st_mode) == required_mode,
                 f"required mode {required_mode:o}:" + str(path))
        blocks: list[bytes] = []
        while True:
            block = os.read(descriptor, 1 << 20)
            if not block:
                break
            blocks.append(block)
        after = os.fstat(descriptor)
        need((before.st_dev, before.st_ino, before.st_size, before.st_mtime_ns,
              before.st_ctime_ns, before.st_nlink) ==
             (after.st_dev, after.st_ino, after.st_size, after.st_mtime_ns,
              after.st_ctime_ns, after.st_nlink), "stable descriptor:" + str(path))
    finally:
        os.close(descriptor)
    path_after = path.lstat()
    need((path_after.st_dev, path_after.st_ino, path_after.st_size, path_after.st_mtime_ns,
          path_after.st_ctime_ns, path_after.st_nlink) ==
         (after.st_dev, after.st_ino, after.st_size, after.st_mtime_ns,
          after.st_ctime_ns, after.st_nlink), "stable path:" + str(path))
    return b"".join(blocks), (before.st_dev, before.st_ino)


def secure_unpinned(path: Path, required_mode: int | None = None) -> bytes:
    return secure_snapshot(path, required_mode)[0]


def secure(path: Path, pin: str) -> bytes:
    raw = secure_unpinned(path)
    need(sha(raw) == pin, "file pin:" + str(path))
    return raw


def secure_dir(path: Path, required_mode: int | None = None) -> None:
    info = path.lstat()
    need(stat.S_ISDIR(info.st_mode) and not path.is_symlink(), "secure directory:" + str(path))
    if required_mode is not None:
        need(stat.S_IMODE(info.st_mode) == required_mode,
             f"required directory mode {required_mode:o}:" + str(path))


def rooted(text: str) -> Path:
    candidate = Path(text)
    path = Path(os.path.abspath(str(candidate if candidate.is_absolute() else ROOT / candidate)))
    need(path == ROOT or ROOT in path.parents, "workspace path")
    return path


def gzip_rows(raw: bytes, label: str) -> list[dict[str, Any]]:
    decoder = zlib.decompressobj(16 + zlib.MAX_WBITS)
    try:
        plain = decoder.decompress(raw) + decoder.flush()
    except zlib.error as exc:
        raise Reject(label + ":gzip") from exc
    need(decoder.eof and not decoder.unused_data and not decoder.unconsumed_tail,
         label + ":one complete gzip member")
    need(plain.endswith(b"\n"), label + ":newline")
    rows: list[dict[str, Any]] = []
    for index, line in enumerate(plain.splitlines(), 1):
        need(bool(line), label + ":blank line")
        row = strict_json(line, f"{label}:{index}")
        need(isinstance(row, dict), label + ":object row")
        verify_row(row, f"{label}:{index}")
        rows.append(row)
    return rows


def parse_manifest(raw: bytes, label: str) -> dict[str, str]:
    need(raw.endswith(b"\n"), label + ":newline")
    out: dict[str, str] = {}
    for line in raw.decode("ascii").splitlines():
        parts = line.split("  ", 1)
        need(len(parts) == 2 and len(parts[0]) == 64 and parts[1] not in out, label + ":entry")
        out[parts[1]] = parts[0]
    return out


def one_index(rows: Iterable[dict[str, Any]], key: str, label: str) -> dict[Any, dict[str, Any]]:
    out: dict[Any, dict[str, Any]] = {}
    for row in rows:
        value = row.get(key)
        need(value not in out, label + ":duplicate")
        out[value] = row
    return out


def dual(a: Path, b: Path, names: Mapping[str, str], pins: Mapping[str, str], label: str) -> dict[str, bytes]:
    secure_dir(a); secure_dir(b)
    need(set(names) == set(pins), label + ":keys")
    out: dict[str, bytes] = {}
    for key in sorted(names):
        left = secure(a / names[key], pins[key]); right = secure(b / names[key], pins[key])
        need(left == right, label + ":dual bytes:" + key)
        out[key] = left
    return out


def read_evidence() -> dict[str, Any]:
    contract = strict_json(secure(CONTRACT, CONTRACT_FILE_PIN), "contract")
    verify_object(contract, "contract", CONTRACT_OBJECT_PIN)
    need(contract["effective_checkpoint_object_sha256"] == CHECKPOINT_OBJECT_PIN, "checkpoint")
    strict_json(secure(CLOSED_SCHEMA, CLOSED_SCHEMA_FILE_PIN), "closed schema")

    fixed = {key: secure(FIXED_PATHS[key], FIXED_PINS[key]) for key in sorted(FIXED_PATHS)}
    objects: dict[str, Any] = {}
    for key, pin in FIXED_OBJECTS.items():
        value = strict_json(fixed[key], key)
        verify_object(value, key, pin); objects[key] = value
    need(objects["C55A_RESULT"]["bnb"]["remaining_unresolved_leaf_count"] == OVERLAY_COUNT and
         objects["C55B_RESULT"]["exact_unresolved_partition"]["total_current_unresolved_cell_count"] == OVERLAY_COUNT and
         objects["C72G_VERIFY"]["public_global_census"]["UNRESOLVED_R1648_CONTINUATION"] == OVERLAY_COUNT and
         objects["C72G_VERIFY"]["structural_closure"] == CLOSURE,
         "fixed predecessor semantics")
    # Fully decode and row-close the structure ledgers, not merely their pins.
    c55b_edges = gzip_rows(fixed["C55B_EDGES"], "C55B edges")
    c55b_components = gzip_rows(fixed["C55B_COMPONENTS"], "C55B components")
    need(bool(c55b_edges) and len(c55b_components) == 26, "C55B structural ledgers")

    c78l = dual(C78L_A, C78L_B, C78L_NAMES, C78L_PINS, "C78l")
    lva = secure(C78L_VERIFY_A, C78L_VERIFY_FILE); lvb = secure(C78L_VERIFY_B, C78L_VERIFY_FILE)
    need(lva == lvb, "C78l verification dual bytes")
    lv = strict_json(lva, "C78l verification"); verify_object(lv, "C78l verification", C78L_VERIFY_OBJECT)
    need(lv.get("self_test", {}).get("attack_count") == 52, "C78l attacks")
    for key, name in C78L_COMPLETION_NAMES.items():
        raw = secure(C78L_COMPLETION / name, C78L_COMPLETION_PINS[key])
        if key == "receipt":
            value = strict_json(raw, "C78l completion"); verify_object(value, "C78l completion", C78L_COMPLETION_OBJECT)
        elif key == "outer":
            value = strict_json(raw, "C78l completion outer"); verify_object(value, "C78l completion outer", C78L_COMPLETION_OUTER_OBJECT)
    lresult = strict_json(c78l["result"], "C78l result"); verify_object(lresult, "C78l result", C78L_RESULT_OBJECT)

    c78s_a = rooted(str(C78S_FINAL["build_A_directory"]))
    c78s_b = rooted(str(C78S_FINAL["build_B_directory"]))
    c78s = dual(c78s_a, c78s_b, C78S_NAMES, C78S_FINAL["pins"], "C78s")
    sva = secure(rooted(str(C78S_FINAL["verification_A_path"])), str(C78S_FINAL["verification_A_file_sha256"]))
    svb = secure(rooted(str(C78S_FINAL["verification_B_path"])), str(C78S_FINAL["verification_B_file_sha256"]))
    need(sva == svb, "C78s verification bytes")
    sv = strict_json(sva, "C78s verification")
    verify_object(sv, "C78s verification", str(C78S_FINAL["verification_A_object_sha256"]))
    need(C78S_FINAL["verification_A_object_sha256"] ==
         C78S_FINAL["verification_B_object_sha256"], "C78s verification object pins agree")
    attacks = sv.get("coherent_attacks", {})
    need(sv.get("verifier_file_sha256") == C78S_FINAL["verifier_source_file_sha256"] and
         attacks.get("attack_count") == attacks.get("rejected") and
         isinstance(attacks.get("attack_count"), int) and attacks["attack_count"] >= 100 and
         len(attacks.get("names", [])) == attacks["attack_count"] and
         len(set(attacks["names"])) == attacks["attack_count"], "C78s coherent attacks")
    final_manifest_a = secure(rooted(str(C78S_FINAL["final_manifest_A_path"])),
                              str(C78S_FINAL["final_manifest_file_sha256"]))
    final_manifest_b = secure(rooted(str(C78S_FINAL["final_manifest_B_path"])),
                              str(C78S_FINAL["final_manifest_file_sha256"]))
    final_outer_a = secure(rooted(str(C78S_FINAL["final_outer_A_path"])),
                           str(C78S_FINAL["final_outer_file_sha256"]))
    final_outer_b = secure(rooted(str(C78S_FINAL["final_outer_B_path"])),
                           str(C78S_FINAL["final_outer_file_sha256"]))
    need(rooted(str(C78S_FINAL["verification_A_path"])).parent == c78s_a and
         rooted(str(C78S_FINAL["verification_B_path"])).parent == c78s_b and
         rooted(str(C78S_FINAL["final_manifest_A_path"])).parent == c78s_a and
         rooted(str(C78S_FINAL["final_manifest_B_path"])).parent == c78s_b and
         rooted(str(C78S_FINAL["final_outer_A_path"])).parent == c78s_a and
         rooted(str(C78S_FINAL["final_outer_B_path"])).parent == c78s_b,
         "C78s final members inside isolated stages")
    need(final_manifest_a == final_manifest_b and final_outer_a == final_outer_b,
         "C78s final dual bytes")
    sfinal = strict_json(final_outer_a, "C78s final outer")
    verify_object(sfinal, "C78s final outer", str(C78S_FINAL["final_outer_object_sha256"]))
    need(sfinal.get("all_final_stage_bytes_identical") is True and
         sfinal.get("all_final_members_terminal_byte_replayed_in_both_stages") is True and
         sfinal.get("terminal_byte_replay_member_count_per_stage") == 13,
         "C78s final closure")
    final_manifest = parse_manifest(final_manifest_a, "C78s final manifest")
    for key, name in C78S_NAMES.items():
        need(final_manifest.get(name) == C78S_FINAL["pins"][key],
             "C78s final manifest base:" + key)
    need(final_manifest.get(rooted(str(C78S_FINAL["verification_A_path"])).name) ==
         C78S_FINAL["verification_A_file_sha256"], "C78s final manifest verification")
    sresult = strict_json(c78s["result"], "C78s result")
    verify_object(sresult, "C78s result", str(C78S_FINAL["result_object_sha256"]))
    return {
        "fixed": fixed,
        "objects": objects,
        "c78l": c78l,
        "c78l_cells": gzip_rows(c78l["cells"], "C78l cells"),
        "c78l_pairs": gzip_rows(c78l["pairs"], "C78l pairs"),
        "c78s": c78s,
        "c78s_projection": gzip_rows(c78s["projection"], "C78s projection"),
        "c78s_pairs": gzip_rows(c78s["pairs"], "C78s pairs"),
        "authority_objects": {
            "C78l_verification": lv,
            "C78s_verification": sv,
            "C78s_final_outer": sfinal,
        },
    }


def reconstruct_expected(evidence: dict[str, Any]) -> dict[str, Any]:
    leaf_object = strict_json(evidence["fixed"]["C55A_LEAF"], "C55A leaf ledger")
    verify_object(leaf_object, "C55A leaf ledger", FIXED_OBJECTS["C55A_LEAF"])
    leaves = leaf_object["leaves"]
    need(len(leaves) == UNIVERSE, "leaf count")
    leaf_by_cell: dict[str, dict[str, Any]] = {}
    unresolved: set[str] = set(); baseline: set[str] = set()
    for ordinal, leaf in enumerate(leaves):
        verify_row(leaf, "C55A leaf")
        need(leaf["leaf_ordinal"] == ordinal and leaf["cell_id"] not in leaf_by_cell, "leaf order/identity")
        terminal = leaf["terminal_disposition"]; reason = leaf["unresolved_reason"]
        need((terminal in TERMINALS and reason is None) or
             (terminal is None and isinstance(reason, str) and bool(reason)), "leaf XOR")
        leaf_by_cell[leaf["cell_id"]] = leaf
        (unresolved if terminal is None else baseline).add(leaf["cell_id"])
    need(len(baseline) == BASELINE and len(unresolved) == OVERLAY_COUNT, "baseline/overlay")

    cells = gzip_rows(evidence["fixed"]["C55B_CELLS"], "C55B cells")
    need(len(cells) == 1_724, "C55B cell count")
    c55b = one_index(cells, "cell_id", "C55B cells")
    pairs: dict[int, list[dict[str, Any]]] = defaultdict(list)
    c55b_unresolved: set[str] = set()
    for row in cells:
        need(row["cell_id"] in leaf_by_cell, "C55B identity")
        pairs[row["pair_index"]].append(row)
        if row["current_effective_disposition"] == "UNRESOLVED_R1648_CONTINUATION":
            c55b_unresolved.add(row["cell_id"])
    need(c55b_unresolved == unresolved and len(pairs) == PAIR_COUNT and
         all(len(rows) == 2 for rows in pairs.values()), "C55B unresolved/pairs")
    for rows in pairs.values():
        need(rows[0]["reflection_partner_cell_id"] == rows[1]["cell_id"] and
             rows[1]["reflection_partner_cell_id"] == rows[0]["cell_id"], "reciprocity")

    large = one_index(evidence["c78l_cells"], "cell_id", "large")
    singleton = one_index(evidence["c78s_projection"], "cell_id", "singleton")
    large_pair = one_index(evidence["c78l_pairs"], "pair_index", "large pairs")
    singleton_pair = one_index(evidence["c78s_pairs"], "pair_index", "singleton pairs")
    large_set = set(large); singleton_set = set(singleton)
    need(len(large_set) == LARGE_COUNT and len(singleton_set) == SINGLETON_COUNT and
         not large_set & singleton_set and large_set | singleton_set == unresolved and
         len(large_pair) == LARGE_PAIRS and len(singleton_pair) == SINGLETON_PAIRS,
         "authority overlay partition")

    overlay_rows: list[dict[str, Any]] = []; overlay_by_cell: dict[str, dict[str, Any]] = {}
    for cell_id in sorted(unresolved, key=lambda item: leaf_by_cell[item]["leaf_ordinal"]):
        leaf = leaf_by_cell[cell_id]; structure = c55b[cell_id]
        if cell_id in large:
            authority_row = large[cell_id]; enum = authority_row["public_cell_disposition"]
            need(enum in LARGE_MAP and authority_row["unresolved_count"] == 0 and
                 authority_row["owner_history_glue_two_sides_incidence_closed"] is True and
                 authority_row["prefix_Kraft"]["prefix_free"] is True, "large semantics")
            terminal, rule = LARGE_MAP[enum]; authority = "C78L_VERIFIED_FINAL_SURFACE"
        else:
            authority_row = singleton[cell_id]; enum = authority_row["terminal_enum"]
            need(enum in SINGLETON_MAP and authority_row["global_projection_installed"] is False and
                 authority_row["candidate_is_authority"] is False, "singleton semantics")
            pair = singleton_pair[structure["pair_index"]]
            need(pair["parent_prefix_free"] is True and pair["parent_Kraft"] == "1", "singleton Kraft")
            terminal, rule = SINGLETON_MAP[enum]; authority = "C78S_VERIFIED_FINAL_SURFACE"
        row = close_row({
            "schema": SCHEMA + ".overlay-row", "overlay_ordinal": len(overlay_rows),
            "leaf_ordinal": leaf["leaf_ordinal"], "cell_id": cell_id,
            "C55A_leaf_row_sha256": leaf["row_sha256"],
            "C55B_cell_row_sha256": structure["row_sha256"],
            "pair_index": structure["pair_index"], "component_index": structure["component_index"],
            "component_id": structure["component_id"],
            "reflection_partner_cell_id": structure["reflection_partner_cell_id"],
            "previous_terminal_disposition": None,
            "previous_unresolved_reason": leaf["unresolved_reason"],
            "terminal_authority": authority,
            "terminal_authority_row_sha256": authority_row["row_sha256"],
            "authority_input_enum": enum, "mapping_rule": rule,
            "terminal_disposition": terminal,
            "overlay_sets_disjoint_and_exact": True,
            "installed_atomically_only_by_C79g_completion": True,
            "row_is_individually_creditable": False, "closure": dict(CLOSURE),
        })
        overlay_rows.append(row); overlay_by_cell[cell_id] = row

    successor_rows: list[dict[str, Any]] = []; successor_by_cell: dict[str, dict[str, Any]] = {}
    census: Counter[str] = Counter(); retained = 0
    for leaf in leaves:
        overlay = overlay_by_cell.get(leaf["cell_id"])
        if overlay is None:
            terminal = leaf["terminal_disposition"]
            mode = "C72G_BASELINE_RETAINED"
            authority = "C55A_PREEXISTING_TERMINAL_RETAINED_UNDER_C72G_STRUCTURAL_CLOSURE"
            authority_row_sha = leaf["row_sha256"]
            overlay_sha = None; preserved = True; retained += 1
        else:
            terminal = overlay["terminal_disposition"]
            mode = "C79G_OVERLAY_REPLACEMENT"; authority = overlay["terminal_authority"]
            authority_row_sha = overlay["terminal_authority_row_sha256"]
            overlay_sha = overlay["row_sha256"]; preserved = False
        need(terminal in TERMINALS, "successor terminal")
        row = close_row({
            "schema": SCHEMA + ".full-successor-row", "leaf_ordinal": leaf["leaf_ordinal"],
            "cell_id": leaf["cell_id"], "C55A_leaf_row_sha256": leaf["row_sha256"],
            "origin_key": leaf["origin_key"], "physical_chart": leaf["physical_chart"],
            "exact_box": leaf["exact_box"], "source_cell_row_sha256": leaf["source_cell_row_sha256"],
            "component_ref": leaf["component_ref"], "reflection_pair_ref": leaf["reflection_pair_ref"],
            "previous_terminal_disposition": leaf["terminal_disposition"],
            "previous_unresolved_reason": leaf["unresolved_reason"],
            "successor_terminal_disposition": terminal, "successor_unresolved_reason": None,
            "lineage_mode": mode, "terminal_authority": authority,
            "terminal_authority_row_sha256": authority_row_sha,
            "overlay_row_sha256": overlay_sha,
            "baseline_terminal_preserved_exactly": preserved,
            "candidate_atomic_install_only": True,
        })
        successor_rows.append(row); successor_by_cell[leaf["cell_id"]] = row; census[terminal] += 1
    need(retained == BASELINE and len(successor_rows) == UNIVERSE, "successor counts")

    parent_rows: list[dict[str, Any]] = []; modes: Counter[str] = Counter()
    for pair_index in sorted(pairs):
        structural = pairs[pair_index]
        roles = {leaf_by_cell[row["cell_id"]]["component_ref"]["cell_role"]: row for row in structural}
        need(set(roles) == {"REPRESENTATIVE", "REFLECTED"}, "roles")
        representative = roles["REPRESENTATIVE"]; reflected = roles["REFLECTED"]
        ids = {representative["cell_id"], reflected["cell_id"]}
        if ids <= baseline:
            mode = "C72G_BASELINE_RETAINED"
            authority = "C55A_PREEXISTING_TERMINALS_WITH_C72G_STRUCTURAL_CLOSURE"
            evidence_authority = "C72G"; authority_sha = representative["C42_parent_row_sha256"]
            need(all(row["whole_pair_terminal_after_C53"] is True for row in structural), "baseline pair")
        elif ids <= large_set:
            mode = "C78L_OVERLAY"; authority = "C78L_VERIFIED_FINAL_SURFACE"
            evidence_authority = "C78L"; pair = large_pair[pair_index]; authority_sha = pair["row_sha256"]
            need(pair["prefix_Kraft"]["prefix_free"] is True and pair["unresolved_count"] == 0, "large pair")
        else:
            need(ids <= singleton_set, "no mixed pair")
            mode = "C78S_OVERLAY"; authority = "C78S_VERIFIED_FINAL_SURFACE"
            evidence_authority = "C78S"; pair = singleton_pair[pair_index]; authority_sha = pair["row_sha256"]
            need(pair["parent_prefix_free"] is True and pair["parent_Kraft"] == "1", "singleton pair")
        components = sorted({row["component_index"] for row in structural}); need(len(components) == 1, "component")
        dispositions = Counter(successor_by_cell[cell]["successor_terminal_disposition"] for cell in ids)
        parent_rows.append(close_row({
            "schema": SCHEMA + ".reflection-parent-closure-row",
            "parent_ordinal": len(parent_rows), "pair_index": pair_index,
            "representative_cell_id": representative["cell_id"],
            "reflected_cell_id": reflected["cell_id"],
            "representative_C55B_row_sha256": representative["row_sha256"],
            "reflected_C55B_row_sha256": reflected["row_sha256"],
            "representative_successor_row_sha256": successor_by_cell[representative["cell_id"]]["row_sha256"],
            "reflected_successor_row_sha256": successor_by_cell[reflected["cell_id"]]["row_sha256"],
            "component_indices": components, "parent_lineage_mode": mode,
            "terminal_authority": authority, "parent_authority_row_sha256": authority_sha,
            "terminal_disposition_census": dict(sorted(dispositions.items())),
            "reciprocal_reflection_partner_identity_closed": True,
            "owner_history_glue_two_sides_incidence_closed": True,
            "prefix_Kraft": {"evidence_authority": evidence_authority, "prefix_free": True,
                             "exact_parent_closure": True, "physical_reflection_duplicate_credit": 0},
            "unresolved_count": 0,
        })); modes[mode] += 1
    need(modes == Counter({"C72G_BASELINE_RETAINED": BASELINE_PAIRS,
                           "C78L_OVERLAY": LARGE_PAIRS, "C78S_OVERLAY": SINGLETON_PAIRS}),
         "parent modes")
    return {"overlay": overlay_rows, "successor": successor_rows, "parents": parent_rows,
            "census": {key: census.get(key, 0) for key in sorted(TERMINALS)},
            "modes": dict(sorted(modes.items()))}


def candidate(candidate_dir: Path, peer_candidate_dir: Path) -> dict[str, Any]:
    secure_dir(candidate_dir, 0o555)
    secure_dir(peer_candidate_dir, 0o555)
    need({path.name for path in candidate_dir.iterdir()} == set(MEMBERS),
         "candidate A exact member universe")
    need({path.name for path in peer_candidate_dir.iterdir()} == set(MEMBERS),
         "candidate B exact member universe")
    raw: dict[str, bytes] = {}
    peer_raw: dict[str, bytes] = {}
    for name in MEMBERS:
        left, left_identity = secure_snapshot(candidate_dir / name, 0o444)
        right, right_identity = secure_snapshot(peer_candidate_dir / name, 0o444)
        need(left == right, "dual candidate byte identity:" + name)
        need(left_identity != right_identity, "dual candidate inode separation:" + name)
        raw[name] = left
        peer_raw[name] = right
    manifest = parse_manifest(raw[MANIFEST], "candidate manifest")
    need(set(manifest) == {LOCK, OVERLAY, SUCCESSOR, PARENTS, REGISTRY, RESULT, REPORT},
         "candidate manifest exact universe")
    for name in (LOCK, OVERLAY, SUCCESSOR, PARENTS, REGISTRY, RESULT, REPORT):
        need(manifest.get(name) == sha(raw[name]), "candidate manifest:" + name)
    outer = strict_json(raw[OUTER_RECEIPT], "candidate outer"); verify_object(outer, "candidate outer")
    need(outer["candidate_manifest_file_sha256"] == sha(raw[MANIFEST]) and
         outer["candidate_outer_receipt_published_last"] is True and
         outer["candidate_credit"] == ZERO and outer["canonical_pointer_written"] is False,
         "candidate outer semantics")
    registry = strict_json(raw[REGISTRY], "candidate registry"); verify_object(registry, "candidate registry")
    result = strict_json(raw[RESULT], "candidate result"); verify_object(result, "candidate result")
    need(result["source_registry_object_sha256"] == registry["object_sha256"] and
         outer["candidate_result_object_sha256"] == result["object_sha256"], "object chain")
    for directory in (candidate_dir, peer_candidate_dir):
        base_mtimes = [(directory / name).stat().st_mtime_ns
                       for name in (LOCK, OVERLAY, SUCCESSOR, PARENTS, REGISTRY, RESULT, REPORT)]
        manifest_mtime = (directory / MANIFEST).stat().st_mtime_ns
        outer_mtime = (directory / OUTER_RECEIPT).stat().st_mtime_ns
        need(max(base_mtimes) < manifest_mtime < outer_mtime,
             "candidate publication mtime order and outer-last:" + str(directory))
    # A second secure itemwise read is the verifier's terminal replay of both
    # already-sealed candidate surfaces.
    for name in MEMBERS:
        replay_a, _ = secure_snapshot(candidate_dir / name, 0o444)
        replay_b, _ = secure_snapshot(peer_candidate_dir / name, 0o444)
        need(replay_a == raw[name] and replay_b == peer_raw[name],
             "dual candidate terminal replay:" + name)
    return {"raw": raw, "overlay": gzip_rows(raw[OVERLAY], "candidate overlay"),
            "successor": gzip_rows(raw[SUCCESSOR], "candidate successor"),
            "parents": gzip_rows(raw[PARENTS], "candidate parents"),
            "registry": registry, "result": result, "outer": outer,
            "dual_candidate_build_directories_mode": "0555",
            "dual_candidate_members_mode": "0444",
            "dual_candidate_members_single_link": True,
            "dual_candidate_members_byte_identical": True,
            "dual_candidate_corresponding_inodes_distinct": True}


def compare(candidate_state: dict[str, Any], expected: dict[str, Any]) -> None:
    for key in ("overlay", "successor", "parents"):
        need(candidate_state[key] == expected[key], "independent exact reconstruction:" + key)
    result = candidate_state["result"]
    census = dict(expected["census"]); census["total"] = sum(census.values())
    need(result["exact_overlay_partition"] == {"C78l_large": LARGE_COUNT,
         "C78s_singleton": SINGLETON_COUNT, "total": OVERLAY_COUNT,
         "sets_disjoint": True, "union_equals_C55A_and_C55B_unresolved": True},
         "result overlay")
    need(result["baseline_retention"]["retained_terminal_rows"] == BASELINE and
         result["derived_final_four_class_census"] == census and
         result["derived_final_four_class_census_was_not_hard_coded"] is True and
         result["public_global_unresolved"] == 0 and
         result["reflection_parent_closure"]["authority_partition"] == expected["modes"] and
         result["closure"] == CLOSURE and result["candidate_credit"] == ZERO and
         result["conditional_completion_credit"] == COMPLETED and
         result["canonical_pointer_written"] is False and result["D02_started"] is False and
         result["actual_C3_disposition_count"] == 0 and
         result["conditional_C3_promoted_to_actual_C3"] is False,
         "result semantics")
    registry = candidate_state["registry"]
    need(registry["all_upstream_producer_sources_opened_or_read"] is False and
         registry["all_upstream_producer_sources_imported_compiled_or_executed"] is False and
         registry["C55A_C55B_C72g_new_terminal_authority"] is False and
         registry["candidate_credit"] == ZERO and registry["D02_started"] is False,
         "registry independence/credit")


def set_path(value: dict[str, Any], path: tuple[str, ...], replacement: Any) -> None:
    target: Any = value
    for key in path[:-1]:
        target = target[key]
    target[path[-1]] = replacement


def altered(value: Any) -> Any:
    if type(value) is bool:
        return not value
    if isinstance(value, int):
        return value + 1
    if value is None:
        return "ATTACK"
    if isinstance(value, str):
        replacement = "0" * 64 if len(value) == 64 else value + "__ATTACK"
        return ("1" * 64) if replacement == value else replacement
    if isinstance(value, list):
        return list(reversed(value)) if len(value) > 1 else [*value, "ATTACK"]
    raise Reject("unsupported structural mutation")


def reclose_row(row: dict[str, Any]) -> dict[str, Any]:
    body = copy.deepcopy(row); body.pop("row_sha256", None)
    return close_row(body)


def reclose_object(value: dict[str, Any]) -> dict[str, Any]:
    body = copy.deepcopy(value); body.pop("object_sha256", None)
    return close_object(body)


def attack_model(actual: dict[str, Any], evidence: dict[str, Any]) -> dict[str, Any]:
    return {
        "overlay": actual["overlay"], "successor": actual["successor"],
        "parents": actual["parents"], "result": actual["result"],
        "registry": actual["registry"], "outer": actual["outer"],
        "manifest": parse_manifest(actual["raw"][MANIFEST], "attack manifest"),
        "authority_objects": evidence["authority_objects"],
        "raw_overlay": actual["raw"][OVERLAY],
        "raw_successor": actual["raw"][SUCCESSOR],
        "raw_parents": actual["raw"][PARENTS],
    }


def validate_attack_patch(patch: dict[str, Any], pristine: dict[str, Any],
                          expected: dict[str, Any]) -> None:
    overlay = patch.get("overlay", pristine["overlay"])
    successor = patch.get("successor", pristine["successor"])
    parents = patch.get("parents", pristine["parents"])
    result = patch.get("result", pristine["result"])
    registry = patch.get("registry", pristine["registry"])
    outer = patch.get("outer", pristine["outer"])
    manifest = patch.get("manifest", pristine["manifest"])
    authority_objects = patch.get("authority_objects", pristine["authority_objects"])

    for label, rows in (("overlay", overlay), ("successor", successor), ("parents", parents)):
        for row in rows:
            verify_row(row, "attack:" + label)
    verify_object(result, "attack result")
    verify_object(registry, "attack registry")
    verify_object(outer, "attack outer")
    for label, value in authority_objects.items():
        verify_object(value, "attack authority:" + label)

    # Every mutated structure is fed back through the same independent exact
    # reconstruction and semantic validator used for the real candidate.
    need(overlay == expected["overlay"], "attack overlay reconstruction")
    need(successor == expected["successor"], "attack successor reconstruction")
    need(parents == expected["parents"], "attack parent reconstruction")
    state = {"overlay": overlay, "successor": successor, "parents": parents,
             "result": result, "registry": registry}
    compare(state, expected)
    need(result == pristine["result"], "attack result exactness")
    need(registry == pristine["registry"], "attack registry exactness")
    need(outer == pristine["outer"], "attack outer exactness")
    need(manifest == pristine["manifest"], "attack manifest exactness")
    need(authority_objects == pristine["authority_objects"], "attack authority exactness")

    if "raw_overlay" in patch:
        need(gzip_rows(patch["raw_overlay"], "attacked overlay gzip") == overlay,
             "attacked overlay gzip rows")
    if "raw_successor" in patch:
        need(gzip_rows(patch["raw_successor"], "attacked successor gzip") == successor,
             "attacked successor gzip rows")
    if "raw_parents" in patch:
        need(gzip_rows(patch["raw_parents"], "attacked parent gzip") == parents,
             "attacked parent gzip rows")


def row_mutation(pristine: dict[str, Any], ledger: str, index: int,
                 path: tuple[str, ...], replacement: Any | None = None) -> dict[str, Any]:
    rows = list(pristine[ledger])
    row = copy.deepcopy(rows[index])
    target: Any = row
    for key in path:
        target = target[key]
    set_path(row, path, altered(target) if replacement is None else replacement)
    rows[index] = reclose_row(row)
    return {ledger: rows}


def object_mutation(pristine: dict[str, Any], key: str, path: tuple[str, ...],
                    replacement: Any | None = None) -> dict[str, Any]:
    value = copy.deepcopy(pristine[key])
    target: Any = value
    for item in path:
        target = target[item]
    set_path(value, path, altered(target) if replacement is None else replacement)
    return {key: reclose_object(value)}


def authority_mutation(pristine: dict[str, Any], authority: str,
                       path: tuple[str, ...], replacement: Any | None = None) -> dict[str, Any]:
    values = copy.deepcopy(pristine["authority_objects"])
    value = values[authority]
    target: Any = value
    for item in path:
        target = target[item]
    set_path(value, path, altered(target) if replacement is None else replacement)
    values[authority] = reclose_object(value)
    return {"authority_objects": values}


def make_attack_cases(pristine: dict[str, Any]) -> list[tuple[str, Any]]:
    overlay = pristine["overlay"]; successor = pristine["successor"]; parents = pristine["parents"]
    large_i = next(i for i, row in enumerate(overlay)
                   if row["terminal_authority"] == "C78L_VERIFIED_FINAL_SURFACE")
    singleton_i = next(i for i, row in enumerate(overlay)
                       if row["terminal_authority"] == "C78S_VERIFIED_FINAL_SURFACE")
    baseline_i = next(i for i, row in enumerate(successor)
                      if row["lineage_mode"] == "C72G_BASELINE_RETAINED")
    replacement_i = next(i for i, row in enumerate(successor)
                         if row["lineage_mode"] == "C79G_OVERLAY_REPLACEMENT")
    base_pair_i = next(i for i, row in enumerate(parents)
                       if row["parent_lineage_mode"] == "C72G_BASELINE_RETAINED")
    large_pair_i = next(i for i, row in enumerate(parents)
                        if row["parent_lineage_mode"] == "C78L_OVERLAY")
    singleton_pair_i = next(i for i, row in enumerate(parents)
                            if row["parent_lineage_mode"] == "C78S_OVERLAY")
    cases: list[tuple[str, Any]] = []

    def row_case(name: str, ledger: str, index: int, path: tuple[str, ...],
                 replacement: Any | None = None) -> None:
        cases.append((name, lambda ledger=ledger, index=index, path=path, replacement=replacement:
                      row_mutation(pristine, ledger, index, path, replacement)))

    for name, path in (
        ("overlay:leaf_ordinal_drift", ("leaf_ordinal",)),
        ("overlay:cell_id_drift", ("cell_id",)),
        ("overlay:C55A_row_drift", ("C55A_leaf_row_sha256",)),
        ("overlay:C55B_row_drift", ("C55B_cell_row_sha256",)),
        ("overlay:pair_index_drift", ("pair_index",)),
        ("overlay:component_index_drift", ("component_index",)),
        ("overlay:component_id_drift", ("component_id",)),
        ("overlay:partner_drift", ("reflection_partner_cell_id",)),
        ("overlay:authority_row_drift", ("terminal_authority_row_sha256",)),
        ("overlay:input_enum_drift", ("authority_input_enum",)),
        ("overlay:mapping_rule_drift", ("mapping_rule",)),
        ("overlay:terminal_drift", ("terminal_disposition",)),
        ("overlay:previous_reason_drift", ("previous_unresolved_reason",)),
        ("overlay:individual_credit_inflation", ("row_is_individually_creditable",)),
        ("overlay:installation_erasure", ("installed_atomically_only_by_C79g_completion",)),
        ("overlay:owner_closure_false", ("closure", "owner")),
        ("overlay:history_closure_false", ("closure", "history")),
        ("overlay:prefix_Kraft_false", ("closure", "prefix_Kraft")),
    ):
        row_case(name, "overlay", large_i, path)
    row_case("overlay:large_authority_swapped_to_singleton", "overlay", large_i,
             ("terminal_authority",), "C78S_VERIFIED_FINAL_SURFACE")
    row_case("overlay:singleton_authority_swapped_to_large", "overlay", singleton_i,
             ("terminal_authority",), "C78L_VERIFIED_FINAL_SURFACE")
    row_case("overlay:singleton_strict_plus_cemetery_mapped_typed", "overlay", singleton_i,
             ("terminal_disposition",), "TYPED_EVENT_GRAPH")

    for name, index, path in (
        ("successor:baseline_cell_id_join_erasure", baseline_i, ("cell_id",)),
        ("successor:baseline_C55A_lineage_drift", baseline_i, ("C55A_leaf_row_sha256",)),
        ("successor:baseline_disposition_mutation", baseline_i, ("successor_terminal_disposition",)),
        ("successor:baseline_authority_inflation", baseline_i, ("terminal_authority",)),
        ("successor:baseline_authority_row_drift", baseline_i, ("terminal_authority_row_sha256",)),
        ("successor:baseline_preservation_false", baseline_i, ("baseline_terminal_preserved_exactly",)),
        ("successor:baseline_mode_swap", baseline_i, ("lineage_mode",)),
        ("successor:overlay_cell_id_join_erasure", replacement_i, ("cell_id",)),
        ("successor:overlay_reference_erasure", replacement_i, ("overlay_row_sha256",)),
        ("successor:overlay_authority_row_erasure", replacement_i, ("terminal_authority_row_sha256",)),
        ("successor:overlay_authority_swap", replacement_i, ("terminal_authority",)),
        ("successor:overlay_disposition_mutation", replacement_i, ("successor_terminal_disposition",)),
        ("successor:unresolved_reintroduced", replacement_i, ("successor_unresolved_reason",)),
        ("successor:origin_key_drift", replacement_i, ("origin_key",)),
        ("successor:source_cell_lineage_drift", replacement_i, ("source_cell_row_sha256",)),
        ("successor:atomic_install_erasure", replacement_i, ("candidate_atomic_install_only",)),
    ):
        row_case(name, "successor", index, path)

    for name, index, path in (
        ("parent:pair_index_drift", base_pair_i, ("pair_index",)),
        ("parent:representative_drift", base_pair_i, ("representative_cell_id",)),
        ("parent:reflected_drift", base_pair_i, ("reflected_cell_id",)),
        ("parent:representative_C55B_drift", base_pair_i, ("representative_C55B_row_sha256",)),
        ("parent:reflected_C55B_drift", base_pair_i, ("reflected_C55B_row_sha256",)),
        ("parent:representative_successor_drift", base_pair_i, ("representative_successor_row_sha256",)),
        ("parent:reflected_successor_drift", base_pair_i, ("reflected_successor_row_sha256",)),
        ("parent:component_mixing", base_pair_i, ("component_indices",)),
        ("parent:authority_row_drift", large_pair_i, ("parent_authority_row_sha256",)),
        ("parent:large_authority_swap", large_pair_i, ("terminal_authority",)),
        ("parent:singleton_authority_swap", singleton_pair_i, ("terminal_authority",)),
        ("parent:reciprocity_break", large_pair_i, ("reciprocal_reflection_partner_identity_closed",)),
        ("parent:closure_false", large_pair_i, ("owner_history_glue_two_sides_incidence_closed",)),
        ("parent:prefix_free_false", large_pair_i, ("prefix_Kraft", "prefix_free")),
        ("parent:Kraft_not_exact", large_pair_i, ("prefix_Kraft", "exact_parent_closure")),
        ("parent:duplicate_credit", large_pair_i, ("prefix_Kraft", "physical_reflection_duplicate_credit")),
        ("parent:evidence_authority_swap", singleton_pair_i, ("prefix_Kraft", "evidence_authority")),
        ("parent:unresolved_reintroduced", singleton_pair_i, ("unresolved_count",)),
    ):
        row_case(name, "parents", index, path)

    # Whole-ledger mutations exercise missing/duplicate/order guards after all
    # surviving rows retain valid individual row hashes.
    cases.extend([
        ("overlay:row_missing", lambda: {"overlay": overlay[:-1]}),
        ("overlay:row_duplicate", lambda: {"overlay": [*overlay, overlay[-1]]}),
        ("overlay:row_order_swap", lambda: {"overlay": [overlay[1], overlay[0], *overlay[2:]]}),
        ("successor:row_missing", lambda: {"successor": successor[:-1]}),
        ("successor:row_duplicate", lambda: {"successor": [*successor, successor[-1]]}),
        ("successor:row_order_swap", lambda: {"successor": [successor[1], successor[0], *successor[2:]]}),
        ("parent:row_missing", lambda: {"parents": parents[:-1]}),
        ("parent:row_duplicate", lambda: {"parents": [*parents, parents[-1]]}),
        ("parent:row_order_swap", lambda: {"parents": [parents[1], parents[0], *parents[2:]]}),
    ])

    def object_case(name: str, key: str, path: tuple[str, ...],
                    replacement: Any | None = None) -> None:
        cases.append((name, lambda key=key, path=path, replacement=replacement:
                      object_mutation(pristine, key, path, replacement)))

    for name, key, path in (
        ("result:public_global_unresolved_nonzero", "result", ("public_global_unresolved",)),
        ("result:derived_census_forgery", "result", ("derived_final_four_class_census", "EARLIEST_PREFIX_EXCLUDED")),
        ("result:hardcode_flag_forgery", "result", ("derived_final_four_class_census_was_not_hard_coded",)),
        ("result:baseline_count_drift", "result", ("baseline_retention", "retained_terminal_rows")),
        ("result:overlay_count_drift", "result", ("exact_overlay_partition", "total")),
        ("result:overlay_disjoint_false", "result", ("exact_overlay_partition", "sets_disjoint")),
        ("result:owner_false", "result", ("closure", "owner")),
        ("result:history_false", "result", ("closure", "history")),
        ("result:glue_false", "result", ("closure", "glue")),
        ("result:two_sides_false", "result", ("closure", "two_sides")),
        ("result:incidence_false", "result", ("closure", "incidence")),
        ("result:prefix_Kraft_false", "result", ("closure", "prefix_Kraft")),
        ("credit:candidate_formal_forgery", "result", ("candidate_credit", "formal_global_closure_credit")),
        ("credit:candidate_D02_unlock_forgery", "result", ("candidate_credit", "D02_unlock")),
        ("credit:D02_gate_forgery", "result", ("candidate_credit", "D02_gate_credit")),
        ("credit:D02_task_forgery", "result", ("candidate_credit", "D02_task_credit")),
        ("credit:D02_pending_reduction", "result", ("candidate_credit", "D02_formal_pending_task_count")),
        ("credit:D02_started_forgery", "result", ("D02_started",)),
        ("credit:precursor_C65_forgery", "result", ("precursor_credits", "C65_local_terminal_formal_credit")),
        ("authority:C55A_terminal_inflation", "result", ("authority_separation", "C55A")),
        ("authority:C55B_terminal_inflation", "result", ("authority_separation", "C55B")),
        ("authority:C72g_overlay_inflation", "result", ("authority_separation", "C72g")),
        ("authority:conditional_C3_promoted", "result", ("conditional_C3_promoted_to_actual_C3",)),
        ("authority:actual_C3_inflation", "result", ("actual_C3_disposition_count",)),
        ("publication:canonical_pointer_forgery", "result", ("canonical_pointer_written",)),
        ("registry:producer_opened", "registry", ("all_upstream_producer_sources_opened_or_read",)),
        ("registry:producer_executed", "registry", ("all_upstream_producer_sources_imported_compiled_or_executed",)),
        ("registry:C55_authority_inflation", "registry", ("C55A_C55B_C72g_new_terminal_authority",)),
        ("registry:D02_started", "registry", ("D02_started",)),
        ("publication:outer_not_last", "outer", ("candidate_outer_receipt_published_last",)),
        ("publication:terminal_replay_omission", "outer", ("terminal_byte_replay_required_after_outer_receipt",)),
        ("publication:outer_credit_forgery", "outer", ("candidate_credit", "formal_global_closure_credit")),
        ("publication:outer_manifest_drift", "outer", ("candidate_manifest_file_sha256",)),
    ):
        object_case(name, key, path)

    cases.extend([
        ("publication:manifest_overlay_hash_bitflip", lambda: {
            "manifest": {**pristine["manifest"], OVERLAY: "0" * 64}}),
        ("publication:manifest_successor_missing", lambda: {
            "manifest": {k: v for k, v in pristine["manifest"].items() if k != SUCCESSOR}}),
        ("publication:manifest_parent_hash_bitflip", lambda: {
            "manifest": {**pristine["manifest"], PARENTS: "0" * 64}}),
    ])

    def authority_case(name: str, authority: str, path: tuple[str, ...],
                       replacement: Any | None = None) -> None:
        cases.append((name, lambda authority=authority, path=path, replacement=replacement:
                      authority_mutation(pristine, authority, path, replacement)))

    for name, authority, path in (
        ("C78l:verification_status_forgery", "C78l_verification", ("status",)),
        ("C78l:producer_read_inflation", "C78l_verification",
         ("producer_was_not_opened_read_parsed_imported_executed_or_decoded",)),
        ("C78l:attack_count_reduction", "C78l_verification", ("self_test", "attack_count")),
        ("C78l:global_zero_inflation", "C78l_verification", ("public_global_unresolved_zero",)),
        ("C78s:verifier_source_pin_drift", "C78s_verification", ("verifier_file_sha256",)),
        ("C78s:build_byte_identity_false", "C78s_verification",
         ("candidate_base_bundle", "stage_a_stage_b_bytes_identical")),
        ("C78s:inode_distinctness_false", "C78s_verification",
         ("candidate_base_bundle", "stage_a_stage_b_inodes_distinct")),
        ("C78s:result_file_pin_drift", "C78s_verification",
         ("candidate_base_bundle", "result_file_sha256")),
        ("C78s:result_object_pin_drift", "C78s_verification",
         ("candidate_base_bundle", "result_object_sha256")),
        ("C78s:coherent_attack_count_reduction", "C78s_verification",
         ("coherent_attacks", "attack_count")),
        ("C78s:coherent_attack_rejected_mismatch", "C78s_verification",
         ("coherent_attacks", "rejected")),
        ("C78s:coherent_attack_name_reorder", "C78s_verification",
         ("coherent_attacks", "names")),
        ("C78s:final_verification_pin_drift", "C78s_final_outer", ("verification_file_sha256",)),
        ("C78s:final_verification_object_drift", "C78s_final_outer", ("verification_object_sha256",)),
        ("C78s:final_manifest_pin_drift", "C78s_final_outer", ("final_manifest_file_sha256",)),
        ("C78s:final_bytes_identity_false", "C78s_final_outer", ("all_final_stage_bytes_identical",)),
        ("C78s:final_terminal_replay_false", "C78s_final_outer",
         ("all_final_members_terminal_byte_replayed_in_both_stages",)),
        ("C78s:final_member_count_drift", "C78s_final_outer",
         ("terminal_byte_replay_member_count_per_stage",)),
    ):
        authority_case(name, authority, path)

    # Raw-byte attacks are decoded again by the strict one-member gzip parser.
    cases.extend([
        ("gzip:overlay_concatenated_member", lambda: {
            "raw_overlay": pristine["raw_overlay"] + pristine["raw_overlay"]}),
        ("gzip:successor_truncation", lambda: {
            "raw_successor": pristine["raw_successor"][:-1]}),
        ("gzip:parent_corruption", lambda: {
            "raw_parents": pristine["raw_parents"][:-8] + b"ATTACK!!"}),
    ])
    return cases


def run_attacks(pristine: dict[str, Any], expected: dict[str, Any]) -> dict[str, str]:
    cases = make_attack_cases(pristine)
    names = [name for name, _ in cases]
    need(len(cases) >= 64 and len(set(names)) == len(cases), "64+ unique actual attacks")
    results: dict[str, str] = {}
    for name, create_patch in cases:
        patch = create_patch()
        need(isinstance(patch, dict) and patch, "nonempty actual attack patch:" + name)
        try:
            validate_attack_patch(patch, pristine, expected)
        except Reject:
            results[name] = "FAIL_CLOSED"
        else:
            raise Reject("actual structural attack accepted:" + name)
    return results


def exclusive(path: Path, raw: bytes) -> None:
    descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL |
                         getattr(os, "O_NOFOLLOW", 0), 0o444)
    try:
        view = memoryview(raw)
        while view:
            count = os.write(descriptor, view)
            need(count > 0, "verification write")
            view = view[count:]
        os.fsync(descriptor)
    finally:
        os.close(descriptor)


def verify(candidate_dir: Path, peer_candidate_dir: Path, output: Path) -> None:
    evidence = read_evidence()
    expected = reconstruct_expected(evidence)
    actual = candidate(candidate_dir, peer_candidate_dir)
    compare(actual, expected)
    pristine = attack_model(actual, evidence)
    attacks = run_attacks(pristine, expected)
    member_hashes = {name: sha(actual["raw"][name]) for name in sorted(MEMBERS)}
    census = dict(expected["census"]); census["total"] = sum(census.values())
    verification = close_object({
        "schema": SCHEMA + ".independent-verification",
        "status": "PASS_INDEPENDENT_C79G__1148_EXACT_OVERLAY__76832_SUCCESSOR__862_REFLECTION_PARENTS__PUBLIC_UNRESOLVED_ZERO__CANDIDATE_ZERO_CREDIT",
        # Exact invocation path, O_NOFOLLOW, fd/path identity, and pre/post
        # stability are all enforced by secure_unpinned().
        "verifier_file_sha256": sha(secure_unpinned(SELF)),
        "declared_producer_file_sha256": actual["registry"]["consumer_file_sha256"],
        "producer_hash_is_declarative_binding_only": True,
        "producer_was_not_opened_read_decoded_parsed_compiled_imported_or_executed": True,
        "candidate_member_file_sha256": member_hashes,
        "dual_candidate_build_directories_mode": actual["dual_candidate_build_directories_mode"],
        "dual_candidate_members_mode": actual["dual_candidate_members_mode"],
        "dual_candidate_members_single_link": actual["dual_candidate_members_single_link"],
        "dual_candidate_members_byte_identical": actual["dual_candidate_members_byte_identical"],
        "dual_candidate_corresponding_inodes_distinct":
            actual["dual_candidate_corresponding_inodes_distinct"],
        "reconstruction": {
            "overlay_rows": len(expected["overlay"]),
            "successor_rows": len(expected["successor"]),
            "reflection_parent_rows": len(expected["parents"]),
            "derived_final_four_class_census": census,
            "authority_partition": expected["modes"],
            "public_global_unresolved": 0,
            "closure": dict(CLOSURE),
        },
        "attack_count": len(attacks),
        "attacks": attacks,
        "all_attacks_fail_closed": all(value == "FAIL_CLOSED" for value in attacks.values()),
        "candidate_credit": dict(ZERO),
        "conditional_completion_credit": dict(COMPLETED),
        "precursor_credits_zero": True,
        "canonical_pointer_written": False,
        "D02_started": False,
    })
    need(not output.exists() and output.parent.is_dir(), "fresh verification output")
    exclusive(output, canonical(verification) + b"\n")
    secure_unpinned(output, 0o444)


def main(argv: list[str] | None = None) -> int:
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("--candidate-dir", required=True, type=Path)
    cli.add_argument("--peer-candidate-dir", required=True, type=Path)
    cli.add_argument("--output", required=True, type=Path)
    args = cli.parse_args(argv)
    # Mandatory first operation after argument parsing.  The static verifier
    # must not inspect either candidate directory/output or any immutable input
    # before it.
    ensure_c78s_filled()
    verify(args.candidate_dir, args.peer_candidate_dir, args.output)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Reject as exc:
        print("REJECT:", exc, file=sys.stderr)
        raise SystemExit(2)
