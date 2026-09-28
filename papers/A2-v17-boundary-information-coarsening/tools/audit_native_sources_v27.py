#!/usr/bin/env python3
"""Audit both complete native A2 TeX closures. Missing inputs are fatal.

The literal TeX scanner is an integration aid, not a TeX interpreter or proof
checker. The native build and its engine logs remain authoritative.
"""
from __future__ import annotations
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import re
import subprocess

ROOT=Path(__file__).resolve().parents[1]
INPUT=re.compile(r'\\(?:input|include)\s*\{([^}]+)\}')
LABEL=re.compile(r'\\label\s*\{([^}]+)\}')
REF=re.compile(r'\\(?:eqref|ref|pageref|autoref|cref|Cref|nameref)\*?\s*\{([^}]+)\}')
CITE=re.compile(r'\\(?:cite|citep|citet)\*?(?:\s*\[[^\]]*\]){0,2}\s*\{([^}]+)\}')
BIB=re.compile(r'\\bibitem(?:\s*\[[^\]]*\])?\s*\{([^}]+)\}')

def clean(text: str) -> str:
    return re.sub(r'(?<!\\)%[^\n]*','',text)

def scan(entry: str) -> dict:
    files: dict[str,dict]={}
    edges: list[dict]=[]
    labels: Counter=Counter()
    refs: set[str]=set()
    citations: set[str]=set()
    bibliography: Counter=Counter()
    def visit(name: str, stack: tuple[str,...]) -> None:
        rel=Path(name)
        if rel.is_absolute() or '..' in rel.parts:
            raise ValueError('Nonlocal native input: '+name)
        if name in stack:
            raise ValueError('Recursive native input: '+' -> '.join((*stack,name)))
        path=ROOT/rel
        if not path.is_file():
            raise FileNotFoundError('Missing native input: '+name)
        raw=path.read_bytes()
        text=clean(raw.decode('utf-8'))
        files[name]={'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest(),
                     'git_blob':hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()}
        labels.update(LABEL.findall(text))
        bibliography.update(BIB.findall(text))
        for match in REF.findall(text):
            refs.update(v.strip() for v in match.split(','))
        for match in CITE.findall(text):
            citations.update(v.strip() for v in match.split(','))
        for rawname in INPUT.findall(text):
            child=rawname if rawname.endswith('.tex') else rawname+'.tex'
            edges.append({'from':name,'to':child})
            visit(child,(*stack,name))
    visit(entry,())
    return {'files':dict(sorted(files.items())),'edges':edges,
            'labels':dict(sorted(labels.items())),'references':sorted(refs),
            'citations':sorted(citations),'bibliography':dict(sorted(bibliography.items()))}

def main() -> None:
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args()
    out=args.output.resolve()
    out.parent.mkdir(parents=True,exist_ok=True)
    result={'status':'started','source_commit':None,
            'scope':'Complete literal native input graph for main.tex and two_collision.tex; not mathematical certification.',
            'entries':{},'errors':[]}
    try:
        cp=subprocess.run(['git','rev-parse','HEAD'],cwd=ROOT,capture_output=True,text=True,check=False)
        if cp.returncode==0: result['source_commit']=cp.stdout.strip()
        for entry in ('two_collision.tex','main.tex'):
            result['entries'][entry]=scan(entry)
        other=result['entries']['two_collision.tex']['labels']
        for entry,data in result['entries'].items():
            available=set(data['labels'])
            if entry=='main.tex': available.update('TC-'+k for k in other)
            unresolved=sorted(set(data['references'])-available)
            uncited=sorted(set(data['citations'])-set(data['bibliography']))
            duplicate_labels=sorted(k for k,v in data['labels'].items() if v>1)
            duplicate_bib=sorted(k for k,v in data['bibliography'].items() if v>1)
            data['diagnostics']={'unresolved_references':unresolved,'unresolved_citations':uncited,
                                 'duplicate_labels':duplicate_labels,'duplicate_bibliography':duplicate_bib}
            for key,values in data['diagnostics'].items():
                if values: result['errors'].append({'entry':entry,'kind':key,'values':values})
        allfiles={p:meta for data in result['entries'].values() for p,meta in data['files'].items()}
        encoded=json.dumps(dict(sorted(allfiles.items())),sort_keys=True,separators=(',',':')).encode()
        result['unique_native_files']=len(allfiles)
        result['native_manifest_sha256']=hashlib.sha256(encoded).hexdigest()
        if result['errors']: raise RuntimeError('Native literal source diagnostics failed; see output JSON')
        result['status']='passed'
    except Exception as exc:
        result['status']='failed'
        result['exception']=str(exc)
        raise
    finally:
        out.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':result['status'],'source_commit':result['source_commit'],
                      'unique_native_files':result['unique_native_files'],
                      'native_manifest_sha256':result['native_manifest_sha256']},indent=2,sort_keys=True))

if __name__=='__main__':
    main()
