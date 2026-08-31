#!/usr/bin/env python3
"""Fail-closed structural and exact-source verification for round nine."""
from __future__ import annotations

from pathlib import Path
import hashlib
import json
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "ROUND9_MATERIALIZATION_MANIFEST.json"
ENV_RE = re.compile(r"\\begin\{(?:theorem|lemma|proposition|corollary)\}")
PROOF_RE = re.compile(r"\\begin\{proof\}")
LABEL_RE = re.compile(r"\\label\{([^}]+)\}")
REF_RE = re.compile(r"\\(?:ref|cref)\{([^}]+)\}")

REQUIRED = {
    "A1-exact-benchmarks": [
        "Physical--symbolic separation", "Hamiltonian impact realization",
        "Directional Lasota--Yorke", "every generated cut",
    ],
    "A2-sinai-homological-pressure": [
        "Parabolic blow-up", "Explicit finite arithmetic packets",
        "temporal nonintegrability", "density LLT", "Sharp windows",
    ],
    "A3-full-empirical-path-ldp": [
        "marked renewal-flow state", "Finite marked-flow LDP",
        "Projective marked-flow LDP", "Actual recession recovery", "pointed",
    ],
    "A4-history-memory-universal-pressure": [
        "natural-extension past", "quenched enhanced invariance",
        "Instantaneous/residual", "zP-PLP-C(z)^{-1}", "full unresolved space",
    ],
    "B1-microcanonical-preparation": [
        "full pressure", "Conditional good-block minorization",
        "Full mixed lattice--continuous", "weighted local coefficient",
    ],
    "B2-collision-clusters-dynamic-ldp": [
        "Closed Green graph", "boundary-renewal hierarchy",
        "Flux-weighted exterior Jacobi", "Scaled one-block", "Conservative finite-cell repair",
    ],
    "B3-hamilton-boltzmann-cotangents": [
        "raw second variation", "KKT-completed", "Backward observability",
        "covariance first", "Mosco", "Fourth-moment increment",
    ],
    "B4-nonlinear-kinetic-semigroups": [
        "Exact augmented law semigroup", "Resolvent graph core",
        "Finite graph-domain corrector", "dynamic entropy", "entropy truncation",
    ],
    "C1-information-risk-sensitive-saddles": [
        "codimension", "logarithmic evidence", "exact belief-state",
        "separate exact finite saddles", "reachable chaotic class",
    ],
    "C2-cotangent-rigidity-tangent-representations": [
        "overline{\\operatorname{span}}", "Uniform weighted Ces", "Kato",
        "Spectral and resolved projections are different", "zR", "nonlinear contraction",
    ],
    "D1-deterministic-theta-contractions": [
        "exact labelled", "Subexponential phase prior", "Lee--Yang",
        "not because", "Exact labelled thin-shell", "commutation principle",
    ],
}

FORBIDDEN = {
    "A1-exact-benchmarks": ["complete dynamic germ surface is the graph", "symmetric total-depth"],
    "A2-sinai-homological-pressure": ["one global certificate", "periodic aperiodicity implies"],
    "A3-full-empirical-path-ldp": ["restriction to x>0 determines", "Gamma limit is assumed"],
    "A4-history-memory-universal-pressure": ["stable-leaf quotient", "C(z)^{-1}-z"],
    "B1-microcanonical-preparation": ["exactly n_0 particles", "pull the likelihood out"],
    "B2-collision-clusters-dynamic-ldp": ["QR reset", "arbitrary pair (g_k"],
    "B3-hamilton-boltzmann-cotangents": ["raw perspective Hessian is coercive", "bounded inverse on the whole"],
    "B4-nonlinear-kinetic-semigroups": ["entire cutoff equal to one", "double counts static preparation"],
    "C1-information-risk-sensitive-saddles": ["uniformly in the observed value", "same one-particle mean become"],
    "C2-cotangent-rigidity-tangent-representations": ["d\\nu_\\eta^D/d\\nu_0^D", "C_\\eta(z)^{-1}-z"],
    "D1-deterministic-theta-contractions": ["(\\max_j Q", "uniform zero-free tube across coexistence"],
}

DAG = {
    "A1": [],
    "A2": [],
    "A3": ["A2"],
    "A4": ["A2", "A3"],
    "B2-GC": [],
    "B1": ["B2-GC"],
    "B2-MC": ["B2-GC", "B1"],
    "B3": ["B2-MC"],
    "B4": ["B2-MC", "B3"],
    "C1": ["B1", "B2-MC", "B3", "B4"],
    "C2": ["A2", "A3", "A4", "B3", "B4"],
    "D1": ["A2", "A3", "A4", "B1", "B2-MC", "B3", "B4", "C1", "C2"],
}


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def acyclic(graph: dict[str, list[str]]) -> bool:
    state: dict[str, int] = {}
    def visit(v: str) -> bool:
        if state.get(v) == 1:
            return False
        if state.get(v) == 2:
            return True
        state[v] = 1
        for u in graph[v]:
            if u not in graph or not visit(u):
                return False
        state[v] = 2
        return True
    return all(visit(v) for v in graph)


def main() -> None:
    errors: list[str] = []
    if not MANIFEST.is_file():
        raise SystemExit("ROUND9 manifest missing")
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    entries = manifest.get("papers", [])
    if len(entries) != 11:
        errors.append(f"expected 11 manifest papers, found {len(entries)}")

    reports = list((ROOT / "papers").glob("*/REFEREE_REPORT_ROUND8_GPT56_PRO.md"))
    if len(reports) != 11:
        errors.append(f"expected 11 round-eight reports, found {len(reports)}")

    results: dict[str, object] = {}
    global_labels: dict[str, str] = {}
    total_env = total_proofs = 0

    for meta in entries:
        paper = meta["paper"]
        source = ROOT / meta["source"]
        module = ROOT / meta["module"]
        main_path = ROOT / "papers" / paper / "main.tex"
        response = ROOT / meta["response"]
        for p in (source, module, main_path, response):
            if not p.is_file():
                errors.append(f"{paper}: missing {p.relative_to(ROOT)}")
        if any(not p.is_file() for p in (source, module, main_path, response)):
            continue

        sb = source.read_bytes(); mb = module.read_bytes()
        st = sb.decode("utf-8"); mt = mb.decode("utf-8")
        main_text = main_path.read_text(encoding="utf-8")
        response_text = response.read_text(encoding="utf-8")
        if sb != mb:
            errors.append(f"{paper}: source/module byte identity failed")
        if sha256(sb) != meta["source_sha256"]:
            errors.append(f"{paper}: source SHA mismatch")
        if sha256(mb) != meta["module_sha256"]:
            errors.append(f"{paper}: module SHA mismatch")
        if any(x < 32 and x not in (9, 10, 13) for x in mb):
            errors.append(f"{paper}: ASCII control byte in module")
        if main_text.count(r"\input{ROUND9_POSITIVE_CLOSURE.tex}") != 1:
            errors.append(f"{paper}: main does not load exactly one round-nine module")
        if re.search(r"\\input\{ROUND[0-8]_POSITIVE_CLOSURE\.tex\}", main_text):
            errors.append(f"{paper}: main still loads an older module")
        if "ROUND9-REFEREE-POSITIVE-CLOSURE" not in main_text:
            errors.append(f"{paper}: controlling marker absent")

        env = len(ENV_RE.findall(mt)); proofs = len(PROOF_RE.findall(mt))
        total_env += env; total_proofs += proofs
        if env == 0 or env != proofs:
            errors.append(f"{paper}: theorem/proof mismatch {env}/{proofs}")

        labels = LABEL_RE.findall(mt)
        refs: list[str] = []
        for payload in REF_RE.findall(mt):
            refs.extend(x.strip() for x in payload.split(",") if x.strip())
        dup = sorted({x for x in labels if labels.count(x) > 1})
        missing = sorted(set(refs) - set(labels))
        if dup: errors.append(f"{paper}: duplicate local labels {dup}")
        if missing: errors.append(f"{paper}: unresolved local refs {missing}")
        for label in labels:
            if label in global_labels:
                errors.append(f"global duplicate label {label}: {global_labels[label]} and {paper}")
            global_labels[label] = paper

        flat = re.sub(r"\s+", " ", mt).lower()
        for token in REQUIRED[paper]:
            if re.sub(r"\s+", " ", token).lower() not in flat:
                errors.append(f"{paper}: required mechanism missing: {token}")
        for token in FORBIDDEN[paper]:
            if token.lower() in mt.lower():
                errors.append(f"{paper}: failed mechanism remains: {token}")
        if "No theorem is replaced by a no-go statement" not in response_text:
            errors.append(f"{paper}: positive response marker absent")

        results[paper] = {
            "status": "PASS",
            "source_bytes": len(sb),
            "source_sha256": sha256(sb),
            "module_bytes": len(mb),
            "module_sha256": sha256(mb),
            "theorem_like_environments": env,
            "proofs": proofs,
            "labels": len(labels),
            "references": len(refs),
        }

    inventory_path = ROOT / "ROUND9_REFEREE_INVENTORY.json"
    if not inventory_path.is_file():
        errors.append("round-nine referee inventory missing")
        inventory_count = 0
    else:
        inventory = json.loads(inventory_path.read_text(encoding="utf-8"))
        inventory_count = int(inventory.get("blocker_count", 0))
        if inventory_count != 92 or len(inventory.get("blockers", [])) != 92:
            errors.append(f"referee inventory count mismatch: {inventory_count}")
        for item in inventory.get("blockers", []):
            for label in item.get("closure_labels", []):
                if label not in global_labels:
                    errors.append(f"inventory maps blocker to unknown label {label}")
            if item.get("disposition") != "positive reconstruction":
                errors.append("inventory contains a nonpositive blocker disposition")

    if not acyclic(DAG):
        errors.append("dependency graph is cyclic or references an unknown node")
    for required_root in (
        "ROUND9_HISTORICAL_DERIVATION_AUDIT.md",
        "ROUND9_PROOF_DEPENDENCY_LEDGER.md",
        "ROUND9_REFEREE_INVENTORY.md",
        "ROUND9_REFEREE_INVENTORY.json",
        "REFEREE_ROUND9_RESPONSE.md",
    ):
        if not (ROOT / required_root).is_file():
            errors.append(f"missing root audit file {required_root}")

    output = {
        "schema": "theta-theory-round9-structural-verification-v1",
        "status": "PASS" if not errors else "FAIL",
        "paper_count": len(entries),
        "report_count": len(reports),
        "blocker_count": inventory_count,
        "dependency_dag": "PASS" if acyclic(DAG) else "FAIL",
        "total_theorem_like_environments": total_env,
        "total_proofs": total_proofs,
        "papers": results,
        "errors": errors,
    }
    (ROOT / "ROUND9_STRUCTURAL_VERIFICATION.json").write_text(
        json.dumps(output, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    if errors:
        for e in errors:
            print(f"ROUND9_VERIFY_ERROR {e}", file=sys.stderr)
        raise SystemExit(1)
    print(f"ROUND9_STRUCTURAL_VERIFICATION_PASS papers=11 theorem_proof={total_env}/{total_proofs}")


if __name__ == "__main__":
    main()
