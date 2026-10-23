#!/usr/bin/env python3
"""Inventory A2-DYN Git objects without expanding repeated archive paths."""
import collections, gzip, hashlib, json, pathlib, subprocess

ROOT=pathlib.Path('/workspace/scratch/917494ae78f7')
REPO=ROOT/'theta-theory'
OUT=ROOT/'revision-prep/history-census'
OUT.mkdir(parents=True,exist_ok=True)
refs=json.loads((ROOT/'remote_refs_initial.json').read_text())
refs=[r for r in refs if 'a2-dyn' in r['ref'].lower()]
proc=subprocess.Popen(['git','cat-file','--batch'],cwd=REPO,stdin=subprocess.PIPE,stdout=subprocess.PIPE)
cache={}
def obj(oid):
    if oid in cache:return cache[oid]
    proc.stdin.write((oid+'\n').encode());proc.stdin.flush()
    header=proc.stdout.readline().split()
    if len(header)!=3:raise RuntimeError(header)
    content=proc.stdout.read(int(header[2]));assert proc.stdout.read(1)==b'\n'
    cache[oid]=(header[1].decode(),content)
    return cache[oid]
def tree(oid):
    typ,data=obj(oid);assert typ=='tree'
    i=0;rows=[]
    while i<len(data):
        j=data.index(b' ',i);k=data.index(b'\0',j)
        mode=data[i:j].decode();name=data[j+1:k].decode()
        child=data[k+1:k+21].hex();i=k+21
        rows.append({'mode':mode,'name':name,'oid':child,'type':'tree' if mode=='40000' else 'blob'})
    return rows
def lookup(oid,name):
    return next((x for x in tree(oid) if x['name']==name),None)
commits={};roots=[];refrows=[]
for r in refs:
    sha=r['object']['sha']
    if sha not in commits:
        typ,data=obj(sha);assert typ=='commit'
        head,body=data.decode().split('\n\n',1)
        lines=head.splitlines();tr=next(x[5:] for x in lines if x.startswith('tree '))
        commits[sha]={'sha':sha,'tree':tr,'commit_header':head,'subject':body.splitlines()[0]}
        for dirname,match in [('papers',lambda s:s.upper().startswith('A2-DYN')),('reviews',lambda s:'a2-dyn' in s.lower())]:
            root=lookup(tr,dirname)
            if root:
                for row in tree(root['oid']):
                    if match(row['name']):
                        roots.append({'commit':sha,'path':dirname+'/'+row['name'],**row})
        gh=lookup(tr,'.github')
        if gh:
            wf=lookup(gh['oid'],'workflows')
            if wf:
                for row in tree(wf['oid']):
                    if 'a2-dyn' in row['name'].lower():roots.append({'commit':sha,'path':'.github/workflows/'+row['name'],**row})
        for row in tree(tr):
            if 'a2_dyn' in row['name'].lower() or 'a2-dyn' in row['name'].lower():
                roots.append({'commit':sha,'path':row['name'],**row})
    refrows.append({'ref':r['ref'],'sha':sha,'tree':commits[sha]['tree'],'subject':commits[sha]['subject']})
queue=collections.deque(sorted(roots,key=lambda x:len(x['path'])))
trees={};blobs={}
while queue:
    row=queue.popleft();oid=row['oid']
    if row['type']=='blob':
        if oid not in blobs:blobs[oid]={'oid':oid,'first_path':row['path'],'first_commit':row.get('commit'),'names':[]}
        if row['name'] not in blobs[oid]['names']:blobs[oid]['names'].append(row['name'])
        continue
    if oid in trees:continue
    children=tree(oid)
    trees[oid]={'oid':oid,'first_path':row['path'],'entries':children}
    for child in children:queue.append({**child,'path':row['path']+'/'+child['name'],'commit':row.get('commit')})
native=[x for x in blobs.values() if any(n.endswith('.tex') for n in x['names'])]
reports=[x for x in blobs.values() if any(('referee' in n.lower() or 'review' in n.lower()) and n.endswith(('.md','.tex','.txt')) for n in x['names'])]
summary={'repository':'TrillionniumFoundation/theta-theory','scope':'All initial a2-dyn named refs; scoped paper/review/workflow/root-index tree DAG, deduplicated by object ID; content identity census is not a claim of independently proving all historical mathematics.','refs':len(refs),'distinct_commits':len(commits),'scoped_root_records':len(roots),'unique_scoped_trees':len(trees),'unique_scoped_blobs':len(blobs),'unique_native_tex_blobs':len(native),'report_named_blobs':len(reports)}
payload={'summary':summary,'refs':refrows,'commits':list(commits.values()),'scope_roots':roots,'trees':list(trees.values()),'blobs':list(blobs.values())}
with gzip.GzipFile(filename=str(OUT/'SCOPED_GIT_OBJECT_CENSUS.json.gz'),mode='wb',mtime=0) as f:f.write((json.dumps(payload,sort_keys=True)+'\n').encode())
(OUT/'SUMMARY.json').write_text(json.dumps(summary,indent=2)+'\n')
(OUT/'NATIVE_TEX_OBJECTS.json').write_text(json.dumps(native,indent=2)+'\n')
(OUT/'native-blob-ids.txt').write_text(''.join(x['oid']+'\n' for x in native))
(OUT/'A2_DYN_REFS.json').write_text(json.dumps(refrows,indent=2)+'\n')
proc.stdin.close();proc.wait()
print(json.dumps(summary,indent=2))
