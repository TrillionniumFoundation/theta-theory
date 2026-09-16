#!/usr/bin/env python3
"""Immutable Git snapshots and fail-closed TeX-recorder verification.

The trusted boundary is Git plus the installed TeX toolchain. This is not a
proof against a malicious compiler or an adversary changing a file during a
read and restoring it afterwards. System packages/fonts are hashed, never
copied into the distributed source archive.
"""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import zipfile

PRODUCT_SUFFIXES = ('.pdf', '.log', '.aux', '.fls', '.fdb_latexmk', '.out',
                    '.toc', '.lof', '.lot', '.synctex.gz')
GENERATED_INPUT_SUFFIXES = ('.aux', '.out', '.toc', '.lof', '.lot')
INPUT = re.compile(r'\\(?:input|include)\s*\{([^}]+)\}')


def require(ok: bool, message: str) -> None:
    if not ok:
        raise RuntimeError(message)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def blob_id(data: bytes) -> str:
    return hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()


def write_json(path: Path, value: object) -> None:
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + '\n', encoding='utf-8')


def git(root: Path, *args: str, data: bytes | None = None) -> bytes:
    cp = subprocess.run(['git', *args], cwd=root, input=data, capture_output=True)
    require(cp.returncode == 0, 'Git command failed: ' + ' '.join(args) + '\n' +
            cp.stderr.decode(errors='replace'))
    return cp.stdout


def safe_relative(name: str) -> Path:
    p = Path(name)
    require(bool(name) and not p.is_absolute() and '..' not in p.parts and
            '\\' not in name and '\x00' not in name, 'Unsafe relative path: ' + repr(name))
    return p


def strip_comments(text: str) -> str:
    lines = []
    for line in text.splitlines():
        for i, char in enumerate(line):
            if char == '%':
                k = i - 1
                while k >= 0 and line[k] == '\\':
                    k -= 1
                if (i - k - 1) % 2 == 0:
                    line = line[:i]
                    break
        lines.append(line)
    return '\n'.join(lines)


def graph(source: Path, entry: str, visited: set[str] | None = None) -> set[str]:
    visited = set() if visited is None else visited
    name = safe_relative(entry).as_posix()
    if name in visited:
        return visited
    path = source / name
    require(path.is_file() and not path.is_symlink(), 'Missing regular native TeX input: ' + name)
    visited.add(name)
    for raw in INPUT.findall(strip_comments(path.read_text(encoding='utf-8'))):
        require(re.fullmatch(r'[A-Za-z0-9_./-]+', raw) is not None,
                'Unresolved dynamic TeX input in ' + name + ': ' + raw)
        graph(source, raw if raw.endswith('.tex') else raw + '.tex', visited)
    return visited


def freeze_git_source(source: Path, destination: Path,
                      entries: tuple[str, ...]) -> dict:
    """Read bytes from HEAD's Git objects, not a mutable working-tree copy."""
    source = source.resolve()
    root = Path(git(source, 'rev-parse', '--show-toplevel').decode().strip()).resolve()
    prefix = source.relative_to(root).as_posix()
    require(prefix != '.', 'Expected a manuscript subtree, not the repository root')
    commit = git(root, 'rev-parse', '--verify', 'HEAD^{commit}').decode().strip()
    tree = git(root, 'rev-parse', commit + ':' + prefix).decode().strip()
    dirty = git(root, 'status', '--porcelain=v1', '--untracked-files=all', '--', prefix)
    require(not dirty, 'Manuscript working tree is not clean; commit or isolate changes before building')
    require(not destination.exists(), 'Snapshot destination already exists')
    records = []
    for record in git(root, 'ls-tree', '-r', '-z', tree).split(b'\0'):
        if not record:
            continue
        meta, raw_name = record.split(b'\t', 1)
        mode, kind, oid = meta.decode().split()
        name = raw_name.decode('utf-8')
        safe_relative(name)
        require(kind == 'blob' and mode in ('100644', '100755'),
                'Nonregular object in source tree: ' + name)
        records.append((name, mode, oid))
    require(bool(records), 'Empty source tree')
    stream = git(root, 'cat-file', '--batch',
                 data=''.join(oid + '\n' for _, _, oid in records).encode())
    offset = 0
    excluded = {stem + suffix for stem in entries for suffix in PRODUCT_SUFFIXES}
    files, skipped = {}, {}
    destination.mkdir(parents=True)
    for name, mode, oid in records:
        end = stream.find(b'\n', offset)
        require(end >= 0, 'Truncated Git batch header')
        header = stream[offset:end].decode().split()
        require(len(header) == 3 and header[:2] == [oid, 'blob'], 'Invalid Git batch header')
        size = int(header[2])
        data = stream[end + 1:end + 1 + size]
        offset = end + size + 2
        require(len(data) == size and stream[offset - 1:offset] == b'\n' and blob_id(data) == oid,
                'Git blob content mismatch: ' + name)
        item = {'git_blob': oid, 'mode': mode, 'bytes': size,
                'sha256': hashlib.sha256(data).hexdigest()}
        if name in excluded:
            skipped[name] = item
            continue
        # Native paper sources have no standalone font assets. Do not package fonts.
        require(Path(name).suffix.lower() not in ('.ttf', '.otf', '.pfb', '.pfa', '.woff', '.woff2'),
                'Standalone font assets are outside this source-delivery policy: ' + name)
        target = destination / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
        target.chmod(0o444)
        files[name] = item
    require(offset == len(stream), 'Unparsed Git batch bytes')
    # The executed verifier must be the verifier named by the declared commit.
    for name in ('tools/build_submission.py', 'tools/source_provenance.py'):
        require(name in files and (source / name).is_file() and
                sha256(source / name) == files[name]['sha256'],
                'Executed verifier differs from declared Git source: ' + name)
    return {'schema': 1, 'source_commit': commit, 'source_tree': tree,
            'repository_tree': git(root, 'rev-parse', commit + '^{tree}').decode().strip(),
            'source_prefix': prefix, 'working_tree': 'clean',
            'snapshot_mode': 'Git object bytes; root build products explicitly excluded',
            'files': files, 'excluded_tracked_products': skipped}


def verify_copy(work: Path, files: dict) -> None:
    for name, item in files.items():
        path = work / safe_relative(name)
        require(path.is_file() and not path.is_symlink(), 'Missing or symlinked snapshot input: ' + name)
        require(path.resolve() == Path(os.path.abspath(path)), 'Symlinked input ancestor: ' + name)
        require(path.stat().st_size == item['bytes'] and sha256(path) == item['sha256'] and
                blob_id(path.read_bytes()) == item['git_blob'], 'Snapshot bytes differ: ' + name)


def source_archive(source: Path, manifest: dict, target: Path) -> None:
    verify_copy(source, manifest['files'])
    with zipfile.ZipFile(target, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        payloads = [('SOURCE_MANIFEST.json', (json.dumps(manifest, indent=2, sort_keys=True) + '\n').encode())]
        payloads += [('source/' + name, (source / name).read_bytes()) for name in sorted(manifest['files'])]
        for name, data in payloads:
            info = zipfile.ZipInfo(name, date_time=(2026, 9, 13, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            # A frozen snapshot is read-only, so filesystem permissions are
            # not the source of truth. Preserve the recorded Git modes (R68-P1).
            mode = (int(manifest['files'][name[len('source/'):]]['mode'], 8)
                    if name.startswith('source/') else 0o100644)
            require(mode in (0o100644, 0o100755), 'Unsupported archive mode: ' + name)
            info.create_system = 3  # Unix permission interpretation in ZIP headers.
            info.external_attr = mode << 16
            archive.writestr(info, data)


def tex_roots(env: dict[str, str]) -> list[Path]:
    roots = []
    for key in ('TEXMFDIST', 'TEXMFMAIN', 'TEXMFDEBIAN', 'TEXMFLOCAL',
                'TEXMFSYSVAR', 'TEXMFSYSCONFIG'):
        cp = subprocess.run(['kpsewhich', '-var-value=' + key], env=env,
                            capture_output=True, text=True, check=True)
        for raw in cp.stdout.strip().split(os.pathsep):
            if not raw:
                continue
            path = Path(raw.removeprefix('!!')).resolve()
            require(path != Path('/') and path.is_absolute(), 'Unsafe TeX installation root')
            if path.is_dir() and path not in roots:
                roots.append(path)
    require(bool(roots), 'No explicit TeX installation roots found')
    return roots


def verify_generated(work: Path, imported: dict) -> None:
    for name, item in imported.items():
        path = work / safe_relative(name)
        require(path.is_file() and not path.is_symlink() and
                path.resolve() == Path(os.path.abspath(path)),
                'Missing or symlinked imported generated input: ' + name)
        require(path.stat().st_size == item['bytes'] and sha256(path) == item['sha256'],
                'Imported generated input differs from producer: ' + name)


def recorder_inputs(stem: str, work: Path, files: dict,
                    expected: set[str], external_roots: list[Path],
                    imported_generated: dict | None = None) -> dict:
    """Hash actual compilation inputs and compare every native input to Git."""
    work = work.resolve()
    imported_generated = {} if imported_generated is None else imported_generated
    require(not set(files).intersection(imported_generated), 'Source/generated input overlap')
    verify_generated(work, imported_generated)
    recorder = work / (stem + '.fls')
    require(recorder.is_file() and recorder.stat().st_size > 0, 'Missing or empty TeX recorder')
    lines = recorder.read_text(encoding='utf-8', errors='strict').splitlines()
    pwds = {Path(line[4:]).resolve() for line in lines if line.startswith('PWD ')}
    require(pwds == {work}, 'Recorder working directory is missing or inconsistent')
    verify_copy(work, files)
    outputs = set()
    for line in lines:
        if line.startswith('OUTPUT '):
            p = Path(line[7:])
            outputs.add((work / p if not p.is_absolute() else p).resolve())
    source_inputs, generated, external = {}, {}, {}
    allowed_generated = {stem + suffix for suffix in GENERATED_INPUT_SUFFIXES}
    for line in lines:
        if not line.startswith('INPUT '):
            continue
        raw = Path(line[6:])
        lexical = Path(os.path.abspath(work / raw if not raw.is_absolute() else raw))
        candidate = lexical.resolve(strict=True)
        require(candidate.is_file(), 'Recorder input is not a file: ' + str(candidate))
        item = {'bytes': candidate.stat().st_size, 'sha256': sha256(candidate)}
        if candidate.is_relative_to(work):
            require(candidate == lexical, 'Symlinked recorder input: ' + str(lexical))
            name = candidate.relative_to(work).as_posix()
            if name in files:
                frozen = files[name]
                require(item['sha256'] == frozen['sha256'] and item['bytes'] == frozen['bytes'] and
                        blob_id(candidate.read_bytes()) == frozen['git_blob'],
                        'Compilation input differs from frozen source: ' + name)
                source_inputs[name] = dict(item, git_blob=frozen['git_blob'])
            elif name in imported_generated:
                producer = imported_generated[name]
                require(item['sha256'] == producer['sha256'] and item['bytes'] == producer['bytes'],
                        'Imported generated input differs from producer: ' + name)
                generated[name] = dict(producer, origin='Verified prior-entry output; not frozen source')
            elif name in allowed_generated and candidate in outputs:
                generated[name] = dict(item, origin='TeX output; not a frozen source file')
            else:
                raise RuntimeError('Unexplained local recorder input: ' + name)
        else:
            # An input escaping through a work-tree symlink is never a package.
            require(not lexical.is_relative_to(work), 'Recorder input escapes compilation tree')
            require(any(candidate.is_relative_to(root.resolve()) for root in external_roots),
                    'Input outside declared TeX installations: ' + str(candidate))
            external[str(candidate)] = item
    require(stem + '.tex' in source_inputs, 'Native entry is absent from recorder')
    require(set(imported_generated).issubset(generated),
            'Declared imported generated inputs absent from recorder')
    missing = sorted(expected - source_inputs.keys())
    require(not missing, 'Recursive native inputs absent from recorder: ' + ', '.join(missing))
    return {'source_inputs': source_inputs, 'generated_inputs': generated,
            'external_inputs': external, 'expected_native_inputs': sorted(expected),
            'verification': 'Actual compilation bytes equal the frozen Git manifest'}
