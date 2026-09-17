#!/usr/bin/env python3
"""Verify exact v72 source preservation and active-input conservation in v73.

Run in a Git checkout containing the pinned v72 objects. No network or writes
to the repository are performed. This is not a mathematical proof checker.
"""
from __future__ import annotations
import json
from pathlib import Path
import subprocess
import tempfile
from source_provenance import blob_id, graph, require

OLD_TREE='78fb5bad4944d0bff60e108996cca84d4473fa85'
EDITED={'README.md','main.tex','rigidity.tex','article/00i_main_thesis_v70.tex',
        'article/10g_uncalibrated_single_law_v72.tex','journal/references_v56.tex','v5/references_v43.tex'}
SOURCE=Path(__file__).resolve().parents[1]

def git(*args, data=None):
    return subprocess.run(['git',*args],cwd=SOURCE,input=data,check=True,capture_output=True).stdout

def main():
    rows=[]
    for row in git('ls-tree','--full-tree','-r','-z',OLD_TREE).split(b'\0'):
        if row:
            meta,name=row.split(b'\t',1); mode,kind,oid=meta.decode().split()
            require(kind=='blob','Nonblob baseline')
            rows.append((name.decode(),mode,oid))
    stream=git('cat-file','--batch',data=''.join(oid+'\n' for _,_,oid in rows).encode())
    offset=0; unchanged=0; preserved=0; edited=[]
    with tempfile.TemporaryDirectory(prefix='a2-v72-conservation-') as tmp:
        old=Path(tmp)
        for name,mode,oid in rows:
            end=stream.index(b'\n',offset); header=stream[offset:end].decode().split(); size=int(header[2])
            data=stream[end+1:end+1+size]; offset=end+size+2
            require(blob_id(data)==oid,'Baseline stream corruption')
            target=SOURCE/name; require(target.is_file() and not target.is_symlink(),'Missing inherited path: '+name)
            actual=target.read_bytes()
            if actual==data:
                unchanged+=1
            else:
                require(name in EDITED,'Unexpected inherited edit: '+name)
                backup=SOURCE/'history/v72-review-baseline'/name
                require(backup.is_file() and backup.read_bytes()==data,'Historical bytes not retained: '+name)
                require(bool(backup.stat().st_mode & 0o111)==(mode=='100755'),'Historical mode differs: '+name)
                preserved+=1; edited.append(name)
            dest=old/name;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(data)
        require(offset==len(stream),'Unparsed baseline data')
        require(set(edited)==EDITED,'Expected edit set differs')
        active={}; oldunion=set(); newunion=set()
        for entry in ('main.tex','rigidity.tex','two_collision.tex'):
            before=graph(old,entry);after=graph(SOURCE,entry)
            require(before<=after,'Removed active inputs: '+repr(before-after))
            oldunion.update(before);newunion.update(after)
            active[entry]={'before':len(before),'after':len(after),'added':sorted(after-before),'removed':[]}
    print(json.dumps({'status':'passed','baseline_tree':OLD_TREE,'inherited_paths':len(rows),
      'unchanged_in_place':unchanged,'edited_with_exact_originals':preserved,'edited_paths':sorted(edited),
      'active_inputs':active,'old_active_union':len(oldunion),'new_active_union':len(newunion),
      'scope':'Byte/mode preservation and active-input conservation, not proof certification.'},indent=2,sort_keys=True))

if __name__=='__main__':main()
