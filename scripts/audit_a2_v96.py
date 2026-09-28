#!/usr/bin/env python3
"""Exact-checkout source and full-manuscript build audit (not a proof verifier)."""
from __future__ import annotations
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys

BASE = "ebb796e49ca51a62b90d92ec0d09819cfe8d00a4"
PAPER = "papers/A2-v17-boundary-information-coarsening"
MANIFEST = "revisions/a2-v96/SOURCE_MANIFEST.json"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git(root: Path, *args: str) -> str:
    return subprocess.check_output(["git", "-C", str(root), *args], text=True).strip()


def source_graph(read, entry: str) -> set[str]:
    seen: set[str] = set()
    def visit(path: str) -> None:
        if path in seen:
            return
        seen.add(path)
        text = re.sub(r"(?<!\\)%[^\n]*", "", read(path))
        for name in re.findall(r"\\(?:input|include)\s*\{([^}]+)\}", text):
            if "\\" in name or "#" in name:
                raise ValueError(f"Dynamic TeX input needs an explicit audit rule: {name}")
            child = f"{PAPER}/{name}"
            if not child.endswith(".tex"):
                child += ".tex"
            visit(child)
    visit(entry)
    return seen


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--fls", type=Path)
    parser.add_argument("--log", type=Path)
    parser.add_argument("--pdf", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    root = args.root.resolve()
    head = git(root, "rev-parse", "HEAD")
    expected = os.environ.get("GITHUB_SHA")
    if expected and expected != head:
        raise ValueError("Runtime HEAD differs from GITHUB_SHA")
    subprocess.run(["git", "-C", str(root), "merge-base", "--is-ancestor", BASE, head], check=True)
    manifest = json.loads((root / MANIFEST).read_text())
    if manifest["base_commit"] != BASE:
        raise ValueError("Unexpected baseline")
    allowed = set(manifest["new_source_sha256"]) | {MANIFEST}
    changes = []
    for line in git(root, "diff", "--name-status", BASE, head).splitlines():
        status, path = line.split("\t", 1)
        if status != "A" or path not in allowed:
            raise ValueError(f"Unapproved inherited edit or additional path: {line}")
        changes.append(path)
    if set(changes) != allowed:
        raise ValueError("Manifest and committed added-file set differ")
    if git(root, "diff", "HEAD", "--", *sorted(allowed)):
        raise ValueError("Tracked revision sources differ from the committed HEAD")
    for name, value in manifest["new_source_sha256"].items():
        if digest(root / name) != value:
            raise ValueError(f"SHA256 mismatch: {name}")
    old = source_graph(lambda p: git(root, "show", f"{BASE}:{p}"), f"{PAPER}/rigidity_v95.tex")
    new = source_graph(lambda p: (root / p).read_text(), f"{PAPER}/rigidity_v96.tex")
    inherited = old - {f"{PAPER}/rigidity_v95.tex", f"{PAPER}/article/v95/paper.tex"}
    if not inherited <= new:
        raise ValueError(f"Inherited inputs no longer active: {sorted(inherited - new)}")
    for p in inherited:
        base_bytes = subprocess.check_output(["git", "-C", str(root), "show", f"{BASE}:{p}"])
        if (root / p).read_bytes() != base_bytes:
            raise ValueError(f"Inherited mathematical input changed: {p}")
    receipt = dict(schema="a2-v96-audit/1", runtime_head=head, github_sha=expected,
                   base_commit=BASE, added_files=sorted(changes),
                   inherited_inputs=sorted(inherited), active_inputs=sorted(new),
                   source_audit="passed", full_build_audit="not requested",
                   qualification="Source identity and compilation are not mathematical proof certification.")
    supplied = [args.fls, args.log, args.pdf]
    if any(supplied) and not all(supplied):
        raise ValueError("A full build audit requires --fls, --log and --pdf together")
    if all(supplied):
        fls, log, pdf = [p.resolve() for p in supplied]
        text = log.read_text(errors="replace")
        patterns = [r"Overfull \\[hv]box", r"(?:Reference|Citation).*undefined",
                    r"undefined references", r"multiply[ -]defined", r"multiply defined",
                    r"destination with the same identifier", r"^!", r"Emergency stop"]
        for pattern in patterns:
            if re.search(pattern, text, re.I | re.M):
                raise ValueError(f"Full build log failed: {pattern}")
        if "Output written on rigidity_v96.pdf" not in text:
            raise ValueError("Log does not identify the complete entrypoint PDF")
        actual = set()
        for line in fls.read_text().splitlines():
            if line.startswith("INPUT "):
                p = Path(line[6:])
                if not p.is_absolute():
                    p = fls.parent / p
                actual.add(p.resolve())
        missing = {p for p in new if (root / p).resolve() not in actual}
        if missing:
            raise ValueError(f"Compiled input graph is incomplete: {sorted(missing)}")
        if not pdf.read_bytes().startswith(b"%PDF-"):
            raise ValueError("Missing PDF output")
        receipt.update(full_build_audit="passed", pdf_sha256=digest(pdf),
                       log_sha256=digest(log), fls_sha256=digest(fls))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"head": head, "inherited_inputs": len(inherited),
                      "source_audit": "passed", "full_build_audit": receipt["full_build_audit"]}))


if __name__ == "__main__":
    try:
        main()
    except (ValueError, OSError, subprocess.CalledProcessError) as exc:
        print(f"A2 v96 audit failed: {exc}", file=sys.stderr)
        raise SystemExit(1) from exc
