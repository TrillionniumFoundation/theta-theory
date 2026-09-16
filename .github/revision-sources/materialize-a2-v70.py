#!/usr/bin/env python3
"""Materialize the locally compiled v70 source delta, preserving the reviewed originals.

The three small transport blobs concatenate to one SHA-256-pinned gzip patch.
The resulting ordinary manuscript sources are committed before compilation.
No existing branch is force-updated and no manuscript path is removed.
"""
from __future__ import annotations
import gzip
import hashlib
import json
from pathlib import Path
import subprocess

PREFIX = 'papers/A2-v17-boundary-information-coarsening'
BASE_TREE = 'e0c2434849fe72a715cec1fae5e6e36bf90b5669'
TARGET_TREE = '63fdb25cd2002d9d2b3a238e7e7f1862b2328d2b'
BASE_SOURCE = '1a46fd69a508bccb90c6d2553892124f068f4657'
ORIGINALS = ('README.md', 'main.tex', 'rigidity.tex',
             'journal/00_principal_introduction_v61.tex',
             'article/00_structural_introduction_v48.tex')
PARTS = ('93b01f6def28ae817876dd732611bfb398980ba2',
         '5cba7e9ba6e0fad61ef779c05c6378a3dfcfb995',
         '44df0e8c06f77379868e0cbc1213fa830bc02ab3')


def require(ok: bool, message: str) -> None:
    if not ok:
        raise RuntimeError(message)


def git(*args: str, data: bytes | None = None) -> bytes:
    return subprocess.run(['git', *args], input=data, capture_output=True, check=True).stdout


def blob(data: bytes) -> str:
    return hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()


def main() -> None:
    require(git('rev-parse', 'HEAD:' + PREFIX).decode().strip() == BASE_TREE,
            'The reviewed manuscript tree differs; do not apply to an unreviewed baseline')
    require(not git('status', '--porcelain', '--', PREFIX), 'Dirty manuscript baseline')
    payloads = []
    for i, expected in enumerate(PARTS):
        data = Path(f'.github/revision-sources/a2-v70.delta.{i}').read_bytes()
        require(blob(data) == expected, 'Transport blob mismatch')
        payloads.append(data)
    packed = b''.join(payloads)
    require(hashlib.sha256(packed).hexdigest() ==
            'afb63f5f3bf90794d43bdd85b9b1b8ac1a5829779d5fe8f09400426baaf86cfb',
            'Source-delta digest mismatch')
    patch = gzip.decompress(packed)
    require(len(patch) == 79791, 'Unexpected source-delta length')
    git('apply', '--check', data=patch)
    manifest = git('show', 'HEAD:deliveries/a2-v69/' + BASE_SOURCE + '/frozen-source-manifest.json')
    require(hashlib.sha256(manifest).hexdigest() ==
            '7d2db47ec7f4be8e3a918151bcf8fe9b11f42614684eb95c50a162442c799a23',
            'Reviewed source manifest differs')
    records = json.loads(manifest)['files']
    require(len(records) == 895, 'Wrong baseline inventory')
    archive = Path(PREFIX) / 'history/v69-review-baseline'
    require(not archive.exists(), 'Historical archive already exists')
    for name in ORIGINALS:
        data = git('show', 'HEAD:' + PREFIX + '/' + name)
        require(blob(data) == records[name]['git_blob'], 'Reviewed original differs: ' + name)
        path = archive / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
        path.chmod(int(records[name]['mode'], 8) & 0o777)
    (archive / 'SOURCE_MANIFEST.json').write_bytes(manifest)
    (archive / 'SOURCE_MANIFEST.json').chmod(0o644)
    git('apply', data=patch)
    git('add', '--', PREFIX)
    index_tree = git('write-tree').decode().strip()
    target = git('rev-parse', index_tree + ':' + PREFIX).decode().strip()
    require(target == TARGET_TREE, 'Materialized tree differs from the clean locally compiled source: ' + target)
    print(json.dumps({'reviewed_tree': BASE_TREE, 'materialized_tree': target,
                      'archived_originals': list(ORIGINALS), 'baseline_paths': len(records)}, indent=2))


if __name__ == '__main__':
    main()
