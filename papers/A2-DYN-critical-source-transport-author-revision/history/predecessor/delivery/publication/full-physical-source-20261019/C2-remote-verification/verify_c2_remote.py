#!/usr/bin/env python3
"""Independently verify saved actual C2 GitHub readbacks; no network or repo writes.

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
C2 = '228ec6a639d4d195a1a8b869a04dae6f49fece0e'
PARENT = '694952d7d6b886d0087e8560da721bfc980adbc3'
ARTICLE = '826219579509e91c87c8dfb0c6348e2c42dba178'
ROOT = '431dfd86fcd60e50a1469af38343afc470527752'
ARTICLE_NAME = 'A2-DYN-full-physical-source-author-revision'
WORKFLOW_NAME = 'a2-dyn-full-physical-source-20261019.yml'
PINS = {'C2_INITIAL_REMOTE_READBACKS.json': 'b5a290fdd88cdb574af8b4e5c58f51d274a4c8a7e535a30d14465773c556b789', 'C2_FILE_IDENTITIES.json': 'd969e7a145e1fa9320433dacc7ba0fd7129a39cb2b91933d91d926997e42faf1', 'C2_ROOT_EXPECTED.json': '6765f04c6bcdcceafc10e347662f55531fada47ee83d5d490b9e79171ccd8381', 'C1_FINAL_REMOTE_READBACKS.json': 'd11252665c264b8188d0d87e151fdc912a9b0bcaf25ea174e3b694464d5bcd44', 'C1_TRANSPORT_TO_PUBLISH.json': '4ac3cb80421872107489b5c48f9b48a79525ea38ae36741effe02bf7852c61ea', 'SOURCE_MANIFEST.json': '13182b20479bcafcd8a3d53804b9cc610739e5a8ad0fb94f32eed65b4768f997'}

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
    saved = read('C2_INITIAL_REMOTE_READBACKS.json')
    frozen = read('C2_FILE_IDENTITIES.json')
    planned = read('C2_ROOT_EXPECTED.json')
    observations = {row['key']: row for row in saved['readbacks']}
    require(len(observations) == len(saved['readbacks']) == 10, 'Incomplete/duplicate C2 observations')
    actual = {key: row['data'] for key, row in observations.items()}
    commit = actual['commit']
    require(commit['sha'] == C2 and commit['tree']['sha'] == ROOT,
            'Actual C2 commit/root mismatch')
    require([parent['sha'] for parent in commit['parents']] == [PARENT],
            'C2 does not have the exact sole authorized baseline parent')
    ref_checks = []
    for family in ('revision', 'referee-response', 'referee-copy'):
        branch = family + '/a2-dyn-full-physical-source-2026-10-19'
        obj = actual['ref:' + branch]
        require(obj['ref'] == 'refs/heads/' + branch and
                obj['object']['type'] == 'commit' and obj['object']['sha'] == C2,
                'New ref differs from actual C2: ' + branch)
        ref_checks.append({'ref': obj['ref'], 'commit': obj['object']['sha'], 'passed': True})

    remote = actual['article']
    require(remote['sha'] == ARTICLE and remote.get('truncated') is False,
            'Remote article tree is wrong or truncated')
    all_entries = indexed(remote['tree'])
    file_entries = {path: row for path, row in all_entries.items() if row['type'] == 'blob'}
    tree_entries = {path: row for path, row in all_entries.items() if row['type'] == 'tree'}
    require(len(file_entries) == 2710 and len(tree_entries) == 113 and len(all_entries) == 2823,
            'Unexpected complete recursive article cardinalities')
    require(len(file_entries) + len(tree_entries) == len(all_entries), 'Unexpected non-blob/tree article object')
    expected_files = indexed(frozen['files'])
    require(set(file_entries) == set(expected_files), 'Remote article file paths differ from frozen C2')
    file_checks = []
    for path in sorted(file_entries):
        row, expected = file_entries[path], expected_files[path]
        require(row['mode'] == expected['mode'] and row['sha'] == expected['sha'] and
                row['size'] == expected['bytes'], 'Remote mode/blob/size mismatch: ' + path)
        file_checks.append({'path': path, 'mode': row['mode'], 'git_blob': row['sha'],
                            'bytes': row['size'], 'frozen_sha256': expected['sha256'], 'passed': True})
    require(sum(row['size'] for row in file_entries.values()) == frozen['bytes'] == 292904889,
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
    require(len(subtree_checks) == 114 and canonical(children['']) == ARTICLE,
            'Article plus all 113 descendant trees were not reconstructed')

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
                    'Control entry differs from planned C2: ' + kind + '/' + path)
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
            planned['expected_tree_identities']['root'] == ROOT, 'Frozen C2 linkage mismatch')

    # Independently constrain the actual C1 -> C2 delta, beyond the original
    # fdf-baseline sibling comparison above.
    prior_frozen = read('C1_TRANSPORT_TO_PUBLISH.json')
    prior_saved = read('C1_FINAL_REMOTE_READBACKS.json')
    prior_actual = {row['key']: row['data'] for row in prior_saved['readbacks']}
    require(prior_actual['commit']['sha'] == PARENT and
            prior_frozen['article_tree_sha'] == prior_actual['article']['sha'] ==
            'f0e29499f0d5de75103b6f52cc464945071ea04b', 'Actual C1 predecessor mismatch')
    previous = indexed(prior_frozen['files'])
    previous_remote = indexed([row for row in prior_actual['article']['tree']
                               if row['type'] == 'blob'])
    require(prior_actual['article'].get('truncated') is False and
            set(previous_remote) == set(previous), 'Incomplete actual C1 predecessor file set')
    for path, row in previous.items():
        old_remote = previous_remote[path]
        require(old_remote['sha'] == row['sha'] and old_remote['mode'] == row['mode'] and
                old_remote['size'] == row['bytes'], 'Actual C1 predecessor file mismatch')
    require(set(previous) <= set(expected_files), 'C2 removes a C1 file')
    modified = sorted(path for path in previous if any(
        previous[path][key] != expected_files[path][key]
        for key in ('sha', 'mode', 'bytes', 'sha256')))
    allowed_modified = {'PUBLICATION_STATUS.json', 'PUBLICATION_RECEIPT.json',
                        'REMOTE_TRANSPORT_STATUS.md'}
    require(set(modified) == allowed_modified, 'Existing C1 bytes changed beyond the exact three metadata files')
    added = sorted(set(expected_files) - set(previous))
    allowed_prefixes = ('delivery/publication/full-physical-source-20261019/',
                        'evidence/current-execution/full-physical-publication-source/')
    require(len(added) == 22 and all(path.startswith(allowed_prefixes) for path in added),
            'C2 additions differ from the 22 authorized publication/source-gate files')
    c1_control_changes = {'root': {'papers'}, 'papers': {ARTICLE_NAME},
                          'github': set(), 'workflows': set()}
    since_c1 = []
    for kind in ('root', 'papers', 'github', 'workflows'):
        prior_rows = indexed(prior_actual[kind]['tree'])
        current_rows = indexed(actual[kind]['tree'])
        require(canonical(prior_actual[kind]['tree']) == prior_actual[kind]['sha'],
                'C1 actual control hash reconstruction failed')
        require(set(prior_rows) == set(current_rows), 'C2 changes a control-tree entry set')
        changed = {path for path in prior_rows
                   if signature(prior_rows[path]) != signature(current_rows[path])}
        require(changed == c1_control_changes[kind], 'Unexpected C1-to-C2 sibling movement')
        since_c1.append({'tree': kind, 'old_sha': prior_actual[kind]['sha'],
                         'new_sha': actual[kind]['sha'], 'entries': len(current_rows),
                         'changed_pointer_entries': sorted(changed),
                         'all_other_entries_unchanged': True})

    manifest = read('SOURCE_MANIFEST.json')
    manifest_bytes = (INPUTS / 'SOURCE_MANIFEST.json').read_bytes()
    manifest_blob = hashlib.sha1(b'blob ' + str(len(manifest_bytes)).encode() +
                                 b'\0' + manifest_bytes).hexdigest()
    require(previous['SOURCE_MANIFEST.json']['sha'] ==
            expected_files['SOURCE_MANIFEST.json']['sha'] == manifest_blob and
            previous['SOURCE_MANIFEST.json']['sha256'] ==
            expected_files['SOURCE_MANIFEST.json']['sha256'] == PINS['SOURCE_MANIFEST.json'],
            'Pinned source manifest does not match both actual carriers')
    require(allowed_modified <= set(manifest['excluded_root_files']),
            'The three mutable publication files are not explicitly manifest-excluded')
    manifest_rows = indexed(manifest['files'])
    require(len(manifest_rows) == manifest['source_count'] == 1668 and
            sum(row['bytes'] for row in manifest_rows.values()) ==
            manifest['source_bytes'] == 122736124, 'Frozen input count/size mismatch')
    frozen_checks = []
    for path, row in sorted(manifest_rows.items()):
        require(path in previous and path in expected_files, 'Frozen source input missing')
        for carrier in (previous, expected_files):
            require(carrier[path]['sha'] == row['git_blob'] and
                    carrier[path]['sha256'] == row['sha256'] and
                    carrier[path]['bytes'] == row['bytes'], 'Frozen source identity changed: ' + path)
        require(previous[path]['mode'] == expected_files[path]['mode'], 'Frozen source mode changed')
        frozen_checks.append({'path': path, 'git_blob': row['git_blob'],
                              'sha256': row['sha256'], 'bytes': row['bytes'], 'unchanged': True})
    closure = manifest['native_tex_closure']
    require(len(closure['active_core_files']) == 56 and
            closure['active_core_start'] == 260 and closure['active_core_end'] == 315 and
            set(closure['reachable_tex_files']) <= set(manifest_rows),
            'Frozen native 260--315 source closure is incomplete')

    def mathematical_fingerprint(carrier):
        paths = []
        for path in carrier:
            p = PurePosixPath(path)
            parts = p.parts
            if ((len(parts) == 1 and p.suffix == '.tex') or
                (len(parts) == 2 and parts[0] == 'core' and p.suffix == '.tex') or
                (len(parts) == 2 and parts[0] == 'tools' and p.suffix == '.py')):
                paths.append(path)
        require(set(paths) <= set(manifest_rows), 'Mathematical fingerprint path is not frozen')
        records = [{'path': path, 'sha256': carrier[path]['sha256']} for path in sorted(paths)]
        return hashlib.sha256(json.dumps(records, sort_keys=True).encode()).hexdigest(), records

    old_fingerprint, old_math_rows = mathematical_fingerprint(previous)
    new_fingerprint, new_math_rows = mathematical_fingerprint(expected_files)
    require(len(new_math_rows) == 101 and old_math_rows == new_math_rows and
            old_fingerprint == new_fingerprint ==
            'ebe48d08b94fc0dceecce96ecef8e0bc81d91918521ee1ba24558d549d558b26',
            'Exact 101-file mathematical source fingerprint changed')
    delta = {'sole_parent': PARENT, 'modified_existing_paths': modified,
             'added_paths': added, 'added_count': 22, 'removed_paths': [],
             'allowed_added_prefixes': list(allowed_prefixes),
             'all_three_changed_root_files_explicitly_manifest_excluded': True,
             'frozen_input_count': 1668, 'frozen_input_bytes': 122736124,
             'frozen_input_identities_and_modes_unchanged': True,
             'manifest_sha256': PINS['SOURCE_MANIFEST.json'],
             'native_core_count': 56, 'native_core_range': [260, 315],
             'mathematical_fingerprint_file_count': 101,
             'mathematical_source_sha256_before': old_fingerprint,
             'mathematical_source_sha256_after': new_fingerprint,
             'c1_to_c2_control_trees': since_c1}
    runs = actual['runs']
    require(runs['total_count'] == 1 and len(runs['workflow_runs']) == 1,
            'Unexpected fixed C2 run lookup')
    run = runs['workflow_runs'][0]
    require(run['id'] == 39229329979 and run['head_sha'] == C2 and
            run['head_branch'] == 'revision/a2-dyn-full-physical-source-2026-10-19' and
            run['path'] == '.github/workflows/' + WORKFLOW_NAME and
            run['status'] == 'in_progress' and run['conclusion'] is None,
            'Actual C2 initial run identity/status differs from saved observation')
    result = {
        'started_utc': started, 'completed_utc': datetime.now(timezone.utc).isoformat(),
        'status': 'passed', 'scope': ('Independent local reconstruction of saved actual C2 '
            'GitHub commit/ref/tree responses. Every remote file mode/blob/size equals the '
            'frozen locally hashed bytes; all descendant/control trees reconstruct. This '
            'does not redownload every blob, certify continuous mathematics, or assert CI success.'),
        'c2_commit': C2, 'sole_parent_commit': PARENT, 'root_tree': ROOT, 'article_tree': ARTICLE,
        'readback_started_utc': saved['started'], 'readback_finished_utc': saved['finished'],
        'input_sha256_pins': PINS, 'verifier_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'file_count': 2710, 'bytes': 292904889, 'descendant_subtree_count': 113,
        'article_inclusive_canonical_tree_count': 114, 'recursive_entries': 2823,
        'remote_article_truncated': False, 'files_added_or_missing_against_frozen': [],
        'new_refs': ref_checks, 'control_trees': root_checks,
        'all_212_old_paper_entries_preserved': True, 'all_174_old_workflow_entries_preserved': True,
        'actual_c2_run_lookup': {'observed_at': saved['finished'], 'total_count': 1,
                                 'run_id': run['id'], 'head_sha': run['head_sha'],
                                 'status': run['status'], 'conclusion': run['conclusion'],
                                 'interpretation': 'Run in progress at this fixed readback; no CI success claim.'},
        'c1_to_c2_delta': delta,
        'old_ref_movement_rechecked': False,
        'old_ref_scope': 'The three new refs only were read here; the full earlier branch census has its own scope.',
        'remote_operations_by_this_verifier': 'none', 'article_writes': 'none',
    }
    for name, value in [('C2_REMOTE_FILE_CHECKS.json', file_checks),
                        ('C2_REMOTE_SUBTREE_CHECKS.json', subtree_checks),
                        ('C2_REMOTE_SIBLING_CHECKS.json', sibling_checks),
                        ('C2_FROZEN_INPUT_CHECKS.json', frozen_checks),
                        ('C2_MATHEMATICAL_FINGERPRINT_FILES.json', new_math_rows),
                        ('C1_TO_C2_DELTA_CHECKS.json', delta),
                        ('C2_REMOTE_VERIFICATION_RECEIPT.json', result)]:
        (HERE / name).write_text(json.dumps(value, indent=2) + '\n')
    print(json.dumps(result))


if __name__ == '__main__':
    main()
