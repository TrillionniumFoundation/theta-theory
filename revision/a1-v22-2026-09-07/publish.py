#!/usr/bin/env python3
"""Publish only v22 outputs after an actual successful validation, without force."""
from __future__ import annotations
import json
import hashlib
import os
from pathlib import Path
import subprocess

BRANCH = 'revision/a1-english-v22-prior-uniform-algebra-2026-09-07'
PREFIX = 'papers/A1-english-v22/'

def git(*args: str) -> str:
    return subprocess.check_output(['git', *args], text=True).strip()

def main() -> None:
    if os.environ.get('GITHUB_REF_NAME') != BRANCH:
        raise RuntimeError('Publication is restricted to the new v22 revision branch')
    root = Path(git('rev-parse', '--show-toplevel'))
    os.chdir(root)
    paper = root / PREFIX
    report = json.loads((paper / 'validation/EXECUTION_REPORT.json').read_text())
    if report.get('passed') is not True or report['verified_source_files_after'] != 763:
        raise RuntimeError('Missing successful current execution report')
    if not report.get('referee_v21_rerun', {}).get('executed'):
        raise RuntimeError('Repository publication requires the actual pinned referee diagnostics')
    if report.get('assertions_total') != 171221 or report.get('pdf_pages') != 120:
        raise RuntimeError('Unexpected full validation count or PDF page count')
    if hashlib.sha256((paper / 'main.pdf').read_bytes()).hexdigest() != report['pdf_sha256']:
        raise RuntimeError('PDF changed after validation')
    subprocess.run(['python', 'manifest.py'], cwd=paper, check=True)
    git('merge-base', '--is-ancestor', '36910a7c6fd08e5ad2e8e10db7c2d8c71c463de8', 'HEAD')
    git('diff', '--exit-code', 'HEAD', '--', 'papers/A1-english-v21', 'reviews', '.github')
    original = git('rev-parse', 'HEAD')
    if original != os.environ['GITHUB_SHA']:
        raise RuntimeError('Workflow input commit mismatch')
    git('fetch', 'origin', BRANCH)
    if git('rev-parse', 'FETCH_HEAD') != original:
        raise RuntimeError('Revision branch advanced; refusing to overwrite concurrent work')
    receipt = {'version': 22, 'workflow_input_commit': original,
               'workflow_run_id': os.environ['GITHUB_RUN_ID'], 'branch': BRANCH,
               'validated_source_files': 763,
               'scope': 'Only the new v22 directory is staged. No old source, review, main or permissions are changed.'}
    (paper / 'validation/PUBLICATION_INPUT.json').write_text(json.dumps(receipt, indent=2) + '\n')
    manifest = json.loads((paper / 'SOURCE_MANIFEST.json').read_text())
    names = set(manifest['files'])
    names.update(('SOURCE_MANIFEST.json', 'main.pdf', 'BUILD_REPORT.json', 'PRESERVATION_REPORT.json'))
    for folder in ('build', 'validation'):
        names.update(p.relative_to(paper).as_posix() for p in (paper / folder).glob('*')
                     if p.is_file() and p.suffix in ('.tex', '.txt', '.json'))
    git('add', '-f', '--', *(PREFIX + name for name in sorted(names)))
    staged = git('diff', '--cached', '--name-only').splitlines()
    if not staged or any(not name.startswith(PREFIX) for name in staged):
        raise RuntimeError('Unexpected staged path outside the revision')
    git('config', 'user.name', 'github-actions[bot]')
    git('config', 'user.email', '41898282+github-actions[bot]@users.noreply.github.com')
    git('commit', '-m', 'A1 v22: publish prior-uniform multistep manuscript and executed referee diagnostics [skip ci]')
    git('push', 'origin', 'HEAD:refs/heads/' + BRANCH)
    print('Published v22 at', git('rev-parse', 'HEAD'))

if __name__ == '__main__':
    main()
