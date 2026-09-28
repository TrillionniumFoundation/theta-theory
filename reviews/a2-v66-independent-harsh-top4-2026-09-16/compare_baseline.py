#!/usr/bin/env python3
"""Byte/mode/source-graph comparison of the frozen v65 and v66 manuscripts.
Usage: python compare_baseline.py WORK_ROOT
WORK_ROOT: source/source and source/SOURCE_MANIFEST.json, baseline/source and
baseline/SOURCE_MANIFEST.json, plus their active-source-manifest.json files.
No manuscript checker is imported; file counts are not theorem counts.
"""
from pathlib import Path
import hashlib,json,sys

def require(ok,message):
    if not ok: raise RuntimeError(message)

def verify(root,manifest):
    for name,rec in manifest['files'].items():
        b=(root/name).read_bytes()
        require(len(b)==rec['bytes'],name+': bytes')
        require(hashlib.sha256(b).hexdigest()==rec['sha256'],name+': SHA256')
        require(hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==rec['git_blob'],name+': Git blob')

def main():
    root=Path(sys.argv[1]).resolve();old=root/'baseline/source';new=root/'source/source'
    om=json.loads((root/'baseline/SOURCE_MANIFEST.json').read_text());nm=json.loads((root/'source/SOURCE_MANIFEST.json').read_text())
    verify(old,om);verify(new,nm)
    changed=[];same=[];archives=[]
    for name,rec in om['files'].items():
        require(name in nm['files'],'Missing inherited path: '+name)
        identical=(old/name).read_bytes()==(new/name).read_bytes() and rec['mode']==nm['files'][name]['mode']
        if identical:same.append(name)
        else:
            changed.append(name);archive=new/'history/v65-review-baseline'/name
            require(archive.exists(),'Missing archive: '+str(archive))
            require(archive.read_bytes()==(old/name).read_bytes(),'Archive bytes differ: '+name)
            require(nm['files'][archive.relative_to(new).as_posix()]['mode']==rec['mode'],'Archive mode differs: '+name)
            archives.append(archive.relative_to(new).as_posix())
    oa=json.loads((root/'baseline/active-source-manifest.json').read_text());na=json.loads((root/'artifact/active-source-manifest.json').read_text())
    ou=set().union(*map(set,oa.values()));nu=set().union(*map(set,na.values()))
    require(ou<=nu,'Missing inherited active input')
    proofs=['article/10a_periodic_itinerary_relative_v64.tex','article/10b_periodic_contact_inverse_v65.tex','article/23f2_finite_experiment_analytic_inverse_v62.tex','article/25a_common_observables_v25.tex','two_collision.tex']
    for name in proofs:require((old/name).read_bytes()==(new/name).read_bytes(),'Changed retained proof: '+name)
    result={'old_frozen_files':len(om['files']),'new_frozen_files':len(nm['files']),'inherited_paths_retained':len(same)+len(changed),'unchanged_bytes_and_mode':len(same),'changed_inherited_paths':changed,'verified_archived_originals':archives,'old_active_union':len(ou),'new_active_union':len(nu),'added_active_paths':sorted(nu-ou),'byte_identical_key_modules':proofs,'scope':'Verified recorded modes, bytes and active source graph; not a semantic proof certification or count of independent theorems.'}
    (root/'SOURCE_DIFF.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
if __name__=='__main__':main()
