#!/usr/bin/env python3
"""Fail-closed structural verifier for Round Seventeen."""
from __future__ import annotations

from pathlib import Path
import hashlib
import json
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
manifest_path = ROOT / "ROUND17_MATERIALIZATION_MANIFEST.json"
inventory_path = ROOT / "ROUND17_REFEREE_INVENTORY.json"
if not manifest_path.is_file() or not inventory_path.is_file():
    raise SystemExit("Round-Seventeen manifest or inventory missing")
manifest = json.loads(manifest_path.read_text())
inventory = json.loads(inventory_path.read_text())

EXPECTED = {
    "A1-exact-benchmarks", "A2-sinai-homological-pressure",
    "A3-full-empirical-path-ldp", "A4-history-memory-universal-pressure",
    "B1-microcanonical-preparation", "B2-collision-clusters-dynamic-ldp",
    "B3-hamilton-boltzmann-cotangents", "B4-nonlinear-kinetic-semigroups",
    "C1-information-risk-sensitive-saddles",
    "C2-cotangent-rigidity-tangent-representations",
    "D1-deterministic-theta-contractions",
}
errors: list[str] = []
if manifest.get("paper_count") != 11 or inventory.get("paper_count") != 11:
    errors.append("paper count is not 11")
if manifest.get("referee_objections") != 63 or inventory.get("major_objection_count") != 63:
    errors.append("major objection count is not 63")

THM = re.compile(r"\\begin\{(?:theorem|lemma|proposition|corollary)\}")
PROOF = re.compile(r"\\begin\{proof\}")
LABEL = re.compile(r"\\label\{([^}]+)\}")
REF = re.compile(r"\\(?:ref|cref)\{([^}]+)\}")
BANNED = [
    "TODO", "FIXME", "NO_THEOREM_CREDIT", "reviewer must verify",
    "assume the main gate", "remove as a standalone", "no-go replacement",
]

report: dict[str, object] = {
    "schema": "theta-theory-round17-structural-verification-v1",
    "papers": {}, "errors": errors,
}

actual_dirs = {p.name for p in (ROOT / "papers").iterdir() if p.is_dir()}
if actual_dirs != EXPECTED:
    errors.append(f"paper directory mismatch: {sorted(actual_dirs ^ EXPECTED)}")

all_labels: dict[str, str] = {}
total_thm = total_proof = total_objections = 0
for entry in manifest["papers"]:
    folder = ROOT / entry["folder"]
    code = entry["code"]
    source = ROOT / entry["registered_source"]
    active = folder / "ROUND17_POSITIVE_CLOSURE.tex"
    main = folder / "main.tex"
    response = folder / "AUTHOR_RESPONSE_ROUND17.md"
    referee = folder / "REFEREE_REPORT_ROUND16_GPT56_PRO.md"
    for path in (source, active, main, response, referee):
        if not path.is_file():
            errors.append(f"{code}: missing {path.relative_to(ROOT)}")
    if not all(x.is_file() for x in (source, active, main, response, referee)):
        continue

    source_bytes = source.read_bytes()
    active_bytes = active.read_bytes()
    byte_identity = source_bytes == active_bytes
    if not byte_identity:
        errors.append(f"{code}: source/active module byte mismatch")
    if hashlib.sha256(source_bytes).hexdigest() != entry["source_sha256"]:
        errors.append(f"{code}: manifest source hash mismatch")

    text = active_bytes.decode("utf-8")
    main_text = main.read_text()
    response_text = response.read_text()
    referee_text = referee.read_text()
    if any(ord(c) < 32 and c not in "\n\t" for c in text):
        errors.append(f"{code}: ASCII control byte in active module")
    if main_text.count(r"\input{ROUND17_POSITIVE_CLOSURE.tex}") != 1:
        errors.append(f"{code}: main must input Round17 exactly once")
    if "ROUND17-REFEREE-POSITIVE-CLOSURE" not in main_text:
        errors.append(f"{code}: controlling marker missing")
    if "ROUND14_POSITIVE_CLOSURE" in main_text or "ROUND16_POSITIVE_CLOSURE" in main_text:
        errors.append(f"{code}: superseded controlling input remains active")

    thm = len(THM.findall(text))
    proofs = len(PROOF.findall(text))
    if thm == 0 or thm != proofs:
        errors.append(f"{code}: theorem/proof mismatch {thm}/{proofs}")
    total_thm += thm
    total_proof += proofs

    labels = LABEL.findall(text)
    if len(labels) != len(set(labels)):
        errors.append(f"{code}: duplicate local labels")
    for label in labels:
        if label in all_labels:
            errors.append(f"global duplicate label {label}: {all_labels[label]} and {code}")
        all_labels[label] = code
    refs: list[str] = []
    for payload in REF.findall(text):
        refs.extend(x.strip() for x in payload.split(",") if x.strip())
    missing = sorted(set(refs) - set(labels))
    if missing:
        errors.append(f"{code}: unresolved local refs {missing}")

    objections = re.findall(r"^###\s+(\d+)\.\s+(.+)$", referee_text, re.M)
    total_objections += len(objections)
    for number, title in objections:
        if f"| {number} |" not in response_text:
            errors.append(f"{code}: author response missing objection {number}")
    for token in BANNED:
        if token.lower() in text.lower():
            errors.append(f"{code}: banned placeholder/deflection: {token}")

    report["papers"][folder.name] = {
        "code": code,
        "registered_source": entry["registered_source"],
        "source_sha256": hashlib.sha256(source_bytes).hexdigest(),
        "active_sha256": hashlib.sha256(active_bytes).hexdigest(),
        "byte_identity": byte_identity,
        "theorem_like_environments": thm,
        "proofs": proofs,
        "labels": len(labels),
        "references": len(refs),
        "objections": len(objections),
        "status": "PASS" if byte_identity and thm == proofs and not missing else "FAIL",
    }

# Explicit acyclic dependency graph.
edges = {
    "A1": [], "A2": [], "A3": ["A2"], "A4": ["A2", "A3"],
    "B2-GC": [], "B1": ["B2-GC"], "B2-MC": ["B2-GC", "B1"],
    "B3": ["B2-MC", "B1"], "B4": ["B3", "B2-MC"],
    "C1": ["B4", "B3", "B1"], "C2": ["A4", "B4", "B3"],
    "D1": ["A3", "A4", "B2-MC", "B3", "B4", "C1", "C2"],
}
visiting: set[str] = set(); visited: set[str] = set()
def visit(node: str) -> None:
    if node in visiting:
        errors.append(f"dependency cycle at {node}"); return
    if node in visited: return
    visiting.add(node)
    for dep in edges.get(node, []): visit(dep)
    visiting.remove(node); visited.add(node)
for node in edges: visit(node)

for required in (
    "ROUND17_HISTORICAL_DERIVATION_AUDIT.md",
    "ROUND17_PROOF_DEPENDENCY_LEDGER.md",
    "REFEREE_ROUND17_RESPONSE.md",
):
    if not (ROOT / required).is_file():
        errors.append(f"missing root audit document {required}")

if total_objections != 63:
    errors.append(f"parsed objection total {total_objections}, expected 63")
report.update({
    "paper_count": 11,
    "referee_objections": total_objections,
    "total_theorem_like_environments": total_thm,
    "total_proofs": total_proof,
    "dependency_dag": "PASS" if not any("dependency cycle" in x for x in errors) else "FAIL",
    "status": "PASS" if not errors else "FAIL",
})
(ROOT / "ROUND17_STRUCTURAL_VERIFICATION.json").write_text(
    json.dumps(report, indent=2, sort_keys=True) + "\n"
)
if errors:
    for error in errors: print("ROUND17_VERIFY_ERROR", error, file=sys.stderr)
    raise SystemExit(1)
print(f"ROUND17_STRUCTURAL_PASS papers=11 objections={total_objections} theorem_proof={total_thm}/{total_proof}")
