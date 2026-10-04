#!/usr/bin/env python3
"""Editorial/source contract tests. These are not continuum proof tests."""
from __future__ import annotations
import hashlib,json,re,sys
from pathlib import Path
import validate_v41 as inherited
ROOT=Path(__file__).resolve().parents[1]


def require(ok:bool,message:str)->None:
    if not ok: raise ValueError(message)


def inspect(texts:dict[str,str], blobs:dict[str,bytes], contract:dict)->None:
    for name,sha in contract['frozen_sources'].items():
        require(name in blobs and hashlib.sha256(blobs[name]).hexdigest()==sha,'frozen source changed: '+name)
    for name in contract['journal_front_matter']:
        require(name in blobs and 'v43' in blobs[name].decode().splitlines()[0], 'stale/missing front matter: '+name)
    for name in ('main.tex','companion.tex'):
        require(name in texts,'missing journal document')
    graph=contract['dependencies'];seen=set();active=set()
    def visit(node):
        require(node not in active,'cyclic theorem dependency')
        if node in seen:return
        active.add(node)
        for dep in graph.get(node,[]):visit(dep)
        active.remove(node);seen.add(node)
    for node in graph:visit(node)
    main=texts['main.tex'];abstract=main.split(r'\begin{abstract}',1)[1].split(r'\end{abstract}',1)[0]
    require('\n\n' in abstract and 'whole-plane' in abstract and 'finitely sampled bits' in abstract,'exact/finite abstract separation')
    require('BV' in abstract and 'local spatial' in abstract and 'patch' in abstract,'abstract norm/period distinction')
    intro=texts['core/00j_two_field_introduction.tex'];law=texts['core/23_two_field_law.tex']
    require('tab:exact-finite-claims' in intro and 'deterministic' in intro, 'missing claim table or alternative')
    label=r'\label{eq:two-field-joint-default-cost}'
    require(label in law,'missing default law budget')
    default=law.split(label,1)[1].split(r'\end{equation}',1)[0]
    require('a_m^{-2}' in default and 'a_m^{-4}' not in default,'wrong default exponent')
    require(law.index(label)<law.index(r'\label{eq:two-field-joint-decomposed-cost}'),'default not first')
    require('retained deterministic all-node alternative' in law and 'm^2a_m^{-4}' in law,'deterministic proof/result not retained')
    require('does not assume that bound as an input' in law,'missing dependency explanation')
    exact=['core/21_two_field_rigidity.tex','core/24_measure_support.tex','core/25_nonsmooth_curvature.tex']
    require(all(not re.search(r'\\(?:eqref|ref)\{H-',texts[n]) for n in exact),'exact proof depends on supplement')
    require(contract['independent_human_review_completed'] is False,'manufactured human review')


def main()->int:
    try:
        closure=inherited.tex_document_inputs(ROOT)
        texts={n:(ROOT/n).read_text() for n in set().union(*map(set,closure.values()))}
        contract=json.loads((ROOT/'JOURNAL_INTERFACE.json').read_text())
        names=set(texts)|set(contract['journal_front_matter'])
        blobs={n:(ROOT/n).read_bytes() for n in names}
        inspect(texts,blobs,contract)
        refs={doc:sorted(set(re.findall(r'\\(?:ref|eqref)\{((?:H-|M-)[^}]+)\}','\n'.join(texts[n] for n in ns)))) for doc,ns in closure.items()}
        require(refs==contract['cross_document_references'],'cross-document symbol interface changed')
        rejected=[]
        mutations=[]
        for target in contract['frozen_sources']:
            b=dict(blobs);b[target]+=b'\n';mutations.append(('changed '+target,texts,b,contract))
        for target in contract['journal_front_matter']:
            b=dict(blobs);b[target]=b[target].replace(b'v43',b'v41',1);mutations.append(('stale '+target,texts,b,contract))
        t=dict(texts);t.pop('companion.tex');mutations.append(('missing companion',t,blobs,contract))
        t=dict(texts);t['core/23_two_field_law.tex']=t['core/23_two_field_law.tex'].replace('a_m^{-2}','a_m^{-4}');mutations.append(('regressed default exponent',t,blobs,contract))
        t=dict(texts);t['main.tex']=t['main.tex'].replace('finitely sampled bits','fields');mutations.append(('merged data models',t,blobs,contract))
        c=json.loads(json.dumps(contract));c['dependencies']['geometry']=['default_joint'];mutations.append(('circular proof graph',texts,blobs,c))
        c=json.loads(json.dumps(contract));c['independent_human_review_completed']=True;mutations.append(('fabricated human review',texts,blobs,c))
        for name,t,b,c in mutations:
            try:inspect(t,b,c)
            except ValueError:rejected.append(name)
            else:raise ValueError('mutation escaped: '+name)
        result={'schema':'a2-v43-contract-tests-1','status':'passed','negative_tests':len(rejected),'rejected_mutations':rejected,'cross_document_references':refs,'formal_proof_certificate':False,'human_specialist_review':False}
        print(json.dumps(result,sort_keys=True,separators=(',',':')));return 0
    except Exception as exc:
        print(json.dumps({'status':'failed','error':str(exc)},sort_keys=True));return 1
if __name__=='__main__':sys.exit(main())
