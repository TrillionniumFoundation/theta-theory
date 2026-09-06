#!/usr/bin/env python3
"""Materialize a complete, source-anchored v17 without changing v16 or reviews."""
from __future__ import annotations
import argparse
import base64
import difflib
from collections import Counter
import hashlib
import json
import lzma
from pathlib import Path, PurePosixPath
import re
import shutil
import subprocess
import sys
import tempfile

REVIEW='0ef7e8bd90c0767b7fdc0f2bd175548242e39cec'
SUBMISSION='9f6875ebf1473b84dcde2ccabcb1556202233276'
MANIFEST_BLOB='56abcea02dc07ce483e0eb2c2182ebce31c4e48d'
BASE_PDF='7e3bdfe801faa834a2a1da0cd771f5d0e68674a4b35c9f8d73d52c4dbf28b45d'
PAYLOAD_SHA256='93ae0c6be9543b9748f64360b46da88f4f666c09805501b9538f87e9741260f1'
GENERATED={'BUILD_REPORT.json','PRESERVATION_REPORT.json','SOURCE_MANIFEST.json',
           'MATERIALIZATION.json','VISUAL_INSPECTION.md','ARTIFACT_INSPECTION.json'}

def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def blob(data: bytes) -> str:
    return hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()

def ignored(directory: str, names: list[str]) -> list[str]:
    return [n for n in names if n in {'build','validation','__pycache__','.git'} or
            Path(n).suffix in {'.pdf','.aux','.log','.out','.toc','.pyc'}]

def main() -> None:
    parser=argparse.ArgumentParser()
    parser.add_argument('--base',type=Path)
    parser.add_argument('--output',type=Path)
    parser.add_argument('--inputs',type=Path,help='Local uncompressed input directory')
    args=parser.parse_args()
    here=Path(__file__).resolve().parent
    repo=here.parents[1]
    base=(args.base or repo/'papers/A1-english-v16').resolve()
    target=(args.output or repo/'papers/A1-english-v17').resolve()
    if target.exists():raise FileExistsError('Refuse to replace an existing revision directory: '+str(target))
    if args.inputs:
        entries={}
        for path in sorted(args.inputs.rglob('*')):
            if not path.is_file():continue
            rel=path.relative_to(args.inputs).as_posix();text=path.read_text()
            info={'sha256':sha(text.encode())}
            if (base/rel).is_file():
                old_text=(base/rel).read_text();a=old_text.splitlines(keepends=True);b=text.splitlines(keepends=True)
                edits=[[i,j,''.join(b[k:l])] for tag,i,j,k,l in
                       difflib.SequenceMatcher(None,a,b,autojunk=False).get_opcodes() if tag!='equal']
                info.update(base_sha256=sha(old_text.encode()),edits=edits)
            else:info['text']=text
            entries[rel]=info
        payload=json.dumps(entries,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()
    else:
        parts=sorted(here.glob('a1-v17-inputs-*.b64'))
        if not parts:raise FileNotFoundError('Missing versioned revision inputs')
        encoded=''.join(p.read_text().strip() for p in parts)
        payload=lzma.decompress(base64.b64decode(encoded,validate=True))
        if sha(payload)!=PAYLOAD_SHA256:raise ValueError('Revision-input digest mismatch')
    entries=json.loads(payload);files={}
    if sha(payload)!=PAYLOAD_SHA256:raise ValueError('Revision-input digest mismatch')
    for rel,info in entries.items():
        q=PurePosixPath(rel)
        if q.is_absolute() or '..' in q.parts or '.git' in q.parts:
            raise ValueError('Unsafe input path: '+rel)
        if 'base_sha256' in info:
            original=(base/rel).read_text()
            if sha(original.encode())!=info['base_sha256']:
                raise ValueError('Patch base mismatch: '+rel)
            lines=original.splitlines(keepends=True)
            for i,j,replacement in reversed(info['edits']):
                if not 0<=i<=j<=len(lines):raise ValueError('Invalid patch range: '+rel)
                lines[i:j]=replacement.splitlines(keepends=True)
            text=''.join(lines)
        else:text=info['text']
        if not isinstance(text,str) or sha(text.encode())!=info['sha256']:
            raise ValueError('Patched source mismatch: '+rel)
        files[rel]=text
    raw_manifest=(base/'SOURCE_MANIFEST.json').read_bytes()
    if blob(raw_manifest)!=MANIFEST_BLOB:raise ValueError('Pinned v16 manifest mismatch')
    old=json.loads(raw_manifest)
    for rel,digest in old['files'].items():
        if sha((base/rel).read_bytes())!=digest:raise ValueError('Pinned source mismatch: '+rel)
    if sha((base/'main.pdf').read_bytes())!=BASE_PDF:raise ValueError('Pinned v16 PDF mismatch')
    # Prepare only a temporary v16 checkout; the source directory remains untouched.
    with tempfile.TemporaryDirectory(prefix='a1-v16-proof-baseline-') as tmp:
        copy=Path(tmp)/'v16'
        shutil.copytree(base,copy,ignore=ignored)
        subprocess.run([sys.executable,'build.py','--prepare-only'],cwd=copy,check=True,
                       stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
        text=(copy/'build/expanded.tex').read_text()
    proofs=re.findall(r'\\begin\{proof\}.*?\\end\{proof\}',text,re.S)
    statements=[m.group() for m in re.finditer(r'\\begin\{(theorem|lemma|proposition|corollary)\}.*?\\end\{\1\}',text,re.S)]
    labels=re.findall(r'\\label\{((?:thm|lem|cor|prop):[^}]+)\}',text)
    if len(proofs)!=84 or len(statements)!=87 or len(labels)!=87:
        raise ValueError('Unexpected baseline theorem/proof count')
    preservation={'source_submission':SUBMISSION,'source_review':REVIEW,
       'source_manifest_git_blob':MANIFEST_BLOB,'expanded_sha256':sha(text.encode()),
       'proof_sha256':[sha(x.encode()) for x in proofs],
       'statement_sha256':[sha(x.encode()) for x in statements],'named_results':labels,
       'scope':'Complete v16 compiled blocks reconstructed from the independently anchored source; not proof validity.'}
    shutil.copytree(base,target,ignore=ignored)
    history=target/'history';history.mkdir(exist_ok=True)
    (history/'V16_SOURCE_MANIFEST.json').write_bytes(raw_manifest)
    archive=set(files)|GENERATED|{'validation/EXECUTION_REPORT.json'}
    for rel in sorted(archive):
        source=base/rel
        if source.is_file():
            destination=history/('V16_'+rel.replace('/','__'))
            if destination.exists() and destination.read_bytes()!=source.read_bytes():
                raise ValueError('Conflicting historical archive: '+str(destination))
            destination.write_bytes(source.read_bytes())
    for name in GENERATED:(target/name).unlink(missing_ok=True)
    for rel,content in files.items():
        p=target/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(content)
    (target/'V16_PRESERVATION_MANIFEST.json').write_text(json.dumps(preservation,indent=2)+'\n')
    materialization={'version':17,'submission_basis':SUBMISSION,'controlling_review':REVIEW,
       'verified_base_manifest_git_blob':MANIFEST_BLOB,'verified_base_source_files':len(old['files']),
       'verified_base_pdf_sha256':BASE_PDF,'input_payload_sha256':sha(payload),
       'input_files':sorted(files),'method':'Copy complete anchored v16, archive superseded text and metadata, apply explicit v17 inputs, preserve every inherited compiled statement and proof.',
       'old_revision_and_review_modified':False}
    (target/'MATERIALIZATION.json').write_text(json.dumps(materialization,indent=2)+'\n')
    subprocess.run([sys.executable,'manifest.py','--write'],cwd=target,check=True)
    subprocess.run([sys.executable,'build.py','--prepare-only'],cwd=target,check=True)
    print(json.dumps(materialization,indent=2))

if __name__=='__main__':main()
