#!/usr/bin/env python3
"""Fail-closed hygiene checks for the active θ-Theory manuscript tree."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT / "papers" / "referee-ready"

ARCHIVED_PATHS = [
    "canonical",
    "cm2",
    "evidence",
    "provenance",
    "papers/expectations-monograph",
    "papers/theta-program",
]

PAPER_DIRS = [
    "paper-I-bilateral-response",
    "paper-II-pressure-diffusion",
    "paper-III-rough-theta",
    "paper-IV-filtering-games",
    "paper-V-representations",
]

VERSIONED_SOURCE = re.compile(
    r"^(main-(?:final|submission|round\d+|v\d+)\.tex|references-round\d+\.bib)$"
)

FORBIDDEN_TOP_LEVEL = {
    "COMMON_REFERENCE_PLATFORM_V3.md",
    "COMMON_REFERENCE_PLATFORM_V3_FINAL.md",
    "MANUSCRIPT_FORMULA_AUDIT.json",
    "Makefile.v3",
    "REFEREE_BUILD_RECEIPT.json",
    "REFEREE_MANUSCRIPT_STATUS.md",
    "REFEREE_REVISION_V3_STATUS.md",
    "REFEREE_REVISION_V4_FINAL_STATUS.md",
    "REFEREE_REVISION_V4_STATUS.md",
    "REVISION_V2_RESPONSE_TO_REFEREES.md",
    "REVISION_V3_FORMULA_AUDIT.json",
    "REVISION_V3_HOSTILE_PROOF_AUDIT.md",
    "REVISION_V3_POSITIVE_RESPONSE_TO_REFEREES.md",
    "REVISION_V3_THEOREM_MANIFEST.yaml",
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"FAIL_CLOSED: {message}")


def main() -> int:
    require((ROOT / "ARCHIVE_POINTER.md").is_file(), "missing archive pointer")
    require((ROOT / "GOVERNANCE.md").is_file(), "missing governance policy")
    require((ROOT / "platforms" / "platform-registry.yaml").is_file(), "missing platform registry")

    for rel in ARCHIVED_PATHS:
        require(not (ROOT / rel).exists(), f"archived path remains active: {rel}")

    legacy_top = sorted(name for name in FORBIDDEN_TOP_LEVEL if (PAPERS / name).exists())
    require(not legacy_top, f"legacy top-level review assets remain active: {legacy_top}")

    for name in PAPER_DIRS:
        folder = PAPERS / name
        require(folder.is_dir(), f"missing paper directory: {name}")
        require((folder / "main.tex").is_file(), f"missing {name}/main.tex")
        require((folder / "references.bib").is_file(), f"missing {name}/references.bib")
        offenders = sorted(p.name for p in folder.iterdir() if VERSIONED_SOURCE.match(p.name))
        require(not offenders, f"versioned sources in {name}: {offenders}")

    result = {
        "status": "PASS_ACTIVE_TREE_GOVERNANCE",
        "paper_count": len(PAPER_DIRS),
        "controlling_main_count": sum((PAPERS / p / "main.tex").is_file() for p in PAPER_DIRS),
        "controlling_bibliography_count": sum(
            (PAPERS / p / "references.bib").is_file() for p in PAPER_DIRS
        ),
        "archived_paths_absent": True,
        "legacy_top_level_assets_absent": True,
        "versioned_sources_absent": True,
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
