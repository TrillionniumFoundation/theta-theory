#!/usr/bin/env python3
"""Verify both frozen source trees and compare v66 with v67; no author code.
Usage: python compare_baseline.py /path/to/v67audit
The work directory contains source/, artifact/ and baseline/{source,artifact}/.
"""
import hashlib,json,sys
from pathlib import Path
from verify_delivery import check_file,tree_hash,require

def verify(root):
    mf=json.loads((root/'source/SOURCE_MANIFEST.json').read_text())['files']
    tree={}
    for path,rec in mf.items():
        check_file(root/'source/source'/path,rec)
        cur=tree;parts=path.split('/')
        for part in parts[:-1]: cur=cur.setdefault(part,{})
        cur[parts[-1]]=(rec['mode'],rec['git_blob'])
    bh=json.loads((root/'artifact/build-report.json').read_text())
    require(tree_hash(tree)==bh['source_tree'],'Frozen source tree mismatch')
    active=json.loads((root/'artifact/active-source-manifest.json').read_text())
    union=set()
    for files in active.values():
        for p,rec in files.items():
            check_file(root/'source/source'/p,rec);union.add(p)
    return mf,union,bh['source_tree']

if __name__=='__main__':
    root=Path(sys.argv[1]).resolve();old,oa,ot=verify(root/'baseline');new,na,nt=verify(root)
    require(set(old)<=set(new),'Deleted inherited file')
    changed=[];identical=[];modes=[]
    for p,rec in old.items():
        if rec['mode']!=new[p]['mode']: modes.append(p)
        if rec['sha256']==new[p]['sha256']: identical.append(p)
        else:
            arc='history/v66-review-baseline/'+p
            require(arc in new,'Missing archived original: '+p)
            require(new[arc]['sha256']==rec['sha256'],'Archived byte mismatch: '+p)
            changed.append(p)
    require(oa<=na,'Removed active path')
    tracked=['article/10a_periodic_itinerary_relative_v64.tex','article/10b_periodic_contact_inverse_v65.tex',
             'article/23f2_finite_experiment_analytic_inverse_v62.tex','article/25a_common_observables_v25.tex']
    require(all(p in identical for p in tracked),'Changed retained proof module')
    out={'baseline_tree':ot,'current_tree':nt,'baseline_files_verified':len(old),'current_files_verified':len(new),
         'inherited_unchanged':len(identical),'inherited_changed':changed,'inherited_mode_changes':modes,
         'archived_originals_verified':len(changed),'new_paths':sorted(set(new)-set(old)),
         'baseline_active_union':len(oa),'current_active_union':len(na),'added_active_paths':sorted(na-oa),
         'unchanged_tracked_proof_modules':tracked,
         'scope':'Byte/mode and input-manifest comparison, not a semantic theorem census.'}
    print(json.dumps(out,indent=2))
