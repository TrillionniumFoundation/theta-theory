#!/usr/bin/env python3
"""Validate the literal TeX input graph and record source hashes; no proof claim."""
from __future__ import annotations
import argparse
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAPER = ROOT / 'papers/A2-v17-boundary-information-coarsening'
INPUT = re.compile(r'\\(?:input|include)\{([^}]+)\}')


def source(path: Path) -> str:
    return re.sub(r'(?<!\\)%[^\n]*', '', path.read_text(encoding='utf-8'))


def graph(entry: str) -> dict[str, dict[str, str]]:
    seen: dict[str, dict[str, str]] = {}
    visiting: set[Path] = set()

    def visit(path: Path) -> None:
        path = path.resolve()
        path.relative_to(PAPER.resolve())  # Reject escaping references.
        key = path.relative_to(ROOT).as_posix()
        if path in visiting:
            raise ValueError(f'Cyclic TeX input: {key}')
        if key in seen:
            return
        if not path.is_file():
            raise FileNotFoundError(f'Missing active TeX source: {key}')
        visiting.add(path)
        data = path.read_bytes()
        seen[key] = {
            'sha256': hashlib.sha256(data).hexdigest(),
            'git_blob': hashlib.sha1(
                f'blob {len(data)}\0'.encode() + data).hexdigest(),
        }
        for name in INPUT.findall(source(path)):
            child = PAPER / name
            if not child.suffix:
                child = child.with_suffix('.tex')
            visit(child)
        visiting.remove(path)

    visit(PAPER / entry)
    return seen


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--core-only', action='store_true',
                        help='Audit only the locally materialized core, not the full manuscript.')
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    entries = ['rigidity_v82_core.tex']
    if not args.core_only:
        entries.append('rigidity_v82.tex')
    result: dict[str, object] = {'scope': 'core-only' if args.core_only else 'full-and-core'}
    graphs = {entry: graph(entry) for entry in entries}
    result['inputs'] = graphs
    if not args.core_only:
        previous = set(INPUT.findall(source(PAPER / 'rigidity_v81.tex')))
        previous.discard('article/v81/frontmatter')  # Superseded title/abstract only.
        active = set(graphs['rigidity_v82.tex'])
        missing = [name for name in sorted(previous)
                   if (PAPER / (name + '.tex')).relative_to(ROOT).as_posix() not in active]
        if missing:
            raise ValueError(f'Lost substantive v81 inputs: {missing}')
        result['retained_v81_top_level_inputs'] = len(previous)
    text = json.dumps(result, indent=2, sort_keys=True) + '\n'
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text, encoding='utf-8')
    else:
        print(text, end='')


if __name__ == '__main__':
    main()
