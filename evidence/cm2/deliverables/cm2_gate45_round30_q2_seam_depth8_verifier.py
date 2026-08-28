#!/usr/bin/env python3
"""Fail-closed verifier for the round-30 Q2 seam depth-eight leaf."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

import cm2_gate45_round30_q2_seam_depth8_cert as cert


def no_duplicates(rows: list[tuple[str, Any]]) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for key, value in rows:
        if key in out:
            raise ValueError(f"duplicate key: {key}")
        out[key] = value
    return out


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=no_duplicates,
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
        cert.verify_dependencies()
        cert.validate_result(manifest["result"])
        if manifest.get("verdict") != manifest["result"]["Gate5_frontier"]:
            errors.append("verdict")
    except Exception as exc:
        errors.append(f"exception: {exc}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("manifest", nargs="?", type=Path, default=cert.DEFAULT_MANIFEST)
    parser.add_argument("--replay", action="store_true")
    args = parser.parse_args()
    errors = verify(args.manifest)
    if errors:
        print("VERIFY: FAIL")
        for error in errors:
            print(error)
        return 1
    if args.replay:
        replayed = cert.build_result()
        if replayed != load(args.manifest)["result"]:
            print("VERIFY: FAIL\nreplay mismatch")
            return 1
        print("VERIFY: PASS")
        return 0
    print("VERIFY: PASS")
    print("CM2: NO-GO_FOR_CLAIM")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
