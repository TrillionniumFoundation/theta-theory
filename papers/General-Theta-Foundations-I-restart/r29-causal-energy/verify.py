#!/usr/bin/env python3
"""Read-only mathematical-source inventory. It is not a proof checker."""
from __future__ import annotations
import hashlib,json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parent
EXCLUDED={'artifacts','evidence','__pycache__','.git','review_inputs'}
REPORT='79c032f1bd1697722d44206dfb28f48b1cdf2311'
def require(ok:bool,message:str)->None:
    if not ok: raise RuntimeError(message)
def sha256(data:bytes)->str:return hashlib.sha256(data).hexdigest()
def git_hash(kind:str,data:bytes)->str:return hashlib.sha1((kind+' '+str(len(data))).encode()+b'\0'+data).hexdigest()
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
def tex_audit(root:Path)->dict:
    active=[]
    def visit(name):
        require(name not in active,'duplicate/cyclic input '+name);active.append(name)
        require((root/name).is_file(),'missing TeX '+str(root/name))
        for child in re.findall(r'\\input\{([^}]+)\}',(root/name).read_text()):
            require(not Path(child).is_absolute() and '..' not in Path(child).parts,'nonlocal TeX input')
            visit(child if child.endswith('.tex') else child+'.tex')
    visit('main.tex')
    expected=sorted([p.relative_to(root).as_posix() for p in (root/'sections').glob('*.tex')]+['main.tex','references.tex'])
    require(sorted(active)==expected,'inactive or missing mathematical input')
    text='\n'.join((root/n).read_text() for n in active)
    labels=re.findall(r'\\label\{([^}]+)\}',text);refs=re.findall(r'\\(?:eqref|ref)\{([^}]+)\}',text)
    bib=re.findall(r'\\bibitem\{([^}]+)\}',text);cites=[k.strip() for g in re.findall(r'\\cite\{([^}]+)\}',text) for k in g.split(',')]
    require(len(labels)==len(set(labels)),'duplicate labels');require(set(refs)<=set(labels),'unresolved references: '+repr(set(refs)-set(labels)))
    require(len(bib)==len(set(bib)),'duplicate bibliography');require(set(cites)==set(bib),'missing/unused literature: '+repr(set(cites)^set(bib)))
    envs=('theorem','proposition','lemma','corollary','definition','remark','proof');counts={e:len(re.findall(r'\\begin\{'+e+r'\}',text)) for e in envs}
    for e in envs:require(counts[e]==len(re.findall(r'\\end\{'+e+r'\}',text)),'unbalanced '+e)
    require('v97' not in text and 'SOURCE_SHA' not in text,'workflow text in mathematics')
    return {'active_tex':active,'labels':len(labels),'references':len(refs),'bibliography_entries':len(bib),'statement_counts':counts,'formal_statements':sum(counts[e] for e in envs if e not in ('proof','remark'))}
def verify(root:Path=ROOT)->dict:
    manifest=json.loads((root/'SOURCE_MANIFEST.json').read_text());names=sources(root)
    require(names==sorted(manifest['files']),'source inventory differs')
    for name in names:
        data=(root/name).read_bytes();item=manifest['files'][name]
        require(not any(c<32 and c not in (9,10) for c in data),'control byte '+name)
        require(sha256(data)==item['sha256'] and git_hash('blob',data)==item['git_blob_sha'],'source hash mismatch '+name)
    native=tex_audit(root);retained=tex_audit(root/'retained/companion_f')
    patches=json.loads((root/'RETAINED_PATCHES.json').read_text())
    for name,entry in patches['files'].items():
        require(sha256((root/'retained/companion_f'/name).read_bytes())==entry['retained_sha256'],'retained patch hash mismatch '+name)
    report=root/'review_inputs/R27_EXTERNAL_REFEREE_REPORT.md'
    if report.exists():require(git_hash('blob',report.read_bytes())==REPORT,'pinned review input changed')
    return {'status':'PASS','ordinary_files':len(names),'native':native,'retained_corrected_companion':retained,'ordinary_source_projection_tree_sha':source_tree(root),'review_input_verified':report.exists(),'review_blob_pin':REPORT,'projection_scope':'ordinary text excluding review_inputs, artifacts and evidence; actual native Git tree is separately recorded by publication','limitations':'source/label/citation audit, not a mathematical proof or full historical re-certification'}
if __name__=='__main__': print(json.dumps(verify(),sort_keys=True,indent=2))
