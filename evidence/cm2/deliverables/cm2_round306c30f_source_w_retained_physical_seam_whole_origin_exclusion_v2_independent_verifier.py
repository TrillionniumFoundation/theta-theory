#!/usr/bin/env python3
"""No-producer-import verifier for the append-only C30f v2 candidate.

The verifier independently reconstructs the retained-seam theorem through the
immutable C30f v1 independent verifier, while separately executing and
recapturing the dynamically SHA-pinned C30e terminal adapter.  The C30f v2
producer is hashed as inert data and is never imported or executed.
"""
from __future__ import annotations

import argparse
import gzip
import hashlib
import importlib.util
import io
import json
import os
import stat
import subprocess
import sys
from collections import Counter
from pathlib import Path
from typing import Any, Iterable

sys.dont_write_bytecode = True


ROOT = Path(__file__).resolve().parent
PREFIX = (
    "cm2_round306c30f_source_w_retained_physical_seam_"
    "whole_origin_exclusion_v2"
)
CELL_LEDGER = PREFIX + "_target_cell_ledger.jsonl.gz"
SOURCE_STRATA_LEDGER = PREFIX + "_source_half_open_strata_ledger.jsonl.gz"
ORIGIN_LEDGER = PREFIX + "_whole_origin_ledger.jsonl.gz"
RESULT = PREFIX + "_result.json"
EXPECTED_FILES = {CELL_LEDGER, SOURCE_STRATA_LEDGER, ORIGIN_LEDGER, RESULT}
PRODUCER_SOURCE = PREFIX + "_producer.py"
PRODUCER_SOURCE_SHA256 = (
    "22e8e4ec8b03231f9310f61d4451b937aa5b4fa1e35410f2d56bc9e41c51eed1"
)
PRODUCER_MODULE_NAME = PRODUCER_SOURCE[:-3]

INDEPENDENT_MATH_SOURCE = (
    "cm2_round306c30f_source_w_retained_physical_seam_"
    "whole_origin_exclusion_independent_verifier.py"
)
INDEPENDENT_MATH_SOURCE_SHA256 = (
    "4feacbc45dda6ec68a326e62603f3af41dfc7cc58ed036128d30d5e802bbdae3"
)
LEGACY_PRODUCER_MODULE_NAME = (
    "cm2_round306c30f_source_w_retained_physical_seam_"
    "whole_origin_exclusion_producer"
)

C30E_PROJECTION_SCHEMA = (
    "cm2.round306c30f.c30e-terminal-predecessor-projection.v1"
)
C30E_PROJECTION_STATUS = (
    "PASS_EXACT_VERSIONED_C30E_TERMINAL_GRAPH_AS_C30F_PREDECESSOR__"
    "ZERO_C30F_FORMAL_CREDIT"
)
C30E_TERMINAL_MEMBERS = tuple(sorted((
    "chain_status.json",
    "evidence_bundle_receipt.json",
    "manifest_receipt.json",
    "outer_verification.json",
    "payload_manifest.sha256",
    "root_manifest.sha256",
    "terminal_replay.json",
    "terminal_seal_receipt.json",
)))
C30E_BEFORE = {
    "excluded": 74_766,
    "conservative_live": 2_066,
    "resolved_nonexcluded": 2_008,
    "remaining": 58,
    "total": 76_832,
    "remaining_partition": {
        "reduced_live": 2,
        "retained_source_seams": 2,
        "compact_q": 54,
    },
}
C30E_CREDIT = {
    "resolved_source_W_origin_dispositions": 2,
    "whole_source_W_origin_exclusions": 0,
    "resolved_nonexcluded": 2,
}
C30E_AFTER = {
    "excluded": 74_766,
    "conservative_live": 2_066,
    "resolved_nonexcluded": 2_010,
    "remaining": 56,
    "total": 76_832,
    "remaining_partition": {
        "retained_source_seams": 2,
        "compact_q": 54,
    },
}
C30F_AFTER = {
    "excluded": 74_768,
    "conservative_live": 2_064,
    "resolved_nonexcluded": 2_010,
    "remaining": 54,
    "total": 76_832,
    "remaining_partition": {"compact_q": 54},
}
C30F_CANDIDATE_CREDIT = {
    "resolved_source_W_origin_dispositions": 2,
    "whole_source_W_origin_exclusions": 2,
    "resolved_nonexcluded": 0,
}
C30F_ZERO_CREDIT = {
    "target_cell_dispositions": 0,
    "target_whole_cell_exclusions": 0,
    "source_half_open_stratum_dispositions": 0,
    "resolved_source_W_origin_dispositions": 0,
    "whole_source_W_origin_exclusions": 0,
    "resolved_nonexcluded": 0,
    "D02": 0,
    "D03": 0,
    "D04": 0,
    "Gate5": 0,
    "CM2": 0,
}

EXPECTED_ORIGINS = 2
EXPECTED_CELLS = 288
EXPECTED_STRATA = 994
EXPECTED_CELLS_PER_ORIGIN = 144
EXPECTED_R201_PER_ORIGIN = 72
EXPECTED_C30A_PER_ORIGIN = 72
EXPECTED_STRATA_PER_ORIGIN = 497

CONTROLLED_HASH_SEEDS = frozenset({"30630071", "30630929"})
CONTROLLED_ENVIRONMENT = {
    "HOME": "/nonexistent",
    "LC_ALL": "C.UTF-8",
    "TZ": "UTC",
}
HASH_SEED_SENTINEL = "CM2_C30F_HASH_SEED_SENTINEL_v2"
HASH_FINGERPRINTS = {
    "30630071": -3949014500883849868,
    "30630929": 276388808340754406,
}
INITIAL_SAFE_SYS_PATH = tuple(sys.path)


class C30FFailure(RuntimeError):
    """Predecessor/runtime failure, returned with exit code two."""


class VerificationFailure(RuntimeError):
    """Typed candidate rejection."""

    def __init__(self, reason: str, detail: str = "") -> None:
        super().__init__(reason + (":" + detail if detail else ""))
        self.reason = reason
        self.detail = detail


def need(condition: bool, label: str) -> None:
    if type(condition) is not bool or not condition:
        raise C30FFailure(label)


def vneed(condition: bool, reason: str, detail: str = "") -> None:
    if type(condition) is not bool or not condition:
        raise VerificationFailure(reason, detail)


def canonical(value: Any) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=True,
        allow_nan=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("ascii")


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def file_hash(path: Path) -> str:
    state = hashlib.sha256()
    with path.open("rb") as stream:
        while block := stream.read(1 << 20):
            state.update(block)
    return state.hexdigest()


def valid_sha256(value: Any) -> bool:
    return bool(
        type(value) is str
        and len(value) == 64
        and all(character in "0123456789abcdef" for character in value)
    )


def identity(value: os.stat_result) -> tuple[int, ...]:
    return (
        value.st_dev, value.st_ino, value.st_mode, value.st_nlink,
        value.st_uid, value.st_gid, value.st_size, value.st_mtime_ns,
        value.st_ctime_ns,
    )


def validate_runtime() -> None:
    environment = dict(os.environ)
    seed = environment.pop("PYTHONHASHSEED", None)
    need(
        bool(
            sys.flags.isolated == 0
            and sys.flags.ignore_environment == 0
            and sys.flags.safe_path is True
            and sys.flags.no_user_site == 1
            and sys.flags.dont_write_bytecode == 1
            and sys.flags.hash_randomization == 1
        ),
        "C30F_VERIFIER_REQUIRES_ENV_I_AND_PYTHON_P_S_B__PYTHON_I_FORBIDDEN",
    )
    need(
        bool(
            seed in CONTROLLED_HASH_SEEDS
            and environment == CONTROLLED_ENVIRONMENT
            and hash(HASH_SEED_SENTINEL) == HASH_FINGERPRINTS[seed]
        ),
        "C30F_VERIFIER_HASH_SEED_OR_ENVIRONMENT_MISMATCH",
    )
    need(
        bool(
            "" not in INITIAL_SAFE_SYS_PATH
            and os.fspath(ROOT) not in INITIAL_SAFE_SYS_PATH
        ),
        "C30F_VERIFIER_UNSAFE_INITIAL_MODULE_SEARCH_PATH",
    )


def capture_regular(path: Path, expected: str, maximum: int) -> bytes:
    try:
        before = path.lstat()
    except OSError as error:
        raise C30FFailure("C30E_TERMINAL_GRAPH_INCOMPLETE:" + path.name) from error
    need(
        bool(
            stat.S_ISREG(before.st_mode)
            and not path.is_symlink()
            and before.st_nlink == 1
            and 0 < before.st_size <= maximum
        ),
        "C30E_AUTHORITY_REGULAR_SINGLETON:" + path.name,
    )
    descriptor = os.open(
        path, os.O_RDONLY | os.O_CLOEXEC | getattr(os, "O_NOFOLLOW", 0)
    )
    try:
        opened = os.fstat(descriptor)
        need(identity(opened) == identity(before), "C30E_AUTHORITY_OPEN_RACE")
        chunks: list[bytes] = []
        while block := os.read(descriptor, 1 << 20):
            chunks.append(block)
        closed = os.fstat(descriptor)
    finally:
        os.close(descriptor)
    raw = b"".join(chunks)
    need(
        bool(
            identity(opened) == identity(closed) == identity(path.lstat())
            and len(raw) == opened.st_size
            and hashlib.sha256(raw).hexdigest() == expected
        ),
        "C30E_AUTHORITY_CAPTURE_OR_HASH:" + path.name,
    )
    return raw


def strict_object(raw: bytes, label: str) -> dict[str, Any]:
    def pairs(values: list[tuple[str, Any]]) -> dict[str, Any]:
        output: dict[str, Any] = {}
        for key, value in values:
            need(bool(type(key) is str and key not in output),
                 "UNIQUE_JSON_KEYS:" + label)
            output[key] = value
        return output

    try:
        value = json.loads(raw.decode("utf-8", "strict"), object_pairs_hook=pairs)
    except (UnicodeError, json.JSONDecodeError) as error:
        raise C30FFailure("CANONICAL_JSON_OBJECT:" + label) from error
    need(bool(type(value) is dict and canonical(value) == raw),
         "CANONICAL_JSON_OBJECT:" + label)
    return value


def validate_projection(
    value: dict[str, Any], chain: Path, pins_sha256: str
) -> dict[str, str]:
    body = dict(value)
    projection_sha256 = body.pop("projection_sha256", None)
    need(
        bool(
            set(value) == {
                "schema", "status", "authority", "formal_handoff",
                "release_boundary", "projection_sha256",
            }
            and projection_sha256 == digest(body)
            and value.get("schema") == C30E_PROJECTION_SCHEMA
            and value.get("status") == C30E_PROJECTION_STATUS
        ),
        "C30E_ADAPTER_EXACT_PROJECTION_SCHEMA_STATUS_CLOSURE",
    )
    authority = value.get("authority")
    need(type(authority) is dict, "C30E_PROJECTION_AUTHORITY_OBJECT")
    assert type(authority) is dict
    members = authority.get("required_members_sha256")
    need(
        bool(
            set(authority) == {
                "adapter_contract", "chain_dir_basename",
                "dynamic_pins_sha256", "required_members_sha256",
                "payload_manifest_member_count", "root_manifest_member_count",
                "root_binds_payload_manifest", "root_binds_outer_verification",
                "payload_all_members_verified", "all_receipt_object_hashes_closed",
                "terminal_seal_exact_pass", "terminal_replay_exact_pass",
                "chain_status_exact_pass",
            }
            and authority.get("adapter_contract")
            == "DIRECT_VERSIONED_C30E_TERMINAL_GRAPH__NO_LEGACY_ALIAS"
            and authority.get("chain_dir_basename") == chain.name
            and authority.get("dynamic_pins_sha256") == pins_sha256
            and type(members) is dict
            and set(members) == set(C30E_TERMINAL_MEMBERS)
            and all(valid_sha256(item) for item in members.values())
            and type(authority.get("payload_manifest_member_count")) is int
            and authority["payload_manifest_member_count"] > 0
            and authority.get("root_manifest_member_count") == 2
            and authority.get("root_binds_payload_manifest") is True
            and authority.get("root_binds_outer_verification") is True
            and authority.get("payload_all_members_verified") is True
            and authority.get("all_receipt_object_hashes_closed") is True
            and authority.get("terminal_seal_exact_pass") is True
            and authority.get("terminal_replay_exact_pass") is True
            and authority.get("chain_status_exact_pass") is True
        ),
        "C30E_ADAPTER_EXACT_TERMINAL_GRAPH_CLOSURE",
    )
    need(
        value.get("formal_handoff") == {
            "before": C30E_BEFORE,
            "credit": C30E_CREDIT,
            "after": C30E_AFTER,
            "transition_status": "PASS_FORMAL_C30E_TERMINAL__58_TO_56_AUTHORIZED",
            "terminal_replay_authorizes_transition": True,
        },
        "C30E_EXACT_TERMINAL_58_TO_56_HANDOFF",
    )
    need(
        value.get("release_boundary") == {
            "C30e_formal_terminal_pass": True,
            "C30f_candidate_created": False,
            "C30f_manifest_created": False,
            "C30f_terminal_created": False,
            "source_W_formal_remainder": 56,
            "source_W_transition_authorized_by_this_projection": False,
            "formal_credit": C30F_ZERO_CREDIT,
            "D02": "BLOCKED_COMPOSITE",
            "D03": "UNAUTHORIZED",
            "D04": "NOT_MINTED",
            "Gate5": "10/18",
            "CM2": "NO-GO_FOR_CLAIM",
        },
        "C30E_PROJECTION_EXACT_C30F_ZERO_CREDIT_BOUNDARY",
    )
    assert type(members) is dict
    return {name: members[name] for name in sorted(members)}


def capture_c30e_authority(
    adapter_path: Path,
    adapter_sha256: str,
    chain_path: Path,
    pins_path: Path,
    pins_sha256: str,
) -> dict[str, Any]:
    need(bool(valid_sha256(adapter_sha256) and valid_sha256(pins_sha256)),
         "WELL_FORMED_DYNAMIC_C30E_ADAPTER_AND_PINS_SHA256")
    adapter = Path(os.path.abspath(os.fspath(adapter_path)))
    chain = Path(os.path.abspath(os.fspath(chain_path)))
    pins = Path(os.path.abspath(os.fspath(pins_path)))
    capture_regular(adapter, adapter_sha256, 8 << 20)
    capture_regular(pins, pins_sha256, 4 << 20)
    try:
        directory_before = chain.lstat()
    except OSError as error:
        raise C30FFailure("C30E_TERMINAL_GRAPH_INCOMPLETE:chain directory") from error
    need(bool(stat.S_ISDIR(directory_before.st_mode) and not chain.is_symlink()),
         "C30E_TERMINAL_GRAPH_INCOMPLETE:chain directory")
    for name in C30E_TERMINAL_MEMBERS:
        path = chain / name
        try:
            item = path.lstat()
        except OSError as error:
            raise C30FFailure("C30E_TERMINAL_GRAPH_INCOMPLETE:" + name) from error
        need(bool(stat.S_ISREG(item.st_mode) and not path.is_symlink()),
             "C30E_TERMINAL_GRAPH_INCOMPLETE:" + name)
    completed = subprocess.run(
        [
            sys.executable, "-I", "-P", "-s", "-B", os.fspath(adapter),
            "--chain-dir", os.fspath(chain),
            "--dynamic-pins", os.fspath(pins),
        ],
        stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        env={
            "HOME": "/nonexistent", "LC_ALL": "C.UTF-8", "TZ": "UTC",
            "PYTHONHASHSEED": "0",
        },
        timeout=600,
        check=False,
    )
    need(
        bool(
            completed.returncode == 0
            and completed.stderr == b""
            and 0 < len(completed.stdout) <= 4 << 20
        ),
        "C30E_ADAPTER_EXIT_STDERR_STDOUT_CONTRACT",
    )
    projection = strict_object(completed.stdout, "C30E_ADAPTER_PROJECTION")
    member_sha256 = validate_projection(projection, chain, pins_sha256)
    facts: dict[str, dict[str, Any]] = {}
    for name in C30E_TERMINAL_MEMBERS:
        raw = capture_regular(chain / name, member_sha256[name], 64 << 20)
        facts[name] = {"sha256": hashlib.sha256(raw).hexdigest(), "size": len(raw)}
    need(identity(directory_before) == identity(chain.lstat()),
         "C30E_TERMINAL_DIRECTORY_CHANGED_DURING_CAPTURE")
    pin_map = {
        "external-adapter:" + adapter.name: adapter_sha256,
        "dynamic-pins:" + pins.name: pins_sha256,
        **{
            "c30e-terminal:" + name: member_sha256[name]
            for name in C30E_TERMINAL_MEMBERS
        },
    }
    binding = {
        "adapter_sha256": adapter_sha256,
        "dynamic_pins_sha256": pins_sha256,
        "chain_dir_basename": chain.name,
        "projection_sha256": projection["projection_sha256"],
        "terminal_replay_sha256": member_sha256["terminal_replay.json"],
        "root_manifest_sha256": member_sha256["root_manifest.sha256"],
        "payload_manifest_sha256": member_sha256["payload_manifest.sha256"],
        "outer_verification_sha256": member_sha256["outer_verification.json"],
        "chain_status_sha256": member_sha256["chain_status.json"],
    }
    return {
        "pins": pin_map,
        "pins_sha256": digest([
            {"filename": name, "sha256": value}
            for name, value in sorted(pin_map.items())
        ]),
        "binding": binding,
        "binding_sha256": digest(binding),
        "terminal_member_facts": facts,
        "formal_before": C30E_BEFORE,
        "predecessor_credit": C30E_CREDIT,
        "formal_after": C30E_AFTER,
    }


def validate_inert_producer() -> None:
    need(
        bool(
            valid_sha256(PRODUCER_SOURCE_SHA256)
            and PRODUCER_MODULE_NAME not in sys.modules
        ),
        "C30F_V2_PRODUCER_PIN_OR_IMPORT",
    )
    raw = capture_regular(ROOT / PRODUCER_SOURCE, PRODUCER_SOURCE_SHA256, 8 << 20)
    need(
        bool(
            hashlib.sha256(raw).hexdigest() == PRODUCER_SOURCE_SHA256
            and PRODUCER_MODULE_NAME not in sys.modules
        ),
        "C30F_V2_PRODUCER_MUST_REMAIN_INERT",
    )


def import_independent_math() -> Any:
    path = ROOT / INDEPENDENT_MATH_SOURCE
    capture_regular(path, INDEPENDENT_MATH_SOURCE_SHA256, 8 << 20)
    module_name = INDEPENDENT_MATH_SOURCE[:-3]
    need(
        bool(
            module_name not in sys.modules
            and PRODUCER_MODULE_NAME not in sys.modules
            and LEGACY_PRODUCER_MODULE_NAME not in sys.modules
        ),
        "C30F_INDEPENDENT_MATH_NOT_PRELOADED",
    )
    specification = importlib.util.spec_from_file_location(module_name, path)
    need(bool(specification is not None and specification.loader is not None),
         "C30F_INDEPENDENT_MATH_IMPORT_SPECIFICATION")
    module = importlib.util.module_from_spec(specification)
    sys.modules[module_name] = module
    try:
        specification.loader.exec_module(module)
    except BaseException:
        sys.modules.pop(module_name, None)
        raise
    need(
        bool(
            Path(module.__file__).resolve(strict=True) == path.resolve(strict=True)
            and file_hash(path) == INDEPENDENT_MATH_SOURCE_SHA256
            and PRODUCER_MODULE_NAME not in sys.modules
            and LEGACY_PRODUCER_MODULE_NAME not in sys.modules
        ),
        "C30F_INDEPENDENT_MATH_IDENTITY_AND_NO_PRODUCER_IMPORT",
    )
    return module


def zero_credit_objects(value: Any) -> Iterable[dict[str, Any]]:
    if type(value) is dict:
        for key, child in value.items():
            if key == "formal_credit":
                vneed(type(child) is dict, "ZERO_FORMAL_CREDIT_REQUIRED")
                assert type(child) is dict
                yield child
            yield from zero_credit_objects(child)
    elif type(value) is list:
        for child in value:
            yield from zero_credit_objects(child)


def bind_rows(rows: list[dict[str, Any]], authority: dict[str, Any]) -> list[dict[str, Any]]:
    binding = {
        "kind": "EXACT_C30E_TERMINAL_PREDECESSOR_BINDING",
        "binding_sha256": authority["binding_sha256"],
        **authority["binding"],
    }
    output: list[dict[str, Any]] = []
    for row in rows:
        body = {key: value for key, value in row.items() if key != "row_sha256"}
        body["c30e_terminal_predecessor"] = binding
        output.append({**body, "row_sha256": digest(body)})
    return output


def reconstruct_reference(authority: dict[str, Any]) -> dict[str, Any]:
    module = import_independent_math()
    module.validate_inert_producer_pin()
    module.ctx.prec = 192
    module.c30a.validate_runtime()
    inputs = module.validate_and_select_scope()
    raw_origins: list[dict[str, Any]] = []
    raw_cells: list[dict[str, Any]] = []
    raw_strata: list[dict[str, Any]] = []
    for ordinal, origin in enumerate(inputs["origin_keys"]):
        origin_row, cells_for_origin, strata_for_origin = module.build_origin(
            ordinal,
            len(raw_cells),
            origin,
            inputs["registry"][origin],
            inputs["retained_by_origin"][origin],
        )
        raw_origins.append(origin_row)
        raw_cells.extend(cells_for_origin)
        raw_strata.extend(strata_for_origin)
    raw_origins.sort(key=lambda row: row["origin_key"])
    raw_cells.sort(key=lambda row: row["cell_key"])
    raw_strata.sort(key=lambda row: (row["origin_key"], row["stratum_id"]))
    cells = bind_rows(raw_cells, authority)
    strata = bind_rows(raw_strata, authority)
    origins = bind_rows(raw_origins, authority)
    vneed(
        bool(len(cells) == EXPECTED_CELLS and len(strata) == EXPECTED_STRATA
             and len(origins) == EXPECTED_ORIGINS),
        "REFERENCE_RECONSTRUCTION_FAILURE",
        "global census",
    )
    origin_keys = sorted(row["origin_key"] for row in origins)
    for origin in origin_keys:
        kinds = Counter(
            row["source_kind"] for row in cells if row["origin_key"] == origin
        )
        vneed(
            bool(
                sum(kinds.values()) == EXPECTED_CELLS_PER_ORIGIN
                and kinds["PINNED_ROUND201_EXACT_BEHIND_EXCLUDED"]
                == EXPECTED_R201_PER_ORIGIN
                and kinds["SEALED_C30A_REDUCED_CLIPPED_KERNEL_REPLAY"]
                == EXPECTED_C30A_PER_ORIGIN
                and sum(1 for row in strata if row["origin_key"] == origin)
                == EXPECTED_STRATA_PER_ORIGIN
            ),
            "REFERENCE_RECONSTRUCTION_FAILURE",
            "per-origin census",
        )
    return {
        "cells": cells,
        "strata": strata,
        "origins": origins,
        "origin_keys": origin_keys,
        "legacy_input_pins": inputs["input_pins"],
        "mathematics_reconstruction_sha256": digest({
            "cells": raw_cells, "strata": raw_strata, "origins": raw_origins,
        }),
    }


def candidate_regular(path: Path, maximum: int) -> bytes:
    try:
        before = path.lstat()
    except OSError as error:
        raise VerificationFailure("CANDIDATE_FORMAT_VIOLATION", path.name) from error
    vneed(
        bool(
            stat.S_ISREG(before.st_mode)
            and not path.is_symlink()
            and before.st_nlink == 1
            and 0 < before.st_size <= maximum
        ),
        "CANDIDATE_FORMAT_VIOLATION",
        "regular-singleton:" + path.name,
    )
    descriptor = os.open(
        path, os.O_RDONLY | os.O_CLOEXEC | getattr(os, "O_NOFOLLOW", 0)
    )
    try:
        opened = os.fstat(descriptor)
        vneed(identity(opened) == identity(before), "CANDIDATE_FORMAT_VIOLATION", "open-race")
        chunks: list[bytes] = []
        while block := os.read(descriptor, 1 << 20):
            chunks.append(block)
        closed = os.fstat(descriptor)
    finally:
        os.close(descriptor)
    raw = b"".join(chunks)
    vneed(
        bool(identity(opened) == identity(closed) == identity(path.lstat())
             and len(raw) == opened.st_size),
        "CANDIDATE_FORMAT_VIOLATION",
        "capture-race:" + path.name,
    )
    return raw


def read_ledger(candidate: Path, filename: str, expected: int) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    raw = candidate_regular(candidate / filename, 256 << 20)
    try:
        unpacked = gzip.decompress(raw)
    except (OSError, EOFError) as error:
        raise VerificationFailure("CANDIDATE_FORMAT_VIOLATION", "gzip:" + filename) from error
    lines = unpacked.splitlines(keepends=True)
    vneed(
        bool(len(lines) == expected and all(line.endswith(b"\n") for line in lines)),
        "CANDIDATE_FORMAT_VIOLATION",
        "row-count-or-framing:" + filename,
    )
    rows: list[dict[str, Any]] = []
    sequence = hashlib.sha256()
    for ordinal, line in enumerate(lines):
        try:
            row = json.loads(line[:-1].decode("ascii"))
        except (UnicodeError, json.JSONDecodeError) as error:
            raise VerificationFailure("CANDIDATE_FORMAT_VIOLATION", filename) from error
        vneed(
            bool(
                type(row) is dict
                and canonical(row) == line[:-1]
                and valid_sha256(row.get("row_sha256"))
                and row["row_sha256"] == digest({
                    key: value for key, value in row.items()
                    if key != "row_sha256"
                })
            ),
            "CANDIDATE_FORMAT_VIOLATION",
            filename + ":" + str(ordinal),
        )
        sequence.update(bytes.fromhex(row["row_sha256"]))
        rows.append(row)
    output = io.BytesIO()
    with gzip.GzipFile(filename="", mode="wb", compresslevel=9, fileobj=output, mtime=0) as stream:
        for row in rows:
            stream.write(canonical(row) + b"\n")
    vneed(output.getvalue() == raw, "CANDIDATE_FORMAT_VIOLATION", "gzip-canonical:" + filename)
    return rows, {
        "filename": filename,
        "row_count": len(rows),
        "row_sequence_sha256": sequence.hexdigest(),
        "sha256": hashlib.sha256(raw).hexdigest(),
        "size": len(raw),
    }


def make_result(
    math: dict[str, Any], authority: dict[str, Any], descriptors: dict[str, dict[str, Any]]
) -> dict[str, Any]:
    theorem = {
        "kind": "SOURCE_W_TWO_RETAINED_PHYSICAL_SEAMS_COMPLETE_EXCLUSION_THEOREM_CANDIDATE_V2",
        "origins_dynamically_discovered_from_pinned_Round212": True,
        "origin_count": EXPECTED_ORIGINS,
        "origin_keys_sha256": digest(math["origin_keys"]),
        "target_cells_per_origin": EXPECTED_CELLS_PER_ORIGIN,
        "Round201_exact_behind_exclusions_per_origin": EXPECTED_R201_PER_ORIGIN,
        "C30a_clipped_kernel_exclusions_per_origin": EXPECTED_C30A_PER_ORIGIN,
        "source_atomic_strata_per_origin": EXPECTED_STRATA_PER_ORIGIN,
        "complete_3D_2D_1D_0D_half_open_ownership": True,
        "both_whole_origins_excluded_candidate": True,
        "child_stratum_count_or_volume_used_as_integer_credit": False,
    }
    body = {
        "schema": "cm2.round306c30f.source-w-retained-physical-seam-whole-origin-exclusion.candidate.v2",
        "status": "PASS_CANDIDATE_C30F_V2__C30E_TERMINAL_BOUND__2_WHOLE_ORIGINS_EXCLUDED__ZERO_FORMAL_CREDIT",
        "mathematics_witness": {
            "source": (
                "cm2_round306c30f_source_w_retained_physical_seam_"
                "whole_origin_exclusion_producer.py"
            ),
            "source_sha256": "3775d481ea5893a2641683ac3d9e8785cf706abd6df4b7861b9162b90b522f8f",
            "independent_reconstruction_target_sha256": math["mathematics_reconstruction_sha256"],
            "legacy_input_pins": math["legacy_input_pins"],
            "used_as_mathematics_only_not_ledger_authority": True,
        },
        "c30e_terminal_authority": authority,
        "dynamic_scope": {
            "selection_uses_hardcoded_origin_keys": False,
            "origin_count": EXPECTED_ORIGINS,
            "origin_keys": math["origin_keys"],
            "origin_keys_sha256": digest(math["origin_keys"]),
        },
        "candidate_theorem": theorem,
        "candidate_theorem_sha256": digest(theorem),
        "census": {
            "target_cells": EXPECTED_CELLS,
            "source_atomic_strata": EXPECTED_STRATA,
            "whole_origins": EXPECTED_ORIGINS,
            "whole_origin_disposition": {"EXCLUDED": EXPECTED_ORIGINS},
        },
        "source_W_handoff_candidate": {
            "before": C30E_AFTER,
            "candidate_credit": C30F_CANDIDATE_CREDIT,
            "after_if_later_terminal_release_passes": C30F_AFTER,
            "transition_status": "UNAUTHORIZED_PENDING_C30F_RELEASE_TERMINAL",
            "terminal_replay_authorizes_transition": False,
            "official_ledger_mutated": False,
        },
        "ledgers": {
            "target_cell_candidate": {**descriptors[CELL_LEDGER], "order": "LEXICOGRAPHIC_ROUND180_FINAL_CELL_KEY"},
            "source_half_open_strata_candidate": {**descriptors[SOURCE_STRATA_LEDGER], "order": "LEXICOGRAPHIC_ORIGIN_KEY_THEN_SOURCE_STRATUM_ID"},
            "whole_origin_exclusion_candidate": {**descriptors[ORIGIN_LEDGER], "order": "LEXICOGRAPHIC_SOURCE_W_ORIGIN_KEY"},
        },
        "formal_credit": C30F_ZERO_CREDIT,
        "strict_nonpromotion": {
            "candidate_only": True,
            "dual_seed_process_attestations_present": False,
            "independent_verifier_release_receipt_present": False,
            "coherent_attack_release_receipt_present": False,
            "cold_TOCTOU_replay_present": False,
            "evidence_bundle_present": False,
            "payload_manifest_present": False,
            "root_manifest_present": False,
            "outer_verifier_present": False,
            "terminal_seal_present": False,
            "terminal_byte_replay_present": False,
            "official_source_W_state": "C30E_TERMINAL_56_BOUND__C30F_NOT_APPLIED",
            "D02": "BLOCKED_COMPOSITE",
            "D03": "UNAUTHORIZED",
            "D04": "NOT_MINTED",
            "Gate5": "10/18",
            "Gate5_complete_global_blocks": 0,
            "CM2": "NO-GO_FOR_CLAIM",
        },
        "required_next": "DUAL_REAL_SEED_FRESH_RUN__NO_IMPORT_VERIFIER__ATTACKS__COLD_TOCTOU__MANIFESTS__OUTER__TERMINAL_BYTE_REPLAY",
    }
    return {**body, "result_sha256": digest(body)}


def verify_candidate_dir(
    candidate_path: Path,
    authority: dict[str, Any],
    reference: dict[str, Any] | None = None,
) -> dict[str, Any]:
    validate_inert_producer()
    reference = reconstruct_reference(authority) if reference is None else reference
    candidate = Path(os.path.abspath(os.fspath(candidate_path)))
    try:
        status = candidate.lstat()
        names = {path.name for path in candidate.iterdir()}
    except OSError as error:
        raise VerificationFailure("CANDIDATE_FORMAT_VIOLATION", "candidate directory") from error
    vneed(
        bool(stat.S_ISDIR(status.st_mode) and not candidate.is_symlink()
             and names == EXPECTED_FILES),
        "CANDIDATE_FORMAT_VIOLATION",
        "exact file set",
    )
    cells, cell_descriptor = read_ledger(candidate, CELL_LEDGER, EXPECTED_CELLS)
    strata, strata_descriptor = read_ledger(candidate, SOURCE_STRATA_LEDGER, EXPECTED_STRATA)
    origins, origin_descriptor = read_ledger(candidate, ORIGIN_LEDGER, EXPECTED_ORIGINS)
    result_raw = candidate_regular(candidate / RESULT, 32 << 20)
    try:
        result = json.loads(result_raw.decode("ascii"))
    except (UnicodeError, json.JSONDecodeError) as error:
        raise VerificationFailure("CANDIDATE_FORMAT_VIOLATION", RESULT) from error
    vneed(
        bool(type(result) is dict and canonical(result) == result_raw
             and valid_sha256(result.get("result_sha256"))
             and result["result_sha256"] == digest({
                 key: value for key, value in result.items()
                 if key != "result_sha256"
             })),
        "CANDIDATE_FORMAT_VIOLATION",
        "result closure",
    )
    vneed(result.get("c30e_terminal_authority") == authority,
          "PREDECESSOR_AUTHORITY_MISMATCH")
    for value in (cells, strata, origins, result):
        for credit in zero_credit_objects(value):
            vneed(
                bool(credit and all(type(item) is int and item == 0
                                    for item in credit.values())),
                "ZERO_FORMAL_CREDIT_REQUIRED",
            )
    vneed(cells == reference["cells"], "TARGET_CELL_RECONSTRUCTION_MISMATCH")
    vneed(strata == reference["strata"], "SOURCE_STRATA_RECONSTRUCTION_MISMATCH")
    vneed(origins == reference["origins"], "ORIGIN_RECONSTRUCTION_MISMATCH")
    descriptors = {
        CELL_LEDGER: cell_descriptor,
        SOURCE_STRATA_LEDGER: strata_descriptor,
        ORIGIN_LEDGER: origin_descriptor,
    }
    expected = make_result(reference, authority, descriptors)
    vneed(result == expected, "RESULT_RECONSTRUCTION_MISMATCH")
    vneed(
        bool(
            result["source_W_handoff_candidate"]["before"] == C30E_AFTER
            and result["source_W_handoff_candidate"]["after_if_later_terminal_release_passes"] == C30F_AFTER
            and result["source_W_handoff_candidate"]["terminal_replay_authorizes_transition"] is False
            and result["strict_nonpromotion"]["D02"] == "BLOCKED_COMPOSITE"
            and result["strict_nonpromotion"]["D03"] == "UNAUTHORIZED"
            and result["strict_nonpromotion"]["D04"] == "NOT_MINTED"
            and result["strict_nonpromotion"]["Gate5"] == "10/18"
            and result["strict_nonpromotion"]["CM2"] == "NO-GO_FOR_CLAIM"
        ),
        "STRICT_NONPROMOTION_MISMATCH",
    )
    report_body = {
        "schema": "cm2.round306c30f.retained-physical-seam.independent-verification.report.v2",
        "status": "PASS_INDEPENDENT_C30F_V2__C30E_TERMINAL_BOUND__288_TARGETS__994_SOURCE_STRATA__2_EXCLUDED_CANDIDATES__ZERO_FORMAL_CREDIT",
        "candidate_result_sha256": result["result_sha256"],
        "producer_source": {
            "filename": PRODUCER_SOURCE,
            "sha256": PRODUCER_SOURCE_SHA256,
            "read_as_inert_bytes_only": True,
            "imported_or_executed": False,
        },
        "independent_math_source": {
            "filename": INDEPENDENT_MATH_SOURCE,
            "sha256": INDEPENDENT_MATH_SOURCE_SHA256,
            "legacy_producer_imported_or_executed": False,
        },
        "c30e_authority_binding_sha256": authority["binding_sha256"],
        "census": {"target_cells": 288, "source_atomic_strata": 994, "whole_origins": 2},
        "formal_credit": {
            "verified_target_cells": 0,
            "verified_source_atomic_strata": 0,
            "verified_whole_origin_exclusions": 0,
            "D02": 0, "D03": 0, "D04": 0, "Gate5": 0, "CM2": 0,
        },
        "artifacts_written": 0,
    }
    return {**report_body, "report_sha256": digest(report_body)}


def verify(
    candidate: Path,
    adapter: Path,
    adapter_sha256: str,
    chain: Path,
    pins: Path,
    pins_sha256: str,
) -> dict[str, Any]:
    validate_runtime()
    authority = capture_c30e_authority(
        adapter, adapter_sha256, chain, pins, pins_sha256
    )
    return verify_candidate_dir(candidate, authority)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--candidate-dir", required=True, type=Path)
    parser.add_argument("--predecessor-adapter", required=True, type=Path)
    parser.add_argument("--predecessor-adapter-sha256", required=True)
    parser.add_argument("--predecessor-chain-dir", required=True, type=Path)
    parser.add_argument("--predecessor-pins", required=True, type=Path)
    parser.add_argument("--predecessor-pins-sha256", required=True)
    arguments = parser.parse_args()
    try:
        report = verify(
            arguments.candidate_dir,
            arguments.predecessor_adapter,
            arguments.predecessor_adapter_sha256,
            arguments.predecessor_chain_dir,
            arguments.predecessor_pins,
            arguments.predecessor_pins_sha256,
        )
    except C30FFailure as error:
        os.write(2, canonical({
            "status": "REJECT", "reason": "PREDECESSOR_OR_RUNTIME_REJECT",
            "detail": str(error), "formal_credit": C30F_ZERO_CREDIT,
        }))
        return 2
    except VerificationFailure as error:
        os.write(2, canonical({
            "status": "REJECT", "reason": error.reason,
            "detail": error.detail, "formal_credit": C30F_ZERO_CREDIT,
        }))
        return 1
    except (OSError, ValueError, KeyError, subprocess.SubprocessError) as error:
        os.write(2, canonical({
            "status": "REJECT", "reason": type(error).__name__,
            "detail": str(error), "formal_credit": C30F_ZERO_CREDIT,
        }))
        return 2
    os.write(1, canonical(report))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
