#!/usr/bin/env python3
"""Check native A2 v51 bytes, reconstructed Git source tree, and optional rebuild.

Requires PyMuPDF. No network, repository writes or mathematical certification.
The optional local-build directory must already have been separately compiled.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import re
import zipfile
import fitz


def require(ok: bool, message: str) -> None:
    if not ok:
        raise RuntimeError(message)


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def git_object(kind: str, data: bytes) -> str:
    return hashlib.sha1(kind.encode()+b' '+str(len(data)).encode()+b'\0'+data).hexdigest()


def path_at(root: Path, name: str) -> Path:
    rel=Path(name)
    require(not rel.is_absolute() and '..' not in rel.parts, 'Unsafe path: '+name)
    p=root/rel
    require(p.is_file() and not p.is_symlink(), 'Nonregular file: '+name)
    return p


def tree_id(files: dict) -> str:
    root={}
    for name,info in files.items():
        parts=Path(name).parts
        require(not Path(name).is_absolute() and '..' not in parts, 'Unsafe tree member')
        d=root
        for part in parts[:-1]:
            d=d.setdefault(part,{})
            require(isinstance(d,dict),'Conflicting tree entry')
        require(parts[-1] not in d,'Duplicate tree entry')
        require(info['mode'] in ('100644','100755'),'Unexpected source mode')
        d[parts[-1]]=(info['mode'],info['git_blob'])
    def encode(node: dict) -> str:
        entries=[]
        for name,value in node.items():
            directory=isinstance(value,dict)
            mode,oid=('40000',encode(value)) if directory else value
            key=name.encode()+ (b'/' if directory else b'')
            entries.append((key,mode.encode()+b' '+name.encode()+b'\0'+bytes.fromhex(oid)))
        return git_object('tree',b''.join(raw for _,raw in sorted(entries)))
    return encode(root)


def verify(native: Path, source: str, expected_tree: str | None,
           local: Path | None, artifact: Path | None, artifact_sha: str | None) -> dict:
    report=json.loads(path_at(native,'build-report.json').read_text())
    require(report['status']=='passed' and report['source_commit']==source,'Wrong/failed source')
    out={'source_commit':source,'source_tree':report['source_tree'],
         'mathematical_certification':False,'visual_inspection':'Not performed by this script'}
    if artifact is not None:
        require(artifact_sha is not None,'Specify expected artifact SHA-256')
        raw=artifact.read_bytes(); require(sha(raw)==artifact_sha,'Actions ZIP mismatch')
        out['actions_zip']={'bytes':len(raw),'sha256':sha(raw)}
    for name,info in report['evidence_files'].items():
        raw=path_at(native,name).read_bytes()
        require(len(raw)==info['bytes'] and sha(raw)==info['sha256'],'Evidence mismatch: '+name)
    out['build_report_evidence_files_verified']=len(report['evidence_files'])
    groups=json.loads(path_at(native,'active-source-manifest.json').read_text())
    active={n:i for group in groups.values() for n,i in group.items()}
    require(len(active)==109,'Unexpected active input count')
    with zipfile.ZipFile(path_at(native,'native-source.zip')) as z:
        manifest=json.loads(z.read('SOURCE_MANIFEST.json'))
        require(manifest['source_commit']==source,'Wrong source archive')
        require(not manifest['excluded_tracked_products'],'Excluded source needs separate tree handling')
        members=z.namelist();require(len(members)==len(set(members)),'Duplicate ZIP names')
        require(set(members)=={'SOURCE_MANIFEST.json'}|{'source/'+n for n in manifest['files']},
                'Unmanifested archive entries')
        for name,info in manifest['files'].items():
            require(not Path(name).is_absolute() and '..' not in Path(name).parts,'Unsafe member')
            require(Path(name).suffix.lower() not in ('.ttf','.otf','.pfb','.pfa','.woff','.woff2'),
                    'Standalone font in source archive')
            raw=z.read('source/'+name)
            require(len(raw)==info['bytes'] and sha(raw)==info['sha256']
                    and git_object('blob',raw)==info['git_blob'],'Frozen source mismatch: '+name)
        for name,info in active.items():
            raw=z.read('source/'+name)
            require(len(raw)==info['bytes'] and sha(raw)==info['sha256']
                    and git_object('blob',raw)==info['git_blob'],'Active source mismatch: '+name)
            if local is not None:
                require(path_at(local,name).read_bytes()==raw,'Local active source differs: '+name)
        rebuilt_tree=tree_id(manifest['files'])
        require(rebuilt_tree==manifest['source_tree']==report['source_tree'],'Source tree mismatch')
        if expected_tree:
            require(rebuilt_tree==expected_tree,'Repository-pinned tree mismatch')
        out.update({'frozen_source_files_verified':len(manifest['files']),
                    'active_inputs_verified':len(active),'reconstructed_source_tree':rebuilt_tree,
                    'externally_supplied_tree_checked':expected_tree is not None,
                    'standalone_font_files':0})
    pairs=[]
    for p in sorted(native.glob('check_*-normal.json')):
        opt=path_at(native,p.name.replace('-normal','-optimized'))
        require(p.read_bytes()==opt.read_bytes(),'Optimization mismatch: '+p.name)
        pairs.append(p.stem.removesuffix('-normal'))
    require(len(pairs)==5,'Wrong diagnostic pair count')
    out['paired_diagnostics']=pairs;out['local_build_checked']=local is not None;out['entries']={}
    for stem in ('main','two_collision'):
        raw=path_at(native,stem+'.pdf').read_bytes()
        item={'bytes':len(raw),'sha256':sha(raw),'git_blob':git_object('blob',raw)}
        with fitz.open(stream=raw,filetype='pdf') as pdf:
            item['pages']=len(pdf)
            require(len(pdf)==report['entries'][stem]['product']['pages'],'Page count mismatch')
            outside=[]
            for i,page in enumerate(pdf,1):
                for block in page.get_text('dict')['blocks']:
                    if block['type']!=0:continue
                    for line in block['lines']:
                        for span in line['spans']:
                            if not page.rect.contains(fitz.Rect(span['bbox'])):outside.append(i)
            item['outside_page_text_span_pages']=sorted(set(outside))
            if local is not None:
                with fitz.open(path_at(local,stem+'.pdf')) as copy:
                    require(len(copy)==len(pdf),'Local page count mismatch')
                    for i,(a,b) in enumerate(zip(pdf,copy),1):
                        require(a.get_text()==b.get_text(),f'{stem} text mismatch {i}')
                        pa=a.get_pixmap(matrix=fitz.Matrix(1,1),colorspace=fitz.csRGB,alpha=False)
                        pb=b.get_pixmap(matrix=fitz.Matrix(1,1),colorspace=fitz.csRGB,alpha=False)
                        require((pa.width,pa.height,pa.samples)==(pb.width,pb.height,pb.samples),
                                f'{stem} RGB raster mismatch {i}')
                    item['same_renderer_text_and_72dpi_parity_pages']=len(pdf)
                item['local_pdf_sha256']=sha(path_at(local,stem+'.pdf').read_bytes())
        out['entries'][stem]=item
    out['source_zip_sha256']=sha(path_at(native,'native-source.zip').read_bytes())
    out['status']='passed'
    return out


def main() -> None:
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--native',required=True,type=Path)
    p.add_argument('--source-commit',required=True)
    p.add_argument('--expected-tree')
    p.add_argument('--local-build',type=Path)
    p.add_argument('--artifact-zip',type=Path)
    p.add_argument('--artifact-sha256')
    p.add_argument('--output',type=Path)
    a=p.parse_args()
    result=verify(a.native,a.source_commit,a.expected_tree,a.local_build,a.artifact_zip,a.artifact_sha256)
    text=json.dumps(result,indent=2,sort_keys=True)+'\n'
    if a.output:a.output.write_text(text)
    else:print(text,end='')

if __name__=='__main__':main()
