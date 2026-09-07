#!/usr/bin/env python3
"""Reproduce the validated v20 text delta from its pinned transport.

The completed branch contains ordinary readable TeX, Python and Markdown.
This idempotent publisher makes no network requests and refuses unrelated
local edits. The transport is data, not executable code.
"""
from __future__ import annotations
import hashlib
import json
import lzma
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parent
PAYLOAD_SHA256 = 'ce0264c095f704e1b95e5ae19b9d00c9016c737ee721e8d9888936089d6f32aa'
MANIFEST_BLOB = 'eb846da7fe3e036ebe31c91ecac7b39c52cb3900'
FINAL_TEXT_EDITS = {'sections/exact_kernels.tex': [('have dimensions $d,k$. No ordering of these dimensions is '
                                 'required in\n'
                                 'this section. For $U\\subset F$ put',
                                 'have dimensions $d,k$. No ordering of these dimensions is '
                                 'required in\n'
                                 'this section. Measures $\\mu$ below are Borel probabilities. For '
                                 '$U\\subset F$ put'),
                                ('Let $P(u,x)$ be a positive history product, twice continuously\n'
                                 'differentiable in an interior command neighborhood of $u_*$, and '
                                 'let',
                                 'Let $P:O\\to C(X;\\R)$ be a positive history-product map of '
                                 'class $C^2$,\n'
                                 'where $u_*$ is an interior point of the command neighborhood '
                                 '$O$, and let'),
                                ('Whenever $r_U>1$, commands with a density bounded below near '
                                 '$u_*$',
                                 'For each maximizing prior with $r_U>1$, commands with a density\n'
                                 'bounded below near $u_*$')],
 'core/06b_collision_geometry.tex': [('For arbitrary additive collisions, the appropriate '
                                      'invariant is a family\n'
                                      'of maximal Vandermonde products on the future exponent set.',
                                      'The affine hypothesis can be removed altogether. The '
                                      'appropriate invariant\n'
                                      'is a family of maximal Vandermonde products on the future '
                                      'exponent set.')],
 'build.py': [("           'core/06b_collision_geometry.tex',\n", ''),
              ("              'sections/covariance_degenerations.tex',\n"
               "              'core/06b_collision_geometry.tex'}",
               "              'sections/covariance_degenerations.tex'}")],
 'README.md': [('The three documented inherited prose edits',
                'The two documented inherited prose edits')],
 'NUMERICAL_EVIDENCE_V20.md': [('in the three prose-edited inherited files',
                                'in the two prose-edited inherited files')]}

def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def main() -> None:
    archive = ROOT/'history/v19'
    manifest = (archive/'SOURCE_MANIFEST.json').read_bytes()
    blob = hashlib.sha1(b'blob '+str(len(manifest)).encode()+b'\0'+manifest).hexdigest()
    if blob != MANIFEST_BLOB:
        raise ValueError('Pinned v19 manifest changed')
    for name, digest in json.loads(manifest)['files'].items():
        if sha((archive/name).read_bytes()) != digest:
            raise ValueError('Pinned archived source changed: '+name)
    data = b''.join((ROOT/f'revision_transport/part-{i:02d}.xz').read_bytes()
                    for i in range(1,5))
    if sha(data) != PAYLOAD_SHA256:
        raise ValueError('Revision transport hash mismatch')
    payload = json.loads(lzma.decompress(data))
    if payload['version'] != 20 or payload['basis'] != '01abeb689b203ea871b88495d16a826bb4942e16':
        raise ValueError('Wrong revision transport')
    outputs = {}
    for name, item in payload['files'].items():
        rel = PurePosixPath(name)
        if rel.is_absolute() or '..' in rel.parts or rel.parts[0] in {'history','validation','build','revision_transport'}:
            raise ValueError('Disallowed output path: '+name)
        target = ROOT/name
        if not target.resolve().is_relative_to(ROOT):
            raise ValueError('Escaping output path: '+name)
        basis = item.get('basis_sha256')
        if basis:
            raw = (archive/name).read_bytes()
            if sha(raw) != basis:
                raise ValueError('Delta basis mismatch: '+name)
        if 'content' in item:
            text = item['content']
        else:
            lines = raw.decode().splitlines(keepends=True)
            previous = 0
            for start, stop, replacement in item['line_edits']:
                if not 0 <= previous <= start <= stop <= len(lines):
                    raise ValueError('Invalid line delta: '+name)
                previous = stop
            for start, stop, replacement in reversed(item['line_edits']):
                lines[start:stop] = [replacement]
            text = ''.join(lines)
        if sha(text.encode()) != item['result_sha256']:
            raise ValueError('Reconstructed source mismatch: '+name)
        for old, new in FINAL_TEXT_EDITS.get(name, []):
            if text.count(old) != 1:
                raise ValueError('Final clarification anchor mismatch: '+name)
            text = text.replace(old, new)
        result = text.encode()
        if target.exists() and sha(target.read_bytes()) not in {basis, item['result_sha256'], sha(result)}:
            raise ValueError('Refusing to overwrite unrelated local edit: '+name)
        outputs[target] = result
    for target, result in outputs.items():
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(result)
    print(json.dumps({'version':20,'materialized_text_files':len(outputs),
                      'transport_sha256':PAYLOAD_SHA256,
                      'scope':'Exact source transport; no mathematical correctness certification.'}))

if __name__ == '__main__':
    main()
