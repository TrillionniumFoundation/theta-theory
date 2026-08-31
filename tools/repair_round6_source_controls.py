#!/usr/bin/env python3
"""Repair JSON-escape control bytes in authored round-six TeX sources.

A missed extra backslash in a connector JSON string can turn a TeX command
such as ``\\beta`` into ASCII backspace followed by ``eta``.  The mapping
below is lossless for those JSON escapes: the control byte identifies the
first command letter.  Tabs are never used as indentation in these sources,
so ASCII tab likewise denotes a lost ``\\t`` prefix.
"""
from __future__ import annotations

from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "revision" / "round6-referee-final"

REPLACEMENTS = {
    0x07: b"\\a",  # JSON \\a-like authoring error: alpha, angle, etc.
    0x08: b"\\b",  # beta, begin, bigsqcup, bounded...
    0x09: b"\\t",  # tau, theta, text, theorem...
    0x0B: b"\\v",  # varphi, varepsilon, vspace...
    0x0C: b"\\f",  # frac...
    0x0D: b"\\r",  # rho, right...
}
FORBIDDEN = re.compile(rb"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]")

changed = 0
repairs = 0
for path in sorted(SRC.glob("*.tex")):
    raw = path.read_bytes()
    out = bytearray()
    local = 0
    for byte in raw:
        replacement = REPLACEMENTS.get(byte)
        if replacement is None:
            out.append(byte)
        else:
            out.extend(replacement)
            local += 1
    repaired = bytes(out)
    if local:
        path.write_bytes(repaired)
        changed += 1
        repairs += local
        print(f"ROUND6_CONTROL_REPAIR {path.name} replacements={local}")
    match = FORBIDDEN.search(repaired)
    if match:
        raise SystemExit(
            f"{path}: unrepaired ASCII control byte {match.group()[0]} at {match.start()}"
        )
    if b"\t" in repaired:
        raise SystemExit(f"{path}: literal tab remains after repair")

print(f"ROUND6_CONTROL_REPAIR_PASS files_changed={changed} replacements={repairs}")
