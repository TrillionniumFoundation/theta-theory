#!/usr/bin/env python3
"""Make round-six materializer regex substitutions backslash-safe."""
from __future__ import annotations

from pathlib import Path

path = Path(__file__).with_name("apply_round6_referee_fixes.py")
text = path.read_text(encoding="utf-8")
start_marker = "    old = DATE_RE.sub("
end_marker = '    old = old.replace("round-three dependency ledger"'
start = text.index(start_marker)
end = text.index(end_marker, start)
replacement = r'''    old = DATE_RE.sub(
        lambda _match: r"\date{August 31, 2026}", old, count=1
    )
    abstract_text = (
        r"\begin{abstract}" + "\n"
        + meta["abstract"].strip()
        + "\n" + r"\end{abstract}"
    )
    old = ABSTRACT_RE.sub(lambda _match: abstract_text, old, count=1)
    marker_text = (
        r"\noindent\textbf{Controlling revision:} "
        r"\texttt{ROUND6-REFEREE-POSITIVE-CLOSURE}."
    )
    old = CONTROL_MARKER_RE.sub(lambda _match: marker_text, old, count=1)
    if INPUT_RE.search(old):
        old = INPUT_RE.sub(
            lambda _match: r"\input{ROUND6_POSITIVE_CLOSURE.tex}",
            old,
            count=1,
        )
    elif r"\input{ROUND6_POSITIVE_CLOSURE.tex}" not in old:
        raise SystemExit(f"{main}: controlling input not found")
'''
new = text[:start] + replacement + text[end:]
path.write_text(new, encoding="utf-8")
print("ROUND6_MATERIALIZER_REPAIR_PASS")
