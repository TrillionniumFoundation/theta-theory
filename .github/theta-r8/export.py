#!/usr/bin/env python3
"""Export committed source/artifacts with per-file Git and SHA-256 bindings."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
from materialize import PAPER, NEW_NAME, OLD_NAME, CONTROLS, TREES, EXPECTED, require, blob

root=Path(__file__).resolve().parents[2]
out=Path(sys.argv[1]).resolve();out.mkdir(parents=True,exist_ok=True)
def git(*args):return subprocess.check_output(['git',*args],cwd=root)
source=os.environ['SOURCE_COMMIT'];artifact=git('rev-parse','HEAD').decode().strip()
require(git('rev-parse','HEAD^').decode().strip()==source,'artifact parent is not source')
paths=set(CONTROLS)
for name in [NEW_NAME,OLD_NAME,'r6-operational-transfer']:
 base=PAPER/name
 manifest=json.loads(git('show',artifact+':'+str(base/'SOURCE_MANIFEST.json')))
 paths.update(str(base/p) for p in manifest['files'])
 paths.add(str(base/'SOURCE_MANIFEST.json'))
for prefix in [PAPER/NEW_NAME/'artifacts',PAPER/NEW_NAME/'evidence',PAPER/'review-inputs',Path('.github/theta-r8')]:
 paths.update(git('ls-tree','-r','--name-only',artifact,'--',str(prefix)).decode().splitlines())
paths.add('.github/workflows/general-theta-restart-r8.yml')
index={}
for path in sorted(paths):
 data=git('show',artifact+':'+path)
 expected=git('rev-parse',artifact+':'+path).decode().strip()
 require(blob(data)==expected,'export blob mismatch')
 dest=out/path;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(data)
 index[path]={'git_blob_sha':expected,'sha256':hashlib.sha256(data).hexdigest(),'bytes':len(data)}
raw_commits={}
for commit in [source,artifact,os.environ['BOOTSTRAP_COMMIT']]:
 raw=git('cat-file','commit',commit)
 digest=hashlib.sha1(b'commit '+str(len(raw)).encode()+b'\0'+raw).hexdigest()
 require(digest==commit,'raw commit object mismatch')
 raw_commits[commit]=raw.decode()
unchanged={name:git('rev-parse',artifact+':'+str(PAPER/name)).decode().strip() for name in TREES}
require(unchanged==TREES,'historical tree changed')
binding={'status':'PASS','source_commit':source,'artifact_commit':artifact,
 'source_tree':EXPECTED,'bootstrap_commit':os.environ['BOOTSTRAP_COMMIT'],
 'hosted_run_id':os.environ['GITHUB_RUN_ID'],'unchanged_historical_trees':unchanged,
 'raw_commit_objects':raw_commits,'files':index,
 'scope':'Complete R8 and full submitted R6 supplement; R7 source provenance. Not a proof certificate or a full repository build.'}
(out/'EXPORT_INDEX.json').write_text(json.dumps(binding,sort_keys=True,indent=2)+'\n')
print(json.dumps({k:v for k,v in binding.items() if k not in ['files','raw_commit_objects']},indent=2))
