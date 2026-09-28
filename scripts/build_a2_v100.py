#!/usr/bin/env python3
"""Build the v100 principal and its complete PDF dependency graph natively.

The archive wraps v99 complete, which wraps earlier complete volumes.
Reading literal TeX input and includepdf edges avoids relying on stale PDFs.
No network download, shell escape, or branch mutation is performed.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAPER = ROOT / 'papers/A2-v17-boundary-information-coarsening'
INPUT = re.compile(r'\\(?:input|include)\s*\{([^{}]+)\}')
PDF = re.compile(r'\\includepdf(?:\[[^\]]*\])?\s*\{([^{}]+)\}')


def text_without_comments(path: Path) -> str:
    return re.sub(r'(?<!\\)%[^\n]*', '', path.read_text(encoding='utf-8'))


def resolve_input(name: str, parent: Path, suffix: str) -> Path:
    name = name.strip()
    if '\\' in name or '#' in name:
        raise ValueError(f'Nonliteral TeX dependency requires explicit review: {name}')
    item = Path(name)
    if not item.suffix:
        item = item.with_suffix(suffix)
    for candidate in (PAPER / item, parent.parent / item):
        candidate = candidate.resolve()
        if candidate.is_relative_to(ROOT) and candidate.is_file():
            return candidate
    raise FileNotFoundError(f'{parent}: missing dependency {name}')


def tex_graph(entry: Path) -> dict[Path, list[Path]]:
    graph: dict[Path, list[Path]] = {}
    def visit(path: Path) -> None:
        if path in graph:
            return
        children = [resolve_input(n, path, '.tex') for n in INPUT.findall(text_without_comments(path))]
        graph[path] = children
        for child in children:
            visit(child)
    visit(entry.resolve())
    return graph


def pdf_dependencies(entry: Path) -> list[Path]:
    deps = []
    for source in tex_graph(entry):
        for name in PDF.findall(text_without_comments(source)):
            candidate = PAPER / name
            if candidate.suffix.lower() != '.pdf':
                candidate = candidate.with_suffix('.pdf')
            tex = candidate.with_suffix('.tex').resolve()
            if tex.is_file() and tex.is_relative_to(ROOT):
                deps.append(tex)
            elif not candidate.is_file():
                raise FileNotFoundError(f'{source}: neither source nor PDF exists for {name}')
    return sorted(set(deps))


def build(entries: list[Path], dry_run: bool = False) -> list[str]:
    done: set[Path] = set()
    active: set[Path] = set()
    order: list[str] = []
    def visit(entry: Path) -> None:
        entry = entry.resolve()
        if entry in done:
            return
        if entry in active:
            raise RuntimeError(f'Cyclic PDF dependency at {entry}')
        active.add(entry)
        for dependency in pdf_dependencies(entry):
            visit(dependency)
        relative = entry.relative_to(PAPER).as_posix()
        order.append(relative)
        if not dry_run:
            subprocess.run(['latexmk', '-pdf', '-g', '-interaction=nonstopmode',
                            '-halt-on-error', '-file-line-error', '-recorder', relative],
                           cwd=PAPER, check=True)
            if not entry.with_suffix('.pdf').is_file():
                raise RuntimeError(f'Native TeX did not produce {entry.with_suffix(".pdf")}')
        active.remove(entry)
        done.add(entry)
    for entry in entries:
        visit(entry)
    return order


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--dry-run', action='store_true')
    parser.add_argument('--output', type=Path, default=ROOT/'a2-v100-artifacts/BUILD_PLAN.json')
    args = parser.parse_args()
    entries = [PAPER / f'rigidity_v100{s}.tex' for s in ('', '_archive', '_complete')]
    order = build(entries, args.dry_run)
    head = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip()
    record = {'source_head': head, 'dry_run': args.dry_run, 'native_build_order': order}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(record, indent=2, sort_keys=True)+'\n', encoding='utf-8')


if __name__ == '__main__':
    main()
