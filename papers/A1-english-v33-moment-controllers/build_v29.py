#!/usr/bin/env python3
"""Offline native two-volume build for A1 v29; receipts state actual execution."""
from __future__ import annotations
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
OUT = ROOT / 'build-v29'

def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def git_blob(path: Path) -> str:
    data = path.read_bytes()
    return hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()

def audit(stage: Path, helpers) -> dict:
    texts = {doc: helpers.expand(stage, stage / (doc + '.tex'))
             for doc in ('main', 'companions')}
    labels = {doc: re.findall(r'\\label\{([^}]+)\}', text)
              for doc, text in texts.items()}
    union = labels['main'] + labels['companions']
    duplicates = {key: n for key, n in Counter(union).items() if n > 1}
    refs = set()
    for text in texts.values():
        refs.update(key for key in re.findall(r'\\(?:eq)?ref\{([^}]+)\}', text)
                    if '#' not in key)
        refs.update(re.findall(r'\\upref\{[^}]+\}\{([^}]+)\}', text))
    missing = sorted(refs - set(union))
    if duplicates or missing:
        raise ValueError(f'Reference audit: duplicates={duplicates}, missing={missing}')
    for doc, text in texts.items():
        cited = {key.strip() for match in re.finditer(r'\\cite(?:\[[^]]*\])*\{([^}]+)\}', text)
                 for key in match[1].split(',')}
        bib = set(re.findall(r'\\bibitem(?:\[[^]]*\])?\{([^}]+)\}', text))
        if cited - bib:
            raise ValueError(f'{doc}: missing citations {sorted(cited-bib)}')
        (OUT / (doc + '-expanded.tex')).write_text(text, encoding='utf-8')
    return {'label_counts': {doc: len(keys) for doc, keys in labels.items()},
            'duplicate_labels': duplicates, 'missing_references': missing}

def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--prepare-only', action='store_true')
    args = parser.parse_args()
    OUT.mkdir(exist_ok=True)
    record = {'version': 29, 'status': 'started', 'full_two_volume_build': False,
              'tex_passes': [], 'scope': 'Source, finite diagnostics and typesetting; not proof or venue certification.'}
    try:
        import build_v28 as helpers
        helpers.OUT = OUT
        pins = json.loads((ROOT / 'NATIVE_SOURCE_RECORD_V28.json').read_text())['pinned_blobs']
        pins['baseline-v28-main.tex'] = '2344a69fa0a4d0a8a9c7220019442ee86b990543'
        for name, expected in pins.items():
            if git_blob(ROOT / name) != expected:
                raise ValueError('Inherited source differs: ' + name)
        record['inherited_pinned_blobs_checked'] = len(pins)
        record['diagnostics'] = {}
        for name in ('diagnostics.py', 'diagnostics_v27.py', 'diagnostics_v28.py', 'diagnostics_v29.py'):
            outputs = []
            for opts in ([], ['-O']):
                proc = subprocess.run([sys.executable, *opts, str(ROOT / name)],
                                      capture_output=True, text=True, check=True, timeout=180)
                outputs.append(proc.stdout)
            if outputs[0] != outputs[1]:
                raise ValueError('Normal and optimized output differ: ' + name)
            record['diagnostics'][name] = {'sha256': sha256(ROOT / name),
                                           'normal_optimized_identical': True,
                                           'result': json.loads(outputs[0])}
        stage = OUT / 'native'
        if stage.exists():
            shutil.rmtree(stage)
        shutil.copytree(ROOT, stage, ignore=shutil.ignore_patterns(
            'build-v*', 'build', '__pycache__', '*.pdf', '*.aux', '*.log', '*.out', '*.toc'))
        helpers.companion_bibliography(stage)
        record['source_audit'] = audit(stage, helpers)
        for doc in ('main', 'companions'):
            path = stage / (doc + '.tex')
            text = path.read_text().replace(r'\externaldocument[][nocite]', r'\externaldocument')
            path.write_text(text, encoding='utf-8')
        record['active_source_sha256'] = {str(path.relative_to(stage)): sha256(path)
                                         for path in sorted(stage.rglob('*.tex'))}
        if args.prepare_only:
            record['status'] = 'source-and-diagnostics-passed; TeX not requested'
            return
        engine = shutil.which('pdflatex')
        if not engine:
            raise RuntimeError('pdflatex unavailable; no complete build performed')
        record['engine'] = subprocess.run([engine, '--version'], capture_output=True,
                                          text=True, check=True).stdout.splitlines()[0]
        allowed = {doc: set(re.findall(r'\\label\{([^}]+)\}',
                                      helpers.expand(stage, stage / (doc + '.tex'))))
                   for doc in ('main', 'companions')}
        for doc in allowed:
            helpers.export_labels(stage, doc, allowed[doc])
        for iteration in range(1, 6):
            for doc in allowed:
                proc = subprocess.run([engine, '-no-shell-escape', '-interaction=nonstopmode',
                                       '-halt-on-error', doc + '.tex'], cwd=stage,
                                      capture_output=True, text=True, timeout=180)
                (OUT / f'{doc}-pass-{iteration}.txt').write_text(proc.stdout + proc.stderr)
                record['tex_passes'].append({'document': doc, 'pass': iteration, 'returncode': proc.returncode})
                if proc.returncode:
                    raise RuntimeError(f'{doc} pass {iteration} failed; see captured log')
                helpers.export_labels(stage, doc, allowed[doc])
        bad = re.compile(r'undefined|multiply defined|Rerun to get cross-references right|Label\(s\) may have changed|Overfull \\[hv]box', re.I)
        record['final_log_messages'] = {}
        for doc in allowed:
            text = (stage / (doc + '.log')).read_text(errors='replace')
            record['final_log_messages'][doc] = [line for line in text.splitlines()
                                                  if any(word in line for word in ('Warning:', 'Underfull', 'Overfull'))]
            if bad.search(text):
                raise RuntimeError(f'{doc}: unresolved reference or layout warning')
        record['pdf_sha256'] = {doc: sha256(stage / (doc + '.pdf')) for doc in allowed}
        record['full_two_volume_build'] = True
        record['status'] = 'native-two-volume-build-passed; visual inspection separate'
    except Exception as exc:
        record['status'] = 'failed'
        record['error'] = str(exc)
        raise
    finally:
        (OUT / 'BUILD_RECORD_V29.json').write_text(json.dumps(record, indent=2, sort_keys=True) + '\n')
        print(json.dumps(record, indent=2, sort_keys=True))

if __name__ == '__main__':
    main()
