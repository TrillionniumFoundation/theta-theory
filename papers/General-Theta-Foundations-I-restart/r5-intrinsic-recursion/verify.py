#!/usr/bin/env python3
"""Read-only source inventory, citation, label and native Git-tree audit."""
from pathlib import Path
import hashlib, json, re
ROOT=Path(__file__).resolve().parent

def sha256(data): return hashlib.sha256(data).hexdigest()
def git_hash(kind,data): return hashlib.sha1(kind.encode()+b' '+str(len(data)).encode()+b'\0'+data).hexdigest()
def tree_hash(files):
    node={}
    for name,data in files.items():
        n=node; parts=name.split('/')
        for x in parts[:-1]: n=n.setdefault(x,{})
        n[parts[-1]]=data
    def rec(n):
        out=b''
        for key in sorted(n,key=lambda k:k+('/' if isinstance(n[k],dict) else '')):
            val=n[key]; isdir=isinstance(val,dict)
            digest=rec(val) if isdir else git_hash('blob',val)
            out+=(b'40000' if isdir else b'100644')+b' '+key.encode()+b'\0'+bytes.fromhex(digest)
        return git_hash('tree',out)
    return rec(node)

def audit(root=ROOT):
    manifest=json.loads((root/'SOURCE_MANIFEST.json').read_text())
    names=[f['path'] for f in manifest['files']]
    if len(names)!=len(set(names)): raise RuntimeError('duplicate manifest entry')
    for f in manifest['files']:
        data=(root/f['path']).read_bytes()
        if sha256(data)!=f['sha256'] or len(data)!=f['bytes']: raise RuntimeError('manifest mismatch: '+f['path'])
    actual=sorted(str(f.relative_to(root)) for f in root.rglob('*') if f.is_file() and f.suffix in {'.tex','.py','.md'} and 'evidence' not in f.relative_to(root).parts)
    if actual!=sorted(n for n in names if Path(n).suffix in {'.tex','.py','.md'}): raise RuntimeError('unmanifested native source')
    seen=[]
    def visit(name):
        if name in seen: raise RuntimeError('duplicate TeX input: '+name)
        seen.append(name); text=(root/name).read_text()
        for child in re.findall(r'\\input\{([^}]+)\}',text): visit(child if child.endswith('.tex') else child+'.tex')
    visit('main.tex')
    if set(seen)!={n for n in names if n.endswith('.tex')}: raise RuntimeError('inactive TeX source')
    text='\n'.join((root/n).read_text() for n in seen)
    labels=re.findall(r'\\label\{([^}]+)\}',text)
    refs=re.findall(r'\\(?:eqref|ref|autoref)\{([^}]+)\}',text)
    bib=re.findall(r'\\bibitem\{([^}]+)\}',text)
    cites=[x.strip() for group in re.findall(r'\\cite(?:\[[^\]]*\])?\{([^}]+)\}',text) for x in group.split(',')]
    if len(labels)!=len(set(labels)) or set(refs)-set(labels): raise RuntimeError('duplicate or missing label')
    if len(bib)!=len(set(bib)) or set(cites)-set(bib): raise RuntimeError('duplicate or missing citation')
    if set(bib)-set(cites): raise RuntimeError('uncited bibliography entry')
    statements=re.findall(r'\\begin\{(?:theorem|proposition|lemma|corollary)\}',text)
    proofs=re.findall(r'\\begin\{proof\}',text)
    if len(statements)!=len(proofs): raise RuntimeError('statement/proof inventory mismatch')
    files={n:(root/n).read_bytes() for n in names};files['SOURCE_MANIFEST.json']=(root/'SOURCE_MANIFEST.json').read_bytes()
    return {'source_files':len(files),'tex_files':len(seen),'formal_statements':len(statements),'proofs':len(proofs),'labels':len(labels),'bibliography_entries':len(bib),'native_tree_sha':tree_hash(files),'manifest_sha256':sha256(files['SOURCE_MANIFEST.json'])}

if __name__=='__main__': print(json.dumps(audit(),sort_keys=True))
