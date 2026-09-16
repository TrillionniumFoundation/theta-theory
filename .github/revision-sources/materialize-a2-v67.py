#!/usr/bin/env python3
"""Apply the already-written, source-pinned v67 manuscript revision.

This verifies both the reviewed and final complete manuscript trees. It is
not a proof generator. Every mathematical edit is in the committed payload.
"""
from pathlib import Path
import base64
import hashlib
import json
import lzma
import os
import subprocess

ROOT = Path(__file__).resolve().parents[2]
PREFIX = 'papers/A2-v17-boundary-information-coarsening'
P = ROOT / PREFIX
BASE = '3d49684cc6c9bad36d80c99dc46af276f53fae18'
BEFORE = 'c693d717577dc5f501f2a86ec937cfa36bf6ce4e'
AFTER = '5ba7cc8f87aaadd2e3f734c41bb030668e15cff7'
PAYLOAD_SHA = 'b35b719d04e0936229341b61f05f5a9683839b93027556f6f8a628019bbba152'
MANIFEST_SHA = 'ce41d6eec5d2000c9e2180f8f3a8334995bf6377c8a8a4167b78f08be7599dda'


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


def git(*args):
    return subprocess.check_output(['git', *args], cwd=ROOT).decode().strip()


def safe_path(name):
    q = Path(name)
    require(not q.is_absolute() and '..' not in q.parts and '\\' not in name,
            'Unsafe payload path: ' + name)
    return q


def main():
    require(git('rev-parse', 'HEAD:' + PREFIX) == BEFORE,
            'The manuscript is not the frozen v66 review baseline')
    require(not git('status', '--porcelain', '--', PREFIX),
            'Manuscript working tree is not clean')
    manifest = ROOT / 'deliveries/a2-v66/38f798a9b28237420f070a032d3601f0bee72cde/frozen-source-manifest.json'
    raw_manifest = manifest.read_bytes()
    require(hashlib.sha256(raw_manifest).hexdigest() == MANIFEST_SHA,
            'Wrong v66 frozen manifest')
    records = json.loads(raw_manifest)['files']
    here = Path(__file__).parent
    encoded = ''.join((here / ('a2-v67-payload-%02d.b64' % i)).read_text().strip()
                      for i in range(3))
    compressed = base64.b64decode(encoded, validate=True)
    require(hashlib.sha256(compressed).hexdigest() == PAYLOAD_SHA,
            'Revision payload hash mismatch')
    payload = json.loads(lzma.decompress(compressed))
    require(payload['revision'] == 67 and len(payload['files']) == 17,
            'Unexpected revision payload')
    archive = P / 'history/v66-review-baseline'
    require(not archive.exists(), 'Refusing to overwrite a historical archive')
    pending, originals = {}, {}
    for name, rec in payload['files'].items():
        target = P / safe_path(name)
        if 'edits' in rec:
            old = target.read_bytes()
            require(hashlib.sha256(old).hexdigest() == rec['sha256'],
                    'Unexpected reviewed file: ' + name)
            require(name in records and rec['sha256'] == records[name]['sha256'],
                    'Edit does not match the reviewed manifest: ' + name)
            lines = old.decode().splitlines(keepends=True)
            last = len(lines) + 1
            for start, stop, replacement in reversed(rec['edits']):
                require(0 <= start <= stop <= len(lines) and stop < last,
                        'Overlapping or invalid edit: ' + name)
                lines[start:stop] = [replacement]
                last = start
            pending[name] = ''.join(lines).encode()
            originals[name] = old
        else:
            require(not target.exists(), 'Refusing to replace an unpinned file: ' + name)
            pending[name] = rec['content'].encode()
    require(len(originals) == 8, 'Unexpected edited-original count')
    archive.mkdir(parents=True)
    (archive / 'SOURCE_MANIFEST.json').write_bytes(raw_manifest)
    for name, old in originals.items():
        target = archive / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(old)
        target.chmod(int(records[name]['mode'], 8) & 0o777)
    for name, data in pending.items():
        target = P / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
        target.chmod(int(payload['files'][name]['mode'], 8))
    git('add', '--', PREFIX)
    index_tree = git('write-tree')
    require(git('rev-parse', index_tree + ':' + PREFIX) == AFTER,
            'Complete revised manuscript tree mismatch')
    previous = ROOT / 'README_PRE_V67.md'
    require(not previous.exists(), 'Refusing to overwrite the preceding root entry')
    previous.write_bytes((ROOT / 'README.md').read_bytes())
    (ROOT / 'README.md').write_text('''# Theta-Theory — A2 revision 67

**Boundary laws and rigidity of periodic dispersing billiards** — Qian Qi.

The current revision is indexed in [A2_REVISION_V67_INDEX.md](A2_REVISION_V67_INDEX.md).
It answers the v66 report with a proved residual stopping criterion and the
complete propagation of curvature error through the signed finite-jet inverse.
The opening states the relative physical law and actual contact reconstruction
as one mechanism. Global exact identification without candidate closeness,
the complete local analytic inverse, and the distinct weaker-data and charged
observation models retain their full stated conclusions and detailed proofs.

[Principal source](papers/A2-v17-boundary-information-coarsening/rigidity.tex) · [Full technical source](papers/A2-v17-boundary-information-coarsening/main.tex) · [Response to the referee](papers/A2-v17-boundary-information-coarsening/RESPONSE_TO_REFEREE_V67.md).

The previous root entry is preserved exactly in [README_PRE_V67.md](README_PRE_V67.md).
Source-matched PDFs and actual native publication identities are recorded in the
versioned delivery and final review-ready index after successful verification.
No default branch, review branch or A1 source is rewritten.
''')
    git('add', '--', 'README.md', 'README_PRE_V67.md')
    print(json.dumps({'review_head': BASE, 'before_manuscript_tree': BEFORE,
                      'after_manuscript_tree': AFTER,
                      'edited_originals_preserved': sorted(originals),
                      'new_mathematics_generated_by_script': False},
                     indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
