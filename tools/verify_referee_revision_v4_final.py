#!/usr/bin/env python3
"""Final structural and finite-formula verifier for θ-Theory revision v4.

Checks the five promoted controlling manuscripts, invoked round-four
bibliographies, mirror bibliography equality, theorem labels, internal
references, citation keys, forbidden superseded shortcuts, exact finite
identities, and the six normative appendices through the companion checker.

This script does not certify infinite-dimensional analysis or replace external
formal review.
"""

from __future__ import annotations

import hashlib
import json
import math
import re
import subprocess
import sys
from fractions import Fraction
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "papers" / "referee-ready"

PAPERS: dict[str, dict[str, Any]] = {
    "paper_I": {
        "folder": "paper-I-bilateral-response",
        "title": "Bilateral Response, Symbolic Desingularization",
        "anchors": {
            "thm:crossed", "thm:fdq", "thm:totalization",
            "prop:symplectic", "lem:contraction", "lem:letters",
            "thm:allorder", "thm:nonconjugacy", "thm:correlation",
            "thm:innovations", "thm:symbolic", "thm:open-billiard",
            "cor:specular",
        },
        "required": {
            "independently prescribed",
            "Symbolic desingularization",
            "Exact predictable innovations",
            "W^{r+N,1}",
            "not time-preservingly",
        },
    },
    "paper_II": {
        "folder": "paper-II-pressure-diffusion",
        "title": "Pressure, Physical Diffusion",
        "anchors": {
            "thm:stabilization", "thm:pressure", "thm:physical",
            "thm:renewal", "thm:GK", "cor:sqrt", "thm:actual",
            "lem:quotient", "ass:diophantine", "lem:phase",
            "thm:full-frequency", "ass:shear", "prop:disk-shear",
            "thm:open-HF", "thm:triangle", "thm:lift",
        },
        "required": {
            "symmetrized Green--Kubo",
            "Diophantine roof vector",
            "Full-frequency moving-family resolvent",
            "Temporal shear",
            "{\\sqrt3\\over4}<r<{1\\over2}",
        },
    },
    "paper_III": {
        "folder": "paper-III-rough-theta",
        "title": "Exact-Innovation Rough Homogenization",
        "anchors": {
            "thm:innovations", "thm:rough", "thm:homogenization",
            "prop:block", "thm:rate", "lem:consistency", "thm:HJB",
            "thm:controlled", "def:theta-independence",
            "thm:theta-independence",
        },
        "required": {
            "canonical geometric lift",
            "{1\\over2}\\sum_{i<t/\\varepsilon^2}",
            "microscopic entropic collision recursion",
            "Forward theta-independence",
            "pointwise",
        },
    },
    "paper_IV": {
        "folder": "paper-IV-filtering-games",
        "title": "Noncompact Filtering, Curvature-Compensated",
        "anchors": {
            "lem:Bayes", "lem:refresh", "thm:filter", "thm:collapse",
            "thm:curvature", "prop:saddle", "lem:consistency",
            "thm:scheme", "thm:feedback", "thm:endtoend",
        },
        "required": {
            "refresh--autoregressive",
            "variational inclusion",
            "mixed Hessian terms cancel",
            "lower and upper collision-game schemes",
            "completion-of-squares",
        },
    },
    "paper_V": {
        "folder": "paper-V-representations",
        "title": "Tangent-Law Characterization",
        "anchors": {
            "thm:fixed-law", "thm:IFT", "thm:analytic", "thm:cocycle",
            "thm:characterization", "thm:dynamic-characterization",
            "thm:micro-tangent", "thm:tangent-PDE", "thm:Girsanov",
            "thm:BSDE", "cor:tangent-BSDE", "thm:path",
            "thm:path-game", "thm:2BSDE",
        },
        "required": {
            "covariance curvature",
            "Microscopic-to-continuum tangent convergence",
            "Radon--Nikodym",
            "Novikov",
            "No inversion",
            "stable under conditioning and pasting",
        },
    },
}

TOP_REQUIRED = {
    "REVISION_V4_RESPONSE_TO_REFEREES.md",
    "COMMON_ACTUAL_PLATFORM_V4.md",
    "REVISION_V4_THEOREM_MANIFEST.yaml",
    "REVISION_V4_APPENDIX_THEOREM_MANIFEST.yaml",
    "TECHNICAL_APPENDICES_V4.md",
    "REVISION_V4_FORMULA_AUDIT.json",
    "REVISION_V4_HOSTILE_PROOF_AUDIT.md",
    "REFEREE_REVISION_V4_STATUS.md",
    "REVISION_V4_EXECUTION_RECEIPT.json",
}

FORBIDDEN = {
    "viscosity-duality solution",
    "ass:paper1_response_input",
    "A1--A5", "S1--S3",
    "FACE_TIME_CM2", "ACTUAL_SLOPE_BRIDGE",
    "proof omitted", "left to the reader",
    "TODO", "FIXME", "TBD", "\\nrac",
}

CITE_RE = re.compile(
    r"\\cite[a-zA-Z*]*(?:\[[^\]]*\])?(?:\[[^\]]*\])?\{([^}]*)\}"
)
BIB_RE = re.compile(r"@[a-zA-Z]+\s*\{\s*([^,\s]+)")
LABEL_RE = re.compile(r"\\label\{([^}]+)\}")
REF_RE = re.compile(r"\\(?:eqref|ref|cref|Cref)\{([^}]+)\}")
SECTION_RE = re.compile(r"\\section\*?\{")
THEOREM_RE = re.compile(r"\\begin\{(?:theorem|proposition|lemma|corollary)\}")
BEGIN_RE = re.compile(r"\\begin\{([^}]+)\}")
END_RE = re.compile(r"\\end\{([^}]+)\}")
BIB_COMMAND_RE = re.compile(r"\\bibliography\{([^}]+)\}")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def split_keys(groups: list[str]) -> set[str]:
    keys: set[str] = set()
    for group in groups:
        keys.update(item.strip() for item in group.split(",") if item.strip())
    return keys


def formula_checks() -> dict[str, bool]:
    A, B, C, D = Fraction(2), Fraction(3), Fraction(1), Fraction(1)
    lam = (B + D) / (A + B + C + D)
    crossed = (
        -lam * A + (1 - lam) * D
        == lam * C - (1 - lam) * B
        == (C * D - A * B) / (A + B + C + D)
    )

    a0, a1 = Fraction(-1, 40), Fraction(1, 40)
    w2 = (Fraction(1, 5) + 2 * a0, Fraction(1, 5) + 2 * a1)
    w3 = (Fraction(3, 10) - a1, Fraction(3, 10) - a0)
    multipliers = (1 / w3[0]) < (1 / w2[1])

    xs = [Fraction(2), Fraction(-1), Fraction(3)]
    second = sum(
        xs[i] * xs[j]
        for i in range(len(xs))
        for j in range(i + 1, len(xs))
    ) + Fraction(1, 2) * sum(x * x for x in xs)
    geometric = second == Fraction(1, 2) * sum(xs) ** 2

    delta, r, y = Fraction(1, 4), Fraction(1, 2), Fraction(3, 2)
    alpha = (1 - delta) * r * r
    refresh_direct = delta * 2 + (1 - delta) * (
        1 + r * r * y * y + (1 - r * r)
    )
    refresh = refresh_direct == alpha * (1 + y * y) + 2 * (1 - alpha)

    mu, nu, p = Fraction(5), Fraction(2), Fraction(3)
    u, v = Fraction(4), Fraction(-2)
    c = Fraction(1, 2) * (1 / mu - 1 / nu)
    us, vs = p / mu, -p / nu
    saddle = (
        p * (us + vs) - mu * us * us / 2 + nu * vs * vs / 2
        == c * p * p
    )
    squares = (
        -c * p * p + p * (u + v) - mu * u * u / 2 + nu * v * v / 2
        == -mu * (u - p / mu) ** 2 / 2
        + nu * (v + p / nu) ** 2 / 2
    )

    weights = [0.1, 0.2, 0.3, 0.4]
    phases = [0.1, 1.2, -0.7, 2.0]
    z = sum(
        w * complex(math.cos(t), -math.sin(t))
        for w, t in zip(weights, phases)
    )
    phase_identity = abs(
        1 - abs(z) ** 2
        - 2 * sum(
            weights[i] * weights[j] * (1 - math.cos(phases[i] - phases[j]))
            for i in range(4)
            for j in range(i + 1, 4)
        )
    ) < 1e-12

    triangle = math.sqrt(3.0) / 4.0 < 0.45 < 0.5

    theta, zeta = Fraction(3, 2), Fraction(5, 3)
    girsanov = (
        theta * (-theta * zeta * zeta / 2)
        + theta * theta * zeta * zeta / 2
        == 0
    )

    q = [0.2, 0.3, 0.5]
    phi = [-0.4, 0.2, 1.1]
    f = [1.2, -0.5, 0.7]
    t, th, eps = 0.7, 1.5, 1e-6

    def tilted(time: float) -> list[float]:
        raw = [qi * math.exp(th * time * pi) for qi, pi in zip(q, phi)]
        total = sum(raw)
        return [x / total for x in raw]

    qt = tilted(t)
    mean_f = sum(x * y0 for x, y0 in zip(qt, f))
    mean_phi = sum(x * y0 for x, y0 in zip(qt, phi))
    cov = (
        sum(x * p0 * f0 for x, p0, f0 in zip(qt, phi, f))
        - mean_phi * mean_f
    )
    finite_derivative = (
        sum(x * y0 for x, y0 in zip(tilted(t + eps), f))
        - sum(x * y0 for x, y0 in zip(tilted(t - eps), f))
    ) / (2 * eps)
    replicator = abs(finite_derivative - th * cov) < 1e-8

    return {
        "bilateral_crossed_exponents": crossed,
        "fixed_multiplier_ranges_disjoint": multipliers,
        "geometric_second_level_diagonal": geometric,
        "refresh_AR_Lyapunov": refresh,
        "quadratic_saddle_value": saddle,
        "completed_squares": squares,
        "weighted_phase_identity": phase_identity,
        "triangular_radius_window": triangle,
        "Girsanov_density_drift": girsanov,
        "tangent_replicator_ODE": replicator,
    }


def verify_paper(
    name: str,
    cfg: dict[str, Any],
    errors: list[str],
    warnings: list[str],
    hashes: dict[str, str],
) -> dict[str, Any]:
    folder = BASE / cfg["folder"]
    main = folder / "main.tex"
    round4 = folder / "main-round4.tex"
    mirror_bib = folder / "references.bib"
    invoked_bib = folder / "references-round4.bib"

    for path in (main, round4, mirror_bib, invoked_bib):
        if not path.is_file():
            errors.append(f"{name}: missing {path.relative_to(ROOT)}")
            return {"folder": str(folder.relative_to(ROOT))}
        hashes[str(path.relative_to(ROOT))] = sha256(path)

    if main.read_bytes() != round4.read_bytes():
        errors.append(f"{name}: main.tex is not the promoted round-four source")
    if mirror_bib.read_bytes() != invoked_bib.read_bytes():
        errors.append(f"{name}: bibliography mirror differs from invoked round-four file")

    text = main.read_text(encoding="utf-8")
    lower = text.lower()
    bib_text = invoked_bib.read_text(encoding="utf-8")

    for token in (
        "\\documentclass", "\\begin{abstract}", "\\maketitle",
        "\\tableofcontents", "Disclosure and review status", "\\end{document}",
    ):
        if token not in text:
            errors.append(f"{name}: missing document token {token!r}")

    if cfg["title"] not in text:
        errors.append(f"{name}: controlling title fragment missing")
    for token in cfg["required"]:
        if token not in text:
            errors.append(f"{name}: required proof anchor missing {token!r}")
    for token in FORBIDDEN:
        if token.lower() in lower:
            errors.append(f"{name}: superseded shortcut appears {token!r}")

    byte_count = len(text.encode("utf-8"))
    line_count = text.count("\n") + 1
    sections = len(SECTION_RE.findall(text))
    theorems = len(THEOREM_RE.findall(text))
    if byte_count < 18000 or line_count < 350:
        errors.append(f"{name}: controlling manuscript below size floor")
    if sections < 8 or theorems < 8:
        errors.append(f"{name}: insufficient section/theorem structure")

    labels = LABEL_RE.findall(text)
    label_set = set(labels)
    if len(labels) != len(label_set):
        duplicates = sorted({x for x in labels if labels.count(x) > 1})
        errors.append(f"{name}: duplicate labels {duplicates}")
    missing_anchors = cfg["anchors"] - label_set
    if missing_anchors:
        errors.append(f"{name}: missing theorem anchors {sorted(missing_anchors)}")

    refs = split_keys(REF_RE.findall(text))
    unresolved_refs = refs - label_set
    if unresolved_refs:
        errors.append(f"{name}: unresolved internal refs {sorted(unresolved_refs)}")

    bib_commands = BIB_COMMAND_RE.findall(text)
    if bib_commands != ["references-round4"]:
        errors.append(f"{name}: bibliography command mismatch {bib_commands}")
    bib_keys = set(BIB_RE.findall(bib_text))
    cite_keys = split_keys(CITE_RE.findall(text))
    unresolved_cites = cite_keys - bib_keys
    if unresolved_cites:
        errors.append(f"{name}: unresolved citations {sorted(unresolved_cites)}")
    unused = bib_keys - cite_keys
    if unused:
        warnings.append(f"{name}: unused bibliography keys {sorted(unused)}")

    begins = BEGIN_RE.findall(text)
    ends = END_RE.findall(text)
    for env in set(begins) | set(ends):
        if begins.count(env) != ends.count(env):
            errors.append(
                f"{name}: unbalanced {env}: "
                f"{begins.count(env)} begin / {ends.count(env)} end"
            )

    return {
        "folder": str(folder.relative_to(ROOT)),
        "bytes": byte_count,
        "lines": line_count,
        "sections": sections,
        "theorem_environments": theorems,
        "labels": len(label_set),
        "references": len(refs),
        "citation_keys": len(cite_keys),
        "main_matches_round4": main.read_bytes() == round4.read_bytes(),
        "bibliography_mirror_matches_invoked_file": (
            mirror_bib.read_bytes() == invoked_bib.read_bytes()
        ),
    }


def main() -> int:
    errors: list[str] = []
    warnings: list[str] = []
    hashes: dict[str, str] = {}
    paper_results: dict[str, Any] = {}

    for name in TOP_REQUIRED:
        path = BASE / name
        if not path.is_file():
            errors.append(f"missing top-level revision file {name}")
        else:
            hashes[str(path.relative_to(ROOT))] = sha256(path)

    for name, cfg in PAPERS.items():
        paper_results[name] = verify_paper(name, cfg, errors, warnings, hashes)

    formulas = formula_checks()
    for key, passed in formulas.items():
        if not passed:
            errors.append(f"formula check failed: {key}")

    appendix_checker = ROOT / "tools" / "verify_referee_appendices_v4.py"
    appendix_result: dict[str, Any] = {"executed": False}
    if not appendix_checker.is_file():
        errors.append("missing appendix verifier")
    else:
        proc = subprocess.run(
            [sys.executable, str(appendix_checker)],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        appendix_result = {
            "executed": True,
            "returncode": proc.returncode,
            "stdout": proc.stdout,
            "stderr": proc.stderr,
        }
        if proc.returncode != 0:
            errors.append("appendix verifier failed")

    manifest = BASE / "SERIES_MANIFEST.yaml"
    if manifest.is_file():
        manifest_text = manifest.read_text(encoding="utf-8")
        for token in (
            "normative_technical_appendices: 6",
            "internal_dependency_cycles: 0",
            "internal_unnamed_imports: 0",
            "collision_to_physical_clock_gap: 0",
            "known_internal_referee_objection_gaps: 0",
        ):
            if token not in manifest_text:
                errors.append(f"series manifest boundary missing {token!r}")
    else:
        errors.append("missing SERIES_MANIFEST.yaml")

    output = {
        "schema": "THETA_REFEREE_REVISION_V4_FINAL_VERIFY",
        "status": "PASS" if not errors else "FAIL",
        "papers": paper_results,
        "formula_checks": formulas,
        "appendix_verifier": appendix_result,
        "errors": errors,
        "warnings": warnings,
        "sha256": dict(sorted(hashes.items())),
        "latex_compilation_checked": False,
        "infinite_dimensional_proofs_verified": False,
        "external_second_review": "NOT_YET_PERFORMED",
        "journal_acceptance": "NOT_CLAIMED",
    }

    receipt = BASE / "REVISION_V4_VERIFICATION_RECEIPT.json"
    receipt.write_text(
        json.dumps(output, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(output, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if not errors else 1


if __name__ == "__main__":
    sys.exit(main())
