#!/usr/bin/env python3
"""Second, dependency-reduced audit for the C43 owner-eligible subset.

This v2 does not import or execute the C43 producer, the v1 auditor, either
C43B0 pilot/planner, or any candidate-generated code.  It derives the five
post-C42 sole-deficit sources in a fresh pass over frozen C41/C42 ledgers,
recomputes adaptive routing from frozen lower mathematical primitives, rebuilds
global 91,879-row incidence and every representative/reflected restriction,
then reconstructs all 862 Kraft rows and the 76,832 census.  It never installs
a C43 pointer or authority seal.
"""

from __future__ import annotations

import argparse
import ast
import copy
from collections import Counter
import ctypes
import errno
from fractions import Fraction as Q
import gzip
import hashlib
import json
import os
from pathlib import Path
import re
import secrets
import stat
import subprocess
import sys
import tempfile
from typing import Any, Callable


sys.dont_write_bytecode = True
if hasattr(sys, "set_int_max_str_digits"):
    sys.set_int_max_str_digits(0)

SELF = Path(__file__).resolve()
ROOT = SELF.parent.parent
DELIVERABLES = SELF.parent
RUNTIME = ROOT / ".cm2-runtime"
CANDIDATE_ROOT = RUNTIME / "candidates"
AUDIT_ROOT = RUNTIME / "audit"
sys.path.insert(0, str(DELIVERABLES))

from flint import arb, fmpq

import cm2_round306c41_d02_lower_strata_depth3_closure_v1 as c41
SCHEMA = (
    "cm2.round306c43.d02-sole-deficit-owner-closure."
    "independent-audit.v2"
)
C43_AUDIT_TOKEN = (
    "c43-independent-audit-v2-20260811T121500Z-owner-subset-f1"
)
CANDIDATE_SCHEMA = "cm2.round306c43.d02-sole-deficit-owner-closure.v1"
PRODUCER = DELIVERABLES / (
    "cm2_round306c43_d02_sole_deficit_owner_closure_v1.py"
)

EXPECTED_PRODUCER_SOURCE = (
    "a279b3cb7ff4b7ec7d8f11f097971acf51a510087a796eab60b73cf139c331f4"
)
EXPECTED_CANDIDATE_OBJECT = (
    "79831178f4450c41540b7ff0f51bde96e61517cbc36a2287efbf0a100cba5bbc"
)
EXPECTED_CANDIDATE_STATUS = (
    "FORMAL_PRODUCER_PASS_C43_OWNER_ELIGIBLE_SUBSET_592_715__"
    "578_PAIRED__1146_UNRESOLVED__PENDING_INDEPENDENT_C43_AUDIT"
)
EXPECTED_RESULT_FILE = (
    "76e367a7e02d5d4fb568e11e85c1facb5a24ce3dd522448bebf66c3ec6e5df07"
)
EXPECTED_MANIFEST_FILE = (
    "8bc3b4259f7a600260344436cfc337621c532b44514866ed9fb8425a378390ff"
)
EXPECTED_RECEIPT_OBJECT = (
    "96ba926d2e20db3c2d9905757736f6a3c0eac4e4dd471f911b38caef4ee0e215"
)
EXPECTED_RECEIPT_FILE = (
    "38761997cdf8df6f6f1a7b1aecffa5e165ea8af4139a28a329bc544e88489263"
)
EXPECTED_RECEIPT_STATUS = (
    "FORMAL_PRODUCER_PASS_C43_RECEIPT__PENDING_INDEPENDENT_C43_AUDIT__"
    "NO_AUTHORITY"
)
EXPECTED_INVOCATION = "c43-formal-producer-20260811T082400Z-f1"
EXPECTED_CANDIDATE_TOKEN = (
    "c43-sole-deficit-owner-closure-20260811T082400Z-f1"
)
EXPECTED_CANDIDATE = CANDIDATE_ROOT / EXPECTED_CANDIDATE_TOKEN
EXPECTED_RECEIPT = (
    AUDIT_ROOT / EXPECTED_CANDIDATE_TOKEN / "execution_receipt.json"
)

EXPECTED_C41_SOURCE = (
    "3fbf6cec247903d6e6ba147d4d06e912638b1472b74adc8311323c554e6e5bde"
)
EXPECTED_C42_TX_AUDITOR_SOURCE = (
    "a37bf76da4674831c90d4e5839e7134b7ebfd9167a0a60840996a331039a06e2"
)
EXPECTED_C42_OBJECT = (
    "a50914a266aff3396054d7f16e91d69db7fa735ad15f01cbf07eee8e708d99d2"
)
EXPECTED_C42_AUDIT_OBJECT = (
    "85a7cd719cee9dceb1763135f74d50bcf28f78ff2426e65996b975b1def7790c"
)
EXPECTED_C42_SEAL_OBJECT = (
    "b321552768a6aeae6c1d229e52b61ca0b4420314234e02e98366153d4156d460"
)
EXPECTED_C42_RECEIPT_OBJECT = (
    "c5f2eb78a0d9d717326bc57fb14df823ab3c5181e3e613a0327425c5e33e784e"
)
EXPECTED_C41_OBJECT = (
    "b7e47a4ca9d6f4bb1fee10e78877850d5070f6d3c2b06bb0234fbabdaa2b7b24"
)
EXPECTED_C41_AUDIT_OBJECT = (
    "44061ec6e26108692fe6e635e9e666cca0b11c66f00384eab539be08f66fe877"
)
EXPECTED_C41_RECEIPT_OBJECT = (
    "39f1c6dadcf21a428174520b5a1aa4d072a57c73ffd9c9b04d2c3d639d94fed9"
)
EXPECTED_C41_MANIFEST = (
    "86e10532d63269cd0fdd58d541b1984522e9718f4613a5dc83211fe84eb258ba"
)
EXPECTED_C42_MANIFEST = (
    "ce1b6260b26a901a9dda3cfbd94eba5a752b5188d6bdbe7c7d3cd7a4d3f7d058"
)
EXPECTED_C41_TOKEN_FILE = (
    "9e4f2d9c02c1f3e56639d69c971ccc7846ba229f87723e878f101730df3dd1a9"
)
EXPECTED_C41_AUDIT_TOKEN_FILE = (
    "f8a9a0bf69169eba05ef3bec1db7e924de4b06b4ab61c97693b2919effd9c86c"
)
EXPECTED_C41_RECEIPT_FILE = (
    "4500c6c38d1e34002cb3384f0c0c17623c93df6fb46ea7a12229e41ed6cb1dc8"
)
EXPECTED_C41_AUDIT_FILE = (
    "6a800959a90c227d587b82c6246f60123483471f61dcf6a5de4da5381fee4b1e"
)

C41_TOKEN = "c41-lower-strata-depth3-20260811T023804Z-f997365c91559599"
C41_AUDIT_TOKEN = "c41-independent-audit-20260811T031547Z-ab94d420c43c94cd"
C42_TOKEN = "c42-p391-formal-producer-20260811T044500Z-f1"
C42_AUDIT_TOKEN = "c42-independent-audit-20260811T052900Z-p391-f1"
C42_RELEASE = "c42-f1-authority-install-a50914a266af-85a7cd719cee-v1"
C41_DIR = CANDIDATE_ROOT / C41_TOKEN
C42_DIR = CANDIDATE_ROOT / C42_TOKEN
C42_INSTALL_RECEIPT = AUDIT_ROOT / C42_RELEASE / "installation_receipt.json"

EXPECTED_C42_FILES = {
    "candidate_pointer": (
        RUNTIME / "c42-current-token",
        "fbc5dd3c55bfdd3098ed34ae09ae633a9526a9c9cc6f40b3d87b5669b2ea7f07",
    ),
    "audit_pointer": (
        RUNTIME / "c42-current-audit-token",
        "59aca53c4c35260801b3c559648c88ee974db01ae950f045a5e5aecd64aa36e5",
    ),
    "authority_seal": (
        RUNTIME / "c42-current-authority-seal",
        "0e5a76059b2c9407340d88e07f4fcc356d376f5c24b7173e6b95fd5e06bc312d",
    ),
    "installation_receipt": (
        C42_INSTALL_RECEIPT,
        "3599494ff330a367a6c27ee57c19c01e86626428871d014c9153f290fdfc407f",
    ),
    "candidate_result": (
        C42_DIR / "result.json",
        "f029c3ce6af33e2f93c33b4155286f60bfafecd724720a598b103ca3c263ccb0",
    ),
    "candidate_manifest": (
        C42_DIR / "root_manifest.sha256",
        "ce1b6260b26a901a9dda3cfbd94eba5a752b5188d6bdbe7c7d3cd7a4d3f7d058",
    ),
    "producer_receipt": (
        AUDIT_ROOT / C42_TOKEN / "execution_receipt.json",
        "5a14c48b028dd20951d02659f9d9655f5718a13e69d2811ee823d78c38530a55",
    ),
    "independent_audit": (
        AUDIT_ROOT / C42_AUDIT_TOKEN / "independent_audit.json",
        "d60bb3c8f79f989df776effa4616ec170097a018547b1f4c929ad068c11138d3",
    ),
}

EXPECTED_TARGETS: dict[int, dict[str, str]] = {
    97: {
        "descendant_path": "111111111",
        "c40_leaf_id": "c40-leaf:d2f84a6eacae6bace954ddd09130d12687d4465ce89316827d35637e0d58febf",
        "c40_row_sha256": "f2e1f153deb87534f1cfa21e3131363c62dbb18eda2054b4991b4017d58b9510",
        "c41_ambient_row_sha256": "2db22144ca16f31dd528835a879e38bf4362c8c7a9b6397c0a29a5f8c92b5767",
        "c41_parent_row_sha256": "6e309c2576f5862630465bb81fa38af3bba0b650852ad111b7fbf0c1c7d67762",
        "c42_parent_row_sha256": "b0f74ff6812a75e9d69bf2e11cfc99ec1e9f8eb43c0ab527152ce4b658d9aa3e",
        "raw_classification": "UNRESOLVED_C40_COLLISION2_WALL_ENDPOINT",
        "residual_classification": "UNRESOLVED_C41_COLLISION2_WALL_ENDPOINT_OUTER",
    },
    211: {
        "descendant_path": "111111111",
        "c40_leaf_id": "c40-leaf:7e0b721bd80687cd3bd1f8fffe0369f3c0ebc7273e3cf941178a9d7a8fc5edb3",
        "c40_row_sha256": "1f8a4094d17cd5f5f888116098c03f97ad62a4df71e44e024930a020df45432a",
        "c41_ambient_row_sha256": "ddc554f00da31c5c4b21ec51de3a49eb0f62ed984f2843ae673bf34ce3b06fc4",
        "c41_parent_row_sha256": "04b77d56f4e96466504972ed3730b7a9bf92364cd6b2f8b64acecdb92cc64600",
        "c42_parent_row_sha256": "bd464fa2e1cefd063860022026758026ba7cc8fbfb399fa323fb2f36f7762064",
        "raw_classification": "UNRESOLVED_C40_COLLISION2_WALL_ENDPOINT",
        "residual_classification": "UNRESOLVED_C41_COLLISION2_WALL_ENDPOINT_OUTER",
    },
    592: {
        "descendant_path": "000000000",
        "c40_leaf_id": "c40-leaf:e34e9616160fabac64fde47c92755efdc8f1f2d93e7ac798f2ff3eab2947f33b",
        "c40_row_sha256": "c804684bb3961f7b60134e7d168488ca0dc30f1fb49bec612b3e301e91d2ab89",
        "c41_ambient_row_sha256": "bf089245fa0f96196014cbd425b0b3d3e265b0350477779f731b32dc05f8985e",
        "c41_parent_row_sha256": "2ba14f7e7e8b89c548ffbafa81168770f53780d287eeeee2396938ceb8fa6e99",
        "c42_parent_row_sha256": "cbb5a195348f179a6e243af79faff1cb1abf7da0d05f76ec63a1b464ce5d3631",
        "raw_classification": "UNRESOLVED_C39_C1_ENHANCED_W_SIDE_COLLISION1_OUTGOING_STATE",
        "residual_classification": "UNRESOLVED_C41_C1_OUTGOING_H1_FACTOR_OUTER",
    },
    664: {
        "descendant_path": "010101010",
        "c40_leaf_id": "c40-leaf:c2e98c22c8d0a87abbd19189d6262a9c81c8a88322ae18ff91ee8ceb73bca4a3",
        "c40_row_sha256": "498cdf8a6d00f7c2b9839eec811710643bf77615268023bf25cc57b7e2d1ea7e",
        "c41_ambient_row_sha256": "395f8ef977aece344cb2e9b6950c4cc5734e3795aa34a7ffdccc73c6616601ba",
        "c41_parent_row_sha256": "d93a77969d0452e5fdcba3e7a42cea4303725f3ba5333335828b7ad8bee05244",
        "c42_parent_row_sha256": "e992c0ff2e0a005bacf10de761ab6ea14b093932d3764353f378df1f71c81fc0",
        "raw_classification": "UNRESOLVED_C39_C1_ENHANCED_W_SIDE_COLLISION1_OUTGOING_STATE",
        "residual_classification": "UNRESOLVED_C41_C1_OUTGOING_H1_FACTOR_OUTER",
    },
    715: {
        "descendant_path": "101010101",
        "c40_leaf_id": "c40-leaf:d2768eebbaf3c62ad68b42b636552586b60875f79121e40422e31bc595869459",
        "c40_row_sha256": "15796e01b7e552f453ae3e9ac4fe145ca1e35c393a9694a68a46aba3b2884c5a",
        "c41_ambient_row_sha256": "24b8a1114e0bda5b0ff4d88b8f7daddfd6b009724fb2e418ea9ac52de42df349",
        "c41_parent_row_sha256": "9c26d3272b8d541ac5856b7f674a44007fea3eb62ac881d8a7d1aa0653cf3354",
        "c42_parent_row_sha256": "dda2b4afca3fe326ac76c48b6e96ef68fda9c04da368d6a6b468fc2fab866920",
        "raw_classification": "UNRESOLVED_C39_C1_ENHANCED_W_SIDE_COLLISION1_OUTGOING_STATE",
        "residual_classification": "UNRESOLVED_C41_C1_OUTGOING_H1_FACTOR_OUTER",
    },
}

ZERO_SURFACE_CLASSES = {
    "UNRESOLVED_C41_C1_OUTGOING_H1_FACTOR_OUTER":
        ("c1_h1_surface_outers", "c1_h1_surface_outer_id", 872),
    "UNRESOLVED_C41_COLLISION2_WALL_ENDPOINT_OUTER":
        ("c2_surface_outers", "c2_surface_outer_id", 2482),
    "UNRESOLVED_C41_COLLISION2_EVALUATION_EXCEPTION_OUTER":
        ("c2_surface_outers", "c2_surface_outer_id", 89),
}
ZERO_SURFACE_METADATA = {
    "UNRESOLVED_C41_C1_OUTGOING_H1_FACTOR_OUTER":
        ("C1_OUTGOING_H1_FACTOR", 6),
    "UNRESOLVED_C41_COLLISION2_WALL_ENDPOINT_OUTER":
        ("C2_WALL_ENDPOINT", 4),
    "UNRESOLVED_C41_COLLISION2_EVALUATION_EXCEPTION_OUTER":
        ("C2_EVALUATION_EXCEPTION", 8),
}
PLANNER_TASK_SCHEMA = (
    "cm2.round306c43b0.d02-zero-surface-shard-plan.v1.task"
)
PRIORITY_ORDER = {
    "WHOLE_PAIR_GAIN": 0,
    "C2_EVALUATION_EXCEPTION": 1,
    "C2_WALL_ENDPOINT": 2,
    "C1_OUTGOING_H1_FACTOR": 3,
}

PRIMITIVE_SOURCE_PINS = {
    "C41_router": (
        Path(c41.__file__).resolve(), EXPECTED_C41_SOURCE,
    ),
    "C38_geometry": (
        Path(c41.c38.__file__).resolve(),
        "8eab87d69fb4e1995df87be7acb387db19d1b81e17040fe6116794bddd4a830d",
    ),
    "C39_graph_router": (
        Path(c41.c39.__file__).resolve(),
        "873a84cb150efc5649ffb5822457c510ab45c32f3e16a48914c8674dc93c0aae",
    ),
    "C40_endpoint_router": (
        Path(c41.c40.__file__).resolve(),
        "9ec1ad4df72b0f25b646d17a43e1186188ace97d2e76ac480c1c2a476fac5f57",
    ),
    "Round166_classifier": (
        Path(c41.c38.round166.__file__).resolve(),
        "6479a78249a717169dea55ecabae98c05f240ea323fa0370037d43339158ae7c",
    ),
    "Round185_refinement": (
        Path(c41.round185.__file__).resolve(),
        "7b48f3ee3417fcfdf5ef6c852e0ab591eb849b357e704e46ee3aaa259d20acc2",
    ),
}

TARGET_PAIRS = (97, 211, 592, 664, 715)
ELIGIBLE = (592, 715)
BLOCKED = (97, 211, 664)
C42_PAIR = 391
SOURCE_FRACTION = Q(1, 512)
EXPECTED_PROFILES = {
    97: (3, 2, 2), 211: (3, 2, 2), 592: (2, 1, 1),
    664: (4, 3, 3), 715: (2, 1, 1),
}
EXPECTED_CLASSES = {
    97: "EXCLUDED_C40_COLLISION2_OWNER_MISMATCH",
    211: "EXCLUDED_C40_COLLISION2_OWNER_MISMATCH",
    592: "EXCLUDED_C39_C1_ENHANCED_W_SIDE_COLLISION1_WORD_MISMATCH",
    664: "EXCLUDED_C39_C1_ENHANCED_W_SIDE_COLLISION1_WORD_MISMATCH",
    715: "EXCLUDED_C39_C1_ENHANCED_W_SIDE_COLLISION1_WORD_MISMATCH",
}

INVENTORY = (
    "C43_SUBSET_CLOSURE.lock",
    "adaptive_splits.jsonl.gz",
    "closed_leaf_certificates.jsonl.gz",
    "exact_sources.jsonl.gz",
    "internal_strata_incidence.jsonl.gz",
    "reflection_transport.jsonl.gz",
    "representative_parent_conservation.jsonl.gz",
    "result.json",
    "root_manifest.sha256",
    "round144_census.json",
    "source_corner_owner_incidence.jsonl.gz",
    "source_face_owner_incidence.jsonl.gz",
    "source_preflight.jsonl.gz",
)
LOCK_BYTES = (
    b"C43 is a producer-only non-authority candidate. It grants credit only "
    b"to owner-eligible pairs 592 and 715. Pairs 97, 211, and 664 remain "
    b"canonical residual-owner blockers with zero credit. The candidate "
    b"cannot install C43 pointers. D02 remains blocked by 1146 complete "
    b"R1648 continuations; D03, D04, Gate5 promotion, and every CM2 claim "
    b"remain unauthorized.\n"
)

LEDGERS = {
    "preflight": (
        "source_preflight", "source_preflight.jsonl.gz", 5,
        "PAIR_INDEX_ASCENDING", "source_preflight_id", "c43-preflight:",
    ),
    "sources": (
        "exact_sources", "exact_sources.jsonl.gz", 2,
        "PAIR_INDEX_ASCENDING", "exact_source_id", "c43-source:",
    ),
    "splits": (
        "adaptive_splits", "adaptive_splits.jsonl.gz", 2,
        "PAIR_INDEX_THEN_PARENT_PATH", "adaptive_split_id", "c43-split:",
    ),
    "leaves": (
        "closed_leaf_certificates", "closed_leaf_certificates.jsonl.gz", 8,
        "PAIR_INDEX_ORIENTATION_PATH", "closed_leaf_certificate_id",
        "c43-leaf:",
    ),
    "reflection": (
        "reflection_transport", "reflection_transport.jsonl.gz", 4,
        "PAIR_INDEX_REPRESENTATIVE_PATH", "reflection_transport_id",
        "c43-reflection:",
    ),
    "internal": (
        "internal_strata_incidence", "internal_strata_incidence.jsonl.gz", 2,
        "PAIR_INDEX_SPLIT_PARENT_PATH", "internal_strata_incidence_id",
        "c43-internal:",
    ),
    "faces": (
        "source_face_owner_incidence",
        "source_face_owner_incidence.jsonl.gz", 8,
        "PAIR_INDEX_FACE_ENUM", "source_face_owner_incidence_id", "c43-face:",
    ),
    "corners": (
        "source_corner_owner_incidence",
        "source_corner_owner_incidence.jsonl.gz", 8,
        "PAIR_INDEX_CORNER_ENUM", "source_corner_owner_incidence_id",
        "c43-corner:",
    ),
    "parents": (
        "representative_parent_conservation",
        "representative_parent_conservation.jsonl.gz", 862,
        "PAIR_INDEX_ASCENDING", None, None,
    ),
}

HEX64 = re.compile(r"[0-9a-f]{64}\Z")


class Reject(RuntimeError):
    """Semantic audit rejection."""


class AuditCommittedError(RuntimeError):
    """A post-rename durability/reporting error; publication already occurred."""


AUDIT_COMMIT_OBSERVED = False


def need(value: bool, label: str) -> None:
    if type(value) is not bool or not value:
        raise Reject(label)


def canonical(value: Any) -> bytes:
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=True,
        allow_nan=False,
    ).encode("ascii")


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def bytes_sha(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def file_sha(path: Path) -> str:
    return bytes_sha(stable_read(path, 256 << 20, "sha256:" + str(path)))


def qstr(value: Any) -> str:
    value = Q(value)
    return str(value.numerator) if value.denominator == 1 else str(value)


def strict_json(raw: bytes, label: str) -> dict[str, Any]:
    need(raw == raw.strip() + b"\n", "terminal newline:" + label)

    def pairs(items: list[tuple[str, Any]]) -> dict[str, Any]:
        need(len(items) == len({key for key, _value in items}),
             "duplicate JSON key:" + label)
        return dict(items)

    value = json.loads(
        raw,
        object_pairs_hook=pairs,
        parse_float=lambda _value: (_ for _ in ()).throw(
            Reject("float JSON:" + label)
        ),
        parse_constant=lambda _value: (_ for _ in ()).throw(
            Reject("constant JSON:" + label)
        ),
    )
    need(type(value) is dict and canonical(value) + b"\n" == raw,
         "canonical JSON:" + label)
    return value


def lexical_no_symlinks(path: Path, label: str) -> None:
    absolute = path.absolute()
    need(absolute == ROOT or ROOT in absolute.parents,
         "workspace boundary:" + label)
    cursor = ROOT
    need(stat.S_ISDIR(os.lstat(cursor).st_mode)
         and not stat.S_ISLNK(os.lstat(cursor).st_mode),
         "real workspace root:" + label)
    for part in absolute.relative_to(ROOT).parts:
        cursor /= part
        info = os.lstat(cursor)
        need(not stat.S_ISLNK(info.st_mode),
             "no symlink path component:" + label)


def stable_read(path: Path, maximum: int, label: str) -> bytes:
    path = path.absolute()
    lexical_no_symlinks(path.parent, label + " parent")
    flags = os.O_RDONLY | getattr(os, "O_CLOEXEC", 0) \
        | getattr(os, "O_NOFOLLOW", 0)
    descriptor = os.open(path, flags)
    try:
        before = os.fstat(descriptor)
        need(
            stat.S_ISREG(before.st_mode) and before.st_nlink == 1
            and 0 < before.st_size <= maximum,
            "fd regular single-link bounded:" + label,
        )
        chunks = []
        remaining = maximum + 1
        while remaining:
            block = os.read(descriptor, min(1 << 20, remaining))
            if not block:
                break
            chunks.append(block)
            remaining -= len(block)
        raw = b"".join(chunks)
        after = os.fstat(descriptor)
        path_after = os.stat(path, follow_symlinks=False)
        fingerprint = lambda value: (
            value.st_dev, value.st_ino, value.st_mode, value.st_nlink,
            value.st_size, value.st_mtime_ns, value.st_ctime_ns,
        )
        need(
            fingerprint(before) == fingerprint(after)
            == fingerprint(path_after)
            and len(raw) == before.st_size <= maximum,
            "fd-bound stable read:" + label,
        )
        return raw
    finally:
        os.close(descriptor)


def self_closed(value: dict[str, Any], field: str, label: str) -> None:
    claimed = value.get(field)
    semantic = copy.deepcopy(value)
    semantic.pop(field, None)
    need(
        type(claimed) is str and HEX64.fullmatch(claimed) is not None
        and claimed == digest(semantic),
        "self hash:" + label,
    )


def row_closed(row: dict[str, Any], id_field: str | None,
               prefix: str | None, label: str) -> None:
    semantic = copy.deepcopy(row)
    row_sha = semantic.pop("row_sha256", None)
    need(row_sha == digest(semantic), "row hash:" + label)
    if id_field is not None:
        claimed = semantic.pop(id_field, None)
        need(claimed == prefix + digest(semantic), "domain id:" + label)


def no_producer_import() -> None:
    """Reject every forbidden C43 implementation dependency by AST and state."""
    forbidden = {
        PRODUCER.stem,
        "cm2_round306c43_d02_sole_deficit_owner_closure_independent_auditor_v1",
        "cm2_round306c43b0_d02_sole_deficit_adaptive_pilot_v1",
        "cm2_round306c43b0_d02_zero_surface_shard_planner_v1",
    }
    need(forbidden.isdisjoint(sys.modules),
         "forbidden C43 implementation in sys.modules")
    tree = ast.parse(
        stable_read(SELF, 16 << 20, "C43 v2 auditor AST").decode("utf-8")
    )
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            need(all(alias.name not in forbidden for alias in node.names),
                 "forbidden C43 direct import")
        if isinstance(node, ast.ImportFrom):
            need(node.module not in forbidden,
                 "forbidden C43 from-import")


def no_c43_pointer() -> None:
    for name in (
        "c43-current-token", "c43-current-audit-token",
        "c43-current-authority-seal",
    ):
        path = RUNTIME / name
        try:
            value = os.lstat(path)
        except FileNotFoundError:
            continue
        if stat.S_ISLNK(value.st_mode):
            try:
                target = os.readlink(path)
            except OSError as error:
                raise Reject("C43 pointer lstat/readlink:" + name) from error
            raise Reject(
                "C43 pointer absent (symlink present):" + name + ":" + target
            )
        raise Reject("C43 pointer absent (entry present):" + name)


def close_expected(semantic: dict[str, Any], id_field: str | None,
                   prefix: str | None) -> dict[str, Any]:
    row = copy.deepcopy(semantic)
    if id_field is not None:
        row[id_field] = prefix + digest(row)
    row["row_sha256"] = digest(row)
    return row


def capture_candidate(directory: Path, *, enforce_pins: bool = True) \
        -> dict[str, Any]:
    directory = directory.absolute()
    lexical_no_symlinks(directory, "C43 candidate path")
    if enforce_pins:
        need(directory == EXPECTED_CANDIDATE.absolute(),
             "exact frozen C43 candidate path")
    mode = directory.lstat().st_mode
    need(stat.S_ISDIR(mode) and not directory.is_symlink(),
         "real C43 candidate directory")
    names = tuple(sorted(path.name for path in directory.iterdir()))
    need(names == INVENTORY, "exact C43 inventory")
    raw = {
        name: stable_read(
            directory / name,
            256 << 20 if name.endswith(".gz") else 32 << 20,
            "C43 candidate:" + name,
        )
        for name in names
    }
    if enforce_pins:
        need(bytes_sha(raw["result.json"]) == EXPECTED_RESULT_FILE,
             "pinned C43 result bytes")
        need(bytes_sha(raw["root_manifest.sha256"]) == EXPECTED_MANIFEST_FILE,
             "pinned C43 manifest bytes")
    expected_manifest = b"".join(
        (bytes_sha(raw[name]) + "  " + name + "\n").encode("ascii")
        for name in names if name != "root_manifest.sha256"
    )
    need(raw["root_manifest.sha256"] == expected_manifest,
         "full C43 manifest replay")
    result = strict_json(raw["result.json"], "C43 result")
    self_closed(result, "object_sha256", "C43 result")
    if enforce_pins:
        need(
            result.get("object_sha256") == EXPECTED_CANDIDATE_OBJECT
            and result.get("status") == EXPECTED_CANDIDATE_STATUS
            and result.get("producer_source_sha256") == EXPECTED_PRODUCER_SOURCE,
            "pinned C43 result object/status/source",
        )
    rows: dict[str, list[dict[str, Any]]] = {}
    for key, (descriptor_key, filename, count, order, id_field, prefix) \
            in LEDGERS.items():
        descriptor = result["ledgers"][descriptor_key]
        need(
            descriptor["filename"] == filename
            and descriptor["row_count"] == count
            and descriptor["order"] == order
            and descriptor["size"] == len(raw[filename])
            and descriptor["sha256"] == bytes_sha(raw[filename]),
            "ledger descriptor:" + key,
        )
        try:
            plain = gzip.decompress(raw[filename])
        except Exception as error:
            raise Reject("gzip decode:" + key) from error
        need(plain.endswith(b"\n") and b"\r" not in plain,
             "ledger line framing:" + key)
        parsed = []
        sequence = hashlib.sha256()
        for ordinal, line in enumerate(plain.splitlines(keepends=True)):
            row = strict_json(line, f"{key}:{ordinal}")
            row_closed(row, id_field, prefix, f"{key}:{ordinal}")
            sequence.update((row["row_sha256"] + "\n").encode("ascii"))
            parsed.append(row)
        need(
            len(parsed) == count
            and sequence.hexdigest()
            == descriptor["row_hash_line_sequence_sha256"],
            "ledger row sequence:" + key,
        )
        rows[key] = parsed
    census = strict_json(raw["round144_census.json"], "round144 census")
    self_closed(census, "census_object_sha256", "round144 census")
    need(raw["C43_SUBSET_CLOSURE.lock"] == LOCK_BYTES,
         "exact C43 nonpromotion lock")
    return {
        "directory": directory,
        "raw": raw,
        "result": result,
        "rows": rows,
        "census": census,
        "manifest_sha256": bytes_sha(raw["root_manifest.sha256"]),
    }


def capture_receipt(path: Path, candidate: dict[str, Any], invocation: str,
                    *, enforce_pins: bool = True) -> dict[str, Any]:
    path = path.absolute()
    lexical_no_symlinks(path, "C43 receipt path")
    if enforce_pins:
        need(path == EXPECTED_RECEIPT.absolute(),
             "exact frozen C43 receipt path")
    raw = stable_read(path, 8 << 20, "C43 receipt")
    if enforce_pins:
        need(bytes_sha(raw) == EXPECTED_RECEIPT_FILE, "pinned receipt bytes")
    value = strict_json(raw, "C43 receipt")
    self_closed(value, "receipt_object_sha256", "C43 receipt")
    if enforce_pins:
        need(
            value.get("receipt_object_sha256") == EXPECTED_RECEIPT_OBJECT
            and value.get("status") == EXPECTED_RECEIPT_STATUS
            and value.get("InvocationID") == invocation == EXPECTED_INVOCATION
            and value.get("candidate_object_sha256") == EXPECTED_CANDIDATE_OBJECT
            and value.get("root_manifest_sha256") == EXPECTED_MANIFEST_FILE
            and value.get("producer_source_sha256") == EXPECTED_PRODUCER_SOURCE
            and value.get("eligible_pairs") == list(ELIGIBLE)
            and value.get("blocked_zero_credit_pairs") == list(BLOCKED)
            and value.get("producer_output_is_authority") is False
            and value.get("authority_pointer_installed") is False,
            "exact C43 receipt semantics",
        )
        expected_path = str(candidate["directory"].relative_to(ROOT))
        need(value.get("candidate_path") == expected_path,
             "receipt candidate path")
    return value


def validate_source_pins() -> None:
    need(file_sha(PRODUCER) == EXPECTED_PRODUCER_SOURCE,
         "frozen C43 producer source read-only pin")
    for label, (path, expected) in PRIMITIVE_SOURCE_PINS.items():
        need(file_sha(path) == expected, "frozen primitive source:" + label)
    # This is a provenance byte pin only.  v2 never imports or executes it.
    need(file_sha(DELIVERABLES /
         "cm2_round306c42_f1_authority_transaction_independent_auditor_v1.py")
         == EXPECTED_C42_TX_AUDITOR_SOURCE,
         "frozen C42 transaction auditor provenance")


def validate_installed_c41_authority() -> dict[str, Any]:
    token_path = RUNTIME / "c41-current-token"
    audit_token_path = RUNTIME / "c41-current-audit-token"
    token_raw = stable_read(token_path, 256, "C41 current token")
    audit_token_raw = stable_read(
        audit_token_path, 256, "C41 current audit token"
    )
    need(bytes_sha(token_raw) == EXPECTED_C41_TOKEN_FILE
         and token_raw == (C41_TOKEN + "\n").encode("ascii"),
         "installed C41 candidate pointer")
    need(bytes_sha(audit_token_raw) == EXPECTED_C41_AUDIT_TOKEN_FILE
         and audit_token_raw == (C41_AUDIT_TOKEN + "\n").encode("ascii"),
         "installed C41 audit pointer")
    manifest_raw = stable_read(
        C41_DIR / "root_manifest.sha256", 8 << 20, "C41 manifest"
    )
    need(bytes_sha(manifest_raw) == EXPECTED_C41_MANIFEST,
         "installed C41 manifest")
    receipt_path = (
        AUDIT_ROOT / C41_TOKEN / "execution_receipt.json"
    )
    receipt_raw = stable_read(receipt_path, 8 << 20, "C41 receipt")
    need(bytes_sha(receipt_raw) == EXPECTED_C41_RECEIPT_FILE,
         "C41 receipt bytes")
    receipt = strict_json(receipt_raw, "C41 receipt")
    self_closed(receipt, "receipt_object_sha256", "C41 receipt")
    need(
        receipt["schema"]
        == "cm2.round306c41.d02-lower-strata-depth3-closure.v1.execution-receipt"
        and receipt["receipt_object_sha256"] == EXPECTED_C41_RECEIPT_OBJECT
        and receipt["candidate_object_sha256"] == EXPECTED_C41_OBJECT
        and receipt["producer_source_sha256"] == EXPECTED_C41_SOURCE
        and receipt["root_manifest_sha256"] == EXPECTED_C41_MANIFEST
        and receipt["candidate_path"] == str(C41_DIR.relative_to(ROOT)),
        "C41 receipt binding",
    )
    audit_path = (
        AUDIT_ROOT / C41_AUDIT_TOKEN / "independent_audit.json"
    )
    audit_raw = stable_read(audit_path, 32 << 20, "C41 independent audit")
    need(bytes_sha(audit_raw) == EXPECTED_C41_AUDIT_FILE,
         "C41 audit bytes")
    audit = strict_json(audit_raw, "C41 independent audit")
    self_closed(audit, "object_sha256", "C41 independent audit")
    need(
        audit["object_sha256"] == EXPECTED_C41_AUDIT_OBJECT
        and audit["candidate_object_sha256"] == EXPECTED_C41_OBJECT
        and audit["producer_source_sha256"] == EXPECTED_C41_SOURCE
        and audit["candidate_path"] == str(C41_DIR.relative_to(ROOT))
        and audit["status"]
        == "PASS_INDEPENDENT_C41_DEPTH3_CLOSURE_AUDIT__37_OF_37_MUTATIONS_REJECTED",
        "C41 audit binding",
    )
    return {
        "candidate_pointer_sha256": bytes_sha(token_raw),
        "audit_pointer_sha256": bytes_sha(audit_token_raw),
        "manifest_sha256": bytes_sha(manifest_raw),
        "receipt_object_sha256": receipt["receipt_object_sha256"],
        "audit_object_sha256": audit["object_sha256"],
    }


def validate_frozen_manifest(directory: Path, expected_sha256: str,
                             expected_members: int, label: str) -> bytes:
    """Independently parse and replay a strict sorted sha256 manifest."""
    manifest = stable_read(
        directory / "root_manifest.sha256", 8 << 20, label + " manifest"
    )
    need(bytes_sha(manifest) == expected_sha256,
         label + " manifest frozen SHA256")
    lines = manifest.decode("ascii").splitlines()
    need(len(lines) == expected_members, label + " manifest member count")
    members: dict[str, str] = {}
    for line in lines:
        match = re.fullmatch(
            r"([0-9a-f]{64})  ([A-Za-z0-9][A-Za-z0-9_.-]*)", line
        )
        need(match is not None, label + " manifest grammar")
        sha256, name = match.groups()
        need(name not in members and name != "root_manifest.sha256",
             label + " manifest unique safe name")
        members[name] = sha256
    need(list(members) == sorted(members), label + " manifest sort")
    actual = sorted(item.name for item in directory.iterdir())
    need(actual == sorted([*members, "root_manifest.sha256"]),
         label + " exact candidate inventory")
    for name, expected in members.items():
        need(bytes_sha(stable_read(
            directory / name, 512 << 20, label + " member:" + name
        )) == expected, label + " manifest replay:" + name)
    return manifest


def validate_installed_c42_authority() -> dict[str, Any]:
    """Rebuild C42 installed authority without invoking its transaction auditor."""
    raw = {
        label: stable_read(path, 512 << 20, "C42 authority:" + label)
        for label, (path, _sha256) in EXPECTED_C42_FILES.items()
    }
    for label, (_path, expected) in EXPECTED_C42_FILES.items():
        need(bytes_sha(raw[label]) == expected,
             "C42 authority frozen bytes:" + label)
    need(raw["candidate_pointer"] == (C42_TOKEN + "\n").encode("ascii")
         and raw["audit_pointer"] == (C42_AUDIT_TOKEN + "\n").encode("ascii"),
         "C42 exact pointer bytes")
    validate_frozen_manifest(C42_DIR, EXPECTED_C42_MANIFEST, 8, "C42")

    result = strict_json(raw["candidate_result"], "C42 result")
    receipt = strict_json(raw["producer_receipt"], "C42 producer receipt")
    audit = strict_json(raw["independent_audit"], "C42 independent audit")
    install_receipt = strict_json(
        raw["installation_receipt"], "C42 installation receipt"
    )
    seal = strict_json(raw["authority_seal"], "C42 authority seal")
    self_closed(result, "object_sha256", "C42 result")
    self_closed(receipt, "receipt_object_sha256", "C42 producer receipt")
    self_closed(audit, "object_sha256", "C42 independent audit")
    self_closed(
        install_receipt, "installation_receipt_object_sha256",
        "C42 installation receipt",
    )
    self_closed(seal, "authority_seal_object_sha256", "C42 authority seal")
    need(
        result.get("object_sha256") == EXPECTED_C42_OBJECT
        and result.get("status")
        == "FORMAL_PRODUCER_PASS_C42_P391_OWNER_CLOSURE__PENDING_INDEPENDENT_C42_AUDIT"
        and result.get("closure_census", {}).get(
            "whole_terminal_paired_coarse_cell_count") == 574
        and result.get("closure_census", {}).get(
            "whole_terminal_representative_parent_count") == 287
        and result.get("closure_census", {}).get(
            "C34_common_refinement_credit_zero_row_count") == 575
        and result.get("round144_terminal_census", {}).get(
            "UNRESOLVED_R1648_CONTINUATION") == 1150
        and result.get("round144_terminal_census", {}).get(
            "terminal_total") == 76832,
        "C42 result formal census",
    )
    need(
        receipt.get("receipt_object_sha256")
        == "e89f66d0e7636bfa781a6ef7e0309fc1ad00c3215ea699c08b231003e1c39f08"
        and receipt.get("candidate_path") == str(C42_DIR.relative_to(ROOT))
        and receipt.get("candidate_object_sha256") == EXPECTED_C42_OBJECT
        and receipt.get("root_manifest_sha256") == EXPECTED_C42_MANIFEST
        and receipt.get("producer_source_sha256")
        == "4b4e96bcb2c701fd6820a04271e2f02058e3699d980a4bee61d4090b2ce30c78",
        "C42 producer receipt binding",
    )
    attacks = audit.get("attacks")
    need(
        audit.get("object_sha256") == EXPECTED_C42_AUDIT_OBJECT
        and audit.get("candidate_object_sha256") == EXPECTED_C42_OBJECT
        and audit.get("execution_receipt_object_sha256")
        == receipt["receipt_object_sha256"]
        and audit.get("root_manifest_sha256") == EXPECTED_C42_MANIFEST
        and audit.get("status")
        == "PASS_INDEPENDENT_C42_P391_OWNER_CLOSURE_AUDIT__54_OF_54_ATTACKS_FAIL_CLOSED"
        and type(attacks) is dict and len(attacks) == 54
        and all(value is True for value in attacks.values()),
        "C42 independent audit binding and attacks",
    )
    need(
        install_receipt.get("schema")
        == "cm2.round306c42.f1-authority-installation-receipt.v1"
        and install_receipt.get("release_id") == C42_RELEASE
        and install_receipt.get("installation_receipt_object_sha256")
        == EXPECTED_C42_RECEIPT_OBJECT
        and install_receipt.get("bindings", {}).get("objects", {}).get(
            "c42_candidate_object_sha256") == EXPECTED_C42_OBJECT
        and install_receipt.get("bindings", {}).get("objects", {}).get(
            "c42_independent_audit_object_sha256") == EXPECTED_C42_AUDIT_OBJECT
        and install_receipt.get("post_install_census") == {
            "CM2": "NO-GO_FOR_CLAIM",
            "D02": "BLOCKED_BY_1150_COMPLETE_R1648_CONTINUATIONS",
            "UNRESOLVED_R1648_CONTINUATION": 1150,
            "remaining_representatives": 575,
            "whole_terminal_paired_coarse_cells": 574,
            "whole_terminal_representatives": 287,
        },
        "C42 installation receipt reconstruction",
    )
    need(
        seal == {
            "audit_pointer_sha256": EXPECTED_C42_FILES["audit_pointer"][1],
            "audit_token": C42_AUDIT_TOKEN,
            "authority_seal_object_sha256": EXPECTED_C42_SEAL_OBJECT,
            "candidate_object_sha256": EXPECTED_C42_OBJECT,
            "candidate_pointer_sha256": EXPECTED_C42_FILES[
                "candidate_pointer"][1],
            "candidate_token": C42_TOKEN,
            "formal_census_after_commit": {
                "paired_coarse_cells": 574,
                "remaining_representatives": 575,
                "unresolved": 1150,
                "whole_representatives": 287,
            },
            "independent_audit_object_sha256": EXPECTED_C42_AUDIT_OBJECT,
            "installer_source_sha256":
                "66f88bc5913af695691c5ae58be7938f94f3f68a9eeeeed32bcd96b37938c276",
            "receipt_file_sha256": EXPECTED_C42_FILES[
                "installation_receipt"][1],
            "receipt_object_sha256": EXPECTED_C42_RECEIPT_OBJECT,
            "receipt_path": str(C42_INSTALL_RECEIPT.relative_to(ROOT)),
            "release_id": C42_RELEASE,
            "schema": "cm2.round306c42.f1-authority-commit-seal.v1",
            "semantic_commit": {
                "compatibility_pointers_without_this_seal_are_not_authority": True,
                "publication_method":
                    "renameat2_RENAME_NOREPLACE_then_runtime_fsync",
                "this_seal_is_required": True,
            },
            "status": "COMMITTED_C42_F1_AUTHORITY__574_PAIRED__1150_UNRESOLVED",
        },
        "C42 exact authority seal reconstruction",
    )
    return {
        "authority_installed": True,
        "candidate_object_sha256": result["object_sha256"],
        "independent_audit_object_sha256": audit["object_sha256"],
        "authority_seal_object_sha256": seal["authority_seal_object_sha256"],
        "installation_receipt_object_sha256":
            install_receipt["installation_receipt_object_sha256"],
    }


def iter_frozen_ledger(directory: Path, descriptor: dict[str, Any],
                       label: str) -> list[dict[str, Any]]:
    """Decode one frozen ledger without using a C43 parser implementation."""
    need(set(descriptor) == {
        "filename", "order", "row_count", "row_hash_line_sequence_sha256",
        "sha256", "size",
    }, label + ": descriptor shape")
    raw = stable_read(directory / descriptor["filename"], 1 << 30, label)
    need(len(raw) == descriptor["size"]
         and bytes_sha(raw) == descriptor["sha256"],
         label + ": descriptor byte binding")
    try:
        plain = gzip.decompress(raw)
    except Exception as error:
        raise Reject(label + ": gzip decode") from error
    need(plain.endswith(b"\n") and b"\r" not in plain,
         label + ": line framing")
    rows: list[dict[str, Any]] = []
    sequence = hashlib.sha256()
    for ordinal, line in enumerate(plain.splitlines(keepends=True)):
        row = strict_json(line, f"{label}:{ordinal}")
        semantic = copy.deepcopy(row)
        claimed = semantic.pop("row_sha256", None)
        need(claimed == digest(semantic), f"{label}:{ordinal}: row closure")
        sequence.update((claimed + "\n").encode("ascii"))
        rows.append(row)
    need(len(rows) == descriptor["row_count"]
         and sequence.hexdigest()
         == descriptor["row_hash_line_sequence_sha256"],
         label + ": exact count/sequence")
    return rows


def derive_sole_deficit_frontier(
    c41_result: dict[str, Any], c42_parents: list[dict[str, Any]],
) -> tuple[dict[int, dict[str, Any]], list[dict[str, Any]], dict[str, Any]]:
    """Fresh two-pass derivation over raw C41 outers and 91,879 ambient rows."""
    primary: dict[str, dict[str, Any]] = {}
    class_census: Counter[str] = Counter()
    for ledger_name in ("c1_h1_surface_outers", "c2_surface_outers"):
        rows = iter_frozen_ledger(
            C41_DIR, c41_result["ledgers"][ledger_name],
            "C41 raw sole discovery:" + ledger_name,
        )
        for row in rows:
            classification = row.get("residual_classification")
            metadata = ZERO_SURFACE_CLASSES.get(classification)
            if metadata is None or row.get("normalized_surface_count") != 0:
                continue
            expected_ledger, id_field, _count = metadata
            need(
                ledger_name == expected_ledger
                and row.get("normalized_surfaces") == []
                and row.get("carrier_existence_status")
                == "UNRESOLVED_STRATIFIED_SURFACE_OUTER"
                and row.get("certified_carrier_dimension") is None
                and row.get("candidate_intersection_rank_status") is None
                and row.get("ambient_or_whole_parent_credit") == 0
                and row.get("D02_gate_credit") == 0,
                "C41 exact zero-surface outer semantics",
            )
            outer_id = row[id_field]
            need(outer_id not in primary, "C41 unique zero-surface outer")
            category, work_units = ZERO_SURFACE_METADATA[classification]
            primary[outer_id] = {
                "schema": PLANNER_TASK_SCHEMA,
                "source_ledger": ledger_name,
                "source_outer_id": outer_id,
                "source_outer_row_sha256": row["row_sha256"],
                "pair_index": row["pair_index"],
                "c40_source_leaf_id": row["c40_source_leaf_id"],
                "descendant_path": row["descendant_path"],
                "residual_classification": classification,
                "category": category,
                "normalized_surface_count": 0,
                "pair_incidence_count": 0,
                "surface_face_incidence_count": 0,
                "base_work_units": work_units,
            }
            class_census[classification] += 1
    need(len(primary) == 3443 and class_census == Counter({
        key: value[2] for key, value in ZERO_SURFACE_CLASSES.items()
    }), "C41 complete zero-surface source census")

    ambient = iter_frozen_ledger(
        C41_DIR, c41_result["ledgers"]["routed_ambient_cells"],
        "C41 raw 91879 ambient discovery",
    )
    need(len(ambient) == 91_879, "C41 exact ambient row count")
    stats = {
        pair: {"nonterminal": 0, "collision3": 0, "sources": []}
        for pair in range(862)
    }
    seen: set[str] = set()
    for row in ambient:
        pair = row["pair_index"]
        need(type(pair) is int and 0 <= pair < 862, "ambient pair range")
        family = row["disposition_family"]
        if family == "TERMINAL_EXCLUDED":
            continue
        stats[pair]["nonterminal"] += 1
        if family == "COLLISION3_READY":
            stats[pair]["collision3"] += 1
            continue
        need(family == "RESIDUAL_OUTER", "ambient disposition enum")
        obligations = row.get("obligation_ids")
        need(type(obligations) is list and obligations,
             "residual primary obligation")
        task = primary.get(obligations[0])
        if task is None:
            continue
        need(task["pair_index"] == pair
             and task["c40_source_leaf_id"] == row["c40_source_leaf_id"]
             and task["descendant_path"] == row["path"]
             and task["residual_classification"]
             == row["residual_classification"]
             and row["local_round144_terminal_credit"] == 0
             and row["lower_dimensional_ambient_credit"] == 0
             and row["collision3_ready_credit"] == 0
             and row["D02_gate_credit"] == 0,
             "C41 outer/ambient foreign key")
        outer_id = task["source_outer_id"]
        need(outer_id not in seen, "zero-surface ambient uniqueness")
        task.update({
            "source_ambient_id": row["c41_ambient_cell_id"],
            "source_ambient_row_sha256": row["row_sha256"],
            "source_parent_volume_fraction": row["parent_volume_fraction"],
            "closed_representative_box": row["closed_representative_box"],
            "closed_reflected_box": row["closed_reflected_box"],
            "representative_cell_id": row["representative_cell_id"],
            "reflected_cell_id": row["reflected_cell_id"],
        })
        stats[pair]["sources"].append(outer_id)
        seen.add(outer_id)
    need(seen == set(primary), "all zero-surface outers ambient-bound")

    raw_sole = []
    for pair, value in stats.items():
        sources = sorted(value["sources"])
        whole = value["nonterminal"] == len(sources) and value["collision3"] == 0
        if whole and len(sources) == 1:
            raw_sole.append(pair)
    need(raw_sole == [97, 211, 391, 592, 664, 715],
         "independently derived six raw C41 sole deficits")
    c42_newly_whole = sorted(
        row["pair_index"] for row in c42_parents
        if row["newly_whole_terminal_vs_C41"] is True
    )
    need(c42_newly_whole == [391], "derive exact C42 sole closure overlay")
    post_c42 = tuple(pair for pair in raw_sole if pair not in c42_newly_whole)
    need(post_c42 == TARGET_PAIRS,
         "independently derived five post-C42 targets")

    planned: dict[int, dict[str, Any]] = {}
    for pair in post_c42:
        task = copy.deepcopy(primary[stats[pair]["sources"][0]])
        category = task["category"]
        priority = "WHOLE_PAIR_GAIN"
        task.update({
            "priority_class": priority,
            "priority_rank": PRIORITY_ORDER[priority],
            "pair_all_nonterminal_count": stats[pair]["nonterminal"],
            "pair_b0_task_count": 1,
            "pair_collision3_ready_count": stats[pair]["collision3"],
            "b0_closure_would_make_whole_pair": True,
            "already_closed_by_C42": False,
            "planning_only": True,
            "D02_gate_credit": 0,
        })
        need(category in PRIORITY_ORDER, "planner category enum")
        task["task_id"] = "c43b0-task:" + digest(task)
        planned[pair] = task
    derivation = {
        "zero_surface_source_count": len(primary),
        "ambient_row_count": len(ambient),
        "raw_C41_sole_pairs": raw_sole,
        "C42_newly_whole_pairs": c42_newly_whole,
        "post_C42_sole_pairs": list(post_c42),
    }
    return planned, ambient, derivation


def validate_target_rows_local(
    ambient: list[dict[str, Any]], c42_parents: list[dict[str, Any]],
) -> tuple[dict[int, dict[str, Any]], dict[int, dict[str, Any]]]:
    c41_rows: dict[int, dict[str, Any]] = {}
    for row in ambient:
        pair = row["pair_index"]
        if pair not in TARGET_PAIRS or row["disposition_family"] == "TERMINAL_EXCLUDED":
            continue
        need(pair not in c41_rows, "unique C41 sole residual:" + str(pair))
        c41_rows[pair] = row
    targets = {row["pair_index"]: row for row in c42_parents
               if row["pair_index"] in TARGET_PAIRS}
    need(set(c41_rows) == set(TARGET_PAIRS)
         and set(targets) == set(TARGET_PAIRS), "five target row domains")
    for pair in TARGET_PAIRS:
        expected = EXPECTED_TARGETS[pair]
        row = c41_rows[pair]
        parent = targets[pair]
        need(
            row["path"] == expected["descendant_path"]
            and row["c40_source_leaf_id"] == expected["c40_leaf_id"]
            and row["c40_source_row_sha256"] == expected["c40_row_sha256"]
            and row["row_sha256"] == expected["c41_ambient_row_sha256"]
            and row["raw_classification"] == expected["raw_classification"]
            and row["residual_classification"]
            == expected["residual_classification"]
            and row["disposition_family"] == "RESIDUAL_OUTER"
            and Q(row["parent_volume_fraction"]) == SOURCE_FRACTION,
            "exact C41 target binding:" + str(pair),
        )
        need(
            parent["row_sha256"] == expected["c42_parent_row_sha256"]
            and parent["C41_parent_row_sha256"]
            == expected["c41_parent_row_sha256"]
            and parent["unresolved_parent_volume"] == "1/512"
            and parent["terminal_excluded_parent_volume"] == "511/512"
            and parent["nonterminal_leaf_count"] == 1
            and parent["C42_terminal_gain"] == "0"
            and parent["newly_whole_terminal_vs_C41"] is False
            and parent["D02_gate_credit"] == 0,
            "exact C42 target baseline:" + str(pair),
        )
    return c41_rows, targets


def load_c40_tasks_local(
    base: dict[str, Any], c40_dir: Path,
    c41_rows: dict[int, dict[str, Any]],
) -> dict[int, dict[str, Any]]:
    wanted = {EXPECTED_TARGETS[pair]["c40_leaf_id"]: pair
              for pair in TARGET_PAIRS}
    tasks: dict[int, dict[str, Any]] = {}
    source_rows = iter_frozen_ledger(
        c40_dir, base["result"]["ledgers"]["routed_leaf_cells"],
        "C40 raw target source ledger",
    )
    for ordinal, source in enumerate(source_rows):
        pair = wanted.get(source["c40_leaf_id"])
        if pair is None:
            continue
        expected = EXPECTED_TARGETS[pair]
        need(pair not in tasks and source["pair_index"] == pair
             and source["row_sha256"] == expected["c40_row_sha256"]
             and source["path"] == c41_rows[pair]["source_path"],
             "exact C40 task source:" + str(pair))
        tasks[pair] = c41.task_for_row(ordinal, source, base)
    need(set(tasks) == set(TARGET_PAIRS), "five exact raw C40 tasks")
    return tasks


def load_context() -> dict[str, Any]:
    c41_authority = validate_installed_c41_authority()
    installed = validate_installed_c42_authority()
    validate_frozen_manifest(C41_DIR, EXPECTED_C41_MANIFEST, 13, "C41")
    c41_result = strict_json(
        stable_read(C41_DIR / "result.json", 32 << 20, "C41 result"),
        "C41 result",
    )
    self_closed(c41_result, "object_sha256", "C41 result")
    need(c41_result["object_sha256"] == EXPECTED_C41_OBJECT,
         "C41 result object pin")
    c42_result = strict_json(
        stable_read(C42_DIR / "result.json", 32 << 20, "C42 result"),
        "C42 result",
    )
    self_closed(c42_result, "object_sha256", "C42 result")
    need(c42_result["object_sha256"] == EXPECTED_C42_OBJECT,
         "C42 result object pin")
    parents = iter_frozen_ledger(
        C42_DIR, c42_result["ledgers"]["parent_conservation"],
        "C42 raw parent conservation",
    )
    need(len(parents) == 862
         and [row["pair_index"] for row in parents] == list(range(862)),
         "C42 complete ordered parent baseline")
    planned, ambient, derivation = derive_sole_deficit_frontier(
        c41_result, parents
    )
    c41_rows, c42_targets = validate_target_rows_local(ambient, parents)
    c40_dir = (ROOT / c41_result["C40_authority"]["path"]).resolve()
    c40_audit = (
        ROOT / c41_result["C40_authority"]["independent_audit_path"]
    ).resolve()
    base = c41.load_context(c40_dir, c40_audit, formal=True)
    jobs = load_c40_tasks_local(base, c40_dir, c41_rows)
    c41.ctx.prec = c41.PRECISION_BITS
    generated = c41.install_complete_immutable_cache()
    need(sum(len(value) for value in generated.values()) == 448,
         "complete immutable mathematical cache")
    config = c41.decode_worker_config(base["config"])
    boundaries = {}
    for row in iter_frozen_ledger(
        C41_DIR, c41_result["ledgers"]["boundary_corner_outers"],
        "C41 raw boundary/corner ledger",
    ):
        pair = row["pair_index"]
        if pair in TARGET_PAIRS and row["descendant_path"] == c41_rows[pair]["path"]:
            need(pair not in boundaries, "unique target boundary")
            boundaries[pair] = row
    need(set(boundaries) == set(TARGET_PAIRS), "five target boundaries")
    exact_sources = iter_frozen_ledger(
        C42_DIR, c42_result["ledgers"]["exact_source"],
        "C42 raw exact source",
    )
    need(len(exact_sources) == 1, "C42 singleton exact source")
    return {
        "C41_authority": c41_authority,
        "installed": installed,
        "C41_result": c41_result,
        "C42_result": c42_result,
        "frontier_derivation": derivation,
        "planner": planned,
        "C41_rows": c41_rows,
        "C42_targets": c42_targets,
        "C42_parents": parents,
        "C42_source": exact_sources[0],
        "base": base,
        "tasks": jobs,
        "config": config,
        "ambient": ambient,
        "boundaries": boundaries,
    }


def box_payload(box: Any) -> dict[str, list[str]]:
    return {
        "t": [qstr(box.t0), qstr(box.t1)],
        "p": [qstr(box.p0), qstr(box.p1)],
        "s": [qstr(box.s0), qstr(box.s1)],
    }


def box_from_payload(value: dict[str, Any], label: str = "") -> Any:
    return c41.c38.round166.ge.AtlasBox(
        Q(value["t"][0]), Q(value["t"][1]),
        Q(value["p"][0]), Q(value["p"][1]),
        Q(value["s"][0]), Q(value["s"][1]), 0, label,
    )


def route_projection(route: dict[str, Any]) -> dict[str, Any]:
    return {
        "closed_box": box_payload(route["box"]),
        "classification": route["classification"],
        "witness": route["witness"],
        "route_method": route["route_method"],
        "c1_result": route["c1_result"],
        "c2_status": route["c2_status"],
        "c2_baseline": route["c2_baseline"],
        "c2_detail": route["c2_detail"],
        "c2_evidence": route["c2_evidence"],
        "route_failure": route["route_failure"],
    }


def adaptive_tree(task: dict[str, Any], start: str,
                  config: dict[str, Any]) -> dict[str, Any]:
    stack = [(start, 0, Q(1), c41.route_at_path(task, start, config))]
    leaves = []
    splits = []
    route_count = 1
    while stack:
        path, depth, fraction, route = stack.pop()
        family = c41.disposition_family(route["classification"])
        if family == "TERMINAL_EXCLUDED":
            leaves.append({
                "path": path, "additional_depth": depth,
                "relative_fraction": fraction, "route": route,
            })
            continue
        need(family != "COLLISION3_READY", "no collision3 handoff")
        need(depth < 32 and route_count + 2 <= 8191,
             "semantic traversal terminates")
        parent = route["box"]
        axis = c41.c38.round166.longest_axis(parent)
        need(axis in {0, 1}, "s=0 adaptive axis")
        children = c41.c38.round166.split_axis(parent, axis)
        routed = []
        for bit in ("0", "1"):
            child = c41.route_at_path(task, path + bit, config)
            need(box_payload(child["box"]) == box_payload(children[int(bit)]),
                 "exact child reconstruction")
            routed.append(child)
        route_count += 2
        lower = (parent.t0, parent.p0)[axis]
        upper = (parent.t1, parent.p1)[axis]
        splits.append({
            "parent_path": path,
            "additional_depth_before_split": depth,
            "relative_parent_fraction": fraction,
            "parent_box": parent,
            "axis": axis,
            "axis_name": ("t", "p")[axis],
            "midpoint": (lower + upper) / 2,
            "children": children,
            "child_paths": (path + "0", path + "1"),
            "child_route_hashes": (
                digest(route_projection(routed[0])),
                digest(route_projection(routed[1])),
            ),
        })
        for bit in ("1", "0"):
            stack.append((path + bit, depth + 1, fraction / 2,
                          routed[int(bit)]))
    leaves.sort(key=lambda row: row["path"])
    splits.sort(key=lambda row: row["parent_path"])
    paths = [row["path"] for row in leaves]
    need(
        len(paths) == len(set(paths))
        and not any(right.startswith(left) for left in paths for right in paths
                    if left != right)
        and sum(row["relative_fraction"] for row in leaves) == 1,
        "prefix-free Kraft tree",
    )
    return {
        "leaves": leaves, "splits": splits, "route_count": route_count,
        "deepest": max(row["additional_depth"] for row in leaves),
    }


def reflected_path_and_box(task: dict[str, Any], path: str,
                           cells: dict[str, dict[str, Any]]) \
        -> tuple[str, Any, Any]:
    representative = task["cell"]
    reflected = cells[task["c38_source"]["reflected_cell_id"]]
    rep_box, _ = c41.c39.reconstruct_box(representative, "")
    ref_box, _ = c41.c39.reconstruct_box(reflected, "")
    chart = representative["gate3_chart"].split(":")[1]
    ref_path = ""
    for bit in path:
        rep_axis = c41.c38.round166.longest_axis(rep_box)
        ref_axis = c41.c38.round166.longest_axis(ref_box)
        need(rep_axis == ref_axis, "reflection split axis")
        reverse = rep_axis == 1 or (rep_axis == 0 and chart in {"E", "W"})
        ref_bit = str(1 - int(bit)) if reverse else bit
        rep_box = c41.c38.round166.split_axis(rep_box, rep_axis)[int(bit)]
        ref_box = c41.c38.round166.split_axis(ref_box, ref_axis)[int(ref_bit)]
        ref_path += ref_bit
    expected = c41.c40.reflected_payload(chart, rep_box)
    need(box_payload(ref_box)["t"] == expected["t"]
         and box_payload(ref_box)["p"] == expected["p"],
         "exact Jy endpoint transport")
    return ref_path, rep_box, ref_box


def make_reflected_task(task: dict[str, Any],
                        cells: dict[str, dict[str, Any]]) -> dict[str, Any]:
    value = copy.deepcopy(task)
    source = value["c38_source"]
    source["representative_origin_key"], source["reflected_origin_key"] = (
        source["reflected_origin_key"], source["representative_origin_key"]
    )
    source["representative_cell_id"], source["reflected_cell_id"] = (
        source["reflected_cell_id"], source["representative_cell_id"]
    )
    value["cell"] = cells[source["representative_cell_id"]]
    return value


def cell_for_box(cell: dict[str, Any], box: Any) -> dict[str, Any]:
    value = copy.deepcopy(cell)
    value["physical_t_interval"] = [
        {"kind": "RATIONAL", "value": qstr(box.t0)},
        {"kind": "RATIONAL", "value": qstr(box.t1)},
    ]
    value["physical_p_interval"] = [qstr(box.p0), qstr(box.p1)]
    return value


def exact_payload(value: Any) -> Any:
    if isinstance(value, arb):
        return c41.c39.arb_payload(value)
    if isinstance(value, (Q, fmpq)):
        return qstr(value)
    if value is None or type(value) in {str, int, bool}:
        return value
    if isinstance(value, dict):
        return {str(key): exact_payload(item) for key, item in value.items()}
    if isinstance(value, (tuple, list)):
        return [exact_payload(item) for item in value]
    raise Reject("unsupported exact payload:" + type(value).__name__)


def record_payload(record: Any) -> dict[str, Any]:
    return {
        "target_id": record.target_id,
        "classification": record.classification,
        "ell": exact_payload(record.ell),
        "discriminant": exact_payload(record.discriminant),
        "near": exact_payload(record.near),
        "far": exact_payload(record.far),
        "transverse": exact_payload(record.transverse),
    }


class PrimitiveRestrictionRebuilder:
    def __init__(self, config: dict[str, Any]):
        self.config = config
        self.cache: dict[bytes, dict[str, Any]] = {}

    def certificate(self, pair: int, orientation: str, path: str,
                    origin: str, cell: dict[str, Any], box: Any, scope: str,
                    terminal_credit: int) -> dict[str, Any]:
        key = canonical({
            "pair": pair, "orientation": orientation, "path": path,
            "origin": origin, "cell": cell["cell_id"],
            "box": box_payload(box), "scope": scope,
            "credit": terminal_credit,
        })
        if key in self.cache:
            return copy.deepcopy(self.cache[key])
        task = {
            # The task id is evidence material, not a mathematical input.  Use
            # the candidate contract's canonical id while independently
            # recomputing every downstream quantity.
            "task_id": f"c43-direct:{pair}:{orientation}:{path}:{scope}",
            "kind": "C1",
            "row": {"path": "", "representative_origin_key": origin},
            "cell": cell_for_box(cell, box),
        }
        routed = c41.c39.route_c1_task(task, self.config)
        need(routed["classification"] == EXPECTED_CLASSES[pair],
             "direct strict C1 word mismatch")
        active = tuple(cell["source_lineage"]["active_candidates"])
        stage_one, records = c41.c38.round166.classify_active(
            cell["gate3_chart"], box, active
        )
        enhanced = []
        evidence = []
        for record in records:
            replacement, item = c41.c39.enhanced_record(origin, box, record)
            enhanced.append(replacement)
            if item is not None:
                evidence.append(item)
        leaf = c41.c38.round166.classify_from_records(
            cell["gate3_chart"], box, enhanced
        )
        need(
            leaf.classification == "unique_first"
            and leaf.owner_target == c41.c39.FROZEN_OWNER
            and all(item.classification not in {
                "unresolved_discriminant", "unresolved_root_sign"
            } for item in enhanced),
            "closed-box unique first owner",
        )
        h1 = c41.c39.h1_route(origin, box)
        need(h1["kind"] == "STRICT_SIDE" and h1["chart"] == "W"
             and h1["H1_centered"]["sign"] != "UNRESOLVED",
             "closed-box strict H1 W side")
        chart_id = ":".join(origin.split(":")[:2])
        owner = c41.c38.first_owner(chart_id, box)
        need(owner is not None
             and owner["selected_target_id"] == c41.c39.FROZEN_OWNER,
             "strict first owner materialized")
        lower = c41.c38.round139.lower
        core_index = c41.c38.CORE_INDEX[chart_id]
        atom = lower.step1.Atom(
            core_index, self.config["cores"][core_index],
            box.t0, box.t1, box.p0, box.p1, Q(0), Q(0), "c43",
        )
        initial = lower.round136.initial_state(atom)
        outgoing = lower.time3.second_outgoing_state(atom, initial, owner)
        need(outgoing is not None and outgoing["chart"] == "W",
             "defined outgoing state")
        word, error = lower.round136.translation_normalized_official_word(
            initial, "W[0,0]", owner,
            self.config["pair_index"], self.config["pattern_index"],
        )
        need(word is not None and error is None, "defined official word")
        compact = lower.round136.compact_key(word["key"])
        expected = self.config["original_path"][0]
        need(compact["official_word_key_id"]
             != expected["official_word_key_id"], "word inequality")
        record_rows = [record_payload(item) for item in enhanced]
        semantic = {
            "schema": CANDIDATE_SCHEMA
                + ".closed-leaf-certificate.direct-restriction",
            "pair_index": pair,
            "orientation": orientation,
            "path": path,
            "scope": scope,
            "parent_key": origin,
            "cell_id": cell["cell_id"],
            "closed_box": box_payload(box),
            "closed_box_scope":
                "ENTIRE_CLOSED_RATIONAL_BOX_INCLUDING_ALL_FACES",
            "active_target_universe": list(active),
            "input_stage_one_classification": stage_one.classification,
            "enhanced_stage_one_classification": leaf.classification,
            "enhanced_unique_owner": leaf.owner_target,
            "ordered_collision1_candidate_records": record_rows,
            "collision1_candidate_record_census": dict(sorted(Counter(
                item["classification"] for item in record_rows
            ).items())),
            "enhancement_evidence": evidence,
            "H1_closed_box_evidence": h1,
            "strict_first_owner": exact_payload(owner),
            "initial_state": exact_payload(initial),
            "outgoing_state": exact_payload(outgoing),
            "official_word": word,
            "official_word_compact_key": compact,
            "expected_lineage_word": expected,
            "official_word_key_inequality": {
                "calculated": compact["official_word_key_id"],
                "expected": expected["official_word_key_id"],
                "operands_are_distinct": True,
            },
            "endpoint_phase": c41.c40.endpoint_phase(box),
            "homogeneity": {
                "s_interval": [qstr(box.s0), qstr(box.s1)],
                "s_is_exactly_zero": box.s0 == box.s1 == 0,
                "physical_core_index": core_index,
            },
            "route_result": routed,
            "strict_disposition": routed["classification"],
            "strict_terminal_on_entire_closed_box": True,
            "local_round144_terminal_credit": terminal_credit,
            "lower_dimensional_ambient_credit": 0,
            "D02_gate_credit": 0,
        }
        semantic["certificate_id"] = "c43-cert:" + digest(semantic)
        self.cache[key] = copy.deepcopy(semantic)
        return semantic


def parsed_box(row: dict[str, Any], orientation: str) \
        -> tuple[Q, Q, Q, Q] | None:
    field = (
        "closed_representative_box"
        if orientation == "REPRESENTATIVE" else "closed_reflected_box"
    )
    value = row[field]
    if value is None:
        return None
    return (Q(value["t"][0]), Q(value["t"][1]),
            Q(value["p"][0]), Q(value["p"][1]))


def owner_key(row: dict[str, Any]) -> tuple[str, int, str]:
    return row["path"], row["pair_index"], row["c41_ambient_cell_id"]


def effective_incident(row: dict[str, Any], terminal: set[str]) \
        -> dict[str, Any]:
    value = (
        row["disposition_family"] == "TERMINAL_EXCLUDED"
        or row["c41_ambient_cell_id"] in terminal
    )
    return {
        "pair_index": row["pair_index"],
        "path": row["path"],
        "representative_cell_id": row["representative_cell_id"],
        "reflected_cell_id": row["reflected_cell_id"],
        "c41_ambient_cell_id": row["c41_ambient_cell_id"],
        "c41_row_sha256": row["row_sha256"],
        "C41_disposition_family": row["disposition_family"],
        "terminal_after_C43_subset": value,
    }


def point_incidents(geometry: list[tuple[Any, Any, Any]], orientation: str,
                    t: Q, p: Q, terminal: set[str]) -> list[dict[str, Any]]:
    index = 1 if orientation == "REPRESENTATIVE" else 2
    rows = []
    for item in geometry:
        box = item[index]
        if box is not None and box[0] <= t <= box[1] and box[2] <= p <= box[3]:
            rows.append(effective_incident(item[0], terminal))
    rows.sort(key=owner_key)
    need(bool(rows), "nonempty point incidence")
    return rows


def face_partition(geometry: list[tuple[Any, Any, Any]], orientation: str,
                   box: Any, face: str, terminal: set[str]) -> dict[str, Any]:
    index = 1 if orientation == "REPRESENTATIVE" else 2
    if face.startswith("t_"):
        fixed = box.t0 if face == "t_lower" else box.t1
        lo, hi, transverse = box.p0, box.p1, 0
    else:
        fixed = box.p0 if face == "p_lower" else box.p1
        lo, hi, transverse = box.t0, box.t1, 1
    candidates = []
    points = {lo, hi}
    for row, rep, ref in geometry:
        value = rep if index == 1 else ref
        if value is None:
            continue
        t0, t1, p0, p1 = value
        contains = t0 <= fixed <= t1 if transverse == 0 else p0 <= fixed <= p1
        along0, along1 = (p0, p1) if transverse == 0 else (t0, t1)
        if contains and max(lo, along0) <= min(hi, along1):
            candidates.append((row, value))
            points.add(max(lo, along0))
            points.add(min(hi, along1))
    ordered = sorted(points)
    need(ordered[0] == lo and ordered[-1] == hi,
         "complete face endpoints")
    segments = []
    for left, right in zip(ordered, ordered[1:]):
        need(left < right, "strict face segment")
        middle = (left + right) / 2
        incident = []
        for row, value in candidates:
            a, b = ((value[2], value[3]) if transverse == 0
                    else (value[0], value[1]))
            if a <= middle <= b:
                incident.append(effective_incident(row, terminal))
        incident.sort(key=owner_key)
        need(bool(incident), "nonempty face segment")
        segments.append({
            "interval": [qstr(left), qstr(right)],
            "midpoint": qstr(middle),
            "incident_ambient_cells": incident,
            "canonical_owner": incident[0],
            "canonical_owner_terminal_after_C43_subset":
                incident[0]["terminal_after_C43_subset"],
        })
    internal = []
    for value in ordered[1:-1]:
        t, p = ((fixed, value) if transverse == 0 else (value, fixed))
        incident = point_incidents(geometry, orientation, t, p, terminal)
        internal.append({
            "coordinate": {"t": qstr(t), "p": qstr(p), "s": "0"},
            "incident_ambient_cells": incident,
            "canonical_owner": incident[0],
            "canonical_owner_terminal_after_C43_subset":
                incident[0]["terminal_after_C43_subset"],
        })
    return {
        "fixed_coordinate": qstr(fixed),
        "longitudinal_interval": [qstr(lo), qstr(hi)],
        "breakpoint_count": len(ordered),
        "breakpoints": [qstr(value) for value in ordered],
        "segments": segments,
        "interior_breakpoints": internal,
        "global_candidate_incident_count": len(candidates),
        "global_incident_census_complete": True,
        "all_required_segment_and_breakpoint_owners_terminal": (
            all(row["canonical_owner_terminal_after_C43_subset"]
                for row in segments)
            and all(row["canonical_owner_terminal_after_C43_subset"]
                    for row in internal)
        ),
    }


def make_face_box(box: Any, face: str, lo: Q | None = None,
                  hi: Q | None = None) -> Any:
    t0, t1, p0, p1 = box.t0, box.t1, box.p0, box.p1
    if face == "t_lower":
        t1 = t0
        if lo is not None: p0, p1 = lo, hi
    elif face == "t_upper":
        t0 = t1
        if lo is not None: p0, p1 = lo, hi
    elif face == "p_lower":
        p1 = p0
        if lo is not None: t0, t1 = lo, hi
    elif face == "p_upper":
        p0 = p1
        if lo is not None: t0, t1 = lo, hi
    else:
        raise Reject("unknown face")
    return type(box)(t0, t1, p0, p1, box.s0, box.s1, 0, face)


def make_point_box(box: Any, corner: str) -> Any:
    t = box.t0 if corner.startswith("t0") else box.t1
    p = box.p0 if corner.endswith("p0") else box.p1
    return type(box)(t, t, p, p, box.s0, box.s1, 0, corner)


def target_orientation(pair: int, orientation: str, context: dict[str, Any]) \
        -> tuple[str, dict[str, Any], Any, str]:
    task = context["tasks"][pair]
    source = context["C41_rows"][pair]
    if orientation == "REPRESENTATIVE":
        return (
            task["c38_source"]["representative_origin_key"], task["cell"],
            box_from_payload(source["closed_representative_box"], "rep"),
            source["path"],
        )
    reflected = make_reflected_task(task, context["base"]["cells"])
    path, _rep, box = reflected_path_and_box(
        task, source["path"], context["base"]["cells"]
    )
    return (
        reflected["c38_source"]["representative_origin_key"],
        reflected["cell"], box, path,
    )


def build_boundaries(context: dict[str, Any], terminal: set[str]) \
        -> tuple[dict[int, dict[str, Any]], list[tuple[Any, Any, Any]]]:
    geometry = [
        (row, parsed_box(row, "REPRESENTATIVE"),
         parsed_box(row, "REFLECTED"))
        for row in context["ambient"]
    ]
    result = {}
    for pair in TARGET_PAIRS:
        faces = []
        corners = []
        blockers = []
        for orientation in ("REPRESENTATIVE", "REFLECTED"):
            _origin, _cell, box, path = target_orientation(
                pair, orientation, context
            )
            for face in ("t_lower", "t_upper", "p_lower", "p_upper"):
                partition = face_partition(
                    geometry, orientation, box, face, terminal
                )
                faces.append({
                    "orientation": orientation, "face": face,
                    "target_path": path, "partition": partition,
                })
                for segment in partition["segments"]:
                    if not segment["canonical_owner_terminal_after_C43_subset"]:
                        blockers.append({
                            "orientation": orientation,
                            "stratum": "FACE_SEGMENT",
                            "face_or_corner": face,
                            "exact_key": segment["interval"],
                            "canonical_owner": segment["canonical_owner"],
                        })
                for point in partition["interior_breakpoints"]:
                    if not point["canonical_owner_terminal_after_C43_subset"]:
                        blockers.append({
                            "orientation": orientation,
                            "stratum": "FACE_BREAKPOINT",
                            "face_or_corner": face,
                            "exact_key": point["coordinate"],
                            "canonical_owner": point["canonical_owner"],
                        })
            for corner in ("t0p0", "t0p1", "t1p0", "t1p1"):
                point = make_point_box(box, corner)
                incident = point_incidents(
                    geometry, orientation, point.t0, point.p0, terminal
                )
                obligation = {
                    "orientation": orientation,
                    "corner": corner,
                    "target_path": path,
                    "coordinate": {
                        "t": qstr(point.t0), "p": qstr(point.p0), "s": "0"
                    },
                    "incident_ambient_cells": incident,
                    "canonical_owner": incident[0],
                    "canonical_owner_terminal_after_C43_subset":
                        incident[0]["terminal_after_C43_subset"],
                }
                corners.append(obligation)
                if not obligation["canonical_owner_terminal_after_C43_subset"]:
                    blockers.append({
                        "orientation": orientation,
                        "stratum": "SOURCE_CORNER",
                        "face_or_corner": corner,
                        "exact_key": obligation["coordinate"],
                        "canonical_owner": incident[0],
                    })
        result[pair] = {
            "face_obligations": faces,
            "corner_obligations": corners,
            "canonical_residual_owner_blockers": blockers,
            "canonical_residual_owner_blocker_count": len(blockers),
            "boundary_owner_eligible": len(blockers) == 0,
        }
    return result, geometry


def box_contains(box: dict[str, Any], t: Q, p: Q) -> bool:
    return (Q(box["t"][0]) <= t <= Q(box["t"][1])
            and Q(box["p"][0]) <= p <= Q(box["p"][1]))


def reconstruct_candidate_ledgers_v2(
                  context: dict[str, Any], trees: dict[int, dict[str, Any]],
                  boundary: dict[int, dict[str, Any]],
                  geometry: list[tuple[Any, Any, Any]],
                  eligible_pairs: tuple[int, ...],
                  blocked_pairs: tuple[int, ...]) \
        -> dict[str, list[dict[str, Any]]]:
    result: dict[str, list[dict[str, Any]]] = {key: [] for key in LEDGERS}
    oracle = PrimitiveRestrictionRebuilder(context["config"])

    for pair in TARGET_PAIRS:
        tree = trees[pair]
        source = context["C41_rows"][pair]
        profile = EXPECTED_PROFILES[pair]
        need(
            (len(tree["leaves"]), len(tree["splits"]), tree["deepest"])
            == profile
            and all(leaf["route"]["classification"] == EXPECTED_CLASSES[pair]
                    for leaf in tree["leaves"]),
            "fresh adaptive profile:" + str(pair),
        )
        semantic = {
            "schema": CANDIDATE_SCHEMA + ".source-preflight",
            "pair_index": pair,
            "derived_from_planner": True,
            "planner_task_id": context["planner"][pair]["task_id"],
            "C41_ambient_cell_id": source["c41_ambient_cell_id"],
            "C41_ambient_row_sha256": source["row_sha256"],
            "C42_parent_row_sha256":
                context["C42_targets"][pair]["row_sha256"],
            "descendant_path": source["path"],
            "source_fraction": source["parent_volume_fraction"],
            "fresh_route_count": tree["route_count"],
            "fresh_split_count": len(tree["splits"]),
            "fresh_terminal_leaf_count": len(tree["leaves"]),
            "fresh_deepest_additional_depth": tree["deepest"],
            "fresh_leaf_path_sequence": [row["path"] for row in tree["leaves"]],
            "fresh_leaf_classification_census": dict(sorted(Counter(
                row["route"]["classification"] for row in tree["leaves"]
            ).items())),
            "relative_Kraft_sum": qstr(sum(
                row["relative_fraction"] for row in tree["leaves"]
            )),
            "canonical_residual_owner_blocker_count":
                boundary[pair]["canonical_residual_owner_blocker_count"],
            "canonical_residual_owner_blockers":
                boundary[pair]["canonical_residual_owner_blockers"],
            "eligible_for_C43_credit":
                boundary[pair]["boundary_owner_eligible"],
            "expected_regression_guard": EXPECTED_TARGETS[pair],
            "local_round144_terminal_credit":
                1 if boundary[pair]["boundary_owner_eligible"] else 0,
            "blocked_input_credit": 0,
            "lower_dimensional_ambient_credit": 0,
            "D02_gate_credit": 0,
        }
        result["preflight"].append(close_expected(
            semantic, "source_preflight_id", "c43-preflight:"
        ))
    need(tuple(row["pair_index"] for row in result["preflight"])
         == TARGET_PAIRS, "preflight pair order")

    preflight_map = {row["pair_index"]: row for row in result["preflight"]}
    for pair in eligible_pairs:
        source = context["C41_rows"][pair]
        task = context["tasks"][pair]
        outer = context["boundaries"][pair]
        planned = context["planner"][pair]
        need(outer["owning_outer_id"] == planned["source_outer_id"],
             "primary outer binding")
        semantic = {
            "schema": CANDIDATE_SCHEMA + ".exact-source",
            "pair_index": pair,
            "installed_C42_candidate_object_sha256": EXPECTED_C42_OBJECT,
            "installed_C42_audit_object_sha256": EXPECTED_C42_AUDIT_OBJECT,
            "installed_C42_seal_object_sha256": EXPECTED_C42_SEAL_OBJECT,
            "installed_C42_receipt_object_sha256": EXPECTED_C42_RECEIPT_OBJECT,
            "C42_candidate_path": str(C42_DIR.relative_to(ROOT)),
            "C42_parent_row_sha256":
                context["C42_targets"][pair]["row_sha256"],
            "C41_candidate_object_sha256": EXPECTED_C41_OBJECT,
            "C41_root_manifest_sha256": EXPECTED_C41_MANIFEST,
            "C41_ambient_cell_id": source["c41_ambient_cell_id"],
            "C41_ambient_row_sha256": source["row_sha256"],
            "C41_primary_outer_id": planned["source_outer_id"],
            "C41_primary_outer_row_sha256": planned["source_outer_row_sha256"],
            "C41_boundary_outer_id": outer["boundary_corner_outer_id"],
            "C41_boundary_outer_row_sha256": outer["row_sha256"],
            "C40_source_leaf_id": source["c40_source_leaf_id"],
            "C40_source_row_sha256": source["c40_source_row_sha256"],
            "C38_source_row_sha256": task["source"]["c38_source_row_sha256"],
            "representative_origin_key":
                task["c38_source"]["representative_origin_key"],
            "reflected_origin_key": task["c38_source"]["reflected_origin_key"],
            "representative_cell_id": source["representative_cell_id"],
            "reflected_cell_id": source["reflected_cell_id"],
            "descendant_path": source["path"],
            "closed_representative_box": source["closed_representative_box"],
            "closed_reflected_box": source["closed_reflected_box"],
            "source_fraction": source["parent_volume_fraction"],
            "source_residual_classification": source["residual_classification"],
            "preflight_row_sha256": preflight_map[pair]["row_sha256"],
            "unique_post_C42_residual_descendant": True,
            "boundary_owner_eligible": True,
            "source_binding_complete": True,
            "producer_output_is_authority": False,
            "D02_gate_credit": 0,
        }
        result["sources"].append(close_expected(
            semantic, "exact_source_id", "c43-source:"
        ))

    for pair in eligible_pairs:
        start = context["C41_rows"][pair]["path"]
        for split in trees[pair]["splits"]:
            semantic = {
                "schema": CANDIDATE_SCHEMA + ".adaptive-split",
                "pair_index": pair,
                "source_descendant_path": start,
                "parent_path": split["parent_path"],
                "additional_depth_before_split":
                    split["additional_depth_before_split"],
                "relative_parent_fraction":
                    qstr(split["relative_parent_fraction"]),
                "absolute_parent_fraction": qstr(
                    SOURCE_FRACTION * split["relative_parent_fraction"]
                ),
                "longest_axis_rule": "ROUND166_PINNED_LONGEST_AXIS_TIE_ORDER",
                "split_axis": split["axis_name"],
                "exact_split_midpoint": qstr(split["midpoint"]),
                "parent_closed_box": box_payload(split["parent_box"]),
                "lower_child_path": split["child_paths"][0],
                "upper_child_path": split["child_paths"][1],
                "lower_child_closed_box": box_payload(split["children"][0]),
                "upper_child_closed_box": box_payload(split["children"][1]),
                "child_route_semantic_sha256": list(split["child_route_hashes"]),
                "lower_child_fraction_multiplier": "1/2",
                "upper_child_fraction_multiplier": "1/2",
                "exact_fraction_conservation": "1",
                "closed_cover_equality": True,
                "half_open_shared_face_owner": "LOWER_BIT_CHILD",
                "ambient_or_whole_parent_credit": 0,
                "D02_gate_credit": 0,
            }
            result["splits"].append(close_expected(
                semantic, "adaptive_split_id", "c43-split:"
            ))
    result["splits"].sort(key=lambda row: (row["pair_index"], row["parent_path"]))

    leaf_map: dict[tuple[int, str, str], dict[str, Any]] = {}
    cells = context["base"]["cells"]
    for pair in eligible_pairs:
        task = context["tasks"][pair]
        reflected = make_reflected_task(task, cells)
        for leaf in trees[pair]["leaves"]:
            path = leaf["path"]
            ref_path, rep_box, ref_box = reflected_path_and_box(task, path, cells)
            need(box_payload(rep_box) == box_payload(leaf["route"]["box"]),
                 "representative leaf replay")
            ref_route = c41.route_at_path(reflected, ref_path, context["config"])
            need(ref_route["classification"] == EXPECTED_CLASSES[pair]
                 and box_payload(ref_route["box"]) == box_payload(ref_box),
                 "reflected leaf replay")
            rep_cert = oracle.certificate(
                pair, "REPRESENTATIVE", path,
                task["c38_source"]["representative_origin_key"],
                task["cell"], rep_box, "AMBIENT_TERMINAL_LEAF", 1,
            )
            ref_cert = oracle.certificate(
                pair, "REFLECTED", ref_path,
                reflected["c38_source"]["representative_origin_key"],
                reflected["cell"], ref_box, "AMBIENT_TERMINAL_LEAF", 1,
            )
            for orientation, cert, cert_path in (
                ("REPRESENTATIVE", rep_cert, path),
                ("REFLECTED", ref_cert, ref_path),
            ):
                semantic = {
                    "schema": CANDIDATE_SCHEMA + ".closed-leaf-certificate",
                    "pair_index": pair,
                    "orientation": orientation,
                    "path": cert_path,
                    "source_relative_fraction": qstr(leaf["relative_fraction"]),
                    "absolute_parent_fraction": qstr(
                        SOURCE_FRACTION * leaf["relative_fraction"]
                    ),
                    "full_closed_box_certificate": cert,
                    "strict_terminal_excluded": True,
                    "local_round144_terminal_credit": 1,
                    "lower_dimensional_ambient_credit": 0,
                    "D02_gate_credit": 0,
                }
                row = close_expected(
                    semantic, "closed_leaf_certificate_id", "c43-leaf:"
                )
                result["leaves"].append(row)
                leaf_map[(pair, orientation, cert_path)] = row
            semantic = {
                "schema": CANDIDATE_SCHEMA + ".reflection-transport",
                "pair_index": pair,
                "representative_path": path,
                "reflected_path": ref_path,
                "representative_certificate_id":
                    leaf_map[(pair, "REPRESENTATIVE", path)][
                        "closed_leaf_certificate_id"
                    ],
                "reflected_certificate_id":
                    leaf_map[(pair, "REFLECTED", ref_path)][
                        "closed_leaf_certificate_id"
                    ],
                "representative_closed_box": box_payload(rep_box),
                "reflected_closed_box": box_payload(ref_box),
                "exact_map": "Jy:(t,p,s)->chart-dependent(-t,-p,s)",
                "endpoint_order_reversal_materialized": True,
                "reflected_route_recomputed_independently": True,
                "representative_classification": rep_cert["strict_disposition"],
                "reflected_classification": ref_cert["strict_disposition"],
                "transport_carries_no_independent_credit": True,
                "D02_gate_credit": 0,
            }
            result["reflection"].append(close_expected(
                semantic, "reflection_transport_id", "c43-reflection:"
            ))
    result["leaves"].sort(key=lambda row: (
        row["pair_index"], row["orientation"], row["path"]
    ))
    result["reflection"].sort(key=lambda row: (
        row["pair_index"], row["representative_path"]
    ))

    for pair in eligible_pairs:
        task = context["tasks"][pair]
        reflected = make_reflected_task(task, cells)
        for split in trees[pair]["splits"]:
            orientation_rows = []
            for orientation, current in (
                ("REPRESENTATIVE", task), ("REFLECTED", reflected)
            ):
                if orientation == "REPRESENTATIVE":
                    parent_path = split["parent_path"]
                    lower_path, upper_path = split["child_paths"]
                    parent_box = split["parent_box"]
                    children = split["children"]
                    axis = split["axis"]
                    origin = task["c38_source"]["representative_origin_key"]
                else:
                    parent_path, _a, parent_box = reflected_path_and_box(
                        task, split["parent_path"], cells
                    )
                    child0, _b, box0 = reflected_path_and_box(
                        task, split["child_paths"][0], cells
                    )
                    child1, _c, box1 = reflected_path_and_box(
                        task, split["child_paths"][1], cells
                    )
                    mapping = dict(sorted(((child0, box0), (child1, box1))))
                    lower_path, upper_path = parent_path + "0", parent_path + "1"
                    need(set(mapping) == {lower_path, upper_path},
                         "reflected child path cover")
                    children = (mapping[lower_path], mapping[upper_path])
                    axis = c41.c38.round166.longest_axis(parent_box)
                    origin = reflected["c38_source"]["representative_origin_key"]
                face_name = ("t", "p")[axis] + "_upper"
                shared = make_face_box(children[0], face_name)
                direct = oracle.certificate(
                    pair, orientation, parent_path + ".shared", origin,
                    current["cell"], shared, "INTERNAL_SPLIT_FACE", 0,
                )
                if axis == 0:
                    endpoint_boxes = [
                        type(shared)(shared.t0, shared.t0, shared.p0, shared.p0,
                                     shared.s0, shared.s1, 0, "endpoint0"),
                        type(shared)(shared.t0, shared.t0, shared.p1, shared.p1,
                                     shared.s0, shared.s1, 0, "endpoint1"),
                    ]
                else:
                    endpoint_boxes = [
                        type(shared)(shared.t0, shared.t0, shared.p0, shared.p0,
                                     shared.s0, shared.s1, 0, "endpoint0"),
                        type(shared)(shared.t1, shared.t1, shared.p0, shared.p0,
                                     shared.s0, shared.s1, 0, "endpoint1"),
                    ]
                orientation_leaves = [
                    row for (p, o, _path), row in leaf_map.items()
                    if p == pair and o == orientation
                ]
                endpoints = []
                for ordinal, point in enumerate(endpoint_boxes):
                    incidents = sorted(
                        row["path"] for row in orientation_leaves
                        if box_contains(
                            row["full_closed_box_certificate"]["closed_box"],
                            point.t0, point.p0,
                        )
                    )
                    need(bool(incidents), "internal point incidence")
                    point_cert = oracle.certificate(
                        pair, orientation,
                        parent_path + f".vertex{ordinal}", origin,
                        current["cell"], point, "INTERNAL_SPLIT_VERTEX", 0,
                    )
                    endpoints.append({
                        "coordinate": {
                            "t": qstr(point.t0), "p": qstr(point.p0), "s": "0"
                        },
                        "incident_terminal_leaf_paths": incidents,
                        "canonical_owner_path": incidents[0],
                        "direct_closed_point_certificate": point_cert,
                        "vertex_ambient_credit": 0,
                    })
                mid_t, mid_p = ((shared.t0 + shared.t1) / 2,
                                (shared.p0 + shared.p1) / 2)
                incidents = sorted(
                    row["path"] for row in orientation_leaves
                    if box_contains(
                        row["full_closed_box_certificate"]["closed_box"],
                        mid_t, mid_p,
                    )
                )
                need(incidents == [lower_path, upper_path],
                     "internal face complete incidence")
                orientation_rows.append({
                    "orientation": orientation,
                    "parent_path": parent_path,
                    "split_axis": ("t", "p")[axis],
                    "shared_face_closed_box": box_payload(shared),
                    "incident_terminal_leaf_paths": incidents,
                    "half_open_owner_path": lower_path,
                    "upper_bit_excludes_duplicate_face": True,
                    "direct_closed_face_certificate": direct,
                    "endpoint_vertices": endpoints,
                    "lower_dimensional_ambient_credit": 0,
                })
            semantic = {
                "schema": CANDIDATE_SCHEMA + ".internal-strata-incidence",
                "pair_index": pair,
                "representative_split_parent_path": split["parent_path"],
                "orientation_restrictions": orientation_rows,
                "representative_and_reflected_restrictions_explicit": True,
                "physical_dimension_credit": 0,
                "D02_gate_credit": 0,
            }
            result["internal"].append(close_expected(
                semantic, "internal_strata_incidence_id", "c43-internal:"
            ))
    result["internal"].sort(key=lambda row: (
        row["pair_index"], row["representative_split_parent_path"]
    ))

    terminal_ids = {
        context["C42_source"]["C41_target_ambient_cell_id"],
        *(context["C41_rows"][pair]["c41_ambient_cell_id"]
          for pair in eligible_pairs),
    }
    for pair in eligible_pairs:
        for face in ("t_lower", "t_upper", "p_lower", "p_upper"):
            orientation_rows = []
            for orientation in ("REPRESENTATIVE", "REFLECTED"):
                origin, cell, box, path = target_orientation(
                    pair, orientation, context
                )
                partition = face_partition(
                    geometry, orientation, box, face, terminal_ids
                )
                need(partition["all_required_segment_and_breakpoint_owners_terminal"],
                     "eligible face owners terminal")
                segments = []
                for ordinal, segment in enumerate(partition["segments"]):
                    lo, hi = map(Q, segment["interval"])
                    restricted = make_face_box(box, face, lo, hi)
                    segments.append(oracle.certificate(
                        pair, orientation,
                        path + "." + face + f".segment{ordinal}",
                        origin, cell, restricted,
                        "SOURCE_EXTERIOR_FACE_SEGMENT", 0,
                    ))
                breakpoints = []
                for ordinal, point in enumerate(partition["interior_breakpoints"]):
                    value = point["coordinate"]
                    restricted = type(box)(
                        Q(value["t"]), Q(value["t"]),
                        Q(value["p"]), Q(value["p"]), Q(0), Q(0), 0,
                        "breakpoint",
                    )
                    breakpoints.append(oracle.certificate(
                        pair, orientation,
                        path + "." + face + f".breakpoint{ordinal}",
                        origin, cell, restricted,
                        "SOURCE_FACE_INTERNAL_BREAKPOINT", 0,
                    ))
                orientation_rows.append({
                    "orientation": orientation,
                    "target_path": path,
                    "source_face": face,
                    "global_incidence_partition": partition,
                    "direct_closed_segment_certificates": segments,
                    "direct_internal_breakpoint_certificates": breakpoints,
                    "all_canonical_owners_terminal_after_C43_subset": True,
                    "face_ambient_credit": 0,
                })
            semantic = {
                "schema": CANDIDATE_SCHEMA + ".source-face-owner-incidence",
                "pair_index": pair,
                "source_face": face,
                "C41_boundary_outer_id":
                    context["boundaries"][pair]["boundary_corner_outer_id"],
                "orientation_restrictions": orientation_rows,
                "representative_and_reflected_restrictions_explicit": True,
                "global_owner_rule":
                    "LEXICOGRAPHIC_MINIMUM_(PATH,PAIR_INDEX,AMBIENT_ID)",
                "D02_gate_credit": 0,
            }
            result["faces"].append(close_expected(
                semantic, "source_face_owner_incidence_id", "c43-face:"
            ))
        for corner in ("t0p0", "t0p1", "t1p0", "t1p1"):
            orientation_rows = []
            for orientation in ("REPRESENTATIVE", "REFLECTED"):
                origin, cell, box, path = target_orientation(
                    pair, orientation, context
                )
                point = make_point_box(box, corner)
                incident = point_incidents(
                    geometry, orientation, point.t0, point.p0, terminal_ids
                )
                need(incident[0]["terminal_after_C43_subset"],
                     "eligible corner owner terminal")
                direct = oracle.certificate(
                    pair, orientation, path + "." + corner,
                    origin, cell, point, "SOURCE_EXTERIOR_CORNER", 0,
                )
                orientation_rows.append({
                    "orientation": orientation,
                    "target_path": path,
                    "coordinate": {
                        "t": qstr(point.t0), "p": qstr(point.p0), "s": "0"
                    },
                    "global_incident_ambient_cells": incident,
                    "canonical_owner": incident[0],
                    "canonical_owner_terminal_after_C43_subset": True,
                    "direct_closed_point_certificate": direct,
                    "corner_ambient_credit": 0,
                })
            semantic = {
                "schema": CANDIDATE_SCHEMA + ".source-corner-owner-incidence",
                "pair_index": pair,
                "source_corner": corner,
                "C41_boundary_outer_id":
                    context["boundaries"][pair]["boundary_corner_outer_id"],
                "orientation_restrictions": orientation_rows,
                "representative_and_reflected_restrictions_explicit": True,
                "global_owner_rule":
                    "LEXICOGRAPHIC_MINIMUM_(PATH,PAIR_INDEX,AMBIENT_ID)",
                "D02_gate_credit": 0,
            }
            result["corners"].append(close_expected(
                semantic, "source_corner_owner_incidence_id", "c43-corner:"
            ))
    result["faces"].sort(key=lambda row: (row["pair_index"], row["source_face"]))
    result["corners"].sort(key=lambda row: (
        row["pair_index"], row["source_corner"]
    ))

    newly = 0
    for prior in context["C42_parents"]:
        pair = prior["pair_index"]
        eligible = pair in eligible_pairs
        gain = SOURCE_FRACTION if eligible else Q(0)
        terminal = Q(prior["terminal_excluded_parent_volume"]) + gain
        unresolved = Q(prior["unresolved_parent_volume"]) - gain
        leaf_count = prior["leaf_count"] + (
            len(trees[pair]["leaves"]) - 1 if eligible else 0
        )
        terminal_leaves = prior["terminal_leaf_count"] + (
            len(trees[pair]["leaves"]) if eligible else 0
        )
        nonterminal = prior["nonterminal_leaf_count"] - int(eligible)
        whole = terminal == 1 and unresolved == 0 and nonterminal == 0
        new = whole and not (
            prior["whole_representative_parent_terminal"]
            and prior["whole_reflected_parent_terminal"]
        )
        newly += int(new)
        semantic = {
            "schema": CANDIDATE_SCHEMA + ".representative-parent-conservation",
            "pair_index": pair,
            "C42_parent_row_sha256": prior["row_sha256"],
            "C42_terminal_excluded_parent_volume":
                prior["terminal_excluded_parent_volume"],
            "C42_unresolved_parent_volume": prior["unresolved_parent_volume"],
            "C42_leaf_count": prior["leaf_count"],
            "C42_terminal_leaf_count": prior["terminal_leaf_count"],
            "C42_nonterminal_leaf_count": prior["nonterminal_leaf_count"],
            "C43_terminal_gain": qstr(gain),
            "terminal_excluded_parent_volume": qstr(terminal),
            "unresolved_parent_volume": qstr(unresolved),
            "parent_Kraft_conservation": "1",
            "leaf_count": leaf_count,
            "terminal_leaf_count": terminal_leaves,
            "nonterminal_leaf_count": nonterminal,
            "newly_whole_terminal_vs_C42": new,
            "whole_representative_parent_terminal": whole,
            "whole_reflected_parent_terminal": whole,
            "terminal_reflection_recomputation_materialized": (
                True if eligible
                else prior["terminal_reflection_transport_materialized"]
            ),
            "canonical_boundary_owner_eligible": True if eligible else None,
            "blocked_source_zero_credit": pair in blocked_pairs,
            "C34_common_refinement_credit": 2 if whole else 0,
            "D02_gate_credit": 0,
        }
        result["parents"].append(close_expected(semantic, None, None))
    need(newly == 2 and sum(
        row["whole_representative_parent_terminal"]
        and row["whole_reflected_parent_terminal"]
        for row in result["parents"]
    ) == 289, "exact parent credit")
    need(result["parents"][C42_PAIR]["C43_terminal_gain"] == "0",
         "pair391 unchanged")
    return result


def expected_census(eligible: tuple[int, ...] = ELIGIBLE,
                    blocked: tuple[int, ...] = BLOCKED) -> dict[str, Any]:
    need(len(eligible) == 2 and set(eligible).isdisjoint(blocked),
         "two derived eligible parents")
    value = {
        "schema": CANDIDATE_SCHEMA + ".round144-census",
        "baseline": "INSTALLED_C42_F1_AUTHORITY",
        "CONNECTED_TO_KNOWN": 0,
        "EARLIEST_PREFIX_EXCLUDED": 75_386 + 2 * len(eligible),
        "SOURCE_GRAZING_OR_CEMETERY": 0,
        "TYPED_EVENT_GRAPH": 296,
        "UNRESOLVED_R1648_CONTINUATION": 1_150 - 2 * len(eligible),
        "terminal_total": 76_832,
        "unresolved_zero": False,
        "eligible_representative_delta": len(eligible),
        "paired_terminal_delta": 2 * len(eligible),
        "blocked_zero_credit_pairs": list(blocked),
        "D02_gate_credit": 0,
    }
    value["census_object_sha256"] = digest(value)
    return value


def independently_expected_result(
    captured: dict[str, Any], reconstructed: dict[str, list[dict[str, Any]]],
    census: dict[str, Any], eligible: tuple[int, ...],
    blocked: tuple[int, ...],
) -> dict[str, Any]:
    descriptors = {}
    for key, (descriptor_key, filename, _count, order, _id, _prefix) \
            in LEDGERS.items():
        raw = captured["raw"][filename]
        rows = reconstructed[key]
        sequence = hashlib.sha256("".join(
            row["row_sha256"] + "\n" for row in rows
        ).encode("ascii")).hexdigest()
        descriptors[descriptor_key] = {
            "filename": filename,
            "order": order,
            "row_count": len(rows),
            "row_hash_line_sequence_sha256": sequence,
            "sha256": bytes_sha(raw),
            "size": len(raw),
        }
    parent_rows = reconstructed["parents"]
    whole = sum(
        row["whole_representative_parent_terminal"]
        and row["whole_reflected_parent_terminal"]
        for row in parent_rows
    )
    newly = sum(row["newly_whole_terminal_vs_C42"] for row in parent_rows)
    closure = {
        "source_preflight_count": len(reconstructed["preflight"]),
        "eligible_exact_source_count": len(reconstructed["sources"]),
        "blocked_zero_credit_source_count": len(blocked),
        "adaptive_split_count": len(reconstructed["splits"]),
        "representative_terminal_leaf_count": len(reconstructed["leaves"]) // 2,
        "reflected_terminal_leaf_count": len(reconstructed["leaves"]) // 2,
        "closed_leaf_certificate_count": len(reconstructed["leaves"]),
        "reflection_transport_count": len(reconstructed["reflection"]),
        "internal_split_incidence_count": len(reconstructed["internal"]),
        "source_face_slot_count": len(reconstructed["faces"]),
        "source_corner_slot_count": len(reconstructed["corners"]),
        "whole_representative_parent_count": whole,
        "whole_paired_coarse_cell_count": 2 * whole,
        "newly_whole_representative_parent_count": newly,
        "newly_whole_paired_coarse_cell_count": 2 * newly,
        "remaining_representative_parent_count": 862 - whole,
        "parent_row_count": len(parent_rows),
    }
    result = {
        "schema": CANDIDATE_SCHEMA,
        "status": EXPECTED_CANDIDATE_STATUS,
        "formal_producer_run": True,
        "producer_output_is_authority": False,
        "formal_authority": False,
        "authority_pointer_installed": False,
        "independent_C43_audit_outstanding": True,
        "producer_source_sha256": EXPECTED_PRODUCER_SOURCE,
        "installed_C42_authority": {
            "candidate_object_sha256": EXPECTED_C42_OBJECT,
            "independent_audit_object_sha256": EXPECTED_C42_AUDIT_OBJECT,
            "authority_seal_object_sha256": EXPECTED_C42_SEAL_OBJECT,
            "installation_receipt_object_sha256": EXPECTED_C42_RECEIPT_OBJECT,
            "root_manifest_sha256": EXPECTED_C42_MANIFEST,
        },
        "target_discovery": {
            "derived_post_C42_sole_deficit_pairs": list(TARGET_PAIRS),
            "owner_eligible_pairs": list(eligible),
            "canonical_residual_owner_blocked_pairs": list(blocked),
            "blocked_pairs_receive_credit": False,
        },
        "closure_census": closure,
        "ledgers": descriptors,
        "round144_census": {
            "filename": "round144_census.json",
            "sha256": bytes_sha(captured["raw"]["round144_census.json"]),
            "object_sha256": census["census_object_sha256"],
            "EARLIEST_PREFIX_EXCLUDED":
                census["EARLIEST_PREFIX_EXCLUDED"],
            "TYPED_EVENT_GRAPH": census["TYPED_EVENT_GRAPH"],
            "UNRESOLVED_R1648_CONTINUATION":
                census["UNRESOLVED_R1648_CONTINUATION"],
            "unresolved_zero": False,
        },
        "nonpromotion_lock": {
            "filename": "C43_SUBSET_CLOSURE.lock",
            "sha256": bytes_sha(LOCK_BYTES),
            "producer_output_is_authority": False,
        },
        "strict_nonpromotion": {
            "D02": "BLOCKED_BY_1146_COMPLETE_R1648_CONTINUATIONS",
            "D03": "UNAUTHORIZED", "D04": "NOT_MINTED",
            "Gate5": "10/18", "complete_global_18_field_blocks": 0,
            "CM2": "NO-GO_FOR_CLAIM",
        },
        "required_next": (
            "independent C43 audit before any separate authority installation "
            "transaction; continue blocked boundary owners and the remaining "
            "573 representatives"
        ),
    }
    result["object_sha256"] = digest(result)
    return result


def independently_expected_receipt(
    observed: dict[str, Any], expected_result: dict[str, Any],
    manifest_sha256: str, candidate_path: str,
    eligible: tuple[int, ...], blocked: tuple[int, ...],
) -> dict[str, Any]:
    for field in ("pid", "proc_start_ticks", "created_unix_ns"):
        need(type(observed.get(field)) is int and observed[field] > 0,
             "receipt positive dynamic field:" + field)
    value = {
        "schema": CANDIDATE_SCHEMA + ".execution-receipt",
        "status": EXPECTED_RECEIPT_STATUS,
        "InvocationID": EXPECTED_INVOCATION,
        "pid": observed["pid"],
        "proc_start_ticks": observed["proc_start_ticks"],
        "producer_source_sha256": EXPECTED_PRODUCER_SOURCE,
        "candidate_path": candidate_path,
        "candidate_object_sha256": expected_result["object_sha256"],
        "root_manifest_sha256": manifest_sha256,
        "installed_C42_candidate_object_sha256": EXPECTED_C42_OBJECT,
        "eligible_pairs": list(eligible),
        "blocked_zero_credit_pairs": list(blocked),
        "producer_output_is_authority": False,
        "authority_pointer_installed": False,
        "created_unix_ns": observed["created_unix_ns"],
    }
    value["receipt_object_sha256"] = digest(value)
    return value


def validate_result(result: dict[str, Any], baseline: dict[str, Any]) -> None:
    self_closed(result, "object_sha256", "result semantic")
    need(result == baseline, "exact independently validated result semantic")
    need(
        result["formal_producer_run"] is True
        and result["producer_output_is_authority"] is False
        and result["formal_authority"] is False
        and result["authority_pointer_installed"] is False
        and result["independent_C43_audit_outstanding"] is True
        and result["strict_nonpromotion"] == {
            "D02": "BLOCKED_BY_1146_COMPLETE_R1648_CONTINUATIONS",
            "D03": "UNAUTHORIZED", "D04": "NOT_MINTED",
            "Gate5": "10/18", "complete_global_18_field_blocks": 0,
            "CM2": "NO-GO_FOR_CLAIM",
        },
        "C43 strict nonauthority semantics",
    )


def validate_receipt_semantic(value: dict[str, Any],
                              baseline: dict[str, Any]) -> None:
    self_closed(value, "receipt_object_sha256", "receipt semantic")
    need(value == baseline, "exact independently validated receipt semantic")


def validate_rows(value: dict[str, list[dict[str, Any]]],
                  expected: dict[str, list[dict[str, Any]]]) -> None:
    for key in LEDGERS:
        if value[key] != expected[key]:
            raise Reject(
                "independent ledger replay:" + key + ":"
                + first_difference(value[key], expected[key])
            )


def first_difference(left: Any, right: Any, path: str = "$") -> str:
    """Return one compact deterministic mismatch path for fail-closed debug."""
    if type(left) is not type(right):
        return path + ":type:" + type(left).__name__ + "!=" + type(right).__name__
    if isinstance(left, dict):
        if set(left) != set(right):
            return path + ":keys:" + repr(sorted(set(left) ^ set(right)))
        ordered_keys = sorted(
            left,
            key=lambda key: (
                key == "row_sha256" or key.endswith("_id")
                or key == "certificate_id",
                key,
            ),
        )
        for key in ordered_keys:
            if left[key] != right[key]:
                return first_difference(left[key], right[key], path + "." + key)
        return path + ":dict"
    if isinstance(left, list):
        if len(left) != len(right):
            return path + f":length:{len(left)}!={len(right)}"
        for ordinal, (one, two) in enumerate(zip(left, right)):
            if one != two:
                return first_difference(one, two, path + f"[{ordinal}]")
        return path + ":list"
    return path + ":" + repr(left)[:160] + "!=" + repr(right)[:160]


def reclose_nested(value: Any) -> None:
    if isinstance(value, list):
        for item in value:
            reclose_nested(item)
    elif isinstance(value, dict):
        for item in list(value.values()):
            reclose_nested(item)
        if "certificate_id" in value and str(value.get("schema", "")).endswith(
            ".direct-restriction"
        ):
            value.pop("certificate_id", None)
            value["certificate_id"] = "c43-cert:" + digest(value)


def reclose_row(key: str, row: dict[str, Any]) -> dict[str, Any]:
    value = copy.deepcopy(row)
    reclose_nested(value)
    _descriptor, _filename, _count, _order, id_field, prefix = LEDGERS[key]
    value.pop("row_sha256", None)
    if id_field is not None:
        value.pop(id_field, None)
        value[id_field] = prefix + digest(value)
    value["row_sha256"] = digest(value)
    return value


def rejected(label: str, action: Callable[[], None]) -> bool:
    try:
        action()
    except Reject:
        return True
    raise Reject("coherent attack accepted:" + label)


def set_path(value: Any, path: tuple[Any, ...], replacement: Any) -> None:
    target = value
    for part in path[:-1]:
        target = target[part]
    target[path[-1]] = replacement


def write_new_file(path: Path, raw: bytes) -> None:
    """Create one bounded test-transaction member without following links."""
    flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL \
        | getattr(os, "O_CLOEXEC", 0) | getattr(os, "O_NOFOLLOW", 0)
    descriptor = os.open(path, flags, 0o600)
    try:
        view = memoryview(raw)
        while view:
            written = os.write(descriptor, view)
            need(written > 0, "test transaction write progress")
            view = view[written:]
        os.fsync(descriptor)
    finally:
        os.close(descriptor)


def gzip_rows(rows: list[dict[str, Any]]) -> bytes:
    plain = b"".join(canonical(row) + b"\n" for row in rows)
    return gzip.compress(plain, compresslevel=9, mtime=0)


def transaction_closure_census(
    rows: dict[str, list[dict[str, Any]]], result: dict[str, Any],
) -> dict[str, Any]:
    representative = sum(
        row.get("orientation") == "REPRESENTATIVE" for row in rows["leaves"]
    )
    reflected = sum(
        row.get("orientation") == "REFLECTED" for row in rows["leaves"]
    )
    whole = sum(
        row.get("whole_representative_parent_terminal") is True
        and row.get("whole_reflected_parent_terminal") is True
        for row in rows["parents"]
    )
    newly = sum(
        row.get("newly_whole_terminal_vs_C42", 0)
        for row in rows["parents"]
    )
    blocked = result["target_discovery"][
        "canonical_residual_owner_blocked_pairs"
    ]
    return {
        "source_preflight_count": len(rows["preflight"]),
        "eligible_exact_source_count": len(rows["sources"]),
        "blocked_zero_credit_source_count": len(blocked),
        "adaptive_split_count": len(rows["splits"]),
        "representative_terminal_leaf_count": representative,
        "reflected_terminal_leaf_count": reflected,
        "closed_leaf_certificate_count": len(rows["leaves"]),
        "reflection_transport_count": len(rows["reflection"]),
        "internal_split_incidence_count": len(rows["internal"]),
        "source_face_slot_count": len(rows["faces"]),
        "source_corner_slot_count": len(rows["corners"]),
        "whole_representative_parent_count": whole,
        "whole_paired_coarse_cell_count": 2 * whole,
        "newly_whole_representative_parent_count": newly,
        "newly_whole_paired_coarse_cell_count": 2 * newly,
        "remaining_representative_parent_count": len(rows["parents"]) - whole,
        "parent_row_count": len(rows["parents"]),
    }


def materialize_test_transaction(
    root: Path, candidate: dict[str, Any], receipt: dict[str, Any],
    *,
    rows_mutator: Callable[[dict[str, list[dict[str, Any]]]], None] | None = None,
    census_mutator: Callable[[dict[str, Any]], None] | None = None,
    result_mutator: Callable[[dict[str, Any]], None] | None = None,
    result_mutator_after_sync: bool = False,
    receipt_mutator: Callable[[dict[str, Any]], None] | None = None,
) -> tuple[Path, Path]:
    """Build a complete, self-consistent hash container for one attack.

    The hostile semantic is carried through row JSON, gzip bytes, descriptors,
    result self-hash, root manifest, and execution-receipt bindings.  Thus the
    semantic validator cannot reject merely because an outer hash was stale.
    """
    directory = root / "candidate"
    directory.mkdir(mode=0o700)
    rows = copy.deepcopy(candidate["rows"])
    census = copy.deepcopy(candidate["census"])
    result = copy.deepcopy(candidate["result"])
    value_receipt = copy.deepcopy(receipt)

    if rows_mutator is not None:
        rows_mutator(rows)
    for key in LEDGERS:
        rows[key] = [reclose_row(key, row) for row in rows[key]]

    if census_mutator is not None:
        census_mutator(census)
    census.pop("census_object_sha256", None)
    census["census_object_sha256"] = digest(census)

    if result_mutator is not None and not result_mutator_after_sync:
        result_mutator(result)

    raw: dict[str, bytes] = {
        "C43_SUBSET_CLOSURE.lock": LOCK_BYTES,
        "round144_census.json": canonical(census) + b"\n",
    }
    descriptors: dict[str, dict[str, Any]] = {}
    for key, (descriptor_key, filename, _count, order, _id, _prefix) \
            in LEDGERS.items():
        ledger_raw = gzip_rows(rows[key])
        raw[filename] = ledger_raw
        sequence = hashlib.sha256("".join(
            row["row_sha256"] + "\n" for row in rows[key]
        ).encode("ascii")).hexdigest()
        descriptors[descriptor_key] = {
            "filename": filename,
            "order": order,
            "row_count": len(rows[key]),
            "row_hash_line_sequence_sha256": sequence,
            "sha256": bytes_sha(ledger_raw),
            "size": len(ledger_raw),
        }
    result["ledgers"] = descriptors
    result["closure_census"] = transaction_closure_census(rows, result)
    result["round144_census"] = {
        "filename": "round144_census.json",
        "sha256": bytes_sha(raw["round144_census.json"]),
        "object_sha256": census["census_object_sha256"],
        "EARLIEST_PREFIX_EXCLUDED": census["EARLIEST_PREFIX_EXCLUDED"],
        "TYPED_EVENT_GRAPH": census["TYPED_EVENT_GRAPH"],
        "UNRESOLVED_R1648_CONTINUATION":
            census["UNRESOLVED_R1648_CONTINUATION"],
        "unresolved_zero": census["unresolved_zero"],
    }
    result["nonpromotion_lock"] = {
        "filename": "C43_SUBSET_CLOSURE.lock",
        "sha256": bytes_sha(LOCK_BYTES),
        "producer_output_is_authority": False,
    }
    if result_mutator is not None and result_mutator_after_sync:
        result_mutator(result)
    result.pop("object_sha256", None)
    result["object_sha256"] = digest(result)
    raw["result.json"] = canonical(result) + b"\n"

    manifest = b"".join(
        (bytes_sha(raw[name]) + "  " + name + "\n").encode("ascii")
        for name in INVENTORY if name != "root_manifest.sha256"
    )
    raw["root_manifest.sha256"] = manifest
    need(set(raw) == set(INVENTORY), "complete hostile inventory")
    for name in INVENTORY:
        write_new_file(directory / name, raw[name])
    fsync_directory(directory)

    value_receipt.update({
        "producer_source_sha256": result["producer_source_sha256"],
        "candidate_path": str(directory.relative_to(ROOT)),
        "candidate_object_sha256": result["object_sha256"],
        "root_manifest_sha256": bytes_sha(manifest),
        "eligible_pairs": result["target_discovery"]["owner_eligible_pairs"],
        "blocked_zero_credit_pairs": result["target_discovery"][
            "canonical_residual_owner_blocked_pairs"
        ],
        "producer_output_is_authority":
            result["producer_output_is_authority"],
        "authority_pointer_installed": result["authority_pointer_installed"],
    })
    if receipt_mutator is not None:
        receipt_mutator(value_receipt)
    value_receipt.pop("receipt_object_sha256", None)
    value_receipt["receipt_object_sha256"] = digest(value_receipt)
    receipt_path = root / "execution_receipt.json"
    write_new_file(receipt_path, canonical(value_receipt) + b"\n")
    fsync_directory(root)
    return directory, receipt_path


def validate_test_transaction(
    directory: Path, receipt_path: Path,
    expected_rows_value: dict[str, list[dict[str, Any]]],
    census: dict[str, Any], eligible: tuple[int, ...],
    blocked: tuple[int, ...],
) -> None:
    captured = capture_candidate(directory, enforce_pins=False)
    value_receipt = capture_receipt(
        receipt_path, captured, EXPECTED_INVOCATION, enforce_pins=False
    )
    validate_rows(captured["rows"], expected_rows_value)
    need(captured["census"] == census,
         "hostile transaction census semantics")
    result = independently_expected_result(
        captured, expected_rows_value, census, eligible, blocked
    )
    validate_result(captured["result"], result)
    expected_receipt = independently_expected_receipt(
        value_receipt, result, captured["manifest_sha256"],
        str(captured["directory"].relative_to(ROOT)), eligible, blocked,
    )
    validate_receipt_semantic(value_receipt, expected_receipt)


def transaction_trial(
    candidate: dict[str, Any], receipt: dict[str, Any],
    expected_rows_value: dict[str, list[dict[str, Any]]],
    census: dict[str, Any], eligible: tuple[int, ...],
    blocked: tuple[int, ...], **mutators: Any,
) -> None:
    with tempfile.TemporaryDirectory(
        prefix="c43-coherent-transaction-", dir=AUDIT_ROOT
    ) as temporary:
        directory, receipt_path = materialize_test_transaction(
            Path(temporary), candidate, receipt, **mutators
        )
        validate_test_transaction(
            directory, receipt_path, expected_rows_value,
            census, eligible, blocked,
        )


def mutation_suite(candidate: dict[str, Any], receipt: dict[str, Any],
                   expected: dict[str, list[dict[str, Any]]],
                   census: dict[str, Any], eligible: tuple[int, ...],
                   blocked: tuple[int, ...]) \
        -> dict[str, bool]:
    attacks: dict[str, bool] = {}

    # A no-mutation transaction rebuilt with fresh gzip bytes and a fresh
    # manifest/receipt must pass the same generic capture and semantic entry.
    transaction_trial(
        candidate, receipt, expected, census, eligible, blocked
    )

    def result_attack(label: str, path: tuple[Any, ...], replacement: Any) -> None:
        attacks[label] = rejected(
            label, lambda: transaction_trial(
                candidate, receipt, expected, census, eligible, blocked,
                result_mutator=lambda value: set_path(
                    value, path, replacement
                ),
                result_mutator_after_sync=(path[0] == "closure_census"),
            )
        )

    def census_attack(label: str, field: str, replacement: Any) -> None:
        attacks[label] = rejected(
            label, lambda: transaction_trial(
                candidate, receipt, expected, census, eligible, blocked,
                census_mutator=lambda value: value.__setitem__(
                    field, replacement
                ),
            )
        )

    def receipt_attack(label: str, field: str, replacement: Any) -> None:
        attacks[label] = rejected(
            label, lambda: transaction_trial(
                candidate, receipt, expected, census, eligible, blocked,
                receipt_mutator=lambda value: value.__setitem__(
                    field, replacement
                ),
            )
        )

    def row_attack(label: str, key: str, index: int,
                   path: tuple[Any, ...], replacement: Any) -> None:
        attacks[label] = rejected(
            label, lambda: transaction_trial(
                candidate, receipt, expected, census, eligible, blocked,
                rows_mutator=lambda value: set_path(
                    value[key][index], path, replacement
                ),
            )
        )

    def list_attack(label: str, key: str,
                    mutate: Callable[[list[dict[str, Any]]], None]) -> None:
        attacks[label] = rejected(
            label, lambda: transaction_trial(
                candidate, receipt, expected, census, eligible, blocked,
                rows_mutator=lambda value: mutate(value[key]),
            )
        )

    result_attack("result_formal_authority", ("formal_authority",), True)
    result_attack("result_producer_authority", ("producer_output_is_authority",), True)
    result_attack("result_pointer_installed", ("authority_pointer_installed",), True)
    result_attack("result_audit_not_outstanding", ("independent_C43_audit_outstanding",), False)
    result_attack("result_credits_pair97", ("target_discovery", "owner_eligible_pairs"), [97, 592, 715])
    result_attack("result_drops_blocked664", ("target_discovery", "canonical_residual_owner_blocked_pairs"), [97, 211])
    result_attack("result_blocked_credit", ("target_discovery", "blocked_pairs_receive_credit"), True)
    result_attack("result_whole_290", ("closure_census", "whole_representative_parent_count"), 290)
    result_attack("result_paired_580", ("closure_census", "whole_paired_coarse_cell_count"), 580)
    result_attack("result_remaining_572", ("closure_census", "remaining_representative_parent_count"), 572)
    result_attack("result_D02_PASS", ("strict_nonpromotion", "D02"), "PASS")
    result_attack("result_CM2_GO", ("strict_nonpromotion", "CM2"), "GO")

    census_attack("census_excluded_plus_one", "EARLIEST_PREFIX_EXCLUDED", 75_391)
    census_attack("census_unresolved_minus_one", "UNRESOLVED_R1648_CONTINUATION", 1_145)
    census_attack("census_unresolved_zero", "unresolved_zero", True)
    census_attack("census_delta_three", "eligible_representative_delta", 3)
    census_attack("census_pair_delta_six", "paired_terminal_delta", 6)
    census_attack("census_credits_664", "blocked_zero_credit_pairs", [97, 211])

    receipt_attack("receipt_authority", "producer_output_is_authority", True)
    receipt_attack("receipt_pointer", "authority_pointer_installed", True)
    receipt_attack("receipt_candidate", "candidate_object_sha256", "0" * 64)
    receipt_attack("receipt_eligible97", "eligible_pairs", [97, 592, 715])
    receipt_attack("receipt_unblocks664", "blocked_zero_credit_pairs", [97, 211])

    row_attack("preflight_pair_swap", "preflight", 0, ("pair_index",), 98)
    row_attack("preflight_credit97", "preflight", 0, ("eligible_for_C43_credit",), True)
    row_attack("preflight_local_credit97", "preflight", 0, ("local_round144_terminal_credit",), 1)
    row_attack("preflight_drop_blocker", "preflight", 0,
               ("canonical_residual_owner_blockers",), [])
    row_attack("preflight_owner_pair", "preflight", 0,
               ("canonical_residual_owner_blockers", 0, "canonical_owner", "pair_index"), 592)
    row_attack("preflight_path592", "preflight", 2,
               ("descendant_path",), "000000001")
    row_attack("preflight_kraft", "preflight", 2, ("relative_Kraft_sum",), "511/512")
    row_attack("preflight_blocks715", "preflight", 4, ("eligible_for_C43_credit",), False)

    row_attack("source_pair97", "sources", 0, ("pair_index",), 97)
    row_attack("source_C42_seal", "sources", 0,
               ("installed_C42_seal_object_sha256",), "0" * 64)
    row_attack("source_ambient_swap", "sources", 0,
               ("C41_ambient_cell_id",), expected["sources"][1]["C41_ambient_cell_id"])
    row_attack("source_fraction", "sources", 0, ("source_fraction",), "1/256")
    row_attack("source_authority", "sources", 0, ("producer_output_is_authority",), True)
    row_attack("source_preflight_crosslink", "sources", 1,
               ("preflight_row_sha256",), expected["preflight"][2]["row_sha256"])

    row_attack("split_axis", "splits", 0, ("split_axis",), "t")
    row_attack("split_midpoint", "splits", 0, ("exact_split_midpoint",), "3618/4096")
    row_attack("split_lower_path", "splits", 0, ("lower_child_path",), "0000000001")
    row_attack("split_child_box", "splits", 0,
               ("lower_child_closed_box", "p", 1), "1809/2048")
    row_attack("split_upper_owns", "splits", 0,
               ("half_open_shared_face_owner",), "UPPER_BIT_CHILD")
    row_attack("split_fraction", "splits", 1,
               ("lower_child_fraction_multiplier",), "1/3")
    list_attack("split_missing", "splits", lambda rows: rows.pop())
    list_attack("split_duplicate", "splits", lambda rows: rows.append(copy.deepcopy(rows[0])))

    row_attack("leaf_pair97", "leaves", 0, ("pair_index",), 97)
    row_attack("leaf_not_terminal", "leaves", 0, ("strict_terminal_excluded",), False)
    row_attack("leaf_box_drift", "leaves", 0,
               ("full_closed_box_certificate", "closed_box", "p", 0), "-1")
    row_attack("leaf_word_id", "leaves", 0,
               ("full_closed_box_certificate", "official_word_key_inequality", "calculated"), "forged")
    row_attack("leaf_expected_word", "leaves", 0,
               ("full_closed_box_certificate", "official_word_key_inequality", "expected"), "forged")
    row_attack("leaf_H1_unresolved", "leaves", 0,
               ("full_closed_box_certificate", "H1_closed_box_evidence", "H1_centered", "sign"), "UNRESOLVED")
    row_attack("leaf_credit_zero", "leaves", 0, ("local_round144_terminal_credit",), 0)
    list_attack("leaf_missing", "leaves", lambda rows: rows.pop(0))

    row_attack("reflection_map", "reflection", 0, ("exact_map",), "identity")
    row_attack("reflection_path", "reflection", 0, ("reflected_path",), "000")
    row_attack("reflection_certificate", "reflection", 0,
               ("reflected_certificate_id",), "c43-leaf:" + "0" * 64)
    row_attack("reflection_not_recomputed", "reflection", 0,
               ("reflected_route_recomputed_independently",), False)
    list_attack("reflection_missing", "reflection", lambda rows: rows.pop())

    row_attack("internal_upper_owner", "internal", 0,
               ("orientation_restrictions", 0, "half_open_owner_path"),
               expected["internal"][0]["orientation_restrictions"][0]["incident_terminal_leaf_paths"][1])
    row_attack("internal_drop_endpoint", "internal", 0,
               ("orientation_restrictions", 0, "endpoint_vertices"), [])
    row_attack("internal_vertex_coordinate", "internal", 0,
               ("orientation_restrictions", 0, "endpoint_vertices", 0,
                "coordinate", "p"), "0")
    row_attack("internal_face_scope", "internal", 0,
               ("orientation_restrictions", 0, "direct_closed_face_certificate", "scope"), "AMBIENT_TERMINAL_LEAF")
    row_attack("internal_incident_missing", "internal", 0,
               ("orientation_restrictions", 0, "incident_terminal_leaf_paths"),
               [expected["internal"][0]["orientation_restrictions"][0]["incident_terminal_leaf_paths"][0]])
    list_attack("internal_missing", "internal", lambda rows: rows.pop())

    row_attack("face_owner_rule", "faces", 0, ("global_owner_rule",), "PAIR_ONLY")
    row_attack("face_owner_pair", "faces", 0,
               ("orientation_restrictions", 0, "global_incidence_partition",
                "segments", 0, "canonical_owner", "pair_index"), 190)
    row_attack("face_omit_incident", "faces", 0,
               ("orientation_restrictions", 0, "global_incidence_partition",
                "segments", 0, "incident_ambient_cells"), [])
    row_attack("face_breakpoint", "faces", 0,
               ("orientation_restrictions", 0, "global_incidence_partition",
                "breakpoints", 0), "0")
    row_attack("face_direct_box", "faces", 0,
               ("orientation_restrictions", 0, "direct_closed_segment_certificates",
                0, "closed_box", "t", 0), "0")
    row_attack("face_owner_nonterminal", "faces", 0,
               ("orientation_restrictions", 0, "all_canonical_owners_terminal_after_C43_subset"), False)
    list_attack("face_missing", "faces", lambda rows: rows.pop())

    row_attack("corner_owner_rule", "corners", 0, ("global_owner_rule",), "PAIR_ONLY")
    row_attack("corner_coordinate", "corners", 0,
               ("orientation_restrictions", 0, "coordinate", "p"), "0")
    row_attack("corner_owner_pair", "corners", 0,
               ("orientation_restrictions", 0, "canonical_owner", "pair_index"), 190)
    row_attack("corner_omit_incident", "corners", 0,
               ("orientation_restrictions", 0, "global_incident_ambient_cells"), [])
    row_attack("corner_direct_scope", "corners", 0,
               ("orientation_restrictions", 0, "direct_closed_point_certificate", "scope"), "FACE")
    list_attack("corner_missing", "corners", lambda rows: rows.pop())

    row_attack("parent_credit97", "parents", 97, ("C43_terminal_gain",), "1/512")
    row_attack("parent_credit211", "parents", 211, ("C43_terminal_gain",), "1/512")
    row_attack("parent_credit664", "parents", 664, ("C43_terminal_gain",), "1/512")
    row_attack("parent_drop592", "parents", 592, ("C43_terminal_gain",), "0")
    row_attack("parent_drop715", "parents", 715, ("C43_terminal_gain",), "0")
    row_attack("parent391_drift", "parents", 391,
               ("C42_parent_row_sha256",), "0" * 64)
    row_attack("parent592_unresolved", "parents", 592,
               ("unresolved_parent_volume",), "1/512")
    row_attack("parent592_not_whole", "parents", 592,
               ("whole_representative_parent_terminal",), False)
    row_attack("parent715_credit_one", "parents", 715,
               ("C34_common_refinement_credit",), 1)
    list_attack("parent_missing", "parents", lambda rows: rows.pop())
    list_attack("parent_reordered", "parents", lambda rows: rows.__setitem__(slice(0, 2), [rows[1], rows[0]]))

    need(len(attacks) >= 54 and all(attacks.values()),
         "at least 54 coherent attacks fail closed")
    return attacks


def audit_core(candidate_path: Path, receipt_path: Path,
               invocation: str, expected_auditor_sha256: str) -> dict[str, Any]:
    no_producer_import()
    no_c43_pointer()
    auditor_source_raw = stable_read(SELF, 8 << 20, "C43 auditor source")
    need(HEX64.fullmatch(expected_auditor_sha256) is not None
         and bytes_sha(auditor_source_raw) == expected_auditor_sha256,
         "externally frozen C43 v2 auditor source")
    validate_source_pins()
    captured = capture_candidate(candidate_path)
    receipt = capture_receipt(receipt_path, captured, invocation)
    context = load_context()
    trees = {
        pair: adaptive_tree(
            context["tasks"][pair], context["C41_rows"][pair]["path"],
            context["config"],
        )
        for pair in TARGET_PAIRS
    }
    # Phase one grants provisional closure to every freshly terminal adaptive
    # source, then derives eligibility solely from global lower-strata owners.
    provisional_terminal = {
        context["C42_source"]["C41_target_ambient_cell_id"],
        *(context["C41_rows"][pair]["c41_ambient_cell_id"]
          for pair in TARGET_PAIRS),
    }
    provisional_boundary, _provisional_geometry = build_boundaries(
        context, provisional_terminal
    )
    derived = tuple(pair for pair in TARGET_PAIRS
                    if provisional_boundary[pair]["boundary_owner_eligible"])
    need(derived == ELIGIBLE, "only 592/715 owner eligible")
    blocked = tuple(pair for pair in TARGET_PAIRS if pair not in derived)
    need(blocked == BLOCKED, "exact three owner-blocked pairs")

    # Phase two retracts all blocked provisional sources and requires a fixed
    # point: no owner decision may have depended on their provisional credit.
    actual_terminal = {
        context["C42_source"]["C41_target_ambient_cell_id"],
        *(context["C41_rows"][pair]["c41_ambient_cell_id"]
          for pair in derived),
    }
    boundary, geometry = build_boundaries(context, actual_terminal)
    fixed_point = tuple(pair for pair in TARGET_PAIRS
                        if boundary[pair]["boundary_owner_eligible"])
    need(fixed_point == derived, "eligibility fixed point after retraction")

    reconstructed = reconstruct_candidate_ledgers_v2(
        context, trees, boundary, geometry, derived, blocked
    )
    validate_rows(captured["rows"], reconstructed)
    census = expected_census(derived, blocked)
    need(captured["census"] == census, "independent round144 census replay")
    fresh_result = independently_expected_result(
        captured, reconstructed, census, derived, blocked
    )
    validate_result(captured["result"], fresh_result)
    fresh_receipt = independently_expected_receipt(
        receipt, fresh_result, captured["manifest_sha256"],
        str(captured["directory"].relative_to(ROOT)), derived, blocked,
    )
    validate_receipt_semantic(receipt, fresh_receipt)
    attacks = mutation_suite(
        captured, receipt, reconstructed, census, derived, blocked
    )

    row_sequences = {
        key: hashlib.sha256("".join(
            row["row_sha256"] + "\n" for row in rows
        ).encode("ascii")).hexdigest()
        for key, rows in reconstructed.items()
    }
    projection = {
        "schema": SCHEMA + ".cold-core-projection",
        "candidate_path": str(captured["directory"].relative_to(ROOT)),
        "candidate_object_sha256": EXPECTED_CANDIDATE_OBJECT,
        "producer_source_sha256": EXPECTED_PRODUCER_SOURCE,
        "root_manifest_sha256": EXPECTED_MANIFEST_FILE,
        "execution_receipt_object_sha256": EXPECTED_RECEIPT_OBJECT,
        "installed_C41_authority": context["C41_authority"],
        "installed_C42_candidate_object_sha256": EXPECTED_C42_OBJECT,
        "installed_C42_audit_object_sha256": EXPECTED_C42_AUDIT_OBJECT,
        "installed_C42_authority_seal_object_sha256": EXPECTED_C42_SEAL_OBJECT,
        "raw_frontier_derivation": context["frontier_derivation"],
        "derived_sole_deficit_pairs": list(TARGET_PAIRS),
        "eligible_pairs": list(derived),
        "blocked_zero_credit_pairs": list(blocked),
        "adaptive_profiles": {
            str(pair): {
                "leaf_paths": [row["path"] for row in trees[pair]["leaves"]],
                "route_count": trees[pair]["route_count"],
                "split_count": len(trees[pair]["splits"]),
                "deepest": trees[pair]["deepest"],
            }
            for pair in TARGET_PAIRS
        },
        "blocked_owner_projection_sha256": digest({
            str(pair): boundary[pair]["canonical_residual_owner_blockers"]
            for pair in blocked
        }),
        "ledger_row_sequence_sha256": row_sequences,
        "direct_closed_restriction_count": 52,
        "whole_paired_coarse_cells": 578,
        "whole_representatives": 289,
        "remaining_representatives": 573,
        "round144_census": census,
        "hostile_mutations": attacks,
        "strict_nonpromotion": captured["result"]["strict_nonpromotion"],
        "independent_auditor_source_sha256": bytes_sha(auditor_source_raw),
        "producer_output_is_authority": False,
        "authority_pointer_installed": False,
    }
    projection["projection_object_sha256"] = digest(projection)

    final = capture_candidate(candidate_path)
    final_receipt = capture_receipt(receipt_path, final, invocation)
    need(final["raw"] == captured["raw"] and final_receipt == receipt,
         "terminal candidate/receipt byte replay")
    terminal_c41 = validate_installed_c41_authority()
    terminal_c42 = validate_installed_c42_authority()
    need(terminal_c41 == context["C41_authority"],
         "terminal C41 authority replay")
    need(terminal_c42 == context["installed"],
         "terminal C42 authority replay")
    validate_frozen_manifest(C41_DIR, EXPECTED_C41_MANIFEST, 13, "terminal C41")
    validate_frozen_manifest(C42_DIR, EXPECTED_C42_MANIFEST, 8, "terminal C42")
    validate_source_pins()
    need(stable_read(SELF, 8 << 20, "terminal C43 auditor source")
         == auditor_source_raw, "auditor source terminal replay")
    no_c43_pointer()
    return projection


def cold_core(candidate: Path, receipt: Path, invocation: str,
              expected_auditor_sha256: str) -> tuple[dict[str, Any], bytes]:
    command = [
        sys.executable, "-I", "-B", str(SELF), "--core-projection",
        "--candidate", str(candidate), "--receipt", str(receipt),
        "--invocation-id", invocation,
        "--expect-auditor-sha256", expected_auditor_sha256,
    ]
    completed = subprocess.run(
        command, cwd=ROOT, check=False, stdout=subprocess.PIPE,
        stderr=subprocess.PIPE, timeout=1800,
    )
    need(completed.returncode == 0,
         "cold core failed:" + completed.stderr.decode("utf-8", "replace"))
    value = strict_json(completed.stdout, "cold core projection")
    self_closed(value, "projection_object_sha256", "cold core projection")
    return value, completed.stdout


def within(path: Path, root: Path) -> bool:
    try:
        path.relative_to(root)
        return True
    except ValueError:
        return False


def output_preflight(path: Path) -> Path:
    absolute = path.absolute()
    need(absolute.name == "independent_audit.json",
         "audit output basename")
    need(within(absolute, AUDIT_ROOT) and absolute.parent.parent == AUDIT_ROOT,
         "audit output direct child of audit root")
    need(absolute.parent.name == C43_AUDIT_TOKEN,
         "audit output exact frozen v2 token")
    need(re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_.-]*", absolute.parent.name)
         is not None, "audit output token syntax")
    for target, label in (
        (absolute.parent, "audit final directory"),
        (absolute, "audit final member"),
    ):
        try:
            value = os.lstat(target)
        except FileNotFoundError:
            continue
        if stat.S_ISLNK(value.st_mode):
            try:
                linked = os.readlink(target)
            except OSError as error:
                raise Reject(label + " lstat/readlink") from error
            raise Reject(label + " no-replace symlink:" + linked)
        raise Reject(label + " no-replace entry")
    return absolute


def fsync_directory(path: Path) -> None:
    descriptor = os.open(path, os.O_RDONLY | getattr(os, "O_DIRECTORY", 0))
    try:
        os.fsync(descriptor)
    finally:
        os.close(descriptor)


def entry_absent_at(directory_fd: int, name: str, label: str) -> None:
    try:
        current = os.stat(name, dir_fd=directory_fd, follow_symlinks=False)
    except FileNotFoundError:
        return
    if stat.S_ISLNK(current.st_mode):
        try:
            linked = os.readlink(name, dir_fd=directory_fd)
        except OSError as error:
            raise Reject(label + " lstat/readlink") from error
        raise Reject(label + " absent (symlink present):" + linked)
    raise Reject(label + " absent (entry present)")


def directory_identity_matches(path: Path, directory_fd: int,
                               identity: tuple[int, int], label: str) -> None:
    opened = os.fstat(directory_fd)
    named = os.stat(path, follow_symlinks=False)
    need(
        stat.S_ISDIR(opened.st_mode) and stat.S_ISDIR(named.st_mode)
        and (opened.st_dev, opened.st_ino) == identity
        == (named.st_dev, named.st_ino),
        label + " fd/path identity",
    )


def read_at(directory_fd: int, name: str, maximum: int,
            label: str) -> bytes:
    flags = os.O_RDONLY | getattr(os, "O_CLOEXEC", 0) \
        | getattr(os, "O_NOFOLLOW", 0)
    descriptor = os.open(name, flags, dir_fd=directory_fd)
    try:
        before = os.fstat(descriptor)
        need(stat.S_ISREG(before.st_mode) and before.st_nlink == 1
             and 0 < before.st_size <= maximum,
             "fd-at regular single-link bounded:" + label)
        chunks = []
        remaining = maximum + 1
        while remaining:
            block = os.read(descriptor, min(1 << 20, remaining))
            if not block:
                break
            chunks.append(block)
            remaining -= len(block)
        raw = b"".join(chunks)
        after = os.fstat(descriptor)
        fingerprint = lambda item: (
            item.st_dev, item.st_ino, item.st_mode, item.st_nlink,
            item.st_size, item.st_mtime_ns, item.st_ctime_ns,
        )
        need(fingerprint(before) == fingerprint(after)
             and len(raw) == before.st_size <= maximum,
             "fd-at stable read:" + label)
        return raw
    finally:
        os.close(descriptor)


def write_new_at(directory_fd: int, name: str, raw: bytes,
                 final_mode: int = 0o600) -> None:
    flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL \
        | getattr(os, "O_CLOEXEC", 0) | getattr(os, "O_NOFOLLOW", 0)
    descriptor = os.open(name, flags, 0o600, dir_fd=directory_fd)
    try:
        created = os.fstat(descriptor)
        need(stat.S_ISREG(created.st_mode) and created.st_nlink == 1,
             "fresh audit member inode")
        view = memoryview(raw)
        while view:
            written = os.write(descriptor, view)
            need(written > 0, "audit write progress")
            view = view[written:]
        os.fchmod(descriptor, final_mode)
        os.fsync(descriptor)
    finally:
        os.close(descriptor)


def rename_noreplace_at(old_directory_fd: int, old_name: str,
                        new_directory_fd: int, new_name: str) -> None:
    """Linux renameat2(RENAME_NOREPLACE), with no emulated fallback."""
    libc = ctypes.CDLL(None, use_errno=True)
    renameat2 = getattr(libc, "renameat2", None)
    need(renameat2 is not None, "renameat2 available")
    renameat2.argtypes = (
        ctypes.c_int, ctypes.c_char_p, ctypes.c_int, ctypes.c_char_p,
        ctypes.c_uint,
    )
    renameat2.restype = ctypes.c_int
    ctypes.set_errno(0)
    result = renameat2(
        old_directory_fd, old_name.encode("ascii"),
        new_directory_fd, new_name.encode("ascii"), 1,
    )
    if result == 0:
        return
    error = ctypes.get_errno()
    if error in (errno.EEXIST, errno.ENOTEMPTY):
        raise Reject("renameat2 RENAME_NOREPLACE final exists")
    raise OSError(error, os.strerror(error), new_name)


def publish_audit_directory(
    path: Path, value: dict[str, Any], terminal_revalidator: Callable[[], None],
) -> None:
    """Seal a private stage directory, then atomically publish the directory.

    There is deliberately no cleanup path.  Any failure after mkdirat leaves
    the unpredictable private stage directory (or committed final directory)
    as fail-closed forensic evidence; no stat-then-unlink race exists.
    """
    global AUDIT_COMMIT_OBSERVED
    raw = canonical(value) + b"\n"
    root_flags = os.O_RDONLY | getattr(os, "O_CLOEXEC", 0) \
        | getattr(os, "O_NOFOLLOW", 0) | getattr(os, "O_DIRECTORY", 0)
    root_fd = os.open(AUDIT_ROOT, root_flags)
    stage_fd: int | None = None
    try:
        root_stat = os.fstat(root_fd)
        root_identity = (root_stat.st_dev, root_stat.st_ino)
        directory_identity_matches(
            AUDIT_ROOT, root_fd, root_identity, "audit root"
        )
        final_name = path.parent.name
        entry_absent_at(root_fd, final_name, "audit final directory")

        stage_flags = os.O_RDONLY | getattr(os, "O_CLOEXEC", 0) \
            | getattr(os, "O_NOFOLLOW", 0) | getattr(os, "O_DIRECTORY", 0)
        stage_name = ""
        stage_identity: tuple[int, int] | None = None
        for _attempt in range(8):
            proposed = ".c43-audit-stage-" + secrets.token_hex(24)
            try:
                os.mkdir(proposed, mode=0o700, dir_fd=root_fd)
            except FileExistsError:
                continue
            stage_fd = os.open(proposed, stage_flags, dir_fd=root_fd)
            stage_stat = os.fstat(stage_fd)
            named_stage = os.stat(
                proposed, dir_fd=root_fd, follow_symlinks=False
            )
            stage_identity = (stage_stat.st_dev, stage_stat.st_ino)
            need(
                stat.S_ISDIR(stage_stat.st_mode)
                and stat.S_ISDIR(named_stage.st_mode)
                and (named_stage.st_dev, named_stage.st_ino)
                == stage_identity
                and (stage_stat.st_mode & 0o777) == 0o700
                and (named_stage.st_mode & 0o777) == 0o700,
                "private stage fd/name identity and mode",
            )
            os.fsync(root_fd)
            stage_name = proposed
            break
        need(
            bool(stage_name) and stage_fd is not None
            and stage_identity is not None,
            "unpredictable private stage allocation",
        )

        write_new_at(stage_fd, path.name, raw, 0o444)
        need(os.listdir(stage_fd) == [path.name],
             "private stage exact inventory")
        replay = read_at(stage_fd, path.name, 32 << 20, "staged C43 audit")
        need(replay == raw, "staged audit byte replay")
        parsed = strict_json(replay, "staged C43 audit")
        self_closed(parsed, "object_sha256", "staged C43 audit")
        staged_member = os.stat(
            path.name, dir_fd=stage_fd, follow_symlinks=False
        )
        need(stat.S_ISREG(staged_member.st_mode)
             and stat.S_IMODE(staged_member.st_mode) == 0o444
             and staged_member.st_nlink == 1
             and staged_member.st_uid == os.getuid(),
             "staged audit immutable singleton mode/owner")
        os.fchmod(stage_fd, 0o500)
        os.fsync(stage_fd)
        named_stage = os.stat(
            stage_name, dir_fd=root_fd, follow_symlinks=False
        )
        need(stat.S_ISDIR(named_stage.st_mode)
             and stat.S_IMODE(named_stage.st_mode) == 0o500
             and (named_stage.st_dev, named_stage.st_ino) == stage_identity,
             "sealed stage directory mode and identity")
        os.fsync(root_fd)

        directory_identity_matches(
            AUDIT_ROOT, root_fd, root_identity, "precommit audit root"
        )
        entry_absent_at(root_fd, final_name, "precommit audit final")
        # This is deliberately the final fallible semantic validation.  It
        # replays source, candidate, receipt, C41/C42 authority, and pointer
        # absence after every stage byte and fsync has completed.
        terminal_revalidator()
        directory_identity_matches(
            AUDIT_ROOT, root_fd, root_identity, "terminal precommit audit root"
        )
        entry_absent_at(root_fd, final_name, "terminal precommit audit final")
        no_c43_pointer()
        rename_noreplace_at(root_fd, stage_name, root_fd, final_name)
        AUDIT_COMMIT_OBSERVED = True
        # renameat2 is the semantic commit.  Parent fsync is the only fallible
        # operation after it; failure is reported as committed/replay-required,
        # never as audit_published=false.  All byte and identity checks above
        # were made through the still-open stage descriptors.
        try:
            os.fsync(root_fd)
        except OSError as error:
            raise AuditCommittedError(
                "audit directory renamed; audit-root fsync failed; "
                "classify committed name by stable replay: " + str(error)
            ) from error
    finally:
        if stage_fd is not None:
            try:
                os.close(stage_fd)
            except OSError:
                if not AUDIT_COMMIT_OBSERVED:
                    raise
        try:
            os.close(root_fd)
        except OSError:
            if not AUDIT_COMMIT_OBSERVED:
                raise


def run_audit(candidate: Path, receipt: Path, invocation: str,
              output: Path, expected_auditor_sha256: str) -> dict[str, Any]:
    no_c43_pointer()
    output = output_preflight(output)
    parent_source_raw = stable_read(SELF, 16 << 20, "C43 v2 parent source")
    need(HEX64.fullmatch(expected_auditor_sha256) is not None
         and bytes_sha(parent_source_raw) == expected_auditor_sha256,
         "externally frozen parent C43 v2 auditor source")
    first, first_raw = cold_core(
        candidate, receipt, invocation, expected_auditor_sha256
    )
    second, second_raw = cold_core(
        candidate, receipt, invocation, expected_auditor_sha256
    )
    need(first == second and first_raw == second_raw,
         "two byte-identical fresh C43 cores")
    attacks = dict(first["hostile_mutations"])
    need(len(attacks) == 88 and all(attacks.values()),
         "88 complete transaction attacks fail closed")
    controls = {
        "cold_core_byte_identity": True,
        "candidate_terminal_byte_replay": True,
        "atomic_directory_rename_noreplace_seal": True,
        "stage_replay_before_commit": True,
        "terminal_inputs_reattested_after_stage_fsync": True,
        "published_file_mode_0444": True,
        "published_directory_mode_0500": True,
        "post_rename_failure_reports_committed": True,
    }
    # All mutable inputs are replayed before the private stage is allocated.
    terminal_candidate = capture_candidate(candidate)
    terminal_receipt = capture_receipt(
        receipt, terminal_candidate, invocation
    )
    validate_source_pins()
    no_c43_pointer()
    audit = {
            "schema": SCHEMA,
            "status": (
                "PASS_INDEPENDENT_C43_V2_OWNER_ELIGIBLE_SUBSET_AUDIT__"
                f"{len(attacks)}_OF_{len(attacks)}_ATTACKS_FAIL_CLOSED"
            ),
            "candidate_path": first["candidate_path"],
            "audit_token": C43_AUDIT_TOKEN,
            "audit_path": str(output.relative_to(ROOT)),
            "candidate_object_sha256": EXPECTED_CANDIDATE_OBJECT,
            "producer_source_sha256": EXPECTED_PRODUCER_SOURCE,
            "root_manifest_sha256": EXPECTED_MANIFEST_FILE,
            "execution_receipt_object_sha256": EXPECTED_RECEIPT_OBJECT,
            "InvocationID": invocation,
            "installed_C42_candidate_object_sha256": EXPECTED_C42_OBJECT,
            "installed_C42_independent_audit_object_sha256":
                EXPECTED_C42_AUDIT_OBJECT,
            "installed_C42_authority_seal_object_sha256":
                EXPECTED_C42_SEAL_OBJECT,
            "independent_auditor_source_sha256": bytes_sha(parent_source_raw),
            "independence_boundary": {
                "C43_producer_imported_or_executed": False,
                "C43_v1_auditor_imported_or_executed": False,
                "C43B0_pilot_imported_or_executed": False,
                "C43B0_planner_imported_or_executed": False,
                "C42_transaction_auditor_imported_or_executed": False,
                "frozen_C41_router_and_lower_primitives_used": True,
                "candidate_rows_used_as_expected_baseline": False,
            },
        "method": (
                "no import or execution of C43 producer, v1 auditor, pilot, "
                "or planner; raw C41 zero-surface/ambient two-pass target "
                "derivation; inert-byte C42 receipt/seal reconstruction; "
                "adaptive traversal from frozen mathematical primitives; "
                "91,879-row representative/reflected rational incidence; "
                "52 direct closed leaf/face/corner/internal restrictions; "
                "exact reflection, Kraft, 862-parent and 76,832-census replay; "
            "reclosed coherent complete-transaction mutations; two fresh "
            "byte-identical cores; immutable private-stage replay, terminal "
            "input reattestation, and final renameat2 RENAME_NOREPLACE commit"
        ),
            "cold_core_projection_sha256": bytes_sha(first_raw),
            "cold_core_projection_byte_count": len(first_raw),
            "derived_sole_deficit_pairs": list(TARGET_PAIRS),
            "owner_eligible_pairs": first["eligible_pairs"],
            "canonical_residual_owner_blocked_pairs":
                first["blocked_zero_credit_pairs"],
            "blocked_pairs_receive_credit": False,
            "reconstructed": {
                "whole_paired_coarse_cells": 578,
                "whole_representatives": 289,
                "remaining_representatives": 573,
                "EARLIEST_PREFIX_EXCLUDED": 75_390,
                "TYPED_EVENT_GRAPH": 296,
                "UNRESOLVED_R1648_CONTINUATION": 1_146,
                "unresolved_zero": False,
                "direct_closed_restriction_count": 52,
                "parent_row_count": 862,
            },
            "attacks": attacks,
            "validation_controls": controls,
            "publication_contract": {
                "private_stage_file_mode": "0444",
                "private_stage_directory_mode": "0500",
                "all_replay_and_input_reattest_before_rename": True,
                "semantic_commit": "renameat2_RENAME_NOREPLACE",
                "post_commit_failure_never_reports_unpublished": True,
            },
            "strict_nonpromotion": first["strict_nonpromotion"],
            "audit_output_is_authority": False,
            "producer_output_is_authority": False,
            "authority_pointer_installed": False,
    }
    audit["object_sha256"] = digest(audit)

    def terminal_revalidator() -> None:
        replay_candidate = capture_candidate(candidate)
        replay_receipt = capture_receipt(
            receipt, replay_candidate, invocation
        )
        need(replay_candidate["raw"] == terminal_candidate["raw"]
             and replay_receipt == terminal_receipt,
             "post-stage candidate/receipt terminal identity")
        need(validate_installed_c41_authority()
             == first["installed_C41_authority"],
             "post-stage C41 authority terminal identity")
        terminal_c42 = validate_installed_c42_authority()
        need(terminal_c42["candidate_object_sha256"] == EXPECTED_C42_OBJECT
             and terminal_c42["independent_audit_object_sha256"]
             == EXPECTED_C42_AUDIT_OBJECT
             and terminal_c42["authority_seal_object_sha256"]
             == EXPECTED_C42_SEAL_OBJECT
             and terminal_c42["installation_receipt_object_sha256"]
             == EXPECTED_C42_RECEIPT_OBJECT,
             "post-stage C42 authority terminal identity")
        validate_source_pins()
        need(stable_read(SELF, 16 << 20, "post-stage C43 v2 source")
             == parent_source_raw, "post-stage auditor source terminal identity")
        no_c43_pointer()

    publish_audit_directory(output, audit, terminal_revalidator)
    return audit


def hostile_fixture_self_test() -> dict[str, bool]:
    """Exercise a coherent cross-linked mini result/receipt mutation."""
    result = {
        "schema": SCHEMA + ".hostile-fixture.result",
        "producer_output_is_authority": False,
        "authority_pointer_installed": False,
        "owner_eligible_pairs": list(ELIGIBLE),
    }
    result["object_sha256"] = digest(result)
    receipt = {
        "schema": SCHEMA + ".hostile-fixture.receipt",
        "candidate_object_sha256": result["object_sha256"],
        "producer_output_is_authority": False,
        "authority_pointer_installed": False,
        "owner_eligible_pairs": list(ELIGIBLE),
    }
    receipt["receipt_object_sha256"] = digest(receipt)

    def validate(one: dict[str, Any], two: dict[str, Any]) -> None:
        self_closed(one, "object_sha256", "hostile fixture result")
        self_closed(two, "receipt_object_sha256", "hostile fixture receipt")
        need(
            one["schema"] == SCHEMA + ".hostile-fixture.result"
            and two["schema"] == SCHEMA + ".hostile-fixture.receipt"
            and one["producer_output_is_authority"] is False
            and one["authority_pointer_installed"] is False
            and one["owner_eligible_pairs"] == list(ELIGIBLE)
            and two["candidate_object_sha256"] == one["object_sha256"]
            and two["producer_output_is_authority"]
            == one["producer_output_is_authority"]
            and two["authority_pointer_installed"]
            == one["authority_pointer_installed"]
            and two["owner_eligible_pairs"] == one["owner_eligible_pairs"],
            "hostile fixture exact nonauthority semantics",
        )

    validate(result, receipt)

    def coherent_attack(field: str, replacement: Any) -> None:
        one = copy.deepcopy(result)
        one[field] = replacement
        one.pop("object_sha256")
        one["object_sha256"] = digest(one)
        two = copy.deepcopy(receipt)
        two["candidate_object_sha256"] = one["object_sha256"]
        if field in two:
            two[field] = replacement
        two.pop("receipt_object_sha256")
        two["receipt_object_sha256"] = digest(two)
        validate(one, two)

    attacks = {
        "coherent_authority_escalation": rejected(
            "self-test coherent authority escalation",
            lambda: coherent_attack("producer_output_is_authority", True),
        ),
        "coherent_eligibility_expansion": rejected(
            "self-test coherent eligibility expansion",
            lambda: coherent_attack("owner_eligible_pairs", [97, 592, 715]),
        ),
    }
    need(all(attacks.values()), "hostile fixture attacks fail closed")
    return attacks


def self_test() -> dict[str, Any]:
    no_producer_import()
    no_c43_pointer()
    validate_source_pins()
    need(TARGET_PAIRS == (97, 211, 592, 664, 715)
         and ELIGIBLE == (592, 715) and BLOCKED == (97, 211, 664),
         "exact C43 eligibility constants")
    need(expected_census()["UNRESOLVED_R1648_CONTINUATION"] == 1_146,
         "exact C43 census fixture")
    fixture_attacks = hostile_fixture_self_test()
    return {
        "schema": SCHEMA + ".self-test",
        "status": "PASS_C43_V2_INDEPENDENT_AUDITOR_FORMAL_PIN_SELF_TEST",
        "formal_pins_ready": True,
        "no_forbidden_C43_implementation_import": True,
        "audit_token": C43_AUDIT_TOKEN,
        "eligible_pairs": list(ELIGIBLE),
        "blocked_zero_credit_pairs": list(BLOCKED),
        "expected_whole_paired": 578,
        "expected_whole_representatives": 289,
        "expected_unresolved": 1_146,
        "hostile_fixture_attacks": fixture_attacks,
        "auditor_installs_pointer": False,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--candidate", type=Path)
    parser.add_argument("--receipt", type=Path)
    parser.add_argument("--invocation-id")
    parser.add_argument("--expect-auditor-sha256")
    parser.add_argument("--output", type=Path)
    parser.add_argument("--core-projection", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    arguments = parser.parse_args()
    try:
        if arguments.self_test:
            need(arguments.candidate is None and arguments.receipt is None
                 and arguments.output is None and arguments.invocation_id is None
                 and arguments.expect_auditor_sha256 is None,
                 "self-test takes no other arguments")
            value = self_test()
        else:
            need(arguments.candidate is not None and arguments.receipt is not None
                 and arguments.invocation_id is not None
                 and arguments.expect_auditor_sha256 is not None,
                 "candidate/receipt/invocation/frozen auditor SHA required")
            if arguments.core_projection:
                need(arguments.output is None, "core projection has no output")
                value = audit_core(
                    arguments.candidate, arguments.receipt,
                    arguments.invocation_id, arguments.expect_auditor_sha256,
                )
            else:
                need(arguments.output is not None, "formal audit output required")
                value = run_audit(
                    arguments.candidate, arguments.receipt,
                    arguments.invocation_id, arguments.output,
                    arguments.expect_auditor_sha256,
                )
        sys.stdout.buffer.write(canonical(value) + b"\n")
        return 0
    except Exception as error:
        committed = AUDIT_COMMIT_OBSERVED or isinstance(
            error, AuditCommittedError
        )
        failure = {
            "schema": SCHEMA + ".failure",
            "status": (
                "AUDIT_COMMITTED__TERMINAL_REPORT_OR_DURABILITY_REPLAY_REQUIRED"
                if committed else "FAIL_CLOSED_INDEPENDENT_C43_V2_AUDIT"
            ),
            "error_type": type(error).__name__,
            "error_message": str(error),
            "audit_published": committed,
            "authority_pointer_installed": False,
        }
        sys.stderr.buffer.write(canonical(failure) + b"\n")
        return 3 if committed else 2


if __name__ == "__main__":
    raise SystemExit(main())
