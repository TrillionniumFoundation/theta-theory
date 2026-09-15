#!/usr/bin/env python3
"""Verify the pinned v55 native artifact; optionally compare a complete rebuild.

Only Python's standard library and PyMuPDF are used. No author module is
imported, no code is built or executed, and no network/repository write occurs.
Byte identities and render parity are not mathematical certification.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import zipfile
import fitz

SOURCE='3903f5b8a5ffb0d0a69065b1d303c247c06ebf69'
TREE='8ff45d47f7dd78bc0c0d4ae284dde147a47d87e9'
ARTIFACT_SHA='848adf607bd34ee8013827a7ab1a7d98cfe88cccfc566fc9948747b603c9a5b6'
FONT_EXT={'.ttf','.otf','.woff','.woff2','.pfb','.pfm','.pfa','.ttc'}

def require(ok: bool, message: str) -> None:
    if not ok: raise RuntimeError(message)

def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def git_hash(kind: str, data: bytes) -> str:
    return hashlib.sha1(kind.encode()+b' '+str(len(data)).encode()+b'\0'+data).hexdigest()

def relative(name: str) -> None:
    p=PurePosixPath(name)
    require(bool(name) and not p.is_absolute() and '..' not in p.parts and '\\' not in name,
            'Unsafe relative path: '+name)

def read(root: Path, name: str) -> bytes:
    relative(name);p=root/name
    require(p.resolve().is_relative_to(root.resolve()) and p.is_file() and not p.is_symlink(),
            'Not a contained regular file: '+name)
    return p.read_bytes()

def check(data: bytes, info: dict, name: str) -> None:
    require(len(data)==info['bytes'] and sha(data)==info['sha256'],'Byte identity: '+name)
    if 'git_blob' in info:
        require(git_hash('blob',data)==info['git_blob'],'Git blob identity: '+name)

def reconstruct_tree(files: dict) -> str:
    root={}
    for name,info in files.items():
        relative(name);parts=name.split('/');node=root
        for part in parts[:-1]:
            node=node.setdefault(part,{})
            require(isinstance(node,dict),'Tree path collision')
        require(parts[-1] not in node,'Tree entry collision')
        require(info['mode'] in ('100644','100755'),'Unexpected source mode')
        node[parts[-1]]=(info['mode'],info['git_blob'])
    def recurse(node):
        entries=[]
        for name,value in node.items():
            if isinstance(value,dict): mode,h,key='40000',recurse(value),name+'/'
            else: mode,h=value;key=name
            entries.append((key.encode(),mode.encode()+b' '+name.encode()+b'\0'+bytes.fromhex(h)))
        return git_hash('tree',b''.join(value for _,value in sorted(entries)))
    return recurse(root)

def verify(native: Path, local: Path | None, artifact: Path | None) -> dict:
    out={'mathematical_certification':False,'visual_review':'Not performed by this script',
         'source_commit':SOURCE,'expected_source_tree':TREE,'local_build_checked':local is not None}
    if artifact is not None:
        data=artifact.read_bytes();require(sha(data)==ARTIFACT_SHA,'Outer artifact digest')
        out['artifact']={'bytes':len(data),'sha256':sha(data)}
    report=json.loads(read(native,'build-report.json'))
    require(report['status']=='passed' and report['source_commit']==SOURCE and report['source_tree']==TREE,
            'Wrong or failed native build')
    for name,info in report['evidence_files'].items():check(read(native,name),info,name)
    out['evidence_files_verified']=len(report['evidence_files'])
    frozen=json.loads(read(native,'frozen-source-manifest.json'))
    active_groups=json.loads(read(native,'active-source-manifest.json'))
    active={name:info for group in active_groups.values() for name,info in group.items()}
    require(len(active)==111 and len(frozen['files'])==640,'Unexpected frozen/active counts')
    require(not frozen['excluded_tracked_products'],'Unexpected excluded source products')
    source_zip=read(native,'native-source.zip')
    require(sha(source_zip)==report['source_archive_sha256'],'Nested source ZIP identity')
    with zipfile.ZipFile(native/'native-source.zip') as archive:
        members=archive.namelist();require(len(members)==len(set(members)),'Duplicate ZIP entries')
        for name in members:
            relative(name)
            require(PurePosixPath(name).suffix.lower() not in FONT_EXT,'Font file distributed')
        require(json.loads(archive.read('SOURCE_MANIFEST.json'))==frozen,'Nested/frozen manifest mismatch')
        actual_names={name.removeprefix('source/') for name in members if name.startswith('source/') and not name.endswith('/')}
        require(actual_names==set(frozen['files']),'Frozen ZIP file set differs')
        for name,info in frozen['files'].items():
            data=archive.read('source/'+name);check(data,info,name)
            if name in active:
                require(info==active[name],'Active/frozen manifest disagreement: '+name)
                if local is not None: require(read(local,name)==data,'Rebuilt input mismatch: '+name)
    tree=reconstruct_tree(frozen['files']);require(tree==TREE==frozen['source_tree'],'Reconstructed source tree')
    out.update(frozen_files_verified=len(frozen['files']),active_inputs_verified=len(active),
               reconstructed_source_tree=tree,no_font_files_distributed=True,
               source_archive={'bytes':len(source_zip),'sha256':sha(source_zip),'git_blob':git_hash('blob',source_zip)})
    names=sorted(p.name.removesuffix('-normal.json') for p in native.glob('check_*-normal.json'))
    require(names==['check_adaptive','check_quantized_v46','check_revision_v32','check_revision_v38','check_revision_v55'],
            'Unexpected diagnostic families')
    for name in names:require(read(native,name+'-normal.json')==read(native,name+'-optimized.json'),'Python-mode mismatch')
    out['ordinary_optimized_pairs']=names;out['products']={}
    for stem in ('main','two_collision'):
        data=read(native,stem+'.pdf');check(data,report['entries'][stem]['product'],stem+'.pdf')
        with fitz.open(native/(stem+'.pdf')) as pdf:
            info={'pages':len(pdf),'bytes':len(data),'sha256':sha(data),'git_blob':git_hash('blob',data)}
            require(len(pdf)==report['entries'][stem]['product']['pages'],'Wrong native page count')
            outside=[]
            for number,page in enumerate(pdf,1):
                for block in page.get_text('dict')['blocks']:
                    for line in block.get('lines',[]):
                        if any(not page.rect.contains(fitz.Rect(span['bbox'])) for span in line['spans']):outside.append(number)
            info['outside_page_text_span_pages']=sorted(set(outside))
            if local is not None:
                rebuilt=read(local,stem+'.pdf');info['rebuilt_sha256']=sha(rebuilt)
                with fitz.open(local/(stem+'.pdf')) as other:
                    require(len(other)==len(pdf),'Page count mismatch')
                    for num,(a,b) in enumerate(zip(pdf,other),1):
                        require(a.get_text()==b.get_text(),f'Text mismatch {stem} {num}')
                        x=a.get_pixmap(matrix=fitz.Matrix(1,1),alpha=False)
                        y=b.get_pixmap(matrix=fitz.Matrix(1,1),alpha=False)
                        require((x.width,x.height,x.n)==(y.width,y.height,y.n) and x.samples==y.samples,
                                f'72-dpi RGB mismatch {stem} {num}')
                info['text_and_same_renderer_72dpi_parity_pages']=len(pdf)
            out['products'][stem]=info
    out['renderer_version']=list(fitz.version);out['status']='passed'
    return out

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--native',required=True,type=Path)
    parser.add_argument('--local-build',type=Path)
    parser.add_argument('--artifact-zip',type=Path)
    parser.add_argument('--output',type=Path)
    args=parser.parse_args()
    result=json.dumps(verify(args.native,args.local_build,args.artifact_zip),indent=2,sort_keys=True)+'\n'
    if args.output:args.output.write_text(result)
    else:print(result,end='')
