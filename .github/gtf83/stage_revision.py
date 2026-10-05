#!/usr/bin/env python3
"""Stage only the new v83 native corpus over the immutable reviewed v82.

Every transferred file is checked before staging. Earlier manuscripts and
reports are read only. This script creates no PDF and changes no Git ref.
"""
from pathlib import Path
import base64
import hashlib
import importlib.util
import json
import lzma
import shutil
import subprocess

REPO=Path(__file__).resolve().parents[2]
BASE=REPO/'papers/GTF-I-v82-finite-outcome-geometry'
ROOT=REPO/'papers/GTF-I-v83-coupled-boundary-geometry'
BASE_COMMIT='57937576a6f413594589d0509a6816ca4ea3a83e'
DELTA_SHA='97d1e790964ef00d3eea108a93691d649fc21b616ec50d746a56dc66a8e0d128'
INVENTORY_SHA='ad8a527bd4b628d5b258ad19e23f6a38684c58d0201be11269b1a86b582d5ac9'
BASELINE_SHA='d09e0c642c7a493de5c2b4f118c26d979ca5a5d704d7ebeaeb9e38529d83c477'
CHANGED=['README.md','quantitative.tex','main.tex','RESPONSE_TO_REFEREE.md',
 'PROOF_STATUS.json','PROOF_AUDIT.md','HISTORY_AND_PIPELINE_AUDIT.md',
 'LITERATURE_AUDIT.md','INDEPENDENT_REVIEW_BRIEF.md','RESOURCE_LEDGER.md',
 'RESOURCE_LEDGER.json','JOURNAL_README.md','CONTROLLING_REPORTS.json',
 'build_revision.py','publish_revision.py','journal_verify.py',
 'PRESERVATION_MANIFEST.json','PROOF_TEXT_PRESERVATION.json']
REPORTS=[('FROZEN_R52_REPORT.md','5bb27a43c0f78ba99020f605a0489bcbd403e236',
 'GENERAL_THETA_FOUNDATIONS_I_V82_REFEREE_REPORT_R52.md',
 'c4e090bf3394003a5d8142d77359bfeea65d698e6749030707ee8f5fb9779902'),
 ('FROZEN_R52_PIPELINE_AUDIT.md','7d5b1033f31c348ae60ebfb04e8b8d57b3b9e75e',
 'GENERAL_THETA_FOUNDATIONS_I_V82_PROOF_PIPELINE_AUDIT_R52.md',
 '7f1574e2e1bb3530a14af06ed83054106cdcceafa62fb59052975416052c71af')]

def require(condition,message):
    if not condition:raise RuntimeError(message)

def digest(data):return hashlib.sha256(data).hexdigest()

def git(*args):
    return subprocess.check_output(['git',*args],cwd=REPO,text=True).strip()

def safe(name):
    path=Path(name)
    require(not path.is_absolute() and '..' not in path.parts and name==path.as_posix(),
            'unsafe relative path')
    return path

def main():
    require(not ROOT.exists(),'refusing to overwrite a revision directory')
    require(git('diff','--name-only',BASE_COMMIT,'HEAD','--',str(BASE.relative_to(REPO)))=='',
            'reviewed predecessor changed')
    packed=''.join((REPO/'.github/gtf83'/('delta.part'+str(i))).read_text().strip()
                   for i in range(4))
    compressed=base64.b64decode(packed,validate=True)
    require(digest(compressed)==DELTA_SHA,'transport digest mismatch')
    delta=json.loads(lzma.decompress(compressed))
    require(len(delta)==27,'unexpected native delta size')
    spec=importlib.util.spec_from_file_location('v82_reference_builder',BASE/'build_revision.py')
    old=importlib.util.module_from_spec(spec);spec.loader.exec_module(old)
    inventory,checked=old.check_source()
    require(len(inventory)==465,'unexpected predecessor native inventory')
    ROOT.mkdir(parents=True)
    for name in inventory:
        dest=ROOT/safe(name);dest.parent.mkdir(parents=True,exist_ok=True)
        shutil.copy2(BASE/name,dest)
    for name in CHANGED:
        dest=ROOT/'predecessor-v82-audit'/name;dest.parent.mkdir(parents=True,exist_ok=True)
        shutil.copy2(BASE/name,dest)
    baseline={'schema':'gtf83.predecessor/1','commit':BASE_COMMIT,
      'native_commit':'868c841240f62a35cf7fc16ace388b0d11dfa920',
      'files':inventory,'graphs':checked['graphs'],'changed_predecessor_paths':CHANGED,
      'originals':'predecessor-v82-audit/'}
    data=(json.dumps(baseline,indent=2,sort_keys=True)+'\n').encode()
    require(digest(data)==BASELINE_SHA,'predecessor graph or baseline identity differs')
    (ROOT/'V82_BASELINE.json').write_bytes(data)
    for name,commit,path,expected in REPORTS:
        data=subprocess.check_output(['git','show',commit+':'+path],cwd=REPO)
        require(digest(data)==expected,'controlling report bytes differ')
        (ROOT/name).write_bytes(data)
    for name,item in delta.items():
        path=ROOT/safe(name)
        if 'text' in item:
            text=item['text']
        else:
            data=(BASE/safe(item['base'])).read_bytes()
            require(digest(data)==item['base_sha256'],'delta predecessor hash mismatch: '+name)
            lines=data.decode('utf-8').splitlines(keepends=True)
            chunks=[]
            for operation in item['ops']:
                if isinstance(operation,str):chunks.append(operation)
                else:
                    require(isinstance(operation,list) and len(operation)==2 and
                            all(type(x) is int for x in operation) and
                            0<=operation[0]<=operation[1]<=len(lines),'invalid line-copy operation')
                    chunks.append(''.join(lines[operation[0]:operation[1]]))
            text=''.join(chunks)
        data=text.encode('utf-8')
        require(digest(data)==item['sha256'],'expanded native hash mismatch: '+name)
        path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(data)
    final=old.sources(ROOT)
    require(len(final)==495,'unexpected final native inventory')
    require(digest(json.dumps(final,sort_keys=True,separators=(',',':')).encode())==INVENTORY_SHA,
            'complete final source inventory differs')
    prefix=ROOT.relative_to(REPO).as_posix()+'/'
    subprocess.run(['git','add','--',*[prefix+n for n in final]],cwd=REPO,check=True)
    staged=set(git('diff','--cached','--name-only').splitlines())
    require(staged=={prefix+n for n in final},'unrelated or missing staged files')
    print(json.dumps({'schema':'gtf83.staging/1','status':'success',
      'reviewed_predecessor':BASE_COMMIT,'transport_sha256':DELTA_SHA,
      'native_files':len(final),'expanded_delta_files':len(delta),
      'complete_inventory_sha256':INVENTORY_SHA},indent=2))

if __name__=='__main__':main()
