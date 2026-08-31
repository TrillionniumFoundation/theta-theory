#!/usr/bin/env python3
"""Fail-closed exact-source, theorem/proof, reference, and dependency checks."""
from __future__ import annotations

from pathlib import Path
import hashlib
import json
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "ROUND7_MATERIALIZATION_MANIFEST.json"
HEADER = "% ROUND7-REFEREE-POSITIVE-CLOSURE\n"
CONTROL_RE = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]")
ENV_RE = re.compile(r"\\begin\{(theorem|lemma|proposition|corollary)\}")
PROOF_RE = re.compile(r"\\begin\{proof\}")
LABEL_RE = re.compile(r"\\label\{([^}]+)\}")
REF_RE = re.compile(r"\\(?:ref|cref|Cref)\{([^}]+)\}")

REQUIRED = {
    "A1-exact-benchmarks": [
        "biseam completion", "horizontal germ", "Anisotropic spectral packet",
        "corner saltation currents", "dot\\tau=1",
    ],
    "A2-sinai-homological-pressure": [
        "Complemented physical realization", "Five-word joint aperiodicity",
        "4\\times4", "Near-opposition inequality", "target-dependent saddle",
    ],
    "A3-full-empirical-path-ldp": [
        "length-weighted empirical measure", "Gamma limit",
        "Excursion-profile recovery", "same period", "SPR--recession dichotomy",
    ],
    "A4-history-memory-universal-pressure": [
        "coarse history", "full microscopic history", "Dirac",
        "continuous-time suspension semigroup", "Riesz--Schur memory dilation",
    ],
    "B1-microcanonical-preparation": [
        "paraboloid", "Finite convolution rank", "empty sector",
        "mu_\\varepsilon^{n_*-1}e^{-c\\mu_\\varepsilon}",
        "Y_\\varepsilon-\\mu_\\varepsilon a'",
    ],
    "B2-collision-clusters-dynamic-ldp": [
        "measure-valued incoming trace hierarchy", "frame-reset",
        "independent of ancestral depth", "Common-root translation is not used",
        "balance defect is exactly zero",
    ],
    "B3-hamilton-boltzmann-cotangents": [
        "exact second variation", "(1-q)D^2A_f",
        "Closed balance range", "Lax--Milgram",
        "deterministic-interval estimates",
    ],
    "B4-nonlinear-kinetic-semigroups": [
        "augmented exact law state", "backward observable propagator",
        "forward Picard iteration", "partial_t c_j(t)+A(t)c_j(t)=-D_j(t)",
        "Bounded-gradient comparison",
    ],
    "C1-information-risk-sensitive-saddles": [
        "coarea posterior", "Hausdorff measure", "quenched block theorem",
        "asymptotic sufficiency", "missing denominator lower bound",
    ],
    "C2-cotangent-rigidity-tangent-representations": [
        "N_{\\rm int}", "N_{\\rm press}", "Constants are absent",
        "Weighted Folner averaging", "Covariant Doob-memory response",
    ],
    "D1-deterministic-theta-contractions": [
        "local zero-free", "face-stratified", "phase coexistence",
        "topology upgrade", "exact finite-centred local likelihood",
    ],
}

BANNED = {
    "A1-exact-benchmarks": ["ordinary isotropic Holder spectral gap"],
    "A2-sinai-homological-pressure": ["three differences form a determinant"],
    "A3-full-empirical-path-ldp": ["choose a threshold $L_N$", "add a forbidden edge"],
    "A4-history-memory-universal-pressure": [
        "complete microscopic history kernel converges to",
        "Smith--McMillan factorization applies",
    ],
    "B1-microcanonical-preparation": [
        "singleton has a full-dimensional density",
        "|\\varphi_\\varepsilon(t,u)|\\le C_M(1+\\sqrt{\\mu_\\varepsilon}|u|)^{-M}\nfor all",
    ],
    "B2-collision-clusters-dynamic-ldp": [
        "delta^{C(1+m)}", "balance commutator is $O(h^M)$", "delete later contacts",
    ],
    "B3-hamilton-boltzmann-cotangents": ["Legendre Hessian inversion therefore"],
    "B4-nonlinear-kinetic-semigroups": [
        "U_{\\rm BBGKY}(-s)", "c_j(t)=-\\int_t^T",
    ],
    "C1-information-risk-sensitive-saddles": [
        "posterior has an L1 density by Jensen",
    ],
    "C2-cotangent-rigidity-tangent-representations": [],
    "D1-deterministic-theta-contractions": [
        "locally uniformly on \\mathbb C^{d_m}",
        "gradient to infinity",
    ],
}

DAG = {
    "A1": [],
    "A2": [],
    "A3": ["A2"],
    "A4": ["A2", "A3"],
    "B2-GC": [],
    "B1": ["B2-GC"],
    "B2-MC": ["B1"],
    "B3": ["B2-MC"],
    "B4": ["B3"],
    "C1": ["B4"],
    "C2": ["A4", "B3"],
    "D1": ["A3", "A4", "B2-MC", "B3", "B4", "C1", "C2"],
}


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def check_dag() -> bool:
    visiting: set[str] = set()
    visited: set[str] = set()

    def dfs(node: str) -> None:
        if node in visiting:
            raise ValueError(f"dependency cycle at {node}")
        if node in visited:
            return
        visiting.add(node)
        for parent in DAG[node]:
            if parent not in DAG:
                raise ValueError(f"unknown dependency {parent} for {node}")
            dfs(parent)
        visiting.remove(node)
        visited.add(node)

    for node in DAG:
        dfs(node)
    return True


def main() -> None:
    if not MANIFEST_PATH.is_file():
        raise SystemExit("ROUND7 materialization manifest missing")
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    errors: list[str] = []
    results: dict[str, object] = {}
    total_env = 0
    total_proofs = 0

    for paper, meta in manifest["papers"].items():
        source_parts: list[str] = []
        source_bytes = 0
        source_hashes: list[str] = []
        for source_name in meta["sources"]:
            path = ROOT / "revision" / "round7-referee-final" / source_name
            if not path.is_file():
                errors.append(f"{paper}: missing registered source {source_name}")
                continue
            data = path.read_bytes()
            source_bytes += len(data)
            source_hashes.append(sha256(data))
            text = data.decode("utf-8")
            if CONTROL_RE.search(text):
                errors.append(f"{paper}: source contains ASCII control byte")
            source_parts.append(text.rstrip() + "\n")
        registered = "\n".join(source_parts)

        module_path = ROOT / meta["module"]
        main_path = ROOT / meta["main"]
        report_path = ROOT / meta["report"]
        response_path = ROOT / meta["response"]
        for path, label in [
            (module_path, "module"), (main_path, "main"),
            (report_path, "latest report"), (response_path, "author response"),
        ]:
            if not path.is_file():
                errors.append(f"{paper}: missing {label}: {path}")
        if not module_path.is_file() or not main_path.is_file():
            continue

        module_bytes = module_path.read_bytes()
        module_text = module_bytes.decode("utf-8")
        if module_text != HEADER + registered:
            errors.append(f"{paper}: registered-source/module byte identity failed")
        main_text = main_path.read_text(encoding="utf-8")
        if r"\input{ROUND7_POSITIVE_CLOSURE.tex}" not in main_text:
            errors.append(f"{paper}: main does not load ROUND7 module")
        if re.search(r"\\input\{ROUND[0-6]_POSITIVE_CLOSURE\.tex\}", main_text):
            errors.append(f"{paper}: main still loads an older controlling module")
        if "ROUND7-REFEREE-POSITIVE-CLOSURE" not in main_text:
            errors.append(f"{paper}: controlling revision marker absent")

        env_count = len(ENV_RE.findall(module_text))
        proof_count = len(PROOF_RE.findall(module_text))
        total_env += env_count
        total_proofs += proof_count
        if env_count != proof_count:
            errors.append(
                f"{paper}: theorem-like/proof mismatch {env_count}/{proof_count}"
            )

        labels = set(LABEL_RE.findall(module_text))
        refs = REF_RE.findall(module_text)
        missing_refs = sorted({ref for ref in refs if ref not in labels})
        if missing_refs:
            errors.append(f"{paper}: unresolved local refs {missing_refs}")
        duplicate_labels = sorted(
            {label for label in labels if module_text.count(r"\label{" + label + "}") > 1}
        )
        if duplicate_labels:
            errors.append(f"{paper}: duplicate labels {duplicate_labels}")

        for token in REQUIRED[paper]:
            if token not in module_text:
                errors.append(f"{paper}: required repair token absent: {token}")
        for token in BANNED[paper]:
            if token in module_text:
                errors.append(f"{paper}: banned failed mechanism remains: {token}")

        results[paper] = {
            "status": "PASS",
            "source_bytes": source_bytes,
            "source_sha256_parts": source_hashes,
            "module_bytes": len(module_bytes),
            "module_sha256": sha256(module_bytes),
            "theorem_like_environments": env_count,
            "proofs": proof_count,
            "labels": len(labels),
            "references": len(refs),
        }

    try:
        dag_pass = check_dag()
    except ValueError as exc:
        dag_pass = False
        errors.append(str(exc))

    output = {
        "schema": "theta-theory-round7-structural-verification-v1",
        "status": "PASS" if not errors else "FAIL",
        "paper_count": len(manifest["papers"]),
        "dependency_dag": "PASS" if dag_pass else "FAIL",
        "total_theorem_like_environments": total_env,
        "total_proofs": total_proofs,
        "papers": results,
        "errors": errors,
    }
    (ROOT / "ROUND7_STRUCTURAL_VERIFICATION.json").write_text(
        json.dumps(output, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    if errors:
        for error in errors:
            print(f"ROUND7_VERIFY_ERROR {error}", file=sys.stderr)
        raise SystemExit(1)
    print(
        f"ROUND7_STRUCTURAL_VERIFICATION_PASS papers={len(results)} "
        f"theorem_proof={total_env}/{total_proofs}"
    )


if __name__ == "__main__":
    main()
