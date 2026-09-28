#!/usr/bin/env python3
"""Independent native-source, Git-tree, and optional rebuild comparison.
Usage: python verify_artifact.py AUDIT_DIRECTORY
AUDIT_DIRECTORY contains native/, source/source/, source/SOURCE_MANIFEST.json,
and optionally rebuild/. No manuscript checker is imported. No proof is certified.
"""
from __future__ import annotations
import hashlib, json, re, sys
from pathlib import Path


def check(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def git_id(kind: str, data: bytes) -> str:
    return hashlib.sha1(kind.encode()+b' '+str(len(data)).encode()+b'\0'+data).hexdigest()


def tree_id(files: dict) -> str:
    root: dict = {}
    for name, entry in files.items():
        node = root
        parts = name.split('/')
        for part in parts[:-1]:
            node = node.setdefault(part, {})
        node[parts[-1]] = (entry['mode'], entry['git_blob'])
    def recurse(node: dict) -> str:
        data = bytearray()
        for name, value in sorted(node.items(), key=lambda kv: (kv[0]+('/' if isinstance(kv[1],dict) else '')).encode()):
            mode, sha = ('40000', recurse(value)) if isinstance(value,dict) else value
            data.extend(mode.encode()+b' '+name.encode()+b'\0'+bytes.fromhex(sha))
        return git_id('tree', bytes(data))
    return recurse(root)


def main(root: Path) -> dict:
    native = root/'native'; src = root/'source/source'
    manifest = json.loads((root/'source/SOURCE_MANIFEST.json').read_text())
    check(manifest == json.loads((native/'frozen-source-manifest.json').read_text()), 'Frozen manifests disagree')
    for name, item in manifest['files'].items():
        data = (src/name).read_bytes()
        check(len(data) == item['bytes'], f'Byte count: {name}')
        check(hashlib.sha256(data).hexdigest() == item['sha256'], f'SHA256: {name}')
        check(git_id('blob',data) == item['git_blob'], f'Git blob: {name}')
    tree = tree_id(manifest['files'])
    check(tree == manifest['source_tree'], 'Reconstructed source tree mismatch')
    active = json.loads((native/'active-source-manifest.json').read_text())
    union = set()
    for entry, group in active.items():
        for name, item in group.items():
            check(item == manifest['files'][name], f'Active identity: {entry}/{name}')
        union.update(group)
    report = json.loads((native/'build-report.json').read_text())
    for name, item in report['evidence_files'].items():
        data = (native/name).read_bytes()
        check(len(data) == item['bytes'] and hashlib.sha256(data).hexdigest() == item['sha256'], f'Evidence mismatch: {name}')
    result = {'source_commit':manifest['source_commit'], 'source_tree':tree,
              'frozen_source_files':len(manifest['files']),
              'active_entry_counts':{e:len(g) for e,g in active.items()},
              'active_union':len(union), 'verified_native_evidence_entries':len(report['evidence_files']),
              'mathematical_certification':False, 'rebuilds':{}}
    try:
        import fitz
    except ImportError:
        result['rebuild_comparison']='not run: PyMuPDF unavailable'
        return result
    for entry in ('two_collision','main','rigidity'):
        a = native/(entry+'.pdf'); b = root/'rebuild'/(entry+'.pdf')
        if not b.exists():
            result['rebuilds'][entry]={'status':'not supplied'}
            continue
        A=fitz.open(a); B=fitz.open(b)
        check(len(A)==len(B), 'Rebuilt page count: '+entry)
        texts=[]; renders=[]
        for i in range(len(A)):
            if A[i].get_text()!=B[i].get_text(): texts.append(i+1)
            pa=A[i].get_pixmap(matrix=fitz.Matrix(1,1),colorspace=fitz.csRGB,alpha=False)
            pb=B[i].get_pixmap(matrix=fitz.Matrix(1,1),colorspace=fitz.csRGB,alpha=False)
            if (pa.width,pa.height,pa.samples)!=(pb.width,pb.height,pb.samples): renders.append(i+1)
        log=(root/'rebuild'/(entry+'.log')).read_text(errors='replace')
        warnings = [line for line in log.splitlines() if re.search(r'Underfull|Overfull|undefined|Missing character|^!|LaTeX Error',line)]
        result['rebuilds'][entry]={'pages':len(A), 'native_sha256':hashlib.sha256(a.read_bytes()).hexdigest(),
            'rebuilt_sha256':hashlib.sha256(b.read_bytes()).hexdigest(), 'byte_identical':a.read_bytes()==b.read_bytes(),
            'text_mismatch_pages':texts, 'rgb_72dpi_mismatch_pages':renders, 'log_matches':warnings}
    result['render_comparison']='All-page same-renderer 72-dpi RGB comparison, not all-page visual reading'
    return result

if __name__=='__main__':
    if len(sys.argv)!=2:
        raise SystemExit('Usage: python verify_artifact.py AUDIT_DIRECTORY')
    print(json.dumps(main(Path(sys.argv[1]).resolve()),indent=2,sort_keys=True))
