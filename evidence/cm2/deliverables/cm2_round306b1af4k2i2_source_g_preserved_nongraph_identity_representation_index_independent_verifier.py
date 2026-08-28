#!/usr/bin/env python3
"""Independent verifier for K2I2 preserved/non-graph identity index.

The verifier never imports or executes the producer.  It statically pins the
producer and all candidate bytes, separately executes the held P1 raw-replay
snapshot, reconstructs every expected member/representation/gap row, and
requires byte-canonical ledger equality.  P1 reuse is still not an independent
mathematical theorem implementation and earns zero formal credit.
"""

from __future__ import annotations

import argparse
from collections import Counter
import gzip
import hashlib
import io
import json
import os
from pathlib import Path
import re
import stat
import tempfile
import types
from typing import Any, BinaryIO, Iterator


class Rejected(RuntimeError):
    pass


def need(condition: bool, label: str) -> None:
    if not condition:
        raise Rejected(label)


PREFIX = "cm2_round306b1af4k2i2_source_g_preserved_nongraph_identity_representation_index_"
SCHEMA = "cm2.round306b1af4k2i2.source-g-preserved-nongraph-identity-representation-index.v1"
STATUS = "PASS_MECHANICAL_144296_MEMBER_183572_REPRESENTATION_INDEX__ZERO_THEOREM_CREDIT"
VERIFICATION_STATUS = "PASS_INDEPENDENT_BYTE_EXACT_K2I2_REPLAY__ZERO_THEOREM_CREDIT"
DELIVERABLES = Path(__file__).resolve().parent
MAX_ROW = 8 << 20
HEX64 = re.compile(r"^[0-9a-f]{64}$")

# Candidate pins are filled only after the double-seed producer replay is
# byte-identical.  No wildcard, result-declared filename, or result-declared
# digest participates in path selection.
EXPECTED_FILES: tuple[tuple[str, str, int, str], ...] = (
    ("P1", "cm2_round306b1af4p1_source_g_preserved_non_graph_exact_join_preflight.py", 112_834, "34098cfd5c5e8d1ff73b4a172ecd0a1375a74a4e51a12c6e89b7984474062dfd"),
    ("K2P0_RESULT", "cm2_round306b1af4k2p0_preserved_nongraph_authority_frontier_result.json", 1_214, "8a32251023ec7c4a8b42d9affdac931376fd8e5f373e49503ce6272235493a93"),
    ("K2P0_LEDGER", "cm2_round306b1af4k2p0_preserved_nongraph_authority_frontier_ledger.json", 35_521, "e56a50b1ce88f0ae45eb09a194a15d3c26804c6e5baac803a1f5f4a19231ed3d"),
    ("PRODUCER", PREFIX + "producer.py", 36_701, "c49601ec8884107ed72338ccdec60b6efc4ee18f565deba9021cabce86aad0a0"),
    ("RESULT", PREFIX + "result.json", 14_562, "4cd7c9982cdd9a72f34a912d78b6dd061fd8351b31581c84b5aaf20a70893e82"),
    ("MEMBER", PREFIX + "member_index.jsonl.gz", 54_523_995, "fbbc37f578219e3167eab1e87f8fc5c67675af4fa6eee979c93d6c0f45d8fc31"),
    ("REPRESENTATION", PREFIX + "representation_index.jsonl.gz", 50_484_688, "68774286f5e25c8e0e41ea42ee3b59fb601ea56d8540ef22e3b949cdce427e83"),
    ("GAP", PREFIX + "authority_gap_index.jsonl.gz", 1_146, "8087a64240a9dc250439b62c3d130063cbb9ff8074e88dc182b20ee57e0314b1"),
)

PRESERVED_COUNTS = {"ROUND174_RESOLVED": 72_500, "ROUND179_RESOLVED": 17_192, "ROUND204_REGION": 736, "ROUND208_REGION": 36_040}
NON_GRAPH_COUNTS = {"R245_WHOLE_ROOT_ZERO_ABSENCE_BULK": 2_872, "R246_WHOLE_ORIGIN_SINGLE_SIGNATURE_RETAINED_BULK": 2_220, "R247_CROSSING_TIME_WHOLE_SIGNATURE_RETAINED_BULK": 240, "R247_SOURCE_CHART_SEAM_WHOLE_SIGNATURE_RETAINED_BULK": 264, "R248_ROUND234_RESOLVED_DESCENDANT": 12_200, "R248_ROUND236_CROSSING_DISCHARGE_BULK": 32}
ALIAS_KIND_COUNTS = {"EXACT_EQUAL_SUPPORT_ENVELOPE_ALIAS_EVIDENCE": 36_680, "EXACT_SAME_POSITIVE_OPEN_REGION_INCLUSION_SUBCOVER": 720, "EXACT_T2_P_S_EXISTING_OCCURRENCE_SUBCOVER_CELL": 1_600, "ADJACENT_POSITIVE_T_CONTINUATION": 276}
ZERO_CREDIT = {"normalized_support": 0, "representation_cover": 0, "A1_A2": 0, "B1A": 0, "B2": 0, "maximality": 0, "fibre": 0, "global_disposition": 0, "D02": 0, "D03": 0, "D04": 0, "Gate5": 0, "CM2": 0}


def canonical(value: Any) -> bytes:
    raw = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True, allow_nan=False).encode("ascii")
    need(len(raw) <= MAX_ROW, "canonical cap")
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
    raise Rejected("nonintegral/nonstandard number:" + token)


def decode(raw: bytes) -> Any:
    need(len(raw) <= MAX_ROW, "decoded byte cap")
    value = json.loads(raw, object_pairs_hook=unique_object, parse_float=reject_number, parse_constant=reject_number)
    canonical(value)
    return value


def strict_equal(actual: Any, expected: Any, label: str = "root") -> None:
    need(type(actual) is type(expected), label + ":type")
    if type(expected) is dict:
        need(set(actual) == set(expected), label + ":keys")
        for key in expected:
            strict_equal(actual[key], expected[key], label + "." + key)
    elif type(expected) is list:
        need(len(actual) == len(expected), label + ":length")
        for index, value in enumerate(expected):
            strict_equal(actual[index], value, f"{label}[{index}]")
    else:
        need(actual == expected, label + ":value")


def fingerprint(value: os.stat_result) -> tuple[int, ...]:
    return (value.st_dev, value.st_ino, value.st_mode, value.st_nlink, value.st_size, value.st_mtime_ns, value.st_ctime_ns)


def dir_identity(value: os.stat_result) -> tuple[int, int, int]:
    return (value.st_dev, value.st_ino, value.st_mode)


def outside(path: str, protected: str) -> bool:
    try:
        return os.path.commonpath((path, protected)) != protected
    except ValueError:
        return True


def hash_fd(fd: int, cap: int) -> tuple[int, str]:
    state = hashlib.sha256()
    total = 0
    offset = 0
    while True:
        block = os.pread(fd, 1 << 20, offset)
        if not block:
            break
        offset += len(block)
        total += len(block)
        need(total <= cap, "held file grew")
        state.update(block)
    return total, state.hexdigest()


class HeldPackage:
    def __init__(self) -> None:
        self.dirfd = -1
        self.dir_before: os.stat_result | None = None
        self.files: dict[str, tuple[int, os.stat_result, str, int, str]] = {}
        self.rows: list[dict[str, Any]] = []

    def __enter__(self) -> "HeldPackage":
        need(all(size > 0 and HEX64.fullmatch(sha) is not None for _, _, size, sha in EXPECTED_FILES), "verifier static pins finalized")
        named = os.stat(DELIVERABLES, follow_symlinks=False)
        need(stat.S_ISDIR(named.st_mode), "deliverables directory")
        self.dirfd = os.open(DELIVERABLES, os.O_RDONLY | getattr(os, "O_DIRECTORY", 0) | getattr(os, "O_CLOEXEC", 0) | getattr(os, "O_NOFOLLOW", 0))
        self.dir_before = os.fstat(self.dirfd)
        need(dir_identity(named) == dir_identity(self.dir_before), "deliverables dirfd binding")
        try:
            for label, filename, size, sha in EXPECTED_FILES:
                before = os.stat(filename, dir_fd=self.dirfd, follow_symlinks=False)
                need(stat.S_ISREG(before.st_mode) and before.st_nlink == 1 and before.st_size == size, "file type/size:" + label)
                fd = os.open(filename, os.O_RDONLY | getattr(os, "O_CLOEXEC", 0) | getattr(os, "O_NOFOLLOW", 0), dir_fd=self.dirfd)
                opened = os.fstat(fd)
                need(fingerprint(before) == fingerprint(opened), "file open race:" + label)
                count, observed = hash_fd(fd, size)
                need(count == size and observed == sha, "file first hash:" + label)
                self.files[label] = (fd, opened, filename, size, sha)
                self.rows.append({"label": label, "filename": filename, "exact_size": size, "sha256": sha, "pass1_sha256": observed})
            return self
        except BaseException:
            self.close(False)
            raise

    def bytes(self, label: str) -> bytes:
        fd, before, _, size, _ = self.files[label]
        raw = os.pread(fd, size, 0)
        need(len(raw) == size and fingerprint(before) == fingerprint(os.fstat(fd)), "held bytes:" + label)
        return raw

    def binary(self, label: str) -> BinaryIO:
        fd, before, _, _, _ = self.files[label]
        need(fingerprint(before) == fingerprint(os.fstat(fd)), "held binary start:" + label)
        return os.fdopen(os.dup(fd), "rb")

    def close(self, verify: bool) -> None:
        error: BaseException | None = None
        for label, (fd, before, filename, size, sha) in list(self.files.items()):
            try:
                if verify:
                    count, observed = hash_fd(fd, size)
                    named = os.stat(filename, dir_fd=self.dirfd, follow_symlinks=False)
                    need(count == size and observed == sha, "file final hash:" + label)
                    need(fingerprint(before) == fingerprint(os.fstat(fd)) == fingerprint(named), "file final binding:" + label)
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
                    need(dir_identity(self.dir_before) == dir_identity(os.fstat(self.dirfd)) == dir_identity(os.stat(DELIVERABLES, follow_symlinks=False)), "deliverables replaced")
            finally:
                os.close(self.dirfd)
                self.dirfd = -1
        if error is not None:
            raise error

    def __exit__(self, exc_type: Any, exc: Any, tb: Any) -> None:
        self.close(exc_type is None)


def load_p1(raw: bytes) -> types.ModuleType:
    module = types.ModuleType("cm2_k2i2_verifier_held_p1")
    module.__file__ = str(DELIVERABLES / EXPECTED_FILES[0][1])
    module.__dict__["__name__"] = module.__name__
    exec(compile(raw, module.__file__, "exec"), module.__dict__)
    doc = module.contract_document()
    module.validate_contract(doc)
    need(all(value == 0 for value in doc["formal_credit"].values()), "P1 zero credit")
    return module


def raw_expected(p1: types.ModuleType) -> tuple[dict[str, Any], ...]:
    with p1.HeldInputs() as held:
        structure = held.validate_selected_documents()
        geometry = p1._load_preserved_geometry(held)
        expanded = p1._load_r266_expanded(held, geometry)
        registry_by_row, registry_by_member = p1._load_preserved_registry(held, expanded)
        preserved = p1._load_preserved_b0(held, registry_by_row)
        nodes = p1._load_non_graph_sources(held)
        lineage = p1._validate_non_graph_lineage(held, nodes)
        non_graph = p1._load_non_graph_r266_b0(held, nodes)
        scope = set(preserved) | set(non_graph)
        need(set(preserved).isdisjoint(non_graph) and len(scope) == 144_296, "raw scope")
        b0: dict[str, dict[str, Any]] = {}
        for row in p1.direct_rows(held, "B0", "member_support_source_rows"):
            member = row.get("member_id")
            if member not in scope:
                continue
            p1.row_digest(row)
            need(member not in b0, "duplicate selected B0")
            b0[member] = {"row_id": row["Round306B0_member_support_source_row_id"], "row_sha256": row["row_sha256"], "primary_source_package": row["primary_source_package"], "primary_source_row_id": row["primary_source_row_id"], "primary_source_row_sha256": row["primary_source_row_sha256"], "identity_tranche": row["identity_tranche"]}
        need(set(b0) == scope, "B0 scope anti-join")

        aliases: list[dict[str, Any]] = []
        all_owners: set[tuple[str, str]] = set()
        residual = 0
        kinds: Counter[str] = Counter()
        r294_targets: set[str] = set()
        for row in p1.direct_rows(held, "R294_ALIAS", "rows"):
            p1.row_digest(row)
            owner = (row["alias_source_kind"], row["source_representation_id"])
            need(owner not in all_owners, "R294 owner unique")
            all_owners.add(owner)
            target = row["target_registry_occurrence_id"]
            if target not in preserved:
                residual += 1
                continue
            need(target in registry_by_member, "R294 preserved target")
            kind = row["support_representation_kind"]
            kinds[kind] += 1
            r294_targets.add(target)
            aliases.append({"owner_member_id": target, "source_kind": row["alias_source_kind"], "source_representation_id": row["source_representation_id"], "source_row_id": row["Round294_occurrence_representation_binding_row_id"], "source_row_sha256": row["row_sha256"], "representation_semantics": kind, "geometry_payload": r294_geometry_payload(row)})
        need(len(all_owners) == 46_288 and residual == 7_288 and len(aliases) == 39_000, "R294 dispatch")
        r295_owners: set[str] = set()
        r295_targets: set[str] = set()
        for row in p1.direct_rows(held, "R295A_ALIAS", "rows"):
            p1.row_digest(row)
            target_row = registry_by_row.get(row["target_Round294_occurrence_registry_row_id"])
            target = row["target_Round294_registry_occurrence_id"]
            need(target_row is not None and target == target_row["member_id"] and target in preserved, "R295 target")
            need(row["target_Round294_occurrence_registry_row_sha256"] == target_row["row_sha256"], "R295 target SHA")
            owner = row["source_Round179_retained_child_row_id"]
            need(owner not in r295_owners, "R295 owner unique")
            r295_owners.add(owner)
            r295_targets.add(target)
            aliases.append({"owner_member_id": target, "source_kind": "R295A_ROUND179_ADJACENT_POSITIVE_T_CONTINUATION", "source_representation_id": owner, "source_row_id": row["Round295A_retained_continuation_alias_row_id"], "source_row_sha256": row["row_sha256"], "representation_semantics": "ADJACENT_POSITIVE_T_CONTINUATION", "geometry_payload": {"support_representation_kind": "ADJACENT_POSITIVE_T_CONTINUATION", "retained_positive_t_open_box": row["retained_positive_t_open_box"]}})
        need(len(r295_owners) == len(r295_targets) == 276 and r294_targets.isdisjoint(r295_targets), "R295 census/disjoint")
        kinds["ADJACENT_POSITIVE_T_CONTINUATION"] = 276
        need(dict(kinds) == ALIAS_KIND_COUNTS, "alias kinds")
        held.finalize()
        raw_pins = list(held.rows)
        structure_sha = p1.digest(structure)
    return preserved, non_graph, geometry, registry_by_member, nodes, b0, aliases, lineage, {"P1_input_pins": raw_pins, "P1_structure_rows_sha256": structure_sha}


def closed(body: dict[str, Any]) -> dict[str, Any]:
    return {**body, "row_sha256": digest(body)}


def r294_geometry_payload(row: dict[str, Any]) -> dict[str, Any]:
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


def expected_rows(raw: tuple[dict[str, Any], ...]) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], str]:
    preserved, non_graph, geometry, registry, nodes, b0, aliases, _lineage, audit = raw
    members: list[dict[str, Any]] = []
    reps: list[dict[str, Any]] = []
    primary_ids: set[str] = set()
    alias_ids: set[str] = set()
    global_raw_commitment = digest({
        "schema": SCHEMA + ".global-raw-input-commitment.v1",
        "anchor_pins": [
            {"label": label, "filename": filename, "exact_size": size, "sha256": sha}
            for label, filename, size, sha in EXPECTED_FILES[:3]
        ],
        "P1_replay_audit": audit,
    })
    for member in sorted(set(preserved) | set(non_graph), key=lambda value: value.encode("ascii")):
        is_preserved = member in preserved
        source = preserved[member] if is_preserved else non_graph[member]
        direct = geometry[member] if is_preserved else nodes[member]
        fine = source["family"]
        coarse = "PRESERVED" if is_preserved else "NON_GRAPH"
        box_sha = digest(source["box"])
        direct_package = "R" + fine[5:8] if fine.startswith("ROUND") else fine.split("_")[0]
        primary_input_commitment = {
            "schema": SCHEMA + ".primary-input-commitment.v1",
            "global_raw_input_commitment_sha256": global_raw_commitment,
            "member_id": member,
            "coarse_family": coarse,
            "fine_family": fine,
            "source_B0_row_id": b0[member]["row_id"],
            "source_B0_row_sha256": b0[member]["row_sha256"],
            "primary_source_package": b0[member]["primary_source_package"],
            "primary_source_row_id": b0[member]["primary_source_row_id"],
            "primary_source_row_sha256": b0[member]["primary_source_row_sha256"],
            "direct_construction_package": direct_package,
            "direct_construction_row_id": member,
            "direct_construction_row_sha256": direct["row_sha256"],
            "exact_geometry_payload_sha256": box_sha,
        }
        primary_input_sha = digest(primary_input_commitment)
        rep_id = "k2i2-primary:" + primary_input_sha
        need(rep_id not in primary_ids, "expected primary uniqueness")
        primary_ids.add(rep_id)
        b0row = b0[member]
        sha_mode = "DECLARED_OR_RECOMPUTED_ROW_SHA256" if fine not in ("ROUND174_RESOLVED", "ROUND179_RESOLVED") else "RECOMPUTED_PACKED_ROW_SHA256_UNDER_WHOLE_FILE_PIN"
        members.append(closed({"schema": SCHEMA + ".member-row", "status": "IDENTITY_JOINED_ENGINEERING_ONLY", "coarse_family": coarse, "fine_family": fine, "member_id": member, "primary_representation_id": rep_id, "source_B0_row_id": b0row["row_id"], "source_B0_row_sha256": b0row["row_sha256"], "primary_source_package": b0row["primary_source_package"], "primary_source_row_id": b0row["primary_source_row_id"], "primary_source_row_sha256": b0row["primary_source_row_sha256"], "direct_construction_package": direct_package, "direct_construction_row_id": member, "direct_construction_row_sha256": direct["row_sha256"], "direct_row_sha_authority_mode": sha_mode, "exact_geometry_payload_sha256": box_sha, "input_commitment_sha256": primary_input_sha, "global_raw_input_commitment_sha256": global_raw_commitment, "authority_priority": "EXACT_CONSTRUCTION_ROW>DIRECT_LINEAGE>IDENTITY_BINDING>PROMOTION_SUMMARY>WITNESS_OR_ENVELOPE", "support_semantics": "MECHANICAL_IDENTITY_AND_PAYLOAD_HANDLE_ONLY__FULL_SUPPORT_NOT_PROVED", "formal_credit": dict(ZERO_CREDIT)}))
        reps.append(closed({"schema": SCHEMA + ".representation-row", "status": "OWNER_INDEXED_ENGINEERING_ONLY", "representation_id": rep_id, "representation_role": "PRIMARY_ENGINEERING_HANDLE", "representation_semantics": "DIRECT_CONSTRUCTION_PAYLOAD_HANDLE__SET_EQUALITY_NOT_PROVED", "owner_member_id": member, "owner_coarse_family": coarse, "owner_fine_family": fine, "source_row_id": member, "source_row_sha256": direct["row_sha256"], "exact_geometry_payload_sha256": box_sha, "input_commitment_sha256": primary_input_sha, "global_raw_input_commitment_sha256": global_raw_commitment, "row_sha_authority_mode": sha_mode, "formal_feature_row": False, "formal_credit": dict(ZERO_CREDIT)}))
    for alias in sorted(aliases, key=lambda row: (row["source_kind"].encode("ascii"), row["source_representation_id"].encode("ascii"))):
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
        alias_input_sha = digest(alias_input_commitment)
        rep_id = "k2i2-alias:" + alias_input_sha
        need(rep_id not in primary_ids and rep_id not in alias_ids, "expected alias uniqueness")
        alias_ids.add(rep_id)
        reps.append(closed({"schema": SCHEMA + ".representation-row", "status": "OWNER_INDEXED_ENGINEERING_ONLY", "representation_id": rep_id, "representation_role": "PRESERVED_ALIAS_HANDLE", "representation_semantics": alias["representation_semantics"], "owner_member_id": owner, "owner_coarse_family": "PRESERVED", "source_kind": alias["source_kind"], "source_representation_id": alias["source_representation_id"], "source_row_id": alias["source_row_id"], "source_row_sha256": alias["source_row_sha256"], "target_R294_registry_row_id": target_registry["row_id"], "target_R294_registry_row_sha256": target_registry["row_sha256"], "owner_source_B0_row_id": b0[owner]["row_id"], "owner_source_B0_row_sha256": b0[owner]["row_sha256"], "exact_geometry_payload_sha256": alias_box_sha, "input_commitment_sha256": alias_input_sha, "global_raw_input_commitment_sha256": global_raw_commitment, "row_sha_authority_mode": "DECLARED_ROW_SHA256_RECOMPUTED_UNDER_WHOLE_FILE_PIN", "coverage_semantics": "ALIAS_OR_SUBCOVER_EVIDENCE_ONLY__COMPLETE_SUPPORT_SET_EQUALITY_NOT_PROVED", "formal_feature_row": False, "formal_credit": dict(ZERO_CREDIT)}))
    reps.sort(key=lambda row: row["representation_id"].encode("ascii"))
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
        gap_input = {"schema": SCHEMA + ".gap-input-commitment.v1", "global_raw_input_commitment_sha256": global_raw_commitment, "gap_body": body}
        gap_input_sha = digest(gap_input)
        gaps.append(closed({"schema": SCHEMA + ".gap-row", **body, "gap_handle_id": "k2i2-gap:" + gap_input_sha, "input_commitment_sha256": gap_input_sha, "global_raw_input_commitment_sha256": global_raw_commitment}))
    need(len(members) == 144_296 and len(reps) == 183_572 and len(gaps) == 6, "expected output census")
    return members, reps, gaps, global_raw_commitment


def verify_jsonl(package: HeldPackage, label: str, expected: list[dict[str, Any]]) -> dict[str, Any]:
    raw_hash = hashlib.sha256()
    raw_size = 0
    count = 0
    with package.binary(label) as raw:
        with gzip.GzipFile(fileobj=raw, mode="rb") as zipped:
            for line in zipped:
                need(line.endswith(b"\n") and line != b"\n", label + ":line grammar")
                need(len(line) - 1 <= MAX_ROW, label + ":line cap")
                value = decode(line[:-1])
                need(canonical(value) + b"\n" == line, label + ":canonical wire")
                need(count < len(expected), label + ":extra row")
                strict_equal(value, expected[count], label + f"[{count}]")
                body = dict(value)
                claimed = body.pop("row_sha256")
                need(type(claimed) is str and HEX64.fullmatch(claimed) is not None and digest(body) == claimed, label + ":row closure")
                raw_hash.update(line)
                raw_size += len(line)
                count += 1
    need(count == len(expected), label + ":row count")
    return {"filename": next(row[1] for row in EXPECTED_FILES if row[0] == label), "row_count": count, "uncompressed_jsonl_size": raw_size, "uncompressed_jsonl_sha256": raw_hash.hexdigest(), "file_size": next(row[2] for row in EXPECTED_FILES if row[0] == label), "file_sha256": next(row[3] for row in EXPECTED_FILES if row[0] == label)}


def attacks(result: dict[str, Any]) -> dict[str, Any]:
    rejected: list[str] = []
    pairs = [(False, 0, "false_left"), (0, False, "false_right"), (True, 1, "true_left"), (1, True, "true_right")]
    for left, right, label in pairs:
        try:
            strict_equal(left, right, label)
        except Rejected:
            rejected.append(label)
    mutations: list[tuple[str, Any, Any]] = [
        ("formal", result["formal_credit"]["B1A"], 1),
        ("formal_bool", result["formal_credit"]["B1A"], False),
        ("member_count", result["exact_census"]["member_count"], 144_295),
        ("rep_count", result["exact_census"]["representation_candidate_count"], 183_571),
        ("seed", result["seed_affects_output"], True),
    ]
    for label, observed, bad in mutations:
        try:
            strict_equal(bad, observed, label)
        except Rejected:
            rejected.append(label)
    need(len(rejected) == len(pairs) + len(mutations), "attack rejection census")
    raw_a = digest({"B0_sha256": "0" * 64, "source_sha256": "1" * 64})
    raw_b = digest({"B0_sha256": "0" * 64, "source_sha256": "2" * 64})
    need(raw_a != raw_b, "different raw commitments must have different digests")
    commitment = {"global": "g", "B0": "b", "source": "s", "target": "t", "alias": "a", "payload": "p"}
    commitment_digest = digest(commitment)
    commitment_field_mutations_rejected = 0
    for field in commitment:
        mutated = dict(commitment)
        mutated[field] += "!"
        need(digest(mutated) != commitment_digest, "commitment field not bound:" + field)
        commitment_field_mutations_rejected += 1
    return {"schema": SCHEMA + ".attack-suite.v1", "status": "PASS_ALL_COHERENT_MUTATIONS_REJECTED", "rejected_count": len(rejected), "rejected": rejected, "false_equals_zero_rejected_both_directions": True, "true_equals_one_rejected_both_directions": True, "different_raw_commitments_have_different_digests": True, "commitment_field_mutations_rejected": commitment_field_mutations_rejected, "formal_credit": 0}


def verify() -> tuple[dict[str, Any], dict[str, Any]]:
    with HeldPackage() as package:
        result_raw = package.bytes("RESULT")
        result = decode(result_raw)
        need(canonical(result) + b"\n" == result_raw, "result canonical wire")
        p1 = load_p1(package.bytes("P1"))
        raw = raw_expected(p1)
        members, reps, gaps, global_raw_commitment = expected_rows(raw)
        member_meta = verify_jsonl(package, "MEMBER", members)
        rep_meta = verify_jsonl(package, "REPRESENTATION", reps)
        gap_meta = verify_jsonl(package, "GAP", gaps)
        # Complete exact result reconstruction.  Candidate-declared hashes are
        # accepted only after the corresponding held bytes and uncompressed
        # canonical rows were independently checked above.
        expected_ledgers = {
            "member": {**member_meta, "order": "unsigned_bytewise_ASCII_member_id"},
            "representation": {**rep_meta, "order": "unsigned_bytewise_ASCII_representation_id"},
            "gap": {**gap_meta, "order": "gap_id"},
        }
        fine = Counter(row["fine_family"] for row in members)
        expected = {
            "schema": SCHEMA,
            "status": STATUS,
            "scope": "PRESERVED_AND_NON_GRAPH_PARTIAL_LANE",
            "producer_sha256": None,
            "producer_byte_binding": "EXTERNAL_INDEPENDENT_VERIFIER_STATIC_PIN_ONLY",
            "seed_affects_output": False,
            "P1_execution_disclosure": "HELD_STATIC_P1_SOURCE_SNAPSHOT_EXECUTED_FOR_RAW_JOIN_REUSE__NOT_AN_INDEPENDENT_MATH_IMPLEMENTATION",
            "anchor_pins": [
                {"label": label, "filename": filename, "exact_size": size, "sha256": sha, "pass1_sha256": sha, "pass2_sha256": sha, "final_path_bound": True}
                for label, filename, size, sha in EXPECTED_FILES[:3]
            ],
            "P1_replay_audit": raw[-1],
            "global_raw_input_commitment_sha256": global_raw_commitment,
            "exact_census": {"member_count": 144_296, "preserved_member_count": 126_468, "non_graph_member_count": 17_828, "representation_candidate_count": 183_572, "preserved_representation_candidate_count": 165_744, "non_graph_representation_candidate_count": 17_828, "primary_representation_count": 144_296, "preserved_alias_representation_count": 39_276, "R294_preserved_alias_count": 39_000, "R295A_preserved_alias_count": 276, "P1_A1_A2_obligation_census_not_feature_rows": 80_092},
            "fine_member_counts": dict(sorted(fine.items())),
            "alias_semantic_counts": dict(sorted(ALIAS_KIND_COUNTS.items())),
            "lineage_replay_counts": raw[-2],
            "closed_anti_joins": {"scope_family_overlap": 0, "selected_members_minus_B0": 0, "B0_selected_minus_members": 0, "R294_preserved_alias_owner_duplicates": 0, "R295A_alias_owner_duplicates": 0, "R294_R295A_target_overlap": 0, "orphan_representation_owner_count": 0, "duplicate_representation_handle_count": 0},
            "ledgers": expected_ledgers,
            "known_gaps": {"normalized_support": 144_296, "representation_set_equality": 183_572, "A1_A2": 80_092, "other_coarse_families_members": 420_196, "global_representation_rows_remaining": 428_332, "K2P0_selected_source_rows_missing_own_sha256": 137_136},
            "formal_credit": dict(ZERO_CREDIT),
        }
        strict_equal(result, expected, "result")
        attack = attacks(result)
        package_rows = package.rows
    verification_body = {"schema": SCHEMA + ".verification.v1", "status": VERIFICATION_STATUS, "candidate_package_pins": package_rows, "producer_imported_or_executed": False, "P1_reuse_is_independent_math_implementation": False, "member_rows_reconstructed": 144_296, "representation_rows_reconstructed": 183_572, "gap_rows_reconstructed": 6, "closed_anti_join_count": 8, "recursive_type_strict_equality": True, "false_equals_zero_rejected_both_directions": True, "true_equals_one_rejected_both_directions": True, "formal_credit": dict(ZERO_CREDIT)}
    return {**verification_body, "verification_sha256": digest(verification_body)}, attack


def publish(output_directory: Path, verification: dict[str, Any], attack: dict[str, Any]) -> None:
    output_directory = Path(os.path.abspath(output_directory))
    named = os.stat(output_directory, follow_symlinks=False)
    need(stat.S_ISDIR(named.st_mode), "output directory")
    outfd = os.open(output_directory, os.O_RDONLY | getattr(os, "O_DIRECTORY", 0) | getattr(os, "O_CLOEXEC", 0) | getattr(os, "O_NOFOLLOW", 0))
    need(dir_identity(named) == dir_identity(os.fstat(outfd)), "output dirfd binding")
    root = "/tmp"
    protected = os.path.realpath(DELIVERABLES)
    need(os.path.realpath(root) == root and outside(root, protected), "explicit /tmp")
    root_named = os.stat(root, follow_symlinks=False)
    need(stat.S_ISDIR(root_named.st_mode), "/tmp directory")
    rootfd = os.open(root, os.O_RDONLY | getattr(os, "O_DIRECTORY", 0) | getattr(os, "O_CLOEXEC", 0) | getattr(os, "O_NOFOLLOW", 0))
    root_held = os.fstat(rootfd)
    need(dir_identity(root_named) == dir_identity(root_held), "/tmp dirfd binding")
    try:
        with tempfile.TemporaryDirectory(prefix="cm2-k2i2-verify-", dir=root) as scratch:
            scratch_real = os.path.realpath(scratch)
            need(os.path.dirname(scratch_real) == root and outside(scratch_real, protected), "receipt scratch placement")
            scratch_named = os.stat(scratch_real, follow_symlinks=False)
            need(stat.S_ISDIR(scratch_named.st_mode), "receipt scratch directory")
            scratchfd = os.open(scratch_real, os.O_RDONLY | getattr(os, "O_DIRECTORY", 0) | getattr(os, "O_CLOEXEC", 0) | getattr(os, "O_NOFOLLOW", 0))
            need(dir_identity(scratch_named) == dir_identity(os.fstat(scratchfd)), "receipt scratch dirfd binding")
            try:
                rows = ((PREFIX + "attack_suite.json", attack), (PREFIX + "verification.json", verification))
                for filename, value in rows:
                    path = Path(scratch_real) / filename
                    path.write_bytes(canonical(value) + b"\n")
                    with path.open("rb") as handle:
                        os.fsync(handle.fileno())
                    staged = os.stat(filename, dir_fd=scratchfd, follow_symlinks=False)
                    need(stat.S_ISREG(staged.st_mode) and staged.st_nlink == 1, "staged receipt")
                    os.replace(filename, filename, src_dir_fd=scratchfd, dst_dir_fd=outfd)
            finally:
                os.close(scratchfd)
        need(dir_identity(named) == dir_identity(os.fstat(outfd)) == dir_identity(os.stat(output_directory, follow_symlinks=False)), "output final binding")
        need(dir_identity(root_held) == dir_identity(os.fstat(rootfd)) == dir_identity(os.stat(root, follow_symlinks=False)), "/tmp final binding")
    finally:
        os.close(rootfd)
        os.close(outfd)


def self_test() -> dict[str, Any]:
    rejected: list[str] = []
    for left, right, label in ((False, 0, "false_left"), (0, False, "false_right"), (True, 1, "true_left"), (1, True, "true_right")):
        try:
            strict_equal(left, right, label)
        except Rejected:
            rejected.append(label)
    need(len(rejected) == 4, "bool/int aliases rejected")
    need(digest({"raw": "a"}) != digest({"raw": "b"}), "input-bound digest regression")
    exact = {"x": "a" * (MAX_ROW - len(canonical({"x": ""})))}
    need(len(canonical(exact)) == MAX_ROW, "exact cap")
    overflow = False
    try:
        canonical({"x": exact["x"] + "a"})
    except Rejected:
        overflow = True
    need(overflow, "cap plus one")
    return {"schema": SCHEMA + ".verifier-self-test", "status": "PASS", "producer_imported_or_executed": False, "false_zero_and_true_one_attacks_rejected": 4, "cap_plus_one_rejected": True, "different_raw_commitments_have_different_digests": True}


def main() -> int:
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--self-test", action="store_true")
    group.add_argument("--verify-publish", action="store_true")
    group.add_argument("--verify-no-write", action="store_true")
    parser.add_argument("--output-directory")
    args = parser.parse_args()
    if args.self_test:
        need(args.output_directory is None, "self-test filesystem inert")
        print(canonical(self_test()).decode("ascii"))
        return 0
    if args.verify_publish:
        need(args.output_directory is not None, "publish output directory required")
    else:
        need(args.verify_no_write and args.output_directory is None, "no-write mode forbids output directory")
    verification, attack = verify()
    if args.verify_publish:
        publish(Path(args.output_directory), verification, attack)
    print(canonical({
        "status": verification["status"],
        "verification_sha256": verification["verification_sha256"],
        "verification_receipt_file_sha256": hashlib.sha256(canonical(verification) + b"\n").hexdigest(),
        "attack_status": attack["status"],
        "attack_receipt_file_sha256": hashlib.sha256(canonical(attack) + b"\n").hexdigest(),
        "mode": "VERIFY_AND_PUBLISH_RECEIPTS" if args.verify_publish else "VERIFY_NO_WRITE",
        "filesystem_write": bool(args.verify_publish),
    }).decode("ascii"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
