#!/usr/bin/env python3
"""Cold independent verifier for the C53 pair-1 atomic successor transaction.

The verifier treats C53, C51, C50a, C52, C46, C42, and C48 artifacts as
inert bytes.  It never imports or executes the C53 candidate producer, the
C51 route producer, or the C50a owner producer.  A PASS independently checks
the complete 64-shard public C46 plan, the complete shard-9 genesis vector,
all 589 candidate states, the two pair-1 task replacements, the 9 logical / 18
physical terminal bridge, the C42 862-row coarse census, the zero-coarse C48
logical predecessor, and a prospective seal-only promotion overlay.

This checked-in revision is deliberately disarmed.  C52 terminal audit hashes
and final C53 candidate hashes must be frozen below before ``--verify`` can
run.  ``--preflight`` and ``--self-test`` are read-only.  The verifier writes
only canonical JSON to stdout and never writes beneath ``.cm2-runtime``.
"""

from __future__ import annotations

import argparse
import ast
import base64
import copy
from fractions import Fraction
import gzip
import hashlib
import io
import json
import os
from pathlib import Path
import re
import stat
import sys
from typing import Any, Callable, Iterable


sys.dont_write_bytecode = True
SELF = Path(__file__).absolute()
ROOT = SELF.parent.parent
DELIVERABLES = ROOT / "deliverables"
RUNTIME = ROOT / ".cm2-runtime"

SCHEMA = "cm2.round306c53.d02-a-pair1-pair-level-successor.independent-verifier.v1"
PROMOTION_SCHEMA = SCHEMA + ".post-seal-promotion-derivation"
CLAIM_SCHEMA = "cm2.global-authority-predecessor-consumption-claim.v1"
CANDIDATE_SCHEMA = "cm2.round306c53.d02-a-pair1-pair-level-successor-candidate.v1"
HEX64 = re.compile(r"[0-9a-f]{64}\Z")
UNFROZEN = "__UNFROZEN__"

PAIR = 1
SHARD_INDEX = 9
SHARD_COUNT = 64
SHARD_TASK_COUNT = 589
GLOBAL_TASK_COUNT = 33_641
GLOBAL_INVENTORY_COUNT = 33_642
PAIR_COUNT = 862
PENDING_PAIR_COUNT = 575
TASK_BINDINGS = [
    "daada4d9fd48677629cbfa9872b073d5fdf1552b115bf94438e7357f9a5dd95b",
    "e37b527423ad1aabba7485faacd03f7bb95ba9d79caebd614fb63d38ccd8dac6",
]
ROOT_PATHS = ["111111110", "111111111"]
FRONTIERS = [
    ["0", "1"],
    ["00", "01", "10", "110", "1110", "11110", "11111"],
]
TASK_PROBE_OBJECTS = [
    "12cf9404b26241f9ce04fe1ba0563cc7e86912b31a7c417dfa7d3c7fac915c30",
    "b24e1872af4fbda8194717fab20d7f8d3b3a93f630c0868a423db845f2665894",
]

C46_SOURCE = DELIVERABLES / "cm2_round306c46_d02a_general_adaptive_lower_strata_closure_engine_v1.py"
C46_SOURCE_SHA256 = "365432e96f2c287ef3c5497b7d15e01a80775f52d8cf5b71810d6f4c0e4442ea"
C46_PLAN_OBJECT_SHA256 = "7d004f59282dee21a28db0cd0b727a9045f4befce207c96be4efb07d1399c9bf"
SHARD_ID = "c46-d02a-shard:0916976b9ec8a154268b3f290d1a4053ad47c8b8d41dbfe17d63cd0735c91095"
SHARD_BINDING_SEQUENCE_SHA256 = "da4be1a51035b750b7981507f6ff74967bf7f441475286af7a1dc6fa0f6abcb7"
GENESIS_CHECKPOINT_OBJECT_SHA256 = "b962a7f05c99ff1e3fe2f2af98319f5e3cab005cca68b453d9152bf2435cacee"

C42_DIR = RUNTIME / "candidates/c42-p391-formal-producer-20260811T044500Z-f1"
C42_SEAL = RUNTIME / "c42-current-authority-seal"
C42_RESULT = C42_DIR / "result.json"
C42_PARENT = C42_DIR / "parent_conservation.jsonl.gz"
C42_SEAL_FILE_SHA256 = "0e5a76059b2c9407340d88e07f4fcc356d376f5c24b7173e6b95fd5e06bc312d"
C42_SEAL_OBJECT_SHA256 = "b321552768a6aeae6c1d229e52b61ca0b4420314234e02e98366153d4156d460"
C42_RESULT_FILE_SHA256 = "f029c3ce6af33e2f93c33b4155286f60bfafecd724720a598b103ca3c263ccb0"
C42_RESULT_OBJECT_SHA256 = "a50914a266aff3396054d7f16e91d69db7fa735ad15f01cbf07eee8e708d99d2"
C42_PARENT_FILE_SHA256 = "9e414b2fea9de614e73fd72f604fb857fb332dbfef49f11c33ae3929f68c8323"
C42_PARENT_ROW_SEQUENCE_SHA256 = "00d8e4a88766a2bba46f9a06f528795773c0606d66cd71e87fa26700e2fa4807"

C48_SEAL = RUNTIME / "c48-current-task-authority-seal"
C48_RECEIPT = RUNTIME / (
    "c48-successor-audits/c48-independent-audit-cf0531127a5c-v1/"
    "installation_receipt.json"
)
C48_SEAL_FILE_SHA256 = "13a07654d2eba6b2f1072d4a6a70636a90437e1da18e0bbeb8630ab841e026c1"
C48_SEAL_OBJECT_SHA256 = "95297adbe0d2ee86788008046bc47c337a9c7a3fa0e46bd896e674a2931ec6b1"
C48_SUCCESSOR_OBJECT_SHA256 = "bbd909cad5a5d0b9cc44362be6acb26d527f86edc1b8191c06a246a514c9c984"
C48_RECEIPT_FILE_SHA256 = "00338955b3225d96670806ab482775313e0afb68ebf7cafe01608787d828561b"
C48_RECEIPT_OBJECT_SHA256 = "90e698b52b95a229805a5e800dd65bc7615998647564f5161b601c26e2b5b299"
C48_STATUS = (
    "COMMITTED_C48_PAIR668_GEN1_TASK_SUCCESSOR_AUTHORITY__ONE_AUDITED_"
    "TASK_LEVEL_SUCCESSOR__ZERO_D02_GATE_CREDIT"
)

C50D_PROTOCOL = DELIVERABLES / "cm2_round306c50d_global_successor_cas_protocol_freeze_v1.md"
C50D_PROTOCOL_COMPANION = Path(str(C50D_PROTOCOL) + ".sha256")
C50D_PROTOCOL_FILE_SHA256 = "46a1a0a78970a6219b5a03bf9b91820b9121f4e409a46adcbb0c2ef793eeaf86"
C50D_PROTOCOL_COMPANION_SHA256 = "d34e35ee41798700699addd02555d32ff6608204db99a869b8ba303cc9784c5a"

C51_RESULT = DELIVERABLES / "cm2_round306c53_d02a_pair1_c51_frozen_route_result_v1.json"
C51_RESULT_FILE_SHA256 = "a560cdae560ce06879e3df3b0265aa97249d879011c7844394da73ea6fb32976"
C51_OBJECT_SHA256 = "187344a3c524dce1898151bf64f507c181dde137a3710eb9bc5cd1b895a81f6e"
C51_SOURCE_SHA256 = "caf043d2a475f8c25e92785587db971a0d33242b8560dd096f09a1e5c6e72069"
C51_REPORT_SHA256 = "d2330ac69da6cdb0e3fa092c9b697c836a21026ebb52b9b3655f9487a88f6330"

C50A_FULL_RESULT = DELIVERABLES / "cm2_round306c50a_pair1_two_task_global_owner_full_candidate_v1.json.gz.b64"
C50A_FULL_AUDIT = DELIVERABLES / "cm2_round306c50a_pair1_two_task_global_owner_full_independent_audit_v1.json.gz.b64"
C50A_RESULT_ENCODED_SHA256 = "3a747cc92700bccc763d6cbf71ece51ebf5d3f5709b330a768c089099025174a"
C50A_RESULT_GZIP_SHA256 = "8cae20c2d26c1e4d8113f39687da4f05908c13f1fb7722fd1f035c2c2c50db15"
C50A_RESULT_FILE_SHA256 = "0c3ffd0a9ff26fd128366a6af22aabeb29f72346303988deb4773b5adcd4131e"
C50A_RESULT_OBJECT_SHA256 = "da4557c64b4ce9675a3f8bff8a250b7ec7b643c48aecd738c03b7abed01d0b82"
C50A_AUDIT_ENCODED_SHA256 = "71102222dd9d8ffe7c21675447405fd65709e0a46122fd5a428326a076838f85"
C50A_AUDIT_GZIP_SHA256 = "a7b860fbf49444aacfc350f12371c6751dfa1ed7b8c39434a587b0dfa763f56c"
C50A_AUDIT_FILE_SHA256 = "5068afb70ec8bf7fddc719324aeae4703fbc4e22d07a9b5555e348471c23dd66"
C50A_AUDIT_OBJECT_SHA256 = "c037b3b15d19b839a254e3122bce7b1f882f6f9e198638c50a08909bf71231d6"
C50A_REQUEST_OBJECT_SHA256 = "db6292e002ec3c0b810f74af192524407afb1cfa3566c4898aa7fa7b2a8e3496"
C50A_HISTORY_HEAD_SHA256 = "543e2289de5a465745f821f510efa62ea2d4985921e2649b7404665ae71c730f"

C52_SOURCE = DELIVERABLES / "cm2_round306c52_d02a_pair1_no_producer_cold_route_verifier_v1.py"
C52_AUDIT = DELIVERABLES / "cm2_round306c52_d02a_pair1_no_producer_cold_route_audit_v1.json"
C52_SOURCE_SHA256 = "6f7ab24f0439b2965e2f406cd9ee2e5078cd43020763a8b658fedf2bd34caeff"
C52_AUDIT_FILE_SHA256 = "ff4ffe3862722d2ff6a00829cc4fb5f2e0ce691e823bd0f6f1918d783f7c7203"
C52_AUDIT_OBJECT_SHA256 = "1667032a6fbbc56cd53983275d8203c2480a2d31c3d4dc3f39b7efaed77ccec4"
C52_STATUS = (
    "PASS_C52_PAIR1_NO_PRODUCER_IMPORT_COLD_INDEPENDENT_ROUTE_MARGIN_"
    "REFLECTION_KRAFT_AND_CANDIDATE_REQUEST_AUDIT__ZERO_CREDIT"
)

C53_SOURCE = DELIVERABLES / "cm2_round306c53_d02a_pair1_pair_level_successor_candidate_v1.py"
C53_RESULT = DELIVERABLES / "cm2_round306c53_d02a_pair1_pair_level_successor_candidate_result_v1.json"
C53_SOURCE_SHA256 = "c251d1d8bd7ae8f4988824021b0533dc796672939dcb1385d9cafa41fa1152e4"
C53_RESULT_FILE_SHA256 = "a145e8a67a8f715f61d06c22943c9be40c2470e22da074add440253b9df794d3"
C53_RESULT_OBJECT_SHA256 = "996b1f213e7fc5a315348a9698960d29a07fd45c0e52c54680961007a28ef052"
C53_SUCCESSOR_OBJECT_SHA256 = "a1566f78ec92d431aad6ef8f495947e204304a75ebdc81d558031e4dd83fe6a7"
C53_TRANSACTION_OBJECT_SHA256 = "f235583e44679fa19ed470dfe40a884378bd322dc4bb852d34b9e3a246470fb2"

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
ZERO_LOCK = {
    "ambient_credit": 0,
    "terminal_credit": 0,
    "whole_parent_credit": 0,
    "D02_gate_credit": 0,
    "formal_credit": 0,
}
C50D_BEFORE = {
    **BEFORE,
    "whole_representative_parent_count": 287,
}
C50D_AFTER = {
    **AFTER,
    "whole_representative_parent_count": 288,
}
D02_FORMAL_BEFORE = {
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
        "total_representatives": PAIR_COUNT,
        "paired_coarse_cells": 574,
        "remaining_representatives": 575,
    },
}
D02_FORMAL_AFTER = copy.deepcopy(D02_FORMAL_BEFORE)
D02_FORMAL_AFTER["four_class_cell_census"].update({
    "strict_exclusions": 75_388,
    "unresolved": 1_148,
})
D02_FORMAL_AFTER["representative_parent_census"].update({
    "terminal_representatives": 288,
    "paired_coarse_cells": 576,
    "remaining_representatives": 574,
})


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


def file_digest(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def sequence_digest(values: Iterable[str]) -> str:
    state = hashlib.sha256()
    for value in values:
        need(type(value) is str, "sequence member string")
        state.update(value.encode("ascii") + b"\n")
    return state.hexdigest()


def close_object(value: dict[str, Any], field: str) -> dict[str, Any]:
    need(field not in value, "fresh self-hash field:" + field)
    return {**value, field: digest(value)}


def object_digest(value: dict[str, Any], field: str) -> str:
    body = dict(value)
    need(field in body, "self-hash field present:" + field)
    body.pop(field)
    return digest(body)


def closed(value: dict[str, Any], field: str, expected: str, label: str) -> None:
    need(HEX64.fullmatch(expected) is not None, label + ": frozen object pin")
    need(value.get(field) == expected, label + ": object pin")
    need(object_digest(value, field) == expected, label + ": self-hash")


def strict_json(raw: bytes, label: str, *, canonical_line: bool = True) -> dict[str, Any]:
    need(b"\x00" not in raw and not raw.startswith(b"\xef\xbb\xbf"),
         label + ": byte hygiene")

    def pairs(items: list[tuple[str, Any]]) -> dict[str, Any]:
        output: dict[str, Any] = {}
        for key, value in items:
            need(key not in output, label + ": duplicate key:" + key)
            output[key] = value
        return output

    def noninteger(token: str) -> Any:
        raise Reject(label + ": noninteger JSON number:" + token)

    value = json.loads(
        raw.decode("utf-8", "strict"), object_pairs_hook=pairs,
        parse_float=noninteger, parse_constant=noninteger,
    )
    need(type(value) is dict, label + ": object")
    if canonical_line:
        need(raw == canonical(value) + b"\n", label + ": canonical newline")
    return value


def prefix_free(paths: list[str]) -> bool:
    return (
        len(paths) == len(set(paths))
        and all(type(path) is str and set(path) <= {"0", "1"} for path in paths)
        and not any(right.startswith(left) for left in paths for right in paths
                    if left != right)
    )


def kraft(paths: list[str]) -> Fraction:
    return sum((Fraction(1, 2 ** len(path)) for path in paths), Fraction(0))


def pins_frozen() -> bool:
    values = (
        C52_SOURCE_SHA256, C52_AUDIT_FILE_SHA256, C52_AUDIT_OBJECT_SHA256,
        C53_SOURCE_SHA256, C53_RESULT_FILE_SHA256, C53_RESULT_OBJECT_SHA256,
        C53_SUCCESSOR_OBJECT_SHA256, C53_TRANSACTION_OBJECT_SHA256,
    )
    return all(HEX64.fullmatch(value) is not None for value in values)


class Capture:
    """Stable owned-file capture through held openat parent and file FDs."""

    def __init__(self, path: Path, label: str, expected: str, maximum: int):
        need(HEX64.fullmatch(expected) is not None, label + ": complete file pin")
        absolute = path.absolute()
        need(ROOT == absolute or ROOT in absolute.parents, label + ": workspace path")
        parts = absolute.relative_to(ROOT).parts
        need(bool(parts), label + ": non-root file")
        current = os.open(ROOT, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW | os.O_CLOEXEC)
        try:
            for part in parts[:-1]:
                child = os.open(
                    part, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW | os.O_CLOEXEC,
                    dir_fd=current,
                )
                os.close(current)
                current = child
            self.parent_fd = current
            current = -1
            self.name = parts[-1]
            self.fd = os.open(
                self.name, os.O_RDONLY | os.O_NOFOLLOW | os.O_CLOEXEC,
                dir_fd=self.parent_fd,
            )
        finally:
            if current >= 0:
                os.close(current)
        self.path = absolute
        self.label = label
        self.before = os.fstat(self.fd)
        need(
            stat.S_ISREG(self.before.st_mode) and self.before.st_nlink == 1
            and self.before.st_uid == os.getuid()
            and 0 < self.before.st_size <= maximum,
            label + ": owned singleton bounded regular",
        )
        self.raw = self._read(maximum)
        self.sha256 = file_digest(self.raw)
        need(self.sha256 == expected, label + ": SHA-256")
        self.unchanged("initial")

    def _read(self, maximum: int) -> bytes:
        os.lseek(self.fd, 0, os.SEEK_SET)
        chunks: list[bytes] = []
        total = 0
        while True:
            block = os.read(self.fd, 1 << 20)
            if not block:
                break
            total += len(block)
            need(total <= maximum, self.label + ": read bound")
            chunks.append(block)
        need(total == self.before.st_size, self.label + ": exact read")
        return b"".join(chunks)

    def unchanged(self, phase: str) -> None:
        path_info = os.stat(self.name, dir_fd=self.parent_fd, follow_symlinks=False)
        now = os.fstat(self.fd)
        fingerprint = lambda row: (
            row.st_dev, row.st_ino, row.st_mode, row.st_nlink, row.st_uid,
            row.st_gid, row.st_size, row.st_mtime_ns, row.st_ctime_ns,
        )
        need(fingerprint(path_info) == fingerprint(now) == fingerprint(self.before),
             self.label + ": " + phase + " identity")
        need(file_digest(self._read(self.before.st_size)) == self.sha256,
             self.label + ": " + phase + " bytes")

    def close(self) -> None:
        os.close(self.fd)
        os.close(self.parent_fd)


def decode_bundle(
    raw: bytes, label: str, encoded_sha: str, gzip_sha: str,
    json_sha: str, maximum: int = 1 << 30,
) -> tuple[bytes, dict[str, Any]]:
    need(file_digest(raw) == encoded_sha, label + ": encoded SHA-256")
    need(all(byte in b"ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=\r\n\t "
             for byte in raw), label + ": base64 alphabet")
    try:
        compressed = base64.b64decode(b"".join(raw.split()), validate=True)
    except Exception as error:
        raise Reject(label + ": base64:" + str(error)) from error
    need(file_digest(compressed) == gzip_sha, label + ": gzip SHA-256")
    try:
        with gzip.GzipFile(fileobj=io.BytesIO(compressed), mode="rb") as stream:
            decoded = stream.read(maximum + 1)
    except Exception as error:
        raise Reject(label + ": gzip:" + str(error)) from error
    need(0 < len(decoded) <= maximum, label + ": decoded bound")
    need(file_digest(decoded) == json_sha, label + ": JSON SHA-256")
    return decoded, strict_json(decoded, label + " JSON")


def gzip_json_lines(raw: bytes, label: str, expected: str, maximum: int) -> list[dict[str, Any]]:
    need(file_digest(raw) == expected, label + ": gzip file SHA-256")
    try:
        with gzip.GzipFile(fileobj=io.BytesIO(raw), mode="rb") as stream:
            decoded = stream.read(maximum + 1)
    except Exception as error:
        raise Reject(label + ": gzip:" + str(error)) from error
    need(0 < len(decoded) <= maximum, label + ": decoded bound")
    need(decoded.endswith(b"\n"), label + ": terminal newline")
    rows = []
    for index, line in enumerate(decoded.splitlines(), 1):
        rows.append(strict_json(line + b"\n", label + ":" + str(index)))
    return rows


def expected_predecessor_identity() -> dict[str, Any]:
    body = {
        "authority_heads": [
            {
                "authority_schema":
                    "cm2.round306c42.f1-authority-commit-seal.v1",
                "role": "FORMAL_COARSE",
                "seal_file_sha256": C42_SEAL_FILE_SHA256,
                "seal_object_sha256": C42_SEAL_OBJECT_SHA256,
                "seal_path": ".cm2-runtime/c42-current-authority-seal",
                "successor_checkpoint_object_sha256": None,
            },
            {
                "authority_schema": (
                    "cm2.round306c48.d02-a-pair668-generation1-successor-"
                    "installer.v1.authority-seal"
                ),
                "role": "LOGICAL_TASK",
                "seal_file_sha256": C48_SEAL_FILE_SHA256,
                "seal_object_sha256": C48_SEAL_OBJECT_SHA256,
                "seal_path": ".cm2-runtime/c48-current-task-authority-seal",
                "successor_checkpoint_object_sha256":
                    C48_SUCCESSOR_OBJECT_SHA256,
            },
        ],
        "before_census": {
            "logical_pending_task_count": 33_640,
            "paired_coarse_cells": 574,
            "representative_parents_remaining": 575,
            "two_side_pending_occurrence_count": 67_280,
            "unresolved_coarse_cells": 1_150,
            "whole_representative_parent_count": 287,
        },
        "ordered_head_roles": ["FORMAL_COARSE", "LOGICAL_TASK"],
        "schema": "cm2.global-authority-predecessor-identity.v1",
    }
    return close_object(body, "predecessor_identity_sha256")


def source_independence(source: bytes) -> dict[str, Any]:
    tree = ast.parse(source.decode("utf-8", "strict"), filename=str(SELF))
    imported: set[str] = set()
    dynamic_calls: list[str] = []
    forbidden_stems = {
        "cm2_round306c53_d02a_pair1_pair_level_successor_candidate_v1",
        "cm2_round306c51_d02a_pair1_two_task_route_probe_v1",
        "cm2_round306c50a_global_codimension_owner_oracle_v1",
    }
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imported.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            imported.add(node.module)
        elif isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
            if node.func.id in {"exec", "eval", "compile", "__import__"}:
                dynamic_calls.append(node.func.id)
        elif isinstance(node, ast.Dict):
            literal = [
                key.value for key in node.keys
                if isinstance(key, ast.Constant) and isinstance(key.value, (str, int))
            ]
            need(len(literal) == len(set(literal)),
                 "verifier source duplicate literal dictionary key")
    need(not any(name.split(".")[-1] in forbidden_stems for name in imported),
         "forbidden producer static import")
    need(not dynamic_calls, "dynamic code execution forbidden")
    need(not (forbidden_stems & set(sys.modules)), "forbidden producer module loaded")
    return {
        "C53_candidate_producer_imported_or_executed": False,
        "C51_producer_imported_or_executed": False,
        "C50a_producer_imported_or_executed": False,
        "producer_artifacts_consumed_as_inert_bytes_only": True,
        "source_AST_import_and_dynamic_execution_scan_pass": True,
        "forbidden_modules_absent_from_sys_modules": True,
    }


def validate_c42(
    seal_raw: bytes, result_raw: bytes, parent_raw: bytes,
) -> tuple[dict[str, Any], dict[str, Any], list[dict[str, Any]]]:
    seal = strict_json(seal_raw, "C42 installed authority seal")
    closed(seal, "authority_seal_object_sha256", C42_SEAL_OBJECT_SHA256,
           "C42 seal")
    need(
        seal.get("candidate_object_sha256") == C42_RESULT_OBJECT_SHA256
        and seal.get("status") == "COMMITTED_C42_F1_AUTHORITY__574_PAIRED__1150_UNRESOLVED"
        and seal.get("formal_census_after_commit") == {
            "paired_coarse_cells": 574,
            "remaining_representatives": 575,
            "unresolved": 1_150,
            "whole_representatives": 287,
        },
        "C42 exact formal authority census",
    )
    result = strict_json(result_raw, "C42 candidate result")
    closed(result, "object_sha256", C42_RESULT_OBJECT_SHA256, "C42 result")
    ledger = result.get("ledgers", {}).get("parent_conservation", {})
    census = result.get("closure_census", {})
    four_class = result.get("round144_terminal_census", {})
    need(
        ledger.get("sha256") == C42_PARENT_FILE_SHA256
        and ledger.get("row_count") == PAIR_COUNT
        and ledger.get("row_hash_line_sequence_sha256")
        == C42_PARENT_ROW_SEQUENCE_SHA256
        and census.get("parent_conservation_row_count") == PAIR_COUNT
        and census.get("whole_terminal_representative_parent_count") == 287
        and census.get("whole_terminal_paired_coarse_cell_count") == 574,
        "C42 result exact parent ledger binding",
    )
    need(four_class == {
        "CONNECTED_TO_KNOWN": 0,
        "EARLIEST_PREFIX_EXCLUDED": 75_386,
        "SOURCE_GRAZING_OR_CEMETERY": 0,
        "TYPED_EVENT_GRAPH": 296,
        "UNRESOLVED_R1648_CONTINUATION": 1_150,
        "terminal_total": 76_832,
        "unresolved_zero": False,
    }, "C42 exact four-class 76832 baseline")
    rows = gzip_json_lines(
        parent_raw, "C42 parent conservation", C42_PARENT_FILE_SHA256, 32 << 20
    )
    need(len(rows) == PAIR_COUNT, "C42 exact 862 rows")
    whole = 0
    row_hashes = []
    for index, row in enumerate(rows):
        need(row.get("pair_index") == index, "C42 pair index order")
        observed = row.get("row_sha256")
        need(HEX64.fullmatch(observed or "") is not None, "C42 row hash shape")
        need(object_digest(row, "row_sha256") == observed, "C42 row self-hash")
        need(row.get("D02_gate_credit") == 0
             and row.get("parent_Kraft_conservation") == "1",
             "C42 row zero D02 and Kraft")
        credit = row.get("C34_common_refinement_credit")
        is_whole = (
            row.get("whole_representative_parent_terminal") is True
            and row.get("whole_reflected_parent_terminal") is True
            and row.get("unresolved_parent_volume") == "0"
        )
        need(credit in {0, 2} and is_whole == (credit == 2),
             "C42 whole/credit equivalence")
        whole += int(is_whole)
        row_hashes.append(observed)
    need(whole == 287 and PAIR_COUNT - whole == 575,
         "C42 287 whole / 575 unresolved")
    need(sequence_digest(row_hashes) == C42_PARENT_ROW_SEQUENCE_SHA256,
         "C42 parent row sequence")
    pair1 = rows[PAIR]
    need(
        pair1.get("C34_common_refinement_credit") == 0
        and pair1.get("unresolved_parent_volume") == "1/256"
        and pair1.get("nonterminal_leaf_count") == 2
        and pair1.get("terminal_leaf_count") == 72
        and pair1.get("leaf_count") == 74,
        "pair1 is unresolved by C42 with exactly two residual leaves",
    )
    return seal, result, rows


def validate_c48(raw: bytes, receipt_raw: bytes) -> dict[str, Any]:
    seal = strict_json(raw, "C48 installed logical authority seal")
    closed(seal, "authority_seal_object_sha256", C48_SEAL_OBJECT_SHA256,
           "C48 seal")
    need(
        seal.get("status") == C48_STATUS
        and seal.get("successor_checkpoint_object_sha256")
        == C48_SUCCESSOR_OBJECT_SHA256
        and seal.get("coarse_formal_authority_unchanged") == {
            "paired_coarse_cells": 574,
            "representative_parents_remaining": 575,
            "unresolved_coarse_cells": 1_150,
        }
        and seal.get("formal_scope") == {
            "D02_gate_credit": 0,
            "audited_task_level_successor_count": 1,
            "whole_parent_credit": 0,
        }
        and seal.get("receipt_file_sha256") == C48_RECEIPT_FILE_SHA256
        and seal.get("receipt_object_sha256") == C48_RECEIPT_OBJECT_SHA256,
        "C48 exact zero-coarse logical predecessor",
    )
    receipt = strict_json(receipt_raw, "C48 installation receipt")
    closed(receipt, "receipt_object_sha256", C48_RECEIPT_OBJECT_SHA256,
           "C48 receipt")
    need(
        receipt.get("candidate", {}).get("successor_checkpoint_object_sha256")
        == C48_SUCCESSOR_OBJECT_SHA256
        and receipt.get("predecessor_authority") == {
            "c42-current-audit-token":
                "59aca53c4c35260801b3c559648c88ee974db01ae950f045a5e5aecd64aa36e5",
            "c42-current-authority-seal": C42_SEAL_FILE_SHA256,
            "c42-current-token":
                "fbc5dd3c55bfdd3098ed34ae09ae633a9526a9c9cc6f40b3d87b5669b2ea7f07",
        }
        and receipt.get("formal_scope", {}).get("coarse_authority") == {
            "paired_coarse_cells": 574,
            "representative_parents_remaining": 575,
            "unresolved_coarse_cells": 1_150,
        }
        and receipt.get("formal_scope", {}).get(
            "remaining_C41_logical_tasks_after_C42_and_C48"
        ) == 33_640
        and receipt.get("formal_scope", {}).get("formal_whole_parent_credit") == 0
        and receipt.get("formal_scope", {}).get("D02_gate_credit") == 0,
        "C48 receipt exact C42 bridge and logical census",
    )
    return seal


def validate_c51(raw: bytes) -> tuple[dict[str, Any], dict[tuple[str, str, str], dict[str, Any]], list[str]]:
    route = strict_json(raw, "C51 frozen route")
    closed(route, "object_sha256", C51_OBJECT_SHA256, "C51 route")
    need(
        route.get("source_sha256") == C51_SOURCE_SHA256
        and route.get("status")
        == "PASS_PAIR1_TWO_TASK_DUAL_SIDE_STRICT_ROUTE_FRONTIERS_ZERO_CREDIT"
        and route.get("pair_index") == PAIR and route.get("task_count") == 2
        and route.get("both_tasks_route_closed") is True
        and route.get("prefix_free_and_Kraft_one_for_both_tasks") is True
        and route.get("formal_credit") == route.get("D02_gate_credit") == 0,
        "C51 exact route scope",
    )
    probes = route.get("task_probes")
    need(type(probes) is list and len(probes) == 2, "C51 two probes")
    bridge: dict[tuple[str, str, str], dict[str, Any]] = {}
    leaf_sequences: list[str] = []
    for index, (probe, binding, root, frontier, probe_hash) in enumerate(zip(
        probes, TASK_BINDINGS, ROOT_PATHS, FRONTIERS, TASK_PROBE_OBJECTS,
        strict=True,
    )):
        closed(probe, "task_probe_object_sha256", probe_hash,
               "C51 task probe " + str(index))
        need(
            probe.get("task_binding_sha256") == binding
            and probe.get("task_id") == "c46-d02a-task:" + binding
            and probe.get("root_path") == root
            and probe.get("frontier_paths") == frontier
            and probe.get("split_count") == (1 if index == 0 else 6)
            and prefix_free(frontier) and kraft(frontier) == 1,
            "C51 task identity/frontier " + str(index),
        )
        split_events = probe.get("split_events")
        need(type(split_events) is list and len(split_events) == probe["split_count"],
             "C51 exact split event count")
        for event in split_events:
            observed = event.get("split_object_sha256")
            need(HEX64.fullmatch(observed or "") is not None
                 and object_digest(event, "split_object_sha256") == observed,
                 "C51 split event self-hash")
        logical_rows = probe.get("dual_side_terminal_rows")
        need(type(logical_rows) is list and len(logical_rows) == len(frontier),
             "C51 logical terminal row count")
        by_path = {row.get("relative_path"): row for row in logical_rows}
        need(list(sorted(by_path)) == list(sorted(frontier))
             and len(by_path) == len(frontier), "C51 exact terminal frontier")
        for relative in frontier:
            sides = by_path[relative].get("physical_sides")
            need(type(sides) is list
                 and [row.get("side") for row in sides]
                 == ["REPRESENTATIVE", "REFLECTED"],
                 "C51 two ordered physical sides")
            for side in sides:
                key = (binding, side["side"], relative)
                need(key not in bridge, "C51 unique bridge key")
                need(
                    side.get("relative_path") == relative
                    and side.get("terminal_classification")
                    == "EXCLUDED_C40_COLLISION2_OWNER_MISMATCH"
                    and side.get("all_required_strict_margins_complete") is True
                    and side.get("unscreened_active_competitor_count") == 0
                    and side.get("formal_credit") == 0
                    and HEX64.fullmatch(side.get("leaf_object_sha256", "")) is not None,
                    "C51 strict physical terminal row",
                )
                bridge[key] = side
        ordered_leaf_hashes = [
            bridge[(binding, side, relative)]["leaf_object_sha256"]
            for side in ("REPRESENTATIVE", "REFLECTED")
            for relative in frontier
        ]
        leaf_sequences.append(sequence_digest(ordered_leaf_hashes))
    need(len(bridge) == 18, "C51 exact 18-side bridge")
    return route, bridge, leaf_sequences


def occurrence_core(row: dict[str, Any]) -> dict[str, Any]:
    return {
        key: value for key, value in row.items()
        if key not in {"geometric_side", "occupied_quadrants"}
    }


def validate_c50a(
    result_bundle: bytes, audit_bundle: bytes,
    route_bridge: dict[tuple[str, str, str], dict[str, Any]],
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    _result_raw, result = decode_bundle(
        result_bundle, "C50a full candidate", C50A_RESULT_ENCODED_SHA256,
        C50A_RESULT_GZIP_SHA256, C50A_RESULT_FILE_SHA256,
    )
    _audit_raw, audit = decode_bundle(
        audit_bundle, "C50a full independent audit", C50A_AUDIT_ENCODED_SHA256,
        C50A_AUDIT_GZIP_SHA256, C50A_AUDIT_FILE_SHA256,
    )
    closed(result, "object_sha256", C50A_RESULT_OBJECT_SHA256,
           "C50a full candidate")
    closed(audit, "object_sha256", C50A_AUDIT_OBJECT_SHA256,
           "C50a full audit")
    request = result.get("request")
    need(type(request) is dict, "C50a embedded request")
    closed(request, "request_object_sha256", C50A_REQUEST_OBJECT_SHA256,
           "C50a request")
    need(
        result.get("request_object_sha256") == C50A_REQUEST_OBJECT_SHA256
        and result.get("status")
        == "PASS_C50A_GENERIC_TWO_SIDE_HISTORY_BOUND_FULL_UNIVERSE_OWNER_ORACLE__ZERO_FORMAL_CREDIT"
        and result.get("formal_credit") == 0,
        "C50a result exact status/request",
    )
    transactions = request.get("transactions")
    need(type(transactions) is list and len(transactions) == 2,
         "C50a exact two transactions")
    replacements: dict[tuple[str, str, str], dict[str, Any]] = {}
    transaction_bindings: dict[str, str] = {}
    for index, (tx, binding, root, frontier, probe_hash) in enumerate(zip(
        transactions, TASK_BINDINGS, ROOT_PATHS, FRONTIERS, TASK_PROBE_OBJECTS,
        strict=True,
    )):
        task = tx.get("task", {})
        need(
            tx.get("transaction_index") == index
            and task.get("upstream_task_binding_sha256") == binding
            and task.get("root_semantic_path") == root
            and task.get("pair_index") == PAIR
            and tx.get("relative_frontier") == frontier,
            "C50a transaction task/frontier",
        )
        observed = tx.get("transaction_binding_sha256")
        need(HEX64.fullmatch(observed or "") is not None
             and object_digest(tx, "transaction_binding_sha256") == observed,
             "C50a transaction self-hash")
        transaction_bindings[binding] = observed
        rows = tx.get("replacements")
        need(type(rows) is list and len(rows) == 2 * len(frontier),
             "C50a replacement count")
        for row in rows:
            key = (binding, row.get("side"), row.get("relative_path"))
            need(key in route_bridge and key not in replacements,
                 "C50a unique replacement bridge key")
            c51 = route_bridge[key]
            evidence = row.get("source_evidence", {})
            need(
                row.get("semantic_path") == root + key[2]
                and row.get("physical_route_path") == c51.get("physical_route_path")
                and row.get("physical_cell_id") == c51.get("physical_cell_id")
                and row.get("exact_closed_box") == c51.get("exact_closed_box")
                and row.get("relative_parent_fraction")
                == str(Fraction(1, 2 ** len(key[2])))
                and evidence.get("source_task_probe_object_sha256") == probe_hash
                and evidence.get("source_physical_leaf_id")
                == c51.get("physical_leaf_id")
                and evidence.get("source_leaf_object_sha256")
                == c51.get("leaf_object_sha256")
                and evidence.get("source_compact_leaf_row_sha256") == digest(c51)
                and evidence.get("terminal_classification")
                == c51.get("terminal_classification")
                and evidence.get("all_required_strict_margins_complete") is True
                and evidence.get("formal_credit") == 0,
                "C51-to-C50a exact per-occurrence replacement bridge",
            )
            replacements[key] = row
    need(set(replacements) == set(route_bridge) and len(replacements) == 18,
         "C50a bridge covers all 18 C51 sides")

    history = result.get("history_replay", {})
    nodes = history.get("history_nodes")
    need(type(nodes) is list and len(nodes) == 2
         and history.get("transaction_count") == 2
         and history.get("history_head_sha256") == C50A_HISTORY_HEAD_SHA256,
         "C50a history chain census")
    target_ids = sorted(
        occurrence
        for node in nodes
        for occurrence in node.get("inserted_occurrence_ids", [])
    )
    need(len(target_ids) == len(set(target_ids)) == 18,
         "C50a exact 18 inserted target occurrence ids")
    target = result.get("target_replay", {})
    need(
        target.get("target_occurrence_count") == 18
        and target.get("target_occurrence_id_sequence_sha256")
        == sequence_digest(target_ids),
        "C50a target occurrence sequence",
    )

    ledger = result.get("owner_ledger", {})
    faces = ledger.get("face_atoms")
    corners = ledger.get("corner_entities")
    need(type(faces) is list and type(corners) is list
         and len(faces) == ledger.get("face_atom_count") == 52
         and len(corners) == ledger.get("corner_entity_count") == 36,
         "C50a owner ledger exact row counts")
    need(
        sequence_digest(row.get("face_atom_id") for row in faces)
        == ledger.get("face_atom_id_sequence_sha256")
        and sequence_digest(row.get("corner_entity_id") for row in corners)
        == ledger.get("corner_entity_id_sequence_sha256"),
        "C50a owner entity sequences",
    )
    occurrence_rows: dict[str, dict[str, Any]] = {}
    face_refs: list[str] = []
    corner_refs: list[str] = []

    def observe(row: dict[str, Any]) -> None:
        occurrence_id = row.get("physical_occurrence_id")
        if row.get("source_kind") != "HISTORY_REPLACEMENT" or occurrence_id not in target_ids:
            return
        core = occurrence_core(row)
        if occurrence_id in occurrence_rows:
            need(occurrence_rows[occurrence_id] == core,
                 "C50a target occurrence identity stable across owner rows")
        else:
            occurrence_rows[occurrence_id] = core

    seen_faces: set[str] = set()
    for face in faces:
        face_id = face.get("face_atom_id")
        incidents = face.get("incident_occurrences")
        need(type(face_id) is str and face_id not in seen_faces,
             "C50a unique face id")
        seen_faces.add(face_id)
        need(
            type(incidents) is list and len(incidents) == 2
            and face.get("incident_occurrence_count") == 2
            and face.get("geometric_side_counts")
            == {"LOWER_COORDINATE_SIDE": 1, "UPPER_COORDINATE_SIDE": 1}
            and face.get("incident_set_complete") is True
            and face.get("owner_unique") is True
            and face.get("positive_length_face_overlap_only") is True
            and face.get("owner") in incidents,
            "C50a face degree/incidence/owner",
        )
        for row in incidents:
            observe(row)
        refs = face.get("target_occurrence_face_references")
        need(type(refs) is list, "C50a face target references")
        for ref in refs:
            occurrence_id = ref.get("target_occurrence_id")
            need(occurrence_id in target_ids, "C50a face ref targets pair1 occurrence")
            face_refs.append(occurrence_id)

    seen_corners: set[str] = set()
    quadrants = {"t+_p+", "t+_p-", "t-_p+", "t-_p-"}
    for corner in corners:
        corner_id = corner.get("corner_entity_id")
        incidents = corner.get("incident_occurrences")
        need(type(corner_id) is str and corner_id not in seen_corners,
             "C50a unique corner id")
        seen_corners.add(corner_id)
        quadrant_rows = corner.get("quadrant_incident_occurrence_ids")
        need(
            type(incidents) is list and bool(incidents)
            and corner.get("incident_occurrence_count") == len(incidents)
            and corner.get("incident_set_complete") is True
            and corner.get("four_quadrant_germ_complete") is True
            and corner.get("owner_unique") is True
            and corner.get("owner") in incidents
            and type(quadrant_rows) is dict and set(quadrant_rows) == quadrants
            and all(type(value) is list and bool(value)
                    for value in quadrant_rows.values()),
            "C50a corner quadrants/incidence/owner",
        )
        for row in incidents:
            observe(row)
        refs = corner.get("target_corner_occurrence_ids")
        need(type(refs) is list and all(value in target_ids for value in refs),
             "C50a corner refs target pair1 occurrences")
        corner_refs.extend(refs)
    need(set(occurrence_rows) == set(target_ids),
         "all 18 target occurrences represented in owner ledger")
    need(len(face_refs) == ledger.get("target_face_atom_occurrence_count") == 78
         and set(face_refs) == set(target_ids),
         "all target face references complete")
    need(len(corner_refs) == ledger.get("target_corner_occurrence_count") == 72
         and set(corner_refs) == set(target_ids),
         "all target corner references complete")

    owner_bridge: dict[tuple[str, str, str], str] = {}
    for occurrence_id, row in occurrence_rows.items():
        key = (
            row.get("upstream_task_binding_sha256"), row.get("side"),
            row.get("relative_path"),
        )
        need(key in replacements and key not in owner_bridge,
             "owner occurrence unique bridge key")
        replacement = replacements[key]
        need(
            row.get("pair_index") == PAIR
            and row.get("physical_cell_id") == replacement.get("physical_cell_id")
            and row.get("physical_route_path") == replacement.get("physical_route_path")
            and row.get("semantic_path") == replacement.get("semantic_path")
            and row.get("transaction_binding_sha256")
            == transaction_bindings[key[0]],
            "C50a owner occurrence equals request replacement",
        )
        owner_bridge[key] = occurrence_id
    need(set(owner_bridge) == set(route_bridge),
         "C51-C50a-owner per-occurrence bridge is bijective")

    candidate_binding = audit.get("candidate", {})
    replay = audit.get("replay", {})
    independence = audit.get("independence_boundary", {})
    need(
        candidate_binding.get("file_sha256") == C50A_RESULT_FILE_SHA256
        and candidate_binding.get("object_sha256") == C50A_RESULT_OBJECT_SHA256
        and candidate_binding.get("request_object_sha256")
        == C50A_REQUEST_OBJECT_SHA256
        and replay.get("transaction_count") == 2
        and replay.get("target_occurrence_count") == 18
        and replay.get("face_atom_count") == 52
        and replay.get("corner_entity_count") == 36
        and replay.get("history_head_sha256") == C50A_HISTORY_HEAD_SHA256
        and replay.get("all_codimension_owners_unique") is True
        and independence.get("C50a_producer_imported_or_executed") is False
        and audit.get("formal_credit") == 0,
        "C50a independent full audit correlation",
    )
    mapping_rows = []
    face_counts = {value: face_refs.count(value) for value in target_ids}
    corner_counts = {value: corner_refs.count(value) for value in target_ids}
    for key in sorted(owner_bridge):
        c51 = route_bridge[key]
        mapping_rows.append({
            "task_binding_sha256": key[0],
            "transaction_binding_sha256": transaction_bindings[key[0]],
            "side": key[1],
            "relative_path": key[2],
            "physical_leaf_id": c51["physical_leaf_id"],
            "leaf_object_sha256": c51["leaf_object_sha256"],
            "compact_leaf_row_sha256": digest(c51),
            "target_occurrence_id": owner_bridge[key],
            "target_face_reference_count": face_counts[owner_bridge[key]],
            "target_corner_reference_count": corner_counts[owner_bridge[key]],
        })
    summary = {
        "request_object_sha256": C50A_REQUEST_OBJECT_SHA256,
        "transaction_count": 2,
        "replacement_count": 18,
        "target_occurrence_count": 18,
        "face_atom_count": 52,
        "corner_entity_count": 36,
        "face_reference_count": 78,
        "corner_reference_count": 72,
        "bridge_key_sequence_sha256": sequence_digest(
            "|".join(key) + "|" + owner_bridge[key] for key in sorted(owner_bridge)
        ),
        "candidate_mapping_row_sequence_sha256": sequence_digest(
            digest(row) for row in mapping_rows
        ),
        "candidate_mapping_rows": mapping_rows,
        "all_18_C51_C50a_owner_rows_correlated": True,
    }
    return result, audit, summary


def validate_c52(
    raw: bytes, route: dict[str, Any], leaf_sequences: list[str],
) -> tuple[dict[str, Any], dict[str, Any]]:
    audit = strict_json(raw, "C52 terminal cold audit")
    closed(audit, "object_sha256", C52_AUDIT_OBJECT_SHA256, "C52 audit")
    c51 = audit.get("C51", {})
    c50a = audit.get("C50a", {})
    tasks = audit.get("tasks")
    census = audit.get("census", {})
    independence = audit.get("independence", {})
    need(
        audit.get("status") == C52_STATUS
        and audit.get("verifier_source_sha256") == C52_SOURCE_SHA256
        and c51.get("object_sha256") == C51_OBJECT_SHA256
        and c51.get("independently_reconstructed_object_sha256")
        == C51_OBJECT_SHA256
        and c50a.get("candidate_object_sha256") == C50A_RESULT_OBJECT_SHA256
        and c50a.get("request_object_sha256") == C50A_REQUEST_OBJECT_SHA256
        and c50a.get("transaction_count") == 2
        and c50a.get("replacement_count") == 18
        and c50a.get("split_decision_count") == 14
        and c50a.get("all_candidate_request_fields_match_independent_replay") is True,
        "C52 exact C51/C50a bridge",
    )
    need(type(tasks) is list and len(tasks) == 2, "C52 two task rows")
    for index, row in enumerate(tasks):
        need(
            row.get("task_index") == index
            and row.get("task_binding_sha256") == TASK_BINDINGS[index]
            and row.get("root_path") == ROOT_PATHS[index]
            and row.get("frontier") == FRONTIERS[index]
            and row.get("task_probe_object_sha256") == TASK_PROBE_OBJECTS[index]
            and row.get("leaf_object_sequence_sha256") == leaf_sequences[index]
            and row.get("logical_leaf_count") == len(FRONTIERS[index])
            and row.get("physical_strict_terminal_count")
            == 2 * len(FRONTIERS[index])
            and row.get("prefix_free") is True
            and row.get("relative_Kraft_sum") == "1",
            "C52 exact task/leaf sequence " + str(index),
        )
    need(
        census.get("task_count") == 2
        and census.get("logical_leaf_count") == 9
        and census.get("physical_side_strict_terminal_count") == 18
        and census.get("collision1_strict_margin_complete_count") == 18
        and census.get("collision2_strict_margin_complete_count") == 18
        and census.get("collision2_55_candidate_replay_count") == 18
        and census.get("collision2_positive_boundary_separation_row_count") == 972
        and census.get("reflection_pair_count") == 9
        and census.get("prefix_free_task_count") == 2
        and census.get("Kraft_one_task_count") == 2,
        "C52 numeric/reflection/Kraft census",
    )
    need(
        independence.get("C51_producer_imported_or_executed") is False
        and independence.get("C48_producer_imported_or_executed") is False
        and independence.get("C40_independent_numeric_implementation_replayed") is True
        and independence.get("C50a_candidate_consumed_as_data_only") is True
        and audit.get("frozen_pre_post_equal") is True
        and audit.get("coherent_attack_count") == 22
        and type(audit.get("coherent_attacks")) is list
        and len(audit["coherent_attacks"]) == 22
        and audit.get("all_attacks_fail_closed") is True
        and all(row.get("fail_closed") is True for row in audit["coherent_attacks"])
        and audit.get("formal_credit") == audit.get("D02_gate_credit") == 0
        and audit.get("runtime_writes_performed") is False
        and audit.get("candidate_or_authority_created") is False
        and audit.get("pointer_seal_or_canonical_modified") is False,
        "C52 independence/immutability/22 attacks/zero credit",
    )
    summary = {
        "audit_object_sha256": C52_AUDIT_OBJECT_SHA256,
        "independently_reconstructed_C51_object_sha256": C51_OBJECT_SHA256,
        "task_probe_object_sha256s": TASK_PROBE_OBJECTS,
        "leaf_object_sequence_sha256s": leaf_sequences,
        "numeric_strict_side_count": 18,
        "coherent_attacks_passed": 22,
    }
    return audit, summary


def scan_inert_candidate_source(raw: bytes) -> dict[str, Any]:
    tree = ast.parse(raw.decode("utf-8", "strict"), filename=str(C53_SOURCE))
    duplicate_count = 0
    for node in ast.walk(tree):
        if not isinstance(node, ast.Dict):
            continue
        literal = [
            key.value for key in node.keys
            if isinstance(key, ast.Constant) and isinstance(key.value, (str, int))
        ]
        duplicate_count += len(literal) - len(set(literal))
    need(duplicate_count == 0, "C53 candidate source duplicate literal keys")
    return {
        "candidate_source_sha256": file_digest(raw),
        "candidate_source_parsed_as_inert_AST": True,
        "candidate_source_executed": False,
        "duplicate_literal_key_count": 0,
    }


def validate_plan_and_genesis(
    plan: dict[str, Any], genesis: dict[str, Any],
) -> tuple[dict[str, Any], list[dict[str, Any]], dict[str, Any]]:
    closed(plan, "plan_object_sha256", C46_PLAN_OBJECT_SHA256, "C46 public plan")
    need(
        plan.get("engine_source", {}).get("sha256") == C46_SOURCE_SHA256
        and plan.get("queue", {}).get("full_inventory_task_count")
        == GLOBAL_INVENTORY_COUNT
        and plan.get("queue", {}).get("default_execution_queue_count")
        == GLOBAL_TASK_COUNT
        and plan.get("queue", {}).get("installed_C42_closed_task_count") == 1,
        "C46 plan source/inventory census",
    )
    sharding = plan.get("sharding", {})
    shards = sharding.get("shards")
    need(
        sharding.get("shard_count") == SHARD_COUNT
        and sharding.get("pair_count") == PENDING_PAIR_COUNT
        and sharding.get("task_count") == GLOBAL_TASK_COUNT
        and sharding.get("pair_preserving") is True
        and sharding.get("shards_disjoint_and_complete") is True
        and type(shards) is list and len(shards) == SHARD_COUNT
        and [row.get("shard_index") for row in shards] == list(range(SHARD_COUNT)),
        "C46 exact 64-shard public plan",
    )
    seen_pairs: dict[int, int] = {}
    task_sum = 0
    for shard in shards:
        shard_body = dict(shard)
        observed_id = shard_body.pop("shard_id", None)
        need(observed_id == "c46-d02a-shard:" + digest(shard_body),
             "C46 public shard self-id")
        pairs = shard.get("pair_indices")
        need(type(pairs) is list and pairs == sorted(set(pairs))
             and shard.get("pair_count") == len(pairs)
             and shard.get("pair_preserving") is True,
             "C46 shard exact pair inventory")
        task_sum += shard.get("task_count", -1)
        for pair in pairs:
            need(type(pair) is int and 0 <= pair < PAIR_COUNT
                 and pair not in seen_pairs, "C46 global pair uniqueness")
            seen_pairs[pair] = shard["shard_index"]
    need(len(seen_pairs) == PENDING_PAIR_COUNT and task_sum == GLOBAL_TASK_COUNT,
         "C46 shards cover 575 pending pairs / 33641 tasks")
    need(seen_pairs.get(PAIR) == SHARD_INDEX
         and sum(PAIR in row["pair_indices"] for row in shards) == 1,
         "pair1 occurs in exactly shard9 across all 64 shards")
    shard9 = shards[SHARD_INDEX]
    need(
        shard9.get("shard_id") == SHARD_ID
        and shard9.get("task_count") == SHARD_TASK_COUNT
        and shard9.get("ordered_task_binding_sequence_sha256")
        == SHARD_BINDING_SEQUENCE_SHA256,
        "C46 shard9 exact pins",
    )

    closed(genesis, "checkpoint_object_sha256", GENESIS_CHECKPOINT_OBJECT_SHA256,
           "C46 shard9 genesis")
    states = genesis.get("task_states")
    need(
        genesis.get("plan_object_sha256") == C46_PLAN_OBJECT_SHA256
        and genesis.get("shard_id") == SHARD_ID
        and genesis.get("shard_index") == SHARD_INDEX
        and genesis.get("generation") == 0
        and genesis.get("previous_checkpoint_object_sha256") is None
        and genesis.get("task_count") == SHARD_TASK_COUNT
        and genesis.get("completed_task_count") == 0
        and genesis.get("pending_task_count") == SHARD_TASK_COUNT
        and genesis.get("ordered_task_binding_sequence_sha256")
        == SHARD_BINDING_SEQUENCE_SHA256
        and type(states) is list and len(states) == SHARD_TASK_COUNT,
        "C46 exact shard9 genesis vector",
    )
    for index, state in enumerate(states):
        frontier = state.get("frontier")
        need(
            state.get("schema")
            == "cm2.round306c46.d02-a-general-adaptive-lower-strata.v1.task-state"
            and state.get("state") == "RESUMABLE_PENDING_ZERO_CREDIT"
            and state.get("pair_index") in seen_pairs
            and type(state.get("task_binding_sha256")) is str
            and state.get("task_id") == "c46-d02a-task:" + state["task_binding_sha256"]
            and type(frontier) is list and len(frontier) == 1
            and frontier[0].get("relative_path") == ""
            and frontier[0].get("relative_fraction") == "1"
            and state.get("exits") == [] and state.get("split_events") == []
            and state.get("event_count") == 0
            and state.get("relative_Kraft_sum") == "1"
            and state.get("prefix_free") is True,
            "C46 initial state shape:" + str(index),
        )
    bindings = [row["task_binding_sha256"] for row in states]
    need(sequence_digest(bindings) == SHARD_BINDING_SEQUENCE_SHA256,
         "C46 genesis binding sequence")
    need(
        genesis.get("ordered_task_state_sequence_sha256")
        == sequence_digest(digest(row) for row in states),
        "C46 genesis state sequence",
    )
    pair1_indices = [index for index, row in enumerate(states)
                     if row.get("pair_index") == PAIR]
    need(pair1_indices == [0, 1]
         and bindings[:2] == TASK_BINDINGS
         and [states[index].get("source_descendant_path") for index in (0, 1)]
         == ROOT_PATHS,
         "pair1 exact two genesis tasks at shard9 indices0/1")
    summary = {
        "plan_object_sha256": C46_PLAN_OBJECT_SHA256,
        "shard_count": SHARD_COUNT,
        "pending_pair_count": PENDING_PAIR_COUNT,
        "pending_task_count": GLOBAL_TASK_COUNT,
        "pair1_unique_shard_index": SHARD_INDEX,
        "pair1_task_indices": [0, 1],
        "pair1_task_binding_sha256s": TASK_BINDINGS,
        "shard9_genesis_object_sha256": GENESIS_CHECKPOINT_OBJECT_SHA256,
        "shard9_state_count": SHARD_TASK_COUNT,
    }
    return shard9, states, summary


def validate_membership_proof(
    proof: dict[str, Any], plan: dict[str, Any], genesis_states: list[dict[str, Any]],
) -> None:
    shards = plan["sharding"]["shards"]
    membership = [
        {"pair_index": pair, "shard_index": shard["shard_index"],
         "shard_id": shard["shard_id"]}
        for shard in shards for pair in shard["pair_indices"]
    ]
    membership.sort(key=lambda row: row["pair_index"])
    pair1_membership = [
        row for row in membership if row["pair_index"] == PAIR
    ]
    need(len(pair1_membership) == 1,
         "C46 pair1 has exactly one global shard membership")
    pair1_tasks = [{
        "shard_index": SHARD_INDEX,
        "task_index": index,
        "task_id": genesis_states[index]["task_id"],
        "task_binding_sha256": genesis_states[index]["task_binding_sha256"],
        "root_path": genesis_states[index]["source_descendant_path"],
        "priority_class": "DIRECT_WHOLE_PAIR",
    } for index in (0, 1)]
    need(
        proof.get("C46_plan_object_sha256") == C46_PLAN_OBJECT_SHA256
        and proof.get("full_C41_residual_task_count") == GLOBAL_INVENTORY_COUNT
        and proof.get("default_C42_only_pending_task_count") == GLOBAL_TASK_COUNT
        and proof.get("global_parent_conservation_count") == PAIR_COUNT
        and proof.get("unresolved_representative_pair_count") == PENDING_PAIR_COUNT
        and proof.get("shard_count") == SHARD_COUNT
        and proof.get("pair_to_shard_membership_count") == PENDING_PAIR_COUNT
        and proof.get("pair_to_shard_membership_sequence_sha256")
        == sequence_digest(digest(row) for row in membership)
        and proof.get("pair1_pair_membership") == pair1_membership
        and proof.get("pair1_global_task_membership") == pair1_tasks
        and proof.get("pair1_global_task_count") == 2
        and proof.get("pair1_absent_from_all_other_shards") is True
        and proof.get("pair1_was_unresolved_under_C42") is True
        and proof.get("formal_credit") == 0,
        "candidate global pair membership proof equals independent replay",
    )


def expected_mapping_proof(summary: dict[str, Any]) -> dict[str, Any]:
    body = {
        "schema": CANDIDATE_SCHEMA + ".C51-C50a-per-occurrence-mapping-proof",
        "replacement_count": 18,
        "target_occurrence_count": 18,
        "face_reference_count": 78,
        "corner_reference_count": 72,
        "all_replacements_biject_to_target_occurrences": True,
        "all_target_face_incident_sets_complete_and_owner_unique": True,
        "all_target_corner_germs_complete_and_owner_unique": True,
        "mapping_row_sequence_sha256": summary[
            "candidate_mapping_row_sequence_sha256"
        ],
        "mapping_rows": summary["candidate_mapping_rows"],
        "formal_credit": 0,
    }
    return close_object(body, "proof_object_sha256")


def validate_successor_checkpoint(
    successor: dict[str, Any], genesis_states: list[dict[str, Any]],
    route: dict[str, Any], mapping_proof: dict[str, Any],
) -> dict[str, Any]:
    closed(successor, "successor_checkpoint_object_sha256",
           C53_SUCCESSOR_OBJECT_SHA256, "C53 successor checkpoint")
    states = successor.get("task_states")
    need(
        successor.get("plan_object_sha256") == C46_PLAN_OBJECT_SHA256
        and successor.get("shard_id") == SHARD_ID
        and successor.get("shard_index") == SHARD_INDEX
        and successor.get("generation") == 1
        and successor.get("local_previous_checkpoint_object_sha256")
        == GENESIS_CHECKPOINT_OBJECT_SHA256
        and successor.get("global_previous_authority_seal_object_sha256")
        == C48_SEAL_OBJECT_SHA256
        and successor.get("global_previous_successor_checkpoint_object_sha256")
        == C48_SUCCESSOR_OBJECT_SHA256
        and successor.get("task_count") == SHARD_TASK_COUNT
        and successor.get("selected_pair_index") == PAIR
        and successor.get("selected_task_indices") == [0, 1]
        and successor.get("candidate_closed_task_count") == 2
        and successor.get("formal_closed_task_count_before_pair_seal") == 0
        and successor.get("pending_task_count_after_candidate") == 587
        and successor.get("ordered_task_binding_sequence_sha256")
        == SHARD_BINDING_SEQUENCE_SHA256
        and type(states) is list and len(states) == SHARD_TASK_COUNT,
        "C53 successor exact local/global predecessor and state census",
    )
    need(
        all(canonical(states[index]) == canonical(genesis_states[index])
            for index in range(2, SHARD_TASK_COUNT))
        and successor.get("unchanged_indices_2_through_588_byte_equal_to_genesis")
        is True
        and successor.get("unchanged_indices_2_through_588_task_state_sequence_sha256")
        == sequence_digest(digest(row) for row in genesis_states[2:]),
        "C53 exact 587 unchanged genesis states",
    )
    need(
        successor.get("ordered_task_state_sequence_sha256")
        == sequence_digest(digest(row) for row in states),
        "C53 full 589-state sequence",
    )
    mapping_by_task_path: dict[tuple[str, str], list[dict[str, Any]]] = {}
    for row in mapping_proof["mapping_rows"]:
        mapping_by_task_path.setdefault(
            (row["task_binding_sha256"], row["relative_path"]), []
        ).append(row)
    for index in (0, 1):
        state = states[index]
        observed = state.get("successor_task_state_sha256")
        need(HEX64.fullmatch(observed or "") is not None
             and object_digest(state, "successor_task_state_sha256") == observed,
             "C53 selected task state self-hash")
        need(
            state.get("C46_predecessor_task_state_sha256")
            == digest(genesis_states[index])
            and state.get("task_id") == "c46-d02a-task:" + TASK_BINDINGS[index]
            and state.get("task_binding_sha256") == TASK_BINDINGS[index]
            and state.get("pair_index") == PAIR
            and state.get("source_descendant_path") == ROOT_PATHS[index]
            and state.get("frontier") == []
            and state.get("candidate_closed") is True
            and state.get("formal_closed") is False
            and state.get("credit_lock") == ZERO_LOCK
            and state.get("relative_Kraft_sum") == "1"
            and state.get("prefix_free") is True,
            "C53 selected task is pre-seal zero-credit closed candidate",
        )
        exits = state.get("exits")
        need(type(exits) is list and len(exits) == len(FRONTIERS[index]),
             "C53 selected task exit count")
        exit_by_path = {row.get("relative_path"): row for row in exits}
        need(set(exit_by_path) == set(FRONTIERS[index])
             and prefix_free(list(exit_by_path)) and kraft(list(exit_by_path)) == 1,
             "C53 selected task exact Kraft exit frontier")
        probe = route["task_probes"][index]
        c51_by_path = {
            row["relative_path"]: row for row in probe["dual_side_terminal_rows"]
        }
        for relative in FRONTIERS[index]:
            exit_row = exit_by_path[relative]
            certificate = exit_row.get("certificate")
            need(type(certificate) is dict, "C53 complete exit certificate")
            certificate_hash = certificate.get("certificate_object_sha256")
            need(
                HEX64.fullmatch(certificate_hash or "") is not None
                and object_digest(certificate, "certificate_object_sha256")
                == certificate_hash
                and exit_row.get("certificate_object_sha256") == certificate_hash
                and certificate.get("task_binding_sha256") == TASK_BINDINGS[index]
                and certificate.get("relative_path") == relative
                and certificate.get("absolute_path") == ROOT_PATHS[index] + relative
                and certificate.get("relative_fraction")
                == str(Fraction(1, 2 ** len(relative)))
                and certificate.get("physical_sides")
                == c51_by_path[relative]["physical_sides"]
                and certificate.get("C51_task_probe_object_sha256")
                == TASK_PROBE_OBJECTS[index]
                and certificate.get("C50a_full_owner_candidate_object_sha256")
                == C50A_RESULT_OBJECT_SHA256
                and certificate.get("C50a_full_owner_audit_object_sha256")
                == C50A_AUDIT_OBJECT_SHA256
                and certificate.get("C51_C50a_mapping_proof_object_sha256")
                == mapping_proof["proof_object_sha256"]
                and certificate.get("C52_cold_route_audit_object_sha256")
                == C52_AUDIT_OBJECT_SHA256
                and certificate.get("both_physical_sides_independently_routed") is True
                and certificate.get("both_physical_sides_strictly_excluded") is True
                and certificate.get("all_strict_terminal_margins_complete") is True
                and certificate.get(
                    "full_active_universe_face_corner_owners_complete_and_unique"
                ) is True
                and certificate.get("formal_credit") == 0,
                "C53 exit certificate exact C51/C50a/C52 bridge",
            )
            expected_mappings = sorted(
                mapping_by_task_path[(TASK_BINDINGS[index], relative)],
                key=lambda row: row["side"],
            )
            need(certificate.get("C50a_target_occurrence_mappings")
                 == expected_mappings and len(expected_mappings) == 2,
                 "C53 exit exact two owner occurrence mappings")
        split_events = state.get("split_events")
        need(type(split_events) is list
             and len(split_events) == route["task_probes"][index]["split_count"],
             "C53 selected task split event count")
        for actual, source in zip(
            split_events, route["task_probes"][index]["split_events"], strict=True
        ):
            observed_split = actual.get("split_event_object_sha256")
            need(
                HEX64.fullmatch(observed_split or "") is not None
                and object_digest(actual, "split_event_object_sha256")
                == observed_split
                and actual.get("relative_path") == source.get("relative_path")
                and actual.get("absolute_path") == source.get("absolute_path")
                and actual.get("split_axis") == source.get("split_axis")
                and actual.get("C41_split_face_adjacency_sha256")
                == source.get("C41_split_face_adjacency_sha256")
                and actual.get("C51_split_object_sha256")
                == source.get("split_object_sha256")
                and actual.get("formal_credit") == 0,
                "C53 split event exact C51 binding",
            )
        need(state.get("event_count") == len(exits) + len(split_events),
             "C53 selected task event census")
    progress = successor.get("global_candidate_progress", {})
    need(
        progress.get("frozen_C41_logical_residual_outer_row_count")
        == GLOBAL_INVENTORY_COUNT
        and progress.get("installed_C42_logical_closed_task_count") == 1
        and progress.get("installed_C48_logical_closed_task_count") == 1
        and progress.get("authoritative_logical_pending_task_count_before_C53")
        == BEFORE["logical_pending_task_count"]
        and progress.get("logical_pending_task_count_after_C53_if_pair_sealed")
        == AFTER["logical_pending_task_count"]
        and progress.get("two_side_pending_occurrence_count_after_C53_if_pair_sealed")
        == AFTER["two_side_pending_occurrence_count"],
        "C53 exact global logical candidate arithmetic",
    )
    return {
        "successor_checkpoint_object_sha256": C53_SUCCESSOR_OBJECT_SHA256,
        "state_count": 589,
        "selected_candidate_closed_zero_credit_state_count": 2,
        "unchanged_genesis_state_count": 587,
        "logical_exit_count": 9,
        "physical_side_count": 18,
        "split_event_count": 7,
        "ordered_state_sequence_sha256": successor[
            "ordered_task_state_sequence_sha256"
        ],
    }


def validate_claim_contract(
    candidate: dict[str, Any], transaction: dict[str, Any],
    successor: dict[str, Any],
) -> dict[str, Any]:
    claim = candidate.get("global_predecessor_claim_template")
    need(type(claim) is dict,
         "C53 exact global_predecessor_claim_template present")
    field = "claim_template_object_sha256"
    observed = claim.get(field)
    need(HEX64.fullmatch(observed or "") is not None
         and object_digest(claim, field) == observed,
         "C53 predecessor claim self-hash")
    identity = claim.get("predecessor_authority_identity")
    if identity is None:
        identity = transaction.get("global_predecessor_authority_identity")
    need(type(identity) is dict, "C53 predecessor authority identity")
    identity_field = (
        "predecessor_identity_sha256" if "predecessor_identity_sha256" in identity
        else "predecessor_authority_identity_sha256"
    )
    identity_hash = identity.get(identity_field)
    need(HEX64.fullmatch(identity_hash or "") is not None
         and object_digest(identity, identity_field) == identity_hash,
         "C53 predecessor identity self-hash")
    expected_identity = expected_predecessor_identity()
    need(identity == expected_identity,
         "C53 predecessor identity exact C50d roles/fields/order/census")
    publication = claim.get("publication")
    if publication is None:
        publication = transaction.get("global_predecessor_claim_publication")
    need(type(publication) is dict, "C53 predecessor claim publication")
    basename = publication.get("claim_basename")
    expected_claim_basename = "predecessor-" + identity_hash + ".claim"
    expected_claim_path = (
        ".cm2-runtime/cm2-global-successor-claims/" + expected_claim_basename
    )
    expected_seal_path = (
        ".cm2-runtime/cm2-global-authority-heads/predecessor-"
        + identity_hash + ".seal"
    )
    need(
        publication.get("claim_namespace")
        in {"cm2-global-successor-claims", ".cm2-runtime/cm2-global-successor-claims"}
        and publication.get("claim_basename") == expected_claim_basename
        and publication.get("claim_relative_path") == expected_claim_path
        and publication.get("authority_seal_target_path") == expected_seal_path
        and publication.get("publication")
        == "O_EXCL_RENAME_NOREPLACE_UNDER_GLOBAL_AUTHORITY_LOCK"
        and publication.get("predecessor_keyed_not_successor_keyed") is True
        and publication.get("different_existing_bytes_are_a_fork_and_must_fail_closed")
        is True
        and publication.get("claim_without_authority_seal_is_reservation_only") is True
        and transaction.get("global_predecessor_authority_identity") == identity
        and transaction.get("global_predecessor_claim_publication") == publication
        and type(basename) is str,
        "C53 predecessor-keyed no-fork CAS contract and transaction bridge",
    )
    need(
        claim.get("schema")
        == "cm2.round306c53.global-predecessor-successor-final-claim-contract.v1"
        and claim.get("successor_domain") == CANDIDATE_SCHEMA
        and claim.get("pair_index") == PAIR
        and claim.get("task_binding_sha256s") == TASK_BINDINGS
        and claim.get("unique_pair_transaction_object_sha256")
        == transaction["pair_transaction_object_sha256"]
        and claim.get("unique_successor_checkpoint_object_sha256")
        == successor["successor_checkpoint_object_sha256"]
        and claim.get("single_successor_for_predecessor") is True
        and claim.get("forks_forbidden") is True
        and claim.get("D02_gate_credit") == 0,
        "C53 claim exact successor scope",
    )
    exact_final_claim_fields = [
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
    ]
    terminal_bindings = [
        "successor_candidate_file_sha256",
        "successor_candidate_object_sha256",
        "independent_audit_file_sha256",
        "independent_audit_object_sha256",
        "post_seal_promotion_derivation_object_sha256",
        "effective_post_seal_checkpoint_object_sha256",
        "authority_seal_target_path",
    ]
    required_semantics = {
        "task_indices_0_and_1_formal_closed": True,
        "per_task_credit_lock": ZERO_LOCK,
        "pair_level_whole_parent_credit": 1,
        "D02_gate_credit": 0,
        "authoritative_after": AFTER,
        "complete_D02_formal_census_before": D02_FORMAL_BEFORE,
        "complete_D02_formal_census_after": D02_FORMAL_AFTER,
        "C50d_before_census": C50D_BEFORE,
        "C50d_after_census": C50D_AFTER,
    }
    need(
        claim.get("C50d_protocol_binding") == {
            "protocol_file_sha256": C50D_PROTOCOL_FILE_SHA256,
            "protocol_companion_file_sha256": C50D_PROTOCOL_COMPANION_SHA256,
        }
        and claim.get("final_claim_schema") == CLAIM_SCHEMA
        and claim.get("final_claim_exact_fields_before_self_hash")
        == exact_final_claim_fields
        and claim.get("final_claim_self_hash_field") == "claim_object_sha256"
        and claim.get("final_claim_must_also_bind_after_terminal_bytes_exist")
        == terminal_bindings
        and claim.get("authority_seal_target_path") == expected_seal_path
        and claim.get("final_claim_is_constructed_only_after_independent_audit")
        is True
        and claim.get("candidate_does_not_mint_final_claim_or_promotion") is True
        and claim.get("final_seal_must_bind_final_claim_file_and_object_sha256")
        is True
        and claim.get("final_seal_must_bind_promotion_and_effective_checkpoint_sha256")
        is True
        and claim.get("required_effective_post_seal_semantics")
        == required_semantics,
        "C53 exact C50d final-claim and post-seal binding contract",
    )
    return {
        "claim_contract_object_sha256": observed,
        "predecessor_identity_sha256": identity_hash,
        "claim_basename": basename,
        "claim_path": expected_claim_path,
        "authority_seal_target_path": expected_seal_path,
        "C50d_protocol_file_sha256": C50D_PROTOCOL_FILE_SHA256,
        "predecessor_keyed": True,
        "forks_forbidden": True,
    }


def validate_candidate(
    raw: bytes, source_raw: bytes, route: dict[str, Any],
    mapping_summary: dict[str, Any],
) -> tuple[dict[str, Any], dict[str, Any], list[dict[str, Any]], dict[str, Any]]:
    candidate = strict_json(raw, "C53 candidate result")
    closed(candidate, "object_sha256", C53_RESULT_OBJECT_SHA256,
           "C53 candidate")
    source = candidate.get("source", {})
    need(
        candidate.get("schema") == CANDIDATE_SCHEMA
        and candidate.get("status")
        == "PASS_C53_PAIR1_ATOMIC_PAIR_LEVEL_SUCCESSOR_CANDIDATE__NO_REPLACE_SEAL_PENDING__ZERO_D02_GATE_CREDIT"
        and candidate.get("formal_credit") == 0
        and source.get("path")
        == "deliverables/cm2_round306c53_d02a_pair1_pair_level_successor_candidate_v1.py"
        and source.get("sha256") == C53_SOURCE_SHA256
        and file_digest(source_raw) == C53_SOURCE_SHA256,
        "C53 candidate source/status exact binding",
    )
    plan = candidate.get("C46_plan_public")
    genesis = candidate.get("C46_shard9_genesis")
    need(type(plan) is dict and type(genesis) is dict,
         "C53 complete inert C46 plan/genesis data")
    _shard9, genesis_states, plan_summary = validate_plan_and_genesis(plan, genesis)
    proof = candidate.get("global_pair_membership_proof")
    need(type(proof) is dict, "C53 global pair membership proof")
    validate_membership_proof(proof, plan, genesis_states)

    expected_map = expected_mapping_proof(mapping_summary)
    mapping = candidate.get("C51_C50a_per_occurrence_mapping_proof")
    need(mapping == expected_map, "C53 mapping proof exact independent replay")

    successor = candidate.get("successor")
    need(type(successor) is dict, "C53 successor checkpoint object")
    successor_summary = validate_successor_checkpoint(
        successor, genesis_states, route, expected_map
    )

    transaction = candidate.get("pair_transaction")
    need(type(transaction) is dict, "C53 pair transaction")
    closed(transaction, "pair_transaction_object_sha256",
           C53_TRANSACTION_OBJECT_SHA256, "C53 pair transaction")
    need(
        transaction.get("schema") == CANDIDATE_SCHEMA + ".atomic-pair-transaction"
        and transaction.get("pair_index") == PAIR
        and transaction.get("shard_index") == SHARD_INDEX
        and transaction.get("task_indices") == [0, 1]
        and transaction.get("task_binding_sha256s") == TASK_BINDINGS
        and transaction.get("local_predecessor_checkpoint_object_sha256")
        == GENESIS_CHECKPOINT_OBJECT_SHA256
        and transaction.get("global_predecessor_authority_seal_object_sha256")
        == C48_SEAL_OBJECT_SHA256
        and transaction.get("global_predecessor_successor_checkpoint_object_sha256")
        == C48_SUCCESSOR_OBJECT_SHA256
        and transaction.get("successor_checkpoint_object_sha256")
        == C53_SUCCESSOR_OBJECT_SHA256
        and transaction.get("C51_route_object_sha256") == C51_OBJECT_SHA256
        and transaction.get("C50a_owner_candidate_object_sha256")
        == C50A_RESULT_OBJECT_SHA256
        and transaction.get("C50a_owner_audit_object_sha256")
        == C50A_AUDIT_OBJECT_SHA256
        and transaction.get("C52_cold_route_audit_object_sha256")
        == C52_AUDIT_OBJECT_SHA256
        and transaction.get("atomicity") == {
            "both_tasks_or_neither": True,
            "single_pair_level_seal_required": True,
            "task_level_partial_credit_forbidden": True,
            "seal_is_only_semantic_commit": True,
        }
        and transaction.get("zero_credit_candidate_authority_effect") == {
            "before": BEFORE,
            "after": BEFORE,
            "C50d_before_census": C50D_BEFORE,
            "complete_D02_formal_census_before": D02_FORMAL_BEFORE,
            "task_formal_closed_count": 0,
            "whole_parent_credit": 0,
            "D02_gate_credit": 0,
        },
        "C53 exact atomic zero-credit transaction",
    )
    prospective = transaction.get("prospective_post_audit_and_seal_promotion")
    need(
        prospective == {
            "before": BEFORE,
            "after": AFTER,
            "C50d_before_census": C50D_BEFORE,
            "C50d_after_census": C50D_AFTER,
            "complete_D02_formal_census_before": D02_FORMAL_BEFORE,
            "complete_D02_formal_census_after": D02_FORMAL_AFTER,
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
        }
        and transaction.get("formal_credit_before_seal") == 0,
        "C53 prospective promotion is explicitly unauthoritative",
    )

    predecessors = candidate.get("predecessors", {})
    need(
        predecessors.get("formal_C42_authority", {}).get("seal_file_sha256")
        == C42_SEAL_FILE_SHA256
        and predecessors.get("formal_C42_authority", {}).get("seal_object_sha256")
        == C42_SEAL_OBJECT_SHA256
        and predecessors.get("formal_C42_authority", {}).get(
            "formal_census_after_commit"
        ) == {
            "paired_coarse_cells": 574,
            "remaining_representatives": 575,
            "unresolved": 1_150,
            "whole_representatives": 287,
        }
        and predecessors.get("logical_C48_authority", {}).get("seal_file_sha256")
        == C48_SEAL_FILE_SHA256
        and predecessors.get("logical_C48_authority", {}).get("seal_object_sha256")
        == C48_SEAL_OBJECT_SHA256
        and predecessors.get("logical_C48_authority", {}).get(
            "successor_checkpoint_object_sha256"
        ) == C48_SUCCESSOR_OBJECT_SHA256,
        "C53 exact C42 formal plus C48 logical predecessors",
    )
    evidence = candidate.get("evidence_bindings", {})
    need(
        evidence.get("C51", {}).get("object_sha256") == C51_OBJECT_SHA256
        and evidence.get("C50a", {}).get("full_result_object_sha256")
        == C50A_RESULT_OBJECT_SHA256
        and evidence.get("C50a", {}).get("full_audit_object_sha256")
        == C50A_AUDIT_OBJECT_SHA256
        and evidence.get("C50a", {}).get("request_object_sha256")
        == C50A_REQUEST_OBJECT_SHA256
        and evidence.get("C52", {}).get("audit_object_sha256")
        == C52_AUDIT_OBJECT_SHA256
        and evidence.get("C52", {}).get("audit_file_sha256")
        == C52_AUDIT_FILE_SHA256,
        "C53 exact evidence bindings",
    )
    selection = candidate.get("selection", {})
    need(selection == {
        "pair_index": PAIR,
        "task_count": 2,
        "task_indices": [0, 1],
        "task_binding_sha256s": TASK_BINDINGS,
        "frontiers": FRONTIERS,
        "logical_leaf_count": 9,
        "physical_side_terminal_count": 18,
    }, "C53 exact pair1 selection")
    claim_summary = validate_claim_contract(candidate, transaction, successor)
    nonpromotion = candidate.get("strict_nonpromotion", {})
    need(
        nonpromotion.get("runtime_writes_performed") is False
        and nonpromotion.get("candidate_pointer_receipt_or_seal_created") is False
        and nonpromotion.get("canonical_or_prior_authority_modified") is False
        and nonpromotion.get("post_seal_promotion_derivation_minted") is False
        and nonpromotion.get("whole_parent_credit") == 0
        and nonpromotion.get("D02_gate_credit") == 0
        and nonpromotion.get("CM2") == "NO-GO_FOR_CLAIM"
        and nonpromotion.get("formal_credit") == 0,
        "C53 strict candidate nonpromotion",
    )
    return candidate, {
        **plan_summary,
        **successor_summary,
        **claim_summary,
    }, genesis_states, expected_map


def build_promotion_derivation(
    candidate: dict[str, Any], c42_rows: list[dict[str, Any]],
    claim_summary: dict[str, Any],
) -> dict[str, Any]:
    successor = candidate["successor"]
    states = successor["task_states"]
    state_projections = []
    for index, state in enumerate(states):
        selected = index in {0, 1}
        body = {
            "schema": PROMOTION_SCHEMA + ".shard9-state-projection",
            "task_index": index,
            "task_binding_sha256": state["task_binding_sha256"],
            "pair_index": state["pair_index"],
            "pre_seal_state_sha256": digest(state),
            "candidate_selected_for_atomic_pair_promotion": selected,
            "post_seal_formal_closed": selected,
            "individual_task_credit_lock_after_seal": ZERO_LOCK,
            "individual_task_whole_parent_credit": 0,
            "pair_aggregate_credit_consumed_only_once": selected,
            "D02_gate_credit": 0,
        }
        state_projections.append(close_object(body, "projection_object_sha256"))
    need(sum(row["post_seal_formal_closed"] for row in state_projections) == 2,
         "promotion exactly two formally closed task projections")

    pair_projections = []
    for row in c42_rows:
        pair = row["pair_index"]
        before_whole = row["C34_common_refinement_credit"] == 2
        after_whole = before_whole or pair == PAIR
        body = {
            "schema": PROMOTION_SCHEMA + ".862-parent-projection",
            "pair_index": pair,
            "C42_parent_row_sha256": row["row_sha256"],
            "before_whole_representative": before_whole,
            "after_whole_representative": after_whole,
            "before_paired_coarse_credit": row["C34_common_refinement_credit"],
            "after_paired_coarse_credit": 2 if after_whole else 0,
            "before_unresolved_parent_volume": row["unresolved_parent_volume"],
            "after_unresolved_parent_volume": (
                "0" if pair == PAIR else row["unresolved_parent_volume"]
            ),
            "before_terminal_excluded_parent_volume": row[
                "terminal_excluded_parent_volume"
            ],
            "after_terminal_excluded_parent_volume": (
                "1" if pair == PAIR else row["terminal_excluded_parent_volume"]
            ),
            "before_leaf_count": row["leaf_count"],
            "after_leaf_count": 81 if pair == PAIR else row["leaf_count"],
            "before_terminal_leaf_count": row["terminal_leaf_count"],
            "after_terminal_leaf_count": (
                81 if pair == PAIR else row["terminal_leaf_count"]
            ),
            "before_nonterminal_leaf_count": row["nonterminal_leaf_count"],
            "after_nonterminal_leaf_count": (
                0 if pair == PAIR else row["nonterminal_leaf_count"]
            ),
            "newly_whole_by_C53_pair_seal": pair == PAIR,
            "D02_gate_credit": 0,
        }
        pair_projections.append(close_object(body, "projection_object_sha256"))
    need(len(pair_projections) == PAIR_COUNT,
         "promotion exact 862 parent projections")
    whole_before = sum(row["before_whole_representative"] for row in pair_projections)
    whole_after = sum(row["after_whole_representative"] for row in pair_projections)
    paired_before = sum(row["before_paired_coarse_credit"] for row in pair_projections)
    paired_after = sum(row["after_paired_coarse_credit"] for row in pair_projections)
    need((whole_before, whole_after, paired_before, paired_after)
         == (287, 288, 574, 576), "promotion exact whole/paired census")
    pair1_projection = pair_projections[PAIR]
    need(
        pair1_projection["before_unresolved_parent_volume"] == "1/256"
        and pair1_projection["after_unresolved_parent_volume"] == "0"
        and pair1_projection["before_nonterminal_leaf_count"] == 2
        and pair1_projection["after_nonterminal_leaf_count"] == 0
        and pair1_projection["before_leaf_count"] == 74
        and pair1_projection["after_leaf_count"] == 81
        and pair1_projection["newly_whole_by_C53_pair_seal"] is True,
        "promotion pair1 consumes two residual leaves into nine terminal leaves",
    )
    effective_checkpoint = close_object({
        "schema": PROMOTION_SCHEMA + ".effective-shard9-checkpoint",
        "candidate_zero_lock_checkpoint_object_sha256": successor[
            "successor_checkpoint_object_sha256"
        ],
        "local_genesis_checkpoint_object_sha256":
            GENESIS_CHECKPOINT_OBJECT_SHA256,
        "global_predecessor_authority_seal_object_sha256":
            C48_SEAL_OBJECT_SHA256,
        "task_count": SHARD_TASK_COUNT,
        "selected_pair_index": PAIR,
        "selected_task_indices": [0, 1],
        "formal_closed_task_count": 2,
        "pending_task_count": 587,
        "ordered_effective_state_projection_sequence_sha256": sequence_digest(
            row["projection_object_sha256"] for row in state_projections
        ),
        "pair_aggregate_whole_parent_credit": 1,
        "individual_task_whole_parent_credit_sum": 0,
        "D02_gate_credit": 0,
        "effective_only_if_installer_seal_binds_promotion": True,
    }, "effective_checkpoint_object_sha256")
    need(effective_checkpoint["effective_checkpoint_object_sha256"]
         != successor["successor_checkpoint_object_sha256"],
         "effective post-seal checkpoint differs from zero-lock candidate")
    body = {
        "schema": PROMOTION_SCHEMA,
        "status": (
            "PASS_INDEPENDENT_C53_PAIR1_PROSPECTIVE_POST_SEAL_PROMOTION_"
            "DERIVATION__NOT_AUTHORITY_UNTIL_INSTALLER_SEAL"
        ),
        "candidate_object_sha256": candidate["object_sha256"],
        "pair_transaction_object_sha256": candidate["pair_transaction"][
            "pair_transaction_object_sha256"
        ],
        "successor_checkpoint_object_sha256": successor[
            "successor_checkpoint_object_sha256"
        ],
        "C42_formal_authority_seal_object_sha256": C42_SEAL_OBJECT_SHA256,
        "C48_logical_predecessor_authority_seal_object_sha256":
            C48_SEAL_OBJECT_SHA256,
        "global_predecessor_claim_contract": claim_summary,
        "source_candidate_checkpoint_remains_immutable_zero_credit": True,
        "seal_applies_separate_formal_overlay_not_checkpoint_mutation": True,
        "effective_post_seal_checkpoint": effective_checkpoint,
        "shard9_state_projection_count": SHARD_TASK_COUNT,
        "selected_task_formal_closed_count_after_seal": 2,
        "unchanged_nonselected_task_count": 587,
        "post_seal_state_projection_sequence_sha256": sequence_digest(
            row["projection_object_sha256"] for row in state_projections
        ),
        "state_projections": state_projections,
        "parent_projection_count": PAIR_COUNT,
        "post_seal_862_parent_projection_sequence_sha256": sequence_digest(
            row["projection_object_sha256"] for row in pair_projections
        ),
        "parent_projections": pair_projections,
        "pair_level_credit_transition": {
            "before": {
                "formal_closed_task_count": 0,
                "whole_parent_credit": 0,
                "D02_gate_credit": 0,
            },
            "after_if_and_only_if_bound_seal_commits": {
                "formal_closed_task_count": 2,
                "whole_parent_credit": 1,
                "D02_gate_credit": 0,
            },
            "individual_task_whole_parent_credit_sum": 0,
            "single_pair_aggregate_prevents_double_credit": True,
        },
        "global_census_transition": {
            "before": BEFORE,
            "after": AFTER,
            "whole_representatives_before": 287,
            "whole_representatives_after": 288,
            "pair_count": PAIR_COUNT,
            "paired_plus_unresolved_constant": 1_724,
        },
        "D02_four_class_census_transition": {
            "before": {
                "EARLIEST_PREFIX_EXCLUDED": 75_386,
                "TYPED_EVENT_GRAPH": 296,
                "CONNECTED_TO_KNOWN": 0,
                "SOURCE_GRAZING_OR_CEMETERY": 0,
                "UNRESOLVED_R1648_CONTINUATION": 1_150,
                "total": 76_832,
            },
            "after_if_and_only_if_bound_seal_commits": {
                "EARLIEST_PREFIX_EXCLUDED": 75_388,
                "TYPED_EVENT_GRAPH": 296,
                "CONNECTED_TO_KNOWN": 0,
                "SOURCE_GRAZING_OR_CEMETERY": 0,
                "UNRESOLVED_R1648_CONTINUATION": 1_148,
                "total": 76_832,
            },
            "pair1_two_reflected_coarse_cells_classification":
                "STRICT_EXCLUDED",
            "class_total_conserved": True,
        },
        "installer_seal_requirements": {
            "must_bind_this_promotion_derivation_object_sha256": True,
            "must_bind_independent_audit_object_sha256": True,
            "must_commit_predecessor_keyed_global_claim": True,
            "seal_is_only_semantic_commit": True,
            "claim_without_seal_is_reservation_only": True,
        },
        "D02_gate_credit": 0,
        "formal_credit_before_installer_seal": 0,
    }
    return close_object(body, "promotion_derivation_object_sha256")


def validate_promotion_derivation(
    value: dict[str, Any], candidate: dict[str, Any],
    c42_rows: list[dict[str, Any]], claim_summary: dict[str, Any],
) -> None:
    expected = build_promotion_derivation(candidate, c42_rows, claim_summary)
    need(value == expected, "promotion derivation exact independent reconstruction")
    need(object_digest(value, "promotion_derivation_object_sha256")
         == value["promotion_derivation_object_sha256"],
         "promotion derivation self-hash")


def reclose_promotion(value: dict[str, Any], *, refresh_sequences: bool = True) -> None:
    for collection in ("state_projections", "parent_projections"):
        for row in value[collection]:
            row.pop("projection_object_sha256", None)
            row["projection_object_sha256"] = digest(row)
    if refresh_sequences:
        value["post_seal_state_projection_sequence_sha256"] = sequence_digest(
            row["projection_object_sha256"] for row in value["state_projections"]
        )
        value["post_seal_862_parent_projection_sequence_sha256"] = sequence_digest(
            row["projection_object_sha256"] for row in value["parent_projections"]
        )
    effective = value["effective_post_seal_checkpoint"]
    effective.pop("effective_checkpoint_object_sha256", None)
    effective["effective_checkpoint_object_sha256"] = digest(effective)
    value.pop("promotion_derivation_object_sha256", None)
    value["promotion_derivation_object_sha256"] = digest(value)


def coherent_promotion_attacks(
    baseline: dict[str, Any], candidate: dict[str, Any],
    c42_rows: list[dict[str, Any]], claim_summary: dict[str, Any],
) -> list[dict[str, Any]]:
    attacks: list[tuple[str, Callable[[dict[str, Any]], None], bool]] = [
        ("after_paired_plus_one", lambda x: x["global_census_transition"]["after"].__setitem__("paired_coarse_cells", 577), True),
        ("after_unresolved_plus_one", lambda x: x["global_census_transition"]["after"].__setitem__("unresolved_coarse_cells", 1149), True),
        ("after_remaining_plus_one", lambda x: x["global_census_transition"]["after"].__setitem__("representative_parents_remaining", 575), True),
        ("after_logical_skip", lambda x: x["global_census_transition"]["after"].__setitem__("logical_pending_task_count", 33637), True),
        ("after_physical_skip", lambda x: x["global_census_transition"]["after"].__setitem__("two_side_pending_occurrence_count", 67274), True),
        ("whole_credit_zero", lambda x: x["pair_level_credit_transition"]["after_if_and_only_if_bound_seal_commits"].__setitem__("whole_parent_credit", 0), True),
        ("D02_credit_one", lambda x: x["pair_level_credit_transition"]["after_if_and_only_if_bound_seal_commits"].__setitem__("D02_gate_credit", 1), True),
        ("formal_task_count_one", lambda x: x["pair_level_credit_transition"]["after_if_and_only_if_bound_seal_commits"].__setitem__("formal_closed_task_count", 1), True),
        ("selected_state_not_formal", lambda x: x["state_projections"][0].__setitem__("post_seal_formal_closed", False), True),
        ("individual_task_credit_one", lambda x: x["state_projections"][0].__setitem__("individual_task_whole_parent_credit", 1), True),
        ("unchanged_state_promoted", lambda x: x["state_projections"][2].__setitem__("post_seal_formal_closed", True), True),
        ("state_binding_swapped", lambda x: x["state_projections"][0].__setitem__("task_binding_sha256", TASK_BINDINGS[1]), True),
        ("pair1_after_credit_zero", lambda x: x["parent_projections"][PAIR].__setitem__("after_paired_coarse_credit", 0), True),
        ("pair1_not_whole", lambda x: x["parent_projections"][PAIR].__setitem__("after_whole_representative", False), True),
        ("pair1_unresolved_retained", lambda x: x["parent_projections"][PAIR].__setitem__("after_unresolved_parent_volume", "1/256"), True),
        ("pair1_leaf_count_80", lambda x: x["parent_projections"][PAIR].__setitem__("after_leaf_count", 80), True),
        ("other_pair_mutated", lambda x: x["parent_projections"][2].__setitem__("newly_whole_by_C53_pair_seal", True), True),
        ("candidate_hash_changed", lambda x: x.__setitem__("candidate_object_sha256", "0" * 64), True),
        ("transaction_hash_changed", lambda x: x.__setitem__("pair_transaction_object_sha256", "0" * 64), True),
        ("C42_predecessor_changed", lambda x: x.__setitem__("C42_formal_authority_seal_object_sha256", "0" * 64), True),
        ("C48_predecessor_changed", lambda x: x.__setitem__("C48_logical_predecessor_authority_seal_object_sha256", "0" * 64), True),
        ("claim_basename_changed", lambda x: x["global_predecessor_claim_contract"].__setitem__("claim_basename", "fork"), True),
        ("seal_binding_removed", lambda x: x["installer_seal_requirements"].__setitem__("must_bind_this_promotion_derivation_object_sha256", False), True),
        ("state_sequence_forged", lambda x: x.__setitem__("post_seal_state_projection_sequence_sha256", "0" * 64), False),
        ("four_class_exclusion_off_by_one", lambda x: x["D02_four_class_census_transition"]["after_if_and_only_if_bound_seal_commits"].__setitem__("EARLIEST_PREFIX_EXCLUDED", 75387), True),
        ("four_class_unresolved_not_reduced", lambda x: x["D02_four_class_census_transition"]["after_if_and_only_if_bound_seal_commits"].__setitem__("UNRESOLVED_R1648_CONTINUATION", 1150), True),
        ("four_class_typed_changed", lambda x: x["D02_four_class_census_transition"]["after_if_and_only_if_bound_seal_commits"].__setitem__("TYPED_EVENT_GRAPH", 297), True),
        ("effective_checkpoint_formal_count_one", lambda x: x["effective_post_seal_checkpoint"].__setitem__("formal_closed_task_count", 1), True),
    ]
    output = []
    for label, mutate, refresh in attacks:
        value = copy.deepcopy(baseline)
        mutate(value)
        reclose_promotion(value, refresh_sequences=refresh)
        rejected = False
        reason = ""
        try:
            validate_promotion_derivation(value, candidate, c42_rows, claim_summary)
        except Reject as error:
            rejected = True
            reason = str(error)
        need(rejected, "coherent attack must fail closed:" + label)
        output.append({
            "attack": label,
            "nested_projection_hashes_reclosed": True,
            "top_promotion_hash_reclosed": True,
            "fail_closed": True,
            "rejection_sha256": hashlib.sha256(reason.encode("utf-8")).hexdigest(),
        })
    need(len(output) == 28 and len({row["attack"] for row in output}) == 28,
         "28 unique coherent promotion attacks")
    return output


class Inputs:
    def __init__(self, expected_verifier_sha256: str):
        need(pins_frozen(), "C52/C53 terminal pins frozen")
        need(HEX64.fullmatch(expected_verifier_sha256) is not None,
             "external verifier source pin")
        specs = {
            "verifier_source": (SELF, expected_verifier_sha256, 8 << 20),
            "C46_source_inert": (C46_SOURCE, C46_SOURCE_SHA256, 8 << 20),
            "C42_seal": (C42_SEAL, C42_SEAL_FILE_SHA256, 4 << 20),
            "C42_result": (C42_RESULT, C42_RESULT_FILE_SHA256, 8 << 20),
            "C42_parent": (C42_PARENT, C42_PARENT_FILE_SHA256, 32 << 20),
            "C48_seal": (C48_SEAL, C48_SEAL_FILE_SHA256, 4 << 20),
            "C48_receipt": (
                C48_RECEIPT, C48_RECEIPT_FILE_SHA256, 8 << 20,
            ),
            "C50d_protocol": (
                C50D_PROTOCOL, C50D_PROTOCOL_FILE_SHA256, 4 << 20,
            ),
            "C50d_protocol_companion": (
                C50D_PROTOCOL_COMPANION, C50D_PROTOCOL_COMPANION_SHA256,
                1 << 20,
            ),
            "C51_result": (C51_RESULT, C51_RESULT_FILE_SHA256, 64 << 20),
            "C50a_result_bundle": (
                C50A_FULL_RESULT, C50A_RESULT_ENCODED_SHA256, 1 << 30,
            ),
            "C50a_audit_bundle": (
                C50A_FULL_AUDIT, C50A_AUDIT_ENCODED_SHA256, 1 << 30,
            ),
            "C52_source": (C52_SOURCE, C52_SOURCE_SHA256, 8 << 20),
            "C52_audit": (C52_AUDIT, C52_AUDIT_FILE_SHA256, 128 << 20),
            "C53_source": (C53_SOURCE, C53_SOURCE_SHA256, 8 << 20),
            "C53_result": (C53_RESULT, C53_RESULT_FILE_SHA256, 1 << 30),
        }
        self.captures: dict[str, Capture] = {}
        try:
            for label, (path, expected, maximum) in specs.items():
                self.captures[label] = Capture(path, label, expected, maximum)
        except Exception:
            self.close()
            raise

    def raw(self, label: str) -> bytes:
        return self.captures[label].raw

    def attest_all(self, phase: str) -> None:
        for label in sorted(self.captures):
            self.captures[label].unchanged(phase)

    def close(self) -> None:
        for capture in reversed(list(getattr(self, "captures", {}).values())):
            capture.close()
        if hasattr(self, "captures"):
            self.captures.clear()


def verify(expected_verifier_sha256: str) -> dict[str, Any]:
    inputs = Inputs(expected_verifier_sha256)
    try:
        independence = source_independence(inputs.raw("verifier_source"))
        candidate_source_scan = scan_inert_candidate_source(inputs.raw("C53_source"))
        inputs.attest_all("after source independence scans")
        c42_seal, c42_result, c42_rows = validate_c42(
            inputs.raw("C42_seal"), inputs.raw("C42_result"),
            inputs.raw("C42_parent"),
        )
        need(
            inputs.raw("C50d_protocol_companion")
            == (C50D_PROTOCOL_FILE_SHA256 + "  " + C50D_PROTOCOL.name + "\n").encode("ascii"),
            "C50d protocol companion exact binding",
        )
        c48 = validate_c48(
            inputs.raw("C48_seal"), inputs.raw("C48_receipt")
        )
        route, route_bridge, leaf_sequences = validate_c51(
            inputs.raw("C51_result")
        )
        _owner, _owner_audit, mapping_summary = validate_c50a(
            inputs.raw("C50a_result_bundle"), inputs.raw("C50a_audit_bundle"),
            route_bridge,
        )
        _c52, c52_summary = validate_c52(
            inputs.raw("C52_audit"), route, leaf_sequences
        )
        candidate, candidate_summary, _genesis_states, _mapping = validate_candidate(
            inputs.raw("C53_result"), inputs.raw("C53_source"), route,
            mapping_summary,
        )
        claim_summary = {
            "claim_contract_object_sha256": candidate_summary[
                "claim_contract_object_sha256"
            ],
            "predecessor_identity_sha256": candidate_summary[
                "predecessor_identity_sha256"
            ],
            "claim_basename": candidate_summary["claim_basename"],
            "predecessor_keyed": True,
            "forks_forbidden": True,
        }
        promotion = build_promotion_derivation(
            candidate, c42_rows, claim_summary
        )
        validate_promotion_derivation(
            promotion, candidate, c42_rows, claim_summary
        )
        attacks = coherent_promotion_attacks(
            promotion, candidate, c42_rows, claim_summary
        )
        inputs.attest_all("terminal post-verification reread")
        body = {
            "schema": SCHEMA,
            "status": (
                "PASS_INDEPENDENT_C53_PAIR1_ATOMIC_TRANSACTION_589_STATE_"
                "862_CENSUS_AND_POST_SEAL_PROMOTION_AUDIT__ZERO_D02_GATE_CREDIT"
            ),
            "verifier": {
                "path": str(SELF.relative_to(ROOT)),
                "sha256": expected_verifier_sha256,
            },
            "candidate": {
                "path": str(C53_RESULT.relative_to(ROOT)),
                "file_sha256": C53_RESULT_FILE_SHA256,
                "object_sha256": C53_RESULT_OBJECT_SHA256,
                "source_sha256": C53_SOURCE_SHA256,
                "pair_transaction_object_sha256": C53_TRANSACTION_OBJECT_SHA256,
                "successor_checkpoint_object_sha256": C53_SUCCESSOR_OBJECT_SHA256,
            },
            "independence_boundary": {
                **independence,
                **candidate_source_scan,
                "C46_source_executed": False,
                "C42_C48_C51_C50a_C52_C53_consumed_as_data_only": True,
                "runtime_writes_performed": False,
            },
            "formal_predecessor": {
                "C42_authority_seal_object_sha256": c42_seal[
                    "authority_seal_object_sha256"
                ],
                "C42_candidate_object_sha256": c42_result["object_sha256"],
                "whole_representatives": 287,
                "paired_coarse_cells": 574,
                "unresolved_coarse_cells": 1_150,
                "parent_row_count": 862,
            },
            "logical_predecessor": {
                "C48_authority_seal_object_sha256": c48[
                    "authority_seal_object_sha256"
                ],
                "successor_checkpoint_object_sha256":
                    C48_SUCCESSOR_OBJECT_SHA256,
                "whole_parent_credit": 0,
                "D02_gate_credit": 0,
                "coarse_formal_authority_unchanged": True,
                "C48_receipt_file_sha256": C48_RECEIPT_FILE_SHA256,
                "C48_receipt_object_sha256": C48_RECEIPT_OBJECT_SHA256,
            },
            "global_CAS_protocol": {
                "path": str(C50D_PROTOCOL.relative_to(ROOT)),
                "file_sha256": C50D_PROTOCOL_FILE_SHA256,
                "companion_file_sha256": C50D_PROTOCOL_COMPANION_SHA256,
                "predecessor_identity": expected_predecessor_identity(),
            },
            "C46_and_successor_replay": candidate_summary,
            "per_occurrence_bridge": {
                **{key: value for key, value in mapping_summary.items()
                   if key != "candidate_mapping_rows"},
                "C52": c52_summary,
            },
            "post_seal_promotion_derivation": promotion,
            "coherent_attacks": attacks,
            "coherent_attack_count": 28,
            "all_coherent_attacks_fail_closed": True,
            "immutability": {
                "all_input_file_descriptors_held_across_verification": True,
                "pre_post_identity_and_byte_reread_equal": True,
            },
            "strict_nonpromotion": {
                "audit_is_not_authority": True,
                "promotion_derivation_is_prospective_until_bound_seal": True,
                "candidate_checkpoint_remains_zero_credit": True,
                "runtime_writes_performed": False,
                "pointer_claim_receipt_or_seal_created": False,
                "canonical_modified": False,
                "D02_gate_credit": 0,
                "CM2": "NO-GO_FOR_CLAIM",
                "formal_credit": 0,
            },
            "D02_gate_credit": 0,
            "formal_credit": 0,
        }
        return close_object(body, "object_sha256")
    finally:
        inputs.close()


def file_hash_readonly(path: Path, maximum: int) -> str:
    fd = os.open(path, os.O_RDONLY | os.O_NOFOLLOW | os.O_CLOEXEC)
    try:
        before = os.fstat(fd)
        need(stat.S_ISREG(before.st_mode) and 0 < before.st_size <= maximum,
             "preflight bounded regular:" + str(path))
        state = hashlib.sha256()
        total = 0
        while True:
            block = os.read(fd, 1 << 20)
            if not block:
                break
            total += len(block)
            need(total <= maximum, "preflight read bound:" + str(path))
            state.update(block)
        after = os.fstat(fd)
        key = lambda row: (
            row.st_dev, row.st_ino, row.st_mode, row.st_nlink, row.st_uid,
            row.st_gid, row.st_size, row.st_mtime_ns, row.st_ctime_ns,
        )
        need(key(before) == key(after), "preflight stable file:" + str(path))
        return state.hexdigest()
    finally:
        os.close(fd)


def preflight(expected_verifier_sha256: str | None) -> dict[str, Any]:
    checks: dict[str, bool] = {}
    blockers: list[str] = []
    specs = {
        "C46_source_inert": (C46_SOURCE, C46_SOURCE_SHA256, 8 << 20),
        "C42_seal": (C42_SEAL, C42_SEAL_FILE_SHA256, 4 << 20),
        "C42_result": (C42_RESULT, C42_RESULT_FILE_SHA256, 8 << 20),
        "C42_parent_862": (C42_PARENT, C42_PARENT_FILE_SHA256, 32 << 20),
        "C48_seal": (C48_SEAL, C48_SEAL_FILE_SHA256, 4 << 20),
        "C48_receipt": (C48_RECEIPT, C48_RECEIPT_FILE_SHA256, 8 << 20),
        "C50d_protocol": (C50D_PROTOCOL, C50D_PROTOCOL_FILE_SHA256, 4 << 20),
        "C50d_protocol_companion": (
            C50D_PROTOCOL_COMPANION, C50D_PROTOCOL_COMPANION_SHA256, 1 << 20,
        ),
        "C51_frozen_result": (C51_RESULT, C51_RESULT_FILE_SHA256, 64 << 20),
        "C50a_full_result": (
            C50A_FULL_RESULT, C50A_RESULT_ENCODED_SHA256, 1 << 30,
        ),
        "C50a_full_audit": (
            C50A_FULL_AUDIT, C50A_AUDIT_ENCODED_SHA256, 1 << 30,
        ),
        "C52_source": (C52_SOURCE, C52_SOURCE_SHA256, 8 << 20),
        "C52_audit": (C52_AUDIT, C52_AUDIT_FILE_SHA256, 128 << 20),
        "C53_source": (C53_SOURCE, C53_SOURCE_SHA256, 8 << 20),
        "C53_result": (C53_RESULT, C53_RESULT_FILE_SHA256, 1 << 30),
    }
    if expected_verifier_sha256 is None or HEX64.fullmatch(
        expected_verifier_sha256
    ) is None:
        checks["verifier_external_source_pin"] = False
        blockers.append("verifier_external_source_pin: --expect-verifier-sha256 required")
    else:
        try:
            observed = file_hash_readonly(SELF, 8 << 20)
            checks["verifier_external_source_pin"] = observed == expected_verifier_sha256
            if observed != expected_verifier_sha256:
                blockers.append("verifier_external_source_pin: mismatch")
        except (Reject, OSError) as error:
            checks["verifier_external_source_pin"] = False
            blockers.append("verifier_external_source_pin:" + str(error))
    for label, (path, expected, maximum) in specs.items():
        if HEX64.fullmatch(expected) is None:
            checks[label] = False
            blockers.append(label + ": terminal pin not frozen")
            continue
        try:
            observed = file_hash_readonly(path, maximum)
            checks[label] = observed == expected
            if observed != expected:
                blockers.append(label + ": file SHA-256 mismatch")
        except (Reject, OSError) as error:
            checks[label] = False
            blockers.append(label + ":" + type(error).__name__ + ":" + str(error))
    checks["all_C52_C53_object_pins_frozen"] = pins_frozen()
    if not checks["all_C52_C53_object_pins_frozen"]:
        blockers.append("all_C52_C53_object_pins_frozen: final C53 pins outstanding")
    ready = bool(checks) and all(checks.values())
    body = {
        "schema": SCHEMA + ".preflight",
        "status": (
            "PASS_C53_INDEPENDENT_VERIFIER_PREFLIGHT__NO_WRITES"
            if ready else
            "BLOCKED_C53_INDEPENDENT_VERIFIER_FAIL_CLOSED__NO_WRITES_NO_CREDIT"
        ),
        "checks": checks,
        "blockers": blockers,
        "ready_to_verify": ready,
        "effective_authority_while_blocked": {
            "formal_C42": {"paired": 574, "unresolved": 1_150,
                           "remaining_representatives": 575},
            "logical_C48_zero_coarse_task_successor_count": 1,
            "C53_formal_credit": 0,
        },
        "runtime_writes_performed": False,
        "formal_credit": 0,
        "D02_gate_credit": 0,
    }
    return close_object(body, "preflight_object_sha256")


def self_test() -> dict[str, Any]:
    checks = {
        "frontier0_prefix_free_Kraft_one":
            prefix_free(FRONTIERS[0]) and kraft(FRONTIERS[0]) == 1,
        "frontier1_prefix_free_Kraft_one":
            prefix_free(FRONTIERS[1]) and kraft(FRONTIERS[1]) == 1,
        "nine_logical_eighteen_physical":
            sum(map(len, FRONTIERS)) == 9 and 2 * sum(map(len, FRONTIERS)) == 18,
        "logical_pending_delta_two":
            BEFORE["logical_pending_task_count"] - AFTER["logical_pending_task_count"] == 2,
        "physical_pending_delta_four":
            BEFORE["two_side_pending_occurrence_count"]
            - AFTER["two_side_pending_occurrence_count"] == 4,
        "paired_delta_two":
            AFTER["paired_coarse_cells"] - BEFORE["paired_coarse_cells"] == 2,
        "unresolved_delta_two":
            BEFORE["unresolved_coarse_cells"] - AFTER["unresolved_coarse_cells"] == 2,
        "representative_delta_one":
            BEFORE["representative_parents_remaining"]
            - AFTER["representative_parents_remaining"] == 1,
        "862_partition_before": 287 + 575 == 862,
        "862_partition_after": 288 + 574 == 862,
        "four_class_before_total": 75_386 + 296 + 0 + 0 + 1_150 == 76_832,
        "four_class_after_total": 75_388 + 296 + 0 + 0 + 1_148 == 76_832,
        "placeholder_rejected": HEX64.fullmatch(UNFROZEN) is None,
        "canonical_self_hash": False,
        "post_close_mutation_detected": False,
    }
    value = close_object({"schema": "selftest", "status": "PASS"}, "object_sha256")
    checks["canonical_self_hash"] = object_digest(value, "object_sha256") == value[
        "object_sha256"
    ]
    mutated = dict(value)
    mutated["status"] = "MUTATED"
    checks["post_close_mutation_detected"] = object_digest(
        mutated, "object_sha256"
    ) != mutated["object_sha256"]
    need(len(checks) == 15 and all(checks.values()), "pure self-test 15/15")
    body = {
        "schema": SCHEMA + ".self-test",
        "status": "PASS_C53_INDEPENDENT_VERIFIER_PURE_SELF_TEST_15_OF_15",
        "passed": 15,
        "total": 15,
        "checks": checks,
        "runtime_writes_performed": False,
        "formal_credit": 0,
    }
    return close_object(body, "object_sha256")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--self-test", action="store_true")
    mode.add_argument("--preflight", action="store_true")
    mode.add_argument("--verify", action="store_true")
    parser.add_argument("--expect-verifier-sha256")
    args = parser.parse_args(argv)
    try:
        if args.self_test:
            need(args.expect_verifier_sha256 is None,
                 "self-test takes no external source pin")
            result = self_test()
        elif args.preflight:
            result = preflight(args.expect_verifier_sha256)
        else:
            need(pins_frozen(), "verifier disarmed until terminal C52/C53 pins freeze")
            need(type(args.expect_verifier_sha256) is str
                 and HEX64.fullmatch(args.expect_verifier_sha256) is not None,
                 "--expect-verifier-sha256 required")
            result = verify(args.expect_verifier_sha256)
        sys.stdout.buffer.write(canonical(result) + b"\n")
        return 0
    except (Reject, OSError, ValueError, KeyError, TypeError, IndexError) as error:
        body = {
            "schema": SCHEMA + ".rejection",
            "status": "REJECT_C53_INDEPENDENT_PAIR1_TRANSACTION_AUDIT_FAIL_CLOSED",
            "error_class": type(error).__name__,
            "reason": str(error),
            "runtime_writes_performed": False,
            "pointer_claim_receipt_or_seal_created": False,
            "formal_credit": 0,
            "D02_gate_credit": 0,
        }
        sys.stdout.buffer.write(canonical(close_object(body, "object_sha256")) + b"\n")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
