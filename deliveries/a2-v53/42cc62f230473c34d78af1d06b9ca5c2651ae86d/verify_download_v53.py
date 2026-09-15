#!/usr/bin/env python3
"""Read-only v53 source/evidence verifier and optional complete-PDF parity check.

Requires PyMuPDF. Does not compile, execute manuscript code, perform a visual
inspection, access the network or certify mathematical statements.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import zipfile
import fitz

SOURCE = '42cc62f230473c34d78af1d06b9ca5c2651ae86d'
FONT_SUFFIXES = {'.ttf','.otf','.woff','.woff2','.pfb','.pfa','.ttc'}

def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)

def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def git_object(kind: str, data: bytes) -> str:
    return hashlib.sha1(kind.encode()+b' '+str(len(data)).encode()+b'\0'+data).hexdigest()

def member(name: str) -> None:
    p=PurePosixPath(name)
    require(not p.is_absolute() and '..' not in p.parts and '\\' not in name,
            'Unsafe path: '+name)

def regular(root: Path, name: str) -> Path:
    member(name)
    p=root/name
    require(p.is_file() and not p.is_symlink(), 'Missing/nonregular file: '+name)
    return p

def check_bytes(raw: bytes, info: dict, name: str) -> None:
    require(len(raw)==info['bytes'] and sha256(raw)==info['sha256'],
            'Byte identity failed: '+name)
    if 'git_blob' in info:
        require(git_object('blob',raw)==info['git_blob'], 'Git blob failed: '+name)

def source_tree(files: dict) -> str:
    root={}
    for name,info in files.items():
        member(name)
        parts=PurePosixPath(name).parts
        current=root
        for part in parts[:-1]:
            current=current.setdefault(part,{})
        require(parts[-1] not in current,'Duplicate source path')
        current[parts[-1]]=(info['mode'],info['git_blob'])
    def digest(node: dict) -> str:
        records=[]
        for name,value in node.items():
            if isinstance(value,dict):
                records.append((name+'/',b'40000 '+name.encode()+b'\0'+bytes.fromhex(digest(value))))
            else:
                mode,blob=value
                require(mode in ('100644','100755'),'Unexpected source mode')
                records.append((name,mode.encode()+b' '+name.encode()+b'\0'+bytes.fromhex(blob)))
        payload=b''.join(raw for _,raw in sorted(records,key=lambda x:x[0].encode()))
        return git_object('tree',payload)
    return digest(root)

def verify(native: Path, local: Path | None, artifact: Path | None,
           artifact_sha: str | None) -> dict:
    report=json.loads(regular(native,'build-report.json').read_text())
    require(report['status']=='passed' and report['source_commit']==SOURCE,'Wrong native source/status')
    frozen=json.loads(regular(native,'frozen-source-manifest.json').read_text())
    require(frozen['source_commit']==SOURCE,'Wrong frozen source')
    for name,info in report['evidence_files'].items():
        check_bytes(regular(native,name).read_bytes(),info,name)
    active_groups=json.loads(regular(native,'active-source-manifest.json').read_text())
    active={name:info for group in active_groups.values() for name,info in group.items()}
    require(len(active)==111,'Unexpected active input count')
    with zipfile.ZipFile(regular(native,'native-source.zip')) as archive:
        names=archive.namelist()
        require(len(names)==len(set(names)),'Duplicate ZIP member')
        for name in names:
            member(name)
            require(PurePosixPath(name).suffix.lower() not in FONT_SUFFIXES,'Distributed font file')
        archived={n.removeprefix('source/') for n in names if n.startswith('source/') and not n.endswith('/')}
        require(archived==set(frozen['files']),'Archive/source manifest membership differs')
        for name,info in frozen['files'].items():
            check_bytes(archive.read('source/'+name),info,name)
        for name,info in active.items():
            raw=archive.read('source/'+name)
            check_bytes(raw,info,name)
            if local is not None:
                require(regular(local,name).read_bytes()==raw,'Local active source mismatch: '+name)
    tree=source_tree(frozen['files'])
    require(tree==frozen['source_tree']==report['source_tree'],'Reconstructed source tree differs')
    modes=[]
    for path in sorted(native.glob('check_*-normal.json')):
        optimized=regular(native,path.name.replace('-normal','-optimized'))
        require(path.read_bytes()==optimized.read_bytes(),'Python mode mismatch: '+path.name)
        modes.append(path.stem.removesuffix('-normal'))
    require(len(modes)==5,'Wrong paired-diagnostic count')
    result={'source_commit':SOURCE,'source_tree':tree,'repository_tree':report['repository_tree'],
        'frozen_source_files_verified':len(frozen['files']),'active_inputs_verified':len(active),
        'evidence_files_verified':len(report['evidence_files']),'diagnostic_mode_parity':modes,
        'no_distributed_font_files':True,'local_build_checked':local is not None,
        'visual_inspection':'Not performed by this script','mathematical_certification':False,'entries':{}}
    if artifact is not None:
        require(artifact_sha is not None,'Expected artifact hash required')
        raw=artifact.read_bytes();require(sha256(raw)==artifact_sha,'Actions artifact digest differs')
        result['actions_artifact']={'bytes':len(raw),'sha256':sha256(raw)}
    for stem in ('main','two_collision'):
        raw=regular(native,stem+'.pdf').read_bytes()
        info={'bytes':len(raw),'sha256':sha256(raw),'git_blob':git_object('blob',raw)}
        with fitz.open(native/(stem+'.pdf')) as pdf:
            info['pages']=len(pdf)
            require(len(pdf)==report['entries'][stem]['product']['pages'],'Wrong native page count')
            outside=[]
            for i,page in enumerate(pdf,1):
                for block in page.get_text('dict')['blocks']:
                    if block['type']!=0:continue
                    for line in block['lines']:
                        for span in line['spans']:
                            if not page.rect.contains(fitz.Rect(span['bbox'])):outside.append(i)
            info['outside_page_text_span_pages']=sorted(set(outside))
            if local is not None:
                localpath=regular(local,stem+'.pdf')
                info['local_pdf_sha256']=sha256(localpath.read_bytes())
                with fitz.open(localpath) as other:
                    require(len(other)==len(pdf),'Different local page count')
                    for i,(a,b) in enumerate(zip(pdf,other),1):
                        require(a.get_text()==b.get_text(),f'{stem} text differs on p{i}')
                        pa=a.get_pixmap(matrix=fitz.Matrix(1,1),alpha=False)
                        pb=b.get_pixmap(matrix=fitz.Matrix(1,1),alpha=False)
                        require((pa.width,pa.height,pa.n,pa.samples)==(pb.width,pb.height,pb.n,pb.samples),
                                f'{stem} 72-dpi RGB differs on p{i}')
                    info['text_and_72dpi_pixel_parity_pages']=len(pdf)
                log=regular(local,stem+'.log').read_text(errors='replace')
                info['local_warnings']=re.findall(r'.*(?:Warning:|Underfull \\[hv]box|Overfull \\[hv]box).*',log)
                info['local_log_sha256']=sha256(regular(local,stem+'.log').read_bytes())
                require(not re.search(r'undefined references|undefined citations|(?:Reference|Citation) `.{0,250}?undefined|Missing character:|multiply[- ]defined', ''.join(log.splitlines()),re.I), 'Unresolved native input/reference/glyph')
        result['entries'][stem]=info
    result['status']='passed'
    return result

def main() -> None:
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--native',type=Path,required=True)
    parser.add_argument('--local-build',type=Path)
    parser.add_argument('--artifact-zip',type=Path)
    parser.add_argument('--artifact-sha256')
    args=parser.parse_args()
    print(json.dumps(verify(args.native,args.local_build,args.artifact_zip,args.artifact_sha256),
                     indent=2,sort_keys=True))

if __name__=='__main__':
    main()
