#!/usr/bin/env python3
"""Verbatim preservation and exact finite interaction controls for A2 v51.

No finite symbolic test below certifies an infinite-flight estimate or
performs a statistical reconstruction from samples.
"""
from __future__ import annotations
from collections import Counter
import hashlib
import json
import re
import sympy as s
from materialize_revision_v51 import P, ARCHIVE, CHANGES, NEW_INPUTS, revised
from source_provenance import require, blob_id, graph
from check_revision_v50 import ENV, BLOCK, two_branch_controls
from check_revision_v49 import new_controls as v49_controls
from check_revision_v48 import differential_controls as v48_controls
from check_revision_v47 import finite_diagnostics as v47_controls


def preservation() -> dict:
    groups=json.loads((ARCHIVE/'active-source-manifest.json').read_text())
    old={n:v for group in groups.values() for n,v in group.items()}
    require(len(old)==107,'Wrong reviewed baseline count')
    before=Counter();oldlabels=set();blocks=0
    for name,info in old.items():
        raw=(ARCHIVE/name if name in CHANGES else P/name).read_bytes()
        require(len(raw)==info['bytes'] and hashlib.sha256(raw).hexdigest()==info['sha256']
                and blob_id(raw)==info['git_blob'],'Baseline identity: '+name)
        text=raw.decode();current=(P/name).read_text()
        before.update(ENV.findall(text));oldlabels.update(re.findall(r'\\label\{([^}]+)\}',text))
        if name in CHANGES:
            require(current==revised(name,text),'Non-prescribed edit: '+name)
        for match in BLOCK.finditer(text):
            require(match.group(0) in current,'Changed old statement/proof: '+name)
            blocks+=1
        oldorder=re.findall(r'\\input\{([^}]+)\}',text)
        neworder=re.findall(r'\\input\{([^}]+)\}',current)
        require([x for x in neworder if x+'.tex' not in NEW_INPUTS]==oldorder,
                'Inherited relative input order changed: '+name)
    active=graph(P,'main.tex')|graph(P,'two_collision.tex')
    require(active==set(old)|set(NEW_INPUTS),'Lost or unexpected active input')
    joined='\n'.join((P/n).read_text() for n in sorted(active))
    added=Counter()
    for n in NEW_INPUTS:added.update(ENV.findall((P/n).read_text()))
    require(Counter(ENV.findall(joined))==before+added,'Environment retention mismatch')
    labels=re.findall(r'\\label\{([^}]+)\}',joined)
    require(len(labels)==len(set(labels)) and oldlabels<=set(labels),'Lost/duplicate label')
    refs=set(re.findall(r'\\(?:ref|eqref|pageref|autoref)\{([^}]+)\}',joined))
    require(not {r for r in refs if r not in labels and not r.startswith('TC-')},'Unresolved references')
    cites={k.strip() for c in re.findall(r'\\cite(?:\[[^\]]*\])?\{([^}]+)\}',joined) for k in c.split(',')}
    bib=set(re.findall(r'\\bibitem(?:\[[^\]]*\])?\{([^}]+)\}',joined))
    require(cites<=bib,'Unresolved citation')
    main=(P/'main.tex').read_text()
    require(main.index(r'\input{article/01_introduction_v41}')>main.index(r'\appendix'),
            'The collected material no longer compiles in the appendix')
    return {'baseline_inputs':len(old),'active_inputs':len(active),
        'unchanged_in_place':len(old)-len(CHANGES),'archived_exact_originals':list(CHANGES),
        'new_inputs':list(NEW_INPUTS),'all_inherited_blocks_preserved_verbatim':blocks,
        'inherited_environments':dict(sorted(before.items())),
        'added_environments':dict(sorted(added.items())),
        'active_labels':len(labels),'unresolved_references_or_citations':[]}


def interaction_controls() -> dict:
    x,y,u,v,z,t=s.symbols('x y u v z t',real=True)
    d=s.Rational(2);xi=s.Rational(2,7);eta=-s.Rational(3,11);a=s.Rational(1,4)
    def S(z):return s.Rational(1,2)*z**2+s.Rational(1,15)*z**3+s.Rational(1,20)*z**4
    def Sp(z):return z+z**2/5+z**3/5
    # Positive curvature is global for this polynomial, not just sampled.
    require(s.expand(s.diff(S(z),z,2)-(s.Rational(3,5)*(z+s.Rational(1,3))**2+s.Rational(14,15)))==0,
            'Strict convexity identity')
    H=d-S(x-xi)-S(y-eta)
    f=(2+(x+1)**2)*(3+(y-2)**2)*H/7
    K=s.cancel(s.diff(f,x,y)/f-s.diff(f,x)*s.diff(f,y)/f**2)
    expected=-Sp(x-xi)*Sp(y-eta)/H**2
    require(s.cancel(K-expected)==0,'Separable weights did not cancel')
    require(s.cancel(K.subs(x,xi))==0 and s.cancel(K.subs(y,eta))==0,'Origin zero lines')
    sx=s.cancel(s.diff(K,x).subs({x:xi,y:eta+a}))
    sy=s.cancel(s.diff(K,y).subs({x:xi+a,y:eta}))
    require(sx==-Sp(a)/(d-S(a))**2 and sy==sx and sx!=0,'Simple-root slopes')
    fc=s.expand(f.subs({x:xi+u,y:eta+v}))
    R=s.cancel(fc*fc.subs({u:0,v:0})/(fc.subs(v,0)*fc.subs(u,0)))
    target=1-S(u)*S(v)/((d-S(u))*(d-S(v)))
    require(s.cancel(R-target)==0,'Asymmetric endpoint factors in anchored ratio')
    q=S(a)/(d-S(a))
    require(q>0 and s.cancel(1-R.subs({u:a,v:a})-q**2)==0,'Positive scalar anchor')
    rec=s.cancel(d*(1-R.subs(v,a))/(q+1-R.subs(v,a)))
    require(s.cancel(rec-S(u))==0,'Signed action extraction')
    samples=[-s.Rational(2,5),-s.Rational(1,5),0,s.Rational(1,5),s.Rational(2,5)]
    require(all(rec.subs(u,w)==S(w) for w in samples),'Signed point control')
    require(S(a)-S(-a)==2*a**3/15 and S(a)!=S(-a),'Odd term lost')
    require(fc.subs({u:a,v:0})!=fc.subs({u:0,v:a}),'Unequal endpoint profiles not exercised')
    # The zero-fiber differential follows the translated geometry, even with
    # a simultaneous signed action perturbation. No density symmetry is used.
    cx=s.Rational(3,5);cy=-s.Rational(2,9)
    def St(z):return S(z)+t*z**3/7
    def Spt(z):return Sp(z)+3*t*z**2/7
    ht=d-St(x-xi-cx*t)-St(y-eta-cy*t)
    kt=-Spt(x-xi-cx*t)*Spt(y-eta-cy*t)/ht**2
    dkx=s.cancel(s.diff(kt,t).subs({t:0,x:xi,y:eta+a}))
    dky=s.cancel(s.diff(kt,t).subs({t:0,x:xi+a,y:eta}))
    require(-dkx/sx==cx and -dky/sy==cy,'Origin derivative sign')
    # Wrongly freezing the numerical origins misses the transport terms.
    require(dkx!=0 and dky!=0,'Stationary-origin shortcut not detected')
    joint=x*y
    require(s.diff(x**3+y**4,x,y)==0 and s.diff(joint,x,y)==1,
            'Separate/joint efficiency distinction')
    require(s.simplify((K+s.diff(joint,x,y)).subs({x:xi,y:eta+a}))==1,
            'A joint factor should destroy the zero-fiber criterion')
    return {'strict_convexity_lower_bound':'14/15','unknown_origins':[str(xi),str(eta)],
        'separate_unequal_endpoint_factors_cancel':True,'origin_zero_lines':True,
        'simple_root_slope':str(sx),'scalar_anchor':str(q),
        'signed_action_recovered_exactly':True,'signed_point_checks':len(samples),
        'origin_velocities_recovered':[str(cx),str(cy)],
        'negative_controls':['freezing the unknown origins misses transport',
          'replacing signed coordinates by absolute values loses the cubic term',
          'a joint exponential xy recording factor shifts the interaction by one'],
        'scope':'Exact finite functional identities, not a realized billiard table, Banach-space proof, or finite-sample certificate.'}

if __name__=='__main__':
    print(json.dumps({'status':'passed','mathematical_certification':False,
        'preservation':preservation(),'interaction_controls':interaction_controls(),
        'retained_v50_controls':two_branch_controls(),'retained_v49_controls':v49_controls(),
        'retained_v48_controls':v48_controls(),'retained_v47_controls':v47_controls()},
        sort_keys=True,indent=2))
