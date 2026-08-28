#!/usr/bin/env python3
"""Independent verifier/publisher scaffold for the Round306B0 source freeze.

The verifier never imports, executes, parses, or tokenizes the Round306B0
producer or the Round306A producer.  The former is inert SHA-pinned bytes; the
latter is sealed only through the final Round306A manifest.  Candidate
admission remains unavailable until the one missing upstream manifest digest
and the consequent local producer digest are frozen.

Round306B0 has intentionally narrow credit: it can freeze the current universe
and pair denominator, but always publishes zero maximality/fibre/global credit.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import ctypes
import errno
import fcntl
import gzip
import hashlib
import io
import itertools
import json
import os
from pathlib import Path
import re
import stat
import tempfile
from typing import Any, BinaryIO, Callable, Iterator, TextIO


def discover_root(source: Path) -> Path:
    for ancestor in (source.resolve().parent, *source.resolve().parents):
        if (ancestor / "deliverables").is_dir() and (ancestor / ".venv-cm2").is_dir():
            return ancestor
    raise RuntimeError("workspace root not found")


ROOT = discover_root(Path(__file__))
DATA = ROOT / "deliverables"
PRIVATE_ROOT = ROOT / ".cm2-round306b0-private-candidates"
PREFIX = "cm2_round306b0_source_g_r306a_universe_support_source_freeze"
SCHEMA = "cm2.round306b0.source-g-r306a-universe-support-source-freeze.v2"
PRODUCER = PREFIX + ".py"
VERIFIER = PREFIX + "_promotion_verifier.py"
ATTACK = PREFIX + "_attack_suite.json"
VERIFICATION = PREFIX + "_verification.json"
PIN = re.compile(r"^[0-9a-f]{64}$")
ENCODER = json.JSONEncoder(
    ensure_ascii=True, allow_nan=False, sort_keys=True, separators=(",", ":")
)

# One missing upstream datum, duplicated deliberately so producer and verifier
# do not share executable code.  EXPECTED_PRODUCER_SHA256 is a local
# cachebuster set only after that single upstream pin is inserted.
R306A_MANIFEST_SHA256 = "35da99af5bb4c424284af2d7b396fc94b82dd6c6aa468c6a43a139107f9d9efc"
EXPECTED_PRODUCER_SHA256 = "48f38e2b90aa2c1b934ba657f8c6e66a8cb97fa89f9439a0b11ed5fbb3d20d83"

R306A_PREFIX = "cm2_round306a_source_g_r305b_fresh_legal_component_dsu_rebuild"
R306A_MANIFEST = R306A_PREFIX + "_manifest.sha256"
R306A_MEMBER = R306A_PREFIX + "_member_component_ledger.json.gz"
R306A_RESULT = R306A_PREFIX + "_result.json"
R306A_VERIFICATION = R306A_PREFIX + "_verification.json"
R306A_PARTITION_SHA256 = "a3f7ce1e28a956a46803ef466709ded0053633f5e104746c6d1e6e51b873e19c"
R306A_MEMBER_SHA256 = "710ebb660a7e7fad6a691c03bf845cf0081037ed09cc49a885c94c4bc472c276"
R306A_RESULT_SHA256 = "febe77da4285791b54e098c80a4b868c1e5dc6e43e98a7553bfff5e065075010"
R306A_RESULT_SELF_SHA256 = "6ee906cddae42e6df086cec26c7e0898ebe198519ce96605fd609a20c4f1e46a"
R306A_EXPECTED_MANIFEST_MEMBERS = frozenset({
    R306A_PREFIX + ".py",
    R306A_PREFIX + "_edge_application_ledger.json.gz",
    R306A_MEMBER,
    R306A_PREFIX + "_r305b_promoted_edge_application_ledger.json.gz",
    R306A_PREFIX + "_r300a_reprojection_ledger.json.gz",
    R306A_PREFIX + "_wtail_disposition_ledger.json.gz",
    R306A_PREFIX + "_residual_gate_ledger.json.gz",
    R306A_RESULT,
    R306A_PREFIX + "_promotion_verifier.py",
    R306A_PREFIX + "_attack_suite.json",
    R306A_VERIFICATION,
    R306A_PREFIX + "_report.md",
    R306A_PREFIX + "_cold_replay.md",
})
R306A_KNOWN_MEMBER_PINS = {
    R306A_PREFIX + ".py": "ab798332c82f7aa3656c61e3b31698a30b0fa1a83d24900432e076e445d6f5d5",
    R306A_PREFIX + "_edge_application_ledger.json.gz": "6da4620a100c980f921350f162fda064580e603f8ff7221eeed768b8bd091d1f",
    R306A_MEMBER: R306A_MEMBER_SHA256,
    R306A_PREFIX + "_r305b_promoted_edge_application_ledger.json.gz": "08f9ff2f5df0210cedd8cb3f8d998846e3722bd6bb0a2216d8d6c24a95a64a41",
    R306A_PREFIX + "_r300a_reprojection_ledger.json.gz": "c3e62f9833c333fb89758edd5c3f1648364a70b91bd1ed85650241a4cd10b673",
    R306A_PREFIX + "_wtail_disposition_ledger.json.gz": "6bdcc231b3cfd67f18ff3c62c27af08fdc9eb562a2c4e24a601798c0ad6d2556",
    R306A_PREFIX + "_residual_gate_ledger.json.gz": "1e79d529f3ca1fcefa170263a5d8b88929361ea27c0eeb3c6de108b870f9d8b8",
    R306A_RESULT: R306A_RESULT_SHA256,
    R306A_PREFIX + "_promotion_verifier.py": "60cc0f9cec6c8f4121f7ed7fde45b11e1b72bd9adc897364d9c0937c92a54c72",
}

FILES = {
    "member": PREFIX + "_member_support_source_index.json.gz",
    "component": PREFIX + "_component_census.json.gz",
    "pair": PREFIX + "_pair_denominator.json.gz",
    "source": PREFIX + "_source_table_inventory.json.gz",
    "gap": PREFIX + "_coverage_gap.json.gz",
    "result": PREFIX + "_result.json",
}
TABLES = {
    "member": "member_support_source_rows",
    "component": "component_census_rows",
    "pair": "pair_denominator_rows",
    "source": "source_table_inventory_rows",
    "gap": "coverage_gap_rows",
}
ID_FIELDS = {
    "member": "Round306B0_member_support_source_row_id",
    "component": "Round306B0_component_census_row_id",
    "pair": "Round306B0_pair_denominator_row_id",
    "source": "Round306B0_source_table_inventory_row_id",
    "gap": "Round306B0_coverage_gap_row_id",
}
CANDIDATE_ORDER = (
    FILES["member"], FILES["component"], FILES["pair"],
    FILES["source"], FILES["gap"], FILES["result"],
)
PROMOTION_ORDER = (
    ATTACK, FILES["member"], FILES["component"], FILES["pair"],
    FILES["source"], FILES["gap"], FILES["result"], VERIFICATION,
)

EXPECTED = {
    "member_count": 564492,
    "occurrence_count": 431208,
    "virtual_count": 133284,
    "virtual_positive_3d_count": 94660,
    "virtual_sheet_count": 38624,
    "R248_sheet_count": 38360,
    "R245_sheet_count": 264,
    "component_count": 92688,
    "official_key_count": 124,
    "all_pair_count": 159325326786,
    "within_component_pair_count": 487242432,
    "cross_component_pair_count": 158838084354,
    "minimum_component_size": 1,
    "maximum_component_size": 10599,
}
PAIR_CLASS_COUNTS = {
    "OCCURRENCE__OCCURRENCE": 92969954028,
    "OCCURRENCE__VIRTUAL_POSITIVE_3D": 40818149280,
    "OCCURRENCE__VIRTUAL_SHEET": 16654977792,
    "VIRTUAL_POSITIVE_3D__VIRTUAL_POSITIVE_3D": 4480210470,
    "VIRTUAL_POSITIVE_3D__VIRTUAL_SHEET": 3656147840,
    "VIRTUAL_SHEET__VIRTUAL_SHEET": 745887376,
}
R306A_MEMBER_COMMITMENT = {
    "row_count": 564492,
    "row_ids_sha256": "befaf5ae8a8ae109912649201e5efd90a03898edc02b5518cadec93e1f835165",
    "row_hashes_sha256": "003ecfe414434477a404c7b1912bfd117e98fc4883faee36119144b877f923ad",
    "rows_sha256": "43bc3ca15f58b6dd089b776c6c21f68fb246eb6af0590974129e20beef93eabd",
}

SOURCE_PACKAGES = {
    "R245": (
        "cm2_round245_source_g_retained_graph_mixed_sheet_quotient_manifest.sha256",
        "1aff29f3a42b618ca85e5a1d3c537307e32326f8d5092b82d4253a5bf6e1c4ac",
        ("cm2_round245_source_g_retained_graph_mixed_sheet_quotient_certificate.json",),
    ),
    "R246": (
        "cm2_round246_source_g_whole_signature_retained_quotient_manifest.sha256",
        "1d25aed877e9cff20fd6c705e8393ffe96a113532b0453a34e8adcec474080ef",
        ("cm2_round246_source_g_whole_signature_retained_quotient_certificate.json",),
    ),
    "R247": (
        "cm2_round247_source_g_crossing_and_source_seam_retained_quotient_manifest.sha256",
        "3399a32de8fc1191eb8214d48da064a1412f0c1dab5f9e044d30d7940a6993f2",
        ("cm2_round247_source_g_crossing_and_source_seam_retained_quotient_certificate.json",),
    ),
    "R248": (
        "cm2_round248_source_g_wall_finite_key_retained_quotient_manifest.sha256",
        "b1ddedd01041e71b5c12fa4989726815c8685e6df77f54d9dbddda64aaf89e07",
        ("cm2_round248_source_g_wall_finite_key_retained_quotient_certificate.json",),
    ),
    "R266": (
        "cm2_round266_source_g_expanded_curved_face_closure_manifest.sha256",
        "63fb5b25d52ca5de579256499629d04d15f6a313e0a73f7e80fcb463385cbe09",
        ("cm2_round266_source_g_expanded_curved_face_closure_certificate.json",),
    ),
    "R275": (
        "cm2_round275_source_g_complete_reverse_rechart_materialization_manifest.sha256",
        "a5dbf43a144a0a752f467911ee59e6afd6d2d60d27e0bc80bc45b7afa9334669",
        ("cm2_round275_source_g_complete_reverse_rechart_materialization_certificate.json",),
    ),
    "R287": (
        "cm2_round287_source_g_rechart_terminal_occurrence_disposition_probe_manifest.sha256",
        "85a9d4fcf9d9931a0e352eeef7582347b12325b92ffc78f2ee40c77c58093751",
        ("cm2_round287_source_g_rechart_terminal_occurrence_disposition_probe_ledger.json.gz",),
    ),
    "R291": (
        "cm2_round291_source_g_complete_lower_stratum_local_disposition_freeze_manifest.sha256",
        "d655907a45cfb7b47ebdc822d35a0e604fc27fa38547c300139c116d7a2191ce",
        ("cm2_round291_source_g_complete_lower_stratum_local_disposition_freeze_ledger.json.gz",),
    ),
    "R294": (
        "cm2_round294_source_g_occurrence_registry_atomic_promotion_manifest.sha256",
        "90d5cda0271610bf95a72f94e9bae8e192425580019dd3c823b5a69d20e52131",
        (
            "cm2_round294_source_g_occurrence_registry_atomic_promotion_registry_ledger.json.gz",
            "cm2_round294_source_g_occurrence_registry_atomic_promotion_representation_binding_ledger.json.gz",
        ),
    ),
    "R294B": (
        "cm2_round294b_source_g_registry_builder_admission_closure_manifest.sha256",
        "fc16aa2792a59dff922afcc8ec66b1ca015251af3c5f718d9d909439a2990d76",
        (
            "cm2_round294_source_g_occurrence_registry_atomic_promotion_manifest.sha256",
            "cm2_round294b_source_g_registry_builder_admission_closure_verification.json",
        ),
    ),
    "R295C": (
        "cm2_round295c_source_g_all_stratum_scope_composition_closure_manifest.sha256",
        "a9499856148480b9ddd5b0dd9ea8de28b989b592477c9a3b7ea43541772180c1",
        ("cm2_round295c_source_g_all_stratum_scope_composition_closure_ledger.json.gz",),
    ),
    "R299A": (
        "cm2_round299a_source_g_refined_occurrence_official_key_binding_closure_manifest.sha256",
        "b1dfe718dd2b7477d9cc4067f1bade59d1589b3822eaf4b94b9dd721e61b468e",
        ("cm2_round299a_source_g_refined_occurrence_official_key_binding_closure_ledger.json.gz",),
    ),
}
R294_REGISTRY = SOURCE_PACKAGES["R294"][2][0]
R266_CERTIFICATE = SOURCE_PACKAGES["R266"][2][0]
R294_COMMITMENT = {
    "row_count": 431208,
    "row_ids_sha256": "bbaca3ecbb804a87fd509aac2b8bd9f505d0c008e7bddbeb1a2ecb2a966f5509",
    "row_hashes_sha256": "ea98de3dab7e6f308f5a07d04bc29ca0d9dcd265a5323d8ecdb728cc501eed56",
    "rows_sha256": "33936ecd04cbce9f9a308b0da10381bd854b45028db53db5d3cbb9aa8b264044",
}
R266_MEMBER_COMMITMENT = {
    "row_count": 259752,
    "row_ids_sha256": "f064d177c25985b38c899c651923b83ba47ee36b465902cca85a4c21e0c33ca6",
    "row_hashes_sha256": "1f28c84d14cf3fabb38d0f2d1fdf862ce8f6a4559552d68fd9c0a5bd0a3ed3ee",
    "rows_sha256": "28398acde446047ff4a210b2fa0831d2c44e3758f7e9239b5ec63cecc386b257",
}


class VerificationBlocked(RuntimeError):
    pass


def need(value: bool, label: str) -> None:
    if not value:
        raise VerificationBlocked(label)


def canonical(value: Any) -> bytes:
    return ENCODER.encode(value).encode("ascii")


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def check_self(value: dict[str, Any], field: str, label: str) -> None:
    payload = dict(value)
    claimed = payload.pop(field, None)
    need(type(claimed) is str and claimed == digest(payload), "self hash:" + label)


def close_row(payload: dict[str, Any]) -> dict[str, Any]:
    return {**payload, "row_sha256": digest(payload)}


def strict_object(raw: bytes, label: str) -> dict[str, Any]:
    need(raw and not raw.startswith(b"\xef\xbb\xbf") and b"\x00" not in raw,
         "strict bytes:" + label)

    def unique(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        out: dict[str, Any] = {}
        for key, value in pairs:
            need(key not in out, "duplicate key:" + label + ":" + key)
            out[key] = value
        return out

    def reject(token: str) -> Any:
        raise VerificationBlocked("nonintegral JSON:" + label + ":" + token)

    value = json.loads(
        raw.decode("utf-8"), object_pairs_hook=unique,
        parse_float=reject, parse_constant=reject,
    )
    need(type(value) is dict, "top object:" + label)
    return value


def exact_regular(path: Path, parent: Path, maximum: int) -> os.stat_result:
    need(path.parent == parent and path.name == os.path.basename(path), "direct file path")
    need(os.path.lexists(path) and not path.is_symlink(), "exists/no symlink:" + path.name)
    info = os.lstat(path)
    need(
        stat.S_ISREG(info.st_mode) and info.st_nlink == 1
        and 0 < info.st_size <= maximum,
        "regular single-link bounded:" + path.name,
    )
    return info


def stable_bytes(path: Path, parent: Path, maximum: int = 3_000_000_000) -> bytes:
    before = exact_regular(path, parent, maximum)
    descriptor = os.open(path, os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0))
    try:
        opened = os.fstat(descriptor)
        named = os.lstat(path)
        before_id = (
            before.st_dev, before.st_ino, before.st_mode, before.st_nlink,
            before.st_size, before.st_mtime_ns, before.st_ctime_ns,
        )
        opened_id = (
            opened.st_dev, opened.st_ino, opened.st_mode, opened.st_nlink,
            opened.st_size, opened.st_mtime_ns, opened.st_ctime_ns,
        )
        named_id = (
            named.st_dev, named.st_ino, named.st_mode, named.st_nlink,
            named.st_size, named.st_mtime_ns, named.st_ctime_ns,
        )
        need(before_id == opened_id == named_id, "fd/path binding:" + path.name)
        chunks: list[bytes] = []
        total = 0
        while True:
            block = os.read(descriptor, 1 << 20)
            if not block:
                break
            total += len(block)
            need(total <= maximum, "bounded read:" + path.name)
            chunks.append(block)
        need(opened_id == (
            os.fstat(descriptor).st_dev, os.fstat(descriptor).st_ino,
            os.fstat(descriptor).st_mode, os.fstat(descriptor).st_nlink,
            os.fstat(descriptor).st_size, os.fstat(descriptor).st_mtime_ns,
            os.fstat(descriptor).st_ctime_ns,
        ), "stable fd:" + path.name)
        return b"".join(chunks)
    finally:
        os.close(descriptor)


def sha256_path_snapshot(
    path: Path, parent: Path, maximum: int = 3_000_000_000,
) -> tuple[str, tuple[int, int, int, int, int, int, int]]:
    before = exact_regular(path, parent, maximum)
    descriptor = os.open(path, os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0))
    state = hashlib.sha256()
    try:
        opened = os.fstat(descriptor)
        named = os.lstat(path)
        expected_identity = stat_identity(before)
        need(
            expected_identity == stat_identity(opened) == stat_identity(named),
            "hash fd/path binding:" + path.name,
        )
        total = 0
        while True:
            block = os.read(descriptor, 1 << 20)
            if not block:
                break
            total += len(block)
            need(total <= maximum, "bounded hash:" + path.name)
            state.update(block)
        need(
            stat_identity(os.fstat(descriptor)) == expected_identity
            and stat_identity(os.lstat(path)) == expected_identity,
            "hash fd/path stable:" + path.name,
        )
        return state.hexdigest(), expected_identity
    finally:
        os.close(descriptor)


def sha256_path(path: Path, parent: Path, maximum: int = 3_000_000_000) -> str:
    return sha256_path_snapshot(path, parent, maximum)[0]


def parse_manifest(name: str, expected_sha256: str) -> dict[str, str]:
    need(PIN.fullmatch(expected_sha256) is not None, "manifest pin syntax")
    raw = stable_bytes(DATA / name, DATA, 1_000_000)
    need(hashlib.sha256(raw).hexdigest() == expected_sha256, "manifest pin:" + name)
    output: dict[str, str] = {}
    for line in raw.decode("ascii").splitlines():
        match = re.fullmatch(r"([0-9a-f]{64})  (?:deliverables/)?([^/\s]+)", line)
        need(match is not None, "manifest line:" + name)
        value, member = match.groups()
        need(member not in output, "manifest duplicate:" + member)
        output[member] = value
    return output


def runtime_verifier_sha256() -> str:
    expected = DATA / VERIFIER
    actual = Path(__file__).resolve()
    need(actual == expected.resolve() and Path(__file__).absolute() == expected.absolute(),
         "runtime verifier exact path")
    return sha256_path(expected, DATA, 3_000_000)


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


def iter_array(stream: TextIO, marker: str, initial: str = "") -> Iterator[dict[str, Any]]:
    buffer = initial
    while marker not in buffer:
        block = stream.read(1 << 20)
        need(bool(block), "missing array:" + marker)
        buffer += block
    buffer = buffer.split(marker, 1)[1]

    def unique(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        out: dict[str, Any] = {}
        for key, value in pairs:
            need(key not in out, "stream duplicate key:" + key)
            out[key] = value
        return out

    decoder = json.JSONDecoder(
        object_pairs_hook=unique,
        parse_float=lambda token: (_ for _ in ()).throw(VerificationBlocked("float:" + token)),
        parse_constant=lambda token: (_ for _ in ()).throw(VerificationBlocked("constant:" + token)),
    )
    while True:
        buffer = buffer.lstrip()
        if not buffer:
            block = stream.read(1 << 20)
            need(bool(block), "truncated array")
            buffer = block
            continue
        if buffer[0] == ",":
            buffer = buffer[1:]
            continue
        if buffer[0] == "]":
            return
        while True:
            try:
                value, end = decoder.raw_decode(buffer)
                break
            except json.JSONDecodeError:
                block = stream.read(1 << 20)
                need(bool(block), "truncated row")
                buffer += block
        need(type(value) is dict, "row object")
        yield value
        buffer = buffer[end:]


def iter_final_array(stream: TextIO, marker: str) -> Iterator[dict[str, Any]]:
    buffer = ""
    while marker not in buffer:
        block = stream.read(1 << 20)
        need(bool(block), "missing final array:" + marker)
        buffer += block
    buffer = buffer.split(marker, 1)[1]

    def unique(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        out: dict[str, Any] = {}
        for key, value in pairs:
            need(key not in out, "candidate row duplicate key:" + key)
            out[key] = value
        return out

    decoder = json.JSONDecoder(
        object_pairs_hook=unique,
        parse_float=lambda token: (_ for _ in ()).throw(VerificationBlocked("float:" + token)),
        parse_constant=lambda token: (_ for _ in ()).throw(VerificationBlocked("constant:" + token)),
    )
    first = True
    while True:
        while not buffer.strip():
            block = stream.read(1 << 20)
            need(bool(block), "truncated final array")
            buffer += block
        buffer = buffer.lstrip()
        if not first:
            if buffer[0] == "]":
                suffix = buffer[1:] + stream.read()
                need(suffix.strip() == "}", "candidate ledger exact final suffix")
                return
            need(buffer[0] == ",", "candidate ledger missing row delimiter")
            buffer = buffer[1:]
            while not buffer.strip():
                block = stream.read(1 << 20)
                need(bool(block), "truncated candidate row after delimiter")
                buffer += block
            buffer = buffer.lstrip()
            need(buffer[0] not in {",", "]"},
                 "candidate ledger duplicate/trailing delimiter")
        elif buffer[0] == "]":
            suffix = buffer[1:] + stream.read()
            need(suffix.strip() == "}", "candidate ledger exact empty final suffix")
            return
        while True:
            try:
                value, end = decoder.raw_decode(buffer)
                break
            except json.JSONDecodeError:
                block = stream.read(1 << 20)
                need(bool(block), "truncated candidate row")
                buffer += block
        need(type(value) is dict, "candidate row object")
        yield value
        buffer = buffer[end:]
        first = False


def gzip_row_iterator(
    path: Path, parent: Path, table: str,
    expected_snapshot: tuple[int, int, int, int, int, int, int] | None = None,
) -> Iterator[dict[str, Any]]:
    named_before = exact_regular(path, parent, 3_000_000_000)
    descriptor = os.open(path, os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0))
    opened_before = os.fstat(descriptor)
    bound = stat_identity(opened_before)
    need(bound == stat_identity(named_before), "gzip source fd/path binding:" + path.name)
    if expected_snapshot is not None:
        need(bound == expected_snapshot, "gzip source manifest snapshot:" + path.name)
    raw = os.fdopen(descriptor, "rb", closefd=True)
    binary = gzip.GzipFile(fileobj=raw, mode="rb")
    stream = io.TextIOWrapper(binary, encoding="utf-8", newline="")
    try:
        yield from iter_array(stream, '"' + table + '":[')
        need(
            stat_identity(os.fstat(raw.fileno())) == bound
            and stat_identity(os.lstat(path)) == bound,
            "gzip source fd/path stable:" + path.name,
        )
    finally:
        try:
            stream.detach()
        except Exception:
            pass
        try:
            binary.close()
        finally:
            raw.close()


def gzip_row_iterator_at(
    directory_fd: int, name: str, table: str,
) -> Iterator[dict[str, Any]]:
    descriptor = os.open(
        name, os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0), dir_fd=directory_fd
    )
    before = os.fstat(descriptor)
    need(
        stat.S_ISREG(before.st_mode) and before.st_nlink == 1
        and stat.S_IMODE(before.st_mode) == 0o600,
        "candidate gzip regular/mode:" + name,
    )
    raw = os.fdopen(descriptor, "rb", closefd=True)
    binary = gzip.GzipFile(fileobj=raw, mode="rb")
    stream = io.TextIOWrapper(binary, encoding="utf-8", newline="")
    try:
        yield from iter_final_array(stream, '"' + table + '":[')
        need(stat_identity(before) == stat_identity(os.fstat(raw.fileno())),
             "candidate gzip fd stable:" + name)
    finally:
        try:
            stream.detach()
        except Exception:
            pass
        try:
            binary.close()
        finally:
            raw.close()


def stable_bytes_at(directory_fd: int, name: str, maximum: int) -> bytes:
    descriptor = os.open(
        name, os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0), dir_fd=directory_fd
    )
    try:
        before = os.fstat(descriptor)
        need(
            stat.S_ISREG(before.st_mode) and before.st_nlink == 1
            and stat.S_IMODE(before.st_mode) == 0o600
            and 0 < before.st_size <= maximum,
            "candidate regular/mode/bound:" + name,
        )
        chunks: list[bytes] = []
        total = 0
        while True:
            block = os.read(descriptor, 1 << 20)
            if not block:
                break
            total += len(block)
            need(total <= maximum, "candidate bounded read:" + name)
            chunks.append(block)
        need(stat_identity(before) == stat_identity(os.fstat(descriptor)),
             "candidate file stable:" + name)
        return b"".join(chunks)
    finally:
        os.close(descriptor)


def candidate_ledger_header_at(
    directory_fd: int, name: str, table: str,
) -> dict[str, Any]:
    descriptor = os.open(
        name, os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0), dir_fd=directory_fd
    )
    before = os.fstat(descriptor)
    need(
        stat.S_ISREG(before.st_mode) and before.st_nlink == 1
        and stat.S_IMODE(before.st_mode) == 0o600,
        "candidate ledger header regular/mode:" + name,
    )
    raw = os.fdopen(descriptor, "rb", closefd=True)
    binary = gzip.GzipFile(fileobj=raw, mode="rb")
    stream = io.TextIOWrapper(binary, encoding="utf-8", newline="")
    marker = ',"' + table + '":['
    buffer = ""
    try:
        while marker not in buffer:
            need(len(buffer) <= 1_000_000, "candidate ledger bounded header:" + name)
            block = stream.read(65536)
            need(bool(block), "candidate ledger missing table marker:" + name)
            buffer += block
        prefix, _tail = buffer.split(marker, 1)
        header = strict_object((prefix + "}").encode("utf-8"), name + ":header")
        need(stat_identity(before) == stat_identity(os.fstat(raw.fileno())),
             "candidate ledger header fd stable:" + name)
        return header
    finally:
        try:
            stream.detach()
        except Exception:
            pass
        try:
            binary.close()
        finally:
            raw.close()


def scan_rows(
    iterator: Iterator[dict[str, Any]], id_field: str,
    visit: Callable[[dict[str, Any]], None] | None = None,
) -> dict[str, Any]:
    rows, ids, hashes = ListHash(), ListHash(), ListHash()
    seen: set[str] = set()
    for row in iterator:
        check_self(row, "row_sha256", "stream row")
        row_id = row.get(id_field)
        need(type(row_id) is str and row_id not in seen, "unique row id")
        seen.add(row_id)
        rows.add(row)
        ids.add(row_id)
        hashes.add(row["row_sha256"])
        if visit is not None:
            visit(row)
    return {
        "row_count": rows.count,
        "row_ids_sha256": ids.finish(),
        "row_hashes_sha256": hashes.finish(),
        "rows_sha256": rows.finish(),
    }


def plain_row_iterator(
    path: Path, table: str,
    expected_snapshot: tuple[int, int, int, int, int, int, int] | None = None,
) -> Iterator[dict[str, Any]]:
    named_before = exact_regular(path, DATA, 3_000_000_000)
    descriptor = os.open(path, os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0))
    opened_before = os.fstat(descriptor)
    bound = stat_identity(opened_before)
    need(bound == stat_identity(named_before), "plain source fd/path binding:" + path.name)
    if expected_snapshot is not None:
        need(bound == expected_snapshot, "plain source manifest snapshot:" + path.name)
    raw = os.fdopen(descriptor, "rb", closefd=True)
    stream = io.TextIOWrapper(raw, encoding="utf-8", newline="")
    outer = '"' + table + '":'
    carry = ""
    try:
        while True:
            block = stream.read(1 << 20)
            need(bool(block), "missing plain table:" + table)
            combined = carry + block
            if outer in combined:
                initial = combined.split(outer, 1)[1]
                break
            carry = combined[-len(outer):]
        yield from iter_array(stream, '"rows":[', initial)
        need(
            stat_identity(os.fstat(raw.fileno())) == bound
            and stat_identity(os.lstat(path)) == bound,
            "plain source fd/path stable:" + path.name,
        )
    finally:
        try:
            stream.detach()
        except Exception:
            pass
        raw.close()


def bind_source_manifests() -> tuple[
    dict[tuple[str, str], tuple[str, str]],
    dict[str, tuple[int, int, int, int, int, int, int]],
]:
    selected: dict[tuple[str, str], tuple[str, str]] = {}
    snapshots: dict[str, tuple[int, int, int, int, int, int, int]] = {}
    for label, (manifest, manifest_sha, members) in SOURCE_PACKAGES.items():
        entries = parse_manifest(manifest, manifest_sha)
        for member in members:
            need(member in entries, "selected source member:" + label + ":" + member)
            member_sha256, snapshot = sha256_path_snapshot(DATA / member, DATA)
            need(member_sha256 == entries[member],
                 "selected source member pin:" + label + ":" + member)
            if member in snapshots:
                need(snapshots[member] == snapshot, "reused selected source snapshot:" + member)
            snapshots[member] = snapshot
            selected[(label, member)] = (manifest_sha, entries[member])
    return selected, snapshots


def bind_round306a() -> tuple[
    dict[str, str],
    dict[str, tuple[int, int, int, int, int, int, int]],
]:
    need(PIN.fullmatch(R306A_MANIFEST_SHA256) is not None,
         "BLOCKED_SINGLE_PIN:Round306A formal manifest SHA is not finalized")
    entries = parse_manifest(R306A_MANIFEST, R306A_MANIFEST_SHA256)
    need(set(entries) == set(R306A_EXPECTED_MANIFEST_MEMBERS),
         "Round306A exact 13-member seal")
    for member, expected in R306A_KNOWN_MEMBER_PINS.items():
        need(entries.get(member) == expected, "Round306A known member pin:" + member)
    snapshots: dict[str, tuple[int, int, int, int, int, int, int]] = {}
    for member, expected in entries.items():
        member_sha256, snapshot = sha256_path_snapshot(DATA / member, DATA)
        need(member_sha256 == expected, "Round306A sealed member:" + member)
        snapshots[member] = snapshot
    result_raw = stable_bytes(DATA / R306A_RESULT, DATA, 2_000_000)
    need(hashlib.sha256(result_raw).hexdigest() == entries[R306A_RESULT],
         "Round306A parsed result remains manifest-bound")
    result = strict_object(result_raw, R306A_RESULT)
    check_self(result, "result_sha256", "Round306A result")
    need(
        result["result_sha256"] == R306A_RESULT_SELF_SHA256
        and result["fresh_forward_application"]["component_count"] == 92688
        and result["fresh_forward_application"]["partition_sha256"] == R306A_PARTITION_SHA256
        and result["full_maximality_gate"]["full_maximality_proved"] is False,
        "Round306A result boundary",
    )
    verification_raw = stable_bytes(DATA / R306A_VERIFICATION, DATA, 3_000_000)
    need(hashlib.sha256(verification_raw).hexdigest() == entries[R306A_VERIFICATION],
         "Round306A parsed verification remains manifest-bound")
    verification = strict_object(verification_raw, R306A_VERIFICATION)
    check_self(verification, "verification_sha256", "Round306A verification")
    need(
        verification["status"] == "PASS_EXACT_CACHELESS_ROUND306A_FRESH_LEGAL_COMPONENT_DSU_REBUILD"
        and verification["exact_fresh_DSU_census"]["fresh_component_count"] == 92688
        and verification["strict_downstream_boundary"]["full_maximality_proved"] is False,
        "Round306A formal marker",
    )
    return entries, snapshots


def independent_source_maps(
    source_snapshots: dict[str, tuple[int, int, int, int, int, int, int]],
) -> tuple[
    dict[str, tuple[str, str, str]],
    dict[str, tuple[int, str, str, str]],
    dict[str, dict[str, Any]],
]:
    source: dict[str, tuple[str, str, str]] = {}
    inherited_dimension: dict[str, tuple[int, str, str, str]] = {}
    commitments: dict[str, dict[str, Any]] = {}
    specifications = (
        (
            "cm2_round245_source_g_retained_graph_mixed_sheet_quotient_certificate.json",
            "formal_retained_stratum_node_ledger", "retained_stratum_node_id", "R245",
        ),
        (
            "cm2_round246_source_g_whole_signature_retained_quotient_certificate.json",
            "formal_new_whole_signature_retained_stratum_node_ledger", "retained_stratum_node_id", "R246",
        ),
        (
            "cm2_round247_source_g_crossing_and_source_seam_retained_quotient_certificate.json",
            "formal_new_crossing_and_source_seam_retained_stratum_node_ledger", "retained_stratum_node_id", "R247",
        ),
    )
    inherited_hist: Counter[tuple[str, int]] = Counter()
    for name, table, id_field, package in specifications:
        def visit(row: dict[str, Any], package: str = package) -> None:
            member = row[id_field]
            dimension = row["local_dimension"]
            need(member not in inherited_dimension and dimension in (2, 3), "inherited dimension")
            inherited_dimension[member] = (
                dimension, package, member, row["row_sha256"],
            )
            inherited_hist[(package, dimension)] += 1

        commitments[package] = scan_rows(
            plain_row_iterator(DATA / name, table, source_snapshots[name]), id_field, visit
        )
    need(
        len(inherited_dimension) == 6388
        and sum(count for (package, dimension), count in inherited_hist.items() if dimension == 2) == 264
        and sum(count for (package, dimension), count in inherited_hist.items() if dimension == 3) == 6124,
        "inherited virtual census",
    )
    tranche_hist: Counter[str] = Counter()

    def registry(row: dict[str, Any]) -> None:
        member = row["registry_occurrence_id"]
        tranche = row["registry_entry_kind"]
        need(member not in source, "registry identity")
        source[member] = (
            tranche, row["Round294_occurrence_registry_row_id"], row["row_sha256"],
        )
        tranche_hist[tranche] += 1

    registry_commitment = scan_rows(
        gzip_row_iterator(
            DATA / R294_REGISTRY, DATA, "rows", source_snapshots[R294_REGISTRY]
        ),
        "Round294_occurrence_registry_row_id", registry,
    )
    commitments["R294"] = registry_commitment
    need(
        registry_commitment["row_count"] == R294_COMMITMENT["row_count"]
        and registry_commitment["row_ids_sha256"] == R294_COMMITMENT["row_ids_sha256"]
        and registry_commitment["row_hashes_sha256"] == R294_COMMITMENT["row_hashes_sha256"]
        and registry_commitment["rows_sha256"] == R294_COMMITMENT["rows_sha256"],
        "Round294 registry commitment",
    )

    def r266(row: dict[str, Any]) -> None:
        member = row["component_member_id"]
        kind = row["component_member_kind"]
        if kind == "EXPANDED_OCCURRENCE":
            need(member in source, "preserved occurrence coverage")
            return
        need(kind == "VALID_VIRTUAL_STRATUM" and member not in source, "virtual identity")
        tranche = row["component_member_source_kind"]
        if tranche == "INHERITED_ROUND247_VIRTUAL_STRATUM":
            need(member in inherited_dimension, "inherited virtual dimension coverage")
        else:
            need(tranche in {"ROUND248_WALL_BULK", "ROUND248_WALL_SHEET"}, "known virtual tranche")
        source[member] = (
            tranche, row["post_Round266_component_member_frontier_row_id"], row["row_sha256"],
        )

    r266_commitment = scan_rows(
        plain_row_iterator(
            DATA / R266_CERTIFICATE,
            "formal_post_Round266_component_member_frontier_ledger",
            source_snapshots[R266_CERTIFICATE],
        ),
        "post_Round266_component_member_frontier_row_id", r266,
    )
    commitments["R266"] = r266_commitment
    need(r266_commitment == R266_MEMBER_COMMITMENT and len(source) == 564492,
         "Round266 member commitment and total source cover")
    return source, inherited_dimension, commitments


def expected_class(
    tranche: str,
    member: str,
    inherited_dimension: dict[str, tuple[int, str, str, str]],
) -> tuple[str, str, str]:
    if tranche.startswith("PRESERVED_") or tranche.startswith("CANDIDATE_NEW_"):
        return "FORMAL_OCCURRENCE", "OCCURRENCE", "MULTI_REPRESENTATION_OCCURRENCE__GEOMETRY_NOT_YET_EXPANDED"
    if tranche == "ROUND248_WALL_BULK":
        return "VALID_VIRTUAL_STRATUM", "VIRTUAL_POSITIVE_3D", "POSITIVE_3D_CARRIER"
    if tranche == "ROUND248_WALL_SHEET":
        return "VALID_VIRTUAL_STRATUM", "VIRTUAL_SHEET", "HALF_OPEN_2D_SHEET"
    need(tranche == "INHERITED_ROUND247_VIRTUAL_STRATUM", "known tranche")
    dimension = inherited_dimension[member][0]
    return (
        "VALID_VIRTUAL_STRATUM",
        "VIRTUAL_SHEET" if dimension == 2 else "VIRTUAL_POSITIVE_3D",
        "HALF_OPEN_2D_SHEET" if dimension == 2 else "POSITIVE_3D_CARRIER",
    )


def stat_identity(info: os.stat_result) -> tuple[int, int, int, int, int, int, int]:
    return (
        info.st_dev, info.st_ino, info.st_mode, info.st_nlink, info.st_size,
        info.st_mtime_ns, info.st_ctime_ns,
    )


def candidate_snapshot(
    descriptor: int,
) -> tuple[
    tuple[int, int, int, int, int, int, int],
    dict[str, tuple[int, int, int, int, int, int, int]],
]:
    names = tuple(sorted(os.listdir(descriptor)))
    need(names == tuple(sorted(CANDIDATE_ORDER)), "candidate exact six-file set")
    files: dict[str, tuple[int, int, int, int, int, int, int]] = {}
    for name in names:
        info = os.stat(name, dir_fd=descriptor, follow_symlinks=False)
        need(
            stat.S_ISREG(info.st_mode) and info.st_nlink == 1
            and stat.S_IMODE(info.st_mode) == 0o600,
            "candidate file mode/link:" + name,
        )
        files[name] = stat_identity(info)
    return stat_identity(os.fstat(descriptor)), files


def enforce_candidate(candidate: Path) -> tuple[
    Path,
    int,
    tuple[
        tuple[int, int, int, int, int, int, int],
        dict[str, tuple[int, int, int, int, int, int, int]],
    ],
]:
    root = Path(os.path.abspath(os.fspath(PRIVATE_ROOT)))
    resolved = Path(os.path.abspath(os.fspath(candidate)))
    need(resolved.parent == root and resolved.name not in {"", ".", ".."},
         "candidate direct child policy")
    need(os.path.lexists(root) and not root.is_symlink(), "private root exists/no symlink")
    root_info = os.lstat(root)
    need(stat.S_ISDIR(root_info.st_mode) and stat.S_IMODE(root_info.st_mode) == 0o700,
         "private root mode")
    root_fd = os.open(
        root,
        os.O_RDONLY | getattr(os, "O_DIRECTORY", 0) | getattr(os, "O_NOFOLLOW", 0),
    )
    try:
        named = os.stat(resolved.name, dir_fd=root_fd, follow_symlinks=False)
        need(stat.S_ISDIR(named.st_mode) and stat.S_IMODE(named.st_mode) == 0o700,
             "candidate mode")
        descriptor = os.open(
            resolved.name,
            os.O_RDONLY | getattr(os, "O_DIRECTORY", 0) | getattr(os, "O_NOFOLLOW", 0),
            dir_fd=root_fd,
        )
        try:
            need(stat_identity(named) == stat_identity(os.fstat(descriptor)),
                 "candidate named-directory/fd binding")
            snapshot = candidate_snapshot(descriptor)
            need(snapshot == candidate_snapshot(descriptor),
                 "candidate directory and file census stable")
        except Exception:
            os.close(descriptor)
            raise
    finally:
        os.close(root_fd)
    return resolved, descriptor, snapshot


def candidate_sha256s(candidate_fd: int) -> dict[str, str]:
    return {name: hash_at(candidate_fd, name) for name in CANDIDATE_ORDER}


class ExpectedRows:
    def __init__(self, id_field: str) -> None:
        self.id_field = id_field
        self.file = tempfile.TemporaryFile(mode="w+b")
        self.rows, self.ids, self.hashes = ListHash(), ListHash(), ListHash()

    def add(self, payload: dict[str, Any]) -> None:
        row = close_row(payload)
        row_id = row[self.id_field]
        self.rows.add(row)
        self.ids.add(row_id)
        self.hashes.add(row["row_sha256"])
        self.file.write(canonical(row) + b"\n")

    def metadata(self) -> dict[str, Any]:
        return {
            "row_count": self.rows.count,
            "row_ids_sha256": self.ids.finish(),
            "row_hashes_sha256": self.hashes.finish(),
            "rows_sha256": self.rows.finish(),
        }

    def compare_iterator(self, iterator: Iterator[dict[str, Any]]) -> dict[str, Any]:
        self.file.flush()
        self.file.seek(0)

        def visit(row: dict[str, Any]) -> None:
            expected = self.file.readline()
            need(expected and expected.rstrip(b"\n") == canonical(row),
                 "candidate row exact independent reconstruction")

        actual = scan_rows(iterator, self.id_field, visit)
        need(not self.file.readline(), "candidate omitted expected row")
        need(actual == self.metadata(), "candidate ledger row commitments")
        return actual

    def close(self) -> None:
        self.file.close()


class ComponentState:
    def __init__(self) -> None:
        self.member_ids = ListHash()
        self.classes: Counter[str] = Counter()
        self.keys: set[str] = set()
        self.size = 0


def independently_rebuild_expected_rows(
    source: dict[str, tuple[str, str, str]],
    inherited: dict[str, tuple[int, str, str, str]],
    selected_sources: dict[tuple[str, str], tuple[str, str]],
    source_commitments: dict[str, dict[str, Any]],
    r306a_member_snapshot: tuple[int, int, int, int, int, int, int],
) -> tuple[dict[str, ExpectedRows], dict[str, Any], dict[str, int]]:
    outputs = {
        "member": ExpectedRows(ID_FIELDS["member"]),
        "component": ExpectedRows(ID_FIELDS["component"]),
        "pair": ExpectedRows(ID_FIELDS["pair"]),
        "source": ExpectedRows(ID_FIELDS["source"]),
        "gap": ExpectedRows(ID_FIELDS["gap"]),
    }
    components: dict[str, ComponentState] = defaultdict(ComponentState)
    class_counts: Counter[str] = Counter()
    keys: set[str] = set()

    def visit(row: dict[str, Any]) -> None:
        member = row["registry_occurrence_id"]
        tranche, source_row_id, source_row_hash = source[member]
        identity_class, denominator_class, profile = expected_class(
            tranche, member, inherited
        )
        inherited_item = inherited.get(member)
        primary_package = "R294" if identity_class == "FORMAL_OCCURRENCE" else "R266"
        component = row["final_component_id"]
        key = row["official_key_id"]
        state = components[component]
        state.size += 1
        state.classes[denominator_class] += 1
        state.keys.add(key)
        state.member_ids.add(member)
        class_counts[denominator_class] += 1
        keys.add(key)
        outputs["member"].add({
            ID_FIELDS["member"]: "round306b0-member-source:" + digest(member),
            "schema": SCHEMA + ".member-support-source-row.v1",
            "member_id": member,
            "base_root_id": row["base_root_id"],
            "Round306A_component_id": component,
            "official_key_id": key,
            "identity_class": identity_class,
            "identity_tranche": tranche,
            "pair_denominator_class": denominator_class,
            "physical_dimension_profile": profile,
            "primary_source_package": primary_package,
            "primary_source_row_id": source_row_id,
            "primary_source_row_sha256": source_row_hash,
            "inherited_virtual_source_package": (
                inherited_item[1] if inherited_item is not None else None
            ),
            "inherited_virtual_source_row_id": (
                inherited_item[2] if inherited_item is not None else None
            ),
            "inherited_virtual_source_row_sha256": (
                inherited_item[3] if inherited_item is not None else None
            ),
            "member_identity_preserved": True,
            "geometry_feature_expansion_deferred_to_Round306B": True,
            "formal_maximality_credit": 0,
            "formal_fibre_credit": 0,
            "formal_global_disposition_credit": 0,
        })

    r306a_commitment = scan_rows(
        gzip_row_iterator(
            DATA / R306A_MEMBER, DATA, "fresh_member_component_rows",
            r306a_member_snapshot,
        ),
        "Round306A_fresh_member_component_row_id", visit,
    )
    need(r306a_commitment == R306A_MEMBER_COMMITMENT, "Round306A member commitment")
    source_commitments["R306A"] = r306a_commitment

    selected_inventory = [
        {
            "source_package": package,
            "manifest_filename": SOURCE_PACKAGES[package][0],
            "manifest_file_sha256": manifest_sha256,
            "selected_member_filename": member,
            "selected_member_file_sha256": member_sha256,
        }
        for (package, member), (manifest_sha256, member_sha256)
        in selected_sources.items()
    ]
    selected_inventory.append({
        "source_package": "R306A",
        "manifest_filename": R306A_MANIFEST,
        "manifest_file_sha256": R306A_MANIFEST_SHA256,
        "selected_member_filename": R306A_MEMBER,
        "selected_member_file_sha256": R306A_MEMBER_SHA256,
    })
    scanned_tables = {
        "R245": "formal_retained_stratum_node_ledger",
        "R246": "formal_new_whole_signature_retained_stratum_node_ledger",
        "R247": "formal_new_crossing_and_source_seam_retained_stratum_node_ledger",
        "R266": "formal_post_Round266_component_member_frontier_ledger",
        "R294": "rows",
        "R306A": "fresh_member_component_rows",
    }
    for index, item in enumerate(sorted(
        selected_inventory,
        key=lambda row: (row["source_package"], row["selected_member_filename"]),
    )):
        package = item["source_package"]
        scanned = package in scanned_tables and not (
            package == "R294" and item["selected_member_filename"] != R294_REGISTRY
        )
        commitment = source_commitments.get(package) if scanned else None
        need(not scanned or commitment is not None,
             "independent source-table commitment:" + package)
        outputs["source"].add({
            ID_FIELDS["source"]: "round306b0-source-inventory:" + digest([
                package, item["selected_member_filename"], index,
            ]),
            "schema": SCHEMA + ".source-table-inventory-row.v1",
            **item,
            "source_table_name": scanned_tables.get(package) if scanned else None,
            "source_row_count": commitment["row_count"] if commitment else None,
            "source_row_ids_sha256": commitment["row_ids_sha256"] if commitment else None,
            "source_row_hashes_sha256": commitment["row_hashes_sha256"] if commitment else None,
            "source_rows_sha256": commitment["rows_sha256"] if commitment else None,
            "consumption_status": (
                "MANIFEST_AND_SELECTED_TABLE_STREAM_RECOMMITTED" if commitment else
                "MANIFEST_BOUND__FEATURE_TABLE_EXPANSION_DEFERRED_TO_ROUND306B"
            ),
            "geometry_feature_expansion_status": "DEFERRED_WITH_ZERO_CREDIT",
            "formal_maximality_credit": 0,
        })
    need(
        class_counts == {
            "OCCURRENCE": 431208,
            "VIRTUAL_POSITIVE_3D": 94660,
            "VIRTUAL_SHEET": 38624,
        }
        and len(components) == 92688 and len(keys) == 124,
        "current universe census",
    )
    within = 0
    per_class_within: Counter[str] = Counter()
    size_hist: Counter[int] = Counter()
    minimum = None
    maximum = 0
    for component_id in sorted(components):
        state = components[component_id]
        n_o = state.classes["OCCURRENCE"]
        n_v = state.classes["VIRTUAL_POSITIVE_3D"]
        n_s = state.classes["VIRTUAL_SHEET"]
        within += state.size * (state.size - 1) // 2
        size_hist[state.size] += 1
        minimum = state.size if minimum is None else min(minimum, state.size)
        maximum = max(maximum, state.size)
        per_class_within["OCCURRENCE__OCCURRENCE"] += n_o * (n_o - 1) // 2
        per_class_within["OCCURRENCE__VIRTUAL_POSITIVE_3D"] += n_o * n_v
        per_class_within["OCCURRENCE__VIRTUAL_SHEET"] += n_o * n_s
        per_class_within["VIRTUAL_POSITIVE_3D__VIRTUAL_POSITIVE_3D"] += n_v * (n_v - 1) // 2
        per_class_within["VIRTUAL_POSITIVE_3D__VIRTUAL_SHEET"] += n_v * n_s
        per_class_within["VIRTUAL_SHEET__VIRTUAL_SHEET"] += n_s * (n_s - 1) // 2
        official_keys = sorted(state.keys)
        outputs["component"].add({
            ID_FIELDS["component"]: "round306b0-component-census:" + digest(component_id),
            "schema": SCHEMA + ".component-census-row.v1",
            "Round306A_component_id": component_id,
            "member_count": state.size,
            "occurrence_member_count": n_o,
            "virtual_positive_3d_member_count": n_v,
            "virtual_sheet_member_count": n_s,
            "official_key_count": len(official_keys),
            "official_key_ids_sha256": digest(official_keys),
            "member_ids_sha256": state.member_ids.finish(),
            "component_size_is_from_complete_Round306A_partition": True,
            "maximality_proved": False,
            "formal_maximality_credit": 0,
            "formal_fibre_credit": 0,
            "formal_global_disposition_credit": 0,
        })
    need(
        within == EXPECTED["within_component_pair_count"]
        and minimum == 1 and maximum == 10599,
        "component denominator",
    )
    for pair_name, total in PAIR_CLASS_COUNTS.items():
        left, right = pair_name.split("__", 1)
        left_count, right_count = class_counts[left], class_counts[right]
        outputs["pair"].add({
            ID_FIELDS["pair"]: "round306b0-pair-denominator:" + digest(pair_name),
            "schema": SCHEMA + ".pair-denominator-row.v1",
            "pair_class": pair_name,
            "left_member_class": left,
            "right_member_class": right,
            "left_member_count": left_count,
            "right_member_count": right_count,
            "unordered_member_pair_count": total,
            "within_component_pair_count": per_class_within[pair_name],
            "cross_component_pair_count": total - per_class_within[pair_name],
            "pair_count_formula": "C(n,2)" if left == right else "n_left*n_right",
            "official_key_used_as_routing_filter": False,
            "complete_geometry_routing_performed": False,
            "formal_maximality_credit": 0,
        })
    audit = {
        "component_count": len(components),
        "within_component_pair_count": within,
        "cross_component_pair_count": EXPECTED["all_pair_count"] - within,
        "minimum_component_size": minimum,
        "maximum_component_size": maximum,
        "component_size_histogram": {
            str(size): count for size, count in sorted(size_hist.items())
        },
        "component_size_histogram_sha256": digest([
            [size, count] for size, count in sorted(size_hist.items())
        ]),
    }
    return outputs, audit, dict(class_counts)


def read_result(candidate_fd: int) -> dict[str, Any]:
    value = strict_object(
        stable_bytes_at(candidate_fd, FILES["result"], 3_000_000), FILES["result"]
    )
    check_self(value, "result_sha256", "Round306B0 result")
    return value


def admit_candidate(candidate_path: Path) -> tuple[
    Path, int, dict[str, str], dict[str, Any], dict[str, Any]
]:
    _round306a_entries, round306a_snapshots = bind_round306a()
    selected_sources, source_snapshots = bind_source_manifests()
    need(
        PIN.fullmatch(EXPECTED_PRODUCER_SHA256) is not None,
        "BLOCKED_LOCAL_FINALIZATION:freeze producer SHA after inserting Round306A manifest pin",
    )
    need(sha256_path(DATA / PRODUCER, DATA, 3_000_000) == EXPECTED_PRODUCER_SHA256,
         "inert producer pin")
    source, inherited, source_commitments = independent_source_maps(source_snapshots)
    expected_rows, component_audit, class_counts = independently_rebuild_expected_rows(
        source, inherited, selected_sources, source_commitments,
        round306a_snapshots[R306A_MEMBER],
    )
    del source, inherited, selected_sources, source_commitments
    candidate, descriptor, initial_snapshot = enforce_candidate(candidate_path)
    try:
        hashes = candidate_sha256s(descriptor)
        result = read_result(descriptor)
        commitments = {
            kind: expected_rows[kind].compare_iterator(
                gzip_row_iterator_at(descriptor, FILES[kind], TABLES[kind])
            )
            for kind in ("member", "component", "pair", "source", "gap")
        }
        need(
            commitments["member"]["row_count"] == 564492
            and commitments["component"]["row_count"] == 92688
            and commitments["pair"]["row_count"] == 6
            and commitments["source"]["row_count"] == 15
            and commitments["gap"]["row_count"] == 0,
            "exact five-ledger row counts",
        )
        output = result["output_ledgers"]
        need(set(output) == set(commitments), "result exact five output-ledger entries")
        ledger_status = (
            "PASS_ZERO_CREDIT_SOURCE_FREEZE_LEDGER__"
            "GEOMETRY_ROUTING_AND_MAXIMALITY_DEFERRED"
        )
        ledger_credit = {"maximality": 0, "fibre": 0, "global_disposition": 0}
        for kind, commitment in commitments.items():
            base = {
                "schema": SCHEMA + "." + kind + "-ledger.v1",
                "status": ledger_status,
                "formal_credit": ledger_credit,
                **commitment,
            }
            exact_meta = {
                **base,
                "ledger_sha256": digest(base),
                "filename": FILES[kind],
                "file_sha256": hashes[FILES[kind]],
                "file_size": initial_snapshot[1][FILES[kind]][4],
            }
            need(
                output[kind] == exact_meta
                and candidate_ledger_header_at(
                    descriptor, FILES[kind], TABLES[kind]
                ) == base | {"ledger_sha256": digest(base)},
                "result/output exact binding:" + kind,
            )
        expected_member_universe = {
            **EXPECTED,
            "identity_class_counts": dict(sorted(class_counts.items())),
            "occurrence_tranches": {
                "preserved_Round266": 126468,
                "new_Round288": 295336,
                "new_Round292": 9404,
            },
            "virtual_breakdown": {
                "positive_3D": 94660,
                "sheets": 38624,
                "Round248_sheets": 38360,
                "inherited_Round245_sheets": 264,
            },
        }
        expected_seal = {
            "manifest_filename": R306A_MANIFEST,
            "manifest_file_sha256": R306A_MANIFEST_SHA256,
            "member_ledger_file_sha256": R306A_MEMBER_SHA256,
            "result_file_sha256": R306A_RESULT_SHA256,
            "result_self_sha256": R306A_RESULT_SELF_SHA256,
            "verification_is_formal_credit_marker": True,
            "component_count": 92688,
            "partition_sha256": R306A_PARTITION_SHA256,
            "Round300A_zero_residual_is_not_full_maximality": True,
        }
        expected_source_binding = {
            "selected_sealed_manifest_count": len(SOURCE_PACKAGES) + 1,
            "all_selected_source_files_byte_pinned": True,
            "all_consumed_large_tables_stream_recommitted": True,
            "official_key_count": 124,
            "stale_116_key_scope_rejected": True,
            "official_key_used_as_pair_routing_filter": False,
            "cross_official_key_physical_adjacency_permitted": True,
        }
        expected_coverage = {
            "source_identity_or_manifest_binding_gap_count": 0,
            "complete_member_to_primary_source_binding": True,
            "complete_geometry_support_feature_cover_proved": False,
            "complete_pair_routing_proved": False,
            "transformed_face_exhaustion_proved": False,
            "cross_chart_exhaustion_proved": False,
            "retained_event_exhaustion_proved": False,
            "lower_2D_1D_0D_exhaustion_proved": False,
            "full_maximality_proved": False,
            "required_next": (
                "Round306B must expand exact 3D/2D/1D/0D support features and "
                "losslessly route all 158838084354 cross-component member pairs"
            ),
        }
        expected_credit_without_marker = {
            "member_universe_freeze": 0,
            "pair_denominator_freeze": 0,
            "maximality": 0,
            "fibre": 0,
            "global_disposition": 0,
            "D02": "BLOCKED",
            "CM2": "NO-GO_FOR_CLAIM",
        }
        expected_candidate_credit = {
            "member_universe_freeze": 1,
            "pair_denominator_freeze": 1,
            "maximality": 0,
            "fibre": 0,
            "global_disposition": 0,
            "D02": "BLOCKED",
            "CM2": "NO-GO_FOR_CLAIM",
        }
        need(
            set(result) == {
                "schema", "status", "producer_file_sha256", "sealed_Round306A",
                "member_universe", "component_denominator_audit",
                "six_pair_class_totals", "source_binding", "coverage_boundary",
                "formal_credit_without_independent_verification_marker",
                "candidate_credit_if_independently_verified", "output_ledgers",
                "candidate_is_formal_without_independent_verification_marker",
                "result_sha256",
            }
            and result["schema"] == SCHEMA
            and result["status"] == (
                "PASS_ROUND306B0_CURRENT_UNIVERSE_AND_PAIR_DENOMINATOR_FREEZE__"
                "CREDIT_REQUIRES_INDEPENDENT_VERIFICATION_MARKER__"
                "ZERO_MAXIMALITY_FIBRE_AND_GLOBAL_CREDIT"
            )
            and result["producer_file_sha256"] == EXPECTED_PRODUCER_SHA256
            and result["sealed_Round306A"] == expected_seal
            and result["member_universe"] == expected_member_universe
            and result["component_denominator_audit"] == component_audit
            and result["six_pair_class_totals"] == dict(sorted(PAIR_CLASS_COUNTS.items()))
            and result["source_binding"] == expected_source_binding
            and result["coverage_boundary"] == expected_coverage
            and result["formal_credit_without_independent_verification_marker"]
            == expected_credit_without_marker
            and result["candidate_credit_if_independently_verified"]
            == expected_candidate_credit
            and result["candidate_is_formal_without_independent_verification_marker"] is False,
            "Round306B0 exact zero-credit result boundary",
        )
        need(
            candidate_snapshot(descriptor) == initial_snapshot
            and stat_identity(os.lstat(candidate)) == initial_snapshot[0]
            and candidate_sha256s(descriptor) == hashes,
            "candidate named directory/files/hashes stable after admission",
        )
        need(
            all(
                stat_identity(os.lstat(DATA / member)) == snapshot
                for member, snapshot in source_snapshots.items()
            )
            and all(
                stat_identity(os.lstat(DATA / member)) == snapshot
                for member, snapshot in round306a_snapshots.items()
            ),
            "all source and Round306A manifest-bound snapshots stable after admission",
        )
        return candidate, descriptor, hashes, result, component_audit
    except Exception:
        os.close(descriptor)
        raise
    finally:
        for expected in expected_rows.values():
            expected.close()


def rejected(callback: Callable[[], None]) -> bool:
    try:
        callback()
    except Exception:
        return True
    return False


def semantic_contract(value: dict[str, Any]) -> None:
    need(
        value == {
            "members": 564492,
            "components": 92688,
            "all_pairs": 159325326786,
            "within": 487242432,
            "cross": 158838084354,
            "keys": 124,
            "R245_sheets": 264,
            "R248_sheets": 38360,
            "official_key_filter": False,
            "geometry_complete": False,
            "current_member_universe_freeze_credit": 0,
            "current_pair_denominator_freeze_credit": 0,
            "maximality_credit": 0,
            "fibre_credit": 0,
            "global_credit": 0,
        },
        "semantic zero-credit contract",
    )


def rename_noreplace(old_fd: int, old_name: str, new_fd: int, new_name: str) -> None:
    libc = ctypes.CDLL(None, use_errno=True)
    function = getattr(libc, "renameat2", None)
    need(function is not None, "renameat2 required")
    function.argtypes = [ctypes.c_int, ctypes.c_char_p, ctypes.c_int, ctypes.c_char_p, ctypes.c_uint]
    function.restype = ctypes.c_int
    if function(old_fd, os.fsencode(old_name), new_fd, os.fsencode(new_name), 1) != 0:
        code = ctypes.get_errno()
        if code == errno.EEXIST:
            raise FileExistsError(code, os.strerror(code), new_name)
        raise OSError(code, os.strerror(code), new_name)


def transaction_self_tests() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    def record(name: str, callback: Callable[[], None]) -> None:
        need(rejected(callback), "transaction self-test accepted:" + name)
        rows.append(close_row({
            "attack_name": name,
            "attack_class": "FILESYSTEM_TRANSACTION",
            "expected": "REJECT",
            "observed": "REJECT",
        }))

    with tempfile.TemporaryDirectory(prefix="cm2-r306b0-selftest-") as temporary:
        root = Path(temporary)
        private = root / "private"
        candidate = private / "candidate"
        private.mkdir(mode=0o700)
        candidate.mkdir(mode=0o700)
        regular = candidate / "x"
        regular.write_bytes(b"x")
        regular.chmod(0o600)

        def symlink_candidate() -> None:
            link = root / "link"
            link.symlink_to(candidate)
            need(not stat.S_ISLNK(os.lstat(link).st_mode), "symlink rejected")

        record("candidate_symlink", symlink_candidate)

        def hardlink() -> None:
            alias = candidate / "alias"
            os.link(regular, alias)
            need(os.lstat(regular).st_nlink == 1, "hardlink rejected")

        record("candidate_hardlink", hardlink)

        def wrong_mode() -> None:
            regular.chmod(0o644)
            need(stat.S_IMODE(os.lstat(regular).st_mode) == 0o600, "mode rejected")

        record("candidate_wrong_mode", wrong_mode)
        regular.chmod(0o600)

        def rename_collision() -> None:
            left = root / "left"
            right = root / "right"
            left.mkdir()
            right.mkdir()
            (left / "x").write_bytes(b"a")
            (right / "x").write_bytes(b"b")
            left_fd = os.open(left, os.O_RDONLY | getattr(os, "O_DIRECTORY", 0))
            right_fd = os.open(right, os.O_RDONLY | getattr(os, "O_DIRECTORY", 0))
            try:
                rename_noreplace(left_fd, "x", right_fd, "x")
            finally:
                os.close(left_fd)
                os.close(right_fd)

        record("rename_noreplace_collision", rename_collision)

        record(
            "extra_candidate_member",
            lambda: need(set(os.listdir(candidate)) == {"expected"}, "extra member rejected"),
        )
        record(
            "candidate_inside_deliverables",
            lambda: need(candidate.parent == DATA, "deliverables descendant rejected"),
        )
    return rows


def wire_grammar_self_tests() -> list[dict[str, Any]]:
    need(
        len(list(iter_final_array(io.StringIO('{"rows":[{},{}]}'), '"rows":['))) == 2
        and len(list(iter_final_array(io.StringIO('{"rows":[]}'), '"rows":['))) == 0,
        "valid final-array grammar fixtures",
    )
    rows: list[dict[str, Any]] = []
    fixtures = (
        ("missing_row_comma", '{"rows":[{}{}]}'),
        ("duplicate_row_comma", '{"rows":[{},,{}]}'),
        ("trailing_row_comma", '{"rows":[{},]}'),
    )
    for name, raw in fixtures:
        need(
            rejected(lambda raw=raw: list(
                iter_final_array(io.StringIO(raw), '"rows":[')
            )),
            "invalid candidate ledger grammar accepted:" + name,
        )
        rows.append(close_row({
            "attack_name": name,
            "attack_class": "CANDIDATE_WIRE_GRAMMAR",
            "expected": "REJECT",
            "observed": "REJECT",
        }))
    return rows


def build_attack_suite(
    candidate_hashes: dict[str, str] | None,
    verifier_sha256: str,
) -> dict[str, Any]:
    baseline = {
        "members": 564492,
        "components": 92688,
        "all_pairs": 159325326786,
        "within": 487242432,
        "cross": 158838084354,
        "keys": 124,
        "R245_sheets": 264,
        "R248_sheets": 38360,
        "official_key_filter": False,
        "geometry_complete": False,
        "current_member_universe_freeze_credit": 0,
        "current_pair_denominator_freeze_credit": 0,
        "maximality_credit": 0,
        "fibre_credit": 0,
        "global_credit": 0,
    }
    mutations = (
        ("stale_116_keys", "keys", 116),
        ("stale_53968_occurrences", "members", 53968),
        ("stale_150876_members", "members", 150876),
        ("stale_94444_components", "components", 94444),
        ("omit_304740_new_occurrences", "members", 259752),
        ("omit_R245_264_sheets", "R245_sheets", 0),
        ("omit_R248_38360_sheets", "R248_sheets", 0),
        ("reinsert_400_empty_bulks", "members", 564892),
        ("all_pair_minus_one", "all_pairs", 159325326785),
        ("within_pair_plus_one", "within", 487242433),
        ("cross_pair_minus_one", "cross", 158838084353),
        ("official_key_prefilter", "official_key_filter", True),
        ("geometry_claim_forgery", "geometry_complete", True),
        (
            "premature_member_universe_freeze_credit",
            "current_member_universe_freeze_credit", 1,
        ),
        (
            "premature_pair_denominator_freeze_credit",
            "current_pair_denominator_freeze_credit", 1,
        ),
        ("maximality_credit_forgery", "maximality_credit", 1),
        ("fibre_credit_forgery", "fibre_credit", 124),
        ("global_credit_forgery", "global_credit", 224580),
    )
    semantic_rows: list[dict[str, Any]] = []
    semantic_contract(baseline)
    for name, field, replacement in mutations:
        forged = dict(baseline)
        forged[field] = replacement
        need(rejected(lambda forged=forged: semantic_contract(forged)),
             "semantic mutation accepted:" + name)
        semantic_rows.append(close_row({
            "attack_name": name,
            "attack_class": "SEMANTIC_CONTRACT_UNIT",
            "mutated_field": field,
            "expected": "REJECT",
            "observed": "REJECT",
        }))
    transaction_rows = transaction_self_tests()
    grammar_rows = wire_grammar_self_tests()
    rows = semantic_rows + transaction_rows + grammar_rows
    payload = {
        "schema": SCHEMA + ".attack-suite.v1",
        "status": "PASS_ROUND306B0_DEFENSE_IN_DEPTH_ATTACKS",
        "binding_mode": (
            "EXACT_FORMAL_CANDIDATE" if candidate_hashes is not None
            else "LIGHTWEIGHT_SCAFFOLD_SELF_TEST"
        ),
        "producer": {
            "filename": PRODUCER,
            "file_sha256": EXPECTED_PRODUCER_SHA256,
            "treated_as_inert_bytes_only": True,
        },
        "runtime_verifier": {"filename": VERIFIER, "file_sha256": verifier_sha256},
        "baseline_candidate_file_sha256s": (
            dict(sorted(candidate_hashes.items())) if candidate_hashes is not None else None
        ),
        "semantic_contract_unit_count": len(semantic_rows),
        "semantic_contract_unit_rejected_count": len(semantic_rows),
        "filesystem_transaction_attack_count": len(transaction_rows),
        "filesystem_transaction_rejected_count": len(transaction_rows),
        "candidate_wire_grammar_attack_count": len(grammar_rows),
        "candidate_wire_grammar_rejected_count": len(grammar_rows),
        "attack_count": len(rows),
        "rejected_count": len(rows),
        "all_rejected": True,
        "attack_rows_sha256": digest(rows),
        "attack_rows": rows,
    }
    return {**payload, "attack_suite_sha256": digest(payload)}


def build_verification(
    hashes: dict[str, str], result: dict[str, Any],
    component_audit: dict[str, Any], attacks: dict[str, Any],
    verifier_sha256: str,
) -> dict[str, Any]:
    check_self(attacks, "attack_suite_sha256", "attack suite")
    payload = {
        "schema": SCHEMA + ".independent-verification.v1",
        "status": "PASS_EXACT_ROUND306B0_UNIVERSE_SUPPORT_SOURCE_FREEZE",
        "producer": {
            "filename": PRODUCER,
            "file_sha256": EXPECTED_PRODUCER_SHA256,
            "treated_as_inert_pinned_bytes_only": True,
            "imported_executed_parsed_or_tokenized": False,
        },
        "runtime_verifier": {"filename": VERIFIER, "file_sha256": verifier_sha256},
        "sealed_Round306A": {
            "manifest_filename": R306A_MANIFEST,
            "manifest_file_sha256": R306A_MANIFEST_SHA256,
            "partition_sha256": R306A_PARTITION_SHA256,
            "formal_verification_marker_required": True,
        },
        "candidate": {
            "dedicated_private_root": PRIVATE_ROOT.name,
            "exact_six_file_set": list(CANDIDATE_ORDER),
            "exact_file_sha256s": dict(sorted(hashes.items())),
            "result_self_sha256": result["result_sha256"],
            "candidate_opened_only_after_independent_source_and_partition_reconstruction": True,
            "all_564492_member_source_rows_equal_independent_reconstruction": True,
            "all_92688_component_rows_equal_independent_reconstruction": True,
            "all_six_pair_rows_equal_independent_reconstruction": True,
        },
        "exact_denominator": {
            **component_audit,
            "member_count": 564492,
            "occurrence_count": 431208,
            "virtual_positive_3d_count": 94660,
            "virtual_sheet_count": 38624,
            "all_unordered_member_pair_count": 159325326786,
            "official_key_count": 124,
            "official_key_used_as_routing_filter": False,
        },
        "attack_suite": {
            "filename": ATTACK,
            "file_sha256": hashlib.sha256(canonical(attacks)).hexdigest(),
            "object_self_sha256": attacks["attack_suite_sha256"],
            "attack_count": attacks["attack_count"],
            "rejected_count": attacks["rejected_count"],
            "all_rejected": True,
        },
        "formal_credit_without_this_verification_marker": {
            "member_universe_freeze": 0,
            "pair_denominator_freeze": 0,
            "maximality": 0,
            "fibre": 0,
            "global_disposition": 0,
        },
        "formal_credit_transition_at_this_verification_marker": {
            "member_universe_freeze": 1,
            "pair_denominator_freeze": 1,
            "maximality": 0,
            "fibre": 0,
            "global_disposition": 0,
        },
        "strict_downstream_boundary": {
            "geometry_feature_cover_proved": False,
            "cross_component_pair_routing_proved": False,
            "full_maximality_proved": False,
            "official_fibres_exhausted": 0,
            "Source_G_global_dispositions_completed": 0,
            "D02_status": "BLOCKED",
            "CM2_status": "NO-GO_FOR_CLAIM",
        },
        "atomic_publication": {
            "promotion_order": list(PROMOTION_ORDER),
            "attack_first": True,
            "verification_last_and_sole_credit_marker": True,
            "renameat2_RENAME_NOREPLACE": True,
            "fsync_stage_and_output_after_each_rename": True,
            "exact_prefix_recovery_only": True,
            "no_clobber": True,
        },
    }
    return {**payload, "verification_sha256": digest(payload)}


def exclusive_write_at(directory_fd: int, name: str, raw: bytes) -> None:
    descriptor = os.open(
        name, os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, "O_NOFOLLOW", 0),
        0o600, dir_fd=directory_fd,
    )
    try:
        offset = 0
        while offset < len(raw):
            offset += os.write(descriptor, raw[offset:])
        os.fsync(descriptor)
        info = os.fstat(descriptor)
        need(stat.S_ISREG(info.st_mode) and info.st_nlink == 1 and info.st_size == len(raw),
             "exclusive stage write:" + name)
    finally:
        os.close(descriptor)


def copy_candidate_to_stage(
    candidate_fd: int, stage_fd: int, name: str, expected_sha256: str,
) -> None:
    source_fd = os.open(
        name, os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0), dir_fd=candidate_fd
    )
    target_fd = os.open(
        name, os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, "O_NOFOLLOW", 0),
        0o600, dir_fd=stage_fd,
    )
    state = hashlib.sha256()
    try:
        source_before = os.fstat(source_fd)
        need(stat.S_ISREG(source_before.st_mode) and source_before.st_nlink == 1,
             "candidate source regular:" + name)
        while True:
            block = os.read(source_fd, 1 << 20)
            if not block:
                break
            state.update(block)
            offset = 0
            while offset < len(block):
                offset += os.write(target_fd, block[offset:])
        os.fsync(target_fd)
        source_after = os.fstat(source_fd)
        target = os.fstat(target_fd)
        need(
            state.hexdigest() == expected_sha256
            and stat_identity(source_before) == stat_identity(source_after)
            and source_before.st_size == target.st_size
            and target.st_nlink == 1 and stat.S_IMODE(target.st_mode) == 0o600,
            "exact candidate stage copy:" + name,
        )
    finally:
        os.close(source_fd)
        os.close(target_fd)


def hash_at(directory_fd: int, name: str) -> str:
    descriptor = os.open(name, os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0), dir_fd=directory_fd)
    state = hashlib.sha256()
    try:
        before = os.fstat(descriptor)
        need(stat.S_ISREG(before.st_mode) and before.st_nlink == 1, "hash-at regular:" + name)
        while True:
            block = os.read(descriptor, 1 << 20)
            if not block:
                break
            state.update(block)
        need(stat_identity(before) == stat_identity(os.fstat(descriptor)),
             "hash-at stable:" + name)
    finally:
        os.close(descriptor)
    return state.hexdigest()


def publish_formal(
    candidate_fd: int,
    hashes: dict[str, str],
    attack_raw: bytes,
    verification_raw: bytes,
) -> None:
    expected_hashes = {
        ATTACK: hashlib.sha256(attack_raw).hexdigest(),
        **hashes,
        VERIFICATION: hashlib.sha256(verification_raw).hexdigest(),
    }
    data_fd = os.open(
        DATA,
        os.O_RDONLY | getattr(os, "O_DIRECTORY", 0) | getattr(os, "O_NOFOLLOW", 0),
    )
    marker_renamed = False
    marker_identity: tuple[int, int] | None = None
    stage_fd = -1
    try:
        fcntl.flock(data_fd, fcntl.LOCK_EX)
        states: list[bool] = []
        seen_absent = False
        for name in PROMOTION_ORDER:
            try:
                info = os.stat(name, dir_fd=data_fd, follow_symlinks=False)
            except FileNotFoundError:
                seen_absent = True
                states.append(False)
                continue
            need(not seen_absent, "formal targets must be an exact committed prefix")
            need(stat.S_ISREG(info.st_mode) and info.st_nlink == 1,
                 "existing formal prefix regular:" + name)
            need(hash_at(data_fd, name) == expected_hashes[name],
                 "existing formal prefix exact:" + name)
            states.append(True)
        need(not states[-1], "verification marker already exists")
        stage_name = "." + PREFIX + ".promotion-stage." + digest(expected_hashes)[:24]
        try:
            os.mkdir(stage_name, 0o700, dir_fd=data_fd)
        except FileExistsError:
            pass
        stage_info = os.stat(stage_name, dir_fd=data_fd, follow_symlinks=False)
        need(stat.S_ISDIR(stage_info.st_mode) and stat.S_IMODE(stage_info.st_mode) == 0o700,
             "promotion stage directory")
        stage_fd = os.open(
            stage_name,
            os.O_RDONLY | getattr(os, "O_DIRECTORY", 0) | getattr(os, "O_NOFOLLOW", 0),
            dir_fd=data_fd,
        )
        expected_stage = {
            name for index, name in enumerate(PROMOTION_ORDER) if not states[index]
        }
        existing_stage = set(os.listdir(stage_fd))
        need(existing_stage <= expected_stage, "no foreign promotion stage members")
        for name in PROMOTION_ORDER:
            if name not in expected_stage or name in existing_stage:
                continue
            if name == ATTACK:
                exclusive_write_at(stage_fd, name, attack_raw)
            elif name == VERIFICATION:
                exclusive_write_at(stage_fd, name, verification_raw)
            else:
                copy_candidate_to_stage(candidate_fd, stage_fd, name, hashes[name])
            need(hash_at(stage_fd, name) == expected_hashes[name], "stage exact:" + name)
            os.fsync(stage_fd)
        need(set(os.listdir(stage_fd)) == expected_stage, "exact complete promotion stage")
        candidate_before = candidate_snapshot(candidate_fd)
        try:
            for index, name in enumerate(PROMOTION_ORDER):
                if states[index]:
                    continue
                need(hash_at(stage_fd, name) == expected_hashes[name],
                     "pre-rename stage hash:" + name)
                source_info = os.stat(name, dir_fd=stage_fd, follow_symlinks=False)
                rename_noreplace(stage_fd, name, data_fd, name)
                if name == VERIFICATION:
                    # Ownership must be recorded immediately after the successful
                    # rename, before any fallible fsync/stat/hash postcondition.
                    marker_renamed = True
                    marker_identity = (source_info.st_dev, source_info.st_ino)
                os.fsync(stage_fd)
                os.fsync(data_fd)
                target_info = os.stat(name, dir_fd=data_fd, follow_symlinks=False)
                need(
                    (source_info.st_dev, source_info.st_ino)
                    == (target_info.st_dev, target_info.st_ino)
                    and hash_at(data_fd, name) == expected_hashes[name],
                    "post-rename inode/hash:" + name,
                )
            need(
                candidate_snapshot(candidate_fd) == candidate_before
                and candidate_sha256s(candidate_fd) == hashes,
                "post-marker candidate stable",
            )
            for name in PROMOTION_ORDER:
                need(hash_at(data_fd, name) == expected_hashes[name],
                     "post-marker full formal bundle:" + name)
            need(not os.listdir(stage_fd), "promotion stage empty after commit")
            os.rmdir(stage_name, dir_fd=data_fd)
            os.fsync(data_fd)
        except Exception:
            if marker_renamed and marker_identity is not None:
                try:
                    current = os.stat(VERIFICATION, dir_fd=data_fd, follow_symlinks=False)
                except FileNotFoundError:
                    pass
                else:
                    if (
                        (current.st_dev, current.st_ino) == marker_identity
                        and hash_at(data_fd, VERIFICATION) == expected_hashes[VERIFICATION]
                    ):
                        os.unlink(VERIFICATION, dir_fd=data_fd)
                        os.fsync(data_fd)
            raise
    finally:
        if stage_fd >= 0:
            os.close(stage_fd)
        try:
            fcntl.flock(data_fd, fcntl.LOCK_UN)
        finally:
            os.close(data_fd)


def contract() -> dict[str, Any]:
    upstream_ready = PIN.fullmatch(R306A_MANIFEST_SHA256) is not None
    producer_ready = PIN.fullmatch(EXPECTED_PRODUCER_SHA256) is not None
    return {
        "schema": SCHEMA + ".independent-verifier-contract.v1",
        "status": (
            "READY_FOR_INDEPENDENT_ADMISSION" if upstream_ready and producer_ready
            else "BLOCKED_SINGLE_UPSTREAM_PIN_AND_CONSEQUENT_LOCAL_CACHEBUSTER"
        ),
        "single_missing_upstream_finalization": {
            "constant": "R306A_MANIFEST_SHA256",
            "artifact": R306A_MANIFEST,
            "currently_finalized": upstream_ready,
        },
        "consequent_local_cachebuster": {
            "constant": "EXPECTED_PRODUCER_SHA256",
            "currently_finalized": producer_ready,
            "not_an_additional_upstream_datum": True,
        },
        "candidate_files": list(CANDIDATE_ORDER),
        "promotion_order": list(PROMOTION_ORDER),
        "expected_member_count": 564492,
        "expected_component_count": 92688,
        "expected_cross_component_pair_count": 158838084354,
        "formal_maximality_credit": 0,
        "producer_or_Round306A_producer_imported_executed_parsed_or_tokenized": False,
    }


def self_test() -> dict[str, Any]:
    expected_member_universe_base_keys = {
        "member_count", "occurrence_count", "virtual_count",
        "virtual_positive_3d_count", "virtual_sheet_count",
        "R248_sheet_count", "R245_sheet_count", "component_count",
        "official_key_count", "all_pair_count", "within_component_pair_count",
        "cross_component_pair_count", "minimum_component_size",
        "maximum_component_size",
    }
    need(
        set(EXPECTED) == expected_member_universe_base_keys
        and EXPECTED["virtual_count"]
        == EXPECTED["virtual_positive_3d_count"] + EXPECTED["virtual_sheet_count"]
        and EXPECTED["virtual_sheet_count"]
        == EXPECTED["R248_sheet_count"] + EXPECTED["R245_sheet_count"],
        "exact member-universe base-key and virtual census regression",
    )
    semantic_contract({
        "members": 564492, "components": 92688, "all_pairs": 159325326786,
        "within": 487242432, "cross": 158838084354, "keys": 124,
        "R245_sheets": 264, "R248_sheets": 38360,
        "official_key_filter": False, "geometry_complete": False,
        "current_member_universe_freeze_credit": 0,
        "current_pair_denominator_freeze_credit": 0,
        "maximality_credit": 0, "fibre_credit": 0, "global_credit": 0,
    })
    manifest_checks = {
        label: hashlib.sha256(stable_bytes(DATA / manifest, DATA, 1_000_000)).hexdigest()
        == expected
        for label, (manifest, expected, _members) in SOURCE_PACKAGES.items()
    }
    need(all(manifest_checks.values()), "lightweight manifest checks")
    attacks = build_attack_suite(None, runtime_verifier_sha256())
    check_self(attacks, "attack_suite_sha256", "self-test attack suite")
    return {
        "status": "PASS_ROUND306B0_LIGHTWEIGHT_INDEPENDENT_VERIFIER_SELF_TEST",
        "source_manifest_pin_checks": manifest_checks,
        "semantic_attack_count": attacks["semantic_contract_unit_count"],
        "filesystem_transaction_attack_count": attacks["filesystem_transaction_attack_count"],
        "candidate_wire_grammar_attack_count": attacks["candidate_wire_grammar_attack_count"],
        "exact_member_universe_base_key_regression": True,
        "attack_count": attacks["attack_count"],
        "rejected_count": attacks["rejected_count"],
        "single_missing_upstream_finalization": contract()["single_missing_upstream_finalization"],
        "large_source_or_candidate_opened": False,
        "formal_artifact_written": False,
        "formal_maximality_credit": 0,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--print-contract", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--candidate-dir", type=Path)
    parser.add_argument("--promote", action="store_true")
    args = parser.parse_args()
    need(sum((args.print_contract, args.self_test, args.candidate_dir is not None)) == 1,
         "choose exactly one explicit verifier mode")
    need(not args.promote or args.candidate_dir is not None, "--promote requires --candidate-dir")
    if args.print_contract:
        print(canonical(contract()).decode("ascii"))
        return
    if args.self_test:
        print(canonical(self_test()).decode("ascii"))
        return
    assert args.candidate_dir is not None
    _candidate, candidate_fd, hashes, result, component_audit = admit_candidate(args.candidate_dir)
    try:
        verifier_sha256 = runtime_verifier_sha256()
        attacks = build_attack_suite(hashes, verifier_sha256)
        attack_raw = canonical(attacks)
        verification = build_verification(
            hashes, result, component_audit, attacks, verifier_sha256
        )
        verification_raw = canonical(verification)
        if args.promote:
            publish_formal(candidate_fd, hashes, attack_raw, verification_raw)
            print(verification_raw.decode("ascii"))
            return
        print(canonical({
            "status": "PASS_EXACT_ROUND306B0_PRIVATE_CANDIDATE_ADMISSION__ZERO_FORMAL_CREDIT",
            "candidate_file_sha256s": dict(sorted(hashes.items())),
            "candidate_result_sha256": result["result_sha256"],
            "attack_suite_file_sha256": hashlib.sha256(attack_raw).hexdigest(),
            "verification_file_sha256": hashlib.sha256(verification_raw).hexdigest(),
            "formal_member_universe_freeze_credit": 0,
            "formal_pair_denominator_freeze_credit": 0,
            "formal_maximality_credit": 0,
            "formal_artifact_written": False,
        }).decode("ascii"))
    finally:
        os.close(candidate_fd)


if __name__ == "__main__":
    main()
