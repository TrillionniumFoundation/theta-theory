#!/usr/bin/env python3
from __future__ import annotations

import argparse
from collections import defaultdict
import gzip
import hashlib
import io
import json
import os
from pathlib import Path
import sys
from typing import Any, Final

ROOT: Final = Path(__file__).resolve().parent
PREFIX: Final = "cm2_round306c15_source_g_502204_member_fresh_dsu_freeze"
SCHEMA: Final = "cm2.round306c15.source-g-502204-member-fresh-dsu-freeze.v1"
EDGES: Final = PREFIX + "_edge_application_ledger.jsonl.gz"
MEMBERS: Final = PREFIX + "_member_component_ledger.jsonl.gz"
ROOTS: Final = PREFIX + "_base_root_component_ledger.jsonl.gz"
COMPONENTS: Final = PREFIX + "_component_census_ledger.jsonl.gz"
CROSS: Final = PREFIX + "_cross_component_pair_denominator.json"
RESULT: Final = PREFIX + "_result.json"
COMPONENT_NS: Final = "round306c15-source-g-component:"

PINS: Final = {
    "C6_RESULT": ("cm2_round306c6_source_g_corrected_g2_invalidation_fresh_dsu_freeze_result.json", 9329, "3f4e3e666dfe0b5b3a163c866057031b42dac09000175f4bc0b32ec353c5e4c5"),
    "C6_MEMBER": ("cm2_round306c6_source_g_corrected_g2_invalidation_fresh_dsu_freeze_member_component_ledger.jsonl.gz", 213125489, "730a1501402d29f9689655b0093edd4d7e499f3a34c6b65e9f21ee6f3f5ffce2"),
    "C6_EDGE": ("cm2_round306c6_source_g_corrected_g2_invalidation_fresh_dsu_freeze_edge_application_ledger.jsonl.gz", 161025678, "9d0421e5e01a14b67a005894ce6b73b3abe2443d95a9194ca52b55d6314554cb"),
    "C14C_RESULT": ("cm2_round306c14c_source_g_registry_official_key_family_and_self_root_admission_result.json", 4684, "9484448678ae157ab7fb9f061cf4fd986bc269d535a98651f5e4e4fb5c9f8e98"),
    "C14C_ADMISSION": ("cm2_round306c14c_source_g_registry_official_key_family_and_self_root_admission_new_exact_sheet_admission_ledger.jsonl.gz", 2526805, "7f65ab28ad43a762d1e02bbd9d869965950b7b6d6db9cceef3fdd8cef12cc205"),
    "C14D_RESULT": ("cm2_round306c14d_source_g_exact_sheet_to_side_edge_promotion_result.json", 3569, "8e9b32e74f38bbadf76f98f7133dae8de636d9b3d166b93a3cf9531160c2c633"),
    "C14D_EDGE": ("cm2_round306c14d_source_g_exact_sheet_to_side_edge_promotion_edge_promotion_ledger.jsonl.gz", 5096928, "8acbee74732ad2e1ee21726053c35e136e563ca34620e8f0c8adad01c0e27655"),
}


class Blocked(RuntimeError): pass


def need(value: bool, label: str) -> None:
    if type(value) is not bool or not value: raise Blocked(label)


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True, allow_nan=False).encode("ascii")


def obj(value: Any) -> str: return hashlib.sha256(canonical(value)).hexdigest()


def fsha(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while block := stream.read(1048576): digest.update(block)
    return digest.hexdigest()


def check_pins() -> None:
    for role, (name, size, sha) in PINS.items():
        path = ROOT / name
        info = path.stat()
        need(path.is_file() and not path.is_symlink() and info.st_nlink == 1 and info.st_size == size, "pin identity:" + role)
        need(fsha(path) == sha, "pin digest:" + role)


def rows(role: str):
    name = PINS[role][0]
    with gzip.open(ROOT / name, "rb") as stream:
        for ordinal, line in enumerate(stream):
            need(line.endswith(b"\n"), "row newline:" + role)
            raw = line[:-1]
            row = json.loads(raw)
            need(canonical(row) == raw, "canonical row:" + role)
            body = dict(row)
            need(body.pop("row_sha256", None) == obj(body), "row closure:" + role)
            yield ordinal, row, hashlib.sha256(raw).hexdigest()


class DSU:
    def __init__(self, items: set[str]):
        self.items = sorted(items); self.index = {item: i for i, item in enumerate(self.items)}
        self.parent = list(range(len(self.items))); self.size = [1] * len(self.items); self.reduction = 0
    def find(self, item: int) -> int:
        while self.parent[item] != item:
            self.parent[item] = self.parent[self.parent[item]]; item = self.parent[item]
        return item
    def union(self, left: str, right: str) -> int:
        a = self.find(self.index[left]); b = self.find(self.index[right])
        if a == b: return 0
        if self.size[a] < self.size[b] or (self.size[a] == self.size[b] and self.items[a] > self.items[b]): a, b = b, a
        self.parent[b] = a; self.size[a] += self.size[b]; self.reduction += 1; return 1
    def partition(self) -> list[list[str]]:
        groups: dict[int, list[str]] = defaultdict(list)
        for ordinal, item in enumerate(self.items): groups[self.find(ordinal)].append(item)
        return sorted(sorted(group) for group in groups.values())


def close_row(body: dict[str, Any]) -> bytes:
    row = {**body, "row_sha256": obj(body)}
    return canonical(row) + b"\n"


def gzip_bytes(lines: list[bytes]) -> bytes:
    target = io.BytesIO()
    with gzip.GzipFile(fileobj=target, mode="wb", compresslevel=9, mtime=0) as stream:
        for line in lines: stream.write(line)
    return target.getvalue()


def write(directory: Path, name: str, data: bytes) -> dict[str, Any]:
    path = directory / name
    need(not path.exists(), "no clobber:" + name)
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600)
    try:
        offset = 0
        while offset < len(data): offset += os.write(fd, data[offset:])
        os.fsync(fd)
    finally: os.close(fd)
    return {"filename": name, "size": len(data), "sha256": hashlib.sha256(data).hexdigest()}


def build() -> tuple[dict[str, Any], dict[str, bytes]]:
    check_pins()
    c6_result = json.loads((ROOT / PINS["C6_RESULT"][0]).read_bytes())
    c14c_result = json.loads((ROOT / PINS["C14C_RESULT"][0]).read_bytes())
    c14d_result = json.loads((ROOT / PINS["C14D_RESULT"][0]).read_bytes())
    need(c6_result["fresh_freeze_census"]["members"] == 497772, "C6 member census")
    need(c14c_result["formal_credit"]["new_registry_member_admission"] == 4432, "C14c admission census")
    need(c14d_result["formal_edge_authority_census"]["promoted_edges"] == 8864, "C14d edge census")

    member_source: dict[str, dict[str, Any]] = {}
    root_member_count: dict[str, int] = defaultdict(int)
    root_key: dict[str, str] = {}
    for ordinal, row, wire_sha in rows("C6_MEMBER"):
        member = row["registry_member_id"]; root = row["new_base_root_id"]
        need(member not in member_source, "C6 duplicate member")
        member_source[member] = {"root": root, "key": row["official_key_id"], "ref": [ordinal, row["row_id"], wire_sha, row["row_sha256"]], "source": "C6_RETAINED"}
        root_member_count[root] += 1
        observed = root_key.setdefault(root, row["official_key_id"]); need(observed == row["official_key_id"], "C6 root key")
    need(len(member_source) == 497772 and len(root_member_count) == 334604, "C6 exhaustion")

    admissions = 0
    for ordinal, row, wire_sha in rows("C14C_ADMISSION"):
        member = row["new_exact_sheet_member_id"]; root = row["self_base_root_id"]
        need(member not in member_source and root not in root_member_count, "new collision")
        need(row["registry_member_admission_credit"] == row["self_root_authority_credit"] == 1, "admission credit")
        member_source[member] = {"root": root, "key": row["official_key_id"], "ref": [ordinal, row["row_id"], wire_sha, row["row_sha256"]], "source": "C14C_NEW_EXACT_SHEET"}
        root_member_count[root] = 1; root_key[root] = row["official_key_id"]; admissions += 1
    need(admissions == 4432 and len(member_source) == 502204 and len(root_member_count) == 339036, "new universe census")

    edge_sources: list[dict[str, Any]] = []
    old_kept = 0
    for ordinal, row, wire_sha in rows("C6_EDGE"):
        if not row["fed_to_new_empty_DSU"]: continue
        pair = row["new_projected_base_root_pair"]
        need(pair == sorted(pair) and all(root in root_member_count for root in pair), "C6 edge roots")
        edge_sources.append({"channel": "C6_RETAINED", "pair": pair, "source_ordinal": ordinal, "source_row_id": row["row_id"], "source_wire_sha256": wire_sha, "source_row_sha256": row["row_sha256"]})
        old_kept += 1
    need(old_kept == 476118, "C6 retained edges")
    new_edges = 0
    for ordinal, row, wire_sha in rows("C14D_EDGE"):
        pair = row["projected_base_root_pair"]
        need(pair == sorted(pair) and all(root in root_member_count for root in pair), "C14d edge roots")
        need(row["edge_promotion_credit"] == 1, "C14d edge credit")
        edge_sources.append({"channel": "C14D_NEW_EXACT_SHEET_TO_SIDE", "pair": pair, "source_ordinal": ordinal, "source_row_id": row["row_id"], "source_wire_sha256": wire_sha, "source_row_sha256": row["row_sha256"]})
        new_edges += 1
    need(new_edges == 8864 and len(edge_sources) == 484982, "edge exhaustion")

    roots = set(root_member_count)
    forward = DSU(roots); forward_flags = [forward.union(*edge["pair"]) for edge in edge_sources]
    reverse = DSU(roots); reverse_flags = [0] * len(edge_sources)
    for ordinal in range(len(edge_sources) - 1, -1, -1): reverse_flags[ordinal] = reverse.union(*edge_sources[ordinal]["pair"])
    forward_partition = forward.partition(); reverse_partition = reverse.partition()
    need(forward_partition == reverse_partition, "forward reverse partition")
    need(forward.reduction == reverse.reduction == 281160 and len(forward_partition) == 57876, "DSU census")

    component_by_root: dict[str, str] = {}; roots_by_component: dict[str, list[str]] = {}
    for component_roots in forward_partition:
        component = COMPONENT_NS + obj(component_roots); roots_by_component[component] = component_roots
        for root in component_roots: component_by_root[root] = component
    component_members = {component: sum(root_member_count[root] for root in component_roots) for component, component_roots in roots_by_component.items()}
    sizes = sorted(component_members.values()); all_pairs = 502204 * 502203 // 2
    within = sum(size * (size - 1) // 2 for size in sizes); cross = all_pairs - within
    need(cross == 125616475670, "cross denominator")

    edge_lines: list[bytes] = []
    for ordinal, source in enumerate(edge_sources):
        body = {"schema": SCHEMA + ".edge-application-row.v1", "row_id": PREFIX + ":edge-application:" + obj([ordinal, source["source_row_id"]]), "application_ordinal": ordinal, **source, "fed_to_fresh_empty_DSU": True, "forward_rank_reduction": forward_flags[ordinal], "reverse_rank_reduction": reverse_flags[ordinal], "fresh_DSU_edge_application_credit": 1}
        edge_lines.append(close_row(body))

    member_lines: list[bytes] = []
    for ordinal, member in enumerate(sorted(member_source)):
        source = member_source[member]; root = source["root"]
        body = {"schema": SCHEMA + ".member-component-row.v1", "row_id": PREFIX + ":member-component:" + obj(member), "member_ordinal": ordinal, "registry_member_id": member, "base_root_id": root, "fresh_component_id": component_by_root[root], "official_key_id": source["key"], "admission_source": source["source"], "source_row_ref": source["ref"], "fresh_member_and_component_credit": 1}
        member_lines.append(close_row(body))

    root_lines: list[bytes] = []
    for ordinal, root in enumerate(sorted(roots)):
        body = {"schema": SCHEMA + ".base-root-component-row.v1", "row_id": PREFIX + ":base-root-component:" + obj(root), "base_root_ordinal": ordinal, "base_root_id": root, "fresh_component_id": component_by_root[root], "official_key_id": root_key[root], "member_count": root_member_count[root], "fresh_root_component_credit": 1}
        root_lines.append(close_row(body))

    component_lines: list[bytes] = []
    for ordinal, component in enumerate(sorted(roots_by_component)):
        component_roots = roots_by_component[component]
        body = {"schema": SCHEMA + ".component-census-row.v1", "row_id": PREFIX + ":component-census:" + obj(component), "component_ordinal": ordinal, "fresh_component_id": component, "base_root_count": len(component_roots), "base_root_ids_sha256": obj(component_roots), "member_count": component_members[component], "fresh_component_credit": 1}
        component_lines.append(close_row(body))

    cross_body = {"schema": SCHEMA + ".cross-component-pair-denominator.v1", "members": 502204, "components": 57876, "all_unordered_member_pairs": all_pairs, "within_component_unordered_member_pairs": within, "cross_component_pair_denominator": cross, "component_member_size_vector_sha256": obj(sizes)}
    cross_object = {**cross_body, "cross_denominator_sha256": obj(cross_body)}
    outputs = {EDGES: gzip_bytes(edge_lines), MEMBERS: gzip_bytes(member_lines), ROOTS: gzip_bytes(root_lines), COMPONENTS: gzip_bytes(component_lines), CROSS: canonical(cross_object)}
    descriptors = {name: {"filename": name, "size": len(data), "sha256": hashlib.sha256(data).hexdigest()} for name, data in outputs.items()}
    body = {"schema": SCHEMA, "status": "PASS_502204_MEMBER_484982_EDGE_FRESH_DSU_SEALED__C7_C14_REPLAY_REQUIRED", "source_pins": [{"role": role, "filename": value[0], "size": value[1], "sha256": value[2]} for role, value in PINS.items()], "fresh_universe_census": {"members": 502204, "base_roots": 339036, "old_C6_members": 497772, "new_C14c_members": 4432}, "edge_application_census": {"applied_edges": 484982, "old_C6_retained_edges": 476118, "new_C14d_edges": 8864, "forward_rank_reduction": 281160, "reverse_rank_reduction": 281160}, "fresh_DSU_census": {"components": 57876, "partition_sha256": obj(forward_partition), "component_member_size_vector_sha256": obj(sizes), "cross_component_pair_denominator": cross}, "output_files": descriptors, "formal_credit": {"fresh_member_universe": 502204, "fresh_base_roots": 339036, "fresh_edge_applications": 484982, "fresh_components": 57876, "cross_denominator": cross}, "strict_invalidation": {"all_pre_C15_component_ids": "INVALIDATED", "C6_through_C14_component_bound_outputs": "REPLAY_REQUIRED"}, "strict_nonpromotion": {"representation_pullback": 0, "normalized_support": 0, "B1A": 0, "B2": 0, "maximality": 0, "CM2": "NO-GO_FOR_CLAIM"}, "required_next": "FULL_C7_THROUGH_C14_REPLAY_ON_C15_COMPONENT_IDS"}
    result = {**body, "result_sha256": obj(body)}; outputs[RESULT] = canonical(result)
    return result, outputs


def main() -> int:
    need(sys.flags.isolated == 1 and sys.dont_write_bytecode is True, "python -I -B")
    parser = argparse.ArgumentParser(); parser.add_argument("--candidate-dir"); parser.add_argument("--publish", action="store_true")
    args = parser.parse_args(); need((args.candidate_dir is not None) != args.publish, "one mode")
    directory = ROOT if args.publish else Path(args.candidate_dir).resolve()
    if not args.publish: directory.mkdir(mode=0o700, parents=False, exist_ok=False)
    result, outputs = build()
    for name in (EDGES, MEMBERS, ROOTS, COMPONENTS, CROSS, RESULT): write(directory, name, outputs[name])
    print(json.dumps({"status": result["status"], "result_sha256": result["result_sha256"]}, sort_keys=True, separators=(",", ":")))
    return 0


if __name__ == "__main__": raise SystemExit(main())
