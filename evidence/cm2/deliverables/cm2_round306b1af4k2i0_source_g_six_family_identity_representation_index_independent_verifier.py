#!/usr/bin/env python3
"""Independent cold verifier for the K2I0 partial R292 lane.

The verifier does not import or execute the producer.  It reconstructs the
R292 component/cell partition and all owner joins from raw pinned ledgers,
then checks every emitted JSONL row and the explicit zero-credit/gap record.
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
from typing import Any, BinaryIO, Iterator, TextIO


class VerificationBlocked(RuntimeError):
    pass


def need(condition: bool, label: str) -> None:
    if not condition:
        raise VerificationBlocked(label)


def type_strict_equal(actual: Any, expected: Any) -> bool:
    """Recursive equality that never aliases bool with int."""
    if type(actual) is not type(expected):
        return False
    if type(actual) is dict:
        if set(actual) != set(expected):
            return False
        return all(type_strict_equal(actual[key], expected[key]) for key in expected)
    if type(actual) in (list, tuple):
        return len(actual) == len(expected) and all(type_strict_equal(left, right) for left, right in zip(actual, expected))
    return bool(actual == expected)


def strict_need(actual: Any, expected: Any, label: str) -> None:
    need(type_strict_equal(actual, expected), label)


PREFIX = "cm2_round306b1af4k2i0_source_g_six_family_identity_representation_index_"
SCHEMA = "cm2.round306b1af4k2i0.source-g-six-family-identity-representation-index.partial-r292.v1"
DELIVERABLES = Path(__file__).resolve().parent
PRODUCER = PREFIX + "producer.py"
PRODUCER_SHA256 = "035629dda904aae42f877e5425dc17c8500ff3e33b837ecdf8142e0b264233b5"
PRODUCER_SIZE = 37_543
EXPECTED_STATUS = "PASS_PARTIAL_R292_IDENTITY_OWNER_INDEX__ZERO_THEOREM_CREDIT__FIVE_FAMILIES_PENDING"
RESULT = PREFIX + "result.json"
VERIFICATION = PREFIX + "verification.json"
OUTPUT_KEYS = {
    "member": PREFIX + "member_index.jsonl.gz",
    "representation": PREFIX + "representation_index.jsonl.gz",
    "preserved_alias": PREFIX + "preserved_alias_index.jsonl.gz",
    "fixed_sign_obligation": PREFIX + "fixed_sign_obligation_index.jsonl.gz",
}
HEX64 = re.compile(r"^[0-9a-f]{64}$")
MAX_ROW = 8 << 20
CHARS = 1 << 18
BUFFER_CAP = MAX_ROW + 4 * CHARS

RAW_PINS: tuple[tuple[str, str, int, str], ...] = (
    ("AF2_RESULT", "cm2_round306b1af2_source_g_primitive_support_source_partition_primary_result.json", 2_540, "7238c245e79124e5bf3aa14c463fcc639efcde7431b03ac3a1cd035a4d1f7ebb"),
    ("AF4_TYPED_SCHEMA", "cm2_round306b1af4_source_g_normalized_support_representation_typed_schema_contract.py", 80_436, "ee095fe5db22c6a4dd0804eca0fb553a132546367dcb37fcd75733050aa52cf9"),
    ("AF4D1_SEMANTIC_DELTA", "cm2_round306b1af4d1_source_g_semantic_wire_delta_contract.py", 84_392, "5082df54ea4c514de906f4a923856adb20c6240c9be33401e784b2513a85f09f"),
    ("R292", "cm2_round292_source_g_r287_registry_overlap_exhaustion_probe_ledger.json.gz", 5_544_437, "8863126e88ffd30438938d0a8bdb577f5928ae81f3f17f4b506829d59103a8ab"),
    ("R294_REGISTRY", "cm2_round294_source_g_occurrence_registry_atomic_promotion_registry_ledger.json.gz", 262_951_902, "c6b26f13e90072db99fa98f99fc62c77135ff1cbdb23bbbd5bac3e9f64a834bb"),
    ("R294_BINDINGS", "cm2_round294_source_g_occurrence_registry_atomic_promotion_representation_binding_ledger.json.gz", 26_672_326, "f9fcc986771b1c3551420516cd9f2c5dde662f87d044666d9306404f30bb6833"),
    ("B0", "cm2_round306b0_source_g_r306a_universe_support_source_freeze_member_support_source_index.json.gz", 162_499_140, "c9a8649c8473bb6a170187e7f803e95748d2ff2198b1b846d97383dd5f0581af"),
)
EXPECTED_TABLES = {
    "R292": (22_820, "556bd0ed95709fe43ff7837522d8729582ce0e7c9679879a57365f864f6ba055"),
    "R294_REGISTRY": (431_208, "33936ecd04cbce9f9a308b0da10381bd854b45028db53db5d3cbb9aa8b264044"),
    "R294_BINDINGS": (46_288, "ece198bf5e8b95448b09f60061677feafca3416525ba80f3b88a51e766414be7"),
    "B0": (564_492, "c7dfb5534fddeb22fffb81bf539fe44d837aced46577aa5f490a0ae14aba77f5"),
}


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True, allow_nan=False).encode("ascii")


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for key, value in pairs:
        need(key not in out, "duplicate JSON key:" + key)
        out[key] = value
    return out


def reject_number(token: str) -> Any:
    raise VerificationBlocked("nonintegral token:" + token)


DECODER = json.JSONDecoder(object_pairs_hook=unique_object, parse_float=reject_number, parse_constant=reject_number)


def closed(row: dict[str, Any], label: str) -> str:
    need(type(row) is dict and type(row.get("row_sha256")) is str, label + ":closed row")
    body = dict(row)
    claimed = body.pop("row_sha256")
    need(HEX64.fullmatch(claimed) is not None and digest(body) == claimed, label + ":row hash")
    return claimed


def fingerprint(value: os.stat_result) -> tuple[int, ...]:
    return (value.st_dev, value.st_ino, value.st_mode, value.st_nlink, value.st_size, value.st_mtime_ns, value.st_ctime_ns)


def hash_fd(fd: int, limit: int) -> tuple[int, str]:
    total = 0
    offset = 0
    state = hashlib.sha256()
    while True:
        block = os.pread(fd, 1 << 20, offset)
        if not block:
            break
        offset += len(block)
        total += len(block)
        need(total <= limit, "file grew while hashing")
        state.update(block)
    return total, state.hexdigest()


class ListHash:
    def __init__(self) -> None:
        self.state = hashlib.sha256(b"[")
        self.count = 0

    def add(self, value: Any) -> None:
        if self.count:
            self.state.update(b",")
        self.state.update(canonical(value))
        self.count += 1

    def finish(self) -> str:
        state = self.state.copy()
        state.update(b"]")
        return state.hexdigest()


def iter_array(stream: TextIO, marker: str) -> Iterator[Any]:
    def append(buffer: str, label: str) -> str:
        block = stream.read(CHARS)
        need(bool(block), label)
        value = buffer + block
        need(len(value.encode("utf-8")) <= BUFFER_CAP, "parser buffer cap")
        return value

    buffer = ""
    while True:
        at = buffer.find(marker)
        if at >= 0:
            buffer = buffer[at + len(marker):]
            break
        buffer = append(buffer, "missing marker")
        at = buffer.find(marker)
        if at >= 0:
            buffer = buffer[at + len(marker):]
            break
        buffer = buffer[-max(1, len(marker) - 1):]
    stripped = buffer.lstrip()
    if stripped.startswith(":"):
        stripped = stripped[1:].lstrip()
        need(stripped.startswith("["), "marker not array")
        buffer = stripped[1:]
    comma = False
    while True:
        buffer = buffer.lstrip()
        while not buffer:
            buffer = append(buffer, "truncated array")
            buffer = buffer.lstrip()
        if buffer[0] == "]":
            return
        if comma:
            need(buffer[0] == ",", "missing comma")
            buffer = buffer[1:].lstrip()
            while not buffer:
                buffer = append(buffer, "truncated row")
                buffer = buffer.lstrip()
        while True:
            try:
                value, end = DECODER.raw_decode(buffer)
                break
            except json.JSONDecodeError:
                need(len(buffer.encode("utf-8")) <= MAX_ROW, "incomplete row cap")
                buffer = append(buffer, "truncated JSON")
        need(len(buffer[:end].encode("utf-8")) <= MAX_ROW and len(canonical(value)) <= MAX_ROW, "final decoded row cap")
        yield value
        buffer = buffer[end:]
        comma = True


class RawPins:
    def __init__(self) -> None:
        self.dirfd = -1
        self.dir_before: os.stat_result | None = None
        self.files: dict[str, tuple[int, os.stat_result, int, str, str]] = {}
        self.pin_rows: list[dict[str, Any]] = []

    def __enter__(self) -> "RawPins":
        info = os.stat(DELIVERABLES, follow_symlinks=False)
        need(stat.S_ISDIR(info.st_mode), "deliverables directory")
        self.dirfd = os.open(DELIVERABLES, os.O_RDONLY | getattr(os, "O_DIRECTORY", 0) | getattr(os, "O_NOFOLLOW", 0))
        self.dir_before = os.fstat(self.dirfd)
        need((info.st_dev, info.st_ino, info.st_mode) == (self.dir_before.st_dev, self.dir_before.st_ino, self.dir_before.st_mode), "deliverables held-dirfd binding")
        try:
            for label, filename, size, sha in RAW_PINS:
                named = os.stat(filename, dir_fd=self.dirfd, follow_symlinks=False)
                need(stat.S_ISREG(named.st_mode) and named.st_nlink == 1 and named.st_size == size, "raw path pin:" + label)
                fd = os.open(filename, os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0), dir_fd=self.dirfd)
                opened = os.fstat(fd)
                need(fingerprint(named) == fingerprint(opened), "raw open race:" + label)
                n, h = hash_fd(fd, size)
                need(n == size and h == sha, "raw byte pin:" + label)
                self.files[label] = (fd, opened, size, sha, filename)
                self.pin_rows.append({"label": label, "filename": filename, "exact_size": size, "sha256": sha, "pass1_sha256": h, "regular": True, "nlink_one": True})
            return self
        except Exception:
            self.close(False)
            raise

    def rows(self, label: str, marker: str) -> Iterator[dict[str, Any]]:
        fd, before, _, _, filename = self.files[label]
        os.lseek(fd, 0, os.SEEK_SET)
        raw = os.fdopen(os.dup(fd), "rb")
        binary: BinaryIO = gzip.GzipFile(fileobj=raw, mode="rb")
        text = io.TextIOWrapper(binary, encoding="utf-8", newline="")
        try:
            yield from iter_array(text, marker)
        finally:
            text.close()
            if not raw.closed:
                raw.close()
            need(fingerprint(os.fstat(fd)) == fingerprint(before), "raw FD stable:" + label)

    def small_json(self, label: str) -> Any:
        fd, before, size, _, _ = self.files[label]
        need(size <= MAX_ROW, "small JSON cap")
        raw = os.pread(fd, size, 0)
        need(len(raw) == size and fingerprint(os.fstat(fd)) == fingerprint(before), "small JSON held read")
        value = DECODER.decode(raw.decode("utf-8"))
        need(len(canonical(value)) <= MAX_ROW, "small JSON canonical cap")
        return value

    def close(self, verify: bool = True) -> None:
        error: Exception | None = None
        for label, (fd, before, size, sha, filename) in list(self.files.items()):
            try:
                if verify:
                    n, h = hash_fd(fd, size)
                    named = os.stat(filename, dir_fd=self.dirfd, follow_symlinks=False)
                    need(n == size and h == sha and fingerprint(before) == fingerprint(os.fstat(fd)) == fingerprint(named), "raw final rebind:" + label)
                    for row in self.pin_rows:
                        if row["label"] == label:
                            row["pass2_sha256"] = h
                            row["final_path_bound"] = True
            except Exception as exc:
                if error is None:
                    error = exc
            finally:
                os.close(fd)
        self.files.clear()
        if self.dirfd >= 0:
            try:
                if verify:
                    assert self.dir_before is not None
                    held = os.fstat(self.dirfd)
                    named = os.stat(DELIVERABLES, follow_symlinks=False)
                    need((self.dir_before.st_dev, self.dir_before.st_ino, self.dir_before.st_mode) == (held.st_dev, held.st_ino, held.st_mode) == (named.st_dev, named.st_ino, named.st_mode), "deliverables final directory binding")
            except Exception as exc:
                if error is None:
                    error = exc
            finally:
                os.close(self.dirfd)
                self.dirfd = -1
        if error:
            raise error

    def __exit__(self, exc_type: Any, exc: Any, tb: Any) -> None:
        self.close(exc_type is None)


class SealedFile:
    def __init__(self, path: Path, expected_size: int | None = None, expected_sha: str | None = None) -> None:
        self.path = path
        self.expected_size = expected_size
        self.expected_sha = expected_sha
        self.fd = -1
        self.before: os.stat_result | None = None

    def __enter__(self) -> "SealedFile":
        named = os.stat(self.path, follow_symlinks=False)
        need(stat.S_ISREG(named.st_mode) and named.st_nlink == 1, "sealed regular single-link:" + self.path.name)
        if self.expected_size is not None:
            need(named.st_size == self.expected_size, "sealed size:" + self.path.name)
        self.fd = os.open(self.path, os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0))
        self.before = os.fstat(self.fd)
        need(fingerprint(named) == fingerprint(self.before), "sealed open race:" + self.path.name)
        n, h = hash_fd(self.fd, named.st_size)
        if self.expected_sha is not None:
            need(h == self.expected_sha, "sealed sha:" + self.path.name)
        self.expected_size = n
        self.expected_sha = h
        return self

    def bytes(self) -> bytes:
        assert self.expected_size is not None
        return os.pread(self.fd, self.expected_size, 0)

    def jsonl(self) -> Iterator[dict[str, Any]]:
        raw = os.fdopen(os.dup(self.fd), "rb")
        binary = gzip.GzipFile(fileobj=raw, mode="rb")
        text = io.TextIOWrapper(binary, encoding="ascii", newline="")
        try:
            for line in text:
                need(len(line.encode("ascii")) <= MAX_ROW + 1, "output JSONL line cap")
                need(line.endswith("\n"), "output JSONL newline")
                row = DECODER.decode(line[:-1])
                need(canonical(row) == line[:-1].encode("ascii"), "output canonical JSONL")
                yield row
        finally:
            text.close()
            if not raw.closed:
                raw.close()

    def __exit__(self, exc_type: Any, exc: Any, tb: Any) -> None:
        if self.fd >= 0:
            try:
                if exc_type is None:
                    assert self.before is not None and self.expected_size is not None and self.expected_sha is not None
                    n, h = hash_fd(self.fd, self.expected_size)
                    named = os.stat(self.path, follow_symlinks=False)
                    need(n == self.expected_size and h == self.expected_sha and fingerprint(self.before) == fingerprint(os.fstat(self.fd)) == fingerprint(named), "sealed final path binding:" + self.path.name)
            finally:
                os.close(self.fd)


def table_check(label: str, audit: ListHash) -> dict[str, Any]:
    count, sha = EXPECTED_TABLES[label]
    observed = audit.finish()
    need(audit.count == count and observed == sha, label + ":table commitment")
    return {"table": label, "row_count": count, "rows_sha256": sha, "all_rows_own_sha256_checked": True}


def verify() -> dict[str, Any]:
    producer_path = DELIVERABLES / PRODUCER
    with SealedFile(producer_path, PRODUCER_SIZE, PRODUCER_SHA256):
        pass
    with SealedFile(DELIVERABLES / RESULT) as result_file:
        result_raw = result_file.bytes()
        need(len(result_raw) <= MAX_ROW and result_raw.endswith(b"\n"), "result wire")
        result = DECODER.decode(result_raw[:-1].decode("ascii"))
        need(canonical(result) + b"\n" == result_raw, "canonical result")
        result_file_sha256 = result_file.expected_sha
    need(set(result) == {"schema", "status", "scope", "producer_sha256", "producer_byte_binding", "seed_affects_output", "input_pins", "source_table_commitments", "exact_census", "ledgers", "closed_anti_joins", "known_gaps", "formal_credit"}, "exact result schema keys")
    need(set(result["ledgers"]) == set(OUTPUT_KEYS), "exact ledger receipt keys")
    need(result["schema"] == SCHEMA and result["status"] == EXPECTED_STATUS and result["scope"] == "R292_ONLY_PARTIAL_LANE", "result scope/status")
    need(result["producer_sha256"] is None and result["producer_byte_binding"] == "EXTERNAL_INDEPENDENT_VERIFIER_STATIC_PIN_ONLY" and result["seed_affects_output"] is False, "producer/result binding")
    expected_credit = {"normalized_support": 0, "representation_cover": 0, "A1_A2": 0, "B1A": 0, "B2": 0, "maximality": 0, "fibre": 0, "global_disposition": 0, "D02": 0, "D03": 0, "D04": 0, "Gate5": 0, "CM2": 0}
    strict_need(result["formal_credit"], expected_credit, "result zero credit")
    strict_need(result["known_gaps"], {"fixed_sign_pullback_obligations_not_discharged": 11_852, "R292_physical_face_and_Kruskal_semantic_obligations_not_discharged": 848, "fixed_sign_sigma_branch_authority_missing": 11_852, "remaining_coarse_families_not_emitted": ["PRESERVED", "NON_GRAPH", "R2", "G2A", "G2B"], "remaining_member_identity_rows_not_emitted": 555_088, "remaining_global_representation_rows_not_emitted": 600_052, "A1_A2_obligations_not_enumerated_in_this_lane": 80_092}, "explicit gap ledger")

    cells: dict[str, dict[str, Any]] = {}
    components: dict[str, dict[str, Any]] = {}
    registry: dict[str, dict[str, Any]] = {}
    b0: dict[str, dict[str, str]] = {}
    aliases: dict[str, dict[str, str]] = {}
    table_rows: list[dict[str, Any]] = []
    shapes: Counter[str] = Counter()
    with RawPins() as pins:
        af2 = pins.small_json("AF2_RESULT")
        need(type_strict_equal(af2["member_count"], 564_492) and type_strict_equal(af2["coarse_partition"]["R292_transformed_cell_union_members"], 9_404) and type_strict_equal(af2["formal_credit"], 0), "AF2 denominator/credit")
        audit = ListHash()
        for row in pins.rows("R292", '"rows"'):
            closed(row, "R292")
            audit.add(row)
            if "Round292_R287_existing_overlap_refinement_cell_id" in row:
                shapes["cell"] += 1
                cid = row["Round292_R287_existing_overlap_refinement_cell_id"]
                need(cid not in cells and row["exact_transformed_coordinate_system"] == "(t^2,p,s)", "unique T2PS cell")
                occ = row["existing_occurrence_occupancy_count"]
                owners = row["existing_occurrence_ids"]
                comp = row["Round292_refined_new_support_component_id"]
                need((occ == 0 and owners == [] and type(comp) is str) or (occ == 1 and len(owners) == 1 and comp is None), "cell occupancy partition")
                cells[cid] = {"sha": row["row_sha256"], "component": comp, "owner": owners[0] if owners else None, "chart": row["source_chart"], "signature": row["complete_10_field_return_signature_sha256"], "exact_transformed_open_cell": row["exact_transformed_open_cell"]}
            elif "member_refinement_cell_ids" in row:
                shapes["component"] += 1
                comp = row["Round292_refined_new_support_component_id"]
                ids = row["member_refinement_cell_ids"]
                need(comp not in components and len(ids) == row["member_refinement_cell_count"] and len(ids) == len(set(ids)) and ids, "component row")
                components[comp] = {"sha": row["row_sha256"], "cells": tuple(ids)}
            else:
                need("Round292_registry_overlap_row_id" in row, "known R292 shape")
                shapes["overlap"] += 1
        table_rows.append(table_check("R292", audit))
        need(shapes == Counter({"overlap": 1_564, "cell": 11_852, "component": 9_404}), "R292 shape count")
        uncovered = {cid for cid, data in cells.items() if data["component"] is not None}
        occupied = set(cells) - uncovered
        seen: set[str] = set()
        for comp, data in components.items():
            for cid in data["cells"]:
                need(cid in cells and cells[cid]["component"] == comp and cid not in seen, "component/cell exact join")
                seen.add(cid)
        need(seen == uncovered and len(uncovered) == 10_252 and len(occupied) == 1_600, "cell anti-join")

        audit = ListHash()
        for row in pins.rows("R294_REGISTRY", '"rows"'):
            closed(row, "R294 registry")
            audit.add(row)
            if row["registry_entry_kind"] != "CANDIDATE_NEW_ROUND292_REFINED_R287_SUPPORT_COMPONENT":
                continue
            comp = row["source_row_id"]
            need(comp in components and row["source_row_sha256"] == components[comp]["sha"], "registry component source")
            embedded = {entry["Round292_refinement_cell_id"] for entry in row["member_refinement_cells"]}
            need(embedded == set(components[comp]["cells"]), "registry embedded cells")
            rid = row["Round294_occurrence_registry_row_id"]
            need(rid not in registry, "duplicate registry row")
            registry[rid] = {"sha": row["row_sha256"], "member": row["registry_occurrence_id"], "component": comp}
            components[comp]["registry"] = rid
            components[comp]["member"] = row["registry_occurrence_id"]
        table_rows.append(table_check("R294_REGISTRY", audit))
        need(len(registry) == 9_404 and all("member" in value for value in components.values()), "registry exhaustion")

        audit = ListHash()
        for row in pins.rows("B0", '"member_support_source_rows"'):
            closed(row, "B0")
            audit.add(row)
            rid = row["primary_source_row_id"]
            if rid not in registry:
                continue
            source = registry[rid]
            need(row["primary_source_package"] == "R294" and row["primary_source_row_sha256"] == source["sha"] and row["member_id"] == source["member"], "B0 registry join")
            need(row["identity_tranche"] == "CANDIDATE_NEW_ROUND292_REFINED_R287_SUPPORT_COMPONENT" and rid not in b0, "B0 R292 tranche")
            b0[rid] = {"id": row["Round306B0_member_support_source_row_id"], "sha": row["row_sha256"]}
        table_rows.append(table_check("B0", audit))
        need(set(b0) == set(registry), "B0 registry anti-join")

        audit = ListHash()
        for row in pins.rows("R294_BINDINGS", '"rows"'):
            closed(row, "R294 binding")
            audit.add(row)
            if row["support_representation_kind"] != "EXACT_T2_P_S_EXISTING_OCCURRENCE_SUBCOVER_CELL":
                continue
            cid = row["source_representation_id"]
            need(cid in occupied and row["source_row_id"] == cid and row["source_row_sha256"] == cells[cid]["sha"], "alias cell source")
            need(row["target_registry_occurrence_id"] == cells[cid]["owner"] and cid not in aliases, "alias owner")
            aliases[cid] = {"id": row["Round294_occurrence_representation_binding_row_id"], "sha": row["row_sha256"], "owner": row["target_registry_occurrence_id"]}
        table_rows.append(table_check("R294_BINDINGS", audit))
        need(set(aliases) == occupied, "alias occupied anti-join")

        independent_pin_rows = pins.pin_rows

    strict_need(result["input_pins"], independent_pin_rows, "result input pin receipt")
    strict_need(result["source_table_commitments"], table_rows, "result source table receipts")
    component_histogram = Counter(len(value["cells"]) for value in components.values())
    expected_census = {
        "R292_member_count": 9_404,
        "R292_uncovered_representation_cell_count": 10_252,
        "R292_primary_representation_count": 9_404,
        "R292_refined_primary_extra_count": 848,
        "R292_preserved_owner_alias_count": 1_600,
        "R292_fixed_sign_obligation_count": 11_852,
        "component_size_histogram": {str(key): value for key, value in sorted(component_histogram.items())},
        "primary_selection_rule": "MIN_UNSIGNED_BYTEWISE_ASCII_CELL_ID_PER_COMPONENT",
    }
    strict_need(result["exact_census"], expected_census, "result exact census receipt")
    expected_anti_joins = {"uncovered_cells_minus_component_members": 0, "component_members_minus_uncovered_cells": 0, "components_minus_R294_registry": 0, "R294_registry_minus_B0": 0, "occupied_cells_minus_R294_aliases": 0, "R294_T2PS_aliases_minus_occupied_cells": 0, "duplicate_member_ids": 0, "duplicate_representation_cell_ids_within_R292_new_lane": 0, "orphan_owner_count": 0}
    strict_need(result["closed_anti_joins"], expected_anti_joins, "result anti-join receipt")

    observed_meta: dict[str, dict[str, Any]] = {}
    seen_members: set[str] = set()
    seen_new_cells: set[str] = set()
    seen_alias_cells: set[str] = set()
    seen_obligation_cells: set[str] = set()
    primary = extra = 0
    expected_counts = {"member": 9_404, "representation": 10_252, "preserved_alias": 1_600, "fixed_sign_obligation": 11_852}
    for key, filename in OUTPUT_KEYS.items():
        meta = result["ledgers"][key]
        need(set(meta) == {"filename", "row_count", "uncompressed_jsonl_size", "uncompressed_jsonl_sha256", "file_size", "file_sha256", "order"}, "exact ledger metadata schema:" + key)
        need(meta["order"] == "unsigned_bytewise_ASCII_by_primary_row_id", "ledger order contract:" + key)
        need(type_strict_equal(meta["filename"], filename) and type_strict_equal(meta["row_count"], expected_counts[key]), "result ledger metadata:" + key)
        need(type(meta["file_size"]) is int and meta["file_size"] > 0 and type(meta["uncompressed_jsonl_size"]) is int and meta["uncompressed_jsonl_size"] > 0, "ledger strict integer sizes:" + key)
        need(type(meta["file_sha256"]) is str and HEX64.fullmatch(meta["file_sha256"]) is not None and type(meta["uncompressed_jsonl_sha256"]) is str and HEX64.fullmatch(meta["uncompressed_jsonl_sha256"]) is not None, "ledger strict digest fields:" + key)
        with SealedFile(DELIVERABLES / filename, meta["file_size"], meta["file_sha256"]) as sealed:
            raw_state = hashlib.sha256()
            raw_size = count = 0
            last_id: str | None = None
            for row in sealed.jsonl():
                closed(row, "output " + key)
                wire = canonical(row) + b"\n"
                raw_state.update(wire)
                raw_size += len(wire)
                count += 1
                if key == "member":
                    need(set(row) == {"schema", "status", "coarse_family", "member_id", "component_id", "primary_representation_cell_id", "representation_cell_count", "source_R292_component_row_sha256", "source_R294_registry_row_id", "source_R294_registry_row_sha256", "source_B0_row_id", "source_B0_row_sha256", "formal_credit", "row_sha256"} and row["schema"] == SCHEMA + ".member-row", "exact member row schema")
                    comp = row["component_id"]
                    need(comp in components, "member component")
                    source = components[comp]
                    rid = source["registry"]
                    expected_primary = min(source["cells"], key=lambda value: value.encode("ascii"))
                    need(row["status"] == "IDENTITY_JOINED" and row["coarse_family"] == "R292" and row["member_id"] == source["member"], "member identity")
                    need(row["primary_representation_cell_id"] == expected_primary and type_strict_equal(row["representation_cell_count"], len(source["cells"])), "member representation selection")
                    need(row["source_R292_component_row_sha256"] == source["sha"] and row["source_R294_registry_row_id"] == rid and row["source_R294_registry_row_sha256"] == registry[rid]["sha"], "member source joins")
                    need(row["source_B0_row_id"] == b0[rid]["id"] and row["source_B0_row_sha256"] == b0[rid]["sha"], "member B0 join")
                    strict_need(row["formal_credit"], {"normalized_support": 0, "representation_cover": 0, "A1_A2": 0, "B1A": 0, "B2": 0, "D02": 0, "CM2": 0}, "member zero credit")
                    row_id = comp
                    need(row["member_id"] not in seen_members, "duplicate output member")
                    seen_members.add(row["member_id"])
                elif key == "representation":
                    need(set(row) == {"schema", "status", "representation_role", "coverage_semantics", "representation_cell_id", "owner_member_id", "source_R292_cell_row_sha256", "source_R292_component_id", "source_R292_component_row_sha256", "formal_credit", "row_sha256"} and row["schema"] == SCHEMA + ".representation-row", "exact representation row schema")
                    cid = row["representation_cell_id"]
                    need(cid in uncovered and cid not in seen_new_cells, "new representation cell")
                    comp = cells[cid]["component"]
                    source = components[comp]
                    expected_role = "PRIMARY" if cid == min(source["cells"], key=lambda value: value.encode("ascii")) else "REFINED_PRIMARY_EXTRA"
                    need(row["status"] == "OWNER_INDEXED" and row["representation_role"] == expected_role and row["owner_member_id"] == source["member"], "representation role/owner")
                    need(row["coverage_semantics"] == "IDENTITY_AND_OWNER_ONLY__SET_EQUALITY_NOT_PROVED", "representation non-credit semantics")
                    need(row["source_R292_cell_row_sha256"] == cells[cid]["sha"] and row["source_R292_component_id"] == comp and row["source_R292_component_row_sha256"] == source["sha"], "representation sources")
                    strict_need(row["formal_credit"], {"normalized_support": 0, "representation_cover": 0, "physical_incidence": 0, "pullback_equivalence": 0}, "representation zero credit")
                    primary += expected_role == "PRIMARY"
                    extra += expected_role != "PRIMARY"
                    seen_new_cells.add(cid)
                    row_id = cid
                elif key == "preserved_alias":
                    need(set(row) == {"schema", "status", "representation_role", "coverage_semantics", "representation_cell_id", "owner_member_id", "source_R292_cell_row_sha256", "source_R294_binding_row_id", "source_R294_binding_row_sha256", "formal_credit", "row_sha256"} and row["schema"] == SCHEMA + ".preserved-alias-row", "exact alias row schema")
                    cid = row["representation_cell_id"]
                    need(cid in aliases and cid not in seen_alias_cells, "alias output cell")
                    source = aliases[cid]
                    need(row["status"] == "OWNER_INDEXED" and row["representation_role"] == "ALIAS_EXISTING_MEMBER" and row["coverage_semantics"] == "PARTIAL_INCLUSION_ONLY__NOT_FULL_SET_EQUALITY", "alias semantics")
                    need(row["owner_member_id"] == source["owner"] and row["source_R292_cell_row_sha256"] == cells[cid]["sha"] and row["source_R294_binding_row_id"] == source["id"] and row["source_R294_binding_row_sha256"] == source["sha"], "alias source/owner")
                    strict_need(row["formal_credit"], {"normalized_support": 0, "representation_cover": 0, "member_identity_minted": 0}, "alias zero credit")
                    seen_alias_cells.add(cid)
                    row_id = cid
                else:
                    need(set(row) == {"schema", "status", "obligation_kind", "representation_cell_id", "owner_member_id", "owner_disposition", "source_chart", "exact_transformed_open_cell", "complete_10_field_return_signature_sha256", "source_R292_cell_row_sha256", "geometry_payload_backbinding", "sigma_branch_authority_status", "formal_feature_row", "formal_credit", "row_sha256"} and row["schema"] == SCHEMA + ".fixed-sign-obligation-row", "exact obligation row schema")
                    cid = row["representation_cell_id"]
                    need(cid in cells and cid not in seen_obligation_cells, "obligation output cell")
                    expected_owner = components[cells[cid]["component"]]["member"] if cid in uncovered else aliases[cid]["owner"]
                    expected_disposition = "NEW_R292_COMPONENT_REPRESENTATION" if cid in uncovered else "PRESERVED_OWNER_ALIAS_REPRESENTATION"
                    need(row["status"] == "OBLIGATION_ENUMERATED_NOT_DISCHARGED" and row["formal_feature_row"] is False, "obligation zero theorem status")
                    need(row["obligation_kind"] == "FIXED_SIGN_T2PS_PULLBACK_t_EQUALS_sigma_sqrt_u__u_EQUALS_t_squared" and row["source_R292_cell_row_sha256"] == cells[cid]["sha"], "obligation kind/source")
                    need(row["owner_member_id"] == expected_owner and row["owner_disposition"] == expected_disposition and row["source_chart"] == cells[cid]["chart"] and row["complete_10_field_return_signature_sha256"] == cells[cid]["signature"], "obligation source/owner")
                    need(row["exact_transformed_open_cell"] == cells[cid]["exact_transformed_open_cell"] and row["geometry_payload_backbinding"] == "EXACT_CELL_PAYLOAD_PLUS_SOURCE_ROW_SHA256" and row["sigma_branch_authority_status"] == "MISSING_NOT_DISCHARGED", "obligation geometry/gap payload")
                    strict_need(row["formal_credit"], {"pullback_equivalence": 0, "fixed_sign": 0, "normalized_support": 0, "representation_cover": 0}, "obligation zero credit")
                    seen_obligation_cells.add(cid)
                    row_id = cid
                need(last_id is None or last_id.encode("ascii") < row_id.encode("ascii"), "strict output order:" + key)
                last_id = row_id
            need(count == expected_counts[key] and type_strict_equal(meta["uncompressed_jsonl_size"], raw_size) and type_strict_equal(meta["uncompressed_jsonl_sha256"], raw_state.hexdigest()), "ledger stream commitment:" + key)
            observed_meta[key] = {"filename": filename, "row_count": count, "file_size": meta["file_size"], "file_sha256": meta["file_sha256"], "uncompressed_jsonl_size": raw_size, "uncompressed_jsonl_sha256": raw_state.hexdigest()}
    need(seen_members == {value["member"] for value in components.values()}, "output member exhaustion")
    need(seen_new_cells == uncovered and seen_alias_cells == occupied and seen_obligation_cells == set(cells), "output cell exhaustion")
    need(primary == 9_404 and extra == 848, "primary/extra census")

    return {
        "schema": SCHEMA + ".independent-verification.v1",
        "status": "PASS_INDEPENDENT_COLD_REPLAY_PARTIAL_R292_IDENTITY_OWNER_INDEX__ZERO_THEOREM_CREDIT",
        "producer_imported_or_executed": False,
        "producer_sha256": PRODUCER_SHA256,
        "result_sha256": result_file_sha256,
        "source_table_commitments": table_rows,
        "verified_ledgers": observed_meta,
        "verified_census": {"members": len(seen_members), "new_component_representations": len(seen_new_cells), "primary": primary, "refined_primary_extra": extra, "preserved_aliases": len(seen_alias_cells), "fixed_sign_obligations_enumerated_not_discharged": len(seen_obligation_cells)},
        "anti_join_gaps": {"component_cell": 0, "component_registry": 0, "registry_B0": 0, "occupied_alias": 0, "output_missing": 0, "output_orphan": 0, "output_duplicate": 0},
        "known_gaps_reproduced_exactly": result["known_gaps"],
        "formal_credit": expected_credit,
    }


def self_test() -> dict[str, Any]:
    row = {"x": 1}
    closed_row = {**row, "row_sha256": digest(row)}
    need(closed(closed_row, "self-test") == closed_row["row_sha256"], "self-test closed row")
    broken = dict(closed_row)
    broken["x"] = 2
    rejected = False
    try:
        closed(broken, "mutation")
    except VerificationBlocked:
        rejected = True
    need(rejected, "self-test mutation rejected")
    strict_alias_mutations = [
        ({"formal_credit": {"CM2": False}}, {"formal_credit": {"CM2": 0}}),
        ({"exact_census": {"R292_member_count": True}}, {"exact_census": {"R292_member_count": 9_404}}),
        ({"formal_credit": {"normalized_support": False}}, {"formal_credit": {"normalized_support": 0}}),
        ({"formal_credit": {"representation_cover": False}}, {"formal_credit": {"representation_cover": 0}}),
        ({"formal_credit": {"member_identity_minted": False}}, {"formal_credit": {"member_identity_minted": 0}}),
        ({"formal_credit": {"fixed_sign": False}}, {"formal_credit": {"fixed_sign": 0}}),
        ({"row_count": True}, {"row_count": 1}),
    ]
    for mutated, expected in strict_alias_mutations:
        need(not type_strict_equal(mutated, expected), "bool/int alias regression")
    need(type_strict_equal({"x": [0, "a", False]}, {"x": [0, "a", False]}), "strict equality positive control")
    return {"schema": SCHEMA + ".independent-verifier-self-test", "status": "PASS", "producer_imported_or_executed": False, "mutation_rejected": True, "bool_int_alias_mutations_rejected": len(strict_alias_mutations), "result_false_equals_zero_rejected": True, "four_ledger_formal_credit_false_equals_zero_rejected": True, "count_true_equals_one_rejected": True}


def publish_verification(document: dict[str, Any]) -> None:
    root = "/tmp"
    need(os.path.realpath(root) == root, "explicit /tmp authority")
    root_named = os.stat(root, follow_symlinks=False)
    need(stat.S_ISDIR(root_named.st_mode), "explicit /tmp directory")
    root_fd = os.open(root, os.O_RDONLY | getattr(os, "O_DIRECTORY", 0) | getattr(os, "O_NOFOLLOW", 0))
    output_named = os.stat(DELIVERABLES, follow_symlinks=False)
    output_fd = os.open(DELIVERABLES, os.O_RDONLY | getattr(os, "O_DIRECTORY", 0) | getattr(os, "O_NOFOLLOW", 0))
    need((root_named.st_dev, root_named.st_ino, root_named.st_mode) == (os.fstat(root_fd).st_dev, os.fstat(root_fd).st_ino, os.fstat(root_fd).st_mode), "held /tmp dirfd")
    need((output_named.st_dev, output_named.st_ino, output_named.st_mode) == (os.fstat(output_fd).st_dev, os.fstat(output_fd).st_ino, os.fstat(output_fd).st_mode), "held output dirfd")
    try:
        with tempfile.TemporaryDirectory(prefix="cm2-k2i0-verify-", dir=root) as temporary:
            temporary_real = os.path.realpath(temporary)
            need(os.path.dirname(temporary_real) == root, "verification staging placement")
            staged_named = os.stat(temporary_real, follow_symlinks=False)
            staged_fd = os.open(temporary_real, os.O_RDONLY | getattr(os, "O_DIRECTORY", 0) | getattr(os, "O_NOFOLLOW", 0))
            need((staged_named.st_dev, staged_named.st_ino, staged_named.st_mode) == (os.fstat(staged_fd).st_dev, os.fstat(staged_fd).st_ino, os.fstat(staged_fd).st_mode), "held staging dirfd")
            try:
                staged_path = Path(temporary_real) / VERIFICATION
                staged_path.write_bytes(canonical(document) + b"\n")
                with staged_path.open("rb") as handle:
                    os.fsync(handle.fileno())
                staged_info = os.stat(VERIFICATION, dir_fd=staged_fd, follow_symlinks=False)
                need(stat.S_ISREG(staged_info.st_mode) and staged_info.st_nlink == 1, "staged verification regular single-link")
                os.replace(VERIFICATION, VERIFICATION, src_dir_fd=staged_fd, dst_dir_fd=output_fd)
                published = os.stat(VERIFICATION, dir_fd=output_fd, follow_symlinks=False)
                need(stat.S_ISREG(published.st_mode) and published.st_nlink == 1 and published.st_size == staged_info.st_size, "published verification regular single-link")
                need((staged_named.st_dev, staged_named.st_ino, staged_named.st_mode) == (os.fstat(staged_fd).st_dev, os.fstat(staged_fd).st_ino, os.fstat(staged_fd).st_mode), "staging final binding")
            finally:
                os.close(staged_fd)
        need((root_named.st_dev, root_named.st_ino, root_named.st_mode) == (os.fstat(root_fd).st_dev, os.fstat(root_fd).st_ino, os.fstat(root_fd).st_mode) == (os.stat(root, follow_symlinks=False).st_dev, os.stat(root, follow_symlinks=False).st_ino, os.stat(root, follow_symlinks=False).st_mode), "root final binding")
        need((output_named.st_dev, output_named.st_ino, output_named.st_mode) == (os.fstat(output_fd).st_dev, os.fstat(output_fd).st_ino, os.fstat(output_fd).st_mode) == (os.stat(DELIVERABLES, follow_symlinks=False).st_dev, os.stat(DELIVERABLES, follow_symlinks=False).st_ino, os.stat(DELIVERABLES, follow_symlinks=False).st_mode), "output final binding")
    finally:
        os.close(root_fd)
        os.close(output_fd)


def main() -> int:
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--self-test", action="store_true")
    group.add_argument("--verify", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        print(canonical(self_test()).decode("ascii"))
        return 0
    verification = verify()
    publish_verification(verification)
    print(canonical({"status": verification["status"], "verification_sha256": digest(verification)}).decode("ascii"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
