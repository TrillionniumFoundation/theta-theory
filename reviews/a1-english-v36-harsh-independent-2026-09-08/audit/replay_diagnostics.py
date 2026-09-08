#!/usr/bin/env python3
"""Replay source-pinned diagnostics, recording current executions separately.

Requires Python 3.10+, sympy, mpmath and the native v36 source directory.
The optional previous-review directory supplies the independent v35 test.
Historical JSON schema/commit fields are deliberately left unchanged.
"""
from __future__ import annotations
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import subprocess
import sys

COMMIT='8f074b8027627a71a81a362b9d15f47975e1f3ae'

def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def blob(path: Path) -> str:
    data=path.read_bytes()
    return hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()

def require(ok: bool, message: str) -> None:
    if not ok:
        raise RuntimeError(message)

def main() -> None:
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--source-root',required=True,type=Path)
    ap.add_argument('--previous-review',type=Path)
    ap.add_argument('--output-root',required=True,type=Path)
    args=ap.parse_args()
    root=args.source_root.resolve();out=args.output_root.resolve();out.mkdir(parents=True,exist_ok=True)
    manifest=root/'verification-v36/EXECUTION_RECORD.json'
    require(blob(manifest)=='48bd7a55894b749ed3801585ef225ec9676c79fe','Execution-manifest Git identity')
    record=json.loads(manifest.read_text())
    jobs=[(root/x['program'],x['program_git_blob'],x['output_sha256'],x['output_file'])
          for x in record['executed_programs']]
    if args.previous_review:
        prev=args.previous_review.resolve()
        expected=digest((prev/'audit/INDEPENDENT_V35_CHECKS.json').read_bytes())
        jobs.append((prev/'audit/independent_v35_checks.py','e06fb129364e549bd6ff99577783346d69be0516',expected,'V35_REFEREE_REPLAY.json'))
    executions=[]
    for path,git_sha,expected,name in jobs:
        require(blob(path)==git_sha,'Script Git identity: '+str(path))
        outputs=[]
        for optimized in (False,True):
            command=[sys.executable]+(['-O'] if optimized else [])+[str(path)]
            started=datetime.now(timezone.utc).isoformat()
            proc=subprocess.run(command,capture_output=True,timeout=90)
            require(proc.returncode==0,'Failed program: '+str(path)+' '+proc.stderr.decode(errors='replace'))
            outputs.append(proc.stdout)
            executions.append({'program':path.name,'git_blob':git_sha,
                'program_sha256':digest(path.read_bytes()),'optimized':optimized,
                'started_utc':started,'finished_utc':datetime.now(timezone.utc).isoformat(),
                'returncode':proc.returncode,'output_sha256':digest(proc.stdout),
                'matches_published_output':digest(proc.stdout)==expected})
        require(outputs[0]==outputs[1],'Normal/optimized difference: '+path.name)
        require(digest(outputs[0])==expected,'Historical replay mismatch: '+path.name)
        (out/name).write_bytes(outputs[0])
    result={'schema':'a1-v36-referee-diagnostic-replay-v1','reviewed_commit':COMMIT,
        'python_version':sys.version,'programs_replayed':len(jobs),
        'all_normal_optimized_outputs_identical':True,'all_published_outputs_reproduced':True,
        'executions':executions,
        'limits':['No general theorem proof is certified by these tests.',
                  'High-precision SVD is diagnostic, not a directed interval proof.',
                  'No global multistage controller optimization was performed.',
                  'Historical schema and reviewed_commit fields inside unmodified outputs retain their original meaning.']}
    (out/'REPLAY_RECEIPT.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'programs':len(jobs),'successful_executions':len(executions),'all_outputs_match':True},indent=2))

if __name__=='__main__':
    main()
