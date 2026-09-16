#!/usr/bin/env python3
"""Materialize exact v71 sources, preserving the reviewed tree and its originals."""
from pathlib import Path
import base64
import hashlib
import json
import lzma
import subprocess

PREFIX='papers/A2-v17-boundary-information-coarsening'
BASE_TREE='63fdb25cd2002d9d2b3a238e7e7f1862b2328d2b'
TARGET_TREE='8549bb0789d5e6cdce8ae12f70ed7c100f81510b'
PAYLOAD_HASH='c09f7051b2857fbee8f21eb192a7bbc35bf72025e55b989be1e9389f73c7da20'

def require(ok,message):
    if not ok:raise RuntimeError(message)

def git(*args):
    return subprocess.check_output(['git',*args])

def safe(name):
    p=Path(name)
    require(name and not p.is_absolute() and '..' not in p.parts and '\\' not in name,
            'Unsafe source path')
    return p

def main():
    require(git('rev-parse','HEAD:'+PREFIX).decode().strip()==BASE_TREE,
            'The bootstrap does not contain the reviewed manuscript tree')
    require(not git('status','--porcelain=v1','--',PREFIX),'Dirty manuscript tree')
    directory=Path('.github/revision-sources')
    parts=[directory/('a2-v71.delta.'+str(i)) for i in range(3)]
    data=lzma.decompress(base64.b64decode(''.join(p.read_text() for p in parts),validate=True))
    require(hashlib.sha256(data).hexdigest()==PAYLOAD_HASH,'Payload digest mismatch')
    files=json.loads(data)['files']; prepared={}
    require(len(files)==24,'Unexpected delta inventory')
    # Read every original from HEAD before writing any file. No mutable copy source.
    for name,entry in files.items():
        safe(name);require(entry['mode'] in ('100644','100755'),'Invalid file mode')
        if 'copy' in entry:
            safe(entry['copy']);result=git('show','HEAD:'+entry['copy'])
        elif 'read' in entry:
            safe(entry['read']);old=git('show','HEAD:'+entry['read']).decode('utf-8')
            cursor=0;pieces=[]
            for begin,end,insertion in entry['edits']:
                require(isinstance(begin,int) and isinstance(end,int) and
                        cursor<=begin<=end<=len(old),'Invalid edit interval')
                pieces.extend((old[cursor:begin],insertion));cursor=end
            pieces.append(old[cursor:]);result=''.join(pieces).encode('utf-8')
        else:
            result=entry['content'].encode('utf-8')
        require(hashlib.sha256(result).hexdigest()==entry['sha256'],'File digest: '+name)
        prepared[name]=(result,int(entry['mode'],8)&0o777)
    for name,(data,mode) in prepared.items():
        path=Path(PREFIX)/safe(name)
        require(not path.is_symlink(),'Refusing symlink')
        path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(data);path.chmod(mode)
    git('add','--',PREFIX)
    staged=set(git('diff','--cached','--name-only').decode().splitlines())
    require(staged=={PREFIX+'/'+name for name in prepared},'Unexpected staged source set')
    root_tree=git('write-tree').decode().strip()
    tree=git('rev-parse',root_tree+':'+PREFIX).decode().strip()
    require(tree==TARGET_TREE,'Materialized manuscript tree differs from compiled local tree')
    print(json.dumps({'status':'verified','source_tree':tree,'changed_or_added':len(prepared)},sort_keys=True))

if __name__=='__main__':main()
