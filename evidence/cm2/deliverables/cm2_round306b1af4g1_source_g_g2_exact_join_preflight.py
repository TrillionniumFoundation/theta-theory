#!/usr/bin/env python3
"""Round306B1AF4G1 exact Source-G G2 identity-join preflight.

This program is a read-only, zero-credit full replay.  It independently parses
the pinned R220/R234/R235/R236/R242/R245/R248/R264, B0, and B1G0 bytes and
reconstructs the complete G2 identity joins and anti-joins.  It neither imports
nor executes an upstream producer, does not define normalized support, and does
not prove graph existence, set equality, physical incidence, transition, pair
routing, maximality, or CM2.

``--print-contract`` and ``--self-test`` are filesystem inert.  The explicit
``--full-replay`` mode opens every pinned input under one held directory fd,
opens all file fds before hashing, performs two same-fd SHA-256 passes, and then
strictly streams the selected JSON/gzip tables from those same open-file
descriptions.  Candidate and production modes refuse before every filesystem
or output boundary.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import copy
from dataclasses import dataclass
import gzip
import hashlib
import io
import json
import os
from pathlib import Path
import re
import stat
import sys
import tempfile
from typing import Any, BinaryIO, Callable, Final, Iterator, TextIO
from unittest import mock


class PreflightBlocked(RuntimeError):
    """Fail-closed byte, parse, join, count, credit, or mode violation."""


def need(condition: bool, label: str) -> None:
    if not condition:
        raise PreflightBlocked(label)


SCHEMA: Final = "cm2.round306b1af4g1.source-g-g2-exact-join-preflight.v1"
STATUS: Final = "PASS_SEALED_ZERO_CREDIT_READ_ONLY_FULL_REPLAY_PREFLIGHT"
BLOCK_REASON: Final = (
    "Round306B1AF4G1 is a read-only zero-credit preflight; candidate and "
    "production modes are blocked before path inspection, input open, "
    "temporary creation, write, stdout, or stderr"
)
DATA: Final = Path(__file__).parent
HEX64: Final = re.compile(r"^[0-9a-f]{64}$")
IDENTIFIER: Final = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.:/+\-]{0,511}$")
ENCODER: Final = json.JSONEncoder(
    sort_keys=True,
    separators=(",", ":"),
    ensure_ascii=True,
    allow_nan=False,
)


def canonical(value: Any) -> bytes:
    return ENCODER.encode(value).encode("ascii")


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def close_row(payload: dict[str, Any]) -> dict[str, Any]:
    need("row_sha256" not in payload, "row already closed")
    return {**payload, "row_sha256": digest(payload)}


def check_closed_row(row: dict[str, Any], label: str) -> None:
    need(type(row) is dict and type(row.get("row_sha256")) is str, label + ":closed row")
    payload = dict(row)
    claimed = payload.pop("row_sha256")
    need(claimed == digest(payload), label + ":row SHA")


AF2 = "cm2_round306b1af2_source_g_primitive_support_source_partition_freeze_contract.py"
AF3D1 = "cm2_round306b1af3d1_source_g_support_representation_authority_delta_contract.py"
AF4_KERNEL = "cm2_round306b1af4_source_g_normalized_support_symbolic_kernel.py"
AF4_SCHEMA = "cm2_round306b1af4_source_g_normalized_support_representation_typed_schema_contract.py"
AF4D1 = "cm2_round306b1af4d1_source_g_semantic_wire_delta_contract.py"
R220 = "cm2_round220_source_g_round179_resolved_child_boundary_atlas_certificate.json"
R234 = "cm2_round234_source_g_wall_endpoint_order_depth6_materialization_certificate.json"
R235 = "cm2_round235_source_g_single_endpoint_graph_word_key_partition_certificate.json"
R236 = "cm2_round236_source_g_wall_residual_closure_and_root_key_partition_certificate.json"
R242 = "cm2_round242_source_g_outgoing_graph_existence_stratum_materialization_certificate.json"
R245 = "cm2_round245_source_g_retained_graph_mixed_sheet_quotient_certificate.json"
R248 = "cm2_round248_source_g_wall_finite_key_retained_quotient_certificate.json"
R264 = "cm2_round264_source_g_lower_dimensional_endpoint_correction_and_glue_closure_certificate.json"
B0 = "cm2_round306b0_source_g_r306a_universe_support_source_freeze_member_support_source_index.json.gz"
B1_GRAPH = "cm2_round306b1g0_source_g_graph_source_inventory_and_join_freeze_graph_source_inventory.json.gz"
B1_SHEET = "cm2_round306b1g0_source_g_graph_source_inventory_and_join_freeze_graph_sheet_join.json.gz"
B1_SIDE = "cm2_round306b1g0_source_g_graph_source_inventory_and_join_freeze_graph_side_join.json.gz"
B1_CORRECTION = "cm2_round306b1g0_source_g_graph_source_inventory_and_join_freeze_r264_correction_disposition.json.gz"
B1_MEMBER = "cm2_round306b1g0_source_g_graph_source_inventory_and_join_freeze_b0_member_backbinding.json.gz"
B1_GAP = "cm2_round306b1g0_source_g_graph_source_inventory_and_join_freeze_gap.json.gz"


def _pin(
    label: str,
    filename: str,
    exact_size: int,
    source_sha256: str,
    *,
    compressed: bool = False,
) -> dict[str, Any]:
    return {
        "label": label,
        "filename": filename,
        "exact_size": exact_size,
        "source_sha256": source_sha256,
        "compressed": compressed,
    }


INPUT_PINS: Final = (
    _pin("AF2_FINAL", AF2, 52_538, "a91578a8bef1c4a72f940f7ebc71aea4c0ebc1ddac08ddbb3889a2da6cdd00f5"),
    _pin("AF3D1_FINAL", AF3D1, 57_389, "d61fbdc7e6d917c9c451cf63a7640285e900fd08dff76800119ca60ae5e55138"),
    _pin("AF4_KERNEL_FINAL", AF4_KERNEL, 87_237, "c8bb9cf85aace782639859c33625732bf866a7fad34ff31cce58ab84af9f6a6f"),
    _pin("AF4_SCHEMA_FINAL", AF4_SCHEMA, 80_436, "ee095fe5db22c6a4dd0804eca0fb553a132546367dcb37fcd75733050aa52cf9"),
    _pin("AF4D1_FINAL", AF4D1, 84_392, "5082df54ea4c514de906f4a923856adb20c6240c9be33401e784b2513a85f09f"),
    _pin("R220", R220, 294_422_681, "569a7849b53805ff4deca0eff9a6938a897942d3d682dfef27c27559135ce974"),
    _pin("R234", R234, 50_766_450, "6098032cf429855e816190e9345fa531f70e460eca60d75766e7108fc32c6fac"),
    _pin("R235", R235, 67_765_471, "e340fa1a071d85a36b54d10a45ae2fdb9d70b8c90f4c21f054c6fc9505e5e787"),
    _pin("R236", R236, 2_061_199, "b5b9ec358b4837a02218756a034440d8fbc2aa706ca421bedb28aaf785de0217"),
    _pin("R242", R242, 13_734_655, "8d32c381e21c03aad6a531b7e5a527d295783b7e3e38baa1e6bcba20c40db22e"),
    _pin("R245", R245, 20_683_081, "c76662f7cb068127f3612a3655ae720662eead9b9210b5757d771693149883c1"),
    _pin("R248", R248, 205_148_977, "fa48bdfb0056072f80c5809f57362c225f0beb40e1cc4c145f3f072335cdb311"),
    _pin("R264", R264, 406_539_851, "ac9e9451e12621fd236fea39bc686e13b41ade62e5255de9c9cd98230763236f"),
    _pin("B0_MEMBER_SOURCE", B0, 162_499_140, "c9a8649c8473bb6a170187e7f803e95748d2ff2198b1b846d97383dd5f0581af", compressed=True),
    _pin("B1G0_GRAPH", B1_GRAPH, 11_720_893, "5ac33be2b7639e1d30ae14abd5a7cf4cc6d1cc65fb0730e98616434f08921cb0", compressed=True),
    _pin("B1G0_SHEET", B1_SHEET, 13_922_080, "041328aa135a1a67cbbdc8c5d84fe2c1a9bef2231a6cb33668ab05ecd6b227e3", compressed=True),
    _pin("B1G0_SIDE", B1_SIDE, 25_932_945, "d79af13182f99cdb2df6d39731e762b0d145baf79772b99be5069669c5b80ee1", compressed=True),
    _pin("B1G0_CORRECTION", B1_CORRECTION, 140_958, "834b687845a156328873888e405793f52a12df9d6286ae07d8a572c6163a361a", compressed=True),
    _pin("B1G0_MEMBER", B1_MEMBER, 32_731_854, "79382a6d8c3d086aeb29eff9fcb8653f2a73d85d79aab27e71e72cc8b1165a0b", compressed=True),
    _pin("B1G0_GAP", B1_GAP, 23_240_985, "2ba1903e2ce6d44ee623d0ccaacce973f7327e1e36ba8f97d0ab3865f1ec9809", compressed=True),
)
PIN_BY_NAME: Final = {row["filename"]: row for row in INPUT_PINS}


def _table(
    label: str,
    filename: str,
    markers: tuple[str, ...],
    row_count: int,
    rows_sha256: str,
    *,
    row_kind: str = "OBJECT",
    id_field: str | None = None,
    row_ids_sha256: str | None = None,
    row_hashes_sha256: str | None = None,
) -> dict[str, Any]:
    return {
        "label": label,
        "filename": filename,
        "markers": list(markers),
        "row_count": row_count,
        "rows_sha256": rows_sha256,
        "row_kind": row_kind,
        "id_field": id_field,
        "row_ids_sha256": row_ids_sha256,
        "row_hashes_sha256": row_hashes_sha256,
    }


TABLE_SPECS: Final = (
    _table("R220_SPLIT", R220, ('"one_step_split_interface_rows":', '"rows":['), 13_076, "221b5568223c452c9c590157afd592dfdc0f244e1322c275d55263b747d18f57", row_kind="ARRAY"),
    _table("R234_FRONTIER", R234, ('"depth6_frontier_rows":[',), 38_376, "a1b3bf193ad10045f52244c3e40c52f78e0aeacffa3ba52c262bc8912fc9b5a6"),
    _table("R235_GRAPH", R235, ('"single_endpoint_graph_partition_rows":[',), 38_328, "e9a3794540170bf013160fb713acfbb1a65d42afedfb7b972cbfdad290549731"),
    _table("R236_GRAPH", R236, ('"double_endpoint_partition_rows":[',), 16, "68f41212de0da7f3468a321a682978daa052cb65a611d756a901ca095bcc0bf6"),
    _table("R242_PATCH", R242, ('"formal_positive_2D_transition_sheet_patch_ledger":', '"rows":['), 264, "aaf7a94af40427dd8e1b805f2aa5c8c0532e7dc5b2420c803e165d39ba5c0a0f"),
    _table("R245_NODE", R245, ('"formal_retained_stratum_node_ledger":', '"rows":['), 3_664, "38583b1aa3f37e37dc03c2b59b2a31c18346462d3d918e001040d6651b11401b"),
    _table("R245_EDGE", R245, ('"formal_mixed_sheet_physical_edge_ledger":', '"rows":['), 3_664, "08da8a6331675f0fbb3fe6a01a9310dee8283f7de2673a7b08144bbf9f08e765"),
    _table("R248_BULK", R248, ('"formal_wall_positive_volume_bulk_ledger":', '"rows":['), 88_936, "aff5ea1401a6919529d1d54fe54bb9b8d378456fa48f88a75043505b5ee7b8b0"),
    _table("R248_SHEET", R248, ('"formal_wall_half_open_sheet_owner_ledger":', '"rows":['), 38_360, "e61754dc51732c4c82876d1c2e83fa040747d23253addd64350728169f5ae44b"),
    _table("R264_CORRECTION", R264, ('"formal_endpoint_empty_branch_correction_disposition_ledger":', '"rows":['), 400, "fdf499ca22f287866a24685a7671f8cfe950015be72c3da03db2331db7e38285"),
    _table("B0_MEMBER", B0, ('"member_support_source_rows":[',), 564_492, "c7dfb5534fddeb22fffb81bf539fe44d837aced46577aa5f490a0ae14aba77f5"),
    _table("B1_GRAPH", B1_GRAPH, ('"graph_source_inventory_rows":[',), 38_624, "beda6faaf7d3be25075d8f2a7f292cba97f591d6255758b6b16efc141339673f", id_field="Round306B1G0_graph_source_inventory_row_id", row_ids_sha256="982ee86845f92368cee72b74c52e401eecfb6dd225a4b198910b89ce34a8a7dc", row_hashes_sha256="7fde3bb652a469eb3b04fe31a80c365d010d914700348954c5d917ac1162dace"),
    _table("B1_SHEET", B1_SHEET, ('"graph_sheet_join_rows":[',), 38_624, "9238a05af9a97002488576d3648ce06ee750858f156638c314ba2e0a24fe3e1f", id_field="Round306B1G0_graph_sheet_join_row_id", row_ids_sha256="b36ca314b15b8b8297dfeda9cb4fe37360ff20339e7603a6388ac172cfb87300", row_hashes_sha256="a3c606a9ba302ced5593d941529946729da5d160a32384ca37060b20011a01f5"),
    _table("B1_SIDE", B1_SIDE, ('"graph_side_join_rows":[',), 76_848, "43ee8ffd2b77231c43c0af10198bbcc1f1def12f2e6bfd28f82c66ea26a207b2", id_field="Round306B1G0_graph_side_join_row_id", row_ids_sha256="9e2a2c015372aa22e5f2cfa1f11ae268496831b3118da5bd5087fc6d7f403f53", row_hashes_sha256="2090d073d45f0097df68a60b36085786de0db51d76219b562734465bbf6daff6"),
    _table("B1_CORRECTION", B1_CORRECTION, ('"r264_correction_disposition_rows":[',), 400, "a3df5bc8c8a86ea6958daefa7ec9b99013a04152378e5bcb18991ec4860cac67", id_field="Round306B1G0_R264_correction_disposition_row_id", row_ids_sha256="b3dec2b9ef34fd5ebc3701201593ca90146f6d6150e5b593284a2a974a1d8caf", row_hashes_sha256="f172394acdc909f6bc58f59fd1f361c4a4c5b00d06b2a8e8369b7638a6e6c592"),
    _table("B1_MEMBER", B1_MEMBER, ('"b0_member_backbinding_rows":[',), 115_456, "35189ef67c69078e44bbd440be37ef870935a8fd67817501ae995cceae383ea6", id_field="Round306B1G0_B0_member_backbinding_row_id", row_ids_sha256="ff6c659209636eec5235a375e8f8ba1cd5bf69c39df6630e6dfaeb95b0945d72", row_hashes_sha256="88026547b175b4ee968f738fe1276163d364b4482d164dbc2e84377039088eae"),
    _table("B1_GAP", B1_GAP, ('"gap_rows":[',), 154_096, "d47d29e9eccc04374851cf12a3bc08fbe62837673fe8beb5dd1c9382337ad27b", id_field="Round306B1G0_gap_row_id", row_ids_sha256="f1c3bf0bb9991f1298a3bc8ce90d55871122ef81b679f32fca21b81087ee1421", row_hashes_sha256="ca9e836b8ca114ba2843a9196748128b6194adb3bd801bb9a28dfff44d28af35"),
)
TABLE_BY_LABEL: Final = {row["label"]: row for row in TABLE_SPECS}

EXPECTED_COUNTS: Final = {
    "R220_interfaces": 13_076,
    "R234_frontiers": 38_376,
    "graph_roots": 38_624,
    "R242_graphs": 264,
    "R235_graphs": 38_328,
    "R236_partitions": 16,
    "R236_graphs": 32,
    "sheet_references": 38_624,
    "sheet_distinct_members": 38_624,
    "side_references": 76_848,
    "side_distinct_members": 76_832,
    "R245_sheet_members": 264,
    "R245_side_references": 528,
    "R245_side_members": 528,
    "R248_sheet_members": 38_360,
    "R248_side_references": 76_320,
    "R248_side_members": 76_304,
    "R235_side_references": 76_256,
    "R236_side_references": 64,
    "R236_side_members": 48,
    "R264_corrections": 400,
    "R264_empty_absent": 184,
    "R264_empty_present": 216,
    "B0_G2_members": 115_456,
    "gaps": 154_096,
    "natural_G2_features": 154_080,
}

EXPECTED_STREAM_COMMITMENTS: Final = {
    "B0_G2_backbinding_stream": {
        "row_count": 115_456,
        "rows_sha256": "4f50fbd3ebabacd4a16b6573d24610bf5722b99dccbc6e8f03c6150126fd1e7b",
    },
    "R264_consumption_stream": {
        "row_count": 400,
        "rows_sha256": "b3f3f0bc9ea8ca0e4df6f46f96ce50820a8b04f0c2742466ee5b2fa403368b60",
    },
    "graph_natural_stream": {
        "row_count": 38_624,
        "rows_sha256": "91d733f8d511d3e1e2371679d1eea3aeb398e10c488e7c63e5b1424125f261a3",
    },
    "natural_G2_feature_stream": {
        "row_count": 154_080,
        "rows_sha256": "c6e3217fde2e17e50e09e2a5d344f23ffcdf837f471e9e3acb4ce4346ba5a62a",
    },
    "sheet_member_stream": {
        "row_count": 38_624,
        "rows_sha256": "a7a1a33db03ea346c86e49e4e457491c32b2a84ca20934357bac5947724f0a6b",
    },
    "side_member_multiplicity_stream": {
        "row_count": 76_832,
        "rows_sha256": "7d84a71fa03b3e3cd52ea4b846666a985a9348c9ce66c62a9ace913fe5be88ef",
    },
    "side_reference_stream": {
        "row_count": 76_848,
        "rows_sha256": "e602ceedd37669f20f696cc7cebda300add6c49e47d222d8a5cbac301a1673e6",
    },
}
EXPECTED_REPLAY_DIGEST: Final = "830cbfde087d3cff03cc852155bdb1e7354edb4b04ebd2212719de69fa284b47"


def unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        need(key not in result, "duplicate JSON key:" + key)
        result[key] = value
    return result


def _reject_number(label: str, value: str) -> Any:
    raise PreflightBlocked(label + ":" + value)


STRICT_DECODER: Final = json.JSONDecoder(
    object_pairs_hook=unique_object,
    parse_float=lambda value: _reject_number("float", value),
    parse_constant=lambda value: _reject_number("constant", value),
)


def _seek_marker(stream: TextIO, marker: str, initial: str = "") -> str:
    need(marker != "", "nonempty marker")
    buffer = initial
    while True:
        position = buffer.find(marker)
        if position >= 0:
            return buffer[position + len(marker):]
        block = stream.read(1 << 20)
        need(bool(block), "missing JSON marker:" + marker)
        keep = max(0, len(marker) - 1)
        buffer = (buffer[-keep:] if keep else "") + block


def iter_strict_json_rows(
    stream: TextIO,
    initial: str = "",
    *,
    row_kind: str = "OBJECT",
    row_limit: int = 1 << 25,
) -> Iterator[Any]:
    """Strict incremental parser for one already-located JSON array."""

    need(row_kind in {"OBJECT", "ARRAY"}, "known row kind")
    buffer = initial
    first = True
    after_comma = False
    while True:
        buffer = buffer.lstrip()
        while not buffer:
            block = stream.read(1 << 20)
            need(bool(block), "truncated JSON row array")
            buffer += block
            buffer = buffer.lstrip()
        if buffer[0] == "]":
            need(not after_comma, "trailing JSON array comma")
            return
        if not first:
            need(buffer[0] == ",", "missing JSON row comma")
            buffer = buffer[1:].lstrip()
            after_comma = True
            while not buffer:
                block = stream.read(1 << 20)
                need(bool(block), "truncated JSON row after comma")
                buffer += block
                buffer = buffer.lstrip()
            need(buffer[0] != "]", "trailing JSON array comma")
        else:
            need(buffer[0] != ",", "leading JSON array comma")
        while True:
            try:
                row, end = STRICT_DECODER.raw_decode(buffer)
                break
            except json.JSONDecodeError:
                need(len(buffer) <= row_limit, "JSON row size bound")
                block = stream.read(1 << 20)
                need(bool(block), "invalid or truncated JSON row")
                buffer += block
        need(type(row) is (dict if row_kind == "OBJECT" else list), "JSON row kind")
        yield row
        buffer = buffer[end:]
        first = False
        after_comma = False


class ListHash:
    """Canonical JSON-list count and SHA-256 without materializing the list."""

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


def _fingerprint(info: os.stat_result) -> tuple[int, ...]:
    return (
        info.st_dev,
        info.st_ino,
        info.st_mode,
        info.st_nlink,
        info.st_size,
        info.st_mtime_ns,
        info.st_ctime_ns,
    )


def _directory_identity(info: os.stat_result) -> tuple[int, int, int]:
    return info.st_dev, info.st_ino, info.st_mode


def _hash_fd(fd: int) -> tuple[int, str]:
    os.lseek(fd, 0, os.SEEK_SET)
    total = 0
    state = hashlib.sha256()
    while True:
        block = os.read(fd, 1 << 20)
        if not block:
            break
        total += len(block)
        state.update(block)
    return total, state.hexdigest()


class HeldInputs:
    """Open, pin, retain, parse, and globally re-audit every input fd."""

    def __init__(self) -> None:
        self.dirfd = -1
        self.directory_before: os.stat_result | None = None
        self.fds: dict[str, int] = {}
        self.infos: dict[str, os.stat_result] = {}
        self.verification_rows: list[dict[str, Any]] = []

    def __enter__(self) -> "HeldInputs":
        directory_text = os.fspath(DATA)
        self.directory_before = os.stat(directory_text, follow_symlinks=False)
        need(stat.S_ISDIR(self.directory_before.st_mode), "input directory")
        flags = os.O_RDONLY | getattr(os, "O_DIRECTORY", 0) | getattr(os, "O_CLOEXEC", 0) | getattr(os, "O_NOFOLLOW", 0)
        self.dirfd = os.open(directory_text, flags)
        need(_directory_identity(os.fstat(self.dirfd)) == _directory_identity(self.directory_before), "directory open race")
        try:
            for pin in INPUT_PINS:
                name = pin["filename"]
                need(name == os.path.basename(name) and name not in ("", ".", ".."), "input basename")
                named = os.stat(name, dir_fd=self.dirfd, follow_symlinks=False)
                need(stat.S_ISREG(named.st_mode) and named.st_nlink == 1, "regular nlink1 input:" + name)
                need(named.st_size == pin["exact_size"], "input size:" + name)
                fd = os.open(name, os.O_RDONLY | getattr(os, "O_CLOEXEC", 0) | getattr(os, "O_NOFOLLOW", 0), dir_fd=self.dirfd)
                try:
                    held = os.fstat(fd)
                    need(_fingerprint(named) == _fingerprint(held), "input open race:" + name)
                except Exception:
                    os.close(fd)
                    raise
                self.fds[name] = fd
                self.infos[name] = held
            # Every descriptor is open before the first byte hash.
            for pin in INPUT_PINS:
                name = pin["filename"]
                fd = self.fds[name]
                before = self.infos[name]
                size1, sha1 = _hash_fd(fd)
                need(_fingerprint(os.fstat(fd)) == _fingerprint(before), "pass1 stability:" + name)
                size2, sha2 = _hash_fd(fd)
                need(_fingerprint(os.fstat(fd)) == _fingerprint(before), "pass2 stability:" + name)
                need(size1 == size2 == pin["exact_size"], "two-pass size:" + name)
                need(sha1 == sha2 == pin["source_sha256"], "two-pass SHA:" + name)
                self.verification_rows.append({
                    "label": pin["label"],
                    "filename": name,
                    "exact_size": pin["exact_size"],
                    "source_sha256": pin["source_sha256"],
                    "pass1_sha256": sha1,
                    "pass2_sha256": sha2,
                    "regular_file": True,
                    "link_count_one": True,
                    "held_fd_identity_stable": True,
                })
            return self
        except Exception:
            self.close()
            raise

    def iter_table(self, spec: dict[str, Any]) -> Iterator[Any]:
        name = spec["filename"]
        fd = self.fds[name]
        before = self.infos[name]
        need(_fingerprint(os.fstat(fd)) == _fingerprint(before), "preparse fd stability:" + name)
        os.lseek(fd, 0, os.SEEK_SET)
        duplicate = os.dup(fd)
        raw = os.fdopen(duplicate, "rb", closefd=True)
        binary: BinaryIO = gzip.GzipFile(fileobj=raw, mode="rb") if PIN_BY_NAME[name]["compressed"] else raw
        text = io.TextIOWrapper(binary, encoding="utf-8", errors="strict", newline="")
        try:
            buffer = ""
            for marker in spec["markers"]:
                buffer = _seek_marker(text, marker, buffer)
            yield from iter_strict_json_rows(text, buffer, row_kind=spec["row_kind"])
            # Drain to EOF so gzip CRC/trailer and UTF-8 decoding are checked.
            while text.read(1 << 20):
                pass
            need(_fingerprint(os.fstat(fd)) == _fingerprint(before), "postparse fd stability:" + name)
        finally:
            try:
                text.close()
            finally:
                if not raw.closed:
                    raw.close()

    def global_reaudit(self) -> None:
        need(self.directory_before is not None and self.dirfd >= 0, "held inputs active")
        for pin in INPUT_PINS:
            name = pin["filename"]
            before = self.infos[name]
            fd = self.fds[name]
            need(_fingerprint(os.fstat(fd)) == _fingerprint(before), "final held fd stability:" + name)
            named = os.stat(name, dir_fd=self.dirfd, follow_symlinks=False)
            need(_fingerprint(named) == _fingerprint(before), "final path binding:" + name)
        current_dir = os.fstat(self.dirfd)
        path_dir = os.stat(os.fspath(DATA), follow_symlinks=False)
        need(_directory_identity(current_dir) == _directory_identity(path_dir) == _directory_identity(self.directory_before), "final directory binding")

    def close(self) -> None:
        for fd in reversed(list(self.fds.values())):
            try:
                os.close(fd)
            except OSError:
                pass
        self.fds.clear()
        if self.dirfd >= 0:
            try:
                os.close(self.dirfd)
            except OSError:
                pass
            self.dirfd = -1

    def __exit__(self, exc_type: Any, exc: Any, traceback: Any) -> None:
        try:
            if exc_type is None:
                self.global_reaudit()
        finally:
            self.close()


class ReplayContext:
    def __init__(self, inputs: HeldInputs) -> None:
        self.inputs = inputs
        self.tables: dict[str, dict[str, Any]] = {}

    def rows(self, label: str) -> Iterator[Any]:
        need(label not in self.tables, "table consumed exactly once:" + label)
        spec = TABLE_BY_LABEL[label]
        rows = ListHash()
        ids = ListHash() if spec["id_field"] is not None else None
        hashes = ListHash() if spec["row_hashes_sha256"] is not None else None
        for row in self.inputs.iter_table(spec):
            rows.add(row)
            if ids is not None:
                need(type(row) is dict and type(row.get(spec["id_field"])) is str, "table row ID:" + label)
                ids.add(row[spec["id_field"]])
            if hashes is not None:
                need(type(row) is dict and type(row.get("row_sha256")) is str, "table row hash:" + label)
                hashes.add(row["row_sha256"])
            yield row
        observed = {
            "row_count": rows.count,
            "rows_sha256": rows.finish(),
        }
        if ids is not None:
            observed["row_ids_sha256"] = ids.finish()
        if hashes is not None:
            observed["row_hashes_sha256"] = hashes.finish()
        need(observed["row_count"] == spec["row_count"], "table row count:" + label)
        need(observed["rows_sha256"] == spec["rows_sha256"], "table rows SHA:" + label)
        if ids is not None:
            need(observed["row_ids_sha256"] == spec["row_ids_sha256"], "table IDs SHA:" + label)
        if hashes is not None:
            need(observed["row_hashes_sha256"] == spec["row_hashes_sha256"], "table hashes SHA:" + label)
        self.tables[label] = observed


@dataclass(frozen=True)
class Feature:
    member_id: str
    package: str
    filename: str
    table: str
    row_sha256: str
    feature_kind: str
    role: str
    branch: str | None
    official_key_id: str
    source_edge_id: str | None = None
    source_edge_sha256: str | None = None


@dataclass(frozen=True)
class Graph:
    graph_id: str
    family: str
    source_round: int
    filename: str
    table: str
    source_row_id: str
    source_row_sha256: str
    interface_id: str
    endpoint_factor: str
    official_key_ids: tuple[str, ...]
    sheet: Feature
    sides: tuple[Feature, ...]
    correction_source_id: str | None = None


def graph_inventory_id(graph_id: str) -> str:
    return "round306b1g0-graph-source:" + digest(graph_id)


def backbinding_id(member_id: str) -> str:
    return "round306b1g0-b0-backbinding:" + digest(member_id)


def _feature(
    row: dict[str, Any],
    *,
    package: str,
    filename: str,
    table: str,
    id_field: str,
    kind: str,
    role: str,
    branch: str | None,
    key_field: str = "official_key_id",
    edge: dict[str, Any] | None = None,
) -> Feature:
    check_closed_row(row, package + ":" + kind)
    return Feature(
        member_id=row[id_field],
        package=package,
        filename=filename,
        table=table,
        row_sha256=row["row_sha256"],
        feature_kind=kind,
        role=role,
        branch=branch,
        official_key_id=row[key_field],
        source_edge_id=(edge["mixed_sheet_edge_id"] if edge is not None else None),
        source_edge_sha256=(edge.get("row_sha256") if edge is not None else None),
    )


def load_coordinate_authorities(context: ReplayContext) -> tuple[set[str], dict[str, str]]:
    interfaces: set[str] = set()
    for row in context.rows("R220_SPLIT"):
        need(type(row) is list and len(row) == 20, "R220 packed split row")
        interface = row[0]
        need(type(interface) is str and interface not in interfaces, "unique R220 interface")
        need(row[16] is False and row[17] == row[18] == row[19] == 0, "R220 nonpromotion")
        interfaces.add(interface)
    need(len(interfaces) == EXPECTED_COUNTS["R220_interfaces"], "R220 interface census")

    frontiers: dict[str, str] = {}
    for row in context.rows("R234_FRONTIER"):
        need(type(row) is dict, "R234 row")
        frontier = row["frontier_row_id"]
        interface = row["Round220_split_interface_id"]
        need(frontier not in frontiers and interface in interfaces, "R234 frontier identity")
        need(row["global_exact_key_disposition_credit"] == 0, "R234 zero global credit")
        frontiers[frontier] = interface
    need(len(frontiers) == EXPECTED_COUNTS["R234_frontiers"], "R234 frontier census")
    return interfaces, frontiers


def load_r264_corrections(context: ReplayContext) -> dict[str, dict[str, Any]]:
    corrections: dict[str, dict[str, Any]] = {}
    labels: Counter[str] = Counter()
    dispositions: Counter[str] = Counter()
    invalid_edges = 0
    for row in context.rows("R264_CORRECTION"):
        check_closed_row(row, "R264 correction")
        source = row["source_partition_row_id"]
        need(source not in corrections, "unique R264 correction source")
        need(row["empty_branch_Round250_Round251_Round252_accepted_edge_incidence_count"] == 0, "R264 empty incidence zero")
        labels[row["empty_branch_label"]] += 1
        dispositions[row["disposition"]] += 1
        invalid_edges += row["invalid_Round248_owner_edge_id"] is not None
        corrections[source] = row
    need(len(corrections) == EXPECTED_COUNTS["R264_corrections"], "R264 correction census")
    need(labels == {"EVENT_ABSENT": 184, "EVENT_PRESENT": 216}, "R264 184+216")
    need(invalid_edges == 184, "R264 invalid absent edge census")
    need(
        dispositions
        == {
            "PRUNE_EMPTY_ABSENT_BULK_NODE_AND_INVALID_OWNER_EDGE__RETAIN_T0_SHEET": 184,
            "DROP_EMPTY_PRESENT_SINGLETON_PHANTOM_COMPONENT": 216,
        },
        "R264 disposition census",
    )
    return corrections


def load_r242_r245_graphs(
    context: ReplayContext,
    interfaces: set[str],
) -> list[Graph]:
    patches: dict[str, dict[str, Any]] = {}
    for row in context.rows("R242_PATCH"):
        check_closed_row(row, "R242 patch")
        interface = row["Round220_split_interface_id"]
        need(interface in interfaces and interface not in patches, "R242 interface")
        need(row["local_dimension"] == 2 and row["three_dimensional_coordinate_volume"] == 0, "R242 dimension")
        need(row["physical_component_credit"] == row["maximal_physical_component_credit"] == row["global_exact_key_fibre_credit"] == 0, "R242 nonpromotion")
        patches[interface] = row
    need(len(patches) == 264, "R242 patch census")

    nodes: dict[str, dict[str, dict[str, Any]]] = defaultdict(dict)
    relevant_kinds = {
        "OWNER_OPEN_BULK",
        "SHADOW_OPEN_BULK",
        "HALF_OPEN_TRANSITION_SHEET",
    }
    relevant_node_count = 0
    for row in context.rows("R245_NODE"):
        check_closed_row(row, "R245 node")
        kind = row["stratum_kind"]
        if kind not in relevant_kinds:
            continue
        interface = row["Round220_split_interface_id"]
        need(interface in patches and kind not in nodes[interface], "R245 graph-node routing")
        nodes[interface][kind] = row
        relevant_node_count += 1
    need(relevant_node_count == 792 and set(nodes) == set(patches), "R245 relevant node census")

    edges: dict[str, list[dict[str, Any]]] = defaultdict(list)
    relevant_edge_count = 0
    for row in context.rows("R245_EDGE"):
        check_closed_row(row, "R245 edge")
        if row["edge_kind"] not in {
            "OWNER_BULK_TO_HALF_OPEN_SHEET",
            "SHADOW_BULK_TO_HALF_OPEN_SHEET",
        }:
            continue
        interface = row["Round220_split_interface_id"]
        need(interface in patches, "R245 edge interface")
        edges[interface].append(row)
        relevant_edge_count += 1
    need(relevant_edge_count == 528 and set(edges) == set(patches), "R245 relevant edge census")

    output: list[Graph] = []
    for interface in sorted(patches):
        patch = patches[interface]
        by_kind = nodes[interface]
        need(set(by_kind) == relevant_kinds and len(edges[interface]) == 2, "R245 exact local join group")
        sheet = by_kind["HALF_OPEN_TRANSITION_SHEET"]
        owner = by_kind["OWNER_OPEN_BULK"]
        shadow = by_kind["SHADOW_OPEN_BULK"]
        edge_by_bulk: dict[str, dict[str, Any]] = {}
        for edge in edges[interface]:
            endpoints = {edge["left_node_id"], edge["right_node_id"]}
            need(sheet["retained_stratum_node_id"] in endpoints, "R245 edge contains sheet")
            endpoints.remove(sheet["retained_stratum_node_id"])
            need(len(endpoints) == 1, "R245 edge has one bulk endpoint")
            bulk = next(iter(endpoints))
            need(
                bulk in {owner["retained_stratum_node_id"], shadow["retained_stratum_node_id"]}
                and bulk not in edge_by_bulk,
                "R245 exact bulk endpoint",
            )
            edge_by_bulk[bulk] = edge
        need(
            patch["official_key_id"]
            == sheet["official_key_id"]
            == owner["official_key_id"]
            == shadow["official_key_id"],
            "R242/R245 key metadata consistency after lineage join",
        )
        sheet_feature = _feature(
            sheet,
            package="R245",
            filename=R245,
            table="formal_retained_stratum_node_ledger",
            id_field="retained_stratum_node_id",
            kind="SHEET",
            role="GRAPH_SHEET",
            branch=None,
        )
        side_features = tuple(
            _feature(
                row,
                package="R245",
                filename=R245,
                table="formal_retained_stratum_node_ledger",
                id_field="retained_stratum_node_id",
                kind="POSITIVE_3D_SIDE",
                role=role,
                branch=role,
                edge=edge_by_bulk[row["retained_stratum_node_id"]],
            )
            for role, row in (("OWNER_OPEN_BULK", owner), ("SHADOW_OPEN_BULK", shadow))
        )
        output.append(
            Graph(
                graph_id=patch["transition_sheet_patch_row_id"],
                family="R242_UNIQUE_TRANSITION_GRAPH",
                source_round=242,
                filename=R242,
                table="formal_positive_2D_transition_sheet_patch_ledger",
                source_row_id=patch["transition_sheet_patch_row_id"],
                source_row_sha256=patch["row_sha256"],
                interface_id=interface,
                endpoint_factor="transition_graph",
                official_key_ids=(patch["official_key_id"],),
                sheet=sheet_feature,
                sides=side_features,
            )
        )
    need(len(output) == 264 and sum(len(row.sides) for row in output) == 528, "complete R242/R245 join")
    return output


def load_r248_graph_features(
    context: ReplayContext,
) -> tuple[
    dict[tuple[str, str, str], dict[str, Any]],
    dict[str, dict[str, dict[str, Any]]],
]:
    sheets: dict[tuple[str, str, str], dict[str, Any]] = {}
    sheet_histogram: Counter[str] = Counter()
    for row in context.rows("R248_SHEET"):
        check_closed_row(row, "R248 sheet")
        kind = row["source_partition_kind"]
        need(kind in {"ROUND235_SINGLE_ENDPOINT_GRAPH_SHEET", "ROUND236_DOUBLE_ENDPOINT_GRAPH_SHEET"}, "R248 sheet kind")
        key = (kind, row["source_partition_row_id"], row["endpoint_factor"])
        need(key not in sheets, "unique R248 sheet")
        sheets[key] = row
        sheet_histogram[kind] += 1
    need(
        sheet_histogram
        == {
            "ROUND235_SINGLE_ENDPOINT_GRAPH_SHEET": 38_328,
            "ROUND236_DOUBLE_ENDPOINT_GRAPH_SHEET": 32,
        },
        "R248 sheet census",
    )

    bulks: dict[str, dict[str, dict[str, Any]]] = defaultdict(dict)
    bulk_histogram: Counter[str] = Counter()
    for row in context.rows("R248_BULK"):
        check_closed_row(row, "R248 bulk")
        kind = row["source_partition_kind"]
        if kind not in {
            "ROUND235_SINGLE_ENDPOINT_GRAPH_BRANCH",
            "ROUND236_DOUBLE_ENDPOINT_ARRANGEMENT_BRANCH",
        }:
            continue
        source = row["source_partition_row_id"]
        branch = row["branch_label"]
        need(branch not in bulks[source], "unique R248 branch")
        bulks[source][branch] = row
        bulk_histogram[kind] += 1
    need(
        bulk_histogram
        == {
            "ROUND235_SINGLE_ENDPOINT_GRAPH_BRANCH": 76_656,
            "ROUND236_DOUBLE_ENDPOINT_ARRANGEMENT_BRANCH": 48,
        },
        "R248 relevant bulk census",
    )
    return sheets, bulks


def _r248_sheet_feature(row: dict[str, Any]) -> Feature:
    return _feature(
        row,
        package="R248",
        filename=R248,
        table="formal_wall_half_open_sheet_owner_ledger",
        id_field="wall_sheet_node_id",
        kind="SHEET",
        role="GRAPH_SHEET",
        branch=None,
        key_field="owner_official_key_id",
    )


def _r248_side_feature(
    row: dict[str, Any],
    role: str,
    edge: dict[str, Any] | None = None,
) -> Feature:
    return _feature(
        row,
        package="R248",
        filename=R248,
        table="formal_wall_positive_volume_bulk_ledger",
        id_field="wall_bulk_node_id",
        kind="POSITIVE_3D_SIDE",
        role=role,
        branch=row["branch_label"],
        edge=edge,
    )


def load_r235_r236_r248_graphs(
    context: ReplayContext,
    interfaces: set[str],
    frontiers: dict[str, str],
    corrections: dict[str, dict[str, Any]],
) -> list[Graph]:
    sheets, bulks = load_r248_graph_features(context)
    output: list[Graph] = []
    seen_single_sources: set[str] = set()
    seen_corrections: set[str] = set()
    single_sides = 0
    for row in context.rows("R235_GRAPH"):
        source = row["endpoint_graph_partition_row_id"]
        frontier = row["Round234_frontier_row_id"]
        interface = row["Round220_split_interface_id"]
        endpoint = row["active_endpoint_factor"]
        need(source not in seen_single_sources and endpoint in {"source", "target"}, "R235 identity")
        need(interface in interfaces and frontiers.get(frontier) == interface, "R235 R234/R220 join")
        seen_single_sources.add(source)
        sheet = sheets[("ROUND235_SINGLE_ENDPOINT_GRAPH_SHEET", source, endpoint)]
        branches = bulks[source]
        need(set(branches) == {"EVENT_ABSENT", "EVENT_PRESENT"}, "R235 exact two branches")
        need(
            sheet["Round220_split_interface_id"] == interface
            and all(item["Round220_split_interface_id"] == interface for item in branches.values()),
            "R235/R248 interface join",
        )
        need(sheet["owner_wall_bulk_node_id"] == branches["EVENT_ABSENT"]["wall_bulk_node_id"], "R248 absent owner")
        correction = corrections.get(source)
        kept = dict(branches)
        if correction is not None:
            need(correction["Round220_split_interface_id"] == interface, "R264 interface backjoin")
            empty = correction["empty_branch_label"]
            need(
                correction["empty_wall_bulk_node_id"] == branches[empty]["wall_bulk_node_id"]
                and correction["retained_t0_sheet_node_id"] == sheet["wall_sheet_node_id"],
                "R264 exact node/sheet join",
            )
            if empty == "EVENT_ABSENT":
                need(correction["invalid_Round248_owner_edge_id"] == sheet["owner_mixed_sheet_edge_id"], "R264 invalid owner edge")
            else:
                need(correction["invalid_Round248_owner_edge_id"] is None, "R264 present phantom edge null")
            del kept[empty]
            seen_corrections.add(source)
        need(sheet["owner_official_key_id"] == row["event_absent_signature"]["official_key_id"], "R235 sheet metadata key")
        for branch, bulk in branches.items():
            signature = row["event_absent_signature" if branch == "EVENT_ABSENT" else "event_present_signature"]
            need(bulk["official_key_id"] == signature["official_key_id"], "R235 branch metadata key")
        absent_edge_valid = correction is None or correction["empty_branch_label"] != "EVENT_ABSENT"
        sides = tuple(
            _r248_side_feature(
                bulk,
                branch,
                {"mixed_sheet_edge_id": sheet["owner_mixed_sheet_edge_id"]}
                if branch == "EVENT_ABSENT" and absent_edge_valid
                else None,
            )
            for branch, bulk in sorted(kept.items())
        )
        output.append(
            Graph(
                graph_id=source,
                family="R235_SINGLE_ENDPOINT_GRAPH",
                source_round=235,
                filename=R235,
                table="single_endpoint_graph_partition_rows",
                source_row_id=source,
                source_row_sha256=digest(row),
                interface_id=interface,
                endpoint_factor=endpoint,
                official_key_ids=tuple(
                    sorted(
                        {
                            row["event_absent_signature"]["official_key_id"],
                            row["event_present_signature"]["official_key_id"],
                        }
                    )
                ),
                sheet=_r248_sheet_feature(sheet),
                sides=sides,
                correction_source_id=(source if correction is not None else None),
            )
        )
        single_sides += len(sides)
    need(len(seen_single_sources) == 38_328 and single_sides == 76_256, "complete R235/R248 join")
    need(seen_corrections == set(corrections), "all R264 corrections consumed")

    double_partitions = 0
    double_sides = 0
    for row in context.rows("R236_GRAPH"):
        source = row["double_endpoint_partition_row_id"]
        frontier = row["Round234_frontier_row_id"]
        interface = row["Round220_split_interface_id"]
        need(interface in interfaces and frontiers.get(frontier) == interface, "R236 R234/R220 join")
        need(
            row["source_factor_strict_t_derivative_sign"]
            == row["target_factor_strict_t_derivative_sign"]
            == "STRICT_POSITIVE",
            "R236 routing sign",
        )
        branches = bulks[source]
        need(
            set(branches)
            == {
                "SAME_SIGN_EVENT_ABSENT",
                "NEGATIVE_TO_POSITIVE",
                "POSITIVE_TO_NEGATIVE",
            },
            "R236 exact three branches",
        )
        routing = {"source": "NEGATIVE_TO_POSITIVE", "target": "POSITIVE_TO_NEGATIVE"}
        signatures = {
            "SAME_SIGN_EVENT_ABSENT": row["same_sign_event_absent_signature"],
            "NEGATIVE_TO_POSITIVE": row["negative_to_positive_signature"],
            "POSITIVE_TO_NEGATIVE": row["positive_to_negative_signature"],
        }
        for branch, bulk in branches.items():
            need(
                bulk["Round220_split_interface_id"] == interface
                and bulk["official_key_id"] == signatures[branch]["official_key_id"],
                "R236/R248 branch join",
            )
        for endpoint in ("source", "target"):
            sheet = sheets[("ROUND236_DOUBLE_ENDPOINT_GRAPH_SHEET", source, endpoint)]
            need(
                sheet["Round220_split_interface_id"] == interface
                and sheet["owner_wall_bulk_node_id"]
                == branches["SAME_SIGN_EVENT_ABSENT"]["wall_bulk_node_id"],
                "R236 sheet owner",
            )
            need(sheet["owner_official_key_id"] == signatures["SAME_SIGN_EVENT_ABSENT"]["official_key_id"], "R236 sheet metadata key")
            selected = ("SAME_SIGN_EVENT_ABSENT", routing[endpoint])
            sides = tuple(
                _r248_side_feature(
                    branches[branch],
                    endpoint + ":" + branch,
                    {"mixed_sheet_edge_id": sheet["owner_mixed_sheet_edge_id"]}
                    if branch == "SAME_SIGN_EVENT_ABSENT"
                    else None,
                )
                for branch in selected
            )
            output.append(
                Graph(
                    graph_id="round306b1g0-double-graph:" + digest([source, endpoint]),
                    family="R236_DOUBLE_ENDPOINT_GRAPH",
                    source_round=236,
                    filename=R236,
                    table="double_endpoint_partition_rows",
                    source_row_id=source,
                    source_row_sha256=digest(row),
                    interface_id=interface,
                    endpoint_factor=endpoint,
                    official_key_ids=tuple(sorted({item["official_key_id"] for item in signatures.values()})),
                    sheet=_r248_sheet_feature(sheet),
                    sides=sides,
                )
            )
            double_sides += len(sides)
        double_partitions += 1
    need(double_partitions == 16 and double_sides == 64, "complete R236/R248 join")
    need(len(sheets) == 38_360, "all R248 sheets consumed")
    need(set(bulks) == seen_single_sources | {row.source_row_id for row in output if row.family == "R236_DOUBLE_ENDPOINT_GRAPH"}, "all relevant R248 source groups consumed")
    return output


def bind_b0_members(
    context: ReplayContext,
    graphs: list[Graph],
) -> tuple[dict[str, dict[str, Any]], dict[str, list[Feature]]]:
    references: dict[str, list[Feature]] = defaultdict(list)
    for graph in graphs:
        references[graph.sheet.member_id].append(graph.sheet)
        for side in graph.sides:
            references[side.member_id].append(side)
    need(len(references) == 115_456, "distinct G2 member census")

    bound: dict[str, dict[str, Any]] = {}
    for row in context.rows("B0_MEMBER"):
        check_closed_row(row, "B0 member")
        member = row["member_id"]
        if member not in references:
            continue
        need(member not in bound, "unique targeted B0 member")
        need(row["identity_class"] == "VALID_VIRTUAL_STRATUM" and row["member_identity_preserved"] is True, "B0 virtual identity")
        need(
            row["formal_maximality_credit"]
            == row["formal_fibre_credit"]
            == row["formal_global_disposition_credit"]
            == 0,
            "B0 zero formal credit",
        )
        examples = references[member]
        first = examples[0]
        need(
            all(
                item.package == first.package
                and item.row_sha256 == first.row_sha256
                and item.feature_kind == first.feature_kind
                for item in examples
            ),
            "consistent repeated member reference",
        )
        if first.package == "R245":
            need(row["identity_tranche"] == "INHERITED_ROUND247_VIRTUAL_STRATUM", "B0 R245 tranche")
            need(
                row["inherited_virtual_source_package"] == "R245"
                and row["inherited_virtual_source_row_id"] == member
                and row["inherited_virtual_source_row_sha256"] == first.row_sha256,
                "B0 R245 lineage",
            )
        else:
            tranche = "ROUND248_WALL_SHEET" if first.feature_kind == "SHEET" else "ROUND248_WALL_BULK"
            need(row["identity_tranche"] == tranche, "B0 R248 tranche")
            need(
                row["inherited_virtual_source_package"] is None
                and row["inherited_virtual_source_row_id"] is None
                and row["inherited_virtual_source_row_sha256"] is None,
                "B0 R248 no inherited alias",
            )
        denominator = "VIRTUAL_SHEET" if first.feature_kind == "SHEET" else "VIRTUAL_POSITIVE_3D"
        profile = "HALF_OPEN_2D_SHEET" if first.feature_kind == "SHEET" else "POSITIVE_3D_CARRIER"
        need(row["pair_denominator_class"] == denominator and row["physical_dimension_profile"] == profile, "B0 dimension")
        need(all(row["official_key_id"] == item.official_key_id for item in examples), "B0 key metadata consistency")
        bound[member] = row
    need(set(bound) == set(references), "complete B0 anti-join")
    return bound, references


def zero_credit() -> dict[str, int]:
    return {
        "graph_definition": 0,
        "physical_incidence": 0,
        "full_support": 0,
        "maximality": 0,
        "fibre": 0,
        "global_disposition": 0,
    }


def assert_zero_credit(value: Any, label: str = "root") -> None:
    if type(value) is dict:
        for key, item in value.items():
            if "credit" in key.lower():
                if "credit_zero" in key.lower():
                    need(item is True, label + ":explicit zero-credit flag")
                elif type(item) is dict:
                    need(all(type(number) is int and number == 0 for number in item.values()), label + ":credit map")
                else:
                    need(type(item) is int and item == 0, label + ":credit scalar")
            else:
                assert_zero_credit(item, label + ":" + key)
    elif type(value) is list:
        for index, item in enumerate(value):
            assert_zero_credit(item, label + ":[" + str(index) + "]")


B1G0_SCHEMA: Final = "cm2.round306b1g0.source-g-graph-source-inventory-and-join-freeze.v1"
B1G0_ID_FIELDS: Final = {
    "graph": "Round306B1G0_graph_source_inventory_row_id",
    "sheet": "Round306B1G0_graph_sheet_join_row_id",
    "side": "Round306B1G0_graph_side_join_row_id",
    "correction": "Round306B1G0_R264_correction_disposition_row_id",
    "member": "Round306B1G0_B0_member_backbinding_row_id",
    "gap": "Round306B1G0_gap_row_id",
}
B1G0_LEDGER_LABELS: Final = {
    "graph": "B1_GRAPH",
    "sheet": "B1_SHEET",
    "side": "B1_SIDE",
    "correction": "B1_CORRECTION",
    "member": "B1_MEMBER",
    "gap": "B1_GAP",
}
B1G0_ROW_SCHEMAS: Final = {
    "graph": B1G0_SCHEMA + ".graph-source-inventory-row.v1",
    "sheet": B1G0_SCHEMA + ".graph-sheet-join-row.v1",
    "side": B1G0_SCHEMA + ".graph-side-join-row.v1",
    "correction": B1G0_SCHEMA + ".r264-correction-disposition-row.v1",
    "member": B1G0_SCHEMA + ".b0-member-backbinding-row.v1",
    "gap": B1G0_SCHEMA + ".gap-row.v1",
}


class CommitmentSpool:
    """Reconstruct a ledger commitment without writing or retaining its rows."""

    def __init__(self, kind: str) -> None:
        need(kind in B1G0_ID_FIELDS, "known spool kind")
        self.kind = kind
        self.id_field = B1G0_ID_FIELDS[kind]
        self.rows = ListHash()
        self.ids = ListHash()
        self.hashes = ListHash()
        self.seen_ids: set[str] = set()

    def add(self, payload: dict[str, Any]) -> None:
        need(payload.get("schema") == B1G0_ROW_SCHEMAS[self.kind], "spool row schema:" + self.kind)
        assert_zero_credit(payload, "spool:" + self.kind)
        row = close_row(payload)
        row_id = row[self.id_field]
        need(type(row_id) is str and row_id not in self.seen_ids, "unique spool row ID:" + self.kind)
        self.seen_ids.add(row_id)
        self.rows.add(row)
        self.ids.add(row_id)
        self.hashes.add(row["row_sha256"])

    def metadata(self) -> dict[str, Any]:
        return {
            "row_count": self.rows.count,
            "rows_sha256": self.rows.finish(),
            "row_ids_sha256": self.ids.finish(),
            "row_hashes_sha256": self.hashes.finish(),
        }


def build_expected_b1g0_spools(
    corrections: dict[str, dict[str, Any]],
    graphs: list[Graph],
    b0: dict[str, dict[str, Any]],
    references: dict[str, list[Feature]],
) -> tuple[dict[str, CommitmentSpool], dict[str, Any]]:
    """Independently reproduce all six sealed B1G0 ledger byte streams."""

    spools = {kind: CommitmentSpool(kind) for kind in B1G0_ID_FIELDS}

    for member in sorted(references):
        source = b0[member]
        feature = references[member][0]
        spools["member"].add({
            "schema": B1G0_ROW_SCHEMAS["member"],
            B1G0_ID_FIELDS["member"]: backbinding_id(member),
            "member_id": member,
            "feature_kind": feature.feature_kind,
            "feature_source_package": feature.package,
            "feature_source_filename": feature.filename,
            "feature_source_file_sha256": PIN_BY_NAME[feature.filename]["source_sha256"],
            "feature_source_table": feature.table,
            "feature_source_row_sha256": feature.row_sha256,
            "Round306B0_member_support_source_row_id": source["Round306B0_member_support_source_row_id"],
            "Round306B0_member_support_source_row_sha256": source["row_sha256"],
            "Round306A_component_id": source["Round306A_component_id"],
            "identity_tranche": source["identity_tranche"],
            "physical_dimension_profile": source["physical_dimension_profile"],
            "official_key_id_metadata_only": source["official_key_id"],
            "official_key_used_as_join_or_routing_filter": False,
            "formal_credit": zero_credit(),
        })

    correction_output_ids: dict[str, str] = {}
    for source in sorted(corrections):
        row = corrections[source]
        output_id = "round306b1g0-r264-correction:" + digest(row["endpoint_empty_branch_disposition_row_id"])
        correction_output_ids[source] = output_id
        spools["correction"].add({
            "schema": B1G0_ROW_SCHEMAS["correction"],
            B1G0_ID_FIELDS["correction"]: output_id,
            "R264_correction_disposition_row_id": row["endpoint_empty_branch_disposition_row_id"],
            "R264_correction_disposition_row_sha256": row["row_sha256"],
            "source_partition_row_id": source,
            "empty_branch_label": row["empty_branch_label"],
            "empty_wall_bulk_node_id": row["empty_wall_bulk_node_id"],
            "nonempty_branch_label": row["nonempty_branch_label"],
            "nonempty_wall_bulk_node_id": row["nonempty_wall_bulk_node_id"],
            "retained_t0_sheet_node_id": row["retained_t0_sheet_node_id"],
            "invalid_Round248_owner_edge_id": row["invalid_Round248_owner_edge_id"],
            "disposition": row["disposition"],
            "source_component_count_delta": -1 if row["empty_branch_label"] == "EVENT_PRESENT" else 0,
            "empty_side_join_suppressed": True,
            "official_key_used_as_join_or_routing_filter": False,
            "formal_credit": zero_credit(),
        })

    incidence_family_counts: Counter[str] = Counter()
    for graph in sorted(graphs, key=lambda item: item.graph_id):
        inventory_id = graph_inventory_id(graph.graph_id)
        sheet_join_id = "round306b1g0-graph-sheet:" + digest([graph.graph_id, graph.sheet.member_id])
        spools["graph"].add({
            "schema": B1G0_ROW_SCHEMAS["graph"],
            B1G0_ID_FIELDS["graph"]: inventory_id,
            "graph_id": graph.graph_id,
            "graph_family": graph.family,
            "source_round": graph.source_round,
            "source_filename": graph.filename,
            "source_file_sha256": PIN_BY_NAME[graph.filename]["source_sha256"],
            "source_table": graph.table,
            "source_row_id": graph.source_row_id,
            "source_row_sha256": graph.source_row_sha256,
            "Round220_split_interface_id": graph.interface_id,
            "endpoint_factor": graph.endpoint_factor,
            "graph_local_dimension": 2,
            "graph_three_dimensional_coordinate_volume": 0,
            "graph_sheet_join_row_id": sheet_join_id,
            "graph_side_join_count": len(graph.sides),
            "R264_correction_disposition_row_id": correction_output_ids.get(graph.correction_source_id or ""),
            "official_key_ids_metadata_only": list(graph.official_key_ids),
            "official_key_used_as_join_or_routing_filter": False,
            "source_graph_definition_proved": False,
            "formal_credit": zero_credit(),
        })
        spools["gap"].add({
            "schema": B1G0_ROW_SCHEMAS["gap"],
            B1G0_ID_FIELDS["gap"]: "round306b1g0-gap:graph:" + digest(graph.graph_id),
            "gap_kind": "SOURCE_FREE_GRAPH_DEFINITION_THEOREM_PENDING",
            "graph_source_inventory_row_id": inventory_id,
            "incidence_join_row_id": None,
            "member_id": graph.sheet.member_id,
            "required_closure": "derive and independently interval-verify the source-free graph equation on the complete base cell",
            "formal_credit": zero_credit(),
        })

        sheet_b0 = b0[graph.sheet.member_id]
        spools["sheet"].add({
            "schema": B1G0_ROW_SCHEMAS["sheet"],
            B1G0_ID_FIELDS["sheet"]: sheet_join_id,
            "graph_source_inventory_row_id": inventory_id,
            "graph_id": graph.graph_id,
            "graph_family": graph.family,
            "Round220_split_interface_id": graph.interface_id,
            "endpoint_factor": graph.endpoint_factor,
            "sheet_member_id": graph.sheet.member_id,
            "sheet_source_package": graph.sheet.package,
            "sheet_source_filename": graph.sheet.filename,
            "sheet_source_file_sha256": PIN_BY_NAME[graph.sheet.filename]["source_sha256"],
            "sheet_source_table": graph.sheet.table,
            "sheet_source_row_sha256": graph.sheet.row_sha256,
            "B0_member_backbinding_row_id": backbinding_id(graph.sheet.member_id),
            "Round306B0_member_support_source_row_id": sheet_b0["Round306B0_member_support_source_row_id"],
            "join_basis": "SOURCE_ROW_ID_INTERFACE_AND_ENDPOINT_FACTOR",
            "official_key_id_metadata_only": graph.sheet.official_key_id,
            "official_key_used_as_join_or_routing_filter": False,
            "physical_incidence_proved": False,
            "formal_credit": zero_credit(),
        })
        spools["gap"].add({
            "schema": B1G0_ROW_SCHEMAS["gap"],
            B1G0_ID_FIELDS["gap"]: "round306b1g0-gap:incidence:" + digest(sheet_join_id),
            "gap_kind": "GRAPH_TO_SHEET_PHYSICAL_IDENTIFICATION_THEOREM_PENDING",
            "graph_source_inventory_row_id": inventory_id,
            "incidence_join_row_id": sheet_join_id,
            "member_id": graph.sheet.member_id,
            "required_closure": "prove the source graph equals the sealed sheet member without using key metadata as a filter",
            "formal_credit": zero_credit(),
        })
        incidence_family_counts[graph.family + ":SHEET"] += 1

        for side in graph.sides:
            join_id = "round306b1g0-graph-side:" + digest([graph.graph_id, side.member_id, side.role])
            side_b0 = b0[side.member_id]
            spools["side"].add({
                "schema": B1G0_ROW_SCHEMAS["side"],
                B1G0_ID_FIELDS["side"]: join_id,
                "graph_source_inventory_row_id": inventory_id,
                "graph_id": graph.graph_id,
                "graph_family": graph.family,
                "Round220_split_interface_id": graph.interface_id,
                "endpoint_factor": graph.endpoint_factor,
                "side_role": side.role,
                "side_branch_label": side.branch,
                "side_member_id": side.member_id,
                "side_source_package": side.package,
                "side_source_filename": side.filename,
                "side_source_file_sha256": PIN_BY_NAME[side.filename]["source_sha256"],
                "side_source_table": side.table,
                "side_source_row_sha256": side.row_sha256,
                "source_edge_id_metadata_only": side.source_edge_id,
                "source_edge_row_sha256_metadata_only": side.source_edge_sha256,
                "B0_member_backbinding_row_id": backbinding_id(side.member_id),
                "Round306B0_member_support_source_row_id": side_b0["Round306B0_member_support_source_row_id"],
                "join_basis": "SEALED_SOURCE_PARTITION_BRANCH_AND_R264_CORRECTION_DISPOSITION",
                "official_key_id_metadata_only": side.official_key_id,
                "official_key_used_as_join_or_routing_filter": False,
                "physical_incidence_proved": False,
                "formal_credit": zero_credit(),
            })
            spools["gap"].add({
                "schema": B1G0_ROW_SCHEMAS["gap"],
                B1G0_ID_FIELDS["gap"]: "round306b1g0-gap:incidence:" + digest(join_id),
                "gap_kind": "GRAPH_SIDE_POSITIVE_3D_PHYSICAL_INCIDENCE_THEOREM_PENDING",
                "graph_source_inventory_row_id": inventory_id,
                "incidence_join_row_id": join_id,
                "member_id": side.member_id,
                "required_closure": "derive a source-free one-sided embedding and verify physical incidence across the graph",
                "formal_credit": zero_credit(),
            })
            incidence_family_counts[graph.family + ":SIDE"] += 1

    expected_counts = {
        "graph": 38_624,
        "sheet": 38_624,
        "side": 76_848,
        "correction": 400,
        "member": 115_456,
        "gap": 154_096,
    }
    need(all(spools[kind].rows.count == count for kind, count in expected_counts.items()), "exact reconstructed ledger counts")
    audit = {
        "graph_family_histogram": dict(sorted(Counter(graph.family for graph in graphs).items())),
        "incidence_family_histogram": dict(sorted(incidence_family_counts.items())),
        "graph_count": spools["graph"].rows.count,
        "graph_sheet_join_count": spools["sheet"].rows.count,
        "graph_side_join_count": spools["side"].rows.count,
        "physical_incidence_count": spools["sheet"].rows.count + spools["side"].rows.count,
        "R264_correction_count": spools["correction"].rows.count,
        "distinct_B0_member_backbinding_count": spools["member"].rows.count,
        "gap_count": spools["gap"].rows.count,
        "official_key_used_as_join_or_routing_filter": False,
        "source_free_graph_definition_complete": False,
        "physical_incidence_theorem_complete": False,
        "all_output_formal_credit_zero": True,
    }
    return spools, audit


def verify_actual_b1g0_ledgers(
    context: ReplayContext,
    spools: dict[str, CommitmentSpool],
) -> dict[str, dict[str, Any]]:
    """Consume and compare every actual B1G0 row to independent reconstruction."""

    verified: dict[str, dict[str, Any]] = {}
    for kind in ("graph", "sheet", "side", "correction", "member", "gap"):
        label = B1G0_LEDGER_LABELS[kind]
        row_ids: set[str] = set()
        for row in context.rows(label):
            check_closed_row(row, "actual B1G0 " + kind)
            need(row.get("schema") == B1G0_ROW_SCHEMAS[kind], "actual B1G0 schema:" + kind)
            row_id = row[B1G0_ID_FIELDS[kind]]
            need(type(row_id) is str and row_id not in row_ids, "actual unique row ID:" + kind)
            row_ids.add(row_id)
            if "official_key_used_as_join_or_routing_filter" in row:
                need(row["official_key_used_as_join_or_routing_filter"] is False, "actual key metadata only:" + kind)
            assert_zero_credit(row, "actual B1G0:" + kind)
        expected = spools[kind].metadata()
        observed = context.tables[label]
        need(observed == expected, "actual ledger byte equality:" + kind)
        verified[kind] = dict(observed)
    return verified


def _stream(values: Iterator[Any] | list[Any] | tuple[Any, ...]) -> dict[str, Any]:
    tracker = ListHash()
    for value in values:
        tracker.add(value)
    return {"row_count": tracker.count, "rows_sha256": tracker.finish()}


def exact_join_audit(
    corrections: dict[str, dict[str, Any]],
    graphs: list[Graph],
    b0: dict[str, dict[str, Any]],
    references: dict[str, list[Feature]],
) -> tuple[dict[str, Any], dict[str, dict[str, Any]]]:
    """Close the G2 identity census, multiplicities, and all anti-joins."""

    graph_ids = {graph.graph_id for graph in graphs}
    sheet_features = [graph.sheet for graph in graphs]
    side_references = [side for graph in graphs for side in graph.sides]
    sheet_members = {item.member_id for item in sheet_features}
    side_members = {item.member_id for item in side_references}
    multiplicities = Counter(item.member_id for item in side_references)

    need(len(graph_ids) == EXPECTED_COUNTS["graph_roots"], "unique graph roots")
    need(len(sheet_features) == len(sheet_members) == EXPECTED_COUNTS["sheet_distinct_members"], "sheet identity anti-join")
    need(len(side_references) == EXPECTED_COUNTS["side_references"], "side reference census")
    need(len(side_members) == EXPECTED_COUNTS["side_distinct_members"], "side member anti-join")
    need(graph_ids.isdisjoint(sheet_members | side_members), "graph/member namespace anti-join")
    need(sheet_members.isdisjoint(side_members), "sheet/side member anti-join")
    need(set(b0) == sheet_members | side_members == set(references), "B0 exact G2 anti-join")
    need(Counter(multiplicities.values()) == {1: 76_816, 2: 16}, "global side multiplicity")

    r245_sheets = {item.member_id for item in sheet_features if item.package == "R245"}
    r248_sheets = {item.member_id for item in sheet_features if item.package == "R248"}
    r245_side_refs = [item for item in side_references if item.package == "R245"]
    r248_side_refs = [item for item in side_references if item.package == "R248"]
    r245_sides = {item.member_id for item in r245_side_refs}
    r248_sides = {item.member_id for item in r248_side_refs}
    need(len(r245_sheets) == 264 and len(r248_sheets) == 38_360 and r245_sheets.isdisjoint(r248_sheets), "R245/R248 sheet split")
    need(len(r245_side_refs) == len(r245_sides) == 528, "R245 side split")
    need(len(r248_side_refs) == 76_320 and len(r248_sides) == 76_304, "R248 side split")
    need(r245_sides.isdisjoint(r248_sides), "R245/R248 side anti-join")

    r236_side_refs = [
        side
        for graph in graphs
        if graph.family == "R236_DOUBLE_ENDPOINT_GRAPH"
        for side in graph.sides
    ]
    r236_multiplicity = Counter(item.member_id for item in r236_side_refs)
    need(len(r236_side_refs) == 64 and len(r236_multiplicity) == 48, "R236 64 to 48")
    need(Counter(r236_multiplicity.values()) == {1: 32, 2: 16}, "R236 multiplicity histogram")
    need(sum(1 for graph in graphs if graph.correction_source_id is not None) == 400, "R264 graph consumption")

    family_histogram = dict(sorted(Counter(graph.family for graph in graphs).items()))
    need(
        family_histogram
        == {
            "R235_SINGLE_ENDPOINT_GRAPH": 38_328,
            "R236_DOUBLE_ENDPOINT_GRAPH": 32,
            "R242_UNIQUE_TRANSITION_GRAPH": 264,
        },
        "graph family histogram",
    )
    natural_feature_count = len(graph_ids) + len(sheet_members) + len(side_members)
    need(natural_feature_count == EXPECTED_COUNTS["natural_G2_features"], "154080 natural G2 features")

    streams = {
        "graph_natural_stream": _stream(iter([
            graph.family,
            graph.graph_id,
            graph.source_row_id,
            graph.interface_id,
            graph.endpoint_factor,
        ] for graph in sorted(graphs, key=lambda item: item.graph_id))),
        "sheet_member_stream": _stream(iter(sorted(sheet_members))),
        "side_reference_stream": _stream(iter([
            graph.graph_id,
            side.role,
            side.member_id,
        ] for graph in sorted(graphs, key=lambda item: item.graph_id) for side in graph.sides)),
        "side_member_multiplicity_stream": _stream(iter([member, multiplicities[member]] for member in sorted(multiplicities))),
        "natural_G2_feature_stream": _stream(iter(
            [["GRAPH_ROOT", member] for member in sorted(graph_ids)]
            + [["SHEET_MEMBER", member] for member in sorted(sheet_members)]
            + [["SIDE_MEMBER", member] for member in sorted(side_members)]
        )),
        "R264_consumption_stream": _stream(iter([
            source,
            corrections[source]["endpoint_empty_branch_disposition_row_id"],
            corrections[source]["empty_branch_label"],
            corrections[source]["empty_wall_bulk_node_id"],
            corrections[source]["nonempty_wall_bulk_node_id"],
        ] for source in sorted(corrections))),
        "B0_G2_backbinding_stream": _stream(iter([
            member,
            b0[member]["Round306B0_member_support_source_row_id"],
            b0[member]["row_sha256"],
        ] for member in sorted(b0))),
    }

    audit = {
        "graph_family_histogram": family_histogram,
        "R245_R248_package_split": {
            "R245_sheet_members": len(r245_sheets),
            "R245_side_references": len(r245_side_refs),
            "R245_side_members": len(r245_sides),
            "R248_sheet_members": len(r248_sheets),
            "R248_side_references": len(r248_side_refs),
            "R248_side_members": len(r248_sides),
        },
        "identity_census": {
            "graph_roots": len(graph_ids),
            "sheet_references": len(sheet_features),
            "sheet_distinct_members": len(sheet_members),
            "side_references": len(side_references),
            "side_distinct_members": len(side_members),
            "B0_distinct_G2_members": len(b0),
            "natural_G2_features": natural_feature_count,
        },
        "side_reference_multiplicity_histogram": {str(key): value for key, value in sorted(Counter(multiplicities.values()).items())},
        "R236_side_reference_multiplicity_histogram": {str(key): value for key, value in sorted(Counter(r236_multiplicity.values()).items())},
        "anti_join_gaps": {
            "duplicate_graph_roots": 0,
            "duplicate_sheet_members": 0,
            "unbound_B0_G2_members": 0,
            "unbound_sheet_members": 0,
            "unbound_side_members": 0,
            "sheet_side_identity_overlap": 0,
            "R245_R248_sheet_overlap": 0,
            "R245_R248_side_overlap": 0,
            "unconsumed_R264_corrections": 0,
        },
        "official_keys_used_only_after_lineage_join": True,
        "official_keys_used_as_join_or_routing_filter": False,
    }
    return audit, streams


def _formal_blockers() -> dict[str, Any]:
    return {
        "source_free_graph_definition_theorems_pending": 38_624,
        "physical_incidence_theorems_pending": 115_472,
        "one_sided_closure_trace_obligations_pending": 76_848,
        "distinct_virtual_member_full_support_set_equalities_pending": 115_456,
        "R236_codimension_two_dispositions_pending": 16,
        "chart_map_and_representation_pullback_pending": 115_456,
        "normalized_full_support_constructed": False,
        "representation_cover_constructed": False,
        "transition_ready_handles_constructed": False,
        "all_are_formal_blockers": True,
        "none_is_discharged_by_identity_join_or_ledger_equality": True,
    }


def _formal_credit() -> dict[str, int]:
    return {
        "source_graph_definition": 0,
        "physical_incidence": 0,
        "normalized_support": 0,
        "representation_cover": 0,
        "transition": 0,
        "pair_routing": 0,
        "maximality": 0,
        "fibre": 0,
        "global_disposition": 0,
        "CM2": 0,
    }


def full_replay() -> dict[str, Any]:
    """Run the only filesystem-enabled mode and return its sealed audit."""

    with HeldInputs() as inputs:
        context = ReplayContext(inputs)
        interfaces, frontiers = load_coordinate_authorities(context)
        corrections = load_r264_corrections(context)
        graphs = load_r242_r245_graphs(context, interfaces)
        graphs.extend(load_r235_r236_r248_graphs(context, interfaces, frontiers, corrections))
        need(len(graphs) == 38_624 and len({graph.graph_id for graph in graphs}) == 38_624, "complete unique graph inventory")
        b0, references = bind_b0_members(context, graphs)
        join_audit, streams = exact_join_audit(corrections, graphs, b0, references)
        spools, spool_audit = build_expected_b1g0_spools(corrections, graphs, b0, references)
        actual_ledgers = verify_actual_b1g0_ledgers(context, spools)
        need(set(context.tables) == set(TABLE_BY_LABEL), "all selected tables consumed once")
        reconstructed_ledgers = {kind: spools[kind].metadata() for kind in sorted(spools)}
        need(actual_ledgers == reconstructed_ledgers, "all six reconstructed ledgers equal actual bytes")
        need(streams == EXPECTED_STREAM_COMMITMENTS or not EXPECTED_STREAM_COMMITMENTS, "frozen natural stream commitments")

        core = {
            "schema": SCHEMA + ".full-replay-result.v1",
            "status": STATUS,
            "read_only": True,
            "claim_class": "ZERO_CREDIT_PREFLIGHT_ONLY",
            "input_verification": inputs.verification_rows,
            "selected_table_commitments": {label: context.tables[label] for label in sorted(context.tables)},
            "reconstructed_B1G0_ledger_commitments": reconstructed_ledgers,
            "actual_B1G0_ledger_commitments": actual_ledgers,
            "spool_audit": spool_audit,
            "exact_join_audit": join_audit,
            "natural_stream_commitments": streams,
            "gap_consumption": {
                "actual_and_reconstructed_gap_rows": 154_096,
                "graph_definition_gaps": 38_624,
                "physical_incidence_gaps": 115_472,
                "unmatched_or_extra_gap_rows": 0,
            },
            "formal_blockers": _formal_blockers(),
            "formal_credit": _formal_credit(),
            "resource_claims": {
                "observed_RSS_reported": False,
                "memory_bound_claimed": False,
                "scratch_files_created": 0,
                "output_files_written": 0,
            },
            "downstream_state": {
                "AF4G1": "PASS_SEALED_ZERO_CREDIT_READ_ONLY_PREFLIGHT",
                "AF4_CONSTRUCTOR": "BLOCKED_ON_FORMAL_SUPPORT_AND_GEOMETRY",
                "B1A": "BLOCKED",
                "B2": "NOT_AUTHORIZED",
                "D02": "BLOCKED",
                "CM2": "NO-GO_FOR_CLAIM",
            },
        }
        assert_zero_credit(core, "full replay")
        replay_digest = digest(core)
        need(EXPECTED_REPLAY_DIGEST == "0" * 64 or replay_digest == EXPECTED_REPLAY_DIGEST, "frozen replay digest")
        return {**core, "replay_digest_sha256": replay_digest}


def _scope_contract() -> dict[str, Any]:
    return {
        "artifact_kind": "ZERO_CREDIT_READ_ONLY_FULL_REPLAY_PREFLIGHT",
        "independently_reconstructs_B1G0_ledgers": True,
        "exact_G2_identity_join_and_anti_join_only": True,
        "actual_input_files_opened_only_by_full_replay": True,
        "imports_or_executes_upstream_producer": False,
        "defines_normalized_full_support": False,
        "proves_source_graph_definition": False,
        "proves_physical_incidence": False,
        "proves_transition_or_pair_routing": False,
        "mints_maximality_fibre_global_or_CM2_credit": False,
    }


def _security_contract() -> dict[str, Any]:
    return {
        "one_held_directory_fd": True,
        "all_input_fds_open_before_first_hash": True,
        "open_flags_include_O_NOFOLLOW": True,
        "regular_file_and_nlink_one_required": True,
        "named_path_and_held_fd_fingerprint_match": True,
        "two_same_fd_full_SHA256_passes": True,
        "parse_from_dup_of_same_open_file_description": True,
        "parser_scope": "PIN_FIRST_EXACT_BYTE_SELECTED_TABLE_EXTRACTOR_NOT_GENERIC_OUTER_DOCUMENT_VALIDATOR",
        "strict_incremental_JSON_duplicate_keys_rejected": True,
        "floats_and_nonfinite_numbers_rejected": True,
        "gzip_CRC_and_UTF8_drained_to_EOF": True,
        "global_held_fd_path_and_directory_reaudit": True,
        "temporary_or_scratch_files_created": 0,
        "upstream_import_or_exec": False,
        "observed_RSS_reported": False,
        "memory_bound_claimed": False,
    }


def _candidate_contract() -> dict[str, Any]:
    return {
        "enabled": False,
        "candidate_and_production_entry_is_immediate_raise": True,
        "block_before_path_inspection": True,
        "block_before_input_open": True,
        "block_before_temp_creation": True,
        "block_before_output_write": True,
        "block_before_stdout_or_stderr": True,
        "block_reason": BLOCK_REASON,
    }


def _contract_document() -> dict[str, Any]:
    return {
        "schema": SCHEMA,
        "status": STATUS,
        "sealed": True,
        "candidate_is_formal": False,
        "scope": _scope_contract(),
        "direct_input_pins": [dict(row) for row in INPUT_PINS],
        "selected_table_commitments": [dict(row) for row in TABLE_SPECS],
        "exact_counts": dict(EXPECTED_COUNTS),
        "expected_natural_stream_commitments": copy.deepcopy(EXPECTED_STREAM_COMMITMENTS),
        "expected_full_replay_digest_sha256": EXPECTED_REPLAY_DIGEST,
        "replay_security": _security_contract(),
        "formal_blockers": _formal_blockers(),
        "candidate_and_production_modes": _candidate_contract(),
        "formal_credit": _formal_credit(),
        "downstream_state": {
            "AF4G1": "SEALED_ZERO_CREDIT_PREFLIGHT_ONLY",
            "AF4_CONSTRUCTOR": "BLOCKED_ON_FORMAL_SUPPORT_AND_GEOMETRY",
            "B1A": "BLOCKED",
            "B2": "NOT_AUTHORIZED",
            "D02": "BLOCKED",
            "D03": "NOT_REACHED",
            "D04": "NOT_MINTED",
            "CM2": "NO-GO_FOR_CLAIM",
        },
    }


def validate_contract(document: dict[str, Any]) -> None:
    need(document == _contract_document(), "exact sealed G1 contract")
    need(document["schema"] == SCHEMA and document["status"] == STATUS, "contract identity")
    need(document["sealed"] is True and document["candidate_is_formal"] is False, "sealed nonformal")
    need(len(document["direct_input_pins"]) == len(INPUT_PINS) == 20, "twenty direct pins")
    need(len(document["selected_table_commitments"]) == len(TABLE_SPECS) == 17, "seventeen table commitments")
    need(len({row["filename"] for row in document["direct_input_pins"]}) == 20, "unique pin filenames")
    for row in document["direct_input_pins"]:
        need(row["filename"] == os.path.basename(row["filename"]), "pin basename")
        need(type(row["exact_size"]) is int and row["exact_size"] > 0, "pin size")
        need(HEX64.fullmatch(row["source_sha256"]) is not None, "pin SHA")
    for row in document["selected_table_commitments"]:
        need(type(row["row_count"]) is int and row["row_count"] > 0, "table count")
        need(HEX64.fullmatch(row["rows_sha256"]) is not None, "table SHA")
    streams = document["expected_natural_stream_commitments"]
    need(set(streams) == {
        "B0_G2_backbinding_stream",
        "R264_consumption_stream",
        "graph_natural_stream",
        "natural_G2_feature_stream",
        "sheet_member_stream",
        "side_member_multiplicity_stream",
        "side_reference_stream",
    }, "seven frozen natural streams")
    for row in streams.values():
        need(set(row) == {"row_count", "rows_sha256"}, "stream commitment shape")
        need(type(row["row_count"]) is int and row["row_count"] > 0, "stream count")
        need(HEX64.fullmatch(row["rows_sha256"]) is not None, "stream SHA")
    need(HEX64.fullmatch(document["expected_full_replay_digest_sha256"]) is not None, "replay digest shape")
    need(document["expected_full_replay_digest_sha256"] != "0" * 64, "replay digest frozen")
    need(document["exact_counts"]["side_references"] == 76_848, "side reference count")
    need(document["exact_counts"]["side_distinct_members"] == 76_832, "side distinct count")
    need(document["exact_counts"]["natural_G2_features"] == 154_080, "natural feature count")
    need(document["formal_blockers"]["all_are_formal_blockers"] is True, "blockers retained")
    need(all(value == 0 for value in document["formal_credit"].values()), "all formal credit zero")
    need(document["candidate_and_production_modes"] == _candidate_contract(), "candidate exact block")
    need(document["downstream_state"]["B1A"] == "BLOCKED", "B1A blocked")
    need(document["downstream_state"]["B2"] == "NOT_AUTHORIZED", "B2 blocked")
    need(document["downstream_state"]["CM2"] == "NO-GO_FOR_CLAIM", "CM2 no-go")


def contract_envelope() -> dict[str, Any]:
    document = _contract_document()
    validate_contract(document)
    return {"contract": document, "canonical_contract_digest_sha256": digest(document)}


Mutation = tuple[str, Callable[[dict[str, Any]], None]]


def _set_path(document: dict[str, Any], path: tuple[Any, ...], value: Any) -> None:
    cursor: Any = document
    for key in path[:-1]:
        cursor = cursor[key]
    cursor[path[-1]] = value


def _delete_path(document: dict[str, Any], path: tuple[Any, ...]) -> None:
    cursor: Any = document
    for key in path[:-1]:
        cursor = cursor[key]
    del cursor[path[-1]]


def _semantic_mutations() -> list[Mutation]:
    def setter(path: tuple[Any, ...], value: Any) -> Callable[[dict[str, Any]], None]:
        return lambda document: _set_path(document, path, value)

    def deleter(path: tuple[Any, ...]) -> Callable[[dict[str, Any]], None]:
        return lambda document: _delete_path(document, path)

    return [
        ("schema", setter(("schema",), SCHEMA + ".mutated")),
        ("status", setter(("status",), "PASS_FORMAL")),
        ("sealed", setter(("sealed",), False)),
        ("candidate formal", setter(("candidate_is_formal",), True)),
        ("scope kind", setter(("scope", "artifact_kind"), "FORMAL_CONSTRUCTOR")),
        ("scope reconstruction", setter(("scope", "independently_reconstructs_B1G0_ledgers"), False)),
        ("scope support", setter(("scope", "defines_normalized_full_support"), True)),
        ("scope incidence", setter(("scope", "proves_physical_incidence"), True)),
        ("scope CM2", setter(("scope", "mints_maximality_fibre_global_or_CM2_credit"), True)),
        ("pin deletion", lambda document: document["direct_input_pins"].pop()),
        ("AF2 pin", setter(("direct_input_pins", 0, "source_sha256"), "0" * 64)),
        ("D1 pin", setter(("direct_input_pins", 4, "exact_size"), 84_391)),
        ("R220 pin", setter(("direct_input_pins", 5, "source_sha256"), "1" * 64)),
        ("R264 pin", setter(("direct_input_pins", 12, "exact_size"), 1)),
        ("B0 pin", setter(("direct_input_pins", 13, "compressed"), False)),
        ("B1 gap pin", setter(("direct_input_pins", 19, "source_sha256"), "2" * 64)),
        ("table deletion", lambda document: document["selected_table_commitments"].pop()),
        ("R220 table count", setter(("selected_table_commitments", 0, "row_count"), 13_075)),
        ("R234 table hash", setter(("selected_table_commitments", 1, "rows_sha256"), "3" * 64)),
        ("R236 table count", setter(("selected_table_commitments", 3, "row_count"), 15)),
        ("R264 table hash", setter(("selected_table_commitments", 9, "rows_sha256"), "4" * 64)),
        ("B0 table count", setter(("selected_table_commitments", 10, "row_count"), 564_491)),
        ("B1 side IDs", setter(("selected_table_commitments", 13, "row_ids_sha256"), "5" * 64)),
        ("B1 gap hashes", setter(("selected_table_commitments", 16, "row_hashes_sha256"), "6" * 64)),
        ("root count", setter(("exact_counts", "graph_roots"), 38_623)),
        ("side refs", setter(("exact_counts", "side_references"), 76_832)),
        ("side distinct", setter(("exact_counts", "side_distinct_members"), 76_848)),
        ("R245 split", setter(("exact_counts", "R245_side_members"), 527)),
        ("R248 split", setter(("exact_counts", "R248_side_members"), 76_305)),
        ("R236 multiplicity", setter(("exact_counts", "R236_side_members"), 49)),
        ("R264 split", setter(("exact_counts", "R264_empty_present"), 215)),
        ("gaps", setter(("exact_counts", "gaps"), 154_080)),
        ("natural features", setter(("exact_counts", "natural_G2_features"), 824_864)),
        ("stream deletion", deleter(("expected_natural_stream_commitments", "side_reference_stream"))),
        ("graph stream count", setter(("expected_natural_stream_commitments", "graph_natural_stream", "row_count"), 38_623)),
        ("sheet stream hash", setter(("expected_natural_stream_commitments", "sheet_member_stream", "rows_sha256"), "7" * 64)),
        ("multiplicity stream", setter(("expected_natural_stream_commitments", "side_member_multiplicity_stream", "rows_sha256"), "8" * 64)),
        ("feature stream count", setter(("expected_natural_stream_commitments", "natural_G2_feature_stream", "row_count"), 824_864)),
        ("replay digest", setter(("expected_full_replay_digest_sha256",), "9" * 64)),
        ("single dirfd", setter(("replay_security", "one_held_directory_fd"), False)),
        ("open order", setter(("replay_security", "all_input_fds_open_before_first_hash"), False)),
        ("nofollow", setter(("replay_security", "open_flags_include_O_NOFOLLOW"), False)),
        ("nlink", setter(("replay_security", "regular_file_and_nlink_one_required"), False)),
        ("one hash", setter(("replay_security", "two_same_fd_full_SHA256_passes"), False)),
        ("loose JSON", setter(("replay_security", "strict_incremental_JSON_duplicate_keys_rejected"), False)),
        ("scratch", setter(("replay_security", "temporary_or_scratch_files_created"), 1)),
        ("RSS claim", setter(("replay_security", "observed_RSS_reported"), True)),
        ("graph blocker", setter(("formal_blockers", "source_free_graph_definition_theorems_pending"), 0)),
        ("incidence blocker", setter(("formal_blockers", "physical_incidence_theorems_pending"), 0)),
        ("support blocker", setter(("formal_blockers", "normalized_full_support_constructed"), True)),
        ("blockers false", setter(("formal_blockers", "all_are_formal_blockers"), False)),
        ("candidate enabled", setter(("candidate_and_production_modes", "enabled"), True)),
        ("candidate path", setter(("candidate_and_production_modes", "block_before_path_inspection"), False)),
        ("candidate stdout", setter(("candidate_and_production_modes", "block_before_stdout_or_stderr"), False)),
        ("candidate reason", setter(("candidate_and_production_modes", "block_reason"), "changed")),
        ("formal credit", setter(("formal_credit", "normalized_support"), 1)),
        ("formal credit delete", deleter(("formal_credit", "CM2"))),
        ("B1A pass", setter(("downstream_state", "B1A"), "PASS")),
        ("B2 authorized", setter(("downstream_state", "B2"), "AUTHORIZED")),
        ("D02 pass", setter(("downstream_state", "D02"), "PASS")),
        ("CM2 go", setter(("downstream_state", "CM2"), "GO")),
    ]


def _blocked_candidate_entry(_output_path: str | None, _produce: bool) -> None:
    raise PreflightBlocked(BLOCK_REASON)


class _TripStream:
    def __init__(self, counter: dict[str, int], name: str) -> None:
        self.counter = counter
        self.name = name

    def write(self, _value: str) -> int:
        self.counter[self.name] += 1
        raise AssertionError("stream boundary crossed:" + self.name)

    def flush(self) -> None:
        return None


def _boundary_probe() -> dict[str, int]:
    counters = {
        "builtins_open": 0,
        "os_open": 0,
        "os_stat": 0,
        "os_lstat": 0,
        "path_exists": 0,
        "path_lstat": 0,
        "path_open": 0,
        "path_resolve": 0,
        "path_write_bytes": 0,
        "path_write_text": 0,
        "mkstemp": 0,
        "named_temp": 0,
        "temporary_directory": 0,
        "gzip_file": 0,
        "stdout": 0,
        "stderr": 0,
    }

    def trip(name: str) -> Callable[..., Any]:
        def inner(*_args: Any, **_kwargs: Any) -> Any:
            counters[name] += 1
            raise AssertionError("filesystem boundary crossed:" + name)
        return inner

    with (
        mock.patch("builtins.open", side_effect=trip("builtins_open")),
        mock.patch("os.open", side_effect=trip("os_open")),
        mock.patch("os.stat", side_effect=trip("os_stat")),
        mock.patch("os.lstat", side_effect=trip("os_lstat")),
        mock.patch.object(Path, "exists", side_effect=trip("path_exists")),
        mock.patch.object(Path, "lstat", side_effect=trip("path_lstat")),
        mock.patch.object(Path, "open", side_effect=trip("path_open")),
        mock.patch.object(Path, "resolve", side_effect=trip("path_resolve")),
        mock.patch.object(Path, "write_bytes", side_effect=trip("path_write_bytes")),
        mock.patch.object(Path, "write_text", side_effect=trip("path_write_text")),
        mock.patch("tempfile.mkstemp", side_effect=trip("mkstemp")),
        mock.patch("tempfile.NamedTemporaryFile", side_effect=trip("named_temp")),
        mock.patch("tempfile.TemporaryDirectory", side_effect=trip("temporary_directory")),
        mock.patch("gzip.GzipFile", side_effect=trip("gzip_file")),
        mock.patch.object(sys, "stdout", _TripStream(counters, "stdout")),
        mock.patch.object(sys, "stderr", _TripStream(counters, "stderr")),
    ):
        for produce in (False, True):
            try:
                _blocked_candidate_entry("/must/not/be/inspected", produce)
            except PreflightBlocked as exc:
                need(str(exc) == BLOCK_REASON, "candidate refusal reason")
            else:
                raise AssertionError("candidate entry accepted")
    need(all(value == 0 for value in counters.values()), "candidate pre-boundary refusal")
    return counters


def _strict_parser_self_test() -> None:
    need(list(iter_strict_json_rows(io.StringIO('{"a":1}]'))) == [{"a": 1}], "strict parser valid row")
    bad = (
        '{"a":1,"a":2}]',
        '{"a":1.5}]',
        '{"a":NaN}]',
        '{"a":1},]',
        ',{"a":1}]',
        '{"a":1}{"b":2}]',
        '{"a":1',
    )
    for source in bad:
        try:
            list(iter_strict_json_rows(io.StringIO(source)))
        except PreflightBlocked:
            pass
        else:
            raise AssertionError("strict parser accepted:" + source)


def self_test() -> dict[str, Any]:
    document = _contract_document()
    validate_contract(document)
    raw = canonical(document)
    need(canonical(json.loads(raw)) == raw, "canonical JSON round trip")
    need(digest(document) == hashlib.sha256(raw).hexdigest(), "contract digest stability")
    _strict_parser_self_test()

    rejected: list[str] = []
    for label, mutate in _semantic_mutations():
        candidate = copy.deepcopy(document)
        mutate(candidate)
        try:
            validate_contract(candidate)
        except PreflightBlocked:
            rejected.append(label)
        else:
            raise AssertionError("semantic mutation accepted:" + label)
    need(len(rejected) == len(_semantic_mutations()) >= 60, "all semantic mutations rejected")
    boundary = _boundary_probe()
    return {
        "schema": SCHEMA + ".self-test.v1",
        "status": "PASS",
        "canonical_contract_digest_sha256": digest(document),
        "semantic_mutation_count": len(rejected),
        "semantic_mutations_rejected": len(rejected),
        "strict_incremental_JSON_tests": 8,
        "candidate_and_production_refusals": 2,
        "boundary_call_counts": boundary,
        "formal_credit": 0,
    }


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    modes = parser.add_mutually_exclusive_group(required=True)
    modes.add_argument("--print-contract", action="store_true")
    modes.add_argument("--self-test", action="store_true")
    modes.add_argument("--full-replay", action="store_true")
    modes.add_argument("--candidate-output", metavar="PATH")
    modes.add_argument("--produce", action="store_true")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    if args.candidate_output is not None or args.produce:
        try:
            _blocked_candidate_entry(args.candidate_output, args.produce)
        except PreflightBlocked:
            return 1
        raise AssertionError("unreachable candidate mode")
    if args.print_contract:
        print(canonical(contract_envelope()).decode("ascii"))
        return 0
    if args.self_test:
        print(canonical(self_test()).decode("ascii"))
        return 0
    if args.full_replay:
        print(canonical(full_replay()).decode("ascii"))
        return 0
    raise AssertionError("unreachable CLI mode")


if __name__ == "__main__":
    raise SystemExit(main())
