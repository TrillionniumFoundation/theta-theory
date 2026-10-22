#!/usr/bin/env python3
"""Read local evidence and prepare Git Data requests; never writes the repository or Git.

The fixed source release, its complete predecessor, and the workflow are anchors.
Prepare-only mode permits an explicitly stale delivery manifest; final mode does not.
This program has no network calls, blob upload, commit, ref, or index mutation.
"""
from __future__ import annotations

import argparse
import base64
import codecs
from collections import defaultdict
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import stat
import subprocess
import sys

HERE = Path(__file__).resolve().parent
LIMIT = 16 * 1024 * 1024
MARGIN = 64 * 1024
TEXT_TARGET = 1024 * 1024
PRUNED = {'history/predecessor', 'build', '__pycache__', 'tools/__pycache__'}
ALLOWED_METADATA = {'PUBLICATION_STATUS.json', 'VALIDATION.md', 'README.md',
                    'HISTORY_PRESERVATION_AUDIT.md', 'RESPONSE_TO_REFEREE.md',
                    'PROOF_DEPENDENCY_LEDGER.md', 'DELIVERY_MANIFEST.json'}


def utc():
    return datetime.now(timezone.utc).isoformat()


def json_bytes(obj, pretty=False):
    return (json.dumps(obj, ensure_ascii=False, indent=2 if pretty else None,
                       sort_keys=pretty, separators=None if pretty else (',', ':')) + '\n').encode()


def load(path):
    return json.loads(path.read_text())


def safe_relative(value):
    path = PurePosixPath(value)
    if path.is_absolute() or '..' in path.parts or not path.parts or any(ch in value for ch in ('\0', '\n', '\r', '\t')):
        raise ValueError(f'Unsafe repository-relative path: {value!r}')
    return path


def tree_sha(entries):
    entries = sorted(entries, key=lambda e: e['path'].encode() + (b'/' if e['type'] == 'tree' else b''))
    raw = b''.join((('40000' if e['type'] == 'tree' else e['mode']).encode() + b' ' + e['path'].encode()
                    + b'\0' + bytes.fromhex(e['sha'])) for e in entries)
    return hashlib.sha1(b'tree ' + str(len(raw)).encode() + b'\0' + raw).hexdigest()


def nested_tree(flat):
    nested = {}
    for entry in flat:
        parts = safe_relative(entry['path']).parts
        node = nested
        for part in parts[:-1]:
            node = node.setdefault(part, {})
        if parts[-1] in node:
            raise ValueError('Duplicate or intersecting tree entry.')
        node[parts[-1]] = (entry['mode'], entry['type'], entry['sha'])
    tree_rows = []
    def visit(node, prefix):
        entries = []
        for name, value in node.items():
            if isinstance(value, dict):
                sha = visit(value, prefix + '/' + name if prefix else name)
                entries.append({'path': name, 'mode': '040000', 'type': 'tree', 'sha': sha})
            else:
                mode, kind, sha = value
                entries.append({'path': name, 'mode': mode, 'type': kind, 'sha': sha})
        sha = tree_sha(entries)
        tree_rows.append({'path': prefix, 'git_tree': sha, 'entries': entries})
        return sha
    return visit(nested, ''), tree_rows


def identify(path, classify=True):
    before = path.lstat()
    symbolic = stat.S_ISLNK(before.st_mode)
    if not symbolic and not stat.S_ISREG(before.st_mode):
        raise ValueError(f'Unsupported filesystem node: {path}')
    target = os.fsencode(os.readlink(path)) if symbolic else None
    size = len(target) if symbolic else before.st_size
    git = hashlib.sha1(b'blob ' + str(size).encode() + b'\0')
    sha = hashlib.sha256()
    decoder = codecs.getincrementaldecoder('utf-8')('strict') if classify else None
    utf8, nul, count = True, False, 0
    stream = path.open('rb') if not symbolic else None
    try:
        chunks = [target] if symbolic else iter(lambda: stream.read(1024 * 1024), b'')
        for chunk in chunks:
            count += len(chunk); git.update(chunk); sha.update(chunk)
            if classify:
                nul = nul or b'\0' in chunk
                if utf8:
                    try:
                        decoder.decode(chunk, final=False)
                    except UnicodeDecodeError:
                        utf8 = False
        if classify and utf8:
            try:
                decoder.decode(b'', final=True)
            except UnicodeDecodeError:
                utf8 = False
    finally:
        if stream:
            stream.close()
    after = path.lstat()
    if (before.st_ino, before.st_size, before.st_mtime_ns, before.st_mode) != (after.st_ino, after.st_size, after.st_mtime_ns, after.st_mode) or count != size:
        raise RuntimeError(f'File changed while being read: {path}')
    return {'bytes': size, 'mode': '120000' if symbolic else ('100755' if before.st_mode & 0o111 else '100644'),
            'git_blob': git.hexdigest(), 'sha256': sha.hexdigest(),
            'encoding_class': 'utf8' if utf8 and not nul else 'binary',
            'mtime_ns': after.st_mtime_ns}


def walk_files(root, prune=None):
    rows = []
    for directory, dirs, files in os.walk(root, followlinks=False):
        rel = Path(directory).relative_to(root)
        dirs[:] = sorted(name for name in dirs if name != '.rsync-tmp' and (rel / name).as_posix() not in (prune or set()))
        for name in list(dirs):
            path = Path(directory) / name
            if path.is_symlink():
                rows.append(path); dirs.remove(name)
        rows.extend(Path(directory) / name for name in sorted(files))
    return sorted(rows)


def ignored_paths(repo, paths):
    command = ['git', 'check-ignore', '--no-index', '-z', '--stdin']
    result = subprocess.run(command, cwd=repo,
                            input=b''.join(path.relative_to(repo).as_posix().encode() + b'\0' for path in paths),
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
    if result.returncode not in (0, 1):
        raise RuntimeError(result.stderr.decode(errors='replace'))
    return {entry.decode() for entry in result.stdout.split(b'\0') if entry}


def identity_errors(expected, actual):
    return [key for key in ('mode', 'bytes', 'git_blob', 'sha256') if expected[key] != actual[key]]


def mutable_document(path):
    return path in ALLOWED_METADATA


def wire_size(body, kind, repository):
    if kind == 'tree':
        args = {'repository_full_name': repository, 'tree_elements': body['tree']}
        if 'base_tree' in body:
            args['base_tree_sha'] = body['base_tree']
        name = 'github.create_tree'
    else:
        args = dict(body, repository_full_name=repository)
        name = 'github.create_blob'
    envelope = {'jsonrpc': '2.0', 'id': 'a2-dyn-evidence-carrier', 'method': 'tools/call',
                'params': {'name': name, 'arguments': args}}
    return len(json_bytes(envelope))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--prepare-only', action='store_true')
    group.add_argument('--final', action='store_true')
    parser.add_argument('--repo', type=Path)
    parser.add_argument('--output', type=Path, required=True, help='New scratch output directory; must not be inside the repository.')
    options = parser.parse_args()
    baseline = load(HERE / 'SOURCE_RELEASE_BASELINE.json')
    repo = (options.repo or Path(baseline['repository_directory'])).resolve()
    article = repo / baseline['article_path']
    output = options.output.resolve()
    if output.is_relative_to(repo) or output == HERE or output.exists() and any(output.iterdir()):
        parser.error('Output must be a new or empty scratch directory outside the repository and helper root.')
    output.mkdir(parents=True, exist_ok=True)
    def save(name, value):
        path = output / name; path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(json_bytes(value, pretty=True))
    started = utc()
    failures = []
    source_rows = baseline['source_outer_files']
    source_by_repo = {row['repo_path']: row for row in source_rows}
    source_by_article = {row['article_path']: row for row in source_rows if row['article_path'] is not None}
    if len(baseline['frozen_math_build_files']) != 130:
        raise RuntimeError('The fixed source baseline does not have the expected 130 inputs.')
    source_root = load(HERE / 'SOURCE_ROOT_TREE.json')
    source_papers = load(HERE / 'SOURCE_PAPERS_TREE.json')
    for value in (source_root, source_papers):
        if value['truncated'] or tree_sha(value['tree']) != value['sha']:
            raise RuntimeError('Invalid or truncated fixed source tree receipt.')
    if source_root['sha'] != baseline['source_root_tree']:
        raise RuntimeError('Source root does not match the published baseline.')
    if next(e['sha'] for e in source_root['tree'] if e['path'] == 'papers') != source_papers['sha']:
        raise RuntimeError('Source papers tree is not bound to source root.')
    if next(e['sha'] for e in source_papers['tree'] if e['path'] == PurePosixPath(baseline['article_path']).name) != baseline['source_article_tree']:
        raise RuntimeError('Published article tree identity mismatch.')
    anchor_bytes = (article / 'CURRENT_SOURCE_ANCHOR.json').read_bytes()
    if hashlib.sha256(anchor_bytes).hexdigest() != baseline['fixed_archive_anchor_sha256']:
        raise RuntimeError('Fixed predecessor anchor changed.')
    anchor = json.loads(anchor_bytes)
    archive_flat = [{'path': row['original_path'], 'mode': row['mode'], 'type': 'blob', 'sha': row['git_blob']} for row in anchor['files']]
    archive_tree, _ = nested_tree(archive_flat)
    if archive_tree != baseline['archive_tree'] or anchor['source_article_tree'] != archive_tree:
        raise RuntimeError('Archive anchor does not reconstruct its immutable Git tree.')
    archive = article / baseline['archive_path']
    archive_paths = walk_files(archive)
    expected_archive = {row['original_path']: row for row in anchor['files']}
    archive_actual = {path.relative_to(archive).as_posix(): path for path in archive_paths}
    if set(archive_actual) != set(expected_archive):
        failures.append({'kind': 'archive_membership', 'missing': sorted(set(expected_archive) - set(archive_actual)),
                         'extra': sorted(set(archive_actual) - set(expected_archive))})
    archive_errors = []
    for path in sorted(set(archive_actual) & set(expected_archive)):
        actual = identify(archive_actual[path], classify=False)
        mismatch = identity_errors(expected_archive[path], actual)
        if mismatch:
            archive_errors.append({'path': path, 'keys': mismatch})
    if archive_errors:
        failures.append({'kind': 'archive_contents', 'files': archive_errors})
    paths = walk_files(article, PRUNED) + [repo / baseline['workflow_path']]
    ignored = ignored_paths(repo, paths)
    current = []
    for path in paths:
        relative = path.relative_to(repo).as_posix()
        if relative in ignored:
            continue
        safe_relative(relative)
        row = identify(path)
        row.update({'repo_path': relative, 'article_path': path.relative_to(article).as_posix() if path.is_relative_to(article) else None})
        current.append(row)
    current.sort(key=lambda r: r['repo_path'])
    current_by_repo = {row['repo_path']: row for row in current}
    current_by_article = {row['article_path']: row for row in current if row['article_path'] is not None}
    frozen_errors = []
    for row in baseline['frozen_math_build_files']:
        actual = current_by_article.get(row['path'])
        if actual is None or identity_errors(row, actual):
            frozen_errors.append(row['path'])
    for path, expected_sha in (('SOURCE_MANIFEST.json', baseline['frozen_source_manifest_sha256']),
                               ('CURRENT_SOURCE_ANCHOR.json', baseline['fixed_archive_anchor_sha256'])):
        if current_by_article.get(path, {}).get('sha256') != expected_sha:
            frozen_errors.append(path)
    if frozen_errors:
        failures.append({'kind': 'frozen_mathematical_or_anchor_input', 'paths': frozen_errors})
    workflow = current_by_repo.get(baseline['workflow_path'])
    if workflow is None or identity_errors(source_by_repo[baseline['workflow_path']], workflow):
        failures.append({'kind': 'root_workflow_changed', 'path': baseline['workflow_path']})
    added = [current_by_repo[path] for path in sorted(set(current_by_repo) - set(source_by_repo))]
    removed = [source_by_repo[path] for path in sorted(set(source_by_repo) - set(current_by_repo))]
    changed = [{'before': source_by_repo[path], 'after': current_by_repo[path]} for path in sorted(set(current_by_repo) & set(source_by_repo))
               if identity_errors(source_by_repo[path], current_by_repo[path])]
    if removed:
        failures.append({'kind': 'published_source_file_removed', 'paths': [r['repo_path'] for r in removed]})
    for row in added:
        path = row['article_path']
        if path is None or not (mutable_document(path) or path.startswith(('audit/', 'evidence/'))):
            failures.append({'kind': 'out_of_carrier_scope_addition', 'path': row['repo_path']})
    for change in changed:
        path = change['after']['article_path']
        if path is None or not mutable_document(path):
            failures.append({'kind': 'published_evidence_or_source_modified', 'path': change['after']['repo_path']})
    preserved_delivery = current_by_article.get('audit/remote-publication/source-release/DELIVERY_MANIFEST.json')
    if preserved_delivery is None or identity_errors(source_by_article['DELIVERY_MANIFEST.json'], preserved_delivery):
        failures.append({'kind': 'source_release_delivery_not_preserved'})
    preservation_errors = []
    for name in sorted(ALLOWED_METADATA):
        retained = current_by_article.get('audit/remote-publication/source-release/' + name)
        if retained is None or identity_errors(source_by_article[name], retained):
            preservation_errors.append(name)
    # Every reachable blob in the already committed article and full predecessor is known.
    known = {}
    for row in [*source_rows, *anchor['files']]:
        existing = known.setdefault(row['git_blob'], {'bytes': row['bytes'], 'sha256': row['sha256']})
        if existing != {'bytes': row['bytes'], 'sha256': row['sha256']}:
            raise RuntimeError('Inconsistent known-blob identity.')
    source_flat = [{'path': row['article_path'], 'mode': row['mode'], 'type': 'blob', 'sha': row['git_blob']} for row in source_rows if row['article_path'] is not None]
    source_flat.append({'path': baseline['archive_path'], 'mode': '040000', 'type': 'tree', 'sha': baseline['archive_tree']})
    if nested_tree(source_flat)[0] != baseline['source_article_tree']:
        raise RuntimeError('Fixed source outer inventory does not reconstruct the published article tree.')
    groups = defaultdict(list)
    for row in current:
        groups[row['git_blob']].append(row)
        if row['git_blob'] in known and known[row['git_blob']] != {'bytes': row['bytes'], 'sha256': row['sha256']}:
            raise RuntimeError('Current blob conflicts with a known committed identity.')
    unique = [{'git_blob': sha, 'bytes': rows[0]['bytes'], 'sha256': rows[0]['sha256'],
               'encoding_class': rows[0]['encoding_class'], 'representative_repo_path': rows[0]['repo_path'],
               'all_repo_paths': [row['repo_path'] for row in rows], 'already_committed': sha in known}
              for sha, rows in sorted(groups.items())]
    manifest_rows = [{key: row[key] for key in ('repo_path', 'article_path', 'mode', 'bytes', 'git_blob', 'sha256')}
                     for row in current if row['article_path'] != 'DELIVERY_MANIFEST.json']
    proposed = {'schema': 'a2-dyn-evidence-carrier-delivery-v1', 'created_utc': utc(),
                'parent_commit': baseline['source_commit'], 'mathematical_source_commit': baseline['source_commit'],
                'new_branch': baseline['branch'], 'source_manifest_sha256': baseline['frozen_source_manifest_sha256'],
                'immutable_predecessor': {'anchor_path': 'CURRENT_SOURCE_ANCHOR.json', 'anchor_sha256': baseline['fixed_archive_anchor_sha256'],
                    'bytes': anchor['bytes'], 'file_count': anchor['file_count'], 'git_tree': baseline['archive_tree'], 'new_path': baseline['archive_path']},
                'scope': 'Evidence-carrier outer article and unchanged dedicated workflow. This manifest excludes itself and ignored runtime files; the complete immutable predecessor is separately anchored. Frozen mathematical/build source is unchanged.',
                'outer_file_count': len(manifest_rows), 'outer_bytes': sum(row['bytes'] for row in manifest_rows), 'files': manifest_rows}
    actual_manifest = load(article / 'DELIVERY_MANIFEST.json')
    declared = {row['repo_path']: row for row in actual_manifest.get('files', [])}
    expected = {row['repo_path']: row for row in manifest_rows}
    manifest_errors = []
    if len(declared) != len(actual_manifest.get('files', [])):
        manifest_errors.append({'kind': 'duplicate_manifest_paths'})
    if set(declared) != set(expected):
        manifest_errors.append({'kind': 'membership', 'missing': sorted(set(expected) - set(declared)), 'unexpected': sorted(set(declared) - set(expected))})
    for path in set(declared) & set(expected):
        if identity_errors(expected[path], declared[path]):
            manifest_errors.append({'kind': 'identity', 'path': path})
    for key in ('outer_file_count', 'outer_bytes', 'parent_commit', 'new_branch', 'source_manifest_sha256', 'immutable_predecessor'):
        if actual_manifest.get(key) != proposed[key]:
            manifest_errors.append({'kind': 'metadata', 'key': key, 'expected': proposed[key], 'actual': actual_manifest.get(key)})
    save('DELIVERY_MANIFEST_PROPOSAL.json', proposed)
    save('FILES.json', current); save('BLOBS.json', unique)
    save('DELTA.json', {'added': added, 'removed': removed, 'changed': changed})
    save('MANIFEST_CHECK.json', {'valid': not manifest_errors, 'errors': manifest_errors,
                                'current_manifest_sha256': current_by_article['DELIVERY_MANIFEST.json']['sha256'],
                                'proposal_is_scratch_only': True,
                                'source_metadata_originals_missing_or_changed': preservation_errors})
    invariants = {'frozen_math_build_inputs_checked': 130, 'frozen_math_build_errors': frozen_errors,
                  'source_manifest_sha256': baseline['frozen_source_manifest_sha256'],
                  'workflow_unchanged': not any(x['kind'] == 'root_workflow_changed' for x in failures),
                  'predecessor_tree': archive_tree, 'predecessor_files_checked': len(archive_actual),
                  'predecessor_bytes_checked': sum(row['bytes'] for row in anchor['files']),
                  'predecessor_content_errors': archive_errors, 'fixed_source_article_tree_reconstructed': True,
                  'all_source_article_and_predecessor_blobs_in_reuse_catalog': True, 'known_committed_unique_blobs': len(known),
                  'allowed_metadata_paths': sorted(ALLOWED_METADATA),
                  'source_metadata_originals_missing_or_changed': preservation_errors,
                  'no_repository_or_index_writes': True, 'no_remote_calls': True, 'failures': failures}
    save('INVARIANTS.json', invariants)
    if failures or options.final and (manifest_errors or preservation_errors):
        save('RESULT.json', {'mode': 'final' if options.final else 'prepare_only', 'ready_for_publication': False,
                             'started_utc': started, 'completed_utc': utc(), 'invariant_failures': failures,
                             'stale_manifest': bool(manifest_errors), 'source_metadata_originals_missing_or_changed': preservation_errors,
                             'payloads_generated': False})
        print(json.dumps({'ready_for_publication': False, 'invariant_failures': len(failures), 'stale_manifest': bool(manifest_errors),
                          'metadata_originals_missing_or_changed': len(preservation_errors), 'output': str(output)}))
        return 2
    payload_directory = 'payloads' if options.final else 'provisional'
    (output / payload_directory).mkdir()
    blocked = []
    def payload(name, body, kind):
        data = json_bytes(body)
        size = wire_size(body, kind, baseline['repository'])
        if size + MARGIN > LIMIT:
            blocked.append({'kind': 'request_too_large', 'name': name, 'rest_body_bytes': len(data),
                            'measured_mcp_envelope_bytes': size, 'required_reserved_bytes': MARGIN, 'limit_bytes': LIMIT})
            return None
        path = output / payload_directory / name
        path.write_bytes(data)
        return {'path': path.relative_to(output).as_posix(), 'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest(),
                'measured_mcp_envelope_bytes': size, 'conservative_request_bytes': size + MARGIN, 'limit_bytes': LIMIT}
    new_blobs = [row for row in unique if not row['already_committed']]
    text_items, binary_payloads = [], []
    for row in new_blobs:
        if row['encoding_class'] == 'binary':
            encoded_size = 4 * ((row['bytes'] + 2) // 3)
            envelope_size = wire_size({'content': '', 'encoding': 'base64'}, 'blob', baseline['repository']) + encoded_size
            if envelope_size + MARGIN > LIMIT:
                blocked.append({'kind': 'binary_requires_authorized_packaging', 'repo_path': row['representative_repo_path'],
                                'bytes': row['bytes'], 'estimated_mcp_envelope_bytes': envelope_size, 'limit_bytes': LIMIT,
                                'action': 'No split was made. Root may authorize raw parts of at most 8 MiB and then regenerate the manifest.'})
                continue
        data = (repo / row['representative_repo_path']).read_bytes()
        if hashlib.sha256(data).hexdigest() != row['sha256']:
            raise RuntimeError('Content changed after inventory; rerun in a new output directory.')
        if row['encoding_class'] == 'binary':
            receipt = payload(f'blob-{len(binary_payloads) + 1:03d}.json', {'content': base64.b64encode(data).decode(), 'encoding': 'base64'}, 'blob')
            if receipt:
                receipt.update({'expected_git_blob': row['git_blob'], 'source_bytes': row['bytes'], 'representative_repo_path': row['representative_repo_path']})
                binary_payloads.append(receipt)
        else:
            entry = {'path': row['git_blob'], 'mode': '100644', 'type': 'blob', 'content': data.decode('utf-8')}
            text_items.append({'entry': entry, 'json_bytes': len(json_bytes(entry)), 'git_blob': row['git_blob']})
    batches = []
    for item in sorted(text_items, key=lambda r: (-r['json_bytes'], r['git_blob'])):
        batch = next((b for b in batches if b['size'] + item['json_bytes'] < TEXT_TARGET), None)
        if batch is None:
            batch = {'size': 12, 'items': []}; batches.append(batch)
        batch['items'].append(item); batch['size'] += item['json_bytes']
    text_payloads = []
    for index, batch in enumerate(batches, 1):
        receipt = payload(f'text-{index:03d}.json', {'tree': [item['entry'] for item in batch['items']]}, 'tree')
        if receipt:
            entries = [{'path': item['git_blob'], 'mode': '100644', 'type': 'blob', 'sha': item['git_blob']} for item in batch['items']]
            receipt.update({'expected_git_tree': tree_sha(entries), 'git_blobs': [item['git_blob'] for item in batch['items']], 'unique_blobs': len(entries)})
            text_payloads.append(receipt)
    flat = [{'path': row['article_path'], 'mode': row['mode'], 'type': 'blob', 'sha': row['git_blob']} for row in current if row['article_path'] is not None]
    flat.append({'path': baseline['archive_path'], 'mode': '040000', 'type': 'tree', 'sha': baseline['archive_tree']})
    article_sha, trees = nested_tree(flat)
    papers_entries = [dict(entry, sha=article_sha) if entry['path'] == PurePosixPath(baseline['article_path']).name else entry for entry in source_papers['tree']]
    papers_sha = tree_sha(papers_entries)
    root_entries = [dict(entry, sha=papers_sha) if entry['path'] == 'papers' else entry for entry in source_root['tree']]
    root_sha = tree_sha(root_entries)
    # Root request has exactly one article subtree update; workflow and all other paths derive from base_tree.
    root_body = {'base_tree': baseline['source_root_tree'], 'tree': [{'path': baseline['article_path'], 'mode': '040000', 'type': 'tree', 'sha': article_sha}]}
    save('ARTICLE_TREES.json', trees)
    article_payload = root_payload = None
    if not blocked:
        article_payload = payload('article-tree.json', {'tree': flat}, 'tree')
        root_payload = payload('root-tree.json', root_body, 'tree')
        if article_payload: article_payload['expected_git_tree'] = article_sha
        if root_payload: root_payload['expected_git_tree'] = root_sha
    end_paths = walk_files(article, PRUNED) + [repo / baseline['workflow_path']]
    end_ignored = ignored_paths(repo, end_paths)
    end_selected = {path.relative_to(repo).as_posix() for path in end_paths if path.relative_to(repo).as_posix() not in end_ignored}
    unstable = [row['repo_path'] for row in current if (repo / row['repo_path']).lstat().st_mtime_ns != row['mtime_ns']]
    if end_selected != set(current_by_repo) or unstable:
        blocked.append({'kind': 'snapshot_changed_during_preparation', 'paths': unstable,
                        'added': sorted(end_selected - set(current_by_repo)), 'removed': sorted(set(current_by_repo) - end_selected)})
    ready = bool(options.final and not blocked and not manifest_errors and not preservation_errors)
    index = {'schema': 'a2-dyn-evidence-carrier-upload-v1', 'mode': 'final' if options.final else 'prepare_only',
             'ready_for_publication': ready, 'source_commit_parent': baseline['source_commit'], 'base_root_tree': baseline['source_root_tree'],
             'article_expected_git_tree': article_sha, 'root_expected_git_tree': root_sha,
             'scope': [baseline['article_path']], 'root_workflow_unchanged': True,
             'text_tree_batches': text_payloads, 'binary_blob_batches': binary_payloads,
             'article_tree': article_payload, 'root_tree': root_payload, 'blocked_payloads': blocked,
             'new_unique_blobs': len(new_blobs), 'new_unique_blob_bytes': sum(row['bytes'] for row in new_blobs),
             'reused_unique_blobs': sum(row['already_committed'] for row in unique),
             'outer_file_count_including_workflow_and_manifest': len(current), 'outer_bytes': sum(row['bytes'] for row in current),
             'manifest_stale': bool(manifest_errors), 'no_remote_or_repository_mutations': True}
    index['source_metadata_originals_missing_or_changed'] = preservation_errors
    save('UPLOAD_INDEX.json', index)
    save('RESULT.json', dict(index, started_utc=started, completed_utc=utc()))
    if ready:
        save('COMMIT_RECIPE.json', {'message': 'Record actual A2-DYN publication and CI evidence [skip ci]', 'tree': root_sha,
                                  'parents': [baseline['source_commit']], 'branch': baseline['branch'],
                                  'expected_old_head_for_ref_update': baseline['source_commit'], 'force': False})
    print(json.dumps({'ready_for_publication': ready, 'mode': index['mode'], 'manifest_stale': bool(manifest_errors),
                      'frozen_inputs_verified': 130, 'archive_files_verified': len(archive_actual), 'new_unique_blobs': len(new_blobs),
                      'new_unique_bytes': index['new_unique_blob_bytes'], 'text_batches': len(text_payloads), 'binary_batches': len(binary_payloads),
                      'blocked_payloads': len(blocked), 'article_tree': article_sha, 'root_tree': root_sha, 'output': str(output)}, indent=2))
    return 2 if options.final and not ready else 0


if __name__ == '__main__':
    try:
        sys.exit(main())
    except Exception as exc:
        print(f'Carrier preparation failed: {exc}', file=sys.stderr)
        sys.exit(2)
