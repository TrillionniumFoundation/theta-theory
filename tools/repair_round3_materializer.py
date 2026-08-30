#!/usr/bin/env python3
"""Repair deterministic round-three source-generation and TeX typos.

The first bootstrap used raw strings ending in ``\n`` and therefore emitted
literal backslash+n characters in generated manuscripts.  The A2 module also
contained one transposition, ``\night)`` instead of ``\right)``.  This script
is deliberately narrow, idempotent, and fail-closed: it changes only the known
source forms and verifies that the corrected forms are present afterwards.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def repair_materializer() -> int:
    path = ROOT / "tools" / "apply_round3_closure.py"
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
    forbidden = (
        'r"\\texttt{" + meta["platform"] + "}.\\n"',
        'r"\\texttt{ROUND3-POSITIVE-CLOSURE}.\\n"',
    )
    if any(item in text for item in forbidden):
        raise SystemExit("raw materializer newline remains")
    path.write_text(text, encoding="utf-8")
    return changed


def repair_tex_sources() -> int:
    path = ROOT / "papers" / "A2-sinai-homological-pressure" / "ROUND3_POSITIVE_CLOSURE.tex"
    text = path.read_text(encoding="utf-8")
    slash = chr(92)
    old = slash + "night)"
    new = slash + "right)"
    occurrences = text.count(old)
    if occurrences > 1:
        raise SystemExit(f"ambiguous A2 delimiter repair: {old!r} occurs {occurrences} times")
    changed = 0
    if occurrences == 1:
        text = text.replace(old, new, 1)
        changed = 1
    if old in text or new not in text:
        raise SystemExit("A2 delimiter repair did not converge")
    path.write_text(text, encoding="utf-8")
    return changed


materializer_changes = repair_materializer()
tex_changes = repair_tex_sources()
print(
    "ROUND3_SOURCE_REPAIR_PASS "
    f"materializer_changes={materializer_changes} tex_changes={tex_changes}"
)
