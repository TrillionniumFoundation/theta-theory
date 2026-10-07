#!/usr/bin/env python3
"""Dynamic exact-source execution receipt. No success is predeclared in source."""
from pathlib import Path
import hashlib,json,os,subprocess
import verify_v31 as verifier
root=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
try:
    head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=root,text=True,stderr=subprocess.DEVNULL).strip()
    dirty=bool(subprocess.check_output(['git','status','--porcelain','--',str(root)],cwd=root,text=True).strip())
except subprocess.CalledProcessError:
    head=None;dirty=None
run=os.environ.get('GITHUB_RUN_ID');event=os.environ.get('GITHUB_SHA')
if os.environ.get('GITHUB_ACTIONS') and (not event or not run or head!=event or dirty is not False):
    raise RuntimeError('not a clean exact-SHA GitHub execution')
checks=json.loads((root/'evidence/v31-source-and-finite-checks.json').read_text())
print(json.dumps({'revision':31,'head_sha':head,'event_sha':event,'workflow_run_id':run,
 'workflow_run_attempt':os.environ.get('GITHUB_RUN_ATTEMPT'),
 'execution_environment':'GitHub Actions' if os.environ.get('GITHUB_ACTIONS') else 'local source validation',
 'dirty_scoped_source':dirty,'native_build_passed':True,'pdf_sha256':sha(root/'build/main.pdf'),
 'tex_log_sha256':sha(root/'build/main.log'),'ordinary_paper_tree':verifier.tree_hash(root).hex(),
 'source_manifest_sha256':sha(root/'SOURCE_MANIFEST.json'),
 'source_checks_sha256':sha(root/'evidence/v31-source-and-finite-checks.json'),
 'verified_source_hashes':checks['source']['source_sha256'],
 'controlling_report_verified':checks['source']['controlling_report_verified'],
 'qualification_workflow_sha256':checks['source']['qualification_workflow_sha256'],
 'continuum_proof_certified':False,'full_raw_LLT_certified':False,'independent_human_review':False},indent=2,sort_keys=True))
