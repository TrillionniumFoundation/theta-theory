#!/usr/bin/env python3
"""Materialize the already-written, authenticated complete A2 v68 revision.

This applies a fixed payload. It is not a mathematical proof generator.
The complete reviewed and revised manuscript trees are checked exactly.
"""
from pathlib import Path
import base64
import hashlib
import json
import lzma
import subprocess

ROOT = Path(__file__).resolve().parents[2]
PREFIX = 'papers/A2-v17-boundary-information-coarsening'
P = ROOT / PREFIX
REVIEW = '2786efc1351e82f61a24ba4f827712e3e04ca39f'
BEFORE = '5ba7cc8f87aaadd2e3f734c41bb030668e15cff7'
AFTER = '23f07201ea4c6a33270cf4d4a977da1eddf8e8fe'
PAYLOAD_SHA = '9f7e68902a34531021bf965a8d1e005e33ee096f94efb1ea684f9864130c0b6c'
MANIFEST_SHA = '404deb66fc8f8cea6f081c51144650c0f8f6e714b8131cd75932f8cc59a3e4c4'


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
            'Manuscript is not the frozen v67 review baseline')
    require(not git('status', '--porcelain', '--untracked-files=all', '--', PREFIX),
            'Manuscript working tree is not clean')
    manifest = ROOT / 'deliveries/a2-v67/97b0c5bf15d6581c42b0f503bbe902c9d89b42db/frozen-source-manifest.json'
    raw_manifest = manifest.read_bytes()
    require(hashlib.sha256(raw_manifest).hexdigest() == MANIFEST_SHA,
            'Wrong reviewed frozen-source manifest')
    records = json.loads(raw_manifest)['files']
    require(len(records) == 855, 'Unexpected reviewed source inventory')
    here = Path(__file__).parent
    encoded = ''.join((here / ('a2-v68-payload-%02d.b64' % i)).read_text().strip()
                      for i in range(4))
    compressed = base64.b64decode(encoded, validate=True)
    require(hashlib.sha256(compressed).hexdigest() == PAYLOAD_SHA,
            'Revision payload hash mismatch')
    payload = json.loads(lzma.decompress(compressed))
    require(payload['revision'] == 68 and len(payload['files']) == 20,
            'Unexpected revision payload inventory')
    archive = P / 'history/v67-review-baseline'
    require(not archive.exists(), 'Refusing to overwrite a historical archive')
    pending, originals = {}, {}
    for name, rec in payload['files'].items():
        target = P / safe_path(name)
        if 'edits' in rec:
            old = target.read_bytes()
            require(hashlib.sha256(old).hexdigest() == rec['sha256'],
                    'Unexpected reviewed file: ' + name)
            require(name in records and rec['sha256'] == records[name]['sha256'],
                    'Edit does not match reviewed manifest: ' + name)
            lines = old.decode().splitlines(keepends=True)
            last = len(lines) + 1
            for start, stop, replacement in reversed(rec['edits']):
                require(0 <= start <= stop <= len(lines) and stop < last,
                        'Overlapping or invalid line edit: ' + name)
                lines[start:stop] = [replacement]
                last = start
            pending[name] = ''.join(lines).encode()
            originals[name] = old
        else:
            require(not target.exists(), 'Refusing to replace an unpinned file: ' + name)
            pending[name] = rec['content'].encode()
    require(len(originals) == 9, 'Unexpected edited-original inventory')
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
    previous = ROOT / 'README_PRE_V68.md'
    require(not previous.exists(), 'Refusing to overwrite the preceding root entry')
    previous.write_bytes((ROOT / 'README.md').read_bytes())
    (ROOT / 'README.md').write_text('''# Theta-Theory — A2 revision 68

**Boundary laws and smooth contact rigidity of periodic dispersing billiards** — Qian Qi.

The current revision is indexed in [A2_REVISION_V68_INDEX.md](A2_REVISION_V68_INDEX.md).
It answers the independent v67 report by extending the central relative-law/contact
mechanism to complete smooth contact germs, with finite-smoothness real-profile
stability and an actual equal-area flat family beyond all formal contact/action jets.
The closed v67 stopping correction and all inherited mathematical modules remain.

[Principal source](papers/A2-v17-boundary-information-coarsening/rigidity.tex) · [Full technical source](papers/A2-v17-boundary-information-coarsening/main.tex) · [Response to the referee](papers/A2-v17-boundary-information-coarsening/RESPONSE_TO_REFEREE_V68.md).

Source-matched native PDFs and completed publication identities are recorded in the
versioned delivery and final review-ready index after successful verification.
The previous root entry is preserved exactly in [README_PRE_V68.md](README_PRE_V68.md).
No default branch, review branch or A1 source is rewritten.
''')
    git('add', '--', 'README.md', 'README_PRE_V68.md')
    print(json.dumps({'review_head': REVIEW, 'before_manuscript_tree': BEFORE,
                      'after_manuscript_tree': AFTER,
                      'edited_originals_preserved': sorted(originals),
                      'new_mathematics_generated_by_script': False},
                     indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
