#!/usr/bin/env python3
"""Regenerate the C79g successor source namespace from held source bytes.

The v16r2 source pass is deliberately separate from the JSON/static builder.
It reads the byte-pinned predecessor sources and the already frozen semantic
rejection chain, then writes three *new* source files with ``O_EXCL``.  No
predecessor file is opened for writing and this program never creates a
manifest, outer receipt, runtime surface, or credit.

There are two kinds of edits in this file:

* explicit AST fixed-span edits close the active path/transition/pin graph;
* a second token-span pass renames inherited namespace spellings.  The latter
  is intentionally performed on individual lexer spans (not on the complete
  source string), so a replacement cannot cross a string/comment boundary or
  silently rewrite an unrelated file.

The resulting files remain runtime-disabled and draft-pinned.  They are
source candidates for an independent reviewer, not an authority surface.
"""

from __future__ import annotations

import ast
import hashlib
import io
import json
import os
import re
import stat
import sys
import tokenize
from pathlib import Path
from typing import Any, Iterable

sys.dont_write_bytecode = True

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "deliverables"
RUNTIME = ROOT / ".cm2-runtime"
BASE = "cm2_round306c79g_true_global_no_producer_consumer"
# Every retry is a fresh append-only namespace.  r6 was emitted by an earlier
# run but failed its self-check; r7 is therefore the only namespace this
# invocation may create.
PREDECESSOR_TAG = "v16r2r8"
SUCCESSOR_TAG = "v16r2r9"
SUCCESSOR_SOURCE_SUFFIX = f"{SUCCESSOR_TAG}_semantic_source"
SUCCESSOR_NAMESPACE = f"{SUCCESSOR_TAG}_semantic_source"
_RETRY_NUMBER = int(SUCCESSOR_TAG.rsplit("r", 1)[1])
STATIC_TAG = f"v16r{_RETRY_NUMBER}"
PREVIOUS_STATIC_TAG = f"v16r{_RETRY_NUMBER - 1}"
SUCCESSOR_CHECKPOINT = (
    "dd9d64f3f0bd0dfd00fd399e3154517a34ba19cfb601ec749f44cbc08b03ca1b"
)
UPSTREAM_CHECKPOINT = (
    "b58d68a0234b8a7de0e9147f891d37910476d622b840cfa073aed7ff3b4382ab"
)

V15_SOURCES = {
    "producer": OUT / f"{BASE}_v15.py",
    "consumer": OUT / f"{BASE}_independent_verifier_assembler_authority_consumer_v15.py",
    "launcher": OUT / f"{BASE}_cold_launch_v15.py",
}
V15_SOURCE_SHA256 = {
    "producer": "7b3621bf6579cd9cc9289ed2bda353cbe5f2e32b108ec718bf80a4fd19af125b",
    "consumer": "5f988490d014a1427a773b7c5fda03318ec67ad9716a4a75b4008b007e944541",
    "launcher": "1ded892a514f21cb534d25a4ecf6cc0b82b97775371f7666d5d24f359d21e015",
}
V16_REJECTION = RUNTIME / (
    "c79g-v16-rejections-" + SUCCESSOR_CHECKPOINT
) / "rejection.json"
V16_SUPERSESSION = OUT / (
    f"{BASE}_v16_semantic_rejection_supersession_receipt_v1.json"
)

# The executable source namespace is deliberately distinct from the inert
# ``*_v16r2.py`` templates made by the static rebuilder.
TARGETS = {
    # r6 is retained as an immutable rejected namespace; this retry is
    # deliberately append-only and therefore uses a fresh name.
    "producer": OUT / f"{BASE}_{SUCCESSOR_SOURCE_SUFFIX}.py",
    "consumer": OUT / (
        f"{BASE}_independent_verifier_assembler_authority_consumer_"
        f"{SUCCESSOR_SOURCE_SUFFIX}.py"
    ),
    "launcher": OUT / f"{BASE}_cold_launch_{SUCCESSOR_SOURCE_SUFFIX}.py",
}
SCHEMA = OUT / f"{BASE}_schema_{STATIC_TAG}.json"
CONTRACT = OUT / f"{BASE}_contract_{STATIC_TAG}.json"
TRANSITION = OUT / (
    f"{BASE}_{PREVIOUS_STATIC_TAG}_to_{STATIC_TAG}_"
    "static_launch_transition_receipt_v1.json")
AUDIT = OUT / f"{BASE}_static_audit_{STATIC_TAG}.json"
SUPSERSESSION_RELATIVE = (
    f"deliverables/{BASE}_v16_semantic_rejection_supersession_receipt_v1.json"
)
SUPSERSESSION_NAME = V16_SUPERSESSION.name

PFILE = TARGETS["producer"].name
CFILE = TARGETS["consumer"].name
LFILE = TARGETS["launcher"].name
SCHEMA_NAME = SCHEMA.name
CONTRACT_NAME = CONTRACT.name
TRANSITION_NAME = TRANSITION.name
AUDIT_NAME = AUDIT.name
MANIFEST_NAME = f"{BASE}_cold_launch_manifest_{STATIC_TAG}.sha256"
OUTER_NAME = f"{BASE}_cold_launch_outer_receipt_{STATIC_TAG}.json"

# Immutable record of the first source namespace.  The first attempt was
# written with O_EXCL and then rejected by the in-memory parser; it is never
# overwritten or reused by this retry.
FIRST_REJECTION = OUT / (
    f"{BASE}_v16r2_semantic_source_rejection_receipt_v1.json"
)
FIRST_SUPERSESSION = OUT / (
    f"{BASE}_v16r2_to_v16r2r2_semantic_source_rejection_supersession_receipt_v1.json"
)
FIRST_FAILED_OUTPUTS = {
    "producer": {
        "path": f"deliverables/{BASE}_v16r2_semantic_source.py",
        "file_sha256": "7547ea4dec0d7754ba61faf9f3aa8e1831b2a31464b8b4d7847d057d3142a534",
        "bytes": 504600,
        "mode": "0664",
        "nlink": 1,
        "syntax_error": {
            "lineno": 134,
            "message": "cannot assign to expression here. Maybe you meant '==' instead of '='?",
        },
    },
    "consumer": {
        "path": f"deliverables/{BASE}_independent_verifier_assembler_authority_consumer_v16r2_semantic_source.py",
        "file_sha256": "6bbc6d9faf1c0165a20d1ead6876d77716572c20fca65c535b5b82fecbc258a4",
        "bytes": 797070,
        "mode": "0664",
        "nlink": 1,
        "syntax_error": {
            "lineno": 170,
            "message": "cannot assign to expression here. Maybe you meant '==' instead of '='?",
        },
    },
    "launcher": {
        "path": f"deliverables/{BASE}_cold_launch_v16r2_semantic_source.py",
        "file_sha256": "18b9346a9177951c1aae35000ddcbce6fc4d3b0198ae6d209db28cdd6131660e",
        "bytes": 473837,
        "mode": "0664",
        "nlink": 1,
        "syntax_error": None,
    },
}
SECOND_REJECTION = OUT / (
    f"{BASE}_v16r2r2_semantic_source_rejection_receipt_v1.json"
)
SECOND_SUPERSESSION = OUT / (
    f"{BASE}_v16r2r2_to_v16r2r3_semantic_source_rejection_supersession_receipt_v1.json"
)
SECOND_FAILED_OUTPUTS = {
    "producer": {
        "path": f"deliverables/{BASE}_v16r2r2_semantic_source.py",
        "file_sha256": "c3b95e56bce39a5f4174c781c52e53783ae1063ef813b842a8d66f4979e915ee",
        "bytes": 504777,
        "mode": "0664",
        "nlink": 1,
        "syntax_error": {
            "lineno": 890,
            "message": "annotated name 'EXACT8' can't be global",
        },
    },
    "consumer": {
        "path": f"deliverables/{BASE}_independent_verifier_assembler_authority_consumer_v16r2r2_semantic_source.py",
        "file_sha256": "38fd2dfcc48cc7f585e38a6837b9b0d7dd70bd90fb15e5c0f19f432f52e5f2be",
        "bytes": 797245,
        "mode": "0664",
        "nlink": 1,
        "syntax_error": None,
    },
    "launcher": {
        "path": f"deliverables/{BASE}_cold_launch_v16r2r2_semantic_source.py",
        "file_sha256": "24bb3a58913859dfbf28a117a32a5cd3a80016940855154f006ca1dc858ceee8",
        "bytes": 474024,
        "mode": "0664",
        "nlink": 1,
        "syntax_error": None,
    },
}
THIRD_REJECTION = OUT / (
    f"{BASE}_v16r2r3_semantic_source_rejection_receipt_v1.json"
)
THIRD_SUPERSESSION = OUT / (
    f"{BASE}_v16r2r3_to_v16r2r4_semantic_source_rejection_supersession_receipt_v1.json"
)
THIRD_FAILED_OUTPUTS = {
    "producer": {
        "path": f"deliverables/{BASE}_v16r2r3_semantic_source.py",
        "file_sha256": "dfa7480ef80cf5797f8018df5e7afa79e89894dc5bfd9257c7273db5cdd48106",
        "bytes": 504779,
        "mode": "0664",
        "nlink": 1,
        "syntax_error": None,
        "semantic_error": "uppercase active transition identifier was lowercased by token span rewrite",
    },
    "consumer": {
        "path": f"deliverables/{BASE}_independent_verifier_assembler_authority_consumer_v16r2r3_semantic_source.py",
        "file_sha256": "1046eaaa5a85b76455533fcebdd6dd912a256f050d7625c4d45e2fe535b4ab2e",
        "bytes": 797247,
        "mode": "0664",
        "nlink": 1,
        "syntax_error": None,
        "semantic_error": "uppercase active transition identifier was lowercased by token span rewrite",
    },
    "launcher": {
        "path": f"deliverables/{BASE}_cold_launch_v16r2r3_semantic_source.py",
        "file_sha256": "10c25993a2e3feb2f381accfa7d72461cab8a16fd1c1c4268785547ed514ce80",
        "bytes": 474008,
        "mode": "0664",
        "nlink": 1,
        "syntax_error": None,
        "semantic_error": "duplicate MANIFEST/OUTER assignment and successor namespace alias remained active",
    },
}
FOURTH_REJECTION = OUT / (
    f"{BASE}_v16r2r4_semantic_source_rejection_receipt_v1.json"
)
FOURTH_SUPERSESSION = OUT / (
    f"{BASE}_v16r2r4_to_v16r2r5_semantic_source_rejection_supersession_receipt_v1.json"
)
FOURTH_FAILED_OUTPUTS = {
    "producer": {
        "path": f"deliverables/{BASE}_v16r2r4_semantic_source.py",
        "file_sha256": "5f05866741b79d1f70471beec0892f3a608206fcb35d1ae296275d953c3b46a8",
        "bytes": 504781,
        "mode": "0664",
        "nlink": 1,
        "syntax_error": None,
        "semantic_error": "launcher import-time manifest/outer chain was not removed",
    },
    "consumer": {
        "path": f"deliverables/{BASE}_independent_verifier_assembler_authority_consumer_v16r2r4_semantic_source.py",
        "file_sha256": "29434720fcd8e26b72e38ea575e7c03e6a7eb0b6d2be19db8494fdcfaff34127",
        "bytes": 797249,
        "mode": "0664",
        "nlink": 1,
        "syntax_error": None,
        "semantic_error": "launcher import-time manifest/outer chain was not removed",
    },
    "launcher": {
        "path": f"deliverables/{BASE}_cold_launch_v16r2r4_semantic_source.py",
        "file_sha256": "a1dbeac9174055567f464aeb10ec7ed566b14c3018385c873a1a8bb06f004377",
        "bytes": 473975,
        "mode": "0664",
        "nlink": 1,
        "syntax_error": None,
        "semantic_error": "launcher import-time manifest/outer chain was not removed",
    },
}
FIFTH_REJECTION = OUT / (
    f"{BASE}_v16r2r5_semantic_source_rejection_receipt_v1.json"
)
FIFTH_SUPERSESSION = OUT / (
    f"{BASE}_v16r2r5_to_v16r2r6_semantic_source_rejection_supersession_receipt_v1.json"
)
FIFTH_FAILED_OUTPUTS = {
    "producer": {
        "path": f"deliverables/{BASE}_v16r2r5_semantic_source.py",
        "file_sha256": "b875277221f2f1257ac9b82227bb547d77b1c8c7cccf40e34773d2a4cf584720",
        "bytes": 504781,
        "mode": "0664",
        "nlink": 1,
        "syntax_error": None,
        "semantic_error": "active predecessor anchor and upstream checkpoint were not explicit",
    },
    "consumer": {
        "path": f"deliverables/{BASE}_independent_verifier_assembler_authority_consumer_v16r2r5_semantic_source.py",
        "file_sha256": "775e25c9e3bd552a8d67e067cccb986635fa568dcdffdd79b09696d58cb1f68d",
        "bytes": 797249,
        "mode": "0664",
        "nlink": 1,
        "syntax_error": None,
        "semantic_error": "active predecessor anchor and upstream checkpoint were not explicit",
    },
    "launcher": {
        "path": f"deliverables/{BASE}_cold_launch_v16r2r5_semantic_source.py",
        "file_sha256": "3abfce74e684e7e51f809991398f40c67929eef131f3ef49ab1a4631b69ce65d",
        "bytes": 474157,
        "mode": "0664",
        "nlink": 1,
        "syntax_error": None,
        "semantic_error": "active predecessor anchor and upstream checkpoint were not explicit",
    },
}
ACTIVE_ANCHOR_RECEIPT = OUT / (
    f"{BASE}_{SUCCESSOR_TAG}_active_predecessor_supersession_receipt_v1.json"
)
# The newest frozen retry supersession is exposed in the generated source as
# the immediate predecessor anchor.  The original v16 semantic supersession
# remains historical input only (never an active exact8 member).
PRIOR_SUPERSESSION = None  # populated after the r6 rejection is sealed

# r6 was installed with O_EXCL and then failed the source self-check.  These
# observed bytes are immutable evidence and are sealed before r7 generation.
SIXTH_REJECTION = OUT / (
    f"{BASE}_v16r2r6_semantic_source_rejection_receipt_v1.json"
)
SIXTH_SUPERSESSION = OUT / (
    f"{BASE}_v16r2r6_to_v16r2r7_semantic_source_rejection_supersession_receipt_v1.json"
)
SIXTH_FAILED_OUTPUTS = {
    "producer": {
        "path": f"deliverables/{BASE}_v16r2r6_semantic_source.py",
        "file_sha256": "5432311a28f3b92d71c68fdaf9e776fb59cab6ce065bd6ab0e8b658ebd11af6d",
        "bytes": 504972,
        "mode": "0664",
        "nlink": 1,
        "syntax_error": None,
        "semantic_error": "historical v16 supersession anchor was not retained and BASE remained predecessor r5",
    },
    "consumer": {
        "path": f"deliverables/{BASE}_independent_verifier_assembler_authority_consumer_v16r2r6_semantic_source.py",
        "file_sha256": "baacbe9adc69ddefe49b7da0d134b63b99f41314383caa8c69d9c2dfe1eba75d",
        "bytes": 797440,
        "mode": "0664",
        "nlink": 1,
        "syntax_error": None,
        "semantic_error": "historical v16 supersession anchor was not retained and BASE remained predecessor r5",
    },
    "launcher": {
        "path": f"deliverables/{BASE}_cold_launch_v16r2r6_semantic_source.py",
        "file_sha256": "503caa41bfc0dbb4aa0f46048a6837ac2fc68fdc74a336d1e3453d4dd9d50fb2",
        "bytes": 474352,
        "mode": "0664",
        "nlink": 1,
        "syntax_error": None,
        "semantic_error": "historical v16 supersession anchor was not retained and BASE remained predecessor r5",
    },
    "active_anchor": {
        "path": f"deliverables/{BASE}_v16r2r6_active_predecessor_supersession_receipt_v1.json",
        "file_sha256": "ac19fbf7b665c0f68706650c14118801d99d301c49c5f47bc929bc1895fed34d",
        "bytes": 1439,
        "mode": "0444",
        "nlink": 1,
        "syntax_error": None,
        "semantic_error": "r6 active anchor is retained as historical evidence only",
    },
}

# r7 was generated by the earlier retry worker before the active inherited
# predicates were corrected.  Seal those bytes as immutable evidence before
# creating the r8 namespace.
SEVENTH_REJECTION = OUT / (
    f"{BASE}_v16r2r7_semantic_source_rejection_receipt_v1.json"
)
SEVENTH_SUPERSESSION = OUT / (
    f"{BASE}_v16r2r7_to_v16r2r8_semantic_source_rejection_supersession_receipt_v1.json"
)
SEVENTH_FAILED_OUTPUTS = {
    "producer": {
        "path": f"deliverables/{BASE}_v16r2r7_semantic_source.py",
        "file_sha256": "ca4b2ca1de3e4c59c16f20f33db1d3062afd6bfcc693e6a1305d95a7856d75c9",
        "bytes": 505889, "mode": "0664", "nlink": 1,
        "syntax_error": None,
        "semantic_error": "inherited active exact8 predicates still referenced V14 receipt",
    },
    "consumer": {
        "path": f"deliverables/{BASE}_independent_verifier_assembler_authority_consumer_v16r2r7_semantic_source.py",
        "file_sha256": "aabf628dd05366c0b4c62799101cacb9f0fc05263d3cc1d9d74e1bf981351b3d",
        "bytes": 798357, "mode": "0664", "nlink": 1,
        "syntax_error": None,
        "semantic_error": "inherited active exact8 predicates still referenced V14 receipt",
    },
    "launcher": {
        "path": f"deliverables/{BASE}_cold_launch_v16r2r7_semantic_source.py",
        "file_sha256": "a644cf8fe475caf3b5825bdcb045c6724aaa648b2467a1ae3ede25bf89506b04",
        "bytes": 475269, "mode": "0664", "nlink": 1,
        "syntax_error": None,
        "semantic_error": "inherited active exact8 predicates still referenced V14 receipt",
    },
    "active_anchor": {
        "path": f"deliverables/{BASE}_v16r2r7_active_predecessor_supersession_receipt_v1.json",
        "file_sha256": "b7740343b4ec45cc57c5a567ab84495decbcfe426a97b6c07ee6aada0aa07603",
        "bytes": 1439, "mode": "0444", "nlink": 1,
        "syntax_error": None,
        "semantic_error": "r7 active anchor retained as historical evidence only",
    },
}

EIGHTH_REJECTION = OUT / (
    f"{BASE}_v16r2r8_semantic_source_rejection_receipt_v1.json"
)
EIGHTH_SUPERSESSION = OUT / (
    f"{BASE}_v16r2r8_to_v16r2r9_semantic_source_rejection_supersession_receipt_v1.json"
)
EIGHTH_FAILED_OUTPUTS = {
    "producer": {
        "path": f"deliverables/{BASE}_v16r2r8_semantic_source.py",
        "file_sha256": "f09a53252385692623b4e1e8651eb0acab74154efcd89231f8385ec78f647e1d",
        "bytes": 505811, "mode": "0664", "nlink": 1,
        "syntax_error": None,
        "semantic_error": "retry source static quartet still pointed at frozen v16r2 filenames",
    },
    "consumer": {
        "path": f"deliverables/{BASE}_independent_verifier_assembler_authority_consumer_v16r2r8_semantic_source.py",
        "file_sha256": "a7061da26366f89191b3a031446c07080dff7dd2a4b37c38af40bc70aa346f2e",
        "bytes": 798141, "mode": "0664", "nlink": 1,
        "syntax_error": None,
        "semantic_error": "retry source static quartet still pointed at frozen v16r2 filenames",
    },
    "launcher": {
        "path": f"deliverables/{BASE}_cold_launch_v16r2r8_semantic_source.py",
        "file_sha256": "5fe4b642a4bf69a5bfa7b52444c7a6f0ebad6be02f26d5838ad7ecc2eaec85c2",
        "bytes": 475160, "mode": "0664", "nlink": 1,
        "syntax_error": None,
        "semantic_error": "retry source static quartet still pointed at frozen v16r2 filenames",
    },
    "active_anchor": {
        "path": f"deliverables/{BASE}_v16r2r8_active_predecessor_supersession_receipt_v1.json",
        "file_sha256": "00e5819cab0a45d30f96503c2b52bb47f6c46f3dcf55c03ada759b49d9738203",
        "bytes": 1439, "mode": "0444", "nlink": 1,
        "syntax_error": None,
        "semantic_error": "r8 active anchor retained as historical evidence only",
    },
}

# Filled by ``main`` after the active r7 anchor is sealed.  The generated
# source receives literal pins, so a later runtime cannot silently substitute
# another receipt.
ACTIVE_ANCHOR_FILE_PIN = _HEX if "_HEX" in globals() else "0" * 64
ACTIVE_ANCHOR_OBJECT_PIN = _HEX if "_HEX" in globals() else "0" * 64
V16_SUPERSESSION_FILE_PIN = "0" * 64
V16_SUPERSESSION_OBJECT_PIN = "0" * 64

_HEX = "0" * 64
_DRAFT_FILE = "d" * 64
_DRAFT_OBJECT = "e" * 64
_DRAFT_SCHEMA = "f" * 64
_DRAFT_SOURCE = "c" * 64


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def canonical(value: Any) -> bytes:
    return json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")


def close_object(body: dict[str, Any]) -> dict[str, Any]:
    out = dict(body)
    out.pop("object_sha256", None)
    out["object_sha256"] = sha(canonical(out))
    return out


def read_stable(path: Path) -> bytes:
    """Read one regular nlink=1 file while checking identity before/after."""
    fd = os.open(path, os.O_RDONLY | os.O_CLOEXEC | getattr(os, "O_NOFOLLOW", 0))
    try:
        before = os.fstat(fd)
        if not stat.S_ISREG(before.st_mode) or before.st_nlink != 1:
            raise RuntimeError(f"input is not regular/nlink=1: {path}")
        chunks: list[bytes] = []
        while True:
            part = os.read(fd, 1 << 20)
            if not part:
                break
            chunks.append(part)
        after = os.fstat(fd)
        named = os.lstat(path)
        if (before.st_dev, before.st_ino, before.st_size) != (
            after.st_dev, after.st_ino, after.st_size
        ) or (before.st_dev, before.st_ino) != (named.st_dev, named.st_ino):
            raise RuntimeError(f"input identity drift: {path}")
        raw = b"".join(chunks)
        if len(raw) != before.st_size:
            raise RuntimeError(f"short read: {path}")
        return raw
    finally:
        os.close(fd)


def install_o_excl(path: Path, raw: bytes, *, mode: int = 0o664) -> str:
    """Install an absent target, or replay exactly identical bytes only."""
    # ``OUT`` already exists in the clean room.  Creating only this explicit
    # parent is harmless and cannot create a runtime surface.
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        fd = os.open(
            path,
            os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_CLOEXEC,
            mode,
        )
    except FileExistsError:
        old = read_stable(path)
        st = path.stat()
        if old != raw or st.st_nlink != 1 or stat.S_IMODE(st.st_mode) != mode:
            raise RuntimeError(f"append-only target mismatch: {path}")
        return "replayed"
    try:
        view = memoryview(raw)
        offset = 0
        while offset < len(view):
            offset += os.write(fd, view[offset:])
        os.fsync(fd)
        os.fchmod(fd, mode)
    finally:
        os.close(fd)
    dfd = os.open(path.parent, os.O_RDONLY | os.O_DIRECTORY | os.O_CLOEXEC)
    try:
        os.fsync(dfd)
    finally:
        os.close(dfd)
    return "installed"


def seal_prior_malformed_namespace(
    *,
    failed_outputs: dict[str, dict[str, Any]],
    rejection_path: Path,
    supersession_path: Path,
    predecessor_namespace: str,
    successor_namespace: str,
    receipt_schema: str | None = None,
    receipt_status: str | None = None,
) -> dict[str, Any]:
    """Freeze one failed namespace before starting its fresh retry."""
    observed: dict[str, Any] = {}
    for role, record in failed_outputs.items():
        path = ROOT / record["path"]
        raw = read_stable(path)
        st = path.stat()
        actual = {
            "path": record["path"],
            "file_sha256": sha(raw),
            "bytes": len(raw),
            "mode": f"{stat.S_IMODE(st.st_mode):04o}",
            "nlink": st.st_nlink,
            "syntax_error": record["syntax_error"],
        }
        if "semantic_error" in record:
            actual["semantic_error"] = record["semantic_error"]
        # The bytes are evidence, not mutable input.  Refuse to seal a name
        # whose observed identity differs from the recorded failed attempt.
        if actual != record:
            raise RuntimeError(
                "malformed predecessor namespace drift: "
                + json.dumps({"role": role, "actual": actual, "recorded": record}, sort_keys=True)
            )
        observed[role] = actual

    rejection = close_object({
        "schema": "cm2.c79g.v16r2.semantic-source-rejection.v1",
        "status": "PERMANENT_FAIL_CLOSED_MALFORMED_SOURCE__ZERO_CREDIT",
        "rejection_reason": "AST_PARSE_FAILED_AFTER_FIXED_SPAN_REGENERATION",
        "failed_namespace": predecessor_namespace,
        "failed_outputs": observed,
        "append_only": True,
        "overwrite_delete_or_reuse_allowed": False,
        "runtime_authorized": False,
        "formal_global_closure_credit": 0,
        "D02_unlock": False,
        "manifest_created": False,
        "outer_created": False,
        "runtime_surface_created": False,
    })
    rejection_raw = canonical(rejection) + b"\n"
    rejection_action = install_o_excl(rejection_path, rejection_raw, mode=0o444)
    predecessor_tag = predecessor_namespace.split("_", 1)[0]
    successor_tag = successor_namespace.split("_", 1)[0]
    supersession = close_object({
        "schema": receipt_schema or
            "cm2.c79g.v16r2-to-v16r2r2.semantic-source-rejection-supersession.v1",
        "status": receipt_status or
            "FROZEN_APPEND_ONLY_V16R2_MALFORMED_SOURCE_REJECTED__V16R2R2_ONLY",
        "predecessor_rejection_path": str(rejection_path.relative_to(ROOT)),
        "predecessor_rejection_file_sha256": sha(rejection_raw),
        "predecessor_rejection_object_sha256": rejection["object_sha256"],
        "predecessor_namespace": predecessor_namespace,
        "successor_namespace": successor_namespace,
        "append_only": True,
        "runtime_authorized": False,
        "formal_global_closure_credit": 0,
        "D02_unlock": False,
    })
    supersession_raw = canonical(supersession) + b"\n"
    supersession_action = install_o_excl(supersession_path, supersession_raw, mode=0o444)
    return {
        "rejection": {
            "path": str(rejection_path.relative_to(ROOT)),
            "file_sha256": sha(rejection_raw),
            "object_sha256": rejection["object_sha256"],
            "action": rejection_action,
        },
        "supersession": {
            "path": str(supersession_path.relative_to(ROOT)),
            "file_sha256": sha(supersession_raw),
            "object_sha256": supersession["object_sha256"],
            "action": supersession_action,
        },
        "failed_outputs": observed,
    }


def seal_active_predecessor_anchor() -> dict[str, Any]:
    """Create the canonical, zero-credit anchor for the current namespace."""
    if PRIOR_SUPERSESSION is None:
        raise RuntimeError("active predecessor supersession was not sealed")
    predecessor_raw = read_stable(PRIOR_SUPERSESSION)
    predecessor_obj = json.loads(predecessor_raw.decode("utf-8"))
    frozen_raw = read_stable(V16_SUPERSESSION)
    frozen_obj = json.loads(frozen_raw.decode("utf-8"))
    body = {
        "schema": f"cm2.c79g.{SUCCESSOR_TAG}.active-predecessor-supersession.v1",
        "status": "FROZEN_APPEND_ONLY_ACTIVE_PREDECESSOR_ANCHOR__ZERO_CREDIT",
        "predecessor_namespace": f"{PREDECESSOR_TAG}_semantic_source",
        "predecessor_supersession_path": str(PRIOR_SUPERSESSION.relative_to(ROOT)),
        "predecessor_supersession_file_sha256": sha(predecessor_raw),
        "predecessor_supersession_object_sha256": predecessor_obj["object_sha256"],
        "frozen_v16_semantic_supersession_path": str(V16_SUPERSESSION.relative_to(ROOT)),
        "frozen_v16_semantic_supersession_file_sha256": sha(frozen_raw),
        "frozen_v16_semantic_supersession_object_sha256": frozen_obj["object_sha256"],
        "upstream_checkpoint_object_sha256": UPSTREAM_CHECKPOINT,
        "successor_checkpoint_object_sha256": SUCCESSOR_CHECKPOINT,
        "successor_namespace": SUCCESSOR_NAMESPACE,
        "append_only": True,
        "runtime_authorized": False,
        "formal_global_closure_credit": 0,
        "D02_unlock": False,
        "manifest_created": False,
        "outer_created": False,
    }
    closed = close_object(body)
    raw = canonical(closed) + b"\n"
    action = install_o_excl(ACTIVE_ANCHOR_RECEIPT, raw, mode=0o444)
    return {
        "path": str(ACTIVE_ANCHOR_RECEIPT.relative_to(ROOT)),
        "file_sha256": sha(raw),
        "object_sha256": closed["object_sha256"],
        "action": action,
        "upstream_checkpoint_object_sha256": UPSTREAM_CHECKPOINT,
        "successor_checkpoint_object_sha256": SUCCESSOR_CHECKPOINT,
    }


def line_offsets(text: str) -> list[int]:
    offsets = [0]
    for line in text.splitlines(keepends=True):
        offsets.append(offsets[-1] + len(line))
    return offsets


def absolute_position(offsets: list[int], row: int, col: int) -> int:
    if row <= 0 or row > len(offsets):
        raise ValueError(f"bad source position {(row, col)}")
    return offsets[row - 1] + col


def target_names(node: ast.AST) -> set[str]:
    targets: Iterable[ast.AST]
    if isinstance(node, ast.Assign):
        targets = node.targets
    elif isinstance(node, ast.AnnAssign):
        targets = (node.target,)
    else:
        return set()
    out: set[str] = set()
    for target in targets:
        if isinstance(target, ast.Name):
            out.add(target.id)
    return out


def indent_for(text: str, line: int) -> str:
    start = line_offsets(text)[line - 1]
    end = text.find("\n", start)
    if end < 0:
        end = len(text)
    prefix = text[start:end]
    return prefix[: len(prefix) - len(prefix.lstrip(" \t"))]


def format_replacement(text: str, node: ast.AST, replacement: str) -> str:
    indent = indent_for(text, int(node.lineno))
    body = replacement.replace("\n", "\n" + indent)
    # apply_edits consumes the complete final source line, including its
    # newline.  Keep one newline on every replacement so the following held
    # line cannot be glued onto the replacement's last token.
    if not body.endswith("\n"):
        body += "\n"
    return indent + body


def apply_edits(text: str, edits: list[tuple[int, int, str]]) -> str:
    # A semantic pass must never have overlapping spans.  This catches an
    # accidental parent/child replacement before bytes reach the new file.
    ordered = sorted(edits, key=lambda item: (item[0], item[1]))
    for previous, current in zip(ordered, ordered[1:]):
        if current[0] < previous[1]:
            raise RuntimeError(f"overlapping fixed spans: {previous} / {current}")
    offsets = line_offsets(text)
    out = text
    for start_line, end_line, replacement in sorted(
        edits, key=lambda item: item[0], reverse=True
    ):
        start = offsets[start_line - 1]
        end_line_start = offsets[end_line - 1]
        end = text.find("\n", end_line_start)
        if end < 0:
            end = len(text)
        else:
            end += 1
        out = out[:start] + replacement + out[end:]
    return out


def exact8_literal(role: str) -> str:
    """Return the active exact8 expression for one source role."""
    if role == "producer":
        members = [
            f'OUT / "{ACTIVE_ANCHOR_RECEIPT.name}"',
            f'OUT / "{SCHEMA_NAME}"',
            f'OUT / "{CONTRACT_NAME}"',
            "SELF",
            f'OUT / "{CFILE}"',
            f'OUT / "{TRANSITION_NAME}"',
            f'OUT / "{AUDIT_NAME}"',
            f'OUT / "{LFILE}"',
        ]
    elif role == "consumer":
        members = [
            f'OUT / "{ACTIVE_ANCHOR_RECEIPT.name}"',
            "CLOSED_SCHEMA",
            "CONTRACT",
            "PRODUCER_SOURCE",
            "SELF",
            "V14_TO_V15_TRANSITION",
            "STATIC_AUDIT_V15",
            "COLD_LAUNCHER",
        ]
    else:
        members = [
            f'ROOT / "deliverables/{ACTIVE_ANCHOR_RECEIPT.name}"',
            "SCHEMA",
            "CONTRACT",
            "PRODUCER",
            "CONSUMER",
            "TRANSITION",
            "AUDIT",
            "SELF",
        ]
    return "(" + ",\n".join("    " + item for item in members) + ",\n)"


def assignment_replacement(role: str, names: set[str], node: ast.AST, text: str) -> str | None:
    """Choose a replacement for one complete AST assignment span."""
    # The launcher has two path blocks: import-time placeholders and the
    # configure_workspace_paths block.  Both are made explicitly successor
    # shaped so a stale path cannot become active after configuration.
    if role == "launcher" and {"SCHEMA", "CONTRACT", "PRODUCER", "CONSUMER", "TRANSITION", "AUDIT"} <= names:
        return (
            f'SCHEMA = ROOT / "deliverables/{SCHEMA_NAME}"\n'
            f'CONTRACT = ROOT / "deliverables/{CONTRACT_NAME}"\n'
            f'PRODUCER = ROOT / "deliverables/{PFILE}"\n'
            f'CONSUMER = ROOT / "deliverables/{CFILE}"\n'
            f'TRANSITION = ROOT / "deliverables/{TRANSITION_NAME}"\n'
            f'AUDIT = ROOT / "deliverables/{AUDIT_NAME}"\n'
            f'MANIFEST = ROOT / "deliverables/{MANIFEST_NAME}"\n'
            f'OUTER = ROOT / "deliverables/{OUTER_NAME}"'
        )
    if role == "launcher" and {"MANIFEST", "OUTER"} <= names and isinstance(getattr(node, "value", None), ast.Name) and getattr(node.value, "id", None) == "SELF":
        return (
            f'MANIFEST = OUT / "{MANIFEST_NAME}"\n'
            f'OUTER = OUT / "{OUTER_NAME}"'
        )
    if role == "launcher" and "BASE7_PINS" in names:
        # Keep one assignment in the module-level draft block.  The later
        # configure hook clears that same mapping instead of introducing a
        # second active assignment.
        return "BASE7_PINS.clear()" if int(node.lineno) > 700 else "BASE7_PINS = {}"
    if role == "launcher" and "EXACT8" in names:
        # The configure hook is inside a function with ``global EXACT8``;
        # an annotation in that scope is illegal at compile time.  Keep the
        # type annotation only in the module-level draft assignment.
        prefix = "EXACT8 = " if int(node.lineno) > 700 else "EXACT8: tuple[Path, ...] = "
        return prefix + exact8_literal(role)

    # All other blocks are single-name assignments.  Matching the complete
    # node (rather than replacing a lexical substring) is the key semantic
    # guard in this pass.
    if len(names) != 1:
        return None
    name = next(iter(names))
    common: dict[str, str] = {
        "V15_DRAFT_RUNTIME_DISABLED": "V15_DRAFT_RUNTIME_DISABLED = True",
        "FINAL_V15_CORE_PINS_INSTALLED": "FINAL_V15_CORE_PINS_INSTALLED = False",
        "FINAL_CURRENT_V15_PINS_INSTALLED": "FINAL_CURRENT_V15_PINS_INSTALLED = False",
        "FINAL_BASE7_PINS_INSTALLED": "FINAL_BASE7_PINS_INSTALLED = False",
        "CONTRACT_FILE_PIN": f'CONTRACT_FILE_PIN = "{_DRAFT_FILE}"',
        "CONTRACT_OBJECT_PIN": f'CONTRACT_OBJECT_PIN = "{_DRAFT_OBJECT}"',
        "CLOSED_SCHEMA_FILE_PIN": f'CLOSED_SCHEMA_FILE_PIN = "{_DRAFT_SCHEMA}"',
        "PRODUCER_SOURCE_PIN": f'PRODUCER_SOURCE_PIN = "{_DRAFT_SOURCE}"',
        "CHECKPOINT_OBJECT_PIN": f'CHECKPOINT_OBJECT_PIN = "{SUCCESSOR_CHECKPOINT}"',
        "V15_DRAFT_CORE_PIN_SENTINELS": (
            'V15_DRAFT_CORE_PIN_SENTINELS = ("' + _DRAFT_FILE + '", "' +
            _DRAFT_OBJECT + '", "' + _DRAFT_SCHEMA + '")'
        ),
        "V15_DRAFT_CURRENT_CORE_PINS": (
            'V15_DRAFT_CURRENT_CORE_PINS = ("' + _DRAFT_FILE + '", "' +
            _DRAFT_OBJECT + '", "' + _DRAFT_SCHEMA + '", "' + _DRAFT_SOURCE + '")'
        ),
    }
    if name in common:
        return common[name]

    if role == "producer":
        replacements = {
            "SELF": f'SELF = OUT / "{PFILE}"',
            "SCHEMA": f'SCHEMA = "cm2.round306c79g.true-global-no-producer-consumer.{STATIC_TAG}"',
            "BASE": f'BASE = "{BASE}_{SUCCESSOR_SOURCE_SUFFIX}"',
            "CONTRACT": f'CONTRACT = OUT / "{CONTRACT_NAME}"',
            "CLOSED_SCHEMA": f'CLOSED_SCHEMA = OUT / "{SCHEMA_NAME}"',
            "V14_TO_V15_TRANSITION": f'V14_TO_V15_TRANSITION = OUT / "{TRANSITION_NAME}"',
            "STATIC_AUDIT_V15": f'STATIC_AUDIT_V15 = OUT / "{AUDIT_NAME}"',
            "COLD_LAUNCHER": f'COLD_LAUNCHER = OUT / "{LFILE}"',
            "COLD_MANIFEST": f'COLD_MANIFEST = OUT / "{MANIFEST_NAME}"',
            "COLD_OUTER": f'COLD_OUTER = OUT / "{OUTER_NAME}"',
            "CANDIDATE_A": 'CANDIDATE_A = RUNTIME / ("c79g-v16r2-semantic-source-candidate-a-" + CHECKPOINT_OBJECT_PIN)',
            "CANDIDATE_B": 'CANDIDATE_B = RUNTIME / ("c79g-v16r2-semantic-source-candidate-b-" + CHECKPOINT_OBJECT_PIN)',
            "COLD_EXACT8": "COLD_EXACT8 = " + exact8_literal(role),
        }
        return replacements.get(name)

    if role == "consumer":
        replacements = {
            "SOURCE_BASENAME": f'SOURCE_BASENAME = "{CFILE}"',
            "SELF": "SELF = OUT / SOURCE_BASENAME",
            "SCHEMA": f'SCHEMA = "cm2.round306c79g.true-global-no-producer-consumer.{STATIC_TAG}"',
            "BASE": f'BASE = "{BASE}_{SUCCESSOR_SOURCE_SUFFIX}"',
            "CONTRACT": f'CONTRACT = OUT / "{CONTRACT_NAME}"',
            "CLOSED_SCHEMA": f'CLOSED_SCHEMA = OUT / "{SCHEMA_NAME}"',
            "V14_TO_V15_TRANSITION": f'V14_TO_V15_TRANSITION = OUT / "{TRANSITION_NAME}"',
            "STATIC_AUDIT_V15": f'STATIC_AUDIT_V15 = OUT / "{AUDIT_NAME}"',
            "PRODUCER_SOURCE": f'PRODUCER_SOURCE = OUT / "{PFILE}"',
            "COLD_LAUNCHER": f'COLD_LAUNCHER = OUT / "{LFILE}"',
            "COLD_LAUNCH_MANIFEST": f'COLD_LAUNCH_MANIFEST = OUT / "{MANIFEST_NAME}"',
            "COLD_LAUNCH_OUTER": f'COLD_LAUNCH_OUTER = OUT / "{OUTER_NAME}"',
            "FINAL_OUTER": f'FINAL_OUTER = "{OUTER_NAME}"',
            "CANDIDATE_A": 'CANDIDATE_A = RUNTIME / ("c79g-v16r2-semantic-source-candidate-a-" + CHECKPOINT_OBJECT_PIN)',
            "CANDIDATE_B": 'CANDIDATE_B = RUNTIME / ("c79g-v16r2-semantic-source-candidate-b-" + CHECKPOINT_OBJECT_PIN)',
            "REJECTION_NAMESPACE": 'REJECTION_NAMESPACE = RUNTIME / ("c79g-v16r2-semantic-source-rejections-" + CHECKPOINT_OBJECT_PIN)',
            "LATER_REJECTION": 'LATER_REJECTION = REJECTION_NAMESPACE / "rejection.json"',
            "V15_CURRENT_EXACT8": "V15_CURRENT_EXACT8 = " + exact8_literal(role),
        }
        return replacements.get(name)

    # launcher-specific scalar assignments
    replacements = {
        # Launcher ``CHECKPOINT`` remains the held upstream C53 witness;
        # ``CHECKPOINT_OBJECT_PIN`` is the successor rejection object pin.
        "CHECKPOINT": f'CHECKPOINT = "{UPSTREAM_CHECKPOINT}"',
    "BASE": f'BASE = "{BASE}_{SUCCESSOR_SOURCE_SUFFIX}"',
        "LAUNCHER_RELATIVE": f'LAUNCHER_RELATIVE = Path("deliverables") / "{LFILE}"',
        "SELF": f'SELF = ROOT / "deliverables/{LFILE}"',
        "V15_REJECTION_NAMESPACE": 'V15_REJECTION_NAMESPACE = ROOT / "__unconfigured_v16r2_semantic_rejections__"',
        "V15_LATER_REJECTION": 'V15_LATER_REJECTION = V15_REJECTION_NAMESPACE / "rejection.json"',
    }
    # The configured launcher path block has RHS names that are not simple
    # top-level values; use the same explicit path replacements everywhere.
    if name == "SCHEMA":
        return f'SCHEMA = OUT / "{SCHEMA_NAME}"'
    if name == "CONTRACT":
        return f'CONTRACT = OUT / "{CONTRACT_NAME}"'
    if name == "PRODUCER":
        return f'PRODUCER = OUT / "{PFILE}"'
    if name == "CONSUMER":
        return f'CONSUMER = OUT / "{CFILE}"'
    if name == "TRANSITION":
        return f'TRANSITION = OUT / "{TRANSITION_NAME}"'
    if name == "AUDIT":
        return f'AUDIT = OUT / "{AUDIT_NAME}"'
    if name == "MANIFEST":
        return f'MANIFEST = OUT / "{MANIFEST_NAME}"'
    if name == "OUTER":
        return f'OUTER = OUT / "{OUTER_NAME}"'
    if name == "V15_REJECTION_NAMESPACE" and node.lineno > 700:
        return 'V15_REJECTION_NAMESPACE = RUNTIME / ("c79g-v16r2-semantic-source-rejections-" + CHECKPOINT)'
    if name == "V15_LATER_REJECTION" and node.lineno > 700:
        return 'V15_LATER_REJECTION = V15_REJECTION_NAMESPACE / "rejection.json"'
    return replacements.get(name)


def semantic_ast_patch(text: str, role: str) -> tuple[str, int, list[str]]:
    """Patch active assignments by complete AST source spans."""
    tree = ast.parse(text, filename=f"held_{role}.py")
    edits: list[tuple[int, int, str]] = []
    changed: list[str] = []
    for node in ast.walk(tree):
        if not isinstance(node, (ast.Assign, ast.AnnAssign)):
            continue
        names = target_names(node)
        replacement = assignment_replacement(role, names, node, text)
        if replacement is None:
            continue
        edits.append((int(node.lineno), int(node.end_lineno), format_replacement(text, node, replacement)))
        changed.append(f"{role}:{node.lineno}:{','.join(sorted(names))}")
    if not edits:
        raise RuntimeError(f"no active AST assignments matched for {role}")
    return apply_edits(text, edits), len(edits), changed


def active_graph_patch(text: str, role: str) -> tuple[str, int, list[str]]:
    """Patch active exact8 paths while retaining historical V14 replay."""
    tree = ast.parse(text, filename=f"active_graph_{role}.py")
    lines = text.splitlines(True)
    edits: list[tuple[int, int, str]] = []
    labels: list[str] = []

    def seg(node: ast.AST) -> str:
        return "".join(lines[int(node.lineno) - 1:int(node.end_lineno)])

    def add(node: ast.AST, replacement: str, label: str) -> None:
        edits.append((int(node.lineno), int(node.end_lineno),
                      format_replacement(text, node, replacement)))
        labels.append(f"{role}:{node.lineno}:{label}")

    for node in ast.walk(tree):
        if role == "launcher" and isinstance(node, ast.Assign):
            if target_names(node) == {"current_first_is_receipt"}:
                add(node, """current_first_is_receipt = (
    len(self.files) == 8 and
    EXACT8[0] == ACTIVE_PREDECESSOR_SUPERSESSION and
    self.files[0] is self.by_path[EXACT8[0]] and
    self.by_path[EXACT8[0]].identity in current_exact8_identities)""",
                    "active_identity_first_member")
        if role == "producer" and isinstance(node, ast.Expr):
            source = seg(node)
            if ("manifest_by_path[V14_RUNTIME_REGISTRY_SHAPE_DRIFT_"
                    "SUPERSESSION_RECEIPT]" in source and "COLD_EXACT8[0]" in source):
                add(node, """need(len(manifest_by_path) == 8 and
     manifest_by_path[SELF] == self_guard.file_sha256 and
     manifest_by_path[CONTRACT] == CONTRACT_FILE_PIN and
     manifest_by_path[CLOSED_SCHEMA] == CLOSED_SCHEMA_FILE_PIN and
     manifest_by_path[ACTIVE_PREDECESSOR_SUPERSESSION] ==
         ACTIVE_PREDECESSOR_SUPERSESSION_FILE_PIN and
     COLD_EXACT8[0] == ACTIVE_PREDECESSOR_SUPERSESSION,
     "cold-launch manifest active predecessor anchor and policy pins")""",
                    "active_manifest_predicate")

    if role == "launcher":
        for node in ast.walk(tree):
            if isinstance(node, ast.Expr):
                source = seg(node)
                if ("EXACT8 == (" in source and
                        "V14_RUNTIME_REGISTRY_SHAPE_DRIFT_SUPERSESSION_RECEIPT" in source):
                    add(node, """need(FINAL_BASE7_PINS_INSTALLED is True and len(BASE7_PINS) == 7 and
         EXACT8 == (ACTIVE_PREDECESSOR_SUPERSESSION, SCHEMA, CONTRACT,
                    PRODUCER, CONSUMER, TRANSITION, AUDIT, SELF),
         "launcher-native rejection requires final active-anchor pins")""",
                        "active_reconstruction_exact8")

    if role == "consumer":
        for node in ast.walk(tree):
            source = seg(node) if isinstance(node, (ast.Assign, ast.Expr)) else ""
            if isinstance(node, ast.Expr):
                if ("set(policy_by_path) ==" in source and
                        "V14_RUNTIME_REGISTRY_SHAPE_DRIFT_SUPERSESSION_RECEIPT" in source):
                    add(node, """need(set(policy_by_path) == {
             ACTIVE_PREDECESSOR_SUPERSESSION, CONTRACT, CLOSED_SCHEMA,
             V16_TO_V16R2_TRANSITION, STATIC_AUDIT_V16R2,
             COLD_LAUNCHER, COLD_LAUNCH_MANIFEST, COLD_LAUNCH_OUTER},
         "read evidence active static/cold policy set")""", "active_policy_set")
                elif ("set(by_path) ==" in source and
                      "V14_RUNTIME_REGISTRY_SHAPE_DRIFT_SUPERSESSION_RECEIPT" in source):
                    add(node, """need(set(by_path) == {
        ACTIVE_PREDECESSOR_SUPERSESSION, CONTRACT, CLOSED_SCHEMA,
        V16_TO_V16R2_TRANSITION, STATIC_AUDIT_V16R2,
        COLD_LAUNCHER, COLD_LAUNCH_MANIFEST, COLD_LAUNCH_OUTER,
    }, "exact active static/cold policy guard")""", "active_static_policy_set")
                elif ("verify_object(" in source and "v14_supersession" in source and
                      "V14_RUNTIME_REGISTRY_SHAPE_DRIFT_SUPERSESSION_RECEIPT_OBJECT_PIN" in source):
                    add(node, """verify_object(
        v14_supersession, "live active predecessor supersession anchor",
        ACTIVE_PREDECESSOR_SUPERSESSION_OBJECT_PIN)""", "active_anchor_object_pin")
            elif isinstance(node, ast.Assign):
                names = target_names(node)
                if names == {"expected_base7_paths"} and "V14_RUNTIME" in source:
                    add(node, """expected_base7_paths = [
        str(ACTIVE_PREDECESSOR_SUPERSESSION.relative_to(ROOT)),
        str(CLOSED_SCHEMA.relative_to(ROOT)), str(CONTRACT.relative_to(ROOT)),
        str(PRODUCER_SOURCE.relative_to(ROOT)), str(SELF.relative_to(ROOT)),
        str(V16_TO_V16R2_TRANSITION.relative_to(ROOT)),
        str(STATIC_AUDIT_V16R2.relative_to(ROOT)),
    ]""", "active_expected_base7_paths")
                elif names == {"v14_supersession"} and "by_path[V14_RUNTIME" in source:
                    add(node, """v14_supersession = strict_json(
        by_path[ACTIVE_PREDECESSOR_SUPERSESSION].raw,
        "live active predecessor supersession anchor")""", "active_anchor_read")
                elif names == {"exact8_stats"} and "by_path[V14_RUNTIME" in source:
                    add(node, """exact8_stats = [
        by_path[ACTIVE_PREDECESSOR_SUPERSESSION].before,
        by_path[CLOSED_SCHEMA].before, by_path[CONTRACT].before,
        producer_guard.before, self_guard.before,
        by_path[V16_TO_V16R2_TRANSITION].before,
        by_path[STATIC_AUDIT_V16R2].before,
        by_path[COLD_LAUNCHER].before,
    ]""", "active_exact8_stats")
                elif names == {"exact8_expected"} and "V14_RUNTIME" in source:
                    add(node, """exact8_expected = [
        {"file_sha256": ACTIVE_PREDECESSOR_SUPERSESSION_FILE_PIN,
         "entry_name": str(ACTIVE_PREDECESSOR_SUPERSESSION.relative_to(ROOT))},
        {"file_sha256": CLOSED_SCHEMA_FILE_PIN, "entry_name": str(CLOSED_SCHEMA.relative_to(ROOT))},
        {"file_sha256": CONTRACT_FILE_PIN, "entry_name": str(CONTRACT.relative_to(ROOT))},
        {"file_sha256": PRODUCER_SOURCE_PIN, "entry_name": str(PRODUCER_SOURCE.relative_to(ROOT))},
        {"file_sha256": self_guard.file_sha256, "entry_name": str(SELF.relative_to(ROOT))},
        {"file_sha256": transition_file_sha256, "entry_name": str(V16_TO_V16R2_TRANSITION.relative_to(ROOT))},
        {"file_sha256": audit_file_sha256, "entry_name": str(STATIC_AUDIT_V16R2.relative_to(ROOT))},
        {"file_sha256": launcher_file_sha256, "entry_name": str(COLD_LAUNCHER.relative_to(ROOT))},
    ]""", "active_exact8_expected")

    if not edits:
        raise RuntimeError(f"no active graph spans matched for {role}")
    return apply_edits(text, edits), len(edits), labels


def token_namespace_rewrite(text: str) -> tuple[str, int]:
    """Rewrite inherited namespace spellings on lexer token fixed spans."""
    offsets = line_offsets(text)
    edits: list[tuple[int, int, str]] = []

    def rewrite(lexeme: str, token_type: int) -> str:
        # Longest transition spellings first.  NAME tokens cannot contain a
        # hyphen, so identifiers use underscore labels while string/comment
        # spans retain the human-readable hyphen spelling.
        if token_type == tokenize.NAME:
            mappings = (
                (r"V13_TO_V16", "V16_TO_V16R2"),
                (r"V14_TO_V15", "V16_TO_V16R2"),
                (r"V13_TO_V15", "V16_TO_V16R2"),
                (r"V12_TO_V15", "V12_TO_V16R2"),
                (r"v13_to_v16", "v16_to_v16r2"),
                (r"v14_to_v15", "v16_to_v16r2"),
                (r"v13_to_v15", "v16_to_v16r2"),
                (r"v13_to_v14", "v16_to_v16r2"),
                (r"v12_to_v15", "v12_to_v16r2"),
                (r"C79G_V15", "C79G_V16R2"),
                (r"c79g_v15", "c79g_v16r2"),
                (r"V15", "V16R2"),
                (r"v15", "v16r2"),
            )
        else:
            mappings = (
                (r"V13_TO_V16", "V16_TO_V16R2"),
                (r"V14_TO_V15", "V16_TO_V16R2"),
                (r"V13_TO_V15", "V16_TO_V16R2"),
                (r"V12_TO_V15", "V12_TO_V16R2"),
                (r"v13-to-v16", "v16-to-v16r2"),
                (r"v14-to-v15", "v16-to-v16r2"),
                (r"v13-to-v15", "v16-to-v16r2"),
                (r"v13-to-v14", "v16-to-v16r2"),
                (r"v12-to-v15", "v12-to-v16r2"),
                (r"v13_to_v16", "v16_to_v16r2"),
                (r"v14_to_v15", "v16_to_v16r2"),
                (r"v13_to_v15", "v16_to_v16r2"),
                (r"v13_to_v14", "v16_to_v16r2"),
                (r"v12_to_v15", "v12_to_v16r2"),
                (r"current_exact8_first_member_is_v14_registry_shape_drift",
                 "current_exact8_first_member_is_active_predecessor"),
                (r"base7_first_member_is_v14_registry_shape_drift",
                 "base7_first_member_is_active_predecessor"),
                (r"C79G_V15", "C79G_V16R2"),
                (r"c79g-v15", "c79g-v16r2"),
                (r"c79g_v15", "c79g_v16r2"),
                (r"V15", "V16R2"),
                (r"v15", "v16r2"),
            )
        result = lexeme
        for pattern, replacement in mappings:
            result = re.sub(pattern, replacement, result)
        # The v15 predecessor may have acquired a v16r2 suffix through the
        # generic mapping; keep the active transition unambiguously successor
        # oriented rather than retaining a v13/v14 expectation.
        if token_type == tokenize.NAME:
            result = re.sub(r"(?i)v13_to_v16r2", "v16_to_v16r2", result)
            result = re.sub(r"(?i)v14_to_v16r2", "v16_to_v16r2", result)
        else:
            result = re.sub(r"(?i)v13[-_]to[-_]v16r2", "v16-to-v16r2", result)
            result = re.sub(r"(?i)v14[-_]to[-_]v16r2", "v16-to-v16r2", result)
        return result

    tokens = tokenize.generate_tokens(io.StringIO(text).readline)
    for token in tokens:
        if token.type not in {
            tokenize.NAME,
            tokenize.STRING,
            tokenize.COMMENT,
        }:
            continue
        old = token.string
        new = rewrite(old, token.type)
        if new == old:
            continue
        start = absolute_position(offsets, token.start[0], token.start[1])
        end = absolute_position(offsets, token.end[0], token.end[1])
        edits.append((start, end, new))
    for start, end, new in sorted(edits, reverse=True):
        text = text[:start] + new + text[end:]
    return text, len(edits)


def insert_successor_anchor(text: str) -> str:
    """Insert a small active anchor after the first OUT assignment."""
    marker = "OUT = ROOT / \"deliverables\""
    pos = text.find(marker)
    if pos < 0:
        raise RuntimeError("OUT anchor missing")
    line_end = text.find("\n", pos)
    if line_end < 0:
        line_end = len(text)
    else:
        line_end += 1
    if ACTIVE_ANCHOR_FILE_PIN in {None, "0" * 64} or ACTIVE_ANCHOR_OBJECT_PIN in {None, "0" * 64}:
        raise RuntimeError("active anchor pins were not populated before source insertion")
    anchor = (
        "\n"
        f'ACTIVE_PREDECESSOR_SUPERSESSION = OUT / "{ACTIVE_ANCHOR_RECEIPT.name}"\n'
        f'ACTIVE_SUCCESSOR_NAMESPACE = "{SUCCESSOR_NAMESPACE}"\n'
        f'ACTIVE_SUCCESSOR_NAMESPACE_TAG = "{SUCCESSOR_TAG}-semantic-regeneration"\n'
        f'ACTIVE_PREDECESSOR_SUPERSESSION_FILE_PIN = "{ACTIVE_ANCHOR_FILE_PIN}"\n'
        f'ACTIVE_PREDECESSOR_SUPERSESSION_OBJECT_PIN = "{ACTIVE_ANCHOR_OBJECT_PIN}"\n'
        f'HISTORICAL_V16_SEMANTIC_SUPERSESSION = OUT / "{V16_SUPERSESSION.name}"\n'
        f'HISTORICAL_V16_SEMANTIC_SUPERSESSION_FILE_PIN = "{V16_SUPERSESSION_FILE_PIN}"\n'
        f'HISTORICAL_V16_SEMANTIC_SUPERSESSION_OBJECT_PIN = "{V16_SUPERSESSION_OBJECT_PIN}"\n'
        f'UPSTREAM_CHECKPOINT_OBJECT_PIN = "{UPSTREAM_CHECKPOINT}"\n'
        f'SUCCESSOR_CHECKPOINT_OBJECT_PIN = "{SUCCESSOR_CHECKPOINT}"\n'
        'UPSTREAM_C53_CHECKPOINT_OBJECT_PIN = UPSTREAM_CHECKPOINT_OBJECT_PIN\n'
        'SUCCESSOR_REJECTION_CHECKPOINT_OBJECT_PIN = SUCCESSOR_CHECKPOINT_OBJECT_PIN\n'
        'CHECKPOINT_CHAIN_OBJECT_PINS = (UPSTREAM_C53_CHECKPOINT_OBJECT_PIN, SUCCESSOR_REJECTION_CHECKPOINT_OBJECT_PIN)\n'
        "RUNTIME_AUTHORIZED = False\n"
        "FORMAL_GLOBAL_CLOSURE_CREDIT = 0\n"
        "D02_UNLOCK = False\n"
        "ACTIVE_EXACT8_FIRST_MEMBER = ACTIVE_PREDECESSOR_SUPERSESSION\n"
        f'ACTIVE_REJECTED_RETRY_SUPERSESSION = OUT / "{ACTIVE_ANCHOR_RECEIPT.name}"\n'
    )
    return text[:line_end] + anchor + text[line_end:]


def add_compatibility_flags(text: str, role: str) -> str:
    """Add literal false/true aliases used by independent static reviewers."""
    # Keep aliases in a fixed inserted block; all values are deliberately
    # fail-closed.  Names contain no predecessor namespace token.
    if role == "producer":
        block = (
            "V16R2_DRAFT_RUNTIME_DISABLED = True\n"
            "V16_DRAFT_RUNTIME_DISABLED = True\n"
            "FINAL_V16R2_CORE_PINS_INSTALLED = False\n"
            "FINAL_V16_CORE_PINS_INSTALLED = False\n"
        )
    elif role == "consumer":
        block = (
            "V16R2_DRAFT_RUNTIME_DISABLED = True\n"
            "V16_DRAFT_RUNTIME_DISABLED = True\n"
            "FINAL_BASE7_PINS_INSTALLED = False\n"
            "FINAL_CURRENT_V16R2_PINS_INSTALLED = False\n"
            "FINAL_CURRENT_V16_PINS_INSTALLED = False\n"
        )
    else:
        block = (
            "V16R2_DRAFT_RUNTIME_DISABLED = True\n"
            "V16_DRAFT_RUNTIME_DISABLED = True\n"
        )
    marker = "ACTIVE_EXACT8_FIRST_MEMBER = ACTIVE_PREDECESSOR_SUPERSESSION\n"
    if marker not in text:
        raise RuntimeError("successor anchor missing")
    return text.replace(marker, marker + block, 1)


def validate_source(raw: bytes, role: str) -> dict[str, Any]:
    text = raw.decode("utf-8")
    tree = ast.parse(text, filename=str(TARGETS[role]))
    compile(tree, str(TARGETS[role]), "exec")
    stale = sorted(set(re.findall(r"(?i)v15", text)))
    old_transition = sorted({
        token for token in (
            "v13-to-v16", "v13_to_v16", "v14-to-v15", "v14_to_v15",
            "v14-to-v16", "v14_to_v16",
        ) if token.lower() in text.lower()
    })
    predecessor_base = re.search(
        r'(?m)^BASE\s*=\s*["\'][^"\']*v16r2r7[^"\']*["\']', text,
        flags=re.IGNORECASE)
    required = {
        "supersession": SUPSERSESSION_NAME in text,
        "active_anchor": ACTIVE_ANCHOR_RECEIPT.name in text and
            "ACTIVE_PREDECESSOR_SUPERSESSION =" in text,
        "active_anchor_pins": ACTIVE_ANCHOR_FILE_PIN in text and
            ACTIVE_ANCHOR_OBJECT_PIN in text,
        "historical_v16_path_explicit": V16_SUPERSESSION.name in text,
        "base_is_current_successor": predecessor_base is None and
            SUCCESSOR_SOURCE_SUFFIX in text,
        "successor_transition": "v16_to_v16r2" in text or "v16-to-v16r2" in text,
        "runtime_authorized_false": "RUNTIME_AUTHORIZED = False" in text,
        "credit_zero": "FORMAL_GLOBAL_CLOSURE_CREDIT = 0" in text,
        "D02_false": "D02_UNLOCK = False" in text,
        "no_stale_tokens": not stale,
        "no_old_transition_expectation": not old_transition,
    }
    pyc = [
        str(path.relative_to(ROOT))
        for path in ROOT.rglob("*.pyc")
        if "v16r2_semantic_source" in str(path)
    ]
    required["no_target_pyc"] = not pyc
    if not all(required.values()):
        raise RuntimeError(
            f"{role} source self-check failed: "
            + json.dumps({"required": required, "stale": stale,
                          "old_transition": old_transition,
                          "predecessor_base": bool(predecessor_base),
                          "pyc": pyc}, sort_keys=True)
        )
    return {
        "sha256": sha(raw),
        "bytes": len(raw),
        "lines": text.count("\n") + (0 if text.endswith("\n") else 1),
        "ast_nodes": sum(1 for _ in ast.walk(tree)),
        "required": required,
    }


def main() -> int:
    try:
        rejection_raw = read_stable(V16_REJECTION)
        supersession_raw = read_stable(V16_SUPERSESSION)
        rejection = json.loads(rejection_raw.decode("utf-8"))
        supersession = json.loads(supersession_raw.decode("utf-8"))
        if rejection.get("formal_global_closure_credit") != 0 or rejection.get("D02_unlock") is not False:
            raise RuntimeError("frozen predecessor rejection is not zero-credit")
        if supersession.get("formal_global_closure_credit") != 0 or supersession.get("D02_unlock") is not False:
            raise RuntimeError("frozen predecessor supersession is not zero-credit")
        first_receipts = seal_prior_malformed_namespace(
            failed_outputs=FIRST_FAILED_OUTPUTS,
            rejection_path=FIRST_REJECTION,
            supersession_path=FIRST_SUPERSESSION,
            predecessor_namespace="v16r2_semantic_source",
            successor_namespace="v16r2r2_semantic_source",
        )
        second_receipts = seal_prior_malformed_namespace(
            failed_outputs=SECOND_FAILED_OUTPUTS,
            rejection_path=SECOND_REJECTION,
            supersession_path=SECOND_SUPERSESSION,
            predecessor_namespace="v16r2r2_semantic_source",
            successor_namespace="v16r2r3_semantic_source",
        )
        third_receipts = seal_prior_malformed_namespace(
            failed_outputs=THIRD_FAILED_OUTPUTS,
            rejection_path=THIRD_REJECTION,
            supersession_path=THIRD_SUPERSESSION,
            predecessor_namespace="v16r2r3_semantic_source",
            successor_namespace="v16r2r4_semantic_source",
        )
        fourth_receipts = seal_prior_malformed_namespace(
            failed_outputs=FOURTH_FAILED_OUTPUTS,
            rejection_path=FOURTH_REJECTION,
            supersession_path=FOURTH_SUPERSESSION,
            predecessor_namespace="v16r2r4_semantic_source",
            successor_namespace="v16r2r5_semantic_source",
        )
        fifth_receipts = seal_prior_malformed_namespace(
            failed_outputs=FIFTH_FAILED_OUTPUTS,
            rejection_path=FIFTH_REJECTION,
            supersession_path=FIFTH_SUPERSESSION,
            predecessor_namespace="v16r2r5_semantic_source",
            successor_namespace="v16r2r6_semantic_source",
        )
        sixth_receipts = seal_prior_malformed_namespace(
            failed_outputs=SIXTH_FAILED_OUTPUTS,
            rejection_path=SIXTH_REJECTION,
            supersession_path=SIXTH_SUPERSESSION,
            predecessor_namespace="v16r2r6_semantic_source",
            successor_namespace="v16r2r7_semantic_source",
            receipt_schema=(
                "cm2.c79g.v16r2r6-to-v16r2r7."
                "semantic-source-rejection-supersession.v1"),
            receipt_status=(
                "FROZEN_APPEND_ONLY_V16R2R6_MALFORMED_SOURCE_REJECTED__"
                "V16R2R7_ONLY"),
        )
        seventh_receipts = seal_prior_malformed_namespace(
            failed_outputs=SEVENTH_FAILED_OUTPUTS,
            rejection_path=SEVENTH_REJECTION,
            supersession_path=SEVENTH_SUPERSESSION,
            predecessor_namespace="v16r2r7_semantic_source",
            successor_namespace="v16r2r8_semantic_source",
            receipt_schema=(
                "cm2.c79g.v16r2r7-to-v16r2r8."
                "semantic-source-rejection-supersession.v1"),
            receipt_status=(
                "FROZEN_APPEND_ONLY_V16R2R7_MALFORMED_SOURCE_REJECTED__"
                "V16R2R8_ONLY"),
        )
        eighth_receipts = seal_prior_malformed_namespace(
            failed_outputs=EIGHTH_FAILED_OUTPUTS,
            rejection_path=EIGHTH_REJECTION,
            supersession_path=EIGHTH_SUPERSESSION,
            predecessor_namespace="v16r2r8_semantic_source",
            successor_namespace=SUCCESSOR_NAMESPACE,
            receipt_schema=(
                "cm2.c79g.v16r2r8-to-v16r2r9."
                "semantic-source-rejection-supersession.v1"),
            receipt_status=(
                "FROZEN_APPEND_ONLY_V16R2R8_MALFORMED_SOURCE_REJECTED__"
                "V16R2R9_ONLY"),
        )
        global PRIOR_SUPERSESSION, ACTIVE_ANCHOR_FILE_PIN
        global ACTIVE_ANCHOR_OBJECT_PIN, V16_SUPERSESSION_FILE_PIN
        global V16_SUPERSESSION_OBJECT_PIN
        PRIOR_SUPERSESSION = EIGHTH_SUPERSESSION
        V16_SUPERSESSION_FILE_PIN = sha(supersession_raw)
        V16_SUPERSESSION_OBJECT_PIN = supersession.get("object_sha256")
        active_anchor = seal_active_predecessor_anchor()
        ACTIVE_ANCHOR_FILE_PIN = active_anchor["file_sha256"]
        ACTIVE_ANCHOR_OBJECT_PIN = active_anchor["object_sha256"]
        prior_receipts = {
            "first": first_receipts,
            "second": second_receipts,
            "third": third_receipts,
            "fourth": fourth_receipts,
            "fifth": fifth_receipts,
            "sixth": sixth_receipts,
            "seventh": seventh_receipts,
            "eighth": eighth_receipts,
            "active_anchor": active_anchor,
        }

        source_raw: dict[str, bytes] = {}
        source_hashes: dict[str, str] = {}
        for role, path in V15_SOURCES.items():
            raw = read_stable(path)
            actual = sha(raw)
            if actual != V15_SOURCE_SHA256[role]:
                raise RuntimeError(f"held source hash drift for {role}: {actual}")
            source_raw[role] = raw
            source_hashes[role] = actual

        generated: dict[str, bytes] = {}
        patch_report: dict[str, Any] = {}
        for role, raw in source_raw.items():
            text = raw.decode("utf-8")
            # Parse before editing to make the held-byte assumption explicit.
            ast.parse(text, filename=str(V15_SOURCES[role]))
            patched, ast_count, ast_changes = semantic_ast_patch(text, role)
            patched, graph_count, graph_changes = active_graph_patch(patched, role)
            patched, token_count = token_namespace_rewrite(patched)
            patched = insert_successor_anchor(patched)
            patched = add_compatibility_flags(patched, role)
            generated[role] = (patched + ("" if patched.endswith("\n") else "\n")).encode("utf-8")
            patch_report[role] = {
                "ast_fixed_span_count": ast_count,
                "ast_fixed_span_labels": ast_changes,
                "active_graph_fixed_span_count": graph_count,
                "active_graph_fixed_span_labels": graph_changes,
                "token_fixed_span_count": token_count,
            }

        installed: dict[str, Any] = {}
        for role, raw in generated.items():
            action = install_o_excl(TARGETS[role], raw, mode=0o664)
            installed[role] = {"path": str(TARGETS[role].relative_to(ROOT)), "action": action}

        validation = {role: validate_source(raw, role) for role, raw in generated.items()}
        # Re-read all targets and require byte identity.  This also catches a
        # concurrent replacement after O_EXCL installation.
        reread_hashes = {role: sha(read_stable(TARGETS[role])) for role in TARGETS}
        if reread_hashes != {role: row["sha256"] for role, row in validation.items()}:
            raise RuntimeError("installed source changed during final identity check")

        report = {
            "schema": "cm2.c79g.v16r2.semantic-source-regenerator.v1",
            "status": "V16R2_EXECUTABLE_SOURCE_REGENERATED__DRAFT_RUNTIME_DISABLED__NO_AUTHORITY",
            "input_source_hashes": source_hashes,
            "frozen_v16_rejection": {
                "path": str(V16_REJECTION.relative_to(ROOT)),
                "file_sha256": sha(rejection_raw),
                "object_sha256": rejection.get("object_sha256"),
            },
            "frozen_v16_supersession": {
                "path": str(V16_SUPERSESSION.relative_to(ROOT)),
                "file_sha256": sha(supersession_raw),
                "object_sha256": supersession.get("object_sha256"),
            },
            "prior_malformed_namespace_receipts": prior_receipts,
            "patch_report": patch_report,
            "installed": installed,
            "validation": validation,
            "reread_hashes": reread_hashes,
            "manifest_created": False,
            "outer_created": False,
            "runtime_surface_created": False,
            "formal_global_closure_credit": 0,
            "D02_unlock": False,
            "runtime_authorized": False,
            "independent_reviewer_34_of_34": "NOT_RUN_BY_THIS_TOOL",
        }
        report["object_sha256"] = sha(
            json.dumps(report, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()
        )
        print(json.dumps(report, ensure_ascii=False, sort_keys=True))
        return 0
    except Exception as exc:
        print(json.dumps({
            "schema": "cm2.c79g.v16r2.semantic-source-regenerator.failure.v1",
            "status": "FAIL_CLOSED_NO_SOURCE_AUTHORITY",
            "error_type": type(exc).__name__,
            "error": str(exc),
            "formal_global_closure_credit": 0,
            "D02_unlock": False,
            "runtime_authorized": False,
        }, ensure_ascii=False, sort_keys=True))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
