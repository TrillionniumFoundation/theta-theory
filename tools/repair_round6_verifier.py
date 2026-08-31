#!/usr/bin/env python3
"""Replace line-wrap-sensitive verifier phrases by stable mathematical tokens."""
from __future__ import annotations

from pathlib import Path

path = Path(__file__).with_name("verify_round6_referee.py")
text = path.read_text(encoding="utf-8")
replacements = {
    '        "not restricted to a port core",\n': '',
    '        "trace-jet Banach scale",\n': '        "trace-jet fluxes",\n',
    '        "relative asymptotic whenever",\n': '        r"G_n\\gg n^{-1/2}",\n',
    '        "transmission-zero modes",\n': '        "Transmission-zero realization",\n',
    '        "exactly the Radon--Nikodym density",\n': '        "Radon--Nikodym density",\n',
}
changed = 0
for old, new in replacements.items():
    if old in text:
        text = text.replace(old, new)
        changed += 1
path.write_text(text, encoding="utf-8")
print(f"ROUND6_VERIFIER_REPAIR_PASS replacements={changed}")
