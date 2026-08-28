#!/usr/bin/env python3
"""Append-only C30d-v3 candidate producer.

This program reuses the frozen C30d mathematical kernel, but replaces its
development-only predecessor reader with the C30c v5/v6 terminal plus
consolidated-formal-ledger adapter.  It creates only a zero-credit mathematical candidate.  It does not
mint a manifest, seal, terminal receipt, or the proposed 78 -> 58 transition.

The C30c authority is checked before the mathematical kernel is imported and
again after reconstruction.  Therefore a missing/incomplete C30c terminal
returns exit 2 with empty stdout/stderr and creates no candidate directory.
"""
from __future__ import annotations

import argparse
import ast
import gzip
import hashlib
import importlib.util
import json
import os
import stat
import subprocess
import sys
from collections import Counter
from pathlib import Path
from types import ModuleType
from typing import Any, Iterable

sys.dont_write_bytecode = True

DELIVERABLES = Path(__file__).resolve().parent
WORKSPACE = DELIVERABLES.parent
PYTHON = Path("/usr/bin/python3")

PREFIX = "cm2_round306c30d_source_w_multi_delta_whole_origin_exclusion_v3"
CELL_LEDGER = PREFIX + "_multi_delta_cell_ledger.jsonl.gz"
ATOMIC_OWNER_LEDGER = PREFIX + "_atomic_half_open_owner_ledger.jsonl.gz"
ORIGIN_LEDGER = PREFIX + "_whole_origin_ledger.jsonl.gz"
RESULT = PREFIX + "_result.json"
RUNTIME_ATTESTATION_REL = (
    "deliverables/cm2_round306c30b_sealed/"
    "cm2_round306c30b_python_flint_runtime_attestation.json"
)
RUNTIME_ATTESTATION_NAME = "cm2_round306c30b_python_flint_runtime_attestation.json"
RUNTIME_ATTESTATION_SHA256 = (
    "6b48cd0ca3fd53f9fdd457cc3c1106055e12db4d4ad999fcfd1fc89ad36b95df"
)

AUTHORITY_ADAPTER_REL = (
    "deliverables/cm2_round306c30d_c30c_v3_predecessor_authority_adapter_v1.py"
)
AUTHORITY_ADAPTER_SHA256 = (
    "f10613b8698997c99d3cece4f301cc89ea9f532f2d23c9d08325ef150b578503"
)
AUTHORITY_SCHEMA = "cm2.round306c30d.c30c-v5-v6-formal-predecessor-projection.v1"
AUTHORITY_STATUS = (
    "PASS_EXACT_C30C_V5_V6_TERMINAL_AND_FORMAL_LEDGER_AS_C30D_PREDECESSOR__"
    "ZERO_C30D_FORMAL_CREDIT"
)
C30C_RESULT_PREFIX = (
    "cm2_round306c30c_source_w_full_delta_whole_origin_disposition"
)
C30C_RESULT_REL = (
    ".cm2-runtime/candidates/c30c-v4-seed-30630071/"
    + C30C_RESULT_PREFIX
    + "_result.json"
)
C30C_RESULT_OBJECT_SHA256 = (
    "df4531942e743389f5e8f85b2d013132f0808f562c21f430e7904577d67087d4"
)
C30C_ORIGIN_KEYS_SHA256 = (
    "a928d0328e94ca98f04a0ee5d5d45ee0b75ee9ca2292afffe5c117880f0d5f93"
)

MATH_SOURCE_REL = (
    "deliverables/"
    "cm2_round306c30d_source_w_multi_delta_whole_origin_exclusion_producer.py"
)
MATH_SOURCE_SHA256 = (
    "93ab9aed0afb93fb88c298bc87c0a5b7edd26a4e7561d6edec18ae2641175dce"
)
SELF_SOURCE_REL = "deliverables/" + Path(__file__).name

EXPECTED_ORIGINS = 20
EXPECTED_ORIGIN_KEYS_SHA256 = (
    "4b9d22a6c363960f67d4da851f5a77e487ee240f427bc9bd9016ced24c1b88e4"
)
EXPECTED_FINAL_CELLS = 3_152
EXPECTED_MULTI_CELLS = 1_176
EXPECTED_C30A_CLIPPED_CELLS = 1_976
EXPECTED_PRIOR_CLOSED = 282
EXPECTED_PRECLOSED_FRONTIER = 68
EXPECTED_RESIDUAL_ROOTS = 360
EXPECTED_INHERITED_TERMINALS = 1_014

ZERO_FORMAL = {
    "multi_Delta_cell_dispositions": 0,
    "multi_Delta_whole_cell_exclusions": 0,
    "resolved_source_W_origin_dispositions": 0,
    "whole_source_W_origin_exclusions": 0,
}
CONTROLLED_ENVIRONMENT = {
    "HOME": "/nonexistent",
    "LC_ALL": "C.UTF-8",
    "TZ": "UTC",
}
CONTROLLED_HASH_SEEDS = frozenset({"30630071", "30630929"})
HASH_SEED_SENTINEL = "CM2_C30D_HASH_SEED_SENTINEL_v1"
HASH_FINGERPRINTS = {
    "30630071": 1743314986988020519,
    "30630929": 3335165125009301667,
}


class Reject(RuntimeError):
    """Stable fail-closed candidate rejection."""


def need(condition: bool, label: str) -> None:
    if type(condition) is not bool or not condition:
        raise Reject(label)


def canonical(value: Any) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=True,
        allow_nan=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("ascii")


def object_digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def identity(value: os.stat_result) -> tuple[int, ...]:
    return (
        value.st_dev,
        value.st_ino,
        value.st_mode,
        value.st_nlink,
        value.st_size,
        value.st_mtime_ns,
        value.st_ctime_ns,
        value.st_uid,
        value.st_gid,
    )


def read_singleton(path: Path, maximum: int, label: str) -> bytes:
    absolute = Path(os.path.abspath(os.fspath(path)))
    need(absolute.resolve(strict=True) == absolute, "canonical path:" + label)
    descriptor = os.open(
        absolute,
        os.O_RDONLY | os.O_CLOEXEC | getattr(os, "O_NOFOLLOW", 0),
    )
    try:
        before = os.fstat(descriptor)
        need(
            stat.S_ISREG(before.st_mode)
            and before.st_nlink == 1
            and before.st_size > 0
            and before.st_size <= maximum,
            "regular singleton:" + label,
        )
        chunks: list[bytes] = []
        remaining = before.st_size
        while remaining > 0:
            block = os.read(descriptor, min(4 << 20, remaining))
            need(bool(block), "complete read:" + label)
            chunks.append(block)
            remaining -= len(block)
        need(os.read(descriptor, 1) == b"", "stable EOF:" + label)
        after = os.fstat(descriptor)
    finally:
        os.close(descriptor)
    need(identity(before) == identity(after), "stable capture:" + label)
    return b"".join(chunks)


def file_hash(path: Path, label: str) -> str:
    absolute = Path(os.path.abspath(os.fspath(path)))
    need(absolute.resolve(strict=True) == absolute, "canonical hash path:" + label)
    descriptor = os.open(
        absolute,
        os.O_RDONLY | os.O_CLOEXEC | getattr(os, "O_NOFOLLOW", 0),
    )
    try:
        before = os.fstat(descriptor)
        need(
            stat.S_ISREG(before.st_mode) and before.st_nlink == 1,
            "hash singleton:" + label,
        )
        state = hashlib.sha256()
        total = 0
        while True:
            block = os.read(descriptor, 4 << 20)
            if block == b"":
                break
            state.update(block)
            total += len(block)
        after = os.fstat(descriptor)
    finally:
        os.close(descriptor)
    need(
        identity(before) == identity(after) and total == before.st_size,
        "stable hash:" + label,
    )
    return state.hexdigest()


def strict_object(raw: bytes, label: str) -> dict[str, Any]:
    need(not raw.startswith(b"\xef\xbb\xbf") and b"\x00" not in raw, "JSON:" + label)

    def reject_number(value: str) -> None:
        raise Reject("noninteger JSON:" + label + ":" + value)

    def unique(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        output: dict[str, Any] = {}
        for key, value in pairs:
            need(key not in output, "duplicate JSON key:" + label)
            output[key] = value
        return output

    value = json.loads(
        raw.decode("utf-8", "strict"),
        object_pairs_hook=unique,
        parse_float=reject_number,
        parse_constant=reject_number,
    )
    need(type(value) is dict, "JSON top object:" + label)
    return value


def controlled_seed_guard() -> str:
    environment = dict(os.environ)
    seed = environment.pop("PYTHONHASHSEED", None)
    need(
        sys.flags.isolated == 0
        and sys.flags.ignore_environment == 0
        and sys.flags.safe_path is True
        and sys.flags.no_user_site == 1
        and sys.flags.dont_write_bytecode == 1
        and sys.flags.hash_randomization == 1
        and sys.dont_write_bytecode is True,
        "controlled Python flags",
    )
    need(
        seed in CONTROLLED_HASH_SEEDS and environment == CONTROLLED_ENVIRONMENT,
        "exact controlled environment",
    )
    need(
        type(seed) is str and hash(HASH_SEED_SENTINEL) == HASH_FINGERPRINTS[seed],
        "controlled hash-seed fingerprint",
    )
    return seed


def validate_projection(value: dict[str, Any], chain: Path, pins: Path) -> None:
    authority = value.get("authority")
    handoff = value.get("predecessor_formal_handoff")
    boundary = value.get("C30d_boundary")
    need(
        value.get("schema") == AUTHORITY_SCHEMA
        and value.get("status") == AUTHORITY_STATUS
        and type(authority) is dict
        and type(handoff) is dict
        and type(boundary) is dict,
        "exact authority envelope",
    )
    expected_relative = os.fspath(chain.relative_to(WORKSPACE))
    need(
        authority.get("kind")
        == "C30C_V5_V6_PUBLICATION_TERMINAL_PLUS_CONSOLIDATED_FORMAL_LEDGER"
        and authority.get("chain_relative_path") == expected_relative
        and authority.get("dynamic_pinset_file_sha256")
        == file_hash(pins, "dynamic pinset replay")
        and authority.get("candidate_result_object_sha256")
        == C30C_RESULT_OBJECT_SHA256
        and authority.get("candidate_origin_keys_sha256")
        == C30C_ORIGIN_KEYS_SHA256
        and all(
            type(authority.get(key)) is str
            and len(authority[key]) == 64
            and all(character in "0123456789abcdef" for character in authority[key])
            for key in (
                "dynamic_pinset_object_sha256",
                "payload_manifest_sha256",
                "root_manifest_sha256",
                "outer_verification_sha256",
                "terminal_replay_sha256",
                "terminal_replay_object_sha256",
                "chain_status_sha256",
                "chain_status_object_sha256",
                "publication_independent_audit_object_sha256",
                "formal_ledger_object_sha256",
                "formal_ledger_application_object_sha256",
                "formal_ledger_independent_verification_object_sha256",
                "formal_ledger_transition_id",
            )
        ),
        "exact terminal graph projection",
    )
    after = handoff.get("after")
    need(
        handoff.get("transition") == {"before": 80, "after": 78}
        and handoff.get("C30c_transition_authorized") is True
        and type(after) is dict
        and after.get("remaining") == 78
        and after.get("remaining_partition")
        == {
            "multi_Delta": 20,
            "reduced_live": 2,
            "retained_source_seams": 2,
            "compact_q": 54,
        }
        and after.get("excluded") + after.get("conservative_live")
        == after.get("total")
        == 76_832
        and after.get("resolved_nonexcluded") == 2_008,
        "exact C30c terminal after state",
    )
    need(
        boundary.get("formal_starting_remainder") == after["remaining"]
        and boundary.get("proposed_after_remainder") == 58
        and boundary.get("C30d_transition_authorized") is False
        and value.get("formal_credit") == ZERO_FORMAL
        and value.get("source_W_formal_remainder") == after["remaining"]
        and value.get("source_W_transition_authorized_by_this_projection") is False
        and value.get("D02") == "BLOCKED_COMPOSITE"
        and value.get("D03") == "UNAUTHORIZED"
        and value.get("D04") == "NOT_MINTED"
        and value.get("Gate5") == "10/18"
        and value.get("CM2") == "NO-GO_FOR_CLAIM",
        "exact zero-credit C30d boundary",
    )


def run_authority(chain_dir: Path, pins_path: Path) -> dict[str, Any]:
    adapter = WORKSPACE / AUTHORITY_ADAPTER_REL
    need(
        file_hash(adapter, "authority adapter") == AUTHORITY_ADAPTER_SHA256,
        "authority adapter source pin",
    )
    chain = Path(os.path.abspath(os.fspath(chain_dir)))
    pins = Path(os.path.abspath(os.fspath(pins_path)))
    need(chain.resolve(strict=True) == chain, "canonical chain directory")
    need(pins.resolve(strict=True) == pins, "canonical dynamic pins")
    process = subprocess.run(
        [
            os.fspath(PYTHON),
            "-P",
            "-s",
            "-B",
            os.fspath(adapter),
            "--chain-dir",
            os.fspath(chain),
            "--dynamic-pins",
            os.fspath(pins),
        ],
        cwd=WORKSPACE,
        env={**CONTROLLED_ENVIRONMENT, "PYTHONHASHSEED": os.environ["PYTHONHASHSEED"]},
        stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    need(
        process.returncode == 0 and process.stderr == b"" and bool(process.stdout),
        "C30c terminal authority adapter",
    )
    payload = process.stdout[:-1] if process.stdout.endswith(b"\n") else b""
    value = strict_object(payload, "authority projection")
    need(process.stdout == canonical(value) + b"\n", "canonical adapter stdout")
    validate_projection(value, chain, pins)
    return value


def load_math_module() -> ModuleType:
    source = WORKSPACE / MATH_SOURCE_REL
    need(file_hash(source, "frozen C30d math source") == MATH_SOURCE_SHA256, "math pin")
    name = "_cm2_round306c30d_frozen_math_kernel_for_v3_producer"
    need(name not in sys.modules, "math kernel not preloaded")
    specification = importlib.util.spec_from_file_location(name, source)
    need(
        specification is not None and specification.loader is not None,
        "math import specification",
    )
    module = importlib.util.module_from_spec(specification)
    sys.modules[name] = module
    try:
        specification.loader.exec_module(module)
    except BaseException:
        sys.modules.pop(name, None)
        raise
    need(
        Path(module.__file__).resolve(strict=True) == source.resolve(strict=True)
        and file_hash(source, "frozen C30d math source replay") == MATH_SOURCE_SHA256,
        "imported math identity",
    )
    return module


def workspace_relative(path: Path) -> str:
    absolute = Path(os.path.abspath(os.fspath(path)))
    need(absolute.resolve(strict=True) == absolute, "canonical pinned input")
    need(absolute.is_relative_to(WORKSPACE), "pinned input workspace containment")
    return os.fspath(absolute.relative_to(WORKSPACE))


def load_full_delta_keys() -> list[str]:
    path = WORKSPACE / C30C_RESULT_REL
    raw = read_singleton(path, 32 << 20, "C30c candidate result")
    value = strict_object(raw, "C30c candidate result")
    body = dict(value)
    claimed = body.pop("result_sha256", None)
    keys = value.get("scope", {}).get("origin_keys")
    need(
        raw == canonical(value)
        and claimed == C30C_RESULT_OBJECT_SHA256
        and object_digest(body) == C30C_RESULT_OBJECT_SHA256
        and type(keys) is list
        and len(keys) == 2
        and all(type(key) is str for key in keys)
        and object_digest(keys) == C30C_ORIGIN_KEYS_SHA256,
        "C30c full-Delta origin projection",
    )
    return keys


def load_math_inputs(math: ModuleType, projection: dict[str, Any], pins_path: Path) -> dict[str, Any]:
    pin_map: dict[str, str] = {}

    def pin(path: Path, expected: str, label: str) -> None:
        actual = file_hash(path, label)
        need(actual == expected, "input pin:" + label)
        relative = workspace_relative(path)
        previous = pin_map.get(relative)
        need(previous is None or previous == actual, "input pin agreement:" + relative)
        pin_map[relative] = actual

    pin(WORKSPACE / MATH_SOURCE_REL, MATH_SOURCE_SHA256, "frozen math")
    pin(WORKSPACE / AUTHORITY_ADAPTER_REL, AUTHORITY_ADAPTER_SHA256, "authority adapter")
    pin(pins_path, projection["authority"]["dynamic_pinset_file_sha256"], "dynamic pins")
    pin(WORKSPACE / RUNTIME_ATTESTATION_REL, RUNTIME_ATTESTATION_SHA256, "runtime attestation")
    pin(WORKSPACE / C30C_RESULT_REL, file_hash(WORKSPACE / C30C_RESULT_REL, "C30c result"), "C30c result")
    pin(DELIVERABLES / math.C30A_SOURCE, math.C30A_SOURCE_SHA256, "C30a producer")
    pin(DELIVERABLES / math.C30A_MANIFEST, math.C30A_MANIFEST_SHA256, "C30a manifest")
    pin(DELIVERABLES / math.C30A_RESULT, math.C30A_RESULT_SHA256, "C30a result")
    pin(DELIVERABLES / math.C30A_CELL_LEDGER, math.C30A_CELL_LEDGER_SHA256, "C30a cells")
    pin(DELIVERABLES / math.R184_CERTIFICATE, math.R184_CERTIFICATE_SHA256, "R184")
    pin(DELIVERABLES / math.R215_CERTIFICATE, math.R215_CERTIFICATE_SHA256, "R215")
    for row in math.c30a.validate_inputs():
        path = DELIVERABLES / row["filename"]
        pin(path, row["sha256"], "C30a transitive:" + row["filename"])
    for filename, expected in math.parse_manifest().items():
        pin(DELIVERABLES / filename, expected, "C30a manifest member:" + filename)

    c30a_result = math.strict_json(DELIVERABLES / math.C30A_RESULT)
    c30a_body = {key: value for key, value in c30a_result.items() if key != "result_sha256"}
    need(
        c30a_result.get("result_sha256") == math.C30A_RESULT_OBJECT_SHA256
        and math.digest(c30a_body) == math.C30A_RESULT_OBJECT_SHA256
        and c30a_result["source_W_ledger_transition"]["after"]["excluded"] == 74_744
        and c30a_result["source_W_ledger_transition"]["after"]["conservative_live"] == 2_088
        and c30a_result["source_W_ledger_transition"]["after"]["remaining"] == 92,
        "C30a mathematical evidence boundary",
    )
    r184 = math.strict_json(DELIVERABLES / math.R184_CERTIFICATE)
    r215_certificate = math.strict_json(DELIVERABLES / math.R215_CERTIFICATE)
    need(
        r184["result_sha256"] == math.R184_RESULT_SHA256
        and math.digest(r184["result"]) == math.R184_RESULT_SHA256
        and r215_certificate["result_sha256"] == math.R215_RESULT_SHA256
        and math.digest(r215_certificate["result"]) == math.R215_RESULT_SHA256
        and r215_certificate["result"]["bounded_probe_result_sha256"]
        == math.R215_BOUNDED_RESULT_SHA256,
        "R184/R215 object closures",
    )
    bounded = r215_certificate["result"]["bounded_probe_result"]
    summaries = {
        row["origin_key"]: row
        for row in bounded["whole_origin_outcome"]["per_origin_rows"]
        if row["first_obstruction"] == "MULTI_DELTA_GRAPH_ARRANGEMENT"
    }
    origin_keys = sorted(summaries)
    registry = {
        row["origin_key"]: row
        for row in r184["result"]["priority_registry"]["rows"]
        if row["origin_key"] in summaries
    }
    full_delta_keys = load_full_delta_keys()
    need(
        len(origin_keys) == EXPECTED_ORIGINS
        and math.digest(origin_keys) == EXPECTED_ORIGIN_KEYS_SHA256
        and set(registry) == set(origin_keys)
        and set(origin_keys).isdisjoint(full_delta_keys)
        and all(
            registry[key]["priority_class"] == "DELTA_H_OR_MULTI_NO_Q"
            and registry[key]["selection_uses_new_closure_outcome"] is False
            and registry[key]["Round180_residual_child_count"]
            == summaries[key]["Round201_residual_cell_count"]
            and summaries[key]["Round215_analytic_closed_cell_count"] == 0
            for key in origin_keys
        )
        and sum(row["Round201_residual_cell_count"] for row in summaries.values())
        == EXPECTED_FINAL_CELLS
        and sum(
            row["Round215_blocker_count"]["MULTI_DELTA_GRAPH_ARRANGEMENT"]
            for row in summaries.values()
        )
        == EXPECTED_MULTI_CELLS
        and sum(
            row["Round215_blocker_count"]["SINGLE_CLIPPED_DELTA_ENDPOINT_OVERWRAP"]
            for row in summaries.values()
        )
        == EXPECTED_C30A_CLIPPED_CELLS,
        "dynamic twenty-origin selection",
    )
    all_c30a_cells = math.gzip_rows(
        DELIVERABLES / math.C30A_CELL_LEDGER,
        c30a_result["ledgers"]["reduced_clipped_cell"],
    )
    origin_set = set(origin_keys)
    c30a_cells = {
        row["cell_key"]: row for row in all_c30a_cells if row["origin_key"] in origin_set
    }
    need(
        len(c30a_cells) == EXPECTED_C30A_CLIPPED_CELLS
        and math.digest(sorted(c30a_cells)) == math.EXPECTED_C30A_CELL_KEYS_SHA256
        and all(
            row["whole_closed_cell_excluded"] is True
            and row["partition"]["closed_box_and_all_owned_faces_edges_vertices_excluded"] is True
            for row in c30a_cells.values()
        ),
        "C30a clipped mathematical evidence",
    )
    return {
        "pin_map": pin_map,
        "input_pins": [
            {"filename": filename, "sha256": sha256}
            for filename, sha256 in sorted(pin_map.items())
        ],
        "origin_keys": origin_keys,
        "registry": registry,
        "summaries": summaries,
        "c30a_cells": c30a_cells,
    }


def derive_transition(projection: dict[str, Any]) -> dict[str, Any]:
    before = json.loads(canonical(projection["predecessor_formal_handoff"]["after"]))
    partition = dict(before["remaining_partition"])
    need(partition.pop("multi_Delta", None) == EXPECTED_ORIGINS, "multi-Delta predecessor lane")
    after = {
        "excluded": before["excluded"] + EXPECTED_ORIGINS,
        "conservative_live": before["conservative_live"] - EXPECTED_ORIGINS,
        "resolved_nonexcluded": before["resolved_nonexcluded"],
        "remaining": before["remaining"] - EXPECTED_ORIGINS,
        "total": before["total"],
        "remaining_partition": partition,
    }
    need(
        before["remaining"] == sum(before["remaining_partition"].values())
        and after["remaining"] == sum(partition.values()) == 58
        and after["excluded"] + after["conservative_live"] == after["total"] == 76_832,
        "derived 78-to-58 conservation",
    )
    return {
        "before": before,
        "candidate_credits": {
            "whole_origin_exclusion": EXPECTED_ORIGINS,
            "resolved_origin_disposition": EXPECTED_ORIGINS,
        },
        "after": after,
        "conservation_identity": "74766+2066=76832",
        "official_ledger_mutated": False,
        "C30d_transition_authorized": False,
    }


def theorem() -> dict[str, Any]:
    return {
        "kind": "SOURCE_W_20_MULTI_DELTA_WHOLE_ORIGIN_EXCLUSION_THEOREM_CANDIDATE",
        "origin_selection_dynamically_derived_from_pinned_R184_R215": True,
        "selected_origin_count": EXPECTED_ORIGINS,
        "selected_origin_keys_sha256": EXPECTED_ORIGIN_KEYS_SHA256,
        "sealed_C30a_clipped_cells_composed": EXPECTED_C30A_CLIPPED_CELLS,
        "new_multi_Delta_cells_closed": EXPECTED_MULTI_CELLS,
        "every_multi_Delta_cell_has_exactly_two_G_and_one_W_admissible_targets": True,
        "every_possible_G_first_target_is_owner_mismatch_excluded": True,
        "every_possible_W_first_target_is_N_or_S_outgoing_mismatch_excluded": True,
        "Delta_zero_Delta_intersection_and_root_tie_strata_included": True,
        "rank_aware_multi_graph_order_not_needed_for_this_exclusion": True,
        "every_origin_has_complete_3D_2D_1D_0D_half_open_owner_audit": True,
        "all_twenty_whole_original_physical_origins_excluded_candidate": True,
        "child_count_or_volume_used_as_whole_origin_credit": False,
    }


def create_fresh_directory(path: Path) -> Path:
    absolute = Path(os.path.abspath(os.fspath(path)))
    parent = absolute.parent
    need(parent.resolve(strict=True) == parent, "canonical candidate parent")
    need(absolute.is_relative_to(WORKSPACE), "candidate workspace containment")
    need(not absolute.exists() and not absolute.is_symlink(), "fresh candidate path")
    os.mkdir(absolute, 0o700)
    opened = absolute.lstat()
    need(stat.S_ISDIR(opened.st_mode) and not absolute.is_symlink(), "candidate directory")
    return absolute


def write_bytes_exclusive(path: Path, raw: bytes) -> None:
    descriptor = os.open(
        path,
        os.O_WRONLY
        | os.O_CREAT
        | os.O_EXCL
        | os.O_CLOEXEC
        | getattr(os, "O_NOFOLLOW", 0),
        0o600,
    )
    try:
        view = memoryview(raw)
        while len(view) > 0:
            written = os.write(descriptor, view)
            need(written > 0, "complete exclusive write:" + path.name)
            view = view[written:]
        os.fsync(descriptor)
        facts = os.fstat(descriptor)
    finally:
        os.close(descriptor)
    need(
        stat.S_ISREG(facts.st_mode) and facts.st_nlink == 1 and facts.st_size == len(raw),
        "exclusive singleton output:" + path.name,
    )


def write_rows_exclusive(path: Path, rows: Iterable[dict[str, Any]]) -> tuple[int, str]:
    descriptor = os.open(
        path,
        os.O_WRONLY
        | os.O_CREAT
        | os.O_EXCL
        | os.O_CLOEXEC
        | getattr(os, "O_NOFOLLOW", 0),
        0o600,
    )
    sequence = hashlib.sha256()
    count = 0
    try:
        with os.fdopen(descriptor, "wb", closefd=False) as raw:
            with gzip.GzipFile(filename="", mode="wb", fileobj=raw, compresslevel=9, mtime=0) as stream:
                for row in rows:
                    stream.write(canonical(row) + b"\n")
                    sequence.update(bytes.fromhex(row["row_sha256"]))
                    count += 1
            raw.flush()
            os.fsync(raw.fileno())
        facts = os.fstat(descriptor)
    finally:
        os.close(descriptor)
    need(stat.S_ISREG(facts.st_mode) and facts.st_nlink == 1, "gzip singleton:" + path.name)
    return count, sequence.hexdigest()


def descriptor(path: Path, count: int, sequence: str, order: str) -> dict[str, Any]:
    facts = path.lstat()
    need(stat.S_ISREG(facts.st_mode) and facts.st_nlink == 1 and not path.is_symlink(), "ledger singleton")
    return {
        "filename": path.name,
        "row_count": count,
        "size": facts.st_size,
        "sha256": file_hash(path, "output ledger:" + path.name),
        "row_sequence_sha256": sequence,
        "order": order,
    }


def result_body(
    *,
    projection: dict[str, Any],
    inputs: dict[str, Any],
    runtime: dict[str, Any],
    transition: dict[str, Any],
    cell_descriptor: dict[str, Any],
    owner_descriptor: dict[str, Any],
    origin_descriptor: dict[str, Any],
    self_sha256: str,
) -> dict[str, Any]:
    candidate_theorem = theorem()
    return {
        "schema": "cm2.round306c30d.source-w-multi-delta-whole-origin-exclusion.candidate.v3",
        "status": (
            "PASS_CANDIDATE_C30D_V3__1176_MULTI_DELTA_CELLS__"
            "20_WHOLE_ORIGINS_EXCLUDED__ZERO_FORMAL_CREDIT__UNAUTHORIZED"
        ),
        "producer_contract": {
            "source": SELF_SOURCE_REL,
            "source_sha256": self_sha256,
            "frozen_mathematical_kernel": MATH_SOURCE_REL,
            "frozen_mathematical_kernel_sha256": MATH_SOURCE_SHA256,
            "predecessor_adapter": AUTHORITY_ADAPTER_REL,
            "predecessor_adapter_sha256": AUTHORITY_ADAPTER_SHA256,
        },
        "input_pins": inputs["input_pins"],
        "runtime": {
            "attestation_source": RUNTIME_ATTESTATION_REL,
            "attestation_filename": RUNTIME_ATTESTATION_NAME,
            "attestation_sha256": RUNTIME_ATTESTATION_SHA256,
            "controlled_seed_contract": runtime,
        },
        "upstream_credit_boundary": {
            "formal_authority": (
                "C30C_V5_V6_PUBLICATION_TERMINAL_PLUS_CONSOLIDATED_FORMAL_LEDGER"
            ),
            "predecessor_projection_sha256": object_digest(projection),
            "authority": projection["authority"],
            "predecessor_formal_after": projection["predecessor_formal_handoff"]["after"],
            "C30c_transition_authorized": True,
            "C30a_clipped_ledger_used_as_mathematical_evidence": True,
            "C30a_used_as_formal_ledger_baseline": False,
        },
        "scope": {
            "origin_count": EXPECTED_ORIGINS,
            "origin_keys": inputs["origin_keys"],
            "origin_keys_sha256": EXPECTED_ORIGIN_KEYS_SHA256,
            "Round180_final_cell_count": EXPECTED_FINAL_CELLS,
            "sealed_C30a_clipped_cell_count": EXPECTED_C30A_CLIPPED_CELLS,
            "new_multi_Delta_cell_count": EXPECTED_MULTI_CELLS,
            "new_multi_Delta_cell_disposition_census": {"EXCLUDED": EXPECTED_MULTI_CELLS},
            "whole_origin_disposition_census_candidate": {"EXCLUDED": EXPECTED_ORIGINS},
        },
        "candidate_theorem": candidate_theorem,
        "candidate_theorem_sha256": object_digest(candidate_theorem),
        "proposed_source_W_transition_if_C30d_is_terminally_sealed": transition,
        "ledgers": {
            "multi_Delta_cell_candidate": cell_descriptor,
            "atomic_half_open_owner_candidate": owner_descriptor,
            "whole_origin_exclusion_candidate": origin_descriptor,
        },
        "formal_credit": ZERO_FORMAL,
        "candidate_credit_if_independently_verified": {
            "multi_Delta_cell_dispositions": EXPECTED_MULTI_CELLS,
            "multi_Delta_whole_cell_exclusions": EXPECTED_MULTI_CELLS,
            "resolved_source_W_origin_dispositions": EXPECTED_ORIGINS,
            "whole_source_W_origin_exclusions": EXPECTED_ORIGINS,
        },
        "strict_nonpromotion": {
            "candidate_only": True,
            "independent_verifier_passed": False,
            "coherent_attacks_passed": False,
            "dual_seed_replay_passed": False,
            "cold_TOCTOU_replay_passed": False,
            "payload_manifest_present": False,
            "root_manifest_present": False,
            "outer_verification_present": False,
            "terminal_replay_present": False,
            "C30d_transition_authorized": False,
            "source_W_formal_remainder": transition["before"]["remaining"],
            "D02": "BLOCKED_COMPOSITE",
            "D03": "UNAUTHORIZED",
            "D04": "NOT_MINTED",
            "Gate5": "10/18",
            "CM2": "NO-GO_FOR_CLAIM",
        },
        "required_next": (
            "DUAL_REAL_SEED_RUN__NO_IMPORT_VERIFIER__COHERENT_AND_RELEASE_ATTACKS__"
            "COLD_TOCTOU__MANIFESTS__OUTER__TERMINAL_BYTE_REPLAY"
        ),
    }


def build(chain_dir: Path, pins_path: Path, candidate_path: Path) -> dict[str, Any]:
    controlled_seed_guard()
    projection = run_authority(chain_dir, pins_path)
    math = load_math_module()
    math.ctx.prec = 192
    math.c30a.validate_runtime()
    runtime = math.validate_controlled_seed_runtime()
    inputs = load_math_inputs(math, projection, Path(os.path.abspath(os.fspath(pins_path))))
    self_sha256 = file_hash(Path(__file__).resolve(), "C30d-v3 producer source")

    origin_rows: list[dict[str, Any]] = []
    cell_rows: list[dict[str, Any]] = []
    owner_rows: list[dict[str, Any]] = []
    for ordinal, origin in enumerate(inputs["origin_keys"]):
        origin_row, new_cells, new_owners = math.build_origin(
            ordinal,
            len(cell_rows),
            origin,
            inputs["registry"][origin],
            inputs["summaries"][origin],
            inputs["c30a_cells"],
        )
        origin_rows.append(origin_row)
        cell_rows.extend(new_cells)
        owner_rows.extend(new_owners)
    lineage: Counter[str] = Counter()
    for row in origin_rows:
        lineage.update(row["lineage_census"])
    need(
        len(origin_rows) == EXPECTED_ORIGINS
        and len(cell_rows) == EXPECTED_MULTI_CELLS
        and bool(owner_rows)
        and {row["ambient_dimension"] for row in owner_rows} == {0, 1, 2, 3}
        and all(row["owner_disposition"] == "EXCLUDED" for row in owner_rows)
        and [row["origin_key"] for row in origin_rows] == inputs["origin_keys"]
        and [row["cell_key"] for row in cell_rows] == sorted(row["cell_key"] for row in cell_rows)
        and Counter(row["source_chart_id"] for row in cell_rows) == Counter({"W:N": 588, "W:S": 588})
        and lineage["Round176_prior_closed"] == EXPECTED_PRIOR_CLOSED
        and lineage["Round176_preclosed_frontier"] == EXPECTED_PRECLOSED_FRONTIER
        and lineage["Round176_residual_roots"] == EXPECTED_RESIDUAL_ROOTS
        and lineage["Round180_inherited_excluded"] == EXPECTED_INHERITED_TERMINALS
        and lineage["Round180_final"] == EXPECTED_FINAL_CELLS
        and lineage["sealed_C30a_clipped_excluded"] == EXPECTED_C30A_CLIPPED_CELLS
        and lineage["Round306C30D_multi_Delta_excluded"] == EXPECTED_MULTI_CELLS
        and all(row["whole_closed_cell_excluded"] is True for row in cell_rows)
        and all(row["whole_origin_disposition_candidate"] == "EXCLUDED" for row in origin_rows),
        "complete C30d-v3 mathematical census",
    )
    transition = derive_transition(projection)
    replay_projection = run_authority(chain_dir, pins_path)
    need(canonical(replay_projection) == canonical(projection), "authority TOCTOU projection")
    for relative, expected in inputs["pin_map"].items():
        need(file_hash(WORKSPACE / relative, "input replay:" + relative) == expected, "input TOCTOU:" + relative)

    candidate = create_fresh_directory(candidate_path)
    runtime_raw = read_singleton(WORKSPACE / RUNTIME_ATTESTATION_REL, 4 << 20, "runtime attestation")
    write_bytes_exclusive(candidate / RUNTIME_ATTESTATION_NAME, runtime_raw)
    cell_count, cell_sequence = write_rows_exclusive(candidate / CELL_LEDGER, cell_rows)
    owner_count, owner_sequence = write_rows_exclusive(candidate / ATOMIC_OWNER_LEDGER, owner_rows)
    origin_count, origin_sequence = write_rows_exclusive(candidate / ORIGIN_LEDGER, origin_rows)
    cell_descriptor = descriptor(candidate / CELL_LEDGER, cell_count, cell_sequence, "LEXICOGRAPHIC_ROUND180_FINAL_CELL_KEY")
    owner_descriptor = descriptor(
        candidate / ATOMIC_OWNER_LEDGER,
        owner_count,
        owner_sequence,
        "ORIGIN_KEY_THEN_DIMENSION_3_TO_0_THEN_LEAF_KEY_OR_CANONICAL_GEOMETRY",
    )
    origin_descriptor = descriptor(candidate / ORIGIN_LEDGER, origin_count, origin_sequence, "LEXICOGRAPHIC_SOURCE_W_ORIGIN_KEY")
    body = result_body(
        projection=projection,
        inputs=inputs,
        runtime=runtime,
        transition=transition,
        cell_descriptor=cell_descriptor,
        owner_descriptor=owner_descriptor,
        origin_descriptor=origin_descriptor,
        self_sha256=self_sha256,
    )
    result = {**body, "result_sha256": object_digest(body)}
    write_bytes_exclusive(candidate / RESULT, canonical(result))
    names = {entry.name for entry in os.scandir(candidate)}
    need(
        names == {RUNTIME_ATTESTATION_NAME, CELL_LEDGER, ATOMIC_OWNER_LEDGER, ORIGIN_LEDGER, RESULT}
        and all(
            stat.S_ISREG((candidate / name).lstat().st_mode)
            and (candidate / name).lstat().st_nlink == 1
            and not (candidate / name).is_symlink()
            for name in names
        ),
        "exact singleton candidate file set",
    )
    return result


def fixture_projection() -> dict[str, Any]:
    after = {
        "excluded": 74_746,
        "conservative_live": 2_086,
        "resolved_nonexcluded": 2_008,
        "remaining": 78,
        "total": 76_832,
        "remaining_partition": {
            "multi_Delta": 20,
            "reduced_live": 2,
            "retained_source_seams": 2,
            "compact_q": 54,
        },
    }
    return {
        "schema": AUTHORITY_SCHEMA,
        "status": AUTHORITY_STATUS,
        "authority": {"fixture": True},
        "predecessor_formal_handoff": {"after": after},
    }


def self_test() -> dict[str, Any]:
    transition = derive_transition(fixture_projection())
    need(transition["before"]["remaining"] == 78, "fixture before")
    need(transition["after"]["remaining"] == 58, "fixture after")
    need(transition["C30d_transition_authorized"] is False, "fixture zero authority")
    tree = ast.parse(read_singleton(Path(__file__).resolve(), 8 << 20, "self source"))
    suspicious: list[int] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == "need" and node.args:
            first = node.args[0]
            if isinstance(first, ast.BoolOp) and isinstance(first.values[-1], (ast.Name, ast.Attribute, ast.Subscript)):
                suspicious.append(node.lineno)
    need(not suspicious, "exact-bool static audit")
    return {
        "schema": "cm2.round306c30d.v3-producer-self-test.v1",
        "status": "PASS_C30D_V3_PRODUCER_STATIC_FIXTURES__ZERO_FORMAL_CREDIT",
        "derived_transition": {"before": 78, "after": 58},
        "exact_bool_suspicious_lines": suspicious,
        "formal_credit": ZERO_FORMAL,
        "C30d_transition_authorized": False,
        "CM2": "NO-GO_FOR_CLAIM",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--chain-dir", type=Path)
    parser.add_argument("--dynamic-pins", type=Path)
    parser.add_argument("--candidate-dir", type=Path)
    parser.add_argument("--self-test", action="store_true")
    arguments = parser.parse_args()
    try:
        if arguments.self_test:
            need(
                arguments.chain_dir is None
                and arguments.dynamic_pins is None
                and arguments.candidate_dir is None,
                "self-test argument isolation",
            )
            print(canonical(self_test()).decode("ascii"))
            return 0
        need(
            arguments.chain_dir is not None
            and arguments.dynamic_pins is not None
            and arguments.candidate_dir is not None,
            "complete producer arguments",
        )
        result = build(arguments.chain_dir, arguments.dynamic_pins, arguments.candidate_dir)
    except (Reject, OSError, ValueError, TypeError, KeyError, AssertionError, subprocess.SubprocessError):
        return 2
    print(canonical({
        "schema": "cm2.round306c30d.v3-producer-run-receipt.v1",
        "status": "PASS_C30D_V3_CANDIDATE_CREATED__ZERO_FORMAL_CREDIT",
        "result_sha256": result["result_sha256"],
        "formal_credit": ZERO_FORMAL,
        "C30d_transition_authorized": False,
        "CM2": "NO-GO_FOR_CLAIM",
    }).decode("ascii"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
