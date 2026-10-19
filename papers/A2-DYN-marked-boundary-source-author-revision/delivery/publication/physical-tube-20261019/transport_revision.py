#!/usr/bin/env python3
"""Read-only local byte inventory and chunk adapter for authorized Git Data publication.

This adapter does not make network calls or mutate Git refs. The actual GitHub
plugin calls and their returned identities are retained separately.
"""
from pathlib import Path
import argparse, base64, hashlib, json, os
from datetime import datetime, timezone

ROOT = Path('/workspace/scratch/b5cc344d4c8e/theta-theory/papers/A2-DYN-physical-tube-source-height-author-revision')
WORK = Path('/workspace/scratch/b5cc344d4c8e/iteration-20261019')
BASE = WORK/'source-audit/BASELINE_ARTICLE_BLOBS.json'
SELF = 'delivery/publication/physical-tube-20261019/TRANSPORT_FILE_MANIFEST.json'

def git_blob(data):
    return hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()

def scan():
    baseline = {x['path']:x for x in json.loads(BASE.read_text())}
    known = {x['sha'] for x in baseline.values()}
    rows=[]
    for p in sorted(ROOT.rglob('*')):
        if not p.is_file() or '__pycache__' in p.parts or '.git' in p.parts:
            continue
        rel=p.relative_to(ROOT).as_posix()
        data=p.read_bytes()
        try:
            data.decode('utf-8'); encoding='utf-8'
        except UnicodeDecodeError:
            encoding='base64'
        mode='100755' if p.stat().st_mode & 0o111 else '100644'
        sha=git_blob(data)
        old=baseline.get(rel)
        rows.append({'path':rel,'mode':mode,'type':'blob','bytes':len(data),
                     'sha':sha,'sha256':hashlib.sha256(data).hexdigest(),
                     'encoding':encoding,'known_baseline_blob':sha in known,
                     'changed_from_base_path':not old or old['sha']!=sha or old['mode']!=mode})
    return rows

def tree_digest(rows):
    tree={}
    for row in rows:
        parts=row['path'].split('/'); node=tree
        for part in parts[:-1]: node=node.setdefault(part,{})
        node[parts[-1]]=(row['mode'],row['sha'])
    hashes={}
    def emit(node,prefix=''):
        entries=[]
        for name,value in node.items():
            if isinstance(value,dict):
                mode='40000'; sha=emit(value,prefix+name+'/'); key=name+'/'
            else:
                mode,sha=value;key=name
            entries.append((key.encode(),mode.encode()+b' '+name.encode()+b'\0'+bytes.fromhex(sha)))
        data=b''.join(x[1] for x in sorted(entries,key=lambda x:x[0]))
        sha=hashlib.sha1(b'tree '+str(len(data)).encode()+b'\0'+data).hexdigest()
        hashes[prefix.rstrip('/')]=sha
        return sha
    root=emit(tree)
    return root,hashes

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('action',choices=['inventory','changes','chunk','stats'])
    p.add_argument('--path');p.add_argument('--offset',type=int,default=0)
    p.add_argument('--length',type=int,default=98304)
    p.add_argument('--output',type=Path)
    args=p.parse_args()
    if args.action=='chunk':
        target=(ROOT/args.path).resolve()
        if not target.is_relative_to(ROOT) or args.offset<0 or args.length<1:
            raise RuntimeError('Invalid publication byte-read range')
        with target.open('rb') as f:
            f.seek(args.offset);data=f.read(args.length)
        print(base64.b64encode(data).decode())
        return
    rows=scan();sha,trees=tree_digest(rows)
    value={'created_utc':datetime.now(timezone.utc).isoformat(),
           'base_commit':'15ad3962de63f50911b765fe6608e722fe9b8c82',
           'base_article_tree':'39f02eb2dab466bb742c7f96139a6535d7bb10ef',
           'scope':'Actual local file bytes for the new isolated article; build evidence included; no continuous mathematical certification.',
           'article_tree_sha':sha,'file_count':len(rows),'bytes':sum(x['bytes'] for x in rows),
           'changed_paths':sum(x['changed_from_base_path'] for x in rows),'files':rows,'subtree_hashes':trees}
    if args.action=='changes':
        print(json.dumps([x for x in rows if x['changed_from_base_path']]))
    elif args.action=='stats':
        print(json.dumps({k:v for k,v in value.items() if k not in ['files','subtree_hashes']}))
    elif args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True)
        args.output.write_text(json.dumps(value,indent=2)+'\n')
        print(json.dumps({k:v for k,v in value.items() if k not in ['files','subtree_hashes']}))
    else:
        print(json.dumps(value))

if __name__=='__main__':main()
