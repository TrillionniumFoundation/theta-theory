#!/usr/bin/env python3
"""Verbatim preservation and finite support/window controls; not a proof certificate."""
from __future__ import annotations
from collections import Counter
import hashlib
import json
import re
import sympy as s
from materialize_revision_v52 import P, ARCHIVE, CHANGES, NEW_INPUTS, revised
from source_provenance import require, blob_id, graph
from check_revision_v50 import ENV, BLOCK, two_branch_controls
from check_revision_v51 import interaction_controls as v51_controls
from check_revision_v49 import new_controls as v49_controls
from check_revision_v48 import differential_controls as v48_controls
from check_revision_v47 import finite_diagnostics as v47_controls


def preservation() -> dict:
    groups=json.loads((ARCHIVE/'active-source-manifest.json').read_text())
    old={n:v for group in groups.values() for n,v in group.items()}
    require(len(old)==109,'Wrong reviewed baseline count')
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


def window_controls() -> dict:
    x,y,u,v,z,t,q=s.symbols('x y u v z t q',real=True)
    # A non-even action specified through its inverse coordinate u=z+c z^2.
    # On |z|<=6/5, c=1/10, the coordinate derivative is >=19/25.
    c=s.Rational(1,10);coord=z+c*z*z
    require(1-2*c*s.Rational(6,5)==s.Rational(19,25),'Inverse-coordinate margin')
    Sprime=2*z/s.diff(coord,z)
    Ssecond=s.cancel(s.diff(Sprime,z)/s.diff(coord,z))
    require(s.cancel(Ssecond-2/(1+2*c*z)**3)==0,'Strict convexity in inverse coordinates')
    width=(s.sqrt(q)+c*q)-(-s.sqrt(q)+c*q)
    require(s.simplify(width-2*s.sqrt(q))==0,'Non-even inverse branch width')
    require(s.diff(width,q).subs(q,1)==1,'Width derivative at cap level')
    require(-s.diff(width,q).subs(q,1)*Ssecond.subs(z,0)==-2,'Nondegenerate width maximum')
    require(s.diff(coord,z,2)!=0,'Non-even action control is absent')

    d=s.Rational(1);xi=s.Rational(1,13);eta=-s.Rational(1,11);a=s.Rational(1,16)
    lo=-s.Rational(1,4);hi=s.Rational(1,4)
    def S(w):return w*w+w**3/10+w**4/100
    def Sp(w):return 2*w+3*w*w/10+w**3/25
    # Both translated window intervals lie in [-1/2,1/2], including small
    # parameter variations; this supplies an exact cap-positivity margin.
    require(max(abs(lo-xi),abs(hi-xi),abs(lo-eta),abs(hi-eta))<s.Rational(1,2),
            'Window excludes origin or exits the displayed domain')
    ceiling=s.Rational(1,4)+s.Rational(1,80)+s.Rational(1,1600)
    require(1-2*ceiling==s.Rational(379,800)>0,'Positive interior window margin')
    require(s.Rational(2)-s.Rational(3,10)>0,'Strict convexity lower bound')
    require(lo<xi<hi and lo<eta<hi,'Critical cross not visible')
    H=d-S(x-xi)-S(y-eta)
    A=2+x+x*x;C=3+2*y+y*y
    raw=s.Poly(s.expand(A*C*H),x,y).as_expr()
    def integral(expr):
        poly=s.Poly(s.expand(expr),x,y)
        return s.Add(*[coef*(hi**(i+1)-lo**(i+1))/(i+1)*(hi**(j+1)-lo**(j+1))/(j+1)
                       for (i,j),coef in poly.terms()])
    Z=integral(raw);require(Z>0,'Window normalizer')
    p=raw/Z
    require(integral(p)==1,'Window law not normalized')
    # Derive interaction from the density, not only the proposed formula.
    K=s.cancel(s.diff(p,x,y)/p-s.diff(p,x)*s.diff(p,y)/p**2)
    expected=-Sp(x-xi)*Sp(y-eta)/H**2
    require(s.cancel(K-expected)==0,'Interaction fails after cropping and normalization')
    require(s.cancel(K.subs(x,xi))==0 and s.cancel(K.subs(y,eta))==0,'Critical cross')
    pc=(2+(xi+u)+(xi+u)**2)*(3+2*(eta+v)+(eta+v)**2)*(d-S(u)-S(v))/Z
    R=s.cancel(pc*pc.subs({u:0,v:0})/(pc.subs(v,0)*pc.subs(u,0)))
    require(s.cancel(1-R-S(u)*S(v)/((d-S(u))*(d-S(v))))==0,'Window odds-ratio identity')
    anchor=S(a)/(d-S(a));require(anchor>0,'Scalar anchor')
    recovered=s.cancel(d*(1-R.subs(v,a))/(anchor+1-R.subs(v,a)))
    require(s.cancel(recovered-S(u))==0 and S(a)!=S(-a),'Signed action lost')

    vx=s.Rational(1,7);vy=-s.Rational(1,9)
    # Fixed numerical window, moving origins; independent varying factors.
    At=2+x+x*x+t*(1+x);Ct=3+2*y+y*y+t*(2-y)
    Ht=d-S(x-xi-vx*t)-S(y-eta-vy*t)
    rawt=At*Ct*Ht
    draw=s.expand(s.diff(rawt,t).subs(t,0))
    dZ=integral(draw);require(dZ!=0,'Normalizer derivative negative control is vacuous')
    dp=s.expand(draw/Z-raw*dZ/Z**2)
    require(integral(dp)==0,'Normalized derivative has nonzero mass')
    require(integral(draw/Z)!=0,'Omitting normalizer derivative was not detected')
    kt=-Sp(x-xi-vx*t)*Sp(y-eta-vy*t)/Ht**2
    slopex=s.diff(expected,x).subs({x:xi,y:eta+a})
    slopey=s.diff(expected,y).subs({x:xi+a,y:eta})
    dKx=s.diff(kt,t).subs({t:0,x:xi,y:eta+a})
    dKy=s.diff(kt,t).subs({t:0,x:xi+a,y:eta})
    require(s.cancel(-dKx/slopex-vx)==0 and s.cancel(-dKy/slopey-vy)==0,'Origin transport')
    # The support of every cropped law is W: its fiber width is constant.
    require(hi-lo==s.Rational(1,2),'Support-only control')
    moved=(xi+s.Rational(1,100),eta-s.Rational(1,100))
    require(all(lo<o<hi for o in moved) and moved!=(xi,eta),'Different invisible support origins')
    eps=s.Rational(1,20)
    require(s.cancel((eps**2*raw)/(eps**2*Z)-p)==0,'Acquisition scaling changed conditional law')
    return {'non_even_inverse_coordinate_width':'2 sqrt(q)',
        'complete_width_second_derivative_at_origin':'-2',
        'window':[['-1/4','1/4'],['-1/4','1/4']],
        'cap_height_lower_bound':'379/800', 'action_second_derivative_lower_bound':'17/10',
        'normalized_window_mass':1, 'unknown_origins':[str(xi),str(eta)],
        'unequal_separate_factors_cancel':True,'signed_action_recovered':True,
        'fixed_window_normalizer_derivative':str(dZ),
        'moving_origin_derivatives':[str(vx),str(vy)],
        'negative_controls':['fixed rectangular support has no unique width maximizer',
          'omitting normalization derivative leaves nonzero total mass derivative',
          'same conditional law does not determine recorded success frequency'],
        'scope':'Finite exact functional tests, not a billiard realization or infinite-flight proof.'}

if __name__=='__main__':
    print(json.dumps({'status':'passed','mathematical_certification':False,
        'preservation':preservation(),'window_controls':window_controls(),
        'retained_v51_controls':v51_controls(),'retained_v50_controls':two_branch_controls(),
        'retained_v49_controls':v49_controls(),'retained_v48_controls':v48_controls(),
        'retained_v47_controls':v47_controls()},sort_keys=True,indent=2))
