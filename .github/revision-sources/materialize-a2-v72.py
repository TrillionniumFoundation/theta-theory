#!/usr/bin/env python3
"""Materialize the reviewed A2 delta on the pinned v71 subtree; never delete history."""
from pathlib import Path
import base64
import hashlib
import lzma
import shutil
import subprocess

PREFIX = 'papers/A2-v17-boundary-information-coarsening'
OLD_TREE = '8549bb0789d5e6cdce8ae12f70ed7c100f81510b'
NEW_TREE = '78fb5bad4944d0bff60e108996cca84d4473fa85'
MANIFEST_BLOB = '2d3c18248e765200c88a7fc77891d8866a34501b'
XZ_HASH = '34b4b2eba6c631d2a44d46419563a001fdfae6efdf4eb156c0f96add5d677945'
PATCH_HASH = 'c3014ba9ddaea51e9e726ef3fac265a330664103737ee80b30b2f8428a304d89'
EDITED = ('README.md', 'main.tex', 'rigidity.tex', 'article/00i_main_thesis_v70.tex')

def require(ok, message):
    if not ok:
        raise RuntimeError(message)

def git(*args, data=None):
    return subprocess.run(['git', *args], input=data, check=True, capture_output=True).stdout

def main():
    require(git('rev-parse', 'HEAD:' + PREFIX).decode().strip() == OLD_TREE, 'Wrong source base')
    require(not git('status', '--porcelain', '--', PREFIX).strip(), 'Dirty manuscript base')
    parts = [Path('.github/revision-sources/a2-v72.delta.' + str(i)) for i in range(4)]
    raw = base64.b64decode(''.join(p.read_text().strip() for p in parts), validate=True)
    require(hashlib.sha256(raw).hexdigest() == XZ_HASH, 'Compressed delta integrity failure')
    patch = lzma.decompress(raw)
    require(len(patch) == 72702 and hashlib.sha256(patch).hexdigest() == PATCH_HASH, 'Delta integrity failure')
    records = git('apply', '--numstat', '-', data=patch).decode().splitlines()
    for row in records:
        added, removed, name = row.split('\t')
        require(name.startswith(PREFIX + '/') and '..' not in Path(name).parts, 'Out-of-scope delta')
        require(removed == '0' or name[len(PREFIX)+1:] in EDITED, 'Unexpected removal')
    git('apply', '--check', '--index', '-', data=patch)
    base = Path(PREFIX) / 'history/v71-review-baseline'
    require(not base.exists(), 'Historical baseline already exists')
    for name in EDITED:
        dest = base / name
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(Path(PREFIX) / name, dest)
    (base / 'SOURCE_MANIFEST.json').write_bytes(git('cat-file', 'blob', MANIFEST_BLOB))
    git('apply', '--index', '-', data=patch)
    git('add', '--', PREFIX)
    tree = git('write-tree').decode().strip()
    require(git('rev-parse', tree + ':' + PREFIX).decode().strip() == NEW_TREE, 'Materialized subtree mismatch')
    print('Verified complete A2 v72 manuscript subtree:', NEW_TREE)

if __name__ == '__main__':
    main()
