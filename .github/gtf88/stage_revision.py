#!/usr/bin/env python3
"""Expand the source-hash-bound v88 delta over the immutable v87 native corpus.

Only the new manuscript directory is staged. No earlier proof, branch, PDF,
status or source is altered by this script.
"""
from pathlib import Path
import base64, hashlib, importlib.util, json, lzma, shutil, subprocess
REPO=Path(__file__).resolve().parents[2]
BASE=REPO/'papers/GTF-I-v87-entanglement-width'
ROOT=REPO/'papers/GTF-I-v88-feedback-reset-width'
BASE_COMMIT='aab076189b7276f6a0b4113b472ea09a7ac640cc'
PACKED_SHA='6a5f9ec7286c5c473b5728427ba08c64556040cba0e27d6243037196c7fac80e'
CHANGED=['README.md','quantitative.tex','main.tex','RESPONSE_TO_REFEREE.md','PROOF_STATUS.json','PROOF_AUDIT.md','HISTORY_AND_PIPELINE_AUDIT.md','LITERATURE_AUDIT.md','INDEPENDENT_REVIEW_BRIEF.md','RESOURCE_LEDGER.md','RESOURCE_LEDGER.json','JOURNAL_README.md','CONTROLLING_REPORTS.json','build_revision.py','publish_revision.py','journal_verify.py','PRESERVATION_MANIFEST.json','PROOF_TEXT_PRESERVATION.json']
REPORTS={'FROZEN_R57_REPORT.md':('796657054bac22426f33520474e4b6020892ee32','GENERAL_THETA_FOUNDATIONS_I_V87_REFEREE_REPORT_R57.md','7391089c2bb0912fa3d75fd51b67dd45077e9fe6c74ee872b1763cd79b640b46'),'FROZEN_R57_PIPELINE_AUDIT.md':('0546af1e2f9caebbbc29376e9eee192440f2e1a2','GENERAL_THETA_FOUNDATIONS_I_V87_PROOF_PIPELINE_AUDIT_R57.md','8440be72b329e4b2f8598e32a3fc106640e28468cae79a6621bf288b8d3b0965')}
def require(ok,msg):
    if not ok:raise RuntimeError(msg)
def sha(data):return hashlib.sha256(data).hexdigest()
def git(*args):return subprocess.check_output(['git',*args],cwd=REPO,text=True).strip()
def safe(name):
    p=Path(name)
    require(not p.is_absolute() and '..' not in p.parts and p.as_posix()==name,'unsafe delta path')
    return p

def main():
    require(not ROOT.exists(),'refusing to replace an existing revision')
    require(not git('diff','--name-only',BASE_COMMIT,'HEAD','--',str(BASE.relative_to(REPO))),'immutable predecessor changed')
    encoded=''.join((REPO/'.github/gtf88'/f'delta.part{i}').read_text().strip() for i in range(3))
    packed=base64.b64decode(encoded,validate=True)
    require(sha(packed)==PACKED_SHA,'transport digest differs')
    delta=json.loads(lzma.decompress(packed));require(len(delta)==30,'wrong delta inventory')
    spec=importlib.util.spec_from_file_location('v87_baseline_builder',BASE/'build_revision.py')
    old=importlib.util.module_from_spec(spec);spec.loader.exec_module(old)
    inv=old.sources(BASE);require(len(inv)==632,'wrong baseline inventory')
    ROOT.mkdir(parents=True)
    for name in inv:
        dest=ROOT/safe(name);dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(BASE/name,dest)
    for name in CHANGED:
        dest=ROOT/'predecessor-v87-audit'/name;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(BASE/name,dest)
    graphs={}
    for entry in old.DOCS:
        f,l=old.graph(BASE,entry);graphs[entry]={'files':sorted(f),'labels':sorted(l)}
    baseline={'schema':'gtf88.predecessor/1','commit':BASE_COMMIT,'native_commit':'d4fc44a02ee0585bf9da899239c3f976d75cc9cf','files':inv,'graphs':graphs,'changed_predecessor_paths':CHANGED,'originals':'predecessor-v87-audit/'}
    (ROOT/'V87_BASELINE.json').write_text(json.dumps(baseline,indent=2,sort_keys=True)+'\n')
    for name,(commit,path,digest) in REPORTS.items():
        data=subprocess.check_output(['git','show',commit+':'+path],cwd=REPO)
        require(sha(data)==digest,'frozen report differs');(ROOT/name).write_bytes(data)
    for name,item in delta.items():
        if 'text' in item:text=item['text']
        else:
            data=(BASE/safe(item['base'])).read_bytes()
            require(sha(data)==item['base_sha256'],'delta base differs: '+name)
            lines=data.decode('utf-8').splitlines(keepends=True);pieces=[]
            for op in item['ops']:
                if isinstance(op,str):pieces.append(op)
                else:
                    require(isinstance(op,list) and len(op)==2 and all(type(i) is int for i in op) and 0<=op[0]<=op[1]<=len(lines),'invalid delta operation')
                    pieces.append(''.join(lines[op[0]:op[1]]))
            text=''.join(pieces)
        data=text.encode('utf-8');require(sha(data)==item['result_sha256'],'expanded source differs: '+name)
        p=ROOT/safe(name);p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(data)
    final=old.sources(ROOT);require(len(final)==665,'wrong expanded source inventory')
    prefix=ROOT.relative_to(REPO).as_posix()+'/'
    names=[prefix+n for n in final]
    subprocess.run(['git','add','--',*names],cwd=REPO,check=True)
    require(set(git('diff','--cached','--name-only').splitlines())==set(names),'staged unrelated or missing changes')
    print(json.dumps({'schema':'gtf88.staging/1','status':'success','base_commit':BASE_COMMIT,'transport_sha256':PACKED_SHA,'native_files':len(final),'delta_files':len(delta)},indent=2))
if __name__=='__main__':main()
