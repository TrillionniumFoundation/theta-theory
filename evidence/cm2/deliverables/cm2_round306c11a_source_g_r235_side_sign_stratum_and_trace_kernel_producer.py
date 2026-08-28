#!/usr/bin/env python3
"""Produce the scoped R235/R235D exact side-stratum and trace kernel.

This producer is intentionally narrower than round306c11.  It emits only the
9,422 graph-to-side relations for which the *current closed carrier* contains
an executable one-sided trace:

* 8,864 R235 target-factor relations (both strict sign strata);
* 552 R235 source-factor relations (the unique inward face stratum); and
* 6 R235D source-factor SAME_SIGN_EVENT_ABSENT relations (the unique inward
  shared stratum).

The 152 R235 adjacent-domain rows, 16 R235D outside-domain rows, and all R242
rows are outside this kernel.  A row can receive scoped local incidence/trace
credit only after its primitive exact side AST, legacy natural key, closure
boundary rule, and axis-ray trace atlas all validate.  No graph-sheet set
equality, representation pullback, normalized support, edge/union, B1A, B2,
maximality, or CM2 claim is made.

The C10 pins deliberately fail closed until C10 is sealed and the four
placeholder pins below are patched to the sealed bytes.  This file is a
producer draft; it does not import or execute any upstream producer.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
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
PREFIX: Final = "cm2_round306c11a_source_g_r235_side_sign_stratum_and_trace_kernel"
SCHEMA: Final = "cm2.round306c11a.source-g-r235-side-sign-stratum-and-trace-kernel.v1"
ROW_SCHEMA: Final = SCHEMA + ".kernel-row.v1"
LEDGER_NAME: Final = PREFIX + "_ledger.jsonl.gz"
RESULT_NAME: Final = PREFIX + "_result.json"
STATUS: Final = (
    "PASS_9422_SCOPED_R235_R235D_EXACT_SIDE_STRATA__"
    "9422_LOCAL_CLOSURE_INCIDENCE_AND_ONE_SIDED_TRACE_KERNEL_ROWS__"
    "ZERO_PULLBACK_NORMALIZED_SUPPORT_DSU_B1A_B2_MAXIMALITY_CM2_CREDIT"
)

C10_MANIFEST: Final = "cm2_round306c10_source_g_exact_graph_support_identity_rematerialization_manifest.sha256"
C10_RESULT: Final = "cm2_round306c10_source_g_exact_graph_support_identity_rematerialization_result.json"
C10_SUPPORT: Final = "cm2_round306c10_source_g_exact_graph_support_identity_rematerialization_exact_graph_support_ledger.jsonl.gz"
C10_IDENTITY: Final = "cm2_round306c10_source_g_exact_graph_support_identity_rematerialization_member_identity_disposition_ledger.jsonl.gz"
C11_MANIFEST: Final = "cm2_round306c11_source_g_graph_side_local_theorem_disposition_manifest.sha256"
C11_RESULT: Final = "cm2_round306c11_source_g_graph_side_local_theorem_disposition_result.json"
C11_DISPOSITION: Final = "cm2_round306c11_source_g_graph_side_local_theorem_disposition_disposition_ledger.jsonl.gz"
C9_MANIFEST: Final = "cm2_round306c9_source_g_g2_relation_admissibility_and_envelope_audit_manifest.sha256"
C9_RESULT: Final = "cm2_round306c9_source_g_g2_relation_admissibility_and_envelope_audit_result.json"
C9_GRAPH: Final = "cm2_round306c9_source_g_g2_relation_admissibility_and_envelope_audit_graph_domain_audit_ledger.jsonl.gz"
C9_RELATION: Final = "cm2_round306c9_source_g_g2_relation_admissibility_and_envelope_audit_relation_disposition_ledger.jsonl.gz"
C7_MANIFEST: Final = "cm2_round306c7_source_g_fresh_identity_support_mechanical_replay_manifest.sha256"
C7_PHYSICAL: Final = "cm2_round306c7_source_g_fresh_identity_support_mechanical_replay_physical_incidence_statement_ledger.jsonl.gz"
C4_MANIFEST: Final = "cm2_round306c4_source_g_r235d_to_g2_orphan_graph_semantic_bridge_manifest.sha256"
C4_LEDGER: Final = "cm2_round306c4_source_g_r235d_to_g2_orphan_graph_semantic_bridge_row_ledger.jsonl.gz"
R235_MANIFEST: Final = "cm2_round235_source_g_single_endpoint_graph_word_key_partition_manifest.sha256"
R235_CERT: Final = "cm2_round235_source_g_single_endpoint_graph_word_key_partition_certificate.json"
R236_MANIFEST: Final = "cm2_round236_source_g_wall_residual_closure_and_root_key_partition_manifest.sha256"
R236_CERT: Final = "cm2_round236_source_g_wall_residual_closure_and_root_key_partition_certificate.json"
R248_MANIFEST: Final = "cm2_round248_source_g_wall_finite_key_retained_quotient_manifest.sha256"
R248_CERT: Final = "cm2_round248_source_g_wall_finite_key_retained_quotient_certificate.json"


@dataclass(frozen=True)
class Pin:
    role: str
    filename: str
    size: int
    sha256: str


PINS: Final = (
    Pin("C10_MANIFEST", C10_MANIFEST, 1_431, "b7277863feb9edc5f35906b04af2a9a256becb7ee9f1f1df6558b897184029ca"),
    Pin("C10_RESULT", C10_RESULT, 9_468, "b188eaa6c4dee77e0fff13b4a48cec9f8b46d324e48e7927265807a0f2865b55"),
    Pin("C10_SUPPORT", C10_SUPPORT, 19_958_893, "b7b2b02653a404060364b788b3e0ac8693d2d9d8d1c45e6109ca7f4400c4080c"),
    Pin("C10_IDENTITY", C10_IDENTITY, 2_966_603, "5041df1ab4b5bf9e79984859f828c9fb69718f53bd62d2920d51ebea8b7ec9df"),
    Pin("C11_MANIFEST", C11_MANIFEST, 1_652, "b087b80d90bc524af29ccbc0dc80ea82f157ae491404f64de342bb10c16d5d73"),
    Pin("C11_RESULT", C11_RESULT, 12_545, "083103ac958dfcb01283850abcda03fcdce26a8910c42b79c570a87486925506"),
    Pin("C11_DISPOSITION", C11_DISPOSITION, 10_888_167, "b1af6336b83842f2c6380929977f6d3591cfb50a1b305c7eafd197931d623543"),
    Pin("C9_MANIFEST", C9_MANIFEST, 1_396, "8921fb3eadd5d8b4aec1afe3af91c938b2c5568e9f9ef3be64002e4146152d04"),
    Pin("C9_RESULT", C9_RESULT, 8_845, "31d8da4e4a3e6ad703bd24fd7456f801d3fd90293e171d9784b2280d393b76a8"),
    Pin("C9_GRAPH", C9_GRAPH, 2_488_534, "955d8930fc321ca4f2556d66af488e4b9391f91002b65ecf8eaace6fbd3a7d50"),
    Pin("C9_RELATION", C9_RELATION, 5_184_953, "0ffdec565560e1b44198285fea7e801ab7ed655d964d521b8693e95064744e71"),
    Pin("C7_MANIFEST", C7_MANIFEST, 2_184, "4e534e412a760d13fe7eb278ca063e86ac2a7164bbfdb3b14a3142219267c0c6"),
    Pin("C7_PHYSICAL", C7_PHYSICAL, 9_771_275, "e6450435f74f038f3de2ada64935fc1f72bec6eb4323f2dc5ad8069bf3ea490e"),
    Pin("C4_MANIFEST", C4_MANIFEST, 1_177, "5550eb9cf4e474a8d08086062e28538e909f6e1c7e499ba10a78a2d24e683de6"),
    Pin("C4_LEDGER", C4_LEDGER, 101_147, "3b273e7637af99e19a23ec62a29999023d73aba9a901fe4311fc631aae0cc6db"),
    Pin("R235_MANIFEST", R235_MANIFEST, 566, "cf58b7d2f419ea252c3398665302fe6f5ff06436af20a56beaaa47e5ef822ea0"),
    Pin("R235_CERT", R235_CERT, 67_765_471, "e340fa1a071d85a36b54d10a45ae2fdb9d70b8c90f4c21f054c6fc9505e5e787"),
    Pin("R236_MANIFEST", R236_MANIFEST, 582, "28f6f6d2f5b0f10edba5cd473b4126a8fed098874849c2f579eadd92b30d324c"),
    Pin("R236_CERT", R236_CERT, 2_061_199, "b5b9ec358b4837a02218756a034440d8fbc2aa706ca421bedb28aaf785de0217"),
    Pin("R248_MANIFEST", R248_MANIFEST, 885, "b1ddedd01041e71b5c12fa4989726815c8685e6df77f54d9dbddda64aaf89e07"),
    Pin("R248_CERT", R248_CERT, 205_148_977, "fa48bdfb0056072f80c5809f57362c225f0beb40e1cc4c145f3f072335cdb311"),
)
PIN_BY_ROLE: Final = {pin.role: pin for pin in PINS}

DOWNSTREAM_ZERO: Final = {
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
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True, allow_nan=False).encode("ascii")


def object_sha(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def identity(info: os.stat_result) -> tuple[int, ...]:
    return (info.st_dev, info.st_ino, info.st_mode, info.st_nlink, info.st_size, info.st_mtime_ns, info.st_ctime_ns)


def hash_fd(descriptor: int) -> str:
    os.lseek(descriptor, 0, os.SEEK_SET)
    digest = hashlib.sha256()
    while True:
        block = os.read(descriptor, 1_048_576)
        if not block:
            return digest.hexdigest()
        digest.update(block)


def read_fd(descriptor: int) -> bytes:
    os.lseek(descriptor, 0, os.SEEK_SET)
    blocks: list[bytes] = []
    while True:
        block = os.read(descriptor, 1_048_576)
        if not block:
            return b"".join(blocks)
        blocks.append(block)


class Snapshot:
    def __init__(self) -> None:
        self.directory_descriptor = -1
        self.descriptors: dict[str, int] = {}
        self.identities: dict[str, tuple[int, ...]] = {}

    def __enter__(self) -> "Snapshot":
        before = os.stat(ROOT, follow_symlinks=False)
        need(stat.S_ISDIR(before.st_mode) and not ROOT.is_symlink(), "deliverables directory")
        self.directory_descriptor = os.open(ROOT, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW | os.O_CLOEXEC)
        for pin in PINS:
            info = os.stat(pin.filename, dir_fd=self.directory_descriptor, follow_symlinks=False)
            need(stat.S_ISREG(info.st_mode) and info.st_nlink == 1 and info.st_size == pin.size, "pin identity:" + pin.role)
            descriptor = os.open(pin.filename, os.O_RDONLY | os.O_NOFOLLOW | os.O_CLOEXEC, dir_fd=self.directory_descriptor)
            opened = os.fstat(descriptor)
            need(identity(opened) == identity(info), "pin race:" + pin.role)
            need(hash_fd(descriptor) == hash_fd(descriptor) == pin.sha256, "pin digest:" + pin.role)
            self.descriptors[pin.role] = descriptor
            self.identities[pin.role] = identity(opened)
        return self

    def read(self, role: str) -> bytes:
        return read_fd(self.descriptors[role])

    def duplicate(self, role: str) -> int:
        descriptor = os.dup(self.descriptors[role])
        os.lseek(descriptor, 0, os.SEEK_SET)
        return descriptor

    def final(self) -> None:
        for pin in reversed(PINS):
            descriptor = self.descriptors[pin.role]
            need(identity(os.fstat(descriptor)) == self.identities[pin.role], "final fd:" + pin.role)
            need(identity(os.stat(pin.filename, dir_fd=self.directory_descriptor, follow_symlinks=False)) == self.identities[pin.role], "final path:" + pin.role)
            need(hash_fd(descriptor) == pin.sha256, "final digest:" + pin.role)

    def __exit__(self, *_: Any) -> None:
        for descriptor in self.descriptors.values():
            try:
                os.close(descriptor)
            except OSError:
                pass
        if self.directory_descriptor >= 0:
            os.close(self.directory_descriptor)


def jsonl_rows(snapshot: Snapshot, role: str) -> Iterator[dict[str, Any]]:
    descriptor = snapshot.duplicate(role)
    with os.fdopen(descriptor, "rb", closefd=True) as raw, gzip.GzipFile(fileobj=raw, mode="rb") as stream:
        for ordinal, line in enumerate(stream):
            row = json.loads(line)
            need(type(row) is dict and line == canonical(row) + b"\n", "canonical JSONL:" + role + ":" + str(ordinal))
            core = dict(row)
            claimed = core.pop("row_sha256", None)
            need(type(claimed) is str and claimed == object_sha(core), "row closure:" + role + ":" + str(ordinal))
            yield row


def closed_document(snapshot: Snapshot, role: str) -> dict[str, Any]:
    raw = snapshot.read(role)
    document = json.loads(raw)
    need(type(document) is dict and raw in (canonical(document), canonical(document) + b"\n"), "canonical document:" + role)
    core = dict(document)
    claimed = core.pop("result_sha256", None)
    need(type(claimed) is str and claimed == object_sha(core), "document closure:" + role)
    return document


def legacy_document(snapshot: Snapshot, role: str) -> dict[str, Any]:
    document = json.loads(snapshot.read(role))
    need(type(document) is dict and type(document.get("result")) is dict, "legacy document:" + role)
    need(document.get("result_sha256") == object_sha(document["result"]), "legacy closure:" + role)
    return document


def bind_manifest(snapshot: Snapshot, manifest_role: str, member_roles: tuple[str, ...]) -> None:
    entries: dict[str, str] = {}
    for line in snapshot.read(manifest_role).decode("ascii").splitlines():
        digest, marker, filename = line.partition("  ")
        need(marker == "  " and len(digest) == 64 and filename not in entries, "manifest syntax:" + manifest_role)
        entries[filename] = digest
    for role in member_roles:
        pin = PIN_BY_ROLE[role]
        candidate_names = (pin.filename, "deliverables/" + pin.filename)
        matches = [entries[name] for name in candidate_names if name in entries]
        need(len(matches) == 1 and matches[0] == pin.sha256, "manifest member:" + manifest_role + ":" + role)


def closed_row(core: dict[str, Any]) -> dict[str, Any]:
    return {**core, "row_sha256": object_sha(core)}


def row_ref(row: dict[str, Any], id_field: str = "row_id") -> dict[str, str]:
    return {"row_id": row[id_field], "row_sha256": row["row_sha256"]}


def qwire(value: Q | int | str) -> str:
    fraction = Q(value)
    return str(fraction.numerator) if fraction.denominator == 1 else f"{fraction.numerator}/{fraction.denominator}"


def q(value: Any) -> Q:
    if type(value) is str:
        return Q(value)
    if type(value) is dict and set(value) == {"numerator", "denominator"}:
        return Q(value["numerator"], value["denominator"])
    raise Rejected("non-exact rational")


def rational_ast(value: Q | int | str) -> dict[str, Any]:
    return {"op": "RATIONAL_CONSTANT", "value": qwire(value)}


def multiply_ast(*arguments: dict[str, Any]) -> dict[str, Any]:
    return {"op": "MUL", "args": list(arguments)}


def and_ast(*arguments: dict[str, Any]) -> dict[str, Any]:
    return {"op": "AND", "args": list(arguments)}


def sign_relation_ast(factor: dict[str, Any], eta: int, relation: str) -> dict[str, Any]:
    need(eta in (-1, 1) and relation in ("GT", "LT"), "side sign relation")
    return {"op": relation, "left": multiply_ast(rational_ast(eta), factor), "right": rational_ast(0)}


def validate_primitive_ast(value: Any, label: str) -> None:
    need(type(value) is dict and type(value.get("op")) is str, "AST node:" + label)
    operation = value["op"]
    if operation == "RATIONAL_CONSTANT":
        need(set(value) == {"op", "value"} and type(value["value"]) is str and qwire(value["value"]) == value["value"], "AST rational:" + label)
        return
    if operation == "COORDINATE":
        need(set(value) == {"op", "name"} and value["name"] in {"t", "p", "s"}, "AST coordinate:" + label)
        return
    if operation in {"ADD", "MUL", "AND"}:
        need(set(value) == {"op", "args"} and type(value["args"]) is list and bool(value["args"]), "AST nary:" + label)
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
        need(set(value) == {"op", "left", "right"}, "AST binary:" + label)
        validate_primitive_ast(value["left"], label + ":left")
        validate_primitive_ast(value["right"], label + ":right")
        return
    if operation == "CLOSED_INTERVAL":
        need(
            set(value) == {"op", "coordinate", "lower", "upper"}
            and value["coordinate"] in {"t", "p", "s"}
            and type(value["lower"]) is str
            and type(value["upper"]) is str
            and qwire(value["lower"]) == value["lower"]
            and qwire(value["upper"]) == value["upper"]
            and Q(value["lower"]) <= Q(value["upper"]),
            "AST interval:" + label,
        )
        return
    if operation == "OR_DISJOINT":
        need(set(value) == {"op", "cases"} and type(value["cases"]) is list and bool(value["cases"]), "AST cases:" + label)
        seen: set[str] = set()
        for ordinal, case in enumerate(value["cases"]):
            need(type(case) is dict and set(case) == {"case", "predicate"} and type(case["case"]) is str and case["case"] not in seen, "AST case:" + label)
            seen.add(case["case"])
            validate_primitive_ast(case["predicate"], label + ":case:" + str(ordinal))
        return
    raise Rejected("unrecognized AST operation:" + label + ":" + operation)


def carrier_bounds(carrier: dict[str, Any]) -> dict[str, tuple[Q, Q]]:
    validate_primitive_ast(carrier, "carrier")
    need(carrier["op"] == "AND", "carrier conjunction")
    bounds: dict[str, tuple[Q, Q]] = {}
    for node in carrier["args"]:
        if node.get("op") != "CLOSED_INTERVAL":
            continue
        coordinate = node["coordinate"]
        need(coordinate not in bounds, "unique carrier coordinate")
        bounds[coordinate] = (Q(node["lower"]), Q(node["upper"]))
    need(set(bounds) == {"t", "p", "s"} and all(lower < upper for lower, upper in bounds.values()), "positive TPS carrier")
    return bounds


def sign_number(label: str) -> int:
    need(label in {"STRICT_NEGATIVE", "STRICT_POSITIVE"}, "strict sign")
    return 1 if label == "STRICT_POSITIVE" else -1


def relation_desired_sign(side_role: str) -> int:
    if side_role in {"EVENT_ABSENT", "source:SAME_SIGN_EVENT_ABSENT"}:
        return 1
    if side_role == "EVENT_PRESENT":
        return -1
    raise Rejected("unsupported scoped side role:" + side_role)


def trace_chart(
    chart_id: str,
    locus: str,
    axis: str,
    derivative_sign: str,
    eta: int,
    desired_sign: int,
    carrier_margin_basis: dict[str, Any],
) -> dict[str, Any]:
    derivative_of_h_sign = eta * sign_number(derivative_sign)
    direction = desired_sign * derivative_of_h_sign
    need(direction in (-1, 1), "trace direction")
    core = {
        "chart_id": chart_id,
        "graph_locus": locus,
        "path_rule": "AXIS_RAY_FROM_GRAPH_POINT_V1",
        "axis": axis,
        "direction": direction,
        "quantified_path": {
            "base_point": "x_IN_EXACT_GRAPH_LOCUS",
            "exists": "epsilon_x_IN_Q_STRICT_POSITIVE",
            "parameter": "lambda_IN_Q_WITH_0_LT_lambda_LT_epsilon_x",
            "path": "gamma_x(lambda)=x+direction*lambda*e_axis",
            "unchanged_coordinates": [coordinate for coordinate in ("t", "p", "s") if coordinate != axis],
        },
        "signed_factor_derivative": {
            "factor_derivative_sign": derivative_sign,
            "eta": eta,
            "eta_times_factor_derivative_sign": "STRICT_POSITIVE" if derivative_of_h_sign > 0 else "STRICT_NEGATIVE",
            "directional_eta_times_factor_derivative_sign": "STRICT_POSITIVE" if desired_sign > 0 else "STRICT_NEGATIVE",
        },
        "carrier_margin_basis": carrier_margin_basis,
        "local_strict_sign_conclusion": "GT_ZERO" if desired_sign > 0 else "LT_ZERO",
        "limit_at_lambda_down_to_zero": "EXACT_GRAPH_BASE_POINT",
    }
    return {**core, "chart_sha256": object_sha(core)}


def target_trace_atlas(support: dict[str, Any], eta: int, desired_sign: int) -> dict[str, Any]:
    certificate = support["monotone_graph_certificate"]
    need(certificate["kind"] == "STRICT_T_MONOTONE_IMPLICIT_GRAPH_OVER_CONNECTED_SIGN_STRADDLE_BASE", "target monotone kind")
    t_proof = certificate["strict_t_derivative_proof"]
    t_sign = t_proof["strict_t_derivative_sign"]
    sign_number(t_sign)
    need(
        type(t_proof["proof_cell_count"]) is int
        and t_proof["proof_cell_count"] > 0
        and type(t_proof["maximum_split_depth"]) is int
        and 0 <= t_proof["maximum_split_depth"] <= 8,
        "target strict t derivative cover",
    )
    topology = certificate["face_p_topology_certificate"]
    need(topology["connected_sign_straddle_p_interval"] is True, "target connected base")
    need(topology["s_independence"] == {"proved_by_free_variable_analysis": True, "factor_variables": ["t", "p"], "full_s_interval_retained": True}, "target s independence")
    bounds = carrier_bounds(support["carrier_domain_ast"])
    charts = [
        trace_chart(
            "INTERIOR_T_GRAPH",
            "exact_graph_support AND t_lower<t<t_upper",
            "t",
            t_sign,
            eta,
            desired_sign,
            {"kind": "STRICT_INTERIOR_T_MARGIN", "carrier_t_interval": [qwire(bounds["t"][0]), qwire(bounds["t"][1])]},
        )
    ]
    roots = topology["implicit_cut_root_descriptors"]
    need(type(roots) is list and len(roots) == topology["implicit_cut_root_count"], "target cut root count")
    need(topology["corner_sign_receipts_sha256"] == object_sha(topology["corner_sign_receipts"]), "target corner receipt hash")
    expected_topology_shape = {
        "INTERNAL_P_BAND": (2, []),
        "LOWER_P_ATTACHED": (1, ["LOWER_P"]),
        "UPPER_P_ATTACHED": (1, ["UPPER_P"]),
        "FULL_P_INTERVAL": (0, ["LOWER_P", "UPPER_P"]),
    }
    need(topology["topology"] in expected_topology_shape, "target topology kind")
    expected_root_count, expected_inherited = expected_topology_shape[topology["topology"]]
    need(
        topology["implicit_cut_root_count"] == expected_root_count
        and topology["inherited_carrier_p_boundaries"] == expected_inherited
        and topology["inherited_carrier_p_boundary_count"] == len(expected_inherited),
        "target topology shape",
    )
    corners = {
        (receipt["face"], receipt["p_side"]): receipt["factor_sign"]
        for receipt in topology["corner_sign_receipts"]
    }
    need(
        set(corners)
        == {
            ("LOWER_T_FACE", "LOWER_P"),
            ("LOWER_T_FACE", "UPPER_P"),
            ("UPPER_T_FACE", "LOWER_P"),
            ("UPPER_T_FACE", "UPPER_P"),
        },
        "target corner receipt exhaustion",
    )
    for corner_sign in corners.values():
        sign_number(corner_sign)
    seen_faces: set[str] = set()
    p_lower, p_upper = bounds["p"]
    p_proofs = {
        "LOWER_T_FACE": topology["lower_t_face_p_derivative_proof"],
        "UPPER_T_FACE": topology["upper_t_face_p_derivative_proof"],
    }
    for face, proof in p_proofs.items():
        need(
            proof["face"] == face
            and sign_number(proof["strict_p_derivative_sign"]) in (-1, 1)
            and type(proof["proof_cell_count"]) is int
            and proof["proof_cell_count"] > 0
            and type(proof["maximum_split_depth"]) is int
            and 0 <= proof["maximum_split_depth"] <= 12,
            "target face p derivative cover:" + face,
        )
    for root in roots:
        face = root["face"]
        need(face in {"LOWER_T_FACE", "UPPER_T_FACE"} and face not in seen_faces, "target cut face")
        seen_faces.add(face)
        descriptor_core = dict(root)
        descriptor_sha = descriptor_core.pop("descriptor_sha256", None)
        need(type(descriptor_sha) is str and descriptor_sha == object_sha(descriptor_core), "target cut root descriptor closure")
        left = q(root["isolation_interval"][0])
        right = q(root["isolation_interval"][1])
        need(p_lower <= left < right <= p_upper, "target cut root bracket inside p carrier")
        need(corners[(face, "LOWER_P")] != corners[(face, "UPPER_P")], "target cut root strict interior by endpoint signs")
        p_sign = root["strict_p_derivative_sign"]
        sign_number(p_sign)
        need(p_sign == p_proofs[face]["strict_p_derivative_sign"], "target cut root p derivative binding")
        expected_t_value = bounds["t"][0] if face == "LOWER_T_FACE" else bounds["t"][1]
        need(q(root["t_value"]) == expected_t_value and q(p_proofs[face]["t_value"]) == expected_t_value, "target cut root t-face binding")
        need(
            sign_number(root["left_factor_sign"]) in (-1, 1)
            and sign_number(root["right_factor_sign"]) in (-1, 1)
            and root["left_factor_sign"] != root["right_factor_sign"],
            "target cut root bracket signs",
        )
        need(root["existence_by_opposite_endpoint_signs"] is True and root["uniqueness_by_strict_p_monotonicity"] is True, "target cut root theorem")
        charts.append(
            trace_chart(
                face + "_CUT_ROOT",
                "exact_graph_support AND t=" + (qwire(bounds["t"][0]) if face == "LOWER_T_FACE" else qwire(bounds["t"][1])),
                "p",
                p_sign,
                eta,
                desired_sign,
                {
                    "kind": "STRICT_INTERIOR_P_ROOT_BRACKET",
                    "implicit_cut_root_descriptor_id": root["descriptor_id"],
                    "implicit_cut_root_descriptor_sha256": root["descriptor_sha256"],
                    "isolation_interval": root["isolation_interval"],
                    "carrier_p_interval": [qwire(p_lower), qwire(p_upper)],
                    "strict_interior_from_opposite_strict_carrier_endpoint_signs": True,
                },
            )
        )
    need(len(charts) == 1 + topology["implicit_cut_root_count"], "target trace atlas exhaustion")
    return {
        "kind": "R235_TARGET_COMPLETE_RELATIVE_CARRIER_TRACE_ATLAS_V1",
        "coordinate_parameter": "TPS",
        "charts": charts,
        "coverage_rule": {
            "rule": "STRICT_T_GRAPH_POINTS_ARE_EITHER_T_INTERIOR_OR_A_UNIQUE_T_FACE_CUT_ROOT",
            "topology": topology["topology"],
            "implicit_cut_root_count": topology["implicit_cut_root_count"],
            "inherited_p_boundaries_have_t_interior_graph_points": topology["inherited_carrier_p_boundaries"],
            "all_exact_graph_points_covered": True,
        },
        "every_graph_point_has_a_side_approach_path": True,
    }


def face_trace_atlas(
    kind: str,
    zero_face: str,
    eta: int,
    desired_sign: int,
    carrier: dict[str, Any],
) -> dict[str, Any]:
    bounds = carrier_bounds(carrier)
    need(zero_face in {"LOWER", "UPPER"}, "source zero face")
    if zero_face == "LOWER":
        need(bounds["t"][0] == 0 < bounds["t"][1], "source lower face carrier")
        inward_direction = 1
        margin = bounds["t"][1]
    else:
        need(bounds["t"][0] < 0 == bounds["t"][1], "source upper face carrier")
        inward_direction = -1
        margin = -bounds["t"][0]
    chart = trace_chart(
        "FULL_BASE_INWARD_T_FACE",
        "exact_graph_support AND t=0",
        "t",
        "STRICT_POSITIVE",
        eta,
        desired_sign,
        {"kind": "EXACT_ONE_SIDED_T_FACE_MARGIN", "zero_face": zero_face, "uniform_rational_margin": qwire(margin)},
    )
    need(chart["direction"] == inward_direction, "selected branch is inward carrier stratum")
    return {
        "kind": kind,
        "coordinate_parameter": "TPS",
        "charts": [chart],
        "coverage_rule": {
            "rule": "EXPLICIT_t_EQUALS_ZERO_FULL_BASE_FACE",
            "zero_face": zero_face,
            "full_closed_p_s_base": True,
            "all_exact_graph_points_covered": True,
        },
        "every_graph_point_has_a_side_approach_path": True,
    }


def validate_r235(row: dict[str, Any], graph_id: str) -> None:
    need(row["endpoint_graph_partition_row_id"] == graph_id, "R235 graph id")
    need(row["endpoint_graph_dimension"] == 2 and row["local_finite_exact_key_partition_credit"] == 1, "R235 partition credit")
    need(row["distinct_side_exact_key_count"] == 2, "R235 side key count")
    sign_number(row["fixed_endpoint_factor_sign"])
    sign_number(row["active_factor_strict_t_derivative_sign"])
    need(row["transition_event_order_position"] in {"STRICT_FIRST", "STRICT_LAST"}, "R235 event order")
    need(type(row["candidate_time_strict_against_existing_event_count"]) is int and row["candidate_time_strict_against_existing_event_count"] >= 0, "R235 event-order comparison census")


def validate_c10_identity(identity_row: dict[str, Any], support: dict[str, Any]) -> None:
    need(identity_row["graph_id"] == support["graph_id"] and identity_row["sheet_member_id"] == support["sheet_member_id"], "C10 identity subject")
    need(identity_row["exact_support_ref"] == row_ref(support), "C10 identity support binding")
    need(identity_row["disposition"] == "PRESERVE_EXISTING_MEMBER_ID" and identity_row["recomputed_member_id"] == support["sheet_member_id"], "C10 identity preservation")
    need(identity_row["member_natural_key_preservation_credit"] == 1, "C10 identity credit")
    need(identity_row["set_equality_proved"] is False and identity_row["physical_incidence_proved"] is False and identity_row["identity_representation_pullback_proved"] is False, "C10 identity nonpromotion")
    need(all(value == 0 for value in identity_row["downstream_nonpromotion"].values()), "C10 identity downstream zero")


def validate_r248_bulk(
    bulk: dict[str, Any],
    relation_member_id: str,
    interface_id: str,
    source_kind: str,
    source_row_id: str,
    branch_label: str,
    signature: dict[str, Any],
) -> dict[str, Any]:
    core = dict(bulk)
    claimed = core.pop("row_sha256", None)
    need(type(claimed) is str and claimed == object_sha(core), "R248 bulk row closure")
    signature_sha = object_sha(signature)
    natural_key = [source_kind, source_row_id, branch_label, signature_sha]
    recomputed = "round248-wall-bulk:" + object_sha(natural_key)
    need(recomputed == relation_member_id == bulk["wall_bulk_node_id"], "R248 bulk natural key")
    need(
        bulk["Round220_split_interface_id"] == interface_id
        and bulk["source_partition_kind"] == source_kind
        and bulk["source_partition_row_id"] == source_row_id
        and bulk["branch_label"] == branch_label
        and bulk["local_return_signature_sha256"] == signature_sha,
        "R248 bulk lineage",
    )
    need(bulk["official_key_ordinal"] == signature["official_key_ordinal"] and bulk["official_key_id"] == signature["official_key_id"], "R248 exact key binding")
    need(bulk["exact_positive_3D_box"] is None and bulk["exact_positive_3D_volume"] is None, "R248 is not exact support geometry")
    need(bulk["physical_component_credit"] == 0 and bulk["maximal_physical_component_credit"] == 0, "R248 historical scope")
    return {
        "row_id": bulk["wall_bulk_node_id"],
        "row_sha256": bulk["row_sha256"],
        "Round220_split_interface_id": bulk["Round220_split_interface_id"],
        "source_partition_kind": bulk["source_partition_kind"],
        "source_partition_row_id": bulk["source_partition_row_id"],
        "branch_label": bulk["branch_label"],
        "local_return_signature_sha256": bulk["local_return_signature_sha256"],
        "positive_volume_proof_kind": bulk["positive_volume_proof_kind"],
        "natural_key_preimage": natural_key,
        "natural_key_preimage_sha256": object_sha(natural_key),
        "recomputed_side_member_id": recomputed,
        "official_key_ordinal": bulk["official_key_ordinal"],
        "official_key_id": bulk["official_key_id"],
        "support_geometry_taken_from_R248": False,
    }


def exact_factor(support: dict[str, Any]) -> dict[str, Any]:
    equation = support["equation_ast"]
    validate_primitive_ast(equation, "C10 equation")
    need(equation["op"] == "EQ" and equation["right"] == rational_ast(0), "C10 zero equation")
    factor = equation["left"]
    validate_primitive_ast(factor, "C10 factor")
    return factor


def branch_equivalence_certificate(
    graph_class: str,
    side_role: str,
    partition_ref: dict[str, Any],
    side_identity: dict[str, Any],
    eta: int,
    desired_sign: int,
    side_ast: dict[str, Any],
) -> dict[str, Any]:
    if graph_class in {"R235_TARGET_POSITIVE_PARTIAL_BASE", "R235_SOURCE_EXACT_FACE_FULL_BASE"}:
        need(side_role in {"EVENT_ABSENT", "EVENT_PRESENT"}, "R235 branch equivalence role")
        need(partition_ref["kind"] == "R235_SINGLE_ENDPOINT_GRAPH_PARTITION_ROW", "R235 partition equivalence source")
        rule = (
            "EVENT_ABSENT_IFF_FIXED_ENDPOINT_TIMES_ACTIVE_ENDPOINT_IS_STRICT_POSITIVE"
            if side_role == "EVENT_ABSENT"
            else "EVENT_PRESENT_IFF_FIXED_ENDPOINT_TIMES_ACTIVE_ENDPOINT_IS_STRICT_NEGATIVE"
        )
        order_basis = {
            "transition_event": partition_ref["transition_event"],
            "transition_event_order_position": partition_ref["transition_event_order_position"],
            "candidate_time_strict_against_existing_event_count": partition_ref["candidate_time_strict_against_existing_event_count"],
        }
    else:
        need(
            graph_class == "R235D_SOURCE_EXACT_FACE_FULL_BASE"
            and side_role == "source:SAME_SIGN_EVENT_ABSENT"
            and partition_ref["kind"] == "R236_DOUBLE_ENDPOINT_PARTITION_PLUS_C4_SOURCE_BRIDGE",
            "R235D branch equivalence scope",
        )
        rule = "SAME_SIGN_EVENT_ABSENT_IFF_FIXED_TARGET_FACTOR_TIMES_SOURCE_FACTOR_IS_STRICT_POSITIVE"
        order_basis = {
            "R236_partition_row_id": partition_ref["row_id"],
            "C4_bridge_ref": partition_ref["C4_bridge_ref"],
            "target_factor_fixed_sign_on_complete_domain": partition_ref["fixed_target_factor_sign"],
        }
    core = {
        "kind": "EXACT_PARTITION_BRANCH_TO_SIDE_MEMBER_SUPPORT_EQUIVALENCE_V1",
        "partition_rule": rule,
        "fixed_other_endpoint_eta": eta,
        "desired_eta_times_active_factor_sign": "STRICT_POSITIVE" if desired_sign > 0 else "STRICT_NEGATIVE",
        "event_order_or_double_arrangement_basis": order_basis,
        "R248_side_member_natural_key_preimage_sha256": side_identity["natural_key_preimage_sha256"],
        "R248_recomputed_side_member_id": side_identity["recomputed_side_member_id"],
        "R248_official_key_id": side_identity["official_key_id"],
        "R248_null_positive_box_used_as_support_geometry": False,
        "exact_side_stratum_ast_sha256": object_sha(side_ast),
        "equivalence_scope": "RELATIVE_TO_THE_C10_EXACT_CLOSED_CARRIER",
        "side_member_exact_support_equivalence_proved": True,
    }
    return {**core, "certificate_sha256": object_sha(core)}


def closure_certificate(
    graph_class: str,
    support: dict[str, Any],
    side_ast: dict[str, Any],
    branch_equivalence: dict[str, Any],
    trace_atlas: dict[str, Any],
    paired_relation_ref: dict[str, str] | None,
) -> dict[str, Any]:
    need(trace_atlas["every_graph_point_has_a_side_approach_path"] is True, "trace atlas completeness")
    need(branch_equivalence["side_member_exact_support_equivalence_proved"] is True, "side member exact support equivalence")
    target = graph_class == "R235_TARGET_POSITIVE_PARTIAL_BASE"
    radical_receipts = support["radical_side_condition_receipts"]
    if target:
        need(paired_relation_ref is not None, "target paired side relation")
        need(
            len(radical_receipts) == 3
            and {receipt["radicand"] for receipt in radical_receipts}
            == {"normal_radicand", "phase_radicand", "hit_radicand"},
            "target radical receipt exhaustion",
        )
        zero_projection_rule = "STRICT_T_MONOTONICITY_AND_ENDPOINT_SIGN_STRADDLE_EQUIVALENCE"
        boundary_statement = "RELATIVE_BOUNDARY_IN_CARRIER_OF_EACH_PAIRED_STRICT_SIGN_STRATUM_EQUALS_EXACT_GRAPH_SUPPORT"
    else:
        need(paired_relation_ref is None, "face graph local-only trace")
        need(radical_receipts == [], "explicit source factor has no radical side condition")
        zero_projection_rule = "EXPLICIT_t_EQUALS_ZERO_FULL_BASE_EQUIVALENCE"
        boundary_statement = "RELATIVE_BOUNDARY_IN_CURRENT_ONE_SIDED_CARRIER_OF_LOCAL_STRICT_SIGN_STRATUM_EQUALS_EXACT_GRAPH_SUPPORT"
    core = {
        "kind": "EXACT_SIGN_STRATUM_RELATIVE_CLOSURE_INCIDENCE_V1",
        "carrier_domain_ast_sha256": support["ast_sha256"]["carrier_domain_ast_sha256"],
        "base_domain_ast_sha256": support["ast_sha256"]["base_domain_ast_sha256"],
        "equation_ast_sha256": support["ast_sha256"]["equation_ast_sha256"],
        "exact_graph_support_ast_sha256": support["ast_sha256"]["exact_support_ast_sha256"],
        "exact_side_stratum_ast_sha256": object_sha(side_ast),
        "partition_branch_equivalence_certificate_sha256": branch_equivalence["certificate_sha256"],
        "factor_continuity_on_carrier": {
            "primitive_exact_AST_validated": True,
            "principal_square_root_side_conditions_ref": object_sha(radical_receipts),
            "all_C10_radical_side_conditions_strict": all(receipt["strictly_positive_on_carrier"] is True for receipt in radical_receipts),
        },
        "zero_projection_rule": zero_projection_rule,
        "strict_sign_stratum_is_relatively_open": True,
        "strict_side_and_graph_are_disjoint": True,
        "graph_subset_of_relative_side_closure_by_trace_atlas": True,
        "relative_closure_intersection_statement": "closure_in_carrier(exact_side_stratum) INTERSECT exact_graph_support = exact_graph_support",
        "boundary_containment_by_continuity": "relative_boundary(strict_sign_stratum) SUBSET factor_zero_set",
        "reverse_containment_by_trace_atlas": "exact_graph_support SUBSET relative_boundary(strict_sign_stratum)",
        "boundary_statement": boundary_statement,
        "paired_opposite_side_relation_ref": paired_relation_ref,
        "trace_atlas_sha256": object_sha(trace_atlas),
        "closure_incidence_complete": True,
    }
    return {**core, "certificate_sha256": object_sha(core)}


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


def producer_record() -> dict[str, Any]:
    info = os.stat(__file__, follow_symlinks=False)
    need(stat.S_ISREG(info.st_mode) and info.st_nlink == 1, "producer identity")
    descriptor = os.open(__file__, os.O_RDONLY | os.O_NOFOLLOW | os.O_CLOEXEC)
    try:
        opened = os.fstat(descriptor)
        need(identity(opened) == identity(info), "producer race")
        digest = hash_fd(descriptor)
        need(digest == hash_fd(descriptor), "producer digest")
        return {"filename": Path(__file__).name, "size": info.st_size, "sha256": digest}
    finally:
        os.close(descriptor)


def build() -> tuple[dict[str, Any], bytes]:
    with Snapshot() as snapshot:
        bind_manifest(snapshot, "C10_MANIFEST", ("C10_RESULT", "C10_SUPPORT", "C10_IDENTITY"))
        bind_manifest(snapshot, "C11_MANIFEST", ("C11_RESULT", "C11_DISPOSITION"))
        bind_manifest(snapshot, "C9_MANIFEST", ("C9_RESULT", "C9_GRAPH", "C9_RELATION"))
        bind_manifest(snapshot, "C7_MANIFEST", ("C7_PHYSICAL",))
        bind_manifest(snapshot, "C4_MANIFEST", ("C4_LEDGER",))
        bind_manifest(snapshot, "R235_MANIFEST", ("R235_CERT",))
        bind_manifest(snapshot, "R236_MANIFEST", ("R236_CERT",))
        bind_manifest(snapshot, "R248_MANIFEST", ("R248_CERT",))

        c9_result = closed_document(snapshot, "C9_RESULT")
        c10_result = closed_document(snapshot, "C10_RESULT")
        c11_result = closed_document(snapshot, "C11_RESULT")
        need(c9_result["audit_census"]["remaining_one_sided_trace_rows"] == 10_118, "C9 side denominator")
        need(all(value == 0 for value in c9_result["formal_credit"].values()), "C9 zero credit")
        need(c10_result["support_census"]["exact_G2_feature_support_AST_rows"] == 5_264, "C10 support census")
        need(c10_result["support_census"]["R235_target_internal_cut_root_descriptors"] == 8_392, "C10 target cut-root census")
        need(c10_result["identity_census"]["PRESERVE_EXISTING_MEMBER_ID"] == 5_264, "C10 identity census")
        need(c10_result["scoped_credit"] == {"exact_G2_feature_support_AST": 5_264, "member_natural_key_preservation": 5_264}, "C10 scoped credit")
        need(all(value == 0 for value in c10_result["formal_credit"].values()), "C10 downstream zero")
        need(c11_result["disposition_census"]["positive_graph_side_relations"] == 10_118, "C11 relation census")
        need(c11_result["disposition_census"]["CANDIDATE_READY_ROUTING"] == 9_950, "C11 ready census")
        need(c11_result["disposition_census"]["BLOCKED"] == 168, "C11 blocked census")
        need(all(value == 0 for value in c11_result["formal_credit"].values()), "C11 zero credit")

        c9_graphs: dict[str, dict[str, Any]] = {}
        for row in jsonl_rows(snapshot, "C9_GRAPH"):
            need(row["graph_id"] not in c9_graphs, "C9 graph uniqueness")
            c9_graphs[row["graph_id"]] = row
        need(len(c9_graphs) == 5_264, "C9 graph exhaustion")

        supports: dict[str, dict[str, Any]] = {}
        for row in jsonl_rows(snapshot, "C10_SUPPORT"):
            graph_id = row["graph_id"]
            need(graph_id not in supports and graph_id in c9_graphs, "C10 support uniqueness")
            need(row["C9_graph_ref"] == row_ref(c9_graphs[graph_id]), "C10-C9 graph binding")
            need(row["ast_sha256"]["carrier_domain_ast_sha256"] == object_sha(row["carrier_domain_ast"]), "C10 carrier hash")
            need(row["ast_sha256"]["base_domain_ast_sha256"] == object_sha(row["base_domain_ast"]), "C10 base hash")
            need(row["ast_sha256"]["equation_ast_sha256"] == object_sha(row["equation_ast"]), "C10 equation hash")
            need(row["ast_sha256"]["exact_support_ast_sha256"] == object_sha(row["exact_support_ast"]), "C10 support hash")
            need(
                row["exact_support_ast"]
                == and_ast(row["carrier_domain_ast"], row["base_domain_ast"], row["equation_ast"]),
                "C10 exact graph support conjunction",
            )
            need(row["scoped_credit"] == {"exact_G2_feature_support_AST": 1, "member_natural_key_preservation": 0}, "C10 support row scope")
            need(all(value == 0 for value in row["downstream_nonpromotion"].values()), "C10 support row zero")
            need(
                row["support_properties"]["nonempty"] is True
                and row["support_properties"]["connected"] is True
                and row["support_properties"]["one_graph_point_per_exact_base_point"] is True,
                "C10 graph support properties",
            )
            for name in ("carrier_domain_ast", "base_domain_ast", "equation_ast", "exact_support_ast"):
                validate_primitive_ast(row[name], "C10:" + graph_id + ":" + name)
            supports[graph_id] = row
        need(len(supports) == 5_264, "C10 support exhaustion")

        identities: dict[str, dict[str, Any]] = {}
        for row in jsonl_rows(snapshot, "C10_IDENTITY"):
            graph_id = row["graph_id"]
            need(graph_id not in identities and graph_id in supports, "C10 identity uniqueness")
            validate_c10_identity(row, supports[graph_id])
            identities[graph_id] = row
        need(set(identities) == set(supports), "C10 identity exhaustion")

        c11_by_c9_relation: dict[str, dict[str, Any]] = {}
        for row in jsonl_rows(snapshot, "C11_DISPOSITION"):
            c9_row_id = row["C9_relation_ref"]["row_id"]
            need(c9_row_id not in c11_by_c9_relation, "C11 routing relation uniqueness")
            c11_by_c9_relation[c9_row_id] = row
        need(len(c11_by_c9_relation) == 10_118, "C11 routing exhaustion")

        c7_rows: dict[str, dict[str, Any]] = {}
        for row in jsonl_rows(snapshot, "C7_PHYSICAL"):
            need(row["row_id"] not in c7_rows, "C7 relation uniqueness")
            c7_rows[row["row_id"]] = row
        need(len(c7_rows) == 15_392, "C7 physical exhaustion")

        positive_relations: list[dict[str, Any]] = []
        relations_by_graph: dict[str, list[dict[str, Any]]] = defaultdict(list)
        relation_count = 0
        for row in jsonl_rows(snapshot, "C9_RELATION"):
            need(row["mechanical_relation_ordinal"] == relation_count, "C9 relation order")
            relation_count += 1
            if row["incidence_role"] == "GRAPH_TO_SIDE" and row["positive_graph_physical_relation_candidate"] == 1:
                need(row["disposition"] == "EXACT_ONE_SIDED_SIGN_STRATUM_AND_TRACE_PENDING", "C9 pending side state")
                positive_relations.append(row)
                relations_by_graph[row["graph_id"]].append(row)
        need(relation_count == 15_392 and len(positive_relations) == 10_118, "C9 relation census")

        r235_document = legacy_document(snapshot, "R235_CERT")
        r235_rows = r235_document["result"]["single_endpoint_graph_partition_rows"]
        r235_by_graph = {row["endpoint_graph_partition_row_id"]: row for row in r235_rows}
        need(len(r235_rows) == len(r235_by_graph) == 38_328, "R235 partition exhaustion")

        r236_document = legacy_document(snapshot, "R236_CERT")
        r236_rows = r236_document["result"]["double_endpoint_partition_rows"]
        r236_by_id = {
            row["double_endpoint_partition_row_id"]: (ordinal, row)
            for ordinal, row in enumerate(r236_rows)
        }
        need(len(r236_rows) == len(r236_by_id) == 16, "R236 partition exhaustion")

        c4_by_source_inventory: dict[str, dict[str, Any]] = {}
        for row in jsonl_rows(snapshot, "C4_LEDGER"):
            source_inventory = row["canonical_input_commitment"]["B1G0_source_graph_row"][1]
            need(source_inventory not in c4_by_source_inventory, "C4 source uniqueness")
            c4_by_source_inventory[source_inventory] = row
        need(len(c4_by_source_inventory) == 16, "C4 bridge exhaustion")

        r248_document = legacy_document(snapshot, "R248_CERT")
        r248_rows = r248_document["result"]["formal_wall_positive_volume_bulk_ledger"]["rows"]
        r248_by_id = {row["wall_bulk_node_id"]: row for row in r248_rows}
        need(len(r248_rows) == len(r248_by_id) == 88_936, "R248 bulk exhaustion")

        # Target rows must arrive as the exact absent/present pair.  The partner
        # reference makes the common-boundary claim pair-local and auditable.
        target_partner: dict[str, dict[str, Any]] = {}
        for graph_id, relations in relations_by_graph.items():
            graph = c9_graphs[graph_id]
            if graph["graph_class"] != "R235_TARGET_POSITIVE_PARTIAL_BASE":
                continue
            need(len(relations) == 2, "R235 target relation pair")
            by_role: dict[str, dict[str, Any]] = {}
            for relation in relations:
                c7 = c7_rows[relation["C7_relation_row_id"]]
                role = c7["incidence_statement_ast"]["side_role"]
                need(role in {"EVENT_ABSENT", "EVENT_PRESENT"} and role not in by_role, "R235 target paired roles")
                by_role[role] = relation
            need(set(by_role) == {"EVENT_ABSENT", "EVENT_PRESENT"}, "R235 target role exhaustion")
            target_partner[by_role["EVENT_ABSENT"]["row_id"]] = by_role["EVENT_PRESENT"]
            target_partner[by_role["EVENT_PRESENT"]["row_id"]] = by_role["EVENT_ABSENT"]
        need(len(target_partner) == 8_864, "R235 target paired relation exhaustion")

        output_rows: list[dict[str, Any]] = []
        class_role_census: Counter[tuple[str, str]] = Counter()
        trace_chart_census: Counter[str] = Counter()
        side_member_ids: set[str] = set()
        relation_ids: set[str] = set()

        for relation in positive_relations:
            graph_id = relation["graph_id"]
            graph = c9_graphs[graph_id]
            need(relation["graph_domain_audit_ref"] == row_ref(graph), "C9 relation graph binding")
            graph_class = graph["graph_class"]
            c7 = c7_rows.get(relation["C7_relation_row_id"])
            need(c7 is not None and c7["row_sha256"] == relation["C7_relation_row_sha256"], "C9-C7 row binding")
            need(c7["graph_id"] == graph_id and c7["member_id"] == relation["member_id"] and c7["incidence_role"] == "GRAPH_TO_SIDE", "C7 relation subject")
            statement = c7["incidence_statement_ast"]
            need(statement["ast_kind"] == "GRAPH_SIDE_INCIDENCE_STATEMENT" and statement["proved"] is False, "C7 pending incidence")
            side_role = statement["side_role"]
            routing = c11_by_c9_relation.get(relation["row_id"])
            need(routing is not None, "C11 routing binding")
            need(
                routing["C9_relation_ref"] == row_ref(relation)
                and routing["graph_id"] == graph_id
                and routing["side_member_id"] == relation["member_id"]
                and routing["side_role"] == side_role,
                "C11 routing subject boundary",
            )
            support = supports[graph_id]
            identity_row = identities[graph_id]
            need(support["graph_class"] == graph_class and support["sheet_member_id"] == graph["sheet_member_id"], "C10 graph subject")
            factor = exact_factor(support)
            partition_ref: dict[str, Any]
            side_identity: dict[str, Any]
            eta: int
            desired_sign: int
            trace: dict[str, Any]
            partner_ref: dict[str, str] | None = None

            if graph_class in {"R235_TARGET_POSITIVE_PARTIAL_BASE", "R235_SOURCE_EXACT_FACE_FULL_BASE"}:
                partition = r235_by_graph.get(graph_id)
                need(partition is not None, "R235 graph partition")
                validate_r235(partition, graph_id)
                eta = sign_number(partition["fixed_endpoint_factor_sign"])
                need(side_role in {"EVENT_ABSENT", "EVENT_PRESENT"}, "R235 side role")
                desired_sign = relation_desired_sign(side_role)
                signature = partition["event_absent_signature" if side_role == "EVENT_ABSENT" else "event_present_signature"]
                bulk = r248_by_id.get(relation["member_id"])
                need(bulk is not None, "R235 side member in R248")
                side_identity = validate_r248_bulk(
                    bulk,
                    relation["member_id"],
                    partition["Round220_split_interface_id"],
                    "ROUND235_SINGLE_ENDPOINT_GRAPH_BRANCH",
                    graph_id,
                    side_role,
                    signature,
                )
                expected_proof_kind = {
                    "EVENT_ABSENT": "ROUND235_STRICT_MONOTONE_GRAPH_ABSENT_OPEN_SIDE",
                    "EVENT_PRESENT": "ROUND235_STRICT_MONOTONE_GRAPH_PRESENT_OPEN_SIDE",
                }[side_role]
                need(bulk["positive_volume_proof_kind"] == expected_proof_kind, "R248 R235 branch semantics")
                partition_ref = {
                    "kind": "R235_SINGLE_ENDPOINT_GRAPH_PARTITION_ROW",
                    "row_id": graph_id,
                    "full_row_sha256": object_sha(partition),
                    "Round220_split_interface_id": partition["Round220_split_interface_id"],
                    "active_endpoint_factor": partition["active_endpoint_factor"],
                    "fixed_endpoint_factor_sign": partition["fixed_endpoint_factor_sign"],
                    "active_factor_strict_t_derivative_sign": partition["active_factor_strict_t_derivative_sign"],
                    "transition_event": partition["transition_event"],
                    "transition_event_order_position": partition["transition_event_order_position"],
                    "candidate_time_strict_against_existing_event_count": partition["candidate_time_strict_against_existing_event_count"],
                }
                if graph_class == "R235_TARGET_POSITIVE_PARTIAL_BASE":
                    need(partition["active_endpoint_factor"] == "target", "R235 target factor")
                    need(
                        partition["active_factor_strict_t_derivative_sign"]
                        == support["monotone_graph_certificate"]["strict_t_derivative_proof"]["strict_t_derivative_sign"],
                        "R235-C10 target derivative binding",
                    )
                    partner_ref = row_ref(target_partner[relation["row_id"]])
                    trace = target_trace_atlas(support, eta, desired_sign)
                else:
                    need(partition["active_endpoint_factor"] == "source", "R235 source factor")
                    monotone = support["monotone_graph_certificate"]
                    need(monotone["kind"] == "EXPLICIT_T_EQUALS_ZERO_FULL_BASE_GRAPH" and q(monotone["strict_t_derivative_exact"]) == Q(9, 25), "R235 source exact factor")
                    need(partition["active_factor_strict_t_derivative_sign"] == "STRICT_POSITIVE", "R235-C10 source derivative binding")
                    bounds = carrier_bounds(support["carrier_domain_ast"])
                    zero_face = "LOWER" if bounds["t"][0] == 0 else "UPPER"
                    need(graph["exact_graph_domain_receipt"]["zero_face"] == zero_face, "C9-C10 source zero face")
                    inward_direction = 1 if zero_face == "LOWER" else -1
                    # The other R235 branch lives in the adjacent carrier and
                    # is deliberately left for the 152-row extension theorem.
                    if desired_sign != eta * inward_direction:
                        continue
                    trace = face_trace_atlas("R235_SOURCE_EXACT_INWARD_FACE_TRACE_V1", zero_face, eta, desired_sign, support["carrier_domain_ast"])
            elif graph_class == "R235D_SOURCE_EXACT_FACE_FULL_BASE":
                # Only the already-materialized local SAME_SIGN relation is in
                # scope.  NEGATIVE_TO_POSITIVE requires outside-domain data.
                if side_role != "source:SAME_SIGN_EVENT_ABSENT":
                    continue
                desired_sign = relation_desired_sign(side_role)
                bridge = c4_by_source_inventory.get(graph["graph_inventory_row_id"])
                need(bridge is not None, "R235D C4 bridge")
                reconstruction = bridge["semantic_reconstruction"]
                need(reconstruction["source_zero_set"] == "EXACT_FACE_GRAPH_t_EQUALS_0" and reconstruction["complete_domain_partition_verified"] is True, "R235D source graph theorem")
                need(q(reconstruction["source_t_derivative_exact_interval"]["lower"]) == q(reconstruction["source_t_derivative_exact_interval"]["upper"]) == Q(9, 25), "R235D exact source derivative")
                r236_ref = bridge["canonical_input_commitment"]["R236_double_endpoint_partition_row"]
                r236_entry = r236_by_id.get(r236_ref[1])
                need(r236_entry is not None, "C4-R236 row existence")
                r236_ordinal, r236 = r236_entry
                need(r236_ref[0] == r236_ordinal and object_sha(r236) == r236_ref[2], "C4-R236 direct ordinal/id/hash binding")
                need(r236["Round220_split_interface_id"] == bridge["Round220_split_interface_id"] and r236["source_factor_strict_t_derivative_sign"] == "STRICT_POSITIVE", "R236 source derivative")
                need(
                    bridge["canonical_input_commitment"]["B1G0_source_graph_row"][1] == graph["graph_inventory_row_id"]
                    and bridge["canonical_input_commitment"]["R236_double_endpoint_partition_row"][1] == r236["double_endpoint_partition_row_id"],
                    "C9-C4-R236 source graph chain",
                )
                c10_c4_ref = support["legacy_source_refs"]["C4_exact_source_semantic_authority"]
                need(
                    c10_c4_ref["ordinal"] == bridge["bridge_ordinal"]
                    and c10_c4_ref["row_id"] == bridge["bridge_row_id"]
                    and c10_c4_ref["row_sha256"] == bridge["row_sha256"]
                    and c10_c4_ref["full_row_sha256"] == object_sha(bridge),
                    "C10-C4 exact source authority binding",
                )
                eta = sign_number(reconstruction["target_factor_fixed_sign"])
                signature = r236["same_sign_event_absent_signature"]
                bulk = r248_by_id.get(relation["member_id"])
                need(bulk is not None, "R235D side member in R248")
                side_identity = validate_r248_bulk(
                    bulk,
                    relation["member_id"],
                    r236["Round220_split_interface_id"],
                    "ROUND236_DOUBLE_ENDPOINT_ARRANGEMENT_BRANCH",
                    r236["double_endpoint_partition_row_id"],
                    "SAME_SIGN_EVENT_ABSENT",
                    signature,
                )
                need(bulk["positive_volume_proof_kind"] == "ROUND236_TWO_ENDPOINT_GRAPHS_SAME_SIGN_OPEN_REGION", "R248 R235D branch semantics")
                need(c7["source_incidence_row_id"] == bridge["canonical_input_commitment"]["B1G0_source_shared_side_row"][1], "R235D shared relation binding")
                partition_ref = {
                    "kind": "R236_DOUBLE_ENDPOINT_PARTITION_PLUS_C4_SOURCE_BRIDGE",
                    "row_id": r236["double_endpoint_partition_row_id"],
                    "ordinal": r236_ordinal,
                    "full_row_sha256": object_sha(r236),
                    "C4_bridge_ref": {"row_id": bridge["bridge_row_id"], "row_sha256": bridge["row_sha256"]},
                    "Round220_split_interface_id": r236["Round220_split_interface_id"],
                    "active_endpoint_factor": "source",
                    "fixed_target_factor_sign": reconstruction["target_factor_fixed_sign"],
                    "source_factor_strict_t_derivative_sign": r236["source_factor_strict_t_derivative_sign"],
                }
                trace = face_trace_atlas(
                    "R235D_SOURCE_EXACT_INWARD_SHARED_FACE_TRACE_V1",
                    reconstruction["source_zero_face"],
                    eta,
                    desired_sign,
                    support["carrier_domain_ast"],
                )
            else:
                continue

            need(
                routing["candidate_ready_routing"] is True
                and routing["disposition"] == "CANDIDATE_READY_ROUTING"
                and routing["local_graph_side_physical_incidence_proved"] is False
                and routing["one_sided_trace_proved"] is False
                and routing["representation_pullback_proved"] is False
                and routing["DSU_edge_or_union_authorized"] is False
                and len(routing["missing_theorem_authority"]) > 0
                and all(value == 0 for value in routing["formal_credit"].values()),
                "C11 selected routing zero-credit boundary",
            )

            sign_ast = sign_relation_ast(factor, eta, "GT" if desired_sign > 0 else "LT")
            side_ast = and_ast(support["carrier_domain_ast"], sign_ast)
            validate_primitive_ast(side_ast, "exact side stratum:" + relation["row_id"])
            branch_equivalence = branch_equivalence_certificate(
                graph_class,
                side_role,
                partition_ref,
                side_identity,
                eta,
                desired_sign,
                side_ast,
            )
            closure = closure_certificate(graph_class, support, side_ast, branch_equivalence, trace, partner_ref)
            need(closure["closure_incidence_complete"] is True and trace["every_graph_point_has_a_side_approach_path"] is True, "local theorem completeness")
            need(relation["row_id"] not in relation_ids and relation["member_id"] not in side_member_ids, "scoped relation/member uniqueness")
            relation_ids.add(relation["row_id"])
            side_member_ids.add(relation["member_id"])
            class_role_census[(graph_class, side_role)] += 1
            trace_chart_census[graph_class] += len(trace["charts"])

            core = {
                "schema": ROW_SCHEMA,
                "row_id": PREFIX + ":kernel-row:" + object_sha([relation["row_id"], relation["member_id"]]),
                "kernel_ordinal": len(output_rows),
                "graph_id": graph_id,
                "graph_class": graph_class,
                "sheet_member_id": support["sheet_member_id"],
                "side_member_id": relation["member_id"],
                "side_role": side_role,
                "C9_relation_ref": row_ref(relation),
                "C7_mechanical_relation_ref": row_ref(c7),
                "C10_exact_graph_support_ref": row_ref(support),
                "C10_sheet_member_identity_ref": row_ref(identity_row),
                "C11_routing_disposition_ref": row_ref(routing),
                "partition_semantic_ref": partition_ref,
                "R248_side_member_identity": side_identity,
                "coordinate_parameter": "TPS",
                "fixed_other_endpoint_eta": eta,
                "desired_eta_times_active_factor_sign": "STRICT_POSITIVE" if desired_sign > 0 else "STRICT_NEGATIVE",
                "exact_side_stratum_ast": side_ast,
                "exact_side_stratum_ast_sha256": object_sha(side_ast),
                "exact_graph_boundary_ast_sha256": support["ast_sha256"]["exact_support_ast_sha256"],
                "partition_branch_to_side_member_equivalence_certificate": branch_equivalence,
                "closure_incidence_certificate": closure,
                "one_sided_trace_certificate": trace,
                "scoped_credit": {
                    "local_graph_side_physical_incidence": 1,
                    "one_sided_trace": 1,
                },
                "strict_nonpromotion": {
                    "R248_positive_volume_label_used_as_support_geometry": False,
                    "graph_sheet_set_equality_proved": False,
                    "representation_pullback_proved": False,
                    "DSU_edge_or_union_authorized": False,
                    **DOWNSTREAM_ZERO,
                },
            }
            output_rows.append(closed_row(core))

        need(len(output_rows) == len(relation_ids) == len(side_member_ids) == 9_422, "C11a scoped row exhaustion")
        expected = {
            ("R235_TARGET_POSITIVE_PARTIAL_BASE", "EVENT_ABSENT"): 4_432,
            ("R235_TARGET_POSITIVE_PARTIAL_BASE", "EVENT_PRESENT"): 4_432,
            ("R235_SOURCE_EXACT_FACE_FULL_BASE", "EVENT_ABSENT"): 336,
            ("R235_SOURCE_EXACT_FACE_FULL_BASE", "EVENT_PRESENT"): 216,
            ("R235D_SOURCE_EXACT_FACE_FULL_BASE", "source:SAME_SIGN_EVENT_ABSENT"): 6,
        }
        need(class_role_census == expected, "C11a class-role census")
        need(trace_chart_census["R235_SOURCE_EXACT_FACE_FULL_BASE"] == 552, "R235 source trace chart census")
        need(trace_chart_census["R235D_SOURCE_EXACT_FACE_FULL_BASE"] == 6, "R235D trace chart census")
        need(trace_chart_census["R235_TARGET_POSITIVE_PARTIAL_BASE"] == 8_864 + 2 * 8_392, "R235 target trace chart census")

        ledger_wire, ledger_plain = gzip_rows(output_rows)
        ledger_descriptor = {
            "filename": LEDGER_NAME,
            "compression": "gzip-level9-mtime-zero",
            "row_schema": ROW_SCHEMA,
            "row_count": len(output_rows),
            "compressed_size": len(ledger_wire),
            "compressed_sha256": hashlib.sha256(ledger_wire).hexdigest(),
            "uncompressed_size": len(ledger_plain),
            "uncompressed_sha256": hashlib.sha256(ledger_plain).hexdigest(),
            "ordered_row_ids_sha256": sequence_sha(row["row_id"] for row in output_rows),
            "ordered_row_hashes_sha256": sequence_sha(row["row_sha256"] for row in output_rows),
            "ordered_rows_sha256": sequence_sha(output_rows),
        }
        body = {
            "schema": SCHEMA,
            "status": STATUS,
            "producer_source": producer_record(),
            "source_pins": [pin.__dict__ for pin in PINS],
            "upstream_seal_bindings": {
                "C10_manifest_sha256": PIN_BY_ROLE["C10_MANIFEST"].sha256,
                "C11_routing_manifest_sha256": PIN_BY_ROLE["C11_MANIFEST"].sha256,
            },
            "scope_census": {
                "C9_positive_graph_side_relation_denominator": 10_118,
                "scoped_kernel_rows": 9_422,
                "R235_target_rows": 8_864,
                "R235_source_inward_face_rows": 552,
                "R235D_source_same_sign_inward_face_rows": 6,
                "excluded_R235_adjacent_domain_rows": 152,
                "excluded_R235D_outside_domain_rows": 16,
                "excluded_R242_rows": 528,
            },
            "class_role_census": {"|".join(key): value for key, value in sorted(class_role_census.items())},
            "trace_chart_census": dict(sorted(trace_chart_census.items())),
            "scoped_credit": {
                "local_graph_side_physical_incidence": 9_422,
                "one_sided_trace": 9_422,
            },
            "formal_downstream_credit": DOWNSTREAM_ZERO,
            "strict_nonpromotion": {
                "producer_output_requires_independent_verification_and_seal": True,
                "152_R235_adjacent_domain_rows_closed": False,
                "16_R235D_outside_domain_rows_closed": False,
                "R242_rows_closed_here": False,
                "graph_sheet_set_equality_proved": False,
                "representation_pullback_proved": False,
                "DSU_edge_or_union_authorized": False,
                "normalized_support_sealed": False,
                "B1A_permitted": False,
                "B2_permitted": False,
                "maximality_permitted": False,
                "CM2": "NO-GO_FOR_CLAIM",
            },
            "kernel_ledger": ledger_descriptor,
            "required_next": {
                "independent_verifier_and_coherent_attacks": True,
                "cold_replay_and_manifest_first": True,
                "close_152_R235_adjacent_domain_traces": True,
                "close_16_R235D_outside_domain_traces": True,
                "prove_graph_sheet_set_equality_before_any_edge_promotion": True,
            },
            "seed_serialized_or_semantically_used": False,
        }
        result = {**body, "result_sha256": object_sha(body)}
        snapshot.final()
    return result, ledger_wire


def write_once(directory: Path, filename: str, payload: bytes) -> None:
    path = directory / filename
    need(not path.exists(), "publish no-clobber:" + filename)
    descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW | os.O_CLOEXEC, 0o600)
    try:
        offset = 0
        while offset < len(payload):
            offset += os.write(descriptor, payload[offset:])
        os.fsync(descriptor)
    finally:
        os.close(descriptor)
    info = os.stat(path, follow_symlinks=False)
    need(stat.S_ISREG(info.st_mode) and info.st_nlink == 1 and info.st_size == len(payload), "published file:" + filename)


def main() -> int:
    need(sys.flags.isolated == 1 and sys.dont_write_bytecode is True, "python -I -B")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--print-result", action="store_true")
    parser.add_argument("--candidate-dir")
    parser.add_argument("--publish", action="store_true")
    arguments = parser.parse_args()
    need(sum((arguments.print_result, arguments.candidate_dir is not None, arguments.publish)) == 1, "exactly one mode")
    result, ledger_wire = build()
    result_wire = canonical(result)
    if arguments.print_result:
        sys.stdout.buffer.write(result_wire + b"\n")
        return 0
    directory = ROOT if arguments.publish else Path(arguments.candidate_dir).resolve()
    if not arguments.publish:
        need(os.path.commonpath((str(directory), str(ROOT.resolve()))) != str(ROOT.resolve()), "candidate outside deliverables")
        directory.mkdir(mode=0o700, parents=False, exist_ok=False)
    records = []
    for filename, payload in ((LEDGER_NAME, ledger_wire), (RESULT_NAME, result_wire)):
        write_once(directory, filename, payload)
        records.append({"filename": filename, "size": len(payload), "sha256": hashlib.sha256(payload).hexdigest()})
    for record in reversed(records):
        info = os.stat(directory / record["filename"], follow_symlinks=False)
        need(stat.S_ISREG(info.st_mode) and info.st_nlink == 1 and info.st_size == record["size"], "reverse publication identity")
        descriptor = os.open(directory / record["filename"], os.O_RDONLY | os.O_NOFOLLOW | os.O_CLOEXEC)
        try:
            need(hash_fd(descriptor) == record["sha256"], "reverse publication digest")
        finally:
            os.close(descriptor)
    print(json.dumps({"status": result["status"], "result_sha256": result["result_sha256"], "published_result_last": True, "files": records}, sort_keys=True, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
