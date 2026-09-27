"""Read-only verification of an exact publication head. Outputs only to a separate directory."""
from __future__ import annotations
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import zipfile

HOME=Path(__file__).resolve().parent
REQUEST='GENERAL_THETA_FOUNDATIONS_I_V59_FINAL_HEAD_REQUEST.json'

def require(ok,msg):
    if not ok:raise RuntimeError(msg)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text())
def git(root,*args):return subprocess.check_output(['git','-C',str(root),*args],text=True).strip()
def main():
    parser=argparse.ArgumentParser();parser.add_argument('--output-dir',type=Path,required=True);args=parser.parse_args()
    root=HOME.parents[1];out=args.output_dir.resolve()
    require(not out.is_relative_to(root),'Attestation output must be outside the repository')
    out.mkdir(parents=True,exist_ok=True)
    head=git(root,'rev-parse','HEAD')
    require(re.fullmatch('[0-9a-f]{40}',head) is not None,'Invalid HEAD identity')
    require(head==os.environ.get('GITHUB_SHA'),'Checkout is not the triggering final SHA')
    request=read(root/REQUEST)
    require(request['schema']=='gtf59.final-head-request/1','Invalid final-head request')
    candidate=request['candidate_publication'];source=request['source_commit']
    require(all(isinstance(x,str) and re.fullmatch('[0-9a-f]{40}',x) for x in [candidate,source]),'Invalid pinned commit identifiers')
    require(git(root,'rev-parse','HEAD^')==candidate,'Request is not a direct publication successor')
    require(git(root,'rev-parse',candidate+'^')==source,'Publication is not a direct native-source successor')
    require(git(root,'diff','--name-only',candidate,head)==REQUEST,'Request commit changed more than provenance')
    require(not git(root,'status','--porcelain','--untracked-files=no'),'Tracked checkout is dirty')
    ev=HOME/'evidence';receipt=read(ev/'BUILD_RECEIPT.json');hashes=read(ev/'SOURCE_HASHES.json')
    require(receipt['status']=='success' and receipt['source_commit']==source,'Invalid source-bound receipt')
    require(receipt['workflow_run']==str(request['builder_run']),'Builder identity mismatch')
    require(receipt['isolated_rebuild']['status']=='success','Original isolated build was not successful')
    require(sha(ev/'CORE_SOURCES.zip')==receipt['core_archive_sha256'],'Native archive hash mismatch')
    for name,digest in hashes.items():require(sha(HOME/name)==digest,'Committed native file mismatch: '+name)
    pdf_hashes={}
    for info in receipt['documents'].values():
        pdf_hashes[info['filename']]=sha(HOME/info['filename'])
        require(pdf_hashes[info['filename']]==info['sha256'],'Committed PDF digest mismatch')
    examples=read(ev/'COMPILER_CLI_RECEIPT.json')
    for name,info in examples.items():require(sha(ev/(name+'.json'))==info['sha256'],'Committed compiler output mismatch')
    with tempfile.TemporaryDirectory(prefix='gtf59-final-native-') as temp:
        temp=Path(temp)
        with zipfile.ZipFile(ev/'CORE_SOURCES.zip') as archive:
            expected={HOME.name+'/'+name for name in hashes}
            require(set(archive.namelist())==expected and len(archive.namelist())==len(expected),'Archive does not contain exactly the native inventory')
            for item in archive.infolist():
                p=Path(item.filename)
                require(not p.is_absolute() and '..' not in p.parts,'Unsafe archive member')
                data=archive.read(item)
                require(hashlib.sha256(data).hexdigest()==hashes[str(p.relative_to(HOME.name))],'Native archive bytes differ')
                target=temp/p;target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(data)
        other=temp/HOME.name;env=os.environ.copy()
        env.update(GTF_SOURCE_COMMIT=source,PYTHONDONTWRITEBYTECODE='1')
        result=subprocess.run([sys.executable,'build.py','--isolated'],cwd=other,env=env,
                              capture_output=True,text=True,timeout=1600)
        (out/'NATIVE_REBUILD_LOG.txt').write_text(result.stdout+'\n'+result.stderr)
        require(result.returncode==0,'Read-only native rebuild failed; see log')
        require(read(other/'evidence/SOURCE_HASHES.json')==hashes,'Rebuilt native identities differ')
        require(read(other/'evidence/PAGE_CHECKS.json')==read(ev/'PAGE_CHECKS.json'),'Rebuilt page text/raster differs')
        require(read(other/'evidence/COMPILER_CLI_RECEIPT.json')==examples,'Rebuilt generic compiler outputs differ')
        require(read(other/'evidence/V59_CHECKS.json')==read(ev/'V59_CHECKS.json'),'Finite regression results differ')
        require(read(other/'evidence/BUILD_RECEIPT.json')['status']=='success','Rebuild was only a preflight')
    require(not git(root,'status','--porcelain','--untracked-files=no'),'Verifier altered tracked repository files')
    attestation={'schema':'gtf59.final-head-attestation/1','status':'success','final_head_sha':head,
                 'candidate_publication':candidate,'source_commit':source,'builder_run':request['builder_run'],
                 'verifier_run':os.environ.get('GITHUB_RUN_ID'),'verifier_attempt':os.environ.get('GITHUB_RUN_ATTEMPT'),
                 'repository_permissions':'contents: read','repository_writes':False,'native_file_count':len(hashes),
                 'all_page_text_and_raster_equal':True,'all_compiler_outputs_equal':True,'all_regressions_reexecuted':True,
                 'native_archive_sha256':sha(ev/'CORE_SOURCES.zip'),'pdf_sha256':pdf_hashes,'compiler_examples':examples,
                 'not_certified':['universal mathematical proofs','independent priority','cryptographic author signature','journal acceptance','A/B/C/D analytic closure']}
    (out/'FINAL_HEAD_ATTESTATION.json').write_text(json.dumps(attestation,indent=2,sort_keys=True)+'\n')
    print(json.dumps(attestation,indent=2,sort_keys=True))
if __name__=='__main__':main()
