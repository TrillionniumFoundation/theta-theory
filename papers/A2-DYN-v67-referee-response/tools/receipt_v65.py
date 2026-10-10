#!/usr/bin/env python3
"""Dynamic receipt only after strict verification and native build."""
from pathlib import Path
import hashlib,json,os,subprocess
import verify_v65 as verifier
root=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
checks=json.loads((root/'evidence/v65-source-and-finite-checks.json').read_text())
qualified=(not checks['source']['local_preflight'] and all(checks['source']['frozen_reports_verified'].values()))
if os.environ.get('GITHUB_ACTIONS') and not qualified:
    raise RuntimeError('preflight is not qualification')
try:
    head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=root,text=True,stderr=subprocess.DEVNULL).strip()
    dirty=bool(subprocess.check_output(['git','status','--porcelain','--',str(root),str(root.parents[1]/verifier.WORKFLOW)],cwd=root,text=True).strip())
except subprocess.CalledProcessError:
    head=None;dirty=None
run=os.environ.get('GITHUB_RUN_ID');event=os.environ.get('GITHUB_SHA')
actual_tree=verifier.tree_hash(root).hex();committed_tree=None
if os.environ.get('GITHUB_ACTIONS'):
    if not event or not run or head!=event or dirty is not False:
        raise RuntimeError('not a clean exact event execution')
    committed_tree=subprocess.check_output(['git','rev-parse',head+':papers/A2-DYN-v65-referee-response'],cwd=root,text=True).strip()
    if actual_tree!=committed_tree:raise RuntimeError('working article differs from committed tree')
print(json.dumps({'revision':65,'head_sha':head,'event_sha':event,'workflow_run_id':run,
 'workflow_run_attempt':os.environ.get('GITHUB_RUN_ATTEMPT'),
 'execution_environment':'GitHub Actions' if os.environ.get('GITHUB_ACTIONS') else 'local preparation',
 'source_qualified':qualified,
 'dirty_scoped_source':dirty,'native_build_passed':True,'pdf_sha256':sha(root/'build/main.pdf'),
 'tex_log_sha256':sha(root/'build/main.log'),'ordinary_paper_tree':actual_tree,'committed_paper_tree':committed_tree,
 'source_manifest_sha256':sha(root/'SOURCE_MANIFEST.json'),
 'source_checks_sha256':sha(root/'evidence/v65-source-and-finite-checks.json'),
 'verified_source_hashes':checks['source']['source_sha256'],
 'frozen_reports_verified':checks['source']['frozen_reports_verified'],
 'qualification_workflow_sha256':checks['source']['qualification_workflow_sha256'],
 'continuum_proof_certified':False,'full_raw_LLT_certified':False,'independent_human_review':False},indent=2,sort_keys=True))
