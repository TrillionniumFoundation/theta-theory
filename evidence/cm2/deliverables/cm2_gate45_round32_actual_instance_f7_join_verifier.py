#!/usr/bin/env python3
"""Fail-closed verifier for the round-32 actual-instance F7 join."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

import cm2_gate45_round32_actual_instance_f7_join_cert as cert


def pairs(rows: list[tuple[str, Any]]) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for key, value in rows:
        if key in out:
            raise ValueError(f"duplicate key: {key}")
        out[key] = value
    return out


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=pairs,
                       parse_constant=lambda token: (_ for _ in ()).throw(ValueError(token)))
    if not isinstance(value, dict):
        raise ValueError("manifest root")
    return value


def verify(path: Path) -> list[str]:
    errors: list[str] = []
    try:
        manifest = load(path)
        if manifest.get("schema") != cert.MANIFEST_SCHEMA:
            errors.append("schema")
        if manifest.get("certificate_sha256") != sha(Path(cert.__file__).resolve()):
            errors.append("certificate hash")
        if manifest.get("verifier_sha256") != sha(Path(__file__).resolve()):
            errors.append("verifier hash")
        if manifest.get("dependencies") != cert.DEPENDENCIES:
            errors.append("dependencies")
        if manifest.get("result") != cert.build_result():
            errors.append("replay")
        join = manifest["result"]["same_ID_actual_instance_F7_join"]
        if join["one_step_numeric_F7_strict_upper"] != "360134800/360493663":
            errors.append("F7 coefficient")
        if join["one_step_F7_is_strict_contraction"] is not True:
            errors.append("F7 contraction")
        if manifest["result"]["Gate5_maturity_update"]["current_global_maturity"] != "5/18":
            errors.append("maturity")
        if manifest["verdict"]["CM2"] != "NO-GO_FOR_CLAIM":
            errors.append("fail-close")
    except Exception as exc:
        errors.append(f"exception: {exc}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("manifest", nargs="?", type=Path, default=cert.DEFAULT_MANIFEST)
    parser.add_argument("--integrity-only", action="store_true")
    args = parser.parse_args()
    errors = verify(args.manifest)
    if errors:
        print("VERIFY: FAIL")
        for error in errors:
            print(error)
        return 1
    print("VERIFY: PASS")
    print("GATE5_MATURITY: 5/18")
    print("CM2: NO-GO_FOR_CLAIM")
    return 0 if args.integrity_only else 2


if __name__ == "__main__":
    raise SystemExit(main())
