#!/usr/bin/env python3
"""Authenticate the R79 census delta and frozen remote-head identities offline.

The unchanged R78 verify_history_r78.py must separately authenticate the 7,137
retained archive texts. This checker streams the 64 additional R78 source texts,
checks their exact extension to 7,201 indexed historical texts, and recomputes
all 873 distinct remote-head Git commit identities. It never invokes Git or the
network, extracts an archive, or writes under --source-root. The optional receipt
is the only file written. The audit bundle is read beside this script.
This is content authentication, not proof verification or independent refereeing.
"""
from __future__ import annotations
import argparse
import base64
import datetime as dt
import gzip
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import sys
import tarfile

MANIFEST_SHA256 = 'b7434b6afe8eefc34c8f61beee0342e8ac0bff09a59c904e5b4791ce356b271a'
RETAINED_INDEX_SHA256 = 'f2e351561ff93a68b2d680a8adc1f24531afe7f6212b48f941f973a149c445bb'
BASELINE = 'e0377beea364e456af2301f5e4fec98fe343cbcb'

def require(value, message):
    if not value:
        raise RuntimeError(message)

def digest(raw):
    return hashlib.sha256(raw).hexdigest()

def git_hash(kind, raw):
    return hashlib.sha1(f'{kind} {len(raw)}\0'.encode('ascii') + raw).hexdigest()

def checked_path(root, name):
    rel = PurePosixPath(name)
    require(not rel.is_absolute() and '..' not in rel.parts, 'Unsafe relative path')
    path = root.joinpath(*rel.parts)
    require(path.is_file() and not path.is_symlink() and root in path.resolve().parents,
            'Missing, nonregular, or escaped input: ' + name)
    return path

def indexed(rows):
    result = {}
    for row in rows:
        key = row.get('git_blob', '')
        require(re.fullmatch('[0-9a-f]{40}', key) and key not in result,
                'Invalid or duplicate indexed blob')
        require(type(row.get('bytes')) is int and row['bytes'] >= 0
                and re.fullmatch('[0-9a-f]{64}', row.get('sha256', '')),
                'Invalid indexed content identity')
        result[key] = row
    return result

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source-root', type=Path,
                        default=Path(__file__).resolve().parents[2],
                        help='standalone R79 source, containing retained R78 archives')
    parser.add_argument('--receipt', type=Path,
                        help='optional output JSON, outside the source directory')
    args = parser.parse_args()
    source = args.source_root.resolve()
    bundle = Path(__file__).resolve().parent
    require(source.is_dir(), 'Source root is not a directory')
    if args.receipt is not None:
        target = args.receipt.resolve()
        require(target != source and source not in target.parents,
                'Receipt must be outside source root; source is read-only')
    started = dt.datetime.now(dt.timezone.utc).isoformat()
    manifest_raw = checked_path(bundle, 'CURRENT_HISTORY_MANIFEST.json').read_bytes()
    require(digest(manifest_raw) == MANIFEST_SHA256, 'Pinned audit manifest differs')
    manifest = json.loads(manifest_raw)
    require(manifest['schema'] == 'theta.r79.portable-census-delta.v1'
            and manifest['baseline_source_commit'] == BASELINE, 'Unexpected manifest identity')
    authenticated_files = {}
    for row in manifest['files']:
        name = row['path']
        require(name not in authenticated_files, 'Duplicate manifest path')
        raw = checked_path(bundle, name).read_bytes()
        require(len(raw) == row['bytes'] and digest(raw) == row['sha256'],
                'Pinned input differs: ' + name)
        authenticated_files[name] = raw
    def read(name):
        raw = authenticated_files[name]
        return json.loads(gzip.decompress(raw) if name.endswith('.gz') else raw)
    retained_raw = checked_path(source,
        'provenance/r78-audit/current-census/HISTORICAL_TEXT_INDEX.json.gz').read_bytes()
    require(digest(retained_raw) == RETAINED_INDEX_SHA256, 'Retained R78 index differs')
    retained = indexed(json.loads(gzip.decompress(retained_raw)))
    extra = indexed(read('NEW_TEXT_INDEX.json.gz'))
    current = indexed(read('CURRENT_HISTORICAL_TEXT_INDEX.json.gz'))
    require(len(retained) == 7137 and len(extra) == 64 and len(current) == 7201
            and not set(retained) & set(extra)
            and set(current) == set(retained) | set(extra), 'Census set partition differs')
    for key, row in {**retained, **extra}.items():
        require(all(row[k] == current[key][k] for k in ('bytes', 'sha256')),
                'Historical content identity changed: ' + key)
    require(sum(r['bytes'] for r in current.values()) == 112371368
            and sum(r['bytes'] for r in extra.values()) == 4205492,
            'Historical text byte totals differ')
    seen = set()
    text_bytes = 0
    with tarfile.open(checked_path(bundle, 'HISTORICAL_TEXT_DELTA_R79.tar.gz'), 'r|gz') as ar:
        for member in ar:
            path = PurePosixPath(member.name)
            require(member.isfile() and len(path.parts) == 2
                    and path.parts[0] == 'blobs' and path.suffix == '.txt'
                    and path.stem in extra and path.stem not in seen,
                    'Unexpected or duplicate archive member')
            key = path.stem
            handle = ar.extractfile(member)
            require(handle is not None, 'Unreadable archive member')
            with handle:
                raw = handle.read()
            row = extra[key]
            require(len(raw) == member.size == row['bytes']
                    and git_hash('blob', raw) == key and digest(raw) == row['sha256'],
                    'Archive member content differs: ' + key)
            text = raw.decode(row.get('encoding', 'utf-8'))
            require(len(text.splitlines()) == row['lines'], 'Decoded line count differs')
            text_bytes += len(raw)
            seen.add(key)
    require(seen == set(extra), 'Missing delta archive members')
    refs = read('CURRENT_REFS.json')['all']
    require(len(refs) == 1307 and len({r['ref'] for r in refs}) == 1307
            and all(r['ref'].startswith('refs/heads/') for r in refs),
            'Unexpected frozen remote refs')
    required_heads = {r['sha'] for r in refs}
    heads = read('ALL_HEAD_COMMIT_IDENTITIES.json.gz')
    metadata = {r['sha']: r for r in heads}
    require(len(heads) == len(metadata) == len(required_heads) == 873
            and set(metadata) == required_heads, 'Head metadata set differs')
    seen_heads = set()
    for row in read('HEAD_COMMIT_OBJECTS.json.gz'):
        key = row['sha']
        raw = base64.b64decode(row['payload_base64'], validate=True)
        require(key in required_heads and key not in seen_heads
                and git_hash('commit', raw) == key, 'Commit payload identity differs')
        header, separator, message = raw.partition(b'\n\n')
        require(separator, 'Malformed commit')
        fields = header.splitlines()
        trees = [s[5:].decode('ascii') for s in fields if s.startswith(b'tree ')]
        parents = [s[7:].decode('ascii') for s in fields if s.startswith(b'parent ')]
        require(trees == [metadata[key]['tree']] and parents == metadata[key]['parents']
                and message.decode('utf-8').splitlines()[0] == metadata[key]['subject'],
                'Commit metadata differs from its authenticated payload')
        seen_heads.add(key)
    require(seen_heads == required_heads, 'Missing frozen head payloads')
    delta = read('REF_DELTA_FROM_R78.json')
    require(delta['old_count'] == 1306 and delta['new_count'] == 1307
            and not delta['changed'] and not delta['removed']
            and len(delta['added']) == 1 and delta['added'][0]['sha'] == BASELINE,
            'Unexpected snapshot change')
    census = read('CURRENT_CENSUS_RECEIPT.json')
    require(census['status'] == 'PASS' and census['remote_heads'] == 1307
            and census['distinct_head_commits'] == 873 and census['ancestor_commits'] == 2711
            and census['total_text_blobs_read_authenticated_decoded'] == 7201
            and census['refs_sha256'] == digest(authenticated_files['CURRENT_REFS.json'])
            and census['archive_receipt_sha256'] == digest(authenticated_files['HISTORICAL_ARCHIVE_AUTHENTICATION.json'])
            and census['verifier_sha256'] == digest(authenticated_files['refresh_census.py']),
            'Recorded census linkage differs')
    require(read('NEW_REPORT_CANDIDATES.json') == [], 'Unexpected new referee report candidate')
    receipt = {
        'schema': 'theta.r79.portable-current-history-verification.v1', 'status': 'PASS',
        'started_utc': started, 'completed_utc': dt.datetime.now(dt.timezone.utc).isoformat(),
        'command': [sys.executable, *sys.argv], 'baseline_source_commit': BASELINE,
        'verifier_sha256': digest(Path(__file__).read_bytes()),
        'manifest_sha256': MANIFEST_SHA256,
        'additional_text_blobs_read_authenticated_decoded': len(seen),
        'additional_text_bytes_read_authenticated_decoded': text_bytes,
        'retained_index_blobs': len(retained), 'combined_index_blobs': len(current),
        'combined_index_bytes': sum(r['bytes'] for r in current.values()),
        'remote_heads': len(refs), 'distinct_head_commit_payloads_authenticated': len(seen_heads),
        'new_independent_referee_report_candidates': 0,
        'retained_archive_requirement': 'Run unchanged provenance/r78-audit/verify_history_r78.py separately to authenticate retained 7137 archive payloads in this verification run.',
        'scope': 'Offline byte and commit identity verification only; no theorem reproof, human expert review, remote CI, editorial decision, or remote mutation.'
    }
    result = json.dumps(receipt, indent=2, sort_keys=True) + '\n'
    if args.receipt is not None:
        args.receipt.write_text(result, encoding='utf-8')
    print(result, end='')

if __name__ == '__main__':
    main()
