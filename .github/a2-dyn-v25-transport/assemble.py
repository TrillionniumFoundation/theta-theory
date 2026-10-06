#!/usr/bin/env python3
"""Reconstruct a checksum-bound paper and create immutable Git objects only."""
from pathlib import Path
import base64
import gzip
import hashlib
import json
import os
import tempfile
import urllib.request

BASE_TREE = 'f15ab9854d022319db374f8ce38f4e6a4273dd84'
EXPECTED = '5c5378441102a155ccbf76f4b7f18d426390d3a9'
PACKET_SHA = 'c35bf9caead0d934262b47ad61bcd263dde24510b2cdae704f71c9a8117c4578'
REPORT = 'reviews/a2-dyn-v24-external-top4-review-2026-10-07/REFEREE_REPORT.md'
REPORT_BLOB = '9f58ef5d84b9e91d5eadd8d4a49317158db695e0'
SKIP = {'build', 'evidence', '__pycache__'}


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


def obj(kind, data):
    return hashlib.sha1(kind.encode()+b' '+str(len(data)).encode()+b'\0'+data).digest()


def ordinary(root):
    return [p for p in sorted(root.rglob('*')) if p.is_file()
            and not any(s in SKIP for s in p.relative_to(root).parts)]


def mode(p):
    return '100755' if p.stat().st_mode & 0o111 else '100644'


def tree_hash(root):
    rows = []
    for p in root.iterdir():
        if p.name in SKIP:
            continue
        require(not p.is_symlink(), 'symlink in source')
        if p.is_dir():
            m, sha, key = '40000', tree_hash(p), p.name+'/'
        else:
            m, sha, key = mode(p), obj('blob', p.read_bytes()), p.name
        rows.append((key, m.encode()+b' '+p.name.encode()+b'\0'+sha))
    return obj('tree', b''.join(row for _, row in sorted(rows)))


def sha256(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def assemble(repo, parts, target):
    compressed = base64.b64decode(''.join((parts/f'part{i:02d}.b64').read_text().strip()
                                         for i in range(1, 34)), validate=True)
    require(hashlib.sha256(compressed).hexdigest() == PACKET_SHA, 'transport checksum')
    packet = json.loads(gzip.decompress(compressed))
    require(packet['revision'] == 25 and packet['baseline_tree'] == BASE_TREE
            and packet['expected_tree'] == EXPECTED, 'packet identity')
    base = repo/'papers/A2-DYN-v24-referee-response'
    require(tree_hash(base).hex() == BASE_TREE, 'baseline ordinary tree')
    for p in ordinary(base):
        dest = target/p.relative_to(base)
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(p.read_bytes())
        dest.chmod(int(mode(p), 8))
    for rel, content in packet['files'].items():
        path = Path(rel)
        require(not path.is_absolute() and '..' not in path.parts, 'unsafe source path')
        dest = target/path
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(content, encoding='utf-8')
        require(packet['modes'][rel] in ('100644', '100755'), 'unsupported mode')
        dest.chmod(int(packet['modes'][rel], 8))
    ledger = json.loads((target/'INHERITED_EDITS.json').read_text())
    require(len(ledger['edits']) == 6, 'wrong edit count')
    source = (base/'main.tex').read_text()
    for edit in ledger['edits']:
        require(edit['path'] == 'main.tex' and source.count(edit['before']) == 1,
                'nonunique or out-of-scope inherited edit')
        source = source.replace(edit['before'], edit['after'], 1)
    (target/'main.tex').write_text(source, encoding='utf-8')
    manifest = packet['manifest_meta']
    manifest['baseline_sha256'] = {p.relative_to(base).as_posix(): sha256(p) for p in ordinary(base)}
    manifest['source_sha256'] = {p.relative_to(target).as_posix(): sha256(p) for p in ordinary(target)
                                 if p.name != 'SOURCE_MANIFEST.json'}
    (target/'SOURCE_MANIFEST.json').write_text(json.dumps(manifest, indent=2, sort_keys=True)+'\n')
    require(tree_hash(target).hex() == EXPECTED, 'reconstructed paper differs from validated tree')
    changes = []
    for p in ordinary(target):
        rel = p.relative_to(target).as_posix()
        old = base/rel
        if not old.exists() or p.read_bytes() != old.read_bytes() or mode(p) != mode(old):
            changes.append({'path': rel, 'mode': mode(p), 'type': 'blob', 'content': p.read_text()})
    require(len(ordinary(target)) == 127 and len(changes) == 17, 'unexpected source delta')
    return changes


def main():
    repo = Path(os.environ['GITHUB_WORKSPACE'])
    parts = Path(__file__).resolve().parent
    report = repo/REPORT
    require(obj('blob', report.read_bytes()).hex() == REPORT_BLOB, 'latest report identity')
    with tempfile.TemporaryDirectory(prefix='a2-dyn-v25-') as tmp:
        target = Path(tmp)/'paper'
        target.mkdir()
        changes = assemble(repo, parts, target)
        body = json.dumps({'base_tree': BASE_TREE, 'tree': changes}).encode()
        request = urllib.request.Request(
            'https://api.github.com/repos/'+os.environ['GITHUB_REPOSITORY']+'/git/trees',
            data=body, method='POST', headers={
                'Authorization': 'Bearer '+os.environ['GH_TOKEN'],
                'Accept': 'application/vnd.github+json', 'Content-Type': 'application/json',
                'X-GitHub-Api-Version': '2022-11-28'})
        with urllib.request.urlopen(request, timeout=90) as response:
            result = json.load(response)
        require(result['sha'] == EXPECTED, 'remote immutable tree differs')
        receipt = {'revision': 25, 'staging_sha': os.environ['GITHUB_SHA'],
                   'workflow_run_id': os.environ['GITHUB_RUN_ID'],
                   'paper_tree': result['sha'], 'expected_paper_tree': EXPECTED,
                   'baseline_paper_tree': BASE_TREE, 'packet_sha256': PACKET_SHA,
                   'controlling_report_blob': REPORT_BLOB, 'ordinary_source_files': 127,
                   'changed_or_new_files': len(changes),
                   'manifest_sha256': sha256(target/'SOURCE_MANIFEST.json'),
                   'commits_created': False, 'branch_refs_modified': False,
                   'continuum_proof_certified': False}
        (repo/'assembly-receipt.json').write_text(json.dumps(receipt, indent=2, sort_keys=True)+'\n')
        print(json.dumps(receipt, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
