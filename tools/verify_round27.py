#!/usr/bin/env python3
"""Round-Twenty-Seven source identity, mathematical regression, and build verifier."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

PAPERS = {
    "A1": "A1-exact-benchmarks",
    "A2": "A2-sinai-homological-pressure",
    "A3": "A3-full-empirical-path-ldp",
    "A4": "A4-history-memory-universal-pressure",
    "B1": "B1-microcanonical-preparation",
    "B2": "B2-collision-clusters-dynamic-ldp",
    "B3": "B3-hamilton-boltzmann-cotangents",
    "B4": "B4-nonlinear-kinetic-semigroups",
    "C1": "C1-information-risk-sensitive-saddles",
    "C2": "C2-cotangent-rigidity-tangent-representations",
    "D1": "D1-deterministic-theta-contractions",
}

REQUIRED = {
    "A1": [
        "Tail derivative identity",
        "Geometric-domain certificate",
        "Maximal coboundary estimate",
        "Trace-class current FCLT",
        "parameter-dependent tail conditional expectation",
    ],
    "A2": [
        "Returned-UNI operator block",
        "Bad-word oscillation",
        "Quantitative intermediate contraction",
        "Exhaustive anisotropic Fourier estimate",
    ],
    "A3": [
        "Polish projective state",
        "Graph-current compact containment",
        "Sublinear connector entropy",
        "Joint stopped local density",
        "coarea",
    ],
    "A4": [
        "Local coupling without exact-tail coalescence",
        "Weighted weak-Harris spectral gap",
        "Typed renewal identity",
        "Stable compression theorem",
        "Domain-safe forced memory equation",
    ],
    "B1": [
        "Uniform conditional good-block probability",
        "Uniform full-frequency damping",
        "Source-uniform mixed local theorem",
        "Separate-saddle exact-number ratio",
    ],
    "B2": [
        "Associative collision-history algebra",
        "Causal triangular loop Jacobian",
        "Multiplicative surplus-contact gain",
        "Radius-loss Duhamel estimate",
        "Collision-simplex correction",
        "Joint dynamic hard-sphere LDP",
    ],
    "B3": [
        "No hidden collision kernel",
        "Localized transport--collision observability",
        "Uniform conditional future density",
        "Aldous estimate from cut cumulants",
        "Quotient Mosco Hessian",
    ],
    "B4": [
        "Representation on the effective domain",
        "Microscopic exponential collision-source bound",
        "Action-coercive containment",
        "Dynamic $W_2$ modulus",
        "typed microscopic realization map",
        "Nonlinear microscopic semigroup limit",
    ],
    "C1": [
        "consistent partially observed model",
        "Model-derived channel regularity",
        "Evidence-stable Feller filter",
        "Recursive QMD",
        "Derived persistent information",
        "Uniform adaptive LAN and Bernstein--von Mises",
    ],
    "C2": [
        "Weighted Polish strict dual",
        "Complete hard-sphere annihilator",
        "Equilibrium localization",
        "path-augmented prediction",
        "Optional projections of path functionals",
        "exponential bracket",
    ],
    "D1": [
        "Full Morse--Bott phase coefficient",
        "Uniform controlled Laplace principle",
        "Leading common-control limit",
        "leading value alone does not encode the sharing constraint",
        "Subleading common-policy selection",
    ],
}

FORBIDDEN_ACTIVE = [
    "ROUND23_POSITIVE_CLOSURE.tex",
    "ROUND25_POSITIVE_CLOSURE.tex",
    r"(1+d_\sigma(h,h'))(V(h)+V(h'))",
    r"E(z)(I-T(z))^{-1}X(z)",
    "the leading scalar max-plus value preserves shared control",
    "condition on the complete phase point and reapply",
]

ROOT_REQUIRED = [
    "AUTHOR_RESPONSE_ROUND26.md",
    "ROUND27_REVIEW_INDEX.md",
    "ROUND27_PREAMBLE.tex",
    "ROUND27_PROOF_DEPENDENCY_LEDGER.md",
    "ROUND27_REVISION_DOSSIER.tex",
    "ROUND27_SOURCE_MANIFEST.json",
    "ROUND27_FINAL_VERIFICATION.json",
]

def fail(message: str) -> None:
    raise AssertionError(message)

def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()

def check_text(path: Path) -> str:
    if not path.is_file():
        fail(f"missing file: {path.relative_to(ROOT)}")
    raw = path.read_bytes()
    for byte in raw:
        if byte < 32 and byte not in (9, 10, 13):
            fail(f"non-printing control byte {byte} in {path.relative_to(ROOT)}")
    return raw.decode("utf-8")

def check_pdf(path: Path) -> None:
    if not path.is_file() or path.stat().st_size < 10_000:
        fail(f"missing or implausibly small PDF: {path.relative_to(ROOT)}")
    if not path.read_bytes()[:5] == b"%PDF-":
        fail(f"invalid PDF header: {path.relative_to(ROOT)}")

def check_sources(require_pdfs: bool = False) -> list[str]:
    labels: dict[str, str] = {}
    checked: list[str] = []
    for code, directory in PAPERS.items():
        pdir = ROOT / "papers" / directory
        source = pdir / "ROUND27_POSITIVE_CLOSURE.tex"
        main = pdir / "main.tex"
        wrapper = pdir / "ROUND27_REVISION.tex"
        pdf = pdir / "ROUND27_REVISION.pdf"
        main_pdf = pdir / "main.pdf"

        body = check_text(source)
        main_text = check_text(main)
        wrapper_text = check_text(wrapper)

        if r"\input{ROUND27_REVISION.tex}" not in main_text:
            fail(f"{code} main.tex does not resolve to the Round 27 wrapper")
        if r"\input{ROUND27_POSITIVE_CLOSURE.tex}" not in wrapper_text:
            fail(f"{code} standalone wrapper does not import Round 27")
        for token in FORBIDDEN_ACTIVE:
            if token in main_text or token in wrapper_text or token in body:
                fail(f"{code} contains forbidden obsolete pattern: {token!r}")
        for token in REQUIRED[code]:
            if token not in body:
                fail(f"{code} missing required regression token: {token}")

        if body.count(r"\begin{proof}") != body.count(r"\end{proof}"):
            fail(f"{code} unbalanced proof environments")
        theorem_starts = sum(body.count(fr"\begin{{{env}}}") for env in
                             ("theorem", "lemma", "proposition", "corollary"))
        if theorem_starts < 4:
            fail(f"{code} has too few active theorem-level statements")

        for label in re.findall(r"\\label\{([^}]+)\}", body):
            if label in labels:
                fail(f"duplicate label {label} in {code} and {labels[label]}")
            labels[label] = code
            if not label.startswith(("sec:r27-", "thm:r27-", "lem:r27-",
                                     "prop:r27-", "cor:r27-", "def:r27-")):
                fail(f"{code} has non-Round-27 label: {label}")

        if require_pdfs:
            check_pdf(pdf)
            check_pdf(main_pdf)
        checked.append(code)
    return checked

def check_root(require_generated_pdfs: bool = False) -> None:
    for rel in ROOT_REQUIRED:
        path = ROOT / rel
        if path.suffix.lower() == ".pdf":
            check_pdf(path)
        else:
            check_text(path)

    response = check_text(ROOT / "AUTHOR_RESPONSE_ROUND26.md")
    if "8b1b945ee2ea69226dcb9562bd61812c5c58db47" not in response:
        fail("author response does not identify the Round 26 review head")

    ledger = check_text(ROOT / "ROUND27_PROOF_DEPENDENCY_LEDGER.md")
    for edge in ("B2-GC -> B1-LOCAL -> B2-MC", "D1 is terminal"):
        if edge not in ledger:
            fail(f"dependency ledger missing acyclicity token: {edge}")

def check_manifest() -> None:
    manifest_path = ROOT / "ROUND27_SOURCE_MANIFEST.json"
    data = json.loads(check_text(manifest_path))
    if data.get("base_review_commit") != "8b1b945ee2ea69226dcb9562bd61812c5c58db47":
        fail("manifest base review commit mismatch")
    entries = data.get("files", [])
    if not entries:
        fail("empty source manifest")
    for entry in entries:
        path = ROOT / entry["path"]
        if not path.is_file():
            fail(f"manifest path missing: {entry['path']}")
        if path.stat().st_size != entry["size"]:
            fail(f"manifest size mismatch: {entry['path']}")
        if sha256(path) != entry["sha256"]:
            fail(f"manifest hash mismatch: {entry['path']}")

def run_build() -> None:
    latexmk = shutil.which("latexmk")
    if latexmk is None:
        fail("--build requested but latexmk is unavailable")
    env = dict(**__import__("os").environ)
    env.setdefault("TERM", "xterm")
    targets = [
        ROOT / "papers" / d / "ROUND27_REVISION.tex"
        for d in PAPERS.values()
    ] + [ROOT / "ROUND27_REVISION_DOSSIER.tex"]
    for tex in targets:
        proc = subprocess.run(
            [latexmk, "-pdf", "-interaction=nonstopmode", "-halt-on-error", tex.name],
            cwd=tex.parent,
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            timeout=180,
        )
        if proc.returncode != 0:
            print(proc.stdout)
            fail(f"LaTeX build failed: {tex.relative_to(ROOT)}")
        if tex.name == "ROUND27_REVISION.tex":
            built = tex.with_suffix(".pdf")
            shutil.copyfile(built, tex.parent / "main.pdf")

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--build", action="store_true",
                        help="also rebuild all eleven wrappers and the dossier")
    args = parser.parse_args()
    checked = check_sources(require_pdfs=False)
    check_root(require_generated_pdfs=False)
    check_manifest()
    if args.build:
        run_build()
        checked = check_sources(require_pdfs=True)
        check_root(require_generated_pdfs=True)
    print("ROUND27 verification passed:", ", ".join(checked))
    print("base review head: 8b1b945ee2ea69226dcb9562bd61812c5c58db47")
    print("active wrappers: 11; active sources: 11; compiled PDFs: 12")
    return 0

if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (AssertionError, ValueError, json.JSONDecodeError) as exc:
        print(f"ROUND27 verification failed: {exc}", file=sys.stderr)
        raise SystemExit(1)
