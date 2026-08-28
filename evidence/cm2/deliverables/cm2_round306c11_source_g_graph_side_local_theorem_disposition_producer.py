#!/usr/bin/env python3
"""Produce the scoped C11 graph-to-side zero-credit routing census.

This producer classifies the 10,118 live graph-to-side mechanical relations.
The 9,950 rows called candidate-ready are routing classifications only:
historical R248/R245 receipts do not supply an exact side carrier,
closure-incidence theorem, or one-sided collar/common-boundary trace.  Thus
this artifact proves no local physical incidence or trace and grants no
downstream credit.
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
PREFIX: Final = "cm2_round306c11_source_g_graph_side_local_theorem_disposition"
SCHEMA: Final = "cm2.round306c11.source-g-graph-side-local-theorem-disposition.v1"
DISPOSITION_ROW_SCHEMA: Final = SCHEMA + ".disposition-row.v1"
READY_ROW_SCHEMA: Final = SCHEMA + ".candidate-ready-routing-row.v1"
BLOCKED_ROW_SCHEMA: Final = SCHEMA + ".blocked-row.v1"
REROUTE_ROW_SCHEMA: Final = SCHEMA + ".missing-local-shared-reroute-finding-row.v1"
DISPOSITION_LEDGER_NAME: Final = PREFIX + "_disposition_ledger.jsonl.gz"
READY_LEDGER_NAME: Final = PREFIX + "_ready_local_theorem_ledger.jsonl.gz"
BLOCKED_LEDGER_NAME: Final = PREFIX + "_blocked_ledger.jsonl.gz"
REROUTE_LEDGER_NAME: Final = PREFIX + "_missing_local_shared_reroute_findings.jsonl.gz"
RESULT_NAME: Final = PREFIX + "_result.json"
STATUS: Final = (
    "PASS_10118_GRAPH_SIDE_ROUTING_DISPOSITIONS__"
    "9950_CANDIDATE_READY_ROUTING__168_STRUCTURALLY_BLOCKED__"
    "10_MISSING_LOCAL_SHARED_REROUTE_FINDINGS__ZERO_LOCAL_THEOREM_AND_DOWNSTREAM_CREDIT"
)

C10_MANIFEST: Final = "cm2_round306c10_source_g_exact_graph_support_identity_rematerialization_manifest.sha256"
C10_RESULT: Final = "cm2_round306c10_source_g_exact_graph_support_identity_rematerialization_result.json"
C10_SUPPORT: Final = "cm2_round306c10_source_g_exact_graph_support_identity_rematerialization_exact_graph_support_ledger.jsonl.gz"
C10_IDENTITY: Final = "cm2_round306c10_source_g_exact_graph_support_identity_rematerialization_member_identity_disposition_ledger.jsonl.gz"
C9_MANIFEST: Final = "cm2_round306c9_source_g_g2_relation_admissibility_and_envelope_audit_manifest.sha256"
C9_RESULT: Final = "cm2_round306c9_source_g_g2_relation_admissibility_and_envelope_audit_result.json"
C9_GRAPH: Final = "cm2_round306c9_source_g_g2_relation_admissibility_and_envelope_audit_graph_domain_audit_ledger.jsonl.gz"
C9_RELATION: Final = "cm2_round306c9_source_g_g2_relation_admissibility_and_envelope_audit_relation_disposition_ledger.jsonl.gz"
C7_MANIFEST: Final = "cm2_round306c7_source_g_fresh_identity_support_mechanical_replay_manifest.sha256"
C7_PHYSICAL: Final = "cm2_round306c7_source_g_fresh_identity_support_mechanical_replay_physical_incidence_statement_ledger.jsonl.gz"
C6_MANIFEST: Final = "cm2_round306c6_source_g_corrected_g2_invalidation_fresh_dsu_freeze_manifest.sha256"
C6_COMPONENT: Final = "cm2_round306c6_source_g_corrected_g2_invalidation_fresh_dsu_freeze_member_component_ledger.jsonl.gz"
C5_MANIFEST: Final = "cm2_round306c5_source_g_corrected_g2_graph_semantic_classification_manifest.sha256"
C5_SEMANTIC: Final = "cm2_round306c5_source_g_corrected_g2_graph_semantic_classification_row_ledger.jsonl.gz"
C4_MANIFEST: Final = "cm2_round306c4_source_g_r235d_to_g2_orphan_graph_semantic_bridge_manifest.sha256"
C4_LEDGER: Final = "cm2_round306c4_source_g_r235d_to_g2_orphan_graph_semantic_bridge_row_ledger.jsonl.gz"
R235_MANIFEST: Final = "cm2_round235_source_g_single_endpoint_graph_word_key_partition_manifest.sha256"
R235_CERT: Final = "cm2_round235_source_g_single_endpoint_graph_word_key_partition_certificate.json"
R236_MANIFEST: Final = "cm2_round236_source_g_wall_residual_closure_and_root_key_partition_manifest.sha256"
R236_CERT: Final = "cm2_round236_source_g_wall_residual_closure_and_root_key_partition_certificate.json"
R242_MANIFEST: Final = "cm2_round242_source_g_outgoing_graph_existence_stratum_materialization_manifest.sha256"
R242_CERT: Final = "cm2_round242_source_g_outgoing_graph_existence_stratum_materialization_certificate.json"
R248_MANIFEST: Final = "cm2_round248_source_g_wall_finite_key_retained_quotient_manifest.sha256"
R248_CERT: Final = "cm2_round248_source_g_wall_finite_key_retained_quotient_certificate.json"
R245_MANIFEST: Final = "cm2_round245_source_g_retained_graph_mixed_sheet_quotient_manifest.sha256"
R245_CERT: Final = "cm2_round245_source_g_retained_graph_mixed_sheet_quotient_certificate.json"


@dataclass(frozen=True)
class Pin:
    role: str
    filename: str
    size: int
    sha256: str


# C10 sealed byte pins.
PINS: Final = (
    Pin("C10_MANIFEST", C10_MANIFEST, 1_431, "b7277863feb9edc5f35906b04af2a9a256becb7ee9f1f1df6558b897184029ca"),
    Pin("C10_RESULT", C10_RESULT, 9_468, "b188eaa6c4dee77e0fff13b4a48cec9f8b46d324e48e7927265807a0f2865b55"),
    Pin("C10_SUPPORT", C10_SUPPORT, 19_958_893, "b7b2b02653a404060364b788b3e0ac8693d2d9d8d1c45e6109ca7f4400c4080c"),
    Pin("C10_IDENTITY", C10_IDENTITY, 2_966_603, "5041df1ab4b5bf9e79984859f828c9fb69718f53bd62d2920d51ebea8b7ec9df"),
    Pin("C9_MANIFEST", C9_MANIFEST, 1_396, "8921fb3eadd5d8b4aec1afe3af91c938b2c5568e9f9ef3be64002e4146152d04"),
    Pin("C9_RESULT", C9_RESULT, 8_845, "31d8da4e4a3e6ad703bd24fd7456f801d3fd90293e171d9784b2280d393b76a8"),
    Pin("C9_GRAPH", C9_GRAPH, 2_488_534, "955d8930fc321ca4f2556d66af488e4b9391f91002b65ecf8eaace6fbd3a7d50"),
    Pin("C9_RELATION", C9_RELATION, 5_184_953, "0ffdec565560e1b44198285fea7e801ab7ed655d964d521b8693e95064744e71"),
    Pin("C7_MANIFEST", C7_MANIFEST, 2_184, "4e534e412a760d13fe7eb278ca063e86ac2a7164bbfdb3b14a3142219267c0c6"),
    Pin("C7_PHYSICAL", C7_PHYSICAL, 9_771_275, "e6450435f74f038f3de2ada64935fc1f72bec6eb4323f2dc5ad8069bf3ea490e"),
    Pin("C6_MANIFEST", C6_MANIFEST, 2_211, "d9c3261421a966f62eeb027517f0f0e58ab2f3f72d856fed5cdcced55ff158f2"),
    Pin("C6_COMPONENT", C6_COMPONENT, 213_125_489, "730a1501402d29f9689655b0093edd4d7e499f3a34c6b65e9f21ee6f3f5ffce2"),
    Pin("C5_MANIFEST", C5_MANIFEST, 1_193, "aefe82ef88c2ddf5f241d76e0f0f7483e230d68219ace6639f7389adbcb14134"),
    Pin("C5_SEMANTIC", C5_SEMANTIC, 78_082_824, "8f28efab9465440a0d6549f99a91d9b3997266f98a9c2eb06eda61ecdc42f333"),
    Pin("C4_MANIFEST", C4_MANIFEST, 1_177, "5550eb9cf4e474a8d08086062e28538e909f6e1c7e499ba10a78a2d24e683de6"),
    Pin("C4_LEDGER", C4_LEDGER, 101_147, "3b273e7637af99e19a23ec62a29999023d73aba9a901fe4311fc631aae0cc6db"),
    Pin("R235_MANIFEST", R235_MANIFEST, 566, "cf58b7d2f419ea252c3398665302fe6f5ff06436af20a56beaaa47e5ef822ea0"),
    Pin("R235_CERT", R235_CERT, 67_765_471, "e340fa1a071d85a36b54d10a45ae2fdb9d70b8c90f4c21f054c6fc9505e5e787"),
    Pin("R236_MANIFEST", R236_MANIFEST, 582, "28f6f6d2f5b0f10edba5cd473b4126a8fed098874849c2f579eadd92b30d324c"),
    Pin("R236_CERT", R236_CERT, 2_061_199, "b5b9ec358b4837a02218756a034440d8fbc2aa706ca421bedb28aaf785de0217"),
    Pin("R242_MANIFEST", R242_MANIFEST, 897, "6da30fe3f9438ec73dc9c7d1aac770d8e9730aa9564ab0c535f1596cdc09ef2f"),
    Pin("R242_CERT", R242_CERT, 13_734_655, "8d32c381e21c03aad6a531b7e5a527d295783b7e3e38baa1e6bcba20c40db22e"),
    Pin("R248_MANIFEST", R248_MANIFEST, 885, "b1ddedd01041e71b5c12fa4989726815c8685e6df77f54d9dbddda64aaf89e07"),
    Pin("R248_CERT", R248_CERT, 205_148_977, "fa48bdfb0056072f80c5809f57362c225f0beb40e1cc4c145f3f072335cdb311"),
    Pin("R245_MANIFEST", R245_MANIFEST, 897, "1aff29f3a42b618ca85e5a1d3c537307e32326f8d5092b82d4253a5bf6e1c4ac"),
    Pin("R245_CERT", R245_CERT, 20_683_081, "c76662f7cb068127f3612a3655ae720662eead9b9210b5757d771693149883c1"),
)
PIN_BY_ROLE: Final = {pin.role: pin for pin in PINS}

ZERO_DOWNSTREAM: Final = {
    "local_graph_side_physical_incidence": 0,
    "one_sided_trace": 0,
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

R235_MISSING_AUTHORITY: Final = [
    "EXACT_SIDE_CARRIER",
    "CLOSURE_INCIDENCE",
    "ONE_SIDED_COLLAR_OR_COMMON_BOUNDARY_TRACE",
]
R235D_MISSING_AUTHORITY: Final = list(R235_MISSING_AUTHORITY)
R242_MISSING_AUTHORITY: Final = [
    "COMPLETE_THREE_EDGE_R245_BINDING_IS_ROUTING_EVIDENCE_ONLY",
    "EXACT_SIDE_CARRIER",
    "CLOSURE_INCIDENCE",
    "ONE_SIDED_COLLAR_OR_COMMON_BOUNDARY_TRACE",
]


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True, allow_nan=False).encode("ascii")


def object_sha(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def identity(info: os.stat_result) -> tuple[int, ...]:
    return (info.st_dev, info.st_ino, info.st_mode, info.st_nlink, info.st_size, info.st_mtime_ns, info.st_ctime_ns)


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
        self.directory_descriptor = os.open(ROOT, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW | os.O_CLOEXEC)
        for pin in PINS:
            info = os.stat(pin.filename, dir_fd=self.directory_descriptor, follow_symlinks=False)
            need(stat.S_ISREG(info.st_mode) and info.st_nlink == 1 and info.st_size == pin.size, "pin identity:" + pin.role)
            file_descriptor = os.open(pin.filename, os.O_RDONLY | os.O_NOFOLLOW | os.O_CLOEXEC, dir_fd=self.directory_descriptor)
            opened = os.fstat(file_descriptor)
            need(identity(opened) == identity(info), "pin race:" + pin.role)
            need(hash_fd(file_descriptor) == hash_fd(file_descriptor) == pin.sha256, "pin digest:" + pin.role)
            self.file_descriptors[pin.role] = file_descriptor
            self.identities[pin.role] = identity(opened)
        return self

    def read(self, role: str) -> bytes:
        return read_fd(self.file_descriptors[role])

    def duplicate(self, role: str) -> int:
        duplicate = os.dup(self.file_descriptors[role])
        os.lseek(duplicate, 0, os.SEEK_SET)
        return duplicate

    def final(self) -> None:
        for pin in reversed(PINS):
            file_descriptor = self.file_descriptors[pin.role]
            need(identity(os.fstat(file_descriptor)) == self.identities[pin.role], "final fd:" + pin.role)
            need(identity(os.stat(pin.filename, dir_fd=self.directory_descriptor, follow_symlinks=False)) == self.identities[pin.role], "final path:" + pin.role)
            need(hash_fd(file_descriptor) == pin.sha256, "final digest:" + pin.role)

    def __exit__(self, *_: Any) -> None:
        for file_descriptor in self.file_descriptors.values():
            try:
                os.close(file_descriptor)
            except OSError:
                pass
        if self.directory_descriptor >= 0:
            os.close(self.directory_descriptor)


def jsonl_rows(snapshot: Snapshot, role: str) -> Iterator[dict[str, Any]]:
    duplicate = snapshot.duplicate(role)
    with os.fdopen(duplicate, "rb", closefd=True) as raw, gzip.GzipFile(fileobj=raw, mode="rb") as stream:
        for ordinal, line in enumerate(stream):
            row = json.loads(line)
            need(type(row) is dict and line == canonical(row) + b"\n", "canonical JSONL:" + role + ":" + str(ordinal))
            core = dict(row)
            claimed = core.pop("row_sha256", None)
            need(type(claimed) is str and claimed == object_sha(core), "row closure:" + role + ":" + str(ordinal))
            yield row


def closed_document(snapshot: Snapshot, role: str) -> dict[str, Any]:
    raw = snapshot.read(role)
    value = json.loads(raw)
    need(type(value) is dict and raw in (canonical(value), canonical(value) + b"\n"), "canonical document:" + role)
    core = dict(value)
    claimed = core.pop("result_sha256", None)
    need(type(claimed) is str and claimed == object_sha(core), "document closure:" + role)
    return value


def legacy_document(snapshot: Snapshot, role: str) -> dict[str, Any]:
    value = json.loads(snapshot.read(role))
    need(type(value) is dict and type(value.get("result")) is dict, "legacy document:" + role)
    need(value.get("result_sha256") == object_sha(value["result"]), "legacy closure:" + role)
    return value


def legacy_row(row: dict[str, Any], label: str) -> None:
    core = dict(row)
    claimed = core.pop("row_sha256", None)
    need(type(claimed) is str and claimed == object_sha(core), "legacy row closure:" + label)


def bind_manifest(snapshot: Snapshot, manifest_role: str, member_roles: tuple[str, ...]) -> None:
    entries: dict[str, str] = {}
    raw = snapshot.read(manifest_role)
    for line in raw.decode("ascii").splitlines():
        digest, marker, filename = line.partition("  ")
        normalized = Path(filename).name
        need(marker == "  " and len(digest) == 64 and normalized and normalized not in entries, "manifest syntax:" + manifest_role)
        need(filename in (normalized, "deliverables/" + normalized), "manifest legacy path normalization:" + manifest_role)
        int(digest, 16)
        entries[normalized] = digest
    for role in member_roles:
        pin = PIN_BY_ROLE[role]
        need(entries.get(pin.filename) == pin.sha256, "manifest member:" + manifest_role + ":" + role)


def producer_record() -> dict[str, Any]:
    info = os.stat(__file__, follow_symlinks=False)
    need(stat.S_ISREG(info.st_mode) and info.st_nlink == 1, "producer identity")
    file_descriptor = os.open(__file__, os.O_RDONLY | os.O_NOFOLLOW | os.O_CLOEXEC)
    try:
        opened = os.fstat(file_descriptor)
        need(identity(opened) == identity(info), "producer race")
        digest = hash_fd(file_descriptor)
        need(digest == hash_fd(file_descriptor), "producer digest")
        return {"filename": Path(__file__).name, "size": info.st_size, "sha256": digest}
    finally:
        os.close(file_descriptor)


def row_ref(row: dict[str, Any], id_field: str = "row_id") -> dict[str, str]:
    return {"row_id": row[id_field], "row_sha256": row["row_sha256"]}


def closed_row(core: dict[str, Any]) -> dict[str, Any]:
    return {**core, "row_sha256": object_sha(core)}


def q(value: Any) -> Q:
    if type(value) is str:
        return Q(value)
    if type(value) is dict and set(value) == {"numerator", "denominator"}:
        return Q(value["numerator"], value["denominator"])
    raise Rejected("non-exact rational")


def positive_box(box: list[Any], dimension: int, label: str) -> Q:
    need(type(box) is list and len(box) == 2 * dimension, "box shape:" + label)
    volume = Q(1)
    for axis in range(dimension):
        lower = q(box[2 * axis])
        upper = q(box[2 * axis + 1])
        need(lower < upper, "positive interval:" + label + ":" + str(axis))
        volume *= upper - lower
    return volume


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


def ledger_descriptor(filename: str, row_schema: str, rows: list[dict[str, Any]], wire: bytes, plain: bytes) -> dict[str, Any]:
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


def component_ref(row: dict[str, Any]) -> dict[str, str]:
    return {
        "row_id": row["row_id"],
        "row_sha256": row["row_sha256"],
        "member_id": row["registry_member_id"],
        "base_root_id": row["new_base_root_id"],
        "fresh_component_id": row["fresh_component_id"],
    }


def local_credit(_candidate_ready: bool) -> dict[str, int]:
    return dict(ZERO_DOWNSTREAM)


def validate_results(c9: dict[str, Any], c10: dict[str, Any]) -> None:
    need(c9["audit_census"]["positive_graph_domain_audit_rows"] == 5_264, "C9 graph census")
    need(c9["audit_census"]["mechanical_relation_statement_rows"] == 15_392, "C9 relation census")
    need(c9["audit_census"]["remaining_one_sided_trace_rows"] == 10_118, "C9 side denominator")
    need(all(value == 0 for value in c9["formal_credit"].values()), "C9 zero credit")
    need(c10["support_census"]["exact_G2_feature_support_AST_rows"] == 5_264, "C10 support census")
    need(c10["C9_denominator_preserved"]["remaining_one_sided_trace_rows"] == 10_118, "C10 denominator")
    need(c10["scoped_credit"] == {"exact_G2_feature_support_AST": 5_264, "member_natural_key_preservation": 5_264}, "C10 scoped credit")
    need(all(value == 0 for value in c10["formal_credit"].values()), "C10 downstream zero")
    need(c10["strict_nonpromotion"]["graph_to_sheet_set_equality_proved"] is False, "C10 graph-sheet boundary")
    need(c10["strict_nonpromotion"]["physical_incidence_proved"] is False, "C10 physical boundary")


def validate_r235_partition(row: dict[str, Any], graph_id: str) -> None:
    need(row["endpoint_graph_partition_row_id"] == graph_id, "R235 graph id")
    need(row["endpoint_graph_dimension"] == 2, "R235 graph dimension")
    need(row["local_finite_exact_key_partition_credit"] == 1, "R235 local partition")
    need(row["distinct_side_exact_key_count"] == 2, "R235 side key count")
    need(row["fixed_endpoint_factor_sign"] in ("STRICT_POSITIVE", "STRICT_NEGATIVE"), "R235 fixed sign")
    need(row["active_factor_strict_t_derivative_sign"] in ("STRICT_POSITIVE", "STRICT_NEGATIVE"), "R235 active derivative")


def validate_r248_bulk(
    row: dict[str, Any],
    graph_id: str,
    side_role: str,
    graph_class: str,
    r236_partition: dict[str, Any] | None = None,
) -> None:
    legacy_row(row, "R248 bulk:" + row["wall_bulk_node_id"])
    need(row["wall_bulk_node_id"].startswith("round248-wall-bulk:"), "R248 bulk id")
    need(row["physical_component_credit"] == 0 and row["maximal_physical_component_credit"] == 0, "R248 legacy scope")
    if graph_class in ("R235_TARGET_POSITIVE_PARTIAL_BASE", "R235_SOURCE_EXACT_FACE_FULL_BASE"):
        need(row["source_partition_kind"] == "ROUND235_SINGLE_ENDPOINT_GRAPH_BRANCH", "R248 R235 kind")
        need(row["source_partition_row_id"] == graph_id, "R248 R235 graph binding")
        need(row["branch_label"] == side_role, "R248 R235 branch")
        expected = {
            "EVENT_ABSENT": "ROUND235_STRICT_MONOTONE_GRAPH_ABSENT_OPEN_SIDE",
            "EVENT_PRESENT": "ROUND235_STRICT_MONOTONE_GRAPH_PRESENT_OPEN_SIDE",
        }[side_role]
        need(row["positive_volume_proof_kind"] == expected, "R248 R235 proof kind")
    else:
        need(graph_class == "R235D_SOURCE_EXACT_FACE_FULL_BASE", "R248 R235D class")
        need(type(r236_partition) is dict, "R248 R235D direct partition")
        short_role = side_role.removeprefix("source:")
        need(row["source_partition_kind"] == "ROUND236_DOUBLE_ENDPOINT_ARRANGEMENT_BRANCH", "R248 R235D kind")
        need(row["source_partition_row_id"] == r236_partition["double_endpoint_partition_row_id"], "R248 R235D partition binding")
        need(row["Round220_split_interface_id"] == r236_partition["Round220_split_interface_id"], "R248 R235D interface binding")
        need(row["branch_label"] == short_role, "R248 R235D branch")
        expected = {
            "SAME_SIGN_EVENT_ABSENT": "ROUND236_TWO_ENDPOINT_GRAPHS_SAME_SIGN_OPEN_REGION",
            "NEGATIVE_TO_POSITIVE": "ROUND236_TWO_ENDPOINT_GRAPHS_NEGATIVE_TO_POSITIVE_OPEN_REGION",
        }[short_role]
        need(row["positive_volume_proof_kind"] == expected, "R248 R235D proof kind")
        signature = {
            "SAME_SIGN_EVENT_ABSENT": r236_partition["same_sign_event_absent_signature"],
            "NEGATIVE_TO_POSITIVE": r236_partition["negative_to_positive_signature"],
        }[short_role]
        need(row["official_key_id"] == signature["official_key_id"], "R248 R235D official key id")
        need(row["official_key_ordinal"] == signature["official_key_ordinal"], "R248 R235D official key ordinal")
        need(row["local_return_signature_sha256"] == object_sha(signature), "R248 R235D return signature")


def r242_pair_certificate(
    graph_id: str,
    semantic: dict[str, Any],
    r242: dict[str, Any],
    support: dict[str, Any],
    relation_rows: list[dict[str, Any]],
    c7_by_id: dict[str, dict[str, Any]],
    r245_nodes: dict[str, dict[str, Any]],
    r245_edges: dict[str, list[dict[str, Any]]],
) -> dict[str, Any]:
    legacy_row(r242, "R242 patch:" + graph_id)
    need(r242["transition_sheet_patch_row_id"] == graph_id, "R242 graph binding")
    need(r242["closed_witness_box"] == semantic["closed_witness_box"], "R242 witness binding")
    need(r242["equation"] == semantic["equation"], "R242 equation binding")
    need(r242["strict_t_derivative_sign"] == semantic["strict_t_derivative_sign"], "R242 derivative binding")
    need(r242["lower_t_face_F_sign"] == semantic["lower_t_face_F_sign"], "R242 lower face-sign binding")
    need(r242["upper_t_face_F_sign"] == semantic["upper_t_face_F_sign"], "R242 upper face-sign binding")
    need(r242["local_positive_2D_transition_sheet_patch_credit"] == 1, "R242 local patch authority")
    need(r242["physical_component_credit"] == 0, "R242 physical nonpromotion")
    need(len(relation_rows) == 2, "R242 two side relations")
    side_nodes: dict[str, dict[str, Any]] = {}
    for relation in relation_rows:
        c7 = c7_by_id[relation["C7_relation_row_id"]]
        role = c7["incidence_statement_ast"]["side_role"]
        need(role in ("OWNER_OPEN_BULK", "SHADOW_OPEN_BULK") and role not in side_nodes, "R242 side roles")
        node = r245_nodes.get(relation["member_id"])
        need(node is not None, "R242 side node")
        legacy_row(node, "R245 side node:" + relation["member_id"])
        need(node["stratum_kind"] == role and node["local_dimension"] == 3, "R242 side dimension")
        need(node["half_open_owner_materialized"] is False, "R242 side not sheet")
        volume = positive_box(node["strict_positive_3D_witness_box"], 3, "R242 side witness")
        need(volume == q(node["strict_positive_3D_witness_volume"]), "R242 side witness volume")
        side_nodes[role] = node
    need(set(side_nodes) == {"OWNER_OPEN_BULK", "SHADOW_OPEN_BULK"}, "R242 role exhaustion")
    owner = side_nodes["OWNER_OPEN_BULK"]
    shadow = side_nodes["SHADOW_OPEN_BULK"]
    common_fields = (
        "Round179_retained_child_row_id",
        "Round220_split_interface_id",
        "inherited_Round244_resolved_bulk_component_id",
        "official_key_id",
        "official_key_ordinal",
    )
    for field in common_fields:
        need(owner[field] == shadow[field], "R242 paired field:" + field)
    owner_signature = owner["local_return_signature"]
    shadow_signature = shadow["local_return_signature"]
    need(type(owner_signature) is dict and type(shadow_signature) is dict, "R242 paired return signature shape")
    allowed_signature_differences = set(r242["signature_difference_field_allowlist"])
    need(allowed_signature_differences == {"outgoing_cell", "target_chart"}, "R242 exact signature difference allowlist")
    differing_signature_fields = {
        field
        for field in set(owner_signature) | set(shadow_signature)
        if owner_signature.get(field) != shadow_signature.get(field)
    }
    need(set(owner_signature) == set(shadow_signature), "R242 owner/shadow signature key set")
    need(differing_signature_fields == allowed_signature_differences, "R242 owner/shadow signature difference exhaustion")
    need(owner_signature == r242["owner_signature"], "R242 owner signature authority")
    need(shadow_signature == r242["shadow_signature"], "R242 shadow signature authority")
    box = semantic["closed_witness_box"]
    need(positive_box(box, 3, "R242 graph box") > 0, "R242 graph box positive")
    need(q(semantic["exact_positive_base_projection_area"]) == (q(box[3]) - q(box[2])) * (q(box[5]) - q(box[4])), "R242 base area")
    for role, node in side_nodes.items():
        witness = node["strict_positive_3D_witness_box"]
        need(witness[2:6] == box[2:6], "R242 full base corridor:" + role)
        need(q(box[0]) <= q(witness[0]) < q(witness[1]) <= q(box[1]), "R242 corridor inside graph carrier:" + role)
    sheet = r245_nodes.get(support["sheet_member_id"])
    need(sheet is not None, "R242 sheet node")
    legacy_row(sheet, "R245 sheet node:" + support["sheet_member_id"])
    need(sheet["stratum_kind"] == "HALF_OPEN_TRANSITION_SHEET" and sheet["local_dimension"] == 2, "R242 sheet state")
    need(sheet["half_open_owner_materialized"] is True, "R242 owner sheet")
    need(q(sheet["exact_positive_2D_sheet_area"]) == q(semantic["exact_positive_base_projection_area"]), "R242 sheet area")
    for field in common_fields:
        need(sheet[field] == owner[field], "R242 sheet paired field:" + field)
    sheet_signature = sheet["local_return_signature"]
    need(sheet_signature == owner_signature, "R242 sheet signature matches half-open owner")

    related_right_nodes = {
        sheet["retained_stratum_node_id"],
        owner["retained_stratum_node_id"],
        shadow["retained_stratum_node_id"],
    }
    related_edges = [edge for node_id in related_right_nodes for edge in r245_edges.get(node_id, [])]
    edge_by_kind: dict[str, dict[str, Any]] = {}
    expected_edge_kinds = {
        "OWNER_BULK_TO_HALF_OPEN_SHEET",
        "SHADOW_BULK_TO_HALF_OPEN_SHEET",
        "RESOLVED_TO_MATCHING_GRAPH_SIDE_BULK",
    }
    for edge in related_edges:
        kind = edge["edge_kind"]
        need(kind in expected_edge_kinds, "R242 unexpected related edge kind")
        need(kind not in edge_by_kind, "R242 unique edge kind:" + kind)
        legacy_row(edge, "R245 edge:" + edge["mixed_sheet_edge_id"])
        need(edge["Round220_split_interface_id"] == owner["Round220_split_interface_id"], "R242 edge interface:" + kind)
        need(edge["inherited_Round244_resolved_bulk_component_id"] == owner["inherited_Round244_resolved_bulk_component_id"], "R242 edge component:" + kind)
        need(edge["current_quotient_lower_bound_edge_credit"] == 1, "R242 historical edge receipt:" + kind)
        need(positive_box(edge["strict_positive_3D_retained_corridor_box"], 3, "R242 retained corridor:" + kind) == q(edge["strict_positive_3D_retained_corridor_volume"]), "R242 retained corridor volume:" + kind)
        need(positive_box(edge["exact_positive_2D_contact_rectangle"], 2, "R242 contact rectangle:" + kind) == q(edge["exact_positive_2D_contact_area"]), "R242 contact area:" + kind)
        contact = edge["exact_positive_2D_contact_rectangle"]
        corridor = edge["strict_positive_3D_retained_corridor_box"]
        if kind in {"OWNER_BULK_TO_HALF_OPEN_SHEET", "SHADOW_BULK_TO_HALF_OPEN_SHEET"}:
            need(contact == box[2:6] == corridor[2:6], "R242 sheet-edge exact base contact:" + kind)
        else:
            proof_kind = edge["contact_proof_kind"]
            if proof_kind == "ROUND242_GRAPH_SIDE_AT_T_INTERFACE":
                need(contact == box[2:6] == corridor[2:6], "R242 resolved t-interface exact base contact")
            elif proof_kind == "256_BIT_STRICT_DYADIC_CORRIDOR_AT_P_INTERFACE":
                need(contact == corridor[0:2] + corridor[4:6], "R242 resolved p-interface t-s contact projection")
                need(contact != box[2:6], "R242 p-interface contact is not graph-base support")
            else:
                raise Rejected("R242 resolved-side proof kind")
        edge_by_kind[kind] = edge
    need(set(edge_by_kind) == expected_edge_kinds and len(related_edges) == 3, "R242 complete three-edge binding")
    owner_edge = edge_by_kind["OWNER_BULK_TO_HALF_OPEN_SHEET"]
    shadow_edge = edge_by_kind["SHADOW_BULK_TO_HALF_OPEN_SHEET"]
    resolved_edge = edge_by_kind["RESOLVED_TO_MATCHING_GRAPH_SIDE_BULK"]
    need(owner_edge["left_node_id"] == owner["retained_stratum_node_id"] and owner_edge["right_node_id"] == sheet["retained_stratum_node_id"], "R242 owner-sheet edge endpoints")
    need(shadow_edge["left_node_id"] == shadow["retained_stratum_node_id"] and shadow_edge["right_node_id"] == sheet["retained_stratum_node_id"], "R242 shadow-sheet edge endpoints")
    need(resolved_edge["right_node_id"] in {owner["retained_stratum_node_id"], shadow["retained_stratum_node_id"]}, "R242 resolved-side endpoint")
    need(owner_edge["contact_proof_kind"] == shadow_edge["contact_proof_kind"] == "ROUND242_POSITIVE_2D_UNIQUE_GRAPH_PATCH", "R242 sheet-edge proof kinds")
    need(resolved_edge["contact_proof_kind"] in ("ROUND242_GRAPH_SIDE_AT_T_INTERFACE", "256_BIT_STRICT_DYADIC_CORRIDOR_AT_P_INTERFACE"), "R242 resolved-side proof kind")
    return {
        "kind": "R242_THREE_EDGE_LOCAL_ROUTING_RECEIPT_WITHOUT_SIDE_CARRIER_OR_TRACE_THEOREM",
        "sheet_node_ref": {"row_id": sheet["retained_stratum_node_id"], "row_sha256": sheet["row_sha256"]},
        "owner_side_ref": {"row_id": owner["retained_stratum_node_id"], "row_sha256": owner["row_sha256"]},
        "shadow_side_ref": {"row_id": shadow["retained_stratum_node_id"], "row_sha256": shadow["row_sha256"]},
        "three_edge_refs": [
            {"edge_kind": kind, "row_id": edge_by_kind[kind]["mixed_sheet_edge_id"], "row_sha256": edge_by_kind[kind]["row_sha256"]}
            for kind in sorted(expected_edge_kinds)
        ],
        "owner_shadow_signature_allowed_difference_fields": sorted(differing_signature_fields),
        "exact_base_projection_area": semantic["exact_positive_base_projection_area"],
        "resolved_edge_contact_proof_kind": resolved_edge["contact_proof_kind"],
        "resolved_edge_contact_rectangle": resolved_edge["exact_positive_2D_contact_rectangle"],
        "resolved_edge_contact_scope": (
            "FULL_R242_P_S_BASE"
            if resolved_edge["contact_proof_kind"] == "ROUND242_GRAPH_SIDE_AT_T_INTERFACE"
            else "P_INTERFACE_T_S_RECTANGLE_NOT_R242_BASE"
        ),
        "strict_t_derivative_sign": semantic["strict_t_derivative_sign"],
        "lower_t_face_F_sign": semantic["lower_t_face_F_sign"],
        "upper_t_face_F_sign": semantic["upper_t_face_F_sign"],
        "routing_evidence_closed": True,
        "exact_side_carrier_proved": False,
        "closure_incidence_proved": False,
        "one_sided_trace_proved": False,
    }


def build() -> tuple[dict[str, Any], bytes, bytes, bytes, bytes]:
    with Snapshot() as snapshot:
        bind_manifest(snapshot, "C10_MANIFEST", ("C10_RESULT", "C10_SUPPORT", "C10_IDENTITY"))
        bind_manifest(snapshot, "C9_MANIFEST", ("C9_RESULT", "C9_GRAPH", "C9_RELATION"))
        bind_manifest(snapshot, "C7_MANIFEST", ("C7_PHYSICAL",))
        bind_manifest(snapshot, "C6_MANIFEST", ("C6_COMPONENT",))
        bind_manifest(snapshot, "C5_MANIFEST", ("C5_SEMANTIC",))
        bind_manifest(snapshot, "C4_MANIFEST", ("C4_LEDGER",))
        bind_manifest(snapshot, "R235_MANIFEST", ("R235_CERT",))
        bind_manifest(snapshot, "R236_MANIFEST", ("R236_CERT",))
        bind_manifest(snapshot, "R242_MANIFEST", ("R242_CERT",))
        bind_manifest(snapshot, "R248_MANIFEST", ("R248_CERT",))
        bind_manifest(snapshot, "R245_MANIFEST", ("R245_CERT",))

        c9_result = closed_document(snapshot, "C9_RESULT")
        c10_result = closed_document(snapshot, "C10_RESULT")
        validate_results(c9_result, c10_result)

        c9_graph_by_id: dict[str, dict[str, Any]] = {}
        for row in jsonl_rows(snapshot, "C9_GRAPH"):
            graph_id = row["graph_id"]
            need(graph_id not in c9_graph_by_id, "C9 graph uniqueness")
            c9_graph_by_id[graph_id] = row
        need(len(c9_graph_by_id) == 5_264, "C9 graph exhaustion")

        support_by_graph: dict[str, dict[str, Any]] = {}
        for row in jsonl_rows(snapshot, "C10_SUPPORT"):
            graph_id = row["graph_id"]
            need(graph_id not in support_by_graph, "C10 support uniqueness")
            graph_audit = c9_graph_by_id.get(graph_id)
            need(graph_audit is not None, "C10 graph in C9")
            need(row["graph_class"] == graph_audit["graph_class"], "C10 graph class")
            need(row["sheet_member_id"] == graph_audit["sheet_member_id"], "C10 sheet member")
            need(row["C9_graph_ref"] == row_ref(graph_audit), "C10 C9 binding")
            need(row["ast_sha256"]["exact_support_ast_sha256"] == object_sha(row["exact_support_ast"]), "C10 exact support AST")
            need(row["scoped_credit"] == {"exact_G2_feature_support_AST": 1, "member_natural_key_preservation": 0}, "C10 row scoped credit")
            need(all(value == 0 for value in row["downstream_nonpromotion"].values()), "C10 row nonpromotion")
            support_by_graph[graph_id] = row
        need(len(support_by_graph) == 5_264 and set(support_by_graph) == set(c9_graph_by_id), "C10 support exhaustion")

        identity_by_graph: dict[str, dict[str, Any]] = {}
        for row in jsonl_rows(snapshot, "C10_IDENTITY"):
            graph_id = row["graph_id"]
            need(graph_id not in identity_by_graph, "C10 identity uniqueness")
            support = support_by_graph.get(graph_id)
            need(support is not None, "C10 identity graph in support")
            need(row["graph_class"] == support["graph_class"], "C10 identity graph class")
            need(row["sheet_member_id"] == support["sheet_member_id"], "C10 identity member")
            need(row["exact_support_ref"] == row_ref(support), "C10 identity support binding")
            need(row["recomputed_member_id"] == row["sheet_member_id"], "C10 identity natural-key replay")
            need(row["disposition"] == "PRESERVE_EXISTING_MEMBER_ID", "C10 identity disposition")
            need(row["member_natural_key_preservation_credit"] == 1, "C10 identity scoped credit")
            need(row["set_equality_proved"] is False, "C10 identity no set equality")
            need(row["physical_incidence_proved"] is False, "C10 identity no physical incidence")
            need(row["identity_representation_pullback_proved"] is False, "C10 identity no pullback")
            need(all(value == 0 for value in row["downstream_nonpromotion"].values()), "C10 identity downstream zero")
            identity_by_graph[graph_id] = row
        need(len(identity_by_graph) == 5_264 and set(identity_by_graph) == set(support_by_graph), "C10 identity exhaustion")

        c5_by_semantic_id: dict[str, dict[str, Any]] = {}
        for row in jsonl_rows(snapshot, "C5_SEMANTIC"):
            if row["semantic_classification"]["classification"] == "POSITIVE_GRAPH":
                semantic_id = row["semantic_row_id"]
                need(semantic_id not in c5_by_semantic_id, "C5 semantic uniqueness")
                c5_by_semantic_id[semantic_id] = row
        need(len(c5_by_semantic_id) == 5_264, "C5 positive exhaustion")

        c7_by_id: dict[str, dict[str, Any]] = {}
        c7_by_source_incidence: dict[str, dict[str, Any]] = {}
        c7_by_source_graph: dict[str, list[dict[str, Any]]] = defaultdict(list)
        for row in jsonl_rows(snapshot, "C7_PHYSICAL"):
            need(row["row_id"] not in c7_by_id, "C7 relation uniqueness")
            need(row["source_incidence_row_id"] not in c7_by_source_incidence, "C7 source incidence uniqueness")
            c7_by_id[row["row_id"]] = row
            c7_by_source_incidence[row["source_incidence_row_id"]] = row
            c7_by_source_graph[row["source_graph_row_id"]].append(row)
        need(len(c7_by_id) == len(c7_by_source_incidence) == 15_392, "C7 physical exhaustion")

        c9_positive_side_rows: list[dict[str, Any]] = []
        c9_empty_rows: list[dict[str, Any]] = []
        c9_by_c7_relation_id: dict[str, dict[str, Any]] = {}
        all_c9_relation_count = 0
        for row in jsonl_rows(snapshot, "C9_RELATION"):
            need(row["mechanical_relation_ordinal"] == all_c9_relation_count, "C9 relation order")
            all_c9_relation_count += 1
            c7_relation_id = row["C7_relation_row_id"]
            need(c7_relation_id not in c9_by_c7_relation_id, "C9 C7-relation uniqueness")
            c9_by_c7_relation_id[c7_relation_id] = row
            if row["incidence_role"] == "GRAPH_TO_SIDE" and row["positive_graph_physical_relation_candidate"] == 1:
                need(row["disposition"] == "EXACT_ONE_SIDED_SIGN_STRATUM_AND_TRACE_PENDING", "C9 positive side state")
                c9_positive_side_rows.append(row)
            if row["disposition"] == "EMPTY_GRAPH_NO_PHYSICAL_INCIDENCE":
                need(row["incidence_role"] == "GRAPH_TO_SIDE" and row["positive_graph_physical_relation_candidate"] == 0, "C9 empty relation")
                c9_empty_rows.append(row)
        need(all_c9_relation_count == 15_392, "C9 relation exhaustion")
        need(len(c9_by_c7_relation_id) == 15_392, "C9 C7-relation exhaustion")
        need(len(c9_positive_side_rows) == 10_118 and len(c9_empty_rows) == 10, "C9 side/empty census")

        c4_rows = list(jsonl_rows(snapshot, "C4_LEDGER"))
        need(len(c4_rows) == 16, "C4 bridge census")
        c4_by_target_graph: dict[str, dict[str, Any]] = {}
        c4_by_source_graph_inventory: dict[str, dict[str, Any]] = {}
        for row in c4_rows:
            target_graph = row["G2_orphan_graph_disposition"]["C3_orphan_target_graph_id"]
            source_graph_inventory = row["canonical_input_commitment"]["B1G0_source_graph_row"][1]
            need(target_graph not in c4_by_target_graph and source_graph_inventory not in c4_by_source_graph_inventory, "C4 uniqueness")
            c4_by_target_graph[target_graph] = row
            c4_by_source_graph_inventory[source_graph_inventory] = row

        r235_document = legacy_document(snapshot, "R235_CERT")
        r235_rows = r235_document["result"]["single_endpoint_graph_partition_rows"]
        need(len(r235_rows) == 38_328, "R235 row census")
        r235_by_graph = {row["endpoint_graph_partition_row_id"]: row for row in r235_rows}
        need(len(r235_by_graph) == len(r235_rows), "R235 graph uniqueness")

        r236_document = legacy_document(snapshot, "R236_CERT")
        r236_rows = r236_document["result"]["double_endpoint_partition_rows"]
        need(len(r236_rows) == 16, "R236 double-endpoint census")
        r236_by_id = {row["double_endpoint_partition_row_id"]: row for row in r236_rows}
        need(len(r236_by_id) == len(r236_rows), "R236 double-endpoint uniqueness")

        r242_document = legacy_document(snapshot, "R242_CERT")
        r242_rows = r242_document["result"]["formal_positive_2D_transition_sheet_patch_ledger"]["rows"]
        need(len(r242_rows) == 264, "R242 positive patch census")
        r242_by_graph = {row["transition_sheet_patch_row_id"]: row for row in r242_rows}
        need(len(r242_by_graph) == len(r242_rows), "R242 graph uniqueness")

        r248_document = legacy_document(snapshot, "R248_CERT")
        r248_rows = r248_document["result"]["formal_wall_positive_volume_bulk_ledger"]["rows"]
        need(len(r248_rows) == 88_936, "R248 bulk census")
        r248_by_member = {row["wall_bulk_node_id"]: row for row in r248_rows}
        need(len(r248_by_member) == len(r248_rows), "R248 bulk uniqueness")

        r245_document = legacy_document(snapshot, "R245_CERT")
        r245_result = r245_document["result"]
        r245_node_rows = r245_result["formal_retained_stratum_node_ledger"]["rows"]
        r245_edge_rows = r245_result["formal_mixed_sheet_physical_edge_ledger"]["rows"]
        need(len(r245_node_rows) == len(r245_edge_rows) == 3_664, "R245 node/edge census")
        r245_nodes = {row["retained_stratum_node_id"]: row for row in r245_node_rows}
        need(len(r245_nodes) == len(r245_node_rows), "R245 node uniqueness")
        r245_edges: dict[str, list[dict[str, Any]]] = defaultdict(list)
        for row in r245_edge_rows:
            r245_edges[row["right_node_id"]].append(row)

        positive_sides_by_graph: dict[str, list[dict[str, Any]]] = defaultdict(list)
        needed_members: set[str] = set()
        for relation in c9_positive_side_rows:
            positive_sides_by_graph[relation["graph_id"]].append(relation)
            needed_members.add(relation["member_id"])
            support = support_by_graph.get(relation["graph_id"])
            need(support is not None, "positive side C10 graph")
            needed_members.add(support["sheet_member_id"])
        for relation in c9_empty_rows:
            needed_members.add(relation["member_id"])
        need(len(needed_members) == 15_392, "C6 requested member denominator")
        components: dict[str, dict[str, Any]] = {}
        for row in jsonl_rows(snapshot, "C6_COMPONENT"):
            member_id = row["registry_member_id"]
            if member_id in needed_members:
                need(member_id not in components, "C6 requested member uniqueness")
                need(row["member_identity_preserved"] is True, "C6 member identity")
                components[member_id] = row
        need(set(components) == needed_members, "C6 requested member exhaustion")

        r242_certificates: dict[str, dict[str, Any]] = {}
        for graph_id, relations in positive_sides_by_graph.items():
            graph_audit = c9_graph_by_id[graph_id]
            if graph_audit["graph_class"] != "R242_UNIQUE_GRAPH_FULL_PATCH":
                continue
            c5 = c5_by_semantic_id[graph_audit["C5_semantic_row_id"]]
            need(c5["row_sha256"] == graph_audit["C5_semantic_row_sha256"], "R242 C5 binding")
            r242 = r242_by_graph.get(graph_id)
            need(r242 is not None, "R242 direct authority")
            r242_commitment = c5["canonical_input_commitment"]["R242_positive_patch_row"]
            need(r242_commitment[1] == graph_id, "R242 C5 commitment id")
            need(r242_commitment[2] == object_sha(r242), "R242 C5 commitment object")
            need(r242_commitment[3] == r242["row_sha256"], "R242 C5 commitment row closure")
            r242_certificates[graph_id] = r242_pair_certificate(
                graph_id,
                c5["semantic_classification"],
                r242,
                support_by_graph[graph_id],
                relations,
                c7_by_id,
                r245_nodes,
                r245_edges,
            )
        need(len(r242_certificates) == 264, "R242 certificate exhaustion")

        disposition_rows: list[dict[str, Any]] = []
        ready_rows: list[dict[str, Any]] = []
        blocked_rows: list[dict[str, Any]] = []
        class_disposition_census: Counter[tuple[str, str]] = Counter()
        class_role_disposition_census: Counter[tuple[str, str, str]] = Counter()
        component_census: Counter[tuple[str, str]] = Counter()
        ready_cross_component_pairs: set[tuple[str, str]] = set()

        for relation in c9_positive_side_rows:
            c7 = c7_by_id.get(relation["C7_relation_row_id"])
            need(c7 is not None and c7["row_sha256"] == relation["C7_relation_row_sha256"], "C9-C7 relation binding")
            need(c7["graph_id"] == relation["graph_id"] and c7["member_id"] == relation["member_id"], "C9-C7 relation subject")
            need(c7["incidence_role"] == "GRAPH_TO_SIDE", "C7 side role")
            need(relation["coarse_family"] == c7["coarse_family"], "C9-C7 coarse family")
            need(relation["physical_incidence_proved"] is False, "C9 physical pending")
            need(relation["one_sided_trace_proved"] is False, "C9 trace pending")
            need(relation["representation_pullback_proved"] is False, "C9 pullback pending")
            need(all(value == 0 for value in relation["formal_credit"].values()), "C9 relation zero credit")
            ast = c7["incidence_statement_ast"]
            need(ast["ast_kind"] == "GRAPH_SIDE_INCIDENCE_STATEMENT" and ast["proved"] is False, "C7 pending statement")
            need(ast["graph_id"] == relation["graph_id"] and ast["member_id"] == relation["member_id"], "C7 statement subject")
            need(c7["graph_semantic_authority_kind"] == "C5_POSITIVE_GRAPH_DEFINITION", "C7 positive authority")

            graph_id = relation["graph_id"]
            graph_audit = c9_graph_by_id.get(graph_id)
            need(graph_audit is not None and relation["graph_domain_audit_ref"] == row_ref(graph_audit), "C9 relation graph binding")
            support = support_by_graph[graph_id]
            graph_class = graph_audit["graph_class"]
            side_role = ast["side_role"]
            c5 = c5_by_semantic_id.get(graph_audit["C5_semantic_row_id"])
            need(c5 is not None and c5["row_sha256"] == graph_audit["C5_semantic_row_sha256"], "C9-C5 binding")
            need(c7["graph_semantic_authority_row_id"] == c5["semantic_row_id"], "C7-C5 authority row")
            need(c7["graph_semantic_authority_row_sha256"] == c5["row_sha256"], "C7-C5 authority closure")
            need(c5["graph_id"] == graph_id and support["C5_semantic_ref"] == {"row_id": c5["semantic_row_id"], "row_sha256": c5["row_sha256"]}, "C10-C5 binding")
            identity_disposition = identity_by_graph[graph_id]
            semantic = c5["semantic_classification"]

            graph_component = components[support["sheet_member_id"]]
            side_component = components[relation["member_id"]]
            if graph_component["new_base_root_id"] == side_component["new_base_root_id"]:
                need(graph_component["fresh_component_id"] == side_component["fresh_component_id"], "same root component")
                component_relation = "SAME_BASE_ROOT"
                component_pair = None
            else:
                need(graph_component["fresh_component_id"] != side_component["fresh_component_id"], "different root same component rejected")
                component_relation = "CROSS_COMPONENT"
                component_pair = tuple(sorted((graph_component["fresh_component_id"], side_component["fresh_component_id"])))

            ready = False
            blocker: str | None = None
            theorem_basis: dict[str, Any]
            legacy_side_ref: dict[str, str]
            missing_theorem_authority: list[str]

            if graph_class == "R235_TARGET_POSITIVE_PARTIAL_BASE":
                need(semantic["kernel"] == "G_TARGET_FIRST_HIT_COORDINATE_MINUS_INTEGER_WALL_V1", "R235 target kernel")
                partition = r235_by_graph.get(graph_id)
                need(partition is not None, "R235 target partition")
                validate_r235_partition(partition, graph_id)
                partition_ref = c5["canonical_input_commitment"]["R235_partition_row"]
                need(partition_ref[1] == graph_id and partition_ref[2] == object_sha(partition), "R235 target partition binding")
                need(partition["active_endpoint_factor"] == "target", "R235 target active factor")
                need(side_role in ("EVENT_ABSENT", "EVENT_PRESENT"), "R235 target side role")
                bulk = r248_by_member.get(relation["member_id"])
                need(bulk is not None, "R235 target bulk")
                validate_r248_bulk(bulk, graph_id, side_role, graph_class)
                eta = 1 if partition["fixed_endpoint_factor_sign"] == "STRICT_POSITIVE" else -1
                sign_relation = "STRICT_GT_ZERO" if side_role == "EVENT_ABSENT" else "STRICT_LT_ZERO"
                theorem_basis = {
                    "kind": "R235_TARGET_SIGN_STRATUM_ROUTING_BASIS_ONLY",
                    "exact_feature_support_AST_sha256": support["ast_sha256"]["exact_support_ast_sha256"],
                    "equation_AST_sha256": support["ast_sha256"]["equation_ast_sha256"],
                    "R235_partition_row_sha256": object_sha(partition),
                    "fixed_endpoint_factor_sign": partition["fixed_endpoint_factor_sign"],
                    "eta": eta,
                    "side_stratum_predicate": {"left": "eta_times_target_feature_F", "relation": sign_relation, "right": "0"},
                    "boundary_predicate": "target_feature_F_EQUALS_0",
                    "strict_t_derivative_sign": semantic["strict_t_derivative_proof"]["strict_t_derivative_sign"],
                    "exact_partial_base_domain_retained": True,
                    "one_sided_local_trace_closed": False,
                }
                legacy_side_ref = {"row_id": bulk["wall_bulk_node_id"], "row_sha256": bulk["row_sha256"]}
                missing_theorem_authority = list(R235_MISSING_AUTHORITY)
                ready = True
            elif graph_class == "R235_SOURCE_EXACT_FACE_FULL_BASE":
                need(semantic["kernel"] == "EXACT_SOURCE_COORDINATE_MINUS_ZERO_EQUALS_9_OVER_25_TIMES_T", "R235 source kernel")
                partition = r235_by_graph.get(graph_id)
                need(partition is not None, "R235 source partition")
                validate_r235_partition(partition, graph_id)
                partition_ref = c5["canonical_input_commitment"]["R235_partition_row"]
                need(partition_ref[1] == graph_id and partition_ref[2] == object_sha(partition), "R235 source partition binding")
                need(partition["active_endpoint_factor"] == "source", "R235 source active factor")
                need(side_role in ("EVENT_ABSENT", "EVENT_PRESENT"), "R235 source side role")
                box = semantic["complete_parameter_domain"]["box"]
                need(positive_box(box, 3, "R235 source carrier") > 0, "R235 source positive carrier")
                need(q(semantic["strict_t_derivative_exact"]) == Q(9, 25), "R235 source derivative")
                need((q(box[3]) - q(box[2])) * (q(box[5]) - q(box[4])) == q(semantic["exact_positive_base_area"]), "R235 source base area")
                zero_face = semantic["zero_face"]
                if zero_face == "LOWER":
                    need(q(box[0]) == 0 < q(box[1]), "R235 source lower face")
                    interior_sign = "STRICT_POSITIVE"
                else:
                    need(zero_face == "UPPER" and q(box[0]) < 0 == q(box[1]), "R235 source upper face")
                    interior_sign = "STRICT_NEGATIVE"
                local_role = "EVENT_ABSENT" if partition["fixed_endpoint_factor_sign"] == interior_sign else "EVENT_PRESENT"
                bulk = r248_by_member.get(relation["member_id"])
                need(bulk is not None, "R235 source bulk")
                validate_r248_bulk(bulk, graph_id, side_role, graph_class)
                theorem_basis = {
                    "kind": "R235_SOURCE_ZERO_FACE_ROUTING_BASIS_ONLY",
                    "exact_feature_support_AST_sha256": support["ast_sha256"]["exact_support_ast_sha256"],
                    "R235_partition_row_sha256": object_sha(partition),
                    "zero_face": zero_face,
                    "interior_source_factor_sign": interior_sign,
                    "fixed_endpoint_factor_sign": partition["fixed_endpoint_factor_sign"],
                    "unique_local_side_role": local_role,
                    "actual_side_role": side_role,
                    "strict_t_derivative_exact": semantic["strict_t_derivative_exact"],
                    "full_base_local_trace_closed": False,
                }
                legacy_side_ref = {"row_id": bulk["wall_bulk_node_id"], "row_sha256": bulk["row_sha256"]}
                missing_theorem_authority = list(R235_MISSING_AUTHORITY)
                ready = side_role == local_role
                if not ready:
                    blocker = "ADJACENT_DOMAIN_REQUIRED"
            elif graph_class == "R235D_SOURCE_EXACT_FACE_FULL_BASE":
                need(semantic["kernel"] == "SEALED_C4_R235D_SOURCE_EXACT_FACE_GRAPH_BRIDGE", "R235D kernel")
                bridge = c4_by_source_graph_inventory.get(graph_audit["graph_inventory_row_id"])
                need(bridge is not None, "R235D bridge")
                r236_commitment = bridge["canonical_input_commitment"]["R236_double_endpoint_partition_row"]
                need(type(r236_commitment) is list and len(r236_commitment) == 3, "R235D R236 commitment shape")
                need(type(r236_commitment[0]) is int and 0 <= r236_commitment[0] < len(r236_rows), "R235D R236 commitment ordinal")
                r236 = r236_by_id.get(r236_commitment[1])
                need(r236 is not None and r236_rows[r236_commitment[0]] == r236, "R235D R236 ordinal/id binding")
                need(r236_commitment[2] == object_sha(r236), "R235D R236 object binding")
                need(r236["Round220_split_interface_id"] == bridge["Round220_split_interface_id"], "R235D R236 interface binding")
                need(r236["local_finite_exact_key_partition_credit"] == 1, "R235D R236 local partition")
                need(r236["whole_root_credit"] == 0, "R235D R236 nonpromotion")
                reconstruction = bridge["semantic_reconstruction"]
                need(reconstruction["complete_domain_partition_verified"] is True, "R235D complete domain")
                need(reconstruction["source_zero_set"] == "EXACT_FACE_GRAPH_t_EQUALS_0", "R235D source zero set")
                need(side_role in ("source:SAME_SIGN_EVENT_ABSENT", "source:NEGATIVE_TO_POSITIVE"), "R235D side role")
                expected_commitment = (
                    "B1G0_source_shared_side_row"
                    if side_role == "source:SAME_SIGN_EVENT_ABSENT"
                    else "B1G0_source_only_side_row"
                )
                need(c7["source_incidence_row_id"] == bridge["canonical_input_commitment"][expected_commitment][1], "R235D side source binding")
                bulk = r248_by_member.get(relation["member_id"])
                need(bulk is not None, "R235D bulk")
                validate_r248_bulk(bulk, graph_id, side_role, graph_class, r236)
                theorem_basis = {
                    "kind": "R235D_SOURCE_FACE_ROUTING_BASIS_ONLY",
                    "exact_feature_support_AST_sha256": support["ast_sha256"]["exact_support_ast_sha256"],
                    "C4_bridge_ref": {"row_id": bridge["bridge_row_id"], "row_sha256": bridge["row_sha256"]},
                    "R236_double_endpoint_partition_ref": {
                        "row_id": r236["double_endpoint_partition_row_id"],
                        "row_object_sha256": object_sha(r236),
                    },
                    "zero_face": reconstruction["source_zero_face"],
                    "actual_side_role": side_role,
                    "complete_domain_partition_verified": True,
                    "shared_same_sign_local_trace_closed": False,
                }
                legacy_side_ref = {"row_id": bulk["wall_bulk_node_id"], "row_sha256": bulk["row_sha256"]}
                missing_theorem_authority = list(R235D_MISSING_AUTHORITY)
                ready = side_role == "source:SAME_SIGN_EVENT_ABSENT"
                if not ready:
                    blocker = "OUTSIDE_DOMAIN_TRACE_AUTHORITY_REQUIRED"
            elif graph_class == "R242_UNIQUE_GRAPH_FULL_PATCH":
                need(semantic["kernel"] == "SEALED_R242_UNIQUE_TRANSITION_GRAPH_PATCH_BRIDGE", "R242 kernel")
                need(side_role in ("OWNER_OPEN_BULK", "SHADOW_OPEN_BULK"), "R242 side role")
                node = r245_nodes[relation["member_id"]]
                theorem_basis = {**r242_certificates[graph_id], "actual_side_role": side_role}
                legacy_side_ref = {"row_id": node["retained_stratum_node_id"], "row_sha256": node["row_sha256"]}
                missing_theorem_authority = list(R242_MISSING_AUTHORITY)
                ready = True
            else:
                raise Rejected("unknown graph class:" + graph_class)

            disposition = "CANDIDATE_READY_ROUTING" if ready else blocker
            need(type(disposition) is str, "disposition assigned")
            class_disposition_census[(graph_class, disposition)] += 1
            class_role_disposition_census[(graph_class, side_role, disposition)] += 1
            component_census[("READY" if ready else "BLOCKED", component_relation)] += 1
            if ready and component_pair is not None:
                ready_cross_component_pairs.add(component_pair)

            core = {
                "schema": DISPOSITION_ROW_SCHEMA,
                "row_id": PREFIX + ":disposition:" + object_sha([relation["row_id"], disposition]),
                "C9_mechanical_relation_ordinal": relation["mechanical_relation_ordinal"],
                "C9_relation_ref": row_ref(relation),
                "C7_relation_ref": row_ref(c7),
                "C9_graph_ref": row_ref(graph_audit),
                "C10_exact_support_ref": row_ref(support),
                "C10_member_identity_ref": row_ref(identity_disposition),
                "graph_id": graph_id,
                "graph_class": graph_class,
                "sheet_member_id": support["sheet_member_id"],
                "side_member_id": relation["member_id"],
                "side_role": side_role,
                "legacy_side_ref": legacy_side_ref,
                "graph_sheet_component_ref": component_ref(graph_component),
                "side_component_ref": component_ref(side_component),
                "component_relation": component_relation,
                "cross_component_pair": list(component_pair) if component_pair is not None else None,
                "theorem_basis": theorem_basis,
                "candidate_ready_routing": ready,
                "missing_theorem_authority": missing_theorem_authority,
                "disposition": disposition,
                "local_graph_side_physical_incidence_proved": False,
                "one_sided_trace_proved": False,
                "representation_pullback_proved": False,
                "graph_sheet_set_equality_proved": False,
                "DSU_edge_or_union_authorized": False,
                "formal_credit": local_credit(ready),
            }
            disposition_row = closed_row(core)
            disposition_rows.append(disposition_row)
            if ready:
                routing_core = {
                    "schema": READY_ROW_SCHEMA,
                    "row_id": PREFIX + ":candidate-ready-routing:" + object_sha(disposition_row["row_id"]),
                    "disposition_ref": row_ref(disposition_row),
                    "graph_id": graph_id,
                    "graph_class": graph_class,
                    "side_member_id": relation["member_id"],
                    "side_role": side_role,
                    "routing_statement": "THIS_ROW_IS_ROUTED_TO_A_LOCAL_GRAPH_SIDE_THEOREM OBLIGATION_BUT_NO_INCIDENCE_OR_TRACE_THEOREM_IS_YET_PROVED",
                    "routing_basis_sha256": object_sha(theorem_basis),
                    "missing_theorem_authority": missing_theorem_authority,
                    "component_relation": component_relation,
                    "cross_component_pair": list(component_pair) if component_pair is not None else None,
                    "local_graph_side_physical_incidence_credit": 0,
                    "one_sided_trace_credit": 0,
                    "graph_sheet_set_equality_credit": 0,
                    "representation_pullback_credit": 0,
                    "DSU_edge_credit": 0,
                    "DSU_union_credit": 0,
                    "downstream_nonpromotion": ZERO_DOWNSTREAM,
                }
                ready_rows.append(closed_row(routing_core))
            else:
                blocked_core = {
                    "schema": BLOCKED_ROW_SCHEMA,
                    "row_id": PREFIX + ":blocked:" + object_sha(disposition_row["row_id"]),
                    "disposition_ref": row_ref(disposition_row),
                    "graph_id": graph_id,
                    "graph_class": graph_class,
                    "side_member_id": relation["member_id"],
                    "side_role": side_role,
                    "blocker": blocker,
                    "missing_theorem_authority": missing_theorem_authority,
                    "missing_authority": (
                        "EXACT_ADJACENT_DOMAIN_AND_COMMON_TRACE"
                        if blocker == "ADJACENT_DOMAIN_REQUIRED"
                        else "EXACT_OUTSIDE_DOMAIN_EXTENSION_AND_TRACE"
                    ),
                    "local_graph_side_physical_incidence_credit": 0,
                    "one_sided_trace_credit": 0,
                    "DSU_edge_credit": 0,
                    "downstream_nonpromotion": ZERO_DOWNSTREAM,
                }
                blocked_rows.append(closed_row(blocked_core))

        need(len(disposition_rows) == 10_118, "disposition exhaustion")
        need(len(ready_rows) == 9_950 and len(blocked_rows) == 168, "ready/blocked exhaustion")
        expected_class_dispositions = {
            ("R235_TARGET_POSITIVE_PARTIAL_BASE", "CANDIDATE_READY_ROUTING"): 8_864,
            ("R235_SOURCE_EXACT_FACE_FULL_BASE", "CANDIDATE_READY_ROUTING"): 552,
            ("R235_SOURCE_EXACT_FACE_FULL_BASE", "ADJACENT_DOMAIN_REQUIRED"): 152,
            ("R235D_SOURCE_EXACT_FACE_FULL_BASE", "CANDIDATE_READY_ROUTING"): 6,
            ("R235D_SOURCE_EXACT_FACE_FULL_BASE", "OUTSIDE_DOMAIN_TRACE_AUTHORITY_REQUIRED"): 16,
            ("R242_UNIQUE_GRAPH_FULL_PATCH", "CANDIDATE_READY_ROUTING"): 528,
        }
        need(class_disposition_census == expected_class_dispositions, "class disposition census")
        expected_class_role_dispositions = {
            ("R235_TARGET_POSITIVE_PARTIAL_BASE", "EVENT_ABSENT", "CANDIDATE_READY_ROUTING"): 4_432,
            ("R235_TARGET_POSITIVE_PARTIAL_BASE", "EVENT_PRESENT", "CANDIDATE_READY_ROUTING"): 4_432,
            ("R235_SOURCE_EXACT_FACE_FULL_BASE", "EVENT_ABSENT", "CANDIDATE_READY_ROUTING"): 336,
            ("R235_SOURCE_EXACT_FACE_FULL_BASE", "EVENT_PRESENT", "CANDIDATE_READY_ROUTING"): 216,
            ("R235_SOURCE_EXACT_FACE_FULL_BASE", "EVENT_ABSENT", "ADJACENT_DOMAIN_REQUIRED"): 32,
            ("R235_SOURCE_EXACT_FACE_FULL_BASE", "EVENT_PRESENT", "ADJACENT_DOMAIN_REQUIRED"): 120,
            ("R235D_SOURCE_EXACT_FACE_FULL_BASE", "source:SAME_SIGN_EVENT_ABSENT", "CANDIDATE_READY_ROUTING"): 6,
            ("R235D_SOURCE_EXACT_FACE_FULL_BASE", "source:NEGATIVE_TO_POSITIVE", "OUTSIDE_DOMAIN_TRACE_AUTHORITY_REQUIRED"): 16,
            ("R242_UNIQUE_GRAPH_FULL_PATCH", "OWNER_OPEN_BULK", "CANDIDATE_READY_ROUTING"): 264,
            ("R242_UNIQUE_GRAPH_FULL_PATCH", "SHADOW_OPEN_BULK", "CANDIDATE_READY_ROUTING"): 264,
        }
        need(class_role_disposition_census == expected_class_role_dispositions, "class-role disposition census")
        need(component_census == {("READY", "SAME_BASE_ROOT"): 5_302, ("READY", "CROSS_COMPONENT"): 4_648, ("BLOCKED", "SAME_BASE_ROOT"): 32, ("BLOCKED", "CROSS_COMPONENT"): 136}, "component disposition census")
        need(len(ready_cross_component_pairs) == 4_500, "ready distinct cross-component pairs")

        reroute_rows: list[dict[str, Any]] = []
        reroute_source_graph_ids: set[str] = set()
        for relation in c9_empty_rows:
            c7_target = c7_by_id.get(relation["C7_relation_row_id"])
            need(c7_target is not None and c7_target["row_sha256"] == relation["C7_relation_row_sha256"], "reroute C9-C7 binding")
            need(c7_target["graph_id"] == relation["graph_id"] and c7_target["member_id"] == relation["member_id"], "reroute target relation subject")
            need(c7_target["incidence_role"] == "GRAPH_TO_SIDE", "reroute target side role")
            need(relation["graph_domain_audit_ref"] is None, "reroute empty target no graph audit")
            need(all(value == 0 for value in relation["formal_credit"].values()), "reroute target C9 zero credit")
            bridge = c4_by_target_graph.get(relation["graph_id"])
            need(bridge is not None, "reroute C4 target")
            need(bridge["canonical_input_commitment_sha256"] == object_sha(bridge["canonical_input_commitment"]), "reroute C4 commitment closure")
            need(c7_target["graph_semantic_authority_kind"] == "C4_ORPHAN_TARGET_EMPTY_GRAPH_DISPOSITION", "reroute target C4 authority kind")
            need(c7_target["graph_semantic_authority_row_id"] == bridge["bridge_row_id"], "reroute target C4 authority row")
            need(c7_target["graph_semantic_authority_row_sha256"] == bridge["row_sha256"], "reroute target C4 authority closure")
            disposition = bridge["G2_orphan_graph_disposition"]
            need(disposition["disposition"] == "EMPTY_GRAPH_ON_COMPLETE_PARAMETER_DOMAIN", "reroute empty target")
            commitments = bridge["canonical_input_commitment"]
            target_shared = commitments["B1G0_target_shared_side_row"]
            source_shared = commitments["B1G0_source_shared_side_row"]
            target_graph = commitments["B1G0_target_graph_row"]
            source_graph = commitments["B1G0_source_graph_row"]
            source_sheet = commitments["B1G0_source_sheet_row"]
            source_only = commitments["B1G0_source_only_side_row"]
            need(c7_target["source_graph_row_id"] == target_graph[1] and c7_target["source_graph_row_sha256"] == target_graph[3], "reroute target graph lineage")
            need(c7_target["source_incidence_row_id"] == target_shared[1], "reroute surviving target shared row")
            need(c7_target["source_incidence_row_sha256"] == target_shared[3], "reroute surviving target shared closure")
            need(c7_target["incidence_statement_ast"]["side_role"] == "target:SAME_SIGN_EVENT_ABSENT", "reroute target shared role")
            need(source_shared[1] not in c7_by_source_incidence, "reroute missing source shared row")
            source_inventory_id = commitments["B1G0_source_graph_row"][1]
            source_relations = c7_by_source_graph[source_inventory_id]
            source_sheet_relations = [row for row in source_relations if row["incidence_role"] == "GRAPH_TO_SHEET"]
            source_side_relations = [row for row in source_relations if row["incidence_role"] == "GRAPH_TO_SIDE"]
            need(len(source_sheet_relations) == 1 and len(source_side_relations) == 1, "reroute source surviving relation shape")
            need(source_sheet_relations[0]["source_incidence_row_id"] == source_sheet[1], "reroute source sheet lineage")
            need(source_sheet_relations[0]["source_incidence_row_sha256"] == source_sheet[3], "reroute source sheet closure")
            need(source_side_relations[0]["source_incidence_row_id"] == source_only[1], "reroute source-only side lineage")
            need(source_side_relations[0]["source_incidence_row_sha256"] == source_only[3], "reroute source-only side closure")
            for source_relation in source_relations:
                need(source_relation["source_graph_row_id"] == source_graph[1], "reroute source graph lineage")
                need(source_relation["source_graph_row_sha256"] == source_graph[3], "reroute source graph closure")
                need(source_relation["graph_semantic_authority_kind"] == "C5_POSITIVE_GRAPH_DEFINITION", "reroute positive source authority kind")
            source_graph_id = source_sheet_relations[0]["graph_id"]
            need(source_graph_id == source_side_relations[0]["graph_id"], "reroute source graph binding")
            need(source_side_relations[0]["incidence_statement_ast"]["side_role"] == "source:NEGATIVE_TO_POSITIVE", "reroute remaining source-only role")
            source_sheet_c9 = c9_by_c7_relation_id[source_sheet_relations[0]["row_id"]]
            source_side_c9 = c9_by_c7_relation_id[source_side_relations[0]["row_id"]]
            need(source_sheet_c9["incidence_role"] == "GRAPH_TO_SHEET" and source_sheet_c9["positive_graph_physical_relation_candidate"] == 1, "reroute positive source sheet C9")
            need(source_side_c9["incidence_role"] == "GRAPH_TO_SIDE" and source_side_c9["positive_graph_physical_relation_candidate"] == 1, "reroute positive source side C9")
            need(source_side_c9["disposition"] == "EXACT_ONE_SIDED_SIGN_STRATUM_AND_TRACE_PENDING", "reroute source-side C9 state")
            support = support_by_graph.get(source_graph_id)
            need(support is not None and support["graph_class"] == "R235D_SOURCE_EXACT_FACE_FULL_BASE", "reroute source support")
            source_graph_audit = c9_graph_by_id[source_graph_id]
            need(source_sheet_c9["graph_domain_audit_ref"] == row_ref(source_graph_audit), "reroute source sheet graph audit")
            need(source_side_c9["graph_domain_audit_ref"] == row_ref(source_graph_audit), "reroute source side graph audit")
            source_c5 = c5_by_semantic_id[source_graph_audit["C5_semantic_row_id"]]
            for source_relation in source_relations:
                need(source_relation["graph_semantic_authority_row_id"] == source_c5["semantic_row_id"], "reroute source C5 authority row")
                need(source_relation["graph_semantic_authority_row_sha256"] == source_c5["row_sha256"], "reroute source C5 authority closure")
            need(support["C9_graph_ref"] == row_ref(source_graph_audit), "reroute C10-C9 graph binding")
            source_identity = identity_by_graph[source_graph_id]
            need(source_graph_id not in reroute_source_graph_ids, "reroute source graph uniqueness")
            reroute_source_graph_ids.add(source_graph_id)
            r236_commitment = commitments["R236_double_endpoint_partition_row"]
            need(type(r236_commitment) is list and len(r236_commitment) == 3, "reroute R236 commitment shape")
            r236 = r236_by_id.get(r236_commitment[1])
            need(r236 is not None and r236_rows[r236_commitment[0]] == r236, "reroute R236 ordinal/id binding")
            need(r236_commitment[2] == object_sha(r236), "reroute R236 object binding")
            need(r236["Round220_split_interface_id"] == bridge["Round220_split_interface_id"], "reroute R236 interface binding")
            graph_component = components[support["sheet_member_id"]]
            shared_component = components[relation["member_id"]]
            if graph_component["new_base_root_id"] == shared_component["new_base_root_id"]:
                need(graph_component["fresh_component_id"] == shared_component["fresh_component_id"], "reroute same root component")
                component_relation = "SAME_BASE_ROOT"
            else:
                need(graph_component["fresh_component_id"] != shared_component["fresh_component_id"], "reroute component separation")
                component_relation = "CROSS_COMPONENT"
            core = {
                "schema": REROUTE_ROW_SCHEMA,
                "row_id": PREFIX + ":missing-local-shared-reroute:" + object_sha([bridge["bridge_row_id"], relation["row_id"]]),
                "bridge_ordinal": bridge["bridge_ordinal"],
                "C4_bridge_ref": {"row_id": bridge["bridge_row_id"], "row_sha256": bridge["row_sha256"]},
                "C9_empty_target_relation_ref": row_ref(relation),
                "C7_surviving_target_shared_relation_ref": row_ref(c7_target),
                "empty_target_graph_id": relation["graph_id"],
                "positive_source_graph_id": source_graph_id,
                "C10_positive_source_support_ref": row_ref(support),
                "C10_positive_source_identity_ref": row_ref(source_identity),
                "C9_positive_source_sheet_relation_ref": row_ref(source_sheet_c9),
                "C9_positive_source_only_relation_ref": row_ref(source_side_c9),
                "R236_double_endpoint_partition_ref": {
                    "row_id": r236["double_endpoint_partition_row_id"],
                    "row_object_sha256": object_sha(r236),
                },
                "surviving_shared_side_member_id": relation["member_id"],
                "missing_source_shared_mechanical_row": {"row_id": source_shared[1], "expected_row_commitment": source_shared},
                "source_graph_sheet_component_ref": component_ref(graph_component),
                "shared_side_component_ref": component_ref(shared_component),
                "component_relation": component_relation,
                "finding": "TARGET_GRAPH_IS_EMPTY_BUT_THE_SHARED_SIDE_SURVIVES_WITHOUT_ITS_POSITIVE_SOURCE_GRAPH_LOCAL_RELATION",
                "required_next": "REROUTE_SHARED_SIDE_TO_POSITIVE_SOURCE_GRAPH_THEN_PROVE_THE_LOCAL_SHARED_TRACE",
                "reroute_performed": False,
                "local_graph_side_physical_incidence_credit": 0,
                "one_sided_trace_credit": 0,
                "DSU_edge_credit": 0,
                "downstream_nonpromotion": ZERO_DOWNSTREAM,
            }
            reroute_rows.append(closed_row(core))
        reroute_rows.sort(key=lambda row: row["bridge_ordinal"])
        need(len(reroute_rows) == len(reroute_source_graph_ids) == 10, "reroute finding exhaustion")

        disposition_wire, disposition_plain = gzip_rows(disposition_rows)
        ready_wire, ready_plain = gzip_rows(ready_rows)
        blocked_wire, blocked_plain = gzip_rows(blocked_rows)
        reroute_wire, reroute_plain = gzip_rows(reroute_rows)
        disposition_descriptor = ledger_descriptor(DISPOSITION_LEDGER_NAME, DISPOSITION_ROW_SCHEMA, disposition_rows, disposition_wire, disposition_plain)
        ready_descriptor = ledger_descriptor(READY_LEDGER_NAME, READY_ROW_SCHEMA, ready_rows, ready_wire, ready_plain)
        blocked_descriptor = ledger_descriptor(BLOCKED_LEDGER_NAME, BLOCKED_ROW_SCHEMA, blocked_rows, blocked_wire, blocked_plain)
        reroute_descriptor = ledger_descriptor(REROUTE_LEDGER_NAME, REROUTE_ROW_SCHEMA, reroute_rows, reroute_wire, reroute_plain)

        body = {
            "schema": SCHEMA,
            "status": STATUS,
            "producer_source": producer_record(),
            "source_pins": [pin.__dict__ for pin in PINS],
            "upstream_seal_bindings": {
                "C10_manifest_sha256": PIN_BY_ROLE["C10_MANIFEST"].sha256,
                "C9_manifest_sha256": PIN_BY_ROLE["C9_MANIFEST"].sha256,
                "C7_manifest_sha256": PIN_BY_ROLE["C7_MANIFEST"].sha256,
                "C6_manifest_sha256": PIN_BY_ROLE["C6_MANIFEST"].sha256,
                "C5_manifest_sha256": PIN_BY_ROLE["C5_MANIFEST"].sha256,
                "C4_manifest_sha256": PIN_BY_ROLE["C4_MANIFEST"].sha256,
                "R235_manifest_sha256": PIN_BY_ROLE["R235_MANIFEST"].sha256,
                "R236_manifest_sha256": PIN_BY_ROLE["R236_MANIFEST"].sha256,
                "R242_manifest_sha256": PIN_BY_ROLE["R242_MANIFEST"].sha256,
                "R248_manifest_sha256": PIN_BY_ROLE["R248_MANIFEST"].sha256,
                "R245_manifest_sha256": PIN_BY_ROLE["R245_MANIFEST"].sha256,
            },
            "disposition_census": {
                "positive_graph_side_relations": 10_118,
                "CANDIDATE_READY_ROUTING": 9_950,
                "BLOCKED": 168,
                "ADJACENT_DOMAIN_REQUIRED": 152,
                "OUTSIDE_DOMAIN_TRACE_AUTHORITY_REQUIRED": 16,
                "missing_local_shared_reroute_findings": 10,
            },
            "candidate_ready_class_census": {
                "R235_TARGET_POSITIVE_PARTIAL_BASE": 8_864,
                "R235_SOURCE_EXACT_FACE_FULL_BASE": 552,
                "R235D_SOURCE_EXACT_FACE_FULL_BASE": 6,
                "R242_UNIQUE_GRAPH_FULL_PATCH": 528,
            },
            "component_forecast_only": {
                "CANDIDATE_READY_same_base_root_relations": 5_302,
                "CANDIDATE_READY_cross_component_relations": 4_648,
                "CANDIDATE_READY_distinct_cross_component_pairs": 4_500,
                "BLOCKED_same_base_root_relations": 32,
                "BLOCKED_cross_component_relations": 136,
                "graph_to_sheet_set_equality_available": False,
                "may_be_promoted_to_DSU_edges_now": False,
                "DSU_edge_credit": 0,
                "DSU_union_credit": 0,
            },
            "formal_credit": ZERO_DOWNSTREAM,
            "strict_nonpromotion": {
                "C10_exact_feature_support_AST_is_graph_sheet_set_equality": False,
                "candidate_ready_routing_is_local_graph_side_theorem": False,
                "local_graph_side_physical_incidence_proved": False,
                "one_sided_trace_proved": False,
                "local_graph_side_theorem_is_representation_pullback": False,
                "cross_component_forecast_is_DSU_edge_or_union": False,
                "normalized_support_sealed": False,
                "B1A_permitted": False,
                "B2_permitted": False,
                "maximality_permitted": False,
                "CM2": "NO-GO_FOR_CLAIM",
            },
            "disposition_ledger": disposition_descriptor,
            "ready_local_theorem_ledger": ready_descriptor,
            "blocked_ledger": blocked_descriptor,
            "missing_local_shared_reroute_findings": reroute_descriptor,
            "required_next": {
                "materialize_exact_side_carriers": True,
                "prove_closure_incidence": True,
                "prove_one_sided_collar_or_common_boundary_traces": True,
                "close_152_R235_adjacent_domain_traces": True,
                "close_16_R235D_outside_domain_traces": True,
                "R235D_direct_R236_binding_completed_in_routing_census": True,
                "all_three_R245_edges_bound_for_each_R242_graph": True,
                "materialize_and_prove_10_missing_source_shared_reroutes": True,
                "prove_graph_to_sheet_set_equality_and_representation_pullbacks": True,
                "seal_theorem_to_edge_before_any_DSU_reclosure": True,
                "B1A": "NOT_AUTHORIZED",
                "B2": "NOT_AUTHORIZED",
            },
            "seed_serialized_or_semantically_used": False,
        }
        result = {**body, "result_sha256": object_sha(body)}
        snapshot.final()
    return result, disposition_wire, ready_wire, blocked_wire, reroute_wire


def write_once(directory: Path, filename: str, payload: bytes) -> None:
    path = directory / filename
    need(not path.exists(), "publish no-clobber:" + filename)
    file_descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW | os.O_CLOEXEC, 0o600)
    try:
        offset = 0
        while offset < len(payload):
            offset += os.write(file_descriptor, payload[offset:])
        os.fsync(file_descriptor)
    finally:
        os.close(file_descriptor)
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
    result, disposition_wire, ready_wire, blocked_wire, reroute_wire = build()
    result_wire = canonical(result)
    if arguments.print_result:
        sys.stdout.buffer.write(result_wire + b"\n")
        return 0
    if arguments.publish:
        directory = ROOT
    else:
        directory = Path(arguments.candidate_dir).resolve()
        need(os.path.commonpath((str(directory), str(ROOT.resolve()))) != str(ROOT.resolve()), "candidate outside deliverables")
        directory.mkdir(mode=0o700, parents=False, exist_ok=False)
    outputs = (
        (DISPOSITION_LEDGER_NAME, disposition_wire),
        (READY_LEDGER_NAME, ready_wire),
        (BLOCKED_LEDGER_NAME, blocked_wire),
        (REROUTE_LEDGER_NAME, reroute_wire),
        (RESULT_NAME, result_wire),
    )
    records = []
    for filename, payload in outputs:
        write_once(directory, filename, payload)
        records.append({"filename": filename, "size": len(payload), "sha256": hashlib.sha256(payload).hexdigest()})
    for record in reversed(records):
        info = os.stat(directory / record["filename"], follow_symlinks=False)
        need(stat.S_ISREG(info.st_mode) and info.st_nlink == 1 and info.st_size == record["size"], "reverse publication identity")
        with open(directory / record["filename"], "rb") as stream:
            need(hashlib.sha256(stream.read()).hexdigest() == record["sha256"], "reverse publication digest")
    print(json.dumps({"status": result["status"], "result_sha256": result["result_sha256"], "published_result_last": True, "files": records}, sort_keys=True, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
