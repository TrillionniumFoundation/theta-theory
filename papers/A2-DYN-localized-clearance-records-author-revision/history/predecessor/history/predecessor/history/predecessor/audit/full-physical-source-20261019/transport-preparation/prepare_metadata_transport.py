#!/usr/bin/env python3
"""Prepare local metadata-successor Git Data payloads after a tested source carrier.

This helper performs no network calls or Git/ref operations. The caller must
provide the actual preceding inventory and frozen source/workflow hashes; the
helper does not infer a completed CI run from a filename or a declared parent.
Only PUBLICATION_STATUS.json may change at an existing path. All added paths
must lie in the explicitly recorded publication/source-gate prefixes.
"""
from pathlib import Path
import argparse
import hashlib
import importlib.util
import json
import re
import sys

sys.dont_write_bytecode = True
WORK = Path('/workspace/scratch/b5cc344d4c8e/iteration-20261019b')


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


def module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    value = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(value)
    return value


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--before', type=Path, required=True,
                        help='Complete immutable preceding carrier inventory')
    parser.add_argument('--parent-commit', required=True)
    parser.add_argument('--manifest-sha256', required=True)
    parser.add_argument('--workflow-sha256', required=True)
    parser.add_argument('--publication-prefix',
                        default='delivery/publication/full-physical-source-20261019/')
    parser.add_argument('--source-gate-prefix',
                        default='evidence/current-execution/full-physical-publication-source/')
    parser.add_argument('--output-prefix', default='C3')
    args = parser.parse_args()
    require(re.fullmatch('[0-9a-f]{40}', args.parent_commit), 'Invalid parent commit SHA')
    for sha in (args.manifest_sha256, args.workflow_sha256):
        require(re.fullmatch('[0-9a-f]{64}', sha), 'Expected a complete SHA256 pin')
    require(re.fullmatch('[A-Za-z0-9_-]+', args.output_prefix), 'Invalid output prefix')
    adapter = module('transport_revision', WORK / 'transport_revision.py')
    for prefix in (args.publication_prefix, args.source_gate_prefix):
        require(prefix.endswith('/'), 'Allowed metadata prefix must end with slash')
        adapter.path_parts(prefix[:-1])
    require(args.publication_prefix.startswith('delivery/publication/') and
            args.source_gate_prefix.startswith('evidence/current-execution/'),
            'Metadata additions must retain the publication/source-gate scope')

    def write(suffix, value):
        path = WORK / (args.output_prefix + '_' + suffix + '.json')
        path.write_text(json.dumps(value, indent=2) + '\n')
        return path

    manifest_path = adapter.ROOT / 'SOURCE_MANIFEST.json'
    require(hashlib.sha256(manifest_path.read_bytes()).hexdigest() == args.manifest_sha256,
            'Frozen source manifest changed')
    gate = module('current_source_gate', adapter.ROOT / 'tools/package_source_manifest.py')
    manifest_result = gate.verify_manifest(adapter.ROOT)
    for path in (adapter.WORKFLOW, adapter.ROOT / 'ci' / adapter.WORKFLOW_NAME):
        require(hashlib.sha256(path.read_bytes()).hexdigest() == args.workflow_sha256,
                'Frozen dedicated workflow changed')

    before = json.loads(args.before.read_bytes())
    require(isinstance(before, dict) and isinstance(before.get('files'), list),
            'Expected a complete predecessor dict.files inventory')
    prior_sha, prior_subtrees = adapter.tree_digest(before['files'])
    require(prior_sha == before['article_tree_sha'], 'Predecessor canonical tree mismatch')
    if 'subtree_hashes' in before:
        require(prior_subtrees == before['subtree_hashes'], 'Predecessor subtree mismatch')
    previous = {row['path']: row for row in before['files']}
    current_value = adapter.inventory(final=True)
    rows = current_value['files']
    current = {row['path']: row for row in rows}
    require(set(previous) <= set(current), 'Metadata successor deletes an existing article path')
    changed = [row for row in rows if row['path'] not in previous or any(
        row[key] != previous[row['path']][key] for key in ('sha', 'mode', 'bytes'))]
    require(changed, 'No metadata delta to prepare')
    modified = [row['path'] for row in changed if row['path'] in previous]
    added = [row['path'] for row in changed if row['path'] not in previous]
    require(all(path == 'PUBLICATION_STATUS.json' for path in modified),
            'Existing predecessor bytes changed outside PUBLICATION_STATUS.json')
    require(all(path.startswith((args.publication_prefix, args.source_gate_prefix))
                for path in added), 'Added file lies outside publication metadata scope')

    known = {row['sha'] for row in before['files']}
    large_by_sha = {}
    for row in changed:
        if row['sha'] not in known and (row['encoding'] == 'base64' or row['bytes'] > 120000):
            large_by_sha.setdefault(row['sha'], row)
    elements = []
    for row in changed:
        entry = {'path': row['path'], 'mode': row['mode'], 'type': 'blob'}
        if row['sha'] in known or row['sha'] in large_by_sha:
            entry['sha'] = row['sha']
        else:
            data, mode, _ = adapter.stable_payload(adapter.ROOT / row['path'])
            require(adapter.git_blob(data) == row['sha'] and mode == row['mode'],
                    'File changed after metadata inventory: ' + row['path'])
            # Explicit byte decoding preserves actual CRLF and literal escapes.
            entry['content'] = data.decode('utf-8')
        elements.append(entry)
    batches, batch, size = [], [], 0
    for entry in elements:
        amount = len(json.dumps(entry))
        if batch and (len(batch) >= 60 or size + amount > 180000):
            batches.append(batch)
            batch, size = [], 0
        batch.append(entry)
        size += amount
    if batch:
        batches.append(batch)
    cumulative = dict(previous)
    plan = []
    for index, batch in enumerate(batches):
        for entry in batch:
            cumulative[entry['path']] = current[entry['path']]
        expected, _ = adapter.tree_digest(list(cumulative.values()))
        path = write('TREE_BATCH_%02d' % index,
                     {'tree_elements': batch, 'expected_tree_sha': expected})
        plan.append({'index': index, 'path': str(path),
                     'characters': len(path.read_bytes().decode('utf-8')),
                     'elements': len(batch), 'expected_tree_sha': expected})
    require(plan[-1]['expected_tree_sha'] == current_value['article_tree_sha'],
            'Final metadata plan differs from actual local bytes')
    write('FILE_IDENTITIES', current_value)
    write('TREE_PLAN', plan)
    write('LARGE_BLOBS', list(large_by_sha.values()))
    scope = {
        'created_utc': adapter.utc_now(), 'status': 'local_metadata_plan_only',
        'parent_commit_declared_by_caller': args.parent_commit,
        'parent_article_tree': prior_sha,
        'parent_inventory_path': str(args.before.resolve()),
        'parent_inventory_sha256': hashlib.sha256(args.before.read_bytes()).hexdigest(),
        'article_tree_sha': current_value['article_tree_sha'],
        'file_count': len(rows), 'bytes': sum(row['bytes'] for row in rows),
        'changed_paths': [row['path'] for row in changed],
        'modified_existing_paths': modified, 'added_paths': added, 'removed_paths': [],
        'allowed_added_prefixes': [args.publication_prefix, args.source_gate_prefix],
        'frozen_inputs_unchanged': True, 'source_manifest_sha256': args.manifest_sha256,
        'workflow_sha256': args.workflow_sha256, 'manifest_verification': manifest_result,
        'new_blob_uploads': len(large_by_sha),
        'new_blob_upload_bytes': sum(row['bytes'] for row in large_by_sha.values()),
        'tree_batches': len(plan), 'remote_mutations_performed': False,
        'ci_result_verified_by_this_adapter': False,
        'scope': ('Local byte/delta/source gates and canonical Git Data payloads only. '
                  'The parent commit and any CI outcome require separate actual remote '
                  'readback receipts; no CI success or publication is inferred here.'),
    }
    write('DELTA_SCOPE', scope)
    print(json.dumps({key: value for key, value in scope.items()
                      if key not in ('changed_paths', 'added_paths', 'manifest_verification')}))


if __name__ == '__main__':
    main()
