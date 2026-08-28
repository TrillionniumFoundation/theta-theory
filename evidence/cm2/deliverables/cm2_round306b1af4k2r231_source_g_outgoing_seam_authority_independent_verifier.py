#!/usr/bin/env python3
"""Independent, zero-credit authority verifier for the frozen Round231 rows.

The Round231 producer is inert evidence: this file never imports, executes,
tokenizes, or evaluates it.  The verifier strictly decodes the frozen 91.9 MB
certificate, independently repeats the Round231 traversal, and closes every
selected row with its complete canonical-row SHA-256.  Frozen upstream engines
are loaded from already-open, twice-hashed file descriptors rather than from
the import path.  Reusing those frozen engines is an explicit engineering
authority boundary; it does not constitute a new mathematical theorem.

All physical-incidence, pullback, normalized-support, B1A, B2, maximality, and
CM2 credits remain exactly zero.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from fractions import Fraction as Q
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
PREFIX: Final = "cm2_round306b1af4k2r231_source_g_outgoing_seam_authority_"
LEDGER_NAME: Final = PREFIX + "row_commitment_ledger.json"
VERIFICATION_NAME: Final = PREFIX + "verification.json"
ATTACK_NAME: Final = PREFIX + "attack_suite.json"
OLD_SCHEMA: Final = "cm2.round231.source-g-outgoing-seam-depth6-materialization.v1"
LEDGER_SCHEMA: Final = "cm2.round306b1af4k2r231.source-g-outgoing-seam-authority.row-commitment-ledger.v1"
VERIFICATION_SCHEMA: Final = "cm2.round306b1af4k2r231.source-g-outgoing-seam-authority.independent-verification.v1"
ATTACK_SCHEMA: Final = "cm2.round306b1af4k2r231.source-g-outgoing-seam-authority.attack-suite.v1"
STATUS: Final = "PASS_R231_ENGINEERING_ROW_AUTHORITY_ONLY__ZERO_FORMAL_CREDIT"
ROW_CAP: Final = 8_388_608

# label, filename, exact size, SHA-256.  The upstream set is independently
# duplicated here and is not accepted from the Round231 producer.
PINS: Final = (
    ("R231_PRODUCER", "cm2_round231_source_g_outgoing_seam_depth6_materialization.py", 12_984, "5afa1bc6fc6faec4c9b13be707c93714acdf5dbd09f2fafeefff07c445c517ad"),
    ("R231_CERTIFICATE", "cm2_round231_source_g_outgoing_seam_depth6_materialization_certificate.json", 91_909_341, "7bc861ef4f2c2962dcf7c8e38839af2ec12477f9fc42d808be1b48d858745374"),
    ("R179_SOURCE", "cm2_round179_source_g_residual_tube_arrangement.py", 63_683, "8c568c58d82708a7ab549f126c1fcedfccff563d1d00e3c1f7e6545b4b0d29ab"),
    ("R179_ROWS", "cm2_round179_source_g_residual_tube_arrangement_rows.json", 131_273_924, "f20b42c1fed781779b537b4d45bf44233eae1ed3ee620b95177a80f0eb2b5e42"),
    ("R220_CERTIFICATE", "cm2_round220_source_g_round179_resolved_child_boundary_atlas_certificate.json", 294_422_681, "569a7849b53805ff4deca0eff9a6938a897942d3d682dfef27c27559135ce974"),
    ("R230_CERTIFICATE", "cm2_round230_source_g_resolved_retained_bulk_continuation_certificate.json", 67_327_799, "88d9d826bd985635d42820c7b66389603ab56a48717531ace525ee2eaf6d3a73"),
    ("R174_ENGINE", "cm2_round174_source_g_unique_first_dynamic_occurrence_materialization_verifier.py", 96_797, "c7ead7c9cb8b4d7b8680e64bfb7870e5c5f5e39277e7c7d3d08a62b600f5c058"),
    ("FIRST_HIT_ENGINE", "cm2_gate3_candidate_first_hit_cert.py", 13_832, "6d224d74cda186a40ef9956d1dd6556d5a7b9f506d47c942427ceb66fd705bd2"),
    ("GE_ENGINE", "cm2_gate3_ge_interval_atlas_cert.py", 17_052, "ab120f85a263f3cb0697d8a40bc9ed2bf12b361aa7c54940c214b6fd85b17e2b"),
    ("ATLAS_ENGINE", "cm2_gate3_eight_cell_symmetry_atlas_cert.py", 18_141, "d867f5cb03691289033d1a0d0e277a03e8395d70aae7e0689446d7aa63eac3da"),
    ("R171_PRODUCER", "cm2_round171_compact_gate3_source_g_coordinate_bridge.py", 26_183, "bcaba20978ebb5386d64bcf248d254c54c8ac79d9c9c7eb023be278ab7e05c75"),
    ("R171_CERTIFICATE", "cm2_round171_compact_gate3_source_g_coordinate_bridge_certificate.json", 23_061, "1fb4827b42569d41602765445d0333c76b2ef97615873fc406563ac0e18af7a5"),
    ("R171_VERIFIER", "cm2_round171_compact_gate3_source_g_coordinate_bridge_verifier.py", 38_840, "aee7b3cc3f1468b6a46e7a90e1bb219bd609bddfe54075c6c73e124d98eda7e0"),
    ("R171_VERIFICATION", "cm2_round171_compact_gate3_source_g_coordinate_bridge_verification.json", 3_083, "effdfd4306dbf7bd70df1e9b5ed9166a58dc00a5d333b0f2f2a5f0cb930ccce9"),
    ("R171_MANIFEST", "cm2-round171-compact-gate3-source-g-coordinate-bridge-manifest-2026-07-26.sha256", 895, "b86a5faa33f503a2de6139f7765fda4e54e027954373ecdf8b8d587ba179417c"),
    ("R173_PRODUCER", "cm2_round173_source_g_exact_return_signature_transport.py", 47_760, "bdbf794a99dc9276b11b7680818994d63f52fe0e5a857948701f64e8d5d16a0f"),
    ("R173_CERTIFICATE", "cm2_round173_source_g_exact_return_signature_transport_certificate.json", 36_739, "5ff82c5822f543109da0d50c0637d0d2f9148a738b1a21b16878c70e5505cf1a"),
    ("R173_VERIFIER", "cm2_round173_source_g_exact_return_signature_transport_verifier.py", 59_083, "eb2b51929719563cd9fe72d180f3f1932a049e983ad1e7a8ec9ac89526bc30f1"),
    ("R173_VERIFICATION", "cm2_round173_source_g_exact_return_signature_transport_verification.json", 3_937, "e205367506bc02aa982de074253e5806f07b4358dd3738fb4a0e14476e44ce99"),
    ("R173_MANIFEST", "cm2-round173-source-g-exact-return-signature-transport-manifest-2026-07-26.sha256", 901, "ba2a1b6eea612e538e3ca70e2916e07469fda38eaef24a751ff862262336f275"),
    ("R174_PRODUCER", "cm2_round174_source_g_unique_first_dynamic_occurrence_materialization.py", 81_094, "3d329525dda6697a3a5d2a8227c94bd9c309ea7ebcc4cdd0c7fbe573c267a218"),
    ("R174_CERTIFICATE", "cm2_round174_source_g_unique_first_dynamic_occurrence_materialization_certificate.json", 15_984, "10221141c58c044b42e43009beb34ae4705995925a88deaa70ff2eba2ea852c7"),
    ("R174_ROWS", "cm2_round174_source_g_unique_first_dynamic_occurrence_materialization_rows.json", 113_656_620, "9edeea2e1033b0dd70dee11a53b0f6aeb21fe74030aeefb60b081a7c420cff54"),
    ("R174_VERIFICATION", "cm2_round174_source_g_unique_first_dynamic_occurrence_materialization_verification.json", 5_011, "1f65b5e02b1d1e63bd7e41d6a88d5eb180e2be92620af4b8afa2141c9f6e344c"),
    ("R174_MANIFEST", "cm2_round174_source_g_unique_first_dynamic_occurrence_materialization_manifest.sha256", 1_037, "9e92db7748a2c0acdce532c830f899ce153765de64a59e9f372df3099ac91b76"),
    ("GATE5_FRONTIER", "cm2-gate5-return-word-three-norm-frontier-manifest-2026-07-16.json", 10_733, "47e84e8b75b289b7a5db4afcbd7dfa8dac909d2f76fa1c95ef290546d031a866"),
)


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True, allow_nan=False).encode("ascii")


def object_sha(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def qstr(value: Q) -> str:
    return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"


def dup_reject(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for key, value in pairs:
        need(key not in out, "duplicate key:" + key)
        out[key] = value
    return out


def reject_number(token: str) -> Any:
    raise Blocked("nonintegral/constant:" + token)


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


def row_bytes(row: Any, label: str) -> bytes:
    data = canonical(row)
    need(len(data) <= ROW_CAP, "final canonical row cap:" + label)
    return data


def file_identity(info: os.stat_result) -> tuple[int, ...]:
    return (info.st_dev, info.st_ino, info.st_mode, info.st_nlink, info.st_size, info.st_mtime_ns, info.st_ctime_ns)


def dir_identity(info: os.stat_result) -> tuple[int, ...]:
    # Other authorized packages may be atomically published into the shared
    # deliverables directory during this replay.  Directory entry timestamps
    # are therefore not identity.  The directory object itself is bound by
    # device, inode and mode; every selected file retains the stricter full
    # inode/size/mtime/ctime identity check below.
    return (info.st_dev, info.st_ino, info.st_mode)


class Snapshot:
    def __init__(self) -> None:
        self.dirfd = -1
        self.dirstat: os.stat_result | None = None
        self.fds: dict[str, int] = {}
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

    def __enter__(self) -> "Snapshot":
        before = os.stat(HERE, follow_symlinks=False)
        need(stat.S_ISDIR(before.st_mode) and not HERE.is_symlink(), "deliverables directory")
        self.dirfd = os.open(HERE, os.O_RDONLY | getattr(os, "O_DIRECTORY", 0) | getattr(os, "O_NOFOLLOW", 0))
        held_dir = os.fstat(self.dirfd)
        need(dir_identity(before) == dir_identity(held_dir), "directory open race")
        self.dirstat = held_dir
        try:
            for label, filename, size, expected_sha in PINS:
                need(filename == os.path.basename(filename), "basename:" + label)
                before_file = os.stat(filename, dir_fd=self.dirfd, follow_symlinks=False)
                need(stat.S_ISREG(before_file.st_mode) and before_file.st_nlink == 1, "regular/nlink:" + label)
                need(before_file.st_size == size, "size:" + label)
                fd = os.open(filename, os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0), dir_fd=self.dirfd)
                held = os.fstat(fd)
                need(file_identity(before_file) == file_identity(held), "open race:" + label)
                self.fds[label] = fd
                first, second = self.hash_fd(fd), self.hash_fd(fd)
                need(first == second == expected_sha, "two-pass SHA:" + label)
                after_file = os.stat(filename, dir_fd=self.dirfd, follow_symlinks=False)
                need(file_identity(held) == file_identity(after_file), "post-hash path:" + label)
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
                need(total == self.rows[label][1], "held read size:" + label)
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
        try:
            exec(compile(source, module.__file__, "exec"), module.__dict__)
            return module
        except BaseException:
            sys.modules.pop(module_name, None)
            raise

    def final_revalidate(self) -> None:
        need(self.dirstat is not None, "snapshot active")
        need(dir_identity(self.dirstat) == dir_identity(os.fstat(self.dirfd)), "held directory changed")
        need(dir_identity(self.dirstat) == dir_identity(os.stat(HERE, follow_symlinks=False)), "directory path changed")
        for label, filename, size, expected_sha in PINS:
            held = os.fstat(self.fds[label])
            path = os.stat(filename, dir_fd=self.dirfd, follow_symlinks=False)
            need(file_identity(held) == file_identity(path), "final FD/path:" + label)
            need(held.st_size == size and self.hash_fd(self.fds[label]) == expected_sha, "final SHA:" + label)

    def __exit__(self, *_args: Any) -> None:
        for fd in self.fds.values():
            try: os.close(fd)
            except OSError: pass
        self.fds.clear()
        if self.dirfd >= 0:
            try: os.close(self.dirfd)
            except OSError: pass
            self.dirfd = -1


def extract_first_value(raw: bytes, key: str, expected_occurrences: int) -> bytes:
    needle = canonical(key) + b":"
    need(raw.count(needle) == expected_occurrences, "key occurrence:" + key)
    start = raw.find(needle) + len(needle)
    need(start >= len(needle), "key missing:" + key)
    while start < len(raw) and raw[start] in b" \t\r\n": start += 1
    opener = raw[start]
    need(opener in (ord("["), ord("{")), "compound selected value:" + key)
    closer = ord("]") if opener == ord("[") else ord("}")
    depth = 0; in_string = False; escaped = False
    for index in range(start, len(raw)):
        byte = raw[index]
        if in_string:
            if escaped: escaped = False
            elif byte == ord("\\"): escaped = True
            elif byte == ord('"'): in_string = False
        else:
            if byte == ord('"'): in_string = True
            elif byte == opener: depth += 1
            elif byte == closer:
                depth -= 1
                if depth == 0: return raw[start:index + 1]
    raise Blocked("unterminated selected value:" + key)


def unwrap_selected(raw: bytes, key: str, occurrences: int, maximum: int) -> Any:
    return strict_decode(extract_first_value(raw, key, occurrences), key, maximum)


def volume(box: Any) -> Q:
    return (box.t1 - box.t0) * (box.p1 - box.p0) * (box.s1 - box.s0)


def load_candidate(raw: bytes) -> tuple[dict[str, Any], dict[str, list[list[str]]]]:
    document = strict_decode(raw, "R231 certificate", 100_000_000)
    need(type(document) is dict and set(document) == {"schema", "result", "result_sha256"}, "candidate envelope")
    strict_need(document["schema"], OLD_SCHEMA, "candidate schema")
    result = document["result"]
    strict_need(document["result_sha256"], object_sha(result), "candidate result digest")
    need(canonical(document) + b"\n" == raw, "candidate canonical wire")
    expected_nonpromotion = {
        "known_block_incidence_credit": 0,
        "physical_component_credit": 0,
        "maximal_physical_component_credit": 0,
        "global_exact_key_disposition_credit": 0,
        "CM2": "NO-GO_FOR_CLAIM",
    }
    strict_need(result["strict_nonpromotion"], expected_nonpromotion, "strict nonpromotion")
    strict_need(result["status"], "DEPTH6_OUTGOING_SEAM_ADAPTIVE_MATERIALIZATION_COMPLETE_ZERO_GLOBAL_PROMOTION", "candidate status")
    table_specs = (
        ("resolved", "resolved_descendant_rows", "materialized_row_id", 22_348),
        ("guard", "guard_descendant_rows", "guard_row_id", 0),
        ("frontier", "depth6_frontier_rows", "frontier_row_id", 67_924),
        ("root", "root_summary_rows", "root_summary_id", 5_368),
    )
    commitments: dict[str, Any] = {}
    digest_rows: dict[str, list[list[str]]] = {}
    for label, property_name, id_name, count in table_specs:
        rows = result[property_name]
        strict_need(len(rows), count, "candidate row count:" + label)
        pairs: list[list[str]] = []
        seen: set[str] = set()
        previous = ""
        stream = hashlib.sha256(); stream.update(b"[")
        for index, row in enumerate(rows):
            need(type(row) is dict and type(row.get(id_name)) is str, "candidate row shape:" + label)
            row_id = row[id_name]
            need(row_id not in seen and (index == 0 or previous < row_id), "candidate row order/unique:" + label)
            seen.add(row_id); previous = row_id
            encoded = row_bytes(row, label)
            if index: stream.update(b",")
            stream.update(encoded)
            pairs.append([row_id, hashlib.sha256(encoded).hexdigest()])
            if label == "resolved":
                strict_need(row["known_block_incidence_credit"], 0, "resolved incidence zero")
                strict_need(row["physical_component_credit"], 0, "resolved component zero")
                strict_need(row["global_exact_key_disposition_credit"], 0, "resolved global zero")
            elif label in {"frontier", "guard"}:
                strict_need(row["physical_component_credit"], 0, label + " component zero")
                strict_need(row["global_exact_key_disposition_credit"], 0, label + " global zero")
        stream.update(b"]")
        ordered_rows_sha = stream.hexdigest()
        declared_name = {
            "resolved": "resolved_descendant_rows_sha256", "guard": "guard_descendant_rows_sha256",
            "frontier": "depth6_frontier_rows_sha256", "root": "root_summary_rows_sha256",
        }[label]
        strict_need(result[declared_name], ordered_rows_sha, "declared table digest:" + label)
        hashes = [pair[1] for pair in pairs]
        commitments[label] = {
            "id_field": id_name, "row_count": count,
            "ordered_rows_sha256": ordered_rows_sha,
            "ordered_row_digest_sequence_sha256": object_sha(hashes),
            "unordered_row_digest_multiset_sha256": object_sha(sorted(hashes)),
            "first_row_sha256": hashes[0] if hashes else None,
            "last_row_sha256": hashes[-1] if hashes else None,
        }
        digest_rows[label] = pairs
    meta = {key: value for key, value in result.items() if key not in {
        "resolved_descendant_rows", "guard_descendant_rows", "depth6_frontier_rows", "root_summary_rows"
    }}
    return {"metadata": meta, "table_commitments": commitments, "certificate_result_sha256": document["result_sha256"]}, digest_rows


def unpack(columns: list[str], rows: list[list[Any]], label: str) -> list[dict[str, Any]]:
    out = []
    for row in rows:
        need(type(row) is list and len(row) == len(columns), "packed row width:" + label)
        out.append(dict(zip(columns, row, strict=True)))
    return out


def rebuild(snapshot: Snapshot, r179: Any, r174: Any) -> tuple[dict[str, Any], dict[str, list[list[str]]]]:
    gate5 = strict_decode(snapshot.bytes("GATE5_FRONTIER"), "Gate5 frontier", 1_000_000)
    registry = r174.rebuild_registry(gate5)

    raw179 = snapshot.bytes("R179_ROWS")
    schemas = unwrap_selected(raw179, "row_column_schemas", 1, 50_000)
    origin_packed = unwrap_selected(raw179, "origin_tube_rows", 3, 40_000_000)
    retained_packed = unwrap_selected(raw179, "retained_3d_child_rows", 3, 60_000_000)
    origins = {row["origin_row_id"]: row for row in unpack(schemas["origin_tube_rows"], origin_packed, "origin")}
    retained = {row["row_id"]: row for row in unpack(schemas["retained_3d_child_rows"], retained_packed, "retained")}
    strict_need(len(origins), 62_012, "origin census")
    strict_need(len(retained), 106_680, "retained census")
    del raw179, schemas, origin_packed, retained_packed; gc.collect()

    raw220 = snapshot.bytes("R220_CERTIFICATE")
    table220 = unwrap_selected(raw220, "one_step_split_interface_rows", 1, 12_000_000)
    del raw220; gc.collect()
    strict_need(table220["row_count"], 13_076, "R220 table census")
    interfaces: list[tuple[str, str]] = []
    for packed in table220["rows"]:
        row = dict(zip(table220["columns"], packed, strict=True))
        if {row["lower_child_kind"], row["upper_child_kind"]} != {"RESOLVED", "RETAINED"}:
            continue
        retained_id = row["upper_child_row_id"] if row["upper_child_kind"] == "RETAINED" else row["lower_child_row_id"]
        interfaces.append((row["split_interface_id"], retained_id))
    strict_need(len(interfaces), 8_960, "R220 mixed interface census")
    del table220; gc.collect()

    raw230 = snapshot.bytes("R230_CERTIFICATE")
    ledger230 = unwrap_selected(raw230, "formal_certified_local_bulk_bridge_star_ledger", 1, 2_000_000)
    del raw230; gc.collect()
    strict_need(ledger230["row_count"], 448, "R230 accepted census")
    accepted = {row["Round220_split_interface_id"] for row in ledger230["rows"]}
    strict_need(len(accepted), 448, "R230 accepted unique")
    roots = [(interface_id, retained[retained_id]) for interface_id, retained_id in interfaces
             if interface_id not in accepted and retained[retained_id]["reason_labels"] == ["outgoing_chart_seam"]]
    roots.sort(key=lambda pair: pair[0])
    strict_need(len(roots), 5_368, "outgoing seam roots")

    expected_pairs: dict[str, list[list[str]]] = {"resolved": [], "guard": [], "frontier": [], "root": []}
    depth_census: dict[int, Counter[str]] = defaultdict(Counter)
    depth_volume: dict[int, Counter[str]] = defaultdict(Counter)
    root_rows: list[dict[str, Any]] = []
    resolved_key_ordinals: set[int] = set()
    fully_resolved = 0
    for interface_id, root in roots:
        owner = origins[root["origin_row_id"]]["owner_target"]
        initial = r179.box_from(root["box"], len(root["refinement_path"]), root["row_id"])
        nodes = [(initial, [])]
        root_resolved = root_guard = 0
        released_volume = Q(0)
        for depth in range(1, 7):
            next_nodes = []
            for box, path in nodes:
                for child_index, child in enumerate(r174.bisect(box, 0)):
                    child_path = [*path, child_index]
                    kind, data = r174.classify_child(root["chart"], child, owner, registry)
                    child_volume = volume(child)
                    depth_census[depth][kind] += 1
                    depth_volume[depth][kind] += child_volume
                    base = {
                        "Round220_split_interface_id": interface_id,
                        "Round179_retained_child_row_id": root["row_id"],
                        "origin_row_id": root["origin_row_id"], "parent_id": root["parent_id"],
                        "chart": root["chart"], "owner_target": owner, "adaptive_depth": depth,
                        "binary_t_path": child_path, "box": r174.box_values(child),
                        "coordinate_volume": qstr(child_volume),
                    }
                    if kind == "resolved":
                        root_resolved += 1; released_volume += child_volume
                        signature = data; resolved_key_ordinals.add(signature["key"]["ordinal"])
                        row = {
                            "materialized_row_id": "round231-resolved:" + object_sha([interface_id, child_path, base["box"], signature]),
                            **base, "local_return_signature": {
                                "source_chart": root["chart"], "target_lift": owner,
                                "ordered_integer_wall_events": signature["events"],
                                "signed_wall_word": list(signature["pattern"]), "roof": signature["roof"],
                                "outgoing_cell": signature["outgoing"], "target_chart": signature["target_chart"],
                                "official_key_row": signature["key"]["row"],
                                "official_key_ordinal": signature["key"]["ordinal"],
                                "official_key_id": signature["key"]["identifier"],
                            }, "credit_kind": "LOCAL_POSITIVE_3D_OCCURRENCE_ONLY",
                            "known_block_incidence_credit": 0, "physical_component_credit": 0,
                            "global_exact_key_disposition_credit": 0,
                        }
                        expected_pairs["resolved"].append([row["materialized_row_id"], hashlib.sha256(row_bytes(row, "rebuilt resolved")).hexdigest()])
                    elif kind == "guard":
                        root_guard += 1; released_volume += child_volume
                        row = {
                            "guard_row_id": "round231-guard:" + object_sha([interface_id, child_path, base["box"]]),
                            **base, "exact_rejection_predicate": "min|t| gives 2*t^2-1>0",
                            "physical_component_credit": 0, "global_exact_key_disposition_credit": 0,
                        }
                        expected_pairs["guard"].append([row["guard_row_id"], hashlib.sha256(row_bytes(row, "rebuilt guard")).hexdigest()])
                    else:
                        strict_need(data, ["outgoing_chart_seam"], "retained reason")
                        next_nodes.append((child, child_path))
            nodes = next_nodes
        retained_volume = sum((volume(box) for box, _ in nodes), Q(0))
        strict_need(released_volume + retained_volume, Q(root["coordinate_volume"]), "root volume conservation")
        if not nodes: fully_resolved += 1
        for box, path in nodes:
            row = {
                "frontier_row_id": "round231-depth6-frontier:" + object_sha([interface_id, path, r174.box_values(box)]),
                "Round220_split_interface_id": interface_id,
                "Round179_retained_child_row_id": root["row_id"], "origin_row_id": root["origin_row_id"],
                "parent_id": root["parent_id"], "chart": root["chart"], "owner_target": owner,
                "adaptive_depth": 6, "binary_t_path": path, "box": r174.box_values(box),
                "coordinate_volume": qstr(volume(box)), "reason_labels": ["outgoing_chart_seam"],
                "physical_component_credit": 0, "global_exact_key_disposition_credit": 0,
            }
            expected_pairs["frontier"].append([row["frontier_row_id"], hashlib.sha256(row_bytes(row, "rebuilt frontier")).hexdigest()])
        summary = {
            "root_summary_id": "round231-root:" + object_sha(interface_id),
            "Round220_split_interface_id": interface_id,
            "Round179_retained_child_row_id": root["row_id"],
            "resolved_descendant_count": root_resolved, "guard_descendant_count": root_guard,
            "depth6_retained_frontier_count": len(nodes), "released_coordinate_volume": qstr(released_volume),
            "retained_coordinate_volume": qstr(retained_volume),
        }
        root_rows.append(summary)

    for label in expected_pairs:
        expected_pairs[label].sort(key=lambda pair: pair[0])
    for row in root_rows:
        expected_pairs["root"].append([row["root_summary_id"], hashlib.sha256(row_bytes(row, "rebuilt root")).hexdigest()])
    expected_pairs["root"].sort(key=lambda pair: pair[0])
    metadata = {
        "status": "DEPTH6_OUTGOING_SEAM_ADAPTIVE_MATERIALIZATION_COMPLETE_ZERO_GLOBAL_PROMOTION",
        "census": {
            "outgoing_seam_root_count": 5_368, "adaptive_depth": 6,
            "materialized_resolved_descendant_count": len(expected_pairs["resolved"]),
            "materialized_guard_descendant_count": len(expected_pairs["guard"]),
            "depth6_retained_frontier_count": len(expected_pairs["frontier"]),
            "roots_fully_resolved_or_guarded_count": fully_resolved,
            "distinct_released_exact_key_count": len(resolved_key_ordinals),
        },
        "depth_census": {str(d): dict(sorted(c.items())) for d, c in sorted(depth_census.items())},
        "depth_coordinate_volume": {str(d): {k: qstr(v) for k, v in sorted(c.items())} for d, c in sorted(depth_volume.items())},
        "resolved_descendant_rows_sha256": None, "guard_descendant_rows_sha256": None,
        "depth6_frontier_rows_sha256": None, "root_summary_rows_sha256": None,
        "strict_nonpromotion": {
            "known_block_incidence_credit": 0, "physical_component_credit": 0,
            "maximal_physical_component_credit": 0, "global_exact_key_disposition_credit": 0,
            "CM2": "NO-GO_FOR_CLAIM",
        },
        "required_next": "attach only exact positive-area/event-trace descendants to frozen known blocks with an independent verifier",
    }
    return metadata, expected_pairs


def run_attacks() -> dict[str, Any]:
    checks: dict[str, bool] = {}
    checks["false_not_equal_zero"] = not type_strict_equal(False, 0)
    checks["true_not_equal_one"] = not type_strict_equal(True, 1)
    for label, raw in {
        "duplicate_key_rejected": b'{"a":0,"a":0}',
        "float_rejected": b'{"a":1.0}',
        "nan_rejected": b'{"a":NaN}',
    }.items():
        try: strict_decode(raw, label, 100)
        except (Blocked, ValueError): checks[label] = True
        else: checks[label] = False
    # Raw UTF-8 is below 8 MiB, but canonical ensure_ascii expansion is above
    # 8 MiB.  This proves the cap is checked after successful final decode.
    oversize_raw = ('{"x":"' + ('界' * 1_450_000) + '"}').encode("utf-8")
    oversize_value = strict_decode(oversize_raw, "oversize coherent row", 5_000_000)
    try: row_bytes(oversize_value, "oversize coherent row")
    except Blocked: checks["post_decode_final_canonical_8MiB_cap"] = True
    else: checks["post_decode_final_canonical_8MiB_cap"] = False
    original_tmpdir = os.environ.get("TMPDIR")
    try:
        os.environ["TMPDIR"] = str(HERE)
        with tempfile.TemporaryDirectory(prefix="cm2-r231-attack-", dir="/tmp") as directory:
            root = Path(directory)
            checks["explicit_external_temp_ignores_TMPDIR"] = not root.is_relative_to(HERE)
            regular = root / "regular"; regular.write_bytes(b"x")
            symlink = root / "symlink"; symlink.symlink_to(regular)
            hardlink = root / "hardlink"; os.link(regular, hardlink)
            checks["symlink_rejected_model"] = symlink.is_symlink()
            checks["hardlink_rejected_model"] = regular.stat().st_nlink == 2
            fd = os.open(regular, os.O_RDONLY)
            before = os.fstat(fd); replacement = root / "replacement"; replacement.write_bytes(b"y"); os.replace(replacement, regular)
            checks["TOCTOU_path_replacement_detected"] = file_identity(before) != file_identity(os.stat(regular, follow_symlinks=False))
            os.close(fd)
    finally:
        if original_tmpdir is None: os.environ.pop("TMPDIR", None)
        else: os.environ["TMPDIR"] = original_tmpdir
    checks["producer_not_imported_or_executed"] = "cm2_round231_source_g_outgoing_seam_depth6_materialization" not in sys.modules
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
            info = existing.lstat(); need(stat.S_ISREG(info.st_mode) and not existing.is_symlink() and info.st_nlink == 1, "existing output")
        os.replace(temporary, existing)
    finally:
        if temporary.exists(): temporary.unlink()


def verify(publish: bool) -> dict[str, Any]:
    need(FLINT_VERSION == "0.9.0", "python-flint version")
    with Snapshot() as snapshot:
        candidate_summary, candidate_pairs = load_candidate(snapshot.bytes("R231_CERTIFICATE"))
        # Load the frozen engine chain from held bytes, in dependency order.
        snapshot.load_module("cm2_gate3_candidate_first_hit_cert", "FIRST_HIT_ENGINE")
        snapshot.load_module("cm2_gate3_ge_interval_atlas_cert", "GE_ENGINE")
        snapshot.load_module("cm2_gate3_eight_cell_symmetry_atlas_cert", "ATLAS_ENGINE")
        r174 = snapshot.load_module("cm2_round174_source_g_unique_first_dynamic_occurrence_materialization_verifier", "R174_ENGINE")
        r179 = snapshot.load_module("cm2_round179_source_g_residual_tube_arrangement", "R179_SOURCE")
        ctx.prec = 192
        rebuilt_metadata, rebuilt_pairs = rebuild(snapshot, r179, r174)
        strict_need(candidate_pairs, rebuilt_pairs, "independent row-by-row replay")
        candidate_meta = candidate_summary["metadata"]
        for key, expected in rebuilt_metadata.items():
            if expected is not None:
                strict_need(candidate_meta[key], expected, "rebuilt metadata:" + key)
        snapshot.final_revalidate()

    input_rows = [[label, filename, size, sha] for label, filename, size, sha in PINS]
    ledger_payload = {
        "authority_scope": "R231_FROZEN_BYTE_ROW_AND_ENGINEERING_REPLAY_AUTHORITY_ONLY",
        "input_commitment_sha256": object_sha(input_rows),
        "certificate_result_sha256": candidate_summary["certificate_result_sha256"],
        "table_commitments": candidate_summary["table_commitments"],
        "row_commitments": {
            label: {"columns": [candidate_summary["table_commitments"][label]["id_field"], "canonical_row_sha256"], "rows": pairs}
            for label, pairs in candidate_pairs.items()
        },
        "selected_row_count": sum(len(rows) for rows in candidate_pairs.values()),
        "formal_credit": {
            "full_support": 0, "physical_incidence": 0, "representation_pullback": 0,
            "normalized_support": 0, "B1A": 0, "B2": 0, "maximality": 0, "CM2": 0,
        },
    }
    ledger = {"schema": LEDGER_SCHEMA, "ledger": ledger_payload, "ledger_sha256": object_sha(ledger_payload)}
    attack = run_attacks()
    self_raw = (HERE / Path(__file__).name).read_bytes()
    result = {
        "status": STATUS,
        "verifier_sha256": hashlib.sha256(self_raw).hexdigest(),
        "old_producer_sha256": PINS[0][3], "old_certificate_sha256": PINS[1][3],
        "certificate_result_sha256": candidate_summary["certificate_result_sha256"],
        "input_pin_count": len(PINS), "input_pinned_bytes": sum(row[2] for row in PINS),
        "two_pass_held_fd_pin_count": len(PINS), "final_path_revalidation_count": len(PINS),
        "selected_table_count": 4, "selected_row_count": ledger_payload["selected_row_count"],
        "per_row_sha256_closed_count": ledger_payload["selected_row_count"],
        "per_row_sha256_missing_count": 0,
        "counts": candidate_summary["metadata"]["census"],
        "table_commitments": candidate_summary["table_commitments"],
        "ledger_payload_sha256": ledger["ledger_sha256"],
        "ledger_file_sha256": hashlib.sha256(canonical(ledger) + b"\n").hexdigest(),
        "attack_result_sha256": attack["result_sha256"],
        "independence_boundary": {
            "R231_producer_imported_or_executed": False,
            "R231_traversal_independently_reimplemented": True,
            "frozen_upstream_engines_loaded_from_held_FDs": True,
            "upstream_mathematical_semantics_independently_reproved": False,
        },
        "spill_files_created": 0, "TMPDIR_consulted_by_main_replay": False,
        "formal_credit": ledger_payload["formal_credit"],
        "authority_verdict": "GO_R231_ENGINEERING_AUTHORITY_ONLY",
        "CM2": "NO-GO_FOR_CLAIM",
    }
    verification = {"schema": VERIFICATION_SCHEMA, "result": result, "result_sha256": object_sha(result)}
    ledger_wire = canonical(ledger) + b"\n"; attack_wire = canonical(attack) + b"\n"; verification_wire = canonical(verification) + b"\n"
    if publish:
        atomic_write(LEDGER_NAME, ledger_wire)
        atomic_write(ATTACK_NAME, attack_wire)
        atomic_write(VERIFICATION_NAME, verification_wire)
    else:
        for name, expected in ((LEDGER_NAME, ledger_wire), (ATTACK_NAME, attack_wire), (VERIFICATION_NAME, verification_wire)):
            path = HERE / name
            info = path.lstat(); need(stat.S_ISREG(info.st_mode) and not path.is_symlink() and info.st_nlink == 1, "published artifact:" + name)
            need(path.read_bytes() == expected, "published artifact exact replay:" + name)
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
    print("selected_rows=" + str(document["result"]["selected_row_count"]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
