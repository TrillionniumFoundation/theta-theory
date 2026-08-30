#!/usr/bin/env python3
"""Restore LaTeX command bytes accidentally decoded as ASCII escapes.

The round-four proof fragments are generated as text artifacts.  A malformed
JSON/string escape can turn a leading LaTeX command byte such as ``\v`` or
``\r`` into vertical-tab or carriage-return.  No round-four TeX fragment is
allowed to contain tabs, carriage returns, or other C0 controls, so the map is
unambiguous and fail-closed.
"""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FRAG = ROOT / "revision" / "round4-referee"

RESTORE = {
    7: b"\\a",   # bell     <- \a...
    8: b"\\b",   # backspace<- \b...
    9: b"\\t",   # tab      <- \t...
    11: b"\\v",  # vtab     <- \v...
    12: b"\\f",  # formfeed <- \f...
    13: b"\\r",  # carriage <- \r...
}


def main() -> None:
    changed = 0
    replacements = 0
    paths = sorted(FRAG.glob("*.tex"))
    if len(paths) != 11:
        raise SystemExit(f"expected 11 round-four fragments, found {len(paths)}")
    for path in paths:
        data = path.read_bytes()
        original = data
        for byte, replacement in RESTORE.items():
            count = data.count(bytes([byte]))
            if count:
                data = data.replace(bytes([byte]), replacement)
                replacements += count
        remaining = sorted({b for b in data if b < 32 and b != 10})
        if remaining:
            raise SystemExit(f"{path}: unrepaired ASCII control bytes {remaining}")
        if data != original:
            path.write_bytes(data)
            changed += 1
    print(
        "ROUND4_FRAGMENT_SANITATION_PASS "
        f"files={len(paths)} changed={changed} replacements={replacements}"
    )


if __name__ == "__main__":
    main()
