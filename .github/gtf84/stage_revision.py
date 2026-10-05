#!/usr/bin/env python3
"""Stage the hash-bound v84 native source over immutable completed v83.

Only the new paper directory is staged. No earlier source or Git ref is changed.
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
BASE=REPO/'papers/GTF-I-v83-coupled-boundary-geometry'
ROOT=REPO/'papers/GTF-I-v84-support-geometry'
BASE_COMMIT='58cbb2608fa65f1fba1b5d56ab1fd55dfd9dacd7'
DELTA_SHA='ea865ca45f1572f8f6393ea18e0e86ac12f21a334e83df3ec407976a7727e5b1'
CHANGED=['README.md','quantitative.tex','main.tex','RESPONSE_TO_REFEREE.md',
 'PROOF_STATUS.json','PROOF_AUDIT.md','HISTORY_AND_PIPELINE_AUDIT.md',
 'LITERATURE_AUDIT.md','INDEPENDENT_REVIEW_BRIEF.md','RESOURCE_LEDGER.md',
 'RESOURCE_LEDGER.json','JOURNAL_README.md','CONTROLLING_REPORTS.json',
 'build_revision.py','publish_revision.py','journal_verify.py',
 'PRESERVATION_MANIFEST.json','PROOF_TEXT_PRESERVATION.json']
REPORTS=[('FROZEN_R53_REPORT.md','0077ff4b39633c3e9b6947e89f0bbcdd8e5ffe2e',
 'GENERAL_THETA_FOUNDATIONS_I_V83_REFEREE_REPORT_R53.md',
 '5f1860c7f8ec0192042f7a25cfe565cde743ff252d53f5f8e28f71a596ddea6f'),
 ('FROZEN_R53_PIPELINE_AUDIT.md','89c8c9cb3d1494d90c3d449d981a7424665256ab',
 'GENERAL_THETA_FOUNDATIONS_I_V83_PROOF_PIPELINE_AUDIT_R53.md',
 '0803570cebd8ec61f101dd1d8d01457680a033a5df92154aabea4242611948f1')]

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
    require(not ROOT.exists(),'refusing to replace an existing revision directory')
    require(git('diff','--name-only',BASE_COMMIT,'HEAD','--',str(BASE.relative_to(REPO)))=='',
            'immutable predecessor changed')
    packed=''.join((REPO/'.github/gtf84'/('delta.part'+str(i))).read_text().strip()
                   for i in range(7))
    compressed=base64.b64decode(packed,validate=True)
    require(digest(compressed)==DELTA_SHA,'transport digest mismatch')
    delta=json.loads(lzma.decompress(compressed))
    require(len(delta)==31,'unexpected native delta size')
    spec=importlib.util.spec_from_file_location('v83_reference_builder',BASE/'build_revision.py')
    old=importlib.util.module_from_spec(spec);spec.loader.exec_module(old)
    inventory=old.sources(BASE)
    require(len(inventory)==495,'unexpected predecessor native inventory')
    ROOT.mkdir(parents=True)
    for name in inventory:
        dest=ROOT/safe(name);dest.parent.mkdir(parents=True,exist_ok=True)
        shutil.copy2(BASE/name,dest)
    for name in CHANGED:
        dest=ROOT/'predecessor-v83-audit'/name;dest.parent.mkdir(parents=True,exist_ok=True)
        shutil.copy2(BASE/name,dest)
    graphs={}
    for entry in ['quantitative.tex','main.tex','structural.tex']:
        files,labels=old.graph(BASE,entry)
        graphs[entry]={'files':sorted(files),'labels':sorted(labels)}
    baseline={'schema':'gtf84.predecessor/1','commit':BASE_COMMIT,
      'native_commit':'736c313c35e1face0fc8e00d9b8a041188880a5f',
      'files':inventory,'graphs':graphs,'changed_predecessor_paths':CHANGED,
      'originals':'predecessor-v83-audit/'}
    (ROOT/'V83_BASELINE.json').write_text(json.dumps(baseline,indent=2,sort_keys=True)+'\n')
    for dest,commit,path,expected in REPORTS:
        data=subprocess.check_output(['git','show',commit+':'+path],cwd=REPO)
        require(digest(data)==expected,'controlling report digest mismatch')
        (ROOT/dest).write_bytes(data)
    for name,item in delta.items():
        path=ROOT/safe(name)
        if 'text' in item:
            text=item['text']
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
    require(len(final)==529,'unexpected v84 native inventory')
    prefix=ROOT.relative_to(REPO).as_posix()+'/'
    subprocess.run(['git','add','--',*[prefix+n for n in final]],cwd=REPO,check=True)
    staged=set(git('diff','--cached','--name-only').splitlines())
    require(staged=={prefix+n for n in final},'staging includes unrelated or missing files')
    print(json.dumps({'schema':'gtf84.staging/1','status':'success',
      'predecessor_commit':BASE_COMMIT,'transport_sha256':DELTA_SHA,
      'native_files':len(final),'expanded_delta_files':len(delta),
      'preserved_quantitative_package':'primary plus current binary supplement'},indent=2))

if __name__=='__main__':main()
