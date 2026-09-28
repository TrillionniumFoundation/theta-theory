#!/usr/bin/env python3
"""Verify downloaded A2 v54 bytes without importing author code.
Usage: python verify_delivery.py NATIVE_DIR SOURCE_DIR
"""
import hashlib, json, pathlib, sys

def demand(condition, message):
    if not condition: raise RuntimeError(message)

def digest(data, kind='sha256'): return hashlib.new(kind, data).hexdigest()
def git_oid(kind, data): return digest((kind+' '+str(len(data))+'\0').encode()+data, 'sha1')
def tree_oid(node):
    entries=[]
    for name, val in node.items():
        if isinstance(val, dict): mode, oid, key='40000',tree_oid(val),name+'/'
        else: mode, oid=val;key=name
        entries.append((key.encode(), mode.encode()+b' '+name.encode()+b'\0'+bytes.fromhex(oid)))
    return git_oid('tree', b''.join(v for k,v in sorted(entries)))

def main():
    native, source=map(pathlib.Path,sys.argv[1:3])
    manifest=json.loads((native/'frozen-source-manifest.json').read_text())
    tree={}
    for name,m in manifest['files'].items():
        data=(source/name).read_bytes()
        demand(len(data)==m['bytes'],name+' length')
        demand(digest(data)==m['sha256'],name+' sha256')
        demand(git_oid('blob',data)==m['git_blob'],name+' blob')
        node=tree;parts=name.split('/')
        for part in parts[:-1]:node=node.setdefault(part,{})
        node[parts[-1]]=(m['mode'],m['git_blob'])
    source_tree=tree_oid(tree)
    demand(source_tree=='407b278984b14e57468e727fb56b0fa4163a7207','source tree mismatch')
    report=json.loads((native/'build-report.json').read_text())
    for name,m in report['evidence_files'].items():
        data=(native/name).read_bytes()
        demand(len(data)==m['bytes'] and digest(data)==m['sha256'],name+' evidence')
    active=json.loads((native/'active-source-manifest.json').read_text())
    for entry,files in active.items():
        for name,m in files.items():
            data=(source/name).read_bytes()
            demand(digest(data)==m['sha256'] and git_oid('blob',data)==m['git_blob'],name+' active')
    baseline=json.loads((source/'history/v53-review-baseline/active-source-manifest.json').read_text())
    demand(set(active)==set(baseline),'entry sets changed')
    for entry in active:
        demand(set(active[entry])==set(baseline[entry]),entry+' active paths changed')
    companion_unchanged=0
    for name,m in baseline['two_collision'].items():
        demand(digest((source/name).read_bytes())==m['sha256'],name+' inherited companion')
        companion_unchanged+=1
    unchanged=[];changed=[]
    for name,m in baseline['main'].items():
        if digest((source/name).read_bytes())==m['sha256']:unchanged.append(name)
        else:
            changed.append(name)
            old=source/'history/v53-review-baseline'/name
            demand(digest(old.read_bytes())==m['sha256'],name+' archive')
    products={}
    for name in ['main','two_collision']:
        data=(native/(name+'.pdf')).read_bytes();m=report['entries'][name]['product']
        demand(len(data)==m['bytes'] and digest(data)==m['sha256'],name+' product')
        products[name]={'bytes':len(data),'sha256':digest(data)}
    nested=json.loads((source.parent/'SOURCE_MANIFEST.json').read_text())
    demand(nested==manifest,'nested source manifest')
    result={'status':'passed','source_files_verified':len(manifest['files']), 'source_tree':source_tree,
       'active_files':{k:len(v) for k,v in active.items()},'evidence_files_verified':len(report['evidence_files']),
       'inherited_main_active_unchanged':len(unchanged),'inherited_main_active_changed':changed,
       'archived_originals_verified':len(changed),'inherited_companion_active_unchanged':companion_unchanged,'products':products,
       'limitations':'Checks bytes and manifest consistency, not signatures or mathematics.'}
    print(json.dumps(result,indent=2,sort_keys=True))
if __name__=='__main__':main()
