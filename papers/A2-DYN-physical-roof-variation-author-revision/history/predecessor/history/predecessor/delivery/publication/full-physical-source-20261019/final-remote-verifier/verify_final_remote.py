#!/usr/bin/env python3
"""Verify complete saved publication readbacks without API or article writes.

All article counts are derived from the supplied complete inventories. The
frozen scientific manifest is independently pinned; metadata-only publication
must retain every frozen input and the native/mathematical source identities.
The script has its own Git tree implementation and does not import a transport
helper. A CI outcome is never inferred from a source or metadata verification.
"""
from pathlib import Path, PurePosixPath
from collections import defaultdict
from datetime import datetime, timezone
import argparse
import hashlib
import json
import re

HERE = Path(__file__).resolve().parent
ARTICLE_NAME = 'A2-DYN-full-physical-source-author-revision'
WORKFLOW_NAME = 'a2-dyn-full-physical-source-20261019.yml'
REF_SUFFIX = 'a2-dyn-full-physical-source-2026-10-19'
MANIFEST_SHA256 = '13182b20479bcafcd8a3d53804b9cc610739e5a8ad0fb94f32eed65b4768f997'
MUTABLE = frozenset(('PUBLICATION_STATUS.json', 'PUBLICATION_RECEIPT.json',
                     'REMOTE_TRANSPORT_STATUS.md'))
ADDED_PREFIXES = ('delivery/publication/full-physical-source-20261019/',
                  'evidence/current-execution/full-physical-publication-source/')


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


def utc():
    return datetime.now(timezone.utc).isoformat()


def digest(data):
    return hashlib.sha256(data).hexdigest()


def blob(data):
    return hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()


def signature(row):
    return (str(row['mode']).lstrip('0'), row['type'], row['sha'])


def indexed(rows):
    result = {row['path']: row for row in rows}
    require(len(result) == len(rows), 'Duplicate object path')
    return result


def canonical(rows):
    encoded, seen = [], set()
    for row in rows:
        name = row['path']
        require(name not in seen and name not in ('', '.', '..') and
                '/' not in name and '\0' not in name, 'Invalid immediate Git tree child')
        seen.add(name)
        mode = str(row['mode']).lstrip('0')
        require(mode in ('40000', '100644', '100755', '120000', '160000'), 'Invalid Git mode')
        sha = row['sha']
        require(re.fullmatch('[0-9a-f]{40}', sha), 'Invalid object SHA')
        name_bytes = name.encode('utf-8')
        key = name_bytes + (b'/' if mode == '40000' else b'')
        encoded.append((key, mode.encode() + b' ' + name_bytes + b'\0' + bytes.fromhex(sha)))
    payload = b''.join(value for _, value in sorted(encoded))
    return hashlib.sha1(b'tree ' + str(len(payload)).encode() + b'\0' + payload).hexdigest()


def normalized(path):
    value = PurePosixPath(path)
    require(str(value) == path and not value.is_absolute() and value.parts and
            all(part not in ('.', '..') for part in value.parts) and '\0' not in path,
            'Invalid relative path: ' + path)
    return value


def file_tree(files):
    """Reconstruct complete inventory trees from file rows, independently."""
    children = defaultdict(list)
    directories = {''}
    for path, row in files.items():
        parts = normalized(path).parts
        parent = '/'.join(parts[:-1])
        children[parent].append(dict(row, path=parts[-1]))
        for index in range(1, len(parts)):
            directories.add('/'.join(parts[:index]))
    hashes = {}
    for path in sorted(directories, key=lambda p: (-len(PurePosixPath(p).parts), p)):
        value = canonical(children[path])
        hashes[path] = value
        if path:
            p = PurePosixPath(path)
            parent = p.parent.as_posix()
            if parent == '.':
                parent = ''
            children[parent].append({'path': p.name, 'mode': '040000', 'type': 'tree', 'sha': value})
    return hashes


def inventory(obj):
    require(isinstance(obj, dict) and isinstance(obj.get('files'), list), 'Expected complete dict.files inventory')
    rows = indexed(obj['files'])
    hashes = file_tree(rows)
    require(hashes[''] == obj['article_tree_sha'], 'Inventory canonical article hash mismatch')
    if 'subtree_hashes' in obj:
        require(hashes == obj['subtree_hashes'], 'Inventory canonical subtree mismatch')
    if 'file_count' in obj:
        require(obj['file_count'] == len(rows), 'Inventory file count mismatch')
    if 'bytes' in obj:
        require(obj['bytes'] == sum(row['bytes'] for row in rows.values()), 'Inventory byte count mismatch')
    return rows, hashes


def observations(saved):
    require(isinstance(saved, dict) and isinstance(saved.get('readbacks'), list), 'Expected saved actual readbacks')
    rows = {row['key']: row for row in saved['readbacks']}
    require(len(rows) == len(saved['readbacks']), 'Duplicate saved readback key')
    require(all(isinstance(row.get('data'), dict) for row in rows.values()), 'Incomplete readback payload')
    return {key: row['data'] for key, row in rows.items()}


def fingerprint(rows):
    chosen = []
    for path in rows:
        parts = normalized(path).parts
        suffix = PurePosixPath(path).suffix
        if ((len(parts) == 1 and suffix == '.tex') or
            (len(parts) == 2 and parts[0] == 'core' and suffix == '.tex') or
            (len(parts) == 2 and parts[0] == 'tools' and suffix == '.py')):
            chosen.append(path)
    records = [{'path': path, 'sha256': rows[path]['sha256']} for path in sorted(chosen)]
    return digest(json.dumps(records, sort_keys=True).encode()), records


def census(obj):
    require(isinstance(obj, dict) and isinstance(obj.get('branches'), list), 'Expected complete census dict.branches')
    rows = {row['name']: row['commit']['sha'] for row in obj['branches']}
    require(len(rows) == len(obj['branches']) == obj['count'], 'Census count or duplicate-name mismatch')
    pages = obj.get('pages', [])
    exhausted = (bool(pages) and pages[-1]['records'] < 100 and
                 [page['page'] for page in pages] == list(range(1, len(pages) + 1)) and
                 sum(page['records'] for page in pages) == len(rows))
    require(exhausted, 'No complete ordered/exhausted page evidence for branch census')
    return rows


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--readbacks', type=Path, required=True)
    parser.add_argument('--expected', type=Path, required=True)
    parser.add_argument('--scope', type=Path, required=True)
    parser.add_argument('--previous', type=Path, required=True)
    parser.add_argument('--head', required=True)
    parser.add_argument('--parent', required=True)
    parser.add_argument('--manifest', type=Path, default=HERE / 'inputs/SOURCE_MANIFEST.json')
    parser.add_argument('--previous-readbacks', type=Path,
                        help='Recommended: actual previous commit/control-tree readbacks')
    parser.add_argument('--old-census', type=Path)
    parser.add_argument('--current-all-refs', type=Path)
    parser.add_argument('--output-dir', type=Path, default=HERE / 'results')
    args = parser.parse_args()
    require(re.fullmatch('[0-9a-f]{40}', args.head) and
            re.fullmatch('[0-9a-f]{40}', args.parent), 'Complete head and parent SHAs required')
    require(bool(args.old_census) == bool(args.current_all_refs), 'Both census inputs must be supplied together')
    output = args.output_dir.resolve()
    parts = output.parts
    require(not any(parts[i] == 'papers' and parts[i + 1] == ARTICLE_NAME
                    for i in range(len(parts) - 1)), 'Write verification output outside the article')
    started = utc()
    inputs, raw = {}, {}

    def read(label, path):
        data = path.read_bytes()
        raw[label] = data
        inputs[label] = {'path': str(path.resolve()), 'bytes': len(data), 'sha256': digest(data)}
        return json.loads(data)

    saved = read('remote_readbacks.json', args.readbacks)
    expected = read('expected_file_identities.json', args.expected)
    scope = read('expected_root_scope.json', args.scope)
    previous = read('previous_file_identities.json', args.previous)
    manifest = read('frozen_source_manifest.json', args.manifest)
    require(inputs['frozen_source_manifest.json']['sha256'] == MANIFEST_SHA256, 'Frozen scientific manifest pin changed')
    wanted, wanted_hashes = inventory(expected)
    old, old_hashes = inventory(previous)
    actual = observations(saved)
    require(actual['commit']['sha'] == args.head and
            [row['sha'] for row in actual['commit']['parents']] == [args.parent],
            'Actual commit or sole parent differs from declared publication')
    require(actual['commit']['tree']['sha'] == scope['expected_tree_identities']['root'], 'Actual commit/root mismatch')
    targets = [family + '/' + REF_SUFFIX for family in ('revision', 'referee-response', 'referee-copy')]
    ref_results = []
    for branch in targets:
        row = actual['ref:' + branch]
        require(row['ref'] == 'refs/heads/' + branch and row['object']['type'] == 'commit' and
                row['object']['sha'] == args.head, 'Actual publication ref mismatch: ' + branch)
        ref_results.append({'ref': row['ref'], 'head': row['object']['sha'], 'passed': True})
    article = actual['article']
    require(article.get('truncated') is False and article['sha'] == expected['article_tree_sha'],
            'Actual article is truncated or has the wrong identity')
    entries = indexed(article['tree'])
    blobs = {path: row for path, row in entries.items() if row['type'] == 'blob'}
    trees = {path: row for path, row in entries.items() if row['type'] == 'tree'}
    require(len(blobs) + len(trees) == len(entries) and set(blobs) == set(wanted), 'Incomplete or unexpected article paths')
    file_checks = []
    for path in sorted(blobs):
        row, wanted_row = blobs[path], wanted[path]
        require(row['mode'] == wanted_row['mode'] and row['sha'] == wanted_row['sha'] and
                row['size'] == wanted_row['bytes'], 'Remote file differs from frozen expected bytes: ' + path)
        file_checks.append({'path': path, 'mode': row['mode'], 'sha': row['sha'],
                            'bytes': row['size'], 'frozen_sha256': wanted_row['sha256'], 'passed': True})
    children = defaultdict(list)
    children[''] = []
    for path, row in entries.items():
        p = normalized(path)
        parent = p.parent.as_posix()
        if parent == '.':
            parent = ''
        require(parent == '' or parent in trees, 'Missing actual directory ancestor')
        children[parent].append(dict(row, path=p.name))
        if row['type'] == 'tree':
            children.setdefault(path, [])
    require(set(children) == set(wanted_hashes), 'Actual and expected subtree sets differ')
    subtree_checks = []
    for path in sorted(children):
        computed = canonical(children[path])
        returned = article['sha'] if path == '' else trees[path]['sha']
        require(computed == returned == wanted_hashes[path], 'Actual canonical subtree mismatch: ' + path)
        subtree_checks.append({'path': path, 'sha': computed, 'children': len(children[path]), 'passed': True})

    controls, sibling_checks = [], []
    allowed_scope = {'root': {'.github', 'papers'}, 'papers': {ARTICLE_NAME},
                     'github': {'workflows'}, 'workflows': {WORKFLOW_NAME}}
    for kind in ('root', 'papers', 'github', 'workflows'):
        remote = actual[kind]
        require(remote.get('truncated') is False, 'Truncated actual control tree')
        rows = indexed(remote['tree'])
        planned = indexed(scope['expected_trees'][kind]['tree'])
        base_obj = scope['base_trees'][kind]
        before = indexed(base_obj['tree'])
        require(canonical(remote['tree']) == remote['sha'] == scope['expected_tree_identities'][kind] ==
                scope['expected_trees'][kind]['sha'] == canonical(scope['expected_trees'][kind]['tree']),
                'Control tree canonical mismatch: ' + kind)
        require(canonical(base_obj['tree']) == scope['base_tree_identities'][kind], 'Pinned base control tree mismatch')
        require(set(rows) == set(planned) and set(before) <= set(rows), 'Control-tree membership/deletion mismatch')
        for path in rows:
            require(signature(rows[path]) == signature(planned[path]), 'Unexpected actual control entry')
        changed = {path for path in rows if path not in before or signature(rows[path]) != signature(before[path])}
        require(changed <= allowed_scope[kind], 'Unrelated repository sibling changed')
        for path in sorted(before):
            sibling_checks.append({'tree': kind, 'path': path, 'old_sha': before[path]['sha'],
                                   'actual_sha': rows[path]['sha'], 'unchanged': path not in changed,
                                   'authorized_pointer_change': path in changed})
        controls.append({'tree': kind, 'sha': remote['sha'], 'base_entries': len(before),
                         'actual_entries': len(rows), 'authorized_changes': sorted(changed),
                         'other_siblings_unchanged': True})
    root_rows = indexed(actual['root']['tree'])
    paper_rows = indexed(actual['papers']['tree'])
    github_rows = indexed(actual['github']['tree'])
    workflow_rows = indexed(actual['workflows']['tree'])
    require(root_rows['papers']['sha'] == actual['papers']['sha'] and
            root_rows['.github']['sha'] == actual['github']['sha'] and
            github_rows['workflows']['sha'] == actual['workflows']['sha'] and
            paper_rows[ARTICLE_NAME]['sha'] == article['sha'] == scope['expected_article_tree'],
            'Actual root-to-source path linkage mismatch')
    workflow = workflow_rows[WORKFLOW_NAME]
    copy = blobs['ci/' + WORKFLOW_NAME]
    require(signature(workflow) == signature(copy) and workflow['size'] == copy['size'],
            'Actual dedicated workflow and article copy differ')

    require(set(old) <= set(wanted), 'Metadata successor deletes an existing source/article file')
    modified = sorted(path for path in old if any(old[path][key] != wanted[path][key]
                      for key in ('sha', 'sha256', 'bytes', 'mode')))
    added = sorted(set(wanted) - set(old))
    require(set(modified) <= MUTABLE, 'Existing bytes changed beyond the three declared publication metadata files')
    require(all(path.startswith(ADDED_PREFIXES) for path in added), 'Added file is outside publication/source-gate scope')
    require(MUTABLE <= set(manifest['excluded_root_files']), 'Manifest does not explicitly exclude the three mutable files')
    manifest_blob = blob(raw['frozen_source_manifest.json'])
    for carrier in (old, wanted):
        require(carrier['SOURCE_MANIFEST.json']['sha'] == manifest_blob and
                carrier['SOURCE_MANIFEST.json']['sha256'] == MANIFEST_SHA256,
                'Frozen manifest differs between carriers')
    fixed = indexed(manifest['files'])
    require(len(fixed) == manifest['source_count'] and
            sum(row['bytes'] for row in fixed.values()) == manifest['source_bytes'], 'Frozen manifest count/size mismatch')
    frozen_checks = []
    for path, row in sorted(fixed.items()):
        require(path in old and path in wanted, 'Frozen input is missing')
        for carrier in (old, wanted):
            require(carrier[path]['sha'] == row['git_blob'] and carrier[path]['sha256'] == row['sha256'] and
                    carrier[path]['bytes'] == row['bytes'], 'Frozen scientific input changed: ' + path)
        require(old[path]['mode'] == wanted[path]['mode'], 'Frozen input Git mode changed')
        frozen_checks.append({'path': path, 'sha': row['git_blob'], 'sha256': row['sha256'],
                              'bytes': row['bytes'], 'unchanged': True})
    closure = manifest['native_tex_closure']
    require(set(closure['reachable_tex_files']) <= set(fixed), 'Native closure has an unfrozen path')
    cores = closure['active_core_files']
    require(set(cores) <= set(fixed), 'Native proof core missing from frozen inputs')
    numbers = sorted(int(PurePosixPath(path).name.split('_')[0]) for path in cores)
    require(numbers == list(range(closure['active_core_start'], closure['active_core_end'] + 1)),
            'Frozen native core chain is not complete and consecutive')
    old_fingerprint, old_math = fingerprint(old)
    new_fingerprint, new_math = fingerprint(wanted)
    require(old_math == new_math and old_fingerprint == new_fingerprint and
            {row['path'] for row in new_math} <= set(fixed), 'Mathematical native/tool fingerprint changed')
    require(all(old['ci/' + WORKFLOW_NAME][key] == wanted['ci/' + WORKFLOW_NAME][key]
                for key in ('sha', 'sha256', 'bytes', 'mode')), 'Previously tested workflow changed')

    parent_controls = {'checked': False, 'scope': 'Supply --previous-readbacks for direct parent control-tree comparison.'}
    if args.previous_readbacks:
        parent_saved = read('previous_remote_readbacks.json', args.previous_readbacks)
        parent_actual = observations(parent_saved)
        require(parent_actual['commit']['sha'] == args.parent and
                parent_actual['article']['sha'] == previous['article_tree_sha'], 'Actual previous carrier identity mismatch')
        parent_root = indexed(parent_actual['root']['tree'])
        parent_papers = indexed(parent_actual['papers']['tree'])
        parent_github = indexed(parent_actual['github']['tree'])
        require(parent_actual['commit']['tree']['sha'] == parent_actual['root']['sha'] and
                parent_root['papers']['sha'] == parent_actual['papers']['sha'] and
                parent_root['.github']['sha'] == parent_actual['github']['sha'] and
                parent_github['workflows']['sha'] == parent_actual['workflows']['sha'] and
                parent_papers[ARTICLE_NAME]['sha'] == previous['article_tree_sha'],
                'Actual previous commit/control/source linkage mismatch')
        allowed_parent = {'root': {'papers'}, 'papers': {ARTICLE_NAME}, 'github': set(), 'workflows': set()}
        comparisons = []
        for kind in ('root', 'papers', 'github', 'workflows'):
            before_obj = parent_actual[kind]
            require(before_obj.get('truncated') is False and canonical(before_obj['tree']) == before_obj['sha'],
                    'Actual previous control tree canonical mismatch')
            before, after = indexed(before_obj['tree']), indexed(actual[kind]['tree'])
            require(set(before) == set(after), 'Metadata successor changes repository control entry membership')
            changed = {path for path in before if signature(before[path]) != signature(after[path])}
            require(changed <= allowed_parent[kind], 'Metadata successor changes an unrelated parent sibling')
            comparisons.append({'tree': kind, 'previous_sha': before_obj['sha'], 'actual_sha': actual[kind]['sha'],
                                'changed_entries': sorted(changed), 'all_other_entries_unchanged': True})
        parent_controls = {'checked': True, 'trees': comparisons}

    ref_census = {'checked': False, 'scope': 'Only three publication refs were verified; no whole-repository stationary-ref claim.'}
    scope_observations = []
    if args.old_census:
        old_census = read('old_complete_census.json', args.old_census)
        new_census = read('current_complete_census.json', args.current_all_refs)
        old_refs, now_refs = census(old_census), census(new_census)
        require(all(now_refs.get(name) == args.head for name in targets), 'Current census publication heads differ')
        missing = sorted(set(old_refs) - set(now_refs))
        moved = [{'ref': name, 'old': old_refs[name], 'new': now_refs[name]}
                 for name in sorted(set(old_refs) & set(now_refs)) if old_refs[name] != now_refs[name]]
        a2 = lambda name: bool(re.search(r'a2[-_]?dyn', name, re.I))
        old_a2_missing = [name for name in missing if a2(name) and name not in targets]
        old_a2_moved = [row for row in moved if a2(row['ref']) and row['ref'] not in targets]
        require(not old_a2_missing and not old_a2_moved, 'An existing non-target A2-DYN ref moved or disappeared')
        added_refs = sorted(set(now_refs) - set(old_refs))
        unexpected_a2 = [name for name in added_refs if a2(name) and name not in targets]
        if unexpected_a2:
            scope_observations.append('Additional new A2-DYN refs require attribution; listed in census receipt.')
        ref_census = {'checked': True, 'old_count': len(old_refs), 'current_count': len(now_refs),
                      'old_observed_finished_utc': old_census.get('observed_finished_utc'),
                      'current_observed_finished_utc': new_census.get('observed_finished_utc'),
                      'existing_non_target_a2_dyn_refs_unchanged': True,
                      'existing_non_target_a2_dyn_ref_count': sum(a2(name) and name not in targets for name in old_refs),
                      'added_refs': added_refs, 'removed_unrelated_refs': missing,
                      'all_observed_ref_movements': moved, 'additional_new_a2_dyn_refs': unexpected_a2,
                      'unrelated_movements_not_attributed_to_this_publication': True}

    runs = actual.get('runs')
    run_observation = {'present': runs is not None, 'observed_finished_utc': saved.get('finished'),
                       'scope': 'Raw observation only; no CI success inference or borrowing from the parent.'}
    if runs is not None:
        run_observation['total_count'] = runs.get('total_count')
        run_observation['runs'] = [{key: row.get(key) for key in
                                   ('id', 'head_sha', 'head_branch', 'path', 'status', 'conclusion')}
                                  for row in runs.get('workflow_runs', [])]
    delta = {'previous_article_tree': previous['article_tree_sha'], 'current_article_tree': expected['article_tree_sha'],
             'modified_existing_paths': modified, 'allowed_modified_existing_paths': sorted(MUTABLE),
             'added_paths': added, 'added_count': len(added), 'removed_paths': [],
             'allowed_added_prefixes': list(ADDED_PREFIXES), 'frozen_inputs': len(fixed),
             'frozen_input_bytes': manifest['source_bytes'], 'manifest_sha256': MANIFEST_SHA256,
             'frozen_input_bytes_and_modes_unchanged': True, 'native_core_count': len(cores),
             'native_core_range': [closure['active_core_start'], closure['active_core_end']],
             'mathematical_fingerprint_file_count': len(new_math),
             'mathematical_fingerprint_before': old_fingerprint, 'mathematical_fingerprint_after': new_fingerprint,
             'parent_control_tree_comparison': parent_controls}
    result = {'started_utc': started, 'completed_utc': utc(),
              'status': 'passed_with_ref_scope_observations' if scope_observations else 'passed',
              'scope': 'Saved actual commit/ref/tree observations independently reconstructed against complete frozen byte identities; no full blob-body redownload, mathematical certification, or CI-success inference.',
              'head': args.head, 'sole_parent': args.parent, 'root_tree': actual['root']['sha'],
              'article_tree': article['sha'], 'file_count': len(blobs),
              'file_bytes': sum(row['size'] for row in blobs.values()), 'recursive_entries': len(entries),
              'descendant_subtrees': len(trees), 'article_inclusive_reconstructed_trees': len(subtree_checks),
              'all_actual_tree_responses_nontruncated': True, 'publication_refs': ref_results,
              'root_control_trees': controls, 'metadata_delta': delta, 'ref_census': ref_census,
              'scope_observations': scope_observations, 'run_observation': run_observation,
              'input_identities': inputs, 'verifier_sha256': digest(Path(__file__).read_bytes()),
              'network_calls': 0, 'article_writes': 0}
    output.mkdir(parents=True, exist_ok=True)
    archive = output / 'inputs'
    archive.mkdir(exist_ok=True)
    for name, data in raw.items():
        target = archive / name
        if target.exists():
            require(target.read_bytes() == data, 'Conflicting verification input archive: ' + name)
        else:
            target.write_bytes(data)
    for name, value in [('REMOTE_FILE_CHECKS.json', file_checks), ('REMOTE_SUBTREE_CHECKS.json', subtree_checks),
                        ('REMOTE_SIBLING_CHECKS.json', sibling_checks), ('FROZEN_INPUT_CHECKS.json', frozen_checks),
                        ('MATHEMATICAL_FINGERPRINT_FILES.json', new_math), ('METADATA_DELTA_CHECKS.json', delta),
                        ('FINAL_REMOTE_VERIFICATION_RECEIPT.json', result)]:
        (output / name).write_text(json.dumps(value, indent=2) + '\n')
    print(json.dumps({key: value for key, value in result.items()
                      if key not in ('metadata_delta', 'input_identities', 'ref_census')}))


if __name__ == '__main__':
    main()
