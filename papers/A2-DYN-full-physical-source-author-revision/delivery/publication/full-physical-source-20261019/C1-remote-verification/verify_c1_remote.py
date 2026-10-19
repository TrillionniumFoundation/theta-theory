#!/usr/bin/env python3
"""Independently verify saved actual C1 GitHub readbacks; no network or repo writes.

This implementation does not import the transport adapter. It reconstructs Git
trees directly from the saved remote entries and compares complete frozen local
identities. It does not claim to redownload every blob or verify a CI outcome.
"""
from pathlib import Path, PurePosixPath
from collections import defaultdict
from datetime import datetime, timezone
import hashlib
import json

HERE = Path(__file__).resolve().parent
INPUTS = HERE / 'inputs'
C1 = '694952d7d6b886d0087e8560da721bfc980adbc3'
PARENT = 'fdf2603c8bf422314f199fa431086485a0d1ebb5'
ARTICLE = 'f0e29499f0d5de75103b6f52cc464945071ea04b'
ROOT = '56031be3c69251f8eadce010b38d576eaf9497e6'
ARTICLE_NAME = 'A2-DYN-full-physical-source-author-revision'
WORKFLOW_NAME = 'a2-dyn-full-physical-source-20261019.yml'
PINS = {
    'C1_FINAL_REMOTE_READBACKS.json': 'd11252665c264b8188d0d87e151fdc912a9b0bcaf25ea174e3b694464d5bcd44',
    'C1_TRANSPORT_TO_PUBLISH.json': '4ac3cb80421872107489b5c48f9b48a79525ea38ae36741effe02bf7852c61ea',
    'C1_ROOT_EXPECTED.json': '022d1ab3e0afaebf34539dc012a5a97a752ac4746bf18193f51decb0fd202d25',
}


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


def read(name):
    data = (INPUTS / name).read_bytes()
    require(hashlib.sha256(data).hexdigest() == PINS[name], 'Changed evidence input: ' + name)
    return json.loads(data)


def canonical(entries):
    """Hash one Git tree using Git's directory-aware bytewise entry order."""
    contents = []
    seen = set()
    for entry in entries:
        name = entry['path']
        require(name not in seen and name not in ('', '.', '..') and
                '/' not in name and '\0' not in name, 'Invalid immediate tree child')
        seen.add(name)
        mode = str(entry['mode']).lstrip('0')
        require(mode in ('40000', '100644', '100755', '120000', '160000'), 'Invalid Git mode')
        sha = entry['sha']
        require(len(sha) == 40 and all(x in '0123456789abcdef' for x in sha), 'Invalid Git SHA')
        raw = name.encode('utf-8')
        sortkey = raw + (b'/' if mode == '40000' else b'')
        contents.append((sortkey, mode.encode('ascii') + b' ' + raw + b'\0' + bytes.fromhex(sha)))
    payload = b''.join(value for _, value in sorted(contents))
    return hashlib.sha1(b'tree ' + str(len(payload)).encode('ascii') + b'\0' + payload).hexdigest()


def signature(entry):
    return (entry['mode'], entry['type'], entry['sha'])


def indexed(entries):
    result = {entry['path']: entry for entry in entries}
    require(len(result) == len(entries), 'Duplicate tree path')
    return result


def main():
    started = datetime.now(timezone.utc).isoformat()
    saved = read('C1_FINAL_REMOTE_READBACKS.json')
    frozen = read('C1_TRANSPORT_TO_PUBLISH.json')
    planned = read('C1_ROOT_EXPECTED.json')
    observations = {row['key']: row for row in saved['readbacks']}
    require(len(observations) == len(saved['readbacks']) == 10, 'Incomplete/duplicate C1 observations')
    actual = {key: row['data'] for key, row in observations.items()}
    commit = actual['commit']
    require(commit['sha'] == C1 and commit['tree']['sha'] == ROOT,
            'Actual C1 commit/root mismatch')
    require([parent['sha'] for parent in commit['parents']] == [PARENT],
            'C1 does not have the exact sole authorized baseline parent')
    ref_checks = []
    for family in ('revision', 'referee-response', 'referee-copy'):
        branch = family + '/a2-dyn-full-physical-source-2026-10-19'
        obj = actual['ref:' + branch]
        require(obj['ref'] == 'refs/heads/' + branch and
                obj['object']['type'] == 'commit' and obj['object']['sha'] == C1,
                'New ref differs from actual C1: ' + branch)
        ref_checks.append({'ref': obj['ref'], 'commit': obj['object']['sha'], 'passed': True})

    remote = actual['article']
    require(remote['sha'] == ARTICLE and remote.get('truncated') is False,
            'Remote article tree is wrong or truncated')
    all_entries = indexed(remote['tree'])
    file_entries = {path: row for path, row in all_entries.items() if row['type'] == 'blob'}
    tree_entries = {path: row for path, row in all_entries.items() if row['type'] == 'tree'}
    require(len(file_entries) == 2688 and len(tree_entries) == 108 and len(all_entries) == 2796,
            'Unexpected complete recursive article cardinalities')
    require(len(file_entries) + len(tree_entries) == len(all_entries), 'Unexpected non-blob/tree article object')
    expected_files = indexed(frozen['files'])
    require(set(file_entries) == set(expected_files), 'Remote article file paths differ from frozen C1')
    file_checks = []
    for path in sorted(file_entries):
        row, expected = file_entries[path], expected_files[path]
        require(row['mode'] == expected['mode'] and row['sha'] == expected['sha'] and
                row['size'] == expected['bytes'], 'Remote mode/blob/size mismatch: ' + path)
        file_checks.append({'path': path, 'mode': row['mode'], 'git_blob': row['sha'],
                            'bytes': row['size'], 'frozen_sha256': expected['sha256'], 'passed': True})
    require(sum(row['size'] for row in file_entries.values()) == frozen['bytes'] == 285948269,
            'Full remote byte total mismatch')

    # Group the actual recursive response into actual immediate child trees.
    children = defaultdict(list)
    children[''] = []
    for path, row in all_entries.items():
        normalized = PurePosixPath(path)
        require(str(normalized) == path and not normalized.is_absolute() and
                all(part not in ('.', '..') for part in normalized.parts), 'Invalid recursive path')
        parent = normalized.parent.as_posix()
        if parent == '.':
            parent = ''
        require(parent == '' or parent in tree_entries, 'Missing remote directory ancestor')
        entry = dict(row, path=normalized.name)
        children[parent].append(entry)
        if row['type'] == 'tree':
            children.setdefault(path, [])
    require(set(children) == set(frozen['subtree_hashes']), 'Remote/frozen subtree path sets differ')
    subtree_checks = []
    for path in sorted(children):
        computed = canonical(children[path])
        remote_sha = ARTICLE if path == '' else tree_entries[path]['sha']
        require(computed == remote_sha == frozen['subtree_hashes'][path],
                'Canonical remote subtree mismatch: ' + path)
        subtree_checks.append({'path': path, 'children': len(children[path]),
                               'sha': computed, 'remote_and_frozen_match': True})
    require(len(subtree_checks) == 109 and canonical(children['']) == ARTICLE,
            'Article plus all 108 descendant trees were not reconstructed')

    root_checks, sibling_checks = [], []
    changed_expectation = {'root': {'.github', 'papers'}, 'papers': {ARTICLE_NAME},
                          'github': {'workflows'}, 'workflows': {WORKFLOW_NAME}}
    for kind in ('root', 'papers', 'github', 'workflows'):
        obj = actual[kind]
        require(obj.get('truncated') is False, 'Truncated actual control tree: ' + kind)
        rows = indexed(obj['tree'])
        desired = indexed(planned['expected_trees'][kind]['tree'])
        before = indexed(planned['base_trees'][kind]['tree'])
        expected_sha = planned['expected_tree_identities'][kind]
        require(canonical(obj['tree']) == obj['sha'] == expected_sha ==
                planned['expected_trees'][kind]['sha'], 'Control canonical tree mismatch: ' + kind)
        require(set(rows) == set(desired), 'Control path membership mismatch: ' + kind)
        for path in rows:
            require(signature(rows[path]) == signature(desired[path]),
                    'Control entry differs from planned C1: ' + kind + '/' + path)
        require(set(before) <= set(rows), 'Existing control entry deleted: ' + kind)
        changed = {path for path in set(before) | set(rows)
                   if path not in before or path not in rows or
                   signature(before[path]) != signature(rows[path])}
        require(changed == changed_expectation[kind], 'Unexpected sibling scope change: ' + kind)
        for path in sorted(before):
            unchanged = path not in changed
            if unchanged:
                require(signature(before[path]) == signature(rows[path]), 'Old sibling moved')
            sibling_checks.append({'tree': kind, 'path': path, 'old_sha': before[path]['sha'],
                                   'actual_sha': rows[path]['sha'], 'unchanged': unchanged,
                                   'authorized_pointer_change': not unchanged})
        root_checks.append({'tree': kind, 'canonical_sha': expected_sha,
                            'old_entries': len(before), 'actual_entries': len(rows),
                            'changed_or_added_entries': sorted(changed),
                            'all_other_entries_preserved': True})

    root_rows = indexed(actual['root']['tree'])
    paper_rows = indexed(actual['papers']['tree'])
    github_rows = indexed(actual['github']['tree'])
    workflow_rows = indexed(actual['workflows']['tree'])
    require(root_rows['papers']['sha'] == actual['papers']['sha'] and
            root_rows['.github']['sha'] == actual['github']['sha'] and
            github_rows['workflows']['sha'] == actual['workflows']['sha'] and
            paper_rows[ARTICLE_NAME]['sha'] == ARTICLE, 'Control-tree path linkage mismatch')
    workflow = workflow_rows[WORKFLOW_NAME]
    local_copy = file_entries['ci/' + WORKFLOW_NAME]
    require(signature(workflow) == signature(local_copy) and workflow['size'] == local_copy['size'] ==
            planned['workflow']['bytes'] and workflow['sha'] == planned['workflow']['sha'],
            'Remote dedicated workflow and article copy differ')
    require(frozen['article_tree_sha'] == ARTICLE and
            planned['expected_article_tree'] == ARTICLE and
            planned['expected_tree_identities']['root'] == ROOT, 'Frozen C1 linkage mismatch')

    runs = actual['runs']
    require(runs['total_count'] == 0 and runs['workflow_runs'] == [],
            'This fixed C1 readback was expected to record no observed run')
    result = {
        'started_utc': started, 'completed_utc': datetime.now(timezone.utc).isoformat(),
        'status': 'passed', 'scope': ('Independent local reconstruction of saved actual C1 '
            'GitHub commit/ref/tree responses. Every remote file mode/blob/size equals the '
            'frozen locally hashed bytes; all descendant/control trees reconstruct. This '
            'does not redownload every blob, certify continuous mathematics, or assert CI success.'),
        'c1_commit': C1, 'sole_parent_commit': PARENT, 'root_tree': ROOT, 'article_tree': ARTICLE,
        'readback_started_utc': saved['started'], 'readback_finished_utc': saved['finished'],
        'input_sha256_pins': PINS, 'verifier_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'file_count': 2688, 'bytes': 285948269, 'descendant_subtree_count': 108,
        'article_inclusive_canonical_tree_count': 109, 'recursive_entries': 2796,
        'remote_article_truncated': False, 'files_added_or_missing_against_frozen': [],
        'new_refs': ref_checks, 'control_trees': root_checks,
        'all_212_old_paper_entries_preserved': True, 'all_174_old_workflow_entries_preserved': True,
        'actual_c1_run_lookup': {'observed_at': saved['finished'], 'total_count': 0,
                                 'interpretation': 'No run observed at this readback; no CI success claim.'},
        'old_ref_movement_rechecked': False,
        'old_ref_scope': 'The three new refs only were read here; the full earlier branch census has its own scope.',
        'remote_operations_by_this_verifier': 'none', 'article_writes': 'none',
    }
    for name, value in [('C1_REMOTE_FILE_CHECKS.json', file_checks),
                        ('C1_REMOTE_SUBTREE_CHECKS.json', subtree_checks),
                        ('C1_REMOTE_SIBLING_CHECKS.json', sibling_checks),
                        ('C1_REMOTE_VERIFICATION_RECEIPT.json', result)]:
        (HERE / name).write_text(json.dumps(value, indent=2) + '\n')
    print(json.dumps(result))


if __name__ == '__main__':
    main()
