#!/usr/bin/env python3
"""Independent, fail-closed verifier for the candidate-only C30d lane.

The C30d producer is pinned as provenance but is never imported or executed.
The twenty origins are selected again from sealed Round184/Round215 objects;
their 1,176 remaining multi-Delta cells are reconstructed through a pinned
C30a *independent verifier*, while formal ledger authority is accepted only
from an independently captured C30c root, verification, and exact six-file
78-state seal.  For every reconstructed cell this verifier proves the
exhaustive G/G/W first-target mismatch directly, including Delta zero and
target ties.  It separately materializes every origin's complete
3D/2D/1D/0D half-open ownership complex without calling the producer owner
code or the legacy R215 summary helper.  A pass remains candidate-only: all
formal credit is zero and no C30d manifest is authorized.
"""
from __future__ import annotations

import argparse
import gzip
import hashlib
import importlib.util
import itertools
import json
import os
import stat
import sys
from collections import Counter, defaultdict
from dataclasses import dataclass
from fractions import Fraction as Q
from pathlib import Path
from types import MappingProxyType
from typing import Any

sys.dont_write_bytecode = True

ROOT = Path(__file__).resolve().parent
PREFIX = "cm2_round306c30d_source_w_multi_delta_whole_origin_exclusion"
CELL_LEDGER = PREFIX + "_multi_delta_cell_ledger.jsonl.gz"
ATOMIC_OWNER_LEDGER = PREFIX + "_atomic_half_open_owner_ledger.jsonl.gz"
ORIGIN_LEDGER = PREFIX + "_whole_origin_ledger.jsonl.gz"
RESULT = PREFIX + "_result.json"
RUNTIME_ATTESTATION = "cm2_round306c30b_python_flint_runtime_attestation.json"
RUNTIME_ATTESTATION_SHA256 = (
    "6b48cd0ca3fd53f9fdd457cc3c1106055e12db4d4ad999fcfd1fc89ad36b95df"
)
PRODUCER = PREFIX + "_producer.py"
PRODUCER_SHA256 = (
    "93ab9aed0afb93fb88c298bc87c0a5b7edd26a4e7561d6edec18ae2641175dce"
)

C30C_PREFIX = "cm2_round306c30c_source_w_full_delta_whole_origin_disposition"
C30C_ROOT_MANIFEST = C30C_PREFIX + "_manifest.sha256"
C30C_PAYLOAD_MANIFEST = C30C_PREFIX + "_payload_manifest.sha256"
C30C_VERIFICATION = C30C_PREFIX + "_verification.json"
C30C_SEALED = Path("cm2_round306c30c_sealed")
C30C_ROOT_MANIFEST_SHA256: str | None = None
C30C_VERIFICATION_SHA256: str | None = None
C30C_SEALED_MEMBER_SHA256: dict[str, str] | None = None
C30C_RESULT_OBJECT_SHA256 = (
    "df4531942e743389f5e8f85b2d013132f0808f562c21f430e7904577d67087d4"
)
C30C_SEALED_MEMBERS = tuple(sorted((
    RUNTIME_ATTESTATION,
    C30C_PREFIX + "_combined_boundary_atomic_owner_join_ledger.jsonl.gz",
    C30C_PREFIX + "_delta_h_cell_ledger.jsonl.gz",
    C30C_PREFIX + "_inherited_h_cell_ledger.jsonl.gz",
    C30C_PREFIX + "_result.json",
    C30C_PREFIX + "_whole_origin_ledger.jsonl.gz",
)))
HASH_SEED_SENTINEL = "CM2_C30D_HASH_SEED_SENTINEL_v1"
HASH_FINGERPRINTS = {
    "30630071": 1743314986988020519,
    "30630929": 3335165125009301667,
}

C30A_PREFIX = (
    "cm2_round306c30a_source_w_162_reduced_clipped_delta_"
    "whole_origin_promotion"
)
C30A_VERIFIER = C30A_PREFIX + "_independent_verifier.py"
C30A_VERIFIER_SHA256 = (
    "5af75a97e9c306cc47a514e4c87ae875a8388bb75d9274d106b64e2ceee87c7c"
)
C30A_PRODUCER = C30A_PREFIX + "_producer.py"
C30A_PRODUCER_SHA256 = (
    "41a3f11c3e44bdbbfcf95edf88902669365186e6fb6394aaee15a6846dc91714"
)
C30A_MANIFEST = C30A_PREFIX + "_manifest.sha256"
C30A_MANIFEST_SHA256 = (
    "0f3e80d54d4307eccf509435470213e19fd4eefffc43b95e01cec0d3b8a094bc"
)
C30A_SEALED = Path("cm2_round306c30a_sealed")
C30A_RESULT = C30A_SEALED / (C30A_PREFIX + "_result.json")
C30A_RESULT_SHA256 = (
    "521be2aefebea96d6a3d2ce1bcf0234753ef69af7182a4e47a0d22d686df6c48"
)
C30A_RESULT_OBJECT_SHA256 = (
    "32c449bc9af41a22ab5468d194431d14fadf5bc95b30067d639f9e4443538e09"
)
C30A_CELL_LEDGER = C30A_SEALED / (C30A_PREFIX + "_cell_ledger.jsonl.gz")
C30A_CELL_LEDGER_SHA256 = (
    "c4c0061a08983471428b2e5113aff60bbeccc67530cac691658a6bbad1ce9904"
)
C30B_PRODUCER = (
    "cm2_round306c30b_source_w_outgoing_h_whole_origin_disposition_producer.py"
)
C30C_PRODUCER = C30C_PREFIX + "_producer.py"

R184_CERTIFICATE = (
    "cm2_round184_source_w_upper_candidate_priority_and_clipped_delta_"
    "certificate.json"
)
R184_CERTIFICATE_SHA256 = (
    "292d80567378b2e028e0e90612b5025533f11fd23a35067fb813dfa57e76e17f"
)
R184_RESULT_SHA256 = (
    "70026cc9e52cfe0adee0be2ff8daf0f4519a2f1947338e902399461039b82dbe"
)
R215_CERTIFICATE = (
    "cm2_round215_source_w_mixed_algebraic_formal_promotion_certificate.json"
)
R215_CERTIFICATE_SHA256 = (
    "9ad5321f5b29111aabe9f044ee22220c83d8c76ace45383ed34a0255a485a3ec"
)
R215_RESULT_SHA256 = (
    "39d38cda12566e25b341b861e0e1ee379138aa465424254a6b60ea35da5629ee"
)
R215_BOUNDED_RESULT_SHA256 = (
    "e6af59b19440723c4770a286d6261d950fb2a22702ec8900d285b43a06d0158c"
)

DIRECT_INPUT_PINS = {
    C30A_PRODUCER: C30A_PRODUCER_SHA256,
    C30A_MANIFEST: C30A_MANIFEST_SHA256,
    os.fspath(C30A_RESULT): C30A_RESULT_SHA256,
    os.fspath(C30A_CELL_LEDGER): C30A_CELL_LEDGER_SHA256,
    R184_CERTIFICATE: R184_CERTIFICATE_SHA256,
    R215_CERTIFICATE: R215_CERTIFICATE_SHA256,
    RUNTIME_ATTESTATION: RUNTIME_ATTESTATION_SHA256,
}

EXPECTED_ORIGINS = 20
EXPECTED_ORIGIN_KEYS_SHA256 = (
    "4b9d22a6c363960f67d4da851f5a77e487ee240f427bc9bd9016ced24c1b88e4"
)
EXPECTED_FINAL_CELLS = 3_152
EXPECTED_MULTI_CELLS = 1_176
EXPECTED_C30A_CLIPPED_CELLS = 1_976
EXPECTED_C30A_CLIPPED_DISPOSITION = Counter({
    "CLOSED_REDUCED_CANDIDATE_OWNER_MISMATCH": 1_440,
    "CLOSED_REDUCED_FROZEN_OWNER_OUTGOING_MISMATCH": 536,
})
EXPECTED_C30A_CLIPPED_TARGET = Counter({
    "G[1,0]": 720,
    "G[1,1]": 720,
    "W[1,0]": 536,
})
EXPECTED_C30A_CELL_KEYS_SHA256 = (
    "268791f9243241847deee9a28f5da83772ab5b0b6ab6a23212fc7246aacb7b03"
)
EXPECTED_PRIOR_CLOSED = 282
EXPECTED_PRECLOSED_FRONTIER = 68
EXPECTED_RESIDUAL_ROOTS = 360
EXPECTED_INHERITED_TERMINALS = 1_014

SEALED_BASELINE = {
    "excluded": 74_746,
    "conservative_live": 2_086,
    "remaining": 78,
    "resolved_nonexcluded": 2_008,
    "total": 76_832,
}
C30A_EVIDENCE_BOUNDARY = {
    "excluded": 74_744,
    "conservative_live": 2_088,
    "remaining": 92,
    "resolved_nonexcluded": 1_996,
    "total": 76_832,
}


class Reject(RuntimeError):
    pass


def require(condition: bool, label: str) -> None:
    if type(condition) is not bool or not condition:
        raise Reject(label)


def bootstrap_hash(path: Path) -> str:
    state = hashlib.sha256()
    with path.open("rb") as stream:
        while block := stream.read(1 << 20):
            state.update(block)
    return state.hexdigest()


def producer_module_absent() -> bool:
    forbidden_files = (PRODUCER, C30A_PRODUCER, C30B_PRODUCER, C30C_PRODUCER)
    forbidden = {filename[:-3] for filename in forbidden_files}
    forbidden_paths = {(ROOT / filename).resolve() for filename in forbidden_files}
    for name, module in tuple(sys.modules.items()):
        if name in forbidden or any(
            name.endswith("." + item) for item in forbidden
        ):
            return False
        filename = getattr(module, "__file__", None)
        if filename is not None:
            try:
                if Path(filename).resolve() in forbidden_paths:
                    return False
            except (OSError, TypeError, ValueError):
                return False
    return True


def import_pinned_c30a_verifier() -> Any:
    path = ROOT / C30A_VERIFIER
    status = path.lstat()
    require(
        stat.S_ISREG(status.st_mode)
        and not path.is_symlink()
        and status.st_nlink == 1
        and bootstrap_hash(path) == C30A_VERIFIER_SHA256,
        "pinned C30a independent verifier source",
    )
    require(
        bootstrap_hash(ROOT / PRODUCER) == PRODUCER_SHA256,
        "pinned C30d producer provenance",
    )
    require(producer_module_absent(), "no producer preloaded")
    module_name = "_cm2_c30d_pinned_c30a_independent_verifier"
    require(module_name not in sys.modules, "C30a verifier not preloaded")
    specification = importlib.util.spec_from_file_location(module_name, path)
    require(
        specification is not None and specification.loader is not None,
        "C30a verifier import specification",
    )
    module = importlib.util.module_from_spec(specification)
    sys.modules[module_name] = module
    try:
        specification.loader.exec_module(module)
    except BaseException:
        sys.modules.pop(module_name, None)
        raise
    require(
        Path(module.__file__).resolve(strict=True) == path.resolve(strict=True)
        and bootstrap_hash(path) == C30A_VERIFIER_SHA256
        and producer_module_absent(),
        "imported C30a verifier identity and producer independence",
    )
    return module


base = import_pinned_c30a_verifier()
wire = base.wire
digest = base.digest
file_hash = base.file_hash
regular_bytes = base.regular_bytes
strict_json = base.strict_json
strict_object_bytes = base.strict_object_bytes
candidate_rows = base.candidate_rows
r176 = base.r176
r180 = base.r180
r215 = base.r215
arb = base.arb
ctx = base.ctx


def sealed(body: dict[str, Any]) -> dict[str, Any]:
    return {**body, "row_sha256": digest(body)}


def verifier_manifest_rows(raw: bytes, label: str) -> dict[str, str]:
    rows: dict[str, str] = {}
    try:
        lines = raw.decode("ascii").splitlines()
    except UnicodeDecodeError as error:
        raise Reject("manifest ASCII:" + label) from error
    for line in lines:
        fields = line.split("  ", 1)
        require(
            len(fields) == 2
            and len(fields[0]) == 64
            and all(character in "0123456789abcdef" for character in fields[0]),
            "manifest syntax:" + label,
        )
        relative = Path(fields[1])
        require(
            fields[1]
            and fields[1] not in rows
            and not relative.is_absolute()
            and ".." not in relative.parts,
            "manifest relative path:" + label,
        )
        rows[fields[1]] = fields[0]
    return rows


def verifier_identity(status: os.stat_result) -> tuple[int, ...]:
    return (
        status.st_dev, status.st_ino, status.st_mode, status.st_nlink,
        status.st_size, status.st_mtime_ns, status.st_ctime_ns,
    )


def verifier_capture_authority_file(
    path: Path, maximum: int
) -> tuple[bytes, tuple[int, ...]]:
    """Verifier-local file capture; deliberately not shared with producer."""
    path_before = path.lstat()
    require(
        stat.S_ISREG(path_before.st_mode)
        and not path.is_symlink()
        and path_before.st_nlink == 1
        and 0 < path_before.st_size <= maximum,
        "C30c authority singleton:" + path.name,
    )
    descriptor = os.open(
        path, os.O_RDONLY | os.O_CLOEXEC | getattr(os, "O_NOFOLLOW", 0)
    )
    try:
        fd_before = os.fstat(descriptor)
        require(verifier_identity(fd_before) == verifier_identity(path_before),
                "C30c authority file open identity:" + path.name)
        data = bytearray()
        while True:
            chunk = os.read(descriptor, 1 << 20)
            if not chunk:
                break
            data.extend(chunk)
        fd_after = os.fstat(descriptor)
    finally:
        os.close(descriptor)
    path_after = path.lstat()
    identity = verifier_identity(fd_before)
    raw = bytes(data)
    require(
        identity == verifier_identity(fd_after) == verifier_identity(path_after)
        and len(raw) == fd_before.st_size,
        "C30c authority file changed during capture:" + path.name,
    )
    return raw, identity


def verifier_capture_c30c_authority() -> dict[str, Any]:
    """Verifier-only C30c authority capture; no C30d/C30c producer code."""
    require(
        C30C_ROOT_MANIFEST_SHA256 is not None
        and C30C_VERIFICATION_SHA256 is not None
        and C30C_SEALED_MEMBER_SHA256 is not None,
        "C30C_78_STATE_AUTHORITY_PINS_UNSET",
    )
    assert C30C_ROOT_MANIFEST_SHA256 is not None
    assert C30C_VERIFICATION_SHA256 is not None
    expected_members = C30C_SEALED_MEMBER_SHA256
    assert expected_members is not None
    require(
        set(expected_members) == set(C30C_SEALED_MEMBERS)
        and all(
            type(value) is str
            and len(value) == 64
            and all(character in "0123456789abcdef" for character in value)
            for value in expected_members.values()
        ),
        "C30c exact six externally pinned members",
    )
    root_path = ROOT / C30C_ROOT_MANIFEST
    payload_path = ROOT / C30C_PAYLOAD_MANIFEST
    verification_path = ROOT / C30C_VERIFICATION
    root_raw, root_identity = verifier_capture_authority_file(
        root_path, 64 * 1024
    )
    payload_raw, payload_identity = verifier_capture_authority_file(
        payload_path, 4 * 1024 * 1024
    )
    verification_raw, verification_identity = verifier_capture_authority_file(
        verification_path, 4 * 1024 * 1024
    )
    require(
        hashlib.sha256(root_raw).hexdigest() == C30C_ROOT_MANIFEST_SHA256
        and hashlib.sha256(verification_raw).hexdigest()
        == C30C_VERIFICATION_SHA256,
        "C30c external root/verification pins",
    )
    root_rows = verifier_manifest_rows(root_raw, "C30c root")
    require(
        root_rows == {
            C30C_PAYLOAD_MANIFEST: hashlib.sha256(payload_raw).hexdigest(),
            C30C_VERIFICATION: C30C_VERIFICATION_SHA256,
        },
        "C30c exact two-member root",
    )

    directory = ROOT / C30C_SEALED
    directory_before = directory.lstat()
    require(
        stat.S_ISDIR(directory_before.st_mode)
        and not directory.is_symlink()
        and directory_before.st_nlink >= 2,
        "C30c seal directory",
    )
    directory_fd = os.open(
        directory,
        os.O_RDONLY | os.O_DIRECTORY | os.O_CLOEXEC
        | getattr(os, "O_NOFOLLOW", 0),
    )
    sealed_raw: dict[str, bytes] = {}
    try:
        opened = os.fstat(directory_fd)
        require(
            verifier_identity(opened) == verifier_identity(directory_before),
            "C30c seal directory open identity",
        )
        names = tuple(sorted(os.listdir(directory_fd)))
        require(names == C30C_SEALED_MEMBERS, "C30c seal exact member names")
        for name in names:
            member_fd = os.open(
                name,
                os.O_RDONLY | os.O_CLOEXEC | getattr(os, "O_NOFOLLOW", 0),
                dir_fd=directory_fd,
            )
            try:
                first = os.fstat(member_fd)
                require(
                    stat.S_ISREG(first.st_mode)
                    and first.st_nlink == 1
                    and first.st_size > 0,
                    "C30c seal singleton:" + name,
                )
                data = bytearray()
                while True:
                    chunk = os.read(member_fd, 1 << 20)
                    if not chunk:
                        break
                    data.extend(chunk)
                second = os.fstat(member_fd)
                raw = bytes(data)
                require(
                    verifier_identity(first) == verifier_identity(second)
                    and len(raw) == first.st_size
                    and hashlib.sha256(raw).hexdigest() == expected_members[name],
                    "C30c seal captured member:" + name,
                )
                sealed_raw[name] = raw
            finally:
                os.close(member_fd)
        final_fd = os.fstat(directory_fd)
        final_path = directory.lstat()
        require(
            verifier_identity(opened) == verifier_identity(final_fd)
            == verifier_identity(final_path)
            and tuple(sorted(os.listdir(directory_fd))) == names,
            "C30c seal changed during verifier capture",
        )
    finally:
        os.close(directory_fd)

    require(
        verifier_identity(root_path.lstat()) == root_identity
        and verifier_identity(payload_path.lstat()) == payload_identity
        and verifier_identity(verification_path.lstat()) == verification_identity,
        "C30c root/verification changed during exact seal capture",
    )

    verification = strict_object_bytes(verification_raw, C30C_VERIFICATION)
    verification_body = dict(verification)
    verification_object_sha256 = verification_body.pop(
        "verification_object_sha256", None
    )
    formal_after = {
        "excluded": 74746,
        "conservative_live": 2086,
        "remaining": 78,
        "resolved_nonexcluded": 2008,
        "total": 76832,
        "remaining_partition": {
            "multi_Delta": 20,
            "reduced_live": 2,
            "retained_source_seams": 2,
            "compact_q": 54,
        },
    }
    require(
        verification_object_sha256 == digest(verification_body)
        and verification.get("status")
        == (
            "PASS_FORMAL_C30C__80_DELTA_H_CELLS__2_RESOLVED_MIXED__"
            "SOURCE_W_80_TO_78__D02_STILL_BLOCKED"
        )
        and verification.get("formal_handoff", {}).get("after") == formal_after
        and verification.get("strict_nonpromotion", {}).get("D02")
        == "BLOCKED_BY_78_REMAINING_SOURCE_W_ORIGINS_AND_COMPOSITE_GATE",
        "C30c independently parsed 78-state handoff",
    )
    result_name = C30C_PREFIX + "_result.json"
    result = strict_object_bytes(sealed_raw[result_name], result_name)
    result_body = dict(result)
    claimed = result_body.pop("result_sha256", None)
    full_delta_keys = result.get("scope", {}).get("origin_keys")
    require(
        claimed == C30C_RESULT_OBJECT_SHA256
        and digest(result_body) == C30C_RESULT_OBJECT_SHA256
        and type(full_delta_keys) is list
        and len(full_delta_keys) == 2
        and digest(full_delta_keys)
        == "a928d0328e94ca98f04a0ee5d5d45ee0b75ee9ca2292afffe5c117880f0d5f93",
        "C30c sealed full-Delta result",
    )
    published = verification.get("sealed_publication", {}).get("sealed_files")
    require(
        type(published) is dict
        and set(published) == set(C30C_SEALED_MEMBERS)
        and all(
            published[name].get("sha256") == expected_members[name]
            and published[name].get("size") == len(sealed_raw[name])
            for name in C30C_SEALED_MEMBERS
        ),
        "C30c verification and seal agree",
    )
    pins = {
        C30C_ROOT_MANIFEST: C30C_ROOT_MANIFEST_SHA256,
        C30C_PAYLOAD_MANIFEST: root_rows[C30C_PAYLOAD_MANIFEST],
        C30C_VERIFICATION: C30C_VERIFICATION_SHA256,
        **{
            os.fspath(C30C_SEALED / name): expected_members[name]
            for name in C30C_SEALED_MEMBERS
        },
    }
    return {
        "pins": pins,
        "pins_sha256": digest([
            {"filename": name, "sha256": value}
            for name, value in sorted(pins.items())
        ]),
        "root_manifest_sha256": C30C_ROOT_MANIFEST_SHA256,
        "verification_sha256": C30C_VERIFICATION_SHA256,
        "verification_object_sha256": verification_object_sha256,
        "sealed_member_map_sha256": digest(expected_members),
        "full_delta_origin_keys": full_delta_keys,
        "formal_after": formal_after,
    }


def parse_c30a_manifest() -> dict[str, str]:
    raw = regular_bytes(ROOT / C30A_MANIFEST, 64 * 1024)
    entries: dict[str, str] = {}
    for line in raw.decode("ascii", "strict").splitlines():
        parts = line.split("  ", 1)
        require(len(parts) == 2 and len(parts[0]) == 64, "C30a manifest syntax")
        expected, filename = parts
        relative = Path(filename)
        require(
            filename not in entries
            and not relative.is_absolute()
            and ".." not in relative.parts,
            "C30a manifest path",
        )
        require(file_hash(ROOT / relative) == expected, "C30a manifest entry:" + filename)
        entries[filename] = expected
    require(
        entries.get(C30A_PRODUCER) == C30A_PRODUCER_SHA256
        and entries.get(os.fspath(C30A_RESULT)) == C30A_RESULT_SHA256
        and entries.get(os.fspath(C30A_CELL_LEDGER)) == C30A_CELL_LEDGER_SHA256,
        "sealed C30a manifest required entries",
    )
    return entries


def exact_input_pins(authority: dict[str, Any]) -> list[dict[str, str]]:
    pin_map: dict[str, str] = dict(authority["pins"])
    for filename, expected in sorted(DIRECT_INPUT_PINS.items()):
        actual = file_hash(ROOT / filename)
        require(actual == expected, "C30d direct input pin:" + filename)
        pin_map[filename] = actual
    for row in base.validate_sources():
        previous = pin_map.get(row["filename"])
        require(
            previous in {None, row["sha256"]},
            "C30d direct/transitive pin disagreement:" + row["filename"],
        )
        pin_map[row["filename"]] = row["sha256"]
    for filename, expected in parse_c30a_manifest().items():
        previous = pin_map.get(filename)
        require(
            previous in {None, expected},
            "C30d pin/manifest disagreement:" + filename,
        )
        pin_map[filename] = expected
    return [
        {"filename": filename, "sha256": sha256}
        for filename, sha256 in sorted(pin_map.items())
    ]


@dataclass(frozen=True)
class InputBundle:
    input_pins: tuple[tuple[str, str], ...]
    c30c_authority: Any
    origin_keys: tuple[str, ...]
    registry: Any
    summaries: Any
    c30a_cells: Any


def load_pinned_inputs() -> InputBundle:
    require(producer_module_absent(), "producer independence before inputs")
    # This is intentionally first: absent C30c publication pins block before
    # any downstream reconstruction can be mistaken for formal-baseline work.
    c30c_authority = verifier_capture_c30c_authority()
    input_pins = exact_input_pins(c30c_authority)
    c30a_result = strict_json(ROOT / C30A_RESULT)
    c30a_body = dict(c30a_result)
    claimed = c30a_body.pop("result_sha256", None)
    require(
        wire(c30a_result) == regular_bytes(ROOT / C30A_RESULT)
        and claimed == C30A_RESULT_OBJECT_SHA256
        and digest(c30a_body) == C30A_RESULT_OBJECT_SHA256
        and c30a_result["source_W_ledger_transition"]["after"]["excluded"]
        == C30A_EVIDENCE_BOUNDARY["excluded"]
        and c30a_result["source_W_ledger_transition"]["after"]["conservative_live"]
        == C30A_EVIDENCE_BOUNDARY["conservative_live"]
        and c30a_result["source_W_ledger_transition"]["after"]["remaining"]
        == C30A_EVIDENCE_BOUNDARY["remaining"]
        and c30a_result["whole_origin_census"]
        ["still_open_active_strict_interior_origins"] == 36,
        "sealed C30a result boundary",
    )

    r184 = strict_json(ROOT / R184_CERTIFICATE)
    r215_certificate = strict_json(ROOT / R215_CERTIFICATE)
    require(
        r184["result_sha256"] == R184_RESULT_SHA256
        and digest(r184["result"]) == R184_RESULT_SHA256
        and r215_certificate["result_sha256"] == R215_RESULT_SHA256
        and digest(r215_certificate["result"]) == R215_RESULT_SHA256
        and r215_certificate["result"]["bounded_probe_result_sha256"]
        == R215_BOUNDED_RESULT_SHA256,
        "pinned R184/R215 result objects",
    )
    bounded = r215_certificate["result"]["bounded_probe_result"]
    summaries = {
        row["origin_key"]: row
        for row in bounded["whole_origin_outcome"]["per_origin_rows"]
        if row["first_obstruction"] == "MULTI_DELTA_GRAPH_ARRANGEMENT"
    }
    origin_keys = tuple(sorted(summaries))
    registry = {
        row["origin_key"]: row
        for row in r184["result"]["priority_registry"]["rows"]
        if row["origin_key"] in summaries
    }
    require(
        len(origin_keys) == EXPECTED_ORIGINS
        and digest(list(origin_keys)) == EXPECTED_ORIGIN_KEYS_SHA256
        and set(registry) == set(origin_keys)
        and set(origin_keys).isdisjoint(c30c_authority["full_delta_origin_keys"])
        and all(
            registry[key]["priority_class"] == "DELTA_H_OR_MULTI_NO_Q"
            and registry[key]["selection_uses_new_closure_outcome"] is False
            and registry[key]["Round180_residual_child_count"]
            == summaries[key]["Round201_residual_cell_count"]
            and summaries[key]["Round215_analytic_closed_cell_count"] == 0
            and set(summaries[key]["Round215_blocker_count"]) == {
                "MULTI_DELTA_GRAPH_ARRANGEMENT",
                "SINGLE_CLIPPED_DELTA_ENDPOINT_OVERWRAP",
            }
            for key in origin_keys
        )
        and sum(row["Round201_residual_cell_count"] for row in summaries.values())
        == EXPECTED_FINAL_CELLS
        and sum(
            row["Round215_blocker_count"]["MULTI_DELTA_GRAPH_ARRANGEMENT"]
            for row in summaries.values()
        ) == EXPECTED_MULTI_CELLS
        and sum(
            row["Round215_blocker_count"]["SINGLE_CLIPPED_DELTA_ENDPOINT_OVERWRAP"]
            for row in summaries.values()
        ) == EXPECTED_C30A_CLIPPED_CELLS,
        "dynamic twenty-origin R184/R215 selection",
    )

    all_c30a_cells = list(candidate_rows(ROOT / C30A_CELL_LEDGER))
    origin_set = set(origin_keys)
    c30a_cells = {
        row["cell_key"]: row
        for row in all_c30a_cells
        if row["origin_key"] in origin_set
    }
    require(
        len(all_c30a_cells)
        == c30a_result["ledgers"]["reduced_clipped_cell"]["row_count"]
        and file_hash(ROOT / C30A_CELL_LEDGER) == C30A_CELL_LEDGER_SHA256
        and len(c30a_cells) == EXPECTED_C30A_CLIPPED_CELLS
        and digest(sorted(c30a_cells)) == EXPECTED_C30A_CELL_KEYS_SHA256
        and Counter(row["disposition"] for row in c30a_cells.values())
        == EXPECTED_C30A_CLIPPED_DISPOSITION
        and Counter(row["candidate_target"] for row in c30a_cells.values())
        == EXPECTED_C30A_CLIPPED_TARGET
        and all(
            row["whole_closed_cell_excluded"] is True
            and row["partition"]
            ["closed_box_and_all_owned_faces_edges_vertices_excluded"] is True
            for row in c30a_cells.values()
        ),
        "sealed C30a clipped cells for selected origins",
    )
    require(producer_module_absent(), "producer independence after inputs")
    return InputBundle(
        tuple((row["filename"], row["sha256"]) for row in input_pins),
        MappingProxyType(c30c_authority),
        origin_keys,
        MappingProxyType(registry),
        MappingProxyType(summaries),
        MappingProxyType(c30a_cells),
    )


def original_origin_leaf(origin: str) -> Any:
    chart_id, path = origin.rsplit(":", 1)
    reflected = path.startswith("H.")
    raw_path = path[2:] if reflected else path
    source_chart = "W:N" if reflected else chart_id
    require(
        source_chart == "W:N"
        and len(raw_path) == 14
        and raw_path[2] == "."
        and raw_path[5] == ".",
        "independent multi-Delta origin path:" + origin,
    )
    initial_path = raw_path[:6]
    matches = [box for box in r176.initial_boxes() if box.path == initial_path]
    require(len(matches) == 1, "independent origin initial box:" + origin)
    box = matches[0]
    for bit in raw_path[6:]:
        require(bit in "01", "independent origin path bit:" + origin)
        box = r176.split(box)[int(bit)]
    leaf, _records = r176.classify(source_chart, box, r176.CANDIDATES[source_chart])
    if reflected:
        leaf = r176.reflect_horizontal(leaf)
    require(
        leaf.box.path == path
        and leaf.classification == "multi_candidate"
        and r176.FROZEN_OWNER in leaf.active_targets,
        "independent original atlas leaf:" + origin,
    )
    return leaf


def independent_local_round176_replay(origin: str) -> dict[str, Any]:
    source_leaf = original_origin_leaf(origin)
    chart_id = origin.rsplit(":", 1)[0]
    pending = [
        r176.Node(chart_id, source_leaf.box, source_leaf.active_targets, source_leaf.box.path)
    ]
    frontier: list[Any] = []
    prior: list[dict[str, Any]] = []
    origin_kinds: set[str] = set()
    for relative_depth in range(7):
        next_pending: list[Any] = []
        for node in pending:
            leaf, records = r176.classify(node.chart_id, node.box, node.active_targets)
            disposition, margins = r176.terminal_disposition(node.chart_id, leaf)
            if disposition is not None:
                evidence: dict[str, Any] = {
                    "leaf_key": f"{node.chart_id}:{node.box.path}",
                    "relative_depth": relative_depth,
                    "dimension": 3,
                    "disposition": disposition,
                    "coverage_numerator_64": 2 ** (6 - relative_depth),
                }
                if margins is not None:
                    evidence["closed_interval_outgoing_margin_signs"] = {
                        key: (
                            "POSITIVE" if bool(value > 0)
                            else "NEGATIVE" if bool(value < 0)
                            else "OVERWRAPPED"
                        )
                        for key, value in sorted(margins.items())
                    }
                prior.append(evidence)
                origin_kinds.add(
                    "EXCLUDED" if disposition.startswith("EXCLUDED") else "LIVE"
                )
                continue
            failure = r176.failure_type(leaf, records, margins)
            inherited = (
                (r176.FROZEN_OWNER,)
                if leaf.classification == "unique_first"
                else node.active_targets
                if leaf.classification == "tangency_graph"
                else leaf.active_targets
            )
            if relative_depth == 6:
                frontier.append(r176.Frontier(
                    node.chart_id, node.box, inherited, origin, failure
                ))
            else:
                widths = (
                    node.box.t1 - node.box.t0,
                    node.box.p1 - node.box.p0,
                    node.box.s1 - node.box.s0,
                )
                axis = max(range(3), key=lambda index: widths[index])
                next_pending.extend(
                    r176.Node(node.chart_id, child, inherited, node.origin_path)
                    for child in r176.split(node.box, axis)
                )
        pending = next_pending
    require(
        origin_kinds <= {"EXCLUDED"}
        and all(row["disposition"].startswith("EXCLUDED") for row in prior),
        "independent prior exclusion:" + origin,
    )
    return {
        "frontier": sorted(frontier, key=lambda row: row.key),
        "origins": {origin: {
            "chart_id": chart_id,
            "path": source_leaf.box.path,
            "box": source_leaf.box,
            "active_targets": tuple(source_leaf.active_targets),
        }},
        "prior": {origin: sorted(prior, key=lambda row: row["leaf_key"])},
        "origin_kinds": {origin: origin_kinds},
    }


def sign_name(value: Any) -> str:
    value_sign = r176.sign(value)
    return (
        "STRICT_POSITIVE" if value_sign > 0
        else "STRICT_NEGATIVE" if value_sign < 0
        else "OVERWRAP"
    )


def all_outgoing_margin_signs(nx: Any, ny: Any) -> dict[str, str]:
    margins = {
        "E.first": nx - ny,
        "E.second": nx + ny,
        "W.first": -nx - ny,
        "W.second": -nx + ny,
        "N.first": ny - nx,
        "N.second": ny + nx,
        "S.first": -ny - nx,
        "S.second": -ny + nx,
    }
    return {key: sign_name(value) for key, value in sorted(margins.items())}


def independent_universal_contact_audit(
    row: Any, owner_record: Any
) -> dict[str, Any]:
    """Enclose all real W-near contacts without ordering Delta graphs."""
    require(
        owner_record.target_id == r176.FROZEN_OWNER
        and owner_record.classification == "unresolved_discriminant",
        "C30d frozen owner unresolved Delta:" + row.key,
    )
    _qx, _qy, ux, uy, _s, _rp = r176.geometry(row.chart_id, row.box)
    radius = r176.base.arbq(r176.base.RADIUS["W"])
    upper = owner_record.discriminant.upper()
    require(bool(upper > 0), "C30d positive Delta upper bound:" + row.key)

    # h=0 includes Delta=0.  The closed upper endpoint includes every
    # positive-Delta near root; taking one interval also includes all graph
    # intersections and root-order ties that could select W first.
    h = r176.hull(arb(0), upper.sqrt().upper())
    transverse = owner_record.transverse
    nx = (transverse * uy - h * ux) / radius
    ny = (-transverse * ux - h * uy) / radius
    signs = all_outgoing_margin_signs(nx, ny)
    strict_charts = [
        chart for chart in ("E", "W", "N", "S")
        if signs[chart + ".first"] == "STRICT_POSITIVE"
        and signs[chart + ".second"] == "STRICT_POSITIVE"
    ]
    expected_chart = "N" if row.chart_id == "W:N" else "S"
    require(
        len(strict_charts) == 1
        and strict_charts[0] == expected_chart
        and expected_chart != r176.FROZEN_CHART
        and bool(owner_record.ell - radius > 0)
        and bool(owner_record.ell < r176.base.arbq(r176.base.TAU_MAX)),
        "C30d universal W first-target owner mismatch:" + row.key,
    )
    return {
        "candidate_target": r176.FROZEN_OWNER,
        "candidate_obstacle": "W",
        "closed_box_Delta_classification": "UNRESOLVED_DISCRIMINANT",
        "actual_Delta_negative_case": "NO_REAL_W_INTERSECTION",
        "actual_Delta_zero_case": "TANGENCY_INCLUDED_BY_RADICAL_h_EQUALS_0",
        "actual_Delta_positive_case": (
            "NEAR_CONTACT_INCLUDED_BY_0_LE_h_LE_sqrt_CLOSED_DELTA_UPPER"
        ),
        "ell_minus_target_radius_sign": "STRICT_POSITIVE",
        "ell_below_frozen_tau_horizon": True,
        "near_root_is_strict_future_whenever_Delta_is_nonnegative": True,
        "contact_normal_enclosure_formula": {
            "h": "[0,sqrt(max(0,sup(Delta_W)))]",
            "nx": "(transverse*uy-h*ux)/R_W",
            "ny": "(-transverse*ux-h*uy)/R_W",
        },
        "all_eight_contact_normal_margin_signs": signs,
        "unique_strict_contact_chart": expected_chart,
        "frozen_stage_one_chart": r176.FROZEN_CHART,
        "outgoing_chart_mismatch_on_every_possible_near_contact": True,
        "closed_interval_proof_restricts_to_every_owned_face_edge_vertex": True,
    }


def reduction_projection(reduction: dict[str, Any]) -> dict[str, Any]:
    return {
        "category": reduction["category"],
        "residual_reason": reduction["residual_reason"],
        "closed": reduction["closed"],
        "disposition": reduction["disposition"],
        "eligible_targets": reduction["eligible_targets"],
        "candidate_evidence": reduction["candidate_evidence"],
    }


def independent_multi_delta_cell(
    ordinal: int,
    row: Any,
    reduction: dict[str, Any],
    evidence: dict[str, Any],
) -> dict[str, Any]:
    expected_g1 = "G[1,1]" if row.chart_id == "W:N" else "G[1,0]"
    expected_g2 = "G[2,1]" if row.chart_id == "W:N" else "G[2,0]"
    expected_targets = (expected_g1, expected_g2, r176.FROZEN_OWNER)
    records = {
        record.target_id: record for record in reduction["current_records"]
    }
    classes = {key: records[key].classification for key in sorted(records)}
    require(
        evidence["blocker"] == "MULTI_DELTA_GRAPH_ARRANGEMENT"
        and evidence["method"] == "MULTI_EQUATION_ARRANGEMENT_CENSUS"
        and evidence["remaining_unresolved_target_count"] == 2
        and tuple(evidence["remaining_unresolved_targets"])
        == (expected_g1, r176.FROZEN_OWNER)
        and tuple(sorted(row.active_targets)) == expected_targets
        and tuple(sorted(records)) == expected_targets
        and classes == {
            expected_g1: "unresolved_discriminant",
            expected_g2: "strict_future_root",
            r176.FROZEN_OWNER: "unresolved_discriminant",
        }
        and reduction["eligible_targets"] == [],
        "C30d independent three-target identity:" + row.key,
    )
    contact_audit = independent_universal_contact_audit(
        row, records[r176.FROZEN_OWNER]
    )
    target_rows = [
        {
            "target": expected_g1,
            "obstacle": "G",
            "possible_first_hit_disposition": (
                "EXCLUDED_UNIQUE_FIRST_OWNER_MISMATCH"
            ),
            "proof_restricts_to_3D_2D_1D_0D": True,
        },
        {
            "target": expected_g2,
            "obstacle": "G",
            "possible_first_hit_disposition": (
                "EXCLUDED_UNIQUE_FIRST_OWNER_MISMATCH"
            ),
            "proof_restricts_to_3D_2D_1D_0D": True,
        },
        {
            "target": r176.FROZEN_OWNER,
            "obstacle": "W",
            "possible_first_hit_disposition": (
                "EXCLUDED_OUTGOING_CHART_MISMATCH"
            ),
            "strict_outgoing_chart": contact_audit["unique_strict_contact_chart"],
            "proof_restricts_to_3D_2D_1D_0D": True,
        },
    ]
    theorem = {
        "kind": (
            "SOURCE_W_MULTI_DELTA_CLOSED_ENCLOSURE_UNIVERSAL_TARGET_"
            "EXCLUSION_THEOREM_CANDIDATE"
        ),
        "frozen_R176_active_target_set_is_pointwise_exhaustive": True,
        "exact_behind_reduction_deletes_no_target_in_this_cell": True,
        "every_G_target_is_a_frozen_owner_mismatch": True,
        "every_possible_W_near_contact_has_strict_N_or_S_chart_mismatch": True,
        "Delta_W_zero_tangencies_are_inside_the_contact_enclosure": True,
        "Delta_G_Delta_W_intersections_are_inside_the_same_target_cases": True,
        "root_order_ties_need_no_ordering_for_exclusion": True,
        "reason_no_rank_aware_CAD_is_needed": (
            "EVERY_MEMBER_OF_EVERY_POSSIBLE_FIRST_TARGET_TIE_IS_EXCLUDED"
        ),
        "first_target_tie_bookkeeping_owner_rule": (
            "LEXICOGRAPHIC_LEAST_TARGET_ID__EXCLUSION_IS_TIE_INVARIANT"
        ),
        "analytic_equality_stratum_owner_rule": (
            "FIRST_APPLY_DYADIC_HALF_OPEN_OWNER__THEN_LEXICOGRAPHIC_"
            "TARGET_TIE_OWNER_INSIDE_THAT_CLOSED_ENCLOSURE"
        ),
        "analytic_equality_dimension_or_transversality_assumption_used": False,
        "degenerate_Delta_or_root_order_equalities_remain_excluded": True,
        "pointwise_first_target_cases_are_exhaustive_and_disjoint_after_"
        "deterministic_tie_ownership": True,
        "closed_box_and_every_owned_face_edge_vertex_excluded": True,
    }
    projection = reduction_projection(reduction)
    body = {
        "schema": "cm2.round306c30d.source-w-multi-delta.cell-row.v1",
        "cell_ordinal": ordinal,
        "cell_key": row.key,
        "origin_key": row.origin_key,
        "source_chart_id": row.chart_id,
        "closed_box": r176.box_row(row.box),
        "exact_volume": str(r215.box_volume(row.box)),
        "active_targets": list(sorted(row.active_targets)),
        "post_exact_behind_record_classes": classes,
        "Round215_reconstructed_evidence_sha256": digest(evidence),
        "Round215_reduction_projection": projection,
        "Round215_reduction_projection_sha256": digest(projection),
        "frozen_owner_contact_audit": contact_audit,
        "exhaustive_possible_first_target_rows": target_rows,
        "exhaustive_possible_first_target_rows_sha256": digest(target_rows),
        "analytic_and_dyadic_ownership_composition": {
            "step_1": (
                "ATOMIC_DYADIC_HALF_OPEN_AUDIT_SELECTS_ONE_CLOSED_3D_"
                "ENCLOSURE_FOR_EVERY_3D_2D_1D_0D_POINT"
            ),
            "step_2": (
                "WITHIN_THE_SELECTED_ENCLOSURE_LEXICOGRAPHIC_TARGET_"
                "OWNERSHIP_BREAKS_ANY_FIRST_ROOT_TIE"
            ),
            "step_3": (
                "THE_SELECTED_TARGET_IS_EXCLUDED_BY_DISCRETE_G_MISMATCH_"
                "OR_CLOSED_INTERVAL_W_OUTGOING_MISMATCH"
            ),
            "Delta_graph_or_root_order_stratum_dimension_needed": False,
            "all_degenerate_and_transverse_equalities_covered": True,
        },
        "closed_enclosure_exclusion_theorem_candidate": theorem,
        "closed_enclosure_exclusion_theorem_candidate_sha256": digest(theorem),
        "whole_closed_cell_disposition": "EXCLUDED",
        "whole_closed_cell_excluded": True,
        "candidate_credit_if_independently_verified": {
            "multi_Delta_cell_disposition": 1,
            "whole_closed_cell_exclusion": 1,
            "whole_source_W_origin_exclusion": 0,
        },
        "formal_credit": {
            "multi_Delta_cell_disposition": 0,
            "whole_closed_cell_exclusion": 0,
            "whole_source_W_origin_exclusion": 0,
        },
        "strict_nonpromotion": (
            "PRODUCER_ONLY__NO_INDEPENDENT_C30D_VERIFIER_OR_MANIFEST"
        ),
    }
    return sealed(body)


def verifier_materialize_atomic_owner_rows(
    parent: Any,
    leaf_rows: dict[str, Any],
    proof_source: dict[str, str],
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    """Independent sparse plane-sweep reconstruction of every atomic row."""
    axes = ("t", "p", "s")
    origin = next(iter(leaf_rows.values())).origin_key
    bounds = {
        key: {
            "t": (row.box.t0, row.box.t1),
            "p": (row.box.p0, row.box.p1),
            "s": (row.box.s0, row.box.s1),
        }
        for key, row in leaf_rows.items()
    }
    require(set(bounds) == set(proof_source), "independent atomic proof coverage")
    grid = {
        axis: sorted({coordinate for box in bounds.values()
                      for coordinate in box[axis]})
        for axis in axes
    }

    def unpack(geometry: dict[str, Any]) -> tuple[
        dict[str, Q], dict[str, tuple[Q, Q]]
    ]:
        return (
            {axis: Q(value) for axis, value in geometry["fixed"].items()},
            {axis: (Q(values[0]), Q(values[1]))
             for axis, values in geometry["open_spans"].items()},
        )

    def close_atom(
        dimension: int, geometry: dict[str, Any], sources: list[str]
    ) -> dict[str, Any]:
        fixed, spans = unpack(geometry)
        probes = {axis: (lower + upper) / 2
                  for axis, (lower, upper) in spans.items()}
        containing: list[str] = []
        for leaf_key in sorted(bounds):
            box = bounds[leaf_key]
            if any(not box[axis][0] <= value <= box[axis][1]
                   for axis, value in fixed.items()):
                continue
            if any(not box[axis][0] <= lower < upper <= box[axis][1]
                   for axis, (lower, upper) in spans.items()):
                continue
            if any(not box[axis][0] < probe < box[axis][1]
                   for axis, probe in probes.items()):
                continue
            containing.append(leaf_key)
        require(bool(containing), "independent atomic owner exists:" + origin)
        owner = containing[0]
        incidence_rows: list[dict[str, Any]] = []
        for leaf_key in containing:
            signature: dict[str, str] = {}
            for axis, coordinate in sorted(fixed.items()):
                lower, upper = bounds[leaf_key][axis]
                if coordinate == lower:
                    signature[axis] = "LOWER"
                elif coordinate == upper:
                    signature[axis] = "UPPER"
            incidence_rows.append(sealed({
                "schema": "cm2.round306c30d.atomic-leaf-incidence.row.v2",
                "leaf_key": leaf_key,
                "relative_boundary_signature": signature,
                "relative_boundary_codimension": len(signature),
                "selected_by_half_open_owner": leaf_key == owner,
                "proof_source": proof_source[leaf_key],
                "leaf_disposition": "EXCLUDED",
            }))
        measure = Q(1)
        for lower, upper in spans.values():
            measure *= upper - lower
        source_set = sorted(set(sources))
        body = {
            "schema": "cm2.round306c30d.atomic-half-open-owner.row.v2",
            "origin_key": origin,
            "ambient_dimension": dimension,
            "geometry": geometry,
            "geometry_sha256": digest(geometry),
            "exact_measure": str(measure),
            "incident_sources": source_set,
            "incident_source_count": len(source_set),
            "closed_containing_leaf_keys": containing,
            "closed_incident_leaf_rows": incidence_rows,
            "closed_incident_leaf_rows_sha256": digest(incidence_rows),
            "half_open_owner_leaf_key": owner,
            "owner_selection_rule": (
                "DETERMINISTIC_LEAF_KEY_LEXICOGRAPHIC_MIN_CONTAINING_LEAF"
            ),
            "owner_proof_source": proof_source[owner],
            "owner_disposition": "EXCLUDED",
            "cross_dimensional_source_incidence_complete": True,
        }
        if dimension == 3:
            require(len(containing) == 1,
                    "independent unique open 3D leaf atom:" + origin)
            source_row = {
                "leaf_key": owner,
                "exact_closed_box_projection": geometry,
                "proof_source": proof_source[owner],
                "disposition": "EXCLUDED",
            }
            body["source_3D_leaf_row"] = source_row
            body["source_3D_leaf_row_sha256"] = digest(source_row)
        return sealed(body)

    rows_3d = []
    for leaf_key in sorted(bounds):
        rows_3d.append(close_atom(3, {
            "fixed": {},
            "open_spans": {
                axis: [str(bounds[leaf_key][axis][0]),
                       str(bounds[leaf_key][axis][1])]
                for axis in axes
            },
        }, ["CLOSED_3D_LEAF:" + leaf_key + ":" + proof_source[leaf_key]]))

    planes: dict[
        tuple[str, Q], list[tuple[str, str, dict[str, tuple[Q, Q]]]]
    ] = defaultdict(list)
    for leaf_key, box in sorted(bounds.items()):
        for axis in axes:
            spans = {other: box[other] for other in axes if other != axis}
            planes[(axis, box[axis][0])].append((leaf_key, "LOWER", spans))
            planes[(axis, box[axis][1])].append((leaf_key, "UPPER", spans))
    rows_2d: list[dict[str, Any]] = []
    for (fixed_axis, coordinate), plane_rows in sorted(
        planes.items(), key=lambda item: (item[0][0], item[0][1])
    ):
        free_axes = [axis for axis in axes if axis != fixed_axis]
        rectangles: set[tuple[tuple[Q, Q], tuple[Q, Q]]] = set()
        for _leaf, _side, spans in plane_rows:
            interval_sets = []
            for axis in free_axes:
                values = [value for value in grid[axis]
                          if spans[axis][0] <= value <= spans[axis][1]]
                interval_sets.append(list(zip(values, values[1:])))
            rectangles.update(itertools.product(*interval_sets))
        for rectangle in sorted(rectangles):
            sources = [
                "LEAF_FACE:" + leaf + ":" + fixed_axis + ":" + side
                for leaf, side, spans in plane_rows
                if all(spans[axis][0] <= interval[0] < interval[1]
                       <= spans[axis][1]
                       for axis, interval in zip(
                           free_axes, rectangle, strict=True
                       ))
            ]
            require(bool(sources), "independent face source incidence")
            geometry = {
                "fixed": {fixed_axis: str(coordinate)},
                "open_spans": {
                    axis: [str(interval[0]), str(interval[1])]
                    for axis, interval in zip(
                        free_axes, rectangle, strict=True
                    )
                },
            }
            rows_2d.append(close_atom(2, geometry, sources))
    rows_2d.sort(key=lambda row: wire(row["geometry"]))

    line_geometries: dict[bytes, dict[str, Any]] = {}
    for face in rows_2d:
        fixed, spans = unpack(face["geometry"])
        for boundary_axis in sorted(spans):
            free_axis = next(axis for axis in spans if axis != boundary_axis)
            for endpoint in spans[boundary_axis]:
                geometry = {
                    "fixed": {axis: str(value) for axis, value in sorted({
                        **fixed, boundary_axis: endpoint,
                    }.items())},
                    "open_spans": {free_axis: [
                        str(spans[free_axis][0]), str(spans[free_axis][1])
                    ]},
                }
                line_geometries[wire(geometry)] = geometry
    rows_1d: list[dict[str, Any]] = []
    for _encoded, geometry in sorted(line_geometries.items()):
        line_fixed, line_spans = unpack(geometry)
        sources: list[str] = []
        for face in rows_2d:
            face_fixed, face_spans = unpack(face["geometry"])
            plane_axis, plane_value = next(iter(face_fixed.items()))
            if line_fixed.get(plane_axis) != plane_value:
                continue
            boundary_axes = [axis for axis in face_spans if axis in line_fixed]
            if len(boundary_axes) != 1:
                continue
            boundary_axis = boundary_axes[0]
            if line_fixed[boundary_axis] == face_spans[boundary_axis][0]:
                side = "LOWER"
            elif line_fixed[boundary_axis] == face_spans[boundary_axis][1]:
                side = "UPPER"
            else:
                continue
            free_axis = next(axis for axis in face_spans if axis != boundary_axis)
            if line_spans == {free_axis: face_spans[free_axis]}:
                sources.append(
                    "ATOMIC_2D:" + face["row_sha256"] + ":"
                    + boundary_axis + ":" + side
                )
        require(bool(sources), "independent line source incidence")
        rows_1d.append(close_atom(1, geometry, sources))

    point_geometries: dict[bytes, dict[str, Any]] = {}
    for line in rows_1d:
        fixed, spans = unpack(line["geometry"])
        free_axis, interval = next(iter(spans.items()))
        for endpoint in interval:
            geometry = {
                "fixed": {axis: str(value) for axis, value in sorted({
                    **fixed, free_axis: endpoint,
                }.items())},
                "open_spans": {},
            }
            point_geometries[wire(geometry)] = geometry
    rows_0d: list[dict[str, Any]] = []
    for _encoded, geometry in sorted(point_geometries.items()):
        fixed, _spans = unpack(geometry)
        sources: list[str] = []
        for line in rows_1d:
            line_fixed, line_spans = unpack(line["geometry"])
            if any(fixed.get(axis) != value for axis, value in line_fixed.items()):
                continue
            free_axis, interval = next(iter(line_spans.items()))
            if fixed.get(free_axis) == interval[0]:
                side = "LOWER"
            elif fixed.get(free_axis) == interval[1]:
                side = "UPPER"
            else:
                continue
            sources.append("ATOMIC_1D:" + line["row_sha256"] + ":" + side)
        require(bool(sources), "independent point source incidence")
        rows_0d.append(close_atom(0, geometry, sources))

    all_rows = rows_3d + rows_2d + rows_1d + rows_0d
    require(
        all(rows for rows in (rows_3d, rows_2d, rows_1d, rows_0d))
        and all(row["owner_disposition"] == "EXCLUDED" for row in all_rows),
        "independent complete excluded atomic dimensions:" + origin,
    )
    parent_volume = r215.box_volume(parent)
    leaf_volume = sum(
        (r215.box_volume(row.box) for row in leaf_rows.values()), Q(0)
    )
    ordered = sorted(bounds)
    pair_rows: list[dict[str, Any]] = []
    for first_ordinal, first in enumerate(ordered):
        for second in ordered[first_ordinal + 1:]:
            overlap = all(
                max(bounds[first][axis][0], bounds[second][axis][0])
                < min(bounds[first][axis][1], bounds[second][axis][1])
                for axis in axes
            )
            require(not overlap, "independent atomic 3D overlap:" + origin)
            pair_rows.append({
                "first": first, "second": second, "interior_overlap": overlap,
            })
    require(leaf_volume == parent_volume, "independent atomic exhaustion:" + origin)
    census = Counter(str(row["ambient_dimension"]) + "D" for row in all_rows)
    summary = {
        "schema": "cm2.round306c30d.atomic-owner-ledger-slice.v2",
        "origin_key": origin,
        "external_ledger_filename": ATOMIC_OWNER_LEDGER,
        "row_count": len(all_rows),
        "dimension_census": dict(sorted(census.items())),
        "row_sha256_sequence_sha256": digest([
            row["row_sha256"] for row in all_rows
        ]),
        "rows_sha256": digest(all_rows),
        "closed_3D_leaf_count": len(leaf_rows),
        "closed_3D_leaf_keys_sha256": digest(sorted(leaf_rows)),
        "closed_3D_leaf_proof_sources_sha256": digest(proof_source),
        "parent_exact_volume": str(parent_volume),
        "closed_3D_leaf_exact_volume_sum": str(leaf_volume),
        "tested_unordered_3D_leaf_pair_count": len(pair_rows),
        "tested_unordered_3D_leaf_pairs_sha256": digest(pair_rows),
        "axis_grid_coordinates_sha256": digest({
            axis: [str(value) for value in values]
            for axis, values in grid.items()
        }),
        "all_3D_interiors_pairwise_disjoint": True,
        "all_3D_leaves_exhaust_parent": True,
        "all_3D_2D_1D_0D_atoms_materialized": True,
        "all_atoms_have_exact_measure_and_source_incidence": True,
        "all_atoms_have_unique_half_open_owner": True,
        "all_owner_dispositions_EXCLUDED": True,
        "sampled_evidence_used_for_uniform_conclusion": False,
    }
    return summary, all_rows


def independent_prior_partition(
    replay: dict[str, Any], origin: str
) -> dict[str, Any]:
    """Rename the C30a verifier's independently rebuilt prior partition."""
    prior = base.prior_partition(replay, origin)
    return {
        "prior_closed_rows": prior["closed"],
        "prior_closed_count": prior["count"],
        "prior_closed_exact_volume": prior["volume"],
        "split_face_rows": prior["split_faces"],
    }


def reconstruct_origin(
    origin_ordinal: int,
    multi_ordinal: int,
    origin: str,
    bundle: InputBundle,
) -> tuple[dict[str, Any], list[dict[str, Any]], list[dict[str, Any]]]:
    replay = independent_local_round176_replay(origin)
    frontier = replay["frontier"]
    roots: list[Any] = []
    base_rows: list[Any] = []
    base_kinds: set[str] = set()
    for row in frontier:
        kind, _evidence = r176.closure(row)
        if kind is None:
            roots.append(row)
        else:
            base_rows.append(row)
            base_kinds.add(kind)
    roots.sort(key=lambda row: row.key)
    base_rows.sort(key=lambda row: row.key)
    require(base_kinds <= {"EXCLUDED"}, "C30d preclosed frontier:" + origin)

    refinement = r180.refine_origin(roots, 4)
    inherited = sorted(
        refinement["terminal_rows"], key=lambda value: value["cell_key"]
    )
    final_rows = sorted(
        refinement["final_residual_rows"], key=lambda value: value.key
    )
    summary = bundle.summaries[origin]
    registry = bundle.registry[origin]
    require(
        all(row["coarse_disposition"] == "EXCLUDED" for row in inherited)
        and len(final_rows) == summary["Round201_residual_cell_count"]
        == registry["Round180_residual_child_count"],
        "C30d inherited/final reconstruction:" + origin,
    )

    prior = independent_prior_partition(replay, origin)
    leaves = r215.reconstruct_refinement_leaf_frontiers(roots, refinement)
    proof_source = {
        key: "PINNED_PRE_DEPTH14_EXCLUDED"
        for key in prior["prior_closed_rows"]
    }
    proof_source.update({
        row.key: "PINNED_ROUND176_PRECLOSED_EXCLUDED" for row in base_rows
    })
    proof_source.update({
        row["cell_key"]: "PINNED_ROUND180_INHERITED_EXCLUDED"
        for row in inherited
    })

    origin_multi_rows: list[dict[str, Any]] = []
    c30a_keys: list[str] = []
    round201_keys: list[str] = []
    round215_keys: list[str] = []
    final_census: Counter[str] = Counter()
    for row in final_rows:
        reduction = r215.exact_behind_reduce(row, r180.residual_category(row))
        if reduction["closed"]:
            round201_keys.append(row.key)
            proof_source[row.key] = "PINNED_ROUND201_EXACT_BEHIND_EXCLUDED"
            final_census["ROUND201_EXCLUDED"] += 1
            continue
        evidence = r215.analyze_residual_cell(row, reduction)
        if evidence["analytic_closed"]:
            round215_keys.append(row.key)
            proof_source[row.key] = "PINNED_ROUND215_ANALYTIC_EXCLUDED"
            final_census["ROUND215_EXCLUDED"] += 1
            continue
        if evidence["blocker"] == "SINGLE_CLIPPED_DELTA_ENDPOINT_OVERWRAP":
            clipped = bundle.c30a_cells.get(row.key)
            require(
                clipped is not None and clipped["whole_closed_cell_excluded"] is True,
                "C30d sealed C30a clipped binding:" + row.key,
            )
            c30a_keys.append(row.key)
            proof_source[row.key] = "SEALED_C30A_CLIPPED_DELTA_EXCLUDED"
            final_census["SEALED_C30A_CLIPPED_EXCLUDED"] += 1
            continue
        require(
            evidence["blocker"] == "MULTI_DELTA_GRAPH_ARRANGEMENT",
            "C30d unexpected final blocker:" + row.key,
        )
        candidate = independent_multi_delta_cell(
            multi_ordinal + len(origin_multi_rows), row, reduction, evidence
        )
        origin_multi_rows.append(candidate)
        proof_source[row.key] = "ROUND306C30D_UNIVERSAL_TARGET_EXCLUDED"
        final_census["ROUND306C30D_MULTI_DELTA_EXCLUDED"] += 1

    require(
        not round201_keys
        and not round215_keys
        and len(c30a_keys) == summary["Round215_blocker_count"]
        ["SINGLE_CLIPPED_DELTA_ENDPOINT_OVERWRAP"]
        and len(origin_multi_rows) == summary["Round215_blocker_count"]
        ["MULTI_DELTA_GRAPH_ARRANGEMENT"]
        and len(c30a_keys) + len(origin_multi_rows) == len(final_rows),
        "C30d per-origin final composition:" + origin,
    )

    leaf_rows: dict[str, Any] = dict(prior["prior_closed_rows"])
    leaf_rows.update({row.key: row for row in base_rows})
    leaf_rows.update(leaves["terminal"])
    leaf_rows.update(leaves["final"])
    require(set(leaf_rows) == set(proof_source), "C30d leaf proof coverage:" + origin)
    owner_audit, atomic_owner_rows = verifier_materialize_atomic_owner_rows(
        replay["origins"][origin]["box"],
        leaf_rows,
        proof_source,
    )
    require(
        owner_audit["all_3D_2D_1D_0D_atoms_materialized"]
        and owner_audit["all_atoms_have_unique_half_open_owner"]
        and owner_audit["all_owner_dispositions_EXCLUDED"],
        "C30d independent 3D/2D/1D/0D owner closure:" + origin,
    )

    parent_volume = r215.box_volume(replay["origins"][origin]["box"])
    base_volume = sum((r215.box_volume(row.box) for row in base_rows), Q(0))
    root_volume = sum((r215.box_volume(row.box) for row in roots), Q(0))
    inherited_volume = sum(
        (r215.box_volume(row.box) for row in leaves["terminal"].values()), Q(0)
    )
    final_volume = sum((r215.box_volume(row.box) for row in final_rows), Q(0))
    c30a_volume = sum(
        (r215.box_volume(leaves["final"][key].box) for key in c30a_keys), Q(0)
    )
    multi_volume = sum(
        (Q(row["exact_volume"]) for row in origin_multi_rows), Q(0)
    )
    require(
        prior["prior_closed_exact_volume"] + base_volume + root_volume
        == parent_volume
        and inherited_volume + final_volume == root_volume
        and c30a_volume + multi_volume == final_volume,
        "C30d independent exact volume conservation:" + origin,
    )

    lower_ledger = r180.lower_strata_ledger(refinement["split_face_rows"])
    theorem = {
        "kind": "SOURCE_W_MULTI_DELTA_WHOLE_ORIGIN_EXCLUSION_THEOREM_CANDIDATE",
        "Round176_prior_and_frontier_partition_exact": True,
        "Round176_preclosed_all_excluded": True,
        "Round180_inherited_terminals_all_excluded": True,
        "sealed_C30a_clipped_cells_all_excluded": True,
        "every_remaining_multi_Delta_cell_has_universal_target_exclusion": True,
        "Delta_and_root_order_equalities_need_no_separate_disposition": True,
        "reason": "EVERY_POSSIBLE_FIRST_TARGET_IS_EXCLUDED_ON_CLOSED_ENCLOSURE",
        "every_internal_and_outer_3D_2D_1D_0D_stratum_has_one_excluded_"
        "half_open_owner": True,
        "whole_original_physical_origin_excluded": True,
    }
    body = {
        "schema": "cm2.round306c30d.source-w-multi-delta.whole-origin-row.v2",
        "origin_ordinal": origin_ordinal,
        "origin_key": origin,
        "priority_ordinal": registry["priority_ordinal"],
        "source_chart_id": replay["origins"][origin]["chart_id"],
        "original_parent_box": r176.box_row(replay["origins"][origin]["box"]),
        "lineage_census": {
            "Round176_prior_closed": prior["prior_closed_count"],
            "Round176_preclosed_frontier": len(base_rows),
            "Round176_residual_roots": len(roots),
            "Round180_inherited_excluded": len(inherited),
            "Round180_final": len(final_rows),
            "Round201_exact_behind_excluded": len(round201_keys),
            "Round215_analytic_excluded": len(round215_keys),
            "sealed_C30a_clipped_excluded": len(c30a_keys),
            "Round306C30D_multi_Delta_excluded": len(origin_multi_rows),
            "closed_3D_leaf_count": len(leaf_rows),
        },
        "final_cell_disposition_census": dict(sorted(final_census.items())),
        "sealed_C30a_clipped_cell_keys_sha256": digest(sorted(c30a_keys)),
        "Round306C30D_multi_Delta_cell_keys_sha256": digest([
            row["cell_key"] for row in origin_multi_rows
        ]),
        "Round306C30D_multi_Delta_cell_rows_sha256": digest(origin_multi_rows),
        "legacy_lower_dimensional_strata_diagnostic_only": lower_ledger,
        "materialized_atomic_half_open_owner_ledger_slice": owner_audit,
        "materialized_atomic_half_open_owner_ledger_slice_sha256": digest(
            owner_audit
        ),
        "exact_volume_conservation": {
            "original_parent": str(parent_volume),
            "Round176_prior": str(prior["prior_closed_exact_volume"]),
            "Round176_preclosed_frontier": str(base_volume),
            "Round176_residual_roots": str(root_volume),
            "Round180_inherited": str(inherited_volume),
            "Round180_final": str(final_volume),
            "sealed_C30a_clipped": str(c30a_volume),
            "Round306C30D_multi_Delta": str(multi_volume),
            "all_equalities_verified": True,
        },
        "whole_origin_exclusion_theorem_candidate": theorem,
        "whole_origin_exclusion_theorem_candidate_sha256": digest(theorem),
        "whole_origin_disposition_candidate": "EXCLUDED",
        "whole_original_physical_origin_excluded_candidate": True,
        "candidate_credit_if_independently_verified": {
            "resolved_source_W_origin_disposition": 1,
            "whole_source_W_origin_exclusion": 1,
        },
        "formal_credit": {
            "resolved_source_W_origin_disposition": 0,
            "whole_source_W_origin_exclusion": 0,
        },
        "strict_nonpromotion": (
            "PRODUCER_ONLY__NO_INDEPENDENT_C30D_VERIFIER_OR_MANIFEST"
        ),
    }
    return sealed(body), origin_multi_rows, atomic_owner_rows


@dataclass(frozen=True)
class Reference:
    input_pins: tuple[tuple[str, str], ...]
    c30c_authority: Any
    origin_keys: tuple[str, ...]
    expected_cells: tuple[dict[str, Any], ...]
    expected_atomic_owners: tuple[dict[str, Any], ...]
    expected_origins: tuple[dict[str, Any], ...]


def reconstruct_reference() -> Reference:
    require(producer_module_absent(), "producer independence before reconstruction")
    ctx.prec = 192
    bundle = load_pinned_inputs()
    origin_rows: list[dict[str, Any]] = []
    multi_rows: list[dict[str, Any]] = []
    atomic_owner_rows: list[dict[str, Any]] = []
    for origin_ordinal, origin in enumerate(bundle.origin_keys):
        origin_row, rows, owner_rows = reconstruct_origin(
            origin_ordinal, len(multi_rows), origin, bundle
        )
        origin_rows.append(origin_row)
        multi_rows.extend(rows)
        atomic_owner_rows.extend(owner_rows)
    lineage = Counter()
    for row in origin_rows:
        lineage.update(row["lineage_census"])
    require(
        len(origin_rows) == EXPECTED_ORIGINS
        and len(multi_rows) == EXPECTED_MULTI_CELLS
        and bool(atomic_owner_rows)
        and set(row["ambient_dimension"] for row in atomic_owner_rows)
        == {0, 1, 2, 3}
        and all(
            row["owner_disposition"] == "EXCLUDED"
            for row in atomic_owner_rows
        )
        and [row["origin_key"] for row in origin_rows] == list(bundle.origin_keys)
        and [row["cell_key"] for row in multi_rows]
        == sorted(row["cell_key"] for row in multi_rows)
        and Counter(row["source_chart_id"] for row in multi_rows)
        == Counter({"W:N": 588, "W:S": 588})
        and Counter(
            row["frozen_owner_contact_audit"]["unique_strict_contact_chart"]
            for row in multi_rows
        ) == Counter({"N": 588, "S": 588})
        and lineage["Round176_prior_closed"] == EXPECTED_PRIOR_CLOSED
        and lineage["Round176_preclosed_frontier"] == EXPECTED_PRECLOSED_FRONTIER
        and lineage["Round176_residual_roots"] == EXPECTED_RESIDUAL_ROOTS
        and lineage["Round180_inherited_excluded"] == EXPECTED_INHERITED_TERMINALS
        and lineage["Round180_final"] == EXPECTED_FINAL_CELLS
        and lineage["sealed_C30a_clipped_excluded"] == EXPECTED_C30A_CLIPPED_CELLS
        and lineage["Round306C30D_multi_Delta_excluded"] == EXPECTED_MULTI_CELLS
        and all(row["whole_closed_cell_excluded"] is True for row in multi_rows)
        and all(
            row["whole_origin_disposition_candidate"] == "EXCLUDED"
            and row["whole_original_physical_origin_excluded_candidate"] is True
            for row in origin_rows
        ),
        "C30d independent 1176-cell/20-EXCLUDED census",
    )
    require(producer_module_absent(), "producer independence after reconstruction")
    return Reference(
        bundle.input_pins,
        bundle.c30c_authority,
        bundle.origin_keys,
        tuple(multi_rows),
        tuple(atomic_owner_rows),
        tuple(origin_rows),
    )


def canonical_rows(path: Path) -> list[dict[str, Any]]:
    return list(candidate_rows(path))


def ledger_descriptor(
    path: Path,
    rows: list[dict[str, Any]],
    order: str,
) -> dict[str, Any]:
    sequence = hashlib.sha256()
    for row in rows:
        sequence.update(bytes.fromhex(row["row_sha256"]))
    return {
        "filename": path.name,
        "row_count": len(rows),
        "size": path.stat().st_size,
        "sha256": file_hash(path),
        "row_sequence_sha256": sequence.hexdigest(),
        "order": order,
    }


def expected_result_body(
    input_pins: list[dict[str, str]],
    c30c_authority: dict[str, Any],
    origin_keys: list[str],
    cell_descriptor: dict[str, Any],
    owner_descriptor: dict[str, Any],
    origin_descriptor: dict[str, Any],
) -> dict[str, Any]:
    theorem = {
        "kind": (
            "SOURCE_W_20_MULTI_DELTA_WHOLE_ORIGIN_EXCLUSION_THEOREM_CANDIDATE"
        ),
        "origin_selection_dynamically_derived_from_pinned_R184_R215": True,
        "selected_origin_count": EXPECTED_ORIGINS,
        "selected_origin_keys_sha256": EXPECTED_ORIGIN_KEYS_SHA256,
        "sealed_C30a_clipped_cells_composed": EXPECTED_C30A_CLIPPED_CELLS,
        "new_multi_Delta_cells_closed": EXPECTED_MULTI_CELLS,
        "every_multi_Delta_cell_has_exactly_two_G_and_one_W_admissible_"
        "targets": True,
        "every_possible_G_first_target_is_owner_mismatch_excluded": True,
        "every_possible_W_first_target_is_N_or_S_outgoing_mismatch_excluded": True,
        "Delta_zero_Delta_intersection_and_root_tie_strata_included": True,
        "rank_aware_multi_graph_order_not_needed_for_this_exclusion": True,
        "every_origin_has_complete_3D_2D_1D_0D_half_open_owner_audit": True,
        "all_twenty_whole_original_physical_origins_excluded_candidate": True,
        "child_count_or_volume_used_as_whole_origin_credit": False,
    }
    return {
        "schema": (
            "cm2.round306c30d.source-w-multi-delta-whole-origin-exclusion."
            "candidate.v2"
        ),
        "status": (
            "PASS_CANDIDATE_ROUND306C30D_MULTI_DELTA_EXCLUSION__"
            "1176_CELLS__20_WHOLE_ORIGINS__ZERO_FORMAL_CREDIT"
        ),
        "input_pins": input_pins,
        "runtime": {
            "attestation_filename": RUNTIME_ATTESTATION,
            "attestation_sha256": RUNTIME_ATTESTATION_SHA256,
            "controlled_seed_contract": {
                "schema": "cm2.round306c30d.controlled-seed-runtime-contract.v1",
                "launcher_contract": (
                    "ENV_I_EXACT_4_VARIABLES__ABSOLUTE_PINNED_PYTHON_-P_-s_-B"
                ),
                "accepted_seeds": [30630071, 30630929],
                "sentinel": HASH_SEED_SENTINEL,
                "accepted_hash_fingerprints": {
                    key: HASH_FINGERPRINTS[key] for key in sorted(HASH_FINGERPRINTS)
                },
                "flags": {
                    "isolated": 0,
                    "ignore_environment": 0,
                    "safe_path": True,
                    "no_user_site": 1,
                    "dont_write_bytecode": 1,
                    "hash_randomization": 1,
                },
                "environment_keys": ["HOME", "LC_ALL", "PYTHONHASHSEED", "TZ"],
                "seed_specific_value_recorded_only_in_external_provenance": True,
                "current_seed_and_fingerprint_verified": True,
            },
        },
        "upstream_credit_boundary": {
            "formal_authority": "SEALED_C30C_78_STATE",
            "C30c_root_manifest_sha256": c30c_authority[
                "root_manifest_sha256"
            ],
            "C30c_verification_sha256": c30c_authority[
                "verification_sha256"
            ],
            "C30c_verification_object_sha256": c30c_authority[
                "verification_object_sha256"
            ],
            "C30c_sealed_member_map_sha256": c30c_authority[
                "sealed_member_map_sha256"
            ],
            "C30c_authority_pins_sha256": c30c_authority["pins_sha256"],
            "C30a_clipped_ledger_used_as_mathematical_evidence": True,
            "C30a_used_as_formal_ledger_baseline": False,
        },
        "scope": {
            "origin_count": EXPECTED_ORIGINS,
            "origin_keys": origin_keys,
            "origin_keys_sha256": EXPECTED_ORIGIN_KEYS_SHA256,
            "Round180_final_cell_count": EXPECTED_FINAL_CELLS,
            "sealed_C30a_clipped_cell_count": EXPECTED_C30A_CLIPPED_CELLS,
            "new_multi_Delta_cell_count": EXPECTED_MULTI_CELLS,
            "new_multi_Delta_cell_disposition_census": {
                "EXCLUDED": EXPECTED_MULTI_CELLS,
            },
            "whole_origin_disposition_census_candidate": {
                "EXCLUDED": EXPECTED_ORIGINS,
            },
        },
        "candidate_theorem": theorem,
        "candidate_theorem_sha256": digest(theorem),
        "proposed_source_W_transition_if_C30d_is_independently_sealed": {
            "before": {
                **SEALED_BASELINE,
                "remaining_partition": {
                    "multi_Delta": 20,
                    "reduced_live": 2,
                    "retained_source_seams": 2,
                    "compact_q": 54,
                },
            },
            "candidate_credits": {
                "whole_origin_exclusion": EXPECTED_ORIGINS,
                "resolved_origin_disposition": EXPECTED_ORIGINS,
            },
            "after": {
                "excluded": 74_766,
                "conservative_live": 2_066,
                "remaining": 58,
                "resolved_nonexcluded": 2_008,
                "total": 76_832,
                "remaining_partition": {
                    "reduced_live": 2,
                    "retained_source_seams": 2,
                    "compact_q": 54,
                },
            },
            "conservation_identity": "74766+2066=76832",
            "official_ledger_mutated": False,
        },
        "ledgers": {
            "multi_Delta_cell_candidate": cell_descriptor,
            "atomic_half_open_owner_candidate": owner_descriptor,
            "whole_origin_exclusion_candidate": origin_descriptor,
        },
        "formal_credit": {
            "multi_Delta_cell_dispositions": 0,
            "multi_Delta_whole_cell_exclusions": 0,
            "resolved_source_W_origin_dispositions": 0,
            "whole_source_W_origin_exclusions": 0,
        },
        "candidate_credit_if_independently_verified": {
            "multi_Delta_cell_dispositions": EXPECTED_MULTI_CELLS,
            "multi_Delta_whole_cell_exclusions": EXPECTED_MULTI_CELLS,
            "resolved_source_W_origin_dispositions": EXPECTED_ORIGINS,
            "whole_source_W_origin_exclusions": EXPECTED_ORIGINS,
        },
        "strict_nonpromotion": {
            "producer_only": True,
            "independent_verifier_present": False,
            "attack_harness_present": False,
            "dual_seed_replay_present": False,
            "cold_replay_present": False,
            "manifest_present": False,
            "sealed_directory_present": False,
            "official_source_W_transition": "UNCHANGED_FROM_SEALED_C30C_78_STATE",
            "D02": "BLOCKED_BY_78_REMAINING_SOURCE_W_ORIGINS_AND_COMPOSITE_GATE",
            "D03": "UNAUTHORIZED",
            "D04": "NOT_MINTED",
            "Gate5_filled_field_slots": "10/18",
            "Gate5_complete_global_blocks": 0,
            "CM2": "NO-GO_FOR_CLAIM",
        },
        "required_next": (
            "BUILD_INDEPENDENT_C30D_VERIFIER_ATTACK_HARNESS_DUAL_SEED_"
            "COLD_REPLAY_AND_MANIFEST_BEFORE_ANY_FORMAL_CREDIT"
        ),
    }


CELL_ZERO_FORMAL = {
    "multi_Delta_cell_disposition": 0,
    "whole_closed_cell_exclusion": 0,
    "whole_source_W_origin_exclusion": 0,
}
ORIGIN_ZERO_FORMAL = {
    "resolved_source_W_origin_disposition": 0,
    "whole_source_W_origin_exclusion": 0,
}
RESULT_ZERO_FORMAL = {
    "multi_Delta_cell_dispositions": 0,
    "multi_Delta_whole_cell_exclusions": 0,
    "resolved_source_W_origin_dispositions": 0,
    "whole_source_W_origin_exclusions": 0,
}


def validate_static_security_boundaries(
    result: dict[str, Any],
    cells: list[dict[str, Any]],
    origins: list[dict[str, Any]],
    reference: Reference,
) -> None:
    require(
        result.get("formal_credit") == RESULT_ZERO_FORMAL
        and all(row.get("formal_credit") == CELL_ZERO_FORMAL for row in cells)
        and all(row.get("formal_credit") == ORIGIN_ZERO_FORMAL for row in origins),
        "C30d zero formal credit boundary",
    )
    require(
        result.get("candidate_theorem", {}).get(
            "child_count_or_volume_used_as_whole_origin_credit"
        ) is False
        and all(
            row.get("child_count_or_volume_used_as_whole_origin_credit")
            in {None, False, 0}
            for row in origins
        ),
        "C30d child/volume credit boundary",
    )
    strict = result.get("strict_nonpromotion", {})
    require(
        strict.get("D02")
        == "BLOCKED_BY_78_REMAINING_SOURCE_W_ORIGINS_AND_COMPOSITE_GATE"
        and strict.get("D03") == "UNAUTHORIZED"
        and strict.get("D04") == "NOT_MINTED"
        and strict.get("CM2") == "NO-GO_FOR_CLAIM"
        and strict.get("manifest_present") is False
        and strict.get("sealed_directory_present") is False,
        "C30d strict nonpromotion boundary",
    )
    pins = [
        {"filename": filename, "sha256": sha256}
        for filename, sha256 in reference.input_pins
    ]
    require(result.get("input_pins") == pins, "C30d exact input pins")


def validate_cell_row(
    candidate: dict[str, Any], expected: dict[str, Any]
) -> None:
    key = expected["cell_key"]
    require(
        candidate.get("frozen_owner_contact_audit")
        == expected["frozen_owner_contact_audit"]
        and candidate.get("exhaustive_possible_first_target_rows")
        == expected["exhaustive_possible_first_target_rows"]
        and candidate.get("closed_enclosure_exclusion_theorem_candidate")
        == expected["closed_enclosure_exclusion_theorem_candidate"]
        and candidate == expected,
        "C30d independent universal-target cell:" + key,
    )


def validate_origin_row(
    candidate: dict[str, Any], expected: dict[str, Any]
) -> None:
    origin = expected["origin_key"]
    require(
        candidate.get("materialized_atomic_half_open_owner_ledger_slice")
        == expected["materialized_atomic_half_open_owner_ledger_slice"],
        "C30d independent 3D/2D/1D/0D owner closure:" + origin,
    )
    require(
        candidate.get("whole_origin_disposition_candidate") == "EXCLUDED"
        and candidate.get("whole_original_physical_origin_excluded_candidate")
        is True
        and candidate == expected,
        "C30d independent whole-origin EXCLUDED row:" + origin,
    )


def validate_result(
    result: dict[str, Any],
    candidate: Path,
    cells: list[dict[str, Any]],
    atomic_owners: list[dict[str, Any]],
    origins: list[dict[str, Any]],
    reference: Reference,
) -> None:
    cell_descriptor = ledger_descriptor(
        candidate / CELL_LEDGER,
        cells,
        "LEXICOGRAPHIC_ROUND180_FINAL_CELL_KEY",
    )
    owner_descriptor = ledger_descriptor(
        candidate / ATOMIC_OWNER_LEDGER,
        atomic_owners,
        "ORIGIN_KEY_THEN_DIMENSION_3_TO_0_THEN_LEAF_KEY_OR_CANONICAL_GEOMETRY",
    )
    origin_descriptor = ledger_descriptor(
        candidate / ORIGIN_LEDGER,
        origins,
        "LEXICOGRAPHIC_SOURCE_W_ORIGIN_KEY",
    )
    require(
        result.get("ledgers", {}).get("multi_Delta_cell_candidate")
        == cell_descriptor,
        "C30d ledger descriptor:" + CELL_LEDGER,
    )
    require(
        result.get("ledgers", {}).get("whole_origin_exclusion_candidate")
        == origin_descriptor,
        "C30d ledger descriptor:" + ORIGIN_LEDGER,
    )
    require(
        result.get("ledgers", {}).get("atomic_half_open_owner_candidate")
        == owner_descriptor,
        "C30d ledger descriptor:" + ATOMIC_OWNER_LEDGER,
    )
    pins = [
        {"filename": filename, "sha256": sha256}
        for filename, sha256 in reference.input_pins
    ]
    body = expected_result_body(
        pins,
        dict(reference.c30c_authority),
        list(reference.origin_keys),
        cell_descriptor,
        owner_descriptor,
        origin_descriptor,
    )
    require(
        result == {**body, "result_sha256": digest(body)},
        "C30d exact candidate-only result",
    )


def verify_candidate_dir(candidate: Path, reference: Reference) -> dict[str, Any]:
    require(producer_module_absent(), "producer independence before candidate")
    candidate = Path(os.path.abspath(os.fspath(candidate)))
    status = candidate.lstat()
    require(
        stat.S_ISDIR(status.st_mode) and not candidate.is_symlink(),
        "C30d candidate regular directory",
    )
    require(
        {path.name for path in candidate.iterdir()}
        == {
            RUNTIME_ATTESTATION,
            CELL_LEDGER,
            ATOMIC_OWNER_LEDGER,
            ORIGIN_LEDGER,
            RESULT,
        },
        "C30d candidate exact file set",
    )
    runtime_raw = regular_bytes(candidate / RUNTIME_ATTESTATION, 4 * 1024 * 1024)
    require(
        hashlib.sha256(runtime_raw).hexdigest() == RUNTIME_ATTESTATION_SHA256
        and runtime_raw == regular_bytes(ROOT / RUNTIME_ATTESTATION, 4 * 1024 * 1024),
        "C30d exact pinned runtime attestation",
    )
    cells = canonical_rows(candidate / CELL_LEDGER)
    atomic_owners = canonical_rows(candidate / ATOMIC_OWNER_LEDGER)
    origins = canonical_rows(candidate / ORIGIN_LEDGER)
    result_raw = regular_bytes(candidate / RESULT)
    result = strict_object_bytes(result_raw, RESULT)
    result_body = dict(result)
    claimed = result_body.pop("result_sha256", None)
    require(
        result_raw == wire(result)
        and type(claimed) is str
        and claimed == digest(result_body),
        "C30d candidate result closure",
    )
    require(
        len(cells) == EXPECTED_MULTI_CELLS
        and len(atomic_owners) == len(reference.expected_atomic_owners)
        and len(origins) == EXPECTED_ORIGINS
        and [row["cell_key"] for row in cells]
        == [row["cell_key"] for row in reference.expected_cells]
        and [row["origin_key"] for row in origins] == list(reference.origin_keys),
        "C30d candidate canonical row order/census",
    )
    validate_static_security_boundaries(result, cells, origins, reference)
    for candidate_row, expected_row in zip(
        cells, reference.expected_cells, strict=True
    ):
        validate_cell_row(candidate_row, expected_row)
    for candidate_row, expected_row in zip(
        atomic_owners, reference.expected_atomic_owners, strict=True
    ):
        require(
            candidate_row == expected_row
            and candidate_row.get("owner_disposition") == "EXCLUDED",
            "C30d independent materialized atomic owner row:"
            + expected_row["origin_key"],
        )
    for candidate_row, expected_row in zip(
        origins, reference.expected_origins, strict=True
    ):
        validate_origin_row(candidate_row, expected_row)
    validate_result(result, candidate, cells, atomic_owners, origins, reference)
    require(producer_module_absent(), "no producer imported or executed")
    return {
        "schema": (
            "cm2.round306c30d.source-w-multi-delta-whole-origin-exclusion."
            "independent-verification.candidate.v2"
        ),
        "status": (
            "PASS_INDEPENDENT_CANDIDATE_C30D__1176_UNIVERSAL_TARGET_"
            "MISMATCH_CELLS__20_EXCLUDED_ORIGINS__ZERO_FORMAL_CREDIT"
        ),
        "candidate_result_sha256": result["result_sha256"],
        "candidate_cell_ledger_sha256": file_hash(candidate / CELL_LEDGER),
        "candidate_atomic_owner_ledger_sha256": file_hash(
            candidate / ATOMIC_OWNER_LEDGER
        ),
        "candidate_origin_ledger_sha256": file_hash(candidate / ORIGIN_LEDGER),
        "dynamic_origin_census": EXPECTED_ORIGINS,
        "universal_target_mismatch_cell_census": EXPECTED_MULTI_CELLS,
        "strict_owner_closure_dimensions": [3, 2, 1, 0],
        "whole_origin_disposition_census": {"EXCLUDED": EXPECTED_ORIGINS},
        "formal_credit": RESULT_ZERO_FORMAL,
        "manifest_authorized": False,
        "candidate_producer_imported_or_executed": False,
        "official_source_W_transition": "UNCHANGED_FROM_SEALED_C30C_78_STATE",
        "D02": "BLOCKED_BY_78_REMAINING_SOURCE_W_ORIGINS_AND_COMPOSITE_GATE",
        "CM2": "NO-GO_FOR_CLAIM",
        "required_before_promotion": (
            "ATTACK_HARNESS_DUAL_SEED_COLD_REPLAY_AND_MANIFEST"
        ),
    }


def verify(candidate: Path) -> dict[str, Any]:
    return verify_candidate_dir(candidate, reconstruct_reference())


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("candidate", type=Path)
    arguments = parser.parse_args()
    try:
        output = verify(arguments.candidate)
    except (
        Reject,
        base.Reject,
        KeyError,
        OSError,
        ValueError,
        TypeError,
        AssertionError,
    ) as error:
        print(wire({
            "schema": (
                "cm2.round306c30d.source-w-multi-delta-whole-origin-"
                "exclusion.independent-verification.candidate.v2"
            ),
            "status": "FAIL_CLOSED",
            "formal_credit": RESULT_ZERO_FORMAL,
            "manifest_authorized": False,
            "error": str(error),
        }).decode("ascii"))
        return 1
    print(wire(output).decode("ascii"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
