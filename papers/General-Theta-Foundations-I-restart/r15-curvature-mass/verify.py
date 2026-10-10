#!/usr/bin/env python3
"""Read-only source, reference, and dependency audit for the native r15 subtree."""
import hashlib
import json
import re
from pathlib import Path

ROOT=Path(__file__).resolve().parent
EXCLUDED={'evidence','artifacts','__pycache__','.git'}

def require(ok, message):
    if not ok:
        raise RuntimeError(message)

def sha256(data):
    return hashlib.sha256(data).hexdigest()

def git_hash(kind, data):
    return hashlib.sha1((kind+' '+str(len(data))).encode()+b'\0'+data).hexdigest()

def sources(root=ROOT):
    return sorted(p.relative_to(root).as_posix() for p in root.rglob('*')
                  if p.is_file() and not EXCLUDED.intersection(p.relative_to(root).parts)
                  and p.name!='SOURCE_MANIFEST.json')

def source_tree(root=ROOT):
    paths=sources(root)+['SOURCE_MANIFEST.json']
    tree={}
    for name in paths:
        node=tree
        parts=name.split('/')
        for part in parts[:-1]:
            node=node.setdefault(part,{})
        node[parts[-1]]=git_hash('blob',(root/name).read_bytes())
    def encode(node):
        data=b''
        for name,value in sorted(node.items(),key=lambda kv:kv[0]+('/' if isinstance(kv[1],dict) else '')):
            isdir=isinstance(value,dict)
            digest=encode(value) if isdir else value
            data+=('40000' if isdir else '100644').encode()+b' '+name.encode()+b'\0'+bytes.fromhex(digest)
        return git_hash('tree',data)
    return encode(tree)

def verify(root=ROOT):
    manifest=json.loads((root/'SOURCE_MANIFEST.json').read_text())
    names=sources(root)
    require(names==sorted(manifest['files']), 'source inventory differs from manifest')
    for name in names:
        data=(root/name).read_bytes(); item=manifest['files'][name]
        require(not any(c < 32 and c not in (9, 10) for c in data), 'unexpected control byte: '+name)
        require(sha256(data)==item['sha256'], 'source hash mismatch: '+name)
        require(git_hash('blob',data)==item['git_blob_sha'], 'Git blob mismatch: '+name)
    active=[]
    def visit(name):
        require(name not in active, 'duplicate or cyclic TeX input: '+name)
        require(name in names, 'unmanifested TeX input: '+name)
        active.append(name)
        text=(root/name).read_text()
        for child in re.findall(r'\\input\{([^}]+)\}',text):
            require('..' not in Path(child).parts, 'out-of-subtree input')
            visit(child if child.endswith('.tex') else child+'.tex')
    visit('main.tex')
    tex=sorted(n for n in names if n.endswith('.tex'))
    require(sorted(active)==tex, 'inactive or missing TeX source')
    text='\n'.join((root/n).read_text() for n in active)
    labels=re.findall(r'\\label\{([^}]+)\}',text)
    require(len(labels)==len(set(labels)), 'duplicate labels')
    refs=re.findall(r'\\(?:eqref|ref)\{([^}]+)\}',text)
    require(set(refs)<=set(labels), 'unresolved labels: '+str(set(refs)-set(labels)))
    bib=re.findall(r'\\bibitem\{([^}]+)\}',text)
    cites=[k.strip() for group in re.findall(r'\\cite\{([^}]+)\}',text) for k in group.split(',')]
    require(len(bib)==len(set(bib)), 'duplicate bibliography keys')
    require(set(cites)==set(bib), 'missing or unused bibliography entries')
    statements=re.findall(r'\\begin\{(theorem|proposition|lemma|corollary|definition|example)\}',text)
    return {'status':'PASS','native_files':len(names),'active_tex':active,
            'labels':len(labels),'references':len(refs),'bibliography_entries':len(bib),
            'formal_statements':len(statements),'native_source_tree_sha':source_tree(root),
            'scope':'native manuscript subtree; not a full repository checkout audit'}

if __name__=='__main__':
    print(json.dumps(verify(),sort_keys=True,indent=2))
