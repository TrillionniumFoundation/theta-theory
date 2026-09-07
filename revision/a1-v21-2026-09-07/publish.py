#!/usr/bin/env python3
"""Publish only v21 outputs after an actual successful validation, without force."""
from __future__ import annotations
import json
import os
from pathlib import Path
import subprocess

BRANCH = 'revision/a1-english-v21-causal-transfer-and-proof-hierarchy-2026-09-07'
PREFIX = 'papers/A1-english-v21/'

def git(*args: str) -> str:
    return subprocess.check_output(['git', *args], text=True).strip()

def main() -> None:
    if os.environ.get('GITHUB_REF_NAME') != BRANCH:
        raise RuntimeError('Publication is restricted to the new v21 revision branch')
    root = Path(git('rev-parse', '--show-toplevel'))
    os.chdir(root)
    paper = root / PREFIX
    report = json.loads((paper / 'validation/EXECUTION_REPORT.json').read_text())
    if report.get('passed') is not True or report['verified_source_files_after'] != 748:
        raise RuntimeError('Missing successful current execution report')
    subprocess.run(['python', 'manifest.py'], cwd=paper, check=True)
    git('diff', '--exit-code', 'HEAD', '--', 'papers/A1-english-v20', 'reviews', '.github')
    original = git('rev-parse', 'HEAD')
    if original != os.environ['GITHUB_SHA']:
        raise RuntimeError('Workflow input commit mismatch')
    git('fetch', 'origin', BRANCH)
    if git('rev-parse', 'FETCH_HEAD') != original:
        raise RuntimeError('Revision branch advanced; refusing to overwrite concurrent work')
    receipt = {'version': 21, 'workflow_input_commit': original,
               'workflow_run_id': os.environ['GITHUB_RUN_ID'], 'branch': BRANCH,
               'validated_source_files': 748,
               'scope': 'Only the new v21 directory is staged. No old source, review, main or permissions are changed.'}
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
    git('commit', '-m', 'A1 v21: publish complete causal-transfer revision and executed validation [skip ci]')
    git('push', 'origin', 'HEAD:refs/heads/' + BRANCH)
    print('Published v21 at', git('rev-parse', 'HEAD'))

if __name__ == '__main__':
    main()
