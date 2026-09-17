#!/usr/bin/env python3
"""Materialize the A2 v73 source on its pinned v72 subtree, preserving originals."""
from pathlib import Path
import base64
import hashlib
import lzma
import shutil
import subprocess

PREFIX = 'papers/A2-v17-boundary-information-coarsening'
OLD_TREE = '78fb5bad4944d0bff60e108996cca84d4473fa85'
NEW_TREE = '80996c207ce723e8d84068f4fe95172f5d18fa65'
XZ_HASH = 'ac70489da710163e1627c1c2ee291ed162b24717d1cd7ee11d50afc53fae2676'
PATCH_HASH = '396b02994a9f7024757785fa1a74112efbc538075635844aba70af534753f9a5'
EDITED = ('README.md', 'main.tex', 'rigidity.tex',
          'article/00i_main_thesis_v70.tex',
          'article/10g_uncalibrated_single_law_v72.tex',
          'journal/references_v56.tex', 'v5/references_v43.tex')

def require(ok, message):
    if not ok:
        raise RuntimeError(message)

def git(*args, data=None):
    return subprocess.run(['git', *args], input=data, check=True, capture_output=True).stdout

def main():
    require(git('rev-parse', 'HEAD:' + PREFIX).decode().strip() == OLD_TREE,
            'Wrong manuscript base')
    require(not git('status', '--porcelain', '--', PREFIX).strip(), 'Dirty manuscript base')
    parts = [Path('.github/revision-sources/a2-v73.delta.' + str(i)) for i in range(7)]
    raw = base64.b64decode(''.join(p.read_text().strip() for p in parts), validate=True)
    require(len(raw) == 28416 and hashlib.sha256(raw).hexdigest() == XZ_HASH,
            'Compressed delta integrity failure')
    patch = lzma.decompress(raw)
    require(len(patch) == 98173 and hashlib.sha256(patch).hexdigest() == PATCH_HASH,
            'Source delta integrity failure')
    for row in git('apply', '--numstat', '-', data=patch).decode().splitlines():
        added, removed, name = row.split('\t')
        require(name.startswith(PREFIX + '/') and '..' not in Path(name).parts,
                'Out-of-scope delta')
        require(removed == '0' or name[len(PREFIX)+1:] in EDITED,
                'Unexpected removal')
    git('apply', '--check', '--index', '-', data=patch)
    baseline = Path(PREFIX) / 'history/v72-review-baseline'
    require(not baseline.exists(), 'Historical baseline already exists')
    for name in EDITED:
        dest = baseline / name
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(Path(PREFIX) / name, dest)
    git('apply', '--index', '-', data=patch)
    # The preservation utility must also work below the repository root.
    verifier = Path(PREFIX) / 'tools/verify_preservation_v73.py'
    text = verifier.read_text()
    before = "git('ls-tree','-r','-z',OLD_TREE)"
    after = "git('ls-tree','--full-tree','-r','-z',OLD_TREE)"
    require(text.count(before) == 1, 'Unexpected preservation utility')
    verifier.write_text(text.replace(before, after))
    git('add', '--', PREFIX)
    tree = git('write-tree').decode().strip()
    require(git('rev-parse', tree + ':' + PREFIX).decode().strip() == NEW_TREE,
            'Materialized manuscript subtree mismatch')
    print('Verified complete A2 v73 manuscript subtree:', NEW_TREE)

if __name__ == '__main__':
    main()
