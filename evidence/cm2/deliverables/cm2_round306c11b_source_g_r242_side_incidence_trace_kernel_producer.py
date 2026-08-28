#!/usr/bin/env python3
"""Produce the scoped R242 graph-side incidence and one-sided trace kernel.

The scope is exactly 264 sealed R242 positive graph patches and their 528
owner/shadow open-side relations.  This producer gives only direct local
graph-side physical-incidence and one-sided common-boundary trace credit.  It
does not prove graph-to-sheet set equality, representation pullback, member or
global normalized support, a new DSU edge/union, B1A, B2, maximality, or CM2.
"""

from __future__ import annotations

import argparse
from collections import Counter
from dataclasses import dataclass
from fractions import Fraction as Q
import gzip
import hashlib
import io
import json
import os
from pathlib import Path
import stat
import sys
from typing import Any, Final, Iterator


class Rejected(RuntimeError):
    pass


def need(condition: bool, label: str) -> None:
    if type(condition) is not bool or not condition:
        raise Rejected(label)


ROOT: Final = Path(__file__).parent
PREFIX: Final = "cm2_round306c11b_source_g_r242_side_incidence_trace_kernel"
SCHEMA: Final = "cm2.round306c11b.source-g-r242-side-incidence-trace-kernel.v1"
INTERFACE_ROW_SCHEMA: Final = SCHEMA + ".interface-kernel-row.v1"
RELATION_ROW_SCHEMA: Final = SCHEMA + ".relation-theorem-row.v1"
INTERFACE_LEDGER_NAME: Final = PREFIX + "_interface_kernel_ledger.jsonl.gz"
RELATION_LEDGER_NAME: Final = PREFIX + "_relation_theorem_ledger.jsonl.gz"
RESULT_NAME: Final = PREFIX + "_result.json"
STATUS: Final = (
    "PASS_264_R242_INTERFACE_KERNELS__"
    "528_DIRECT_LOCAL_GRAPH_SIDE_INCIDENCES__"
    "528_ONE_SIDED_COMMON_BOUNDARY_TRACES__"
    "ZERO_PULLBACK_NORMALIZED_SUPPORT_DSU_B1A_B2_MAXIMALITY_CM2_CREDIT"
)

C10_MANIFEST: Final = "cm2_round306c10_source_g_exact_graph_support_identity_rematerialization_manifest.sha256"
C10_RESULT: Final = "cm2_round306c10_source_g_exact_graph_support_identity_rematerialization_result.json"
C10_SUPPORT: Final = "cm2_round306c10_source_g_exact_graph_support_identity_rematerialization_exact_graph_support_ledger.jsonl.gz"
C10_IDENTITY: Final = "cm2_round306c10_source_g_exact_graph_support_identity_rematerialization_member_identity_disposition_ledger.jsonl.gz"
C11_MANIFEST: Final = "cm2_round306c11_source_g_graph_side_local_theorem_disposition_manifest.sha256"
C11_RESULT: Final = "cm2_round306c11_source_g_graph_side_local_theorem_disposition_result.json"
C11_DISPOSITION: Final = "cm2_round306c11_source_g_graph_side_local_theorem_disposition_disposition_ledger.jsonl.gz"
R242_MANIFEST: Final = "cm2_round242_source_g_outgoing_graph_existence_stratum_materialization_manifest.sha256"
R242_CERT: Final = "cm2_round242_source_g_outgoing_graph_existence_stratum_materialization_certificate.json"
R245_MANIFEST: Final = "cm2_round245_source_g_retained_graph_mixed_sheet_quotient_manifest.sha256"
R245_CERT: Final = "cm2_round245_source_g_retained_graph_mixed_sheet_quotient_certificate.json"


@dataclass(frozen=True)
class Pin:
    role: str
    filename: str
    size: int
    sha256: str


# C10 is intentionally fail-closed until its newly built bytes are sealed.
# The three pending zero sizes/impossible digests must be patched before use.
PINS: Final = (
    Pin("C10_MANIFEST", C10_MANIFEST, 1_431, "b7277863feb9edc5f35906b04af2a9a256becb7ee9f1f1df6558b897184029ca"),
    Pin("C10_RESULT", C10_RESULT, 9_468, "b188eaa6c4dee77e0fff13b4a48cec9f8b46d324e48e7927265807a0f2865b55"),
    Pin("C10_SUPPORT", C10_SUPPORT, 19_958_893, "b7b2b02653a404060364b788b3e0ac8693d2d9d8d1c45e6109ca7f4400c4080c"),
    Pin("C10_IDENTITY", C10_IDENTITY, 2_966_603, "5041df1ab4b5bf9e79984859f828c9fb69718f53bd62d2920d51ebea8b7ec9df"),
    Pin("C11_MANIFEST", C11_MANIFEST, 1_652, "b087b80d90bc524af29ccbc0dc80ea82f157ae491404f64de342bb10c16d5d73"),
    Pin("C11_RESULT", C11_RESULT, 12_545, "083103ac958dfcb01283850abcda03fcdce26a8910c42b79c570a87486925506"),
    Pin("C11_DISPOSITION", C11_DISPOSITION, 10_888_167, "b1af6336b83842f2c6380929977f6d3591cfb50a1b305c7eafd197931d623543"),
    Pin("R242_MANIFEST", R242_MANIFEST, 897, "6da30fe3f9438ec73dc9c7d1aac770d8e9730aa9564ab0c535f1596cdc09ef2f"),
    Pin("R242_CERT", R242_CERT, 13_734_655, "8d32c381e21c03aad6a531b7e5a527d295783b7e3e38baa1e6bcba20c40db22e"),
    Pin("R245_MANIFEST", R245_MANIFEST, 897, "1aff29f3a42b618ca85e5a1d3c537307e32326f8d5092b82d4253a5bf6e1c4ac"),
    Pin("R245_CERT", R245_CERT, 20_683_081, "c76662f7cb068127f3612a3655ae720662eead9b9210b5757d771693149883c1"),
)
PIN_BY_ROLE: Final = {pin.role: pin for pin in PINS}

ZERO_DOWNSTREAM: Final = {
    "graph_sheet_set_equality": 0,
    "representation_pullback": 0,
    "member_normalized_support": 0,
    "global_normalized_support": 0,
    "A1_A2": 0,
    "transition": 0,
    "DSU_edge": 0,
    "DSU_union": 0,
    "B1A": 0,
    "B2": 0,
    "maximality": 0,
    "fibre": 0,
    "global_disposition": 0,
    "CM2": 0,
}


def canonical(value: Any) -> bytes:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
        allow_nan=False,
    ).encode("ascii")


def object_sha(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def identity(info: os.stat_result) -> tuple[int, ...]:
    return (
        info.st_dev,
        info.st_ino,
        info.st_mode,
        info.st_nlink,
        info.st_size,
        info.st_mtime_ns,
        info.st_ctime_ns,
    )


def hash_fd(file_descriptor: int) -> str:
    os.lseek(file_descriptor, 0, os.SEEK_SET)
    digest = hashlib.sha256()
    while True:
        block = os.read(file_descriptor, 1_048_576)
        if not block:
            return digest.hexdigest()
        digest.update(block)


def read_fd(file_descriptor: int) -> bytes:
    os.lseek(file_descriptor, 0, os.SEEK_SET)
    blocks: list[bytes] = []
    while True:
        block = os.read(file_descriptor, 1_048_576)
        if not block:
            return b"".join(blocks)
        blocks.append(block)


class Snapshot:
    def __init__(self) -> None:
        self.directory_descriptor = -1
        self.file_descriptors: dict[str, int] = {}
        self.identities: dict[str, tuple[int, ...]] = {}

    def __enter__(self) -> "Snapshot":
        before = os.stat(ROOT, follow_symlinks=False)
        need(stat.S_ISDIR(before.st_mode) and not ROOT.is_symlink(), "deliverables directory")
        self.directory_descriptor = os.open(
            ROOT,
            os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW | os.O_CLOEXEC,
        )
        for pin in PINS:
            info = os.stat(pin.filename, dir_fd=self.directory_descriptor, follow_symlinks=False)
            need(
                stat.S_ISREG(info.st_mode)
                and info.st_nlink == 1
                and info.st_size == pin.size,
                "pin identity:" + pin.role,
            )
            descriptor = os.open(
                pin.filename,
                os.O_RDONLY | os.O_NOFOLLOW | os.O_CLOEXEC,
                dir_fd=self.directory_descriptor,
            )
            opened = os.fstat(descriptor)
            need(identity(opened) == identity(info), "pin race:" + pin.role)
            need(hash_fd(descriptor) == hash_fd(descriptor) == pin.sha256, "pin digest:" + pin.role)
            self.file_descriptors[pin.role] = descriptor
            self.identities[pin.role] = identity(opened)
        return self

    def read(self, role: str) -> bytes:
        return read_fd(self.file_descriptors[role])

    def duplicate(self, role: str) -> int:
        descriptor = os.dup(self.file_descriptors[role])
        os.lseek(descriptor, 0, os.SEEK_SET)
        return descriptor

    def final(self) -> None:
        for pin in reversed(PINS):
            descriptor = self.file_descriptors[pin.role]
            need(identity(os.fstat(descriptor)) == self.identities[pin.role], "final fd:" + pin.role)
            need(
                identity(os.stat(pin.filename, dir_fd=self.directory_descriptor, follow_symlinks=False))
                == self.identities[pin.role],
                "final path:" + pin.role,
            )
            need(hash_fd(descriptor) == pin.sha256, "final digest:" + pin.role)

    def __exit__(self, *_: Any) -> None:
        for descriptor in self.file_descriptors.values():
            try:
                os.close(descriptor)
            except OSError:
                pass
        if self.directory_descriptor >= 0:
            os.close(self.directory_descriptor)


def parse_manifest(raw: bytes, label: str) -> dict[str, str]:
    need(raw.endswith(b"\n"), "manifest newline:" + label)
    records: dict[str, str] = {}
    for line in raw.decode("ascii").splitlines():
        parts = line.split("  ")
        need(len(parts) == 2 and len(parts[0]) == 64, "manifest line:" + label)
        int(parts[0], 16)
        name = Path(parts[1]).name
        need(
            parts[1] in {name, "deliverables/" + name}
            and name not in records,
            "manifest name:" + label,
        )
        records[name] = parts[0]
    return records


def bind_manifest(snapshot: Snapshot, manifest_role: str, member_roles: tuple[str, ...]) -> None:
    records = parse_manifest(snapshot.read(manifest_role), manifest_role)
    for role in member_roles:
        pin = PIN_BY_ROLE[role]
        need(records.get(pin.filename) == pin.sha256, "manifest member:" + manifest_role + ":" + role)


def closed_document(snapshot: Snapshot, role: str) -> dict[str, Any]:
    raw = snapshot.read(role)
    value = json.loads(raw)
    need(type(value) is dict and raw in {canonical(value), canonical(value) + b"\n"}, "canonical document:" + role)
    core = dict(value)
    claimed = core.pop("result_sha256", None)
    need(type(claimed) is str and claimed == object_sha(core), "document closure:" + role)
    return value


def legacy_document(snapshot: Snapshot, role: str) -> dict[str, Any]:
    value = json.loads(snapshot.read(role))
    need(type(value) is dict and set(value) == {"schema", "result", "result_sha256"}, "legacy envelope:" + role)
    need(value["result_sha256"] == object_sha(value["result"]), "legacy closure:" + role)
    return value


def jsonl_rows(snapshot: Snapshot, role: str) -> Iterator[dict[str, Any]]:
    duplicate = snapshot.duplicate(role)
    try:
        with os.fdopen(duplicate, "rb", closefd=True) as raw, gzip.GzipFile(fileobj=raw, mode="rb") as stream:
            for ordinal, line in enumerate(stream):
                row = json.loads(line)
                need(
                    type(row) is dict
                    and line.endswith(b"\n")
                    and line == canonical(row) + b"\n",
                    "canonical JSONL:" + role + ":" + str(ordinal),
                )
                validate_closed_row(row, role + ":" + str(ordinal))
                yield row
    finally:
        try:
            os.close(duplicate)
        except OSError:
            pass


def validate_closed_row(row: dict[str, Any], label: str) -> None:
    core = dict(row)
    claimed = core.pop("row_sha256", None)
    need(type(claimed) is str and claimed == object_sha(core), "row closure:" + label)


def producer_record() -> dict[str, Any]:
    info = os.stat(__file__, follow_symlinks=False)
    need(stat.S_ISREG(info.st_mode) and info.st_nlink == 1, "producer identity")
    descriptor = os.open(__file__, os.O_RDONLY | os.O_NOFOLLOW | os.O_CLOEXEC)
    try:
        opened = os.fstat(descriptor)
        need(identity(opened) == identity(info), "producer race")
        digest = hash_fd(descriptor)
        need(digest == hash_fd(descriptor), "producer two-pass digest")
        return {"filename": Path(__file__).name, "size": info.st_size, "sha256": digest}
    finally:
        os.close(descriptor)


def qstr(value: Q | int | str) -> str:
    rational = Q(value)
    return str(rational.numerator) if rational.denominator == 1 else f"{rational.numerator}/{rational.denominator}"


def positive_box(box: list[str], dimension: int, label: str) -> Q:
    need(type(box) is list and len(box) == 2 * dimension, "box shape:" + label)
    result = Q(1)
    for axis in range(dimension):
        lower = Q(box[2 * axis])
        upper = Q(box[2 * axis + 1])
        need(qstr(lower) == box[2 * axis] and qstr(upper) == box[2 * axis + 1] and lower < upper, "box axis:" + label)
        result *= upper - lower
    return result


def row_ref(row: dict[str, Any], id_field: str = "row_id") -> dict[str, str]:
    return {"row_id": row[id_field], "row_sha256": row["row_sha256"]}


def closed_row(core: dict[str, Any]) -> dict[str, Any]:
    return {**core, "row_sha256": object_sha(core)}


def rational_ast(value: Q | int | str) -> dict[str, Any]:
    return {"op": "RATIONAL_CONSTANT", "value": qstr(value)}


def closed_interval_ast(coordinate: str, lower: str, upper: str) -> dict[str, Any]:
    need(coordinate in {"t", "p", "s"} and Q(lower) < Q(upper), "closed interval AST")
    return {
        "op": "CLOSED_INTERVAL",
        "coordinate": coordinate,
        "lower": qstr(lower),
        "upper": qstr(upper),
    }


def box_ast(box: list[str]) -> dict[str, Any]:
    need(positive_box(box, 3, "AST box") > 0, "positive AST box")
    return {
        "op": "AND",
        "args": [
            closed_interval_ast("t", box[0], box[1]),
            closed_interval_ast("p", box[2], box[3]),
            closed_interval_ast("s", box[4], box[5]),
        ],
    }


def and_ast(*arguments: dict[str, Any]) -> dict[str, Any]:
    return {"op": "AND", "args": list(arguments)}


def relation_ast(sign: str, factor: dict[str, Any]) -> dict[str, Any]:
    need(sign in {"STRICT_NEGATIVE", "STRICT_POSITIVE"}, "factor sign")
    return {
        "op": "LT" if sign == "STRICT_NEGATIVE" else "GT",
        "left": factor,
        "right": rational_ast(0),
    }


def validate_primitive_ast(value: Any, label: str) -> None:
    need(type(value) is dict and type(value.get("op")) is str, "AST node:" + label)
    operation = value["op"]
    if operation == "RATIONAL_CONSTANT":
        need(set(value) == {"op", "value"} and type(value["value"]) is str, "AST rational:" + label)
        need(qstr(value["value"]) == value["value"], "AST reduced rational:" + label)
        return
    if operation == "COORDINATE":
        need(set(value) == {"op", "name"} and value["name"] in {"t", "p", "s"}, "AST coordinate:" + label)
        return
    if operation in {"ADD", "MUL", "AND"}:
        need(
            set(value) == {"op", "args"}
            and type(value["args"]) is list
            and len(value["args"]) > 0,
            "AST nary:" + label,
        )
        for ordinal, argument in enumerate(value["args"]):
            validate_primitive_ast(argument, label + ":" + str(ordinal))
        return
    if operation in {"NEG", "SQUARE"}:
        need(set(value) == {"op", "arg"}, "AST unary:" + label)
        validate_primitive_ast(value["arg"], label + ":arg")
        return
    if operation == "SQRT_PRINCIPAL_NONNEGATIVE":
        need(set(value) == {"op", "radicand"}, "AST sqrt:" + label)
        validate_primitive_ast(value["radicand"], label + ":radicand")
        return
    if operation in {"EQ", "LT", "GT"}:
        need(set(value) == {"op", "left", "right"}, "AST relation:" + label)
        validate_primitive_ast(value["left"], label + ":left")
        validate_primitive_ast(value["right"], label + ":right")
        return
    if operation == "CLOSED_INTERVAL":
        need(
            set(value) == {"op", "coordinate", "lower", "upper"}
            and value["coordinate"] in {"t", "p", "s"}
            and type(value["lower"]) is str
            and type(value["upper"]) is str
            and qstr(value["lower"]) == value["lower"]
            and qstr(value["upper"]) == value["upper"]
            and Q(value["lower"]) <= Q(value["upper"]),
            "AST interval:" + label,
        )
        return
    if operation == "OR_DISJOINT":
        need(
            set(value) == {"op", "cases"}
            and type(value["cases"]) is list
            and len(value["cases"]) > 0,
            "AST cases:" + label,
        )
        for ordinal, case in enumerate(value["cases"]):
            need(type(case) is dict and set(case) == {"case", "predicate"} and type(case["case"]) is str, "AST case:" + label)
            validate_primitive_ast(case["predicate"], label + ":case:" + str(ordinal))
        return
    raise Rejected("unrecognized AST operation:" + label + ":" + operation)


def edge_receipt(edge: dict[str, Any]) -> dict[str, Any]:
    corridor = edge["strict_positive_3D_retained_corridor_box"]
    contact = edge["exact_positive_2D_contact_rectangle"]
    need(positive_box(corridor, 3, "edge corridor") == Q(edge["strict_positive_3D_retained_corridor_volume"]), "edge corridor volume")
    need(positive_box(contact, 2, "edge contact") == Q(edge["exact_positive_2D_contact_area"]), "edge contact area")
    return {
        "row_id": edge["mixed_sheet_edge_id"],
        "row_sha256": edge["row_sha256"],
        "edge_kind": edge["edge_kind"],
        "contact_proof_kind": edge["contact_proof_kind"],
        "left_node_id": edge["left_node_id"],
        "right_node_id": edge["right_node_id"],
        "exact_positive_2D_contact_rectangle": contact,
        "exact_positive_2D_contact_area": edge["exact_positive_2D_contact_area"],
        "strict_positive_3D_retained_corridor_box": corridor,
        "strict_positive_3D_retained_corridor_volume": edge["strict_positive_3D_retained_corridor_volume"],
        "current_quotient_lower_bound_edge_credit": edge["current_quotient_lower_bound_edge_credit"],
    }


def gzip_rows(rows: list[dict[str, Any]]) -> tuple[bytes, bytes]:
    plain = b"".join(canonical(row) + b"\n" for row in rows)
    buffer = io.BytesIO()
    with gzip.GzipFile(filename="", mode="wb", compresslevel=9, fileobj=buffer, mtime=0) as stream:
        stream.write(plain)
    return buffer.getvalue(), plain


def sequence_sha(values: Any) -> str:
    digest = hashlib.sha256()
    for value in values:
        digest.update(canonical(value))
        digest.update(b"\n")
    return digest.hexdigest()


def ledger_descriptor(
    filename: str,
    row_schema: str,
    rows: list[dict[str, Any]],
    wire: bytes,
    plain: bytes,
) -> dict[str, Any]:
    return {
        "filename": filename,
        "compression": "gzip-level9-mtime-zero",
        "row_schema": row_schema,
        "row_count": len(rows),
        "compressed_size": len(wire),
        "compressed_sha256": hashlib.sha256(wire).hexdigest(),
        "uncompressed_size": len(plain),
        "uncompressed_sha256": hashlib.sha256(plain).hexdigest(),
        "ordered_row_ids_sha256": sequence_sha(row["row_id"] for row in rows),
        "ordered_row_hashes_sha256": sequence_sha(row["row_sha256"] for row in rows),
        "ordered_rows_sha256": sequence_sha(rows),
    }


def validate_c10_result(result: dict[str, Any]) -> None:
    need(result["support_census"]["exact_G2_feature_support_AST_rows"] == 5_264, "C10 support census")
    need(result["identity_census"]["member_natural_key_preservation_rows"] == 5_264, "C10 identity census")
    need(
        result["scoped_credit"]
        == {"exact_G2_feature_support_AST": 5_264, "member_natural_key_preservation": 5_264},
        "C10 scoped credit",
    )
    need(all(value == 0 for value in result["formal_credit"].values()), "C10 downstream zero")
    need(result["strict_nonpromotion"]["graph_to_sheet_set_equality_proved"] is False, "C10 set boundary")
    need(result["strict_nonpromotion"]["physical_incidence_proved"] is False, "C10 physical boundary")
    need(result["strict_nonpromotion"]["representation_pullback_proved"] is False, "C10 pullback boundary")


def build() -> tuple[dict[str, Any], bytes, bytes]:
    with Snapshot() as snapshot:
        bind_manifest(snapshot, "C10_MANIFEST", ("C10_RESULT", "C10_SUPPORT", "C10_IDENTITY"))
        bind_manifest(snapshot, "C11_MANIFEST", ("C11_RESULT", "C11_DISPOSITION"))
        bind_manifest(snapshot, "R242_MANIFEST", ("R242_CERT",))
        bind_manifest(snapshot, "R245_MANIFEST", ("R245_CERT",))

        c10_result = closed_document(snapshot, "C10_RESULT")
        validate_c10_result(c10_result)
        c11_result = closed_document(snapshot, "C11_RESULT")
        need(c11_result["disposition_census"]["positive_graph_side_relations"] == 10_118, "C11 relation census")
        need(c11_result["disposition_census"]["CANDIDATE_READY_ROUTING"] == 9_950, "C11 ready census")
        need(c11_result["disposition_census"]["BLOCKED"] == 168, "C11 blocked census")
        need(all(value == 0 for value in c11_result["formal_credit"].values()), "C11 zero credit")

        c11_by_subject: dict[tuple[str, str, str], dict[str, Any]] = {}
        c11_relation_ids: set[str] = set()
        for row in jsonl_rows(snapshot, "C11_DISPOSITION"):
            c9_row_id = row["C9_relation_ref"]["row_id"]
            need(c9_row_id not in c11_relation_ids, "C11 routing relation uniqueness")
            c11_relation_ids.add(c9_row_id)
            key = (row["graph_id"], row["side_role"], row["side_member_id"])
            need(key not in c11_by_subject, "C11 routing subject uniqueness")
            c11_by_subject[key] = row
        need(len(c11_relation_ids) == len(c11_by_subject) == 10_118, "C11 routing exhaustion")

        supports: dict[str, dict[str, Any]] = {}
        total_support_rows = 0
        for row in jsonl_rows(snapshot, "C10_SUPPORT"):
            total_support_rows += 1
            if row["graph_class"] == "R242_UNIQUE_GRAPH_FULL_PATCH":
                need(row["graph_id"] not in supports, "C10 R242 support uniqueness")
                supports[row["graph_id"]] = row
        need(total_support_rows == 5_264 and len(supports) == 264, "C10 R242 support exhaustion")

        identities: dict[str, dict[str, Any]] = {}
        total_identity_rows = 0
        for row in jsonl_rows(snapshot, "C10_IDENTITY"):
            total_identity_rows += 1
            if row["graph_class"] == "R242_UNIQUE_GRAPH_FULL_PATCH":
                need(row["graph_id"] not in identities, "C10 R242 identity uniqueness")
                identities[row["graph_id"]] = row
        need(total_identity_rows == 5_264 and len(identities) == 264, "C10 R242 identity exhaustion")

        r242 = legacy_document(snapshot, "R242_CERT")["result"]
        patch_rows = r242["formal_positive_2D_transition_sheet_patch_ledger"]["rows"]
        root_rows = r242["formal_root_existence_classification_ledger"]["rows"]
        need(len(patch_rows) == 264 and len(root_rows) == 3_136, "R242 census")
        patches: dict[str, dict[str, Any]] = {}
        for row in patch_rows:
            validate_closed_row(row, "R242 patch")
            need(row["transition_sheet_patch_row_id"] not in patches, "R242 patch uniqueness")
            patches[row["transition_sheet_patch_row_id"]] = row
        roots: dict[str, dict[str, Any]] = {}
        for row in root_rows:
            validate_closed_row(row, "R242 root")
            patch_id = row["transition_sheet_patch_row_id"]
            if patch_id is not None:
                need(patch_id not in roots, "R242 positive root uniqueness")
                roots[patch_id] = row
        need(len(roots) == 264 and set(roots) == set(patches), "R242 positive root exhaustion")

        r245 = legacy_document(snapshot, "R245_CERT")["result"]
        node_rows = r245["formal_retained_stratum_node_ledger"]["rows"]
        edge_rows = r245["formal_mixed_sheet_physical_edge_ledger"]["rows"]
        need(len(node_rows) == len(edge_rows) == 3_664, "R245 census")
        nodes_by_interface: dict[str, dict[str, dict[str, Any]]] = {}
        for row in node_rows:
            validate_closed_row(row, "R245 node")
            interface_id = row["Round220_split_interface_id"]
            if interface_id not in {patch["Round220_split_interface_id"] for patch in patch_rows}:
                continue
            by_kind = nodes_by_interface.setdefault(interface_id, {})
            need(row["stratum_kind"] not in by_kind, "R245 selected node-kind uniqueness")
            by_kind[row["stratum_kind"]] = row
        edges_by_interface: dict[str, dict[str, dict[str, Any]]] = {}
        for row in edge_rows:
            validate_closed_row(row, "R245 edge")
            interface_id = row["Round220_split_interface_id"]
            if interface_id not in nodes_by_interface:
                continue
            by_kind = edges_by_interface.setdefault(interface_id, {})
            need(row["edge_kind"] not in by_kind, "R245 selected edge-kind uniqueness")
            by_kind[row["edge_kind"]] = row
        need(len(nodes_by_interface) == len(edges_by_interface) == 264, "R245 selected interface exhaustion")

        interface_rows: list[dict[str, Any]] = []
        relation_rows: list[dict[str, Any]] = []
        edge_kind_census: Counter[str] = Counter()
        role_census: Counter[str] = Counter()
        direction_census: Counter[str] = Counter()
        derivative_census: Counter[str] = Counter()
        resolved_contact_census: Counter[str] = Counter()

        for graph_id, patch in sorted(patches.items()):
            support = supports.get(graph_id)
            identity_row = identities.get(graph_id)
            root = roots[graph_id]
            need(support is not None and identity_row is not None, "C10 graph binding")
            need(
                support["sheet_member_id"] == identity_row["sheet_member_id"]
                and identity_row["recomputed_member_id"] == support["sheet_member_id"]
                and identity_row["exact_support_ref"] == row_ref(support)
                and identity_row["member_natural_key_preservation_credit"] == 1
                and identity_row["identity_prerequisites"]["natural_key_graph_member_pair_bijection"] is True
                and identity_row["set_equality_proved"] is False
                and identity_row["physical_incidence_proved"] is False
                and identity_row["identity_representation_pullback_proved"] is False,
                "C10 identity boundary",
            )
            need(
                support["scoped_credit"] == {"exact_G2_feature_support_AST": 1, "member_natural_key_preservation": 0}
                and support["support_properties"]["nonempty"] is True
                and support["support_properties"]["connected"] is True
                and all(value == 0 for value in support["downstream_nonpromotion"].values()),
                "C10 support scope",
            )
            validate_primitive_ast(support["carrier_domain_ast"], graph_id + ":carrier")
            validate_primitive_ast(support["base_domain_ast"], graph_id + ":base")
            validate_primitive_ast(support["equation_ast"], graph_id + ":equation")
            validate_primitive_ast(support["exact_support_ast"], graph_id + ":support")
            need(
                support["equation_ast"]["op"] == "EQ"
                and support["equation_ast"]["right"] == rational_ast(0)
                and support["exact_support_ast"]
                == and_ast(support["carrier_domain_ast"], support["base_domain_ast"], support["equation_ast"]),
                "C10 exact support assembly",
            )
            r242_ref = support["legacy_source_refs"]["R242_exact_patch_authority"]
            need(
                r242_ref["row_id"] == graph_id
                and r242_ref["row_sha256"] == patch["row_sha256"]
                and r242_ref["full_row_sha256"] == object_sha(patch),
                "C10-R242 patch authority",
            )

            validate_closed_row(root, "R242 selected root")
            need(
                root["transition_sheet_patch_row_id"] == graph_id
                and root["existence_classification"] == "POSITIVE_2D_UNIQUE_GRAPH_PATCH_WITH_HALF_OPEN_OWNER"
                and root["local_positive_2D_transition_sheet_patch_credit"] == 1
                and root["Round220_split_interface_id"] == patch["Round220_split_interface_id"]
                and root["Round179_retained_child_row_id"] == patch["Round179_retained_child_row_id"]
                and root["strict_t_derivative_sign"] == patch["strict_t_derivative_sign"],
                "R242 root-patch binding",
            )
            box = patch["closed_witness_box"]
            base = patch["closed_base_rectangle"]
            need(
                positive_box(box, 3, "R242 witness") > 0
                and positive_box(base, 2, "R242 base") == Q(patch["exact_positive_base_projection_area"])
                and box[2:6] == base
                and patch["unique_graph_point_for_every_closed_base_point"] is True
                and patch["graph_strictly_interior_to_t_interval"] is True,
                "R242 exact patch geometry",
            )
            derivative_sign = patch["strict_t_derivative_sign"]
            need(derivative_sign in {"STRICT_NEGATIVE", "STRICT_POSITIVE"}, "R242 derivative sign")
            expected_faces = (
                ("STRICT_NEGATIVE", "STRICT_POSITIVE")
                if derivative_sign == "STRICT_POSITIVE"
                else ("STRICT_POSITIVE", "STRICT_NEGATIVE")
            )
            need(
                (patch["lower_t_face_F_sign"], patch["upper_t_face_F_sign"])
                == expected_faces,
                "R242 oriented face signs",
            )
            derivative_census[derivative_sign] += 1

            interface_id = patch["Round220_split_interface_id"]
            by_node = nodes_by_interface[interface_id]
            need(
                set(by_node)
                == {"OWNER_OPEN_BULK", "SHADOW_OPEN_BULK", "HALF_OPEN_TRANSITION_SHEET"},
                "R245 three node kinds",
            )
            owner = by_node["OWNER_OPEN_BULK"]
            shadow = by_node["SHADOW_OPEN_BULK"]
            sheet = by_node["HALF_OPEN_TRANSITION_SHEET"]
            common_node_fields = (
                "Round179_retained_child_row_id",
                "Round220_split_interface_id",
                "inherited_Round244_resolved_bulk_component_id",
                "official_key_id",
                "official_key_ordinal",
            )
            for field in common_node_fields:
                need(owner[field] == shadow[field] == sheet[field], "R245 common node field:" + field)
            need(
                owner["local_return_signature"] == patch["owner_signature"]
                and shadow["local_return_signature"] == patch["shadow_signature"]
                and sheet["local_return_signature"] == patch["owner_signature"]
                and owner["local_dimension"] == shadow["local_dimension"] == 3
                and sheet["local_dimension"] == 2
                and owner["half_open_owner_materialized"] is False
                and shadow["half_open_owner_materialized"] is False
                and sheet["half_open_owner_materialized"] is True
                and sheet["retained_stratum_node_id"] == support["sheet_member_id"]
                and Q(sheet["exact_positive_2D_sheet_area"]) == Q(patch["exact_positive_base_projection_area"]),
                "R245 patch node binding",
            )

            by_edge = edges_by_interface[interface_id]
            required_edge_kinds = {
                "OWNER_BULK_TO_HALF_OPEN_SHEET",
                "SHADOW_BULK_TO_HALF_OPEN_SHEET",
                "RESOLVED_TO_MATCHING_GRAPH_SIDE_BULK",
            }
            need(set(by_edge) == required_edge_kinds, "R245 three edge kinds")
            owner_edge = by_edge["OWNER_BULK_TO_HALF_OPEN_SHEET"]
            shadow_edge = by_edge["SHADOW_BULK_TO_HALF_OPEN_SHEET"]
            resolved_edge = by_edge["RESOLVED_TO_MATCHING_GRAPH_SIDE_BULK"]
            for edge_kind, edge in by_edge.items():
                edge_kind_census[edge_kind] += 1
                need(
                    edge["Round220_split_interface_id"] == interface_id
                    and edge["inherited_Round244_resolved_bulk_component_id"]
                    == sheet["inherited_Round244_resolved_bulk_component_id"]
                    and edge["current_quotient_lower_bound_edge_credit"] == 1
                    and edge["physical_component_credit"] == 0
                    and edge["maximal_physical_component_credit"] == 0
                    and edge["global_exact_key_fibre_credit"] == 0,
                    "R245 edge scope:" + edge_kind,
                )
                edge_receipt(edge)
            need(
                owner_edge["left_node_id"] == owner["retained_stratum_node_id"]
                and owner_edge["right_node_id"] == sheet["retained_stratum_node_id"]
                and shadow_edge["left_node_id"] == shadow["retained_stratum_node_id"]
                and shadow_edge["right_node_id"] == sheet["retained_stratum_node_id"]
                and owner_edge["contact_proof_kind"]
                == shadow_edge["contact_proof_kind"]
                == "ROUND242_POSITIVE_2D_UNIQUE_GRAPH_PATCH"
                and owner_edge["exact_positive_2D_contact_rectangle"]
                == shadow_edge["exact_positive_2D_contact_rectangle"]
                == base
                and Q(owner_edge["exact_positive_2D_contact_area"])
                == Q(shadow_edge["exact_positive_2D_contact_area"])
                == Q(patch["exact_positive_base_projection_area"]),
                "R245 graph-side contact endpoints",
            )
            need(
                resolved_edge["left_node_id"] == root["Round179_resolved_sibling_row_id"]
                and resolved_edge["right_node_id"]
                in {owner["retained_stratum_node_id"], shadow["retained_stratum_node_id"]}
                and resolved_edge["contact_proof_kind"]
                in {"ROUND242_GRAPH_SIDE_AT_T_INTERFACE", "256_BIT_STRICT_DYADIC_CORRIDOR_AT_P_INTERFACE"},
                "R245 resolved-lineage edge",
            )
            resolved_contact_census[resolved_edge["contact_proof_kind"]] += 1

            interface_core = {
                "schema": INTERFACE_ROW_SCHEMA,
                "row_id": PREFIX + ":interface-kernel:" + object_sha(graph_id),
                "graph_id": graph_id,
                "Round220_split_interface_id": interface_id,
                "C10_exact_support_ref": row_ref(support),
                "C10_identity_ref": row_ref(identity_row),
                "R242_patch_ref": row_ref(patch, "transition_sheet_patch_row_id"),
                "R242_root_ref": row_ref(root, "root_existence_row_id"),
                "exact_closed_witness_box": box,
                "exact_closed_base_rectangle": base,
                "exact_positive_base_area": patch["exact_positive_base_projection_area"],
                "strict_t_derivative_sign": derivative_sign,
                "lower_t_face_F_sign": patch["lower_t_face_F_sign"],
                "upper_t_face_F_sign": patch["upper_t_face_F_sign"],
                "owner_t_side": patch["owner_t_side"],
                "node_bundle": {
                    "sheet": row_ref(sheet, "retained_stratum_node_id"),
                    "owner_open_bulk": row_ref(owner, "retained_stratum_node_id"),
                    "shadow_open_bulk": row_ref(shadow, "retained_stratum_node_id"),
                },
                "three_edge_bundle": {
                    "owner_bulk_to_half_open_sheet": edge_receipt(owner_edge),
                    "shadow_bulk_to_half_open_sheet": edge_receipt(shadow_edge),
                    "resolved_to_matching_graph_side_bulk": edge_receipt(resolved_edge),
                },
                "edge_kind_exhaustion": sorted(required_edge_kinds),
                "graph_sheet_set_equality_proved": False,
                "representation_pullback_proved": False,
                "DSU_edge_or_union_authorized": False,
                "downstream_nonpromotion": ZERO_DOWNSTREAM,
            }
            interface_row = closed_row(interface_core)
            interface_rows.append(interface_row)

            factor = support["equation_ast"]["left"]
            for role, node, role_edge in (
                ("OWNER_OPEN_BULK", owner, owner_edge),
                ("SHADOW_OPEN_BULK", shadow, shadow_edge),
            ):
                routing = c11_by_subject.get((graph_id, role, node["retained_stratum_node_id"]))
                need(routing is not None, "C11 R242 routing binding")
                need(
                    routing["graph_id"] == graph_id
                    and routing["side_role"] == role
                    and routing["side_member_id"] == node["retained_stratum_node_id"]
                    and routing["candidate_ready_routing"] is True
                    and routing["disposition"] == "CANDIDATE_READY_ROUTING"
                    and routing["local_graph_side_physical_incidence_proved"] is False
                    and routing["one_sided_trace_proved"] is False
                    and routing["representation_pullback_proved"] is False
                    and routing["DSU_edge_or_union_authorized"] is False
                    and len(routing["missing_theorem_authority"]) > 0
                    and all(value == 0 for value in routing["formal_credit"].values()),
                    "C11 R242 routing zero-credit boundary",
                )
                role_census[role] += 1
                side_sign = "STRICT_POSITIVE" if role == "OWNER_OPEN_BULK" else "STRICT_NEGATIVE"
                side_t_side = (
                    patch["owner_t_side"]
                    if role == "OWNER_OPEN_BULK"
                    else ("LOWER_T_SIDE" if patch["owner_t_side"] == "UPPER_T_SIDE" else "UPPER_T_SIDE")
                )
                face_sign = patch["lower_t_face_F_sign"] if side_t_side == "LOWER_T_SIDE" else patch["upper_t_face_F_sign"]
                need(face_sign == side_sign, "R242 role/face factor sign")
                direction = "DECREASING_T_FROM_GRAPH" if side_t_side == "LOWER_T_SIDE" else "INCREASING_T_FROM_GRAPH"
                direction_census[direction] += 1
                corridor = node["strict_positive_3D_witness_box"]
                need(
                    corridor == role_edge["strict_positive_3D_retained_corridor_box"]
                    and corridor[2:6] == base
                    and Q(node["strict_positive_3D_witness_volume"])
                    == positive_box(corridor, 3, "R245 role corridor")
                    == Q(role_edge["strict_positive_3D_retained_corridor_volume"])
                    and Q(box[0]) <= Q(corridor[0]) < Q(corridor[1]) <= Q(box[1]),
                    "R245 role corridor geometry",
                )
                if side_t_side == "LOWER_T_SIDE":
                    need(corridor[0] == box[0], "lower-side anchored witness")
                else:
                    need(corridor[1] == box[1], "upper-side anchored witness")

                sign_predicate = relation_ast(side_sign, factor)
                exact_side_carrier_ast = and_ast(
                    support["carrier_domain_ast"],
                    support["base_domain_ast"],
                    sign_predicate,
                )
                sealed_witness_corridor_ast = and_ast(box_ast(corridor), sign_predicate)
                common_boundary_ast = and_ast(
                    support["carrier_domain_ast"],
                    support["base_domain_ast"],
                    support["equation_ast"],
                )
                need(common_boundary_ast == support["exact_support_ast"], "common boundary exact support")
                validate_primitive_ast(exact_side_carrier_ast, graph_id + ":" + role + ":side")
                validate_primitive_ast(sealed_witness_corridor_ast, graph_id + ":" + role + ":corridor")

                relation_core = {
                    "schema": RELATION_ROW_SCHEMA,
                    "row_id": PREFIX + ":relation-theorem:" + object_sha([graph_id, role, node["retained_stratum_node_id"]]),
                    "graph_id": graph_id,
                    "side_role": role,
                    "side_member_id": node["retained_stratum_node_id"],
                    "sheet_member_id": sheet["retained_stratum_node_id"],
                    "interface_kernel_ref": row_ref(interface_row),
                    "C10_exact_support_ref": row_ref(support),
                    "C10_identity_ref": row_ref(identity_row),
                    "C11_routing_disposition_ref": row_ref(routing),
                    "R242_patch_ref": row_ref(patch, "transition_sheet_patch_row_id"),
                    "R245_side_node_ref": row_ref(node, "retained_stratum_node_id"),
                    "R245_role_graph_sheet_edge_ref": row_ref(role_edge, "mixed_sheet_edge_id"),
                    "R245_resolved_lineage_edge_ref": row_ref(resolved_edge, "mixed_sheet_edge_id"),
                    "exact_side_carrier_ast": exact_side_carrier_ast,
                    "sealed_signature_witness_corridor_ast": sealed_witness_corridor_ast,
                    "common_boundary_graph_ast": common_boundary_ast,
                    "ast_sha256": {
                        "exact_side_carrier_ast": object_sha(exact_side_carrier_ast),
                        "sealed_signature_witness_corridor_ast": object_sha(sealed_witness_corridor_ast),
                        "common_boundary_graph_ast": object_sha(common_boundary_ast),
                    },
                    "one_sided_direction_receipt": {
                        "coordinate": "t",
                        "direction_from_graph": direction,
                        "t_side": side_t_side,
                        "factor_sign_on_side": side_sign,
                        "strict_t_derivative_sign": derivative_sign,
                        "corresponding_carrier_face_sign": face_sign,
                        "unique_graph_point_for_every_exact_base_point": True,
                    },
                    "collar_receipt": {
                        "exact_closed_base_rectangle": base,
                        "exact_positive_base_area": patch["exact_positive_base_projection_area"],
                        "strict_positive_witness_corridor_box": corridor,
                        "strict_positive_witness_corridor_volume": node["strict_positive_3D_witness_volume"],
                        "witness_corridor_signature": node["local_return_signature"],
                        "strict_monotonicity_orders_side_and_graph_over_every_base_point": True,
                        "role_edge_contact_rectangle_equals_exact_graph_base": True,
                    },
                    "common_boundary_trace_receipt": {
                        "direct_patch_theorem_not_graph_sheet_set_equality": True,
                        "primitive_factor_continuity_bound_to_C10_radical_receipts": True,
                        "C10_radical_side_condition_receipts_sha256": object_sha(support["radical_side_condition_receipts"]),
                        "strict_monotone_unique_zero_over_full_base": True,
                        "closure_of_one_sided_sign_collar_meets_zero_set_in_exact_C10_support": True,
                        "R245_role_edge_has_exact_R242_patch_contact": True,
                        "trace_direction": direction,
                    },
                    "theorem_statement": "THE_C10_EXACT_R242_GRAPH_FEATURE_IS_DIRECTLY_INCIDENT_TO_THIS_R245_OPEN_SIDE_AND_IS_ITS_LOCAL_ONE_SIDED_COMMON_BOUNDARY_TRACE",
                    "local_graph_side_physical_incidence_proved": True,
                    "one_sided_trace_proved": True,
                    "graph_sheet_set_equality_proved": False,
                    "representation_pullback_proved": False,
                    "DSU_edge_or_union_authorized": False,
                    "formal_credit": {
                        "local_graph_side_physical_incidence": 1,
                        "one_sided_trace": 1,
                        **ZERO_DOWNSTREAM,
                    },
                }
                relation_rows.append(closed_row(relation_core))

        need(len(interface_rows) == 264 and len(relation_rows) == 528, "output census")
        need(role_census == {"OWNER_OPEN_BULK": 264, "SHADOW_OPEN_BULK": 264}, "role census")
        need(direction_census == {"DECREASING_T_FROM_GRAPH": 264, "INCREASING_T_FROM_GRAPH": 264}, "direction census")
        need(derivative_census == {"STRICT_POSITIVE": 132, "STRICT_NEGATIVE": 132}, "derivative census")
        need(
            edge_kind_census
            == {
                "OWNER_BULK_TO_HALF_OPEN_SHEET": 264,
                "SHADOW_BULK_TO_HALF_OPEN_SHEET": 264,
                "RESOLVED_TO_MATCHING_GRAPH_SIDE_BULK": 264,
            },
            "edge-kind census",
        )
        need(
            resolved_contact_census
            == {
                "ROUND242_GRAPH_SIDE_AT_T_INTERFACE": 252,
                "256_BIT_STRICT_DYADIC_CORRIDOR_AT_P_INTERFACE": 12,
            },
            "resolved contact census",
        )

        interface_wire, interface_plain = gzip_rows(interface_rows)
        relation_wire, relation_plain = gzip_rows(relation_rows)
        body = {
            "schema": SCHEMA,
            "status": STATUS,
            "producer_source": producer_record(),
            "source_pins": [pin.__dict__ for pin in PINS],
            "upstream_seal_bindings": {
                "C10_manifest_sha256": PIN_BY_ROLE["C10_MANIFEST"].sha256,
                "C11_routing_manifest_sha256": PIN_BY_ROLE["C11_MANIFEST"].sha256,
                "R242_manifest_sha256": PIN_BY_ROLE["R242_MANIFEST"].sha256,
                "R245_manifest_sha256": PIN_BY_ROLE["R245_MANIFEST"].sha256,
            },
            "census": {
                "R242_graphs": 264,
                "R242_split_interfaces": 264,
                "local_graph_side_relations": 528,
                "OWNER_OPEN_BULK": 264,
                "SHADOW_OPEN_BULK": 264,
                "R245_edges_bound": 792,
                "edge_kind_census": dict(edge_kind_census),
                "resolved_contact_proof_kind_census": dict(resolved_contact_census),
                "strict_t_derivative_sign_census": dict(derivative_census),
                "direction_census": dict(direction_census),
            },
            "scoped_credit": {
                "local_graph_side_physical_incidence": 528,
                "one_sided_trace": 528,
            },
            "formal_credit": ZERO_DOWNSTREAM,
            "strict_nonpromotion": {
                "graph_sheet_set_equality_proved": False,
                "representation_pullback_proved": False,
                "member_normalized_support_sealed": False,
                "global_normalized_support_sealed": False,
                "new_DSU_edge_or_union_authorized": False,
                "B1A_permitted": False,
                "B2_permitted": False,
                "maximality_permitted": False,
                "CM2": "NO-GO_FOR_CLAIM",
            },
            "interface_kernel_ledger": ledger_descriptor(
                INTERFACE_LEDGER_NAME,
                INTERFACE_ROW_SCHEMA,
                interface_rows,
                interface_wire,
                interface_plain,
            ),
            "relation_theorem_ledger": ledger_descriptor(
                RELATION_LEDGER_NAME,
                RELATION_ROW_SCHEMA,
                relation_rows,
                relation_wire,
                relation_plain,
            ),
            "required_next": {
                "independent_verifier_and_attack_suite": True,
                "prove_representation_pullback_before_normalized_support": True,
                "seal_theorem_to_edge_before_any_DSU_reclosure": True,
            },
            "seed_serialized_or_semantically_used": False,
        }
        result = {**body, "result_sha256": object_sha(body)}
        snapshot.final()
    return result, interface_wire, relation_wire


def write_once(directory: Path, filename: str, payload: bytes) -> None:
    path = directory / filename
    need(not path.exists(), "publish no-clobber:" + filename)
    descriptor = os.open(
        path,
        os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW | os.O_CLOEXEC,
        0o600,
    )
    try:
        offset = 0
        while offset < len(payload):
            written = os.write(descriptor, payload[offset:])
            need(written > 0, "publish progress:" + filename)
            offset += written
        os.fsync(descriptor)
    finally:
        os.close(descriptor)
    info = os.stat(path, follow_symlinks=False)
    need(
        stat.S_ISREG(info.st_mode)
        and info.st_nlink == 1
        and info.st_size == len(payload),
        "published file:" + filename,
    )


def main() -> int:
    need(sys.flags.isolated == 1 and sys.dont_write_bytecode is True, "python -I -B")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--print-result", action="store_true")
    parser.add_argument("--candidate-dir")
    parser.add_argument("--publish", action="store_true")
    arguments = parser.parse_args()
    need(
        sum((arguments.print_result, arguments.candidate_dir is not None, arguments.publish)) == 1,
        "exactly one mode",
    )
    result, interface_wire, relation_wire = build()
    result_wire = canonical(result)
    if arguments.print_result:
        sys.stdout.buffer.write(result_wire + b"\n")
        return 0
    directory = ROOT if arguments.publish else Path(arguments.candidate_dir).resolve()
    if not arguments.publish:
        need(
            os.path.commonpath((str(directory), str(ROOT.resolve()))) != str(ROOT.resolve()),
            "candidate outside deliverables",
        )
        directory.mkdir(mode=0o700, parents=False, exist_ok=False)
    payloads = (
        (INTERFACE_LEDGER_NAME, interface_wire),
        (RELATION_LEDGER_NAME, relation_wire),
        (RESULT_NAME, result_wire),
    )
    records = []
    for filename, payload in payloads:
        write_once(directory, filename, payload)
        records.append({
            "filename": filename,
            "size": len(payload),
            "sha256": hashlib.sha256(payload).hexdigest(),
        })
    for record in reversed(records):
        descriptor = os.open(
            directory / record["filename"],
            os.O_RDONLY | os.O_NOFOLLOW | os.O_CLOEXEC,
        )
        try:
            need(hash_fd(descriptor) == record["sha256"], "reverse publication digest")
        finally:
            os.close(descriptor)
    print(json.dumps({
        "status": result["status"],
        "result_sha256": result["result_sha256"],
        "published_result_last": True,
        "files": records,
    }, sort_keys=True, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
