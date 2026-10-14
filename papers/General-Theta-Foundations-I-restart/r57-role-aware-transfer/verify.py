#!/usr/bin/env python3
"""Read-only source consistency checks. These are not theorem verification."""
from pathlib import Path
import hashlib,json,re,os
ROOT=Path(__file__).resolve().parent
REVIEW='review_inputs/R56_EXTERNAL_REFEREE_REPORT.md'
REVIEW_BLOB='15c692a39c17a34a408e2979f049c87b804179f8'
def require(test,message):
    if not test:raise RuntimeError(message)
def sha256(data):return hashlib.sha256(data).hexdigest()
def git_hash(kind,data):return hashlib.sha1(kind.encode()+b' '+str(len(data)).encode()+b'\0'+data).hexdigest()
def tree_hash(files):
    root={}
    for name,data in files.items():
        node=root;parts=name.split('/')
        for part in parts[:-1]:node=node.setdefault(part,{})
        node[parts[-1]]=data
    def encode(node):
        body=b''
        for name,value in sorted(node.items(),key=lambda z:z[0]+('/' if isinstance(z[1],dict) else '')):
            kind='tree' if isinstance(value,dict) else 'blob';mode='40000' if kind=='tree' else '100644'
            digest=encode(value) if kind=='tree' else git_hash(kind,value)
            body+=mode.encode()+b' '+name.encode()+b'\0'+bytes.fromhex(digest)
        return git_hash('tree',body)
    return encode(root)
def ordinary_files():
    return {p.relative_to(ROOT).as_posix():p.read_bytes() for p in sorted(ROOT.rglob('*')) if p.is_file() and not set(p.relative_to(ROOT).parts)&{'artifacts','evidence','__pycache__','transport'} and p.name!='SOURCE_MANIFEST.json'}
def verify():
    manifest=json.loads((ROOT/'SOURCE_MANIFEST.json').read_text());files=ordinary_files()
    require(set(files)==set(manifest['files']),'ordinary-source inventory mismatch')
    for name,data in files.items():
        require(not (ROOT/name).is_symlink(),'symlink input '+name)
        require(sha256(data)==manifest['files'][name],'source digest mismatch '+name)
    report_verified=REVIEW in files and git_hash('blob',files[REVIEW])==REVIEW_BLOB
    require(report_verified,'exact R56 report required')
    active=[]
    def load(name):
        require(name in files,'undeclared TeX input '+name)
        if name in active:return
        active.append(name)
        for target in re.findall(r'\\input\{([^}]+)\}',files[name].decode()):load(target if target.endswith('.tex') else target+'.tex')
    load('main.tex');text='\n'.join(files[name].decode() for name in active)
    labels=re.findall(r'\\label\{([^}]+)\}',text);refs=re.findall(r'\\(?:eqref|ref)\{([^}]+)\}',text)
    cites=[v.strip() for item in re.findall(r'\\cite\{([^}]+)\}',text) for v in item.split(',')];bib=re.findall(r'\\bibitem\{([^}]+)\}',text)
    require(len(labels)==len(set(labels)),'duplicate label');require(set(refs)<=set(labels),'unresolved label '+str(set(refs)-set(labels)))
    require(len(bib)==len(set(bib)) and set(cites)<=set(bib),'bibliography mismatch')
    require(set(active)=={n for n in files if n.endswith('.tex')},'inactive native TeX')
    require(not re.search(r'\b(?:TODO|FIXME|TBD)\b',text),'unfinished manuscript marker')
    require({'thm:main','def:stopping','lem:packing','thm:approx','prop:sharp-approx','thm:directional','prop:role-composition','prop:moment','thm:joint'}<=set(labels),'missing central obligations')
    statements=len(re.findall(r'\\begin\{(?:theorem|lemma|proposition|corollary|definition|example)\}',text))
    return {'status':'PASS','ordinary_source_projection_tree_sha':tree_hash(files),'source_files':len(files),'manifest_sha256':sha256((ROOT/'SOURCE_MANIFEST.json').read_bytes()),'review_input_verified':report_verified,'review_input_git_blob':REVIEW_BLOB,'native':{'active_tex':sorted(active),'labels':len(labels),'cross_references':len(refs),'bibliography_items':len(bib),'citation_uses':len(cites),'formal_statements':statements},'scope':'source consistency, not proof validity or significance'}
if __name__=='__main__':print(json.dumps(verify(),sort_keys=True,indent=2))
