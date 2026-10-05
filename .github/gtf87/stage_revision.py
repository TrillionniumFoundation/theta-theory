#!/usr/bin/env python3
"""Reconstruct v87 native sources from the immutable reviewed v86 and checked delta.

Only the new manuscript directory is staged. Previous manuscripts and review
branches are never edited; no source qualification is inferred from transport.
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
BASE=REPO/'papers/GTF-I-v86-one-sided-boundary-geometry'
ROOT=REPO/'papers/GTF-I-v87-entanglement-width'
BASE_COMMIT='0a7d65923c12334ecc60ec42084bdd0c612e2e49'
DELTA_SHA='b59ef6d663ca2d264cf56b70cde58f5ce8ccc74e770847bea6cb2e324c9576d8'
INVENTORY_SHA='815d8a90569ae62da978b0b2254766de307f39cc56050fdf0c49a08a57240098'
CHANGED=['README.md','quantitative.tex','main.tex','RESPONSE_TO_REFEREE.md',
 'PROOF_STATUS.json','PROOF_AUDIT.md','HISTORY_AND_PIPELINE_AUDIT.md',
 'LITERATURE_AUDIT.md','INDEPENDENT_REVIEW_BRIEF.md','RESOURCE_LEDGER.md',
 'RESOURCE_LEDGER.json','JOURNAL_README.md','CONTROLLING_REPORTS.json',
 'build_revision.py','publish_revision.py','journal_verify.py',
 'PRESERVATION_MANIFEST.json','PROOF_TEXT_PRESERVATION.json']
REPORTS=[('9098548d4c8e347193141b34f4a631344500695a',
 'GENERAL_THETA_FOUNDATIONS_I_V86_REFEREE_REPORT_R56.md','FROZEN_R56_REPORT.md',
 '9b610372f2c3e876b56a59c341cbc3f9bcc15d9ab088b6f8ff3afe55277537d1'),
 ('884087a1a62d5d8af4861fed4c4535d8e6eacd0f',
 'GENERAL_THETA_FOUNDATIONS_I_V86_PROOF_PIPELINE_AUDIT_R56.md','FROZEN_R56_PIPELINE_AUDIT.md',
 '674ec80b4fceb8f59cdcd1df0753dc6183c1803e1c91c004e3abd26b2b8c8482')]

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
    require(not ROOT.exists(),'refusing to overwrite an existing revision')
    require(git('diff','--name-only',BASE_COMMIT,'HEAD','--',str(BASE.relative_to(REPO)))=='',
            'reviewed predecessor source changed')
    packed=''.join((REPO/'.github/gtf87'/('delta.part'+str(i))).read_text().strip()
                   for i in range(4))
    compressed=base64.b64decode(packed,validate=True)
    require(digest(compressed)==DELTA_SHA,'transport digest mismatch')
    delta=json.loads(lzma.decompress(compressed))
    require(len(delta)==29,'unexpected delta inventory')
    spec=importlib.util.spec_from_file_location('v86_reference_builder',BASE/'build_revision.py')
    old=importlib.util.module_from_spec(spec);spec.loader.exec_module(old)
    inventory=old.sources(BASE)
    require(len(inventory)==600,'unexpected reviewed native inventory')
    ROOT.mkdir(parents=True)
    for name in inventory:
        dest=ROOT/safe(name);dest.parent.mkdir(parents=True,exist_ok=True)
        shutil.copy2(BASE/name,dest)
    for name in CHANGED:
        dest=ROOT/'predecessor-v86-audit'/name;dest.parent.mkdir(parents=True,exist_ok=True)
        shutil.copy2(BASE/name,dest)
    graphs={}
    for entry in ['quantitative.tex','supplement.tex','structural.tex','main.tex']:
        files,labels=old.graph(BASE,entry)
        graphs[entry]={'files':sorted(files),'labels':sorted(labels)}
    baseline={'schema':'gtf87.predecessor/1','commit':BASE_COMMIT,
      'native_commit':'7f86bddb2309417edaa74430073a1bdf5329d8bf',
      'files':inventory,'graphs':graphs,'changed_predecessor_paths':CHANGED,
      'originals':'predecessor-v86-audit/'}
    (ROOT/'V86_BASELINE.json').write_text(json.dumps(baseline,indent=2,sort_keys=True)+'\n')
    for commit,source,target,expected in REPORTS:
        data=subprocess.check_output(['git','show',commit+':'+source],cwd=REPO)
        require(digest(data)==expected,'controlling report digest mismatch')
        (ROOT/target).write_bytes(data)
    for name,item in delta.items():
        path=ROOT/safe(name)
        if 'text' in item:text=item['text']
        else:
            data=(BASE/safe(item['base'])).read_bytes()
            require(digest(data)==item['base_sha256'],'delta predecessor mismatch: '+name)
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
        encoded=text.encode('utf-8')
        require(digest(encoded)==item['result_sha256'],'expanded native digest mismatch: '+name)
        path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(encoded)
    final=old.sources(ROOT)
    require(len(final)==632,'unexpected new native inventory')
    require(digest(json.dumps(final,indent=2,sort_keys=True).encode())==INVENTORY_SHA,
            'complete native inventory mismatch')
    prefix=ROOT.relative_to(REPO).as_posix()+'/'
    subprocess.run(['git','add','--',*[prefix+n for n in final]],cwd=REPO,check=True)
    staged=set(git('diff','--cached','--name-only').splitlines())
    require(staged=={prefix+n for n in final},'staging contains unrelated or missing files')
    print(json.dumps({'schema':'gtf87.staging/1','status':'success',
        'predecessor_commit':BASE_COMMIT,'transport_sha256':DELTA_SHA,
        'native_inventory_sha256':INVENTORY_SHA,'native_files':len(final),
        'expanded_delta_files':len(delta),'prior_mathematics_modified':False},indent=2))

if __name__=='__main__':main()
