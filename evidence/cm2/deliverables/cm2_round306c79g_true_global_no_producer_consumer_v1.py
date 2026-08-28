#!/usr/bin/env python3
"""C79g true public-global no-producer consumer (statically staged).

This file is intentionally non-executable in the present publication state.
Every path and byte/object pin for the future independently verified C78s
final surface is an explicit ``UNFILLED_C78S_*`` sentinel.  ``main`` rejects
those sentinels before reading any immutable input or creating any output
directory, and the frozen C79g verifier hash is also an explicit
``UNFILLED_C79G_*`` sentinel.  This v1 is permanently frozen and may never be
pin-filled in place; runtime use requires a complete append-only v2 successor.

The append-only successor design independently replays C55A/C55B/C72g, both
byte-identical C78l builds and their verification/completion surface, and the
future corresponding C78s surface.  It derives (never guesses) an exact
1,148-row overlay, a compact 76,832-row successor ledger, and all 862
reflection-parent closure rows.  Candidate builds stay zero-credit.  Formal
global closure credit and the D02 unlock appear only in the final completion
receipt after two isolated byte-identical builds and two byte-identical
independent no-producer verifications have passed.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import copy
import gzip
import hashlib
import io
import json
import os
from pathlib import Path
import stat
import sys
from typing import Any, Iterable, Iterator, Mapping
import zlib


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "deliverables"
SELF = Path(__file__).resolve()
SCHEMA = "cm2.round306c79g.true-global-no-producer-consumer.v1"
BASE = "cm2_round306c79g_true_global_no_producer_consumer_v1"

CONTRACT = OUT / "cm2_round306c79g_true_global_no_producer_consumer_contract_v1.json"
CLOSED_SCHEMA = OUT / "cm2_round306c79g_true_global_no_producer_consumer_schema_v1.json"
CONTRACT_FILE_PIN = "69bcb716b6c85b241d99938ea57d085c1e8ee868ad5f5c95017bb934de007e07"
CONTRACT_OBJECT_PIN = "974f48d607cb573c161eee6aa830cfbc50cf514e2be718b8e5930034e3fa3176"
CLOSED_SCHEMA_FILE_PIN = "5e2fa93785a8bc019118567627ab1c47d120beace56b7d3a0daa2eb91ca79071"
CHECKPOINT_OBJECT_PIN = "b58d68a0234b8a7de0e9147f891d37910476d622b840cfa073aed7ff3b4382ab"

EXPECTED_UNIVERSE = 76_832
EXPECTED_BASELINE = 75_684
EXPECTED_OVERLAY = 1_148
EXPECTED_LARGE = 1_124
EXPECTED_SINGLETON = 24
EXPECTED_C55B_CELLS = 1_724
EXPECTED_PAIRS = 862
EXPECTED_BASELINE_PAIRS = 288
EXPECTED_OVERLAY_PAIRS = 574
EXPECTED_LARGE_PAIRS = 562
EXPECTED_SINGLETON_PAIRS = 12
EXPECTED_PENDING_D02 = 33_638

TERMINALS = {
    "CONNECTED_TO_KNOWN",
    "EARLIEST_PREFIX_EXCLUDED",
    "SOURCE_GRAZING_OR_CEMETERY",
    "TYPED_EVENT_GRAPH",
}
LARGE_MAP = {
    "WHOLE_PUBLIC_CELL_STRICT_EXCLUSION": (
        "EARLIEST_PREFIX_EXCLUDED",
        "C78L_WHOLE_STRICT_TO_EARLIEST_PREFIX_EXCLUDED",
    ),
    "EXHAUSTIVE_PUBLIC_CELL_TYPED_EVENT_C3_PARTITION": (
        "TYPED_EVENT_GRAPH",
        "C78L_TYPED_PARTITION_TO_TYPED_EVENT_GRAPH",
    ),
}
SINGLETON_MAP = {
    "STRICT_EXCLUSION_ONLY": (
        "EARLIEST_PREFIX_EXCLUDED",
        "C78S_STRICT_ONLY_TO_EARLIEST_PREFIX_EXCLUDED",
    ),
    "STRICT_EXCLUSION_PLUS_CEMETERY_TANGENCY": (
        "SOURCE_GRAZING_OR_CEMETERY",
        "C78S_STRICT_PLUS_CEMETERY_TO_SOURCE_GRAZING_OR_CEMETERY",
    ),
}
CLOSURE = {
    "owner": True,
    "history": True,
    "glue": True,
    "two_sides": True,
    "incidence": True,
    "prefix_Kraft": True,
}
ZERO_CANDIDATE_CREDIT = {
    "formal_global_closure_credit": 0,
    "D02_unlock": False,
    "D02_gate_credit": 0,
    "D02_task_credit": 0,
    "D02_formal_pending_task_count": EXPECTED_PENDING_D02,
    "D02_started": False,
}
COMPLETED_CREDIT = {
    "formal_global_closure_credit": 1,
    "D02_unlock": True,
    "D02_gate_credit": 0,
    "D02_task_credit": 0,
    "D02_formal_pending_task_count": EXPECTED_PENDING_D02,
    "D02_started": False,
}

C55A_PATHS = {
    "leaf_ledger": OUT / "cm2_round306c55a_four_chart_fundamental_domain_bnb_leaf_ledger_v1.json",
    "result": OUT / "cm2_round306c55a_four_chart_fundamental_domain_bnb_result_v1.json",
    "verification": OUT / "cm2_round306c55a_four_chart_fundamental_domain_bnb_independent_verification_v1.json",
    "manifest": OUT / "cm2_round306c55a_four_chart_fundamental_domain_bnb_manifest_v1.sha256",
}
C55A_PINS = {
    "leaf_ledger": "e80c012e3260e8f9e68d5858ba5d9dafd94611e2a1c1200d787a20e3842d8db6",
    "result": "d38f39792fc944b72e70100f9f96f312b5e30e034d5104ce5f848d24378ae5af",
    "verification": "6e9dfe5c50cfb104cbb8014873f69f79761b22848f50a51033fced651a121772",
    "manifest": "848c56c5d328cbdf291715d1eaab2611d3af95fb8bf2875beaadcbb9ffca6e0d",
}
C55A_OBJECTS = {
    "leaf_ledger": "7dd4c19cfb2b9f8cd30a4a9a23e30f11734e856cc6cc5a04e9a169c051059d90",
    "result": "93b732cd65be4453e7b29379d7f70d8c849057d5bcba5489e1f6c4dd705972e3",
    "verification": "cd6e3915f1dd89d8eef0766b4a806bc8a22244f348162af72fd009b98368d623",
}

C55B_PATHS = {
    "cells": OUT / "cm2_round306c55b_global_component_adjacency_known_sheet_cell_component_crosswalk_v1.jsonl.gz",
    "edges": OUT / "cm2_round306c55b_global_component_adjacency_known_sheet_component_edges_and_glue_v1.jsonl.gz",
    "components": OUT / "cm2_round306c55b_global_component_adjacency_known_sheet_ordinary_components_v1.jsonl.gz",
    "result": OUT / "cm2_round306c55b_global_component_adjacency_known_sheet_result_v1.json",
    "verification": OUT / "cm2_round306c55b_global_component_adjacency_known_sheet_independent_verification_v1.json",
    "self_test": OUT / "cm2_round306c55b_global_component_adjacency_known_sheet_independent_self_test_v1.json",
    "manifest": OUT / "cm2_round306c55b_global_component_adjacency_known_sheet_manifest_v1.sha256",
}
C55B_PINS = {
    "cells": "123a742ed553d89fd1026cf65c64879d9a92916492b5b583888c3312551ca2ce",
    "edges": "23ea0b4419f155f62d32b6b73c5a16c6f402884d333c222ff803899a58da29a0",
    "components": "bebc49f66efb01c0b980ec10258a60d7aead9d4d2006d28bdd169c9a9ae38a04",
    "result": "6bf9cae7b4b422c5c2121f95828e1508700fe1a5d1b1128598c8617f65032a93",
    "verification": "42f31f0c158b08651bec97d83d6980f0372353e71cb4f59959f186a329601bae",
    "self_test": "e2e45f1a26ae73dd5e0aca08d8fa05b5b3f87fc985cf0a55b977c136948c7a15",
    "manifest": "c5bd6973bd4836c3d72ae6c32961266ea12a281e4821306fbcc69be86acc45be",
}
C55B_OBJECTS = {
    "result": "1ce396e9746d3c0364325e8308e94c9dcd4a3bfbba8c17a9c9961915e807cc56",
    "verification": "350f076a3dcfaa4424bfb27f2730e876d0f6159baa033c7aafbfaded8c870a68",
    "self_test": "665cb4eea435b367e8c261788c0c6fe30620b2f0f66f6cd618976500ada1ef01",
}

C72G_PATHS = {
    "contract": OUT / "cm2_round306c72g_no_producer_global_consumer_successor_contract_v1.json",
    "verification": OUT / "cm2_round306c72g_no_producer_global_consumer_successor_verification_v1.json",
    "self_test": OUT / "cm2_round306c72g_no_producer_global_consumer_successor_self_test_v1.json",
    "manifest": OUT / "cm2_round306c72g_no_producer_global_consumer_successor_manifest_v1.sha256",
    "outer": OUT / "cm2_round306c72g_no_producer_global_consumer_successor_outer_receipt_v1.json",
    "head": ROOT / ".cm2-runtime/cm2-global-authority-heads/predecessor-10fb050d30c92b0f2bdcf85a30d28ff670d8efc0b48104b7f04a63c391967b41.seal",
}
C72G_PINS = {
    "contract": "6de59a039600f75d0b0d5722f9735fb2456f3b25b8a777df3fffef1f27e1749a",
    "verification": "7e21fcca280d1f860559d9a1a4afdd2f592b717c5844fc4178fabb2e1d8b684f",
    "self_test": "79935bb45848ff83db595a4b173bd2df12925be09fa4c3be66dabcdd5453b058",
    "manifest": "fa77aff4fee070710fb9daf3d229182fb9f14f6b3e7a2534bb728ea91f5a51a7",
    "outer": "de70ab6c7c621e768662055f96a552d5cb4aaae123d4dd82b56ceed926fa68ee",
    "head": "f62483c87df4b6f4a8a2ad8dcf56febbfce9977200ce94a0ad6ce38e736aeeb3",
}
C72G_OBJECTS = {
    "contract": "5b2784b7f033ba4dde0a3d7f30af05ba4a71fb64bd6bf9fe34b64c48cc976b51",
    "verification": "cd259985de0d2c43d5ad030843fc8116204c6f1cbcce1e18eea44137fe62c62d",
    "self_test": "0ac9d83cc5e08dae3d0aabeddc2bf0fa665af0bc31c382ff20543c31ec64e0c1",
    "outer": "6380e5bf80dc2063bce5632fa73389dd07f4fe175c6c4b54a2661516d712fa92",
    "head": "cb90ab914c3b6518384669f42d05df33c21a717596190131c6a0f5683934cbfb",
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
C78L_VERIFY_FILE_PIN = "22223e2aca6eaa069cfda7ab95da5f31b6adb36773544f9f2034bd01c6d1f0c1"
C78L_VERIFY_OBJECT_PIN = "850eba67fb2d343e8b607394469c8d2febf47229b26d86c6894249fd060c1419"
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
C78L_RESULT_OBJECT_PIN = "bfee46ce15d46718326881fce97cbca7ff10df459732a789b314928ca7c62204"
C78L_COMPLETION_OBJECT_PIN = "4b627b9e05d4552ce1a5c55c31a2e9dc11e3e5067657691e0b3fdfdf53562cfe"
C78L_COMPLETION_OUTER_OBJECT_PIN = "d67abd63ffabefddcb7829cb781dc038a00498686726e54d806db10f3c2fc4a9"

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
# Deliberate hard-disable sentinels.  Do not replace from the current skeleton
# or from either unsealed c78s-build-a.v1 / c78s-build-b.v1 directory.
C78S_FINAL = {
    "build_A_directory": "UNFILLED_C78S_BUILD_A_DIRECTORY",
    "build_B_directory": "UNFILLED_C78S_BUILD_B_DIRECTORY",
    "pins": {
        "lock": "UNFILLED_C78S_LOCK_FILE_SHA256",
        "children": "UNFILLED_C78S_CHILD_DISPOSITIONS_FILE_SHA256",
        "sources": "UNFILLED_C78S_SOURCE_ROLLUPS_FILE_SHA256",
        "pairs": "UNFILLED_C78S_REFLECTION_PAIR_ROLLUPS_FILE_SHA256",
        "cells": "UNFILLED_C78S_SINGLETON_CELL_ROLLUPS_FILE_SHA256",
        "projection": "UNFILLED_C78S_GLOBAL_ENUM_PROJECTION_FILE_SHA256",
        "result": "UNFILLED_C78S_RESULT_FILE_SHA256",
        "report": "UNFILLED_C78S_REPORT_FILE_SHA256",
        "manifest": "UNFILLED_C78S_MANIFEST_FILE_SHA256",
        "outer": "UNFILLED_C78S_OUTER_RECEIPT_FILE_SHA256",
    },
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
    "closure_receipt_is_final_outer": True,
    "final_stage_member_count_per_build": 13,
    "extra_completion_receipt_exists": False,
}
C79_FROZEN_VERIFIER_FILE_PIN = "UNFILLED_C79G_FROZEN_VERIFIER_SOURCE_FILE_SHA256"

LOCK = "ZERO_CREDIT_CANDIDATE_C79G_TRUE_GLOBAL_CONSUMER_ONLY.lock"
OVERLAY = BASE + "_overlay_1148.jsonl.gz"
SUCCESSOR = BASE + "_full_successor_76832.jsonl.gz"
PARENTS = BASE + "_reflection_parent_closure_862.jsonl.gz"
REGISTRY = BASE + "_source_registry.json"
RESULT = BASE + "_result.json"
REPORT = BASE + "_report.md"
CANDIDATE_MANIFEST = BASE + "_candidate_manifest.sha256"
CANDIDATE_OUTER = BASE + "_candidate_outer_receipt.json"
CANDIDATE_MEMBERS = (
    LOCK, OVERLAY, SUCCESSOR, PARENTS, REGISTRY, RESULT, REPORT,
    CANDIDATE_MANIFEST, CANDIDATE_OUTER,
)
FINAL_VERIFY = BASE + "_independent_verification.json"
FINAL_RECEIPT = BASE + "_dual_completion_receipt.json"
GLOBAL_MANIFEST = BASE + "_global_manifest.sha256"
GLOBAL_OUTER = BASE + "_global_outer_receipt.json"


class Reject(RuntimeError):
    pass


def need(condition: bool, label: str) -> None:
    if type(condition) is not bool or not condition:
        raise Reject(label)


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=True, allow_nan=False).encode("ascii")


def sha_bytes(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def sha_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def digest(value: Any) -> str:
    return sha_bytes(canonical(value))


def close_row(body: dict[str, Any]) -> dict[str, Any]:
    need("row_sha256" not in body, "row already closed")
    return {**body, "row_sha256": digest(body)}


def close_object(body: dict[str, Any]) -> dict[str, Any]:
    need("object_sha256" not in body, "object already closed")
    return {**body, "object_sha256": digest(body)}


def verify_row(row: Mapping[str, Any], label: str) -> None:
    body = copy.deepcopy(dict(row))
    claim = body.pop("row_sha256", None)
    need(isinstance(claim, str) and claim == digest(body), label + ":row closure")


def verify_object(value: Mapping[str, Any], label: str, pin: str | None = None) -> None:
    body = copy.deepcopy(dict(value))
    claim = body.pop("object_sha256", None)
    need(isinstance(claim, str) and claim == digest(body), label + ":object closure")
    if pin is not None:
        need(claim == pin, label + ":object pin")


def strict_json(raw: bytes, label: str) -> Any:
    def pairs(items: list[tuple[str, Any]]) -> dict[str, Any]:
        out: dict[str, Any] = {}
        for key, value in items:
            need(key not in out, label + ":duplicate key:" + key)
            out[key] = value
        return out
    try:
        return json.loads(
            raw,
            object_pairs_hook=pairs,
            parse_constant=lambda token: (_ for _ in ()).throw(Reject(label + ":" + token)),
        )
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise Reject(label + ":strict JSON") from exc


def _sentinels(value: Any) -> list[str]:
    if isinstance(value, str):
        return [value] if ("UNFILLED_C78S" in value or "UNFILLED_C79G" in value) else []
    if isinstance(value, Mapping):
        return [item for child in value.values() for item in _sentinels(child)]
    if isinstance(value, (list, tuple)):
        return [item for child in value for item in _sentinels(child)]
    return []


def ensure_final_pins_filled() -> None:
    missing = _sentinels({"C78s": C78S_FINAL, "C79g_verifier": C79_FROZEN_VERIFIER_FILE_PIN})
    need(not missing,
         "C79g execution disabled: explicit final-surface/frozen-verifier slots=" + str(len(missing)))


def secure_snapshot(path: Path, required_mode: int | None = None) -> tuple[bytes, tuple[int, int]]:
    try:
        before_path = path.lstat()
    except FileNotFoundError as exc:
        raise Reject("missing input:" + str(path)) from exc
    need(stat.S_ISREG(before_path.st_mode) and not path.is_symlink(),
         "regular non-symlink input:" + str(path))
    flags = os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0)
    descriptor = os.open(path, flags)
    try:
        before_fd = os.fstat(descriptor)
        need(stat.S_ISREG(before_fd.st_mode) and before_fd.st_nlink == 1,
             "regular single-link descriptor:" + str(path))
        if required_mode is not None:
            need(stat.S_IMODE(before_fd.st_mode) == required_mode,
                 f"required mode {required_mode:o}:" + str(path))
        need((before_path.st_dev, before_path.st_ino) == (before_fd.st_dev, before_fd.st_ino),
             "path/descriptor identity before read:" + str(path))
        blocks: list[bytes] = []
        while True:
            block = os.read(descriptor, 1 << 20)
            if not block:
                break
            blocks.append(block)
        after_fd = os.fstat(descriptor)
        need((before_fd.st_dev, before_fd.st_ino, before_fd.st_size, before_fd.st_mtime_ns,
              before_fd.st_ctime_ns, before_fd.st_nlink) ==
             (after_fd.st_dev, after_fd.st_ino, after_fd.st_size, after_fd.st_mtime_ns,
              after_fd.st_ctime_ns, after_fd.st_nlink),
             "descriptor stable during read:" + str(path))
    finally:
        os.close(descriptor)
    after_path = path.lstat()
    need((after_path.st_dev, after_path.st_ino, after_path.st_size, after_path.st_mtime_ns,
          after_path.st_ctime_ns, after_path.st_nlink) ==
         (before_fd.st_dev, before_fd.st_ino, before_fd.st_size, before_fd.st_mtime_ns,
          before_fd.st_ctime_ns, before_fd.st_nlink),
         "path identity after read:" + str(path))
    return b"".join(blocks), (before_fd.st_dev, before_fd.st_ino)


def secure_unpinned(path: Path, required_mode: int | None = None) -> bytes:
    return secure_snapshot(path, required_mode)[0]


def secure_file(path: Path, expected_sha256: str) -> bytes:
    raw = secure_unpinned(path)
    need(sha_bytes(raw) == expected_sha256, "file pin:" + str(path))
    return raw


def secure_directory(path: Path, required_mode: int | None = None) -> None:
    info = path.lstat()
    need(stat.S_ISDIR(info.st_mode) and not path.is_symlink(), "secure directory:" + str(path))
    if required_mode is not None:
        need(stat.S_IMODE(info.st_mode) == required_mode,
             f"required directory mode {required_mode:o}:" + str(path))


def rooted(relative: str) -> Path:
    candidate = Path(relative)
    path = Path(os.path.abspath(str(candidate if candidate.is_absolute() else ROOT / candidate)))
    need(path == ROOT or ROOT in path.parents, "path escapes workspace")
    return path


def gzip_rows(raw: bytes, label: str) -> list[dict[str, Any]]:
    decoder = zlib.decompressobj(16 + zlib.MAX_WBITS)
    try:
        plain = decoder.decompress(raw) + decoder.flush()
    except zlib.error as exc:
        raise Reject(label + ":gzip decode") from exc
    need(decoder.eof and not decoder.unused_data and not decoder.unconsumed_tail,
         label + ":exactly one complete gzip member")
    need(plain.endswith(b"\n"), label + ":terminal newline")
    rows: list[dict[str, Any]] = []
    for ordinal, line in enumerate(plain.splitlines(), 1):
        need(bool(line), label + ":blank line")
        value = strict_json(line, f"{label}:{ordinal}")
        need(isinstance(value, dict), label + ":row object")
        verify_row(value, f"{label}:{ordinal}")
        rows.append(value)
    return rows


def gzip_encode(rows: Iterable[Mapping[str, Any]]) -> tuple[bytes, dict[str, Any]]:
    line_hashes: list[str] = []
    plain = bytearray()
    count = 0
    for row in rows:
        verify_row(row, "output")
        line = canonical(dict(row))
        plain.extend(line + b"\n")
        line_hashes.append(sha_bytes(line))
        count += 1
    sink = io.BytesIO()
    with gzip.GzipFile(filename="", mode="wb", fileobj=sink, mtime=0) as stream:
        stream.write(bytes(plain))
    raw = sink.getvalue()
    return raw, {
        "row_count": count,
        "file_sha256": sha_bytes(raw),
        "uncompressed_sha256": sha_bytes(bytes(plain)),
        "row_hash_line_sequence_sha256": digest(line_hashes),
        "single_gzip_member": True,
    }


def exclusive(path: Path, raw: bytes) -> None:
    flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, "O_NOFOLLOW", 0)
    descriptor = os.open(path, flags, 0o444)
    try:
        view = memoryview(raw)
        while view:
            written = os.write(descriptor, view)
            need(written > 0, "write progress:" + path.name)
            view = view[written:]
        os.fsync(descriptor)
    finally:
        os.close(descriptor)


def read_pinned(paths: Mapping[str, Path], pins: Mapping[str, str]) -> dict[str, bytes]:
    need(set(paths) == set(pins), "path/pin key equality")
    return {key: secure_file(paths[key], pins[key]) for key in sorted(paths)}


def read_dual(directory_a: Path, directory_b: Path,
              names: Mapping[str, str], pins: Mapping[str, str], label: str) -> dict[str, bytes]:
    secure_directory(directory_a)
    secure_directory(directory_b)
    need(set(names) == set(pins), label + ":name/pin keys")
    out: dict[str, bytes] = {}
    for key in sorted(names):
        left = secure_file(directory_a / names[key], pins[key])
        right = secure_file(directory_b / names[key], pins[key])
        need(left == right, label + ":dual byte identity:" + key)
        out[key] = left
    return out


def parse_manifest_ordered(raw: bytes, label: str) -> list[dict[str, str]]:
    need(raw.endswith(b"\n"), label + ":newline")
    out: list[dict[str, str]] = []
    seen: set[str] = set()
    for line in raw.decode("ascii").splitlines():
        parts = line.split("  ", 1)
        need(len(parts) == 2 and len(parts[0]) == 64, label + ":entry")
        need(parts[1] not in seen, label + ":duplicate filename")
        seen.add(parts[1])
        out.append({"file_sha256": parts[0], "entry_name": parts[1]})
    return out


def parse_manifest(raw: bytes, label: str) -> dict[str, str]:
    return {entry["entry_name"]: entry["file_sha256"]
            for entry in parse_manifest_ordered(raw, label)}


def one_index(rows: Iterable[dict[str, Any]], key: str, label: str) -> dict[Any, dict[str, Any]]:
    out: dict[Any, dict[str, Any]] = {}
    for row in rows:
        value = row.get(key)
        need(value not in out, label + ":duplicate:" + str(value))
        out[value] = row
    return out


def validate_static_authorities() -> dict[str, Any]:
    contract_raw = secure_file(CONTRACT, CONTRACT_FILE_PIN)
    schema_raw = secure_file(CLOSED_SCHEMA, CLOSED_SCHEMA_FILE_PIN)
    contract = strict_json(contract_raw, "C79g contract")
    verify_object(contract, "C79g contract", CONTRACT_OBJECT_PIN)
    need(contract["effective_checkpoint_object_sha256"] == CHECKPOINT_OBJECT_PIN,
         "contract checkpoint")
    closed = strict_json(schema_raw, "C79g closed schemas")
    need(closed.get("execution_enabled") is False and
         closed.get("C78S_pin_state") == "EXPLICITLY_UNFILLED",
         "static schema declaration remains auditable after pin fill")

    c55a_raw = read_pinned(C55A_PATHS, C55A_PINS)
    c55a = {key: strict_json(c55a_raw[key], "C55A:" + key)
            for key in ("leaf_ledger", "result", "verification")}
    for key in c55a:
        verify_object(c55a[key], "C55A:" + key, C55A_OBJECTS[key])
    need(c55a["result"].get("bnb", {}).get("unresolved_zero") is False and
         c55a["result"].get("bnb", {}).get("remaining_unresolved_leaf_count") == EXPECTED_OVERLAY and
         c55a["leaf_ledger"].get("census", {}).get("UNRESOLVED_R1648_CONTINUATION") == EXPECTED_OVERLAY,
         "C55A predecessor unresolved census")

    c55b_raw = read_pinned(C55B_PATHS, C55B_PINS)
    c55b_objects = {key: strict_json(c55b_raw[key], "C55B:" + key)
                    for key in ("result", "verification", "self_test")}
    for key in c55b_objects:
        verify_object(c55b_objects[key], "C55B:" + key, C55B_OBJECTS[key])
    need(c55b_objects["result"].get("global_closure_proved") is False and
         c55b_objects["result"].get("unresolved_zero") is False,
         "C55B structure-only boundary")
    need(c55b_objects["self_test"].get("status", "").startswith("PASS_16_OF_16"),
         "C55B independent self-test")

    c72_raw = read_pinned(C72G_PATHS, C72G_PINS)
    c72 = {key: strict_json(c72_raw[key], "C72g:" + key)
           for key in ("contract", "verification", "self_test", "outer", "head")}
    for key in c72:
        verify_object(c72[key], "C72g:" + key, C72G_OBJECTS[key])
    need(c72["contract"].get("effective_checkpoint_object_sha256") == CHECKPOINT_OBJECT_PIN,
         "C72g head binding")
    need(c72["verification"].get("status", "").startswith("PASS_FROZEN_NO_PRODUCER") and
         c72["verification"].get("public_global_census", {}).get("UNRESOLVED_R1648_CONTINUATION") == EXPECTED_OVERLAY and
         c72["verification"].get("public_global_unresolved_zero") is False and
         c72["verification"].get("formal_credit") == 0,
         "C72g structural authority only")
    need(c72["self_test"].get("status", "").startswith("PASS_39_OF_39"),
         "C72g attacks")
    return {
        "contract": contract,
        "C55A_raw": c55a_raw,
        "C55A": c55a,
        "C55B_raw": c55b_raw,
        "C55B": c55b_objects,
        "C72g_raw": c72_raw,
        "C72g": c72,
    }


def validate_c78l() -> dict[str, Any]:
    raw = read_dual(C78L_A, C78L_B, C78L_NAMES, C78L_PINS, "C78l")
    verification_a = secure_file(C78L_VERIFY_A, C78L_VERIFY_FILE_PIN)
    verification_b = secure_file(C78L_VERIFY_B, C78L_VERIFY_FILE_PIN)
    need(verification_a == verification_b, "C78l verification A/B bytes")
    verification = strict_json(verification_a, "C78l verification")
    verify_object(verification, "C78l verification", C78L_VERIFY_OBJECT_PIN)
    need(verification.get("status", "").startswith("PASS_INDEPENDENT_C78L") and
         verification.get("self_test", {}).get("attack_count") == 52 and
         all(value == "FAIL_CLOSED" for value in
             verification.get("self_test", {}).get("attacks", {}).values()),
         "C78l independent verification")
    completion_raw = {
        key: secure_file(C78L_COMPLETION / name, C78L_COMPLETION_PINS[key])
        for key, name in C78L_COMPLETION_NAMES.items()
    }
    receipt = strict_json(completion_raw["receipt"], "C78l completion")
    outer = strict_json(completion_raw["outer"], "C78l completion outer")
    verify_object(receipt, "C78l completion", C78L_COMPLETION_OBJECT_PIN)
    verify_object(outer, "C78l completion outer", C78L_COMPLETION_OUTER_OBJECT_PIN)
    need(receipt.get("dual_build_byte_identical") is True and
         receipt.get("verification_A_B_byte_identical") is True and
         receipt.get("canonical_pointer_or_seal_written") is False,
         "C78l final completion semantics")
    result = strict_json(raw["result"], "C78l result")
    verify_object(result, "C78l result", C78L_RESULT_OBJECT_PIN)
    need(result.get("branch_unresolved") == 0 and
         result.get("public_global_unresolved_after_branch") == EXPECTED_SINGLETON and
         result.get("public_global_unresolved_zero") is False and
         result.get("candidate_is_authority") is False,
         "C78l branch boundary")
    manifest = parse_manifest(raw["manifest"], "C78l manifest")
    for key in ("lock", "tasks", "sides", "cells", "pairs", "registry", "result", "report"):
        need(manifest.get(C78L_NAMES[key]) == C78L_PINS[key], "C78l manifest:" + key)
    return {
        "raw": raw,
        "verification_raw": verification_a,
        "verification": verification,
        "completion_raw": completion_raw,
        "completion": receipt,
        "result": result,
        "cells": gzip_rows(raw["cells"], "C78l public cells"),
        "pairs": gzip_rows(raw["pairs"], "C78l reflection pairs"),
    }


def validate_c78s() -> dict[str, Any]:
    a = rooted(str(C78S_FINAL["build_A_directory"]))
    b = rooted(str(C78S_FINAL["build_B_directory"]))
    pins = C78S_FINAL["pins"]
    need(isinstance(pins, dict), "C78s pins mapping")
    raw = read_dual(a, b, C78S_NAMES, pins, "C78s")
    verify_a_raw = secure_file(rooted(str(C78S_FINAL["verification_A_path"])),
                               str(C78S_FINAL["verification_A_file_sha256"]))
    verify_b_raw = secure_file(rooted(str(C78S_FINAL["verification_B_path"])),
                               str(C78S_FINAL["verification_B_file_sha256"]))
    need(verify_a_raw == verify_b_raw, "C78s verification A/B bytes")
    verify_a = strict_json(verify_a_raw, "C78s verification A")
    verify_b = strict_json(verify_b_raw, "C78s verification B")
    verify_object(verify_a, "C78s verification A",
                  str(C78S_FINAL["verification_A_object_sha256"]))
    verify_object(verify_b, "C78s verification B",
                  str(C78S_FINAL["verification_B_object_sha256"]))
    need(verify_a.get("object_sha256") == verify_b.get("object_sha256") ==
         C78S_FINAL["verification_A_object_sha256"] ==
         C78S_FINAL["verification_B_object_sha256"],
         "C78s verification A/B object pins agree")
    attacks = verify_a.get("coherent_attacks", {})
    attack_count = attacks.get("attack_count")
    attack_names = attacks.get("names")
    need(verify_a == verify_b and
         verify_a.get("candidate_base_bundle", {}).get("stage_a_stage_b_bytes_identical") is True and
         verify_a.get("candidate_base_bundle", {}).get("stage_a_stage_b_inodes_distinct") is True and
         verify_a.get("candidate_base_bundle", {}).get("result_file_sha256") == pins["result"] and
         verify_a.get("candidate_base_bundle", {}).get("result_object_sha256") == C78S_FINAL["result_object_sha256"] and
         verify_a.get("verifier_file_sha256") == C78S_FINAL["verifier_source_file_sha256"] and
         isinstance(attack_count, int) and attack_count >= 100 and
         attacks.get("rejected") == attack_count and
         isinstance(attack_names, list) and len(attack_names) == attack_count and
         len(set(attack_names)) == attack_count,
         "C78s independent dual verification")

    final_manifest_a_raw = secure_file(rooted(str(C78S_FINAL["final_manifest_A_path"])),
        str(C78S_FINAL["final_manifest_file_sha256"]))
    final_manifest_b_raw = secure_file(rooted(str(C78S_FINAL["final_manifest_B_path"])),
        str(C78S_FINAL["final_manifest_file_sha256"]))
    final_outer_a_raw = secure_file(rooted(str(C78S_FINAL["final_outer_A_path"])),
        str(C78S_FINAL["final_outer_file_sha256"]))
    final_outer_b_raw = secure_file(rooted(str(C78S_FINAL["final_outer_B_path"])),
        str(C78S_FINAL["final_outer_file_sha256"]))
    need(rooted(str(C78S_FINAL["verification_A_path"])).parent == a and
         rooted(str(C78S_FINAL["verification_B_path"])).parent == b and
         rooted(str(C78S_FINAL["final_manifest_A_path"])).parent == a and
         rooted(str(C78S_FINAL["final_manifest_B_path"])).parent == b and
         rooted(str(C78S_FINAL["final_outer_A_path"])).parent == a and
         rooted(str(C78S_FINAL["final_outer_B_path"])).parent == b,
         "C78s all final members remain inside their isolated stages")
    need(final_manifest_a_raw == final_manifest_b_raw and final_outer_a_raw == final_outer_b_raw,
         "C78s final stage A/B bytes")
    final_outer = strict_json(final_outer_a_raw, "C78s final outer closure receipt")
    verify_object(final_outer, "C78s final outer closure receipt",
                  str(C78S_FINAL["final_outer_object_sha256"]))
    need(final_outer.get("verification_file_sha256") == C78S_FINAL["verification_A_file_sha256"] and
         final_outer.get("verification_object_sha256") == C78S_FINAL["verification_A_object_sha256"] and
         final_outer.get("final_manifest_file_sha256") == C78S_FINAL["final_manifest_file_sha256"] and
         final_outer.get("all_final_stage_bytes_identical") is True and
         final_outer.get("all_final_members_terminal_byte_replayed_in_both_stages") is True and
         final_outer.get("terminal_byte_replay_member_count_per_stage") == 13,
         "C78s 13-member final closure")
    final_manifest = parse_manifest(final_manifest_a_raw, "C78s final manifest")
    for key, name in C78S_NAMES.items():
        need(final_manifest.get(name) == pins[key], "C78s final manifest base:" + key)
    need(final_manifest.get(rooted(str(C78S_FINAL["verification_A_path"])).name) ==
         C78S_FINAL["verification_A_file_sha256"],
         "C78s final manifest verification")

    result = strict_json(raw["result"], "C78s result")
    verify_object(result, "C78s result", str(C78S_FINAL["result_object_sha256"]))
    need(result.get("singleton_branch_unresolved") == 0 and
         result.get("public_global_unresolved_after_branch") == EXPECTED_LARGE and
         result.get("public_global_unresolved_zero") is False and
         result.get("branch_projection_installed_as_canonical_state") is False,
         "C78s branch boundary")
    manifest = parse_manifest(raw["manifest"], "C78s manifest")
    for key in ("lock", "children", "sources", "pairs", "cells", "projection", "result", "report"):
        need(manifest.get(C78S_NAMES[key]) == pins[key], "C78s manifest:" + key)
    return {
        "raw": raw,
        "verification_raw": verify_a_raw,
        "verification": verify_a,
        "completion_raw": {
            "manifest": final_manifest_a_raw,
            "outer": final_outer_a_raw,
        },
        "completion": final_outer,
        "result": result,
        "projection": gzip_rows(raw["projection"], "C78s projection"),
        "pairs": gzip_rows(raw["pairs"], "C78s pairs"),
        "cells": gzip_rows(raw["cells"], "C78s cells"),
    }


def reconstruct() -> dict[str, Any]:
    static = validate_static_authorities()
    c78l = validate_c78l()
    c78s = validate_c78s()

    ledger = static["C55A"]["leaf_ledger"]
    leaves = ledger.get("leaves")
    need(isinstance(leaves, list) and len(leaves) == EXPECTED_UNIVERSE, "C55A 76832 leaves")
    by_cell: dict[str, dict[str, Any]] = {}
    unresolved: set[str] = set()
    baseline: set[str] = set()
    for ordinal, leaf in enumerate(leaves):
        need(isinstance(leaf, dict), "C55A leaf object")
        verify_row(leaf, "C55A leaf")
        need(leaf.get("leaf_ordinal") == ordinal, "C55A leaf order")
        cell_id = leaf.get("cell_id")
        need(isinstance(cell_id, str) and cell_id not in by_cell, "C55A unique cell")
        terminal = leaf.get("terminal_disposition")
        reason = leaf.get("unresolved_reason")
        need((terminal in TERMINALS and reason is None) or
             (terminal is None and isinstance(reason, str) and bool(reason)),
             "C55A terminal/unresolved XOR")
        by_cell[cell_id] = leaf
        (unresolved if terminal is None else baseline).add(cell_id)
    need(len(baseline) == EXPECTED_BASELINE and len(unresolved) == EXPECTED_OVERLAY,
         "C55A exact baseline/overlay partition")

    cell_rows = gzip_rows(static["C55B_raw"]["cells"], "C55B cells")
    edge_rows = gzip_rows(static["C55B_raw"]["edges"], "C55B edges")
    component_rows = gzip_rows(static["C55B_raw"]["components"], "C55B components")
    need(len(cell_rows) == EXPECTED_C55B_CELLS and len(component_rows) == 26 and edge_rows,
         "C55B structural census")
    c55b_by_cell = one_index(cell_rows, "cell_id", "C55B cells")
    component_by_index = one_index(component_rows, "component_index", "C55B components")
    need(Counter(row["cell_count"] for row in component_rows) == Counter({850: 2, 1: 24}),
         "C55B component sizes")
    pair_cells: dict[int, list[dict[str, Any]]] = defaultdict(list)
    c55b_unresolved: set[str] = set()
    for row in cell_rows:
        cell_id = row["cell_id"]
        need(cell_id in by_cell, "C55B cell in C55A")
        pair_cells[row["pair_index"]].append(row)
        if row["current_effective_disposition"] == "UNRESOLVED_R1648_CONTINUATION":
            c55b_unresolved.add(cell_id)
            need(cell_id in unresolved, "C55B unresolved agrees C55A")
        else:
            need(row["current_effective_disposition"] == "EARLIEST_PREFIX_EXCLUDED" and
                 by_cell[cell_id]["terminal_disposition"] == "EARLIEST_PREFIX_EXCLUDED",
                 "C55B baseline agrees C55A")
        component = component_by_index[row["component_index"]]
        need(component["component_id"] == row["component_id"], "C55B component identity")
    need(c55b_unresolved == unresolved, "C55A/C55B exact unresolved identity")
    need(len(pair_cells) == EXPECTED_PAIRS and
         all(len(rows) == 2 for rows in pair_cells.values()), "C55B 862 reflection pairs")
    for rows in pair_cells.values():
        left, right = rows
        need(left["reflection_partner_cell_id"] == right["cell_id"] and
             right["reflection_partner_cell_id"] == left["cell_id"],
             "C55B reciprocal reflection")

    large_cells = c78l["cells"]
    large_pairs = c78l["pairs"]
    need(len(large_cells) == EXPECTED_LARGE and len(large_pairs) == EXPECTED_LARGE_PAIRS,
         "C78l exact row census")
    large_by_cell = one_index(large_cells, "cell_id", "C78l cells")
    large_pair_by_index = one_index(large_pairs, "pair_index", "C78l pairs")
    singleton_rows = c78s["projection"]
    singleton_pairs = c78s["pairs"]
    need(len(singleton_rows) == EXPECTED_SINGLETON and
         len(singleton_pairs) == EXPECTED_SINGLETON_PAIRS and
         len(c78s["cells"]) == EXPECTED_SINGLETON,
         "C78s exact row census")
    singleton_by_cell = one_index(singleton_rows, "cell_id", "C78s projection")
    singleton_pair_by_index = one_index(singleton_pairs, "pair_index", "C78s pairs")

    large_set = set(large_by_cell)
    singleton_set = set(singleton_by_cell)
    need(not (large_set & singleton_set) and
         large_set | singleton_set == unresolved,
         "C78l/C78s disjoint exhaustive unresolved overlay")
    need(all(component_by_index[c55b_by_cell[cell]["component_index"]]["cell_count"] == 850
             for cell in large_set), "C78l only large components")
    need(all(component_by_index[c55b_by_cell[cell]["component_index"]]["cell_count"] == 1
             for cell in singleton_set), "C78s only singleton components")

    overlay_rows: list[dict[str, Any]] = []
    overlay_by_cell: dict[str, dict[str, Any]] = {}
    for cell_id in sorted(unresolved, key=lambda item: by_cell[item]["leaf_ordinal"]):
        leaf = by_cell[cell_id]
        structure = c55b_by_cell[cell_id]
        if cell_id in large_by_cell:
            authority_row = large_by_cell[cell_id]
            enum = authority_row.get("public_cell_disposition")
            need(enum in LARGE_MAP and authority_row.get("unresolved_count") == 0 and
                 authority_row.get("owner_history_glue_two_sides_incidence_closed") is True and
                 authority_row.get("prefix_Kraft", {}).get("prefix_free") is True and
                 authority_row.get("C55A_identity_role_only") is True and
                 authority_row.get("C55A_termination_or_partition_authority_used") is False,
                 "C78l terminal and closure authority")
            terminal, rule = LARGE_MAP[enum]
            authority = "C78L_VERIFIED_FINAL_SURFACE"
        else:
            authority_row = singleton_by_cell[cell_id]
            enum = authority_row.get("terminal_enum")
            need(enum in SINGLETON_MAP and
                 authority_row.get("global_projection_installed") is False and
                 authority_row.get("candidate_is_authority") is False and
                 authority_row.get("singleton_branch_unresolved") == 0 and
                 authority_row.get("branch_projection_target") == "C79G_ATOMIC_MERGE",
                 "C78s terminal authority projection")
            pair = singleton_pair_by_index[structure["pair_index"]]
            need(pair.get("whole_reflection_pair_terminal") is True and
                 pair.get("parent_prefix_free") is True and
                 pair.get("parent_Kraft") == "1" and
                 pair.get("prefix_free_and_exact_Kraft_one_certificate_carried_from_C77s") is True,
                 "C78s exact parent Kraft")
            terminal, rule = SINGLETON_MAP[enum]
            authority = "C78S_VERIFIED_FINAL_SURFACE"
        row = close_row({
            "schema": SCHEMA + ".overlay-row",
            "overlay_ordinal": len(overlay_rows),
            "leaf_ordinal": leaf["leaf_ordinal"],
            "cell_id": cell_id,
            "C55A_leaf_row_sha256": leaf["row_sha256"],
            "C55B_cell_row_sha256": structure["row_sha256"],
            "pair_index": structure["pair_index"],
            "component_index": structure["component_index"],
            "component_id": structure["component_id"],
            "reflection_partner_cell_id": structure["reflection_partner_cell_id"],
            "previous_terminal_disposition": None,
            "previous_unresolved_reason": leaf["unresolved_reason"],
            "terminal_authority": authority,
            "terminal_authority_row_sha256": authority_row["row_sha256"],
            "authority_input_enum": enum,
            "mapping_rule": rule,
            "terminal_disposition": terminal,
            "overlay_sets_disjoint_and_exact": True,
            "installed_atomically_only_by_C79g_completion": True,
            "row_is_individually_creditable": False,
            "closure": dict(CLOSURE),
        })
        overlay_rows.append(row)
        overlay_by_cell[cell_id] = row
    need(len(overlay_rows) == EXPECTED_OVERLAY, "overlay 1148")

    successor_rows: list[dict[str, Any]] = []
    successor_by_cell: dict[str, dict[str, Any]] = {}
    final_census: Counter[str] = Counter()
    retained = 0
    replaced = 0
    for leaf in leaves:
        overlay = overlay_by_cell.get(leaf["cell_id"])
        if overlay is None:
            terminal = leaf["terminal_disposition"]
            need(terminal in TERMINALS and leaf["unresolved_reason"] is None,
                 "baseline remains terminal")
            mode = "C72G_BASELINE_RETAINED"
            authority = "C55A_PREEXISTING_TERMINAL_RETAINED_UNDER_C72G_STRUCTURAL_CLOSURE"
            authority_row_sha = leaf["row_sha256"]
            overlay_sha = None
            preserved = True
            retained += 1
        else:
            terminal = overlay["terminal_disposition"]
            mode = "C79G_OVERLAY_REPLACEMENT"
            authority = overlay["terminal_authority"]
            authority_row_sha = overlay["terminal_authority_row_sha256"]
            overlay_sha = overlay["row_sha256"]
            preserved = False
            replaced += 1
        row = close_row({
            "schema": SCHEMA + ".full-successor-row",
            "leaf_ordinal": leaf["leaf_ordinal"],
            "cell_id": leaf["cell_id"],
            "C55A_leaf_row_sha256": leaf["row_sha256"],
            "origin_key": leaf["origin_key"],
            "physical_chart": leaf["physical_chart"],
            "exact_box": leaf["exact_box"],
            "source_cell_row_sha256": leaf["source_cell_row_sha256"],
            "component_ref": leaf["component_ref"],
            "reflection_pair_ref": leaf["reflection_pair_ref"],
            "previous_terminal_disposition": leaf["terminal_disposition"],
            "previous_unresolved_reason": leaf["unresolved_reason"],
            "successor_terminal_disposition": terminal,
            "successor_unresolved_reason": None,
            "lineage_mode": mode,
            "terminal_authority": authority,
            "terminal_authority_row_sha256": authority_row_sha,
            "overlay_row_sha256": overlay_sha,
            "baseline_terminal_preserved_exactly": preserved,
            "candidate_atomic_install_only": True,
        })
        successor_rows.append(row)
        successor_by_cell[leaf["cell_id"]] = row
        final_census[terminal] += 1
    need(len(successor_rows) == EXPECTED_UNIVERSE and retained == EXPECTED_BASELINE and
         replaced == EXPECTED_OVERLAY and sum(final_census.values()) == EXPECTED_UNIVERSE,
         "full successor exact partition")
    need(not (set(final_census) - TERMINALS), "final four-class census keys")

    parent_rows: list[dict[str, Any]] = []
    parent_modes: Counter[str] = Counter()
    for pair_index in sorted(pair_cells):
        rows = pair_cells[pair_index]
        role_rows = {by_cell[row["cell_id"]]["component_ref"]["cell_role"]: row for row in rows}
        need(set(role_rows) == {"REPRESENTATIVE", "REFLECTED"}, "reflection roles")
        representative = role_rows["REPRESENTATIVE"]
        reflected = role_rows["REFLECTED"]
        ids = {representative["cell_id"], reflected["cell_id"]}
        if ids <= baseline:
            mode = "C72G_BASELINE_RETAINED"
            authority = "C55A_PREEXISTING_TERMINALS_WITH_C72G_STRUCTURAL_CLOSURE"
            evidence = "C72G"
            authority_sha = representative["C42_parent_row_sha256"]
            need(all(row["whole_pair_terminal_after_C53"] is True for row in rows),
                 "baseline pair C53 closure")
        elif ids <= large_set:
            mode = "C78L_OVERLAY"
            authority = "C78L_VERIFIED_FINAL_SURFACE"
            evidence = "C78L"
            pair = large_pair_by_index[pair_index]
            authority_sha = pair["row_sha256"]
            need(pair.get("owner_history_glue_two_sides_incidence_closed") is True and
                 pair.get("prefix_Kraft", {}).get("prefix_free") is True and
                 pair.get("unresolved_count") == 0,
                 "C78l reflection parent closure")
        else:
            need(ids <= singleton_set, "no mixed reflection authority")
            mode = "C78S_OVERLAY"
            authority = "C78S_VERIFIED_FINAL_SURFACE"
            evidence = "C78S"
            pair = singleton_pair_by_index[pair_index]
            authority_sha = pair["row_sha256"]
            need(pair.get("whole_reflection_pair_terminal") is True and
                 pair.get("parent_prefix_free") is True and pair.get("parent_Kraft") == "1",
                 "C78s reflection parent closure")
        component_indices = sorted({row["component_index"] for row in rows})
        need(len(component_indices) == 1, "reflection pair one component")
        dispositions = Counter(successor_by_cell[item]["successor_terminal_disposition"] for item in ids)
        parent = close_row({
            "schema": SCHEMA + ".reflection-parent-closure-row",
            "parent_ordinal": len(parent_rows),
            "pair_index": pair_index,
            "representative_cell_id": representative["cell_id"],
            "reflected_cell_id": reflected["cell_id"],
            "representative_C55B_row_sha256": representative["row_sha256"],
            "reflected_C55B_row_sha256": reflected["row_sha256"],
            "representative_successor_row_sha256": successor_by_cell[representative["cell_id"]]["row_sha256"],
            "reflected_successor_row_sha256": successor_by_cell[reflected["cell_id"]]["row_sha256"],
            "component_indices": component_indices,
            "parent_lineage_mode": mode,
            "terminal_authority": authority,
            "parent_authority_row_sha256": authority_sha,
            "terminal_disposition_census": dict(sorted(dispositions.items())),
            "reciprocal_reflection_partner_identity_closed": True,
            "owner_history_glue_two_sides_incidence_closed": True,
            "prefix_Kraft": {
                "evidence_authority": evidence,
                "prefix_free": True,
                "exact_parent_closure": True,
                "physical_reflection_duplicate_credit": 0,
            },
            "unresolved_count": 0,
        })
        parent_rows.append(parent)
        parent_modes[mode] += 1
    need(len(parent_rows) == EXPECTED_PAIRS and parent_modes == Counter({
        "C72G_BASELINE_RETAINED": EXPECTED_BASELINE_PAIRS,
        "C78L_OVERLAY": EXPECTED_LARGE_PAIRS,
        "C78S_OVERLAY": EXPECTED_SINGLETON_PAIRS,
    }), "862 reflection parent authority partition")

    return {
        "static": static,
        "C78l": c78l,
        "C78s": c78s,
        "overlay_rows": overlay_rows,
        "successor_rows": successor_rows,
        "parent_rows": parent_rows,
        "final_census": {key: final_census.get(key, 0) for key in sorted(TERMINALS)},
        "parent_modes": dict(sorted(parent_modes.items())),
        "baseline_count": retained,
        "overlay_count": replaced,
    }


def input_registry(state: dict[str, Any]) -> dict[str, Any]:
    fixed_files: dict[str, dict[str, str]] = {}
    for family, paths, pins in (
        ("C55A", C55A_PATHS, C55A_PINS),
        ("C55B", C55B_PATHS, C55B_PINS),
        ("C72g", C72G_PATHS, C72G_PINS),
    ):
        for key in sorted(paths):
            fixed_files[f"{family}:{key}"] = {
                "path": str(paths[key].relative_to(ROOT)), "file_sha256": pins[key],
            }
    c78l_files = {key: {"filename": C78L_NAMES[key], "file_sha256": C78L_PINS[key]}
                   for key in sorted(C78L_NAMES)}
    c78s_files = {key: {"filename": C78S_NAMES[key], "file_sha256": C78S_FINAL["pins"][key]}
                   for key in sorted(C78S_NAMES)}
    return close_object({
        "schema": SCHEMA + ".source-registry",
        "consumer_file_sha256": sha_file(SELF),
        "contract_file_sha256": CONTRACT_FILE_PIN,
        "contract_object_sha256": CONTRACT_OBJECT_PIN,
        "closed_schema_file_sha256": CLOSED_SCHEMA_FILE_PIN,
        "effective_checkpoint_object_sha256": CHECKPOINT_OBJECT_PIN,
        "fixed_input_files": fixed_files,
        "C78l_dual_base_member_pins": c78l_files,
        "C78l_verification_file_sha256": C78L_VERIFY_FILE_PIN,
        "C78l_verification_object_sha256": C78L_VERIFY_OBJECT_PIN,
        "C78l_completion_member_pins": dict(C78L_COMPLETION_PINS),
        "C78s_filled_final_surface": copy.deepcopy(C78S_FINAL),
        "C78s_dual_base_member_pins": c78s_files,
        "all_upstream_producer_sources_opened_or_read": False,
        "all_upstream_producer_sources_imported_compiled_or_executed": False,
        "terminal_authority": {"C78l_rows": EXPECTED_LARGE, "C78s_rows": EXPECTED_SINGLETON},
        "structure_only_authority": ["C55A", "C55B", "C72g"],
        "C55A_C55B_C72g_new_terminal_authority": False,
        "canonical_pointer_written": False,
        "D02_started": False,
        "candidate_credit": dict(ZERO_CANDIDATE_CREDIT),
    })


def build(outdir: Path) -> None:
    # The caller/main has already executed ensure_final_pins_filled().
    # No input was read and no output path was touched before that gate.
    state = reconstruct()
    need(not outdir.exists() and outdir.parent.is_dir(), "fresh append-only candidate directory")

    overlay_raw, overlay_desc = gzip_encode(state["overlay_rows"])
    successor_raw, successor_desc = gzip_encode(state["successor_rows"])
    parents_raw, parents_desc = gzip_encode(state["parent_rows"])
    need(overlay_desc["row_count"] == EXPECTED_OVERLAY and
         successor_desc["row_count"] == EXPECTED_UNIVERSE and
         parents_desc["row_count"] == EXPECTED_PAIRS,
         "output descriptor counts")
    registry = input_registry(state)
    descriptors = {
        "overlay_1148": overlay_desc,
        "full_successor_76832": successor_desc,
        "reflection_parent_closure_862": parents_desc,
    }
    final_census = dict(state["final_census"])
    final_census["total"] = sum(final_census.values())
    result = close_object({
        "schema": SCHEMA + ".result",
        "status": "PASS_CANDIDATE_1148_EXACT_OVERLAY__76832_FULL_SUCCESSOR__862_REFLECTION_PARENTS__PUBLIC_UNRESOLVED_ZERO__AWAIT_DUAL_COMPLETION_FOR_FORMAL_CREDIT",
        "source_registry_object_sha256": registry["object_sha256"],
        "ledger_descriptors": descriptors,
        "exact_overlay_partition": {
            "C78l_large": EXPECTED_LARGE,
            "C78s_singleton": EXPECTED_SINGLETON,
            "total": state["overlay_count"],
            "sets_disjoint": True,
            "union_equals_C55A_and_C55B_unresolved": True,
        },
        "baseline_retention": {
            "retained_terminal_rows": state["baseline_count"],
            "terminal_disposition_unchanged": True,
            "C55A_row_lineage_unchanged": True,
        },
        "derived_final_four_class_census": final_census,
        "derived_final_four_class_census_was_not_hard_coded": True,
        "public_global_unresolved": 0,
        "reflection_parent_closure": {
            "row_count": EXPECTED_PAIRS,
            "authority_partition": state["parent_modes"],
            "reciprocal": True,
            "all_terminal": True,
        },
        "authority_separation": {
            "C55A": "IDENTITY_AND_PREDECESSOR_DISPOSITION_ONLY",
            "C55B": "COMPONENT_REFLECTION_GLUE_INCIDENCE_STRUCTURE_ONLY",
            "C72g": "BASELINE_STRUCTURAL_CLOSURE_ONLY",
            "C78l": "SOLE_AUTHORITY_FOR_1124_REPLACEMENTS",
            "C78s": "SOLE_AUTHORITY_FOR_24_REPLACEMENTS",
            "C55A_C55B_C72g_new_terminal_authority": False,
        },
        "closure": dict(CLOSURE),
        "candidate_credit": dict(ZERO_CANDIDATE_CREDIT),
        "conditional_completion_credit": dict(COMPLETED_CREDIT),
        "precursor_credits": {
            "C65_local_terminal_formal_credit": 0,
            "C69c_source_decision_formal_credit": 0,
            "C70_ready_intersection_formal_credit": 0,
            "C78l_precursor_formal_credit": 0,
            "C78s_precursor_formal_credit": 0,
        },
        "actual_C3_disposition_count": 0,
        "conditional_C3_promoted_to_actual_C3": False,
        "canonical_pointer_written": False,
        "D02_started": False,
    })
    report = (
        "# C79g true global no-producer consumer candidate\n\n"
        f"- exact overlay: `{EXPECTED_LARGE} + {EXPECTED_SINGLETON} = {EXPECTED_OVERLAY}`\n"
        f"- baseline terminal rows retained: `{EXPECTED_BASELINE}`\n"
        f"- full successor rows: `{EXPECTED_UNIVERSE}`; public unresolved: `0`\n"
        f"- reflection parents: `{EXPECTED_PAIRS}` (`{EXPECTED_BASELINE_PAIRS}` baseline, "
        f"`{EXPECTED_LARGE_PAIRS}` C78l, `{EXPECTED_SINGLETON_PAIRS}` C78s)\n"
        f"- final four-class census (derived after merge): `{json.dumps(final_census, sort_keys=True)}`\n"
        "- owner/history/glue/two-sides/incidence/prefix-Kraft: closed\n"
        "- C55A/C55B/C72g are identity/structure only; new terminal authority is exclusively C78l/C78s\n"
        "- candidate credit is zero; formal global closure credit exists only after dual completion\n"
        f"- D02 gate/task credit: `0/0`; formal pending tasks: `{EXPECTED_PENDING_D02}`; D02 not started\n"
        "- no canonical pointer.\n"
    ).encode("utf-8")
    lock = (
        "C79g isolated candidate only. Formal-global credit remains zero until the unique "
        "dual-build, dual-verification completion surface is sealed. D02 is not started.\n"
    ).encode("ascii")

    base_raw = {
        LOCK: lock,
        OVERLAY: overlay_raw,
        SUCCESSOR: successor_raw,
        PARENTS: parents_raw,
        REGISTRY: canonical(registry) + b"\n",
        RESULT: canonical(result) + b"\n",
        REPORT: report,
    }
    os.mkdir(outdir, 0o755)
    for name in (LOCK, OVERLAY, SUCCESSOR, PARENTS, REGISTRY, RESULT, REPORT):
        exclusive(outdir / name, base_raw[name])
    manifest_raw = b"".join(
        f"{sha_bytes(base_raw[name])}  {name}\n".encode("ascii")
        for name in (LOCK, OVERLAY, SUCCESSOR, PARENTS, REGISTRY, RESULT, REPORT)
    )
    exclusive(outdir / CANDIDATE_MANIFEST, manifest_raw)
    outer = close_object({
        "schema": SCHEMA + ".candidate-outer-receipt",
        "candidate_result_object_sha256": result["object_sha256"],
        "source_registry_object_sha256": registry["object_sha256"],
        "candidate_manifest_file_sha256": sha_bytes(manifest_raw),
        "ordered_member_file_sha256": [
            {"filename": name, "file_sha256": sha_bytes(base_raw[name])}
            for name in (LOCK, OVERLAY, SUCCESSOR, PARENTS, REGISTRY, RESULT, REPORT)
        ],
        "candidate_outer_receipt_published_last": True,
        "terminal_byte_replay_required_after_outer_receipt": True,
        "candidate_directory_sealed_mode_after_terminal_replay": "0555",
        "candidate_member_required_mode": "0444",
        "partial_publication_policy": "REJECT_AND_PRESERVE_NEVER_OVERWRITE_OR_REUSE",
        "candidate_credit": dict(ZERO_CANDIDATE_CREDIT),
        "canonical_pointer_written": False,
        "D02_started": False,
    })
    exclusive(outdir / CANDIDATE_OUTER, canonical(outer) + b"\n")
    base_mtimes = [(outdir / name).stat().st_mtime_ns
                   for name in (LOCK, OVERLAY, SUCCESSOR, PARENTS, REGISTRY, RESULT, REPORT)]
    manifest_mtime = (outdir / CANDIDATE_MANIFEST).stat().st_mtime_ns
    outer_mtime = (outdir / CANDIDATE_OUTER).stat().st_mtime_ns
    need(max(base_mtimes) < manifest_mtime < outer_mtime,
         "candidate publication mtime order and outer-last")
    for name in CANDIDATE_MEMBERS:
        secure_snapshot(outdir / name, 0o444)
    os.chmod(outdir, 0o555)
    secure_directory(outdir, 0o555)


def complete(build_a: Path, build_b: Path, verify_a: Path, verify_b: Path, outdir: Path) -> None:
    # A failed publication is deliberately left in place.  Because this entry
    # point accepts only a fresh directory and every member uses O_EXCL, an
    # isolated half publication can only be rejected/superseded, never resumed,
    # overwritten, or silently reused.
    secure_directory(build_a, 0o555)
    secure_directory(build_b, 0o555)
    need({path.name for path in build_a.iterdir()} == set(CANDIDATE_MEMBERS),
         "C79g build A exact member universe")
    need({path.name for path in build_b.iterdir()} == set(CANDIDATE_MEMBERS),
         "C79g build B exact member universe")
    members: dict[str, bytes] = {}
    build_identities: dict[str, dict[str, tuple[int, int]]] = {"A": {}, "B": {}}
    for name in CANDIDATE_MEMBERS:
        left, left_identity = secure_snapshot(build_a / name, 0o444)
        right, right_identity = secure_snapshot(build_b / name, 0o444)
        need(left == right, "C79g dual candidate byte identity:" + name)
        need(left_identity != right_identity,
             "C79g dual candidate inode separation:" + name)
        build_identities["A"][name] = left_identity
        build_identities["B"][name] = right_identity
        members[name] = left
    result = strict_json(members[RESULT], "C79g candidate result")
    verify_object(result, "C79g candidate result")
    need(result.get("public_global_unresolved") == 0 and
         result.get("closure") == CLOSURE and
         result.get("candidate_credit") == ZERO_CANDIDATE_CREDIT and
         result.get("conditional_completion_credit") == COMPLETED_CREDIT,
         "candidate result completion gate")
    va, verify_a_identity = secure_snapshot(verify_a, 0o444)
    vb, verify_b_identity = secure_snapshot(verify_b, 0o444)
    need(va == vb, "C79g verification A/B bytes")
    need(verify_a_identity != verify_b_identity, "C79g verification A/B inode separation")
    verification = strict_json(va, "C79g independent verification")
    verify_object(verification, "C79g independent verification")
    attacks = verification.get("attacks")
    need(verification.get("status", "").startswith("PASS_INDEPENDENT_C79G") and
         verification.get("all_attacks_fail_closed") is True and
         verification.get("verifier_file_sha256") == C79_FROZEN_VERIFIER_FILE_PIN and
         verification.get("attack_count") == 121 and
         isinstance(attacks, dict) and len(attacks) == 121 and
         len(set(attacks)) == 121 and
         all(value == "FAIL_CLOSED" for value in attacks.values()) and
         verification.get("dual_candidate_build_directories_mode") == "0555" and
         verification.get("dual_candidate_members_mode") == "0444" and
         verification.get("dual_candidate_members_single_link") is True and
         verification.get("dual_candidate_members_byte_identical") is True and
         verification.get("dual_candidate_corresponding_inodes_distinct") is True and
         verification.get("candidate_member_file_sha256") ==
             {name: sha_bytes(raw) for name, raw in sorted(members.items())},
         "independent verification completion gate")
    need(not outdir.exists() and outdir.parent.is_dir(), "fresh append-only completion directory")

    attack_names = sorted(attacks)
    member_hashes = {name: sha_bytes(raw) for name, raw in sorted(members.items())}
    receipt = close_object({
        "schema": SCHEMA + ".dual-completion-receipt",
        "status": "PASS_DUAL_ISOLATED_BYTE_IDENTICAL__DUAL_INDEPENDENT_NO_PRODUCER_VERIFICATION__PUBLIC_UNRESOLVED_ZERO__FORMAL_GLOBAL_CLOSURE_CREDIT_ONE__D02_UNLOCK_ONLY",
        "candidate_member_file_sha256": member_hashes,
        "dual_build_byte_identical": True,
        "dual_build_directory_required_mode": "0555",
        "dual_build_member_required_mode": "0444",
        "dual_build_member_single_link": True,
        "dual_build_corresponding_inodes_distinct": True,
        "candidate_result_object_sha256": result["object_sha256"],
        "frozen_C79g_verifier_source_file_sha256": C79_FROZEN_VERIFIER_FILE_PIN,
        "independent_verification_file_sha256": sha_bytes(va),
        "independent_verification_object_sha256": verification["object_sha256"],
        "verification_A_B_byte_identical": True,
        "verification_A_B_inodes_distinct": True,
        "attack_count": 121,
        "unique_attack_names": attack_names,
        "all_attacks_fail_closed": True,
        "public_global_unresolved": 0,
        "closure": dict(CLOSURE),
        "completion_credit": dict(COMPLETED_CREDIT),
        "precursor_credits_remain_zero": True,
        "completion_directory_sealed_mode_after_terminal_replay": "0555",
        "completion_member_required_mode": "0444",
        "partial_publication_policy": "REJECT_AND_PRESERVE_NEVER_OVERWRITE_OR_REUSE",
        "canonical_pointer_written": False,
        "D02_started": False,
    })
    os.mkdir(outdir, 0o755)
    exclusive(outdir / FINAL_VERIFY, va)
    receipt_raw = canonical(receipt) + b"\n"
    exclusive(outdir / FINAL_RECEIPT, receipt_raw)
    global_entries = [
        {"file_sha256": sha_bytes(members[name]), "entry_name": "build-a/" + name}
        for name in CANDIDATE_MEMBERS
    ] + [
        {"file_sha256": sha_bytes(members[name]), "entry_name": "build-b/" + name}
        for name in CANDIDATE_MEMBERS
    ] + [
        {"file_sha256": sha_bytes(va), "entry_name": "verification-a/" + FINAL_VERIFY},
        {"file_sha256": sha_bytes(vb), "entry_name": "verification-b/" + FINAL_VERIFY},
        {"file_sha256": sha_bytes(va), "entry_name": "completion/" + FINAL_VERIFY},
        {"file_sha256": sha_bytes(receipt_raw), "entry_name": "completion/" + FINAL_RECEIPT},
    ]
    need(len(global_entries) == 22 and len({item["entry_name"] for item in global_entries}) == 22,
         "exact global manifest universe")
    manifest_raw = b"".join(
        f"{item['file_sha256']}  {item['entry_name']}\n".encode("ascii")
        for item in global_entries
    )
    need(parse_manifest_ordered(manifest_raw, "C79g global manifest") == global_entries,
         "exact ordered global manifest replay")
    exclusive(outdir / GLOBAL_MANIFEST, manifest_raw)
    replay_target_names = (
        *["build-a/" + name for name in CANDIDATE_MEMBERS],
        *["build-b/" + name for name in CANDIDATE_MEMBERS],
        "verification-a/" + FINAL_VERIFY,
        "verification-b/" + FINAL_VERIFY,
        "completion/" + FINAL_VERIFY,
        "completion/" + FINAL_RECEIPT,
        "completion/" + GLOBAL_MANIFEST,
        "completion/" + GLOBAL_OUTER,
    )
    need(len(replay_target_names) == 24 and len(set(replay_target_names)) == 24,
         "exact terminal replay universe")
    outer = close_object({
        "schema": SCHEMA + ".global-outer-receipt",
        "dual_completion_receipt_object_sha256": receipt["object_sha256"],
        "dual_completion_receipt_file_sha256": sha_bytes(receipt_raw),
        "global_manifest_file_sha256": sha_bytes(manifest_raw),
        "global_manifest_entry_count": 22,
        "global_manifest_entry_universe_sha256": digest(global_entries),
        "ordered_global_manifest_entries": global_entries,
        "both_candidate_surfaces_explicitly_bound": True,
        "both_verification_surfaces_explicitly_bound": True,
        "completion_receipt_explicitly_bound": True,
        "frozen_C79g_verifier_source_file_sha256": C79_FROZEN_VERIFIER_FILE_PIN,
        "exact_coherent_attack_count": 121,
        "unique_attack_names": attack_names,
        "dual_build_directory_required_mode": "0555",
        "dual_build_member_required_mode": "0444",
        "dual_build_member_single_link": True,
        "dual_build_corresponding_inodes_distinct": True,
        "verification_A_B_inodes_distinct": True,
        "one_final_global_manifest": True,
        "outer_receipt_published_last": True,
        "terminal_byte_replay_after_outer_receipt_required": True,
        "terminal_byte_replay_target_count": 24,
        "ordered_terminal_byte_replay_targets": list(replay_target_names),
        "completion_directory_sealed_mode_after_terminal_replay": "0555",
        "completion_member_required_mode": "0444",
        "strict_completion_mtime_order": [FINAL_VERIFY, FINAL_RECEIPT, GLOBAL_MANIFEST, GLOBAL_OUTER],
        "partial_publication_policy": "REJECT_AND_PRESERVE_NEVER_OVERWRITE_OR_REUSE",
        "completion_credit": dict(COMPLETED_CREDIT),
        "canonical_pointer_written": False,
        "D02_started": False,
    })
    need({path.name for path in outdir.iterdir()} == {FINAL_VERIFY, FINAL_RECEIPT, GLOBAL_MANIFEST},
         "completion surface immediately before outer")
    outer_raw = canonical(outer) + b"\n"
    exclusive(outdir / GLOBAL_OUTER, outer_raw)
    need({path.name for path in outdir.iterdir()} ==
         {FINAL_VERIFY, FINAL_RECEIPT, GLOBAL_MANIFEST, GLOBAL_OUTER},
         "completion surface exact after outer")
    mtimes = [(outdir / name).stat().st_mtime_ns
              for name in (FINAL_VERIFY, FINAL_RECEIPT, GLOBAL_MANIFEST, GLOBAL_OUTER)]
    need(mtimes == sorted(mtimes) and len(set(mtimes)) == 4,
         "verification/receipt/manifest/outer strict mtime order")

    replay_targets = (
        *[(build_a / name, sha_bytes(members[name])) for name in CANDIDATE_MEMBERS],
        *[(build_b / name, sha_bytes(members[name])) for name in CANDIDATE_MEMBERS],
        (verify_a, sha_bytes(va)),
        (verify_b, sha_bytes(vb)),
        (outdir / FINAL_VERIFY, sha_bytes(va)),
        (outdir / FINAL_RECEIPT, sha_bytes(receipt_raw)),
        (outdir / GLOBAL_MANIFEST, sha_bytes(manifest_raw)),
        (outdir / GLOBAL_OUTER, sha_bytes(outer_raw)),
    )
    need(len(replay_targets) == 24, "terminal replay target count")
    for path, expected_sha256 in replay_targets:
        replayed, _ = secure_snapshot(path, 0o444)
        need(sha_bytes(replayed) == expected_sha256, "post-outer terminal replay:" + str(path))
    os.chmod(outdir, 0o555)
    secure_directory(outdir, 0o555)


def parser() -> argparse.ArgumentParser:
    cli = argparse.ArgumentParser(description=__doc__)
    sub = cli.add_subparsers(dest="command", required=True)
    build_cmd = sub.add_parser("build")
    build_cmd.add_argument("--outdir", required=True, type=Path)
    complete_cmd = sub.add_parser("complete")
    complete_cmd.add_argument("--build-a", required=True, type=Path)
    complete_cmd.add_argument("--build-b", required=True, type=Path)
    complete_cmd.add_argument("--verification-a", required=True, type=Path)
    complete_cmd.add_argument("--verification-b", required=True, type=Path)
    complete_cmd.add_argument("--outdir", required=True, type=Path)
    return cli


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    # Mandatory first gate after argument parsing.  Do not move any read,
    # existence check, directory creation, or producer/verifier work above it.
    ensure_final_pins_filled()
    if args.command == "build":
        build(args.outdir)
    else:
        complete(args.build_a, args.build_b, args.verification_a, args.verification_b, args.outdir)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Reject as exc:
        print("REJECT:", exc, file=sys.stderr)
        raise SystemExit(2)
