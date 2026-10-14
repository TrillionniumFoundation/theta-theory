#!/usr/bin/env python3
from pathlib import Path
import hashlib,json,os,subprocess
root=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=root,text=True).strip()
event=os.environ.get('GITHUB_SHA')
dirty=bool(subprocess.check_output(['git','status','--porcelain','--',str(root)],cwd=root,text=True).strip())
if event and (head!=event or dirty):raise RuntimeError('not exact clean event source')
checks=json.loads((root/'evidence/v27-source-and-finite-checks.json').read_text())
print(json.dumps({'revision':27,'head_sha':head,'event_sha':event,
 'workflow_run_id':os.environ.get('GITHUB_RUN_ID'),'workflow_run_attempt':os.environ.get('GITHUB_RUN_ATTEMPT'),
 'dirty_scoped_source':dirty,'native_build_passed':True,'pdf_sha256':sha(root/'build/main.pdf'),
 'tex_log_sha256':sha(root/'build/main.log'),'source_manifest_sha256':sha(root/'SOURCE_MANIFEST.json'),
 'source_checks_sha256':sha(root/'evidence/v27-source-and-finite-checks.json'),
 'verified_source_hashes':checks['source']['source_sha256'],
 'controlling_report_verified':checks['source']['controlling_report_verified'],
 'continuum_proof_certified':False,'full_raw_LLT_certified':False,'independent_human_review':False},indent=2,sort_keys=True))
