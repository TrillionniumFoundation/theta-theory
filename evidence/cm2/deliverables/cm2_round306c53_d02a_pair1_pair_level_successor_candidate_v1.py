#!/usr/bin/env python3
"""Build a fail-closed pair-1, pair-level C46 shard-9 successor candidate.

The builder deliberately separates two predecessor relations:

* the local state-vector predecessor is the frozen C46 shard-9 generation-0
  checkpoint; and
* the global authority predecessor is the already installed C48 task-level
  authority seal.

It never writes runtime state.  A candidate is emitted only after the complete
C51 route object, the complete (not compact-only) C50a owner candidate/audit,
and a statically pinned C52 no-producer cold audit are all present and valid.
Until then ``--preflight`` reports a fail-closed blocker and ``--build``
rejects.  Even a successfully emitted object has zero formal/D02 credit; only
the separately guarded C53 no-replace seal can make the pair transition
authoritative.
"""

from __future__ import annotations

import argparse
import base64
import copy
from fractions import Fraction
import gzip
import hashlib
import json
import os
from pathlib import Path
import re
import stat
import sys
import tempfile
import types
from typing import Any, Iterable


sys.dont_write_bytecode = True
SELF = Path(__file__).absolute()
ROOT = SELF.parent.parent
DELIVERABLES = ROOT / "deliverables"
RUNTIME = ROOT / ".cm2-runtime"

SCHEMA = "cm2.round306c53.d02-a-pair1-pair-level-successor-candidate.v1"
CHECKPOINT_SCHEMA = SCHEMA + ".generation-1-successor-checkpoint"
TASK_STATE_SCHEMA = SCHEMA + ".successor-task-state"
EXIT_SCHEMA = SCHEMA + ".logical-exit-certificate"

HEX64 = re.compile(r"[0-9a-f]{64}\Z")
ZERO_LOCK = {
    "ambient_credit": 0,
    "terminal_credit": 0,
    "whole_parent_credit": 0,
    "D02_gate_credit": 0,
    "formal_credit": 0,
}

C46_SOURCE = DELIVERABLES / (
    "cm2_round306c46_d02a_general_adaptive_lower_strata_closure_engine_v1.py"
)
C46_SOURCE_SHA256 = "365432e96f2c287ef3c5497b7d15e01a80775f52d8cf5b71810d6f4c0e4442ea"
C46_PLAN_OBJECT_SHA256 = "7d004f59282dee21a28db0cd0b727a9045f4befce207c96be4efb07d1399c9bf"
SHARD_INDEX = 9
SHARD_ID = "c46-d02a-shard:0916976b9ec8a154268b3f290d1a4053ad47c8b8d41dbfe17d63cd0735c91095"
SHARD_TASK_COUNT = 589
SHARD_BINDING_SEQUENCE_SHA256 = "da4be1a51035b750b7981507f6ff74967bf7f441475286af7a1dc6fa0f6abcb7"
GENESIS_CHECKPOINT_OBJECT_SHA256 = "b962a7f05c99ff1e3fe2f2af98319f5e3cab005cca68b453d9152bf2435cacee"

PAIR = 1
TASKS = (
    {
        "index": 0,
        "task_binding_sha256": "daada4d9fd48677629cbfa9872b073d5fdf1552b115bf94438e7357f9a5dd95b",
        "root_path": "111111110",
        "frontier": ["0", "1"],
        "split_count": 1,
    },
    {
        "index": 1,
        "task_binding_sha256": "e37b527423ad1aabba7485faacd03f7bb95ba9d79caebd614fb63d38ccd8dac6",
        "root_path": "111111111",
        "frontier": ["00", "01", "10", "110", "1110", "11110", "11111"],
        "split_count": 6,
    },
)

C48_SEAL = RUNTIME / "c48-current-task-authority-seal"
C48_SEAL_FILE_SHA256 = "13a07654d2eba6b2f1072d4a6a70636a90437e1da18e0bbeb8630ab841e026c1"
C48_SEAL_OBJECT_SHA256 = "95297adbe0d2ee86788008046bc47c337a9c7a3fa0e46bd896e674a2931ec6b1"
C48_SUCCESSOR_OBJECT_SHA256 = "bbd909cad5a5d0b9cc44362be6acb26d527f86edc1b8191c06a246a514c9c984"
C48_SEAL_SCHEMA = (
    "cm2.round306c48.d02-a-pair668-generation1-successor-installer.v1."
    "authority-seal"
)
C48_SEAL_STATUS = (
    "COMMITTED_C48_PAIR668_GEN1_TASK_SUCCESSOR_AUTHORITY__ONE_AUDITED_"
    "TASK_LEVEL_SUCCESSOR__ZERO_D02_GATE_CREDIT"
)

C42_SEAL = RUNTIME / "c42-current-authority-seal"
C42_SEAL_FILE_SHA256 = "0e5a76059b2c9407340d88e07f4fcc356d376f5c24b7173e6b95fd5e06bc312d"
C42_SEAL_OBJECT_SHA256 = "b321552768a6aeae6c1d229e52b61ca0b4420314234e02e98366153d4156d460"
C42_SEAL_STATUS = "COMMITTED_C42_F1_AUTHORITY__574_PAIRED__1150_UNRESOLVED"
C42_SEAL_SCHEMA = "cm2.round306c42.f1-authority-commit-seal.v1"
C42_CENSUS = {
    "paired_coarse_cells": 574,
    "remaining_representatives": 575,
    "unresolved": 1_150,
    "whole_representatives": 287,
}

C51_SOURCE = DELIVERABLES / "cm2_round306c51_d02a_pair1_two_task_route_probe_v1.py"
C51_REPORT = DELIVERABLES / "cm2_round306c51_d02a_pair1_two_task_route_probe_report_v1.md"
C51_RESULT = DELIVERABLES / "cm2_round306c53_d02a_pair1_c51_frozen_route_result_v1.json"
C51_RESULT_FILE_SHA256 = "a560cdae560ce06879e3df3b0265aa97249d879011c7844394da73ea6fb32976"
C51_SOURCE_SHA256 = "caf043d2a475f8c25e92785587db971a0d33242b8560dd096f09a1e5c6e72069"
C51_REPORT_SHA256 = "d2330ac69da6cdb0e3fa092c9b697c836a21026ebb52b9b3655f9487a88f6330"
C51_OBJECT_SHA256 = "187344a3c524dce1898151bf64f507c181dde137a3710eb9bc5cd1b895a81f6e"
C51_STATUS = "PASS_PAIR1_TWO_TASK_DUAL_SIDE_STRICT_ROUTE_FRONTIERS_ZERO_CREDIT"

C50A_COMPACT_RESULT = DELIVERABLES / "cm2_round306c50a_pair1_two_task_global_owner_result_v1.json"
C50A_COMPACT_AUDIT = DELIVERABLES / (
    "cm2_round306c50a_pair1_two_task_global_owner_independent_verification_v1.json"
)
C50A_COMPACT_RESULT_FILE_SHA256 = "cdec578a1bc86a939b320676f59f859243eb7dc135f2fd5e5a727ac73f419241"
C50A_COMPACT_AUDIT_FILE_SHA256 = "b69457f93f982c73a850407d2d9f9fa5c39102b3ee6a23c5850e9428c0618f5c"
C50A_COMPACT_RESULT_OBJECT_SHA256 = "f16817bd52e954ba1e8135b1dbbdd11cfa0784acb1f7b7ad8d0f73bf78d1c2ed"
C50A_COMPACT_AUDIT_OBJECT_SHA256 = "d7d138bfb4c49f0a43db7f43103e51fe3441475ad2244b9d8233762acf7e8ac0"
C50A_FULL_RESULT = DELIVERABLES / "cm2_round306c50a_pair1_two_task_global_owner_full_candidate_v1.json.gz.b64"
C50A_FULL_AUDIT = DELIVERABLES / "cm2_round306c50a_pair1_two_task_global_owner_full_independent_audit_v1.json.gz.b64"
C50A_MANIFEST = DELIVERABLES / "cm2_round306c50a_global_codimension_owner_oracle_manifest_v1.sha256"
C50A_MANIFEST_FILE_SHA256 = "07444544362d8b25d7d5d735e17ad08057dfc459d166ade868a073c2ce4c50f6"
C50A_FULL_RESULT_ENCODED_SHA256 = "3a747cc92700bccc763d6cbf71ece51ebf5d3f5709b330a768c089099025174a"
C50A_FULL_RESULT_GZIP_SHA256 = "8cae20c2d26c1e4d8113f39687da4f05908c13f1fb7722fd1f035c2c2c50db15"
C50A_FULL_RESULT_FILE_SHA256 = "0c3ffd0a9ff26fd128366a6af22aabeb29f72346303988deb4773b5adcd4131e"
C50A_FULL_RESULT_OBJECT_SHA256 = "da4557c64b4ce9675a3f8bff8a250b7ec7b643c48aecd738c03b7abed01d0b82"
C50A_FULL_RESULT_STATUS = (
    "PASS_C50A_GENERIC_TWO_SIDE_HISTORY_BOUND_FULL_UNIVERSE_OWNER_ORACLE__"
    "ZERO_FORMAL_CREDIT"
)
C50A_FULL_AUDIT_ENCODED_SHA256 = "71102222dd9d8ffe7c21675447405fd65709e0a46122fd5a428326a076838f85"
C50A_FULL_AUDIT_GZIP_SHA256 = "a7b860fbf49444aacfc350f12371c6751dfa1ed7b8c39434a587b0dfa763f56c"
C50A_FULL_AUDIT_FILE_SHA256 = "5068afb70ec8bf7fddc719324aeae4703fbc4e22d07a9b5555e348471c23dd66"
C50A_FULL_AUDIT_OBJECT_SHA256 = "c037b3b15d19b839a254e3122bce7b1f882f6f9e198638c50a08909bf71231d6"
C50A_FULL_AUDIT_STATUS = (
    "PASS_INDEPENDENT_C50A_GENERIC_HISTORY_BOUND_FULL_UNIVERSE_OWNER_ORACLE__"
    "ZERO_FORMAL_CREDIT"
)
C50A_REQUEST_OBJECT_SHA256 = "db6292e002ec3c0b810f74af192524407afb1cfa3566c4898aa7fa7b2a8e3496"
C50A_HISTORY_HEAD_SHA256 = "543e2289de5a465745f821f510efa62ea2d4985921e2649b7404665ae71c730f"

C52_AUDIT = DELIVERABLES / "cm2_round306c52_d02a_pair1_no_producer_cold_route_audit_v1.json"
C52_SCHEMA = "cm2.round306c52.d02-a-pair1-no-producer-cold-route-audit.v1"
C52_STATUS = (
    "PASS_C52_PAIR1_NO_PRODUCER_IMPORT_COLD_INDEPENDENT_ROUTE_MARGIN_"
    "REFLECTION_KRAFT_AND_CANDIDATE_REQUEST_AUDIT__ZERO_CREDIT"
)
C52_VERIFIER_SOURCE_SHA256 = "6f7ab24f0439b2965e2f406cd9ee2e5078cd43020763a8b658fedf2bd34caeff"
C52_AUDIT_FILE_SHA256 = "ff4ffe3862722d2ff6a00829cc4fb5f2e0ce691e823bd0f6f1918d783f7c7203"
C52_AUDIT_OBJECT_SHA256 = "1667032a6fbbc56cd53983275d8203c2480a2d31c3d4dc3f39b7efaed77ccec4"

C50D_PROTOCOL = DELIVERABLES / "cm2_round306c50d_global_successor_cas_protocol_freeze_v1.md"
C50D_PROTOCOL_COMPANION = DELIVERABLES / (
    "cm2_round306c50d_global_successor_cas_protocol_freeze_v1.md.sha256"
)
C50D_PROTOCOL_FILE_SHA256 = "46a1a0a78970a6219b5a03bf9b91820b9121f4e409a46adcbb0c2ef793eeaf86"
C50D_PROTOCOL_COMPANION_FILE_SHA256 = "d34e35ee41798700699addd02555d32ff6608204db99a869b8ba303cc9784c5a"
C50D_PREDECESSOR_IDENTITY_SCHEMA = "cm2.global-authority-predecessor-identity.v1"
C50D_CLAIM_SCHEMA = "cm2.global-authority-predecessor-consumption-claim.v1"
C50D_LEGACY_PREDECESSOR_IDENTITY_SHA256 = (
    "10fb050d30c92b0f2bdcf85a30d28ff670d8efc0b48104b7f04a63c391967b41"
)
GLOBAL_CLAIM_NAMESPACE = "cm2-global-successor-claims"
GLOBAL_HEAD_NAMESPACE = "cm2-global-authority-heads"

BEFORE = {
    "logical_pending_task_count": 33_640,
    "two_side_pending_occurrence_count": 67_280,
    "paired_coarse_cells": 574,
    "unresolved_coarse_cells": 1_150,
    "representative_parents_remaining": 575,
}
AFTER_IF_SEALED = {
    "logical_pending_task_count": 33_638,
    "two_side_pending_occurrence_count": 67_276,
    "paired_coarse_cells": 576,
    "unresolved_coarse_cells": 1_148,
    "representative_parents_remaining": 574,
}
D02_FORMAL_CENSUS_BEFORE = {
    "four_class_cell_census": {
        "strict_exclusions": 75_386,
        "typed_events": 296,
        "connected_components": 0,
        "cemetery_or_disconnected_exteriors": 0,
        "unresolved": 1_150,
        "total": 76_832,
    },
    "representative_parent_census": {
        "terminal_representatives": 287,
        "total_representatives": 862,
        "paired_coarse_cells": 574,
        "remaining_representatives": 575,
    },
}
D02_FORMAL_CENSUS_AFTER_IF_SEALED = {
    "four_class_cell_census": {
        "strict_exclusions": 75_388,
        "typed_events": 296,
        "connected_components": 0,
        "cemetery_or_disconnected_exteriors": 0,
        "unresolved": 1_148,
        "total": 76_832,
    },
    "representative_parent_census": {
        "terminal_representatives": 288,
        "total_representatives": 862,
        "paired_coarse_cells": 576,
        "remaining_representatives": 574,
    },
}
C50D_BEFORE_CENSUS = {
    "logical_pending_task_count": 33_640,
    "paired_coarse_cells": 574,
    "representative_parents_remaining": 575,
    "two_side_pending_occurrence_count": 67_280,
    "unresolved_coarse_cells": 1_150,
    "whole_representative_parent_count": 287,
}
C50D_AFTER_CENSUS_IF_SEALED = {
    "logical_pending_task_count": 33_638,
    "paired_coarse_cells": 576,
    "representative_parents_remaining": 574,
    "two_side_pending_occurrence_count": 67_276,
    "unresolved_coarse_cells": 1_148,
    "whole_representative_parent_count": 288,
}


class Reject(RuntimeError):
    pass


def need(condition: bool, label: str) -> None:
    if type(condition) is not bool or not condition:
        raise Reject(label)


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
        need(type(value) is str, "sequence member string")
        state.update(value.encode("ascii") + b"\n")
    return state.hexdigest()


def file_digest(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def fingerprint(info: os.stat_result) -> tuple[int, ...]:
    return (
        info.st_dev, info.st_ino, info.st_mode, info.st_nlink, info.st_uid,
        info.st_gid, info.st_size, info.st_mtime_ns, info.st_ctime_ns,
    )


def object_digest(value: dict[str, Any], field: str = "object_sha256") -> str:
    body = dict(value)
    need(field in body, "self-hash field present:" + field)
    body.pop(field)
    return digest(body)


def close_object(value: dict[str, Any], field: str) -> dict[str, Any]:
    need(field not in value, "fresh self-hash field:" + field)
    return {**value, field: digest(value)}


def stable_read(path: Path, label: str, maximum: int = 1 << 30) -> bytes:
    path = path.absolute()
    need(ROOT == path or ROOT in path.parents, label + ": workspace path")
    cursor = ROOT
    for part in path.relative_to(ROOT).parts[:-1]:
        cursor /= part
        need(not stat.S_ISLNK(os.lstat(cursor).st_mode), label + ": no symlink parent")
    fd = os.open(path, os.O_RDONLY | os.O_CLOEXEC | os.O_NOFOLLOW)
    try:
        before = os.fstat(fd)
        need(
            stat.S_ISREG(before.st_mode) and before.st_nlink == 1
            and before.st_uid == os.getuid() and 0 < before.st_size <= maximum,
            label + ": owned singleton bounded regular file",
        )
        chunks: list[bytes] = []
        remaining = before.st_size
        while remaining:
            block = os.read(fd, min(4 << 20, remaining))
            need(bool(block), label + ": no short read")
            chunks.append(block)
            remaining -= len(block)
        need(os.read(fd, 1) == b"", label + ": stable EOF")
        after = os.fstat(fd)
        path_info = os.stat(path, follow_symlinks=False)
    finally:
        os.close(fd)
    key = lambda row: (
        row.st_dev, row.st_ino, row.st_mode, row.st_nlink, row.st_uid,
        row.st_gid, row.st_size, row.st_mtime_ns, row.st_ctime_ns,
    )
    need(key(before) == key(after) == key(path_info), label + ": stable identity")
    return b"".join(chunks)


class HeldSourceCapture:
    """Hold source identity and bytes across compile, exec, and use."""

    def __init__(
        self, path: Path, label: str, expected: str | None, *,
        workspace_only: bool = True, maximum: int = 8 << 20,
    ):
        if expected is not None:
            need(HEX64.fullmatch(expected) is not None,
                 label + ": complete source pin")
        self.path = path.absolute()
        self.label = label
        if workspace_only:
            need(ROOT == self.path or ROOT in self.path.parents,
                 label + ": workspace source path")
        self.fd = os.open(self.path, os.O_RDONLY | os.O_CLOEXEC | os.O_NOFOLLOW)
        self.before = os.fstat(self.fd)
        need(
            stat.S_ISREG(self.before.st_mode) and self.before.st_nlink == 1
            and self.before.st_uid == os.getuid()
            and 0 < self.before.st_size <= maximum,
            label + ": owned singleton bounded source",
        )
        self.raw = self._read()
        self.sha256 = file_digest(self.raw)
        if expected is not None:
            need(self.sha256 == expected, label + ": source SHA-256")
        self.unchanged("initial")

    def _read(self) -> bytes:
        os.lseek(self.fd, 0, os.SEEK_SET)
        chunks: list[bytes] = []
        while block := os.read(self.fd, 1 << 20):
            chunks.append(block)
        return b"".join(chunks)

    def unchanged(self, phase: str) -> None:
        path_info = os.stat(self.path, follow_symlinks=False)
        need(
            fingerprint(path_info) == fingerprint(os.fstat(self.fd))
            == fingerprint(self.before),
            self.label + ": " + phase + " stable identity",
        )
        need(self._read() == self.raw,
             self.label + ": " + phase + " stable bytes")

    def close(self) -> None:
        os.close(self.fd)


def json_document(raw: bytes, label: str, *, canonical_line: bool) -> dict[str, Any]:
    need(b"\x00" not in raw and not raw.startswith(b"\xef\xbb\xbf"),
         label + ": byte hygiene")

    def pairs(items: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in items:
            need(key not in result, label + ": duplicate key:" + key)
            result[key] = value
        return result

    def no_noninteger(token: str) -> Any:
        raise Reject(label + ": noninteger JSON number:" + token)

    value = json.loads(
        raw.decode("utf-8", "strict"), object_pairs_hook=pairs,
        parse_float=no_noninteger, parse_constant=no_noninteger,
    )
    need(type(value) is dict, label + ": JSON object")
    if canonical_line:
        need(raw == canonical(value) + b"\n", label + ": canonical JSON newline")
    return value


def strict_json(raw: bytes, label: str) -> dict[str, Any]:
    return json_document(raw, label, canonical_line=True)


def captured_json(
    path: Path, label: str, expected_file: str | None = None, *,
    canonical_line: bool = True,
) -> tuple[bytes, dict[str, Any]]:
    raw = stable_read(path, label)
    if expected_file is not None:
        need(HEX64.fullmatch(expected_file) is not None, label + ": frozen file pin")
        need(file_digest(raw) == expected_file, label + ": file SHA-256")
    return raw, json_document(raw, label, canonical_line=canonical_line)


def closed(value: dict[str, Any], expected: str, label: str) -> None:
    need(HEX64.fullmatch(expected) is not None, label + ": frozen object pin")
    need(value.get("object_sha256") == expected, label + ": object pin")
    need(object_digest(value) == expected, label + ": object self-hash")


def prefix_free(paths: list[str]) -> bool:
    return (
        len(paths) == len(set(paths))
        and all(type(path) is str and set(path) <= {"0", "1"} for path in paths)
        and not any(right.startswith(left) for left in paths for right in paths if left != right)
    )


def kraft(paths: list[str]) -> Fraction:
    return sum((Fraction(1, 2 ** len(path)) for path in paths), Fraction(0))


def validate_c48() -> dict[str, Any]:
    _raw, seal = captured_json(C48_SEAL, "installed C48 seal", C48_SEAL_FILE_SHA256)
    need(
        seal.get("authority_seal_object_sha256") == C48_SEAL_OBJECT_SHA256
        and object_digest(seal, "authority_seal_object_sha256") == C48_SEAL_OBJECT_SHA256,
        "C48 authority seal self-hash",
    )
    need(
        seal.get("status") == C48_SEAL_STATUS
        and seal.get("successor_checkpoint_object_sha256") == C48_SUCCESSOR_OBJECT_SHA256
        and seal.get("coarse_formal_authority_unchanged") == {
            "paired_coarse_cells": 574,
            "unresolved_coarse_cells": 1_150,
            "representative_parents_remaining": 575,
        },
        "C48 exact logical predecessor scope",
    )
    return seal


def validate_c42() -> dict[str, Any]:
    _raw, seal = captured_json(C42_SEAL, "installed C42 seal", C42_SEAL_FILE_SHA256)
    need(
        seal.get("authority_seal_object_sha256") == C42_SEAL_OBJECT_SHA256
        and object_digest(seal, "authority_seal_object_sha256")
        == C42_SEAL_OBJECT_SHA256
        and seal.get("status") == C42_SEAL_STATUS
        and seal.get("formal_census_after_commit") == C42_CENSUS,
        "C42 exact installed formal authority/census",
    )
    return seal


def validate_route(path: Path) -> dict[str, Any]:
    need(file_digest(stable_read(C51_SOURCE, "C51 source", 4 << 20)) == C51_SOURCE_SHA256,
         "C51 source pin")
    need(file_digest(stable_read(C51_REPORT, "C51 report", 4 << 20)) == C51_REPORT_SHA256,
         "C51 report pin")
    _raw, route = captured_json(
        path, "C51 complete route result", C51_RESULT_FILE_SHA256
    )
    closed(route, C51_OBJECT_SHA256, "C51 route")
    need(
        route.get("schema") == "cm2.round306c51.d02-a-pair1-two-task-route-probe.v1"
        and route.get("status") == C51_STATUS
        and route.get("source_sha256") == C51_SOURCE_SHA256
        and route.get("C46_plan_object_sha256") == C46_PLAN_OBJECT_SHA256
        and route.get("pair_index") == PAIR and route.get("task_count") == 2
        and route.get("both_tasks_route_closed") is True
        and route.get("prefix_free_and_Kraft_one_for_both_tasks") is True
        and route.get("runtime_writes_performed") is False
        and route.get("formal_credit") == route.get("D02_gate_credit") == 0,
        "C51 route exact scope",
    )
    probes = route.get("task_probes")
    need(type(probes) is list and len(probes) == 2, "C51 exact two probes")
    for probe, expected in zip(probes, TASKS, strict=True):
        body = dict(probe)
        observed_hash = body.pop("task_probe_object_sha256", None)
        paths = probe.get("frontier_paths")
        terminal = probe.get("dual_side_terminal_rows")
        need(
            observed_hash == digest(body)
            and probe.get("task_binding_sha256") == expected["task_binding_sha256"]
            and probe.get("pair_index") == PAIR
            and probe.get("root_path") == expected["root_path"]
            and probe.get("split_count") == expected["split_count"]
            and paths == expected["frontier"] and prefix_free(paths) and kraft(paths) == 1
            and probe.get("relative_Kraft_sum") == "1"
            and probe.get("all_frontier_leaves_dual_side_strict_terminal") is True
            and probe.get("candidate_route_closure_only") is True
            and probe.get("global_codimension_owner_oracle_applied") is False
            and probe.get("formal_credit") == probe.get("D02_gate_credit") == 0
            and type(terminal) is list and len(terminal) == len(paths),
            "C51 task probe exact route/frontier:" + str(expected["index"]),
        )
        for logical in terminal:
            sides = logical.get("physical_sides")
            need(
                logical.get("relative_path") in paths and type(sides) is list
                and [row.get("side") for row in sides] == ["REPRESENTATIVE", "REFLECTED"]
                and all(
                    row.get("relative_path") == logical["relative_path"]
                    and row.get("terminal_classification")
                    == "EXCLUDED_C40_COLLISION2_OWNER_MISMATCH"
                    and row.get("all_required_strict_margins_complete") is True
                    and row.get("formal_credit") == 0
                    and type(row.get("physical_leaf_id")) is str
                    and HEX64.fullmatch(row.get("leaf_object_sha256", "")) is not None
                    for row in sides
                ),
                "C51 exact dual-side strict terminal row",
            )
    need(sum(row["frontier_leaf_count"] for row in probes) == 9,
         "C51 nine logical leaves")
    return route


def validate_owner_wrappers() -> tuple[dict[str, Any], dict[str, Any]]:
    manifest = stable_read(C50A_MANIFEST, "C50a immutable manifest", 1 << 20)
    need(file_digest(manifest) == C50A_MANIFEST_FILE_SHA256,
         "C50a immutable manifest file pin")
    manifest_text = manifest.decode("ascii", "strict").splitlines()
    need(
        len(manifest_text) == 8
        and (C50A_FULL_RESULT_ENCODED_SHA256 + "  deliverables/" + C50A_FULL_RESULT.name)
        in manifest_text
        and (C50A_FULL_AUDIT_ENCODED_SHA256 + "  deliverables/" + C50A_FULL_AUDIT.name)
        in manifest_text,
        "C50a manifest exact full-byte bundle entries",
    )
    _raw, result = captured_json(
        C50A_COMPACT_RESULT, "C50a compact owner binding",
        C50A_COMPACT_RESULT_FILE_SHA256, canonical_line=False,
    )
    _raw, audit = captured_json(
        C50A_COMPACT_AUDIT, "C50a compact audit binding",
        C50A_COMPACT_AUDIT_FILE_SHA256, canonical_line=False,
    )
    closed(result, C50A_COMPACT_RESULT_OBJECT_SHA256, "C50a compact result")
    closed(audit, C50A_COMPACT_AUDIT_OBJECT_SHA256, "C50a compact audit")
    full = result.get("full_candidate", {})
    replay = result.get("replay_census", {})
    bindings = result.get("frozen_bindings", {})
    need(
        result.get("status")
        == "PASS_PAIR1_TWO_TASK_GLOBAL_OWNER_FULL_RESULT_REPLAYED_AND_INDEPENDENTLY_VERIFIED__COMPACT_BINDING__ZERO_FORMAL_CREDIT"
        and full.get("file_sha256") == C50A_FULL_RESULT_FILE_SHA256
        and full.get("object_sha256") == C50A_FULL_RESULT_OBJECT_SHA256
        and full.get("request_object_sha256") == C50A_REQUEST_OBJECT_SHA256
        and full.get("status") == C50A_FULL_RESULT_STATUS
        and full.get("replay_required_for_full_rows") is True
        and bindings.get("C51_pair1_probe_object_sha256") == C51_OBJECT_SHA256
        and bindings.get("history_head_sha256") == C50A_HISTORY_HEAD_SHA256
        and replay.get("transaction_count") == 2
        and replay.get("logical_leaf_count") == 9
        and replay.get("target_physical_occurrence_count") == 18
        and replay.get("final_overlay_occurrence_count") == 183_772
        and replay.get("face_atom_count") == 52
        and replay.get("corner_entity_count") == 36
        and replay.get("all_face_atoms_degree_two") is True
        and replay.get("all_face_incident_sets_complete") is True
        and replay.get("all_corner_four_quadrant_germs_complete") is True
        and replay.get("all_codimension_owners_unique") is True
        and result.get("formal_credit") == 0,
        "C50a compact result exact full-owner binding",
    )
    full_audit = audit.get("full_audit", {})
    independent = audit.get("independent_replay", {})
    need(
        audit.get("status")
        == "PASS_INDEPENDENT_PAIR1_C50A_GLOBAL_OWNER_REPLAY__COMPACT_BINDING__ZERO_FORMAL_CREDIT"
        and full_audit.get("file_sha256") == C50A_FULL_AUDIT_FILE_SHA256
        and full_audit.get("object_sha256") == C50A_FULL_AUDIT_OBJECT_SHA256
        and full_audit.get("status") == C50A_FULL_AUDIT_STATUS
        and full_audit.get("candidate_file_sha256") == C50A_FULL_RESULT_FILE_SHA256
        and full_audit.get("candidate_object_sha256") == C50A_FULL_RESULT_OBJECT_SHA256
        and full_audit.get("request_object_sha256") == C50A_REQUEST_OBJECT_SHA256
        and independent.get("C50a_producer_imported_or_executed") is False
        and independent.get("C48_C41_C32_producers_imported_or_executed") is False
        and independent.get("frozen_ledgers_parsed_directly") is True
        and independent.get("transaction_count") == 2
        and independent.get("target_occurrence_count") == 18
        and independent.get("final_overlay_occurrence_count") == 183_772
        and independent.get("face_atom_count") == 52
        and independent.get("corner_entity_count") == 36
        and independent.get("all_codimension_owners_unique") is True
        and audit.get("formal_credit") == 0,
        "C50a compact audit exact independent binding",
    )
    return result, audit


def validate_full_owner(result_path: Path, audit_path: Path) -> tuple[dict[str, Any], dict[str, Any]]:
    def decode_bundle(
        path: Path, label: str, encoded_sha: str, gzip_sha: str,
        json_sha: str,
    ) -> tuple[bytes, dict[str, Any]]:
        encoded = stable_read(path, label + " base64 bundle", 1 << 30)
        need(file_digest(encoded) == encoded_sha, label + ": encoded file SHA-256")
        try:
            need(all(
                byte in b"ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=\r\n\t "
                for byte in encoded
            ), label + ": base64 alphabet/whitespace")
            compressed = base64.b64decode(b"".join(encoded.split()), validate=True)
        except Exception as error:
            raise Reject(label + ": strict base64:" + str(error)) from error
        need(file_digest(compressed) == gzip_sha, label + ": decoded gzip SHA-256")
        try:
            raw = gzip.decompress(compressed)
        except Exception as error:
            raise Reject(label + ": strict gzip:" + str(error)) from error
        need(0 < len(raw) <= (1 << 30), label + ": decompressed bound")
        need(file_digest(raw) == json_sha, label + ": decompressed JSON SHA-256")
        return raw, strict_json(raw, label + " decompressed JSON")

    _raw, result = decode_bundle(
        result_path, "C50a full owner candidate", C50A_FULL_RESULT_ENCODED_SHA256,
        C50A_FULL_RESULT_GZIP_SHA256, C50A_FULL_RESULT_FILE_SHA256,
    )
    _raw, audit = decode_bundle(
        audit_path, "C50a full owner audit", C50A_FULL_AUDIT_ENCODED_SHA256,
        C50A_FULL_AUDIT_GZIP_SHA256, C50A_FULL_AUDIT_FILE_SHA256,
    )
    closed(result, C50A_FULL_RESULT_OBJECT_SHA256, "C50a full owner candidate")
    closed(audit, C50A_FULL_AUDIT_OBJECT_SHA256, "C50a full owner audit")
    need(
        result.get("schema") == "cm2.round306c50a.global-codimension-owner-oracle.v1"
        and result.get("status") == C50A_FULL_RESULT_STATUS
        and result.get("formal_credit") == 0,
        "C50a full candidate status/scope",
    )
    need(
        audit.get("schema")
        == "cm2.round306c50a.global-codimension-owner-oracle.independent-verifier.v1"
        and audit.get("status") == C50A_FULL_AUDIT_STATUS
        and audit.get("formal_credit") == 0,
        "C50a full audit status/scope",
    )
    audit_candidate = audit.get("candidate", {})
    replay = audit.get("replay", {})
    independence = audit.get("independence_boundary", {})
    immutability = audit.get("immutability", {})
    need(
        audit_candidate.get("file_sha256") == C50A_FULL_RESULT_FILE_SHA256
        and audit_candidate.get("object_sha256") == C50A_FULL_RESULT_OBJECT_SHA256
        and audit_candidate.get("request_object_sha256") == C50A_REQUEST_OBJECT_SHA256
        and replay.get("transaction_count") == 2
        and replay.get("target_occurrence_count") == 18
        and replay.get("final_overlay_occurrence_count") == 183_772
        and replay.get("face_atom_count") == 52
        and replay.get("corner_entity_count") == 36
        and replay.get("all_codimension_owners_unique") is True
        and replay.get("history_head_sha256") == C50A_HISTORY_HEAD_SHA256
        and independence.get("C50a_producer_imported_or_executed") is False
        and independence.get("C48_C41_C32_producers_imported_or_executed") is False
        and independence.get("frozen_ledgers_parsed_directly") is True
        and independence.get("full_universe_reconstructed_twice_in_opposite_traversal_orders") is True
        and immutability.get("candidate_identity_replay_equal") is True
        and immutability.get("candidate_terminal_byte_replay_equal") is True
        and immutability.get("pre_post_snapshot_equal") is True,
        "C50a full independent audit exact replay/immutability",
    )
    return result, audit


def validate_route_owner_mapping(
    route: dict[str, Any], owner: dict[str, Any], owner_audit: dict[str, Any],
) -> dict[str, Any]:
    """Bind every C51 physical leaf to one C50a replacement/occurrence.

    Top hashes and aggregate booleans are insufficient here.  This replay
    checks all 18 replacement rows, then follows every replacement into the
    history overlay and the complete face/corner owner ledgers.
    """
    request = owner.get("request")
    need(type(request) is dict, "C50a embedded request object")
    request_body = dict(request)
    request_hash = request_body.pop("request_object_sha256", None)
    need(
        request_hash == C50A_REQUEST_OBJECT_SHA256
        and digest(request_body) == C50A_REQUEST_OBJECT_SHA256
        and owner.get("request_object_sha256") == C50A_REQUEST_OBJECT_SHA256,
        "C50a embedded request self-hash",
    )
    transactions = request.get("transactions")
    need(type(transactions) is list and len(transactions) == 2,
         "C50a exact two transactions")
    mapping_rows: list[dict[str, Any]] = []
    replacement_rows: list[dict[str, Any]] = []
    for probe, transaction, expected in zip(
        route["task_probes"], transactions, TASKS, strict=True
    ):
        tx_body = dict(transaction)
        tx_hash = tx_body.pop("transaction_binding_sha256", None)
        task = transaction.get("task", {})
        replacements = transaction.get("replacements")
        need(
            tx_hash == digest(tx_body)
            and transaction.get("transaction_index") == expected["index"]
            and transaction.get("relative_frontier") == expected["frontier"]
            and task.get("upstream_task_binding_sha256")
            == expected["task_binding_sha256"]
            and task.get("pair_index") == PAIR
            and task.get("root_semantic_path") == expected["root_path"]
            and type(replacements) is list
            and len(replacements) == 2 * len(expected["frontier"]),
            "C50a transaction exact C51 task binding:" + str(expected["index"]),
        )
        c51_leaves = {
            (leaf["side"], logical["relative_path"]): leaf
            for logical in probe["dual_side_terminal_rows"]
            for leaf in logical["physical_sides"]
        }
        need(len(c51_leaves) == len(replacements),
             "C51/C50a replacement key census")
        split_root = sequence_digest(
            event["split_object_sha256"] for event in probe["split_events"]
        )
        for replacement in replacements:
            key = (replacement.get("side"), replacement.get("relative_path"))
            need(key in c51_leaves, "C50a replacement has exact C51 leaf key")
            leaf = c51_leaves[key]
            evidence = replacement.get("source_evidence", {})
            expected_fraction = str(Fraction(1, 2 ** len(leaf["relative_path"])))
            need(
                replacement.get("semantic_path")
                == expected["root_path"] + leaf["relative_path"]
                and replacement.get("physical_route_path")
                == leaf["physical_route_path"]
                and replacement.get("physical_cell_id") == leaf["physical_cell_id"]
                and replacement.get("exact_closed_box") == leaf["exact_closed_box"]
                and replacement.get("relative_parent_fraction") == expected_fraction
                and evidence.get("source_schema") == probe["schema"]
                and evidence.get("source_task_probe_object_sha256")
                == probe["task_probe_object_sha256"]
                and evidence.get("source_split_event_sequence_sha256") == split_root
                and evidence.get("source_physical_leaf_id") == leaf["physical_leaf_id"]
                and evidence.get("source_leaf_object_sha256")
                == leaf["leaf_object_sha256"]
                and evidence.get("source_compact_leaf_row_sha256") == digest(leaf)
                and evidence.get("terminal_classification")
                == leaf["terminal_classification"]
                and evidence.get("all_required_strict_margins_complete") is True
                and evidence.get("formal_credit") == 0,
                "C51 leaf to C50a replacement exact row binding",
            )
            replacement_rows.append(replacement)
            mapping_rows.append({
                "task_binding_sha256": expected["task_binding_sha256"],
                "transaction_binding_sha256": tx_hash,
                "side": leaf["side"],
                "relative_path": leaf["relative_path"],
                "physical_leaf_id": leaf["physical_leaf_id"],
                "leaf_object_sha256": leaf["leaf_object_sha256"],
                "compact_leaf_row_sha256": digest(leaf),
            })

    history = owner.get("history_replay", {})
    nodes = history.get("history_nodes")
    need(
        history.get("transaction_count") == 2
        and history.get("history_head_sha256") == C50A_HISTORY_HEAD_SHA256
        and type(nodes) is list and len(nodes) == 2,
        "C50a two-node history replay",
    )
    inserted_ids: list[str] = []
    prior_history_head = history.get("genesis_sha256")
    need(
        prior_history_head == request.get("history_genesis_sha256"),
        "C50a history replay/request genesis binding",
    )
    for node, transaction in zip(nodes, transactions, strict=True):
        need(set(node) == {
            "schema", "history_protocol_version",
            "active_universe_binding_sha256", "transaction_index",
            "parent_history_sha256", "transaction_binding_sha256",
            "oracle_task_binding_sha256", "split_decision_sequence_sha256",
            "removed_occurrence_id_sequence_sha256",
            "inserted_occurrence_id_sequence_sha256",
            "resulting_overlay_occurrence_binding_sequence_sha256",
            "resulting_overlay_occurrence_count", "history_node_sha256",
            "removed_occurrence_ids", "inserted_occurrence_ids",
        }, "C50a exact history-node fields")
        # The producer hashes the semantic history body first, then appends the
        # two explicit ID arrays as replay witnesses.  Recompute that exact
        # pre-append body rather than treating the post-hash witnesses as hash
        # inputs.
        node_body = {
            key: value for key, value in node.items()
            if key not in {
                "history_node_sha256", "removed_occurrence_ids",
                "inserted_occurrence_ids",
            }
        }
        node_hash = node.get("history_node_sha256")
        need(
            node_hash == digest(node_body)
            and node.get("transaction_binding_sha256")
            == transaction["transaction_binding_sha256"]
            and node.get("transaction_index") == transaction["transaction_index"]
            and node.get("parent_history_sha256") == prior_history_head
            and node.get("removed_occurrence_id_sequence_sha256")
            == sequence_digest(node["removed_occurrence_ids"])
            and node.get("inserted_occurrence_id_sequence_sha256")
            == sequence_digest(node["inserted_occurrence_ids"])
            and len(node["removed_occurrence_ids"]) == 2
            and len(node["inserted_occurrence_ids"])
            == len(transaction["replacements"]),
            "C50a history node exact transaction/insertions",
        )
        inserted_ids.extend(node["inserted_occurrence_ids"])
        prior_history_head = node_hash
    need(prior_history_head == C50A_HISTORY_HEAD_SHA256,
         "C50a chained history terminal head")
    inserted = set(inserted_ids)
    need(len(inserted_ids) == len(inserted) == 18,
         "C50a 18 unique inserted target occurrences")
    target_replay = owner.get("target_replay", {})
    need(
        target_replay.get("target_occurrence_count") == 18
        and target_replay.get("target_occurrence_id_sequence_sha256")
        == sequence_digest(sorted(inserted)),
        "C50a target occurrence exact inserted set",
    )

    ledger = owner.get("owner_ledger", {})
    faces = ledger.get("face_atoms")
    corners = ledger.get("corner_entities")
    need(type(faces) is list and len(faces) == 52
         and type(corners) is list and len(corners) == 36,
         "C50a complete owner ledger row census")
    face_refs: list[str] = []
    corner_refs: list[str] = []
    target_records: dict[str, dict[str, Any]] = {}
    core_fields = (
        "physical_occurrence_id", "pair_index", "side", "semantic_path",
        "physical_route_path", "physical_cell_id", "relative_path",
        "upstream_task_binding_sha256", "transaction_binding_sha256",
        "source_kind",
    )

    def retain(row: dict[str, Any]) -> None:
        occurrence_id = row.get("physical_occurrence_id")
        if occurrence_id not in inserted:
            return
        compact = {field: row.get(field) for field in core_fields}
        prior = target_records.setdefault(occurrence_id, compact)
        need(prior == compact, "target occurrence consistent across owner ledgers")

    for face in faces:
        need(
            face.get("incident_set_complete") is True
            and face.get("owner_unique") is True
            and face.get("incident_occurrence_count") == 2
            and face.get("geometric_side_counts")
            == {"LOWER_COORDINATE_SIDE": 1, "UPPER_COORDINATE_SIDE": 1},
            "C50a face row complete unique degree two",
        )
        for row in face["incident_occurrences"]:
            retain(row)
        face_refs.extend(
            ref["target_occurrence_id"]
            for ref in face["target_occurrence_face_references"]
        )
    for corner in corners:
        need(
            corner.get("incident_set_complete") is True
            and corner.get("owner_unique") is True
            and corner.get("four_quadrant_germ_complete") is True,
            "C50a corner row complete unique four-quadrant",
        )
        for row in corner["incident_occurrences"]:
            retain(row)
        corner_refs.extend(corner["target_corner_occurrence_ids"])
    need(
        len(face_refs) == ledger.get("target_face_atom_occurrence_count") == 78
        and len(corner_refs) == ledger.get("target_corner_occurrence_count") == 72
        and set(face_refs) == set(corner_refs) == inserted
        and set(target_records) == inserted,
        "every target occurrence covered by complete face/corner ledgers",
    )
    face_counts = {value: face_refs.count(value) for value in inserted}
    corner_counts = {value: corner_refs.count(value) for value in inserted}
    need(
        sorted(face_counts.values()) == [4] * 12 + [5] * 6
        and set(corner_counts.values()) == {4},
        "per-occurrence 78-face/72-corner reference distribution",
    )

    by_key: dict[tuple[Any, ...], str] = {}
    for occurrence_id, row in target_records.items():
        key = (
            row["upstream_task_binding_sha256"], row["side"],
            row["relative_path"], row["physical_route_path"],
            row["physical_cell_id"], row["semantic_path"],
        )
        need(key not in by_key, "target occurrence unique route key")
        by_key[key] = occurrence_id
    for mapping, replacement in zip(mapping_rows, replacement_rows, strict=True):
        key = (
            mapping["task_binding_sha256"], replacement["side"],
            replacement["relative_path"], replacement["physical_route_path"],
            replacement["physical_cell_id"], replacement["semantic_path"],
        )
        need(key in by_key, "replacement maps to one owner-ledger target occurrence")
        mapping["target_occurrence_id"] = by_key[key]
        mapping["target_face_reference_count"] = face_counts[by_key[key]]
        mapping["target_corner_reference_count"] = corner_counts[by_key[key]]
    need(
        len({row["target_occurrence_id"] for row in mapping_rows}) == 18
        and owner_audit.get("candidate", {}).get("object_sha256")
        == owner["object_sha256"],
        "C51/C50a/independent-audit complete 18-row bijection",
    )
    mapping_rows.sort(key=lambda row: (
        row["task_binding_sha256"], row["side"], row["relative_path"]
    ))
    proof = {
        "schema": SCHEMA + ".C51-C50a-per-occurrence-mapping-proof",
        "replacement_count": 18,
        "target_occurrence_count": 18,
        "face_reference_count": 78,
        "corner_reference_count": 72,
        "all_replacements_biject_to_target_occurrences": True,
        "all_target_face_incident_sets_complete_and_owner_unique": True,
        "all_target_corner_germs_complete_and_owner_unique": True,
        "mapping_row_sequence_sha256": sequence_digest(digest(row) for row in mapping_rows),
        "mapping_rows": mapping_rows,
        "formal_credit": 0,
    }
    return close_object(proof, "proof_object_sha256")


def pins_frozen(values: Iterable[str]) -> bool:
    return all(HEX64.fullmatch(value) is not None for value in values)


def c52_pins_frozen() -> bool:
    return pins_frozen((C52_AUDIT_FILE_SHA256, C52_AUDIT_OBJECT_SHA256))


def validate_c52(path: Path) -> dict[str, Any]:
    need(c52_pins_frozen(), "C52 terminal file/object pins frozen in source")
    _raw, audit = captured_json(path, "C52 cold route audit", C52_AUDIT_FILE_SHA256)
    closed(audit, C52_AUDIT_OBJECT_SHA256, "C52 cold route audit")
    need(
        audit.get("schema") == C52_SCHEMA
        and audit.get("status") == C52_STATUS
        and audit.get("verifier_source_sha256") == C52_VERIFIER_SOURCE_SHA256
        and audit.get("formal_credit") == 0
        and audit.get("D02_gate_credit") == 0
        and audit.get("CM2") == "NO-GO_FOR_CLAIM"
        and audit.get("candidate_or_authority_created") is False
        and audit.get("pointer_seal_or_canonical_modified") is False
        and audit.get("runtime_writes_performed") is False,
        "C52 exact schema/status/nonpromotion scope",
    )
    c51 = audit.get("C51", {})
    c50a = audit.get("C50a", {})
    census = audit.get("census", {})
    independence = audit.get("independence", {})
    need(
        c51.get("object_sha256") == C51_OBJECT_SHA256
        and c51.get("independently_reconstructed_object_sha256")
        == C51_OBJECT_SHA256
        and c51.get("source_file_sha256") == C51_SOURCE_SHA256
        and c51.get("report_file_sha256") == C51_REPORT_SHA256
        and c50a.get("candidate_object_sha256")
        == C50A_FULL_RESULT_OBJECT_SHA256
        and c50a.get("independent_owner_audit_object_sha256")
        == C50A_FULL_AUDIT_OBJECT_SHA256
        and c50a.get("request_object_sha256") == C50A_REQUEST_OBJECT_SHA256
        and c50a.get("all_candidate_request_fields_match_independent_replay")
        is True
        and c50a.get("replacement_count") == 18
        and c50a.get("transaction_count") == 2
        and c50a.get("split_decision_count") == 14,
        "C52 frozen C51/C50a exact bindings",
    )
    expected_census = {
        "Kraft_one_task_count": 2,
        "collision1_strict_margin_complete_count": 18,
        "collision2_55_candidate_replay_count": 18,
        "collision2_owner_census": {"G[1,0]": 9, "G[1,1]": 9},
        "collision2_positive_boundary_separation_row_count": 972,
        "collision2_strict_margin_complete_count": 18,
        "logical_leaf_count": 9,
        "physical_side_strict_terminal_count": 18,
        "prefix_free_task_count": 2,
        "reflection_pair_count": 9,
        "route_classification_census": {
            "EXCLUDED_C39_C1_ENHANCED_W_SIDE_COLLISION2_OWNER_MISMATCH": 12,
            "UNRESOLVED_C39_C1_ENHANCED_W_SIDE_COLLISION2_OWNER": 6,
        },
        "task_count": 2,
    }
    need(census == expected_census, "C52 exact route/margin/reflection/Kraft census")
    expected_tasks = [
        {
            "task_index": row["index"],
            "task_binding_sha256": row["task_binding_sha256"],
            "root_path": row["root_path"],
            "frontier": row["frontier"],
            "logical_leaf_count": len(row["frontier"]),
            "physical_strict_terminal_count": 2 * len(row["frontier"]),
            "split_count": row["split_count"],
            "prefix_free": True,
            "relative_Kraft_sum": "1",
        }
        for row in TASKS
    ]
    tasks = audit.get("tasks")
    need(type(tasks) is list and len(tasks) == 2, "C52 two exact tasks")
    for actual, expected in zip(tasks, expected_tasks):
        need(
            all(actual.get(key) == value for key, value in expected.items())
            and HEX64.fullmatch(actual.get("leaf_object_sequence_sha256", ""))
            is not None
            and HEX64.fullmatch(actual.get("task_probe_object_sha256", ""))
            is not None,
            "C52 task replay exact",
        )
    attacks = audit.get("coherent_attacks")
    need(
        audit.get("coherent_attack_count") == 22
        and type(attacks) is list and len(attacks) == 22
        and len({row.get("attack") for row in attacks}) == 22
        and all(
            row.get("fail_closed") is True
            and HEX64.fullmatch(row.get("rejection_sha256", "")) is not None
            for row in attacks
        )
        and audit.get("all_attacks_fail_closed") is True,
        "C52 22 coherent attacks fail closed",
    )
    need(
        independence.get("C51_producer_imported_or_executed") is False
        and independence.get("C48_producer_imported_or_executed") is False
        and independence.get("C50a_candidate_consumed_as_data_only") is True
        and independence.get("forbidden_modules_absent_from_sys_modules") is True
        and independence.get("source_ast_import_scan_pass") is True
        and independence.get("source_ast_duplicate_literal_key_scan_pass") is True
        and independence.get("C40_independent_numeric_implementation_replayed")
        is True
        and independence.get("C41_C46_and_C32_frozen_authorities_consumed")
        is True
        and audit.get("frozen_pre_post_equal") is True
        and audit.get("frozen_file_sha256")
        == audit.get("frozen_file_post_sha256")
        and audit.get("frozen_plan") == {
            "C46_plan_object_sha256": C46_PLAN_OBJECT_SHA256,
            "pair_index": PAIR,
            "shard_index": SHARD_INDEX,
            "task_indices": [0, 1],
        },
        "C52 cold independence and frozen pre/post equality",
    )
    return audit


def validate_c50d() -> dict[str, Any]:
    protocol = stable_read(C50D_PROTOCOL, "C50d global CAS protocol", 1 << 20)
    companion = stable_read(
        C50D_PROTOCOL_COMPANION, "C50d global CAS protocol companion", 1 << 20
    )
    need(
        file_digest(protocol) == C50D_PROTOCOL_FILE_SHA256
        and file_digest(companion) == C50D_PROTOCOL_COMPANION_FILE_SHA256
        and companion == (
            C50D_PROTOCOL_FILE_SHA256 + "  " + C50D_PROTOCOL.name + "\n"
        ).encode("ascii"),
        "C50d protocol and exact sha256sum companion",
    )
    required_literals = (
        C50D_PREDECESSOR_IDENTITY_SCHEMA,
        C50D_CLAIM_SCHEMA,
        ".cm2-runtime/cm2-global-successor-claims",
        ".cm2-runtime/cm2-global-authority-heads",
        "predecessor-<P>.claim",
        "predecessor-<P>.seal",
        "predecessor_identity_sha256",
        "claim_object_sha256",
    )
    text = protocol.decode("utf-8", "strict")
    need(all(value in text for value in required_literals),
         "C50d required frozen protocol literals")
    return {
        "protocol_file_sha256": C50D_PROTOCOL_FILE_SHA256,
        "protocol_companion_file_sha256": C50D_PROTOCOL_COMPANION_FILE_SHA256,
    }


def artifact_paths(args: argparse.Namespace) -> dict[str, Path]:
    return {
        "route": args.route_result.absolute(),
        "owner_result": args.owner_result.absolute(),
        "owner_audit": args.owner_audit.absolute(),
        "cold_audit": args.cold_audit.absolute(),
    }


def preflight(args: argparse.Namespace) -> dict[str, Any]:
    checks: dict[str, bool] = {}
    blockers: list[str] = []

    def attempt(name: str, function: Any) -> None:
        try:
            function()
            checks[name] = True
        except (Reject, OSError, ValueError, KeyError, TypeError) as error:
            checks[name] = False
            blockers.append(name + ":" + type(error).__name__ + ":" + str(error))

    paths = artifact_paths(args)
    attempt("installed_C42_formal_predecessor", validate_c42)
    attempt("installed_C48_logical_predecessor", validate_c48)
    attempt("C50d_global_successor_CAS_protocol", validate_c50d)
    attempt("C50a_compact_bindings", validate_owner_wrappers)
    attempt("C51_complete_route_bytes", lambda: validate_route(paths["route"]))
    attempt(
        "C50a_complete_owner_candidate_and_audit_bytes",
        lambda: validate_full_owner(paths["owner_result"], paths["owner_audit"]),
    )
    if not c52_pins_frozen():
        checks["C52_static_terminal_pins"] = False
        blockers.append("C52_static_terminal_pins:independent C52 file/object hashes not frozen")
    else:
        checks["C52_static_terminal_pins"] = True
        attempt("C52_no_producer_cold_route_audit", lambda: validate_c52(paths["cold_audit"]))
    ready = bool(checks) and all(checks.values())
    body = {
        "schema": SCHEMA + ".preflight",
        "status": (
            "PASS_C53_PAIR1_CANDIDATE_INPUT_PREFLIGHT__NO_WRITES"
            if ready else
            "BLOCKED_C53_PAIR1_CANDIDATE_FAIL_CLOSED__NO_WRITES_NO_CREDIT"
        ),
        "checks": checks,
        "blockers": blockers,
        "ready_to_build_candidate": ready,
        "installed_authority_while_blocked": {
            "global_logical_predecessor": "C48",
            "logical_pending_task_count": BEFORE["logical_pending_task_count"],
            "paired_coarse_cells": BEFORE["paired_coarse_cells"],
            "unresolved_coarse_cells": BEFORE["unresolved_coarse_cells"],
            "representative_parents_remaining": BEFORE["representative_parents_remaining"],
        },
        "prospective_transition_only_not_authority": AFTER_IF_SEALED,
        "runtime_writes_performed": False,
        "formal_credit": 0,
        "D02_gate_credit": 0,
    }
    return close_object(body, "preflight_object_sha256")


def load_c46() -> tuple[
    Any, dict[str, Any], list[dict[str, Any]], list[dict[str, Any]],
    dict[str, Any], dict[str, Any],
]:
    capture = HeldSourceCapture(C46_SOURCE, "C46 source", C46_SOURCE_SHA256)
    try:
        # Execute exactly the captured bytes, never a second path read through
        # SourceFileLoader.  C46 has no transitive Python-module imports; its
        # runtime ledgers/manifests are each stable-read and hash-pinned by C46.
        code = compile(capture.raw, str(C46_SOURCE), "exec", dont_inherit=True)
        module = types.ModuleType("c53_frozen_c46")
        module.__file__ = str(C46_SOURCE)
        module.__package__ = None
        exec(code, module.__dict__)
        capture.unchanged("after captured-byte exec")
        plan, _tasks, shards = module.build_read_only_plan(64)
        capture.unchanged("after plan reconstruction")
        need(plan.get("plan_object_sha256") == C46_PLAN_OBJECT_SHA256,
             "C46 plan object pin")
        shard = next(row for row in shards if row["shard_index"] == SHARD_INDEX)
        need(
            shard["shard_id"] == SHARD_ID
            and shard["task_count"] == SHARD_TASK_COUNT
            and shard["ordered_task_binding_sequence_sha256"] == SHARD_BINDING_SEQUENCE_SHA256,
            "C46 shard9 pins",
        )
        genesis = module.make_checkpoint(plan, shard)
        capture.unchanged("after genesis reconstruction")
        need(genesis["checkpoint_object_sha256"] == GENESIS_CHECKPOINT_OBJECT_SHA256,
             "C46 shard9 genesis pin")
        for expected in TASKS:
            task = shard["_tasks"][expected["index"]]
            need(
                task["pair_index"] == PAIR
                and task["task_binding_sha256"] == expected["task_binding_sha256"]
                and task["descendant_path"] == expected["root_path"],
                "C46 exact pair1 task index:" + str(expected["index"]),
            )
        need(all(row["pair_index"] != PAIR for row in shard["_tasks"][2:]),
             "pair1 exact two-task group at indices 0/1")
        return module, plan, _tasks, shards, shard, genesis
    finally:
        capture.close()


def global_membership_proof(
    plan: dict[str, Any], tasks: list[dict[str, Any]],
    shards: list[dict[str, Any]], shard9: dict[str, Any],
) -> dict[str, Any]:
    need(
        len(tasks) == 33_642 and len(shards) == 64
        and [row["shard_index"] for row in shards] == list(range(64)),
        "C46 full inventory and 64-shard census",
    )
    pending = [
        row for row in tasks
        if row["queue"]["state"] == "RESUMABLE_PENDING_ZERO_CREDIT"
    ]
    closed = [
        row for row in tasks
        if row["queue"]["state"] == "CLOSED_BY_INSTALLED_C42_AUTHORITY"
    ]
    need(
        len(pending) == 33_641 and len(closed) == 1
        and closed[0]["pair_index"] == 391,
        "C46 C42-only pending/closed partition",
    )
    public_shards = plan.get("sharding", {}).get("shards")
    need(type(public_shards) is list and len(public_shards) == 64,
         "C46 public 64-shard plan")
    pair_membership = []
    for public in public_shards:
        need(
            public.get("pair_preserving") is True
            and public.get("pair_count") == len(public.get("pair_indices", [])),
            "C46 public shard pair-preserving census",
        )
        for pair_index in public["pair_indices"]:
            pair_membership.append({
                "pair_index": pair_index,
                "shard_index": public["shard_index"],
                "shard_id": public["shard_id"],
            })
    pair_membership.sort(key=lambda row: row["pair_index"])
    need(
        len(pair_membership) == 575
        and [row["pair_index"] for row in pair_membership]
        == sorted({row["pair_index"] for row in pending})
        and len({row["pair_index"] for row in pair_membership}) == 575,
        "C46 all pending pairs assigned exactly once",
    )
    pair1_membership = [row for row in pair_membership if row["pair_index"] == PAIR]
    pair1_tasks = []
    for index, task in enumerate(shard9["_tasks"]):
        if task["pair_index"] == PAIR:
            pair1_tasks.append({
                "shard_index": SHARD_INDEX,
                "task_index": index,
                "task_id": task["task_id"],
                "task_binding_sha256": task["task_binding_sha256"],
                "root_path": task["descendant_path"],
                "priority_class": task["queue"]["priority_class"],
            })
    need(
        pair1_membership == [{
            "pair_index": PAIR,
            "shard_index": SHARD_INDEX,
            "shard_id": SHARD_ID,
        }]
        and [row["task_index"] for row in pair1_tasks] == [0, 1]
        and [row["task_binding_sha256"] for row in pair1_tasks]
        == [row["task_binding_sha256"] for row in TASKS]
        and [row["root_path"] for row in pair1_tasks]
        == [row["root_path"] for row in TASKS]
        and all(row["priority_class"] == "DIRECT_WHOLE_PAIR"
                for row in pair1_tasks)
        and len([row for row in tasks if row["pair_index"] == PAIR]) == 2,
        "pair1 globally unique two-task direct whole-pair membership",
    )
    inventory = plan.get("full_lower_strata_inventory", {})
    queue = plan.get("queue", {})
    sharding = plan.get("sharding", {})
    need(
        inventory.get("primary_residual_outer_count") == 33_642
        and inventory.get("parent_conservation_row_count") == 862
        and inventory.get("parent_path_prefix_free_count") == 862
        and inventory.get("parent_Kraft_one_count") == 862
        and queue.get("full_inventory_task_count") == 33_642
        and queue.get("default_execution_queue_count") == 33_641
        and queue.get("installed_C42_closed_task_count") == 1
        and sharding.get("pair_count") == 575
        and sharding.get("task_count") == 33_641
        and sharding.get("shards_disjoint_and_complete") is True,
        "C46 33642-task/862-parent/575-pending-pair global census",
    )
    return {
        "schema": SCHEMA + ".global-pair-membership-proof",
        "C46_plan_object_sha256": C46_PLAN_OBJECT_SHA256,
        "full_C41_residual_task_count": 33_642,
        "default_C42_only_pending_task_count": 33_641,
        "installed_C42_closed_task_count": 1,
        "global_parent_conservation_count": 862,
        "unresolved_representative_pair_count": 575,
        "shard_count": 64,
        "pair_to_shard_membership_count": 575,
        "pair_to_shard_membership_sequence_sha256": sequence_digest(
            digest(row) for row in pair_membership
        ),
        "pair1_pair_membership": pair1_membership,
        "pair1_global_task_membership": pair1_tasks,
        "pair1_global_task_count": 2,
        "pair1_absent_from_all_other_shards": True,
        "pair1_was_unresolved_under_C42": True,
        "formal_credit": 0,
    }


def logical_exits(
    task_probe: dict[str, Any], owner_result: dict[str, Any],
    owner_audit: dict[str, Any], cold_audit: dict[str, Any],
    occurrence_mapping: dict[str, Any],
) -> list[dict[str, Any]]:
    exits = []
    for logical in task_probe["dual_side_terminal_rows"]:
        relative = logical["relative_path"]
        sides = copy.deepcopy(logical["physical_sides"])
        mapped = sorted([
            row for row in occurrence_mapping["mapping_rows"]
            if row["task_binding_sha256"] == task_probe["task_binding_sha256"]
            and row["relative_path"] == relative
        ], key=lambda row: row["side"])
        need(
            len(mapped) == 2
            and [row["side"] for row in mapped]
            == ["REFLECTED", "REPRESENTATIVE"],
            "logical exit exact two C50a occurrence mappings",
        )
        body = {
            "schema": EXIT_SCHEMA,
            "task_id": task_probe["task_id"],
            "task_binding_sha256": task_probe["task_binding_sha256"],
            "pair_index": PAIR,
            "relative_path": relative,
            "absolute_path": task_probe["root_path"] + relative,
            "relative_fraction": str(Fraction(1, 2 ** len(relative))),
            "exit_class": "STRICT_EXCLUDED",
            "physical_sides": sides,
            "physical_side_count": 2,
            "C51_task_probe_object_sha256": task_probe["task_probe_object_sha256"],
            "C50a_full_owner_candidate_object_sha256": owner_result["object_sha256"],
            "C50a_full_owner_audit_object_sha256": owner_audit["object_sha256"],
            "C50a_history_head_sha256": C50A_HISTORY_HEAD_SHA256,
            "C51_C50a_mapping_proof_object_sha256": occurrence_mapping[
                "proof_object_sha256"
            ],
            "C50a_target_occurrence_mappings": mapped,
            "C52_cold_route_audit_object_sha256": cold_audit["object_sha256"],
            "both_physical_sides_independently_routed": True,
            "both_physical_sides_strictly_excluded": True,
            "all_strict_terminal_margins_complete": True,
            "full_active_universe_face_corner_owners_complete_and_unique": True,
            "formal_credit": 0,
        }
        certificate = close_object(body, "certificate_object_sha256")
        exits.append({
            "relative_path": relative,
            "absolute_path": body["absolute_path"],
            "relative_fraction": body["relative_fraction"],
            "state": "C53_PAIR_LEVEL_CANDIDATE_EXIT_ZERO_CREDIT_PENDING_SEAL",
            "exit_class": "STRICT_EXCLUDED",
            "certificate_object_sha256": certificate["certificate_object_sha256"],
            "certificate": certificate,
        })
    exits.sort(key=lambda row: row["relative_path"])
    need(prefix_free([row["relative_path"] for row in exits]) and
         kraft([row["relative_path"] for row in exits]) == 1,
         "C53 logical exit prefix/Kraft")
    return exits


def successor_task_state(
    old: dict[str, Any], task: dict[str, Any], probe: dict[str, Any],
    owner_result: dict[str, Any], owner_audit: dict[str, Any],
    cold_audit: dict[str, Any], occurrence_mapping: dict[str, Any],
) -> dict[str, Any]:
    exits = logical_exits(
        probe, owner_result, owner_audit, cold_audit, occurrence_mapping
    )
    split_events = []
    for event in probe["split_events"]:
        body = {
            "relative_path": event["relative_path"],
            "absolute_path": event["absolute_path"],
            "split_axis": event["split_axis"],
            "C41_split_face_adjacency_sha256": event[
                "C41_split_face_adjacency_sha256"
            ],
            "C51_split_object_sha256": event["split_object_sha256"],
            "C51_task_probe_object_sha256": probe["task_probe_object_sha256"],
            "formal_credit": 0,
        }
        split_events.append(close_object(body, "split_event_object_sha256"))
    body = {
        "schema": TASK_STATE_SCHEMA,
        "C46_predecessor_task_state_sha256": digest(old),
        "task_id": task["task_id"],
        "task_binding_sha256": task["task_binding_sha256"],
        "pair_index": PAIR,
        "source_descendant_path": task["descendant_path"],
        "dependency_closure_sha256": task["dependency_closure_sha256"],
        "state": "C53_PAIR_LEVEL_CANDIDATE_SOURCE_CLOSED_ZERO_CREDIT_PENDING_SEAL",
        "frontier": [],
        "exits": exits,
        "split_events": split_events,
        "event_count": len(exits) + len(split_events),
        "deepest_additional_depth": max(len(row["relative_path"]) for row in exits),
        "relative_Kraft_sum": "1",
        "prefix_free": True,
        "candidate_closed": True,
        "formal_closed": False,
        "credit_lock": ZERO_LOCK,
    }
    return close_object(body, "successor_task_state_sha256")


def successor_checkpoint(
    plan: dict[str, Any], shard: dict[str, Any], genesis: dict[str, Any],
    route: dict[str, Any], owner_result: dict[str, Any],
    owner_audit: dict[str, Any], cold_audit: dict[str, Any],
    occurrence_mapping: dict[str, Any],
) -> dict[str, Any]:
    old_states = genesis["task_states"]
    states = copy.deepcopy(old_states)
    for expected, probe in zip(TASKS, route["task_probes"], strict=True):
        index = expected["index"]
        states[index] = successor_task_state(
            old_states[index], shard["_tasks"][index], probe,
            owner_result, owner_audit, cold_audit, occurrence_mapping,
        )
    need(
        all(canonical(states[index]) == canonical(old_states[index])
            for index in range(2, SHARD_TASK_COUNT)),
        "C53 unchanged shard9 indices 2..588 byte-equal genesis",
    )
    body = {
        "schema": CHECKPOINT_SCHEMA,
        "status": (
            "C53_PAIR1_TWO_TASKS_CANDIDATE_CLOSED__587_SHARD_TASKS_PENDING__"
            "PAIR_LEVEL_SEAL_PENDING__ZERO_D02_GATE_CREDIT"
        ),
        "plan_object_sha256": plan["plan_object_sha256"],
        "shard_id": SHARD_ID,
        "shard_index": SHARD_INDEX,
        "generation": 1,
        "local_previous_checkpoint_object_sha256": GENESIS_CHECKPOINT_OBJECT_SHA256,
        "global_previous_authority_seal_object_sha256": C48_SEAL_OBJECT_SHA256,
        "global_previous_successor_checkpoint_object_sha256": C48_SUCCESSOR_OBJECT_SHA256,
        "task_count": SHARD_TASK_COUNT,
        "selected_pair_index": PAIR,
        "selected_task_indices": [0, 1],
        "candidate_closed_task_count": 2,
        "formal_closed_task_count_before_pair_seal": 0,
        "pending_task_count_after_candidate": 587,
        "ordered_task_binding_sequence_sha256": SHARD_BINDING_SEQUENCE_SHA256,
        "ordered_task_state_sequence_sha256": sequence_digest(digest(row) for row in states),
        "unchanged_indices_2_through_588_task_state_sequence_sha256": sequence_digest(
            digest(row) for row in old_states[2:]
        ),
        "unchanged_indices_2_through_588_byte_equal_to_genesis": True,
        "task_states": states,
        "global_candidate_progress": {
            "frozen_C41_logical_residual_outer_row_count": 33_642,
            "frozen_C41_two_side_residual_occurrence_count": 67_284,
            "installed_C42_logical_closed_task_count": 1,
            "installed_C48_logical_closed_task_count": 1,
            "authoritative_logical_pending_task_count_before_C53": 33_640,
            "C53_pair1_candidate_closed_task_count_pending_pair_seal": 2,
            "logical_pending_task_count_after_C53_if_pair_sealed": 33_638,
            "two_side_pending_occurrence_count_after_C53_if_pair_sealed": 67_276,
            "coarse_formal_authority_before_pair_seal": {
                "paired_coarse_cells": 574,
                "unresolved_coarse_cells": 1_150,
                "representative_parents_remaining": 575,
            },
            "coarse_formal_authority_after_pair_seal_only": {
                "paired_coarse_cells": 576,
                "unresolved_coarse_cells": 1_148,
                "representative_parents_remaining": 574,
            },
        },
        "credit_lock_before_pair_seal": ZERO_LOCK,
    }
    # The full genesis object is an input used to derive and byte-compare the
    # vector, but it is not appended after closure.  Appending it here would
    # mutate an already self-hashed object.  The immutable predecessor is
    # instead bound above by its frozen object hash.
    checkpoint = close_object(body, "successor_checkpoint_object_sha256")
    need(
        object_digest(checkpoint, "successor_checkpoint_object_sha256")
        == checkpoint["successor_checkpoint_object_sha256"],
        "C53 successor checkpoint terminal self-hash",
    )
    return checkpoint


def build_result(
    args: argparse.Namespace, self_capture: HeldSourceCapture,
) -> dict[str, Any]:
    self_capture.unchanged("build entry")
    gate = preflight(args)
    need(gate["ready_to_build_candidate"],
         "candidate inputs not terminal: " + " | ".join(gate["blockers"]))
    paths = artifact_paths(args)
    c42 = validate_c42()
    c48 = validate_c48()
    route = validate_route(paths["route"])
    compact_result, compact_audit = validate_owner_wrappers()
    owner_result, owner_audit = validate_full_owner(
        paths["owner_result"], paths["owner_audit"]
    )
    occurrence_mapping = validate_route_owner_mapping(
        route, owner_result, owner_audit
    )
    cold_audit = validate_c52(paths["cold_audit"])
    _c46, plan, all_tasks, shards, shard, genesis = load_c46()
    membership = global_membership_proof(
        plan, all_tasks, shards, shard
    )
    checkpoint = successor_checkpoint(
        plan, shard, genesis, route, owner_result, owner_audit, cold_audit,
        occurrence_mapping,
    )
    c50d = validate_c50d()
    predecessor_identity = close_object({
        "authority_heads": [
            {
                "authority_schema": C42_SEAL_SCHEMA,
                "role": "FORMAL_COARSE",
                "seal_file_sha256": C42_SEAL_FILE_SHA256,
                "seal_object_sha256": C42_SEAL_OBJECT_SHA256,
                "seal_path": ".cm2-runtime/c42-current-authority-seal",
                "successor_checkpoint_object_sha256": None,
            },
            {
                "authority_schema": C48_SEAL_SCHEMA,
                "role": "LOGICAL_TASK",
                "seal_file_sha256": C48_SEAL_FILE_SHA256,
                "seal_object_sha256": C48_SEAL_OBJECT_SHA256,
                "seal_path": ".cm2-runtime/c48-current-task-authority-seal",
                "successor_checkpoint_object_sha256":
                    C48_SUCCESSOR_OBJECT_SHA256,
            },
        ],
        "before_census": C50D_BEFORE_CENSUS,
        "ordered_head_roles": ["FORMAL_COARSE", "LOGICAL_TASK"],
        "schema": C50D_PREDECESSOR_IDENTITY_SCHEMA,
    }, "predecessor_identity_sha256")
    need(
        predecessor_identity["predecessor_identity_sha256"]
        == C50D_LEGACY_PREDECESSOR_IDENTITY_SHA256,
        "C50d frozen legacy predecessor identity hash",
    )
    # This basename is a compare-and-swap key for the predecessor, not for the
    # proposed successor.  Therefore two distinct successor bodies racing from
    # the same predecessor necessarily contend on the same O_EXCL target.
    claim_basename = (
        "predecessor-"
        + C50D_LEGACY_PREDECESSOR_IDENTITY_SHA256
        + ".claim"
    )
    head_basename = (
        "predecessor-" + C50D_LEGACY_PREDECESSOR_IDENTITY_SHA256 + ".seal"
    )
    claim_publication = {
        "claim_namespace": GLOBAL_CLAIM_NAMESPACE,
        "claim_basename": claim_basename,
        "claim_relative_path": (
            ".cm2-runtime/" + GLOBAL_CLAIM_NAMESPACE + "/" + claim_basename
        ),
        "publication": "O_EXCL_RENAME_NOREPLACE_UNDER_GLOBAL_AUTHORITY_LOCK",
        "predecessor_keyed_not_successor_keyed": True,
        "exact_existing_bytes_required_for_idempotent_resume": True,
        "different_existing_bytes_are_a_fork_and_must_fail_closed": True,
        "successor_round_or_domain_cannot_change_namespace_or_key": True,
        "claim_without_authority_seal_is_reservation_only": True,
        "authority_head_namespace": GLOBAL_HEAD_NAMESPACE,
        "authority_head_basename": head_basename,
        "authority_seal_target_path": (
            ".cm2-runtime/" + GLOBAL_HEAD_NAMESPACE + "/" + head_basename
        ),
    }
    transaction_body = {
        "schema": SCHEMA + ".atomic-pair-transaction",
        "pair_index": PAIR,
        "shard_index": SHARD_INDEX,
        "task_indices": [0, 1],
        "task_binding_sha256s": [row["task_binding_sha256"] for row in TASKS],
        "local_predecessor_checkpoint_object_sha256": GENESIS_CHECKPOINT_OBJECT_SHA256,
        "global_predecessor_authority_seal_object_sha256": C48_SEAL_OBJECT_SHA256,
        "global_predecessor_successor_checkpoint_object_sha256": C48_SUCCESSOR_OBJECT_SHA256,
        "successor_checkpoint_object_sha256": checkpoint[
            "successor_checkpoint_object_sha256"
        ],
        "C51_route_object_sha256": C51_OBJECT_SHA256,
        "C50a_owner_candidate_object_sha256": C50A_FULL_RESULT_OBJECT_SHA256,
        "C50a_owner_audit_object_sha256": C50A_FULL_AUDIT_OBJECT_SHA256,
        "C52_cold_route_audit_object_sha256": C52_AUDIT_OBJECT_SHA256,
        "global_predecessor_authority_identity": predecessor_identity,
        "global_predecessor_claim_publication": claim_publication,
        "atomicity": {
            "both_tasks_or_neither": True,
            "single_pair_level_seal_required": True,
            "task_level_partial_credit_forbidden": True,
            "seal_is_only_semantic_commit": True,
        },
        "zero_credit_candidate_authority_effect": {
            "before": BEFORE,
            "after": BEFORE,
            "C50d_before_census": C50D_BEFORE_CENSUS,
            "complete_D02_formal_census_before": D02_FORMAL_CENSUS_BEFORE,
            "task_formal_closed_count": 0,
            "whole_parent_credit": 0,
            "D02_gate_credit": 0,
        },
        "prospective_post_audit_and_seal_promotion": {
            "before": BEFORE,
            "after": AFTER_IF_SEALED,
            "C50d_before_census": C50D_BEFORE_CENSUS,
            "C50d_after_census": C50D_AFTER_CENSUS_IF_SEALED,
            "complete_D02_formal_census_before": D02_FORMAL_CENSUS_BEFORE,
            "complete_D02_formal_census_after":
                D02_FORMAL_CENSUS_AFTER_IF_SEALED,
            "task_formal_closed_count": 2,
            "whole_parent_credit": 1,
            "D02_gate_credit": 0,
            "effective_selected_task_projection": {
                "selected_task_indices": [0, 1],
                "candidate_formal_closed_values": [False, False],
                "effective_post_seal_formal_closed_values": [True, True],
                "per_task_credit_lock_remains": ZERO_LOCK,
                "pair_level_credit_is_unique": {
                    "whole_parent_credit": 1,
                    "D02_gate_credit": 0,
                },
                "indices_2_through_588_remain_byte_equal_to_genesis": True,
            },
            "independent_C53_promotion_derivation_required": True,
            "promotion_derivation_not_minted_by_candidate": True,
            "pair_level_seal_must_bind_promotion_derivation_object_sha256": True,
        },
        "formal_credit_before_seal": 0,
    }
    transaction = close_object(transaction_body, "pair_transaction_object_sha256")
    claim_contract_body = {
        "schema": (
            "cm2.round306c53.global-predecessor-successor-final-claim-contract.v1"
        ),
        "predecessor_authority_identity": predecessor_identity,
        "successor_domain": SCHEMA,
        "unique_pair_transaction_object_sha256": transaction[
            "pair_transaction_object_sha256"
        ],
        "unique_successor_checkpoint_object_sha256": checkpoint[
            "successor_checkpoint_object_sha256"
        ],
        "pair_index": PAIR,
        "task_binding_sha256s": [row["task_binding_sha256"] for row in TASKS],
        "publication": claim_publication,
        "C50d_protocol_binding": c50d,
        "final_claim_schema": C50D_CLAIM_SCHEMA,
        "final_claim_exact_fields_before_self_hash": [
            "authority_seal_target_path",
            "independent_audit_object_sha256",
            "installation_receipt_file_sha256",
            "installation_receipt_object_sha256",
            "pair_transaction_object_sha256",
            "post_seal_effective_checkpoint_object_sha256",
            "predecessor_identity",
            "promotion_derivation_object_sha256",
            "schema",
            "successor_descriptor_object_sha256",
            "zero_credit_before_seal",
        ],
        "final_claim_self_hash_field": "claim_object_sha256",
        "final_claim_must_also_bind_after_terminal_bytes_exist": [
            "successor_candidate_file_sha256",
            "successor_candidate_object_sha256",
            "independent_audit_file_sha256",
            "independent_audit_object_sha256",
            "post_seal_promotion_derivation_object_sha256",
            "effective_post_seal_checkpoint_object_sha256",
            "authority_seal_target_path",
        ],
        "authority_seal_target_path": claim_publication[
            "authority_seal_target_path"
        ],
        "final_claim_is_constructed_only_after_independent_audit": True,
        "candidate_does_not_mint_final_claim_or_promotion": True,
        "final_seal_must_bind_final_claim_file_and_object_sha256": True,
        "final_seal_must_bind_promotion_and_effective_checkpoint_sha256": True,
        "required_effective_post_seal_semantics": {
            "task_indices_0_and_1_formal_closed": True,
            "per_task_credit_lock": ZERO_LOCK,
            "pair_level_whole_parent_credit": 1,
            "D02_gate_credit": 0,
            "authoritative_after": AFTER_IF_SEALED,
            "complete_D02_formal_census_before": D02_FORMAL_CENSUS_BEFORE,
            "complete_D02_formal_census_after":
                D02_FORMAL_CENSUS_AFTER_IF_SEALED,
            "C50d_before_census": C50D_BEFORE_CENSUS,
            "C50d_after_census": C50D_AFTER_CENSUS_IF_SEALED,
        },
        "single_successor_for_predecessor": True,
        "forks_forbidden": True,
        "D02_gate_credit": 0,
    }
    claim_contract = close_object(
        claim_contract_body, "claim_template_object_sha256"
    )
    body = {
        "schema": SCHEMA,
        "status": (
            "PASS_C53_PAIR1_ATOMIC_PAIR_LEVEL_SUCCESSOR_CANDIDATE__"
            "NO_REPLACE_SEAL_PENDING__ZERO_D02_GATE_CREDIT"
        ),
        "source": {"path": str(SELF.relative_to(ROOT)),
                   "sha256": self_capture.sha256},
        "predecessors": {
            "formal_C42_authority": {
                "seal_file_sha256": C42_SEAL_FILE_SHA256,
                "seal_object_sha256": c42["authority_seal_object_sha256"],
                "status": C42_SEAL_STATUS,
                "formal_census_after_commit": C42_CENSUS,
            },
            "local_C46_shard9_generation0": {
                "checkpoint_object_sha256": GENESIS_CHECKPOINT_OBJECT_SHA256,
                "shard_id": SHARD_ID,
                "shard_index": SHARD_INDEX,
                "task_count": SHARD_TASK_COUNT,
                "ordered_task_binding_sequence_sha256": SHARD_BINDING_SEQUENCE_SHA256,
            },
            "logical_C48_authority": {
                "seal_file_sha256": C48_SEAL_FILE_SHA256,
                "seal_object_sha256": c48["authority_seal_object_sha256"],
                "successor_checkpoint_object_sha256": C48_SUCCESSOR_OBJECT_SHA256,
                "coarse_formal_authority_unchanged": {
                    "paired_coarse_cells": 574,
                    "unresolved_coarse_cells": 1_150,
                    "representative_parents_remaining": 575,
                },
            },
        },
        "C46_plan_public": plan,
        "C46_shard9_genesis": genesis,
        "global_pair_membership_proof": membership,
        "C51_C50a_per_occurrence_mapping_proof": occurrence_mapping,
        "evidence_bindings": {
            "C50d": c50d,
            "C51": {"object_sha256": route["object_sha256"],
                    "source_sha256": C51_SOURCE_SHA256,
                    "report_sha256": C51_REPORT_SHA256},
            "C50a": {
                "compact_result_object_sha256": compact_result["object_sha256"],
                "compact_audit_object_sha256": compact_audit["object_sha256"],
                "full_result_file_sha256": C50A_FULL_RESULT_FILE_SHA256,
                "full_result_encoded_bundle_sha256": C50A_FULL_RESULT_ENCODED_SHA256,
                "full_result_gzip_sha256": C50A_FULL_RESULT_GZIP_SHA256,
                "full_result_object_sha256": owner_result["object_sha256"],
                "full_audit_file_sha256": C50A_FULL_AUDIT_FILE_SHA256,
                "full_audit_encoded_bundle_sha256": C50A_FULL_AUDIT_ENCODED_SHA256,
                "full_audit_gzip_sha256": C50A_FULL_AUDIT_GZIP_SHA256,
                "full_audit_object_sha256": owner_audit["object_sha256"],
                "request_object_sha256": C50A_REQUEST_OBJECT_SHA256,
                "history_head_sha256": C50A_HISTORY_HEAD_SHA256,
            },
            "C52": {"audit_file_sha256": C52_AUDIT_FILE_SHA256,
                    "audit_object_sha256": cold_audit["object_sha256"]},
        },
        "selection": {
            "pair_index": PAIR,
            "task_count": 2,
            "task_indices": [0, 1],
            "task_binding_sha256s": [row["task_binding_sha256"] for row in TASKS],
            "frontiers": [row["frontier"] for row in TASKS],
            "logical_leaf_count": 9,
            "physical_side_terminal_count": 18,
        },
        "global_predecessor_claim_template": claim_contract,
        "pair_transaction": transaction,
        "successor": checkpoint,
        "strict_nonpromotion": {
            "runtime_write_code_path_exists": False,
            "runtime_writes_performed": False,
            "candidate_pointer_receipt_or_seal_created": False,
            "canonical_or_prior_authority_modified": False,
            "coarse_formal_authority_before_pair_seal": BEFORE,
            "prospective_after_is_not_authority_without_independent_promotion_and_pair_seal": True,
            "post_seal_promotion_derivation_minted": False,
            "whole_parent_credit": 0,
            "D02_A_complete": False,
            "D02_gate_credit": 0,
            "CM2": "NO-GO_FOR_CLAIM",
            "formal_credit": 0,
        },
        "formal_credit": 0,
    }
    self_capture.unchanged("build terminal barrier")
    return close_object(body, "object_sha256")


def self_test() -> dict[str, Any]:
    checks: dict[str, bool] = {}
    checks["pair1_task_indices_exact"] = [row["index"] for row in TASKS] == [0, 1]
    checks["pair1_bindings_distinct"] = len({row["task_binding_sha256"] for row in TASKS}) == 2
    checks["frontier0_prefix_free"] = prefix_free(TASKS[0]["frontier"])
    checks["frontier0_Kraft_one"] = kraft(TASKS[0]["frontier"]) == 1
    checks["frontier1_prefix_free"] = prefix_free(TASKS[1]["frontier"])
    checks["frontier1_Kraft_one"] = kraft(TASKS[1]["frontier"]) == 1
    checks["nine_logical_eighteen_physical"] = (
        sum(len(row["frontier"]) for row in TASKS) == 9
        and 2 * sum(len(row["frontier"]) for row in TASKS) == 18
    )
    checks["pending_arithmetic"] = 33_642 - 1 - 1 - 2 == 33_638
    checks["physical_arithmetic"] = 67_284 - 2 - 2 - 4 == 67_276
    checks["coarse_atomic_transition"] = (
        AFTER_IF_SEALED["paired_coarse_cells"] - BEFORE["paired_coarse_cells"] == 2
        and BEFORE["unresolved_coarse_cells"] - AFTER_IF_SEALED["unresolved_coarse_cells"] == 2
        and BEFORE["representative_parents_remaining"]
        - AFTER_IF_SEALED["representative_parents_remaining"] == 1
    )
    value = close_object({"schema": "selftest", "status": "PASS"}, "object_sha256")
    checks["canonical_self_hash"] = object_digest(value) == value["object_sha256"]
    mutated = copy.deepcopy(value)
    mutated["status"] = "MUTATED"
    checks["post_close_mutation_rejected"] = (
        object_digest(mutated) != mutated["object_sha256"]
    )
    checks["placeholder_pin_fixture_rejected"] = not pins_frozen(
        ("__PLACEHOLDER__", "0" * 64)
    )
    checks["complete_pin_fixture_accepted"] = pins_frozen(("a" * 64, "b" * 64))
    checks["global_and_local_predecessors_distinct"] = (
        GENESIS_CHECKPOINT_OBJECT_SHA256 != C48_SUCCESSOR_OBJECT_SHA256
        and SHARD_INDEX != 2
    )
    with tempfile.TemporaryDirectory(prefix="c53-source-capture-selftest-") as directory:
        source = Path(directory) / "source.py"
        replacement = Path(directory) / "replacement.py"
        payload = b"VALUE = 1\n"
        replacement_payload = b"VALUE = 2\n"
        for path, raw in ((source, payload), (replacement, replacement_payload)):
            fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_CLOEXEC, 0o600)
            try:
                os.write(fd, raw)
                os.fsync(fd)
            finally:
                os.close(fd)
        capture = HeldSourceCapture(
            source, "selftest source", file_digest(payload), workspace_only=False
        )
        try:
            os.replace(replacement, source)
            try:
                capture.unchanged("late replacement attack")
            except Reject:
                checks["late_source_replacement_rejected"] = True
        finally:
            capture.close()
    need(len(checks) == 16 and all(checks.values()), "C53 candidate self-test 16/16")
    return {
        "schema": SCHEMA + ".self-test",
        "status": "PASS_C53_PAIR1_CANDIDATE_SELF_TEST_16_OF_16",
        "passed": 16,
        "total": 16,
        "checks": checks,
        "runtime_writes_performed": False,
        "formal_credit": 0,
    }


def parser() -> argparse.ArgumentParser:
    value = argparse.ArgumentParser(description=__doc__)
    mode = value.add_mutually_exclusive_group(required=True)
    mode.add_argument("--self-test", action="store_true")
    mode.add_argument("--preflight", action="store_true")
    mode.add_argument("--build", action="store_true")
    value.add_argument("--route-result", type=Path, default=C51_RESULT)
    value.add_argument("--owner-result", type=Path, default=C50A_FULL_RESULT)
    value.add_argument("--owner-audit", type=Path, default=C50A_FULL_AUDIT)
    value.add_argument("--cold-audit", type=Path, default=C52_AUDIT)
    return value


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    try:
        if args.self_test:
            result = self_test()
        elif args.preflight:
            result = preflight(args)
        else:
            self_capture = HeldSourceCapture(
                SELF, "C53 executing candidate source", None, maximum=4 << 20
            )
            try:
                result = build_result(args, self_capture)
                self_capture.unchanged("immediately before terminal stdout")
            finally:
                self_capture.close()
        sys.stdout.buffer.write(canonical(result) + b"\n")
        return 0
    except (Reject, OSError, ValueError, KeyError, TypeError, StopIteration) as error:
        body = {
            "schema": SCHEMA + ".fail-closed",
            "status": "REJECT_C53_PAIR1_PAIR_LEVEL_SUCCESSOR_CANDIDATE",
            "error_class": type(error).__name__,
            "reason": str(error),
            "runtime_writes_performed": False,
            "formal_credit": 0,
            "D02_gate_credit": 0,
        }
        sys.stdout.buffer.write(canonical(close_object(body, "object_sha256")) + b"\n")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
