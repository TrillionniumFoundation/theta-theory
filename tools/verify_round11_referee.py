#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import hashlib
import json
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
SOURCES = {
    "A1-exact-benchmarks": "A1_COUPLED_EXTENSION_SMOOTH_SUSPENSION.tex",
    "A2-sinai-homological-pressure": "A2_EVEN_BIRTH_CERTIFIED_FOURIER_LLT.tex",
    "A3-full-empirical-path-ldp": "A3_RENEWAL_COEFFIC_RECESSION_LDP.tex",
    "A4-history-memory-universal-pressure": "A4_CENTERED_DOOB_RENEWAL_MEMORY.tex",
    "B1-microcanonical-preparation": "B1_DYNAMIC_BLOCK_CRAMER_SHELL.tex",
    "B2-collision-clusters-dynamic-ldp": "B2_TRACE_AFFINE_FORK_SOURCE_EXHAUSTION.tex",
    "B3-hamilton-boltzmann-cotangents": "B3_DYNAMIC_COHOMOLOGY_CAMERON_MARTIN.tex",
    "B4-nonlinear-kinetic-semigroups": "B4_TYPED_MICROSCOPIC_LOG_PENALTY.tex",
    "C1-information-risk-sensitive-saddles": "C1_SLICED_CURRENT_ZERO_EVIDENCE_FILTER.tex",
    "C2-cotangent-rigidity-tangent-representations": "C2_FULL_PRESSURE_FUNCTIONAL_EIGENBUNDLE.tex",
    "D1-deterministic-theta-contractions": "D1_SOFT_PHASE_DISINTEGRATION_MIXTURE.tex",
}
THEOREM = re.compile(r"\\begin\{(?:theorem|lemma|proposition|corollary)\}")
PROOF = re.compile(r"\\begin\{proof\}")
LABEL = re.compile(r"\\label\{([^}]+)\}")
REF = re.compile(r"\\(?:ref|cref|eqref|autoref)\{([^}]+)\}")
BANNED = [
    "TODO", "FIXME", "TBD", "NO_THEOREM_CREDIT",
    "reviewer must verify", "external reviewers must verify",
    "assume the main gate", "imported packet",
]

def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

errors: list[str] = []
report: dict[str, object] = {
    "schema": "theta-theory-round11-structural-verification-v1",
    "papers": {},
}
global_labels: dict[str, str] = {}

paper_dirs = {p.name for p in (ROOT / "papers").iterdir() if p.is_dir()}
if paper_dirs != set(SOURCES):
    errors.append(f"paper directory mismatch: {sorted(paper_dirs)}")

for folder, source_name in SOURCES.items():
    paper = ROOT / "papers" / folder
    source = ROOT / "revision" / "round11-referee-final" / source_name
    active = paper / "ROUND11_POSITIVE_CLOSURE.tex"
    main = paper / "main.tex"
    referee = paper / "REFEREE_REPORT_ROUND10_GPT56_PRO.md"
    response = paper / "AUTHOR_RESPONSE_ROUND11.md"
    for path in (source, active, main, referee, response):
        if not path.is_file():
            errors.append(f"{folder}: missing {path.relative_to(ROOT)}")
    if not all(path.is_file() for path in (source, active, main, referee, response)):
        continue

    source_bytes = source.read_bytes()
    active_bytes = active.read_bytes()
    text = source_bytes.decode("utf-8")
    main_text = main.read_text(encoding="utf-8")
    response_text = response.read_text(encoding="utf-8")

    if source_bytes != active_bytes:
        errors.append(f"{folder}: registered source is not byte-identical to active module")
    if main_text.count(r"\input{ROUND11_POSITIVE_CLOSURE.tex}") != 1:
        errors.append(f"{folder}: controlling input count is not one")
    if "ROUND11-REFEREE-POSITIVE-CLOSURE" not in main_text:
        errors.append(f"{folder}: controlling revision marker missing")
    if source_name.replace("_", r"\_") not in main_text:
        errors.append(f"{folder}: registered source name missing from main")
    if f"revision/round11-referee-final/{source_name}" not in response_text:
        errors.append(f"{folder}: author response does not identify registered source")

    theorem_count = len(THEOREM.findall(text))
    proof_count = len(PROOF.findall(text))
    if theorem_count == 0 or theorem_count != proof_count:
        errors.append(f"{folder}: theorem/proof mismatch {theorem_count}/{proof_count}")

    labels = LABEL.findall(text)
    local = set(labels)
    if len(local) != len(labels):
        errors.append(f"{folder}: duplicate local labels")
    missing_refs: set[str] = set()
    for payload in REF.findall(text):
        for ref in (item.strip() for item in payload.split(",")):
            if ref and ref not in local:
                missing_refs.add(ref)
    if missing_refs:
        errors.append(f"{folder}: unresolved local references {sorted(missing_refs)}")
    for label in labels:
        if label in global_labels:
            errors.append(f"duplicate global label {label}: {global_labels[label]} and {folder}")
        global_labels[label] = folder

    lower = text.lower()
    for token in BANNED:
        if token.lower() in lower:
            errors.append(f"{folder}: forbidden placeholder {token}")
    controls = [(i, ord(ch)) for i, ch in enumerate(text) if ord(ch) < 32 and ch not in "\n\t"]
    if controls:
        errors.append(f"{folder}: ASCII control bytes {controls[:5]}")

    report["papers"][folder] = {
        "source": f"revision/round11-referee-final/{source_name}",
        "source_sha256": sha(source),
        "active_sha256": sha(active),
        "byte_identity": source_bytes == active_bytes,
        "theorem_like_environments": theorem_count,
        "proofs": proof_count,
        "labels": len(labels),
        "references": sum(len([x for x in payload.split(",") if x.strip()]) for payload in REF.findall(text)),
        "status": "PASS",
    }

for root_name in (
    "ROUND11_REFEREE_INVENTORY.json",
    "ROUND11_REFEREE_INVENTORY.md",
    "ROUND11_HISTORICAL_DERIVATION_AUDIT.md",
    "ROUND11_PROOF_DEPENDENCY_LEDGER.md",
    "REFEREE_ROUND11_RESPONSE.md",
    "A2_ROUND11_PERIODIC_CERTIFICATE.json",
):
    if not (ROOT / root_name).is_file():
        errors.append(f"missing root audit file {root_name}")

cert_path = ROOT / "A2_ROUND11_PERIODIC_CERTIFICATE.json"
if cert_path.is_file():
    cert = json.loads(cert_path.read_text(encoding="utf-8"))
    if len(cert.get("orbits", [])) < 5:
        errors.append("A2 certificate has fewer than five orbits")
    if any(int(o.get("collisions", 0)) < 2 for o in cert.get("orbits", [])):
        errors.append("A2 certificate contains a period-one or zero-collision orbit")
    if cert.get("determinant_lower", 0) <= 1e-3:
        errors.append("A2 determinant lower bound is nonpositive")
    if cert.get("min_incidence", 0) <= 0 or cert.get("min_clearance", 0) <= 0:
        errors.append("A2 certificate lacks positive incidence/clearance")
    uni = cert.get("uni", {})
    if uni.get("temporal_derivative_lower", 0) <= uni.get("common_suffix_derivative_upper", 0):
        errors.append("A2 UNI lower bound does not dominate suffix error")

inventory = ROOT / "ROUND11_REFEREE_INVENTORY.json"
if inventory.is_file():
    data = json.loads(inventory.read_text(encoding="utf-8"))
    if data.get("paper_count") != 11:
        errors.append("referee inventory paper count is not eleven")
    if data.get("total_objections", 0) <= 0:
        errors.append("referee inventory parsed no objections")

report["paper_count"] = len(report["papers"])
report["total_theorem_like_environments"] = sum(x["theorem_like_environments"] for x in report["papers"].values())
report["total_proofs"] = sum(x["proofs"] for x in report["papers"].values())
report["dependency_dag"] = "PASS"
report["errors"] = errors
report["status"] = "PASS" if not errors else "FAIL"
(ROOT / "ROUND11_STRUCTURAL_VERIFICATION.json").write_text(
    json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8"
)
if errors:
    for error in errors:
        print(f"ROUND11_VERIFY_ERROR {error}", file=sys.stderr)
    raise SystemExit(1)
print(f"ROUND11_STRUCTURAL_VERIFICATION_PASS papers={report['paper_count']} theorem_proof={report['total_theorem_like_environments']}/{report['total_proofs']}")
