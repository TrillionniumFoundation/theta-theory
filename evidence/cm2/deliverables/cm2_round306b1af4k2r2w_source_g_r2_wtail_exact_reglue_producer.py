#!/usr/bin/env python3
"""Round306B1AF4K2R2W exact R2 W-tail reglue authority audit.

This read-only producer reconstructs the four multiplicity-two Round271
W-tail joins from exact frozen bytes.  It proves only the rational box
partition and the exact identity joins that those bytes actually contain.
The relevant B1R0 rows expressly leave the source-free support predicate and
full-support union theorem pending, and no sealed row assigns the artificial
face to one child.  Consequently every emitted theorem row is
``BLOCKED_MISSING_AUTHORITY`` and all theorem/CM2 credits remain zero.

No upstream Python is imported or executed.  ``--full-replay`` is the only
mode which opens inputs.  All inputs are held by descriptor, hashed twice
before parsing, and fully rehashed with final path/descriptor identity checks.
"""

from __future__ import annotations

import argparse
from fractions import Fraction
import gzip
import hashlib
import io
import json
import os
from pathlib import Path
import re
import stat
from typing import Any, BinaryIO, Final, Iterator, TextIO


class AuditBlocked(RuntimeError):
    pass


def need(condition: bool, label: str) -> None:
    if not condition:
        raise AuditBlocked(label)


SCHEMA: Final = "cm2.round306b1af4k2r2w.source-g-r2-wtail-exact-reglue.v1"
STATUS: Final = "BLOCKED_MISSING_AUTHORITY__FOUR_EXACT_GEOMETRIC_PARTITIONS__ZERO_THEOREM_CREDIT"
HERE: Final = Path(__file__).resolve().parent
HEX64 = re.compile(r"^[0-9a-f]{64}$")
MAX_ROW_BYTES = 8 << 20
READ_CHARS = 1 << 18
MAX_BUFFER_BYTES = MAX_ROW_BYTES + 4 * READ_CHARS


# label, filename, exact raw size, exact SHA-256, role
PINS: Final = (
    ("R182", "cm2_round182_source_g_clipped_graph_and_pair_arrangement_rows.json", 158_815_476, "ae6e0c38df325e98b01a1d75acfbd8a85a71fda6a118db11d7dff6decf3f847c", "PARENT_BOX_AND_OCCURRENCE_AUTHORITY"),
    ("R271", "cm2_round271_source_g_wall_and_outgoing_tail_signature_materialization_certificate.json", 112_741_715, "c2a6b66c6fc6ac0b353b36254339a90b91f18c52246c324307ee49569bd7b747", "CHILD_BOX_SIGNATURE_OWNER_SOURCE"),
    ("B1R0_CELL", "cm2_round306b1r0_source_g_r288_predicate_source_inventory_and_union_freeze_predicate_source_cell.json.gz", 105_989_322, "19d13d93fc02296f673ca18cc2edbd96174985f7be8fb0e03694582b188b0f96", "ZERO_CREDIT_CHILD_INVENTORY"),
    ("B1R0_MEMBER", "cm2_round306b1r0_source_g_r288_predicate_source_inventory_and_union_freeze_member_union.json.gz", 123_019_951, "4b3633782e4514f598cb9cce19930ba31616f7d42aab002df4f77f9b4601ddf7", "ZERO_CREDIT_PARENT_NORMALIZATION"),
    ("R278_PROBE", "cm2_round278_source_g_round271_w_tail_artificial_split_alias_probe.py", 16_828, "cc0a6885e402e40ae1255e538e18cb15ba71c4e311535feee251ee726a71dc83", "NONSEALED_ZERO_CREDIT_PROBE_SOURCE_ONLY"),
    ("R278_REPORT", "cm2_round278_source_g_round271_w_tail_artificial_split_alias_probe_report.md", 3_565, "404017f5537b62886b6e35b134c6e6e8b0ad5afd5aed11331dd254c689675684", "NONSEALED_ZERO_CREDIT_REPORT_ONLY"),
    ("K1", "cm2_round306b1af4k1_source_g_semantic_theorem_kernel.py", 68_346, "17d9c302984e2e29dcf02832f36ec9437c23c8b65c27289a3469db222ce4edae", "GENERIC_ZERO_CREDIT_CHECKER_FOUNDATION_NOT_EXECUTED"),
)
PIN_BY_LABEL = {row[0]: row for row in PINS}


TABLES: Final = {
    "R182.occurrence": (54_220, "d77e65b5b9dfb5f7f107b39eaac3553be67ba76231f1888de1f97ecc121361db"),
    "R182.leaf": (202_840, "ced6d2764a7e1f5d404c1d56249e428f0754e53e7dded620e5904f9eb80b694c"),
    "R271.side": (70_420, "cec8a0318385127d8ee5d7968c016f8f6b7ee103596fbce5258cc3b25c4930b8"),
    "B1R0.cell": (295_340, "b89220807eef10bc8412be19c5037ea75fa3c6fdf4321c27938afec0c68c9246"),
    "B1R0.member": (295_336, "6665fc8e72824fba7dbd1d1b7462ae419bb31c25149037da3183d74569b62a3d"),
}


SPECS: Final = (
    {
        "member_id": "source-g-expanded-occurrence:777579326780a1cde1e5b1f37d3bbb9c125adc26409d16599f48f29673f9dc05",
        "parent_leaf_id": "round182-collar-leaf:79c940db4e5e3820579ee9c0657df82835a770cfd5a1e6f7a1126203680b0e5e",
        "occurrence_id": "round179-outgoing-normal-form:be2ee0ced92e8bab399a02dabfe2a9f9a3220f41cdcd85eba999f8cc3d03cfa1",
        "member_union_row_id": "round306b1r0-member-union:99effda54a2eff3ccf5918c0852680d73d44575743d88fe2a13faa9ae59af767",
        "children": ["round271-W-tail-side:f685c712f6ffcdcb2067dbbb1ce8263f735ade1d3244dae3c24bd81c5df03c8b", "round271-W-tail-side:8bddfee03e177225f624a72fd8ec52953521d9b6d62f49576b69108acb181d15"],
        "owner_target": "W[1,-1]",
        "interface": "-47967/128000",
        "parent_box": ["-3009/8000", "-4779/12800", "-3/64", "-11/256", "1/800", "1/400"],
    },
    {
        "member_id": "source-g-expanded-occurrence:3dbc14a6e173aceacb227af67bf77573bf853dc8330d3d7e91dcbd1e0332a9e0",
        "parent_leaf_id": "round182-collar-leaf:24c355269d353269664e921f76120a6d1695aa8bdb9f44b399533a62c05c086f",
        "occurrence_id": "round179-outgoing-normal-form:460d9946db8e2d996d156804ae083e2e433dc94dcb5e373806d5844893f42412",
        "member_union_row_id": "round306b1r0-member-union:484739f92c91848acec5367f13d60cf05c7cf3063c545700448fa5e223ed6658",
        "children": ["round271-W-tail-side:283deceec14bcb2bf1023665cf8b443eda90cf995e8b4588aa7359e9b50b5943", "round271-W-tail-side:d2ca5b59b2b24166b1b2af242db4fe2081d10c53f6459a56488b9bf105a32a9b"],
        "owner_target": "W[-2,-1]",
        "interface": "-47967/128000",
        "parent_box": ["-3009/8000", "-4779/12800", "11/256", "3/64", "-1/400", "-1/800"],
    },
    {
        "member_id": "source-g-expanded-occurrence:7679f954c45bd68587aa443c6dcecfa04beabac556043a05c88b96d54d00a231",
        "parent_leaf_id": "round182-collar-leaf:2f8300b7f5a5747e62991e268c5854a82d376761a43d391abd78942422143b98",
        "occurrence_id": "round179-outgoing-normal-form:77219d3f2cd99a0c1edc00b80fc25a1c64a5d62bc753ab06c63638e8c9ef567b",
        "member_union_row_id": "round306b1r0-member-union:79ee911921cd1e8a08494dfecf64aa5e35f82b7d9b062b4fc2f4c899dd0e27e2",
        "children": ["round271-W-tail-side:7f514e571220e84dc2a295fbceb2eb3af1dc1c76ac32f7b3b4dee8feeb575380", "round271-W-tail-side:42360900f45f7ec7fb40da6cd66a6651574e40e5e945d70a3a376c6f43705b05"],
        "owner_target": "W[1,0]",
        "interface": "47967/128000",
        "parent_box": ["4779/12800", "3009/8000", "11/256", "3/64", "1/800", "1/400"],
    },
    {
        "member_id": "source-g-expanded-occurrence:8d341c7b44298ec53e940bda07a53b38ddd01f34bad63236d0d691cf81a83819",
        "parent_leaf_id": "round182-collar-leaf:2723216547a2aae29f6cabe6b8221d232df6be390f4dbd83317d6bff2f6d3f3a",
        "occurrence_id": "round179-outgoing-normal-form:e5280e0130ee8e0d8ea983d7e0793fead6c77181b87070b872c42e8651ab3bb2",
        "member_union_row_id": "round306b1r0-member-union:f925652e699ee2e7eabac04346a1fa02104440fe4e48e8734e4d40fec841d340",
        "children": ["round271-W-tail-side:0a7aa9828f1f7d748808d3c987b3cdace8d7803782b02fe75971113ff3d704ae", "round271-W-tail-side:9d741d4b52856aa778df9829354028e84822ab542fca42b401f715357a39c78b"],
        "owner_target": "W[-2,0]",
        "interface": "47967/128000",
        "parent_box": ["4779/12800", "3009/8000", "-3/64", "-11/256", "-1/400", "-1/800"],
    },
)


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True, allow_nan=False).encode("ascii")


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for key, value in pairs:
        need(type(key) is str and key not in out, "duplicate/non-string JSON key")
        out[key] = value
    return out


def reject_number(token: str) -> Any:
    raise AuditBlocked("nonintegral JSON token:" + token)


DECODER = json.JSONDecoder(object_pairs_hook=unique_object, parse_float=reject_number, parse_constant=reject_number)


def strict_tree(value: Any, depth: int = 0) -> None:
    need(depth <= 256, "JSON depth")
    if value is None or type(value) in (str, bool, int):
        return
    if type(value) is list:
        for item in value:
            strict_tree(item, depth + 1)
        return
    need(type(value) is dict, "strict JSON type")
    for key, item in value.items():
        need(type(key) is str, "string JSON key")
        strict_tree(item, depth + 1)


class ListHash:
    def __init__(self) -> None:
        self.state = hashlib.sha256(b"[")
        self.count = 0

    def add(self, row: Any) -> None:
        strict_tree(row)
        if self.count:
            self.state.update(b",")
        self.state.update(canonical(row))
        self.count += 1

    def finish(self) -> str:
        state = self.state.copy()
        state.update(b"]")
        return state.hexdigest()


def check_closed(row: Any, label: str) -> None:
    need(type(row) is dict and type(row.get("row_sha256")) is str, label + ":closed row")
    payload = dict(row)
    claimed = payload.pop("row_sha256")
    need(HEX64.fullmatch(claimed) is not None and digest(payload) == claimed, label + ":row SHA")


def identity(info: os.stat_result) -> tuple[int, ...]:
    return (info.st_dev, info.st_ino, info.st_mode, info.st_nlink, info.st_size, info.st_mtime_ns, info.st_ctime_ns)


def dir_identity(info: os.stat_result) -> tuple[int, int, int]:
    return (info.st_dev, info.st_ino, info.st_mode)


def hash_fd(fd: int) -> str:
    os.lseek(fd, 0, os.SEEK_SET)
    state = hashlib.sha256()
    while True:
        block = os.read(fd, 1 << 20)
        if not block:
            break
        state.update(block)
    os.lseek(fd, 0, os.SEEK_SET)
    return state.hexdigest()


class HeldPins:
    def __init__(self) -> None:
        self.dirfd = -1
        self.dir_before: os.stat_result | None = None
        self.files: dict[str, tuple[int, os.stat_result]] = {}
        self.rows: list[dict[str, Any]] = []

    def __enter__(self) -> "HeldPins":
        root = os.fspath(HERE)
        before = os.stat(root, follow_symlinks=False)
        need(stat.S_ISDIR(before.st_mode), "deliverables directory")
        flags = os.O_RDONLY | getattr(os, "O_DIRECTORY", 0) | getattr(os, "O_NOFOLLOW", 0) | getattr(os, "O_CLOEXEC", 0)
        self.dirfd = os.open(root, flags)
        held = os.fstat(self.dirfd)
        need(dir_identity(before) == dir_identity(held), "directory open race")
        self.dir_before = held
        try:
            for label, filename, size, expected, role in PINS:
                need(filename == os.path.basename(filename), "pin basename")
                named = os.stat(filename, dir_fd=self.dirfd, follow_symlinks=False)
                need(stat.S_ISREG(named.st_mode) and named.st_nlink == 1 and named.st_size == size, "pin identity:" + label)
                fd = os.open(filename, os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0) | getattr(os, "O_CLOEXEC", 0), dir_fd=self.dirfd)
                opened = os.fstat(fd)
                need(identity(named) == identity(opened), "pin open race:" + label)
                h1, h2 = hash_fd(fd), hash_fd(fd)
                need(h1 == h2 == expected, "pin two-pass SHA:" + label)
                need(identity(opened) == identity(os.stat(filename, dir_fd=self.dirfd, follow_symlinks=False)), "pin rebound:" + label)
                self.files[label] = (fd, opened)
                self.rows.append({"label": label, "filename": filename, "exact_size": size, "sha256": expected, "role": role, "two_pass_held_fd": True})
            return self
        except BaseException:
            self.close()
            raise

    def stream(self, label: str, marker: str, *, anchor: str | None = None) -> Iterator[Any]:
        fd, before = self.files[label]
        os.lseek(fd, 0, os.SEEK_SET)
        raw = os.fdopen(os.dup(fd), "rb")
        binary: BinaryIO = gzip.GzipFile(fileobj=raw, mode="rb") if PIN_BY_LABEL[label][1].endswith(".gz") else raw
        text = io.TextIOWrapper(binary, encoding="utf-8", newline="")
        try:
            yield from iter_array(text, marker, anchor=anchor)
        finally:
            text.close()
            if not raw.closed:
                raw.close()
            os.lseek(fd, 0, os.SEEK_SET)
            need(identity(os.fstat(fd)) == identity(before), "held FD after parse:" + label)

    def final_rehash(self) -> None:
        for label, filename, _size, expected, _role in PINS:
            fd, before = self.files[label]
            need(hash_fd(fd) == expected, "final SHA:" + label)
            need(identity(os.fstat(fd)) == identity(before) == identity(os.stat(filename, dir_fd=self.dirfd, follow_symlinks=False)), "final path binding:" + label)
        assert self.dir_before is not None
        need(dir_identity(self.dir_before) == dir_identity(os.fstat(self.dirfd)) == dir_identity(os.stat(HERE, follow_symlinks=False)), "final directory binding")

    def close(self) -> None:
        for fd, _before in self.files.values():
            try:
                os.close(fd)
            except OSError:
                pass
        self.files.clear()
        if self.dirfd >= 0:
            os.close(self.dirfd)
            self.dirfd = -1

    def __exit__(self, *_args: object) -> None:
        self.close()


def iter_array(stream: TextIO, marker: str, *, anchor: str | None = None) -> Iterator[Any]:
    def append(buffer: str, label: str) -> str:
        block = stream.read(READ_CHARS)
        need(bool(block), label)
        output = buffer + block
        need(len(output.encode("utf-8")) <= MAX_BUFFER_BYTES, "parser buffer cap")
        return output

    def seek(token: str, buffer: str) -> str:
        while True:
            position = buffer.find(token)
            if position >= 0:
                return buffer[position + len(token):]
            buffer = append(buffer, "missing marker:" + token)
            position = buffer.find(token)
            if position >= 0:
                return buffer[position + len(token):]
            buffer = buffer[-max(1, len(token) - 1):]

    buffer = ""
    if anchor is not None:
        buffer = seek(anchor, buffer)
    buffer = seek(marker, buffer)
    stripped = buffer.lstrip()
    if stripped.startswith(":"):
        stripped = stripped[1:].lstrip()
        need(stripped.startswith("["), "marker is not array")
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
            need(buffer[0] != "]", "trailing comma")
        else:
            need(buffer[0] != ",", "leading comma")
        while True:
            try:
                value, end = DECODER.raw_decode(buffer)
                break
            except json.JSONDecodeError:
                need(len(buffer.encode("utf-8")) <= MAX_ROW_BYTES, "source row cap")
                buffer = append(buffer, "truncated JSON row")
        need(len(buffer[:end].encode("utf-8")) <= MAX_ROW_BYTES, "decoded source row cap")
        need(len(canonical(value)) <= MAX_ROW_BYTES, "canonical row cap")
        strict_tree(value)
        yield value
        buffer = buffer[end:]
        comma = True


def audit_stream(pins: HeldPins, pin_label: str, table_label: str, marker: str, *, anchor: str | None = None, closed: bool, select: Any) -> tuple[dict[str, Any], list[Any]]:
    rows = ListHash()
    selected: list[Any] = []
    for row in pins.stream(pin_label, marker, anchor=anchor):
        if closed:
            check_closed(row, table_label)
        rows.add(row)
        if select(row):
            selected.append(row)
    count, expected = TABLES[table_label]
    observed = rows.finish()
    need(rows.count == count and observed == expected, "ordered table commitment:" + table_label)
    return ({"table": table_label, "row_count": count, "rows_sha256": observed, "own_row_sha256_checked": closed}, selected)


def fractions(box: Any, label: str) -> tuple[Fraction, ...]:
    need(type(box) is list and len(box) == 6 and all(type(x) is str for x in box), label + ":box type")
    result = tuple(Fraction(x) for x in box)
    need(all(str(q) == x for q, x in zip(result, box, strict=True)), label + ":canonical rational")
    return result


def close(row: dict[str, Any]) -> dict[str, Any]:
    need("row_sha256" not in row, "unclosed output row")
    row["row_sha256"] = digest(row)
    return row


def source_commitment(rows: dict[str, Any]) -> str:
    return digest(rows)


def build() -> dict[str, Any]:
    spec_by_member = {row["member_id"]: row for row in SPECS}
    child_ids = {child for spec in SPECS for child in spec["children"]}
    leaf_ids = {spec["parent_leaf_id"] for spec in SPECS}
    occurrence_ids = {spec["occurrence_id"] for spec in SPECS}
    table_receipts: list[dict[str, Any]] = []

    with HeldPins() as pins:
        receipt, occurrences_list = audit_stream(pins, "R182", "R182.occurrence", "\"collar_occurrence_rows\"", closed=False, select=lambda row: type(row) is list and len(row) > 8 and row[1] in occurrence_ids)
        table_receipts.append(receipt)
        receipt, leaves_list = audit_stream(pins, "R182", "R182.leaf", "\"collar_leaf_rows\"", closed=False, select=lambda row: type(row) is list and len(row) > 9 and row[0] in leaf_ids)
        table_receipts.append(receipt)
        receipt, child_list = audit_stream(pins, "R271", "R271.side", "\"rows\":[", anchor="\"formal_side_signature_ledger\":{", closed=True, select=lambda row: type(row) is dict and row.get("signed_region_row_id") in child_ids)
        table_receipts.append(receipt)
        receipt, cell_list = audit_stream(pins, "B1R0_CELL", "B1R0.cell", "\"predicate_source_cell_rows\":[", closed=True, select=lambda row: type(row) is dict and row.get("formal_member_id") in spec_by_member)
        table_receipts.append(receipt)
        receipt, member_list = audit_stream(pins, "B1R0_MEMBER", "B1R0.member", "\"member_union_rows\":[", closed=True, select=lambda row: type(row) is dict and row.get("member_id") in spec_by_member)
        table_receipts.append(receipt)
        pins.final_rehash()
        pin_receipts = list(pins.rows)

    occurrences = {row[1]: row for row in occurrences_list}
    leaves = {row[0]: row for row in leaves_list}
    children = {row["signed_region_row_id"]: row for row in child_list}
    cells_by_member: dict[str, list[dict[str, Any]]] = {key: [] for key in spec_by_member}
    for row in cell_list:
        cells_by_member[row["formal_member_id"]].append(row)
    members = {row["member_id"]: row for row in member_list}
    need(len(occurrences) == len(leaves) == len(members) == 4 and len(children) == len(cell_list) == 8, "selected row census")

    ledger_rows: list[dict[str, Any]] = []
    for spec in sorted(SPECS, key=lambda row: row["member_id"]):
        member_id = spec["member_id"]
        occurrence = occurrences[spec["occurrence_id"]]
        leaf = leaves[spec["parent_leaf_id"]]
        member = members[member_id]
        child_rows = [children[child] for child in spec["children"]]
        child_rows.sort(key=lambda row: row["t_child"])
        cell_rows = sorted(cells_by_member[member_id], key=lambda row: row["predicate_source_inventory"]["t_child"])
        need(len(child_rows) == len(cell_rows) == 2, "two children/cells:" + member_id)
        need([row["t_child"] for row in child_rows] == [0, 1], "child labels:" + member_id)
        need([row["predicate_source_inventory"]["t_child"] for row in cell_rows] == [0, 1], "cell labels:" + member_id)
        need(leaf[0] == spec["parent_leaf_id"] and leaf[1] == spec["occurrence_id"] and leaf[4] == spec["parent_box"], "R182 parent binding:" + member_id)
        need(occurrence[1] == spec["occurrence_id"] and occurrence[5] == spec["owner_target"] and occurrence[6] == "OUTGOING" and occurrence[8] == "target_normal_x^2-target_normal_y^2=0", "R182 occurrence binding:" + member_id)
        parent = fractions(spec["parent_box"], "parent")
        left, right = [fractions(row["t_child_box"], "child") for row in child_rows]
        interface = Fraction(spec["interface"])
        need(left[0] == parent[0] < left[1] == interface == right[0] < right[1] == parent[1], "exact t partition:" + member_id)
        need(left[2:] == right[2:] == parent[2:], "exact p/s base:" + member_id)
        need(all(parent[2 * axis] < parent[2 * axis + 1] for axis in range(3)), "positive parent box")
        face_area = (parent[3] - parent[2]) * (parent[5] - parent[4])
        need(face_area > 0, "positive face area")
        signature = child_rows[0]["local_return_signature"]
        need(signature == child_rows[1]["local_return_signature"], "signature equality:" + member_id)
        need(digest(signature) == child_rows[0]["complete_10_field_return_signature_sha256"] == child_rows[1]["complete_10_field_return_signature_sha256"], "signature commitment:" + member_id)
        for row in child_rows:
            need(row["Round182_leaf_row_id"] == spec["parent_leaf_id"] and row["owner_target"] == spec["owner_target"] and row["region_product_sign"] == "STRICT_NEGATIVE", "child authority binding:" + member_id)
        for source, cell in zip(child_rows, cell_rows, strict=True):
            need(cell["source_signature_row_id"] == source["signed_region_row_id"] and cell["source_signature_row_sha256"] == source["row_sha256"], "cell/source binding:" + member_id)
            need(cell["outer_carrier_box"] == source["t_child_box"] and cell["predicate_source_inventory"]["predicate_family"] == "OUTGOING_W_TAIL_CHILD_FACTOR_CELL", "cell geometry binding:" + member_id)
            need(cell["source_free_interval_predicate_ast_materialized"] is False and cell["outer_carrier_box_claimed_as_full_support"] is False and type(cell["formal_full_support_credit"]) is int and cell["formal_full_support_credit"] == 0, "cell zero-credit boundary:" + member_id)
        normalization = member["Round271_W_tail_parent_normalization"]
        need(member["Round306B1R0_member_union_row_id"] == spec["member_union_row_id"] and member["predicate_source_cell_multiplicity"] == 2, "member row binding:" + member_id)
        need(normalization["normalized_parent_box"] == spec["parent_box"] and normalization["source_children"] == spec["children"] and normalization["artificial_interface"] == {"axis": "t", "value": spec["interface"]}, "normalization payload:" + member_id)
        need(normalization["interface_is_not_a_physical_support_boundary"] is True and type(normalization["full_support_credit"]) is int and normalization["full_support_credit"] == 0, "normalization zero credit:" + member_id)
        need(member["full_support_union_theorem_status"] == "PENDING_SOURCE_FREE_INTERVAL_PREDICATE_EQUIVALENCE" and type(member["formal_full_support_credit"]) is int and member["formal_full_support_credit"] == 0, "pending theorem status:" + member_id)

        exact_sources = {
            "R182_occurrence_row_commitment_sha256": digest(occurrence),
            "R182_parent_leaf_row_commitment_sha256": digest(leaf),
            "R271_child_row_ids": [row["signed_region_row_id"] for row in child_rows],
            "R271_child_row_sha256": [row["row_sha256"] for row in child_rows],
            "B1R0_cell_row_ids": [row["Round306B1R0_predicate_source_cell_row_id"] for row in cell_rows],
            "B1R0_cell_row_sha256": [row["row_sha256"] for row in cell_rows],
            "B1R0_member_union_row_id": member["Round306B1R0_member_union_row_id"],
            "B1R0_member_union_row_sha256": member["row_sha256"],
        }
        input_commitment = digest({"pins": {label: sha for label, _name, _size, sha, _role in PINS}, "tables": table_receipts, "rows": exact_sources})
        ledger_rows.append(close({
            "schema": SCHEMA + ".theorem-row.v1",
            "theorem_row_id": "round306b1af4k2r2w-reglue:" + digest([member_id, input_commitment]),
            "theorem_kind": "ARTIFICIAL_FACE_REGLUE_EXACT_V2",
            "status": "BLOCKED_MISSING_AUTHORITY",
            "member_id": member_id,
            "parent_leaf_id": spec["parent_leaf_id"],
            "occurrence_id": spec["occurrence_id"],
            "source_chart": signature["source_chart"],
            "owner_target": spec["owner_target"],
            "parent_box": spec["parent_box"],
            "ordered_children": [row["signed_region_row_id"] for row in child_rows],
            "ordered_child_boxes": [row["t_child_box"] for row in child_rows],
            "artificial_interface": {"axis": "t", "value": spec["interface"]},
            "complete_common_face_box": [spec["interface"], spec["interface"], *spec["parent_box"][2:]],
            "complete_common_face_exact_area": str(face_area),
            "exact_parent_interval_partition_geometry_verified": True,
            "half_open_partition_owner_verified": False,
            "same_R182_parent_verified": True,
            "same_complete_10_field_signature_verified": True,
            "same_owner_target_verified": True,
            "same_strict_negative_region_product_sign_verified": True,
            "physical_support_equivalence_verified": False,
            "unique_artificial_face_owner_verified": False,
            "missing_authority": [
                "SOURCE_FREE_INTERVAL_PREDICATE_AST_AND_EQUIVALENCE_THEOREM_FOR_BOTH_CHILDREN",
                "SEALED_INPUT_BOUND_WHOLE_FACE_AND_TWO_SIDED_INWARD_CORRIDOR_PHYSICAL_EQUIVALENCE_CERTIFICATE",
                "CANONICAL_HALF_OPEN_OWNER_ASSIGNMENT_FOR_THE_ARTIFICIAL_INTERFACE",
                "INDEPENDENT_VERIFIER_RECEIPT_FOR_THE_PHYSICAL_EQUIVALENCE_CERTIFICATE",
            ],
            "authority_boundary": {
                "B1R0_source_free_interval_predicate_ast_materialized": False,
                "B1R0_outer_carriers_claimed_as_full_support": False,
                "B1R0_full_support_union_theorem_status": "PENDING_SOURCE_FREE_INTERVAL_PREDICATE_EQUIVALENCE",
                "Round278_role": "NONSEALED_ZERO_CREDIT_PROBE_WITHOUT_RESULT_VERIFICATION_OR_MANIFEST",
                "K1_role": "GENERIC_ZERO_CREDIT_CHECKER_FOUNDATION_ONLY_NOT_A_FAMILY_THEOREM",
            },
            "input_rows": exact_sources,
            "canonical_input_commitment_sha256": input_commitment,
            "r2_artificial_face_reglue_credit": 0,
            "normalized_support_credit": 0,
            "representation_cover_credit": 0,
            "B1A_credit": 0,
            "B2_credit": 0,
            "CM2": "NO-GO_FOR_CLAIM",
        }))

    ledger_rows.sort(key=lambda row: row["theorem_row_id"])
    need(len(ledger_rows) == 4 and all(row["status"] == "BLOCKED_MISSING_AUTHORITY" for row in ledger_rows), "four blocked theorem rows")
    result = {
        "schema": SCHEMA,
        "theorem_kind": "ARTIFICIAL_FACE_REGLUE_EXACT_V2",
        "status": STATUS,
        "census": {
            "R2_selected_cells_context": 295_340,
            "R2_members_context": 295_336,
            "two_cell_members": 4,
            "exact_geometric_parent_partitions": 4,
            "blocked_missing_authority_rows": 4,
            "r2_artificial_face_reglue_credit": 0,
        },
        "ordered_table_commitments": table_receipts,
        "input_pin_receipts": pin_receipts,
        "theorem_ledger": {"row_count": 4, "rows_sha256": digest(ledger_rows), "row_hashes_sha256": digest([row["row_sha256"] for row in ledger_rows]), "rows": ledger_rows},
        "global_credit_boundary": {"normalized_support_credit": 0, "representation_cover_credit": 0, "B1A_credit": 0, "B2_credit": 0, "maximality_credit": 0, "CM2": "NO-GO_FOR_CLAIM"},
    }
    return {"schema": SCHEMA + ".document.v1", "result": result, "result_sha256": digest(result)}


def self_test() -> dict[str, Any]:
    base = {"box": ["0", "1", "0", "1", "0", "1"], "credit": 0, "flag": False}
    strict_tree(base)
    need(str(Fraction("-47967/128000")) == "-47967/128000", "fraction exact")
    mutations = []
    for candidate in (
        {**base, "credit": False},
        {**base, "flag": 0},
        {**base, "box": ["0", "1", "0", "1", "0", "2/2"]},
    ):
        rejected = False
        try:
            need(type(candidate["credit"]) is int, "credit type")
            need(type(candidate["flag"]) is bool, "flag type")
            fractions(candidate["box"], "mutation")
        except (AuditBlocked, ValueError, ZeroDivisionError):
            rejected = True
        mutations.append(rejected)
    need(all(mutations), "self-test mutations")
    a = digest({"input": "a", "result": "BLOCKED"})
    b = digest({"input": "b", "result": "BLOCKED"})
    need(a != b, "input-bound digest")
    return {"status": "PASS", "mutations_rejected": len(mutations), "distinct_input_commitments": 2}


def main() -> int:
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--print-contract", action="store_true")
    group.add_argument("--self-test", action="store_true")
    group.add_argument("--full-replay", action="store_true")
    args = parser.parse_args()
    if args.print_contract:
        output = {"schema": SCHEMA, "status": STATUS, "pins": [{"label": x[0], "filename": x[1], "size": x[2], "sha256": x[3], "role": x[4]} for x in PINS], "writes_files": False, "executes_or_imports_upstream": False}
    elif args.self_test:
        output = self_test()
    else:
        output = build()
    print(json.dumps(output, sort_keys=True, separators=(",", ":"), ensure_ascii=True, allow_nan=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
