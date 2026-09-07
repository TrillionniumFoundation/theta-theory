#!/usr/bin/env python3
"""Materialize and build the complete A1 v27 source overlay without editing v26."""
from __future__ import annotations
import argparse
import datetime
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys


BASE_SUBMISSION = 'a2e5d3737085241137211f1cf21393d5bcafa1ce'
BASE_PAPER_TREE = '899f2124e9e43e11f2e99f0bbba84d7806f34bda'
REVIEW_COMMIT = '19fbf4fe0e7495afd537de73a63670a9cf5616e0'
MARKER = '.theta-v27-build-root'


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_json(path: Path, value: dict) -> None:
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + '\n', encoding='utf-8')


def export_labels(source: Path, target: Path) -> None:
    if not source.is_file():
        raise RuntimeError(f'Missing auxiliary file: {source}')
    # External documents supply theorem labels, never foreign bibliography numbers.
    lines = [line for line in source.read_text(encoding='utf-8', errors='replace').splitlines()
             if line.startswith('\\newlabel{')]
    target.write_text('\n'.join(lines) + '\n', encoding='utf-8')


def materialize(source: Path, base: Path, output: Path) -> tuple[Path, list[dict]]:
    if not (base / 'main.tex').is_file() or not (base / 'companions.tex').is_file():
        raise RuntimeError('The complete repository source papers/A1-english-v26 is required.')
    if output == source or output == base or output in source.parents or output in base.parents:
        raise RuntimeError('The build directory must not replace a source directory or its ancestor.')
    if output.exists() and any(output.iterdir()) and not (output / MARKER).is_file():
        raise RuntimeError('Refusing to replace an unmarked, nonempty output directory.')
    output.mkdir(parents=True, exist_ok=True)
    (output / MARKER).write_text('Generated A1 v27 build files only.\n', encoding='utf-8')
    stage = output / 'native'
    if stage.exists():
        shutil.rmtree(stage)
    shutil.copytree(base, stage, ignore=shutil.ignore_patterns('__pycache__', '.git', 'build-v27'))
    # Collect before copying, and exclude the output tree to prevent recursion.
    additions = [p for p in source.rglob('*') if p.is_file()
                 and output not in p.parents and '__pycache__' not in p.parts
                 and '.git' not in p.parts]
    for path in additions:
        target = stage / path.relative_to(source)
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, target)
    patches = []
    # The older xr-hyper interface lacks the optional nocite argument. The
    # exported external aux files contain labels only, so the forms are equivalent.
    for path in stage.rglob('*.tex'):
        text = path.read_text(encoding='utf-8')
        old = '\\externaldocument[][nocite]'
        if old in text:
            count = text.count(old)
            path.write_text(text.replace(old, '\\externaldocument'), encoding='utf-8')
            patches.append({'path': str(path.relative_to(stage)),
                            'change': 'xr-hyper label-only compatibility', 'occurrences': count})
    return stage, patches


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output-dir', type=Path)
    parser.add_argument('--materialize-only', action='store_true')
    parser.add_argument('--engine', default='pdflatex')
    args = parser.parse_args()
    source = Path(__file__).resolve().parent
    base = source.parent / 'A1-english-v26'
    output = (args.output_dir or source / 'build-v27').resolve()
    record = {'revision': 'A1-v27', 'review_commit': REVIEW_COMMIT,
              'base_submission': BASE_SUBMISSION, 'base_paper_tree': BASE_PAPER_TREE,
              'started_at_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
              'native_two_volume_compile': 'not started', 'passes': [],
              'pdf_visual_inspection': 'not performed by this script',
              'scope': 'Materialization and native TeX compilation only; not proof verification.'}
    try:
        stage, patches = materialize(source, base, output)
        record['staging_directory'] = str(stage)
        record['staging_compatibility_patches'] = patches
        record['source_sha256'] = {str(p.relative_to(source)): sha256(p)
                                   for p in source.rglob('*') if p.is_file()
                                   and output not in p.parents and '__pycache__' not in p.parts}
        if args.materialize_only:
            record['native_two_volume_compile'] = 'not requested'
            write_json(output / 'BUILD_RECORD_V27.json', record)
            print(f'Materialized complete source: {stage}')
            return 0
        engine = shutil.which(args.engine)
        if engine is None:
            raise RuntimeError(f'TeX engine not found: {args.engine}')
        version = subprocess.run([engine, '--version'], check=True, capture_output=True,
                                 text=True, timeout=30)
        record['engine'] = version.stdout.splitlines()[0]
        env = dict(os.environ)
        env['TEXINPUTS'] = str(stage) + os.pathsep + env.get('TEXINPUTS', '')
        for cycle in range(1, 4):
            for name in ('companions', 'main'):
                command = [engine, '-interaction=nonstopmode', '-halt-on-error',
                           '-file-line-error', '-no-shell-escape', name + '.tex']
                result = subprocess.run(command, cwd=stage, env=env, capture_output=True,
                                        text=True, errors='replace', timeout=180)
                stdout_path = output / f'{name}-pass-{cycle}.stdout.txt'
                stdout_path.write_text(result.stdout + '\n' + result.stderr, encoding='utf-8')
                record['passes'].append({'document': name, 'cycle': cycle,
                                         'returncode': result.returncode,
                                         'stdout': str(stdout_path.relative_to(output))})
                if result.returncode:
                    raise RuntimeError(f'{name}, pass {cycle}, failed; inspect {stdout_path}')
                export_labels(stage / (name + '.aux'), stage / (name + '-external.aux'))
        issues = []
        overfull = {}
        for name in ('main', 'companions'):
            log = (stage / (name + '.log')).read_text(encoding='utf-8', errors='replace')
            patterns = [r'There were undefined references', r'There were undefined citations',
                        r'(?:Reference|Citation) [^\n]*undefined',
                        r'Label\(s\) may have changed', r'There were multiply-defined labels']
            for pattern in patterns:
                if re.search(pattern, log):
                    issues.append({'document': name, 'pattern': pattern})
            overfull[name] = re.findall(r'Overfull \\[hv]box[^\n]*', log)
        record['reference_issues'] = issues
        record['overfull_box_messages'] = overfull
        if issues:
            raise RuntimeError('Unresolved or unstable references remain in a final native log.')
        record['native_two_volume_compile'] = 'passed'
        record['pdfs'] = {}
        for name in ('main', 'companions'):
            pdf = stage / (name + '.pdf')
            if not pdf.is_file():
                raise RuntimeError(f'Missing generated PDF: {pdf}')
            record['pdfs'][name] = {'path': str(pdf), 'sha256': sha256(pdf),
                                    'bytes': pdf.stat().st_size}
        write_json(output / 'BUILD_RECORD_V27.json', record)
        print(f'Native compilation passed. Record: {output / "BUILD_RECORD_V27.json"}')
        print('PDF visual inspection remains a separate step.')
        return 0
    except Exception as exc:
        record['native_two_volume_compile'] = 'failed or not completed'
        record['error'] = f'{type(exc).__name__}: {exc}'
        if output.is_dir() and (output / MARKER).is_file():
            write_json(output / 'BUILD_RECORD_V27.json', record)
        print(record['error'], file=sys.stderr)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
