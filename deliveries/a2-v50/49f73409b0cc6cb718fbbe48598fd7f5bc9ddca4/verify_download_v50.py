#!/usr/bin/env python3
"""Verify the v50 native evidence, frozen source and optional local-build parity.

Requires PyMuPDF. Performs no network or repository writes. The optional output
is an operational report, not a mathematical or individual visual certificate.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import zipfile
import fitz

SOURCE='49f73409b0cc6cb718fbbe48598fd7f5bc9ddca4'


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def blob(data: bytes) -> str:
    return hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()


def relative(name: str) -> Path:
    path=Path(name)
    require(bool(name) and not path.is_absolute() and '..' not in path.parts
            and '\\' not in name and '\0' not in name, 'Unsafe relative name: '+repr(name))
    return path


def regular(root: Path, name: str) -> Path:
    root=root.resolve();path=root/relative(name)
    require(path.is_file() and not path.is_symlink() and path.resolve().is_relative_to(root),
            'Missing or unsafe regular file: '+name)
    return path


def check_bytes(data: bytes, info: dict, name: str) -> None:
    require(len(data)==info['bytes'] and digest(data)==info['sha256'],
            'Size/SHA-256 mismatch: '+name)
    if 'git_blob' in info:
        require(blob(data)==info['git_blob'], 'Git blob mismatch: '+name)


def verify(native: Path, local: Path | None, artifact: Path | None,
           artifact_sha256: str | None) -> dict:
    report=json.loads(regular(native,'build-report.json').read_text())
    require(report['status']=='passed' and report['source_commit']==SOURCE,
            'Wrong source or unsuccessful native build')
    require(not report['errors'], 'Native build has recorded errors')
    for name,info in report['evidence_files'].items():
        check_bytes(regular(native,name).read_bytes(),info,name)
    frozen=json.loads(regular(native,'frozen-source-manifest.json').read_text())
    require(frozen['source_commit']==SOURCE and frozen['source_tree']==report['source_tree'],
            'Frozen-source identity mismatch')
    grouped=json.loads(regular(native,'active-source-manifest.json').read_text())
    active={name:info for group in grouped.values() for name,info in group.items()}
    require(len(active)==107, 'Unexpected active graph size')
    archive_path=regular(native,'native-source.zip')
    require(digest(archive_path.read_bytes())==report['source_archive_sha256'],
            'Wrong source archive digest')
    with zipfile.ZipFile(archive_path) as archive:
        names=archive.namelist()
        expected={'SOURCE_MANIFEST.json'}|{'source/'+n for n in frozen['files']}
        require(len(names)==len(set(names)) and set(names)==expected,
                'Missing, repeated or unexpected archive member')
        require(json.loads(archive.read('SOURCE_MANIFEST.json'))==frozen,
                'Embedded and external frozen manifests differ')
        for name,info in frozen['files'].items():
            relative(name)
            require(Path(name).suffix.lower() not in {'.ttf','.otf','.woff','.woff2','.pfb','.pfa'},
                    'Font file must not be distributed: '+name)
            check_bytes(archive.read('source/'+name),info,name)
        for name,info in active.items():
            data=archive.read('source/'+name)
            check_bytes(data,info,'active/'+name)
            require(name in frozen['files'], 'Active source absent from frozen manifest')
            if local is not None:
                require(regular(local,name).read_bytes()==data,
                        'Local build input differs: '+name)
    paired=[]
    for normal in sorted(native.glob('check_*-normal.json')):
        optimized=regular(native,normal.name.replace('-normal','-optimized'))
        require(normal.read_bytes()==optimized.read_bytes(), 'Ordinary/optimized output differs')
        paired.append(normal.stem.removesuffix('-normal'))
    require(paired==['check_adaptive','check_quantized_v46','check_revision_v32',
                     'check_revision_v38','check_revision_v50'], 'Wrong dual-mode diagnostic set')
    result={'status':'passed','source_commit':SOURCE,'source_tree':report['source_tree'],
        'build_report_evidence_files_verified':len(report['evidence_files']),
        'frozen_source_files_verified':len(frozen['files']),
        'active_source_inputs_verified':len(active),'ordinary_optimized_parity':paired,
        'local_build_checked':local is not None,'entries':{},'mathematical_certification':False,
        'visual_inspection':'Not performed by this script'}
    if artifact is not None:
        data=artifact.read_bytes()
        require(artifact_sha256 is not None and digest(data)==artifact_sha256,
                'Actions archive digest differs from supplied GitHub artifact digest')
        result['actions_archive']={'bytes':len(data),'sha256':digest(data)}
    for stem in ('main','two_collision'):
        path=regular(native,stem+'.pdf');data=path.read_bytes()
        check_bytes(data,report['entries'][stem]['product'],stem+'.pdf')
        with fitz.open(path) as document:
            require(len(document)==report['entries'][stem]['product']['pages'],
                    'Native page count mismatch')
            outside=set()
            for number,page in enumerate(document,1):
                for block in page.get_text('dict')['blocks']:
                    if block['type']!=0:
                        continue
                    for line in block['lines']:
                        for span in line['spans']:
                            if not page.rect.contains(fitz.Rect(span['bbox'])):
                                outside.add(number)
            require(not outside, 'Extracted text span outside page: '+stem+' '+str(outside))
            entry={'pages':len(document),'bytes':len(data),'sha256':digest(data),
                'git_blob':blob(data),'outside_page_text_span_pages':sorted(outside),
                'native_layout_warnings':report['entries'][stem]['warnings']}
            if local is not None:
                local_path=regular(local,stem+'.pdf')
                with fitz.open(local_path) as counterpart:
                    require(len(document)==len(counterpart),'Local page count mismatch')
                    for number,(a,b) in enumerate(zip(document,counterpart),1):
                        require(a.get_text()==b.get_text(),f'{stem}: local text differs at page {number}')
                        pa=a.get_pixmap(matrix=fitz.Matrix(1,1),alpha=False)
                        pb=b.get_pixmap(matrix=fitz.Matrix(1,1),alpha=False)
                        require((pa.width,pa.height,pa.n,pa.samples)==(pb.width,pb.height,pb.n,pb.samples),
                                f'{stem}: local 72-dpi RGB pixels differ at page {number}')
                    entry['same_renderer_text_and_72dpi_pixel_parity_pages']=len(document)
                entry['local_pdf_sha256']=digest(local_path.read_bytes())
                entry['pdf_byte_identity']=data==local_path.read_bytes()
            result['entries'][stem]=entry
    return result


def main() -> None:
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--native',required=True,type=Path)
    parser.add_argument('--local-build',type=Path)
    parser.add_argument('--artifact-zip',type=Path)
    parser.add_argument('--artifact-sha256')
    parser.add_argument('--output',type=Path)
    args=parser.parse_args()
    text=json.dumps(verify(args.native,args.local_build,args.artifact_zip,args.artifact_sha256),
                    sort_keys=True,indent=2)+'\n'
    if args.output:
        args.output.write_text(text)
    else:
        print(text,end='')

if __name__=='__main__':
    main()
