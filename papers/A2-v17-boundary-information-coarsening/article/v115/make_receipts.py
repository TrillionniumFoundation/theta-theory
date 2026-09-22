#!/usr/bin/env python3
"""Bind actual source bytes, build logs and PDFs to their local build commit."""
from __future__ import annotations
import hashlib,json,os,re,subprocess,sys
from datetime import datetime,timezone
from pathlib import Path
HERE=Path(__file__).resolve().parent

def digest(p:Path)->str:return hashlib.sha256(p.read_bytes()).hexdigest()
def run(*args:str,cwd:Path=HERE)->str:return subprocess.check_output(list(args),cwd=cwd,text=True).strip()
def need(ok:bool,message:str)->None:
    if not ok:raise RuntimeError(message)

def source_paths()->list[Path]:
    selected=[]
    for p in HERE.rglob('*'):
        if not p.is_file() or '__pycache__' in p.parts:continue
        r=p.relative_to(HERE)
        if r.parts[0] in ('evidence','crossrefs'):continue
        if p.suffix in ('.tex','.py','.sh','.md'):selected.append(p)
    selected.append(HERE/'evidence/V114_SOURCE_MANIFEST.json')
    return sorted(selected)

def main()->None:
    files=source_paths();hashes={str(p.relative_to(HERE)):digest(p) for p in files}
    commit=None;root=None;prefix=None
    try:
        root=Path(run('git','rev-parse','--show-toplevel'));prefix=HERE.relative_to(root)
        paths=[str(p.relative_to(root)) for p in files]
        commit=run('git','log','-1','--format=%H','--',*paths,cwd=root)
        need(bool(commit),'no committed mathematical source')
        for p,name in zip(files,paths):
            data=subprocess.check_output(['git','show',commit+':'+name],cwd=root)
            need(hashlib.sha256(data).hexdigest()==digest(p),'uncommitted source differs from build commit: '+name)
    except subprocess.CalledProcessError:
        # A standalone ZIP can still be rebuilt, but must not invent a Git commit.
        if (HERE/'.git').exists():raise
        commit=None
    source={'kind':'source-bound local revision receipt','upstream_review_commit':'09869129e16fd43bd2420fa3573a09cd5cbbdff9','upstream_reviewed_source_commit':'d58d4ad0546487f4313cf8ed2f05ad9321b54e63','mathematical_source_commit':commit,'source_commit_namespace':'local_patch_generation_workspace' if commit else 'standalone_uncommitted_rebuild','remote_publication_performed':False,'sha256':hashes}
    pdfs={}
    for name in ('paper','geometry','applications'):
        pdf=HERE/(name+'.pdf');log=HERE/(name+'.log');need(pdf.exists() and log.exists(),'missing generated artifact '+name)
        text=log.read_text(errors='replace')
        problems=re.findall(r'^.*(?:LaTeX Warning:|Package .* Warning:|Overfull \\[hv]box|Undefined control sequence|Emergency stop).*$' ,text,re.M)
        need(not problems,'build warnings in '+name+': '+str(problems))
        info=run('pdfinfo',str(pdf));pages=int(re.search(r'^Pages:\s*(\d+)',info,re.M).group(1))
        fls=(HERE/(name+'.fls')).read_text(errors='replace')
        for inp in re.findall(r'^INPUT (.+)$',fls,re.M):
            path=Path(inp);path=path if path.is_absolute() else HERE/path
            if path.suffix=='.tex' and path.exists() and path.resolve().is_relative_to(HERE):
                rel=str(path.resolve().relative_to(HERE));need(rel in hashes,'untracked TeX build input '+rel)
        pdfs[name+'.pdf']={'sha256':digest(pdf),'bytes':pdf.stat().st_size,'pages':pages,'log_sha256':digest(log),'undefined_references':0,'duplicate_labels':0,'overfull_boxes':0,'compiled_input_record_sha256':digest(HERE/(name+'.fls'))}
    need(hashes=={str(p.relative_to(HERE)):digest(p) for p in files},'source mutated during receipt creation')
    evidence=HERE/'evidence';evidence.mkdir(exist_ok=True)
    (evidence/'SOURCE_RECEIPT.json').write_text(json.dumps(source,indent=2,sort_keys=True)+'\n')
    receipt={'kind':'actual local PDF build; not proof certification','built_utc':datetime.now(timezone.utc).isoformat(),'mathematical_source_commit':commit,'source_receipt_sha256':digest(evidence/'SOURCE_RECEIPT.json'),'diagnostics_sha256':digest(evidence/'DIAGNOSTICS.json'),'pdfs':pdfs,'toolchain':{'python':sys.version,'pdflatex':run('pdflatex','--version').splitlines()[0],'git':run('git','--version')},'reproducibility_epoch':os.environ.get('SOURCE_DATE_EPOCH'),'remote_publication_performed':False,'proof_certification':False}
    (evidence/'BUILD_RECEIPT.json').write_text(json.dumps(receipt,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'source_commit':commit,'pdfs':pdfs},indent=2))
if __name__=='__main__':main()
