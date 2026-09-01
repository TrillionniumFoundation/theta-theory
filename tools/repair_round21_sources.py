#!/usr/bin/env python3
"""Repair the audited JSON-escape corruptions in the Round-21 payload.

The large TeX payload was sent through a JSON string. Four command families
were found at exact, logged offsets where a single TeX backslash had been
interpreted as a JSON control escape: A2 ``\\frac12`` (form feed), C1
``\\vartheta`` (vertical tab), and D1 ``\\rho`` (carriage return) and
``\\varepsilon`` (vertical tab). Only these exact byte patterns are repaired.
The script then rejects every remaining C0 control byte other than line feed
and every standalone truncated fraction token. It is idempotent after the
repaired sources are committed by the workflow.
"""
from __future__ import annotations

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
ACTIVE = sorted((ROOT / "papers").glob("*/ROUND17_POSITIVE_CLOSURE.tex"))
REPAIRS = {
    ROOT / "papers/A2-sinai-homological-pressure/ROUND17_POSITIVE_CLOSURE.tex": [
        (b"\x0crac12", b"\\frac12", "A2 JSON form-feed corruption: \\frac12"),
    ],
    ROOT / "papers/C1-information-risk-sensitive-saddles/ROUND17_POSITIVE_CLOSURE.tex": [
        (b"\x0bartheta", b"\\vartheta", "C1 JSON vertical-tab corruption: \\vartheta"),
    ],
    ROOT / "papers/D1-deterministic-theta-contractions/ROUND17_POSITIVE_CLOSURE.tex": [
        (b"\x0dho", b"\\rho", "D1 JSON carriage-return corruption: \\rho"),
        (b"\x0barepsilon", b"\\varepsilon", "D1 JSON vertical-tab corruption: \\varepsilon"),
    ],
}


def fail(message: str) -> None:
    print(f"ROUND21_SOURCE_REPAIR_FAIL: {message}", file=sys.stderr)
    raise SystemExit(1)


def main() -> None:
    total_repairs = 0
    for path, replacements in REPAIRS.items():
        raw = path.read_bytes()
        changed = False
        for broken, repaired, label in replacements:
            count = raw.count(broken)
            if count:
                raw = raw.replace(broken, repaired)
                changed = True
                total_repairs += count
                print(f"repaired {count} occurrence(s): {label}")
            elif repaired not in raw:
                fail(
                    f"neither broken nor repaired token found for {label} in "
                    f"{path.relative_to(ROOT)}"
                )
            else:
                print(f"repair already present: {label}")
        if changed:
            path.write_bytes(raw)

    diagnostics: list[str] = []
    for path in ACTIVE:
        data = path.read_bytes()
        for offset, value in enumerate(data):
            if value < 0x20 and value != 0x0A:
                lo = max(0, offset - 24)
                hi = min(len(data), offset + 40)
                context = repr(data[lo:hi])
                diagnostics.append(
                    f"{path.relative_to(ROOT)} offset={offset} "
                    f"control=0x{value:02x} context={context}"
                )
        residue = data.replace(b"\\frac12", b"")
        if b"rac12" in residue:
            diagnostics.append(
                f"{path.relative_to(ROOT)} contains standalone truncated rac12"
            )
    if diagnostics:
        for item in diagnostics:
            print(f"ROUND21_SOURCE_REPAIR_DIAGNOSTIC: {item}", file=sys.stderr)
        fail(f"{len(diagnostics)} unapproved source transport corruptions remain")

    print(
        f"ROUND21_SOURCE_REPAIR_PASS active_modules={len(ACTIVE)} "
        f"repairs_applied={total_repairs}"
    )


if __name__ == "__main__":
    main()
