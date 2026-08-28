#!/usr/bin/env python3
from __future__ import annotations

import copy
import hashlib
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any, Callable


ROOT = Path(__file__).resolve().parent
PREFIX = "cm2_round306c25_source_g_502204_member_549616_representation_typed_global_support_ledger"
RESULT = PREFIX + "_result.json"
VERIFIER = ROOT / (PREFIX + "_independent_verifier.py")
PYTHON = ROOT.parent / ".venv-cm2/bin/python"


def canonical(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=True, allow_nan=False, sort_keys=True, separators=(",", ":")).encode("ascii")


def close(value: dict[str, Any]) -> dict[str, Any]:
    body = dict(value)
    body.pop("result_sha256", None)
    return {**body, "result_sha256": hashlib.sha256(canonical(body)).hexdigest()}


def main() -> int:
    candidate = Path(sys.argv[1]).resolve()
    base = json.loads((candidate / RESULT).read_bytes())
    attacks: list[tuple[str, Callable[[dict[str, Any]], None]]] = [
        ("member_count", lambda value: value["corrected_universe_census"].__setitem__("members", 502203)),
        ("representation_count", lambda value: value["corrected_universe_census"].__setitem__("representations", 549615)),
        ("base_roots", lambda value: value["corrected_universe_census"].__setitem__("authorized_base_roots", 339035)),
        ("set_equality", lambda value: value["global_credit"].__setitem__("representation_set_equality", 538679)),
        ("source_census", lambda value: value["member_support_source_census"].__setitem__("C24B", 167)),
        ("typed_ledger", lambda value: value["global_credit"].__setitem__("typed_global_support_ledger", 0)),
        ("B1A", lambda value: value["strict_nonpromotion"].__setitem__("B1A", 1)),
        ("CM2", lambda value: value["strict_nonpromotion"].__setitem__("CM2", "GO")),
    ]
    rejected: list[str] = []
    for name, mutate in attacks:
        with tempfile.TemporaryDirectory(prefix="c25-attack-") as raw:
            target = Path(raw)
            for entry in candidate.iterdir():
                if entry.name != RESULT:
                    os.symlink(entry, target / entry.name)
            forged = copy.deepcopy(base)
            mutate(forged)
            (target / RESULT).write_bytes(canonical(close(forged)))
            run = subprocess.run([str(PYTHON), "-I", "-B", str(VERIFIER), "--candidate-dir", str(target)], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if run.returncode == 0:
                raise RuntimeError("accepted:" + name)
            rejected.append(name)
    print(canonical({"status": "PASS_8_OF_8_COHERENT_ATTACKS_REJECTED", "rejected": rejected}).decode())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
