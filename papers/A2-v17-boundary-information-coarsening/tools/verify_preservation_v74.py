#!/usr/bin/env python3
"""Verify every inherited path and every active mathematical input against v73."""
from __future__ import annotations
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile
from source_provenance import graph, require
ROOT=Path(__file__).resolve().parents[1]
BASE_TREE='80996c207ce723e8d84068f4fe95172f5d18fa65'
BASE_COMMIT='9c69f03f97dea57e83061af96aeb9bfe4dcc80d3'
ABSTRACTS={'article/00h_abstract_v66.tex','article/00j_abstract_v70.tex',
           'article/00m_abstract_addition_v72.tex','article/00o_abstract_addition_v73.tex'}

def blob(data: bytes) -> str:
    return hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()

def git(*args: str) -> bytes:
    return subprocess.check_output(['git','-C',str(ROOT),*args])

def main() -> None:
    edited=set(json.loads((ROOT/'REVISION_V74_EDITED_PATHS.json').read_text()))
    paths={}
    for item in git('ls-tree','--full-tree','-rz',BASE_TREE).split(b'\0'):
        if not item:continue
        meta,path=item.split(b'\t',1)
        mode,kind,sha=meta.decode().split()
        require(kind=='blob' and mode in ('100644','100755'),'Unsupported inherited object')
        paths[path.decode()]=(mode,sha)
    changed=[]
    for name,(mode,sha) in paths.items():
        current=ROOT/name
        require(current.is_file() and not current.is_symlink(),'Inherited path removed: '+name)
        current_mode='100755' if current.stat().st_mode&0o111 else '100644'
        if blob(current.read_bytes())!=sha or current_mode!=mode:
            require(name in edited,'Undeclared edit: '+name)
            saved=ROOT/'history/v73-review-baseline'/name
            require(saved.is_file() and blob(saved.read_bytes())==sha,'Original not preserved: '+name)
            require(('100755' if saved.stat().st_mode&0o111 else '100644')==mode,'Original mode changed: '+name)
            changed.append(name)
    require(set(changed)==edited,'Edited-path manifest mismatch')
    entries={}
    with tempfile.TemporaryDirectory(prefix='a2-v73-proof-inputs-') as temp:
        old=Path(temp)
        # Only TeX files are needed to resolve the source graph.
        for name,(_,sha) in paths.items():
            if name.endswith('.tex'):
                p=old/name;p.parent.mkdir(parents=True,exist_ok=True)
                p.write_bytes(git('cat-file','blob',sha))
        for entry in ('main.tex','rigidity.tex','two_collision.tex'):
            before=graph(old,entry);after=graph(ROOT,entry)
            missing=before-after
            require(missing<=ABSTRACTS,'Active proof input removed: '+repr(missing))
            entries[entry]={'inherited_active_files':len(before),'current_active_files':len(after),
                            'replaced_summary_inputs':sorted(missing),'removed_mathematical_inputs':[]}
    print(json.dumps({'status':'passed','baseline_review_commit':BASE_COMMIT,'baseline_source_tree':BASE_TREE,
                      'inherited_paths':len(paths),'deleted_inherited_paths':0,'byte_and_mode_preserved_originals':sorted(changed),
                      'entries':entries,
                      'scope':'Source preservation and routing only; not mathematical correctness or journal certification.'},indent=2,sort_keys=True))

if __name__=='__main__':
    main()
