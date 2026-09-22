#!/usr/bin/env python3
"""Bind actual source bytes, logs and PDFs; never certify mathematical proofs."""
from __future__ import annotations
import hashlib,json,os,re,subprocess,sys
from datetime import datetime,timezone
from pathlib import Path
HERE=Path(__file__).resolve().parent
REVIEW='1cb4e00c86699247454d21dbec2dcce01a9c6b8b'
REVIEWED='acfd3d57e0053e1b03df53020fd8e79e14599c03'
BRANCH='revision/a2-v116-higher-product-structure-2026-09-22'

def digest(p:Path)->str:return hashlib.sha256(p.read_bytes()).hexdigest()
def run(*args:str,cwd:Path=HERE)->str:
    return subprocess.check_output(list(args),cwd=cwd,text=True).strip()
def need(ok:bool,message:str)->None:
    if not ok:raise RuntimeError(message)

def source_paths()->list[Path]:
    selected=[]
    for p in HERE.rglob('*'):
        if not p.is_file() or '__pycache__' in p.parts:continue
        r=p.relative_to(HERE)
        if r.parts[0] in ('evidence','crossrefs'):continue
        if p.suffix in ('.tex','.py','.sh','.md'):selected.append(p)
    selected.extend(HERE/'evidence'/n for n in ('V114_SOURCE_MANIFEST.json','V115_SOURCE_MANIFEST.json'))
    return sorted(selected)

def main()->None:
    files=source_paths();hashes={str(p.relative_to(HERE)):digest(p) for p in files}
    commit=None;remote_head=None
    probe=subprocess.run(['git','rev-parse','--show-toplevel'],cwd=HERE,text=True,capture_output=True)
    if probe.returncode==0:
        root=Path(probe.stdout.strip());paths=[str(p.relative_to(root)) for p in files]
        commit=run('git','log','-1','--format=%H','--',*paths,cwd=root)
        need(bool(commit),'no committed mathematical source')
        for p,name in zip(files,paths):
            data=subprocess.check_output(['git','show',commit+':'+name],cwd=root)
            need(hashlib.sha256(data).hexdigest()==digest(p),'uncommitted source differs from source commit: '+name)
        if os.environ.get('GITHUB_ACTIONS')=='true':
            need(os.environ.get('GITHUB_REF_NAME')==BRANCH,'unexpected publication branch')
            ref=run('git','ls-remote','--heads','origin','refs/heads/'+BRANCH,cwd=root)
            need(bool(ref),'remote branch absent')
            remote_head=ref.split()[0]
            need(subprocess.run(['git','merge-base','--is-ancestor',commit,remote_head],cwd=root).returncode==0,
                 'source commit not present in observed remote branch')
    source={'kind':'source-bound revision receipt','revision':116,
            'upstream_review_commit':REVIEW,'upstream_reviewed_head':REVIEWED,
            'mathematical_source_commit':commit,
            'source_commit_namespace':'repository_branch_build' if commit else 'standalone_uncommitted_rebuild',
            'source_publication_verified':remote_head is not None,'observed_remote_head':remote_head,
            'branch':BRANCH,'generated_evidence_commit_recorded_here':False,
            'sha256':hashes}
    pdfs={}
    for name in ('paper','geometry','applications'):
        pdf=HERE/(name+'.pdf');log=HERE/(name+'.log')
        need(pdf.exists() and log.exists(),'missing generated artifact '+name)
        text=log.read_text(errors='replace')
        problems=re.findall(r'^.*(?:LaTeX Warning:|Package .* Warning:|Overfull \\[hv]box|Undefined control sequence|Emergency stop).*$' ,text,re.M)
        need(not problems,'build warnings in '+name+': '+str(problems))
        info=run('pdfinfo',str(pdf));match=re.search(r'^Pages:\s*(\d+)',info,re.M)
        need(match is not None,'page count absent');pages=int(match.group(1))
        fls=(HERE/(name+'.fls')).read_text(errors='replace')
        for inp in re.findall(r'^INPUT (.+)$',fls,re.M):
            path=Path(inp);path=path if path.is_absolute() else HERE/path
            if path.suffix=='.tex' and path.exists() and path.resolve().is_relative_to(HERE):
                rel=str(path.resolve().relative_to(HERE));need(rel in hashes,'untracked TeX input '+rel)
        pdfs[name+'.pdf']={'sha256':digest(pdf),'bytes':pdf.stat().st_size,'pages':pages,
                         'log_sha256':digest(log),'undefined_references':0,'duplicate_labels':0,
                         'overfull_boxes':0,'compiled_input_record_sha256':digest(HERE/(name+'.fls'))}
    need(hashes=={str(p.relative_to(HERE)):digest(p) for p in files},'source mutated during receipt creation')
    evidence=HERE/'evidence';evidence.mkdir(exist_ok=True)
    (evidence/'SOURCE_RECEIPT.json').write_text(json.dumps(source,indent=2,sort_keys=True)+'\n')
    import sympy
    receipt={'kind':'source-bound PDF build; not proof certification','revision':116,
             'built_utc':datetime.now(timezone.utc).isoformat(),'mathematical_source_commit':commit,
             'source_receipt_sha256':digest(evidence/'SOURCE_RECEIPT.json'),
             'diagnostics_sha256':{n:digest(evidence/n) for n in ('DIAGNOSTICS.json','V116_DIAGNOSTICS.json')},
             'pdfs':pdfs,'toolchain':{'python':sys.version,'sympy':sympy.__version__,
                 'pdflatex':run('pdflatex','--version').splitlines()[0],'git':run('git','--version')},
             'reproducibility_epoch':os.environ.get('SOURCE_DATE_EPOCH'),
             'github_run_id':os.environ.get('GITHUB_RUN_ID'),
             'source_publication_verified':remote_head is not None,'proof_certification':False,
             'note':'Generated artifacts are committed after this receipt; inspect the branch head for that later commit.'}
    (evidence/'BUILD_RECEIPT.json').write_text(json.dumps(receipt,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'source_commit':commit,'pdfs':pdfs},indent=2))
if __name__=='__main__':main()
