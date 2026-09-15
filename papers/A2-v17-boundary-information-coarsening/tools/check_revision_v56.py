#!/usr/bin/env python3
"""Content preservation, explicit proof-reference closure, and finite controls.

Not a proof assistant, a new independent referee, or a journal acceptance test.
"""
from __future__ import annotations
from collections import Counter
import hashlib
import json
import re
import sympy as s
from source_provenance import require, blob_id, graph
from materialize_revision_v56 import P, ARCHIVE, amended_main
from check_revision_v50 import ENV, BLOCK
from check_revision_v55 import reduction_controls


def preservation():
    baseline=json.loads((ARCHIVE/'active-source-manifest.json').read_text())
    old={n:i for d in baseline.values() for n,i in d.items()}
    require(len(old)==111,'Wrong baseline graph')
    blocks=0; before=Counter(); labels=set()
    for name,info in old.items():
        data=(ARCHIVE/name if name=='main.tex' else P/name).read_bytes()
        require(len(data)==info['bytes'] and hashlib.sha256(data).hexdigest()==info['sha256']
                and blob_id(data)==info['git_blob'],'Baseline content mismatch: '+name)
        text=data.decode(); current=(P/name).read_text()
        require(current==(amended_main(text) if name=='main.tex' else text),'Unprescribed edit: '+name)
        for m in BLOCK.finditer(text):
            require(m.group(0) in current,'Inherited statement/proof changed: '+name);blocks+=1
        before.update(ENV.findall(text));labels.update(re.findall(r'\\label\{([^}]+)\}',text))
    full=graph(P,'main.tex')|graph(P,'two_collision.tex')
    require(full==set(old),'Complete technical graph changed')
    joined='\n'.join((P/n).read_text() for n in full)
    require(Counter(ENV.findall(joined))==before,'Full mathematical inventory changed')
    dep=json.loads((P/'journal/DEPENDENCY_MAP_V56.json').read_text())
    principal=graph(P,'rigidity.tex')
    require(set(dep['principal_inputs'])==principal,'Principal input graph mismatch')
    for src,dst in dep['display_views'].items():
        a,b=dep['display_edits'][src]
        original=(P/src).read_text();view=(P/dst).read_text()
        require(original.count(a)==1 and view==original.replace(a,b,1),'Unexpected presentation view')
        for match in BLOCK.finditer(original):
            require(match.group(0) in view,'Presentation changed proof or theorem: '+src)
    orig=(P/'article/00_structural_introduction_v48.tex').read_text()
    extracted=(P/'journal/01_structural_statements_v56.tex').read_text()
    a=orig.index(r'\subsection{The observation and the main theorem}')
    b=orig.index(r'\subsection{Proof of the geometric inverse}')
    require(extracted==orig[a:b],'Structural statements not exact shared text')
    texts={n:(P/n).read_text() for n in principal}
    plabels=[l for t in texts.values() for l in re.findall(r'\\label\{([^}]+)\}',t)]
    require(len(plabels)==len(set(plabels)),'Duplicate principal labels')
    external=set(dep['external_comparison_labels'])
    references={l for n,t in texts.items() if not n.endswith('full_reference_routes_v56.tex')
                for l in re.findall(r'\\(?:ref|eqref|autoref|pageref)\{([^}]+)\}',t)}
    require(references-set(plabels)==external and external<=labels,'Wrong cross-document reference set')
    for n,t in texts.items():
        for proof in re.findall(r'\\begin\{proof\}.*?\\end\{proof\}',t,re.S):
            refs=set(re.findall(r'\\(?:ref|eqref|autoref|pageref)\{([^}]+)\}',proof))
            require(not refs&external,'Full-only reference inside principal proof: '+n)
    # For the principal record, count every finite non-proof cross-reference explicitly.
    for stem,files in [('full',full),('principal',principal)]:
        text='\n'.join((P/n).read_text() for n in files)
        cites={k.strip() for c in re.findall(r'\\cite(?:\[[^\]]*\])?\{([^}]+)\}',text) for k in c.split(',')}
        bib=set(re.findall(r'\\bibitem(?:\[[^\]]*\])?\{([^}]+)\}',text))
        require(cites<=bib,'Unresolved '+stem+' bibliography')
    return {'inherited_active_inputs':len(old),'byte_identical_in_place':len(old)-1,
      'metadata_only_input':'main.tex','inherited_blocks_preserved_verbatim':blocks,
      'inherited_environments':dict(sorted(before.items())),
      'full_active_inputs':len(full),'principal_active_inputs':len(principal),
      'combined_unique_active_inputs':len(full|principal),
      'principal_labels':len(plabels),'external_comparison_labels':sorted(external),
      'external_labels_in_principal_proof_environments':[],
      'presentation_views':dep['display_views'],
      'scope':'Historical block retention and static reference closure; not semantic proof certification.'}


def coordinate_controls():
    # A non-even graph; local Legendre conversion through degree five.
    p=s.symbols('p'); k,q3,q4,q5=s.symbols('k q3 q4 q5',nonzero=True)
    a2,a3,a4=s.symbols('a2 a3 a4')
    y=p/k+a2*p**2+a3*p**3+a4*p**4
    psi=lambda v:k*v**2/2+q3*v**3/6+q4*v**4/24+q5*v**5/120
    eq=s.series(k*y+q3*y*y/2+q4*y**3/6+q5*y**4/24-p,p,0,5).removeO()
    solutions={}
    for n,a in [(2,a2),(3,a3),(4,a4)]:solutions[a]=s.solve(eq.subs(solutions).coeff(p,n),a)[0]
    y=y.subs(solutions)
    H=s.series(p*y-psi(y),p,0,6).removeO()
    require(s.expand(s.diff(H,p)-y)==0,'Legendre derivative does not recover inverse gradient')
    require(s.simplify(H.coeff(p,3)+q3/(6*k**3))==0,'Odd signed coefficient lost')
    z,r=s.symbols('z r',nonzero=True)
    determinants=[]
    for n in range(3,13):
        c=(1+z**(2*n))/(1-z**(2*n));t=2*z**n/(1-z**(2*n))
        matrix=s.Matrix([[c,r**n*t],[r**(-n)*t,c]])
        require(s.factor(matrix.det())==1,'Wrong signed contact block')
        determinants.append(n)
    return {'graph_support_Legendre_orders':list(range(2,6)),
      'odd_cubic_term_checked':True,'signed_block_orders':determinants,
      'scope':'Exact finite coordinate/algebra controls only; no infinite-order or statistical claim.'}

if __name__=='__main__':
    print(json.dumps({'status':'passed','mathematical_certification':False,
      'preservation':preservation(),'coordinate_controls':coordinate_controls(),
      'retained_v55_stopping_controls':reduction_controls()},sort_keys=True,indent=2))
