#!/usr/bin/env python3
"""Verify frozen v60 source/evidence and optional three-entry rebuild parity.

No manuscript code is imported. Requires PyMuPDF. This verifies identities
and same-renderer parity, not mathematical truth or visual presentation.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import zipfile
import fitz


def require(value: bool, message: str) -> None:
    if not value:
        raise RuntimeError(message)


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def git_hash(kind: str, data: bytes) -> str:
    return hashlib.sha1(kind.encode()+b' '+str(len(data)).encode()+b'\0'+data).hexdigest()


def member(name: str) -> None:
    p=PurePosixPath(name)
    require(bool(name) and not p.is_absolute() and '..' not in p.parts
            and '\\' not in name, 'Unsafe path: '+name)


def regular(root: Path, name: str) -> Path:
    member(name)
    p=root/name
    require(p.is_file() and not p.is_symlink(), 'Nonregular file: '+name)
    require(p.resolve().is_relative_to(root.resolve()), 'Escaping path: '+name)
    return p


def match(data: bytes, info: dict, name: str) -> None:
    require(len(data)==info['bytes'] and sha256(data)==info['sha256'], 'Byte identity: '+name)
    if 'git_blob' in info:
        require(git_hash('blob',data)==info['git_blob'], 'Git blob: '+name)


def tree_hash(files: dict) -> str:
    root={}
    for name, info in files.items():
        member(name); node=root; parts=PurePosixPath(name).parts
        for part in parts[:-1]: node=node.setdefault(part,{})
        node[parts[-1]]=(info['mode'],info['git_blob'])
    def visit(node: dict) -> str:
        data=b''
        for name,item in sorted(node.items(),key=lambda kv:(kv[0]+('/' if isinstance(kv[1],dict) else '')).encode()):
            mode,oid=('40000',visit(item)) if isinstance(item,dict) else item
            data+=mode.encode()+b' '+name.encode()+b'\0'+bytes.fromhex(oid)
        return git_hash('tree',data)
    return visit(root)


def verify(args: argparse.Namespace) -> dict:
    n=args.native
    report=json.loads(regular(n,'build-report.json').read_text())
    frozen=json.loads(regular(n,'frozen-source-manifest.json').read_text())
    active_manifest=json.loads(regular(n,'active-source-manifest.json').read_text())
    active={name:info for group in active_manifest.values() for name,info in group.items()}
    require(report['status']=='passed' and not report['errors'],'Failed native report')
    for record in (report,frozen):
        require(record['source_commit']==args.source_commit and record['source_tree']==args.source_tree,
                'Unexpected pinned source identity')
    require(len(active)==123,'Unexpected active input union')
    for name,info in report['evidence_files'].items(): match(regular(n,name).read_bytes(),info,name)
    archive_path=regular(n,'native-source.zip')
    require(sha256(archive_path.read_bytes())==report['source_archive_sha256'],'Source archive digest')
    with zipfile.ZipFile(archive_path) as archive:
        names=archive.namelist(); require(len(names)==len(set(names)),'Duplicate archive name')
        for name in names: member(name)
        require(json.loads(archive.read('SOURCE_MANIFEST.json'))==frozen,'Nested manifest mismatch')
        for name,info in frozen['files'].items():
            member(name)
            require(info['mode'] in ('100644','100755'),'Unsupported frozen file mode')
            require(Path(name).suffix.lower() not in ('.ttf','.otf','.woff','.woff2','.pfb','.pfa'),
                    'Standalone font in archive: '+name)
            match(archive.read('source/'+name),info,name)
        for name,info in active.items():
            data=archive.read('source/'+name); match(data,info,name)
            if args.rebuild:
                require(regular(args.rebuild,name).read_bytes()==data,'Rebuild input differs: '+name)
    reconstructed=tree_hash(frozen['files'])
    require(reconstructed==args.source_tree,'Reconstructed source tree differs')
    pairs=[]
    for p in sorted(n.glob('check_*-normal.json')):
        require(p.read_bytes()==regular(n,p.name.replace('-normal','-optimized')).read_bytes(),
                'Python mode mismatch: '+p.name)
        pairs.append(p.stem.removesuffix('-normal'))
    require(len(pairs)==5,'Expected five paired diagnostics')
    out={'status':'passed','source_commit':args.source_commit,'source_tree':args.source_tree,
         'reconstructed_source_tree':reconstructed,'frozen_files_verified':len(frozen['files']),
         'active_inputs_verified':len(active),'entry_active_counts':{k:len(v) for k,v in active_manifest.items()},
         'evidence_files_verified':len(report['evidence_files']),'ordinary_optimized_pairs':pairs,
         'mathematical_certification':False,'visual_inspection':'Not performed by this script',
         'entries':{}}
    if args.artifact:
        require(args.artifact_sha256 is not None,'Supply the independently obtained artifact digest')
        data=args.artifact.read_bytes();require(sha256(data)==args.artifact_sha256,'Outer artifact digest')
        out['artifact']={'bytes':len(data),'sha256':sha256(data)}
    for stem in ('rigidity','main','two_collision'):
        path=regular(n,stem+'.pdf');data=path.read_bytes()
        match(data,report['entries'][stem]['product'],stem+'.pdf')
        with fitz.open(path) as native:
            require(len(native)==report['entries'][stem]['product']['pages'],'Native page count')
            info={'pages':len(native),'bytes':len(data),'sha256':sha256(data),'git_blob':git_hash('blob',data)}
            outside=[]
            for number,page in enumerate(native,1):
                for block in page.get_text('dict')['blocks']:
                    if block['type']!=0:continue
                    for line in block['lines']:
                        for span in line['spans']:
                            if not page.rect.contains(fitz.Rect(span['bbox'])):outside.append(number)
            info['outside_page_text_span_pages']=sorted(set(outside))
            if args.rebuild:
                localpath=regular(args.rebuild,stem+'.pdf')
                with fitz.open(localpath) as rebuilt:
                    require(len(rebuilt)==len(native),'Rebuild page count')
                    for number,(a,b) in enumerate(zip(native,rebuilt),1):
                        require(a.get_text()==b.get_text(),f'Text mismatch: {stem} p{number}')
                        aa=a.get_pixmap(matrix=fitz.Matrix(1,1),alpha=False)
                        bb=b.get_pixmap(matrix=fitz.Matrix(1,1),alpha=False)
                        require((aa.width,aa.height,aa.samples)==(bb.width,bb.height,bb.samples),
                                f'RGB mismatch: {stem} p{number}')
                info.update(rebuilt_sha256=sha256(localpath.read_bytes()),
                            same_renderer_text_and_72dpi_pixel_parity_pages=len(native),
                            pdf_byte_identical=data==localpath.read_bytes())
            out['entries'][stem]=info
    return out


def main() -> None:
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--native',type=Path,required=True)
    p.add_argument('--source-commit',required=True)
    p.add_argument('--source-tree',required=True)
    p.add_argument('--artifact',type=Path)
    p.add_argument('--artifact-sha256')
    p.add_argument('--rebuild',type=Path)
    p.add_argument('--output',type=Path)
    args=p.parse_args(); result=json.dumps(verify(args),indent=2,sort_keys=True)+'\n'
    if args.output:args.output.write_text(result)
    else:print(result,end='')

if __name__=='__main__':main()
