#!/usr/bin/env python3
"""Structural verifier for the six normative referee-revision-v4 appendices.

This checker validates existence, size, LaTeX structure, local references,
bibliography keys, and the absence of superseded dependency shortcuts.  It
does not certify the mathematical arguments.
"""

from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "papers" / "referee-ready"

APPENDICES = {
    "paper_I_symbolic": (
        "paper-I-bilateral-response",
        "technical-appendix-v4.tex",
        9000,
        {
            "lem:Jacobi",
            "thm:analytic-sequence",
            "cor:coding",
            "lem:analytic-operator",
            "thm:normal-susceptibility",
            "prop:noncoboundary",
        },
    ),
    "paper_II_frequency": (
        "paper-II-pressure-diffusion",
        "technical-appendix-v4.tex",
        10000,
        {
            "lem:quotient-inverse",
            "lem:circle",
            "cor:imaginary-gap",
            "lem:strip-gap",
            "thm:strip-resolvent",
            "lem:twisted-letter",
            "thm:derivative-word",
            "lem:oscillatory",
            "prop:Dolgopyat-block",
        },
    ),
    "paper_III_rough": (
        "paper-III-rough-theta",
        "technical-appendix-v4.tex",
        10000,
        {
            "lem:disintegration",
            "thm:endogenous-innovation",
            "prop:tensorization",
            "lem:geometric",
            "lem:BDG2",
            "thm:lifted-martingale",
            "lem:Riemann-bracket",
            "lem:uniform-consistency",
            "thm:pointwise-viscosity",
            "prop:theta-independent",
        },
    ),
    "paper_III_clock": (
        "paper-III-rough-theta",
        "physical-clock-appendix-v4.tex",
        8000,
        {
            "lem:clock-decomp",
            "thm:clock-limit",
            "thm:physical-SDE",
            "lem:physical-consistency",
            "thm:physical-HJB",
        },
    ),
    "paper_IV_filter_game": (
        "paper-IV-filtering-games",
        "technical-appendix-v4.tex",
        9000,
        {
            "lem:Bayes-bound",
            "lem:prediction",
            "thm:posterior",
            "lem:convolution",
            "lem:mixed",
            "thm:VI",
            "lem:localization",
            "prop:pure-consistency",
            "thm:common-limit",
            "prop:smooth-approx",
        },
    ),
    "paper_V_tangent": (
        "paper-V-representations",
        "technical-appendix-v4.tex",
        10000,
        {
            "lem:tilt-solution",
            "lem:replicator-unique",
            "thm:full-characterization",
            "prop:cocycle-equivalence",
            "lem:tilted-convergence",
            "prop:kernel-convergence",
            "lem:bounded-density",
            "lem:stochastic-log",
            "prop:two-routes",
            "thm:true-Girsanov",
            "prop:three-tangents",
            "prop:DPP-2BSDE",
        },
    ),
}

FORBIDDEN = {
    "TODO",
    "FIXME",
    "TBD",
    "proof omitted",
    "left to the reader",
    "A1--A5",
    "S1--S3",
    "viscosity-duality",
    "FormalCredit",
    "LATEST-WINS",
    "\\nrac",
}

LABEL_RE = re.compile(r"\\label\{([^}]+)\}")
REF_RE = re.compile(r"\\(?:eqref|ref|cref|Cref)\{([^}]+)\}")
CITE_RE = re.compile(
    r"\\cite[a-zA-Z*]*(?:\[[^\]]*\])?(?:\[[^\]]*\])?\{([^}]*)\}"
)
BIB_RE = re.compile(r"@[a-zA-Z]+\s*\{\s*([^,\s]+)")
BEGIN_RE = re.compile(r"\\begin\{([^}]+)\}")
END_RE = re.compile(r"\\end\{([^}]+)\}")
THEOREM_RE = re.compile(
    r"\\begin\{(?:theorem|proposition|lemma|corollary)\}"
)
SECTION_RE = re.compile(r"\\section\*?\{")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def split_keys(groups: list[str]) -> set[str]:
    out: set[str] = set()
    for group in groups:
        out.update(k.strip() for k in group.split(",") if k.strip())
    return out


def main() -> int:
    errors: list[str] = []
    warnings: list[str] = []
    results: dict[str, object] = {}
    hashes: dict[str, str] = {}

    manifest = BASE / "TECHNICAL_APPENDICES_V4.md"
    if not manifest.is_file():
        errors.append("missing TECHNICAL_APPENDICES_V4.md")
    else:
        hashes[str(manifest.relative_to(ROOT))] = sha256(manifest)

    for name, (folder_name, file_name, min_bytes, anchors) in APPENDICES.items():
        folder = BASE / folder_name
        path = folder / file_name
        bib_path = folder / "references.bib"
        if not path.is_file():
            errors.append(f"{name}: missing {path.relative_to(ROOT)}")
            continue
        if not bib_path.is_file():
            errors.append(f"{name}: missing bibliography {bib_path.relative_to(ROOT)}")
            continue

        text = path.read_text(encoding="utf-8")
        lower = text.lower()
        bib = bib_path.read_text(encoding="utf-8")
        hashes[str(path.relative_to(ROOT))] = sha256(path)

        byte_count = len(text.encode("utf-8"))
        line_count = text.count("\n") + 1
        theorem_count = len(THEOREM_RE.findall(text))
        section_count = len(SECTION_RE.findall(text))

        if byte_count < min_bytes:
            errors.append(
                f"{name}: appendix too short ({byte_count} < {min_bytes} bytes)"
            )
        if line_count < 180:
            errors.append(f"{name}: appendix too short ({line_count} lines)")
        if theorem_count < 4:
            errors.append(f"{name}: too few theorem environments ({theorem_count})")
        if section_count < 4:
            errors.append(f"{name}: too few sections ({section_count})")

        for token in (
            "\\documentclass",
            "\\maketitle",
            "\\bibliography{references}",
            "\\end{document}",
        ):
            if token not in text:
                errors.append(f"{name}: missing document token {token!r}")

        labels = LABEL_RE.findall(text)
        label_set = set(labels)
        if len(labels) != len(label_set):
            duplicates = sorted({x for x in labels if labels.count(x) > 1})
            errors.append(f"{name}: duplicate labels {duplicates}")
        missing_anchors = anchors - label_set
        if missing_anchors:
            errors.append(f"{name}: missing anchors {sorted(missing_anchors)}")

        refs = split_keys(REF_RE.findall(text))
        unresolved_refs = refs - label_set
        if unresolved_refs:
            errors.append(f"{name}: unresolved internal refs {sorted(unresolved_refs)}")

        cite_keys = split_keys(CITE_RE.findall(text))
        bib_keys = set(BIB_RE.findall(bib))
        unresolved_cites = cite_keys - bib_keys
        if unresolved_cites:
            errors.append(f"{name}: unresolved citations {sorted(unresolved_cites)}")

        begins = BEGIN_RE.findall(text)
        ends = END_RE.findall(text)
        for env in set(begins) | set(ends):
            if begins.count(env) != ends.count(env):
                errors.append(
                    f"{name}: unbalanced {env}: "
                    f"{begins.count(env)} begin / {ends.count(env)} end"
                )

        for token in FORBIDDEN:
            if token.lower() in lower:
                errors.append(f"{name}: forbidden marker {token!r}")

        if not cite_keys:
            warnings.append(f"{name}: appendix has no explicit citations")

        results[name] = {
            "path": str(path.relative_to(ROOT)),
            "bytes": byte_count,
            "lines": line_count,
            "sections": section_count,
            "theorem_environments": theorem_count,
            "labels": len(label_set),
            "references": len(refs),
            "citation_keys": len(cite_keys),
        }

    output = {
        "schema": "THETA_REFEREE_APPENDICES_V4_VERIFY",
        "status": "PASS" if not errors else "FAIL",
        "appendix_count": len(APPENDICES),
        "appendices": results,
        "errors": errors,
        "warnings": warnings,
        "sha256": dict(sorted(hashes.items())),
        "latex_compilation_checked": False,
        "analytical_correctness_verified": False,
        "external_review_replaced": False,
    }
    print(json.dumps(output, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if not errors else 1


if __name__ == "__main__":
    sys.exit(main())
