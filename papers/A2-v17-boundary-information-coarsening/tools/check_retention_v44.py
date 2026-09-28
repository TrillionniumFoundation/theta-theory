#!/usr/bin/env python3
"""Reproduce the ignore-rule defect and verify the actual retention helper."""
from pathlib import Path
import argparse,os,tempfile,subprocess,json
from retain_native_v44 import prepare,verify
from source_provenance import require
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--evidence',required=True,type=Path)
args=parser.parse_args()
evidence=args.evidence.resolve()
source=json.loads((evidence/'build-report.json').read_text())['source_commit']
with tempfile.TemporaryDirectory() as tmp:
 os.chdir(tmp)
 def run(*args):return subprocess.run(['git',*args],check=True,capture_output=True)
 run('init','-q');run('config','user.name','Local diagnostic');run('config','user.email','local@example.invalid')
 Path('.gitignore').write_text('*.pdf\n*.aux\n*.log\n*.fls\n*.out\n*.toc\n*.fdb_latexmk\n')
 dest=Path('deliveries/a2-v43-repaired')/source
 receipt=prepare(evidence,dest,dest.name,'local')
 run('add','--','.')
 failed=False
 try:verify(dest,'INDEX')
 except RuntimeError as exc:
  failed=True; require('main.pdf' in str(exc) and 'two_collision.pdf' in str(exc),'Wrong negative control')
 require(failed,'Ordinary staging falsely passed')
 missing=[]
 for name in receipt['files']:
  if subprocess.run(['git','cat-file','-e',':'+str(dest/name)],capture_output=True).returncode:missing.append(name)
 require(len(missing)==13,'Expected 13 omitted files')
 run('add','-f','--',str(dest));verify(dest,'INDEX');run('commit','-qm','native files')
 result=verify(dest,'HEAD')
 (dest/'main.pdf').unlink()
 require(verify(dest,'HEAD')['status']=='passed','Verification incorrectly read working-tree file')
 print(json.dumps({'status':'passed','plain_add_missing_files':missing,'force_add_verified_files':result['verified_file_count'],'committed_object_independent_of_working_tree':True,'mathematical_certification':False},sort_keys=True,indent=2))
