#!/usr/bin/env python3
"""Independent hash/tree/build comparison for the downloaded A2 v55 artifact.
Usage: python verify_delivery.py NATIVE_DIR SOURCE_DIR REBUILD_DIR
No network access. The native directory must be the extracted workflow artifact;
the source directory is the 'source' child extracted from native-source.zip.
"""
from __future__ import annotations
import hashlib,json,sys
from pathlib import Path
import fitz

def require(ok:bool, msg:str)->None:
    if not ok: raise RuntimeError(msg)
def digest(data:bytes, kind:str='sha256')->str:
    return hashlib.new(kind,data).hexdigest()
def git_hash(data:bytes, kind:str)->str:
    return digest(f'{kind} {len(data)}\0'.encode()+data,'sha1')
def main()->dict:
    native,source,rebuild=map(Path,sys.argv[1:4])
    manifest=json.loads((native/'frozen-source-manifest.json').read_text())
    tree={}
    for name,meta in manifest['files'].items():
        data=(source/name).read_bytes()
        require(len(data)==meta['bytes'],f'size {name}')
        require(digest(data)==meta['sha256'],f'sha256 {name}')
        require(git_hash(data,'blob')==meta['git_blob'],f'git blob {name}')
        ptr=tree
        parts=name.split('/')
        for part in parts[:-1]: ptr=ptr.setdefault(part,{})
        ptr[parts[-1]]=(meta['mode'],meta['git_blob'])
    def tree_hash(node:dict)->str:
        entries=[]
        for name,value in node.items():
            isdir=isinstance(value,dict)
            mode,sha=('40000',tree_hash(value)) if isdir else value
            entries.append((name+('/' if isdir else ''),mode.encode()+b' '+name.encode()+b'\0'+bytes.fromhex(sha)))
        return git_hash(b''.join(v for _,v in sorted(entries)),'tree')
    subtree=tree_hash(tree)
    require(subtree==manifest['source_tree'],'source subtree mismatch')
    active=json.loads((native/'active-source-manifest.json').read_text())
    active_names=set()
    for entry,files in active.items():
        for name,meta in files.items():
            require(digest((source/name).read_bytes())==meta['sha256'],f'active {name}')
            active_names.add(name)
    report=json.loads((native/'build-report.json').read_text())
    verified=[]
    for name,meta in report['evidence_files'].items():
        data=(native/name).read_bytes()
        require(digest(data)==meta['sha256'],f'evidence hash {name}')
        require(len(data)==meta['bytes'],f'evidence size {name}')
        verified.append(name)
    rebuilt={}
    for stem in ('main','two_collision'):
        a=fitz.open(native/f'{stem}.pdf'); b=fitz.open(rebuild/f'{stem}.pdf')
        require(len(a)==len(b),f'page count {stem}')
        text_equal=[];pixel_equal=[]
        for i in range(len(a)):
            text_equal.append(a[i].get_text()==b[i].get_text())
            ap=a[i].get_pixmap(matrix=fitz.Matrix(1,1),colorspace=fitz.csRGB,alpha=False)
            bp=b[i].get_pixmap(matrix=fitz.Matrix(1,1),colorspace=fitz.csRGB,alpha=False)
            pixel_equal.append(ap.width==bp.width and ap.height==bp.height and ap.samples==bp.samples)
        log=(rebuild/f'{stem}.log').read_text(errors='replace')
        warnings=[line for line in log.splitlines() if 'Underfull' in line or 'Overfull' in line or 'LaTeX Warning:' in line or 'Missing character' in line]
        rebuilt[stem]={'pages':len(a),'native_sha256':digest((native/f'{stem}.pdf').read_bytes()),'rebuilt_sha256':digest((rebuild/f'{stem}.pdf').read_bytes()),'same_extracted_text_pages':sum(text_equal),'same_72dpi_RGB_pages':sum(pixel_equal),'warnings':warnings}
        require(all(text_equal),f'text difference {stem}')
        require(all(pixel_equal),f'render difference {stem}')
    return {'status':'passed','source_commit':manifest['source_commit'],'source_subtree':subtree,'frozen_files_verified':len(manifest['files']),'active_files_verified':len(active_names),'native_evidence_files_verified':len(verified),'pdf_comparison':rebuilt,'renderer':fitz.VersionBind,'scope':'Independent local integrity and complete native rebuild comparison; not a theorem certificate. Visual inspection is separate; pixel equality is not a claim of PDF byte equality.'}
if __name__=='__main__':
    print(json.dumps(main(),indent=2,sort_keys=True))
