#!/usr/bin/env python3
"""Pinned-source preservation and static reference audit; not proof certification."""
from __future__ import annotations
import hashlib,json,re
from pathlib import Path
P=Path(__file__).resolve().parents[1]
H=P/'history/v45-review-baseline'
ADDED={'article/01g_quantized_reconstruction_overview_v46.tex','article/23k_quantized_law_stability_v46.tex'}
CHANGED={'main.tex','article/01f_generic_rigidity_overview_v45.tex','article/23j_generic_finite_channel_rigidity_v45.tex','v5/references_v43.tex'}

def require(ok: bool,msg: str) -> None:
    if not ok:raise RuntimeError(msg)

def blob(data: bytes) -> str:
    return hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()

def closure(entry: str) -> dict[str,str]:
    files={}
    def visit(name):
        require('..' not in Path(name).parts,'Unsafe source input')
        if name in files:return
        text=(P/name).read_text();files[name]=text
        plain=re.sub(r'(?<!\\)%[^\n]*','',text)
        for n in re.findall(r'\\(?:input|include)\{([^}]+)\}',plain):visit(n if n.endswith('.tex') else n+'.tex')
    visit(entry);return files

def theorem_blocks(text: str) -> list[str]:
    return re.findall(r'\\begin\{(theorem|lemma|proposition|corollary|definition|remark|proof)\}.*?\\end\{\1\}',text,re.S)

def main():
    manifest=json.loads((H/'active-source-manifest.json').read_text())
    current=closure('main.tex');old={};verified=0
    for entry,files in manifest.items():
        for name,identity in files.items():
            path=H/name if name in CHANGED else P/name
            data=path.read_bytes()
            require(blob(data)==identity['git_blob'],'Changed baseline input: '+name)
            require(hashlib.sha256(data).hexdigest()==identity['sha256'],'Baseline SHA mismatch: '+name)
            if entry=='main':old[name]=data.decode()
            verified+=1
    require(set(current)==set(manifest['main'])|ADDED,'Native input closure changed unexpectedly')
    inp=lambda s:re.findall(r'\\input\{([^}]+)\}',s)
    require([x for x in inp(current['main.tex']) if x+'.tex' not in ADDED]==inp(old['main.tex']),'Inherited input order changed')
    # Every inherited mathematical environment is retained verbatim except P1.
    pattern=r'\\begin\{(theorem|lemma|proposition|corollary|definition|remark|proof)\}.*?\\end\{\1\}'
    inherited_blocks=0
    for name,text in old.items():
        before=[m.group() for m in re.finditer(pattern,text,re.S)]
        after=[m.group() for m in re.finditer(pattern,current[name],re.S)]
        before=[v.replace('zero-gain edge followed by its reverse','zero-net-gain backtrack $ee^{-1}$') for v in before]
        require(before==after,'Inherited theorem/proof block changed: '+name)
        inherited_blocks+=len(before)
    name='article/23j_generic_finite_channel_rigidity_v45.tex'
    require(current[name]==old[name].replace('zero-gain edge followed by its reverse','zero-net-gain backtrack $ee^{-1}$'),'Unapproved change in generic theorem module')
    plain=re.sub(r'(?<!\\)%[^\n]*','','\n'.join(current.values()))
    labels=re.findall(r'\\label\{([^}]+)\}',plain)
    require(len(labels)==len(set(labels)),'Duplicate labels')
    refs=set(re.findall(r'\\(?:ref|eqref|pageref)\{([^}]+)\}',plain))
    require(not {r for r in refs-set(labels) if not r.startswith('TC-')},'Unresolved reference: '+str(refs-set(labels)))
    citations={c.strip() for x in re.findall(r'\\cite(?:\[[^]]*\])?\{([^}]+)\}',plain) for c in x.split(',')}
    bib=set(re.findall(r'\\bibitem(?:\[[^]]*\])?\{([^}]+)\}',plain))
    require(citations<=bib,'Undefined citation: '+str(citations-bib))
    env=r'\\begin\{(?:theorem|lemma|proposition|corollary|definition)\}'
    allpath=set(manifest['main'])|set(manifest['two_collision'])
    print(json.dumps({'status':'passed','baseline_source':'2f064b86b4e071d24ad671f4dc652d7de32a56a4',
      'baseline_manifest_entries_verified':verified,'main_inputs':len(current),'companion_inputs':len(closure('two_collision.tex')),
      'unchanged_active_files':len(allpath-CHANGED),'archived_modified_active_files':sorted(CHANGED),
      'retained_theorem_style_environments':sum(len(re.findall(env,t)) for t in old.values()),
      'retained_remark_environments':sum(t.count(r'\begin{remark}') for t in old.values()),
      'retained_mathematical_environment_blocks':inherited_blocks,
      'added_theorem_style_environments':sum(len(re.findall(env,current[n])) for n in ADDED),
      'active_source_sha256':{n:hashlib.sha256((P/n).read_bytes()).hexdigest() for n in sorted(current)},
      'proof_certification':False},sort_keys=True,indent=2))
if __name__=='__main__':main()
