#!/usr/bin/env python3
"""Freeze authoritative source and retained evidence, excluding derived current outputs.
Run deliberately before qualification, not to suppress any missing-source error.
"""
from pathlib import Path
import hashlib,json
P=Path(__file__).resolve().parents[1]
EXCLUDED_PREFIXES=('build/','evidence/current-execution/','provenance/current-transport/','delivery/')
EXCLUDED_FILES={'SOURCE_MANIFEST.json','PROOF_INDEX.json'}
files=[]
for f in sorted(P.rglob('*')):
    if not f.is_file():continue
    rel=str(f.relative_to(P))
    if rel in EXCLUDED_FILES or rel.startswith(EXCLUDED_PREFIXES) or '__pycache__' in f.parts or '.git' in f.parts:continue
    d=f.read_bytes()
    files.append({'path':rel,'bytes':len(d),'sha256':hashlib.sha256(d).hexdigest(),
                  'git_blob':hashlib.sha1(b'blob '+str(len(d)).encode()+b'\0'+d).hexdigest()})
manifest={'schema':'a2-dyn-summable-physical-source-v1','files':files,'file_count':len(files),
          'model':'original triangular Lorentz gas, R=[9/20,47/100], actual clock and all exact labels unchanged',
          'native_core_range':[260,303],'new_native_modules':[302,303],
          'full_raw_pointwise_LLT_proved':False,'four_coordinate_inversion_completed':False,
          'all_historical_proofs_independently_reconstructed':False,
          'excluded_derived_output_prefixes':EXCLUDED_PREFIXES,'excluded_self_or_derived_files':sorted(EXCLUDED_FILES),
          'remote_commit_for_new_revision':None,
          'identity_scope':'all authoritative current source, unchanged/frozen predecessors and retained historical evidence; current command receipts are derived separately'}
(P/'SOURCE_MANIFEST.json').write_text(json.dumps(manifest,indent=2,sort_keys=True)+'\n')
print(json.dumps({'files':len(files),'manifest_sha256':hashlib.sha256((P/'SOURCE_MANIFEST.json').read_bytes()).hexdigest()},indent=2))
