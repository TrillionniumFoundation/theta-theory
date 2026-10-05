#!/usr/bin/env python3
"""Expand the source-hash-bound v89 delta over the immutable v88 native corpus.

Only the new manuscript directory is staged. No earlier proof, branch, PDF,
status or source is altered by this script.
"""
from pathlib import Path
import base64, hashlib, importlib.util, json, lzma, shutil, subprocess
REPO=Path(__file__).resolve().parents[2]
BASE=REPO/'papers/GTF-I-v88-feedback-reset-width'
ROOT=REPO/'papers/GTF-I-v89-resource-profile'
BASE_COMMIT='d1add4a7ba45230b3cba71b47ef46da5e4a88d72'
PACKED_SHA='3eb75049d76c9e68698120e241370029b89081a5899d156f9d15043e26f04761'
CHANGED=['README.md','quantitative.tex','main.tex','RESPONSE_TO_REFEREE.md','PROOF_STATUS.json','PROOF_AUDIT.md','HISTORY_AND_PIPELINE_AUDIT.md','LITERATURE_AUDIT.md','INDEPENDENT_REVIEW_BRIEF.md','RESOURCE_LEDGER.md','RESOURCE_LEDGER.json','JOURNAL_README.md','CONTROLLING_REPORTS.json','build_revision.py','publish_revision.py','journal_verify.py','PRESERVATION_MANIFEST.json','PROOF_TEXT_PRESERVATION.json']
REPORTS={'FROZEN_R58_REPORT.md': ('601b5b72ce223ee6650e346457a8915ea38a51de', 'GENERAL_THETA_FOUNDATIONS_I_V88_REFEREE_REPORT_R58.md', '16e3999c2fc0b5f6f2661a4a1c911978c4d72f871d130ab2afbac79c7cbc0082'), 'FROZEN_R58_PIPELINE_AUDIT.md': ('c493692c529b0bfe73fcb3c7de9a3b676308f233', 'GENERAL_THETA_FOUNDATIONS_I_V88_PROOF_PIPELINE_AUDIT_R58.md', 'fa9384731cbb00425b39e708de3d00483b40d4f37b99cc0baa86b301a4b9e2dd')}
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
    encoded=''.join((REPO/'.github/gtf89'/f'delta.part{i}').read_text().strip() for i in range(4))
    packed=base64.b64decode(encoded,validate=True)
    require(sha(packed)==PACKED_SHA,'transport digest differs')
    delta=json.loads(lzma.decompress(packed));require(len(delta)==42,'wrong delta inventory')
    spec=importlib.util.spec_from_file_location('v88_baseline_builder',BASE/'build_revision.py')
    old=importlib.util.module_from_spec(spec);spec.loader.exec_module(old)
    inv=old.sources(BASE);require(len(inv)==665,'wrong baseline inventory')
    ROOT.mkdir(parents=True)
    for name in inv:
        dest=ROOT/safe(name);dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(BASE/name,dest)
    for name in CHANGED:
        dest=ROOT/'predecessor-v88-audit'/name;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(BASE/name,dest)
    graphs={}
    for entry in old.DOCS:
        f,l=old.graph(BASE,entry);graphs[entry]={'files':sorted(f),'labels':sorted(l)}
    baseline={'schema':'gtf89.predecessor/1','commit':BASE_COMMIT,'native_commit':'cebd9b28f8ea603fa98c8c5c8f70d9e1daafb3d1','files':inv,'graphs':graphs,'changed_predecessor_paths':CHANGED,'originals':'predecessor-v88-audit/'}
    (ROOT/'V88_BASELINE.json').write_text(json.dumps(baseline,indent=2,sort_keys=True)+'\n')
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
    final=old.sources(ROOT);require(len(final)==710,'wrong expanded source inventory')
    require(sha(json.dumps(final,sort_keys=True,separators=(',',':')).encode())=='31ffb8235c71b57705a3fa9260d7b038d32aee397d5e49a2a104be13a5b16a67','complete native inventory mismatch')
    prefix=ROOT.relative_to(REPO).as_posix()+'/'
    names=[prefix+n for n in final]
    subprocess.run(['git','add','--',*names],cwd=REPO,check=True)
    require(set(git('diff','--cached','--name-only').splitlines())==set(names),'staged unrelated or missing changes')
    print(json.dumps({'schema':'gtf89.staging/1','status':'success','base_commit':BASE_COMMIT,'transport_sha256':PACKED_SHA,'native_files':len(final),'delta_files':len(delta)},indent=2))
if __name__=='__main__':main()
