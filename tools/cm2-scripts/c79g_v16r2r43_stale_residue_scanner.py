#!/usr/bin/env python3
"""Read-only r43 successor of the independent stale-residue scanner.

The reviewed r42 scanner is loaded as source/AST in memory (never through a
bytecode-producing import) and executed with the r43/r42 namespace selectors.
This wrapper emits the scanner's single stdout JSON report and performs no
workspace writes.
"""
from __future__ import annotations

import ast
import hashlib
import os
from pathlib import Path
import sys

sys.dont_write_bytecode = True
os.environ.update({"PYTHONDONTWRITEBYTECODE": "1", "PYTHONNOUSERSITE": "1",
                   "CM2_STALE_SCAN_TAG": "v16r2r43",
                   "CM2_STALE_SCAN_PREV": "v16r2r42"})

ROOT = Path(__file__).resolve().parents[1]
BASE_SCANNER = ROOT / "scripts/c79g_v16r2r42_stale_residue_scanner.py"
BASE_SCANNER_SHA256 = "e5fdf024066984cbe74c8b988446b4c43204cb6a1cea7a9f67c511ee0bf9545b"


def main() -> int:
    raw = BASE_SCANNER.read_bytes()
    if hashlib.sha256(raw).hexdigest() != BASE_SCANNER_SHA256:
        raise RuntimeError("r42 scanner template hash drift")
    tree = ast.parse(raw.decode("utf-8"), filename=str(BASE_SCANNER), mode="exec")
    code = compile(tree, str(BASE_SCANNER), "exec")
    ns: dict[str, object] = {"__name__": "_r43_stale_scanner",
                             "__file__": str(BASE_SCANNER),
                             "__package__": None}
    exec(code, ns, ns)
    runner = ns.get("main")
    if not callable(runner):
        raise RuntimeError("r42 scanner main missing")
    return int(runner())


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"R43_STALE_SCANNER_FAIL_CLOSED: {type(exc).__name__}: {exc}",
              file=sys.stderr)
        raise SystemExit(2)
