#!/usr/bin/env python3
"""Validate the frozen packet and create immutable Git objects only."""
from pathlib import Path
import base64
import hashlib
import json
import os
import shutil
import tempfile
import urllib.request
import zlib

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
OUT = REPO / 'v26-assembly-evidence'
OUT.mkdir(exist_ok=True)
BASE_TREE = '5c5378441102a155ccbf76f4b7f18d426390d3a9'
EXPECTED_TREE = '6101fe93f514d9586658d748e08a0ffd6c610044'
PACKET_SHA = '0d121b42676da526c691a1b762145ae8fc5818819d72aa14e1b872ca4a9e5f38'
PAYLOAD_SHA = 'b07c57358cec4c972f6253e7293e8336bc109ae224541c5f72ce900971a391a7'
EXCLUDED = {'build', 'evidence', '__pycache__'}


def require(ok, why):
    if not ok:
        raise RuntimeError(why)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def git_hash(kind, data):
    return hashlib.sha1(kind.encode() + b' ' + str(len(data)).encode() + b'\0' + data).digest()


def tree_hash(root):
    rows = []
    for path in root.iterdir():
        if path.name in EXCLUDED:
            continue
        require(not path.is_symlink(), 'symlink in source')
        if path.is_dir():
            mode, oid, key = '40000', tree_hash(path), path.name + '/'
        else:
            mode = '100755' if path.stat().st_mode & 0o111 else '100644'
            oid, key = git_hash('blob', path.read_bytes()), path.name
        rows.append((key, mode.encode() + b' ' + path.name.encode() + b'\0' + oid))
    return git_hash('tree', b''.join(value for _, value in sorted(rows)))


def ordinary(root):
    return {str(p.relative_to(root)): p for p in sorted(root.rglob('*'))
            if p.is_file() and not any(x in EXCLUDED for x in p.relative_to(root).parts)}


parts = {}
for index in range(1, 5):
    name = f'part{index}.b64'
    data = (HERE / name).read_bytes()
    (OUT / name).write_bytes(data)
    parts[name] = data
repair_file = HERE / 'repairs.json'
if repair_file.exists():
    repairs = json.loads(repair_file.read_text())
    for repair in repairs:
        name = repair['path']
        require(name in parts, 'repair outside transport')
        data = parts[name]
        require(digest(data) == repair['before_sha256'], 'unexpected transport input')
        previous = len(data) + 1
        for edit in reversed(repair['edits']):
            start, end = edit['start'], edit['end']
            require(0 <= start <= end < previous, 'invalid transport edit ordering')
            data = data[:start] + edit['text'].encode('ascii') + data[end:]
            previous = start
        require(digest(data) == repair['after_sha256'], 'transport repair differs')
        parts[name] = data
    shutil.copy2(repair_file, OUT / 'repairs.json')
encoded = ''.join(parts[f'part{i}.b64'].decode('ascii').strip() for i in range(1, 5))
packet = base64.b64decode(encoded, validate=True)
require(digest(packet) == PACKET_SHA, 'compressed packet checksum mismatch')
payload = zlib.decompress(packet)
require(digest(payload) == PAYLOAD_SHA, 'payload checksum mismatch')
obj = json.loads(payload)
require(len(obj['files']) == 15, 'unexpected file count')
base = REPO / 'papers/A2-DYN-v25-referee-response'
require(tree_hash(base).hex() == BASE_TREE, 'baseline tree differs')
with tempfile.TemporaryDirectory(prefix='a2-dyn-v26-') as td:
    root = Path(td) / 'paper'
    root.mkdir()
    for rel, path in ordinary(base).items():
        dest = root / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, dest)
    for rel, text in obj['files'].items():
        path = Path(rel)
        require(not path.is_absolute() and '..' not in path.parts, 'unsafe source path')
        dest = root / path
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(text, encoding='utf-8')
        dest.chmod(0o755 if rel == 'build.sh' else 0o644)
    ledger = json.loads((root / 'INHERITED_EDITS.json').read_text())
    print('ledger type:', type(ledger).__name__)
    edits = ledger if isinstance(ledger, list) else ledger['edits']
    for edit in edits:
        path = root / edit['path']
        text = path.read_text()
        before = edit.get('before', edit.get('old'))
        after = edit.get('after', edit.get('new'))
        require(isinstance(before, str) and isinstance(after, str), 'invalid exact edit')
        require(text.count(before) == 1, 'nonunique inherited edit')
        path.write_text(text.replace(before, after, 1))
    manifest = obj['manifest_header']
    manifest['baseline_sha256'] = {rel: digest(path.read_bytes()) for rel, path in ordinary(base).items()}
    manifest['source_sha256'] = {rel: digest(path.read_bytes()) for rel, path in ordinary(root).items()
                                 if rel != 'SOURCE_MANIFEST.json'}
    (root / 'SOURCE_MANIFEST.json').write_text(json.dumps(manifest, indent=2, sort_keys=True) + '\n')
    actual = tree_hash(root).hex()
    require(actual == EXPECTED_TREE, 'rebuilt ordinary paper tree differs: ' + actual)
    old_files = ordinary(base)
    entries = []
    for rel, path in ordinary(root).items():
        data = path.read_bytes()
        mode = '100755' if path.stat().st_mode & 0o111 else '100644'
        old = old_files.get(rel)
        if old is not None and old.read_bytes() == data and ((old.stat().st_mode & 0o111) != 0) == (mode == '100755'):
            continue
        entries.append({'path': rel, 'mode': mode, 'type': 'blob', 'content': data.decode('utf-8')})
    token = os.environ['GITHUB_TOKEN']
    url = 'https://api.github.com/repos/TrillionniumFoundation/theta-theory/git/trees'
    request = urllib.request.Request(url, data=json.dumps({'base_tree': BASE_TREE, 'tree': entries}).encode(),
        headers={'Authorization': 'Bearer ' + token, 'Accept': 'application/vnd.github+json',
                 'Content-Type': 'application/json', 'X-GitHub-Api-Version': '2022-11-28'}, method='POST')
    with urllib.request.urlopen(request, timeout=90) as response:
        result = json.load(response)
    require(result['sha'] == EXPECTED_TREE, 'remote immutable tree differs')
    receipt = {'event_sha': os.environ.get('GITHUB_SHA'), 'run_id': os.environ.get('GITHUB_RUN_ID'),
               'paper_tree': result['sha'], 'baseline_paper_tree': BASE_TREE,
               'packet_sha256': PACKET_SHA, 'payload_sha256': PAYLOAD_SHA,
               'ordinary_files': len(ordinary(root)), 'changed_tree_entries': len(entries),
               'created_commits': False, 'moved_refs': False, 'continuum_proof_certified': False}
    (OUT / 'assembly-receipt.json').write_text(json.dumps(receipt, indent=2, sort_keys=True) + '\n')
    print(json.dumps(receipt, indent=2, sort_keys=True))
