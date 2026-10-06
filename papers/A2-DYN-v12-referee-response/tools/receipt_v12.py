#!/usr/bin/env python3
from pathlib import Path
import hashlib,json,os,subprocess
p=Path(__file__).resolve().parents[1]
def sha(f): return hashlib.sha256(f.read_bytes()).hexdigest()
head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=p,text=True).strip()
dirty=bool(subprocess.check_output(['git','status','--porcelain','--',str(p)],cwd=p,text=True).strip())
event=os.environ.get('GITHUB_SHA')
if event and (head!=event or dirty): raise RuntimeError('not exact clean event source')
print(json.dumps({'revision':12,'head_sha':head,'event_sha':event,'workflow_run_id':os.environ.get('GITHUB_RUN_ID'),'workflow_run_attempt':os.environ.get('GITHUB_RUN_ATTEMPT'),'dirty_scoped_source':dirty,
 'native_build_passed':True,'pdf_sha256':sha(p/'build/main.pdf'),
 'validation_scope':'source, finite algebra and native typesetting; not proof certification',
 'full_raw_LLT_verified':False,'independent_human_review':False},indent=2,sort_keys=True))
