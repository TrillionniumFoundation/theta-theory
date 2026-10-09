#!/usr/bin/env python3
from pathlib import Path
import hashlib,json,re
import verify_v11
ROOT=Path(__file__).resolve().parents[1]
V11=ROOT.parent/'A2-DYN-v11-referee-response'
V10=ROOT.parent/'A2-DYN-v10-referee-response'
def req(c,m):
    if not c: raise RuntimeError(m)
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def source_checks():
    man=json.loads((ROOT/'SOURCE_MANIFEST.json').read_text())
    req(man['revision']==12,'wrong revision')
    core=sorted((ROOT/'core').glob('*.tex'))
    req(len(core)==29,'expected 29 core files')
    for p in sorted((V11/'core').glob('*.tex')):
        if p.name in {'06_downstream.tex','28_marked_return_band.tex'}: continue
        req(p.read_bytes()==(ROOT/'core'/p.name).read_bytes(),'changed unrepaired v11 mathematics: '+p.name)
    req((ROOT/'core/06_downstream.tex').read_bytes()==(V10/'core/06_downstream.tex').read_bytes(),
        '06_downstream.tex is not exact reviewed-v10 content')
    main=(ROOT/'main.tex').read_text()
    mark=(ROOT/'core/28_marked_return_band.tex').read_text()
    req('A2-DYN, revision 12' in main,'stale revision metadata')
    req('\\nef{' not in main,'malformed ref remains')
    req('}.+\\]' not in mark,'stray marked-event fragment remains')
    inputs=re.findall(r'\\input\{(core/[^}]+)\}',main)
    req(len(inputs)==len(set(inputs))==29,'missing or duplicate core inclusion')
    req(set(s+'.tex' for s in inputs)==set(str(p.relative_to(ROOT)) for p in core),'unlisted core source')
    tex=main+'\n'+'\n'.join((ROOT/(s+'.tex')).read_text() for s in inputs)
    labels=re.findall(r'\\label\{([^}]+)\}',tex)
    req(len(labels)==len(set(labels)),'duplicate label')
    refs=set(re.findall(r'\\(?:ref|eqref|pageref|autoref)\{([^}]+)\}',tex))
    req(refs<=set(labels),'unresolved refs: '+str(refs-set(labels)))
    cites=set()
    for g in re.findall(r'\\cite(?:\[[^\]]*\])?\{([^}]+)\}',tex):
        cites.update(x.strip() for x in g.split(','))
    bib=set(re.findall(r'\\bibitem\{([^}]+)\}',(ROOT/'references.tex').read_text()))
    req(cites<=bib,'unresolved citation')
    for env in ['theorem','lemma','proposition','corollary','proof','maintheorem']:
        req(tex.count('\\begin{'+env+'}')==tex.count('\\end{'+env+'}'),'unbalanced '+env)
    return {'core_files':len(core),'labels':len(labels),'proofs':tex.count(r'\begin{proof}'),
            'restored_v10_downstream_sha256':sha(ROOT/'core/06_downstream.tex'),
            'tex_sha256':{str(p.relative_to(ROOT)):sha(p) for p in sorted(ROOT.rglob('*.tex'))}}
def finite_checks(): return verify_v11.finite_checks()
if __name__=='__main__':
    print(json.dumps({'revision':12,'source':source_checks(),'finite':finite_checks(),
      'continuum_proof_certified':False,'full_raw_LLT_certified':False,
      'independent_human_review':False},indent=2,sort_keys=True))
