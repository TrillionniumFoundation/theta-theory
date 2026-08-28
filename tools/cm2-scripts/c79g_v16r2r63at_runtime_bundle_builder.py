#!/usr/bin/env python3
"""Append-only r63at successor correcting the r63as proof projection."""
from __future__ import annotations

import hashlib
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "scripts/c79g_v16r2r63as_runtime_bundle_builder.py"
TEMPLATE_SHA256 = "41f24d45260c489718051ccc42399de149d17fb23627bc71bb4d65c5b22be760"


def main(argv: list[str] | None = None) -> int:
    raw = TEMPLATE.read_bytes()
    if hashlib.sha256(raw).hexdigest() != TEMPLATE_SHA256:
        raise RuntimeError("immutable r63as builder template hash drift")
    text = raw.decode("utf-8").replace("r63as", "r63at").replace("R63AS", "R63AT")

    old_head = (
        "def _r63at_project_v4_exact8_for_schema(freeze_proof):\n"
        "    raw = _expected_v4_provisional_exact8()\n"
    )
    new_head = (
        "def _r63at_project_v4_proof_for_schema(freeze_proof):\n"
        "    proof = v4_rejection_supersession_proof(freeze_proof)\n"
        "    if not isinstance(proof, dict):\n"
        "        raise RuntimeError(\"r63at v4 proof is not an object\")\n"
        "    raw = proof.get(\"ordered_provisional_exact8\")\n"
    )
    if text.count(old_head) != 1:
        raise RuntimeError("r63at v4 helper head anchor drift")
    text = text.replace(old_head, new_head, 1)

    old_tail = "    return projected\n"
    new_tail = (
        "    proof[\"ordered_provisional_exact8\"] = projected\n"
        "    return proof\n"
    )
    if text.count(old_tail) != 1:
        raise RuntimeError("r63at v4 helper tail anchor drift")
    text = text.replace(old_tail, new_tail, 1)

    old_call = "            _r63at_project_v4_exact8_for_schema(freeze_proof),"
    new_call = "            _r63at_project_v4_proof_for_schema(freeze_proof),"
    if text.count(old_call) != 1:
        raise RuntimeError("r63at v4 helper call anchor drift")
    text = text.replace(old_call, new_call, 1)

    ns = {
        "__name__": "_c79g_r63at_builder_template",
        "__file__": str(ROOT / "scripts/c79g_v16r2r63at_runtime_bundle_builder.py"),
    }
    exec(compile(text, str(TEMPLATE), "exec"), ns, ns)
    return int(ns["main"](sys.argv[1:] if argv is None else argv))


if __name__ == "__main__":
    raise SystemExit(main())
