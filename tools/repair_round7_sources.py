#!/usr/bin/env python3
"""Apply deterministic, idempotent repairs found by the pre-materialization audit."""
from __future__ import annotations

from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "revision" / "round7-referee-final"

changed = 0

# JSON/string transport can interpret a single TeX prefix such as ``\v`` as
# an ASCII control byte.  Restore the corresponding TeX command prefix in
# every registered source.  A second transport pathology turns a TeX command
# beginning with ``n`` (for example ``\nu``, ``\nabla``, or ``\neq``) into a
# single backslash, a physical newline, and the remaining command letters.
# The negative lookbehind deliberately excludes a legal TeX ``\\`` row break.
CONTROL_PREFIX = {
    0x07: r"\a",
    0x08: r"\b",
    0x09: r"\t",
    0x0B: r"\v",
    0x0C: r"\f",
    0x0D: r"\r",
}
BROKEN_N_PREFIX = re.compile(r"(?<!\\)\\\n([A-Za-z]+)")

for source in sorted(SRC.glob("*.tex")):
    text = source.read_text(encoding="utf-8")
    repaired_parts: list[str] = []
    control_replacements = 0
    for char in text:
        code = ord(char)
        if code in CONTROL_PREFIX:
            repaired_parts.append(CONTROL_PREFIX[code])
            control_replacements += 1
        else:
            repaired_parts.append(char)
    repaired = "".join(repaired_parts)

    recovered_commands: list[str] = []

    def restore_n_prefix(match: re.Match[str]) -> str:
        command = "\\n" + match.group(1)
        recovered_commands.append(command)
        return command

    repaired, n_prefix_replacements = BROKEN_N_PREFIX.subn(
        restore_n_prefix, repaired
    )

    leftovers = [
        (index, ord(char))
        for index, char in enumerate(repaired)
        if ord(char) < 32 and char != "\n"
    ]
    if leftovers:
        raise SystemExit(f"{source}: unrepaired ASCII controls {leftovers[:8]}")
    broken_n_leftovers = [
        (match.start(), match.group(0))
        for match in BROKEN_N_PREFIX.finditer(repaired)
    ]
    if broken_n_leftovers:
        raise SystemExit(
            f"{source}: unrepaired TeX n-prefix breaks {broken_n_leftovers[:8]}"
        )

    if repaired != text:
        source.write_text(repaired, encoding="utf-8")
        changed += 1
        print(
            f"ROUND7_TEX_TRANSPORT_REPAIR {source.name} "
            f"control_replacements={control_replacements} "
            f"n_prefix_replacements={n_prefix_replacements} "
            f"commands={','.join(recovered_commands[:20])}"
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

# A JSON ``\r`` escape in the A4 source was normalized to a physical line
# break before Python could see the carriage-return byte, leaving ``ight]``.
# Restore the exact closing delimiter and fail if neither audited form occurs.
a4 = SRC / "A4_COARSE_HISTORY_RIESZ_SCHUR.tex"
text = a4.read_text(encoding="utf-8")
a4_old = " h_\\Psi(Y_1)\night]."
a4_new = " h_\\Psi(Y_1)\n \\right]."
if a4_old in text:
    text = text.replace(a4_old, a4_new, 1)
    a4.write_text(text, encoding="utf-8")
    changed += 1
elif a4_new not in text:
    raise SystemExit("A4 history eigenfunction closing delimiter not found")

# ``D_\tan`` makes TeX parse the trigonometric operator as a naked subscript.
# The intended symbol is the textual tangential derivative label.
b2 = SRC / "B2_FRAME_RESET_MEASURE_TRACE_LDP.tex"
text = b2.read_text(encoding="utf-8")
b2_old = r"D_\tan\gamma_{k,\rm ac}^-"
b2_new = r"D_{\mathrm{tan}}\gamma_{k,\mathrm{ac}}^-"
if b2_old in text:
    text = text.replace(b2_old, b2_new, 1)
    b2.write_text(text, encoding="utf-8")
    changed += 1
elif b2_new not in text:
    raise SystemExit("B2 tangential trace notation not found")

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
