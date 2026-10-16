#!/usr/bin/env python3
"""Fail-closed byte identity and status-scope checks; not proof certification."""
from pathlib import Path
import hashlib
import json
ROOT=Path(__file__).resolve().parents[1]
def require(ok,message):
    if not ok: raise RuntimeError(message)
def blob(data):
    return hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
def sha(data): return hashlib.sha256(data).hexdigest()
def check():
    m=json.loads((ROOT/'SOURCE_MANIFEST.json').read_text())
    for name,expected in m['active_blobs'].items():
        require(blob((ROOT/name).read_bytes())==expected,'changed active bytes: '+name)
    for name,expected in m.get('preserved_v114_files',{}).items():
        require(sha((ROOT/'provenance/v114-frozen'/name).read_bytes())==expected,'changed v114 frozen bytes: '+name)
    for name,expected in m['preserved_v112_files'].items():
        require(sha((ROOT/'provenance/v112-active'/name).read_bytes())==expected,'changed v112 bytes: '+name)
    original=json.loads((ROOT/'provenance/v112-active/SOURCE_MANIFEST.json').read_text())
    for name,expected in original['active_blobs'].items():
        require(blob((ROOT/'provenance/v112-active'/name).read_bytes())==expected,'v112 Git blob mismatch: '+name)
    for name,expected in m['preserved_clearance_flux_files'].items():
        require(sha((ROOT/'provenance/clearance-flux-active'/name).read_bytes())==expected,'changed clearance-flux provenance: '+name)
    for name,expected in m['retained_active_proof_blobs'].items():
        require(blob((ROOT/name).read_bytes())==expected,'changed retained active proof: '+name)
    for name,expected in m['retained_model_blobs'].items():
        require(blob((ROOT/name).read_bytes())==expected,'changed physical model/interface: '+name)
    for name,expected in m['retained_provenance_blobs'].items():
        require(blob((ROOT/'provenance'/name).read_bytes())==expected,'changed retained anchor/report: '+name)
    for key in ['full_raw_return_LLT_proved','primary_referee_request_closed','remote_push_completed',
                'full_historical_archive_locally_reconstructed','independent_human_review',
                'full_capacity_abundance_proved','uniform_normalized_clearance_chart_sum_proved']:
        require(m['claims'][key] is False,'unsupported completion: '+key)
    return {'status':'passed','active_blob_count':len(m['active_blobs']),
            'preserved_v112_file_count':len(m['preserved_v112_files']),
            'verified_original_v112_active_Git_blobs':len(original['active_blobs']),
            'preserved_clearance_flux_file_count':len(m['preserved_clearance_flux_files']),
            'unchanged_active_core_proof_bodies':len(m['retained_active_proof_blobs']),
            'new_core_proof_bodies':len(m['new_core_modules']),'unchanged_model_and_interface_files':len(m['retained_model_blobs']),
            'repository_ancestor_verified':False,
            'scope':'Byte identity and explicit claim scope only; not proof certification.'}
if __name__=='__main__': print(json.dumps(check(),indent=2,sort_keys=True))
