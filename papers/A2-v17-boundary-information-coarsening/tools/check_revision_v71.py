#!/usr/bin/env python3
"""Source conservation and exact finite controls, not a theorem certificate."""
from __future__ import annotations
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path
import re
import stat
import subprocess
import sys
import tempfile
from source_provenance import INPUT, blob_id, require, safe_relative, strip_comments
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'history/v70-review-baseline'
EDITED={'README.md','main.tex','rigidity.tex','article/00i_main_thesis_v70.tex',
        'journal/references_v56.tex','v5/references_v43.tex'}
CORE=('article/10a_periodic_itinerary_relative_v64.tex',
      'article/10b_periodic_contact_inverse_v65.tex',
      'article/10c_global_curvature_inverse_v66.tex',
      'article/10d_smooth_contact_rigidity_v68.tex',
      'article/10e_sampled_smooth_recovery_v69.tex')
ENTRIES=('main.tex','rigidity.tex','two_collision.tex')
ADDED={'article/00k_lens_comparison_v71.tex',
       'article/10f_local_observation_comparison_v71.tex',
       'journal/lens_references_v71.tex'}

def old_path(name: str)->Path:
    return (BASE if name in EDITED else ROOT)/safe_relative(name)

def matches(data: bytes, rec: dict)->bool:
    return (len(data)==rec['bytes'] and blob_id(data)==rec['git_blob']
            and hashlib.sha256(data).hexdigest()==rec['sha256'])

def active(name: str,old: bool=False,found: set[str]|None=None)->set[str]:
    found=set() if found is None else found
    if name in found:return found
    found.add(name)
    p=old_path(name) if old else ROOT/safe_relative(name)
    require(p.is_file() and not p.is_symlink(),'Missing input '+name)
    for child in INPUT.findall(strip_comments(p.read_text())):
        active(child if child.endswith('.tex') else child+'.tex',old,found)
    return found

def conservation(records: dict)->dict:
    require(len(records)==911,'Unexpected reviewed inventory')
    changed=[]
    for name,rec in records.items():
        p=ROOT/name;old=old_path(name)
        require(p.is_file() and not p.is_symlink(),'Removed source '+name)
        require(old.is_file() and matches(old.read_bytes(),rec),'Changed original '+name)
        expected=int(rec['mode'],8)&0o777
        for q in (p,old):
            require(stat.S_IMODE(q.stat().st_mode) in (expected,0o444),'Mode mismatch '+name)
        if not matches(p.read_bytes(),rec):changed.append(name)
    require(set(changed)==EDITED,'Unexpected edits '+repr(changed))
    for name in CORE:require(matches((ROOT/name).read_bytes(),records[name]),'Core edit '+name)
    old={e:active(e,True) for e in ENTRIES};new={e:active(e) for e in ENTRIES}
    ou=set().union(*old.values());nu=set().union(*new.values())
    require(len(ou)==138 and ou<=nu and nu-ou==ADDED,'Active source loss or unexpected addition')
    for e in ENTRIES:require(old[e]<=new[e],'Lost entry-specific input '+e)
    for e in ENTRIES[:2]:
        t=(ROOT/e).read_text();pos=[t.index('\\input{'+x[:-4]+'}') for x in CORE]
        require(pos==sorted(pos),'Reordered core')
        require(pos[-1]<t.index('\\input{article/10f_local_observation_comparison_v71}')
                <t.index('\\input{article/01c_geometric_setup_v43}'),'Incorrect comparison placement')
    expr=r'\\begin\{theorem\}.*?\\end\{theorem\}'
    path='article/00i_main_thesis_v70.tex'
    require(re.findall(expr,(ROOT/path).read_text(),re.S)==
            re.findall(expr,old_path(path).read_text(),re.S),'Edited lead theorem statement')
    require(not matches((ROOT/CORE[0]).read_bytes()+b'bad',records[CORE[0]]),'Corruption control')
    require(not ou<=(nu-{CORE[0]}),'Missing-input control')
    return {'review_commit':'f1d516c0033256d50ca23d87cc5a40fef8f72d45',
            'reviewed_source':'16ec1030b9dfd9b185a1f0da8e50b10b40a71940',
            'reviewed_tree':'63fdb25cd2002d9d2b3a238e7e7f1862b2328d2b',
            'inherited_files':len(records),'unchanged_inherited':len(records)-len(changed),
            'edited_originals_byte_and_mode_preserved':sorted(changed),
            'five_core_modules_unchanged':list(CORE),'main_theorem_statements_unchanged':True,
            'old_active_union':len(ou),'active_union':len(nu),
            'active_by_entry':{e:len(v) for e,v in new.items()},'new_active_inputs':sorted(ADDED),
            'negative_controls_detected':['source_corruption','active_input_deletion']}

def authentic_v70(records: dict)->dict:
    with tempfile.TemporaryDirectory(prefix='a2-v70-authentic-') as tmp:
        root=Path(tmp)
        for name,rec in records.items():
            p=root/safe_relative(name);p.parent.mkdir(parents=True,exist_ok=True)
            data=old_path(name).read_bytes();require(matches(data,rec),'Unverified baseline')
            p.write_bytes(data);p.chmod(int(rec['mode'],8)&0o777)
        cmd=[sys.executable,'-B']+(['-O'] if sys.flags.optimize else [])
        cp=subprocess.run(cmd+[str(root/'tools/check_revision_v70.py')],cwd=root,capture_output=True,text=True)
        require(cp.returncode==0,'Authentic v70 failed: '+cp.stderr)
        result=json.loads(cp.stdout)
    return {'scope':'unchanged checker against reconstructed reviewed v70 bytes and modes','result':result}

def finite_controls()->dict:
    # Finite exact measures test normalization, not the billiard continuum proof.
    cases=0;negative=0;products=0
    for numer in ((F(1,21),F(2,21),F(1,14)),(F(1,31),F(3,31),F(2,31))):
        for area in (F(2),F(5,2),F(7)):
            for other in (F(3),F(11,3),F(8)):
                a=tuple(x/area for x in numer);b=tuple(x/other for x in numer)
                pa=sum(a);pb=sum(b)
                require(b==tuple(area/other*x for x in a),'Area scaling')
                require(tuple(x/pa for x in a)==tuple(x/pb for x in b),'Conditional cancellation')
                require((1-pa,*a)!=(1-pb,*b),'Omitted-area negative control')
                cases+=1;negative+=1
                same=tuple(x/area for x in numer)
                record=(1-pa,*a);record2=(1-sum(same),*same)
                for x in range(len(record)):
                    for y in range(len(record)):
                        require(record[x]*record[y]==record2[x]*record2[y],'Product law')
                        products+=1
    area_pairs=0
    for first in range(1,6):
        for second in range(1,6):
            require(F(first)-F(first,second)*second==0,'Area first variation')
            area_pairs+=1
    return {'scope':'finite exact normalization/product/linearized-area bookkeeping only',
            'area_scaling_cases':cases,'conditional_cases':cases,
            'wrong_equal_record_at_unequal_area_controls':negative,
            'two_record_product_entries':products,'area_first_variation_cases':area_pairs,
            'does_not_certify':['stationary uniqueness','phase-volume parametrization','smooth inversion',
                                'area implicit-function theorem','lens theorem','originality']}

def main()->None:
    records=json.loads((BASE/'SOURCE_MANIFEST.json').read_text())['files']
    print(json.dumps({'scope':'Author-side conservation and finite controls; not proof certification',
                      'source':conservation(records),'finite_controls':finite_controls(),
                      'authentic_v70':authentic_v70(records)},indent=2,sort_keys=True))
if __name__=='__main__':main()
