#!/usr/bin/env python3
"""Apply deterministic, idempotent repairs found by the pre-materialization audit."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "revision" / "round7-referee-final"

changed = 0

# JSON/string transport can interpret a single TeX prefix such as ``\v`` as
# an ASCII control byte.  Restore the corresponding TeX command prefix in
# every registered source, and then fail if any non-newline control remains.
CONTROL_PREFIX = {
    0x07: r"\a",
    0x08: r"\b",
    0x09: r"\t",
    0x0B: r"\v",
    0x0C: r"\f",
    0x0D: r"\r",
}
for source in sorted(SRC.glob("*.tex")):
    text = source.read_text(encoding="utf-8")
    repaired_parts: list[str] = []
    replacements = 0
    for char in text:
        code = ord(char)
        if code in CONTROL_PREFIX:
            repaired_parts.append(CONTROL_PREFIX[code])
            replacements += 1
        else:
            repaired_parts.append(char)
    repaired = "".join(repaired_parts)
    leftovers = [
        (index, ord(char))
        for index, char in enumerate(repaired)
        if ord(char) < 32 and char != "\n"
    ]
    if leftovers:
        raise SystemExit(f"{source}: unrepaired ASCII controls {leftovers[:8]}")
    if repaired != text:
        source.write_text(repaired, encoding="utf-8")
        changed += 1
        print(
            f"ROUND7_TEX_CONTROL_REPAIR {source.name} "
            f"replacements={replacements}"
        )

# Correct a harmless but ambiguous typography in A1.
a1 = SRC / "A1_BISEAM_ANISOTROPIC_AUTONOMOUS.tex"
text = a1.read_text(encoding="utf-8")
new = text.replace(
    r"\|\mathcal L_a^nu\|_{m,+}",
    r"\|\mathcal L_a^n u\|_{m,+}",
)
if new != text:
    a1.write_text(new, encoding="utf-8")
    changed += 1

# The backward observable propagator V(t,s), t <= s, is constructed by
# forward evolution in the remaining-time variable.  This is not a
# negative-time BBGKY group.  Its terminal-value formula has positive sign.
b4 = SRC / "B4_FORWARD_POISSON_TATARU_SEMIGROUP.tex"
text = b4.read_text(encoding="utf-8")
old = r"""Let $A(t)$ be the limiting triangular hierarchy generator along a smooth test
path and $U(t,s)$ its forward evolution for $t\ge s$.  Suppose the uncancelled
order-$j$ defect is $D_j(t)$.  Define
\[
 c_j(t)=-\int_t^T U(s,t)D_j(s)\,ds,
 \qquad c_j(T)=0.
\]
Then
\[
 \partial_t c_j(t)+A(t)c_j(t)=-D_j(t).
\]
The terminal boundary term is part of the perturbed test and is exactly zero.
"""
replacement = r"""Let $A(t)$ be the limiting triangular hierarchy generator on observables.
For $t\le s$, let $V(t,s)$ be the backward observable propagator satisfying
\[
 \partial_tV(t,s)=-A(t)V(t,s),
 \qquad V(s,s)=I.
\]
It is constructed by a forward Picard iteration in the remaining-time variable
$r=s-t$ and does not require a negative-time hierarchy evolution.  If the
uncancelled order-$j$ defect is $D_j(t)$, define
\[
 c_j(t)=\int_t^T V(t,s)D_j(s)\,ds,
 \qquad c_j(T)=0.
\]
Then
\[
 \partial_t c_j(t)+A(t)c_j(t)=-D_j(t).
\]
The terminal boundary term is exactly zero.
"""
if old in text:
    text = text.replace(old, replacement)
    changed += 1
elif replacement not in text:
    raise SystemExit("B4 corrector declaration did not match either audited form")

old_proof = r"""Differentiate the Duhamel integral.  Since
$\partial_tU(s,t)=-U(s,t)A(t)$, the identity
$\partial_tc_j+A(t)c_j=-D_j$ follows with no remainder.  The B2 forward
semigroup estimate gives
\[
 \|c_j(t)\|_{\rm gr}
 \le\int_t^Te^{C(s-t)}\|D_j(s)\|_{\rm gr}ds.
\]
"""
new_proof = r"""Differentiate the Duhamel integral.  The lower endpoint gives
$-D_j(t)$ and $\partial_tV(t,s)=-A(t)V(t,s)$ gives
\[
 \partial_tc_j(t)=-D_j(t)-A(t)c_j(t).
\]
Thus the defect is cancelled with no terminal remainder.  The forward
remaining-time construction gives
\[
 \|c_j(t)\|_{\rm gr}
 \le\int_t^Te^{C(s-t)}\|D_j(s)\|_{\rm gr}ds.
\]
"""
if old_proof in text:
    text = text.replace(old_proof, new_proof)
    changed += 1
elif new_proof not in text:
    raise SystemExit("B4 corrector proof did not match either audited form")

b4.write_text(text, encoding="utf-8")

print(f"ROUND7_SOURCE_REPAIR_PASS changed_files_or_blocks={changed}")
