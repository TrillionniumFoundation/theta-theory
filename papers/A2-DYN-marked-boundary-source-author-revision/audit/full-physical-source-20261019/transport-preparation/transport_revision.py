#!/usr/bin/env python3
"""Read-only local Git Data adapter for the full-physical-source author revision.

No network calls, Git commands, remote object creation, or ref mutations occur.
Every actual article file is included, including inherited/current build records;
only .git and __pycache__ components are excluded. An inventory is provisional
unless its caller explicitly requests --final after all writers have stopped.
"""
from pathlib import Path, PurePosixPath
import argparse
import base64
import hashlib
import json
import os
import stat
from datetime import datetime, timezone

WORK = Path('/workspace/scratch/b5cc344d4c8e/iteration-20261019b')
REPO = WORK.parent / 'theta-theory'
ARTICLE_NAME = 'A2-DYN-full-physical-source-author-revision'
ROOT = REPO / 'papers' / ARTICLE_NAME
WORKFLOW_NAME = 'a2-dyn-full-physical-source-20261019.yml'
WORKFLOW = REPO / '.github/workflows' / WORKFLOW_NAME
BASE = WORK / 'source-audit/BASELINE_EXPECTED_FILE_IDENTITIES.json'
BASE_COMMIT = 'fdf2603c8bf422314f199fa431086485a0d1ebb5'
BASE_ARTICLE = 'papers/A2-DYN-physical-tube-source-height-author-revision'
BASE_TREE = 'f5c90ecd279dd116330c5d90fa31cae2b0d6f61e'
BASE_FILE_SHA256 = '2dbbbad489541592bd034b08bffeefb8491c68a9c8be8909349415f9c53c2de2'
CONTROL_TREES = {
    'root': 'd90e88848644a25b2d9f2e3a28383f4908d2a646',
    'papers': '7313099b5b12c91d3c3352ec62cdc50ba2f72232',
    'github': 'c1cae8fe6a323d93ff90ec92cdff712a8651586e',
    'workflows': '11e3e251551d1029dbf74d280546c1ca38b808fe',
}
EXCLUDED_COMPONENTS = frozenset(('.git', '__pycache__'))


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


def utc_now():
    return datetime.now(timezone.utc).isoformat()


def git_blob(data):
    return hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()


def normalize_mode(mode):
    value = str(mode).lstrip('0')
    require(value in ('40000', '100644', '100755', '120000', '160000'),
            'Unsupported Git mode: ' + str(mode))
    return value


def path_parts(value):
    require(isinstance(value, str) and value and '\0' not in value,
            'Invalid empty or NUL-containing Git path')
    path = PurePosixPath(value)
    require(not path.is_absolute() and str(path) == value and
            all(part not in ('.', '..') for part in path.parts),
            'Path must be normalized and article-relative: ' + value)
    return path.parts


def flat_tree_digest(entries):
    """Canonical Git tree hash; input entries are immediate children only."""
    encoded = []
    names = set()
    for row in entries:
        name = row['path']
        require(len(path_parts(name)) == 1 and name not in names,
                'Duplicate or non-immediate tree entry: ' + name)
        names.add(name)
        mode = normalize_mode(row['mode'])
        sha = row['sha']
        require(len(sha) == 40 and all(x in '0123456789abcdef' for x in sha),
                'Malformed object SHA at ' + name)
        raw_name = name.encode('utf-8')
        key = raw_name + (b'/' if mode == '40000' else b'')
        payload = mode.encode() + b' ' + raw_name + b'\0' + bytes.fromhex(sha)
        encoded.append((key, payload))
    data = b''.join(payload for _, payload in sorted(encoded))
    return hashlib.sha1(b'tree ' + str(len(data)).encode() + b'\0' + data).hexdigest()


def tree_digest(rows):
    """Canonical article tree and every subtree from path-level identities."""
    tree = {}
    for row in rows:
        parts = path_parts(row['path'])
        node = tree
        for part in parts[:-1]:
            if part not in node:
                node[part] = {}
            require(isinstance(node[part], dict), 'File/directory path collision')
            node = node[part]
        require(parts[-1] not in node, 'Duplicate or conflicting path: ' + row['path'])
        node[parts[-1]] = (normalize_mode(row['mode']), row['sha'])
    hashes = {}

    def emit(node, prefix=''):
        entries = []
        for name, value in node.items():
            if isinstance(value, dict):
                mode, sha = '40000', emit(value, prefix + name + '/')
            else:
                mode, sha = value
            entries.append({'path': name, 'mode': mode, 'sha': sha})
        sha = flat_tree_digest(entries)
        hashes[prefix.rstrip('/')] = sha
        return sha

    return emit(tree), hashes


def load_baseline():
    data = BASE.read_bytes()
    require(hashlib.sha256(data).hexdigest() == BASE_FILE_SHA256,
            'Pinned baseline identity receipt changed')
    obj = json.loads(data)
    require(isinstance(obj, dict) and isinstance(obj.get('files'), list),
            'Expected the current baseline dict.files schema')
    require(len(obj['files']) == 2088, 'Incomplete 2,088-file baseline receipt')
    sha, subtrees = tree_digest(obj['files'])
    require(sha == obj['article_tree_sha'] == BASE_TREE,
            'Baseline canonical article identity mismatch')
    require(subtrees == obj['subtree_hashes'], 'Baseline subtree identities mismatch')
    return obj


def included_paths():
    """Do not follow directory symlinks; a symlink is its literal Git blob."""
    require(ROOT.is_dir() and not ROOT.is_symlink(), 'Missing or symlink article root')
    paths = []
    for folder, dirs, files in os.walk(ROOT, followlinks=False):
        dirs[:] = sorted(name for name in dirs if name not in EXCLUDED_COMPONENTS)
        retained_dirs = []
        for name in dirs:
            path = Path(folder) / name
            if path.is_symlink():
                paths.append(path)
            else:
                retained_dirs.append(name)
        dirs[:] = retained_dirs
        paths.extend(Path(folder) / name for name in sorted(files)
                     if name not in EXCLUDED_COMPONENTS)
    return sorted(paths, key=lambda p: p.relative_to(ROOT).as_posix())


def stable_payload(path):
    before = path.lstat()
    if stat.S_ISLNK(before.st_mode):
        data, mode = os.fsencode(os.readlink(path)), '120000'
    else:
        require(stat.S_ISREG(before.st_mode), 'Unsupported special file: ' + str(path))
        data = path.read_bytes()
        mode = '100755' if before.st_mode & 0o111 else '100644'
    after = path.lstat()
    signature = lambda s: (s.st_dev, s.st_ino, s.st_mode, s.st_size,
                           s.st_mtime_ns, s.st_ctime_ns)
    require(signature(before) == signature(after), 'File changed while reading: ' + str(path))
    return data, mode, signature(after)


def identity(path, relative):
    data, mode, signature = stable_payload(path)
    try:
        data.decode('utf-8')
        encoding = 'utf-8'
    except UnicodeDecodeError:
        encoding = 'base64'
    return {'path': relative, 'mode': mode, 'type': 'blob', 'bytes': len(data),
            'sha': git_blob(data), 'sha256': hashlib.sha256(data).hexdigest(),
            'encoding': encoding}, signature


def scan():
    baseline = {row['path']: row for row in load_baseline()['files']}
    known = {row['sha'] for row in baseline.values()}
    rows, signatures = [], {}
    paths = included_paths()
    for path in paths:
        relative = path.relative_to(ROOT).as_posix()
        row, signature = identity(path, relative)
        old = baseline.get(relative)
        row['known_baseline_blob'] = row['sha'] in known
        row['changed_from_base_path'] = old is None or any(
            row[key] != old[key] for key in ('sha', 'mode', 'bytes'))
        rows.append(row)
        signatures[path] = signature
    require(paths == included_paths(), 'Article path set changed during inventory')
    for path, before in signatures.items():
        after = path.lstat()
        signature = (after.st_dev, after.st_ino, after.st_mode, after.st_size,
                     after.st_mtime_ns, after.st_ctime_ns)
        require(signature == before, 'Article file changed during inventory: ' + str(path))
    return rows


def inventory(final=False):
    started = utc_now()
    rows = scan()
    sha, subtrees = tree_digest(rows)
    baseline = load_baseline()
    old_paths = {row['path'] for row in baseline['files']}
    current_paths = {row['path'] for row in rows}
    changed = [row['path'] for row in rows if row['changed_from_base_path']]
    known = [row for row in rows if row['known_baseline_blob']]
    return {
        'created_utc': utc_now(), 'scan_started_utc': started,
        'snapshot_status': 'final_local_candidate' if final else 'provisional_not_frozen',
        'remote_mutations_performed': False,
        'base_commit': BASE_COMMIT, 'base_root_tree': CONTROL_TREES['root'],
        'base_article_path': BASE_ARTICLE, 'base_article_tree': BASE_TREE,
        'base_file_identities_sha256': BASE_FILE_SHA256,
        'article_path': ROOT.relative_to(REPO).as_posix(),
        'scope': ('Actual local file bytes and Git modes, including inherited/current '
                  'build evidence; only .git and __pycache__ are excluded. '
                  'This records source transport identity, not mathematical certification '
                  'or completed remote publication. A final candidate still requires '
                  'later remote hash/ref verification.'),
        'article_tree_sha': sha, 'file_count': len(rows),
        'bytes': sum(row['bytes'] for row in rows),
        'changed_paths': len(changed), 'changed_path_list': changed,
        'removed_baseline_paths': sorted(old_paths - current_paths),
        'known_baseline_blob_paths': len(known),
        'known_baseline_blob_unique': len({row['sha'] for row in known}),
        'new_blob_unique': len({row['sha'] for row in rows if not row['known_baseline_blob']}),
        'files': rows, 'subtree_hashes': subtrees,
    }


def read_control_trees():
    result = {}
    for kind, expected in CONTROL_TREES.items():
        receipt = WORK / ('source-audit/readbacks/fixed/baseline_' + kind + '.json')
        obj = json.loads(receipt.read_bytes())['response']
        require(obj.get('truncated') is False, 'Truncated baseline control tree: ' + kind)
        require(obj['sha'] == expected == flat_tree_digest(obj['tree']),
                'Canonical baseline control tree mismatch: ' + kind)
        result[kind] = obj
    commit = json.loads((WORK / 'source-audit/readbacks/fixed/baseline_commit.json').read_bytes())['response']
    require(commit['sha'] == BASE_COMMIT and commit['tree']['sha'] == CONTROL_TREES['root'],
            'Baseline commit/root linkage mismatch')
    prior = json.loads((WORK.parent / 'iteration-20261019/C3_ROOT_EXPECTED.json').read_bytes())
    published = json.loads((WORK.parent / 'iteration-20261019/C3_TRANSPORT_EXECUTION_RECEIPTS.json').read_bytes())
    require(prior['root_tree'] == published['root'] == CONTROL_TREES['root'] and
            prior['article_tree'] == published['article'] == BASE_TREE and
            published['final_commit'] == BASE_COMMIT,
            'Prior actual C3 receipt disagrees with fresh baseline identities')
    for kind in ('papers', 'github', 'workflows'):
        require(prior[kind + '_tree'] == CONTROL_TREES[kind], 'Prior C3 subtree mismatch')
    return result


def repository_scope(current):
    """Prepare exactly one new article plus one new dedicated workflow."""
    base = read_control_trees()
    before = {kind: {row['path']: dict(row) for row in obj['tree']}
              for kind, obj in base.items()}
    require(before['root']['papers']['sha'] == CONTROL_TREES['papers'] and
            before['root']['.github']['sha'] == CONTROL_TREES['github'] and
            before['github']['workflows']['sha'] == CONTROL_TREES['workflows'] and
            before['papers'][Path(BASE_ARTICLE).name]['sha'] == BASE_TREE,
            'Baseline control tree linkage mismatch')
    require(ARTICLE_NAME not in before['papers'], 'New article name already exists in baseline')
    require(WORKFLOW_NAME not in before['workflows'], 'New workflow name already exists in baseline')
    workflow, _ = identity(WORKFLOW, WORKFLOW.relative_to(REPO).as_posix())
    copy, _ = identity(ROOT / 'ci' / WORKFLOW_NAME, 'ci/' + WORKFLOW_NAME)
    require(all(workflow[key] == copy[key] for key in ('sha', 'sha256', 'mode', 'bytes')),
            'Dedicated repository workflow and article copy differ')
    after = {kind: {path: dict(row) for path, row in rows.items()}
             for kind, rows in before.items()}
    after['papers'][ARTICLE_NAME] = {'path': ARTICLE_NAME, 'mode': '040000',
                                    'type': 'tree', 'sha': current['article_tree_sha']}
    after['workflows'][WORKFLOW_NAME] = {'path': WORKFLOW_NAME, 'mode': workflow['mode'],
                                       'type': 'blob', 'sha': workflow['sha']}
    new_hashes = {}
    for kind in ('papers', 'workflows'):
        new_hashes[kind] = flat_tree_digest(after[kind].values())
    after['github']['workflows']['sha'] = new_hashes['workflows']
    new_hashes['github'] = flat_tree_digest(after['github'].values())
    after['root']['papers']['sha'] = new_hashes['papers']
    after['root']['.github']['sha'] = new_hashes['github']
    new_hashes['root'] = flat_tree_digest(after['root'].values())
    changes = {}
    for kind in before:
        changes[kind] = sorted(path for path in set(before[kind]) | set(after[kind])
                               if before[kind].get(path) != after[kind].get(path))
    require(changes == {'root': ['.github', 'papers'], 'papers': [ARTICLE_NAME],
                       'github': ['workflows'], 'workflows': [WORKFLOW_NAME]},
            'Unexpected repository publication scope')
    return {'created_utc': utc_now(), 'snapshot_status': current['snapshot_status'],
            'remote_mutations_performed': False, 'base_commit': BASE_COMMIT,
            'base_tree_identities': CONTROL_TREES, 'expected_tree_identities': new_hashes,
            'expected_article_tree': current['article_tree_sha'], 'workflow': workflow,
            'old_counts': {kind: len(rows) for kind, rows in before.items()},
            'new_counts': {kind: len(rows) for kind, rows in after.items()},
            'changes': changes, 'all_other_entries_preserved': True,
            'scope': ('Local canonical construction using fresh pinned GitHub tree receipts. '
                      'All 212 prior article entries and 174 prior workflows are reused '
                      'exactly; no repository or remote mutation is performed.'),
            'base_trees': base, 'expected_trees': {
                kind: {'sha': new_hashes[kind], 'tree': list(rows.values())}
                for kind, rows in after.items()}}


def chunk(relative, offset, length, expected_sha=None):
    parts = path_parts(relative)
    require(not any(part in EXCLUDED_COMPONENTS for part in parts), 'Excluded path requested')
    require(offset >= 0 and length >= 1, 'Invalid publication byte-read range')
    target = ROOT.joinpath(*parts)
    for ancestor in target.parents:
        if ancestor == ROOT:
            break
        require(not ancestor.is_symlink(), 'Chunk path traverses a symlink')
    data, _, _ = stable_payload(target)
    if expected_sha is not None:
        require(git_blob(data) == expected_sha, 'Chunk bytes differ from expected Git blob')
    return base64.b64encode(data[offset:offset + length]).decode('ascii')


def brief(value):
    return {key: item for key, item in value.items()
            if key not in ('files', 'subtree_hashes', 'changed_path_list',
                           'base_trees', 'expected_trees')}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=('inventory', 'changes', 'chunk', 'stats', 'baseline', 'scope'))
    parser.add_argument('--path')
    parser.add_argument('--offset', type=int, default=0)
    parser.add_argument('--length', type=int, default=98304)
    parser.add_argument('--expected-sha')
    parser.add_argument('--output', type=Path)
    parser.add_argument('--final', action='store_true',
                        help='Caller explicitly declares a stopped-writer final local candidate')
    args = parser.parse_args()
    if args.action == 'chunk':
        require(args.path is not None, '--path is required for chunk')
        print(chunk(args.path, args.offset, args.length, args.expected_sha))
        return
    if args.action == 'baseline':
        value = load_baseline()
        value = {'base_commit': BASE_COMMIT, 'article_tree_sha': value['article_tree_sha'],
                 'file_count': len(value['files']), 'subtree_count': len(value['subtree_hashes']),
                 'identity_receipt_sha256': BASE_FILE_SHA256, 'status': 'passed'}
    else:
        value = inventory(final=args.final)
        if args.action == 'changes':
            value = [row for row in value['files'] if row['changed_from_base_path']]
        elif args.action == 'stats':
            value = brief(value)
        elif args.action == 'scope':
            value = repository_scope(value)
    if args.output:
        target = args.output.resolve()
        require(target.is_relative_to(WORK) and not target.is_relative_to(ROOT),
                'Write receipts only beneath the iteration work directory')
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(json.dumps(value, indent=2) + '\n')
        print(json.dumps(brief(value) if isinstance(value, dict) else {'rows': len(value)}))
    else:
        print(json.dumps(value))


if __name__ == '__main__':
    main()
