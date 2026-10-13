#!/usr/bin/env python3
"""Record the exact executed source and native output; never certify mathematics."""
from pathlib import Path
import hashlib,json,os,subprocess
from verify_v19 import tree_hash
root=Path(__file__).resolve().parents[1]
def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def git(*args):return subprocess.check_output(['git',*args],cwd=root,text=True,stderr=subprocess.DEVNULL).strip()
event=os.environ.get('GITHUB_SHA')
try:
    head=git('rev-parse','HEAD');dirty=bool(git('status','--porcelain','--',str(root)))
except (subprocess.CalledProcessError,FileNotFoundError):
    head=None;dirty=None
if event and (head!=event or dirty is not False):raise RuntimeError('not the exact clean event source')
checks=json.loads((root/'evidence/v19-source-and-finite-checks.json').read_text())
if checks['revision']!=19:raise RuntimeError('wrong diagnostic revision')
receipt={'revision':19,'head_sha':head,'event_sha':event,
 'workflow_run_id':os.environ.get('GITHUB_RUN_ID'),'workflow_run_attempt':os.environ.get('GITHUB_RUN_ATTEMPT'),
 'execution_environment':'GitHub Actions' if event else 'local source directory',
 'dirty_scoped_source':dirty,'ordinary_paper_tree':tree_hash(root).hex(),'native_build_passed':True,
 'pdf_sha256':digest(root/'build/main.pdf'),'tex_log_sha256':digest(root/'build/main.log'),
 'source_manifest_sha256':digest(root/'SOURCE_MANIFEST.json'),
 'source_checks_sha256':digest(root/'evidence/v19-source-and-finite-checks.json'),
 'source_counts':{k:v for k,v in checks['source'].items() if k!='source_sha256'},
 'verified_source_hashes':checks['source']['source_sha256'],
 'validation_scope':'exact source, finite regression models and native typesetting, not continuum proof certification',
 'full_raw_LLT_verified':False,'independent_human_review':False}
archive=root/'evidence/exact-source.tar'
if archive.exists():receipt['source_archive_sha256']=digest(archive)
print(json.dumps(receipt,indent=2,sort_keys=True))
