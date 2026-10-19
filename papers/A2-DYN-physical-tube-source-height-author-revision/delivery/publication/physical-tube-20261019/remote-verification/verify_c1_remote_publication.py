#!/usr/bin/env python3
"""Verify immutable C1 Git tree readbacks and the observed branch census.

Inputs are saved API responses and the exact local publication transport list.
No network request, article write, or Git ref mutation is performed here.
"""
from __future__ import annotations
import argparse
from collections import defaultdict
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import sys

C1 = '706aa8d1bca33b0d6268806cca873d57511ad8d9'
BASE = '15ad3962de63f50911b765fe6608e722fe9b8c82'
BASE_ROOT = 'a1eccaf41b953cbcba430cf0ecf78195771db4a8'
ROOT = 'ae3eca89e4210f2a9a44d52493c22df111b75d66'
ARTICLE = 'b0c173ad4f974576d0f639e18b77fe16fbab6ff6'
ARTICLE_NAME = 'A2-DYN-physical-tube-source-height-author-revision'
WORKFLOW = 'a2-dyn-physical-tube-source-height-20261019.yml'
REF_SUFFIX = 'a2-dyn-physical-tube-source-height-2026-10-19'
NEW_REFS = {prefix + '/' + REF_SUFFIX for prefix in ('revision', 'referee-copy', 'referee-response')}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def read(path):
    return json.loads(path.read_text(encoding='utf-8'))


def file_identity(path):
    body = path.read_bytes()
    return {'bytes': len(body), 'sha256': hashlib.sha256(body).hexdigest()}


def canonical_tree(response):
    require(response.get('truncated') is False, 'Tree is truncated or has no truncation receipt')
    records = []
    seen = set()
    for entry in response['tree']:
        name = entry['path']
        require('/' not in name and name not in ('', '.', '..'), 'Not a nonrecursive tree entry')
        require(name not in seen, 'Duplicate tree name')
        seen.add(name)
        require(re.fullmatch(r'[0-9a-f]{40}', entry['sha']) is not None, 'Invalid Git object ID')
        encoded = name.encode('utf-8')
        is_dir = entry['type'] == 'tree'
        require(entry['type'] in ('tree', 'blob'), 'Unexpected Git entry type')
        mode = entry['mode'].lstrip('0')
        require((mode == '40000') == is_dir, 'Tree type/mode mismatch')
        record = mode.encode() + b' ' + encoded + b'\0' + bytes.fromhex(entry['sha'])
        records.append((encoded + (b'/' if is_dir else b''), record))
    body = b''.join(record for _, record in sorted(records))
    return hashlib.sha1(b'tree ' + str(len(body)).encode() + b'\0' + body).hexdigest()


def entry_signature(entry):
    return {key: entry.get(key) for key in ('mode', 'type', 'sha', 'size')}


def tree_delta(before, after):
    a = {entry['path']: entry for entry in before['tree']}
    b = {entry['path']: entry for entry in after['tree']}
    return {
        'before_count': len(a), 'after_count': len(b),
        'removed': sorted(set(a) - set(b)),
        'added': [b[path] for path in sorted(set(b) - set(a))],
        'changed': [{'path': path, 'before': entry_signature(a[path]), 'after': entry_signature(b[path])}
                    for path in sorted(set(a) & set(b)) if entry_signature(a[path]) != entry_signature(b[path])],
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--work-dir', type=Path, required=True)
    args = parser.parse_args()
    work = args.work_dir.resolve()
    out = work / 'remote-verification'
    transport_path = work / 'TRANSPORT_TO_PUBLISH.json'
    expected_path = work / 'ROOT_PUBLICATION_EXPECTED.json'
    base_path = work / 'ROOT_PUBLICATION_BASE_TREES.json'
    old_branches_path = work / 'source-audit/ALL_BRANCHES_READBACK.json'
    transport, expected, base = read(transport_path), read(expected_path), read(base_path)
    article_walk = read(out / 'C1_ARTICLE_TREE_WALK.json')
    controls = read(out / 'C1_CONTROL_TREE_READBACKS.json')
    old_branches = read(old_branches_path)
    branches = read(out / 'ALL_BRANCHES_AFTER_C1.json')
    require(article_walk['commit'] == C1 and article_walk['article_tree'] == ARTICLE, 'Wrong article walk identity')
    require(not article_walk['fetch_errors'] and not article_walk['unfetched_queue'], 'Incomplete tree walk')
    require(transport['article_tree_sha'] == ARTICLE and transport['file_count'] == 1964, 'Wrong transport identity')
    commit = controls['commit']['response']
    require(commit['sha'] == C1, 'Wrong C1 commit')
    require(commit['tree']['sha'] == ROOT, 'C1 commit points to unexpected root')
    require([row['sha'] for row in commit['parents']] == [BASE], 'C1 parent differs from pinned baseline')

    canonical_rows = []
    all_trees = article_walk['trees']
    for sha, record in all_trees.items():
        response = record['response']
        actual = canonical_tree(response)
        require(response['sha'] == sha and actual == sha, 'Article subtree canonical ID mismatch: ' + sha)
        canonical_rows.append({'role': 'article', 'expected_sha': sha, 'computed_sha': actual,
                               'entries': len(response['tree']), 'observed_at': record['observed_at']})
    remote_rows = []
    tree_placements = []
    visited = set()

    def walk(sha, prefix='', ancestors=()):
        require(sha not in ancestors, 'Cycle in saved Git tree graph')
        require(sha in all_trees, 'Missing reachable subtree: ' + sha)
        visited.add(sha)
        tree_placements.append({'path': prefix.rstrip('/') or '.', 'sha': sha})
        for entry in all_trees[sha]['response']['tree']:
            path = prefix + entry['path']
            if entry['type'] == 'tree':
                walk(entry['sha'], path + '/', ancestors + (sha,))
            else:
                remote_rows.append({'path': path, **entry_signature(entry)})
    walk(ARTICLE)
    require(visited == set(all_trees), 'Saved tree walk contains unreachable or missing trees')
    expected_files = {row['path']: row for row in transport['files']}
    remote_files = {row['path']: row for row in remote_rows}
    require(len(expected_files) == len(transport['files']) == 1964, 'Transport duplicates or count error')
    require(len(remote_files) == len(remote_rows), 'Remote path duplication')
    missing = sorted(set(expected_files) - set(remote_files))
    extra = sorted(set(remote_files) - set(expected_files))
    comparisons, mismatches = [], []
    for path in sorted(set(expected_files) | set(remote_files)):
        local = expected_files.get(path)
        remote = remote_files.get(path)
        want = None if local is None else {'mode': local['mode'], 'type': local['type'], 'sha': local['sha'], 'size': local['bytes']}
        actual = None if remote is None else entry_signature(remote)
        row = {'path': path, 'transport': want, 'remote': actual, 'matches': want == actual,
               'transport_sha256': None if local is None else local['sha256']}
        comparisons.append(row)
        if not row['matches']:
            mismatches.append(path)
    require(not missing and not extra and not mismatches, 'Remote article differs from transport list')
    remote_bytes = sum(row['size'] for row in remote_rows)
    require(remote_bytes == transport['bytes'], 'Total remote byte count differs from transport')

    top = {key: row['response'] for key, row in controls['trees'].items()}
    expected_top = {'root': ROOT, 'papers': expected['papers_tree'], '.github': expected['github_tree'],
                    'workflows': expected['workflows_tree']}
    for key, sha in expected_top.items():
        actual = canonical_tree(top[key])
        require(top[key]['sha'] == sha and actual == sha, 'Current top tree mismatch: ' + key)
        canonical_rows.append({'role': 'current_' + key, 'expected_sha': sha, 'computed_sha': actual,
                               'entries': len(top[key]['tree'])})
    base_key = {'root': 'root', 'papers': 'papers', '.github': 'github', 'workflows': 'workflows'}
    for key, source_key in base_key.items():
        response = base[source_key]
        sha = BASE_ROOT if key == 'root' else response['sha']
        actual = canonical_tree(response)
        require(actual == sha, 'Baseline top tree canonical ID mismatch: ' + key)
        canonical_rows.append({'role': 'baseline_' + key, 'expected_sha': sha, 'computed_sha': actual,
                               'entries': len(response['tree'])})
    deltas = {key: tree_delta(base[source_key], top[key]) for key, source_key in base_key.items()}
    require(not deltas['root']['removed'] and not deltas['root']['added'] and
            {row['path'] for row in deltas['root']['changed']} == {'.github', 'papers'}, 'Unexpected root scope')
    require(not deltas['papers']['removed'] and not deltas['papers']['changed'] and
            [row['path'] for row in deltas['papers']['added']] == [ARTICLE_NAME], 'Unexpected papers scope')
    require(deltas['papers']['added'][0]['sha'] == ARTICLE, 'New article is attached at wrong tree')
    require(not deltas['.github']['removed'] and not deltas['.github']['added'] and
            [row['path'] for row in deltas['.github']['changed']] == ['workflows'], 'Unexpected .github scope')
    require(not deltas['workflows']['removed'] and not deltas['workflows']['changed'] and
            [row['path'] for row in deltas['workflows']['added']] == [WORKFLOW], 'Unexpected workflow scope')
    require((deltas['papers']['before_count'], deltas['papers']['after_count']) == (211, 212), 'Wrong paper counts')
    require((deltas['workflows']['before_count'], deltas['workflows']['after_count']) == (173, 174), 'Wrong workflow counts')
    workflow_entry = deltas['workflows']['added'][0]
    require(workflow_entry['sha'] == expected_files['ci/' + WORKFLOW]['sha'], 'Top workflow differs from article copy')

    before = {row['name']: row['commit']['sha'] for row in old_branches['branches']}
    after = {row['name']: row['commit']['sha'] for row in branches['branches']}
    require(len(before) == len(old_branches['branches']) == 1287, 'Wrong baseline branch census')
    require(len(after) == len(branches['branches']), 'Duplicate branches in current pagination')
    require(branches['pages'][-1]['records'] == 0, 'No empty final branch page')
    require([page['page'] for page in branches['pages']] == list(range(1, len(branches['pages']) + 1)), 'Branch page gap')
    removed = sorted(set(before) - set(after))
    added = [{'name': name, 'sha': after[name]} for name in sorted(set(after) - set(before))]
    moved = [{'name': name, 'before': before[name], 'after': after[name]} for name in sorted(set(before) & set(after))
             if before[name] != after[name]]
    is_a2 = lambda name: bool(re.search(r'a2[-_]dyn', name, re.IGNORECASE))
    a2_before = [name for name in before if is_a2(name)]
    a2_moved = [row for row in moved if is_a2(row['name'])]
    a2_removed = [name for name in removed if is_a2(name)]
    added_a2 = {row['name'] for row in added if is_a2(row['name'])}
    require(not removed, 'A pre-existing ref disappeared')
    require(not a2_moved and not a2_removed, 'A pre-existing A2-DYN ref moved or disappeared')
    require(added_a2 == NEW_REFS, 'New A2-DYN refs differ from authorized three-ref publication')
    require(all(after[name] == C1 for name in NEW_REFS), 'C1 branch census did not observe C1 at all three new refs')
    ref_result = {
        'status': 'PASS_FOR_PREEXISTING_A2_DYN_REFS_WITH_UNRELATED_REF_MOVEMENT' if moved else 'PASS',
        'old_census_observed_utc': old_branches['observed_utc'],
        'current_census_observed_started_utc': branches['observed_started_utc'],
        'current_census_observed_finished_utc': branches['observed_finished_utc'],
        'old_count': len(before), 'current_count': len(after), 'preexisting_a2_dyn_count': len(a2_before),
        'removed': removed, 'added': added, 'moved': moved,
        'preexisting_a2_dyn_moved': a2_moved, 'preexisting_a2_dyn_removed': a2_removed,
        'scope_note': 'An unrelated-named pre-existing ref movement is reported as observed; no attribution is inferred. This census is time-scoped and is not a statement about subsequent C2 or later fast-forwards.',
    }
    all_pass = not mismatches and not a2_moved and not removed
    result = {
        'schema': 'A2-DYN-C1-independent-remote-publication-verification-v1',
        'verified_at_utc': datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z'),
        'status': 'PASS_WITH_OBSERVED_UNRELATED_REF_MOVEMENT' if moved else 'PASS',
        'source_publication_status': 'PASS' if all_pass else 'FAIL',
        'c1_commit': C1, 'parent': BASE, 'root_tree': ROOT, 'article_tree': ARTICLE,
        'remote_article_file_count': len(remote_rows), 'remote_article_bytes': remote_bytes,
        'distinct_article_subtrees': len(all_trees), 'article_tree_placements': len(tree_placements),
        'canonical_tree_checks': len(canonical_rows),
        'path_identity_mismatches': mismatches, 'missing_paths': missing, 'extra_paths': extra,
        'transport_receipt_identity': file_identity(transport_path),
        'baseline_top_receipt_identity': file_identity(base_path),
        'expected_top_receipt_identity': file_identity(expected_path),
        'baseline_branch_receipt_identity': file_identity(old_branches_path),
        'root_isolation': deltas, 'branch_isolation': ref_result,
        'canonical_trees': canonical_rows, 'article_tree_paths': tree_placements,
        'file_comparisons': comparisons,
        'verification_boundary': 'Every reachable article subtree was independently fetched through nonrecursive Git tree API calls. All 1,964 file modes, sizes, and Git blob IDs match the local byte-derived transport list; every returned tree ID was canonically recomputed. This step did not download all 1,964 blob bodies again, rerun mathematics, qualify CI, or verify subsequent metadata-only commits.',
    }
    encoded = (json.dumps(result, indent=2) + '\n').encode()
    (out / 'C1_REMOTE_VERIFICATION.json').write_bytes(encoded)
    (out / 'C1_REF_ISOLATION.json').write_text(json.dumps(ref_result, indent=2) + '\n', encoding='utf-8')
    summary = [
        '# Independent C1 remote publication verification', '',
        f"**Source publication: PASS.** Verified at {result['verified_at_utc']}.", '',
        f"Commit `{C1}` has parent `{BASE}`, root tree `{ROOT}`, and new article tree `{ARTICLE}`.", '',
        '| Verification | Result |', '| --- | --- |',
        f"| Remote article files compared with the exact transport list | {len(remote_rows):,} |",
        f"| Remote article bytes represented | {remote_bytes:,} |",
        f"| Distinct article subtrees fetched nonrecursively | {len(all_trees):,} |",
        f"| Canonical tree hashes recomputed, including current and baseline top trees | {len(canonical_rows):,}; all match |",
        '| Missing, extra, or mismatched article file identities | 0 |',
        '| Existing paper subtrees changed or removed | 0 |',
        '| Existing workflows changed or removed | 0 |',
        '| Papers | 211 → 212; the new A2-DYN article is the sole addition |',
        '| Workflows | 173 → 174; the new dedicated workflow is the sole addition |', '',
        'The root changes only the `papers` and `.github` tree pointers. Within `.github`, only the `workflows` tree pointer changes. Every pre-existing sibling entry remains exact, including the complete predecessor article and all companion papers. The newly added workflow blob matches the copy carried inside the article.', '',
        '## Branch census', '',
        f"The saved branch census contains {len(after):,} distinct refs, compared with {len(before):,} in the initial census. It observes exactly the three authorized new A2-DYN refs, each at C1. All {len(a2_before):,} pre-existing A2-DYN refs remain unchanged, and no pre-existing ref is missing.", '',
    ]
    if moved:
        summary += ['A movement of a pre-existing unrelated-named ref was also observed and is explicitly retained:', '',
                    '| Ref | Initial head | Later observed head |', '| --- | --- | --- |']
        summary += [f"| `{row['name']}` | `{row['before']}` | `{row['after']}` |" for row in moved]
        summary += ['', 'The receipt makes no attribution for that movement and does not claim that all repository refs were stationary.', '']
    summary += [
        '## Scope and reproduction', '',
        'The file comparison uses remotely returned modes, sizes, and Git blob IDs against the transport list computed from the publication bytes. Canonical recomputation verifies all returned tree identities. It does not claim a second download of every blob body, a new mathematical validation, a current-head CI pass, or validation of later metadata-only commits.', '',
        'Reproduce the saved-response checks with:', '', '```bash',
        f"python verify_c1_remote_publication.py --work-dir '{work}'", '```', '',
        f"Full path-level result SHA-256: `{hashlib.sha256(encoded).hexdigest()}`.", '',
    ]
    (out / 'C1_REMOTE_VERIFICATION_SUMMARY.md').write_text('\n'.join(summary), encoding='utf-8')
    print(json.dumps({'status': result['status'], 'source_publication_status': result['source_publication_status'],
                      'remote_article_file_count': len(remote_rows), 'remote_article_bytes': remote_bytes,
                      'distinct_article_subtrees': len(all_trees), 'canonical_tree_checks': len(canonical_rows),
                      'preexisting_a2_dyn_refs_unchanged': len(a2_before), 'unrelated_ref_movements': moved,
                      'result_sha256': hashlib.sha256(encoded).hexdigest()}, sort_keys=True))
    return 0


if __name__ == '__main__':
    sys.exit(main())
