#!/usr/bin/env python3
"""Superseding canonical JSON closure for the Round292 R289/R291 audit.

Round292's mathematical build is retained byte-for-byte as the baseline.  Its
only result-object defect is serialization closure: one histogram was built
with integer keys, so numeric in-memory key ordering differs from the
lexicographic string-key ordering after a JSON round trip.  This producer
reruns that frozen mathematical build, recursively normalizes every mapping
key to a string before any enclosing commitment is computed, and emits a new
Round293 result and deterministic gzip ledger.  It never writes a Round292
artifact and it awards no mathematical credit.
"""

from __future__ import annotations

import gzip
import hashlib
import importlib.util
import io
import json
import os
from pathlib import Path
import tempfile
from types import ModuleType
from typing import Any


HERE = Path(__file__).resolve().parent
PREFIX = "cm2_round293_source_g_r289_r291_witness_binding_canonical_closure"
RESULT = HERE / f"{PREFIX}_result.json"
LEDGER = HERE / f"{PREFIX}_ledger.json.gz"

BASELINE_NAME = "cm2_round292_source_g_r289_r291_witness_binding_audit_probe"
BASELINE_PRODUCER = HERE / f"{BASELINE_NAME}.py"
BASELINE_RESULT = HERE / f"{BASELINE_NAME}_result.json"
BASELINE_LEDGER = HERE / f"{BASELINE_NAME}_ledger.json.gz"

BASELINE_PINS = {
    BASELINE_PRODUCER.name:
        "72ff71aa4e74c2d4274afb760879d11d63ffae09dbfe9e6773519ee7a5abc163",
    BASELINE_RESULT.name:
        "07ced5c6e0f5c06b4f22019deda6c770341b264b654fe6ddb9a8f44ec68472ca",
    BASELINE_LEDGER.name:
        "5602f3bd5860ca70277f820e36b602273d7253073c4c4ba6111f6eff2f500570",
}

ROUND292_IN_MEMORY_RESULT_SHA256 = (
    "919634dc108d9bf06c6b40209b8245f223ae52e2909fb76c71a1e9c25f291db0"
)
ROUND292_PERSISTED_RESULT_RECOMPUTED_SHA256 = (
    "ea99ee814e41fe22ea55ba04682fc44d3a5538aab1e41ccd7a154160a538c670"
)
SCHEMA = "cm2.round293.r289-r291-witness-binding-canonical-closure.v1"
LEDGER_SCHEMA = SCHEMA + ".ledger.v1"


def canonical(value: Any) -> bytes:
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=True
    ).encode()


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def file_sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def need(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def normalize_mapping_keys(value: Any, path: str = "$") -> Any:
    """Return an isomorphic JSON value whose mapping keys are all strings."""
    if isinstance(value, dict):
        result: dict[str, Any] = {}
        for key, child in value.items():
            text_key = key if isinstance(key, str) else str(key)
            need(
                text_key not in result,
                f"mapping-key normalization collision at {path}.{text_key}",
            )
            result[text_key] = normalize_mapping_keys(
                child, f"{path}.{text_key}"
            )
        return result
    if isinstance(value, list):
        return [
            normalize_mapping_keys(child, f"{path}[{index}]")
            for index, child in enumerate(value)
        ]
    need(
        value is None or isinstance(value, (str, int, float, bool)),
        f"non-JSON value at {path}",
    )
    return value


def all_mapping_keys_are_strings(value: Any) -> bool:
    if isinstance(value, dict):
        return all(
            isinstance(key, str) and all_mapping_keys_are_strings(child)
            for key, child in value.items()
        )
    if isinstance(value, list):
        return all(map(all_mapping_keys_are_strings, value))
    return True


def deterministic_gzip_bytes(value: Any) -> bytes:
    output = io.BytesIO()
    with gzip.GzipFile(
        filename="", mode="wb", fileobj=output, mtime=0
    ) as handle:
        handle.write(canonical(value))
    return output.getvalue()


def atomic_write(path: Path, payload: bytes) -> None:
    descriptor, temporary = tempfile.mkstemp(
        prefix="." + path.name + ".", dir=path.parent
    )
    try:
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(payload)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def read_json(path: Path) -> dict[str, Any]:
    with path.open("rb") as handle:
        value = json.load(handle)
    need(isinstance(value, dict), f"JSON object:{path.name}")
    return value


def load_frozen_baseline() -> ModuleType:
    for name, expected in BASELINE_PINS.items():
        need(file_sha256(HERE / name) == expected, f"baseline pin:{name}")
    spec = importlib.util.spec_from_file_location(
        "_cm2_round292_witness_binding_frozen_baseline", BASELINE_PRODUCER
    )
    need(spec is not None and spec.loader is not None, "baseline import spec")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def build() -> tuple[dict[str, Any], dict[str, Any]]:
    baseline = load_frozen_baseline()
    baseline_ledger_raw, baseline_result_raw = baseline.build()
    need(
        baseline_result_raw["result_sha256"]
        == ROUND292_IN_MEMORY_RESULT_SHA256,
        "frozen Round292 in-memory commitment",
    )

    persisted = read_json(BASELINE_RESULT)
    persisted_claim = persisted.pop("result_sha256")
    need(
        persisted_claim == ROUND292_IN_MEMORY_RESULT_SHA256,
        "frozen Round292 persisted claim",
    )
    need(
        digest(persisted)
        == ROUND292_PERSISTED_RESULT_RECOMPUTED_SHA256
        != persisted_claim,
        "frozen Round292 serialization defect witness",
    )

    baseline_result_raw = dict(baseline_result_raw)
    baseline_result_raw.pop("result_sha256")
    normalized_baseline_result = normalize_mapping_keys(baseline_result_raw)
    need(
        normalized_baseline_result == persisted,
        "normalized fresh baseline equals persisted JSON semantics",
    )
    need(
        digest(normalized_baseline_result)
        == ROUND292_PERSISTED_RESULT_RECOMPUTED_SHA256,
        "normalized baseline digest",
    )

    ledger = normalize_mapping_keys(baseline_ledger_raw)
    ledger["schema"] = LEDGER_SCHEMA
    ledger["status"] = (
        "PASS_ZERO_CREDIT__ROUND293_CANONICAL_LEDGER_CLOSURE__"
        "ROUND292_ROW_PAYLOADS_PRESERVED"
    )
    ledger["canonical_closure"] = {
        "all_mapping_keys_are_strings": True,
        "row_payloads_and_row_sha256_preserved": True,
        "superseded_ledger_filename": BASELINE_LEDGER.name,
        "superseded_ledger_file_sha256":
            BASELINE_PINS[BASELINE_LEDGER.name],
    }
    need(all_mapping_keys_are_strings(ledger), "ledger string mapping keys")
    ledger_bytes = deterministic_gzip_bytes(ledger)

    result = normalized_baseline_result
    result["schema"] = SCHEMA
    result["status"] = (
        "PASS_ZERO_CREDIT__ROUND293_CANONICAL_JSON_CLOSURE__"
        "R289_R291_AUDIT__UNRESOLVED_OBLIGATIONS_RETAINED_FAIL_CLOSED"
    )
    result["ledger"]["filename"] = LEDGER.name
    result["ledger"]["file_sha256"] = hashlib.sha256(ledger_bytes).hexdigest()
    result["canonical_closure"] = {
        "all_mapping_keys_normalized_to_strings_before_commitment": True,
        "normalized_histogram_paths": [
            "Round289.tail_directed_endpoint_target_count_histogram",
        ],
        "result_sha256_definition":
            "SHA256_CANONICAL_JSON_OF_RESULT_WITHOUT_RESULT_SHA256",
        "round292_in_memory_result_sha256":
            ROUND292_IN_MEMORY_RESULT_SHA256,
        "round292_persisted_result_recomputed_sha256":
            ROUND292_PERSISTED_RESULT_RECOMPUTED_SHA256,
        "round292_result_round_trip_closed": False,
        "round293_result_round_trip_closed": True,
        "superseded_producer_filename": BASELINE_PRODUCER.name,
        "superseded_producer_sha256":
            BASELINE_PINS[BASELINE_PRODUCER.name],
        "superseded_result_filename": BASELINE_RESULT.name,
        "superseded_result_file_sha256":
            BASELINE_PINS[BASELINE_RESULT.name],
    }
    need(
        result["Round289"]["actual_relation_uncovered_subcell_count"] == 396
        and result["Round291"]["physical_witness_unresolved_count"] == 576,
        "unresolved obligations preserved",
    )
    need(
        all_mapping_keys_are_strings(result),
        "result string mapping keys before commitment",
    )
    result["result_sha256"] = digest(result)

    # The defining closure is checked against the value parsed from the exact
    # bytes that will be written, not merely against the in-memory object.
    result_bytes = canonical(result) + b"\n"
    round_trip = json.loads(result_bytes)
    round_trip_claim = round_trip.pop("result_sha256")
    need(
        round_trip_claim == digest(round_trip),
        "Round293 persisted JSON result closure",
    )
    need(
        all_mapping_keys_are_strings(round_trip),
        "Round293 round-trip string mapping keys",
    )
    return ledger, result


def main() -> None:
    ledger, result = build()
    ledger_bytes = deterministic_gzip_bytes(ledger)
    result_bytes = canonical(result) + b"\n"
    atomic_write(LEDGER, ledger_bytes)
    atomic_write(RESULT, result_bytes)
    print(json.dumps({
        "status": result["status"],
        "Round289_unresolved_subcells":
            result["Round289"]["actual_relation_uncovered_subcell_count"],
        "Round291_unresolved_witnesses":
            result["Round291"]["physical_witness_unresolved_count"],
        "ledger_sha256": hashlib.sha256(ledger_bytes).hexdigest(),
        "result_sha256": result["result_sha256"],
        "persisted_result_closure": True,
    }, sort_keys=True, indent=2))


if __name__ == "__main__":
    main()
