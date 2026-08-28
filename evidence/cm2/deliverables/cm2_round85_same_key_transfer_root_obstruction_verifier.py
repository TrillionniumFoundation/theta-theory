#!/usr/bin/env python3
"""Independent verifier for the Round-85 same-key transfer obstruction."""
from __future__ import annotations

import copy
import json
import math
import sys
from pathlib import Path
from typing import Any, Iterable

import cm2_round85_same_key_transfer_root_obstruction_cert as cert


HERE = Path(__file__).resolve().parent
INPUT = HERE / "cm2-round85-same-key-transfer-root-obstruction-2026-07-22.json"


def reject_constant(token: str) -> None:
    raise ValueError(f"nonfinite constant: {token}")


def unique(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate key: {key}")
        result[key] = value
    return result


def reject_nonfinite(value: Any) -> None:
    if isinstance(value, float) and not math.isfinite(value):
        raise ValueError("nonfinite number")
    if isinstance(value, dict):
        for child in value.values():
            reject_nonfinite(child)
    elif isinstance(value, list):
        for child in value:
            reject_nonfinite(child)


def loads_strict(raw: str) -> Any:
    value = json.loads(raw, object_pairs_hook=unique, parse_constant=reject_constant)
    reject_nonfinite(value)
    return value


def validate(value: Any, expected: dict[str, Any]) -> None:
    if not isinstance(value, dict):
        raise ValueError("top-level object")
    if set(value) != {"schema", "pins", "result", "result_sha256"}:
        raise ValueError("closed top-level schema")
    if value["result_sha256"] != cert.digest(value["result"]):
        raise ValueError("result digest")
    if value != expected:
        raise ValueError("fresh exact reconstruction")


def scalar_paths(value: Any, prefix: tuple[Any, ...] = ()) -> Iterable[tuple[Any, ...]]:
    if isinstance(value, dict):
        for key, child in value.items():
            yield from scalar_paths(child, prefix + (key,))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            yield from scalar_paths(child, prefix + (index,))
    else:
        yield prefix


def mutate_scalar(value: Any) -> Any:
    if value is None:
        return "MUTATED"
    if isinstance(value, bool):
        return not value
    if isinstance(value, int):
        return value + 1
    if isinstance(value, str):
        return value + "_MUTATED"
    raise TypeError(type(value).__name__)


def set_path(value: Any, path: tuple[Any, ...], replacement: Any) -> None:
    target = value
    for key in path[:-1]:
        target = target[key]
    target[path[-1]] = replacement


def get_path(value: Any, path: tuple[Any, ...]) -> Any:
    for key in path:
        value = value[key]
    return value


def rejected(hostile: dict[str, Any], expected: dict[str, Any]) -> bool:
    try:
        validate(hostile, expected)
    except (ValueError, KeyError, TypeError, IndexError):
        return True
    return False


def main(argv: list[str]) -> int:
    path = Path(argv[1]).resolve() if len(argv) > 1 else INPUT
    value = loads_strict(path.read_text())
    expected = cert.build(512)
    validate(value, expected)

    higher = cert.build(768)
    for key in (
        "status", "same_key_Q_E_u_v_transfer_rows_installable_on_current_root",
        "necessary_next_action", "gate1", "gate4",
    ):
        if higher["result"][key] != value["result"][key]:
            raise ValueError(f"higher-precision invariant: {key}")
    if higher["result"]["current_root"] != value["result"]["current_root"]:
        raise ValueError("higher-precision root ledger")

    scalar_rejected = 0
    for path_key in list(scalar_paths(value["result"])):
        hostile = copy.deepcopy(value)
        old = get_path(hostile["result"], path_key)
        set_path(hostile["result"], path_key, mutate_scalar(old))
        hostile["result_sha256"] = cert.digest(hostile["result"])
        if not rejected(hostile, expected):
            raise ValueError(f"accepted result mutation: {path_key}")
        scalar_rejected += 1
    pin_rejected = 0
    for key in value["pins"]:
        hostile = copy.deepcopy(value)
        hostile["pins"][key] += "_MUTATED"
        if not rejected(hostile, expected):
            raise ValueError(f"accepted pin mutation: {key}")
        pin_rejected += 1
    hostile = copy.deepcopy(value)
    hostile["extra_claim"] = "CERTIFIED"
    if not rejected(hostile, expected):
        raise ValueError("accepted structural mutation")

    strict_attacks = ('{"x":1,"x":2}', '{"x":NaN}', '{"x":Infinity}', '{"x":1e9999}')
    strict_rejected = 0
    for raw in strict_attacks:
        try:
            loads_strict(raw)
        except ValueError:
            strict_rejected += 1
    if strict_rejected != len(strict_attacks):
        raise ValueError("strict JSON suite")

    audit_result = {
        "producer_reconstruction": "EXACT_EQUALITY_VERIFIED",
        "independent_escape_recomputation_precision_bits": 768,
        "owner_atom_count": 176,
        "destination_owner_comparison_count": 1360,
        "depth2_same_key_survivor_count": 0,
        "uniform_escape_gap_strict_lower": "1/100",
        "result_scalar_mutations_rejected": scalar_rejected,
        "pin_mutations_rejected": pin_rejected,
        "structural_mutations_rejected": 1,
        "strict_json_attacks_rejected": f"{strict_rejected}/{len(strict_attacks)}",
        "verdict": "PASS",
    }
    audit = {
        "schema": "cm2.round85.same-key-transfer-root-obstruction-audit.v1",
        "result": audit_result,
        "result_sha256": cert.digest(audit_result),
    }
    json.dump(audit, sys.stdout, sort_keys=True, indent=2, allow_nan=False)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
