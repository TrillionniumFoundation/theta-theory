#!/usr/bin/env python3
"""Materialize the byte-anchored A1 v15 source, preserving the complete v14.

The four binary parts are only a transport encoding of a JSON text delta.
No content from the packet is executed. Every old and new text byte is
checked before validation; the expanded readable manuscript is committed
by the associated workflow. This script never alters the baseline/reviews.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import lzma
from pathlib import Path
import re
import shutil
import subprocess
import sys

BASIS = 'ffb9214b0fc7e218d6183c1f81bccb3e47587421'
REVIEW = '3d58bb33ae122ebb2430874e2a57a5863e6a876a'
OLD_MANIFEST_BLOB = 'c7995cd0073733257d85f0520e1f889dbe034335'
INPUT_SHA = 'df4fb8b61335c052f90c3690b8dd5e3d585098c7fae47eb2f4a42d024272933e'
NEW_MANIFEST_SHA = '26e4a3f59d1439e900f6d29ed67eae68260996a10879653576ecf581d7a89f49'
PRESERVATION_SHA = 'b65812a92ba7fafec8c42fdf9efff9d544a2d78169be2c5a39e68d618e87ac64'
HISTORY = [
    'BUILD_REPORT.json', 'HISTORICAL_DERIVATION_MAP.md',
    'LITERATURE_VERIFICATION.md', 'NUMERICAL_EVIDENCE.md',
    'PRESERVATION_REPORT.json', 'PROOF_LEDGER.md', 'README.md',
    'RESPONSE_TO_REFEREE.md', 'SOURCE_MANIFEST.json', 'VISUAL_INSPECTION.md',
    'build.py', 'introduction.tex', 'main.tex', 'manifest.py', 'validate.py',
]


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def checked_path(root: Path, name: str) -> Path:
    rel = Path(name)
    require(not rel.is_absolute() and '..' not in rel.parts,
            'Unsafe packet path: ' + name)
    target = root / rel
    require(target.resolve().is_relative_to(root.resolve()), 'Path escapes source')
    return target


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repository', type=Path, default=Path.cwd())
    args = parser.parse_args()
    repo = args.repository.resolve()
    old = repo / 'papers/A1-english-v14'
    new = repo / 'papers/A1-english-v15'
    require(old.is_dir(), 'Pinned v14 source directory is absent')
    require(not new.exists(), 'Refusing to overwrite an existing v15 directory')
    old_bytes = (old / 'SOURCE_MANIFEST.json').read_bytes()
    git_blob = hashlib.sha1(b'blob ' + str(len(old_bytes)).encode() + b'\0' + old_bytes).hexdigest()
    require(git_blob == OLD_MANIFEST_BLOB, 'Wrong v14 source-manifest identity')
    old_manifest = json.loads(old_bytes)
    require(len(old_manifest['files']) == 80, 'Unexpected old source count')
    for name, sha in old_manifest['files'].items():
        require(digest(checked_path(old, name).read_bytes()) == sha,
                'Pinned source mismatch: ' + name)

    input_dir = repo / '.github/scripts/a1-v15-inputs'
    packed = b''.join((input_dir / f'part-{i:02d}.xz').read_bytes() for i in range(1, 5))
    require(digest(packed) == INPUT_SHA, 'Input packet hash mismatch')
    payload = json.loads(lzma.decompress(packed))
    require(payload['basis'] == BASIS and payload['review'] == REVIEW, 'Wrong revision anchors')
    require(payload['source_manifest_sha256'] == NEW_MANIFEST_SHA, 'Wrong new manifest anchor')
    require(payload['preservation_manifest_sha256'] == PRESERVATION_SHA, 'Wrong preservation anchor')
    require(len(payload['files']) == 18, 'Unexpected delta file count')

    shutil.copytree(old, new, ignore=shutil.ignore_patterns('__pycache__', 'build', '.git'))
    shutil.rmtree(new / 'validation', ignore_errors=True)
    (new / 'validation').mkdir()
    for suffix in ('pdf', 'aux', 'log', 'out', 'toc'):
        (new / ('main.' + suffix)).unlink(missing_ok=True)
    (new / 'history').mkdir(exist_ok=True)
    for name in HISTORY:
        source = old / ('sections/introduction.tex' if name == 'introduction.tex' else name)
        shutil.copyfile(source, new / 'history' / ('V14_' + name))

    # Expand the original main file with the original builder before applying edits.
    subprocess.run([sys.executable, 'build.py', '--prepare-only'], cwd=new, check=True)
    expanded = (new / 'build/expanded.tex').read_text(encoding='utf-8')
    proofs = re.findall(r'\\begin\{proof\}.*?\\end\{proof\}', expanded, re.S)
    statements = [m.group() for m in re.finditer(
        r'\\begin\{(theorem|lemma|proposition|corollary)\}.*?\\end\{\1\}', expanded, re.S)]
    require(len(proofs) == 77 and len(statements) == 80, 'Wrong v14 complete-block count')
    preservation = {
        'version': 14, 'submission_commit': BASIS, 'source_manifest_git_blob': OLD_MANIFEST_BLOB,
        'scope': 'Complete expanded v14 proofs and named statements, not mathematical verification.',
        'proof_sha256': [digest(s.encode()) for s in proofs],
        'statement_sha256': [digest(s.encode()) for s in statements],
        'named_results': re.findall(r'\\label\{((?:thm|lem|cor|prop):[^}]+)\}', expanded),
    }
    preservation_bytes = (json.dumps(preservation, indent=2) + '\n').encode()
    require(digest(preservation_bytes) == PRESERVATION_SHA, 'Expanded v14 block hashes differ')
    (new / 'V14_PRESERVATION_MANIFEST.json').write_bytes(preservation_bytes)

    for name, item in payload['files'].items():
        target = checked_path(new, name)
        target.parent.mkdir(parents=True, exist_ok=True)
        if item['mode'] == 'replace':
            result = item['text'].encode('utf-8')
        elif item['mode'] == 'edit':
            before = target.read_bytes()
            require(digest(before) == item['before_sha256'], 'Wrong delta baseline: ' + name)
            lines = before.decode('utf-8').splitlines(keepends=True)
            original_length = len(lines)
            previous = -1
            for edit in item['edits']:
                require(0 <= edit['start'] <= edit['end'] <= original_length,
                        'Invalid edit range: ' + name)
                require(edit['start'] >= previous, 'Overlapping/unsorted edits: ' + name)
                previous = edit['end']
            for edit in reversed(item['edits']):
                lines[edit['start']:edit['end']] = edit['text'].splitlines(keepends=True)
            result = ''.join(lines).encode('utf-8')
        else:
            raise ValueError('Unknown delta mode')
        require(digest(result) == item['sha256'], 'New source hash mismatch: ' + name)
        target.write_bytes(result)

    subprocess.run([sys.executable, 'manifest.py', '--write'], cwd=new, check=True)
    new_bytes = (new / 'SOURCE_MANIFEST.json').read_bytes()
    require(digest(new_bytes) == NEW_MANIFEST_SHA,
            'Expanded source differs from the locally validated 100-file source')
    require(len(json.loads(new_bytes)['files']) == 100, 'Unexpected current source count')
    for name, sha in old_manifest['files'].items():
        require(digest(checked_path(old, name).read_bytes()) == sha, 'Baseline was altered')
    receipt = {
        'basis': BASIS, 'controlling_review': REVIEW, 'input_sha256': INPUT_SHA,
        'input_delta_files': len(payload['files']), 'old_source_files_verified': 80,
        'new_source_files_verified': 100, 'source_manifest_sha256': NEW_MANIFEST_SHA,
        'retained_complete_v14_proofs': len(proofs),
        'retained_complete_v14_statements': len(statements),
        'baseline_unchanged': True,
        'scope': 'Source identity and materialization, not mathematical proof verification.',
    }
    (new / 'validation/PREPARATION_REPORT.json').write_text(json.dumps(receipt, indent=2) + '\n')
    print(json.dumps(receipt, indent=2))


if __name__ == '__main__':
    main()
