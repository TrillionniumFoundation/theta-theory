#!/usr/bin/env python3
"""Reconstruct only the new v85 native directory from pinned v84 and R54 inputs."""
from pathlib import Path
import base64
import hashlib
import importlib.util
import json
import lzma
import shutil
import subprocess

REPO=Path(__file__).resolve().parents[2]
BASE=REPO/'papers/GTF-I-v84-support-geometry'
ROOT=REPO/'papers/GTF-I-v85-smooth-boundary-geometry'
BASE_COMMIT='9ee14476f539a38f2f45f9bd4ed99a658a7eb14d'
DELTA_SHA='0415330c2953c779e75b278c48213a96a60bf2a1db72603ccb43a1dd48cecb36'
INVENTORY_SHA='17c600aa2f52e1f13af7be3a81820627c151403dd6372ca64a92dea6028d87d2'
CHANGED=['README.md','quantitative.tex','main.tex','RESPONSE_TO_REFEREE.md',
 'PROOF_STATUS.json','PROOF_AUDIT.md','HISTORY_AND_PIPELINE_AUDIT.md',
 'LITERATURE_AUDIT.md','INDEPENDENT_REVIEW_BRIEF.md','RESOURCE_LEDGER.md',
 'RESOURCE_LEDGER.json','JOURNAL_README.md','CONTROLLING_REPORTS.json',
 'build_revision.py','publish_revision.py','journal_verify.py',
 'PRESERVATION_MANIFEST.json','PROOF_TEXT_PRESERVATION.json']
REPORTS=[('FROZEN_R54_REPORT.md','e96b4d271e60ec636e1e6022d1708b755a9e4d4a',
 'GENERAL_THETA_FOUNDATIONS_I_V84_REFEREE_REPORT_R54.md',
 'ca0712f6e1afaf6ea87f445a14aee9451d07239adebaeb4db37e234f8d64d4d3'),
 ('FROZEN_R54_PIPELINE_AUDIT.md','57d23a10cb08171b2ab23464fca8ba89e808f253',
 'GENERAL_THETA_FOUNDATIONS_I_V84_PROOF_PIPELINE_AUDIT_R54.md',
 '789767007436d9a8109ced9421a8af5ee26088df46793540a13f1066f8afe855')]

def require(ok,message):
    if not ok:raise RuntimeError(message)

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
            'predecessor differs from its immutable publication')
    encoded=''.join((REPO/'.github/gtf85'/('delta.part'+str(i))).read_text().strip()
                    for i in range(5))
    packed=base64.b64decode(encoded,validate=True)
    require(digest(packed)==DELTA_SHA,'transport digest mismatch')
    delta=json.loads(lzma.decompress(packed))
    require(len(delta)==33,'unexpected native delta size')
    spec=importlib.util.spec_from_file_location('v84_reference_builder',BASE/'build_revision.py')
    old=importlib.util.module_from_spec(spec);spec.loader.exec_module(old)
    inventory=old.sources(BASE)
    require(len(inventory)==529,'unexpected predecessor native inventory')
    ROOT.mkdir(parents=True)
    for name in inventory:
        dest=ROOT/safe(name);dest.parent.mkdir(parents=True,exist_ok=True)
        shutil.copy2(BASE/name,dest)
    for name in CHANGED:
        dest=ROOT/'predecessor-v84-audit'/safe(name);dest.parent.mkdir(parents=True,exist_ok=True)
        shutil.copy2(BASE/name,dest)
    graphs={}
    for entry in old.DOCS:
        files,labels=old.graph(BASE,entry)
        graphs[entry]={'files':sorted(files),'labels':sorted(labels)}
    baseline={'schema':'gtf85.predecessor/1','commit':BASE_COMMIT,
      'native_commit':'bd90865ed1d755399bcf047ec4d353cac0f48206',
      'files':inventory,'graphs':graphs,'changed_predecessor_paths':CHANGED,
      'originals':'predecessor-v84-audit/'}
    (ROOT/'V84_BASELINE.json').write_text(json.dumps(baseline,indent=2,sort_keys=True)+'\n')
    for name,commit,path,expected in REPORTS:
        data=subprocess.check_output(['git','show',commit+':'+path],cwd=REPO)
        require(digest(data)==expected,'frozen report digest mismatch')
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
    require(len(final)==565,'unexpected v85 native inventory')
    serialized=(json.dumps(final,indent=2,sort_keys=True)+'\n').encode('utf-8')
    require(digest(serialized)==INVENTORY_SHA,'complete native inventory digest mismatch')
    prefix=ROOT.relative_to(REPO).as_posix()+'/'
    subprocess.run(['git','add','--',*[prefix+n for n in final]],cwd=REPO,check=True)
    staged=set(git('diff','--cached','--name-only').splitlines())
    require(staged=={prefix+n for n in final},'unrelated or missing staged files')
    print(json.dumps({'schema':'gtf85.staging/1','status':'success',
      'predecessor_commit':BASE_COMMIT,'transport_sha256':DELTA_SHA,
      'source_inventory_sha256':INVENTORY_SHA,'native_files':len(final),
      'expanded_delta_files':len(delta),'prior_directories_modified':False},indent=2))

if __name__=='__main__':main()
