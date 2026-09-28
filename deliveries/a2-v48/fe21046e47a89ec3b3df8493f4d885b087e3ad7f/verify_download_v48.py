#!/usr/bin/env python3
"""Verify a downloaded v48 native evidence directory and optional local-build parity.

Requires PyMuPDF. This checks bytes, source snapshots and rendered parity;
it does not perform a human visual review or certify mathematical statements.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import zipfile
import fitz

SOURCE = 'fe21046e47a89ec3b3df8493f4d885b087e3ad7f'

def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)

def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def blob(data: bytes) -> str:
    return hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()

def safe(root: Path, name: str) -> Path:
    path=root/name
    require(not Path(name).is_absolute() and '..' not in Path(name).parts,
            'Unsafe manifest path: '+name)
    require(path.is_file() and not path.is_symlink(), 'Nonregular file: '+name)
    return path

def verify(evidence: Path, local_build: Path | None) -> dict:
    report=json.loads(safe(evidence,'build-report.json').read_text())
    require(report['status']=='passed' and report['source_commit']==SOURCE,
            'Wrong or failed native source build')
    for name, info in report['evidence_files'].items():
        data=safe(evidence,name).read_bytes()
        require(len(data)==info['bytes'] and digest(data)==info['sha256'],
                'Evidence mismatch: '+name)
    manifest=json.loads(safe(evidence,'active-source-manifest.json').read_text())
    active={name:info for entry in manifest.values() for name,info in entry.items()}
    require(len(active)==105, 'Unexpected active source count')
    with zipfile.ZipFile(safe(evidence,'native-source.zip')) as archive:
        for name,info in active.items():
            require(not Path(name).is_absolute() and '..' not in Path(name).parts,
                    'Unsafe archive member')
            data=archive.read('source/'+name)
            require(len(data)==info['bytes'] and digest(data)==info['sha256']
                    and blob(data)==info['git_blob'], 'Archived source: '+name)
            if local_build is not None:
                require(safe(local_build,name).read_bytes()==data,
                        'Local build source differs: '+name)
    parity=[]
    for normal in sorted(evidence.glob('check_*-normal.json')):
        optimized=safe(evidence,normal.name.replace('-normal','-optimized'))
        require(normal.read_bytes()==optimized.read_bytes(), 'Python mode mismatch')
        parity.append(normal.stem.removesuffix('-normal'))
    require(len(parity)==5, 'Expected five dual-mode diagnostic families')
    out={'source_commit':SOURCE,'source_tree':report['source_tree'],
         'build_report_evidence_files_verified':len(report['evidence_files']),
         'archived_active_inputs_verified':len(active),'ordinary_optimized_parity':parity,
         'mathematical_certification':False,'visual_inspection':'Not performed by this script',
         'local_build_checked':local_build is not None,'entries':{}}
    for stem in ('main','two_collision'):
        path=safe(evidence,stem+'.pdf'); data=path.read_bytes()
        with fitz.open(path) as native:
            info={'pages':len(native),'bytes':len(data),'sha256':digest(data),
                  'git_blob':blob(data),'outside_page_text_span_pages':[]}
            require(len(native)==report['entries'][stem]['product']['pages'],
                    'Native page count differs from build report')
            outside=[]
            for number,page in enumerate(native,1):
                for block in page.get_text('dict')['blocks']:
                    if block['type']!=0:
                        continue
                    for line in block['lines']:
                        for span in line['spans']:
                            if not page.rect.contains(fitz.Rect(span['bbox'])):
                                outside.append(number)
            info['outside_page_text_span_pages']=sorted(set(outside))
            if local_build is not None:
                with fitz.open(safe(local_build,stem+'.pdf')) as local:
                    require(len(native)==len(local),'Local page count mismatch')
                    for number,(a,b) in enumerate(zip(native,local),1):
                        require(a.get_text()==b.get_text(),f'{stem} text mismatch p{number}')
                        require(a.get_pixmap(matrix=fitz.Matrix(1,1),alpha=False).samples
                                ==b.get_pixmap(matrix=fitz.Matrix(1,1),alpha=False).samples,
                                f'{stem} 72-dpi raster mismatch p{number}')
                    info['same_renderer_text_and_72dpi_pixel_parity_pages']=len(native)
            out['entries'][stem]=info
    out['status']='passed'
    return out

def main() -> None:
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--evidence',required=True,type=Path)
    parser.add_argument('--local-build',type=Path)
    parser.add_argument('--output',type=Path)
    args=parser.parse_args()
    result=json.dumps(verify(args.evidence,args.local_build),sort_keys=True,indent=2)+'\n'
    if args.output:
        args.output.write_text(result)
    else:
        print(result,end='')

if __name__=='__main__':
    main()
