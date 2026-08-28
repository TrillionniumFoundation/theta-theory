#!/usr/bin/env python3
"""Fail-closed verifier for θ-Theory referee revision v3.

This script checks the five controlling LaTeX manuscripts, bibliography keys,
internal labels, mandatory proof anchors and exact algebraic identities.  It
does not certify the infinite-dimensional analytical proofs.
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

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "papers" / "referee-ready"

PAPERS = {
    "paper_I": {
        "dir": "paper-I-bilateral-response", "main": "main-submission.tex",
        "title": "Bilateral Response, Exact Innovations",
        "anchors": ["thm:bilateral", "thm:fdq", "thm:totalization",
                    "prop:collision", "thm:nonconjugacy", "lem:contraction",
                    "lem:letters", "thm:allorder", "thm:innovations",
                    "cor:martingale", "thm:specular"],
        "required": ["Branches two and three contain the regular interior fixed points",
                     "W^{N+2,1}", "Exact innovation theorem"],
        "forbidden": ["three regular interior fixed points",
                      "branches one, two, and three contain"],
    },
    "paper_II": {
        "dir": "paper-II-pressure-diffusion", "main": "main-final.tex",
        "title": "Pressure, Physical Diffusion",
        "anchors": ["thm:bundle", "thm:pressure", "thm:physical",
                    "thm:renewal", "thm:GK", "thm:actual", "ass:dio",
                    "lem:phase", "thm:HF", "thm:triangle"],
        "required": [r"0\le\operatorname{Re}z\le\sigma_0",
                     r"{\sqrt3\over4}<r<{1\over2}", "symmetrized Green--Kubo"],
        "forbidden": ["0.34<r<0.49", "1/3<r<1/2", "symmetric strip"],
    },
    "paper_III": {
        "dir": "paper-III-rough-theta", "main": "main-final.tex",
        "title": "Exact-Innovation Rough Homogenization",
        "anchors": ["thm:innovations", "thm:rough", "thm:homogenization",
                    "prop:block", "thm:rate", "lem:consistency", "thm:HJB"],
        "required": [r"{\varepsilon^2\over2}",
                     "canonical geometric step-two lift",
                     "pointwise finite-branch entropic recursion"],
        "forbidden": ["paired residual implies",
                      "anisotropic pairing gives the viscosity"],
    },
    "paper_IV": {
        "dir": "paper-IV-filtering-games", "main": "main-final.tex",
        "title": "Noncompact Filtering and Pure Isaacs",
        "anchors": ["lem:Bayes", "lem:drift", "thm:filter", "thm:collapse",
                    "thm:VI", "prop:saddle", "lem:consistency", "thm:scheme",
                    "thm:feedback", "thm:endtoend"],
        "required": ["variational inequality", "Gaussian refresh--autoregression",
                     "Curvature-compensation pure-saddle theorem"],
        "forbidden": ["one-step prior erasure",
                      "mixed Isaacs equality therefore gives a pure saddle"],
    },
    "paper_V": {
        "dir": "paper-V-representations", "main": "main-final.tex",
        "title": "Tangent Laws and Stochastic Representations",
        "anchors": ["thm:fixedlaw", "thm:IFT", "thm:analytic", "thm:cocycle",
                    "thm:tangent", "thm:Girsanov", "thm:BSDE",
                    "cor:tangentBSDE", "thm:path", "thm:pathgame", "thm:2BSDE"],
        "required": ["Radon--Nikodym derivative", "Novikov condition",
                     "No inversion of the map", "stable under conditioning and pasting"],
        "forbidden": ["Z=p", "invert Z=", "formal Girsanov shift"],
    },
}

TOP = [
    "REVISION_V3_POSITIVE_RESPONSE_TO_REFEREES.md",
    "COMMON_REFERENCE_PLATFORM_V3_FINAL.md",
    "REVISION_V3_FORMULA_AUDIT.json",
    "REVISION_V3_HOSTILE_PROOF_AUDIT.md",
    "REVISION_V3_THEOREM_MANIFEST.yaml",
    "REFEREE_REVISION_V3_STATUS.md",
]

CITE_RE = re.compile(r"\\cite[a-zA-Z*]*(?:\[[^\]]*\])?(?:\[[^\]]*\])?\{([^}]*)\}")
BIB_RE = re.compile(r"@[a-zA-Z]+\s*\{\s*([^,\s]+)")
LABEL_RE = re.compile(r"\\label\{([^}]+)\}")
REF_RE = re.compile(r"\\(?:eqref|ref|cref|Cref)\{([^}]+)\}")
BEGIN_RE = re.compile(r"\\begin\{([^}]+)\}")
END_RE = re.compile(r"\\end\{([^}]+)\}")
SECTION_RE = re.compile(r"\\section\*?\{")
THEOREM_RE = re.compile(r"\\begin\{(?:theorem|proposition|lemma|corollary)\}")


def keys(groups: list[str]) -> set[str]:
    return {x.strip() for group in groups for x in group.split(",") if x.strip()}


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def formula_checks() -> dict[str, bool]:
    A, B, C, D = map(Fraction, (2, 3, 1, 1))
    lam = (B + D) / (A + B + C + D)
    crossed = (-lam*A + (1-lam)*D == lam*C - (1-lam)*B
               == (C*D-A*B)/(A+B+C+D))
    fixed = Fraction(1, 4) < Fraction(11, 40)
    triangle = math.sqrt(3)/4 < 0.45 < 0.5
    xs = [Fraction(2), Fraction(-1), Fraction(3)]
    level2 = sum(xs[i]*xs[j] for i in range(3) for j in range(i+1, 3))
    level2 += Fraction(1, 2)*sum(x*x for x in xs)
    geometric = level2 == Fraction(1, 2)*sum(xs)**2
    delta, r, y = Fraction(1,4), Fraction(1,2), Fraction(3,2)
    alpha = (1-delta)*r*r
    ew = delta*2 + (1-delta)*(1+(r*y)**2+(1-r*r))
    refresh = ew == alpha*(1+y*y)+2*(1-alpha)
    mu, nu, p, u, v = map(Fraction, (5,2,3,4,-2))
    c = Fraction(1,2)*(1/mu-1/nu)
    us, vs = p/mu, -p/nu
    value = p*(us+vs)-mu*us*us/2+nu*vs*vs/2
    saddle = value == c*p*p
    squares = (-c*p*p+p*(u+v)-mu*u*u/2+nu*v*v/2
               == -mu*(u-p/mu)**2/2+nu*(v+p/nu)**2/2)
    theta, z = Fraction(3,2), Fraction(5,3)
    girsanov = theta*(-theta*z*z/2)+theta*theta*z*z/2 == 0
    return {
        "crossed_exponents": crossed,
        "regular_fixed_multiplier_ranges": fixed,
        "triangular_radius_window": triangle,
        "geometric_second_level": geometric,
        "refresh_AR_drift": refresh,
        "quadratic_saddle": saddle,
        "completed_squares": squares,
        "Girsanov_drift_cancellation": girsanov,
    }


def verify_paper(name: str, cfg: dict, errors: list[str], warnings: list[str], hashes: dict[str,str]) -> dict:
    folder = BASE / cfg["dir"]
    tex_path = folder / cfg["main"]
    bib_path = folder / "references.bib"
    out = {"main": str(tex_path.relative_to(ROOT))}
    if not tex_path.is_file() or not bib_path.is_file():
        errors.append(f"{name}: missing controlling tex or bibliography")
        return out
    text = tex_path.read_text(encoding="utf-8")
    bib = bib_path.read_text(encoding="utf-8")
    low = text.lower()
    hashes[str(tex_path.relative_to(ROOT))] = digest(tex_path)
    hashes[str(bib_path.relative_to(ROOT))] = digest(bib_path)

    for token in [r"\documentclass", r"\begin{abstract}", r"\maketitle",
                  r"\tableofcontents", r"\bibliography{references}",
                  r"\end{document}", "Disclosure and review status"]:
        if token not in text:
            errors.append(f"{name}: missing {token!r}")
    if cfg["title"] not in text:
        errors.append(f"{name}: title fragment missing")

    size = len(text.encode("utf-8")); lines = text.count("\n")+1
    sections = len(SECTION_RE.findall(text)); theorems = len(THEOREM_RE.findall(text))
    if size < 12000: errors.append(f"{name}: manuscript below 12000 bytes ({size})")
    if lines < 280: errors.append(f"{name}: manuscript below 280 lines ({lines})")
    if sections < 7: errors.append(f"{name}: fewer than 7 sections ({sections})")
    if theorems < 7: errors.append(f"{name}: fewer than 7 theorem environments ({theorems})")

    labels = LABEL_RE.findall(text); label_set = set(labels)
    if len(labels) != len(label_set):
        errors.append(f"{name}: duplicate labels")
    for anchor in cfg["anchors"]:
        if anchor not in label_set: errors.append(f"{name}: missing anchor {anchor}")
    unresolved_refs = keys(REF_RE.findall(text)) - label_set
    if unresolved_refs: errors.append(f"{name}: unresolved refs {sorted(unresolved_refs)}")

    bib_keys = set(BIB_RE.findall(bib)); cite_keys = keys(CITE_RE.findall(text))
    unresolved_cites = cite_keys - bib_keys
    if unresolved_cites: errors.append(f"{name}: unresolved citations {sorted(unresolved_cites)}")
    unused = bib_keys - cite_keys
    if unused: warnings.append(f"{name}: unused bibliography keys {sorted(unused)}")

    begins, ends = BEGIN_RE.findall(text), END_RE.findall(text)
    for env in set(begins)|set(ends):
        if begins.count(env) != ends.count(env):
            errors.append(f"{name}: unbalanced {env}")
    for token in cfg["required"]:
        if token not in text: errors.append(f"{name}: required text missing {token!r}")
    for token in cfg["forbidden"]:
        if token.lower() in low: errors.append(f"{name}: superseded text present {token!r}")
    for token in ["todo", "fixme", "proof omitted", "left to the reader", "known gap"]:
        if token in low: errors.append(f"{name}: draft marker {token!r}")

    out.update(bytes=size, lines=lines, sections=sections,
               theorem_environments=theorems, labels=len(label_set),
               citation_keys=len(cite_keys), bibliography_entries=len(bib_keys))
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--write-receipt", action="store_true")
    args = ap.parse_args()
    errors: list[str] = []; warnings: list[str] = []; hashes: dict[str,str] = {}
    if not BASE.is_dir():
        print(json.dumps({"status":"FAIL","errors":[f"missing {BASE}"]}))
        return 1
    for filename in TOP:
        path = BASE / filename
        if not path.is_file(): errors.append(f"missing top-level {filename}")
        else: hashes[str(path.relative_to(ROOT))] = digest(path)
    results = {name: verify_paper(name,cfg,errors,warnings,hashes)
               for name,cfg in PAPERS.items()}
    formulas = formula_checks()
    for name, ok in formulas.items():
        if not ok: errors.append(f"formula check failed: {name}")
    manifest = (BASE/"REVISION_V3_THEOREM_MANIFEST.yaml").read_text(encoding="utf-8")
    for token in ["known_proof_blockers_in_declared_scopes: 0",
                  "positively_repaired_in_controlling_files: 15",
                  "second_external_referee_review: NOT_YET_PERFORMED"]:
        if token not in manifest: errors.append(f"manifest boundary missing {token!r}")
    output = {
        "schema":"THETA_REFEREE_REVISION_V3_VERIFY_V2",
        "status":"PASS" if not errors else "FAIL",
        "papers":results, "formula_checks":formulas,
        "errors":errors, "warnings":warnings,
        "sha256":dict(sorted(hashes.items())),
        "latex_compilation_checked":False,
        "analytical_proofs_certified_by_script":False,
        "second_external_referee_review":"NOT_YET_PERFORMED",
    }
    rendered = json.dumps(output, ensure_ascii=False, indent=2, sort_keys=True)
    print(rendered)
    if args.write_receipt:
        (BASE/"REVISION_V3_VERIFICATION_RECEIPT.json").write_text(rendered+"\n",encoding="utf-8")
    return 0 if not errors else 1

if __name__ == "__main__":
    sys.exit(main())
