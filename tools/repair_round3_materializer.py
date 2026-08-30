#!/usr/bin/env python3
"""Repair the two newline-producing source lines in the round-three materializer.

The original generator used raw strings ending in ``\n``.  That preserved the
characters backslash+n in the generated TeX instead of emitting a newline.
This repair is intentionally narrow and idempotent; it patches only the two
known source lines and then verifies the corrected form.
"""
from pathlib import Path

path = Path(__file__).with_name("apply_round3_closure.py")
lines = path.read_text(encoding="utf-8").splitlines()
changed = 0
for index, line in enumerate(lines):
    stripped = line.strip()
    if stripped == '+ r"\\texttt{" + meta["platform"] + "}.\\n"':
        lines[index] = '        + "\\\\texttt{" + meta["platform"] + "}.\\n"'
        changed += 1
    elif stripped == '+ r"\\texttt{ROUND3-POSITIVE-CLOSURE}.\\n"':
        lines[index] = '        + "\\\\texttt{ROUND3-POSITIVE-CLOSURE}.\\n"'
        changed += 1

text = "\n".join(lines) + "\n"
required = (
    '+ "\\\\texttt{" + meta["platform"] + "}.\\n"',
    '+ "\\\\texttt{ROUND3-POSITIVE-CLOSURE}.\\n"',
)
if not all(item in text for item in required):
    raise SystemExit("round-three materializer escape repair did not converge")
if 'r"\\texttt{" + meta["platform"] + "}.\\n"' in text:
    raise SystemExit("raw platform newline remains")
if 'r"\\texttt{ROUND3-POSITIVE-CLOSURE}.\\n"' in text:
    raise SystemExit("raw revision newline remains")

path.write_text(text, encoding="utf-8")
print(f"ROUND3_MATERIALIZER_ESCAPE_REPAIR_PASS changed={changed}")
