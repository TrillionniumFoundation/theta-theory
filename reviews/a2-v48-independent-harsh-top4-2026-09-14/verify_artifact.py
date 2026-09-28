#!/usr/bin/env python3
"""Verify the pinned A2 v48 artifact and optionally a separate complete rebuild.

Usage:
  python verify_artifact.py --native-root NATIVE --source-root SOURCE \
      --local-build SOURCE > ARTIFACT_AUDIT.json

NATIVE contains main.pdf, native-source.zip and the native manifests.
SOURCE is the source/ directory extracted from native-source.zip.
--local-build points to a directory where BOTH complete entries were rebuilt.
Requires PyMuPDF. Does not compile, use a network, or write to the repository.
Raster parity is an automated same-renderer check, not human proof review.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import re
from typing import Any
import fitz

PIN='fe21046e47a89ec3b3df8493f4d885b087e3ad7f'


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def verify_file(path: Path, spec: dict[str, Any]) -> None:
    require(path.is_file(), f'Missing file: {path}')
    data=path.read_bytes()
    require(len(data)==spec['bytes'], f'Byte count: {path}')
    require(hashlib.sha256(data).hexdigest()==spec['sha256'], f'SHA256: {path}')
    if 'git_blob' in spec:
        blob=hashlib.sha1(f'blob {len(data)}\0'.encode()+data).hexdigest()
        require(blob==spec['git_blob'], f'Git blob: {path}')


def main() -> None:
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--native-root',type=Path,required=True)
    parser.add_argument('--source-root',type=Path,required=True)
    parser.add_argument('--local-build',type=Path)
    args=parser.parse_args()
    native,source=args.native_root,args.source_root
    build=json.loads((native/'build-report.json').read_text())
    require(build['source_commit']==PIN,'Wrong mathematical source snapshot')
    require(sha256(native/'native-source.zip')==build['source_archive_sha256'],'Source ZIP hash')
    manifest=json.loads((native/'active-source-manifest.json').read_text())
    inputs={}
    for entry_files in manifest.values():
        for name,spec in entry_files.items():
            if name in inputs: require(inputs[name]==spec,f'Conflicting active input: {name}')
            inputs[name]=spec
            verify_file(source/name,spec)
    require(len(inputs)==105,'Unexpected active-input count')
    for name,spec in build['evidence_files'].items(): verify_file(native/name,spec)
    result={'source_commit':PIN,'status':'pass','active_source_files_verified':len(inputs),
            'active_source_sha256_and_git_blobs_verified':True,
            'native_evidence_files_verified':len(build['evidence_files']),
            'native_source_zip_sha256':sha256(native/'native-source.zip'),
            'active_manifest_sha256':sha256(native/'active-source-manifest.json'),
            'scope':'Content identity and optional automated same-renderer build parity; no mathematical certification and no human full-page inspection claim.',
            'pdfs':{}}
    for name in ('main','two_collision'):
        path=native/(name+'.pdf')
        spec=build['entries'][name]['product']
        verify_file(path,spec)
        with fitz.open(path) as original:
            require(len(original)==spec['pages'],f'Native page count: {name}')
            info={'native_bytes':path.stat().st_size,'native_pages':len(original),'native_sha256':sha256(path)}
            if args.local_build:
                localpath=args.local_build/(name+'.pdf')
                with fitz.open(localpath) as local:
                    require(len(original)==len(local),f'Rebuild page count: {name}')
                    text_bad=[];pixel_bad=[]
                    for i in range(len(original)):
                        if original[i].get_text()!=local[i].get_text():text_bad.append(i+1)
                        a=original[i].get_pixmap(dpi=100,alpha=False)
                        b=local[i].get_pixmap(dpi=100,alpha=False)
                        if (a.width,a.height,a.samples)!=(b.width,b.height,b.samples):pixel_bad.append(i+1)
                    require(not text_bad,f'Rebuild text difference: {name}, {text_bad}')
                    require(not pixel_bad,f'Rebuild raster difference: {name}, {pixel_bad}')
                    log=(args.local_build/(name+'.log')).read_text(errors='replace')
                    info.update({'local_pages':len(local),'local_sha256':sha256(localpath),
                        'byte_identical_pdf':path.read_bytes()==localpath.read_bytes(),
                        'text_different_pages':text_bad,'raster_different_pages_100_dpi':pixel_bad,
                        'local_final_log_underfull':len(re.findall(r'Underfull \\[hv]box',log)),
                        'local_final_log_overfull':len(re.findall(r'Overfull \\[hv]box',log)),
                        'local_final_log_undefined_or_error':bool(re.search(r'undefined references|undefined citations|multiply defined|^!',log,re.M))})
            result['pdfs'][name]=info
    print(json.dumps(result,indent=2,sort_keys=True))


if __name__=='__main__':
    main()
