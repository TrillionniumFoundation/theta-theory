#!/usr/bin/env python3
"""Bind actual source bytes and build evidence to a committed source snapshot.
Compilation and finite diagnostics are not mathematical proof certification.
"""
from __future__ import annotations
import hashlib, json, os, re, subprocess, sys
from datetime import datetime, timezone
from pathlib import Path
HERE=Path(__file__).resolve().parent
REVIEW='a65e0e92b24fe6882e60ebcf678bb2f9f5048312'
BASE='fadcfaa11a1939625177eb12e97569b63b7a1a9d'
def digest(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def need(ok,msg):
    if not ok: raise RuntimeError(msg)
def run(*args,cwd=HERE):
    return subprocess.check_output(list(args),cwd=cwd,text=True,stderr=subprocess.PIPE).strip()
def source_paths():
    out=[]
    for p in HERE.rglob('*'):
        if not p.is_file() or '__pycache__' in p.parts: continue
        rel=p.relative_to(HERE)
        if rel.parts[0] in ('evidence','crossrefs'): continue
        if p.suffix in ('.tex','.py','.sh','.md','.json'): out.append(p)
    out.append(HERE/'evidence/V116_SOURCE_MANIFEST.json')
    return sorted(out)
def main():
    files=source_paths(); hashes={str(p.relative_to(HERE)):digest(p) for p in files}
    try:
        root=Path(run('git','rev-parse','--show-toplevel'))
    except (subprocess.CalledProcessError,FileNotFoundError):
        root=None
    commit=None
    if root is not None:
        commit=run('git','rev-parse','HEAD',cwd=root)
        for p in files:
            name=str(p.relative_to(root))
            raw=subprocess.check_output(['git','show',commit+':'+name],cwd=root,stderr=subprocess.PIPE)
            need(hashlib.sha256(raw).hexdigest()==digest(p),'Source differs from committed build input: '+name)
    source={'kind':'A2 revision 117 source-bound receipt','controlling_review_commit':REVIEW,'reviewed_revision_commit':BASE,'mathematical_source_commit':commit,'source_commit_namespace':'repository_branch_build' if commit else 'standalone_rebuild','remote_publication_verified_by_this_script':False,'sha256':hashes}
    pdfs={}
    for name in ('paper','geometry','applications'):
        pdf=HERE/(name+'.pdf'); log=HERE/(name+'.log'); fls=HERE/(name+'.fls')
        need(pdf.is_file() and log.is_file() and fls.is_file(),'Missing generated files: '+name)
        text=log.read_text(errors='replace')
        problems=re.findall(r'^.*(?:LaTeX Warning:|Package .* Warning:|Overfull \\[hv]box|Underfull \\[hv]box|Undefined control sequence|Emergency stop).*$' ,text,re.M)
        need(not problems,'Final build warnings in '+name+': '+str(problems))
        info=run('pdfinfo',str(pdf)); pages=int(re.search(r'^Pages:\s*(\d+)',info,re.M).group(1))
        for inp in re.findall(r'^INPUT (.+)$',fls.read_text(errors='replace'),re.M):
            p=Path(inp); p=p if p.is_absolute() else HERE/p
            if p.suffix=='.tex' and p.exists() and p.resolve().is_relative_to(HERE):
                need(str(p.resolve().relative_to(HERE)) in hashes,'Untracked TeX input: '+str(p))
        pdfs[name+'.pdf']={'sha256':digest(pdf),'bytes':pdf.stat().st_size,'pages':pages,'log_sha256':digest(log),'input_record_sha256':digest(fls),'undefined_references':0,'duplicate_labels':0,'overfull_boxes':0,'underfull_boxes':0}
    need(hashes=={str(p.relative_to(HERE)):digest(p) for p in files},'Source changed during receipt creation')
    evidence=HERE/'evidence'; evidence.mkdir(exist_ok=True)
    (evidence/'SOURCE_RECEIPT.json').write_text(json.dumps(source,indent=2,sort_keys=True)+'\n')
    receipt={'kind':'A2 v117 source-bound PDF build; NOT proof certification','built_utc':datetime.now(timezone.utc).isoformat(),'mathematical_source_commit':commit,'source_receipt_sha256':digest(evidence/'SOURCE_RECEIPT.json'),'diagnostics_sha256':digest(evidence/'DIAGNOSTICS.json'),'inherited_diagnostics_sha256':digest(evidence/'V116_RERUN_DIAGNOSTICS.json'),'pdfs':pdfs,'toolchain':{'python':sys.version,'pdflatex':run('pdflatex','--version').splitlines()[0]},'reproducibility_epoch':os.environ.get('SOURCE_DATE_EPOCH'),'remote_publication_verified_by_this_script':False,'proof_certification':False}
    (evidence/'BUILD_RECEIPT.json').write_text(json.dumps(receipt,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'source_commit':commit,'pdfs':pdfs},indent=2))
if __name__=='__main__': main()
