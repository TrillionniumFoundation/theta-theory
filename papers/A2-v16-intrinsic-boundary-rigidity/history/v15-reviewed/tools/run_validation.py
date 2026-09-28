#!/usr/bin/env python3
"""Build the three complete documents and record read-only source qualification."""
from __future__ import annotations
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'verification/current'
OUT.mkdir(parents=True, exist_ok=True)
ENV = {**os.environ, 'PYTHONDONTWRITEBYTECODE': '1'}
receipt = {'schema': 'a2-v15-executed-qualification-1', 'status': 'running',
           'started_utc': datetime.now(timezone.utc).isoformat(),
           'source_commit': os.getenv('GITHUB_SHA'),
           'workflow_commit': os.getenv('GITHUB_WORKFLOW_SHA'),
           'workflow_run_id': os.getenv('GITHUB_RUN_ID'),
           'runner_image': os.getenv('ImageVersion'),
           'commands': [], 'documents': {}, 'formal_proof_certificate': False}


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def execute(name: str, args: list[str], cwd: Path = ROOT) -> Path:
    path = OUT / name
    with path.open('wb') as log:
        result = subprocess.run(args, cwd=cwd, env=ENV, stdout=log,
                                stderr=subprocess.STDOUT, timeout=1200, check=False)
    receipt['commands'].append({'argv': args, 'cwd': str(cwd.relative_to(ROOT)),
                               'exit_code': result.returncode, 'log': name,
                               'log_sha256': sha(path)})
    if result.returncode:
        raise RuntimeError(f'{name} exited {result.returncode}; see {path}')
    return path


def equal_files(a: Path, b: Path) -> None:
    if a.read_bytes() != b.read_bytes():
        raise RuntimeError(f'Diagnostic outputs differ: {a.name}, {b.name}')


try:
    execute('python-version.txt', [sys.executable, '--version'])
    execute('tex-version.txt', ['pdflatex', '--version'])
    execute('latexmk-version.txt', ['latexmk', '-v'])
    before = execute('source-before.json', [sys.executable, 'tools/verify_sources.py'])
    source = json.loads(before.read_text())
    receipt['mathematical_source_manifest_sha256'] = source['mathematical_source_manifest_sha256']
    receipt['frozen_native_v14_tree'] = source['frozen_native_v14_tree']
    pairs = [('v15', ROOT, 'tools/verify_blocks.py', []),
             ('v14', ROOT / 'complete', 'tools/verify_v14.py', ['--algebra-only'])]
    receipt['finite_diagnostics'] = {}
    for key, cwd, script, extra in pairs:
        normal = execute(key + '-normal.json', [sys.executable, script, *extra], cwd)
        optimized = execute(key + '-optimized.json', [sys.executable, '-O', script, *extra], cwd)
        equal_files(normal, optimized)
        receipt['finite_diagnostics'][key] = {'optimized_output_identical': True,
                                             'result': json.loads(normal.read_text())}
    builds = [('primary', ROOT, 'main'),
              ('two_collision', ROOT / 'complete', 'two_collision'),
              ('complete', ROOT / 'complete', 'main')]
    bad = re.compile(r'undefined references|undefined citations|multiply defined|'
                     r'Overfull \\[hv]box|^!|LaTeX Warning:', re.MULTILINE)
    for key, cwd, stem in builds:
        execute(key + '-build.stdout', ['latexmk', '-gg', '-pdf',
                '-interaction=nonstopmode', '-halt-on-error', stem + '.tex'], cwd)
        log, pdf = cwd / (stem + '.log'), cwd / (stem + '.pdf')
        findings = bad.findall(log.read_text(errors='replace'))
        if findings:
            raise RuntimeError(f'{key}: final TeX log has disallowed findings: {findings}')
        info = execute(key + '-pdfinfo.txt', ['pdfinfo', str(pdf)])
        pages = int(re.search(r'^Pages:\s+(\d+)', info.read_text(), re.MULTILINE).group(1))
        receipt['documents'][key] = {'pages': pages, 'pdf_sha256': sha(pdf),
            'final_tex_log_sha256': sha(log), 'final_tex_warning_count': 0,
            'pdf': pdf.relative_to(ROOT).as_posix()}
    after = execute('source-after.json', [sys.executable, 'tools/verify_sources.py'])
    equal_files(before, after)
    receipt['source_unchanged_by_validation'] = True
    receipt['validation_tools_sha256'] = {
        p.name: sha(p) for p in sorted((ROOT / 'tools').glob('*.py'))}
    if os.getenv('GITHUB_SHA'):
        execute('git-clean.txt', ['git', 'diff', '--exit-code'])
        tree = execute('git-tree.txt', ['git', 'rev-parse', 'HEAD^{tree}'])
        receipt['source_tree'] = tree.read_text().strip()
    receipt['status'] = 'passed'
except Exception as exc:
    receipt['status'] = 'failed'
    receipt['error'] = f'{type(exc).__name__}: {exc}'
    raise
finally:
    receipt['finished_utc'] = datetime.now(timezone.utc).isoformat()
    (OUT / 'receipt.json').write_text(json.dumps(receipt, indent=2, sort_keys=True) + '\n')
print(json.dumps({'status': receipt['status'], 'documents': receipt['documents'],
                  'receipt': str(OUT / 'receipt.json')}, indent=2))
