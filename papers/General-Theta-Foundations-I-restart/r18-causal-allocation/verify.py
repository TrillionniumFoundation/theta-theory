#!/usr/bin/env python3
"""Read-only native source audit; it does not verify mathematical theorems."""
from __future__ import annotations
import hashlib,json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parent
EXCLUDED={'artifacts','evidence','__pycache__','.git'}
def require(ok: bool,message: str)->None:
    if not ok:raise RuntimeError(message)
def sha256(data: bytes)->str:return hashlib.sha256(data).hexdigest()
def git_hash(kind: str,data: bytes)->str:return hashlib.sha1((kind+' '+str(len(data))).encode()+b'\0'+data).hexdigest()
def sources(root:Path=ROOT)->list[str]:
    return sorted(p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_file() and not EXCLUDED.intersection(p.relative_to(root).parts) and p.name!='SOURCE_MANIFEST.json')
def source_tree(root:Path=ROOT)->str:
    tree={}
    for name in sources(root)+['SOURCE_MANIFEST.json']:
        node=tree;parts=name.split('/')
        for part in parts[:-1]:node=node.setdefault(part,{})
        node[parts[-1]]=git_hash('blob',(root/name).read_bytes())
    def encode(node):
        data=b''
        for name,value in sorted(node.items(),key=lambda kv:kv[0]+('/' if isinstance(kv[1],dict) else '')):
            isdir=isinstance(value,dict);digest=encode(value) if isdir else value
            data+=('40000' if isdir else '100644').encode()+b' '+name.encode()+b'\0'+bytes.fromhex(digest)
        return git_hash('tree',data)
    return encode(tree)
def verify(root:Path=ROOT)->dict:
    manifest=json.loads((root/'SOURCE_MANIFEST.json').read_text());names=sources(root)
    require(names==sorted(manifest['files']),'source inventory differs from manifest')
    for name in names:
        data=(root/name).read_bytes();item=manifest['files'][name]
        require(not any(c<32 and c not in (9,10) for c in data),'unexpected control byte: '+name)
        require(sha256(data)==item['sha256'],'SHA256 mismatch: '+name)
        require(git_hash('blob',data)==item['git_blob_sha'],'Git blob mismatch: '+name)
    active=[]
    def visit(name):
        require(name not in active,'duplicate/cyclic TeX input: '+name);require(name in names,'unmanifested TeX: '+name)
        active.append(name)
        for child in re.findall(r'\\input\{([^}]+)\}',(root/name).read_text()):
            require(not Path(child).is_absolute() and '..' not in Path(child).parts,'out-of-native TeX input')
            visit(child if child.endswith('.tex') else child+'.tex')
    visit('main.tex');require(sorted(active)==sorted(n for n in names if n.endswith('.tex')),'inactive/missing TeX')
    text='\n'.join((root/n).read_text() for n in active)
    labels=re.findall(r'\\label\{([^}]+)\}',text);refs=re.findall(r'\\(?:eqref|ref)\{([^}]+)\}',text)
    bib=re.findall(r'\\bibitem\{([^}]+)\}',text)
    cites=[k.strip() for g in re.findall(r'\\cite\{([^}]+)\}',text) for k in g.split(',')]
    require(len(labels)==len(set(labels)),'duplicate labels');require(set(refs)<=set(labels),'missing references: '+str(set(refs)-set(labels)))
    require(len(bib)==len(set(bib)),'duplicate bibliography');require(set(cites)==set(bib),'missing/unused bibliography: '+str(set(cites)^set(bib)))
    envs=('theorem','proposition','lemma','corollary','definition','remark','proof')
    counts={e:len(re.findall(r'\\begin\{'+e+r'\}',text)) for e in envs}
    for e in envs:require(counts[e]==len(re.findall(r'\\end\{'+e+r'\}',text)),'unbalanced environment '+e)
    require('v97' not in text and 'SOURCE_SHA' not in text,'workflow/historical numbering in native prose')
    return {'status':'PASS','native_files':len(names),'active_tex':active,'labels':len(labels),'references':len(refs),'bibliography_entries':len(bib),'statement_counts':counts,'formal_statements':sum(counts[e] for e in envs if e not in ('proof','remark')),'native_source_tree_sha':source_tree(root),'scope':'native ordinary-source projection only; checks are not mathematical proofs'}
if __name__=='__main__':print(json.dumps(verify(),sort_keys=True,indent=2))
