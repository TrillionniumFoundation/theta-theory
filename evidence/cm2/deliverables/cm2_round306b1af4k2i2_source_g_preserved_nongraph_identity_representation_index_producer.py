#!/usr/bin/env python3
"""K2I2 preserved/non-graph mechanical identity/representation index.

This is a partial engineering lane.  It replays the statically pinned P1 raw
join implementation from its held source bytes, then emits deterministic
member and representation handles for the 126,468 preserved and 17,828
non-graph members.  Reusing P1 is disclosed and receives no independent
mathematical credit.  In particular, identity joins, boxes, aliases, or
outer envelopes do not become normalized full-support or representation-set
equality theorems here.
"""

from __future__ import annotations

import argparse
from collections import Counter
import gzip
import hashlib
import json
import os
from pathlib import Path
import re
import stat
import tempfile
import types
from typing import Any


class Blocked(RuntimeError):
    pass


def need(condition: bool, label: str) -> None:
    if not condition:
        raise Blocked(label)


PREFIX = "cm2_round306b1af4k2i2_source_g_preserved_nongraph_identity_representation_index_"
SCHEMA = "cm2.round306b1af4k2i2.source-g-preserved-nongraph-identity-representation-index.v1"
STATUS = "PASS_MECHANICAL_144296_MEMBER_183572_REPRESENTATION_INDEX__ZERO_THEOREM_CREDIT"
DELIVERABLES = Path(__file__).resolve().parent
HEX64 = re.compile(r"^[0-9a-f]{64}$")
MAX_ROW = 8 << 20

ANCHOR_PINS: tuple[tuple[str, str, int, str], ...] = (
    ("P1", "cm2_round306b1af4p1_source_g_preserved_non_graph_exact_join_preflight.py", 112_834, "34098cfd5c5e8d1ff73b4a172ecd0a1375a74a4e51a12c6e89b7984474062dfd"),
    ("K2P0_RESULT", "cm2_round306b1af4k2p0_preserved_nongraph_authority_frontier_result.json", 1_214, "8a32251023ec7c4a8b42d9affdac931376fd8e5f373e49503ce6272235493a93"),
    ("K2P0_LEDGER", "cm2_round306b1af4k2p0_preserved_nongraph_authority_frontier_ledger.json", 35_521, "e56a50b1ce88f0ae45eb09a194a15d3c26804c6e5baac803a1f5f4a19231ed3d"),
)

OUTPUTS = {
    "member": PREFIX + "member_index.jsonl.gz",
    "representation": PREFIX + "representation_index.jsonl.gz",
    "gap": PREFIX + "authority_gap_index.jsonl.gz",
    "result": PREFIX + "result.json",
}

PRESERVED_COUNTS = {
    "ROUND174_RESOLVED": 72_500,
    "ROUND179_RESOLVED": 17_192,
    "ROUND204_REGION": 736,
    "ROUND208_REGION": 36_040,
}
NON_GRAPH_COUNTS = {
    "R245_WHOLE_ROOT_ZERO_ABSENCE_BULK": 2_872,
    "R246_WHOLE_ORIGIN_SINGLE_SIGNATURE_RETAINED_BULK": 2_220,
    "R247_CROSSING_TIME_WHOLE_SIGNATURE_RETAINED_BULK": 240,
    "R247_SOURCE_CHART_SEAM_WHOLE_SIGNATURE_RETAINED_BULK": 264,
    "R248_ROUND234_RESOLVED_DESCENDANT": 12_200,
    "R248_ROUND236_CROSSING_DISCHARGE_BULK": 32,
}
ALIAS_KIND_COUNTS = {
    "EXACT_EQUAL_SUPPORT_ENVELOPE_ALIAS_EVIDENCE": 36_680,
    "EXACT_SAME_POSITIVE_OPEN_REGION_INCLUSION_SUBCOVER": 720,
    "EXACT_T2_P_S_EXISTING_OCCURRENCE_SUBCOVER_CELL": 1_600,
    "ADJACENT_POSITIVE_T_CONTINUATION": 276,
}

ZERO_CREDIT = {
    "normalized_support": 0,
    "representation_cover": 0,
    "A1_A2": 0,
    "B1A": 0,
    "B2": 0,
    "maximality": 0,
    "fibre": 0,
    "global_disposition": 0,
    "D02": 0,
    "D03": 0,
    "D04": 0,
    "Gate5": 0,
    "CM2": 0,
}


def canonical(value: Any) -> bytes:
    raw = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True, allow_nan=False).encode("ascii")
    need(len(raw) <= MAX_ROW, "canonical row cap")
    return raw


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for key, value in pairs:
        need(key not in out, "duplicate JSON key:" + key)
        out[key] = value
    return out


def reject_number(token: str) -> Any:
    raise Blocked("nonintegral/nonstandard JSON number:" + token)


def parse_json_bytes(raw: bytes) -> Any:
    need(len(raw) <= MAX_ROW, "small JSON byte cap")
    value = json.loads(raw, object_pairs_hook=unique_object, parse_float=reject_number, parse_constant=reject_number)
    canonical(value)
    return value


def fingerprint(value: os.stat_result) -> tuple[int, ...]:
    return (value.st_dev, value.st_ino, value.st_mode, value.st_nlink, value.st_size, value.st_mtime_ns, value.st_ctime_ns)


def dir_identity(value: os.stat_result) -> tuple[int, int, int]:
    return (value.st_dev, value.st_ino, value.st_mode)


def hash_fd(fd: int, cap: int) -> tuple[int, str]:
    state = hashlib.sha256()
    total = 0
    offset = 0
    while True:
        block = os.pread(fd, 1 << 20, offset)
        if not block:
            break
        total += len(block)
        offset += len(block)
        need(total <= cap, "held file grew")
        state.update(block)
    return total, state.hexdigest()


def closed(body: dict[str, Any]) -> dict[str, Any]:
    need("row_sha256" not in body, "row preclosed")
    return {**body, "row_sha256": digest(body)}


def r294_geometry_payload(row: dict[str, Any]) -> dict[str, Any]:
    """Return the complete type-specific R294 geometry payload.

    R294's TPS rows carry an exact support box, while T2PS rows carry a
    transformed open cell plus its coordinate system and exact volume.  The
    payload is deliberately tagged so the two encodings cannot collide.
    """
    kind = row["support_representation_kind"]
    common = {
        "support_representation_kind": kind,
        "physical_support_chart": row["physical_support_chart"],
    }
    if kind in (
        "EXACT_EQUAL_SUPPORT_ENVELOPE_ALIAS_EVIDENCE",
        "EXACT_SAME_POSITIVE_OPEN_REGION_INCLUSION_SUBCOVER",
    ):
        return {**common, "exact_support_representation_box": row["exact_support_representation_box"]}
    need(kind == "EXACT_T2_P_S_EXISTING_OCCURRENCE_SUBCOVER_CELL", "R294 geometry kind")
    return {
        **common,
        "exact_transformed_coordinate_system": row["exact_transformed_coordinate_system"],
        "exact_transformed_open_cell": row["exact_transformed_open_cell"],
        "exact_transformed_cell_volume": row["exact_transformed_cell_volume"],
    }


class HeldAnchors:
    def __init__(self) -> None:
        self.dirfd = -1
        self.dir_before: os.stat_result | None = None
        self.files: dict[str, tuple[int, os.stat_result, str, int, str]] = {}
        self.rows: list[dict[str, Any]] = []

    def __enter__(self) -> "HeldAnchors":
        named = os.stat(DELIVERABLES, follow_symlinks=False)
        need(stat.S_ISDIR(named.st_mode), "deliverables directory")
        self.dirfd = os.open(DELIVERABLES, os.O_RDONLY | getattr(os, "O_DIRECTORY", 0) | getattr(os, "O_CLOEXEC", 0) | getattr(os, "O_NOFOLLOW", 0))
        self.dir_before = os.fstat(self.dirfd)
        need(dir_identity(named) == dir_identity(self.dir_before), "deliverables dirfd binding")
        try:
            for label, filename, size, sha in ANCHOR_PINS:
                before = os.stat(filename, dir_fd=self.dirfd, follow_symlinks=False)
                need(stat.S_ISREG(before.st_mode) and before.st_nlink == 1 and before.st_size == size, "anchor type/size:" + label)
                fd = os.open(filename, os.O_RDONLY | getattr(os, "O_CLOEXEC", 0) | getattr(os, "O_NOFOLLOW", 0), dir_fd=self.dirfd)
                opened = os.fstat(fd)
                need(fingerprint(before) == fingerprint(opened), "anchor open race:" + label)
                count, observed = hash_fd(fd, size)
                need(count == size and observed == sha, "anchor first hash:" + label)
                self.files[label] = (fd, opened, filename, size, sha)
                self.rows.append({"label": label, "filename": filename, "exact_size": size, "sha256": sha, "pass1_sha256": observed})
            return self
        except BaseException:
            self.close(False)
            raise

    def bytes(self, label: str) -> bytes:
        fd, before, _, size, _ = self.files[label]
        raw = os.pread(fd, size, 0)
        need(len(raw) == size and fingerprint(before) == fingerprint(os.fstat(fd)), "anchor held read:" + label)
        return raw

    def close(self, verify: bool) -> None:
        error: BaseException | None = None
        for label, (fd, before, filename, size, sha) in list(self.files.items()):
            try:
                if verify:
                    count, observed = hash_fd(fd, size)
                    named = os.stat(filename, dir_fd=self.dirfd, follow_symlinks=False)
                    need(count == size and observed == sha, "anchor final hash:" + label)
                    need(fingerprint(before) == fingerprint(os.fstat(fd)) == fingerprint(named), "anchor final binding:" + label)
                    for row in self.rows:
                        if row["label"] == label:
                            row["pass2_sha256"] = observed
                            row["final_path_bound"] = True
            except BaseException as exc:
                if error is None:
                    error = exc
            finally:
                os.close(fd)
        self.files.clear()
        if self.dirfd >= 0:
            try:
                if verify:
                    assert self.dir_before is not None
                    need(dir_identity(self.dir_before) == dir_identity(os.fstat(self.dirfd)) == dir_identity(os.stat(DELIVERABLES, follow_symlinks=False)), "deliverables directory replaced")
            finally:
                os.close(self.dirfd)
                self.dirfd = -1
        if error is not None:
            raise error

    def __exit__(self, exc_type: Any, exc: Any, tb: Any) -> None:
        self.close(exc_type is None)


def load_p1(raw: bytes) -> types.ModuleType:
    module = types.ModuleType("cm2_k2i2_held_p1_snapshot")
    module.__file__ = str(DELIVERABLES / ANCHOR_PINS[0][1])
    module.__dict__["__name__"] = module.__name__
    exec(compile(raw, module.__file__, "exec"), module.__dict__)
    doc = module.contract_document()
    module.validate_contract(doc)
    need(doc["formal_credit"]["normalized_member_support"] == 0, "P1 normalized zero credit")
    need(doc["formal_credit"]["representation_cover"] == 0, "P1 representation zero credit")
    return module


def build_raw_index(p1: types.ModuleType) -> tuple[dict[str, Any], ...]:
    with p1.HeldInputs() as held:
        structure = held.validate_selected_documents()
        geometry = p1._load_preserved_geometry(held)
        expanded = p1._load_r266_expanded(held, geometry)
        registry_by_row, registry_by_member = p1._load_preserved_registry(held, expanded)
        preserved = p1._load_preserved_b0(held, registry_by_row)
        non_graph_nodes = p1._load_non_graph_sources(held)
        lineage_counts = p1._validate_non_graph_lineage(held, non_graph_nodes)
        non_graph = p1._load_non_graph_r266_b0(held, non_graph_nodes)
        need(set(preserved).isdisjoint(non_graph), "scope overlap")
        scope = set(preserved) | set(non_graph)
        need(len(scope) == 144_296, "scope census")

        b0: dict[str, dict[str, Any]] = {}
        for row in p1.direct_rows(held, "B0", "member_support_source_rows"):
            member = row.get("member_id")
            if member not in scope:
                continue
            p1.row_digest(row)
            need(member not in b0, "duplicate selected B0 member")
            b0[member] = {
                "row_id": row["Round306B0_member_support_source_row_id"],
                "row_sha256": row["row_sha256"],
                "primary_source_package": row["primary_source_package"],
                "primary_source_row_id": row["primary_source_row_id"],
                "primary_source_row_sha256": row["primary_source_row_sha256"],
                "identity_tranche": row["identity_tranche"],
            }
        need(set(b0) == scope, "B0 selected anti-join")

        r294_aliases: list[dict[str, Any]] = []
        all_r294_owners: set[tuple[str, str]] = set()
        preserved_alias_owners: set[tuple[str, str]] = set()
        residual = 0
        kind_counts: Counter[str] = Counter()
        for row in p1.direct_rows(held, "R294_ALIAS", "rows"):
            p1.row_digest(row)
            owner = (row["alias_source_kind"], row["source_representation_id"])
            need(owner not in all_r294_owners, "duplicate R294 alias owner")
            all_r294_owners.add(owner)
            target = row["target_registry_occurrence_id"]
            if target not in preserved:
                residual += 1
                continue
            need(target in registry_by_member, "R294 preserved target registry")
            preserved_alias_owners.add(owner)
            kind = row["support_representation_kind"]
            kind_counts[kind] += 1
            r294_aliases.append({
                "owner_member_id": target,
                "source_kind": row["alias_source_kind"],
                "source_representation_id": row["source_representation_id"],
                "source_row_id": row["Round294_occurrence_representation_binding_row_id"],
                "source_row_sha256": row["row_sha256"],
                "representation_semantics": kind,
                "geometry_payload": r294_geometry_payload(row),
            })
        need(len(all_r294_owners) == 46_288 and residual == 7_288, "R294 dispatch census")
        need(len(r294_aliases) == len(preserved_alias_owners) == 39_000, "R294 preserved alias census")

        r295_aliases: list[dict[str, Any]] = []
        r295_owners: set[str] = set()
        r295_targets: set[str] = set()
        for row in p1.direct_rows(held, "R295A_ALIAS", "rows"):
            p1.row_digest(row)
            target_row = registry_by_row.get(row["target_Round294_occurrence_registry_row_id"])
            need(target_row is not None, "R295 target registry")
            target = row["target_Round294_registry_occurrence_id"]
            need(target == target_row["member_id"] and target in preserved, "R295 preserved target")
            need(row["target_Round294_occurrence_registry_row_sha256"] == target_row["row_sha256"], "R295 registry SHA")
            owner = row["source_Round179_retained_child_row_id"]
            need(owner not in r295_owners, "duplicate R295 owner")
            r295_owners.add(owner)
            r295_targets.add(target)
            r295_aliases.append({
                "owner_member_id": target,
                "source_kind": "R295A_ROUND179_ADJACENT_POSITIVE_T_CONTINUATION",
                "source_representation_id": owner,
                "source_row_id": row["Round295A_retained_continuation_alias_row_id"],
                "source_row_sha256": row["row_sha256"],
                "representation_semantics": "ADJACENT_POSITIVE_T_CONTINUATION",
                "geometry_payload": {
                    "support_representation_kind": "ADJACENT_POSITIVE_T_CONTINUATION",
                    "retained_positive_t_open_box": row["retained_positive_t_open_box"],
                },
            })
        need(len(r295_aliases) == len(r295_owners) == len(r295_targets) == 276, "R295 alias census")
        r294_targets = {row["owner_member_id"] for row in r294_aliases}
        need(r294_targets.isdisjoint(r295_targets), "R294/R295 target overlap")
        kind_counts["ADJACENT_POSITIVE_T_CONTINUATION"] = 276
        need(dict(kind_counts) == ALIAS_KIND_COUNTS, "alias semantic census")
        held.finalize()
        raw_pin_rows = list(held.rows)
        structure_digest = p1.digest(structure)

    return preserved, non_graph, geometry, registry_by_member, non_graph_nodes, b0, r294_aliases, r295_aliases, lineage_counts, {"P1_input_pins": raw_pin_rows, "P1_structure_rows_sha256": structure_digest}


def write_jsonl(path: Path, rows: list[dict[str, Any]], order: str) -> dict[str, Any]:
    raw_hash = hashlib.sha256()
    raw_size = 0
    with path.open("wb") as target:
        with gzip.GzipFile(filename="", mode="wb", fileobj=target, compresslevel=9, mtime=0) as zipped:
            for row in rows:
                wire = canonical(row) + b"\n"
                raw_hash.update(wire)
                raw_size += len(wire)
                zipped.write(wire)
        target.flush()
        os.fsync(target.fileno())
    named = os.stat(path, follow_symlinks=False)
    need(stat.S_ISREG(named.st_mode) and named.st_nlink == 1, "staged ledger regular single-link")
    fd = os.open(path, os.O_RDONLY | getattr(os, "O_CLOEXEC", 0) | getattr(os, "O_NOFOLLOW", 0))
    try:
        opened = os.fstat(fd)
        need(fingerprint(named) == fingerprint(opened), "staged ledger open binding")
        size, sha = hash_fd(fd, named.st_size)
        need(fingerprint(opened) == fingerprint(os.fstat(fd)) == fingerprint(os.stat(path, follow_symlinks=False)), "staged ledger final binding")
    finally:
        os.close(fd)
    return {"filename": path.name, "row_count": len(rows), "uncompressed_jsonl_size": raw_size, "uncompressed_jsonl_sha256": raw_hash.hexdigest(), "file_size": size, "file_sha256": sha, "order": order}


def outside(path: str, protected: str) -> bool:
    try:
        return os.path.commonpath((path, protected)) != protected
    except ValueError:
        return True


def produce(output_directory: Path, seed: str) -> dict[str, Any]:
    need(type(seed) is str, "seed type")
    output_directory = Path(os.path.abspath(output_directory))
    output_named = os.stat(output_directory, follow_symlinks=False)
    need(stat.S_ISDIR(output_named.st_mode), "real output directory")
    output_fd = os.open(output_directory, os.O_RDONLY | getattr(os, "O_DIRECTORY", 0) | getattr(os, "O_CLOEXEC", 0) | getattr(os, "O_NOFOLLOW", 0))
    need(dir_identity(output_named) == dir_identity(os.fstat(output_fd)), "output dirfd binding")
    try:
        with HeldAnchors() as anchors:
            k2p0_result = parse_json_bytes(anchors.bytes("K2P0_RESULT"))
            k2p0_ledger = parse_json_bytes(anchors.bytes("K2P0_LEDGER"))
            need(k2p0_result["formal_credit"] == 0 and k2p0_result["normalized_full_support_credit"] == 0, "K2P0 zero credit")
            need(k2p0_result["ledger_file_sha256"] == ANCHOR_PINS[2][3], "K2P0 ledger binding")
            need(k2p0_ledger["ledger"]["artifact_kind"] == "ZERO_CREDIT_DIRECT_SOURCE_AUTHORITY_FRONTIER", "K2P0 artifact kind")
            p1 = load_p1(anchors.bytes("P1"))
            anchor_rows = anchors.rows
            (preserved, non_graph, geometry, registry, nodes, b0, r294_aliases, r295_aliases, lineage_counts, replay_audit) = build_raw_index(p1)

        members: list[dict[str, Any]] = []
        representations: list[dict[str, Any]] = []
        member_counts: Counter[str] = Counter()
        rep_counts: Counter[str] = Counter()
        primary_ids: set[str] = set()
        alias_ids: set[str] = set()
        global_raw_commitment = digest({
            "schema": SCHEMA + ".global-raw-input-commitment.v1",
            "anchor_pins": [
                {"label": label, "filename": filename, "exact_size": size, "sha256": sha}
                for label, filename, size, sha in ANCHOR_PINS
            ],
            "P1_replay_audit": replay_audit,
        })

        for member in sorted(set(preserved) | set(non_graph), key=lambda value: value.encode("ascii")):
            is_preserved = member in preserved
            source = preserved[member] if is_preserved else non_graph[member]
            fine = source["family"]
            coarse = "PRESERVED" if is_preserved else "NON_GRAPH"
            box_sha = digest(source["box"])
            b0row = b0[member]
            direct = geometry[member] if is_preserved else nodes[member]
            direct_package = "R" + fine[5:8] if fine.startswith("ROUND") else fine.split("_")[0]
            primary_input_commitment = {
                "schema": SCHEMA + ".primary-input-commitment.v1",
                "global_raw_input_commitment_sha256": global_raw_commitment,
                "member_id": member,
                "coarse_family": coarse,
                "fine_family": fine,
                "source_B0_row_id": b0row["row_id"],
                "source_B0_row_sha256": b0row["row_sha256"],
                "primary_source_package": b0row["primary_source_package"],
                "primary_source_row_id": b0row["primary_source_row_id"],
                "primary_source_row_sha256": b0row["primary_source_row_sha256"],
                "direct_construction_package": direct_package,
                "direct_construction_row_id": member,
                "direct_construction_row_sha256": direct["row_sha256"],
                "exact_geometry_payload_sha256": box_sha,
            }
            primary_input_commitment_sha = digest(primary_input_commitment)
            primary_id = "k2i2-primary:" + primary_input_commitment_sha
            need(primary_id not in primary_ids, "duplicate primary representation handle")
            primary_ids.add(primary_id)
            direct_sha_mode = "DECLARED_OR_RECOMPUTED_ROW_SHA256" if fine not in ("ROUND174_RESOLVED", "ROUND179_RESOLVED") else "RECOMPUTED_PACKED_ROW_SHA256_UNDER_WHOLE_FILE_PIN"
            member_row = closed({
                "schema": SCHEMA + ".member-row",
                "status": "IDENTITY_JOINED_ENGINEERING_ONLY",
                "coarse_family": coarse,
                "fine_family": fine,
                "member_id": member,
                "primary_representation_id": primary_id,
                "source_B0_row_id": b0row["row_id"],
                "source_B0_row_sha256": b0row["row_sha256"],
                "primary_source_package": b0row["primary_source_package"],
                "primary_source_row_id": b0row["primary_source_row_id"],
                "primary_source_row_sha256": b0row["primary_source_row_sha256"],
                "direct_construction_package": direct_package,
                "direct_construction_row_id": member,
                "direct_construction_row_sha256": direct["row_sha256"],
                "direct_row_sha_authority_mode": direct_sha_mode,
                "exact_geometry_payload_sha256": box_sha,
                "input_commitment_sha256": primary_input_commitment_sha,
                "global_raw_input_commitment_sha256": global_raw_commitment,
                "authority_priority": "EXACT_CONSTRUCTION_ROW>DIRECT_LINEAGE>IDENTITY_BINDING>PROMOTION_SUMMARY>WITNESS_OR_ENVELOPE",
                "support_semantics": "MECHANICAL_IDENTITY_AND_PAYLOAD_HANDLE_ONLY__FULL_SUPPORT_NOT_PROVED",
                "formal_credit": dict(ZERO_CREDIT),
            })
            members.append(member_row)
            representations.append(closed({
                "schema": SCHEMA + ".representation-row",
                "status": "OWNER_INDEXED_ENGINEERING_ONLY",
                "representation_id": primary_id,
                "representation_role": "PRIMARY_ENGINEERING_HANDLE",
                "representation_semantics": "DIRECT_CONSTRUCTION_PAYLOAD_HANDLE__SET_EQUALITY_NOT_PROVED",
                "owner_member_id": member,
                "owner_coarse_family": coarse,
                "owner_fine_family": fine,
                "source_row_id": member,
                "source_row_sha256": direct["row_sha256"],
                "exact_geometry_payload_sha256": box_sha,
                "input_commitment_sha256": primary_input_commitment_sha,
                "global_raw_input_commitment_sha256": global_raw_commitment,
                "row_sha_authority_mode": direct_sha_mode,
                "formal_feature_row": False,
                "formal_credit": dict(ZERO_CREDIT),
            }))
            member_counts[coarse] += 1
            rep_counts[coarse + "_PRIMARY"] += 1

        for alias in sorted(r294_aliases + r295_aliases, key=lambda row: (row["source_kind"].encode("ascii"), row["source_representation_id"].encode("ascii"))):
            owner = alias["owner_member_id"]
            target_registry = registry[owner]
            alias_box_sha = digest(alias["geometry_payload"])
            alias_input_commitment = {
                "schema": SCHEMA + ".alias-input-commitment.v1",
                "global_raw_input_commitment_sha256": global_raw_commitment,
                "owner_member_id": owner,
                "owner_source_B0_row_id": b0[owner]["row_id"],
                "owner_source_B0_row_sha256": b0[owner]["row_sha256"],
                "target_R294_registry_row_id": target_registry["row_id"],
                "target_R294_registry_row_sha256": target_registry["row_sha256"],
                "source_kind": alias["source_kind"],
                "source_representation_id": alias["source_representation_id"],
                "source_row_id": alias["source_row_id"],
                "source_row_sha256": alias["source_row_sha256"],
                "representation_semantics": alias["representation_semantics"],
                "exact_geometry_payload_sha256": alias_box_sha,
            }
            alias_input_commitment_sha = digest(alias_input_commitment)
            rep_id = "k2i2-alias:" + alias_input_commitment_sha
            need(rep_id not in primary_ids and rep_id not in alias_ids, "duplicate alias representation handle")
            alias_ids.add(rep_id)
            semantics = alias["representation_semantics"]
            representations.append(closed({
                "schema": SCHEMA + ".representation-row",
                "status": "OWNER_INDEXED_ENGINEERING_ONLY",
                "representation_id": rep_id,
                "representation_role": "PRESERVED_ALIAS_HANDLE",
                "representation_semantics": semantics,
                "owner_member_id": owner,
                "owner_coarse_family": "PRESERVED",
                "source_kind": alias["source_kind"],
                "source_representation_id": alias["source_representation_id"],
                "source_row_id": alias["source_row_id"],
                "source_row_sha256": alias["source_row_sha256"],
                "target_R294_registry_row_id": target_registry["row_id"],
                "target_R294_registry_row_sha256": target_registry["row_sha256"],
                "owner_source_B0_row_id": b0[owner]["row_id"],
                "owner_source_B0_row_sha256": b0[owner]["row_sha256"],
                "exact_geometry_payload_sha256": alias_box_sha,
                "input_commitment_sha256": alias_input_commitment_sha,
                "global_raw_input_commitment_sha256": global_raw_commitment,
                "row_sha_authority_mode": "DECLARED_ROW_SHA256_RECOMPUTED_UNDER_WHOLE_FILE_PIN",
                "coverage_semantics": "ALIAS_OR_SUBCOVER_EVIDENCE_ONLY__COMPLETE_SUPPORT_SET_EQUALITY_NOT_PROVED",
                "formal_feature_row": False,
                "formal_credit": dict(ZERO_CREDIT),
            }))
            rep_counts["PRESERVED_ALIAS"] += 1

        representations.sort(key=lambda row: row["representation_id"].encode("ascii"))
        need(len(members) == 144_296 and member_counts == Counter({"PRESERVED": 126_468, "NON_GRAPH": 17_828}), "member output census")
        need(len(representations) == 183_572 and rep_counts == Counter({"PRESERVED_PRIMARY": 126_468, "PRESERVED_ALIAS": 39_276, "NON_GRAPH_PRIMARY": 17_828}), "representation output census")
        need(len(primary_ids) == 144_296 and len(alias_ids) == 39_276, "representation ID uniqueness")

        gap_bodies = [
            {"gap_id": "G01_NORMALIZED_SUPPORT_THEOREM", "status": "MISSING_NOT_DISCHARGED", "affected_member_count": 144_296, "formal_credit": 0},
            {"gap_id": "G02_REPRESENTATION_SET_EQUALITY", "status": "MISSING_NOT_DISCHARGED", "affected_representation_count": 183_572, "formal_credit": 0},
            {"gap_id": "G03_A1_A2_THEOREM_OBLIGATIONS", "status": "ENUMERATED_BY_P1_NOT_DISCHARGED", "obligation_count": 80_092, "formal_credit": 0},
            {"gap_id": "G04_K2P0_DIRECT_AUTHORITY_FRONTIER", "status": "SIX_OF_SIX_SEMANTIC_AUTHORITIES_BLOCKED", "blocked_source_count": 6, "selected_rows_missing_own_sha256": 137_136, "formal_credit": 0},
            {"gap_id": "G05_INDEPENDENT_MATH_IMPLEMENTATION", "status": "P1_RAW_REPLAY_LOGIC_REUSED__NOT_INDEPENDENT", "formal_credit": 0},
            {"gap_id": "G06_GLOBAL_PIPELINE", "status": "B1A_B2_D02_D03_D04_GATE5_CM2_NOT_REACHED", "formal_credit": 0},
        ]
        gaps: list[dict[str, Any]] = []
        for body in gap_bodies:
            gap_input_commitment = {
                "schema": SCHEMA + ".gap-input-commitment.v1",
                "global_raw_input_commitment_sha256": global_raw_commitment,
                "gap_body": body,
            }
            gap_input_sha = digest(gap_input_commitment)
            gaps.append(closed({
                "schema": SCHEMA + ".gap-row",
                **body,
                "gap_handle_id": "k2i2-gap:" + gap_input_sha,
                "input_commitment_sha256": gap_input_sha,
                "global_raw_input_commitment_sha256": global_raw_commitment,
            }))

        root = "/tmp"
        need(os.path.realpath(root) == root and outside(root, os.path.realpath(DELIVERABLES)), "explicit /tmp authority")
        root_named = os.stat(root, follow_symlinks=False)
        need(stat.S_ISDIR(root_named.st_mode), "/tmp directory")
        root_fd = os.open(root, os.O_RDONLY | getattr(os, "O_DIRECTORY", 0) | getattr(os, "O_CLOEXEC", 0) | getattr(os, "O_NOFOLLOW", 0))
        root_held = os.fstat(root_fd)
        need(dir_identity(root_named) == dir_identity(root_held), "/tmp held binding")
        try:
            with tempfile.TemporaryDirectory(prefix="cm2-k2i2-", dir=root) as scratch_name:
                scratch_real = os.path.realpath(scratch_name)
                need(os.path.dirname(scratch_real) == root and outside(scratch_real, os.path.realpath(DELIVERABLES)), "scratch placement")
                scratch_named = os.stat(scratch_real, follow_symlinks=False)
                scratch_fd = os.open(scratch_real, os.O_RDONLY | getattr(os, "O_DIRECTORY", 0) | getattr(os, "O_CLOEXEC", 0) | getattr(os, "O_NOFOLLOW", 0))
                need(dir_identity(scratch_named) == dir_identity(os.fstat(scratch_fd)), "scratch held binding")
                try:
                    scratch = Path(scratch_real)
                    ledgers = {
                        "member": write_jsonl(scratch / OUTPUTS["member"], members, "unsigned_bytewise_ASCII_member_id"),
                        "representation": write_jsonl(scratch / OUTPUTS["representation"], representations, "unsigned_bytewise_ASCII_representation_id"),
                        "gap": write_jsonl(scratch / OUTPUTS["gap"], gaps, "gap_id"),
                    }
                    result = {
                        "schema": SCHEMA,
                        "status": STATUS,
                        "scope": "PRESERVED_AND_NON_GRAPH_PARTIAL_LANE",
                        "producer_sha256": None,
                        "producer_byte_binding": "EXTERNAL_INDEPENDENT_VERIFIER_STATIC_PIN_ONLY",
                        "seed_affects_output": False,
                        "P1_execution_disclosure": "HELD_STATIC_P1_SOURCE_SNAPSHOT_EXECUTED_FOR_RAW_JOIN_REUSE__NOT_AN_INDEPENDENT_MATH_IMPLEMENTATION",
                        "anchor_pins": anchor_rows,
                        "P1_replay_audit": replay_audit,
                        "global_raw_input_commitment_sha256": global_raw_commitment,
                        "exact_census": {
                            "member_count": 144_296,
                            "preserved_member_count": 126_468,
                            "non_graph_member_count": 17_828,
                            "representation_candidate_count": 183_572,
                            "preserved_representation_candidate_count": 165_744,
                            "non_graph_representation_candidate_count": 17_828,
                            "primary_representation_count": 144_296,
                            "preserved_alias_representation_count": 39_276,
                            "R294_preserved_alias_count": 39_000,
                            "R295A_preserved_alias_count": 276,
                            "P1_A1_A2_obligation_census_not_feature_rows": 80_092,
                        },
                        "fine_member_counts": dict(sorted((Counter(row["fine_family"] for row in members)).items())),
                        "alias_semantic_counts": dict(sorted(ALIAS_KIND_COUNTS.items())),
                        "lineage_replay_counts": lineage_counts,
                        "closed_anti_joins": {
                            "scope_family_overlap": 0,
                            "selected_members_minus_B0": 0,
                            "B0_selected_minus_members": 0,
                            "R294_preserved_alias_owner_duplicates": 0,
                            "R295A_alias_owner_duplicates": 0,
                            "R294_R295A_target_overlap": 0,
                            "orphan_representation_owner_count": 0,
                            "duplicate_representation_handle_count": 0,
                        },
                        "ledgers": ledgers,
                        "known_gaps": {"normalized_support": 144_296, "representation_set_equality": 183_572, "A1_A2": 80_092, "other_coarse_families_members": 420_196, "global_representation_rows_remaining": 428_332, "K2P0_selected_source_rows_missing_own_sha256": 137_136},
                        "formal_credit": dict(ZERO_CREDIT),
                    }
                    result_path = scratch / OUTPUTS["result"]
                    result_path.write_bytes(canonical(result) + b"\n")
                    with result_path.open("rb") as handle:
                        os.fsync(handle.fileno())
                    for key in ("member", "representation", "gap", "result"):
                        staged = os.stat(OUTPUTS[key], dir_fd=scratch_fd, follow_symlinks=False)
                        need(stat.S_ISREG(staged.st_mode) and staged.st_nlink == 1, "staged output:" + key)
                        os.replace(OUTPUTS[key], OUTPUTS[key], src_dir_fd=scratch_fd, dst_dir_fd=output_fd)
                        published = os.stat(OUTPUTS[key], dir_fd=output_fd, follow_symlinks=False)
                        need(stat.S_ISREG(published.st_mode) and published.st_nlink == 1 and published.st_size == staged.st_size, "published output:" + key)
                    need(dir_identity(output_named) == dir_identity(os.fstat(output_fd)) == dir_identity(os.stat(output_directory, follow_symlinks=False)), "output final binding")
                finally:
                    os.close(scratch_fd)
            need(dir_identity(root_held) == dir_identity(os.fstat(root_fd)) == dir_identity(os.stat(root, follow_symlinks=False)), "/tmp final binding")
        finally:
            os.close(root_fd)
        return result
    finally:
        os.close(output_fd)


def self_test() -> dict[str, Any]:
    row = closed({"x": 1, "formal": False})
    body = dict(row)
    claimed = body.pop("row_sha256")
    need(type(claimed) is str and HEX64.fullmatch(claimed) is not None and digest(body) == claimed, "row closure")
    need(type(False) is bool and type(False) is not int, "bool type identity fixture")
    need(type(0) is int and type(0) is not bool, "int type identity fixture")
    need(
        digest({"B0_sha256": "0" * 64, "source_sha256": "1" * 64})
        != digest({"B0_sha256": "0" * 64, "source_sha256": "2" * 64}),
        "different raw commitments must have different digests",
    )
    exact = {"x": "a" * (MAX_ROW - len(canonical({"x": ""})))}
    need(len(canonical(exact)) == MAX_ROW, "exact canonical cap")
    rejected = False
    try:
        canonical({"x": exact["x"] + "a"})
    except Blocked:
        rejected = True
    need(rejected, "cap plus one rejected")
    return {"schema": SCHEMA + ".self-test", "status": "PASS", "producer_is_formal": False, "exact_cap": MAX_ROW, "cap_plus_one_rejected": True, "recursive_type_strictness_required_downstream": True, "different_raw_commitments_have_different_digests": True}


def main() -> int:
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--self-test", action="store_true")
    group.add_argument("--produce", action="store_true")
    parser.add_argument("--output-directory")
    parser.add_argument("--hash-seed", default="0")
    args = parser.parse_args()
    if args.self_test:
        need(args.output_directory is None, "self-test filesystem inert")
        print(canonical(self_test()).decode("ascii"))
        return 0
    need(args.output_directory is not None, "output directory required")
    result = produce(Path(args.output_directory), args.hash_seed)
    print(canonical({"status": result["status"], "result_sha256": digest(result)}).decode("ascii"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
