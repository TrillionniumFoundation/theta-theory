#!/usr/bin/env python3
"""Verify frozen source bytes, the Git tree and all-page native/rebuild parity.

Requires PyMuPDF. No author checking code is imported. This script performs
no compilation, network request, visual inspection or mathematical certification.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import zipfile
import fitz


def require(ok: bool, message: str) -> None:
    if not ok:
        raise RuntimeError(message)


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def git_hash(kind: str, data: bytes) -> str:
    return hashlib.sha1(kind.encode()+b' '+str(len(data)).encode()+b'\0'+data).hexdigest()


def path_check(name: str) -> None:
    require(not Path(name).is_absolute() and '..' not in Path(name).parts, 'Unsafe path: '+name)


def read(root: Path, name: str) -> bytes:
    path_check(name)
    f=root/name
    require(f.is_file() and not f.is_symlink(), 'Missing/nonregular file: '+name)
    return f.read_bytes()


def tree_hash(files: dict) -> str:
    root={}
    for name, info in files.items():
        path_check(name)
        node=root
        parts=Path(name).parts
        for part in parts[:-1]:
            node=node.setdefault(part,{})
        node[parts[-1]]=(info['mode'],info['git_blob'])
    def visit(node: dict) -> str:
        chunks=[]
        for name,value in sorted(node.items(),key=lambda kv:(kv[0]+('/' if isinstance(kv[1],dict) else '')).encode()):
            mode,h=('40000',visit(value)) if isinstance(value,dict) else value
            require(mode in ('40000','100644','100755'), 'Unsupported source mode')
            chunks.append(mode.encode()+b' '+name.encode()+b'\0'+bytes.fromhex(h))
        return git_hash('tree',b''.join(chunks))
    return visit(root)


def verify(args) -> dict:
    native=args.native
    report=json.loads(read(native,'build-report.json'))
    frozen=json.loads(read(native,'frozen-source-manifest.json'))
    active=json.loads(read(native,'active-source-manifest.json'))
    require(report['status']=='passed' and report['source_commit']==args.source_commit,'Wrong native source/build')
    require(report['source_tree']==args.source_tree,'Wrong declared tree')
    require(not frozen['excluded_tracked_products'],'Reconstruction expects the complete source tree')
    for name,info in report['evidence_files'].items():
        data=read(native,name)
        require(len(data)==info['bytes'] and sha(data)==info['sha256'],'Native evidence mismatch: '+name)
    sourcezip=read(native,'native-source.zip')
    require(sha(sourcezip)==report['source_archive_sha256'],'Wrong source archive')
    with zipfile.ZipFile(native/'native-source.zip') as z:
        require(json.loads(z.read('SOURCE_MANIFEST.json'))==frozen,'Nested manifest differs')
        expected={'SOURCE_MANIFEST.json'}|{'source/'+n for n in frozen['files']}
        require(set(z.namelist())==expected and len(z.namelist())==len(expected),'Unexpected/duplicate source member')
        for name,info in frozen['files'].items():
            path_check(name)
            require(Path(name).suffix.lower() not in {'.ttf','.otf','.woff','.woff2','.pfb','.pfa'},'Standalone font file')
            data=z.read('source/'+name)
            require(len(data)==info['bytes'] and sha(data)==info['sha256'] and git_hash('blob',data)==info['git_blob'],'Frozen source mismatch: '+name)
            if args.rebuild:
                require(read(args.rebuild,name)==data,'Rebuild source differs: '+name)
    actual_tree=tree_hash(frozen['files'])
    require(actual_tree==args.source_tree,'Reconstructed Git tree differs')
    union={n:i for group in active.values() for n,i in group.items()}
    require(len(union)==121,'Unexpected v58 active union')
    for name,info in union.items():
        fi=frozen['files'][name]
        require(all(info[k]==fi[k] for k in ('bytes','sha256','git_blob')),'Active identity differs')
        if args.preflight:
            require(sha(read(args.preflight,name))==info['sha256'],'Preflight active source differs')
    pairs=[]
    for normal in sorted(native.glob('check_*-normal.json')):
        require(normal.read_bytes()==read(native,normal.name.replace('-normal','-optimized')),'Python modes differ')
        pairs.append(normal.stem.removesuffix('-normal'))
    require(len(pairs)==5,'Expected five paired diagnostic families')
    out={'status':'passed','source_commit':args.source_commit,'source_tree':actual_tree,
         'frozen_source_files':len(frozen['files']),'active_union':len(union),
         'entry_source_counts':{k:len(v) for k,v in active.items()},
         'evidence_files':len(report['evidence_files']),'paired_diagnostics':pairs,
         'standalone_fonts':False,'mathematical_certification':False,
         'visual_inspection':'Not performed by this script','entries':{}}
    if args.artifact:
        digest=sha(args.artifact.read_bytes())
        require(args.artifact_sha256 and digest==args.artifact_sha256,'Wrong outer artifact digest')
        out['artifact_sha256']=digest
    for stem in ('rigidity','main','two_collision'):
        data=read(native,stem+'.pdf')
        with fitz.open(native/(stem+'.pdf')) as doc:
            info={'pages':len(doc),'bytes':len(data),'sha256':sha(data),'git_blob':git_hash('blob',data)}
            require(all(info[k]==report['entries'][stem]['product'][k] for k in ('pages','bytes','sha256')),'Product differs from report')
            outside=[]
            for n,page in enumerate(doc,1):
                for block in page.get_text('dict')['blocks']:
                    for line in block.get('lines',[]):
                        for span in line['spans']:
                            if not page.rect.contains(fitz.Rect(span['bbox'])):outside.append(n)
            info['outside_page_text_span_pages']=sorted(set(outside))
            for tag,root in (('rebuild',args.rebuild),('preflight',args.preflight)):
                if not root:continue
                other_data=read(root,stem+'.pdf')
                with fitz.open(root/(stem+'.pdf')) as other:
                    require(len(other)==len(doc),'Different page counts')
                    for n,(a,b) in enumerate(zip(doc,other),1):
                        require(a.get_text()==b.get_text(),f'{stem} {tag} text differs p{n}')
                        x,y=a.get_pixmap(matrix=fitz.Matrix(1,1),alpha=False),b.get_pixmap(matrix=fitz.Matrix(1,1),alpha=False)
                        require((x.width,x.height,x.samples)==(y.width,y.height,y.samples),f'{stem} {tag} pixels differ p{n}')
                info[tag]={'text_and_72dpi_rgb_equal_pages':len(doc),'sha256':sha(other_data),'byte_identical':data==other_data}
            out['entries'][stem]=info
    return out


def main() -> None:
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--native',required=True,type=Path)
    p.add_argument('--source-commit',required=True)
    p.add_argument('--source-tree',required=True)
    p.add_argument('--rebuild',type=Path)
    p.add_argument('--preflight',type=Path)
    p.add_argument('--artifact',type=Path)
    p.add_argument('--artifact-sha256')
    p.add_argument('--output',type=Path)
    args=p.parse_args()
    text=json.dumps(verify(args),sort_keys=True,indent=2)+'\n'
    if args.output:args.output.write_text(text)
    else:print(text,end='')

if __name__=='__main__':main()
