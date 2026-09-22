#!/usr/bin/env python3
"""Clean native two-volume build with source and cross-reference provenance.

Run from a revision directory: python v35/build_native.py
Or: python build_native.py --source-root PATH --edition v34 --source-commit SHA
No external labels, theorem statements or document inputs are substituted.
"""
from __future__ import annotations
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git_blob(path: Path) -> str:
    data = path.read_bytes()
    return hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()


def sources(root: Path, name: str, seen: set[str] | None = None) -> set[str]:
    seen = set() if seen is None else seen
    name = name if name.endswith('.tex') else name+'.tex'
    if name in seen:
        return seen
    path = root/name
    if not path.is_file():
        raise FileNotFoundError(f'Missing native input: {name}')
    if not path.resolve().is_relative_to(root):
        raise ValueError(f'Input outside source root: {name}')
    seen.add(name)
    text = '\n'.join(re.split(r'(?<!\\)%', line)[0]
                     for line in path.read_text().splitlines())
    for child in re.findall(r'\\(?:input|include)\{([^}]+)\}', text):
        sources(root, child, seen)
    return seen


def exported_labels(aux: str) -> str:
    result = []
    for line in aux.splitlines():
        match = re.match(r'\\newlabel\{([^}]+)\}', line)
        if match and not re.fullmatch(r'tocindent-?\d+', match.group(1)):
            result.append(line)
    return '\\relax\n'+'\n'.join(result)+'\n'


def build(root: Path, edition: str, source_commit: str | None,
          allow_overfull: bool) -> dict:
    root = root.resolve()
    compiler = shutil.which('pdflatex')
    if compiler is None:
        raise RuntimeError('pdflatex is required for the complete native build')
    active = sorted(sources(root, 'main') | sources(root, 'companions'))
    out = root/('verification-'+edition)
    logs = out/'build-logs'
    logs.mkdir(parents=True, exist_ok=True)
    receipt = {
        'status': 'STARTED', 'edition': edition, 'source_commit': source_commit,
        'scope': 'Complete native main.tex and companions.tex; no smoke harness',
        'started_utc': datetime.now(timezone.utc).isoformat(),
        'builder_sha256': digest(Path(__file__)),
        'compiler': subprocess.run([compiler, '--version'], check=True,
            capture_output=True, text=True).stdout.splitlines()[0],
        'source_sha256': {name: digest(root/name) for name in active},
        'source_git_blob': {name: git_blob(root/name) for name in active},
        'source_count': len(active), 'passes': [], 'cross_volume_states': [],
        'stubbed_external_labels': False, 'substituted_theorems': False,
        'pdf_visual_inspection': 'RECORDED_SEPARATELY',
        'proof_assistant': 'NOT_RUN; analytical proofs are in the manuscript',
    }
    try:
        # Remove only generated entrypoint products in this explicit source root.
        for stem in ('main', 'companions'):
            for ext in ('aux','out','toc','log','pdf','fls'):
                (root/f'{stem}.{ext}').unlink(missing_ok=True)
            (root/f'{stem}-external.aux').unlink(missing_ok=True)
        previous = None
        for cycle in range(1, 7):
            for stem in ('main', 'companions'):
                command = [compiler, '-recorder', '-no-shell-escape',
                    '-interaction=nonstopmode', '-halt-on-error',
                    '-file-line-error', stem+'.tex']
                proc = subprocess.run(command, cwd=root, capture_output=True,
                    text=True, encoding='utf-8', errors='replace', timeout=120)
                dest = logs/f'{stem}-pass-{cycle}.log'
                dest.write_text(proc.stdout+'\n'+proc.stderr)
                receipt['passes'].append({'volume': stem, 'cycle': cycle,
                    'command': command, 'returncode': proc.returncode,
                    'log_sha256': digest(dest)})
                if proc.returncode:
                    raise RuntimeError(f'{stem} pass {cycle} failed: {dest.name}')
                aux = (root/f'{stem}.aux').read_text(errors='replace')
                (root/f'{stem}-external.aux').write_text(exported_labels(aux))
            state = {s: digest(root/f'{s}-external.aux')
                     for s in ('main', 'companions')}
            receipt['cross_volume_states'].append({'cycle': cycle, **state})
            if cycle >= 3 and state == previous:
                break
            previous = state
        else:
            raise RuntimeError('Cross-volume labels did not converge within six cycles')
        receipt['cross_volume_labels_stable'] = True
        receipt['layout_warnings'] = {}
        receipt['pdfs'] = {}
        receipt['final_logs'] = {}
        actual_inputs: set[str] = set()
        hard = ('There were undefined references', 'There were undefined citations',
            'undefined on input line', 'multiply defined', 'Label(s) may have changed',
            'No file main-external.aux', 'No file companions-external.aux')
        for stem in ('main', 'companions'):
            log = (root/f'{stem}.log').read_text(errors='replace')
            failed = [item for item in hard if item in log]
            if failed:
                raise RuntimeError(f'Unresolved final {stem}: {failed}')
            receipt['layout_warnings'][stem] = re.findall(r'Overfull \\[hv]box[^\n]*', log)
            receipt['final_logs'][stem] = digest(root/f'{stem}.log')
            page_match = re.search(r'Output written on .*?\((\d+) pages?', log, re.S)
            if page_match is None:
                raise RuntimeError(f'Cannot read {stem} page count')
            pdf = root/f'{stem}.pdf'
            receipt['pdfs'][stem+'.pdf'] = {'sha256': digest(pdf),
                'bytes': pdf.stat().st_size, 'pages': int(page_match.group(1))}
            for line in (root/f'{stem}.fls').read_text().splitlines():
                if line.startswith('INPUT '):
                    path = Path(line[6:])
                    path = (root/path).resolve() if not path.is_absolute() else path.resolve()
                    if path.is_relative_to(root) and path.suffix in ('.tex','.bib'):
                        actual_inputs.add(str(path.relative_to(root)))
        receipt['recorder_source_inputs'] = sorted(actual_inputs)
        if actual_inputs != set(active):
            raise RuntimeError('Declared source closure disagrees with TeX recorder')
        if any(receipt['layout_warnings'].values()) and not allow_overfull:
            raise RuntimeError('Overfull boxes remain; inspect and repair the source')
        for name in active:
            if digest(root/name) != receipt['source_sha256'][name]:
                raise RuntimeError(f'Source changed during build: {name}')
        receipt['status'] = 'COMPILED_REFERENCES_RESOLVED'
    except Exception as exc:
        receipt['status'] = 'FAILED'
        receipt['failure'] = str(exc)
        raise
    finally:
        receipt['finished_utc'] = datetime.now(timezone.utc).isoformat()
        (out/'BUILD_RECEIPT.json').write_text(json.dumps(receipt, indent=2)+'\n')
    return receipt


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source-root', type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument('--edition', default='v35')
    parser.add_argument('--source-commit')
    parser.add_argument('--allow-overfull', action='store_true')
    args = parser.parse_args()
    try:
        receipt = build(args.source_root, args.edition, args.source_commit, args.allow_overfull)
    except Exception as exc:
        print(str(exc), file=sys.stderr)
        return 1
    print(json.dumps({k:receipt[k] for k in ('status','source_count','layout_warnings','pdfs')}, indent=2))
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
