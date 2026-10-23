#!/usr/bin/env python3
"""Populate only an isolated audit object store from authenticated R75 bytes."""
import datetime, gzip, hashlib, json, pathlib, subprocess, tarfile, zlib
ROOT=pathlib.Path('/workspace/scratch/f856e3d63ac5')
REPO=ROOT/'theta-r76-work'
OUT=ROOT/'r76-audit'
CACHE=OUT/'history.git'
SOURCE=REPO/'papers/General-Theta-Foundations-I-restart/r75-nonabelian-stationary-memory'
PUBLICATION=pathlib.Path(str(SOURCE)+'-publication')
def require(c,m):
    if not c: raise RuntimeError(m)
def write_object(data,expected=None):
    raw=f'blob {len(data)}\0'.encode()+data
    sha=hashlib.sha1(raw).hexdigest()
    require(expected is None or expected==sha,'Git blob identity mismatch')
    p=CACHE/'objects'/sha[:2]/sha[2:]
    p.parent.mkdir(exist_ok=True)
    if not p.exists():p.write_bytes(zlib.compress(raw))
    return sha
def main():
    subprocess.run(['git','init','--bare',str(CACHE)],check=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    (CACHE/'objects/info/alternates').write_text(str(REPO/'.git/objects')+'\n')
    archive=OUT/'r75-archives/General_Theta_Foundations_I_R75_Historical_Text_Corpus.tar.gz'
    require(hashlib.sha256(archive.read_bytes()).hexdigest()=='d9722229622f615401c7df4df83f6062ef04202923f0ec460569591c22164dae','Archive identity mismatch')
    index=json.loads(gzip.decompress((SOURCE/'provenance/current-full-scan/HISTORICAL_TEXT_INDEX.json.gz').read_bytes()))
    rows={r['git_blob']:r for r in index}; seen=set(); total=0; enc={}
    with tarfile.open(archive) as tar:
        for member in tar:
            require(member.isfile(),'Unexpected nonfile history member')
            sha=pathlib.Path(member.name).stem; require(sha in rows and sha not in seen,'Unexpected/duplicate corpus member')
            data=tar.extractfile(member).read(); row=rows[sha]
            require(len(data)==row['bytes'] and hashlib.sha256(data).hexdigest()==row['sha256'],'History SHA256 or size mismatch')
            require(write_object(data,sha)==sha,'History Git object mismatch')
            data.decode(row['encoding']);enc[row['encoding']]=enc.get(row['encoding'],0)+1
            total+=len(data);seen.add(sha)
    require(seen==set(rows),'Incomplete historical corpus')
    current=[]
    for folder in [SOURCE,PUBLICATION]:
        for p in folder.rglob('*'):
            if p.is_file() and '__pycache__' not in p.parts:
                data=p.read_bytes();sha=write_object(data)
                current.append({'path':str(p.relative_to(REPO)),'git_blob':sha,'sha256':hashlib.sha256(data).hexdigest(),'bytes':len(data)})
    result={'schema':'theta.r76.historical-object-cache.v1','completed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'historical_members':len(seen),'historical_bytes':total,'historical_encodings':enc,'source_and_publication_files':len(current),'files':current,'scope':'Isolated audit Git object cache. Shared repository refs, index and worktree were not changed.'}
    (OUT/'HISTORY_CACHE_MATERIALIZATION.json').write_text(json.dumps(result,indent=2)+'\n')
    print({k:v for k,v in result.items() if k!='files'})
if __name__=='__main__':main()
