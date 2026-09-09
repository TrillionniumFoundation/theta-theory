#!/usr/bin/env python3
"""Restore the exact A2 v9 manuscript and optionally reproduce its two PDFs.

The complete text payload is committed under .publication/a2-v9. All
117 original text files are SHA-256 checked before writing. No file outside
this manuscript directory is changed. The original packet's historical
publication status is preserved, not rewritten retrospectively.
"""
from __future__ import annotations
import argparse
import base64
import hashlib
import json
import lzma
from pathlib import Path, PurePosixPath
import subprocess
import sys

PAPER = Path(__file__).resolve().parent
TRANSPORT = PAPER.parents[1] / '.publication' / 'a2-v9'
XZ_SHA256 = 'ef947b9ee98acd7348d4e6d3b76a8d9f0384e63a9ea062afd30f30d48fff9a91'
JSON_SHA256 = 'eeba93cc4d5e0bc4f03d7dd2604bcdc13e62fd885b6cb8fe8195f3b367e687d0'


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def git_blob(data: bytes) -> str:
    return hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--build', action='store_true', help='Run the original clean LaTeX build after restoration')
    parser.add_argument('--verify', action='store_true', help='Run both original finite diagnostic suites after restoration')
    args = parser.parse_args()
    packed = base64.b64decode(''.join((TRANSPORT / f'chunk-{i:02d}.b64').read_text().strip() for i in range(8)), validate=True)
    require(sha256(packed) == XZ_SHA256, 'Compressed transport SHA-256 mismatch')
    raw = lzma.decompress(packed)
    require(sha256(raw) == JSON_SHA256, 'Decoded payload SHA-256 mismatch')
    payload = json.loads(raw)
    require(len(payload['reuse']) == 82 and len(payload['text']) == 35 and len(payload['binary']) == 2, 'Unexpected payload inventory')
    require(set(payload['reuse']) | set(payload['text']) | set(payload['binary']) == set(payload['hashes']), 'Manifest inventory mismatch')
    restored = {}
    for name, expected in payload['hashes'].items():
        if name in payload['binary']:
            continue
        path = PurePosixPath(name)
        require(not path.is_absolute() and '..' not in path.parts and '\\' not in name, 'Unsafe source path')
        if name in payload['text']:
            data = payload['text'][name].encode('utf-8')
        else:
            source = TRANSPORT / 'reuse' / name
            require(source.is_file() and not source.is_symlink(), 'Missing original source: ' + name)
            data = source.read_bytes()
            require(git_blob(data) == payload['reuse'][name], 'Inherited Git blob mismatch: ' + name)
        require(sha256(data) == expected, 'Original source digest mismatch: ' + name)
        restored[name] = data
    require(len(restored) == 117, 'Incomplete native-source inventory')
    for name, data in restored.items():
        destination = PAPER / name
        require(PAPER.resolve() in destination.resolve().parents, 'Destination escapes manuscript directory')
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(data)
    print('Restored and verified all 117 original text files, without content changes.')
    if args.verify:
        for script in ('verify_v9.py', 'verify_revision.py'):
            subprocess.run([sys.executable, str(PAPER / 'tools' / script)], cwd=PAPER, check=True)
    if args.build:
        subprocess.run([sys.executable, str(PAPER / 'tools' / 'build.py')], cwd=PAPER, check=True)
        for name, spec in payload['binary'].items():
            data = (PAPER / name).read_bytes()
            require(sha256(data) == spec['sha256'] and git_blob(data) == spec['git_blob'], 'Rebuilt PDF differs from delivered original: ' + name)
        print('Both rebuilt PDFs are byte-identical to the delivered originals.')


if __name__ == '__main__':
    main()
