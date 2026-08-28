#!/usr/bin/env python3
"""Small shared primitives for the append-only CM2 Round-66 certificates."""

from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path
from typing import Any, Callable


class CertError(RuntimeError):
    pass


def require(condition: bool, label: str) -> None:
    if not condition:
        raise CertError(label)


def strict_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for key, value in pairs:
        if key in out:
            raise CertError(f"duplicate JSON key: {key}")
        out[key] = value
    return out


def reject_constant(token: str) -> None:
    raise CertError(f"non-finite JSON token: {token}")


def strict_json_text(text: str) -> Any:
    return json.loads(
        text,
        object_pairs_hook=strict_object,
        parse_constant=reject_constant,
    )


def strict_json_path(path: Path) -> dict[str, Any]:
    value = strict_json_text(path.read_text(encoding="utf-8"))
    require(isinstance(value, dict), f"JSON root is not an object: {path.name}")
    return value


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False)


def canonical_bytes(value: Any) -> bytes:
    return (canonical_json(value) + "\n").encode("utf-8")


def digest(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def sha256_path(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def validate_pins(here: Path, pins: dict[str, str]) -> None:
    for name, expected in pins.items():
        path = here / name
        require(path.is_file() and not path.is_symlink(), f"pin file/type: {name}")
        require(path.resolve().parent == here.resolve(), f"pin parent: {name}")
        require(sha256_path(path) == expected, f"pin hash: {name}")


def replay_sidecar(here: Path, sidecar: Path, expected_rows: int) -> int:
    rows = [line.strip() for line in sidecar.read_text(encoding="utf-8").splitlines()
            if line.strip()]
    require(len(rows) == expected_rows, f"sidecar row count: {sidecar.name}")
    seen: set[Path] = set()
    for row in rows:
        parts = row.split(maxsplit=1)
        require(len(parts) == 2, f"sidecar syntax: {row}")
        expected, token = parts
        require(len(expected) == 64 and all(c in "0123456789abcdef" for c in expected),
                f"sidecar digest syntax: {row}")
        target = (here.parent / token if token.startswith("deliverables/") else here / token).resolve()
        require(target.parent == here.resolve(), f"sidecar parent: {token}")
        require(target not in seen, f"sidecar duplicate: {token}")
        seen.add(target)
        require(target.is_file() and not target.is_symlink(), f"sidecar file/type: {token}")
        require(sha256_path(target) == expected, f"sidecar hash: {token}")
    return len(rows)


def deep_paths(value: Any, prefix: tuple[Any, ...] = ()) -> list[tuple[Any, ...]]:
    out: list[tuple[Any, ...]] = []
    if isinstance(value, dict):
        for key, child in value.items():
            if key != "internal_replay_digest":
                out.extend(deep_paths(child, prefix + (key,)))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            out.extend(deep_paths(child, prefix + (index,)))
    else:
        out.append(prefix)
    return out


def get_path(root: Any, path: tuple[Any, ...]) -> Any:
    node = root
    for step in path:
        node = node[step]
    return node


def set_path(root: Any, path: tuple[Any, ...], value: Any) -> None:
    node = root
    for step in path[:-1]:
        node = node[step]
    node[path[-1]] = value


def hostile_value(value: Any) -> Any:
    if isinstance(value, bool):
        return not value
    if isinstance(value, int):
        return value + 1
    if isinstance(value, str):
        return value + "__HOSTILE"
    if value is None:
        return "HOSTILE"
    return {"hostile": True}


def semantic_mutation_test(
    manifest: dict[str, Any],
    integrity: Callable[[dict[str, Any], bool], None],
    semantics: Callable[[dict[str, Any]], None],
) -> int:
    paths = deep_paths(manifest["result"])
    require(paths, "empty hostile path set")
    rejected = 0
    for path in paths:
        mutant = copy.deepcopy(manifest)
        result = mutant["result"]
        set_path(result, path, hostile_value(get_path(result, path)))
        replay = copy.deepcopy(result)
        replay.pop("internal_replay_digest", None)
        result["internal_replay_digest"] = digest(replay)
        mutant["verdict"] = result.get("strict_status")
        try:
            integrity(mutant, False)
            semantics(result)
        except (CertError, KeyError, ValueError, TypeError, IndexError, ArithmeticError):
            rejected += 1
    require(rejected == len(paths), f"hostile semantic accepted: {rejected}/{len(paths)}")
    return rejected


def strict_json_self_test() -> int:
    payloads = ['{"x":1,"x":2}', '{"x":NaN}', '{"x":Infinity}', '{"x":-Infinity}']
    rejected = 0
    for payload in payloads:
        try:
            strict_json_text(payload)
        except (CertError, ValueError):
            rejected += 1
    require(rejected == len(payloads), "hostile strict JSON accepted")
    return rejected
