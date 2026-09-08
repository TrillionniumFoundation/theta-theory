#!/usr/bin/env python3
"""Verify the pinned v36 source manifest and rebuild both native volumes.

Usage: python reproduce_native.py --source-root PATH --work-root NEW_PATH
Requires the unmodified v36 native source closure, Python 3.10+, and pdflatex.
The working copy is separate; the input directory and Git repository are untouched.
This validates source identity and production, not mathematical correctness.
"""
from __future__ import annotations
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import sys

COMMIT = '8f074b8027627a71a81a362b9d15f47975e1f3ae'
PINNED = {
    'verification-v36/NATIVE_BUILD_V36.json': 'f4dbd653b585f0fa446d95653b247b3bffd14268',
    'verification-v35/NATIVE_BUILD_V35.json': '1e5f92cf41b563779ad702c85ee440a470a689fe',
    'v35/build_native.py': '66e5fa5a5fe7ba7c551b62bc38afb4c5951823a4',
    'v36/spectral_comparison.tex': '2fd691e92008175c072d04e17a5c7cc1fc79234d',
}

def blob(path: Path) -> str:
    data = path.read_bytes()
    return hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()

def require(ok: bool, message: str) -> None:
    if not ok:
        raise RuntimeError(message)

def verify(root: Path) -> dict:
    for name, sha in PINNED.items():
        require(blob(root/name) == sha, 'Pinned source mismatch: '+name)
    current = json.loads((root/'verification-v36/NATIVE_BUILD_V36.json').read_text())
    base = json.loads((root/'verification-v35/NATIVE_BUILD_V35.json').read_text())
    descriptor = current['source_manifest']
    expected = dict(base[descriptor['base_field']])
    for name in descriptor['delete']:
        expected.pop(name)
    expected.update(descriptor['replace_or_add'])
    require(len(expected) == current['source_count'] == 80, 'Source count mismatch')
    observed = {name: blob(root/name) for name in expected}
    require(observed == expected, 'Source bytes differ from the pinned manifest')
    spec = importlib.util.spec_from_file_location('native_builder', root/'v35/build_native.py')
    require(spec is not None and spec.loader is not None, 'Cannot load verified builder')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    active = module.sources(root, 'main') | module.sources(root, 'companions')
    require(active == set(expected), 'Entrypoint closure differs from published manifest')
    return {'reviewed_commit': COMMIT, 'pin_checks': PINNED,
        'source_count': len(expected), 'entrypoint_closure_matches': True,
        'all_sources_match_pinned_manifest': True, 'source_git_blob': observed,
        'identity_scope': 'All active bytes compared with the content-addressed manifest fetched from the pinned repository; four root objects directly checked against GitHub fetch responses.'}

def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--source-root', required=True, type=Path)
    ap.add_argument('--work-root', required=True, type=Path)
    args = ap.parse_args()
    source, work = args.source_root.resolve(), args.work_root.resolve()
    require(source.is_dir(), 'Missing source root')
    require(not work.exists(), 'Working directory must be new; refusing to overwrite')
    require(not work.is_relative_to(source), 'Working directory must be outside source')
    record = verify(source)
    shutil.copytree(source, work)
    (work/'SOURCE_IDENTITY.json').write_text(json.dumps(record, indent=2, sort_keys=True)+'\n')
    command = [sys.executable, str(work/'v35/build_native.py'), '--source-root', str(work),
        '--edition', 'v36-referee', '--source-commit', COMMIT]
    proc = subprocess.run(command, capture_output=True, text=True, timeout=180)
    (work/'REFEREE_BUILD_STDOUT.txt').write_text(proc.stdout+'\n'+proc.stderr)
    require(proc.returncode == 0, 'Native build failed; see REFEREE_BUILD_STDOUT.txt')
    receipt = json.loads((work/'verification-v36-referee/BUILD_RECEIPT.json').read_text())
    require(receipt['source_git_blob'] == record['source_git_blob'], 'Build source mismatch')
    require(receipt['recorder_source_inputs'] == sorted(record['source_git_blob']), 'Recorder mismatch')
    print(json.dumps({'source_count':80, 'status':receipt['status'],
        'passes':len(receipt['passes']), 'pdfs':receipt['pdfs'],
        'layout_warnings':receipt['layout_warnings'],
        'source_root_unchanged':verify(source)==record}, indent=2))

if __name__ == '__main__':
    main()
