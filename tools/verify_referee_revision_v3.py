#!/usr/bin/env python3
"""Fail-closed structural and formula verifier for θ-Theory referee revision v3.

The script verifies the five controlling LaTeX manuscripts, their bibliography
and internal labels, the theorem anchors named by the revision manifest, and a
small collection of exact finite-dimensional identities.  It does not certify
infinite-dimensional analytical proofs and does not replace external review.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
import sys
from fractions import Fraction
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "papers" / "referee-ready"

PAPERS: dict[str, dict[str, Any]] = {
    "paper_I": {
        "folder": "paper-I-bilateral-response",
        "main": "main-submission.tex",
        "title": "Bilateral Response, Exact Innovations",
        "anchors": {
            "thm:bilateral",
            "thm:fdq",
            "thm:totalization",
            "prop:collision",
            "thm:nonconjugacy",
            "lem:contraction",
            "lem:letters",
            "thm:allorder",
            "thm:innovations",
            "cor:martingale",
            "thm:specular",
        },
        "required_text": {
            "Branches two and three contain the regular interior fixed points",
            "W^{N+2,1}",
            "Exact innovation theorem",
        },
        "forbidden_text": {
            "branches one, two, and three contain",
            "branches 1, 2, and 3 contain",
            "three regular interior fixed points",
        },
    },
    "paper_II": {
        "folder": "paper-II-pressure-diffusion",
        "main": "main-final.tex",
        "title": "Pressure, Physical Diffusion",
        "anchors": {
            "thm:bundle",
            "thm:pressure",
            "thm:physical",
            "thm:renewal",
            "thm:GK",
            "thm:actual",
            "ass:dio",
            "lem:phase",
            "thm:HF",
            "thm:triangle",
        },
        "required_text": {
            "0\\le\\operatorname{Re}z\\le\\sigma_0",
            "{\\sqrt3\\over4}<r<{1\\over2}",
            "symmetrized Green--Kubo",
        },
        "forbidden_text": {
            "0.34<r<0.49",
            "1/3<r<1/2",
            "symmetric strip",
        },
    },
    "paper_III": {
        "folder": "paper-III-rough-theta",
        "main": "main-final.tex",
        "title": "Exact-Innovation Rough Homogenization",
        "anchors": {
            "thm:innovations",
            "thm:rough",
            "thm:homogenization",
            "prop:block",
            "thm:rate",
            "lem:consistency",
            "thm:HJB",
        },
        "required_text": {
            "{\\varepsilon^2\\over2}",
            "canonical geometric step-two lift",
            "pointwise finite-branch entropic recursion",
        },
        "forbidden_text": {
            "paired residual implies",
            "anisotropic pairing gives the viscosity",
        },
    },
    "paper_IV": {
        "folder": "paper-IV-filtering-games",
        "main": "main-final.tex",
        "title": "Noncompact Filtering and Pure Isaacs",
        "anchors": {
            "lem:Bayes",
            "lem:drift",
            "thm:filter",
            "thm:collapse",
            "thm:VI",
            "prop:saddle",
            "lem:consistency",
            "thm:scheme",
            "thm:feedback",
            "thm:endtoend",
        },
        "required_text": {
            "variational inequality",
            "Gaussian refresh--autoregression",
            "Curvature-compensation pure-saddle theorem",
        },
        "forbidden_text": {
            "one-step prior erasure",
            "mixed Isaacs equality therefore gives a pure saddle",
        },
    },
    "paper_V": {
        "folder": "paper-V-representations",
        "main": "main-final.tex",
        "title": "Tangent Laws and Stochastic Representations",
        "anchors": {
            "thm:fixedlaw",
            "thm:IFT",
            "thm:analytic",
            "thm:cocycle",
            "thm:tangent",
            "thm:Girsanov",
            "thm:BSDE",
            "cor:tangentBSDE",
            "thm:path",
            "thm:pathgame",
            "thm:2BSDE",
        },
        "required_text": {
            "Radon--Nikodym derivative",
            "Novikov condition",
            "No inversion of the map",
            "stable under conditioning and pasting",
        },
        "forbidden_text": {
            "Z=p",
            "invert Z=",
            "formal Girsanov shift",
        },
    },
}

TOP_REQUIRED = {
    "REVISION_V3_POSITIVE_RESPONSE_TO_REFEREES.md",
    "COMMON_REFERENCE_PLATFORM_V3_FINAL.md",
    "REVISION_V3_FORMULA_AUDIT.json",
    "REVISION_V3_HOSTILE_PROOF_AUDIT.md",
    "REVISION_V3_THEOREM_MANIFEST.yaml",
    "REFEREE_REVISION_V3_STATUS.md",
}

CITE_RE = re.compile(
    r"\\cite[a-zA-Z*]*(?:\[[^\]]*\])?(?:\[[^\]]*\])?\{([^}]*)\}"
)
BIB_RE = re.compile(r"@[a-zA-Z]+\s*\{\s*([^,\s]+)")
LABEL_RE = re.compile(r"\\label\{([^}]+)\}")
REF_RE = re.compile(r"\\(?:eqref|ref|cref|Cref)\{([^}]+)\}")
SECTION_RE = re.compile(r"\\section\*?\{")
THEOREM_RE = re.compile(
    r"\\begin\{(?:theorem|proposition|lemma|corollary)\}"
)
BEGIN_RE = re.compile(r"\\begin\{([^}]+)\}")
END_RE = re.compile(r"\\end\{([^}]+)\}")

GLOBAL_FORBIDDEN = {
    "TODO",
    "FIXME",
    "TBD",
    "proof omitted",
    "left to the reader",
    "known gap",
    "\\nrac",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def split_keys(groups: list[str]) -> set[str]:
    keys: set[str] = set()
    for group in groups:
        keys.update(k.strip() for k in group.split(",") if k.strip())
    return keys


def formula_checks() -> dict[str, bool]:
    # Bilateral interpolation, evaluated with exact rational arithmetic at a
    # nondegenerate test tuple and separately checked symbolically by the
    # committed formula receipt.
    A, B, C, D = Fraction(2), Fraction(3), Fraction(1), Fraction(1)
    lam = (B + D) / (A + B + C + D)
    exp_m = -lam * A + (1 - lam) * D
    exp_n = lam * C - (1 - lam) * B
    crossed = exp_m == exp_n == (C * D - A * B) / (A + B + C + D)

    w2_lo, w2_hi = Fraction(3, 20), Fraction(1, 4)
    w3_lo, w3_hi = Fraction(11, 40), Fraction(13, 40)
    fixed_ranges = w2_hi < w3_lo

    # Triangular lattice row spacing and radius thresholds.
    triangle = math.sqrt(3.0) / 4.0 < 0.45 < 0.5

    # Geometric second level in one scalar component.
    xs = [Fraction(2), Fraction(-1), Fraction(3)]
    second = sum(xs[i] * xs[j] for i in range(3) for j in range(i + 1, 3))
    second += Fraction(1, 2) * sum(x * x for x in xs)
    geometric = second == Fraction(1, 2) * sum(xs) ** 2

    # Refresh--AR Lyapunov identity at a representative exact tuple.
    delta, r, y = Fraction(1, 4), Fraction(1, 2), Fraction(3, 2)
    alpha = (1 - delta) * r * r
    ew = delta * 2 + (1 - delta) * (1 + (r * y) ** 2 + (1 - r * r))
    refresh = ew == alpha * (1 + y * y) + 2 * (1 - alpha)

    # Pure quadratic saddle and completed squares.
    mu, nu, p, u, v = Fraction(5), Fraction(2), Fraction(3), Fraction(4), Fraction(-2)
    c = Fraction(1, 2) * (1 / mu - 1 / nu)
    u_star, v_star = p / mu, -p / nu
    value = p * (u_star + v_star) - mu * u_star * u_star / 2 + nu * v_star * v_star / 2
    saddle = value == c * p * p
    lhs = -c * p * p + p * (u + v) - mu * u * u / 2 + nu * v * v / 2
    rhs = -mu * (u - p / mu) ** 2 / 2 + nu * (v + p / nu) ** 2 / 2
    squares = lhs == rhs

    # Girsanov exponential drift cancellation.
    theta, z = Fraction(3, 2), Fraction(5, 3)
    girsanov = theta * (-theta * z * z / 2) + theta * theta * z * z / 2 == 0

    return {
        "bilateral_crossed_exponents": crossed,
        "regular_fixed_multiplier_ranges": fixed_ranges,
        "triangular_radius_window": triangle,
        "geometric_second_level_diagonal": geometric,
        "refresh_AR_Lyapunov": refresh,
        "quadratic_saddle_value": saddle,
        "completed_squares": squares,
        "Girsanov_density_drift": girsanov,
    }


def verify_tex(
    paper: str,
    cfg: dict[str, Any],
    errors: list[str],
    warnings: list[str],
    hashes: dict[str, str],
) -> dict[str, Any]:
    folder = BASE / cfg["folder"]
    main_path = folder / cfg["main"]
    bib_path = folder / "references.bib"
    result: dict[str, Any] = {
        "folder": str(folder.relative_to(ROOT)),
        "main": str(main_path.relative_to(ROOT)),
    }

    for path in (main_path, bib_path):
        if not path.is_file():
            errors.append(f"{paper}: missing {path.relative_to(ROOT)}")
            return result
        hashes[str(path.relative_to(ROOT))] = sha256(path)

    text = main_path.read_text(encoding="utf-8")
    bib = bib_path.read_text(encoding="utf-8")
    lower = text.lower()

    required_doc = {
        "\\documentclass",
        "\\begin{abstract}",
        "\\maketitle",
        "\\tableofcontents",
        "\\bibliography{references}",
        "\\end{document}",
        "Disclosure and review status",
    }
    for token in required_doc:
        if token not in text:
            errors.append(f"{paper}: missing document token {token!r}")

    if cfg["title"] not in text:
        errors.append(f"{paper}: controlling title fragment missing")

    byte_count = len(text.encode("utf-8"))
    line_count = text.count("\n") + 1
    section_count = len(SECTION_RE.findall(text))
    theorem_count = len(THEOREM_RE.findall(text))
    if byte_count < 15000:
        errors.append(f"{paper}: controlling manuscript too short ({byte_count} bytes)")
    if line_count < 300:
        errors.append(f"{paper}: controlling manuscript too short ({line_count} lines)")
    if section_count < 7:
        errors.append(f"{paper}: too few sections ({section_count})")
    if theorem_count < 7:
        errors.append(f"{paper}: too few theorem environments ({theorem_count})")

    labels = LABEL_RE.findall(text)
    label_set = set(labels)
    if len(labels) != len(label_set):
        dup = sorted({x for x in labels if labels.count(x) > 1})
        errors.append(f"{paper}: duplicate labels {dup}")

    for anchor in cfg["anchors"]:
        if anchor not in label_set:
            errors.append(f"{paper}: missing theorem anchor {anchor}")

    refs = split_keys(REF_RE.findall(text))
    unresolved_refs = refs - label_set
    if unresolved_refs:
        errors.append(f"{paper}: unresolved internal refs {sorted(unresolved_refs)}")

    bib_keys = set(BIB_RE.findall(bib))
    cite_keys = split_keys(CITE_RE.findall(text))
    unresolved_cites = cite_keys - bib_keys
    if unresolved_cites:
        errors.append(f"{paper}: unresolved citation keys {sorted(unresolved_cites)}")
    unused = bib_keys - cite_keys
    if unused:
        warnings.append(f"{paper}: unused bibliography keys {sorted(unused)}")

    begins = BEGIN_RE.findall(text)
    ends = END_RE.findall(text)
    for env in set(begins) | set(ends):
        if begins.count(env) != ends.count(env):
            errors.append(
                f"{paper}: unbalanced environment {env}: "
                f"{begins.count(env)} begin / {ends.count(env)} end"
            )

    for token in cfg["required_text"]:
        if token not in text:
            errors.append(f"{paper}: required proof text missing {token!r}")
    for token in cfg["forbidden_text"]:
        if token.lower() in lower:
            errors.append(f"{paper}: superseded text still present {token!r}")
    for token in GLOBAL_FORBIDDEN:
        if token.lower() in lower:
            errors.append(f"{paper}: forbidden draft marker {token!r}")

    result.update(
        bytes=byte_count,
        lines=line_count,
        sections=section_count,
        theorem_environments=theorem_count,
        labels=len(label_set),
        references=len(refs),
        citation_keys=len(cite_keys),
        bibliography_entries=len(bib_keys),
    )
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--write-receipt",
        action="store_true",
        help="write the JSON result to papers/referee-ready/REVISION_V3_VERIFICATION_RECEIPT.json",
    )
    args = parser.parse_args()

    errors: list[str] = []
    warnings: list[str] = []
    hashes: dict[str, str] = {}
    papers: dict[str, Any] = {}

    if not BASE.is_dir():
        print(json.dumps({"status": "FAIL", "error": f"missing {BASE}"}))
        return 1

    for name in TOP_REQUIRED:
        path = BASE / name
        if not path.is_file():
            errors.append(f"missing top-level revision file {name}")
        else:
            hashes[str(path.relative_to(ROOT))] = sha256(path)

    for paper, cfg in PAPERS.items():
        papers[paper] = verify_tex(paper, cfg, errors, warnings, hashes)

    formulas = formula_checks()
    for name, passed in formulas.items():
        if not passed:
            errors.append(f"formula check failed: {name}")

    manifest_path = BASE / "REVISION_V3_THEOREM_MANIFEST.yaml"
    if manifest_path.is_file():
        manifest = manifest_path.read_text(encoding="utf-8")
        required_manifest = {
            "known_proof_blockers_in_declared_scopes: 0",
            "positively_repaired_in_controlling_files: 15",
            "second_external_referee_review: NOT_YET_PERFORMED",
        }
        for token in required_manifest:
            if token not in manifest:
                errors.append(f"manifest boundary missing {token!r}")

    output = {
        "schema": "THETA_REFEREE_REVISION_V3_VERIFY_V1",
        "status": "PASS" if not errors else "FAIL",
        "papers": papers,
        "formula_checks": formulas,
        "errors": errors,
        "warnings": warnings,
        "sha256": dict(sorted(hashes.items())),
        "latex_compilation_checked": False,
        "analytical_proofs_certified_by_script": False,
        "second_external_referee_review": "NOT_YET_PERFORMED",
    }

    rendered = json.dumps(output, ensure_ascii=False, indent=2, sort_keys=True)
    print(rendered)
    if args.write_receipt:
        receipt = BASE / "REVISION_V3_VERIFICATION_RECEIPT.json"
        receipt.write_text(rendered + "\n", encoding="utf-8")
    return 0 if not errors else 1


if __name__ == "__main__":
    sys.exit(main())
