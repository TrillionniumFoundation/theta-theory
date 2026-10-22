#!/usr/bin/env python3
"""Verify saved actual C2 objects against its staged inventory and sealed C1."""
from pathlib import Path
import collections
import datetime
import hashlib
import json

HERE = Path(__file__).resolve().parent
RAW = HERE / 'readbacks'
PREVIOUS = HERE / 'inputs' / 'immutable-c1-readbacks'
C1 = '409fc85c84a5f239d071b8452da48cb73694365f'
C2 = 'efde9fa6c45e7835989b653622a9870e59027530'
ROOT = 'b5d618b8a4b356f8ca07f1c9f1238e35d879ede8'
ARTICLE = 'b4add0580cc8211223dfa57e6e618e2bf9546d09'
ARTICLE_NAME = 'A2-DYN-marked-boundary-source-author-revision'
ARCHIVE = 'delivery/publication/marked-boundary-source-20261019/c1-ref-creation/'
MODIFIED = {'PUBLICATION_RECEIPT.json', 'PUBLICATION_STATUS.json', 'REMOTE_TRANSPORT_STATUS.md'}
REFS = {'refs/heads/' + p + '/a2-dyn-marked-boundary-source-2026-10-19'
        for p in ('revision', 'referee-copy', 'referee-response')}


def read(name, directory=RAW):
    return json.loads((directory / (name + '.json')).read_text())


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def entry(e):
    return {k: e[k] for k in ('mode', 'type', 'sha')}


def tree_hash(entries):
    raw = b''.join(
        e['mode'].lstrip('0').encode() + b' ' + e['path'].encode()
        + b'\0' + bytes.fromhex(e['sha'])
        for e in sorted(entries, key=lambda x: (x['path'] + ('/' if x['type'] == 'tree' else '')).encode())
    )
    return hashlib.sha1(b'tree ' + str(len(raw)).encode() + b'\0' + raw).hexdigest()


started = datetime.datetime.now(datetime.timezone.utc).isoformat()
failures = []


def require(condition, description):
    if not condition:
        failures.append(description)


expected_path = HERE / 'inputs' / 'EXPECTED_FILE_IDENTITIES.json'
expected = json.loads(expected_path.read_text())
commit = read('c2_commit')
require(commit['sha'] == C2 and commit['tree']['sha'] == ROOT, 'Wrong C2 commit/root')
require([p['sha'] for p in commit['parents']] == [C1], 'C2 is not a direct successor of C1')
require(expected['root_tree_sha'] == ROOT and expected['article_tree_sha'] == ARTICLE,
        'Wrong expected C2 inventory identity')
a = read('article_recursive')
old_a = read('article_recursive', PREVIOUS)
require(a['sha'] == ARTICLE and a.get('truncated') is False, 'Wrong/truncated C2 article tree')
require(len(a['tree']) == len({e['path'] for e in a['tree']}), 'Duplicate C2 paths')
files = {e['path']: e for e in a['tree'] if e['type'] == 'blob'}
old_files = {e['path']: e for e in old_a['tree'] if e['type'] == 'blob'}
wanted = {e['path']: e for e in expected['files']}
require(set(files) == set(wanted) and len(files) == 3596, 'C2 file path set mismatch')
file_mismatches = []
for p, e in wanted.items():
    actual = files.get(p)
    if actual is None or entry(actual) != entry(e) or actual['size'] != e['bytes']:
        file_mismatches.append({'path': p, 'expected': e, 'actual': actual})
require(not file_mismatches, 'C2 file identity mismatch')
trees = {'': a['sha'], **{e['path']: e['sha'] for e in a['tree'] if e['type'] == 'tree'}}
require(set(trees) == set(expected['subtree_hashes']), 'C2 subtree path set mismatch')
children = collections.defaultdict(list)
for e in a['tree']:
    parent, _, name = e['path'].rpartition('/')
    children[parent].append({**e, 'path': name})
tree_checks = []
for p, expected_sha in expected['subtree_hashes'].items():
    rebuilt = tree_hash(children[p])
    tree_checks.append({'path': p, 'expected_sha': expected_sha,
                        'remote_sha': trees.get(p), 'recomputed_sha': rebuilt,
                        'matches': expected_sha == trees.get(p) == rebuilt})
require(len(tree_checks) == 156 and all(e['matches'] for e in tree_checks),
        'C2 subtree identity/reconstruction failed')

changes = []
for p in sorted(set(old_files) | set(files)):
    old, new = old_files.get(p), files.get(p)
    if old is None:
        changes.append({'path': p, 'status': 'added', 'new': entry(new)})
    elif new is None:
        changes.append({'path': p, 'status': 'deleted', 'old': entry(old)})
    elif entry(old) != entry(new) or old['size'] != new['size']:
        changes.append({'path': p, 'status': 'modified', 'old': entry(old), 'new': entry(new)})
require(len(changes) == 13, 'Unexpected C1-to-C2 changed-file count')
require({x['path'] for x in changes if x['status'] == 'modified'} == MODIFIED,
        'Modified file outside allowed publication metadata')
added = [x for x in changes if x['status'] == 'added']
require(len(added) == 10 and all(x['path'].startswith(ARCHIVE) for x in added),
        'Unexpected new evidence path')
require(not any(x['status'] == 'deleted' for x in changes), 'C1 file deleted')
old_metadata_retention = []
for p in sorted(MODIFIED):
    archived = files.get(ARCHIVE + 'prepublication-metadata/' + p)
    matched = archived is not None and entry(archived) == entry(old_files[p])
    old_metadata_retention.append({'original': p, 'archived': ARCHIVE + 'prepublication-metadata/' + p,
                                   'original_blob': old_files[p]['sha'], 'matches': matched})
require(all(x['matches'] for x in old_metadata_retention), 'Original publication metadata not retained')

def math_path(p):
    q = Path(p)
    return (len(q.parts) == 1 and q.suffix == '.tex') or (
        len(q.parts) == 2 and ((q.parts[0] == 'core' and q.suffix == '.tex')
                              or (q.parts[0] == 'tools' and q.suffix == '.py')))


old_math = {p for p in old_files if math_path(p)}
new_math = {p for p in files if math_path(p)}
require(old_math == new_math and len(old_math) == 107, 'Mathematical source set changed')
math_checks = [{'path': p, 'c1_blob': old_files[p]['sha'], 'c2_blob': files[p]['sha'],
                'matches': entry(old_files[p]) == entry(files[p])} for p in sorted(old_math)]
require(all(x['matches'] for x in math_checks), 'Mathematical source byte identity changed')

isolation = {}
for level, allowed in [('root', {'papers'}), ('papers', {ARTICLE_NAME})]:
    old = read('c1_' + level, PREVIOUS)
    new = read('c2_' + level)
    d0 = {x['path']: entry(x) for x in old['tree']}
    d1 = {x['path']: entry(x) for x in new['tree']}
    changed = {p: {'c1': d0[p], 'c2': d1[p]} for p in d0.keys() & d1.keys() if d0[p] != d1[p]}
    isolation[level] = {'c1_tree': old['sha'], 'c2_tree': new['sha'],
                        'c1_entries': len(d0), 'c2_entries': len(d1), 'changed': changed,
                        'unchanged_count': sum(d0[p] == d1[p] for p in d0.keys() & d1.keys()),
                        'c1_recomputed': tree_hash(old['tree']), 'c2_recomputed': tree_hash(new['tree'])}
    require(set(d0) == set(d1) and set(changed) == allowed, 'Unrelated change at ' + level)
    require(tree_hash(old['tree']) == old['sha'] and tree_hash(new['tree']) == new['sha'],
            'Immediate tree reconstruction failed at ' + level)
    require(old.get('truncated') is False and new.get('truncated') is False, 'Truncated ' + level)
old_root = read('c1_root', PREVIOUS)
new_root = read('c2_root')
old_github = next(x for x in old_root['tree'] if x['path'] == '.github')
new_github = next(x for x in new_root['tree'] if x['path'] == '.github')
require(entry(old_github) == entry(new_github), '.github/workflow subtree changed')
workflow = next(x for x in read('c1_workflows', PREVIOUS)['tree']
                if x['path'] == 'a2-dyn-marked-boundary-source-20261019.yml')

refs = {}
for name in ('author_ref', 'copy_ref', 'response_ref'):
    x = read(name)
    refs[x['ref']] = x['object']['sha']
require(set(refs) == REFS and set(refs.values()) == {C2}, 'Observed C2 head mismatch')
raw_records = []
for p in sorted(RAW.glob('*.request.json')):
    x = json.loads(p.read_text())
    body = RAW / x['body_file']
    require(x['tool_isError'] is False, 'GET error: ' + p.name)
    raw_records.append({'request_file': p.name, 'request_sha256': sha256(p),
                        'body_file': body.name, 'body_bytes': body.stat().st_size,
                        'body_sha256': sha256(body), 'url': x['request_url'],
                        'requested_utc': x['requested_utc'], 'observed_utc': x['observed_utc']})
require(len(raw_records) == 7, 'Missing actual C2 GET record')

receipt = {
    'schema': 'A2-DYN-independent-C2-remote-preservation-v1',
    'status': 'passed' if not failures else 'failed', 'started_utc': started,
    'finished_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'scope': 'Actual immutable C2 objects, exact staged inventory, evidence-only delta to C1, '
             'and moving heads as observed. No remote or scientific-source mutation.',
    'commit': C2, 'root_tree': ROOT, 'article_tree': ARTICLE, 'sole_parent': C1,
    'expected_inventory_sha256': sha256(expected_path), 'program_sha256': sha256(Path(__file__)),
    'file_count': len(files), 'article_blob_bytes': sum(x['size'] for x in files.values()),
    'file_identity_mismatches': file_mismatches,
    'tree_checks_including_root': tree_checks,
    'exact_C1_to_C2_file_changes': changes,
    'original_modified_metadata_retained': old_metadata_retention,
    'mathematical_source_checks': math_checks,
    'inherited_frozen_mathematical_fingerprint': 'ee0bd027bf5b4263ea5c6eebfb8ffe2d24c8fa0b21d1187f0967bfcaf0a221a5',
    'fingerprint_scope': 'All 107 constituent mathematical source blobs remain identical to '
                         'the independently checked C1 source; no new source hash is invented.',
    'unrelated_tree_isolation': isolation,
    'github_tree_unchanged': entry(old_github) == entry(new_github),
    'unchanged_workflow_blob': workflow['sha'],
    'three_refs_as_observed': refs,
    'ref_scope': 'No repeat of all 1293 baseline heads in this C2 audit; the C1 census remains '
                 'its own timed record. Future C3 heads require a fresh final readback.',
    'raw_GET_records': raw_records,
    'CI_success_claimed': False, 'continuum_proof_certificate': False,
    'failures': failures,
}
(HERE / 'INDEPENDENT_C2_PUBLICATION_AUDIT.json').write_text(json.dumps(receipt, indent=2) + '\n')
(HERE / 'RAW_RESPONSE_MANIFEST.json').write_text(json.dumps(raw_records, indent=2) + '\n')
print(json.dumps({'status': receipt['status'], 'files': len(files), 'trees': len(tree_checks),
                  'file_changes': len(changes), 'unchanged_math_sources': len(math_checks),
                  'workflow_unchanged': receipt['github_tree_unchanged'], 'failures': failures}))
if failures:
    raise SystemExit(1)
