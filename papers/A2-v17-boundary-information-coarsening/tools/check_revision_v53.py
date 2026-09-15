#!/usr/bin/env python3
"""Verbatim preservation and finite realized-window controls; not a proof certificate."""
from __future__ import annotations
from collections import Counter
import hashlib
import json
import re
import sympy as s
from materialize_revision_v53 import P, ARCHIVE, CHANGES, NEW_INPUTS, revised
from source_provenance import require, blob_id, graph
from check_revision_v50 import ENV, BLOCK, two_branch_controls
from check_revision_v52 import window_controls
from check_revision_v51 import interaction_controls as v51_controls
from check_revision_v49 import new_controls as v49_controls
from check_revision_v48 import differential_controls as v48_controls
from check_revision_v47 import finite_diagnostics as v47_controls


def preservation() -> dict:
    groups=json.loads((ARCHIVE/'active-source-manifest.json').read_text())
    old={n:v for group in groups.values() for n,v in group.items()}
    require(len(old)==110,'Wrong reviewed baseline count')
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


def small_window_controls() -> dict:
    a,b,d,h,z,w=s.symbols('a b d h z w', positive=True)
    F=s.Rational(1,9)-z*z*w*w
    def integrate(poly):
        p=s.Poly(s.expand(poly),z,w)
        return s.Add(*[c*s.Rational(1-(-1)**(i+1),i+1)*s.Rational(1-(-1)**(j+1),j+1)
                      for (i,j),c in p.terms()])
    require(integrate(F)==0,'Centering of the normalized leading score')
    norm=integrate(F**2)
    require(norm==s.Rational(224,2025),'Squared interaction integral')
    C=s.factor((b*b-a*a)**2*norm/(256*d**4))
    require(s.simplify(C-7*(b*b-a*a)**2/(16200*d**4))==0,'Hellinger coefficient')
    J=4*C
    mean_gap=14*(b*b-a*a)/(2025*d*d)
    variance=s.Rational(56,2025)
    require(s.simplify(mean_gap**2/variance-J)==0,'Mean test critical information')
    bad=-a*a*z*z*w*w/(16*d*d)
    require(integrate(bad)!=0,'Omitted-normalizer control must fail normalization')
    badC=s.factor((b*b-a*a)**2*integrate(z**4*w**4)/(256*d**4))
    require(s.simplify(badC-C)!=0,'Omitted normalization must change the information constant')
    # Different higher even jets: the h^4 coefficient must not depend on them.
    c0,c1=s.symbols('c0 c1',real=True)
    tx=a*h*h*z*z/(2*d)+(c0/d+a*a/(4*d*d))*h**4*z**4
    tw=tx.subs(z,w)
    I=a*h*h/(3*d)+2*(c0/d+a*a/(4*d*d))*h**4/5
    approx=s.series((1-tx*tw)/(4-I*I),h,0,6).removeO()
    require(s.simplify(approx-(s.Rational(1,4)+a*a*h**4*F/(16*d*d)))==0,
            'Fourth-order coefficient depends on higher even action jets')
    # Independent quadratic half-line sum for equal-curvature contacts.
    r,g=s.symbols('r g',positive=True)
    c=(r+1/r)/2
    half_hessian=s.factor((c*(1+r*r)-2*r)/(g*(1-r*r)))
    require(s.simplify(half_hessian-(1/r-r)/(2*g))==0,'Actual leading half-line Hessian')
    require(s.simplify(half_hessian**2-(c*c-1)/(g*g))==0,'Leading geometry square')
    R=s.Rational(1,10); gap=1-2*R
    s0,s1=R/128,R/64
    k0,k1=1/(R-16*s0),1/(R-16*s1)
    A0,A1=k0*k0+2*k0/gap,k1*k1+2*k1/gap
    require((A0,A1,A1-A0)==(s.Rational(7800,49),s.Rational(1900,9),s.Rational(22900,441)),
            'Realized pair coefficient')
    require(R-16*s1==3*R/4 and R-2*s1>0 and gap>0,'Convexity/separation margins')
    require(1-R>s.Rational(4,5),'All-lattice axis clearance lower bound')
    require(R-s0!=R-s1,'Perimeters must differ')
    # A crop normalizer and its perturbation both have area order h^2.
    eps=s.symbols('eps',positive=True)
    q=s.cancel(h*h*(1+eps*z)/(4*h*h))
    require(s.simplify(q-s.Rational(1,4)-eps*z/4)==0,'False area loss in rescaled quotient')
    return {'interaction_square_integral':str(norm),
        'quadratic_functional_example_coefficient':str(C.subs({a:1,b:2,d:3})),
        'Hellinger_coefficient_formula':str(C),'critical_information_equals_four_times_Hellinger':True,
        'mean_test_attains_critical_information':True,'higher_even_jets_do_not_change_leading_term':True,
        'realized_squared_action_hessians':[str(A0),str(A1)],
        'realized_squared_hessian_difference':str(A1-A0),
        'minimum_radius_of_curvature':str(R-16*s1),'common_gap':str(gap),
        'third_obstacle_axis_segment_clearance':str(1-R),
        'negative_controls':['omitted normalizer creates nonzero leading mass',
                             'omitted normalizer changes Hellinger coefficient'],
        'scope':'Exact finite algebra. Actual nonlinear actions, all-lattice geometry and product limits are justified by the written proofs, not by numerical simulation.'}

if __name__=='__main__':
    print(json.dumps({'status':'passed','mathematical_certification':False,
        'preservation':preservation(),'small_window_controls':small_window_controls(),
        'retained_v52_window_controls':window_controls(),
        'retained_v51_controls':v51_controls(),'retained_v50_controls':two_branch_controls(),
        'retained_v49_controls':v49_controls(),'retained_v48_controls':v48_controls(),
        'retained_v47_controls':v47_controls()},sort_keys=True,indent=2))
