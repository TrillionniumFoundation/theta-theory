#!/usr/bin/env python3
"""Expand the hash-bound v82 native delta over the immutable published v81.

This script stages only the new manuscript directory. It never edits earlier
manuscripts, creates a PDF, infers a proof from tests, or changes a Git ref.
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
BASE=REPO/'papers/GTF-I-v81-finite-risk-certificates'
ROOT=REPO/'papers/GTF-I-v82-finite-outcome-geometry'
BASE_COMMIT='67ada63a593d452f23e8d26540504b8fb8ab8acc'
DELTA_SHA='019cfaa6f1cbfa07fb1597bebed066c5f5569d9ed9d66415289cf92a60c7bfad'
CHANGED=['README.md','quantitative.tex','main.tex','RESPONSE_TO_REFEREE.md',
 'PROOF_STATUS.json','PROOF_AUDIT.md','HISTORY_AND_PIPELINE_AUDIT.md',
 'LITERATURE_AUDIT.md','INDEPENDENT_REVIEW_BRIEF.md','RESOURCE_LEDGER.md',
 'RESOURCE_LEDGER.json','JOURNAL_README.md','CONTROLLING_REPORTS.json',
 'build_revision.py','publish_revision.py','journal_verify.py',
 'PRESERVATION_MANIFEST.json','PROOF_TEXT_PRESERVATION.json']

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
            'predecessor has changed since its immutable publication')
    packed=''.join((REPO/'.github/gtf82'/('delta.part'+str(i))).read_text().strip()
                   for i in range(4))
    compressed=base64.b64decode(packed,validate=True)
    require(digest(compressed)==DELTA_SHA,'transport digest mismatch')
    delta=json.loads(lzma.decompress(compressed))
    require(len(delta)==26,'unexpected native delta size')
    spec=importlib.util.spec_from_file_location('v81_reference_builder',BASE/'build_revision.py')
    old=importlib.util.module_from_spec(spec);spec.loader.exec_module(old)
    inventory=old.sources(BASE)
    require(len(inventory)==438,'unexpected predecessor native inventory')
    ROOT.mkdir(parents=True)
    for name in inventory:
        dest=ROOT/safe(name);dest.parent.mkdir(parents=True,exist_ok=True)
        shutil.copy2(BASE/name,dest)
    for name in CHANGED:
        dest=ROOT/'predecessor-v81-audit'/name;dest.parent.mkdir(parents=True,exist_ok=True)
        shutil.copy2(BASE/name,dest)
    graphs={}
    for entry in ['quantitative.tex','structural.tex','main.tex']:
        files,labels=old.graph(BASE,entry)
        graphs[entry]={'files':sorted(files),'labels':sorted(labels)}
    baseline={'schema':'gtf82.predecessor/1','commit':BASE_COMMIT,
      'native_commit':'ed70f20a5d1b54a73cb5cd2e50d334c1cc3b357d',
      'files':inventory,'graphs':graphs,'changed_predecessor_paths':CHANGED,
      'originals':'predecessor-v81-audit/',
      'structural_pdf_sha256':digest((BASE/'STRUCTURAL_PAPER.pdf').read_bytes()),
      'structural_signature':old.pdf_signature(BASE/'STRUCTURAL_PAPER.pdf')}
    (ROOT/'V81_BASELINE.json').write_text(json.dumps(baseline,indent=2,sort_keys=True)+'\n')
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
        encoded=text.encode('utf-8')
        require(digest(encoded)==item['result_sha256'],'expanded native hash mismatch: '+name)
        path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(encoded)
    final=old.sources(ROOT)
    require(len(final)==465,'unexpected v82 native inventory')
    prefix=ROOT.relative_to(REPO).as_posix()+'/'
    subprocess.run(['git','add','--',*[prefix+n for n in final]],cwd=REPO,check=True)
    staged=set(git('diff','--cached','--name-only').splitlines())
    require(staged=={prefix+n for n in final},'staging includes unrelated or missing files')
    print(json.dumps({'schema':'gtf82.staging/1','status':'success',
      'predecessor_commit':BASE_COMMIT,'transport_sha256':DELTA_SHA,
      'native_files':len(final),'expanded_delta_files':len(delta)},indent=2))

if __name__=='__main__':main()
