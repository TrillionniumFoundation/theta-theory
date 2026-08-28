#!/usr/bin/env python3
"""Round306B0: freeze the post-Round306A universe and source denominators.

This is deliberately *not* a maximality audit.  It binds one sealed
Round306A partition, reclassifies every current member against the sealed
occurrence/virtual source registries, and freezes the exact pair denominator
which the later Round306B geometry audit must exhaust.

The sole missing upstream datum at scaffolding time is the SHA-256 of the
formal Round306A manifest.  Until ``R306A_MANIFEST_SHA256`` is replaced by a
64-lowercase-hex digest, every reconstruction mode fails before opening a
large source.  ``--print-contract`` and ``--self-test`` remain lightweight.

The producer writes only a private candidate.  Formal publication belongs to
the independent promotion verifier and remains attack-first / verification-
last.  No output of this file carries maximality, fibre, disposition, D02, or
CM2 credit.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from dataclasses import dataclass, field
import ctypes
import errno
import gzip
import hashlib
import io
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
PIN = re.compile(r"^[0-9a-f]{64}$")
ENCODER = json.JSONEncoder(
    ensure_ascii=True, allow_nan=False, sort_keys=True, separators=(",", ":")
)

# SINGLE UPSTREAM FINALIZATION DATUM.  Replace this one logical pin in both
# Round306B0 programs only after the Round306A verification-last seal exists.
R306A_MANIFEST_SHA256 = "35da99af5bb4c424284af2d7b396fc94b82dd6c6aa468c6a43a139107f9d9efc"

R306A_PREFIX = "cm2_round306a_source_g_r305b_fresh_legal_component_dsu_rebuild"
R306A = {
    "producer": R306A_PREFIX + ".py",
    "edge": R306A_PREFIX + "_edge_application_ledger.json.gz",
    "member": R306A_PREFIX + "_member_component_ledger.json.gz",
    "promoted": R306A_PREFIX + "_r305b_promoted_edge_application_ledger.json.gz",
    "frontier": R306A_PREFIX + "_r300a_reprojection_ledger.json.gz",
    "wtail": R306A_PREFIX + "_wtail_disposition_ledger.json.gz",
    "residual": R306A_PREFIX + "_residual_gate_ledger.json.gz",
    "result": R306A_PREFIX + "_result.json",
    "verifier": R306A_PREFIX + "_promotion_verifier.py",
    "attack": R306A_PREFIX + "_attack_suite.json",
    "verification": R306A_PREFIX + "_verification.json",
    "report": R306A_PREFIX + "_report.md",
    "cold": R306A_PREFIX + "_cold_replay.md",
    "manifest": R306A_PREFIX + "_manifest.sha256",
}
R306A_EXPECTED_MANIFEST_MEMBERS = frozenset(
    value for key, value in R306A.items() if key != "manifest"
)
R306A_KNOWN_MEMBER_PINS = {
    R306A["producer"]: "ab798332c82f7aa3656c61e3b31698a30b0fa1a83d24900432e076e445d6f5d5",
    R306A["edge"]: "6da4620a100c980f921350f162fda064580e603f8ff7221eeed768b8bd091d1f",
    R306A["member"]: "710ebb660a7e7fad6a691c03bf845cf0081037ed09cc49a885c94c4bc472c276",
    R306A["promoted"]: "08f9ff2f5df0210cedd8cb3f8d998846e3722bd6bb0a2216d8d6c24a95a64a41",
    R306A["frontier"]: "c3e62f9833c333fb89758edd5c3f1648364a70b91bd1ed85650241a4cd10b673",
    R306A["wtail"]: "6bdcc231b3cfd67f18ff3c62c27af08fdc9eb562a2c4e24a601798c0ad6d2556",
    R306A["residual"]: "1e79d529f3ca1fcefa170263a5d8b88929361ea27c0eeb3c6de108b870f9d8b8",
    R306A["result"]: "febe77da4285791b54e098c80a4b868c1e5dc6e43e98a7553bfff5e065075010",
    R306A["verifier"]: "60cc0f9cec6c8f4121f7ed7fde45b11e1b72bd9adc897364d9c0937c92a54c72",
}
R306A_RESULT_SELF_SHA256 = "6ee906cddae42e6df086cec26c7e0898ebe198519ce96605fd609a20c4f1e46a"
R306A_PARTITION_SHA256 = "a3f7ce1e28a956a46803ef466709ded0053633f5e104746c6d1e6e51b873e19c"

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


@dataclass(frozen=True)
class Package:
    manifest: str
    manifest_sha256: str
    selected_members: tuple[str, ...]


PACKAGES: dict[str, Package] = {
    "R245": Package(
        "cm2_round245_source_g_retained_graph_mixed_sheet_quotient_manifest.sha256",
        "1aff29f3a42b618ca85e5a1d3c537307e32326f8d5092b82d4253a5bf6e1c4ac",
        ("cm2_round245_source_g_retained_graph_mixed_sheet_quotient_certificate.json",),
    ),
    "R246": Package(
        "cm2_round246_source_g_whole_signature_retained_quotient_manifest.sha256",
        "1d25aed877e9cff20fd6c705e8393ffe96a113532b0453a34e8adcec474080ef",
        ("cm2_round246_source_g_whole_signature_retained_quotient_certificate.json",),
    ),
    "R247": Package(
        "cm2_round247_source_g_crossing_and_source_seam_retained_quotient_manifest.sha256",
        "3399a32de8fc1191eb8214d48da064a1412f0c1dab5f9e044d30d7940a6993f2",
        ("cm2_round247_source_g_crossing_and_source_seam_retained_quotient_certificate.json",),
    ),
    "R248": Package(
        "cm2_round248_source_g_wall_finite_key_retained_quotient_manifest.sha256",
        "b1ddedd01041e71b5c12fa4989726815c8685e6df77f54d9dbddda64aaf89e07",
        ("cm2_round248_source_g_wall_finite_key_retained_quotient_certificate.json",),
    ),
    "R266": Package(
        "cm2_round266_source_g_expanded_curved_face_closure_manifest.sha256",
        "63fb5b25d52ca5de579256499629d04d15f6a313e0a73f7e80fcb463385cbe09",
        ("cm2_round266_source_g_expanded_curved_face_closure_certificate.json",),
    ),
    "R275": Package(
        "cm2_round275_source_g_complete_reverse_rechart_materialization_manifest.sha256",
        "a5dbf43a144a0a752f467911ee59e6afd6d2d60d27e0bc80bc45b7afa9334669",
        ("cm2_round275_source_g_complete_reverse_rechart_materialization_certificate.json",),
    ),
    "R287": Package(
        "cm2_round287_source_g_rechart_terminal_occurrence_disposition_probe_manifest.sha256",
        "85a9d4fcf9d9931a0e352eeef7582347b12325b92ffc78f2ee40c77c58093751",
        ("cm2_round287_source_g_rechart_terminal_occurrence_disposition_probe_ledger.json.gz",),
    ),
    "R291": Package(
        "cm2_round291_source_g_complete_lower_stratum_local_disposition_freeze_manifest.sha256",
        "d655907a45cfb7b47ebdc822d35a0e604fc27fa38547c300139c116d7a2191ce",
        ("cm2_round291_source_g_complete_lower_stratum_local_disposition_freeze_ledger.json.gz",),
    ),
    "R294": Package(
        "cm2_round294_source_g_occurrence_registry_atomic_promotion_manifest.sha256",
        "90d5cda0271610bf95a72f94e9bae8e192425580019dd3c823b5a69d20e52131",
        (
            "cm2_round294_source_g_occurrence_registry_atomic_promotion_registry_ledger.json.gz",
            "cm2_round294_source_g_occurrence_registry_atomic_promotion_representation_binding_ledger.json.gz",
        ),
    ),
    "R294B": Package(
        "cm2_round294b_source_g_registry_builder_admission_closure_manifest.sha256",
        "fc16aa2792a59dff922afcc8ec66b1ca015251af3c5f718d9d909439a2990d76",
        (
            "cm2_round294_source_g_occurrence_registry_atomic_promotion_manifest.sha256",
            "cm2_round294b_source_g_registry_builder_admission_closure_verification.json",
        ),
    ),
    "R295C": Package(
        "cm2_round295c_source_g_all_stratum_scope_composition_closure_manifest.sha256",
        "a9499856148480b9ddd5b0dd9ea8de28b989b592477c9a3b7ea43541772180c1",
        ("cm2_round295c_source_g_all_stratum_scope_composition_closure_ledger.json.gz",),
    ),
    "R299A": Package(
        "cm2_round299a_source_g_refined_occurrence_official_key_binding_closure_manifest.sha256",
        "b1dfe718dd2b7477d9cc4067f1bade59d1589b3822eaf4b94b9dd721e61b468e",
        ("cm2_round299a_source_g_refined_occurrence_official_key_binding_closure_ledger.json.gz",),
    ),
}

R294_REGISTRY = PACKAGES["R294"].selected_members[0]
R266_CERTIFICATE = PACKAGES["R266"].selected_members[0]

R294_COMMITMENT = {
    "row_count": 431_208,
    "row_ids_sha256": "bbaca3ecbb804a87fd509aac2b8bd9f505d0c008e7bddbeb1a2ecb2a966f5509",
    "row_hashes_sha256": "ea98de3dab7e6f308f5a07d04bc29ca0d9dcd265a5323d8ecdb728cc501eed56",
    "rows_sha256": "33936ecd04cbce9f9a308b0da10381bd854b45028db53db5d3cbb9aa8b264044",
    "occurrence_ids_sha256": "169869b5755eda22f1527e7393a5bef0a77a842eefbdf45ab34d315b0dad1936",
}
R266_MEMBER_COMMITMENT = {
    "row_count": 259_752,
    "row_ids_sha256": "f064d177c25985b38c899c651923b83ba47ee36b465902cca85a4c21e0c33ca6",
    "row_hashes_sha256": "1f28c84d14cf3fabb38d0f2d1fdf862ce8f6a4559552d68fd9c0a5bd0a3ed3ee",
    "rows_sha256": "28398acde446047ff4a210b2fa0831d2c44e3758f7e9239b5ec63cecc386b257",
}
R306A_MEMBER_COMMITMENT = {
    "row_count": 564_492,
    "row_ids_sha256": "befaf5ae8a8ae109912649201e5efd90a03898edc02b5518cadec93e1f835165",
    "row_hashes_sha256": "003ecfe414434477a404c7b1912bfd117e98fc4883faee36119144b877f923ad",
    "rows_sha256": "43bc3ca15f58b6dd089b776c6c21f68fb246eb6af0590974129e20beef93eabd",
}

EXPECTED = {
    "member_count": 564_492,
    "occurrence_count": 431_208,
    "virtual_count": 133_284,
    "virtual_positive_3d_count": 94_660,
    "virtual_sheet_count": 38_624,
    "R248_sheet_count": 38_360,
    "R245_sheet_count": 264,
    "component_count": 92_688,
    "official_key_count": 124,
    "all_pair_count": 159_325_326_786,
    "within_component_pair_count": 487_242_432,
    "cross_component_pair_count": 158_838_084_354,
    "minimum_component_size": 1,
    "maximum_component_size": 10_599,
}
PAIR_CLASS_COUNTS = {
    "OCCURRENCE__OCCURRENCE": 92_969_954_028,
    "OCCURRENCE__VIRTUAL_POSITIVE_3D": 40_818_149_280,
    "OCCURRENCE__VIRTUAL_SHEET": 16_654_977_792,
    "VIRTUAL_POSITIVE_3D__VIRTUAL_POSITIVE_3D": 4_480_210_470,
    "VIRTUAL_POSITIVE_3D__VIRTUAL_SHEET": 3_656_147_840,
    "VIRTUAL_SHEET__VIRTUAL_SHEET": 745_887_376,
}

ROW_FIELDS = {
    "member": frozenset({
        ID_FIELDS["member"], "schema", "member_id", "base_root_id",
        "Round306A_component_id", "official_key_id", "identity_class",
        "identity_tranche", "pair_denominator_class",
        "physical_dimension_profile", "primary_source_package",
        "primary_source_row_id", "primary_source_row_sha256",
        "inherited_virtual_source_package", "inherited_virtual_source_row_id",
        "inherited_virtual_source_row_sha256", "member_identity_preserved",
        "geometry_feature_expansion_deferred_to_Round306B", "formal_maximality_credit",
        "formal_fibre_credit", "formal_global_disposition_credit", "row_sha256",
    }),
    "component": frozenset({
        ID_FIELDS["component"], "schema", "Round306A_component_id",
        "member_count", "occurrence_member_count", "virtual_positive_3d_member_count",
        "virtual_sheet_member_count", "official_key_count", "official_key_ids_sha256",
        "member_ids_sha256", "component_size_is_from_complete_Round306A_partition",
        "maximality_proved", "formal_maximality_credit", "formal_fibre_credit",
        "formal_global_disposition_credit", "row_sha256",
    }),
    "pair": frozenset({
        ID_FIELDS["pair"], "schema", "pair_class", "left_member_class",
        "right_member_class", "left_member_count", "right_member_count",
        "unordered_member_pair_count", "within_component_pair_count",
        "cross_component_pair_count", "pair_count_formula",
        "official_key_used_as_routing_filter", "complete_geometry_routing_performed",
        "formal_maximality_credit", "row_sha256",
    }),
    "source": frozenset({
        ID_FIELDS["source"], "schema", "source_package", "manifest_filename",
        "manifest_file_sha256", "selected_member_filename",
        "selected_member_file_sha256", "source_table_name", "source_row_count",
        "source_row_ids_sha256", "source_row_hashes_sha256", "source_rows_sha256",
        "consumption_status", "geometry_feature_expansion_status",
        "formal_maximality_credit", "row_sha256",
    }),
    "gap": frozenset({
        ID_FIELDS["gap"], "schema", "gap_class", "gap_count", "status",
        "source_identity_or_manifest_binding_gap", "geometry_feature_gap",
        "formal_maximality_credit", "required_next", "row_sha256",
    }),
}


class FreezeBlocked(RuntimeError):
    pass


def need(value: bool, label: str) -> None:
    if not value:
        raise FreezeBlocked(label)


def canonical(value: Any) -> bytes:
    return ENCODER.encode(value).encode("ascii")


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def close_row(payload: dict[str, Any]) -> dict[str, Any]:
    row = dict(payload)
    row["row_sha256"] = digest(payload)
    return row


FileIdentity = tuple[int, int, int, int, int, int, int]
INPUT_SNAPSHOTS: dict[Path, FileIdentity] = {}


def identity(info: os.stat_result) -> FileIdentity:
    return (
        info.st_dev, info.st_ino, info.st_mode, info.st_nlink,
        info.st_size, info.st_mtime_ns, info.st_ctime_ns,
    )


def exact_file(path: Path, maximum: int = 3_000_000_000) -> os.stat_result:
    need(path.parent == DATA and path.name == os.path.basename(path), "direct input path")
    need(os.path.lexists(path) and not path.is_symlink(), "input exists/no symlink:" + path.name)
    info = os.lstat(path)
    need(
        stat.S_ISREG(info.st_mode) and info.st_nlink == 1
        and 0 < info.st_size <= maximum,
        "regular single-link bounded input:" + path.name,
    )
    return info


def fd_open(path: Path, maximum: int = 3_000_000_000) -> BinaryIO:
    before = exact_file(path, maximum)
    descriptor = os.open(path, os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0))
    try:
        opened = os.fstat(descriptor)
        named = os.lstat(path)
        need(identity(before) == identity(opened) == identity(named), "fd/path binding:" + path.name)
        INPUT_SNAPSHOTS.setdefault(path, identity(before))
        return os.fdopen(descriptor, "rb", closefd=True)
    except Exception:
        os.close(descriptor)
        raise


def stable_bytes(path: Path, maximum: int = 3_000_000_000) -> bytes:
    chunks: list[bytes] = []
    total = 0
    with fd_open(path, maximum) as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            total += len(block)
            need(total <= maximum, "bounded read:" + path.name)
            chunks.append(block)
    return b"".join(chunks)


def file_sha256(path: Path, maximum: int = 3_000_000_000) -> str:
    state = hashlib.sha256()
    with fd_open(path, maximum) as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            state.update(block)
    return state.hexdigest()


def assert_inputs_unchanged() -> None:
    for path, expected in sorted(INPUT_SNAPSHOTS.items(), key=lambda item: str(item[0])):
        need(os.path.lexists(path) and not path.is_symlink(), "input disappeared:" + path.name)
        need(identity(os.lstat(path)) == expected, "input changed:" + path.name)


def strict_object(raw: bytes, label: str) -> dict[str, Any]:
    need(raw and not raw.startswith(b"\xef\xbb\xbf") and b"\x00" not in raw, "strict bytes:" + label)

    def unique(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        out: dict[str, Any] = {}
        for key, value in pairs:
            need(key not in out, "duplicate key:" + label + ":" + key)
            out[key] = value
        return out

    def reject(token: str) -> Any:
        raise FreezeBlocked("nonintegral JSON:" + label + ":" + token)

    value = json.loads(
        raw.decode("utf-8"), object_pairs_hook=unique,
        parse_float=reject, parse_constant=reject,
    )
    need(type(value) is dict, "top object:" + label)
    return value


def check_self(value: dict[str, Any], field: str, label: str) -> None:
    payload = dict(value)
    claimed = payload.pop(field, None)
    need(type(claimed) is str and claimed == digest(payload), "self hash:" + label)


def check_row(row: dict[str, Any], label: str) -> None:
    check_self(row, "row_sha256", label)


def parse_manifest(name: str, expected_sha256: str) -> dict[str, str]:
    need(PIN.fullmatch(expected_sha256) is not None, "manifest pin syntax:" + name)
    raw = stable_bytes(DATA / name, 1_000_000)
    need(hashlib.sha256(raw).hexdigest() == expected_sha256, "manifest pin:" + name)
    entries: dict[str, str] = {}
    for line in raw.decode("ascii").splitlines():
        match = re.fullmatch(r"([0-9a-f]{64})  (?:deliverables/)?([^/\s]+)", line)
        need(match is not None, "manifest line:" + name)
        value, member = match.groups()
        need(member not in entries, "manifest duplicate:" + name + ":" + member)
        entries[member] = value
    need(entries, "manifest nonempty:" + name)
    return entries


def bind_selected_packages() -> tuple[dict[str, dict[str, str]], list[dict[str, Any]]]:
    bindings: dict[str, dict[str, str]] = {}
    inventory: list[dict[str, Any]] = []
    for label, package in PACKAGES.items():
        entries = parse_manifest(package.manifest, package.manifest_sha256)
        selected: dict[str, str] = {}
        for member in package.selected_members:
            need(member in entries, "selected manifest member:" + label + ":" + member)
            expected = entries[member]
            need(file_sha256(DATA / member) == expected, "selected member pin:" + label + ":" + member)
            selected[member] = expected
            inventory.append({
                "source_package": label,
                "manifest_filename": package.manifest,
                "manifest_file_sha256": package.manifest_sha256,
                "selected_member_filename": member,
                "selected_member_file_sha256": expected,
            })
        bindings[label] = selected
    return bindings, inventory


def require_round306a_seal() -> tuple[dict[str, str], dict[str, Any]]:
    need(
        PIN.fullmatch(R306A_MANIFEST_SHA256) is not None,
        "BLOCKED_SINGLE_PIN:replace R306A_MANIFEST_SHA256 after formal Round306A seal",
    )
    entries = parse_manifest(R306A["manifest"], R306A_MANIFEST_SHA256)
    need(set(entries) == set(R306A_EXPECTED_MANIFEST_MEMBERS), "Round306A exact 13-member seal")
    for member, expected in R306A_KNOWN_MEMBER_PINS.items():
        need(entries.get(member) == expected, "Round306A known member pin:" + member)
    for member, expected in entries.items():
        need(file_sha256(DATA / member) == expected, "Round306A sealed member:" + member)
    result = strict_object(stable_bytes(DATA / R306A["result"], 2_000_000), R306A["result"])
    check_self(result, "result_sha256", "Round306A result")
    need(result["result_sha256"] == R306A_RESULT_SELF_SHA256, "Round306A result self pin")
    need(
        result["member_universe"] == {
            "member_count": 564492, "base_root_count": 367964, "official_key_count": 124,
        }
        and result["fresh_forward_application"]["component_count"] == 92688
        and result["fresh_forward_application"]["partition_sha256"] == R306A_PARTITION_SHA256
        and result["fresh_reverse_application"]["component_count"] == 92688
        and result["fresh_reverse_application"]["partition_sha256"] == R306A_PARTITION_SHA256
        and result["fresh_reverse_application"]["edge_rows"]
        == result["fresh_forward_application"]["edge_rows"] == 478718
        and result["fresh_reverse_application"]["rank_reduction"]
        == result["fresh_forward_application"]["rank_reduction"] == 275276
        and result["full_maximality_gate"]["formal_maximality_credit"] == 0
        and result["full_maximality_gate"]["full_maximality_proved"] is False,
        "Round306A exact frozen boundary",
    )
    verification = strict_object(
        stable_bytes(DATA / R306A["verification"], 3_000_000), R306A["verification"]
    )
    check_self(verification, "verification_sha256", "Round306A verification")
    need(
        verification["status"] == "PASS_EXACT_CACHELESS_ROUND306A_FRESH_LEGAL_COMPONENT_DSU_REBUILD"
        and verification["exact_fresh_DSU_census"]["fresh_component_count"] == 92688
        and verification["exact_fresh_DSU_census"]["fresh_partition_sha256"] == R306A_PARTITION_SHA256
        and verification["strict_downstream_boundary"]["full_maximality_proved"] is False,
        "Round306A verification marker",
    )
    return entries, result


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
        need(bool(block), "missing array marker:" + marker)
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
        parse_float=lambda token: (_ for _ in ()).throw(FreezeBlocked("float:" + token)),
        parse_constant=lambda token: (_ for _ in ()).throw(FreezeBlocked("constant:" + token)),
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
                row, end = decoder.raw_decode(buffer)
                break
            except json.JSONDecodeError:
                block = stream.read(1 << 20)
                need(bool(block), "truncated streamed row")
                buffer += block
        need(type(row) is dict, "stream row object")
        yield row
        buffer = buffer[end:]


def scan_table(
    name: str,
    table: str,
    id_field: str,
    visit: Callable[[dict[str, Any]], None],
    *,
    gzip_source: bool,
    expected: dict[str, Any] | None = None,
    occurrence_field: str | None = None,
) -> dict[str, Any]:
    rows, ids, hashes = ListHash(), ListHash(), ListHash()
    occurrences = ListHash() if occurrence_field is not None else None
    seen: set[str] = set()
    raw = fd_open(DATA / name)
    binary: BinaryIO
    if gzip_source:
        binary = gzip.GzipFile(fileobj=raw, mode="rb")
    else:
        binary = raw
    stream = io.TextIOWrapper(binary, encoding="utf-8", newline="")
    try:
        if gzip_source:
            iterator = iter_array(stream, '"' + table + '":[')
        else:
            outer = '"' + table + '":'
            carry = ""
            while True:
                block = stream.read(1 << 20)
                need(bool(block), "missing table:" + table)
                combined = carry + block
                if outer in combined:
                    initial = combined.split(outer, 1)[1]
                    break
                carry = combined[-len(outer):]
            iterator = iter_array(stream, '"rows":[', initial)
        for row in iterator:
            check_row(row, name + ":" + table)
            row_id = row.get(id_field)
            need(type(row_id) is str and row_id not in seen, "unique row id:" + table)
            seen.add(row_id)
            rows.add(row)
            ids.add(row_id)
            hashes.add(row["row_sha256"])
            if occurrences is not None:
                occurrences.add(row[occurrence_field])
            visit(row)
    finally:
        try:
            stream.detach()
        except Exception:
            pass
        try:
            binary.close()
        finally:
            raw.close()
    actual = {
        "row_count": rows.count,
        "row_ids_sha256": ids.finish(),
        "row_hashes_sha256": hashes.finish(),
        "rows_sha256": rows.finish(),
    }
    if occurrences is not None:
        actual["occurrence_ids_sha256"] = occurrences.finish()
    if expected is not None:
        need(actual == expected, "exact table commitment:" + name + ":" + table)
    return actual


@dataclass(frozen=True)
class SourceMeta:
    identity_class: str
    identity_tranche: str
    source_package: str
    source_row_id: str
    source_row_sha256: str
    inherited_package: str | None = None
    inherited_row_id: str | None = None
    inherited_row_sha256: str | None = None
    inherited_dimension: int | None = None


@dataclass
class ComponentAggregate:
    member_ids: ListHash = field(default_factory=ListHash)
    size: int = 0
    classes: Counter[str] = field(default_factory=Counter)
    official_keys: set[str] = field(default_factory=set)


class RowSpool:
    def __init__(self, id_field: str) -> None:
        self.id_field = id_field
        self.stream = tempfile.TemporaryFile(mode="w+b")
        self.rows = ListHash()
        self.ids = ListHash()
        self.hashes = ListHash()
        self.seen: set[str] = set()

    def add(self, payload: dict[str, Any]) -> dict[str, Any]:
        row = close_row(payload)
        row_id = row.get(self.id_field)
        need(type(row_id) is str and row_id not in self.seen, "spool unique id")
        self.seen.add(row_id)
        need(set(row) == ROW_FIELDS[self.kind], "exact generated row fields:" + self.kind)
        if self.rows.count:
            self.stream.write(b",")
        self.stream.write(canonical(row))
        self.rows.add(row)
        self.ids.add(row_id)
        self.hashes.add(row["row_sha256"])
        return row

    @property
    def kind(self) -> str:
        for key, value in ID_FIELDS.items():
            if value == self.id_field:
                return key
        raise FreezeBlocked("unknown spool id field")

    def metadata(self) -> dict[str, Any]:
        return {
            "row_count": self.rows.count,
            "row_ids_sha256": self.ids.finish(),
            "row_hashes_sha256": self.hashes.finish(),
            "rows_sha256": self.rows.finish(),
        }

    def rewind(self) -> None:
        self.stream.flush()
        self.stream.seek(0)

    def close(self) -> None:
        self.stream.close()


def ledger_metadata(kind: str, spool: RowSpool) -> dict[str, Any]:
    base = {
        "schema": SCHEMA + "." + kind + "-ledger.v1",
        "status": (
            "PASS_ZERO_CREDIT_SOURCE_FREEZE_LEDGER__"
            "GEOMETRY_ROUTING_AND_MAXIMALITY_DEFERRED"
        ),
        "formal_credit": {
            "maximality": 0, "fibre": 0, "global_disposition": 0,
        },
        **spool.metadata(),
    }
    return {**base, "ledger_sha256": digest(base)}


def emit_spooled_ledger(path: Path, kind: str, spool: RowSpool) -> dict[str, Any]:
    meta = ledger_metadata(kind, spool)
    ordered = (
        "schema", "status", "formal_credit", "row_count", "row_ids_sha256",
        "row_hashes_sha256", "rows_sha256", "ledger_sha256",
    )
    descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    try:
        with os.fdopen(descriptor, "wb", closefd=True) as raw:
            with gzip.GzipFile(filename="", mode="wb", fileobj=raw, compresslevel=9, mtime=0) as output:
                output.write(b"{")
                for index, key in enumerate(ordered):
                    if index:
                        output.write(b",")
                    output.write(canonical(key) + b":" + canonical(meta[key]))
                output.write(b"," + canonical(TABLES[kind]) + b":[")
                spool.rewind()
                for block in iter(lambda: spool.stream.read(1 << 20), b""):
                    output.write(block)
                output.write(b"]}")
            raw.flush()
            os.fsync(raw.fileno())
    except Exception:
        try:
            os.unlink(path)
        except FileNotFoundError:
            pass
        raise
    info = os.lstat(path)
    need(stat.S_ISREG(info.st_mode) and info.st_nlink == 1 and stat.S_IMODE(info.st_mode) == 0o600,
         "private ledger mode/link:" + path.name)
    return {
        **meta,
        "filename": path.name,
        "file_sha256": file_sha256_local(path),
        "file_size": info.st_size,
    }


def file_sha256_local(path: Path) -> str:
    state = hashlib.sha256()
    descriptor = os.open(path, os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0))
    try:
        before = os.fstat(descriptor)
        need(stat.S_ISREG(before.st_mode) and before.st_nlink == 1, "local regular file")
        while True:
            block = os.read(descriptor, 1 << 20)
            if not block:
                break
            state.update(block)
        after = os.fstat(descriptor)
        need(identity(before) == identity(after), "local file stable")
    finally:
        os.close(descriptor)
    return state.hexdigest()


def bind_inherited_virtual_dimensions() -> tuple[dict[str, SourceMeta], dict[str, dict[str, Any]]]:
    result: dict[str, SourceMeta] = {}
    commitments: dict[str, dict[str, Any]] = {}
    specifications = (
        (
            "R245", "cm2_round245_source_g_retained_graph_mixed_sheet_quotient_certificate.json",
            "formal_retained_stratum_node_ledger", "retained_stratum_node_id",
        ),
        (
            "R246", "cm2_round246_source_g_whole_signature_retained_quotient_certificate.json",
            "formal_new_whole_signature_retained_stratum_node_ledger", "retained_stratum_node_id",
        ),
        (
            "R247", "cm2_round247_source_g_crossing_and_source_seam_retained_quotient_certificate.json",
            "formal_new_crossing_and_source_seam_retained_stratum_node_ledger", "retained_stratum_node_id",
        ),
    )
    dimension_histogram: Counter[int] = Counter()
    package_histogram: Counter[str] = Counter()
    for package, name, table, id_field in specifications:
        def visit(row: dict[str, Any], package: str = package) -> None:
            member = row[id_field]
            dimension = row["local_dimension"]
            need(dimension in (2, 3) and member not in result, "inherited virtual dimension")
            result[member] = SourceMeta(
                identity_class="VALID_VIRTUAL_STRATUM",
                identity_tranche="INHERITED_ROUND247_VIRTUAL_STRATUM",
                source_package="R266",
                source_row_id="",
                source_row_sha256="",
                inherited_package=package,
                inherited_row_id=member,
                inherited_row_sha256=row["row_sha256"],
                inherited_dimension=dimension,
            )
            dimension_histogram[dimension] += 1
            package_histogram[package] += 1

        commitments[package] = scan_table(
            name, table, id_field, visit, gzip_source=False,
        )
    need(
        package_histogram == {"R245": 3664, "R246": 2220, "R247": 504}
        and dimension_histogram == {2: 264, 3: 6124}
        and len(result) == 6388,
        "inherited virtual exact 6388=6124+264 census",
    )
    return result, commitments


def reconstruct_source_meta(
    inherited: dict[str, SourceMeta],
) -> tuple[dict[str, SourceMeta], dict[str, dict[str, Any]]]:
    output: dict[str, SourceMeta] = {}
    commitments: dict[str, dict[str, Any]] = {}
    tranches: Counter[str] = Counter()

    def registry_visit(row: dict[str, Any]) -> None:
        occurrence = row["registry_occurrence_id"]
        tranche = row["registry_entry_kind"]
        need(occurrence not in output, "unique formal occurrence")
        output[occurrence] = SourceMeta(
            identity_class="FORMAL_OCCURRENCE",
            identity_tranche=tranche,
            source_package="R294",
            source_row_id=row["Round294_occurrence_registry_row_id"],
            source_row_sha256=row["row_sha256"],
        )
        tranches[tranche] += 1

    commitments["R294_REGISTRY"] = scan_table(
        R294_REGISTRY, "rows", "Round294_occurrence_registry_row_id",
        registry_visit, gzip_source=True, expected=R294_COMMITMENT,
        occurrence_field="registry_occurrence_id",
    )
    need(
        tranches == {
            "PRESERVED_ROUND266_EXISTING_LOCAL_OCCURRENCE": 126468,
            "CANDIDATE_NEW_ROUND288_CANONICAL_ATOM": 295336,
            "CANDIDATE_NEW_ROUND292_REFINED_R287_SUPPORT_COMPONENT": 9404,
        },
        "Round294 tranche census",
    )
    virtual_kinds: Counter[str] = Counter()

    def member_visit(row: dict[str, Any]) -> None:
        member = row["component_member_id"]
        kind = row["component_member_kind"]
        if kind == "EXPANDED_OCCURRENCE":
            need(member in output, "Round266 occurrence must be preserved in R294")
            return
        need(kind == "VALID_VIRTUAL_STRATUM" and member not in output, "Round266 virtual identity")
        tranche = row["component_member_source_kind"]
        inherited_meta = inherited.get(member)
        if tranche == "INHERITED_ROUND247_VIRTUAL_STRATUM":
            need(inherited_meta is not None, "inherited virtual source coverage")
        else:
            need(tranche in {"ROUND248_WALL_BULK", "ROUND248_WALL_SHEET"} and inherited_meta is None,
                 "Round248 virtual source coverage")
        output[member] = SourceMeta(
            identity_class="VALID_VIRTUAL_STRATUM",
            identity_tranche=tranche,
            source_package="R266",
            source_row_id=row["post_Round266_component_member_frontier_row_id"],
            source_row_sha256=row["row_sha256"],
            inherited_package=(inherited_meta.inherited_package if inherited_meta else None),
            inherited_row_id=(inherited_meta.inherited_row_id if inherited_meta else None),
            inherited_row_sha256=(inherited_meta.inherited_row_sha256 if inherited_meta else None),
            inherited_dimension=(inherited_meta.inherited_dimension if inherited_meta else None),
        )
        virtual_kinds[tranche] += 1

    commitments["R266_MEMBER_FRONTIER"] = scan_table(
        R266_CERTIFICATE, "formal_post_Round266_component_member_frontier_ledger",
        "post_Round266_component_member_frontier_row_id", member_visit,
        gzip_source=False, expected=R266_MEMBER_COMMITMENT,
    )
    need(
        virtual_kinds == {
            "INHERITED_ROUND247_VIRTUAL_STRATUM": 6388,
            "ROUND248_WALL_BULK": 88536,
            "ROUND248_WALL_SHEET": 38360,
        }
        and len(output) == 564492,
        "complete 431208+133284 source metadata",
    )
    return output, commitments


def pair_class(meta: SourceMeta) -> tuple[str, str]:
    if meta.identity_class == "FORMAL_OCCURRENCE":
        return "OCCURRENCE", "MULTI_REPRESENTATION_OCCURRENCE__GEOMETRY_NOT_YET_EXPANDED"
    if meta.identity_tranche == "ROUND248_WALL_BULK":
        return "VIRTUAL_POSITIVE_3D", "POSITIVE_3D_CARRIER"
    if meta.identity_tranche == "ROUND248_WALL_SHEET":
        return "VIRTUAL_SHEET", "HALF_OPEN_2D_SHEET"
    need(meta.identity_tranche == "INHERITED_ROUND247_VIRTUAL_STRATUM", "known virtual tranche")
    if meta.inherited_dimension == 2:
        return "VIRTUAL_SHEET", "HALF_OPEN_2D_SHEET"
    need(meta.inherited_dimension == 3, "inherited dimension 3")
    return "VIRTUAL_POSITIVE_3D", "POSITIVE_3D_CARRIER"


def build_member_and_components(
    source_meta: dict[str, SourceMeta],
) -> tuple[RowSpool, dict[str, ComponentAggregate], dict[str, int], dict[str, dict[str, Any]]]:
    spool = RowSpool(ID_FIELDS["member"])
    components: dict[str, ComponentAggregate] = defaultdict(ComponentAggregate)
    class_counts: Counter[str] = Counter()
    official_keys: set[str] = set()

    def visit(row: dict[str, Any]) -> None:
        need(
            set(row) == {
                "Round306A_fresh_member_component_row_id", "schema", "registry_occurrence_id",
                "base_root_id", "official_key_id", "final_component_id",
                "member_identity_preserved", "formal_maximality_credit",
                "formal_fibre_credit", "formal_global_disposition_credit", "row_sha256",
            }
            and row["member_identity_preserved"] is True
            and row["formal_maximality_credit"] == row["formal_fibre_credit"]
            == row["formal_global_disposition_credit"] == 0,
            "Round306A exact member row contract",
        )
        member = row["registry_occurrence_id"]
        meta = source_meta.get(member)
        need(meta is not None, "member source metadata exact coverage")
        denominator_class, dimension_profile = pair_class(meta)
        component = row["final_component_id"]
        official_key = row["official_key_id"]
        official_keys.add(official_key)
        aggregate = components[component]
        aggregate.size += 1
        aggregate.classes[denominator_class] += 1
        aggregate.official_keys.add(official_key)
        aggregate.member_ids.add(member)
        class_counts[denominator_class] += 1
        spool.add({
            ID_FIELDS["member"]: "round306b0-member-source:" + digest(member),
            "schema": SCHEMA + ".member-support-source-row.v1",
            "member_id": member,
            "base_root_id": row["base_root_id"],
            "Round306A_component_id": component,
            "official_key_id": official_key,
            "identity_class": meta.identity_class,
            "identity_tranche": meta.identity_tranche,
            "pair_denominator_class": denominator_class,
            "physical_dimension_profile": dimension_profile,
            "primary_source_package": meta.source_package,
            "primary_source_row_id": meta.source_row_id,
            "primary_source_row_sha256": meta.source_row_sha256,
            "inherited_virtual_source_package": meta.inherited_package,
            "inherited_virtual_source_row_id": meta.inherited_row_id,
            "inherited_virtual_source_row_sha256": meta.inherited_row_sha256,
            "member_identity_preserved": True,
            "geometry_feature_expansion_deferred_to_Round306B": True,
            "formal_maximality_credit": 0,
            "formal_fibre_credit": 0,
            "formal_global_disposition_credit": 0,
        })

    commitment = scan_table(
        R306A["member"], "fresh_member_component_rows",
        "Round306A_fresh_member_component_row_id", visit,
        gzip_source=True, expected=R306A_MEMBER_COMMITMENT,
    )
    need(
        class_counts == {
            "OCCURRENCE": 431208, "VIRTUAL_POSITIVE_3D": 94660, "VIRTUAL_SHEET": 38624,
        }
        and len(components) == 92688 and len(official_keys) == 124,
        "complete current member classification",
    )
    return spool, components, dict(class_counts), {"R306A_MEMBER": commitment}


def build_component_spool(
    components: dict[str, ComponentAggregate],
) -> tuple[RowSpool, dict[str, Any], dict[str, dict[str, int]]]:
    spool = RowSpool(ID_FIELDS["component"])
    size_histogram: Counter[int] = Counter()
    within_total = 0
    within_by_pair_class: Counter[str] = Counter()
    minimum = None
    maximum = 0
    for component_id in sorted(components):
        aggregate = components[component_id]
        n_o = aggregate.classes["OCCURRENCE"]
        n_v = aggregate.classes["VIRTUAL_POSITIVE_3D"]
        n_s = aggregate.classes["VIRTUAL_SHEET"]
        need(n_o + n_v + n_s == aggregate.size, "component member class conservation")
        within_total += aggregate.size * (aggregate.size - 1) // 2
        size_histogram[aggregate.size] += 1
        minimum = aggregate.size if minimum is None else min(minimum, aggregate.size)
        maximum = max(maximum, aggregate.size)
        within_by_pair_class["OCCURRENCE__OCCURRENCE"] += n_o * (n_o - 1) // 2
        within_by_pair_class["OCCURRENCE__VIRTUAL_POSITIVE_3D"] += n_o * n_v
        within_by_pair_class["OCCURRENCE__VIRTUAL_SHEET"] += n_o * n_s
        within_by_pair_class["VIRTUAL_POSITIVE_3D__VIRTUAL_POSITIVE_3D"] += n_v * (n_v - 1) // 2
        within_by_pair_class["VIRTUAL_POSITIVE_3D__VIRTUAL_SHEET"] += n_v * n_s
        within_by_pair_class["VIRTUAL_SHEET__VIRTUAL_SHEET"] += n_s * (n_s - 1) // 2
        keys = sorted(aggregate.official_keys)
        spool.add({
            ID_FIELDS["component"]: "round306b0-component-census:" + digest(component_id),
            "schema": SCHEMA + ".component-census-row.v1",
            "Round306A_component_id": component_id,
            "member_count": aggregate.size,
            "occurrence_member_count": n_o,
            "virtual_positive_3d_member_count": n_v,
            "virtual_sheet_member_count": n_s,
            "official_key_count": len(keys),
            "official_key_ids_sha256": digest(keys),
            "member_ids_sha256": aggregate.member_ids.finish(),
            "component_size_is_from_complete_Round306A_partition": True,
            "maximality_proved": False,
            "formal_maximality_credit": 0,
            "formal_fibre_credit": 0,
            "formal_global_disposition_credit": 0,
        })
    need(
        spool.rows.count == EXPECTED["component_count"]
        and within_total == EXPECTED["within_component_pair_count"]
        and minimum == EXPECTED["minimum_component_size"]
        and maximum == EXPECTED["maximum_component_size"],
        "Round306A component-size denominator census",
    )
    audit = {
        "component_count": spool.rows.count,
        "within_component_pair_count": within_total,
        "cross_component_pair_count": EXPECTED["all_pair_count"] - within_total,
        "minimum_component_size": minimum,
        "maximum_component_size": maximum,
        "component_size_histogram": {
            str(size): count for size, count in sorted(size_histogram.items())
        },
        "component_size_histogram_sha256": digest([
            [size, count] for size, count in sorted(size_histogram.items())
        ]),
    }
    need(audit["cross_component_pair_count"] == EXPECTED["cross_component_pair_count"],
         "exact cross-component denominator")
    per_class = {
        pair_name: {
            "within": within_by_pair_class[pair_name],
            "cross": total - within_by_pair_class[pair_name],
        }
        for pair_name, total in PAIR_CLASS_COUNTS.items()
    }
    need(
        sum(item["within"] for item in per_class.values()) == within_total
        and sum(item["cross"] for item in per_class.values())
        == EXPECTED["cross_component_pair_count"],
        "pair-class within/cross conservation",
    )
    return spool, audit, per_class


def build_pair_spool(
    class_counts: dict[str, int],
    per_class: dict[str, dict[str, int]],
) -> RowSpool:
    spool = RowSpool(ID_FIELDS["pair"])
    for pair_name, total in PAIR_CLASS_COUNTS.items():
        left, right = pair_name.split("__", 1)
        same = left == right
        left_count = class_counts[left]
        right_count = class_counts[right]
        formula = "C(n,2)" if same else "n_left*n_right"
        independently_computed = (
            left_count * (left_count - 1) // 2 if same else left_count * right_count
        )
        need(independently_computed == total, "pair-class arithmetic:" + pair_name)
        spool.add({
            ID_FIELDS["pair"]: "round306b0-pair-denominator:" + digest(pair_name),
            "schema": SCHEMA + ".pair-denominator-row.v1",
            "pair_class": pair_name,
            "left_member_class": left,
            "right_member_class": right,
            "left_member_count": left_count,
            "right_member_count": right_count,
            "unordered_member_pair_count": total,
            "within_component_pair_count": per_class[pair_name]["within"],
            "cross_component_pair_count": per_class[pair_name]["cross"],
            "pair_count_formula": formula,
            "official_key_used_as_routing_filter": False,
            "complete_geometry_routing_performed": False,
            "formal_maximality_credit": 0,
        })
    need(
        spool.rows.count == 6
        and sum(PAIR_CLASS_COUNTS.values()) == EXPECTED["all_pair_count"],
        "six-class all-pair partition",
    )
    return spool


def build_source_spool(
    manifest_inventory: list[dict[str, Any]],
    table_commitments: dict[str, dict[str, Any]],
) -> RowSpool:
    scanned = {
        "R245": ("formal_retained_stratum_node_ledger", table_commitments["R245"]),
        "R246": ("formal_new_whole_signature_retained_stratum_node_ledger", table_commitments["R246"]),
        "R247": ("formal_new_crossing_and_source_seam_retained_stratum_node_ledger", table_commitments["R247"]),
        "R266": ("formal_post_Round266_component_member_frontier_ledger", table_commitments["R266_MEMBER_FRONTIER"]),
        "R294": ("rows", table_commitments["R294_REGISTRY"]),
        "R306A": ("fresh_member_component_rows", table_commitments["R306A_MEMBER"]),
    }
    rows = list(manifest_inventory)
    rows.append({
        "source_package": "R306A",
        "manifest_filename": R306A["manifest"],
        "manifest_file_sha256": R306A_MANIFEST_SHA256,
        "selected_member_filename": R306A["member"],
        "selected_member_file_sha256": R306A_KNOWN_MEMBER_PINS[R306A["member"]],
    })
    spool = RowSpool(ID_FIELDS["source"])
    for index, item in enumerate(sorted(
        rows, key=lambda row: (row["source_package"], row["selected_member_filename"])
    )):
        table_name = None
        commitment = None
        if item["source_package"] in scanned:
            candidate_name, candidate_commitment = scanned[item["source_package"]]
            # R294 has two selected members; only the registry is scanned here.
            if (
                item["source_package"] != "R294"
                or item["selected_member_filename"] == R294_REGISTRY
            ):
                table_name, commitment = candidate_name, candidate_commitment
        if commitment is None:
            count = None
            row_ids = None
            row_hashes = None
            rows_hash = None
            status = "MANIFEST_BOUND__FEATURE_TABLE_EXPANSION_DEFERRED_TO_ROUND306B"
        else:
            count = commitment["row_count"]
            row_ids = commitment["row_ids_sha256"]
            row_hashes = commitment["row_hashes_sha256"]
            rows_hash = commitment["rows_sha256"]
            status = "MANIFEST_AND_SELECTED_TABLE_STREAM_RECOMMITTED"
        spool.add({
            ID_FIELDS["source"]: "round306b0-source-inventory:" + digest([
                item["source_package"], item["selected_member_filename"], index,
            ]),
            "schema": SCHEMA + ".source-table-inventory-row.v1",
            **item,
            "source_table_name": table_name,
            "source_row_count": count,
            "source_row_ids_sha256": row_ids,
            "source_row_hashes_sha256": row_hashes,
            "source_rows_sha256": rows_hash,
            "consumption_status": status,
            "geometry_feature_expansion_status": "DEFERRED_WITH_ZERO_CREDIT",
            "formal_maximality_credit": 0,
        })
    return spool


def build_gap_spool() -> RowSpool:
    # The empty row set certifies only zero *binding* gaps.  Geometry feature
    # coverage is expressly not represented by an empty gap ledger here.
    return RowSpool(ID_FIELDS["gap"])


def result_payload(
    producer_sha256: str,
    output_meta: dict[str, dict[str, Any]],
    component_audit: dict[str, Any],
    class_counts: dict[str, int],
    source_manifest_count: int,
) -> dict[str, Any]:
    payload = {
        "schema": SCHEMA,
        "status": (
            "PASS_ROUND306B0_CURRENT_UNIVERSE_AND_PAIR_DENOMINATOR_FREEZE__"
            "CREDIT_REQUIRES_INDEPENDENT_VERIFICATION_MARKER__"
            "ZERO_MAXIMALITY_FIBRE_AND_GLOBAL_CREDIT"
        ),
        "producer_file_sha256": producer_sha256,
        "sealed_Round306A": {
            "manifest_filename": R306A["manifest"],
            "manifest_file_sha256": R306A_MANIFEST_SHA256,
            "member_ledger_file_sha256": R306A_KNOWN_MEMBER_PINS[R306A["member"]],
            "result_file_sha256": R306A_KNOWN_MEMBER_PINS[R306A["result"]],
            "result_self_sha256": R306A_RESULT_SELF_SHA256,
            "verification_is_formal_credit_marker": True,
            "component_count": 92688,
            "partition_sha256": R306A_PARTITION_SHA256,
            "Round300A_zero_residual_is_not_full_maximality": True,
        },
        "member_universe": {
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
        },
        "component_denominator_audit": component_audit,
        "six_pair_class_totals": dict(sorted(PAIR_CLASS_COUNTS.items())),
        "source_binding": {
            "selected_sealed_manifest_count": source_manifest_count,
            "all_selected_source_files_byte_pinned": True,
            "all_consumed_large_tables_stream_recommitted": True,
            "official_key_count": 124,
            "stale_116_key_scope_rejected": True,
            "official_key_used_as_pair_routing_filter": False,
            "cross_official_key_physical_adjacency_permitted": True,
        },
        "coverage_boundary": {
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
        },
        "formal_credit_without_independent_verification_marker": {
            "member_universe_freeze": 0,
            "pair_denominator_freeze": 0,
            "maximality": 0,
            "fibre": 0,
            "global_disposition": 0,
            "D02": "BLOCKED",
            "CM2": "NO-GO_FOR_CLAIM",
        },
        "candidate_credit_if_independently_verified": {
            "member_universe_freeze": 1,
            "pair_denominator_freeze": 1,
            "maximality": 0,
            "fibre": 0,
            "global_disposition": 0,
            "D02": "BLOCKED",
            "CM2": "NO-GO_FOR_CLAIM",
        },
        "output_ledgers": output_meta,
        "candidate_is_formal_without_independent_verification_marker": False,
    }
    return {**payload, "result_sha256": digest(payload)}


def exclusive_bytes(path: Path, raw: bytes) -> None:
    descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    try:
        offset = 0
        while offset < len(raw):
            offset += os.write(descriptor, raw[offset:])
        os.fsync(descriptor)
        info = os.fstat(descriptor)
        need(stat.S_ISREG(info.st_mode) and info.st_nlink == 1 and info.st_size == len(raw),
             "private exact write")
    finally:
        os.close(descriptor)


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


def ensure_private_root() -> tuple[Path, int]:
    if not os.path.lexists(PRIVATE_ROOT):
        os.mkdir(PRIVATE_ROOT, 0o700)
    need(not PRIVATE_ROOT.is_symlink(), "private root no symlink")
    info = os.lstat(PRIVATE_ROOT)
    need(stat.S_ISDIR(info.st_mode) and stat.S_IMODE(info.st_mode) == 0o700,
         "private root exact mode")
    descriptor = os.open(
        PRIVATE_ROOT,
        os.O_RDONLY | getattr(os, "O_DIRECTORY", 0) | getattr(os, "O_NOFOLLOW", 0),
    )
    return PRIVATE_ROOT, descriptor


def create_private_stage(candidate: Path) -> tuple[Path, int, int]:
    root, root_fd = ensure_private_root()
    absolute = Path(os.path.abspath(os.fspath(candidate)))
    need(absolute.parent == root and absolute.name not in {"", ".", ".."},
         "candidate must be one direct child of dedicated private root")
    need(not os.path.lexists(absolute), "candidate target must be absent")
    stage_name = "." + absolute.name + ".stage." + digest([os.getpid(), absolute.name])[:24]
    os.mkdir(stage_name, 0o700, dir_fd=root_fd)
    stage_fd = os.open(
        stage_name,
        os.O_RDONLY | getattr(os, "O_DIRECTORY", 0) | getattr(os, "O_NOFOLLOW", 0),
        dir_fd=root_fd,
    )
    return root / stage_name, root_fd, stage_fd


def build_private_candidate(candidate: Path) -> dict[str, Any]:
    round306a_entries, _round306a_result = require_round306a_seal()
    _bindings, manifest_inventory = bind_selected_packages()
    inherited, inherited_commitments = bind_inherited_virtual_dimensions()
    source_meta, source_commitments = reconstruct_source_meta(inherited)
    member_spool, components, class_counts, member_commitment = build_member_and_components(source_meta)
    del source_meta, inherited
    component_spool, component_audit, per_class = build_component_spool(components)
    del components
    pair_spool = build_pair_spool(class_counts, per_class)
    source_spool = build_source_spool(
        manifest_inventory,
        {**inherited_commitments, **source_commitments, **member_commitment},
    )
    gap_spool = build_gap_spool()
    stage, root_fd, stage_fd = create_private_stage(candidate)
    spools = {
        "member": member_spool, "component": component_spool, "pair": pair_spool,
        "source": source_spool, "gap": gap_spool,
    }
    try:
        output_meta: dict[str, dict[str, Any]] = {}
        for kind in ("member", "component", "pair", "source", "gap"):
            output_meta[kind] = emit_spooled_ledger(stage / FILES[kind], kind, spools[kind])
            os.fsync(stage_fd)
        producer_sha256 = file_sha256(DATA / (PREFIX + ".py"), 2_000_000)
        result = result_payload(
            producer_sha256, output_meta, component_audit, class_counts,
            len(PACKAGES) + 1,
        )
        result_raw = canonical(result)
        exclusive_bytes(stage / FILES["result"], result_raw)
        output_meta["result"] = {
            "filename": FILES["result"],
            "file_sha256": hashlib.sha256(result_raw).hexdigest(),
            "file_size": len(result_raw),
            "result_sha256": result["result_sha256"],
        }
        os.fsync(stage_fd)
        need(set(os.listdir(stage_fd)) == set(CANDIDATE_ORDER), "exact private candidate set")
        assert_inputs_unchanged()
        target_name = Path(candidate).name
        rename_noreplace(root_fd, stage.name, root_fd, target_name)
        os.fsync(root_fd)
        return {
            "status": "PASS_ROUND306B0_PRIVATE_ZERO_CREDIT_CANDIDATE_WRITTEN",
            "candidate_directory": str(PRIVATE_ROOT / target_name),
            "Round306A_manifest_sha256": R306A_MANIFEST_SHA256,
            "Round306A_manifest_member_count": len(round306a_entries),
            "output_file_sha256s": {
                item["filename"]: item["file_sha256"] for item in output_meta.values()
            },
            "result_sha256": result["result_sha256"],
            "formal_maximality_credit": 0,
            "formal_artifact_written": False,
        }
    finally:
        for spool in spools.values():
            spool.close()
        os.close(stage_fd)
        os.close(root_fd)


def contract() -> dict[str, Any]:
    ready = PIN.fullmatch(R306A_MANIFEST_SHA256) is not None
    return {
        "schema": SCHEMA + ".contract.v1",
        "status": (
            "READY_FOR_PRIVATE_RECONSTRUCTION" if ready
            else "BLOCKED_SINGLE_UPSTREAM_PIN__NO_LARGE_INPUT_OPENED"
        ),
        "single_missing_upstream_finalization": {
            "constant": "R306A_MANIFEST_SHA256",
            "required_artifact": R306A["manifest"],
            "required_value_format": "64 lowercase hexadecimal SHA-256",
            "currently_finalized": ready,
        },
        "expected_Round306A_partition_sha256": R306A_PARTITION_SHA256,
        "expected_member_count": EXPECTED["member_count"],
        "expected_component_count": EXPECTED["component_count"],
        "expected_all_pair_count": EXPECTED["all_pair_count"],
        "expected_cross_component_pair_count": EXPECTED["cross_component_pair_count"],
        "expected_candidate_files": list(CANDIDATE_ORDER),
        "dedicated_private_candidate_root": PRIVATE_ROOT.name,
        "formal_maximality_credit": 0,
        "formal_fibre_credit": 0,
        "formal_global_disposition_credit": 0,
        "producer_imports_or_executes_Round306A_producer": False,
    }


def self_test() -> dict[str, Any]:
    sample = close_row({"schema": "self-test", "value": 1})
    check_row(sample, "self-test")
    need(
        sum(PAIR_CLASS_COUNTS.values()) == EXPECTED["all_pair_count"]
        and EXPECTED["within_component_pair_count"]
        + EXPECTED["cross_component_pair_count"] == EXPECTED["all_pair_count"]
        and 431208 + 94660 + 38624 == 564492
        and 38360 + 264 == 38624,
        "self-test arithmetic",
    )
    manifest_pin_checks = {
        label: hashlib.sha256(stable_bytes(DATA / package.manifest, 1_000_000)).hexdigest()
        == package.manifest_sha256
        for label, package in PACKAGES.items()
    }
    need(all(manifest_pin_checks.values()), "lightweight source manifest pins")
    result_probe = result_payload(
        "0" * 64, {}, {},
        {"OCCURRENCE": 431208, "VIRTUAL_POSITIVE_3D": 94660, "VIRTUAL_SHEET": 38624},
        len(PACKAGES) + 1,
    )
    zero_credit = {
        "member_universe_freeze": 0,
        "pair_denominator_freeze": 0,
        "maximality": 0,
        "fibre": 0,
        "global_disposition": 0,
        "D02": "BLOCKED",
        "CM2": "NO-GO_FOR_CLAIM",
    }
    conditional_credit = {
        **zero_credit,
        "member_universe_freeze": 1,
        "pair_denominator_freeze": 1,
    }
    need(
        result_probe["formal_credit_without_independent_verification_marker"]
        == zero_credit
        and result_probe["candidate_credit_if_independently_verified"]
        == conditional_credit
        and "CREDIT_REQUIRES_INDEPENDENT_VERIFICATION_MARKER"
        in result_probe["status"],
        "candidate/formal credit transition boundary",
    )
    return {
        "status": "PASS_ROUND306B0_LIGHTWEIGHT_SCAFFOLD_SELF_TEST",
        "large_source_or_candidate_opened": False,
        "formal_artifact_written": False,
        "source_manifest_pin_checks": manifest_pin_checks,
        "pair_arithmetic_checks": True,
        "candidate_credit_boundary_checks": True,
        "single_missing_upstream_finalization": contract()["single_missing_upstream_finalization"],
        "formal_maximality_credit": 0,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--print-contract", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--candidate-dir", type=Path)
    args = parser.parse_args()
    need(sum((args.print_contract, args.self_test, args.candidate_dir is not None)) == 1,
         "choose exactly one explicit mode")
    if args.print_contract:
        print(canonical(contract()).decode("ascii"))
        return
    if args.self_test:
        print(canonical(self_test()).decode("ascii"))
        return
    assert args.candidate_dir is not None
    print(canonical(build_private_candidate(args.candidate_dir)).decode("ascii"))


if __name__ == "__main__":
    main()
