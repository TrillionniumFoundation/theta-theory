#!/usr/bin/env python3
"""Verify the complete v52 artifact and optional separately built PDF parity.

Requires PyMuPDF. No network or repository writes. This program checks source
and product identities; it neither visually inspects pages nor certifies proofs.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import zipfile
import fitz

SOURCE='9fd0c14c7b3fd816bdb9d7c3db0fdbae2104dcd6'
FONT_SUFFIXES={'.ttf','.otf','.pfb','.pfa','.woff','.woff2','.ttc'}

def require(ok: bool, message: str) -> None:
    if not ok:
        raise RuntimeError(message)

def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def object_id(kind: str, data: bytes) -> str:
    return hashlib.sha1(kind.encode()+b' '+str(len(data)).encode()+b'\0'+data).hexdigest()

def safe_name(name: str) -> str:
    p=PurePosixPath(name)
    require(bool(name) and not p.is_absolute() and '..' not in p.parts and '\\' not in name,
            'Unsafe manifest path: '+name)
    return p.as_posix()

def read(root: Path, name: str) -> bytes:
    path=root/safe_name(name)
    require(path.is_file() and not path.is_symlink(),'Not a regular file: '+name)
    return path.read_bytes()

def check_bytes(data: bytes, info: dict, name: str, git: bool=False) -> None:
    require(len(data)==info['bytes'] and sha256(data)==info['sha256'],'Byte mismatch: '+name)
    if git:
        require(object_id('blob',data)==info['git_blob'],'Git blob mismatch: '+name)

def tree_id(files: dict) -> str:
    root={}
    for name,info in files.items():
        parts=PurePosixPath(safe_name(name)).parts
        node=root
        for component in parts[:-1]:
            node=node.setdefault(component,{})
        require(parts[-1] not in node,'Duplicate source tree path')
        require(info['mode'] in ('100644','100755'),'Unexpected source mode')
        node[parts[-1]]=(info['mode'],info['git_blob'])
    def rec(node: dict) -> str:
        body=b''
        for name,item in sorted(node.items(),key=lambda kv:(kv[0]+('/' if isinstance(kv[1],dict) else '')).encode()):
            mode,oid=('40000',rec(item)) if isinstance(item,dict) else item
            body+=mode.encode()+b' '+name.encode()+b'\0'+bytes.fromhex(oid)
        return object_id('tree',body)
    return rec(root)

def verify(native: Path, local_build: Path|None, artifact: Path|None, artifact_sha: str|None) -> dict:
    report=json.loads(read(native,'build-report.json'))
    require(report['status']=='passed' and report['source_commit']==SOURCE,'Wrong/failed native build')
    for name,info in report['evidence_files'].items():
        check_bytes(read(native,name),info,name)
    frozen=json.loads(read(native,'frozen-source-manifest.json'))
    require(frozen['source_commit']==SOURCE and frozen['source_tree']==report['source_tree'],
            'Frozen source identity mismatch')
    require(not frozen['excluded_tracked_products'],'Tree reconstruction requires an unexcluded source subtree')
    groups=json.loads(read(native,'active-source-manifest.json'))
    active={n:v for group in groups.values() for n,v in group.items()}
    require(len(active)==110,'Unexpected active input count')
    archive_bytes=read(native,'native-source.zip')
    require(sha256(archive_bytes)==report['source_archive_sha256'],'Source ZIP hash mismatch')
    with zipfile.ZipFile(native/'native-source.zip') as archive:
        names=[n for n in archive.namelist() if not n.endswith('/')]
        require(len(names)==len(set(names)),'Duplicate ZIP members')
        require(set(names)=={'source/'+n for n in frozen['files']}|{'SOURCE_MANIFEST.json'},
                'Unexpected or missing source ZIP member')
        require(json.loads(archive.read('SOURCE_MANIFEST.json'))==frozen,'Embedded source manifest differs')
        for name,info in frozen['files'].items():
            safe_name(name)
            require(PurePosixPath(name).suffix.lower() not in FONT_SUFFIXES,'Standalone font distribution')
            data=archive.read('source/'+name)
            check_bytes(data,info,name,git=True)
            if name in active:
                check_bytes(data,active[name],name,git=True)
                if local_build is not None:
                    require(read(local_build,name)==data,'Local active source mismatch: '+name)
        require(set(active)<=set(frozen['files']),'Missing active source record')
    reconstructed=tree_id(frozen['files'])
    require(reconstructed==report['source_tree'],'Reconstructed Git subtree mismatch')
    pairs=[]
    for normal in sorted(native.glob('check_*-normal.json')):
        require(normal.read_bytes()==read(native,normal.name.replace('-normal','-optimized')),
                'Python mode mismatch: '+normal.name)
        pairs.append(normal.stem.removesuffix('-normal'))
    require(len(pairs)==5,'Expected five paired diagnostic families')
    result={'source_commit':SOURCE,'source_tree':report['source_tree'],
        'reconstructed_source_tree':reconstructed,'frozen_source_files_verified':len(frozen['files']),
        'active_inputs_verified':len(active),'build_report_evidence_files_verified':len(report['evidence_files']),
        'ordinary_optimized_pairs':pairs,'standalone_font_files_distributed':False,
        'local_build_checked':local_build is not None,'mathematical_certification':False,
        'visual_inspection':'Not performed by this script','entries':{}}
    if artifact is not None:
        require(artifact_sha is not None,'Supply the independently fetched artifact digest')
        data=artifact.read_bytes()
        require(sha256(data)==artifact_sha,'Actions archive digest mismatch')
        result['actions_archive']={'bytes':len(data),'sha256':sha256(data)}
    for stem in ('main','two_collision'):
        data=read(native,stem+'.pdf')
        check_bytes(data,report['entries'][stem]['product'],stem+'.pdf')
        with fitz.open(native/(stem+'.pdf')) as pdf:
            require(len(pdf)==report['entries'][stem]['product']['pages'],'Wrong PDF page count')
            outside=[]
            for number,page in enumerate(pdf,1):
                for block in page.get_text('dict')['blocks']:
                    if block['type']!=0:continue
                    for line in block['lines']:
                        for span in line['spans']:
                            if not page.rect.contains(fitz.Rect(span['bbox'])):outside.append(number)
            info={'pages':len(pdf),'bytes':len(data),'sha256':sha256(data),'git_blob':object_id('blob',data),
                  'outside_page_text_span_pages':sorted(set(outside))}
            if local_build is not None:
                with fitz.open(local_build/(stem+'.pdf')) as other:
                    require(len(other)==len(pdf),'Rebuild page count mismatch')
                    for number,(a,b) in enumerate(zip(pdf,other),1):
                        require(a.get_text()==b.get_text(),f'{stem}: text mismatch on page {number}')
                        pa=a.get_pixmap(matrix=fitz.Matrix(1,1),alpha=False)
                        pb=b.get_pixmap(matrix=fitz.Matrix(1,1),alpha=False)
                        require((pa.width,pa.height,pa.n,pa.samples)==(pb.width,pb.height,pb.n,pb.samples),
                                f'{stem}: RGB mismatch on page {number}')
                info['same_renderer_text_and_72dpi_rgb_parity_pages']=len(pdf)
            result['entries'][stem]=info
    result['status']='passed'
    return result

def main() -> None:
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--native',required=True,type=Path)
    p.add_argument('--local-build',type=Path)
    p.add_argument('--artifact-zip',type=Path)
    p.add_argument('--artifact-sha256')
    p.add_argument('--output',type=Path)
    args=p.parse_args()
    result=json.dumps(verify(args.native,args.local_build,args.artifact_zip,args.artifact_sha256),
                      sort_keys=True,indent=2)+'\n'
    if args.output:args.output.write_text(result)
    else:print(result,end='')

if __name__=='__main__':main()
