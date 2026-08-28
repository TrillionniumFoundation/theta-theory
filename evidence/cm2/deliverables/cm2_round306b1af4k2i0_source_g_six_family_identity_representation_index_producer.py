#!/usr/bin/env python3
"""Round306B1AF4K2I0: strict R292 identity/representation index lane.

This producer is deliberately a *partial*, zero-theorem-credit K2 package.
It closes one atomic lane of the requested six-family index directly from
pinned raw ledgers:

* 9,404 R292 member identities;
* 10,252 exact transformed-cell representation identities, with one
  bytewise-minimum primary cell per connected component and 848 extras;
* 1,600 occupied transformed cells back-bound to preserved owners; and
* 11,852 fixed-sign pullback obligations, enumerated but not discharged.

Nothing here claims normalized full support, representation cover, A1/A2,
B1A, B2, D02, maximality, fibres, global disposition, or CM2.  The remaining
five coarse families and the A1/A2 census are explicitly outside this partial
lane.  The producer never imports or executes an upstream Python artifact.
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


class Blocked(RuntimeError):
    pass


def need(condition: bool, label: str) -> None:
    if not condition:
        raise Blocked(label)


PREFIX = "cm2_round306b1af4k2i0_source_g_six_family_identity_representation_index_"
SCHEMA = "cm2.round306b1af4k2i0.source-g-six-family-identity-representation-index.partial-r292.v1"
STATUS = "PASS_PARTIAL_R292_IDENTITY_OWNER_INDEX__ZERO_THEOREM_CREDIT__FIVE_FAMILIES_PENDING"
DELIVERABLES = Path(__file__).resolve().parent
HEX64 = re.compile(r"^[0-9a-f]{64}$")

MAX_DECODED_CANONICAL_ROW_BYTES = 8 << 20
STREAM_READ_CHUNK_CHARACTERS = 1 << 18
MAX_READ_CHUNK_UTF8_BYTES = 4 * STREAM_READ_CHUNK_CHARACTERS
MAX_PARSER_BUFFER_UTF8_BYTES = MAX_DECODED_CANONICAL_ROW_BYTES + MAX_READ_CHUNK_UTF8_BYTES

INPUT_PINS: tuple[tuple[str, str, int, str], ...] = (
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

OUTPUTS = {
    "member": PREFIX + "member_index.jsonl.gz",
    "representation": PREFIX + "representation_index.jsonl.gz",
    "preserved_alias": PREFIX + "preserved_alias_index.jsonl.gz",
    "fixed_sign_obligation": PREFIX + "fixed_sign_obligation_index.jsonl.gz",
    "result": PREFIX + "result.json",
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
    raise Blocked("nonintegral JSON token:" + token)


DECODER = json.JSONDecoder(object_pairs_hook=unique_object, parse_float=reject_number, parse_constant=reject_number)


def row_hash(row: dict[str, Any], label: str) -> str:
    need(type(row) is dict and type(row.get("row_sha256")) is str, label + ":closed row")
    body = dict(row)
    claimed = body.pop("row_sha256")
    need(HEX64.fullmatch(claimed) is not None, label + ":row hash syntax")
    need(digest(body) == claimed, label + ":row hash")
    return claimed


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


def stat_fingerprint(value: os.stat_result) -> tuple[int, ...]:
    return (value.st_dev, value.st_ino, value.st_mode, value.st_nlink, value.st_size, value.st_mtime_ns, value.st_ctime_ns)


def directory_identity(value: os.stat_result) -> tuple[int, int, int]:
    return (value.st_dev, value.st_ino, value.st_mode)


def hash_fd(fd: int, expected_size: int) -> tuple[int, str]:
    total = 0
    state = hashlib.sha256()
    offset = 0
    while True:
        block = os.pread(fd, 1 << 20, offset)
        if not block:
            break
        offset += len(block)
        total += len(block)
        need(total <= expected_size, "held FD grew while hashing")
        state.update(block)
    return total, state.hexdigest()


def path_within(path: str, directory: str) -> bool:
    try:
        return os.path.commonpath((path, directory)) == directory
    except ValueError:
        return False


class PinnedInputs:
    def __init__(self, directory: Path) -> None:
        self.directory = str(directory)
        self.dirfd = -1
        self.dir_before: os.stat_result | None = None
        self.files: dict[str, tuple[int, os.stat_result, int, str]] = {}
        self.pin_rows: list[dict[str, Any]] = []

    def __enter__(self) -> "PinnedInputs":
        named = os.stat(self.directory, follow_symlinks=False)
        need(stat.S_ISDIR(named.st_mode), "deliverables real directory")
        self.dirfd = os.open(self.directory, os.O_RDONLY | getattr(os, "O_DIRECTORY", 0) | getattr(os, "O_CLOEXEC", 0) | getattr(os, "O_NOFOLLOW", 0))
        self.dir_before = os.fstat(self.dirfd)
        need(directory_identity(named) == directory_identity(self.dir_before), "deliverables dirfd binding")
        try:
            for label, filename, size, sha in INPUT_PINS:
                before = os.stat(filename, dir_fd=self.dirfd, follow_symlinks=False)
                need(stat.S_ISREG(before.st_mode), "regular input:" + filename)
                need(before.st_nlink == 1 and before.st_size == size, "single-link size pin:" + filename)
                fd = os.open(filename, os.O_RDONLY | getattr(os, "O_CLOEXEC", 0) | getattr(os, "O_NOFOLLOW", 0), dir_fd=self.dirfd)
                opened = os.fstat(fd)
                need(stat_fingerprint(before) == stat_fingerprint(opened), "path/open race:" + filename)
                observed_size, observed_sha = hash_fd(fd, size)
                need(observed_size == size and observed_sha == sha, "first-pass byte pin:" + filename)
                self.files[label] = (fd, opened, size, sha)
                self.pin_rows.append({"label": label, "filename": filename, "exact_size": size, "sha256": sha, "pass1_sha256": observed_sha, "regular": True, "nlink_one": True})
            return self
        except Exception:
            self.close(False)
            raise

    def stream(self, label: str, marker: str, *, anchor: str | None = None) -> Iterator[Any]:
        need(label in self.files, "known held input:" + label)
        fd, before, _, _ = self.files[label]
        os.lseek(fd, 0, os.SEEK_SET)
        raw = os.fdopen(os.dup(fd), "rb")
        filename = next(row[1] for row in INPUT_PINS if row[0] == label)
        binary: BinaryIO = gzip.GzipFile(fileobj=raw, mode="rb") if filename.endswith(".gz") else raw
        text = io.TextIOWrapper(binary, encoding="utf-8", newline="")
        try:
            yield from iter_array(text, marker, anchor=anchor)
        finally:
            text.close()
            if not raw.closed:
                raw.close()
            need(stat_fingerprint(os.fstat(fd)) == stat_fingerprint(before), "held FD stable after parse:" + label)

    def small_json(self, label: str) -> Any:
        fd, before, _, _ = self.files[label]
        size = before.st_size
        need(size <= MAX_DECODED_CANONICAL_ROW_BYTES, "small JSON cap")
        raw = os.pread(fd, size, 0)
        need(len(raw) == size, "small JSON short read")
        value = DECODER.decode(raw.decode("utf-8"))
        need(len(canonical(value)) <= MAX_DECODED_CANONICAL_ROW_BYTES, "small JSON canonical cap")
        return value

    def close(self, verify: bool = True) -> None:
        error: Exception | None = None
        for label, (fd, before, size, sha) in list(self.files.items()):
            try:
                if verify:
                    n2, h2 = hash_fd(fd, size)
                    filename = next(row[1] for row in INPUT_PINS if row[0] == label)
                    named = os.stat(filename, dir_fd=self.dirfd, follow_symlinks=False)
                    need(n2 == size and h2 == sha, "final held-FD rehash:" + label)
                    need(stat_fingerprint(before) == stat_fingerprint(os.fstat(fd)) == stat_fingerprint(named), "final path/FD binding:" + label)
                    for pin in self.pin_rows:
                        if pin["label"] == label:
                            pin["pass2_sha256"] = h2
                            pin["final_path_bound"] = True
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
                    need(directory_identity(self.dir_before) == directory_identity(os.fstat(self.dirfd)) == directory_identity(os.stat(self.directory, follow_symlinks=False)), "deliverables directory replaced")
            except Exception as exc:
                if error is None:
                    error = exc
            finally:
                os.close(self.dirfd)
                self.dirfd = -1
        if error is not None:
            raise error

    def __exit__(self, exc_type: Any, exc: Any, tb: Any) -> None:
        self.close(exc_type is None)


def iter_array(stream: TextIO, marker: str, *, anchor: str | None = None) -> Iterator[Any]:
    def append(buffer: str, label: str) -> str:
        block = stream.read(STREAM_READ_CHUNK_CHARACTERS)
        need(bool(block), label)
        combined = buffer + block
        need(len(combined.encode("utf-8")) <= MAX_PARSER_BUFFER_UTF8_BYTES, "parser buffer cap")
        return combined

    def seek(token: str, initial: str) -> str:
        buffer = initial
        while True:
            at = buffer.find(token)
            if at >= 0:
                return buffer[at + len(token):]
            buffer = append(buffer, "missing marker:" + token)
            at = buffer.find(token)
            if at >= 0:
                return buffer[at + len(token):]
            buffer = buffer[-max(len(token) - 1, 1):]

    buffer = ""
    if anchor is not None:
        buffer = seek(anchor, buffer)
    buffer = seek(marker, buffer)
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
                buffer = append(buffer, "truncated row after comma")
                buffer = buffer.lstrip()
            need(buffer[0] != "]", "trailing comma")
        else:
            need(buffer[0] != ",", "leading comma")
        while True:
            try:
                value, end = DECODER.raw_decode(buffer)
                break
            except json.JSONDecodeError:
                need(len(buffer.encode("utf-8")) <= MAX_DECODED_CANONICAL_ROW_BYTES, "incomplete row source cap")
                buffer = append(buffer, "truncated JSON row")
        need(len(buffer[:end].encode("utf-8")) <= MAX_DECODED_CANONICAL_ROW_BYTES, "successful row source cap")
        need(len(canonical(value)) <= MAX_DECODED_CANONICAL_ROW_BYTES, "successful canonical row cap")
        yield value
        buffer = buffer[end:]
        comma = True


def checked_scratch() -> tuple[str, str, tuple[int, int, int], int]:
    deliverables_real = os.path.realpath(DELIVERABLES)
    # The spill authority is the explicit system /tmp directory, not TMPDIR.
    root = "/tmp"
    need(os.path.realpath(root) == root, "explicit /tmp must resolve to itself")
    need(not path_within(root, deliverables_real), "scratch root inside deliverables")
    info = os.stat(root, follow_symlinks=False)
    need(stat.S_ISDIR(info.st_mode), "scratch root directory")
    root_fd = os.open(root, os.O_RDONLY | getattr(os, "O_DIRECTORY", 0) | getattr(os, "O_CLOEXEC", 0) | getattr(os, "O_NOFOLLOW", 0))
    held = os.fstat(root_fd)
    need(directory_identity(info) == directory_identity(held), "scratch root held-dirfd binding")
    return root, deliverables_real, directory_identity(info), root_fd


def table_finish(label: str, stream: ListHash) -> dict[str, Any]:
    count, sha = EXPECTED_TABLES[label]
    observed = stream.finish()
    need(stream.count == count and observed == sha, label + ":ordered table commitment")
    return {"table": label, "row_count": count, "rows_sha256": observed, "all_rows_own_sha256_checked": True}


def closed_output_row(body: dict[str, Any]) -> dict[str, Any]:
    need("row_sha256" not in body, "output row preclosed")
    return {**body, "row_sha256": digest(body)}


def write_jsonl_gzip(path: Path, rows: list[dict[str, Any]]) -> dict[str, Any]:
    raw_sha = hashlib.sha256()
    raw_size = 0
    with path.open("wb") as target:
        with gzip.GzipFile(filename="", mode="wb", fileobj=target, compresslevel=9, mtime=0) as zipped:
            for row in rows:
                wire = canonical(row) + b"\n"
                raw_sha.update(wire)
                raw_size += len(wire)
                zipped.write(wire)
        target.flush()
        os.fsync(target.fileno())
    named = os.stat(path, follow_symlinks=False)
    need(stat.S_ISREG(named.st_mode) and named.st_nlink == 1, "staged ledger regular single-link")
    fd = os.open(path, os.O_RDONLY | getattr(os, "O_CLOEXEC", 0) | getattr(os, "O_NOFOLLOW", 0))
    try:
        opened = os.fstat(fd)
        need(stat_fingerprint(named) == stat_fingerprint(opened), "staged ledger path/open binding")
        file_size, file_sha = hash_fd(fd, named.st_size)
        final_named = os.stat(path, follow_symlinks=False)
        need(stat_fingerprint(opened) == stat_fingerprint(os.fstat(fd)) == stat_fingerprint(final_named), "staged ledger final path binding")
    finally:
        os.close(fd)
    return {"filename": path.name, "row_count": len(rows), "uncompressed_jsonl_size": raw_size, "uncompressed_jsonl_sha256": raw_sha.hexdigest(), "file_size": file_size, "file_sha256": file_sha, "order": "unsigned_bytewise_ASCII_by_primary_row_id"}


def produce(output_directory: Path, _seed: str) -> dict[str, Any]:
    output_directory = Path(os.path.abspath(output_directory))
    output_named = os.stat(output_directory, follow_symlinks=False)
    need(stat.S_ISDIR(output_named.st_mode), "output directory must be a real preexisting directory")
    output_dirfd = os.open(output_directory, os.O_RDONLY | getattr(os, "O_DIRECTORY", 0) | getattr(os, "O_CLOEXEC", 0) | getattr(os, "O_NOFOLLOW", 0))
    output_held = os.fstat(output_dirfd)
    need(directory_identity(output_named) == directory_identity(output_held), "output held-dirfd binding")
    af2: dict[str, Any]
    cells: dict[str, dict[str, Any]] = {}
    components: dict[str, dict[str, Any]] = {}
    registry: dict[str, dict[str, Any]] = {}
    registry_member_ids: set[str] = set()
    b0: dict[str, dict[str, Any]] = {}
    aliases: dict[str, dict[str, Any]] = {}
    source_tables: list[dict[str, Any]] = []
    shape_counts: Counter[str] = Counter()

    with PinnedInputs(DELIVERABLES) as pins:
        af2 = pins.small_json("AF2_RESULT")
        need(af2["member_count"] == 564_492, "AF2 member denominator")
        need(af2["coarse_partition"]["R292_transformed_cell_union_members"] == 9_404, "AF2 R292 denominator")
        need(af2["formal_credit"] == 0, "AF2 zero credit")

        audit = ListHash()
        for row in pins.stream("R292", '"rows"'):
            row_hash(row, "R292")
            audit.add(row)
            if "Round292_R287_existing_overlap_refinement_cell_id" in row:
                shape_counts["EXACT_REFINEMENT_CELL"] += 1
                cell_id = row["Round292_R287_existing_overlap_refinement_cell_id"]
                need(cell_id not in cells, "duplicate R292 cell")
                need(row["exact_transformed_coordinate_system"] == "(t^2,p,s)", "R292 coordinate system")
                occupancy = row["existing_occurrence_occupancy_count"]
                need(type(occupancy) is int and occupancy in (0, 1), "R292 occupancy")
                existing = row["existing_occurrence_ids"]
                component = row["Round292_refined_new_support_component_id"]
                if occupancy == 0:
                    need(existing == [] and type(component) is str, "uncovered R292 cell")
                else:
                    need(type(existing) is list and len(existing) == 1 and component is None, "occupied R292 cell")
                cells[cell_id] = {"row_sha256": row["row_sha256"], "component_id": component, "occupancy": occupancy, "existing_owner": existing[0] if existing else None, "source_chart": row["source_chart"], "signature_sha256": row["complete_10_field_return_signature_sha256"], "exact_transformed_open_cell": row["exact_transformed_open_cell"]}
            elif "member_refinement_cell_ids" in row:
                shape_counts["REFINED_COMPONENT"] += 1
                component_id = row["Round292_refined_new_support_component_id"]
                need(component_id not in components, "duplicate R292 component")
                member_cells = row["member_refinement_cell_ids"]
                need(type(member_cells) is list and len(member_cells) == row["member_refinement_cell_count"] and len(member_cells) > 0, "R292 component list")
                need(len(set(member_cells)) == len(member_cells), "duplicate cell in component")
                components[component_id] = {"row_sha256": row["row_sha256"], "cell_ids": tuple(member_cells), "source_union_id": row["source_Round287_potential_new_support_union_id"]}
            elif "Round292_registry_overlap_row_id" in row:
                shape_counts["REGISTRY_OVERLAP"] += 1
            else:
                raise Blocked("unknown R292 row shape")
        source_tables.append(table_finish("R292", audit))
        need(shape_counts == Counter({"REGISTRY_OVERLAP": 1_564, "EXACT_REFINEMENT_CELL": 11_852, "REFINED_COMPONENT": 9_404}), "R292 shape census")
        uncovered = {cid for cid, value in cells.items() if value["occupancy"] == 0}
        occupied = set(cells) - uncovered
        component_cells: set[str] = set()
        for component_id, component in components.items():
            for cell_id in component["cell_ids"]:
                need(cell_id in cells and cells[cell_id]["component_id"] == component_id and cells[cell_id]["occupancy"] == 0, "component/cell backbinding")
                need(cell_id not in component_cells, "cell in multiple components")
                component_cells.add(cell_id)
        need(component_cells == uncovered and len(uncovered) == 10_252 and len(occupied) == 1_600, "R292 cell partition")

        audit = ListHash()
        for row in pins.stream("R294_REGISTRY", '"rows"'):
            row_hash(row, "R294 registry")
            audit.add(row)
            if row["registry_entry_kind"] != "CANDIDATE_NEW_ROUND292_REFINED_R287_SUPPORT_COMPONENT":
                continue
            source_id = row["source_row_id"]
            need(source_id in components and row["source_row_sha256"] == components[source_id]["row_sha256"], "R294/component source binding")
            embedded = [cell["Round292_refinement_cell_id"] for cell in row["member_refinement_cells"]]
            need(len(embedded) == row["member_refinement_cell_count"] and set(embedded) == set(components[source_id]["cell_ids"]), "R294 embedded component cells")
            row_id = row["Round294_occurrence_registry_row_id"]
            member_id = row["registry_occurrence_id"]
            need(row_id not in registry and member_id not in registry_member_ids, "duplicate R292 registry identity")
            registry_member_ids.add(member_id)
            registry[row_id] = {"row_sha256": row["row_sha256"], "member_id": member_id, "component_id": source_id}
            components[source_id]["registry_row_id"] = row_id
            components[source_id]["registry_row_sha256"] = row["row_sha256"]
            components[source_id]["member_id"] = member_id
        source_tables.append(table_finish("R294_REGISTRY", audit))
        need(len(registry) == len(components) == 9_404, "R294 R292 registry census")
        need(all("member_id" in component for component in components.values()), "component registry exhaustion")

        audit = ListHash()
        for row in pins.stream("B0", '"member_support_source_rows"'):
            row_hash(row, "B0")
            audit.add(row)
            registry_row_id = row["primary_source_row_id"]
            if registry_row_id not in registry:
                continue
            source = registry[registry_row_id]
            need(row["primary_source_package"] == "R294" and row["primary_source_row_sha256"] == source["row_sha256"], "B0/R294 source binding")
            need(row["member_id"] == source["member_id"] and row["identity_tranche"] == "CANDIDATE_NEW_ROUND292_REFINED_R287_SUPPORT_COMPONENT", "B0 R292 member binding")
            need(registry_row_id not in b0, "duplicate B0 registry source")
            b0[registry_row_id] = {"row_id": row["Round306B0_member_support_source_row_id"], "row_sha256": row["row_sha256"], "component_id": source["component_id"]}
        source_tables.append(table_finish("B0", audit))
        need(set(b0) == set(registry), "B0/R292 registry anti-join")

        audit = ListHash()
        for row in pins.stream("R294_BINDINGS", '"rows"'):
            row_hash(row, "R294 binding")
            audit.add(row)
            if row["support_representation_kind"] != "EXACT_T2_P_S_EXISTING_OCCURRENCE_SUBCOVER_CELL":
                continue
            cell_id = row["source_representation_id"]
            need(cell_id in occupied and row["source_row_id"] == cell_id, "R294 T2PS cell identity")
            source = cells[cell_id]
            need(row["source_row_sha256"] == source["row_sha256"] and row["target_registry_occurrence_id"] == source["existing_owner"], "R294 T2PS owner/source binding")
            need(cell_id not in aliases, "duplicate R294 T2PS alias cell")
            aliases[cell_id] = {"row_id": row["Round294_occurrence_representation_binding_row_id"], "row_sha256": row["row_sha256"], "owner_member_id": row["target_registry_occurrence_id"]}
        source_tables.append(table_finish("R294_BINDINGS", audit))
        need(set(aliases) == occupied and len(aliases) == 1_600, "occupied-cell alias anti-join")

        pin_rows = pins.pin_rows

    member_rows: list[dict[str, Any]] = []
    representation_rows: list[dict[str, Any]] = []
    alias_rows: list[dict[str, Any]] = []
    obligation_rows: list[dict[str, Any]] = []
    primary_count = 0
    extra_count = 0
    component_size_histogram: Counter[int] = Counter()

    for component_id in sorted(components):
        component = components[component_id]
        registry_row_id = component["registry_row_id"]
        b0row = b0[registry_row_id]
        member_id = component["member_id"]
        ordered_cells = sorted(component["cell_ids"], key=lambda value: value.encode("ascii"))
        primary_cell_id = ordered_cells[0]
        component_size_histogram[len(ordered_cells)] += 1
        member_rows.append(closed_output_row({
            "schema": SCHEMA + ".member-row",
            "status": "IDENTITY_JOINED",
            "coarse_family": "R292",
            "member_id": member_id,
            "component_id": component_id,
            "primary_representation_cell_id": primary_cell_id,
            "representation_cell_count": len(ordered_cells),
            "source_R292_component_row_sha256": component["row_sha256"],
            "source_R294_registry_row_id": registry_row_id,
            "source_R294_registry_row_sha256": component["registry_row_sha256"],
            "source_B0_row_id": b0row["row_id"],
            "source_B0_row_sha256": b0row["row_sha256"],
            "formal_credit": {"normalized_support": 0, "representation_cover": 0, "A1_A2": 0, "B1A": 0, "B2": 0, "D02": 0, "CM2": 0},
        }))
        for index, cell_id in enumerate(ordered_cells):
            source = cells[cell_id]
            role = "PRIMARY" if index == 0 else "REFINED_PRIMARY_EXTRA"
            primary_count += index == 0
            extra_count += index != 0
            representation_rows.append(closed_output_row({
                "schema": SCHEMA + ".representation-row",
                "status": "OWNER_INDEXED",
                "representation_role": role,
                "coverage_semantics": "IDENTITY_AND_OWNER_ONLY__SET_EQUALITY_NOT_PROVED",
                "representation_cell_id": cell_id,
                "owner_member_id": member_id,
                "source_R292_cell_row_sha256": source["row_sha256"],
                "source_R292_component_id": component_id,
                "source_R292_component_row_sha256": component["row_sha256"],
                "formal_credit": {"normalized_support": 0, "representation_cover": 0, "physical_incidence": 0, "pullback_equivalence": 0},
            }))

    for cell_id in sorted(aliases):
        source = cells[cell_id]
        alias = aliases[cell_id]
        alias_rows.append(closed_output_row({
            "schema": SCHEMA + ".preserved-alias-row",
            "status": "OWNER_INDEXED",
            "representation_role": "ALIAS_EXISTING_MEMBER",
            "coverage_semantics": "PARTIAL_INCLUSION_ONLY__NOT_FULL_SET_EQUALITY",
            "representation_cell_id": cell_id,
            "owner_member_id": alias["owner_member_id"],
            "source_R292_cell_row_sha256": source["row_sha256"],
            "source_R294_binding_row_id": alias["row_id"],
            "source_R294_binding_row_sha256": alias["row_sha256"],
            "formal_credit": {"normalized_support": 0, "representation_cover": 0, "member_identity_minted": 0},
        }))

    for cell_id in sorted(cells):
        source = cells[cell_id]
        if source["occupancy"] == 0:
            owner = components[source["component_id"]]["member_id"]
            disposition = "NEW_R292_COMPONENT_REPRESENTATION"
        else:
            owner = aliases[cell_id]["owner_member_id"]
            disposition = "PRESERVED_OWNER_ALIAS_REPRESENTATION"
        obligation_rows.append(closed_output_row({
            "schema": SCHEMA + ".fixed-sign-obligation-row",
            "status": "OBLIGATION_ENUMERATED_NOT_DISCHARGED",
            "obligation_kind": "FIXED_SIGN_T2PS_PULLBACK_t_EQUALS_sigma_sqrt_u__u_EQUALS_t_squared",
            "representation_cell_id": cell_id,
            "owner_member_id": owner,
            "owner_disposition": disposition,
            "source_chart": source["source_chart"],
            "exact_transformed_open_cell": source["exact_transformed_open_cell"],
            "complete_10_field_return_signature_sha256": source["signature_sha256"],
            "source_R292_cell_row_sha256": source["row_sha256"],
            "geometry_payload_backbinding": "EXACT_CELL_PAYLOAD_PLUS_SOURCE_ROW_SHA256",
            "sigma_branch_authority_status": "MISSING_NOT_DISCHARGED",
            "formal_feature_row": False,
            "formal_credit": {"pullback_equivalence": 0, "fixed_sign": 0, "normalized_support": 0, "representation_cover": 0},
        }))

    # Component iteration is canonical for the member ledger; representation
    # identity order is independently canonical by exact cell ID.
    representation_rows.sort(key=lambda row: row["representation_cell_id"].encode("ascii"))

    need(len(member_rows) == 9_404, "member output count")
    need(len(representation_rows) == 10_252 and primary_count == 9_404 and extra_count == 848, "representation output census")
    need(len(alias_rows) == 1_600 and len(obligation_rows) == 11_852, "alias/obligation output census")

    scratch_root, deliverables_real, root_identity, scratch_root_fd = checked_scratch()
    try:
        with tempfile.TemporaryDirectory(prefix="cm2-k2i0-r292-", dir=scratch_root) as scratch_name:
            scratch_real = os.path.realpath(scratch_name)
            need(os.path.dirname(scratch_real) == scratch_root and not path_within(scratch_real, deliverables_real), "scratch placement")
            need(directory_identity(os.fstat(scratch_root_fd)) == root_identity == directory_identity(os.stat(scratch_root, follow_symlinks=False)), "scratch root changed")
            scratch = Path(scratch_real)
            scratch_named = os.stat(scratch, follow_symlinks=False)
            scratch_dirfd = os.open(scratch, os.O_RDONLY | getattr(os, "O_DIRECTORY", 0) | getattr(os, "O_CLOEXEC", 0) | getattr(os, "O_NOFOLLOW", 0))
            need(directory_identity(scratch_named) == directory_identity(os.fstat(scratch_dirfd)), "staging held-dirfd binding")
            ledger_meta = {
                "member": write_jsonl_gzip(scratch / OUTPUTS["member"], member_rows),
                "representation": write_jsonl_gzip(scratch / OUTPUTS["representation"], representation_rows),
                "preserved_alias": write_jsonl_gzip(scratch / OUTPUTS["preserved_alias"], alias_rows),
                "fixed_sign_obligation": write_jsonl_gzip(scratch / OUTPUTS["fixed_sign_obligation"], obligation_rows),
            }
            result = {
            "schema": SCHEMA,
            "status": STATUS,
            "scope": "R292_ONLY_PARTIAL_LANE",
            "producer_sha256": None,
            "producer_byte_binding": "EXTERNAL_INDEPENDENT_VERIFIER_STATIC_PIN_ONLY",
            "seed_affects_output": False,
            "input_pins": pin_rows,
            "source_table_commitments": source_tables,
            "exact_census": {
                "R292_member_count": 9_404,
                "R292_uncovered_representation_cell_count": 10_252,
                "R292_primary_representation_count": 9_404,
                "R292_refined_primary_extra_count": 848,
                "R292_preserved_owner_alias_count": 1_600,
                "R292_fixed_sign_obligation_count": 11_852,
                "component_size_histogram": {str(key): value for key, value in sorted(component_size_histogram.items())},
                "primary_selection_rule": "MIN_UNSIGNED_BYTEWISE_ASCII_CELL_ID_PER_COMPONENT",
            },
            "ledgers": ledger_meta,
            "closed_anti_joins": {
                "uncovered_cells_minus_component_members": 0,
                "component_members_minus_uncovered_cells": 0,
                "components_minus_R294_registry": 0,
                "R294_registry_minus_B0": 0,
                "occupied_cells_minus_R294_aliases": 0,
                "R294_T2PS_aliases_minus_occupied_cells": 0,
                "duplicate_member_ids": 0,
                "duplicate_representation_cell_ids_within_R292_new_lane": 0,
                "orphan_owner_count": 0,
            },
            "known_gaps": {
                "fixed_sign_pullback_obligations_not_discharged": 11_852,
                "R292_physical_face_and_Kruskal_semantic_obligations_not_discharged": 848,
                "fixed_sign_sigma_branch_authority_missing": 11_852,
                "remaining_coarse_families_not_emitted": ["PRESERVED", "NON_GRAPH", "R2", "G2A", "G2B"],
                "remaining_member_identity_rows_not_emitted": 555_088,
                "remaining_global_representation_rows_not_emitted": 600_052,
                "A1_A2_obligations_not_enumerated_in_this_lane": 80_092,
            },
            "formal_credit": {"normalized_support": 0, "representation_cover": 0, "A1_A2": 0, "B1A": 0, "B2": 0, "maximality": 0, "fibre": 0, "global_disposition": 0, "D02": 0, "D03": 0, "D04": 0, "Gate5": 0, "CM2": 0},
            }
            result_path = scratch / OUTPUTS["result"]
            result_path.write_bytes(canonical(result) + b"\n")
            with result_path.open("rb") as handle:
                os.fsync(handle.fileno())
            # The result is the completion marker and is deliberately last.
            for key in ("member", "representation", "preserved_alias", "fixed_sign_obligation", "result"):
                source = scratch / OUTPUTS[key]
                source_info = os.stat(OUTPUTS[key], dir_fd=scratch_dirfd, follow_symlinks=False)
                need(stat.S_ISREG(source_info.st_mode) and source_info.st_nlink == 1, "staged regular single-link:" + key)
                os.replace(OUTPUTS[key], OUTPUTS[key], src_dir_fd=scratch_dirfd, dst_dir_fd=output_dirfd)
                published = os.stat(OUTPUTS[key], dir_fd=output_dirfd, follow_symlinks=False)
                need(stat.S_ISREG(published.st_mode) and published.st_nlink == 1 and published.st_size == source_info.st_size, "published regular single-link:" + key)
            need(directory_identity(os.fstat(output_dirfd)) == directory_identity(output_named) == directory_identity(os.stat(output_directory, follow_symlinks=False)), "output directory final binding")
            need(directory_identity(os.fstat(scratch_dirfd)) == directory_identity(scratch_named), "staging directory final binding")
            os.close(scratch_dirfd)
        need(directory_identity(os.fstat(scratch_root_fd)) == root_identity == directory_identity(os.stat(scratch_root, follow_symlinks=False)), "scratch root final binding")
        return result
    finally:
        os.close(scratch_root_fd)
        os.close(output_dirfd)


def self_test() -> dict[str, Any]:
    value = {"x": "a"}
    row = closed_output_row(value)
    need(row_hash(row, "self-test") == row["row_sha256"], "output row hash")
    bad = dict(row)
    bad["x"] = "b"
    rejected = False
    try:
        row_hash(bad, "self-test mutation")
    except Blocked:
        rejected = True
    need(rejected, "mutation rejected")
    exact_body = {"x": "a" * (MAX_DECODED_CANONICAL_ROW_BYTES - len(canonical({"x": ""})))}
    exact_wire = canonical(exact_body)
    need(len(exact_wire) == MAX_DECODED_CANONICAL_ROW_BYTES, "exact cap fixture")
    parsed = list(iter_array(io.StringIO('{"rows":[' + exact_wire.decode("ascii") + ']}'), '"rows"'))
    need(parsed == [exact_body], "exact cap accepted")
    overflow = {"x": exact_body["x"] + "a"}
    rejected_cap = False
    try:
        list(iter_array(io.StringIO('{"rows":[' + canonical(overflow).decode("ascii") + ']}'), '"rows"'))
    except Blocked:
        rejected_cap = True
    need(rejected_cap, "cap plus one rejected")
    return {"schema": SCHEMA + ".self-test", "status": "PASS", "mutation_rejected": True, "decoded_row_exact_cap": MAX_DECODED_CANONICAL_ROW_BYTES, "decoded_row_cap_plus_one_rejected": True, "candidate_is_formal": False}


def main() -> int:
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--self-test", action="store_true")
    group.add_argument("--produce", action="store_true")
    parser.add_argument("--output-directory")
    parser.add_argument("--hash-seed", default="0")
    args = parser.parse_args()
    if args.self_test:
        need(args.output_directory is None, "self-test is filesystem-inert")
        print(canonical(self_test()).decode("ascii"))
        return 0
    need(args.output_directory is not None, "production output directory required")
    result = produce(Path(args.output_directory), args.hash_seed)
    print(canonical({"status": result["status"], "result_sha256": digest(result)}).decode("ascii"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
