#!/usr/bin/env python3
"""Publish the authorized, hash-pinned A2 v9 packet without touching other refs.
The transport branch is not an ancestor of the manuscript revision branch.
"""
from __future__ import annotations
import argparse
import base64
import hashlib
import json
import lzma
import os
from pathlib import Path, PurePosixPath
import shutil
import subprocess
import sys
import tempfile

BASE = '79ff2f96fc2e41899666065355238915f21273b0'
BASE_TREE = '53ee30324ded06e3443af93ed87f18a936f1599a'
TARGET = 'revision/a2-v9-nonlinear-boundary-compatibility-2026-09-09'
PREFIX = 'papers/A2-v9-nonlinear-boundary-compatibility/'
PAYLOAD_HASH = 'eeba93cc4d5e0bc4f03d7dd2604bcdc13e62fd885b6cb8fe8195f3b367e687d0'
XZ_HASH = 'ef947b9ee98acd7348d4e6d3b76a8d9f0384e63a9ea062afd30f30d48fff9a91'
HERE = Path(__file__).resolve().parent


def require(ok: bool, message: str) -> None:
    if not ok:
        raise RuntimeError(message)


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def blob(data: bytes) -> str:
    return hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()


def run(args: list[str], *, data: bytes | None = None,
        env: dict[str, str] | None = None, cwd: Path | None = None) -> bytes:
    result = subprocess.run(args, input=data, env=env, cwd=cwd,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode:
        sys.stderr.buffer.write(result.stdout + result.stderr)
        raise RuntimeError('Command failed: ' + ' '.join(args))
    return result.stdout


def git(*args: str, data: bytes | None = None,
        env: dict[str, str] | None = None) -> str:
    return run(['git', *args], data=data, env=env).decode().strip()


def read_payload() -> dict:
    chunks = [HERE / ('chunk-%02d.b64' % i) for i in range(8)]
    raw = base64.b64decode(''.join(p.read_text().strip() for p in chunks), validate=True)
    require(digest(raw) == XZ_HASH, 'Transport digest mismatch')
    decoded = lzma.decompress(raw)
    require(digest(decoded) == PAYLOAD_HASH, 'Payload digest mismatch')
    p = json.loads(decoded)
    require(len(p['reuse']) == 82 and len(p['text']) == 35 and len(p['binary']) == 2,
            'Unexpected payload inventory')
    require(set(p['reuse']) | set(p['text']) | set(p['binary']) == set(p['hashes']),
            'Manifest inventory mismatch')
    require(len(p['hashes']) == 119, 'Expected 119 original packet files')
    for name in p['hashes']:
        path = PurePosixPath(name)
        require(not path.is_absolute() and '..' not in path.parts and '\\' not in name,
                'Unsafe payload path: ' + name)
    return p


def restore(p: dict, destination: Path) -> None:
    destination.mkdir(parents=True, exist_ok=False)
    for name, expected in p['hashes'].items():
        if name in p['binary']:
            continue
        if name in p['text']:
            data = p['text'][name].encode('utf-8')
        else:
            source = HERE / 'reuse' / name
            require(source.is_file() and not source.is_symlink(), 'Missing reused file: ' + name)
            data = source.read_bytes()
            require(blob(data) == p['reuse'][name], 'Reused blob mismatch: ' + name)
        require(digest(data) == expected, 'Original file digest mismatch: ' + name)
        target = destination / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
    print('RESTORED_ORIGINAL_TEXT_FILES=117', flush=True)


def native_commit(files: dict[str, bytes], parent: str, message: str) -> str:
    with tempfile.TemporaryDirectory(prefix='a2-native-index-') as tmp:
        env = dict(os.environ)
        env.update(GIT_INDEX_FILE=str(Path(tmp) / 'index'),
                   GIT_AUTHOR_NAME='github-actions[bot]',
                   GIT_AUTHOR_EMAIL='41898282+github-actions[bot]@users.noreply.github.com',
                   GIT_COMMITTER_NAME='github-actions[bot]',
                   GIT_COMMITTER_EMAIL='41898282+github-actions[bot]@users.noreply.github.com')
        git('read-tree', parent, env=env)
        for name, data in sorted(files.items()):
            require(name.startswith(PREFIX), 'Out-of-scope write')
            sha = git('hash-object', '-w', '--stdin', data=data)
            require(sha == blob(data), 'Git blob identity mismatch')
            git('update-index', '--add', '--cacheinfo', '100644,' + sha + ',' + name, env=env)
        tree = git('write-tree', env=env)
        changes = git('diff-tree', '--no-commit-id', '--name-status', '-r', BASE, tree)
        expected = set(files)
        actual = set()
        for line in changes.splitlines():
            status, name = line.split('\t', 1)
            require(status == 'A' and name.startswith(PREFIX), 'Nonadditive or out-of-scope change')
            actual.add(name)
        require(actual == expected, 'Changed-file inventory mismatch')
        sha = git('commit-tree', tree, '-p', parent, data=(message + '\n').encode(), env=env)
        for name, data in files.items():
            require(git('rev-parse', sha + ':' + name) == blob(data), 'Read-back blob mismatch')
        return sha


def remote_head() -> str | None:
    result = git('ls-remote', '--heads', 'origin', 'refs/heads/' + TARGET)
    return result.split()[0] if result else None


def push_and_read(sha: str, expected: str | None) -> None:
    require(remote_head() == expected, 'Target branch changed; refusing to overwrite')
    git('push', 'origin', sha + ':refs/heads/' + TARGET)
    require(remote_head() == sha, 'Remote ref read-back mismatch')
    print('REMOTE_VERIFIED_COMMIT=' + sha, flush=True)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--restore-only', type=Path)
    args = parser.parse_args()
    payload = read_payload()
    if args.restore_only:
        restore(payload, args.restore_only)
        return
    require(os.environ.get('GITHUB_REPOSITORY') == 'TrillionniumFoundation/theta-theory',
            'Unexpected repository')
    require(git('rev-parse', BASE + '^{tree}') == BASE_TREE, 'Frozen review tree mismatch')
    require(not git('ls-tree', BASE, PREFIX.rstrip('/')), 'Destination already exists at base')
    require(remote_head() is None, 'Target branch already exists; no force push is allowed')
    with tempfile.TemporaryDirectory(prefix='a2-v9-publication-') as tmp:
        work = Path(tmp)
        original = work / 'original'
        restore(payload, original)
        check = work / 'check'
        shutil.copytree(original, check)
        totals = {}
        for script, total in [('verify_v9.py', 407), ('verify_revision.py', 249)]:
            results = []
            for flags, suffix in [([], 'normal'), (['-O'], 'optimized')]:
                output = work / (script + '.' + suffix + '.json')
                text = run([sys.executable, *flags, str(check / 'tools' / script),
                            '--output', str(output)])
                print(text.decode().strip(), flush=True)
                result = json.loads(output.read_text())
                require(result['status'] == 'pass' and result['counts']['total'] == total,
                        'Diagnostic suite failure: ' + script)
                results.append(output.read_bytes())
            require(results[0] == results[1], 'Normal and optimized diagnostics disagree')
            totals[script] = total
        files = {PREFIX + name: (original / name).read_bytes()
                 for name in payload['hashes'] if name not in payload['binary']}
        source_sha = native_commit(files, BASE,
            'A2 v9: publish complete native revision sources and referee response\n\n'
            'Restore all 117 text files byte-for-byte from the delivered packet. '
            'Preserve the frozen review baseline. Re-run 407+249 finite diagnostics '
            'in normal and optimized modes. Compiled PDFs follow after independent rebuild.')
        push_and_read(source_sha, None)
        print('SOURCE_COMMIT=' + source_sha, flush=True)
        print(run([sys.executable, str(check / 'tools' / 'build.py')]).decode(), flush=True)
        build_record = json.loads((check / 'verification' / 'build.json').read_text())
        for name, spec in payload['binary'].items():
            data = (check / name).read_bytes()
            print('REBUILT_PDF ' + name + ' sha256=' + digest(data), flush=True)
            require(digest(data) == spec['sha256'] and blob(data) == spec['git_blob'],
                    'Rebuilt PDF is not byte-identical to the delivered packet: ' + name)
            (original / name).write_bytes(data)
            files[PREFIX + name] = data
        require(len(files) == 119, 'Incomplete original packet')
        for name, expected in payload['hashes'].items():
            require(digest((original / name).read_bytes()) == expected,
                    'Final original-file verification failure: ' + name)
        receipt = {
            'schema': 'a2-v9-remote-materialization-v1',
            'repository': 'TrillionniumFoundation/theta-theory',
            'branch': TARGET, 'frozen_review_parent': BASE,
            'source_commit_pushed_and_read_back': source_sha,
            'paper_path': PREFIX.rstrip('/'),
            'original_packet_files': 119, 'all_original_files_byte_identical': True,
            'original_file_sha256': payload['hashes'],
            'pdf_git_blobs': {name: spec['git_blob'] for name, spec in payload['binary'].items()},
            'remote_clean_build': build_record['documents'],
            'remote_diagnostics': totals,
            'normal_and_optimized_diagnostic_outputs_identical': True,
            'workflow_run': os.environ['GITHUB_SERVER_URL'] + '/' + os.environ['GITHUB_REPOSITORY']
                            + '/actions/runs/' + os.environ['GITHUB_RUN_ID'],
            'publication_changes': 'Only added files under the new manuscript directory; no existing files altered.',
            'historical_status_note': 'DELIVERY_STATUS.json and other original packet-generation records remain unchanged. This receipt records the later remote materialization.',
            'scope': 'Publication integrity and finite diagnostics; not formal mathematical proof certification.'
        }
        files[PREFIX + 'PUBLICATION_RECEIPT.json'] = (json.dumps(receipt, indent=2, sort_keys=True) + '\n').encode()
        final = native_commit(files, source_sha,
            'A2 v9: add byte-identical compiled PDFs and verified publication receipt\n\n'
            'All 119 original packet files match SHA-256 and Git blob identities. '
            'Add a dated remote materialization record without rewriting historical status files. '
            'Only the new revision directory changes; no merges or force pushes.')
        push_and_read(final, source_sha)
        paper_tree = git('rev-parse', final + ':' + PREFIX.rstrip('/'))
        print('PUBLISHED_SHA=' + final, flush=True)
        print('PUBLISHED_PAPER_TREE=' + paper_tree, flush=True)
        summary = os.environ.get('GITHUB_STEP_SUMMARY')
        if summary:
            Path(summary).write_text('A2 v9 published and remote ref verified.\n\nCommit: `' + final
                + '`\n\nPaper tree: `' + paper_tree + '`\n\n119 original files byte-identical; '
                'one new publication receipt. No existing files modified or deleted.\n')


if __name__ == '__main__':
    main()
