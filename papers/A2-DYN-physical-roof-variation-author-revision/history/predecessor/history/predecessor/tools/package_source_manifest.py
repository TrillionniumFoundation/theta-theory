#!/usr/bin/env python3
"""Verify immutable inherited source bytes and freeze the current source package.

Reconstructed after workspace pruning, with the previous helper's public API:
    python3 tools/package_source_manifest.py . history
    python3 tools/package_source_manifest.py . freeze
    python3 tools/package_source_manifest.py . verify
    import package_source_manifest; package_source_manifest.verify_manifest(ROOT)

No assert-based gate is used. This verifies source identity, not mathematical truth.
The first literal anchor comes from the surviving pre-pruning transport inventory.
The second anchor binds the verified 15ad3962 native source. A third anchor
binds every one of the 2,088 actual fdf2603 predecessor files. A fourth
binds all 2,765 actual 0933e9b predecessor files. None can be
reset when freezing a new current-source manifest.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path, PurePosixPath

ANCHOR_PATH = 'history/IMMUTABLE_SOURCE_ANCHOR.json'
ANCHOR_SHA256 = 'bc93f16657c09a87a469ab8275cdf966082fa64131f517dbb308c6f70db17177'
EXPECTED_GROUPS = {
    'predecessor_snapshot': (103, 1557258),
    'numbered_variants': (355, 3392932),
    'historical_build_sources': (390, 3221429),
    'historical_manuscript_variants': (66, 902709),
    'reports': (90, 3058273),
    'active_inherited_core': (44, 442771),
}
GLOBAL_MINIMIZER_ANCHOR_PATH = 'history/GLOBAL_MINIMIZER_NATIVE_SOURCE_ANCHOR.json'
GLOBAL_MINIMIZER_ANCHOR_SHA256 = 'ce75ebb333627f86e6ec8d731a5f348d2061dfb950ec3ee03542c7c937cc43b1'
EXPECTED_GLOBAL_MINIMIZER_GROUPS = {
    'active_inherited_core_260_309': (50, 508842),
    'active_inherited_model_and_inputs': (8, 35004),
    'predecessor_author_documents_and_helpers': (16, 1015586),
}
PHYSICAL_TUBE_ANCHOR_PATH = 'history/PHYSICAL_TUBE_SOURCE_ANCHOR.json'
PHYSICAL_TUBE_ANCHOR_SHA256 = '0e0570ca2a01aa274dd6e93e048a3a9db90539562d56d10c68405ee0ad6e3eff'
FULL_PHYSICAL_ANCHOR_PATH = 'history/FULL_PHYSICAL_SOURCE_ANCHOR.json'
FULL_PHYSICAL_ANCHOR_SHA256 = '93ebe2519b142e2f60a9a5d23dd128ef2a7071001b8c1e24e18d31859ec35912'
MANIFEST_NAME = 'SOURCE_MANIFEST.json'
EXCLUDED_ROOT_FILES = {
    MANIFEST_NAME, 'SOURCE_MANIFEST.sha256', 'PROOF_INDEX.json', 'PUBLICATION_STATUS.json',
    'REMOTE_TRANSPORT_STATUS.md', 'PUBLICATION_RECEIPT.json',
}
EXCLUDED_PREFIXES = ('evidence/current-execution/', 'delivery/')
EXCLUDED_COMPONENTS = {'build', '.git', '__pycache__', '.pytest_cache', '.rsync-tmp'}
INPUT_RE = re.compile(r'\\(?:input|include)\s*\{([^}]+)\}')


class VerificationError(RuntimeError):
    """An explicit verification failure, including under optimized Python."""


def checked_path(root: Path, relative: str) -> Path:
    q = PurePosixPath(relative)
    if not relative or q.is_absolute() or '..' in q.parts or str(q) != relative:
        raise VerificationError(f'Unsafe or noncanonical source path: {relative!r}')
    p = root / relative
    current = root
    for part in q.parts:
        current = current / part
        if current.is_symlink():
            raise VerificationError(f'Symlink in source path: {relative}')
    return p


def identity(data: bytes) -> dict:
    return {
        'bytes': len(data),
        'sha256': hashlib.sha256(data).hexdigest(),
        'git_blob': hashlib.sha1(b'blob ' + str(len(data)).encode('ascii') + b'\0' + data).hexdigest(),
    }


def check_row(root: Path, row: dict) -> None:
    if set(('path', 'bytes', 'sha256', 'git_blob')) - row.keys():
        raise VerificationError('Incomplete source identity row')
    path = checked_path(root, row['path'])
    if not path.is_file():
        raise VerificationError(f'Missing immutable/source file: {row["path"]}')
    actual = identity(path.read_bytes())
    for key, value in actual.items():
        if row[key] != value:
            raise VerificationError(f'{key} mismatch: {row["path"]}: expected {row[key]}, got {value}')


def load_anchor(root: Path) -> dict:
    p = checked_path(root, ANCHOR_PATH)
    if not p.is_file():
        raise VerificationError(f'Missing immutable source anchor: {ANCHOR_PATH}')
    raw = p.read_bytes()
    if hashlib.sha256(raw).hexdigest() != ANCHOR_SHA256:
        raise VerificationError('Immutable source anchor hash mismatch')
    data = json.loads(raw)
    if set(data['groups']) != set(EXPECTED_GROUPS):
        raise VerificationError('Immutable source group set changed')
    return data


def verify_history(root: Path | str) -> dict:
    root = Path(root).resolve()
    anchor = load_anchor(root)
    checks = {}
    for name, (expected_count, expected_bytes) in EXPECTED_GROUPS.items():
        group = anchor['groups'][name]
        rows = group['files']
        paths = [x['path'] for x in rows]
        if len(rows) != expected_count or len(set(paths)) != expected_count:
            raise VerificationError(f'Wrong immutable source count or duplicate path: {name}')
        if sum(x['bytes'] for x in rows) != expected_bytes:
            raise VerificationError(f'Wrong immutable source byte total: {name}')
        if group['count'] != expected_count or group['bytes'] != expected_bytes:
            raise VerificationError(f'Wrong immutable source group metadata: {name}')
        for row in rows:
            check_row(root, row)
        checks[name] = {'files': expected_count, 'bytes': expected_bytes, 'verified': True}
    # Canonical numbering is checked independently of aliases of other variants.
    historical = anchor['groups']['historical_build_sources']['files']
    old_numbers = {int(m.group(1)) for row in historical for m in [re.match(r'history/historical-v108/core/(\d+)_', row['path'])] if m}
    current_numbers = {int(m.group(1)) for row in anchor['groups']['active_inherited_core']['files'] for m in [re.match(r'core/(\d+)_', row['path'])] if m}
    if old_numbers != set(range(1, 260)) or current_numbers != set(range(260, 304)):
        raise VerificationError('Canonical inherited native numbering 1-303 is incomplete')
    preceding = verify_global_minimizer_history(root)
    complete = verify_physical_tube_history(root)
    return {'scope': 'Immutable inherited source identities, not a proof certificate', 'anchor_sha256': ANCHOR_SHA256, 'groups': checks, 'preceding_author_native': preceding, 'complete_physical_tube_predecessor': complete, 'complete_full_physical_predecessor': verify_full_physical_history(root)}


def verify_global_minimizer_history(root: Path | str) -> dict:
    """Verify the separate 15ad3962 anchor without altering the 1-303 anchor."""
    root = Path(root).resolve()
    p = checked_path(root, GLOBAL_MINIMIZER_ANCHOR_PATH)
    if not p.is_file():
        raise VerificationError(f'Missing preceding-author source anchor: {GLOBAL_MINIMIZER_ANCHOR_PATH}')
    raw = p.read_bytes()
    if hashlib.sha256(raw).hexdigest() != GLOBAL_MINIMIZER_ANCHOR_SHA256:
        raise VerificationError('Preceding-author native source anchor hash mismatch')
    anchor = json.loads(raw)
    if anchor.get('source_commit') != '15ad3962de63f50911b765fe6608e722fe9b8c82':
        raise VerificationError('Preceding-author native source commit changed')
    if anchor.get('source_article_tree') != '39f02eb2dab466bb742c7f96139a6535d7bb10ef':
        raise VerificationError('Preceding-author native article tree changed')
    if set(anchor.get('groups', {})) != set(EXPECTED_GLOBAL_MINIMIZER_GROUPS):
        raise VerificationError('Preceding-author immutable source group set changed')
    checks = {}
    all_paths = set()
    for name, (expected_count, expected_bytes) in EXPECTED_GLOBAL_MINIMIZER_GROUPS.items():
        group = anchor['groups'][name]
        rows = group['files']
        paths = [row['path'] for row in rows]
        if len(rows) != expected_count or len(set(paths)) != expected_count:
            raise VerificationError(f'Wrong preceding-author source count or duplicate path: {name}')
        if all_paths.intersection(paths):
            raise VerificationError('Repeated path across preceding-author immutable groups')
        all_paths.update(paths)
        if sum(row['bytes'] for row in rows) != expected_bytes or group['count'] != expected_count or group['bytes'] != expected_bytes:
            raise VerificationError(f'Wrong preceding-author immutable group size: {name}')
        for row in rows:
            check_row(root, row)
        checks[name] = {'files': expected_count, 'bytes': expected_bytes, 'verified': True}
    core_rows = anchor['groups']['active_inherited_core_260_309']['files']
    numbers = {int(match.group(1)) for row in core_rows for match in [re.match(r'core/(\d+)_', row['path'])] if match}
    if numbers != set(range(260, 310)):
        raise VerificationError('Preceding-author native core numbering 260-309 is incomplete')
    return {'scope': 'Exact preceding author source, not an independent continuum proof certificate',
            'source_commit': anchor['source_commit'], 'source_article_tree': anchor['source_article_tree'],
            'anchor_sha256': GLOBAL_MINIMIZER_ANCHOR_SHA256, 'groups': checks}


def verify_physical_tube_history(root: Path | str) -> dict:
    """Verify every actual file in the complete fdf2603 predecessor article."""
    root = Path(root).resolve()
    raw = checked_path(root, PHYSICAL_TUBE_ANCHOR_PATH).read_bytes()
    if hashlib.sha256(raw).hexdigest() != PHYSICAL_TUBE_ANCHOR_SHA256:
        raise VerificationError('Complete physical-tube predecessor anchor changed')
    anchor = json.loads(raw)
    if anchor.get('source_commit') != 'fdf2603c8bf422314f199fa431086485a0d1ebb5' or anchor.get('source_article_tree') != 'f5c90ecd279dd116330c5d90fa31cae2b0d6f61e':
        raise VerificationError('Complete physical-tube predecessor identity changed')
    rows = anchor.get('files', [])
    if len(rows) != 2088 or anchor.get('file_count') != 2088 or anchor.get('bytes') != 215569322 or sum(row['bytes'] for row in rows) != 215569322:
        raise VerificationError('Complete physical-tube predecessor size changed')
    if len({row['original_path'] for row in rows}) != 2088 or len({row['path'] for row in rows}) != 2088:
        raise VerificationError('Duplicate complete-predecessor source or placement')
    tree = {}
    core_numbers = set()
    for row in rows:
        check_row(root, row)
        checked_path(root, row['original_path'])
        if row['original_mode'] not in {'100644', '100755'}:
            raise VerificationError('Unsupported original predecessor mode')
        match = re.match(r'core/(\d+)_', row['original_path'])
        if match:
            core_numbers.add(int(match.group(1)))
            if row['path'] != row['original_path']:
                raise VerificationError('Inherited complete active proof moved out of native core')
        parts = row['original_path'].split('/')
        node = tree
        for part in parts[:-1]:
            node = node.setdefault(part, {})
        node[parts[-1]] = (row['original_mode'], row['git_blob'])
    if core_numbers != set(range(260, 314)):
        raise VerificationError('Complete inherited native range 260-313 changed')
    def digest(node):
        entries = []
        for name, value in node.items():
            if isinstance(value, dict):
                mode, sha, key = '40000', digest(value), name + '/'
            else:
                mode, sha = value
                key = name
            entries.append((key.encode(), mode.encode() + b' ' + name.encode() + b'\0' + bytes.fromhex(sha)))
        data = b''.join(value for key, value in sorted(entries, key=lambda item: item[0]))
        return hashlib.sha1(b'tree ' + str(len(data)).encode() + b'\0' + data).hexdigest()
    original_tree = digest(tree)
    if original_tree != anchor['source_article_tree']:
        raise VerificationError('Complete original Git article tree does not reconstruct')
    return {'source_commit': anchor['source_commit'], 'source_article_tree': original_tree,
            'anchor_sha256': PHYSICAL_TUBE_ANCHOR_SHA256, 'files': 2088, 'bytes': 215569322,
            'active_complete_core_bodies_unchanged': 54,
            'preserved_copy_placements': sum(row['path'] != row['original_path'] for row in rows),
            'verified': True}


def verify_full_physical_history(root: Path | str) -> dict:
    """Verify every actual file in the complete 0933e9b predecessor article."""
    root = Path(root).resolve()
    raw = checked_path(root, FULL_PHYSICAL_ANCHOR_PATH).read_bytes()
    if hashlib.sha256(raw).hexdigest() != FULL_PHYSICAL_ANCHOR_SHA256:
        raise VerificationError('Complete full-physical-source predecessor anchor changed')
    anchor = json.loads(raw)
    if anchor.get('source_commit') != '0933e9b44f5b0fd1d1a624d37ffd881d352496f8' or anchor.get('source_article_tree') != 'ff4daf7f42d868bd9b41b0b9fe4033489f99bd21':
        raise VerificationError('Complete full-physical-source predecessor identity changed')
    rows = anchor.get('files', [])
    if len(rows) != 2765 or anchor.get('file_count') != 2765 or anchor.get('bytes') != 318080854 or sum(row['bytes'] for row in rows) != 318080854:
        raise VerificationError('Complete full-physical-source predecessor size changed')
    if len({row['original_path'] for row in rows}) != 2765 or len({row['path'] for row in rows}) != 2765:
        raise VerificationError('Duplicate complete-predecessor source or placement')
    tree = {}
    core_numbers = set()
    for row in rows:
        check_row(root, row)
        checked_path(root, row['original_path'])
        if row['original_mode'] not in {'100644', '100755'}:
            raise VerificationError('Unsupported original predecessor mode')
        match = re.match(r'core/(\d+)_', row['original_path'])
        if match:
            core_numbers.add(int(match.group(1)))
            if row['path'] != row['original_path']:
                raise VerificationError('Inherited complete active proof moved out of native core')
        parts = row['original_path'].split('/')
        node = tree
        for part in parts[:-1]:
            node = node.setdefault(part, {})
        node[parts[-1]] = (row['original_mode'], row['git_blob'])
    if core_numbers != set(range(260, 316)):
        raise VerificationError('Complete inherited native range 260-315 changed')
    def digest(node):
        entries = []
        for name, value in node.items():
            if isinstance(value, dict):
                mode, sha, key = '40000', digest(value), name + '/'
            else:
                mode, sha = value
                key = name
            entries.append((key.encode(), mode.encode() + b' ' + name.encode() + b'\0' + bytes.fromhex(sha)))
        data = b''.join(value for key, value in sorted(entries, key=lambda item: item[0]))
        return hashlib.sha1(b'tree ' + str(len(data)).encode() + b'\0' + data).hexdigest()
    original_tree = digest(tree)
    if original_tree != anchor['source_article_tree']:
        raise VerificationError('Complete original Git article tree does not reconstruct')
    return {'source_commit': anchor['source_commit'], 'source_article_tree': original_tree,
            'anchor_sha256': FULL_PHYSICAL_ANCHOR_SHA256, 'files': 2765, 'bytes': 318080854,
            'active_complete_core_bodies_unchanged': 56,
            'preserved_copy_placements': sum(row['path'] != row['original_path'] for row in rows),
            'verified': True}


def excluded(relative: str) -> bool:
    p = PurePosixPath(relative)
    if relative in EXCLUDED_ROOT_FILES:
        return True
    if any(part in EXCLUDED_COMPONENTS for part in p.parts):
        return True
    if any(relative.startswith(prefix) for prefix in EXCLUDED_PREFIXES):
        return True
    if p.suffix in {'.pyc', '.pyo'}:
        return True
    return False


def source_files(root: Path) -> list[Path]:
    found = []
    for p in root.rglob('*'):
        rel = p.relative_to(root).as_posix()
        if excluded(rel):
            continue
        if p.is_symlink():
            raise VerificationError(f'Symlink in current source tree: {rel}')
        if p.is_file():
            checked_path(root, rel)
            found.append(p)
    return sorted(found, key=lambda p: p.relative_to(root).as_posix())


def tex_closure(root: Path) -> dict:
    """Follow literal active-main input/include dependencies, with no guessed bodies."""
    queue = ['main.tex']
    visited = set()
    while queue:
        rel = queue.pop()
        if rel in visited:
            continue
        path = checked_path(root, rel)
        if not path.is_file():
            raise VerificationError(f'Missing active native TeX input: {rel}')
        visited.add(rel)
        text = re.sub(r'(?<!\\)%[^\n]*', '', path.read_text(encoding='utf-8'))
        for name in INPUT_RE.findall(text):
            if '\\' in name or '#' in name:
                raise VerificationError(f'Unresolved dynamic TeX input in {rel}: {name}')
            name = name if Path(name).suffix else name + '.tex'
            checked_path(root, name)
            queue.append(name)
    cores = sorted(p.relative_to(root).as_posix() for p in (root / 'core').glob('*.tex'))
    numbers = []
    for rel in cores:
        m = re.match(r'core/(\d+)_', rel)
        if not m:
            raise VerificationError(f'Unexpected active core filename: {rel}')
        numbers.append(int(m.group(1)))
        if rel not in visited:
            raise VerificationError(f'Active mathematical source is not included by main.tex: {rel}')
    if not numbers or len(set(numbers)) != len(numbers) or set(numbers) != set(range(260, max(numbers) + 1)):
        raise VerificationError('Active mathematical source sequence is not contiguous from 260')
    return {'reachable_tex_files': sorted(visited), 'active_core_files': cores, 'active_core_start': 260, 'active_core_end': max(numbers)}


def freeze_manifest(root: Path | str) -> dict:
    root = Path(root).resolve()
    history = verify_history(root)
    closure = tex_closure(root)
    rows = []
    for p in source_files(root):
        rows.append(dict(path=p.relative_to(root).as_posix(), **identity(p.read_bytes())))
    manifest = {
        'schema': 5,
        'scope': 'Current complete source and retained evidence manifest; regenerable builds, current execution outputs, derived delivery artifacts, manifest self and post-publication receipts excluded.',
        'helper_status': 'All four literal immutable anchors are verified before every freeze; every actual complete predecessor file and its original canonical Git article tree are checked. Prior helpers remain preserved.',
        'immutable_source_anchor_sha256': ANCHOR_SHA256,
        'preceding_author_native_anchor_sha256': GLOBAL_MINIMIZER_ANCHOR_SHA256,
        'complete_physical_tube_anchor_sha256': PHYSICAL_TUBE_ANCHOR_SHA256,
        'complete_full_physical_anchor_sha256': FULL_PHYSICAL_ANCHOR_SHA256,
        'source_count': len(rows),
        'source_bytes': sum(x['bytes'] for x in rows),
        'excluded_root_files': sorted(EXCLUDED_ROOT_FILES),
        'excluded_prefixes': list(EXCLUDED_PREFIXES),
        'excluded_components': sorted(EXCLUDED_COMPONENTS),
        'history_verification': history,
        'native_tex_closure': closure,
        'files': rows,
    }
    (root / MANIFEST_NAME).write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
    return manifest


def verify_manifest(root: Path | str) -> dict:
    root = Path(root).resolve()
    history = verify_history(root)
    closure = tex_closure(root)
    mp = root / MANIFEST_NAME
    if not mp.is_file():
        raise VerificationError(f'Missing {MANIFEST_NAME}; explicitly freeze only after current sources are complete')
    manifest = json.loads(mp.read_text(encoding='utf-8'))
    if manifest.get('immutable_source_anchor_sha256') != ANCHOR_SHA256:
        raise VerificationError('Current manifest has the wrong immutable source anchor')
    if manifest.get('schema') != 5 or manifest.get('preceding_author_native_anchor_sha256') != GLOBAL_MINIMIZER_ANCHOR_SHA256:
        raise VerificationError('Current manifest has the wrong preceding-author source anchor or schema')
    if manifest.get('complete_physical_tube_anchor_sha256') != PHYSICAL_TUBE_ANCHOR_SHA256:
        raise VerificationError('Current manifest has the wrong complete physical-tube predecessor anchor')
    if manifest.get('complete_full_physical_anchor_sha256') != FULL_PHYSICAL_ANCHOR_SHA256:
        raise VerificationError('Current manifest has the wrong complete full-physical predecessor anchor')
    rows = manifest.get('files', [])
    listed = [x.get('path') for x in rows]
    actual = [p.relative_to(root).as_posix() for p in source_files(root)]
    if len(set(listed)) != len(listed):
        raise VerificationError('Duplicate current manifest paths')
    if set(listed) != set(actual):
        raise VerificationError(f'Current source membership mismatch: missing={sorted(set(listed)-set(actual))}; unlisted={sorted(set(actual)-set(listed))}')
    if manifest.get('source_count') != len(rows) or manifest.get('source_bytes') != sum(x['bytes'] for x in rows):
        raise VerificationError('Current manifest count/byte metadata mismatch')
    for row in rows:
        if excluded(row['path']):
            raise VerificationError(f'Excluded output incorrectly listed as source: {row["path"]}')
        check_row(root, row)
    if manifest.get('native_tex_closure') != closure:
        raise VerificationError('Current native TeX dependency closure changed')
    if manifest.get('history_verification') != history:
        raise VerificationError('Current manifest immutable-source verification metadata changed')
    return {'source_count': len(rows), 'source_bytes': sum(x['bytes'] for x in rows), 'immutable_source_anchor_sha256': ANCHOR_SHA256, 'preceding_author_native_anchor_sha256': GLOBAL_MINIMIZER_ANCHOR_SHA256, 'complete_physical_tube_anchor_sha256': PHYSICAL_TUBE_ANCHOR_SHA256,
        'complete_full_physical_anchor_sha256': FULL_PHYSICAL_ANCHOR_SHA256, 'active_core_count': len(closure['active_core_files']), 'verified': True}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('root', nargs='?', default='.')
    parser.add_argument('phase', nargs='?', default='history', choices=('history', 'freeze', 'verify'))
    args = parser.parse_args(argv)
    try:
        action = {'history': verify_history, 'freeze': freeze_manifest, 'verify': verify_manifest}[args.phase]
        result = action(Path(args.root))
        if args.phase == 'freeze':
            result = {'source_count': result['source_count'], 'source_bytes': result['source_bytes'], 'manifest': MANIFEST_NAME, 'phase': 'freeze'}
        print(json.dumps(result, indent=2, sort_keys=True))
        return 0
    except (VerificationError, OSError, ValueError, KeyError, TypeError) as exc:
        print(f'source verification failed: {exc}', file=sys.stderr)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
