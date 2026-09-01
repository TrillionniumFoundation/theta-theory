#!/usr/bin/env python3
"""Repair the one audited JSON-escape corruption in the Round-21 payload.

The A2 Gaussian coefficient was transmitted with JSON's form-feed escape in
place of the TeX command ``\\frac``.  This script performs exactly that one
byte-level repair and then fails on every remaining C0 control character or
standalone truncated ``rac12`` token.  It is idempotent after the repaired
source is committed by the verification workflow.
"""
from __future__ import annotations

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
A2 = ROOT / "papers/A2-sinai-homological-pressure/ROUND17_POSITIVE_CLOSURE.tex"
ACTIVE = sorted((ROOT / "papers").glob("*/ROUND17_POSITIVE_CLOSURE.tex"))


def fail(message: str) -> None:
    print(f"ROUND21_SOURCE_REPAIR_FAIL: {message}", file=sys.stderr)
    raise SystemExit(1)


def main() -> None:
    raw = A2.read_bytes()
    broken = b"\x0crac12"
    repaired = b"\\frac12"
    count = raw.count(broken)
    if count > 1:
        fail(f"A2 contains {count} copies of the audited corruption")
    if count == 1:
        raw = raw.replace(broken, repaired, 1)
        A2.write_bytes(raw)
        print("repaired A2 JSON form-feed corruption: \\frac12")
    else:
        print("A2 audited transport repair already present")

    for path in ACTIVE:
        data = path.read_bytes()
        for value in list(range(0x00, 0x09)) + [0x0B, 0x0C, 0x0E, 0x0F]:
            if bytes([value]) in data:
                fail(
                    f"unexpected control byte 0x{value:02x} in "
                    f"{path.relative_to(ROOT)}"
                )
        # A valid TeX token ``\\frac12`` naturally contains the suffix
        # ``rac12``.  Remove valid occurrences before looking for the audited
        # standalone truncation.
        residue = data.replace(b"\\frac12", b"")
        if b"rac12" in residue:
            fail(f"truncated TeX fraction remains in {path.relative_to(ROOT)}")
    print("ROUND21_SOURCE_REPAIR_PASS active_modules=11")


if __name__ == "__main__":
    main()
