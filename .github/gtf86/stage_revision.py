#!/usr/bin/env python3
"""Reconstruct only the new v86 native directory from immutable v85 and a checked delta.

No previous manuscript, review report, workflow, or remote ref is changed here.
The complete source graph is verified separately by the new native builder.
"""
from pathlib import Path
import base64,hashlib,importlib.util,json,lzma,shutil,subprocess

REPO=Path(__file__).resolve().parents[2]
BASE=REPO/'papers/GTF-I-v85-smooth-boundary-geometry'
ROOT=REPO/'papers/GTF-I-v86-one-sided-boundary-geometry'
PREDECESSOR='ca39533970c77a156cafe916ee6287c54c91fa00'
DELTA_SHA='4de0c3e20345550d537054ec21216425f463d5408008f3a1d773be24f1e98b10'
PARTS=3
EXPECTED_FILES=600
REPORTS={
 'FROZEN_R55_REPORT.md':('107182f19e0534ae99cd68fc10cd71dddd1563a7','GENERAL_THETA_FOUNDATIONS_I_V85_REFEREE_REPORT_R55.md','80f18213230fd0851a885be945d65f4da3a872d7a98a1b48861b28567e0c8c86'),
 'FROZEN_R55_PIPELINE_AUDIT.md':('7dc5d76ace1aa993c946770e0b5b2d8b853e5419','GENERAL_THETA_FOUNDATIONS_I_V85_PROOF_PIPELINE_AUDIT_R55.md','daa40a25b93f8e916037069075bfe1a8dc2791175183fffaacf118438dc3113c')}

def require(value,message):
    if not value:raise RuntimeError(message)

def digest(data):return hashlib.sha256(data).hexdigest()

def safe(name):
    require(isinstance(name,str),'path must be text')
    p=Path(name)
    require(not p.is_absolute() and '..' not in p.parts and p.as_posix()==name,'unsafe path')
    return p

def native(root):
    result={}
    for p in sorted(root.rglob('*')):
        rel=p.relative_to(root)
        if not p.is_file() or any(x in {'build','evidence','__pycache__','.git'} for x in rel.parts):continue
        if p.suffix.lower() in {'.tex','.py','.json','.md','.txt'}:result[rel.as_posix()]=digest(p.read_bytes())
    return result

def git(*args):return subprocess.check_output(['git',*args],cwd=REPO,text=True).strip()

def main():
    require(not ROOT.exists(),'refusing to replace an existing revision directory')
    require(git('diff','--name-only',PREDECESSOR,'HEAD','--',str(BASE.relative_to(REPO)))=='','predecessor changed')
    packed=''.join((REPO/'.github/gtf86'/('delta.part'+str(i))).read_text().strip() for i in range(PARTS))
    compressed=base64.b64decode(packed,validate=True)
    require(digest(compressed)==DELTA_SHA,'transport digest mismatch')
    delta=json.loads(lzma.decompress(compressed))
    require(delta['schema']=='gtf86.native-delta/1','unexpected delta schema')
    require(delta['base_commit']==PREDECESSOR,'unexpected delta baseline')
    inventory=native(BASE)
    require(len(inventory)==565 and inventory==json.loads((BASE/'evidence/SOURCE_HASHES.json').read_text()),'immutable predecessor inventory mismatch')
    spec=importlib.util.spec_from_file_location('v85_reference_builder',BASE/'build_revision.py')
    old=importlib.util.module_from_spec(spec);spec.loader.exec_module(old)
    graphs={}
    for entry in old.DOCS:
        files,labels=old.graph(BASE,entry);graphs[entry]={'files':sorted(files),'labels':sorted(labels)}
    prior_signature=json.loads((BASE/'evidence/PAGE_CHECKS.json').read_text())['STRUCTURAL_PAPER.pdf']
    baseline={'schema':'gtf86.predecessor/1','commit':PREDECESSOR,
      'native_commit':'81e17daffff86fe0ac1762f06a4785eb9c4339bc','files':inventory,'graphs':graphs,
      'changed_predecessor_paths':delta['changed_predecessor_paths'],'originals':'predecessor-v85-audit/',
      'structural_pdf_sha256':digest((BASE/'STRUCTURAL_PAPER.pdf').read_bytes()),
      'structural_signature':{k:v for k,v in prior_signature.items() if k!='sha256'}}
    baseline_bytes=(json.dumps(baseline,indent=2,sort_keys=True)+'\n').encode('utf-8')
    require(digest(baseline_bytes)==delta['baseline_sha256'],'reconstructed baseline differs')
    ROOT.mkdir(parents=True)
    (ROOT/'V85_BASELINE.json').write_bytes(baseline_bytes)
    for name in inventory:
        target=ROOT/safe(name);target.parent.mkdir(parents=True,exist_ok=True)
        shutil.copy2(BASE/name,target)
    for name in baseline['changed_predecessor_paths']:
        target=ROOT/'predecessor-v85-audit'/safe(name);target.parent.mkdir(parents=True,exist_ok=True)
        shutil.copy2(BASE/name,target)
    for name,(commit,path,expected) in REPORTS.items():
        data=subprocess.check_output(['git','show',commit+':'+path],cwd=REPO)
        require(digest(data)==expected,'frozen report mismatch')
        (ROOT/name).write_bytes(data)
    for name,item in delta['files'].items():
        target=ROOT/safe(name)
        if 'text' in item:output=item['text']
        else:
            base=(BASE/safe(item['base'])).read_bytes()
            require(digest(base)==item['base_sha256'],'base hash mismatch: '+name)
            lines=base.decode('utf-8').splitlines(keepends=True)
            chunks=[]
            for operation in item['ops']:
                if isinstance(operation,str):chunks.append(operation)
                else:
                    require(isinstance(operation,list) and len(operation)==2 and all(type(x) is int for x in operation) and 0<=operation[0]<=operation[1]<=len(lines),'invalid line-copy operation')
                    chunks.append(''.join(lines[operation[0]:operation[1]]))
            output=''.join(chunks)
        data=output.encode('utf-8')
        require(digest(data)==item['result_sha256'],'expanded hash mismatch: '+name)
        target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(data)
    final=native(ROOT)
    require(len(final)==EXPECTED_FILES and digest(json.dumps(final,sort_keys=True,separators=(',',':')).encode())==delta['final_inventory_sha256'],'expanded complete native inventory differs')
    prefix=ROOT.relative_to(REPO).as_posix()+'/'
    subprocess.run(['git','add','--',*[prefix+n for n in final]],cwd=REPO,check=True)
    require(set(git('diff','--cached','--name-only').splitlines())=={prefix+n for n in final},'unrelated staged paths')
    print(json.dumps({'schema':'gtf86.staging/1','status':'success','base_commit':PREDECESSOR,'native_files':len(final),'delta_sha256':DELTA_SHA,'delta_files':len(delta['files']),'previous_manuscripts_changed':False},indent=2))

if __name__=='__main__':main()
