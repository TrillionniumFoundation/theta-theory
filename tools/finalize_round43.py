#!/usr/bin/env python3
"""One-use deterministic finalizer for the immutable Round 43 reviewer object."""
from __future__ import annotations

import base64
import gzip
import hashlib
import py_compile
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAYLOAD_SHA256 = "5e5ed75a74776c957674a48d28151fa2322131a1487b8dfeccbfc11a14caf72f"
PREPATCH_SHA256 = "27041361d57cb4c0112e49ddb55c18859d8ea0920fe8548808c4cbe68918aa3d"


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def replace_exactly_once(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f"{label}: expected one anchor, found {count}")
    return text.replace(old, new, 1)


def run(*parts: str) -> None:
    subprocess.run(parts, cwd=ROOT, check=True)


# Freeze the already-reviewed Round 41 source constructors before executing them.
generator = ROOT / "tools/materialize_round41.py"
text = generator.read_text(encoding="utf-8")
old = 'r"""The true transient cross term is at most\n'
new = 'r"""The\ntrue transient cross term is at most\n'
if old in text:
    text = replace_exactly_once(text, old, new, "Round 41 paragraph break")
elif new not in text:
    raise RuntimeError("Round 41 paragraph-break anchor not found")
generator.write_text(text, encoding="utf-8")

hardener = ROOT / "tools/harden_round41_ldp.py"
text = hardener.read_text(encoding="utf-8")
bs = chr(92)
bad_denominator = chr(12) + "rac1n" + bs + "log"
good_denominator = bs + "frac1n" + bs + "log"
text = replace_exactly_once(
    text,
    bad_denominator,
    good_denominator,
    "Round 41 LDP denominator control character",
)
hardener.write_text(text, encoding="utf-8")

# Recover the reviewed Round 43 constructor from its hash-locked staging payload.
parts = sorted((ROOT / ".round43_payload").glob("part*.b64"))
if len(parts) != 5:
    raise RuntimeError(f"expected five payload parts, found {len(parts)}")
payload_text = "".join(path.read_text(encoding="ascii") for path in parts)
payload_bytes = payload_text.encode("ascii")
if sha256_bytes(payload_bytes) != PAYLOAD_SHA256:
    raise RuntimeError("concatenated Round 43 payload hash mismatch")
compressed = base64.b64decode(payload_bytes, validate=True)
materializer_bytes = gzip.decompress(compressed)
if sha256_bytes(materializer_bytes) != PREPATCH_SHA256:
    raise RuntimeError("decoded Round 43 materializer hash mismatch")

materializer = ROOT / "tools/materialize_round43.py"
materializer.write_bytes(materializer_bytes)
text = materializer.read_text(encoding="utf-8")
replacements = [
    (
        'self.assertIn(r"M_R=2e^{' + bs * 2 + 'Lambda_AT}' + bs * 2 + 'Lambda_A^R", quantitative)',
        'self.assertIn(r"M_R=2e^{' + bs + 'Lambda_AT}' + bs + 'Lambda_A^R", quantitative)',
    ),
    (
        'self.assertIn(r"C_R' + bs * 2 + 'le 2^{R+1}(R+1)!", quantitative)',
        'self.assertIn(r"C_R' + bs + 'le 2^{R+1}(R+1)!", quantitative)',
    ),
    (
        'self.assertIn(r"K_J' + bs * 2 + 'delta^{2R_J+3}", quantitative)',
        'self.assertIn(r"K_J' + bs + 'delta^{2R_J+3}", quantitative)',
    ),
]
for old, new in replacements:
    text = replace_exactly_once(text, old, new, "Round 43 TeX certificate literal")
materializer.write_text(text, encoding="utf-8")
materializer.chmod(0o755)

for path in (generator, hardener, materializer):
    py_compile.compile(str(path), doraise=True)

run(sys.executable, "tools/materialize_round41.py")
run(sys.executable, "tools/harden_round41_ldp.py")
run(sys.executable, "tools/materialize_round43.py")

# Strengthen the test from the actual generated Python source, then mirror the
# exact source lines into the materializer template so regeneration is stable.
test_path = ROOT / "tests/test_round43.py"
test_text = test_path.read_text(encoding="utf-8")
literal_pattern = re.compile(
    r'''(?P<prefix>[rRuUbBfF]{0,2})(?P<quote>["'])rac1n(?P=quote)'''
)
literal_matches = list(literal_pattern.finditer(test_text))
if len(literal_matches) != 1:
    raise RuntimeError(
        f"generated Round 43 malformed-token literal: expected one, found {len(literal_matches)}"
    )
old_literal = literal_matches[0].group(0)
test_text = test_text[: literal_matches[0].start()] + "chr(12)" + test_text[literal_matches[0].end() :]

assertion_pattern = re.compile(
    r'''(?m)^(?P<indent>\s*)self\.assertNotIn\(token,\s*(?P<subject>[A-Za-z_][A-Za-z0-9_]*)\)\s*$'''
)
assertion_matches = list(assertion_pattern.finditer(test_text))
if len(assertion_matches) != 1:
    raise RuntimeError(
        f"generated Round 43 token-loop assertion: expected one, found {len(assertion_matches)}"
    )
match = assertion_matches[0]
old_assertion_line = match.group(0)
indent = match.group("indent")
subject = match.group("subject")
new_assertion_lines = (
    f"{indent}self.assertNotIn(token, {subject})\n"
    f'{indent}self.assertIn(r"{bs}frac1n{bs}log", {subject})'
)
test_text = test_text[: match.start()] + new_assertion_lines + test_text[match.end() :]
test_path.write_text(test_text, encoding="utf-8")

materializer_text = materializer.read_text(encoding="utf-8")
materializer_text = replace_exactly_once(
    materializer_text,
    old_literal,
    "chr(12)",
    "materializer malformed-token literal",
)
materializer_text = replace_exactly_once(
    materializer_text,
    old_assertion_line,
    new_assertion_lines,
    "materializer token-loop assertion",
)
materializer.write_text(materializer_text, encoding="utf-8")
postpatch_sha = sha256_bytes(materializer.read_bytes())
py_compile.compile(str(materializer), doraise=True)
py_compile.compile(str(test_path), doraise=True)

# Make the source-control-character repair an explicit invariant of the frozen object.
for relative in ("round41/infinite_jacobi.tex", "round43/infinite_jacobi.tex"):
    rendered = (ROOT / relative).read_text(encoding="utf-8")
    if chr(12) in rendered:
        raise RuntimeError(f"form-feed survived in {relative}")
    if good_denominator not in rendered:
        raise RuntimeError(f"correct LDP denominator missing from {relative}")

provenance = ROOT / "round43/MATERIALIZATION_PROVENANCE.sha256"
provenance.write_text(
    f"{PAYLOAD_SHA256}  .round43_payload/concatenated-base64\n"
    f"{PREPATCH_SHA256}  tools/materialize_round43.py.prepatch\n"
    f"{postpatch_sha}  tools/materialize_round43.py\n",
    encoding="utf-8",
)
print(
    {
        "materialized": True,
        "round": 43,
        "materializer_sha256": postpatch_sha,
        "control_character_repair": "verified",
        "generated_test_repair": "mirrored-to-materializer",
    }
)
