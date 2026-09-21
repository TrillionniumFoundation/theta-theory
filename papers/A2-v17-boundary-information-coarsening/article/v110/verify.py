#!/usr/bin/env python3
"""Exact-source review build. Full mode replays v110, v109 and v108.

--allow-partial is a principal-only local build and never claims Git binding.
The full receipt is written only after every inherited and new check succeeds.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[3] if len(HERE.parents) > 3 else HERE
REVIEW = '87b63e155dac402ec6a9d0a34f69ff0ba5363fdb'
PREFIX = 'papers/A2-v17-boundary-information-coarsening/article/v110/'
BAD = re.compile(r'undefined|multiply defined|Label\(s\) may have changed|Overfull \\hbox', re.I)
SOURCE_NAMES = ('paper.tex', 'checks.py', 'verify.py', 'README.md',
                'RESPONSE_TO_R109.md', 'DEPENDENCIES.md')


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def blob(path):
    data = path.read_bytes()
    return hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()


def command(args, cwd, log=None):
    proc = subprocess.run(args, cwd=cwd, text=True, stdout=subprocess.PIPE,
                          stderr=subprocess.STDOUT, check=False)
    if log is not None:
        log.write_text(proc.stdout)
    if proc.returncode:
        raise RuntimeError(f'Command failed ({proc.returncode}): {args}\n{proc.stdout}')
    return proc.stdout


def verify(partial=False):
    evidence = HERE/'evidence'
    evidence.mkdir(exist_ok=True)
    sources = [HERE/name for name in SOURCE_NAMES]
    if not all(p.is_file() for p in sources):
        raise FileNotFoundError('Missing principal source or metadata')
    commit = None
    manifest = {}
    if not partial:
        commit = command(['git', 'rev-parse', 'HEAD'], REPO).strip()
        changes = command(['git', 'diff', '--name-status', REVIEW, commit], REPO)
        allowed = ('A2_REVISION_V110_INDEX.md', '.github/workflows/a2-v110-review.yml')
        for line in changes.splitlines():
            status, path = line.split('\t', 1)
            if status != 'A' or not (path.startswith(PREFIX) or path in allowed):
                raise RuntimeError('Inherited path modified, deleted, or unrelated addition: '+line)
        sources += [REPO/name for name in allowed]
        for p in sources:
            rel = p.relative_to(REPO).as_posix()
            raw = subprocess.run(['git', 'show', f'{commit}:{rel}'], cwd=REPO,
                                 stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True).stdout
            if raw != p.read_bytes():
                raise RuntimeError('Worktree differs from immutable source commit: '+rel)
            manifest[rel] = {'sha256': sha(p), 'git_blob': blob(p)}
    else:
        manifest = {p.name: {'sha256': sha(p), 'git_blob': blob(p)} for p in sources}

    inherited = None
    if not partial:
        previous = HERE.parent/'v109'
        command([sys.executable, str(previous/'verify.py')], REPO,
                evidence/'inherited-verifier-console.txt')
        inherited = json.loads((previous/'evidence/verification.json').read_text())
        if inherited.get('status') != 'passed' or not inherited.get('source_bound') or inherited.get('source_commit') != commit:
            raise RuntimeError('Inherited receipt is not bound to this source commit')
        manifest.update(json.loads((previous/'evidence/source-manifest.json').read_text()))
        for p in (previous/'evidence').iterdir():
            if p.suffix in ('.json', '.txt', '.log', '.pdf'):
                shutil.copyfile(p, evidence/('inherited-'+p.name))
        referee = REPO/'reviews/a2-v109-independent-harsh-top4-2026-09-21/INDEPENDENT_CHECKS.py'
        out = command([sys.executable, str(referee)], REPO,
                      evidence/'independent-v109-referee.json')
        if json.loads(out).get('status') != 'passed':
            raise RuntimeError('Independent v109 referee diagnostics failed')
        rel = referee.relative_to(REPO).as_posix()
        raw = subprocess.run(['git', 'show', f'{commit}:{rel}'], cwd=REPO,
                             stdout=subprocess.PIPE, check=True).stdout
        if raw != referee.read_bytes():
            raise RuntimeError('Referee script differs from source commit')
        manifest[rel] = {'sha256': sha(referee), 'git_blob': blob(referee)}

    out = command([sys.executable, str(HERE/'checks.py'), '--output', str(evidence/'checks-v110.json')],
                  HERE, evidence/'checks-v110-console.txt')
    diagnostics = json.loads(out)
    if diagnostics['status'] != 'passed':
        raise RuntimeError('v110 diagnostics failed')
    with tempfile.TemporaryDirectory(prefix='A2-v110-') as temporary:
        args = ['latexmk', '-pdf', '-interaction=nonstopmode', '-halt-on-error',
                '-file-line-error', '-outdir='+temporary, '-jobname=A2-v110', 'paper.tex']
        command(args, HERE, evidence/'A2-v110-console.txt')
        pdf = Path(temporary)/'A2-v110.pdf'
        log = Path(temporary)/'A2-v110.log'
        lines = [line for line in log.read_text(errors='replace').splitlines() if BAD.search(line)]
        shutil.copyfile(log, evidence/log.name)
        if lines:
            raise RuntimeError('Forbidden final TeX diagnostics: '+repr(lines))
        shutil.copyfile(pdf, evidence/pdf.name)
        info = command(['pdfinfo', str(pdf)], HERE)
        pages = int(re.search(r'^Pages:\s+(\d+)', info, re.M).group(1))
    manifest_text = json.dumps(manifest, indent=2, sort_keys=True)+'\n'
    (evidence/'source-manifest.json').write_text(manifest_text)
    receipt = {
        'status': 'passed', 'source_commit': commit, 'review_commit': REVIEW,
        'source_bound': not partial,
        'execution': 'exact Git checkout' if not partial else 'unbound local principal bundle',
        'scope': 'three-volume build and finite diagnostics' if not partial else 'principal build and finite diagnostics only',
        'not_proof_certification': True,
        'inherited_paths_unchanged': True if not partial else None,
        'source_manifest_sha256': hashlib.sha256(manifest_text.encode()).hexdigest(),
        'source_file_count': len(manifest), 'run_url': os.environ.get('A2_RUN_URL'),
        'principal': {'pages': pages, 'pdf_sha256': sha(evidence/'A2-v110.pdf'),
                      'log_sha256': sha(evidence/'A2-v110.log'), 'forbidden_diagnostics': []},
        'checks_v110_sha256': sha(evidence/'checks-v110.json'),
        'inherited_receipt': inherited,
        'python': sys.version,
        'compiler': command(['pdflatex', '--version'], HERE).splitlines()[0],
        'latexmk': command(['latexmk', '-v'], HERE).strip(),
    }
    name = 'verification.json' if not partial else 'local-verification.json'
    (evidence/name).write_text(json.dumps(receipt, indent=2, sort_keys=True)+'\n')
    print(json.dumps(receipt, indent=2, sort_keys=True))
    return receipt


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--allow-partial', action='store_true')
    verify(parser.parse_args().allow_partial)
