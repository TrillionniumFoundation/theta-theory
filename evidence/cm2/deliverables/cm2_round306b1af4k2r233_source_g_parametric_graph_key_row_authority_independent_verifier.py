#!/usr/bin/env python3
"""Harden the frozen Round233 graph-key rows without minting global credit.

This verifier treats the old Round233 producer and verifier as inert bytes.  It
opens every authority input through held file descriptors, hashes every input
twice, strictly decodes the selected JSON, independently reruns the frozen
interval-geometry traversal, and binds every output row to every source row
that was actually used.  The frozen R179/R174/Gate3 engine chain is loaded
from already-open file descriptors; this is an engineering replay boundary,
not a new proof of those engines' mathematical semantics.

The only positive scope is local Round233 parametric graph-key row authority.
Full support, incidence/equivalence, representation pullback, B1A, B2,
maximality, and CM2 credits remain exactly zero.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import gc
import hashlib
import json
import os
from pathlib import Path
import stat
import sys
import tempfile
import types
from typing import Any, Final

from flint import ctx, __version__ as FLINT_VERSION


class Blocked(RuntimeError):
    pass


def need(condition: bool, label: str) -> None:
    if not condition:
        raise Blocked(label)


def type_strict_equal(left: Any, right: Any) -> bool:
    if type(left) is not type(right):
        return False
    if type(right) is dict:
        return set(left) == set(right) and all(
            type_strict_equal(left[key], right[key]) for key in right
        )
    if type(right) in {list, tuple}:
        return len(left) == len(right) and all(
            type_strict_equal(a, b) for a, b in zip(left, right, strict=True)
        )
    return bool(left == right)


def strict_need(left: Any, right: Any, label: str) -> None:
    need(type_strict_equal(left, right), label)


HERE: Final = Path(__file__).parent
PREFIX: Final = "cm2_round306b1af4k2r233_source_g_parametric_graph_key_row_authority_"
LEDGER_NAME: Final = PREFIX + "row_commitment_ledger.json"
VERIFICATION_NAME: Final = PREFIX + "verification.json"
ATTACK_NAME: Final = PREFIX + "attack_suite.json"
OLD_SCHEMA: Final = "cm2.round233.source-g-outgoing-seam-parametric-graph-key-partition.v1"
LEDGER_SCHEMA: Final = "cm2.round306b1af4k2r233.source-g-parametric-graph-key-row-authority.ledger.v1"
VERIFICATION_SCHEMA: Final = "cm2.round306b1af4k2r233.source-g-parametric-graph-key-row-authority.verification.v1"
ATTACK_SCHEMA: Final = "cm2.round306b1af4k2r233.source-g-parametric-graph-key-row-authority.attack-suite.v1"
STATUS: Final = "PASS_R233_LOCAL_GRAPH_KEY_ROW_AUTHORITY_ONLY__ZERO_GLOBAL_FORMAL_CREDIT"
ROW_CAP: Final = 8_388_608

# The old manifest is deliberately first.  Its four entries are validated
# before any old payload is decoded.  The two misplaced narrative files are
# pinned for audit, but are explicitly excluded from authority membership.
PINS: Final = (
    ("R233_MANIFEST", "cm2_round233_source_g_outgoing_seam_parametric_graph_key_partition_manifest.sha256", 582, "6e5d8babad93fbfad5a6656891f8600a3cc831c0f1d02085f8abe1c46a978459"),
    ("R233_SOURCE", "cm2_round233_source_g_outgoing_seam_parametric_graph_key_partition.py", 13_285, "820085392577265eabcbdfea19f095e942736c0fe938554b811b04f1bd1f3546"),
    ("R233_CERTIFICATE", "cm2_round233_source_g_outgoing_seam_parametric_graph_key_partition_certificate.json", 6_808_749, "cb2f74daa9836841ce311d8d555c2d94ba897f346a63c1e29551d7f99e8d1a41"),
    ("R233_VERIFIER", "cm2_round233_source_g_outgoing_seam_parametric_graph_key_partition_verifier.py", 14_492, "6c2eb0729a90866c4d98743462f5e379764c7ce8bbfe330680b18d49965b516d"),
    ("R233_VERIFICATION", "cm2_round233_source_g_outgoing_seam_parametric_graph_key_partition_verification.json", 871, "184121d738cfcac44f06e65d14cf8581bc82c215ecf6f6bfb1ac2f2baf97bc63"),
    ("R233_MISPLACED_REPORT", "deliverables/cm2_round233_source_g_outgoing_seam_parametric_graph_key_partition_report.md", 2_918, "d3273a8679e774af5012590033a220a0324d75961e9fd7cff7f70fb89a05e79d"),
    ("R233_MISPLACED_COLD", "deliverables/cm2_round233_source_g_outgoing_seam_parametric_graph_key_partition_cold_replay.md", 547, "2c2bf8c259c6f695fd3516f4d06759ac5245649499d3fd846af237c13a63e9c0"),
    ("R179_SOURCE", "cm2_round179_source_g_residual_tube_arrangement.py", 63_683, "8c568c58d82708a7ab549f126c1fcedfccff563d1d00e3c1f7e6545b4b0d29ab"),
    ("R179_ROWS", "cm2_round179_source_g_residual_tube_arrangement_rows.json", 131_273_924, "f20b42c1fed781779b537b4d45bf44233eae1ed3ee620b95177a80f0eb2b5e42"),
    ("R220_CERTIFICATE", "cm2_round220_source_g_round179_resolved_child_boundary_atlas_certificate.json", 294_422_681, "569a7849b53805ff4deca0eff9a6938a897942d3d682dfef27c27559135ce974"),
    ("R231_CERTIFICATE", "cm2_round231_source_g_outgoing_seam_depth6_materialization_certificate.json", 91_909_341, "7bc861ef4f2c2962dcf7c8e38839af2ec12477f9fc42d808be1b48d858745374"),
    ("R232_CERTIFICATE", "cm2_round232_source_g_depth6_whole_origin_promotion_certificate.json", 3_596_500, "a33d14fd7fd0ca0bb8e64efefd97be0839a5a8107b759f2219c14580ef3aa8c0"),
    ("FIRST_HIT_ENGINE", "cm2_gate3_candidate_first_hit_cert.py", 13_832, "6d224d74cda186a40ef9956d1dd6556d5a7b9f506d47c942427ceb66fd705bd2"),
    ("GE_ENGINE", "cm2_gate3_ge_interval_atlas_cert.py", 17_052, "ab120f85a263f3cb0697d8a40bc9ed2bf12b361aa7c54940c214b6fd85b17e2b"),
    ("ATLAS_ENGINE", "cm2_gate3_eight_cell_symmetry_atlas_cert.py", 18_141, "d867f5cb03691289033d1a0d0e277a03e8395d70aae7e0689446d7aa63eac3da"),
    ("R174_ENGINE", "cm2_round174_source_g_unique_first_dynamic_occurrence_materialization_verifier.py", 96_797, "c7ead7c9cb8b4d7b8680e64bfb7870e5c5f5e39277e7c7d3d08a62b600f5c058"),
)

OLD_MANIFEST_MEMBERS: Final = (
    ("cm2_round233_source_g_outgoing_seam_parametric_graph_key_partition.py", PINS[1][3]),
    ("cm2_round233_source_g_outgoing_seam_parametric_graph_key_partition_certificate.json", PINS[2][3]),
    ("cm2_round233_source_g_outgoing_seam_parametric_graph_key_partition_verifier.py", PINS[3][3]),
    ("cm2_round233_source_g_outgoing_seam_parametric_graph_key_partition_verification.json", PINS[4][3]),
)


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True, allow_nan=False).encode("ascii")


def object_sha(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def dup_reject(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for key, value in pairs:
        need(key not in out, "duplicate key:" + key)
        out[key] = value
    return out


def reject_number(token: str) -> Any:
    raise Blocked("nonintegral/nonfinite number:" + token)


def strict_decode(raw: bytes, label: str, maximum: int) -> Any:
    need(0 < len(raw) <= maximum, "raw size:" + label)
    need(not raw.startswith(b"\xef\xbb\xbf") and b"\x00" not in raw, "raw encoding:" + label)
    try:
        value = json.loads(
            raw.decode("utf-8"), object_pairs_hook=dup_reject,
            parse_float=reject_number, parse_constant=reject_number,
        )
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise Blocked("decode:" + label) from exc

    def walk(item: Any) -> None:
        if type(item) is dict:
            for key, child in item.items():
                need(type(key) is str, "key type:" + label)
                walk(key); walk(child)
        elif type(item) is list:
            for child in item: walk(child)
        elif type(item) is str:
            need("\x00" not in item and not any(0xD800 <= ord(c) <= 0xDFFF for c in item), "string:" + label)
        else:
            need(item is None or type(item) in {bool, int}, "scalar:" + label)
    walk(value)
    return value


def row_wire(row: Any, label: str) -> bytes:
    data = canonical(row)
    need(len(data) <= ROW_CAP, "final canonical row cap:" + label)
    return data


def file_identity(info: os.stat_result) -> tuple[int, ...]:
    return (info.st_dev, info.st_ino, info.st_mode, info.st_nlink, info.st_size, info.st_mtime_ns, info.st_ctime_ns)


def dir_identity(info: os.stat_result) -> tuple[int, ...]:
    return (info.st_dev, info.st_ino, info.st_mode)


class Snapshot:
    def __init__(self) -> None:
        self.rootfd = -1
        self.rootstat: os.stat_result | None = None
        self.nestedfd = -1
        self.nestedstat: os.stat_result | None = None
        self.fds: dict[str, int] = {}
        self.modules: list[str] = []
        self.rows = {label: (name, size, sha) for label, name, size, sha in PINS}

    @staticmethod
    def hash_fd(fd: int) -> str:
        os.lseek(fd, 0, os.SEEK_SET)
        out = hashlib.sha256()
        while True:
            chunk = os.read(fd, 1_048_576)
            if not chunk:
                return out.hexdigest()
            out.update(chunk)

    def parent_and_name(self, relative: str) -> tuple[int, str]:
        parts = Path(relative).parts
        if len(parts) == 1:
            return self.rootfd, parts[0]
        need(parts == ("deliverables", parts[-1]) and len(parts) == 2, "safe relative pin path:" + relative)
        need(self.nestedfd >= 0, "nested directory open")
        return self.nestedfd, parts[-1]

    def __enter__(self) -> "Snapshot":
        before = os.stat(HERE, follow_symlinks=False)
        need(stat.S_ISDIR(before.st_mode) and not HERE.is_symlink(), "deliverables directory")
        self.rootfd = os.open(HERE, os.O_RDONLY | getattr(os, "O_DIRECTORY", 0) | getattr(os, "O_NOFOLLOW", 0))
        held = os.fstat(self.rootfd)
        need(dir_identity(before) == dir_identity(held), "root directory race")
        self.rootstat = held
        nested_before = os.stat("deliverables", dir_fd=self.rootfd, follow_symlinks=False)
        need(stat.S_ISDIR(nested_before.st_mode), "nested deliverables regular directory")
        self.nestedfd = os.open("deliverables", os.O_RDONLY | getattr(os, "O_DIRECTORY", 0) | getattr(os, "O_NOFOLLOW", 0), dir_fd=self.rootfd)
        nested_held = os.fstat(self.nestedfd)
        need(dir_identity(nested_before) == dir_identity(nested_held), "nested directory race")
        self.nestedstat = nested_held
        try:
            for label, relative, size, expected_sha in PINS:
                parent, filename = self.parent_and_name(relative)
                before_file = os.stat(filename, dir_fd=parent, follow_symlinks=False)
                need(stat.S_ISREG(before_file.st_mode) and before_file.st_nlink == 1, "regular/nlink:" + label)
                need(before_file.st_size == size, "size:" + label)
                fd = os.open(filename, os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0), dir_fd=parent)
                opened = os.fstat(fd)
                need(file_identity(before_file) == file_identity(opened), "open race:" + label)
                self.fds[label] = fd
                first = self.hash_fd(fd); second = self.hash_fd(fd)
                need(first == second == expected_sha, "two-pass pin:" + label)
                after_file = os.stat(filename, dir_fd=parent, follow_symlinks=False)
                need(file_identity(opened) == file_identity(after_file), "post-hash path:" + label)
            return self
        except BaseException:
            self.__exit__(None, None, None)
            raise

    def bytes(self, label: str) -> bytes:
        fd = self.fds[label]
        os.lseek(fd, 0, os.SEEK_SET)
        chunks: list[bytes] = []
        total = 0
        while True:
            chunk = os.read(fd, 1_048_576)
            if not chunk:
                need(total == self.rows[label][1], "held size:" + label)
                return b"".join(chunks)
            total += len(chunk); chunks.append(chunk)

    def load_module(self, module_name: str, label: str) -> types.ModuleType:
        need(module_name not in sys.modules, "module preloaded:" + module_name)
        source = self.bytes(label)
        module = types.ModuleType(module_name)
        module.__file__ = str(HERE / self.rows[label][0])
        module.__package__ = ""
        module.__cached__ = None
        sys.modules[module_name] = module
        self.modules.append(module_name)
        try:
            exec(compile(source, module.__file__, "exec"), module.__dict__)
            return module
        except BaseException:
            sys.modules.pop(module_name, None)
            self.modules.remove(module_name)
            raise

    def final_revalidate(self) -> None:
        need(self.rootstat is not None and self.nestedstat is not None, "snapshot active")
        need(dir_identity(self.rootstat) == dir_identity(os.fstat(self.rootfd)), "held root changed")
        need(dir_identity(self.rootstat) == dir_identity(os.stat(HERE, follow_symlinks=False)), "root path changed")
        need(dir_identity(self.nestedstat) == dir_identity(os.fstat(self.nestedfd)), "held nested changed")
        need(dir_identity(self.nestedstat) == dir_identity(os.stat("deliverables", dir_fd=self.rootfd, follow_symlinks=False)), "nested path changed")
        for label, relative, size, expected_sha in PINS:
            parent, filename = self.parent_and_name(relative)
            held = os.fstat(self.fds[label])
            path = os.stat(filename, dir_fd=parent, follow_symlinks=False)
            need(file_identity(held) == file_identity(path), "final FD/path:" + label)
            need(held.st_size == size and self.hash_fd(self.fds[label]) == expected_sha, "final pin:" + label)

    def __exit__(self, *_args: Any) -> None:
        for module_name in reversed(self.modules):
            sys.modules.pop(module_name, None)
        self.modules.clear()
        for fd in self.fds.values():
            try: os.close(fd)
            except OSError: pass
        self.fds.clear()
        for field in ("nestedfd", "rootfd"):
            fd = getattr(self, field)
            if fd >= 0:
                try: os.close(fd)
                except OSError: pass
                setattr(self, field, -1)


def validate_old_manifest(raw: bytes) -> dict[str, Any]:
    try:
        text = raw.decode("ascii")
    except UnicodeDecodeError as exc:
        raise Blocked("old manifest encoding") from exc
    need(text.endswith("\n"), "old manifest newline")
    entries = []
    for line in text.splitlines():
        parts = line.split("  ")
        need(len(parts) == 2 and len(parts[0]) == 64 and all(c in "0123456789abcdef" for c in parts[0]), "old manifest syntax")
        need(parts[1] == os.path.basename(parts[1]), "old manifest basename")
        entries.append((parts[1], parts[0]))
    strict_need(tuple(entries), OLD_MANIFEST_MEMBERS, "old manifest exact ordered membership")
    return {
        "entry_count": 4,
        "ordered_entries_sha256": object_sha([list(row) for row in entries]),
        "report_in_manifest": False,
        "cold_replay_in_manifest": False,
        "misplaced_narratives_pinned_for_audit_only": True,
    }


def load_envelope(raw: bytes, schema: str, label: str, maximum: int) -> dict[str, Any]:
    document = strict_decode(raw, label, maximum)
    need(type(document) is dict and set(document) == {"schema", "result", "result_sha256"}, "envelope:" + label)
    strict_need(document["schema"], schema, "schema:" + label)
    strict_need(document["result_sha256"], object_sha(document["result"]), "result digest:" + label)
    need(canonical(document) + b"\n" == raw, "canonical wire:" + label)
    return document


def unpack(document: dict[str, Any], table: str) -> list[dict[str, Any]]:
    columns = document["row_column_schemas"][table]
    rows = []
    for packed in document[table]:
        need(type(packed) is list and len(packed) == len(columns), "packed width:" + table)
        rows.append(dict(zip(columns, packed, strict=True)))
    return rows


def index_rows(rows: list[dict[str, Any]], id_field: str, label: str) -> dict[str, tuple[int, dict[str, Any]]]:
    out: dict[str, tuple[int, dict[str, Any]]] = {}
    for ordinal, row in enumerate(rows):
        need(type(row) is dict and type(row.get(id_field)) is str, "row shape:" + label)
        row_id = row[id_field]
        need(row_id not in out, "duplicate row id:" + label)
        row_wire(row, label)
        out[row_id] = (ordinal, row)
    return out


def row_ref(source_ordinal: int, row: dict[str, Any], id_field: str, label: str) -> list[Any]:
    return [source_ordinal, row[id_field], hashlib.sha256(row_wire(row, label)).hexdigest()]


def commit_table(selected: list[tuple[int, dict[str, Any]]], id_field: str, label: str) -> tuple[dict[str, Any], list[list[Any]]]:
    commitments: list[list[Any]] = []
    hashes: list[str] = []
    seen: set[str] = set()
    previous_source = -1
    rows: list[dict[str, Any]] = []
    for selection_ordinal, (source_ordinal, row) in enumerate(selected):
        need(source_ordinal > previous_source, "selected source order:" + label)
        previous_source = source_ordinal
        row_id = row[id_field]
        need(row_id not in seen, "selected unique:" + label)
        seen.add(row_id)
        sha = hashlib.sha256(row_wire(row, label)).hexdigest()
        commitments.append([selection_ordinal, source_ordinal, row_id, sha])
        hashes.append(sha); rows.append(row)
    summary = {
        "id_field": id_field,
        "row_count": len(rows),
        "ordered_selected_rows_sha256": object_sha(rows),
        "ordered_row_digest_sequence_sha256": object_sha(hashes),
        "unordered_row_digest_multiset_sha256": object_sha(sorted(hashes)),
        "source_ordinal_sequence_sha256": object_sha([row[1] for row in commitments]),
        "first_row_sha256": hashes[0] if hashes else None,
        "last_row_sha256": hashes[-1] if hashes else None,
    }
    return summary, commitments


def signature(row: dict[str, Any]) -> dict[str, Any]:
    return {
        "source_chart": row["chart"], "target_lift": row["owner_target"],
        "ordered_integer_wall_events": row["ordered_integer_wall_events"],
        "signed_wall_word": row["signed_wall_word"], "roof": row["roof"],
        "outgoing_cell": row["outgoing_cell"], "target_chart": row["target_chart"],
        "official_key_row": row["official_key_row"],
        "official_key_ordinal": row["official_key_ordinal"],
        "official_key_id": row["official_key_id"],
    }


def side_signature(base: dict[str, Any], cell: str) -> dict[str, Any]:
    out = dict(base); out["outgoing_cell"] = cell; out["target_chart"] = f"{base['target_lift'][0]}:{cell}"
    return out


def cell(axis: str, sign_name: str) -> str:
    need(sign_name in {"STRICT_POSITIVE", "STRICT_NEGATIVE"}, "strict sign:" + axis)
    if axis == "x": return "E" if sign_name == "STRICT_POSITIVE" else "W"
    return "N" if sign_name == "STRICT_POSITIVE" else "S"


def rebuild(snapshot: Snapshot) -> tuple[dict[str, Any], dict[str, Any]]:
    old_manifest = validate_old_manifest(snapshot.bytes("R233_MANIFEST"))
    old_candidate = load_envelope(snapshot.bytes("R233_CERTIFICATE"), OLD_SCHEMA, "R233 certificate", 10_000_000)
    old_verification = load_envelope(
        snapshot.bytes("R233_VERIFICATION"),
        "cm2.round233.source-g-outgoing-seam-parametric-graph-key-partition.verification.v1",
        "R233 verification", 10_000,
    )
    candidate = old_candidate["result"]
    candidate_rows = candidate["parametric_graph_key_partition_rows"]
    strict_need(len(candidate_rows), 3_148, "candidate row census")
    strict_need(candidate["parametric_graph_key_partition_rows_sha256"], object_sha(candidate_rows), "candidate table digest")
    strict_need(old_verification["result"]["candidate_sha256"], PINS[2][3], "old verification candidate pin")
    strict_need(old_verification["result"]["candidate_result_sha256"], old_candidate["result_sha256"], "old verification result pin")

    r231_document = load_envelope(
        snapshot.bytes("R231_CERTIFICATE"),
        "cm2.round231.source-g-outgoing-seam-depth6-materialization.v1",
        "R231 certificate", 100_000_000,
    )
    r231 = r231_document["result"]
    root_rows = r231["root_summary_rows"]
    released_rows = r231["resolved_descendant_rows"]
    strict_need(len(root_rows), 5_368, "R231 root census")
    strict_need(len(released_rows), 22_348, "R231 released census")
    root_index = index_rows(root_rows, "root_summary_id", "R231 root")
    unresolved_rows = [(i, row) for i, row in enumerate(root_rows) if type(row["depth6_retained_frontier_count"]) is int and row["depth6_retained_frontier_count"] > 0]
    resolved_root_rows = [(i, row) for i, row in enumerate(root_rows) if type(row["depth6_retained_frontier_count"]) is int and row["depth6_retained_frontier_count"] == 0]
    strict_need(len(unresolved_rows), 3_148, "R231 unresolved root census")
    strict_need(len(resolved_root_rows), 2_220, "R231 zero-frontier root census")
    unresolved_by_interface = {row["Round220_split_interface_id"]: (i, row) for i, row in unresolved_rows}
    need(len(unresolved_by_interface) == 3_148, "R231 unresolved interface unique")

    selected_released = [(i, row) for i, row in enumerate(released_rows) if row["Round220_split_interface_id"] in unresolved_by_interface]
    strict_need(len(selected_released), 15_544, "selected released descendant census")
    released_by_interface: dict[str, list[tuple[int, dict[str, Any]]]] = defaultdict(list)
    for item in selected_released:
        released_by_interface[item[1]["Round220_split_interface_id"]].append(item)

    r232_document = load_envelope(
        snapshot.bytes("R232_CERTIFICATE"),
        "cm2.round232.source-g-depth6-whole-origin-promotion.v1",
        "R232 certificate", 5_000_000,
    )
    r232_rows = r232_document["result"]["whole_origin_promotion_rows"]
    strict_need(len(r232_rows), 2_220, "R232 prior census")
    r232_index = index_rows(r232_rows, "whole_origin_promotion_row_id", "R232 promotion")
    prior_interfaces = {row["Round220_split_interface_id"] for row in r232_rows}
    zero_frontier_interfaces = {row["Round220_split_interface_id"] for _, row in resolved_root_rows}
    strict_need(prior_interfaces, zero_frontier_interfaces, "R232 exact zero-frontier universe")

    candidate_index = index_rows(candidate_rows, "parametric_graph_partition_row_id", "R233 output")
    candidate_interfaces = {row["Round220_split_interface_id"] for row in candidate_rows}
    strict_need(candidate_interfaces, set(unresolved_by_interface), "R233 exact unresolved universe")
    need(not (candidate_interfaces & prior_interfaces) and len(candidate_interfaces | prior_interfaces) == 5_368, "channel partition")

    r179_document = load_envelope(
        snapshot.bytes("R179_ROWS"),
        "cm2.round179.source-g-residual-tube-arrangement-rows.v1",
        "R179 rows", 140_000_000,
    )
    r179 = r179_document["result"]
    origins_all = unpack(r179, "origin_tube_rows")
    retained_all = unpack(r179, "retained_3d_child_rows")
    resolved_all = unpack(r179, "resolved_3d_child_rows")
    strict_need((len(origins_all), len(retained_all), len(resolved_all)), (62_012, 106_680, 17_192), "R179 table census")
    origin_index = index_rows(origins_all, "origin_row_id", "R179 origin")
    retained_index = index_rows(retained_all, "row_id", "R179 retained")
    resolved_index = index_rows(resolved_all, "row_id", "R179 resolved")
    del r179_document, r179, origins_all, retained_all, resolved_all; gc.collect()

    r220_document = load_envelope(
        snapshot.bytes("R220_CERTIFICATE"),
        "cm2.round220.source-g-round179-resolved-child-boundary-atlas.v1",
        "R220 certificate", 310_000_000,
    )
    table220 = r220_document["result"]["coordinate_boundary_atlas"]["tables"]["one_step_split_interface_rows"]
    strict_need(table220["row_count"], 13_076, "R220 table census")
    interfaces_all = [dict(zip(table220["columns"], packed, strict=True)) for packed in table220["rows"]]
    interface_index = index_rows(interfaces_all, "split_interface_id", "R220 interface")
    del r220_document, table220, interfaces_all; gc.collect()

    # Load the frozen engine chain only after every authority manifest and JSON
    # envelope above has been pinned and checked.
    snapshot.load_module("cm2_gate3_candidate_first_hit_cert", "FIRST_HIT_ENGINE")
    snapshot.load_module("cm2_gate3_ge_interval_atlas_cert", "GE_ENGINE")
    snapshot.load_module("cm2_gate3_eight_cell_symmetry_atlas_cert", "ATLAS_ENGINE")
    snapshot.load_module("cm2_round174_source_g_unique_first_dynamic_occurrence_materialization_verifier", "R174_ENGINE")
    r179_engine = snapshot.load_module("cm2_round179_source_g_residual_tube_arrangement", "R179_SOURCE")
    ctx.prec = 192

    selected_origins: dict[str, tuple[int, dict[str, Any]]] = {}
    selected_retained: dict[str, tuple[int, dict[str, Any]]] = {}
    selected_siblings: dict[str, tuple[int, dict[str, Any]]] = {}
    selected_interfaces: dict[str, tuple[int, dict[str, Any]]] = {}
    conclusion_rows: list[list[Any]] = []
    reconstructed: list[dict[str, Any]] = []
    face_histogram: Counter[str] = Counter()
    derivative_histogram: Counter[str] = Counter()
    side_histogram: Counter[str] = Counter()
    exact_keys: set[int] = set()
    released_count = 0
    engine_chain = [[label, PINS[[row[0] for row in PINS].index(label)][3]] for label in ("FIRST_HIT_ENGINE", "GE_ENGINE", "ATLAS_ENGINE", "R174_ENGINE", "R179_SOURCE")]
    engine_chain_sha = object_sha(engine_chain)
    prior_refs = [row_ref(i, row, "whole_origin_promotion_row_id", "R232 promotion") for i, row in enumerate(r232_rows)]
    global_universe_commitment_sha = object_sha({
        "engine_chain_sha256": engine_chain_sha,
        "unresolved_interfaces": sorted(candidate_interfaces),
        "prior_promoted_interfaces": sorted(prior_interfaces),
        "prior_promotion_rows": prior_refs,
        "channel_root_count": 5_368,
    })

    for interface_id in sorted(candidate_interfaces):
        root_ordinal, summary = unresolved_by_interface[interface_id]
        interface_ordinal, interface = interface_index[interface_id]
        retained_id = summary["Round179_retained_child_row_id"]
        retained_ordinal, retained_row = retained_index[retained_id]
        origin_ordinal, origin = origin_index[retained_row["origin_row_id"]]
        strict_need((origin["resolved_child_count"], origin["retained_child_count"], origin["guard_child_count"]), (1, 1, 0), "origin partition:" + interface_id)
        strict_need(origin["original_reason_labels"], ["outgoing_chart_seam"], "origin reason:" + interface_id)
        sibling_id = interface["lower_child_row_id"] if interface["lower_child_kind"] == "RESOLVED" else interface["upper_child_row_id"]
        sibling_ordinal, sibling = resolved_index[sibling_id]
        sibling_signature = signature(sibling)
        strict_need(sibling_signature["target_lift"], origin["owner_target"], "sibling owner:" + interface_id)
        box = r179_engine.box_from(retained_row["box"], len(retained_row["refinement_path"]), retained_row["row_id"])
        geometry = r179_engine.interval_geometry(retained_row["chart"], origin["owner_target"], box)
        x_sign = r179_engine.sign(geometry["outgoing_x"][0])
        y_sign = r179_engine.sign(geometry["outgoing_y"][0])
        derivative_sign = r179_engine.sign(geometry["outgoing_equality"][1][0])
        x_cell = cell("x", x_sign); y_cell = cell("y", y_sign)
        x_signature = side_signature(sibling_signature, x_cell)
        y_signature = side_signature(sibling_signature, y_cell)
        strict_need(x_signature["official_key_id"], y_signature["official_key_id"], "shared key:" + interface_id)
        lower_face = r179_engine.interval_geometry(retained_row["chart"], origin["owner_target"], r179_engine.fixed_axis_face(box, "t", False))["outgoing_equality"][0]
        upper_face = r179_engine.interval_geometry(retained_row["chart"], origin["owner_target"], r179_engine.fixed_axis_face(box, "t", True))["outgoing_equality"][0]
        face_classification = r179_engine.face_classification(lower_face, upper_face)
        lower_cell = y_cell if derivative_sign == "STRICT_POSITIVE" else x_cell
        upper_cell = x_cell if derivative_sign == "STRICT_POSITIVE" else y_cell
        released = released_by_interface[interface_id]
        released_count += len(released)
        allowed = {object_sha(x_signature), object_sha(y_signature)}
        need(all(object_sha(row["local_return_signature"]) in allowed for _, row in released), "released side:" + interface_id)
        need(all(row["local_return_signature"]["official_key_id"] == sibling_signature["official_key_id"] for _, row in released), "released key:" + interface_id)
        expected = {
            "parametric_graph_partition_row_id": "round233-graph-key-partition:" + object_sha(interface_id),
            "Round220_split_interface_id": interface_id,
            "origin_row_id": retained_row["origin_row_id"],
            "Round179_resolved_sibling_row_id": sibling_id,
            "Round179_retained_child_row_id": retained_id,
            "source_chart": retained_row["chart"], "target_lift": origin["owner_target"],
            "equation": "target_normal_x^2-target_normal_y^2=0",
            "strict_t_derivative_sign": derivative_sign,
            "strict_outgoing_x_sign": x_sign, "strict_outgoing_y_sign": y_sign,
            "lower_t_side_outgoing_cell": lower_cell, "upper_t_side_outgoing_cell": upper_cell,
            "x_dominant_signature": x_signature, "y_dominant_signature": y_signature,
            "shared_official_key_row": sibling_signature["official_key_row"],
            "shared_official_key_ordinal": sibling_signature["official_key_ordinal"],
            "shared_official_key_id": sibling_signature["official_key_id"],
            "retained_root_t_face_classification": face_classification,
            "seam_dimension": 2, "seam_three_dimensional_coordinate_volume": 0,
            "retained_root_exact_key_constant_off_seam": True,
            "whole_origin_local_exact_key_disposition_credit": 1,
            "known_block_incidence_credit": 0, "maximal_component_credit": 0,
            "global_exact_key_fibre_credit": 0,
        }
        output_ordinal, got = candidate_index[expected["parametric_graph_partition_row_id"]]
        strict_need(got, expected, "exact candidate row:" + interface_id)
        strict_need(got["whole_origin_local_exact_key_disposition_credit"], 1, "local credit integer:" + interface_id)
        for key in ("known_block_incidence_credit", "maximal_component_credit", "global_exact_key_fibre_credit"):
            strict_need(got[key], 0, "zero global credit:" + key + ":" + interface_id)
        input_object = {
            "engine_chain_sha256": engine_chain_sha,
            "global_universe_commitment_sha256": global_universe_commitment_sha,
            "R179_origin": row_ref(origin_ordinal, origin, "origin_row_id", "R179 origin"),
            "R179_retained": row_ref(retained_ordinal, retained_row, "row_id", "R179 retained"),
            "R179_resolved_sibling": row_ref(sibling_ordinal, sibling, "row_id", "R179 resolved"),
            "R220_interface": row_ref(interface_ordinal, interface, "split_interface_id", "R220 interface"),
            "R231_root_summary": row_ref(root_ordinal, summary, "root_summary_id", "R231 root"),
            "R231_released_descendants": [row_ref(i, row, "materialized_row_id", "R231 released") for i, row in released],
        }
        output_sha = hashlib.sha256(row_wire(got, "R233 output")).hexdigest()
        input_sha = object_sha(input_object)
        conclusion_sha = object_sha({"canonical_input_commitment_sha256": input_sha, "canonical_output_row_sha256": output_sha})
        conclusion_rows.append([output_ordinal, got["parametric_graph_partition_row_id"], output_sha, input_sha, conclusion_sha])
        reconstructed.append(expected)
        selected_origins[origin["origin_row_id"]] = (origin_ordinal, origin)
        selected_retained[retained_id] = (retained_ordinal, retained_row)
        selected_siblings[sibling_id] = (sibling_ordinal, sibling)
        selected_interfaces[interface_id] = (interface_ordinal, interface)
        face_histogram[face_classification] += 1
        derivative_histogram[derivative_sign] += 1
        side_histogram[f"{lower_cell}->{upper_cell}"] += 1
        exact_keys.add(sibling_signature["official_key_ordinal"])

    reconstructed.sort(key=lambda row: row["parametric_graph_partition_row_id"])
    strict_need(candidate_rows, reconstructed, "canonical output sequence")
    conclusion_rows.sort(key=lambda row: row[0])
    strict_need(released_count, 15_544, "released cross-check total")
    expected_scope = {
        "strict_t_derivative_makes_the_zero_set_a_parametric_graph_where_present": True,
        "strict_component_signs_determine_both_open_side_charts": True,
        "both_open_side_signatures_share_one_official_exact_key": True,
        "two_dimensional_seam_has_zero_three_dimensional_coordinate_volume": True,
        "graph_existence_over_every_base_point_not_required_for_exact_key_constancy": True,
    }
    strict_need(candidate["scope_contract"], expected_scope, "candidate scope")
    strict_need(candidate["strict_nonpromotion"], {
        "known_block_incidence_credit": 0, "physical_component_credit": 0,
        "maximal_physical_component_credit": 0, "global_exact_key_fibre_credit": 0,
        "CM2": "NO-GO_FOR_CLAIM",
    }, "candidate nonpromotion")
    expected_census = {
        "previously_whole_signature_promoted_root_count": 2_220,
        "new_parametric_graph_key_partition_root_count": 3_148,
        "outgoing_seam_channel_whole_origin_local_exact_key_disposed_count": 5_368,
        "outgoing_seam_channel_root_count": 5_368,
        "released_descendants_cross_checked_count": 15_544,
        "strict_component_sign_root_count": 3_148,
        "strict_t_derivative_root_count": 3_148,
        "distinct_shared_official_key_count": len(exact_keys),
        "retained_root_t_face_classification_histogram": dict(sorted(face_histogram.items())),
        "strict_t_derivative_sign_histogram": dict(sorted(derivative_histogram.items())),
        "lower_to_upper_side_cell_histogram": dict(sorted(side_histogram.items())),
    }
    strict_need(candidate["census"], expected_census, "candidate census")

    table_sources = {
        "R179_ORIGIN": (sorted(selected_origins.values()), "origin_row_id"),
        "R179_RETAINED": (sorted(selected_retained.values()), "row_id"),
        "R179_RESOLVED_SIBLING": (sorted(selected_siblings.values()), "row_id"),
        "R220_INTERFACE": (sorted(selected_interfaces.values()), "split_interface_id"),
        # All 5,368 root summaries are selected: 3,148 feed the new rows and
        # the complementary 2,220 prove that the R232 prior set is exactly the
        # zero-frontier side of the channel partition.
        "R231_ROOT_SUMMARY": (list(enumerate(root_rows)), "root_summary_id"),
        "R231_RELEASED_DESCENDANT": (selected_released, "materialized_row_id"),
        "R232_PRIOR_PROMOTION": (list(enumerate(r232_rows)), "whole_origin_promotion_row_id"),
        "R233_PARTITION_OUTPUT": (list(enumerate(candidate_rows)), "parametric_graph_partition_row_id"),
    }
    table_commitments: dict[str, Any] = {}
    row_commitments: dict[str, Any] = {}
    for label, (rows, id_field) in table_sources.items():
        summary, commitments = commit_table(rows, id_field, label)
        table_commitments[label] = summary
        row_commitments[label] = {
            "columns": ["selection_ordinal", "source_ordinal", id_field, "canonical_row_sha256"],
            "rows": commitments,
        }
    row_commitments["R233_INPUT_BOUND_CONCLUSION"] = {
        "columns": ["source_ordinal", "parametric_graph_partition_row_id", "canonical_output_row_sha256", "canonical_input_commitment_sha256", "input_bound_conclusion_sha256"],
        "rows": conclusion_rows,
    }
    table_commitments["R233_INPUT_BOUND_CONCLUSION"] = {
        "row_count": len(conclusion_rows),
        "ordered_rows_sha256": object_sha(conclusion_rows),
        "ordered_input_commitment_sequence_sha256": object_sha([row[3] for row in conclusion_rows]),
        "ordered_conclusion_digest_sequence_sha256": object_sha([row[4] for row in conclusion_rows]),
        "distinct_input_commitment_count": len({row[3] for row in conclusion_rows}),
    }
    strict_need(table_commitments["R233_INPUT_BOUND_CONCLUSION"]["distinct_input_commitment_count"], 3_148, "distinct input commitments")

    pin_rows = [[label, relative, size, sha] for label, relative, size, sha in PINS]
    selected_row_appearances = sum(table_commitments[label]["row_count"] for label in table_sources)
    strict_need(selected_row_appearances, 38_872, "selected row appearances")
    ledger_payload = {
        "authority_scope": "R233_FROZEN_LOCAL_PARAMETRIC_GRAPH_KEY_ROW_AUTHORITY_ONLY",
        "manifest_first_input_pins": pin_rows,
        "manifest_first_input_commitment_sha256": object_sha(pin_rows),
        "old_manifest_audit": old_manifest,
        "old_package_defects": [
            "REPORT_AND_COLD_REPLAY_MISNESTED_AND_EXCLUDED_FROM_OLD_MANIFEST",
            "NO_PER_ROW_SHA256_FOR_3148_SELECTED_OUTPUT_ROWS",
            "NO_COMPLETE_CANONICAL_INPUT_COMMITMENT_PER_OUTPUT_ROW",
            "OLD_PATH_READS_NOT_HELD_FD_TWO_PASS_FINAL_REVALIDATED",
            "OLD_JSON_ACCEPTS_NONINTEGRAL_NUMBERS_AND_ORDINARY_EQUALITY_HAS_BOOL_INT_ALIAS",
            "NO_POST_DECODE_8MIB_FINAL_CANONICAL_ROW_CAP",
            "OLD_COLD_REPLAY_IS_UNSEALED_NARRATIVE_ONLY",
        ],
        "engine_chain_commitment_sha256": engine_chain_sha,
        "global_channel_universe_commitment_sha256": global_universe_commitment_sha,
        "old_certificate_result_sha256": old_candidate["result_sha256"],
        "selected_table_count": len(table_sources),
        "selected_row_appearance_count": selected_row_appearances,
        "per_row_sha256_closed_count": selected_row_appearances,
        "per_row_sha256_missing_count": 0,
        "table_commitments": table_commitments,
        "row_commitments": row_commitments,
        "narrow_positive_authority": {
            "input_bound_parametric_graph_key_partition_row_count": 3_148,
            "strict_interval_derivative_row_count": 3_148,
            "strict_two_open_side_cell_partition_row_count": 3_148,
            "shared_local_official_exact_key_row_count": 3_148,
            "frozen_channel_local_disposition_census": 5_368,
            "semantic_boundary": "FROZEN_ENGINE_REPLAY_NOT_NEW_ENGINE_THEOREM",
        },
        "remaining_blockers": {
            "input_bound_full_support_theorem": 3_148,
            "physical_incidence_or_equivalence_theorem": 3_148,
            "representation_pullback_theorem": 3_148,
            "known_block_attachment": 5_368,
        },
        "formal_credit": {
            "full_support": 0, "physical_incidence": 0, "physical_equivalence": 0,
            "representation_pullback": 0, "normalized_support": 0,
            "B1A": 0, "B2": 0, "maximality": 0, "CM2": 0,
        },
    }
    return ledger_payload, {
        "old_manifest": old_manifest,
        "census": expected_census,
        "table_commitments": table_commitments,
        "old_certificate_result_sha256": old_candidate["result_sha256"],
        "selected_row_appearances": selected_row_appearances,
        "global_universe_commitment_sha256": global_universe_commitment_sha,
    }


def run_attacks() -> dict[str, Any]:
    checks: dict[str, bool] = {
        "false_not_equal_zero": not type_strict_equal(False, 0),
        "true_not_equal_one": not type_strict_equal(True, 1),
        "different_inputs_produce_different_commitments": object_sha({"output": "same", "input": {"owner": 1}}) != object_sha({"output": "same", "input": {"owner": 2}}),
        "old_manifest_excludes_misplaced_report": "deliverables/" not in "\n".join(row[0] for row in OLD_MANIFEST_MEMBERS),
    }
    for label, raw in {
        "duplicate_key_rejected": b'{"a":0,"a":0}',
        "float_rejected": b'{"a":1.0}',
        "nan_rejected": b'{"a":NaN}',
        "infinity_rejected": b'{"a":Infinity}',
    }.items():
        try: strict_decode(raw, label, 100)
        except (Blocked, ValueError): checks[label] = True
        else: checks[label] = False
    oversized_raw = ('{"x":"' + ('\u754c' * 1_450_000) + '"}').encode("utf-8")
    oversized = strict_decode(oversized_raw, "coherent oversized row", 5_000_000)
    try: row_wire(oversized, "coherent oversized row")
    except Blocked: checks["post_decode_final_canonical_8MiB_cap"] = True
    else: checks["post_decode_final_canonical_8MiB_cap"] = False
    original_tmpdir = os.environ.get("TMPDIR")
    try:
        os.environ["TMPDIR"] = str(HERE)
        with tempfile.TemporaryDirectory(prefix="cm2-r233-attack-", dir="/tmp") as directory:
            root = Path(directory).resolve()
            checks["explicit_external_temp_ignores_TMPDIR"] = not root.is_relative_to(HERE.resolve())
            regular = root / "regular"; regular.write_bytes(b"x")
            symlink = root / "symlink"; symlink.symlink_to(regular)
            hardlink = root / "hardlink"; os.link(regular, hardlink)
            checks["symlink_rejected_model"] = symlink.is_symlink()
            checks["hardlink_rejected_model"] = regular.stat().st_nlink == 2
            fd = os.open(regular, os.O_RDONLY)
            before = os.fstat(fd)
            replacement = root / "replacement"; replacement.write_bytes(b"y"); os.replace(replacement, regular)
            checks["TOCTOU_path_replacement_detected"] = file_identity(before) != file_identity(os.stat(regular, follow_symlinks=False))
            os.close(fd)
    finally:
        if original_tmpdir is None: os.environ.pop("TMPDIR", None)
        else: os.environ["TMPDIR"] = original_tmpdir
    checks["old_R233_producer_not_imported_or_executed"] = "cm2_round233_source_g_outgoing_seam_parametric_graph_key_partition" not in sys.modules
    strict_need(all(checks.values()), True, "attack suite")
    result = {"status": "PASS", "check_count": len(checks), "checks": checks}
    return {"schema": ATTACK_SCHEMA, "result": result, "result_sha256": object_sha(result)}


def atomic_write(name: str, data: bytes) -> None:
    need(name == os.path.basename(name), "output basename")
    before = os.stat(HERE, follow_symlinks=False)
    need(stat.S_ISDIR(before.st_mode) and not HERE.is_symlink(), "output directory")
    fd, temporary_name = tempfile.mkstemp(prefix="." + name + ".", suffix=".tmp", dir=HERE)
    temporary = Path(temporary_name)
    try:
        with os.fdopen(fd, "wb") as handle:
            handle.write(data); handle.flush(); os.fsync(handle.fileno())
        existing = HERE / name
        if existing.exists() or existing.is_symlink():
            info = existing.lstat()
            need(stat.S_ISREG(info.st_mode) and not existing.is_symlink() and info.st_nlink == 1, "existing output:" + name)
        os.replace(temporary, existing)
    finally:
        if temporary.exists(): temporary.unlink()


def self_sha256() -> str:
    path = Path(__file__)
    before = path.lstat()
    need(stat.S_ISREG(before.st_mode) and not path.is_symlink() and before.st_nlink == 1, "verifier self regular")
    fd = os.open(path, os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0))
    try:
        held = os.fstat(fd)
        need(file_identity(before) == file_identity(held), "verifier self open race")
        first = Snapshot.hash_fd(fd); second = Snapshot.hash_fd(fd)
        need(first == second, "verifier self two-pass")
        need(file_identity(held) == file_identity(path.lstat()), "verifier self final path")
        return first
    finally:
        os.close(fd)


def verify(publish: bool) -> dict[str, Any]:
    need(FLINT_VERSION == "0.9.0", "python-flint version")
    with Snapshot() as snapshot:
        ledger_payload, replay = rebuild(snapshot)
        snapshot.final_revalidate()
    ledger = {"schema": LEDGER_SCHEMA, "ledger": ledger_payload, "ledger_sha256": object_sha(ledger_payload)}
    attack = run_attacks()
    ledger_wire = canonical(ledger) + b"\n"
    attack_wire = canonical(attack) + b"\n"
    result = {
        "status": STATUS,
        "verifier_sha256": self_sha256(),
        "old_manifest_sha256": PINS[0][3],
        "old_certificate_sha256": PINS[2][3],
        "old_certificate_result_sha256": replay["old_certificate_result_sha256"],
        "old_manifest_audit": replay["old_manifest"],
        "input_pin_count": len(PINS),
        "input_pinned_bytes": sum(row[2] for row in PINS),
        "two_pass_held_fd_pin_count": len(PINS),
        "final_path_revalidation_count": len(PINS),
        "selected_table_count": 8,
        "selected_row_appearance_count": replay["selected_row_appearances"],
        "per_row_sha256_closed_count": replay["selected_row_appearances"],
        "per_row_sha256_missing_count": 0,
        "input_bound_conclusion_count": 3_148,
        "global_channel_universe_commitment_sha256": replay["global_universe_commitment_sha256"],
        "counts": replay["census"],
        "table_commitments": replay["table_commitments"],
        "ledger_payload_sha256": ledger["ledger_sha256"],
        "ledger_file_sha256": hashlib.sha256(ledger_wire).hexdigest(),
        "attack_result_sha256": attack["result_sha256"],
        "independence_boundary": {
            "R233_producer_imported_or_executed": False,
            "R233_verifier_imported_or_executed": False,
            "R233_rows_independently_reconstructed": True,
            "frozen_upstream_engines_loaded_from_held_FDs": True,
            "upstream_engine_mathematical_semantics_independently_reproved": False,
            "R232_local_promotion_semantics_independently_reproved": False,
        },
        "main_replay_spill_file_count": 0,
        "TMPDIR_consulted_by_main_replay": False,
        "narrow_positive_authority": ledger_payload["narrow_positive_authority"],
        "remaining_blockers": ledger_payload["remaining_blockers"],
        "formal_credit": ledger_payload["formal_credit"],
        "authority_verdict": "GO_R233_LOCAL_ROW_AUTHORITY_ONLY",
        "CM2": "NO-GO_FOR_CLAIM",
    }
    verification = {"schema": VERIFICATION_SCHEMA, "result": result, "result_sha256": object_sha(result)}
    verification_wire = canonical(verification) + b"\n"
    if publish:
        atomic_write(LEDGER_NAME, ledger_wire)
        atomic_write(ATTACK_NAME, attack_wire)
        atomic_write(VERIFICATION_NAME, verification_wire)
    else:
        for name, expected in ((LEDGER_NAME, ledger_wire), (ATTACK_NAME, attack_wire), (VERIFICATION_NAME, verification_wire)):
            path = HERE / name
            info = path.lstat()
            need(stat.S_ISREG(info.st_mode) and not path.is_symlink() and info.st_nlink == 1, "published artifact:" + name)
            need(path.read_bytes() == expected, "published exact no-write replay:" + name)
    return verification


def main() -> int:
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--verify-publish", action="store_true")
    mode.add_argument("--verify-no-write", action="store_true")
    args = parser.parse_args()
    document = verify(args.verify_publish)
    print(document["result"]["status"])
    print("result_sha256=" + document["result_sha256"])
    print("selected_row_appearances=" + str(document["result"]["selected_row_appearance_count"]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
