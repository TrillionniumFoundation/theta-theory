#!/usr/bin/env python3
"""Replay an exact author-validated packet into unreferenced Git objects.

No commit, branch ref, manuscript baseline or unrelated file is changed.
This one-time transport script is removed in the final ordinary-source tree.
"""
from pathlib import Path, PurePosixPath
import base64
import hashlib
import json
import lzma
import os
import subprocess
import urllib.request

REPO = 'TrillionniumFoundation/theta-theory'
BASE = 'papers/A2-DYN-v14-referee-response'
TARGET = 'papers/A2-DYN-v15-referee-response'
BASE_TREE = '446d7989a1529dac4fc1034a56a324cb90fa3ddb'
EXPECTED_TREE = 'f0672475c063777e4abea0450874f4821320c4a1'
PAYLOAD_SHA = '21a467a1f6bc339ef4d3cfc2fd866a91665336adda4c69253955176440c5bd85'
ROOT = Path(__file__).resolve().parent


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


def git(*args):
    return subprocess.check_output(['git', *args])


def blob_hash(data):
    return hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()


def valid_path(path):
    p = PurePosixPath(path)
    require(not p.is_absolute() and '..' not in p.parts and str(p) == path,
            'unsafe packet path')


def post(resource, body):
    require(resource in ('blobs', 'trees'), 'write outside object creation')
    req = urllib.request.Request(
        'https://api.github.com/repos/' + REPO + '/git/' + resource,
        data=json.dumps(body).encode(), method='POST',
        headers={'Authorization': 'Bearer ' + os.environ['GH_TOKEN'],
                 'Accept': 'application/vnd.github+json',
                 'Content-Type': 'application/json',
                 'X-GitHub-Api-Version': '2022-11-28'})
    with urllib.request.urlopen(req, timeout=60) as response:
        return json.load(response)


require(os.environ['GITHUB_REPOSITORY'] == REPO, 'wrong repository')
require(os.environ['GITHUB_REF_NAME'] == 'revision/a2-dyn-v15-referee-response-2026-10-06',
        'wrong assembly branch')
head = git('rev-parse', 'HEAD').decode().strip()
require(head == os.environ['GITHUB_SHA'], 'not the event SHA')
require(git('rev-parse', 'HEAD:' + BASE).decode().strip() == BASE_TREE, 'changed baseline tree')
packed = base64.b64decode(''.join((ROOT / ('part%d.b64' % i)).read_text() for i in (1,2,3)), validate=True)
require(hashlib.sha256(packed).hexdigest() == PAYLOAD_SHA, 'transport checksum mismatch')
payload = json.loads(lzma.decompress(packed))
require(payload['revision'] == 15 and payload['baseline_tree'] == BASE_TREE
        and payload['expected_tree'] == EXPECTED_TREE
        and payload['baseline_directory'] == BASE and payload['target_directory'] == TARGET,
        'wrong source packet identity')

files, modes, old_shas = {}, {}, {}
for entry in git('ls-tree', '-r', '-z', 'HEAD:' + BASE).split(b'\0'):
    if not entry:
        continue
    meta, raw_path = entry.split(b'\t', 1)
    mode, kind, sha = meta.decode().split()
    path = raw_path.decode()
    valid_path(path)
    require(kind == 'blob' and mode in ('100644', '100755'), 'unexpected baseline entry')
    files[path] = git('cat-file', 'blob', sha)
    modes[path], old_shas[path] = mode, sha

for path, content in payload['files'].items():
    valid_path(path)
    files[path] = content.encode('utf-8')
    modes.setdefault(path, '100644')
ledger = json.loads(files['INHERITED_EDITS.json'])
require(ledger['baseline'] == payload['baseline_commit'], 'wrong edit baseline')
for edit in ledger['edits']:
    path = edit['path']
    valid_path(path)
    require(path in old_shas, 'edit is not inherited')
    text = files[path].decode('utf-8')
    require(text.count(edit['before']) == 1, 'edit is not an exact unique replacement: ' + path)
    files[path] = text.replace(edit['before'], edit['after'], 1).encode('utf-8')

require(set(files) == set(payload['hashes']), 'packet adds or omits an undeclared source')
for path, data in files.items():
    require(hashlib.sha256(data).hexdigest() == payload['hashes'][path],
            'replayed source differs from the validated author file: ' + path)
manifest = json.loads(files['SOURCE_MANIFEST.json'])
require(set(manifest['source_sha256']) == set(files) - {'SOURCE_MANIFEST.json'}, 'incomplete manifest')
for path, expected in manifest['source_sha256'].items():
    require(hashlib.sha256(files[path]).hexdigest() == expected, 'manifest mismatch')

entries, changed = [], {}
for path in sorted(files):
    sha = blob_hash(files[path])
    if old_shas.get(path) == sha:
        continue
    result = post('blobs', {'encoding': 'base64',
                           'content': base64.b64encode(files[path]).decode()})
    require(result['sha'] == sha, 'created blob identity differs')
    changed[path] = sha
    entries.append({'path': path, 'mode': modes[path], 'type': 'blob', 'sha': sha})
result = post('trees', {'base_tree': BASE_TREE, 'tree': entries})
require(result['sha'] == EXPECTED_TREE, 'assembled tree is not the locally validated tree')
receipt = {'revision':15, 'event_sha':head, 'workflow_run_id':os.environ['GITHUB_RUN_ID'],
           'payload_sha256':PAYLOAD_SHA, 'baseline_tree':BASE_TREE,
           'paper_tree':result['sha'], 'files_checked':len(files),
           'edit_operations':len(ledger['edits']), 'created_blobs':changed,
           'commits_created':False, 'branch_refs_changed':False,
           'continuum_proof_certified':False}
out = Path('.v15-assembly')
out.mkdir(exist_ok=True)
(out / 'assembly-receipt.json').write_text(json.dumps(receipt, indent=2, sort_keys=True) + '\n')
print(json.dumps(receipt, indent=2, sort_keys=True))
