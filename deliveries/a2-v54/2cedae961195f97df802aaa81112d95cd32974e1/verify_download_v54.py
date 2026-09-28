#!/usr/bin/env python3
"""Verify a v54 native artifact, source tree and optional full local rebuild.

Requires PyMuPDF. No network, build, author-code execution or repository writes
are performed. Hash and renderer comparisons are not mathematical certificates.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import zipfile
import fitz

SOURCE = '2cedae961195f97df802aaa81112d95cd32974e1'
SOURCE_TREE = '407b278984b14e57468e727fb56b0fa4163a7207'
ARTIFACT_SHA256 = 'd7572bce8b3a9131685f9a76cab47b381e60bf99aaf9c7dd4adf0444e5419610'
FONTS = {'.ttf','.otf','.woff','.woff2','.pfa','.pfb','.ttc'}


def require(ok: bool, message: str) -> None:
    if not ok:
        raise RuntimeError(message)


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def git_id(kind: str, data: bytes) -> str:
    return hashlib.sha1(kind.encode()+b' '+str(len(data)).encode()+b'\0'+data).hexdigest()


def safe_name(name: str) -> None:
    require(bool(name) and not Path(name).is_absolute() and '..' not in Path(name).parts,
            'Unsafe path: '+name)


def regular(root: Path, name: str) -> Path:
    safe_name(name)
    path=root/name
    require(path.is_file() and not path.is_symlink(), 'Nonregular input: '+name)
    require(path.resolve().is_relative_to(root.resolve()),'Path escapes root: '+name)
    return path


def check_identity(data: bytes, info: dict, name: str) -> None:
    require(len(data)==info['bytes'] and sha256(data)==info['sha256'], 'Digest: '+name)
    if 'git_blob' in info:
        require(git_id('blob',data)==info['git_blob'], 'Git blob: '+name)


def tree_identity(files: dict) -> str:
    nested={}
    for name,info in files.items():
        safe_name(name)
        parts=Path(name).parts; node=nested
        for part in parts[:-1]:
            node=node.setdefault(part,{})
        require(parts[-1] not in node,'Duplicate tree member: '+name)
        require(info['mode'] in ('100644','100755'),'Unsupported file mode: '+name)
        node[parts[-1]]=(info['mode'],info['git_blob'])
    def tree(node: dict) -> str:
        entries=[]
        for name,value in node.items():
            isdir=isinstance(value,dict)
            mode,oid=('40000',tree(value)) if isdir else value
            sortkey=name.encode()+ (b'/' if isdir else b'')
            payload=mode.encode()+b' '+name.encode()+b'\0'+bytes.fromhex(oid)
            entries.append((sortkey,payload))
        return git_id('tree',b''.join(v for _,v in sorted(entries)))
    return tree(nested)


def verify(native: Path, local_build: Path | None, artifact: Path | None) -> dict:
    report=json.loads(regular(native,'build-report.json').read_text())
    frozen=json.loads(regular(native,'frozen-source-manifest.json').read_text())
    active_groups=json.loads(regular(native,'active-source-manifest.json').read_text())
    require(report['status']=='passed' and report['source_commit']==SOURCE,'Wrong/failed native build')
    require(report['source_tree']==SOURCE_TREE and frozen['source_tree']==SOURCE_TREE,
            'Unexpected source tree')
    require(not frozen.get('excluded_tracked_products'), 'Cannot reconstruct a partial source tree')
    result={'source_commit':SOURCE,'source_tree':SOURCE_TREE,'mathematical_certification':False,
            'visual_inspection':'Not performed by this script','local_build_checked':local_build is not None}
    if artifact is not None:
        raw=artifact.read_bytes()
        require(sha256(raw)==ARTIFACT_SHA256, 'Actions artifact digest')
        result['artifact']={'bytes':len(raw),'sha256':sha256(raw)}
    for name,info in report['evidence_files'].items():
        check_identity(regular(native,name).read_bytes(),info,name)
    result['build_report_evidence_files_verified']=len(report['evidence_files'])
    active={n:i for group in active_groups.values() for n,i in group.items()}
    require(len(active)==111,'Unexpected active graph')
    archive_path=regular(native,'native-source.zip')
    require(sha256(archive_path.read_bytes())==report['source_archive_sha256'],'Source archive digest')
    with zipfile.ZipFile(archive_path) as archive:
        names=[n for n in archive.namelist() if not n.endswith('/')]
        require(len(names)==len(set(names)),'Duplicate archive members')
        require(set(names)==({'source/'+n for n in frozen['files']}|{'SOURCE_MANIFEST.json'}),'Unexpected archive file set')
        require(json.loads(archive.read('SOURCE_MANIFEST.json'))==frozen,'Nested manifest differs')
        for name,info in frozen['files'].items():
            safe_name(name)
            require(Path(name).suffix.lower() not in FONTS,'Font file must not be distributed')
            check_identity(archive.read('source/'+name),info,name)
        for name,info in active.items():
            raw=archive.read('source/'+name);check_identity(raw,info,name)
            if local_build is not None:
                require(regular(local_build,name).read_bytes()==raw,'Local active source differs: '+name)
    require(tree_identity(frozen['files'])==SOURCE_TREE,'Reconstructed source tree mismatch')
    result.update({'frozen_source_files_verified':len(frozen['files']),
                   'archived_active_inputs_verified':len(active),
                   'reconstructed_source_tree':SOURCE_TREE,'distributed_font_files':[]})
    pairs=[]
    for normal in sorted(native.glob('check_*-normal.json')):
        optimized=regular(native,normal.name.replace('-normal','-optimized'))
        require(normal.read_bytes()==optimized.read_bytes(),'Python-mode mismatch: '+normal.name)
        pairs.append(normal.stem.removesuffix('-normal'))
    require(len(pairs)==5,'Expected five diagnostic families')
    result['ordinary_optimized_parity']=pairs
    result['entries']={}
    for stem in ('main','two_collision'):
        path=regular(native,stem+'.pdf'); raw=path.read_bytes()
        check_identity(raw,report['entries'][stem]['product'],stem)
        with fitz.open(path) as doc:
            require(len(doc)==report['entries'][stem]['product']['pages'],'Wrong page count')
            info={'bytes':len(raw),'sha256':sha256(raw),'git_blob':git_id('blob',raw),
                  'pages':len(doc),'warnings':report['entries'][stem]['warnings']}
            outside=[]
            for number,page in enumerate(doc,1):
                for block in page.get_text('dict')['blocks']:
                    if block['type']!=0:continue
                    for line in block['lines']:
                        for span in line['spans']:
                            if not page.rect.contains(fitz.Rect(span['bbox'])):outside.append(number)
            info['outside_page_text_span_pages']=sorted(set(outside))
            if local_build is not None:
                other=regular(local_build,stem+'.pdf')
                info['local_pdf_sha256']=sha256(other.read_bytes())
                with fitz.open(other) as local:
                    require(len(local)==len(doc),'Local page count')
                    for number,(a,b) in enumerate(zip(doc,local),1):
                        require(a.get_text()==b.get_text(),f'{stem} text p{number}')
                        x=a.get_pixmap(matrix=fitz.Matrix(1,1),alpha=False)
                        y=b.get_pixmap(matrix=fitz.Matrix(1,1),alpha=False)
                        require((x.width,x.height,x.n,x.samples)==(y.width,y.height,y.n,y.samples),
                                f'{stem} 72-dpi RGB p{number}')
                info['same_renderer_text_and_72dpi_pixel_parity_pages']=len(doc)
            result['entries'][stem]=info
    result['status']='passed'
    return result


def main() -> None:
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--native',type=Path,required=True)
    parser.add_argument('--local-build',type=Path)
    parser.add_argument('--artifact-zip',type=Path)
    parser.add_argument('--output',type=Path)
    args=parser.parse_args()
    text=json.dumps(verify(args.native,args.local_build,args.artifact_zip),indent=2,sort_keys=True)+'\n'
    if args.output:args.output.write_text(text)
    else:print(text,end='')

if __name__=='__main__':
    main()
