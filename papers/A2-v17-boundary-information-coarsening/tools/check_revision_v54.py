#!/usr/bin/env python3
"""Preservation and finite controls for A2 v54, not a mathematical certificate."""
from __future__ import annotations
from collections import Counter
from fractions import Fraction as F
import hashlib
import json
import math
import re
import sympy as s
from materialize_revision_v54 import P, ARCHIVE, CHANGES, MODULE, revised, old_corollary_region
from source_provenance import require, blob_id, graph
from check_revision_v50 import ENV, BLOCK, two_branch_controls
from check_revision_v53 import small_window_controls
from check_revision_v52 import window_controls
from check_revision_v51 import interaction_controls as v51_controls
from check_revision_v49 import new_controls as v49_controls
from check_revision_v48 import differential_controls as v48_controls
from check_revision_v47 import finite_diagnostics as v47_controls


def preservation() -> dict:
    groups=json.loads((ARCHIVE/'active-source-manifest.json').read_text())
    old={n:v for group in groups.values() for n,v in group.items()}
    require(len(old)==111,'Wrong reviewed v53 baseline count')
    before=Counter(); oldlabels=set(); preserved=0; strengthened=[]
    for name,info in old.items():
        raw=(ARCHIVE/name if name in CHANGES else P/name).read_bytes()
        require(len(raw)==info['bytes'] and hashlib.sha256(raw).hexdigest()==info['sha256']
                and blob_id(raw)==info['git_blob'],'Baseline identity: '+name)
        text=raw.decode(); current=(P/name).read_text()
        before.update(ENV.findall(text)); oldlabels.update(re.findall(r'\\label\{([^}]+)\}',text))
        if name in CHANGES:
            require(current==revised(name,text),'Non-prescribed edit: '+name)
        a,b=old_corollary_region(text) if name==MODULE else (-1,-1)
        for match in BLOCK.finditer(text):
            if a<=match.start()<b:
                strengthened.append({'file':name,'environment':match.group(1),
                    'old_block_sha256':hashlib.sha256(match.group(0).encode()).hexdigest()})
            else:
                require(match.group(0) in current,'Lost statement/proof: '+name)
                preserved+=1
        require(re.findall(r'\\input\{([^}]+)\}',text)==
                re.findall(r'\\input\{([^}]+)\}',current),'Changed input order: '+name)
    require(len(strengthened)==2,'Only one corollary and its proof may be strengthened')
    active=graph(P,'main.tex')|graph(P,'two_collision.tex')
    require(active==set(old),'Lost/unexpected active input')
    joined='\n'.join((P/n).read_text() for n in sorted(active))
    require(Counter(ENV.findall(joined))==before+Counter({'theorem':1,'proof':1}),
            'Environment inventory differs beyond new theorem/proof')
    labels=re.findall(r'\\label\{([^}]+)\}',joined)
    require(len(labels)==len(set(labels)) and oldlabels<=set(labels),'Lost/duplicate label')
    refs=set(re.findall(r'\\(?:ref|eqref|pageref|autoref)\{([^}]+)\}',joined))
    require(not {r for r in refs if r not in labels and not r.startswith('TC-')},'Unresolved references')
    cites={k.strip() for c in re.findall(r'\\cite(?:\[[^\]]*\])?\{([^}]+)\}',joined) for k in c.split(',')}
    bib=set(re.findall(r'\\bibitem(?:\[[^\]]*\])?\{([^}]+)\}',joined))
    require(cites<=bib,'Unresolved citation')
    main=(P/'main.tex').read_text()
    require(main.index(r'\input{article/01_introduction_v41}')>main.index(r'\appendix'),
            'The full catalogue must stay compiled in the appendix')
    return {'baseline_inputs':len(old),'active_inputs':len(active),
        'unchanged_in_place':len(old)-len(CHANGES),'archived_exact_originals':list(CHANGES),
        'inherited_blocks_preserved_verbatim':preserved,'strengthened_old_blocks':strengthened,
        'inherited_environments':dict(sorted(before.items())),
        'new_environments':{'theorem':1,'proof':1},'active_labels':len(labels),
        'unresolved_references_or_citations':[],
        'scope':'One corollary/proof is strengthened in place; all its old conclusions are retained as consequences, not claimed verbatim.'}


def finite_controls() -> dict:
    z=s.symbols('z',real=True)
    epsilon=s.symbols('epsilon',positive=True)
    # Taylor check of affinity for two positive two-cell densities.
    affinity=(s.sqrt(1+2*epsilon)+s.sqrt(1-2*epsilon))/2
    H2=s.series(2-2*affinity,epsilon,0,6).removeO()
    require(s.expand(H2)==epsilon**2+s.Rational(5,4)*epsilon**4,'Quadratic Hellinger order')
    cases=0
    for n in range(1,17):
        for k in range(1,20):
            x=F(k,40)
            require(1-(1-x)**n<=n*x,'Affinity tensorization inequality')
            cases+=1
    # Strict improvement in sufficient conditions: n=m^8, epsilon=m^-5.
    for m in (2,4,8,16):
        n=m**8; eps=F(1,m**5)
        require(n*eps**2==F(1,m*m) and n*eps==m**3,'Joint-flight control')
    # Without a uniform lower density bound, H^2 may be linear in epsilon.
    bad=s.series(2-2*s.sqrt(1-epsilon),epsilon,0,3).removeO()
    require(s.expand(bad).coeff(epsilon,1)==1,'Lower-bound negative control')
    # Range-one Hoeffding budget after a finite-flight mean perturbation.
    ideal_gap=F(1,16); mean_error=F(1,64)
    require(ideal_gap/2-mean_error==ideal_gap/4,'Direct mean-test margin')
    require(2*(ideal_gap/4)**2==ideal_gap**2/8,'Direct mean-test exponent')
    require(s.Rational(35,3)>s.Rational(71,7)>1,'Actual hyperbolic ordering')
    # Exact finite geometric/terminal-mark laws, including a common cemetery.
    p0,p1=F(1,16),F(1,1024)
    mark0,mark1=(F(1,3),F(2,3)),(F(1,2),F(1,2))
    checked=[]
    for b in (1,2,7,31):
        def capped(p,mark):
            out=[(1-p)**b]
            for k in range(1,b+1):
                out.extend((1-p)**(k-1)*p*q for q in mark)
            require(sum(out)==1,'Capped law normalization')
            return out
        a0,a1=1-(1-p0)**b,1-(1-p1)**b
        t0,t1=capped(p0,mark0),capped(p1,mark1)
        tv=sum(abs(x-y) for x,y in zip(t0,t1))/2
        require(a0-a1<=tv<=a0,'Cemetery total-variation sandwich')
        indicator_error=((1-p0)**b+1-(1-p1)**b)/2
        require(indicator_error==(1-a0+a1)/2,'Indicator risk')
        for p in (p0,p1):
            expected=sum(k*(1-p)**(k-1)*p for k in range(1,b+1))+b*(1-p)**b
            require(expected==(1-(1-p)**b)/p,'Exact capped preparation charge')
        mix=[(x+y)/2 for x,y in zip(t0,t1)]
        require(sum(abs(x-y) for x,y in zip(t0,mix))/2==tv/2,'State-independent mixture bound')
        checked.append(b)
    rho=p1/p0
    m=math.ceil(1/math.sqrt(float(p0*p1)))
    require((1-p1)**(m-1)!=(1-p1)**m,'One-based waiting-time negative control')
    require(F(m)*p1<=F(1,8)+p1,'Rounded first-waiting threshold')
    # A cap threshold must not always be the event of any acceptance:
    # when both b*p_i diverge that indicator loses separation; use min(b,m).
    numeric=[]
    for M in (16,64,256):
        pp0=1/M**2;pp1=1/M**4;bb=M**2
        a0=-math.expm1(bb*math.log1p(-pp0));a1=-math.expm1(bb*math.log1p(-pp1))
        risk=(1-a0+a1)/2
        require(abs(risk-math.exp(-1)/2)<2/M**2,'Critical cemetery risk approximation')
        numeric.append({'M':M,'indicator_error':format(risk,'.8f')})
    huge_b=10**7
    survival1_upper=1/(1+huge_b*p1)
    require((1-survival1_upper)/2>F(49,100),'Large-cap any-acceptance negative control')
    return {'positive_two_cell_Hellinger_series':str(H2),
        'exact_affinity_cases':cases,'strict_product_condition_improvement':True,
        'direct_mean_test_exponent_divisor':8,'actual_cosh_gamma':['71/7','35/3'],
        'exact_capped_law_tests':checked,'critical_lambda_one_controls':numeric,
        'negative_controls':['missing lower density bound changes Hellinger order',
          'off-by-one geometric survival changes waiting law',
          'any-acceptance indicator fails at a cap where both expected success counts diverge'],
        'scope':'Finite distribution and exact algebra controls only; actual billiard rarity, joint limits and deficiency statements rely on the written proofs.'}

if __name__=='__main__':
    print(json.dumps({'status':'passed','mathematical_certification':False,
        'preservation':preservation(),'finite_controls':finite_controls(),
        'retained_v53_controls':small_window_controls(),'retained_v52_controls':window_controls(),
        'retained_v51_controls':v51_controls(),'retained_v50_controls':two_branch_controls(),
        'retained_v49_controls':v49_controls(),'retained_v48_controls':v48_controls(),
        'retained_v47_controls':v47_controls()},indent=2,sort_keys=True))
