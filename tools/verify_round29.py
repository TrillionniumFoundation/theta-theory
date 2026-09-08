#!/usr/bin/env python3
"""Round-Twenty-Nine active-source, regression, build, and PDF verifier."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
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
        "Correct direction of distributional loss",
        "Coherent shell and cumulative boundary data",
        "Affine seam-current membership",
        "actual polygonal interpolation",
        "Trace-class current FCLT with response",
        r"\nabla_a:\mathbb J^s\longrightarrow\mathbb J^{s+2}",
    ],
    "A2": [
        "Jacobian-weighted finite grammar certificate",
        "Certificate validation and nonemptiness",
        "Finite-automaton bad-word estimate",
        "Correct continuous-character annihilator",
        "All-frequency anisotropic estimate",
        r"\beta_2=(\sqrt2,\sqrt3)",
    ],
    "A3": [
        "Exact finite-word telescoping identity",
        "Two graph clocks and bounded recession mass",
        "Mass-budget compactification",
        "Derived power drift",
        "Gaussian--overshoot stopped local theorem",
        r"O_N=S_{\nu_N}R-N",
    ],
    "A4": [
        "History transportation and a compatible function space",
        "Weighted weak-Harris operator gap",
        "Typed suspension renewal identity",
        "Graph-isomorphic compression",
        "Memory on a vertical half-plane",
        "No sectorial estimate is used",
    ],
    "B1": [
        "A universal coarea anchor on every component",
        "Configurationwise anchor density",
        "Exceptional-component smoothing",
        "Source-uniform exact-number local theorem",
        "Dimension-consistent coefficient ratio",
    ],
    "B2": [
        "The disintegrated cut-kernel category",
        "Associative disintegrated history algebra",
        "Constraint-preserving triangular rank",
        "Multiplicative loop gain",
        "Radius-loss Duhamel estimate",
        "Joint hard-sphere dynamic LDP",
        "fully labelled histories the exponential-generating coefficient",
    ],
    "B3": [
        "Normal and cycle contact defects",
        "Full contact cost and density contraction",
        "Global near-Maxwellian observability",
        "Stopped cluster revealment",
        "Joint density/contact process CLT",
        "Full-contact Mosco Hessian",
    ],
    "B4": [
        "Joint and contracted actions",
        "Correct effective-domain representation",
        "Energy-supported path compactness",
        "Preparation--dynamics factorization",
        r"V_0=I",
        "Recovery-independent realization",
        "Nonlinear microscopic semigroup limit",
    ],
    "C1": [
        "A normalized stratified observation channel",
        "Exact envelope normalization",
        "Belief derivatives in a negative Sobolev scale",
        "Differentiable deterministic push-forward",
        "Noncircular persistent excitation",
        "Global identification and adaptive Bernstein--von Mises",
        r"\rho_s(y-\mathcal O^a_{\vartheta,s}(x))\over q_s(y)",
    ],
    "C2": [
        "no compact exhaustion",
        "Weighted Polish strict dual",
        "Complete full-contact annihilator",
        "One fixed stopped-path prediction space",
        "Discrete-time product likelihood",
        "Marked-point likelihood",
        "Brownian diagnostic likelihood",
    ],
    "D1": [
        "Finite-dimensional mixed local input",
        "Noncircular labelled rates and prior support",
        r"J_+(w)=\{j:w_j>0\}",
        "Closed adapted policy compactness",
        "Epi-argmax rather than policy integration",
        "Lexicographic common-policy selection",
        "There is no Morse--Bott factor from the policy set",
    ],
}

FORBIDDEN_ACTIVE = [
    "ROUND27_REVISION.tex",
    "ROUND27_POSITIVE_CLOSURE.tex",
    "ROUND25_POSITIVE_CLOSURE.tex",
    r"\mathbb J^{m+2r-2j}",
    "applying Morse--Bott integration on that common-policy manifold",
    "the leading scalar max-plus value preserves shared control",
    "condition on the complete phase point and reapply",
]

ROOT_REQUIRED = [
    "AUTHOR_RESPONSE_ROUND28.md",
    "ROUND29_CHANGELOG.md",
    "ROUND29_MATHEMATICAL_REGRESSIONS.md",
    "ROUND29_PREAMBLE.tex",
    "ROUND29_PROOF_DEPENDENCY_LEDGER.md",
    "ROUND29_REVIEW_INDEX.md",
    "ROUND29_REVISION_DOSSIER.tex",
    "ROUND29_SOURCE_MANIFEST.json",
    "ROUND29_FINAL_VERIFICATION.json",
    ".github/workflows/verify-round29-referee-closure.yml",
]

BASE_REVIEW_HEAD = "12bfa8d233078a3a0fb2e25b9e9ab7245c62c2e7"


def fail(message: str) -> None:
    raise AssertionError(message)


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
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


def pdf_pages(path: Path) -> int:
    pdfinfo = shutil.which("pdfinfo")
    if pdfinfo is None:
        fail("pdfinfo unavailable")
    proc = subprocess.run(
        [pdfinfo, str(path)], check=True, text=True,
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
    )
    match = re.search(r"^Pages:\s+(\d+)$", proc.stdout, re.MULTILINE)
    if not match:
        fail(f"cannot read page count: {path.relative_to(ROOT)}")
    return int(match.group(1))


def check_pdf(path: Path, minimum_pages: int) -> int:
    if not path.is_file() or path.stat().st_size < 20_000:
        fail(f"missing or implausibly small PDF: {path.relative_to(ROOT)}")
    if path.read_bytes()[:5] != b"%PDF-":
        fail(f"invalid PDF header: {path.relative_to(ROOT)}")
    pages = pdf_pages(path)
    if pages < minimum_pages:
        fail(f"too few PDF pages ({pages}): {path.relative_to(ROOT)}")
    return pages


def check_sources(require_pdfs: bool = False) -> tuple[list[str], dict[str, int]]:
    labels: dict[str, str] = {}
    checked: list[str] = []
    page_inventory: dict[str, int] = {}

    for code, directory in PAPERS.items():
        paper_dir = ROOT / "papers" / directory
        source = paper_dir / "ROUND29_POSITIVE_CLOSURE.tex"
        wrapper = paper_dir / "ROUND29_REVISION.tex"
        main = paper_dir / "main.tex"
        pdf = paper_dir / "ROUND29_REVISION.pdf"
        main_pdf = paper_dir / "main.pdf"

        body = check_text(source)
        wrapper_text = check_text(wrapper)
        main_text = check_text(main)

        if r"\input{ROUND29_REVISION.tex}" not in main_text:
            fail(f"{code}: main.tex does not resolve to Round 29")
        if r"\input{ROUND29_POSITIVE_CLOSURE.tex}" not in wrapper_text:
            fail(f"{code}: wrapper does not import Round 29 source")
        if r"\input{../../ROUND29_PREAMBLE.tex}" not in wrapper_text:
            fail(f"{code}: wrapper does not import Round 29 preamble")

        active_text = body + "\n" + wrapper_text + "\n" + main_text
        for token in FORBIDDEN_ACTIVE:
            if token in active_text:
                fail(f"{code}: forbidden obsolete pattern {token!r}")
        for token in REQUIRED[code]:
            if token not in body:
                fail(f"{code}: missing regression token {token!r}")

        if body.count(r"\begin{proof}") != body.count(r"\end{proof}"):
            fail(f"{code}: unbalanced proof environments")
        theorem_count = sum(
            body.count(fr"\begin{{{env}}}")
            for env in ("theorem", "lemma", "proposition", "corollary")
        )
        if theorem_count < 5:
            fail(f"{code}: too few theorem-level statements ({theorem_count})")

        for label in re.findall(r"\\label\{([^}]+)\}", body):
            if label in labels:
                fail(f"duplicate label {label}: {code} and {labels[label]}")
            labels[label] = code
            if not label.startswith((
                "sec:r29-", "thm:r29-", "lem:r29-", "prop:r29-",
                "cor:r29-", "def:r29-", "ass:r29-", "con:r29-",
            )):
                fail(f"{code}: non-Round-29 label {label}")

        if require_pdfs:
            page_inventory[code] = check_pdf(pdf, 4)
            check_pdf(main_pdf, 4)
        checked.append(code)

    return checked, page_inventory


def check_root(require_pdfs: bool = False) -> int | None:
    for rel in ROOT_REQUIRED:
        check_text(ROOT / rel)

    response = check_text(ROOT / "AUTHOR_RESPONSE_ROUND28.md")
    if BASE_REVIEW_HEAD not in response:
        fail("author response does not identify the controlling Round 28 head")

    ledger = check_text(ROOT / "ROUND29_PROOF_DEPENDENCY_LEDGER.md")
    for token in (
        "B2-GC -> B1-LOCAL -> B2-MC",
        "D1 is terminal",
        "B3 uses B2 histories; B2 does not use B3",
    ):
        if token not in ledger:
            fail(f"dependency ledger missing acyclicity token: {token}")

    regressions = check_text(ROOT / "ROUND29_MATHEMATICAL_REGRESSIONS.md")
    if regressions.count("R29-") < 30:
        fail("regression ledger is incomplete")

    if require_pdfs:
        return check_pdf(ROOT / "ROUND29_REVISION_DOSSIER.pdf", 45)
    return None


def check_manifest() -> None:
    manifest_path = ROOT / "ROUND29_SOURCE_MANIFEST.json"
    data = json.loads(check_text(manifest_path))
    if data.get("base_review_commit") != BASE_REVIEW_HEAD:
        fail("source manifest base review commit mismatch")
    if data.get("active_round") != 29:
        fail("source manifest active round mismatch")
    entries = data.get("files", [])
    if len(entries) < 40:
        fail("source manifest has too few entries")
    for entry in entries:
        path = ROOT / entry["path"]
        if not path.is_file():
            fail(f"manifest path missing: {entry['path']}")
        if path.stat().st_size != entry["size"]:
            fail(f"manifest size mismatch: {entry['path']}")
        if sha256(path) != entry["sha256"]:
            fail(f"manifest hash mismatch: {entry['path']}")


def run_latex(tex: Path) -> None:
    latexmk = shutil.which("latexmk")
    if latexmk is None:
        fail("--build requested but latexmk is unavailable")
    env = dict(os.environ)
    env.setdefault("TERM", "xterm")
    proc = subprocess.run(
        [latexmk, "-pdf", "-interaction=nonstopmode", "-halt-on-error", tex.name],
        cwd=tex.parent,
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        timeout=240,
    )
    if proc.returncode != 0:
        print(proc.stdout)
        fail(f"LaTeX build failed: {tex.relative_to(ROOT)}")


def render_first_page(pdf: Path) -> None:
    pdftoppm = shutil.which("pdftoppm")
    if pdftoppm is None:
        fail("pdftoppm unavailable")
    with tempfile.TemporaryDirectory(prefix="round29-render-") as temp:
        target = Path(temp) / "page"
        proc = subprocess.run(
            [pdftoppm, "-f", "1", "-singlefile", "-r", "96", "-png", str(pdf), str(target)],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            timeout=120,
        )
        png = target.with_suffix(".png")
        if proc.returncode != 0 or not png.is_file() or png.stat().st_size < 1_000:
            print(proc.stdout)
            fail(f"PDF render verification failed: {pdf.relative_to(ROOT)}")


def run_build() -> None:
    for directory in PAPERS.values():
        tex = ROOT / "papers" / directory / "ROUND29_REVISION.tex"
        run_latex(tex)
        built = tex.with_suffix(".pdf")
        shutil.copyfile(built, tex.parent / "main.pdf")
    run_latex(ROOT / "ROUND29_REVISION_DOSSIER.tex")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--build", action="store_true")
    args = parser.parse_args()

    checked, pages = check_sources(require_pdfs=False)
    check_root(require_pdfs=False)
    check_manifest()

    if args.build:
        run_build()
        checked, pages = check_sources(require_pdfs=True)
        dossier_pages = check_root(require_pdfs=True)
        for directory in PAPERS.values():
            render_first_page(ROOT / "papers" / directory / "ROUND29_REVISION.pdf")
        render_first_page(ROOT / "ROUND29_REVISION_DOSSIER.pdf")
    else:
        dossier_pages = None

    print("ROUND29 verification passed:", ", ".join(checked))
    print("base review head:", BASE_REVIEW_HEAD)
    if args.build:
        print("individual page inventory:", json.dumps(pages, sort_keys=True))
        print("dossier pages:", dossier_pages)
        print("active wrappers: 11; active sources: 11; rendered PDFs: 12")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (AssertionError, ValueError, json.JSONDecodeError, subprocess.SubprocessError) as exc:
        print(f"ROUND29 verification failed: {exc}", file=sys.stderr)
        raise SystemExit(1)
