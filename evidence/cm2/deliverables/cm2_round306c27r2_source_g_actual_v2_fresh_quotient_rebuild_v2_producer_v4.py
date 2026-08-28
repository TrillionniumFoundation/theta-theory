#!/usr/bin/env python3
"""Build the fresh C27R2 quotient from terminal-pinned actual-v2 seed 1.

This is a mathematical candidate producer, not a release tool.  A successful
run writes three deterministic, canonical gzip ledgers and a zero-credit
result.  It never mints C27R2, never reads an old C27/C28/C29 partition, and
never assigns a post-quotient identifier from a DSU implementation root.

The actual-v2 terminal receipt pins a base seal.  The base seal in turn pins
both real-seed edge ledgers and the frozen C15 member/component ledger through
its payload manifest and single-open-file-description attestations.  This
producer consumes only the seed-1 edge ledger from that chain.  An independent
verifier is required to rebuild the same quotient from seed 2.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import gzip
import hashlib
import json
import os
from pathlib import Path
import stat
import sys
import tempfile
from typing import Any, Iterator


ROOT = Path(__file__).resolve().parent.parent
SELF = Path(__file__).resolve()
C15_RELATIVE = (
    "deliverables/"
    "cm2_round306c15_source_g_502204_member_fresh_dsu_freeze_"
    "member_component_ledger.jsonl.gz"
)
C15_SHA256 = "e70c667fd8f14cb3c3d6444bb752dfc86244e61be292a9f884889d53951ff25a"
C15_SCHEMA = (
    "cm2.round306c15.source-g-502204-member-fresh-dsu-freeze.v1."
    "member-component-row.v1"
)
EDGE_SCHEMA = (
    "cm2.c27-independent.primitive-twenty-family-gate-v5-actual."
    "full-component-edge-union.row.v2"
)
EDGE_PREFIX = "round306c27r2-v5-component-edge:"
POST_PREFIX = "round306c27r2-source-g-post-component:"
OLD_TO_POST_SCHEMA = (
    "cm2.round306c27r2.source-g-actual-v2-fresh-quotient-rebuild.v2."
    "old-c15-component-to-post-component-row.v1"
)
MEMBER_TO_POST_SCHEMA = (
    "cm2.round306c27r2.source-g-actual-v2-fresh-quotient-rebuild.v2."
    "member-to-post-component-row.v1"
)
POST_CENSUS_SCHEMA = (
    "cm2.round306c27r2.source-g-actual-v2-fresh-quotient-rebuild.v2."
    "post-component-census-row.v1"
)
RESULT_SCHEMA = (
    "cm2.round306c27r2.source-g-actual-v2-fresh-quotient-rebuild.v2."
    "producer-result.v1"
)
TERMINAL_SCHEMA = (
    "cm2.c27-independent.primitive-twenty-family-gate-v5-actual-v2-"
    "dual-seed-terminal-receipt.v1"
)
TERMINAL_STATUS = (
    "PASS_ACTUAL_V2_TWO_REAL_SEEDS_INDEPENDENT_REPLAY_24_ATTACKS_"
    "COLD_REPLAY_TERMINAL_SEAL__ZERO_CREDIT"
)
BASE_SCHEMA = (
    "cm2.c27-independent.primitive-twenty-family-gate-v5-actual-v2-"
    "dual-seed-zero-credit-seal.v1"
)
BASE_STATUS = (
    "PASS_SEALED_TWO_REAL_SEEDS_NATIVE_AND_INDEPENDENT_REPLAY_PLUS_"
    "24_ATTACKS__PENDING_COLD_REPLAY__ZERO_CREDIT"
)
EXPECTED = {
    "members": 502_204,
    "old_components": 57_876,
    "edges": 14_860,
    "merges": 14_192,
    "cycles": 668,
    "post_components": 43_684,
    "total_pairs": 126_104_177_706,
    "within_pairs": 542_179_508,
    "cross_pairs": 125_561_998_198,
}
OUTPUT_NAMES = {
    "old_to_post": "old_c15_component_to_post_component.jsonl.gz",
    "member_to_post": "member_to_post_component.jsonl.gz",
    "post_census": "post_component_census.jsonl.gz",
    "result": "result.json",
}


class Failure(RuntimeError):
    pass


def need(value: bool, label: str) -> None:
    if type(value) is not bool or not value:
        raise Failure(label)


def canonical(value: Any) -> bytes:
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=True,
        allow_nan=False,
    ).encode("ascii")


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def close_row(body: dict[str, Any]) -> dict[str, Any]:
    return {**body, "row_sha256": digest(body)}


def sequence(values: list[str]) -> str:
    state = hashlib.sha256()
    for value in values:
        state.update(value.encode("ascii") + b"\n")
    return state.hexdigest()


def is_sha256(value: Any) -> bool:
    return (
        type(value) is str and len(value) == 64
        and all(character in "0123456789abcdef" for character in value)
    )


def strict_loads(payload: bytes) -> Any:
    def pairs(items: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in items:
            need(key not in result, "duplicate JSON key:" + key)
            result[key] = value
        return result

    def constant(value: str) -> None:
        raise Failure("non-finite JSON:" + value)

    return json.loads(payload, object_pairs_hook=pairs, parse_constant=constant)


def lexical_inside(raw: str | Path, *, may_not_exist: bool = False) -> Path:
    value = Path(raw)
    path = (ROOT / value if not value.is_absolute() else value).absolute()
    try:
        relative = path.relative_to(ROOT)
    except ValueError as error:
        raise Failure("path outside workspace:" + str(raw)) from error
    need(all(piece not in {"", ".", ".."} for piece in relative.parts),
         "canonical workspace path:" + str(raw))
    current = ROOT
    for piece in relative.parts:
        current = current / piece
        if not current.exists():
            need(may_not_exist, "missing path component:" + str(current))
            break
        need(not current.is_symlink(), "symlink path component:" + str(current))
    return path


def fingerprint(info: os.stat_result) -> tuple[int, ...]:
    return (
        info.st_dev, info.st_ino, info.st_mode, info.st_nlink, info.st_size,
        info.st_mtime_ns, info.st_ctime_ns, info.st_uid, info.st_gid,
    )


class Capture:
    """Stable, single-link, O_NOFOLLOW input capture."""

    def __init__(self, path: Path, label: str):
        self.path = lexical_inside(path)
        self.label = label
        self.fd = os.open(
            self.path,
            os.O_RDONLY | getattr(os, "O_CLOEXEC", 0)
            | getattr(os, "O_NOFOLLOW", 0),
        )
        self.before = os.fstat(self.fd)
        need(stat.S_ISREG(self.before.st_mode), label + ":regular")
        need(self.before.st_nlink == 1, label + ":single-link")
        self.sha256 = self._hash()

    def _rewind(self) -> None:
        os.lseek(self.fd, 0, os.SEEK_SET)

    def _hash(self) -> str:
        self._rewind()
        state = hashlib.sha256()
        while block := os.read(self.fd, 4 << 20):
            state.update(block)
        self._rewind()
        need(fingerprint(os.fstat(self.fd)) == fingerprint(self.before),
             self.label + ":stable-after-hash")
        return state.hexdigest()

    def bytes(self) -> bytes:
        self._rewind()
        chunks: list[bytes] = []
        while block := os.read(self.fd, 4 << 20):
            chunks.append(block)
        self._rewind()
        need(fingerprint(os.fstat(self.fd)) == fingerprint(self.before),
             self.label + ":stable-after-read")
        return b"".join(chunks)

    def json(self, closure: str | None = None) -> Any:
        payload = self.bytes()
        need(payload.endswith(b"\n"), self.label + ":JSON-newline")
        value = strict_loads(payload[:-1])
        need(canonical(value) == payload[:-1], self.label + ":canonical-JSON")
        if closure is not None:
            need(type(value) is dict, self.label + ":closed-object")
            body = dict(value)
            claim = body.pop(closure, None)
            need(is_sha256(claim) and claim == digest(body),
                 self.label + ":object-closure")
        return value

    def gzip_rows(self) -> Iterator[tuple[int, dict[str, Any]]]:
        self._rewind()
        duplicate = os.dup(self.fd)
        raw = os.fdopen(duplicate, "rb", closefd=True)
        try:
            with gzip.GzipFile(fileobj=raw, mode="rb") as stream:
                for ordinal, line in enumerate(stream):
                    need(line.endswith(b"\n"),
                         f"{self.label}:gzip-newline:{ordinal}")
                    payload = line[:-1]
                    row = strict_loads(payload)
                    need(type(row) is dict and canonical(row) == payload,
                         f"{self.label}:canonical-row:{ordinal}")
                    body = dict(row)
                    claim = body.pop("row_sha256", None)
                    need(is_sha256(claim) and claim == digest(body),
                         f"{self.label}:row-closure:{ordinal}")
                    yield ordinal, row
        except (EOFError, OSError, gzip.BadGzipFile) as error:
            raise Failure(self.label + ":gzip-integrity") from error
        finally:
            raw.close()
            self._rewind()
        need(fingerprint(os.fstat(self.fd)) == fingerprint(self.before),
             self.label + ":stable-after-gzip")

    def attestation(self) -> dict[str, Any]:
        current = os.fstat(self.fd)
        need(fingerprint(current) == fingerprint(self.before),
             self.label + ":pre-post-stat")
        need(self._hash() == self.sha256, self.label + ":pre-post-sha")
        return {
            "path": str(self.path.relative_to(ROOT)),
            "sha256": self.sha256,
            "size": self.before.st_size,
            "stat_fingerprint": list(fingerprint(self.before)),
            "O_NOFOLLOW": True,
            "single_open_file_description_hash_parse_fstat": True,
        }

    def close(self) -> None:
        os.close(self.fd)


def parse_manifest(capture: Capture) -> dict[str, str]:
    payload = capture.bytes()
    need(payload.endswith(b"\n"), capture.label + ":manifest-newline")
    rows: dict[str, str] = {}
    for ordinal, line in enumerate(payload.decode("ascii", "strict").splitlines()):
        pieces = line.split("  ", 1)
        need(len(pieces) == 2 and is_sha256(pieces[0]) and type(pieces[1]) is str and pieces[1] != "",
             f"{capture.label}:manifest-row:{ordinal}")
        claimed, name = pieces
        need(name not in rows, capture.label + ":manifest-unique")
        rows[name] = claimed
    return rows


def manifest_path(path: Path) -> str:
    return str(path.relative_to(ROOT))


def validate_expected_census(value: Any, label: str) -> None:
    need(type(value) is dict, label + ":object")
    checks = {
        "frozen_C15_member_total": EXPECTED["members"],
        "frozen_C15_component_total": EXPECTED["old_components"],
        "full_component_edge_union_total": EXPECTED["edges"],
        "fresh_DSU_successful_merges": EXPECTED["merges"],
        "fresh_DSU_cycle_edges": EXPECTED["cycles"],
        "fresh_DSU_final_component_total": EXPECTED["post_components"],
    }
    need(all(value.get(key) == expected for key, expected in checks.items()),
         label + ":exact-C27-census")


def load_authority(
    terminal_dir: Path,
    base_dir: Path,
    expected_terminal_root: str,
    expected_terminal_receipt_file: str,
    expected_terminal_receipt_object: str,
    seed_label: str,
) -> tuple[dict[str, Any], dict[str, Any], Capture, Capture,
           list[Capture]]:
    need(seed_label in {"seed1", "seed2"}, "authority seed label")
    terminal_dir = lexical_inside(terminal_dir)
    base_dir = lexical_inside(base_dir)
    need(terminal_dir.is_dir() and base_dir.is_dir()
         and terminal_dir != base_dir, "distinct terminal/base directories")
    need(is_sha256(expected_terminal_root)
         and is_sha256(expected_terminal_receipt_file)
         and is_sha256(expected_terminal_receipt_object),
         "required terminal SHA256 pins")
    pass_path = terminal_dir / "PASS.lock"
    need(pass_path.read_bytes()
         == b"PASS_ACTUAL_V2_DUAL_SEED_TERMINAL_ZERO_CREDIT_SEAL\n",
         "actual-v2 exact terminal PASS lock")
    need(not pass_path.is_symlink(), "actual-v2 PASS lock no symlink")

    terminal_root = Capture(terminal_dir / "root_manifest.sha256",
                            "terminal-root")
    terminal_payload = Capture(terminal_dir / "payload_manifest.sha256",
                               "terminal-payload")
    terminal_receipt_cap = Capture(terminal_dir / "terminal_receipt.json",
                                   "terminal-receipt")
    base_root = Capture(base_dir / "root_manifest.sha256", "base-root")
    base_payload = Capture(base_dir / "payload_manifest.sha256", "base-payload")
    base_receipt_cap = Capture(base_dir / "receipt.json", "base-receipt")
    captures = [terminal_root, terminal_payload, terminal_receipt_cap,
                base_root, base_payload, base_receipt_cap]
    try:
        need(terminal_root.sha256 == expected_terminal_root,
             "terminal root external pin")
        need(terminal_receipt_cap.sha256 == expected_terminal_receipt_file,
             "terminal receipt external file pin")
        terminal = terminal_receipt_cap.json("terminal_receipt_sha256")
        need(terminal["terminal_receipt_sha256"]
             == expected_terminal_receipt_object,
             "terminal receipt external object pin")
        need(
            terminal.get("schema") == TERMINAL_SCHEMA
            and terminal.get("status") == TERMINAL_STATUS
            and terminal.get("actual_v2_terminal_seal_passed") is True
            and terminal.get("formal_credit") == 0
            and terminal.get("manifest_authorized") is False
            and terminal.get("C27R2_C28_C29")
            == "AUTHORIZED_TO_BEGIN_FRESH_REBUILD_ONLY__NOT_REBUILT_NOT_CREDITED"
            and terminal.get("CM2") == "NO-GO_FOR_CLAIM",
            "terminal semantic authority",
        )
        validate_expected_census(terminal.get("exact_census"), "terminal")
        need(
            type(terminal.get("execution_seeds")) is list
            and len(terminal["execution_seeds"]) == 2
            and all(type(seed) is int and seed > 0
                    for seed in terminal["execution_seeds"])
            and terminal["execution_seeds"][0] != terminal["execution_seeds"][1],
            "terminal two real seeds",
        )

        terminal_root_rows = parse_manifest(terminal_root)
        need(terminal_root_rows == {
            "payload_manifest.sha256": terminal_payload.sha256,
            "terminal_receipt.json": terminal_receipt_cap.sha256,
        }, "terminal exact root manifest")
        terminal_payload_rows = parse_manifest(terminal_payload)
        need(len(terminal_payload_rows)
             == terminal["terminal_payload_manifest"]["entry_count"]
             and terminal_payload.sha256
             == terminal["terminal_payload_manifest"]["file_sha256"],
             "terminal payload descriptor")

        base = base_receipt_cap.json("receipt_sha256")
        binding = terminal.get("base_seal")
        need(type(binding) is dict
             and base_receipt_cap.sha256 == binding.get("receipt_file_sha256")
             and base["receipt_sha256"] == binding.get("receipt_object_sha256")
             and base_payload.sha256
                 == binding.get("payload_manifest_file_sha256")
             and base_root.sha256 == binding.get("root_manifest_file_sha256"),
             "terminal-to-base seal hash chain")
        need(
            terminal_payload_rows.get(manifest_path(base_root.path))
            == base_root.sha256
            and terminal_payload_rows.get(manifest_path(base_receipt_cap.path))
            == base_receipt_cap.sha256
            and terminal_payload_rows.get(manifest_path(base_payload.path))
            == base_payload.sha256,
            "terminal payload includes base seal",
        )
        need(
            base.get("schema") == BASE_SCHEMA
            and base.get("status") == BASE_STATUS
            and base.get("formal_credit") == 0
            and base.get("manifest_authorized") is False
            and base.get("actual_v2_terminal_gate") == "PENDING_COLD_REPLAY"
            and base.get("CM2") == "NO-GO_FOR_CLAIM",
            "base seal semantic authority",
        )
        need(base.get("execution_seeds") == terminal["execution_seeds"],
             "base/terminal seed binding")
        validate_expected_census(base.get("exact_census"), "base")
        base_root_rows = parse_manifest(base_root)
        need(base_root_rows == {
            "payload_manifest.sha256": base_payload.sha256,
            "receipt.json": base_receipt_cap.sha256,
        }, "base exact root manifest")
        base_payload_rows = parse_manifest(base_payload)
        need(len(base_payload_rows) == base["payload_manifest"]["entry_count"]
             and base_payload.sha256 == base["payload_manifest"]["file_sha256"],
             "base payload descriptor")

        attestations = base.get("root_input_capture", {}).get("attestations")
        need(type(attestations) is dict, "base root input attestations")
        edge_one = attestations.get("seed1_full_component_edge_union")
        edge_two = attestations.get("seed2_full_component_edge_union")
        c15_attestation = attestations.get("frozen_C15")
        need(all(type(item) is dict
                 for item in (edge_one, edge_two, c15_attestation)),
             "base selected input attestations")
        need(edge_one["path"] != edge_two["path"]
             and edge_one["sha256"] == edge_two["sha256"]
             and edge_one["size"] == edge_two["size"],
             "dual-seed edge byte identity")
        chosen = edge_one if seed_label == "seed1" else edge_two
        edge = Capture(lexical_inside(chosen["path"]), seed_label + "-edge")
        c15 = Capture(lexical_inside(C15_RELATIVE), "frozen-C15")
        captures.extend((edge, c15))
        need(edge.sha256 == chosen["sha256"]
             and edge.before.st_size == chosen["size"]
             and base_payload_rows.get(chosen["path"]) == edge.sha256,
             seed_label + " edge terminal pin")
        need(c15.sha256 == C15_SHA256
             and c15_attestation["path"] == C15_RELATIVE
             and c15_attestation["sha256"] == C15_SHA256
             and c15.before.st_size == c15_attestation["size"]
             and base_payload_rows.get(C15_RELATIVE) == C15_SHA256
             and terminal.get("source_pins", {}).get("frozen_C15")
                 == C15_SHA256,
             "frozen C15 terminal pin")
        return terminal, base, edge, c15, captures
    except BaseException:
        for capture in captures:
            capture.close()
        raise


class DSU:
    def __init__(self, values: list[str]):
        need(values == sorted(values) and len(values) == len(set(values)),
             "DSU sorted unique values")
        self.values = values
        self.index = {value: ordinal for ordinal, value in enumerate(values)}
        self.parent = list(range(len(values)))
        self.size = [1] * len(values)
        self.merges = 0

    def find_index(self, value: int) -> int:
        while self.parent[value] != value:
            self.parent[value] = self.parent[self.parent[value]]
            value = self.parent[value]
        return value

    def find(self, value: str) -> int:
        need(value in self.index, "DSU known component:" + value)
        return self.find_index(self.index[value])

    def union(self, left: str, right: str) -> bool:
        a, b = self.find(left), self.find(right)
        if a == b:
            return False
        if self.size[a] < self.size[b] or (
            self.size[a] == self.size[b] and self.values[a] > self.values[b]
        ):
            a, b = b, a
        self.parent[b] = a
        self.size[a] += self.size[b]
        self.merges += 1
        return True

    def groups(self) -> list[list[str]]:
        values: dict[int, list[str]] = defaultdict(list)
        for component in self.values:
            values[self.find(component)].append(component)
        return sorted((sorted(group) for group in values.values()),
                      key=lambda group: group[0])


def read_c15(capture: Capture) -> tuple[list[tuple[str, str]], list[str],
                                         Counter[str]]:
    members: list[tuple[str, str]] = []
    component_members: Counter[str] = Counter()
    seen_members: set[str] = set()
    for ordinal, row in capture.gzip_rows():
        need(row.get("schema") == C15_SCHEMA
             and row.get("member_ordinal") == ordinal,
             f"C15 schema/ordinal:{ordinal}")
        member = row.get("registry_member_id")
        component = row.get("fresh_component_id")
        need(type(member) is str and member and member not in seen_members,
             f"C15 unique member:{ordinal}")
        need(type(component) is str and component != "",
             f"C15 component:{ordinal}")
        seen_members.add(member)
        members.append((member, component))
        component_members[component] += 1
    components = sorted(component_members)
    need(len(members) == EXPECTED["members"]
         and len(components) == EXPECTED["old_components"],
         "C15 exact member/component census")
    return members, components, component_members


def apply_edges(capture: Capture, components: list[str]) -> tuple[DSU, int, int,
                                                                  str]:
    dsu = DSU(components)
    previous: str | None = None
    seen_pairs: set[tuple[str, str]] = set()
    edge_hashes: list[str] = []
    merges = cycles = 0
    for ordinal, row in capture.gzip_rows():
        need(row.get("schema") == EDGE_SCHEMA and row.get("ordinal") == ordinal,
             f"edge schema/ordinal:{ordinal}")
        key = row.get("component_edge_key")
        pair = row.get("ordered_C15_component_pair")
        need(type(key) is str and (previous is None or previous < key),
             f"edge strict key order:{ordinal}")
        previous = key
        need(type(pair) is list and len(pair) == 2
             and all(type(value) is str for value in pair)
             and pair[0] < pair[1]
             and tuple(pair) not in seen_pairs,
             f"edge ordered unique pair:{ordinal}")
        seen_pairs.add(tuple(pair))
        need(key == EDGE_PREFIX + digest(pair), f"edge key formula:{ordinal}")
        need(row.get("formal_credit") == 0
             and type(row.get("supporting_physical_proof_row_count")) is int
             and row["supporting_physical_proof_row_count"] > 0
             and is_sha256(
                 row.get("supporting_physical_proof_row_sequence_sha256")
             ), f"edge proof/credit closure:{ordinal}")
        if dsu.union(pair[0], pair[1]):
            merges += 1
        else:
            cycles += 1
        edge_hashes.append(row["row_sha256"])
    need(len(edge_hashes) == EXPECTED["edges"]
         and merges == EXPECTED["merges"]
         and cycles == EXPECTED["cycles"]
         and dsu.merges == EXPECTED["merges"],
         "actual-v2 exact edge/DSU census")
    return dsu, merges, cycles, sequence(edge_hashes)


def quotient(
    dsu: DSU,
    component_members: Counter[str],
) -> tuple[dict[str, str], dict[str, dict[str, Any]], int]:
    old_to_post: dict[str, str] = {}
    census: dict[str, dict[str, Any]] = {}
    within_pairs = 0
    for group in dsu.groups():
        post = POST_PREFIX + digest(group)
        need(post not in census, "post component hash collision")
        member_count = sum(component_members[old] for old in group)
        within = member_count * (member_count - 1) // 2
        body = {
            "old_component_ids": group,
            "old_component_ids_sha256": sequence(group),
            "old_component_count": len(group),
            "member_count": member_count,
            "within_member_pair_count": within,
        }
        census[post] = body
        within_pairs += within
        for old in group:
            need(old not in old_to_post, "old component assigned once")
            old_to_post[old] = post
    need(len(old_to_post) == EXPECTED["old_components"]
         and len(census) == EXPECTED["post_components"]
         and within_pairs == EXPECTED["within_pairs"],
         "quotient exact component/within-pair census")
    return old_to_post, census, within_pairs


class LedgerWriter:
    def __init__(self, path: Path, schema: str, ordering: list[str],
                 unique_key: str):
        self.path = path
        self.schema = schema
        self.ordering = ordering
        self.unique_key = unique_key
        flags = (os.O_WRONLY | os.O_CREAT | os.O_EXCL
                 | getattr(os, "O_NOFOLLOW", 0))
        descriptor = os.open(path, flags, 0o600)
        self.raw = os.fdopen(descriptor, "wb")
        self.stream = gzip.GzipFile(
            filename="", mode="wb", compresslevel=9, fileobj=self.raw, mtime=0,
        )
        self.count = 0
        self.row_sequence = hashlib.sha256()

    def write(self, row: dict[str, Any]) -> None:
        need(row.get("schema") == self.schema
             and row.get("ordinal") == self.count,
             "output ledger schema/ordinal")
        body = dict(row)
        claim = body.pop("row_sha256", None)
        need(is_sha256(claim) and claim == digest(body),
             "output ledger row closure")
        self.stream.write(canonical(row) + b"\n")
        self.row_sequence.update(claim.encode("ascii") + b"\n")
        self.count += 1

    def finish(self) -> dict[str, Any]:
        self.stream.close()
        self.raw.flush()
        os.fsync(self.raw.fileno())
        self.raw.close()
        info = self.path.stat()
        need(stat.S_ISREG(info.st_mode) and info.st_nlink == 1,
             "output regular single-link ledger")
        state = hashlib.sha256()
        with self.path.open("rb") as stream:
            while block := stream.read(4 << 20):
                state.update(block)
        return {
            "filename": self.path.name,
            "sha256": state.hexdigest(),
            "size": info.st_size,
            "row_count": self.count,
            "row_schema": self.schema,
            "ordering": self.ordering,
            "unique_key": self.unique_key,
            "row_sequence_sha256": self.row_sequence.hexdigest(),
            "gzip_mtime": 0,
            "canonical_jsonl": True,
            "row_closure": "row_sha256=SHA256(canonical row without row_sha256)",
        }


def write_exclusive(path: Path, payload: bytes) -> None:
    descriptor = os.open(
        path,
        os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, "O_NOFOLLOW", 0),
        0o600,
    )
    try:
        total = 0
        while total < len(payload):
            total += os.write(descriptor, payload[total:])
        os.fsync(descriptor)
    finally:
        os.close(descriptor)


def build(args: argparse.Namespace) -> dict[str, Any]:
    out_dir = lexical_inside(args.out_dir, may_not_exist=True)
    need(not out_dir.exists(), "fresh output directory")
    terminal, base, edge, c15, captures = load_authority(
        Path(args.terminal_dir), Path(args.base_seal_dir),
        args.expect_terminal_root_sha256,
        args.expect_terminal_receipt_file_sha256,
        args.expect_terminal_receipt_object_sha256,
        "seed1",
    )
    producer_capture: Capture | None = None
    try:
        producer_capture = Capture(SELF, "producer-source")
        producer_source_sha256 = producer_capture.sha256
        producer_source_attestation = producer_capture.attestation()
        members, components, component_members = read_c15(c15)
        dsu, merges, cycles, edge_sequence = apply_edges(edge, components)
        old_to_post, census, within_pairs = quotient(dsu, component_members)
        total_pairs = len(members) * (len(members) - 1) // 2
        cross_pairs = total_pairs - within_pairs
        need(total_pairs == EXPECTED["total_pairs"]
             and cross_pairs == EXPECTED["cross_pairs"],
             "global pair identity")

        out_dir.mkdir(parents=True, mode=0o700)
        old_writer = LedgerWriter(
            out_dir / OUTPUT_NAMES["old_to_post"], OLD_TO_POST_SCHEMA,
            ["old_C15_component_id"], "old_C15_component_id",
        )
        for ordinal, old in enumerate(components):
            post = old_to_post[old]
            group = census[post]
            old_writer.write(close_row({
                "schema": OLD_TO_POST_SCHEMA,
                "ordinal": ordinal,
                "old_C15_component_id": old,
                "post_C27R2_component_id": post,
                "post_C27R2_old_component_count":
                    group["old_component_count"],
                "post_C27R2_old_component_ids_sha256":
                    group["old_component_ids_sha256"],
                "formal_credit": 0,
            }))
        old_descriptor = old_writer.finish()

        member_writer = LedgerWriter(
            out_dir / OUTPUT_NAMES["member_to_post"], MEMBER_TO_POST_SCHEMA,
            ["member_ordinal"], "registry_member_id",
        )
        for ordinal, (member, old) in enumerate(members):
            member_writer.write(close_row({
                "schema": MEMBER_TO_POST_SCHEMA,
                "ordinal": ordinal,
                "member_ordinal": ordinal,
                "registry_member_id": member,
                "old_C15_component_id": old,
                "post_C27R2_component_id": old_to_post[old],
                "formal_credit": 0,
            }))
        member_descriptor = member_writer.finish()

        census_writer = LedgerWriter(
            out_dir / OUTPUT_NAMES["post_census"], POST_CENSUS_SCHEMA,
            ["post_C27R2_component_id"], "post_C27R2_component_id",
        )
        for ordinal, post in enumerate(sorted(census)):
            group = census[post]
            census_writer.write(close_row({
                "schema": POST_CENSUS_SCHEMA,
                "ordinal": ordinal,
                "post_C27R2_component_id": post,
                "old_C15_component_count": group["old_component_count"],
                "old_C15_component_ids_sha256":
                    group["old_component_ids_sha256"],
                "member_count": group["member_count"],
                "within_member_pair_count": group["within_member_pair_count"],
                "formal_credit": 0,
            }))
        census_descriptor = census_writer.finish()

        input_attestations = {
            capture.label: capture.attestation() for capture in captures
        }
        body = {
            "schema": RESULT_SCHEMA,
            "status": (
                "PASS_FRESH_ACTUAL_V2_SEED1_QUOTIENT_REBUILD_"
                "ZERO_CREDIT__PENDING_NO_IMPORT_SEED2_VERIFICATION_"
                "ATTACKS_COLD_REPLAY_AND_TERMINAL_SEAL"
            ),
            "producer_source_sha256": producer_source_sha256,
            "producer_source_attestation": producer_source_attestation,
            "authority": {
                "actual_v2_terminal_root_manifest_sha256":
                    args.expect_terminal_root_sha256,
                "actual_v2_terminal_receipt_file_sha256":
                    args.expect_terminal_receipt_file_sha256,
                "actual_v2_terminal_receipt_object_sha256":
                    args.expect_terminal_receipt_object_sha256,
                "actual_v2_base_seal_receipt_file_sha256":
                    terminal["base_seal"]["receipt_file_sha256"],
                "actual_v2_base_seal_receipt_object_sha256":
                    terminal["base_seal"]["receipt_object_sha256"],
                "actual_v2_seed_label": "seed1",
                "actual_v2_execution_seed": terminal["execution_seeds"][0],
                "actual_v2_edge_ledger_path":
                    input_attestations["seed1-edge"]["path"],
                "actual_v2_edge_ledger_sha256": edge.sha256,
                "frozen_C15_path": C15_RELATIVE,
                "frozen_C15_sha256": C15_SHA256,
            },
            "canonical_post_component_id_formula": (
                POST_PREFIX
                + "SHA256(canonical JSON sorted list of old C15 component IDs)"
            ),
            "exact_census": {
                "frozen_C15_members": len(members),
                "frozen_C15_components": len(components),
                "proof_derived_component_edges": EXPECTED["edges"],
                "successful_DSU_merges": merges,
                "cycle_edges": cycles,
                "post_C27R2_components": len(census),
                "total_unordered_member_pairs": total_pairs,
                "within_post_component_member_pairs": within_pairs,
                "cross_post_component_member_pairs": cross_pairs,
            },
            "edge_row_sequence_sha256": edge_sequence,
            "ledgers": {
                "old_C15_component_to_post_component": old_descriptor,
                "member_to_post_component": member_descriptor,
                "post_component_census": census_descriptor,
            },
            "derivation_closures": {
                "DSU_started_from_all_57876_frozen_C15_components": True,
                "only_terminal_pinned_actual_v2_seed1_edges_applied": True,
                "post_component_ID_never_uses_DSU_root": True,
                "all_502204_members_rebound_through_frozen_C15": True,
                "pair_identity_total_equals_within_plus_cross": True,
                "old_C27_C28_C29_partition_imported_or_read": False,
            },
            "input_pre_post_attestations": input_attestations,
            "formal_credit": 0,
            "manifest_authorized": False,
            "C27R2": "UNAUTHORIZED_PENDING_INDEPENDENT_VERIFICATION_AND_TERMINAL_SEAL",
            "C28_C29": "UNAUTHORIZED",
            "Source_W": "UNCHANGED_BY_SOURCE_G_REBUILD_CANDIDATE",
            "CM2": "NO-GO_FOR_CLAIM",
        }
        producer_final = Capture(SELF, "producer-source-final")
        try:
            need(producer_final.attestation()
                 == body["producer_source_attestation"],
                 "producer source independent final SHA/stat")
        finally:
            producer_final.close()
        result = dict(body)
        result["result_sha256"] = digest(result)
        write_exclusive(out_dir / OUTPUT_NAMES["result"],
                        canonical(result) + b"\n")
        return result
    finally:
        if producer_capture is not None:
            producer_capture.close()
        for capture in captures:
            capture.close()


def self_test() -> dict[str, Any]:
    values = ["c0", "c1", "c2", "c3", "c4"]
    dsu = DSU(values)
    outcomes = [
        dsu.union("c0", "c1"), dsu.union("c1", "c2"),
        dsu.union("c0", "c2"), dsu.union("c3", "c4"),
    ]
    need(outcomes == [True, True, False, True], "fixture merge/cycle")
    groups = dsu.groups()
    need(groups == [["c0", "c1", "c2"], ["c3", "c4"]],
         "fixture canonical groups")
    counts = Counter({"c0": 2, "c1": 1, "c2": 3, "c3": 1, "c4": 1})
    old_to_post, census, within = quotient_fixture(dsu, counts)
    need(len(old_to_post) == 5 and len(census) == 2 and within == 16,
         "fixture quotient/pairs")
    need(old_to_post["c0"] == POST_PREFIX + digest(["c0", "c1", "c2"]),
         "fixture canonical post ID")
    # Deterministic gzip smoke test outside the workspace.
    with tempfile.TemporaryDirectory(prefix="cm2-c27r2-v2-selftest-") as raw:
        path = Path(raw) / "fixture.jsonl.gz"
        writer = LedgerWriter(path, OLD_TO_POST_SCHEMA,
                              ["old_C15_component_id"],
                              "old_C15_component_id")
        writer.write(close_row({
            "schema": OLD_TO_POST_SCHEMA, "ordinal": 0,
            "old_C15_component_id": "c0",
            "post_C27R2_component_id": old_to_post["c0"],
            "formal_credit": 0,
        }))
        descriptor = writer.finish()
        need(descriptor["row_count"] == 1 and descriptor["gzip_mtime"] == 0,
             "fixture deterministic gzip")
    return {
        "schema": RESULT_SCHEMA + ".self-test",
        "status": "PASS_SMALL_FIXTURE_DSU_CANONICAL_ID_PAIR_AND_GZIP_TESTS",
        "fixture_groups": groups,
        "fixture_within_pairs": within,
        "formal_credit": 0,
        "CM2": "NO-GO_FOR_CLAIM",
    }


def quotient_fixture(
    dsu: DSU, component_members: Counter[str]
) -> tuple[dict[str, str], dict[str, dict[str, Any]], int]:
    old_to_post: dict[str, str] = {}
    census: dict[str, dict[str, Any]] = {}
    within = 0
    for group in dsu.groups():
        post = POST_PREFIX + digest(group)
        count = sum(component_members[item] for item in group)
        pairs = count * (count - 1) // 2
        census[post] = {
            "old_component_ids": group,
            "old_component_ids_sha256": sequence(group),
            "old_component_count": len(group),
            "member_count": count,
            "within_member_pair_count": pairs,
        }
        within += pairs
        for old in group:
            old_to_post[old] = post
    return old_to_post, census, within


def parser() -> argparse.ArgumentParser:
    value = argparse.ArgumentParser(description=__doc__)
    value.add_argument("--self-test", action="store_true")
    value.add_argument("--terminal-dir")
    value.add_argument("--base-seal-dir")
    value.add_argument("--expect-terminal-root-sha256")
    value.add_argument("--expect-terminal-receipt-file-sha256")
    value.add_argument("--expect-terminal-receipt-object-sha256")
    value.add_argument("--out-dir")
    return value


def main() -> int:
    args = parser().parse_args()
    try:
        if args.self_test:
            need(all(getattr(args, name) is None for name in (
                "terminal_dir", "base_seal_dir", "expect_terminal_root_sha256",
                "expect_terminal_receipt_file_sha256",
                "expect_terminal_receipt_object_sha256", "out_dir",
            )), "self-test accepts no authority/output arguments")
            result = self_test()
        else:
            need(all(getattr(args, name) is not None for name in (
                "terminal_dir", "base_seal_dir", "expect_terminal_root_sha256",
                "expect_terminal_receipt_file_sha256",
                "expect_terminal_receipt_object_sha256", "out_dir",
            )), "all authority pins and fresh output directory are required")
            result = build(args)
        sys.stdout.buffer.write(canonical({
            "status": result["status"], "formal_credit": 0,
            "CM2": "NO-GO_FOR_CLAIM",
        }) + b"\n")
        return 0
    except (Failure, OSError, ValueError, KeyError, TypeError) as error:
        sys.stderr.write("REJECT:" + str(error) + "\n")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
