#!/usr/bin/env python3
"""Build the exact A2 v103 source and its complete inherited native graph.

A full receipt is emitted only after native compilation and log checks.
Use --dry-run to inspect the source-bound plan without claiming success.
"""
from __future__ import annotations
import argparse
import hashlib
import importlib.util
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAPER = ROOT / 'papers/A2-v17-boundary-information-coarsening'
REVIEW = '8054ae5d5c318b7e59f9ad42545ae27b416bec09'


def command(*args: str) -> str:
    return subprocess.check_output(args, cwd=ROOT, text=True).strip()


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_json(path: Path, value: object) -> None:
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + '\n', encoding='utf-8')


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--dry-run', action='store_true')
    parser.add_argument('--output', type=Path, default=ROOT / 'revisions/a2-v103/native')
    args = parser.parse_args()
    output = args.output.resolve()
    allowed = (ROOT / 'revisions/a2-v103').resolve()
    if not output.is_relative_to(allowed) or output == allowed:
        raise ValueError('Output must be a child directory of revisions/a2-v103')
    spec = importlib.util.spec_from_file_location('a2_native_base', ROOT / 'scripts/build_a2_v100.py')
    if spec is None or spec.loader is None:
        raise RuntimeError('Reviewed recursive builder is missing')
    builder = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(builder)
    entries = [PAPER / f'rigidity_v103{s}.tex' for s in ('', '_supporting', '_archive', '_complete')]
    head = command('git', 'rev-parse', 'HEAD')
    order = builder.build(entries, dry_run=True)
    sources = {Path(__file__).resolve(), ROOT / 'scripts/build_a2_v100.py',
               ROOT / 'scripts/check_a2_v103.py', ROOT / '.github/workflows/a2-v103.yml'}
    binary_inputs = set()
    for name in order:
        graph = builder.tex_graph(PAPER / name)
        sources.update(graph)
        for source in graph:
            for pdf_name in builder.PDF.findall(builder.text_without_comments(source)):
                pdf = (PAPER / pdf_name).with_suffix('.pdf').resolve()
                if not pdf.with_suffix('.tex').exists():
                    if not pdf.is_relative_to(ROOT) or not pdf.is_file():
                        raise RuntimeError(f'Unbound binary dependency: {pdf}')
                    binary_inputs.add(pdf)
    hashes = {}

    def bind(path: Path) -> None:
        path = path.resolve()
        relative = path.relative_to(ROOT).as_posix()
        committed = subprocess.check_output(['git', 'show', f'{head}:{relative}'], cwd=ROOT)
        if path.read_bytes() != committed:
            raise RuntimeError(f'Working input differs from {head}: {relative}')
        hashes[relative] = digest(path)

    for source in sorted(sources | binary_inputs):
        bind(source)
    changes = command('git', 'diff', '--name-status', REVIEW, head).splitlines()
    if any(not line.startswith('A\t') for line in changes):
        raise RuntimeError('An inherited path was changed; review preservation before building')
    plan = {'source_head': head, 'source_tree': command('git', 'rev-parse', 'HEAD^{tree}'),
            'review_base': REVIEW, 'native_build_order': order, 'source_sha256': hashes,
            'binary_only_input_paths': [p.relative_to(ROOT).as_posix() for p in sorted(binary_inputs)],
            'preservation': 'addition-only relative to the controlling v102 review', 'changes': changes}
    if args.dry_run:
        print(json.dumps(plan, indent=2, sort_keys=True))
        return
    if output.exists():
        shutil.rmtree(output)
    output.mkdir(parents=True)
    write_json(output / 'BUILD_PLAN.json', plan)
    subprocess.run([sys.executable, str(ROOT / 'scripts/check_a2_v103.py'),
                    '--output', str(output / 'EXACT_DIAGNOSTICS.json')], cwd=ROOT, check=True)
    builder.build(entries, dry_run=False)
    generated_pdfs = {(PAPER / name).with_suffix('.pdf').resolve() for name in order}
    generated_exts = {'.aux', '.out', '.toc', '.bbl', '.blg', '.log', '.fls', '.fdb_latexmk'}
    log_summary = {}
    for name in order:
        target = PAPER / name
        log = target.with_suffix('.log')
        text = log.read_text(errors='replace')
        bad = ('LaTeX Error:', 'There were undefined references', 'multiply defined')
        unresolved = re.search(r'(?:Reference|Citation)\s+[^\n]+undefined', text)
        if any(token in text for token in bad) or unresolved:
            raise RuntimeError(f'Unresolved native log: {log}')
        warnings = {'overfull_boxes': text.count('Overfull \\'),
                    'underfull_boxes': text.count('Underfull \\'),
                    'undefined_references_or_citations': False}
        if target.name == 'rigidity_v103.tex' and (warnings['overfull_boxes'] or warnings['underfull_boxes']):
            raise RuntimeError('Principal typography requires inspection')
        log_summary[name] = warnings
        # Bind additional repository-local recorder inputs (styles, images, etc.).
        # Generated products are distinguished from source and from binary-only inputs.
        recorder = target.with_suffix('.fls')
        for line in recorder.read_text(errors='replace').splitlines():
            if not line.startswith('INPUT '):
                continue
            path = Path(line[6:])
            path = (PAPER / path).resolve() if not path.is_absolute() else path.resolve()
            if not path.is_relative_to(ROOT) or not path.is_file():
                continue
            if path in generated_pdfs or path.suffix in generated_exts:
                continue
            bind(path)
    for relative, sha in hashes.items():
        if digest(ROOT / relative) != sha:
            raise RuntimeError(f'Source changed during native compilation: {relative}')
    (output / 'dependency-logs').mkdir()
    for name in order:
        log = (PAPER / name).with_suffix('.log')
        safe_name = name.replace('/', '__').removesuffix('.tex') + '.log'
        shutil.copy2(log, output / 'dependency-logs' / safe_name)
    outputs = {}
    for entry in entries:
        for ext in ('.pdf', '.log', '.fls', '.aux', '.out', '.toc', '.bbl', '.blg'):
            item = entry.with_suffix(ext)
            if item.is_file():
                dest = output / item.name
                shutil.copy2(item, dest)
    write_json(output / 'LOG_SUMMARY.json', log_summary)
    # Record late-discovered source inputs from the native recorder as well.
    write_json(output / 'BUILD_PLAN.json', plan)
    for item in sorted(output.rglob('*')):
        if item.is_file():
            outputs[item.relative_to(output).as_posix()] = {'sha256': digest(item), 'bytes': item.stat().st_size}
    record = {**plan, 'status': 'native_passed', 'outputs': outputs, 'python': sys.version,
              'pdflatex': command('pdflatex', '--version').splitlines()[0],
              'latexmk': command('latexmk', '-v'), 'github_run_id': os.environ.get('GITHUB_RUN_ID'),
              'github_run_attempt': os.environ.get('GITHUB_RUN_ATTEMPT'),
              'scope': 'Native principal, supporting, archive and complete targets; available PDF-source dependencies rebuilt, binary-only inputs explicitly pinned. Exact finite checks are not formal proof verification.',
              'receipt_commit_convention': 'The source head is the compiled commit; a later artifact-only commit is not claimed to have compiled its own hash.'}
    write_json(output / 'RUNTIME_RECEIPT.json', record)
    print(json.dumps({'status': 'native_passed', 'source_head': head, 'output': str(output)}))


if __name__ == '__main__':
    main()
