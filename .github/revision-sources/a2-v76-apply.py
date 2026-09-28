#!/usr/bin/env python3
"""Materialize the reviewed authorial delta; preserve and verify its entire baseline."""
from pathlib import Path, PurePosixPath
import base64,hashlib,json,lzma,os,re,subprocess
PREFIX=os.environ.get('SOURCE_PREFIX','papers/A2-v17-boundary-information-coarsening')
ROOT=Path(PREFIX)
BASE='89d5a3aa3e9f00a806d48f19f6f6831770184d76'
TREE='8a1a76ffba5009a6c3d9ed2e3c93e48a59f3ac1d'
PAYLOAD='2e0c43ebf82519cdcf0e733fcf4700c13cf608415b2c232bbf6e82eaade7013d'
def need(test,message):
    if not test:raise RuntimeError(message)
def git(*args):return subprocess.check_output(['git',*args])
def digest(b):return hashlib.sha256(b).hexdigest()
def write(name,data):
    p=PurePosixPath(name);need(not p.is_absolute() and '..' not in p.parts and bool(p.parts),'Unsafe delta path')
    dest=ROOT/name;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(data)
need(git('rev-parse','HEAD:'+PREFIX).decode().strip()==TREE,'Unexpected baseline tree')
parts=sorted(Path('.github/revision-sources').glob('a2-v76-payload-*.b64'))
need(len(parts)==3,'Incomplete payload')
packed=base64.b64decode(''.join(p.read_text().strip() for p in parts),validate=True)
need(digest(packed)==PAYLOAD,'Payload hash mismatch')
delta=json.loads(lzma.decompress(packed));need(len(delta['files'])==9 and len(delta['derived'])==9,'Unexpected delta set')
before={};records={}
for item in git('ls-tree','-r','-z','HEAD:'+PREFIX).split(b'\0'):
    if not item:continue
    meta,name=item.split(b'\t',1);name=name.decode();mode,kind,oid=meta.decode().split()
    need(kind=='blob' and mode in ('100644','100755'),'Nonregular source')
    data=(ROOT/name).read_bytes()
    need(hashlib.sha1(f'blob {len(data)}\0'.encode()+data).hexdigest()==oid,'Working bytes differ from Git: '+name)
    before[name]=data
    records[name]={'bytes':len(data),'sha256':digest(data),'git_blob':oid,'mode':mode,'archive':('archive/v75-before-v76/'+name) if name in ('main.tex','rigidity.tex') else None}
need(len(records)==1017,'Wrong baseline inventory')
def expand(name,seen=None):
    seen=set() if seen is None else seen
    need(name not in seen,'Cyclic source input');seen.add(name)
    return re.sub(r'\\input\{([^}]+)\}',lambda m:expand(m[1]+('' if m[1].endswith('.tex') else '.tex'),seen),before[name].decode())
labels=set()
for stem in ('main','rigidity','two_collision'):labels.update(re.findall(r'\\label\{([^}]+)\}',expand(stem+'.tex')))
need(len(labels)==1435,'Unexpected baseline labels')
for name,body in delta['files'].items():
    need(name not in before and not (ROOT/name).exists(),'Seed already exists: '+name)
    write(name,body.encode())
for name,spec in delta['derived'].items():
    original=before[spec['base']];need(digest(original)==spec['sha256'],'Wrong patch base')
    need(name in ('main.tex','rigidity.tex') or not (ROOT/name).exists(),'Unexpected derived target')
    lines=original.decode().splitlines(keepends=True);last=0;output=[]
    for start,end,body in spec['hunks']:
        need(last<=start<=end<=len(lines),'Overlapping patch');output.extend(lines[last:start]);output.append(body);last=end
    output.extend(lines[last:]);write(name,''.join(output).encode())
write('verification/v76-baseline-preservation.json',(json.dumps({'base_commit':BASE,'base_tree':TREE,'files':records},indent=2,sort_keys=True)+'\n').encode())
write('verification/v76-inherited-labels.json',(json.dumps(sorted(labels),indent=2)+'\n').encode())
git('add','--',PREFIX)
tree=git('write-tree').decode().strip();actual=git('rev-parse',tree+':'+PREFIX).decode().strip()
need(actual==delta['expected_tree'],'Materialized tree differs from tested authorial tree')
print(json.dumps({'status':'materialized','source_tree':actual,'baseline_files':len(records),'inherited_labels':len(labels),'payload_sha256':PAYLOAD},indent=2))
