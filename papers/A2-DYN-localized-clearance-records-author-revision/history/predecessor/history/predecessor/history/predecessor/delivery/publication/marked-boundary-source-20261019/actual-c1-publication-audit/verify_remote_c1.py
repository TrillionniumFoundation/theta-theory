#!/usr/bin/env python3
"""Verify only saved actual C1 GET responses and exact supplied inventories."""
from pathlib import Path
import collections
import datetime
import hashlib
import json

HERE = Path(__file__).resolve().parent
RAW = HERE / 'readbacks'
C1 = '409fc85c84a5f239d071b8452da48cb73694365f'
PARENT = '0933e9b44f5b0fd1d1a624d37ffd881d352496f8'
ROOT = '753cfd8589bc0b7c93942a727ed6925abc214bc2'
ARTICLE = '1c4fe72a8217c590568844d6d69f00e428193049'
ARTICLE_NAME = 'A2-DYN-marked-boundary-source-author-revision'
WORKFLOW = 'a2-dyn-marked-boundary-source-20261019.yml'
NEW_REFS = {
    'revision/a2-dyn-marked-boundary-source-2026-10-19',
    'referee-copy/a2-dyn-marked-boundary-source-2026-10-19',
    'referee-response/a2-dyn-marked-boundary-source-2026-10-19',
}


def read(name):
    return json.loads((RAW / (name + '.json')).read_text())


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def tree_hash(entries):
    def key(e):
        return (e['path'] + ('/' if e['type'] == 'tree' else '')).encode()
    raw = b''.join(
        e['mode'].lstrip('0').encode() + b' ' + e['path'].encode()
        + b'\0' + bytes.fromhex(e['sha'])
        for e in sorted(entries, key=key)
    )
    return hashlib.sha1(b'tree ' + str(len(raw)).encode() + b'\0' + raw).hexdigest()


def triple(e):
    return {k: e[k] for k in ('mode', 'type', 'sha')}


def tree_difference(parent, current):
    old = {e['path']: triple(e) for e in parent['tree']}
    new = {e['path']: triple(e) for e in current['tree']}
    return {
        'parent_sha': parent['sha'], 'current_sha': current['sha'],
        'parent_entries': len(old), 'current_entries': len(new),
        'added': {p: new[p] for p in sorted(new.keys() - old.keys())},
        'removed': {p: old[p] for p in sorted(old.keys() - new.keys())},
        'changed': {p: {'parent': old[p], 'current': new[p]}
                    for p in sorted(old.keys() & new.keys()) if old[p] != new[p]},
        'unchanged_count': sum(old[p] == new[p] for p in old.keys() & new.keys()),
        'parent_tree_reconstruction_pass': tree_hash(parent['tree']) == parent['sha'],
        'current_tree_reconstruction_pass': tree_hash(current['tree']) == current['sha'],
        'parent_truncated': parent.get('truncated'),
        'current_truncated': current.get('truncated'),
    }


started = datetime.datetime.now(datetime.timezone.utc).isoformat()
failures = []


def require(condition, description):
    if not condition:
        failures.append(description)


expected_path = HERE / 'inputs' / 'EXPECTED_FILE_IDENTITIES.json'
baseline_path = HERE / 'inputs' / 'BASELINE_ALL_BRANCHES_READBACK.json'
expected = json.loads(expected_path.read_text())
baseline = json.loads(baseline_path.read_text())
commit = read('c1_commit')
require(commit['sha'] == C1, 'Wrong commit identity')
require(commit['tree']['sha'] == ROOT, 'Wrong C1 root identity')
require([p['sha'] for p in commit['parents']] == [PARENT], 'Wrong C1 parent chain')
require(expected['root_tree_sha'] == ROOT and expected['article_tree_sha'] == ARTICLE,
        'Wrong supplied inventory identity')

article = read('article_recursive')
require(article['sha'] == ARTICLE and article.get('truncated') is False,
        'Wrong or truncated article tree response')
require(len(article['tree']) == len({e['path'] for e in article['tree']}),
        'Duplicate article tree paths')
blobs = {e['path']: e for e in article['tree'] if e['type'] == 'blob'}
expected_blobs = {e['path']: e for e in expected['files']}
file_mismatches = []
require(set(blobs) == set(expected_blobs), 'Article file path set mismatch')
for path, e in expected_blobs.items():
    a = blobs.get(path)
    if a is None or triple(a) != triple(e) or a['size'] != e['bytes']:
        file_mismatches.append({'path': path, 'expected': e, 'actual': a})
require(not file_mismatches and len(blobs) == 3586, 'Article file identities mismatch')

trees = {'': article['sha'], **{e['path']: e['sha'] for e in article['tree']
                               if e['type'] == 'tree'}}
require(set(trees) == set(expected['subtree_hashes']), 'Article subtree set mismatch')
children = collections.defaultdict(list)
for e in article['tree']:
    parent, _, name = e['path'].rpartition('/')
    children[parent].append({**e, 'path': name})
tree_checks = []
for path, wanted in expected['subtree_hashes'].items():
    actual = trees.get(path)
    rebuilt = tree_hash(children[path])
    tree_checks.append({'path': path, 'entries': len(children[path]),
                        'expected_sha': wanted, 'remote_sha': actual,
                        'recomputed_sha': rebuilt,
                        'matches': wanted == actual == rebuilt})
require(len(tree_checks) == 154 and all(x['matches'] for x in tree_checks),
        'Article reported or independently rebuilt tree identity mismatch')

differences = {level: tree_difference(read('parent_' + level), read('c1_' + level))
               for level in ('root', 'papers', 'github', 'workflows')}
for level, d in differences.items():
    require(d['parent_tree_reconstruction_pass'] and d['current_tree_reconstruction_pass'],
            'Immediate tree hash reconstruction failed: ' + level)
    require(d['parent_truncated'] is False and d['current_truncated'] is False,
            'Truncated immediate tree: ' + level)
    require(not d['removed'], 'Removed original immediate entry: ' + level)
require(set(differences['root']['changed']) == {'.github', 'papers'}
        and not differences['root']['added'], 'Unexpected root change')
require(set(differences['papers']['added']) == {ARTICLE_NAME}
        and not differences['papers']['changed'], 'Unrelated paper changed')
require(differences['papers']['added'].get(ARTICLE_NAME, {}).get('sha') == ARTICLE,
        'C1 article not linked from papers tree')
require(set(differences['github']['changed']) == {'workflows'}
        and not differences['github']['added'], 'Unrelated .github change')
require(set(differences['workflows']['added']) == {WORKFLOW}
        and not differences['workflows']['changed'], 'Unrelated workflow changed')

all_branches = []
page_counts = []
for page in range(1, 15):
    rows = read('branches_' + str(page))
    require(isinstance(rows, list), 'Invalid branch page ' + str(page))
    page_counts.append(len(rows))
    all_branches.extend(rows)
old = {e['name']: e['commit']['sha'] for e in baseline['branches']}
new = {e['name']: e['commit']['sha'] for e in all_branches}
missing_refs = sorted(old.keys() - new.keys())
changed_refs = {p: {'old': old[p], 'observed': new[p]} for p in old.keys() & new.keys()
                if old[p] != new[p]}
added_refs = {p: new[p] for p in sorted(new.keys() - old.keys())}
require(page_counts == [100] * 12 + [96, 0], 'Incomplete or unexpected pagination')
require(len(old) == 1293 and len(new) == len(all_branches) == 1296,
        'Unexpected or duplicate branch inventory')
require(not missing_refs and not changed_refs, 'Original branch deleted or changed')
require(set(added_refs) == NEW_REFS and set(added_refs.values()) == {C1},
        'Unexpected added branch or observed new head')
single_refs = {}
for name in ('author_ref', 'copy_ref', 'response_ref'):
    d = read(name)
    single_refs[d['ref']] = d['object']['sha']
require(set(single_refs) == {'refs/heads/' + x for x in NEW_REFS}
        and set(single_refs.values()) == {C1}, 'Individual ref readback mismatch')

raw_records = []
for request in sorted(RAW.glob('*.request.json')):
    metadata = json.loads(request.read_text())
    body = RAW / metadata['body_file']
    require(metadata['tool_isError'] is False, 'GET tool error: ' + request.name)
    raw_records.append({'request_file': request.name, 'request_sha256': sha256(request),
                        'body_file': body.name, 'body_bytes': body.stat().st_size,
                        'body_sha256': sha256(body), 'request_url': metadata['request_url'],
                        'requested_utc': metadata.get('requested_utc'),
                        'observed_utc': metadata.get('observed_utc')})
require(len(raw_records) == 27, 'Missing raw GET request or response record')

receipt = {
    'schema': 'A2-DYN-independent-C1-remote-preservation-v1',
    'status': 'passed' if not failures else 'failed',
    'started_utc': started,
    'finished_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'scope': 'Read-only audit of actual immutable C1 Git objects and observed branch heads; '
             'no scientific file, index, remote ref or workflow was mutated. '
             'Blob hashes/modes/lengths were compared; all remote blob bodies were not downloaded.',
    'commit': C1, 'root_tree': ROOT, 'article_tree': ARTICLE, 'parent_commit': PARENT,
    'program_sha256': sha256(Path(__file__).resolve()),
    'expected_inventory_sha256': sha256(expected_path),
    'baseline_inventory_sha256': sha256(baseline_path),
    'article_file_count': len(blobs),
    'article_blob_bytes': sum(e['size'] for e in blobs.values()),
    'article_files_mismatched': file_mismatches,
    'article_tree_checks_including_root': tree_checks,
    'immediate_tree_comparisons': differences,
    'branch_scope': 'GitHub branch refs (heads); the baseline is not a tags inventory.',
    'branch_page_counts': page_counts,
    'baseline_branch_count': len(old), 'observed_unique_branch_count': len(new),
    'missing_baseline_branches': missing_refs, 'changed_baseline_heads': changed_refs,
    'added_branches_as_observed': added_refs,
    'individual_ref_GETs_as_observed': single_refs,
    'moving_head_scope': 'These C1 head observations are not assertions about a later C2/C3 head. '
                         'C1 commit/tree objects remain the immutable audit target.',
    'raw_GET_records': raw_records,
    'timestamp_scope': 'First four actual GETs lacked per-call timestamps; their raw responses '
                       'are preserved and timestamps are null rather than fabricated.',
    'CI_completed_claimed': False, 'continuum_proof_certificate': False,
    'failures': failures,
}
(HERE / 'INDEPENDENT_C1_PUBLICATION_AUDIT.json').write_text(json.dumps(receipt, indent=2) + '\n')
(HERE / 'ALL_BRANCHES_AS_OBSERVED.json').write_text(json.dumps(all_branches, indent=2) + '\n')
(HERE / 'RAW_RESPONSE_MANIFEST.json').write_text(json.dumps(raw_records, indent=2) + '\n')
print(json.dumps({'status': receipt['status'], 'files': len(blobs), 'trees': len(tree_checks),
                  'old_refs_unchanged': len(old) - len(missing_refs) - len(changed_refs),
                  'new_refs': added_refs, 'failures': failures}))
if failures:
    raise SystemExit(1)
