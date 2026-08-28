#!/usr/bin/env python3
"""Structural verifier for the five referee-ready θ-Theory manuscripts.

The verifier checks repository structure, manuscript size and anchors,
bibliography/citation consistency, theorem-label references, companion-paper
dependency direction, and forbidden internal workflow language.  It does not
verify mathematical correctness or replace external refereeing.
"""

from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "papers" / "referee-ready"

PAPERS = {
    "paper_I": {
        "folder": "paper-I-bilateral-response",
        "title": "Bilateral Graph-Current Mixing",
        "companion": set(),
        "anchors": {
            "thm:bilateral",
            "thm:fdq",
            "thm:u3",
            "thm:fourbranch",
            "thm:sinai-u3",
            "thm:maximality",
        },
    },
    "paper_II": {
        "folder": "paper-II-pressure-diffusion",
        "title": "Pressure, Suspension Resolvents",
        "companion": {"QiResponse"},
        "anchors": {
            "thm:stabilization",
            "thm:pressure",
            "thm:physical",
            "thm:suspension",
            "thm:covariance",
            "thm:uniform-bdl",
            "thm:similarity-bdl",
            "thm:radial-hf",
        },
    },
    "paper_III": {
        "folder": "paper-III-rough-theta",
        "title": "Doob-Selected Rough Homogenization",
        "companion": {"QiPressure"},
        "anchors": {
            "thm:frozen-WIP",
            "prop:diagonal",
            "thm:sharp-rate",
            "thm:nonautonomous",
            "thm:actual-K2",
            "thm:HJB",
            "thm:theta",
        },
    },
    "paper_IV": {
        "folder": "paper-IV-filtering-games",
        "title": "Filtering and Isaacs Limits",
        "companion": {"QiRough"},
        "anchors": {
            "thm:filter",
            "thm:initial-collapse",
            "thm:weighted-filter",
            "thm:sequential",
            "thm:mixed-limit",
            "thm:pure-iff",
            "thm:strong-saddle",
            "thm:actual-game",
            "thm:gaussian-filter",
        },
    },
    "paper_V": {
        "folder": "paper-V-representations",
        "title": "Representation Theory for Theta-Expectations",
        "companion": {"QiGames"},
        "anchors": {
            "thm:single-law",
            "thm:calibration",
            "thm:FBSDE",
            "thm:second-order-rule",
            "thm:path-game",
            "thm:quadratic-BSDE",
            "thm:G-PPDE",
            "thm:2BSDE",
            "thm:hierarchy",
        },
    },
}

REQUIRED_FILES = {"main.tex", "references.bib", "README.md", "REFEREE_GUIDE.md"}
TOP_REQUIRED = {"README.md", "SERIES_REFEREE_GUIDE.md", "SERIES_MANIFEST.yaml"}
MIN_MAIN_BYTES = 25000
MIN_SECTIONS = 8
MIN_THEOREM_ENVIRONMENTS = 8

FORBIDDEN_MAIN_PATTERNS = {
    r"LATEST[- ]WINS",
    r"BLOCKER[_ -]CLOSURE",
    r"FormalCredit",
    r"P[1-5]-[A-Z]",
    r"internal proof DAG",
    r"verification receipt",
}

CITE_RE = re.compile(
    r"\\cite[a-zA-Z*]*(?:\[[^\]]*\])?(?:\[[^\]]*\])?\{([^}]*)\}"
)
BIB_RE = re.compile(r"@[a-zA-Z]+\s*\{\s*([^,\s]+)")
LABEL_RE = re.compile(r"\\label\{([^}]+)\}")
REF_RE = re.compile(r"\\(?:eqref|ref|cref|Cref)\{([^}]+)\}")
SECTION_RE = re.compile(r"\\section\*?\{")
THEOREM_RE = re.compile(
    r"\\begin\{(?:theorem|proposition|lemma|corollary|claim)\}"
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def split_keys(groups: list[str]) -> set[str]:
    out: set[str] = set()
    for group in groups:
        out.update(item.strip() for item in group.split(",") if item.strip())
    return out


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


def main() -> int:
    errors: list[str] = []
    warnings: list[str] = []
    hashes: dict[str, str] = {}
    paper_results: dict[str, dict[str, object]] = {}

    if not BASE.is_dir():
        print(json.dumps({"status": "FAIL", "error": f"missing {BASE}"}))
        return 1

    for name in TOP_REQUIRED:
        path = BASE / name
        if not path.is_file():
            fail(errors, f"missing top-level file: {name}")
        else:
            hashes[str(path.relative_to(ROOT))] = sha256(path)

    all_labels: dict[str, str] = {}

    for paper, cfg in PAPERS.items():
        folder = BASE / str(cfg["folder"])
        result: dict[str, object] = {"folder": str(folder.relative_to(ROOT))}
        paper_results[paper] = result

        if not folder.is_dir():
            fail(errors, f"missing paper folder: {folder.relative_to(ROOT)}")
            continue

        present = {p.name for p in folder.iterdir() if p.is_file()}
        missing = REQUIRED_FILES - present
        if missing:
            fail(errors, f"{paper}: missing files {sorted(missing)}")
            continue

        for name in REQUIRED_FILES:
            path = folder / name
            hashes[str(path.relative_to(ROOT))] = sha256(path)

        main_path = folder / "main.tex"
        bib_path = folder / "references.bib"
        guide_path = folder / "REFEREE_GUIDE.md"
        readme_path = folder / "README.md"

        text = main_path.read_text(encoding="utf-8")
        bib = bib_path.read_text(encoding="utf-8")
        guide = guide_path.read_text(encoding="utf-8")
        readme = readme_path.read_text(encoding="utf-8")

        byte_count = len(text.encode("utf-8"))
        section_count = len(SECTION_RE.findall(text))
        theorem_count = len(THEOREM_RE.findall(text))
        result.update(
            main_bytes=byte_count,
            section_count=section_count,
            theorem_environment_count=theorem_count,
        )

        if byte_count < MIN_MAIN_BYTES:
            fail(errors, f"{paper}: manuscript is too short ({byte_count} bytes)")
        if section_count < MIN_SECTIONS:
            fail(errors, f"{paper}: too few sections ({section_count})")
        if theorem_count < MIN_THEOREM_ENVIRONMENTS:
            fail(errors, f"{paper}: too few theorem environments ({theorem_count})")

        if str(cfg["title"]) not in text:
            fail(errors, f"{paper}: expected title fragment missing")
        for anchor in set(cfg["anchors"]):
            if f"\\label{{{anchor}}}" not in text:
                fail(errors, f"{paper}: missing theorem anchor {anchor}")

        for required in (
            "\\begin{abstract}",
            "\\maketitle",
            "\\tableofcontents",
            "\\bibliography{references}",
            "Acknowledgements and disclosure",
            "\\end{document}",
        ):
            if required not in text:
                fail(errors, f"{paper}: missing manuscript anchor {required!r}")

        for pattern in FORBIDDEN_MAIN_PATTERNS:
            if re.search(pattern, text, flags=re.IGNORECASE):
                fail(errors, f"{paper}: forbidden internal language matching {pattern!r}")

        bib_keys = set(BIB_RE.findall(bib))
        cite_keys = split_keys(CITE_RE.findall(text))
        missing_bib = cite_keys - bib_keys
        if missing_bib:
            fail(errors, f"{paper}: unresolved bibliography keys {sorted(missing_bib)}")
        unused_bib = bib_keys - cite_keys
        if unused_bib:
            warnings.append(f"{paper}: unused bibliography keys {sorted(unused_bib)}")

        companion_keys = {key for key in cite_keys if key.startswith("Qi")}
        if companion_keys != set(cfg["companion"]):
            fail(
                errors,
                f"{paper}: companion citations {sorted(companion_keys)} != "
                f"expected {sorted(set(cfg['companion']))}",
            )

        labels = LABEL_RE.findall(text)
        if len(labels) != len(set(labels)):
            duplicates = sorted({x for x in labels if labels.count(x) > 1})
            fail(errors, f"{paper}: duplicate labels {duplicates}")
        for label in labels:
            if label in all_labels:
                warnings.append(
                    f"cross-paper label reuse {label}: {all_labels[label]} and {paper}"
                )
            else:
                all_labels[label] = paper

        refs = split_keys(REF_RE.findall(text))
        unresolved_refs = refs - set(labels)
        if unresolved_refs:
            fail(errors, f"{paper}: unresolved theorem/equation refs {sorted(unresolved_refs)}")

        if "pdflatex main" not in readme or "bibtex main" not in readme:
            fail(errors, f"{paper}: incomplete build instructions")
        if "Suggested audit order" not in guide:
            fail(errors, f"{paper}: referee guide lacks audit order")
        if "Permanent scope" not in guide:
            fail(errors, f"{paper}: referee guide lacks scope boundary")

        result.update(
            bibliography_entries=len(bib_keys),
            citation_keys=len(cite_keys),
            labels=len(labels),
            references=len(refs),
        )

    manifest_path = BASE / "SERIES_MANIFEST.yaml"
    if manifest_path.is_file():
        manifest = manifest_path.read_text(encoding="utf-8")
        for required in (
            "folder_count: 5",
            "standalone_projects: 5",
            "internal_dependency_cycles: 0",
            "external_peer_review: NOT_PERFORMED",
            "formal_credit: 0",
        ):
            if required not in manifest:
                fail(errors, f"manifest boundary missing: {required}")

    output = {
        "schema": "THETA_REFEREE_MANUSCRIPT_VERIFY_V1",
        "status": "PASS" if not errors else "FAIL",
        "paper_count": len(PAPERS),
        "papers": paper_results,
        "errors": errors,
        "warnings": warnings,
        "sha256": dict(sorted(hashes.items())),
        "latex_compilation_checked": False,
        "mathematical_correctness_verified": False,
        "external_peer_review": "NOT_PERFORMED",
        "formal_credit": 0,
    }
    print(json.dumps(output, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if not errors else 1


if __name__ == "__main__":
    sys.exit(main())
