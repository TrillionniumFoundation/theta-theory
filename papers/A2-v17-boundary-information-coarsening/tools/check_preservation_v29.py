#!/usr/bin/env python3
"""Compare the full Git tree with the pinned v28 review; no silent deletions."""
from __future__ import annotations
import hashlib
import json
from pathlib import Path
import re
import subprocess

P='papers/A2-v17-boundary-information-coarsening'
BASE='5f10927a6399ebec0492b7f87b622ec80a4df631'
ROOT=Path(__file__).resolve().parents[1]

def git(*args: str) -> bytes:
    return subprocess.check_output(['git',*args],cwd=ROOT)

def tree(ref: str) -> dict[str,str]:
    result={}
    for entry in git('ls-tree','-rz',ref).split(b'\0'):
        if entry:
            meta,path=entry.split(b'\t',1)
            result[path.decode()]=meta.decode().split()[2]
    return result

def require(condition: bool, message: str) -> None:
    if not condition: raise RuntimeError(message)

def main() -> None:
    before,after=tree(BASE),tree('HEAD')
    missing=sorted(set(before)-set(after))
    require(not missing,'Deleted review-base paths: '+repr(missing))
    archives={'README.md':'README_PRE_V29.md',P+'/README.md':P+'/README_PRE_V29.md',
              P+'/main.tex':P+'/main_pre_v29.tex'}
    modified=sorted(p for p in before if before[p]!=after[p])
    for p in modified:
        require(p in archives,'Unexpected modification of inherited source: '+p)
        require(after.get(archives[p])==before[p],'Missing exact archive: '+p)
    old=git('show',BASE+':'+P+'/main.tex').decode()
    new=git('show','HEAD:'+P+'/main.tex').decode()
    inputs=lambda s: re.findall(r'\\input\{([^}]+)\}',s)
    expected=[{'article/01b_observation_hierarchy_v28':'article/01b_observation_hierarchy_v29',
               'article/23h_global_orientation_quotient_v28':'article/23h_global_orientation_quotient_v29'}.get(x,x)
              for x in inputs(old)]
    i=expected.index('article/23f_single_offset_law_inverse_v26')+1
    expected.insert(i,'article/23f1_equivariant_density_extension_v29')
    require(inputs(new)==expected,'Native direct-input ordering changed unexpectedly')
    abstract=lambda s: s.split('\\begin{abstract}',1)[1].split('\\end{abstract}',1)[0]
    require(abstract(old)==abstract(new),'Inherited abstract changed unexpectedly')
    orientation={}
    for version in (28,29):
        ref=BASE if version==28 else 'HEAD'
        orientation[version]=git('show',ref+':'+P+f'/article/23h_global_orientation_quotient_v{version}.tex').decode()
    labels=lambda s: re.findall(r'\\label\{([^}]+)\}',s)
    require(labels(orientation[28])==labels(orientation[29]),'Orientation labels lost or reordered')
    divider='\\begin{corollary}[Holonomy and fixed-order stability under the quotient]'
    require(orientation[28].split(divider)[0]==orientation[29].split(divider)[0],
            'Exact classification or gluing proof changed')
    divider='\\begin{remark}[Law-valued orientation orbits are not folded records]'
    require(orientation[28].split(divider)[1]==orientation[29].split(divider)[1],
            'Folded-record distinction changed')
    result={'status':'passed','review_base':BASE,'head':git('rev-parse','HEAD').decode().strip(),
            'inherited_paths':len(before),'deleted_paths':missing,'modified_inherited_paths':modified,
            'added_paths':sorted(set(after)-set(before)),'main_direct_inputs':len(expected),
            'orientation_labels_preserved':len(labels(orientation[28])),
            'exact_classification_and_folded_remark_byte_preserved':True,
            'scope':'Full Git-tree preservation and changed-module integration; not a proof or native compilation certificate.'}
    print(json.dumps(result,indent=2,sort_keys=True))

if __name__=='__main__': main()
