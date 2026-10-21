#!/usr/bin/env python3
"""Read-only baseline preservation census; write receipts only to --output-dir.

This checks bytes, Git blob IDs, sizes, and Git file modes. It does not run
mathematical tests, compile sources, change article files, or qualify CI.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import stat
import sys

BASELINE_COMMIT = '15ad3962de63f50911b765fe6608e722fe9b8c82'
BASELINE_ROOT_TREE = 'a1eccaf41b953cbcba430cf0ecf78195771db4a8'
BASELINE_ARTICLE_TREE = '39f02eb2dab466bb742c7f96139a6535d7bb10ef'
BASELINE_COUNT = 1645
OLD_NAME = 'A2-DYN-global-minimizer-localization-author-revision'
NEW_NAME = 'A2-DYN-physical-tube-source-height-author-revision'


def now():
    return datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')


def git_id(kind, body):
    return hashlib.sha1(kind.encode() + b' ' + str(len(body)).encode() + b'\0' + body).hexdigest()


def stable_read(path):
    for _ in range(3):
        before = path.lstat()
        if not stat.S_ISREG(before.st_mode):
            raise ValueError('not a regular file: ' + str(path))
        body = path.read_bytes()
        after = path.lstat()
        fields = ('st_dev', 'st_ino', 'st_size', 'st_mtime_ns', 'st_ctime_ns', 'st_mode')
        if all(getattr(before, key) == getattr(after, key) for key in fields):
            if len(body) != after.st_size:
                raise ValueError('read length differs from stable stat: ' + str(path))
            return body, {
                'git_blob': git_id('blob', body),
                'sha256': hashlib.sha256(body).hexdigest(),
                'bytes': len(body),
                'mode': '100755' if after.st_mode & 0o111 else '100644',
            }
    raise ValueError('file changed during three reads: ' + str(path))


def tree_from_rows(rows):
    root = {}
    seen = set()
    for row in rows:
        rel = PurePosixPath(row['path'])
        if rel.is_absolute() or '..' in rel.parts or str(rel) != row['path']:
            raise ValueError('unsafe or noncanonical baseline path: ' + row['path'])
        if row['path'] in seen:
            raise ValueError('duplicate baseline path: ' + row['path'])
        seen.add(row['path'])
        if row['type'] != 'blob' or row['mode'] not in ('100644', '100755'):
            raise ValueError('unexpected baseline entry type/mode: ' + row['path'])
        if not re.fullmatch(r'[0-9a-f]{40}', row['sha']):
            raise ValueError('invalid baseline Git blob ID: ' + row['path'])
        if not isinstance(row['size'], int) or row['size'] < 0:
            raise ValueError('invalid baseline byte length: ' + row['path'])
        node = root
        for part in rel.parts[:-1]:
            node = node.setdefault(part, {})
            if not isinstance(node, dict):
                raise ValueError('baseline directory/file collision')
        if rel.name in node:
            raise ValueError('baseline directory/file collision')
        node[rel.name] = (row['mode'], row['sha'])

    def fold(node):
        entries = []
        for name, value in node.items():
            encoded = name.encode('utf-8')
            if isinstance(value, dict):
                mode, sha, key = '40000', fold(value), encoded + b'/'
            else:
                mode, sha = value
                key = encoded
            entries.append((key, mode.encode() + b' ' + encoded + b'\0' + bytes.fromhex(sha)))
        return git_id('tree', b''.join(record for _, record in sorted(entries)))

    return fold(root)


def expected_matches(row, actual):
    return (actual['git_blob'] == row['sha'] and actual['bytes'] == row['size']
            and actual['mode'] == row['mode'])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--baseline-blobs', type=Path, required=True)
    parser.add_argument('--old-article', type=Path, required=True)
    parser.add_argument('--new-article', type=Path, required=True)
    parser.add_argument('--output-dir', type=Path, required=True)
    args = parser.parse_args()
    started = now()
    old = args.old_article.resolve()
    new = args.new_article.resolve()
    out = args.output_dir.resolve()
    if old == new or out == old or out == new or old in out.parents or new in out.parents:
        raise ValueError('output must be outside both articles; article roots must differ')
    receipt_body, receipt_identity = stable_read(args.baseline_blobs.resolve())
    rows = json.loads(receipt_body)
    if len(rows) != BASELINE_COUNT:
        raise ValueError('baseline file count differs from pinned 1,645')
    baseline_tree = tree_from_rows(rows)
    if baseline_tree != BASELINE_ARTICLE_TREE:
        raise ValueError('baseline blob list does not reproduce the pinned article Git tree')

    new_files = sorted(p for p in new.rglob('*') if p.is_file() and not p.is_symlink())
    new_by_path = {}
    candidates = defaultdict(list)
    read_errors = []
    for path in new_files:
        rel = path.relative_to(new).as_posix()
        try:
            _, identity = stable_read(path)
            new_by_path[rel] = identity
            candidates[(identity['git_blob'], identity['bytes'], identity['mode'])].append(rel)
        except (OSError, ValueError) as exc:
            read_errors.append({'path': rel, 'error': str(exc)})

    classified = []
    old_mismatches = []
    race_errors = []
    for baseline in sorted(rows, key=lambda row: row['path']):
        rel = baseline['path']
        entry = {
            'path': rel,
            'baseline': {'commit': BASELINE_COMMIT, 'git_blob': baseline['sha'],
                         'bytes': baseline['size'], 'mode': baseline['mode']},
        }
        try:
            old_body, old_identity = stable_read(old / rel)
            entry['predecessor_current'] = old_identity
            entry['predecessor_matches_baseline'] = expected_matches(baseline, old_identity)
        except (OSError, ValueError) as exc:
            old_body, old_identity = None, None
            entry['predecessor_current'] = {'error': str(exc)}
            entry['predecessor_matches_baseline'] = False
        if not entry['predecessor_matches_baseline']:
            old_mismatches.append(rel)
        entry['new_at_original_path'] = new_by_path.get(rel)
        key = (baseline['sha'], baseline['size'], baseline['mode'])
        exact_copies = []
        for candidate in sorted(candidates.get(key, []), key=lambda p: (p != rel, p)):
            try:
                new_body, candidate_identity = stable_read(new / candidate)
                if candidate_identity != new_by_path[candidate]:
                    raise ValueError('candidate changed after inventory')
                if old_body is None or new_body != old_body:
                    raise ValueError('candidate is not byte-identical to verified predecessor')
                exact_copies.append({'path': candidate, **candidate_identity,
                                     'bytes_compared_to_predecessor': True})
            except (OSError, ValueError) as exc:
                race_errors.append({'baseline_path': rel, 'candidate': candidate, 'error': str(exc)})
        entry['exact_locations_in_new_article'] = exact_copies
        if any(copy['path'] == rel for copy in exact_copies):
            entry['classification'] = 'unchanged_at_original_path'
        elif exact_copies:
            entry['classification'] = 'preserved_exact_at_retained_path'
        else:
            entry['classification'] = 'missing_exact_copy_in_new_article'
        classified.append(entry)

    counts = dict(Counter(row['classification'] for row in classified))
    missing = [row['path'] for row in classified if row['classification'] == 'missing_exact_copy_in_new_article']
    baseline_paths = {row['path'] for row in rows}
    old_extra = sorted(p.relative_to(old).as_posix() for p in old.rglob('*')
                       if p.is_file() and p.relative_to(old).as_posix() not in baseline_paths)
    protected = [row for row in classified if re.match(r'core/(?:26[0-9]|27[0-9]|28[0-9]|29[0-9]|30[0-9])_', row['path'])]
    protected_aux = ['angular-source-audit.tex', 'clearance-audit.tex', 'comparison-scope.tex',
                     'critical-roof-audit.tex', 'cross-flight-audit.tex', 'inputs.tex', 'model.tex',
                     'retained-geometric-input.tex']
    aux_rows = [row for row in classified if row['path'] in protected_aux]
    native_in_place = len(protected) == 50 and len(aux_rows) == 8 and all(
        row['classification'] == 'unchanged_at_original_path' for row in protected + aux_rows)
    passed = not old_mismatches and not missing and not read_errors and not race_errors and native_in_place
    result = {
        'schema': 'A2-DYN-final-baseline-preservation-v1',
        'started_at_utc': started,
        'finished_at_utc': now(),
        'status': 'PASS' if passed else 'FAIL',
        'read_only_scope': 'No article file, Git ref, or workflow was written. This receipt checks historical preservation only; it does not certify mathematical proofs, builds, CI, or publication.',
        'baseline': {'commit': BASELINE_COMMIT, 'root_tree': BASELINE_ROOT_TREE,
                     'article_tree': BASELINE_ARTICLE_TREE, 'article_path': 'papers/' + OLD_NAME,
                     'blob_receipt': str(args.baseline_blobs.resolve()),
                     'blob_receipt_identity': receipt_identity,
                     'canonical_tree_recomputed': baseline_tree,
                     'file_count': len(rows), 'total_bytes': sum(row['size'] for row in rows)},
        'local_roots': {'predecessor': str(old), 'new_article': str(new)},
        'new_article_files_observed': len(new_files),
        'classification_counts': counts,
        'predecessor_exact_files': len(rows) - len(old_mismatches),
        'predecessor_mismatches': old_mismatches,
        'predecessor_unlisted_local_paths': old_extra,
        'missing_exact_new_article_paths': missing,
        'read_errors': read_errors,
        'candidate_changed_during_read_errors': race_errors,
        'protected_native': {'core_260_309_files': len(protected), 'model_and_input_files': len(aux_rows),
                             'all_58_unchanged_at_original_paths': native_in_place},
        'paths': classified,
    }
    out.mkdir(parents=True, exist_ok=True)
    receipt_path = out / 'BASELINE_PRESERVATION_CLASSIFICATION.json'
    encoded = (json.dumps(result, indent=2, ensure_ascii=False) + '\n').encode()
    receipt_path.write_bytes(encoded)
    changed = [row for row in classified if row['classification'] != 'unchanged_at_original_path']
    summary = [
        '# Final predecessor preservation census', '',
        f"**Status: {result['status']}.** Observation completed at {result['finished_at_utc']}.", '',
        f"The fixed predecessor is commit `{BASELINE_COMMIT}`, root tree `{BASELINE_ROOT_TREE}`, article tree `{BASELINE_ARTICLE_TREE}`. Its complete 1,645-file blob list independently recomputes that article Git tree.", '',
        f"All {result['predecessor_exact_files']:,} of the {len(rows):,} published predecessor files were read from the predecessor article and compared with their pinned Git blob ID, byte count, and Git file mode. Every retained new-article location listed in the JSON was also compared byte for byte with its verified predecessor file.", '',
        '| Preservation class | Baseline paths |', '| --- | ---: |',
        f"| Exact at original path in new article | {counts.get('unchanged_at_original_path', 0):,} |",
        f"| Exact at a retained path in new article | {counts.get('preserved_exact_at_retained_path', 0):,} |",
        f"| Missing exact copy in new article | {len(missing):,} |",
        f"| Predecessor mismatches | {len(old_mismatches):,} |", '',
        f"The 50 core files 260–309 and all eight model/input source files remain byte-identical at their active paths: **{'PASS' if native_in_place else 'FAIL'}**.", '',
        '## Paths with changed current content and exact retained copies', '',
        '| Baseline path | Exact retained location in new article | Baseline Git blob |',
        '| --- | --- | --- |',
    ]
    for row in changed:
        locations = '<br>'.join('`' + copy['path'] + '`' for copy in row['exact_locations_in_new_article']) or '**MISSING**'
        summary.append(f"| `{row['path']}` | {locations} | `{row['baseline']['git_blob']}` |")
    summary += [
        '', '## Interpretation and reproducibility', '',
        'The retained predecessor documents include the exact earlier source manifest, proof index, proof ledger, main manuscript, response, audit documents, and source identity record. The earlier proof navigation remains under its dedicated history directory. Historical main/supplement logs and PDFs regenerated during this revision are covered by their exact earlier execution-log and delivery copies.', '',
        'This is a path-level preservation check. It records the snapshot of baseline paths and their retained copies; newly created execution, delivery, or publication receipts may continue to accumulate. It does not assert a new mathematical theorem, replace proof review, or claim a current-head CI pass.', '',
        f"The predecessor contains {len(old_extra):,} local files outside the pinned 1,645-file publication list; those paths, if any, are separately enumerated in the JSON and are not silently added to the published source identity.", '',
        'Reproduce with Python 3 using the saved verifier and these explicit read-only inputs:', '', '```bash',
        'python verify_baseline_preservation.py \\',
        f"  --baseline-blobs '{args.baseline_blobs.resolve()}' \\",
        f"  --old-article '{old}' \\",
        f"  --new-article '{new}' \\",
        f"  --output-dir '{out}'", '```', '',
        f"Path-level JSON SHA-256: `{hashlib.sha256(encoded).hexdigest()}`.", '',
    ]
    (out / 'BASELINE_PRESERVATION_SUMMARY.md').write_text('\n'.join(summary), encoding='utf-8')
    compact = {key: result[key] for key in ['status', 'finished_at_utc', 'classification_counts',
               'predecessor_exact_files', 'predecessor_mismatches', 'missing_exact_new_article_paths',
               'read_errors', 'candidate_changed_during_read_errors', 'protected_native']}
    compact.update({'json_sha256': hashlib.sha256(encoded).hexdigest(),
                    'json_bytes': len(encoded), 'summary_path': str(out / 'BASELINE_PRESERVATION_SUMMARY.md')})
    print(json.dumps(compact, sort_keys=True))
    return 0 if passed else 1


if __name__ == '__main__':
    sys.exit(main())
