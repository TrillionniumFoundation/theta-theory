#!/usr/bin/env python3
"""Verify an extracted A2-v53 artifact and independently rebuilt PDFs.

Usage: python verify_delivery.py --artifact a2-v53-native-artifact.zip \
  --native native --source source/source --rebuild rebuild --output result.json
Requires PyMuPDF. Does not download, build, or execute manuscript code.
Source identity and rendering agreement are not mathematical certificates.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import fitz

EXPECTED_ARCHIVE = '288117d5b31d61ad65e8ab2b62ad3de805a059a3d5629c144a4bc38978391638'
EXPECTED_COMMIT = '42cc62f230473c34d78af1d06b9ca5c2651ae86d'
EXPECTED_TREE = '6153e28c29bd54c2d45f6466d3c3c3bf6dd09942'

def require(ok: bool, message: str) -> None:
    if not ok:
        raise RuntimeError(message)

def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def git_object(kind: str, data: bytes) -> str:
    return hashlib.sha1(kind.encode()+b' '+str(len(data)).encode()+b'\0'+data).hexdigest()

def tree_id(tree: dict) -> str:
    entries = []
    for name, value in tree.items():
        mode, sha = ('40000', tree_id(value)) if isinstance(value,dict) else value
        key = (name+('/' if mode == '40000' else '')).encode()
        entry = mode.encode()+b' '+name.encode()+b'\0'+bytes.fromhex(sha)
        entries.append((key,entry))
    return git_object('tree',b''.join(v for _,v in sorted(entries)))

def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ['artifact','native','source','rebuild','output']:
        parser.add_argument('--'+name, required=True, type=Path)
    args = parser.parse_args()
    archive_sha = sha256(args.artifact.read_bytes())
    require(archive_sha == EXPECTED_ARCHIVE, 'Artifact digest differs from pinned GitHub digest')
    manifest = json.loads((args.native/'frozen-source-manifest.json').read_text())
    require(manifest['source_commit'] == EXPECTED_COMMIT, 'Wrong compiled source')
    tree = {}
    for path, info in manifest['files'].items():
        target = (args.source/path).resolve()
        require(target.is_relative_to(args.source.resolve()), 'Unsafe manifest path')
        data = target.read_bytes()
        require(len(data) == info['bytes'] and sha256(data) == info['sha256']
                and git_object('blob',data) == info['git_blob'], 'Source mismatch: '+path)
        node = tree
        for part in path.split('/')[:-1]:
            node = node.setdefault(part,{})
        node[path.split('/')[-1]] = (info['mode'],info['git_blob'])
    reconstructed = tree_id(tree)
    require(reconstructed == manifest['source_tree'] == EXPECTED_TREE, 'Source tree mismatch')
    active = json.loads((args.native/'active-source-manifest.json').read_text())
    files = {n:v for group in active.values() for n,v in group.items()}
    for path, info in files.items():
        require(info == manifest['files'][path], 'Active input mismatch: '+path)
    build = json.loads((args.native/'build-report.json').read_text())
    for path, info in build['evidence_files'].items():
        target = (args.native/path).resolve()
        require(target.is_relative_to(args.native.resolve()), 'Unsafe evidence path')
        data = target.read_bytes()
        require(len(data) == info['bytes'] and sha256(data) == info['sha256'],
                'Native evidence mismatch: '+path)
    comparisons = {}
    for name in ['main','two_collision']:
        left, right = args.native/(name+'.pdf'), args.rebuild/(name+'.pdf')
        with fitz.open(left) as a, fitz.open(right) as b:
            require(len(a) == len(b), 'Different page counts: '+name)
            text_bad, pixel_bad = [], []
            for number,(p,q) in enumerate(zip(a,b),1):
                if p.get_text() != q.get_text():
                    text_bad.append(number)
                x = p.get_pixmap(matrix=fitz.Matrix(1,1), colorspace=fitz.csRGB, alpha=False)
                y = q.get_pixmap(matrix=fitz.Matrix(1,1), colorspace=fitz.csRGB, alpha=False)
                if (x.width,x.height,x.samples) != (y.width,y.height,y.samples):
                    pixel_bad.append(number)
            log = (args.rebuild/(name+'.log')).read_text(errors='replace')
            comparisons[name] = {'pages':len(a),'native_sha256':sha256(left.read_bytes()),
                'rebuild_sha256':sha256(right.read_bytes()),'text_mismatch_pages':text_bad,
                'same_renderer_72dpi_rgb_mismatch_pages':pixel_bad,
                'warning_lines':[line for line in log.splitlines() if any(token in line for token in
                    ['Underfull','Overfull','undefined','LaTeX Warning','Missing character'])]}
    result = {'artifact_id':10380075042,'artifact_sha256':archive_sha,
        'compiled_source':EXPECTED_COMMIT,'reconstructed_source_tree':reconstructed,
        'verified_frozen_files':len(manifest['files']),'verified_unique_active_inputs':len(files),
        'verified_native_evidence_files':len(build['evidence_files']),'rebuilds':comparisons,
        'pdf_byte_identity_claimed':False,'pixel_comparison_is_not_proof_check':True}
    args.output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
    require(all(not v['text_mismatch_pages'] and not v['same_renderer_72dpi_rgb_mismatch_pages']
                for v in comparisons.values()), 'PDF text/render comparison failed; see output')

if __name__ == '__main__':
    main()
