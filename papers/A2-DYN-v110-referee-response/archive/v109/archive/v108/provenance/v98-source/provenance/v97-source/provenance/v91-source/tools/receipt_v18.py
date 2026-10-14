#!/usr/bin/env python3
"""Emit a dynamic receipt for the exact checked-out source, never a proof certificate."""
from pathlib import Path
import hashlib
import json
import os
import subprocess

root = Path(__file__).resolve().parents[1]

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

head = subprocess.check_output(['git','rev-parse','HEAD'], cwd=root, text=True).strip()
event = os.environ.get('GITHUB_SHA')
status = subprocess.check_output(['git','status','--porcelain','--',str(root)], cwd=root, text=True)
dirty = bool(status.strip())
if event and (event != head or dirty):
    raise RuntimeError('not the exact clean event source')
checks = json.loads((root/'evidence/v18-source-and-finite-checks.json').read_text())
print(json.dumps({'revision':18,'head_sha':head,'event_sha':event,
 'workflow_run_id':os.environ.get('GITHUB_RUN_ID'),
 'workflow_run_attempt':os.environ.get('GITHUB_RUN_ATTEMPT'),
 'execution_environment':'GitHub Actions' if event else 'local checkout',
 'dirty_scoped_source':dirty,'native_build_passed':True,
 'pdf_sha256':sha(root/'build/main.pdf'),
 'tex_log_sha256':sha(root/'build/main.log'),
 'source_manifest_sha256':sha(root/'SOURCE_MANIFEST.json'),
 'source_checks_sha256':sha(root/'evidence/v18-source-and-finite-checks.json'),
 'verified_source_hashes':checks['source']['source_sha256'],
 'validation_scope':'source identity, finite diagnostics, native typesetting; not continuum proof certification',
 'full_raw_LLT_verified':False,'independent_human_review':False},indent=2,sort_keys=True))
