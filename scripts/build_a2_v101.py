#!/usr/bin/env python3
"""Reuse the reviewed recursive native builder and preserve v101 evidence.

A successful receipt is written only after all three native targets and
all their PDF-source dependencies have built. It names the triggering
source commit; a later receipt-only commit does not pretend to have
compiled its own self-referential commit hash.
"""
from __future__ import annotations
import argparse
import hashlib
import importlib.util
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAPER = ROOT/'papers/A2-v17-boundary-information-coarsening'


def command(*args: str) -> str:
    return subprocess.check_output(args, cwd=ROOT, text=True).strip()


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--dry-run', action='store_true')
    parser.add_argument('--output', type=Path, default=ROOT/'revisions/a2-v101/native')
    args = parser.parse_args()
    spec = importlib.util.spec_from_file_location('a2_native_base', ROOT/'scripts/build_a2_v100.py')
    if spec is None or spec.loader is None:
        raise RuntimeError('The reviewed recursive builder is missing')
    builder = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(builder)
    entries = [PAPER/f'rigidity_v101{s}.tex' for s in ('', '_archive', '_complete')]
    head = command('git', 'rev-parse', 'HEAD')
    order = builder.build(entries, dry_run=True)
    sources = {ROOT/'scripts/build_a2_v100.py', Path(__file__).resolve(),
               ROOT/'scripts/check_a2_v101.py', ROOT/'.github/workflows/a2-v101.yml'}
    for name in order:
        sources.update(builder.tex_graph(PAPER/name))
    source_hashes = {}
    for source in sorted(sources):
        relative = source.relative_to(ROOT).as_posix()
        committed = subprocess.check_output(['git', 'show', f'{head}:{relative}'], cwd=ROOT)
        if committed != source.read_bytes():
            raise RuntimeError(f'Source differs from triggering commit: {relative}')
        source_hashes[relative] = sha(source)
    if args.dry_run:
        print(json.dumps({'source_head': head, 'dry_run': True, 'native_build_order': order,
                          'source_sha256': source_hashes}, indent=2, sort_keys=True))
        return
    # No prior receipt may survive a failed rerun and be mistaken for new success.
    if args.output.exists():
        shutil.rmtree(args.output)
    args.output.mkdir(parents=True)
    builder.build(entries, dry_run=False)
    for relative, digest in source_hashes.items():
        if sha(ROOT/relative) != digest:
            raise RuntimeError(f'Source changed during native execution: {relative}')
    outputs = {}
    unresolved = ('There were undefined references', 'Citation ', 'multiply defined')
    for entry in entries:
        log = entry.with_suffix('.log')
        text = log.read_text(errors='replace')
        if 'LaTeX Error:' in text or any(x in text for x in unresolved):
            raise RuntimeError(f'Native output has unresolved references/citations: {log}')
        stem = entry.stem
        for ext in ('.pdf', '.log', '.fls', '.aux', '.out', '.toc', '.bbl', '.blg'):
            item = entry.with_suffix(ext)
            if item.is_file():
                dest = args.output/(stem+ext)
                shutil.copy2(item, dest)
                outputs[dest.name] = {'sha256': sha(dest), 'bytes': dest.stat().st_size}
    record = {
        'status': 'native_passed',
        'source_head': head,
        'source_tree': command('git', 'rev-parse', 'HEAD^{tree}'),
        'source_sha256': source_hashes,
        'native_build_order': order,
        'outputs': outputs,
        'bibliography': 'Inline thebibliography; no BibTeX bbl is required for the principal article.',
        'python': sys.version,
        'pdflatex': command('pdflatex', '--version').splitlines()[0],
        'latexmk': command('latexmk', '-v'),
        'github_run_id': os.environ.get('GITHUB_RUN_ID'),
        'github_run_attempt': os.environ.get('GITHUB_RUN_ATTEMPT'),
        'scope': 'Native compilation and source binding, not machine verification of mathematical proofs.',
        'receipt_commit_convention': 'This receipt names the built source commit. A later commit may add only these artifacts; compare source_sha256 rather than asserting self-referential HEAD equality.',
    }
    (args.output/'RUNTIME_RECEIPT.json').write_text(json.dumps(record, indent=2, sort_keys=True)+'\n')
    print(json.dumps({'status': record['status'], 'source_head': head, 'output': str(args.output)}))


if __name__ == '__main__':
    main()
