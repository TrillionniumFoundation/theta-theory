#!/usr/bin/env python3
"""Copy a closed evidence packet, verifying every original and copied byte."""
import argparse
import hashlib
import json
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument('source', type=Path)
parser.add_argument('seal')
parser.add_argument('destination', type=Path)
args = parser.parse_args()
source = args.source.resolve()
destination = args.destination.resolve()
assert not destination.exists(), 'Never overwrite an evidence packet'
assert 'delivery/publication/marked-boundary-source-20261019' in str(destination)
seal_path = source / args.seal
seal = json.loads(seal_path.read_bytes())
rows = seal['files']
actual_paths = {p.relative_to(source).as_posix() for p in source.rglob('*') if p.is_file()}
declared_paths = {row['path'] for row in rows} | {args.seal}
assert actual_paths == declared_paths, (sorted(actual_paths - declared_paths), sorted(declared_paths - actual_paths))
for row in rows:
    data = (source / row['path']).read_bytes()
    assert len(data) == row['bytes']
    assert hashlib.sha256(data).hexdigest() == row['sha256']
destination.mkdir(parents=True)
for relative in sorted(actual_paths):
    target = destination / relative
    target.parent.mkdir(parents=True, exist_ok=True)
    original = (source / relative).read_bytes()
    target.write_bytes(original)
    assert target.read_bytes() == original
print(json.dumps({'status': 'passed', 'source': str(source), 'destination': str(destination), 'files': len(actual_paths), 'bytes': sum((source / relative).stat().st_size for relative in actual_paths), 'seal_sha256': hashlib.sha256(seal_path.read_bytes()).hexdigest()}, indent=2))
