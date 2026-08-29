#!/usr/bin/env python3
"""Fail-closed checks for the active five-paper external-review tree."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAPERS_ROOT = ROOT / "papers"
EXPECTED = {
    "paper-I-geometric-response",
    "paper-II-physical-rough",
    "paper-III-dpp-hjb",
    "paper-IV-filtering-games",
    "paper-V-tangent-laws",
}
ALLOWED_FILES = {
    "main.tex",
    "references.bib",
    "README.md",
    "REFEREE_GUIDE.md",
    "main.pdf",
}
FORBIDDEN_PARTS = (
    "main-v",
    "main-final",
    "main-round",
    "main-submission",
    "references-round",
    "FINAL_STATUS",
    "LATEST_STATUS",
    "REVISION_V2",
    "REVISION_V3",
)
FORBIDDEN_TOP = {"canonical", "cm2", "evidence", "provenance"}
PLATFORM_IDS = {
    "OB3-MG-v1",
    "FB4-EXACT-v1",
    "SL-SIM-v1",
    "AR-FILTER-v1",
    "SV-CONTROL-v1",
}


def fail(msg: str) -> None:
    raise SystemExit(f"FAIL: {msg}")


def bib_keys(text: str) -> set[str]:
    return set(re.findall(r"@\w+\s*\{\s*([^,\s]+)", text))


def cite_keys(text: str) -> set[str]:
    out: set[str] = set()
    for group in re.findall(r"\\cite\w*\{([^}]+)\}", text):
        out.update(k.strip() for k in group.split(",") if k.strip())
    return out


def labels(text: str) -> set[str]:
    return set(re.findall(r"\\label\{([^}]+)\}", text))


def refs(text: str) -> set[str]:
    out: set[str] = set()
    for group in re.findall(r"\\(?:cref|Cref|ref|eqref)\{([^}]+)\}", text):
        out.update(k.strip() for k in group.split(",") if k.strip())
    return out


def main() -> int:
    if not PAPERS_ROOT.is_dir():
        fail("papers directory is missing")

    actual_dirs = {
        p.name for p in PAPERS_ROOT.iterdir()
        if p.is_dir() and not p.name.startswith(".")
    }
    if actual_dirs != EXPECTED:
        fail(f"paper directories mismatch: {sorted(actual_dirs)}")

    for top in FORBIDDEN_TOP:
        if (ROOT / top).exists():
            fail(f"historical top-level tree present: {top}")

    checked = {}
    for name in sorted(EXPECTED):
        folder = PAPERS_ROOT / name
        names = {p.name for p in folder.iterdir() if p.is_file()}
        extra = names - ALLOWED_FILES
        missing = {"main.tex", "references.bib", "README.md", "REFEREE_GUIDE.md"} - names
        if extra:
            fail(f"{name}: unexpected files {sorted(extra)}")
        if missing:
            fail(f"{name}: missing files {sorted(missing)}")

        tex = (folder / "main.tex").read_text(encoding="utf-8")
        bib = (folder / "references.bib").read_text(encoding="utf-8")

        for part in FORBIDDEN_PARTS:
            if part in tex or part in str(folder):
                fail(f"{name}: forbidden historical marker {part}")

        bk = bib_keys(bib)
        ck = cite_keys(tex)
        missing_cites = ck - bk
        if missing_cites:
            fail(f"{name}: missing bibliography keys {sorted(missing_cites)}")

        labs = labels(tex)
        if len(labs) != len(re.findall(r"\\label\{([^}]+)\}", tex)):
            fail(f"{name}: duplicate LaTeX labels")
        missing_refs = refs(tex) - labs
        if missing_refs:
            fail(f"{name}: unresolved internal labels {sorted(missing_refs)}")

        if "\\begin{document}" not in tex or "\\end{document}" not in tex:
            fail(f"{name}: incomplete LaTeX document")
        if "external review" not in tex.lower():
            fail(f"{name}: review-status scope statement missing")

        checked[name] = {
            "citations": len(ck),
            "bibliography_keys": len(bk),
            "labels": len(labs),
            "pdf_present": (folder / "main.pdf").exists(),
        }

    registry = (ROOT / "platforms" / "platform-registry.yaml").read_text(
        encoding="utf-8"
    )
    for platform_id in PLATFORM_IDS:
        if platform_id not in registry:
            fail(f"platform registry missing {platform_id}")

    manifest = (PAPERS_ROOT / "SERIES_MANIFEST.yaml").read_text(encoding="utf-8")
    for name in EXPECTED:
        if name not in manifest:
            fail(f"series manifest missing {name}")
    if "historical_paper_versions: 0" not in manifest:
        fail("manifest does not certify zero historical versions")

    all_paths = [str(p.relative_to(ROOT)) for p in ROOT.rglob("*") if p.is_file()]
    for path in all_paths:
        for part in FORBIDDEN_PARTS:
            if part in path:
                fail(f"forbidden historical path: {path}")

    receipt = {
        "status": "PASS_ACTIVE_EXTERNAL_REVIEW_TREE",
        "paper_count": 5,
        "historical_paper_versions": 0,
        "checked": checked,
        "machine_check_is_peer_review": False,
    }
    out = ROOT / "status" / "ACTIVE_TREE_RECEIPT.json"
    out.write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n",
                   encoding="utf-8")
    print(json.dumps(receipt, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
