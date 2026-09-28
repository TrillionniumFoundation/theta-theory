#!/usr/bin/env python3
"""Verify frozen v59 source/products and optionally all-page rebuild parity.

No author checking code is imported. Requires PyMuPDF for PDF inspection.
Performs no network access, compilation, or repository writes.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import zipfile
import fitz


def require(test: bool, message: str) -> None:
    if not test:
        raise RuntimeError(message)


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def obj(kind: str, data: bytes) -> str:
    return hashlib.sha1(kind.encode()+b' '+str(len(data)).encode()+b'\0'+data).hexdigest()


def checked_name(name: str) -> str:
    p=PurePosixPath(name)
    require(not p.is_absolute() and '..' not in p.parts and str(p)==name,
            'Unsafe manifest path: '+name)
    return name


def read(root: Path, name: str) -> bytes:
    path=root/checked_name(name)
    require(path.is_file() and not path.is_symlink(),'Missing/nonregular file: '+name)
    return path.read_bytes()


def verify_bytes(data: bytes, info: dict, name: str) -> None:
    require(len(data)==info['bytes'] and sha(data)==info['sha256'],'Byte/digest mismatch: '+name)
    if 'git_blob' in info:
        require(obj('blob',data)==info['git_blob'],'Git blob mismatch: '+name)


def tree_hash(files: dict) -> str:
    root={}
    for name,info in files.items():
        parts=PurePosixPath(checked_name(name)).parts; at=root
        for part in parts[:-1]:
            at=at.setdefault(part,{})
            require(isinstance(at,dict),'File/directory collision')
        require(parts[-1] not in at,'Duplicate tree path')
        require(info['mode'] in ('100644','100755'),'Unexpected source mode')
        at[parts[-1]]=(info['mode'],info['git_blob'])
    def visit(node):
        entries=[]
        for name,value in node.items():
            directory=isinstance(value,dict)
            mode,identity=('40000',visit(value)) if directory else value
            entries.append((name.encode()+(b'/' if directory else b''),
                mode.encode()+b' '+name.encode()+b'\0'+bytes.fromhex(identity)))
        return obj('tree',b''.join(data for _,data in sorted(entries)))
    return visit(root)


def verify(native: Path, source: str, source_tree: str,
           rebuild: Path | None, artifact: Path | None, artifact_sha: str | None) -> dict:
    report=json.loads(read(native,'build-report.json'))
    require(report['status']=='passed' and report['source_commit']==source,'Wrong/failed build')
    frozen=json.loads(read(native,'frozen-source-manifest.json'))
    require(frozen['source_commit']==source and frozen['source_tree']==source_tree
            and report['source_tree']==source_tree,'Source identity disagreement')
    require(not frozen['excluded_tracked_products'],'Cannot reconstruct an incomplete source tree')
    if artifact is not None:
        require(artifact_sha is not None and sha(artifact.read_bytes())==artifact_sha,
                'Outer artifact digest differs')
    for name,info in report['evidence_files'].items():
        verify_bytes(read(native,name),info,name)
    with zipfile.ZipFile(native/'native-source.zip') as z:
        require(json.loads(z.read('SOURCE_MANIFEST.json'))==frozen,'Nested manifest differs')
        require(set(z.namelist())=={'SOURCE_MANIFEST.json'}|{'source/'+n for n in frozen['files']},
                'Unmanifested or missing ZIP member')
        require(len(z.namelist())==len(set(z.namelist())),'Duplicate archive member')
        for name,info in frozen['files'].items():
            checked_name(name)
            require(PurePosixPath(name).suffix.lower() not in ('.ttf','.otf','.woff','.woff2','.pfb','.pfa'),
                    'Standalone font file: '+name)
            data=z.read('source/'+name);verify_bytes(data,info,name)
            if rebuild is not None:
                require(read(rebuild,name)==data,'Rebuild source differs: '+name)
    reconstructed=tree_hash(frozen['files'])
    require(reconstructed==source_tree,'Reconstructed Git subtree differs')
    active=json.loads(read(native,'active-source-manifest.json'))
    union={name:info for group in active.values() for name,info in group.items()}
    require(len(union)==122,'Unexpected active union')
    for name,info in union.items():
        ref=frozen['files'][name]
        require(all(info[k]==ref[k] for k in ('bytes','sha256','git_blob')),'Active identity: '+name)
    pairs=[]
    for n in sorted(native.glob('check_*-normal.json')):
        require(n.read_bytes()==read(native,n.name.replace('-normal','-optimized')),'Python mode mismatch')
        pairs.append(n.stem.removesuffix('-normal'))
    require(len(pairs)==5,'Expected five diagnostic pairs')
    out={'status':'passed','source_commit':source,'source_tree':source_tree,
        'reconstructed_source_tree':reconstructed,'frozen_files_verified':len(frozen['files']),
        'active_sources_verified':len(union),'entry_active_counts':{k:len(v) for k,v in active.items()},
        'evidence_files_verified':len(report['evidence_files']),'ordinary_optimized_pairs':pairs,
        'mathematical_certification':False,'visual_inspection':'Not performed by this script',
        'standalone_font_files':False,'rebuild_checked':rebuild is not None,'entries':{}}
    if artifact is not None:
        out['outer_artifact']={'bytes':artifact.stat().st_size,'sha256':artifact_sha}
    for stem in ('rigidity','main','two_collision'):
        data=read(native,stem+'.pdf');verify_bytes(data,report['entries'][stem]['product'],stem+'.pdf')
        with fitz.open(native/(stem+'.pdf')) as doc:
            info={'pages':len(doc),'bytes':len(data),'sha256':sha(data),'git_blob':obj('blob',data)}
            require(len(doc)==report['entries'][stem]['product']['pages'],'Page count differs')
            outside=[]
            for n,page in enumerate(doc,1):
                for block in page.get_text('dict')['blocks']:
                    if block['type']!=0: continue
                    for line in block['lines']:
                        if any(not page.rect.contains(fitz.Rect(s['bbox'])) for s in line['spans']):
                            outside.append(n)
            info['outside_page_text_span_pages']=sorted(set(outside))
            if rebuild is not None:
                other=read(rebuild,stem+'.pdf')
                with fitz.open(rebuild/(stem+'.pdf')) as local:
                    require(len(local)==len(doc),'Rebuild page count differs')
                    for n,(a,b) in enumerate(zip(doc,local),1):
                        require(a.get_text()==b.get_text(),f'{stem} text differs p{n}')
                        ap=a.get_pixmap(matrix=fitz.Matrix(1,1),alpha=False)
                        bp=b.get_pixmap(matrix=fitz.Matrix(1,1),alpha=False)
                        require((ap.width,ap.height,ap.samples)==(bp.width,bp.height,bp.samples),
                                f'{stem} raster differs p{n}')
                info.update(rebuilt_sha256=sha(other),byte_identical=other==data,
                            text_and_same_renderer_72dpi_parity_pages=len(doc))
            out['entries'][stem]=info
    return out


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--native',required=True,type=Path)
    p.add_argument('--source-commit',required=True)
    p.add_argument('--source-tree',required=True)
    p.add_argument('--rebuild',type=Path)
    p.add_argument('--artifact',type=Path)
    p.add_argument('--artifact-sha256')
    a=p.parse_args()
    print(json.dumps(verify(a.native,a.source_commit,a.source_tree,a.rebuild,a.artifact,a.artifact_sha256),
                     indent=2,sort_keys=True))

if __name__=='__main__':main()
