#!/usr/bin/env python3
"""One-shot, checksummed source transport. Writes only inside this v114 directory."""
from __future__ import annotations
import base64
import hashlib
import json
import lzma
from pathlib import Path, PurePosixPath
import subprocess

HERE = Path(__file__).resolve().parent
BASE = '63daaeee1da5a1ee3ac569584e06f55081073da0'
OLD = 'papers/A2-v17-boundary-information-coarsening/article/v113/'
PACK_SHA256 = '642413980be15cf32552275b0438166c7d446329809cf85fe775a21f75c4bcbb'
CHUNKS = 6

def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def target(name: str) -> Path:
    p = PurePosixPath(name)
    if p.is_absolute() or '..' in p.parts or p.suffix not in {'.tex','.md','.py'}:
        raise ValueError('Unsafe materialization target: '+name)
    out = HERE.joinpath(*p.parts)
    if not out.resolve().is_relative_to(HERE):
        raise ValueError('Target escapes article directory')
    return out

def baseline(spec: dict) -> bytes:
    path = spec['path']
    if not path.startswith(OLD) or '..' in PurePosixPath(path).parts:
        raise ValueError('Invalid baseline path')
    data = subprocess.check_output(['git','show',BASE+':'+path],cwd=HERE)
    if sha(data) != spec['sha256']:
        raise ValueError('Baseline digest mismatch: '+path)
    return data

def main() -> None:
    marker = HERE/'SOURCE_MATERIALIZATION.json'
    if marker.exists():
        print('Source already materialized; later manuscript edits are not overwritten.')
        return
    packed = ''.join((HERE/'.sourcepack'/f'{i:03d}.b64').read_text().strip()
                     for i in range(CHUNKS))
    data = base64.b64decode(packed,validate=True)
    if sha(data) != PACK_SHA256:
        raise ValueError('Compressed source-pack digest mismatch')
    payload = json.loads(lzma.decompress(data))
    if payload['baseline'] != BASE:
        raise ValueError('Wrong frozen review baseline')
    files = {name:text.encode('utf-8') for name,text in payload['files'].items()}
    for name,spec in payload['copies'].items():
        if name in files: raise ValueError('Duplicate source name')
        files[name] = baseline(spec)
    for name,spec in payload['patches'].items():
        if name in files: raise ValueError('Duplicate source name')
        old = baseline(spec['base']).decode('utf-8')
        result,last = [],0
        for i,j,replacement in spec['edits']:
            if not (last <= i <= j <= len(old)):
                raise ValueError('Invalid/nonmonotone source edit')
            result.extend([old[last:i],replacement]); last=j
        result.append(old[last:])
        files[name] = ''.join(result).encode('utf-8')
    if set(files) != set(payload['sha256']):
        raise ValueError('Incomplete source manifest')
    for name,contents in files.items():
        out=target(name)
        if sha(contents) != payload['sha256'][name]:
            raise ValueError('Materialized digest mismatch: '+name)
        if out.exists() and out.read_bytes() != contents:
            raise ValueError('Refusing to overwrite different existing source: '+name)
    for name,contents in files.items():
        out=target(name);out.parent.mkdir(parents=True,exist_ok=True);out.write_bytes(contents)
    bootstrap=subprocess.check_output(['git','rev-parse','HEAD'],cwd=HERE,text=True).strip()
    marker.write_text(json.dumps({'bootstrap_commit':bootstrap,'baseline_review_commit':BASE,
                                 'compressed_pack_sha256':PACK_SHA256,
                                 'materialized_file_sha256':payload['sha256']},
                                indent=2,sort_keys=True)+'\n')
    print(f'Materialized and checked {len(files)} manuscript and review files.')

if __name__ == '__main__':
    main()
