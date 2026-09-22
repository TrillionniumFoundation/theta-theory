#!/usr/bin/env python3
from __future__ import annotations
import hashlib, json, os, re, sys
from pathlib import Path
import fitz

ROOT = Path(__file__).resolve().parent
pdf = ROOT / "geometry.pdf"
log = ROOT / "geometry.log"
if not pdf.exists() or pdf.stat().st_size == 0:
    raise SystemExit("geometry.pdf missing or empty")
if not log.exists():
    raise SystemExit("geometry.log missing")
text = log.read_text(errors="replace")

fatal_patterns = [
    r"LaTeX Warning: There were undefined references",
    r"LaTeX Warning: There were undefined citations",
    r"Citation .* undefined",
    r"Reference .* undefined",
    r"! LaTeX Error:",
    r"Emergency stop",
]
hits = [p for p in fatal_patterns if re.search(p, text)]
if hits:
    raise SystemExit("unresolved/fatal LaTeX diagnostics: " + "; ".join(hits))

doc = fitz.open(pdf)
pages = len(doc)
if pages < 10:
    raise SystemExit(f"unexpectedly short principal article: {pages} pages")
pdf_sha = hashlib.sha256(pdf.read_bytes()).hexdigest()

expected_logs = [
    ROOT / "evidence" / "exact_k3.log",
    ROOT / "evidence" / "exact_corank_two.log",
]
for p in expected_logs:
    if not p.exists() or p.stat().st_size == 0:
        raise SystemExit(f"missing exact-check log: {p.name}")

k3 = (ROOT / "evidence" / "K3_CERTIFICATES.json")
c2 = (ROOT / "evidence" / "CORANK2_CERTIFICATES.json")
if not k3.exists() or not c2.exists():
    raise SystemExit("certificate JSON missing")
kr = json.loads(k3.read_text())
cr = json.loads(c2.read_text())
if not kr.get("finite_witness_checks_passed"):
    raise SystemExit("K3 exact witness did not pass")
if kr.get("general_proof_machine_certified") is not False:
    raise SystemExit("K3 certificate must not claim general proof certification")
if not cr.get("primary_identity") or cr.get("general_proof_machine_certified") is not False:
    raise SystemExit("corank-two regression status invalid")

receipt = {
    "revision": 124,
    "principal_object": "geometry.pdf",
    "principal_pages": pages,
    "principal_pdf_sha256": pdf_sha,
    "source_commit": os.environ.get("SOURCE_COMMIT_SHA"),
    "branch": os.environ.get("GITHUB_REF_NAME"),
    "exact_k3_witness_passed": True,
    "exact_corank_two_regression_passed": True,
    "general_proof_machine_certified": False,
    "priority_certified": False,
    "ballico_1993_complete_text_read": False,
    "undefined_reference_diagnostics": [],
}
out = ROOT / "evidence" / "BUILD_RECEIPT.json"
out.write_text(json.dumps(receipt, indent=2) + "\n")
print(json.dumps(receipt, indent=2))
