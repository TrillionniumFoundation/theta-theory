#!/usr/bin/env python3
"""Reconstruct the reviewed v21 source exactly; never overwrite an existing revision.

The small transport is only a connector delivery format. The workflow commits
readable source, PDF and actual validation receipts to the new revision branch.
"""
from __future__ import annotations
import argparse
import base64
import hashlib
import json
import lzma
from pathlib import Path
import shutil
import subprocess
import sys

HERE = Path(__file__).resolve().parent
MANIFEST_BLOB = 'db8414e9ec13e862a7af091c89417fdd2aa6207d'
XZ_SHA256 = '210bc8939af09cb35e8f5b267bb01985be256c64852dcf305b36fd96459b2e75'
DELTA_SHA256 = 'f6a7cbbede8d507362d67fc2ff23496dc04b8b8b2a22f7be3f7fc8e59cebda3c'
SOURCE_SHA256 = '1b75e7bd6613a5c6edbe106c1572378b0cbf63a9c23d0a0d1aca28899a001d05'
ARCHIVE = ('main.tex', 'sections/introduction.tex', 'sections/exact_kernels.tex',
           'README.md', 'RESPONSE_TO_REFEREE.md', 'build.py', 'validate.py',
           'manifest.py', 'SOURCE_MANIFEST.json')

def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--root', type=Path, default=HERE.parents[1])
    args = parser.parse_args()
    root = args.root.resolve()
    base = root / 'papers/A1-english-v20'
    dest = root / 'papers/A1-english-v21'
    if dest.exists():
        raise RuntimeError('Refusing to replace an existing v21 directory')
    manifest_bytes = (base / 'SOURCE_MANIFEST.json').read_bytes()
    blob = hashlib.sha1(b'blob ' + str(len(manifest_bytes)).encode() + b'\0' + manifest_bytes).hexdigest()
    if blob != MANIFEST_BLOB:
        raise ValueError('Wrong independently pinned v20 source manifest')
    inherited = json.loads(manifest_bytes)['files']
    if len(inherited) != 729:
        raise ValueError('Unexpected baseline source count')
    for name, expected in inherited.items():
        if sha((base / name).read_bytes()) != expected:
            raise ValueError('Baseline differs: ' + name)
    encoded = ''.join((HERE / f'delta-{i:02d}.b64').read_text().strip() for i in range(1, 6))
    compressed = base64.b64decode(encoded, validate=True)
    if sha(compressed) != XZ_SHA256:
        raise ValueError('Transport checksum mismatch')
    raw = lzma.decompress(compressed)
    if sha(raw) != DELTA_SHA256:
        raise ValueError('Decoded source checksum mismatch')
    delta = json.loads(raw)
    if len(delta) != 18:
        raise ValueError('Unexpected delta file count')
    for name, text in delta.items():
        rel = Path(name)
        if rel.is_absolute() or '..' in rel.parts or not isinstance(text, str):
            raise ValueError('Unsafe source path or content')
    dest.mkdir(parents=True)
    for name in inherited:
        target = dest / name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(base / name, target)
    archive = dest / 'history/v20-editorial'
    archive.mkdir(parents=True, exist_ok=True)
    for name in ARCHIVE:
        shutil.copyfile(base / name, archive / name.replace('/', '__'))
    for name, text in delta.items():
        target = dest / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text, encoding='utf-8')
    subprocess.run([sys.executable, 'manifest.py', '--write'], cwd=dest, check=True)
    if sha((dest / 'SOURCE_MANIFEST.json').read_bytes()) != SOURCE_SHA256:
        raise ValueError('Materialized source differs from locally validated revision')
    validation = dest / 'validation'
    validation.mkdir()
    shutil.copyfile(HERE / 'LOCAL_VISUAL_INSPECTION.json', validation / 'VISUAL_INSPECTION.json')
    receipt = {'version': 21, 'source_files': 748, 'source_manifest_sha256': SOURCE_SHA256,
               'delta_sha256': DELTA_SHA256, 'compressed_transport_sha256': XZ_SHA256,
               'baseline_manifest_git_blob': MANIFEST_BLOB, 'passed': True,
               'scope': 'Exact delivery and source identity; no mathematical correctness claim.'}
    (validation / 'MATERIALIZATION_REPORT.json').write_text(json.dumps(receipt, indent=2) + '\n')
    print(json.dumps(receipt, indent=2))

if __name__ == '__main__':
    main()
