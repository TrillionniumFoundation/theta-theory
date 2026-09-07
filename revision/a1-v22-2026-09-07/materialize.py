#!/usr/bin/env python3
"""Reconstruct the prepared v22 source exactly; never overwrite an existing revision.

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
MANIFEST_BLOB = '14d877c7db051926fe461ccfbe007093a786e860'
XZ_SHA256 = '80f54c5cdc8cba63aec2b4f1056b474402bd621ab848c4f7e976d73424097efc'
DELTA_SHA256 = '7a565af5caf1e4cf16a7cc30e296101ecefb4991921f975b05d1bde2b9a9d2b4'
SOURCE_SHA256 = '785e6b35e53474bdce973693c0dd76ca4912e45937e0c705c16f11b5c503bc8e'
ARCHIVE = ('main.tex', 'sections/introduction.tex', 'README.md', 'RESPONSE_TO_REFEREE.md', 'build.py', 'validate.py',
           'manifest.py', 'SOURCE_MANIFEST.json')

def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--root', type=Path, default=HERE.parents[1])
    args = parser.parse_args()
    root = args.root.resolve()
    base = root / 'papers/A1-english-v21'
    dest = root / 'papers/A1-english-v22'
    if dest.exists():
        raise RuntimeError('Refusing to replace an existing v22 directory')
    manifest_bytes = (base / 'SOURCE_MANIFEST.json').read_bytes()
    blob = hashlib.sha1(b'blob ' + str(len(manifest_bytes)).encode() + b'\0' + manifest_bytes).hexdigest()
    if blob != MANIFEST_BLOB:
        raise ValueError('Wrong independently pinned v21 source manifest')
    inherited = json.loads(manifest_bytes)['files']
    if len(inherited) != 748:
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
    if len(delta) != 14:
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
    archive = dest / 'history/v21-editorial'
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
    receipt = {'version': 22, 'source_files': 763, 'source_manifest_sha256': SOURCE_SHA256,
               'delta_sha256': DELTA_SHA256, 'compressed_transport_sha256': XZ_SHA256,
               'baseline_manifest_git_blob': MANIFEST_BLOB, 'passed': True,
               'scope': 'Exact delivery and source identity; no mathematical correctness claim.'}
    (validation / 'MATERIALIZATION_REPORT.json').write_text(json.dumps(receipt, indent=2) + '\n')
    print(json.dumps(receipt, indent=2))

if __name__ == '__main__':
    main()
