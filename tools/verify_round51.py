#!/usr/bin/env python3
"""Verify a frozen Round 51 checkout; never reseal or silently skip a failed step.

Run from any directory: python tools/verify_round51.py [--build]
A successful exit without --build verifies source identity and executes the tests,
not the PDF. Outputs are written below artifacts/round51 and are not manifest inputs.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / 'round51/SOURCE_MANIFEST.json'


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def checked_path(relative: str) -> Path:
    candidate = (ROOT / relative).resolve()
    if not candidate.is_relative_to(ROOT) or not candidate.is_file():
        raise ValueError(f'Missing or unsafe input path: {relative}')
    return candidate


def source_check() -> dict:
    manifest = json.loads(MANIFEST.read_text(encoding='utf-8'))
    files = manifest['files']
    if not files or manifest['roots'] != ['ROUND51_REVISION.tex']:
        raise ValueError('Unexpected active roots or empty source manifest')
    for relative, expected in files.items():
        path = checked_path(relative)
        if sha256(path) != expected['sha256']:
            raise ValueError(f'SHA256 mismatch: {relative}')
        raw = path.read_bytes()
        blob = hashlib.sha1(b'blob ' + str(len(raw)).encode() + b'\0' + raw).hexdigest()
        if blob != expected['git_blob']:
            raise ValueError(f'Git blob mismatch: {relative}')
    seen: set[str] = set()
    pending = list(manifest['roots'])
    while pending:
        relative = pending.pop()
        if relative in seen:
            continue
        if relative not in files:
            raise ValueError(f'TeX dependency missing from manifest: {relative}')
        seen.add(relative)
        text = checked_path(relative).read_text(encoding='utf-8')
        # All active inputs are literal, root-relative paths. Reject dynamic inputs.
        if re.search(r'\\(?:input|include)\s+[^\s{]', text):
            raise ValueError(f'Nonliteral TeX input in {relative}')
        for dep in re.findall(r'\\(?:input|include)\{([^}]+)\}', text):
            if '\\' in dep or '#' in dep:
                raise ValueError(f'Dynamic TeX dependency in {relative}')
            pending.append(dep if Path(dep).suffix else dep + '.tex')
    return dict(manifest_sha256=sha256(MANIFEST), files_checked=len(files),
                tex_closure=sorted(seen), status='passed')


def run_logged(command: list[str], logfile: Path) -> None:
    with logfile.open('w', encoding='utf-8') as stream:
        result = subprocess.run(command, cwd=ROOT, stdout=stream,
                                stderr=subprocess.STDOUT, text=True, check=False)
    if result.returncode:
        raise RuntimeError(f'Command failed ({result.returncode}): {command}; see {logfile}')


def verify(build: bool) -> int:
    out = ROOT / 'artifacts/round51'
    out.mkdir(parents=True, exist_ok=True)
    receipt = dict(schema=1, revision='Round 51',
                   checked_at_utc=datetime.now(timezone.utc).isoformat(),
                   python=sys.version, source={}, tests={},
                   pdf={'requested': build, 'status': 'not_run'},
                   formal_proof_verification=False, status='failed')
    try:
        receipt['source'] = source_check()
        run_logged([sys.executable, 'tests/test_round51.py', '--json-out',
                    'artifacts/round51/TEST_RESULTS.json'], out/'TESTS.log')
        tests = json.loads((out/'TEST_RESULTS.json').read_text(encoding='utf-8'))
        if not tests['success']:
            raise RuntimeError('Test runner did not report success')
        receipt['tests'] = tests
        if build:
            executable = shutil.which('pdflatex')
            if executable is None:
                raise RuntimeError('pdflatex is required for --build; build not skipped')
            cmd = [executable, '-interaction=nonstopmode', '-halt-on-error',
                   '-file-line-error', '-output-directory=artifacts/round51',
                   'ROUND51_REVISION.tex']
            for k in range(1, 4):
                run_logged(cmd, out/f'build-pass{k}.log')
            log = (out/'ROUND51_REVISION.log').read_text(encoding='utf-8', errors='replace')
            forbidden = ['undefined references', 'undefined citations',
                         'Label(s) may have changed', 'Overfull \\hbox', 'Overfull \\vbox']
            bad = [s for s in forbidden if s in log]
            if re.search(r'LaTeX Warning: (?:Reference|Citation).*undefined', log):
                bad.append('undefined reference/citation')
            if bad:
                raise RuntimeError('Unresolved build diagnostics: '+', '.join(bad))
            pdf = out/'ROUND51_REVISION.pdf'
            if not pdf.is_file() or not pdf.read_bytes().startswith(b'%PDF-'):
                raise RuntimeError('Expected PDF output missing')
            receipt['pdf'] = dict(requested=True, status='passed', passes=3,
                                  sha256=sha256(pdf), bytes=pdf.stat().st_size,
                                  visual_inspection='separately reported')
        receipt['status'] = 'passed'
    except Exception as exc:
        receipt['error'] = f'{type(exc).__name__}: {exc}'
    (out/'VERIFICATION.json').write_text(json.dumps(receipt, indent=2)+'\n', encoding='utf-8')
    print(json.dumps(receipt, indent=2))
    return 0 if receipt['status'] == 'passed' else 1


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--build', action='store_true', help='Require and run a three-pass TeX build')
    args = parser.parse_args()
    sys.exit(verify(args.build))
