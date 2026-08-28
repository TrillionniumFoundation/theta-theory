#!/usr/bin/env python3
"""No-producer-import verifier for an append-only C30d-v3 candidate.

The C30c predecessor is revalidated by the independent v5/v6 terminal and
formal-ledger implementation.  The mathematical reference is reconstructed through the
frozen C30d independent kernel, never through either C30d producer.  Success
is still zero-credit and does not authorize a manifest or 78 -> 58 handoff.
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
from types import MappingProxyType, ModuleType
from typing import Any, Iterator

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

NEW_PRODUCER_REL = "deliverables/" + PREFIX + "_producer.py"
# Set after the append-only producer is frozen.  This is provenance only; the
# verifier never imports or executes it.
NEW_PRODUCER_SHA256 = (
    "946955775cfe1ddc2acba538f6723b64c57b8080ce12bd34e4959c2c46e1f11c"
)
AUTHORITY_ADAPTER_REL = (
    "deliverables/cm2_round306c30d_c30c_v3_predecessor_authority_adapter_v1.py"
)
AUTHORITY_ADAPTER_SHA256 = (
    "f10613b8698997c99d3cece4f301cc89ea9f532f2d23c9d08325ef150b578503"
)
AUTHORITY_VERIFIER_REL = (
    "deliverables/cm2_round306c30d_c30c_v3_predecessor_authority_"
    "independent_verifier_v1.py"
)
AUTHORITY_VERIFIER_SHA256 = (
    "2502080768137561722df2ef5662a560e3a49c943606920690b99e6ea695caae"
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

MATH_VERIFIER_REL = (
    "deliverables/"
    "cm2_round306c30d_source_w_multi_delta_whole_origin_exclusion_"
    "independent_verifier.py"
)
MATH_VERIFIER_SHA256 = (
    "faf778dcf6fb6e3f29c02dec20c545b3e72d4fd2e0453ba01fff81f5935ddbed"
)
MATH_PRODUCER_REL = (
    "deliverables/"
    "cm2_round306c30d_source_w_multi_delta_whole_origin_exclusion_producer.py"
)
MATH_PRODUCER_SHA256 = (
    "93ab9aed0afb93fb88c298bc87c0a5b7edd26a4e7561d6edec18ae2641175dce"
)

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
CELL_ZERO_FORMAL = {
    "multi_Delta_cell_disposition": 0,
    "whole_closed_cell_exclusion": 0,
    "whole_source_W_origin_exclusion": 0,
}
ORIGIN_ZERO_FORMAL = {
    "resolved_source_W_origin_disposition": 0,
    "whole_source_W_origin_exclusion": 0,
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
    """Independent fail-closed rejection."""


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
        need(stat.S_ISREG(before.st_mode) and before.st_nlink == 1, "hash singleton:" + label)
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
    need(identity(before) == identity(after) and total == before.st_size, "stable hash:" + label)
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


def independent_runtime_guard() -> str:
    environment = dict(os.environ)
    seed = environment.pop("PYTHONHASHSEED", None)
    need(
        sys.flags.isolated == 1
        and sys.flags.ignore_environment == 1
        and sys.flags.safe_path is True
        and sys.flags.no_user_site == 1
        and sys.flags.dont_write_bytecode == 1
        and sys.flags.hash_randomization == 1
        and sys.dont_write_bytecode is True,
        "isolated independent-verifier Python flags",
    )
    need(
        seed in CONTROLLED_HASH_SEEDS and environment == CONTROLLED_ENVIRONMENT,
        "exact independently attested environment",
    )
    # -I deliberately ignores PYTHONHASHSEED for interpreter initialization.
    # The declared seed remains external provenance; mathematical equality is
    # reconstructed without relying on dict/set iteration order.
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
        and authority.get("dynamic_pinset_file_sha256") == file_hash(pins, "dynamic pins replay")
        and authority.get("candidate_result_object_sha256") == C30C_RESULT_OBJECT_SHA256
        and authority.get("candidate_origin_keys_sha256") == C30C_ORIGIN_KEYS_SHA256,
        "exact independent terminal graph projection",
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
        and after.get("excluded") + after.get("conservative_live") == after.get("total") == 76_832
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
        "exact independent zero-credit boundary",
    )


def run_authority(chain_dir: Path, pins_path: Path) -> dict[str, Any]:
    verifier = WORKSPACE / AUTHORITY_VERIFIER_REL
    need(file_hash(verifier, "authority verifier") == AUTHORITY_VERIFIER_SHA256, "authority verifier source pin")
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
            os.fspath(verifier),
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
    need(process.returncode == 0 and process.stderr == b"" and bool(process.stdout), "independent C30c authority")
    payload = process.stdout[:-1] if process.stdout.endswith(b"\n") else b""
    value = strict_object(payload, "independent authority projection")
    need(process.stdout == canonical(value) + b"\n", "canonical authority stdout")
    validate_projection(value, chain, pins)
    return value


def producer_module_absent() -> bool:
    forbidden_paths = {
        (WORKSPACE / NEW_PRODUCER_REL).resolve(),
        (WORKSPACE / MATH_PRODUCER_REL).resolve(),
    }
    for module in tuple(sys.modules.values()):
        filename = getattr(module, "__file__", None)
        if filename is not None:
            try:
                if Path(filename).resolve() in forbidden_paths:
                    return False
            except (OSError, TypeError, ValueError):
                return False
    return True


def load_math_verifier() -> ModuleType:
    source = WORKSPACE / MATH_VERIFIER_REL
    need(file_hash(source, "frozen independent math") == MATH_VERIFIER_SHA256, "independent math pin")
    need(file_hash(WORKSPACE / MATH_PRODUCER_REL, "frozen producer provenance") == MATH_PRODUCER_SHA256, "frozen producer provenance pin")
    need(file_hash(WORKSPACE / NEW_PRODUCER_REL, "new producer provenance") == NEW_PRODUCER_SHA256, "new producer provenance pin")
    need(producer_module_absent(), "no producer loaded before math verifier")
    name = "_cm2_round306c30d_frozen_independent_math_for_v3"
    need(name not in sys.modules, "independent math not preloaded")
    specification = importlib.util.spec_from_file_location(name, source)
    need(specification is not None and specification.loader is not None, "independent math import specification")
    module = importlib.util.module_from_spec(specification)
    sys.modules[name] = module
    try:
        specification.loader.exec_module(module)
    except BaseException:
        sys.modules.pop(name, None)
        raise
    need(
        Path(module.__file__).resolve(strict=True) == source.resolve(strict=True)
        and file_hash(source, "independent math replay") == MATH_VERIFIER_SHA256
        and producer_module_absent(),
        "imported independent math identity",
    )
    return module


def workspace_relative(path: Path) -> str:
    absolute = Path(os.path.abspath(os.fspath(path)))
    need(absolute.resolve(strict=True) == absolute, "canonical pinned input")
    need(absolute.is_relative_to(WORKSPACE), "pinned input workspace containment")
    return os.fspath(absolute.relative_to(WORKSPACE))


def parse_manifest(path: Path) -> dict[str, str]:
    raw = read_singleton(path, 1 << 20, "C30a manifest")
    rows: dict[str, str] = {}
    for line in raw.decode("ascii", "strict").splitlines():
        pieces = line.split("  ", 1)
        need(
            len(pieces) == 2
            and len(pieces[0]) == 64
            and all(character in "0123456789abcdef" for character in pieces[0]),
            "manifest syntax",
        )
        relative = Path(pieces[1])
        need(
            pieces[1] not in rows
            and not relative.is_absolute()
            and ".." not in relative.parts,
            "manifest path",
        )
        rows[pieces[1]] = pieces[0]
    need(bool(rows), "nonempty manifest")
    return rows


def load_full_delta_keys() -> list[str]:
    raw = read_singleton(WORKSPACE / C30C_RESULT_REL, 32 << 20, "C30c candidate result")
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
        "C30c full-Delta origins",
    )
    return keys


def expected_input_pins(legacy: ModuleType, projection: dict[str, Any], pins_path: Path) -> tuple[list[dict[str, str]], dict[str, str]]:
    pin_map: dict[str, str] = {}

    def pin(path: Path, expected: str, label: str) -> None:
        actual = file_hash(path, label)
        need(actual == expected, "input pin:" + label)
        relative = workspace_relative(path)
        previous = pin_map.get(relative)
        need(previous is None or previous == actual, "input pin agreement:" + relative)
        pin_map[relative] = actual

    pin(WORKSPACE / MATH_PRODUCER_REL, MATH_PRODUCER_SHA256, "frozen producer math")
    pin(WORKSPACE / AUTHORITY_ADAPTER_REL, AUTHORITY_ADAPTER_SHA256, "producer authority adapter")
    pin(pins_path, projection["authority"]["dynamic_pinset_file_sha256"], "dynamic pins")
    pin(WORKSPACE / RUNTIME_ATTESTATION_REL, RUNTIME_ATTESTATION_SHA256, "runtime attestation")
    pin(WORKSPACE / C30C_RESULT_REL, file_hash(WORKSPACE / C30C_RESULT_REL, "C30c result"), "C30c result")
    pin(DELIVERABLES / legacy.C30A_PRODUCER, legacy.C30A_PRODUCER_SHA256, "C30a producer")
    pin(DELIVERABLES / legacy.C30A_MANIFEST, legacy.C30A_MANIFEST_SHA256, "C30a manifest")
    pin(DELIVERABLES / legacy.C30A_RESULT, legacy.C30A_RESULT_SHA256, "C30a result")
    pin(DELIVERABLES / legacy.C30A_CELL_LEDGER, legacy.C30A_CELL_LEDGER_SHA256, "C30a cells")
    pin(DELIVERABLES / legacy.R184_CERTIFICATE, legacy.R184_CERTIFICATE_SHA256, "R184")
    pin(DELIVERABLES / legacy.R215_CERTIFICATE, legacy.R215_CERTIFICATE_SHA256, "R215")
    for filename, expected in legacy.base.PINS.items():
        pin(DELIVERABLES / filename, expected, "C30a transitive:" + filename)
    for filename, expected in parse_manifest(DELIVERABLES / legacy.C30A_MANIFEST).items():
        pin(DELIVERABLES / filename, expected, "C30a manifest member:" + filename)
    return (
        [{"filename": filename, "sha256": sha256} for filename, sha256 in sorted(pin_map.items())],
        pin_map,
    )


def load_reference_inputs(legacy: ModuleType, projection: dict[str, Any], pins_path: Path) -> tuple[Any, list[dict[str, str]], dict[str, str]]:
    input_pins, pin_map = expected_input_pins(legacy, projection, pins_path)
    c30a_result = legacy.strict_json(DELIVERABLES / legacy.C30A_RESULT)
    c30a_body = dict(c30a_result)
    claimed = c30a_body.pop("result_sha256", None)
    need(
        claimed == legacy.C30A_RESULT_OBJECT_SHA256
        and legacy.digest(c30a_body) == legacy.C30A_RESULT_OBJECT_SHA256
        and c30a_result["source_W_ledger_transition"]["after"]["excluded"] == 74_744
        and c30a_result["source_W_ledger_transition"]["after"]["conservative_live"] == 2_088
        and c30a_result["source_W_ledger_transition"]["after"]["remaining"] == 92,
        "independent C30a boundary",
    )
    r184 = legacy.strict_json(DELIVERABLES / legacy.R184_CERTIFICATE)
    r215_certificate = legacy.strict_json(DELIVERABLES / legacy.R215_CERTIFICATE)
    need(
        r184["result_sha256"] == legacy.R184_RESULT_SHA256
        and legacy.digest(r184["result"]) == legacy.R184_RESULT_SHA256
        and r215_certificate["result_sha256"] == legacy.R215_RESULT_SHA256
        and legacy.digest(r215_certificate["result"]) == legacy.R215_RESULT_SHA256
        and r215_certificate["result"]["bounded_probe_result_sha256"] == legacy.R215_BOUNDED_RESULT_SHA256,
        "independent R184/R215 closures",
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
    full_delta_keys = load_full_delta_keys()
    need(
        len(origin_keys) == EXPECTED_ORIGINS
        and legacy.digest(list(origin_keys)) == EXPECTED_ORIGIN_KEYS_SHA256
        and set(registry) == set(origin_keys)
        and set(origin_keys).isdisjoint(full_delta_keys)
        and all(
            registry[key]["priority_class"] == "DELTA_H_OR_MULTI_NO_Q"
            and registry[key]["selection_uses_new_closure_outcome"] is False
            and registry[key]["Round180_residual_child_count"] == summaries[key]["Round201_residual_cell_count"]
            and summaries[key]["Round215_analytic_closed_cell_count"] == 0
            for key in origin_keys
        )
        and sum(row["Round201_residual_cell_count"] for row in summaries.values()) == EXPECTED_FINAL_CELLS
        and sum(row["Round215_blocker_count"]["MULTI_DELTA_GRAPH_ARRANGEMENT"] for row in summaries.values()) == EXPECTED_MULTI_CELLS
        and sum(row["Round215_blocker_count"]["SINGLE_CLIPPED_DELTA_ENDPOINT_OVERWRAP"] for row in summaries.values()) == EXPECTED_C30A_CLIPPED_CELLS,
        "independent dynamic twenty-origin selection",
    )
    all_cells = list(legacy.candidate_rows(DELIVERABLES / legacy.C30A_CELL_LEDGER))
    origin_set = set(origin_keys)
    c30a_cells = {row["cell_key"]: row for row in all_cells if row["origin_key"] in origin_set}
    need(
        len(c30a_cells) == EXPECTED_C30A_CLIPPED_CELLS
        and legacy.digest(sorted(c30a_cells)) == legacy.EXPECTED_C30A_CELL_KEYS_SHA256
        and all(
            row["whole_closed_cell_excluded"] is True
            and row["partition"]["closed_box_and_all_owned_faces_edges_vertices_excluded"] is True
            for row in c30a_cells.values()
        ),
        "independent C30a clipped evidence",
    )
    bundle = legacy.InputBundle(
        tuple((row["filename"], row["sha256"]) for row in input_pins),
        MappingProxyType(projection["authority"]),
        origin_keys,
        MappingProxyType(registry),
        MappingProxyType(summaries),
        MappingProxyType(c30a_cells),
    )
    return bundle, input_pins, pin_map


def reconstruct_reference(legacy: ModuleType, projection: dict[str, Any], pins_path: Path) -> dict[str, Any]:
    need(producer_module_absent(), "producer absence before reconstruction")
    legacy.ctx.prec = 192
    bundle, input_pins, pin_map = load_reference_inputs(legacy, projection, pins_path)
    origins: list[dict[str, Any]] = []
    cells: list[dict[str, Any]] = []
    owners: list[dict[str, Any]] = []
    for ordinal, origin in enumerate(bundle.origin_keys):
        origin_row, new_cells, new_owners = legacy.reconstruct_origin(ordinal, len(cells), origin, bundle)
        origins.append(origin_row)
        cells.extend(new_cells)
        owners.extend(new_owners)
    lineage: Counter[str] = Counter()
    for row in origins:
        lineage.update(row["lineage_census"])
    need(
        len(origins) == EXPECTED_ORIGINS
        and len(cells) == EXPECTED_MULTI_CELLS
        and bool(owners)
        and {row["ambient_dimension"] for row in owners} == {0, 1, 2, 3}
        and all(row["owner_disposition"] == "EXCLUDED" for row in owners)
        and [row["origin_key"] for row in origins] == list(bundle.origin_keys)
        and [row["cell_key"] for row in cells] == sorted(row["cell_key"] for row in cells)
        and lineage["Round176_prior_closed"] == EXPECTED_PRIOR_CLOSED
        and lineage["Round176_preclosed_frontier"] == EXPECTED_PRECLOSED_FRONTIER
        and lineage["Round176_residual_roots"] == EXPECTED_RESIDUAL_ROOTS
        and lineage["Round180_inherited_excluded"] == EXPECTED_INHERITED_TERMINALS
        and lineage["Round180_final"] == EXPECTED_FINAL_CELLS
        and lineage["sealed_C30a_clipped_excluded"] == EXPECTED_C30A_CLIPPED_CELLS
        and lineage["Round306C30D_multi_Delta_excluded"] == EXPECTED_MULTI_CELLS
        and all(row["whole_closed_cell_excluded"] is True for row in cells)
        and all(row["whole_origin_disposition_candidate"] == "EXCLUDED" for row in origins)
        and producer_module_absent(),
        "independent complete C30d-v3 census",
    )
    return {
        "input_pins": input_pins,
        "pin_map": pin_map,
        "origin_keys": list(bundle.origin_keys),
        "cells": cells,
        "owners": owners,
        "origins": origins,
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
    need(after["remaining"] == sum(partition.values()) == 58, "derived 58 remainder")
    need(after["excluded"] + after["conservative_live"] == after["total"] == 76_832, "derived conservation")
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


def controlled_runtime_contract() -> dict[str, Any]:
    return {
        "schema": "cm2.round306c30d.controlled-seed-runtime-contract.v1",
        "launcher_contract": "ENV_I_EXACT_4_VARIABLES__ABSOLUTE_PINNED_PYTHON_-P_-s_-B",
        "accepted_seeds": [30630071, 30630929],
        "sentinel": HASH_SEED_SENTINEL,
        "accepted_hash_fingerprints": {key: HASH_FINGERPRINTS[key] for key in sorted(HASH_FINGERPRINTS)},
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
    }


def ledger_descriptor(path: Path, rows: list[dict[str, Any]], order: str) -> dict[str, Any]:
    sequence = hashlib.sha256()
    for row in rows:
        sequence.update(bytes.fromhex(row["row_sha256"]))
    return {
        "filename": path.name,
        "row_count": len(rows),
        "size": path.lstat().st_size,
        "sha256": file_hash(path, "candidate ledger:" + path.name),
        "row_sequence_sha256": sequence.hexdigest(),
        "order": order,
    }


def expected_result_body(
    projection: dict[str, Any],
    reference: dict[str, Any],
    cell_descriptor: dict[str, Any],
    owner_descriptor: dict[str, Any],
    origin_descriptor: dict[str, Any],
) -> dict[str, Any]:
    candidate_theorem = theorem()
    transition = derive_transition(projection)
    return {
        "schema": "cm2.round306c30d.source-w-multi-delta-whole-origin-exclusion.candidate.v3",
        "status": (
            "PASS_CANDIDATE_C30D_V3__1176_MULTI_DELTA_CELLS__"
            "20_WHOLE_ORIGINS_EXCLUDED__ZERO_FORMAL_CREDIT__UNAUTHORIZED"
        ),
        "producer_contract": {
            "source": NEW_PRODUCER_REL,
            "source_sha256": NEW_PRODUCER_SHA256,
            "frozen_mathematical_kernel": MATH_PRODUCER_REL,
            "frozen_mathematical_kernel_sha256": MATH_PRODUCER_SHA256,
            "predecessor_adapter": AUTHORITY_ADAPTER_REL,
            "predecessor_adapter_sha256": AUTHORITY_ADAPTER_SHA256,
        },
        "input_pins": reference["input_pins"],
        "runtime": {
            "attestation_source": RUNTIME_ATTESTATION_REL,
            "attestation_filename": RUNTIME_ATTESTATION_NAME,
            "attestation_sha256": RUNTIME_ATTESTATION_SHA256,
            "controlled_seed_contract": controlled_runtime_contract(),
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
            "origin_keys": reference["origin_keys"],
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


def canonical_rows(path: Path) -> list[dict[str, Any]]:
    absolute = Path(os.path.abspath(os.fspath(path)))
    need(absolute.resolve(strict=True) == absolute, "canonical ledger path")
    before = absolute.lstat()
    need(stat.S_ISREG(before.st_mode) and before.st_nlink == 1 and not absolute.is_symlink(), "ledger singleton")
    rows: list[dict[str, Any]] = []
    with absolute.open("rb") as header:
        prefix = header.read(10)
    need(len(prefix) == 10 and prefix[:2] == b"\x1f\x8b" and int.from_bytes(prefix[4:8], "little") == 0, "deterministic gzip header")
    with gzip.open(absolute, "rb") as stream:
        for ordinal, line in enumerate(stream):
            need(line.endswith(b"\n"), "ledger newline:" + str(ordinal))
            row = strict_object(line[:-1], path.name + ":" + str(ordinal))
            body = dict(row)
            claimed = body.pop("row_sha256", None)
            need(
                canonical(row) + b"\n" == line
                and type(claimed) is str
                and claimed == object_digest(body),
                "canonical row closure:" + str(ordinal),
            )
            rows.append(row)
    after = absolute.lstat()
    need(identity(before) == identity(after), "ledger TOCTOU identity")
    return rows


def validate_candidate_directory(candidate_path: Path, projection: dict[str, Any], reference: dict[str, Any]) -> dict[str, Any]:
    candidate = Path(os.path.abspath(os.fspath(candidate_path)))
    need(candidate.resolve(strict=True) == candidate, "canonical candidate path")
    directory_before = candidate.lstat()
    need(stat.S_ISDIR(directory_before.st_mode) and not candidate.is_symlink(), "candidate directory")
    expected_names = {RUNTIME_ATTESTATION_NAME, CELL_LEDGER, ATOMIC_OWNER_LEDGER, ORIGIN_LEDGER, RESULT}
    names = {entry.name for entry in os.scandir(candidate)}
    need(names == expected_names, "exact candidate file set")
    for name in names:
        facts = (candidate / name).lstat()
        need(stat.S_ISREG(facts.st_mode) and facts.st_nlink == 1 and not (candidate / name).is_symlink(), "candidate singleton:" + name)
    runtime_raw = read_singleton(candidate / RUNTIME_ATTESTATION_NAME, 4 << 20, "candidate runtime")
    need(
        hashlib.sha256(runtime_raw).hexdigest() == RUNTIME_ATTESTATION_SHA256
        and runtime_raw == read_singleton(WORKSPACE / RUNTIME_ATTESTATION_REL, 4 << 20, "sealed runtime"),
        "correct sealed C30b runtime attestation",
    )
    cells = canonical_rows(candidate / CELL_LEDGER)
    owners = canonical_rows(candidate / ATOMIC_OWNER_LEDGER)
    origins = canonical_rows(candidate / ORIGIN_LEDGER)
    need(
        len(cells) == len(reference["cells"]) == EXPECTED_MULTI_CELLS
        and len(owners) == len(reference["owners"])
        and len(origins) == len(reference["origins"]) == EXPECTED_ORIGINS
        and cells == reference["cells"]
        and owners == reference["owners"]
        and origins == reference["origins"],
        "independent byte-semantic mathematical reconstruction",
    )
    need(
        all(row.get("formal_credit") == CELL_ZERO_FORMAL for row in cells)
        and all(row.get("formal_credit") == ORIGIN_ZERO_FORMAL for row in origins)
        and all(row.get("owner_disposition") == "EXCLUDED" for row in owners),
        "zero-credit row boundary",
    )
    cell_descriptor = ledger_descriptor(candidate / CELL_LEDGER, cells, "LEXICOGRAPHIC_ROUND180_FINAL_CELL_KEY")
    owner_descriptor = ledger_descriptor(
        candidate / ATOMIC_OWNER_LEDGER,
        owners,
        "ORIGIN_KEY_THEN_DIMENSION_3_TO_0_THEN_LEAF_KEY_OR_CANONICAL_GEOMETRY",
    )
    origin_descriptor = ledger_descriptor(candidate / ORIGIN_LEDGER, origins, "LEXICOGRAPHIC_SOURCE_W_ORIGIN_KEY")
    result_raw = read_singleton(candidate / RESULT, 32 << 20, "candidate result")
    result = strict_object(result_raw, "candidate result")
    body = dict(result)
    claimed = body.pop("result_sha256", None)
    expected_body = expected_result_body(projection, reference, cell_descriptor, owner_descriptor, origin_descriptor)
    need(
        result_raw == canonical(result)
        and type(claimed) is str
        and claimed == object_digest(body)
        and body == expected_body
        and result.get("formal_credit") == ZERO_FORMAL
        and result.get("strict_nonpromotion", {}).get("C30d_transition_authorized") is False,
        "exact C30d-v3 candidate result",
    )
    for relative, expected in reference["pin_map"].items():
        need(file_hash(WORKSPACE / relative, "input replay:" + relative) == expected, "input TOCTOU:" + relative)
    need(
        identity(directory_before) == identity(candidate.lstat())
        and {entry.name for entry in os.scandir(candidate)} == names
        and producer_module_absent(),
        "candidate directory TOCTOU and no producer import",
    )
    return {
        "schema": "cm2.round306c30d.source-w-multi-delta-whole-origin-exclusion.independent-verification.v3",
        "status": (
            "PASS_NO_IMPORT_INDEPENDENT_C30D_V3__1176_CELLS__20_EXCLUDED_ORIGINS__"
            "ZERO_FORMAL_CREDIT__MANIFEST_UNAUTHORIZED"
        ),
        "candidate_result_sha256": result["result_sha256"],
        "candidate_files": {
            name: file_hash(candidate / name, "candidate replay:" + name)
            for name in sorted(names)
        },
        "whole_origin_disposition_census": {"EXCLUDED": EXPECTED_ORIGINS},
        "formal_credit": ZERO_FORMAL,
        "manifest_authorized": False,
        "C30d_transition_authorized": False,
        "source_W_formal_remainder": projection["predecessor_formal_handoff"]["after"]["remaining"],
        "D02": "BLOCKED_COMPOSITE",
        "D03": "UNAUTHORIZED",
        "D04": "NOT_MINTED",
        "Gate5": "10/18",
        "CM2": "NO-GO_FOR_CLAIM",
    }


def verify(chain_dir: Path, pins_path: Path, candidate: Path) -> dict[str, Any]:
    independent_runtime_guard()
    projection = run_authority(chain_dir, pins_path)
    legacy = load_math_verifier()
    reference = reconstruct_reference(legacy, projection, Path(os.path.abspath(os.fspath(pins_path))))
    replay = run_authority(chain_dir, pins_path)
    need(canonical(replay) == canonical(projection), "authority TOCTOU projection")
    return validate_candidate_directory(candidate, projection, reference)


def fixture_projection() -> dict[str, Any]:
    return {
        "predecessor_formal_handoff": {
            "after": {
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
        }
    }


def self_test() -> dict[str, Any]:
    transition = derive_transition(fixture_projection())
    need(transition["before"]["remaining"] == 78 and transition["after"]["remaining"] == 58, "fixture transition")
    source = read_singleton(Path(__file__).resolve(), 8 << 20, "self source")
    tree = ast.parse(source)
    imports = [node for node in ast.walk(tree) if isinstance(node, (ast.Import, ast.ImportFrom))]
    need(
        all(
            NEW_PRODUCER_REL not in canonical(ast.dump(node)).decode("ascii")
            and Path(NEW_PRODUCER_REL).stem not in canonical(ast.dump(node)).decode("ascii")
            for node in imports
        ),
        "no producer import syntax",
    )
    suspicious: list[int] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == "need" and node.args:
            first = node.args[0]
            if isinstance(first, ast.BoolOp) and isinstance(first.values[-1], (ast.Name, ast.Attribute, ast.Subscript)):
                suspicious.append(node.lineno)
    need(not suspicious, "exact-bool static audit")
    return {
        "schema": "cm2.round306c30d.v3-independent-verifier-self-test.v1",
        "status": "PASS_C30D_V3_NO_IMPORT_VERIFIER_STATIC_FIXTURES__ZERO_FORMAL_CREDIT",
        "producer_imported_or_executed": False,
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
            "complete verifier arguments",
        )
        output = verify(arguments.chain_dir, arguments.dynamic_pins, arguments.candidate_dir)
    except (Reject, OSError, ValueError, TypeError, KeyError, AssertionError, subprocess.SubprocessError):
        return 2
    print(canonical(output).decode("ascii"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
