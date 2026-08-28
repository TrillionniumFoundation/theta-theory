#!/usr/bin/env python3
"""C42 provisional singleton closure for the P391 C41 wall outer.

The C41 P391 leaf 111101111 is a closed-box interval dependency failure,
not a physical wall contact.  One exact p-midpoint split gives two closed
representative boxes on which the complete Round185 router certifies the
same strict collision-two owner mismatch.  The horizontally reflected pair
is recomputed independently.  Four full closed faces and four exact corners
are also recomputed, then joined to the complete C41 incident-cell census.

The independent C41 audit is pinned and required in every mode.  Formal mode
is only a producer pass pending a separate independent C42 audit: this source
never mints authority and never installs an authority pointer.
"""

from __future__ import annotations

import argparse
import ctypes
import copy
import errno
import hashlib
import json
import os
import re
import shutil
import stat
import sys
from contextlib import ExitStack
from fractions import Fraction as Q
from pathlib import Path
from typing import Any, Iterable

import flint
from flint import arb, ctx

import cm2_gate3_eight_cell_symmetry_atlas_cert as atlas
import cm2_gate3_ge_interval_atlas_cert as ge
import cm2_gate34_round28_nonempty_adaptive_component_registry_cert as registry
import cm2_round178_later_return_exact_key_bridge as round178
import cm2_round181_parametric_collision2_graph_arrangement as round181
import cm2_round185_preconditioned_c1_residual_refinement as round185
import cm2_round306c40_d02_h1_endpoint_collision2_arrangement_v1 as c40
import cm2_round306c41_d02_lower_strata_depth3_closure_v1 as c41


if hasattr(sys, "set_int_max_str_digits"):
    sys.set_int_max_str_digits(0)
sys.dont_write_bytecode = True

ROOT = Path(__file__).resolve().parent.parent
DELIVERABLES = ROOT / "deliverables"
RUNTIME = ROOT / ".cm2-runtime"

SCHEMA = "cm2.round306c42.d02-singleton-wall-endpoint-owner-closure.v1"
SOURCE_SCHEMA = SCHEMA + ".exact-source"
INTERIOR_SCHEMA = SCHEMA + ".closed-interior-certificate"
FACE_SCHEMA = SCHEMA + ".face-owner-incidence"
CORNER_SCHEMA = SCHEMA + ".corner-owner-incidence"
REFLECTION_SCHEMA = SCHEMA + ".reflection-transport"
PARENT_SCHEMA = SCHEMA + ".parent-conservation"
RECEIPT_SCHEMA = SCHEMA + ".execution-receipt"

INVENTORY = tuple(sorted([
    "C42_SINGLETON_CLOSURE.lock",
    "corner_owner_incidence.jsonl.gz",
    "exact_source.jsonl.gz",
    "face_owner_incidence.jsonl.gz",
    "interior_certificates.jsonl.gz",
    "parent_conservation.jsonl.gz",
    "reflection_transport.jsonl.gz",
    "result.json",
    "root_manifest.sha256",
]))

PRECISION_BITS = 384
PAIR_INDEX = 391
TARGET_PATH = "111101111"
TARGET_FRACTION = Q(1, 512)
MID_P = Q(1119, 2048)

EXPECTED_C41_SOURCE = (
    "3fbf6cec247903d6e6ba147d4d06e912638b1472b74adc8311323c554e6e5bde"
)
EXPECTED_ROUND185_SOURCE = (
    "7b48f3ee3417fcfdf5ef6c852e0ab591eb849b357e704e46ee3aaa259d20acc2"
)
EXPECTED_C40_SOURCE = (
    "9ec1ad4df72b0f25b646d17a43e1186188ace97d2e76ac480c1c2a476fac5f57"
)
EXPECTED_C41_OBJECT = (
    "b7e47a4ca9d6f4bb1fee10e78877850d5070f6d3c2b06bb0234fbabdaa2b7b24"
)
EXPECTED_C41_RECEIPT_OBJECT = (
    "39f1c6dadcf21a428174520b5a1aa4d072a57c73ffd9c9b04d2c3d639d94fed9"
)
EXPECTED_C41_ROOT_MANIFEST = (
    "86e10532d63269cd0fdd58d541b1984522e9718f4613a5dc83211fe84eb258ba"
)
EXPECTED_C41_AUDITOR_SOURCE = (
    "537f3dea94c3743235df8984ba4922d37f82999ff3d8abbac59e5171ef38b74c"
)
EXPECTED_C41_AUDIT_FILE_SHA256 = (
    "6a800959a90c227d587b82c6246f60123483471f61dcf6a5de4da5381fee4b1e"
)
EXPECTED_C41_AUDIT_PATH = (
    ".cm2-runtime/audit/"
    "c41-independent-audit-20260811T031547Z-ab94d420c43c94cd/"
    "independent_audit.json"
)
EXPECTED_C41_CANDIDATE_TOKEN = (
    "c41-lower-strata-depth3-20260811T023804Z-f997365c91559599"
)
EXPECTED_C41_CANDIDATE_PATH = (
    ".cm2-runtime/candidates/" + EXPECTED_C41_CANDIDATE_TOKEN
)
EXPECTED_C41_RECEIPT_PATH = (
    ".cm2-runtime/audit/" + EXPECTED_C41_CANDIDATE_TOKEN
    + "/execution_receipt.json"
)
EXPECTED_C41_AUDIT_TOKEN = (
    "c41-independent-audit-20260811T031547Z-ab94d420c43c94cd"
)
EXPECTED_C41_CURRENT_TOKEN_SHA256 = (
    "9e4f2d9c02c1f3e56639d69c971ccc7846ba229f87723e878f101730df3dd1a9"
)
EXPECTED_C41_CURRENT_AUDIT_TOKEN_SHA256 = (
    "f8a9a0bf69169eba05ef3bec1db7e924de4b06b4ab61c97693b2919effd9c86c"
)
EXPECTED_C41_STATUS = (
    "PASS_C41_DEPTH3_STRICT_ROUTER_PARTIAL__91879_AMBIENT_LEAVES__"
    "572_WHOLE_CELLS_TERMINAL__1152_FORMAL_UNRESOLVED"
)

EXPECTED_C41_AUDIT_OBJECT = (
    "44061ec6e26108692fe6e635e9e666cca0b11c66f00384eab539be08f66fe877"
)
EXPECTED_C41_AUDIT_STATUS = (
    "PASS_INDEPENDENT_C41_DEPTH3_CLOSURE_AUDIT__"
    "37_OF_37_MUTATIONS_REJECTED"
)

CANDIDATE_ROOT = (RUNTIME / "candidates").resolve()
AUDIT_ROOT = (RUNTIME / "audit").resolve()

TARGET_AMBIENT_ID = (
    "c41-ambient:01bcc14671eacb7628822945582e307e70cf9fbeeff7f3f47adc6e9597f3ab38"
)
TARGET_AMBIENT_ROW = (
    "49b986a5ba33c0fba075e854feb5316348815199e56e2b93e1ab224898c6c0e8"
)
TARGET_C40_LEAF_ID = (
    "c40-leaf:cea9d97f7e317690cd115fda8becf276f56e9f101ef479b16a2ad3b6cabb6add"
)
TARGET_C40_ROW = (
    "47688bd2d8bd7f065f9336c1ab9a1c7d68a6d5a8e71a5fe897a3310a885242a8"
)
TARGET_C38_ROW = (
    "d53afd4ff2cdba6bf5bb738078d49774d71184ca92fb6cbf2a5b44b97ec32383"
)
TARGET_C2_OUTER_ID = (
    "c41-c2-outer:6711f208eef9b4a3e63d73649ffed9e296c0de107c5f92185489d287908fbad3"
)
TARGET_C2_OUTER_ROW = (
    "3e336912ccc519e429c98449138fcfd4b197c631a67029fe6271d88d1123f469"
)
TARGET_BOUNDARY_ID = (
    "c41-boundary-corner:2a70f5dd12d5108578d02d237253a8423402c12ff6c71ab57514ba1feb146afd"
)
TARGET_BOUNDARY_ROW = (
    "9099ec4b3a04cba4357b313c269759a3a33cd5f65484e78f1d337c47afe559e4"
)
TARGET_PARENT_ROW = (
    "8a95ca622e00f69085cd315333d8999c22aed92d98c8c3bd61799b1f33a5a727"
)

REPRESENTATIVE_CELL_ID = (
    "c32-compact-cell:42e1769797f57b5b64e4586c8fea91c494e1b46e38e70ebc8afc67ec39fbedd6"
)
REFLECTED_CELL_ID = (
    "c32-compact-cell:94182bdd4e235fc42c9f64d9bf7485f4f3b9e6078684c2d0109bb7d0d13891ad"
)
REPRESENTATIVE_PARENT_KEY = "W:E:01.12.000110"
REFLECTED_PARENT_KEY = "W:E:06.03.111001"

REPRESENTATIVE_BOX = {
    "t": ["-125493/256000", "-31329/64000"],
    "p": ["559/1024", "35/64"],
    "s": ["0", "0"],
}
REFLECTED_BOX = {
    "compact_chart": "E",
    "t": ["31329/64000", "125493/256000"],
    "p": ["-35/64", "-559/1024"],
    "s": ["0", "0"],
}

FACE_NEIGHBORS = {
    "t_lower": (
        "c41-ambient:67e4f34f3e9e303b5daf09f68eb8d5bc4529bfaadd732d69fdd0cf47797bbe75",
        "add29e42b099fbd33f33378573b2c7c7ec16e24275338ae98b9b085b20646091",
        "111101110",
    ),
    "t_upper": (
        "c41-ambient:46c46990ada80fb1a023ab155fb2d103a592eec5f4508a1f9961c9ff5eef6fae",
        "792a7c30d97f80ef1e228e1cf4e766002c0c19d88390cce01ebb28f92f3d533b",
        "11111101",
    ),
    "p_lower": (
        "c41-ambient:64b466124663c44cd7bdb0eeb571d90a30ba78ea5b48bd018ae2dc1a3d3e047b",
        "35e6d7b2c6de5ad11b346767f055f93349bb6384f8ef721541099bc3fcde6372",
        "11110110",
    ),
    "p_upper": (
        "c41-ambient:31aea73dfa35a0e5d8f7e1f2fd0959ca53bce28c6209b8fd6c2e3ee22117bdbf",
        "1f933370504c6103aa89d34b1bbd46e83d644e22180291366a6b9cc5152b4ef6",
        "100010",
    ),
}

CORNER_INCIDENT_IDS = {
    "t0p0": {
        "c41-ambient:64b466124663c44cd7bdb0eeb571d90a30ba78ea5b48bd018ae2dc1a3d3e047b",
        "c41-ambient:67e4f34f3e9e303b5daf09f68eb8d5bc4529bfaadd732d69fdd0cf47797bbe75",
        TARGET_AMBIENT_ID,
    },
    "t0p1": {
        "c41-ambient:31aea73dfa35a0e5d8f7e1f2fd0959ca53bce28c6209b8fd6c2e3ee22117bdbf",
        "c41-ambient:67e4f34f3e9e303b5daf09f68eb8d5bc4529bfaadd732d69fdd0cf47797bbe75",
        TARGET_AMBIENT_ID,
    },
    "t1p0": {
        "c41-ambient:64b466124663c44cd7bdb0eeb571d90a30ba78ea5b48bd018ae2dc1a3d3e047b",
        TARGET_AMBIENT_ID,
        "c41-ambient:1143eb0d79e64dcd23d42c5da8df2c530469fbde0e29357f1501cdc377fab892",
        "c41-ambient:46c46990ada80fb1a023ab155fb2d103a592eec5f4508a1f9961c9ff5eef6fae",
    },
    "t1p1": {
        "c41-ambient:31aea73dfa35a0e5d8f7e1f2fd0959ca53bce28c6209b8fd6c2e3ee22117bdbf",
        "c41-ambient:f79c769054cd4a130e9c13dfb6cdf7d1c4b90b5772c43f083ce98b766e3ad3d8",
        TARGET_AMBIENT_ID,
        "c41-ambient:46c46990ada80fb1a023ab155fb2d103a592eec5f4508a1f9961c9ff5eef6fae",
    },
}

EXPECTED_FACE_IDS = {
    "t_lower": "c41-boundary-face:b89577eeee342230d16ea77549854a32122bc8a9fa25c6397ef0e086aba2abe1",
    "t_upper": "c41-boundary-face:912c37a767ade41c388341619c2e1e0b5b8e38cf5ed802961381ee7bec8bdb48",
    "p_lower": "c41-boundary-face:2e0bad42004d221562652331667b509a47e4867e55effecd1dfce5c31c5ec8ae",
    "p_upper": "c41-boundary-face:d6e8c78598860b62a121f349bff5f81f1525ed95f942fe8c6c8fdd28cb55e370",
}
EXPECTED_CORNER_IDS = {
    "t0p0": "c41-boundary-corner-point:e1d1b793d03995b28e9ac30985f2aca290e7bf898f7a11a1f42ed9fb77c7849e",
    "t0p1": "c41-boundary-corner-point:4fa9c13a859a6e0eed0f704a70d543b0d6bae1d8ca6fed8deb3877c2752e81b1",
    "t1p0": "c41-boundary-corner-point:8c2a2d5f4a1b3252d7163e773839e6a337fc340d7f6098e1df1a31acef67051f",
    "t1p1": "c41-boundary-corner-point:24b115aee698bddb92ee9fb3927a29476b222c05f5483873b6de3c3737e44786",
}

EXPECTED_REP_OWNER = "G[1,0]"
EXPECTED_REF_OWNER = "G[1,1]"
EXPECTED_REP_OUTGOING = "N"
EXPECTED_REF_OUTGOING = "S"
EXPECTED_REP_WORD_ROW = ["W:W", "G[0,0]", [], 1]
EXPECTED_REF_WORD_ROW = ["W:W", "G[0,1]", [], 1]
EXPECTED_REP_LIVE_OWNER = "G[0,1]"
EXPECTED_REF_LIVE_OWNER = "G[0,0]"

HEX64 = re.compile(r"[0-9a-f]{64}\Z")
TOKEN = re.compile(r"[A-Za-z0-9][A-Za-z0-9_.:-]{15,127}\Z")


class C42Error(RuntimeError):
    pass


def require(condition: bool, label: str) -> None:
    if not condition:
        raise C42Error(label)


def canonical(value: Any) -> bytes:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    ).encode("utf-8")


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def file_sha256(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def qstr(value: Q) -> str:
    return str(value.numerator) if value.denominator == 1 else str(value)


def box_payload(box: Any, *, reflected: bool = False) -> dict[str, Any]:
    result = {
        "t": [qstr(box.t0), qstr(box.t1)],
        "p": [qstr(box.p0), qstr(box.p1)],
        "s": [qstr(box.s0), qstr(box.s1)],
    }
    if reflected:
        result["compact_chart"] = "E"
    return result


def box_from_payload(value: dict[str, Any], path: str) -> Any:
    return atlas.AtlasBox(
        Q(value["t"][0]), Q(value["t"][1]),
        Q(value["p"][0]), Q(value["p"][1]),
        Q(value["s"][0]), Q(value["s"][1]),
        len(TARGET_PATH), path,
    )


def arb_bounds(value: arb) -> dict[str, Any]:
    return {
        "lower": str(value.lower()),
        "upper": str(value.upper()),
        "contains_zero": bool(value.contains(0)),
    }


def write_json(path: Path, value: dict[str, Any]) -> None:
    path.write_bytes(canonical(value) + b"\n")


def strict_json(path: Path) -> dict[str, Any]:
    raw = path.read_bytes()
    require(raw == raw.strip() + b"\n", f"canonical newline:{path}")

    def pairs(items: list[tuple[str, Any]]) -> dict[str, Any]:
        require(len(items) == len({key for key, _value in items}),
                f"duplicate JSON key:{path}")
        return dict(items)

    value = json.loads(
        raw,
        object_pairs_hook=pairs,
        parse_float=lambda _value: (_ for _ in ()).throw(
            C42Error(f"float forbidden:{path}")
        ),
        parse_constant=lambda _value: (_ for _ in ()).throw(
            C42Error(f"constant forbidden:{path}")
        ),
    )
    require(type(value) is dict and canonical(value) + b"\n" == raw,
            f"canonical JSON:{path}")
    return value


def validate_self_object(value: dict[str, Any], field: str, label: str) -> None:
    observed = value.get(field)
    semantic = dict(value)
    semantic.pop(field, None)
    require(
        isinstance(observed, str)
        and HEX64.fullmatch(observed) is not None
        and observed == digest(semantic),
        f"self object:{label}",
    )


def require_regular_single_link(path: Path, label: str) -> None:
    value = path.lstat()
    require(
        stat.S_ISREG(value.st_mode)
        and not path.is_symlink()
        and value.st_nlink == 1,
        f"regular single-link:{label}:{path}",
    )


def within(path: Path, ancestor: Path) -> bool:
    try:
        path.relative_to(ancestor)
        return True
    except ValueError:
        return False


def workspace_path(path: Path, label: str, *, must_exist: bool) -> Path:
    require(
        ".." not in path.parts and "." not in path.parts,
        f"dot-segment path alias forbidden:{label}",
    )
    absolute = path if path.is_absolute() else ROOT / path
    lexical = Path(os.path.abspath(absolute))
    resolved = lexical.resolve(strict=must_exist)
    require(
        lexical == resolved,
        f"canonical path without symlink alias:{label}",
    )
    require(within(resolved, ROOT), f"workspace path:{label}")
    if must_exist:
        require(resolved.exists(), f"exists:{label}")
    return resolved


def validate_current_c41_pointers() -> dict[str, str]:
    current = RUNTIME / "c41-current-token"
    current_audit = RUNTIME / "c41-current-audit-token"
    require_regular_single_link(current, "C41 current token")
    require_regular_single_link(current_audit, "C41 current audit token")
    require(
        current.read_bytes()
        == (EXPECTED_C41_CANDIDATE_TOKEN + "\n").encode("ascii")
        and file_sha256(current) == EXPECTED_C41_CURRENT_TOKEN_SHA256
        and current_audit.read_bytes()
        == (EXPECTED_C41_AUDIT_TOKEN + "\n").encode("ascii")
        and file_sha256(current_audit)
        == EXPECTED_C41_CURRENT_AUDIT_TOKEN_SHA256,
        "installed C41 candidate/audit pointers",
    )
    return {
        "candidate_pointer_sha256": EXPECTED_C41_CURRENT_TOKEN_SHA256,
        "audit_pointer_sha256": EXPECTED_C41_CURRENT_AUDIT_TOKEN_SHA256,
    }


def related(left: Path, right: Path) -> bool:
    return left == right or within(left, right) or within(right, left)


def require_unrelated(left: Path, right: Path, label: str) -> None:
    require(not related(left, right), f"path relation forbidden:{label}")


def require_direct_child(path: Path, root: Path, label: str) -> None:
    require(
        path.parent == root
        and path != root
        and path.name not in {"", ".", ".."}
        and TOKEN.fullmatch(path.name) is not None,
        f"direct child:{label}",
    )


def initial_target_preflight(
    candidate: Path,
    c41_receipt: Path,
    c41_audit: Path,
    output: Path,
    receipt_output: Path,
) -> tuple[Path, Path]:
    require_direct_child(output, CANDIDATE_ROOT, "C42 output")
    stage = output.with_name(output.name + f".stage-{os.getpid()}")
    require_direct_child(stage, CANDIDATE_ROOT, "C42 stage")
    receipt_parent = receipt_output.parent
    require_direct_child(receipt_parent, AUDIT_ROOT, "C42 receipt token")
    require(
        receipt_output.name == "execution_receipt.json"
        and receipt_output.parent == receipt_parent,
        "C42 canonical receipt filename",
    )
    require(
        receipt_parent.name == output.name,
        "C42 output and receipt share one transaction token",
    )
    receipt_stage = receipt_output.with_name(
        receipt_output.name + f".stage-{os.getpid()}"
    )
    require(
        not output.exists()
        and not stage.exists()
        and not receipt_parent.exists()
        and not receipt_output.exists()
        and not receipt_stage.exists(),
        "fresh C42 output/stage/receipt token targets",
    )
    for left_label, left in (
        ("output", output),
        ("stage", stage),
        ("receipt token", receipt_parent),
        ("receipt", receipt_output),
        ("receipt stage", receipt_stage),
    ):
        for right_label, right in (
            ("C41 candidate", candidate),
            ("C41 receipt", c41_receipt),
            ("C41 receipt parent", c41_receipt.parent),
            ("C41 audit", c41_audit),
            ("C41 audit parent", c41_audit.parent),
            ("deliverables", DELIVERABLES.resolve()),
            ("producer source", Path(__file__).resolve()),
        ):
            require_unrelated(
                left, right, f"{left_label} vs {right_label}"
            )
    for left_label, left, right_label, right in (
        ("output", output, "stage", stage),
        ("output", output, "receipt token", receipt_parent),
        ("output", output, "receipt", receipt_output),
        ("output", output, "receipt stage", receipt_stage),
        ("stage", stage, "receipt token", receipt_parent),
        ("stage", stage, "receipt", receipt_output),
        ("stage", stage, "receipt stage", receipt_stage),
    ):
        require_unrelated(left, right, f"{left_label} vs {right_label}")
    return stage, receipt_stage


def authority_target_preflight(
    output: Path,
    stage: Path,
    receipt_output: Path,
    context: dict[str, Any],
) -> None:
    c40_candidate = context["c40_candidate"].resolve()
    c40_audit = (
        ROOT
        / context["result"]["C40_authority"]["independent_audit_path"]
    ).resolve()
    targets = (
        ("output", output),
        ("stage", stage),
        ("receipt token", receipt_output.parent),
        ("receipt", receipt_output),
    )
    forbidden = (
        ("C40 candidate", c40_candidate),
        ("C40 audit", c40_audit),
        ("C40 audit parent", c40_audit.parent),
    )
    for left_label, left in targets:
        for right_label, right in forbidden:
            require_unrelated(
                left, right, f"{left_label} vs {right_label}"
            )


def fsync_directory(path: Path) -> None:
    descriptor = os.open(path, os.O_RDONLY | os.O_DIRECTORY)
    try:
        os.fsync(descriptor)
    finally:
        os.close(descriptor)


def write_exclusive_fsynced(path: Path, payload: bytes) -> None:
    descriptor = os.open(
        path,
        os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW | os.O_CLOEXEC,
        0o600,
    )
    try:
        offset = 0
        while offset < len(payload):
            written = os.write(descriptor, payload[offset:])
            require(written > 0, "receipt short write made progress")
            offset += written
        os.fsync(descriptor)
    finally:
        os.close(descriptor)


def rename_noreplace(source: Path, target: Path) -> None:
    libc = ctypes.CDLL(None, use_errno=True)
    function = getattr(libc, "renameat2", None)
    require(function is not None, "renameat2 RENAME_NOREPLACE available")
    function.argtypes = [
        ctypes.c_int,
        ctypes.c_char_p,
        ctypes.c_int,
        ctypes.c_char_p,
        ctypes.c_uint,
    ]
    function.restype = ctypes.c_int
    at_fdcwd = -100
    rename_noreplace_flag = 1
    result = function(
        at_fdcwd,
        os.fsencode(source),
        at_fdcwd,
        os.fsencode(target),
        rename_noreplace_flag,
    )
    if result != 0:
        number = ctypes.get_errno()
        raise OSError(number, os.strerror(number), str(target))


def rollback_publication(
    output: Path,
    receipt_output: Path,
    receipt_stage: Path,
    *,
    output_created: bool,
    receipt_parent_created: bool,
    receipt_stage_created: bool,
    receipt_final_created: bool,
) -> None:
    receipt_parent = receipt_output.parent
    failures: list[str] = []
    if receipt_parent_created and receipt_parent.exists():
        try:
            if receipt_final_created and receipt_output.exists():
                receipt_output.unlink()
            if receipt_stage_created and receipt_stage.exists():
                receipt_stage.unlink()
            receipt_parent.rmdir()
        except OSError as error:
            failures.append(
                "receipt rollback:" + type(error).__name__ + ":" + str(error)
            )
        finally:
            fsync_directory(AUDIT_ROOT)
    if output_created and output.exists():
        try:
            require_direct_child(output, CANDIDATE_ROOT, "rollback output")
            shutil.rmtree(output)
        except OSError as error:
            failures.append(
                "output rollback:" + type(error).__name__ + ":" + str(error)
            )
        finally:
            fsync_directory(CANDIDATE_ROOT)
    require(not failures, ";".join(failures))


def publish_candidate_and_receipt(
    stage: Path,
    output: Path,
    receipt_output: Path,
    receipt_payload: bytes,
    *,
    inject_failure: str | None = None,
) -> None:
    receipt_parent = receipt_output.parent
    receipt_stage = receipt_output.with_name(
        receipt_output.name + f".stage-{os.getpid()}"
    )
    output_created = False
    receipt_parent_created = False
    receipt_stage_created = False
    receipt_final_created = False
    try:
        rename_noreplace(stage, output)
        output_created = True
        fsync_directory(CANDIDATE_ROOT)
        if inject_failure == "AFTER_OUTPUT_RENAME":
            raise C42Error("injected failure after output rename")
        os.mkdir(receipt_parent, 0o755)
        receipt_parent_created = True
        fsync_directory(AUDIT_ROOT)
        if inject_failure == "AFTER_RECEIPT_PARENT_CREATE":
            raise C42Error("injected failure after receipt parent create")
        write_exclusive_fsynced(receipt_stage, receipt_payload)
        receipt_stage_created = True
        if inject_failure == "AFTER_RECEIPT_STAGE_WRITE":
            raise C42Error("injected failure after receipt stage write")
        rename_noreplace(receipt_stage, receipt_output)
        receipt_stage_created = False
        receipt_final_created = True
        fsync_directory(receipt_parent)
        fsync_directory(AUDIT_ROOT)
        if inject_failure == "AFTER_RECEIPT_FINAL_RENAME":
            raise C42Error("injected failure after receipt final rename")
    except Exception as original:
        rollback_error: Exception | None = None
        try:
            rollback_publication(
                output,
                receipt_output,
                receipt_stage,
                output_created=output_created,
                receipt_parent_created=receipt_parent_created,
                receipt_stage_created=receipt_stage_created,
                receipt_final_created=receipt_final_created,
            )
        except Exception as error:
            rollback_error = error
        if stage.exists():
            shutil.rmtree(stage)
            fsync_directory(CANDIDATE_ROOT)
        if rollback_error is not None:
            raise C42Error(
                "publication failed and rollback was incomplete:"
                + str(rollback_error)
            ) from original
        raise


def source_pins() -> dict[str, str]:
    observed = {
        "C41": file_sha256(Path(c41.__file__).resolve()),
        "C41_independent_auditor": file_sha256(
            DELIVERABLES
            / "cm2_round306c41_d02_lower_strata_depth3_closure_"
              "independent_auditor_v1.py"
        ),
        "Round185": file_sha256(Path(round185.__file__).resolve()),
        "C40": file_sha256(Path(c40.__file__).resolve()),
    }
    require(observed == {
        "C41": EXPECTED_C41_SOURCE,
        "C41_independent_auditor": EXPECTED_C41_AUDITOR_SOURCE,
        "Round185": EXPECTED_ROUND185_SOURCE,
        "C40": EXPECTED_C40_SOURCE,
    }, "C42 source pins")
    c41.source_pins()
    return observed


def formal_gate(audit_path: Path | None) -> dict[str, Any]:
    require(
        HEX64.fullmatch(EXPECTED_C41_AUDIT_OBJECT) is not None
        and EXPECTED_C41_AUDIT_STATUS.startswith("PASS_"),
        "C41 independent audit pins",
    )
    require(audit_path is not None, "C41 independent audit path")
    require(
        audit_path == (ROOT / EXPECTED_C41_AUDIT_PATH).resolve(),
        "C41 independent audit canonical pinned path",
    )
    require_regular_single_link(audit_path, "C41 independent audit")
    require(
        file_sha256(audit_path) == EXPECTED_C41_AUDIT_FILE_SHA256,
        "C41 independent audit file SHA256",
    )
    audit = strict_json(audit_path)
    validate_self_object(audit, "object_sha256", "C41 independent audit")
    require(
        audit["object_sha256"] == EXPECTED_C41_AUDIT_OBJECT
        and audit.get("candidate_object_sha256") == EXPECTED_C41_OBJECT
        and audit.get("producer_source_sha256") == EXPECTED_C41_SOURCE
        and audit.get("status") == EXPECTED_C41_AUDIT_STATUS,
        "C41 independent audit binding",
    )
    return audit


def validate_receipt(path: Path, candidate: Path) -> dict[str, Any]:
    require_regular_single_link(path, "C41 receipt")
    receipt = strict_json(path)
    validate_self_object(receipt, "receipt_object_sha256", "C41 receipt")
    require(
        receipt["schema"] == c41.RECEIPT_SCHEMA
        and receipt["receipt_object_sha256"] == EXPECTED_C41_RECEIPT_OBJECT
        and receipt["candidate_object_sha256"] == EXPECTED_C41_OBJECT
        and receipt["producer_source_sha256"] == EXPECTED_C41_SOURCE
        and receipt["root_manifest_sha256"] == EXPECTED_C41_ROOT_MANIFEST
        and (ROOT / receipt["candidate_path"]).resolve() == candidate,
        "C41 receipt exact binding",
    )
    return receipt


def effective_incident(row: dict[str, Any]) -> dict[str, Any]:
    is_target = row["c41_ambient_cell_id"] == TARGET_AMBIENT_ID
    disposition = (
        "TERMINAL_EXCLUDED_BY_C42_CLOSED_COVER"
        if is_target else row["disposition_family"]
    )
    return {
        "pair_index": row["pair_index"],
        "representative_cell_id": row["representative_cell_id"],
        "path": row["path"],
        "c41_ambient_cell_id": row["c41_ambient_cell_id"],
        "c41_row_sha256": row["row_sha256"],
        "C41_disposition_family": row["disposition_family"],
        "C42_effective_disposition_family": disposition,
        "terminal_after_C42": disposition.startswith("TERMINAL_EXCLUDED"),
    }


def owner_key(row: dict[str, Any]) -> tuple[str, int, str]:
    return row["path"], row["pair_index"], row["c41_ambient_cell_id"]


def contains_point(row: dict[str, Any], t: Q, p: Q) -> bool:
    box = row["closed_representative_box"]
    if box is None:
        return False
    return (
        Q(box["t"][0]) <= t <= Q(box["t"][1])
        and Q(box["p"][0]) <= p <= Q(box["p"][1])
        and Q(box["s"][0]) == Q(0) == Q(box["s"][1])
    )


def load_input(
    candidate: Path,
    receipt_path: Path,
    audit_path: Path | None,
    *,
    formal: bool,
) -> dict[str, Any]:
    pins = source_pins()
    result = c41.validate_c41_candidate(candidate)
    require(
        result["schema"] == c41.SCHEMA
        and result["status"] == EXPECTED_C41_STATUS
        and result["object_sha256"] == EXPECTED_C41_OBJECT,
        "exact C41 candidate",
    )
    require(
        file_sha256(candidate / "root_manifest.sha256")
        == EXPECTED_C41_ROOT_MANIFEST,
        "C41 root manifest pin",
    )
    receipt = validate_receipt(receipt_path, candidate)
    audit = formal_gate(audit_path)

    ambient_rows: list[dict[str, Any]] = []
    ambient_by_id: dict[str, dict[str, Any]] = {}
    needed_ids = set().union(*CORNER_INCIDENT_IDS.values())
    for row in c41.iter_ledger(
        candidate, result["ledgers"]["routed_ambient_cells"]
    ):
        ambient_rows.append(row)
        if row["c41_ambient_cell_id"] in needed_ids:
            require(row["c41_ambient_cell_id"] not in ambient_by_id,
                    "unique needed ambient id")
            ambient_by_id[row["c41_ambient_cell_id"]] = row
    require(set(ambient_by_id) == needed_ids, "complete P391 incident rows")
    target = ambient_by_id[TARGET_AMBIENT_ID]
    require(
        target["row_sha256"] == TARGET_AMBIENT_ROW
        and target["pair_index"] == PAIR_INDEX
        and target["path"] == TARGET_PATH
        and target["closed_representative_box"] == REPRESENTATIVE_BOX
        and target["closed_reflected_box"] == REFLECTED_BOX
        and target["representative_cell_id"] == REPRESENTATIVE_CELL_ID
        and target["reflected_cell_id"] == REFLECTED_CELL_ID
        and target["parent_volume_fraction"] == qstr(TARGET_FRACTION)
        and target["residual_classification"]
        == "UNRESOLVED_C41_COLLISION2_WALL_ENDPOINT_OUTER",
        "exact C41 P391 target",
    )

    c2_outer = None
    for row in c41.iter_ledger(
        candidate, result["ledgers"]["c2_surface_outers"]
    ):
        if row["c2_surface_outer_id"] == TARGET_C2_OUTER_ID:
            require(c2_outer is None, "unique C41 C2 outer")
            c2_outer = row
    require(
        c2_outer is not None
        and c2_outer["row_sha256"] == TARGET_C2_OUTER_ROW
        and c2_outer["normalized_surface_count"] == 0,
        "exact C41 C2 wall outer",
    )

    boundary = None
    for row in c41.iter_ledger(
        candidate, result["ledgers"]["boundary_corner_outers"]
    ):
        if row["boundary_corner_outer_id"] == TARGET_BOUNDARY_ID:
            require(boundary is None, "unique C41 boundary outer")
            boundary = row
    require(
        boundary is not None
        and boundary["row_sha256"] == TARGET_BOUNDARY_ROW
        and boundary["owning_outer_id"] == TARGET_C2_OUTER_ID
        and boundary["exact_face_row_count"] == 4
        and boundary["exact_corner_row_count"] == 4,
        "exact C41 boundary outer",
    )

    parents = list(c41.iter_ledger(
        candidate, result["ledgers"]["parent_conservation"]
    ))
    require(len(parents) == 862, "C41 862 parent rows")
    target_parent = {row["pair_index"]: row for row in parents}[PAIR_INDEX]
    require(
        target_parent["row_sha256"] == TARGET_PARENT_ROW
        and target_parent["terminal_excluded_parent_volume"] == "511/512"
        and target_parent["unresolved_parent_volume"] == "1/512"
        and target_parent["nonterminal_leaf_count"] == 1,
        "exact C41 P391 parent deficit",
    )

    c40_candidate = (ROOT / result["C40_authority"]["path"]).resolve()
    context = c41.load_context(c40_candidate, None, formal=False)
    config = c41.decode_worker_config(context["config"])
    c40_row = None
    for row in c41.iter_ledger(
        c40_candidate,
        context["result"]["ledgers"]["routed_leaf_cells"],
    ):
        if row["c40_leaf_id"] == TARGET_C40_LEAF_ID:
            require(c40_row is None, "unique C40 source leaf")
            c40_row = row
    require(
        c40_row is not None
        and c40_row["row_sha256"] == TARGET_C40_ROW
        and c40_row["c38_source_row_sha256"] == TARGET_C38_ROW,
        "exact C40 source leaf",
    )
    c38_row = context["c38_index"].get(TARGET_C38_ROW)
    require(
        c38_row is not None
        and c38_row["representative_origin_key"] == REPRESENTATIVE_PARENT_KEY
        and c38_row["reflected_origin_key"] == REFLECTED_PARENT_KEY,
        "exact C38 parent keys",
    )
    require(
        config["original_path"][1]["selected_absolute_owner_id"]
        == EXPECTED_REP_LIVE_OWNER
        and config["reflected_path"][1]["selected_absolute_owner_id"]
        == EXPECTED_REF_LIVE_OWNER,
        "exact live collision-two owner authorities",
    )
    return {
        "pins": pins,
        "result": result,
        "receipt": receipt,
        "audit": audit,
        "ambient_rows": ambient_rows,
        "ambient_by_id": ambient_by_id,
        "target": target,
        "c2_outer": c2_outer,
        "boundary": boundary,
        "parents": parents,
        "c40_candidate": c40_candidate,
        "c40_result": context["result"],
        "c40_row": c40_row,
        "c38_row": c38_row,
        "config": config,
    }


def strict_open_integer_strip(q: arb, h: arb, axis: str) -> dict[str, Any]:
    matches = [
        wall for wall in range(-6, 7)
        if bool(q > wall) and bool(q < wall + 1)
        and bool(h > wall) and bool(h < wall + 1)
    ]
    require(len(matches) == 1, f"unique strict {axis} integer strip")
    wall = matches[0]
    events, reason = registry.ordered_axis_events(q, h, axis)
    require(events == [] and reason is None, f"empty strict {axis} events")
    return {
        "axis": axis,
        "open_integer_strip": [wall, wall + 1],
        "start_endpoint": arb_bounds(q),
        "hit_endpoint": arb_bounds(h),
        "start_and_hit_strictly_inside_same_open_strip": True,
        "ordered_axis_event_tokens": [],
        "endpoint_on_integer_wall": False,
    }


def certify_box(
    orientation: str,
    parent_key: str,
    box: Any,
    config: dict[str, Any],
    ordinal: int,
    half_open_role: str,
) -> dict[str, Any]:
    pair_index = config["pair_index"]
    pattern_index = config["pattern_index"]
    status, detail, evidence, baseline = round185.resolve_dynamic_box(
        parent_key, box, pair_index, pattern_index
    )
    require(
        status == "LOCAL_EXACT_KEY"
        and baseline == "LOCAL_EXACT_KEY"
        and evidence == [],
        f"strict closed-box Round185 result:{orientation}:{ordinal}",
    )
    owner_status, owner, owner_evidence = round185.enhanced_select_owner(
        parent_key, box
    )
    require(
        owner_status == "STRICT_UNIQUE_OWNER"
        and owner is not None,
        f"strict enhanced owner:{orientation}:{ordinal}",
    )
    expected_owner = (
        EXPECTED_REP_OWNER if orientation == "REPRESENTATIVE"
        else EXPECTED_REF_OWNER
    )
    expected_outgoing = (
        EXPECTED_REP_OUTGOING if orientation == "REPRESENTATIVE"
        else EXPECTED_REF_OUTGOING
    )
    expected_word = (
        EXPECTED_REP_WORD_ROW if orientation == "REPRESENTATIVE"
        else EXPECTED_REF_WORD_ROW
    )
    expected_live_owner = (
        EXPECTED_REP_LIVE_OWNER if orientation == "REPRESENTATIVE"
        else EXPECTED_REF_LIVE_OWNER
    )
    require(
        owner[0] == detail["absolute_collision2_owner"] == expected_owner
        and detail["collision2_outgoing_chart"] == expected_outgoing
        and detail["official_gate5_key"]["row"] == expected_word
        and detail["ordered_clean_wall_record"] == [],
        f"exact owner/chart/word:{orientation}:{ordinal}",
    )
    classification, witness = c40.expected_collision2(detail, config)
    require(
        classification == "EXCLUDED_C40_COLLISION2_OWNER_MISMATCH"
        and witness == expected_owner
        and expected_owner != expected_live_owner,
        f"strict collision-two owner exclusion:{orientation}:{ordinal}",
    )
    state = round181.collision1_state_direct(parent_key, box)
    hit_x = state["contact_x"] + owner[1]["near"] * state["outgoing_x"]
    hit_y = state["contact_y"] + owner[1]["near"] * state["outgoing_y"]
    x_strip = strict_open_integer_strip(
        state["contact_x"] - 1, hit_x - 1, "X"
    )
    y_strip = strict_open_integer_strip(
        state["contact_y"], hit_y, "Y"
    )
    crossings, reason = registry.strict_event_order([])
    require(crossings == () and reason is None, "empty event order")
    row = {
        "schema": INTERIOR_SCHEMA,
        "pair_index": PAIR_INDEX,
        "source_c41_ambient_cell_id": TARGET_AMBIENT_ID,
        "source_c41_row_sha256": TARGET_AMBIENT_ROW,
        "orientation": orientation,
        "certificate_ordinal": ordinal,
        "parent_key": parent_key,
        "closed_box": box_payload(
            box, reflected=orientation == "REFLECTED"
        ),
        "closed_box_scope": "ENTIRE_CLOSED_DYADIC_HALF_BOX",
        "half_open_shared_mid_face_role": half_open_role,
        "Round185_baseline_status": baseline,
        "Round185_status": status,
        "enhanced_owner_status": owner_status,
        "enhanced_owner_surface_evidence_count": len(owner_evidence),
        "absolute_collision2_owner": owner[0],
        "strict_owner_near_root": arb_bounds(owner[1]["near"]),
        "collision2_outgoing_chart": detail["collision2_outgoing_chart"],
        "official_gate5_key": detail["official_gate5_key"],
        "ordered_clean_wall_record": [],
        "strict_axis_endpoint_certificates": [x_strip, y_strip],
        "wall_endpoint_or_corner_present_on_closed_box": False,
        "strict_disposition": classification,
        "disposition_witness": witness,
        "expected_live_collision2_owner": expected_live_owner,
        "owner_mismatch_is_uniform_on_entire_closed_box": True,
        "local_round144_terminal_credit": 1,
        "D02_gate_credit": 0,
    }
    row["interior_certificate_id"] = "c42-interior:" + digest(row)
    return row


def face_box(value: dict[str, Any], name: str) -> Any:
    t0, t1 = map(Q, value["t"])
    p0, p1 = map(Q, value["p"])
    if name == "t_lower":
        t1 = t0
    elif name == "t_upper":
        t0 = t1
    elif name == "p_lower":
        p1 = p0
    elif name == "p_upper":
        p0 = p1
    else:  # pragma: no cover - closed enum
        raise C42Error("unknown face")
    return atlas.AtlasBox(t0, t1, p0, p1, Q(0), Q(0), 10,
                          TARGET_PATH + "." + name)


def point_box(value: dict[str, Any], name: str) -> Any:
    t0, t1 = map(Q, value["t"])
    p0, p1 = map(Q, value["p"])
    t = t0 if name.startswith("t0") else t1
    p = p0 if name.endswith("p0") else p1
    return atlas.AtlasBox(t, t, p, p, Q(0), Q(0), 10,
                          TARGET_PATH + "." + name)


def exact_face_rows(
    context: dict[str, Any],
    config: dict[str, Any],
) -> list[dict[str, Any]]:
    boundary_faces = {
        row["face"]: row for row in context["boundary"]["face_rows"]
    }
    require(set(boundary_faces) == set(EXPECTED_FACE_IDS),
            "four C41 boundary faces")
    rows = []
    for ordinal, name in enumerate((
        "t_lower", "t_upper", "p_lower", "p_upper"
    )):
        source_face = boundary_faces[name]
        neighbor_id, neighbor_sha, neighbor_path = FACE_NEIGHBORS[name]
        neighbor = context["ambient_by_id"][neighbor_id]
        require(
            source_face["boundary_face_id"] == EXPECTED_FACE_IDS[name]
            and neighbor["row_sha256"] == neighbor_sha
            and neighbor["path"] == neighbor_path
            and neighbor["disposition_family"] == "TERMINAL_EXCLUDED",
            f"exact face neighbor:{name}",
        )
        box = face_box(REPRESENTATIVE_BOX, name)
        face_cert = certify_box(
            "REPRESENTATIVE", REPRESENTATIVE_PARENT_KEY, box, config,
            100 + ordinal, "FACE_RESTRICTION_NO_MID_FACE_ROLE",
        )
        incidents = [
            effective_incident(context["target"]),
            effective_incident(neighbor),
        ]
        incidents.sort(key=owner_key)
        owner = incidents[0]
        require(
            all(row["terminal_after_C42"] for row in incidents)
            and owner["path"] == {
                "t_lower": "111101110",
                "t_upper": TARGET_PATH,
                "p_lower": "11110110",
                "p_upper": "100010",
            }[name],
            f"terminal lexicographic face owner:{name}",
        )
        row = {
            "schema": FACE_SCHEMA,
            "pair_index": PAIR_INDEX,
            "face": name,
            "C41_boundary_face_id": source_face["boundary_face_id"],
            "C41_boundary_outer_id": TARGET_BOUNDARY_ID,
            "exact_closed_face_box": box_payload(box),
            "direct_closed_face_certificate": face_cert,
            "incident_ambient_cells": incidents,
            "incident_cell_count": 2,
            "owner_rule": (
                "LEXICOGRAPHIC_MINIMUM_(PATH,PAIR_INDEX,AMBIENT_ID)_"
                "AMONG_INCIDENT_CELLS"
            ),
            "owner_incident": owner,
            "owner_is_terminal_after_C42": True,
            "face_has_no_unresolved_wall_endpoint": True,
            "D02_gate_credit": 0,
        }
        row["face_owner_incidence_id"] = "c42-face:" + digest(row)
        rows.append(row)
    return rows


def exact_corner_rows(
    context: dict[str, Any],
    config: dict[str, Any],
) -> list[dict[str, Any]]:
    boundary_corners = {
        row["corner"]: row for row in context["boundary"]["corner_rows"]
    }
    require(set(boundary_corners) == set(EXPECTED_CORNER_IDS),
            "four C41 boundary corners")
    rows = []
    for ordinal, name in enumerate(("t0p0", "t0p1", "t1p0", "t1p1")):
        source_corner = boundary_corners[name]
        box = point_box(REPRESENTATIVE_BOX, name)
        t, p = box.t0, box.p0
        observed = {
            row["c41_ambient_cell_id"]: row
            for row in context["ambient_rows"]
            if contains_point(row, t, p)
        }
        require(
            set(observed) == CORNER_INCIDENT_IDS[name]
            and source_corner["boundary_corner_id"]
            == EXPECTED_CORNER_IDS[name],
            f"complete global corner incident census:{name}",
        )
        incidents = [effective_incident(row) for row in observed.values()]
        incidents.sort(key=owner_key)
        owner = incidents[0]
        expected_owner_path = {
            "t0p0": "11110110",
            "t0p1": "100010",
            "t1p0": "11110110",
            "t1p1": "100010",
        }[name]
        require(
            all(row["terminal_after_C42"] for row in incidents)
            and owner["path"] == expected_owner_path,
            f"terminal lexicographic corner owner:{name}",
        )
        point_cert = certify_box(
            "REPRESENTATIVE", REPRESENTATIVE_PARENT_KEY, box, config,
            200 + ordinal, "ZERO_DIMENSIONAL_OWNER_POINT",
        )
        reflected_t = -t
        reflected_p = -p
        row = {
            "schema": CORNER_SCHEMA,
            "pair_index": PAIR_INDEX,
            "corner": name,
            "C41_boundary_corner_id": source_corner["boundary_corner_id"],
            "C41_boundary_outer_id": TARGET_BOUNDARY_ID,
            "exact_closed_corner_box": box_payload(box),
            "exact_reflected_corner": {
                "t": qstr(reflected_t),
                "p": qstr(reflected_p),
                "s": "0",
            },
            "direct_closed_point_certificate": point_cert,
            "global_incident_ambient_cells": incidents,
            "global_incident_cell_count": len(incidents),
            "global_incident_census_complete": True,
            "owner_rule": (
                "LEXICOGRAPHIC_MINIMUM_(PATH,PAIR_INDEX,AMBIENT_ID)_"
                "AMONG_INCIDENT_CELLS"
            ),
            "owner_incident": owner,
            "owner_is_terminal_after_C42": True,
            "all_incidents_terminal_after_C42": True,
            "corner_has_no_unresolved_wall_endpoint": True,
            "D02_gate_credit": 0,
        }
        row["corner_owner_incidence_id"] = "c42-corner:" + digest(row)
        rows.append(row)
    return rows


def build_interior(
    config: dict[str, Any],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    representative = box_from_payload(REPRESENTATIVE_BOX, TARGET_PATH)
    reflected = box_from_payload(REFLECTED_BOX, TARGET_PATH + ".reflected")
    rep_halves = ge.split(representative)
    ref_halves = ge.split(reflected)
    require(
        rep_halves[0].p1 == rep_halves[1].p0 == MID_P
        and ref_halves[0].p1 == ref_halves[1].p0 == -MID_P,
        "exact p midpoint splits",
    )
    rep_rows = [
        certify_box(
            "REPRESENTATIVE", REPRESENTATIVE_PARENT_KEY, rep_halves[index],
            config, index,
            "OWNS_SHARED_P_MID_FACE" if index == 0
            else "EXCLUDES_SHARED_P_MID_FACE",
        )
        for index in range(2)
    ]
    ref_rows = [
        certify_box(
            "REFLECTED", REFLECTED_PARENT_KEY, ref_halves[index], config,
            2 + index,
            "OWNS_SHARED_P_MID_FACE" if index == 0
            else "EXCLUDES_SHARED_P_MID_FACE",
        )
        for index in range(2)
    ]
    require(
        sum(
            (box.t1 - box.t0) * (box.p1 - box.p0)
            for box in rep_halves
        )
        == (representative.t1 - representative.t0)
        * (representative.p1 - representative.p0),
        "representative closed cover area conservation",
    )
    return rep_rows + ref_rows, [
        {
            "schema": REFLECTION_SCHEMA,
            "pair_index": PAIR_INDEX,
            "representative_certificate_id": rep_rows[index][
                "interior_certificate_id"
            ],
            "reflected_certificate_id": ref_rows[1 - index][
                "interior_certificate_id"
            ],
            "representative_closed_box": rep_rows[index]["closed_box"],
            "reflected_closed_box": ref_rows[1 - index]["closed_box"],
            "exact_map": "(t,p,s)->(-t,-p,s)",
            "endpoint_order_reversal_materialized": True,
            "owner_map": [EXPECTED_REP_OWNER, EXPECTED_REF_OWNER],
            "outgoing_chart_map": [EXPECTED_REP_OUTGOING, EXPECTED_REF_OUTGOING],
            "relative_target_map": ["G[0,0]", "G[0,1]"],
            "empty_wall_word_preserved": True,
            "strict_owner_mismatch_preserved": True,
            "reflection_transport_terminal_credit": 1,
            "D02_gate_credit": 0,
        }
        for index in range(2)
    ]


def validate_parent_credit_rows(
    rows: list[dict[str, Any]], label: str
) -> dict[str, int]:
    require(
        len(rows) == 862
        and [row["pair_index"] for row in rows] == list(range(862)),
        f"{label}:ordered 862 parent rows",
    )
    whole = sum(bool(row["whole_representative_parent_terminal"])
                for row in rows)
    credit_two = 0
    credit_zero = 0
    credit_sum = 0
    for row in rows:
        derived_whole = (
            Q(row["terminal_excluded_parent_volume"]) == 1
            and Q(row["unresolved_parent_volume"]) == 0
            and row["nonterminal_leaf_count"] == 0
            and row["terminal_reflection_transport_materialized"] is True
        )
        whole_row = row["whole_representative_parent_terminal"]
        require(
            whole_row is derived_whole
            and row["whole_reflected_parent_terminal"] is derived_whole
            and row["leaf_count"]
            == row["terminal_leaf_count"] + row["nonterminal_leaf_count"],
            f"{label}:paired whole flag:{row['pair_index']}",
        )
        expected = 2 if whole_row else 0
        observed = row["C34_common_refinement_credit"]
        require(
            observed == expected,
            f"{label}:credit iff whole:{row['pair_index']}",
        )
        credit_two += int(observed == 2)
        credit_zero += int(observed == 0)
        credit_sum += observed
    target = rows[PAIR_INDEX]
    require(
        whole == 287
        and credit_two == 287
        and credit_zero == 575
        and credit_sum == 574,
        f"{label}:frozen C34 credit census",
    )
    require(
        target["newly_whole_terminal_vs_C41"] is True
        and sum(bool(row["newly_whole_terminal_vs_C41"]) for row in rows) == 1,
        f"{label}:unique P391 new whole transition",
    )
    return {
        "whole_terminal_representative_parent_count": whole,
        "whole_terminal_paired_coarse_cell_count": 2 * whole,
        "C34_common_refinement_credit_two_row_count": credit_two,
        "C34_common_refinement_credit_zero_row_count": credit_zero,
        "C34_common_refinement_credit_sum": credit_sum,
    }


def parent_credit_regressions(rows: list[dict[str, Any]]) -> list[str]:
    def rejected(mutated: list[dict[str, Any]], label: str) -> None:
        try:
            validate_parent_credit_rows(mutated, "mutation:" + label)
        except C42Error:
            return
        raise C42Error("parent credit mutation accepted:" + label)

    whole_index = next(
        index for index, row in enumerate(rows)
        if row["whole_representative_parent_terminal"]
    )
    partial_index = next(
        index for index, row in enumerate(rows)
        if not row["whole_representative_parent_terminal"]
    )
    mutations = []
    value = copy.deepcopy(rows)
    value[whole_index]["C34_common_refinement_credit"] = 0
    rejected(value, "WHOLE_CREDIT_ZEROED")
    mutations.append("WHOLE_CREDIT_ZEROED")
    value = copy.deepcopy(rows)
    value[partial_index]["C34_common_refinement_credit"] = 2
    rejected(value, "PARTIAL_CREDIT_FORGED")
    mutations.append("PARTIAL_CREDIT_FORGED")
    value = copy.deepcopy(rows)
    value[PAIR_INDEX]["whole_reflected_parent_terminal"] = False
    rejected(value, "PAIRED_WHOLE_FLAG_DROPPED")
    mutations.append("PAIRED_WHOLE_FLAG_DROPPED")
    value = copy.deepcopy(rows)
    value[whole_index]["C34_common_refinement_credit"] = 1
    rejected(value, "NONBINARY_CREDIT_FORGED")
    mutations.append("NONBINARY_CREDIT_FORGED")
    value = copy.deepcopy(rows)
    for key in (
        "whole_representative_parent_terminal",
        "whole_reflected_parent_terminal",
        "C34_common_refinement_credit",
    ):
        value[whole_index][key], value[partial_index][key] = (
            value[partial_index][key], value[whole_index][key]
        )
    rejected(value, "WHOLE_PARTIAL_FLAGS_AND_CREDIT_SWAPPED")
    mutations.append("WHOLE_PARTIAL_FLAGS_AND_CREDIT_SWAPPED")
    value = copy.deepcopy(rows)
    value[whole_index]["terminal_reflection_transport_materialized"] = False
    rejected(value, "WHOLE_REFLECTION_MATERIALIZATION_DROPPED")
    mutations.append("WHOLE_REFLECTION_MATERIALIZATION_DROPPED")
    value = copy.deepcopy(rows)
    value[whole_index]["nonterminal_leaf_count"] = 1
    value[whole_index]["terminal_leaf_count"] -= 1
    rejected(value, "WHOLE_NONTERMINAL_LEAF_FORGED")
    mutations.append("WHOLE_NONTERMINAL_LEAF_FORGED")
    value = copy.deepcopy(rows)
    value[PAIR_INDEX]["newly_whole_terminal_vs_C41"] = False
    rejected(value, "P391_NEW_WHOLE_FLAG_DROPPED")
    mutations.append("P391_NEW_WHOLE_FLAG_DROPPED")
    value = copy.deepcopy(rows)
    value[1] = copy.deepcopy(value[0])
    rejected(value, "DUPLICATE_PAIR_INDEX")
    mutations.append("DUPLICATE_PAIR_INDEX")
    rejected(copy.deepcopy(rows[:-1]), "MISSING_PAIR_ROW")
    mutations.append("MISSING_PAIR_ROW")
    value = copy.deepcopy(rows)
    value[0], value[1] = value[1], value[0]
    rejected(value, "PAIR_ORDER_SWAPPED")
    mutations.append("PAIR_ORDER_SWAPPED")
    return mutations


def parent_rows(
    prior_rows: list[dict[str, Any]]
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    rows = []
    whole = 0
    newly = 0
    for prior in sorted(prior_rows, key=lambda row: row["pair_index"]):
        pair = prior["pair_index"]
        prior_terminal = Q(prior["terminal_excluded_parent_volume"])
        prior_unresolved = Q(prior["unresolved_parent_volume"])
        if pair == PAIR_INDEX:
            gain = TARGET_FRACTION
            terminal = Q(1)
            unresolved = Q(0)
            terminal_leaf_count = prior["terminal_leaf_count"] + 1
            nonterminal_leaf_count = prior["nonterminal_leaf_count"] - 1
            reflection_materialized = True
        else:
            gain = Q(0)
            terminal = prior_terminal
            unresolved = prior_unresolved
            terminal_leaf_count = prior["terminal_leaf_count"]
            nonterminal_leaf_count = prior["nonterminal_leaf_count"]
            reflection_materialized = prior[
                "terminal_reflection_transport_materialized"
            ]
        require(
            prior_terminal + prior_unresolved == 1
            and prior_terminal + gain == terminal
            and terminal + unresolved == 1
            and nonterminal_leaf_count >= 0,
            f"parent conservation:{pair}",
        )
        prior_whole = (
            prior["whole_representative_parent_terminal"]
            and prior["whole_reflected_parent_terminal"]
        )
        is_whole = (
            terminal == 1
            and unresolved == 0
            and nonterminal_leaf_count == 0
            and reflection_materialized is True
        )
        new = is_whole and not prior_whole
        credit = 2 if is_whole else 0
        require(
            (pair == PAIR_INDEX and prior["C34_common_refinement_credit"] == 0)
            or (
                pair != PAIR_INDEX
                and prior["C34_common_refinement_credit"] == credit
            ),
            f"cross-generation C34 credit preservation:{pair}",
        )
        whole += int(is_whole)
        newly += int(new)
        row = {
            "schema": PARENT_SCHEMA,
            "pair_index": pair,
            "C41_parent_row_sha256": prior["row_sha256"],
            "C41_terminal_excluded_parent_volume": qstr(prior_terminal),
            "C41_unresolved_parent_volume": qstr(prior_unresolved),
            "C42_terminal_gain": qstr(gain),
            "terminal_excluded_parent_volume": qstr(terminal),
            "unresolved_parent_volume": qstr(unresolved),
            "parent_Kraft_conservation": "1",
            "leaf_count": prior["leaf_count"],
            "terminal_leaf_count": terminal_leaf_count,
            "nonterminal_leaf_count": nonterminal_leaf_count,
            "newly_whole_terminal_vs_C41": new,
            "whole_representative_parent_terminal": is_whole,
            "whole_reflected_parent_terminal": is_whole,
            "terminal_reflection_transport_materialized": (
                reflection_materialized
            ),
            "C34_common_refinement_credit": credit,
            "D02_gate_credit": 0,
        }
        require(
            row["leaf_count"]
            == row["terminal_leaf_count"] + row["nonterminal_leaf_count"],
            f"leaf census conservation:{pair}",
        )
        rows.append(row)
    require(newly == 1, "C42 exact new whole parent census")
    census = validate_parent_credit_rows(rows, "producer")
    regressions = parent_credit_regressions(rows)
    return rows, {
        **census,
        "newly_whole_terminal_representative_parent_count": newly,
        "newly_whole_terminal_paired_coarse_cell_count": 2 * newly,
        "parent_credit_regression_count": len(regressions),
        "parent_credit_regressions_rejected": regressions,
    }


def source_row(
    context: dict[str, Any],
    candidate: Path,
    receipt_path: Path,
    formal: bool,
) -> dict[str, Any]:
    row = {
        "schema": SOURCE_SCHEMA,
        "pair_index": PAIR_INDEX,
        "C41_input_mode": "AUDITED_C41_FORMAL_INPUT",
        "C41_candidate_path": str(candidate.relative_to(ROOT)),
        "C41_candidate_object_sha256": EXPECTED_C41_OBJECT,
        "C41_candidate_status": EXPECTED_C41_STATUS,
        "C41_producer_source_sha256": EXPECTED_C41_SOURCE,
        "C41_root_manifest_sha256": EXPECTED_C41_ROOT_MANIFEST,
        "C41_receipt_path": str(receipt_path.relative_to(ROOT)),
        "C41_receipt_object_sha256": EXPECTED_C41_RECEIPT_OBJECT,
        "C41_independent_audit_path": EXPECTED_C41_AUDIT_PATH,
        "C41_independent_audit_object_sha256": context["audit"][
            "object_sha256"
        ],
        "C41_independent_audit_status": context["audit"]["status"],
        "C41_independent_auditor_source_sha256": (
            EXPECTED_C41_AUDITOR_SOURCE
        ),
        "C41_candidate_and_audit_pointers_installed": True,
        "producer_mode": "FORMAL_PRODUCER_PASS" if formal else "REVIEW",
        "producer_output_is_authority": False,
        "independent_C42_audit_outstanding": True,
        "C41_target_ambient_cell_id": TARGET_AMBIENT_ID,
        "C41_target_ambient_row_sha256": TARGET_AMBIENT_ROW,
        "C41_C2_outer_id": TARGET_C2_OUTER_ID,
        "C41_C2_outer_row_sha256": TARGET_C2_OUTER_ROW,
        "C41_boundary_outer_id": TARGET_BOUNDARY_ID,
        "C41_boundary_outer_row_sha256": TARGET_BOUNDARY_ROW,
        "C41_parent_row_sha256": TARGET_PARENT_ROW,
        "C40_source_leaf_id": TARGET_C40_LEAF_ID,
        "C40_source_row_sha256": TARGET_C40_ROW,
        "C38_source_row_sha256": TARGET_C38_ROW,
        "representative_parent_key": REPRESENTATIVE_PARENT_KEY,
        "reflected_parent_key": REFLECTED_PARENT_KEY,
        "representative_cell_id": REPRESENTATIVE_CELL_ID,
        "reflected_cell_id": REFLECTED_CELL_ID,
        "source_closed_representative_box": REPRESENTATIVE_BOX,
        "source_closed_reflected_box": REFLECTED_BOX,
        "source_parent_volume_fraction": qstr(TARGET_FRACTION),
        "source_residual_classification": (
            "UNRESOLVED_C41_COLLISION2_WALL_ENDPOINT_OUTER"
        ),
        "source_binding_complete": True,
        "D02_gate_credit": 0,
    }
    row["exact_source_id"] = "c42-source:" + digest(row)
    return row


def write_manifest(directory: Path) -> None:
    members = sorted(
        path for path in directory.iterdir()
        if path.name != "root_manifest.sha256"
    )
    (directory / "root_manifest.sha256").write_text(
        "".join(f"{file_sha256(path)}  {path.name}\n" for path in members),
        encoding="utf-8",
    )


def validate_manifest(directory: Path) -> None:
    require(
        sorted(path.name for path in directory.iterdir()) == list(INVENTORY),
        "C42 exact nine-file inventory",
    )
    raw = (directory / "root_manifest.sha256").read_text(encoding="utf-8")
    expected = "".join(
        f"{file_sha256(path)}  {path.name}\n"
        for path in sorted(directory.iterdir())
        if path.name != "root_manifest.sha256"
    )
    require(raw == expected, "C42 root manifest replay")


def validate_published_candidate(
    directory: Path, expected_result: dict[str, Any]
) -> None:
    value = directory.lstat()
    require(
        stat.S_ISDIR(value.st_mode) and not directory.is_symlink(),
        "published C42 candidate real directory",
    )
    validate_manifest(directory)
    for member in directory.iterdir():
        require_regular_single_link(member, "published C42 member")
    result = strict_json(directory / "result.json")
    validate_self_object(result, "object_sha256", "published C42 candidate")
    require(result == expected_result, "published C42 result recapture")
    for descriptor in result["ledgers"].values():
        for _row in c41.iter_ledger(directory, descriptor):
            pass


def validate_published_receipt(
    path: Path, expected: dict[str, Any]
) -> None:
    require_regular_single_link(path, "published C42 receipt")
    require(
        stat.S_IMODE(path.stat().st_mode) == 0o600,
        "published C42 receipt mode 0600",
    )
    replay = strict_json(path)
    validate_self_object(
        replay, "receipt_object_sha256", "published C42 receipt"
    )
    require(replay == expected, "published C42 receipt recapture")


def fsync_file(path: Path) -> None:
    with path.open("rb") as stream:
        os.fsync(stream.fileno())


def proc_start_ticks(pid: int) -> int:
    raw = Path(f"/proc/{pid}/stat").read_text(encoding="utf-8")
    return int(raw[raw.rfind(")") + 2:].split()[19])


def build(
    candidate: Path,
    c41_receipt: Path,
    c41_audit: Path | None,
    output: Path,
    receipt_output: Path,
    invocation_id: str,
    *,
    formal: bool,
) -> dict[str, Any]:
    require(TOKEN.fullmatch(invocation_id) is not None, "InvocationID syntax")
    candidate = workspace_path(candidate, "C41 candidate", must_exist=True)
    c41_receipt = workspace_path(c41_receipt, "C41 receipt", must_exist=True)
    require(c41_audit is not None, "C41 independent audit required in all modes")
    c41_audit = workspace_path(c41_audit, "C41 audit", must_exist=True)
    output = workspace_path(output, "C42 output", must_exist=False)
    receipt_output = workspace_path(
        receipt_output, "C42 receipt", must_exist=False
    )
    require(
        candidate == (ROOT / EXPECTED_C41_CANDIDATE_PATH).resolve()
        and c41_receipt == (ROOT / EXPECTED_C41_RECEIPT_PATH).resolve()
        and c41_audit == (ROOT / EXPECTED_C41_AUDIT_PATH).resolve(),
        "exact pinned C41 candidate/receipt/audit paths",
    )
    pointer_pins = validate_current_c41_pointers()
    stage, receipt_stage = initial_target_preflight(
        candidate, c41_receipt, c41_audit, output, receipt_output
    )
    # The audited C41 gate and all path-envelope checks run before mkdir(stage).
    formal_gate(c41_audit)

    ctx.prec = PRECISION_BITS
    generated = c41.install_complete_immutable_cache()
    require(sum(map(len, generated.values())) == 448,
            "complete immutable chart cache")
    context = load_input(
        candidate, c41_receipt, c41_audit, formal=formal
    )
    authority_target_preflight(
        output, stage, receipt_output, context
    )
    config = context["config"]
    interior_rows, reflection_rows = build_interior(config)
    require(
        len(interior_rows) == 4
        and sum(row["orientation"] == "REPRESENTATIVE"
                for row in interior_rows) == 2
        and sum(row["orientation"] == "REFLECTED"
                for row in interior_rows) == 2,
        "four closed interior certificates",
    )
    face_rows = exact_face_rows(context, config)
    corner_rows = exact_corner_rows(context, config)
    conservation_rows, conservation_census = parent_rows(context["parents"])
    exact_source = source_row(
        context, candidate, c41_receipt, formal
    )

    stage.mkdir(mode=0o755)
    fsync_directory(CANDIDATE_ROOT)
    writers: dict[str, Any] = {}
    try:
        with ExitStack() as stack:
            for key, filename, order in (
                ("source", "exact_source.jsonl.gz", "SINGLE_EXACT_SOURCE"),
                ("interior", "interior_certificates.jsonl.gz",
                 "ORIENTATION_THEN_CERTIFICATE_ORDINAL"),
                ("face", "face_owner_incidence.jsonl.gz", "FACE_ENUM_ORDER"),
                ("corner", "corner_owner_incidence.jsonl.gz", "CORNER_ENUM_ORDER"),
                ("reflection", "reflection_transport.jsonl.gz",
                 "REPRESENTATIVE_HALF_ORDINAL"),
                ("parent", "parent_conservation.jsonl.gz",
                 "PAIR_INDEX_ASCENDING"),
            ):
                writers[key] = stack.enter_context(
                    c41.LedgerWriter(stage / filename, order)
                )
            writers["source"].write(exact_source)
            for row in interior_rows:
                writers["interior"].write(row)
            for row in face_rows:
                writers["face"].write(row)
            for row in corner_rows:
                writers["corner"].write(row)
            for row in reflection_rows:
                semantic = copy.deepcopy(row)
                semantic["reflection_transport_id"] = (
                    "c42-reflection:" + digest(semantic)
                )
                writers["reflection"].write(semantic)
            for row in conservation_rows:
                writers["parent"].write(row)

        lock_mode = (
            "formal producer pass pending an independent C42 audit"
            if formal else "review candidate pending an independent C42 audit"
        )
        (stage / "C42_SINGLETON_CLOSURE.lock").write_text(
            "C42 is a non-authority " + lock_mode + ". The independently audited "
            "C41 object is pinned as input. This producer materializes the exact "
            "P391 closed-box proof, four faces, four corners, reflection pair and "
            "862-parent conservation ledger, but it cannot mint C42 authority or "
            "install an authority pointer. D02 remains blocked by 1150 complete "
            "R1648 continuations; D03, D04, Gate5 promotion and any CM2 claim "
            "remain unauthorized.\n",
            encoding="utf-8",
        )
        ledger_descriptors = {
            "exact_source": writers["source"].descriptor(),
            "interior_certificates": writers["interior"].descriptor(),
            "face_owner_incidence": writers["face"].descriptor(),
            "corner_owner_incidence": writers["corner"].descriptor(),
            "reflection_transport": writers["reflection"].descriptor(),
            "parent_conservation": writers["parent"].descriptor(),
        }
        result: dict[str, Any] = {
            "schema": SCHEMA,
            "status": (
                "REVIEW_CANDIDATE_C42_P391_SINGLE_PARENT_WALL_ENDPOINT_"
                "OWNER_CLOSURE__1_REPRESENTATIVE__2_PAIRED__"
                "1150_UNRESOLVED__C41_AUDIT_BOUND__"
                "C42_INDEPENDENT_AUDIT_PENDING"
                if not formal else
                "FORMAL_PRODUCER_PASS_C42_P391_OWNER_CLOSURE__"
                "PENDING_INDEPENDENT_C42_AUDIT"
            ),
            "review_only": not formal,
            "formal_producer_run": formal,
            "producer_output_is_authority": False,
            "formal_authority": False,
            "authority_pointer_installed": False,
            "independent_C42_audit_outstanding": True,
            "nonpromotion_lock": {
                "filename": "C42_SINGLETON_CLOSURE.lock",
                "sha256": file_sha256(
                    stage / "C42_SINGLETON_CLOSURE.lock"
                ),
                "size": (
                    stage / "C42_SINGLETON_CLOSURE.lock"
                ).stat().st_size,
                "producer_mode_semantic": lock_mode,
                "producer_output_is_authority": False,
            },
            "C41_audited_input": {
                "path": str(candidate.relative_to(ROOT)),
                "object_sha256": EXPECTED_C41_OBJECT,
                "receipt_path": str(c41_receipt.relative_to(ROOT)),
                "receipt_object_sha256": EXPECTED_C41_RECEIPT_OBJECT,
                "independent_audit_path": EXPECTED_C41_AUDIT_PATH,
                "independent_audit_object_sha256": context["audit"][
                    "object_sha256"
                ],
                "independent_audit_status": context["audit"]["status"],
                "independent_auditor_source_sha256": (
                    EXPECTED_C41_AUDITOR_SOURCE
                ),
                "installed_pointer_sha256": pointer_pins,
                "C41_authority_pointers_installed": True,
            },
            "numeric_certificate": {
                "source_sha256": context["pins"],
                "flint_version": flint.__version__,
                "precision_bits": PRECISION_BITS,
                "official_registry_sha256": (
                    c41.EXPECTED_OFFICIAL_REGISTRY_SHA256
                ),
                "full_chart_candidate_count": 448,
                "candidate_cache_immutable": True,
                "exact_split_axis": "p",
                "exact_split_midpoint": qstr(MID_P),
                "representative_closed_half_count": 2,
                "reflected_closed_half_count": 2,
                "all_closed_halves_LOCAL_EXACT_KEY": True,
                "all_closed_halves_strict_owner_mismatch": True,
                "all_closed_halves_integer_wall_endpoint_free": True,
                "original_C41_WALL_ENDPOINT_is_interval_dependency_artifact": True,
            },
            "closure_census": {
                "source_row_count": 1,
                "closed_interior_certificate_count": 4,
                "representative_closed_interior_certificate_count": 2,
                "reflected_closed_interior_certificate_count": 2,
                "face_owner_incidence_count": len(face_rows),
                "corner_owner_incidence_count": len(corner_rows),
                "reflection_transport_count": len(reflection_rows),
                "parent_conservation_row_count": len(conservation_rows),
                "newly_whole_terminal_representative_parent_count": 1,
                "newly_whole_terminal_paired_coarse_cell_count": 2,
                "representative_terminal_gain": qstr(TARGET_FRACTION),
                "all_face_owners_terminal_after_C42": True,
                "all_corner_owners_terminal_after_C42": True,
                "all_corner_incidents_terminal_after_C42": True,
                **conservation_census,
            },
            "ledgers": ledger_descriptors,
            "round144_terminal_census": {
                "CONNECTED_TO_KNOWN": 0,
                "EARLIEST_PREFIX_EXCLUDED": 75_386,
                "SOURCE_GRAZING_OR_CEMETERY": 0,
                "TYPED_EVENT_GRAPH": 296,
                "UNRESOLVED_R1648_CONTINUATION": 1_150,
                "terminal_total": 76_832,
                "unresolved_zero": False,
            },
            "strict_nonpromotion": {
                "review_candidate_is_authority": False,
                "formal_producer_pass_is_authority": False,
                "producer_can_mint_C42_authority": False,
                "authority_pointer_installed": False,
                "C41_independent_audit_complete": True,
                "C42_independent_audit_outstanding": True,
                "D02": "BLOCKED_BY_1150_COMPLETE_R1648_CONTINUATIONS",
                "D03": "UNAUTHORIZED",
                "D04": "NOT_MINTED",
                "Gate5": "10/18",
                "complete_global_18_field_blocks": 0,
                "CM2": "NO-GO_FOR_CLAIM",
            },
            "execution_receipt_policy": (
                "out-of-band self-hashed receipt binds InvocationID/PID, source "
                "SHA, candidate object and root manifest through O_EXCL, fsync "
                "and atomic no-replace publication; no producer receipt carries "
                "authority"
            ),
            "required_next": (
                "independently audit this C42 formal producer object; only a "
                "separate audited installation transaction may mint/install C42 "
                "authority; continue the remaining 575 representative unresolved "
                "continuations afterward"
            ),
        }
        result["object_sha256"] = digest(result)
        write_json(stage / "result.json", result)
        write_manifest(stage)
        validate_manifest(stage)
        replay = strict_json(stage / "result.json")
        validate_self_object(replay, "object_sha256", "C42 candidate")
        require(replay == result, "C42 result byte replay")
        for path in sorted(stage.iterdir()):
            fsync_file(path)
        fsync_directory(stage)
        receipt = {
            "schema": RECEIPT_SCHEMA,
            "status": (
                "REVIEW_PRODUCER_RECEIPT_BOUND_TO_C42_CANDIDATE__"
                "PENDING_INDEPENDENT_C42_AUDIT__NO_AUTHORITY"
                if not formal else
                "FORMAL_PRODUCER_PASS_C42_RECEIPT__"
                "PENDING_INDEPENDENT_C42_AUDIT__NO_AUTHORITY"
            ),
            "mode": (
                "REVIEW_PRODUCER_PENDING_INDEPENDENT_C42_AUDIT"
                if not formal else
                "FORMAL_PRODUCER_PASS_PENDING_INDEPENDENT_C42_AUDIT"
            ),
            "InvocationID": invocation_id,
            "producer_pid": os.getpid(),
            "producer_parent_pid": os.getppid(),
            "producer_proc_start_ticks": proc_start_ticks(os.getpid()),
            "producer_executable": sys.executable,
            "producer_source_sha256": file_sha256(Path(__file__).resolve()),
            "candidate_path": str(output.relative_to(ROOT)),
            "candidate_object_sha256": result["object_sha256"],
            "candidate_inventory_count": len(INVENTORY),
            "root_manifest_sha256": file_sha256(
                stage / "root_manifest.sha256"
            ),
            "C41_candidate_object_sha256": EXPECTED_C41_OBJECT,
            "C41_independent_audit_path": EXPECTED_C41_AUDIT_PATH,
            "C41_independent_audit_object_sha256": context["audit"][
                "object_sha256"
            ],
            "C41_independent_audit_status": context["audit"]["status"],
            "formal_producer_run": formal,
            "producer_output_is_authority": False,
            "formal_authority": False,
            "independent_C42_audit_outstanding": True,
            "authority_pointer_installed": False,
        }
        receipt["receipt_object_sha256"] = digest(receipt)
        publish_candidate_and_receipt(
            stage,
            output,
            receipt_output,
            canonical(receipt) + b"\n",
        )
        try:
            validate_published_candidate(output, result)
            validate_published_receipt(receipt_output, receipt)
            require(
                file_sha256(output / "root_manifest.sha256")
                == receipt["root_manifest_sha256"],
                "published candidate/receipt manifest binding",
            )
        except Exception:
            rollback_publication(
                output,
                receipt_output,
                receipt_stage,
                output_created=True,
                receipt_parent_created=True,
                receipt_stage_created=False,
                receipt_final_created=True,
            )
            raise
        return result
    except Exception:
        if stage.exists():
            shutil.rmtree(stage)
            fsync_directory(CANDIDATE_ROOT)
        raise


def expect_rejection(function: Any, label: str) -> str:
    try:
        function()
    except (C42Error, OSError):
        return label
    raise C42Error("regression unexpectedly accepted:" + label)


def remove_regression_path(path: Path, root: Path) -> None:
    if path.is_symlink() or (path.exists() and not path.is_dir()):
        path.unlink()
    elif path.exists():
        shutil.rmtree(path)
    fsync_directory(root)


def prewrite_and_orphan_regressions() -> dict[str, Any]:
    candidate = (ROOT / EXPECTED_C41_CANDIDATE_PATH).resolve()
    c41_receipt = (ROOT / EXPECTED_C41_RECEIPT_PATH).resolve()
    c41_audit = (ROOT / EXPECTED_C41_AUDIT_PATH).resolve()
    base = (
        f"c42-hardening-regression-{os.getpid()}-"
        f"{proc_start_ticks(os.getpid())}"
    )
    prewrite: list[str] = []
    orphan: list[str] = []
    cleanup_candidates: list[Path] = []
    cleanup_audits: list[Path] = []
    try:
        valid_output = CANDIDATE_ROOT / (base + "-valid")
        valid_receipt = (
            AUDIT_ROOT / valid_output.name / "execution_receipt.json"
        )
        initial_target_preflight(
            candidate, c41_receipt, c41_audit,
            valid_output, valid_receipt,
        )
        prewrite.append("VALID_DIRECT_CHILD_ENVELOPE_ACCEPTED")
        prewrite.append(expect_rejection(
            lambda: initial_target_preflight(
                candidate, c41_receipt, c41_audit,
                RUNTIME / (base + "-outside-candidates"), valid_receipt,
            ),
            "OUTPUT_OUTSIDE_CANDIDATE_ROOT_REJECTED",
        ))
        prewrite.append(expect_rejection(
            lambda: initial_target_preflight(
                candidate, c41_receipt, c41_audit,
                valid_output,
                RUNTIME / (base + "-outside-audit")
                / "execution_receipt.json",
            ),
            "RECEIPT_OUTSIDE_AUDIT_ROOT_REJECTED",
        ))
        prewrite.append(expect_rejection(
            lambda: initial_target_preflight(
                candidate, c41_receipt, c41_audit,
                valid_output,
                AUDIT_ROOT / (base + "-different-token")
                / "execution_receipt.json",
            ),
            "OUTPUT_RECEIPT_TOKEN_MISMATCH_REJECTED",
        ))
        prewrite.append(expect_rejection(
            lambda: initial_target_preflight(
                candidate, c41_receipt, c41_audit,
                candidate,
                AUDIT_ROOT / candidate.name / "execution_receipt.json",
            ),
            "PREEXISTING_INPUT_CANDIDATE_OUTPUT_REJECTED",
        ))

        alias = CANDIDATE_ROOT / (base + "-symlink-alias")
        cleanup_candidates.append(alias)
        alias.symlink_to(candidate, target_is_directory=True)
        fsync_directory(CANDIDATE_ROOT)
        prewrite.append(expect_rejection(
            lambda: workspace_path(alias, "symlink alias", must_exist=True),
            "SYMLINK_ALIAS_INPUT_REJECTED",
        ))
        alias.unlink()
        fsync_directory(CANDIDATE_ROOT)
        cleanup_candidates.remove(alias)

        symlink_output = CANDIDATE_ROOT / (base + "-receipt-symlink")
        symlink_parent = AUDIT_ROOT / symlink_output.name
        cleanup_audits.append(symlink_parent)
        symlink_parent.mkdir(mode=0o755)
        (symlink_parent / "execution_receipt.json").symlink_to(c41_receipt)
        fsync_directory(symlink_parent)
        fsync_directory(AUDIT_ROOT)
        prewrite.append(expect_rejection(
            lambda: initial_target_preflight(
                candidate, c41_receipt, c41_audit,
                symlink_output,
                symlink_parent / "execution_receipt.json",
            ),
            "PREEXISTING_RECEIPT_SYMLINK_REJECTED",
        ))
        remove_regression_path(symlink_parent, AUDIT_ROOT)
        cleanup_audits.remove(symlink_parent)

        collision_output = CANDIDATE_ROOT / (base + "-noreplace")
        collision_stage = CANDIDATE_ROOT / (
            collision_output.name + ".stage-regression"
        )
        cleanup_candidates.extend((collision_output, collision_stage))
        collision_output.mkdir(mode=0o755)
        collision_stage.mkdir(mode=0o755)
        (collision_output / "sentinel").write_bytes(b"preexisting\n")
        (collision_stage / "candidate").write_bytes(b"new\n")
        try:
            rename_noreplace(collision_stage, collision_output)
        except OSError as error:
            require(error.errno == errno.EEXIST, "rename no-replace EEXIST")
            prewrite.append("CANDIDATE_RENAME_NOREPLACE_COLLISION_REJECTED")
        else:
            raise C42Error("candidate rename overwrote preexisting output")
        require(
            (collision_output / "sentinel").read_bytes() == b"preexisting\n"
            and (collision_stage / "candidate").read_bytes() == b"new\n",
            "no-replace collision preserves both trees",
        )
        remove_regression_path(collision_stage, CANDIDATE_ROOT)
        remove_regression_path(collision_output, CANDIDATE_ROOT)
        cleanup_candidates = [
            path for path in cleanup_candidates
            if path not in {collision_output, collision_stage}
        ]

        for index, phase in enumerate((
            "AFTER_OUTPUT_RENAME",
            "AFTER_RECEIPT_PARENT_CREATE",
            "AFTER_RECEIPT_STAGE_WRITE",
            "AFTER_RECEIPT_FINAL_RENAME",
        )):
            output = CANDIDATE_ROOT / f"{base}-orphan-{index}"
            receipt = AUDIT_ROOT / output.name / "execution_receipt.json"
            stage = output.with_name(output.name + f".stage-{os.getpid()}")
            cleanup_candidates.extend((output, stage))
            cleanup_audits.append(receipt.parent)
            initial_target_preflight(
                candidate, c41_receipt, c41_audit, output, receipt
            )
            stage.mkdir(mode=0o755)
            (stage / "dummy").write_bytes(b"candidate\n")
            fsync_file(stage / "dummy")
            fsync_directory(stage)
            fsync_directory(CANDIDATE_ROOT)
            orphan.append(expect_rejection(
                lambda phase=phase, stage=stage, output=output, receipt=receipt:
                    publish_candidate_and_receipt(
                        stage, output, receipt, b"{}\n",
                        inject_failure=phase,
                    ),
                phase + "_CLEANUP_TRIGGERED",
            ))
            require(
                not stage.exists()
                and not output.exists()
                and not receipt.exists()
                and not receipt.parent.exists(),
                "zero orphan after injected failure:" + phase,
            )
            cleanup_candidates = [
                path for path in cleanup_candidates
                if path not in {output, stage}
            ]
            cleanup_audits.remove(receipt.parent)
    finally:
        for path in cleanup_candidates:
            if path.exists() or path.is_symlink():
                remove_regression_path(path, CANDIDATE_ROOT)
        for path in cleanup_audits:
            if path.exists() or path.is_symlink():
                remove_regression_path(path, AUDIT_ROOT)
    return {
        "prewrite_case_count": len(prewrite),
        "prewrite_cases": prewrite,
        "injected_orphan_case_count": len(orphan),
        "injected_orphan_cases": orphan,
        "orphan_candidate_count_after_cleanup": 0,
        "orphan_receipt_count_after_cleanup": 0,
    }


def self_test() -> dict[str, Any]:
    pins = source_pins()
    require(
        HEX64.fullmatch(EXPECTED_C41_AUDIT_OBJECT) is not None
        and EXPECTED_C41_AUDIT_STATUS.startswith("PASS_"),
        "formal C41 audit pins ready",
    )
    audit = formal_gate((ROOT / EXPECTED_C41_AUDIT_PATH).resolve())
    pointers = validate_current_c41_pointers()
    hardening = prewrite_and_orphan_regressions()
    ctx.prec = PRECISION_BITS
    generated = c41.install_complete_immutable_cache()
    require(sum(map(len, generated.values())) == 448,
            "C42 self-test chart cache")
    return {
        "status": (
            "PASS_C42_HARDENED_SELF_TEST__C41_AUDIT_BOUND__"
            "PREWRITE_AND_ORPHAN_REGRESSIONS_PASS"
        ),
        "source_sha256": pins,
        "formal_gate_ready": True,
        "C41_independent_audit_object_sha256": audit["object_sha256"],
        "C41_independent_audit_status": audit["status"],
        "installed_C41_pointer_sha256": pointers,
        "hardening_regressions": hardening,
        "pair_index": PAIR_INDEX,
        "target_path": TARGET_PATH,
        "exact_split_midpoint": qstr(MID_P),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--c41-candidate", type=Path)
    parser.add_argument("--c41-receipt", type=Path)
    parser.add_argument("--c41-audit", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--receipt", type=Path)
    parser.add_argument("--invocation-id")
    parser.add_argument("--review-candidate", action="store_true")
    parser.add_argument("--formal", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    arguments = parser.parse_args()
    if arguments.self_test:
        print(canonical(self_test()).decode("utf-8"))
        return 0
    require(arguments.review_candidate != arguments.formal,
            "choose exactly one of --review-candidate/--formal")
    require(
        arguments.c41_candidate is not None
        and arguments.c41_receipt is not None
        and arguments.c41_audit is not None
        and arguments.output is not None
        and arguments.receipt is not None
        and arguments.invocation_id is not None,
        "candidate/receipt/output/InvocationID arguments",
    )
    result = build(
        arguments.c41_candidate,
        arguments.c41_receipt,
        arguments.c41_audit,
        arguments.output,
        arguments.receipt,
        arguments.invocation_id,
        formal=arguments.formal,
    )
    print(canonical({
        "status": result["status"],
        "object_sha256": result["object_sha256"],
        "formal_authority": result["formal_authority"],
        "authority_pointer_installed": False,
    }).decode("utf-8"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
