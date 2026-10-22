#!/usr/bin/env python3
"""Prepare exact frozen C1 blob/tree payloads locally; never publish objects/refs."""
from pathlib import Path
import hashlib
import importlib.util
import json
import sys

sys.dont_write_bytecode = True
WORK = Path('/workspace/scratch/b5cc344d4c8e/iteration-20261019b')
INVENTORY = WORK / 'C1_TRANSPORT_TO_PUBLISH.json'
INVENTORY_SHA256 = '4ac3cb80421872107489b5c48f9b48a79525ea38ae36741effe02bf7852c61ea'
ARTICLE_SHA = 'f0e29499f0d5de75103b6f52cc464945071ea04b'
ROOT_SHA = '56031be3c69251f8eadce010b38d576eaf9497e6'
MAX_ENTRIES = 60
MAX_CHARACTERS = 180000


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


def write(name, value):
    path = WORK / name
    path.write_text(json.dumps(value, indent=2) + '\n')
    return path


def batch_text(batch, expected='0' * 40):
    return json.dumps({'tree_elements': batch, 'expected_tree_sha': expected}, indent=2) + '\n'


def main():
    spec = importlib.util.spec_from_file_location('transport_revision', WORK / 'transport_revision.py')
    adapter = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(adapter)
    data = INVENTORY.read_bytes()
    require(hashlib.sha256(data).hexdigest() == INVENTORY_SHA256, 'Frozen C1 inventory changed')
    final = json.loads(data)
    require(final['snapshot_status'] == 'final_local_candidate' and
            final['file_count'] == 2688 and final['bytes'] == 285948269,
            'Unexpected frozen C1 source cardinality or status')
    expected, subtrees = adapter.tree_digest(final['files'])
    require(expected == final['article_tree_sha'] == ARTICLE_SHA and
            subtrees == final['subtree_hashes'], 'Frozen C1 canonical tree mismatch')
    root_scope = json.loads((WORK / 'C1_ROOT_EXPECTED.json').read_bytes())
    require(root_scope['expected_tree_identities']['root'] == ROOT_SHA and
            root_scope['expected_article_tree'] == ARTICLE_SHA,
            'Frozen C1 root/article scope mismatch')
    baseline = adapter.load_baseline()
    old = {row['path']: row for row in baseline['files']}
    current = {row['path']: row for row in final['files']}
    require(set(old) <= set(current), 'C1 deletes a baseline-relative article path')
    actual = {row['path']: row for row in adapter.scan()}
    require(set(actual) == set(current), 'Actual local path set differs from frozen C1')
    for path in current:
        require(all(current[path][key] == actual[path][key]
                    for key in ('sha', 'sha256', 'mode', 'bytes')),
                'Actual bytes or mode differ from frozen C1: ' + path)

    changed = [row for row in final['files'] if row['path'] not in old or any(
        row[key] != old[row['path']][key] for key in ('sha', 'mode', 'bytes'))]
    require(len(changed) == final['changed_paths'], 'Changed-path count mismatch')
    known = {row['sha'] for row in baseline['files']}
    all_paths_by_blob = {}
    for row in changed:
        all_paths_by_blob.setdefault(row['sha'], []).append(row['path'])
    large_by_sha = {}
    content_by_sha = {}
    for row in changed:
        if row['sha'] in known or row['sha'] in large_by_sha or row['sha'] in content_by_sha:
            continue
        reason = None
        if row['encoding'] == 'base64':
            reason = 'new_binary'
        elif row['bytes'] > 120000:
            reason = 'new_utf8_over_120000_bytes'
        else:
            payload, mode, _ = adapter.stable_payload(adapter.ROOT / row['path'])
            require(adapter.git_blob(payload) == row['sha'] and mode == row['mode'],
                    'Inline source changed after frozen byte verification')
            content = payload.decode('utf-8')
            candidate = {'path': row['path'], 'mode': row['mode'], 'type': 'blob',
                         'content': content}
            if len(batch_text([candidate])) > MAX_CHARACTERS:
                reason = 'escaped_single_entry_over_180000_characters'
            else:
                content_by_sha[row['sha']] = content
        if reason is not None:
            large_by_sha[row['sha']] = dict(row, upload_reason=reason,
                                            reused_by_paths=all_paths_by_blob[row['sha']])

    elements = []
    for row in changed:
        entry = {'path': row['path'], 'mode': row['mode'], 'type': 'blob'}
        if row['sha'] in known or row['sha'] in large_by_sha:
            entry['sha'] = row['sha']
        else:
            entry['content'] = content_by_sha[row['sha']]
        elements.append(entry)

    batches, batch = [], []
    for entry in elements:
        if batch and (len(batch) >= MAX_ENTRIES or
                      len(batch_text(batch + [entry])) > MAX_CHARACTERS):
            batches.append(batch)
            batch = []
        batch.append(entry)
        require(len(batch_text(batch)) <= MAX_CHARACTERS, 'Single entry exceeds batch budget')
    if batch:
        batches.append(batch)
    cumulative = dict(old)
    parent = adapter.BASE_TREE
    plan = []
    for index, batch in enumerate(batches):
        for entry in batch:
            cumulative[entry['path']] = current[entry['path']]
        expected, _ = adapter.tree_digest(list(cumulative.values()))
        serialized = batch_text(batch, expected)
        require(len(batch) <= MAX_ENTRIES and len(serialized) <= MAX_CHARACTERS,
                'Prepared batch exceeds exact stored-character or entry limit')
        path = WORK / ('C1_TREE_BATCH_%02d.json' % index)
        path.write_text(serialized)
        plan.append({'index': index, 'path': str(path), 'parent_tree_sha': parent,
                     'characters': len(serialized), 'elements': len(batch),
                     'expected_tree_sha': expected,
                     'payload_sha256': hashlib.sha256(path.read_bytes()).hexdigest()})
        parent = expected
    require(parent == ARTICLE_SHA, 'Final cumulative payload differs from frozen C1 article')
    large = list(large_by_sha.values())
    write('C1_LARGE_BLOBS.json', large)
    write('C1_TREE_PLAN.json', plan)
    result = {
        'created_utc': adapter.utc_now(), 'status': 'prepared_local_payloads_only',
        'frozen_inventory_sha256': INVENTORY_SHA256,
        'base_commit': adapter.BASE_COMMIT, 'base_article_tree': adapter.BASE_TREE,
        'article_tree_sha': ARTICLE_SHA, 'root_tree_sha': ROOT_SHA,
        'file_count': len(current), 'bytes': final['bytes'],
        'actual_local_files_match_frozen_inventory': True,
        'changed_paths': len(changed), 'removed_paths': [],
        'baseline_blob_reuse_paths_among_changed': sum(row['sha'] in known for row in changed),
        'large_new_unique_blobs': len(large),
        'large_new_unique_blob_bytes': sum(row['bytes'] for row in large),
        'large_new_unique_binary_blobs': sum(row['encoding'] == 'base64' for row in large),
        'large_new_unique_utf8_blobs': sum(row['encoding'] == 'utf-8' for row in large),
        'oversize_single_entry_promotions': sum(
            row['upload_reason'] == 'escaped_single_entry_over_180000_characters' for row in large),
        'inline_new_unique_blobs': len(content_by_sha),
        'tree_batches': len(plan), 'maximum_entries': max(row['elements'] for row in plan),
        'maximum_stored_json_characters': max(row['characters'] for row in plan),
        'final_canonical_intermediate_sha_matches': parent == ARTICLE_SHA,
        'remote_operations': 'none', 'article_writes': 'none',
        'adapter_script_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    }
    write('C1_TRANSPORT_PREPARATION_RECEIPT.json', result)
    print(json.dumps(result))


if __name__ == '__main__':
    main()
