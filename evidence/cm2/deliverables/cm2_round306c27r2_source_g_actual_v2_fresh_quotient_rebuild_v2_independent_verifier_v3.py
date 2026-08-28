#!/usr/bin/env python3
"""No-import verifier for the fresh C27R2 actual-v2 quotient candidate.

The verifier does not import or execute the producer.  It follows the pinned
actual-v2 terminal-to-base-seal chain independently, selects the seed-2 edge
ledger, reparses frozen C15, rebuilds the DSU, derives canonical post-component
IDs from sorted old-component sets, and compares every candidate ledger row.
Its PASS is conditional and always carries zero formal credit.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import ast
import gzip
import hashlib
import json
import os
from pathlib import Path
import stat
import sys
import tempfile
from typing import Any, Iterator


WORKSPACE = Path(__file__).resolve().parent.parent
THIS_FILE = Path(__file__).resolve()
PRODUCER_BASENAME = (
    "cm2_round306c27r2_source_g_actual_v2_fresh_quotient_rebuild_v2_producer_v3.py"
)
C15_REL = (
    "deliverables/"
    "cm2_round306c15_source_g_502204_member_fresh_dsu_freeze_"
    "member_component_ledger.jsonl.gz"
)
C15_HASH = "e70c667fd8f14cb3c3d6444bb752dfc86244e61be292a9f884889d53951ff25a"
C15_ROW_TYPE = (
    "cm2.round306c15.source-g-502204-member-fresh-dsu-freeze.v1."
    "member-component-row.v1"
)
EDGE_ROW_TYPE = (
    "cm2.c27-independent.primitive-twenty-family-gate-v5-actual."
    "full-component-edge-union.row.v2"
)
EDGE_KEY_PREFIX = "round306c27r2-v5-component-edge:"
POST_KEY_PREFIX = "round306c27r2-source-g-post-component:"
OLD_MAP_TYPE = (
    "cm2.round306c27r2.source-g-actual-v2-fresh-quotient-rebuild.v2."
    "old-c15-component-to-post-component-row.v1"
)
MEMBER_MAP_TYPE = (
    "cm2.round306c27r2.source-g-actual-v2-fresh-quotient-rebuild.v2."
    "member-to-post-component-row.v1"
)
POST_CENSUS_TYPE = (
    "cm2.round306c27r2.source-g-actual-v2-fresh-quotient-rebuild.v2."
    "post-component-census-row.v1"
)
PRODUCER_RESULT_TYPE = (
    "cm2.round306c27r2.source-g-actual-v2-fresh-quotient-rebuild.v2."
    "producer-result.v1"
)
VERIFICATION_TYPE = (
    "cm2.round306c27r2.source-g-actual-v2-fresh-quotient-rebuild.v2."
    "independent-verification.v1"
)
ACTUAL_TERMINAL_TYPE = (
    "cm2.c27-independent.primitive-twenty-family-gate-v5-actual-v2-"
    "dual-seed-terminal-receipt.v1"
)
ACTUAL_TERMINAL_PASS = (
    "PASS_ACTUAL_V2_TWO_REAL_SEEDS_INDEPENDENT_REPLAY_24_ATTACKS_"
    "COLD_REPLAY_TERMINAL_SEAL__ZERO_CREDIT"
)
ACTUAL_BASE_TYPE = (
    "cm2.c27-independent.primitive-twenty-family-gate-v5-actual-v2-"
    "dual-seed-zero-credit-seal.v1"
)
ACTUAL_BASE_PASS = (
    "PASS_SEALED_TWO_REAL_SEEDS_NATIVE_AND_INDEPENDENT_REPLAY_PLUS_"
    "24_ATTACKS__PENDING_COLD_REPLAY__ZERO_CREDIT"
)
COUNTS = {
    "members": 502_204,
    "old": 57_876,
    "edges": 14_860,
    "merges": 14_192,
    "cycles": 668,
    "post": 43_684,
    "all_pairs": 126_104_177_706,
    "within": 542_179_508,
    "cross": 125_561_998_198,
}
FILES = {
    "old": "old_c15_component_to_post_component.jsonl.gz",
    "member": "member_to_post_component.jsonl.gz",
    "census": "post_component_census.jsonl.gz",
    "result": "result.json",
}


class Reject(RuntimeError):
    pass


def require(condition: bool, label: str) -> None:
    if type(condition) is not bool or not condition:
        raise Reject(label)


def wire(value: Any) -> bytes:
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=True,
        allow_nan=False,
    ).encode("ascii")


def object_hash(value: Any) -> str:
    return hashlib.sha256(wire(value)).hexdigest()


def row_close(body: dict[str, Any]) -> dict[str, Any]:
    return {**body, "row_sha256": object_hash(body)}


def hash_sequence(values: list[str]) -> str:
    state = hashlib.sha256()
    for value in values:
        state.update(value.encode("ascii") + b"\n")
    return state.hexdigest()


def valid_hash(value: Any) -> bool:
    return (
        type(value) is str and len(value) == 64
        and all(character in "0123456789abcdef" for character in value)
    )


def strict_decode(payload: bytes) -> Any:
    def pairs(items: list[tuple[str, Any]]) -> dict[str, Any]:
        value: dict[str, Any] = {}
        for key, item in items:
            require(key not in value, "duplicate JSON key:" + key)
            value[key] = item
        return value

    def constant(value: str) -> None:
        raise Reject("non-finite JSON:" + value)

    return json.loads(payload, object_pairs_hook=pairs, parse_constant=constant)


def workspace_path(raw: str | Path, *, absent_allowed: bool = False) -> Path:
    supplied = Path(raw)
    path = (WORKSPACE / supplied if not supplied.is_absolute()
            else supplied).absolute()
    try:
        relative = path.relative_to(WORKSPACE)
    except ValueError as error:
        raise Reject("path outside workspace:" + str(raw)) from error
    require(all(part not in {"", ".", ".."} for part in relative.parts),
            "canonical workspace path:" + str(raw))
    current = WORKSPACE
    for part in relative.parts:
        current = current / part
        if not current.exists():
            require(absent_allowed, "missing path component:" + str(current))
            break
        require(not current.is_symlink(), "symlink path component:" + str(current))
    return path


def stat_key(info: os.stat_result) -> tuple[int, ...]:
    return (
        info.st_dev, info.st_ino, info.st_mode, info.st_nlink, info.st_size,
        info.st_mtime_ns, info.st_ctime_ns, info.st_uid, info.st_gid,
    )


class FileView:
    def __init__(self, path: Path, label: str):
        self.path = workspace_path(path)
        self.label = label
        self.handle = os.open(
            self.path,
            os.O_RDONLY | getattr(os, "O_CLOEXEC", 0)
            | getattr(os, "O_NOFOLLOW", 0),
        )
        self.initial = os.fstat(self.handle)
        require(stat.S_ISREG(self.initial.st_mode), label + ":regular")
        require(self.initial.st_nlink == 1, label + ":single-link")
        self.sha256 = self._sha()

    def _seek(self) -> None:
        os.lseek(self.handle, 0, os.SEEK_SET)

    def _sha(self) -> str:
        self._seek()
        state = hashlib.sha256()
        while chunk := os.read(self.handle, 4 << 20):
            state.update(chunk)
        self._seek()
        require(stat_key(os.fstat(self.handle)) == stat_key(self.initial),
                self.label + ":stable-hash")
        return state.hexdigest()

    def read(self) -> bytes:
        self._seek()
        blocks: list[bytes] = []
        while chunk := os.read(self.handle, 4 << 20):
            blocks.append(chunk)
        self._seek()
        require(stat_key(os.fstat(self.handle)) == stat_key(self.initial),
                self.label + ":stable-read")
        return b"".join(blocks)

    def document(self, closure: str | None = None) -> Any:
        raw = self.read()
        require(raw.endswith(b"\n"), self.label + ":document-newline")
        value = strict_decode(raw[:-1])
        require(wire(value) == raw[:-1], self.label + ":canonical-document")
        if closure is not None:
            require(type(value) is dict, self.label + ":closed-document")
            body = dict(value)
            claim = body.pop(closure, None)
            require(valid_hash(claim) and claim == object_hash(body),
                    self.label + ":document-closure")
        return value

    def rows(self) -> Iterator[tuple[int, dict[str, Any]]]:
        self._seek()
        duplicate = os.dup(self.handle)
        raw = os.fdopen(duplicate, "rb", closefd=True)
        try:
            with gzip.GzipFile(fileobj=raw, mode="rb") as stream:
                for ordinal, line in enumerate(stream):
                    require(line.endswith(b"\n"),
                            f"{self.label}:row-newline:{ordinal}")
                    payload = line[:-1]
                    value = strict_decode(payload)
                    require(type(value) is dict and wire(value) == payload,
                            f"{self.label}:canonical-row:{ordinal}")
                    body = dict(value)
                    claim = body.pop("row_sha256", None)
                    require(valid_hash(claim) and claim == object_hash(body),
                            f"{self.label}:row-closure:{ordinal}")
                    yield ordinal, value
        except (EOFError, OSError, gzip.BadGzipFile) as error:
            raise Reject(self.label + ":gzip-integrity") from error
        finally:
            raw.close()
            self._seek()
        require(stat_key(os.fstat(self.handle)) == stat_key(self.initial),
                self.label + ":stable-gzip")

    def attest(self) -> dict[str, Any]:
        require(stat_key(os.fstat(self.handle)) == stat_key(self.initial),
                self.label + ":pre-post-stat")
        require(self._sha() == self.sha256, self.label + ":pre-post-sha")
        return {
            "path": str(self.path.relative_to(WORKSPACE)),
            "sha256": self.sha256,
            "size": self.initial.st_size,
            "stat_fingerprint": list(stat_key(self.initial)),
            "O_NOFOLLOW": True,
            "single_open_file_description_hash_parse_fstat": True,
        }

    def close(self) -> None:
        os.close(self.handle)


def manifest(view: FileView) -> dict[str, str]:
    raw = view.read()
    require(raw.endswith(b"\n"), view.label + ":manifest-newline")
    result: dict[str, str] = {}
    for ordinal, line in enumerate(raw.decode("ascii", "strict").splitlines()):
        parts = line.split("  ", 1)
        require(len(parts) == 2 and valid_hash(parts[0]) and type(parts[1]) is str and parts[1] != "",
                f"{view.label}:manifest-row:{ordinal}")
        require(parts[1] not in result, view.label + ":manifest-unique")
        result[parts[1]] = parts[0]
    return result


def rel(path: Path) -> str:
    return str(path.relative_to(WORKSPACE))


def census_contract(value: Any, label: str) -> None:
    require(type(value) is dict, label + ":census-object")
    expected = {
        "frozen_C15_member_total": COUNTS["members"],
        "frozen_C15_component_total": COUNTS["old"],
        "full_component_edge_union_total": COUNTS["edges"],
        "fresh_DSU_successful_merges": COUNTS["merges"],
        "fresh_DSU_cycle_edges": COUNTS["cycles"],
        "fresh_DSU_final_component_total": COUNTS["post"],
    }
    require(all(value.get(key) == item for key, item in expected.items()),
            label + ":exact-census")


def authority(
    terminal_raw: str,
    base_raw: str,
    terminal_root_pin: str,
    terminal_file_pin: str,
    terminal_object_pin: str,
) -> tuple[dict[str, Any], dict[str, Any], FileView, FileView,
           list[FileView]]:
    require(all(valid_hash(item) for item in (
        terminal_root_pin, terminal_file_pin, terminal_object_pin,
    )), "external terminal pins")
    terminal_dir = workspace_path(terminal_raw)
    base_dir = workspace_path(base_raw)
    require(terminal_dir.is_dir() and base_dir.is_dir()
            and terminal_dir != base_dir, "terminal/base directories")
    lock = terminal_dir / "PASS.lock"
    require(not lock.is_symlink()
            and lock.read_bytes()
            == b"PASS_ACTUAL_V2_DUAL_SEED_TERMINAL_ZERO_CREDIT_SEAL\n",
            "terminal exact PASS lock")
    tr = FileView(terminal_dir / "root_manifest.sha256", "terminal-root")
    tp = FileView(terminal_dir / "payload_manifest.sha256", "terminal-payload")
    td = FileView(terminal_dir / "terminal_receipt.json", "terminal-receipt")
    br = FileView(base_dir / "root_manifest.sha256", "base-root")
    bp = FileView(base_dir / "payload_manifest.sha256", "base-payload")
    bd = FileView(base_dir / "receipt.json", "base-receipt")
    views = [tr, tp, td, br, bp, bd]
    try:
        require(tr.sha256 == terminal_root_pin and td.sha256 == terminal_file_pin,
                "terminal external file pins")
        terminal = td.document("terminal_receipt_sha256")
        require(terminal["terminal_receipt_sha256"] == terminal_object_pin,
                "terminal external object pin")
        require(
            terminal.get("schema") == ACTUAL_TERMINAL_TYPE
            and terminal.get("status") == ACTUAL_TERMINAL_PASS
            and terminal.get("actual_v2_terminal_seal_passed") is True
            and terminal.get("formal_credit") == 0
            and terminal.get("manifest_authorized") is False
            and terminal.get("C27R2_C28_C29")
                == "AUTHORIZED_TO_BEGIN_FRESH_REBUILD_ONLY__NOT_REBUILT_NOT_CREDITED"
            and terminal.get("CM2") == "NO-GO_FOR_CLAIM",
            "terminal semantic contract",
        )
        census_contract(terminal.get("exact_census"), "terminal")
        seeds = terminal.get("execution_seeds")
        require(type(seeds) is list and len(seeds) == 2
                and all(type(seed) is int and seed > 0 for seed in seeds)
                and seeds[0] != seeds[1], "two terminal seeds")
        require(manifest(tr) == {
            "payload_manifest.sha256": tp.sha256,
            "terminal_receipt.json": td.sha256,
        }, "terminal root exact members")
        terminal_payload = manifest(tp)
        require(len(terminal_payload)
                == terminal["terminal_payload_manifest"]["entry_count"]
                and tp.sha256
                == terminal["terminal_payload_manifest"]["file_sha256"],
                "terminal payload contract")

        base = bd.document("receipt_sha256")
        binding = terminal.get("base_seal")
        require(type(binding) is dict
                and bd.sha256 == binding.get("receipt_file_sha256")
                and base["receipt_sha256"] == binding.get("receipt_object_sha256")
                and bp.sha256 == binding.get("payload_manifest_file_sha256")
                and br.sha256 == binding.get("root_manifest_file_sha256"),
                "terminal-to-base chain")
        require(terminal_payload.get(rel(br.path)) == br.sha256
                and terminal_payload.get(rel(bp.path)) == bp.sha256
                and terminal_payload.get(rel(bd.path)) == bd.sha256,
                "terminal payload contains base")
        require(
            base.get("schema") == ACTUAL_BASE_TYPE
            and base.get("status") == ACTUAL_BASE_PASS
            and base.get("execution_seeds") == seeds
            and base.get("formal_credit") == 0
            and base.get("manifest_authorized") is False
            and base.get("actual_v2_terminal_gate") == "PENDING_COLD_REPLAY"
            and base.get("CM2") == "NO-GO_FOR_CLAIM",
            "base semantic contract",
        )
        census_contract(base.get("exact_census"), "base")
        require(manifest(br) == {
            "payload_manifest.sha256": bp.sha256,
            "receipt.json": bd.sha256,
        }, "base root exact members")
        base_payload = manifest(bp)
        require(len(base_payload) == base["payload_manifest"]["entry_count"]
                and bp.sha256 == base["payload_manifest"]["file_sha256"],
                "base payload contract")
        inputs = base.get("root_input_capture", {}).get("attestations")
        require(type(inputs) is dict, "base input attestations")
        edge1 = inputs.get("seed1_full_component_edge_union")
        edge2 = inputs.get("seed2_full_component_edge_union")
        c15_claim = inputs.get("frozen_C15")
        require(all(type(item) is dict for item in (edge1, edge2, c15_claim)),
                "selected base attestations")
        require(edge1["path"] != edge2["path"]
                and edge1["sha256"] == edge2["sha256"]
                and edge1["size"] == edge2["size"],
                "dual seed edges byte-identical")
        edge = FileView(workspace_path(edge2["path"]), "seed2-edge")
        c15 = FileView(workspace_path(C15_REL), "frozen-C15")
        views.extend((edge, c15))
        require(edge.sha256 == edge2["sha256"]
                and edge.initial.st_size == edge2["size"]
                and base_payload.get(edge2["path"]) == edge.sha256,
                "seed2 edge pinned")
        require(c15.sha256 == C15_HASH
                and c15_claim["path"] == C15_REL
                and c15_claim["sha256"] == C15_HASH
                and c15.initial.st_size == c15_claim["size"]
                and base_payload.get(C15_REL) == C15_HASH
                and terminal.get("source_pins", {}).get("frozen_C15")
                    == C15_HASH,
                "frozen C15 pinned")
        return terminal, base, edge, c15, views
    except BaseException:
        for view in views:
            view.close()
        raise


class UnionFind:
    def __init__(self, components: list[str]):
        require(components == sorted(components)
                and len(components) == len(set(components)),
                "union-find sorted unique components")
        self.components = components
        self.position = {value: index for index, value in enumerate(components)}
        self.parent = list(range(len(components)))
        self.weight = [1] * len(components)
        self.merge_count = 0

    def root(self, index: int) -> int:
        while self.parent[index] != index:
            self.parent[index] = self.parent[self.parent[index]]
            index = self.parent[index]
        return index

    def locate(self, component: str) -> int:
        require(component in self.position, "known component:" + component)
        return self.root(self.position[component])

    def join(self, left: str, right: str) -> bool:
        a, b = self.locate(left), self.locate(right)
        if a == b:
            return False
        if self.weight[a] < self.weight[b] or (
            self.weight[a] == self.weight[b]
            and self.components[a] > self.components[b]
        ):
            a, b = b, a
        self.parent[b] = a
        self.weight[a] += self.weight[b]
        self.merge_count += 1
        return True

    def partitions(self) -> list[list[str]]:
        groups: dict[int, list[str]] = defaultdict(list)
        for component in self.components:
            groups[self.locate(component)].append(component)
        return sorted((sorted(group) for group in groups.values()),
                      key=lambda group: group[0])


def frozen_partition(c15: FileView) -> tuple[list[tuple[str, str]], list[str],
                                             Counter[str]]:
    members: list[tuple[str, str]] = []
    sizes: Counter[str] = Counter()
    unique: set[str] = set()
    for ordinal, row in c15.rows():
        require(row.get("schema") == C15_ROW_TYPE
                and row.get("member_ordinal") == ordinal,
                f"C15 schema/ordinal:{ordinal}")
        member = row.get("registry_member_id")
        component = row.get("fresh_component_id")
        require(type(member) is str and member and member not in unique,
                f"C15 unique member:{ordinal}")
        require(type(component) is str and component != "",
                f"C15 component:{ordinal}")
        unique.add(member)
        members.append((member, component))
        sizes[component] += 1
    components = sorted(sizes)
    require(len(members) == COUNTS["members"]
            and len(components) == COUNTS["old"], "C15 exact census")
    return members, components, sizes


def rebuild_edges(edge: FileView, components: list[str]) -> tuple[UnionFind, int,
                                                                   int, str]:
    union = UnionFind(components)
    prior: str | None = None
    pairs: set[tuple[str, str]] = set()
    hashes: list[str] = []
    merges = cycles = 0
    for ordinal, row in edge.rows():
        require(row.get("schema") == EDGE_ROW_TYPE
                and row.get("ordinal") == ordinal,
                f"edge schema/ordinal:{ordinal}")
        key = row.get("component_edge_key")
        pair = row.get("ordered_C15_component_pair")
        require(type(key) is str and (prior is None or prior < key),
                f"edge strict key order:{ordinal}")
        prior = key
        require(type(pair) is list and len(pair) == 2
                and all(type(item) is str for item in pair)
                and pair[0] < pair[1] and tuple(pair) not in pairs,
                f"edge ordered unique pair:{ordinal}")
        pairs.add(tuple(pair))
        require(key == EDGE_KEY_PREFIX + object_hash(pair),
                f"edge key formula:{ordinal}")
        require(row.get("formal_credit") == 0
                and type(row.get("supporting_physical_proof_row_count")) is int
                and row["supporting_physical_proof_row_count"] > 0
                and valid_hash(
                    row.get("supporting_physical_proof_row_sequence_sha256")
                ), f"edge proof closure:{ordinal}")
        if union.join(pair[0], pair[1]):
            merges += 1
        else:
            cycles += 1
        hashes.append(row["row_sha256"])
    require(len(hashes) == COUNTS["edges"] and merges == COUNTS["merges"]
            and cycles == COUNTS["cycles"]
            and union.merge_count == COUNTS["merges"], "edge/DSU census")
    return union, merges, cycles, hash_sequence(hashes)


def canonical_quotient(
    union: UnionFind, old_sizes: Counter[str]
) -> tuple[dict[str, str], dict[str, dict[str, Any]], int]:
    old_to_post: dict[str, str] = {}
    census: dict[str, dict[str, Any]] = {}
    within = 0
    for group in union.partitions():
        post = POST_KEY_PREFIX + object_hash(group)
        require(post not in census, "canonical post ID collision")
        members = sum(old_sizes[old] for old in group)
        pairs = members * (members - 1) // 2
        census[post] = {
            "old_component_ids": group,
            "old_component_ids_sha256": hash_sequence(group),
            "old_component_count": len(group),
            "member_count": members,
            "within_member_pair_count": pairs,
        }
        within += pairs
        for old in group:
            require(old not in old_to_post, "old component exactly once")
            old_to_post[old] = post
    require(len(old_to_post) == COUNTS["old"]
            and len(census) == COUNTS["post"]
            and within == COUNTS["within"], "quotient exact census")
    return old_to_post, census, within


def descriptor_contract(
    descriptor: Any,
    view: FileView,
    expected_rows: int,
    row_type: str,
    ordering: list[str],
    unique_key: str,
    sequence_hash: str,
) -> None:
    require(type(descriptor) is dict, view.label + ":descriptor-object")
    expected = {
        "filename": view.path.name,
        "sha256": view.sha256,
        "size": view.initial.st_size,
        "row_count": expected_rows,
        "row_schema": row_type,
        "ordering": ordering,
        "unique_key": unique_key,
        "row_sequence_sha256": sequence_hash,
        "gzip_mtime": 0,
        "canonical_jsonl": True,
        "row_closure": "row_sha256=SHA256(canonical row without row_sha256)",
    }
    require(descriptor == expected, view.label + ":exact-descriptor")
    header = view.read()[:10]
    require(len(header) == 10 and header[:2] == b"\x1f\x8b"
            and header[4:8] == b"\x00\x00\x00\x00",
            view.label + ":deterministic-gzip-header")


def source_has_no_producer_import() -> str:
    source = THIS_FILE.read_text("utf-8")
    tree = ast.parse(source, filename=str(THIS_FILE))
    forbidden = PRODUCER_BASENAME.removesuffix(".py")
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            require(all(alias.name != forbidden for alias in node.names),
                    "verifier imports producer")
        if isinstance(node, ast.ImportFrom):
            require(node.module != forbidden, "verifier imports producer")
    return hashlib.sha256(THIS_FILE.read_bytes()).hexdigest()


def verify(args: argparse.Namespace) -> dict[str, Any]:
    candidate_dir = workspace_path(args.candidate_dir)
    output = workspace_path(args.out_file, absent_allowed=True)
    require(candidate_dir.is_dir() and not output.exists(),
            "candidate directory/fresh verification output")
    require(output.parent.is_dir() and output.parent != candidate_dir,
            "verification output outside candidate directory")
    names = {entry.name for entry in candidate_dir.iterdir()}
    require(names == set(FILES.values()), "candidate exact four-file inventory")

    result_view = FileView(candidate_dir / FILES["result"], "candidate-result")
    old_view = FileView(candidate_dir / FILES["old"], "candidate-old-map")
    member_view = FileView(candidate_dir / FILES["member"],
                           "candidate-member-map")
    census_view = FileView(candidate_dir / FILES["census"],
                           "candidate-post-census")
    candidate_views = [result_view, old_view, member_view, census_view]
    authority_views: list[FileView] = []
    try:
        result = result_view.document("result_sha256")
        require(
            result.get("schema") == PRODUCER_RESULT_TYPE
            and result.get("status")
                == "PASS_FRESH_ACTUAL_V2_SEED1_QUOTIENT_REBUILD_"
                   "ZERO_CREDIT__PENDING_NO_IMPORT_SEED2_VERIFICATION_"
                   "ATTACKS_COLD_REPLAY_AND_TERMINAL_SEAL"
            and result.get("formal_credit") == 0
            and result.get("manifest_authorized") is False
            and result.get("C27R2")
                == "UNAUTHORIZED_PENDING_INDEPENDENT_VERIFICATION_AND_TERMINAL_SEAL"
            and result.get("C28_C29") == "UNAUTHORIZED"
            and result.get("Source_W")
                == "UNCHANGED_BY_SOURCE_G_REBUILD_CANDIDATE"
            and result.get("CM2") == "NO-GO_FOR_CLAIM",
            "candidate result zero-credit semantic contract",
        )
        producer_path = workspace_path(
            result.get("producer_source_attestation", {}).get("path", "")
        )
        require(producer_path.name == PRODUCER_BASENAME,
                "candidate producer source basename")
        producer_view = FileView(producer_path, "producer-source")
        candidate_views.append(producer_view)
        require(producer_view.sha256 == result.get("producer_source_sha256")
                == result["producer_source_attestation"].get("sha256"),
                "candidate producer source current pin")

        terminal, base, seed2_edge, c15, authority_views = authority(
            args.terminal_dir, args.base_seal_dir,
            args.expect_terminal_root_sha256,
            args.expect_terminal_receipt_file_sha256,
            args.expect_terminal_receipt_object_sha256,
        )
        result_authority = result.get("authority")
        base_inputs = base["root_input_capture"]["attestations"]
        seed1_claim = base_inputs["seed1_full_component_edge_union"]
        require(type(result_authority) is dict
                and result_authority.get("actual_v2_terminal_root_manifest_sha256")
                    == args.expect_terminal_root_sha256
                and result_authority.get("actual_v2_terminal_receipt_file_sha256")
                    == args.expect_terminal_receipt_file_sha256
                and result_authority.get("actual_v2_terminal_receipt_object_sha256")
                    == args.expect_terminal_receipt_object_sha256
                and result_authority.get("actual_v2_base_seal_receipt_file_sha256")
                    == terminal["base_seal"]["receipt_file_sha256"]
                and result_authority.get("actual_v2_base_seal_receipt_object_sha256")
                    == terminal["base_seal"]["receipt_object_sha256"]
                and result_authority.get("actual_v2_seed_label") == "seed1"
                and result_authority.get("actual_v2_execution_seed")
                    == terminal["execution_seeds"][0]
                and result_authority.get("actual_v2_edge_ledger_path")
                    == seed1_claim["path"]
                and result_authority.get("actual_v2_edge_ledger_sha256")
                    == seed1_claim["sha256"] == seed2_edge.sha256
                and result_authority.get("frozen_C15_path") == C15_REL
                and result_authority.get("frozen_C15_sha256") == C15_HASH,
                "candidate seed1 authority versus independent seed2")
        claimed_inputs = result.get("input_pre_post_attestations")
        require(type(claimed_inputs) is dict and set(claimed_inputs) == {
            "terminal-root", "terminal-payload", "terminal-receipt",
            "base-root", "base-payload", "base-receipt", "seed1-edge",
            "frozen-C15",
        }, "candidate exact producer input-attestation inventory")
        current_shared = {
            view.label: view.attest() for view in authority_views
            if view.label not in {"seed2-edge"}
        }
        for label in (
            "terminal-root", "terminal-payload", "terminal-receipt",
            "base-root", "base-payload", "base-receipt", "frozen-C15",
        ):
            require(claimed_inputs[label] == current_shared[label],
                    "candidate producer input current pre/post attestation:" + label)
        seed1_input = claimed_inputs["seed1-edge"]
        require(type(seed1_input) is dict
                and seed1_input.get("path") == seed1_claim["path"]
                and seed1_input.get("sha256") == seed1_claim["sha256"]
                and seed1_input.get("size") == seed1_claim["size"]
                and seed1_input.get("O_NOFOLLOW") is True
                and seed1_input.get(
                    "single_open_file_description_hash_parse_fstat") is True
                and type(seed1_input.get("stat_fingerprint")) is list
                and len(seed1_input["stat_fingerprint"]) == 9,
                "candidate seed1 edge producer input attestation")

        members, components, old_sizes = frozen_partition(c15)
        union, merges, cycles, edge_sequence = rebuild_edges(seed2_edge, components)
        old_to_post, expected_census, within = canonical_quotient(union, old_sizes)
        all_pairs = len(members) * (len(members) - 1) // 2
        cross = all_pairs - within
        require((all_pairs, within, cross)
                == (COUNTS["all_pairs"], COUNTS["within"], COUNTS["cross"]),
                "independent pair identity")
        require(result.get("edge_row_sequence_sha256") == edge_sequence,
                "candidate/seed2 edge sequence")
        require(result.get("canonical_post_component_id_formula")
                == POST_KEY_PREFIX
                   + "SHA256(canonical JSON sorted list of old C15 component IDs)",
                "canonical post ID formula declaration")
        require(result.get("exact_census") == {
            "frozen_C15_members": COUNTS["members"],
            "frozen_C15_components": COUNTS["old"],
            "proof_derived_component_edges": COUNTS["edges"],
            "successful_DSU_merges": merges,
            "cycle_edges": cycles,
            "post_C27R2_components": COUNTS["post"],
            "total_unordered_member_pairs": all_pairs,
            "within_post_component_member_pairs": within,
            "cross_post_component_member_pairs": cross,
        }, "candidate exact census")
        require(result.get("derivation_closures") == {
            "DSU_started_from_all_57876_frozen_C15_components": True,
            "only_terminal_pinned_actual_v2_seed1_edges_applied": True,
            "post_component_ID_never_uses_DSU_root": True,
            "all_502204_members_rebound_through_frozen_C15": True,
            "pair_identity_total_equals_within_plus_cross": True,
            "old_C27_C28_C29_partition_imported_or_read": False,
        }, "candidate derivation declarations")

        old_sequence = hashlib.sha256()
        rows = iter(old_view.rows())
        for ordinal, old in enumerate(components):
            observed_ordinal, observed = next(rows, (-1, {}))
            post = old_to_post[old]
            group = expected_census[post]
            expected = row_close({
                "schema": OLD_MAP_TYPE,
                "ordinal": ordinal,
                "old_C15_component_id": old,
                "post_C27R2_component_id": post,
                "post_C27R2_old_component_count":
                    group["old_component_count"],
                "post_C27R2_old_component_ids_sha256":
                    group["old_component_ids_sha256"],
                "formal_credit": 0,
            })
            require(observed_ordinal == ordinal and observed == expected,
                    f"old-map exact row:{ordinal}")
            old_sequence.update(observed["row_sha256"].encode("ascii") + b"\n")
        require(next(rows, None) is None, "old-map exact EOF")

        member_sequence = hashlib.sha256()
        rows = iter(member_view.rows())
        for ordinal, (member, old) in enumerate(members):
            observed_ordinal, observed = next(rows, (-1, {}))
            expected = row_close({
                "schema": MEMBER_MAP_TYPE,
                "ordinal": ordinal,
                "member_ordinal": ordinal,
                "registry_member_id": member,
                "old_C15_component_id": old,
                "post_C27R2_component_id": old_to_post[old],
                "formal_credit": 0,
            })
            require(observed_ordinal == ordinal and observed == expected,
                    f"member-map exact row:{ordinal}")
            member_sequence.update(
                observed["row_sha256"].encode("ascii") + b"\n")
        require(next(rows, None) is None, "member-map exact EOF")

        census_sequence = hashlib.sha256()
        rows = iter(census_view.rows())
        for ordinal, post in enumerate(sorted(expected_census)):
            observed_ordinal, observed = next(rows, (-1, {}))
            group = expected_census[post]
            expected = row_close({
                "schema": POST_CENSUS_TYPE,
                "ordinal": ordinal,
                "post_C27R2_component_id": post,
                "old_C15_component_count": group["old_component_count"],
                "old_C15_component_ids_sha256":
                    group["old_component_ids_sha256"],
                "member_count": group["member_count"],
                "within_member_pair_count": group["within_member_pair_count"],
                "formal_credit": 0,
            })
            require(observed_ordinal == ordinal and observed == expected,
                    f"post-census exact row:{ordinal}")
            census_sequence.update(
                observed["row_sha256"].encode("ascii") + b"\n")
        require(next(rows, None) is None, "post-census exact EOF")

        ledgers = result.get("ledgers")
        require(type(ledgers) is dict and set(ledgers) == {
            "old_C15_component_to_post_component", "member_to_post_component",
            "post_component_census",
        }, "candidate ledger descriptor inventory")
        descriptor_contract(
            ledgers["old_C15_component_to_post_component"], old_view,
            COUNTS["old"], OLD_MAP_TYPE, ["old_C15_component_id"],
            "old_C15_component_id", old_sequence.hexdigest(),
        )
        descriptor_contract(
            ledgers["member_to_post_component"], member_view,
            COUNTS["members"], MEMBER_MAP_TYPE, ["member_ordinal"],
            "registry_member_id", member_sequence.hexdigest(),
        )
        descriptor_contract(
            ledgers["post_component_census"], census_view,
            COUNTS["post"], POST_CENSUS_TYPE,
            ["post_C27R2_component_id"], "post_C27R2_component_id",
            census_sequence.hexdigest(),
        )
        verifier_sha = source_has_no_producer_import()
        candidate_attestations = {
            view.label: view.attest() for view in candidate_views
        }
        authority_attestations = {
            view.label: view.attest() for view in authority_views
        }
        projection = {
            "terminal_receipt_object_sha256": terminal_object_pin(args),
            "seed1_edge_sha256": seed1_claim["sha256"],
            "seed2_edge_sha256": seed2_edge.sha256,
            "C15_sha256": C15_HASH,
            "old_components": COUNTS["old"],
            "edges": COUNTS["edges"],
            "merges": merges,
            "cycles": cycles,
            "post_components": COUNTS["post"],
            "members": COUNTS["members"],
            "within_pairs": within,
            "cross_pairs": cross,
            "candidate_result_object_sha256": result["result_sha256"],
        }
        body = {
            "schema": VERIFICATION_TYPE,
            "status": (
                "PASS_NO_IMPORT_ACTUAL_V2_SEED2_INDEPENDENT_QUOTIENT_AND_"
                "BYTE_EXACT_CANDIDATE_REPLAY__ZERO_CREDIT_PENDING_ATTACKS_"
                "COLD_REPLAY_AND_TERMINAL_SEAL"
            ),
            "independent_verifier_source_sha256": verifier_sha,
            "producer_imported_or_executed": False,
            "actual_v2_seed_used": "seed2",
            "actual_v2_execution_seed": terminal["execution_seeds"][1],
            "candidate_result_file_sha256": result_view.sha256,
            "candidate_result_object_sha256": result["result_sha256"],
            "mathematical_projection": projection,
            "mathematical_projection_sha256": object_hash(projection),
            "candidate_attestations": candidate_attestations,
            "authority_attestations": authority_attestations,
            "exact_checks": {
                "seed1_and_seed2_edge_ledgers_byte_identical": True,
                "fresh_DSU_rebuilt_without_producer_import": True,
                "canonical_post_IDs_rederived_from_sorted_old_component_sets": True,
                "all_three_candidate_ledgers_byte_semantically_exact": True,
                "all_gzip_canonical_order_count_row_closures_pass": True,
                "pair_identity_126104177706_equals_542179508_plus_125561998198": True,
            },
            "formal_credit": 0,
            "manifest_authorized": False,
            "C27R2": "UNAUTHORIZED_PENDING_ATTACKS_COLD_REPLAY_AND_TERMINAL_SEAL",
            "C28_C29": "UNAUTHORIZED",
            "Source_W": "UNCHANGED",
            "CM2": "NO-GO_FOR_CLAIM",
        }
        verification = dict(body)
        verification["verification_sha256"] = object_hash(verification)
        write_once(output, wire(verification) + b"\n")
        return verification
    finally:
        for view in candidate_views:
            view.close()
        for view in authority_views:
            view.close()


def terminal_object_pin(args: argparse.Namespace) -> str:
    return args.expect_terminal_receipt_object_sha256


def write_once(path: Path, payload: bytes) -> None:
    descriptor = os.open(
        path,
        os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, "O_NOFOLLOW", 0),
        0o600,
    )
    try:
        written = 0
        while written < len(payload):
            written += os.write(descriptor, payload[written:])
        os.fsync(descriptor)
    finally:
        os.close(descriptor)


def self_test() -> dict[str, Any]:
    components = ["x0", "x1", "x2", "x3"]
    union = UnionFind(components)
    outcomes = [union.join("x0", "x1"), union.join("x1", "x2"),
                union.join("x0", "x2")]
    require(outcomes == [True, True, False], "fixture merge/cycle")
    require(union.partitions() == [["x0", "x1", "x2"], ["x3"]],
            "fixture partitions")
    sizes = Counter({"x0": 1, "x1": 2, "x2": 1, "x3": 2})
    old, census, within = quotient_fixture(union, sizes)
    require(len(old) == 4 and len(census) == 2 and within == 7,
            "fixture quotient/pairs")
    require(old["x0"]
            == POST_KEY_PREFIX + object_hash(["x0", "x1", "x2"]),
            "fixture canonical post ID")
    require(source_has_no_producer_import() == hashlib.sha256(
        THIS_FILE.read_bytes()).hexdigest(), "fixture no producer import")
    with tempfile.TemporaryDirectory(prefix="cm2-c27r2-v2-verifier-selftest-"):
        pass
    return {
        "schema": VERIFICATION_TYPE + ".self-test",
        "status": "PASS_NO_IMPORT_SMALL_FIXTURE_DSU_CANONICAL_ID_AND_PAIR_TESTS",
        "fixture_within_pairs": within,
        "formal_credit": 0,
        "CM2": "NO-GO_FOR_CLAIM",
    }


def quotient_fixture(
    union: UnionFind, sizes: Counter[str]
) -> tuple[dict[str, str], dict[str, dict[str, Any]], int]:
    old: dict[str, str] = {}
    census: dict[str, dict[str, Any]] = {}
    within = 0
    for group in union.partitions():
        post = POST_KEY_PREFIX + object_hash(group)
        members = sum(sizes[item] for item in group)
        pairs = members * (members - 1) // 2
        census[post] = {
            "old_component_ids": group,
            "old_component_ids_sha256": hash_sequence(group),
            "old_component_count": len(group),
            "member_count": members,
            "within_member_pair_count": pairs,
        }
        within += pairs
        for item in group:
            old[item] = post
    return old, census, within


def arguments() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--terminal-dir")
    parser.add_argument("--base-seal-dir")
    parser.add_argument("--expect-terminal-root-sha256")
    parser.add_argument("--expect-terminal-receipt-file-sha256")
    parser.add_argument("--expect-terminal-receipt-object-sha256")
    parser.add_argument("--candidate-dir")
    parser.add_argument("--out-file")
    return parser


def main() -> int:
    args = arguments().parse_args()
    try:
        fields = (
            "terminal_dir", "base_seal_dir", "expect_terminal_root_sha256",
            "expect_terminal_receipt_file_sha256",
            "expect_terminal_receipt_object_sha256", "candidate_dir", "out_file",
        )
        if args.self_test:
            require(all(getattr(args, field) is None for field in fields),
                    "self-test accepts no authority/candidate arguments")
            result = self_test()
        else:
            require(all(getattr(args, field) is not None for field in fields),
                    "all authority pins, candidate and output are required")
            result = verify(args)
        sys.stdout.buffer.write(wire({
            "status": result["status"], "formal_credit": 0,
            "CM2": "NO-GO_FOR_CLAIM",
        }) + b"\n")
        return 0
    except (Reject, OSError, ValueError, KeyError, TypeError) as error:
        sys.stderr.write("REJECT:" + str(error) + "\n")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())


