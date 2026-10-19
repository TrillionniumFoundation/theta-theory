#!/usr/bin/env python3
"""Recheck retained GitHub source receipts against an unchanged local baseline.

This verifies source identity and census coverage. It is not a mathematical proof.
No network call or mutation of the baseline is performed.
"""
from __future__ import annotations
import argparse
import datetime
import hashlib
import json
import re
from pathlib import Path


def load(path: Path):
    return json.loads(path.read_text(encoding='utf-8'))


def git_blob(data: bytes) -> str:
    return hashlib.sha1(b'blob ' + str(len(data)).encode('ascii') + b'\0' + data).hexdigest()


def git_tree(entries: list[dict]) -> str:
    def key(row):
        return (row['path'] + ('/' if row['type'] == 'tree' else '')).encode('utf-8')
    raw = b''.join(
        row['mode'].lstrip('0').encode('ascii') + b' ' + row['path'].encode('utf-8')
        + b'\0' + bytes.fromhex(row['sha']) for row in sorted(entries, key=key)
    )
    return hashlib.sha1(b'tree ' + str(len(raw)).encode('ascii') + b'\0' + raw).hexdigest()


def need(condition: bool, message: str):
    if not condition:
        raise RuntimeError(message)


def run(audit: Path, baseline: Path) -> dict:
    branches = load(audit / 'ALL_BRANCHES_READBACK.json')
    current = {row['name']: row['commit']['sha'] for row in branches['branches']}
    need(len(current) == branches['count'] == 1287, 'Incomplete or duplicate branch census')
    need(branches['pages'][-1] == {'page': 14, 'records': 0}, 'Pagination not closed')
    old = {row['name']: row['commit']['sha'] for row in load(baseline / 'history/all-branches.json')['branches']}
    added = sorted(current.keys() - old.keys())
    removed = sorted(old.keys() - current.keys())
    moved = sorted(name for name in current.keys() & old.keys() if current[name] != old[name])
    need(not removed and not moved, 'A previous ref was removed or moved')
    need(len(added) == 4, 'Unexpected branch delta')
    a2dyn = {name: sha for name, sha in current.items() if re.search(r'a2-?dyn', name, re.I)}
    author_refs = {name: sha for name, sha in a2dyn.items() if not name.startswith('review/')}
    review_refs = {name: sha for name, sha in a2dyn.items() if name.startswith('review/')}
    commits = load(audit / 'ALL_AUTHOR_COMMIT_READBACKS.json')['commits']
    need(set(author_refs.values()) == {row['response']['sha'] for row in commits}, 'Author commit coverage mismatch')
    need(len(author_refs) == 245 and len(commits) == 128 and len(review_refs) == 178, 'Ref class count mismatch')
    tree_checks = []
    for filename in ['ALL_AUTHOR_ROOT_TREE_READBACKS.json', 'ALL_AUTHOR_PAPERS_TREE_READBACKS.json',
                     'ALL_AUTHOR_ARTICLE_TREE_READBACKS.json', 'ALL_AUTHOR_CORE_TREE_READBACKS.json',
                     'BASELINE_ARTICLE_NONRECURSIVE_TREES.json', 'SUMMABLE_PREDECESSOR_COMPLETE_TREE_READBACK.json']:
        for row in load(audit / filename)['trees']:
            response = row['response']
            need(not response.get('truncated'), f'Truncated tree in {filename}')
            expected = row.get('canonical_tree_sha', row['requested_sha'])
            actual = git_tree(response['tree'])
            need(actual == expected, f'Canonical Git tree identity mismatch: {filename}, {expected}, {actual}')
            tree_checks.append({'receipt': filename, 'requested_sha': row['requested_sha'], 'canonical_tree_sha': expected, 'verified': True})
    remote_rows = load(audit / 'BASELINE_ARTICLE_BLOBS.json')
    for row in remote_rows:
        path = baseline / row['path']
        need(path.is_file() and not path.is_symlink(), f'Missing or symlinked baseline source {row["path"]}')
        data = path.read_bytes()
        need(len(data) == row['size'] and git_blob(data) == row['sha'], f'Baseline blob mismatch {row["path"]}')
        mode = '100755' if path.stat().st_mode & 0o100 else '100644'
        need(mode == row['mode'], f'Baseline mode mismatch {row["path"]}')
    variants = load(audit / 'NUMBERED_NATIVE_VARIANT_WITNESSES.json')['variants']
    anchor = load(baseline / 'history/IMMUTABLE_SOURCE_ANCHOR.json')
    old_variants = {row['git_blob'] for row in anchor['groups']['numbered_variants']['files']}
    native_now = {git_blob(path.read_bytes()) for path in (baseline / 'core').glob('*.tex')}
    need({row['sha'] for row in variants} == old_variants | native_now, 'Native variant union differs from retained complete sources')
    need(len(variants) == 361 and len(old_variants) == 355 and len(native_now) == 50, 'Native variant counts changed')
    predecessor = load(audit / 'SUMMABLE_PREDECESSOR_COMPLETE_TREE_READBACK.json')
    prior_remote = {row['path']: row for row in predecessor['blobs']}
    prior_root = baseline / 'history/predecessor-source'
    prior_manifest = load(prior_root / 'SOURCE_MANIFEST.json')
    prior_listed = {row['path']: row for row in prior_manifest['files']}
    present = sorted(prior_remote.keys() & prior_listed.keys())
    missing = sorted(prior_listed.keys() - prior_remote.keys())
    unlisted = sorted(prior_remote.keys() - prior_listed.keys())
    for rel, row in prior_remote.items():
        data = (prior_root / rel).read_bytes()
        need(git_blob(data) == row['sha'] and len(data) == row['size'], f'Predecessor snapshot differs from old actual tree: {rel}')
        if rel in prior_listed:
            need(row['sha'] == prior_listed[rel]['git_blob'] and len(data) == prior_listed[rel]['bytes'] and hashlib.sha256(data).hexdigest() == prior_listed[rel]['sha256'], f'Present original manifest entry differs: {rel}')
    need((len(prior_remote), len(prior_listed), len(present), len(missing), len(unlisted)) == (103, 982, 101, 881, 2), 'Original manifest discrepancy changed')
    return {
        'observed_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'scope': 'Read-only source identity and complete current-ref census; no continuum theorem certification',
        'baseline_commit': '15ad3962de63f50911b765fe6608e722fe9b8c82',
        'branch_counts': {'all': len(current), 'a2dyn': len(a2dyn), 'author': len(author_refs), 'report': len(review_refs), 'author_heads': len(commits)},
        'added_refs': added, 'removed_refs': removed, 'moved_refs': moved,
        'canonical_git_tree_checks': len(tree_checks), 'tree_checks': tree_checks,
        'baseline_matched_files': len(remote_rows),
        'numbered_native_variants': len(variants), 'previous_numbered_variants': len(old_variants), 'native_current_cores': len(native_now),
        'predecessor_manifest': {'actual_files': len(prior_remote), 'listed': len(prior_listed), 'present_exact': len(present), 'missing': missing, 'actual_unlisted': unlisted},
        'verified': True,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--baseline', type=Path, required=True)
    parser.add_argument('--audit', type=Path, default=Path(__file__).resolve().parent)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    result = run(args.audit.resolve(), args.baseline.resolve())
    out = args.output or args.audit / 'SOURCE_CENSUS_VERIFICATION.json'
    out.write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({key: value for key, value in result.items() if key not in ('tree_checks', 'predecessor_manifest')}, indent=2))
    print(json.dumps({'predecessor_manifest_counts': {key: len(value) if isinstance(value, list) else value for key, value in result['predecessor_manifest'].items()}}, indent=2))


if __name__ == '__main__':
    main()
