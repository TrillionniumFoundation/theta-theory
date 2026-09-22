#!/usr/bin/env python3
"""Build both complete volumes and audit cross-volume references.

Run: python v33/build_revision.py [--allow-overfull]
Only source inputs reached from the entrypoints are hashed. This script does
not certify mathematics or visual appearance. Its receipt records execution.
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

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'verification-v33'

def sha256(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()

def inputs(name: str, seen: set[str] | None = None) -> set[str]:
    if seen is None:
        seen = set()
    name = name if name.endswith('.tex') else name + '.tex'
    if name in seen:
        return seen
    p = ROOT / name
    if not p.is_file():
        raise FileNotFoundError(name)
    seen.add(name)
    text = '\n'.join(re.split(r'(?<!\\)%', x)[0] for x in p.read_text().splitlines())
    for child in re.findall(r'\\(?:input|include)\{([^}]+)\}', text):
        inputs(child, seen)
    return seen

def exported_labels(aux: str) -> str:
    lines = []
    for line in aux.splitlines():
        m = re.match(r'\\newlabel\{([^}]+)\}', line)
        if m and not re.fullmatch(r'tocindent-?\d+', m.group(1)):
            lines.append(line)
    return '\\relax\n' + '\n'.join(lines) + '\n'

def build(allow_overfull: bool = False) -> dict:
    OUT.mkdir(exist_ok=True)
    logs = OUT / 'build-logs'
    logs.mkdir(exist_ok=True)
    compiler = shutil.which('pdflatex')
    if not compiler:
        raise RuntimeError('pdflatex is required')
    active = sorted(inputs('main') | inputs('companions'))
    result = {
        'status': 'STARTED',
        'started_utc': datetime.now(timezone.utc).isoformat(),
        'scope': 'Complete main.tex and companions.tex; no packet substitute',
        'review_commit': '60c5b116a2c002dfd8056a351a87d7014d8c78e1',
        'inherited_manuscript_commit': 'e712437fe13cf29978715d3f16d825eadb450fea',
        'compiler': subprocess.run([compiler, '--version'], capture_output=True,
                                  text=True, check=True).stdout.splitlines()[0],
        'source_sha256': {x: sha256(ROOT/x) for x in active},
        'passes': [], 'visual_inspection': 'RECORDED_SEPARATELY',
        'mathematical_proof_checker': 'NOT_RUN; analytical manuscript proofs',
    }
    try:
        for stem in ('main', 'companions'):
            for ext in ('aux', 'out', 'toc', 'log', 'pdf'):
                (ROOT/f'{stem}.{ext}').unlink(missing_ok=True)
            (ROOT/f'{stem}-external.aux').write_text('\\relax\n')
        previous = None
        for cycle in range(1, 7):
            for stem in ('main', 'companions'):
                cmd = [compiler, '-no-shell-escape', '-interaction=nonstopmode',
                       '-halt-on-error', '-file-line-error', stem+'.tex']
                proc = subprocess.run(cmd, cwd=ROOT, text=True, capture_output=True,
                                      encoding='utf-8', errors='replace', timeout=90)
                dest = logs/f'{stem}-pass-{cycle}.log'
                dest.write_text(proc.stdout+'\n'+proc.stderr)
                result['passes'].append({'volume':stem, 'cycle':cycle,
                    'returncode':proc.returncode, 'stdout_sha256':sha256(dest)})
                if proc.returncode:
                    raise RuntimeError(f'{stem} pass {cycle} failed: {dest}')
                (ROOT/f'{stem}-external.aux').write_text(
                    exported_labels((ROOT/f'{stem}.aux').read_text()))
            state = tuple(sha256(ROOT/f'{s}-external.aux') for s in ('main','companions'))
            if cycle >= 3 and state == previous:
                break
            previous = state
        else:
            raise RuntimeError('Cross-volume references did not stabilize')
        hard = ('There were undefined references', 'There were undefined citations',
                'undefined on input line', 'multiply defined', 'Label(s) may have changed')
        result['layout_warnings'] = {}
        result['pdfs'] = {}
        for stem in ('main','companions'):
            log = (ROOT/f'{stem}.log').read_text(errors='replace')
            failures = [x for x in hard if x in log]
            if failures:
                raise RuntimeError(f'Unresolved {stem}: {failures}')
            result['layout_warnings'][stem] = re.findall(r'Overfull \\[hv]box[^\n]*', log)
            pdf = ROOT/f'{stem}.pdf'
            result['pdfs'][stem] = {'sha256':sha256(pdf), 'bytes':pdf.stat().st_size}
        if any(result['layout_warnings'].values()) and not allow_overfull:
            raise RuntimeError('Overfull boxes: repair or explicitly record with --allow-overfull')
        result['status'] = 'COMPILED_REFERENCES_RESOLVED'
    except Exception as exc:
        result['status'] = 'FAILED'
        result['failure'] = str(exc)
        raise
    finally:
        result['finished_utc'] = datetime.now(timezone.utc).isoformat()
        (OUT/'BUILD_RECEIPT.json').write_text(json.dumps(result, indent=2)+'\n')
    return result

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--allow-overfull', action='store_true')
    args = parser.parse_args()
    try:
        receipt = build(args.allow_overfull)
    except Exception as exc:
        print(str(exc), file=sys.stderr)
        return 1
    print(json.dumps({k:receipt[k] for k in ('status','layout_warnings','pdfs')}, indent=2))
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
