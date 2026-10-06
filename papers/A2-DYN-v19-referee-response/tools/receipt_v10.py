#!/usr/bin/env python3
"""Describe exactly what was built; never infer mathematical acceptance."""
from pathlib import Path
import hashlib,json,os,subprocess
p=Path(__file__).resolve().parents[1]
def sha(f):return hashlib.sha256(f.read_bytes()).hexdigest()
try:
    head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=p,text=True,stderr=subprocess.DEVNULL).strip()
    dirty=bool(subprocess.check_output(['git','status','--porcelain','--',str(p)],cwd=p,text=True).strip())
except subprocess.CalledProcessError:
    head=None;dirty=None
event=os.environ.get('GITHUB_SHA')
if event and (head!=event or dirty):
    raise RuntimeError('CI source is not the clean exact event commit')
print(json.dumps({'revision':10,'head_sha':head,'event_sha':event,'dirty_scoped_source':dirty,
  'native_build_passed':True,'validation_scope':'source, finite algebra, native typesetting; not a continuum proof certificate','tex_sha256':{str(f.relative_to(p)):sha(f) for f in sorted(p.rglob('*.tex'))},
  'pdf_sha256':sha(p/'build/main.pdf'),
  'mathematical_completion_certified':False,'full_raw_LLT_verified':False,
  'independent_human_review':False},indent=2,sort_keys=True))
