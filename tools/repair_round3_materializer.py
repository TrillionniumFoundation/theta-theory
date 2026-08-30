#!/usr/bin/env python3
"""Repair deterministic round-three generator and one-shot driver defects.

This bootstrap repair is intentionally narrow.  It fixes the original raw
newline generator lines, the first A2 delimiter typo, and two over-escaped
idempotence markers in the hostile-fix driver.  The latter matters because
build diagnostics are committed with ``[skip ci]`` and a later proof edit must
be able to rerun the same hostile-fix pass safely.
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


def repair_a2_delimiter() -> int:
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
    # Do not use the mere presence of another \right as the success test.
    if old in text:
        raise SystemExit("A2 delimiter repair did not converge")
    path.write_text(text, encoding="utf-8")
    return changed


def repair_harsh_driver_markers() -> int:
    path = ROOT / "tools" / "apply_round3_harsh_fixes.py"
    if not path.is_file():
        return 0
    lines = path.read_text(encoding="utf-8").splitlines()
    changed = 0
    for index, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith('if "homogeneity cutoff ') and stripped.endswith('not in text:'):
            desired = '    if "homogeneity cutoff" not in text:'
            if line != desired:
                lines[index] = desired
                changed += 1
        elif 'return replace_once(path, old, new, "remaining ' in stripped:
            desired = (
                '    return replace_once(path, old, new, '
                '"remaining cycle occurrences are not claimed")'
            )
            if line != desired:
                lines[index] = desired
                changed += 1
    text = "\n".join(lines) + "\n"
    if 'if "homogeneity cutoff" not in text:' not in text:
        raise SystemExit("A3 hostile-fix idempotence marker was not normalized")
    if '"remaining cycle occurrences are not claimed")' not in text:
        raise SystemExit("B2 hostile-fix idempotence marker was not normalized")
    path.write_text(text, encoding="utf-8")
    return changed


materializer_changes = repair_materializer()
a2_changes = repair_a2_delimiter()
driver_changes = repair_harsh_driver_markers()
print(
    "ROUND3_BOOTSTRAP_REPAIR_PASS "
    f"materializer={materializer_changes} a2={a2_changes} driver={driver_changes}"
)
