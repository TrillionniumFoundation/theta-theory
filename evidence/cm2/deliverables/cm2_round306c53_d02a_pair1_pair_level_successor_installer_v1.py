#!/usr/bin/env python3
"""No-replace installer for the C53 pair-1 pair-level successor.

This follows the C48 generation-1 publication semantics: stable no-follow
captures, immutable candidate/evidence bundles, exact resumable transaction
prefixes, O_EXCL, fsync, Linux renameat2(RENAME_NOREPLACE), and a self-hashed
seal as the only semantic commit point.

All C51, C52, C53 candidate, and independent-audit inputs are frozen by exact
hash.  ``--preflight``, ``--dry-run``, and ``--verify-installed`` are read-only.
``--install`` remains gated by the exact confirmation literal and the frozen
installer self-hash.  No transition is authoritative unless the exact
predecessor-keyed C50d global head seal commits last and is fully replayed.
"""

from __future__ import annotations

import argparse
import ast
import ctypes
import errno
import fcntl
import hashlib
import json
import os
from pathlib import Path
import re
import stat
import sys
import tempfile
from typing import Any


sys.dont_write_bytecode = True
SELF = Path(__file__).absolute()
ROOT = SELF.parent.parent
DELIVERABLES = ROOT / "deliverables"
RUNTIME = ROOT / ".cm2-runtime"

SCHEMA = "cm2.round306c53.d02-a-pair1-pair-level-successor-installer.v1"
RECEIPT_SCHEMA = SCHEMA + ".installation-receipt"
SEAL_SCHEMA = SCHEMA + ".authority-seal"
MANIFEST_SCHEMA = SCHEMA + ".bundle-manifest"
CONFIRMATION = "INSTALL_C53_PAIR1_ATOMIC_TWO_TASK_PAIR_LEVEL_SUCCESSOR_ZERO_D02_GATE_CREDIT"

HEX64 = re.compile(r"[0-9a-f]{64}\Z")
SAFE_NAME = re.compile(r"(?:[A-Za-z0-9]|\.[A-Za-z0-9])[A-Za-z0-9_.-]*\Z")
UNFROZEN = "__UNFROZEN__"

PAIR = 1
SHARD_INDEX = 9
SHARD_ID = "c46-d02a-shard:0916976b9ec8a154268b3f290d1a4053ad47c8b8d41dbfe17d63cd0735c91095"
SHARD_TASK_COUNT = 589
SHARD_BINDING_SEQUENCE_SHA256 = "da4be1a51035b750b7981507f6ff74967bf7f441475286af7a1dc6fa0f6abcb7"
GENESIS_CHECKPOINT_OBJECT_SHA256 = "b962a7f05c99ff1e3fe2f2af98319f5e3cab005cca68b453d9152bf2435cacee"
TASK_BINDINGS = [
    "daada4d9fd48677629cbfa9872b073d5fdf1552b115bf94438e7357f9a5dd95b",
    "e37b527423ad1aabba7485faacd03f7bb95ba9d79caebd614fb63d38ccd8dac6",
]
FRONTIERS = [["0", "1"], ["00", "01", "10", "110", "1110", "11110", "11111"]]

C46_SOURCE_PATH = (
    "deliverables/cm2_round306c46_d02a_general_adaptive_lower_strata_"
    "closure_engine_v1.py"
)
C46_SOURCE_SHA256 = "365432e96f2c287ef3c5497b7d15e01a80775f52d8cf5b71810d6f4c0e4442ea"

C48_SEAL_PATH = ".cm2-runtime/c48-current-task-authority-seal"
C48_SEAL_FILE_SHA256 = "13a07654d2eba6b2f1072d4a6a70636a90437e1da18e0bbeb8630ab841e026c1"
C48_SEAL_OBJECT_SHA256 = "95297adbe0d2ee86788008046bc47c337a9c7a3fa0e46bd896e674a2931ec6b1"
C48_SUCCESSOR_OBJECT_SHA256 = "bbd909cad5a5d0b9cc44362be6acb26d527f86edc1b8191c06a246a514c9c984"
C48_SEAL_SCHEMA = (
    "cm2.round306c48.d02-a-pair668-generation1-successor-installer.v1."
    "authority-seal"
)
C48_STATUS = (
    "COMMITTED_C48_PAIR668_GEN1_TASK_SUCCESSOR_AUTHORITY__ONE_AUDITED_"
    "TASK_LEVEL_SUCCESSOR__ZERO_D02_GATE_CREDIT"
)

C42_SEAL_PATH = ".cm2-runtime/c42-current-authority-seal"
C42_SEAL_FILE_SHA256 = "0e5a76059b2c9407340d88e07f4fcc356d376f5c24b7173e6b95fd5e06bc312d"
C42_SEAL_OBJECT_SHA256 = "b321552768a6aeae6c1d229e52b61ca0b4420314234e02e98366153d4156d460"
C42_SEAL_SCHEMA = "cm2.round306c42.f1-authority-commit-seal.v1"
C42_STATUS = "COMMITTED_C42_F1_AUTHORITY__574_PAIRED__1150_UNRESOLVED"
C42_CANDIDATE_POINTER_PATH = ".cm2-runtime/c42-current-token"
C42_CANDIDATE_POINTER_SHA256 = "fbc5dd3c55bfdd3098ed34ae09ae633a9526a9c9cc6f40b3d87b5669b2ea7f07"
C42_AUDIT_POINTER_PATH = ".cm2-runtime/c42-current-audit-token"
C42_AUDIT_POINTER_SHA256 = "59aca53c4c35260801b3c559648c88ee974db01ae950f045a5e5aecd64aa36e5"

C48_RECEIPT_PATH = (
    ".cm2-runtime/c48-successor-audits/"
    "c48-independent-audit-cf0531127a5c-v1/installation_receipt.json"
)
C48_RECEIPT_FILE_SHA256 = "00338955b3225d96670806ab482775313e0afb68ebf7cafe01608787d828561b"
C48_RECEIPT_OBJECT_SHA256 = "90e698b52b95a229805a5e800dd65bc7615998647564f5161b601c26e2b5b299"
C48_CANDIDATE_POINTER_PATH = ".cm2-runtime/c48-current-successor-token"
C48_CANDIDATE_POINTER_SHA256 = "30f289738d4e3d28a3fa230ad19253b29ef7373f33689181a3e50b1c7867fae4"
C48_AUDIT_POINTER_PATH = ".cm2-runtime/c48-current-successor-audit-token"
C48_AUDIT_POINTER_SHA256 = "f80179317dee4b7e02cfe651e23f059d1219ffe753c5e9f5b1d970721b0490be"

C50D_PROTOCOL_PATH = "deliverables/cm2_round306c50d_global_successor_cas_protocol_freeze_v1.md"
C50D_PROTOCOL_FILE_SHA256 = "46a1a0a78970a6219b5a03bf9b91820b9121f4e409a46adcbb0c2ef793eeaf86"
C50D_PROTOCOL_COMPANION_PATH = C50D_PROTOCOL_PATH + ".sha256"
C50D_PROTOCOL_COMPANION_FILE_SHA256 = "d34e35ee41798700699addd02555d32ff6608204db99a869b8ba303cc9784c5a"
C50D_PREDECESSOR_IDENTITY_SCHEMA = "cm2.global-authority-predecessor-identity.v1"
C50D_CLAIM_SCHEMA = "cm2.global-authority-predecessor-consumption-claim.v1"
C50D_PREDECESSOR_IDENTITY_SHA256 = "10fb050d30c92b0f2bdcf85a30d28ff670d8efc0b48104b7f04a63c391967b41"

C51_SOURCE_PATH = "deliverables/cm2_round306c51_d02a_pair1_two_task_route_probe_v1.py"
C51_SOURCE_SHA256 = "caf043d2a475f8c25e92785587db971a0d33242b8560dd096f09a1e5c6e72069"
C51_REPORT_PATH = "deliverables/cm2_round306c51_d02a_pair1_two_task_route_probe_report_v1.md"
C51_REPORT_SHA256 = "d2330ac69da6cdb0e3fa092c9b697c836a21026ebb52b9b3655f9487a88f6330"
C51_RESULT_PATH = "deliverables/cm2_round306c53_d02a_pair1_c51_frozen_route_result_v1.json"
C51_RESULT_FILE_SHA256 = "a560cdae560ce06879e3df3b0265aa97249d879011c7844394da73ea6fb32976"
C51_OBJECT_SHA256 = "187344a3c524dce1898151bf64f507c181dde137a3710eb9bc5cd1b895a81f6e"

C50A_ARTIFACTS = {
    "owner_compact_result": (
        "deliverables/cm2_round306c50a_pair1_two_task_global_owner_result_v1.json",
        "cdec578a1bc86a939b320676f59f859243eb7dc135f2fd5e5a727ac73f419241",
    ),
    "owner_compact_audit": (
        "deliverables/cm2_round306c50a_pair1_two_task_global_owner_independent_verification_v1.json",
        "b69457f93f982c73a850407d2d9f9fa5c39102b3ee6a23c5850e9428c0618f5c",
    ),
    "owner_full_candidate_bundle": (
        "deliverables/cm2_round306c50a_pair1_two_task_global_owner_full_candidate_v1.json.gz.b64",
        "3a747cc92700bccc763d6cbf71ece51ebf5d3f5709b330a768c089099025174a",
    ),
    "owner_full_audit_bundle": (
        "deliverables/cm2_round306c50a_pair1_two_task_global_owner_full_independent_audit_v1.json.gz.b64",
        "71102222dd9d8ffe7c21675447405fd65709e0a46122fd5a428326a076838f85",
    ),
    "owner_manifest": (
        "deliverables/cm2_round306c50a_global_codimension_owner_oracle_manifest_v1.sha256",
        "07444544362d8b25d7d5d735e17ad08057dfc459d166ade868a073c2ce4c50f6",
    ),
}
C50A_COMPACT_RESULT_OBJECT_SHA256 = "f16817bd52e954ba1e8135b1dbbdd11cfa0784acb1f7b7ad8d0f73bf78d1c2ed"
C50A_COMPACT_AUDIT_OBJECT_SHA256 = "d7d138bfb4c49f0a43db7f43103e51fe3441475ad2244b9d8233762acf7e8ac0"
C50A_FULL_RESULT_FILE_SHA256 = "0c3ffd0a9ff26fd128366a6af22aabeb29f72346303988deb4773b5adcd4131e"
C50A_FULL_RESULT_OBJECT_SHA256 = "da4557c64b4ce9675a3f8bff8a250b7ec7b643c48aecd738c03b7abed01d0b82"
C50A_FULL_AUDIT_FILE_SHA256 = "5068afb70ec8bf7fddc719324aeae4703fbc4e22d07a9b5555e348471c23dd66"
C50A_FULL_AUDIT_OBJECT_SHA256 = "c037b3b15d19b839a254e3122bce7b1f882f6f9e198638c50a08909bf71231d6"
C50A_REQUEST_OBJECT_SHA256 = "db6292e002ec3c0b810f74af192524407afb1cfa3566c4898aa7fa7b2a8e3496"
C50A_HISTORY_HEAD_SHA256 = "543e2289de5a465745f821f510efa62ea2d4985921e2649b7404665ae71c730f"

C52_SOURCE_PATH = "deliverables/cm2_round306c52_d02a_pair1_no_producer_cold_route_verifier_v1.py"
C52_SOURCE_SHA256 = "6f7ab24f0439b2965e2f406cd9ee2e5078cd43020763a8b658fedf2bd34caeff"
C52_AUDIT_PATH = "deliverables/cm2_round306c52_d02a_pair1_no_producer_cold_route_audit_v1.json"
C52_AUDIT_FILE_SHA256 = "ff4ffe3862722d2ff6a00829cc4fb5f2e0ce691e823bd0f6f1918d783f7c7203"
C52_AUDIT_OBJECT_SHA256 = "1667032a6fbbc56cd53983275d8203c2480a2d31c3d4dc3f39b7efaed77ccec4"
C52_STATUS = (
    "PASS_C52_PAIR1_NO_PRODUCER_IMPORT_COLD_INDEPENDENT_ROUTE_MARGIN_"
    "REFLECTION_KRAFT_AND_CANDIDATE_REQUEST_AUDIT__ZERO_CREDIT"
)

CANDIDATE_SOURCE_PATH = "deliverables/cm2_round306c53_d02a_pair1_pair_level_successor_candidate_v1.py"
CANDIDATE_SOURCE_SHA256 = "c251d1d8bd7ae8f4988824021b0533dc796672939dcb1385d9cafa41fa1152e4"
CANDIDATE_RESULT_PATH = "deliverables/cm2_round306c53_d02a_pair1_pair_level_successor_candidate_result_v1.json"
CANDIDATE_RESULT_FILE_SHA256 = "a145e8a67a8f715f61d06c22943c9be40c2470e22da074add440253b9df794d3"
CANDIDATE_OBJECT_SHA256 = "996b1f213e7fc5a315348a9698960d29a07fd45c0e52c54680961007a28ef052"
SUCCESSOR_CHECKPOINT_OBJECT_SHA256 = "a1566f78ec92d431aad6ef8f495947e204304a75ebdc81d558031e4dd83fe6a7"
PAIR_TRANSACTION_OBJECT_SHA256 = "f235583e44679fa19ed470dfe40a884378bd322dc4bb852d34b9e3a246470fb2"
CANDIDATE_CLAIM_TEMPLATE_OBJECT_SHA256 = "abeb575fa8aa4e93f207412ba7450ad91bd444e93403b68d6c60c51ca9363a3d"
CANDIDATE_STATUS = (
    "PASS_C53_PAIR1_ATOMIC_PAIR_LEVEL_SUCCESSOR_CANDIDATE__"
    "NO_REPLACE_SEAL_PENDING__ZERO_D02_GATE_CREDIT"
)

INDEPENDENT_VERIFIER_PATH = (
    "deliverables/cm2_round306c53_d02a_pair1_pair_level_successor_"
    "independent_verifier_v1.py"
)
INDEPENDENT_VERIFIER_SHA256 = "ac6ae0eed9841df386785194bdbb3927736207cef0641dc2f462c9892932b136"
INDEPENDENT_VERIFIER_SIDECAR_PATH = INDEPENDENT_VERIFIER_PATH + ".sha256"
INDEPENDENT_VERIFIER_SIDECAR_FILE_SHA256 = "6ba7ffc354f0fc3b685d2bd6e8bf94b6802d5ffbc5abc3ae8983c9f2b9051b9f"
INDEPENDENT_AUDIT_PATH = (
    "deliverables/cm2_round306c53_d02a_pair1_pair_level_successor_"
    "independent_audit_v1.json"
)
INDEPENDENT_AUDIT_FILE_SHA256 = "b58a6ba170e43be02ca414208e7197e746183dd335a49982b9ae28dab919497b"
INDEPENDENT_AUDIT_OBJECT_SHA256 = "a7bee7e57b6527c7bf9ea7f17966379c62a722fe9ce2ce2009f19f85a5afaa7c"
INDEPENDENT_AUDIT_SIDECAR_PATH = INDEPENDENT_AUDIT_PATH + ".sha256"
INDEPENDENT_AUDIT_SIDECAR_FILE_SHA256 = "e53a55851546dabaddd7373d1a173d22758f318d37037c85ec913c2ec41cdbcd"
PROMOTION_DERIVATION_OBJECT_SHA256 = "760bbb0098a88995ec9a0e5e340058e72a4074d386a352eb0d34c076b1ea462c"
EFFECTIVE_CHECKPOINT_OBJECT_SHA256 = "b58d68a0234b8a7de0e9147f891d37910476d622b840cfa073aed7ff3b4382ab"
INDEPENDENT_REPORT_PATH = (
    "deliverables/cm2_round306c53_d02a_pair1_pair_level_successor_"
    "independent_report_v1.md"
)
INDEPENDENT_REPORT_FILE_SHA256 = "4f7e10ebc74a1d84b5ccfacd03f78f478f4ac1a68368a54f9dd8054e0e0e80fb"
INDEPENDENT_REPORT_SIDECAR_PATH = INDEPENDENT_REPORT_PATH + ".sha256"
INDEPENDENT_REPORT_SIDECAR_FILE_SHA256 = "09a0286b12c0c408da23c8c045621a4aba84951e1502674c25fbab43c216291f"
INDEPENDENT_MANIFEST_PATH = (
    "deliverables/cm2_round306c53_d02a_pair1_pair_level_successor_"
    "independent_manifest_v1.sha256"
)
INDEPENDENT_MANIFEST_FILE_SHA256 = "3403098e000b2436e4587817286c65c253bc610fa5692af1f57fed692512776f"
INDEPENDENT_MANIFEST_SIDECAR_PATH = INDEPENDENT_MANIFEST_PATH + ".sha256"
INDEPENDENT_MANIFEST_SIDECAR_FILE_SHA256 = "8eba2a7c2b5c2b3592f40702464cd27d6fb0966a5e0820fab3182cf9c646bfbf"

BEFORE = {
    "logical_pending_task_count": 33_640,
    "two_side_pending_occurrence_count": 67_280,
    "paired_coarse_cells": 574,
    "unresolved_coarse_cells": 1_150,
    "representative_parents_remaining": 575,
}
AFTER = {
    "logical_pending_task_count": 33_638,
    "two_side_pending_occurrence_count": 67_276,
    "paired_coarse_cells": 576,
    "unresolved_coarse_cells": 1_148,
    "representative_parents_remaining": 574,
}
C50D_BEFORE = {**BEFORE, "whole_representative_parent_count": 287}
C50D_AFTER = {**AFTER, "whole_representative_parent_count": 288}
D02_FORMAL_BEFORE = {
    "EARLIEST_PREFIX_EXCLUDED": 75_386,
    "TYPED_EVENT_GRAPH": 296,
    "CONNECTED_TO_KNOWN": 0,
    "SOURCE_GRAZING_OR_CEMETERY": 0,
    "UNRESOLVED_R1648_CONTINUATION": 1_150,
    "total": 76_832,
}
D02_FORMAL_AFTER = {
    "EARLIEST_PREFIX_EXCLUDED": 75_388,
    "TYPED_EVENT_GRAPH": 296,
    "CONNECTED_TO_KNOWN": 0,
    "SOURCE_GRAZING_OR_CEMETERY": 0,
    "UNRESOLVED_R1648_CONTINUATION": 1_148,
    "total": 76_832,
}
ZERO_LOCK = {
    "ambient_credit": 0,
    "terminal_credit": 0,
    "whole_parent_credit": 0,
    "D02_gate_credit": 0,
    "formal_credit": 0,
}

CANDIDATE_PARENT = "c53-pair-successor-candidates"
AUDIT_PARENT = "c53-pair-successor-audits"
CANDIDATE_TOKEN = (
    "c53-pair1-gen1-" + SUCCESSOR_CHECKPOINT_OBJECT_SHA256[:12]
    + "-" + CANDIDATE_OBJECT_SHA256[:12] + "-v1"
)
AUDIT_TOKEN = "c53-independent-audit-" + INDEPENDENT_AUDIT_OBJECT_SHA256[:12] + "-v1"
CANDIDATE_POINTER = "c53-current-pair-successor-token"
AUDIT_POINTER = "c53-current-pair-successor-audit-token"
RELEASE_ID = (
    "c53-pair1-gen1-" + CANDIDATE_OBJECT_SHA256[:12]
    + "-" + INDEPENDENT_AUDIT_OBJECT_SHA256[:12] + "-v1"
)
CANDIDATE_POINTER_BYTES = (CANDIDATE_TOKEN + "\n").encode("ascii")
AUDIT_POINTER_BYTES = (AUDIT_TOKEN + "\n").encode("ascii")

GLOBAL_CLAIM_PARENT = "cm2-global-successor-claims"
GLOBAL_HEAD_PARENT = "cm2-global-authority-heads"
GLOBAL_CLAIM_BASENAME = (
    "predecessor-" + C50D_PREDECESSOR_IDENTITY_SHA256 + ".claim"
)
GLOBAL_HEAD_BASENAME = (
    "predecessor-" + C50D_PREDECESSOR_IDENTITY_SHA256 + ".seal"
)
GLOBAL_CLAIM_PATH = (
    ".cm2-runtime/" + GLOBAL_CLAIM_PARENT + "/" + GLOBAL_CLAIM_BASENAME
)
GLOBAL_HEAD_PATH = (
    ".cm2-runtime/" + GLOBAL_HEAD_PARENT + "/" + GLOBAL_HEAD_BASENAME
)
GLOBAL_CLAIM_STAGE = (
    "." + GLOBAL_CLAIM_BASENAME + "." + RELEASE_ID + ".stage"
)
CANDIDATE_POINTER_STAGE = (
    "." + CANDIDATE_POINTER + "." + RELEASE_ID + ".stage"
)
AUDIT_POINTER_STAGE = "." + AUDIT_POINTER + "." + RELEASE_ID + ".stage"
GLOBAL_HEAD_STAGE = "." + GLOBAL_HEAD_BASENAME + "." + RELEASE_ID + ".stage"
C50D_ALLOWED_PREFIXES = {
    ("ABSENT", "ABSENT", "ABSENT", "ABSENT"),
    ("EXACT", "ABSENT", "ABSENT", "ABSENT"),
    ("EXACT", "EXACT", "ABSENT", "ABSENT"),
    ("EXACT", "EXACT", "EXACT", "ABSENT"),
    ("EXACT", "EXACT", "EXACT", "EXACT"),
}


class Reject(RuntimeError):
    pass


class WriteTracker:
    """Truthful fail-closed publication phase accounting."""

    def __init__(self) -> None:
        self.phase = "READ_ONLY"
        self.runtime_writes_may_have_occurred = False
        self.final_seal_fully_replayed = False
        self.final_seal_may_have_committed = False
        self.entered_write_phases: list[str] = []

    def before_write(self, phase: str) -> None:
        self.phase = phase
        self.runtime_writes_may_have_occurred = True
        self.entered_write_phases.append(phase)
        if phase == "FINAL_GLOBAL_HEAD_SEAL_LAST_WRITE":
            self.final_seal_may_have_committed = True

    def observe_possible_final_seal(self) -> None:
        self.final_seal_may_have_committed = True

    def seal_verified(self) -> None:
        self.phase = "FINAL_SEAL_FULLY_REPLAYED_READ_ONLY"
        self.final_seal_fully_replayed = True
        self.final_seal_may_have_committed = True


def failure_authority_fields(tracker: WriteTracker) -> dict[str, Any]:
    if tracker.final_seal_fully_replayed:
        return {
            "authority_state": "COMMITTED_AND_FULLY_REPLAYED",
            "effective_authoritative_census": C50D_AFTER,
            "seal_created": True,
            "verify_installed_required": False,
            "external_resolution_required": False,
        }
    if tracker.final_seal_may_have_committed:
        return {
            "authority_state": (
                "UNKNOWN_OR_FORK_REQUIRES_EXTERNAL_RESOLUTION"
            ),
            "effective_authoritative_census": None,
            "seal_created": None,
            "verify_installed_required": True,
            "external_resolution_required": True,
        }
    return {
        "authority_state": "PREDECESSOR_REMAINS_EFFECTIVE",
        "effective_authoritative_census": C50D_BEFORE,
        "seal_created": False,
        "verify_installed_required": False,
        "external_resolution_required": False,
    }


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


def file_digest(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def object_digest(value: dict[str, Any], field: str) -> str:
    body = dict(value)
    need(field in body, "self-hash field present:" + field)
    body.pop(field)
    return digest(body)


def close_object(value: dict[str, Any], field: str) -> dict[str, Any]:
    need(field not in value, "fresh self-hash field:" + field)
    return {**value, field: digest(value)}


def duplicate_literal_dict_keys(source: str) -> list[str]:
    duplicates: list[str] = []
    tree = ast.parse(source, filename=str(SELF))
    for node in ast.walk(tree):
        if not isinstance(node, ast.Dict):
            continue
        seen: set[tuple[type[Any], Any]] = set()
        for key in node.keys:
            if not isinstance(key, ast.Constant):
                continue
            try:
                marker = (type(key.value), key.value)
                if marker in seen:
                    duplicates.append(
                        str(key.value) + "@" + str(getattr(key, "lineno", 0))
                    )
                seen.add(marker)
            except TypeError:
                continue
    return duplicates


def pins_frozen(values: tuple[str, ...]) -> bool:
    return all(HEX64.fullmatch(value) is not None for value in values)


def all_terminal_pins_frozen() -> bool:
    pins = (
        C51_RESULT_FILE_SHA256,
        C52_SOURCE_SHA256,
        C52_AUDIT_FILE_SHA256,
        C52_AUDIT_OBJECT_SHA256,
        CANDIDATE_SOURCE_SHA256,
        CANDIDATE_RESULT_FILE_SHA256,
        CANDIDATE_OBJECT_SHA256,
        SUCCESSOR_CHECKPOINT_OBJECT_SHA256,
        PAIR_TRANSACTION_OBJECT_SHA256,
        CANDIDATE_CLAIM_TEMPLATE_OBJECT_SHA256,
        INDEPENDENT_VERIFIER_SHA256,
        INDEPENDENT_VERIFIER_SIDECAR_FILE_SHA256,
        INDEPENDENT_AUDIT_FILE_SHA256,
        INDEPENDENT_AUDIT_SIDECAR_FILE_SHA256,
        INDEPENDENT_AUDIT_OBJECT_SHA256,
        PROMOTION_DERIVATION_OBJECT_SHA256,
        EFFECTIVE_CHECKPOINT_OBJECT_SHA256,
        INDEPENDENT_REPORT_FILE_SHA256,
        INDEPENDENT_REPORT_SIDECAR_FILE_SHA256,
        INDEPENDENT_MANIFEST_FILE_SHA256,
        INDEPENDENT_MANIFEST_SIDECAR_FILE_SHA256,
    )
    return pins_frozen(pins)


def strict_json(raw: bytes, label: str, *, canonical_line: bool = True) -> dict[str, Any]:
    need(b"\x00" not in raw and not raw.startswith(b"\xef\xbb\xbf"),
         label + ": byte hygiene")

    def pairs(items: list[tuple[str, Any]]) -> dict[str, Any]:
        value: dict[str, Any] = {}
        for key, item in items:
            need(key not in value, label + ": duplicate key:" + key)
            value[key] = item
        return value

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


def fingerprint(info: os.stat_result) -> tuple[int, ...]:
    return (
        info.st_dev, info.st_ino, info.st_mode, info.st_nlink, info.st_uid,
        info.st_gid, info.st_size, info.st_mtime_ns, info.st_ctime_ns,
    )


class Capture:
    """Stable, held-open, O_NOFOLLOW input capture."""

    def __init__(
        self, path: Path, label: str, expected: str, maximum: int = 1 << 30,
        *, workspace_only: bool = True,
    ):
        need(HEX64.fullmatch(expected) is not None, label + ": complete SHA pin")
        self.path = path.absolute()
        self.label = label
        if workspace_only:
            need(ROOT == self.path or ROOT in self.path.parents,
                 label + ": workspace path")
            cursor = ROOT
            for part in self.path.relative_to(ROOT).parts[:-1]:
                cursor /= part
                need(not stat.S_ISLNK(os.lstat(cursor).st_mode),
                     label + ": no symlink parent")
        self.fd = os.open(self.path, os.O_RDONLY | os.O_CLOEXEC | os.O_NOFOLLOW)
        self.before = os.fstat(self.fd)
        need(
            stat.S_ISREG(self.before.st_mode) and self.before.st_nlink == 1
            and self.before.st_uid == os.getuid()
            and 0 < self.before.st_size <= maximum,
            label + ": owned singleton bounded regular",
        )
        self.raw = self._read()
        self.sha256 = file_digest(self.raw)
        need(self.sha256 == expected, label + ": pinned SHA-256")
        self.unchanged("initial")

    def _read(self) -> bytes:
        os.lseek(self.fd, 0, os.SEEK_SET)
        chunks: list[bytes] = []
        total = 0
        while True:
            block = os.read(self.fd, 4 << 20)
            if not block:
                break
            total += len(block)
            need(total <= self.before.st_size, self.label + ": read bound")
            chunks.append(block)
        need(total == self.before.st_size, self.label + ": exact read")
        return b"".join(chunks)

    def unchanged(self, phase: str) -> None:
        path_info = os.stat(self.path, follow_symlinks=False)
        need(
            fingerprint(path_info) == fingerprint(os.fstat(self.fd))
            == fingerprint(self.before),
            self.label + ": " + phase + " stable identity",
        )
        need(file_digest(self._read()) == self.sha256,
             self.label + ": " + phase + " stable bytes")

    def close(self) -> None:
        os.close(self.fd)


def expected_predecessor_identity() -> dict[str, Any]:
    value = close_object({
        "authority_heads": [
            {
                "authority_schema": C42_SEAL_SCHEMA,
                "role": "FORMAL_COARSE",
                "seal_file_sha256": C42_SEAL_FILE_SHA256,
                "seal_object_sha256": C42_SEAL_OBJECT_SHA256,
                "seal_path": C42_SEAL_PATH,
                "successor_checkpoint_object_sha256": None,
            },
            {
                "authority_schema": C48_SEAL_SCHEMA,
                "role": "LOGICAL_TASK",
                "seal_file_sha256": C48_SEAL_FILE_SHA256,
                "seal_object_sha256": C48_SEAL_OBJECT_SHA256,
                "seal_path": C48_SEAL_PATH,
                "successor_checkpoint_object_sha256":
                    C48_SUCCESSOR_OBJECT_SHA256,
            },
        ],
        "before_census": C50D_BEFORE,
        "ordered_head_roles": ["FORMAL_COARSE", "LOGICAL_TASK"],
        "schema": C50D_PREDECESSOR_IDENTITY_SCHEMA,
    }, "predecessor_identity_sha256")
    need(
        value["predecessor_identity_sha256"]
        == C50D_PREDECESSOR_IDENTITY_SHA256,
        "C50d legacy predecessor identity frozen hash",
    )
    return value


def validate_c42(value: dict[str, Any]) -> None:
    need(
        value.get("schema") == C42_SEAL_SCHEMA
        and value.get("status") == C42_STATUS
        and value.get("authority_seal_object_sha256")
        == C42_SEAL_OBJECT_SHA256
        and object_digest(value, "authority_seal_object_sha256")
        == C42_SEAL_OBJECT_SHA256
        and value.get("candidate_pointer_sha256")
        == C42_CANDIDATE_POINTER_SHA256
        and value.get("audit_pointer_sha256") == C42_AUDIT_POINTER_SHA256
        and value.get("formal_census_after_commit") == {
            "paired_coarse_cells": 574,
            "remaining_representatives": 575,
            "unresolved": 1_150,
            "whole_representatives": 287,
        },
        "C42 exact installed formal predecessor",
    )


def validate_c48(value: dict[str, Any]) -> None:
    need(
        value.get("schema") == C48_SEAL_SCHEMA
        and value.get("authority_seal_object_sha256") == C48_SEAL_OBJECT_SHA256
        and object_digest(value, "authority_seal_object_sha256")
        == C48_SEAL_OBJECT_SHA256
        and value.get("successor_checkpoint_object_sha256") == C48_SUCCESSOR_OBJECT_SHA256
        and value.get("status") == C48_STATUS
        and value.get("receipt_file_sha256") == C48_RECEIPT_FILE_SHA256
        and value.get("receipt_object_sha256") == C48_RECEIPT_OBJECT_SHA256
        and value.get("receipt_path") == C48_RECEIPT_PATH
        and value.get("candidate_pointer_sha256")
        == C48_CANDIDATE_POINTER_SHA256
        and value.get("audit_pointer_sha256") == C48_AUDIT_POINTER_SHA256
        and value.get("coarse_formal_authority_unchanged") == {
            "paired_coarse_cells": 574,
            "unresolved_coarse_cells": 1_150,
            "representative_parents_remaining": 575,
        },
        "C48 exact installed global predecessor",
    )


def validate_c48_receipt(value: dict[str, Any], c42: dict[str, Any],
                         c48: dict[str, Any]) -> None:
    need(
        value.get("receipt_object_sha256") == C48_RECEIPT_OBJECT_SHA256
        and object_digest(value, "receipt_object_sha256")
        == C48_RECEIPT_OBJECT_SHA256
        and value.get("release_id") == c48.get("release_id")
        and value.get("candidate", {}).get("successor_checkpoint_object_sha256")
        == C48_SUCCESSOR_OBJECT_SHA256
        and value.get("candidate", {}).get("candidate_object_sha256")
        == c48.get("candidate_object_sha256")
        and value.get("audit", {}).get("audit_object_sha256")
        == c48.get("audit_object_sha256")
        and value.get("pointer_intent", {}).get("candidate_pointer_sha256")
        == C48_CANDIDATE_POINTER_SHA256
        and value.get("pointer_intent", {}).get("audit_pointer_sha256")
        == C48_AUDIT_POINTER_SHA256
        and value.get("predecessor_authority") == {
            "c42-current-audit-token": C42_AUDIT_POINTER_SHA256,
            "c42-current-authority-seal": C42_SEAL_FILE_SHA256,
            "c42-current-token": C42_CANDIDATE_POINTER_SHA256,
        }
        and c42.get("candidate_pointer_sha256")
        == C42_CANDIDATE_POINTER_SHA256
        and c42.get("audit_pointer_sha256") == C42_AUDIT_POINTER_SHA256,
        "C48 receipt exact transitive C42/pointer bindings",
    )


def validate_c50d(protocol: bytes, companion: bytes) -> None:
    expected_companion = (
        C50D_PROTOCOL_FILE_SHA256 + "  "
        + Path(C50D_PROTOCOL_PATH).name + "\n"
    ).encode("ascii")
    need(
        file_digest(protocol) == C50D_PROTOCOL_FILE_SHA256
        and file_digest(companion) == C50D_PROTOCOL_COMPANION_FILE_SHA256
        and companion == expected_companion
        and C50D_PREDECESSOR_IDENTITY_SCHEMA.encode() in protocol
        and C50D_CLAIM_SCHEMA.encode() in protocol
        and b".cm2-runtime/cm2-global-successor-claims" in protocol
        and b".cm2-runtime/cm2-global-authority-heads" in protocol
        and b"predecessor-<P>.claim" in protocol
        and b"predecessor-<P>.seal" in protocol,
        "C50d protocol/companion exact bytes",
    )


def validate_c52(value: dict[str, Any]) -> None:
    need(
        value.get("object_sha256") == C52_AUDIT_OBJECT_SHA256
        and object_digest(value, "object_sha256") == C52_AUDIT_OBJECT_SHA256
        and value.get("status") == C52_STATUS
        and value.get("formal_credit") == 0,
        "C52 exact terminal cold audit",
    )


def validate_candidate(value: dict[str, Any]) -> None:
    need(
        value.get("schema")
        == "cm2.round306c53.d02-a-pair1-pair-level-successor-candidate.v1"
        and value.get("object_sha256") == CANDIDATE_OBJECT_SHA256
        and object_digest(value, "object_sha256") == CANDIDATE_OBJECT_SHA256
        and value.get("status") == CANDIDATE_STATUS
        and value.get("source") == {
            "path": CANDIDATE_SOURCE_PATH,
            "sha256": CANDIDATE_SOURCE_SHA256,
        }
        and value.get("formal_credit") == 0,
        "C53 candidate self-hash/status",
    )
    selection = value.get("selection", {})
    predecessor = value.get("predecessors", {})
    local = predecessor.get("local_C46_shard9_generation0", {})
    formal_predecessor = predecessor.get("formal_C42_authority", {})
    global_predecessor = predecessor.get("logical_C48_authority", {})
    transaction = value.get("pair_transaction", {})
    successor = value.get("successor", {})
    claim = value.get("global_predecessor_claim_template", {})
    identity = expected_predecessor_identity()
    need(
        selection.get("pair_index") == PAIR
        and selection.get("task_count") == 2
        and selection.get("task_indices") == [0, 1]
        and selection.get("task_binding_sha256s") == TASK_BINDINGS
        and selection.get("frontiers") == FRONTIERS
        and selection.get("logical_leaf_count") == 9
        and selection.get("physical_side_terminal_count") == 18
        and local.get("checkpoint_object_sha256") == GENESIS_CHECKPOINT_OBJECT_SHA256
        and local.get("shard_id") == SHARD_ID
        and local.get("shard_index") == SHARD_INDEX
        and local.get("task_count") == SHARD_TASK_COUNT
        and local.get("ordered_task_binding_sequence_sha256")
        == SHARD_BINDING_SEQUENCE_SHA256
        and formal_predecessor.get("seal_file_sha256")
        == C42_SEAL_FILE_SHA256
        and formal_predecessor.get("seal_object_sha256")
        == C42_SEAL_OBJECT_SHA256
        and formal_predecessor.get("formal_census_after_commit") == {
            "paired_coarse_cells": 574,
            "remaining_representatives": 575,
            "unresolved": 1_150,
            "whole_representatives": 287,
        }
        and global_predecessor.get("seal_file_sha256") == C48_SEAL_FILE_SHA256
        and global_predecessor.get("seal_object_sha256") == C48_SEAL_OBJECT_SHA256
        and global_predecessor.get("successor_checkpoint_object_sha256")
        == C48_SUCCESSOR_OBJECT_SHA256,
        "C53 candidate exact selection/predecessors",
    )
    need(
        transaction.get("pair_transaction_object_sha256")
        == PAIR_TRANSACTION_OBJECT_SHA256
        and object_digest(transaction, "pair_transaction_object_sha256")
        == PAIR_TRANSACTION_OBJECT_SHA256
        and transaction.get("task_indices") == [0, 1]
        and transaction.get("task_binding_sha256s") == TASK_BINDINGS
        and transaction.get("successor_checkpoint_object_sha256")
        == SUCCESSOR_CHECKPOINT_OBJECT_SHA256
        and transaction.get("global_predecessor_authority_identity") == identity
        and transaction.get("global_predecessor_authority_seal_object_sha256")
        == C48_SEAL_OBJECT_SHA256
        and transaction.get("global_predecessor_successor_checkpoint_object_sha256")
        == C48_SUCCESSOR_OBJECT_SHA256
        and transaction.get("local_predecessor_checkpoint_object_sha256")
        == GENESIS_CHECKPOINT_OBJECT_SHA256
        and transaction.get("zero_credit_candidate_authority_effect", {}).get("before")
        == BEFORE
        and transaction.get("zero_credit_candidate_authority_effect", {}).get("after")
        == BEFORE
        and transaction.get("zero_credit_candidate_authority_effect", {}).get(
            "C50d_before_census"
        ) == C50D_BEFORE
        and transaction.get("zero_credit_candidate_authority_effect", {}).get(
            "task_formal_closed_count"
        ) == 0
        and transaction.get("zero_credit_candidate_authority_effect", {}).get(
            "whole_parent_credit"
        ) == 0
        and transaction.get("zero_credit_candidate_authority_effect", {}).get(
            "D02_gate_credit"
        ) == 0
        and transaction.get("atomicity") == {
            "both_tasks_or_neither": True,
            "single_pair_level_seal_required": True,
            "task_level_partial_credit_forbidden": True,
            "seal_is_only_semantic_commit": True,
        },
        "C53 exact atomic pair transaction",
    )
    prospective = transaction.get("prospective_post_audit_and_seal_promotion", {})
    need(
        prospective.get("before") == BEFORE
        and prospective.get("after") == AFTER
        and prospective.get("C50d_before_census") == C50D_BEFORE
        and prospective.get("C50d_after_census") == C50D_AFTER
        and prospective.get("task_formal_closed_count") == 2
        and prospective.get("whole_parent_credit") == 1
        and prospective.get("D02_gate_credit") == 0
        and prospective.get("independent_C53_promotion_derivation_required")
        is True
        and prospective.get("promotion_derivation_not_minted_by_candidate")
        is True,
        "C53 prospective promotion exact and unauthoritative",
    )
    publication = claim.get("publication", {})
    need(
        claim.get("claim_template_object_sha256")
        == CANDIDATE_CLAIM_TEMPLATE_OBJECT_SHA256
        and object_digest(claim, "claim_template_object_sha256")
        == CANDIDATE_CLAIM_TEMPLATE_OBJECT_SHA256
        and claim.get("predecessor_authority_identity") == identity
        and claim.get("final_claim_schema") == C50D_CLAIM_SCHEMA
        and claim.get("unique_pair_transaction_object_sha256")
        == PAIR_TRANSACTION_OBJECT_SHA256
        and claim.get("unique_successor_checkpoint_object_sha256")
        == SUCCESSOR_CHECKPOINT_OBJECT_SHA256
        and claim.get("pair_index") == PAIR
        and claim.get("task_binding_sha256s") == TASK_BINDINGS
        and claim.get("candidate_does_not_mint_final_claim_or_promotion") is True
        and claim.get("D02_gate_credit") == 0
        and publication.get("claim_namespace") == GLOBAL_CLAIM_PARENT
        and publication.get("claim_basename") == GLOBAL_CLAIM_BASENAME
        and publication.get("claim_relative_path") == GLOBAL_CLAIM_PATH
        and publication.get("authority_seal_target_path") == GLOBAL_HEAD_PATH
        and publication.get("different_existing_bytes_are_a_fork_and_must_fail_closed")
        is True
        and publication.get("claim_without_authority_seal_is_reservation_only")
        is True,
        "C53 exact C50d predecessor claim template",
    )
    checkpoint_body = dict(successor)
    observed = checkpoint_body.pop("successor_checkpoint_object_sha256", None)
    need(
        observed == SUCCESSOR_CHECKPOINT_OBJECT_SHA256
        and digest(checkpoint_body) == SUCCESSOR_CHECKPOINT_OBJECT_SHA256
        and successor.get("shard_index") == SHARD_INDEX
        and successor.get("generation") == 1
        and successor.get("local_previous_checkpoint_object_sha256")
        == GENESIS_CHECKPOINT_OBJECT_SHA256
        and successor.get("global_previous_authority_seal_object_sha256")
        == C48_SEAL_OBJECT_SHA256
        and successor.get("selected_task_indices") == [0, 1]
        and successor.get("candidate_closed_task_count") == 2
        and successor.get("formal_closed_task_count_before_pair_seal") == 0
        and successor.get("pending_task_count_after_candidate") == 587
        and successor.get("unchanged_indices_2_through_588_byte_equal_to_genesis")
        is True
        and type(successor.get("task_states")) is list
        and len(successor["task_states"]) == SHARD_TASK_COUNT,
        "C53 exact shard9 generation-1 successor",
    )
    selected = successor["task_states"][:2]
    need(
        [row.get("task_binding_sha256") for row in selected] == TASK_BINDINGS
        and all(
            row.get("candidate_closed") is True
            and row.get("formal_closed") is False
            and row.get("credit_lock") == ZERO_LOCK
            for row in selected
        ),
        "C53 selected candidate tasks stay zero-lock before seal",
    )
    nonpromotion = value.get("strict_nonpromotion", {})
    need(
        nonpromotion.get("runtime_writes_performed") is False
        and nonpromotion.get("candidate_pointer_receipt_or_seal_created")
        is False
        and nonpromotion.get("post_seal_promotion_derivation_minted") is False
        and nonpromotion.get("whole_parent_credit") == 0
        and nonpromotion.get("D02_gate_credit") == 0
        and nonpromotion.get("formal_credit") == 0
        and nonpromotion.get("CM2") == "NO-GO_FOR_CLAIM",
        "C53 candidate strict nonpromotion",
    )


def validate_independent_audit(value: dict[str, Any]) -> None:
    need(
        value.get("schema")
        == "cm2.round306c53.d02-a-pair1-pair-level-successor."
        "independent-verifier.v1"
        and value.get("status")
        == "PASS_INDEPENDENT_C53_PAIR1_ATOMIC_TRANSACTION_589_STATE_862_"
        "CENSUS_AND_POST_SEAL_PROMOTION_AUDIT__ZERO_D02_GATE_CREDIT"
        and value.get("object_sha256") == INDEPENDENT_AUDIT_OBJECT_SHA256
        and object_digest(value, "object_sha256")
        == INDEPENDENT_AUDIT_OBJECT_SHA256
        and value.get("verifier") == {
            "path": INDEPENDENT_VERIFIER_PATH,
            "sha256": INDEPENDENT_VERIFIER_SHA256,
        }
        and value.get("formal_credit") == 0
        and value.get("D02_gate_credit") == 0,
        "C53 independent audit exact self-hash/status/verifier",
    )
    need(
        value.get("candidate") == {
            "file_sha256": CANDIDATE_RESULT_FILE_SHA256,
            "object_sha256": CANDIDATE_OBJECT_SHA256,
            "pair_transaction_object_sha256": PAIR_TRANSACTION_OBJECT_SHA256,
            "path": CANDIDATE_RESULT_PATH,
            "source_sha256": CANDIDATE_SOURCE_SHA256,
            "successor_checkpoint_object_sha256":
                SUCCESSOR_CHECKPOINT_OBJECT_SHA256,
        }
        and value.get("formal_predecessor", {}).get(
            "C42_authority_seal_object_sha256"
        ) == C42_SEAL_OBJECT_SHA256
        and value.get("logical_predecessor", {}).get(
            "C48_authority_seal_object_sha256"
        ) == C48_SEAL_OBJECT_SHA256
        and value.get("logical_predecessor", {}).get(
            "C48_receipt_file_sha256"
        ) == C48_RECEIPT_FILE_SHA256
        and value.get("logical_predecessor", {}).get(
            "C48_receipt_object_sha256"
        ) == C48_RECEIPT_OBJECT_SHA256
        and value.get("global_CAS_protocol", {}).get("predecessor_identity")
        == expected_predecessor_identity()
        and value.get("global_CAS_protocol", {}).get("file_sha256")
        == C50D_PROTOCOL_FILE_SHA256
        and value.get("global_CAS_protocol", {}).get("companion_file_sha256")
        == C50D_PROTOCOL_COMPANION_FILE_SHA256,
        "C53 audit exact candidate and predecessor bindings",
    )
    promotion = value.get("post_seal_promotion_derivation", {})
    effective = promotion.get("effective_post_seal_checkpoint", {})
    need(
        promotion.get("promotion_derivation_object_sha256")
        == PROMOTION_DERIVATION_OBJECT_SHA256
        and object_digest(promotion, "promotion_derivation_object_sha256")
        == PROMOTION_DERIVATION_OBJECT_SHA256
        and effective.get("effective_checkpoint_object_sha256")
        == EFFECTIVE_CHECKPOINT_OBJECT_SHA256
        and object_digest(effective, "effective_checkpoint_object_sha256")
        == EFFECTIVE_CHECKPOINT_OBJECT_SHA256
        and effective.get("candidate_zero_lock_checkpoint_object_sha256")
        == SUCCESSOR_CHECKPOINT_OBJECT_SHA256
        and effective.get("formal_closed_task_count") == 2
        and effective.get("pending_task_count") == 587
        and effective.get("selected_pair_index") == PAIR
        and effective.get("selected_task_indices") == [0, 1]
        and effective.get("pair_aggregate_whole_parent_credit") == 1
        and effective.get("individual_task_whole_parent_credit_sum") == 0
        and effective.get("D02_gate_credit") == 0
        and promotion.get("pair_transaction_object_sha256")
        == PAIR_TRANSACTION_OBJECT_SHA256
        and promotion.get("candidate_object_sha256") == CANDIDATE_OBJECT_SHA256
        and promotion.get("successor_checkpoint_object_sha256")
        == SUCCESSOR_CHECKPOINT_OBJECT_SHA256
        and promotion.get("shard9_state_projection_count") == 589
        and promotion.get("parent_projection_count") == 862
        and promotion.get("selected_task_formal_closed_count_after_seal") == 2
        and promotion.get("unchanged_nonselected_task_count") == 587,
        "C53 exact independent promotion/effective checkpoint",
    )
    census = promotion.get("global_census_transition", {})
    d02 = promotion.get("D02_four_class_census_transition", {})
    credit = promotion.get("pair_level_credit_transition", {})
    need(
        census.get("before") == BEFORE
        and census.get("after") == AFTER
        and census.get("whole_representatives_before") == 287
        and census.get("whole_representatives_after") == 288
        and census.get("pair_count") == 862
        and d02.get("before") == D02_FORMAL_BEFORE
        and d02.get("after_if_and_only_if_bound_seal_commits")
        == D02_FORMAL_AFTER
        and d02.get("class_total_conserved") is True
        and credit.get("before") == {
            "formal_closed_task_count": 0,
            "whole_parent_credit": 0,
            "D02_gate_credit": 0,
        }
        and credit.get("after_if_and_only_if_bound_seal_commits") == {
            "formal_closed_task_count": 2,
            "whole_parent_credit": 1,
            "D02_gate_credit": 0,
        }
        and credit.get("individual_task_whole_parent_credit_sum") == 0,
        "C53 promotion complete coarse/four-class/credit census",
    )
    attacks = value.get("coherent_attacks")
    independence = value.get("independence_boundary", {})
    nonpromotion = value.get("strict_nonpromotion", {})
    need(
        value.get("coherent_attack_count") == 28
        and type(attacks) is list and len(attacks) == 28
        and all(row.get("fail_closed") is True for row in attacks)
        and value.get("all_coherent_attacks_fail_closed") is True
        and independence.get("candidate_source_executed") is False
        and independence.get("candidate_source_parsed_as_inert_AST") is True
        and independence.get("duplicate_literal_key_count") == 0
        and independence.get("runtime_writes_performed") is False
        and value.get("immutability", {}).get(
            "pre_post_identity_and_byte_reread_equal"
        ) is True
        and nonpromotion.get("audit_is_not_authority") is True
        and nonpromotion.get("runtime_writes_performed") is False
        and nonpromotion.get("pointer_claim_receipt_or_seal_created") is False
        and nonpromotion.get("formal_credit") == 0
        and nonpromotion.get("D02_gate_credit") == 0,
        "C53 independent attacks/immutability/nonpromotion",
    )


def validate_independent_bundle_metadata(captures: dict[str, Capture]) -> None:
    sidecars = (
        ("independent_verifier_sidecar", INDEPENDENT_VERIFIER_SHA256,
         Path(INDEPENDENT_VERIFIER_PATH).name),
        ("independent_audit_sidecar", INDEPENDENT_AUDIT_FILE_SHA256,
         Path(INDEPENDENT_AUDIT_PATH).name),
        ("independent_report_sidecar", INDEPENDENT_REPORT_FILE_SHA256,
         Path(INDEPENDENT_REPORT_PATH).name),
        ("independent_manifest_sidecar", INDEPENDENT_MANIFEST_FILE_SHA256,
         Path(INDEPENDENT_MANIFEST_PATH).name),
    )
    need(all(
        captures[label].raw == (sha + "  " + basename + "\n").encode("ascii")
        for label, sha, basename in sidecars
    ), "C53 independent sidecars exact sha256sum bytes")
    expected = {
        Path(C46_SOURCE_PATH).name: C46_SOURCE_SHA256,
        Path(C50D_PROTOCOL_PATH).name: C50D_PROTOCOL_FILE_SHA256,
        Path(C50D_PROTOCOL_COMPANION_PATH).name:
            C50D_PROTOCOL_COMPANION_FILE_SHA256,
        Path(C51_RESULT_PATH).name: C51_RESULT_FILE_SHA256,
        Path(C50A_ARTIFACTS["owner_full_candidate_bundle"][0]).name:
            C50A_ARTIFACTS["owner_full_candidate_bundle"][1],
        Path(C50A_ARTIFACTS["owner_full_audit_bundle"][0]).name:
            C50A_ARTIFACTS["owner_full_audit_bundle"][1],
        Path(C52_SOURCE_PATH).name: C52_SOURCE_SHA256,
        Path(C52_AUDIT_PATH).name: C52_AUDIT_FILE_SHA256,
        Path(CANDIDATE_SOURCE_PATH).name: CANDIDATE_SOURCE_SHA256,
        Path(CANDIDATE_RESULT_PATH).name: CANDIDATE_RESULT_FILE_SHA256,
        Path(INDEPENDENT_VERIFIER_PATH).name: INDEPENDENT_VERIFIER_SHA256,
        Path(INDEPENDENT_AUDIT_PATH).name: INDEPENDENT_AUDIT_FILE_SHA256,
        Path(INDEPENDENT_REPORT_PATH).name: INDEPENDENT_REPORT_FILE_SHA256,
    }
    rows: dict[str, str] = {}
    lines = captures["independent_manifest"].raw.decode("ascii", "strict").splitlines()
    need(len(lines) == 13, "C53 independent manifest 13 rows")
    for line in lines:
        match = re.fullmatch(r"([0-9a-f]{64})  ([A-Za-z0-9_.-]+)", line)
        need(match is not None and match.group(2) not in rows,
             "C53 independent manifest strict unique row")
        rows[match.group(2)] = match.group(1)
    need(rows == expected, "C53 independent manifest exact 13 bindings")


class Inputs:
    def __init__(self, expected_installer_sha256: str):
        need(all_terminal_pins_frozen(), "all terminal source/file/object pins frozen")
        self.captures: dict[str, Capture] = {}
        self.captures["installer"] = Capture(SELF, "installer", expected_installer_sha256, 4 << 20)
        self.captures["C42_seal"] = Capture(
            ROOT / C42_SEAL_PATH, "C42 seal", C42_SEAL_FILE_SHA256, 4 << 20
        )
        self.captures["C42_candidate_pointer"] = Capture(
            ROOT / C42_CANDIDATE_POINTER_PATH, "C42 candidate pointer",
            C42_CANDIDATE_POINTER_SHA256, 4 << 20,
        )
        self.captures["C42_audit_pointer"] = Capture(
            ROOT / C42_AUDIT_POINTER_PATH, "C42 audit pointer",
            C42_AUDIT_POINTER_SHA256, 4 << 20,
        )
        self.captures["C48_seal"] = Capture(ROOT / C48_SEAL_PATH, "C48 seal", C48_SEAL_FILE_SHA256, 4 << 20)
        self.captures["C48_receipt"] = Capture(
            ROOT / C48_RECEIPT_PATH, "C48 receipt", C48_RECEIPT_FILE_SHA256,
            4 << 20,
        )
        self.captures["C48_candidate_pointer"] = Capture(
            ROOT / C48_CANDIDATE_POINTER_PATH, "C48 candidate pointer",
            C48_CANDIDATE_POINTER_SHA256, 4 << 20,
        )
        self.captures["C48_audit_pointer"] = Capture(
            ROOT / C48_AUDIT_POINTER_PATH, "C48 audit pointer",
            C48_AUDIT_POINTER_SHA256, 4 << 20,
        )
        self.captures["C50d_protocol"] = Capture(
            ROOT / C50D_PROTOCOL_PATH, "C50d protocol",
            C50D_PROTOCOL_FILE_SHA256, 4 << 20,
        )
        self.captures["C50d_protocol_companion"] = Capture(
            ROOT / C50D_PROTOCOL_COMPANION_PATH, "C50d protocol companion",
            C50D_PROTOCOL_COMPANION_FILE_SHA256, 4 << 20,
        )
        self.captures["C46_source"] = Capture(
            ROOT / C46_SOURCE_PATH, "C46 source", C46_SOURCE_SHA256, 8 << 20
        )
        self.captures["C51_source"] = Capture(ROOT / C51_SOURCE_PATH, "C51 source", C51_SOURCE_SHA256, 4 << 20)
        self.captures["C51_report"] = Capture(ROOT / C51_REPORT_PATH, "C51 report", C51_REPORT_SHA256, 4 << 20)
        self.captures["C51_result"] = Capture(ROOT / C51_RESULT_PATH, "C51 result", C51_RESULT_FILE_SHA256)
        for label, (path, sha) in sorted(C50A_ARTIFACTS.items()):
            self.captures[label] = Capture(ROOT / path, label, sha)
        self.captures["C52_source"] = Capture(ROOT / C52_SOURCE_PATH, "C52 source", C52_SOURCE_SHA256, 8 << 20)
        self.captures["C52_audit"] = Capture(ROOT / C52_AUDIT_PATH, "C52 audit", C52_AUDIT_FILE_SHA256)
        self.captures["candidate_source"] = Capture(ROOT / CANDIDATE_SOURCE_PATH, "candidate source", CANDIDATE_SOURCE_SHA256, 8 << 20)
        self.captures["candidate_result"] = Capture(ROOT / CANDIDATE_RESULT_PATH, "candidate result", CANDIDATE_RESULT_FILE_SHA256)
        self.captures["independent_verifier"] = Capture(
            ROOT / INDEPENDENT_VERIFIER_PATH, "independent verifier",
            INDEPENDENT_VERIFIER_SHA256, 8 << 20,
        )
        self.captures["independent_verifier_sidecar"] = Capture(
            ROOT / INDEPENDENT_VERIFIER_SIDECAR_PATH,
            "independent verifier sidecar",
            INDEPENDENT_VERIFIER_SIDECAR_FILE_SHA256, 4 << 20,
        )
        self.captures["independent_audit"] = Capture(
            ROOT / INDEPENDENT_AUDIT_PATH, "independent audit",
            INDEPENDENT_AUDIT_FILE_SHA256,
        )
        self.captures["independent_audit_sidecar"] = Capture(
            ROOT / INDEPENDENT_AUDIT_SIDECAR_PATH,
            "independent audit sidecar",
            INDEPENDENT_AUDIT_SIDECAR_FILE_SHA256, 4 << 20,
        )
        self.captures["independent_report"] = Capture(
            ROOT / INDEPENDENT_REPORT_PATH, "independent report",
            INDEPENDENT_REPORT_FILE_SHA256, 8 << 20,
        )
        self.captures["independent_report_sidecar"] = Capture(
            ROOT / INDEPENDENT_REPORT_SIDECAR_PATH,
            "independent report sidecar",
            INDEPENDENT_REPORT_SIDECAR_FILE_SHA256, 4 << 20,
        )
        self.captures["independent_manifest"] = Capture(
            ROOT / INDEPENDENT_MANIFEST_PATH, "independent manifest",
            INDEPENDENT_MANIFEST_FILE_SHA256, 8 << 20,
        )
        self.captures["independent_manifest_sidecar"] = Capture(
            ROOT / INDEPENDENT_MANIFEST_SIDECAR_PATH,
            "independent manifest sidecar",
            INDEPENDENT_MANIFEST_SIDECAR_FILE_SHA256, 4 << 20,
        )
        c42 = strict_json(self.captures["C42_seal"].raw, "C42 seal")
        c48 = strict_json(self.captures["C48_seal"].raw, "C48 seal")
        c48_receipt = strict_json(
            self.captures["C48_receipt"].raw, "C48 receipt"
        )
        validate_c42(c42)
        validate_c48(c48)
        validate_c48_receipt(c48_receipt, c42, c48)
        need(
            self.captures["C42_candidate_pointer"].raw
            == (c42["candidate_token"] + "\n").encode("ascii")
            and self.captures["C42_audit_pointer"].raw
            == (c42["audit_token"] + "\n").encode("ascii")
            and self.captures["C48_candidate_pointer"].raw
            == (c48["candidate_token"] + "\n").encode("ascii")
            and self.captures["C48_audit_pointer"].raw
            == (c48["audit_token"] + "\n").encode("ascii"),
            "C42/C48 exact live pointer bytes",
        )
        validate_c50d(
            self.captures["C50d_protocol"].raw,
            self.captures["C50d_protocol_companion"].raw,
        )
        route = strict_json(self.captures["C51_result"].raw, "C51 result")
        need(route.get("object_sha256") == C51_OBJECT_SHA256
             and object_digest(route, "object_sha256") == C51_OBJECT_SHA256,
             "C51 route object self-hash")
        validate_c52(strict_json(self.captures["C52_audit"].raw, "C52 audit"))
        validate_candidate(strict_json(self.captures["candidate_result"].raw, "candidate result"))
        validate_independent_audit(
            strict_json(self.captures["independent_audit"].raw,
                        "independent audit")
        )
        validate_independent_bundle_metadata(self.captures)

    def attest_all(self, phase: str) -> None:
        for label in sorted(self.captures):
            self.captures[label].unchanged(phase)

    def close(self) -> None:
        for capture in reversed(list(self.captures.values())):
            capture.close()


def node_at(directory_fd: int, name: str) -> os.stat_result | None:
    try:
        return os.stat(name, dir_fd=directory_fd, follow_symlinks=False)
    except FileNotFoundError:
        return None


def open_dir_at(directory_fd: int, name: str) -> int:
    fd = os.open(
        name, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW | os.O_CLOEXEC,
        dir_fd=directory_fd,
    )
    info = os.fstat(fd)
    need(stat.S_ISDIR(info.st_mode) and info.st_uid == os.getuid(),
         name + ": owned directory")
    return fd


def read_at(directory_fd: int, name: str, maximum: int) -> tuple[bytes, os.stat_result]:
    need(SAFE_NAME.fullmatch(name) is not None, "safe basename:" + name)
    fd = os.open(name, os.O_RDONLY | os.O_NOFOLLOW | os.O_CLOEXEC,
                 dir_fd=directory_fd)
    try:
        before = os.fstat(fd)
        need(
            stat.S_ISREG(before.st_mode) and before.st_nlink == 1
            and before.st_uid == os.getuid() and 0 < before.st_size <= maximum,
            name + ": strict installed file",
        )
        chunks: list[bytes] = []
        total = 0
        while True:
            block = os.read(fd, 4 << 20)
            if not block:
                break
            total += len(block)
            need(total <= maximum, name + ": read bound")
            chunks.append(block)
        after = os.fstat(fd)
        path_info = os.stat(name, dir_fd=directory_fd, follow_symlinks=False)
        need(fingerprint(before) == fingerprint(after) == fingerprint(path_info),
             name + ": stable installed reread")
        return b"".join(chunks), before
    finally:
        os.close(fd)


def write_once_at(directory_fd: int, name: str, payload: bytes,
                  mode: int = 0o444) -> None:
    need(SAFE_NAME.fullmatch(name) is not None, "safe output basename")
    fd = os.open(
        name,
        os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW | os.O_CLOEXEC,
        0o600, dir_fd=directory_fd,
    )
    try:
        view = memoryview(payload)
        offset = 0
        while offset < len(view):
            written = os.write(fd, view[offset:])
            need(written > 0, "write progress")
            offset += written
        os.fchmod(fd, mode)
        os.fsync(fd)
    finally:
        os.close(fd)
    raw, info = read_at(directory_fd, name, max(1, len(payload)))
    need(raw == payload and stat.S_IMODE(info.st_mode) == mode,
         name + ": exact staged terminal replay")
    os.fsync(directory_fd)


def rename_noreplace(source_fd: int, source_name: str,
                     target_fd: int, target_name: str) -> None:
    function = getattr(ctypes.CDLL(None, use_errno=True), "renameat2", None)
    need(function is not None, "renameat2(RENAME_NOREPLACE) available")
    function.argtypes = [ctypes.c_int, ctypes.c_char_p,
                         ctypes.c_int, ctypes.c_char_p, ctypes.c_uint]
    function.restype = ctypes.c_int
    result = function(
        source_fd, os.fsencode(source_name), target_fd,
        os.fsencode(target_name), 1,
    )
    if result == 0:
        return
    number = ctypes.get_errno()
    if number == errno.EEXIST:
        raise FileExistsError(number, os.strerror(number), target_name)
    raise OSError(number, os.strerror(number), target_name)


def ensure_parent(runtime_fd: int, name: str) -> int:
    info = node_at(runtime_fd, name)
    if info is None:
        os.mkdir(name, 0o700, dir_fd=runtime_fd)
        os.fsync(runtime_fd)
    else:
        need(stat.S_ISDIR(info.st_mode) and not stat.S_ISLNK(info.st_mode)
             and info.st_uid == os.getuid(), name + ": existing owned directory")
    return open_dir_at(runtime_fd, name)


def exact_or_absent(directory_fd: int, name: str, payload: bytes) -> str:
    info = node_at(directory_fd, name)
    if info is None:
        return "ABSENT"
    need(stat.S_ISREG(info.st_mode) and info.st_nlink == 1,
         name + ": exact existing regular")
    raw, row = read_at(directory_fd, name, max(1, len(payload)))
    need(raw == payload and stat.S_IMODE(row.st_mode) == 0o444,
         name + ": exact existing bytes/mode")
    return "EXACT"


def verify_terminal_file_no_stage(directory_fd: int, target: str, stage: str,
                                  payload: bytes) -> None:
    need(exact_or_absent(directory_fd, stage, payload) == "ABSENT",
         target + ": terminal target forbids leftover stage")
    need(exact_or_absent(directory_fd, target, payload) == "EXACT",
         target + ": exact terminal target")


def publish_file(runtime_fd: int, target: str, stage: str,
                 payload: bytes) -> str:
    target_state = exact_or_absent(runtime_fd, target, payload)
    stage_state = exact_or_absent(runtime_fd, stage, payload)
    if target_state == "EXACT":
        need(stage_state == "ABSENT", target + ": no leftover stage")
        return "RESUMED_EXACT"
    if stage_state == "ABSENT":
        write_once_at(runtime_fd, stage, payload)
    rename_noreplace(runtime_fd, stage, runtime_fd, target)
    os.fsync(runtime_fd)
    need(exact_or_absent(runtime_fd, target, payload) == "EXACT",
         target + ": post-publication replay")
    return "INSTALLED"


def installed_name(label: str, capture: Capture) -> str:
    return label + "__" + capture.path.name


def build_manifest(bundle: str, token: str, labels: list[str],
                   inputs: Inputs,
                   derived_payloads: dict[str, bytes] | None = None) -> dict[str, Any]:
    rows = []
    for label in sorted(labels):
        capture = inputs.captures[label]
        rows.append({
            "file_sha256": capture.sha256,
            "installed_name": installed_name(label, capture),
            "size": capture.before.st_size,
            "source_path": str(capture.path.relative_to(ROOT)),
        })
    for name, payload in sorted((derived_payloads or {}).items()):
        need(SAFE_NAME.fullmatch(name) is not None,
             "derived manifest safe installed name")
        rows.append({
            "file_sha256": file_digest(payload),
            "installed_name": name,
            "size": len(payload),
            "source_path": "DERIVED_AND_BOUND_BY_INDEPENDENT_AUDIT",
        })
    return close_object({
        "schema": MANIFEST_SCHEMA,
        "bundle": bundle,
        "token": token,
        "files": rows,
    }, "manifest_object_sha256")


def bundle_payloads(labels: list[str], manifest: dict[str, Any],
                    inputs: Inputs, receipt: dict[str, Any] | None = None,
                    derived_payloads: dict[str, bytes] | None = None) -> dict[str, bytes]:
    output = {
        installed_name(label, inputs.captures[label]): inputs.captures[label].raw
        for label in sorted(labels)
    }
    for name, payload in sorted((derived_payloads or {}).items()):
        need(name not in output and SAFE_NAME.fullmatch(name) is not None,
             "derived bundle unique safe member")
        output[name] = payload
    output["bundle_manifest.json"] = canonical(manifest) + b"\n"
    if receipt is not None:
        output["installation_receipt.json"] = canonical(receipt) + b"\n"
    return output


def validate_terminal_bundle_directory_stat(
    descriptor: os.stat_result, path_info: os.stat_result, token: str,
) -> None:
    need(
        fingerprint(descriptor) == fingerprint(path_info)
        and stat.S_ISDIR(descriptor.st_mode)
        and descriptor.st_uid == os.getuid()
        and descriptor.st_nlink == 2
        and path_info.st_nlink == 2
        and stat.S_IMODE(descriptor.st_mode) == 0o500,
        token + ": immutable owned singleton-level directory mode/link count",
    )


def verify_bundle(parent_fd: int, token: str,
                  payloads: dict[str, bytes]) -> None:
    directory_fd = open_dir_at(parent_fd, token)
    try:
        before = os.fstat(directory_fd)
        path_before = os.stat(token, dir_fd=parent_fd, follow_symlinks=False)
        validate_terminal_bundle_directory_stat(before, path_before, token)
        first_inventory = sorted(os.listdir(directory_fd))
        need(first_inventory == sorted(payloads),
             token + ": exact inventory")
        for name, payload in sorted(payloads.items()):
            raw, info = read_at(directory_fd, name, max(1, len(payload)))
            need(raw == payload and stat.S_IMODE(info.st_mode) == 0o444,
                 token + ": exact immutable member:" + name)
        after = os.fstat(directory_fd)
        path_after = os.stat(token, dir_fd=parent_fd, follow_symlinks=False)
        validate_terminal_bundle_directory_stat(after, path_after, token)
        need(
            sorted(os.listdir(directory_fd)) == first_inventory
            and fingerprint(before) == fingerprint(after)
            == fingerprint(path_before) == fingerprint(path_after),
            token + ": held directory remains terminal path identity",
        )
    finally:
        os.close(directory_fd)


def verify_terminal_bundle_no_stage(parent_fd: int, token: str,
                                    payloads: dict[str, bytes]) -> None:
    """Replay a published bundle and reject any post-publication stage."""
    need(node_at(parent_fd, "." + token + ".stage") is None,
         token + ": terminal bundle forbids leftover stage")
    verify_bundle(parent_fd, token, payloads)


def require_existing_claim_bundles(runtime_fd: int, state: dict[str, Any],
                                   opened: list[int]) -> None:
    """C50d S2/S3 recovery: an existing claim may not precede bundles."""
    for parent, token, payloads in (
        (CANDIDATE_PARENT, CANDIDATE_TOKEN, state["candidate_payloads"]),
        (AUDIT_PARENT, AUDIT_TOKEN, state["audit_payloads"]),
    ):
        info = node_at(runtime_fd, parent)
        need(
            info is not None and stat.S_ISDIR(info.st_mode)
            and not stat.S_ISLNK(info.st_mode) and info.st_uid == os.getuid(),
            parent + ": exact claim requires existing referenced bundle parent",
        )
        parent_fd = open_dir_at(runtime_fd, parent)
        opened.append(parent_fd)
        path_before = os.stat(parent, dir_fd=runtime_fd, follow_symlinks=False)
        need(fingerprint(os.fstat(parent_fd)) == fingerprint(path_before),
             parent + ": referenced bundle parent descriptor/path identity")
        verify_terminal_bundle_no_stage(parent_fd, token, payloads)
        path_after = os.stat(parent, dir_fd=runtime_fd, follow_symlinks=False)
        need(
            fingerprint(os.fstat(parent_fd)) == fingerprint(path_before)
            == fingerprint(path_after),
            parent + ": referenced bundle parent remains current path",
        )


def verify_existing_claim_bundles(runtime_fd: int,
                                  state: dict[str, Any]) -> None:
    opened: list[int] = []
    try:
        require_existing_claim_bundles(runtime_fd, state, opened)
    finally:
        for parent_fd in reversed(opened):
            os.close(parent_fd)


def classify_bundle_recovery(parent_fd: int, token: str,
                             payloads: dict[str, bytes]) -> str:
    """Read-only validation of an absent, final, or resumable bundle stage."""
    final_info = node_at(parent_fd, token)
    stage = "." + token + ".stage"
    stage_info = node_at(parent_fd, stage)
    if final_info is not None:
        need(stage_info is None,
             token + ": final bundle forbids leftover stage")
        verify_terminal_bundle_no_stage(parent_fd, token, payloads)
        return "FINAL_EXACT"
    if stage_info is None:
        return "ABSENT"
    need(
        stat.S_ISDIR(stage_info.st_mode) and not stat.S_ISLNK(stage_info.st_mode)
        and stage_info.st_uid == os.getuid() and stage_info.st_nlink == 2
        and stat.S_IMODE(stage_info.st_mode) in {0o700, 0o500},
        stage + ": read-only resumable exact owned directory",
    )
    stage_fd = open_dir_at(parent_fd, stage)
    try:
        before = os.fstat(stage_fd)
        path_before = os.stat(stage, dir_fd=parent_fd, follow_symlinks=False)
        need(fingerprint(before) == fingerprint(path_before),
             stage + ": read-only descriptor/path identity")
        inventory = sorted(os.listdir(stage_fd))
        need(set(inventory) <= set(payloads),
             stage + ": read-only exact inventory subset")
        for name in inventory:
            payload = payloads[name]
            raw, info = read_at(stage_fd, name, max(1, len(payload)))
            need(raw == payload and stat.S_IMODE(info.st_mode) == 0o444,
                 stage + ": read-only exact staged member:" + name)
        missing = set(payloads) - set(inventory)
        need(not missing or stat.S_IMODE(before.st_mode) == 0o700,
             stage + ": incomplete stage must be writable mode 0700")
        after = os.fstat(stage_fd)
        path_after = os.stat(stage, dir_fd=parent_fd, follow_symlinks=False)
        need(
            inventory == sorted(os.listdir(stage_fd))
            and fingerprint(before) == fingerprint(after)
            == fingerprint(path_before) == fingerprint(path_after),
            stage + ": read-only stable resumable stage",
        )
        inventory_sha = digest(inventory)[:16]
        return (
            "RESUMABLE_STAGE_" + str(len(inventory)) + "_OF_"
            + str(len(payloads)) + "__" + inventory_sha + "__M"
            + format(stat.S_IMODE(before.st_mode), "03o") + "__FILES_"
            + ",".join(inventory)
        )
    finally:
        os.close(stage_fd)


def classify_runtime_bundle(runtime_fd: int, parent: str, token: str,
                            payloads: dict[str, bytes]) -> str:
    info = node_at(runtime_fd, parent)
    if info is None:
        return "ABSENT"
    need(
        stat.S_ISDIR(info.st_mode) and not stat.S_ISLNK(info.st_mode)
        and info.st_uid == os.getuid(),
        parent + ": exact owned bundle namespace",
    )
    parent_fd = open_dir_at(runtime_fd, parent)
    try:
        before = os.fstat(parent_fd)
        path_before = os.stat(parent, dir_fd=runtime_fd, follow_symlinks=False)
        need(fingerprint(before) == fingerprint(path_before),
             parent + ": bundle namespace descriptor/path identity")
        result = classify_bundle_recovery(parent_fd, token, payloads)
        after = os.fstat(parent_fd)
        path_after = os.stat(parent, dir_fd=runtime_fd, follow_symlinks=False)
        need(
            fingerprint(before) == fingerprint(after)
            == fingerprint(path_before) == fingerprint(path_after),
            parent + ": bundle namespace remains current path",
        )
        return result
    finally:
        os.close(parent_fd)


def bundle_recovery_details(
    value: str,
) -> tuple[int, frozenset[str] | None, int | None, int | None]:
    if value == "ABSENT":
        return 0, frozenset(), 0, None
    if value == "FINAL_EXACT":
        return 1 << 30, None, None, None
    match = re.fullmatch(
        r"RESUMABLE_STAGE_([0-9]+)_OF_([0-9]+)__([0-9a-f]{16})__"
        r"M(500|700)__FILES_(.*)",
        value,
    )
    need(match is not None, "recognized bundle recovery state")
    count = int(match.group(1))
    total = int(match.group(2))
    inventory = [] if match.group(5) == "" else match.group(5).split(",")
    need(
        len(inventory) == count and len(set(inventory)) == count
        and all(SAFE_NAME.fullmatch(name) is not None for name in inventory)
        and digest(sorted(inventory))[:16] == match.group(3),
        "bundle recovery state exact inventory encoding",
    )
    return count + 1, frozenset(inventory), total, int(match.group(4), 8)


def bundle_recovery_progress(value: str) -> int:
    return bundle_recovery_details(value)[0]


def require_bundle_recovery_monotone(before: dict[str, str],
                                     after: dict[str, str],
                                     label: str) -> None:
    for key in ("candidate_bundle", "audit_bundle"):
        old_progress, old_members, old_total, old_mode = (
            bundle_recovery_details(before[key])
        )
        new_progress, new_members, new_total, new_mode = (
            bundle_recovery_details(after[key])
        )
        if old_members is None:
            need(new_members is None,
                 label + ": " + key + " final bundle regressed")
            continue
        if new_members is None:
            continue
        need(
            old_total in {0, new_total} and old_members <= new_members
            and new_progress >= old_progress,
            label + ": " + key + " must complete only absent members",
        )
        if old_members == new_members and old_mode is not None:
            need(not (old_mode == 0o500 and new_mode == 0o700),
                 label + ": " + key + " immutable stage mode regressed")


def validate_c50d_recovery_grammar(
    prefix: tuple[str, str, str, str],
    stages: tuple[str, str, str, str],
) -> None:
    need(prefix in C50D_ALLOWED_PREFIXES,
         "C50d exact claim-pointer-pointer-head publication prefix")
    need(all(value in {"ABSENT", "EXACT"} for value in stages),
         "C50d exact-or-absent file stages")
    for target, stage in zip(prefix, stages):
        need(not (target == "EXACT" and stage == "EXACT"),
             "C50d exact target forbids leftover stage")
    claim_stage, candidate_stage, audit_stage, head_stage = stages
    if claim_stage == "EXACT":
        need(prefix == ("ABSENT", "ABSENT", "ABSENT", "ABSENT"),
             "C50d claim stage requires pre-claim S0/S1 targets")
    if candidate_stage == "EXACT":
        need(prefix == ("EXACT", "ABSENT", "ABSENT", "ABSENT"),
             "C50d candidate-pointer stage requires exact claim")
    if audit_stage == "EXACT":
        need(prefix == ("EXACT", "EXACT", "ABSENT", "ABSENT"),
             "C50d audit-pointer stage requires exact claim/candidate pointer")
    if head_stage == "EXACT":
        need(prefix == ("EXACT", "EXACT", "EXACT", "ABSENT"),
             "C50d head stage requires exact claim and both pointers")


def classify_c50d_runtime(runtime_fd: int,
                          state: dict[str, Any]) -> dict[str, str]:
    """Read-only, stage-aware classification of the current C50d slot."""
    def namespaced(parent: str, target: str, stage: str,
                   payload: bytes) -> tuple[str, str]:
        info = node_at(runtime_fd, parent)
        if info is None:
            return "ABSENT", "ABSENT"
        need(
            stat.S_ISDIR(info.st_mode) and not stat.S_ISLNK(info.st_mode)
            and info.st_uid == os.getuid(),
            parent + ": exact owned namespace",
        )
        parent_fd = open_dir_at(runtime_fd, parent)
        try:
            before = os.fstat(parent_fd)
            path_before = os.stat(
                parent, dir_fd=runtime_fd, follow_symlinks=False
            )
            need(fingerprint(before) == fingerprint(path_before),
                 parent + ": namespace descriptor/path identity")
            target_state = exact_or_absent(parent_fd, target, payload)
            stage_state = exact_or_absent(parent_fd, stage, payload)
            after = os.fstat(parent_fd)
            path_after = os.stat(
                parent, dir_fd=runtime_fd, follow_symlinks=False
            )
            need(
                fingerprint(before) == fingerprint(after)
                == fingerprint(path_before) == fingerprint(path_after),
                parent + ": namespace remains current path",
            )
            return target_state, stage_state
        finally:
            os.close(parent_fd)

    candidate_bundle = classify_runtime_bundle(
        runtime_fd, CANDIDATE_PARENT, CANDIDATE_TOKEN,
        state["candidate_payloads"],
    )
    audit_bundle = classify_runtime_bundle(
        runtime_fd, AUDIT_PARENT, AUDIT_TOKEN, state["audit_payloads"],
    )
    claim, claim_stage = namespaced(
        GLOBAL_CLAIM_PARENT, GLOBAL_CLAIM_BASENAME, GLOBAL_CLAIM_STAGE,
        state["claim_raw"],
    )
    head, head_stage = namespaced(
        GLOBAL_HEAD_PARENT, GLOBAL_HEAD_BASENAME, GLOBAL_HEAD_STAGE,
        state["seal_raw"],
    )
    candidate = exact_or_absent(
        runtime_fd, CANDIDATE_POINTER, CANDIDATE_POINTER_BYTES
    )
    candidate_stage = exact_or_absent(
        runtime_fd, CANDIDATE_POINTER_STAGE, CANDIDATE_POINTER_BYTES
    )
    audit = exact_or_absent(
        runtime_fd, AUDIT_POINTER, AUDIT_POINTER_BYTES
    )
    audit_stage = exact_or_absent(
        runtime_fd, AUDIT_POINTER_STAGE, AUDIT_POINTER_BYTES
    )
    prefix = (claim, candidate, audit, head)
    stages = (claim_stage, candidate_stage, audit_stage, head_stage)
    validate_c50d_recovery_grammar(prefix, stages)
    if claim == "EXACT" or claim_stage == "EXACT":
        need(
            candidate_bundle == audit_bundle == "FINAL_EXACT",
            "C50d claim target/stage requires both terminal bundles",
        )
    return {
        "candidate_bundle": candidate_bundle,
        "audit_bundle": audit_bundle,
        "claim": claim,
        "candidate_pointer": candidate,
        "audit_pointer": audit,
        "global_head_seal": head,
        "claim_stage": claim_stage,
        "candidate_pointer_stage": candidate_stage,
        "audit_pointer_stage": audit_stage,
        "global_head_stage": head_stage,
    }


def reconcile_bundles_at_claim_barrier(
    claim_or_stage: str, candidate_parent_fd: int, audit_parent_fd: int,
    state: dict[str, Any],
) -> tuple[str, str]:
    """Publish only before a claim reservation; then bundles are read-only."""
    need(claim_or_stage in {"ABSENT", "EXACT"},
         "claim-or-stage barrier exact-or-absent")
    if claim_or_stage == "EXACT":
        verify_terminal_bundle_no_stage(
            candidate_parent_fd, CANDIDATE_TOKEN,
            state["candidate_payloads"],
        )
        verify_terminal_bundle_no_stage(
            audit_parent_fd, AUDIT_TOKEN, state["audit_payloads"],
        )
        return ("READ_ONLY_VERIFIED_EXACT_AFTER_CLAIM_RESERVATION",) * 2
    return (
        publish_bundle(
            candidate_parent_fd, CANDIDATE_TOKEN,
            state["candidate_payloads"],
        ),
        publish_bundle(
            audit_parent_fd, AUDIT_TOKEN, state["audit_payloads"],
        ),
    )


def publish_bundle(parent_fd: int, token: str,
                   payloads: dict[str, bytes]) -> str:
    existing = node_at(parent_fd, token)
    if existing is not None:
        need(stat.S_ISDIR(existing.st_mode) and not stat.S_ISLNK(existing.st_mode),
             token + ": exact existing directory")
        need(node_at(parent_fd, "." + token + ".stage") is None,
             token + ": exact target forbids leftover stage")
        verify_bundle(parent_fd, token, payloads)
        return "RESUMED_EXACT"
    stage = "." + token + ".stage"
    stage_info = node_at(parent_fd, stage)
    if stage_info is None:
        os.mkdir(stage, 0o700, dir_fd=parent_fd)
        os.fsync(parent_fd)
        stage_action = "CREATED_STAGE"
    else:
        need(
            stat.S_ISDIR(stage_info.st_mode)
            and not stat.S_ISLNK(stage_info.st_mode)
            and stage_info.st_uid == os.getuid()
            and stage_info.st_nlink == 2
            and stat.S_IMODE(stage_info.st_mode) in {0o700, 0o500},
            stage + ": interrupted stage exact owned directory",
        )
        stage_action = "RESUMED_INTERRUPTED_EXACT_STAGE"
    stage_fd = open_dir_at(parent_fd, stage)
    try:
        opened_stage = os.fstat(stage_fd)
        path_stage = os.stat(stage, dir_fd=parent_fd, follow_symlinks=False)
        need(
            fingerprint(opened_stage) == fingerprint(path_stage)
            and opened_stage.st_nlink == 2
            and stat.S_IMODE(opened_stage.st_mode) in {0o700, 0o500},
            stage + ": held descriptor is exact stage path",
        )
        inventory = set(os.listdir(stage_fd))
        need(inventory <= set(payloads),
             stage + ": no unexpected interrupted members")
        for name in sorted(inventory):
            payload = payloads[name]
            raw, info = read_at(stage_fd, name, max(1, len(payload)))
            need(
                raw == payload and stat.S_IMODE(info.st_mode) == 0o444,
                stage + ": exact interrupted member:" + name,
            )
        missing = sorted(set(payloads) - inventory)
        need(not missing or stat.S_IMODE(os.fstat(stage_fd).st_mode) == 0o700,
             stage + ": incomplete stage must remain mode 0700")
        for name in missing:
            write_once_at(stage_fd, name, payloads[name])
        need(set(os.listdir(stage_fd)) == set(payloads),
             stage + ": completed exact inventory")
        os.fchmod(stage_fd, 0o500)
        os.fsync(stage_fd)
        terminal_stage = os.fstat(stage_fd)
        terminal_path = os.stat(
            stage, dir_fd=parent_fd, follow_symlinks=False
        )
        need(
            fingerprint(terminal_stage) == fingerprint(terminal_path)
            and terminal_stage.st_nlink == 2
            and stat.S_IMODE(terminal_stage.st_mode) == 0o500
            and set(os.listdir(stage_fd)) == set(payloads),
            stage + ": terminal descriptor/path identity before rename",
        )
    finally:
        os.close(stage_fd)
    rename_noreplace(parent_fd, stage, parent_fd, token)
    os.fsync(parent_fd)
    verify_bundle(parent_fd, token, payloads)
    return "INSTALLED__" + stage_action


CANDIDATE_LABELS = ["candidate_source", "candidate_result"]
AUDIT_LABELS = [
    "installer", "C42_seal", "C42_candidate_pointer", "C42_audit_pointer",
    "C48_seal", "C48_receipt", "C48_candidate_pointer",
    "C48_audit_pointer", "C50d_protocol", "C50d_protocol_companion",
    "C46_source", "C51_source", "C51_report", "C51_result",
    *sorted(C50A_ARTIFACTS), "C52_source", "C52_audit",
    "independent_verifier", "independent_verifier_sidecar",
    "independent_audit", "independent_audit_sidecar",
    "independent_report", "independent_report_sidecar",
    "independent_manifest", "independent_manifest_sidecar",
]


def expected_state(inputs: Inputs) -> dict[str, Any]:
    independent = strict_json(
        inputs.captures["independent_audit"].raw, "independent audit state"
    )
    promotion = independent["post_seal_promotion_derivation"]
    effective = promotion["effective_post_seal_checkpoint"]
    predecessor_identity = expected_predecessor_identity()
    descriptor = close_object({
        "schema": SCHEMA + ".successor-descriptor",
        "status": (
            "C53_PAIR1_AUDITED_SUCCESSOR_DESCRIPTOR__FINAL_GLOBAL_HEAD_"
            "SEAL_PENDING"
        ),
        "predecessor_identity": predecessor_identity,
        "candidate_file_sha256": CANDIDATE_RESULT_FILE_SHA256,
        "candidate_object_sha256": CANDIDATE_OBJECT_SHA256,
        "candidate_zero_credit_checkpoint_object_sha256":
            SUCCESSOR_CHECKPOINT_OBJECT_SHA256,
        "pair_transaction_object_sha256": PAIR_TRANSACTION_OBJECT_SHA256,
        "independent_audit_file_sha256": INDEPENDENT_AUDIT_FILE_SHA256,
        "independent_audit_object_sha256": INDEPENDENT_AUDIT_OBJECT_SHA256,
        "promotion_derivation_object_sha256":
            PROMOTION_DERIVATION_OBJECT_SHA256,
        "post_seal_effective_checkpoint_object_sha256":
            EFFECTIVE_CHECKPOINT_OBJECT_SHA256,
        "pair_scope": {
            "pair_index": PAIR,
            "shard_index": SHARD_INDEX,
            "task_indices": [0, 1],
            "task_bindings": TASK_BINDINGS,
            "candidate_selected_tasks_formal_closed": [False, False],
            "post_seal_selected_tasks_formal_closed": [True, True],
            "individual_task_credit_lock": ZERO_LOCK,
            "pair_level_whole_parent_credit": 1,
            "D02_gate_credit": 0,
        },
        "before_census": C50D_BEFORE,
        "after_census_if_final_global_head_seal_commits": C50D_AFTER,
        "D02_four_class_census_before": D02_FORMAL_BEFORE,
        "D02_four_class_census_after_if_sealed": D02_FORMAL_AFTER,
        "claim_target_path": GLOBAL_CLAIM_PATH,
        "authority_seal_target_path": GLOBAL_HEAD_PATH,
        "zero_credit_before_final_global_head_seal": True,
    }, "successor_descriptor_object_sha256")
    promotion_raw = canonical(promotion) + b"\n"
    effective_raw = canonical(effective) + b"\n"
    descriptor_raw = canonical(descriptor) + b"\n"
    derived_payloads = {
        "post_seal_promotion_derivation.json": promotion_raw,
        "post_seal_effective_checkpoint.json": effective_raw,
        "successor_descriptor.json": descriptor_raw,
    }
    candidate_manifest = build_manifest(
        "candidate", CANDIDATE_TOKEN, CANDIDATE_LABELS, inputs
    )
    audit_manifest = build_manifest(
        "evidence", AUDIT_TOKEN, AUDIT_LABELS, inputs, derived_payloads
    )
    receipt_path = (
        ".cm2-runtime/" + AUDIT_PARENT + "/" + AUDIT_TOKEN
        + "/installation_receipt.json"
    )
    receipt_body = {
        "schema": RECEIPT_SCHEMA,
        "status": "PREPARED_C53_PAIR1_ATOMIC_PAIR_SUCCESSOR_RECEIPT__SEAL_PENDING",
        "release_id": RELEASE_ID,
        "predecessor_identity": predecessor_identity,
        "successor_descriptor_object_sha256": descriptor[
            "successor_descriptor_object_sha256"
        ],
        "candidate_object_sha256": CANDIDATE_OBJECT_SHA256,
        "pair_transaction_object_sha256": PAIR_TRANSACTION_OBJECT_SHA256,
        "candidate_zero_credit_checkpoint_object_sha256":
            SUCCESSOR_CHECKPOINT_OBJECT_SHA256,
        "independent_audit_object_sha256": INDEPENDENT_AUDIT_OBJECT_SHA256,
        "promotion_derivation_object_sha256":
            PROMOTION_DERIVATION_OBJECT_SHA256,
        "post_seal_effective_checkpoint_object_sha256":
            EFFECTIVE_CHECKPOINT_OBJECT_SHA256,
        "candidate_bundle": {
            "token": CANDIDATE_TOKEN,
            "manifest_object_sha256": candidate_manifest["manifest_object_sha256"],
        },
        "evidence_bundle": {
            "token": AUDIT_TOKEN,
            "manifest_object_sha256": audit_manifest["manifest_object_sha256"],
        },
        "predecessor_authority": {
            "C42_seal_object_sha256": C42_SEAL_OBJECT_SHA256,
            "C48_seal_object_sha256": C48_SEAL_OBJECT_SHA256,
            "C48_successor_checkpoint_object_sha256": C48_SUCCESSOR_OBJECT_SHA256,
            "C48_receipt_file_sha256": C48_RECEIPT_FILE_SHA256,
            "C48_receipt_object_sha256": C48_RECEIPT_OBJECT_SHA256,
        },
        "pair_scope": {
            "pair_index": PAIR,
            "shard_index": SHARD_INDEX,
            "task_indices": [0, 1],
            "task_bindings": TASK_BINDINGS,
            "before": C50D_BEFORE,
            "after_if_sealed": C50D_AFTER,
            "D02_four_class_before": D02_FORMAL_BEFORE,
            "D02_four_class_after_if_sealed": D02_FORMAL_AFTER,
            "D02_gate_credit": 0,
            "whole_parent_credit_if_sealed": 1,
        },
        "claim_target_path": GLOBAL_CLAIM_PATH,
        "authority_seal_target_path": GLOBAL_HEAD_PATH,
        "publication": {
            "O_EXCL": True, "O_NOFOLLOW": True, "O_CLOEXEC": True,
            "file_and_parent_fsync": True,
            "renameat2_RENAME_NOREPLACE": True,
            "seal_is_only_semantic_commit": True,
        },
    }
    receipt = close_object(receipt_body, "receipt_object_sha256")
    receipt_raw = canonical(receipt) + b"\n"
    claim = close_object({
        "authority_seal_target_path": GLOBAL_HEAD_PATH,
        "independent_audit_object_sha256": INDEPENDENT_AUDIT_OBJECT_SHA256,
        "installation_receipt_file_sha256": file_digest(receipt_raw),
        "installation_receipt_object_sha256": receipt[
            "receipt_object_sha256"
        ],
        "pair_transaction_object_sha256": PAIR_TRANSACTION_OBJECT_SHA256,
        "post_seal_effective_checkpoint_object_sha256":
            EFFECTIVE_CHECKPOINT_OBJECT_SHA256,
        "predecessor_identity": predecessor_identity,
        "promotion_derivation_object_sha256":
            PROMOTION_DERIVATION_OBJECT_SHA256,
        "schema": C50D_CLAIM_SCHEMA,
        "successor_descriptor_object_sha256": descriptor[
            "successor_descriptor_object_sha256"
        ],
        "zero_credit_before_seal": True,
    }, "claim_object_sha256")
    claim_raw = canonical(claim) + b"\n"
    seal_body = {
        "schema": SEAL_SCHEMA,
        "status": (
            "COMMITTED_C53_PAIR1_ATOMIC_TWO_TASK_PAIR_LEVEL_SUCCESSOR__"
            "ONE_WHOLE_PARENT_CREDIT__ZERO_D02_GATE_CREDIT"
        ),
        "release_id": RELEASE_ID,
        "authority_role": "GLOBAL_COMPOSITE",
        "authority_seal_target_path": GLOBAL_HEAD_PATH,
        "predecessor_identity": predecessor_identity,
        "predecessor_identity_sha256": C50D_PREDECESSOR_IDENTITY_SHA256,
        "predecessor_consumption_claim_path": GLOBAL_CLAIM_PATH,
        "predecessor_consumption_claim_file_sha256": file_digest(claim_raw),
        "predecessor_consumption_claim_object_sha256": claim[
            "claim_object_sha256"
        ],
        "candidate_token": CANDIDATE_TOKEN,
        "candidate_pointer_sha256": file_digest(CANDIDATE_POINTER_BYTES),
        "audit_token": AUDIT_TOKEN,
        "audit_pointer_sha256": file_digest(AUDIT_POINTER_BYTES),
        "candidate_object_sha256": CANDIDATE_OBJECT_SHA256,
        "pair_transaction_object_sha256": PAIR_TRANSACTION_OBJECT_SHA256,
        "candidate_zero_credit_checkpoint_object_sha256":
            SUCCESSOR_CHECKPOINT_OBJECT_SHA256,
        "successor_checkpoint_object_sha256": EFFECTIVE_CHECKPOINT_OBJECT_SHA256,
        "post_seal_effective_checkpoint_object_sha256":
            EFFECTIVE_CHECKPOINT_OBJECT_SHA256,
        "promotion_derivation_object_sha256":
            PROMOTION_DERIVATION_OBJECT_SHA256,
        "independent_audit_object_sha256": INDEPENDENT_AUDIT_OBJECT_SHA256,
        "successor_descriptor_object_sha256": descriptor[
            "successor_descriptor_object_sha256"
        ],
        "C48_predecessor_authority_seal_object_sha256": C48_SEAL_OBJECT_SHA256,
        "receipt_object_sha256": receipt["receipt_object_sha256"],
        "receipt_file_sha256": file_digest(receipt_raw),
        "receipt_path": receipt_path,
        "formal_scope": {
            "pair_index": PAIR,
            "task_level_successor_count_this_transaction": 2,
            "whole_parent_credit": 1,
            "D02_gate_credit": 0,
            "before": C50D_BEFORE,
            "after": C50D_AFTER,
            "D02_four_class_before": D02_FORMAL_BEFORE,
            "D02_four_class_after": D02_FORMAL_AFTER,
        },
        "semantic_commit": {
            "both_tasks_or_neither": True,
            "compatibility_pointers_without_this_seal_are_not_authority": True,
            "this_seal_is_required": True,
            "this_predecessor_keyed_global_head_is_only_semantic_commit": True,
            "no_runtime_writes_after_this_seal": True,
            "publication_method": (
                "O_EXCL_O_NOFOLLOW_fsync_renameat2_RENAME_NOREPLACE"
            ),
        },
    }
    seal = close_object(seal_body, "authority_seal_object_sha256")
    candidate_payloads = bundle_payloads(
        CANDIDATE_LABELS, candidate_manifest, inputs
    )
    audit_payloads = bundle_payloads(
        AUDIT_LABELS, audit_manifest, inputs, receipt, derived_payloads
    )
    return {
        "candidate_manifest": candidate_manifest,
        "audit_manifest": audit_manifest,
        "candidate_payloads": candidate_payloads,
        "audit_payloads": audit_payloads,
        "receipt": receipt,
        "receipt_raw": receipt_raw,
        "claim": claim,
        "claim_raw": claim_raw,
        "successor_descriptor": descriptor,
        "successor_descriptor_raw": descriptor_raw,
        "promotion": promotion,
        "promotion_raw": promotion_raw,
        "effective_checkpoint": effective,
        "effective_checkpoint_raw": effective_raw,
        "seal": seal,
        "seal_raw": canonical(seal) + b"\n",
    }


def open_runtime() -> int:
    fd = os.open(RUNTIME, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW | os.O_CLOEXEC)
    info = os.fstat(fd)
    need(stat.S_ISDIR(info.st_mode) and info.st_uid == os.getuid(),
         "runtime owned directory")
    return fd


def attest_directory_fd(fd: int, path: Path, label: str) -> None:
    descriptor = os.fstat(fd)
    path_info = os.stat(path, follow_symlinks=False)
    need(
        stat.S_ISDIR(descriptor.st_mode)
        and descriptor.st_uid == os.getuid()
        and fingerprint(descriptor) == fingerprint(path_info),
        label + ": descriptor/path identity",
    )


def verify_installed(inputs: Inputs, state: dict[str, Any],
                     tracker: WriteTracker | None = None) -> dict[str, Any]:
    """Read-only terminal replay of the complete C50d committed chain."""
    runtime_fd = open_runtime()
    opened: list[int] = []
    try:
        fcntl.flock(runtime_fd, fcntl.LOCK_SH)
        attest_directory_fd(runtime_fd, RUNTIME, "runtime terminal replay")
        slot = (
            classify_c50d_tracked(runtime_fd, state, tracker)
            if tracker is not None else classify_c50d_runtime(runtime_fd, state)
        )
        need(
            tuple(slot[key] for key in (
                "claim", "candidate_pointer", "audit_pointer",
                "global_head_seal",
            )) == ("EXACT", "EXACT", "EXACT", "EXACT")
            and all(slot[key] == "ABSENT" for key in (
                "claim_stage", "candidate_pointer_stage",
                "audit_pointer_stage", "global_head_stage",
            )),
            "C53 terminal replay requires exact S4 with no file stages",
        )
        candidate_parent_fd = open_dir_at(runtime_fd, CANDIDATE_PARENT)
        audit_parent_fd = open_dir_at(runtime_fd, AUDIT_PARENT)
        claim_parent_fd = open_dir_at(runtime_fd, GLOBAL_CLAIM_PARENT)
        head_parent_fd = open_dir_at(runtime_fd, GLOBAL_HEAD_PARENT)
        opened.extend([
            candidate_parent_fd, audit_parent_fd, claim_parent_fd,
            head_parent_fd,
        ])
        verify_terminal_bundle_no_stage(
            candidate_parent_fd, CANDIDATE_TOKEN, state["candidate_payloads"]
        )
        verify_terminal_bundle_no_stage(
            audit_parent_fd, AUDIT_TOKEN, state["audit_payloads"]
        )
        verify_terminal_file_no_stage(
            runtime_fd, CANDIDATE_POINTER, CANDIDATE_POINTER_STAGE,
            CANDIDATE_POINTER_BYTES,
        )
        verify_terminal_file_no_stage(
            runtime_fd, AUDIT_POINTER, AUDIT_POINTER_STAGE,
            AUDIT_POINTER_BYTES,
        )
        verify_terminal_file_no_stage(
            claim_parent_fd, GLOBAL_CLAIM_BASENAME, GLOBAL_CLAIM_STAGE,
            state["claim_raw"],
        )
        verify_terminal_file_no_stage(
            head_parent_fd, GLOBAL_HEAD_BASENAME, GLOBAL_HEAD_STAGE,
            state["seal_raw"],
        )
        claim = strict_json(state["claim_raw"], "expected final claim")
        seal = strict_json(state["seal_raw"], "expected final global head")
        need(
            claim == state["claim"]
            and object_digest(claim, "claim_object_sha256")
            == claim["claim_object_sha256"]
            and seal == state["seal"]
            and object_digest(seal, "authority_seal_object_sha256")
            == seal["authority_seal_object_sha256"]
            and seal.get("predecessor_consumption_claim_file_sha256")
            == file_digest(state["claim_raw"])
            and seal.get("predecessor_consumption_claim_object_sha256")
            == claim["claim_object_sha256"]
            and seal.get("promotion_derivation_object_sha256")
            == PROMOTION_DERIVATION_OBJECT_SHA256
            and seal.get("post_seal_effective_checkpoint_object_sha256")
            == EFFECTIVE_CHECKPOINT_OBJECT_SHA256
            and seal.get("successor_checkpoint_object_sha256")
            == EFFECTIVE_CHECKPOINT_OBJECT_SHA256
            and seal.get("formal_scope", {}).get("before") == C50D_BEFORE
            and seal.get("formal_scope", {}).get("after") == C50D_AFTER
            and seal.get("formal_scope", {}).get("D02_four_class_before")
            == D02_FORMAL_BEFORE
            and seal.get("formal_scope", {}).get("D02_four_class_after")
            == D02_FORMAL_AFTER,
            "C53 global head complete claim/promotion/effective/census bindings",
        )
        inputs.attest_all("verify-installed terminal input replay")
        attest_directory_fd(
            candidate_parent_fd, RUNTIME / CANDIDATE_PARENT,
            "candidate parent terminal replay",
        )
        attest_directory_fd(
            audit_parent_fd, RUNTIME / AUDIT_PARENT,
            "audit parent terminal replay",
        )
        attest_directory_fd(
            claim_parent_fd, RUNTIME / GLOBAL_CLAIM_PARENT,
            "claim parent terminal replay",
        )
        attest_directory_fd(
            head_parent_fd, RUNTIME / GLOBAL_HEAD_PARENT,
            "global head parent terminal replay",
        )
        final_slot = (
            classify_c50d_tracked(runtime_fd, state, tracker)
            if tracker is not None else classify_c50d_runtime(runtime_fd, state)
        )
        need(final_slot == slot,
             "C53 terminal replay slot remains exact S4 with no stages")
        attest_directory_fd(
            runtime_fd, RUNTIME, "runtime final terminal replay"
        )
    finally:
        for fd in reversed(opened):
            os.close(fd)
        os.close(runtime_fd)
    return {
        "schema": SCHEMA + ".verify-installed",
        "status": (
            "PASS_C53_C50D_GLOBAL_HEAD_COMPLETE_TERMINAL_REPLAY__"
            "576_PAIRED__1148_UNRESOLVED__ZERO_D02_GATE_CREDIT"
        ),
        "global_head_path": GLOBAL_HEAD_PATH,
        "global_head_file_sha256": file_digest(state["seal_raw"]),
        "global_head_object_sha256": state["seal"][
            "authority_seal_object_sha256"
        ],
        "claim_path": GLOBAL_CLAIM_PATH,
        "claim_file_sha256": file_digest(state["claim_raw"]),
        "claim_object_sha256": state["claim"]["claim_object_sha256"],
        "effective_checkpoint_object_sha256":
            EFFECTIVE_CHECKPOINT_OBJECT_SHA256,
        "promotion_derivation_object_sha256":
            PROMOTION_DERIVATION_OBJECT_SHA256,
        "authoritative_census": C50D_AFTER,
        "D02_four_class_census": D02_FORMAL_AFTER,
        "whole_parent_credit": 1,
        "D02_gate_credit": 0,
        "runtime_writes_performed": False,
    }


def slot_prefix(slot: dict[str, str]) -> tuple[str, str, str, str]:
    return tuple(slot[key] for key in (
        "claim", "candidate_pointer", "audit_pointer", "global_head_seal",
    ))


def slot_rank(slot: dict[str, str]) -> int:
    ordered = [
        ("ABSENT", "ABSENT", "ABSENT", "ABSENT"),
        ("EXACT", "ABSENT", "ABSENT", "ABSENT"),
        ("EXACT", "EXACT", "ABSENT", "ABSENT"),
        ("EXACT", "EXACT", "EXACT", "ABSENT"),
        ("EXACT", "EXACT", "EXACT", "EXACT"),
    ]
    return ordered.index(slot_prefix(slot))


def slot_progress_rank(slot: dict[str, str]) -> int:
    """Interleave each exact stage with its corresponding final target."""
    prefix = slot_prefix(slot)
    stage_keys = (
        "claim_stage", "candidate_pointer_stage",
        "audit_pointer_stage", "global_head_stage",
    )
    stages = tuple(slot[key] for key in stage_keys)
    validate_c50d_recovery_grammar(prefix, stages)
    target_rank = slot_rank(slot)
    if "EXACT" not in stages:
        return target_rank * 2
    need(stages.count("EXACT") == 1,
         "C50d recovery has at most one exact file stage")
    return target_rank * 2 + 1


def global_head_node_present(runtime_fd: int) -> bool:
    namespace = node_at(runtime_fd, GLOBAL_HEAD_PARENT)
    if namespace is None:
        return False
    if not stat.S_ISDIR(namespace.st_mode) or stat.S_ISLNK(namespace.st_mode):
        return True
    try:
        parent_fd = open_dir_at(runtime_fd, GLOBAL_HEAD_PARENT)
    except (Reject, OSError):
        return True
    try:
        return node_at(parent_fd, GLOBAL_HEAD_BASENAME) is not None
    finally:
        os.close(parent_fd)


def observe_global_head_for_failure(tracker: WriteTracker) -> None:
    """Best-effort read-only resolver probe before emitting a failure receipt."""
    try:
        runtime_fd = open_runtime()
    except (Reject, OSError):
        tracker.observe_possible_final_seal()
        return
    try:
        try:
            fcntl.flock(runtime_fd, fcntl.LOCK_SH | fcntl.LOCK_NB)
        except OSError:
            tracker.observe_possible_final_seal()
            return
        if global_head_node_present(runtime_fd):
            tracker.observe_possible_final_seal()
    except (Reject, OSError):
        tracker.observe_possible_final_seal()
    finally:
        os.close(runtime_fd)


def classify_c50d_tracked(runtime_fd: int, state: dict[str, Any],
                          tracker: WriteTracker) -> dict[str, str]:
    if global_head_node_present(runtime_fd):
        tracker.observe_possible_final_seal()
    return classify_c50d_runtime(runtime_fd, state)


def resume_exact_s4(inputs: Inputs, state: dict[str, Any],
                    tracker: WriteTracker, runtime_fd: int) -> dict[str, Any]:
    tracker.observe_possible_final_seal()
    fcntl.flock(runtime_fd, fcntl.LOCK_UN)
    terminal = verify_installed(inputs, state, tracker)
    tracker.seal_verified()
    return {
        "schema": SCHEMA + ".installation-result",
        "status": "RESUMED_EXACT_C53_C50D_GLOBAL_HEAD_READ_ONLY",
        "release_id": RELEASE_ID,
        "global_head_path": GLOBAL_HEAD_PATH,
        "authority_seal_object_sha256": state["seal"][
            "authority_seal_object_sha256"
        ],
        "authority_seal_file_sha256": file_digest(state["seal_raw"]),
        "publication_actions": {
            "candidate_bundle": "READ_ONLY_VERIFIED_EXACT",
            "audit_bundle": "READ_ONLY_VERIFIED_EXACT",
            "predecessor_claim": "READ_ONLY_VERIFIED_EXACT",
            "candidate_pointer": "READ_ONLY_VERIFIED_EXACT",
            "audit_pointer": "READ_ONLY_VERIFIED_EXACT",
            "final_global_head_seal": "READ_ONLY_VERIFIED_EXACT",
        },
        "terminal_replay": terminal,
        "runtime_writes_performed": False,
        "formal_scope": {
            "after": C50D_AFTER,
            "whole_parent_credit": 1,
            "D02_gate_credit": 0,
        },
    }


def reject_head_after_write_start(slot: dict[str, str],
                                  tracker: WriteTracker, label: str) -> None:
    if slot["global_head_seal"] == "EXACT":
        tracker.observe_possible_final_seal()
        raise Reject(label + ": exact head appeared after write phase began")


def install(inputs: Inputs, state: dict[str, Any],
            tracker: WriteTracker) -> dict[str, Any]:
    need(all_terminal_pins_frozen(), "installer armed only by complete static pins")
    inputs.attest_all("immediately before commit")
    runtime_fd = open_runtime()
    descriptors: list[int] = []
    try:
        fcntl.flock(runtime_fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
        attest_directory_fd(runtime_fd, RUNTIME, "runtime pre-publication")
        initial_slot = classify_c50d_tracked(runtime_fd, state, tracker)
        if initial_slot["global_head_seal"] == "EXACT":
            return resume_exact_s4(inputs, state, tracker, runtime_fd)

        inputs.attest_all("between initial and second publication barriers")
        attest_directory_fd(runtime_fd, RUNTIME, "runtime second barrier")
        second_slot = classify_c50d_tracked(runtime_fd, state, tracker)
        need(slot_progress_rank(second_slot) >= slot_progress_rank(initial_slot),
             "C50d second barrier forbids target/stage regression")
        require_bundle_recovery_monotone(
            initial_slot, second_slot, "C50d second barrier"
        )
        if second_slot["global_head_seal"] == "EXACT":
            return resume_exact_s4(inputs, state, tracker, runtime_fd)

        tracker.before_write("BUNDLES_AND_NAMESPACES")
        candidate_parent_fd = ensure_parent(runtime_fd, CANDIDATE_PARENT)
        audit_parent_fd = ensure_parent(runtime_fd, AUDIT_PARENT)
        claim_parent_fd = ensure_parent(runtime_fd, GLOBAL_CLAIM_PARENT)
        head_parent_fd = ensure_parent(runtime_fd, GLOBAL_HEAD_PARENT)
        descriptors.extend([
            candidate_parent_fd, audit_parent_fd, claim_parent_fd,
            head_parent_fd,
        ])

        bundle_barrier = classify_c50d_tracked(runtime_fd, state, tracker)
        need(
            slot_progress_rank(bundle_barrier)
            >= slot_progress_rank(second_slot),
            "C50d bundle barrier forbids target/stage regression",
        )
        require_bundle_recovery_monotone(
            second_slot, bundle_barrier, "C50d bundle barrier"
        )
        reject_head_after_write_start(
            bundle_barrier, tracker, "C50d bundle barrier"
        )
        bundle_decision = classify_c50d_tracked(
            runtime_fd, state, tracker
        )
        need(
            slot_progress_rank(bundle_decision)
            >= slot_progress_rank(bundle_barrier),
            "C50d immediate bundle decision forbids target/stage regression",
        )
        require_bundle_recovery_monotone(
            bundle_barrier, bundle_decision,
            "C50d immediate bundle decision",
        )
        reject_head_after_write_start(
            bundle_decision, tracker, "C50d immediate bundle decision"
        )
        candidate_action, audit_action = reconcile_bundles_at_claim_barrier(
            (
                "EXACT" if "EXACT" in {
                    bundle_decision["claim"], bundle_decision["claim_stage"]
                } else "ABSENT"
            ),
            candidate_parent_fd, audit_parent_fd,
            state,
        )
        verify_terminal_bundle_no_stage(
            candidate_parent_fd, CANDIDATE_TOKEN, state["candidate_payloads"]
        )
        verify_terminal_bundle_no_stage(
            audit_parent_fd, AUDIT_TOKEN, state["audit_payloads"]
        )
        inputs.attest_all("before predecessor consumption claim")
        attest_directory_fd(runtime_fd, RUNTIME, "runtime pre-claim")
        attest_directory_fd(
            candidate_parent_fd, RUNTIME / CANDIDATE_PARENT,
            "candidate parent pre-claim",
        )
        attest_directory_fd(
            audit_parent_fd, RUNTIME / AUDIT_PARENT,
            "audit parent pre-claim",
        )
        attest_directory_fd(
            claim_parent_fd, RUNTIME / GLOBAL_CLAIM_PARENT,
            "claim parent pre-claim",
        )
        preclaim_slot = classify_c50d_tracked(runtime_fd, state, tracker)
        need(
            slot_progress_rank(preclaim_slot)
            >= slot_progress_rank(bundle_decision),
            "C50d pre-claim barrier forbids target/stage regression",
        )
        require_bundle_recovery_monotone(
            bundle_decision, preclaim_slot, "C50d pre-claim barrier"
        )
        reject_head_after_write_start(
            preclaim_slot, tracker, "C50d pre-claim barrier"
        )
        tracker.before_write("PREDECESSOR_CONSUMPTION_CLAIM")
        claim_action = publish_file(
            claim_parent_fd, GLOBAL_CLAIM_BASENAME, GLOBAL_CLAIM_STAGE,
            state["claim_raw"],
        )
        verify_terminal_file_no_stage(
            claim_parent_fd, GLOBAL_CLAIM_BASENAME, GLOBAL_CLAIM_STAGE,
            state["claim_raw"],
        )

        candidate_barrier = classify_c50d_tracked(runtime_fd, state, tracker)
        need(
            slot_rank(candidate_barrier) >= 1
            and slot_progress_rank(candidate_barrier)
            >= max(2, slot_progress_rank(preclaim_slot)),
            "C50d candidate-pointer barrier requires monotone exact claim",
        )
        reject_head_after_write_start(
            candidate_barrier, tracker, "C50d candidate-pointer barrier"
        )
        tracker.before_write("COMPATIBILITY_POINTERS")
        candidate_pointer_action = publish_file(
            runtime_fd, CANDIDATE_POINTER, CANDIDATE_POINTER_STAGE,
            CANDIDATE_POINTER_BYTES,
        )
        verify_terminal_file_no_stage(
            runtime_fd, CANDIDATE_POINTER, CANDIDATE_POINTER_STAGE,
            CANDIDATE_POINTER_BYTES,
        )

        audit_barrier = classify_c50d_tracked(runtime_fd, state, tracker)
        need(
            slot_rank(audit_barrier) >= 2
            and slot_progress_rank(audit_barrier)
            >= max(4, slot_progress_rank(candidate_barrier)),
            "C50d audit-pointer barrier requires monotone claim/candidate",
        )
        reject_head_after_write_start(
            audit_barrier, tracker, "C50d audit-pointer barrier"
        )
        audit_pointer_action = publish_file(
            runtime_fd, AUDIT_POINTER, AUDIT_POINTER_STAGE,
            AUDIT_POINTER_BYTES,
        )
        verify_terminal_file_no_stage(
            runtime_fd, AUDIT_POINTER, AUDIT_POINTER_STAGE,
            AUDIT_POINTER_BYTES,
        )

        inputs.attest_all("before final global head seal")
        verify_terminal_bundle_no_stage(
            candidate_parent_fd, CANDIDATE_TOKEN, state["candidate_payloads"]
        )
        verify_terminal_bundle_no_stage(
            audit_parent_fd, AUDIT_TOKEN, state["audit_payloads"]
        )
        verify_terminal_file_no_stage(
            claim_parent_fd, GLOBAL_CLAIM_BASENAME, GLOBAL_CLAIM_STAGE,
            state["claim_raw"],
        )
        verify_terminal_file_no_stage(
            runtime_fd, CANDIDATE_POINTER, CANDIDATE_POINTER_STAGE,
            CANDIDATE_POINTER_BYTES,
        )
        verify_terminal_file_no_stage(
            runtime_fd, AUDIT_POINTER, AUDIT_POINTER_STAGE,
            AUDIT_POINTER_BYTES,
        )
        attest_directory_fd(runtime_fd, RUNTIME, "runtime pre-seal")
        attest_directory_fd(
            candidate_parent_fd, RUNTIME / CANDIDATE_PARENT,
            "candidate parent pre-seal",
        )
        attest_directory_fd(
            audit_parent_fd, RUNTIME / AUDIT_PARENT,
            "audit parent pre-seal",
        )
        attest_directory_fd(
            claim_parent_fd, RUNTIME / GLOBAL_CLAIM_PARENT,
            "claim parent pre-seal",
        )
        attest_directory_fd(
            head_parent_fd, RUNTIME / GLOBAL_HEAD_PARENT,
            "global head parent pre-seal",
        )
        preseal_slot = classify_c50d_tracked(runtime_fd, state, tracker)
        need(slot_prefix(preseal_slot)
             == ("EXACT", "EXACT", "EXACT", "ABSENT"),
             "C50d exact complete S3 prefix before final seal")
        need(
            slot_progress_rank(preseal_slot)
            >= max(6, slot_progress_rank(audit_barrier)),
            "C50d pre-seal barrier forbids target/stage regression",
        )
        need(all(preseal_slot[key] == "ABSENT" for key in (
            "claim_stage", "candidate_pointer_stage", "audit_pointer_stage",
        )), "C50d no completed-prefix stages before final seal")
        tracker.before_write("FINAL_GLOBAL_HEAD_SEAL_LAST_WRITE")
        seal_action = publish_file(
            head_parent_fd, GLOBAL_HEAD_BASENAME, GLOBAL_HEAD_STAGE,
            state["seal_raw"],
        )
        # No filesystem mutation is permitted after the final publication.
    finally:
        for fd in reversed(descriptors):
            os.close(fd)
        os.close(runtime_fd)
    terminal = verify_installed(inputs, state, tracker)
    tracker.seal_verified()
    return {
        "schema": SCHEMA + ".installation-result",
        "status": (
            "PASS_C53_PAIR1_C50D_GLOBAL_HEAD_INSTALLED__576_PAIRED__"
            "1148_UNRESOLVED__ZERO_D02_GATE_CREDIT"
        ),
        "release_id": RELEASE_ID,
        "global_head_path": GLOBAL_HEAD_PATH,
        "authority_seal_object_sha256": state["seal"][
            "authority_seal_object_sha256"
        ],
        "authority_seal_file_sha256": file_digest(state["seal_raw"]),
        "claim_object_sha256": state["claim"]["claim_object_sha256"],
        "claim_file_sha256": file_digest(state["claim_raw"]),
        "receipt_object_sha256": state["receipt"]["receipt_object_sha256"],
        "publication_actions": {
            "candidate_bundle": candidate_action,
            "audit_bundle": audit_action,
            "predecessor_claim": claim_action,
            "candidate_pointer": candidate_pointer_action,
            "audit_pointer": audit_pointer_action,
            "final_global_head_seal": seal_action,
        },
        "terminal_replay": terminal,
        "formal_scope": {
            "before": C50D_BEFORE,
            "after": C50D_AFTER,
            "D02_four_class_after": D02_FORMAL_AFTER,
            "whole_parent_credit": 1,
            "D02_gate_credit": 0,
        },
    }


def read_file_hash(path: Path, maximum: int = 1 << 30) -> str:
    flags = os.O_RDONLY | os.O_CLOEXEC | os.O_NOFOLLOW
    fd = os.open(path, flags)
    try:
        before = os.fstat(fd)
        need(stat.S_ISREG(before.st_mode) and 0 < before.st_size <= maximum,
             "preflight bounded regular:" + str(path))
        state = hashlib.sha256()
        while block := os.read(fd, 4 << 20):
            state.update(block)
        after = os.fstat(fd)
        need(fingerprint(before) == fingerprint(after),
             "preflight stable read:" + str(path))
        return state.hexdigest()
    finally:
        os.close(fd)


def inspect_global_prefix(state: dict[str, Any]) -> dict[str, str]:
    """Read-only, stage-aware C50d S0--S4 inspection."""
    runtime_fd = open_runtime()
    try:
        fcntl.flock(runtime_fd, fcntl.LOCK_SH)
        attest_directory_fd(runtime_fd, RUNTIME, "runtime prefix inspection")
        slot = classify_c50d_runtime(runtime_fd, state)
        attest_directory_fd(
            runtime_fd, RUNTIME, "runtime final prefix inspection"
        )
        return slot
    finally:
        os.close(runtime_fd)


def dry_run(expected_installer_sha256: str) -> dict[str, Any]:
    inputs = Inputs(expected_installer_sha256)
    try:
        state = expected_state(inputs)
        prefix = inspect_global_prefix(state)
        inputs.attest_all("dry-run terminal replay")
    finally:
        inputs.close()
    authority_probe = WriteTracker()
    observe_global_head_for_failure(authority_probe)
    authority = failure_authority_fields(authority_probe)
    return close_object({
        "schema": SCHEMA + ".dry-run",
        "status": "PASS_C53_INSTALLER_DRY_RUN__NO_WRITES__AWAITING_CONFIRMATION",
        "release_id": RELEASE_ID,
        "current_C50d_prefix": prefix,
        "expected_claim": {
            "path": GLOBAL_CLAIM_PATH,
            "file_sha256": file_digest(state["claim_raw"]),
            "object_sha256": state["claim"]["claim_object_sha256"],
        },
        "expected_global_head": {
            "path": GLOBAL_HEAD_PATH,
            "file_sha256": file_digest(state["seal_raw"]),
            "object_sha256": state["seal"]["authority_seal_object_sha256"],
            "successor_checkpoint_object_sha256":
                EFFECTIVE_CHECKPOINT_OBJECT_SHA256,
        },
        "expected_receipt": {
            "file_sha256": file_digest(state["receipt_raw"]),
            "object_sha256": state["receipt"]["receipt_object_sha256"],
        },
        "successor_descriptor_object_sha256": state[
            "successor_descriptor"
        ]["successor_descriptor_object_sha256"],
        "promotion_derivation_object_sha256":
            PROMOTION_DERIVATION_OBJECT_SHA256,
        "post_seal_effective_checkpoint_object_sha256":
            EFFECTIVE_CHECKPOINT_OBJECT_SHA256,
        "before_census": C50D_BEFORE,
        "prospective_after_census": C50D_AFTER,
        **authority,
        "runtime_writes_performed": False,
        "ready_for_exact_confirmation": True,
        "install_confirmation": CONFIRMATION,
        "formal_credit": 0,
        "D02_gate_credit": 0,
    }, "dry_run_object_sha256")


def preflight(expected_installer_sha256: str | None) -> dict[str, Any]:
    checks: dict[str, bool] = {}
    blockers: list[str] = []

    def file_check(label: str, path: str, expected: str) -> None:
        if HEX64.fullmatch(expected) is None:
            checks[label] = False
            blockers.append(label + ": terminal SHA-256 not frozen")
            return
        try:
            observed = read_file_hash(ROOT / path)
            checks[label] = observed == expected
            if observed != expected:
                blockers.append(label + ": pinned SHA-256 mismatch")
        except (Reject, OSError) as error:
            checks[label] = False
            blockers.append(label + ":" + type(error).__name__ + ":" + str(error))

    if expected_installer_sha256 is None or HEX64.fullmatch(expected_installer_sha256) is None:
        checks["installer_self_pin"] = False
        blockers.append("installer_self_pin: --expect-installer-sha256 requires 64 lowercase hex")
    else:
        observed = read_file_hash(SELF, 4 << 20)
        checks["installer_self_pin"] = observed == expected_installer_sha256
        if observed != expected_installer_sha256:
            blockers.append("installer_self_pin: installer bytes mismatch")
    file_check("installed_C42_predecessor", C42_SEAL_PATH, C42_SEAL_FILE_SHA256)
    file_check("C42_candidate_pointer", C42_CANDIDATE_POINTER_PATH,
               C42_CANDIDATE_POINTER_SHA256)
    file_check("C42_audit_pointer", C42_AUDIT_POINTER_PATH,
               C42_AUDIT_POINTER_SHA256)
    file_check("installed_C48_predecessor", C48_SEAL_PATH, C48_SEAL_FILE_SHA256)
    file_check("C48_receipt", C48_RECEIPT_PATH, C48_RECEIPT_FILE_SHA256)
    file_check("C48_candidate_pointer", C48_CANDIDATE_POINTER_PATH,
               C48_CANDIDATE_POINTER_SHA256)
    file_check("C48_audit_pointer", C48_AUDIT_POINTER_PATH,
               C48_AUDIT_POINTER_SHA256)
    file_check("C50d_protocol", C50D_PROTOCOL_PATH, C50D_PROTOCOL_FILE_SHA256)
    file_check("C50d_protocol_companion", C50D_PROTOCOL_COMPANION_PATH,
               C50D_PROTOCOL_COMPANION_FILE_SHA256)
    file_check("C46_source", C46_SOURCE_PATH, C46_SOURCE_SHA256)
    file_check("C51_source", C51_SOURCE_PATH, C51_SOURCE_SHA256)
    file_check("C51_report", C51_REPORT_PATH, C51_REPORT_SHA256)
    file_check("C51_complete_route_bytes", C51_RESULT_PATH, C51_RESULT_FILE_SHA256)
    for label, (path, sha) in sorted(C50A_ARTIFACTS.items()):
        file_check("C50a_" + label, path, sha)
    file_check("C52_source", C52_SOURCE_PATH, C52_SOURCE_SHA256)
    file_check("C52_terminal_audit", C52_AUDIT_PATH, C52_AUDIT_FILE_SHA256)
    file_check("C53_candidate_source", CANDIDATE_SOURCE_PATH, CANDIDATE_SOURCE_SHA256)
    file_check("C53_candidate_result", CANDIDATE_RESULT_PATH, CANDIDATE_RESULT_FILE_SHA256)
    file_check("C53_independent_verifier", INDEPENDENT_VERIFIER_PATH,
               INDEPENDENT_VERIFIER_SHA256)
    file_check("C53_independent_verifier_sidecar",
               INDEPENDENT_VERIFIER_SIDECAR_PATH,
               INDEPENDENT_VERIFIER_SIDECAR_FILE_SHA256)
    file_check("C53_independent_audit", INDEPENDENT_AUDIT_PATH,
               INDEPENDENT_AUDIT_FILE_SHA256)
    file_check("C53_independent_audit_sidecar", INDEPENDENT_AUDIT_SIDECAR_PATH,
               INDEPENDENT_AUDIT_SIDECAR_FILE_SHA256)
    file_check("C53_independent_report", INDEPENDENT_REPORT_PATH,
               INDEPENDENT_REPORT_FILE_SHA256)
    file_check("C53_independent_report_sidecar",
               INDEPENDENT_REPORT_SIDECAR_PATH,
               INDEPENDENT_REPORT_SIDECAR_FILE_SHA256)
    file_check("C53_independent_manifest", INDEPENDENT_MANIFEST_PATH,
               INDEPENDENT_MANIFEST_FILE_SHA256)
    file_check("C53_independent_manifest_sidecar",
               INDEPENDENT_MANIFEST_SIDECAR_PATH,
               INDEPENDENT_MANIFEST_SIDECAR_FILE_SHA256)
    checks["all_terminal_object_pins_frozen"] = all_terminal_pins_frozen()
    if not checks["all_terminal_object_pins_frozen"]:
        blockers.append("all_terminal_object_pins_frozen: C51/C52/C53 terminal pins incomplete")
    expected_summary: dict[str, Any] | None = None
    if bool(checks) and all(checks.values()):
        try:
            inputs = Inputs(expected_installer_sha256)  # type: ignore[arg-type]
            try:
                state = expected_state(inputs)
                prefix = inspect_global_prefix(state)
                inputs.attest_all("preflight terminal semantic replay")
                expected_summary = {
                    "claim_path": GLOBAL_CLAIM_PATH,
                    "claim_file_sha256": file_digest(state["claim_raw"]),
                    "claim_object_sha256": state["claim"]["claim_object_sha256"],
                    "global_head_path": GLOBAL_HEAD_PATH,
                    "global_head_file_sha256": file_digest(state["seal_raw"]),
                    "global_head_object_sha256": state["seal"][
                        "authority_seal_object_sha256"
                    ],
                    "current_C50d_prefix": prefix,
                }
                checks["deep_semantic_expected_state"] = True
            finally:
                inputs.close()
        except (Reject, OSError, ValueError, KeyError, TypeError) as error:
            checks["deep_semantic_expected_state"] = False
            blockers.append(
                "deep_semantic_expected_state:" + type(error).__name__
                + ":" + str(error)
            )
    ready = bool(checks) and all(checks.values())
    authority_probe = WriteTracker()
    observe_global_head_for_failure(authority_probe)
    authority = failure_authority_fields(authority_probe)
    body = {
        "schema": SCHEMA + ".preflight",
        "status": (
            "PASS_C53_PAIR1_INSTALLER_PREFLIGHT__NO_WRITES"
            if ready else
            "BLOCKED_C53_PAIR1_INSTALLER_FAIL_CLOSED__NO_WRITES_NO_SEAL_NO_CREDIT"
        ),
        "checks": checks,
        "blockers": blockers,
        "ready_to_install": ready,
        "install_confirmation_if_ready": CONFIRMATION if ready else None,
        "expected_C50d_targets_if_ready": expected_summary,
        "effective_authority_while_blocked": {
            "global_predecessor": "C48",
            "authority_state": authority["authority_state"],
            "effective_census": authority[
                "effective_authoritative_census"
            ],
            "global_head_resolution_required": True,
        },
        "prospective_after_only_not_authority": C50D_AFTER,
        "runtime_writes_performed": False,
        **authority,
        "formal_credit": 0,
        "D02_gate_credit": 0,
    }
    return close_object(body, "preflight_object_sha256")


def self_test() -> dict[str, Any]:
    checks: dict[str, bool] = {}
    with tempfile.TemporaryDirectory(prefix="c53-pair-installer-selftest-") as directory:
        root_fd = os.open(directory, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW | os.O_CLOEXEC)
        try:
            write_once_at(root_fd, "one", b"alpha\n")
            checks["O_EXCL_O_NOFOLLOW_write"] = exact_or_absent(root_fd, "one", b"alpha\n") == "EXACT"
            try:
                write_once_at(root_fd, "one", b"beta\n")
            except FileExistsError:
                checks["duplicate_create_rejected"] = True
            write_once_at(root_fd, "stage", b"gamma\n")
            rename_noreplace(root_fd, "stage", root_fd, "two")
            checks["rename_noreplace_publish"] = exact_or_absent(root_fd, "two", b"gamma\n") == "EXACT"
            write_once_at(root_fd, "collision", b"delta\n")
            write_once_at(root_fd, "stage2", b"epsilon\n")
            try:
                rename_noreplace(root_fd, "stage2", root_fd, "collision")
            except FileExistsError:
                checks["rename_existing_rejected"] = True
            os.symlink("one", "link", dir_fd=root_fd)
            try:
                read_at(root_fd, "link", 1024)
            except OSError:
                checks["symlink_read_rejected"] = True
            write_once_at(root_fd, "held-source", b"VALUE=1\n")
            write_once_at(root_fd, "replacement-source", b"VALUE=2\n")
            capture = Capture(
                Path(directory) / "held-source", "selftest held source",
                file_digest(b"VALUE=1\n"), 1024, workspace_only=False,
            )
            try:
                os.replace(
                    Path(directory) / "replacement-source",
                    Path(directory) / "held-source",
                )
                try:
                    capture.unchanged("late replacement attack")
                except Reject:
                    checks["late_source_replacement_rejected"] = True
            finally:
                capture.close()
            os.mkdir(".bundle.stage", 0o700, dir_fd=root_fd)
            stage_fd = open_dir_at(root_fd, ".bundle.stage")
            try:
                write_once_at(stage_fd, "first", b"one\n")
            finally:
                os.close(stage_fd)
            partial_bundle_state = classify_bundle_recovery(
                root_fd, "bundle", {"first": b"one\n", "second": b"two\n"}
            )
            checks["read_only_partial_bundle_stage_classified"] = (
                partial_bundle_state.startswith("RESUMABLE_STAGE_1_OF_2__")
            )
            action = publish_bundle(
                root_fd, "bundle", {"first": b"one\n", "second": b"two\n"}
            )
            checks["interrupted_bundle_stage_exact_resume"] = (
                action == "INSTALLED__RESUMED_INTERRUPTED_EXACT_STAGE"
            )
            verify_bundle(
                root_fd, "bundle", {"first": b"one\n", "second": b"two\n"}
            )
            bundle_fd = open_dir_at(root_fd, "bundle")
            try:
                bundle_stat = os.fstat(bundle_fd)
            finally:
                os.close(bundle_fd)
            forged_values = list(bundle_stat)
            forged_values[3] = 3
            forged_nlink = os.stat_result(forged_values)
            forged_nlink_rejected = False
            try:
                validate_terminal_bundle_directory_stat(
                    forged_nlink, forged_nlink, "selftest-forged-nlink"
                )
            except Reject:
                forged_nlink_rejected = True
            checks["terminal_bundle_directory_wrong_nlink_rejected"] = (
                bundle_stat.st_nlink == 2 and forged_nlink_rejected
            )
            os.mkdir(".bundle.stage", 0o700, dir_fd=root_fd)
            final_plus_stage_rejected = False
            try:
                classify_bundle_recovery(
                    root_fd, "bundle",
                    {"first": b"one\n", "second": b"two\n"},
                )
            except Reject:
                final_plus_stage_rejected = True
            checks["read_only_final_plus_bundle_stage_rejected"] = (
                final_plus_stage_rejected
            )
            os.rmdir(".bundle.stage", dir_fd=root_fd)
            os.mkdir(".corrupt.stage", 0o700, dir_fd=root_fd)
            corrupt_stage_fd = open_dir_at(root_fd, ".corrupt.stage")
            try:
                write_once_at(corrupt_stage_fd, "member", b"wrong\n")
            finally:
                os.close(corrupt_stage_fd)
            corrupt_stage_rejected = False
            try:
                classify_bundle_recovery(
                    root_fd, "corrupt", {"member": b"expected\n"}
                )
            except Reject:
                corrupt_stage_rejected = True
            checks["read_only_corrupt_bundle_stage_rejected"] = (
                corrupt_stage_rejected
            )
            recovery_state = {
                "candidate_payloads": {"candidate.json": b"candidate\n"},
                "audit_payloads": {"audit.json": b"audit\n"},
            }
            os.mkdir(CANDIDATE_PARENT, 0o700, dir_fd=root_fd)
            os.mkdir(AUDIT_PARENT, 0o700, dir_fd=root_fd)
            candidate_parent_fd = open_dir_at(root_fd, CANDIDATE_PARENT)
            try:
                publish_bundle(
                    candidate_parent_fd, CANDIDATE_TOKEN,
                    recovery_state["candidate_payloads"],
                )
            finally:
                os.close(candidate_parent_fd)
            recovery_fds: list[int] = []
            missing_bundle_rejected = False
            try:
                require_existing_claim_bundles(
                    root_fd, recovery_state, recovery_fds
                )
            except (Reject, OSError):
                missing_bundle_rejected = True
            finally:
                for recovery_fd in reversed(recovery_fds):
                    os.close(recovery_fd)
            audit_parent_fd = open_dir_at(root_fd, AUDIT_PARENT)
            try:
                publish_bundle(
                    audit_parent_fd, AUDIT_TOKEN,
                    recovery_state["audit_payloads"],
                )
            finally:
                os.close(audit_parent_fd)
            recovery_fds = []
            require_existing_claim_bundles(
                root_fd, recovery_state, recovery_fds
            )
            for recovery_fd in reversed(recovery_fds):
                os.close(recovery_fd)
            candidate_parent_fd = open_dir_at(root_fd, CANDIDATE_PARENT)
            try:
                os.mkdir(
                    "." + CANDIDATE_TOKEN + ".stage", 0o700,
                    dir_fd=candidate_parent_fd,
                )
            finally:
                os.close(candidate_parent_fd)
            recovery_fds = []
            leftover_stage_rejected = False
            try:
                require_existing_claim_bundles(
                    root_fd, recovery_state, recovery_fds
                )
            except Reject:
                leftover_stage_rejected = True
            finally:
                for recovery_fd in reversed(recovery_fds):
                    os.close(recovery_fd)
            checks["exact_claim_requires_preexisting_terminal_bundles"] = (
                missing_bundle_rejected and leftover_stage_rejected
            )

            os.mkdir("live-parent", 0o700, dir_fd=root_fd)
            live_parent_fd = open_dir_at(root_fd, "live-parent")
            try:
                os.rename(
                    "live-parent", "detached-parent",
                    src_dir_fd=root_fd, dst_dir_fd=root_fd,
                )
                os.mkdir("live-parent", 0o700, dir_fd=root_fd)
                path_swap_rejected = False
                try:
                    attest_directory_fd(
                        live_parent_fd, Path(directory) / "live-parent",
                        "selftest parent path swap",
                    )
                except Reject:
                    path_swap_rejected = True
                checks["preclaim_parent_fd_path_swap_rejected"] = (
                    path_swap_rejected
                )
            finally:
                os.close(live_parent_fd)

            write_once_at(root_fd, "simulated-final-stage", b"seal\n")
            ambiguous_tracker = WriteTracker()
            ambiguous_tracker.before_write(
                "FINAL_GLOBAL_HEAD_SEAL_LAST_WRITE"
            )
            rename_noreplace(
                root_fd, "simulated-final-stage",
                root_fd, "simulated-final-seal",
            )
            # Model rename success followed by parent-fsync/replay failure.
            ambiguous = failure_authority_fields(ambiguous_tracker)
            checks["rename_success_fsync_failure_is_authority_unknown"] = (
                exact_or_absent(
                    root_fd, "simulated-final-seal", b"seal\n"
                ) == "EXACT"
                and ambiguous["authority_state"]
                == "UNKNOWN_OR_FORK_REQUIRES_EXTERNAL_RESOLUTION"
                and ambiguous["effective_authoritative_census"] is None
                and ambiguous["seal_created"] is None
                and ambiguous["verify_installed_required"] is True
            )
        finally:
            os.close(root_fd)
    barrier_state = {
        "candidate_payloads": {"candidate.json": b"candidate\n"},
        "audit_payloads": {"audit.json": b"audit\n"},
        "claim_raw": b"claim\n",
        "seal_raw": b"seal\n",
    }
    with tempfile.TemporaryDirectory(
        prefix="c53-pair-installer-claim-barrier-selftest-"
    ) as barrier_directory:
        barrier_root_fd = os.open(
            barrier_directory,
            os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW | os.O_CLOEXEC,
        )
        try:
            os.mkdir(CANDIDATE_PARENT, 0o700, dir_fd=barrier_root_fd)
            os.mkdir(AUDIT_PARENT, 0o700, dir_fd=barrier_root_fd)
            os.mkdir(GLOBAL_CLAIM_PARENT, 0o700, dir_fd=barrier_root_fd)
            os.mkdir(GLOBAL_HEAD_PARENT, 0o700, dir_fd=barrier_root_fd)
            candidate_fd = open_dir_at(barrier_root_fd, CANDIDATE_PARENT)
            audit_fd = open_dir_at(barrier_root_fd, AUDIT_PARENT)
            try:
                publish_bundle(
                    candidate_fd, CANDIDATE_TOKEN,
                    barrier_state["candidate_payloads"],
                )
                publish_bundle(
                    audit_fd, AUDIT_TOKEN, barrier_state["audit_payloads"],
                )
                exact_actions = reconcile_bundles_at_claim_barrier(
                    "EXACT", candidate_fd, audit_fd, barrier_state
                )
                checks["claim_barrier_exact_is_bundle_read_only"] = (
                    exact_actions == (
                        "READ_ONLY_VERIFIED_EXACT_AFTER_CLAIM_RESERVATION",
                        "READ_ONLY_VERIFIED_EXACT_AFTER_CLAIM_RESERVATION",
                    )
                )
                claim_parent_fd = open_dir_at(
                    barrier_root_fd, GLOBAL_CLAIM_PARENT
                )
                try:
                    write_once_at(
                        claim_parent_fd, GLOBAL_CLAIM_STAGE,
                        barrier_state["claim_raw"],
                    )
                finally:
                    os.close(claim_parent_fd)
                claim_stage_slot = classify_c50d_runtime(
                    barrier_root_fd, barrier_state
                )
                checks["claim_stage_requires_terminal_bundles"] = (
                    claim_stage_slot["claim"] == "ABSENT"
                    and claim_stage_slot["claim_stage"] == "EXACT"
                    and claim_stage_slot["candidate_bundle"]
                    == claim_stage_slot["audit_bundle"] == "FINAL_EXACT"
                    and slot_progress_rank(claim_stage_slot) == 1
                )

                candidate_stage = "." + CANDIDATE_TOKEN + ".stage"
                os.mkdir(candidate_stage, 0o700, dir_fd=candidate_fd)
                leftover_inventory = sorted(os.listdir(candidate_fd))
                leftover_rejected = False
                leftover_classification_rejected = False
                try:
                    reconcile_bundles_at_claim_barrier(
                        "EXACT", candidate_fd, audit_fd, barrier_state
                    )
                except Reject:
                    leftover_rejected = True
                try:
                    classify_c50d_runtime(barrier_root_fd, barrier_state)
                except Reject:
                    leftover_classification_rejected = True
                checks["claim_barrier_leftover_stage_is_read_only_reject"] = (
                    leftover_rejected and leftover_classification_rejected
                    and sorted(os.listdir(candidate_fd)) == leftover_inventory
                )
                os.rmdir(candidate_stage, dir_fd=candidate_fd)

                held_token = CANDIDATE_TOKEN + "-held"
                os.rename(
                    CANDIDATE_TOKEN, held_token,
                    src_dir_fd=candidate_fd, dst_dir_fd=candidate_fd,
                )
                missing_inventory = sorted(os.listdir(candidate_fd))
                missing_rejected = False
                missing_classification_rejected = False
                try:
                    reconcile_bundles_at_claim_barrier(
                        "EXACT", candidate_fd, audit_fd, barrier_state
                    )
                except (Reject, OSError):
                    missing_rejected = True
                try:
                    classify_c50d_runtime(barrier_root_fd, barrier_state)
                except (Reject, OSError):
                    missing_classification_rejected = True
                checks["claim_barrier_missing_bundle_not_reconstructed"] = (
                    missing_rejected and missing_classification_rejected
                    and node_at(candidate_fd, CANDIDATE_TOKEN) is None
                    and sorted(os.listdir(candidate_fd)) == missing_inventory
                )
                os.rename(
                    held_token, CANDIDATE_TOKEN,
                    src_dir_fd=candidate_fd, dst_dir_fd=candidate_fd,
                )

                wrong_token = CANDIDATE_TOKEN + "-wrong"
                publish_bundle(
                    candidate_fd, wrong_token,
                    {"candidate.json": b"wrong\n"},
                )
                good_token = CANDIDATE_TOKEN + "-good"
                os.rename(
                    CANDIDATE_TOKEN, good_token,
                    src_dir_fd=candidate_fd, dst_dir_fd=candidate_fd,
                )
                os.rename(
                    wrong_token, CANDIDATE_TOKEN,
                    src_dir_fd=candidate_fd, dst_dir_fd=candidate_fd,
                )
                replaced_inventory = sorted(os.listdir(candidate_fd))
                replacement_rejected = False
                replacement_classification_rejected = False
                try:
                    reconcile_bundles_at_claim_barrier(
                        "EXACT", candidate_fd, audit_fd, barrier_state
                    )
                except Reject:
                    replacement_rejected = True
                try:
                    classify_c50d_runtime(barrier_root_fd, barrier_state)
                except Reject:
                    replacement_classification_rejected = True
                checks["claim_barrier_replaced_bundle_not_repaired"] = (
                    replacement_rejected
                    and replacement_classification_rejected
                    and sorted(os.listdir(candidate_fd)) == replaced_inventory
                )
            finally:
                os.close(audit_fd)
                os.close(candidate_fd)
        finally:
            os.close(barrier_root_fd)
    value = close_object({"schema": "selftest", "status": "PASS"}, "object_sha256")
    checks["canonical_self_hash"] = object_digest(value, "object_sha256") == value["object_sha256"]
    checks["placeholder_pin_fixture_rejected"] = not pins_frozen(
        ("__PLACEHOLDER__", "0" * 64)
    )
    checks["pair_indices_atomic"] = TASK_BINDINGS == list(dict.fromkeys(TASK_BINDINGS)) and len(TASK_BINDINGS) == 2
    checks["pending_arithmetic"] = 33_642 - 1 - 1 - 2 == AFTER["logical_pending_task_count"]
    checks["physical_arithmetic"] = 67_284 - 2 - 2 - 4 == AFTER["two_side_pending_occurrence_count"]
    checks["coarse_transition"] = (
        AFTER["paired_coarse_cells"] == BEFORE["paired_coarse_cells"] + 2
        and AFTER["unresolved_coarse_cells"] == BEFORE["unresolved_coarse_cells"] - 2
        and AFTER["representative_parents_remaining"]
        == BEFORE["representative_parents_remaining"] - 1
    )
    c50d_prefixes = C50D_ALLOWED_PREFIXES
    checks["C50d_S0_through_S4_prefixes"] = len(c50d_prefixes) == 5
    checks["head_without_claim_rejected"] = (
        ("ABSENT", "EXACT", "EXACT", "EXACT") not in c50d_prefixes
    )

    def synthetic_slot(
        prefix: tuple[str, str, str, str],
        stages: tuple[str, str, str, str],
    ) -> dict[str, str]:
        return {
            "claim": prefix[0],
            "candidate_pointer": prefix[1],
            "audit_pointer": prefix[2],
            "global_head_seal": prefix[3],
            "claim_stage": stages[0],
            "candidate_pointer_stage": stages[1],
            "audit_pointer_stage": stages[2],
            "global_head_stage": stages[3],
        }

    no_stages = ("ABSENT", "ABSENT", "ABSENT", "ABSENT")
    interleaved_slots = [
        synthetic_slot(("ABSENT", "ABSENT", "ABSENT", "ABSENT"), no_stages),
        synthetic_slot(
            ("ABSENT", "ABSENT", "ABSENT", "ABSENT"),
            ("EXACT", "ABSENT", "ABSENT", "ABSENT"),
        ),
        synthetic_slot(("EXACT", "ABSENT", "ABSENT", "ABSENT"), no_stages),
        synthetic_slot(
            ("EXACT", "ABSENT", "ABSENT", "ABSENT"),
            ("ABSENT", "EXACT", "ABSENT", "ABSENT"),
        ),
        synthetic_slot(("EXACT", "EXACT", "ABSENT", "ABSENT"), no_stages),
        synthetic_slot(
            ("EXACT", "EXACT", "ABSENT", "ABSENT"),
            ("ABSENT", "ABSENT", "EXACT", "ABSENT"),
        ),
        synthetic_slot(("EXACT", "EXACT", "EXACT", "ABSENT"), no_stages),
        synthetic_slot(
            ("EXACT", "EXACT", "EXACT", "ABSENT"),
            ("ABSENT", "ABSENT", "ABSENT", "EXACT"),
        ),
        synthetic_slot(("EXACT", "EXACT", "EXACT", "EXACT"), no_stages),
    ]
    checks["C50d_target_stage_progress_total_order"] = (
        [slot_progress_rank(slot) for slot in interleaved_slots]
        == list(range(9))
    )
    invalid_recovery_states = [
        # Candidate stage without claim.
        (
            ("ABSENT", "ABSENT", "ABSENT", "ABSENT"),
            ("ABSENT", "EXACT", "ABSENT", "ABSENT"),
        ),
        # Audit stage without candidate target.
        (
            ("EXACT", "ABSENT", "ABSENT", "ABSENT"),
            ("ABSENT", "ABSENT", "EXACT", "ABSENT"),
        ),
        # Head stage without both pointer targets.
        (
            ("EXACT", "EXACT", "ABSENT", "ABSENT"),
            ("ABSENT", "ABSENT", "ABSENT", "EXACT"),
        ),
        # Exact S4 target plus a leftover head stage.
        (
            ("EXACT", "EXACT", "EXACT", "EXACT"),
            ("ABSENT", "ABSENT", "ABSENT", "EXACT"),
        ),
        # Impossible pointer order at the second barrier.
        (
            ("EXACT", "ABSENT", "EXACT", "ABSENT"),
            no_stages,
        ),
    ]
    invalid_rejected = 0
    for invalid_prefix, invalid_stages in invalid_recovery_states:
        try:
            validate_c50d_recovery_grammar(invalid_prefix, invalid_stages)
        except Reject:
            invalid_rejected += 1
    checks["C50d_unbound_and_leftover_file_stages_rejected"] = (
        invalid_rejected == len(invalid_recovery_states)
    )
    checks["C50d_exact_stage_regression_detected"] = (
        slot_progress_rank(interleaved_slots[2])
        < slot_progress_rank(interleaved_slots[3])
        and slot_progress_rank(interleaved_slots[4])
        < slot_progress_rank(interleaved_slots[5])
    )
    checks["predecessor_identity_exact"] = (
        expected_predecessor_identity()["predecessor_identity_sha256"]
        == C50D_PREDECESSOR_IDENTITY_SHA256
    )
    checks["predecessor_keyed_targets"] = (
        GLOBAL_CLAIM_BASENAME
        == "predecessor-" + C50D_PREDECESSOR_IDENTITY_SHA256 + ".claim"
        and GLOBAL_HEAD_BASENAME
        == "predecessor-" + C50D_PREDECESSOR_IDENTITY_SHA256 + ".seal"
        and "c53" not in GLOBAL_CLAIM_BASENAME.lower()
        and "c53" not in GLOBAL_HEAD_BASENAME.lower()
    )
    checks["complete_D02_census_conserved"] = (
        sum(D02_FORMAL_BEFORE[key] for key in (
            "EARLIEST_PREFIX_EXCLUDED", "TYPED_EVENT_GRAPH",
            "CONNECTED_TO_KNOWN", "SOURCE_GRAZING_OR_CEMETERY",
            "UNRESOLVED_R1648_CONTINUATION",
        )) == D02_FORMAL_BEFORE["total"] == 76_832
        and sum(D02_FORMAL_AFTER[key] for key in (
            "EARLIEST_PREFIX_EXCLUDED", "TYPED_EVENT_GRAPH",
            "CONNECTED_TO_KNOWN", "SOURCE_GRAZING_OR_CEMETERY",
            "UNRESOLVED_R1648_CONTINUATION",
        )) == D02_FORMAL_AFTER["total"] == 76_832
    )
    checks["source_AST_has_no_duplicate_literal_dict_keys"] = (
        duplicate_literal_dict_keys(SELF.read_text(encoding="utf-8")) == []
    )

    def synthetic_bundle_state(names: list[str], total: int) -> str:
        ordered = sorted(names)
        return (
            "RESUMABLE_STAGE_" + str(len(ordered)) + "_OF_" + str(total)
            + "__" + digest(ordered)[:16] + "__M700__FILES_"
            + ",".join(ordered)
        )

    subset_swap_rejected = False
    try:
        require_bundle_recovery_monotone(
            {
                "candidate_bundle": synthetic_bundle_state(["a"], 3),
                "audit_bundle": "ABSENT",
            },
            {
                "candidate_bundle": synthetic_bundle_state(["b", "c"], 3),
                "audit_bundle": "ABSENT",
            },
            "selftest same-count/set-theoretic bundle attack",
        )
    except Reject:
        subset_swap_rejected = True
    checks["bundle_stage_completion_requires_old_inventory_subset"] = (
        subset_swap_rejected
    )

    predecessor_tracker = WriteTracker()
    predecessor_tracker.before_write("BUNDLES_AND_NAMESPACES")
    predecessor_failure = failure_authority_fields(predecessor_tracker)
    checks["pre_final_failure_keeps_predecessor_effective"] = (
        predecessor_failure["authority_state"]
        == "PREDECESSOR_REMAINS_EFFECTIVE"
        and predecessor_failure["effective_authoritative_census"]
        == C50D_BEFORE
        and predecessor_failure["seal_created"] is False
    )
    observed_head_tracker = WriteTracker()
    observed_head_tracker.observe_possible_final_seal()
    observed_head_failure = failure_authority_fields(observed_head_tracker)
    checks["observed_unreplayed_head_is_authority_unknown"] = (
        observed_head_failure["authority_state"]
        == "UNKNOWN_OR_FORK_REQUIRES_EXTERNAL_RESOLUTION"
        and observed_head_failure["effective_authoritative_census"] is None
        and observed_head_failure["verify_installed_required"] is True
    )
    tracker = WriteTracker()
    checks["write_tracker_initial_read_only"] = (
        tracker.runtime_writes_may_have_occurred is False
        and tracker.final_seal_fully_replayed is False
    )
    tracker.before_write("SELFTEST")
    tracker.seal_verified()
    checks["write_tracker_truthful_transition"] = (
        tracker.runtime_writes_may_have_occurred is True
        and tracker.final_seal_fully_replayed is True
    )
    checks["global_head_is_only_commit"] = (
        GLOBAL_HEAD_PATH != GLOBAL_CLAIM_PATH
        and GLOBAL_HEAD_BASENAME not in {CANDIDATE_POINTER, AUDIT_POINTER}
    )
    total = len(checks)
    need(total == 40 and all(checks.values()),
         "C53 installer self-test 40/40")
    return {
        "schema": SCHEMA + ".self-test",
        "status": "PASS_C53_PAIR1_INSTALLER_SELF_TEST_40_OF_40",
        "passed": 40,
        "total": 40,
        "checks": checks,
        "runtime_writes_performed_outside_private_temp": False,
        "formal_credit": 0,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--self-test", action="store_true")
    mode.add_argument("--preflight", action="store_true")
    mode.add_argument("--dry-run", action="store_true")
    mode.add_argument("--verify-installed", action="store_true")
    mode.add_argument("--install", action="store_true")
    parser.add_argument("--expect-installer-sha256")
    parser.add_argument("--confirm")
    args = parser.parse_args()
    tracker = WriteTracker()
    try:
        if args.self_test:
            need(args.confirm is None, "self-test takes no confirmation")
            result = self_test()
        elif args.preflight:
            need(args.confirm is None, "preflight takes no confirmation")
            result = preflight(args.expect_installer_sha256)
        elif args.dry_run:
            need(args.confirm is None, "dry-run takes no confirmation")
            need(type(args.expect_installer_sha256) is str
                 and HEX64.fullmatch(args.expect_installer_sha256) is not None,
                 "--expect-installer-sha256 required")
            result = dry_run(args.expect_installer_sha256)
        elif args.verify_installed:
            need(args.confirm is None, "verify-installed takes no confirmation")
            need(type(args.expect_installer_sha256) is str
                 and HEX64.fullmatch(args.expect_installer_sha256) is not None,
                 "--expect-installer-sha256 required")
            inputs = Inputs(args.expect_installer_sha256)
            try:
                state = expected_state(inputs)
                result = verify_installed(inputs, state, tracker)
                tracker.seal_verified()
            finally:
                inputs.close()
        else:
            # This check precedes every runtime publication operation.
            need(all_terminal_pins_frozen(),
                 "installer disarmed: terminal C51/C52/C53 pins incomplete")
            need(args.confirm == CONFIRMATION, "exact install confirmation")
            need(type(args.expect_installer_sha256) is str
                 and HEX64.fullmatch(args.expect_installer_sha256) is not None,
                 "--expect-installer-sha256 required")
            inputs = Inputs(args.expect_installer_sha256)
            try:
                state = expected_state(inputs)
                result = install(inputs, state, tracker)
            finally:
                inputs.close()
        sys.stdout.buffer.write(canonical(result) + b"\n")
        return 0
    except (Reject, OSError, ValueError, KeyError, TypeError, StopIteration) as error:
        observe_global_head_for_failure(tracker)
        authority = failure_authority_fields(tracker)
        body = {
            "schema": SCHEMA + ".fail-closed",
            "status": "REJECT_C53_PAIR1_PAIR_LEVEL_SUCCESSOR_INSTALLER",
            "error_class": type(error).__name__,
            "reason": str(error),
            "failure_phase": tracker.phase,
            "entered_write_phases": tracker.entered_write_phases,
            "runtime_writes_performed": (
                False if not tracker.runtime_writes_may_have_occurred else None
            ),
            "runtime_writes_may_have_occurred":
                tracker.runtime_writes_may_have_occurred,
            "final_global_head_seal_fully_replayed":
                tracker.final_seal_fully_replayed,
            **authority,
            "formal_credit": 1 if tracker.final_seal_fully_replayed else 0,
            "D02_gate_credit": 0,
        }
        sys.stdout.buffer.write(canonical(close_object(body, "object_sha256")) + b"\n")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
