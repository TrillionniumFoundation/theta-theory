#!/usr/bin/env python3
"""Round-Thirty-One active-source, counterexample, build, and PDF verifier."""
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
        "Buffered differentiation",
        "Seam shell and two-sided projection decay",
        "Common-level trace-class FCLT and covariance response",
        r"\mathscr H_r:=\mathbb J^{m+2r}",
        r"\iota_{m+2j,m+2r}",
        r"(1+|q|)^{1/2}",
    ],
    "A2": [
        "Exact Diophantine arithmetic leaf",
        "Twisted complement estimate",
        "Integrable all-frequency estimate",
        "Source-uniform mixed Edgeworth local theorem",
        r"|b|\ge B_0",
        r"|b|>n^A",
        r"\cL_\xi^n=\lambda(\xi)^n\Pi(\xi)",
    ],
    "A3": [
        "Exact renewal relation",
        "Transition-count entropy action",
        "Two-scale chronological current",
        "Matrix-amplitude stopped local theorem",
        r"\nu_N={1\over N}\sum",
        r"\cA(Q)=",
        r"\partial_sL+\operatorname{div}_{U}\cJ",
    ],
    "A4": [
        "Weighted weak-Harris gap",
        "Finite-amplitude continuation along a certified bridge",
        "Resolvent-certified relative perturbation",
        "Stable compressed generator",
        "Admissible vertical-line memory calculus",
        r"\norm{A(z-L_0)^{-1}}",
        r"e_j\in D(L^*)",
    ],
    "B1": [
        "Quadratic relative-energy smoothing",
        "Stratified anchor damping",
        "Exact-number mixed Edgeworth theorem",
        "Dimension-consistent separate-saddle ratio",
        r"e_\perp(w)={1\over2}|w|^2",
        "anchor variables are not included in any good-block test",
    ],
    "B2": [
        "Constructed causal right inverse",
        "Chronological pivot induction",
        "All-graph multiplicative loop gain",
        "Ovsyannikov collision-history evolution",
        "Finite-time factorial tree propagation",
        "Grand-canonical pressure and joint dynamic LDP",
        r"a(t)=a_0-\Lambda t",
        r"DF_TX_e=0",
    ],
    "B3": [
        "Full joint collision Hessian",
        "Even deterministic-interval moments",
        "Uniform temporal modulus",
        "Aldous estimate in the temporal filtration",
        "Joint density/contact process CLT",
        "Full-contact Mosco theorem",
        "No root-resampling",
    ],
    "B4": [
        "Ballistic energy compactification",
        "Compact energy shells",
        "Ballistic energy path compactness",
        "Shellwise strongly continuous semigroup",
        "Comparison on compact ballistic shells",
        "Microscopic semigroup limit on ballistic shells",
        "No global sup-norm strong continuity",
        "zero-recession face",
    ],
    "C1": [
        "Whole-channel normalization",
        "Distributional projective push-forward",
        "Observable-quotient derivative stability",
        "Adaptive LAN and Bernstein--von Mises",
        r"\sum_s p_s(\vartheta,a,x)=1",
        r"p_s(\vartheta,a,x)\rho_s",
        "No strict contraction is claimed for latent directions",
        "Hellinger separation of the induced observation laws",
    ],
    "C2": [
        "Weighted strict dual on a Polish state",
        "Full kinetic annihilator",
        "Correct discrete hidden-model likelihood",
        "Quantitative filter stability",
        "Stable optional projections of full paths",
        "Discrete BSDE stability",
        "Marked-point BSDE stability",
        "Brownian BSDE stability",
        r"\Pi_{k-1}^\vartheta",
        r"\Pi_{k-1}^{\vartheta_0}",
    ],
    "D1": [
        "Mixed lattice--Morse--Bott dichotomy",
        "Finite-memory policy expansion",
        "Causal finite-memory approximation",
        "Policy-uniform controlled expansion",
        "Lexicographic common-policy selection",
        r"\kappa_j^{\rm fib}",
        r"\kappa_j^{\rm cell}",
        r"{K_N-Nk_j\over\sqrt N}",
        "Policies are optimized, not integrated",
    ],
}

FORBIDDEN_ACTIVE = [
    "ROUND29_POSITIVE_CLOSURE.tex",
    "ROUND29_REVISION.tex",
    "ROUND27_POSITIVE_CLOSURE.tex",
    "exact nonarithmeticity is open",
    "A(q,L)",
    "integrated against holding occupation",
    "common filter in numerator and denominator",
    r"\sqrt N(\xi_N-m_{J_N})",
    "applying Morse--Bott integration on the policy manifold",
    "entropy and energy imply W_2 compactness",
    "condition on the root revealment",
]

ROOT_REQUIRED = [
    "AUTHOR_RESPONSE_ROUND30.md",
    "ROUND31_CHANGELOG.md",
    "ROUND31_FINAL_VERIFICATION.json",
    "ROUND31_MATHEMATICAL_REGRESSIONS.md",
    "ROUND31_PREAMBLE.tex",
    "ROUND31_PROOF_DEPENDENCY_LEDGER.md",
    "ROUND31_REVIEW_INDEX.md",
    "ROUND31_REVISION_DOSSIER.tex",
    "ROUND31_SOURCE_MANIFEST.json",
    ".github/workflows/verify-round31-referee-closure.yml",
]

BASE_REVIEW_HEAD = "4c6aa83111d404d9139acad1699b1f31bdb792e4"
REVIEWED_SOURCE = "76f7ae36d7f894673383ceccda41c86b1cb6ac5c"


def fail(message: str) -> None:
    raise AssertionError(message)


def check_text(path: Path) -> str:
    if not path.is_file():
        fail(f"missing file: {path.relative_to(ROOT)}")
    raw = path.read_bytes()
    for byte in raw:
        if byte < 32 and byte not in (9, 10, 13):
            fail(f"control byte {byte} in {path.relative_to(ROOT)}")
    return raw.decode("utf-8")


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def pdf_pages(path: Path) -> int:
    pdfinfo = shutil.which("pdfinfo")
    if not pdfinfo:
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
    if not path.is_file() or path.stat().st_size < 15000:
        fail(f"missing or implausibly small PDF: {path.relative_to(ROOT)}")
    if path.read_bytes()[:5] != b"%PDF-":
        fail(f"invalid PDF header: {path.relative_to(ROOT)}")
    pages = pdf_pages(path)
    if pages < minimum_pages:
        fail(f"too few pages ({pages}): {path.relative_to(ROOT)}")
    return pages


def check_log(tex: Path) -> None:
    log = tex.with_suffix(".log")
    text = check_text(log)
    fatal = [
        "Undefined control sequence",
        "LaTeX Error:",
        "Emergency stop",
        "Fatal error occurred",
        "There were undefined references",
        "There were undefined citations",
    ]
    for token in fatal:
        if token in text:
            fail(f"{token} in {log.relative_to(ROOT)}")


def check_sources(require_pdfs: bool = False) -> tuple[list[str], dict[str, int]]:
    labels: dict[str, str] = {}
    checked: list[str] = []
    pages: dict[str, int] = {}

    for code, directory in PAPERS.items():
        paper_dir = ROOT / "papers" / directory
        source = paper_dir / "ROUND31_POSITIVE_CLOSURE.tex"
        wrapper = paper_dir / "ROUND31_REVISION.tex"
        main = paper_dir / "main.tex"
        pdf = paper_dir / "ROUND31_REVISION.pdf"
        main_pdf = paper_dir / "main.pdf"

        body = check_text(source)
        wrapper_text = check_text(wrapper)
        main_text = check_text(main)

        if r"\input{ROUND31_REVISION.tex}" not in main_text:
            fail(f"{code}: main.tex does not resolve to Round 31")
        if r"\input{ROUND31_POSITIVE_CLOSURE.tex}" not in wrapper_text:
            fail(f"{code}: wrapper does not import Round 31 source")
        if r"\input{../../ROUND31_PREAMBLE.tex}" not in wrapper_text:
            fail(f"{code}: wrapper does not import Round 31 preamble")

        active = body + "\n" + wrapper_text + "\n" + main_text
        for token in FORBIDDEN_ACTIVE:
            if token in active:
                fail(f"{code}: forbidden obsolete token {token!r}")
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
                "sec:r31-", "thm:r31-", "lem:r31-", "prop:r31-",
                "cor:r31-", "def:r31-", "ass:r31-", "con:r31-",
            )):
                fail(f"{code}: non-Round-31 label {label}")

        if require_pdfs:
            pages[code] = check_pdf(pdf, 4)
            check_pdf(main_pdf, 4)
            check_log(wrapper)
        checked.append(code)

    return checked, pages


def check_root(require_pdfs: bool = False) -> int | None:
    for rel in ROOT_REQUIRED:
        check_text(ROOT / rel)

    response = check_text(ROOT / "AUTHOR_RESPONSE_ROUND30.md")
    if BASE_REVIEW_HEAD not in response or REVIEWED_SOURCE not in response:
        fail("author response does not identify the exact review/source commits")

    ledger = check_text(ROOT / "ROUND31_PROOF_DEPENDENCY_LEDGER.md")
    for token in (
        "B2-GC -> B1-EDGE -> B2-MC",
        "transition marginal `nu`",
        "D1 imports exactly",
        "D1 remains terminal",
    ):
        if token not in ledger:
            fail(f"dependency ledger missing token {token!r}")

    regressions = check_text(ROOT / "ROUND31_MATHEMATICAL_REGRESSIONS.md")
    if regressions.count("R31-") < 44:
        fail("mathematical regression ledger has fewer than 44 rows")

    manifest = json.loads(check_text(ROOT / "ROUND31_SOURCE_MANIFEST.json"))
    if manifest.get("active_round") != 31:
        fail("manifest active round mismatch")
    if manifest.get("controlling_review_commit") != BASE_REVIEW_HEAD:
        fail("manifest review head mismatch")
    if manifest.get("reviewed_mathematical_commit") != REVIEWED_SOURCE:
        fail("manifest reviewed source mismatch")
    for code, rel in manifest.get("active_papers", {}).items():
        if code not in PAPERS or not (ROOT / rel).is_file():
            fail(f"invalid manifest active paper: {code} -> {rel}")
    if len(manifest.get("active_papers", {})) != 11:
        fail("manifest must list eleven active papers")

    if require_pdfs:
        dossier = ROOT / "ROUND31_REVISION_DOSSIER.pdf"
        pages = check_pdf(dossier, 45)
        check_log(ROOT / "ROUND31_REVISION_DOSSIER.tex")
        return pages
    return None


def run_latex(tex: Path) -> None:
    latexmk = shutil.which("latexmk")
    if not latexmk:
        fail("--build requested but latexmk is unavailable")
    env = dict(os.environ)
    env.setdefault("TERM", "xterm")
    proc = subprocess.run(
        [latexmk, "-pdf", "-interaction=nonstopmode", "-halt-on-error", tex.name],
        cwd=tex.parent,
        env=env,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=300,
    )
    if proc.returncode != 0:
        print(proc.stdout)
        fail(f"LaTeX build failed: {tex.relative_to(ROOT)}")


def render_first_page(pdf: Path) -> None:
    pdftoppm = shutil.which("pdftoppm")
    if not pdftoppm:
        fail("pdftoppm unavailable")
    with tempfile.TemporaryDirectory(prefix="round31-render-") as temp:
        target = Path(temp) / "page"
        proc = subprocess.run(
            [pdftoppm, "-f", "1", "-singlefile", "-r", "96", "-png",
             str(pdf), str(target)],
            text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
            timeout=120,
        )
        png = target.with_suffix(".png")
        if proc.returncode != 0 or not png.is_file() or png.stat().st_size < 1000:
            print(proc.stdout)
            fail(f"render failed: {pdf.relative_to(ROOT)}")


def run_build() -> None:
    for directory in PAPERS.values():
        tex = ROOT / "papers" / directory / "ROUND31_REVISION.tex"
        run_latex(tex)
        shutil.copyfile(tex.with_suffix(".pdf"), tex.parent / "main.pdf")
    run_latex(ROOT / "ROUND31_REVISION_DOSSIER.tex")


def write_runtime_result(checked: list[str], pages: dict[str, int], dossier_pages: int | None) -> None:
    files = [ROOT / "ROUND31_REVISION_DOSSIER.pdf"] + [
        ROOT / "papers" / directory / "ROUND31_REVISION.pdf"
        for directory in PAPERS.values()
    ]
    hashes = {
        str(path.relative_to(ROOT)): sha256(path)
        for path in files if path.is_file()
    }
    result = {
        "status": "pass",
        "active_round": 31,
        "checked_papers": checked,
        "paper_pages": pages,
        "dossier_pages": dossier_pages,
        "pdf_sha256": hashes,
        "review_head": BASE_REVIEW_HEAD,
        "reviewed_source": REVIEWED_SOURCE,
    }
    (ROOT / "ROUND31_CI_VERIFICATION.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--build", action="store_true")
    args = parser.parse_args()

    checked, pages = check_sources(require_pdfs=False)
    check_root(require_pdfs=False)

    dossier_pages = None
    if args.build:
        run_build()
        checked, pages = check_sources(require_pdfs=True)
        dossier_pages = check_root(require_pdfs=True)
        for directory in PAPERS.values():
            render_first_page(ROOT / "papers" / directory / "ROUND31_REVISION.pdf")
        render_first_page(ROOT / "ROUND31_REVISION_DOSSIER.pdf")

    write_runtime_result(checked, pages, dossier_pages)
    print("ROUND31 verification passed:", ", ".join(checked))
    print("review head:", BASE_REVIEW_HEAD)
    if args.build:
        print("paper pages:", json.dumps(pages, sort_keys=True))
        print("dossier pages:", dossier_pages)
        print("built and rendered PDFs: 12")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (AssertionError, ValueError, json.JSONDecodeError, subprocess.SubprocessError) as exc:
        print(f"ROUND31 verification failed: {exc}", file=sys.stderr)
        raise SystemExit(1)
