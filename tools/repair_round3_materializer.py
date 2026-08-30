#!/usr/bin/env python3
"""Repair deterministic round-three generator and one-shot driver defects.

This bootstrap repair is intentionally narrow.  It fixes the original raw
newline generator lines, the first A2 delimiter typo, and early quoting or
idempotence defects in the hostile-fix driver.  The driver is compiled before
this script returns, so a malformed proof-patch program cannot reach the
manuscript build stage.
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
    if old in text:
        raise SystemExit("A2 delimiter repair did not converge")
    path.write_text(text, encoding="utf-8")
    return changed


def repair_harsh_driver() -> int:
    path = ROOT / "tools" / "apply_round3_harsh_fixes.py"
    if not path.is_file():
        return 0
    lines = path.read_text(encoding="utf-8").splitlines()
    changed = 0
    slash = chr(92)
    index = 0
    while index < len(lines):
        line = lines[index]
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
        elif stripped == 'proof_marker = r"The mark statements are the exponential-tilt argument used in':
            if index + 1 >= len(lines):
                raise SystemExit("truncated A3 proof_marker in hostile-fix driver")
            next_stripped = lines[index + 1].strip()
            expected_next = "Theorem~" + slash + 'ref{thm:r3-a3-block}."'
            if next_stripped != expected_next:
                raise SystemExit(
                    "unexpected A3 proof_marker continuation: " + repr(next_stripped)
                )
            lines[index] = (
                '        proof_marker = r"""The mark statements are the '
                'exponential-tilt argument used in'
            )
            lines[index + 1] = (
                "Theorem~" + slash + 'ref{thm:r3-a3-block}."""'
            )
            changed += 1
            index += 1
        index += 1

    text = "\n".join(lines) + "\n"
    if 'if "homogeneity cutoff" not in text:' not in text:
        raise SystemExit("A3 hostile-fix idempotence marker was not normalized")
    if '"remaining cycle occurrences are not claimed")' not in text:
        raise SystemExit("B2 hostile-fix idempotence marker was not normalized")
    if 'proof_marker = r"""The mark statements' not in text:
        raise SystemExit("A3 hostile-fix multiline proof marker was not repaired")
    compile(text, str(path), "exec")
    path.write_text(text, encoding="utf-8")
    return changed


materializer_changes = repair_materializer()
a2_changes = repair_a2_delimiter()
driver_changes = repair_harsh_driver()
print(
    "ROUND3_BOOTSTRAP_REPAIR_PASS "
    f"materializer={materializer_changes} a2={a2_changes} driver={driver_changes}"
)
